from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import isotonic_regression
from scipy.signal import find_peaks, savgol_filter


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "38e00020906e3a024e493c214c1a99a6f8ab07d2"
EXPECTED_SUBJECT = "audit(phase066): reproduce skew direct14 fitting"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "CONDITIONAL_P066_STEP77_FIT_REPLAY_WITH_NONCONVERGED_SELECTED_TRIAL_AND_UNSEALED_PROCESS_LOGS"
PERSISTENCE = "PASS_P066_STEP77_PERSISTENCE"
RAW_PATH = "Claude/results/comp_v24/sintef_data/sigr.csv"
SOURCES_PATH = "Claude/results/comp_v24/sintef_data/SOURCES.md"
STORED_PATH = "Claude/results/comp_v26_data/out_versions/summary_versions.json"
DRIVER_PATH = "Claude/results/comp_v26_data/build_two_versions.py"
PREPROCESS_PATH = "Claude/results/comp_v26_data/test_skew_regsol_v2.py"
ENSEMBLE_PATH = "Claude/results/comp_v26_data/bdd_dqdv.py"
SEED_PATH = "Claude/results/comp_v26_data/test_gallery_vs_regsol.py"
PARAMS_PATH = "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json"
RELEASE_PATH = "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
EXPECTED_RAW_SHA256 = "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6"
EXPECTED_V_SHA256 = "6c7ca15d7b9eaf80561d2d2d834856c9b3076f31f6d7e4e6ce304ddb266020b4"
EXPECTED_D_SHA256 = "713c1de666d84e29edd55fbaab5b6321bfe505fb25cfe03c0b727a88bce743ce"
EXPECTED_LB_SHA256 = "56a35d64e713853ca0fb0a72dfc1c787f0ea36790b08d406a5faa0df5545e796"
EXPECTED_UB_SHA256 = "0bea5037639ce74c22f20f45e0def0a2d57bca053467ab04cef671d839ad7517"
EXPECTED_START_SHA256 = "3d5c9a7b04cfbd4a6773d9d45d64f46cb342b9adadc790960cc9264d71122ead"
EXPECTED_RUNTIME_SEALS = {
    "python3.12": {"raw": "279df24f1d7758dd35b5c217696d3c41557dba772d62eccb83148c4aae857a61",
                   "semantic": "cef03c80688fd02e65c35ccfb7a0b322234dbe665432b5f80b5053c3c94ba4ba"},
    "python3.14": {"raw": "2d271429355cf9a33424246d5216092b0230e125dff3d5571266c61de288aa3d",
                   "semantic": "1f284ce29c717558115908b71eb1913cdfd204eca47ec75544e74ac51d7a9fe3"},
}

BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step77.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step77.py"
FIT_PATH = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
PROVENANCE_PATH = "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_077_FIT_REPRODUCTION_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

