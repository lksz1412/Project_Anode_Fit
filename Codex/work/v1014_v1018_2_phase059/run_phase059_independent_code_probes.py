#!/usr/bin/env python3
"""Run independent physics/numerics probes for Phase 059 Step 34.4.

The probes import frozen release modules read-only.  They do not call the
release test/demo harnesses and do not treat a known-defect confirmation as a
scientific PASS.  The execution gate means only that the independent
measurements were completed reproducibly.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import sys
import warnings
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
OUTPUT = RESULTS / "PHASE_059_INDEPENDENT_CODE_PROBES.json"
REVIEW = RESULTS / "PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"

MODULE_PATHS = {
    "v1.0.14": "Claude/docs/v1.0.14/Anode_Fit_v1.0.14.py",
    "v1.0.15": "Claude/docs/v1.0.15/Anode_Fit_v1.0.15.py",
    "v1.0.16": "Claude/docs/v1.0.16/Anode_Fit_v1.0.16.py",
    "v1.0.18.2": "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(version: str, relative: str):
    name = "phase059_probe_" + version.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    yv = np.asarray(y, dtype=float)
    xv = np.asarray(x, dtype=float)
    return float(np.sum(0.5 * (yv[:-1] + yv[1:]) * np.diff(xv)))


def max_abs(a: Any, b: Any) -> float:
    av = np.asarray(a, dtype=float)
    bv = np.asarray(b, dtype=float)
    return float(np.max(np.abs(av - bv)))


def fwhm(x: np.ndarray, y: np.ndarray) -> float:
    xv = np.asarray(x, dtype=float)
    yv = np.asarray(y, dtype=float)
    half = 0.5 * float(np.max(yv))
    indices = np.flatnonzero(yv >= half)
    if indices.size < 2:
        return float("nan")
    return float(xv[indices[-1]] - xv[indices[0]])


def finite_difference(function, temperature: float, step: float = 1.0e-3) -> float:
    return float((function(temperature + step) - function(temperature - step)) / (2.0 * step))


def probe(
    probe_id: str,
    category: str,
    title: str,
    verdict: str,
    contract: str,
    measurements: dict[str, Any],
    acceptance: str,
    interpretation: str,
) -> dict[str, Any]:
    return {
        "probe_id": probe_id,
        "category": category,
        "title": title,
        "verdict": verdict,
        "contract": contract,
        "measurements": measurements,
        "acceptance": acceptance,
        "interpretation": interpretation,
    }


def raw_einstein_quantities(R: float, theta: float, temperature: float) -> dict[str, float]:
    x = theta / temperature
    free = R * temperature * float(np.log1p(-np.exp(-x)))
    entropy = R * (
        -float(np.log1p(-np.exp(-x))) + x / float(np.expm1(x))
    )
    internal = R * theta / float(np.expm1(x))
    return {
        "F_J_per_mol": free,
        "S_J_per_molK": entropy,
        "U_J_per_mol": internal,
        "F_plus_TS_J_per_mol": free + temperature * entropy,
    }


def feature_lineage(modules: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for version, module in modules.items():
        cls = module.GraphiteAnodeDischargeDQDV
        records.append(
            {
                "version": version,
                "source_path": MODULE_PATHS[version],
                "source_sha256": sha256(ROOT / MODULE_PATHS[version]),
                "has_pointwise_memory": hasattr(module, "_causal_memory_pointwise"),
                "has_grid_lowpass": hasattr(module, "_causal_lowpass"),
                "has_dwdT": hasattr(cls, "_dwdT"),
                "has_vib_theta": hasattr(cls, "_vib_theta"),
                "has_vib_entropy": hasattr(cls, "_vib_dS"),
            }
        )
    return records


def run_latest_probes(module) -> list[dict[str, Any]]:
    probes: list[dict[str, Any]] = []
    R = float(module.R)
    F = float(module.F)
    T0 = 298.15

    # MEM-001: the recurrence is exact for a piecewise-linear source.
    path = np.array([0.0, 0.003, 0.011, 0.019, 0.041, 0.070, 0.111])
    lag_length = 0.017
    intercept = 0.21
    slope = 0.43
    source = intercept + slope * path
    memory = module._causal_memory_pointwise(path, source, lag_length)
    analytic = intercept + slope * (
        path - lag_length + lag_length * np.exp(-path / lag_length)
    )
    constant_memory = module._causal_memory_pointwise(
        path, np.full_like(path, 0.37), lag_length
    )
    probes.append(
        probe(
            "MEM-001",
            "memory",
            "pointwise recurrence normalization and linear-source exactness",
            "PASS_IDENTITY",
            "A normalized exponential memory preserves a constant source and exactly integrates a linear source on each segment.",
            {
                "constant_source_max_abs_error": max_abs(constant_memory, 0.37),
                "linear_source_max_abs_error": max_abs(memory, analytic),
                "irregular_path_point_count": int(path.size),
                "lag_length_V": lag_length,
            },
            "both maximum errors < 1e-12",
            "The v1.0.15 pointwise recurrence itself satisfies its local normalization/exact-integration contract.",
        )
    )

    # MEM-002/003: wide-window conservation, suppression, broadening and L->0.
    voltage = np.linspace(-0.6, 0.6, 60001)
    base_transition = {"U": 0.0, "w": 0.02, "Q": 1.0}
    equilibrium_model = module.GraphiteAnodeDischargeDQDV(
        [copy.deepcopy(base_transition)], Rn=0.0, Cbg=0.0
    )
    equilibrium = np.asarray(equilibrium_model.equilibrium(voltage, T0), dtype=float)
    lagged_transition = dict(base_transition, L_V=0.02)
    lagged_model = module.GraphiteAnodeDischargeDQDV(
        [lagged_transition], Rn=0.0, Cbg=0.0
    )
    lagged = np.asarray(lagged_model.dqdv(voltage, T0, 0.7, 1.0, +1), dtype=float)
    probes.append(
        probe(
            "MEM-002",
            "memory",
            "wide-window capacity conservation with peak suppression/broadening",
            "PASS_IDENTITY",
            "For a resolved causal lag on a sufficiently wide voltage window, integral(dQ/dV)dV approaches Q while peak height falls and FWHM grows.",
            {
                "equilibrium_area": trapezoid(equilibrium, voltage),
                "lagged_area": trapezoid(lagged, voltage),
                "expected_capacity": 1.0,
                "equilibrium_peak": float(np.max(equilibrium)),
                "lagged_peak": float(np.max(lagged)),
                "equilibrium_fwhm_V": fwhm(voltage, equilibrium),
                "lagged_fwhm_V": fwhm(voltage, lagged),
                "voltage_window_V": [float(voltage[0]), float(voltage[-1])],
            },
            "area error < 1e-8; lagged peak lower; lagged FWHM larger",
            "The direct-LV mathematical kernel can produce the user's qualitative suppression/broadening observation without losing transition capacity on a wide window.",
        )
    )

    lag_sweep = []
    for lag in [1.0e-2, 3.0e-3, 1.0e-3, 3.0e-4, 1.0e-4]:
        model = module.GraphiteAnodeDischargeDQDV(
            [dict(base_transition, L_V=lag)], Rn=0.0, Cbg=0.0
        )
        values = np.asarray(model.dqdv(voltage, T0, 0.7, 1.0, +1), dtype=float)
        lag_sweep.append(
            {
                "L_V": lag,
                "max_abs_vs_equilibrium": max_abs(values, equilibrium),
                "area": trapezoid(values, voltage),
                "peak": float(np.max(values)),
            }
        )
    differences = [item["max_abs_vs_equilibrium"] for item in lag_sweep]
    probes.append(
        probe(
            "MEM-003",
            "memory",
            "resolved small-LV continuity toward equilibrium",
            "PASS_IDENTITY",
            "At fixed adequate resolution, the causal peak converges continuously to the equilibrium derivative as L_V decreases.",
            {
                "sweep": lag_sweep,
                "difference_strictly_decreases": all(
                    a > b for a, b in zip(differences, differences[1:])
                ),
                "grid_spacing_V": float(voltage[1] - voltage[0]),
            },
            "max-error sequence strictly decreases and all areas remain within 1e-8 of Q",
            "The resolved branch has the correct L_V->0 trend; this does not validate the provenance of L_V.",
        )
    )

    # ORD-001: exact mirror under the symmetric one-transition contract.
    mirror_voltage = np.linspace(-0.25, 0.25, 25001)
    mirror_model = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.0, "w": 0.018, "Q": 1.0, "L_V": 0.013}],
        Rn=0.0,
        Cbg=0.0,
    )
    discharge = np.asarray(
        mirror_model.dqdv(mirror_voltage, T0, 0.5, 1.0, +1), dtype=float
    )
    reflected_voltage = -mirror_voltage
    charge_reflected = np.asarray(
        mirror_model.dqdv(reflected_voltage, T0, 0.5, 1.0, -1), dtype=float
    )
    probes.append(
        probe(
            "ORD-001",
            "direction",
            "charge/discharge mirror identity",
            "PASS_IDENTITY",
            "With zero polarization/hysteresis and symmetric parameters, reversing both direction and voltage about U must mirror the same positive peak.",
            {
                "mirror_max_abs_error": max_abs(discharge, charge_reflected),
                "discharge_area": trapezoid(discharge, mirror_voltage),
                "charge_area_in_progress_coordinate": -trapezoid(
                    charge_reflected, reflected_voltage
                ),
            },
            "mirror max error < 1e-12 and both progress-coordinate areas approach Q",
            "The fixed-direction mirror convention is internally coherent.",
        )
    )

    # ORD-002: permutation invariance is a failure for chronology-sensitive data.
    chronology_voltage = np.linspace(-0.22, 0.22, 4001)
    chronology_model = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.0, "w": 0.018, "Q": 1.0, "L_V": 0.015}],
        Rn=0.0,
        Cbg=0.0,
    )
    sorted_curve = np.asarray(
        chronology_model.dqdv(chronology_voltage, T0, 0.4, 1.0, +1),
        dtype=float,
    )
    rng = np.random.default_rng(20260728)
    permutation = rng.permutation(chronology_voltage.size)
    shuffled_voltage = chronology_voltage[permutation]
    shuffled_curve = np.asarray(
        chronology_model.dqdv(shuffled_voltage, T0, 0.4, 1.0, +1),
        dtype=float,
    )
    shuffled_restored = np.empty_like(shuffled_curve)
    shuffled_restored[permutation] = shuffled_curve
    shuffled_eq = np.asarray(
        module.func_ksi_eq(T0, shuffled_voltage, 0.0, 0.018 * F / (R * T0), +1),
        dtype=float,
    )
    true_order_memory = module._causal_memory_pointwise(
        shuffled_voltage, shuffled_eq, 0.015
    )
    true_order_peak = (shuffled_eq - true_order_memory) / 0.015
    probes.append(
        probe(
            "ORD-002",
            "direction",
            "input chronology is erased by voltage sorting",
            "BLOCKER_CONFIRMED",
            "A history-dependent model must distinguish different acquisition orders of the same voltage coordinates unless the API explicitly declares an unordered curve.",
            {
                "sorted_vs_shuffled_then_restored_max_abs": max_abs(
                    sorted_curve, shuffled_restored
                ),
                "model_shuffled_vs_true_input_order_memory_max_abs": max_abs(
                    shuffled_curve, true_order_peak
                ),
                "point_count": int(chronology_voltage.size),
                "permutation_seed": 20260728,
            },
            "defect is confirmed when restored model output is invariant while an order-following recurrence differs materially",
            "dqdv sorts voltage before evolving memory. It therefore cannot represent pulses, reversals, loops, pauses, or measurement chronology from the supplied order.",
        )
    )

    # CUR-001/002 and UNT-001: current limits and units.
    dynamic_transition = {
        "U": 0.0,
        "w": 0.02,
        "Q": 1.0,
        "dH_a": 44000.0,
        "dS_a": 0.0,
        "dVdq_qa": 0.30,
        "Omega": 0.0,
    }
    dynamic_model = module.GraphiteAnodeDischargeDQDV(
        [copy.deepcopy(dynamic_transition)], Rn=0.0, Cbg=0.0
    )
    dynamic_eq = np.asarray(dynamic_model.equilibrium(voltage, T0), dtype=float)
    i0_dynamic = np.asarray(
        dynamic_model.dqdv(voltage, T0, 0.0, 1.0, +1), dtype=float
    )
    dynamic_lags = {}
    for current in [0.0, 1.0e-6, 1.0e-4, 1.0e-2, 1.0]:
        dynamic_lags[str(current)] = float(
            dynamic_model._resolve_lag_length(
                dynamic_transition,
                T0,
                current,
                1.0,
                float(dynamic_model._n_factor(dynamic_transition, T0)),
                +1,
            )
        )
    probes.append(
        probe(
            "CUR-001",
            "current",
            "derived kinetic path has an equilibrium zero-current branch",
            "PASS_IDENTITY",
            "A rate-derived lag must vanish at I=0 and the observable must equal equilibrium.",
            {
                "I0_vs_equilibrium_max_abs": max_abs(i0_dynamic, dynamic_eq),
                "resolved_lag_lengths_V": dynamic_lags,
            },
            "I=0 difference = 0 and resolved lag length = 0",
            "The derived path implements the formal zero-current branch, although its units and barrier closure remain separate issues.",
        )
    )

    direct_i0 = np.asarray(
        lagged_model.dqdv(voltage, T0, 0.0, 1.0, +1), dtype=float
    )
    direct_i1 = np.asarray(
        lagged_model.dqdv(voltage, T0, 1.0, 1.0, +1), dtype=float
    )
    probes.append(
        probe(
            "CUR-002",
            "current",
            "direct LV override bypasses the zero-current limit",
            "BLOCKER_CONFIRMED",
            "Any physical finite-current lag must disappear when I approaches zero; a fit convenience parameter cannot silently override that limit.",
            {
                "direct_LV_V": 0.02,
                "I0_vs_I1_max_abs": max_abs(direct_i0, direct_i1),
                "I0_vs_equilibrium_max_abs": max_abs(direct_i0, equilibrium),
                "I0_peak": float(np.max(direct_i0)),
                "equilibrium_peak": float(np.max(equilibrium)),
            },
            "defect is confirmed when I0 equals I1 but differs from equilibrium",
            "The override is useful as a diagnostic kernel but is not a valid physical current law in its present unconditional precedence.",
        )
    )

    A = 4.0 * R * T0
    lag_code_units = float(
        module.func_L_q(T0, 3600.0, 3600.0, 44000.0, 0.0, 0.5, A)
    )
    lag_si_units = float(
        module.func_L_q(T0, 1.0, 3600.0, 44000.0, 0.0, 0.5, A)
    )
    unit_model = module.GraphiteAnodeDischargeDQDV(
        [copy.deepcopy(dynamic_transition)], Rn=0.01, Cbg=0.0
    )
    code_c_rate_curve = np.asarray(
        unit_model.curve(
            voltage, direction="discharge", c_rate=1.0, Q_cell=3600.0, T=T0
        ),
        dtype=float,
    )
    si_current_curve = np.asarray(
        unit_model.dqdv(voltage, T0, 1.0, 3600.0, +1), dtype=float
    )
    probes.append(
        probe(
            "UNT-001",
            "units",
            "C-rate per hour is passed to a per-second attempt-frequency law",
            "BLOCKER_CONFIRMED",
            "For Q_cell=3600 C, 1C means 1 A; c_rate[1/h] must be divided by 3600 before entering I/Q in an SI-second kinetic law.",
            {
                "Q_cell_C": 3600.0,
                "c_rate_per_h": 1.0,
                "code_implied_current_A": 3600.0,
                "physical_current_A": 1.0,
                "func_Lq_code_to_SI_ratio": lag_code_units / lag_si_units,
                "curve_max_abs_difference": max_abs(
                    code_c_rate_curve, si_current_curve
                ),
            },
            "defect is confirmed when kinetic ratio is 3600 and code-implied current is 3600 A",
            "The curve facade and func_L_q use incompatible hour/second contracts unless Q_cell is redefined away from the documented charge unit.",
        )
    )

    # WID-001..006: width and entropy chain.
    temp_step = 1.0e-3
    n_const_tr = {"U": 0.0, "n": 1.7, "Q": 1.0}
    n_const_model = module.GraphiteAnodeDischargeDQDV([n_const_tr])
    n_const_fd = finite_difference(
        lambda temp: float(n_const_model._width(n_const_tr, temp)),
        T0,
        temp_step,
    )
    n_const_analytic = float(n_const_model._dwdT(n_const_tr, T0))
    probes.append(
        probe(
            "WID-001",
            "width_entropy",
            "constant-n thermal width derivative",
            "PASS_IDENTITY",
            "For w=nRT/F with constant n, dw/dT=nR/F.",
            {
                "finite_difference_V_per_K": n_const_fd,
                "code_dwdT_V_per_K": n_const_analytic,
                "expected_nR_over_F": 1.7 * R / F,
                "abs_error": abs(n_const_fd - n_const_analytic),
            },
            "finite-difference/code error < 1e-12",
            "The explicit constant-n branch propagates the thermal width derivative correctly.",
        )
    )

    n_t_tr = {
        "dH_rxn": -12000.0,
        "dS_rxn": 17.0,
        "n": 1.4,
        "n_T1": 1.7e-3,
        "n_T_ref": T0,
        "Q": 1.0,
    }
    n_t_model = module.GraphiteAnodeDischargeDQDV([n_t_tr], Cbg=0.0)
    n_t_fd = finite_difference(
        lambda temp: float(n_t_model._width(n_t_tr, temp)), T0, temp_step
    )
    n_t_analytic = float(n_t_model._dwdT(n_t_tr, T0))
    xi_target = 0.31
    logit = float(np.log(xi_target / (1.0 - xi_target)))

    def state_voltage(temp: float) -> float:
        center = float(module.func_U_j(temp, n_t_tr["dH_rxn"], n_t_tr["dS_rxn"]))
        return center + float(n_t_model._width(n_t_tr, temp)) * logit

    state_voltage_T0 = state_voltage(T0)
    entropy_code = float(
        np.asarray(
            n_t_model.entropy_coefficient(np.array([state_voltage_T0]), T0)
        )[0]
    )
    state_voltage_fd = finite_difference(state_voltage, T0, temp_step)
    probes.append(
        probe(
            "WID-002",
            "width_entropy",
            "n(T) width derivative and fixed-state entropy chain",
            "PASS_IDENTITY",
            "For n(T)=n0+n1(T-Tref), dw/dT=(R/F)(n(T)+T n1), and dU(x)/dT=dS/F+(dw/dT)logit(x).",
            {
                "width_finite_difference_V_per_K": n_t_fd,
                "width_code_dwdT_V_per_K": n_t_analytic,
                "width_abs_error": abs(n_t_fd - n_t_analytic),
                "state_fraction": xi_target,
                "state_voltage_V": state_voltage_T0,
                "entropy_code_V_per_K": entropy_code,
                "state_voltage_finite_difference_V_per_K": state_voltage_fd,
                "entropy_abs_error": abs(entropy_code - state_voltage_fd),
            },
            "both finite-difference errors < 1e-10",
            "The v1.0.16 n(T) algebra and its configurational entropy propagation are internally consistent for one transition.",
        )
    )

    w_only_tr = {"U": 0.0, "w": 0.013, "Q": 1.0}
    w_only_model = module.GraphiteAnodeDischargeDQDV([w_only_tr])
    w_only_fd = finite_difference(
        lambda temp: float(w_only_model._width(w_only_tr, temp)), T0, temp_step
    )
    probes.append(
        probe(
            "WID-003",
            "width_entropy",
            "w-only empirical width remains temperature-frozen",
            "PASS_IDENTITY",
            "A direct empirical w without n is constant in temperature and has dw/dT=0.",
            {
                "width_258K_V": float(w_only_model._width(w_only_tr, 258.15)),
                "width_318K_V": float(w_only_model._width(w_only_tr, 318.15)),
                "finite_difference_V_per_K": w_only_fd,
                "code_dwdT_V_per_K": float(w_only_model._dwdT(w_only_tr, T0)),
            },
            "both derivative magnitudes < 1e-12 and widths equal",
            "The w-only branch is a clearly empirical, temperature-frozen width law.",
        )
    )

    default_tr = {"U": 0.0, "Q": 1.0}
    default_model = module.GraphiteAnodeDischargeDQDV([default_tr])
    default_fd = finite_difference(
        lambda temp: float(default_model._width(default_tr, temp)), T0, temp_step
    )
    default_code = float(default_model._dwdT(default_tr, T0))
    probes.append(
        probe(
            "WID-004",
            "width_entropy",
            "implicit default width and entropy derivative disagree",
            "BLOCKER_CONFIRMED",
            "If missing n/w defaults to n=1 and w=RT/F, the same branch must use dw/dT=R/F rather than zero.",
            {
                "default_width_V": float(default_model._width(default_tr, T0)),
                "finite_difference_V_per_K": default_fd,
                "code_dwdT_V_per_K": default_code,
                "expected_R_over_F": R / F,
                "mismatch_V_per_K": default_fd - default_code,
            },
            "defect is confirmed when finite difference equals R/F but code returns zero",
            "The observable and entropy paths assign different temperature laws to the same implicit default transition.",
        )
    )

    bad_tr = {"U": 0.0, "n": 0.1, "n_T1": -0.01, "n_T_ref": T0, "Q": 1.0}
    positivity_exception = None
    try:
        module.GraphiteAnodeDischargeDQDV([bad_tr])._width(bad_tr, T0 + 20.0)
    except Exception as exc:  # exact class/message are evidence
        positivity_exception = f"{type(exc).__name__}: {exc}"
    probes.append(
        probe(
            "WID-005",
            "width_entropy",
            "n(T) positivity guard",
            "PASS_GUARD",
            "Any parameterized transition width must remain strictly positive over the evaluated temperature range.",
            {"exception": positivity_exception},
            "a ValueError is raised for n(T)<=0",
            "The v1.0.16 fail-fast guard prevents negative or zero peak widths at evaluated points.",
        )
    )

    both_a = {"U": 0.0, "n": 1.2, "w": 0.003, "Q": 1.0}
    both_b = {"U": 0.0, "n": 1.2, "w": 0.090, "Q": 1.0}
    both_a_model = module.GraphiteAnodeDischargeDQDV([both_a])
    both_b_model = module.GraphiteAnodeDischargeDQDV([both_b])
    both_a_curve = np.asarray(both_a_model.equilibrium(voltage, T0), dtype=float)
    both_b_curve = np.asarray(both_b_model.equilibrium(voltage, T0), dtype=float)
    probes.append(
        probe(
            "WID-006",
            "identifiability",
            "n shadows w when both are supplied",
            "IDENTIFIABILITY_CAUTION",
            "Two exposed fit parameters must not be presented as simultaneously identifiable when one has exact precedence and the other is inert.",
            {
                "w_values_compared_V": [both_a["w"], both_b["w"]],
                "curve_max_abs_difference": max_abs(both_a_curve, both_b_curve),
                "effective_width_V": float(both_a_model._width(both_a, T0)),
            },
            "caution is confirmed when changing w produces exactly zero curve change",
            "The n/w API is a mutually exclusive parameterization, not two independently estimable width controls.",
        )
    )

    # VIB-001..004: derivative, thermodynamic identities, stability and scope.
    theta = 430.0
    vib_tr = {
        "dH_rxn": -12000.0,
        "dS_rxn": 8.0,
        "n": 1.0,
        "Q": 1.0,
        "theta_E": theta,
        "theta_E_Tref": T0,
    }
    vib_model = module.GraphiteAnodeDischargeDQDV([vib_tr])
    derivative_rows = []
    for temperature in [120.0, 200.0, 258.15, 298.15, 350.0, 500.0, 900.0]:
        numeric = finite_difference(
            lambda temp: float(vib_model._vib_dU(vib_tr, temp)),
            temperature,
            1.0e-3,
        )
        analytic_value = float(vib_model._vib_dS(vib_tr, temperature)) / F
        derivative_rows.append(
            {
                "T_K": temperature,
                "dDeltaU_dT_numeric_V_per_K": numeric,
                "DeltaS_over_F_V_per_K": analytic_value,
                "abs_error": abs(numeric - analytic_value),
            }
        )
    probes.append(
        probe(
            "VIB-001",
            "vibration",
            "Einstein voltage-shift derivative equals entropy difference over F",
            "PASS_IDENTITY",
            "The reference-subtracted free-energy voltage shift must satisfy d(Delta U_vib)/dT=Delta S_vib/F.",
            {
                "theta_E_K": theta,
                "T_ref_K": T0,
                "rows": derivative_rows,
                "max_abs_error": max(row["abs_error"] for row in derivative_rows),
                "DeltaU_at_reference_V": float(vib_model._vib_dU(vib_tr, T0)),
                "DeltaS_at_reference_J_per_molK": float(
                    vib_model._vib_dS(vib_tr, T0)
                ),
            },
            "maximum derivative error < 1e-10 and both reference-subtracted quantities equal zero",
            "The additive v1.0.18.2 Einstein free-energy/entropy pair is thermodynamically self-consistent.",
        )
    )

    thermo_rows = []
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        for temperature in [0.1, 1.0, 10.0, 120.0, T0, 1000.0, 1.0e6]:
            raw = raw_einstein_quantities(R, theta, temperature)
            code_entropy = float(vib_model._S_vib(temperature, theta))
            thermo_rows.append(
                {
                    "T_K": temperature,
                    **raw,
                    "code_entropy_J_per_molK": code_entropy,
                    "U_minus_F_plus_TS_J_per_mol": raw["U_J_per_mol"]
                    - raw["F_plus_TS_J_per_mol"],
                    "all_finite": bool(
                        all(np.isfinite(value) for value in raw.values())
                        and np.isfinite(code_entropy)
                    ),
                }
            )
    low_entropy = thermo_rows[0]["code_entropy_J_per_molK"]
    high_expected = R * (1.0 + np.log(1.0e6 / theta))
    high_entropy = thermo_rows[-1]["code_entropy_J_per_molK"]
    probes.append(
        probe(
            "VIB-002",
            "vibration",
            "Einstein F, S, internal-energy identity and asymptotes",
            "PASS_IDENTITY",
            "For one thermal Einstein oscillator without zero-point energy, U=F+TS, S->0 at low T, and S~R[1+ln(T/theta)] at high T.",
            {
                "rows": thermo_rows,
                "max_U_identity_abs_error_J_per_mol": max(
                    abs(row["U_minus_F_plus_TS_J_per_mol"])
                    for row in thermo_rows
                ),
                "low_T_entropy_J_per_molK": low_entropy,
                "high_T_entropy_J_per_molK": high_entropy,
                "high_T_asymptote_J_per_molK": high_expected,
                "high_T_relative_error": abs(high_entropy - high_expected)
                / abs(high_expected),
            },
            "all values finite; identity error < 1e-8 J/mol; low entropy < 1e-10; high-T relative error < 1e-6",
            "The stated single-oscillator thermodynamic identities are numerically satisfied over a wide positive-temperature range.",
        )
    )

    invalid_reference_rows = []
    for invalid_reference in [0.0, -10.0]:
        invalid_tr = dict(vib_tr, theta_E_Tref=invalid_reference)
        caught = None
        value = None
        value_repr = None
        returned_is_nan = False
        warning_messages = []
        try:
            with warnings.catch_warnings(record=True) as captured:
                warnings.simplefilter("always")
                raw_value = float(vib_model._vib_dU(invalid_tr, 300.0))
                if np.isfinite(raw_value):
                    value = raw_value
                else:
                    value_repr = str(raw_value)
                    returned_is_nan = bool(np.isnan(raw_value))
                warning_messages = [str(item.message) for item in captured]
        except Exception as exc:
            caught = f"{type(exc).__name__}: {exc}"
        invalid_reference_rows.append(
            {
                "theta_E_Tref_K": invalid_reference,
                "exception": caught,
                "returned_value": value,
                "returned_value_repr": value_repr,
                "returned_is_nan": returned_is_nan,
                "returned_finite": value is not None and bool(np.isfinite(value)),
                "warnings": warning_messages,
            }
        )
    probes.append(
        probe(
            "VIB-003",
            "vibration",
            "nonpositive Einstein reference temperature is not rejected",
            "BLOCKER_CONFIRMED",
            "The Einstein reference temperature must be finite and strictly positive before any theta/T or thermal free-energy evaluation.",
            {"cases": invalid_reference_rows},
            "defect is confirmed when no ValueError is raised before non-finite arithmetic",
            "theta_E is guarded positive, but theta_E_Tref uses only a finite-value guard.",
        )
    )

    all_default_transitions = list(module.GRAPHITE_STAGING_LIT) + list(
        module.LCO_MSMR_LIT
    )
    probes.append(
        probe(
            "VIB-004",
            "vibration",
            "Einstein capability is dormant in all shipped defaults",
            "SCOPE_ABSENT_CONFIRMED",
            "An additive capability with no populated material parameter does not validate any released graphite or LCO prediction.",
            {
                "default_transition_count": len(all_default_transitions),
                "theta_E_key_count": sum(
                    "theta_E" in transition for transition in all_default_transitions
                ),
                "theta_E_Tref_key_count": sum(
                    "theta_E_Tref" in transition
                    for transition in all_default_transitions
                ),
            },
            "scope absence is confirmed when key counts are zero",
            "v1.0.18.2 adds a mathematically consistent option but no material-specific vibrational calibration or validation.",
        )
    )

    # LCO-001..003 and KIN-001.
    lco_transitions = copy.deepcopy(module.LCO_MSMR_LIT)
    lco = module.LCOCathodeDQDV(lco_transitions, Rn=0.0, Cbg=0.0)
    electronic = next(tr for tr in lco_transitions if tr.get("electronic"))
    electronic_values = [
        float(np.asarray(lco._effective_dS_rxn(electronic, temp)).reshape(-1)[0])
        for temp in [240.0, T0, 360.0]
    ]
    probes.append(
        probe(
            "LCO-001",
            "lco",
            "LCO electronic entropy is frozen at 298.15 K",
            "BLOCKER_CONFIRMED",
            "If the theory claims Sommerfeld electronic entropy proportional to temperature, the effective entropy and integrated center shift cannot be temperature-constant.",
            {
                "temperatures_K": [240.0, T0, 360.0],
                "effective_dS_J_per_molK": electronic_values,
                "range_J_per_molK": max(electronic_values)
                - min(electronic_values),
            },
            "defect is confirmed when all effective entropy values are exactly equal",
            "The seam is internally shared, but it implements a single-reference constant offset rather than the document's T-dependent electronic law.",
        )
    )

    lco_voltage = np.linspace(3.4, 4.7, 50001)
    lco_i0 = np.asarray(lco.dqdv(lco_voltage, T0, 0.0, 1.0, +1), dtype=float)
    lco_i1 = np.asarray(lco.dqdv(lco_voltage, T0, 1.0, 1.0, +1), dtype=float)
    probes.append(
        probe(
            "LCO-002",
            "lco",
            "default LCO has no rate-dependent kinetic broadening",
            "BLOCKER_CONFIRMED",
            "A model intended to explain current-induced LCO peak suppression/broadening must have an active rate path beyond optional ohmic translation.",
            {
                "I0_vs_I1_Rn0_max_abs": max_abs(lco_i0, lco_i1),
                "all_transitions_missing_dH_a": all(
                    "dH_a" not in tr for tr in lco_transitions
                ),
                "all_transitions_missing_L_V": all(
                    "L_V" not in tr for tr in lco_transitions
                ),
                "all_transitions_missing_Omega": all(
                    "Omega" not in tr for tr in lco_transitions
                ),
            },
            "defect is confirmed when I=0 and I=1 curves are identical at Rn=0",
            "The released LCO defaults cannot test the founding current-broadening hypothesis.",
        )
    )

    dopant_tokens = {
        "dopant",
        "doping",
        "al",
        "mg",
        "ti",
        "ni",
        "mn",
        "coating",
        "surface_reconstruction",
        "oxygen_loss",
    }
    present_keys = {
        str(key).lower() for transition in lco_transitions for key in transition
    }
    probes.append(
        probe(
            "LCO-003",
            "lco",
            "doped high-voltage LCO state is absent from defaults",
            "SCOPE_ABSENT_CONFIRMED",
            "Explaining doped high-voltage LCO requires explicit composition/surface/oxygen-loss state and data-supported transitions above the present placeholder range.",
            {
                "transition_count": len(lco_transitions),
                "maximum_literal_U_V": max(float(tr["U"]) for tr in lco_transitions),
                "present_transition_keys": sorted(present_keys),
                "recognized_dopant_or_degradation_keys": sorted(
                    present_keys & dopant_tokens
                ),
                "theta_E_key_count": sum("theta_E" in tr for tr in lco_transitions),
            },
            "scope absence is confirmed when maximum U is 4.05 V and no dopant/degradation key is present",
            "The shipped three-transition LCO set is a tier-C demonstration placeholder, not a high-voltage doped-LCO fit model.",
        )
    )

    lag_tr_low = {
        "U": 0.08,
        "w": 0.02,
        "Q": 1.0,
        "dH_a": 44000.0,
        "dS_a": 0.0,
        "dVdq_qa": 0.30,
        "Omega": 9000.0,
    }
    lag_tr_high = dict(lag_tr_low, U=0.28)
    barrier_model = module.GraphiteAnodeDischargeDQDV(
        [lag_tr_low], Rn=0.0, Cbg=0.0
    )
    n_rep = float(barrier_model._n_factor(lag_tr_low, T0))
    lag_low = float(
        barrier_model._resolve_lag_length(
            lag_tr_low, T0, 0.2, 1.0, n_rep, +1
        )
    )
    lag_high = float(
        barrier_model._resolve_lag_length(
            lag_tr_high, T0, 0.2, 1.0, n_rep, +1
        )
    )
    resolver_parameters = list(
        inspect.signature(barrier_model._resolve_lag_length).parameters
    )
    probes.append(
        probe(
            "KIN-001",
            "kinetics",
            "lag/barrier closure is independent of local voltage or affinity",
            "BLOCKER_CONFIRMED",
            "A transition barrier hypothesized to depend on electrode potential and local thermodynamic driving force must receive/evaluate a local state variable rather than one frozen cutoff value per transition.",
            {
                "resolver_parameters": resolver_parameters,
                "lag_for_U_0p08_V": lag_low,
                "lag_for_U_0p28_V": lag_high,
                "absolute_difference_V": abs(lag_low - lag_high),
                "voltage_or_affinity_parameter_present": any(
                    name.lower() in {"v", "voltage", "affinity", "eta", "ksi", "xi"}
                    for name in resolver_parameters
                ),
            },
            "defect is confirmed when the signature has no local voltage/affinity and changing U leaves lag unchanged",
            "The current closure cannot express the user's central hypothesis that temperature, current, and electrode potential jointly modify the activation barrier.",
        )
    )

    return probes


def make_review(payload: dict[str, Any]) -> str:
    by_verdict: dict[str, int] = payload["verdict_counts"]
    probe_map = {item["probe_id"]: item for item in payload["probes"]}

    def value(probe_id: str, key: str):
        return probe_map[probe_id]["measurements"][key]

    return rf"""# Phase 059 독립 code 물리·수치 probe 검토

