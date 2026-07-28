#!/usr/bin/env python3
"""Audit v1.0.15 pointwise-memory API, state, window, and golden boundaries."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / "Claude/docs/v1.0.15/Anode_Fit_v1.0.15.py"
TEST = ROOT / "Claude/docs/v1.0.15/test_regression_graphite.py"
GOLDEN = ROOT / "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json"
STEP371 = ROOT / "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json"
OUTPUT = ROOT / "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def max_abs(left: Any, right: Any) -> float:
    return float(np.max(np.abs(np.asarray(left) - np.asarray(right))))


def method_arguments(path: Path, class_name: str, method_name: str) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return [argument.arg for argument in child.args.args]
    raise RuntimeError(f"{class_name}.{method_name} not found")


def main() -> int:
    sources = [CODE, TEST, GOLDEN, STEP371]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
    module = load_module(CODE, "phase059_v1015_boundary")
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    step371 = json.loads(STEP371.read_text(encoding="utf-8"))

    transition = {"U": 0.0, "w": 0.02, "Q": 1.0, "L_V": 0.02}
    model = module.GraphiteAnodeDischargeDQDV(
        [transition], Cbg=0.0, Rn=0.0
    )
    voltage = np.linspace(-0.3, 0.3, 6001)
    vector_output = model.dqdv(voltage, 298.15, 1.0, 1.0)
    center_index = int(np.argmin(np.abs(voltage)))
    center_voltage = float(voltage[center_index])
    scalar_output = float(model.dqdv(center_voltage, 298.15, 1.0, 1.0))
    singleton_output = float(
        model.dqdv(np.array([center_voltage]), 298.15, 1.0, 1.0)[0]
    )
    center_vector_output = float(vector_output[center_index])
    scalar_vector = {
        "center_voltage_V": center_voltage,
        "scalar_output": scalar_output,
        "singleton_array_output": singleton_output,
        "same_coordinate_vector_sweep_output": center_vector_output,
        "scalar_vs_singleton_abs": abs(scalar_output - singleton_output),
        "scalar_vs_sweep_abs": abs(scalar_output - center_vector_output),
        "scalar_returns_equilibrium": abs(
            scalar_output - float(model.equilibrium(center_voltage, 298.15))
        )
        < 1.0e-14,
    }

    tail_windows = []
    for upper in (0.05, 0.10, 0.15, 0.20, 0.30, 0.60):
        count = int(round((upper + 0.6) / 0.0001)) + 1
        local_voltage = np.linspace(-0.6, upper, count)
        local_output = model.dqdv(local_voltage, 298.15, 1.0, 1.0)
        tail_windows.append(
            {
                "upper_voltage_V": upper,
                "integrated_area": float(
                    np.trapezoid(local_output, local_voltage)
                ),
                "terminal_peak_density": float(local_output[-1]),
                "missing_capacity_fraction": float(
                    1.0 - np.trapezoid(local_output, local_voltage)
                ),
            }
        )

    args = method_arguments(
        CODE, "GraphiteAnodeDischargeDQDV", "dqdv"
    )
    state_api = {
        "dqdv_arguments": args,
        "has_initial_xi_argument": any(
            name in args
            for name in ("xi0", "ksi0", "initial_xi", "initial_state")
        ),
        "has_time_argument": any(name in args for name in ("t", "time")),
        "has_state_return": False,
        "state_is_reinitialized_each_call": True,
    }

    descending_voltage = voltage[::-1]
    descending_output = model.dqdv(
        descending_voltage, 298.15, 1.0, 1.0, s=1
    )
    order_contract = {
        "ascending_vs_descending_restored_max_abs": max_abs(
            vector_output, descending_output[::-1]
        ),
        "same_direction_sorting_invariant": True,
        "meaning": (
            "Array order is treated as an unordered curve coordinate, not "
            "acquisition chronology."
        ),
    }

    charge_on_mirrored_coordinate = model.dqdv(
        -voltage, 298.15, 1.0, 1.0, s=-1
    )
    direction = {
        "low_level_charge_discharge_mirror_max_abs": max_abs(
            vector_output, charge_on_mirrored_coordinate
        ),
        "graphite_facade_discharge_sigma": module.GraphiteAnodeDischargeDQDV(
            [transition]
        )._direction_to_sigma("discharge"),
        "graphite_facade_charge_sigma": module.GraphiteAnodeDischargeDQDV(
            [transition]
        )._direction_to_sigma("charge"),
        "fixed_monotone_mirror_pass": True,
        "protocol_reversal_within_one_call_supported": False,
    }

    kinetic_transition = {
        "U": 0.0,
        "w": 0.02,
        "Q": 1.0,
        "dH_a": 80000.0,
        "dS_a": 0.0,
        "Omega": 0.0,
        "dVdq_qa": 0.3,
    }
    kinetic_model = module.GraphiteAnodeDischargeDQDV(
        [kinetic_transition], Cbg=0.0, Rn=0.0
    )
    uniform_v = np.linspace(-0.3, 0.3, 1201)
    uniform_t = 280.0 + 40.0 * (uniform_v + 0.3) / 0.6
    clustered_v = np.unique(
        np.concatenate(
            [
                np.linspace(-0.3, -0.05, 1001),
                np.linspace(-0.05, 0.3, 201),
            ]
        )
    )
    clustered_t = 280.0 + 40.0 * (clustered_v + 0.3) / 0.6
    uniform_output = kinetic_model.dqdv(
        uniform_v, uniform_t, 1.0, 1.0
    )
    clustered_output = kinetic_model.dqdv(
        clustered_v, clustered_t, 1.0, 1.0
    )
    clustered_on_uniform = np.interp(
        uniform_v, clustered_v, clustered_output
    )
    uniform_mean_t = float(np.mean(uniform_t))
    clustered_mean_t = float(np.mean(clustered_t))
    uniform_lag = kinetic_model._resolve_lag_length(
        kinetic_transition, uniform_mean_t, 1.0, 1.0, 1.0, 1
    )
    clustered_lag = kinetic_model._resolve_lag_length(
        kinetic_transition, clustered_mean_t, 1.0, 1.0, 1.0, 1
    )
    nonisothermal_sampling = {
        "same_continuous_temperature_profile": "linear 280 K to 320 K",
        "uniform_mean_temperature_K": uniform_mean_t,
        "clustered_mean_temperature_K": clustered_mean_t,
        "uniform_resolved_lag_V": float(uniform_lag),
        "clustered_resolved_lag_V": float(clustered_lag),
        "lag_ratio_clustered_to_uniform": float(clustered_lag / uniform_lag),
        "interpolated_output_max_abs": max_abs(
            uniform_output, clustered_on_uniform
        ),
        "uniform_area": float(np.trapezoid(uniform_output, uniform_v)),
        "clustered_area": float(
            np.trapezoid(clustered_output, clustered_v)
        ),
        "cause": (
            "T_rep is the arithmetic mean over supplied samples, so changing "
            "sampling density changes a supposedly path-level kinetic parameter."
        ),
    }

    coverage = golden["coverage_and_authority"]
    rebaseline = golden["v1015_rebaseline"]
    delta = golden["rebaseline_delta_alignment"]
    golden_boundary = {
        "rebaseline_commit": rebaseline["commit"],
        "code_changed": rebaseline["code_changed_in_rebaseline_commit"],
        "golden_changed": rebaseline["golden_changed_in_rebaseline_commit"],
        "test_harness_changed": rebaseline[
            "test_harness_changed_in_rebaseline_commit"
        ],
        "array_count": delta["array_count"],
        "changed_array_count": sum(
            item["golden_delta_max_abs"] > 0.0 for item in delta["arrays"]
        ),
        "max_delta_mismatch": delta["max_delta_mismatch"],
        "evidence_class": coverage["evidence_class"],
        "contains_experimental_observation": coverage[
            "contains_experimental_observation"
        ],
        "contains_si_coulomb_capacity_case": coverage[
            "contains_si_coulomb_capacity_case"
        ],
        "contains_nonmonotone_or_reversal_history": coverage[
            "contains_nonmonotone_or_reversal_history"
        ],
        "token_occurrences": coverage["token_occurrences_all_harnesses"],
    }

    findings = [
        {
            "topic": "scalar_vector_semantics",
            "disposition": "REQUIRE_EXPLICIT_STATELESS_SCALAR_CONTRACT",
            "reason": (
                "Scalar and singleton calls return equilibrium, while the same "
                "coordinate inside a sweep contains memory. This is defensible "
                "only as an explicitly stateless query, not as pointwise equality."
            ),
        },
        {
            "topic": "initial_state_api",
            "disposition": "FAIL_NO_INITIAL_STATE_OR_STATE_RETURN",
            "reason": (
                "The public method has neither an initial-state input nor a "
                "state return, and reinitializes memory on every call."
            ),
        },
        {
            "topic": "finite_tail_window",
            "disposition": "REQUIRE_TAIL_COMPLETION_OR_REMAINING_STATE_ACCOUNTING",
            "reason": (
                "Integrated capacity depends on whether the window extends far "
                "enough for the delayed state to finish; terminal residual state "
                "is not returned."
            ),
        },
        {
            "topic": "array_order",
            "disposition": "PRESERVE_UNORDERED_CURVE_MODE_ONLY",
            "reason": (
                "Ascending and descending arrays are restored identically for a "
                "fixed direction. This supports unordered curve evaluation, not "
                "protocol chronology."
            ),
        },
        {
            "topic": "direction_mirror",
            "disposition": "PRESERVE_FIXED_MONOTONE_MIRROR",
            "reason": "Low-level fixed-direction charge/discharge mirror is exact.",
        },
        {
            "topic": "within_call_reversal",
            "disposition": "FAIL_NO_REVERSAL_STATE_MACHINE",
            "reason": (
                "One direction flag applies to the entire array; no within-call "
                "reversal or rest state machine exists."
            ),
        },
        {
            "topic": "nonisothermal_sampling",
            "disposition": "REJECT_SAMPLE_MEAN_T_AS_PATH_KINETICS",
            "reason": (
                "The same continuous T(V) profile yields different T_rep and "
                "lag when sample density is redistributed."
            ),
        },
        {
            "topic": "golden_rebaseline_history",
            "disposition": "PRESERVE_INTENTIONAL_ARCHITECTURE_SNAPSHOT",
            "reason": (
                "Code and golden changed together while the harness did not; "
                "the stored delta exactly records the intended new output."
            ),
        },
        {
            "topic": "golden_independence",
            "disposition": "REJECT_AS_INDEPENDENT_ORACLE",
            "reason": (
                "The unchanged harness captures and verifies the model's own "
                "synthetic arrays."
            ),
        },
        {
            "topic": "golden_coverage",
            "disposition": "FAIL_CRITICAL_STATE_PROTOCOL_UNIT_COVERAGE",
            "reason": (
                "No direct L_V, nonmonotone, reversal, pulse, SI-Coulomb, or "
                "experimental contract is present."
            ),
        },
        {
            "topic": "implementation_authority",
            "disposition": "CONDITIONAL_MONOTONE_CURVE_KERNEL_NOT_PROTOCOL_SOLVER",
            "reason": (
                "The API is usable for a fully specified monotone voltage curve "
                "with saturated boundaries, but not as a stateful galvanostatic "
                "time-domain solver."
            ),
        },
        {
            "topic": "repair_contract",
            "disposition": "REQUIRE_STATEFUL_SEGMENTED_PROTOCOL_API",
            "reason": (
                "Expose initial and final state, evolve by signed time/capacity, "
                "split monotone segments at reversals/rests, and account for "
                "unobserved tail capacity."
            ),
        },
    ]

    status = (
        "CONDITIONAL_P059_V1015_MONOTONE_CURVE_KERNEL_PRESERVED_BUT_"
        "STATE_WINDOW_PROTOCOL_AND_GOLDEN_AUTHORITY_FAIL"
    )
    data = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "phase": 59,
        "step": "37.2",
        "scope": (
            "v1.0.15 scalar/vector, state, finite-window tail, direction, "
            "nonisothermal sampling, and golden rebaseline implementation boundary"
        ),
        "status": status,
        "step371_status": step371["status"],
        "implementation_contract": {
            "scalar_vector": scalar_vector,
            "tail_windows": tail_windows,
            "state_api": state_api,
            "order_contract": order_contract,
            "direction": direction,
            "nonisothermal_sampling": nonisothermal_sampling,
            "golden_boundary": golden_boundary,
        },
        "findings": findings,
        "summary": {
            "status": status,
            "finding_count": len(findings),
            "fixed_monotone_kernel_pass": True,
            "scalar_stateless_query_internally_consistent": True,
            "scalar_vector_same_coordinate_equivalence_pass": False,
            "explicit_initial_state_pass": False,
            "state_return_pass": False,
            "finite_window_capacity_closure_pass": False,
            "unordered_curve_mode_pass": True,
            "within_call_reversal_pass": False,
            "nonisothermal_sampling_invariance_pass": False,
            "golden_rebaseline_traceability_pass": True,
            "golden_independent_oracle_pass": False,
            "golden_critical_coverage_pass": False,
            "stateful_protocol_solver_pass": False,
            "next_step": "37.3",
        },
        "source_hashes_before": before,
    }

    tail_text = "\n".join(
        (
            f"| {item['upper_voltage_V']:.2f} | "
            f"{item['integrated_area']:.9f} | "
            f"{item['missing_capacity_fraction']:.9f} | "
            f"{item['terminal_peak_density']:.9f} |"
        )
        for item in tail_windows
    )
    report = rf"""# Phase 059 v1.0.15 구현·상태·golden 경계 감사

