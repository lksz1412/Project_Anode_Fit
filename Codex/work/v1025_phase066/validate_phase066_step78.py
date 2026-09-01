from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
STEP77_COMMIT = "5d26e0746864cea7a8bd37a22874093b73c1a12f"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_SUBJECT = "audit(phase066): bind optimizer state vector"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
FIT_PATH = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
PROVENANCE_PATH = "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
STORED_PATH = "Claude/results/comp_v26_data/out_versions/summary_versions.json"
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step78.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step78.py"
MATRIX_PATH = "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_078_OPTIMIZER_VECTOR_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
GATE = "CONDITIONAL_P066_STEP78_VECTOR_BOUND_WITH_ORIGINAL_STATE_GROUND_NOT_FOUND"
PERSISTENCE = "PASS_P066_STEP78_PERSISTENCE"
TOLERANCE = 5.0e-8
FINAL_PATHS = [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, MATRIX_PATH,
               RESULT_PATH, BUILDER_PATH, VALIDATOR_PATH]


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


def pairs_unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_unique,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    require(isinstance(value, dict) and canonical_bytes(value) == raw, "E_CANONICAL_JSON")
    observed = value.get("semantic_sha256")
    clone = dict(value); clone["semantic_sha256"] = ""
    require(observed == sha256(canonical_bytes(clone)), "E_SEMANTIC_JSON")
    return value


def git(*args: str) -> bytes:
    baseline_paths = {STORED_PATH}
    step77_paths = {FIT_PATH, PROVENANCE_PATH}
    exact = {
        ("rev-parse", "HEAD"), ("rev-parse", "HEAD^"), ("rev-parse", UPSTREAM),
        ("rev-parse", "--abbrev-ref", "@{u}"), ("rev-parse", PROTECTED_BRANCH),
        ("rev-parse", f"origin/{PROTECTED_BRANCH}"), ("rev-parse", "origin/main"),
        ("branch", "--show-current"), ("remote", "get-url", "origin"),
        ("diff", "--cached", "--name-only"), ("diff", "--cached", "--name-status"),
        ("diff", "--cached", "--check"), ("diff", "--name-only"),
        ("diff", "--name-only", "HEAD^"), ("ls-files", "--others", "--exclude-standard"),
        ("show", "-s", "--format=%s", "HEAD"), ("status", "--porcelain"),
        ("rev-list", "--parents", "-n", "1", "HEAD"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}"),
        ("ls-remote", "--heads", "origin", "refs/heads/main"),
    }
    read = (len(args) == 3 and args[:2] == ("cat-file", "blob") and
            ((args[2].startswith(STEP77_COMMIT + ":") and args[2][41:] in step77_paths) or
             (args[2].startswith(BASELINE + ":") and args[2][41:] in baseline_paths)))
    identity = (len(args) == 2 and args[0] == "rev-parse" and
                ((args[1].startswith(STEP77_COMMIT + ":") and args[1][41:] in step77_paths) or
                 (args[1].startswith(BASELINE + ":") and args[1][41:] in baseline_paths)))
    require(args in exact or read or identity, "E_GIT_ALLOWLIST", repr(args))
    run = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=False, check=False)
    require(run.returncode == 0, "E_GIT", run.stderr.decode("utf-8", "replace"))
    return run.stdout


def input_record(commit: str, path: str, raw: bytes) -> dict[str, Any]:
    return {"commit": commit, "path": path,
            "git_blob_sha1": git("rev-parse", f"{commit}:{path}").decode().strip(),
            "raw_sha256": sha256(raw), "bytes": len(raw)}


def compare(left: list[float], right: list[float], left_id: str, right_id: str) -> dict[str, Any]:
    delta = [abs(a - b) for a, b in zip(left, right)]
    maximum = max(delta); identical = left == right
    return {"left": left_id, "right": right_id,
            "status": "IDENTICAL" if identical else "TOLERANCE_EQUIVALENT" if maximum <= TOLERANCE else "NOT_EQUIVALENT",
            "identical": identical, "tolerance": TOLERANCE, "max_abs": maximum,
            "max_abs_index": delta.index(maximum), "mean_abs": sum(delta) / len(delta),
            "rmse": math.sqrt(sum(value * value for value in delta) / len(delta)),
            "element_status_counts": {
                "IDENTICAL": sum(a == b for a, b in zip(left, right)),
                "TOLERANCE_EQUIVALENT": sum(a != b and value <= TOLERANCE
                                            for a, b, value in zip(left, right, delta)),
                "NOT_EQUIVALENT": sum(value > TOLERANCE for value in delta)},
            "round_replay_to_8dp_equal_count":
                sum(round(b, 8) == a for a, b in zip(left, right)) if left_id == "stored_8dp" else None}


