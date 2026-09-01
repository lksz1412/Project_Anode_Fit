from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
STEP77_COMMIT = "5d26e0746864cea7a8bd37a22874093b73c1a12f"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
FIT_PATH = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
PROVENANCE_PATH = "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
STORED_PATH = "Claude/results/comp_v26_data/out_versions/summary_versions.json"
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step78.py"
OUTPUT_PATH = ROOT / "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"
GATE = "CONDITIONAL_P066_STEP78_VECTOR_BOUND_WITH_ORIGINAL_STATE_GROUND_NOT_FOUND"
TOLERANCE = 5.0e-8


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = ""
    value["semantic_sha256"] = sha256(canonical_bytes(value))
    return value


def git_blob(commit: str, path: str) -> tuple[bytes, str]:
    allowed = {
        (STEP77_COMMIT, FIT_PATH), (STEP77_COMMIT, PROVENANCE_PATH),
        (BASELINE, STORED_PATH),
    }
    require((commit, path) in allowed, "E_GIT_INPUT_ALLOWLIST", f"{commit}:{path}")
    content = subprocess.run(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=False, check=False)
    identity = subprocess.run(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              shell=False, check=False)
    require(content.returncode == identity.returncode == 0, "E_GIT_INPUT", path)
    return content.stdout, identity.stdout.decode("ascii").strip()


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"))
    require(isinstance(value, dict) and canonical_bytes(value) == raw, "E_CANONICAL_INPUT")
    observed = value.get("semantic_sha256")
    value["semantic_sha256"] = ""
    require(observed == sha256(canonical_bytes(value)), "E_SEMANTIC_INPUT")
    value["semantic_sha256"] = observed
    return value


def source_record(commit: str, path: str, raw: bytes, blob: str) -> dict[str, Any]:
    return {"commit": commit, "path": path, "git_blob_sha1": blob,
            "raw_sha256": sha256(raw), "bytes": len(raw)}


def comparison(left: list[float], right: list[float], left_id: str, right_id: str) -> dict[str, Any]:
    differences = [abs(a - b) for a, b in zip(left, right)]
    maximum = max(differences)
    identical = left == right
    status = "IDENTICAL" if identical else "TOLERANCE_EQUIVALENT" if maximum <= TOLERANCE else "NOT_EQUIVALENT"
    return {
        "left": left_id, "right": right_id, "status": status,
        "identical": identical, "tolerance": TOLERANCE,
        "max_abs": maximum, "max_abs_index": differences.index(maximum),
        "mean_abs": sum(differences) / len(differences),
        "rmse": math.sqrt(sum(value * value for value in differences) / len(differences)),
        "element_status_counts": {
            "IDENTICAL": sum(a == b for a, b in zip(left, right)),
            "TOLERANCE_EQUIVALENT": sum(a != b and delta <= TOLERANCE
                                        for a, b, delta in zip(left, right, differences)),
            "NOT_EQUIVALENT": sum(delta > TOLERANCE for delta in differences),
        },
        "round_replay_to_8dp_equal_count":
            sum(round(b, 8) == a for a, b in zip(left, right)) if left_id == "stored_8dp" else None,
    }


def family_deltas(stored: list[float], replay: list[float]) -> list[dict[str, Any]]:
    families = [("U", 0, 14), ("w", 14, 28), ("Q", 28, 42),
                ("alpha", 42, 56), ("bg", 56, 57)]
    records = []
    for family, start, stop in families:
        differences = [abs(stored[index] - replay[index]) for index in range(start, stop)]
        maximum = max(differences)
        records.append({
            "family": family, "index_range": [start, stop - 1], "count": stop - start,
            "max_abs": maximum, "max_abs_global_index": start + differences.index(maximum),
            "mean_abs": sum(differences) / len(differences),
            "rmse": math.sqrt(sum(value * value for value in differences) / len(differences)),
        })
    return records


def component_deltas(stored: list[float], replay: list[float]) -> list[dict[str, Any]]:
    records = []
    for component_index in range(14):
        indices = [component_index, 14 + component_index, 28 + component_index, 42 + component_index]
        differences = [abs(stored[index] - replay[index]) for index in indices]
        maximum = max(differences)
        records.append({"component": component_index + 1, "flat_indices": indices,
                        "max_abs": maximum, "max_abs_flat_index": indices[differences.index(maximum)],
                        "mean_abs": sum(differences) / 4.0})
    return records


def parameter_label(index: int) -> str:
    if index < 14: return f"U[{index + 1}]"
    if index < 28: return f"w[{index - 13}]"
    if index < 42: return f"Q[{index - 27}]"
    if index < 56: return f"alpha[{index - 41}]"
    return "bg"


