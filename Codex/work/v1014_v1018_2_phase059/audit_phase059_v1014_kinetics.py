#!/usr/bin/env python3
"""Audit v1.0.14 kinetics, barrier, and low-T x finite-current broadening."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CH1 = ROOT / "Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex"
CODE = ROOT / "Claude/docs/v1.0.14/Anode_Fit_v1.0.14.py"
V1010_CODE = ROOT / "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py"
OUTPUT = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md"

F = 96485.33212
R = 8.31446261815324
KB = 1.380649e-23
PLANCK = 6.62607015e-34


PRIMARY_SOURCES = [
    {
        "id": "EYRING_1935",
        "title": "The Activated Complex in Chemical Reactions",
        "doi": "10.1063/1.1749604",
        "url": "https://doi.org/10.1063/1.1749604",
        "verified_claim": (
            "Transition-state theory obtains an absolute molecular reaction "
            "rate from the statistical probability of an activated state "
            "and its decomposition frequency."
        ),
        "audit_effect": (
            "The kBT/h prefactor is a molecular transition-state result. "
            "Promoting it directly to an electrode-scale phase-fraction "
            "relaxation rate requires a coarse-graining derivation."
        ),
    },
    {
        "id": "BAZANT_2013",
        "title": (
            "Theory of Chemical Kinetics and Charge Transfer based on "
            "Nonequilibrium Thermodynamics"
        ),
        "doi": "10.1021/ar300145c",
        "url": "https://doi.org/10.1021/ar300145c",
        "verified_claim": (
            "Reaction rates in concentrated and phase-separating solids "
            "depend on local activities, reaction free energy, transition-"
            "state activity, gradients, strain, and electrochemical state."
        ),
        "audit_effect": (
            "It supports local thermodynamically consistent kinetics, not "
            "a voltage-independent affinity frozen at an arbitrary peak cut."
        ),
    },
    {
        "id": "FLY_CHEN_2020",
        "title": (
            "Rate dependency of incremental capacity analysis (dQ/dV) as "
            "a diagnostic tool for lithium-ion batteries"
        ),
        "doi": "10.1016/j.est.2020.101329",
        "url": "https://doi.org/10.1016/j.est.2020.101329",
        "data_url": "https://doi.org/10.17028/rd.lboro.7637921",
        "verified_claim": (
            "In commercial NCA/graphite and LFP/graphite full cells, "
            "increasing rate lowers, broadens, shifts, and can erase ICA "
            "peaks; resistance and diffusion effects motivate low-rate ICA."
        ),
        "audit_effect": (
            "The user's finite-current target is experimentally supported, "
            "but the full-cell experiment does not identify a unique "
            "single-exponential electrode transition mechanism."
        ),
    },
    {
        "id": "GISMERO_2023",
        "title": (
            "The Influence of Testing Conditions on State of Health "
            "Estimations of Electric Vehicle Lithium-Ion Batteries Using "
            "an Incremental Capacity Analysis"
        ),
        "doi": "10.3390/batteries9120568",
        "url": "https://doi.org/10.3390/batteries9120568",
        "verified_claim": (
            "For graphite/NMC532 cells, lower temperature or higher charge "
            "rate flattens and broadens selected IC peaks and increases "
            "polarization; features can merge or vanish."
        ),
        "audit_effect": (
            "This independently confirms the joint low-temperature and "
            "finite-current target, while also showing feature-specific and "
            "full-cell behavior beyond a universal one-tail model."
        ),
    },
    {
        "id": "PERSSON_PRB_2010",
        "title": (
            "Thermodynamic and kinetic properties of the Li-graphite system "
            "from first-principles calculations"
        ),
        "doi": "10.1103/PhysRevB.82.125416",
        "url": "https://doi.org/10.1103/PhysRevB.82.125416",
        "open_record": (
            "https://ets.lbl.gov/publications/"
            "thermodynamic-and-kinetic-properties"
        ),
        "verified_claim": (
            "The study calculates Li migration barriers and bulk "
            "composition-dependent diffusivity in stage-I and stage-II "
            "graphite."
        ),
        "audit_effect": (
            "A bulk migration barrier is not by itself an electrode-scale "
            "phase-transition relaxation enthalpy or exchange-current law."
        ),
    },
    {
        "id": "PERSSON_JPCL_2010",
        "title": "Lithium Diffusion in Graphitic Carbon",
        "doi": "10.1021/jz100188d",
        "url": "https://doi.org/10.1021/jz100188d",
        "verified_claim": (
            "Experiment and first-principles analysis show strongly "
            "anisotropic Li transport: fast in-plane bulk diffusion and "
            "much slower grain-boundary transport."
        ),
        "audit_effect": (
            "Transport pathways and geometry must be coarse-grained before "
            "a measured dQ/dV relaxation time can be assigned to one barrier."
        ),
    },
    {
        "id": "DOYLE_FULLER_NEWMAN_1993",
        "title": (
            "Modeling of Galvanostatic Charge and Discharge of the "
            "Lithium/Polymer/Insertion Cell"
        ),
        "doi": "10.1149/1.2221597",
        "url": "https://doi.org/10.1149/1.2221597",
        "open_record": "https://www.osti.gov/biblio/6108611",
        "verified_claim": (
            "A galvanostatic insertion-cell forward model couples "
            "concentrated-solution transport, solid diffusion, reaction, "
            "and active-material utilization under the imposed current."
        ),
        "audit_effect": (
            "A prescribed voltage-grid convolution can be a reduced "
            "observation model, but it is not a closed galvanostatic "
            "electrochemical forward model without current balance and "
            "terminal-voltage closure."
        ),
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_line(text: str, marker: str) -> int:
    return next(
        index for index, line in enumerate(text.splitlines(), 1) if marker in line
    )


def normalized_function_hashes(path: Path) -> dict[str, str]:
    """Hash executable AST while ignoring function docstrings and line numbers."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions: dict[str, str] = {}

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
            functions[node.name] = digest(node)
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    functions[f"{node.name}.{child.name}"] = digest(child)
    return functions


