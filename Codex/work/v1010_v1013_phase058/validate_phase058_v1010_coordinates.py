#!/usr/bin/env python3
"""Independent coordinate, unit and conservation checks for v1.0.10."""

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
OUT = (
    ROOT
    / "Codex/results/PHASE_058_V1010_COORDINATE_CONSERVATION_VALIDATION.json"
)


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
        "phase058_v1010_coordinate_probe", CODE
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("Cannot load v1.0.10 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def main() -> int:
    legacy = load_legacy()
    temperature = 298.15
    width = legacy.R * temperature / legacy.F
    center = 0.0
    voltage = np.linspace(-20.0 * width, 20.0 * width, 400_001)
    occupancy = 1.0 / (1.0 + np.exp(-(voltage - center) / width))
    kernel = occupancy * (1.0 - occupancy) / width
    numerical_area = float(np.trapezoid(kernel, voltage))
    numerical_peak = float(np.max(kernel))
    half_peak = numerical_peak / 2.0
    above = voltage[kernel >= half_peak]
    numerical_fwhm = float(above[-1] - above[0])
    analytic_fwhm = float(4.0 * width * np.arccosh(np.sqrt(2.0)))

    capacity_coulomb = 3600.0
    c_rate_per_hour = 0.2
    correct_current_ampere = c_rate_per_hour * capacity_coulomb / 3600.0
    legacy_facade_current_numeric = c_rate_per_hour * capacity_coulomb

    graphite_capacity_sum = float(
        sum(item["Q"] for item in legacy.GRAPHITE_STAGING_LIT)
    )
    lco_capacity_sum = float(
        sum(item["Q"] for item in legacy.LCO_MSMR_LIT)
    )

    result = {
        "schema_version": "phase058-v1010-coordinate-validation-v1",
        "sources": {
            "theory": str(THEORY.relative_to(ROOT)),
            "theory_sha256": sha256(THEORY),
            "code": str(CODE.relative_to(ROOT)),
            "code_sha256": sha256(CODE),
        },
        "source_evidence": {
            "theory_qcell_unit_c_line": source_line(
                THEORY, "$Q_\\cell$ (\\code{Q\\_cell}) & C"
            ),
            "theory_c_rate_map_line": source_line(
                THEORY, "|I|=\\text{c\\_rate}\\cdot Q_\\cell"
            ),
            "theory_charge_balance_line": source_line(
                THEORY, "Q_\\cell q=Q_\\bg(V_n)+\\sum_jQ_j\\xi_j"
            ),
            "theory_direction_line": source_line(
                THEORY, "전이 $j$ 의 진행률 $\\xi_j$(방전 시 $0\\to1$"
            ),
            "code_c_rate_map_line": source_line(
                CODE, "I_use = c * Q_cell"
            ),
            "code_kernel_line": source_line(
                CODE, "ksi_eq * (1.0 - ksi_eq) / w"
            ),
        },
        "independent_logistic_check": {
            "temperature_k": temperature,
            "width_rt_over_f_v": width,
            "integration_domain_widths_each_side": 20.0,
            "numerical_unit_kernel_area": numerical_area,
            "analytic_unit_kernel_area": 1.0,
            "area_absolute_error": abs(numerical_area - 1.0),
            "numerical_peak_per_v": numerical_peak,
            "analytic_peak_per_v": 1.0 / (4.0 * width),
            "peak_absolute_error_per_v": abs(
                numerical_peak - 1.0 / (4.0 * width)
            ),
            "numerical_fwhm_v": numerical_fwhm,
            "analytic_fwhm_v": analytic_fwhm,
            "fwhm_relative_error": abs(numerical_fwhm - analytic_fwhm)
            / analytic_fwhm,
            "analytic_fwhm_factor_times_w": float(
                4.0 * np.arccosh(np.sqrt(2.0))
            ),
        },
        "c_rate_unit_check": {
            "capacity_coulomb": capacity_coulomb,
            "capacity_ampere_hour": capacity_coulomb / 3600.0,
            "c_rate_per_hour": c_rate_per_hour,
            "correct_current_ampere": correct_current_ampere,
            "legacy_facade_numeric_result": legacy_facade_current_numeric,
            "legacy_to_correct_ratio": legacy_facade_current_numeric
            / correct_current_ampere,
            "verdict": "FACTOR_3600_UNIT_ERROR_IF_Q_CELL_IS_COULOMB",
            "valid_alternative_contract": (
                "I_A = c_rate_per_hour * Q_cell_Ah; or "
                "I_A = c_rate_per_hour * Q_cell_C / 3600"
            ),
        },
        "default_capacity_weights": {
            "graphite_sum_q": graphite_capacity_sum,
            "lco_sum_q": lco_capacity_sum,
            "code_values_are_consistent_with": (
                "NORMALIZED_CAPACITY_FRACTIONS_OR_USER_CHOSEN_CAPACITY_UNIT"
            ),
            "conflict": (
                "The theory table fixes Q_j and Q_cell to coulomb, while the "
                "shipped defaults are dimensionless weights and demos use Q_cell=1."
            ),
        },
        "coordinate_contract": {
            "state_coordinate": (
                "Q_state(V)=Q_bg(V)+sum_j Q_j xi_j(V)"
            ),
            "normalized_state_coordinate": "q=Q_state/Q_cell",
            "li_stoichiometry_relation": (
                "For a delithiation progress coordinate, host Li fraction "
                "x_Li decreases as xi increases; the proportionality requires "
                "active-material inventory and usable stoichiometric window."
            ),
            "differential_capacity": (
                "dQ_state/dV=C_bg+sum_j Q_j dxi_j/dV"
            ),
            "plot_convention": (
                "A positive ICA bell is |dQ_state/dV|. Accumulated passed "
                "capacity increasing with time needs an explicit branch sign."
            ),
            "constant_resistance_voltage_map": (
                "V_internal=V_app-sigma*|I|R gives "
                "dV_internal/dV_app=1 only for constant I and R."
            ),
        },
        "direction_contract": {
            "verdict": "REACTION_DIRECTION_MUST_BE_SEPARATED_FROM_CYCLE_LABEL",
            "reason": (
                "Delithiation is a material reaction direction. 'charge' and "
                "'discharge' depend on whether the label refers to a graphite "
                "half-cell, an LCO half-cell, or the full cell. A universal "
                "sigma_d label cannot encode all three."
            ),
            "recommended_primitive": (
                "Use s_rxn=+1 for delithiation (or define the opposite once), "
                "then map instrument current and cell/half-cell cycle labels "
                "through an electrode-specific observation layer."
            ),
        },
        "claim_dispositions": [
            {
                "claim": "Charge-balance differentiation yields a sum of local transition derivatives.",
                "disposition": "PRESERVE_WITH_EXPLICIT_COORDINATE",
            },
            {
                "claim": "The normalized logistic derivative has unit area and peak Q_j/(4w_j).",
                "disposition": "PRESERVE",
            },
            {
                "claim": "Q_cell is in coulomb and I=c_rate[h^-1]*Q_cell.",
                "disposition": "REJECT_UNIT_INCONSISTENT",
            },
            {
                "claim": "One discharge/charge sign convention is electrode-independent.",
                "disposition": "REJECT_SEMANTIC_CONFLATION",
            },
            {
                "claim": "Default Q_j values carry an intrinsic coulomb unit.",
                "disposition": "UNVERIFIED_DEFAULTS_ARE_NORMALIZED_WEIGHTS",
            },
        ],
        "validation": {
            "finite": all(
                math.isfinite(value)
                for value in (
                    numerical_area,
                    numerical_peak,
                    numerical_fwhm,
                    analytic_fwhm,
                )
            ),
            "logistic_area_error_lt_1e_8": abs(numerical_area - 1.0) < 1e-8,
            "logistic_peak_error_lt_1e_12": abs(
                numerical_peak - 1.0 / (4.0 * width)
            )
            < 1e-12,
            "fwhm_relative_error_lt_1e_4": abs(
                numerical_fwhm - analytic_fwhm
            )
            / analytic_fwhm
            < 1e-4,
            "c_rate_ratio_is_3600": abs(
                legacy_facade_current_numeric / correct_current_ampere - 3600.0
            )
            < 1e-12,
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
                "area_error": result["independent_logistic_check"][
                    "area_absolute_error"
                ],
                "fwhm_relative_error": result["independent_logistic_check"][
                    "fwhm_relative_error"
                ],
                "c_rate_ratio": result["c_rate_unit_check"][
                    "legacy_to_correct_ratio"
                ],
                "graphite_capacity_sum": graphite_capacity_sum,
                "lco_capacity_sum": lco_capacity_sum,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
