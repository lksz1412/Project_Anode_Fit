#!/usr/bin/env python3
"""Validate Phase 059 Step 35.3 artifact genealogy evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex"
    / "work"
    / "v1014_v1018_2_phase059"
    / "audit_phase059_artifact_genealogy.py"
)
DATA = ROOT / "Codex" / "results" / "PHASE_059_ARTIFACT_GENEALOGY.json"
REPORT = (
    ROOT
    / "Codex"
    / "results"
    / "PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    summary = data["summary"]
    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("sources_unchanged", data["sources_unchanged"]),
        ("artifact_occurrences_48", summary["artifact_occurrence_count"] == 48),
        (
            "artifact_unique_content_30",
            summary["artifact_unique_content_count"] == 30,
        ),
        ("pdf_occurrences_18", summary["pdf_occurrence_count"] == 18),
        (
            "pdf_unique_byte_content_18",
            summary["pdf_unique_byte_content_count"] == 18,
        ),
        (
            "pdf_unique_rendered_content_17",
            summary["pdf_unique_rendered_content_count"] == 17,
        ),
        (
            "pdf_dependency_blocked_18",
            summary["pdf_rerender_dependency_blocked_count"] == 18,
        ),
        (
            "pdf_preflight_dependency_block",
            data["pdf_rerender_preflight"]["status"]
            == "DEPENDENCY_BLOCKED_MISSING_KOTEX_AND_D2CODING",
        ),
        (
            "pdf_missing_kotex_marker",
            data["pdf_rerender_preflight"]["missing_kotex_marker"],
        ),
        (
            "pdf_no_false_bit_exact",
            summary["pdf_rerender_bit_exact_count"] == 0,
        ),
        ("image_occurrences_24", summary["image_occurrence_count"] == 24),
        (
            "image_unique_content_10",
            summary["image_unique_content_count"] == 10,
        ),
        (
            "image_copy_forward_14",
            summary["image_copy_forward_occurrence_count"] == 14,
        ),
        (
            "image_all_regenerated",
            summary["image_regeneration_bit_exact_count"]
            + summary["image_regeneration_non_bit_exact_count"]
            == 24,
        ),
        (
            "image_zero_bit_exact",
            summary["image_regeneration_bit_exact_count"] == 0,
        ),
        (
            "image_filename_mismatches_nonzero",
            summary["image_filename_version_mismatch_count"] > 0,
        ),
        (
            "all_image_artifacts_exist",
            all(
                (ROOT / record["path"]).is_file()
                for record in data["image_occurrences"]
            ),
        ),
        (
            "all_image_sources_exist",
            all(
                (ROOT / record[key]["path"]).is_file()
                for record in data["image_occurrences"]
                for key in (
                    "current_version_generator",
                    "current_version_model",
                )
            ),
        ),
        ("golden_occurrences_6", summary["golden_occurrence_count"] == 6),
        (
            "golden_unique_content_2",
            summary["golden_unique_content_count"] == 2,
        ),
        (
            "golden_copy_forward_4",
            summary["golden_copy_forward_occurrence_count"] == 4,
        ),
        (
            "golden_all_versions_1_of_13_exact",
            summary["golden_versions_array_exact_1_of_13_count"] == 6,
        ),
        (
            "golden_all_versions_13_of_13_tolerant",
            summary["golden_versions_tolerance_13_of_13_count"] == 6,
        ),
        (
            "golden_no_file_bit_exact_claim",
            all(
                record["current_regeneration"]["file_bit_exact"] is False
                for record in data["golden_occurrences"]
            ),
        ),
        (
            "all_commit_ids_full",
            all(
                len(record["last_commit"]["commit"]) == 40
                and len(record["first_added_commit"]["commit"]) == 40
                for family in (
                    "pdf_occurrences",
                    "image_occurrences",
                    "golden_occurrences",
                )
                for record in data[family]
            ),
        ),
        (
            "v1016_appendix_stale_label",
            any(
                record["path"]
                == "Claude/docs/v1.0.16/appendix_phase_separation.pdf"
                and record["visible_version_label_disposition"].startswith(
                    "STALE_"
                )
                for record in data["pdf_occurrences"]
            ),
        ),
        (
            "authority_boundary",
            "no physics" in data["authority_boundary"],
        ),
        (
            "conditional_status",
            data["status"].startswith("CONDITIONAL_P059_"),
        ),
        ("report_exists", REPORT.is_file()),
        (
            "report_boundaries",
            all(
                marker in REPORT.read_text(encoding="utf-8")
                for marker in (
                    "UNTESTED_DEPENDENCY_BLOCKED",
                    "0/24",
                    "1/13",
                    "13/13",
                    "실험 타당성을 제공하지 않는다",
                )
            ),
        ),
        (
            "next_step_36_1",
            "Step 36.1" in data["next_action"],
        ),
    ]

    before_data = digest(DATA)
    before_report = digest(REPORT)
    completed = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    checks.extend(
        [
            ("auditor_rerun_exit_zero", completed.returncode == 0),
            ("deterministic_data", digest(DATA) == before_data),
            ("deterministic_report", digest(REPORT) == before_report),
        ]
    )

    for index, (name, passed) in enumerate(checks, 1):
        print(f"{index:02d} {'PASS' if passed else 'FAIL'} {name}")
    passed_count = sum(passed for _, passed in checks)
    print(f"SUMMARY {passed_count}/{len(checks)} PASS")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
