#!/usr/bin/env python3
"""Audit joint identifiability in v1.0.16 without multi-T rate-series."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / "Claude/docs/v1.0.16/Anode_Fit_v1.0.16.py"
CH1 = ROOT / "Claude/docs/v1.0.16/graphite_ica_ch1_v1.0.16.tex"
CH2 = ROOT / "Claude/docs/v1.0.16/graphite_ica_ch2_v1.0.16.tex"
GUIDE = ROOT / "Claude/docs/v1.0.16/FITTING_GUIDE.md"
STEP364 = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json"
STEP363 = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json"
STEP374 = ROOT / "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json"
OUTPUT = ROOT / "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix_metrics(matrix: np.ndarray, names: list[str]) -> dict[str, Any]:
    matrix = np.asarray(matrix, dtype=float)
    singular = np.linalg.svd(matrix, compute_uv=False)
    tolerance = max(matrix.shape) * np.finfo(float).eps * singular[0]
    rank = int(np.sum(singular > tolerance))
    return {
        "parameter_names": names,
        "shape": list(matrix.shape),
        "rank": rank,
        "nullity": len(names) - rank,
        "singular_values": singular.tolist(),
        "matrix": matrix.tolist(),
    }


def finite_gradient(function: Any, point: np.ndarray, steps: np.ndarray) -> np.ndarray:
    gradient = []
    for index, step in enumerate(steps):
        plus = point.copy()
        minus = point.copy()
        plus[index] += step
        minus[index] -= step
        gradient.append((function(plus) - function(minus)) / (2.0 * step))
    return np.asarray(gradient)


def main() -> int:
    sources = [CODE, CH1, CH2, GUIDE, STEP364, STEP363, STEP374]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
    module = load_module(CODE, "phase059_v1016_ident")
    kinetics_prior = json.loads(STEP364.read_text(encoding="utf-8"))
    lco_prior = json.loads(STEP363.read_text(encoding="utf-8"))
    nt_prior = json.loads(STEP374.read_text(encoding="utf-8"))

    tref = 298.15
    # At one T, every voltage datum depends on n0,n1 through n(T) only.
    single_t_nt = matrix_metrics(
        np.tile([1.0, 0.0], (200, 1)),
        ["n0", "n1"],
    )
    multi_t_nt = matrix_metrics(
        np.column_stack(
            [
                np.ones(3),
                np.asarray([268.15, 298.15, 328.15]) - tref,
            ]
        ),
        ["n0", "n1"],
    )

    # log L = known(T,I,A)+dH/(RT)-dS/R+log|dV/dq|.
    def activation_design(temperatures: list[float], rates: list[float]) -> np.ndarray:
        rows = []
        for temperature in temperatures:
            for _rate in rates:
                rows.append(
                    [
                        1.0 / (module.R * temperature),
                        -1.0 / module.R,
                        1.0,
                    ]
                )
        return np.asarray(rows)

    activation_one_t_many_rates = matrix_metrics(
        activation_design([tref], [0.02, 0.1, 0.5, 1.0]),
        ["dH_a", "dS_a", "log_dVdq_qa"],
    )
    activation_many_t_many_rates = matrix_metrics(
        activation_design(
            [268.15, 298.15, 328.15], [0.02, 0.1, 0.5, 1.0]
        ),
        ["dH_a", "dS_a", "log_dVdq_qa"],
    )
    activation_exact_null = {
        "vector": [0.0, module.R, 1.0],
        "meaning": (
            "dS_a -> dS_a+R*c and log_dVdq -> log_dVdq+c leave "
            "log L unchanged; one must be fixed by independent data."
        ),
    }

    lco_transition = module.LCO_MSMR_LIT[0]
    point = np.array(
        [
            lco_transition["dS_rxn"],
            lco_transition["g_max_eV"],
            lco_transition["x_MIT"],
            lco_transition["dx_MIT"],
        ],
        dtype=float,
    )

    def effective_entropy(parameters: np.ndarray) -> float:
        dS, gmax, xmit, dx = parameters
        return float(
            dS
            + module.func_dSe_molar(
                lco_transition["x_center"], 298.15, gmax, xmit, dx
            )
        )

    gate_gradient = finite_gradient(
        effective_entropy,
        point,
        np.array([1.0e-4, 1.0e-4, 1.0e-6, 1.0e-6]),
    )
    # All V/T rows multiply this same frozen scalar gradient by a transition weight.
    synthetic_weights = np.linspace(0.01, 1.0, 300)
    lco_gate_design = synthetic_weights[:, None] * gate_gradient[None, :]
    lco_gate_rank = matrix_metrics(
        lco_gate_design,
        ["dS_rxn_T1", "g_max_eV", "x_MIT", "dx_MIT"],
    )

    vibrational = {
        "production_parameter_count": 0,
        "production_callable_count": 0,
        "jacobian_rank": 0,
        "status": "THEORY_ONLY_ABSORBED_IN_DS_RXN",
        "consequence": (
            "No v1.0.16 observation can estimate a vibrational residual "
            "parameter because none exists in the forward model."
        ),
    }

    scenario_matrix = [
        {
            "scenario": "single_T_single_rate",
            "n0_n1": "STRUCTURALLY_NONIDENTIFIABLE",
            "activation": "STRUCTURALLY_NONIDENTIFIABLE",
            "lco_electronic_vs_base_entropy": "STRUCTURALLY_NONIDENTIFIABLE",
            "vibrational_residual": "ABSENT",
        },
        {
            "scenario": "single_T_rate_series",
            "n0_n1": "STRUCTURALLY_NONIDENTIFIABLE",
            "activation": "ONLY_ONE_COMPOSITE_LAG_SCALE",
            "lco_electronic_vs_base_entropy": "STRUCTURALLY_NONIDENTIFIABLE",
            "vibrational_residual": "ABSENT",
        },
        {
            "scenario": "multi_T_single_rate",
            "n0_n1": "STRUCTURALLY_IDENTIFIABLE_PRACTICALLY_CONDITIONAL",
            "activation": "DH_IDENTIFIABLE_BUT_DS_PREFACTOR_NULL_REMAINS",
            "lco_electronic_vs_base_entropy": "STILL_RANK1_IN_CURRENT_CODE",
            "vibrational_residual": "ABSENT",
        },
        {
            "scenario": "multi_T_rate_series_plus_independent_priors",
            "n0_n1": "CANDIDATE",
            "activation": "CANDIDATE_IF_DVDQ_OR_PREFACTOR_FIXED",
            "lco_electronic_vs_base_entropy": (
                "REQUIRES_COMPOSITION_RESOLVED_NONFROZEN_GATE"
            ),
            "vibrational_residual": "REQUIRES_FORWARD_TERM_AND_PHONON_PRIOR",
        },
    ]

    minimum_evidence_contract = {
        "width_nt": [
            "At least two distinct temperatures; prefer points on both sides of T_ref.",
            "Per-temperature peak-width uncertainty and profile-likelihood for n1.",
            "Domain-wide n(T)>0 endpoint constraints.",
        ],
        "activation": [
            "Rate series at each of at least three temperatures.",
            "Independent dVdq_qa from quasi-equilibrium OCV or fix the prefactor.",
            "Current interruption/transport diagnostics to separate kinetic lag from transport.",
        ],
        "lco_electronic": [
            "Correct Li-reference half-cell entropy coefficient.",
            "Composition-resolved x(V,T), not a frozen x_center evaluation.",
            "Multiple temperatures spanning enough range to resolve curvature.",
            "Independent DOS/phase-coexistence priors and actual doped high-voltage data.",
        ],
        "vibrational": [
            "An explicit oscillator/phonon forward term.",
            "Independent phonon or heat-capacity prior, or a temperature range that separates its curvature.",
            "Do not infer electronic curvature while vibrational residual is unconstrained.",
        ],
    }

    findings = [
        ("n0_n1_single_temperature", "FAIL_STRUCTURAL_RANK_DEFICIENCY"),
        ("activation_single_temperature", "FAIL_ONLY_COMPOSITE_LAG_SCALE"),
        ("activation_multi_temperature", "FAIL_DS_PREFACTOR_EXACT_NULL"),
        ("rate_series_role", "REQUIRE_RATE_SERIES_FOR_MODEL_DISCRIMINATION"),
        ("lco_gate_current_code", "FAIL_FROZEN_GATE_RANK1"),
        ("lco_base_entropy", "FAIL_ELECTRONIC_BASE_ENTROPY_SEPARATION"),
        ("vibrational", "FAIL_FORWARD_TERM_ABSENT"),
        ("electronic_vibrational", "FAIL_JOINT_CURVATURE_ATTRIBUTION"),
        ("width_activation", "PRACTICAL_CORRELATION_REQUIRES_TIERED_FREEZE"),
        ("transport", "REQUIRE_TRANSPORT_DIAGNOSTICS"),
        ("data_contract", "REQUIRE_MULTI_T_RATE_AND_INDEPENDENT_PRIORS"),
        ("guide_tiering", "PRESERVE_STAGED_INTENT_NOT_COMPLETED_IDENTIFICATION"),
        ("synthetic_roundtrip", "NOT_STATISTICAL_IDENTIFIABILITY_EVIDENCE"),
        ("material_authority", "NO_GRAPHITE_LCO_SI_FIT_AUTHORITY"),
    ]

    result = {
        "schema_version": 1,
        "phase": 59,
        "step": "37.5",
        "scope": (
            "structural and practical identifiability of n(T), activation, "
            "LCO electronic, and vibrational terms without multi-temperature "
            "rate-series and independent component data"
        ),
        "rank_analyses": {
            "n0_n1_single_temperature": single_t_nt,
            "n0_n1_three_temperatures": multi_t_nt,
            "activation_one_temperature_many_rates": (
                activation_one_t_many_rates
            ),
            "activation_three_temperatures_many_rates": (
                activation_many_t_many_rates
            ),
            "activation_exact_null": activation_exact_null,
            "lco_frozen_gate": lco_gate_rank,
            "lco_frozen_gate_gradient": gate_gradient.tolist(),
            "vibrational": vibrational,
        },
        "scenario_matrix": scenario_matrix,
        "minimum_evidence_contract": minimum_evidence_contract,
        "inherited_evidence": {
            "kinetics_status": kinetics_prior["summary"]["status"],
            "lco_heat_status": lco_prior["status"],
            "nt_width_status": nt_prior["status"],
            "baseline_lag_gradient_practically_weak": True,
            "lco_reference_closure_pass": lco_prior["summary"][
                "half_cell_reference_closure_pass"
            ],
            "lco_electronic_code_conformance_pass": lco_prior["summary"][
                "theory_code_electronic_conformance_pass"
            ],
        },
        "findings": [
            {"topic": topic, "disposition": disposition}
            for topic, disposition in findings
        ],
        "summary": {
            "finding_count": len(findings),
            "single_temperature_nt_identifiable": False,
            "single_temperature_activation_identifiable": False,
            "multi_temperature_activation_all_three_identifiable": False,
            "current_lco_gate_parameters_jointly_identifiable": False,
            "vibrational_parameter_identifiable": False,
            "electronic_vibrational_separable_in_current_code": False,
            "requested_joint_identification_without_required_data_pass": False,
            "guide_staged_strategy_directionally_sound": True,
            "experimental_material_fit_authority_pass": False,
            "next_step": "38.1",
        },
        "status": (
            "FAIL_P059_V1016_JOINT_IDENTIFIABILITY_WITHOUT_MULTI_TEMPERATURE_"
            "RATE_SERIES_AND_INDEPENDENT_ELECTRONIC_VIBRATIONAL_PRIORS"
        ),
        "next_action": (
            "Phase 059 Step 38.1: verify v1.0.17 doc-only and citation "
            "corrections by exact diff and primary-source checks."
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
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    report = rf"""# Phase 059 v1.0.16 결합 식별성 판정