def profile_metrics(axis: np.ndarray, signal: np.ndarray) -> dict[str, float]:
    x = np.asarray(axis, dtype=float)
    y = np.asarray(signal, dtype=float)
    peak_index = int(np.argmax(y))
    peak = float(y[peak_index])
    half = 0.5 * peak

    left_candidates = np.flatnonzero(y[: peak_index + 1] <= half)
    if left_candidates.size:
        left_index = int(left_candidates[-1])
        left_x = float(
            np.interp(
                half,
                [y[left_index], y[left_index + 1]],
                [x[left_index], x[left_index + 1]],
            )
        )
    else:
        left_x = float(x[0])

    right_candidates = np.flatnonzero(y[peak_index:] <= half)
    if right_candidates.size:
        right_index = peak_index + int(right_candidates[0])
        if right_index == peak_index:
            right_x = float(x[right_index])
        else:
            right_x = float(
                np.interp(
                    half,
                    [y[right_index], y[right_index - 1]],
                    [x[right_index], x[right_index - 1]],
                )
            )
    else:
        right_x = float(x[-1])

    return {
        "area": float(np.trapezoid(y, x)),
        "peak_height": peak,
        "peak_voltage": float(x[peak_index]),
        "fwhm_V": right_x - left_x,
    }


def causal_continuum_profile(
    axis: np.ndarray, equilibrium_progress: np.ndarray, lag_length: float
) -> np.ndarray:
    """High-resolution causal solve used only as an existence/limit probe."""
    x = np.asarray(axis, dtype=float)
    target = np.asarray(equilibrium_progress, dtype=float)
    if lag_length <= 0.0:
        return np.gradient(target, x)
    step = float(x[1] - x[0])
    rho = math.exp(-step / lag_length)
    lagged = np.empty_like(target)
    lagged[0] = target[0]
    for index in range(1, target.size):
        lagged[index] = (
            rho * lagged[index - 1] + (1.0 - rho) * target[index]
        )
    return (target - lagged) / lag_length


def source_contracts(ch1: str, code: str) -> dict[str, Any]:
    return {
        "line_counts": {
            "chapter_1": len(ch1.splitlines()),
            "production_code": len(code.splitlines()),
            "v1010_production_code": len(
                V1010_CODE.read_text(encoding="utf-8").splitlines()
            ),
        },
        "chapter_1_lines": {
            "constant_current_transform": first_line(ch1, "\\label{eq:Lq}"),
            "frozen_cut_affinity": first_line(ch1, "\\label{eq:Acut}"),
            "omega_barrier": first_line(ch1, "\\label{eq:dHeff}"),
            "lag_voltage_transform": first_line(ch1, "\\label{eq:LV}"),
            "frozen_local_derivative": first_line(
                ch1, "\\partial\\ln L_q/\\partial V=0"
            ),
            "causal_memory": first_line(ch1, "\\label{eq:memory}"),
            "grid_branch": first_line(ch1, "\\label{eq:branch}"),
            "default_dormant_statement": first_line(
                ch1, "$L_{V,j}$ 는 $10^{-10}$--$10^{-8}$ V"
            ),
        },
        "code_lines": {
            "func_L_q": first_line(code, "def func_L_q"),
            "causal_lowpass": first_line(code, "def _causal_lowpass"),
            "omega_barrier": first_line(code, "def func_dH_a_eff"),
            "lag_resolver": first_line(code, "def _resolve_lag_length"),
            "direct_lag_override": first_line(
                code, "L_V_override = transition.get('L_V')"
            ),
            "frozen_affinity": first_line(
                code, "A = float(min(z_cut * n_safe * R * T"
            ),
            "nonfinite_lag_to_equilibrium": first_line(
                code, "if not np.isfinite(L_q):"
            ),
            "mean_temperature_lag": first_line(code, "T_rep = float(np.mean"),
            "voltage_sorting": first_line(code, "sort_idx = np.argsort"),
            "grid_switch": first_line(
                code, "lag_len_V < self.min_lag_grid_steps * grid_step"
            ),
            "curve_hour_rate": first_line(
                code, "c_rate    : C-rate [1/h]"
            ),
            "curve_current_conversion": first_line(
                code, "I_use = c * Q_cell"
            ),
        },
        "explicit_dual_capacity_unit_contract": (
            "C(또는 A\\,h)" in ch1
            and "[1/h]$\\cdot$[A\\,h]$\\to$[A]" in ch1
        ),
        "frozen_affinity_is_admitted": (
            "\\partial\\ln L_q/\\partial V=0" in ch1
        ),
        "grid_discontinuity_is_admitted": (
            "\\sim23\\%" in ch1 and "불연속" in ch1
        ),
        "default_current_broadening_is_admitted_absent": (
            "$L_{V,j}$ 는 $10^{-10}$--$10^{-8}$ V" in ch1
        ),
        "code_has_current_partition_solver": any(
            token in code
            for token in (
                "current_partition",
                "solve_current",
                "I_transition",
                "I_j",
            )
        ),
        "code_has_local_affinity_state": (
            "1-2*ksi" in code
            or "1.0 - 2.0 * ksi" in code
            or "local_affinity" in code
        ),
        "code_has_time_domain_state_integrator": (
            "solve_ivp" in code or "dksi_dt" in code or "d_xi_dt" in code
        ),
    }


