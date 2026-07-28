#!/usr/bin/env python3
"""Validate Phase 059 Step 36.4 v1.0.14 kinetics audit."""

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
    "audit_phase059_v1014_kinetics.py"
)
DATA = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 1.0e-9) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    source = data["source_contracts"]
    lineage = data["lineage_contract"]
    numeric = data["numerical_rederivation"]
    unit = numeric["unit_contract"]
    cutoff = numeric["cut_affinity"]
    barrier = numeric["barrier_scale_for_LV_equal_width"]
    lags = numeric["default_lag_lengths_V"]
    profiles = numeric["default_single_transition_profiles"]
    joint = numeric["default_joint_ratios"]
    direct = numeric["direct_lag_override"]
    overflow = numeric["overflow_contract"]
    grid = numeric["grid_handoff"]
    proof = numeric["repair_existence_proof"]
    summary = data["summary"]
    dispositions = {
        item["topic"]: item["disposition"] for item in data["findings"]
    }
    report = REPORT.read_text(encoding="utf-8")

    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("phase_step", data["phase"] == 59 and data["step"] == "36.4"),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_hashes_equal",
            data["source_hashes_before"] == data["source_hashes_after"],
        ),
        (
            "source_lines",
            source["line_counts"]
            == {
                "chapter_1": 3445,
                "production_code": 904,
                "v1010_production_code": 851,
            },
        ),
        (
            "source_equation_lines",
            source["chapter_1_lines"]["constant_current_transform"] == 1883
            and source["chapter_1_lines"]["frozen_cut_affinity"] == 1905
            and source["chapter_1_lines"]["omega_barrier"] == 1933
            and source["chapter_1_lines"]["lag_voltage_transform"] == 1959
            and source["chapter_1_lines"]["causal_memory"] == 1996
            and source["chapter_1_lines"]["grid_branch"] == 2059,
        ),
        (
            "source_code_lines",
            source["code_lines"]["func_L_q"] == 103
            and source["code_lines"]["lag_resolver"] == 333
            and source["code_lines"]["frozen_affinity"] == 361
            and source["code_lines"]["grid_switch"] == 499,
        ),
        (
            "source_admissions",
            source["explicit_dual_capacity_unit_contract"]
            and source["frozen_affinity_is_admitted"]
            and source["grid_discontinuity_is_admitted"]
            and source["default_current_broadening_is_admitted_absent"],
        ),
        (
            "missing_closed_solver",
            not source["code_has_current_partition_solver"]
            and not source["code_has_local_affinity_state"]
            and not source["code_has_time_domain_state_integrator"],
        ),
        ("primary_sources_7", summary["primary_source_count"] == 7),
        (
            "primary_dois",
            {item["doi"] for item in data["primary_source_checks"]}
            == {
                "10.1063/1.1749604",
                "10.1021/ar300145c",
                "10.1016/j.est.2020.101329",
                "10.3390/batteries9120568",
                "10.1103/PhysRevB.82.125416",
                "10.1021/jz100188d",
                "10.1149/1.2221597",
            },
        ),
        (
            "lineage_core_count",
            len(lineage["core_functions"]) == 4,
        ),
        (
            "lineage_core_ast_equal",
            lineage["all_core_functions_executable_ast_equal"]
            and all(
                item["executable_ast_equal"]
                for item in lineage["core_functions"].values()
            ),
        ),
        ("lineage_dqdv_guard_change", not lineage["dqdv_ast_equal"]),
        ("unit_rate", close(unit["correct_qdot_per_second"], 0.1 / 3600)),
        ("unit_factor_3600", close(unit["code_to_si_ratio"], 3600.0)),
        (
            "unit_lag_factor_3600",
            close(
                unit["lag_length_overestimate_if_hour_rate_enters_second_TST"],
                3600.0,
            ),
        ),
        (
            "unit_barrier_bias",
            close(
                unit["equivalent_barrier_bias_J_per_mol_at_298p15K"],
                20299.4084683,
                1.0e-4,
            ),
        ),
        (
            "unit_verdict",
            unit["verdict"] == "FACTOR_3600_MIXED_HOUR_SECOND_CONTRACT",
        ),
        ("cut_A4RT", close(cutoff["default_A_over_RT"], 4.0)),
        (
            "cut_fraction_7p065",
            close(
                cutoff["logistic_derivative_fraction_of_peak"],
                0.07065082485,
                1.0e-10,
            ),
        ),
        (
            "cut_not_claimed_5pct",
            not close(
                cutoff["logistic_derivative_fraction_of_peak"],
                cutoff["claimed_nominal_fraction"],
                1.0e-3,
            ),
        ),
        (
            "local_derivative_nonzero",
            cutoff["local_model_dlnL_dV_per_V_at_A4RT_chi0p5"] < -18.0,
        ),
        (
            "implemented_derivative_zero",
            cutoff["implemented_dlnL_dV_per_V"] == 0.0,
        ),
        (
            "barrier_code_77p6",
            close(
                barrier["code_hour_as_second_barrier_J_per_mol"],
                77642.742002,
                1.0e-3,
            ),
        ),
        (
            "barrier_si_97p9",
            close(
                barrier["dimensionally_correct_barrier_J_per_mol"],
                97942.150470,
                1.0e-3,
            ),
        ),
        (
            "barrier_difference_matches_unit",
            close(
                barrier["difference_J_per_mol"],
                unit["equivalent_barrier_bias_J_per_mol_at_298p15K"],
                1.0e-8,
            ),
        ),
        (
            "default_lag_temperatures",
            set(lags) == {"258.15", "298.15", "318.15"},
        ),
        (
            "default_lag_rates",
            all(
                set(row) == {"0.1C_numeric", "1.0C_numeric"}
                for row in lags.values()
            ),
        ),
        (
            "default_lag_four_transitions",
            all(len(values) == 4 for row in lags.values() for values in row.values()),
        ),
        (
            "default_lag_rate_linear",
            all(
                all(
                    close(high / low, 10.0, 1.0e-10)
                    for low, high in zip(
                        row["0.1C_numeric"], row["1.0C_numeric"]
                    )
                )
                for row in lags.values()
            ),
        ),
        (
            "default_lag_lowT_largest",
            max(lags["258.15"]["1.0C_numeric"])
            > max(lags["298.15"]["1.0C_numeric"])
            > max(lags["318.15"]["1.0C_numeric"]),
        ),
        (
            "default_rate_shapes_identical",
            all(
                row["max_abs_0p1C_vs_1C"] == 0.0
                for row in profiles.values()
            ),
        ),
        (
            "default_lowT_taller",
            joint["default_lowT_is_taller"]
            and joint["lowT_to_roomT_peak_height"] > 1.15,
        ),
        (
            "default_lowT_narrower",
            joint["default_lowT_is_narrower"]
            and joint["lowT_to_roomT_fwhm"] < 0.87,
        ),
        ("direct_I_invariant", direct["max_abs_I0_vs_I1"] == 0.0),
        (
            "direct_not_equilibrium",
            direct["max_abs_I0_vs_equilibrium"] > 10.0,
        ),
        ("direct_zero_current_violation", direct["violates_zero_current_limit"]),
        (
            "direct_area_finite_window",
            0.95 < direct["I0_metrics"]["area"] < 1.0,
        ),
        (
            "overflow_raw_inf",
            overflow["raw_Lq_is_positive_infinity"],
        ),
        (
            "overflow_resolved_zero",
            overflow["resolved_LV_V"] == 0.0,
        ),
        ("overflow_physics_reversal", overflow["physics_reversal_present"]),
        (
            "grid_area_0p770747",
            close(
                grid["kinetic_branch_impulse_area_fraction_at_threshold"],
                0.770747041268,
                1.0e-10,
            ),
        ),
        (
            "grid_jump_22p925pct",
            close(grid["jump_fraction"], 0.229252958732, 1.0e-10),
        ),
        (
            "grid_capacity_repair_named",
            grid["capacity_preserving_discrete_derivative"]
            == "(xi_lag[i]-xi_lag[i-1])/DeltaV",
        ),
        (
            "proof_status",
            proof["status"]
            == "REDUCED_MODEL_EXISTENCE_PROOF_NOT_MATERIAL_VALIDATION",
        ),
        (
            "proof_reference_ratio",
            close(proof["reference_lag_to_width"], 0.5),
        ),
        (
            "proof_lowT_lag_ratio",
            proof["profiles"]["258.15"]["lag_to_width"] > 3.7,
        ),
        (
            "proof_room_lag_ratio",
            close(proof["profiles"]["298.15"]["lag_to_width"], 0.5),
        ),
        (
            "proof_lowT_peak_suppressed",
            proof["lowT_to_roomT_finite_current_peak_height"] < 0.65,
        ),
        (
            "proof_lowT_broadened",
            proof["lowT_to_roomT_finite_current_fwhm"] > 1.45,
        ),
        ("proof_joint_target", proof["joint_target_reproduced"]),
        (
            "proof_area_conserved",
            all(
                row["finite_current_metrics"]["area"] > 0.997
                for row in proof["profiles"].values()
            ),
        ),
        ("findings_20", summary["finding_count"] == 20),
        ("preserve_4", summary["preserve_family_count"] == 4),
        ("reject_6", summary["reject_family_count"] == 6),
        ("fail_3", summary["fail_family_count"] == 3),
        ("require_4", summary["require_family_count"] == 4),
        ("empirical_1", summary["empirical_only_count"] == 1),
        ("blocker_1", summary["blocker_count"] == 1),
        (
            "target_supported",
            summary["experimental_joint_target_supported"],
        ),
        (
            "skeleton_preserved",
            summary["linear_relaxation_continuum_skeleton_pass"],
        ),
        (
            "closure_flags_fail",
            not summary["constant_current_unit_contract_pass"]
            and not summary["closed_galvanostatic_forward_model_pass"]
            and not summary["local_potential_barrier_pass"]
            and not summary["nonideal_detailed_balance_pass"]
            and not summary["default_current_broadening_pass"]
            and not summary["default_lowT_finite_current_joint_limit_pass"]
            and not summary["zero_current_limit_all_paths_pass"]
            and not summary["small_lag_continuity_pass"]
            and not summary["frozen_rate_limit_pass"]
            and not summary["v1010_blockers_repaired_in_v1014"],
        ),
        ("repair_proof_pass", summary["repair_existence_proof_pass"]),
        (
            "disposition_unit",
            dispositions["constant_current_unit_contract"]
            == "REJECT_FACTOR_3600_DUAL_UNIT_API",
        ),
        (
            "disposition_local_affinity",
            dispositions["local_affinity"] == "REJECT_FROZEN_CUT_AFFINITY",
        ),
        (
            "disposition_default",
            dispositions["default_current_broadening"]
            == "FAIL_DORMANT_DEFAULT_PATH",
        ),
        (
            "disposition_joint",
            dispositions["low_temperature_finite_current_joint_limit"]
            == "FAIL_USER_TARGET_ON_SHIPPED_DEFAULT",
        ),
        (
            "disposition_overflow",
            dispositions["low_temperature_overflow"]
            == "FAIL_NONFINITE_PHYSICS_REVERSAL",
        ),
        (
            "disposition_lineage",
            dispositions["v1010_to_v1014_lineage"]
            == "BLOCKERS_CARRIED_FORWARD",
        ),
        (
            "repair_contract_sections",
            set(data["repair_contract"])
            == {
                "theory_manuscript_physics_only",
                "code_conformance_after_theory_freeze",
                "validation_ladder",
            },
        ),
        (
            "conditional_status",
            summary["status"]
            == (
                "CONDITIONAL_P059_V1014_KINETIC_SKELETON_PRESERVED_BUT_"
                "CONSTANT_CURRENT_LOCAL_BARRIER_AND_JOINT_LIMIT_FAIL"
            ),
        ),
        ("next_step_36_5", summary["next_step"] == "36.5"),
        ("report_exists", REPORT.exists() and REPORT.stat().st_size > 5000),
        (
            "report_core_markers",
            "3,600배 단위 결함" in report
            and "전위·조성 의존 장벽" in report
            and "저장 default의 joint limit" in report
            and "v1.0.10에서 실제로 고쳐졌는가" in report
            and "권고하는 정본 구조" in report,
        ),
    ]

    before_data = digest(DATA)
    before_report = digest(REPORT)
    rerun = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    checks.extend(
        [
            ("auditor_rerun_exit_zero", rerun.returncode == 0),
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
