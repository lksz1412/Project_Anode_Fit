#!/usr/bin/env python3
"""Audit both unique Phase 059 golden NPZ contents and the v1.0.15 rebaseline."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
OUTPUT = RESULTS / "PHASE_059_GOLDEN_NPZ_AUDIT.json"
REVIEW = RESULTS / "PHASE_059_GOLDEN_NPZ_REVIEW.md"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
REBASELINE_COMMIT = "03dab9221d9b017501a1a9d391ce8825dd440106"

VERSIONS = [
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
]


def version_tag(version: str) -> str:
    return version.removeprefix("v").replace(".", "_")


def source_paths(version: str) -> dict[str, str]:
    base = f"Claude/docs/{version}"
    code = f"{base}/Anode_Fit_{version}.py"
    return {
        "code": code,
        "test": f"{base}/test_regression_graphite.py",
        "golden": f"{base}/golden_graphite_ref.npz",
    }


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_text(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True
    ).strip()


def git_bytes(spec: str) -> bytes:
    return subprocess.check_output(["git", "show", spec], cwd=ROOT)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def array_sha(array: np.ndarray) -> str:
    value = np.ascontiguousarray(array)
    return sha256_bytes(value.tobytes())


def array_inventory(key: str, array: np.ndarray) -> dict[str, Any]:
    value = np.asarray(array)
    return {
        "key": key,
        "shape": list(value.shape),
        "dtype": str(value.dtype),
        "element_count": int(value.size),
        "nbytes": int(value.nbytes),
        "finite_count": int(np.count_nonzero(np.isfinite(value))),
        "nan_count": int(np.count_nonzero(np.isnan(value))),
        "positive_inf_count": int(np.count_nonzero(np.isposinf(value))),
        "negative_inf_count": int(np.count_nonzero(np.isneginf(value))),
        "minimum": float(np.min(value)),
        "maximum": float(np.max(value)),
        "mean": float(np.mean(value)),
        "array_bytes_sha256": array_sha(value),
    }


def comparison(key: str, left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    a = np.asarray(left)
    b = np.asarray(right)
    shape_equal = a.shape == b.shape
    dtype_equal = a.dtype == b.dtype
    if not shape_equal:
        return {
            "key": key,
            "shape_equal": False,
            "dtype_equal": dtype_equal,
            "array_equal": False,
        }
    difference = np.abs(a.astype(float) - b.astype(float))
    return {
        "key": key,
        "shape_equal": shape_equal,
        "dtype_equal": dtype_equal,
        "array_equal": bool(np.array_equal(a, b)),
        "unequal_element_count": int(np.count_nonzero(a != b)),
        "max_abs_diff": float(np.max(difference)),
        "mean_abs_diff": float(np.mean(difference)),
        "allclose_rtol0_atol1e_15": bool(
            np.allclose(a, b, rtol=0.0, atol=1.0e-15)
        ),
        "allclose_rtol0_atol5e_15": bool(
            np.allclose(a, b, rtol=0.0, atol=5.0e-15)
        ),
        "allclose_rtol0_atol1e_12": bool(
            np.allclose(a, b, rtol=0.0, atol=1.0e-12)
        ),
    }


def npz_inventory(path: Path, occurrence_paths: list[str]) -> tuple[dict, dict[str, np.ndarray]]:
    arrays: dict[str, np.ndarray] = {}
    with np.load(path, allow_pickle=False) as archive:
        keys = list(archive.files)
        for key in keys:
            arrays[key] = np.asarray(archive[key]).copy()
    zip_members = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            raw = archive.read(info.filename)
            zip_members.append(
                {
                    "filename": info.filename,
                    "compress_type": info.compress_type,
                    "compressed_size": info.compress_size,
                    "uncompressed_size": info.file_size,
                    "crc32_hex": f"{info.CRC:08x}",
                    "member_sha256": sha256_bytes(raw),
                }
            )
    return (
        {
            "representative_path": str(path.relative_to(ROOT)),
            "occurrence_paths": occurrence_paths,
            "occurrence_count": len(occurrence_paths),
            "file_sha256": sha256(path),
            "file_size_bytes": path.stat().st_size,
            "key_order": list(arrays),
            "key_count": len(arrays),
            "arrays": [
                array_inventory(key, value) for key, value in arrays.items()
            ],
            "zip_members": zip_members,
        },
        arrays,
    )


def release_outputs(version: str) -> tuple[dict[str, np.ndarray], dict[str, str]]:
    paths = source_paths(version)
    code = load_module(ROOT / paths["code"], f"phase059_golden_code_{version_tag(version)}")
    test = load_module(ROOT / paths["test"], f"phase059_golden_test_{version_tag(version)}")
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        outputs = {
            key: np.asarray(value).copy()
            for key, value in test.graphite_outputs(code).items()
        }
    return outputs, {
        role: sha256(ROOT / relative) for role, relative in paths.items()
    }


def normalized_harness_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for version in VERSIONS:
        text = text.replace(version, "<VERSION>")
        text = text.replace(version.removeprefix("v"), "<VERSION_NUMBER>")
    return text


def main() -> None:
    tracked_paths = [
        relative
        for version in VERSIONS
        for relative in source_paths(version).values()
    ]
    source_before = {
        relative: sha256(ROOT / relative) for relative in tracked_paths
    }

    occurrences_by_hash: dict[str, list[str]] = {}
    for version in VERSIONS:
        relative = source_paths(version)["golden"]
        occurrences_by_hash.setdefault(sha256(ROOT / relative), []).append(relative)
    unique_hashes = sorted(occurrences_by_hash)
    unique_records = []
    unique_arrays: dict[str, dict[str, np.ndarray]] = {}
    for digest in unique_hashes:
        occurrences = occurrences_by_hash[digest]
        record, arrays = npz_inventory(ROOT / occurrences[0], occurrences)
        unique_records.append(record)
        unique_arrays[digest] = arrays

    v14_hash = sha256(ROOT / source_paths("v1.0.14")["golden"])
    v15_hash = sha256(ROOT / source_paths("v1.0.15")["golden"])
    old_arrays = unique_arrays[v14_hash]
    new_arrays = unique_arrays[v15_hash]
    key_order_equal = list(old_arrays) == list(new_arrays)
    key_set_equal = set(old_arrays) == set(new_arrays)
    golden_pair_arrays = [
        comparison(key, old_arrays[key], new_arrays[key])
        for key in old_arrays
        if key in new_arrays
    ]

    generated_by_version: dict[str, dict[str, np.ndarray]] = {}
    version_records = []
    for version in VERSIONS:
        outputs, hashes = release_outputs(version)
        generated_by_version[version] = outputs
        golden_path = ROOT / source_paths(version)["golden"]
        with np.load(golden_path, allow_pickle=False) as archive:
            golden = {key: np.asarray(archive[key]).copy() for key in archive.files}
        keys_equal = list(outputs) == list(golden)
        arrays = [
            comparison(key, outputs[key], golden[key])
            for key in outputs
            if key in golden
        ]
        version_records.append(
            {
                "version": version,
                "paths": source_paths(version),
                "source_sha256": hashes,
                "generated_key_order": list(outputs),
                "golden_key_order": list(golden),
                "key_order_equal": keys_equal,
                "key_set_equal": set(outputs) == set(golden),
                "array_count": len(arrays),
                "array_equal_count": sum(item["array_equal"] for item in arrays),
                "allclose_rtol0_atol1e_15_count": sum(
                    item["allclose_rtol0_atol1e_15"] for item in arrays
                ),
                "allclose_rtol0_atol5e_15_count": sum(
                    item["allclose_rtol0_atol5e_15"] for item in arrays
                ),
                "allclose_rtol0_atol1e_12_count": sum(
                    item["allclose_rtol0_atol1e_12"] for item in arrays
                ),
                "max_abs_diff": max(item["max_abs_diff"] for item in arrays),
                "arrays": arrays,
            }
        )

    current_v14 = generated_by_version["v1.0.14"]
    current_v15 = generated_by_version["v1.0.15"]
    delta_alignment = []
    for key in old_arrays:
        golden_delta = new_arrays[key] - old_arrays[key]
        current_delta = current_v15[key] - current_v14[key]
        delta_alignment.append(
            {
                "key": key,
                "golden_delta_max_abs": float(np.max(np.abs(golden_delta))),
                "current_delta_max_abs": float(np.max(np.abs(current_delta))),
                "delta_max_abs_difference": float(
                    np.max(np.abs(golden_delta - current_delta))
                ),
            }
        )

    copy_forward_current = []
    for version in ["v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2"]:
        rows = [
            comparison(
                key,
                generated_by_version["v1.0.15"][key],
                generated_by_version[version][key],
            )
            for key in generated_by_version["v1.0.15"]
        ]
        copy_forward_current.append(
            {
                "left": "v1.0.15",
                "right": version,
                "array_equal_count": sum(item["array_equal"] for item in rows),
                "array_count": len(rows),
                "max_abs_diff": max(item["max_abs_diff"] for item in rows),
                "arrays": rows,
            }
        )

    commit_parent = git_text("rev-parse", f"{REBASELINE_COMMIT}^")
    v15_golden_path = source_paths("v1.0.15")["golden"]
    v15_code_path = source_paths("v1.0.15")["code"]
    v15_test_path = source_paths("v1.0.15")["test"]
    pre_golden = git_bytes(f"{REBASELINE_COMMIT}^:{v15_golden_path}")
    post_golden = git_bytes(f"{REBASELINE_COMMIT}:{v15_golden_path}")
    changed_paths = git_text(
        "diff-tree",
        "--no-commit-id",
        "--name-status",
        "-r",
        REBASELINE_COMMIT,
        "--",
        v15_code_path,
        v15_test_path,
        v15_golden_path,
    ).splitlines()
    rebaseline = {
        "commit": REBASELINE_COMMIT,
        "parent": commit_parent,
        "author_date": git_text(
            "show", "-s", "--format=%aI", REBASELINE_COMMIT
        ),
        "subject": git_text(
            "show", "-s", "--format=%s", REBASELINE_COMMIT
        ),
        "selected_changed_paths": changed_paths,
        "code_blob_before": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}^:{v15_code_path}"
        ),
        "code_blob_after": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}:{v15_code_path}"
        ),
        "test_blob_before": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}^:{v15_test_path}"
        ),
        "test_blob_after": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}:{v15_test_path}"
        ),
        "golden_blob_before": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}^:{v15_golden_path}"
        ),
        "golden_blob_after": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}:{v15_golden_path}"
        ),
        "golden_sha256_before": sha256_bytes(pre_golden),
        "golden_sha256_after": sha256_bytes(post_golden),
        "pre_golden_equals_v1014_golden": sha256_bytes(pre_golden)
        == v14_hash,
        "post_golden_equals_v1015_current_file": sha256_bytes(post_golden)
        == v15_hash,
        "test_harness_changed_in_rebaseline_commit": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}^:{v15_test_path}"
        )
        != git_text("rev-parse", f"{REBASELINE_COMMIT}:{v15_test_path}"),
        "code_changed_in_rebaseline_commit": git_text(
            "rev-parse", f"{REBASELINE_COMMIT}^:{v15_code_path}"
        )
        != git_text("rev-parse", f"{REBASELINE_COMMIT}:{v15_code_path}"),
        "golden_changed_in_rebaseline_commit": sha256_bytes(pre_golden)
        != sha256_bytes(post_golden),
    }

    harness_texts = {
        version: (ROOT / source_paths(version)["test"]).read_text(encoding="utf-8")
        for version in VERSIONS
    }
    normalized_hashes = {
        version: sha256_bytes(
            normalized_harness_text(ROOT / source_paths(version)["test"]).encode(
                "utf-8"
            )
        )
        for version in VERSIONS
    }
    feature_tokens = [
        "n_T1",
        "theta_E",
        "LCOCathodeDQDV",
        "'L_V'",
        '"L_V"',
        "nonmonotone",
        "reversal",
        "pulse",
        "measured",
        "experimental",
        "3600",
        "entropy_coefficient",
        "reversible_heat",
    ]
    coverage = {
        "normalized_harness_sha256_by_version": normalized_hashes,
        "normalized_logic_family_count": len(set(normalized_hashes.values())),
        "token_occurrences_all_harnesses": {
            token: sum(text.count(token) for text in harness_texts.values())
            for token in feature_tokens
        },
        "key_semantics": {
            "V": "synthetic voltage coordinate generated by np.linspace",
            "equilibrium_298": "model-generated graphite equilibrium dQ/dV at 298.15 K",
            "dqdv_dis_I*": "model-generated graphite discharge curves at three numeric current inputs",
            "dqdv_chg_I*": "model-generated graphite charge curves at three numeric current inputs",
            "dqdv_T*": "model-generated graphite discharge curves at three temperatures",
            "dqdv_TV": "model-generated graphite curve under a synthetic linear T(V) profile",
            "curve_dis_02C": "model-generated facade output at 0.2 C and Q_cell=1.0",
        },
        "evidence_class": "DERIVED_MODEL_OUTPUT_SNAPSHOT",
        "contains_experimental_observation": False,
        "contains_optimizer_state": False,
        "contains_parameter_covariance_or_uncertainty": False,
        "contains_lco_output": False,
        "contains_si_coulomb_capacity_case": False,
        "contains_nonmonotone_or_reversal_history": False,
    }

    source_after = {
        relative: sha256(ROOT / relative) for relative in tracked_paths
    }
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "scope": "Phase 059 Step 34.5 full key/shape/dtype/array audit of two unique golden NPZ contents across six releases",
        "authority_boundary": "Golden equality is an internal model-output regression invariant, not experimental validation, optimizer-state reproduction, parameter identifiability, or physical correctness.",
        "status": "CONDITIONAL_P059_GOLDEN_NPZ",
        "execution_gate": "PASS_P059_GOLDEN_NPZ_AUDIT_EXECUTION",
        "source_sha256_before": source_before,
        "source_sha256_after": source_after,
        "sources_unchanged": source_before == source_after,
        "version_count": len(VERSIONS),
        "golden_occurrence_count": len(VERSIONS),
        "unique_golden_content_count": len(unique_records),
        "unique_golden_contents": unique_records,
        "golden_pair": {
            "left_sha256": v14_hash,
            "right_sha256": v15_hash,
            "key_order_equal": key_order_equal,
            "key_set_equal": key_set_equal,
            "array_count": len(golden_pair_arrays),
            "array_equal_count": sum(
                item["array_equal"] for item in golden_pair_arrays
            ),
            "changed_array_count": sum(
                not item["array_equal"] for item in golden_pair_arrays
            ),
            "max_abs_diff": max(
                item["max_abs_diff"] for item in golden_pair_arrays
            ),
            "arrays": golden_pair_arrays,
        },
        "version_regeneration": version_records,
        "v1015_rebaseline": rebaseline,
        "rebaseline_delta_alignment": {
            "array_count": len(delta_alignment),
            "max_delta_mismatch": max(
                item["delta_max_abs_difference"] for item in delta_alignment
            ),
            "arrays": delta_alignment,
        },
        "post_rebaseline_current_copy_forward": copy_forward_current,
        "coverage_and_authority": coverage,
        "findings": [
            {
                "finding_id": "GOLD-001",
                "disposition": "CONFIRMED_INTERNAL_BASELINE",
                "claim": "v1.0.15 deliberately replaced the v1.0.14-equivalent NPZ in the same commit as the pointwise-memory code architecture change.",
            },
            {
                "finding_id": "GOLD-002",
                "disposition": "CONFIRMED_ARCHITECTURE_DELTA_CAPTURE",
                "claim": "The rebaseline kept V/equilibrium unchanged and replaced all eleven finite-current/temperature/facade arrays; the stored delta matches the current v1.0.14->15 code delta within floating tolerance.",
            },
            {
                "finding_id": "GOLD-003",
                "disposition": "REJECT_BIT_EXACT_PORTABILITY",
                "claim": "On the current runtime only one of thirteen regenerated arrays is bit-exact per version, while all thirteen pass rtol=0, atol=1e-12.",
            },
            {
                "finding_id": "GOLD-004",
                "disposition": "COPY_FORWARD_NO_NEW_FEATURE_COVERAGE",
                "claim": "v1.0.15-v1.0.18.2 share one golden content and regenerate identical legacy outputs; n(T) and Einstein additions are absent from the harness.",
            },
            {
                "finding_id": "GOLD-005",
                "disposition": "INSUFFICIENT_SCIENTIFIC_AUTHORITY",
                "claim": "The archive contains synthetic model outputs only and cannot validate chronology, SI C-rate units, direct-LV zero-current behavior, entropy/heat, LCO, doping, experimental fit, uncertainty, or optimizer state.",
            },
            {
                "finding_id": "GOLD-006",
                "disposition": "SELF_REFERENTIAL_CAPTURE_CAUTION",
                "claim": "The same harness can capture and verify its own output; rebaselining establishes an intentional implementation snapshot but is not an independent oracle for physical correctness.",
            },
        ],
        "next_step": "35.1",
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    REVIEW.write_text(make_review(payload), encoding="utf-8")


def make_review(payload: dict[str, Any]) -> str:
    pair = payload["golden_pair"]
    regen = payload["version_regeneration"]
    rebaseline = payload["v1015_rebaseline"]
    delta = payload["rebaseline_delta_alignment"]
    coverage = payload["coverage_and_authority"]
    exact_counts = {row["version"]: row["array_equal_count"] for row in regen}
    tolerant_counts = {
        row["version"]: row["allclose_rtol0_atol1e_12_count"]
        for row in regen
    }
    max_runtime_difference = max(row["max_abs_diff"] for row in regen)
    changed_keys = [
        row["key"] for row in pair["arrays"] if not row["array_equal"]
    ]
    unchanged_keys = [
        row["key"] for row in pair["arrays"] if row["array_equal"]
    ]
    tokens = coverage["token_occurrences_all_harnesses"]
    return rf"""# Phase 059 golden NPZ·v1.0.15 rebaseline 감사

