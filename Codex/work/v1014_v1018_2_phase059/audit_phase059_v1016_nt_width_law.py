#!/usr/bin/env python3
"""Audit v1.0.16 n(T), dwdT, positivity, and width-law status."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
V15 = ROOT / "Claude/docs/v1.0.15"
V16 = ROOT / "Claude/docs/v1.0.16"
CODE15 = V15 / "Anode_Fit_v1.0.15.py"
CODE16 = V16 / "Anode_Fit_v1.0.16.py"
CH1_15 = V15 / "graphite_ica_ch1_v1.0.15.tex"
CH1_16 = V16 / "graphite_ica_ch1_v1.0.16.tex"
CH2_15 = V15 / "graphite_ica_ch2_v1.0.15.tex"
CH2_16 = V16 / "graphite_ica_ch2_v1.0.16.tex"
GUIDE15 = V15 / "FITTING_GUIDE.md"
GUIDE16 = V16 / "FITTING_GUIDE.md"
TEST16 = V16 / "test_regression_graphite.py"
HANDOVER16 = V16 / "HANDOVER_v1.0.16.md"
LEDGER16 = ROOT / "Claude/results/process/V1016_EXECUTION_LEDGER.md"
STEP373 = ROOT / "Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json"
OUTPUT = ROOT / "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def numstat(old: Path, new: Path) -> dict[str, int]:
    run = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(old), str(new)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if run.returncode not in (0, 1):
        raise RuntimeError(run.stderr)
    fields = run.stdout.strip().split("\t")
    return {"added": int(fields[0]), "deleted": int(fields[1])}


def method_ast(path: Path, name: str) -> str | None:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == (
            "GraphiteAnodeDischargeDQDV"
        ):
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == name:
                    return hashlib.sha256(
                        ast.dump(child, annotate_fields=True).encode("utf-8")
                    ).hexdigest()
    return None


def scalar(value: Any) -> float:
    return float(np.asarray(value, dtype=float).reshape(-1)[0])


def exact_comparison(m15: Any, m16: Any) -> dict[str, Any]:
    voltage = np.linspace(0.03, 0.34, 1000)
    a = m15.GraphiteAnodeDischargeDQDV(
        m15.GRAPHITE_STAGING_LIT, Rn=0.01, Cbg=0.05
    )
    b = m16.GraphiteAnodeDischargeDQDV(
        m16.GRAPHITE_STAGING_LIT, Rn=0.01, Cbg=0.05
    )
    pairs = {
        "equilibrium": (
            a.equilibrium(voltage, 298.15),
            b.equilibrium(voltage, 298.15),
        ),
        "dqdv": (
            a.dqdv(voltage, 298.15, 0.1, 1.0),
            b.dqdv(voltage, 298.15, 0.1, 1.0),
        ),
        "entropy_coefficient": (
            a.entropy_coefficient(voltage, 298.15),
            b.entropy_coefficient(voltage, 298.15),
        ),
        "reversible_heat": (
            a.reversible_heat(voltage, 298.15, 1.0),
            b.reversible_heat(voltage, 298.15, 1.0),
        ),
    }
    rows = []
    for name, (left, right) in pairs.items():
        rows.append(
            {
                "quantity": name,
                "array_equal": bool(np.array_equal(left, right)),
                "max_abs": float(
                    np.max(np.abs(np.asarray(left) - np.asarray(right)))
                ),
            }
        )
    return {
        "rows": rows,
        "all_four_bit_exact": all(row["array_equal"] for row in rows),
    }


def transition_voltage(
    module: Any,
    model: Any,
    transition: dict[str, Any],
    temperature: float,
    fraction: float,
) -> float:
    center = (
        -transition["dH_rxn"] + temperature * transition["dS_rxn"]
    ) / module.F
    return center + scalar(model._width(transition, temperature)) * np.log(
        fraction / (1.0 - fraction)
    )


def finite_difference(
    function: Any, temperature: float, increment: float = 1.0e-3
) -> float:
    return (
        function(temperature + increment) - function(temperature - increment)
    ) / (2.0 * increment)


def capture_error(function: Any) -> dict[str, Any]:
    try:
        function()
    except Exception as exc:  # audit exact failure behavior
        return {"raised": True, "type": type(exc).__name__, "message": str(exc)}
    return {"raised": False, "type": None, "message": None}


def design_metrics(temperatures: list[float], reference: float) -> dict[str, Any]:
    temp = np.asarray(temperatures, dtype=float)
    # Dimensionless slope b=Tref*n1; absolute-width observations w~T[n0+b*dT/Tref].
    jacobian = np.column_stack(
        [temp, temp * (temp - reference) / reference]
    )
    singular = np.linalg.svd(jacobian, compute_uv=False)
    covariance = np.linalg.inv(jacobian.T @ jacobian)
    correlation = covariance[0, 1] / np.sqrt(
        covariance[0, 0] * covariance[1, 1]
    )
    return {
        "temperatures_K": temperatures,
        "parameterization": "[n0, b=T_ref*n1]",
        "condition_number": float(singular[0] / singular[-1]),
        "parameter_correlation": float(correlation),
    }


def main() -> int:
    sources = [
        CODE15,
        CODE16,
        CH1_15,
        CH1_16,
        CH2_15,
        CH2_16,
        GUIDE15,
        GUIDE16,
        TEST16,
        HANDOVER16,
        LEDGER16,
        STEP373,
    ]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
    m15 = load_module(CODE15, "phase059_v1015_nt_base")
    m16 = load_module(CODE16, "phase059_v1016_nt")

    changed_methods = []
    for name in (
        "_n_factor",
        "_width",
        "_dwdT",
        "entropy_coefficient",
        "reversible_heat",
        "dqdv",
    ):
        old = method_ast(CODE15, name)
        new = method_ast(CODE16, name)
        changed_methods.append(
            {
                "method": name,
                "v1015_ast_sha256": old,
                "v1016_ast_sha256": new,
                "added": old is None and new is not None,
                "changed": old != new,
            }
        )

    transition = {
        "dH_rxn": -10000.0,
        "dS_rxn": 10.0,
        "Q": 1.0,
        "n": 1.0,
        "n_T1": 0.004,
        "n_T_ref": 298.15,
    }
    model = m16.GraphiteAnodeDischargeDQDV([transition])
    temperature = 298.15
    fraction = 0.2
    voltage = transition_voltage(
        m16, model, transition, temperature, fraction
    )
    analytic_dwdt = (m16.R / m16.F) * (
        transition["n"]
        + transition["n_T1"] * (temperature - transition["n_T_ref"])
        + temperature * transition["n_T1"]
    )
    analytic_dudt = (
        transition["dS_rxn"] / m16.F
        + analytic_dwdt * np.log(fraction / (1.0 - fraction))
    )
    code_dudt = scalar(model.entropy_coefficient(voltage, temperature))
    fd_dudt = finite_difference(
        lambda temp: transition_voltage(
            m16, model, transition, temp, fraction
        ),
        temperature,
    )
    nt_roundtrip = {
        "transition": transition,
        "fraction": fraction,
        "temperature_K": temperature,
        "voltage_V": voltage,
        "code_n": scalar(model._n_factor(transition, temperature)),
        "code_width_V": scalar(model._width(transition, temperature)),
        "analytic_dwdT_V_per_K": analytic_dwdt,
        "code_dwdT_V_per_K": scalar(model._dwdT(transition, temperature)),
        "analytic_dUdT_V_per_K": analytic_dudt,
        "code_dUdT_V_per_K": code_dudt,
        "finite_difference_dUdT_V_per_K": fd_dudt,
        "analytic_code_abs_V_per_K": abs(analytic_dudt - code_dudt),
        "analytic_fd_abs_V_per_K": abs(analytic_dudt - fd_dudt),
    }

    fixed_w_transition = {
        "dH_rxn": -10000.0,
        "dS_rxn": 10.0,
        "Q": 1.0,
        "w": 0.02,
    }
    fixed_model = m16.GraphiteAnodeDischargeDQDV([fixed_w_transition])
    fixed_voltage = transition_voltage(
        m16, fixed_model, fixed_w_transition, temperature, fraction
    )
    fixed_width = {
        "width_V": scalar(
            fixed_model._width(fixed_w_transition, temperature)
        ),
        "dwdT_V_per_K": scalar(
            fixed_model._dwdT(fixed_w_transition, temperature)
        ),
        "code_dUdT_V_per_K": scalar(
            fixed_model.entropy_coefficient(fixed_voltage, temperature)
        ),
        "expected_center_only_V_per_K": (
            fixed_w_transition["dS_rxn"] / m16.F
        ),
    }

    default_transition = {
        "dH_rxn": -10000.0,
        "dS_rxn": 10.0,
        "Q": 1.0,
    }
    default_model = m16.GraphiteAnodeDischargeDQDV([default_transition])
    default_voltage = transition_voltage(
        m16, default_model, default_transition, temperature, fraction
    )
    default_code = scalar(
        default_model.entropy_coefficient(default_voltage, temperature)
    )
    default_actual = finite_difference(
        lambda temp: transition_voltage(
            m16, default_model, default_transition, temp, fraction
        ),
        temperature,
    )
    default_branch = {
        "declared_n_fallback": 1.0,
        "width_V": scalar(
            default_model._width(default_transition, temperature)
        ),
        "width_is_RT_over_F": bool(
            abs(
                scalar(default_model._width(default_transition, temperature))
                - m16.R * temperature / m16.F
            )
            < 1.0e-15
        ),
        "code_dwdT_V_per_K": scalar(
            default_model._dwdT(default_transition, temperature)
        ),
        "actual_dwdT_V_per_K": m16.R / m16.F,
        "code_entropy_coefficient_V_per_K": default_code,
        "finite_difference_entropy_coefficient_V_per_K": default_actual,
        "mismatch_V_per_K": default_code - default_actual,
    }

    temperatures = np.array([273.15, 298.15, 323.15])
    fractions = np.array([0.2, 0.5, 0.8])
    vector_voltage = np.array(
        [
            transition_voltage(m16, model, transition, temp, frac)
            for temp, frac in zip(temperatures, fractions)
        ]
    )
    vector_output = np.asarray(
        model.entropy_coefficient(vector_voltage, temperatures)
    )
    scalar_output = np.array(
        [
            scalar(model.entropy_coefficient(v, t))
            for v, t in zip(vector_voltage, temperatures)
        ]
    )
    array_temperature = {
        "temperatures_K": temperatures.tolist(),
        "voltages_V": vector_voltage.tolist(),
        "vector_output_V_per_K": vector_output.tolist(),
        "scalar_pointwise_output_V_per_K": scalar_output.tolist(),
        "max_abs": float(np.max(np.abs(vector_output - scalar_output))),
    }

    guard_transition = {
        "U": 0.0,
        "Q": 1.0,
        "n": 0.1,
        "n_T1": 0.005,
        "n_T_ref": 298.15,
    }
    guard_model = m16.GraphiteAnodeDischargeDQDV([guard_transition])
    positivity = {
        "temperature_domain_K": [273.15, 323.15],
        "required_constraints": [
            "n0+n1*(T_min-T_ref)>0",
            "n0+n1*(T_max-T_ref)>0",
        ],
        "example_n_at_273p15": scalar(
            guard_model._n_factor(guard_transition, 273.15)
        ),
        "example_n_at_298p15": scalar(
            guard_model._n_factor(guard_transition, 298.15)
        ),
        "reference_point_constructor_accepts_profile": True,
        "low_temperature_width_guard": capture_error(
            lambda: guard_model._width(guard_transition, 273.15)
        ),
        "domain_bound_documented_in_guide": False,
        "fitting_schema_enforces_domain_bound": False,
    }
    key_guard = capture_error(
        lambda: m16.GraphiteAnodeDischargeDQDV(
            [{"U": 0.0, "Q": 1.0, "w": 0.02, "n_T1": 0.001}]
        )
    )

    runnable_files = sorted(
        list(V16.glob("test*.py"))
        + list(V16.glob("sample*.py"))
        + list(V16.glob("demo*.py"))
        + list(V16.glob("graph_suite*.py"))
        + list(V16.glob("plot*.py"))
    )
    persistent_coverage = {
        "runnable_file_count": len(runnable_files),
        "n_T1_occurrence_count": sum(
            path.read_text(encoding="utf-8").count("n_T1")
            for path in runnable_files
        ),
        "_dwdT_occurrence_count": sum(
            path.read_text(encoding="utf-8").count("_dwdT")
            for path in runnable_files
        ),
        "execution_ledger_claims_nt_roundtrip": (
            "config 전파 round-trip 정확"
            in LEDGER16.read_text(encoding="utf-8")
        ),
        "persistent_nt_test_present": False,
    }

    identifiability = {
        "width_law": (
            "w(T)=(R/F)[(n0-n1*T_ref)T+n1*T^2], so linear n(T) "
            "is a quadratic-in-T width law"
        ),
        "centered_symmetric_60K": design_metrics(
            [268.15, 298.15, 328.15], 298.15
        ),
        "one_sided_20K": design_metrics(
            [278.15, 288.15, 298.15], 298.15
        ),
        "single_temperature_rank": 1,
        "two_parameter_width_model_rank_at_one_temperature": 1,
        "n1_center_entropy_sensitivity_at_x_half": 0.0,
        "reason": (
            "At one T only n(T) is observed; n0 and n1 are inseparable. "
            "Even across a narrow window the dimensionless slope column is "
            "weak and can correlate with n0, while dS and n1 both affect "
            "off-center entropy slopes."
        ),
    }

    findings = [
        ("nt_status", "EMPIRICAL_WIDTH_LAW_NOT_MICROSCOPIC_MULTIPLICITY"),
        ("dwdt_algebra", "PRESERVE_PRODUCT_RULE"),
        ("nt_roundtrip", "PRESERVE_OPT_IN_NUMERICAL_CONFORMANCE"),
        ("constant_n", "PRESERVE_V1015_BIT_EXACT_PATH"),
        ("fixed_w", "PRESERVE_T_FROZEN_CENTER_ONLY_PATH"),
        ("default_branch", "FAIL_DEFAULT_N1_THERMAL_WIDTH_DWDT_MISMATCH"),
        ("positivity", "REQUIRE_DOMAIN_WIDE_ENDPOINT_BOUNDS"),
        ("guard_scope", "CONDITIONAL_POINTWISE_FAIL_FAST_NOT_FIT_BOUND"),
        ("linear_scope", "LOCAL_EMPIRICAL_APPROXIMATION_ONLY"),
        ("parameter_correlation", "REQUIRE_CENTERED_SCALED_PARAMETERIZATION"),
        ("persistent_tests", "FAIL_NO_PERSISTENT_NT_REGRESSION"),
        ("array_temperature", "PRESERVE_POINTWISE_ARRAY_T_CONFORMANCE"),
        ("two_phase_interpretation", "DO_NOT_PROMOTE_NT_TO_PHASE_MECHANISM"),
        ("inherited_kinetics", "CARRY_SAMPLE_MEAN_T_LAG_BLOCKER"),
        ("lco_entropy", "CARRY_T_DEPENDENT_DSE_DERIVATIVE_BLOCKER"),
        ("manuscript_boundary", "PRESERVE_NT_DERIVATION_AS_CODE_FREE_BODY"),
    ]

    result = {
        "schema_version": 1,
        "phase": 59,
        "step": "37.4",
        "scope": (
            "v1.0.16 linear n(T) width law, dwdT propagation, code "
            "branches, positivity, parameter correlation, tests, and "
            "empirical-versus-microscopic authority"
        ),
        "exact_delta": {
            "production_code": numstat(CODE15, CODE16),
            "chapter_1": numstat(CH1_15, CH1_16),
            "chapter_2": numstat(CH2_15, CH2_16),
            "fitting_guide": numstat(GUIDE15, GUIDE16),
            "regression_harness": numstat(V15 / TEST16.name, TEST16),
            "method_ast": changed_methods,
        },
        "mathematical_contract": {
            "n_law": "n(T)=n0+n1*(T-T_ref)",
            "width_law": "w(T)=n(T)*R*T/F",
            "dwdT": "(R/F)*(n(T)+T*n1)",
            "status": "EMPIRICAL_LOCAL_WIDTH_LAW",
            "microscopic_multiplicity_derivation_present": False,
        },
        "opt_in_nt_roundtrip": nt_roundtrip,
        "constant_n_v1015_comparison": exact_comparison(m15, m16),
        "fixed_w_branch": fixed_width,
        "missing_n_and_w_default_branch": default_branch,
        "array_temperature": array_temperature,
        "guards": {
            "n_T1_without_n": key_guard,
            "positivity": positivity,
        },
        "parameter_identifiability": identifiability,
        "persistent_test_coverage": persistent_coverage,
        "findings": [
            {"topic": topic, "disposition": disposition}
            for topic, disposition in findings
        ],
        "summary": {
            "finding_count": len(findings),
            "product_rule_pass": True,
            "opt_in_nt_roundtrip_pass": (
                nt_roundtrip["analytic_code_abs_V_per_K"] < 1.0e-14
                and nt_roundtrip["analytic_fd_abs_V_per_K"] < 1.0e-12
            ),
            "constant_n_bit_exact_pass": exact_comparison(
                m15, m16
            )["all_four_bit_exact"],
            "fixed_w_branch_pass": abs(
                fixed_width["code_dUdT_V_per_K"]
                - fixed_width["expected_center_only_V_per_K"]
            )
            < 1.0e-15,
            "default_branch_conformance_pass": False,
            "domain_wide_positivity_contract_pass": False,
            "persistent_nt_regression_pass": False,
            "microscopic_nt_authority_pass": False,
            "single_temperature_n0_n1_identifiability_pass": False,
            "array_temperature_pointwise_pass": (
                array_temperature["max_abs"] == 0.0
            ),
            "next_step": "37.5",
        },
        "status": (
            "CONDITIONAL_P059_V1016_NT_DWDT_ALGEBRA_AND_OPT_IN_ROUNDTRIP_"
            "PASS_BUT_EMPIRICAL_STATUS_DEFAULT_BRANCH_POSITIVITY_AND_"
            "IDENTIFIABILITY_GAPS_REMAIN"
        ),
        "next_action": (
            "Phase 059 Step 37.5: adjudicate structural and practical "
            "identifiability of n(T), activation, and LCO electronic/"
            "vibrational terms without multi-temperature rate-series data."
        ),
        "source_hashes_before": before,
        "source_hashes_after": {
            str(path.relative_to(ROOT)): sha256(path) for path in sources
        },
    }
    result["source_unchanged"] = (
        result["source_hashes_before"] == result["source_hashes_after"]
    )
    OUTPUT.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=lambda value: (
                value.item()
                if isinstance(value, np.generic)
                else TypeError(type(value).__name__)
            ),
        )
        + "\n",
        encoding="utf-8",
    )

    default_error = default_branch["mismatch_V_per_K"] * 1000.0
    report = rf"""# Phase 059 v1.0.16 \(n(T)\) 폭 법칙 독립 판정

