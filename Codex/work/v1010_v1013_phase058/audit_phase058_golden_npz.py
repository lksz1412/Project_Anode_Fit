#!/usr/bin/env python3
"""Audit every array in the v1.0.13 frozen graphite golden NPZ."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py"
GOLD = ROOT / "Claude/docs/v1.0.13/golden_graphite_ref.npz"
OUT = ROOT / "Codex/results/PHASE_058_GOLDEN_NPZ_AUDIT.json"
EXPECTED_KEYS = [
    "V",
    "equilibrium_298",
    "dqdv_dis_I0.02",
    "dqdv_dis_I0.2",
    "dqdv_dis_I1.0",
    "dqdv_chg_I0.02",
    "dqdv_chg_I0.2",
    "dqdv_chg_I1.0",
    "dqdv_T258",
    "dqdv_T298",
    "dqdv_T318",
    "dqdv_TV",
    "curve_dis_02C",
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_module():
    spec = importlib.util.spec_from_file_location("phase058_v1013_golden", CODE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def regenerate(module) -> dict[str, np.ndarray]:
    voltage = np.linspace(0.03, 0.34, 1000)
    model = module.GraphiteAnodeDischargeDQDV(
        module.GRAPHITE_STAGING_LIT,
        x=0.5,
        Rn=0.01,
        Cbg=0.05,
        use_dH_eff=True,
    )
    arrays: dict[str, np.ndarray] = {"V": voltage}
    arrays["equilibrium_298"] = np.asarray(
        model.equilibrium(voltage, T=298.15), dtype=float
    )
    for direction, name in [(+1, "dis"), (-1, "chg")]:
        for current in (0.02, 0.2, 1.0):
            arrays[f"dqdv_{name}_I{current}"] = np.asarray(
                model.dqdv(
                    voltage,
                    T=298.15,
                    I_abs=current,
                    Q_cell=1.0,
                    s=direction,
                ),
                dtype=float,
            )
    for temperature in (258.15, 298.15, 318.15):
        arrays[f"dqdv_T{int(temperature)}"] = np.asarray(
            model.dqdv(
                voltage,
                T=temperature,
                I_abs=0.2,
                Q_cell=1.0,
                s=+1,
            ),
            dtype=float,
        )
    temperature_profile = np.linspace(288.15, 308.15, voltage.size)
    arrays["dqdv_TV"] = np.asarray(
        model.dqdv(
            voltage,
            T=temperature_profile,
            I_abs=0.2,
            Q_cell=1.0,
            s=+1,
        ),
        dtype=float,
    )
    arrays["curve_dis_02C"] = np.asarray(
        model.curve(
            voltage,
            direction="discharge",
            c_rate=0.2,
            Q_cell=1.0,
            T=298.15,
        ),
        dtype=float,
    )
    return arrays


def role(key: str) -> str:
    if key == "V":
        return "INPUT_GRID"
    if key == "equilibrium_298":
        return "MODEL_OUTPUT_EQUILIBRIUM"
    if key.startswith("dqdv_dis"):
        return "MODEL_OUTPUT_DIRECTION_CURRENT"
    if key.startswith("dqdv_chg"):
        return "MODEL_OUTPUT_DIRECTION_CURRENT"
    if key.startswith("dqdv_T"):
        return "MODEL_OUTPUT_TEMPERATURE"
    if key.startswith("curve_"):
        return "MODEL_OUTPUT_FACADE"
    return "MODEL_OUTPUT_OTHER"


def array_record(key: str, golden: np.ndarray, current: np.ndarray) -> dict:
    golden_f = np.asarray(golden, dtype=float)
    current_f = np.asarray(current, dtype=float)
    delta = current_f - golden_f
    denominator = np.maximum(np.abs(golden_f), np.finfo(float).tiny)
    return {
        "key": key,
        "role": role(key),
        "shape_golden": list(golden.shape),
        "shape_current": list(current.shape),
        "dtype_golden": str(golden.dtype),
        "dtype_current": str(current.dtype),
        "element_count": int(golden.size),
        "finite_golden": bool(np.all(np.isfinite(golden_f))),
        "finite_current": bool(np.all(np.isfinite(current_f))),
        "golden_array_byte_sha256": sha256_bytes(golden.tobytes(order="C")),
        "current_array_byte_sha256": sha256_bytes(current.tobytes(order="C")),
        "bit_exact": bool(np.array_equal(golden, current)),
        "allclose_rtol1e12_atol1e12": bool(
            np.allclose(golden_f, current_f, rtol=1e-12, atol=1e-12)
        ),
        "max_abs_diff": float(np.max(np.abs(delta))),
        "rms_diff": float(np.sqrt(np.mean(delta * delta))),
        "max_relative_diff": float(np.max(np.abs(delta) / denominator)),
        "golden_min": float(np.min(golden_f)),
        "golden_max": float(np.max(golden_f)),
        "current_min": float(np.min(current_f)),
        "current_max": float(np.max(current_f)),
    }


def main() -> None:
    source_hash_before = sha256_file(CODE)
    golden_hash_before = sha256_file(GOLD)
    module = load_module()
    current = regenerate(module)
    with np.load(GOLD, allow_pickle=False) as archive:
        keys = list(archive.files)
        golden = {key: np.asarray(archive[key]) for key in keys}
    records = [
        array_record(key, golden[key], current[key])
        for key in keys
        if key in current
    ]
    with zipfile.ZipFile(GOLD) as archive:
        zip_members = [
            {
                "filename": info.filename,
                "uncompressed_bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "crc32": f"{info.CRC:08x}",
            }
            for info in archive.infolist()
        ]
    source_hash_after = sha256_file(CODE)
    golden_hash_after = sha256_file(GOLD)
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "golden_path": str(GOLD.relative_to(ROOT)),
        "golden_file_sha256": golden_hash_before,
        "golden_file_size_bytes": GOLD.stat().st_size,
        "production_code_path": str(CODE.relative_to(ROOT)),
        "production_code_sha256": source_hash_before,
        "array_count": len(keys),
        "expected_array_count": len(EXPECTED_KEYS),
        "keys": keys,
        "expected_keys": EXPECTED_KEYS,
        "missing_expected_keys": sorted(set(EXPECTED_KEYS) - set(keys)),
        "unexpected_keys": sorted(set(keys) - set(EXPECTED_KEYS)),
        "zip_members": zip_members,
        "arrays": records,
        "summary": {
            "bit_exact_count": sum(record["bit_exact"] for record in records),
            "bit_exact_fail_count": sum(not record["bit_exact"] for record in records),
            "allclose_1e12_count": sum(
                record["allclose_rtol1e12_atol1e12"] for record in records
            ),
            "max_abs_diff": max(record["max_abs_diff"] for record in records),
            "all_golden_finite": all(record["finite_golden"] for record in records),
            "all_current_finite": all(record["finite_current"] for record in records),
        },
        "scientific_evidence_class": "DERIVED_MODEL_OUTPUT_SNAPSHOT",
        "not_present": [
            "raw experimental measurements",
            "optimizer state or parameter covariance",
            "experimental metadata and uncertainty",
            "software/runtime provenance sufficient for cross-platform bitwise reproduction",
        ],
        "interpretation_rule": "Numerical closeness can support output continuity but cannot independently validate the model physics that generated both arrays.",
        "validation": {
            "all_13_keys_present": keys == EXPECTED_KEYS,
            "all_13_arrays_compared": len(records) == len(EXPECTED_KEYS),
            "source_unchanged": source_hash_before == source_hash_after,
            "golden_unchanged": golden_hash_before == golden_hash_after,
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
