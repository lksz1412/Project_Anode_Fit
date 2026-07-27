#!/usr/bin/env python3
"""Independently validate the v1.0.13 statistical-mechanics rederivation."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CH1 = ROOT / "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex"
CH2 = ROOT / "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex"
CODE = ROOT / "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py"
RESULT = ROOT / "Codex/results/PHASE_058_V1013_STATMECH_VALIDATION.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_line(path: Path, needle: str) -> int:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return number
    raise ValueError(f"Needle not found in {path}: {needle}")


def logistic(argument: np.ndarray | float) -> np.ndarray | float:
    argument_array = np.asarray(argument, dtype=float)
    result = np.empty_like(argument_array)
    nonnegative = argument_array >= 0.0
    result[nonnegative] = 1.0 / (1.0 + np.exp(-argument_array[nonnegative]))
    exponential = np.exp(argument_array[~nonnegative])
    result[~nonnegative] = exponential / (1.0 + exponential)
    if np.ndim(argument) == 0:
        return float(result)
    return result


def symmetric_binodal(omega_over_rt: float) -> float:
    def residual(theta: float) -> float:
        return math.log(theta / (1.0 - theta)) + omega_over_rt * (
            1.0 - 2.0 * theta
        )

    lower = 1.0e-12
    upper = 0.499999
    for _ in range(200):
        midpoint = 0.5 * (lower + upper)
        if residual(midpoint) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    return 0.5 * (lower + upper)


def main() -> int:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    constants = data["constants"]
    numeric = data["numeric_invariants"]
    temperature = constants["temperature_k"]
    gas_constant = constants["gas_constant_j_per_mol_k"]
    faraday = constants["faraday_constant_c_per_mol"]
    width = gas_constant * temperature / faraday
    fwhm = 4.0 * math.acosh(math.sqrt(2.0)) * width
    peak = 1.0 / (4.0 * width)

    checks: dict[str, bool] = {}
    checks["schema"] = (
        data["schema_version"] == "phase058-v1013-statmech-validation-v1"
    )
    checks["boundary"] = (
        data["audit_boundary"]
        == "INDEPENDENT_STANDARD_STATISTICAL_MECHANICS_REDERIVATION_NOT_EXTERNAL_VALIDATION"
    )
    checks["chapter_1_hash"] = (
        sha256(CH1) == data["sources"]["chapter_1_sha256"]
    )
    checks["chapter_2_hash"] = (
        sha256(CH2) == data["sources"]["chapter_2_sha256"]
    )
    checks["production_code_hash"] = (
        sha256(CODE) == data["sources"]["production_code_sha256"]
    )

    evidence_needles = {
        "chapter_2_single_site_partition_line": (
            CH2,
            "Z_1 \\;=\\; \\sum_{n=0,1}",
        ),
        "chapter_2_ideal_logistic_line": (
            CH2,
            "\\boxed{\\;\\theta_\\eq(V,T)",
        ),
        "chapter_1_ideal_chemical_potential_line": (
            CH1,
            "\\boxed{\\;\\mu(\\theta)=\\mu^0+RT",
        ),
        "chapter_1_regular_solution_chemical_potential_line": (
            CH1,
            "\\mu_\\mathrm{Li}(\\theta)=\\mu^0+RT",
        ),
        "chapter_1_ideal_logistic_line": (
            CH1,
            "\\boxed{\\;\\theta_\\eq(V,T)",
        ),
        "chapter_1_nonideal_not_logistic_line": (
            CH1,
            "$\\Omega_j\\ne0$ 이면 닫힌 logistic 이 아니다",
        ),
        "chapter_1_width_generalization_line": (
            CH1,
            "평형 진행률의 폭 척도는 이상 극한에서",
        ),
        "chapter_1_directional_equilibrium_line": (
            CH1,
            "\\boxed{\\;\\xi_{\\eq,j}(V,T)=",
        ),
        "chapter_1_capacity_sum_line": (
            CH1,
            "Q_\\cell q=Q_\\bg(V_n)+\\sum_jQ_j\\xi_j",
        ),
    }
    for key, (path, needle) in evidence_needles.items():
        checks[f"source_line_{key}"] = (
            source_line(path, needle) == data["source_evidence"][key]
        )

    checks["ideal_width"] = math.isclose(
        width, numeric["ideal_width_v"], rel_tol=0.0, abs_tol=1.0e-15
    )
    checks["ideal_fwhm"] = math.isclose(
        fwhm, numeric["ideal_fwhm_v"], rel_tol=0.0, abs_tol=1.0e-15
    )
    checks["ideal_peak"] = math.isclose(
        peak, numeric["ideal_peak_per_v"], rel_tol=0.0, abs_tol=1.0e-12
    )

    center = 0.1
    voltage = np.linspace(center - 30.0 * width, center + 30.0 * width, 300001)
    chemical_potential = -faraday * (voltage - center)
    grand_weight = np.exp(chemical_potential / (gas_constant * temperature))
    theta_partition = grand_weight / (1.0 + grand_weight)
    xi_partition = 1.0 - theta_partition
    xi_logistic = np.asarray(
        logistic(faraday * (voltage - center) / (gas_constant * temperature))
    )
    partition_logistic_error = float(
        np.max(np.abs(xi_partition - xi_logistic))
    )
    ideal_profile = xi_logistic * (1.0 - xi_logistic) / width
    ideal_area = float(np.trapezoid(ideal_profile, voltage))
    checks["partition_equals_logistic"] = partition_logistic_error < 3.0e-16
    checks["ideal_area"] = (
        abs(ideal_area - numeric["ideal_area"]) < 3.0e-13
    )
    checks["ideal_half_max"] = all(
        math.isclose(
            float(
                logistic((offset * fwhm / 2.0) / width)
                * (1.0 - logistic((offset * fwhm / 2.0) / width))
                / width
            ),
            peak / 2.0,
            rel_tol=0.0,
            abs_tol=2.0e-14,
        )
        for offset in (-1.0, 1.0)
    )

    g0 = 1.0
    g1 = numeric["degeneracy_ratio_g1_over_g0"]
    degeneracy_shift = width * math.log(g1 / g0)
    checks["degeneracy_shift"] = math.isclose(
        degeneracy_shift,
        numeric["degeneracy_center_shift_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["degeneracy_does_not_change_fwhm"] = math.isclose(
        fwhm,
        numeric["degeneracy_fwhm_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    capacities = np.asarray(numeric["multi_transition_capacities"])
    centers = np.asarray([-0.15, 0.05, 0.25])
    broad_voltage = np.linspace(-1.5, 1.5, 600001)
    total_profile = np.zeros_like(broad_voltage)
    for capacity, transition_center in zip(capacities, centers, strict=True):
        progress = np.asarray(
            logistic((broad_voltage - transition_center) / width)
        )
        total_profile += capacity * progress * (1.0 - progress) / width
    multi_area = float(np.trapezoid(total_profile, broad_voltage))
    checks["capacity_weights_sum"] = math.isclose(
        float(np.sum(capacities)),
        numeric["multi_transition_total_area"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["multi_transition_area"] = abs(
        multi_area - numeric["multi_transition_total_area"]
    ) < 2.0e-14

    xi = 0.8
    omega = numeric["subcritical_omega_over_rt"] * gas_constant * temperature
    regular_minus_ideal = omega * (1.0 - 2.0 * xi) / faraday
    center_equivalent_width = (
        gas_constant * temperature - omega / 2.0
    ) / faraday
    checks["subcritical_not_ideal_logistic"] = math.isclose(
        regular_minus_ideal,
        numeric["subcritical_regular_minus_ideal_v_at_xi_0p8"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["subcritical_center_width"] = math.isclose(
        center_equivalent_width,
        numeric["subcritical_center_slope_equivalent_width_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    critical_omega = 2.0 * gas_constant * temperature
    critical_curvature = 4.0 * gas_constant * temperature - 2.0 * critical_omega
    checks["critical_curvature"] = (
        critical_curvature == numeric["critical_curvature_j_per_mol"] == 0.0
    )

    omega_over_rt = numeric["binodal_omega_over_rt"]
    theta_low = symmetric_binodal(omega_over_rt)
    theta_high = 1.0 - theta_low
    binodal_residual = math.log(theta_low / (1.0 - theta_low)) + omega_over_rt * (
        1.0 - 2.0 * theta_low
    )
    checks["binodal_low"] = math.isclose(
        theta_low,
        numeric["binodal_theta_low"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["binodal_high"] = math.isclose(
        theta_high,
        numeric["binodal_theta_high"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["binodal_residual"] = abs(binodal_residual) < 1.0e-14

    dispositions = data["claim_dispositions"]
    identifiers = [item["id"] for item in dispositions]
    checks["claim_count"] = len(dispositions) == 13
    checks["claim_ids_unique"] = len(identifiers) == len(set(identifiers))
    checks["underived_n_handoff"] = any(
        item["id"] == "SM13-13"
        and item["disposition"] == "REJECT_UNDERIVED_MODEL_FORM_HANDOFF_TO_STEP_31_2"
        for item in dispositions
    )
    internal = data["source_internal_consistency"]
    checks["source_flags_nonideal"] = (
        internal["correctly_limits_closed_logistic_to_omega_zero"]
        and internal["also_overstates_rt_over_f_for_all_subcritical_regular_solutions"]
    )
    checks["direction_boundary_recorded"] = (
        internal["uses_fixed_s_plus_one_in_first_principles_equilibrium_derivation"]
        and internal["later_reintroduces_sigma_d_into_an_equilibrium_named_quantity"]
    )

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "artifact": str(RESULT.relative_to(ROOT)),
                "check_count": len(checks),
                "failures": failures,
                "partition_logistic_max_abs_error": partition_logistic_error,
                "ideal_area_numeric": ideal_area,
                "multi_transition_area_numeric": multi_area,
                "binodal_theta_low": theta_low,
                "binodal_residual": binodal_residual,
                "verdict": data["verdict"],
                "gate": (
                    "PASS_P058_V1013_STATMECH_REDERIVATION"
                    if not failures
                    else "FAIL_P058_V1013_STATMECH_REDERIVATION"
                ),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