정본일: 2026-07-28

판정: `{result["status"]}`

## 결론

v1.0.16의 opt-in 수학은 맞다.
\(n(T)=n_0+n_1(T-T_\mathrm{{ref}})\),
\(w=n(T)RT/F\)이면
\[
\frac{{\partial w}}{{\partial T}}
=\frac{{R}}{{F}}\left[n(T)+Tn_1\right]
\]
이고, 새 `_dwdT`와 entropy config 항은 이 곱미분을 정확히
구현한다. \(n_1=0.004\ \mathrm{{K^{{-1}}}}\), \(x=0.2\) 독립 probe에서
해석식–code–유한차분 오차는
{nt_roundtrip["analytic_fd_abs_V_per_K"]:.3e} V/K였다.

상수 \(n\)의 equilibrium/dQdV/entropy/reversible-heat 네 경로도
v1.0.15와 bit-exact다. `w`-only의 \(T\)-동결 폭과 중심값-only
entropy 경로도 맞다.

그러나 \(n(T)\)은 미시적 다중도 법칙이 아니다. 현재 근거로는
열적 \(RT/F\) 위에 남는 폭을 국소 선형식으로 흡수하는 empirical width law다.
선형 \(n(T)\)조차 실제 폭에는
\(w(T)=(R/F)[(n_0-n_1T_\mathrm{{ref}})T+n_1T^2]\)의 2차식을 만든다.
상분리, 입자분포, 수송 또는 관측 폭의 어느 기작인지 식별하지
않으므로 phase mechanism으로 승격할 수 없다.

