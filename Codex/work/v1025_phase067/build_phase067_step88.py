#!/usr/bin/env python3
"""Build Phase 067 Step 88 source-grounded numerical-guard impact evidence."""

from __future__ import annotations

import argparse
import ast
import bisect
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
DATE = "2026-09-02"
SUBJECT = "audit(phase067): bound numerical guard impacts"
GATE = "PASS_P067_STEP88_NUMERICAL_GUARD"
PERSISTENCE = "PASS_P067_STEP88_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "3002e6ad393e79d5834ff46633dcc4adec1f128d62f030fbccaaf84728380600"

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
CALL_GRAPH_PATH = "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json"
UNIT_PATH = "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json"
TEST_DEMO_PATH = "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json"
STATE_FLOW_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
MUTABLE_STATE_PATH = "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json"
SAVED_RUNTIME_PATH = "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json"
GUIDE_TOOL_PATH = "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json"
FIT_REPLAY_PATH = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
OUTPUT_PATH = "Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json"

INPUT_PINS = {
    INVENTORY_PATH: ("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63",
                     "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1", False),
    ATTESTATION_PATH: ("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174",
                       "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9", False),
    CALL_GRAPH_PATH: ("54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f",
                      "63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc", True),
    UNIT_PATH: ("62f5eb265121987b83398266895a11e8a84d7f1ffa90c59fe929efb6f00614be",
                "099899de75edfde55a92ff31f577e178967212226cf4a13cdb951643b15e535c", True),
    TEST_DEMO_PATH: ("13a281c76282f5fae370d1c2b10f183937c685bceba466489a62b9e850049d4a",
                     "eadde68e51257e0daae9f9455be3a7331c77a56d1490b2291934ef75f45fa154", True),
    STATE_FLOW_PATH: ("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8",
                      "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44", True),
    MUTABLE_STATE_PATH: ("b8ac7affbb31195ec8dde6015890cbb50b1f2b9cc5815fc33c325efc95286f23",
                         "845b676aea321134b648de41320e7baf4f39f925ad2a1abe96f36f713bc95542", True),
    SAVED_RUNTIME_PATH: ("9bf610d2d09be7d95fd2493541d6c4336de330c37fb56d1f12c411b228dfbf82",
                         "0e2b0bd3f6120c9c8feaa879b5fe62a49934de5ea8dbddff14c700ddef32f196", True),
    GUIDE_TOOL_PATH: ("474f09ebb1605d3190867cee9746079b10c04f6bfbdfbab028e9d6c1be70ec08",
                      "c556671b6fd4284d740fdb0cc3777087442d4abd2160ace42d4ff70749d4144c", True),
    FIT_REPLAY_PATH: ("ff8141e7f0d950cfb6f588f41743e7b9221c5f4cb73ecc76522b0beb45a70d80",
                      "567c8b65886851e34fff8e913e6ad81819d8ce022001df6bf20a9b26fce6b029", False),
}

RELEASES = [
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14",
    "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2",
    "v1.0.19", "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23",
    "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
]

FEATURE_KEYS = [
    "LOGISTIC_BRANCH", "ENTROPY_XI_CLIP", "ENTROPY_DEN_FLOOR", "REGSOL_EXP_CLIP",
    "LOWPASS_DEPENDENCY_FALLBACK",
    "LEGACY_VOLTAGE_SORT", "LEGACY_T_INTERPOLATION", "LEGACY_OUTPUT_INTERPOLATION",
    "POINTWISE_STABLE_SORT", "POINTWISE_INVERSE_RESTORE", "RESOLUTION_FALLBACK",
    "PAD_FUNCTION", "PAD_CALL_SITE", "PAD_POINT_CAP", "ROOT_INPUT_GUARD", "ROOT_BRACKET_GUARD",
    "ROOT_ITERATION_LOOP", "ROOT_SILENT_MIDPOINT", "L_V_OVERRIDE_GUARD",
    "MISSING_KINETICS_FALLBACK", "NONFINITE_LQ_FALLBACK", "OMEGA_DOMAIN_BRANCH",
    "TRANSFER_HELPER", "RATIO_LOCAL_EXP", "POINTWISE_DENSE_THRESHOLD",
]
DEFAULT_KEYS = [
    "DEFAULT_ENTROPY_EPS", "DEFAULT_LAG_DECAY_CAP", "DEFAULT_PAD_NLV",
    "DEFAULT_PAD_MAXPTS", "DEFAULT_PAD_L_OVER_20", "DEFAULT_REGSOL_DELTA_FLOOR",
    "DEFAULT_LEGACY_GRID", "DEFAULT_ROOT_SOLVER",
]


class BuildError(RuntimeError):
    pass


def require(ok: bool, code: str) -> None:
    if not ok:
        raise BuildError(code)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("semantic_sha256", None)
    return sha(canonical(copy))


def predecessor_semantic(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy["semantic_sha256"] = ""
    return sha((json.dumps(copy, ensure_ascii=False, indent=2, sort_keys=True,
                           separators=(",", ": "), allow_nan=False) + "\n").encode("utf-8"))


def finish(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic(value)
    return value


def strict_json(raw: bytes, code: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, code + "_DUPLICATE")
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise BuildError(code) from exc
    require(isinstance(value, dict), code + "_ROOT")
    return value


def git_bytes(args: list[str]) -> bytes:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(completed.returncode == 0 and completed.stderr == b"", "E_GIT_READ")
    return completed.stdout


def input_json(path: str) -> dict[str, Any]:
    raw_pin, semantic_pin, modern = INPUT_PINS[path]
    raw = git_bytes(["show", f"{EXPECTED_PARENT}:{path}"])
    require(sha(raw) == raw_pin, "E_INPUT_RAW_" + path)
    value = strict_json(raw, "E_INPUT_JSON")
    observed = semantic(value) if modern else predecessor_semantic(value)
    require(observed == semantic_pin == value["semantic_sha256"], "E_INPUT_SEMANTIC_" + path)
    return value


def blob(oid: str) -> bytes:
    require(len(oid) == 40 and all(c in "0123456789abcdef" for c in oid), "E_BLOB_OID")
    return git_bytes(["cat-file", "blob", oid])


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__, "fields": [
            [field, stable_ast(getattr(value, field, None))] for field in value._fields
        ]}
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, tuple):
        return {"_tuple": [stable_ast(item) for item in value]}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return {"_literal_type": type(value).__name__, "repr": repr(value)}


def qualified_owner(tree: ast.Module, selected: ast.AST) -> str:
    rows: list[tuple[int, str]] = []
    def walk(node: ast.AST, scope: list[str]) -> None:
        nested = scope
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            nested = [*scope, node.name]
            if node.lineno <= selected.lineno and node.end_lineno >= selected.end_lineno:
                rows.append((node.end_lineno - node.lineno, ".".join(nested)))
        for child in ast.iter_child_nodes(node):
            walk(child, nested)
    walk(tree, [])
    return min(rows)[1] if rows else "<module>"


def anchor(tree: ast.Module, source: str, node: ast.AST) -> dict[str, Any]:
    start, end = int(node.lineno), int(node.end_lineno)
    text = "\n".join(source.splitlines()[start - 1:end]) + "\n"
    return {
        "qualified_owner": qualified_owner(tree, node),
        "ast_kind": type(node).__name__,
        "start_line": start,
        "end_line": end,
        "source_sha256_lf": sha(text.encode("utf-8")),
        "source_normalization": "LF_TERMINATED",
        "node_sha256": sha(canonical(stable_ast(node))),
        "expression": ast.unparse(node),
    }


def find_anchors(tree: ast.Module, source: str,
                 predicate: Callable[[ast.AST, str], bool]) -> list[dict[str, Any]]:
    rows: list[ast.AST] = []
    for node in ast.walk(tree):
        try:
            expression = ast.unparse(node)
        except (TypeError, ValueError):
            expression = ""
        if predicate(node, expression):
            rows.append(node)
    ordered = sorted(rows, key=lambda n: (n.lineno, n.col_offset, n.end_lineno, type(n).__name__))
    return [anchor(tree, source, node) for node in ordered]