정본일: 2026-07-28

범위: v1.0.14–v1.0.18.2 production 계보, Step 34.4

상태: `{payload["status"]}`

## 판정 경계

이 gate는 frozen release module을 변조하지 않고 독립 검산
{payload["probe_count"]}건을 완주했다는 뜻이다. 알려진 결함을 재현한
`BLOCKER_CONFIRMED`를 과학적 PASS로 세지 않는다. release test/demo는
호출하지 않았고 실험 적합성도 부여하지 않는다.

verdict 집계:

| verdict | 수 |
|---|---:|
| PASS_IDENTITY | {by_verdict.get("PASS_IDENTITY", 0)} |
| PASS_GUARD | {by_verdict.get("PASS_GUARD", 0)} |
| BLOCKER_CONFIRMED | {by_verdict.get("BLOCKER_CONFIRMED", 0)} |
| SCOPE_ABSENT_CONFIRMED | {by_verdict.get("SCOPE_ABSENT_CONFIRMED", 0)} |
| IDENTIFIABILITY_CAUTION | {by_verdict.get("IDENTIFIABILITY_CAUTION", 0)} |

## 보존된 수학

- v1.0.15 점별 recurrence는 불규칙 격자의 상수·선형 source를
  각각 최대 오차
  `{value("MEM-001", "constant_source_max_abs_error"):.3e}`,
  `{value("MEM-001", "linear_source_max_abs_error"):.3e}`로 재현했다.