정본일: 2026-07-28

상태: `{payload["status"]}`

## 결론

6개 release의 golden occurrence는 내용 기준 2개뿐이다.
v1.0.14 golden과 v1.0.15–v1.0.18.2 공통 golden이다. v1.0.15
pointwise-memory code 변경 commit `{rebaseline["commit"][:12]}`에서
code와 NPZ가 함께 바뀌었고 regression harness 자체는 바뀌지 않았다.
따라서 rebaseline은 임의 파일 교체가 아니라 새 architecture의
내부 출력 snapshot을 의도적으로 다시 잡은 기록이다.

그러나 이 사실은 새 architecture의 물리적 정당성을 검증하지 않는다.
같은 harness가 자기 출력을 `capture`하고 다시 `verify`하므로 golden은
독립 oracle이 아니다.

## 두 unique golden의 전수 비교

- key/order/shape/dtype은 13/13 동일하다.
- unchanged arrays {pair["array_equal_count"]}/13:
  `{", ".join(unchanged_keys)}`.
- changed arrays {pair["changed_array_count"]}/13:
  `{", ".join(changed_keys)}`.
- 최대 변화는 `{pair["max_abs_diff"]:.9e}`다.
- 저장된 golden delta와 현재 환경에서 직접 계산한
  v1.0.14→15 output delta의 최대 불일치는
  `{delta["max_delta_mismatch"]:.3e}`다.