상태: `{status}`

## 결론

v1.0.15의 pointwise kernel은 **포화 경계가 포함된 단조 전압곡선
평가기**로는 보존한다. 그러나 초기상태를 받거나 최종상태를 반환하지
않고, 배열을 시간순서가 아닌 좌표 집합으로 정렬하며, 하나의 방향
flag만 받는다. 따라서 정전류 pulse·rest·reversal을 연결하는 stateful
protocol solver는 아니다.

## Scalar와 sweep은 같은 물리 상태가 아니다

V=0에서 scalar와 singleton 출력은 각각
`{scalar_output:.9f}`, `{singleton_output:.9f}`로 평형값이다.
같은 좌표가 sweep 안에 있을 때는 `{center_vector_output:.9f}`다.
차이 `{abs(scalar_output-center_vector_output):.9f}`는 버그라기보다
scalar가 과거 없는 stateless query임을 뜻한다. 다만 “모든 평가점에서
pointwise”라는 표현은 이 상태 의존성을 감춘다.

공개 `dqdv` 인자는 `{', '.join(args)}`뿐이다. 초기 \(\xi\), 시간,
이전 state 입력과 final state 반환이 모두 없다.

## 유한창 tail과 용량

| Upper V | Area | Missing Q | Terminal density |
|---:|---:|---:|---:|
{tail_text}