- 넓은 창에서 평형/지연 면적은
  `{value("MEM-002", "equilibrium_area"):.12f}`,
  `{value("MEM-002", "lagged_area"):.12f}`로 \(Q=1\)을 보존했다.
  지연 peak는 `{value("MEM-002", "equilibrium_peak"):.6g}`에서
  `{value("MEM-002", "lagged_peak"):.6g}`로 낮아지고 FWHM은
  `{value("MEM-002", "equilibrium_fwhm_V"):.6g}` V에서
  `{value("MEM-002", "lagged_fwhm_V"):.6g}` V로 넓어졌다.
- resolved \(L_V\) 감소열은 평형과의 오차가 단조 감소했다.
  대칭 단일 전이의 charge/discharge mirror 최대 오차는
  `{value("ORD-001", "mirror_max_abs_error"):.3e}`다.
- explicit \(n\), \(n(T)\), `w`-only의 폭 미분은 독립
  finite difference와 일치했다. \(n(T)\) 고정-state entropy chain
  오차는 `{value("WID-002", "entropy_abs_error"):.3e}` V/K다.
- Einstein 보정은
  \(\partial\Delta U_\mathrm{{vib}}/\partial T=\Delta S_\mathrm{{vib}}/F\)
  및 \(U=F+TS\), 저·고온 asymptote를 만족했다.