def families(stored: list[float], replay: list[float]) -> list[dict[str, Any]]:
    result = []
    for name, start, stop in (("U", 0, 14), ("w", 14, 28), ("Q", 28, 42),
                              ("alpha", 42, 56), ("bg", 56, 57)):
        delta = [abs(stored[index] - replay[index]) for index in range(start, stop)]
        maximum = max(delta)
        result.append({"family": name, "index_range": [start, stop - 1], "count": stop - start,
                       "max_abs": maximum, "max_abs_global_index": start + delta.index(maximum),
                       "mean_abs": sum(delta) / len(delta),
                       "rmse": math.sqrt(sum(value * value for value in delta) / len(delta))})
    return result


def components(stored: list[float], replay: list[float]) -> list[dict[str, Any]]:
    result = []
    for component_index in range(14):
        indices = [component_index, 14 + component_index, 28 + component_index, 42 + component_index]
        delta = [abs(stored[index] - replay[index]) for index in indices]; maximum = max(delta)
        result.append({"component": component_index + 1, "flat_indices": indices,
                       "max_abs": maximum, "max_abs_flat_index": indices[delta.index(maximum)],
                       "mean_abs": sum(delta) / 4.0})
    return result


def parameter_label(index: int) -> str:
    if index < 14: return f"U[{index + 1}]"
    if index < 28: return f"w[{index - 13}]"
    if index < 42: return f"Q[{index - 27}]"
    if index < 56: return f"alpha[{index - 41}]"
    return "bg"


def selected(run: dict[str, Any], lower: list[float], upper: list[float]) -> dict[str, Any]:
    trial = run["trials"][run["best_trial"]]; mask = trial["active_mask"]
    vector = trial["returned_vector"]
    active = [{"flat_index": index, "parameter": parameter_label(index),
               "side": "lower" if flag == -1 else "upper", "value": vector[index],
               "bound": lower[index] if flag == -1 else upper[index],
               "distance": abs(vector[index] - (lower[index] if flag == -1 else upper[index]))}
              for index, flag in enumerate(mask) if flag != 0]
    return {"runtime_label": run["runtime_label"], "selected_trial": run["best_trial"],
            "success": trial["success"], "status": trial["status"], "nfev": trial["nfev"],
            "njev": trial["njev"], "optimality": trial["optimality"], "cost": trial["cost"],
            "active_mask_counts": {"lower": mask.count(-1), "free": mask.count(0), "upper": mask.count(1)},
            "active_bound_rows": active,
            "returned_vector_sha256": trial["returned_vector_sha256"],
            "diagnostic_authority": "SEALED_REPLAY_RUNTIME_RECORD; NOT ORIGINAL_HISTORICAL_STATE"}


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


