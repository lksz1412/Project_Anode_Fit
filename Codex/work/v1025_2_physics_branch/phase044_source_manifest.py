#!/usr/bin/env python3
"""Build the Phase 044 byte-level source inventory.

The manifest is an inventory, not a scientific verdict and not proof that a
file was read.  Human full-read coverage is recorded separately in the Phase
044 result.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


REPO = Path(__file__).resolve().parents[3]
OUTPUT = REPO / "Codex/results/PHASE_044_SOURCE_FREEZE_MANIFEST.json"
BASELINE_COMMIT = "ab196b292e14492b647f87a6c0d1d8c9ed0630ab"

TEXT_SUFFIXES = {".csv", ".html", ".json", ".md", ".py", ".tex", ".txt"}
VERSION_NAMES = {
    "v1.0.10",
    "v1.0.11",
    "v1.0.12",
    "v1.0.13",
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
    "v1.0.19",
    "v1.0.20",
    "v1.0.21",
    "v1.0.22",
    "v1.0.23",
    "v1.0.24",
    "v1.0.24.1",
    "v1.0.25",
    "v1.0.25.1",
    "v1.0.25.2",
}
EXCLUDED_DIRTY_PATHS = {
    "Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html",
}

CODEX_CANDIDATES = [
    "Codex/results/graphite_ica_ch1_codex_candidate_v5.tex",
    "Codex/results/graphite_ica_ch2_codex_candidate_v1.tex",
    "Codex/results/graphite_ica_ch3_codex_candidate_v1.tex",
    "Codex/results/graphite_ica_ch4_codex_candidate_v1.tex",
    "Codex/results/graphite_ica_ch5_codex_candidate_v1.tex",
]

CODEX_GOVERNANCE = [
    "Codex/plans/2026-06-01-chapter1-claude-base-review-repair-plan.md",
    "Codex/plans/2026-06-01-claude-rebuilt-base-codex-completion-roadmap.md",
    "Codex/plans/2026-06-02-ch1-v5-repair-and-ch2-5-resume-plan.md",
    "Codex/plans/2026-06-02-chapter1-completion-criteria-addendum.md",
    "Codex/plans/2026-06-02-chapter1-v4-full-rebuild-10pass-plan.md",
    "Codex/plans/2026-06-02-claude-final-full-10pass-review-plan.md",
    "Codex/results/PHASE_035_CLAUDE_CH1_REVIEW_INTAKE_AND_V5_GATE.md",
    "Codex/results/PHASE_036_CH1_V5_REPAIR_RESULT.md",
    "Codex/results/PHASE_037_CH1_V5_10PASS_REVIEW.md",
    "Codex/results/PHASE_038_CH1_V5_VERIFICATION_AND_HANDOVER.md",
    "Codex/results/PHASE_039_CH2_V5_SPINE_PLAN_AND_SOURCE_REVIEW.md",
    "Codex/results/PHASE_040_CH2_CANDIDATE_V1_10PASS_AND_VERIFICATION.md",
    "Codex/results/PHASE_041_CH3_CANDIDATE_V1_10PASS_AND_VERIFICATION.md",
    "Codex/results/PHASE_042_CH4_CANDIDATE_V1_10PASS_AND_VERIFICATION.md",
    "Codex/results/PHASE_042A_CH4_MISSING_CHARACTER_CLEANUP_RESULT.md",
    "Codex/results/PHASE_043_CH5_CANDIDATE_V1_10PASS_AND_VERIFICATION.md",
]

RELEASE_MASTERS = [
    "Claude/docs/v1.0.25.2/ch1_graphite_v1.0.24.tex",
    "Claude/docs/v1.0.25.2/ch2_lco_v1.0.24.tex",
    "Claude/docs/v1.0.25.2/ch3_si_v1.0.24.tex",
]

RELEASE_SUPPORT = [
    "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py",
    "Claude/docs/v1.0.25.2/CODE_GUIDE_v24.md",
    "Claude/docs/v1.0.25.2/FITTING_GUIDE.md",
    "Claude/docs/v1.0.25.2/results/V1025_CHANGE_LEDGER.md",
    "Claude/docs/v1.0.25.2/results/V1025_DATA_ADDENDUM.md",
    "Claude/docs/v1.0.25.2/test_gates_v1024.py",
    "Claude/docs/v1.0.25.2/test_gates_v1025.py",
    "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md",
    "Claude/results/comp_v26_data/build_two_versions.py",
    "Claude/results/comp_v26_data/test_skew_regsol_v2.py",
    "Claude/results/comp_v26_data/test_gallery_vs_regsol.py",
    "Claude/results/comp_v26_data/bdd_dqdv.py",
    "Claude/results/comp_v26_data/regsol_kernel.py",
    "Claude/results/comp_v26_data/out_versions/summary_versions.json",
    "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json",
    "Claude/results/comp_v24/sintef_data/gr.csv",
    "Claude/results/comp_v24/sintef_data/si.csv",
    "Claude/results/comp_v24/sintef_data/sigr.csv",
]

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")


def line_count(data: bytes) -> int:
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def record(path: Path, group: str) -> dict:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "group": group,
        "bytes": len(data),
        "lines": line_count(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def resolve_tex_graph(master_paths: list[Path]) -> tuple[set[Path], list[dict]]:
    visited: set[Path] = set()
    edges: list[dict] = []

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in visited:
            return
        visited.add(resolved)
        text = resolved.read_text(encoding="utf-8")
        for target in INPUT_RE.findall(text):
            child = (resolved.parent / target)
            if child.suffix == "":
                child = child.with_suffix(".tex")
            child = child.resolve()
            if not child.is_file():
                raise FileNotFoundError(
                    f"unresolved TeX input from {resolved.relative_to(REPO)}: {target}"
                )
            edges.append(
                {
                    "from": resolved.relative_to(REPO).as_posix(),
                    "to": child.relative_to(REPO).as_posix(),
                }
            )
            visit(child)

    for master in master_paths:
        visit(master)
    return visited, edges


def lineage_files() -> list[Path]:
    root = REPO / "Claude/docs"
    files: list[Path] = []
    for version_name in sorted(VERSION_NAMES):
        version_root = root / version_name
        if not version_root.is_dir():
            raise FileNotFoundError(version_root)
        files.extend(
            path
            for path in version_root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in TEXT_SUFFIXES
            and "__pycache__" not in path.parts
            and path.relative_to(REPO).as_posix() not in EXCLUDED_DIRTY_PATHS
        )
    return sorted(set(files))


def main() -> None:
    groups: list[tuple[str, list[Path]]] = [
        ("codex_candidate", [REPO / path for path in CODEX_CANDIDATES]),
        ("codex_governance", [REPO / path for path in CODEX_GOVERNANCE]),
        ("release_master", [REPO / path for path in RELEASE_MASTERS]),
        ("release_support", [REPO / path for path in RELEASE_SUPPORT]),
        ("lineage_text_inventory", lineage_files()),
    ]

    release_graph, release_edges = resolve_tex_graph(
        [REPO / path for path in RELEASE_MASTERS]
    )
    groups.append(("release_recursive_tex", sorted(release_graph)))

    records_by_path: dict[str, dict] = {}
    memberships: dict[str, set[str]] = {}
    for group, paths in groups:
        for path in paths:
            if not path.is_file():
                raise FileNotFoundError(path)
            relative = path.relative_to(REPO).as_posix()
            memberships.setdefault(relative, set()).add(group)
            if relative not in records_by_path:
                records_by_path[relative] = record(path, group)

    records = []
    for relative, item in records_by_path.items():
        item["groups"] = sorted(memberships[relative])
        item.pop("group", None)
        records.append(item)
    records.sort(key=lambda item: item["path"])
    content_groups: dict[str, list[str]] = {}
    for item in records:
        content_groups.setdefault(item["sha256"], []).append(item["path"])
    duplicate_groups = [
        {"sha256": digest, "paths": paths}
        for digest, paths in content_groups.items()
        if len(paths) > 1
    ]
    duplicate_groups.sort(key=lambda item: (-len(item["paths"]), item["paths"][0]))

    manifest = {
        "schema": "phase044-source-freeze-v1",
        "baseline_commit": BASELINE_COMMIT,
        "scientific_source_exclusion": ["Claude/docs/v1.0.26A-regsol", "Claude/docs/v1.0.26B-gallery"],
        "working_tree_exclusion": sorted(EXCLUDED_DIRTY_PATHS),
        "notice": (
            "Designated text-source byte inventory only. Presence in this "
            "manifest is not proof of full reading or scientific validity; "
            "binary artifacts and visual QA are outside this manifest."
        ),
        "inventory_scope": {
            "lineage_text_suffixes": sorted(TEXT_SUFFIXES),
            "binary_artifacts": "excluded",
            "binary_visual_qa": "not performed",
        },
        "counts": {
            "unique_files": len(records),
            "unique_byte_contents": len(content_groups),
            "duplicate_path_instances": len(records) - len(content_groups),
            "duplicate_content_groups": len(duplicate_groups),
            "release_recursive_tex_files": len(release_graph),
            "release_tex_edges": len(release_edges),
        },
        "release_tex_edges": sorted(
            release_edges, key=lambda item: (item["from"], item["to"])
        ),
        "duplicate_content_groups": duplicate_groups,
        "files": records,
    }
    OUTPUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