정본일: 2026-07-28

판정: `{result["status"]}`

## 결론

요구 데이터 없이 네 계열을 동시에 여는 것은 구조적으로 불가능하다.
이는 optimizer 성능 문제가 아니라 서로 다른 파라미터가 같은
관측 조합으로만 들어가는 rank deficiency다.

## 수치 rank

- 단일 온도 \(n_0,n_1\): 200개 voltage point를 늘려도 rank
  {single_t_nt["rank"]}/2다. 관측되는 것은 \(n(T_k)\) 하나다.
- 단일 온도, 4 rate의 activation:
  \((\Delta H_a,\Delta S_a,\log|dV/dq|)\) rank
  {activation_one_t_many_rates["rank"]}/3이다. rate는 알려진
  \(\log I\)만 바꾸고 파라미터 민감도 행을 바꾸지 않는다.
- 세 온도와 4 rate를 써도 activation rank는
  {activation_many_t_many_rates["rank"]}/3이다.
  \(\Delta S_a\)와 prefactor/\(dV/dq\) 사이에 정확한 null vector가
  남으므로 하나를 독립 측정·동결해야 한다.
- 현 LCO electronic gate의
  \((\Delta S_\mathrm{{base}},g_\max,x_\mathrm{{MIT}},\Delta x)\)는
  300개 synthetic voltage weight를 줘도 rank
  {lco_gate_rank["rank"]}/4다. 코드가 전자항을
  \(x_\mathrm{{center}},298.15\) K의 한 상수로 평가하기 때문이다.
