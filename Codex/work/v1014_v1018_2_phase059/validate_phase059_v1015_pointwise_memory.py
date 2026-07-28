#!/usr/bin/env python3
"""Validate Phase 059 Step 37.1 v1.0.15 pointwise-memory audit."""

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
    "audit_phase059_v1015_pointwise_memory.py"
)
DATA = ROOT / "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_REVIEW.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 1.0e-9) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    source = data["source_contracts"]
    lineage = data["lineage_contract"]
    numeric = data["numerical_rederivation"]
    recurrence = numeric["recurrence_identity"]
    small_a = numeric["small_a_branch"]
    wide = numeric["wide_window"]
    finite = numeric["finite_window_initial_condition"]
    sampling = numeric["sampling_dependence"]
    guard = numeric["resolution_guard"]
    mirror = numeric["fixed_direction_mirror"]
    chronology = numeric["chronology"]
    current = numeric["current_limits"]
    overflow = numeric["nonfinite_lag"]
    test_scope = data["test_and_golden_scope"]
    summary = data["summary"]
    dispositions = {
        item["topic"]: item["disposition"] for item in data["findings"]
    }
    report = REPORT.read_text(encoding="utf-8")

    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("phase_step", data["phase"] == 59 and data["step"] == "37.1"),
        (
            "status",
            data["status"]
            == "CONDITIONAL_P059_V1015_POINTWISE_MEMORY_CORE_PRESERVED_BUT_FINITE_WINDOW_RESOLUTION_SWITCH_AND_CHRONOLOGY_FAIL",
        ),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_hashes_equal",
            data["source_hashes_before"] == data["source_hashes_after"],
        ),
        (
            "source_lines",
            source["line_counts"]
            == {
                "v14_production_code": 904,
                "v15_production_code": 895,
                "v15_chapter_1": 3512,
                "v15_regression_test": 85,
            },
        ),
        (
            "theory_lines",
            source["chapter_1_lines"]["finite_initial_general_solution"] == 1985
            and source["chapter_1_lines"]["minus_infinity_boundary"] == 1996
            and source["chapter_1_lines"]["normalized_lag_integral"] == 2021
            and source["chapter_1_lines"]["peak_shape"] == 2064
            and source["chapter_1_lines"]["small_lag_limit"] == 2098
            and source["chapter_1_lines"]["direction_reversal"] == 2141
            and source["chapter_1_lines"]["pointwise_sum"] == 2219,
        ),
        (
            "code_lines",
            source["code_lines"]["decay_cap"] == 75
            and source["code_lines"]["pointwise_recurrence"] == 105
            and source["code_lines"]["small_a_branch"] == 126
            and source["code_lines"]["initial_condition"] == 122
            and source["code_lines"]["voltage_sorting"] == 441
            and source["code_lines"]["resolution_switch"] == 496
            and source["code_lines"]["nonfinite_to_zero"] == 366
            and source["code_lines"]["curve_hour_rate"] == 523,
        ),
        ("func_Lq_carried", lineage["func_L_q_executable_ast_equal"]),
        ("resolver_carried", lineage["lag_resolver_executable_ast_equal"]),
        ("dqdv_changed", not lineage["dqdv_executable_ast_equal"]),
        ("old_lowpass_removed", lineage["v14_lowpass_removed"]),
        ("pointwise_added", lineage["v15_pointwise_added"]),
        ("recurrence_points", recurrence["irregular_point_count"] == 7),
        (
            "constant_recurrence",
            recurrence["constant_source_max_abs_error"] < 1.0e-12,
        ),
        (
            "linear_recurrence",
            recurrence["linear_source_max_abs_error"] < 1.0e-12,
        ),
        ("small_a_rows", len(small_a) == 3),
        (
            "small_a_nonzero_error",
            small_a[0]["release_uses_small_a_formula"]
            and small_a[0]["small_a_formula_abs_error"] > 1.0e-10,
        ),
        (
            "small_a_threshold_exact_branch",
            not small_a[1]["release_uses_small_a_formula"],
        ),
        (
            "wide_equilibrium_area",
            close(wide["equilibrium_area"], 1.0, 1.0e-8),
        ),
        ("wide_lagged_area", close(wide["lagged_area"], 1.0, 1.0e-8)),
        ("wide_peak_suppressed", wide["lagged_peak"] < wide["equilibrium_peak"]),
        (
            "finite_first_point_mismatch",
            finite["first_point_release_peak"] == 0.0
            and finite["first_point_infinite_history_peak"] > 1.8,
        ),
        (
            "finite_window_max_difference",
            finite["standalone_vs_infinite_history_max_abs"] > 1.8,
        ),
        (
            "finite_window_area_bias",
            abs(finite["area_bias_fraction_of_Q"]) > 0.03,
        ),
        (
            "sampling_difference",
            sampling["coarse_vs_dense_at_same_coordinates_max_abs"] > 0.05,
        ),
        (
            "guard_cap",
            guard["decay_cap"] == 40.0
            and close(guard["critical_lag_V"], 0.00025, 1.0e-12),
        ),
        (
            "guard_below_equilibrium",
            guard["below_branch_vs_equilibrium_max_abs"] == 0.0,
        ),
        (
            "guard_jump",
            guard["above_vs_below_max_abs_jump"] > 1.0
            and guard["jump_fraction_of_equilibrium_peak"] > 0.08,
        ),
        (
            "v14_jump",
            close(guard["v14_grid_handoff_jump_fraction"], 0.2292529587316009),
        ),
        ("mirror", mirror["max_abs_error"] < 1.0e-12),
        (
            "chronology_sorted_invariant",
            chronology["sorted_vs_shuffled_then_restored_max_abs"] == 0.0,
        ),
        (
            "chronology_true_order_differs",
            chronology["prior_true_input_order_memory_max_abs"] > 20.0,
        ),
        (
            "direct_I0_bypass",
            current["direct_LV_I0_vs_I1_max_abs"] == 0.0
            and current["direct_LV_I0_vs_equilibrium_max_abs"] > 3.0,
        ),
        (
            "derived_I0_equilibrium",
            current["derived_path_I0_vs_equilibrium_max_abs"] == 0.0,
        ),
        (
            "overflow_reversed",
            overflow["resolved_lag_V"] == 0.0
            and overflow["mapped_to_equilibrium"],
        ),
        ("test_no_ast_assert", test_scope["ast_assert_count"] == 0),
        (
            "test_missing_pointwise",
            not test_scope["mentions_pointwise_memory"],
        ),
        ("test_missing_direct_LV", not test_scope["mentions_direct_LV"]),
        ("test_missing_nonmonotone", not test_scope["mentions_nonmonotone"]),
        ("test_missing_reversal", not test_scope["mentions_reversal"]),
        ("test_missing_pulse", not test_scope["mentions_pulse"]),
        (
            "golden_scope",
            test_scope["golden_rebaseline_changed_array_count"] == 11
            and test_scope["golden_evidence_class"]
            == "DERIVED_MODEL_OUTPUT_SNAPSHOT",
        ),
        ("finding_count", summary["finding_count"] == 16),
        (
            "preserve_kernel",
            dispositions["continuum_memory_derivation"]
            == "PRESERVE_NORMALIZED_CAUSAL_KERNEL",
        ),
        (
            "correct_small_a",
            dispositions["small_a_branch"]
            == "CORRECT_EXACTNESS_CLAIM_TO_ASYMPTOTIC_APPROXIMATION",
        ),
        (
            "require_initial_state",
            dispositions["finite_window_initial_state"]
            == "REQUIRE_EXPLICIT_INITIAL_STATE_OR_PREHISTORY",
        ),
        (
            "reject_guard",
            dispositions["resolution_guard"]
            == "REJECT_CLAIM_OF_CONTINUOUS_NONBRANCH_GUARD",
        ),
        (
            "preserve_improvement",
            dispositions["v14_grid_switch"]
            == "PRESERVE_V15_AS_MATERIAL_IMPROVEMENT_NOT_COMPLETE_FIX",
        ),
        (
            "reject_chronology",
            dispositions["chronology"] == "REJECT_AS_TIME_HISTORY_MODEL",
        ),
        (
            "carry_kinetic_blockers",
            dispositions["inherited_kinetic_closure"]
            == "CARRY_FORWARD_UNIT_LOCAL_AFFINITY_BLOCKERS",
        ),
        (
            "repair_contract",
            dispositions["repair_contract"]
            == "REQUIRE_SIGNED_TIME_STATE_INTEGRATOR",
        ),
        ("summary_kernel", summary["continuum_kernel_pass"]),
        ("summary_recurrence", summary["resolved_linear_segment_recurrence_pass"]),
        ("summary_wide_capacity", summary["wide_window_capacity_pass"]),
        ("summary_mirror", summary["fixed_direction_mirror_pass"]),
        ("summary_v14_improved", summary["v14_grid_switch_materially_improved"]),
        ("summary_small_a_fail", not summary["small_a_exactness_claim_pass"]),
        (
            "summary_initial_fail",
            not summary["finite_window_initial_condition_conformance_pass"],
        ),
        (
            "summary_sampling_fail",
            not summary["sampling_independence_pass"],
        ),
        (
            "summary_guard_fail",
            not summary["resolution_guard_continuity_pass"],
        ),
        ("summary_chronology_fail", not summary["input_chronology_pass"]),
        (
            "summary_direct_I0_fail",
            not summary["direct_lag_zero_current_pass"],
        ),
        (
            "summary_overflow_fail",
            not summary["nonfinite_frozen_limit_pass"],
        ),
        (
            "summary_inherited_fail",
            not summary["inherited_unit_local_barrier_repaired"],
        ),
        (
            "summary_golden_external_fail",
            not summary["golden_external_authority_pass"],
        ),
        ("next_step", summary["next_step"] == "37.2"),
        ("report_title", report.startswith("# Phase 059 v1.0.15")),
        ("report_status", data["status"] in report),
        ("report_finite_window", "유한 전압창 초기조건" in report),
        ("report_guard", "해상도 cap" in report),
        ("report_chronology", "실제 시간 이력" in report),
        ("report_next", "Step 37.2" in report),
        ("report_source_untouched", "원본 `Claude/`, `main`" in report),
    ]

    initial_hashes = (digest(DATA), digest(REPORT))
    run = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.extend(
        [
            ("auditor_rerun_exit", run.returncode == 0),
            (
                "auditor_rerun_deterministic",
                initial_hashes == (digest(DATA), digest(REPORT)),
            ),
        ]
    )

    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"SUMMARY {len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        print("FAILED " + ", ".join(failed))
        return 1
    print(f"PASS_P059_V1015_POINTWISE_MEMORY_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