def expected_matrix() -> dict[str, Any]:
    fit_raw = git("cat-file", "blob", f"{STEP77_COMMIT}:{FIT_PATH}")
    prov_raw = git("cat-file", "blob", f"{STEP77_COMMIT}:{PROVENANCE_PATH}")
    stored_raw = git("cat-file", "blob", f"{BASELINE}:{STORED_PATH}")
    fit = strict_json(fit_raw); provenance = strict_json(prov_raw)
    token_tree = json.loads(stored_raw.decode("utf-8"), parse_float=str, parse_int=str)
    tokens = token_tree["C_skew"]["blend"]["params"]
    stored = [float(token) for token in tokens]
    require(stored == fit["stored_evidence"]["parameter_vector_8dp"], "E_STORED_SOURCE")
    runs = fit["runtime_reproductions"]
    vectors = {run["runtime_label"]: [float(value) for value in run["best_vector"]] for run in runs}
    missing = ["full_precision_returned_vector", "initial_vectors", "success", "status", "cost", "rss",
               "residual_vector", "nfev", "njev", "optimality", "active_mask", "jacobian", "gradient",
               "covariance", "hessian", "inverse_hessian", "termination_message", "historical_python_version",
               "historical_numpy_version", "historical_scipy_version", "resolved_loss", "resolved_method",
               "resolved_tolerances", "resolved_jacobian_scheme", "full_precision_prediction"]
    bounds = provenance["optimizer_contract"]["bounds"]
    lower = [bounds["U"][0]] * 14 + [bounds["w"][0]] * 14 + [bounds["Q"][0]] * 14 + \
        [bounds["alpha"][0]] * 14 + [bounds["bg"][0]]
    upper = [bounds["U"][1]] * 14 + [bounds["w"][1]] * 14 + [bounds["Q"][1]] * 14 + \
        [bounds["alpha"][1]] * 14 + [bounds["bg"][1]]
    result = {
        "schema_version": "phase066-step78-optimizer-state-vector-matrix-v1",
        "phase": 66, "step": 78, "gate": GATE, "baseline_commit": BASELINE,
        "step77_commit": STEP77_COMMIT,
        "generator_identity": {"path": BUILDER_PATH,
                               "raw_sha256": sha256((ROOT / BUILDER_PATH).read_bytes())},
        "inputs": [input_record(STEP77_COMMIT, FIT_PATH, fit_raw),
                   input_record(STEP77_COMMIT, PROVENANCE_PATH, prov_raw),
                   input_record(BASELINE, STORED_PATH, stored_raw)],
        "parameter_contract": {"count": 57, "order": ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
                               "all_replay_parameters_free": True,
                               "stored_precision": "JSON numeric tokens produced from source rounding to 8 decimal places"},
        "vectors": {
            "stored_8dp": {"status": "DISPLAYED_ROUNDED_VECTOR", "source_numeric_tokens": tokens,
                           "numeric_values": stored,
                           "token_sequence_sha256": sha256(("\n".join(tokens) + "\n").encode("ascii"))},
            "python3.12_replay": {"status": "SEALED_FULL_PRECISION_REPLAY_VECTOR",
                                  "numeric_values": vectors["python3.12"], "sha256": runs[0]["best_vector_sha256"]},
            "python3.14_replay": {"status": "SEALED_FULL_PRECISION_REPLAY_VECTOR",
                                  "numeric_values": vectors["python3.14"], "sha256": runs[1]["best_vector_sha256"]},
            "original_historical": {"status": "GROUND_NOT_FOUND", "numeric_values": None}},
        "pairwise_vector_classification": [
            compare(stored, vectors["python3.12"], "stored_8dp", "python3.12_replay"),
            compare(stored, vectors["python3.14"], "stored_8dp", "python3.14_replay"),
            compare(vectors["python3.12"], vectors["python3.14"], "python3.12_replay", "python3.14_replay"),
            {"left": "original_historical", "right": "stored_8dp", "status": "GROUND_NOT_FOUND"},
            {"left": "original_historical", "right": "python3.12_replay", "status": "GROUND_NOT_FOUND"},
            {"left": "original_historical", "right": "python3.14_replay", "status": "GROUND_NOT_FOUND"}],
        "family_deltas_vs_stored": {"python3.12": families(stored, vectors["python3.12"]),
                                    "python3.14": families(stored, vectors["python3.14"])},
        "component_deltas_vs_stored": {"python3.12": components(stored, vectors["python3.12"]),
                                       "python3.14": components(stored, vectors["python3.14"])},
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
                fit["comparison"]["predeclared_tolerances"]["runtime_vs_stored_cost_relative"]},
        "selected_replay_trials": [selected(run, lower, upper) for run in runs],
        "vector_bound_classification": [
            bound_classification("stored_8dp", stored, lower, upper),
            bound_classification("python3.12_replay", vectors["python3.12"], lower, upper),
            bound_classification("python3.14_replay", vectors["python3.14"], lower, upper),
            {"vector": "original_historical", "status": "GROUND_NOT_FOUND"}],
        "original_optimizer_state_availability": [
            {"field": field, "status": "GROUND_NOT_FOUND",
             "owner": "historical Direct14 execution state not retained in repository"} for field in missing],
        "available_source_contract_not_original_runtime_state": {
            "bounds_sha256": provenance["optimizer_contract"]["bounds_sha256"],
            "start_matrix_sha256": provenance["optimizer_contract"]["start_matrix_sha256"],
            "objective": provenance["optimizer_contract"]["objective"],
            "source_explicit_options": provenance["optimizer_contract"]["source_explicit_options"]},
        "authority_ceiling": {"stored_8dp_is_original_full_precision": False,
                              "replay_vector_is_original_historical_vector": False,
                              "curve_equivalence_implies_parameter_identifiability": False,
                              "replay_diagnostics_are_historical_diagnostics": False},
        "semantic_sha256": "",
    }
    result["semantic_sha256"] = sha256(canonical_bytes(result))
    return result