def source_features(oid: str) -> dict[str, Any]:
    raw = blob(oid)
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    tests: dict[str, Callable[[ast.AST, str], bool]] = {
        "LOGISTIC_BRANCH": lambda n, e: isinstance(n, ast.Return) and "np.where" in e and "np.exp(-z)" in e and "np.exp(z)" in e,
        "ENTROPY_XI_CLIP": lambda n, e: isinstance(n, ast.Assign) and "xi_c" in e and "np.clip" in e,
        "ENTROPY_DEN_FLOOR": lambda n, e: isinstance(n, ast.Assign) and "dUdT" in e and "np.maximum(den, eps)" in e,
        "REGSOL_EXP_CLIP": lambda n, e: isinstance(n, ast.Assign) and "np.clip" in e and "-350.0" in e and "350.0" in e,
        "LOWPASS_DEPENDENCY_FALLBACK": lambda n, e: isinstance(n, ast.Try) and "scipy.signal" in e and "lfilter" in e,
        "LEGACY_VOLTAGE_SORT": lambda n, e: isinstance(n, ast.Assign) and "sort_idx" in e and "np.argsort(V_n)" in e,
        "LEGACY_T_INTERPOLATION": lambda n, e: isinstance(n, ast.Assign) and "T_work" in e and "np.interp" in e,
        "LEGACY_OUTPUT_INTERPOLATION": lambda n, e: isinstance(n, ast.Assign) and "dqdv_out" in e and "np.interp" in e,
        "POINTWISE_STABLE_SORT": lambda n, e: isinstance(n, ast.Assign) and "order" in e and "np.argsort" in e and "stable" in e,
        "POINTWISE_INVERSE_RESTORE": lambda n, e: isinstance(n, ast.Assign) and "dqdv_out" in e and "inv_order" in e,
        "RESOLUTION_FALLBACK": lambda n, e: isinstance(n, ast.Assign) and "unresolved" in e and "char_h" in e and "lag_len_V" in e,
        "PAD_FUNCTION": lambda n, e: isinstance(n, ast.FunctionDef) and n.name == "_causal_pad",
        "PAD_CALL_SITE": lambda n, e: isinstance(n, ast.Call) and e.startswith("_causal_pad("),
        "PAD_POINT_CAP": lambda n, e: isinstance(n, ast.If) and "npad > _LAG_PAD_MAXPTS" in e,
        "ROOT_INPUT_GUARD": lambda n, e: isinstance(n, ast.If) and "x_arr <= 0.0" in e and "x_arr >= 1.0" in e,
        "ROOT_BRACKET_GUARD": lambda n, e: isinstance(n, ast.If) and "f_lo < 0.0 < f_hi" in e,
        "ROOT_ITERATION_LOOP": lambda n, e: isinstance(n, ast.For) and "range(int(max_iter))" in e,
        "ROOT_SILENT_MIDPOINT": lambda n, e: isinstance(n, ast.Assign) and "out[k]" in e and "0.5 * (lo + hi)" in e,
        "L_V_OVERRIDE_GUARD": lambda n, e: isinstance(n, ast.If) and "L_V_override is not None" in e and "np.isfinite(v)" in e,
        "MISSING_KINETICS_FALLBACK": lambda n, e: isinstance(n, ast.If) and "I <= 0" in e and "transition.get('dH_a') is None" in e,
        "NONFINITE_LQ_FALLBACK": lambda n, e: isinstance(n, ast.If) and "not np.isfinite(L_q)" in e,
        "OMEGA_DOMAIN_BRANCH": lambda n, e: isinstance(n, ast.If) and "Omega <= two_RT" in e,
        "TRANSFER_HELPER": lambda n, e: isinstance(n, ast.FunctionDef) and n.name == "transfer_apparent_from_equilibrium",
        "RATIO_LOCAL_EXP": lambda n, e: isinstance(n, ast.Assign) and "L_loc" in e and "np.exp" in e and "g_eff" in e,
        "POINTWISE_DENSE_THRESHOLD": lambda n, e: isinstance(n, ast.If) and "a < 0.0001" in e,
        "DEFAULT_ENTROPY_EPS": lambda n, e: isinstance(n, ast.Assign) and "eps = 1e-12" in e,
        "DEFAULT_LAG_DECAY_CAP": lambda n, e: isinstance(n, ast.Assign) and "_LAG_RESOLVE_DECAY_CAP = 40.0" in e,
        "DEFAULT_PAD_NLV": lambda n, e: isinstance(n, ast.Assign) and "_LAG_PAD_NLV = 5.0" in e,
        "DEFAULT_PAD_MAXPTS": lambda n, e: isinstance(n, ast.Assign) and "_LAG_PAD_MAXPTS = 4000" in e,
        "DEFAULT_PAD_L_OVER_20": lambda n, e: isinstance(n, ast.Assign) and "lag_length / 20.0" in e,
        "DEFAULT_REGSOL_DELTA_FLOOR": lambda n, e: isinstance(n, ast.Assign) and "max(float(delta), 1e-09)" in e,
        "DEFAULT_LEGACY_GRID": lambda n, e: isinstance(n, ast.FunctionDef) and n.name == "__init__" and "grid_pad_lo: float=0.15" in e and "n_work_min: int=2048" in e,
        "DEFAULT_ROOT_SOLVER": lambda n, e: isinstance(n, ast.FunctionDef) and n.name == "solve_U_oc" and "tol: float=1e-13" in e and "max_iter: int=200" in e,
    }
    anchors = {key: find_anchors(tree, source, tests[key]) for key in FEATURE_KEYS + DEFAULT_KEYS}
    return {
        "blob_oid": oid,
        "raw_sha256": sha(raw),
        "lf_sha256": sha(lf_bytes(raw)),
        "lf_normalization": "CRLF_AND_LONE_CR_TO_LF",
        "size_bytes": len(raw),
        "physical_lines": len(source.splitlines()),
        "encoding": "utf-8",
        "ast_parse": "PASS",
        "anchors": anchors,
    }


def optimizer_source_record(inventory: dict[str, Any], attestation: dict[str, Any]) -> dict[str, Any]:
    candidates = [row for row in inventory["occurrence_records"]
                  if row["path"].endswith("/fit_roundtrip_demo.py")]
    require(len(candidates) == 1, "E_OPTIMIZER_SOURCE_COUNT")
    occurrence = candidates[0]
    raw = blob(occurrence["blob_oid"])
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    tests = {
        "NELDER_MAXFEV_LOOP": lambda n, e: isinstance(n, ast.While) and "nfev < maxfev" in e,
        "NELDER_UNCONDITIONAL_RETURN": lambda n, e: isinstance(n, ast.Return) and "sim[idx][0]" in e,
        "SCIPY_STATUS_IGNORED": lambda n, e: isinstance(n, ast.Assign) and "theta_hat" in e and "sol.x" in e,
        "BACKEND_FALLBACK_DISCLOSED": lambda n, e: isinstance(n, ast.Assign) and "OPTIMIZER" in e and "Nelder-Mead fallback" in e,
        "DEFAULT_NELDER_MEAD": lambda n, e: isinstance(n, ast.FunctionDef) and n.name == "_nelder_mead" and "maxfev=20000" in e and "xatol=1e-10" in e and "fatol=1e-14" in e,
        "DEFAULT_SCIPY_LEAST_SQUARES": lambda n, e: isinstance(n, ast.Call) and "_scipy_ls" in e and "xtol=1e-14" in e and "max_nfev=5000" in e,
    }
    anchors = {key: find_anchors(tree, source, predicate) for key, predicate in tests.items()}
    require(all(value for value in anchors.values()), "E_OPTIMIZER_ANCHOR")
    inv = next(row for row in inventory["blob_records"] if row["blob_oid"] == occurrence["blob_oid"])
    att = next(row for row in attestation["blob_attestations"] if row["blob_oid"] == occurrence["blob_oid"])
    require(inv["blob_oid"] == occurrence["blob_oid"] and inv["ordinal"] == occurrence["blob_ordinal"]
            and inv["git_mode"] == occurrence["git_mode"] and inv["raw_sha256"] == sha(raw)
            and inv["lf_sha256"] == sha(lf_bytes(raw)) and inv["size_bytes"] == len(raw)
            and inv["physical_lines"] == len(source.splitlines()) and inv["occurrence_count"] == 1
            and inv["occurrence_paths"] == [occurrence["path"]]
            and inv["release_projection"] == [occurrence["release"]]
            and inv["role_projection"] == [occurrence["role"]], "E_OPTIMIZER_INVENTORY_BINDING")
    require(att["read_status"] == "READ_FULL" and att["unread_lines"] == 0
            and att["truncation_unresolved"] == 0 and att["ast_parse"] == "PASS"
            and att["blob_oid"] == occurrence["blob_oid"] and att["ordinal"] == occurrence["blob_ordinal"]
            and att["raw_sha256"] == sha(raw) and att["lf_sha256"] == sha(lf_bytes(raw))
            and att["encoding"] == "utf-8" and att["line_ranges"] == [[1, len(source.splitlines())]]
            and att["occurrence_projection"] == {"paths":[occurrence["path"]],
                                                   "releases":[occurrence["release"]],
                                                   "roles":[occurrence["role"]]}, "E_OPTIMIZER_ATTESTATION")
    return {
        "ordinal": occurrence["ordinal"],
        "manifest_entry_index": occurrence["manifest_entry_index"],
        "release": occurrence["release"],
        "path": occurrence["path"],
        "role": occurrence["role"],
        "blob_oid": occurrence["blob_oid"],
        "blob_ordinal": occurrence["blob_ordinal"],
        "git_mode": occurrence["git_mode"],
        "size_bytes": len(raw),
        "physical_lines": len(source.splitlines()),
        "raw_sha256": sha(raw),
        "lf_sha256": sha(lf_bytes(raw)),
        "lf_normalization":"CRLF_AND_LONE_CR_TO_LF",
        "anchors": anchors,
        "inventory_binding":{key:inv[key] for key in ("ordinal","blob_oid","git_mode","raw_sha256","lf_sha256","size_bytes","physical_lines","occurrence_count","occurrence_paths","release_projection","role_projection")},
        "attestation_binding":{key:att[key] for key in ("ordinal","blob_oid","raw_sha256","lf_sha256","encoding","ast_parse","read_status","unread_lines","truncation_unresolved","line_ranges","occurrence_projection","partition","reviewer","review_evidence_sha256","genealogy_sha256")},
    }


