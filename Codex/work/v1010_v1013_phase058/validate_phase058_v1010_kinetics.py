#!/usr/bin/env python3
"""Independent equilibrium, hysteresis and kinetic checks for v1.0.10."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
THEORY = ROOT / "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex"
CODE = ROOT / "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py"
OUT = ROOT / "Codex/results/PHASE_058_V1010_KINETICS_VALIDATION.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_line(path: Path, needle: str) -> int:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return number
    raise ValueError(f"Needle not found in {path}: {needle}")


def load_legacy():
    sys.dont_write_bytecode = True
    specification = importlib.util.spec_from_file_location(
        "phase058_v1010_kinetic_probe", CODE
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("Cannot load v1.0.10 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def peak_metrics(voltage: np.ndarray, signal: np.ndarray) -> dict:
    peak_index = int(np.argmax(signal))
    peak = float(signal[peak_index])
    half = peak / 2.0
    above = voltage[signal >= half]
    return {
        "area": float(np.trapezoid(signal, voltage)),
        "peak_height": peak,
        "peak_voltage": float(voltage[peak_index]),
        "fwhm": float(above[-1] - above[0]),
    }


def continuous_relaxation_family(width: float) -> list[dict]:
    voltage = np.linspace(-20.0 * width, 40.0 * width, 600_001)
    step = float(voltage[1] - voltage[0])
    equilibrium_occupancy = 1.0 / (1.0 + np.exp(-voltage / width))
    equilibrium_kernel = (
        equilibrium_occupancy * (1.0 - equilibrium_occupancy) / width
    )
    equilibrium = peak_metrics(voltage, equilibrium_kernel)
    records = [
        {
            "lag_over_width": 0.0,
            **equilibrium,
            "peak_height_relative_to_equilibrium": 1.0,
            "fwhm_relative_to_equilibrium": 1.0,
        }
    ]
    for ratio in (0.25, 0.5, 1.0, 2.0):
        lag_length = ratio * width
        decay = math.exp(-step / lag_length)
        lagged = np.empty_like(equilibrium_occupancy)
        lagged[0] = equilibrium_occupancy[0]
        for index in range(1, lagged.size):
            lagged[index] = (
                decay * lagged[index - 1]
                + (1.0 - decay) * equilibrium_occupancy[index]
            )
        observed = (equilibrium_occupancy - lagged) / lag_length
        metrics = peak_metrics(voltage, observed)
        records.append(
            {
                "lag_over_width": ratio,
                **metrics,
                "peak_height_relative_to_equilibrium": metrics["peak_height"]
                / equilibrium["peak_height"],
                "fwhm_relative_to_equilibrium": metrics["fwhm"]
                / equilibrium["fwhm"],
            }
        )
    return records


def regular_solution_checks(legacy) -> list[dict]:
    records = []
    temperature = 298.15
    critical = 2.0 * legacy.R * temperature
    for ratio in (0.99, 1.0, 1.000001, 1.1, 2.0, 4.0):
        omega = ratio * critical
        implementation = float(legacy.func_dU_hys(temperature, omega))
        if omega <= critical:
            independent = 0.0
            u = None
        else:
            u = math.sqrt(1.0 - critical / omega)
            independent = (
                2.0
                / legacy.F
                * (
                    omega * u
                    - critical * math.atanh(u)
                )
            )
        records.append(
            {
                "omega_over_2rt": ratio,
                "u": u,
                "implementation_gap_v": implementation,
                "independent_gap_v": independent,
                "absolute_error_v": abs(implementation - independent),
            }
        )
    return records


def legacy_switch_check(legacy, width: float) -> dict:
    grid_step = 2.0e-4
    voltage = np.arange(-0.3, 0.3000001, grid_step)
    occupancy = 1.0 / (1.0 + np.exp(-voltage / width))
    equilibrium = occupancy * (1.0 - occupancy) / width
    threshold = 2.0 * grid_step
    lag_length = threshold * 1.0001
    lagged = legacy._causal_lowpass(occupancy, grid_step, lag_length)
    kinetic = (occupancy - lagged) / lag_length
    return {
        "grid_step_v": grid_step,
        "branch_threshold_v": threshold,
        "kinetic_probe_lag_v": lag_length,
        "equilibrium_peak": float(np.max(equilibrium)),
        "kinetic_peak_just_above_threshold": float(np.max(kinetic)),
        "peak_ratio_kinetic_to_equilibrium": float(
            np.max(kinetic) / np.max(equilibrium)
        ),
        "relative_jump_at_mode_switch": float(
            1.0 - np.max(kinetic) / np.max(equilibrium)
        ),
    }


def default_lag_check(legacy) -> dict:
    model = legacy.GraphiteAnodeDischargeDQDV(
        legacy.GRAPHITE_STAGING_LIT,
        Rn=0.0,
        Cbg=0.0,
    )
    temperature = 258.15
    current_numeric = 1.0
    values = []
    for transition in legacy.GRAPHITE_STAGING_LIT:
        n_factor = float(model._n_factor(transition, temperature))
        values.append(
            float(
                model._resolve_lag_length(
                    transition,
                    temperature,
                    current_numeric,
                    1.0,
                    n_factor,
                    +1,
                )
            )
        )
    v_span = 0.34 - 0.02
    work_span = v_span * (1.0 + model.grid_pad_lo + model.grid_pad_hi)
    grid_step = work_span / (model.n_work_min - 1)
    threshold = model.min_lag_grid_steps * grid_step
    return {
        "temperature_k": temperature,
        "current_numeric": current_numeric,
        "q_cell_numeric": 1.0,
        "lag_lengths_v": values,
        "maximum_lag_v": max(values),
        "representative_work_grid_step_v": grid_step,
        "equilibrium_switch_threshold_v": threshold,
        "maximum_lag_to_threshold_ratio": max(values) / threshold,
        "all_default_transitions_use_equilibrium_branch": all(
            value < threshold for value in values
        ),
    }


def direct_override_zero_current_check(legacy) -> dict:
    temperature = 298.15
    voltage = np.linspace(-0.4, 0.4, 5001)
    transition = {"U": 0.0, "n": 1.0, "Q": 1.0, "L_V": 0.04}
    model = legacy.GraphiteAnodeDischargeDQDV(
        [transition],
        Rn=0.0,
        Cbg=0.0,
    )
    equilibrium = np.asarray(model.equilibrium(voltage, temperature))
    zero_current = np.asarray(
        model.dqdv(
            voltage,
            temperature,
            I_abs=0.0,
            Q_cell=3600.0,
            s=+1,
        )
    )
    eq_metrics = peak_metrics(voltage, equilibrium)
    zero_metrics = peak_metrics(voltage, zero_current)
    return {
        "direct_l_v": transition["L_V"],
        "current_a": 0.0,
        "equilibrium": eq_metrics,
        "zero_current_with_override": zero_metrics,
        "maximum_absolute_curve_difference": float(
            np.max(np.abs(zero_current - equilibrium))
        ),
        "zero_current_peak_relative_to_equilibrium": zero_metrics["peak_height"]
        / eq_metrics["peak_height"],
        "zero_current_fwhm_relative_to_equilibrium": zero_metrics["fwhm"]
        / eq_metrics["fwhm"],
        "verdict": "DIRECT_LV_OVERRIDE_VIOLATES_I_TO_ZERO_LIMIT",
    }


def main() -> int:
    legacy = load_legacy()
    temperature = 298.15
    width = legacy.R * temperature / legacy.F
    regular_solution = regular_solution_checks(legacy)
    relaxation = continuous_relaxation_family(width)
    switch = legacy_switch_check(legacy, width)
    default_lag = default_lag_check(legacy)
    direct_override = direct_override_zero_current_check(legacy)

    affinity_default = min(4.357 * legacy.R * temperature, 4.0 * legacy.R * temperature)
    result = {
        "schema_version": "phase058-v1010-kinetics-validation-v1",
        "sources": {
            "theory": str(THEORY.relative_to(ROOT)),
            "theory_sha256": sha256(THEORY),
            "code": str(CODE.relative_to(ROOT)),
            "code_sha256": sha256(CODE),
        },
        "source_evidence": {
            "logistic_direction_line": source_line(
                THEORY,
                "\\xi_{\\eq,j}(V,T)=\\frac{1}{1+\\exp",
            ),
            "broadening_three_sources_line": source_line(
                THEORY,
                "broadening 의 세 출처",
            ),
            "lag_definition_line": source_line(
                THEORY,
                "L_{q,j}=\\frac{|I|}{Q_\\cell\\,k_j}",
            ),
            "cut_affinity_line": source_line(
                THEORY,
                "\\mathcal A=\\min\\!",
            ),
            "effective_barrier_line": source_line(
                THEORY,
                "\\Delta H_{a,j}^\\eff=\\Delta H_{a,j}-\\chi_d",
            ),
            "branch_switch_line": source_line(
                THEORY,
                "L_{V,j}<\\nu\\,\\Delta_\\mathrm{grid}",
            ),
            "code_direct_override_line": source_line(
                CODE,
                "L_V_override = transition.get('L_V')",
            ),
            "code_cut_affinity_line": source_line(
                CODE,
                "A = float(min(z_cut * n_safe * R * T",
            ),
        },
        "regular_solution_spinodal": {
            "critical_condition": "Omega > 2 R T",
            "records": regular_solution,
            "maximum_absolute_error_v": max(
                item["absolute_error_v"] for item in regular_solution
            ),
            "interpretation": (
                "The formula is the separation of homogeneous regular-solution "
                "spinodal extrema, an upper metastability scale rather than a "
                "closed prediction of measured hysteresis."
            ),
        },
        "continuous_relaxation": {
            "equation": "d xi/dV = (xi_eq-xi)/L_V",
            "width_v": width,
            "records": relaxation,
            "qualitative_result": (
                "Increasing L_V lowers the peak, broadens it, shifts it in the "
                "causal direction, and conserves area over a sufficiently wide domain."
            ),
        },
        "legacy_grid_switch": switch,
        "default_dynamic_path": default_lag,
        "default_hysteresis_path": {
            "transition_count": len(legacy.GRAPHITE_STAGING_LIT),
            "transitions_with_gamma": sum(
                "gamma" in item for item in legacy.GRAPHITE_STAGING_LIT
            ),
            "implicit_gamma": 0.0,
            "hysteresis_active": any(
                float(item.get("gamma", 0.0)) != 0.0
                for item in legacy.GRAPHITE_STAGING_LIT
            ),
            "cross_call_state_variable": False,
            "verdict": "DEFAULT_HYSTERESIS_DISABLED_AND_MODEL_STATELESS",
        },
        "direct_override_zero_current": direct_override,
        "affinity_and_barrier": {
            "default_n": 1.0,
            "z_cut": 4.357,
            "a_cap_rt": 4.0,
            "selected_affinity_j_per_mol": affinity_default,
            "selected_affinity_over_rt": affinity_default
            / (legacy.R * temperature),
            "z_cut_is_inactive_at_default_n": True,
            "local_voltage_dependence_in_code": False,
            "effective_barrier_default_enabled": True,
            "verdict": (
                "THE_CODE_FREEZES_AN_ARBITRARY_CUT_AFFINITY_AND_OVERLOADS_OMEGA; "
                "IT_DOES_NOT_EVALUATE_A_LOCAL_POTENTIAL_DEPENDENT_BARRIER"
            ),
        },
        "equilibrium_direction_probe": {
            "voltage_v": width,
            "center_v": 0.0,
            "xi_s_plus": float(
                legacy.func_ksi_eq(temperature, width, 0.0, 1.0, +1)
            ),
            "xi_s_minus": float(
                legacy.func_ksi_eq(temperature, width, 0.0, 1.0, -1)
            ),
            "sum": float(
                legacy.func_ksi_eq(temperature, width, 0.0, 1.0, +1)
                + legacy.func_ksi_eq(temperature, width, 0.0, 1.0, -1)
            ),
            "verdict": (
                "THE_KERNEL_IS_DIRECTION_INVARIANT_BUT_THE_EQUILIBRIUM_STATE "
                "VARIABLE_IS_PROTOCOL_DEPENDENT"
            ),
        },
        "claim_dispositions": [
            {
                "claim": "Linear first-order relaxation can lower and broaden a finite-rate ICA peak.",
                "disposition": "PRESERVE_AS_REDUCED_MODEL",
            },
            {
                "claim": "The stored default model demonstrates that mechanism.",
                "disposition": "REJECT_DEFAULT_PATH_IS_EQUILIBRIUM",
            },
            {
                "claim": "The regular-solution closed form is a measured hysteresis prediction.",
                "disposition": "CORRECT_TO_SPINODAL_UPPER_SCALE",
            },
            {
                "claim": "gamma and h_eta close hysteresis memory.",
                "disposition": "REJECT_STATELESS_PHENOMENOLOGY",
            },
            {
                "claim": "The barrier depends on local electrode potential.",
                "disposition": "REJECT_AFFINITY_IS_FROZEN_PER_TRANSITION",
            },
            {
                "claim": "A direct L_V is a physical parameter compatible with equilibrium.",
                "disposition": "REJECT_UNLESS_PROTOCOL_SCALED",
            },
        ],
        "validation": {
            "regular_solution_error_lt_1e_15_v": max(
                item["absolute_error_v"] for item in regular_solution
            )
            < 1e-15,
            "relaxation_area_within_2e_4": all(
                abs(item["area"] - 1.0) < 2e-4 for item in relaxation
            ),
            "peak_decreases_with_lag": all(
                relaxation[index]["peak_height"]
                > relaxation[index + 1]["peak_height"]
                for index in range(len(relaxation) - 1)
            ),
            "fwhm_increases_with_lag": all(
                relaxation[index]["fwhm"]
                < relaxation[index + 1]["fwhm"]
                for index in range(len(relaxation) - 1)
            ),
            "default_path_equilibrium": default_lag[
                "all_default_transitions_use_equilibrium_branch"
            ],
            "direct_override_differs_at_zero_current": direct_override[
                "maximum_absolute_curve_difference"
            ]
            > 1e-3,
        },
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUT.relative_to(ROOT)),
                "spinodal_error": result["regular_solution_spinodal"][
                    "maximum_absolute_error_v"
                ],
                "switch_jump": switch["relative_jump_at_mode_switch"],
                "default_lag_ratio": default_lag[
                    "maximum_lag_to_threshold_ratio"
                ],
                "zero_current_peak_ratio": direct_override[
                    "zero_current_peak_relative_to_equilibrium"
                ],
                "validation": result["validation"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