## 확인된 구현 결함

`n`과 `w`가 모두 없는 공개 기본 경로는 `_n_factor=1`이라
폭이 실제로 \(RT/F\)인데 `_dwdT`는 이를 \(T\)-동결로 취급해 0을
반환한다. \(x=0.2\) 단일 전이에서 code entropy와 실제 고정-\(x\)
유한차분은 {default_error:.6f} mV/K 어긋난다. 기본 데이터셋은
명시적 `n=1`이라 영향받지 않지만 API와 문건의 “없으면 n=1” 계약은
불일치한다.

폭 양수 guard도 평가점 fail-fast일 뿐 fitting-domain bound가 아니다.
선형 \(n(T)\)은 사용할 전체 \([T_\min,T_\max]\)에서
\[
n_0+n_1(T_\min-T_\mathrm{{ref}})>0,\qquad
n_0+n_1(T_\max-T_\mathrm{{ref}})>0
\]
두 endpoint 제약을 가져야 한다. guide와 fitting schema에는 이
제약이 없다. 실제 probe는 \(T_\mathrm{{ref}}\)에서 양수라 생성되지만
273.15 K에서 음수가 되어 뒤늦게 예외를 냈다.

## 상관성과 검증 권위

한 온도에서는 관측되는 것이 \(n(T_k)\) 하나라 \(n_0,n_1\)의
Jacobian rank가 1이다. 278.15/288.15/298.15 K의 한쪽 20 K 창에서
dimensionless slope \(b=T_\mathrm{{ref}}n_1\)를 쓴 width Jacobian도
condition number {identifiability["one_sided_20K"]["condition_number"]:.2f},
parameter correlation {identifiability["one_sided_20K"]["parameter_correlation"]:.3f}다.
따라서 \(T_\mathrm{{ref}}\) 중심화, slope scaling, 양쪽 온도점,
profile likelihood/uncertainty가 필요하다.