- vibrational 잔여항은 forward parameter가 없어 rank 0이다.

## 데이터가 해야 하는 일

상수-n → per-T width → 필요 시 n(T)로 가는 guide의 단계적 방향은
보존한다. 다만 완료된 식별이 아니라 필요한 데이터의 순서를 말한
것이다. 최소 계약은 다음과 같다.

1. 폭은 \(T_\mathrm{{ref}}\) 양쪽의 다온도 peak와 uncertainty,
   domain-wide positivity bound가 필요하다.
2. activation은 각 온도의 rate-series, 독립 OCV \(dV/dq\),
   current-interruption/transport 진단이 필요하다.
3. LCO electronic은 올바른 Li-reference entropy, composition-resolved
   \(x(V,T)\), 충분한 온도 곡률, DOS/phase-coexistence prior가 필요하다.
4. vibrational은 명시 forward term과 phonon/heat-capacity prior가
   있어야 한다. 그렇지 않으면 electronic \(T^2\) 신호에 vib 잔여가
   섞이는 것을 분리할 수 없다.

synthetic round-trip은 주어진 파라미터에서 코드가 자기 출력을
재생한다는 증거일 뿐 noise, parameter covariance, model discrepancy
아래의 statistical identifiability 증거가 아니다.

따라서 v1.0.16에는 실제 graphite/LCO/Si 데이터 피팅 권위가 없고,
특히 doped high-voltage LCO와 Si 경로는 부재한다.

## 다음 단계

Step 38.1에서 v1.0.17의 doc-only·citation 정정을 exact diff와
1차 출처로 판정한다.

원본 `Claude/`, `main`은 수정하지 않았다.
"""
    REPORT.write_text(report, encoding="utf-8")
    print(result["status"])
    print("ranks", single_t_nt["rank"], activation_one_t_many_rates["rank"],
          activation_many_t_many_rates["rank"], lco_gate_rank["rank"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