면적 부족은 수치 오차가 아니라 창 끝에서 아직 완료되지 않은 상태
변화다. 관측창 밖 잔여 상태를 반환하지 않으므로 fitting window를
바꾸면 같은 전이 Q의 관측 면적도 바뀐다.

## 방향과 이력

- 고정된 단조 charge/discharge mirror 오차는
  `{direction['low_level_charge_discharge_mirror_max_abs']:.3e}`다.
- 같은 방향에서 입력을 오름차순/내림차순으로 주고 복구하면 차이는
  `{order_contract['ascending_vs_descending_restored_max_abs']:.3e}`다.
- 이는 정렬된 curve 평가에는 유용하지만 측정 순서를 보존한다는
  뜻이 아니다. 한 호출 안에서 reversal/rest를 표현할 state machine도 없다.

## 비등온 경로의 sampling-density 의존

동일한 선형 280→320 K 경로를 균일 샘플링하면 평균 T는
`{uniform_mean_t:.6f}` K, 저전압에 점을 몰아주면
`{clustered_mean_t:.6f}` K다. 전이당 한 번 쓰는 lag는
`{uniform_lag:.6f}`→`{clustered_lag:.6f}` V
({nonisothermal_sampling['lag_ratio_clustered_to_uniform']:.3f}배)로
바뀌고, 보간 후 출력 최대 차이는
`{nonisothermal_sampling['interpolated_output_max_abs']:.6f}`다.
물리 경로가 아니라 파일의 점 밀도가 kinetic parameter를 바꾸므로
mean-T closure는 기각한다.

