#!/usr/bin/env python3
"""Validate Phase 059 Step 37.2 implementation-boundary audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex/work/v1014_v1018_2_phase059/"
    "audit_phase059_v1015_implementation_boundary.py"
)
DATA = (
    ROOT / "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_AUDIT.json"
)
REPORT = (
    ROOT / "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_REVIEW.md"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    contract = data["implementation_contract"]
    scalar = contract["scalar_vector"]
    tails = contract["tail_windows"]
    state = contract["state_api"]
    order = contract["order_contract"]
    direction = contract["direction"]
    thermal = contract["nonisothermal_sampling"]
    golden = contract["golden_boundary"]
    summary = data["summary"]
    dispositions = {
        item["topic"]: item["disposition"] for item in data["findings"]
    }
    report = REPORT.read_text(encoding="utf-8")

    checks = [
        ("schema", data["schema_version"] == 1),
        ("phase_step", data["phase"] == 59 and data["step"] == "37.2"),
        (
            "status",
            data["status"]
            == "CONDITIONAL_P059_V1015_MONOTONE_CURVE_KERNEL_PRESERVED_BUT_STATE_WINDOW_PROTOCOL_AND_GOLDEN_AUTHORITY_FAIL",
        ),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_hashes",
            data["source_hashes_before"] == data["source_hashes_after"],
        ),
        ("scalar_singleton", scalar["scalar_vs_singleton_abs"] == 0.0),
        ("scalar_equilibrium", scalar["scalar_returns_equilibrium"]),
        ("scalar_sweep_diff", scalar["scalar_vs_sweep_abs"] > 2.8),
        ("tail_rows", len(tails) == 6),
        ("tail_area_increases", all(
            tails[i]["integrated_area"] < tails[i + 1]["integrated_area"]
            for i in range(len(tails) - 1)
        )),
        ("tail_short_missing", tails[0]["missing_capacity_fraction"] > 0.2),
        ("tail_long_complete", tails[-1]["missing_capacity_fraction"] < 1e-8),
        ("no_initial", not state["has_initial_xi_argument"]),
        ("no_time", not state["has_time_argument"]),
        ("no_state_return", not state["has_state_return"]),
        ("reinitialized", state["state_is_reinitialized_each_call"]),
        (
            "order_invariant",
            order["ascending_vs_descending_restored_max_abs"] == 0.0,
        ),
        (
            "mirror",
            direction["low_level_charge_discharge_mirror_max_abs"] < 1e-12,
        ),
        (
            "facade_signs",
            direction["graphite_facade_discharge_sigma"] == 1
            and direction["graphite_facade_charge_sigma"] == -1,
        ),
        (
            "no_within_reversal",
            not direction["protocol_reversal_within_one_call_supported"],
        ),
        (
            "thermal_means",
            thermal["uniform_mean_temperature_K"] == 300.0
            and thermal["clustered_mean_temperature_K"] < 292.0,
        ),
        (
            "thermal_lag_density",
            thermal["lag_ratio_clustered_to_uniform"] > 2.5,
        ),
        (
            "thermal_output_density",
            thermal["interpolated_output_max_abs"] > 0.6,
        ),
        ("golden_code_changed", golden["code_changed"]),
        ("golden_changed", golden["golden_changed"]),
        ("harness_unchanged", not golden["test_harness_changed"]),
        ("golden_arrays", golden["array_count"] == 13),
        ("golden_changed_arrays", golden["changed_array_count"] == 11),
        ("golden_delta", golden["max_delta_mismatch"] < 5e-15),
        (
            "golden_class",
            golden["evidence_class"] == "DERIVED_MODEL_OUTPUT_SNAPSHOT",
        ),
        (
            "golden_no_external",
            not golden["contains_experimental_observation"]
            and not golden["contains_si_coulomb_capacity_case"]
            and not golden["contains_nonmonotone_or_reversal_history"],
        ),
        ("finding_count", summary["finding_count"] == 12),
        (
            "scalar_disposition",
            dispositions["scalar_vector_semantics"]
            == "REQUIRE_EXPLICIT_STATELESS_SCALAR_CONTRACT",
        ),
        (
            "state_disposition",
            dispositions["initial_state_api"]
            == "FAIL_NO_INITIAL_STATE_OR_STATE_RETURN",
        ),
        (
            "tail_disposition",
            dispositions["finite_tail_window"]
            == "REQUIRE_TAIL_COMPLETION_OR_REMAINING_STATE_ACCOUNTING",
        ),
        (
            "thermal_disposition",
            dispositions["nonisothermal_sampling"]
            == "REJECT_SAMPLE_MEAN_T_AS_PATH_KINETICS",
        ),
        (
            "golden_trace",
            dispositions["golden_rebaseline_history"]
            == "PRESERVE_INTENTIONAL_ARCHITECTURE_SNAPSHOT",
        ),
        (
            "golden_oracle",
            dispositions["golden_independence"]
            == "REJECT_AS_INDEPENDENT_ORACLE",
        ),
        (
            "authority",
            dispositions["implementation_authority"]
            == "CONDITIONAL_MONOTONE_CURVE_KERNEL_NOT_PROTOCOL_SOLVER",
        ),
        (
            "repair",
            dispositions["repair_contract"]
            == "REQUIRE_STATEFUL_SEGMENTED_PROTOCOL_API",
        ),
        ("summary_kernel", summary["fixed_monotone_kernel_pass"]),
        (
            "summary_scalar_fail",
            not summary["scalar_vector_same_coordinate_equivalence_pass"],
        ),
        ("summary_initial_fail", not summary["explicit_initial_state_pass"]),
        ("summary_state_fail", not summary["state_return_pass"]),
        (
            "summary_window_fail",
            not summary["finite_window_capacity_closure_pass"],
        ),
        ("summary_unordered", summary["unordered_curve_mode_pass"]),
        (
            "summary_reversal_fail",
            not summary["within_call_reversal_pass"],
        ),
        (
            "summary_thermal_fail",
            not summary["nonisothermal_sampling_invariance_pass"],
        ),
        (
            "summary_golden_trace",
            summary["golden_rebaseline_traceability_pass"],
        ),
        (
            "summary_golden_oracle_fail",
            not summary["golden_independent_oracle_pass"],
        ),
        (
            "summary_golden_coverage_fail",
            not summary["golden_critical_coverage_pass"],
        ),
        (
            "summary_protocol_fail",
            not summary["stateful_protocol_solver_pass"],
        ),
        ("next", summary["next_step"] == "37.3"),
        ("report_title", report.startswith("# Phase 059 v1.0.15")),
        ("report_status", data["status"] in report),
        ("report_scalar", "Scalar와 sweep" in report),
        ("report_tail", "유한창 tail" in report),
        ("report_thermal", "sampling-density" in report),
        ("report_golden", "Golden rebaseline" in report),
        ("report_next", "Step 37.3" in report),
        ("report_source", "원본 `Claude/`, `main`" in report),
    ]

    initial = (digest(DATA), digest(REPORT))
    run = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks += [
        ("rerun_exit", run.returncode == 0),
        ("rerun_deterministic", initial == (digest(DATA), digest(REPORT))),
    ]

    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"SUMMARY {len(checks)-len(failed)}/{len(checks)} checks passed")
    if failed:
        print("FAILED " + ", ".join(failed))
        return 1
    print(f"PASS_P059_V1015_IMPLEMENTATION_BOUNDARY_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