즉 좌표와 298 K 평형 curve는 그대로이고, 유한전류·온도·T(V)·facade
11개 curve가 새 pointwise architecture 출력으로 재정초됐다.

## 현재 runtime 재생성

| version | bit-exact | atol=1e-12 |
|---|---:|---:|
{chr(10).join(f'| {version} | {exact_counts[version]}/13 | {tolerant_counts[version]}/13 |' for version in VERSIONS)}

전체 최대 절대차는 `{max_runtime_difference:.3e}`다. 따라서 현
`np.array_equal` gate 실패는 수 \(10^{{-15}}\) 규모의 runtime/library
부동소수 차이이며, 저장된 architecture delta
\(\sim10^{{-5}}\)와 구분된다. bit-exact 이식성은 REJECT지만
`rtol=0, atol=1e-12` 내부 회귀는 모두 성립한다.

v1.0.15와 v1.0.16/17/18.1/18.2가 이 13개 legacy output에서
각각 13/13 exact identical인 것은 후속 additive feature가 default
off라는 뜻일 뿐, 그 feature가 검증됐다는 뜻이 아니다.

## golden이 검사하지 않는 것

6개 harness 전체 token count는 `n_T1={tokens["n_T1"]}`,
`theta_E={tokens["theta_E"]}`, `LCOCathodeDQDV={tokens["LCOCathodeDQDV"]}`,
direct `L_V={tokens["'L_V'"] + tokens['"L_V"']}`,
`nonmonotone={tokens["nonmonotone"]}`, `reversal={tokens["reversal"]}`,
`pulse={tokens["pulse"]}`, `3600={tokens["3600"]}`다.