def lineage_contract() -> dict[str, Any]:
    old_hashes = normalized_function_hashes(V1010_CODE)
    new_hashes = normalized_function_hashes(CODE)
    core = [
        "func_L_q",
        "_causal_lowpass",
        "func_dH_a_eff",
        "GraphiteAnodeDischargeDQDV._resolve_lag_length",
    ]
    comparison = {
        name: {
            "v1010_hash": old_hashes[name],
            "v1014_hash": new_hashes[name],
            "executable_ast_equal": old_hashes[name] == new_hashes[name],
        }
        for name in core
    }
    return {
        "core_functions": comparison,
        "all_core_functions_executable_ast_equal": all(
            item["executable_ast_equal"] for item in comparison.values()
        ),
        "dqdv_ast_equal": (
            old_hashes["GraphiteAnodeDischargeDQDV.dqdv"]
            == new_hashes["GraphiteAnodeDischargeDQDV.dqdv"]
        ),
        "dqdv_change_scope": (
            "v1.0.14 adds a degenerate-span/scalar-input equilibrium guard; "
            "the finite-array lag law and grid switch remain."
        ),
    }


def numerical_rederivation(module) -> dict[str, Any]:
    temperature_ref = 298.15
    c_rate = 0.1
    qdot_code_numeric = c_rate
    qdot_si_per_second = c_rate / 3600.0
    unit_ratio = qdot_code_numeric / qdot_si_per_second
    barrier_bias = R * temperature_ref * math.log(unit_ratio)

    cutoff_a = 4.0
    sigma_cut = 1.0 / (1.0 + math.exp(-cutoff_a))
    derivative_fraction = 4.0 * sigma_cut * (1.0 - sigma_cut)
    local_dlnL_dV = (
        F
        / (R * temperature_ref)
        * (1.0 / (1.0 + math.exp(cutoff_a)) - 0.5)
    )

    width_ref = R * temperature_ref / F
    dVdq = 0.30
    target_lq = width_ref / dVdq

    def barrier_for_target(qdot_per_second: float) -> float:
        prefactor = qdot_per_second * PLANCK / (KB * temperature_ref)
        return R * temperature_ref * (
            math.log(
                target_lq
                * (1.0 + math.exp(-cutoff_a))
                / prefactor
            )
            + 0.5 * cutoff_a
        )

    barrier_code = barrier_for_target(qdot_code_numeric)
    barrier_si = barrier_for_target(qdot_si_per_second)

    default_lags: dict[str, dict[str, list[float]]] = {}
    model = module.GraphiteAnodeDischargeDQDV(
        copy.deepcopy(module.GRAPHITE_STAGING_LIT),
        x=0.5,
        Rn=0.0,
        Cbg=0.0,
        use_dH_eff=True,
    )
    for temperature in (258.15, 298.15, 318.15):
        temperature_key = f"{temperature:.2f}"
        default_lags[temperature_key] = {}
        for rate in (0.1, 1.0):
            values = []
            for transition in model.transitions:
                values.append(
                    float(
                        model._resolve_lag_length(
                            transition,
                            temperature,
                            rate,
                            1.0,
                            1.0,
                            +1,
                        )
                    )
                )
            default_lags[temperature_key][f"{rate:.1f}C_numeric"] = values

    voltage = np.linspace(0.015, 0.27, 5001)
    transition = copy.deepcopy(module.GRAPHITE_STAGING_LIT[2])
    single_model = module.GraphiteAnodeDischargeDQDV(
        [transition],
        x=0.5,
        Rn=0.0,
        Cbg=0.0,
        use_dH_eff=True,
    )
    default_profiles: dict[str, dict[str, Any]] = {}
    for temperature in (258.15, 298.15, 318.15):
        low_rate = np.asarray(
            single_model.curve(
                voltage,
                direction="discharge",
                c_rate=0.1,
                Q_cell=1.0,
                T=temperature,
            ),
            dtype=float,
        )
        high_rate = np.asarray(
            single_model.curve(
                voltage,
                direction="discharge",
                c_rate=1.0,
                Q_cell=1.0,
                T=temperature,
            ),
            dtype=float,
        )
        default_profiles[f"{temperature:.2f}"] = {
            "low_rate_metrics": profile_metrics(voltage, low_rate),
            "high_rate_metrics": profile_metrics(voltage, high_rate),
            "max_abs_0p1C_vs_1C": float(np.max(np.abs(low_rate - high_rate))),
        }

    low_temp_metrics = default_profiles["258.15"]["high_rate_metrics"]
    room_temp_metrics = default_profiles["298.15"]["high_rate_metrics"]
    default_joint_ratios = {
        "lowT_to_roomT_peak_height": (
            low_temp_metrics["peak_height"] / room_temp_metrics["peak_height"]
        ),
        "lowT_to_roomT_fwhm": (
            low_temp_metrics["fwhm_V"] / room_temp_metrics["fwhm_V"]
        ),
        "default_lowT_is_taller": (
            low_temp_metrics["peak_height"] > room_temp_metrics["peak_height"]
        ),
        "default_lowT_is_narrower": (
            low_temp_metrics["fwhm_V"] < room_temp_metrics["fwhm_V"]
        ),
    }

    direct_model = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.12, "w": 0.014, "Q": 1.0, "L_V": 0.04}],
        x=0.5,
        Rn=0.0,
        Cbg=0.0,
    )
    direct_zero = np.asarray(
        direct_model.dqdv(voltage, 298.15, 0.0, 3600.0, s=+1),
        dtype=float,
    )
    direct_one = np.asarray(
        direct_model.dqdv(voltage, 298.15, 1.0, 3600.0, s=+1),
        dtype=float,
    )
    equilibrium_direct = np.asarray(
        direct_model.equilibrium(voltage, 298.15), dtype=float
    )
    direct_override = {
        "max_abs_I0_vs_I1": float(np.max(np.abs(direct_zero - direct_one))),
        "max_abs_I0_vs_equilibrium": float(
            np.max(np.abs(direct_zero - equilibrium_direct))
        ),
        "I0_metrics": profile_metrics(voltage, direct_zero),
        "equilibrium_metrics": profile_metrics(voltage, equilibrium_direct),
        "violates_zero_current_limit": bool(
            np.max(np.abs(direct_zero - equilibrium_direct)) > 1.0e-3
            and np.max(np.abs(direct_zero - direct_one)) < 1.0e-14
        ),
    }

    with np.errstate(over="ignore", invalid="ignore"):
        overflow_model = module.GraphiteAnodeDischargeDQDV(
            [
                {
                    "U": 0.12,
                    "w": 0.014,
                    "Q": 1.0,
                    "dH_a": 2.0e6,
                    "dS_a": 0.0,
                    "dVdq_qa": 0.30,
                }
            ],
            x=0.5,
            Rn=0.0,
            Cbg=0.0,
        )
        raw_overflow_lq = module.func_L_q(
            200.0,
            1.0,
            3600.0,
            2.0e6,
            0.0,
            0.5,
            4.0 * R * 200.0,
        )
        resolved_overflow_lag = overflow_model._resolve_lag_length(
            overflow_model.transitions[0],
            200.0,
            1.0,
            3600.0,
            1.0,
            +1,
        )
    overflow_contract = {
        "raw_Lq_is_positive_infinity": bool(np.isposinf(raw_overflow_lq)),
        "resolved_LV_V": float(resolved_overflow_lag),
        "physical_rate_limit": "k_to_zero_and_Lq_to_positive_infinity",
        "implementation_limit": "nonfinite_Lq_to_LV_zero_equilibrium",
        "physics_reversal_present": bool(
            np.isposinf(raw_overflow_lq) and resolved_overflow_lag == 0.0
        ),
    }

    nu = 2.0
    step_over_lag = 1.0 / nu
    rho = math.exp(-step_over_lag)
    discrete_area_fraction = (
        step_over_lag * rho / (1.0 - rho)
    )
    grid_handoff = {
        "min_lag_grid_steps": nu,
        "kinetic_branch_impulse_area_fraction_at_threshold": (
            discrete_area_fraction
        ),
        "equilibrium_branch_area_fraction": 1.0,
        "jump_fraction": 1.0 - discrete_area_fraction,
        "cause": (
            "endpoint ODE derivative is summed as a rectangle instead of "
            "using the exact cell-average state increment"
        ),
        "capacity_preserving_discrete_derivative": (
            "(xi_lag[i]-xi_lag[i-1])/DeltaV"
        ),
    }

    axis = np.linspace(-0.65, 0.65, 50001)
    activation_energy = 30_000.0
    slope = 0.30
    target_lag_to_width_ref = 0.50
    lag_ref = target_lag_to_width_ref * width_ref
    lq_ref = lag_ref / slope
    k_ref = qdot_si_per_second / lq_ref
    repair_profiles: dict[str, dict[str, Any]] = {}
    for temperature in (258.15, 298.15, 318.15):
        width = R * temperature / F
        equilibrium_progress = 1.0 / (
            1.0 + np.exp(-axis / width)
        )
        k_temperature = k_ref * math.exp(
            -activation_energy
            / R
            * (1.0 / temperature - 1.0 / temperature_ref)
        )
        lag = slope * qdot_si_per_second / k_temperature
        kinetic_profile = causal_continuum_profile(
            axis, equilibrium_progress, lag
        )
        equilibrium_profile = np.gradient(equilibrium_progress, axis)
        repair_profiles[f"{temperature:.2f}"] = {
            "width_V": width,
            "k_effective_per_s": k_temperature,
            "lag_V": lag,
            "lag_to_width": lag / width,
            "finite_current_metrics": profile_metrics(axis, kinetic_profile),
            "zero_current_metrics": profile_metrics(axis, equilibrium_profile),
        }

    repair_low = repair_profiles["258.15"]["finite_current_metrics"]
    repair_room = repair_profiles["298.15"]["finite_current_metrics"]
    repair_existence_proof = {
        "status": "REDUCED_MODEL_EXISTENCE_PROOF_NOT_MATERIAL_VALIDATION",
        "activation_energy_J_per_mol": activation_energy,
        "reference_k_effective_per_s": k_ref,
        "reference_lag_to_width": target_lag_to_width_ref,
        "profiles": repair_profiles,
        "lowT_to_roomT_finite_current_peak_height": (
            repair_low["peak_height"] / repair_room["peak_height"]
        ),
        "lowT_to_roomT_finite_current_fwhm": (
            repair_low["fwhm_V"] / repair_room["fwhm_V"]
        ),
        "joint_target_reproduced": bool(
            repair_low["peak_height"] < repair_room["peak_height"]
            and repair_low["fwhm_V"] > repair_room["fwhm_V"]
        ),
        "interpretation": (
            "A causal relaxation with a separately calibrated mesoscopic "
            "rate can reproduce the target qualitatively. This does not "
            "validate the v1.0.14 molecular prefactor, frozen affinity, "
            "constant voltage transform, or material parameters."
        ),
    }

    return {
        "unit_contract": {
            "c_rate_per_hour": c_rate,
            "code_numeric_qdot": qdot_code_numeric,
            "correct_qdot_per_second": qdot_si_per_second,
            "code_to_si_ratio": unit_ratio,
            "lag_length_overestimate_if_hour_rate_enters_second_TST": unit_ratio,
            "equivalent_barrier_bias_J_per_mol_at_298p15K": barrier_bias,
            "verdict": "FACTOR_3600_MIXED_HOUR_SECOND_CONTRACT",
        },
        "cut_affinity": {
            "default_A_over_RT": cutoff_a,
            "logistic_derivative_fraction_of_peak": derivative_fraction,
            "claimed_nominal_fraction": 0.05,
            "local_model_dlnL_dV_per_V_at_A4RT_chi0p5": local_dlnL_dV,
            "implemented_dlnL_dV_per_V": 0.0,
        },
        "barrier_scale_for_LV_equal_width": {
            "temperature_K": temperature_ref,
            "c_rate_per_hour": c_rate,
            "width_V": width_ref,
            "dVdq_V": dVdq,
            "target_Lq": target_lq,
            "code_hour_as_second_barrier_J_per_mol": barrier_code,
            "dimensionally_correct_barrier_J_per_mol": barrier_si,
            "difference_J_per_mol": barrier_si - barrier_code,
        },
        "default_lag_lengths_V": default_lags,
        "default_single_transition_profiles": default_profiles,
        "default_joint_ratios": default_joint_ratios,
        "direct_lag_override": direct_override,
        "overflow_contract": overflow_contract,
        "grid_handoff": grid_handoff,
        "repair_existence_proof": repair_existence_proof,
    }


