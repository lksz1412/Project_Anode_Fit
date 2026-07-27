#!/usr/bin/env python3
"""Validate the v1.0.10 -> v1.0.11 copy-lineage classification."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "Codex/results/PHASE_058_V1011_COPY_LINEAGE_MATRIX.json"
PDF_REVIEW = ROOT / "Codex/results/PHASE_058_PDF_VISUAL_REVIEW.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def main() -> int:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    pdf_review = json.loads(PDF_REVIEW.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["schema"] = data["schema_version"] == "phase058-v1011-copy-lineage-v1"
    checks["boundary"] = (
        data["audit_boundary"] == "COPY_AND_PROVENANCE_AUDIT_NOT_NEW_PHYSICS"
    )

    text_lines = 0
    filename_only = 0
    same_name = 0
    for pair in data["text_pairs"]:
        old = ROOT / pair["v1010"]
        new = ROOT / pair["v1011"]
        pair_id = pair["role"]
        checks[f"text_exists:{pair_id}"] = old.is_file() and new.is_file()
        checks[f"text_equal:{pair_id}"] = old.read_bytes() == new.read_bytes()
        checks[f"text_hash:{pair_id}"] = (
            sha256(old) == pair["sha256"] == sha256(new)
        )
        checks[f"text_lines:{pair_id}"] = (
            line_count(old) == pair["lines"] == line_count(new)
        )
        text_lines += pair["lines"]
        if pair["classification"] == "BYTE_IDENTICAL_FILENAME_ONLY_RELABEL":
            filename_only += 1
        elif pair["classification"] == "BYTE_IDENTICAL_COPY":
            same_name += 1

    checks["text_pair_count"] = (
        len(data["text_pairs"]) == data["summary"]["paired_text_files"]
    )
    checks["text_line_total"] = text_lines == data["summary"]["paired_text_lines"]
    checks["filename_only_count"] = (
        filename_only == data["summary"]["filename_only_relabel_pairs"]
    )
    checks["same_name_count"] = (
        same_name == data["summary"]["same_filename_copy_pairs"]
    )

    comparisons = {
        item["comparison_id"]: item
        for item in pdf_review["pixel_comparisons"]
    }
    comparison_ids = {
        "chapter_1_pdf": "v1010_v1011_ch1",
        "chapter_2_pdf": "v1010_v1011_ch2",
    }
    pdf_pages = 0
    identical_pages = 0
    for pair in data["pdf_pairs"]:
        old = ROOT / pair["v1010"]
        new = ROOT / pair["v1011"]
        pair_id = pair["role"]
        comparison = comparisons[comparison_ids[pair_id]]
        checks[f"pdf_exists:{pair_id}"] = old.is_file() and new.is_file()
        checks[f"pdf_binary_differs:{pair_id}"] = old.read_bytes() != new.read_bytes()
        checks[f"pdf_hash_old:{pair_id}"] = sha256(old) == pair["v1010_sha256"]
        checks[f"pdf_hash_new:{pair_id}"] = sha256(new) == pair["v1011_sha256"]
        checks[f"pdf_pages:{pair_id}"] = comparison["page_count"] == pair["pages"]
        checks[f"pdf_pixels:{pair_id}"] = (
            comparison["pixel_identical_page_count"]
            == pair["pixel_identical_pages"]
            == pair["pages"]
            and comparison["maximum_channel_difference"]
            == pair["maximum_channel_difference"]
            == 0
        )
        pdf_pages += pair["pages"]
        identical_pages += pair["pixel_identical_pages"]

    checks["pdf_pair_count"] = (
        len(data["pdf_pairs"]) == data["summary"]["paired_pdfs"]
    )
    checks["pdf_page_total"] = pdf_pages == data["summary"]["paired_pdf_pages"]
    checks["pdf_identical_page_total"] = (
        identical_pages == data["summary"]["pixel_identical_pdf_pages"]
    )

    for path_string in data["v1010_material_not_copied_to_v1011_docs"]:
        checks[f"v1010_extra_exists:{path_string}"] = (ROOT / path_string).is_file()

    ledger = ROOT / data["v1011_new_record_outside_docs"]["path"]
    ledger_text = ledger.read_text(encoding="utf-8")
    checks["ledger_exists"] = ledger.is_file()
    checks["ledger_only_phase_0p1_complete"] = (
        "| 0.1 |" in ledger_text
        and "| 1.1 |" in ledger_text
        and "Phase 0.1 ✅" in ledger_text
        and "Phase 1.1 착수" in ledger_text
    )

    last_commits = {
        subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", pair["v1011"]],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        for pair in data["text_pairs"] + data["pdf_pairs"]
    }
    checks["single_creation_commit"] = last_commits == {data["creation_commit"]}

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "matrix": str(MATRIX.relative_to(ROOT)),
                "check_count": len(checks),
                "failures": failures,
                "text_pairs": len(data["text_pairs"]),
                "text_lines": text_lines,
                "pdf_pairs": len(data["pdf_pairs"]),
                "pixel_identical_pages": identical_pages,
                "creation_commits": sorted(last_commits),
                "gate": (
                    "PASS_P058_V1011_COPY_LINEAGE"
                    if not failures
                    else "FAIL_P058_V1011_COPY_LINEAGE"
                ),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