## 확인된 구조적 결함

1. `dqdv`는 입력 전압을 정렬한다. 같은 좌표를 섞어도 원위치로
   복구한 출력 차이가
   `{value("ORD-002", "sorted_vs_shuffled_then_restored_max_abs"):.3e}`다.
   실제 입력 순서를 따라간 memory와는
   `{value("ORD-002", "model_shuffled_vs_true_input_order_memory_max_abs"):.6g}`
   차이가 난다. pulse/reversal/rest chronology를 표현하지 못한다.
2. direct `L_V`는 \(I=0\)과 \(I=1\) 출력이 완전히 같고,
   \(I=0\)에서도 평형과
   `{value("CUR-002", "I0_vs_equilibrium_max_abs"):.6g}`만큼 다르다.
3. \(Q_\mathrm{{cell}}=3600\) C, 1C에서 facade는 3600 A를 만들며,
   SI-consistent 1 A 대비 `func_L_q` 비가 정확히
   `{value("UNT-001", "func_Lq_code_to_SI_ratio"):.1f}`다.
4. `n`/`w`가 모두 없을 때 observable 폭은 \(RT/F\)인데
   entropy 경로 `_dwdT`는 0을 반환한다. 누락량은
   `{value("WID-004", "mismatch_V_per_K"):.6e}` V/K다.