def findings() -> list[dict[str, str]]:
    return [
        {
            "id": "KIN-059-01",
            "topic": "experimental_target",
            "disposition": "PRESERVE_TARGET_NOT_UNIQUE_MECHANISM",
            "reason": (
                "Primary full-cell data support lower, broader, shifted or "
                "vanishing peaks at higher rate and lower temperature, but "
                "do not identify a unique single-exponential electrode tail."
            ),
        },
        {
            "id": "KIN-059-02",
            "topic": "linear_relaxation_limit",
            "disposition": "PRESERVE_AS_REDUCED_CAUSAL_LIMIT",
            "reason": (
                "dξ/dt=k(ξeq-ξ) has the correct causal, area-preserving "
                "continuum limit when the equilibrium target and k are "
                "well-defined."
            ),
        },
        {
            "id": "KIN-059-03",
            "topic": "constant_current_unit_contract",
            "disposition": "REJECT_FACTOR_3600_DUAL_UNIT_API",
            "reason": (
                "The facade accepts C-rate in h^-1 and Ah-like capacity "
                "while func_L_q combines I/Q numerically with a seconds-based "
                "Eyring prefactor. Lq is 3600 times too large in that path."
            ),
        },
        {
            "id": "KIN-059-04",
            "topic": "galvanostatic_forward_closure",
            "disposition": "REJECT_AS_CLOSED_CONSTANT_CURRENT_MODEL",
            "reason": (
                "The code prescribes a voltage grid and filters equilibrium "
                "occupancy on it; it does not solve current balance, "
                "transition-current partition, transport, and terminal "
                "voltage under imposed current."
            ),
        },
        {
            "id": "KIN-059-05",
            "topic": "local_affinity",
            "disposition": "REJECT_FROZEN_CUT_AFFINITY",
            "reason": (
                "Default n=1 always selects A=4RT, so implemented "
                "d ln Lq/dV=0. The user's potential-dependent barrier "
                "hypothesis is removed from the computation."
            ),
        },
        {
            "id": "KIN-059-06",
            "topic": "nonideal_detailed_balance",
            "disposition": "REJECT_OMEGA_BARRIER_SHORTCUT",
            "reason": (
                "Subtracting χΩ from a common activation enthalpy changes "
                "the speed but leaves r+/r-=exp(Aideal/RT). It does not "
                "recover the regular-solution local chemical affinity."
            ),
        },
        {
            "id": "KIN-059-07",
            "topic": "migration_barrier_anchor",
            "disposition": "REJECT_AS_MACRO_RELAXATION_ENTHALPY",
            "reason": (
                "Persson studies support bulk Li migration and diffusion "
                "physics, not the direct assignment of those barriers to "
                "electrode-scale phase-fraction relaxation."
            ),
        },
        {
            "id": "KIN-059-08",
            "topic": "eyring_prefactor",
            "disposition": "REQUIRE_MESOSCOPIC_COARSE_GRAINING",
            "reason": (
                "kBT/h with a hop barrier omits active area, site density, "
                "nucleation population, phase-boundary mobility, particle "
                "geometry, diffusion, and porous-electrode transport."
            ),
        },
        {
            "id": "KIN-059-09",
            "topic": "default_current_broadening",
            "disposition": "FAIL_DORMANT_DEFAULT_PATH",
            "reason": (
                "All four default lag lengths remain below the grid switch "
                "for the audited rate/temperature range, so 0.1C and 1C "
                "single-transition shapes are identical when IR shift is "
                "removed."
            ),
        },
        {
            "id": "KIN-059-10",
            "topic": "low_temperature_finite_current_joint_limit",
            "disposition": "FAIL_USER_TARGET_ON_SHIPPED_DEFAULT",
            "reason": (
                "With the lag branch dormant, lower temperature only narrows "
                "the RT/F equilibrium width and raises the peak, opposite the "
                "target finite-current trend."
            ),
        },
        {
            "id": "KIN-059-11",
            "topic": "direct_lag_override",
            "disposition": "EMPIRICAL_ONLY_REQUIRE_PROTOCOL_SCALING",
            "reason": (
                "A direct L_V produces the same nonequilibrium curve at "
                "I=0 and I>0. It may be a nuisance kernel only if a protocol "
                "law forces L_V to zero with current and constrains T."
            ),
        },
        {
            "id": "KIN-059-12",
            "topic": "small_lag_numerics",
            "disposition": "REJECT_DISCONTINUOUS_GRID_HANDOFF",
            "reason": (
                "At the two-grid-step threshold the kinetic branch carries "
                "only 0.7707 of an impulse while the equilibrium branch "
                "carries one, causing a 22.9% fit-objective jump."
            ),
        },
        {
            "id": "KIN-059-13",
            "topic": "low_temperature_overflow",
            "disposition": "FAIL_NONFINITE_PHYSICS_REVERSAL",
            "reason": (
                "An infinite Lq from a vanishing rate is converted to L_V=0, "
                "which returns the equilibrium peak instead of a frozen "
                "transition."
            ),
        },
        {
            "id": "KIN-059-14",
            "topic": "nonisothermal_rate",
            "disposition": "REQUIRE_LOCAL_T_STATE_RATE",
            "reason": (
                "The lag is evaluated once at mean T and mean n; Arrhenius "
                "kinetics along a varying T(V) path is not implemented."
            ),
        },
        {
            "id": "KIN-059-15",
            "topic": "chronology",
            "disposition": "REQUIRE_MONOTONE_SEGMENT_OR_TIME_SOLVER",
            "reason": (
                "Sorting/interpolation by voltage discards revisits and "
                "protocol chronology. Hysteresis and memory require an "
                "explicit monotone-segment contract or time integration."
            ),
        },
        {
            "id": "KIN-059-16",
            "topic": "ohmic_polarization",
            "disposition": "PRESERVE_AS_SHIFT_NOT_BROADENING",
            "reason": (
                "For constant I and R, Vn=Vapp-sigma*IR shifts a peak but "
                "cannot change its width or height."
            ),
        },
        {
            "id": "KIN-059-17",
            "topic": "parameter_identifiability",
            "disposition": "REQUIRE_MULTI_T_MULTI_RATE_RELAXATION_DATA",
            "reason": (
                "One curve cannot separate equilibrium width, heterogeneity, "
                "charge transfer, diffusion, phase motion, IR, observation "
                "smoothing, activation enthalpy, and activation entropy."
            ),
        },
        {
            "id": "KIN-059-18",
            "topic": "v1010_to_v1014_lineage",
            "disposition": "BLOCKERS_CARRIED_FORWARD",
            "reason": (
                "The executable AST of func_L_q, _causal_lowpass, "
                "func_dH_a_eff, and _resolve_lag_length is unchanged from "
                "v1.0.10 to v1.0.14."
            ),
        },
        {
            "id": "KIN-059-19",
            "topic": "mechanism_existence",
            "disposition": "PRESERVE_QUALITATIVE_EXISTENCE_PROOF",
            "reason": (
                "A dimensionally consistent causal reduced model with a "
                "separately calibrated mesoscopic Arrhenius rate can "
                "qualitatively reproduce low-T peak suppression/broadening."
            ),
        },
        {
            "id": "KIN-059-20",
            "topic": "repair_architecture",
            "disposition": "REPLACE_WITH_SIGNED_TIME_DOMAIN_STATE_MODEL",
            "reason": (
                "Use one free-energy state definition, local affinity and "
                "transition-state law, current conservation, material/host "
                "states, transport, and a separate observation operator."
            ),
        },
    ]