def validate_documents() -> None:
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    for token in (GATE, "GROUND_NOT_FOUND", "NOT_EQUIVALENT", "IDENTICAL",
                  "TOLERANCE_EQUIVALENT", "runtime_success=false"):
        require(token in result, "E_RESULT_TOKEN", token)
    for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH):
        text = (ROOT / path).read_text(encoding="utf-8")
        require("Step 78" in text and GATE in text and "Step 79" in text and
                PERSISTENCE in text, "E_CONTROL_DOCUMENT", path)


def validate_source_policy() -> None:
    expected_imports = {
        BUILDER_PATH: ["from __future__ import annotations", "import hashlib", "import json", "import math",
                       "import os", "import subprocess", "from pathlib import Path", "from typing import Any"],
        VALIDATOR_PATH: ["from __future__ import annotations", "import argparse", "import ast", "import hashlib",
                         "import json", "import math", "import subprocess", "from pathlib import Path",
                         "from typing import Any"],
    }
    expected_processes = {
        BUILDER_PATH: [
            "subprocess.run(['git', 'cat-file', 'blob', f'{commit}:{path}'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)",
            "subprocess.run(['git', 'rev-parse', f'{commit}:{path}'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)"],
        VALIDATOR_PATH: [
            "subprocess.run(['git', *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)",
            "subprocess.run(['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)"],
    }
    expected_mutations = {
        BUILDER_PATH: ["temporary.write_bytes(raw)", "os.replace(temporary, OUTPUT_PATH)"],
        VALIDATOR_PATH: [],
    }
    for path in (BUILDER_PATH, VALIDATOR_PATH):
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        imports = [ast.unparse(node) for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        require(imports == expected_imports[path], "E_SOURCE_IMPORTS", path)
        processes: list[str] = []; mutations: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, (ast.Name, ast.Subscript)):
                if isinstance(node.func, ast.Subscript):
                    require(False, "E_SOURCE_SUBSCRIPT_CALL", path)
                require(node.func.id not in {"eval", "exec", "compile", "open", "getattr", "vars",
                                             "globals", "locals", "__import__"}, "E_SOURCE_DYNAMIC", path)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                require(node.func.attr not in {"system", "Popen", "popen", "open", "write_text", "touch",
                                               "mkdir", "rmdir", "rename", "remove", "copy", "copy2",
                                               "copyfile", "move", "rmtree", "urlopen", "connect"},
                        "E_SOURCE_EFFECT", f"{path}:{node.func.attr}")
                if node.func.attr == "run": processes.append(ast.unparse(node))
                if node.func.attr == "write_bytes": mutations.append(ast.unparse(node))
                if node.func.attr == "replace" and isinstance(node.func.value, ast.Name) and \
                        node.func.value.id == "os":
                    mutations.append(ast.unparse(node))
        require(sorted(processes) == sorted(expected_processes[path]), "E_SOURCE_PROCESSES", path)
        require(sorted(mutations) == sorted(expected_mutations[path]), "E_SOURCE_MUTATIONS", path)


def run_negatives(matrix: dict[str, Any]) -> int:
    edits = [
        lambda value: value["vectors"]["stored_8dp"].__setitem__("status", "SEALED_FULL_PRECISION_REPLAY_VECTOR"),
        lambda value: value["vectors"]["original_historical"].__setitem__("status", "IDENTICAL"),
        lambda value: value["pairwise_vector_classification"][0].__setitem__("status", "TOLERANCE_EQUIVALENT"),
        lambda value: value["parameter_contract"].__setitem__("order", ["w", "U"]),
        lambda value: value["pairwise_vector_classification"][0].__setitem__("tolerance", 9.0),
        lambda value: value["authority_ceiling"].__setitem__("replay_diagnostics_are_historical_diagnostics", True),
        lambda value: value["authority_ceiling"].__setitem__("curve_equivalence_implies_parameter_identifiability", True),
        lambda value: value.__setitem__("unreviewed", True),
    ]
    expected = expected_matrix()
    for index, edit in enumerate(edits):
        mutated = json.loads(json.dumps(matrix)); edit(mutated)
        require(mutated != expected, "E_NEGATIVE_FALSE_PASS", str(index))
    return len(edits)