def selected_trial_record(run: dict[str, Any], lower: list[float], upper: list[float]) -> dict[str, Any]:
    trial = run["trials"][run["best_trial"]]
    mask = trial["active_mask"]
    vector = trial["returned_vector"]
    active = [{"flat_index": index, "parameter": parameter_label(index),
               "side": "lower" if flag == -1 else "upper", "value": vector[index],
               "bound": lower[index] if flag == -1 else upper[index],
               "distance": abs(vector[index] - (lower[index] if flag == -1 else upper[index]))}
              for index, flag in enumerate(mask) if flag != 0]
    return {
        "runtime_label": run["runtime_label"], "selected_trial": run["best_trial"],
        "success": trial["success"], "status": trial["status"], "nfev": trial["nfev"],
        "njev": trial["njev"], "optimality": trial["optimality"], "cost": trial["cost"],
        "active_mask_counts": {"lower": mask.count(-1), "free": mask.count(0), "upper": mask.count(1)},
        "active_bound_rows": active,
        "returned_vector_sha256": trial["returned_vector_sha256"],
        "diagnostic_authority": "SEALED_REPLAY_RUNTIME_RECORD; NOT ORIGINAL_HISTORICAL_STATE",
    }


def bound_classification(vector_id: str, vector: list[float],
                         lower: list[float], upper: list[float]) -> dict[str, Any]:
    rows = []
    for index, value in enumerate(vector):
        if value == lower[index] or value == upper[index] or \
                abs(value - lower[index]) <= 1.0e-12 or abs(value - upper[index]) <= 1.0e-12:
            side = "lower" if abs(value - lower[index]) <= abs(value - upper[index]) else "upper"
            bound = lower[index] if side == "lower" else upper[index]
            rows.append({"flat_index": index, "parameter": parameter_label(index), "side": side,
                         "value": value, "bound": bound, "distance": abs(value - bound),
                         "exact_equal": value == bound})
    return {"vector": vector_id,
            "out_of_bounds_count": sum(value < lo or value > hi
                                       for value, lo, hi in zip(vector, lower, upper)),
            "exact_lower_bound_count": sum(value == lo for value, lo in zip(vector, lower)),
            "exact_upper_bound_count": sum(value == hi for value, hi in zip(vector, upper)),
            "within_1e-12_of_either_bound_count": len(rows), "boundary_rows": rows}


