#!/usr/bin/env python3
"""Independent numerical probes for the v1.0.10-v1.0.13 model lineage."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Codex" / "results" / "PHASE_058_INDEPENDENT_PROBES.json"
MODULES = {
    "v1.0.10": "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    "v1.0.12": "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py",
    "v1.0.13": "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(version: str, relative: str):
    spec = importlib.util.spec_from_file_location(f"phase058_{version.replace('.', '_')}", ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    return float(np.sum((y[:-1] + y[1:]) * 0.5 * np.diff(x)))


def fwhm(x: np.ndarray, y: np.ndarray) -> float:
    baseline = float(np.min(y))
    shifted = y - baseline
    half = 0.5 * float(np.max(shifted))
    indices = np.flatnonzero(shifted >= half)
    if indices.size < 2:
        return float("nan")
    return float(x[indices[-1]] - x[indices[0]])


def independent_logistic_derivative(
    voltage: np.ndarray, center: float, width: float, capacity: float
) -> np.ndarray:
    z = (voltage - center) / width
    # Stable identity: logistic'(z) = 1/(2 + exp(z) + exp(-z)).
    clipped = np.clip(z, -700.0, 700.0)
    return capacity / width / (2.0 + np.exp(clipped) + np.exp(-clipped))


def finite_max_abs(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def peak_voltage(voltage: np.ndarray, values: np.ndarray) -> float:
    return float(voltage[int(np.argmax(values))])


def probe_version(version: str, module) -> dict:
    R = float(module.R)
    F = float(module.F)
    temperature_values = [258.15, 298.15, 318.15]

    # 1. One-transition equilibrium compared with an independently coded
    # logistic derivative, its normalization, FWHM, and peak amplitude.
    single_transition = [{"U": 0.12, "n": 1.0, "Q": 0.5}]
    single = module.GraphiteAnodeDischargeDQDV(single_transition, Rn=0.0, Cbg=0.0)
    voltage = np.linspace(-0.8, 1.0, 180001)
    equilibrium = np.asarray(single.equilibrium(voltage, T=298.15), dtype=float)
    width = R * 298.15 / F
    analytic = independent_logistic_derivative(voltage, 0.12, width, 0.5)
    width_factor = 4.0 * np.arccosh(np.sqrt(2.0))
    equilibrium_kernel = {
        "area_numeric": trapezoid(equilibrium, voltage),
        "area_expected": 0.5,
        "area_abs_error": abs(trapezoid(equilibrium, voltage) - 0.5),
        "max_abs_error_vs_independent_formula": finite_max_abs(equilibrium, analytic),
        "peak_numeric": float(np.max(equilibrium)),
        "peak_expected": 0.5 / (4.0 * width),
        "fwhm_numeric_V": fwhm(voltage, equilibrium),
        "fwhm_expected_V": width_factor * width,
    }

    temperature_scaling = []
    voltage_t = np.linspace(-0.2, 0.44, 128001)
    for temperature in temperature_values:
        values = np.asarray(single.equilibrium(voltage_t, T=temperature), dtype=float)
        expected_width = width_factor * R * temperature / F
        temperature_scaling.append(
            {
                "T_K": temperature,
                "peak": float(np.max(values)),
                "fwhm_V": fwhm(voltage_t, values),
                "expected_fwhm_V": expected_width,
                "area": trapezoid(values, voltage_t),
            }
        )

    # 2. 'n' precedence and the distinct temperature behavior of a w-only
    # empirical width.
    with_both = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.12, "n": 1.0, "w": 0.005, "Q": 0.5}], Cbg=0.0
    )
    n_only = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.12, "n": 1.0, "Q": 0.5}], Cbg=0.0
    )
    w_only = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.12, "w": 0.005, "Q": 0.5}], Cbg=0.0
    )
    n_precedence = {
        "both_vs_n_only_max_abs_298K": finite_max_abs(
            with_both.equilibrium(voltage_t, 298.15),
            n_only.equilibrium(voltage_t, 298.15),
        ),
        "w_only_fwhm_258K_V": fwhm(
            voltage_t, np.asarray(w_only.equilibrium(voltage_t, 258.15), dtype=float)
        ),
        "w_only_fwhm_318K_V": fwhm(
            voltage_t, np.asarray(w_only.equilibrium(voltage_t, 318.15), dtype=float)
        ),
    }

    # 3. Current behavior of the shipped graphite defaults with Rn removed.
    voltage_g = np.linspace(0.02, 0.35, 4000)
    graphite = module.GraphiteAnodeDischargeDQDV(
        copy.deepcopy(module.GRAPHITE_STAGING_LIT), Rn=0.0, Cbg=0.0
    )
    current_values = [0.0, 0.02, 0.2, 1.0]
    graphite_curves = {
        str(current): np.asarray(
            graphite.dqdv(voltage_g, 298.15, current, 1.0, s=+1), dtype=float
        )
        for current in current_values
    }
    graphite_lag_lengths = {}
    for current in current_values:
        graphite_lag_lengths[str(current)] = [
            float(
                graphite._resolve_lag_length(
                    transition,
                    298.15,
                    current,
                    1.0,
                    float(np.asarray(graphite._n_factor(transition, 298.15)).reshape(-1)[0]),
                    +1,
                )
            )
            for transition in graphite.transitions
        ]
    default_graphite_current = {
        "current_A": current_values,
        "lag_lengths_V": graphite_lag_lengths,
        "max_abs_vs_I0": {
            key: finite_max_abs(values, graphite_curves["0.0"])
            for key, values in graphite_curves.items()
        },
        "peaks": {key: float(np.max(values)) for key, values in graphite_curves.items()},
    }

    # A direct L_V override bypasses the I<=0 branch and is independent of I.
    direct_lag = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.12, "n": 0.2, "Q": 0.5, "L_V": 0.02}], Rn=0.0, Cbg=0.0
    )
    direct_eq = np.asarray(direct_lag.equilibrium(voltage_t, 298.15), dtype=float)
    direct_i0 = np.asarray(direct_lag.dqdv(voltage_t, 298.15, 0.0, 1.0, +1), dtype=float)
    direct_i1 = np.asarray(direct_lag.dqdv(voltage_t, 298.15, 1.0, 1.0, +1), dtype=float)
    direct_lag_behavior = {
        "I0_vs_I1_max_abs": finite_max_abs(direct_i0, direct_i1),
        "I0_vs_equilibrium_max_abs": finite_max_abs(direct_i0, direct_eq),
        "I0_peak": float(np.max(direct_i0)),
        "I1_peak": float(np.max(direct_i1)),
        "equilibrium_peak": float(np.max(direct_eq)),
        "I0_fwhm_V": fwhm(voltage_t, direct_i0),
        "equilibrium_fwhm_V": fwhm(voltage_t, direct_eq),
    }

    # 4. C-rate/capacity dimensional contract.
    unit_model = module.GraphiteAnodeDischargeDQDV(
        [{"U": 0.12, "n": 1.0, "Q": 0.5}], Rn=0.01, Cbg=0.0
    )
    c_rate_curve = np.asarray(
        unit_model.curve(voltage_t, c_rate=0.2, Q_cell=3600.0, T=298.15), dtype=float
    )
    current_720 = np.asarray(
        unit_model.dqdv(voltage_t, 298.15, 720.0, 3600.0, +1), dtype=float
    )
    current_02 = np.asarray(
        unit_model.dqdv(voltage_t, 298.15, 0.2, 3600.0, +1), dtype=float
    )
    c_rate_contract = {
        "Q_cell_input": 3600.0,
        "c_rate_per_h": 0.2,
        "code_implied_I": 720.0,
        "c_rate_curve_vs_I720_max_abs": finite_max_abs(c_rate_curve, current_720),
        "c_rate_curve_vs_I0p2_max_abs": finite_max_abs(c_rate_curve, current_02),
        "dimensional_note": "If Q_cell is coulombs, the physically converted current is c_rate*Q_cell/3600.",
    }

    # 5. Hysteresis center split and absence of cross-call state memory.
    hys_transition = [{"U": 0.12, "n": 0.2, "Q": 0.5, "Omega": 12000.0, "gamma": 1.0}]
    hys = module.GraphiteAnodeDischargeDQDV(hys_transition, Rn=0.0, Cbg=0.0)
    hys_dis_1 = np.asarray(hys.dqdv(voltage_t, 298.15, 0.0, 1.0, +1), dtype=float)
    hys_chg = np.asarray(hys.dqdv(voltage_t, 298.15, 0.0, 1.0, -1), dtype=float)
    hys_dis_2 = np.asarray(hys.dqdv(voltage_t, 298.15, 0.0, 1.0, +1), dtype=float)
    predicted_gap = float(module.func_dU_hys(298.15, 12000.0))
    hysteresis = {
        "predicted_gap_V": predicted_gap,
        "discharge_peak_V": peak_voltage(voltage_t, hys_dis_1),
        "charge_peak_V": peak_voltage(voltage_t, hys_chg),
        "numeric_peak_gap_V": peak_voltage(voltage_t, hys_dis_1)
        - peak_voltage(voltage_t, hys_chg),
        "repeat_after_opposite_call_max_abs": finite_max_abs(hys_dis_1, hys_dis_2),
        "cross_call_state_detected": finite_max_abs(hys_dis_1, hys_dis_2) != 0.0,
    }

    # 6. Entropy and heat identities plus the unguarded irreversible-heat sign.
    entropy_transition = [
        {"dH_rxn": -12000.0, "dS_rxn": 20.0, "n": 1.0, "Q": 1.0, "U": 0.0}
    ]
    entropy_model = module.GraphiteAnodeDischargeDQDV(entropy_transition, Cbg=0.0)
    entropy_center = float(module.func_U_j(298.15, -12000.0, 20.0))
    entropy_code = float(
        np.asarray(entropy_model.entropy_coefficient(np.array([entropy_center]), 298.15))[0]
    )
    dtemperature = 1e-3
    entropy_fd = float(
        (
            module.func_U_j(298.15 + dtemperature, -12000.0, 20.0)
            - module.func_U_j(298.15 - dtemperature, -12000.0, 20.0)
        )
        / (2.0 * dtemperature)
    )
    qrev = float(
        np.asarray(entropy_model.reversible_heat(np.array([entropy_center]), 298.15, 2.0))[0]
    )
    heat = {
        "entropy_coefficient_center_V_per_K": entropy_code,
        "expected_dS_over_F_V_per_K": 20.0 / F,
        "finite_difference_center_V_per_K": entropy_fd,
        "reversible_heat_W": qrev,
        "reversible_heat_expected_W": -2.0 * 298.15 * entropy_code,
        "irreversible_heat_positive_case_W": float(entropy_model.irreversible_heat(3.8, 3.7, 1.0)),
        "irreversible_heat_negative_case_W": float(entropy_model.irreversible_heat(3.7, 3.8, 1.0)),
    }

    # 7. LCO default scope and high-level direction mapping.
    lco_transitions = copy.deepcopy(module.LCO_MSMR_LIT)
    lco = module.LCOCathodeDQDV(lco_transitions, Rn=0.0, Cbg=0.0)
    voltage_lco = np.linspace(3.65, 4.25, 5000)
    lco_i0 = np.asarray(lco.dqdv(voltage_lco, 298.15, 0.0, 1.0, +1), dtype=float)
    lco_i1 = np.asarray(lco.dqdv(voltage_lco, 298.15, 1.0, 1.0, +1), dtype=float)
    lco_direction = module.LCOCathodeDQDV(lco_transitions, Rn=0.01, Cbg=0.0)
    high_charge = np.asarray(
        lco_direction.curve(
            voltage_lco, direction="charge", I_abs=0.2, Q_cell=1.0, T=298.15
        ),
        dtype=float,
    )
    low_plus = np.asarray(
        lco_direction.dqdv(voltage_lco, 298.15, 0.2, 1.0, +1), dtype=float
    )
    low_minus = np.asarray(
        lco_direction.dqdv(voltage_lco, 298.15, 0.2, 1.0, -1), dtype=float
    )
    electronic_transition = next(
        transition for transition in lco_transitions if transition.get("electronic")
    )
    effective_entropy = float(
        np.asarray(lco._effective_dS_rxn(electronic_transition, 298.15)).reshape(-1)[0]
    )
    electronic_removed = copy.deepcopy(electronic_transition)
    electronic_removed["electronic"] = False
    non_electronic_entropy = float(
        np.asarray(lco._effective_dS_rxn(electronic_removed, 298.15)).reshape(-1)[0]
    )
    lco_scope = {
        "all_default_transitions_have_no_Omega": all("Omega" not in tr for tr in lco_transitions),
        "all_default_transitions_have_no_dH_a": all("dH_a" not in tr for tr in lco_transitions),
        "I0_vs_I1_Rn0_max_abs": finite_max_abs(lco_i0, lco_i1),
        "I0_peak": float(np.max(lco_i0)),
        "I1_peak": float(np.max(lco_i1)),
        "high_level_charge_vs_low_level_plus_max_abs": finite_max_abs(high_charge, low_plus),
        "high_level_charge_vs_low_level_minus_max_abs": finite_max_abs(high_charge, low_minus),
        "electronic_effective_dS_J_per_molK": effective_entropy,
        "same_transition_without_electronic_dS_J_per_molK": non_electronic_entropy,
        "electronic_delta_dS_J_per_molK": effective_entropy - non_electronic_entropy,
    }

    return {
        "version": version,
        "equilibrium_kernel": equilibrium_kernel,
        "temperature_scaling": temperature_scaling,
        "n_precedence": n_precedence,
        "default_graphite_current": default_graphite_current,
        "direct_lag_behavior": direct_lag_behavior,
        "c_rate_contract": c_rate_contract,
        "hysteresis": hysteresis,
        "heat": heat,
        "lco_scope": lco_scope,
    }


def main() -> None:
    before = {relative: sha256(ROOT / relative) for relative in MODULES.values()}
    results = [
        probe_version(version, load_module(version, relative))
        for version, relative in MODULES.items()
    ]
    after = {relative: sha256(ROOT / relative) for relative in MODULES.values()}
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "probe_method": "Independent logistic formula and numerical identities evaluated against imported frozen modules; no source mutation.",
        "source_sha256_before": before,
        "source_sha256_after": after,
        "sources_unchanged": before == after,
        "versions": results,
        "cross_version_summary": {
            "equilibrium_formula_max_error": max(
                result["equilibrium_kernel"]["max_abs_error_vs_independent_formula"]
                for result in results
            ),
            "direct_LV_I0_equals_I1": all(
                result["direct_lag_behavior"]["I0_vs_I1_max_abs"] == 0.0
                for result in results
            ),
            "negative_irreversible_heat_returned": all(
                result["heat"]["irreversible_heat_negative_case_W"] < 0.0
                for result in results
            ),
            "lco_default_rate_invariant_Rn0": all(
                result["lco_scope"]["I0_vs_I1_Rn0_max_abs"] == 0.0
                for result in results
            ),
            "lco_charge_maps_to_delithiation_plus": {
                result["version"]: (
                    result["lco_scope"]["high_level_charge_vs_low_level_plus_max_abs"]
                    < result["lco_scope"]["high_level_charge_vs_low_level_minus_max_abs"]
                )
                for result in results
            },
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
