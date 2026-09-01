from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
from scipy import __version__ as scipy_version
from scipy.optimize import isotonic_regression, least_squares
from scipy.signal import find_peaks, savgol_filter


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
GATE = "CONDITIONAL_P066_STEP77_FIT_REPLAY_WITH_NONCONVERGED_SELECTED_TRIAL_AND_UNSEALED_PROCESS_LOGS"
RAW_PATH = "Claude/results/comp_v24/sintef_data/sigr.csv"
SOURCES_PATH = "Claude/results/comp_v24/sintef_data/SOURCES.md"
STORED_PATH = "Claude/results/comp_v26_data/out_versions/summary_versions.json"
PARAMS_PATH = "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json"
DRIVER_PATH = "Claude/results/comp_v26_data/build_two_versions.py"
PREPROCESS_PATH = "Claude/results/comp_v26_data/test_skew_regsol_v2.py"
ENSEMBLE_PATH = "Claude/results/comp_v26_data/bdd_dqdv.py"
SEED_PATH = "Claude/results/comp_v26_data/test_gallery_vs_regsol.py"
RELEASE_PATH = "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
FIT_PATH = ROOT / "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
PROVENANCE_PATH = ROOT / "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
BUILDER_RELATIVE_PATH = "Codex/work/v1025_phase066/build_phase066_step77.py"

