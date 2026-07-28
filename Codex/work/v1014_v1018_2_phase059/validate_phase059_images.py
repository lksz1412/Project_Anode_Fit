#!/usr/bin/env python3
"""Validate Phase 059 standalone-image audit evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = ROOT / "Codex/work/v1014_v1018_2_phase059/audit_phase059_images.py"
OUTPUT = ROOT / "Codex/results/PHASE_059_IMAGE_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_STANDALONE_IMAGE_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    before_output = sha256(OUTPUT)
    before_report = sha256(REPORT)
    completed = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    check("auditor_exit_zero", completed.returncode == 0)
    check("schema", payload["schema_version"] == 1)
    check("unique_images_10", payload["unique_image_count"] == 10)
    check(
        "path_occurrences_24",
        payload["image_path_occurrence_count"] == 24,
    )
    check(
        "visually_inspected_10",
        payload["visually_inspected_unique_image_count"] == 10,
    )
    check(
        "family_counts",
        payload["image_family_counts"]
        == {
            "DQDV_BELL_SHAPES": 1,
            "GRAPH_SUITE": 3,
            "P4_LCO_HEAT": 2,
            "SAMPLE_TEST": 4,
        },
    )
    check("decode_failures_zero", payload["summary"]["decode_failure_count"] == 0)
    check(
        "queue_blob_mismatches_zero",
        payload["summary"]["queue_blob_mismatch_count"] == 0,
    )
    check(
        "occurrence_blob_mismatches_zero",
        payload["summary"]["occurrence_blob_mismatch_count"] == 0,
    )
    check(
        "generators_present",
        payload["summary"]["generator_missing_count"] == 0,
    )
    check(
        "generator_output_names_present",
        payload["summary"]["generator_output_name_missing_count"] == 0,
    )
    check(
        "visual_defect_image_count_3",
        payload["summary"]["unique_visual_defect_image_count"] == 3,
    )
    check(
        "right_edge_content_images_2",
        payload["summary"]["right_edge_content_image_count"] == 2,
    )
    check(
        "no_experimental_observation_images",
        payload["summary"]["experimental_observation_image_count"] == 0,
    )
    check("all_paths_exist", all(
        (ROOT / occurrence["path"]).exists()
        for image in payload["images"]
        for occurrence in image["occurrences"]
    ))
    check("all_generators_exist", all(
        (ROOT / image["generator"]["path"]).exists()
        for image in payload["images"]
    ))
    check("all_inspection_status", all(
        image["visual_review"]["inspection_status"]
        == "ORIGINAL_RESOLUTION_VISUALLY_INSPECTED"
        for image in payload["images"]
    ))
    check("all_synthetic_evidence", all(
        image["evidence_class"] == "SYNTHETIC_MODEL_OUTPUT"
        for image in payload["images"]
    ))
    check(
        "p4_two_unique_defects",
        sum(
            image["visual_review"]["visual_defects"]
            == ["RIGHT_CLIPPED_PANEL_C_TITLE"]
            for image in payload["images"]
        )
        == 2,
    )
    check(
        "stale_filename_one_unique",
        sum(
            image["visual_review"]["visual_defects"]
            == ["FILENAME_VERSION_1_0_14_BUT_TITLE_AND_CODE_1_0_16"]
            for image in payload["images"]
        )
        == 1,
    )
    check(
        "finding_ids_exact",
        [finding["id"] for finding in payload["findings"]]
        == [
            "IMG-059-01",
            "IMG-059-02",
            "IMG-059-03",
            "IMG-059-04",
            "IMG-059-05",
            "IMG-059-06",
        ],
    )
    check(
        "scope_absent_finding",
        next(
            finding for finding in payload["findings"]
            if finding["id"] == "IMG-059-05"
        )["status"]
        == "SCOPE_ABSENT",
    )
    check(
        "status_conditional",
        payload["status"] == "CONDITIONAL_P059_SYNTHETIC_IMAGE_EVIDENCE",
    )
    check("report_exists", REPORT.exists())
    report = REPORT.read_text(encoding="utf-8")
    check("report_claim_boundary", "synthetic model output" in report)
    check("report_next_step", "Step 35.3" in report)
    check("deterministic_output", sha256(OUTPUT) == before_output)
    check("deterministic_report", sha256(REPORT) == before_report)

    failures = [name for name, passed in checks if not passed]
    for index, (name, passed) in enumerate(checks, start=1):
        print(f"{index:02d} {'PASS' if passed else 'FAIL'} {name}")
    print(f"SUMMARY {len(checks) - len(failures)}/{len(checks)} PASS")
    if failures:
        if completed.stderr:
            print(completed.stderr)
        raise SystemExit("failed checks: " + ", ".join(failures))


if __name__ == "__main__":
    main()
