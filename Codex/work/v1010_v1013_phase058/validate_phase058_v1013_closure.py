#!/usr/bin/env python3
"""Validate the Phase 058 v1.0.13 explanation-closure audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_058_V1013_CLOSURE_AUDIT.json"
INSPECTOR_PATH = (
    ROOT
    / "Codex/work/v1010_v1013_phase058/inspect_phase058_v1013_closure.py"
)
V13_DIR = ROOT / "Claude/docs/v1.0.13"
CH1 = V13_DIR / "graphite_ica_ch1_v1.0.13.tex"
CH2 = V13_DIR / "graphite_ica_ch2_v1.0.13.tex"
PDF1 = V13_DIR / "graphite_ica_ch1_v1.0.13.pdf"
CODE = V13_DIR / "Anode_Fit_v1.0.13.py"


def load_inspector():
    spec = importlib.util.spec_from_file_location("phase058_closure_inspector", INSPECTOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load inspector: {INSPECTOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count(pattern: str, text: str, flags: int = 0) -> int:
    return len(re.findall(pattern, text, flags))


def slice_text(lines: list[str], start: int, end: int) -> str:
    return "\n".join(lines[start - 1 : end])


def main() -> int:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    inspector = load_inspector()
    ch1_text = CH1.read_text(encoding="utf-8")
    ch2_text = CH2.read_text(encoding="utf-8")
    code_text = CODE.read_text(encoding="utf-8")
    ch1_lines = ch1_text.splitlines()
    ch2_lines = ch2_text.splitlines()
    rows1 = inspector.section_rows(ch1_text)
    rows2 = inspector.section_rows(ch2_text)
    checks: dict[str, bool] = {}

    paths = {
        "chapter_1_tex": CH1,
        "chapter_2_tex": CH2,
        "chapter_1_pdf": PDF1,
        "production_code": CODE,
    }
    for key, path in paths.items():
        checks[f"hash_{key}"] = sha256(path) == data["source_hashes"][key]

    structure = data["structure"]
    actual_structure = {
        "chapter_1_source_lines": len(ch1_lines),
        "chapter_1_pdf_pages": len(PdfReader(PDF1).pages),
        "chapter_1_heading_blocks": len(rows1),
        "chapter_1_section_count": sum(row["level"] == "section" for row in rows1),
        "chapter_1_subsection_count": sum(
            row["level"] == "subsection" for row in rows1
        ),
        "chapter_1_subsubsection_count": sum(
            row["level"] == "subsubsection" for row in rows1
        ),
        "chapter_1_equation_label_count": count(r"\\label\{eq:", ch1_text),
        "chapter_1_citation_command_count": count(r"\\cite\{", ch1_text),
        "chapter_1_bibliography_item_count": count(
            r"^\\bibitem\{", ch1_text, re.MULTILINE
        ),
        "chapter_2_source_lines": len(ch2_lines),
        "chapter_2_heading_blocks": len(rows2),
        "chapter_2_section_count": sum(row["level"] == "section" for row in rows2),
        "chapter_2_subsection_count": sum(
            row["level"] == "subsection" for row in rows2
        ),
        "chapter_2_equation_label_count": count(r"\\label\{eq:", ch2_text),
        "chapter_2_citation_command_count": count(r"\\cite\{", ch2_text),
        "chapter_2_bibliography_item_count": count(
            r"^\\bibitem\{", ch2_text, re.MULTILINE
        ),
    }
    bib_keys = set(
        re.findall(r"^\\bibitem\{([^}]+)", ch1_text + "\n" + ch2_text, re.MULTILINE)
    )
    actual_structure["combined_unique_bibliography_key_count"] = len(bib_keys)
    for key, value in actual_structure.items():
        checks[f"structure_{key}"] = value == structure[key]

    region_totals = {
        "source_line_count": lambda block, start, end: end - start + 1,
        "code_mentions": lambda block, start, end: count(r"\\code\{", block),
        "equation_labels": lambda block, start, end: count(r"\\label\{eq:", block),
        "citation_commands": lambda block, start, end: count(r"\\cite\{", block),
    }
    for region in data["chapter_1_regions"]:
        start = region["start_line"]
        end = region["end_line"]
        block = slice_text(ch1_lines, start, end)
        for key, calculator in region_totals.items():
            checks[f"region_{region['id']}_{key}"] = (
                calculator(block, start, end) == region[key]
            )

    policy = data["theory_only_policy"]
    total_code = count(r"\\code\{", ch1_text)
    narrow = slice_text(
        ch1_lines,
        policy["existing_labeled_lco_code_section_start_line"],
        policy["existing_labeled_lco_code_section_end_line"],
    )
    generous = slice_text(
        ch1_lines,
        policy["generous_implementation_boundary_start_line"],
        policy["generous_implementation_boundary_end_line"],
    )
    blocks_with_code = sum(row["code_mentions"] > 0 for row in rows1)
    outside_generous_blocks = sum(
        row["code_mentions"] > 0
        and not (
            policy["generous_implementation_boundary_start_line"]
            <= row["start_line"]
            <= policy["generous_implementation_boundary_end_line"]
        )
        for row in rows1
    )
    policy_actual = {
        "chapter_1_total_code_mentions": total_code,
        "chapter_1_heading_blocks_with_code_mentions": blocks_with_code,
        "code_mentions_inside_existing_labeled_lco_code_section": count(
            r"\\code\{", narrow
        ),
        "code_mentions_outside_existing_labeled_lco_code_section": total_code
        - count(r"\\code\{", narrow),
        "code_mentions_inside_generous_implementation_boundary": count(
            r"\\code\{", generous
        ),
        "code_mentions_outside_generous_implementation_boundary": total_code
        - count(r"\\code\{", generous),
        "heading_blocks_with_code_mentions_outside_generous_boundary": outside_generous_blocks,
        "chapter_2_total_code_mentions": count(r"\\code\{", ch2_text),
    }
    for key, value in policy_actual.items():
        checks[f"policy_{key}"] = value == policy[key]

    width_cluster = next(
        row
        for row in data["overlapping_explanation_clusters"]
        if row["id"] == "R13-03"
    )
    checks["literal_empirical_width_formula_count"] = (
        count(r"(?:w_j=)?n_jRT/F", ch1_text)
        == width_cluster["chapter_1_literal_occurrence_count"]
    )
    checks["overlap_cluster_count"] = len(
        data["overlapping_explanation_clusters"]
    ) == 4

    line_snippets = {
        1726: "기본값 $\\nu=2$ 에선 $\\sim23\\%$",
        1902: "고전압, 범위 밖",
        2123: "초기값 미배정",
        2323: "모델 가정",
        2731: "다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제",
    }
    for line_number, snippet in line_snippets.items():
        checks[f"line_evidence_{line_number}"] = snippet in ch1_lines[line_number - 1]

    closure = data["closure_dimensions"]
    closure_ids = [row["id"] for row in closure]
    decisions = {row["id"]: row["decision"] for row in closure}
    checks["closure_dimension_count"] = len(closure) == 20
    checks["closure_ids_unique"] = len(set(closure_ids)) == len(closure_ids)
    checks["closure_ids_complete"] = closure_ids == [
        f"C13-{number:02d}" for number in range(1, 21)
    ]
    expected_decisions = {
        "C13-02": "REJECT_CURRENT_CHAPTER_1_ARCHITECTURE",
        "C13-08": "THEORY_ONLY",
        "C13-09": "CORRECT_LOCAL_STATE_DEPENDENCE",
        "C13-13": "REJECT_AS_COVERED",
        "C13-15": "MISSING_FROM_CURRENT_USER_GOAL",
        "C13-16": "MISSING_FROM_CURRENT_USER_GOAL",
        "C13-18": "MISSING",
        "C13-19": "REJECT_AS_FULL_GATE",
    }
    for key, value in expected_decisions.items():
        checks[f"decision_{key}"] = decisions[key] == value

    files = sorted(path.name for path in V13_DIR.iterdir() if path.is_file())
    directory = data["v1013_directory_evidence"]
    checks["directory_top_level_file_count"] = (
        len(files) == directory["top_level_file_count"]
    )
    checks["golden_snapshot_count"] = (
        sum(name == "golden_graphite_ref.npz" for name in files)
        == directory["golden_model_output_snapshot_count"]
    )
    public_data_suffixes = {".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".h5", ".hdf5"}
    checks["public_dataset_count"] = (
        sum(Path(name).suffix.lower() in public_data_suffixes for name in files)
        == directory["public_experimental_dataset_count"]
    )
    checks["fit_result_count"] = (
        sum(
            bool(re.search(r"(fit_result|best_params|posterior|holdout)", name, re.I))
            for name in files
        )
        == directory["fit_result_count"]
    )
    checks["optimizer_state_count"] = (
        sum(bool(re.search(r"(study|optimizer|optuna).*\.(db|pkl|pickle)$", name, re.I)) for name in files)
        == directory["optimizer_state_count"]
    )
    silicon_count = count(
        r"실리콘|silicon|\bSi\b",
        ch1_text + "\n" + ch2_text + "\n" + code_text,
        re.IGNORECASE,
    )
    checks["silicon_path_count"] = (
        silicon_count == directory["silicon_theory_or_code_path_count"]
    )

    expected_verdict = (
        "V1013_HAS_REAL_PEDAGOGICAL_DEPTH_BUT_50_PAGES_DO_NOT_CLOSE_"
        "THE_PHYSICS_CHEMISTRY_OBSERVATION_OR_VALIDATION_CHAIN"
    )
    checks["verdict"] = data["verdict"] == expected_verdict
    checks["rewrite_requirement_count"] = len(data["rewrite_requirements"]) == 10
    checks["carry_forward_count"] = len(data["carry_forward"]) == 7

    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "check_count": len(checks),
        "failures": failures,
        "gate": (
            "PASS_P058_V1013_EXPLANATION_CLOSURE"
            if not failures
            else "FAIL_P058_V1013_EXPLANATION_CLOSURE"
        ),
        "chapter_1_pdf_pages": actual_structure["chapter_1_pdf_pages"],
        "chapter_1_code_mentions": total_code,
        "chapter_1_code_mentions_outside_generous_boundary": policy_actual[
            "code_mentions_outside_generous_implementation_boundary"
        ],
        "closure_dimension_count": len(closure),
        "public_experimental_dataset_count": directory[
            "public_experimental_dataset_count"
        ],
        "verdict": data["verdict"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