def production_projection(inventory: dict[str, Any], attestation: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = sorted([row for row in inventory["occurrence_records"] if row["role"] == "code"],
                  key=lambda row: RELEASES.index(row["release"]))
    require(len(rows) == 20 and [row["release"] for row in rows] == RELEASES, "E_OCCURRENCE_PROJECTION")
    keys = ("ordinal", "manifest_entry_index", "release", "path", "role", "blob_oid",
            "blob_ordinal", "git_mode", "size_bytes", "physical_lines")
    occurrences = [{key: row[key] for key in keys} for row in rows]
    features = []
    for oid in sorted({row["blob_oid"] for row in rows}):
        item = source_features(oid)
        refs = [row for row in occurrences if row["blob_oid"] == oid]
        item["blob_ordinal"] = refs[0]["blob_ordinal"]
        item["git_mode"] = refs[0]["git_mode"]
        item["occurrence_refs"] = [dict(row) for row in refs]
        require(item["size_bytes"] == refs[0]["size_bytes"]
                and item["physical_lines"] == refs[0]["physical_lines"], "E_SOURCE_EXTENT")
        inv = next(row for row in inventory["blob_records"] if row["blob_oid"] == oid)
        att = next(row for row in attestation["blob_attestations"] if row["blob_oid"] == oid)
        expected_paths = sorted(row["path"] for row in refs)
        expected_releases = [release for release in RELEASES if any(row["release"] == release for row in refs)]
        expected_roles = sorted({row["role"] for row in refs})
        require(inv["ordinal"] == item["blob_ordinal"] and inv["git_mode"] == item["git_mode"]
                and inv["raw_sha256"] == item["raw_sha256"] and inv["lf_sha256"] == item["lf_sha256"]
                and inv["size_bytes"] == item["size_bytes"] and inv["physical_lines"] == item["physical_lines"]
                and inv["blob_oid"] == oid and inv["occurrence_count"] == len(refs)
                and inv["occurrence_paths"] == expected_paths
                and inv["release_projection"] == expected_releases
                and inv["role_projection"] == expected_roles,
                "E_INVENTORY_BLOB_BINDING")
        require(att["ordinal"] == item["blob_ordinal"] and att["raw_sha256"] == item["raw_sha256"]
                and att["lf_sha256"] == item["lf_sha256"] and att["encoding"] == "utf-8"
                and att["ast_parse"] == "PASS" and att["read_status"] == "READ_FULL"
                and att["unread_lines"] == 0 and att["truncation_unresolved"] == 0
                and att["blob_oid"] == oid and att["line_ranges"] == [[1, item["physical_lines"]]]
                and att["occurrence_projection"] == {"paths":expected_paths,
                                                       "releases":expected_releases,
                                                       "roles":expected_roles},
                "E_ATTESTATION_BLOB_BINDING")
        item["inventory_binding"] = {key: inv[key] for key in
                                     ("ordinal", "blob_oid", "git_mode", "raw_sha256", "lf_sha256",
                                      "size_bytes", "physical_lines", "occurrence_count", "occurrence_paths",
                                      "release_projection", "role_projection")}
        item["attestation_binding"] = {key: att[key] for key in
                                       ("ordinal", "blob_oid", "raw_sha256", "lf_sha256", "encoding",
                                        "ast_parse", "read_status", "unread_lines", "truncation_unresolved",
                                        "line_ranges", "occurrence_projection", "partition", "reviewer",
                                        "review_evidence_sha256", "genealogy_sha256")}
        features.append(item)
    require(len(features) == 15, "E_FEATURE_BLOB_COUNT")
    return occurrences, features


def rounded(value: float) -> float:
    require(math.isfinite(value), "E_NONFINITE")
    return float(format(value, ".17g"))


def logistic(value: float) -> float:
    if value >= 0.0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def trap(values: list[float], step: float) -> float:
    return step * (sum(values) - 0.5 * values[0] - 0.5 * values[-1])


def dual_numpy_observation(script_body: str, code: str) -> list[dict[str, Any]]:
    prefix = "import json,platform,sys,warnings\nimport numpy as np\n"
    suffix = "\nresult['runtime']={'implementation':platform.python_implementation(),'python_version':list(sys.version_info[:3]),'numpy_version':np.__version__}\nprint(json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False))\n"
    records = []
    for version in ("3.12", "3.14"):
        argv = ["py", "-" + version, "-I", "-B", "-X", "utf8", "-c", prefix + script_body + suffix]
        completed = subprocess.run(argv, cwd=ROOT, check=False, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, timeout=30)
        require(completed.returncode == 0 and completed.stderr == b"", code + "_RUNTIME")
        value = strict_json(completed.stdout, code + "_JSON")
        records.append({"launcher":["py","-" + version,"-I","-B","-X","utf8","-c","<PINNED_SCRIPT>"],
                        "script_sha256_lf":sha((prefix + script_body + suffix).encode("utf-8")),
                        "exit_code":completed.returncode,"stdout_sha256":sha(completed.stdout),
                        "stderr_sha256":sha(completed.stderr),"payload":value})
    return records


def require_dual_payload(records: list[dict[str, Any]], expected: dict[str, Any], code: str) -> None:
    require(len(records) == 2 and [row["launcher"][1] for row in records] == ["-3.12", "-3.14"], code + "_ORDER")
    projections = []
    for index, row in enumerate(records):
        payload = row["payload"]
        require(set(row) == {"launcher","script_sha256_lf","exit_code","stdout_sha256","stderr_sha256","payload"}
                and row["exit_code"] == 0 and row["stderr_sha256"] == sha(b"")
                and set(payload) == set(expected) | {"runtime"}, code + "_SCHEMA")
        runtime = payload["runtime"]
        require(set(runtime) == {"implementation","python_version","numpy_version"}
                and runtime["implementation"] == "CPython"
                and type(runtime["python_version"]) is list and len(runtime["python_version"]) == 3
                and all(type(value) is int for value in runtime["python_version"])
                and runtime["python_version"][:2] == ([3,12] if index == 0 else [3,14])
                and type(runtime["numpy_version"]) is str, code + "_RUNTIME_IDENTITY")
        projection = {key:value for key,value in payload.items() if key != "runtime"}
        require(canonical(projection) == canonical(expected), code + "_EXPECTED_PAYLOAD")
        projections.append(projection)
    require(canonical(projections[0]) == canonical(projections[1]), code + "_CROSS_RUNTIME")


def logistic_runtime_observation() -> list[dict[str, Any]]:
    script = r'''z=np.array([-1000.0,-100.0,0.0,100.0,1000.0])
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter("always")
 out=np.where(z>=0,1.0/(1.0+np.exp(-z)),np.exp(z)/(1.0+np.exp(z)))
result={"finite":bool(np.all(np.isfinite(out))),"values":[float(x) for x in out],
"warning_categories":sorted([type(w.message).__name__ for w in caught]),
"overflow_count":sum("overflow" in str(w.message).lower() for w in caught),
"invalid_count":sum("invalid" in str(w.message).lower() for w in caught)}'''
    rows = dual_numpy_observation(script, "E_LOGISTIC")
    require(all(row["payload"]["finite"] is True and row["payload"]["overflow_count"] == 3
                and row["payload"]["invalid_count"] == 1 for row in rows), "E_LOGISTIC_RUNTIME_EXPECTATION")
    return rows


def lq_runtime_observation() -> list[dict[str, Any]]:
    script = r'''T=298.15; I=1.0; Q=1.0; R=8.314; h=6.62607015e-34; kB=1.380649e-23; A=4.0*R*T; dVdq=0.3
cases=[]
for dH in (-2000000.0,0.0,2000000.0):
 ln=float(np.log((I/Q)*h/kB/T)-np.log1p(np.exp(-A/(R*T)))+dH/(R*T)-0.5*A/(R*T))
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always'); raw=np.exp(ln)
 finite=bool(np.isfinite(raw)); rv=float(raw) if finite else 'POSITIVE_INFINITY'
 cases.append({'dH':dH,'ln_Lq':ln,'raw_Lq':rv,'resolver_lag_length':abs(dVdq)*float(raw) if finite else 0.0,
               'warning_categories':[type(w.message).__name__ for w in caught],
               'overflow_count':sum('overflow' in str(w.message).lower() for w in caught)})
result={'formula':'abs(dVdq)*L_q before nonfinite-to-zero fallback','dVdq':dVdq,'cases':cases}'''
    rows = dual_numpy_observation(script, "E_LQ")
    expected = {
        "formula":"abs(dVdq)*L_q before nonfinite-to-zero fallback", "dVdq":0.3,
        "cases":[
            {"dH":-2000000.0,"ln_Lq":-838.3115278411767,"raw_Lq":0.0,
             "resolver_lag_length":0.0,"warning_categories":[],"overflow_count":0},
            {"dH":0.0,"ln_Lq":-31.475724453991145,"raw_Lq":2.139274703366186e-14,
             "resolver_lag_length":6.417824110098558e-15,"warning_categories":[],"overflow_count":0},
            {"dH":2000000.0,"ln_Lq":775.3600789331945,"raw_Lq":"POSITIVE_INFINITY",
             "resolver_lag_length":0.0,"warning_categories":["RuntimeWarning"],"overflow_count":1},
        ],
    }
    require_dual_payload(rows, expected, "E_LQ")
    return rows


def ratio_exp_runtime_observation() -> list[dict[str, Any]]:
    script = r'''args=np.array([1000.0,0.0,-1000.0])
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter('always'); raw=np.exp(args)
vals=['POSITIVE_INFINITY' if np.isposinf(x) else float(x) for x in raw]
downstream=[]
for Li in raw:
 try:
  a=0.1/float(Li); previous=0.2; kp=0.2; kc=0.8
  if a < 1e-4: out=(1-a)*previous+a*0.5*(kc+kp)
  else:
   decay=float(np.exp(-a)); dksi=kc-kp
   out=decay*previous+kc*(1-decay)-(dksi/a)*(1-(1+a)*decay)
  peak=(kc-out)/float(Li)
  downstream.append({'status':'RETURNED','a':a,'state':out,'peak':peak})
 except ZeroDivisionError:
  downstream.append({'status':'UNCAUGHT_ZERO_DIVISION','exception':'ZeroDivisionError'})
result={'exponents':[1000.0,0.0,-1000.0],'exp_values':vals,
        'warning_categories':[type(w.message).__name__ for w in caught],
        'overflow_count':sum('overflow' in str(w.message).lower() for w in caught),
        'downstream':downstream}'''
    rows = dual_numpy_observation(script, "E_RATIO_EXP")
    expected = {
        "exponents":[1000.0,0.0,-1000.0], "exp_values":["POSITIVE_INFINITY",1.0,0.0],
        "warning_categories":["RuntimeWarning"], "overflow_count":1,
        "downstream":[
            {"status":"RETURNED","a":0.0,"state":0.2,"peak":0.0},
            {"status":"RETURNED","a":0.1,"state":0.22902450821575793,"peak":0.5709754917842421},
            {"status":"UNCAUGHT_ZERO_DIVISION","exception":"ZeroDivisionError"},
        ],
    }
    require_dual_payload(rows, expected, "E_RATIO_EXP")
    return rows


def np_interp_like(points: list[float], xp: list[float], fp: list[float]) -> list[float]:
    result: list[float] = []
    for point in points:
        index = bisect.bisect_right(xp, point)
        if index == 0:
            result.append(fp[0])
        elif index >= len(xp):
            result.append(fp[-1])
        else:
            left = index - 1
            scale = (point - xp[left]) / (xp[index] - xp[left])
            result.append(fp[left] + scale * (fp[index] - fp[left]))
    return result


def probe_records() -> list[dict[str, Any]]:
    runtime = logistic_runtime_observation()
    lq_runtime = lq_runtime_observation()
    ratio_runtime = ratio_exp_runtime_observation()
    eps = 1e-12
    sorted_indices = [1, 0, 2]
    sorted_v = [0.1, 0.2, 0.3]
    sorted_t = [280.0, 300.0, 340.0]
    work_v = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
    work_t = np_interp_like(work_v, sorted_v, sorted_t)
    point_order = [1, 3, 2, 0]
    inverse = [3, 0, 2, 1]
    payload = ["s0", "s1", "s2", "s3"]
    restored = [[payload[i] for i in point_order][inverse[i]] for i in range(4)]
    pad_rows = []
    for ratio in (0.1, 0.001, 0.000001):
        raw_n = int(math.ceil(5.0 / min(ratio, 0.05)))
        n = min(raw_n, 4000)
        direction = 1.0
        original = [0.0, ratio, 2.0 * ratio]
        pstep = 5.0 / n
        padded = [original[0] - direction * pstep * i for i in range(n, 0, -1)] + original
        evaluated = [rounded(logistic(value)) for value in padded]
        pad_rows.append({"step_over_lag": ratio, "raw_npad": raw_n, "returned_npad": n,
                         "capped": raw_n > 4000, "pstep_over_lag": pstep,
                         "span_over_lag": 5.0, "kernel_residual": rounded(math.exp(-5.0)),
                         "direction": "ASCENDING", "original_sample_suffix_preserved":padded[-len(original):] == original,
                         "suffix_identity":padded[-len(original):],"content_evaluated_count":len(evaluated),
                         "content_suffix_matches_direct":evaluated[-len(original):] == [rounded(logistic(v)) for v in original]})
    width = 0.1
    root_target = 0.9
    root0 = 0.5
    residual0 = logistic((root0 - 0.5) / width) - root_target
    lo, hi = 0.0, 1.0
    mid = 0.5 * (lo + hi)
    if logistic((mid - 0.5) / width) - root_target < 0.0:
        lo = mid
    else:
        hi = mid
    root1 = 0.5 * (lo + hi)
    residual1 = logistic((root1 - 0.5) / width) - root_target
    recurrence = [0.0]
    decay = math.exp(-0.1 / 0.2)
    for source in [1.0, 0.5, 0.0]:
        recurrence.append(decay * recurrence[-1] + (1.0 - decay) * source)
    regsol_delta = 0.01
    regsol_step = 0.01
    regsol_v = [-20.0 + i * regsol_step for i in range(4001)]
    def regsol_density(value: float, clipped: bool) -> float:
        z_value = value / (2.0 * regsol_delta)
        if clipped:
            z_value = min(max(z_value, -350.0), 350.0)
        try:
            return (1.0 / math.cosh(z_value)) ** 2 / (4.0 * regsol_delta)
        except OverflowError:
            return 0.0
    regsol_before = [regsol_density(v, False) for v in regsol_v]
    regsol_after = [regsol_density(v, True) for v in regsol_v]
    regsol_before_area = trap(regsol_before, regsol_step)
    regsol_after_area = trap(regsol_after, regsol_step)
    regsol_center = regsol_v[max(range(len(regsol_after)), key=lambda index: regsol_after[index])]
    regsol_plateau = regsol_density(20.0, True)
    def peak_monotonicity_violations(values: list[float]) -> int:
        center = max(range(len(values)), key=lambda index: values[index])
        return (sum(values[i] < values[i-1] for i in range(1,center+1))
                + sum(values[i] > values[i-1] for i in range(center+1,len(values))))
    clip_boundaries = []
    for boundary in (-7.0, 7.0):
        below = math.nextafter(boundary, -math.inf)
        above = math.nextafter(boundary, math.inf)
        values = [regsol_density(below,True),regsol_density(boundary,True),regsol_density(above,True)]
        clip_boundaries.append({"V":boundary,"one_sided_values":[rounded(v) for v in values],
                                "max_one_ulp_jump":rounded(max(abs(values[1]-values[0]),abs(values[2]-values[1])))})
    equality_lag = 0.001
    nextbelow_lag = math.nextafter(equality_lag, 0.0)
    a_equal = 1e-4
    a_below = math.nextafter(a_equal, 0.0)
    previous, ksi_previous, ksi_current = 0.2, 0.2, 0.8
    def dense(a_value: float) -> float:
        return (1.0 - a_value) * previous + a_value * 0.5 * (ksi_current + ksi_previous)
    def general(a_value: float) -> float:
        decay_value = math.exp(-a_value)
        dksi = ksi_current - ksi_previous
        return (decay_value * previous + ksi_current * (1.0 - decay_value)
                - (dksi / a_value) * (1.0 - (1.0 + a_value) * decay_value))
    resolution_width=0.02
    resolution_z=[-2.0,0.0,2.0]
    eq_curve=[logistic(value) for value in resolution_z]
    eq_derivative=[value*(1.0-value)/resolution_width for value in eq_curve]
    memory_curve=[eq_curve[0]]
    for current in eq_curve[1:]:
        pv=memory_curve[-1]; kp=eq_curve[len(memory_curve)-1]; a_value=0.04/equality_lag
        decay_value=math.exp(-a_value); dksi=current-kp
        memory_curve.append(decay_value*pv+current*(1-decay_value)
                            -(dksi/a_value)*(1-(1+a_value)*decay_value))
    fallback_curve=list(eq_curve)
    equality_peak=[(eq-lag)/equality_lag for eq,lag in zip(eq_curve,memory_curve)]
    nextbelow_peak=list(eq_derivative)
    base = {
        "status": "PASS_BOUNDED_INTERNAL",
        "authority": {"internal_software": True, "internal_numerical": True,
                      "external_scientific": False, "material": False,
                      "experimental": False, "canonical": False, "publication": False},
    }
    def probe_row(pid: str, family: str, feature_ids: list[str], trigger: str,
            inputs: dict[str, Any], pre: dict[str, Any], post: dict[str, Any],
            delta: dict[str, Any], warning_error: dict[str, Any], silent: bool,
            probe_evaluation_passed: bool, interpretation: str, status: str | None = None) -> dict[str, Any]:
        convergence = ({"criterion_met":False,"budget_exhausted":pid in {"I09","I10","I23"},
                        "success_flag_checked":pid == "I23","return_present":True,
                        "convergence_authority":False}
                       if pid in {"I09","I10","I15","I23"} else None)
        provenance = ("PINNED_PHASE066_STEP77_RUNTIME" if pid == "I23"
                      else "ISOLATED_DUAL_NUMPY_RUNTIME_FIXED_VECTOR" if pid in {"I01","I25","I26"}
                      else "FROZEN_SOURCE_STATIC_BRANCH" if pid in {"I08","I11","I13","I14","I15","I16","I22","I24"}
                      else "BOUNDED_STEP88_INDEPENDENT_ARITHMETIC_FIXTURE")
        return {"probe_id": pid, "family": family, "source_feature_ids": feature_ids,
                "trigger_predicate": trigger, "inputs": inputs, "pre_metrics": pre,
                "post_metrics": post, "delta_metrics": delta,
                "warning_error": warning_error, "silent": silent,
                "probe_evaluation_passed": probe_evaluation_passed,
                "convergence":convergence,
                "input_provenance":provenance,
                "interpretation": interpretation, "status": status or base["status"],
                "authority": base["authority"]}
    rows = [
        probe_row("I01", "OVERFLOW_BRANCH_EVALUATION", ["LOGISTIC_BRANCH"], "z includes +/-1000",
            {"z": [-1000.0, -100.0, 0.0, 100.0, 1000.0]}, {}, runtime,
            {"nonfinite_return_count": 0}, {"kind": "RUNTIME_WARNING", "observed": True},
            False, True, "Return is finite, but eager np.where branches emit overflow/invalid warnings."),
        probe_row("I02", "ENTROPY_CLIP", ["ENTROPY_XI_CLIP"], "xi outside or on [0,1] boundary",
            {"xi": [-1e-15, 0.0, 0.5, 1.0, 1.000000000000001], "eps": eps},
            {"finite_logit_count": 1},
            {"clipped": [eps, eps, 0.5, 1.0 - eps, 1.0 - eps],
             "logit_limit": rounded(math.log((1.0 - eps) / eps)), "finite_logit_count": 5},
            {"clipped_count": 4}, {"kind": "SILENT_CLIP", "observed": True},
            True, True, "Entropy logit is bounded; this is not clipping of the returned dQ/dV curve."),
        probe_row("I03", "ENTROPY_CLIP_METRIC_SCOPE", ["ENTROPY_XI_CLIP"], "entropy state xi is clipped before logit",
            {"xi_domain":"SCALAR_OR_ARRAY_STATE","eps":eps,"input_origin":"FROZEN_SOURCE_GUARD"},
            {"area":"NOT_APPLICABLE","center":"NOT_APPLICABLE","sign":"NOT_APPLICABLE",
             "continuity":"NOT_APPLICABLE","monotonicity":"NOT_APPLICABLE"},
            {"area":"NOT_APPLICABLE","center":"NOT_APPLICABLE","sign":"NOT_APPLICABLE",
             "continuity":"NOT_APPLICABLE","monotonicity":"NOT_APPLICABLE"},
            {"changed_metrics":[],"reason":"ENTROPY_STATE_CLIP_IS_NOT_A_CURVE_CLIP"},
            {"kind":"NONE","observed":False}, True, True,
            "Area, center, sign, continuity and monotonicity are inapplicable to this entropy state clip; no dQ/dV proxy is invented."),
        probe_row("I04", "LEGACY_SORT_INTERPOLATION", ["LEGACY_VOLTAGE_SORT", "LEGACY_T_INTERPOLATION"],
            "strictly distinct nonmonotonic voltages plus endpoint queries",
            {"V": [0.2,0.1,0.3], "T": [300.0,280.0,340.0], "work_V": work_v,
             "input_origin":"BOUNDED_STEP88_INDEPENDENT_FIXTURE"},
            {"chronology": [0,1,2], "duplicate_voltage_contract":"NOT_CLAIMED"},
            {"sort_indices": sorted_indices, "T_work": work_t,
             "left_endpoint_clamp":work_t[0],"right_endpoint_clamp":work_t[-1]},
            {"chronology_preserved": False, "endpoint_extrapolation_kind":"CONSTANT_CLAMP",
             "duplicate_voltage_case":"NOT_EXECUTED_NOT_CLAIMED"},
            {"kind": "NONE", "observed": False}, True, True,
            "Legacy path discards chronological order and clamps endpoint queries; duplicate-voltage behavior was not executed and is not claimed."),
        probe_row("I05", "POINTWISE_SORT_INVERSE", ["POINTWISE_STABLE_SORT", "POINTWISE_INVERSE_RESTORE"],
            "nonmonotonic input within one call",
            {"V": [0.3,0.1,0.2,0.1], "payload": payload},
            {"chronological_order": [0,1,2,3]},
            {"stable_voltage_order": point_order, "inverse": inverse, "restored_payload": restored},
            {"sample_correspondence_preserved": restored == payload,
             "chronological_causality_preserved": False},
            {"kind": "NONE", "observed": False}, True, True,
            "Output samples return to input positions, but memory follows voltage-sorted monotonic sweep order."),
        probe_row("I06", "PAD_UNCAPPED", ["PAD_FUNCTION", "PAD_POINT_CAP"], "step/L=0.1",
            {"step_over_lag": 0.1,"input_origin":"BOUNDED_STEP88_PAD_FIXTURE"}, {}, pad_rows[0],
            {"original_sample_suffix_preserved":pad_rows[0]["original_sample_suffix_preserved"],
             "content_re_evaluated":pad_rows[0]["content_suffix_matches_direct"]}, {"kind": "NONE", "observed": False},
            True, True, "Five-lag past extension uses 100 points at L/20."),
        probe_row("I07", "PAD_CAPPED", ["PAD_FUNCTION", "PAD_POINT_CAP"], "step/L below 0.00125",
            {"cases": [0.001,0.000001],"input_origin":"BOUNDED_STEP88_PAD_FIXTURE"}, {}, {"cases": pad_rows[1:]},
            {"cap": 4000, "span_over_lag": 5.0,
             "original_sample_suffix_preserved":all(r["original_sample_suffix_preserved"] for r in pad_rows[1:]),
             "content_re_evaluated":all(r["content_suffix_matches_direct"] for r in pad_rows[1:])},
            {"kind": "NONE", "observed": False}, True, True,
            "Point cap coarsens pad spacing but preserves five-lag span and original-sample suffix."),
        probe_row("I08", "ROOT_FAIL_FAST", ["ROOT_INPUT_GUARD", "ROOT_BRACKET_GUARD"],
            "x outside (0,1), Q_total<=0, invalid or unsigned bracket",
            {"invalid_cases": ["x=0", "x=1", "Q_total=0", "U_lo>=U_hi", "endpoint_sign_failure"]},
            {}, {"returned": None}, {"failure_cases": 5},
            {"kind": "SOURCE_STATIC_VALUE_ERROR_PATH", "observed": False}, False, False,
            "Frozen source raises ValueError on these guards; no fault-injection runtime was executed.", "SOURCE_STATIC_FAIL_FAST"),
        probe_row("I09", "ROOT_ZERO_ITERATION", ["ROOT_ITERATION_LOOP", "ROOT_SILENT_MIDPOINT"],
            "max_iter=0 with bracket width above tol",
            {"U_lo":0.0,"U_hi":1.0,"center":0.5,"width":width,"target":root_target,"tol":1e-13,"max_iter":0},
            {"bracket_width":1.0}, {"returned_midpoint":root0,"residual":rounded(residual0)},
            {"tolerance_met":False,"convergence_flag_returned":False},
            {"kind":"NONE","observed":False}, True, False,
            "Silent midpoint is a returned value, never promoted to converged root.", "FAIL_NONCONVERGED_SILENT_RETURN"),
        probe_row("I10", "ROOT_INSUFFICIENT_ITERATION", ["ROOT_ITERATION_LOOP", "ROOT_SILENT_MIDPOINT"],
            "max_iter=1 leaves residual above tolerance",
            {"U_lo":0.0,"U_hi":1.0,"center":0.5,"width":width,"target":root_target,"tol":1e-13,"max_iter":1},
            {"bracket_width":1.0}, {"returned_midpoint":root1,"residual":rounded(residual1)},
            {"tolerance_met":False,"convergence_flag_returned":False},
            {"kind":"NONE","observed":False}, True, False,
            "Iteration exhaustion is silent and must remain a failed convergence boundary.", "FAIL_NONCONVERGED_SILENT_RETURN"),
        probe_row("I11", "LAG_FALLBACK", ["L_V_OVERRIDE_GUARD", "MISSING_KINETICS_FALLBACK", "NONFINITE_LQ_FALLBACK"],
            "direct L_V override or I<=0 or dH_a missing or computed L_q nonfinite",
            {"cases":["valid_L_V=0.02","invalid_L_V=-0.01","invalid_L_V=nonfinite",
                       "zero_current","missing_dH_a","nonfinite_L_q"]}, {},
            {"valid_override":0.02,"invalid_override_exception":"ValueError",
             "missing_or_zero_current_lag_length":0.0,"nonfinite_lq_lag_length":0.0},
            {"valid_override_is_intended":True,"invalid_override_fails_fast":True,
             "missing_kinetics_is_contractual_no_tail":True,"nonfinite_collapse_is_intended":False},
            {"kind":"MIXED_VALUE_OR_VALUE_ERROR","observed":False,"evidence":"SOURCE_STATIC"}, True, True,
            "Direct finite override and missing-kinetics no-tail behavior are intended; invalid override fails, while nonfinite computed kinetics silently collapses."),
        probe_row("I12", "LAG_RESOLUTION_FALLBACK", ["RESOLUTION_FALLBACK"],
            "char_h<=0 or lag_length*40<char_h or singleton",
            {"char_h":[0.0,0.1],"lag_length":[0.01,0.001]}, {},
            {"returned_state":"EQUILIBRIUM_DERIVATIVE","threshold":40.0},
            {"memory_curve_replaced":True}, {"kind":"NONE","observed":False}, True, True,
            "Resolution guard changes finite-memory curve to its equilibrium limit silently."),
        probe_row("I13", "LOWPASS_DEPENDENCY_FALLBACK", ["LOWPASS_DEPENDENCY_FALLBACK"],
            "SciPy lfilter import or call raises Exception",
            {"source_signal":[0.0,1.0,0.5,0.0],"grid_step":0.1,"lag_length":0.2}, {},
            {"manual_recurrence":[rounded(x) for x in recurrence],"decay":rounded(decay)},
            {"backend_disclosed_to_caller":False}, {"kind":"SOURCE_STATIC_CAUGHT_PATH","observed":False},
            True, True, "Manual recurrence fallback is silent at this helper boundary."),
        probe_row("I14", "OPTIMIZER_BACKEND_FALLBACK", ["BACKEND_FALLBACK_DISCLOSED"],
            "SciPy least_squares import raises Exception",
            {"preferred":"scipy.optimize.least_squares (trf)","alternate":"pure-numpy Nelder-Mead fallback"},
            {}, {"selected_backend_printed":True}, {"algorithm_changed":True},
            {"kind":"SOURCE_STATIC_CAUGHT_PATH","observed":False}, False, True,
            "Backend substitution is disclosed by OPTIMIZER print; result validity is not established."),
        probe_row("I15", "OPTIMIZER_NONCONVERGENCE", ["NELDER_MAXFEV_LOOP", "NELDER_UNCONDITIONAL_RETURN", "SCIPY_STATUS_IGNORED"],
            "source permits SciPy unsuccessful status or Nelder-Mead maxfev exhaustion",
            {"scipy_status_fields_consumed":False,"nelder_maxfev":20000}, {},
            {"return_path_present":True,"convergence_flag_returned":False,"budget_exhaustion_observed":False},
            {"must_not_promote_success":True,"actual_demo_exhaustion_claimed":False}, {"kind":"SOURCE_STATIC","observed":False}, True, False,
            "A source return path does not establish that a criterion was met or that exhaustion occurred in the observed demo.", "FAIL_NONCONVERGENCE_STATUS_UNBOUND"),
        probe_row("I16", "NUMERICAL_DEFAULT_CEILING", ["ROOT_ITERATION_LOOP", "ROOT_SILENT_MIDPOINT", "PAD_POINT_CAP"],
            "closed numerical-default inventory is used",
            {"default_record_refs":["D01","D02","D03","D04","D05","D06","D07","D08"]}, {},
            {"validation_of_tol_or_max_iter":False,"physical_optimality_proven":False},
            {"defaults_are_software_choices":True}, {"kind":"NONE","observed":False},
            True, False, "Defaults are frozen implementation choices, not externally validated physical constants.",
            "WITHHOLD_PHYSICAL_DEFAULT_AUTHORITY"),
    ]
    rows.extend([
        probe_row("I17", "ENTROPY_DENOMINATOR_FLOOR", ["ENTROPY_DEN_FLOOR"],
            "den<=0 returns zero; positive den divides by max(den,eps)",
            {"num":1e-12,"eps":1e-12,"den":[-1e-6,0.0,1e-15,1e-12]},
            {"unprotected":[-1e-6,"POSITIVE_INFINITY",1000.0,1.0]},
            {"guarded":[0.0,0.0,1.0,1.0]},
            {"changed_indices":[0,1,2],"sign_information_removed":True},
            {"kind":"SILENT_FLOOR_AND_ZERO","observed":True}, True, True,
            "Guard bounds entropy quotient only; it is not a dQ/dV clip."),
        probe_row("I18", "REGSOL_EXP_CLIP", ["REGSOL_EXP_CLIP"],
            "v24/v24.1 regular-solution |z| exceeds 350 on bounded V in [-20,20]",
            {"delta":regsol_delta,"V_min":-20.0,"V_max":20.0,"step":regsol_step,
             "input_origin":"BOUNDED_STEP88_REGSOL_FIXTURE"},
            {"area":rounded(regsol_before_area),"center":0.0,"minimum":0.0,"sign":"NONNEGATIVE",
             "adjacent_grid_max_change":rounded(max(abs(regsol_before[i]-regsol_before[i-1]) for i in range(1,len(regsol_before)))),
             "monotonicity_violations":peak_monotonicity_violations(regsol_before)},
            {"area":rounded(regsol_after_area),"center":regsol_center,"minimum":rounded(regsol_plateau),"sign":"NONNEGATIVE",
             "adjacent_grid_max_change":rounded(max(abs(regsol_after[i]-regsol_after[i-1]) for i in range(1,len(regsol_after)))),
             "monotonicity_violations":peak_monotonicity_violations(regsol_after),
             "clip_boundary_continuity":clip_boundaries},
            {"area":rounded(regsol_after_area-regsol_before_area),"center":regsol_center,
             "sign_changes":0,"tail_plateau_nonzero":True,
             "monotonicity_change":peak_monotonicity_violations(regsol_after)-peak_monotonicity_violations(regsol_before),
             "clip_boundary_max_one_ulp_jump":rounded(max(row["max_one_ulp_jump"] for row in clip_boundaries)),
             "bounded_domain":"[-20,20]","global_area":"DIVERGENT_NONZERO_CONSTANT_TAIL"},
            {"kind":"NONE","observed":False}, True, True,
            "Removed after v24.1; applies only to regular-solution helper, not the later logistic kernel."),
        probe_row("I19", "CHARGE_EQUAL_VOLTAGE_TIE", ["POINTWISE_STABLE_SORT"],
            "charge reverses a stable ascending argsort containing equal voltages",
            {"V":[0.1,0.1,0.2],"sample_ids":["a","b","c"]},
            {"ascending_stable_order":[0,1,2],"equal_tie_order":["a","b"]},
            {"charge_order":[2,1,0],"equal_tie_order":["b","a"]},
            {"equal_tie_reversed":True,"sample_identity_lost":False},
            {"kind":"NONE","observed":False}, True, True,
            "Stable ascending sort followed by full reversal reverses equal-voltage tie order."),
        probe_row("I20", "PAD_FIRST_STEP_ZERO", ["PAD_FUNCTION"],
            "first sorted interval is zero although later intervals are nonzero",
            {"V_prog":[0.0,0.0,1.0],"lag_length":0.1}, {},
            {"returned_npad":0,"returned_state":"ORIGINAL_ARRAY"},
            {"later_spacing_inspected":False,"pad_suppressed":True},
            {"kind":"NONE","observed":False}, True, False,
            "Pad decision samples only the first interval; later spacing does not recover padding.",
            "WITHHOLD_ARBITRARY_GRID_PAD_CORRECTNESS"),
        probe_row("I21", "RESOLUTION_STRICT_BOUNDARY", ["RESOLUTION_FALLBACK"],
            "unresolved=(char_h<=0) or lag_length*40<char_h",
            {"char_h":0.04,"decay_cap":40.0,"lag_equal":equality_lag,"lag_nextbelow":nextbelow_lag,
             "logistic_z":resolution_z,"width":resolution_width,
             "release_scope":"v1.0.15_THROUGH_v1.0.24.1_PRE_PAD_HELPER",
             "padding_before_pointwise_memory":False}, {},
            {"equal_fallback":equality_lag*40.0 < 0.04,
             "nextbelow_fallback":nextbelow_lag*40.0 < 0.04,
             "equilibrium_state":[rounded(v) for v in eq_curve],
             "equilibrium_derivative":[rounded(v) for v in eq_derivative],
             "equality_memory_state":[rounded(v) for v in memory_curve],
             "equality_returned_peak_shape":[rounded(v) for v in equality_peak],
             "nextbelow_returned_peak_shape":[rounded(v) for v in nextbelow_peak]},
            {"strict_operator":"<","boundary_discontinuous_branch":True,
             "state_lag_max_abs":rounded(max(abs(a-b) for a,b in zip(memory_curve,eq_curve))),
             "returned_peak_max_abs_delta":rounded(max(abs(a-b) for a,b in zip(equality_peak,nextbelow_peak)))},
            {"kind":"NONE","observed":False}, True, True,
            "For the pre-v25 no-pad helper, equality keeps memory and the next lower representable lag selects equilibrium fallback; v25+ padding impact is not generalized from this fixture."),
        probe_row("I22", "TRANSFER_PRECONDITION_GNF", ["TRANSFER_HELPER"],
            "helper prose requires uniform grid, but executable validation is absent",
            {"invalid_cases":["length<2","nonuniform_grid","zero_spacing","shape_mismatch"]}, {},
            {"executable_guards_found":0}, {"runtime_success_claimed":False},
            {"kind":"GROUND_NOT_FOUND","observed":True}, False, False,
            "Doc-only preconditions are not executable guard evidence.", "GROUND_NOT_FOUND_EXECUTABLE_GUARD"),
        probe_row("I23", "PERSISTED_OPTIMIZER_NONCONVERGENCE", ["SCIPY_STATUS_IGNORED"],
            "selected Direct14 trial reaches max_nfev",
            {"selected_trial":11,"max_nfev":6000}, {},
            {"status":0,"success":False,"nfev":6000,"njev":5656,
             "optimality":0.11459771897658692,"cost":11.287055224907945},
            {"returned_vector_present":True,"runtime_success":False},
            {"kind":"PERSISTED_STEP77_EVIDENCE","observed":True}, False, False,
            "Finite selected vector remains explicitly nonconverged.", "FAIL_NONCONVERGED_SELECTED_TRIAL"),
        probe_row("I24", "OMEGA_DOMAIN_BRANCH", ["OMEGA_DOMAIN_BRANCH"],
            "Omega<=2*R*T",
            {"Omega_over_2RT":[0.0,0.5,1.0]}, {},
            {"hysteresis_gap":0.0}, {"fallback":False,"intended_domain_branch":True},
            {"kind":"NONE","observed":False}, True, True,
            "This is an intended model-domain branch and is not a numerical fallback."),
        probe_row("I25", "LQ_OVERFLOW_COLLAPSE", ["NONFINITE_LQ_FALLBACK"],
            "func_L_q exponent underflows, is finite, or overflows",
            {"T":298.15,"I":1.0,"Q_cell":1.0,"A_formula":"4*R*T","dVdq":0.3,
             "dH":[-2_000_000.0,0.0,2_000_000.0],"input_origin":"BOUNDED_STEP88_LQ_FIXTURE"}, {},
            {"dual_runtime_observations":lq_runtime},
            {"overflow_maps_to_zero_lag":True,"finite_path_scales_by_abs_dVdq":True},
            {"kind":"ISOLATED_NUMPY_RUNTIME","observed":True}, True, False,
            "Nonfinite kinetic output silently collapses to equilibrium; this is not successful kinetics.",
            "FAIL_NONFINITE_KINETICS_COLLAPSE"),
        probe_row("I26", "RATIO_LOCAL_EXP_RANGE", ["RATIO_LOCAL_EXP"],
            "g_eff*(1-ksi_lag0) spans +/-1000",
            {"exponents":[1000.0,0.0,-1000.0],"input_origin":"BOUNDED_STEP88_RATIO_EXP_FIXTURE"}, {},
            {"dual_runtime_observations":ratio_runtime},
            {"overflow_count_per_runtime":1,"underflow_to_zero":True,"finite_middle":True,
             "infinite_Li_state_frozen":True,"infinite_Li_peak_zero":True,
             "zero_Li_exception":"ZeroDivisionError"},
            {"kind":"RUNTIME_WARNING_AND_UNCAUGHT_ZERO_DIVISION","observed":True}, False, False,
            "The ratio path maps infinite local length to a frozen state and zero peak, while zero local length raises uncaught ZeroDivisionError; neither is success.",
            "FAIL_NONFINITE_RATIO_LOCAL_LENGTH"),
        probe_row("I27", "POINTWISE_DENSE_THRESHOLD", ["POINTWISE_DENSE_THRESHOLD"],
            "a<1e-4 selects dense-grid approximation while equality selects general expression",
            {"a_equal":a_equal,"a_nextbelow":a_below,"previous":previous,
             "ksi_previous":ksi_previous,"ksi_current":ksi_current,
             "input_origin":"BOUNDED_STEP88_POINTWISE_THRESHOLD_FIXTURE"},
            {"nextbelow_dense":rounded(dense(a_below))},
            {"equality_general":rounded(general(a_equal))},
            {"branch_output_jump":rounded(general(a_equal)-dense(a_below)),"operator":"<"},
            {"kind":"NONE","observed":False}, True, True,
            "A one-ULP input change across the strict threshold changes formulas; the bounded output discontinuity is recorded."),
    ])
    return rows


def guard_records(features: list[dict[str, Any]], optimizer: dict[str, Any]) -> list[dict[str, Any]]:
    definitions = [
        ("G01","LOGISTIC_OVERFLOW","z branch evaluated through np.where","finite logistic state","RuntimeWarning overflow/invalid","EAGER_BRANCH_WARNING",["LOGISTIC_BRANCH"],["I01"]),
        ("G02","ENTROPY_CLIP","xi clipped to [eps,1-eps]","finite bounded logit","none","SILENT_CLIP",["ENTROPY_XI_CLIP"],["I02","I03"]),
        ("G03","LEGACY_SORT_INTERPOLATE","legacy voltage work-grid path","interpolated temperature and output","none","SILENT_RESAMPLE",["LEGACY_VOLTAGE_SORT","LEGACY_T_INTERPOLATION","LEGACY_OUTPUT_INTERPOLATION"],["I04"]),
        ("G04","POINTWISE_SORT_RESTORE","v15+ voltage-stable sort","input-position output correspondence","none","SILENT_REORDER",["POINTWISE_STABLE_SORT","POINTWISE_INVERSE_RESTORE"],["I05"]),
        ("G05","PAD_EXTENSION","v25+ finite positive lag/grid","five-lag past extension","none","SILENT_PAD",["PAD_FUNCTION","PAD_CALL_SITE"],["I06"]),
        ("G06","PAD_CAP","raw npad exceeds 4000","4000-point five-lag extension","none","SILENT_COARSEN",["PAD_POINT_CAP"],["I07"]),
        ("G07","ROOT_INVALID","invalid domain/capacity/bracket","no root returned","ValueError","FAIL_FAST",["ROOT_INPUT_GUARD","ROOT_BRACKET_GUARD"],["I08"]),
        ("G08","ROOT_EXHAUSTION","iteration range ends before tolerance","midpoint returned without status","none","SILENT_NONCONVERGENCE",["ROOT_ITERATION_LOOP","ROOT_SILENT_MIDPOINT"],["I09","I10"]),
        ("G09","DIRECT_LAG_OVERRIDE","L_V key supplied","finite nonnegative override or ValueError","ValueError invalid override","EXPLICIT_OVERRIDE",["L_V_OVERRIDE_GUARD"],["I11"]),
        ("G10","MISSING_KINETICS","I<=0 or dH_a absent","lag length 0 then equilibrium derivative","none","SILENT_FALLBACK",["MISSING_KINETICS_FALLBACK"],["I11"]),
        ("G11","NONFINITE_KINETICS","computed L_q nonfinite","lag length 0 then equilibrium derivative","none","SILENT_FALLBACK",["NONFINITE_LQ_FALLBACK"],["I11","I25"]),
        ("G12","RESOLUTION_LIMIT","singleton, repeated V, or lag*40<char_h","equilibrium derivative","none","SILENT_NUMERICAL_FALLBACK",["RESOLUTION_FALLBACK"],["I12"]),
        ("G13","LOWPASS_BACKEND","SciPy lfilter raises","manual recurrence","caught Exception","SILENT_DEPENDENCY_FALLBACK",["LOWPASS_DEPENDENCY_FALLBACK"],["I13"]),
        ("G14","OPTIMIZER_BACKEND_SELECTION","SciPy import unavailable","alternate backend selected","backend printed","DISCLOSED_BACKEND_SELECTION",["BACKEND_FALLBACK_DISCLOSED"],["I14"]),
        ("G15","OPTIMIZER_TERMINATION_CONVERGENCE","SciPy unsuccessful status or pure-NM budget exhaustion","parameter vector returned","convergence flag ignored or absent","SILENT_NONCONVERGENCE",["NELDER_MAXFEV_LOOP","NELDER_UNCONDITIONAL_RETURN","SCIPY_STATUS_IGNORED"],["I15","I23"]),
        ("G16","ENTROPY_DENOMINATOR","den<=0 or 0<den<eps","zero or floored quotient","none","SILENT_FLOOR_AND_ZERO",["ENTROPY_DEN_FLOOR"],["I17"]),
        ("G17","REGSOL_EXPONENT_CLIP","v24/v24.1 regular-solution |z|>350","clipped cosh tail plateau","none","SILENT_CLIP",["REGSOL_EXP_CLIP"],["I18"]),
        ("G18","CHARGE_TIE_REVERSAL","equal voltage samples in charge order","stable ascending order fully reversed","none","SILENT_REORDER",["POINTWISE_STABLE_SORT"],["I19"]),
        ("G19","PAD_FIRST_STEP","first interval is zero","original array and npad=0","none","SILENT_PAD_SUPPRESSION",["PAD_FUNCTION"],["I20"]),
        ("G20","RESOLUTION_STRICT_BOUNDARY","lag*40<char_h","equilibrium derivative below strict boundary","none","SILENT_NUMERICAL_FALLBACK",["RESOLUTION_FALLBACK"],["I21"]),
        ("G21","TRANSFER_PRECONDITION","uniform-grid/length preconditions stated only in prose","no validated state","none","GROUND_NOT_FOUND_EXECUTABLE_GUARD",["TRANSFER_HELPER"],["I22"]),
        ("G22","OMEGA_DOMAIN","Omega<=2RT","zero hysteresis gap","none","INTENDED_MODEL_BRANCH",["OMEGA_DOMAIN_BRANCH"],["I24"]),
        ("G23","RATIO_LOCAL_EXPONENT","local exponent outside finite range","infinite Li freezes state/zeroes peak; zero Li raises before return","RuntimeWarning overflow or uncaught ZeroDivisionError","NONFINITE_RATIO_LOCAL_LENGTH",["RATIO_LOCAL_EXP"],["I26"]),
        ("G24","POINTWISE_DENSE_THRESHOLD","a<1e-4 versus equality","different recurrence formula","none","STRICT_BRANCH_DISCONTINUITY",["POINTWISE_DENSE_THRESHOLD"],["I27"]),
    ]
    result = []
    for gid, family, trigger, returned, warning, behavior, keys, probes in definitions:
        production_keys = [key for key in keys if key in FEATURE_KEYS]
        blob_oids = sorted({row["blob_oid"] for row in features
                            if any(row["anchors"].get(key, []) for key in production_keys)})
        refs = sorted([ref for row in features if row["blob_oid"] in blob_oids
                       for ref in row["occurrence_refs"]], key=lambda ref: RELEASES.index(ref["release"]))
        if any(key not in FEATURE_KEYS for key in keys):
            blob_oids = sorted(set(blob_oids + [optimizer["blob_oid"]]))
        result.append({"guard_id":gid,"family":family,"trigger_predicate":trigger,
                       "returned_state":returned,"warning_error":warning,"behavior":behavior,
                       "source_feature_ids":keys,"source_blob_oids":blob_oids,
                       "production_occurrence_refs":refs,"probe_ids":probes,
                       "fallback_is_intended_behavior":(
                            True if family in {"MISSING_KINETICS","OMEGA_DOMAIN","DIRECT_LAG_OVERRIDE"}
                            else False if family in {"NONFINITE_KINETICS","RESOLUTION_LIMIT","RESOLUTION_STRICT_BOUNDARY","ROOT_EXHAUSTION","OPTIMIZER_TERMINATION_CONVERGENCE","RATIO_LOCAL_EXPONENT"}
                           else None),
                       "physical_interpretation_ceiling":"INTERNAL_SOFTWARE_NUMERICAL_ONLY"})
    return result


def numerical_default_records(features: list[dict[str, Any]], optimizer: dict[str, Any]) -> list[dict[str, Any]]:
    specifications = [
        ("D01","ENTROPY_EPS",{"eps":1e-12},["DEFAULT_ENTROPY_EPS"]),
        ("D02","LAG_RESOLUTION_CAP",{"decay_cap":40.0},["DEFAULT_LAG_DECAY_CAP"]),
        ("D03","PAD_EXTENSION",{"lag_span":5.0,"lag_step_divisor":20.0,"max_points":4000},
         ["DEFAULT_PAD_NLV","DEFAULT_PAD_L_OVER_20","DEFAULT_PAD_MAXPTS"]),
        ("D04","REGSOL_CLIP",{"delta_floor":1e-9,"z_clip_lower":-350.0,"z_clip_upper":350.0},
         ["DEFAULT_REGSOL_DELTA_FLOOR","REGSOL_EXP_CLIP"]),
        ("D05","LEGACY_WORK_GRID",{"grid_pad_lo":0.15,"grid_pad_hi":0.15,"n_work_min":2048,"min_lag_grid_steps":2.0},
         ["DEFAULT_LEGACY_GRID"]),
        ("D06","ROOT_SOLVER",{"tol":1e-13,"max_iter":200},["DEFAULT_ROOT_SOLVER"]),
    ]
    result = []
    for default_id, family, values, keys in specifications:
        source_rows = []
        refs = []
        for row in features:
            counts = {key:len(row["anchors"].get(key, [])) for key in keys}
            if any(counts.values()):
                source_rows.append({"blob_oid":row["blob_oid"],"blob_ordinal":row["blob_ordinal"],
                                    "anchor_multiplicities":counts})
                refs.extend(row["occurrence_refs"])
        result.append({"default_id":default_id,"family":family,"values":values,
                       "source_feature_ids":keys,"source_blob_records":source_rows,
                       "occurrence_refs":sorted(refs,key=lambda ref:RELEASES.index(ref["release"])),
                       "validated_input_range":False,"external_physical_authority":False})
    for default_id, family, values, key in [
        ("D07","PURE_NUMPY_NELDER_MEAD",{"maxfev":20000,"xatol":1e-10,"fatol":1e-14},"DEFAULT_NELDER_MEAD"),
        ("D08","SCIPY_LEAST_SQUARES",{"xtol":1e-14,"ftol":1e-14,"gtol":1e-14,"max_nfev":5000},"DEFAULT_SCIPY_LEAST_SQUARES")]:
        result.append({"default_id":default_id,"family":family,"values":values,
                       "source_feature_ids":[key],"source_blob_records":[{
                           "blob_oid":optimizer["blob_oid"],"blob_ordinal":optimizer["blob_ordinal"],
                           "anchor_multiplicities":{key:len(optimizer["anchors"][key])}}],
                       "occurrence_refs":[{k:optimizer[k] for k in ("ordinal","manifest_entry_index","release","path","role","blob_oid","blob_ordinal","git_mode","size_bytes","physical_lines")}],
                       "validated_input_range":False,"external_physical_authority":False})
    require([row["default_id"] for row in result] == [f"D{i:02d}" for i in range(1,9)], "E_DEFAULT_RECORDS")
    return result


def candidate_dispositions(inventory: dict[str, Any], selected_oids: set[str]) -> list[dict[str, Any]]:
    rows = []
    for item in sorted(inventory["blob_records"], key=lambda row: row["ordinal"]):
        roles = item["role_projection"]
        included = item["blob_oid"] in selected_oids
        rows.append({"blob_ordinal":item["ordinal"],"blob_oid":item["blob_oid"],
                     "occurrence_count":item["occurrence_count"],"role_projection":roles,
                     "selected_for_step88":included,
                     "disposition":"CANONICAL_PRODUCTION_OR_OPTIMIZER_SOURCE" if included else "DISCOVERY_ONLY_EXCLUDED_NONPRODUCTION",
                     "reason":"production role or exact v1.0.19 optimizer source" if included else "outside Step88 production/optimizer scope; lexical hits are not authority"})
    require(len(rows) == 84 and len({row["blob_oid"] for row in rows}) == 84, "E_CANDIDATE_DISPOSITION")
    return rows


def optimizer_routes(optimizer: dict[str, Any], test_demo: dict[str, Any],
                     fit_replay: dict[str, Any]) -> list[dict[str, Any]]:
    runtime = [row for row in test_demo["runtime_records"] if row["blob_oid"] == optimizer["blob_oid"]]
    require(len(runtime) == 2, "E_OPTIMIZER_RUNTIME_COUNT")
    runtime_projection = [{"runtime_record_id":"STEP86_RUNTIME_" + str(index + 100),
                           "runtime":row["runtime"],"launcher":row["launcher"],
                           "representative_release":row["representative_release"],
                           "representative_path":row["representative_path"],
                           "blob_oid":row["blob_oid"],"exit_code":row["exit_code"],
                           "outcome":row["outcome"],"runtime_execution_status":row["runtime_execution_status"],
                           "stdout_sha256":row["stdout_sha256"],"stderr_sha256":row["stderr_sha256"],
                           "backend_disclosure":"scipy.optimize.least_squares (trf)" if "scipy.optimize" in row["stdout"] else "pure-numpy Nelder-Mead fallback"}
                          for index,row in enumerate(runtime)]
    trials = []
    for run in fit_replay["runtime_reproductions"]:
        selected = run["trials"][run["best_trial"]]
        trials.append({"runtime_label":run["runtime_label"],"python_implementation":run["python_implementation"],
                       "python_version":run["python_version"],"numpy_version":run["numpy_version"],
                       "scipy_version":run["scipy_version"],"sealed_runtime_record_sha256":run["sealed_runtime_record_sha256"],
                       "sealed_runtime_record_semantic_sha256":run["sealed_runtime_record_semantic_sha256"],
                       "selected_trial":{key:selected[key] for key in ("index","status","success","nfev","njev","optimality","cost","returned_vector_sha256")}})
    require(len(trials) == 2 and trials[0]["selected_trial"] == trials[1]["selected_trial"]
            and trials[0]["selected_trial"]["index"] == 11 and trials[0]["selected_trial"]["status"] == 0
            and trials[0]["selected_trial"]["success"] is False, "E_SELECTED_TRIAL")
    return [
        {"route_id":"OR01","kind":"BACKEND_SELECTION","source_blob_oid":optimizer["blob_oid"],
         "source_anchor_ids":["BACKEND_FALLBACK_DISCLOSED"],"selected_backend_disclosed":True,
         "runtime_observations":runtime_projection,"convergence_claim":False},
        {"route_id":"OR02","kind":"DEMO_TERMINATION_CONVERGENCE","source_blob_oid":optimizer["blob_oid"],
         "source_anchor_ids":["SCIPY_STATUS_IGNORED","NELDER_MAXFEV_LOOP","NELDER_UNCONDITIONAL_RETURN"],
          "criterion_observed":False,"budget_exhaustion_observed":False,"success_flag_checked":False,
          "result_returned":True,"convergence_authority":False,"runtime_observations":runtime_projection},
        {"route_id":"OR03","kind":"PERSISTED_DIRECT14_TERMINATION","source_blob_oid":None,
         "source_anchor_ids":[],"criterion_observed":True,"budget_exhaustion_observed":True,
         "success_flag_checked":True,"result_returned":True,"convergence_authority":False,
         "runtime_observations":trials},
    ]


def build() -> dict[str, Any]:
    inventory = input_json(INVENTORY_PATH)
    attestation = input_json(ATTESTATION_PATH)
    graph = input_json(CALL_GRAPH_PATH)
    unit = input_json(UNIT_PATH)
    test_demo = input_json(TEST_DEMO_PATH)
    fit_replay = input_json(FIT_REPLAY_PATH)
    state_flow = input_json(STATE_FLOW_PATH)
    mutable_state = input_json(MUTABLE_STATE_PATH)
    saved_runtime = input_json(SAVED_RUNTIME_PATH)
    guide_tool = input_json(GUIDE_TOOL_PATH)
    occurrences, features = production_projection(inventory, attestation)
    optimizer = optimizer_source_record(inventory, attestation)
    probes = probe_records()
    guards = guard_records(features, optimizer)
    defaults = numerical_default_records(features, optimizer)
    routes = optimizer_routes(optimizer, test_demo, fit_replay)
    dispositions = candidate_dispositions(inventory, {row["blob_oid"] for row in features} | {optimizer["blob_oid"]})
    require(len(probes) == 27 and [row["probe_id"] for row in probes] == [f"I{i:02d}" for i in range(1,28)], "E_PROBE_COUNT")
    require(len(guards) == 24 and [row["guard_id"] for row in guards] == [f"G{i:02d}" for i in range(1,25)], "E_GUARD_COUNT")
    require(len(defaults) == 8, "E_DEFAULT_COUNT")
    probes_by_id = {row["probe_id"]:row for row in probes}
    linked_probe_ids = {probe_id for guard in guards for probe_id in guard["probe_ids"]}
    require(linked_probe_ids == set(probes_by_id) - {"I16"}, "E_GUARD_PROBE_COMPLETENESS")
    for guard in guards:
        for probe_id in guard["probe_ids"]:
            require(set(guard["source_feature_ids"]) & set(probes_by_id[probe_id]["source_feature_ids"]),
                    "E_GUARD_PROBE_FEATURE_CROSSWIRE")
    require(graph["universe"]["code_occurrences"] == 20 and graph["universe"]["code_unique_blobs"] == 15, "E_GRAPH_UNIVERSE")
    require(unit["universe"]["code_occurrences"] == 20 and unit["universe"]["code_unique_blobs"] == 15, "E_UNIT_UNIVERSE")
    require(state_flow["universe"]["flow_target_occurrences"] == 20
            and state_flow["universe"]["flow_target_unique_blobs"] == 15
            and state_flow["authority"]["runtime_behavior"] is False, "E_STATE_FLOW_SCOPE")
    require(mutable_state["authority"]["isolated_runtime_behavior"] is True
            and mutable_state["authority"]["canonical_profile"] is False, "E_MUTABLE_STATE_SCOPE")
    require(saved_runtime["runtime_contract"]["network_used"] is False
            and saved_runtime["authority"]["production_saved_loader"] is False, "E_SAVED_RUNTIME_SCOPE")
    require(guide_tool["authority"]["guide_claim_truth"] is False
            and guide_tool["authority"]["source_static"] is True, "E_GUIDE_TOOL_SCOPE")
    require(attestation["coverage"]["unique_blobs_read_full"] == 84, "E_ATTESTATION_COVERAGE")
    value = {
        "schema_version":"phase067-step88-numerical-guard-impact-v1",
        "artifact":OUTPUT_PATH,"phase":67,"step":88,"generated_date":DATE,
        "baseline_commit":BASELINE,"expected_parent":EXPECTED_PARENT,"branch":BRANCH,
        "expected_subject":SUBJECT,"gate":GATE,"persistence_terminal":PERSISTENCE,
        "precommit_status":"PASS_PENDING_PERSISTENCE",
        "containing_commit":"PENDING_AT_PRECOMMIT_BY_DESIGN",
        "result_first":True,"json_output_last":True,
        "inputs":{Path(path).stem.lower():{"path":path,"raw_sha256":pins[0],"semantic_sha256":pins[1]}
                  for path,pins in INPUT_PINS.items()},
        "universe":{"all_python_occurrences":129,"all_python_unique_blobs":84,
                    "production_occurrences":20,"production_unique_blobs":15,
                    "nonproduction_occurrences_total":109,
                    "supplemental_nonproduction_occurrences_selected":1,
                    "excluded_nonproduction_occurrences":108,"guard_records":24,
                    "impact_probe_records":27,"numerical_default_records":8,"optimizer_route_records":3,
                    "candidate_disposition_records":84,"release_count":20},
        "scope_policy":{"canonical_denominator":"PRODUCTION_20_OCCURRENCES_15_BLOBS_PLUS_EXACT_V19_OPTIMIZER",
                         "all_84_blobs_dispositioned":True,"broad_lexical_scan_authoritative":False,
                         "discovery_candidate_line_count":"NOT_CANONICAL_DENOMINATOR",
                          "nonproduction_runtime_behavior_promoted":False,
                          "nonproduction_projection_invariant":"109_TOTAL_EQUALS_1_SELECTED_OPTIMIZER_PLUS_108_EXCLUDED",
                          "intentionally_unlinked_probe_ids":["I16"],
                          "excluded_default_families":["plot_style_defaults","demo_display_defaults","tier_parameter_values","optimizer_initial_guesses"]},
        "candidate_disposition_records":dispositions,
        "source_occurrence_records":occurrences,
        "source_feature_records":features,
        "supplemental_optimizer_source_record":optimizer,
        "guard_records":guards,
        "impact_probe_records":probes,
        "numerical_default_records":defaults,
        "optimizer_route_records":routes,
        "open_gap_records":[
            {"gap_id":"O01","status":"OPEN","topic":"Q_cell basis and executable /3600 remain unresolved",
             "owner":"EXISTING_P066_OWNER_AND_STEP87_RECORD","promoted":False},
            {"gap_id":"O02","status":"OPEN","topic":"arbitrary nonmonotonic chronology is not represented by voltage sorting",
             "owner":"FOLLOWUP_RUNTIME_OR_API_OWNER","promoted":False},
            {"gap_id":"O03","status":"OPEN","topic":"root and optimizer return values lack convergence status on exhaustion",
             "owner":"FOLLOWUP_RUNTIME_OR_API_OWNER","promoted":False},
        ],
        "coverage":{"source_occurrences":"20/20","source_blobs":"15/15",
                    "guard_records":"24/24","impact_probes":"27/27","numerical_defaults":"8/8",
                    "candidate_dispositions":"84/84","optimizer_routes":"3/3",
                    "root_nonconvergence_success_promotions":0,
                    "optimizer_nonconvergence_success_promotions":0,
                    "fallback_intended_behavior_promotions":0,
                    "nonfinite_values":0,"duplicate_ids":0},
        "authority":{"internal_source_identity":True,"internal_software_behavior":True,
                     "internal_numerical_impact":True,"production_modified":False,
                     "external_scientific":False,"material":False,"experimental":False,
                     "canonical":False,"publication":False,
                      "runtime_scope":"ISOLATED_DUAL_NUMPY_FIXED_VECTOR_WARNING_VALUE_STATE_EXCEPTION_OBSERVATION",
                     "physical_ceiling":"NO_EXTERNAL_PHYSICAL_TRUTH"},
        "validation":{"strict_json_inputs":True,"source_git_blob_bound":True,
                      "typed_schema":True,"semantic_negative_controls":True,
                      "determinism_runs":2,"determinism_matches":2},
        "semantic_sha256":"",
    }
    return finish(value)


def atomic_write(path: Path, raw: bytes) -> None:
    require(not path.exists(), "E_OUTPUT_EXISTS")
    temp = path.with_name(path.name + ".tmp-phase067-step88")
    require(not temp.exists(), "E_TEMP_EXISTS")
    try:
        with temp.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--preview", action="store_true")
    modes.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    first = build()
    second = build()
    require(canonical(first) == canonical(second), "E_NONDETERMINISTIC")
    if args.collect:
        atomic_write(ROOT / OUTPUT_PATH, canonical(first))
    print("PASS_P067_STEP88_PREVIEW" if args.preview else GATE,
          "occurrences=20 blobs=15 guards=24 probes=27 defaults=8 determinism=2/2",
          "semantic=" + first["semantic_sha256"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
