#!/usr/bin/env python3
"""Audit the v1.0.15 pointwise-memory derivation and v1.0.14 grid replacement."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import math
import warnings
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
V14_CODE = ROOT / "Claude/docs/v1.0.14/Anode_Fit_v1.0.14.py"
V15_CODE = ROOT / "Claude/docs/v1.0.15/Anode_Fit_v1.0.15.py"
V15_CH1 = ROOT / "Claude/docs/v1.0.15/graphite_ica_ch1_v1.0.15.tex"
V15_TEST = ROOT / "Claude/docs/v1.0.15/test_regression_graphite.py"
V15_HANDOVER = ROOT / "Claude/docs/v1.0.15/HANDOVER_v1.0.15.md"
V14_KINETICS = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json"
PRIOR_PROBES = ROOT / "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json"

OUTPUT = ROOT / "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first_line(path: Path, marker: str) -> int:
    return next(
        number
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        )
        if marker in line
    )


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_function_hashes(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    result: dict[str, str] = {}

    def digest(node: ast.FunctionDef) -> str:
        normalized = copy.deepcopy(node)
        if (
            normalized.body
            and isinstance(normalized.body[0], ast.Expr)
            and isinstance(normalized.body[0].value, ast.Constant)
            and isinstance(normalized.body[0].value.value, str)
        ):
            normalized.body = normalized.body[1:]
        payload = ast.dump(normalized, include_attributes=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            result[node.name] = digest(node)
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    result[f"{node.name}.{child.name}"] = digest(child)
    return result


def stable_linear_recurrence(
    coordinate: np.ndarray,
    source: np.ndarray,
    lag_length: float,
) -> np.ndarray:
    """Independent exact recurrence for a linearly interpolated source."""
    output = np.empty_like(source, dtype=float)
    output[0] = float(source[0])
    for index in range(1, source.size):
        step = abs(float(coordinate[index] - coordinate[index - 1]))
        a = step / lag_length
        e = math.exp(-a)
        delta = float(source[index] - source[index - 1])
        # For the audit points a is not near zero; this is independent of the
        # release's small-a branch.
        segment = float(source[index]) * (1.0 - e)
        segment -= (delta / a) * (1.0 - (1.0 + a) * e)
        output[index] = e * output[index - 1] + segment
    return output


def decimal_exact_step(
    a_text: str,
    previous_text: str = "0.2",
    left_text: str = "0.3",
    right_text: str = "0.7",
) -> tuple[float, float, float]:
    """Compare the release small-a approximation with a high-precision step."""
    getcontext().prec = 80
    a = Decimal(a_text)
    previous = Decimal(previous_text)
    left = Decimal(left_text)
    right = Decimal(right_text)
    delta = right - left
    e = (-a).exp()
    exact = (
        e * previous
        + right * (Decimal(1) - e)
        - (delta / a)
        * (Decimal(1) - (Decimal(1) + a) * e)
    )
    approximate = (
        (Decimal(1) - a) * previous
        + a * (left + right) / Decimal(2)
    )
    return float(approximate), float(exact), float(abs(approximate - exact))


def one_transition_model(module: Any, lag_length: float):
    return module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.0, "w": 0.02, "Q": 1.0, "L_V": lag_length}],
        Cbg=0.0,
        Rn=0.0,
    )


def max_abs(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(left) - np.asarray(right))))


def main() -> int:
    sources = [V14_CODE, V15_CODE, V15_CH1, V15_TEST, V15_HANDOVER]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in sources}

    v14 = load_module(V14_CODE, "phase059_v14_pointwise_comparison")
    v15 = load_module(V15_CODE, "phase059_v15_pointwise_audit")
    v14_audit = json.loads(V14_KINETICS.read_text(encoding="utf-8"))
    prior_probes = json.loads(PRIOR_PROBES.read_text(encoding="utf-8"))
    probe_by_id = {
        item["probe_id"]: item for item in prior_probes["probes"]
    }

    hashes14 = normalized_function_hashes(V14_CODE)
    hashes15 = normalized_function_hashes(V15_CODE)
    lineage = {
        "func_L_q_executable_ast_equal": (
            hashes14["func_L_q"] == hashes15["func_L_q"]
        ),
        "lag_resolver_executable_ast_equal": (
            hashes14["GraphiteAnodeDischargeDQDV._resolve_lag_length"]
            == hashes15["GraphiteAnodeDischargeDQDV._resolve_lag_length"]
        ),
        "dqdv_executable_ast_equal": (
            hashes14["GraphiteAnodeDischargeDQDV.dqdv"]
            == hashes15["GraphiteAnodeDischargeDQDV.dqdv"]
        ),
        "v14_lowpass_removed": "_causal_lowpass" not in hashes15,
        "v15_pointwise_added": "_causal_memory_pointwise" in hashes15,
    }

    irregular_v = np.array([-0.31, -0.22, -0.10, -0.015, 0.07, 0.18, 0.33])
    constant_source = np.full(irregular_v.size, 0.37)
    linear_source = 0.23 + 0.41 * (irregular_v - irregular_v[0])
    lag_for_recurrence = 0.017
    constant_release = v15._causal_memory_pointwise(
        irregular_v, constant_source, lag_for_recurrence
    )
    linear_release = v15._causal_memory_pointwise(
        irregular_v, linear_source, lag_for_recurrence
    )
    constant_reference = stable_linear_recurrence(
        irregular_v, constant_source, lag_for_recurrence
    )
    linear_reference = stable_linear_recurrence(
        irregular_v, linear_source, lag_for_recurrence
    )

    small_a_rows = []
    for a_text in ("0.000099999", "0.0001", "0.000100001"):
        approximate, exact, error = decimal_exact_step(a_text)
        small_a_rows.append(
            {
                "a": float(a_text),
                "release_small_a_formula": approximate,
                "exact_linear_segment": exact,
                "small_a_formula_abs_error": error,
                "release_uses_small_a_formula": float(a_text) < 1.0e-4,
            }
        )

    wide_v = np.linspace(-0.6, 0.6, 120001)
    equilibrium_model = one_transition_model(v15, 0.0)
    lagged_model = one_transition_model(v15, 0.02)
    equilibrium_wide = equilibrium_model.dqdv(
        wide_v, 298.15, 1.0, 1.0
    )
    lagged_wide = lagged_model.dqdv(wide_v, 298.15, 1.0, 1.0)
    wide_window = {
        "voltage_window_V": [-0.6, 0.6],
        "equilibrium_area": float(np.trapezoid(equilibrium_wide, wide_v)),
        "lagged_area": float(np.trapezoid(lagged_wide, wide_v)),
        "expected_capacity": 1.0,
        "equilibrium_peak": float(np.max(equilibrium_wide)),
        "lagged_peak": float(np.max(lagged_wide)),
    }

    crop_mask = (wide_v >= -0.05) & (wide_v <= 0.2)
    crop_v = wide_v[crop_mask]
    history_preserved_crop = lagged_wide[crop_mask]
    standalone_crop = lagged_model.dqdv(crop_v, 298.15, 1.0, 1.0)
    finite_window = {
        "crop_window_V": [-0.05, 0.2],
        "first_point_release_peak": float(standalone_crop[0]),
        "first_point_infinite_history_peak": float(history_preserved_crop[0]),
        "standalone_vs_infinite_history_max_abs": max_abs(
            standalone_crop, history_preserved_crop
        ),
        "standalone_crop_area": float(
            np.trapezoid(standalone_crop, crop_v)
        ),
        "infinite_history_crop_area": float(
            np.trapezoid(history_preserved_crop, crop_v)
        ),
        "area_bias_fraction_of_Q": float(
            np.trapezoid(
                standalone_crop - history_preserved_crop, crop_v
            )
        ),
        "code_initial_condition": "xi_lag(V0)=xi_eq(V0)",
        "theory_boundary": "convolution from minus infinity",
    }

    coarse_v = np.linspace(-0.3, 0.3, 61)
    dense_v = np.linspace(-0.3, 0.3, 6001)
    coarse_y = lagged_model.dqdv(coarse_v, 298.15, 1.0, 1.0)
    dense_y = lagged_model.dqdv(dense_v, 298.15, 1.0, 1.0)
    dense_at_coarse = dense_y[::100]
    sampling = {
        "coarse_spacing_V": float(coarse_v[1] - coarse_v[0]),
        "dense_spacing_V": float(dense_v[1] - dense_v[0]),
        "coarse_vs_dense_at_same_coordinates_max_abs": max_abs(
            coarse_y, dense_at_coarse
        ),
        "coarse_area": float(np.trapezoid(coarse_y, coarse_v)),
        "dense_area": float(np.trapezoid(dense_y, dense_v)),
        "interpretation": (
            "No hidden work grid remains, but piecewise-linear source "
            "integration still converges with the supplied sampling."
        ),
    }

    threshold_v = np.arange(-0.2, 0.2000001, 0.01)
    char_h = float(np.median(np.abs(np.diff(threshold_v))))
    critical_lag = char_h / float(v15._LAG_RESOLVE_DECAY_CAP)
    below_lag = critical_lag * 0.999
    above_lag = critical_lag * 1.001
    threshold_eq = one_transition_model(v15, 0.0).dqdv(
        threshold_v, 298.15, 1.0, 1.0
    )
    threshold_below = one_transition_model(v15, below_lag).dqdv(
        threshold_v, 298.15, 1.0, 1.0
    )
    threshold_above = one_transition_model(v15, above_lag).dqdv(
        threshold_v, 298.15, 1.0, 1.0
    )
    resolution_guard = {
        "decay_cap": float(v15._LAG_RESOLVE_DECAY_CAP),
        "median_spacing_V": char_h,
        "critical_lag_V": critical_lag,
        "below_lag_V": below_lag,
        "above_lag_V": above_lag,
        "below_branch_vs_equilibrium_max_abs": max_abs(
            threshold_below, threshold_eq
        ),
        "above_vs_below_max_abs_jump": max_abs(
            threshold_above, threshold_below
        ),
        "jump_fraction_of_equilibrium_peak": (
            max_abs(threshold_above, threshold_below)
            / float(np.max(threshold_eq))
        ),
        "v14_grid_handoff_jump_fraction": v14_audit[
            "numerical_rederivation"
        ]["grid_handoff"]["jump_fraction"],
        "verdict": "FINITE_SAMPLING_DEPENDENT_SWITCH_REMAINS",
    }

    mirror_v = np.linspace(-0.3, 0.3, 6001)
    mirror_model = one_transition_model(v15, 0.02)
    discharge = mirror_model.dqdv(mirror_v, 298.15, 1.0, 1.0, s=1)
    charge = mirror_model.dqdv(-mirror_v, 298.15, 1.0, 1.0, s=-1)
    mirror = {
        "max_abs_error": max_abs(discharge, charge),
        "discharge_area": float(np.trapezoid(discharge, mirror_v)),
        "charge_area_in_progress_coordinate": float(
            np.trapezoid(charge, mirror_v)
        ),
    }

    shuffled_v = mirror_v.copy()
    rng = np.random.default_rng(20260728)
    permutation = rng.permutation(shuffled_v.size)
    shuffled_output = mirror_model.dqdv(
        shuffled_v[permutation], 298.15, 1.0, 1.0, s=1
    )
    restored = np.empty_like(shuffled_output)
    restored[permutation] = shuffled_output
    chronology = {
        "sorted_vs_shuffled_then_restored_max_abs": max_abs(
            discharge, restored
        ),
        "prior_true_input_order_memory_max_abs": probe_by_id["ORD-002"][
            "measurements"
        ]["model_shuffled_vs_true_input_order_memory_max_abs"],
        "point_count": int(mirror_v.size),
        "verdict": "INPUT_CHRONOLOGY_ERASED_BY_VOLTAGE_SORTING",
    }

    direct_i0 = mirror_model.dqdv(mirror_v, 298.15, 0.0, 1.0)
    direct_i1 = mirror_model.dqdv(mirror_v, 298.15, 1.0, 1.0)
    direct_eq = mirror_model.equilibrium(mirror_v, 298.15)
    derived_transition = {
        "U": 0.0,
        "w": 0.02,
        "Q": 1.0,
        "dH_a": 50000.0,
        "dS_a": 0.0,
        "Omega": 0.0,
        "dVdq_qa": 0.3,
    }
    derived_model = v15.GraphiteAnodeDischargeDQDV(
        [derived_transition], Cbg=0.0, Rn=0.0
    )
    derived_i0 = derived_model.dqdv(mirror_v, 298.15, 0.0, 1.0)
    current_limits = {
        "direct_LV_I0_vs_I1_max_abs": max_abs(direct_i0, direct_i1),
        "direct_LV_I0_vs_equilibrium_max_abs": max_abs(
            direct_i0, direct_eq
        ),
        "derived_path_I0_vs_equilibrium_max_abs": max_abs(
            derived_i0, derived_model.equilibrium(mirror_v, 298.15)
        ),
    }

    overflow_transition = dict(derived_transition)
    overflow_transition["dH_a"] = 1.0e6
    overflow_model = v15.GraphiteAnodeDischargeDQDV(
        [overflow_transition], Cbg=0.0, Rn=0.0
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        overflow_lag = overflow_model._resolve_lag_length(
            overflow_transition, 120.0, 1.0, 1.0, 1.0, 1
        )
    overflow = {
        "resolved_lag_V": float(overflow_lag),
        "mapped_to_equilibrium": overflow_lag == 0.0,
        "physical_large_barrier_limit": "frozen or extremely slow state",
        "verdict": "NONFINITE_RATE_LIMIT_REVERSED_TO_EQUILIBRIUM",
    }

    test_text = V15_TEST.read_text(encoding="utf-8")
    test_scope = {
        "ast_assert_count": sum(
            isinstance(node, ast.Assert)
            for node in ast.walk(ast.parse(test_text))
        ),
        "mentions_pointwise_memory": "pointwise" in test_text.lower(),
        "mentions_direct_LV": "L_V" in test_text,
        "mentions_nonmonotone": "nonmonot" in test_text.lower(),
        "mentions_reversal": "reversal" in test_text.lower(),
        "mentions_pulse": "pulse" in test_text.lower(),
        "golden_rebaseline_changed_array_count": 11,
        "golden_evidence_class": "DERIVED_MODEL_OUTPUT_SNAPSHOT",
    }

    findings = [
        {
            "topic": "continuum_memory_derivation",
            "disposition": "PRESERVE_NORMALIZED_CAUSAL_KERNEL",
            "reason": (
                "The integrating-factor solution, normalized exponential "
                "kernel, and L_V->0 derivative limit are mathematically sound "
                "for a monotone coordinate with a specified past boundary."
            ),
        },
        {
            "topic": "pointwise_linear_segment_recurrence",
            "disposition": "PRESERVE_EXACT_RESOLVED_SEGMENT_INTEGRATION",
            "reason": (
                "For a>=1e-4 the recurrence exactly integrates a linearly "
                "interpolated source; constant and linear independent checks "
                "are at floating-point noise."
            ),
        },
        {
            "topic": "small_a_branch",
            "disposition": "CORRECT_EXACTNESS_CLAIM_TO_ASYMPTOTIC_APPROXIMATION",
            "reason": (
                "The a<1e-4 branch is a first-order trapezoidal asymptote, "
                "not the exact segment integral. Its local error is tiny but "
                "nonzero."
            ),
        },
        {
            "topic": "wide_window_capacity",
            "disposition": "PRESERVE_WIDE_WINDOW_CAPACITY_LIMIT",
            "reason": (
                "A saturated wide starting boundary recovers Q and produces "
                "lower, broader peaks for direct finite L_V."
            ),
        },
        {
            "topic": "finite_window_initial_state",
            "disposition": "REQUIRE_EXPLICIT_INITIAL_STATE_OR_PREHISTORY",
            "reason": (
                "The code sets xi_lag(V0)=xi_eq(V0), while the theory integrates "
                "from minus infinity. Cropped windows therefore change the "
                "observable and its integrated area."
            ),
        },
        {
            "topic": "grid_independence",
            "disposition": "PRESERVE_NO_HIDDEN_GRID_CORRECT_SAMPLING_INDEPENDENCE",
            "reason": (
                "v1.0.15 removes V_work and reverse interpolation, but nonlinear "
                "source accuracy and the guard still depend on supplied spacing."
            ),
        },
        {
            "topic": "resolution_guard",
            "disposition": "REJECT_CLAIM_OF_CONTINUOUS_NONBRANCH_GUARD",
            "reason": (
                "Crossing char_h/L_V=40 changes between analytic equilibrium "
                "and a cell-average memory derivative with a finite jump."
            ),
        },
        {
            "topic": "v14_grid_switch",
            "disposition": "PRESERVE_V15_AS_MATERIAL_IMPROVEMENT_NOT_COMPLETE_FIX",
            "reason": (
                "The 22.925% v1.0.14 two-grid-step handoff is removed, but a "
                "smaller sampling-dependent cap switch remains."
            ),
        },
        {
            "topic": "fixed_direction_mirror",
            "disposition": "PRESERVE_MONOTONE_CHARGE_DISCHARGE_MIRROR",
            "reason": "The symmetric monotone direct-LV case mirrors exactly.",
        },
        {
            "topic": "chronology",
            "disposition": "REJECT_AS_TIME_HISTORY_MODEL",
            "reason": (
                "Stable voltage sorting makes shuffled input indistinguishable "
                "from sorted input and erases pulse, rest, loop, and reversal order."
            ),
        },
        {
            "topic": "derived_zero_current",
            "disposition": "PRESERVE_FORMAL_DERIVED_I0_BRANCH",
            "reason": "The rate-derived path returns equilibrium at I=0.",
        },
        {
            "topic": "direct_lag_override",
            "disposition": "EMPIRICAL_ONLY_REJECT_PHYSICAL_I0_LIMIT",
            "reason": (
                "Direct L_V precedes the current law and remains active at I=0."
            ),
        },
        {
            "topic": "nonfinite_lag",
            "disposition": "REJECT_FROZEN_LIMIT_REVERSAL",
            "reason": (
                "A nonfinite lag from an extremely slow transition is mapped "
                "to L_V=0 equilibrium."
            ),
        },
        {
            "topic": "inherited_kinetic_closure",
            "disposition": "CARRY_FORWARD_UNIT_LOCAL_AFFINITY_BLOCKERS",
            "reason": (
                "func_L_q and the resolver executable AST are unchanged, so "
                "the 3600 unit factor, frozen cut affinity, and mesoscopic "
                "coarse-graining debts remain."
            ),
        },
        {
            "topic": "golden_rebaseline",
            "disposition": "PRESERVE_INTERNAL_SNAPSHOT_ONLY",
            "reason": (
                "The 11 changed arrays capture the new architecture output, "
                "but the harness contains no direct-LV, nonmonotone, reversal, "
                "pulse, or 3600-unit contract."
            ),
        },
        {
            "topic": "repair_contract",
            "disposition": "REQUIRE_SIGNED_TIME_STATE_INTEGRATOR",
            "reason": (
                "Keep the normalized kernel as a monotone reduced limit, but "
                "use an explicit initial state and signed time/capacity evolution "
                "for real galvanostatic protocols; make the equilibrium limit "
                "numerically continuous without a sampling threshold."
            ),
        },
    ]

    source_contracts = {
        "line_counts": {
            "v14_production_code": len(
                V14_CODE.read_text(encoding="utf-8").splitlines()
            ),
            "v15_production_code": len(
                V15_CODE.read_text(encoding="utf-8").splitlines()
            ),
            "v15_chapter_1": len(
                V15_CH1.read_text(encoding="utf-8").splitlines()
            ),
            "v15_regression_test": len(
                V15_TEST.read_text(encoding="utf-8").splitlines()
            ),
        },
        "chapter_1_lines": {
            "finite_initial_general_solution": first_line(
                V15_CH1, "r_j(q)=r_j(q_0)"
            ),
            "minus_infinity_boundary": first_line(
                V15_CH1, "q_0\\to-\\infty"
            ),
            "normalized_lag_integral": first_line(
                V15_CH1, "\\boxed{\\;\\xi_{\\mathrm{lag},j}(V)"
            ),
            "peak_shape": first_line(
                V15_CH1, "\\boxed{\\;\\text{peak shape}"
            ),
            "small_lag_limit": first_line(
                V15_CH1, "\\lim_{L_{V,j}\\to0}\\text{peak shape}"
            ),
            "direction_reversal": first_line(
                V15_CH1, "\\label{eq:reversal}"
            ),
            "pointwise_sum": first_line(
                V15_CH1, "\\label{eq:sum}"
            ),
        },
        "code_lines": {
            "decay_cap": first_line(V15_CODE, "_LAG_RESOLVE_DECAY_CAP ="),
            "pointwise_recurrence": first_line(
                V15_CODE, "def _causal_memory_pointwise"
            ),
            "small_a_branch": first_line(V15_CODE, "if a < 1e-4"),
            "initial_condition": first_line(
                V15_CODE, "out[0] = float(ksi_eq[0])"
            ),
            "voltage_sorting": first_line(
                V15_CODE, "order = np.argsort(V_n"
            ),
            "resolution_switch": first_line(
                V15_CODE, "unresolved = (char_h <= 0.0)"
            ),
            "nonfinite_to_zero": first_line(
                V15_CODE, "if not np.isfinite(L_q):"
            ),
            "curve_hour_rate": first_line(
                V15_CODE, "c_rate    : C-rate [1/h]"
            ),
        },
    }

    summary_status = (
        "CONDITIONAL_P059_V1015_POINTWISE_MEMORY_CORE_PRESERVED_BUT_"
        "FINITE_WINDOW_RESOLUTION_SWITCH_AND_CHRONOLOGY_FAIL"
    )
    data = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "phase": 59,
        "step": "37.1",
        "scope": (
            "v1.0.15 pointwise continuous-memory derivation, v1.0.14 "
            "grid-switch replacement, and independent numerical limits"
        ),
        "status": summary_status,
        "source_contracts": source_contracts,
        "lineage_contract": lineage,
        "independent_rederivation": {
            "continuum_equations": {
                "state_ode": (
                    "d xi/ds = (xi_eq-xi)/L, with signed monotone progress s"
                ),
                "finite_initial_solution": (
                    "xi(s)=exp(-(s-s0)/L)xi(s0)+(1/L) integral_s0^s "
                    "exp(-(s-u)/L)xi_eq(u)du"
                ),
                "natural_boundary_solution": (
                    "xi_lag(s)=(1/L) integral_-infinity^s "
                    "exp(-(s-u)/L)xi_eq(u)du"
                ),
                "peak_shape": "(xi_eq-xi_lag)/L = d xi_lag/ds",
                "small_lag_limit": "lim_L->0 peak_shape = d xi_eq/ds",
                "capacity_identity": (
                    "integral peak_shape ds = xi_lag(s_end)-xi_lag(s_start)"
                ),
            },
            "assumption_boundary": (
                "The minus-infinity convolution is equivalent to the finite "
                "initial-value problem only when prehistory or a saturated "
                "equilibrium boundary is supplied."
            ),
        },
        "numerical_rederivation": {
            "recurrence_identity": {
                "irregular_point_count": int(irregular_v.size),
                "lag_length_V": lag_for_recurrence,
                "constant_source_max_abs_error": max_abs(
                    constant_release, constant_reference
                ),
                "linear_source_max_abs_error": max_abs(
                    linear_release, linear_reference
                ),
            },
            "small_a_branch": small_a_rows,
            "wide_window": wide_window,
            "finite_window_initial_condition": finite_window,
            "sampling_dependence": sampling,
            "resolution_guard": resolution_guard,
            "fixed_direction_mirror": mirror,
            "chronology": chronology,
            "current_limits": current_limits,
            "nonfinite_lag": overflow,
        },
        "test_and_golden_scope": test_scope,
        "findings": findings,
        "summary": {
            "status": summary_status,
            "finding_count": len(findings),
            "continuum_kernel_pass": True,
            "resolved_linear_segment_recurrence_pass": True,
            "wide_window_capacity_pass": True,
            "fixed_direction_mirror_pass": True,
            "v14_grid_switch_materially_improved": True,
            "small_a_exactness_claim_pass": False,
            "finite_window_initial_condition_conformance_pass": False,
            "sampling_independence_pass": False,
            "resolution_guard_continuity_pass": False,
            "input_chronology_pass": False,
            "direct_lag_zero_current_pass": False,
            "nonfinite_frozen_limit_pass": False,
            "inherited_unit_local_barrier_repaired": False,
            "golden_external_authority_pass": False,
            "next_step": "37.2",
        },
        "source_hashes_before": before,
    }

    report_lines = [
        "# Phase 059 v1.0.15 점별 연속 메모리 독립 재유도",
        "",
        f"상태: `{summary_status}`",
        "",
        "## 결론",
        "",
        (
            "v1.0.15는 v1.0.14의 숨은 `V_work`·역보간과 "
            "두-grid-step 전환을 제거한 **실질적 개선**이다. 정규화된 "
            "지수 기억 커널, 선형 구간 적분, 넓은 전압창의 용량 보존과 "
            "고정 방향 충·방전 거울은 보존한다."
        ),
        "",
        (
            "그러나 “모든 평가점에서 연속이며 격자와 무관하다”는 강한 "
            "해석은 성립하지 않는다. 유한창 첫 상태가 이론의 "
            "무한 과거 경계와 다르고, `char_h/L_V=40`에서 여전히 "
            "샘플링 의존 전환이 있으며, 전압 정렬이 실제 protocol "
            "chronology를 지운다."
        ),
        "",
        "## 독립 유도",
        "",
        (
            r"진행 좌표를 \(s\)라 하면 "
            r"\(\mathrm d\xi/\mathrm ds=(\xi_\mathrm{eq}-\xi)/L\)이고, "
            "유한 초기점 해는"
        ),
        "",
        (
            r"\[\xi(s)=e^{-(s-s_0)/L}\xi(s_0)+"
            r"\frac1L\int_{s_0}^{s}e^{-(s-u)/L}"
            r"\xi_\mathrm{eq}(u)\,\mathrm du.\]"
        ),
        "",
        (
            r"\(s_0\to-\infty\)의 정규화 convolution은 초기항이 "
            "소멸할 만큼 충분한 prehistory가 있을 때만 이 해와 같다. "
            r"또한 \((\xi_\mathrm{eq}-\xi)/L=\mathrm d\xi/\mathrm ds\)"
            "이므로 면적은 시작과 끝의 실제 상태 차이다. 따라서 유한 "
            "창에서는 초기 상태를 생략할 수 없다."
        ),
        "",
        "## 보존되는 수학과 개선",
        "",
        (
            f"- 불규칙 7점에서 상수·선형 source recurrence 오차는 각각 "
            f"`{max_abs(constant_release, constant_reference):.3e}`, "
            f"`{max_abs(linear_release, linear_reference):.3e}`다."
        ),
        (
            f"- 넓은 창의 평형/지연 면적은 "
            f"`{wide_window['equilibrium_area']:.12f}`, "
            f"`{wide_window['lagged_area']:.12f}`로 Q=1을 보존한다."
        ),
        (
            rf"- direct \(L_V=0.02\)에서 peak는 "
            f"`{wide_window['equilibrium_peak']:.6f}`→"
            f"`{wide_window['lagged_peak']:.6f}`로 낮아진다."
        ),
        (
            f"- 대칭 단일 전이의 충·방전 거울 최대 오차는 "
            f"`{mirror['max_abs_error']:.3e}`다."
        ),
        (
            "- v1.0.14의 22.925% 두-grid-step handoff를 제거했고, "
            "입력 좌표로 직접 반환한다."
        ),
        "",
        "## 새로 확인한 결함",
        "",
        "### 1. 유한 전압창 초기조건",
        "",
        (
            r"이론은 \(-\infty\)부터의 과거를 적분하지만 코드는 첫 점에서 "
            "`xi_lag=xi_eq`로 둔다. [-0.05, 0.2] V만 독립 호출하면 첫 "
            f"peak는 `{finite_window['first_point_release_peak']:.6f}`, "
            "넓은 창의 실제 과거를 유지하면 "
            f"`{finite_window['first_point_infinite_history_peak']:.6f}`다. "
            "같은 crop에서 최대 차이는 "
            f"`{finite_window['standalone_vs_infinite_history_max_abs']:.6f}`, "
            "면적은 "
            f"`{finite_window['standalone_crop_area']:.6f}` 대 "
            f"`{finite_window['infinite_history_crop_area']:.6f}`다."
        ),
        "",
        "### 2. 해상도 cap은 여전히 유한 전환이다",
        "",
        (
            f"입력 간격 `{char_h:.6g}` V에서 cap 경계는 "
            f"`L_V={critical_lag:.6g}` V다. 경계 아래는 평형 종, "
            "경계 위는 cell-average memory 종이 되며 최대 jump는 "
            f"`{resolution_guard['above_vs_below_max_abs_jump']:.6f}` "
            f"({100*resolution_guard['jump_fraction_of_equilibrium_peak']:.3f}% "
            "of equilibrium peak)다. 따라서 “물리 분기가 아니며 "
            "불연속이 없다”는 주장은 기각한다."
        ),
        "",
        "### 3. 숨은 격자 제거와 sampling independence는 다르다",
        "",
        (
            "작업격자와 역보간은 사라졌지만 logistic source를 구간별 "
            "선형으로 근사하므로 supplied sampling에 따라 수렴한다. "
            "0.01 V와 0.0001 V 입력을 같은 좌표에서 비교한 최대 차이는 "
            f"`{sampling['coarse_vs_dense_at_same_coordinates_max_abs']:.6f}`다."
        ),
        "",
        "### 4. 실제 시간 이력을 계산하지 않는다",
        "",
        (
            "전압 좌표를 섞은 뒤 원위치로 복구해도 출력 차이는 "
            f"`{chronology['sorted_vs_shuffled_then_restored_max_abs']:.3e}`다. "
            "반면 입력 순서를 실제로 따라간 recurrence와는 기존 독립 "
            f"probe에서 `{chronology['prior_true_input_order_memory_max_abs']:.6f}` "
            "차이가 났다. pulse·rest·loop·reversal의 시간 이력 모델로 "
            "사용할 수 없다."
        ),
        "",
        "### 5. 기존 동역학 blocker는 고쳐지지 않았다",
        "",
        (
            "`func_L_q`와 lag resolver의 executable AST는 v1.0.14와 "
            "동일하다. 따라서 3,600 시간단위 인자, 컷점에 동결된 "
            "affinity, 전극-scale coarse graining 부재는 그대로다. "
            "direct `L_V`는 I=0에서도 활성이고, derived overflow는 "
            "다시 L_V=0 평형으로 뒤집힌다."
        ),
        "",
        "## 최종 처분",
        "",
        (
            "점별 지수 커널은 monotone sweep의 **축약 수학 모형**으로 "
            "보존한다. 실제 정전류 protocol에는 전압 정렬이 아니라 "
            "부호 있는 시간/용량 상태 적분, 명시 초기 상태, current "
            "conservation과 terminal-voltage closure가 필요하다. "
            "평형 극한은 sampling threshold 없이 연속적인 수치식으로 "
            "구현해야 한다."
        ),
        "",
        "다음은 Step 37.2: 방향, 초기조건, 유한창, tail, mirror, "
        "scalar/vector와 golden rebaseline의 구현 경계 종합 판정이다.",
        "",
        "원본 `Claude/`, `main`과 생산 이론·코드는 수정하지 않았다.",
    ]

    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    after = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
    data["source_hashes_after"] = after
    data["source_unchanged"] = before == after
    OUTPUT.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