def validate_content() -> int:
    matrix = strict_json((ROOT / MATRIX_PATH).read_bytes())
    require(matrix == expected_matrix(), "E_MATRIX_MISMATCH")
    validate_documents(); validate_source_policy()
    return run_negatives(matrix)


def local_ref_guard() -> None:
    require(git("rev-parse", PROTECTED_BRANCH).decode().strip() == PROTECTED_TIP, "E_PROTECTED_LOCAL")
    local_main = subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/main"],
                                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=False, check=False)
    require(local_main.returncode == 1, "E_LOCAL_MAIN")


def live_refs(active: str) -> None:
    require(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").decode().split()[0] == active,
            "E_ACTIVE_LIVE")
    require(git("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}").decode().split()[0] ==
            PROTECTED_TIP, "E_PROTECTED_LIVE")
    require(git("ls-remote", "--heads", "origin", "refs/heads/main").decode().split()[0] == MAIN_TIP,
            "E_MAIN_LIVE")


def validate_staged() -> None:
    require(git("rev-parse", "HEAD").decode().strip() == STEP77_COMMIT, "E_PARENT")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "--abbrev-ref", "@{u}").decode().strip() == UPSTREAM, "E_UPSTREAM_NAME")
    require(git("rev-parse", UPSTREAM).decode().strip() == STEP77_COMMIT, "E_UPSTREAM_PARENT")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN")
    require(git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP and
            git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_TRACKING_PROTECTED")
    require(git("diff", "--cached", "--name-only").decode().splitlines() == FINAL_PATHS, "E_PATHS")
    require(not git("diff", "--name-only").strip() and
            not git("ls-files", "--others", "--exclude-standard").strip(), "E_DIRTY_OUTSIDE_STAGE")
    require(not git("diff", "--cached", "--check").strip(), "E_DIFF_CHECK")
    expected_status = {BUILDER_PATH: "A", VALIDATOR_PATH: "A", MATRIX_PATH: "A", RESULT_PATH: "A",
                       PARENT_LEDGER_PATH: "M", ACTIVE_LEDGER_PATH: "M", HANDOVER_PATH: "M"}
    status = git("diff", "--cached", "--name-status").decode().splitlines()
    require({line.split("\t", 1)[1]: line.split("\t", 1)[0] for line in status} == expected_status,
            "E_STATUS")
    live_refs(STEP77_COMMIT); local_ref_guard()


def validate_persistence(commit: str) -> None:
    require(len(commit) == 40 and all(char in "0123456789abcdef" for char in commit), "E_COMMIT")
    require(git("rev-parse", "HEAD").decode().strip() == commit, "E_HEAD")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "--abbrev-ref", "@{u}").decode().strip() == UPSTREAM,
            "E_UPSTREAM_NAME")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN")
    require(git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP and
            git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_TRACKING_PROTECTED")
    require(git("rev-parse", "HEAD^").decode().strip() == STEP77_COMMIT, "E_COMMIT_PARENT")
    require(len(git("rev-list", "--parents", "-n", "1", "HEAD").decode().split()) == 2,
            "E_SINGLE_PARENT")
    require(git("show", "-s", "--format=%s", "HEAD").decode().strip() == EXPECTED_SUBJECT, "E_SUBJECT")
    require(git("rev-parse", UPSTREAM).decode().strip() == commit, "E_UPSTREAM")
    live_refs(commit); local_ref_guard()
    require(git("diff", "--name-only", "HEAD^").decode().splitlines() == FINAL_PATHS, "E_COMMITTED_PATHS")
    require(not any(path.startswith("Claude/") for path in FINAL_PATHS), "E_CLAUDE")
    require(not git("status", "--porcelain").strip(), "E_DIRTY")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--staged", action="store_true")
    parser.add_argument("--persistence"); args = parser.parse_args()
    negatives = validate_content()
    if args.staged: validate_staged()
    if args.persistence:
        validate_persistence(args.persistence)
        print(f"{PERSISTENCE} commit={args.persistence} negative={negatives}/8")
    else:
        print(f"{GATE} negative={negatives}/8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL_P066_STEP78 {error}")
        raise SystemExit(1)