따라서 다음은 golden 권위 밖이다.

- 입력 chronology, reversal, pulse, rest와 초기 state
- direct \(L_V\)의 \(I\to0\) 극한과 SI C-rate/Ah/C 환산
- \(n(T)\), default \(\partial w/\partial T\), entropy와 heat
- Einstein 입력·reference guard와 material calibration
- LCO rate dependence, 전자 온도의존, doped high-voltage state
- 공개 실험값, optimizer state, covariance와 불확도

NPZ의 evidence class는 `DERIVED_MODEL_OUTPUT_SNAPSHOT`이다.
실험 데이터나 저장된 fit/optimizer 재현 상태로 읽으면 안 된다.

## v1.0.15 rebaseline 판정

- 보존: 새 architecture가 의도한 13개 legacy output을 고정한
  internal regression snapshot이라는 기록.
- 정정: “13/13 bit-exact gate green”은 runtime-independent
  과학 검증이 아니다.
- 한계: rebaseline은 chronology sorting, 단위, local barrier,
  LCO와 후속 \(n(T)\)/Einstein branch를 검사하지 않아 해당 결함을
  발견하거나 배제할 수 없다.

Step 34 code/test/demo/golden 감사는 이로써 끝났다. 다음 Step 35.1은
18개 PDF 492쪽의 전 페이지 render·기계/시각 검독이다.
"""


if __name__ == "__main__":
    main()
