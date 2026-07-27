#!/usr/bin/env python3
"""Independent entropy, heat and LCO checks for v1.0.10."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CH1 = ROOT / "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex"
CH2 = ROOT / "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex"
CODE = ROOT / "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py"
OUT = ROOT / "Codex/results/PHASE_058_V1010_HEAT_LCO_VALIDATION.json"


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
        "phase058_v1010_heat_probe", CODE
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("Cannot load v1.0.10 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def entropy_case(legacy, mode: str, width_parameter: float) -> dict:
    temperature = 298.15
    xi = 0.8
    logit = math.log(xi / (1.0 - xi))
    d_h = -13_000.0
    d_s = -16.0
    transition = {"dH_rxn": d_h, "dS_rxn": d_s, "Q": 1.0}
    if mode == "n_factor":
        transition["n"] = width_parameter
        width = width_parameter * legacy.R * temperature / legacy.F
        independent = d_s / legacy.F + width_parameter * legacy.R / legacy.F * logit
    elif mode == "constant_w":
        transition["w"] = width_parameter
        width = width_parameter
        independent = d_s / legacy.F
    else:
        raise ValueError(mode)

    center = float(legacy.func_U_j(temperature, d_h, d_s))
    voltage = center + width * logit
    model = legacy.GraphiteAnodeDischargeDQDV([transition], Rn=0.0, Cbg=0.0)
    implementation = float(model.entropy_coefficient(voltage, temperature)[0])
    return {
        "mode": mode,
        "parameter": width_parameter,
        "temperature_k": temperature,
        "xi": xi,
        "voltage_v": voltage,
        "independent_dudt_v_per_k": independent,
        "implementation_dudt_v_per_k": implementation,
        "absolute_error_v_per_k": abs(implementation - independent),
        "implementation_to_independent": (
            implementation / independent if independent != 0.0 else None
        ),
    }


def electronic_gate_check(legacy) -> dict:
    temperature = 298.15
    g_max = 13.0
    x_mit = 0.5
    dx_mit = 0.05
    center_value = float(
        legacy.func_dSe_molar(x_mit, temperature, g_max, x_mit, dx_mit)
    )
    composition = np.linspace(0.0, 1.0, 1_000_001)
    values = np.asarray(
        legacy.func_dSe_molar(
            composition,
            temperature,
            g_max,
            x_mit,
            dx_mit,
        )
    )
    integrated = float(np.trapezoid(values, composition))
    endpoint_scale = (
        -(np.pi**2 / 3.0)
        * legacy.R
        * (legacy.kB * temperature / legacy.EV_TO_J)
        * g_max
    )
    cited_partial_anchor_j_per_mol_k = 0.18 * legacy.R
    return {
        "temperature_k": temperature,
        "g_max_states_per_ev_atom": g_max,
        "x_mit": x_mit,
        "dx_mit": dx_mit,
        "gate_center_j_per_mol_k": center_value,
        "integral_dse_dx_j_per_mol_k": integrated,
        "analytic_endpoint_entropy_change_j_per_mol_k": endpoint_scale,
        "integration_absolute_error_j_per_mol_k": abs(
            integrated - endpoint_scale
        ),
        "integrated_change_over_r": integrated / legacy.R,
        "stated_0p18_kb_anchor_j_per_mol_k": cited_partial_anchor_j_per_mol_k,
        "integrated_magnitude_to_0p18_anchor_ratio": abs(integrated)
        / cited_partial_anchor_j_per_mol_k,
        "verdict": (
            "THE_LOGISTIC_GATE_INTEGRATES_TO_THE_FULL_GMAX_ENDPOINT_CHANGE; "
            "THE_0P18_KB_ANCHOR_CANNOT_BE_DECLARED_INDEPENDENT_OF_THIS_SUM_RULE"
        ),
    }


def electronic_temperature_check(legacy) -> dict:
    transition = next(
        item for item in legacy.LCO_MSMR_LIT if item.get("electronic")
    )
    model = legacy.LCOCathodeDQDV([transition], Rn=0.0, Cbg=0.0)
    t_ref = 298.15
    t_high = 328.15
    d_s_e_ref = float(
        legacy.func_dSe_molar(
            transition["x_center"],
            t_ref,
            transition["g_max_eV"],
            transition["x_MIT"],
            transition["dx_MIT"],
        )
    )
    a_e = d_s_e_ref / t_ref
    d_s_0 = float(transition["dS_rxn"])
    code_u_ref = float(
        legacy.func_U_j(
            t_ref,
            transition["dH_rxn"],
            model._effective_dS_rxn(transition, t_ref),
        )
    )
    code_u_high = float(
        legacy.func_U_j(
            t_high,
            transition["dH_rxn"],
            model._effective_dS_rxn(transition, t_high),
        )
    )
    correct_u_high = (
        code_u_ref
        + d_s_0 / legacy.F * (t_high - t_ref)
        + a_e / (2.0 * legacy.F) * (t_high**2 - t_ref**2)
    )
    return {
        "t_ref_k": t_ref,
        "t_high_k": t_high,
        "dse_ref_j_per_mol_k": d_s_e_ref,
        "electronic_slope_a_e_j_per_mol_k2": a_e,
        "code_u_ref_v": code_u_ref,
        "code_u_high_v": code_u_high,
        "integrated_t_squared_u_high_v": correct_u_high,
        "code_minus_t_squared_v": code_u_high - correct_u_high,
        "code_curvature_d2u_dt2": 0.0,
        "theory_curvature_d2u_dt2_v_per_k2": a_e / legacy.F,
        "verdict": "THEORY_T_SQUARED_TERM_IS_NOT_IMPLEMENTED",
    }


def lco_default_check(legacy) -> dict:
    transitions = legacy.LCO_MSMR_LIT
    model = legacy.LCOCathodeDQDV(transitions, Rn=0.0, Cbg=0.0)
    voltage = np.linspace(3.6, 4.3, 4001)
    zero = np.asarray(
        model.dqdv(voltage, 298.15, I_abs=0.0, Q_cell=3600.0, s=+1)
    )
    one = np.asarray(
        model.dqdv(voltage, 298.15, I_abs=1.0, Q_cell=3600.0, s=+1)
    )
    return {
        "transition_count": len(transitions),
        "listed_u_values_v": [item["U"] for item in transitions],
        "maximum_listed_u_v": max(item["U"] for item in transitions),
        "transitions_with_omega": sum("Omega" in item for item in transitions),
        "transitions_with_gamma": sum("gamma" in item for item in transitions),
        "transitions_with_activation_enthalpy": sum(
            "dH_a" in item for item in transitions
        ),
        "transitions_with_dopant_state": sum(
            any(
                key in item
                for key in (
                    "dopant",
                    "dopant_fraction",
                    "oxygen_activity",
                    "surface_reconstruction",
                )
            )
            for item in transitions
        ),
        "maximum_abs_dqdv_difference_i0_i1": float(
            np.max(np.abs(zero - one))
        ),
        "covers_above_4p5_v": max(item["U"] for item in transitions) > 4.5,
        "verdict": (
            "DEFAULT_LCO_IS_A_RATE_INVARIANT_THREE_BELL_PLACEHOLDER_WITHOUT "
            "DOPING_OR_HIGH_VOLTAGE_CLOSURE"
        ),
    }


def main() -> int:
    legacy = load_legacy()
    entropy_cases = [
        entropy_case(legacy, "n_factor", 1.0),
        entropy_case(legacy, "n_factor", 2.0),
        entropy_case(legacy, "constant_w", 0.04),
    ]
    electronic_gate = electronic_gate_check(legacy)
    electronic_temperature = electronic_temperature_check(legacy)
    lco_default = lco_default_check(legacy)

    heat_probe = {
        "reversible_identity": "q_rev=-I*T*dUoc/dT",
        "units": "A*K*V/K=W",
        "positive_heat_convention": "q_dot>0 means heat generation",
        "positive_discharge_current_required": True,
        "irreversible_positive_example_w": float(
            legacy.GraphiteAnodeDischargeDQDV([], Cbg=0.0).irreversible_heat(
                4.0, 3.0, 1.0
            )
        ),
        "irreversible_negative_example_w": float(
            legacy.GraphiteAnodeDischargeDQDV([], Cbg=0.0).irreversible_heat(
                3.0, 4.0, 1.0
            )
        ),
        "verdict": (
            "THE_REVERSIBLE_IDENTITY_IS_DIMENSIONALLY_VALID_UNDER_ITS_SIGN "
            "CONVENTION; THE_IRREVERSIBLE_HELPER_DOES_NOT_ENFORCE_ENTROPY_PRODUCTION"
        ),
    }

    result = {
        "schema_version": "phase058-v1010-heat-lco-validation-v1",
        "sources": {
            "chapter_1": str(CH1.relative_to(ROOT)),
            "chapter_1_sha256": sha256(CH1),
            "chapter_2": str(CH2.relative_to(ROOT)),
            "chapter_2_sha256": sha256(CH2),
            "code": str(CODE.relative_to(ROOT)),
            "code_sha256": sha256(CODE),
        },
        "source_evidence": {
            "weighted_entropy_line": source_line(
                CH2,
                "\\frac{\\partial U_\\oc}{\\partial T}(x)\\Big|_{\\text{단순식}}",
            ),
            "reversible_heat_line": source_line(
                CH2,
                "\\dot Q_\\rev \\;=\\; -\\,I\\,T",
            ),
            "electronic_gate_line": source_line(
                CH1,
                "\\Delta S_{e,j}(x,T)",
            ),
            "t_squared_line": source_line(
                CH1,
                "\\boxed{\\;U_1(T)=U_1(T_0)",
            ),
            "code_config_line": source_line(
                CODE,
                "config = (R / F) * np.log",
            ),
            "code_irreversible_line": source_line(
                CODE,
                "return np.asarray(I) * (np.asarray(U_oc",
            ),
            "code_frozen_tref_line": source_line(
                CODE,
                "T_ref = 298.15",
            ),
        },
        "entropy_coefficient_cases": entropy_cases,
        "heat_sign_and_units": heat_probe,
        "electronic_entropy_gate": electronic_gate,
        "electronic_temperature_dependence": electronic_temperature,
        "lco_default_scope": lco_default,
        "claim_dispositions": [
            {
                "claim": "The ideal n=1 configurational entropy coefficient follows from implicit differentiation.",
                "disposition": "PRESERVE_IN_IDEAL_N1_LIMIT",
            },
            {
                "claim": "The same R/F logit term remains valid for arbitrary n or constant empirical w.",
                "disposition": "REJECT_WIDTH_ENTROPY_CONTRACT_MISMATCH",
            },
            {
                "claim": "q_rev=-I*T*dU/dT.",
                "disposition": "PRESERVE_WITH_EXPLICIT_CURRENT_AND_HEAT_SIGN",
            },
            {
                "claim": "The irreversible heat helper always returns nonnegative dissipation.",
                "disposition": "REJECT_NO_SIGN_OR_ENTROPY_PRODUCTION_GUARD",
            },
            {
                "claim": "The LCO electronic entropy gate is quantitatively anchored.",
                "disposition": "EMPIRICAL_ONLY_SUM_RULE_CONFLICT",
            },
            {
                "claim": "The code implements the documented T-squared electronic shift.",
                "disposition": "REJECT_FROZEN_TREF_LINEAR_ONLY",
            },
            {
                "claim": "The default LCO model covers doped high-voltage finite-rate behavior.",
                "disposition": "REJECT_PLACEHOLDER_ONLY",
            },
        ],
        "validation": {
            "ideal_n1_entropy_error_lt_1e_15": entropy_cases[0][
                "absolute_error_v_per_k"
            ]
            < 1e-15,
            "n2_entropy_mismatch_detected": entropy_cases[1][
                "absolute_error_v_per_k"
            ]
            > 1e-5,
            "constant_w_entropy_mismatch_detected": entropy_cases[2][
                "absolute_error_v_per_k"
            ]
            > 1e-5,
            "electronic_gate_integral_matches_endpoint": electronic_gate[
                "integration_absolute_error_j_per_mol_k"
            ]
            < 1e-3,
            "irreversible_negative_case_detected": heat_probe[
                "irreversible_negative_example_w"
            ]
            < 0.0,
            "t_squared_missing_detected": abs(
                electronic_temperature["code_minus_t_squared_v"]
            )
            > 1e-6,
            "lco_rate_invariance_detected": lco_default[
                "maximum_abs_dqdv_difference_i0_i1"
            ]
            == 0.0,
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
                "entropy_errors": [
                    item["absolute_error_v_per_k"] for item in entropy_cases
                ],
                "gate_center": electronic_gate[
                    "gate_center_j_per_mol_k"
                ],
                "gate_integral": electronic_gate[
                    "integral_dse_dx_j_per_mol_k"
                ],
                "t_squared_difference_v": electronic_temperature[
                    "code_minus_t_squared_v"
                ],
                "lco_rate_difference": lco_default[
                    "maximum_abs_dqdv_difference_i0_i1"
                ],
                "validation": result["validation"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
