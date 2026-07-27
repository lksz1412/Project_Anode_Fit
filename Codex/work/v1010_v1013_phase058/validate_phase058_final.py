#!/usr/bin/env python3
"""Validate Phase 058 coverage, adjudication, routing, and gate semantics."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
VALIDATION_PATH = RESULTS / "PHASE_058_VALIDATION.json"
REPORT_PATH = RESULTS / "PHASE_058_V1010_V1013_LINEAGE_REPORT_A.md"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def run_validator(relative_path: str) -> dict:
    result = subprocess.run(
        [sys.executable, relative_path],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "path": relative_path,
        "returncode": result.returncode,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "stderr": result.stderr.strip(),
    }


def main() -> int:
    validation = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
    queue = load("PHASE_058_V1010_V1013_AUDIT_QUEUE.json")
    coverage = load("PHASE_058_V1010_V1013_TEXT_COVERAGE.json")
    theory = load("PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json")
    theory_diff = load("PHASE_058_THEORY_LINEAGE_DIFF.json")
    code = load("PHASE_058_CODE_BEHAVIOR_MATRIX.json")
    tests = load("PHASE_058_TEST_DEMO_CLAIM_MATRIX.json")
    pdf_metrics = load("PHASE_058_PDF_RENDER_METRICS.json")
    pdf_review = load("PHASE_058_PDF_VISUAL_REVIEW.json")
    images = load("PHASE_058_STANDALONE_IMAGE_AUDIT.json")
    genealogy = load("PHASE_058_ARTIFACT_GENEALOGY.json")
    golden = load("PHASE_058_GOLDEN_NPZ_AUDIT.json")
    legacy = load("PHASE_058_LEGACY_ISOLATED_EXECUTION.json")
    claims = load("PHASE_058_THEORY_CLAIM_DISPOSITIONS.json")
    four_axis = load("PHASE_058_FOUR_AXIS_CONFORMANCE_MATRIX.json")
    routing = load("PHASE_058_CARRY_FORWARD_BLOCKER_REGISTER.json")
    v1013_closure = load("PHASE_058_V1013_CLOSURE_AUDIT.json")

    checks: dict[str, bool] = {}
    counts = validation["scope_counts"]
    adjudication = validation["adjudication_counts"]
    dispositions = validation["artifact_dispositions"]

    checks["gate"] = validation["gate"] == "PASS_P058_LINEAGE_A"
    checks["gate_semantics"] = validation["gate_semantics"] == (
        "AUDIT_COVERAGE_AND_ADJUDICATION_COMPLETE;_NOT_A_CANONICAL_MODEL_OR_EXTERNAL_PHYSICAL_VALIDITY_PASS"
    )
    checks["queue_counts"] = (
        queue["path_count"],
        queue["unique_blob_count"],
        queue["text_blob_count"],
        queue["text_line_count"],
    ) == (
        counts["version_path_count"],
        counts["unique_blob_count"],
        counts["full_text_blob_count"],
        counts["full_text_line_count"],
    )
    checks["queue_validation"] = all(queue["validation"].values())
    checks["queue_current_blobs_unchanged"] = all(
        all(
            (ROOT / occurrence).is_file()
            and git_blob_sha(ROOT / occurrence) == record["blob_sha"]
            for occurrence in record["occurrence_paths"]
        )
        for record in queue["records"]
    )
    checks["text_coverage"] = (
        coverage["document_count"] == counts["full_text_blob_count"]
        and coverage["total_lines"] == counts["full_text_line_count"]
        and coverage["completed_lines"] == counts["full_text_line_count"]
        and coverage["status_counts"]
        == {"COMPLETE": counts["full_text_blob_count"], "UNREAD": 0}
    )
    checks["theory_exact_diff"] = (
        theory_diff["status"] == "PASS_P058_THEORY_EXACT_DIFF"
    )
    checks["theory_coverage"] = (
        theory["document_count"] == counts["theory_blob_count"]
        and theory["total_lines"] == counts["theory_line_count"]
        and theory["equation_environment_count"]
        == adjudication["theory_equation_occurrence_count"]
    )
    checks["code_coverage"] = (
        code["document_count"] == counts["production_code_blob_count"]
        and code["total_lines"] == counts["production_code_line_count"]
    )
    role_counts = {}
    for record in queue["records"]:
        role_counts[record["role"]] = role_counts.get(record["role"], 0) + 1
    checks["test_demo_coverage"] = (
        role_counts["test"] == counts["test_blob_count"]
        and role_counts["demo"] == counts["demo_blob_count"]
        and tests["document_count"]
        == counts["test_blob_count"] + counts["demo_blob_count"]
    )
    checks["pdf_coverage"] = (
        pdf_metrics["pdf_count"] == counts["pdf_count"]
        and pdf_metrics["total_pdf_pages"] == counts["pdf_page_count"]
        and pdf_metrics["total_rendered_pages"] == counts["pdf_page_count"]
        and pdf_review["summary"]["pdfs_reviewed"] == counts["pdf_count"]
        and pdf_review["summary"]["pages_reviewed"] == counts["pdf_page_count"]
        and pdf_review["summary"]["visual_review_complete"]
    )
    checks["image_coverage"] = (
        len(images["images"]) == counts["image_count"]
        and all(images["machine_checks"].values())
        and genealogy["scope"]["images"] == counts["image_count"]
        and genealogy["validation"]["all_artifacts_disposed"]
    )
    checks["golden_coverage"] = (
        golden["array_count"] == counts["golden_array_count"]
        and golden["summary"]["bit_exact_count"]
        == dispositions["golden_bit_exact_count"]
        and golden["summary"]["allclose_1e12_count"]
        == dispositions["golden_allclose_1e12_count"]
        and all(golden["validation"].values())
    )
    checks["legacy_execution_disposed"] = (
        legacy["case_count"] == dispositions["legacy_execution_case_count"]
        and legacy["classification_counts"]["EXECUTED_REPORT_ONLY"]
        == dispositions["legacy_report_only_count"]
        and legacy["classification_counts"]["BLOCKED_MISSING_FROZEN_GOLDEN"]
        == dispositions["legacy_blocked_missing_frozen_golden_count"]
        and legacy["classification_counts"]["FAIL_BIT_EXACT_GOLDEN_FLOAT_DRIFT"]
        == dispositions["legacy_bit_exact_failure_count"]
        and all(legacy["validation"].values())
    )
    checks["theory_claim_disposition"] = (
        claims["coverage"]["equation_occurrence_count"]
        == adjudication["theory_equation_occurrence_count"]
        and claims["coverage"]["assigned_equation_occurrence_count"]
        == adjudication["theory_equation_assigned_count"]
        and claims["coverage"]["unassigned_equation_occurrence_count"] == 0
    )
    checks["four_axis_counts"] = (
        len(four_axis["rows"]) == adjudication["four_axis_row_count"]
        and four_axis["overall_counts"]["ALIGNED"]
        == adjudication["four_axis_aligned_count"]
        and four_axis["overall_counts"]["PARTIAL"]
        == adjudication["four_axis_partial_count"]
        and four_axis["overall_counts"]["MISALIGNED"]
        == adjudication["four_axis_misaligned_count"]
        and four_axis["overall_counts"]["ABSENT"]
        == adjudication["four_axis_absent_count"]
        and four_axis["overall_counts"]["UNVERIFIED"]
        == adjudication["four_axis_unverified_count"]
    )
    checks["routing_counts"] = (
        routing["counts"]["carry_forward_asset_count"]
        == adjudication["carry_forward_asset_count"]
        and routing["counts"]["repair_blocker_count"]
        == adjudication["repair_blocker_count"]
        and routing["counts"]["new_scope_blocker_count"]
        == adjudication["new_scope_blocker_count"]
        and routing["counts"]["evidence_debt_count"]
        == adjudication["evidence_debt_count"]
        and routing["counts"]["total_register_item_count"]
        == adjudication["register_item_count"]
        and routing["counts"]["four_axis_route_count"]
        == adjudication["four_axis_row_count"]
    )
    checks["artifact_defects_not_hidden"] = (
        pdf_review["summary"]["confirmed_clipping_defects"]
        == dispositions["confirmed_pdf_clipping_count"]
        and genealogy["summary"]["stale_provenance_count"]
        == dispositions["stale_image_provenance_count"]
    )
    directory_evidence = v1013_closure["v1013_directory_evidence"]
    checks["missing_scientific_scope_not_hidden"] = all(
        (
            directory_evidence["public_experimental_dataset_count"]
            == dispositions["public_experimental_dataset_count"],
            directory_evidence["fit_result_count"]
            == dispositions["fit_result_count"],
            directory_evidence["optimizer_state_count"]
            == dispositions["optimizer_state_count"],
            directory_evidence["silicon_theory_or_code_path_count"]
            == dispositions["silicon_theory_or_code_path_count"],
        )
    )
    checks["scientific_pass_exclusions"] = all(
        (
            validation["scientific_disposition"]["canonical_version_selected"]
            is False,
            validation["scientific_disposition"][
                "external_material_validity_established"
            ]
            is False,
            validation["scientific_disposition"]["public_data_fit_established"]
            is False,
            validation["scientific_disposition"][
                "doped_high_voltage_lco_closure_established"
            ]
            is False,
            validation["scientific_disposition"][
                "silicon_or_composite_closure_established"
            ]
            is False,
        )
    )
    checks["all_declared_gate_requirements_true"] = all(
        validation["gate_requirements"].values()
    )
    checks["required_subgate_manifest"] = (
        len(validation["required_subgates"]) == 15
        and len(set(validation["required_subgates"])) == 15
        and all(
            gate.startswith("PASS_P058_")
            for gate in validation["required_subgates"]
        )
    )

    report = REPORT_PATH.read_text(encoding="utf-8")
    checks["report_semantics"] = all(
        phrase in report
        for phrase in (
            "`PASS_P058_LINEAGE_A`",
            "이 PASS는 어느",
            "정본으로 승격",
            "external material validity",
            "공개 experimental dataset 0",
            "theory-only 본문 원칙",
            "v1.0.14–v1.0.18.2",
        )
    )

    validator_paths = [
        "Codex/work/v1010_v1013_phase058/validate_phase058_carry_forward.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_four_axis_matrix.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_prior_report_adjudication.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_r1_consistency.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_theory_claim_dispositions.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1010_coordinates.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1010_heat_lco.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1010_kinetics.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1011_copy_lineage.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1012_patch.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1013_closure.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1013_patch.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1013_statmech.py",
        "Codex/work/v1010_v1013_phase058/validate_phase058_v1013_width_semantics.py",
    ]
    subordinate = [run_validator(path) for path in validator_paths]
    checks["all_subordinate_validators_pass"] = all(
        item["returncode"] == 0 and not item["stderr"] for item in subordinate
    )

    claude_status = subprocess.run(
        ["git", "status", "--short", "--", "Claude"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    checks["original_claude_tree_unchanged"] = not claude_status

    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "artifact": str(VALIDATION_PATH.relative_to(ROOT)),
        "report": str(REPORT_PATH.relative_to(ROOT)),
        "check_count": len(checks),
        "failures": failures,
        "subordinate_validator_count": len(subordinate),
        "subordinate_validators": subordinate,
        "gate": "PASS_P058_LINEAGE_A" if not failures else "FAIL_P058",
        "gate_semantics": validation["gate_semantics"],
        "verdict": validation["verdict"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