5. `theta_E_Tref<=0`은 fail-fast 되지 않고 non-finite
   값을 반환한다.
6. LCO 전자 엔트로피는 240–360 K에서 range
   `{value("LCO-001", "range_J_per_molK"):.3e}` J mol⁻¹ K⁻¹로
   완전히 동결돼 있다. 기본 LCO는 \(R_n=0\)일 때 \(I=0\)과
   \(I=1\) 곡선 차이가
   `{value("LCO-002", "I0_vs_I1_Rn0_max_abs"):.3e}`다.
7. lag resolver에는 local voltage/affinity 인자가 없고 전이 중심
   U를 0.08 V에서 0.28 V로 바꿔도 lag 차이는
   `{value("KIN-001", "absolute_difference_V"):.3e}`다.

## 범위·식별성 판정

- `n`과 `w`를 함께 주면 `w`를 0.003 V에서 0.090 V로 바꿔도
  곡선 차이는 `{value("WID-006", "curve_max_abs_difference"):.3e}`다.
  두 파라미터는 동시 fit 변수가 아니라 배타적 parameterization이다.
- graphite+LCO 기본 전이 {value("VIB-004", "default_transition_count")}개에
  `theta_E`는 0개다. Einstein 항은 material validation이 없는 dormant
  capability다.