def repair_contract() -> dict[str, list[str]]:
    return {
        "theory_manuscript_physics_only": [
            "Define the written lithiation/delithiation reaction and signed current.",
            "Derive equilibrium chemical potentials from one host free energy.",
            "Derive local affinity from electrochemical potentials, composition, phase fraction, stress, and temperature.",
            "Derive forward and reverse rates from one transition-state free energy and verify detailed balance.",
            "Separate charge transfer, solid diffusion, nucleation/phase-boundary motion, porous transport, and ohmic loss by controlled reductions.",
            "Derive the low-current equilibrium limit and the low-temperature x finite-current competition without numerical grid language.",
            "State that measured ICA broadening is a convolution of physical dynamics, heterogeneity, and observation response.",
        ],
        "code_conformance_after_theory_freeze": [
            "Use seconds, amperes, and coulombs internally; convert Ah and h^-1 once at the API boundary.",
            "Integrate signed state evolution in time or normalized charge while enforcing sum_j I_j plus background equals applied current.",
            "Solve terminal potential or overpotential self-consistently rather than prescribing a voltage convolution as galvanostatic closure.",
            "Evaluate local T, composition, activity, overpotential, and phase state at every integration point.",
            "Represent microscopic diffusion parameters and mesoscopic transformation rates as distinct typed quantities.",
            "Use a continuous, capacity-preserving small-lag discretization and treat k->0 as a frozen-state limit.",
            "Keep direct L_V only in the observation/nuisance layer and force it to zero at zero current.",
        ],
        "validation_ladder": [
            "Analytic ideal-site and regular-solution equilibrium limits.",
            "Detailed-balance and nonnegative-entropy-production tests.",
            "I->0, T sweeps, k->0, k->infinity, and grid-convergence tests.",
            "Single-transition synthetic recovery before multi-transition fitting.",
            "Graphite and LCO half-cell multi-temperature, multi-rate, GITT/rest, and impedance constraints.",
            "Full-cell validation only after host current partition and electrode balancing are fixed.",
            "Public-data holdout with peak position, height, FWHM, area, and voltage residual metrics.",
        ],
    }


