#!/usr/bin/env python3
"""Validate Phase 067 Step 85 without importing the builder or production."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "f00bf2fa8f25c85f0c62cb901912763d98c8f070"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
EXPECTED_SUBJECT = "audit(phase067): separate defaults state persistence"
GATE = "PASS_P067_STEP85_STATE_DEFAULT_IMPORT"
PERSISTENCE = "PASS_P067_STEP85_PERSISTENCE"

BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step85.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step85.py"
MATRIX_PATH = "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json"
RUNTIME_PATH = "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_085_STATE_DEFAULT_IMPORT_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = [BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RUNTIME_PATH, RESULT_PATH,
               PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER]
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if index < 5 else "M") for index, path in enumerate(FINAL_PATHS)}

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STEP83_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
STEP84_PATH = "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json"
P066_MATRIX_PATH = "Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"
P066_RUNTIME_PATH = "Codex/results/PHASE_066_RUNTIME_ATTESTATION.json"
P066_CARRY_PATH = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"
INPUT_PINS = {
    INVENTORY_PATH: ("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63", "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"),
    ATTESTATION_PATH: ("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174", "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"),
    STEP83_PATH: ("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8", "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44"),
    STEP84_PATH: ("54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f", "63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc"),
    P066_MATRIX_PATH: ("7bab3f907ab6879fec0854c94f05e7d0b42fc618d6585f2737750e2a2b1b0695", "da615e36ce8df9d16e8ca7dfb69d1a74137510c1212cf2e2fcb53e8850fc2f75"),
    P066_RUNTIME_PATH: ("a5c909105280cf11a72ca9189070feb59c9005a824eeee4f3e161660394539d4", "3a393149d36513233e46ebbdbb0ce36f0393e28cb88e1fd3704cef5bf83fb040"),
    P066_CARRY_PATH: ("847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003", "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6"),
}

SOURCE_PATH = "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
TEST_PATH = "Claude/docs/v1.0.25.2/test_gates_v1024.py"
WRITER_PATH = "Claude/results/comp_v26_data/build_two_versions.py"
SAVED_PATHS = {
    "A_regsol": "Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json",
    "B_gallery": "Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json",
    "C_skew": "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json",
}
CASE_IDS = (
    "C01_FRESH_BASELINE", "C02_EXPLICIT_PROFILE", "C03_SKEW_REBIND_EXISTING_FUTURE",
    "C04_INPLACE_TRANSITION_ALIAS", "C05_SI_REBIND_SEED_CACHE",
    "C06_ORDINARY_IMPORT_CACHE", "C07_EXPLICIT_RELOAD", "C08_TWO_SPEC_LOAD_OBJECTS",
    "C09_NEW_PROCESS_RESET", "C10_TOGGLE_ORDER_A", "C11_TOGGLE_ORDER_B",
    "C12_ALIAS_EXPORT_GNF", "C13_SAVED_ROUTE_GNF",
)
CASE_CONTRACT = [
    {"case_id": "C01_FRESH_BASELINE", "class": "FRESH_PROCESS_PUBLIC_DEFAULT", "expected": "4_PLUS_2"},
    {"case_id": "C02_EXPLICIT_PROFILE", "class": "EXPLICIT_NONMUTATING", "expected": "7_PLUS_7_GLOBALS_UNCHANGED"},
    {"case_id": "C03_SKEW_REBIND_EXISTING_FUTURE", "class": "MODULE_GLOBAL_REBIND", "expected": "EXISTING_6_FUTURE_14"},
    {"case_id": "C04_INPLACE_TRANSITION_ALIAS", "class": "CALLER_LIST_ALIAS", "expected": "EXISTING_AND_FUTURE_OBSERVE_APPEND"},
    {"case_id": "C05_SI_REBIND_SEED_CACHE", "class": "SI_CONSTANT_R_F_REBIND_AND_SEED_CACHE", "expected": "LEGACY_TO_SI_DYNAMIC_CHANGE_EXISTING_SEED_STABLE_FALSE_RESTORES"},
    {"case_id": "C06_ORDINARY_IMPORT_CACHE", "class": "SYS_MODULE_CACHE", "expected": "MUTATED_STATE_PERSISTS"},
    {"case_id": "C07_EXPLICIT_RELOAD", "class": "EXPLICIT_REEXECUTION", "expected": "MODULE_DEFAULTS_RESET_EXISTING_OBJECT_STATE_AND_SEED_PERSIST"},
    {"case_id": "C08_TWO_SPEC_LOAD_OBJECTS", "class": "DISTINCT_MODULE_OBJECTS", "expected": "STATE_ISOLATED"},
    {"case_id": "C09_NEW_PROCESS_RESET", "class": "PAIRED_FRESH_ISOLATED_PROCESS", "expected": "C06_MUTATED_14_PID_DISTINCT_C09_FRESH_6"},
    {"case_id": "C10_TOGGLE_ORDER_A", "class": "BOUNDED_TWO_TOGGLE_ORDER", "expected": "SI_THEN_SKEW_FINAL_SI_7_PLUS_7"},
    {"case_id": "C11_TOGGLE_ORDER_B", "class": "BOUNDED_TWO_TOGGLE_ORDER", "expected": "SKEW_THEN_SI_FINAL_SI_7_PLUS_7"},
    {"case_id": "C12_ALIAS_EXPORT_GNF", "class": "CLOSED_VOCABULARY_SOURCE_SEARCH", "expected": "EXACT_SIX_SURFACES_GROUND_NOT_FOUND"},
    {"case_id": "C13_SAVED_ROUTE_GNF", "class": "STRICT_CONFIG_PARSE_DUMP_AND_DIRECT_CONSTRUCTOR_INJECTION", "expected": "8_14_14_SEARCHED_NAMES_ABSENT_NO_LOADER_USED_NO_KERNEL_DISPATCH"},
]
CONTROL_PINS = {
    RESULT_PATH: "dddd89968b0f9a5b4e6ac41b40e2ab7e7cf8b2bb74ff2e28436cda0099f293af",
    PARENT_LEDGER: "f2ff135df45558ccb955ba2f726d6a1525bb05bb580b97ebf00cef058bff4f7f",
    CANONICAL_LEDGER: "c03fe525eb73d9452de5b97b4abbace36c5c5faae5a7fdb6ac70f3bf8f4d05ab",
    HANDOVER: "e52aa07b1bc61a2bc20acb6ceea9d43620b8fecf5a8e98b74254b86fb045d60f",
}
BUILDER_SOURCE_POLICY_SHA256_LF = "1f299dc25d048de3e194bbe6d84ff301a839bd5c8cf8125f59f99489f800052c"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "6eee08a2fdd4f531b2147db809c85adf7b3d2ca27acda99d6510f6a3bf5a8351"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, diagnostic: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(diagnostic + (":" + detail if detail else ""))


def typed_equal(actual: Any, expected: Any) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return (set(actual) == set(expected)
                and all(typed_equal(actual[key], expected[key]) for key in expected))
    if isinstance(expected, list):
        return (len(actual) == len(expected)
                and all(typed_equal(left, right) for left, right in zip(actual, expected)))
    return bool(actual == expected)


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__,
                **{field: stable_ast(getattr(value, field, None)) for field in value._fields}}
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if isinstance(value, complex):
        return {"_complex": [value.real, value.imag]}
    if value is Ellipsis:
        return {"_ellipsis": True}
    return value


def source_anchor(path: str, source: str, node: ast.AST, owner: str) -> dict[str, Any]:
    segment = ast.get_source_segment(source, node) or ""
    return {
        "path": path, "qualified_owner": owner, "ast_kind": type(node).__name__,
        "start_line": int(getattr(node, "lineno", 0)),
        "end_line": int(getattr(node, "end_lineno", getattr(node, "lineno", 0))),
        "source_sha256": sha256(segment.encode("utf-8")),
        "ast_sha256": sha256(canonical_bytes(stable_ast(node))),
    }


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    clone = copy.deepcopy(value)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def strict_load(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    require(not raw.startswith(b"\xef\xbb\xbf"), "E_JSON_BOM", label)
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, "E_JSON_DUPLICATE", f"{label}:{key}")
            out[key] = value
        return out
    def constant(token: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{label}:{token}")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    require(isinstance(value, dict), "E_JSON_TOP", label)
    nodes = 0
    maximum = 0
    stack = [(value, 1)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        maximum = max(maximum, depth)
        require(nodes <= 600_000 and depth <= 18, "E_JSON_BOUNDS", label)
        if isinstance(current, dict):
            stack.extend((entry, depth + 1) for entry in current.values())
        elif isinstance(current, list):
            stack.extend((entry, depth + 1) for entry in current)
        elif isinstance(current, float):
            require(math.isfinite(current), "E_JSON_NONFINITE", label)
    return value, nodes, maximum


def allowed_git_argv(args: tuple[str, ...]) -> bool:
    fixed = {
        ("rev-parse", "--abbrev-ref", "HEAD"),
        ("rev-parse", "--abbrev-ref", "@{upstream}"),
        ("rev-parse", "HEAD"), ("rev-parse", UPSTREAM),
        ("rev-parse", f"refs/remotes/{UPSTREAM}"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("ls-remote", "--get-url", "origin"),
        ("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        ("show-ref", "--verify", "--hash", "refs/heads/main"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("status", "--porcelain"), ("ls-files", "-s"),
        ("diff", "--name-only"), ("ls-files", "--others", "--exclude-standard"),
        ("diff", "--cached", "--check"),
        ("diff", "--cached", "--name-status", "--no-renames", "HEAD"),
        ("diff", "--name-only", PROTECTED_TIP, "--", "Claude"),
    }
    if args in fixed:
        return True
    if len(args) == 4 and args[:3] == ("ls-remote", "--heads", "origin"):
        return args[3] in {f"refs/heads/{BRANCH}",
                           "refs/heads/codex/lib-physics-endgame-v1025_2",
                           "refs/heads/main"}
    if len(args) == 2 and args[0] == "show":
        token = args[1]
        if token.startswith(EXPECTED_PARENT + ":"):
            return token.split(":", 1)[1] in INPUT_PINS
        if token.startswith(BASELINE + ":"):
            return token.split(":", 1)[1] in {SOURCE_PATH, TEST_PATH, WRITER_PATH, *SAVED_PATHS.values()}
        if token.startswith(":"):
            return token.split(":", 1)[1] in FINAL_SET
        if re.fullmatch(r"[0-9a-f]{40}:.+", token):
            return token.split(":", 1)[1] in FINAL_SET
    if len(args) == 3 and args[:2] == ("cat-file", "blob"):
        return bool(re.fullmatch(r"[0-9a-f]{40}", args[2]))
    if len(args) == 2 and args[0] == "rev-parse" and ":" in args[1]:
        revision, path = args[1].split(":", 1)
        return revision == BASELINE and path in {SOURCE_PATH, TEST_PATH, WRITER_PATH, *SAVED_PATHS.values()}
    if len(args) == 4 and args[:3] == ("ls-tree", BASELINE, "--"):
        return args[3] in SAVED_PATHS.values()
    if len(args) == 2 and args[0] == "rev-parse" and args[1].endswith("^"):
        return bool(re.fullmatch(r"[0-9a-f]{40}\^", args[1]))
    if len(args) == 4 and args[:3] in {
            ("show", "-s", "--format=%P"), ("show", "-s", "--format=%s")}:
        return bool(re.fullmatch(r"[0-9a-f]{40}", args[3]))
    if len(args) == 7 and args[:5] == (
            "diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r"):
        return (bool(re.fullmatch(r"[0-9a-f]{40}\^", args[5]))
                and bool(re.fullmatch(r"[0-9a-f]{40}", args[6])))
    if len(args) == 3 and args[:2] == ("ls-tree", "-r"):
        return bool(re.fullmatch(r"[0-9a-f]{40}", args[2]))
    return False


def git(args: tuple[str, ...], *, allow_failure: bool = False) -> bytes:
    require(allowed_git_argv(args), "E_GIT_ARGV", repr(args))
    cp = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, shell=False,
                        check=False, timeout=90)
    if not allow_failure:
        require(cp.returncode == 0, "E_GIT_READ", repr(args))
    return cp.stdout


def baseline_bytes(path: str) -> bytes:
    return git(("show", f"{BASELINE}:{path}"))


def commit_bytes(path: str) -> bytes:
    return git(("show", f"{EXPECTED_PARENT}:{path}"))


def normalized_policy(path: str, constant: str) -> str:
    raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
    pattern = re.compile(rb"(?m)^(" + constant.encode() + rb" = \")[0-9a-f]{64}(\")$")
    replaced, count = pattern.subn(rb"\g<1>" + b"0" * 64 + rb"\g<2>", raw)
    require(count == 1, "E_POLICY_CONSTANT", path)
    return sha256(replaced)


def load_predecessors() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    values: dict[str, dict[str, Any]] = {}
    bindings = []
    for path, (raw_pin, semantic_pin) in INPUT_PINS.items():
        raw = commit_bytes(path)
        require(sha256(raw) == raw_pin, "E_INPUT_RAW", path)
        value, _, _ = strict_load(raw, path)
        require(value.get("semantic_sha256") == semantic_pin, "E_INPUT_SEMANTIC_STORED", path)
        if path not in {INVENTORY_PATH, ATTESTATION_PATH}:
            clone = copy.deepcopy(value)
            clone.pop("semantic_sha256", None)
            fresh = (sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":"), allow_nan=False).encode("utf-8"))
                     if path in {P066_MATRIX_PATH, P066_RUNTIME_PATH, P066_CARRY_PATH}
                     else semantic_sha(value))
            require(fresh == semantic_pin, "E_INPUT_SEMANTIC_FRESH", path)
        values[path] = value
        bindings.append({"path": path, "raw_sha256": raw_pin, "semantic_sha256": semantic_pin})
    return values, bindings


def expected_source_static() -> dict[str, Any]:
    raw = baseline_bytes(SOURCE_PATH)
    text = raw.decode("utf-8")
    tree = ast.parse(text)
    assignments: dict[str, ast.AST] = {}
    functions: dict[str, ast.FunctionDef] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            assignments[node.targets[0].id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments[node.target.id] = node
        elif isinstance(node, ast.FunctionDef):
            functions[node.name] = node
    expected = {
        "R": "8.314", "F": "96485.0",
        "R_SI": "8.314462618", "F_SI": "96485.33212",
        "DEFAULT_GRAPHITE_TRANSITIONS": "GRAPHITE_STAGING_LIT",
        "DEFAULT_SI_TRANSITIONS": "None",
        "DEFAULT_CBG_GRAPHITE": "0.55",
        "DEFAULT_CBG_SI": "0.051",
    }
    for name, expression in expected.items():
        require(name in assignments and ast.unparse(assignments[name].value) == expression,
                "E_STATIC_ASSIGNMENT", name)
    toggle = functions.get("use_skew7_default")
    require(toggle is not None, "E_STATIC_TOGGLE")
    si_toggle = functions.get("use_si_constants")
    require(si_toggle is not None, "E_STATIC_SI_TOGGLE")
    blend = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                 and node.name == "BlendedAnodeDQDV")
    init = next(node for node in blend.body if isinstance(node, ast.FunctionDef) and node.name == "__init__")
    from_wt = next(node for node in blend.body if isinstance(node, ast.FunctionDef) and node.name == "from_wt")
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    absent = {
        "load_profile": "load_profile" not in names,
        "from_profile": "from_profile" not in names,
        "PROFILE_ALIASES": "PROFILE_ALIASES" not in names,
        "SAVED_PROFILES": "SAVED_PROFILES" not in names,
        "module___all__": "__all__" not in assignments,
        "use_legacy_4transition": "use_legacy_4transition" not in names,
    }
    assignment_rows = [
        {"name": name, "value_expression": expression,
         "anchor": source_anchor(SOURCE_PATH, text, assignments[name], "<module>")}
        for name, expression in expected.items()
    ]
    artifact = {
        "path": SOURCE_PATH,
        "blob_oid": gtext(("rev-parse", f"{BASELINE}:{SOURCE_PATH}")),
        "raw_sha256": sha256(raw), "physical_lines": len(text.splitlines()),
        "ast_parse": "PASS", "assignment_rows": assignment_rows,
        "toggle": {"name": "use_skew7_default",
                   "anchor": source_anchor(SOURCE_PATH, text, toggle, "use_skew7_default")},
        "si_constants_toggle": {
            "name": "use_si_constants", "legacy": {"R": 8.314, "F": 96485.0},
            "si": {"R": 8.314462618, "F": 96485.33212},
            "anchor": source_anchor(SOURCE_PATH, text, si_toggle, "use_si_constants")},
        "constructor_default_load": source_anchor(
            SOURCE_PATH, text, init, "BlendedAnodeDQDV.__init__"),
        "from_wt_q_gr_default": {
            "expression": ast.unparse(from_wt.args.defaults[-2]),
            "runtime_bound_value": 372.0,
            "anchor": source_anchor(SOURCE_PATH, text, from_wt, "BlendedAnodeDQDV.from_wt")},
        "absent_surfaces": absent,
        "header_docstring_conflict": {
            "status": "STALE_PROSE_CONFLICT_EXECUTABLE_ASSIGNMENT_WINS",
            "runtime_adjudication": "STEP85_FRESH_ISOLATED_PROCESS"},
    }
    return {
        "raw_sha256": sha256(raw), "physical_lines": len(text.splitlines()),
        "assignment_values": expected, "toggle_ast": ast.unparse(toggle),
        "si_toggle_ast": ast.unparse(si_toggle),
        "init_ast": ast.unparse(init),
        "from_wt_default_expression": ast.unparse(from_wt.args.defaults[-2]),
        "absent_surfaces": absent,
        "artifact": artifact,
    }


def independent_blob_search(inventory: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    search_names = {"load_profile", "from_profile", "PROFILE_ALIASES", "SAVED_PROFILES",
                    "__all__", "use_legacy_4transition", "use_skew7_default",
                    "use_si_constants", "R_SI", "F_SI", "_R_LEGACY", "_F_LEGACY"}
    all_rows = []
    for record in inventory["blob_records"]:
        oid = record["blob_oid"]
        raw = git(("cat-file", "blob", oid))
        tree = ast.parse(raw.decode("utf-8"))
        matches = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name, kind = node.name, type(node).__name__
            elif isinstance(node, ast.Name):
                name, kind = node.id, "Name"
            else:
                continue
            if name in search_names:
                matches.append({"name": name, "kind": kind,
                                "line": int(getattr(node, "lineno", 0))})
        occurrences = [row for row in inventory["occurrence_records"] if row["blob_oid"] == oid]
        all_rows.append({
            "blob_oid": oid, "blob_ordinal": record["ordinal"],
            "occurrence_paths": sorted(row["path"] for row in occurrences),
            "role_projection": sorted({row["role"] for row in occurrences}),
            "matches": sorted(matches, key=lambda row: (row["name"], row["line"], row["kind"])),
        })
    require(len(all_rows) == 84, "E_SEARCH_COUNT")
    production = [
        match for row in all_rows if "code" in row["role_projection"] for match in row["matches"]
        if match["name"] in {"load_profile", "from_profile", "PROFILE_ALIASES", "SAVED_PROFILES", "__all__"}
    ]
    require(not production, "E_SEARCH_PRODUCTION_LOADER")
    return sha256(canonical_bytes(all_rows)), [row for row in all_rows if row["matches"]]


def independent_production_projection(inventory: dict[str, Any]) -> dict[str, Any]:
    occurrences = [copy.deepcopy(row) for row in inventory["occurrence_records"]
                   if row.get("role") == "code"]
    oids = {row["blob_oid"] for row in occurrences}
    blobs = [copy.deepcopy(row) for row in inventory["blob_records"]
             if row.get("blob_oid") in oids]
    require(len(occurrences) == 20 and len(blobs) == len(oids) == 15,
            "E_PRODUCTION_SOURCE_DENOMINATOR")
    bindings = []
    for blob in blobs:
        members = [row for row in occurrences if row["blob_oid"] == blob["blob_oid"]]
        bindings.append({
            "blob_oid": blob["blob_oid"], "blob_ordinal": blob["ordinal"],
            "shared_blob_ref": f"P067-S82-B{blob['ordinal']:03d}",
            "occurrence_count": len(members),
            "occurrence_ordinals": [row["ordinal"] for row in members],
            "occurrence_paths": [row["path"] for row in members],
        })
    si_rows = []
    for row in occurrences:
        tree = ast.parse(git(("cat-file", "blob", row["blob_oid"])).decode("utf-8"),
                         filename=row["path"])
        if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == "use_si_constants" for node in ast.walk(tree)):
            si_rows.append({
                "release": row["release"], "ordinal": row["ordinal"],
                "manifest_entry_index": row["manifest_entry_index"], "path": row["path"],
                "blob_oid": row["blob_oid"], "blob_ordinal": row["blob_ordinal"],
                "shared_blob_ref": f"P067-S82-B{row['blob_ordinal']:03d}",
            })
    require([row["release"] for row in si_rows] ==
            ["v1.0.25.1", "v1.0.25.2", "v1.0.25"], "E_SI_RELEASE_PROJECTION")
    projection = {"occurrences": occurrences, "blobs": blobs,
                  "shared_blob_bindings": bindings}
    return {
        **projection, "occurrence_count": 20, "unique_blob_count": 15,
        "projection_sha256": sha256(canonical_bytes(projection)),
        "use_si_constants_occurrences": si_rows,
        "use_si_constants_occurrence_count": 3,
        "use_si_constants_unique_blob_count": 2,
    }


def independent_saved_profiles() -> list[dict[str, Any]]:
    transition_keys = {
        "A_regsol": ["Omega", "Omega_over_RT", "Q", "U", "two_phase", "w", "x_binodal"],
        "B_gallery": ["Q", "U", "w"], "C_skew": ["Q", "U", "alpha", "w"],
    }
    metric_keys = ["BIC", "R2", "area_data", "area_model", "bg", "npar",
                   "peakRMSE", "valleyRMSE"]
    rows = []
    for route, path in SAVED_PATHS.items():
        raw = baseline_bytes(path)
        value, _, _ = strict_load(raw, path)
        require(set(value) == {"material", "kernel", "N", "metrics", "transitions"},
                "E_SAVED_TOP", route)
        require(type(value["material"]) is str and type(value["kernel"]) is str
                and type(value["N"]) is int and value["N"] == len(value["transitions"]),
                "E_SAVED_TOP_TYPES", route)
        require(sorted(value["metrics"]) == metric_keys
                and type(value["metrics"]["npar"]) is int
                and all(type(entry) is float for key, entry in value["metrics"].items()
                        if key != "npar"), "E_SAVED_METRIC_TYPES", route)
        require(all(isinstance(item, dict) and sorted(item) == transition_keys[route]
                    for item in value["transitions"]), "E_SAVED_TRANSITION_KEYS", route)
        for item in value["transitions"]:
            for key, entry in item.items():
                require(type(entry) is (bool if key == "two_phase" else float),
                        "E_SAVED_TRANSITION_TYPE", f"{route}:{key}")
                if type(entry) is float:
                    require(math.isfinite(entry), "E_SAVED_TRANSITION_FINITE", f"{route}:{key}")
        tree_text = gtext(("ls-tree", BASELINE, "--", path))
        meta, actual_path = tree_text.split("\t", 1)
        mode, kind, tree_oid = meta.split()
        oid = gtext(("rev-parse", f"{BASELINE}:{path}"))
        require((mode, kind, actual_path, tree_oid) == ("100644", "blob", path, oid),
                "E_SAVED_TREE", route)
        rows.append({
            "route": route, "path": path, "blob_oid": oid, "git_mode": mode,
            "raw_sha256": sha256(raw), "top_keys": sorted(value),
            "material": value["material"], "kernel": value["kernel"], "N": value["N"],
            "transition_count": len(value["transitions"]),
            "transition_keysets": [sorted(item) for item in value["transitions"]],
            "transition_value_types": [{key: type(entry).__name__
                                        for key, entry in sorted(item.items())}
                                       for item in value["transitions"]],
            "finite_numeric_values": True, "metrics_keys": sorted(value["metrics"]),
            "metrics_value_types": {key: type(entry).__name__
                                    for key, entry in sorted(value["metrics"].items())},
            "metrics_values": value["metrics"],
            "canonical_roundtrip_sha256": sha256(canonical_bytes(value)),
            "strict_parse_canonical_dump_semantic_identity": True,
            "searched_loader_names_status": "GROUND_NOT_FOUND",
            "config_replay_authority": "CONFIG_GENEALOGY_ONLY",
        })
    require([(row["material"], row["kernel"], row["N"]) for row in rows] ==
            [("blend", "regsol", 8), ("blend", "logistic", 14),
             ("blend", "skew-logistic", 14)], "E_SAVED_IDENTITIES")
    return rows


MATRIX_KEYS = {
    "artifact", "schema_version", "phase", "step", "generated_date", "baseline_commit",
    "expected_parent", "branch", "expected_subject", "gate", "precommit_status",
    "containing_commit", "persistence_terminal", "result_first", "json_outputs_last",
    "inputs", "source_static", "complete_python_search", "production_occurrence_projection",
    "saved_profiles",
    "writer_evidence", "runtime_binding", "case_contract", "default_adjudication",
    "owner_resolution", "control_hashes", "source_policy", "validation", "authority",
    "semantic_sha256",
}
RUNTIME_KEYS = {
    "artifact", "schema_version", "phase", "step", "generated_date", "baseline_commit",
    "expected_parent", "branch", "expected_subject", "result_first", "json_outputs_last",
    "runtime_contract", "runs", "process_pair_records", "cross_runtime_behavior_equal",
    "aggregate", "authority",
    "semantic_sha256",
}

RUN_KEYS = {"python", "case_id", "invocation_ordinal", "isolated_child_invocation_id",
            "argv", "cwd", "exit_code", "timed_out", "stdout_sha256", "stderr_sha256",
            "stderr_empty", "stdout_is_canonical_observation", "observation"}
COMMON_OBSERVATION_KEYS = {"case_id", "fresh_first", "events", "runtime", "surfaces",
                           "observation_sha256"}
CASE_EXTRA_KEYS = {
    "C01_FRESH_BASELINE": {"ordinary_reimport_same_object", "from_wt_q_gr_default"},
    "C02_EXPLICIT_PROFILE": {"explicit_counts"},
    "C03_SKEW_REBIND_EXISTING_FUTURE": {"existing_counts_after_rebind",
        "future_counts_after_rebind", "existing_si_identity_stable",
        "future_si_is_copied_from_default"},
    "C04_INPLACE_TRANSITION_ALIAS": {"existing_before", "existing_after_inplace",
                                      "future_after_inplace"},
    "C05_SI_REBIND_SEED_CACHE": {"legacy_before", "si_after_true", "legacy_after_false",
        "R_SI", "F_SI", "legacy_R", "legacy_F", "imported_scalar_alias_after_true",
        "dynamic_width_after_true", "existing_seed_before", "existing_seed_after_true",
        "existing_seed_unchanged", "future_seed_under_si", "future_seed_differs_from_existing"},
    "C06_ORDINARY_IMPORT_CACHE": {"same_module_object"},
    "C07_EXPLICIT_RELOAD": {"same_module_object", "module_dict_reexecuted_defaults_reset",
        "existing_transition_identity_stable", "existing_counts_after_reload",
        "existing_seed_after_reload", "existing_seed_unchanged", "existing_seed_before_reload"},
    "C08_TWO_SPEC_LOAD_OBJECTS": {"distinct_objects", "a_after_toggle",
                                   "b_independent_fresh"},
    "C09_NEW_PROCESS_RESET": {"fresh_isolated_process", "paired_prior_case_id"},
    "C10_TOGGLE_ORDER_A": {"existing_seed_unchanged", "existing_counts", "future_counts",
                             "future_seed", "final_constants"},
    "C11_TOGGLE_ORDER_B": {"existing_seed_unchanged", "existing_counts", "future_counts",
                             "future_seed", "final_constants"},
    "C12_ALIAS_EXPORT_GNF": {"searched_absent_names", "all_absent", "present_toggle_names"},
    "C13_SAVED_ROUTE_GNF": {"saved_routes", "searched_loader_names_absent"},
}
EVENT_KEYS = {"label", "counts", "graphite_legacy", "graphite_seed_L_V",
              "graphite_skew", "si_none", "si_skew", "constants"}
COUNT_KEYS = {"graphite", "silicon", "total"}
CONSTANT_KEYS = {"R", "F", "R_is_legacy", "F_is_legacy", "R_is_si", "F_is_si",
                 "width_298"}
SURFACE_KEYS = {"load_profile", "from_profile", "PROFILE_ALIASES", "SAVED_PROFILES",
                "__all__", "use_legacy_4transition", "use_skew7_default",
                "use_si_constants", "R_SI", "F_SI"}
C13_ROW_KEYS = {"route", "path", "blob_oid", "git_mode", "raw_sha256", "material",
                "kernel", "N", "transition_count", "top_keys", "metrics_keys",
                "metrics_value_types", "transition_keysets", "transition_value_types",
                "canonical_sha256", "strict_parse_canonical_dump_semantic_identity",
                "constructor_injection_accepted", "kernel_metadata_dispatched",
                "production_loader_used", "config_replay_authority"}
LEGACY_CONSTANTS = {"R": 8.314, "F": 96485.0, "R_is_legacy": True,
                    "F_is_legacy": True, "R_is_si": False, "F_is_si": False,
                    "width_298": 0.025691238016271958}
SI_CONSTANTS = {"R": 8.314462618, "F": 96485.33212, "R_is_legacy": False,
                "F_is_legacy": False, "R_is_si": True, "F_is_si": True,
                "width_298": 0.025692579121493725}
LEGACY_SEED = [4.914568556909695e-08, 1.4651392128230395e-08,
               4.367896974259587e-09, 4.749637433599175e-10]
SI_SEED = [4.909606952880419e-08, 1.4637586156098104e-08,
           4.364074976541478e-09, 4.746067291517e-10]
SURFACE_VALUES = {"load_profile": False, "from_profile": False,
                  "PROFILE_ALIASES": False, "SAVED_PROFILES": False,
                  "__all__": False, "use_legacy_4transition": False,
                  "use_skew7_default": True, "use_si_constants": True,
                  "R_SI": True, "F_SI": True}
RUNTIME_VERSIONS = {"3.12": [3, 12, 10], "3.14": [3, 14, 4]}


def expected_event(label: str) -> dict[str, Any] | None:
    fresh = {"counts": {"graphite": 4, "silicon": 2, "total": 6},
             "graphite_legacy": True, "graphite_skew": False,
             "si_none": True, "si_skew": False,
             "constants": LEGACY_CONSTANTS, "graphite_seed_L_V": LEGACY_SEED}
    skew_legacy = {"counts": {"graphite": 7, "silicon": 7, "total": 14},
                   "graphite_legacy": False, "graphite_skew": True,
                   "si_none": False, "si_skew": True,
                   "constants": LEGACY_CONSTANTS, "graphite_seed_L_V": [0.0] * 7}
    skew_si = {**skew_legacy, "constants": SI_CONSTANTS}
    si_only = {**fresh, "constants": SI_CONSTANTS, "graphite_seed_L_V": SI_SEED}
    mapping = {
        "fresh_before_mutation": fresh, "globals_unchanged": fresh,
        "after_reload_reset": fresh, "b_fresh": fresh,
        "future_after_rebind": skew_legacy, "ordinary_reimport_mutated": skew_legacy,
        "a_mutated": skew_legacy, "skew_then": skew_legacy,
        "before_reload": skew_si, "si_then_skew": skew_si, "skew_then_si": skew_si,
        "si_then": si_only,
    }
    return None if label not in mapping else {"label": label, **mapping[label]}


def expected_case_specific(case: str) -> dict[str, Any]:
    values: dict[str, dict[str, Any]] = {
        "C01_FRESH_BASELINE": {
            "ordinary_reimport_same_object": True, "from_wt_q_gr_default": 372.0},
        "C02_EXPLICIT_PROFILE": {
            "explicit_counts": {"graphite": 7, "silicon": 7, "total": 14}},
        "C03_SKEW_REBIND_EXISTING_FUTURE": {
            "existing_counts_after_rebind": {"graphite": 4, "silicon": 2, "total": 6},
            "future_counts_after_rebind": {"graphite": 7, "silicon": 7, "total": 14},
            "existing_si_identity_stable": True, "future_si_is_copied_from_default": True},
        "C04_INPLACE_TRANSITION_ALIAS": {
            "existing_before": {"graphite": 4, "silicon": 2, "total": 6},
            "existing_after_inplace": {"graphite": 5, "silicon": 2, "total": 6},
            "future_after_inplace": {"graphite": 5, "silicon": 2, "total": 7}},
        "C05_SI_REBIND_SEED_CACHE": {
            "legacy_before": LEGACY_CONSTANTS, "si_after_true": SI_CONSTANTS,
            "legacy_after_false": LEGACY_CONSTANTS, "R_SI": 8.314462618,
            "F_SI": 96485.33212, "legacy_R": 8.314, "legacy_F": 96485.0,
            "imported_scalar_alias_after_true": {"R": 8.314, "F": 96485.0,
                                                   "follows_rebind": False},
            "dynamic_width_after_true": 0.025692579121493725,
            "existing_seed_before": LEGACY_SEED, "existing_seed_after_true": LEGACY_SEED,
            "existing_seed_unchanged": True, "future_seed_under_si": SI_SEED,
            "future_seed_differs_from_existing": True},
        "C06_ORDINARY_IMPORT_CACHE": {"same_module_object": True},
        "C07_EXPLICIT_RELOAD": {
            "same_module_object": True, "module_dict_reexecuted_defaults_reset": True,
            "existing_transition_identity_stable": True,
            "existing_counts_after_reload": {"graphite": 4, "silicon": 2, "total": 6},
            "existing_seed_before_reload": LEGACY_SEED,
            "existing_seed_after_reload": LEGACY_SEED, "existing_seed_unchanged": True},
        "C08_TWO_SPEC_LOAD_OBJECTS": {
            "distinct_objects": True, "a_after_toggle": expected_event("a_mutated"),
            "b_independent_fresh": expected_event("b_fresh")},
        "C09_NEW_PROCESS_RESET": {
            "fresh_isolated_process": expected_event("fresh_before_mutation"),
            "paired_prior_case_id": "C06_ORDINARY_IMPORT_CACHE"},
        "C10_TOGGLE_ORDER_A": {
            "existing_seed_unchanged": True,
            "existing_counts": {"graphite": 4, "silicon": 2, "total": 6},
            "future_counts": {"graphite": 7, "silicon": 7, "total": 14},
            "future_seed": [0.0] * 7, "final_constants": SI_CONSTANTS},
        "C11_TOGGLE_ORDER_B": {
            "existing_seed_unchanged": True,
            "existing_counts": {"graphite": 4, "silicon": 2, "total": 6},
            "future_counts": {"graphite": 7, "silicon": 7, "total": 14},
            "future_seed": [0.0] * 7, "final_constants": SI_CONSTANTS},
        "C12_ALIAS_EXPORT_GNF": {
            "searched_absent_names": ["load_profile", "from_profile", "PROFILE_ALIASES",
                                      "SAVED_PROFILES", "__all__", "use_legacy_4transition"],
            "all_absent": True,
            "present_toggle_names": ["use_skew7_default", "use_si_constants", "R_SI", "F_SI"]},
        "C13_SAVED_ROUTE_GNF": {"searched_loader_names_absent": True},
    }
    require(case in values, "E_CASE_SPECIFIC_EXPECTED", case)
    return values[case]


def runtime_schema_errors(runtime: dict[str, Any], matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    def test(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)
    runs = runtime.get("runs")
    test(isinstance(runs, list) and len(runs) == 26, "E_RUNTIME_RUN_COUNT")
    if not isinstance(runs, list):
        return errors
    saved_by_route = {row.get("route"): row for row in matrix.get("saved_profiles", [])
                      if isinstance(row, dict)}
    for index, run in enumerate(runs):
        version = "3.12" if index < 13 else "3.14"
        ordinal = index % 13 + 1
        case = CASE_IDS[ordinal - 1]
        test(isinstance(run, dict) and set(run) == RUN_KEYS, f"E_RUN_KEYS:{index}")
        if not isinstance(run, dict):
            continue
        expected_argv = ["py", f"-{version}", "-B", "-I", "-X", "utf8", "<PROBE>",
                         "<SOURCE_DIR>", case, "<SAVED_DIR>"]
        test(run.get("python") == version and run.get("case_id") == case
             and type(run.get("invocation_ordinal")) is int
             and run.get("invocation_ordinal") == ordinal
             and run.get("isolated_child_invocation_id") == f"PY{version}-C{ordinal:02d}"
             and run.get("argv") == expected_argv, f"E_RUN_IDENTITY:{index}")
        test(run.get("cwd") == "<DISPOSABLE_ROOT>"
             and type(run.get("exit_code")) is int and run.get("exit_code") == 0
             and run.get("timed_out") is False and run.get("stderr_empty") is True
             and run.get("stderr_sha256") == sha256(b"")
             and run.get("stdout_is_canonical_observation") is True,
             f"E_RUN_PROCESS:{index}")
        observation = run.get("observation")
        expected_keys = COMMON_OBSERVATION_KEYS | CASE_EXTRA_KEYS[case]
        test(isinstance(observation, dict) and set(observation) == expected_keys,
             f"E_OBSERVATION_KEYS:{case}")
        if not isinstance(observation, dict):
            continue
        test(observation.get("case_id") == case and observation.get("fresh_first") is True,
             f"E_OBSERVATION_IDENTITY:{case}")
        expected_specific = expected_case_specific(case)
        test(typed_equal({key: observation.get(key) for key in expected_specific},
                         expected_specific),
             f"E_CASE_SPECIFIC_EXACT:{case}")
        test(run.get("stdout_sha256") == sha256(canonical_bytes(observation)),
             f"E_STDOUT_BINDING:{case}")
        runtime_id = observation.get("runtime")
        test(isinstance(runtime_id, dict) and set(runtime_id) == {"implementation", "version", "pid"}
             and runtime_id.get("implementation") == "cpython"
             and typed_equal(runtime_id.get("version"), RUNTIME_VERSIONS[version])
             and type(runtime_id.get("pid")) is int and runtime_id.get("pid", 0) > 0,
             f"E_RUNTIME_ID:{case}")
        surfaces = observation.get("surfaces")
        test(isinstance(surfaces, dict) and set(surfaces) == SURFACE_KEYS
             and typed_equal(surfaces, SURFACE_VALUES),
             f"E_SURFACE_KEYS:{case}")
        events = observation.get("events")
        test(isinstance(events, list) and bool(events), f"E_EVENT_LIST:{case}")
        if isinstance(events, list):
            for event_index, event in enumerate(events):
                test(isinstance(event, dict) and set(event) == EVENT_KEYS,
                     f"E_EVENT_KEYS:{case}:{event_index}")
                if not isinstance(event, dict):
                    continue
                test(isinstance(event.get("counts"), dict)
                     and set(event["counts"]) == COUNT_KEYS,
                     f"E_COUNT_KEYS:{case}:{event_index}")
                test(isinstance(event.get("constants"), dict)
                     and set(event["constants"]) == CONSTANT_KEYS,
                     f"E_CONSTANT_KEYS:{case}:{event_index}")
                test(isinstance(event.get("graphite_seed_L_V"), list)
                     and all(type(value) is float and math.isfinite(value)
                             for value in event.get("graphite_seed_L_V", [])),
                     f"E_EVENT_SEED:{case}:{event_index}")
                test(typed_equal(event, expected_event(str(event.get("label")))),
                     f"E_EVENT_EXACT:{case}:{event_index}")
        for key in ("explicit_counts", "existing_counts_after_rebind",
                    "future_counts_after_rebind", "existing_before", "existing_after_inplace",
                    "future_after_inplace", "existing_counts_after_reload", "existing_counts",
                    "future_counts"):
            if key in observation:
                test(isinstance(observation[key], dict) and set(observation[key]) == COUNT_KEYS,
                     f"E_SPECIAL_COUNT:{case}:{key}")
        for key in ("legacy_before", "si_after_true", "legacy_after_false", "final_constants"):
            if key in observation:
                test(isinstance(observation[key], dict) and set(observation[key]) == CONSTANT_KEYS,
                     f"E_SPECIAL_CONSTANT:{case}:{key}")
        if case == "C08_TWO_SPEC_LOAD_OBJECTS":
            for key in ("a_after_toggle", "b_independent_fresh"):
                test(isinstance(observation.get(key), dict)
                     and set(observation[key]) == EVENT_KEYS
                     and typed_equal(observation[key],
                                     expected_event(str(observation[key].get("label")))),
                     f"E_C08_EVENT:{key}")
        if case == "C09_NEW_PROCESS_RESET":
            test(isinstance(observation.get("fresh_isolated_process"), dict)
                 and set(observation["fresh_isolated_process"]) == EVENT_KEYS
                 and typed_equal(observation["fresh_isolated_process"],
                                 expected_event("fresh_before_mutation")),
                 "E_C09_FRESH_EVENT")
        if case == "C13_SAVED_ROUTE_GNF":
            rows = observation.get("saved_routes")
            test(isinstance(rows, list) and len(rows) == 3, "E_C13_ROWS")
            if isinstance(rows, list):
                for row in rows:
                    test(isinstance(row, dict) and set(row) == C13_ROW_KEYS, "E_C13_ROW_KEYS")
                    if not isinstance(row, dict):
                        continue
                    source = saved_by_route.get(row.get("route"), {})
                    expected = {
                        "route": source.get("route"), "path": source.get("path"),
                        "blob_oid": source.get("blob_oid"), "git_mode": source.get("git_mode"),
                        "raw_sha256": source.get("raw_sha256"), "material": source.get("material"),
                        "kernel": source.get("kernel"), "N": source.get("N"),
                        "transition_count": source.get("transition_count"),
                        "top_keys": source.get("top_keys"), "metrics_keys": source.get("metrics_keys"),
                        "metrics_value_types": source.get("metrics_value_types"),
                        "transition_keysets": source.get("transition_keysets"),
                        "transition_value_types": source.get("transition_value_types"),
                        "canonical_sha256": source.get("canonical_roundtrip_sha256"),
                        "strict_parse_canonical_dump_semantic_identity": True,
                        "constructor_injection_accepted": True,
                        "kernel_metadata_dispatched": False, "production_loader_used": False,
                        "config_replay_authority": "CONFIG_GENEALOGY_ONLY",
                    }
                    test(typed_equal(row, expected), f"E_C13_EXACT:{row.get('route')}")
    return errors


def artifact_errors(matrix: dict[str, Any], runtime: dict[str, Any],
                    predecessors: dict[str, dict[str, Any]],
                    input_rows: list[dict[str, Any]],
                    independent: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    def check(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)
    check(set(matrix) == MATRIX_KEYS, "E_MATRIX_SCHEMA")
    check(set(runtime) == RUNTIME_KEYS, "E_RUNTIME_SCHEMA")
    check(matrix.get("artifact") == "PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX", "E_MATRIX_ARTIFACT")
    check(runtime.get("artifact") == "PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION", "E_RUNTIME_ARTIFACT")
    check(matrix.get("schema_version") == "phase067-step85-default-import-v1",
          "E_MATRIX_SCHEMA_VERSION")
    check(runtime.get("schema_version") == "phase067-step85-runtime-v1",
          "E_RUNTIME_SCHEMA_VERSION")
    metadata = [67, 85, "2026-09-02", BASELINE, EXPECTED_PARENT, BRANCH, EXPECTED_SUBJECT]
    check(typed_equal([matrix.get(key) for key in ("phase", "step", "generated_date", "baseline_commit",
                                                    "expected_parent", "branch", "expected_subject")], metadata),
          "E_MATRIX_METADATA")
    check(typed_equal([runtime.get(key) for key in ("phase", "step", "generated_date", "baseline_commit",
                                                     "expected_parent", "branch", "expected_subject")], metadata),
          "E_RUNTIME_METADATA")
    check(matrix.get("gate") == GATE and matrix.get("precommit_status") == "PASS_PENDING_PERSISTENCE"
          and matrix.get("containing_commit") == "PENDING_AT_PRECOMMIT_BY_DESIGN"
          and matrix.get("persistence_terminal") == PERSISTENCE, "E_GATE")
    check(matrix.get("result_first") is True and matrix.get("json_outputs_last") is True
          and runtime.get("result_first") is True and runtime.get("json_outputs_last") is True,
          "E_GENERATION_ORDER")
    check(typed_equal(matrix.get("inputs"), input_rows), "E_INPUT_BINDING")
    check(matrix.get("semantic_sha256") == semantic_sha(matrix), "E_MATRIX_SEMANTIC")
    check(runtime.get("semantic_sha256") == semantic_sha(runtime), "E_RUNTIME_SEMANTIC")
    check(typed_equal(matrix.get("control_hashes"), CONTROL_PINS), "E_CONTROL_BINDING")
    check(typed_equal(matrix.get("source_policy"), {
        "builder_neutral_sha256": BUILDER_SOURCE_POLICY_SHA256_LF,
        "validator_neutral_sha256": VALIDATOR_SOURCE_POLICY_SHA256_LF,
    }), "E_SOURCE_POLICY_BINDING")

    if independent is None:
        writer_raw_value = baseline_bytes(WRITER_PATH)
        writer_tree_value = ast.parse(writer_raw_value.decode("utf-8"), filename=WRITER_PATH)
        independent = {
            "static": expected_source_static(),
            "search": independent_blob_search(predecessors[INVENTORY_PATH]),
            "production": independent_production_projection(predecessors[INVENTORY_PATH]),
            "saved": independent_saved_profiles(),
            "writer_raw": writer_raw_value,
            "writer_calls": [node for node in ast.walk(writer_tree_value)
                if isinstance(node, ast.Call)
                and ("write" in ast.unparse(node.func) or "dump" in ast.unparse(node.func))
                and ("params" in ast.unparse(node) or "json" in ast.unparse(node).lower())],
        }
    static = independent["static"]
    stored_static = matrix.get("source_static", {})
    check(typed_equal(stored_static, static["artifact"]), "E_SOURCE_STATIC_EXACT")
    stored_values = {row.get("name"): row.get("value_expression")
                     for row in stored_static.get("assignment_rows", [])}
    check(typed_equal(stored_values, static["assignment_values"]), "E_DEFAULT_ASSIGNMENTS")
    check(typed_equal(stored_static.get("absent_surfaces"), static["absent_surfaces"]),
          "E_ABSENT_SURFACES")
    check(stored_static.get("from_wt_q_gr_default", {}).get("expression") ==
          static["from_wt_default_expression"]
          and type(stored_static.get("from_wt_q_gr_default", {}).get("runtime_bound_value")) is float
          and stored_static.get("from_wt_q_gr_default", {}).get("runtime_bound_value") == 372.0,
          "E_QGR_DEFAULT")
    check(typed_equal(stored_static.get("si_constants_toggle", {}).get("legacy"),
                      {"R": 8.314, "F": 96485.0})
          and typed_equal(stored_static.get("si_constants_toggle", {}).get("si"),
                          {"R": 8.314462618, "F": 96485.33212})
          and "global R, F" in static["si_toggle_ast"], "E_SI_CONSTANT_STATIC")

    search_digest, matched_rows = independent["search"]
    stored_search = matrix.get("complete_python_search", {})
    check(all(type(stored_search.get(key)) is int for key in
              ("searched_occurrences", "searched_unique_python_blobs", "ast_parse_pass"))
          and stored_search.get("searched_occurrences") == 129
          and stored_search.get("searched_unique_python_blobs") == 84
          and stored_search.get("ast_parse_pass") == 84, "E_SEARCH_COUNTS")
    check(stored_search.get("all_blob_projection_sha256") == search_digest
          and typed_equal(stored_search.get("matched_blob_rows"), matched_rows),
          "E_SEARCH_PROJECTION")
    check(stored_search.get("searched_exact_names_status") == "GROUND_NOT_FOUND"
          and stored_search.get("searched_exact_names_matches") == [], "E_LOADER_GNF")

    expected_production = independent["production"]
    check(typed_equal(matrix.get("production_occurrence_projection"), expected_production),
          "E_PRODUCTION_OCCURRENCE_PROJECTION")

    saved = matrix.get("saved_profiles", [])
    check(typed_equal(saved, independent["saved"]), "E_SAVED_EXACT_PROJECTION")

    writer = matrix.get("writer_evidence", {})
    writer_raw = independent["writer_raw"]
    writer_calls = independent["writer_calls"]
    writer_text = writer_raw.decode("utf-8")
    expected_writer = {
        "path": WRITER_PATH,
        "blob_oid": gtext(("rev-parse", f"{BASELINE}:{WRITER_PATH}")),
        "raw_sha256": sha256(writer_raw),
        "write_anchors": [source_anchor(WRITER_PATH, writer_text, node, "<static-owner>")
                          for node in writer_calls],
        "saved_profile_loader_anchors": [],
        "classification": "WRITER_EVIDENCE_NOT_PRODUCTION_LOADER",
    }
    check(len(writer_calls) == 2 and typed_equal(writer, expected_writer),
          "E_WRITER_NOT_LOADER")

    check(set(stored_static) == {"path", "blob_oid", "raw_sha256", "physical_lines",
          "ast_parse", "assignment_rows", "toggle", "si_constants_toggle",
          "constructor_default_load", "from_wt_q_gr_default", "absent_surfaces",
          "header_docstring_conflict"}, "E_SOURCE_STATIC_SCHEMA")
    check(stored_static.get("path") == SOURCE_PATH
          and stored_static.get("blob_oid") == gtext(("rev-parse", f"{BASELINE}:{SOURCE_PATH}"))
          and typed_equal(stored_static.get("header_docstring_conflict"), {
              "status": "STALE_PROSE_CONFLICT_EXECUTABLE_ASSIGNMENT_WINS",
              "runtime_adjudication": "STEP85_FRESH_ISOLATED_PROCESS",
          }), "E_SOURCE_STATIC_EXACT")
    check(isinstance(stored_static.get("assignment_rows"), list)
          and len(stored_static["assignment_rows"]) == 8
          and all(set(row) == {"name", "value_expression", "anchor"}
                  and set(row.get("anchor", {})) == {"path", "qualified_owner", "ast_kind",
                      "start_line", "end_line", "source_sha256", "ast_sha256"}
                  and type(row["anchor"].get("start_line")) is int
                  and type(row["anchor"].get("end_line")) is int
                  for row in stored_static["assignment_rows"]), "E_SOURCE_ASSIGNMENT_SCHEMA")
    check(set(stored_search) == {"search_names", "searched_occurrences",
          "searched_unique_python_blobs", "ast_parse_pass", "all_blob_projection_sha256",
          "matched_blob_rows", "searched_exact_names_status",
          "searched_exact_names_matches"}
          and typed_equal(stored_search.get("search_names"), ["load_profile", "from_profile",
              "PROFILE_ALIASES", "SAVED_PROFILES", "__all__", "use_legacy_4transition",
              "use_skew7_default", "use_si_constants", "R_SI", "F_SI", "_R_LEGACY",
              "_F_LEGACY"]), "E_SEARCH_SCHEMA")

    check(typed_equal(matrix.get("case_contract"), CASE_CONTRACT), "E_CASE_CONTRACT")
    for code in runtime_schema_errors(runtime, matrix):
        check(False, code)
    runs = runtime.get("runs", [])
    by_version = {version: {run["case_id"]: run["observation"] for run in runs
                            if run["python"] == version} for version in ("3.12", "3.14")}
    behavior = {}
    for version, rows in by_version.items():
        behavior[version] = {}
        for case, observation in rows.items():
            clone = copy.deepcopy(observation)
            clone.pop("runtime", None)
            stored_hash = clone.pop("observation_sha256", None)
            check(stored_hash == sha256(canonical_bytes(clone).rstrip(b"\n")),
                  f"E_OBSERVATION_SHA:{version}:{case}")
            clone["observation_sha256"] = stored_hash
            behavior[version][case] = clone
    check(typed_equal(behavior.get("3.12"), behavior.get("3.14"))
          and runtime.get("cross_runtime_behavior_equal") is True, "E_RUNTIME_CROSS")
    if set(behavior.get("3.12", {})) == set(CASE_IDS):
        p = behavior["3.12"]
        check(typed_equal(p["C01_FRESH_BASELINE"]["events"][0]["counts"],
                          {"graphite": 4, "silicon": 2, "total": 6}), "E_FRESH_DEFAULT")
        check(typed_equal(p["C02_EXPLICIT_PROFILE"]["explicit_counts"],
                          {"graphite": 7, "silicon": 7, "total": 14})
              and typed_equal(p["C02_EXPLICIT_PROFILE"]["events"][-1]["counts"],
                              {"graphite": 4, "silicon": 2, "total": 6}),
              "E_EXPLICIT_NONMUTATING")
        c03 = p["C03_SKEW_REBIND_EXISTING_FUTURE"]
        check(typed_equal(c03["existing_counts_after_rebind"], {"graphite": 4, "silicon": 2, "total": 6})
              and typed_equal(c03["future_counts_after_rebind"], {"graphite": 7, "silicon": 7, "total": 14})
              and c03["existing_si_identity_stable"] is True
              and c03["future_si_is_copied_from_default"] is True, "E_REBIND")
        c04 = p["C04_INPLACE_TRANSITION_ALIAS"]
        check(typed_equal(c04["existing_before"], {"graphite": 4, "silicon": 2, "total": 6})
              and typed_equal(c04["existing_after_inplace"], {"graphite": 5, "silicon": 2, "total": 6})
              and typed_equal(c04["future_after_inplace"], {"graphite": 5, "silicon": 2, "total": 7}),
              "E_ALIAS_INPLACE")
        c05 = p["C05_SI_REBIND_SEED_CACHE"]
        check(typed_equal(c05["legacy_R"], 8.314) and typed_equal(c05["legacy_F"], 96485.0)
              and typed_equal(c05["R_SI"], 8.314462618) and typed_equal(c05["F_SI"], 96485.33212)
              and c05["legacy_before"]["R_is_legacy"] is True
              and c05["si_after_true"]["R_is_si"] is True
              and c05["si_after_true"]["F_is_si"] is True
              and c05["legacy_after_false"]["R_is_legacy"] is True
              and c05["legacy_after_false"]["F_is_legacy"] is True
              and typed_equal(c05["dynamic_width_after_true"], c05["si_after_true"]["width_298"])
              and typed_equal(c05["existing_seed_before"], LEGACY_SEED)
              and typed_equal(c05["existing_seed_after_true"], LEGACY_SEED)
              and c05["existing_seed_unchanged"] is True
              and typed_equal(c05["future_seed_under_si"], SI_SEED)
              and c05["future_seed_differs_from_existing"] is True
              and typed_equal(c05["imported_scalar_alias_after_true"], {
                  "R": 8.314, "F": 96485.0, "follows_rebind": False}), "E_SI_REBIND_SEED")
        check(typed_equal(p["C06_ORDINARY_IMPORT_CACHE"]["events"][-1]["counts"]["total"], 14),
              "E_IMPORT_CACHE")
        c07 = p["C07_EXPLICIT_RELOAD"]
        check(c07["same_module_object"] is True
              and c07["module_dict_reexecuted_defaults_reset"] is True
              and typed_equal(c07["events"][-1]["counts"], {"graphite": 4, "silicon": 2, "total": 6})
              and c07["existing_transition_identity_stable"] is True
              and typed_equal(c07["existing_counts_after_reload"], {"graphite": 4, "silicon": 2, "total": 6})
              and typed_equal(c07["existing_seed_before_reload"], c07["existing_seed_after_reload"])
              and c07["existing_seed_unchanged"] is True, "E_RELOAD_EXISTING")
        check(typed_equal(p["C08_TWO_SPEC_LOAD_OBJECTS"]["a_after_toggle"]["counts"]["total"], 14)
              and typed_equal(p["C08_TWO_SPEC_LOAD_OBJECTS"]["b_independent_fresh"]["counts"]["total"], 6),
              "E_SPEC_OBJECTS")
        c09 = p["C09_NEW_PROCESS_RESET"]
        check(typed_equal(c09["fresh_isolated_process"]["counts"],
                          {"graphite": 4, "silicon": 2, "total": 6})
              and c09["paired_prior_case_id"] == "C06_ORDINARY_IMPORT_CACHE",
              "E_FRESH_PROCESS")
        c10, c11 = p["C10_TOGGLE_ORDER_A"], p["C11_TOGGLE_ORDER_B"]
        check(typed_equal([event["label"] for event in c10["events"]],
                          ["fresh_before_mutation", "si_then", "si_then_skew"])
              and typed_equal([event["label"] for event in c11["events"]],
                              ["fresh_before_mutation", "skew_then", "skew_then_si"])
              and c10["existing_seed_unchanged"] is True
              and c11["existing_seed_unchanged"] is True
              and typed_equal(c10["existing_counts"], {"graphite": 4, "silicon": 2, "total": 6})
              and typed_equal(c11["existing_counts"], {"graphite": 4, "silicon": 2, "total": 6})
              and typed_equal(c10["future_counts"], {"graphite": 7, "silicon": 7, "total": 14})
              and typed_equal(c11["future_counts"], {"graphite": 7, "silicon": 7, "total": 14})
              and typed_equal(c10["future_seed"], c11["future_seed"])
              and typed_equal(c10["final_constants"], c11["final_constants"])
              and c10["final_constants"]["R_is_si"] is True, "E_TOGGLE_ORDER_CROSS")
        c12 = p["C12_ALIAS_EXPORT_GNF"]
        check(typed_equal(c12["searched_absent_names"], ["load_profile", "from_profile",
              "PROFILE_ALIASES", "SAVED_PROFILES", "__all__", "use_legacy_4transition"]
              ) and typed_equal(c12["present_toggle_names"],
              ["use_skew7_default", "use_si_constants", "R_SI", "F_SI"])
              and c12["all_absent"] is True, "E_ALIAS_EXPORT_RUNTIME")
        check(typed_equal([row["transition_count"] for row in p["C13_SAVED_ROUTE_GNF"]["saved_routes"]],
                          [8, 14, 14])
              and p["C13_SAVED_ROUTE_GNF"]["searched_loader_names_absent"] is True,
              "E_SAVED_RUNTIME")
    contract = runtime.get("runtime_contract", {})
    check(typed_equal(contract, {"controller_imported_production": False,
          "child_process_isolation": "-B -I -X utf8", "network_used": False,
          "repository_runtime_cwd": False, "persistent_cache_written": False,
          "disposable_cleanup_completed": True, "case_sequence": list(CASE_IDS),
          "bounded_no_cartesian_permutations": True}), "E_RUNTIME_CONTRACT")
    pairs = runtime.get("process_pair_records")
    pair_keys = {"python", "mutated_case", "mutated_invocation_id", "mutated_pid",
                 "mutated_total", "fresh_case", "fresh_invocation_id", "fresh_pid",
                 "fresh_total", "pid_distinct"}
    check(isinstance(pairs, list) and len(pairs) == 2
          and all(isinstance(row, dict) and set(row) == pair_keys for row in pairs),
          "E_PROCESS_PAIR_SCHEMA")
    if isinstance(pairs, list) and len(pairs) == 2:
        run_map = {(run.get("python"), run.get("case_id")): run for run in runs}
        for index, version in enumerate(("3.12", "3.14")):
            row = pairs[index]
            c06 = run_map.get((version, "C06_ORDINARY_IMPORT_CACHE"), {})
            c09 = run_map.get((version, "C09_NEW_PROCESS_RESET"), {})
            expected_pair = {
                "python": version, "mutated_case": "C06_ORDINARY_IMPORT_CACHE",
                "mutated_invocation_id": c06.get("isolated_child_invocation_id"),
                "mutated_pid": c06.get("observation", {}).get("runtime", {}).get("pid"),
                "mutated_total": c06.get("observation", {}).get("events", [{}])[-1].get("counts", {}).get("total"),
                "fresh_case": "C09_NEW_PROCESS_RESET",
                "fresh_invocation_id": c09.get("isolated_child_invocation_id"),
                "fresh_pid": c09.get("observation", {}).get("runtime", {}).get("pid"),
                "fresh_total": c09.get("observation", {}).get("fresh_isolated_process", {}).get("counts", {}).get("total"),
                "pid_distinct": True,
            }
            check(typed_equal(row, expected_pair)
                  and type(row.get("mutated_pid")) is int
                  and type(row.get("fresh_pid")) is int
                  and row.get("mutated_pid") != row.get("fresh_pid")
                  and type(row.get("mutated_total")) is int
                  and type(row.get("fresh_total")) is int
                  and row.get("mutated_total") == 14 and row.get("fresh_total") == 6,
                  f"E_PROCESS_PAIR:{version}")
    aggregate = runtime.get("aggregate", {})
    check(typed_equal(aggregate, {"interpreters": 2, "cases_per_interpreter": 13, "processes": 26,
                        "exit_zero": 26, "stderr_empty": 26, "timeouts": 0, "temp_leaks": 0},
          ), "E_RUNTIME_AGGREGATE")
    adjudication = matrix.get("default_adjudication", {})
    check(typed_equal(adjudication, {"fresh_executable_default": "GRAPHITE_STAGING_LIT_4_PLUS_SIC_LIT_2",
          "header_docstring_7_gallery_default_claim": "STALE_CONFLICT_NOT_EXECUTABLE_AUTHORITY",
          "use_legacy_4transition": "GROUND_NOT_FOUND",
          "use_skew7_default": "PRESENT_MUTABLE_GLOBAL_API",
          "from_wt_q_gr_default_bound_at_definition": 372.0,
          "test_mutated_state_is_fresh_public_default": False,
          "ordinary_reimport_resets_module_state": False,
          "explicit_reload_resets_module_state": True,
          "serialization_roundtrip_is_public_loader": False}), "E_DEFAULT_ADJUDICATION")
    owner = matrix.get("owner_resolution", {})
    carry = predecessors[P066_CARRY_PATH]
    obligation = next(row for row in carry["active_obligations"]
                      if row.get("obligation_id") == "P066-OBL-0125")
    observation = next(row for row in carry["step76_80_disposition_records"]
                       if row.get("observation_id") == "P066-R80-14")
    expected_owner = {"obligation_id": "P066-OBL-0125", "origin_identity": "P066-R80-14",
        "origin_record_sha256": observation["origin_record_sha256"],
        "prior_disposition": observation["evidence_identity_disposition"],
        "prior_state": observation["state"],
        "prior_serialized_disposition": observation["disposition"],
        "obligation_state": obligation["state"], "target_phase": obligation["target_phase"],
        "resolution": "BOUNDED_CONFIG_PARSE_CONSTRUCTOR_ACCEPTANCE_SEARCHED_EXACT_NAMES_GROUND_NOT_FOUND",
        "resolution_state": "BOUND_NOT_RESOLVED_OR_DISPATCHED",
        "owner": obligation["canonical_owner"],
        "external_authority_promoted": (obligation["external_authority_promoted"]
                                          or observation["external_authority_promoted"])}
    check(typed_equal(owner, expected_owner) and owner["prior_disposition"] == "PRESERVE"
          and owner["prior_serialized_disposition"] == "WITHHOLD"
          and owner["prior_state"] == owner["obligation_state"] == "OPEN_CARRY",
          "E_OWNER_EXACT")
    check(typed_equal(matrix.get("runtime_binding"), {"path": RUNTIME_PATH,
          "semantic_sha256": runtime.get("semantic_sha256"), "processes": 26,
          "cross_runtime_behavior_equal": True}), "E_RUNTIME_BINDING")
    check(typed_equal(matrix.get("validation"), {"step82_129_84_bound": True,
          "step83_and_step84_pinned": True, "production_source_ast": "PASS",
          "complete_python_loader_search_84_of_84": "PASS",
          "fresh_before_mutation": "PASS", "bounded_permutations": "PASS",
          "saved_schema_parse_dump_and_constructor_acceptance": "PASS",
          "owner_direct_binding": "PASS", "authority_promotions": 0,
          "required_absent_surface": "SEARCHED_EXACT_NAMES_GROUND_NOT_FOUND"}),
          "E_VALIDATION_EXACT")
    authority = matrix.get("authority", {})
    runtime_authority = runtime.get("authority", {})
    check(typed_equal(authority, {
        "source_static_defaults": True, "isolated_runtime_behavior": True,
        "config_genealogy": True, "general_test_behavior": False,
        "science": False, "material": False, "canonical_profile": False, "publication": False,
    }), "E_MATRIX_AUTHORITY")
    check(typed_equal(runtime_authority, {
        "isolated_runtime_behavior": True,
        "saved_config_semantic_parse_and_constructor_acceptance": True,
        "production_saved_loader": False, "original_optimizer_state": False,
        "scientific_truth": False, "material_validity": False,
        "canonical_profile": False, "publication_readiness": False,
    }), "E_RUNTIME_AUTHORITY")
    return errors


INDEPENDENT_PROBE = r'''
from __future__ import annotations
import importlib, importlib.util, json, pathlib, sys
source=pathlib.Path(sys.argv[1]); saved=pathlib.Path(sys.argv[2]); sys.path.insert(0,str(source))
def fresh():
    sys.modules.pop('anode_fit_frozen',None)
    return importlib.import_module('anode_fit_frozen')
def spec(name):
    s=importlib.util.spec_from_file_location(name,source/'anode_fit_frozen.py')
    if s is None or s.loader is None: raise RuntimeError('loader')
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def model(m,**kw): return m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0,**kw)
def counts(x): return [len(x.gr_host.transitions),len(x.si_host.transitions)]
def seed(x): return [float(v) for v in x.gr_host.seed_L_V]
out={}
m=fresh(); out['C01']={'counts':counts(model(m)),'qgr':m.BlendedAnodeDQDV.from_wt.__func__.__defaults__[1]}
m=fresh(); x=model(m,graphite_transitions=m.GRAPHITE_MSMR7_LIT,si_transitions=m.SI_MSMR7_SKEW_LIT)
out['C02']={'explicit':counts(x),'fresh_after':counts(model(m))}
m=fresh(); old=model(m); old_si=id(old.si_host.transitions); m.use_skew7_default(True); new=model(m)
out['C03']={'old':counts(old),'new':counts(new),'old_si_stable':id(old.si_host.transitions)==old_si,
            'future_si_copy':id(new.si_host.transitions)!=id(m.SI_MSMR7_SKEW_LIT)}
m=fresh(); old=model(m); m.GRAPHITE_STAGING_LIT.append(dict(m.GRAPHITE_STAGING_LIT[-1])); out['C04']={'old':counts(old),'new':counts(model(m))}
m=fresh(); alias_R,alias_F=m.R,m.F; old=model(m); old_seed=seed(old); before_w=float(m.func_w(298.15))
m.use_si_constants(True); future=model(m); si_w=float(m.func_w(298.15)); after_seed=seed(old)
si=[m.R,m.F,m.R==m.R_SI,m.F==m.F_SI]; future_seed=seed(future); m.use_si_constants(False)
out['C05']={'legacy':[alias_R,alias_F,before_w], 'si':si+[si_w],
            'alias_static':[alias_R,alias_F], 'old_seed_stable':old_seed==after_seed,
            'future_seed_differs':future_seed!=old_seed, 'restored':[m.R,m.F]}
m=fresh(); m.use_skew7_default(True); again=importlib.import_module('anode_fit_frozen'); out['C06']={'same':again is m,'counts':counts(model(again))}
m=fresh(); old=model(m); old_ids=[id(old.gr_host.transitions),id(old.si_host.transitions)]; old_seed=seed(old)
m.use_skew7_default(True); m.use_si_constants(True); again=importlib.reload(m)
out['C07']={'same':again is m,'module':counts(model(again)), 'old':counts(old),
            'old_ids':old_ids==[id(old.gr_host.transitions),id(old.si_host.transitions)],
            'old_seed':old_seed==seed(old), 'legacy':[m.R,m.F]}
a=spec('step85_independent_a'); b=spec('step85_independent_b'); a.use_skew7_default(True); out['C08']={'distinct':a is not b,'a':counts(model(a)),'b':counts(model(b))}
m=fresh(); out['C09']={'counts':counts(model(m))}
m=fresh(); old=model(m); old_seed=seed(old); m.use_si_constants(True); m.use_skew7_default(True); future=model(m)
out['C10']={'old':counts(old),'future':counts(future),'old_seed':old_seed==seed(old),'future_seed':seed(future),'rf':[m.R,m.F]}
m=fresh(); old=model(m); old_seed=seed(old); m.use_skew7_default(True); m.use_si_constants(True); future=model(m)
out['C11']={'old':counts(old),'future':counts(future),'old_seed':old_seed==seed(old),'future_seed':seed(future),'rf':[m.R,m.F]}
m=fresh(); names=('load_profile','from_profile','PROFILE_ALIASES','SAVED_PROFILES','__all__','use_legacy_4transition'); out['C12']={'absent':all(not hasattr(m,n) for n in names)}
out['C13']={'counts':[],'canonical':[],'construct':[],'searched_names_absent':all(not hasattr(m,n) for n in names[:4])}
for route in ('A_regsol','B_gallery','C_skew'):
    raw=(saved/(route+'.json')).read_bytes(); value=json.loads(raw.decode('utf-8'))
    canonical=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
    out['C13']['counts'].append(len(value['transitions'])); out['C13']['canonical'].append(json.loads(canonical)==value)
    obj=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0,graphite_transitions=value['transitions'],si_transitions=None)
    out['C13']['construct'].append(len(obj.gr_host.transitions)==len(value['transitions']))
print(json.dumps({'runtime':{'implementation':sys.implementation.name,
                             'version':list(sys.version_info[:3])},'cases':out},
                 ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False))
'''


def independent_runtime(stored_runtime: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    root = Path(tempfile.mkdtemp(prefix="p067_step85_validator_"))
    cleanup = False
    outputs: dict[str, dict[str, Any]] = {}
    try:
        source_dir = root / "source"
        saved_dir = root / "saved"
        source_dir.mkdir()
        saved_dir.mkdir()
        (source_dir / "anode_fit_frozen.py").write_bytes(baseline_bytes(SOURCE_PATH))
        probe = root / "independent_probe.py"
        probe.write_text(INDEPENDENT_PROBE, encoding="utf-8", newline="\n")
        for route, path in SAVED_PATHS.items():
            (saved_dir / f"{route}.json").write_bytes(baseline_bytes(path))
        initial = {str(path.relative_to(root)): sha256(path.read_bytes())
                   for path in root.rglob("*") if path.is_file()}
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8",
               "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"}
        for version in ("3.12", "3.14"):
            cp = subprocess.run(("py", f"-{version}", "-B", "-I", "-X", "utf8",
                                 str(probe), str(source_dir), str(saved_dir)),
                                cwd=root, env=env, capture_output=True, shell=False,
                                check=False, timeout=180)
            require(cp.returncode == 0, "E_INDEPENDENT_RUNTIME_EXIT",
                    f"{version}:{cp.stderr.decode('utf-8', 'replace')[:400]}")
            require(cp.stderr == b"" and len(cp.stdout.splitlines()) == 1,
                    "E_INDEPENDENT_RUNTIME_STREAM", version)
            outputs[version], _, _ = strict_load(cp.stdout, "independent:" + version)
        final = {str(path.relative_to(root)): sha256(path.read_bytes())
                 for path in root.rglob("*") if path.is_file()}
        require(initial == final, "E_INDEPENDENT_TEMP_MUTATION")
        require(not any(path.suffix in {".pyc", ".pyo"} or path.name == "__pycache__"
                        for path in root.rglob("*")), "E_INDEPENDENT_CACHE_LEAK")
    finally:
        shutil.rmtree(root, ignore_errors=False)
        cleanup = not root.exists()
    require(cleanup, "E_INDEPENDENT_TEMP_CLEANUP")
    for version in ("3.12", "3.14"):
        require(set(outputs.get(version, {})) == {"runtime", "cases"},
                "E_INDEPENDENT_RUNTIME_SCHEMA", version)
        require(typed_equal(outputs[version]["runtime"], {
            "implementation": "cpython", "version": RUNTIME_VERSIONS[version]}),
            "E_INDEPENDENT_RUNTIME_ID", version)
    if stored_runtime is not None:
        for version in ("3.12", "3.14"):
            versions = {tuple(run["observation"]["runtime"]["version"])
                        for run in stored_runtime["runs"] if run["python"] == version}
            require(versions == {tuple(outputs[version]["runtime"]["version"])}
                    and all(typed_equal(run["observation"]["runtime"]["version"],
                                        outputs[version]["runtime"]["version"])
                            for run in stored_runtime["runs"] if run["python"] == version),
                    "E_STORED_RUNTIME_VERSION", version)
    cases = {version: outputs[version]["cases"] for version in ("3.12", "3.14")}
    require(typed_equal(cases.get("3.12"), cases.get("3.14")),
            "E_INDEPENDENT_RUNTIME_CROSS")
    expected = {
        "C01": {"counts": [4, 2], "qgr": 372.0},
        "C02": {"explicit": [7, 7], "fresh_after": [4, 2]},
        "C03": {"old": [4, 2], "new": [7, 7], "old_si_stable": True,
                "future_si_copy": True},
        "C04": {"old": [5, 2], "new": [5, 2]},
        "C05": {"legacy": [8.314, 96485.0, 0.025691238016271958],
                "si": [8.314462618, 96485.33212, True, True, 0.025692579121493725],
                "alias_static": [8.314, 96485.0], "old_seed_stable": True,
                "future_seed_differs": True, "restored": [8.314, 96485.0]},
        "C06": {"same": True, "counts": [7, 7]},
        "C07": {"same": True, "module": [4, 2], "old": [4, 2],
                "old_ids": True, "old_seed": True, "legacy": [8.314, 96485.0]},
        "C08": {"distinct": True, "a": [7, 7], "b": [4, 2]},
        "C09": {"counts": [4, 2]},
        "C10": {"old": [4, 2], "future": [7, 7], "old_seed": True,
                "future_seed": [0.0] * 7, "rf": [8.314462618, 96485.33212]},
        "C11": {"old": [4, 2], "future": [7, 7], "old_seed": True,
                "future_seed": [0.0] * 7, "rf": [8.314462618, 96485.33212]},
        "C12": {"absent": True},
        "C13": {"counts": [8, 14, 14], "canonical": [True, True, True],
                "construct": [True, True, True], "searched_names_absent": True},
    }
    require(typed_equal(cases["3.12"], expected), "E_INDEPENDENT_RUNTIME_GROUND")
    return outputs


def validate_artifacts(matrix: dict[str, Any], runtime: dict[str, Any],
                       predecessors: dict[str, dict[str, Any]],
                       input_rows: list[dict[str, Any]]) -> None:
    errors = artifact_errors(matrix, runtime, predecessors, input_rows)
    require(not errors, errors[0] if errors else "E_ARTIFACT")


def negative_controls(matrix: dict[str, Any], runtime: dict[str, Any],
                      predecessors: dict[str, dict[str, Any]],
                      input_rows: list[dict[str, Any]]) -> tuple[int, int]:
    if matrix.get("source_policy") != {
            "builder_neutral_sha256": BUILDER_SOURCE_POLICY_SHA256_LF,
            "validator_neutral_sha256": VALIDATOR_SOURCE_POLICY_SHA256_LF}:
        matrix = copy.deepcopy(matrix)
        matrix["source_policy"] = {
            "builder_neutral_sha256": BUILDER_SOURCE_POLICY_SHA256_LF,
            "validator_neutral_sha256": VALIDATOR_SOURCE_POLICY_SHA256_LF,
        }
        matrix["semantic_sha256"] = semantic_sha(matrix)
    writer_raw = baseline_bytes(WRITER_PATH)
    writer_tree = ast.parse(writer_raw.decode("utf-8"), filename=WRITER_PATH)
    independent = {
        "static": expected_source_static(),
        "search": independent_blob_search(predecessors[INVENTORY_PATH]),
        "production": independent_production_projection(predecessors[INVENTORY_PATH]),
        "saved": independent_saved_profiles(), "writer_raw": writer_raw,
        "writer_calls": [node for node in ast.walk(writer_tree) if isinstance(node, ast.Call)
            and ("write" in ast.unparse(node.func) or "dump" in ast.unparse(node.func))
            and ("params" in ast.unparse(node) or "json" in ast.unparse(node).lower())],
    }
    baseline_errors = set(artifact_errors(
        matrix, runtime, predecessors, input_rows, independent))
    def reseal(left: dict[str, Any], right: dict[str, Any]) -> None:
        right["semantic_sha256"] = semantic_sha(right)
        if isinstance(left.get("runtime_binding"), dict):
            left["runtime_binding"]["semantic_sha256"] = right["semantic_sha256"]
        left["semantic_sha256"] = semantic_sha(left)
    def reject(name: str, operation: Any) -> None:
        left, right = copy.deepcopy(matrix), copy.deepcopy(runtime)
        operation(left, right)
        reseal(left, right)
        mutated_errors = set(artifact_errors(
            left, right, predecessors, input_rows, independent))
        if not (mutated_errors - baseline_errors):
            raise ValidationError("E_NEGATIVE_FALSE_PASS:" + name)
    def wrong_value(value: Any) -> Any:
        if type(value) is bool:
            return not value
        if type(value) is int:
            return value + 1
        if type(value) is float:
            return value + 1.0
        if type(value) is str:
            return value + "_WRONG"
        if isinstance(value, list):
            clone = copy.deepcopy(value)
            require(bool(clone), "E_NEGATIVE_EMPTY_LIST")
            clone[0] = wrong_value(clone[0])
            return clone
        if isinstance(value, dict):
            clone = copy.deepcopy(value)
            require(bool(clone), "E_NEGATIVE_EMPTY_DICT")
            key = sorted(clone)[0]
            clone[key] = wrong_value(clone[key])
            return clone
        raise ValidationError("E_NEGATIVE_VALUE_TYPE:" + type(value).__name__)
    def equality_type_swap(value: Any) -> tuple[bool, Any]:
        if type(value) is bool:
            return True, int(value)
        if type(value) is int:
            return True, float(value)
        if type(value) is float and value.is_integer():
            return True, int(value)
        if isinstance(value, list):
            for index, item in enumerate(value):
                changed, replacement = equality_type_swap(item)
                if changed:
                    clone = copy.deepcopy(value)
                    clone[index] = replacement
                    return True, clone
            return False, value
        if isinstance(value, dict):
            for key in sorted(value):
                changed, replacement = equality_type_swap(value[key])
                if changed:
                    clone = copy.deepcopy(value)
                    clone[key] = replacement
                    return True, clone
            return False, value
        return False, value
    def full_reseal(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            observation = run["observation"]
            projection = copy.deepcopy(observation)
            projection.pop("runtime", None)
            projection.pop("observation_sha256", None)
            observation["observation_sha256"] = sha256(
                canonical_bytes(projection).rstrip(b"\n"))
            run["stdout_sha256"] = sha256(canonical_bytes(observation))
            run["stdout_is_canonical_observation"] = True
        right["semantic_sha256"] = semantic_sha(right)
        left["runtime_binding"]["semantic_sha256"] = right["semantic_sha256"]
        left["semantic_sha256"] = semantic_sha(left)
    def full_case_reject(name: str, case: str, key: str) -> None:
        left, right = copy.deepcopy(matrix), copy.deepcopy(runtime)
        matching = [run for run in right["runs"] if run["case_id"] == case]
        require(len(matching) == 2, "E_NEGATIVE_CASE_CARDINALITY", case)
        for run in matching:
            observation = run["observation"]
            require(key in observation, "E_NEGATIVE_CASE_KEY", f"{case}:{key}")
            observation[key] = wrong_value(observation[key])
        full_reseal(left, right)
        mutated_errors = set(artifact_errors(
            left, right, predecessors, input_rows, independent))
        if not (mutated_errors - baseline_errors):
            raise ValidationError("E_NEGATIVE_FALSE_PASS:full_reseal_" + name)
    def full_case_type_reject(name: str, case: str, key: str) -> None:
        left, right = copy.deepcopy(matrix), copy.deepcopy(runtime)
        matching = [run for run in right["runs"] if run["case_id"] == case]
        require(len(matching) == 2, "E_NEGATIVE_CASE_CARDINALITY", case)
        for run in matching:
            observation = run["observation"]
            changed, replacement = equality_type_swap(observation[key])
            require(changed and replacement == observation[key]
                    and not typed_equal(replacement, observation[key]),
                    "E_NEGATIVE_TYPE_SWAP", f"{case}:{key}")
            observation[key] = replacement
        full_reseal(left, right)
        mutated_errors = set(artifact_errors(
            left, right, predecessors, input_rows, independent))
        if not (mutated_errors - baseline_errors):
            raise ValidationError("E_NEGATIVE_FALSE_PASS:type_reseal_" + name)
    def full_runtime_reject(name: str, operation: Any) -> None:
        left, right = copy.deepcopy(matrix), copy.deepcopy(runtime)
        operation(left, right)
        full_reseal(left, right)
        mutated_errors = set(artifact_errors(
            left, right, predecessors, input_rows, independent))
        if not (mutated_errors - baseline_errors):
            raise ValidationError("E_NEGATIVE_FALSE_PASS:full_runtime_" + name)
    operations: list[tuple[str, Any]] = [
        ("matrix_extra_key", lambda m, r: m.update({"extra": 1})),
        ("runtime_extra_key", lambda m, r: r.update({"extra": 1})),
        ("case_contract_class", lambda m, r: m["case_contract"][4].update({"class": "SI_LIST_COPY"})),
        ("case_contract_expected", lambda m, r: m["case_contract"][8].update({"expected": "SELF_ASSERTED_RESET"})),
        ("mutation_order", lambda m, r: m["case_contract"].reverse()),
        ("repeated_import", lambda m, r: r["runs"][5]["observation"].update({"same_module_object": False})),
        ("si_toggle_rf", lambda m, r: r["runs"][4]["observation"]["si_after_true"].update({"R": 8.314})),
        ("si_toggle_seed", lambda m, r: r["runs"][4]["observation"].update({"existing_seed_unchanged": False})),
        ("si_alias_follow", lambda m, r: r["runs"][4]["observation"]["imported_scalar_alias_after_true"].update({"follows_rebind": True})),
        ("reload_existing_object", lambda m, r: r["runs"][6]["observation"].update({"existing_transition_identity_stable": False})),
        ("reload_existing_seed", lambda m, r: r["runs"][6]["observation"].update({"existing_seed_unchanged": False})),
        ("toggle_order_cross", lambda m, r: r["runs"][9]["observation"]["events"][1].update({"label": "skew_then"})),
        ("process_pair_pid", lambda m, r: r["process_pair_records"][0].update({"fresh_pid": r["process_pair_records"][0]["mutated_pid"]})),
        ("process_pair_total", lambda m, r: r["process_pair_records"][0].update({"fresh_total": 14})),
        ("runtime_observation_extra", lambda m, r: r["runs"][0]["observation"].update({"extra": 1})),
        ("runtime_event_extra", lambda m, r: r["runs"][0]["observation"]["events"][0].update({"extra": 1})),
        ("runtime_event_value", lambda m, r: r["runs"][0]["observation"]["events"][0]["constants"].update({"R": 7.0})),
        ("runtime_count_extra", lambda m, r: r["runs"][0]["observation"]["events"][0]["counts"].update({"extra": 1})),
        ("runtime_nested_constant_extra", lambda m, r: r["runs"][0]["observation"]["events"][0]["constants"].update({"extra": 1})),
        ("run_argv", lambda m, r: r["runs"][0]["argv"].append("--escape")),
        ("run_stdout", lambda m, r: r["runs"][0].update({"stdout_sha256": "0" * 64})),
        ("run_stderr", lambda m, r: r["runs"][0].update({"stderr_sha256": "1" * 64})),
        ("run_runtime", lambda m, r: r["runs"][0]["observation"]["runtime"].update({"version": [3, 13, 0]})),
        ("run_runtime_extra", lambda m, r: r["runs"][0]["observation"]["runtime"].update({"extra": 1})),
        ("alias_export", lambda m, r: m["source_static"]["absent_surfaces"].update({"module___all__": False})),
        ("missing_loader", lambda m, r: m["complete_python_search"].update({"searched_exact_names_status": "PRESENT"})),
        ("search_vocabulary", lambda m, r: m["complete_python_search"]["search_names"].append("read_params")),
        ("production_occurrence_crosswire", lambda m, r: m["production_occurrence_projection"]["occurrences"][0].update({"blob_ordinal": 84})),
        ("production_occurrence_extra", lambda m, r: m["production_occurrence_projection"]["occurrences"][0].update({"extra": 1})),
        ("production_blob_hash", lambda m, r: m["production_occurrence_projection"]["blobs"][0].update({"raw_sha256": "2" * 64})),
        ("production_blob_extra", lambda m, r: m["production_occurrence_projection"]["blobs"][0].update({"extra": 1})),
        ("production_shared_binding", lambda m, r: m["production_occurrence_projection"]["shared_blob_bindings"][0].update({"blob_ordinal": 84})),
        ("production_use_si_crosswire", lambda m, r: m["production_occurrence_projection"]["use_si_constants_occurrences"][0].update({"release": "v1.0.24"})),
        ("saved_path", lambda m, r: m["saved_profiles"][0].update({"path": m["saved_profiles"][1]["path"]})),
        ("saved_blob", lambda m, r: m["saved_profiles"][0].update({"blob_oid": "3" * 40})),
        ("saved_mode", lambda m, r: m["saved_profiles"][0].update({"git_mode": "100755"})),
        ("saved_kernel", lambda m, r: m["saved_profiles"][0].update({"kernel": "logistic"})),
        ("saved_material", lambda m, r: m["saved_profiles"][0].update({"material": "graphite"})),
        ("saved_n", lambda m, r: m["saved_profiles"][0].update({"N": 14})),
        ("saved_transition_keyset", lambda m, r: m["saved_profiles"][0]["transition_keysets"][0].append("alpha")),
        ("saved_transition_type", lambda m, r: m["saved_profiles"][0]["transition_value_types"][0].update({"Q": "int"})),
        ("saved_nested_extra", lambda m, r: m["saved_profiles"][0].update({"extra": 1})),
        ("saved_runtime_kernel", lambda m, r: r["runs"][12]["observation"]["saved_routes"][0].update({"kernel": "logistic"})),
        ("saved_runtime_dispatch", lambda m, r: r["runs"][12]["observation"]["saved_routes"][0].update({"kernel_metadata_dispatched": True})),
        ("saved_runtime_loader", lambda m, r: r["runs"][12]["observation"]["saved_routes"][0].update({"production_loader_used": True})),
        ("saved_runtime_extra", lambda m, r: r["runs"][12]["observation"]["saved_routes"][0].update({"extra": 1})),
        ("fresh_mutated_conflation", lambda m, r: m["default_adjudication"].update({"test_mutated_state_is_fresh_public_default": True})),
        ("stale_header_promotion", lambda m, r: m["default_adjudication"].update({"header_docstring_7_gallery_default_claim": "EXECUTABLE_AUTHORITY"})),
        ("stdout_only_pass", lambda m, r: r["runs"][0].update({"exit_code": 1})),
        ("runtime_version", lambda m, r: r["runs"][0].update({"python": "3.13"})),
        ("temp_leak", lambda m, r: r["aggregate"].update({"temp_leaks": 1})),
        ("authority_promotion", lambda m, r: m["authority"].update({"science": True})),
        ("runtime_authority", lambda m, r: r["authority"].update({"canonical_profile": True})),
        ("inplace_alias", lambda m, r: r["runs"][3]["observation"].update({"existing_after_inplace": {"graphite": 4, "silicon": 2, "total": 6}})),
        ("qgr_default", lambda m, r: m["source_static"]["from_wt_q_gr_default"].update({"runtime_bound_value": 3117.0})),
        ("writer_loader", lambda m, r: m["writer_evidence"].update({"classification": "PRODUCTION_LOADER"})),
        ("case_drop", lambda m, r: m["case_contract"].pop()),
        ("saved_count", lambda m, r: r["runs"][12]["observation"]["saved_routes"][0].update({"transition_count": 9})),
        ("owner_crosswire", lambda m, r: m["owner_resolution"].update({"origin_identity": "P066-R80-13"})),
        ("owner_hash", lambda m, r: m["owner_resolution"].update({"origin_record_sha256": "4" * 64})),
        ("owner_disposition", lambda m, r: m["owner_resolution"].update({"prior_serialized_disposition": "DISPATCH"})),
        ("owner_resolution", lambda m, r: m["owner_resolution"].update({"resolution_state": "RESOLVED"})),
        ("control_pin", lambda m, r: m["control_hashes"].update({RESULT_PATH: "0" * 64})),
        ("source_pin", lambda m, r: m["source_policy"].update({"builder_neutral_sha256": "0" * 64})),
        ("runtime_binding", lambda m, r: m["runtime_binding"].update({"processes": 25})),
        ("bounded_cases", lambda m, r: r["runtime_contract"].update({"bounded_no_cartesian_permutations": False})),
        ("new_process_reset", lambda m, r: r["runs"][8]["observation"]["fresh_isolated_process"]["counts"].update({"total": 14})),
        ("ordinary_reimport_reset", lambda m, r: m["default_adjudication"].update({"ordinary_reimport_resets_module_state": True})),
        ("loader_promotion", lambda m, r: r["authority"].update({"production_saved_loader": True})),
        ("original_optimizer", lambda m, r: r["authority"].update({"original_optimizer_state": True})),
        ("matrix_phase_type", lambda m, r: m.update({"phase": 67.0})),
        ("runtime_step_type", lambda m, r: r.update({"step": 85.0})),
        ("matrix_schema_version_value", lambda m, r: m.update({"schema_version": "phase067-step85-default-import-v2"})),
        ("runtime_schema_version_type", lambda m, r: r.update({"schema_version": 1})),
        ("generation_order_type", lambda m, r: m.update({"result_first": 1})),
        ("source_lines_type", lambda m, r: m["source_static"].update({"physical_lines": float(m["source_static"]["physical_lines"])})),
        ("source_assignment_anchor_type", lambda m, r: m["source_static"]["assignment_rows"][0]["anchor"].update({"start_line": float(m["source_static"]["assignment_rows"][0]["anchor"]["start_line"])})),
        ("source_toggle_anchor_type", lambda m, r: m["source_static"]["toggle"]["anchor"].update({"end_line": float(m["source_static"]["toggle"]["anchor"]["end_line"])})),
        ("source_constructor_anchor_type", lambda m, r: m["source_static"]["constructor_default_load"].update({"start_line": float(m["source_static"]["constructor_default_load"]["start_line"])})),
        ("source_qgr_type", lambda m, r: m["source_static"]["from_wt_q_gr_default"].update({"runtime_bound_value": 372})),
        ("search_count_type", lambda m, r: m["complete_python_search"].update({"searched_occurrences": 129.0})),
        ("production_ordinal_type", lambda m, r: m["production_occurrence_projection"]["occurrences"][0].update({"ordinal": float(m["production_occurrence_projection"]["occurrences"][0]["ordinal"])})),
        ("saved_n_type", lambda m, r: m["saved_profiles"][0].update({"N": 8.0})),
        ("saved_finite_type", lambda m, r: m["saved_profiles"][0].update({"finite_numeric_values": 1})),
        ("writer_anchor_type", lambda m, r: m["writer_evidence"]["write_anchors"][0].update({"start_line": float(m["writer_evidence"]["write_anchors"][0]["start_line"])})),
        ("default_qgr_type", lambda m, r: m["default_adjudication"].update({"from_wt_q_gr_default_bound_at_definition": 372})),
        ("owner_target_phase_type", lambda m, r: m["owner_resolution"].update({"target_phase": 67.0})),
        ("owner_external_type", lambda m, r: m["owner_resolution"].update({"external_authority_promoted": 0})),
        ("matrix_authority_type", lambda m, r: m["authority"].update({"science": 0})),
        ("runtime_authority_type", lambda m, r: r["authority"].update({"production_saved_loader": 0})),
        ("runtime_binding_processes_type", lambda m, r: m["runtime_binding"].update({"processes": 26.0})),
        ("runtime_binding_equal_type", lambda m, r: m["runtime_binding"].update({"cross_runtime_behavior_equal": 1})),
        ("validation_zero_type", lambda m, r: m["validation"].update({"authority_promotions": 0.0})),
        ("aggregate_process_type", lambda m, r: r["aggregate"].update({"processes": 26.0})),
        ("process_pair_total_type", lambda m, r: r["process_pair_records"][0].update({"mutated_total": 14.0})),
        ("process_pair_pid_type", lambda m, r: r["process_pair_records"][0].update({"mutated_pid": float(r["process_pair_records"][0]["mutated_pid"])})),
        ("process_pair_bool_type", lambda m, r: r["process_pair_records"][0].update({"pid_distinct": 1})),
        ("runtime_contract_bool_type", lambda m, r: r["runtime_contract"].update({"network_used": 0})),
    ]
    for name, operation in operations:
        reject(name, operation)
    full_case_fields = [
        (case, key) for case in CASE_IDS
        for key in sorted(CASE_EXTRA_KEYS[case])
    ]
    for case, key in full_case_fields:
        full_case_reject(f"{case}:{key}", case, key)
    case_samples = {case: next(run["observation"] for run in runtime["runs"]
                               if run["python"] == "3.12" and run["case_id"] == case)
                    for case in CASE_IDS}
    typed_case_fields = [(case, key) for case, key in full_case_fields
                         if equality_type_swap(case_samples[case][key])[0]]
    for case, key in typed_case_fields:
        full_case_type_reject(f"{case}:{key}", case, key)
    for case, key in (("C01_FRESH_BASELINE", "fresh_first"),
                      ("C01_FRESH_BASELINE", "case_id"),
                      ("C01_FRESH_BASELINE", "surfaces"),
                      ("C01_FRESH_BASELINE", "events")):
        full_case_reject(f"common:{key}", case, key)
    def mutate_micro(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            run["observation"]["runtime"]["version"][2] += 1
    def collapse_pair_pid(left: dict[str, Any], right: dict[str, Any]) -> None:
        for version in ("3.12", "3.14"):
            c06 = next(run for run in right["runs"] if run["python"] == version
                       and run["case_id"] == "C06_ORDINARY_IMPORT_CACHE")
            c09 = next(run for run in right["runs"] if run["python"] == version
                       and run["case_id"] == "C09_NEW_PROCESS_RESET")
            pid = c06["observation"]["runtime"]["pid"]
            c09["observation"]["runtime"]["pid"] = pid
            pair = next(row for row in right["process_pair_records"] if row["python"] == version)
            pair["fresh_pid"] = pid
    full_runtime_reject("version_micro", mutate_micro)
    full_runtime_reject("c06_c09_pid_invariant", collapse_pair_pid)
    def type_swap_runtime_version(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            run["observation"]["runtime"]["version"][0] = 3.0
    def type_swap_common_surfaces(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            run["observation"]["surfaces"]["module___all__"] = 0
    def type_swap_common_events(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            run["observation"]["events"][0]["counts"]["graphite"] = float(
                run["observation"]["events"][0]["counts"]["graphite"])
    def type_swap_common_fresh(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            run["observation"]["fresh_first"] = 1
    def type_swap_run_fields(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            run["invocation_ordinal"] = float(run["invocation_ordinal"])
            run["exit_code"] = 0.0
            run["timed_out"] = 0
    def type_swap_c13_saved_n(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            if run["case_id"] == "C13_SAVED_ROUTE_GNF":
                run["observation"]["saved_routes"][0]["N"] = 8.0
    def type_swap_c13_saved_bool(left: dict[str, Any], right: dict[str, Any]) -> None:
        for run in right["runs"]:
            if run["case_id"] == "C13_SAVED_ROUTE_GNF":
                run["observation"]["saved_routes"][0]["constructor_injection_accepted"] = 1
    full_runtime_reject("version_major_type", type_swap_runtime_version)
    full_runtime_reject("common_surfaces_type", type_swap_common_surfaces)
    full_runtime_reject("common_events_type", type_swap_common_events)
    full_runtime_reject("common_fresh_type", type_swap_common_fresh)
    full_runtime_reject("run_scalar_types", type_swap_run_fields)
    full_runtime_reject("c13_saved_n_type", type_swap_c13_saved_n)
    full_runtime_reject("c13_saved_bool_type", type_swap_c13_saved_bool)
    total = len(operations) + len(full_case_fields) + len(typed_case_fields) + 13
    return total, total


def strict_json_controls() -> tuple[int, int]:
    samples = (b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'\xef\xbb\xbf{}\n')
    passed = 0
    for raw in samples:
        try:
            strict_load(raw, "negative")
        except (ValidationError, json.JSONDecodeError, UnicodeDecodeError):
            passed += 1
    require(passed == len(samples), "E_JSON_NEGATIVES")
    return passed, len(samples)


def source_policy_errors(path: str, role: str) -> list[str]:
    errors: list[str] = []
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"), filename=path)
    allowed_imports = {"argparse", "ast", "copy", "hashlib", "json", "math", "os",
                       "pathlib", "re", "shutil", "subprocess", "tempfile", "typing",
                       "__future__"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = ([alias.name.split(".")[0] for alias in node.names]
                     if isinstance(node, ast.Import) else [])
            module = ((node.module or "").split(".")[0]
                      if isinstance(node, ast.ImportFrom) else None)
            if any(name not in allowed_imports for name in names) or (module and module not in allowed_imports):
                errors.append("E_SOURCE_IMPORT")
        if isinstance(node, ast.Call):
            call = ast.unparse(node.func)
            if call in {"eval", "exec", "compile", "__import__"}:
                errors.append("E_SOURCE_DYNAMIC_EXECUTION")
            if call == "subprocess.run":
                owner = next((parent.name for parent in ast.walk(tree)
                              if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef))
                              and node in list(ast.walk(parent))), "<module>")
                allowed_owners = ({"run_git", "isolated_runs"} if role == "builder"
                                  else {"git", "independent_runtime"})
                if owner not in allowed_owners:
                    errors.append("E_SOURCE_SUBPROCESS_OWNER")
                if any(keyword.arg == "shell" and not isinstance(keyword.value, ast.Constant)
                       for keyword in node.keywords):
                    errors.append("E_SOURCE_SHELL")
                shell = next((keyword.value.value for keyword in node.keywords
                              if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant)), None)
                if shell is not False:
                    errors.append("E_SOURCE_SHELL")
            if any(token in call for token in ("urlopen", "requests.", "socket.", "urllib.")):
                errors.append("E_SOURCE_NETWORK")
    return errors


def verify_source_policy() -> None:
    require(not source_policy_errors(BUILDER_PATH, "builder"), "E_BUILDER_SOURCE_POLICY")
    require(not source_policy_errors(VALIDATOR_PATH, "validator"), "E_VALIDATOR_SOURCE_POLICY")
    require(normalized_policy(BUILDER_PATH, "BUILDER_SOURCE_POLICY_SHA256_LF") ==
            BUILDER_SOURCE_POLICY_SHA256_LF, "E_BUILDER_POLICY_HASH")
    require(normalized_policy(VALIDATOR_PATH, "VALIDATOR_SOURCE_POLICY_SHA256_LF") ==
            VALIDATOR_SOURCE_POLICY_SHA256_LF, "E_VALIDATOR_POLICY_HASH")


def verify_control_documents() -> None:
    for path, expected in CONTROL_PINS.items():
        require(sha256((ROOT / path).read_bytes()) == expected, "E_CONTROL_HASH", path)
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    parent = (ROOT / PARENT_LEDGER).read_text(encoding="utf-8")
    canonical = (ROOT / CANONICAL_LEDGER).read_text(encoding="utf-8")
    handover = (ROOT / HANDOVER).read_text(encoding="utf-8")
    for token in (GATE, "PASS_PENDING_PERSISTENCE", "PENDING_AT_PRECOMMIT_BY_DESIGN",
                  EXPECTED_PARENT, EXPECTED_SUBJECT, PERSISTENCE, "C01", "C13",
                  "P066-OBL-0125", "P066-R80-14", "P0/P1/P2=0/0/0"):
        require(token in result, "E_RESULT_TOKEN", token)
    for text, label in ((parent, "parent"), (canonical, "canonical"), (handover, "handover")):
        require("f00bf2fa8f25c85f0c62cb901912763d98c8f070" in text,
                "E_STEP84_PERSISTENCE", label)
        require(GATE in text and EXPECTED_SUBJECT in text and PERSISTENCE in text,
                "E_STEP85_CURRENT", label)
        require("Step 86" in text and "blocked" in text.lower(), "E_STEP86_BLOCKED", label)
    require(canonical.count("| 067 |") == 1, "E_CANONICAL_PHASE_ROW")
    require(f"현재 result: `{RESULT_PATH}`" in handover, "E_HANDOVER_CURRENT_RESULT")
    require(f"현재 machine evidence: `{MATRIX_PATH}` + `{RUNTIME_PATH}`" in handover,
            "E_HANDOVER_CURRENT_MACHINE")


def parse_porcelain(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4 and line[2] == " ", "E_STATUS_LINE")
        status, path = line[:2], line[3:].replace("\\", "/")
        require(" -> " not in path and path not in result, "E_STATUS_RENAME")
        result[path] = status
    return result


def parse_name_status(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        status, path = line.split("\t", 1)
        require(status in {"A", "M"} and path not in result, "E_NAME_STATUS")
        result[path] = status
    return result


def parse_ls_tree(text: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        if path in FINAL_SET:
            require(kind == "blob", "E_TREE_KIND")
            result[path] = (mode, oid)
    return result


def gtext(args: tuple[str, ...], *, allow_failure: bool = False) -> str:
    return git(args, allow_failure=allow_failure).decode("utf-8").rstrip("\r\n")


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    return text.removesuffix(".git").strip("/")


def live_oid(ref: str) -> str:
    value = gtext(("ls-remote", "--heads", "origin", ref))
    require("\t" in value, "E_LIVE_REF", ref)
    return value.split("\t", 1)[0]


def repository_refs(expected_tip: str) -> dict[str, Any]:
    record = {
        "branch": gtext(("rev-parse", "--abbrev-ref", "HEAD")),
        "head": gtext(("rev-parse", "HEAD")),
        "upstream_name": gtext(("rev-parse", "--abbrev-ref", "@{upstream}")),
        "upstream_oid": gtext(("rev-parse", UPSTREAM)),
        "active_tracking_oid": gtext(("rev-parse", f"refs/remotes/{UPSTREAM}")),
        "active_live_oid": live_oid(f"refs/heads/{BRANCH}"),
        "origin": canonical_origin(gtext(("ls-remote", "--get-url", "origin"))),
        "protected_local_oid": gtext(("show-ref", "--verify", "--hash",
                                        "refs/heads/codex/lib-physics-endgame-v1025_2")),
        "protected_tracking_oid": gtext(("rev-parse",
                                           "refs/remotes/origin/codex/lib-physics-endgame-v1025_2")),
        "protected_live_oid": live_oid("refs/heads/codex/lib-physics-endgame-v1025_2"),
        "main_local": gtext(("show-ref", "--verify", "--hash", "refs/heads/main"),
                            allow_failure=True),
        "main_tracking_oid": gtext(("rev-parse", "refs/remotes/origin/main")),
        "main_live_oid": live_oid("refs/heads/main"),
    }
    expected = {"branch": BRANCH, "head": expected_tip, "upstream_name": UPSTREAM,
                "upstream_oid": expected_tip, "active_tracking_oid": expected_tip,
                "active_live_oid": expected_tip,
                "origin": "github.com/lksz1412/project_anode_fit",
                "protected_local_oid": PROTECTED_TIP,
                "protected_tracking_oid": PROTECTED_TIP,
                "protected_live_oid": PROTECTED_TIP, "main_local": "",
                "main_tracking_oid": MAIN_TIP, "main_live_oid": MAIN_TIP}
    require(record == expected, "E_REPOSITORY_REFS", repr(record))
    return record


def worktree_status() -> dict[str, str]:
    return parse_porcelain(gtext(("status", "--porcelain=v1", "--untracked-files=all")))


def index_snapshot() -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in gtext(("ls-files", "-s")).splitlines():
        meta, path = line.split("\t", 1)
        if path in FINAL_SET:
            mode, oid, stage = meta.split()
            require(stage == "0", "E_INDEX_STAGE")
            result[path] = (mode, oid)
    return result


def transaction_seal(expected_tip: str) -> dict[str, Any]:
    return {
        "repository_refs": repository_refs(expected_tip),
        "status": worktree_status(), "index": index_snapshot(),
        "path_hashes": {path: sha256((ROOT / path).read_bytes())
                        for path in FINAL_PATHS if (ROOT / path).exists()},
        "input_hashes": {path: sha256(commit_bytes(path)) for path in INPUT_PINS},
    }


def verify_content() -> None:
    expected = {path: ("??" if FINAL_STATUS[path] == "A" else " M") for path in FINAL_PATHS}
    require(worktree_status() == expected, "E_CONTENT_PATHS", repr(worktree_status()))
    require(not set(index_snapshot()).intersection(set(FINAL_PATHS[:5])), "E_CONTENT_STAGED_ADD")


def verify_staged() -> None:
    require(gtext(("rev-parse", "HEAD")) == EXPECTED_PARENT, "E_STAGED_PARENT")
    require(parse_name_status(gtext(("diff", "--cached", "--name-status", "--no-renames", "HEAD")))
            == FINAL_STATUS, "E_STAGED_PATHS")
    require(gtext(("diff", "--name-only")) == ""
            and gtext(("ls-files", "--others", "--exclude-standard")) == "", "E_STAGED_DIRTY")
    require(gtext(("diff", "--cached", "--check")) == "", "E_DIFF_CHECK")
    index = index_snapshot()
    require(set(index) == FINAL_SET and all(mode == "100644" for mode, _ in index.values()),
            "E_INDEX_MODES")
    for path, (_, oid) in index.items():
        raw = (ROOT / path).read_bytes()
        require(git(("show", f":{path}")) == raw, "E_INDEX_BYTES", path)
        require(git(("cat-file", "blob", oid)) == raw, "E_INDEX_BLOB", path)


def verify_persistence(commit: str) -> None:
    parents = gtext(("show", "-s", "--format=%P", commit)).split()
    require(parents == [EXPECTED_PARENT], "E_COMMIT_PARENTS", repr(parents))
    require(gtext(("rev-parse", f"{commit}^")) == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(gtext(("show", "-s", "--format=%s", commit)) == EXPECTED_SUBJECT,
            "E_COMMIT_SUBJECT")
    changed = parse_name_status(gtext(("diff-tree", "--no-commit-id", "--name-status",
                                        "--no-renames", "-r", f"{commit}^", commit)))
    require(changed == FINAL_STATUS, "E_COMMIT_PATHS")
    tree = parse_ls_tree(gtext(("ls-tree", "-r", commit)))
    require(set(tree) == FINAL_SET and all(mode == "100644" for mode, _ in tree.values()),
            "E_COMMIT_MODES")
    require(gtext(("status", "--porcelain")) == "", "E_WORKTREE_DIRTY")
    require(gtext(("diff", "--name-only", PROTECTED_TIP, "--", "Claude")) == "",
            "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        require(git(("show", f"{commit}:{path}")) == (ROOT / path).read_bytes(),
                "E_COMMITTED_BYTES", path)


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require((args.verify_persistence and args.expected_commit is not None)
            or (not args.verify_persistence and args.expected_commit is None),
            "E_EXPECTED_COMMIT_MODE")
    if args.verify_persistence:
        require(re.fullmatch(r"[0-9a-f]{40}", args.expected_commit or "") is not None,
                "E_EXPECTED_COMMIT")
    expected_tip = args.expected_commit if args.verify_persistence else EXPECTED_PARENT
    entry = transaction_seal(expected_tip or "")
    verify_source_policy()
    verify_control_documents()
    predecessors, input_rows = load_predecessors()
    matrix, matrix_nodes, matrix_depth = strict_load((ROOT / MATRIX_PATH).read_bytes(), MATRIX_PATH)
    runtime, runtime_nodes, runtime_depth = strict_load((ROOT / RUNTIME_PATH).read_bytes(), RUNTIME_PATH)
    validate_artifacts(matrix, runtime, predecessors, input_rows)
    independent_runtime(runtime)
    semantic_passed, semantic_total = negative_controls(
        matrix, runtime, predecessors, input_rows)
    json_passed, json_total = strict_json_controls()
    if args.content_only:
        verify_content()
    elif args.verify_staged:
        verify_staged()
    else:
        verify_persistence(args.expected_commit or "")
    terminal = transaction_seal(expected_tip or "")
    require(entry == terminal, "E_TRANSACTION_SEAL")
    print(f"PASS_P067_STEP85_CONTROLS semantic={semantic_passed}/{semantic_total} "
          f"json={json_passed}/{json_total} nodes={matrix_nodes + runtime_nodes} "
          f"depth={max(matrix_depth, runtime_depth)} independent=13/13x2")
    print(f"{PERSISTENCE if args.verify_persistence else GATE} cases=13 processes=26 "
          "search=84/84 saved=3 determinism=2/2")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(str(exc))
        raise SystemExit(1)