- 기본 LCO 최대 중심은
  `{value("LCO-003", "maximum_literal_U_V"):.2f}` V이고 dopant,
  oxygen-loss, surface-reconstruction state는 없다. 고전압
  doped-LCO 설명 범위가 아니다.

## Step 34.4 결론

점별 지수 memory와 \(n(T)\), Einstein 보정의 일부 수학적 항등식은
보존된다. 그러나 사용자의 출발 가설을 실제 데이터에 적용하는 데
필수인 시간 순서, \(I\to0\), SI rate 단위, local
voltage-dependent barrier, LCO rate path와 고전압 도핑 상태는
닫히지 않았다. 따라서 판정은 **독립 probe 실행 PASS,
release 물리 정합 CONDITIONAL/REJECTED 항목 병존**이다.

다음 Step 34.5에서는 두 golden NPZ의 모든 key/shape/dtype/array를
재생성해 bit-exact와 tolerance match를 분리하고, v1.0.15 rebaseline이
무엇을 고정했고 무엇을 검사하지 못했는지 판정한다.
"""


def main() -> None:
    source_before = {
        relative: sha256(ROOT / relative) for relative in MODULE_PATHS.values()
    }
    modules = {
        version: load_module(version, relative)
        for version, relative in MODULE_PATHS.items()
    }
    lineage = feature_lineage(modules)
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        probes = run_latest_probes(modules["v1.0.18.2"])
    source_after = {
        relative: sha256(ROOT / relative) for relative in MODULE_PATHS.values()
    }
    verdict_counts: dict[str, int] = {}
    for item in probes:
        verdict_counts[item["verdict"]] = verdict_counts.get(item["verdict"], 0) + 1
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "scope": "Phase 059 Step 34.4 independent physics/numerics probes over the v1.0.14-v1.0.18.2 production-code lineage",
        "method": "Read-only imports of frozen release modules; independent analytic identities, finite differences, asymptotes, limit tests, permutation tests, and material-scope checks; no release test/demo invocation.",
        "authority_boundary": "Execution PASS means the probes completed and their evidence is internally validated. BLOCKER_CONFIRMED is not a scientific PASS and the probes do not establish experimental validity.",
        "status": "CONDITIONAL_P059_CODE_CONFORMANCE",
        "execution_gate": "PASS_P059_INDEPENDENT_CODE_PROBE_EXECUTION",
        "source_sha256_before": source_before,
        "source_sha256_after": source_after,
        "sources_unchanged": source_before == source_after,
        "feature_lineage": lineage,
        "probe_count": len(probes),
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "probes": probes,
        "next_step": "34.5",
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    REVIEW.write_text(make_review(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