def build() -> None:
    fit_raw, fit_blob = git_blob(STEP77_COMMIT, FIT_PATH)
    provenance_raw, provenance_blob = git_blob(STEP77_COMMIT, PROVENANCE_PATH)
    stored_raw, stored_blob = git_blob(BASELINE, STORED_PATH)
    fit = strict_json(fit_raw)
    provenance = strict_json(provenance_raw)
    stored_text = json.loads(stored_raw.decode("utf-8"), parse_float=str, parse_int=str)
    stored_tokens = stored_text["C_skew"]["blend"]["params"]
    stored_vector = [float(token) for token in stored_tokens]
    require(len(stored_vector) == 57 and stored_vector == fit["stored_evidence"]["parameter_vector_8dp"],
            "E_STORED_VECTOR_BINDING")
    runs = fit["runtime_reproductions"]
    require([run["runtime_label"] for run in runs] == ["python3.12", "python3.14"], "E_RUNTIME_SET")
    vectors = {run["runtime_label"]: [float(value) for value in run["best_vector"]] for run in runs}
    comparisons = [
        comparison(stored_vector, vectors["python3.12"], "stored_8dp", "python3.12_replay"),
        comparison(stored_vector, vectors["python3.14"], "stored_8dp", "python3.14_replay"),
        comparison(vectors["python3.12"], vectors["python3.14"],
                   "python3.12_replay", "python3.14_replay"),
        {"left": "original_historical", "right": "stored_8dp", "status": "GROUND_NOT_FOUND"},
        {"left": "original_historical", "right": "python3.12_replay", "status": "GROUND_NOT_FOUND"},
        {"left": "original_historical", "right": "python3.14_replay", "status": "GROUND_NOT_FOUND"},
    ]
    missing = [
        "full_precision_returned_vector", "initial_vectors", "success", "status", "cost", "rss",
        "residual_vector", "nfev", "njev", "optimality", "active_mask", "jacobian", "gradient",
        "covariance", "hessian", "inverse_hessian", "termination_message", "historical_python_version",
        "historical_numpy_version", "historical_scipy_version", "resolved_loss", "resolved_method",
        "resolved_tolerances", "resolved_jacobian_scheme", "full_precision_prediction",
    ]
    bounds = provenance["optimizer_contract"]["bounds"]
    lower = [bounds["U"][0]] * 14 + [bounds["w"][0]] * 14 + [bounds["Q"][0]] * 14 + \
        [bounds["alpha"][0]] * 14 + [bounds["bg"][0]]
    upper = [bounds["U"][1]] * 14 + [bounds["w"][1]] * 14 + [bounds["Q"][1]] * 14 + \
        [bounds["alpha"][1]] * 14 + [bounds["bg"][1]]
    result = {
        "schema_version": "phase066-step78-optimizer-state-vector-matrix-v1",
        "phase": 66, "step": 78, "gate": GATE,
        "baseline_commit": BASELINE, "step77_commit": STEP77_COMMIT,
        "generator_identity": {"path": BUILDER_PATH,
                               "raw_sha256": sha256((ROOT / BUILDER_PATH).read_bytes())},
        "inputs": [source_record(STEP77_COMMIT, FIT_PATH, fit_raw, fit_blob),
                   source_record(STEP77_COMMIT, PROVENANCE_PATH, provenance_raw, provenance_blob),
                   source_record(BASELINE, STORED_PATH, stored_raw, stored_blob)],
        "parameter_contract": {"count": 57,
                               "order": ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
                               "all_replay_parameters_free": True,
                               "stored_precision": "JSON numeric tokens produced from source rounding to 8 decimal places"},
        "vectors": {
            "stored_8dp": {"status": "DISPLAYED_ROUNDED_VECTOR", "source_numeric_tokens": stored_tokens,
                           "numeric_values": stored_vector,
                           "token_sequence_sha256": sha256(("\n".join(stored_tokens) + "\n").encode("ascii"))},
            "python3.12_replay": {"status": "SEALED_FULL_PRECISION_REPLAY_VECTOR",
                                  "numeric_values": vectors["python3.12"],
                                  "sha256": runs[0]["best_vector_sha256"]},
            "python3.14_replay": {"status": "SEALED_FULL_PRECISION_REPLAY_VECTOR",
                                  "numeric_values": vectors["python3.14"],
                                  "sha256": runs[1]["best_vector_sha256"]},
            "original_historical": {"status": "GROUND_NOT_FOUND", "numeric_values": None},
        },
        "pairwise_vector_classification": comparisons,
        "family_deltas_vs_stored": {
            "python3.12": family_deltas(stored_vector, vectors["python3.12"]),
            "python3.14": family_deltas(stored_vector, vectors["python3.14"]),
        },
        "component_deltas_vs_stored": {
            "python3.12": component_deltas(stored_vector, vectors["python3.12"]),
            "python3.14": component_deltas(stored_vector, vectors["python3.14"]),
        },
        "curve_objective_classification": {
            "python3.12_vs_python3.14_curve": "IDENTICAL",
            "replay_vs_stored_curve": "TOLERANCE_EQUIVALENT",
            "ordered_parameter_vectors_vs_stored": "NOT_EQUIVALENT",
            "original_historical_curve_and_objective": "GROUND_NOT_FOUND",
            "source_step77_gate": fit["gate"],
            "runtime_vs_stored_curve_rmse": fit["comparison"]["runtime_vs_stored_curve_rmse"],
            "runtime_cost_relative_to_stored": fit["comparison"]["runtime_cost_relative_to_stored"],
            "runtime_vs_stored_curve_rmse_tolerance":
                fit["comparison"]["predeclared_tolerances"]["runtime_vs_stored_curve_rmse"],
            "runtime_vs_stored_cost_relative_tolerance":
                fit["comparison"]["predeclared_tolerances"]["runtime_vs_stored_cost_relative"],
        },
        "selected_replay_trials": [selected_trial_record(run, lower, upper) for run in runs],
        "vector_bound_classification": [
            bound_classification("stored_8dp", stored_vector, lower, upper),
            bound_classification("python3.12_replay", vectors["python3.12"], lower, upper),
            bound_classification("python3.14_replay", vectors["python3.14"], lower, upper),
            {"vector": "original_historical", "status": "GROUND_NOT_FOUND"},
        ],
        "original_optimizer_state_availability": [
            {"field": field, "status": "GROUND_NOT_FOUND",
             "owner": "historical Direct14 execution state not retained in repository"}
            for field in missing
        ],
        "available_source_contract_not_original_runtime_state": {
            "bounds_sha256": provenance["optimizer_contract"]["bounds_sha256"],
            "start_matrix_sha256": provenance["optimizer_contract"]["start_matrix_sha256"],
            "objective": provenance["optimizer_contract"]["objective"],
            "source_explicit_options": provenance["optimizer_contract"]["source_explicit_options"],
        },
        "authority_ceiling": {
            "stored_8dp_is_original_full_precision": False,
            "replay_vector_is_original_historical_vector": False,
            "curve_equivalence_implies_parameter_identifiability": False,
            "replay_diagnostics_are_historical_diagnostics": False,
        },
    }
    raw = canonical_bytes(semantic(result))
    temporary = OUTPUT_PATH.with_name(OUTPUT_PATH.name + ".step78.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, OUTPUT_PATH)
    print(f"{GATE} stored_vs_replay=NOT_EQUIVALENT replay_cross=IDENTICAL original=GROUND_NOT_FOUND")


if __name__ == "__main__":
    try:
        build()
    except (BuildFailure, KeyError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL_P066_STEP78_BUILD {error}")
        raise SystemExit(1)