def render_report(data: dict[str, Any]) -> str:
    numeric = data["numerical_rederivation"]
    unit = numeric["unit_contract"]
    cutoff = numeric["cut_affinity"]
    barrier = numeric["barrier_scale_for_LV_equal_width"]
    joint = numeric["default_joint_ratios"]
    override = numeric["direct_lag_override"]
    grid = numeric["grid_handoff"]
    overflow = numeric["overflow_contract"]
    proof = numeric["repair_existence_proof"]
    lines = [
        "# Phase 059 v1.0.14 kinetics·barrier·저온×유한전류 독립 재유도",
        "",
        "정본일: 2026-07-28",
        "",
        (
            "판정: "
            "`CONDITIONAL_P059_V1014_KINETIC_SKELETON_PRESERVED_BUT_"
            "CONSTANT_CURRENT_LOCAL_BARRIER_AND_JOINT_LIMIT_FAIL`"
        ),
        "",
        "## 결론",
        "",
        "다음 최소 골격은 보존할 가치가 있다.",
        "",
        "- `dξ/dt = k(ξ_eq-ξ)`의 1차 인과 완화",
        "- 같은 단위계에서 `L_q=|I|/(Q_scale k)`",
        "- 국소 선형화가 유효할 때 `L_V=|dV/dq|L_q`",
        "- 연속계에서 유한 `L_V`가 peak를 낮추고 넓히며 진행방향으로 민다는 정성 결과",
        "",
        "그러나 v1.0.14는 사용자의 출발 관측을 정본 수준으로 닫지 못했다.",
        "저장 default에서는 current broadening이 꺼져 있고, 저온에서는 RT/F",
        "평형폭만 줄어 peak가 오히려 높고 좁아진다. 실제 피팅이 된다는 사실은",
        "경험적 `L_V` 또는 조정 파라미터가 곡선을 표현할 수 있음을 보일 뿐,",
        "그 값이 전위·온도·전류에 따른 물리 장벽을 식별했다는 뜻은 아니다.",
        "",
        "## 실험 관측과 기작의 지위",
        "",
        "Fly–Chen은 고율에서 ICA peak가 낮아지고 넓어지며 이동·소실할 수",
        "있음을 보였고, Gismero 등은 graphite/NMC532에서 온도 하강 또는",
        "전류 증가가 선택된 peak를 flatten/broaden한다는 것을 직접 보였다.",
        "따라서 사용자의 관측 목표는 문헌과 양립한다.",
        "",
        "다만 둘 다 full-cell 결과다. 저항, 전해질·고체 확산, 전하전달,",
        "전극 balancing, 상경계 운동, feature overlap이 함께 들어간다.",
        "따라서 단일 지수 꼬리는 가능한 reduced mechanism이지 문헌이",
        "유일하게 확정한 mechanism이 아니다.",
        "",
        "## 정전류 좌표와 3,600배 단위 결함",
        "",
        "시간초를 쓰는 Eyring rate와 결합하려면",
        "`qdot = I[A]/Q[C]`여야 한다. 그런데 facade는 C-rate를 h^-1로",
        "받아 `I=c_rate*Q_cell`로 만든 뒤 같은 숫자를 seconds-based",
        "`kBT/h`와 결합한다.",
        "",
        f"- code numeric qdot: {unit['code_numeric_qdot']:.8g}",
        f"- correct qdot: {unit['correct_qdot_per_second']:.8g} s^-1",
        f"- L_q ratio: {unit['code_to_si_ratio']:.0f}",
        (
            "- equivalent barrier bias at 298.15 K: "
            f"{unit['equivalent_barrier_bias_J_per_mol_at_298p15K']/1000:.3f} "
            "kJ/mol"
        ),
        "",
        "즉 같은 broadening을 맞출 때 현재 hour/second 경로는 유효 장벽을",
        "약 20.3 kJ/mol 낮게 보이게 한다. `L_V/w=1`의 예에서 code",
        f"수치계약은 {barrier['code_hour_as_second_barrier_J_per_mol']/1000:.3f}",
        "kJ/mol, SI 일관 계약은",
        f"{barrier['dimensionally_correct_barrier_J_per_mol']/1000:.3f} kJ/mol을 요구한다.",
        "",
        "## 전위·조성 의존 장벽이 계산에서 사라지는 지점",
        "",
        "default n=1이면 `min(4.357 n RT, 4 RT)`는 항상 `A=4RT`다.",
        f"이 지점의 logistic derivative는 정점의 {100*cutoff['logistic_derivative_fraction_of_peak']:.3f}%로,",
        "문건이 먼저 말한 5%도 아니다. 더 중요한 것은 A를 전이당 상수로",
        "동결하므로 실제 code의 `d ln L_q/dV=0`이라는 점이다.",
        "동일 식을 local A로 유지했다면 298.15 K, chi=0.5, A=4RT에서",
        f"`d ln L_q/dV={cutoff['local_model_dlnL_dV_per_V_at_A4RT_chi0p5']:.3f} V^-1`이다.",
        "",
        "Bazant의 비평형 열역학이 요구하는 것은 local activity와 reaction",
        "free energy다. `DeltaH_a_eff=DeltaH_a-chi*Omega`는 속도만",
        "바꾸고 forward/reverse 비에는 regular-solution chemical",
        "potential을 복원하지 않으므로 nonideal detailed balance closure가 아니다.",
        "",
        "## 저장 default의 joint limit",
        "",
        "대표 단일 전이에서 IR shift를 끄고 0.1C와 1C를 비교하면 세 온도",
        "모두 shape 차이가 0이다. 모든 lag가 grid switch 아래이기 때문이다.",
        "",
        f"- 258.15 K / 298.15 K peak-height ratio: {joint['lowT_to_roomT_peak_height']:.6f}",
        f"- 258.15 K / 298.15 K FWHM ratio: {joint['lowT_to_roomT_fwhm']:.6f}",
        f"- low-T taller: {joint['default_lowT_is_taller']}",
        f"- low-T narrower: {joint['default_lowT_is_narrower']}",
        "",
        "따라서 shipped default는 사용자의 `저온 × 유한전류 -> peak",
        "suppression/broadening`을 재현하지 않는다. 반대로 별도 mesoscopic",
        "rate를 둔 차원 일관 causal existence probe는 같은 관측을 정성적으로",
        f"재현했다: low-T/room-T peak ratio={proof['lowT_to_roomT_finite_current_peak_height']:.6f},",
        f"FWHM ratio={proof['lowT_to_roomT_finite_current_fwhm']:.6f}.",
        "이는 1차 완화 골격의 가능성만 보존하며 현 파라미터를 검증하지 않는다.",
        "",
        "## 수치·극한 결함",
        "",
        f"- direct L_V: max |I=0-I=1|={override['max_abs_I0_vs_I1']:.3e},",
        f"  max |I=0-equilibrium|={override['max_abs_I0_vs_equilibrium']:.6g}.",
        "  즉 zero-current limit를 위반한다.",
        f"- two-grid-step handoff: kinetic area={grid['kinetic_branch_impulse_area_fraction_at_threshold']:.6f},",
        f"  jump={100*grid['jump_fraction']:.3f}%.",
        "- 큰 장벽/저온에서 `L_q=+inf`가 되면 resolver는 `L_V=0`으로",
        f"  바꾼다(검산 result={overflow['resolved_LV_V']:.1f} V).",
        "  물리적 frozen limit를 equilibrium limit로 뒤집는 오류다.",
        "- 비등온 입력은 mean T에서 lag를 한 번만 평가하고, voltage sorting은",
        "  되돌림·휴지·비단조 protocol의 chronology를 잃는다.",
        "",
        "## v1.0.10에서 실제로 고쳐졌는가",
        "",
        "`func_L_q`, `_causal_lowpass`, `func_dH_a_eff`,",
        "`_resolve_lag_length`의 docstring 제외 executable AST는",
        "v1.0.10과 v1.0.14가 모두 동일하다. v1.0.14의 scalar-input",
        "guard와 설명 확장은 필요하지만, unit·frozen affinity·Omega",
        "shortcut·direct lag·grid switch의 핵심 blocker를 고치지 않았다.",
        "",
        "## 권고하는 정본 구조",
        "",
        "문건은 코드 이름 없이 다음 물리 순서로 다시 세워야 한다.",
        "",
        "1. 반응 방향과 signed current를 고정한다.",
        "2. host별 하나의 자유에너지에서 equilibrium chemical potential을 유도한다.",
        "3. local composition, phase fraction, stress, T, overpotential에서 affinity를 계산한다.",
        "4. 하나의 transition-state free energy에서 forward/reverse rate를 만들고 detailed balance를 검산한다.",
        "5. 전하전달·확산·핵생성/상경계·porous transport의 축약 순서를 명시한다.",
        "6. imposed current와 모든 reaction current의 합을 보존하며 terminal voltage를 푼다.",
        "7. 마지막에만 instrument/processing/heterogeneity observation operator를 적용한다.",
        "",
        "코드는 이 이론이 동결된 뒤 SI 내부단위, time/charge-domain state",
        "integration, local rate, current conservation, continuous small-lag",
        "limit, k->0 frozen limit를 그대로 구현해야 한다.",
        "",
        "## 직접 대조한 1차 문헌",
        "",
    ]
    for source in data["primary_source_checks"]:
        lines.append(f"- [{source['title']}]({source['url']})")
    lines.extend(
        [
            "",
            "## 판정표",
            "",
            "| ID | topic | disposition | reason |",
            "|---|---|---|---|",
        ]
    )
    for item in data["findings"]:
        reason = item["reason"].replace("|", "\\|")
        lines.append(
            f"| {item['id']} | {item['topic']} | "
            f"{item['disposition']} | {reason} |"
        )
    lines.extend(
        [
            "",
            "## 다음 단계",
            "",
            "Step 36.5에서 v1.0.14의 다수 review round가 선언한 수렴·완주·",
            "물리 오류 0 주장을 이번 독립 blocker와 대조해 v1.0.14 최종",
            "권위 판정을 닫는다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    paths = [CH1, CODE, V1010_CODE]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in paths}
    ch1 = CH1.read_text(encoding="utf-8")
    code = CODE.read_text(encoding="utf-8")
    module = load_module(CODE, "phase059_v1014_kinetics")
    numerical = numerical_rederivation(module)
    finding_rows = findings()
    source = source_contracts(ch1, code)
    lineage = lineage_contract()
    after = {str(path.relative_to(ROOT)): sha256(path) for path in paths}

    dispositions = [item["disposition"] for item in finding_rows]
    data: dict[str, Any] = {
        "schema_version": 1,
        "phase": 59,
        "step": "36.4",
        "audit_date": "2026-07-28",
        "scope": (
            "v1.0.14 kinetics, activation barrier, causal broadening, "
            "and low-temperature x finite-current joint theory-code limit"
        ),
        "authority_boundary": {
            "source_version": "v1.0.14",
            "latest_authoritative_release": "v1.0.25.2",
            "excluded_release": "v1.0.26",
            "source_edit_allowed": False,
            "new_theory_or_production_code_written": False,
        },
        "source_hashes_before": before,
        "source_hashes_after": after,
        "source_unchanged": before == after,
        "source_contracts": source,
        "lineage_contract": lineage,
        "primary_source_checks": PRIMARY_SOURCES,
        "numerical_rederivation": numerical,
        "findings": finding_rows,
        "repair_contract": repair_contract(),
        "summary": {
            "status": (
                "CONDITIONAL_P059_V1014_KINETIC_SKELETON_PRESERVED_BUT_"
                "CONSTANT_CURRENT_LOCAL_BARRIER_AND_JOINT_LIMIT_FAIL"
            ),
            "primary_source_count": len(PRIMARY_SOURCES),
            "finding_count": len(finding_rows),
            "preserve_family_count": sum(
                item.startswith("PRESERVE") for item in dispositions
            ),
            "reject_family_count": sum(
                item.startswith("REJECT") for item in dispositions
            ),
            "fail_family_count": sum(
                item.startswith("FAIL") for item in dispositions
            ),
            "require_family_count": sum(
                item.startswith("REQUIRE") for item in dispositions
            ),
            "empirical_only_count": sum(
                item.startswith("EMPIRICAL_ONLY") for item in dispositions
            ),
            "blocker_count": sum(
                item.startswith("BLOCKER") for item in dispositions
            ),
            "experimental_joint_target_supported": True,
            "linear_relaxation_continuum_skeleton_pass": True,
            "constant_current_unit_contract_pass": False,
            "closed_galvanostatic_forward_model_pass": False,
            "local_potential_barrier_pass": False,
            "nonideal_detailed_balance_pass": False,
            "default_current_broadening_pass": False,
            "default_lowT_finite_current_joint_limit_pass": False,
            "zero_current_limit_all_paths_pass": False,
            "small_lag_continuity_pass": False,
            "frozen_rate_limit_pass": False,
            "v1010_blockers_repaired_in_v1014": False,
            "repair_existence_proof_pass": numerical[
                "repair_existence_proof"
            ]["joint_target_reproduced"],
            "next_step": "36.5",
        },
    }
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text(render_report(data), encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))
    print(REPORT.relative_to(ROOT))
    print(data["summary"]["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
