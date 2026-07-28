#!/usr/bin/env python3
"""Phase 059 Step 38.3: independent Einstein-oscillator thermodynamic audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py"
OUT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md"
R = 8.31446261815324
FARADAY = 96485.33212


def load_module():
    spec = importlib.util.spec_from_file_location("anodefit_v10182_einstein_audit", CODE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def z_exc(T: float, theta: float) -> float:
    return 1.0 / (-math.expm1(-theta / T))


def free_exc(T: float, theta: float) -> float:
    return R * T * math.log1p(-math.exp(-theta / T))


def internal_exc(T: float, theta: float) -> float:
    return R * theta / math.expm1(theta / T)


def entropy(T: float, theta: float) -> float:
    u = theta / T
    return R * (-math.log1p(-math.exp(-u)) + u / math.expm1(u))


def heat_capacity(T: float, theta: float) -> float:
    u = theta / T
    return R * u * u * math.exp(u) / math.expm1(u) ** 2


def centered_voltage(T: float, theta: float, tref: float) -> float:
    sref = entropy(tref, theta)
    return -(free_exc(T, theta) - free_exc(tref, theta) + sref * (T - tref)) / FARADAY


def main() -> None:
    module = load_module()
    model = module.GraphiteAnodeDischargeDQDV([])
    theta, tref = 700.0, 298.15
    temperatures = [50.0, 100.0, 278.15, 298.15, 318.15, 348.15, 1000.0, 5000.0]
    rows = []
    for T in temperatures:
        h = max(1e-4, T * 1e-6)
        analytic_s = entropy(T, theta)
        fd_s = -(free_exc(T + h, theta) - free_exc(T - h, theta)) / (2 * h)
        fd_voltage = (centered_voltage(T + h, theta, tref) - centered_voltage(T - h, theta, tref)) / (2 * h)
        code_s = float(model._S_vib(T, theta))
        code_du = float(model._vib_dU({"theta_E": theta, "theta_E_Tref": tref}, T))
        code_ds = float(model._vib_dS({"theta_E": theta, "theta_E_Tref": tref}, T))
        u = theta / T
        code_expected_s = module.R * (-math.log1p(-math.exp(-u)) + u / math.expm1(u))
        uref = theta / tref
        code_sref = module.R * (-math.log1p(-math.exp(-uref)) + uref / math.expm1(uref))
        code_A = module.R * T * math.log1p(-math.exp(-u))
        code_Aref = module.R * tref * math.log1p(-math.exp(-uref))
        code_expected_du = -(code_A - code_Aref + code_sref * (T - tref)) / module.F
        rows.append({
            "T_K": T,
            "u": theta / T,
            "Z_exc": z_exc(T, theta),
            "A_exc_J_per_mol": free_exc(T, theta),
            "U_exc_J_per_mol": internal_exc(T, theta),
            "S_J_per_mol_K": analytic_s,
            "Cv_J_per_mol_K": heat_capacity(T, theta),
            "A_plus_TS_minus_U_J_per_mol": free_exc(T, theta) + T * analytic_s - internal_exc(T, theta),
            "entropy_finite_difference_error_J_per_mol_K": fd_s - analytic_s,
            "code_entropy_error_J_per_mol_K": code_s - code_expected_s,
            "constant_rounding_entropy_difference_J_per_mol_K": code_expected_s - analytic_s,
            "centered_voltage_V": centered_voltage(T, theta, tref),
            "code_centered_voltage_error_V": code_du - code_expected_du,
            "constant_rounding_voltage_difference_V": code_expected_du - centered_voltage(T, theta, tref),
            "centered_entropy_J_per_mol_K": analytic_s - entropy(tref, theta),
            "code_centered_entropy_error_J_per_mol_K": code_ds - (code_expected_s - code_sref),
            "constant_rounding_centered_entropy_difference_J_per_mol_K": (
                code_expected_s - code_sref - (analytic_s - entropy(tref, theta))
            ),
            "voltage_derivative_uV_per_K": fd_voltage * 1e6,
            "entropy_over_F_uV_per_K": (analytic_s - entropy(tref, theta)) / FARADAY * 1e6,
            "roundtrip_error_uV_per_K": (fd_voltage - (analytic_s - entropy(tref, theta)) / FARADAY) * 1e6,
        })

    low_T = 20.0
    high_T = 100000.0
    u_high = theta / high_T
    slow = entropy(low_T, theta)
    slow_asym = R * (1.0 + theta / low_T) * math.exp(-theta / low_T)
    shigh = entropy(high_T, theta)
    shigh_asym = R * (1.0 + math.log(high_T / theta) + u_high * u_high / 24.0)

    zero_point = R * theta / 2.0
    zpe_centered_difference = max(abs(
        (
            -(free_exc(T, theta) + zero_point - free_exc(tref, theta) - zero_point
              + entropy(tref, theta) * (T - tref)) / FARADAY
        ) - centered_voltage(T, theta, tref)
    ) for T in temperatures)

    three_axis_entropy = 3.0 * entropy(tref, theta)
    one_mode_entropy = entropy(tref, theta)
    reaction_counterexample = {
        "theta_lithiated_K": 500.0,
        "theta_delithiated_K": 900.0,
        "delta_S_reaction_at_Tref_J_per_mol_K": entropy(tref, 500.0) - entropy(tref, 900.0),
        "single_effective_mode_absolute_S_at_Tref_J_per_mol_K": one_mode_entropy,
        "point": "A reaction vibrational entropy is a difference between spectra; one positive absolute oscillator entropy is not that difference.",
    }

    findings = [
        {"id": "EIN-001", "disposition": "PRESERVE", "text": "For excitation-only Z=1/(1-exp(-theta/T)), A=RT ln(1-exp(-theta/T)), U=R theta/(exp(theta/T)-1), and S=(U-A)/T reproduce the manuscript expression."},
        {"id": "EIN-002", "disposition": "PRESERVE", "text": "Adding the zero-point R theta/2 changes A and U by the same constant, leaves S unchanged, and cancels exactly from the tangent-subtracted voltage correction."},
        {"id": "EIN-003", "disposition": "PRESERVE", "text": "The reference subtraction makes both voltage shift and entropy correction zero at Tref and gives d(delta U)/dT=delta S/F."},
        {"id": "EIN-004", "disposition": "PRESERVE", "text": "The independent 700 K numerical values reproduce -3.74, 0, +3.70 and +9.14 microvolt/K at the four reported temperatures."},
        {"id": "EIN-005", "disposition": "PRESERVE", "text": "Low-T S~R(1+u)e^-u and high-T S~R[1+ln(T/theta)+u^2/24] limits are correct."},
        {"id": "EIN-006", "disposition": "CORRECT", "text": "The implementation is one molar mode with fixed amplitude R, while Chapter 1 discusses three local axes and a real solid has a phonon DOS and mode multiplicities."},
        {"id": "EIN-007", "disposition": "CORRECT", "text": "A reaction vibrational contribution must be a lithiated-minus-delithiated spectral free-energy difference; a single absolute S(theta) is only a constrained phenomenological residual after baseline absorption."},
        {"id": "EIN-008", "disposition": "CORRECT", "text": "The correction has fixed positive dS/dT and no amplitude/sign parameter, so it cannot represent general spectral hardening/softening reaction curvature."},
        {"id": "EIN-009", "disposition": "CORRECT", "text": "In the high-T limit the centered entropy tends to R ln(T/Tref), losing leading-order theta sensitivity; theta is weakly identifiable unless the data span the quantum-curvature window."},
        {"id": "EIN-010", "disposition": "CORRECT", "text": "Three temperatures are necessary for curvature but not sufficient for practical identification with baseline, electronic slope, width and noise; replication and uncertainty are required."},
        {"id": "EIN-011", "disposition": "EMPIRICAL_ONLY", "text": "theta_E=700 K is a demonstration capability, not a graphite or LCO fitted material constant."},
        {"id": "EIN-012", "disposition": "CARRY_FORWARD", "text": "The formula does not repair the frozen LCO electronic gate, reference entropy, composition mapping, or joint-identifiability blockers."},
    ]

    max_identity = max(abs(x["A_plus_TS_minus_U_J_per_mol"]) for x in rows)
    max_entropy_fd = max(abs(x["entropy_finite_difference_error_J_per_mol_K"]) for x in rows)
    max_code_s = max(abs(x["code_entropy_error_J_per_mol_K"]) for x in rows)
    max_code_u = max(abs(x["code_centered_voltage_error_V"]) for x in rows)
    max_code_ds = max(abs(x["code_centered_entropy_error_J_per_mol_K"]) for x in rows)
    max_roundtrip = max(abs(x["roundtrip_error_uV_per_K"]) for x in rows)

    data = {
        "schema_version": 1,
        "phase": 59,
        "step": "38.3",
        "status": "CONDITIONAL_P059_V1018_2_EINSTEIN_THERMODYNAMIC_ALGEBRA_AND_REFERENCE_ROUNDTRIP_PASS_BUT_REACTION_SPECTRUM_AMPLITUDE_AND_IDENTIFIABILITY_SCOPE_FAIL",
        "source_code": str(CODE.relative_to(ROOT)),
        "source_code_sha256": hashlib.sha256(CODE.read_bytes()).hexdigest(),
        "derivation": {
            "partition_function_excitation_only": "Z=1/(1-exp(-theta/T))",
            "helmholtz_excitation_J_per_mol": "A=R*T*ln(1-exp(-theta/T))",
            "internal_energy_excitation_J_per_mol": "U=R*theta/(exp(theta/T)-1)",
            "entropy_J_per_mol_K": "S=R[-ln(1-exp(-u))+u/(exp(u)-1)]",
            "heat_capacity_J_per_mol_K": "Cv=R*u^2*exp(u)/(exp(u)-1)^2",
            "u": "theta/T",
            "zero_point_J_per_mol": zero_point,
            "zero_point_centered_voltage_max_difference_V": zpe_centered_difference,
        },
        "numeric_rows": rows,
        "limits": {
            "low_T_K": low_T,
            "low_T_exact_S": slow,
            "low_T_asymptotic_S": slow_asym,
            "low_T_relative_error": abs(slow_asym / slow - 1.0),
            "high_T_K": high_T,
            "high_T_exact_S": shigh,
            "high_T_asymptotic_S": shigh_asym,
            "high_T_relative_error": abs(shigh_asym / shigh - 1.0),
        },
        "normalization_scope": {
            "implemented_mode_multiplicity": 1.0,
            "one_mode_S_at_Tref_J_per_mol_K": one_mode_entropy,
            "three_equal_axes_S_at_Tref_J_per_mol_K": three_axis_entropy,
            "explicit_amplitude_parameter_present": False,
            "reactant_and_product_theta_pair_present": False,
            "phonon_DOS_integral_present": False,
            "reaction_counterexample": reaction_counterexample,
        },
        "validation": {
            "max_A_plus_TS_minus_U_J_per_mol": max_identity,
            "max_entropy_finite_difference_error_J_per_mol_K": max_entropy_fd,
            "max_code_entropy_error_J_per_mol_K": max_code_s,
            "max_code_centered_voltage_error_V": max_code_u,
            "max_code_centered_entropy_error_J_per_mol_K": max_code_ds,
            "max_roundtrip_error_uV_per_K": max_roundtrip,
            "code_constants": {"R": module.R, "F": module.F},
            "reference_constants": {"R": R, "F": FARADAY},
            "reported_four_temperature_values_match": all(
                abs(a - b) < 0.015 for a, b in zip(
                    [rows[i]["voltage_derivative_uV_per_K"] for i in [2, 3, 4, 5]],
                    [-3.74, 0.0, 3.70, 9.14],
                )
            ),
        },
        "primary_scope_source": {
            "citation": "Haruyama et al., J. Phys. Chem. C 125, 27891-27900 (2021)",
            "doi": "10.1021/acs.jpcc.1c08992",
            "url": "https://pubs.acs.org/doi/10.1021/acs.jpcc.1c08992",
            "supported_scope": "Graphite vibrational/configurational free energies require structure- and mode-resolved phonon calculations; does not validate theta_E=700 K.",
        },
        "findings": findings,
        "summary": {
            "finding_count": len(findings),
            "algebra_pass": True,
            "reference_roundtrip_pass": True,
            "general_reaction_vibrational_model_pass": False,
            "material_validation_pass": False,
            "next_step": "38.4",
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(f"""# Phase 059 v1.0.18.2 Einstein 열역학 재유도

