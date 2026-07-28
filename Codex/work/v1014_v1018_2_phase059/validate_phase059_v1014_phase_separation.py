#!/usr/bin/env python3
"""Validate Phase 059 Step 36.2 phase-separation rederivation."""

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
    "audit_phase059_v1014_phase_separation.py"
)
DATA = (
    ROOT / "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json"
)
REPORT = (
    ROOT / "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 1.0e-8) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    summary = data["summary"]
    numeric = data["numerical_rederivation"]["regular_solution"]
    ch = data["numerical_rederivation"][
        "cahn_hilliard_factor_two_convention"
    ]
    source = data["source_contracts"]
    dispositions = {item["topic"]: item["disposition"] for item in data["findings"]}
    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("source_unchanged", data["source_unchanged"]),
        ("source_lines_492", source["line_count"] == 492),
        ("equation_labels_9", len(source["equation_label_lines"]) == 9),
        ("binodal_minus", close(numeric["binodal_minus"], 0.07072018)),
        ("binodal_plus", close(numeric["binodal_plus"], 0.92927982)),
        ("spinodal_minus", close(numeric["spinodal_minus"], 0.211324865)),
        ("spinodal_plus", close(numeric["spinodal_plus"], 0.788675135)),
        ("binodal_energy", close(numeric["binodal_f_over_RT"], -0.05834135)),
        ("binodal_derivative_minus_zero", abs(numeric["binodal_derivative_minus"]) < 1e-12),
        ("binodal_derivative_plus_zero", abs(numeric["binodal_derivative_plus"]) < 1e-12),
        ("common_tangent_slope_zero", abs(numeric["common_tangent_chord_slope"]) < 1e-12),
        ("maxwell_area_zero", abs(numeric["maxwell_equal_area_residual"]) < 1e-12),
        ("binodal_outside_spinodal", numeric["binodal_outside_spinodal"]),
        ("critical_curvature_negative_for_ratio3", close(numeric["critical_curvature_fpp_over_RT_at_half"], -2.0)),
        ("ch_k_relation", ch["maximum_equals_critical_over_sqrt2"]),
        ("ch_growth_zero_mode", close(ch["growth_at_zero"], 0.0)),
        ("ch_growth_unstable_band", ch["growth_at_half_critical"] > 0),
        ("ch_growth_maximum", close(ch["growth_at_maximum"], ch["maximum_growth_closed_form"])),
        ("ch_growth_critical_zero", abs(ch["growth_at_critical"]) < 1e-12),
        ("ch_growth_above_negative", ch["growth_above_critical"] < 0),
        ("molar_f_detected", source["molar_f_definition_present"]),
        ("molar_volume_mismatch_detected", source["molar_f_integrated_over_volume_without_conversion"]),
        ("factor_two_source_consistent", source["gradient_term_without_half"] and source["factor_two_chemical_potential"] and source["factor_two_growth_rate"]),
        ("kappa_units_absent", source["explicit_kappa_unit_count"] == 0),
        ("mobility_units_absent", source["explicit_mobility_unit_count"] == 0),
        ("no_flux_boundary_absent", source["explicit_no_flux_boundary_count"] == 0),
        ("composition_boundary_absent", source["explicit_composition_boundary_count"] == 0),
        ("elasticity_absent", source["elastic_energy_term_present"] is False),
        ("primary_sources_2", summary["primary_source_count"] == 2),
        ("primary_dois", {item["doi"] for item in data["primary_source_checks"]} == {"10.1063/1.1744102", "10.1016/0001-6160(61)90182-1"}),
        ("findings_10", summary["finding_count"] == 10),
        ("gradient_units_fail", dispositions["gradient_functional_units"] == "FAIL_DIMENSIONAL_CLOSURE"),
        ("boundary_fail", dispositions["boundary_conditions"] == "FAIL_MISSING"),
        ("elastic_scope_correct", dispositions["chemical_spinodal_scope"] == "CORRECT_MAJOR_SCOPE_BOUNDARY"),
        ("linear_stability_conditional_preserve", dispositions["linear_stability"] == "PRESERVE_AFTER_DIMENSIONAL_REPAIR"),
        ("closure_flags_false", not summary["dimensional_closure_pass"] and not summary["boundary_condition_closure_pass"] and not summary["elasticity_scope_closure_pass"]),
        ("canonical_definitions_6", len(data["canonical_repair_contract"]["definitions"]) == 6),
        ("canonical_boundaries_2", len(data["canonical_repair_contract"]["natural_boundary_conditions"]) == 2),
        ("conditional_status", data["status"].startswith("CONDITIONAL_P059_")),
        ("report_exists", REPORT.is_file()),
        (
            "report_core_markers",
            all(
                marker in REPORT.read_text(encoding="utf-8")
                for marker in (
                    "0.0707202",
                    "stress-free chemical spinodal",
                    "Step 36.3",
                )
            ),
        ),
        ("next_step_36_3", "Step 36.3" in data["next_action"]),
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