N = 14
VLO, VHI, DV = 0.060, 0.700, 5.0e-4
WLO, WHI = 1.0e-4, 0.12
RESTARTS = 4
NFEV = 6000
RNG_SEED = 23
PRECEDING_PARAMETER_COUNTS = [17, 17, 33, 22, 22, 43, 29, 29]
TRAPZ = np.trapezoid


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def array_sha256(value: np.ndarray) -> str:
    return sha256(np.asarray(value, dtype="<f8").tobytes(order="C"))


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def add_semantic(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = ""
    value["semantic_sha256"] = sha256(canonical_bytes(value))
    return value


def temp_contained(path: Path) -> bool:
    try:
        path.resolve().relative_to(Path(tempfile.gettempdir()).resolve())
        return True
    except ValueError:
        return False


def write_temp_json(path: Path, value: dict[str, Any]) -> None:
    require(temp_contained(path), "E_TEMP_OUTPUT", str(path))
    temporary = path.with_name(path.name + ".partial")
    temporary.write_bytes(canonical_bytes(add_semantic(value)))
    os.replace(temporary, path)


def atomic_write_pair(first_path: Path, first_value: dict[str, Any],
                      second_path: Path, second_value: dict[str, Any]) -> None:
    require((first_path.resolve(), second_path.resolve()) ==
            (PROVENANCE_PATH.resolve(), FIT_PATH.resolve()), "E_ARTIFACT_OUTPUT_ALLOWLIST")
    first_bytes = canonical_bytes(add_semantic(first_value))
    second_bytes = canonical_bytes(add_semantic(second_value))
    first_tmp = first_path.with_name(first_path.name + ".step77.tmp")
    second_tmp = second_path.with_name(second_path.name + ".step77.tmp")
    first_backup = first_path.read_bytes() if first_path.exists() else None
    second_backup = second_path.read_bytes() if second_path.exists() else None
    first_backup_tmp = first_path.with_name(first_path.name + ".step77.rollback")
    second_backup_tmp = second_path.with_name(second_path.name + ".step77.rollback")
    first_backup_ready = second_backup_ready = False
    first_installed = second_installed = False
    try:
        if first_backup is not None:
            first_backup_tmp.write_bytes(first_backup)
            require(first_backup_tmp.read_bytes() == first_backup, "E_FIRST_BACKUP_VERIFY")
            first_backup_ready = True
        if second_backup is not None:
            second_backup_tmp.write_bytes(second_backup)
            require(second_backup_tmp.read_bytes() == second_backup, "E_SECOND_BACKUP_VERIFY")
            second_backup_ready = True
        first_tmp.write_bytes(first_bytes)
        second_tmp.write_bytes(second_bytes)
        os.replace(first_tmp, first_path)
        first_installed = True
        os.replace(second_tmp, second_path)
        second_installed = True
    except Exception:
        if first_installed:
            if first_backup is None:
                if first_path.exists(): first_path.unlink()
            else:
                require(first_backup_ready, "E_FIRST_BACKUP_NOT_READY")
                os.replace(first_backup_tmp, first_path)
        if second_installed:
            if second_backup is None:
                if second_path.exists(): second_path.unlink()
            else:
                require(second_backup_ready, "E_SECOND_BACKUP_NOT_READY")
                os.replace(second_backup_tmp, second_path)
        raise
    finally:
        if first_tmp.exists(): first_tmp.unlink()
        if second_tmp.exists(): second_tmp.unlink()
        if first_backup_tmp.exists(): first_backup_tmp.unlink()
        if second_backup_tmp.exists(): second_backup_tmp.unlink()


def git_bytes(path: str) -> bytes:
    run = subprocess.run(["git", "cat-file", "blob", f"{BASELINE}:{path}"], cwd=ROOT,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=False, check=False)
    require(run.returncode == 0, "E_GIT_BLOB", f"{path}: {run.stderr.decode('utf-8', 'replace')}")
    return run.stdout


def git_blob_id(path: str) -> str:
    run = subprocess.run(["git", "rev-parse", f"{BASELINE}:{path}"], cwd=ROOT,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=False, check=False)
    require(run.returncode == 0, "E_GIT_ID", path)
    return run.stdout.decode("ascii").strip()


def parse_raw() -> tuple[np.ndarray, np.ndarray, bytes, list[str]]:
    raw = git_bytes(RAW_PATH)
    text = raw.decode("utf-8")
    reader = csv.reader(io.StringIO(text, newline=""))
    rows = list(reader)
    require(rows and rows[0] == ["V_vs_Li", "Q_mAh"], "E_RAW_HEADER")
    require(len(rows) == 16736, "E_RAW_ROWS", str(len(rows)))
    values = np.asarray([[float(a), float(b)] for a, b in rows[1:]], dtype=float)
    require(np.isfinite(values).all(), "E_RAW_NONFINITE")
    return values[:, 0], values[:, 1], raw, rows[0]


def savgol_ensemble(data: np.ndarray, ratios: tuple[float, ...]) -> np.ndarray:
    length = len(data)
    ensemble = [np.asarray(data, float)]
    for ratio in ratios:
        window = int(round(length * ratio // 2)) * 2 + 1
        if window <= 3 or window >= length:
            continue
        try:
            ensemble.append(savgol_filter(data, window, 3))
        except Exception:
            pass
        with np.errstate(divide="ignore", invalid="ignore"):
            try:
                ensemble.append(1.0 / savgol_filter(1.0 / data, window, 3))
            except Exception:
                pass
    values = np.asarray(ensemble, dtype=float)
    values[~np.isfinite(values)] = np.nan
    with np.errstate(invalid="ignore"):
        return np.nanmedian(values, axis=0)


def preprocess(V: np.ndarray, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    valid = np.isfinite(V) & np.isfinite(Q)
    V, Q = V[valid], Q[valid]
    order = np.argsort(Q, kind="mergesort")
    V, Q = V[order], Q[order]
    Qu, indices = np.unique(Q, return_index=True)
    Vu = V[indices]
    Vm = isotonic_regression(Vu, increasing=True).x
    grid = np.arange(VLO, VHI + 0.5 * DV, DV)
    locations = np.searchsorted(Vm, grid, side="right") - 1
    Qg = np.where(locations >= 0, Qu[np.clip(locations, 0, len(Qu) - 1)], 0.0)
    centers = 0.5 * (grid[:-1] + grid[1:])
    derivative = np.diff(Qg) / DV
    keep = np.isfinite(derivative) & (derivative > 0)
    usable = np.flatnonzero(keep)
    require(usable.size > 0, "E_NO_DQDV")
    runs = np.split(usable, np.flatnonzero(np.diff(usable) > 1) + 1)
    longest = max(runs, key=len)
    Vx = centers[longest[0]: longest[-1] + 1]
    Dx_raw = derivative[longest[0]: longest[-1] + 1]
    Dx = np.abs(savgol_ensemble(Dx_raw, (0.01, 0.02, 0.03)))
    require(len(Vx) == 1280 and len(Dx) == 1280, "E_PROCESSED_COUNT", str(len(Vx)))
    info = {
        "finite_input_rows": int(valid.sum()),
        "unique_Q_rows": int(len(Qu)),
        "grid_points_before_difference": int(len(grid)),
        "positive_finite_bins": int(keep.sum()),
        "longest_contiguous_bins": int(len(longest)),
        "V_min": float(Vx.min()),
        "V_max": float(Vx.max()),
        "D_min": float(Dx.min()),
        "D_max": float(Dx.max()),
        "area_data": float(TRAPZ(Dx, Vx)),
    }
    return Vx, Dx, info


def sigmoid(V: np.ndarray, U: float, w: float) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip((np.asarray(V, float) - U) / w, -350, 350)))


def component(V: np.ndarray, U: float, w: float, Q: float, alpha: float) -> np.ndarray:
    sig = sigmoid(V, U, w)
    return Q * (alpha / w) * sig ** alpha * (1.0 - sig)


def model(V: np.ndarray, params: np.ndarray) -> np.ndarray:
    result = np.full(V.size, params[-1])
    for index in range(N):
        result = result + component(V, params[index], params[N + index],
                                    params[2 * N + index], params[3 * N + index])
    return result


def seed_sets(Vx: np.ndarray, Dx: np.ndarray, peaks: list[float]) -> list[list[float]]:
    lo, hi = float(Vx.min()), float(Vx.max())
    first = list(peaks)[:N]
    while len(first) < N:
        first.append(lo + (hi - lo) * (len(first) + 0.5) / (N + 1))
    second = list(np.linspace(lo + 0.05 * (hi - lo), hi - 0.05 * (hi - lo), N))
    third = list(peaks)[:N]
    while len(third) < N:
        require(len(peaks) > 0, "E_NO_PEAK_SEED")
        third.append(float(peaks[len(third) % len(peaks)]) * (1 + 0.01 * len(third)))
    return [first, second, third[:N]]


def bounds_and_seed(Vx: np.ndarray, Dx: np.ndarray, U: list[float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    area = float(TRAPZ(Dx, Vx))
    lo, hi = float(Vx.min()), float(Vx.max())
    q0, qhi = area / N, 10.0 * area
    bg0, bghi = float(Dx.min()), float(max(Dx.max(), 1e-9))
    p0 = U + [0.004] * N + [q0] * N + [1.0] * N + [bg0]
    lb = [lo] * N + [WLO] * N + [1e-9] * N + [0.15] * N + [min(0.0, bg0)]
    ub = [hi] * N + [WHI] * N + [qhi] * N + [8.0] * N + [bghi]
    return (np.clip(np.asarray(p0, float), lb, ub), np.asarray(lb, float), np.asarray(ub, float))


def make_starts(Vx: np.ndarray, Dx: np.ndarray) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    peak_indices, _ = find_peaks(Dx, prominence=Dx.max() * 0.02)
    peaks = list(Vx[peak_indices][np.argsort(-Dx[peak_indices])])
    rng = np.random.default_rng(RNG_SEED)
    for parameter_count in PRECEDING_PARAMETER_COUNTS:
        for _strategy in range(3):
            for _restart in range(1, RESTARTS):
                rng.uniform(0.75, 1.25, parameter_count)
    records: list[dict[str, Any]] = []
    common_lb: np.ndarray | None = None
    common_ub: np.ndarray | None = None
    for strategy, U in enumerate(seed_sets(Vx, Dx, peaks)):
        p0, lb, ub = bounds_and_seed(Vx, Dx, U)
        common_lb, common_ub = lb, ub
        for restart in range(RESTARTS):
            start = p0 if restart == 0 else np.clip(p0 * rng.uniform(0.75, 1.25, p0.size), lb, ub)
            records.append({
                "strategy": strategy,
                "restart": restart,
                "sha256": array_sha256(start),
                "vector": [float(x) for x in start],
            })
    require(common_lb is not None and common_ub is not None, "E_NO_BOUNDS")
    require(sha256(b"".join(np.asarray(r["vector"], dtype="<f8").tobytes() for r in records)) ==
            "3d5c9a7b04cfbd4a6773d9d45d64f46cb342b9adadc790960cc9264d71122ead",
            "E_START_DIGEST")
    return records, common_lb, common_ub


def region_rmse(Dx: np.ndarray, prediction: np.ndarray) -> tuple[float, float]:
    peaks, _ = find_peaks(Dx, prominence=Dx.max() * 0.04)
    valleys, _ = find_peaks(-Dx, prominence=Dx.max() * 0.02)
    def calculate(indices: np.ndarray, halfwidth: int = 5) -> float:
        require(len(indices) > 0, "E_EMPTY_REGION")
        mask = np.zeros_like(Dx, bool)
        for index in indices:
            mask[max(0, index - halfwidth): index + halfwidth] = True
        return float(np.sqrt(np.mean((Dx[mask] - prediction[mask]) ** 2)))
    return calculate(peaks), calculate(valleys)


def metrics(Vx: np.ndarray, Dx: np.ndarray, params: np.ndarray) -> dict[str, Any]:
    prediction = model(Vx, params)
    residual = Dx - prediction
    rss = float(np.sum(residual ** 2))
    r2 = 1.0 - rss / float(np.sum((Dx - Dx.mean()) ** 2))
    bic = len(Dx) * np.log(max(rss, 1e-300) / len(Dx)) + len(params) * np.log(len(Dx))
    peak, valley = region_rmse(Dx, prediction)
    area_model = float(TRAPZ(prediction, Vx))
    area_data = float(TRAPZ(Dx, Vx))
    return {
        "R2": float(r2), "BIC": float(bic), "peakRMSE": peak, "valleyRMSE": valley,
        "npar": int(len(params)), "area_model": area_model, "area_data": area_data,
        "area_abs_error": abs(area_model - area_data), "bg": float(params[-1]),
        "rss": rss, "cost": 0.5 * rss, "prediction_sha256": array_sha256(prediction),
    }


def execute_fit(runtime_label: str, output: Path) -> None:
    require(platform.python_version().startswith(runtime_label.removeprefix("python")),
            "E_RUNTIME_VERSION", f"{runtime_label}:{platform.python_version()}")
    V, Q, raw, _columns = parse_raw()
    Vx, Dx, process_info = preprocess(V, Q)
    starts, lb, ub = make_starts(Vx, Dx)
    trials: list[dict[str, Any]] = []
    best_index = -1
    best_cost = math.inf
    best_vector: np.ndarray | None = None
    for index, start_record in enumerate(starts):
        start = np.asarray(start_record["vector"], dtype=float)
        result = least_squares(lambda p: model(Vx, p) - Dx, start, bounds=(lb, ub), max_nfev=NFEV)
        trial = {
            "index": index,
            "strategy": start_record["strategy"],
            "restart": start_record["restart"],
            "start_sha256": start_record["sha256"],
            "success": bool(result.success),
            "status": int(result.status),
            "cost": float(result.cost),
            "optimality": float(result.optimality),
            "nfev": int(result.nfev),
            "njev": None if result.njev is None else int(result.njev),
            "active_mask": [int(x) for x in result.active_mask],
            "returned_vector": [float(x) for x in result.x],
            "returned_vector_sha256": array_sha256(result.x),
        }
        trials.append(trial)
        if result.cost < best_cost:
            best_index, best_cost, best_vector = index, float(result.cost), np.asarray(result.x, float)
    require(best_vector is not None, "E_ALL_FITS_FAILED")
    record = {
        "schema_version": "phase066-step77-runtime-fit-v1",
        "runtime_label": runtime_label,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "numpy_version": np.__version__,
        "scipy_version": scipy_version,
        "actual_optimizer_executed": True,
        "optimizer_call_count": len(trials),
        "successful_call_count": sum(1 for t in trials if t["success"]),
        "raw_sha256": sha256(raw),
        "V_sha256": array_sha256(Vx),
        "D_sha256": array_sha256(Dx),
        "processed_input": process_info,
        "bounds_sha256": {"lower": array_sha256(lb), "upper": array_sha256(ub)},
        "start_matrix_sha256": "3d5c9a7b04cfbd4a6773d9d45d64f46cb342b9adadc790960cc9264d71122ead",
        "best_trial": best_index,
        "best_vector": [float(x) for x in best_vector],
        "best_vector_sha256": array_sha256(best_vector),
        "metrics": metrics(Vx, Dx, best_vector),
        "trials": trials,
    }
    write_temp_json(output, record)
    print(f"FIT_P066_STEP77_{runtime_label} best_trial={best_index} cost={best_cost:.12g}")


def source_record(path: str) -> dict[str, Any]:
    raw = git_bytes(path)
    return {
        "path": path,
        "git_blob_sha1": git_blob_id(path),
        "raw_sha256": sha256(raw),
        "bytes": len(raw),
        "lines": len(raw.decode("utf-8").splitlines()),
    }


def math_rederivation() -> dict[str, Any]:
    alphas = [0.15, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    z = np.linspace(-350.0, 40.0, 2_000_001)
    sig = 1.0 / (1.0 + np.exp(-z))
    normalization_errors = []
    fd_errors = []
    direction_fd_errors = []
    reflection_errors = []
    for alpha in alphas:
        profile = alpha * sig ** alpha * (1.0 - sig)
        normalization_errors.append(abs(float(TRAPZ(profile, z)) - 1.0))
        sample = np.linspace(-8.0, 8.0, 2001)
        step = 1.0e-6
        plus = (1.0 / (1.0 + np.exp(-(sample + step)))) ** alpha
        minus = (1.0 / (1.0 + np.exp(-(sample - step)))) ** alpha
        numerical = (plus - minus) / (2.0 * step)
        base_sig = 1.0 / (1.0 + np.exp(-sample))
        analytic = alpha * base_sig ** alpha * (1.0 - base_sig)
        mask = analytic > 1.0e-7
        fd_errors.append(float(np.max(np.abs(numerical[mask] - analytic[mask]) /
                                              np.maximum(np.abs(analytic[mask]), 1.0e-15))))
        for direction in (-1.0, 1.0):
            sample_V = np.linspace(-8.0, 8.0, 2001)
            plus_sig = 1.0 / (1.0 + np.exp(-direction * (sample_V + step)))
            minus_sig = 1.0 / (1.0 + np.exp(-direction * (sample_V - step)))
            signed_numeric = (plus_sig ** alpha - minus_sig ** alpha) / (2.0 * step)
            direct_sig = 1.0 / (1.0 + np.exp(-direction * sample_V))
            signed_analytic = direction * alpha * direct_sig ** alpha * (1.0 - direct_sig)
            signed_mask = np.abs(signed_analytic) > 1.0e-7
            direction_fd_errors.append(float(np.max(
                np.abs(signed_numeric[signed_mask] - signed_analytic[signed_mask]) /
                np.maximum(np.abs(signed_analytic[signed_mask]), 1.0e-15))))
        positive = alpha * (1.0 / (1.0 + np.exp(-sample))) ** alpha * \
            (1.0 - 1.0 / (1.0 + np.exp(-sample)))
        negative_reflected = alpha * (1.0 / (1.0 + np.exp(sample[::-1]))) ** alpha * \
            (1.0 - 1.0 / (1.0 + np.exp(sample[::-1])))
        reflection_errors.append(float(np.max(np.abs(positive - negative_reflected))))
    extreme = np.asarray([-1000.0, -350.0, -100.0, 0.0, 100.0, 350.0, 1000.0])
    safe_sig = np.empty_like(extreme)
    positive = extreme >= 0
    safe_sig[positive] = 1.0 / (1.0 + np.exp(-np.minimum(extreme[positive], 350.0)))
    ez = np.exp(np.maximum(extreme[~positive], -350.0))
    safe_sig[~positive] = ez / (1.0 + ez)
    alpha_one = sig * (1.0 - sig)
    formula_one = 1.0 * sig ** 1.0 * (1.0 - sig)
    fit_sig = sigmoid(extreme, 0.0, 1.0)
    fit_profile = component(extreme, 0.0, 1.0, 1.0, 0.15)
    fit_alpha_one = component(np.linspace(-30.0, 30.0, 2001), 0.0, 1.0, 1.0, 1.0)
    fit_base = sigmoid(np.linspace(-30.0, 30.0, 2001), 0.0, 1.0)
    fit_base = fit_base * (1.0 - fit_base)
    direction_sample = np.linspace(-8.0, 8.0, 2001)
    reverse_sig = 1.0 / (1.0 + np.exp(direction_sample))
    reverse_magnitude = 2.0 * reverse_sig ** 2.0 * (1.0 - reverse_sig)
    reverse_signed = -reverse_magnitude
    magnitude_distinction = bool(np.all(reverse_magnitude >= 0.0) and
                                 np.all(reverse_signed <= 0.0) and
                                 np.array_equal(reverse_magnitude, np.abs(reverse_signed)))
    clip_probe = np.asarray([-351.0, -350.0, -349.0])
    clip_coordinate = sigmoid(clip_probe, 0.0, 1.0) ** 0.15
    clip_fd = (clip_coordinate[1] - clip_coordinate[0])
    clip_helper = float(component(np.asarray([-351.0]), 0.0, 1.0, 1.0, 0.15)[0])
    clip_mismatch = bool(clip_fd == 0.0 and clip_helper > 0.0)
    eager_overflow = False
    try:
        with np.errstate(over="raise", invalid="raise"):
            eager_z = np.asarray([-1000.0, 1000.0])
            np.where(eager_z >= 0, 1.0 / (1.0 + np.exp(-eager_z)),
                     np.exp(eager_z) / (1.0 + np.exp(eager_z)))
    except FloatingPointError:
        eager_overflow = True
    return {
        "base_coordinate": "sigma=1/(1+exp(-d*(V-U)/w)); d in {-1,+1}",
        "skew_coordinate": "xi=sigma**alpha",
        "chain_rule": "dxi/dV=alpha*sigma**(alpha-1)*(dsigma/dV); dsigma/dV=d*sigma*(1-sigma)/w",
        "analytic_derivative": "dxi/dV=d*(alpha/w)*sigma**alpha*(1-sigma)",
        "component_profile": "dQ/dV=Q*abs(dxi/dV); Direct14 fixes d=+1",
        "normalization": "integral[-inf,+inf](dQ/dV)dV=Q for Q finite,w>0,alpha>0",
        "center": "U is sigma=1/2 coordinate; it is not the profile mode unless alpha=1",
        "mode": "V_mode=U+d*w*ln(alpha)",
        "profile_slope": "d(dQ/dV)/dV=(d/w)*(dQ/dV)*(alpha-(alpha+1)*sigma)",
        "domains": {"w": "w>0", "alpha": "alpha>0", "Q": "finite; fitted bound Q>0",
                    "V_U_bg": "finite real"},
        "parameter_order": ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
        "interpretation_ceiling": {
            "U": "underlying sigmoid half-coordinate, not an independently identified material phase",
            "w": "empirical voltage-width scale",
            "Q": "component area on the fitted capacity basis",
            "alpha": "empirical equilibrium-shape skew parameter; not a new phase or material constant",
            "bg": "free additive dQ/dV background",
        },
        "probes": {
            "alphas": alphas,
            "normalization_max_abs_error": max(normalization_errors),
            "finite_difference_max_rel_error": max(fd_errors),
            "direction_fd_max_rel_error": max(direction_fd_errors),
            "direction_reflection_max_abs_error": max(reflection_errors),
            "production_magnitude_signed_distinction_pass": magnitude_distinction,
            "alpha_one_max_abs_error": float(np.max(np.abs(alpha_one - formula_one))),
            "fit_alpha_one_max_abs_error": float(np.max(np.abs(fit_alpha_one - fit_base))),
            "positive_profile": bool(all(np.all(a * sig ** a * (1 - sig) >= 0) for a in alphas)),
            "safe_extreme_branch_finite": bool(np.isfinite(safe_sig).all()),
            "fit_kernel_extreme_finite": bool(np.isfinite(fit_sig).all() and np.isfinite(fit_profile).all()),
            "fit_clip_outside_derivative_mismatch_observed": clip_mismatch,
            "production_eager_overflow_observed": eager_overflow,
            "lower_limit": float(safe_sig[0]),
            "upper_limit_error": float(1.0 - safe_sig[-1]),
            "clip_branch": "fit kernel clips z to [-350,350]; production func_ksi_eq uses sign-stable piecewise logistic",
            "clip_derivative_ceiling": "outside |z|<350 the clipped coordinate is constant, so the helper profile is not its exact derivative; normalization claim is analytic/interior, not a clipped whole-real-line identity",
            "production_eager_branch_ceiling": "numpy.where evaluates both exponential branches and can emit overflow warnings at extreme finite z although the selected final value is finite",
        },
    }


def load_runtime(path: Path, expected_label: str) -> dict[str, Any]:
    require(temp_contained(path), "E_RUNTIME_INPUT_LOCATION", str(path))
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    require(value["semantic_sha256"] == sha256(canonical_bytes({**value, "semantic_sha256": ""})),
            "E_RUNTIME_SEMANTIC", expected_label)
    require(value["runtime_label"] == expected_label, "E_RUNTIME_LABEL")
    require(value["python_version"].startswith(expected_label.removeprefix("python")), "E_RUNTIME_VERSION")
    value["sealed_runtime_record_semantic_sha256"] = value.pop("semantic_sha256")
    value["sealed_runtime_record_sha256"] = sha256(raw)
    value["external_process_evidence"] = {
        "collector_verified_disposable_temp_input": True,
        "sealed_result_record_available": True,
        "argv": "GROUND_NOT_FOUND; not captured inside the sealed runtime result",
        "cwd": "GROUND_NOT_FOUND; not captured inside the sealed runtime result",
        "exit_code": "GROUND_NOT_FOUND; caller observation was not sealed",
        "stdout_sha256": "GROUND_NOT_FOUND; caller stream was not sealed",
        "stderr_sha256": "GROUND_NOT_FOUND; caller stream was not sealed",
        "temporary_input_cleanup": "SCHEDULED_AFTER_PUSH_BEFORE_STEP77_PERSISTENCE_VALIDATION",
    }
    return value


def rounded_metric_pass(calculated: dict[str, Any], reported: dict[str, Any]) -> bool:
    return (
        round(calculated["R2"], 5) == reported["R2"] and
        round(calculated["BIC"], 1) == reported["BIC"] and
        round(calculated["peakRMSE"], 3) == reported["peakRMSE"] and
        round(calculated["valleyRMSE"], 3) == reported["valleyRMSE"] and
        round(calculated["area_model"], 4) == reported["area_model"] and
        round(calculated["area_data"], 4) == reported["area_data"] and
        round(calculated["bg"], 6) == reported["bg"]
    )


def collect(runtime312_path: Path, runtime314_path: Path) -> None:
    run312 = load_runtime(runtime312_path, "python3.12")
    run314 = load_runtime(runtime314_path, "python3.14")
    V, Q, raw, columns = parse_raw()
    Vx, Dx, process_info = preprocess(V, Q)
    starts, lb, ub = make_starts(Vx, Dx)
    require(run312["V_sha256"] == run314["V_sha256"] == array_sha256(Vx), "E_CROSS_V")
    require(run312["D_sha256"] == run314["D_sha256"] == array_sha256(Dx), "E_CROSS_D")
    stored_all = json.loads(git_bytes(STORED_PATH).decode("utf-8"))
    stored = stored_all["C_skew"]["blend"]
    stored_vector = np.asarray(stored["params"], dtype=float)
    reported = {key: stored[key] for key in
                ("R2", "BIC", "peakRMSE", "valleyRMSE", "npar", "area_model", "area_data", "bg")}
    stored_eval = metrics(Vx, Dx, stored_vector)
    vector312 = np.asarray(run312["best_vector"], dtype=float)
    vector314 = np.asarray(run314["best_vector"], dtype=float)
    pred_stored = model(Vx, stored_vector)
    pred312 = model(Vx, vector312)
    pred314 = model(Vx, vector314)
    tolerances = {
        "stored_metric_rounding": {"R2": 5.0e-6, "BIC": 0.05, "rmse": 5.0e-4,
                                   "area": 5.0e-5, "bg": 5.0e-7},
        "ordered_parameter_max_abs": 5.0e-8,
        "runtime_curve_max_abs": 2.0e-5,
        "runtime_vs_stored_curve_rmse": 2.0e-3,
        "runtime_vs_stored_cost_relative": 1.0e-3,
        "runtime_R2_floor": 0.9995,
    }
    runtime_curve_max = float(np.max(np.abs(pred312 - pred314)))
    runtime_stored_rmse = {
        "python3.12": float(np.sqrt(np.mean((pred312 - pred_stored) ** 2))),
        "python3.14": float(np.sqrt(np.mean((pred314 - pred_stored) ** 2))),
    }
    ordered_max = {
        "python3.12": float(np.max(np.abs(vector312 - stored_vector))),
        "python3.14": float(np.max(np.abs(vector314 - stored_vector))),
    }
    stored_cost = stored_eval["cost"]
    science_pass = all(
        run["metrics"]["R2"] >= tolerances["runtime_R2_floor"] and
        run["metrics"]["cost"] <= stored_cost * (1.0 + tolerances["runtime_vs_stored_cost_relative"])
        for run in (run312, run314)
    )
    curve_pass = (runtime_curve_max <= tolerances["runtime_curve_max_abs"] and
                  max(runtime_stored_rmse.values()) <= tolerances["runtime_vs_stored_curve_rmse"])
    exact_parameters = max(ordered_max.values()) <= tolerances["ordered_parameter_max_abs"]
    execution_complete = all(run["optimizer_call_count"] == 12 for run in (run312, run314))
    selected_trial_converged = all(
        run["trials"][run["best_trial"]]["success"] for run in (run312, run314)
    )
    generator_identity = {
        "path": BUILDER_RELATIVE_PATH,
        "raw_sha256": sha256((ROOT / BUILDER_RELATIVE_PATH).read_bytes()),
    }

    raw_record = source_record(RAW_PATH)
    raw_record.update({
        "columns": columns,
        "column_units": {"V_vs_Li": "V versus Li/Li+", "Q_mAh": "mAh"},
        "data_rows": 16735,
        "source_kind": "repository-derived CSV consumed by Direct14; not original experimental parquet",
        "capacity_basis": "absolute_mAh_not_mass_normalized",
        "specimen_protocol_status": "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND",
        "source_declared_specimen": "graphite+Si blend half-cell",
        "source_declared_protocol": "pOCV, C/50, room temperature approximately 25 C",
        "source_declaration_path": SOURCES_PATH,
        "ground_not_found": [
            "exact original Zenodo parquet key and checksum",
            "specimen UUID and composition binding for sigr.csv",
            "extraction script-to-parquet cryptographic binding",
        ],
        "bounded_dataset_claim": "SINTEF/EU IntelLiGent Zenodo 20086298, CC-BY-4.0, half-cell versus Li; exact blend protocol unbound",
    })
    provenance = {
        "schema_version": "phase066-step77-fit-input-provenance-v1",
        "baseline_commit": BASELINE,
        "generator_identity": generator_identity,
        "raw_input": raw_record,
        "source_code": [source_record(path) for path in
                        (SOURCES_PATH, DRIVER_PATH, PREPROCESS_PATH, ENSEMBLE_PATH, SEED_PATH,
                         STORED_PATH, PARAMS_PATH, RELEASE_PATH)],
        "preprocessing": {
            "steps": [
                "finite rows", "stable ascending Q sort", "unique Q retaining first V",
                "increasing isotonic regression V(Q)", "uniform V grid and right-continuous cumulative Q",
                "forward Q difference divided by dV", "positive finite bins",
                "longest contiguous interval", "absolute Savitzky-Golay direct/reciprocal median ensemble",
            ],
            "window_V": [VLO, VHI], "grid_step_V": DV,
            "savgol_ratios": [0.01, 0.02, 0.03], "savgol_polyorder": 3,
            "weighting": "unit_weight_per_retained_grid_point",
            "wavelet_or_bdd_dmsmcd_used": False,
        },
        "processed_input": {
            **process_info, "points": len(Vx), "V_sha256": array_sha256(Vx),
            "D_sha256": array_sha256(Dx), "dtype_serialization": "little-endian float64 C-order",
        },
        "optimizer_contract": {
            "kernel": "skew-logistic", "components": N,
            "parameter_order": ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
            "free_mask": "implicit_all_57_parameters_free; no persisted explicit mask",
            "bounds": {
                "U": [float(Vx.min()), float(Vx.max())], "w": [WLO, WHI],
                "Q": [1e-9, 10.0 * process_info["area_data"]], "alpha": [0.15, 8.0],
                "bg": [min(0.0, float(Dx.min())), max(float(Dx.max()), 1e-9)],
            },
            "bounds_sha256": {"lower": array_sha256(lb), "upper": array_sha256(ub)},
            "initial_vectors_sha256": [record["sha256"] for record in starts],
            "start_matrix_sha256": "3d5c9a7b04cfbd4a6773d9d45d64f46cb342b9adadc790960cc9264d71122ead",
            "rng_seed": RNG_SEED, "rng_draws_before_direct14": 1908,
            "rng_draws_within_direct14": 513, "seed_strategies": 3,
            "restarts_per_strategy": RESTARTS, "max_nfev": NFEV,
            "objective": "source_explicit_unweighted_residual=model(V)-D",
            "solver": "scipy.optimize.least_squares",
            "source_explicit_options": ["bounds", "max_nfev"],
            "replay_runtime_resolved_defaults": {
                "loss": "linear", "method": "trf",
                "note": "observed defaults of the recorded replay runtimes; not historical source-pinned values",
            },
            "historical_resolved_defaults_and_scipy_version": "GROUND_NOT_FOUND",
        },
        "runtime_input_identity": {
            "python3.12": {k: run312[k] for k in ("python_version", "numpy_version", "scipy_version", "V_sha256", "D_sha256")},
            "python3.14": {k: run314[k] for k in ("python_version", "numpy_version", "scipy_version", "V_sha256", "D_sha256")},
        },
    }
    fit = {
        "schema_version": "phase066-step77-direct14-fit-reproduction-v1",
        "baseline_commit": BASELINE,
        "generator_identity": generator_identity,
        "gate": GATE,
        "status": ("NUMERICAL_CURVE_REPRODUCED_FROM_REPOSITORY_DERIVED_CSV; "
                   "SELECTED_TRIAL_NONCONVERGED") if science_pass and curve_pass and not selected_trial_converged else
                  ("NUMERICAL_CURVE_REPRODUCED_FROM_REPOSITORY_DERIVED_CSV; "
                   "SELECTED_TRIAL_CONVERGED") if science_pass and curve_pass else "REPRODUCTION_MISMATCH",
        "mathematical_rederivation": math_rederivation(),
        "runtime_reproductions": [run312, run314],
        "stored_evidence": {
            "source_path": STORED_PATH,
            "source_git_blob_sha1": git_blob_id(STORED_PATH),
            "parameter_vector_8dp": [float(x) for x in stored_vector],
            "reported_metrics": reported,
            "transition_only_path": PARAMS_PATH,
            "original_full_precision_optimizer_state": "GROUND_NOT_FOUND",
            "original_optimizer_diagnostics_and_environment": "GROUND_NOT_FOUND",
            "full_precision_stored_curve": "GROUND_NOT_FOUND; only rasterized PNG retained",
            "stored_vector_self_evaluation": stored_eval,
        },
        "comparison": {
            "predeclared_tolerances": tolerances,
            "stored_vector_self_evaluation_pass": rounded_metric_pass(stored_eval, reported),
            "runtime_numerical_agreement_pass": science_pass,
            "runtime_curve_agreement_pass": curve_pass,
            "ordered_parameter_exact_reproduction": exact_parameters,
            "ordered_parameter_max_abs": ordered_max,
            "cross_runtime_curve_max_abs": runtime_curve_max,
            "runtime_vs_stored_curve_rmse": runtime_stored_rmse,
            "runtime_cost_relative_to_stored": {
                "python3.12": float(run312["metrics"]["cost"] / stored_cost - 1.0),
                "python3.14": float(run314["metrics"]["cost"] / stored_cost - 1.0),
            },
            "interpretation": "ordered parameter equality is stricter than equivalent in-sample curve reproduction and is reported separately",
        },
        "optimizer_execution_complete": execution_complete,
        "selected_trial_converged": selected_trial_converged,
        "runtime_success": selected_trial_converged,
        "scientific_validity": "bounded to in-sample numerical replay of repository-derived CSV",
        "authority_ceiling": {
            "material_assignment_authority": False,
            "phase_identification_authority": False,
            "parameter_identifiability_authority": False,
            "external_scientific_validation": False,
            "exact_historical_optimizer_state_reconstruction": False,
        },
    }
    require(rounded_metric_pass(stored_eval, reported) and execution_complete and science_pass and curve_pass,
            "E_GATE_NOT_SATISFIED")
    atomic_write_pair(PROVENANCE_PATH, provenance, FIT_PATH, fit)
    print(f"{GATE} stored_self=True execution_complete=True science={science_pass} "
          f"curve={curve_pass} selected_converged={selected_trial_converged} exact_params={exact_parameters}")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    fit_parser = sub.add_parser("fit")
    fit_parser.add_argument("--runtime-label", required=True, choices=("python3.12", "python3.14"))
    fit_parser.add_argument("--output", type=Path, required=True)
    collect_parser = sub.add_parser("collect")
    collect_parser.add_argument("--runtime312", type=Path, required=True)
    collect_parser.add_argument("--runtime314", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "fit":
        execute_fit(args.runtime_label, args.output)
    else:
        collect(args.runtime312, args.runtime314)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildFailure, KeyError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL_P066_STEP77_BUILD {error}", file=sys.stderr)
        raise SystemExit(1)