FINAL_PATHS = [
    HANDOVER_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    FIT_PATH,
    PROVENANCE_PATH,
    RESULT_PATH,
    BUILDER_PATH,
    VALIDATOR_PATH,
]


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationFailure(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone["semantic_sha256"] = ""
    return sha256(canonical_bytes(clone))


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def strict_load(path: str) -> dict[str, Any]:
    raw = (ROOT / path).read_bytes()
    require(raw.endswith(b"\n") and b"\r" not in raw, "E_JSON_LF", path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    require(isinstance(value, dict), "E_JSON_ROOT", path)
    require(canonical_bytes(value) == raw, "E_JSON_CANONICAL", path)
    require(value.get("semantic_sha256") == semantic_hash(value), "E_JSON_SEMANTIC", path)
    return value


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    baseline_paths = {RAW_PATH, SOURCES_PATH, DRIVER_PATH, PREPROCESS_PATH, ENSEMBLE_PATH,
                      SEED_PATH, STORED_PATH, PARAMS_PATH, RELEASE_PATH}
    exact = {
        ("rev-parse", "HEAD"), ("rev-parse", "HEAD^"),
        ("rev-parse", "--abbrev-ref", "@{u}"), ("rev-parse", UPSTREAM),
        ("rev-parse", f"origin/{PROTECTED_BRANCH}"), ("rev-parse", "origin/main"),
        ("rev-parse", PROTECTED_BRANCH),
        ("branch", "--show-current"), ("remote", "get-url", "origin"),
        ("diff", "--cached", "--name-only"), ("diff", "--name-only"),
        ("diff", "--cached", "--check"), ("diff", "--cached", "--name-status"),
        ("diff", "--name-only", "HEAD^"), ("ls-files", "--others", "--exclude-standard"),
        ("show", "-s", "--format=%s", "HEAD"), ("status", "--porcelain"),
        ("rev-list", "--parents", "-n", "1", "HEAD"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}"),
        ("ls-remote", "--heads", "origin", "refs/heads/main"),
    }
    baseline_read = (len(args) == 3 and args[0] == "cat-file" and args[1] == "blob" and
                     args[2].startswith(BASELINE + ":") and
                     args[2][len(BASELINE) + 1:] in baseline_paths)
    baseline_id = (len(args) == 2 and args[0] == "rev-parse" and
                   args[1].startswith(BASELINE + ":") and
                   args[1][len(BASELINE) + 1:] in baseline_paths)
    require(input_bytes is None and (args in exact or baseline_read or baseline_id),
            "E_GIT_ARG_ALLOWLIST", repr(args))
    run = subprocess.run(["git", *args], cwd=ROOT, input=input_bytes,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=False, check=False)
    require(run.returncode == 0, "E_GIT", run.stderr.decode("utf-8", "replace"))
    return run.stdout


def finite_tree(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            finite_tree(item)
    elif isinstance(value, list):
        for item in value:
            finite_tree(item)
    elif isinstance(value, float):
        require(math.isfinite(value), "E_NONFINITE")


def require_keys(value: dict[str, Any], expected: str, code: str) -> None:
    require(set(value) == set(expected.split()), code,
            f"missing={sorted(set(expected.split()) - set(value))}; extra={sorted(set(value) - set(expected.split()))}")


def array_sha256(value: np.ndarray) -> str:
    return sha256(np.asarray(value, dtype="<f8").tobytes(order="C"))


def independent_preprocess(raw: bytes) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8"), newline="")))
    require(rows[0] == ["V_vs_Li", "Q_mAh"] and len(rows) == 16736, "E_RAW_TABLE")
    values = np.asarray([[float(a), float(b)] for a, b in rows[1:]], dtype=float)
    require(np.isfinite(values).all(), "E_RAW_NUMERIC")
    V, Q = values[:, 0], values[:, 1]
    valid = np.isfinite(V) & np.isfinite(Q)
    order = np.argsort(Q[valid], kind="mergesort")
    V, Q = V[valid][order], Q[valid][order]
    Qu, indices = np.unique(Q, return_index=True)
    Vm = isotonic_regression(V[indices], increasing=True).x
    grid = np.arange(0.060, 0.700 + 0.5 * 5.0e-4, 5.0e-4)
    locations = np.searchsorted(Vm, grid, side="right") - 1
    Qg = np.where(locations >= 0, Qu[np.clip(locations, 0, len(Qu) - 1)], 0.0)
    centers = 0.5 * (grid[:-1] + grid[1:])
    derivative = np.diff(Qg) / 5.0e-4
    keep = np.isfinite(derivative) & (derivative > 0)
    usable = np.flatnonzero(keep)
    runs = np.split(usable, np.flatnonzero(np.diff(usable) > 1) + 1)
    longest = max(runs, key=len)
    Vx = centers[longest[0]: longest[-1] + 1]
    base = derivative[longest[0]: longest[-1] + 1]
    ensemble = [np.asarray(base, float)]
    for ratio in (0.01, 0.02, 0.03):
        window = int(round(len(base) * ratio // 2)) * 2 + 1
        if window <= 3 or window >= len(base):
            continue
        try:
            ensemble.append(savgol_filter(base, window, 3))
        except Exception:
            pass
        with np.errstate(divide="ignore", invalid="ignore"):
            try:
                ensemble.append(1.0 / savgol_filter(1.0 / base, window, 3))
            except Exception:
                pass
    stack = np.asarray(ensemble, float)
    stack[~np.isfinite(stack)] = np.nan
    with np.errstate(invalid="ignore"):
        Dx = np.abs(np.nanmedian(stack, axis=0))
    require(len(Vx) == len(Dx) == 1280, "E_INDEPENDENT_POINTS")
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
        "area_data": float(np.trapezoid(Dx, Vx)),
    }
    return Vx, Dx, info


def independent_contract(Vx: np.ndarray, Dx: np.ndarray) -> tuple[list[str], str, str]:
    n = 14
    area = float(np.trapezoid(Dx, Vx))
    peak_indices, _ = find_peaks(Dx, prominence=Dx.max() * 0.02)
    peaks = list(Vx[peak_indices][np.argsort(-Dx[peak_indices])])
    lo, hi = float(Vx.min()), float(Vx.max())
    first = peaks[:n]
    while len(first) < n:
        first.append(lo + (hi - lo) * (len(first) + 0.5) / (n + 1))
    second = list(np.linspace(lo + 0.05 * (hi - lo), hi - 0.05 * (hi - lo), n))
    third = peaks[:n]
    while len(third) < n:
        third.append(float(peaks[len(third) % len(peaks)]) * (1 + 0.01 * len(third)))
    rng = np.random.default_rng(23)
    for count in (17, 17, 33, 22, 22, 43, 29, 29):
        for _strategy in range(3):
            for _restart in range(1, 4):
                rng.uniform(0.75, 1.25, count)
    hashes: list[str] = []
    serialized: list[bytes] = []
    lower = upper = None
    for U in (first, second, third[:n]):
        p0 = U + [0.004] * n + [area / n] * n + [1.0] * n + [float(Dx.min())]
        lb = [lo] * n + [0.0001] * n + [1e-9] * n + [0.15] * n + [min(0.0, float(Dx.min()))]
        ub = [hi] * n + [0.12] * n + [10.0 * area] * n + [8.0] * n + [max(float(Dx.max()), 1e-9)]
        p0, lower, upper = (np.asarray(x, float) for x in (p0, lb, ub))
        p0 = np.clip(p0, lower, upper)
        for restart in range(4):
            start = p0 if restart == 0 else np.clip(p0 * rng.uniform(0.75, 1.25, p0.size), lower, upper)
            hashes.append(array_sha256(start)); serialized.append(np.asarray(start, dtype="<f8").tobytes())
    require(lower is not None and upper is not None, "E_INDEPENDENT_BOUNDS")
    require(sha256(b"".join(serialized)) == EXPECTED_START_SHA256, "E_INDEPENDENT_START")
    return hashes, array_sha256(lower), array_sha256(upper)


def independent_model(V: np.ndarray, params: np.ndarray) -> np.ndarray:
    result = np.full(V.size, params[-1])
    for index in range(14):
        z = np.clip((V - params[index]) / params[14 + index], -350.0, 350.0)
        sig = 1.0 / (1.0 + np.exp(-z))
        result += params[28 + index] * (params[42 + index] / params[14 + index]) * \
            sig ** params[42 + index] * (1.0 - sig)
    return result


def independent_metrics(Vx: np.ndarray, Dx: np.ndarray, params: np.ndarray) -> dict[str, float]:
    prediction = independent_model(Vx, params)
    residual = Dx - prediction
    rss = float(np.sum(residual ** 2))
    peaks, _ = find_peaks(Dx, prominence=Dx.max() * 0.04)
    valleys, _ = find_peaks(-Dx, prominence=Dx.max() * 0.02)
    def regional(indices: np.ndarray) -> float:
        mask = np.zeros_like(Dx, bool)
        for index in indices:
            mask[max(0, index - 5): index + 5] = True
        return float(np.sqrt(np.mean((Dx[mask] - prediction[mask]) ** 2)))
    area_model = float(np.trapezoid(prediction, Vx)); area_data = float(np.trapezoid(Dx, Vx))
    return {
        "rss": rss,
        "cost": 0.5 * rss,
        "R2": 1.0 - rss / float(np.sum((Dx - Dx.mean()) ** 2)),
        "BIC": len(Dx) * math.log(max(rss, 1e-300) / len(Dx)) + len(params) * math.log(len(Dx)),
        "peakRMSE": regional(peaks), "valleyRMSE": regional(valleys),
        "area_model": area_model, "area_data": area_data,
        "area_abs_error": abs(area_model - area_data), "bg": float(params[-1]),
        "prediction_sha256": array_sha256(prediction),
    }


def validate_math(fit: dict[str, Any]) -> None:
    math_record = fit["mathematical_rederivation"]
    require_keys(math_record, "analytic_derivative base_coordinate center chain_rule component_profile "
                 "domains interpretation_ceiling mode normalization parameter_order probes profile_slope "
                 "skew_coordinate", "E_MATH_SCHEMA")
    require_keys(math_record["domains"], "Q V_U_bg alpha w", "E_MATH_DOMAINS_SCHEMA")
    require_keys(math_record["interpretation_ceiling"], "Q U alpha bg w", "E_MATH_INTERPRETATION_SCHEMA")
    require(math_record["base_coordinate"] == "sigma=1/(1+exp(-d*(V-U)/w)); d in {-1,+1}", "E_MATH_BASE")
    require(math_record["skew_coordinate"] == "xi=sigma**alpha", "E_MATH_SKEW")
    require(math_record["analytic_derivative"] ==
            "dxi/dV=d*(alpha/w)*sigma**alpha*(1-sigma)", "E_MATH_DERIVATIVE")
    require(math_record["mode"] == "V_mode=U+d*w*ln(alpha)", "E_MATH_MODE")
    require(math_record["component_profile"] == "dQ/dV=Q*abs(dxi/dV); Direct14 fixes d=+1", "E_SIGNED_MAGNITUDE")
    require(math_record["chain_rule"] ==
            "dxi/dV=alpha*sigma**(alpha-1)*(dsigma/dV); dsigma/dV=d*sigma*(1-sigma)/w",
            "E_CHAIN_RULE")
    require(math_record["profile_slope"] ==
            "d(dQ/dV)/dV=(d/w)*(dQ/dV)*(alpha-(alpha+1)*sigma)", "E_PROFILE_SLOPE")
    require(math_record["center"] ==
            "U is sigma=1/2 coordinate; it is not the profile mode unless alpha=1", "E_CENTER")
    require(math_record["domains"] == {"V_U_bg": "finite real", "Q": "finite; fitted bound Q>0",
            "alpha": "alpha>0", "w": "w>0"}, "E_DOMAINS")
    require(math_record["parameter_order"] == ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
            "E_PARAMETER_ORDER")
    probes = math_record["probes"]
    require_keys(probes, "alpha_one_max_abs_error alphas clip_branch clip_derivative_ceiling "
                 "direction_fd_max_rel_error direction_reflection_max_abs_error "
                 "finite_difference_max_rel_error fit_alpha_one_max_abs_error "
                 "fit_clip_outside_derivative_mismatch_observed fit_kernel_extreme_finite lower_limit "
                 "normalization_max_abs_error positive_profile production_eager_branch_ceiling "
                 "production_eager_overflow_observed production_magnitude_signed_distinction_pass "
                 "safe_extreme_branch_finite upper_limit_error", "E_MATH_PROBE_SCHEMA")
    require(probes["normalization_max_abs_error"] <= 2.0e-8, "E_NORMALIZATION")
    require(probes["finite_difference_max_rel_error"] <= 2.0e-6, "E_DERIVATIVE")
    require(probes["direction_fd_max_rel_error"] <= 2.0e-6, "E_DIRECTION_DERIVATIVE")
    require(probes["direction_reflection_max_abs_error"] <= 1.0e-14, "E_DIRECTION_REFLECTION")
    require(probes["production_magnitude_signed_distinction_pass"] is True, "E_MAGNITUDE_DISTINCTION")
    require(probes["alpha_one_max_abs_error"] == 0.0, "E_ALPHA_ONE")
    require(probes["fit_alpha_one_max_abs_error"] == 0.0, "E_FIT_ALPHA_ONE")
    require(probes["positive_profile"] is True, "E_DERIVATIVE_SIGN")
    require(probes["safe_extreme_branch_finite"] is True, "E_OVERFLOW_BRANCH")
    require(probes["fit_kernel_extreme_finite"] is True, "E_FIT_EXTREME")
    require(probes["fit_clip_outside_derivative_mismatch_observed"] is True, "E_FIT_CLIP_MISMATCH")
    require(probes["production_eager_overflow_observed"] is True, "E_PRODUCTION_EAGER_OVERFLOW")
    require(probes["clip_branch"] ==
            "fit kernel clips z to [-350,350]; production func_ksi_eq uses sign-stable piecewise logistic",
            "E_CLIP_BRANCH")
    require(probes["clip_derivative_ceiling"] ==
            "outside |z|<350 the clipped coordinate is constant, so the helper profile is not its exact derivative; normalization claim is analytic/interior, not a clipped whole-real-line identity",
            "E_CLIP_CEILING")
    require(probes["production_eager_branch_ceiling"] ==
            "numpy.where evaluates both exponential branches and can emit overflow warnings at extreme finite z although the selected final value is finite",
            "E_PRODUCTION_OVERFLOW")
    require(probes["lower_limit"] <= 1.0e-150 and probes["upper_limit_error"] <= 1.0e-14,
            "E_LIMIT")
    # Independent numerical audit of every claimed scalar/boolean probe.
    alphas = probes["alphas"]
    require(alphas == [0.15, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0], "E_PROBE_ALPHAS")
    z = np.linspace(-350.0, 40.0, 2_000_001)
    sig = 1.0 / (1.0 + np.exp(-z))
    norm = max(abs(float(np.trapezoid(a * sig ** a * (1.0 - sig), z)) - 1.0) for a in alphas)
    require(math.isclose(probes["normalization_max_abs_error"], norm, rel_tol=0.0, abs_tol=1e-15),
            "E_PROBE_NORMALIZATION_REPLAY")
    sample = np.linspace(-8.0, 8.0, 2001); step = 1e-6
    fd_errors: list[float] = []; reflection: list[float] = []
    for alpha in alphas:
        for direction in (-1.0, 1.0):
            plus = (1.0 / (1.0 + np.exp(-direction * (sample + step)))) ** alpha
            minus = (1.0 / (1.0 + np.exp(-direction * (sample - step)))) ** alpha
            numerical = (plus - minus) / (2.0 * step)
            direct = 1.0 / (1.0 + np.exp(-direction * sample))
            analytic = direction * alpha * direct ** alpha * (1.0 - direct)
            mask = np.abs(analytic) > 1e-7
            fd_errors.append(float(np.max(np.abs(numerical[mask] - analytic[mask]) /
                                                 np.maximum(np.abs(analytic[mask]), 1e-15))))
        positive = alpha * (1.0 / (1.0 + np.exp(-sample))) ** alpha * \
            (1.0 - 1.0 / (1.0 + np.exp(-sample)))
        negative_reflected = alpha * (1.0 / (1.0 + np.exp(sample[::-1]))) ** alpha * \
            (1.0 - 1.0 / (1.0 + np.exp(sample[::-1])))
        reflection.append(float(np.max(np.abs(positive - negative_reflected))))
    require(math.isclose(probes["direction_fd_max_rel_error"], max(fd_errors), rel_tol=0.0, abs_tol=1e-15),
            "E_PROBE_DIRECTION_REPLAY")
    require(math.isclose(probes["direction_reflection_max_abs_error"], max(reflection), rel_tol=0.0, abs_tol=1e-15),
            "E_PROBE_REFLECTION_REPLAY")
    reverse_sig = 1.0 / (1.0 + np.exp(sample))
    reverse_magnitude = 2.0 * reverse_sig ** 2.0 * (1.0 - reverse_sig)
    reverse_signed = -reverse_magnitude
    magnitude_distinction = bool(np.all(reverse_magnitude >= 0.0) and
                                 np.all(reverse_signed <= 0.0) and
                                 np.array_equal(reverse_magnitude, np.abs(reverse_signed)))
    require(probes["production_magnitude_signed_distinction_pass"] is magnitude_distinction,
            "E_PROBE_MAGNITUDE_REPLAY")
    clip_probe = np.asarray([-351.0, -350.0, -349.0])
    clip_z = np.clip(clip_probe, -350.0, 350.0)
    clip_sig = 1.0 / (1.0 + np.exp(-clip_z))
    clip_coordinate = clip_sig ** 0.15
    helper_sig = 1.0 / (1.0 + np.exp(-np.clip(np.asarray([-351.0]), -350.0, 350.0)))
    clip_helper = float((0.15 * helper_sig ** 0.15 * (1.0 - helper_sig))[0])
    clip_mismatch = bool(clip_coordinate[1] - clip_coordinate[0] == 0.0 and clip_helper > 0.0)
    require(probes["fit_clip_outside_derivative_mismatch_observed"] is clip_mismatch,
            "E_PROBE_CLIP_REPLAY")
    eager_overflow = False
    try:
        with np.errstate(over="raise", invalid="raise"):
            eager_z = np.asarray([-1000.0, 1000.0])
            np.where(eager_z >= 0, 1.0 / (1.0 + np.exp(-eager_z)),
                     np.exp(eager_z) / (1.0 + np.exp(eager_z)))
    except FloatingPointError:
        eager_overflow = True
    require(probes["production_eager_overflow_observed"] is eager_overflow,
            "E_PROBE_EAGER_OVERFLOW_REPLAY")


def validate_provenance(prov: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    require(set(prov) == {"schema_version", "baseline_commit", "generator_identity", "raw_input", "source_code",
            "preprocessing", "processed_input", "optimizer_contract", "runtime_input_identity",
            "semantic_sha256"}, "E_PROV_TOPLEVEL_SCHEMA")
    require(prov["schema_version"] == "phase066-step77-fit-input-provenance-v1", "E_PROV_SCHEMA")
    require(prov["baseline_commit"] == BASELINE, "E_BASELINE")
    require_keys(prov["generator_identity"], "path raw_sha256", "E_GENERATOR_SCHEMA")
    require(prov["generator_identity"] == {"path": BUILDER_PATH,
            "raw_sha256": sha256((ROOT / BUILDER_PATH).read_bytes())}, "E_GENERATOR_BINDING")
    raw = prov["raw_input"]
    require_keys(raw, "bounded_dataset_claim bytes capacity_basis column_units columns data_rows "
                 "git_blob_sha1 ground_not_found lines path raw_sha256 source_declaration_path "
                 "source_declared_protocol source_declared_specimen source_kind "
                 "specimen_protocol_status", "E_RAW_SCHEMA")
    require_keys(raw["column_units"], "Q_mAh V_vs_Li", "E_RAW_UNIT_SCHEMA")
    path = RAW_PATH
    require(raw["path"] == path, "E_RAW_PATH")
    observed = git("cat-file", "blob", f"{BASELINE}:{path}")
    require(raw["git_blob_sha1"] == git("rev-parse", f"{BASELINE}:{path}").decode().strip(), "E_RAW_BLOB")
    require(raw["raw_sha256"] == sha256(observed), "E_RAW_HASH")
    require(raw["raw_sha256"] == EXPECTED_RAW_SHA256, "E_RAW_PIN")
    require(raw["bytes"] == len(observed), "E_RAW_BYTES")
    require(raw["columns"] == ["V_vs_Li", "Q_mAh"], "E_COLUMNS")
    require(raw["column_units"] == {"V_vs_Li": "V versus Li/Li+", "Q_mAh": "mAh"},
            "E_COLUMN_UNITS")
    require(raw["lines"] == 16736, "E_RAW_LINES")
    require(raw["data_rows"] == 16735, "E_ROWS")
    require(raw["specimen_protocol_status"] ==
            "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND", "E_PROTOCOL_CEILING")
    require(raw["source_declared_specimen"] == "graphite+Si blend half-cell", "E_DECLARED_SPECIMEN")
    require(raw["source_declared_protocol"] ==
            "pOCV, C/50, room temperature approximately 25 C", "E_DECLARED_PROTOCOL")
    require(raw["source_declaration_path"] == SOURCES_PATH, "E_DECLARATION_PATH")
    require(raw["capacity_basis"] == "absolute_mAh_not_mass_normalized", "E_BASIS")
    require(raw["source_kind"] ==
            "repository-derived CSV consumed by Direct14; not original experimental parquet", "E_SOURCE_KIND")
    require(raw["ground_not_found"] == [
        "exact original Zenodo parquet key and checksum",
        "specimen UUID and composition binding for sigr.csv",
        "extraction script-to-parquet cryptographic binding",
    ], "E_RAW_GROUND")
    require(raw["bounded_dataset_claim"] ==
            "SINTEF/EU IntelLiGent Zenodo 20086298, CC-BY-4.0, half-cell versus Li; exact blend protocol unbound",
            "E_RAW_CLAIM_CEILING")
    expected_source_paths = [
        SOURCES_PATH,
        DRIVER_PATH,
        PREPROCESS_PATH,
        ENSEMBLE_PATH,
        SEED_PATH,
        STORED_PATH,
        PARAMS_PATH,
        RELEASE_PATH,
    ]
    semantic_anchors = {
        SOURCES_PATH: [b"Zenodo record **20086298**", b"`sigr.csv`", b"Q_mAh ="],
        DRIVER_PATH: [b"_rng = np.random.default_rng(23)",
                                   b"least_squares(lambda q: f(q) - Dx, st, bounds=(lb, ub), max_nfev=nfev)",
                                   b'("C_skew", dirC, "skew-logistic", {"graphite": 7, "silicon": 7, "blend": 14}'],
        PREPROCESS_PATH: [b"Vm = isotonic_regression(Vu, increasing=True).x",
                                   b"grid = np.arange(vlo, vhi + 0.5 * dv, dv)",
                                   b"return Q * (a / w) * s ** a * (1 - s)"],
        ENSEMBLE_PATH: [b"def savgol_ensemble(data, ratios):"],
        SEED_PATH: [b"def bounds_and_seed(kern, N, Vx, Dx, useeds):",
                                    b"return [a, b, c[:N]]"],
        RELEASE_PATH: [b"def func_ksi_eq(", b"def func_dxi_eq(",
                       b"return np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)), np.exp(z) / (1.0 + np.exp(z)))"],
    }
    require([record["path"] for record in prov["source_code"]] == expected_source_paths, "E_SOURCE_PATHS")
    for record in prov["source_code"]:
        require_keys(record, "bytes git_blob_sha1 lines path raw_sha256", "E_SOURCE_RECORD_SCHEMA")
        source_raw = git("cat-file", "blob", f"{BASELINE}:{record['path']}")
        require(record["git_blob_sha1"] == git("rev-parse", f"{BASELINE}:{record['path']}").decode().strip(),
                "E_SOURCE_BLOB", record["path"])
        require(record["raw_sha256"] == sha256(source_raw) and record["bytes"] == len(source_raw),
                "E_SOURCE_HASH", record["path"])
        require(record["lines"] == len(source_raw.decode("utf-8").splitlines()), "E_SOURCE_LINES", record["path"])
        for anchor in semantic_anchors.get(record["path"], []):
            require(anchor in source_raw, "E_SOURCE_SEMANTIC_ANCHOR", record["path"])
    pre = prov["preprocessing"]
    require_keys(pre, "grid_step_V savgol_polyorder savgol_ratios steps "
                 "wavelet_or_bdd_dmsmcd_used weighting window_V", "E_PREPROCESS_SCHEMA")
    require(pre["steps"] == [
        "finite rows", "stable ascending Q sort", "unique Q retaining first V",
        "increasing isotonic regression V(Q)", "uniform V grid and right-continuous cumulative Q",
        "forward Q difference divided by dV", "positive finite bins",
        "longest contiguous interval", "absolute Savitzky-Golay direct/reciprocal median ensemble",
    ], "E_PREPROCESS_STEPS")
    require(pre["window_V"] == [0.06, 0.7] and pre["grid_step_V"] == 0.0005, "E_WINDOW")
    require(pre["savgol_ratios"] == [0.01, 0.02, 0.03] and pre["savgol_polyorder"] == 3,
            "E_SAVGOL")
    require(pre["weighting"] == "unit_weight_per_retained_grid_point", "E_WEIGHTING")
    require(pre["wavelet_or_bdd_dmsmcd_used"] is False, "E_PREPROCESS_ROUTE")
    opt = prov["optimizer_contract"]
    require_keys(opt, "bounds bounds_sha256 components free_mask "
                 "historical_resolved_defaults_and_scipy_version initial_vectors_sha256 kernel max_nfev "
                 "objective parameter_order replay_runtime_resolved_defaults restarts_per_strategy "
                 "rng_draws_before_direct14 rng_draws_within_direct14 rng_seed seed_strategies solver "
                 "source_explicit_options start_matrix_sha256", "E_OPTIMIZER_SCHEMA")
    require_keys(opt["bounds"], "Q U alpha bg w", "E_OPT_BOUNDS_SCHEMA")
    require_keys(opt["bounds_sha256"], "lower upper", "E_OPT_BOUND_HASH_SCHEMA")
    require_keys(opt["replay_runtime_resolved_defaults"], "loss method note", "E_REPLAY_DEFAULT_SCHEMA")
    require(opt["kernel"] == "skew-logistic" and opt["components"] == 14, "E_KERNEL")
    require(opt["parameter_order"] == ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
            "E_OPT_PARAMETER_ORDER")
    require(opt["bounds"]["w"] == [0.0001, 0.12], "E_BOUNDS")
    require(opt["bounds"]["alpha"] == [0.15, 8.0], "E_ALPHA_BOUNDS")
    require(opt["objective"] == "source_explicit_unweighted_residual=model(V)-D",
            "E_OBJECTIVE")
    require(opt["solver"] == "scipy.optimize.least_squares", "E_SOLVER")
    require(opt["rng_seed"] == 23 and opt["seed_strategies"] == 3 and opt["restarts_per_strategy"] == 4,
            "E_SEEDS")
    require(opt["max_nfev"] == 6000, "E_NFEV")
    require(opt["rng_draws_before_direct14"] == 1908 and opt["rng_draws_within_direct14"] == 513,
            "E_RNG_ADVANCE")
    require(opt["free_mask"] == "implicit_all_57_parameters_free; no persisted explicit mask", "E_FREE_MASK")
    require(opt["source_explicit_options"] == ["bounds", "max_nfev"], "E_EXPLICIT_OPTIONS")
    require(opt["historical_resolved_defaults_and_scipy_version"] == "GROUND_NOT_FOUND", "E_HISTORICAL_DEFAULTS")
    require(opt["replay_runtime_resolved_defaults"]["loss"] == "linear" and
            opt["replay_runtime_resolved_defaults"]["method"] == "trf", "E_REPLAY_DEFAULTS")
    require(opt["replay_runtime_resolved_defaults"]["note"] ==
            "observed defaults of the recorded replay runtimes; not historical source-pinned values",
            "E_REPLAY_DEFAULT_NOTE")
    Vx, Dx, process_info = independent_preprocess(observed)
    require(array_sha256(Vx) == EXPECTED_V_SHA256 and array_sha256(Dx) == EXPECTED_D_SHA256,
            "E_INDEPENDENT_PREPROCESS")
    processed = prov["processed_input"]
    require_keys(processed, "D_max D_min D_sha256 V_max V_min V_sha256 area_data "
                 "dtype_serialization finite_input_rows grid_points_before_difference "
                 "longest_contiguous_bins points positive_finite_bins unique_Q_rows", "E_PROCESSED_SCHEMA")
    require(processed["points"] == 1280 and processed["V_sha256"] == EXPECTED_V_SHA256 and
            processed["D_sha256"] == EXPECTED_D_SHA256, "E_PROCESSED_HASH")
    require(processed == {**process_info, "points": 1280, "V_sha256": EXPECTED_V_SHA256,
            "D_sha256": EXPECTED_D_SHA256,
            "dtype_serialization": "little-endian float64 C-order"}, "E_PROCESSED_VALUES")
    starts, lower_hash, upper_hash = independent_contract(Vx, Dx)
    require(opt["initial_vectors_sha256"] == starts, "E_INITIAL_STATES")
    require(opt["start_matrix_sha256"] == EXPECTED_START_SHA256, "E_START_MATRIX")
    require(opt["bounds_sha256"] == {"lower": EXPECTED_LB_SHA256, "upper": EXPECTED_UB_SHA256}, "E_BOUND_HASH")
    require(lower_hash == EXPECTED_LB_SHA256 and upper_hash == EXPECTED_UB_SHA256, "E_INDEPENDENT_BOUND")
    require(opt["bounds"]["U"] == [float(Vx.min()), float(Vx.max())], "E_U_BOUNDS")
    require(opt["bounds"]["Q"] == [1e-9, 10.0 * float(np.trapezoid(Dx, Vx))], "E_Q_BOUNDS")
    require(opt["bounds"]["bg"] == [min(0.0, float(Dx.min())), max(float(Dx.max()), 1e-9)], "E_BG_BOUNDS")
    identities = prov["runtime_input_identity"]
    require(set(identities) == {"python3.12", "python3.14"}, "E_RUNTIME_IDENTITY_SET")
    expected_versions = {
        "python3.12": {"python_version": "3.12.10", "numpy_version": "2.3.5",
                       "scipy_version": "1.17.1", "V_sha256": EXPECTED_V_SHA256,
                       "D_sha256": EXPECTED_D_SHA256},
        "python3.14": {"python_version": "3.14.4", "numpy_version": "2.5.2",
                       "scipy_version": "1.17.1", "V_sha256": EXPECTED_V_SHA256,
                       "D_sha256": EXPECTED_D_SHA256},
    }
    for label, identity in identities.items():
        require_keys(identity, "D_sha256 V_sha256 numpy_version python_version scipy_version",
                     "E_RUNTIME_IDENTITY_SCHEMA")
        require(identity["python_version"].startswith(label.removeprefix("python")), "E_IDENTITY_VERSION")
        require(identity["V_sha256"] == EXPECTED_V_SHA256 and identity["D_sha256"] == EXPECTED_D_SHA256,
                "E_IDENTITY_ARRAY")
        require(identity == expected_versions[label], "E_RUNTIME_VERSION_PIN")
    return Vx, Dx


def validate_runtime(run: dict[str, Any], prov: dict[str, Any], Vx: np.ndarray, Dx: np.ndarray) -> None:
    require_keys(run, "D_sha256 V_sha256 actual_optimizer_executed best_trial best_vector "
                 "best_vector_sha256 bounds_sha256 external_process_evidence metrics numpy_version "
                 "optimizer_call_count processed_input python_implementation python_version raw_sha256 "
                 "runtime_label schema_version scipy_version sealed_runtime_record_semantic_sha256 "
                 "sealed_runtime_record_sha256 start_matrix_sha256 successful_call_count trials",
                 "E_RUNTIME_SCHEMA")
    require_keys(run["bounds_sha256"], "lower upper", "E_RUNTIME_BOUNDS_SCHEMA")
    require_keys(run["processed_input"], "D_max D_min V_max V_min area_data finite_input_rows "
                 "grid_points_before_difference longest_contiguous_bins positive_finite_bins unique_Q_rows",
                 "E_RUNTIME_PROCESSED_SCHEMA")
    require_keys(run["metrics"], "BIC R2 area_abs_error area_data area_model bg cost npar peakRMSE "
                 "prediction_sha256 rss valleyRMSE", "E_RUNTIME_METRIC_SCHEMA")
    require_keys(run["external_process_evidence"], "argv collector_verified_disposable_temp_input cwd "
                 "exit_code sealed_result_record_available stderr_sha256 stdout_sha256 "
                 "temporary_input_cleanup", "E_PROCESS_EVIDENCE_SCHEMA")
    require(run["runtime_label"] in {"python3.12", "python3.14"}, "E_RUNTIME_LABEL")
    require(run["python_version"].startswith(run["runtime_label"].removeprefix("python")), "E_RUNTIME_VERSION")
    for field in ("sealed_runtime_record_sha256", "sealed_runtime_record_semantic_sha256"):
        require(len(run[field]) == 64 and all(char in "0123456789abcdef" for char in run[field]),
                "E_RUNTIME_SEAL", field)
    require(run["sealed_runtime_record_sha256"] == EXPECTED_RUNTIME_SEALS[run["runtime_label"]]["raw"] and
            run["sealed_runtime_record_semantic_sha256"] ==
            EXPECTED_RUNTIME_SEALS[run["runtime_label"]]["semantic"], "E_RUNTIME_SEAL_PIN")
    sealed = {key: value for key, value in run.items()
              if key not in {"sealed_runtime_record_sha256", "sealed_runtime_record_semantic_sha256",
                             "external_process_evidence"}}
    sealed["semantic_sha256"] = run["sealed_runtime_record_semantic_sha256"]
    require(semantic_hash(sealed) == run["sealed_runtime_record_semantic_sha256"],
            "E_RUNTIME_SEMANTIC_SEAL_REPLAY")
    require(sha256(canonical_bytes(sealed)) == run["sealed_runtime_record_sha256"],
            "E_RUNTIME_RAW_SEAL_REPLAY")
    process = run["external_process_evidence"]
    require(process["collector_verified_disposable_temp_input"] is True and
            process["sealed_result_record_available"] is True, "E_PROCESS_RESULT_SEAL")
    require(all(str(process[key]).startswith("GROUND_NOT_FOUND") for key in
                ("argv", "cwd", "exit_code", "stdout_sha256", "stderr_sha256")),
            "E_PROCESS_CAPTURE_CEILING")
    require(process["temporary_input_cleanup"] ==
            "SCHEDULED_AFTER_PUSH_BEFORE_STEP77_PERSISTENCE_VALIDATION",
            "E_PROCESS_CLEANUP_STATE")
    require(run["actual_optimizer_executed"] is True, "E_ACTUAL_FIT")
    require(run["optimizer_call_count"] == 12, "E_OPTIMIZER_CALLS")
    require(run["raw_sha256"] == prov["raw_input"]["raw_sha256"], "E_RUNTIME_RAW")
    require(run["V_sha256"] == prov["processed_input"]["V_sha256"], "E_RUNTIME_V")
    require(run["D_sha256"] == prov["processed_input"]["D_sha256"], "E_RUNTIME_D")
    require(run["processed_input"] == {key: prov["processed_input"][key] for key in
            ("D_max", "D_min", "V_max", "V_min", "area_data", "finite_input_rows",
             "grid_points_before_difference", "longest_contiguous_bins",
             "positive_finite_bins", "unique_Q_rows")}, "E_RUNTIME_PROCESSED_BINDING")
    identity = prov["runtime_input_identity"][run["runtime_label"]]
    require({key: run[key] for key in ("python_version", "numpy_version", "scipy_version",
                                      "V_sha256", "D_sha256")} == identity,
            "E_RUNTIME_INPUT_IDENTITY_BINDING")
    require(len(run["trials"]) == 12, "E_TRIALS")
    require(run["best_trial"] in range(12), "E_BEST_TRIAL")
    require(len(run["best_vector"]) == 57, "E_VECTOR_LENGTH")
    require(run["metrics"]["npar"] == 57, "E_NPAR")
    require(run["metrics"]["R2"] >= 0.9995, "E_R2")
    require(run["metrics"]["area_abs_error"] <= 5.0e-4, "E_AREA")
    expected_starts = prov["optimizer_contract"]["initial_vectors_sha256"]
    lower = np.asarray([*([float(Vx.min())] * 14), *([0.0001] * 14), *([1e-9] * 14),
                        *([0.15] * 14), min(0.0, float(Dx.min()))])
    upper = np.asarray([*([float(Vx.max())] * 14), *([0.12] * 14),
                        *([10.0 * float(np.trapezoid(Dx, Vx))] * 14), *([8.0] * 14),
                        max(float(Dx.max()), 1e-9)])
    for index, trial in enumerate(run["trials"]):
        require_keys(trial, "active_mask cost index nfev njev optimality restart returned_vector "
                     "returned_vector_sha256 start_sha256 status strategy success", "E_TRIAL_SCHEMA")
        require(trial["index"] == index and trial["strategy"] == index // 4 and
                trial["restart"] == index % 4, "E_TRIAL_INDEX")
        require(trial["start_sha256"] == expected_starts[index], "E_TRIAL_START")
        returned = np.asarray(trial["returned_vector"], float)
        require(len(returned) == 57 and np.isfinite(returned).all(), "E_TRIAL_VECTOR")
        require(array_sha256(returned) == trial["returned_vector_sha256"], "E_TRIAL_VECTOR_HASH")
        require(np.all(returned >= lower - 1e-12) and np.all(returned <= upper + 1e-12), "E_TRIAL_BOUND")
        require(len(trial["active_mask"]) == 57 and trial["nfev"] > 0 and math.isfinite(trial["cost"]),
                "E_TRIAL_DIAGNOSTIC")
        require(type(trial["success"]) is bool and type(trial["status"]) is int and
                trial["status"] in {-1, 0, 1, 2, 3, 4}, "E_TRIAL_STATUS_TYPE")
        require((trial["status"] > 0) is trial["success"], "E_TRIAL_STATUS_SUCCESS")
        require(type(trial["nfev"]) is int and 1 <= trial["nfev"] <= 6000 and
                (trial["njev"] is None or (type(trial["njev"]) is int and trial["njev"] > 0)),
                "E_TRIAL_EVALUATION_COUNT")
        require(type(trial["optimality"]) is float and math.isfinite(trial["optimality"]) and
                trial["optimality"] >= 0.0, "E_TRIAL_OPTIMALITY_TYPE")
        require(all(type(item) is int and item in {-1, 0, 1} for item in trial["active_mask"]),
                "E_TRIAL_ACTIVE_MASK")
        replay_cost = independent_metrics(Vx, Dx, returned)["cost"]
        require(math.isclose(replay_cost, trial["cost"], rel_tol=2e-12, abs_tol=2e-12),
                "E_TRIAL_COST_REPLAY", f"{run['runtime_label']}:{index}")
    require(run["successful_call_count"] == sum(1 for trial in run["trials"] if trial["success"]),
            "E_SUCCESS_COUNT")
    require(run["successful_call_count"] >= 1, "E_NO_CONVERGED_TRIAL")
    observed = independent_metrics(Vx, Dx, np.asarray(run["best_vector"], float))
    for key in ("rss", "cost", "R2", "BIC", "peakRMSE", "valleyRMSE",
                "area_model", "area_data", "area_abs_error", "bg"):
        require(math.isclose(observed[key], run["metrics"][key], rel_tol=2e-12, abs_tol=2e-12),
                "E_RUNTIME_METRIC_REPLAY", f"{run['runtime_label']}:{key}")
    require(observed["prediction_sha256"] == run["metrics"]["prediction_sha256"],
            "E_RUNTIME_PREDICTION", run["runtime_label"])
    best = min(range(12), key=lambda index: run["trials"][index]["cost"])
    require(best == run["best_trial"], "E_BEST_SELECTION")
    require(run["best_vector"] == run["trials"][best]["returned_vector"], "E_BEST_VECTOR_BINDING")
    require(array_sha256(np.asarray(run["best_vector"], float)) == run["best_vector_sha256"], "E_BEST_VECTOR_HASH")


def validate_fit(fit: dict[str, Any], prov: dict[str, Any], Vx: np.ndarray, Dx: np.ndarray) -> None:
    require(set(fit) == {"schema_version", "baseline_commit", "generator_identity", "gate", "status",
            "mathematical_rederivation", "runtime_reproductions", "stored_evidence",
            "comparison", "optimizer_execution_complete", "selected_trial_converged",
            "runtime_success", "scientific_validity", "authority_ceiling", "semantic_sha256"},
            "E_FIT_TOPLEVEL_SCHEMA")
    require(fit["schema_version"] == "phase066-step77-direct14-fit-reproduction-v1", "E_FIT_SCHEMA")
    require(fit["baseline_commit"] == BASELINE and fit["gate"] == GATE, "E_FIT_IDENTITY")
    require(fit["generator_identity"] == prov["generator_identity"], "E_CROSS_GENERATOR_BINDING")
    validate_math(fit)
    runs = fit["runtime_reproductions"]
    require([r["runtime_label"] for r in runs] == ["python3.12", "python3.14"], "E_RUNTIME_SET")
    for run in runs:
        validate_runtime(run, prov, Vx, Dx)
    stored = fit["stored_evidence"]
    require_keys(stored, "full_precision_stored_curve original_full_precision_optimizer_state "
                 "original_optimizer_diagnostics_and_environment parameter_vector_8dp reported_metrics "
                 "source_git_blob_sha1 source_path stored_vector_self_evaluation transition_only_path",
                 "E_STORED_SCHEMA")
    require_keys(stored["reported_metrics"], "BIC R2 area_data area_model bg npar peakRMSE valleyRMSE",
                 "E_STORED_REPORTED_SCHEMA")
    require_keys(stored["stored_vector_self_evaluation"],
                 "BIC R2 area_abs_error area_data area_model bg cost npar peakRMSE prediction_sha256 "
                 "rss valleyRMSE", "E_STORED_SELF_SCHEMA")
    require(stored["source_path"] ==
            "Claude/results/comp_v26_data/out_versions/summary_versions.json", "E_STORED_PATH")
    require(len(stored["parameter_vector_8dp"]) == 57, "E_STORED_VECTOR")
    baseline_stored = json.loads(git("cat-file", "blob", f"{BASELINE}:{STORED_PATH}").decode("utf-8"))["C_skew"]["blend"]
    require(stored["parameter_vector_8dp"] == baseline_stored["params"], "E_STORED_VECTOR_BINDING")
    require(stored["original_full_precision_optimizer_state"] == "GROUND_NOT_FOUND", "E_ORIGINAL_STATE")
    require(stored["original_optimizer_diagnostics_and_environment"] == "GROUND_NOT_FOUND",
            "E_ORIGINAL_DIAGNOSTICS")
    require(stored["full_precision_stored_curve"] ==
            "GROUND_NOT_FOUND; only rasterized PNG retained", "E_STORED_CURVE_CEILING")
    require(stored["transition_only_path"] == PARAMS_PATH, "E_TRANSITION_PATH")
    require(stored["source_git_blob_sha1"] ==
            git("rev-parse", f"{BASELINE}:{STORED_PATH}").decode().strip(), "E_STORED_BLOB")
    require(stored["reported_metrics"] == {
        "BIC": -4760.7, "R2": 0.99965, "area_data": 3.4451,
        "area_model": 3.4452, "bg": 0.516912, "npar": 57,
        "peakRMSE": 0.459, "valleyRMSE": 0.074,
    }, "E_STORED_METRICS")
    require(stored["reported_metrics"] == {key: baseline_stored[key] for key in
            ("BIC", "R2", "area_data", "area_model", "bg", "npar", "peakRMSE", "valleyRMSE")},
            "E_STORED_METRIC_BINDING")
    stored_vector = np.asarray(stored["parameter_vector_8dp"], float)
    stored_replay = independent_metrics(Vx, Dx, stored_vector)
    for key in ("rss", "cost", "R2", "BIC", "peakRMSE", "valleyRMSE",
                "area_model", "area_data", "area_abs_error", "bg"):
        require(math.isclose(stored["stored_vector_self_evaluation"][key], stored_replay[key],
                             rel_tol=2e-12, abs_tol=2e-12), "E_STORED_SELF_REPLAY", key)
    require(stored["stored_vector_self_evaluation"]["prediction_sha256"] ==
            stored_replay["prediction_sha256"], "E_STORED_PREDICTION")
    cmp = fit["comparison"]
    require_keys(cmp, "cross_runtime_curve_max_abs interpretation ordered_parameter_exact_reproduction "
                 "ordered_parameter_max_abs predeclared_tolerances runtime_cost_relative_to_stored "
                 "runtime_curve_agreement_pass runtime_numerical_agreement_pass "
                 "runtime_vs_stored_curve_rmse stored_vector_self_evaluation_pass", "E_COMPARISON_SCHEMA")
    require_keys(cmp["predeclared_tolerances"], "ordered_parameter_max_abs runtime_R2_floor "
                 "runtime_curve_max_abs runtime_vs_stored_cost_relative runtime_vs_stored_curve_rmse "
                 "stored_metric_rounding", "E_TOLERANCE_SCHEMA")
    require_keys(cmp["predeclared_tolerances"]["stored_metric_rounding"], "BIC R2 area bg rmse",
                 "E_ROUNDING_TOLERANCE_SCHEMA")
    for field in ("ordered_parameter_max_abs", "runtime_cost_relative_to_stored",
                  "runtime_vs_stored_curve_rmse"):
        require_keys(cmp[field], "python3.12 python3.14", "E_RUNTIME_COMPARISON_SCHEMA")
    require(cmp["predeclared_tolerances"]["stored_metric_rounding"] == {
        "BIC": 0.05, "R2": 5e-06, "area": 5e-05, "bg": 5e-07, "rmse": 0.0005,
    }, "E_TOLERANCE")
    require(cmp["interpretation"] ==
            "ordered parameter equality is stricter than equivalent in-sample curve reproduction and is reported separately",
            "E_COMPARISON_INTERPRETATION")
    tolerances = cmp["predeclared_tolerances"]
    require(tolerances == {
        "ordered_parameter_max_abs": 5e-08,
        "runtime_R2_floor": 0.9995,
        "runtime_curve_max_abs": 2e-05,
        "runtime_vs_stored_cost_relative": 0.001,
        "runtime_vs_stored_curve_rmse": 0.002,
        "stored_metric_rounding": {"BIC": 0.05, "R2": 5e-06, "area": 5e-05,
                                   "bg": 5e-07, "rmse": 0.0005},
    }, "E_ALL_TOLERANCES")
    rounded_pass = (
        round(stored_replay["R2"], 5) == stored["reported_metrics"]["R2"] and
        round(stored_replay["BIC"], 1) == stored["reported_metrics"]["BIC"] and
        round(stored_replay["peakRMSE"], 3) == stored["reported_metrics"]["peakRMSE"] and
        round(stored_replay["valleyRMSE"], 3) == stored["reported_metrics"]["valleyRMSE"] and
        round(stored_replay["area_model"], 4) == stored["reported_metrics"]["area_model"] and
        round(stored_replay["area_data"], 4) == stored["reported_metrics"]["area_data"] and
        round(stored_replay["bg"], 6) == stored["reported_metrics"]["bg"]
    )
    vectors = {run["runtime_label"]: np.asarray(run["best_vector"], float) for run in runs}
    predictions = {label: independent_model(Vx, vector) for label, vector in vectors.items()}
    stored_prediction = independent_model(Vx, stored_vector)
    cross_curve = float(np.max(np.abs(predictions["python3.12"] - predictions["python3.14"])))
    stored_rmse = {label: float(np.sqrt(np.mean((prediction - stored_prediction) ** 2)))
                   for label, prediction in predictions.items()}
    ordered = {label: float(np.max(np.abs(vector - stored_vector))) for label, vector in vectors.items()}
    relative_cost = {run["runtime_label"]: float(run["metrics"]["cost"] / stored_replay["cost"] - 1.0)
                     for run in runs}
    science_pass = all(run["metrics"]["R2"] >= tolerances["runtime_R2_floor"] and
                       run["metrics"]["cost"] <= stored_replay["cost"] *
                       (1 + tolerances["runtime_vs_stored_cost_relative"]) for run in runs)
    curve_pass = cross_curve <= tolerances["runtime_curve_max_abs"] and \
        max(stored_rmse.values()) <= tolerances["runtime_vs_stored_curve_rmse"]
    exact_pass = max(ordered.values()) <= tolerances["ordered_parameter_max_abs"]
    require(cmp["stored_vector_self_evaluation_pass"] is rounded_pass is True, "E_STORED_SELF_EVAL")
    require(cmp["runtime_numerical_agreement_pass"] is science_pass is True, "E_RUNTIME_SCIENCE")
    require(cmp["runtime_curve_agreement_pass"] is curve_pass is True, "E_RUNTIME_CURVE")
    require(cmp["ordered_parameter_exact_reproduction"] is exact_pass, "E_VECTOR_VERDICT")
    require(cmp["ordered_parameter_max_abs"] == ordered, "E_ORDERED_DISTANCE")
    require(math.isclose(cmp["cross_runtime_curve_max_abs"], cross_curve, rel_tol=2e-12, abs_tol=2e-12),
            "E_CROSS_CURVE")
    for label in vectors:
        require(math.isclose(cmp["runtime_vs_stored_curve_rmse"][label], stored_rmse[label],
                             rel_tol=2e-12, abs_tol=2e-12), "E_STORED_CURVE_RMSE", label)
        require(math.isclose(cmp["runtime_cost_relative_to_stored"][label], relative_cost[label],
                             rel_tol=2e-12, abs_tol=2e-12), "E_RELATIVE_COST", label)
    selected_converged = all(run["trials"][run["best_trial"]]["success"] for run in runs)
    require(fit["status"] ==
            "NUMERICAL_CURVE_REPRODUCED_FROM_REPOSITORY_DERIVED_CSV; SELECTED_TRIAL_NONCONVERGED",
            "E_FIT_STATUS")
    require(fit["optimizer_execution_complete"] is True, "E_EXECUTION_COMPLETE")
    require(fit["selected_trial_converged"] is selected_converged is False,
            "E_SELECTED_TRIAL_CONVERGENCE")
    require(fit["runtime_success"] is selected_converged is False, "E_RUNTIME_SUCCESS")
    require(fit["scientific_validity"] ==
            "bounded to in-sample numerical replay of repository-derived CSV", "E_SCIENCE_CEILING")
    require(fit["authority_ceiling"] == {
        "exact_historical_optimizer_state_reconstruction": False,
        "external_scientific_validation": False,
        "material_assignment_authority": False,
        "parameter_identifiability_authority": False,
        "phase_identification_authority": False,
    }, "E_AUTHORITY")


def validate_documents() -> None:
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    require(GATE in result, "E_RESULT_GATE")
    require("GROUND_NOT_FOUND" in result, "E_RESULT_GROUND")
    require("Python 3.12" in result and "Python 3.14" in result, "E_RESULT_RUNTIMES")
    for token in ("success=false", "status=0", "runtime_success=false",
                  "1.3322676295501878e-15", "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND"):
        require(token in result, "E_RESULT_SEMANTIC_BINDING", token)
    for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH):
        text = (ROOT / path).read_text(encoding="utf-8")
        require("Step 77" in text and GATE in text and "runtime_success=false" in text and
                "Step 78" in text and "PASS_P066_STEP77_PERSISTENCE" in text,
                "E_CONTROL_DOC", path)


def validate_source_text(path: str, source: str) -> None:
    expected_imports = {
        BUILDER_PATH: [
            "from __future__ import annotations", "import argparse", "import csv", "import hashlib",
            "import io", "import json", "import math", "import os", "import platform",
            "import subprocess", "import sys", "import tempfile", "from pathlib import Path",
            "from typing import Any", "import numpy as np",
            "from scipy import __version__ as scipy_version",
            "from scipy.optimize import isotonic_regression, least_squares",
            "from scipy.signal import find_peaks, savgol_filter",
        ],
        VALIDATOR_PATH: [
            "from __future__ import annotations", "import argparse", "import ast", "import csv",
            "import hashlib", "import io", "import json", "import math", "import subprocess",
            "import sys", "import tempfile", "from pathlib import Path", "from typing import Any",
            "import numpy as np", "from scipy.optimize import isotonic_regression",
            "from scipy.signal import find_peaks, savgol_filter",
        ],
    }
    expected_processes = {
        BUILDER_PATH: [
            "subprocess.run(['git', 'cat-file', 'blob', f'{BASELINE}:{path}'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)",
            "subprocess.run(['git', 'rev-parse', f'{BASELINE}:{path}'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)",
        ],
        VALIDATOR_PATH: [
            "subprocess.run(['git', *args], cwd=ROOT, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)",
            "subprocess.run(['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)",
        ],
    }
    expected_mutations = {BUILDER_PATH: [
        "temporary.write_bytes(canonical_bytes(add_semantic(value)))",
        "os.replace(temporary, path)", "first_backup_tmp.write_bytes(first_backup)",
        "second_backup_tmp.write_bytes(second_backup)", "first_tmp.write_bytes(first_bytes)",
        "second_tmp.write_bytes(second_bytes)", "os.replace(first_tmp, first_path)",
        "os.replace(second_tmp, second_path)", "first_path.unlink()", "second_path.unlink()",
        "os.replace(first_backup_tmp, first_path)", "os.replace(second_backup_tmp, second_path)",
        "first_tmp.unlink()", "second_tmp.unlink()", "first_backup_tmp.unlink()",
        "second_backup_tmp.unlink()",
    ], VALIDATOR_PATH: []}
    tree = ast.parse(source)
    imports = [ast.unparse(node) for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    require(imports == expected_imports[path], "E_SOURCE_IMPORT_ALLOWLIST", f"{path}:{imports}")
    mutations: list[str] = []
    processes: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(node.func.id not in {"eval", "exec", "compile", "__import__", "input", "open",
                                         "getattr", "vars", "globals", "locals"},
                    "E_SOURCE_DYNAMIC_CALL", f"{path}:{node.func.id}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Subscript):
            require(False, "E_SOURCE_SUBSCRIPT_CALL", f"{path}:{ast.unparse(node.func)}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            require(node.func.attr not in {"system", "popen", "Popen", "call", "check_call",
                                           "check_output", "urlopen", "request", "connect", "copy",
                                           "copy2", "copyfile", "move", "rmtree", "write_text", "touch",
                                           "mkdir", "rmdir", "rename", "remove", "open"},
                    "E_SOURCE_UNDECLARED_EFFECT", f"{path}:{node.func.attr}")
            if node.func.attr in {"write_bytes", "unlink"}:
                mutations.append(ast.unparse(node))
            if node.func.attr == "replace" and isinstance(node.func.value, ast.Name) and \
                    node.func.value.id == "os":
                mutations.append(ast.unparse(node))
            if node.func.attr == "run":
                processes.append(ast.unparse(node))
    require(sorted(processes) == sorted(expected_processes[path]),
            "E_SOURCE_PROCESS_ALLOWLIST", f"{path}:{processes}")
    require(sorted(mutations) == sorted(expected_mutations[path]),
            "E_SOURCE_MUTATION_ALLOWLIST", f"{path}:{mutations}")


def validate_source_policy() -> None:
    for path in (BUILDER_PATH, VALIDATOR_PATH):
        validate_source_text(path, (ROOT / path).read_text(encoding="utf-8"))


def run_source_negative_controls() -> int:
    builder = (ROOT / BUILDER_PATH).read_text(encoding="utf-8")
    attacks = [
        "\ngetattr(os, 'system')('echo forbidden')\n",
        "\nsubprocess.run(['git', 'push'], shell=False, check=False)\n",
        "\n(ROOT / 'forbidden').write_text('x')\n",
        "\nimport socket\n",
        "\nvars(os)['system']('echo forbidden')\n",
        "\nPath('forbidden').open('w')\n",
        "\n(ROOT / 'forbidden').write_bytes(b'x')\n",
    ]
    for attack in attacks:
        try:
            validate_source_text(BUILDER_PATH, builder + attack)
        except ValidationFailure:
            continue
        raise ValidationFailure("E_SOURCE_NEGATIVE_CONTROL", attack.strip())
    return len(attacks)


def run_negative_controls(fit: dict[str, Any], prov: dict[str, Any]) -> int:
    tests: list[tuple[str, Any]] = []
    def rejected(name: str, edit: Any) -> None:
        f = json.loads(json.dumps(fit)); p = json.loads(json.dumps(prov))
        edit(f, p)
        try:
            Vx, Dx = validate_provenance(p); validate_fit(f, p, Vx, Dx)
        except (ValidationFailure, KeyError, TypeError):
            tests.append((name, True)); return
        tests.append((name, False))
    rejected("derivative_sign", lambda f, p: f["mathematical_rederivation"]["probes"].__setitem__("positive_profile", False))
    rejected("normalization", lambda f, p: f["mathematical_rederivation"]["probes"].__setitem__("normalization_max_abs_error", 1e-2))
    rejected("parameter_order", lambda f, p: f["mathematical_rederivation"].__setitem__("parameter_order", ["w", "U"]))
    rejected("data_hash", lambda f, p: p["raw_input"].__setitem__("raw_sha256", "0" * 64))
    rejected("bound", lambda f, p: p["optimizer_contract"]["bounds"].__setitem__("w", [0.0, 0.12]))
    rejected("objective", lambda f, p: p["optimizer_contract"].__setitem__("objective", "success text"))
    rejected("synthetic_as_raw", lambda f, p: p["raw_input"].__setitem__("source_kind", "synthetic raw"))
    rejected("failed_fit_as_reproduced", lambda f, p: f.__setitem__("runtime_success", True))
    rejected("fabricated_original_state", lambda f, p: f["stored_evidence"].__setitem__(
        "original_full_precision_optimizer_state", "invented"))
    rejected("material_promotion", lambda f, p: f["authority_ceiling"].__setitem__(
        "material_assignment_authority", True))
    rejected("wrong_gate", lambda f, p: f.__setitem__("gate", "PASS_BY_TEXT"))
    rejected("runtime_seal", lambda f, p: f["runtime_reproductions"][0].__setitem__(
        "sealed_runtime_record_sha256", "0" * 64))
    rejected("nested_unknown_key", lambda f, p: p["optimizer_contract"].__setitem__(
        "unreviewed_authority", True))
    rejected("production_clip", lambda f, p: f["mathematical_rederivation"]["probes"].__setitem__(
        "fit_clip_outside_derivative_mismatch_observed", False))
    rejected("fabricated_preprocessing_step", lambda f, p: p["preprocessing"].__setitem__(
        "steps", ["FABRICATED_STEP"]))
    rejected("fabricated_unit", lambda f, p: p["raw_input"]["column_units"].__setitem__("Q_mAh", "kg"))
    rejected("fabricated_runtime_metric", lambda f, p: f["runtime_reproductions"][0]["metrics"].__setitem__(
        "peakRMSE", 999.0))
    rejected("fabricated_trial_diagnostic", lambda f, p: f["runtime_reproductions"][0]["trials"][0].__setitem__(
        "optimality", 999.0))
    try:
        git("push")
    except ValidationFailure:
        tests.append(("arbitrary_git_argv", True))
    else:
        tests.append(("arbitrary_git_argv", False))
    require(all(ok for _, ok in tests), "E_NEGATIVE_CONTROL", repr(tests))
    return len(tests)


def validate_content() -> int:
    fit = strict_load(FIT_PATH)
    prov = strict_load(PROVENANCE_PATH)
    finite_tree(fit); finite_tree(prov)
    Vx, Dx = validate_provenance(prov)
    validate_fit(fit, prov, Vx, Dx)
    validate_documents()
    validate_source_policy()
    return run_negative_controls(fit, prov) + run_source_negative_controls()


def validate_local_protected_refs() -> None:
    require(git("rev-parse", PROTECTED_BRANCH).decode().strip() == PROTECTED_TIP,
            "E_PROTECTED_LOCAL")
    local_main = subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/main"],
                                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=False, check=False)
    require(local_main.returncode == 1, "E_UNEXPECTED_LOCAL_MAIN_REF",
            "local main did not exist at the frozen Step 76 parent and must not be created by Step 77")


def validate_staged() -> None:
    require(git("rev-parse", "HEAD").decode().strip() == EXPECTED_PARENT, "E_PARENT")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "--abbrev-ref", "@{u}").decode().strip() == UPSTREAM, "E_SYMBOLIC_UPSTREAM")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN_URL")
    require(git("diff", "--cached", "--name-only").decode().splitlines() == FINAL_PATHS, "E_STAGED_PATHS")
    require(not git("diff", "--name-only").strip(), "E_UNSTAGED")
    require(not git("ls-files", "--others", "--exclude-standard").strip(), "E_UNTRACKED")
    require(not git("diff", "--cached", "--check").strip(), "E_DIFF_CHECK")
    status = git("diff", "--cached", "--name-status").decode().splitlines()
    expected_status = {BUILDER_PATH: "A", VALIDATOR_PATH: "A", FIT_PATH: "A", PROVENANCE_PATH: "A",
                       RESULT_PATH: "A", PARENT_LEDGER_PATH: "M", ACTIVE_LEDGER_PATH: "M", HANDOVER_PATH: "M"}
    require({line.split("\t", 1)[1]: line.split("\t", 1)[0] for line in status} == expected_status,
            "E_STAGED_STATUS")
    require(git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP,
            "E_PROTECTED_TRACKING")
    require(git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_MAIN_TRACKING")
    require(git("rev-parse", UPSTREAM).decode().strip() == EXPECTED_PARENT, "E_STAGED_UPSTREAM_PARENT")
    active_live = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").decode().split()[0]
    protected_live = git("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}").decode().split()[0]
    main_live = git("ls-remote", "--heads", "origin", "refs/heads/main").decode().split()[0]
    require(active_live == EXPECTED_PARENT, "E_STAGED_ACTIVE_LIVE_PARENT")
    require(protected_live == PROTECTED_TIP and main_live == MAIN_TIP, "E_STAGED_PROTECTED_LIVE")
    validate_local_protected_refs()


def validate_persistence(expected_commit: str) -> None:
    require(len(expected_commit) == 40 and all(c in "0123456789abcdef" for c in expected_commit), "E_COMMIT_ARG")
    head = git("rev-parse", "HEAD").decode().strip()
    require(head == expected_commit, "E_HEAD")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "--abbrev-ref", "@{u}").decode().strip() == UPSTREAM, "E_SYMBOLIC_UPSTREAM")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN_URL")
    require(git("rev-parse", "HEAD^").decode().strip() == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(len(git("rev-list", "--parents", "-n", "1", "HEAD").decode().split()) == 2,
            "E_SINGLE_PARENT_COMMIT")
    require(git("show", "-s", "--format=%s", "HEAD").decode().strip() == EXPECTED_SUBJECT, "E_SUBJECT")
    require(git("rev-parse", UPSTREAM).decode().strip() == head, "E_UPSTREAM")
    live = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").decode().split()[0]
    require(live == head, "E_LIVE_REMOTE")
    protected_live = git("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}").decode().split()[0]
    main_live = git("ls-remote", "--heads", "origin", "refs/heads/main").decode().split()[0]
    require(protected_live == git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP,
            "E_PROTECTED_LIVE")
    require(main_live == git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_MAIN_LIVE")
    validate_local_protected_refs()
    require(not (Path(tempfile.gettempdir()) / "p066_step77_py312.json").exists() and
            not (Path(tempfile.gettempdir()) / "p066_step77_py314.json").exists(),
            "E_RUNTIME_TEMP_NOT_CLEANED")
    require(git("diff", "--name-only", "HEAD^").decode().splitlines() == FINAL_PATHS, "E_COMMITTED_PATHS")
    require(not any(path.startswith("Claude/") for path in git("diff", "--name-only", "HEAD^").decode().splitlines()),
            "E_CLAUDE_DRIFT")
    require(not git("status", "--porcelain").strip(), "E_DIRTY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--persistence")
    args = parser.parse_args()
    negatives = validate_content()
    if args.staged:
        validate_staged()
    if args.persistence:
        validate_persistence(args.persistence)
        print(f"{PERSISTENCE} commit={args.persistence} negative={negatives}/26")
    else:
        print(f"{GATE} negative={negatives}/26")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL_P066_STEP77 {error}", file=sys.stderr)
        raise SystemExit(1)
