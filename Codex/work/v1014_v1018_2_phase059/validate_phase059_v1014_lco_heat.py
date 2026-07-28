#!/usr/bin/env python3
"""Validate Phase 059 Step 36.3 LCO/heat independent audit."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex/work/v1014_v1018_2_phase059/"
    "audit_phase059_v1014_lco_heat.py"
)
DATA = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 1.0e-9) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    source = data["source_contracts"]
    summary = data["summary"]
    numeric = data["numerical_rederivation"]
    reference = numeric["potential_reference_rederivation"]
    gate = numeric["sommerfeld_gate_rederivation"]
    temp = numeric["theory_code_temperature_contract"]
    transitions = numeric["transition_map"]
    dispositions = {
        item["topic"]: item["disposition"] for item in data["findings"]
    }
    report = REPORT.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_lines",
            source["line_counts"]
            == {
                "chapter_1": 3445,
                "chapter_2": 794,
                "production_code": 904,
            },
        ),
        (
            "primary_sources_7",
            summary["primary_source_count"] == 7,
        ),
        (
            "primary_dois",
            {item["doi"] for item in data["primary_source_checks"]}
            == {
                "10.1039/C8CP06638H",
                "10.1103/PhysRevB.80.165114",
                "10.1039/A900016J",
                "10.1103/PhysRevB.70.174304",
                "10.1149/1.2113792",
                "10.1016/j.jmps.2024.105726",
                "10.1002/smll.202311578",
            },
        ),
        (
            "intrinsic_entropy_80",
            close(
                reference["manuscript_intrinsic_entropy_J_per_mol_K"],
                80.083,
                0.002,
            ),
        ),
        (
            "half_cell_entropy_minus24",
            close(
                reference["measured_half_cell_entropy_J_per_mol_K"],
                -24.1213,
                0.002,
            ),
        ),
        ("entropy_sign_reversal", reference["entropy_sign_reversal"]),
        (
            "intrinsic_difference_minus0p20mV",
            close(reference["intrinsic_difference_V_per_K"], -0.20e-3),
        ),
        (
            "endpoint_entropy_1p1kB",
            close(gate["endpoint_electronic_entropy_kB"], 1.0988, 0.0002),
        ),
        (
            "gate_center_minus45p7",
            close(
                gate["gate_center_dS_code_J_per_mol_K"],
                -45.7,
                0.1,
            ),
        ),
        (
            "gate_code_closed_form",
            close(
                gate["gate_center_dS_code_J_per_mol_K"],
                gate["gate_center_dS_closed_form_J_per_mol_K"],
                0.003,
            ),
        ),
        (
            "gate_x1_residual",
            0.04 < gate["x_1_residual_fraction"] < 0.05,
        ),
        ("gate_inverse_width", gate["gate_peak_scales_as_inverse_dx"]),
        ("gate_area_endpoint", gate["gate_area_tracks_endpoint_difference"]),
        (
            "code_entropy_frozen",
            temp["code_effective_entropy_temperature_invariant"],
        ),
        (
            "code_zero_curvature",
            abs(temp["code_center_second_difference_V"]) < 1.0e-14,
        ),
        (
            "theory_nonzero_curvature",
            abs(temp["theory_expected_symmetric_second_difference_V"])
            > 1.0e-3,
        ),
        (
            "t_squared_not_implemented",
            temp["theory_T_squared_curvature_implemented"] is False,
        ),
        (
            "theory_transition_centers",
            transitions["theory_centers_V"] == [3.9, 4.05, 4.17],
        ),
        (
            "code_transition_count_3",
            len(transitions["code_centers_V_at_298p15K"]) == 3,
        ),
        (
            "transition_map_mismatch",
            transitions["theory_code_centers_match"] is False,
        ),
        (
            "no_code_center_above_4p15",
            transitions["code_center_above_4p15V_count"] == 0,
        ),
        (
            "no_doped_high_voltage_profile",
            transitions["doped_high_voltage_profile_present"] is False,
        ),
        (
            "theory_t4_optional",
            source["theory_high_voltage_t4_present"]
            and source["theory_high_voltage_t4_scope"]
            == "OPTIONAL_OUT_OF_SCOPE",
        ),
        ("no_code_doping_parameter", not source["code_has_doping_parameter"]),
        ("no_code_lco_omega", not source["code_has_lco_omega"]),
        (
            "no_composition_resolved_gate",
            not source["code_has_composition_resolved_electronic_gate"],
        ),
        (
            "no_code_t_squared_center",
            not source["code_has_t_squared_lco_center"],
        ),
        (
            "heat_current_not_linked_to_curve_direction",
            not source["heat_current_linked_to_curve_direction"],
        ),
        ("findings_16", summary["finding_count"] == 16),
        ("preserve_5", summary["preserve_family_count"] == 5),
        ("correct_4", summary["correct_family_count"] == 4),
        ("reject_4", summary["reject_family_count"] == 4),
        ("fail_2", summary["fail_family_count"] == 2),
        ("empirical_1", summary["empirical_only_count"] == 1),
        (
            "reference_rejected",
            dispositions["lco_temperature_coefficient_anchor"]
            == "REJECT_REFERENCE_CONFLATION_AND_SIGN",
        ),
        (
            "gate_empirical",
            dispositions["mit_logistic_gate"] == "EMPIRICAL_ONLY",
        ),
        (
            "two_phase_corrected",
            dispositions["mit_two_phase_thermodynamics"]
            == "CORRECT_TO_COEXISTENCE_AND_LEVER_RULE",
        ),
        (
            "theory_code_fail",
            dispositions["composition_mapping"]
            == "FAIL_THEORY_CODE_CONFORMANCE",
        ),
        (
            "doping_rejected",
            dispositions["doping_mechanism"]
            == "REJECT_SCALAR_OMEGA_ONLY_GENERALIZATION",
        ),
        (
            "high_voltage_fail",
            dispositions["doped_high_voltage_coverage"]
            == "FAIL_SCOPE_ABSENT",
        ),
        (
            "citation_corrected",
            dispositions["ml2024_citation_support"]
            == "CORRECT_CITATION_AND_REJECT_CLAIM_SUPPORT",
        ),
        (
            "closure_flags",
            summary["heat_identity_algebra_pass"]
            and not summary["half_cell_reference_closure_pass"]
            and not summary["electronic_gate_external_validation_pass"]
            and not summary["theory_code_electronic_conformance_pass"]
            and not summary["doped_high_voltage_coverage_pass"],
        ),
        (
            "repair_contract_sections",
            set(data["canonical_repair_contract"])
            == {
                "potential_and_heat",
                "electronic_entropy",
                "doping_and_high_voltage",
                "theory_to_code",
            },
        ),
        (
            "conditional_status",
            data["status"].startswith("CONDITIONAL_P059_"),
        ),
        ("report_exists", REPORT.is_file()),
        (
            "report_core_markers",
            all(
                marker in report
                for marker in (
                    "-0.25 mV/K",
                    "-46",
                    "105726",
                    "lever",
                    "Step 36.4",
                )
            ),
        ),
        ("next_step_36_4", "Step 36.4" in data["next_action"]),
    ]
    before_data = digest(DATA)
    before_report = digest(REPORT)
    completed = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
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
    passed = sum(value for _, value in checks)
    print(f"SUMMARY {passed}/{len(checks)} PASS")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