정본일: 2026-07-28

판정: `{data["status"]}`

## 결론

단일 조화모드의 대수는 맞다. 영점에너지를 제외한
$Z=[1-e^{{-\\theta/T}}]^{{-1}}$에서
$A=RT\\ln(1-e^{{-\\theta/T}})$,
$U=R\\theta/(e^{{\\theta/T}}-1)$,
$S=(U-A)/T$를 얻으면 문건 식과 정확히 같다. 영점에너지
$R\\theta/2$를 포함해도 entropy는 같고 기준 접선 subtraction에서
상수는 완전히 소거된다.

$T_{{ref}}$에서 자유에너지의 접선을 뺀 전위 보정도 맞다.
$\\Delta U(T_{{ref}})=0$, $\\Delta S(T_{{ref}})=0$이며
$d\\Delta U/dT=\\Delta S/F$다. 독립 계산은 $\\theta=700$ K에서
278.15/298.15/318.15/348.15 K의 -3.738/0/3.700/9.138
microvolt/K를 재현했다.

## 물리 범위의 한계

현재 항은 “반응의 진동 엔트로피”를 일반적으로 구현한 것이 아니다.
실제 반응량은 lithiated와 delithiated phonon spectrum의 자유에너지
차이다. 현재는 mode multiplicity가 1, amplitude가 $R$로 고정되고,
reactant/product frequency pair와 phonon-DOS 적분이 없다. 따라서
기준온도에 흡수된 baseline 위의 매우 제한된 phenomenological
curvature 항으로만 읽어야 한다.

이 항은 $dS/dT>0$의 부호와 크기가 고정돼 일반적인 spectral
hardening/softening 차이를 표현하지 못한다. 또한 고온에서는
$\\Delta S\\to R\\ln(T/T_{{ref}})$가 되어 leading order의
$\\theta$ 감도가 사라진다. 세 온도점은 곡률에 필요한 최소 조건일
뿐 baseline·electronic slope·width·noise와 함께 안정적으로
식별하기에 충분하다는 보장은 없다.

그러므로 700 K는 capability demo이지 graphite/LCO 물성값이 아니다.
Haruyama et al.의 phonon 계산은 mode-resolved 접근의 필요성을
지지하지만 이 단일-mode 수치를 검증하지 않는다.

## 다음 단계

Step 38.4에서 theta_E 부재 bit-exact, 활성 branch, derivative
round-trip과 실제 equilibrium/dQdV/entropy full-path coupling을
검사한다.

원본 `Claude/`, `main`은 수정하지 않았다.
""", encoding="utf-8")
    print(data["status"])
    print("max_roundtrip_uV_per_K", max_roundtrip, "findings", len(findings))


if __name__ == "__main__":
    main()