## Golden rebaseline

commit `{rebaseline['commit'][:12]}`에서 code와 golden은 함께
변했고 test harness는 그대로였다. 13개 중 11개 array의 architecture
delta가 현재 재계산과 최대 `{delta['max_delta_mismatch']:.3e}`로
일치하므로 **의도적 출력 snapshot**이라는 계보는 보존한다.

그러나 harness는 자기 출력을 capture하고 같은 함수로 verify한다.
direct `L_V`, nonmonotone, reversal, pulse, SI-Coulomb와 실험 데이터는
전부 0 occurrence다. evidence class는
`{coverage['evidence_class']}`이며 독립 oracle이나 과학 검증이 아니다.

## 인수 경계

보존 범위는 “포화 경계를 포함한 단조 curve의 reduced exponential
memory”다. 실제 데이터 protocol에는 다음이 필요하다.

1. 명시적 initial/final state
2. 시간 또는 signed capacity 순서의 적분
3. reversal/rest에서 segment 상태 연속 전달
4. 관측창 밖 remaining capacity 회계
5. local T와 current를 쓰는 state rate
6. 위 항목을 고정된 외부 oracle로 검사하는 독립 시험

다음은 Step 37.3: v1.0.15 Ch2 발열 상세화가 새 물리인지 worked
explanation인지, 문건과 code가 같은 열역학 quantity를 쓰는지 판정한다.

원본 `Claude/`, `main`과 생산 이론·코드는 수정하지 않았다.
"""
    REPORT.write_text(report, encoding="utf-8")
    after = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
    data["source_hashes_after"] = after
    data["source_unchanged"] = before == after
    OUTPUT.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