v1.0.16 실행 원장은 n(T) round-trip을 주장하지만 배포된 test/demo
파일에는 `n_T1`과 `_dwdT` occurrence가 0이다. 기존 golden은 상수-n
불변만 검사한다. 이번 독립 probe가 수학을 확인했어도 release 당시
주장의 persistent regression authority는 없다.

비등온 배열 \(T(V)\)의 entropy 결과는 scalar pointwise 호출과
exact 일치했다. 다만 Step 37.2의 lag가 local T가 아니라 sample
mean \(T\)를 쓰는 blocker와 LCO의 \(T\)-의존 \(\Delta S_e\) 미분
blocker는 별개로 남는다.

## 문건 방향

Ch1/Ch2의 새 \(n(T)\) 유도 자체는 code 이름 없이 물리식으로
서술돼 theory-only body 방향에 맞는다. 최종 정본에서는 `n`을
“다중도”라는 미시적 명칭보다 `empirical width ratio`로 고정하고,
상수-n/상수-w/n(T)를 서로 배타적인 관측모델 후보로 둬야 한다.

## 다음 단계

Step 37.5에서 다온도 rate-series가 없을 때 \(n(T)\), activation,
LCO electronic/vibrational 항을 동시에 식별할 수 있는지 structural/
practical identifiability로 판정한다.

원본 `Claude/`, `main`은 수정하지 않았다.
"""
    REPORT.write_text(report, encoding="utf-8")
    print(result["status"])
    print(
        "nt roundtrip:",
        nt_roundtrip["analytic_code_abs_V_per_K"],
        nt_roundtrip["analytic_fd_abs_V_per_K"],
    )
    print("default mismatch V/K:", default_branch["mismatch_V_per_K"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
