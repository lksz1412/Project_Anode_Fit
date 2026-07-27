#!/usr/bin/env python3
"""Validate the Phase 058 theory-code-test-artifact matrix."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_MATRIX.json"


def load(name: str) -> dict:
    return json.loads((ROOT / f"Codex/results/{name}").read_text(encoding="utf-8"))


def main() -> int:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    theory = load("PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json")
    code = load("PHASE_058_CODE_BEHAVIOR_MATRIX.json")
    test_demo = load("PHASE_058_TEST_DEMO_CLAIM_MATRIX.json")
    execution = load("PHASE_058_LEGACY_ISOLATED_EXECUTION.json")
    probes = load("PHASE_058_INDEPENDENT_PROBES.json")
    golden = load("PHASE_058_GOLDEN_NPZ_AUDIT.json")
    pdf_metrics = load("PHASE_058_PDF_RENDER_METRICS.json")
    pdf_review = load("PHASE_058_PDF_VISUAL_REVIEW.json")
    image_audit = load("PHASE_058_STANDALONE_IMAGE_AUDIT.json")
    genealogy = load("PHASE_058_ARTIFACT_GENEALOGY.json")
    closure = load("PHASE_058_V1013_CLOSURE_AUDIT.json")
    rows = data["rows"]
    checks: dict[str, bool] = {}

    checks["row_count"] = len(rows) == 26
    checks["row_ids_unique"] = len({row["id"] for row in rows}) == len(rows)
    checks["row_ids_complete"] = [row["id"] for row in rows] == [
        f"F4-{number:02d}" for number in range(1, 27)
    ]
    checks["topics_unique"] = len({row["topic"] for row in rows}) == len(rows)

    vocabulary = data["axis_status_vocabulary"]
    for axis in ("theory", "code", "test", "artifact", "overall"):
        checks[f"vocabulary_{axis}"] = all(
            row[axis] in vocabulary[axis] for row in rows
        )
    allowed_decisions = {
        "PRESERVE",
        "CORRECT",
        "SUPERSEDE",
        "EMPIRICAL_ONLY",
        "THEORY_ONLY",
        "REJECT",
        "UNVERIFIED",
    }
    checks["carry_decisions"] = all(
        row["carry_decision"] in allowed_decisions for row in rows
    )
    checks["pass_boundaries_nonempty"] = all(
        bool(row["pass_does_not_mean"].strip()) for row in rows
    )
    checks["overall_counts"] = (
        dict(sorted(Counter(row["overall"] for row in rows).items()))
        == data["overall_counts"]
    )

    evidence = data["evidence_summary"]
    actual = {
        "theory_source_count": theory["document_count"],
        "theory_equation_occurrence_count": theory["equation_environment_count"],
        "production_code_blob_count": code["document_count"],
        "production_code_line_count": code["total_lines"],
        "test_and_demo_document_count": test_demo["document_count"],
        "python_assert_count": sum(
            document.get("assert_statement_count", 0)
            for document in test_demo["documents"]
        ),
        "legacy_execution_case_count": execution["case_count"],
        "legacy_report_only_success_count": execution["classification_counts"][
            "EXECUTED_REPORT_ONLY"
        ],
        "golden_array_count": golden["array_count"],
        "golden_bit_exact_count": golden["summary"]["bit_exact_count"],
        "golden_allclose_1e12_count": golden["summary"]["allclose_1e12_count"],
        "pdf_count": pdf_metrics["pdf_count"],
        "pdf_page_count": pdf_metrics["total_pdf_pages"],
        "pdf_confirmed_clipping_defect_count": pdf_review["summary"][
            "confirmed_clipping_defects"
        ],
        "standalone_image_count": image_audit["scope"]["image_paths"],
        "stale_image_count": genealogy["summary"]["stale_provenance_count"],
        "public_experimental_dataset_count": closure[
            "v1013_directory_evidence"
        ]["public_experimental_dataset_count"],
    }
    for key, value in actual.items():
        checks[f"evidence_{key}"] = value == evidence[key]

    summary = probes["cross_version_summary"]
    critical = {row["id"]: row for row in rows}
    checks["f4_01_misaligned"] = critical["F4-01"]["overall"] == "MISALIGNED"
    checks["f4_03_aligned"] = critical["F4-03"]["overall"] == "ALIGNED"
    checks["f4_11_partial"] = critical["F4-11"]["overall"] == "PARTIAL"
    checks["f4_12_misaligned"] = critical["F4-12"]["overall"] == "MISALIGNED"
    checks["f4_14_aligned"] = critical["F4-14"]["overall"] == "ALIGNED"
    checks["f4_20_absent"] = critical["F4-20"]["overall"] == "ABSENT"
    checks["f4_25_absent"] = critical["F4-25"]["overall"] == "ABSENT"
    checks["f4_26_misaligned"] = critical["F4-26"]["overall"] == "MISALIGNED"
    checks["direct_lv_probe"] = summary["direct_LV_I0_equals_I1"] is True
    checks["lco_direction_v1013"] = (
        summary["lco_charge_maps_to_delithiation_plus"]["v1.0.13"] is True
    )
    checks["default_lco_rate_invariant"] = (
        summary["lco_default_rate_invariant_Rn0"] is True
    )
    checks["source_integrity_execution"] = execution["validation"][
        "sources_unchanged"
    ]
    checks["source_integrity_probe"] = probes["sources_unchanged"]
    checks["source_integrity_pdf"] = pdf_metrics["sources_unchanged"]

    expected_verdict = (
        "NO_SINGLE_AXIS_PASS_IS_A_PHYSICAL_CLOSURE;_SIX_TOPICS_ALIGN_"
        "INTERNALLY_BUT_NONE_ESTABLISHES_MATERIAL_EXTERNAL_VALIDITY"
    )
    checks["verdict"] = data["verdict"] == expected_verdict

    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "check_count": len(checks),
        "failures": failures,
        "gate": (
            "PASS_P058_FOUR_AXIS_CONFORMANCE"
            if not failures
            else "FAIL_P058_FOUR_AXIS_CONFORMANCE"
        ),
        "row_count": len(rows),
        "overall_counts": data["overall_counts"],
        "verdict": data["verdict"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
