#!/usr/bin/env python3
"""Validate Phase 067 Step 88 numerical-guard impact evidence."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4"
REJECTED_CANDIDATE = "6ee61ea9e5636a66e0aa217e4929e60897d8b073"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
DATE = "2026-09-02"
SUBJECT = "audit(phase067): bound numerical guard impacts"
GATE = "PASS_P067_STEP88_NUMERICAL_GUARD"
PERSISTENCE = "PASS_P067_STEP88_PERSISTENCE"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_BASE_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
MAIN_ADVANCE_COMMIT_COUNT = 7
MAIN_ADVANCE_PATH_COUNT = 25
BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step88.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step88.py"
MATRIX_PATH = "Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RESULT_PATH,
               PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if index < 4 else "M") for index, path in enumerate(FINAL_PATHS)}
ALLOWED_STAGED_PORCELAIN = {"A ", "M "}
MAX_JSON_BYTES = 8_000_000
MAX_JSON_DEPTH = 64
MAX_JSON_NODES = 600_000
BUILDER_SOURCE_POLICY_SHA256_LF = "3002e6ad393e79d5834ff46633dcc4adec1f128d62f030fbccaaf84728380600"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "973ac64ede4001bee3a3c71cf6c76013edb6c5494613e27c1abeb863d176999a"
CONTROL_SHA256 = {
    RESULT_PATH:"221c02f9e17d316d1d6e4b355234347fa93e1ef4ea08a9fcc9d9be71d7d32942",
    PARENT_LEDGER:"e8cf14dc3ec94d1e531f2df7fb2f45f62b6a436371301ae1ffaa0d01b30e1f1d",
    CANONICAL_LEDGER:"55fd6d856f8ec35448156834aeec20faa34f0b7ddd33f1cabeac8ebe66747ded",
    HANDOVER:"704aeeb14f08ad5807eec2712c6c15f84a6fbddfa67f52fd48780011bbababe5",
}
SECTION_SHA256 = {
    "inputs":"ed1f218d6c271eb74a795238c6c25a8aea9a83f1a131acab1045366aeb0f2f39",
    "universe":"36a3623df8f221b1b563f30eaed02948d7af3132daa42d625edf554f2ece6659",
    "scope_policy":"890ca5699a07be92577dff45c3369f665b209bc4893a822baceba3732a48a9d3",
    "candidate_disposition_records":"2775dbce9e50df79824b77eff3bdbb004a813a851071b45da3cc4d52af7a0cfc",
    "source_occurrence_records":"f7c1424ddf6bbdd9177da7782f433452981e0be507214f67e8c3f1ca442494ac",
    "source_feature_records":"4de3fa771dee9e25a9c502a955c42540ad3fdddbedf3ec11be35704efc29628c",
    "supplemental_optimizer_source_record":"8121e723b59f7d9495b282e8d049d6e24fdbf6e580ac03c73d6df2db40584a2e",
    "guard_records":"9bb4346e260b59f578e4ce94e349b1eb73ac370c4a0c38b98d078471fd3458eb",
    "impact_probe_records":"80eb86a8bdd7854a15c08419abf8b1935eef87c88f3711ebbb62c8910c4d1766",
    "numerical_default_records":"613c45a1625303660984fa588be5f1b4e8831e6e06c0fe6b2c15886ab0ee9769",
    "optimizer_route_records":"5ee940ade7bb6021fa929e4c317382d921f38f304eb52b38b4f376661d8c1e74",
    "open_gap_records":"c062e720a732afa2bbab2df1ecbe5260aeb64b25fc45f330c4d8823abe49a68f",
    "coverage":"7d41c455539e1090aa843d343b5cac76e6e9e8f85434258283bb7a801f71f140",
    "authority":"4b6e1561f9a44a91e87faf0dd446605737c3ee983afdb916678409f0bd2c5e3f",
    "validation":"cdb9cbe979119d89da2c211c12ed040bb00e35fc984d7f23e24377ddbdfa4087",
}

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
INPUT_PINS = {
    INVENTORY_PATH:("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63","593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1",False),
    ATTESTATION_PATH:("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174","e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9",False),
    CALL_GRAPH_PATH:("54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f","63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc",True),
    UNIT_PATH:("62f5eb265121987b83398266895a11e8a84d7f1ffa90c59fe929efb6f00614be","099899de75edfde55a92ff31f577e178967212226cf4a13cdb951643b15e535c",True),
    TEST_DEMO_PATH:("13a281c76282f5fae370d1c2b10f183937c685bceba466489a62b9e850049d4a","eadde68e51257e0daae9f9455be3a7331c77a56d1490b2291934ef75f45fa154",True),
    STATE_FLOW_PATH:("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8","c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44",True),
    MUTABLE_STATE_PATH:("b8ac7affbb31195ec8dde6015890cbb50b1f2b9cc5815fc33c325efc95286f23","845b676aea321134b648de41320e7baf4f39f925ad2a1abe96f36f713bc95542",True),
    SAVED_RUNTIME_PATH:("9bf610d2d09be7d95fd2493541d6c4336de330c37fb56d1f12c411b228dfbf82","0e2b0bd3f6120c9c8feaa879b5fe62a49934de5ea8dbddff14c700ddef32f196",True),
    GUIDE_TOOL_PATH:("474f09ebb1605d3190867cee9746079b10c04f6bfbdfbab028e9d6c1be70ec08","c556671b6fd4284d740fdb0cc3777087442d4abd2160ace42d4ff70749d4144c",True),
    FIT_REPLAY_PATH:("ff8141e7f0d950cfb6f588f41743e7b9221c5f4cb73ecc76522b0beb45a70d80","567c8b65886851e34fff8e913e6ad81819d8ce022001df6bf20a9b26fce6b029",False),
}
RELEASES = ["v1.0.10","v1.0.11","v1.0.12","v1.0.13","v1.0.14","v1.0.15","v1.0.16","v1.0.17","v1.0.18.1","v1.0.18.2","v1.0.19","v1.0.20","v1.0.21","v1.0.22","v1.0.23","v1.0.24","v1.0.24.1","v1.0.25","v1.0.25.1","v1.0.25.2"]


class ValidationError(RuntimeError):
    pass


def require(ok: bool, code: str, detail: str = "") -> None:
    if not ok:
        raise ValidationError(code + ((":" + detail) if detail else ""))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    copy_value = dict(value)
    copy_value.pop("semantic_sha256", None)
    return sha(canonical(copy_value))


def predecessor_semantic(value: dict[str, Any]) -> str:
    copy_value = dict(value)
    copy_value["semantic_sha256"] = ""
    return sha((json.dumps(copy_value, ensure_ascii=False, indent=2, sort_keys=True,
                           separators=(",", ": "), allow_nan=False) + "\n").encode("utf-8"))


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(typed_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and finite_tree(item) for key, item in value.items())
    if isinstance(value, list):
        return all(finite_tree(item) for item in value)
    return value is None or isinstance(value, (bool, int, str))


def strict_load(raw: bytes, label: str, generated: bool = True, *,
                max_bytes: int = MAX_JSON_BYTES, max_depth: int = MAX_JSON_DEPTH,
                max_nodes: int = MAX_JSON_NODES) -> tuple[dict[str, Any], int, int]:
    nodes = 0
    depth = 0
    require(type(max_bytes) is int and 0 < max_bytes <= MAX_JSON_BYTES, label + "_LIMIT")
    require(type(max_depth) is int and 0 < max_depth <= MAX_JSON_DEPTH, label + "_LIMIT")
    require(type(max_nodes) is int and 0 < max_nodes <= MAX_JSON_NODES, label + "_LIMIT")
    require(len(raw) <= max_bytes, label + "_BYTES")
    nesting = 0
    in_string = False
    escaped = False
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                in_string = False
        elif byte == 34:
            in_string = True
        elif byte in (91, 123):
            nesting += 1
            require(nesting <= max_depth, label + "_DEPTH")
        elif byte in (93, 125):
            nesting -= 1
            require(nesting >= 0, label + "_LEXICAL")
    require(nesting == 0 and not in_string and not escaped, label + "_LEXICAL")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, label + "_DUPLICATE")
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError, MemoryError) as exc:
        raise ValidationError(label) from exc
    require(isinstance(value, dict), label + "_TREE")
    stack: list[tuple[Any, int]] = [(value, 0)]
    while stack:
        item, level = stack.pop()
        nodes += 1
        require(nodes <= max_nodes, label + "_NODES")
        require(level <= max_depth, label + "_DEPTH")
        depth = max(depth, level)
        if isinstance(item, dict):
            for key, child in item.items():
                require(isinstance(key, str), label + "_TREE")
                stack.append((key, level + 1))
                stack.append((child, level + 1))
        elif isinstance(item, list):
            for child in item:
                stack.append((child, level + 1))
        elif isinstance(item, float):
            require(math.isfinite(item), label + "_TREE")
        else:
            require(item is None or isinstance(item, (str, int, bool)), label + "_TREE")
    if generated:
        require(raw == canonical(value), label + "_NONCANONICAL")
    return value, nodes, depth


def is_oid(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value))


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    exact = {
        ("rev-parse", "HEAD"), ("rev-parse", "--abbrev-ref", "HEAD"),
        ("rev-parse", "--abbrev-ref", "@{upstream}"), ("rev-parse", "@{upstream}"),
        ("rev-parse", f"refs/remotes/origin/{BRANCH}"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("rev-parse", "refs/remotes/origin/main"), ("remote", "get-url", "origin"),
        ("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        ("show-ref", "--verify", "--hash", "refs/heads/main"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("ls-remote", "--heads", "origin", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        ("ls-remote", "--heads", "origin", "refs/heads/main"),
        ("merge-base", EXPECTED_PARENT, MAIN_TIP),
        ("rev-list", "--count", f"{MAIN_BASE_TIP}..{MAIN_TIP}"),
        ("diff", "--name-only", f"{MAIN_BASE_TIP}..{MAIN_TIP}", "--"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--name-only", EXPECTED_PARENT, "--", "Claude"),
        ("diff", "--cached", "--name-status", "-z"), ("ls-files", "-s", "-z"),
        ("diff", "--cached", "--name-status", "-z", EXPECTED_PARENT, "--"),
        ("diff", "--name-only", "--"),
    }
    if args in exact:
        return True
    if len(args) == 3 and args[:2] == ("cat-file", "blob") and is_oid(args[2]):
        return True
    if (len(args) == 4
            and args[:3] in (("show", "--no-patch", "--format=%s"),
                             ("show", "--no-patch", "--format=%P"))
            and is_oid(args[3])):
        return True
    if len(args) == 2 and args[0] == "show" and re.fullmatch(r"[0-9a-f]{40}:Codex/results/[A-Za-z0-9_./-]+", args[1]):
        return True
    if len(args) == 8 and args[:5] == ("diff-tree", "--no-commit-id", "--name-status", "-r", "-z"):
        return bool(re.fullmatch(r"[0-9a-f]{40}\^", args[5]) and is_oid(args[6])
                    and args[5] == args[6] + "^" and args[7] == "--")
    return False


def git(args: tuple[str, ...], allow_failure: bool = False) -> bytes:
    require(git_argv_allowed(args), "E_GIT_ARGV", repr(args))
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not allow_failure:
        require(completed.returncode == 0 and completed.stderr == b"", "E_GIT", repr(args))
    return completed.stdout


def gtext(args: tuple[str, ...], allow_failure: bool = False) -> str:
    return git(args, allow_failure).decode("utf-8").strip()


def blob(oid: str) -> bytes:
    return git(("cat-file", "blob", oid))


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__, "fields":[
            [field, stable_ast(getattr(value, field, None))] for field in value._fields
        ]}
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, tuple):
        return {"_tuple":[stable_ast(item) for item in value]}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return {"_literal_type":type(value).__name__,"repr":repr(value)}


def qualified_owner(tree: ast.Module, selected: ast.AST) -> str:
    rows: list[tuple[int,str]] = []
    def walk(node: ast.AST, scope: list[str]) -> None:
        nested = scope
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            nested = [*scope, node.name]
            if node.lineno <= selected.lineno and node.end_lineno >= selected.end_lineno:
                rows.append((node.end_lineno-node.lineno,".".join(nested)))
        for child in ast.iter_child_nodes(node):
            walk(child, nested)
    walk(tree, [])
    return min(rows)[1] if rows else "<module>"


def verify_anchor(tree: ast.Module, source: str, stored: dict[str, Any]) -> bool:
    candidates = [node for node in ast.walk(tree)
                  if getattr(node,"lineno",None) == stored.get("start_line")
                  and getattr(node,"end_lineno",None) == stored.get("end_line")
                  and type(node).__name__ == stored.get("ast_kind")]
    if len(candidates) != 1:
        return False
    node = candidates[0]
    text = "\n".join(source.splitlines()[node.lineno-1:node.end_lineno]) + "\n"
    expected = {"qualified_owner":qualified_owner(tree,node),"ast_kind":type(node).__name__,
                "start_line":node.lineno,"end_line":node.end_lineno,
                "source_sha256_lf":sha(text.encode("utf-8")),
                "source_normalization":"LF_TERMINATED",
                "node_sha256":sha(canonical(stable_ast(node))),"expression":ast.unparse(node)}
    return typed_equal(stored, expected)


def load_inputs() -> tuple[dict[str, dict[str, Any]], int, int]:
    result = {}; total_nodes = 0; max_depth = 0
    for path, (raw_pin, semantic_pin, modern) in INPUT_PINS.items():
        raw = git(("show", f"{EXPECTED_PARENT}:{path}"))
        require(sha(raw) == raw_pin, "E_INPUT_RAW", path)
        value, nodes, depth = strict_load(raw, "E_INPUT_JSON", False)
        observed = semantic(value) if modern else predecessor_semantic(value)
        require(observed == semantic_pin == value["semantic_sha256"], "E_INPUT_SEMANTIC", path)
        result[path] = value; total_nodes += nodes; max_depth = max(max_depth, depth)
    return result, total_nodes, max_depth


TOP_KEYS = {"schema_version","artifact","phase","step","generated_date","baseline_commit",
            "expected_parent","branch","expected_subject","gate","persistence_terminal",
            "precommit_status","containing_commit","result_first","json_output_last","inputs",
            "universe","scope_policy","candidate_disposition_records","source_occurrence_records",
            "source_feature_records","supplemental_optimizer_source_record","guard_records",
            "impact_probe_records","numerical_default_records","optimizer_route_records","open_gap_records","coverage",
            "authority","validation","semantic_sha256"}


def section_digest(value: Any) -> str:
    return sha(canonical(value))


def expected_occurrences(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    rows = sorted([row for row in inventory["occurrence_records"] if row["role"] == "code"],
                  key=lambda row: RELEASES.index(row["release"]))
    keys = ("ordinal","manifest_entry_index","release","path","role","blob_oid","blob_ordinal","git_mode","size_bytes","physical_lines")
    return [{key:row[key] for key in keys} for row in rows]


def independent_source_errors(matrix: dict[str, Any], inventory: dict[str, Any], attestation: dict[str, Any]) -> list[str]:
    errors=[]; occurrences=expected_occurrences(inventory)
    if not typed_equal(matrix.get("source_occurrence_records"),occurrences): errors.append("source_occurrence_projection")
    features=matrix.get("source_feature_records",[])
    expected_oids=sorted({row["blob_oid"] for row in occurrences})
    if len(features)!=15 or [row.get("blob_oid") for row in features]!=expected_oids:
        return errors+["source_feature_identity"]
    by_oid={oid:[row for row in occurrences if row["blob_oid"]==oid] for oid in expected_oids}
    presence={key:0 for key in features[0]["anchors"]}; multiplicity={key:0 for key in presence}
    for row in features:
        oid=row["blob_oid"]; raw=blob(oid); source=raw.decode("utf-8"); tree=ast.parse(source)
        refs=[dict(item) for item in by_oid[oid]]
        inv=next(item for item in inventory["blob_records"] if item["blob_oid"]==oid)
        att=next(item for item in attestation["blob_attestations"] if item["blob_oid"]==oid)
        expected_paths=sorted(item["path"] for item in refs)
        expected_releases=[release for release in RELEASES if any(item["release"]==release for item in refs)]
        expected_roles=sorted({item["role"] for item in refs})
        if not (inv["blob_oid"]==oid and inv["ordinal"]==refs[0]["blob_ordinal"]
                and inv["git_mode"]==refs[0]["git_mode"] and inv["raw_sha256"]==sha(raw)
                and inv["lf_sha256"]==sha(lf_bytes(raw)) and inv["size_bytes"]==len(raw)
                and inv["physical_lines"]==len(source.splitlines()) and inv["occurrence_count"]==len(refs)
                and inv["occurrence_paths"]==expected_paths and inv["release_projection"]==expected_releases
                and inv["role_projection"]==expected_roles): errors.append("inventory_source_crossbind")
        if not (att["blob_oid"]==oid and att["ordinal"]==refs[0]["blob_ordinal"]
                and att["raw_sha256"]==sha(raw) and att["lf_sha256"]==sha(lf_bytes(raw))
                and att["encoding"]=="utf-8" and att["ast_parse"]=="PASS"
                and att["read_status"]=="READ_FULL" and att["unread_lines"]==0
                and att["truncation_unresolved"]==0 and att["line_ranges"]==[[1,len(source.splitlines())]]
                and att["occurrence_projection"]=={"paths":expected_paths,"releases":expected_releases,"roles":expected_roles}):
            errors.append("attestation_source_crossbind")
        expected={"raw_sha256":sha(raw),"lf_sha256":sha(lf_bytes(raw)),"lf_normalization":"CRLF_AND_LONE_CR_TO_LF",
                   "size_bytes":len(raw),"physical_lines":len(source.splitlines()),"encoding":"utf-8","ast_parse":"PASS",
                   "blob_ordinal":by_oid[oid][0]["blob_ordinal"],"git_mode":by_oid[oid][0]["git_mode"],"occurrence_refs":refs,
                   "inventory_binding":{key:inv[key] for key in ("ordinal","blob_oid","git_mode","raw_sha256","lf_sha256","size_bytes","physical_lines","occurrence_count","occurrence_paths","release_projection","role_projection")},
                   "attestation_binding":{key:att[key] for key in ("ordinal","blob_oid","raw_sha256","lf_sha256","encoding","ast_parse","read_status","unread_lines","truncation_unresolved","line_ranges","occurrence_projection","partition","reviewer","review_evidence_sha256","genealogy_sha256")}}
        for key,value in expected.items():
            if not typed_equal(row.get(key),value): errors.append("feature_"+key)
        for key,stored_list in row["anchors"].items():
            if stored_list:
                presence[key]+=1
                multiplicity[key]+=len(stored_list)
                if not isinstance(stored_list,list): errors.append("anchor_list_"+key); continue
                if any(not verify_anchor(tree,source,stored) for stored in stored_list): errors.append("anchor_"+key)
                order=[(item["start_line"],item["end_line"],item["ast_kind"]) for item in stored_list]
                if order!=sorted(order): errors.append("anchor_order_"+key)
    expected_presence={"LOGISTIC_BRANCH":15,"ENTROPY_XI_CLIP":15,"ENTROPY_DEN_FLOOR":15,"REGSOL_EXP_CLIP":1,
        "LOWPASS_DEPENDENCY_FALLBACK":4,"LEGACY_VOLTAGE_SORT":4,"LEGACY_T_INTERPOLATION":4,"LEGACY_OUTPUT_INTERPOLATION":4,
        "POINTWISE_STABLE_SORT":11,"POINTWISE_INVERSE_RESTORE":11,"RESOLUTION_FALLBACK":11,"PAD_FUNCTION":2,"PAD_CALL_SITE":2,"PAD_POINT_CAP":2,
        "ROOT_INPUT_GUARD":8,"ROOT_BRACKET_GUARD":8,"ROOT_ITERATION_LOOP":8,"ROOT_SILENT_MIDPOINT":8,
        "L_V_OVERRIDE_GUARD":15,"MISSING_KINETICS_FALLBACK":15,"NONFINITE_LQ_FALLBACK":15,"OMEGA_DOMAIN_BRANCH":15,"TRANSFER_HELPER":4,
        "RATIO_LOCAL_EXP":4,"POINTWISE_DENSE_THRESHOLD":11,
        "DEFAULT_ENTROPY_EPS":15,"DEFAULT_LAG_DECAY_CAP":11,"DEFAULT_PAD_NLV":2,"DEFAULT_PAD_MAXPTS":2,
        "DEFAULT_PAD_L_OVER_20":2,"DEFAULT_REGSOL_DELTA_FLOOR":1,"DEFAULT_LEGACY_GRID":4,"DEFAULT_ROOT_SOLVER":8}
    if not typed_equal(presence,expected_presence): errors.append("feature_presence:"+repr(presence))
    expected_multiplicity=dict(expected_presence)
    expected_multiplicity.update({"ENTROPY_DEN_FLOOR":23,"PAD_CALL_SITE":4,
        "ROOT_ITERATION_LOOP":16,"OMEGA_DOMAIN_BRANCH":19,"POINTWISE_DENSE_THRESHOLD":15})
    if not typed_equal(multiplicity,expected_multiplicity): errors.append("feature_multiplicity:"+repr(multiplicity))
    optimizer_rows=[item for item in inventory["occurrence_records"] if item["path"].endswith("/fit_roundtrip_demo.py")]
    stored_optimizer=matrix.get("supplemental_optimizer_source_record",{})
    if len(optimizer_rows)!=1:
        errors.append("optimizer_occurrence_count")
    else:
        occurrence=optimizer_rows[0]; oid=occurrence["blob_oid"]; raw=blob(oid); source=raw.decode("utf-8"); tree=ast.parse(source)
        inv=next(item for item in inventory["blob_records"] if item["blob_oid"]==oid)
        att=next(item for item in attestation["blob_attestations"] if item["blob_oid"]==oid)
        if not (inv["blob_oid"]==oid and inv["ordinal"]==occurrence["blob_ordinal"]
                and inv["git_mode"]==occurrence["git_mode"] and inv["raw_sha256"]==sha(raw)
                and inv["lf_sha256"]==sha(lf_bytes(raw)) and inv["size_bytes"]==len(raw)
                and inv["physical_lines"]==len(source.splitlines()) and inv["occurrence_count"]==1
                and inv["occurrence_paths"]==[occurrence["path"]]
                and inv["release_projection"]==[occurrence["release"]]
                and inv["role_projection"]==[occurrence["role"]]): errors.append("optimizer_inventory_crossbind")
        if not (att["blob_oid"]==oid and att["ordinal"]==occurrence["blob_ordinal"]
                and att["raw_sha256"]==sha(raw) and att["lf_sha256"]==sha(lf_bytes(raw))
                and att["encoding"]=="utf-8" and att["ast_parse"]=="PASS"
                and att["read_status"]=="READ_FULL" and att["unread_lines"]==0
                and att["truncation_unresolved"]==0 and att["line_ranges"]==[[1,len(source.splitlines())]]
                and att["occurrence_projection"]=={"paths":[occurrence["path"]],"releases":[occurrence["release"]],"roles":[occurrence["role"]]}):
            errors.append("optimizer_attestation_crossbind")
        expected={key:occurrence[key] for key in ("ordinal","manifest_entry_index","release","path","role","blob_oid","blob_ordinal","git_mode")}
        expected.update({"size_bytes":len(raw),"physical_lines":len(source.splitlines()),"raw_sha256":sha(raw),
                         "lf_sha256":sha(lf_bytes(raw)),"lf_normalization":"CRLF_AND_LONE_CR_TO_LF",
                         "inventory_binding":{key:inv[key] for key in ("ordinal","blob_oid","git_mode","raw_sha256","lf_sha256","size_bytes","physical_lines","occurrence_count","occurrence_paths","release_projection","role_projection")},
                         "attestation_binding":{key:att[key] for key in ("ordinal","blob_oid","raw_sha256","lf_sha256","encoding","ast_parse","read_status","unread_lines","truncation_unresolved","line_ranges","occurrence_projection","partition","reviewer","review_evidence_sha256","genealogy_sha256")}})
        for key,value in expected.items():
            if not typed_equal(stored_optimizer.get(key),value): errors.append("optimizer_"+key)
        for key,items in stored_optimizer.get("anchors",{}).items():
            if not isinstance(items,list) or not items or any(not verify_anchor(tree,source,item) for item in items): errors.append("optimizer_anchor_"+key)
    return errors


def independent_numeric_errors(matrix: dict[str, Any], inputs: dict[str, dict[str, Any]]) -> list[str]:
    errors=[]; rows={row.get("probe_id"):row for row in matrix.get("impact_probe_records",[])}
    if set(rows)!={f"I{i:02d}" for i in range(1,28)}: return ["probe_ids"]
    eps=1e-12
    if rows["I02"]["post_metrics"].get("logit_limit")!=float(format(math.log((1-eps)/eps),".17g")): errors.append("clip_logit")
    if rows["I03"]["delta_metrics"]!={"changed_metrics":[],"reason":"ENTROPY_STATE_CLIP_IS_NOT_A_CURVE_CLIP"}: errors.append("entropy_metric_scope")
    if rows["I04"]["delta_metrics"].get("duplicate_voltage_case")!="NOT_EXECUTED_NOT_CLAIMED": errors.append("duplicate_voltage_authority")
    if rows["I07"]["post_metrics"]["cases"][0].get("returned_npad")!=4000: errors.append("pad_cap")
    if not all(case["original_sample_suffix_preserved"] is True and case["content_suffix_matches_direct"] is True for case in rows["I07"]["post_metrics"]["cases"]): errors.append("pad_execution")
    if rows["I20"]["post_metrics"].get("returned_npad")!=0: errors.append("pad_first_step")
    if rows["I21"]["post_metrics"].get("equal_fallback") is not False or rows["I21"]["post_metrics"].get("nextbelow_fallback") is not True:
        errors.append("resolution_boundary")
    if (rows["I21"]["inputs"].get("release_scope")!="v1.0.15_THROUGH_v1.0.24.1_PRE_PAD_HELPER"
            or rows["I21"]["inputs"].get("padding_before_pointwise_memory") is not False): errors.append("resolution_release_scope")
    if rows["I21"]["delta_metrics"].get("state_lag_max_abs",0.0)<=0.0 or rows["I21"]["delta_metrics"].get("returned_peak_max_abs_delta",0.0)<=0.0:
        errors.append("resolution_curve_delta")
    if any(rows[key]["convergence"] is None or rows[key]["convergence"]["criterion_met"] is not False
           or rows[key]["convergence"]["convergence_authority"] is not False for key in ("I09","I10","I15","I23")): errors.append("success_promotion")
    fit=inputs[FIT_REPLAY_PATH]; selected=[run["trials"][run["best_trial"]] for run in fit["runtime_reproductions"]]
    expected_trial={key:selected[0][key] for key in ("status","success","nfev","njev","optimality","cost")}
    if not typed_equal(rows["I23"]["post_metrics"],expected_trial): errors.append("optimizer_trial_ground")
    if rows["I22"]["status"]!="GROUND_NOT_FOUND_EXECUTABLE_GUARD": errors.append("transfer_guard_promotion")
    regsol=rows["I18"]
    if (not isinstance(regsol["delta_metrics"].get("area"),float) or regsol["delta_metrics"].get("sign_changes")!=0
            or regsol["pre_metrics"].get("sign")!="NONNEGATIVE" or regsol["post_metrics"].get("sign")!="NONNEGATIVE"
            or len(regsol["post_metrics"].get("clip_boundary_continuity",[]))!=2
            or not isinstance(regsol["delta_metrics"].get("clip_boundary_max_one_ulp_jump"),float)
            or regsol["delta_metrics"].get("global_area")!="DIVERGENT_NONZERO_CONSTANT_TAIL"):
        errors.append("regsol_metrics")
    if rows["I24"]["delta_metrics"].get("intended_domain_branch") is not True: errors.append("omega_branch")
    if rows["I11"]["post_metrics"]!={"valid_override":0.02,"invalid_override_exception":"ValueError","missing_or_zero_current_lag_length":0.0,"nonfinite_lq_lag_length":0.0}: errors.append("lag_override")
    if (rows["I08"]["warning_error"]!={"kind":"SOURCE_STATIC_VALUE_ERROR_PATH","observed":False}
            or rows["I08"]["status"]!="SOURCE_STATIC_FAIL_FAST" or rows["I08"]["input_provenance"]!="FROZEN_SOURCE_STATIC_BRANCH"
            or rows["I11"]["input_provenance"]!="FROZEN_SOURCE_STATIC_BRANCH"
            or rows["I11"]["warning_error"].get("observed") is not False): errors.append("static_observation_ceiling")
    for key in ("I25","I26"):
        observations=rows[key]["post_metrics"].get("dual_runtime_observations",[])
        if len(observations)!=2 or [item["payload"]["runtime"]["python_version"][:2] for item in observations]!=[[3,12],[3,14]]: errors.append("runtime_identity_"+key)
    lq_expected={"formula":"abs(dVdq)*L_q before nonfinite-to-zero fallback","dVdq":0.3,"cases":[
        {"dH":-2000000.0,"ln_Lq":-838.3115278411767,"raw_Lq":0.0,"resolver_lag_length":0.0,"warning_categories":[],"overflow_count":0},
        {"dH":0.0,"ln_Lq":-31.475724453991145,"raw_Lq":2.139274703366186e-14,"resolver_lag_length":6.417824110098558e-15,"warning_categories":[],"overflow_count":0},
        {"dH":2000000.0,"ln_Lq":775.3600789331945,"raw_Lq":"POSITIVE_INFINITY","resolver_lag_length":0.0,"warning_categories":["RuntimeWarning"],"overflow_count":1}]}
    ratio_expected={"exponents":[1000.0,0.0,-1000.0],"exp_values":["POSITIVE_INFINITY",1.0,0.0],
        "warning_categories":["RuntimeWarning"],"overflow_count":1,"downstream":[
        {"status":"RETURNED","a":0.0,"state":0.2,"peak":0.0},
        {"status":"RETURNED","a":0.1,"state":0.22902450821575793,"peak":0.5709754917842421},
        {"status":"UNCAUGHT_ZERO_DIVISION","exception":"ZeroDivisionError"}]}
    for probe_id,expected in (("I25",lq_expected),("I26",ratio_expected)):
        observations=rows[probe_id]["post_metrics"]["dual_runtime_observations"]
        projections=[]
        for index,observation in enumerate(observations):
            payload=observation["payload"]; runtime=payload.get("runtime",{})
            projection={key:value for key,value in payload.items() if key!="runtime"}
            if (not typed_equal(projection,expected) or set(payload)!=set(expected)|{"runtime"}
                    or runtime.get("implementation")!="CPython"
                    or runtime.get("python_version",[])[:2] != ([3,12] if index==0 else [3,14])
                    or not all(type(value) is int for value in runtime.get("python_version",[]))):
                errors.append("runtime_payload_"+probe_id)
            projections.append(projection)
        if len(projections)!=2 or not typed_equal(projections[0],projections[1]): errors.append("runtime_cross_version_"+probe_id)
    a=1e-4; below=math.nextafter(a,0.0); prev=0.2; kp=0.2; kc=0.8
    dense=(1-below)*prev+below*0.5*(kc+kp); decay=math.exp(-a); general=decay*prev+kc*(1-decay)-((kc-kp)/a)*(1-(1+a)*decay)
    expected_jump=float(format(general-dense,".17g"))
    if rows["I27"]["delta_metrics"]!={"branch_output_jump":expected_jump,"operator":"<"}: errors.append("pointwise_threshold")
    defaults=matrix.get("numerical_default_records",[])
    expected_defaults=[{"eps":1e-12},{"decay_cap":40.0},{"lag_span":5.0,"lag_step_divisor":20.0,"max_points":4000},
        {"delta_floor":1e-9,"z_clip_lower":-350.0,"z_clip_upper":350.0},
        {"grid_pad_lo":0.15,"grid_pad_hi":0.15,"n_work_min":2048,"min_lag_grid_steps":2.0},
        {"tol":1e-13,"max_iter":200},{"maxfev":20000,"xatol":1e-10,"fatol":1e-14},
        {"xtol":1e-14,"ftol":1e-14,"gtol":1e-14,"max_nfev":5000}]
    if len(defaults)!=8 or any(not typed_equal(row.get("values"),value) for row,value in zip(defaults,expected_defaults)): errors.append("default_values")
    return errors


def artifact_errors(matrix: dict[str, Any], inputs: dict[str, dict[str, Any]]) -> list[str]:
    errors=[]
    literals={"schema_version":"phase067-step88-numerical-guard-impact-v1","artifact":MATRIX_PATH,"phase":67,"step":88,
        "generated_date":DATE,"baseline_commit":BASELINE,"expected_parent":EXPECTED_PARENT,"branch":BRANCH,
        "expected_subject":SUBJECT,"gate":GATE,"persistence_terminal":PERSISTENCE,"precommit_status":"PASS_PENDING_PERSISTENCE",
        "containing_commit":"PENDING_AT_PRECOMMIT_BY_DESIGN","result_first":True,"json_output_last":True}
    if set(matrix)!=TOP_KEYS: errors.append("top_keys")
    for key,value in literals.items():
        if not typed_equal(matrix.get(key),value): errors.append("metadata_"+key)
    if matrix.get("semantic_sha256")!=semantic(matrix): errors.append("semantic")
    for key,expected in SECTION_SHA256.items():
        if expected!="PENDING" and section_digest(matrix.get(key))!=expected: errors.append("section_"+key)
    if any(item.startswith("section_") for item in errors):
        return sorted(set(errors))
    errors.extend(independent_source_errors(matrix,inputs[INVENTORY_PATH],inputs[ATTESTATION_PATH]))
    errors.extend(independent_numeric_errors(matrix,inputs))
    for key,count in (("guard_records",24),("impact_probe_records",27),("numerical_default_records",8),("candidate_disposition_records",84),("optimizer_route_records",3)):
        if len(matrix.get(key,[]))!=count: errors.append(key+"_count")
    universe=matrix.get("universe",{})
    expected_universe={"all_python_occurrences":129,"all_python_unique_blobs":84,
        "production_occurrences":20,"production_unique_blobs":15,"nonproduction_occurrences_total":109,
        "supplemental_nonproduction_occurrences_selected":1,"excluded_nonproduction_occurrences":108,
        "guard_records":24,"impact_probe_records":27,"numerical_default_records":8,
        "optimizer_route_records":3,"candidate_disposition_records":84,"release_count":20}
    if not typed_equal(universe,expected_universe): errors.append("universe")
    scope=matrix.get("scope_policy",{})
    if scope.get("nonproduction_projection_invariant")!="109_TOTAL_EQUALS_1_SELECTED_OPTIMIZER_PLUS_108_EXCLUDED": errors.append("scope_nonproduction")
    if scope.get("intentionally_unlinked_probe_ids")!=["I16"]: errors.append("scope_intentional_unlinked")
    if [row.get("guard_id") for row in matrix.get("guard_records",[])]!=[f"G{i:02d}" for i in range(1,25)]: errors.append("guard_ids")
    if [row.get("probe_id") for row in matrix.get("impact_probe_records",[])]!=[f"I{i:02d}" for i in range(1,28)]: errors.append("probe_ids_order")
    guards={row.get("family"):row for row in matrix.get("guard_records",[])}
    probes_by_id={row.get("probe_id"):row for row in matrix.get("impact_probe_records",[])}
    linked_probe_ids={probe_id for guard in matrix.get("guard_records",[]) for probe_id in guard.get("probe_ids",[])}
    if linked_probe_ids!=set(probes_by_id)-{"I16"}: errors.append("guard_probe_completeness")
    for guard in matrix.get("guard_records",[]):
        for probe_id in guard.get("probe_ids",[]):
            if probe_id not in probes_by_id or not (set(guard.get("source_feature_ids",[])) & set(probes_by_id[probe_id].get("source_feature_ids",[]))):
                errors.append("guard_probe_feature_crosswire")
    if guards.get("MISSING_KINETICS",{}).get("fallback_is_intended_behavior") is not True: errors.append("missing_kinetics_intended")
    if guards.get("NONFINITE_KINETICS",{}).get("fallback_is_intended_behavior") is not False: errors.append("nonfinite_kinetics_not_intended")
    routes=matrix.get("optimizer_route_records",[])
    if len(routes)==3 and (routes[0].get("kind")!="BACKEND_SELECTION" or routes[1].get("kind")!="DEMO_TERMINATION_CONVERGENCE"
                           or routes[0].get("convergence_claim") is not False or routes[1].get("convergence_authority") is not False): errors.append("optimizer_route_separation")
    authority=matrix.get("authority",{})
    if any(authority.get(key) is not False for key in ("production_modified","external_scientific","material","experimental","canonical","publication")): errors.append("authority_promotion")
    return sorted(set(errors))


def reseal(value: dict[str, Any]) -> None:
    value["semantic_sha256"]=semantic(value)


def put(mapping: Any, key: Any, value: Any) -> None:
    mapping[key]=value


def negative_controls(matrix: dict[str, Any], inputs: dict[str, dict[str, Any]]) -> tuple[int,int]:
    controls=[
        ("root_midpoint_success",lambda x:put(x["impact_probe_records"][8]["convergence"],"criterion_met",True)),
        ("optimizer_return_success",lambda x:put(x["impact_probe_records"][14]["convergence"],"convergence_authority",True)),
        ("selected_trial_success",lambda x:put(x["impact_probe_records"][22]["post_metrics"],"runtime_success",True)),
        ("fallback_intended",lambda x:put(x["guard_records"][10],"fallback_is_intended_behavior",True)),
        ("missing_kinetics_not_intended",lambda x:put(x["guard_records"][9],"fallback_is_intended_behavior",False)),
        ("entropy_clip_curve",lambda x:put(x["impact_probe_records"][1],"interpretation","dQ/dV curve clipped")),
        ("regsol_area_crosswire",lambda x:put(x["impact_probe_records"][17]["pre_metrics"],"area",999.0)),
        ("pad_cap",lambda x:put(x["impact_probe_records"][6]["post_metrics"]["cases"][0],"returned_npad",3999)),
        ("pad_first_step",lambda x:put(x["impact_probe_records"][19]["post_metrics"],"returned_npad",1)),
        ("resolution_operator",lambda x:put(x["impact_probe_records"][20]["delta_metrics"],"strict_operator","<=")),
        ("resolution_pad_scope_promotion",lambda x:put(x["impact_probe_records"][20]["inputs"],"padding_before_pointwise_memory",True)),
        ("transfer_guard_promotion",lambda x:put(x["impact_probe_records"][21],"status","PASS_BOUNDED_INTERNAL")),
        ("omega_fallback",lambda x:put(x["impact_probe_records"][23]["delta_metrics"],"fallback",True)),
        ("before_after_swap",lambda x:x["impact_probe_records"][17].update({"pre_metrics":x["impact_probe_records"][17]["post_metrics"],"post_metrics":x["impact_probe_records"][17]["pre_metrics"]})),
        ("sort_crosswire",lambda x:put(x["impact_probe_records"][3]["post_metrics"],"sort_indices",[0,1,2])),
        ("duplicate_voltage_promotion",lambda x:put(x["impact_probe_records"][3]["delta_metrics"],"duplicate_voltage_case","RUNTIME_CONFIRMED")),
        ("tie_order",lambda x:put(x["impact_probe_records"][18]["post_metrics"],"equal_tie_order",["a","b"])),
        ("lq_overflow_success",lambda x:put(x["impact_probe_records"][24],"probe_evaluation_passed",True)),
        ("ratio_overflow_success",lambda x:put(x["impact_probe_records"][25],"probe_evaluation_passed",True)),
        ("small_a_operator",lambda x:put(x["impact_probe_records"][26]["delta_metrics"],"operator","<=")),
        ("direct_lv_invalid_accept",lambda x:put(x["impact_probe_records"][10]["post_metrics"],"invalid_override_exception","NONE")),
        ("root_failure_observed_promotion",lambda x:put(x["impact_probe_records"][7]["warning_error"],"observed",True)),
        ("pad_content_claim",lambda x:put(x["impact_probe_records"][5]["delta_metrics"],"content_re_evaluated",False)),
        ("probe_delete",lambda x:x["impact_probe_records"].pop()),
        ("probe_duplicate",lambda x:x["impact_probe_records"].append(copy.deepcopy(x["impact_probe_records"][0]))),
        ("probe_order",lambda x:x["impact_probe_records"].reverse()),
        ("guard_delete",lambda x:x["guard_records"].pop()),
        ("guard_crosswire",lambda x:put(x["guard_records"][0],"probe_ids",["I25"])),
        ("guard_entropy_crosswire",lambda x:x["guard_records"][0]["probe_ids"].append("I03")),
        ("guard_nonfinite_drop",lambda x:put(x["guard_records"][10],"probe_ids",["I11"])),
        ("intentional_unlinked_probe_drift",lambda x:put(x["scope_policy"],"intentionally_unlinked_probe_ids",[])),
        ("occurrence_release",lambda x:put(x["source_occurrence_records"][0],"release","v1.0.11")),
        ("occurrence_blob",lambda x:put(x["source_occurrence_records"][0],"blob_oid",x["source_occurrence_records"][2]["blob_oid"])),
        ("feature_raw",lambda x:put(x["source_feature_records"][0],"raw_sha256","0"*64)),
        ("feature_lf",lambda x:put(x["source_feature_records"][0],"lf_sha256","f"*64)),
        ("feature_anchor_line",lambda x:put(next(v for v in x["source_feature_records"][0]["anchors"].values() if v)[0],"start_line",1)),
        ("feature_anchor_drop",lambda x:next(v for v in x["source_feature_records"][-1]["anchors"].values() if v).pop()),
        ("feature_inventory_binding",lambda x:put(x["source_feature_records"][0]["inventory_binding"],"size_bytes",0)),
        ("feature_inventory_projection",lambda x:put(x["source_feature_records"][0]["inventory_binding"],"role_projection",["demo"])),
        ("feature_attestation_status",lambda x:put(x["source_feature_records"][0]["attestation_binding"],"read_status","READ_PARTIAL")),
        ("feature_attestation_occurrence_projection",lambda x:put(x["source_feature_records"][0]["attestation_binding"]["occurrence_projection"],"roles",["demo"])),
        ("optimizer_inventory_projection",lambda x:put(x["supplemental_optimizer_source_record"]["inventory_binding"],"occurrence_count",2)),
        ("optimizer_attestation_line_ranges",lambda x:put(x["supplemental_optimizer_source_record"]["attestation_binding"],"line_ranges",[[1,1]])),
        ("feature_extra",lambda x:put(x["source_feature_records"][0],"extra",True)),
        ("candidate_select",lambda x:put(x["candidate_disposition_records"][0],"selected_for_step88",not x["candidate_disposition_records"][0]["selected_for_step88"])),
        ("optimizer_backend_converged",lambda x:put(x["optimizer_route_records"][0],"convergence_claim",True)),
        ("sol_x_success",lambda x:put(x["optimizer_route_records"][1],"success_flag_checked",True)),
        ("nm_exhaustion_success",lambda x:put(x["optimizer_route_records"][1],"convergence_authority",True)),
        ("step77_vector_success",lambda x:put(x["optimizer_route_records"][2],"convergence_authority",True)),
        ("runtime_version",lambda x:put(x["impact_probe_records"][0]["post_metrics"][0]["payload"]["runtime"]["python_version"],2,0)),
        ("runtime_stderr",lambda x:put(x["impact_probe_records"][24]["post_metrics"]["dual_runtime_observations"][0],"stderr_sha256","0"*64)),
        ("lq_runtime_full_reseal",lambda x:put(x["impact_probe_records"][24]["post_metrics"]["dual_runtime_observations"][0]["payload"]["cases"][1],"resolver_lag_length",0.0)),
        ("ratio_runtime_full_reseal",lambda x:put(x["impact_probe_records"][25]["post_metrics"]["dual_runtime_observations"][1]["payload"]["downstream"][0],"state",0.3)),
        ("resolution_peak_crosswire",lambda x:put(x["impact_probe_records"][20]["post_metrics"],"nextbelow_returned_peak_shape",x["impact_probe_records"][20]["post_metrics"]["equality_memory_state"])),
        ("regsol_boundary_delta",lambda x:put(x["impact_probe_records"][17]["delta_metrics"],"clip_boundary_max_one_ulp_jump",1.0)),
        ("default_value",lambda x:put(x["numerical_default_records"][0]["values"],"eps",1e-9)),
        ("default_anchor_crosswire",lambda x:x["numerical_default_records"][2]["source_feature_ids"].reverse()),
        ("default_extra",lambda x:put(x["numerical_default_records"][0],"extra",True)),
        ("authority_science",lambda x:put(x["authority"],"external_scientific",True)),
        ("bool_int_type",lambda x:put(x["validation"],"typed_schema",1)),
        ("int_float_type",lambda x:put(x["universe"],"guard_records",24.0)),
        ("nested_extra",lambda x:put(x["coverage"],"extra",False)),
        ("schema_version",lambda x:put(x,"schema_version","wrong")),
    ]
    passed=0
    for name,mutate in controls:
        candidate=copy.deepcopy(matrix); before=canonical(candidate); mutate(candidate)
        require(canonical(candidate)!=before,"E_NEGATIVE_NOOP",name); reseal(candidate)
        if artifact_errors(candidate,inputs): passed+=1
        else: raise ValidationError("E_NEGATIVE_FALSE_PASS:"+name)
    candidate=copy.deepcopy(matrix);candidate["semantic_sha256"]="0"*64
    if artifact_errors(candidate,inputs): passed+=1
    else: raise ValidationError("E_NEGATIVE_FALSE_PASS:semantic_only")
    return passed,len(controls)+1


def json_controls() -> tuple[int,int]:
    probes=[
        (b'{"a":1,"a":2}\n', {}),
        (b'{"x":NaN}\n', {}),
        (b'{"x":Infinity}\n', {}),
        (b'{"x":1}\n ', {}),
        (b" " * (MAX_JSON_BYTES + 1), {}),
        ((b'{"x":' * (MAX_JSON_DEPTH + 1)) + b"0" + (b"}" * (MAX_JSON_DEPTH + 1)) + b"\n", {}),
        (b'{"x":[0,1,2]}\n', {"max_nodes": 3}),
    ];passed=0
    for raw, limits in probes:
        try: strict_load(raw,"E_JSON_NEGATIVE",True,**limits)
        except ValidationError: passed+=1
    return passed,len(probes)


def neutral_source_hash(path: Path, constant: str) -> str:
    text=lf_bytes(path.read_bytes()).decode("utf-8")
    replaced,count=re.subn(rf'^{constant} = "[0-9a-f]{{64}}"$',f'{constant} = "'+"0"*64+'"',text,flags=re.MULTILINE)
    require(count==1,"E_SOURCE_PIN_CARDINALITY",constant)
    return sha(replaced.encode("utf-8"))


def source_policy_errors(source: str, role: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return ["E_AST_PARSE:" + str(exc)]
    parents = {child: parent for parent in ast.walk(tree)
               for child in ast.iter_child_nodes(parent)}
    owners: dict[ast.AST, str] = {}
    for node in ast.walk(tree):
        cursor = parents.get(node)
        owner = "<module>"
        while cursor is not None:
            if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                owner = cursor.name
                break
            cursor = parents.get(cursor)
        owners[node] = owner

    expected_functions = {
        "builder": [
            ("<module>", name) for name in (
                "require", "sha", "lf_bytes", "canonical", "semantic",
                "predecessor_semantic", "finish", "strict_json", "git_bytes",
                "input_json", "blob", "stable_ast", "qualified_owner", "anchor",
                "find_anchors", "source_features", "optimizer_source_record",
                "production_projection", "rounded", "logistic", "trap",
                "dual_numpy_observation", "require_dual_payload",
                "logistic_runtime_observation", "lq_runtime_observation",
                "ratio_exp_runtime_observation", "np_interp_like", "probe_records",
                "guard_records", "numerical_default_records", "candidate_dispositions",
                "optimizer_routes", "build", "atomic_write", "main",
            )
        ] + [
            ("strict_json", "pairs"), ("qualified_owner", "walk"),
            ("probe_records", "regsol_density"),
            ("probe_records", "peak_monotonicity_violations"),
            ("probe_records", "dense"), ("probe_records", "general"),
            ("probe_records", "probe_row"),
        ],
        "validator": [
            ("<module>", name) for name in (
                "require", "sha", "lf_bytes", "canonical", "semantic",
                "predecessor_semantic", "typed_equal", "finite_tree", "strict_load",
                "is_oid", "git_argv_allowed", "git", "gtext", "blob", "stable_ast",
                "qualified_owner", "verify_anchor", "load_inputs", "section_digest",
                "expected_occurrences", "independent_source_errors",
                "independent_numeric_errors", "artifact_errors", "reseal", "put",
                "negative_controls", "json_controls", "neutral_source_hash",
                "source_policy_errors", "source_policy_controls", "source_policy",
                "control_document_errors", "control_documents", "parse_porcelain",
                "parse_name_status", "canonical_origin", "live", "repository_refs",
                "status", "index_snapshot", "seal", "verify_artifacts",
                "verify_content", "verify_staged", "verify_persistence",
                "git_argv_controls", "main",
            )
        ] + [
            ("strict_load", "pairs"),
            ("qualified_owner", "walk"),
            ("control_document_errors", "unique_line"),
        ],
    }[role]
    observed_functions = [
        (owners[node], node.name) for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    if sorted(observed_functions) != sorted(expected_functions):
        errors.append("E_FUNCTION_INVENTORY")
    expected_classes = {"builder": ["BuildError"], "validator": ["ValidationError"]}[role]
    observed_classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    if observed_classes != expected_classes:
        errors.append("E_CLASS_INVENTORY")

    imports: list[str] = []
    from_imports: list[tuple[str, tuple[str, ...]]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if parents.get(node) is not tree:
                errors.append("E_NESTED_IMPORT")
            for alias in node.names:
                imports.append(alias.name)
                if alias.asname is not None:
                    errors.append("E_IMPORT_ALIAS")
        elif isinstance(node, ast.ImportFrom):
            if parents.get(node) is not tree or node.level != 0:
                errors.append("E_NESTED_FROM_IMPORT")
            from_imports.append((node.module or "", tuple(alias.name for alias in node.names)))
            if any(alias.asname is not None or alias.name == "*" for alias in node.names):
                errors.append("E_FROM_IMPORT_ALIAS")
    expected_imports = {
        "builder": ["argparse", "ast", "bisect", "hashlib", "json", "math", "os", "subprocess", "sys"],
        "validator": ["argparse", "ast", "copy", "hashlib", "json", "math", "re", "subprocess", "sys"],
    }[role]
    expected_from = [("__future__", ("annotations",)), ("pathlib", ("Path",)),
                     ("typing", ("Any", "Callable"))]
    if sorted(imports) != sorted(expected_imports):
        errors.append("E_IMPORT_INVENTORY")
    if sorted(from_imports) != sorted(expected_from):
        errors.append("E_FROM_IMPORT_INVENTORY")

    annotation_nodes: set[ast.AST] = set()
    for node in ast.walk(tree):
        annotations: list[ast.AST] = []
        if isinstance(node, ast.arg) and node.annotation is not None:
            annotations.append(node.annotation)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.returns is not None:
            annotations.append(node.returns)
        elif isinstance(node, ast.AnnAssign) and node.annotation is not None:
            annotations.append(node.annotation)
        for annotation in annotations:
            annotation_nodes.update(ast.walk(annotation))

    protected = {"argparse", "subprocess", "os", "sys", "Path", "git", "git_bytes", "gtext",
                 "live", "atomic_write", "eval", "exec", "compile", "__import__",
                 "open", "__builtins__"}
    sensitive = {"eval", "exec", "compile", "__import__", "open", "setattr",
                 "delattr", "globals", "locals", "vars", "__builtins__"}
    protected_callables = {"git", "git_bytes", "gtext", "live", "atomic_write"}
    allowed_name_calls = {
        "abs", "all", "any", "bool", "bytes", "dict", "enumerate", "float",
        "format", "int", "isinstance", "len", "list", "max", "min", "next",
        "object", "print", "range", "repr", "set", "sorted", "str", "sum",
        "tuple", "type", "zip", "Path", "SystemExit", "ValueError", "BuildError",
        "ValidationError",
    }
    top_level_function_names = {name for owner, name in expected_functions if owner == "<module>"}
    nested_function_names = {name for owner, name in expected_functions if owner != "<module>"}
    declared_function_names = top_level_function_names | nested_function_names
    reserved_bindings = protected | set(allowed_name_calls) | declared_function_names
    allowed_name_calls.update(top_level_function_names)
    allowed_callbacks = {
        "builder": {("find_anchors", "predicate"), ("probe_records", "regsol_density"),
                    ("probe_records", "peak_monotonicity_violations"),
                    ("probe_records", "probe_row"), ("probe_records", "dense"),
                    ("probe_records", "general"), ("qualified_owner", "walk"),
                    ("walk", "walk")},
        "validator": {("negative_controls", "mutate"),
                      ("control_document_errors", "unique_line"),
                      ("qualified_owner", "walk"),
                      ("walk", "walk")},
    }[role]

    subprocess_calls: list[tuple[str, str]] = []
    argparse_calls: list[tuple[str, str]] = []
    module_attributes: list[tuple[str, str]] = []
    mutation_calls: list[tuple[str, str]] = []
    replace_calls: list[tuple[str, str]] = []
    getattr_calls: list[tuple[str, str]] = []
    git_calls: list[tuple[str, str]] = []
    gtext_calls: list[tuple[str, str]] = []
    live_calls: list[tuple[str, str]] = []
    atomic_calls: list[tuple[str, str]] = []
    path_calls: list[tuple[str, str]] = []
    filesystem_read_calls: list[tuple[str, str]] = []
    mutation_names = {"open", "write", "writelines", "write_text", "write_bytes",
                      "flush", "fileno", "unlink", "rmdir", "rename", "remove",
                      "removedirs", "renames", "mkdir", "touch", "chmod", "chown",
                      "truncate", "symlink_to", "hardlink_to", "link_to", "fsync"}
    process_names = {"Popen", "call", "check_call", "check_output", "system", "popen",
                     "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve",
                     "spawnvp", "spawnvpe"}
    filesystem_read_names = {"read_bytes", "read_text"}

    for node in ast.walk(tree):
        owner = owners[node]
        if isinstance(node, ast.arg) and node.arg in reserved_bindings:
            errors.append("E_PROTECTED_ARGUMENT:" + node.arg + ":" + owner)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in reserved_bindings:
            errors.append("E_PROTECTED_REBIND:" + node.id + ":" + owner)
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            if isinstance(node.value, ast.Name) and node.value.id in {"argparse", "subprocess", "os", "sys"}:
                errors.append("E_PROTECTED_ATTRIBUTE_REBIND:" + node.value.id + "." + node.attr)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            parent = parents.get(node)
            if node.id in sensitive:
                errors.append("E_SENSITIVE_NAME:" + node.id + ":" + owner)
            if node.id in {"argparse", "subprocess", "os", "sys"}:
                if not isinstance(parent, ast.Attribute) or parent.value is not node:
                    errors.append("E_MODULE_VALUE_ESCAPE:" + node.id + ":" + owner)
            if node.id == "Path" and node not in annotation_nodes:
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_PATH_VALUE_ESCAPE:" + owner)
            if node.id in protected_callables:
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_CALLABLE_ESCAPE:" + node.id + ":" + owner)
            if node.id in declared_function_names:
                direct = isinstance(parent, ast.Call) and parent.func is node
                pairs_hook = (node.id == "pairs" and owner in {"strict_json", "strict_load"}
                              and isinstance(parent, ast.keyword)
                              and parent.arg == "object_pairs_hook")
                if not direct and not pairs_hook:
                    errors.append("E_DECLARED_CALLABLE_TRANSPORT:" + node.id + ":" + owner)
        if isinstance(node, ast.Attribute):
            parent = parents.get(node)
            if node.attr in mutation_names | {"replace"} | filesystem_read_names:
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_SENSITIVE_ATTRIBUTE_TRANSPORT:" + node.attr + ":" + owner)
            if node.attr.startswith("__"):
                allowed_dunder = (
                    node.attr == "__name__" and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name) and node.value.func.id == "type"
                )
                if not allowed_dunder:
                    errors.append("E_DUNDER_ATTRIBUTE:" + node.attr + ":" + owner)
            if isinstance(node.value, ast.Name) and node.value.id in {"argparse", "subprocess", "os", "sys"}:
                module_attributes.append((owner, ast.unparse(node)))
                parent = parents.get(node)
                if node.attr not in {"PIPE", "stderr"}:
                    if not isinstance(parent, ast.Call) or parent.func is not node:
                        errors.append("E_MODULE_CALLABLE_ESCAPE:" + ast.unparse(node) + ":" + owner)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                errors.append("E_INDIRECT_CALL:" + owner)
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name == "getattr":
                    getattr_calls.append((owner, ast.unparse(node)))
                elif name not in allowed_name_calls and (owner, name) not in allowed_callbacks:
                    errors.append("E_UNKNOWN_NAME_CALL:" + name + ":" + owner)
                if name == "git_bytes":
                    git_calls.append((owner, ast.unparse(node)))
                elif name == "git":
                    git_calls.append((owner, ast.unparse(node)))
                elif name == "gtext":
                    gtext_calls.append((owner, ast.unparse(node)))
                elif name == "live":
                    live_calls.append((owner, ast.unparse(node)))
                elif name == "atomic_write":
                    atomic_calls.append((owner, ast.unparse(node)))
                if name == "Path":
                    path_calls.append((owner, ast.unparse(node)))
            elif isinstance(node.func, ast.Attribute):
                attr = node.func.attr
                if attr in mutation_names:
                    mutation_calls.append((owner, ast.unparse(node)))
                if attr == "replace":
                    replace_calls.append((owner, ast.unparse(node)))
                    if isinstance(node.func.value, ast.Call) and isinstance(node.func.value.func, ast.Name) and node.func.value.func.id == "Path":
                        errors.append("E_PATH_REPLACE_MUTATION:" + owner)
                if attr in filesystem_read_names:
                    filesystem_read_calls.append((owner, ast.unparse(node)))
                if attr in process_names:
                    errors.append("E_PROCESS_API:" + attr + ":" + owner)
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    subprocess_calls.append((owner, ast.unparse(node)))
                    if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant)
                           and keyword.value.value is True for keyword in node.keywords):
                        errors.append("E_SHELL_EXECUTION:" + owner)
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "argparse":
                    argparse_calls.append((owner, ast.unparse(node)))

    expected_module_attributes = {
        "builder": [
            ("main", "argparse.ArgumentParser"),
            ("atomic_write", "os.fsync"), ("atomic_write", "os.replace"),
            ("dual_numpy_observation", "subprocess.PIPE"),
            ("dual_numpy_observation", "subprocess.PIPE"),
            ("dual_numpy_observation", "subprocess.run"),
            ("git_bytes", "subprocess.PIPE"), ("git_bytes", "subprocess.PIPE"),
            ("git_bytes", "subprocess.run"), ("<module>", "sys.stderr"),
        ],
        "validator": [
            ("main", "argparse.ArgumentParser"),
            ("git", "subprocess.PIPE"), ("git", "subprocess.PIPE"),
            ("git", "subprocess.run"), ("<module>", "sys.stderr"),
        ],
    }[role]
    expected_argparse_calls = {
        "builder": [("main", "argparse.ArgumentParser()")],
        "validator": [("main", "argparse.ArgumentParser()")],
    }[role]
    expected_subprocess_calls = {
        "builder": [
            ("git_bytes", "subprocess.run(['git', *args], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
            ("dual_numpy_observation", "subprocess.run(argv, cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)"),
        ],
        "validator": [
            ("git", "subprocess.run(['git', *args], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
        ],
    }[role]
    expected_mutations = {
        "builder": [
            ("atomic_write", "temp.open('xb')"), ("atomic_write", "handle.write(raw)"),
            ("atomic_write", "handle.flush()"), ("atomic_write", "handle.fileno()"),
            ("atomic_write", "os.fsync(handle.fileno())"), ("atomic_write", "temp.unlink()"),
        ],
        "validator": [],
    }[role]
    expected_replaces = {
        "builder": [
            ("lf_bytes", "raw.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')"),
            ("lf_bytes", "raw.replace(b'\\r\\n', b'\\n')"),
            ("atomic_write", "os.replace(temp, path)"),
        ],
        "validator": [
            ("lf_bytes", "raw.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')"),
            ("lf_bytes", "raw.replace(b'\\r\\n', b'\\n')"),
            ("control_documents", "candidate[PARENT_LEDGER].replace(phase_row, phase_row.replace(EXPECTED_PARENT, 'PENDING_AT_PRECOMMIT_BY_DESIGN'), 1)"),
            ("control_documents", "phase_row.replace(EXPECTED_PARENT, 'PENDING_AT_PRECOMMIT_BY_DESIGN')"),
            ("control_documents", "candidate[HANDOVER].replace('PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md', 'PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md', 1)"),
            ("parse_porcelain", "line[3:].replace('\\\\', '/')"),
            ("parse_name_status", "parts[i + 1].replace('\\\\', '/')"),
            ("canonical_origin", "value.lower().replace('https://', '').replace('http://', '')"),
            ("canonical_origin", "value.lower().replace('https://', '')"),
            ("index_snapshot", "path.replace('\\\\', '/')"),
        ],
    }[role]
    expected_getattr = {
        "builder": [("stable_ast", "getattr(value, field, None)")],
        "validator": [
            ("stable_ast", "getattr(value, field, None)"),
            ("verify_anchor", "getattr(node, 'lineno', None)"),
            ("verify_anchor", "getattr(node, 'end_lineno', None)"),
        ],
    }[role]
    expected_git_calls = {
        "builder": [
            ("input_json", "git_bytes(['show', f'{EXPECTED_PARENT}:{path}'])"),
            ("blob", "git_bytes(['cat-file', 'blob', oid])"),
        ],
        "validator": [
            ("blob", "git(('cat-file', 'blob', oid))"),
            ("load_inputs", "git(('show', f'{EXPECTED_PARENT}:{path}'))"),
            ("status", "git(('status', '--porcelain=v1', '--untracked-files=all'))"),
            ("verify_content", "git(('diff', '--cached', '--name-status', '-z'))"),
            ("verify_staged", "git(('diff', '--cached', '--name-status', '-z', EXPECTED_PARENT, '--'))"),
            ("verify_persistence", "git(('diff-tree', '--no-commit-id', '--name-status', '-r', '-z', commit + '^', commit, '--'))"),
            ("gtext", "git(args, allow_failure)"),
            ("index_snapshot", "git(('ls-files', '-s', '-z'))"),
        ],
    }[role]
    expected_gtext = {
        "builder": [],
        "validator": [
            ("repository_refs", "gtext(('rev-parse', 'HEAD'))"),
            ("repository_refs", "gtext(('rev-parse', '--abbrev-ref', 'HEAD'))"),
            ("repository_refs", "gtext(('rev-parse', '--abbrev-ref', '@{upstream}'))"),
            ("repository_refs", "gtext(('rev-parse', '@{upstream}'))"),
            ("repository_refs", "gtext(('rev-parse', f'refs/remotes/origin/{BRANCH}'))"),
            ("repository_refs", "gtext(('show-ref', '--verify', '--hash', 'refs/heads/codex/lib-physics-endgame-v1025_2'))"),
            ("repository_refs", "gtext(('rev-parse', 'refs/remotes/origin/codex/lib-physics-endgame-v1025_2'))"),
            ("repository_refs", "gtext(('show-ref', '--verify', '--hash', 'refs/heads/main'), True)"),
            ("repository_refs", "gtext(('rev-parse', 'refs/remotes/origin/main'))"),
            ("repository_refs", "gtext(('merge-base', EXPECTED_PARENT, MAIN_TIP))"),
            ("live", "gtext(('ls-remote', '--heads', 'origin', ref))"),
            ("repository_refs", "gtext(('diff', '--name-only', f'{MAIN_BASE_TIP}..{MAIN_TIP}', '--'))"),
            ("repository_refs", "gtext(('remote', 'get-url', 'origin'))"),
            ("repository_refs", "gtext(('rev-list', '--count', f'{MAIN_BASE_TIP}..{MAIN_TIP}'))"),
            ("verify_content", "gtext(('diff', '--name-only', EXPECTED_PARENT, '--', 'Claude'))"),
            ("verify_staged", "gtext(('rev-parse', 'HEAD'))"),
            ("verify_staged", "gtext(('show', '--no-patch', '--format=%P', staged_head))"),
            ("verify_staged", "gtext(('show', '--no-patch', '--format=%s', staged_head))"),
            ("verify_staged", "gtext(('diff', '--name-only', EXPECTED_PARENT, '--', 'Claude'))"),
            ("verify_staged", "gtext(('diff', '--name-only', '--'))"),
            ("verify_persistence", "gtext(('show', '--no-patch', '--format=%s', commit))"),
            ("verify_persistence", "gtext(('diff', '--name-only', EXPECTED_PARENT, '--', 'Claude'))"),
            ("verify_persistence", "gtext(('show', '--no-patch', '--format=%P', commit))"),
        ],
    }[role]
    expected_live = {
        "builder": [],
        "validator": [
            ("repository_refs", "live(f'refs/heads/{BRANCH}')"),
            ("repository_refs", "live('refs/heads/codex/lib-physics-endgame-v1025_2')"),
            ("repository_refs", "live('refs/heads/main')"),
        ],
    }[role]
    expected_atomic = {
        "builder": [("main", "atomic_write(ROOT / OUTPUT_PATH, canonical(first))")],
        "validator": [],
    }[role]
    expected_path_calls = {
        "builder": [("<module>", "Path(__file__)"), ("build", "Path(path)")],
        "validator": [("<module>", "Path(__file__)")],
    }[role]
    expected_filesystem_reads = {
        "builder": [],
        "validator": [
            ("neutral_source_hash", "path.read_bytes()"),
            ("source_policy", "builder.read_bytes()"),
            ("source_policy", "validator.read_bytes()"),
            ("control_documents", "(ROOT / path).read_bytes()"),
            ("seal", "(ROOT / path).read_bytes()"),
            ("verify_artifacts", "(ROOT / MATRIX_PATH).read_bytes()"),
        ],
    }[role]

    inventories = [
        (module_attributes, expected_module_attributes, "E_MODULE_ATTRIBUTE_INVENTORY"),
        (argparse_calls, expected_argparse_calls, "E_ARGPARSE_CALL_INVENTORY"),
        (subprocess_calls, expected_subprocess_calls, "E_SUBPROCESS_INVENTORY"),
        (mutation_calls, expected_mutations, "E_MUTATION_INVENTORY"),
        (replace_calls, expected_replaces, "E_REPLACE_INVENTORY"),
        (getattr_calls, expected_getattr, "E_GETATTR_INVENTORY"),
        (git_calls, expected_git_calls, "E_GIT_CALL_INVENTORY"),
        (gtext_calls, expected_gtext, "E_GTEXT_CALL_INVENTORY"),
        (live_calls, expected_live, "E_LIVE_CALL_INVENTORY"),
        (atomic_calls, expected_atomic, "E_ATOMIC_CALL_INVENTORY"),
        (path_calls, expected_path_calls, "E_PATH_CALL_INVENTORY"),
        (filesystem_read_calls, expected_filesystem_reads, "E_FILESYSTEM_READ_INVENTORY"),
    ]
    for observed, expected, code in inventories:
        if sorted(observed) != sorted(expected):
            errors.append(code)
    return errors


def source_policy_controls(builder_source: str, validator_source: str) -> tuple[int, int]:
    parser_marker = "\n    parser = argparse.ArgumentParser()"
    builder_parser_index = builder_source.rindex(parser_marker)
    validator_parser_index = validator_source.rindex(parser_marker)
    probes = [
        ("shell_true", validator_source + "\ndef injected(): subprocess.run(['git'], shell=True)\n", "validator", "E_SHELL_EXECUTION"),
        ("popen", builder_source + "\ndef injected(): subprocess.Popen(['x'])\n", "builder", "E_PROCESS_API"),
        ("os_system", builder_source + "\ndef injected(): os.system('x')\n", "builder", "E_PROCESS_API"),
        ("filesystem_write", validator_source + "\ndef injected(): Path('x').write_text('x')\n", "validator", "E_MUTATION_INVENTORY"),
        ("path_replace", builder_source + "\ndef injected(): Path('x').replace('y')\n", "builder", "E_PATH_REPLACE_MUTATION"),
        ("callable_alias", validator_source + "\ndef injected():\n    runner=subprocess.run\n    runner(['git'])\n", "validator", "E_MODULE_CALLABLE_ESCAPE"),
        ("module_alias", builder_source + "\ndef injected():\n    module=subprocess\n    module.run(['x'])\n", "builder", "E_MODULE_VALUE_ESCAPE"),
        ("dynamic_alias", validator_source + "\ndef injected():\n    hidden=__import__\n    hidden('os')\n", "validator", "E_SENSITIVE_NAME"),
        ("from_process_import", builder_source + "\nfrom subprocess import Popen\n", "builder", "E_FROM_IMPORT_INVENTORY"),
        ("indirect_lambda", validator_source + "\ndef injected(): (lambda: 0)()\n", "validator", "E_INDIRECT_CALL"),
        ("dunder", builder_source + "\ndef injected(): return object().__class__\n", "builder", "E_DUNDER_ATTRIBUTE"),
        ("dynamic_getattr", validator_source + "\ndef injected(): getattr(subprocess, 'run')(['git'])\n", "validator", "E_GETATTR_INVENTORY"),
        ("builder_git_argv", builder_source + "\ndef injected(): git_bytes(['status'])\n", "builder", "E_GIT_CALL_INVENTORY"),
        ("validator_git_argv", validator_source + "\ndef injected(): gtext(('fetch', 'origin'))\n", "validator", "E_GTEXT_CALL_INVENTORY"),
        ("extra_atomic_writer", builder_source + "\ndef injected(): atomic_write(ROOT / 'x', b'x')\n", "builder", "E_ATOMIC_CALL_INVENTORY"),
        ("validator_unlink", validator_source + "\ndef injected(): Path('x').unlink()\n", "validator", "E_MUTATION_INVENTORY"),
        ("builtin_open", builder_source + "\ndef injected(): open('x', 'w')\n", "builder", "E_SENSITIVE_NAME"),
        ("subprocess_call", validator_source + "\ndef injected(): subprocess.call(['git'])\n", "validator", "E_PROCESS_API"),
        ("network_import", builder_source + "\nimport requests\n", "builder", "E_IMPORT_INVENTORY"),
        ("protected_rebind", validator_source + "\ndef injected():\n    subprocess=object()\n", "validator", "E_PROTECTED_REBIND"),
        ("writer_name_rebind", validator_source + "\nprint = Path('x').write_text\nprint('x')\n", "validator", "E_PROTECTED_REBIND"),
        ("writer_keyword_transport", builder_source + "\ndef injected(): sorted(['x'], key=Path('x').write_text)\n", "builder", "E_SENSITIVE_ATTRIBUTE_TRANSPORT"),
        ("unc_network_read", validator_source + "\ndef injected(): Path(r'\\\\attacker.invalid\\share\\payload').read_text()\n", "validator", "E_PATH_CALL_INVENTORY"),
        ("function_name_rebind", builder_source + "\nrequire = Path('x').write_text\n", "builder", "E_PROTECTED_REBIND"),
        ("network_reader_transport", validator_source + "\ndef injected():\n    reader=Path(r'\\\\attacker.invalid\\share\\payload').read_text\n    print(reader())\n", "validator", "E_SENSITIVE_ATTRIBUTE_TRANSPORT"),
        ("nested_name_main_transport", builder_source + "\npairs = main\npairs()\n", "builder", "E_PROTECTED_REBIND"),
        ("declared_higher_order_transport", validator_source + "\ndef injected(): sorted([], key=main)\n", "validator", "E_DECLARED_CALLABLE_TRANSPORT"),
        ("argparse_filetype_transport",
         builder_source[:builder_parser_index]
         + "\n    sorted(['x'], key=argparse.FileType('w'))"
         + builder_source[builder_parser_index:],
         "builder", "E_MODULE_ATTRIBUTE_INVENTORY"),
        ("argparse_fromfile_constructor",
         validator_source[:validator_parser_index]
         + "\n    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')"
         + validator_source[validator_parser_index + len(parser_marker):],
         "validator", "E_ARGPARSE_CALL_INVENTORY"),
    ]
    passed = 0
    for label, mutated, role, expected_code in probes:
        errors = source_policy_errors(mutated, role)
        require(any(item.startswith(expected_code) for item in errors),
                "E_SOURCE_POLICY_NEGATIVE_FALSE_PASS", label + ":" + repr(errors[:5]))
        passed += 1
    return passed, len(probes)


def source_policy() -> None:
    builder = ROOT / BUILDER_PATH
    validator = ROOT / VALIDATOR_PATH
    require(neutral_source_hash(builder, "BUILDER_SOURCE_POLICY_SHA256_LF") == BUILDER_SOURCE_POLICY_SHA256_LF,
            "E_BUILDER_POLICY_HASH")
    require(neutral_source_hash(validator, "VALIDATOR_SOURCE_POLICY_SHA256_LF") == VALIDATOR_SOURCE_POLICY_SHA256_LF,
            "E_VALIDATOR_POLICY_HASH")
    builder_source = lf_bytes(builder.read_bytes()).decode("utf-8")
    validator_source = lf_bytes(validator.read_bytes()).decode("utf-8")
    builder_errors = source_policy_errors(builder_source, "builder")
    validator_errors = source_policy_errors(validator_source, "validator")
    require(not builder_errors, "E_BUILDER_SOURCE_POLICY", repr(builder_errors[:8]))
    require(not validator_errors, "E_VALIDATOR_SOURCE_POLICY", repr(validator_errors[:8]))
    passed, total = source_policy_controls(builder_source, validator_source)
    require(passed == total, "E_SOURCE_POLICY_CONTROLS")
    print(f"PASS_P067_STEP88_SOURCE_POLICY {passed}/{total}")


def control_document_errors(documents: dict[str,str]) -> list[str]:
    errors=[]
    result=document_lines=documents[RESULT_PATH].splitlines()
    if not (document_lines[0]=="# Phase 067 Step 88 Numerical Guard Impact Result"
            and "- Gate: `"+GATE+"`." in document_lines
            and "- Persistence state: `PASS_PENDING_PERSISTENCE`." in document_lines
            and "- Expected parent: `"+EXPECTED_PARENT+"`." in document_lines
            and "- Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`." in document_lines
            and "- external scientific/material/experimental/canonical/publication authority: false." in document_lines):
        errors.append("doc_result_status")
    def unique_line(path: str, prefix: str) -> str:
        matches=[line for line in documents[path].splitlines() if line.startswith(prefix)]
        if len(matches)!=1:
            errors.append("doc_bounded_line_"+path+":"+prefix)
            return ""
        return matches[0]
    for path in (PARENT_LEDGER,CANONICAL_LEDGER):
        row=unique_line(path,"| 067 | 82–90 |")
        needed=("Steps 82–87 persisted","Step 88",EXPECTED_PARENT,GATE,"PASS_PENDING_PERSISTENCE","Step 89")
        if any(token not in row for token in needed) or "Step 87 unit/numerical audit pending persistence" in row:
            errors.append("doc_phase067_row_"+path)
    current=unique_line(HANDOVER,"19. 현재 Phase 상태:")
    result_pointer=unique_line(HANDOVER,"20. 현재 result:")
    machine_pointer=unique_line(HANDOVER,"21. 현재 machine evidence:")
    if any(token not in current for token in ("Steps 82–87 persisted",EXPECTED_PARENT,"PASS_P067_STEP87_PERSISTENCE","Step 88",GATE,"PASS_PENDING_PERSISTENCE","Step 89 blocked")):
        errors.append("doc_handover_current")
    if "PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md" not in result_pointer or "현재 result: `Codex/results/PHASE_067_STEP_087" in result_pointer:
        errors.append("doc_handover_result_pointer")
    if "PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json" not in machine_pointer or "terminal `PASS_P067_STEP88_PERSISTENCE` pending" not in machine_pointer:
        errors.append("doc_handover_machine_pointer")
    return errors


def control_documents() -> tuple[int,int]:
    documents={}
    for path,expected in CONTROL_SHA256.items():
        raw=(ROOT/path).read_bytes();require(sha(raw)==expected,"E_CONTROL_HASH",path);documents[path]=raw.decode("utf-8")
    require(not control_document_errors(documents),"E_CONTROL_DOCUMENT")
    candidate=dict(documents)
    phase_row=next(line for line in candidate[PARENT_LEDGER].splitlines() if line.startswith("| 067 | 82–90 |"))
    candidate[PARENT_LEDGER]=candidate[PARENT_LEDGER].replace(phase_row,phase_row.replace(EXPECTED_PARENT,"PENDING_AT_PRECOMMIT_BY_DESIGN"),1)
    require(control_document_errors(candidate),"E_DOC_NEGATIVE_FALSE_PASS:phase_row")
    candidate=dict(documents)
    candidate[HANDOVER]=candidate[HANDOVER].replace("PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md","PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md",1)
    require(control_document_errors(candidate),"E_DOC_NEGATIVE_FALSE_PASS:result_pointer")
    return 2,2


def parse_porcelain(text: str) -> dict[str,str]:
    result={}
    for line in text.rstrip("\r\n").splitlines():
        if line: require(len(line)>=4,"E_STATUS_PARSE");result[line[3:].replace("\\","/")]=line[:2]
    return result


def parse_name_status(raw: bytes) -> dict[str,str]:
    parts=raw.decode("utf-8").split("\0");result={}
    for i in range(0,len(parts)-1,2): result[parts[i+1].replace("\\","/")]=parts[i]
    return result


def canonical_origin(value: str) -> str:
    return value.lower().replace("https://","").replace("http://","").removesuffix(".git")


def live(ref: str) -> str:
    parts=gtext(("ls-remote","--heads","origin",ref)).split();require(len(parts)==2 and parts[1]==ref,"E_LIVE_REF");return parts[0]


def repository_refs(tip: str) -> dict[str,Any]:
    main_paths=gtext(("diff","--name-only",f"{MAIN_BASE_TIP}..{MAIN_TIP}","--")).splitlines()
    observed={"head":gtext(("rev-parse","HEAD")),"branch":gtext(("rev-parse","--abbrev-ref","HEAD")),"upstream_name":gtext(("rev-parse","--abbrev-ref","@{upstream}")),"upstream_oid":gtext(("rev-parse","@{upstream}")),"active_tracking":gtext(("rev-parse",f"refs/remotes/origin/{BRANCH}")),"active_live":live(f"refs/heads/{BRANCH}"),"origin":canonical_origin(gtext(("remote","get-url","origin"))),"protected_local":gtext(("show-ref","--verify","--hash","refs/heads/codex/lib-physics-endgame-v1025_2")),"protected_tracking":gtext(("rev-parse","refs/remotes/origin/codex/lib-physics-endgame-v1025_2")),"protected_live":live("refs/heads/codex/lib-physics-endgame-v1025_2"),"main_local":gtext(("show-ref","--verify","--hash","refs/heads/main"),True),"main_tracking":gtext(("rev-parse","refs/remotes/origin/main")),"main_live":live("refs/heads/main"),"main_base":MAIN_BASE_TIP,"main_merge_base":gtext(("merge-base",EXPECTED_PARENT,MAIN_TIP)),"main_advance_commits":int(gtext(("rev-list","--count",f"{MAIN_BASE_TIP}..{MAIN_TIP}"))),"main_advance_path_count":len(main_paths),"main_advance_nonclaude_paths":sum(not path.startswith("Claude/") for path in main_paths)}
    expected={"head":tip,"branch":BRANCH,"upstream_name":f"origin/{BRANCH}","upstream_oid":tip,"active_tracking":tip,"active_live":tip,"origin":"github.com/lksz1412/project_anode_fit","protected_local":PROTECTED_TIP,"protected_tracking":PROTECTED_TIP,"protected_live":PROTECTED_TIP,"main_local":"","main_tracking":MAIN_TIP,"main_live":MAIN_TIP,"main_base":MAIN_BASE_TIP,"main_merge_base":MAIN_BASE_TIP,"main_advance_commits":MAIN_ADVANCE_COMMIT_COUNT,"main_advance_path_count":MAIN_ADVANCE_PATH_COUNT,"main_advance_nonclaude_paths":0}
    require(observed==expected,"E_REPOSITORY_REFS");return observed


def status() -> dict[str,str]:
    return parse_porcelain(git(("status","--porcelain=v1","--untracked-files=all")).decode("utf-8"))


def index_snapshot() -> dict[str,tuple[str,str]]:
    parts=git(("ls-files","-s","-z")).decode("utf-8").split("\0");result={}
    for item in parts:
        if item:
            meta,path=item.split("\t",1);mode,oid,stage=meta.split();path=path.replace("\\","/")
            if path in FINAL_SET: require(stage=="0","E_INDEX_STAGE");result[path]=(mode,oid)
    return result


def seal(tip: str) -> dict[str,Any]:
    return {"refs":repository_refs(tip),"status":status(),"index":index_snapshot(),"inputs":{path:sha((ROOT/path).read_bytes()) for path in INPUT_PINS}}


def verify_artifacts() -> tuple[int,int,int,int]:
    source_policy();inputs,input_nodes,input_depth=load_inputs();raw=(ROOT/MATRIX_PATH).read_bytes();matrix,nodes,depth=strict_load(raw,"E_MATRIX",True)
    errors=artifact_errors(matrix,inputs);require(not errors,"E_ARTIFACT",repr(errors[:5]))
    negative_passed,negative_total=negative_controls(matrix,inputs);json_passed,json_total=json_controls();doc_passed,doc_total=control_documents()
    print(f"PASS_P067_STEP88_CONTROLS semantic={negative_passed}/{negative_total} json={json_passed}/{json_total} docs={doc_passed}/{doc_total} nodes={nodes+input_nodes} depth={max(depth,input_depth)}")
    return negative_passed,negative_total,nodes+input_nodes,max(depth,input_depth)


def verify_content() -> None:
    entry=seal(EXPECTED_PARENT);verify_artifacts();expected={path:("??" if index<4 else " M") for index,path in enumerate(FINAL_PATHS)}
    require(status()==expected,"E_CONTENT_STATUS",repr(status()))
    require(parse_name_status(git(("diff","--cached","--name-status","-z")))=={},"E_CONTENT_STAGED")
    require(gtext(("diff","--name-only",EXPECTED_PARENT,"--","Claude"))=="","E_CLAUDE_DRIFT");require(seal(EXPECTED_PARENT)==entry,"E_TRANSACTION_SEAL")
    print("PASS_P067_STEP88_CONTENT occurrences=20 blobs=15 guards=24 probes=27 defaults=8 determinism=2/2 authority=internal-only")


def verify_staged() -> None:
    staged_head=gtext(("rev-parse","HEAD"));require(staged_head in {EXPECTED_PARENT,REJECTED_CANDIDATE},"E_STAGED_HEAD")
    entry=seal(staged_head)
    if staged_head==REJECTED_CANDIDATE:
        require(gtext(("show","--no-patch","--format=%P",staged_head)).split()==[EXPECTED_PARENT],"E_STAGED_HEAD_PARENT")
        require(gtext(("show","--no-patch","--format=%s",staged_head))==SUBJECT,"E_STAGED_HEAD_SUBJECT")
    verify_artifacts();require(parse_name_status(git(("diff","--cached","--name-status","-z",EXPECTED_PARENT,"--")))==FINAL_STATUS,"E_STAGED_STATUS")
    snapshot=index_snapshot();require(set(snapshot)==FINAL_SET and all(mode=="100644" for mode,_ in snapshot.values()),"E_STAGED_INDEX")
    staged_status=status();require(set(staged_status)<=FINAL_SET and all(value in ALLOWED_STAGED_PORCELAIN for value in staged_status.values()),"E_STAGED_WORKTREE",repr(staged_status));require(gtext(("diff","--name-only","--"))=="","E_STAGED_WORKTREE");require(gtext(("diff","--name-only",EXPECTED_PARENT,"--","Claude"))=="","E_CLAUDE_DRIFT");require(seal(staged_head)==entry,"E_TRANSACTION_SEAL")
    print("PASS_P067_STEP88_STAGED occurrences=20 blobs=15 guards=24 probes=27 defaults=8 determinism=2/2 authority=internal-only")


def verify_persistence(commit: str) -> None:
    require(is_oid(commit),"E_EXPECTED_COMMIT");entry=seal(commit);verify_artifacts();require(gtext(("show","--no-patch","--format=%P",commit)).split()==[EXPECTED_PARENT],"E_COMMIT_PARENT");require(gtext(("show","--no-patch","--format=%s",commit))==SUBJECT,"E_COMMIT_SUBJECT")
    require(parse_name_status(git(("diff-tree","--no-commit-id","--name-status","-r","-z",commit+"^",commit,"--")))==FINAL_STATUS,"E_COMMIT_DIFF")
    require(status()=={},"E_PERSISTENCE_DIRTY");require(gtext(("diff","--name-only",EXPECTED_PARENT,"--","Claude"))=="","E_CLAUDE_DRIFT");require(seal(commit)==entry,"E_TRANSACTION_SEAL")
    print(PERSISTENCE,"occurrences=20 blobs=15 guards=24 probes=27 defaults=8 determinism=2/2 authority=internal-only")


def git_argv_controls() -> tuple[int,int]:
    tree=("diff-tree","--no-commit-id","--name-status","-r","-z",EXPECTED_PARENT+"^",EXPECTED_PARENT,"--")
    good=[tree,("show","--no-patch","--format=%P",EXPECTED_PARENT),("show","--no-patch","--format=%s",EXPECTED_PARENT)]
    bad=[tree[:-1]+("",),tree+("extra",),tree[:5]+(EXPECTED_PARENT,EXPECTED_PARENT,"--"),tree[:6]+("f"*40,"--"),tree[:7]+("Claude",),tree[:5]+("--write",EXPECTED_PARENT,"--"),("merge-base",MAIN_TIP,EXPECTED_PARENT),("rev-list","--count",f"{MAIN_BASE_TIP}...{MAIN_TIP}"),("diff","--name-only",f"{MAIN_BASE_TIP}..{MAIN_TIP}"),("show","--format=%P",EXPECTED_PARENT),("show","--format=%s",EXPECTED_PARENT)]
    require(all(git_argv_allowed(item) for item in good) and not any(git_argv_allowed(item) for item in bad),"E_GIT_ARGV_CONTROL");return 14,14


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--verify-content", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    git_passed,git_total=git_argv_controls()
    if args.verify_content:
        require(args.expected_commit is None,"E_MODE_PAYLOAD");verify_content()
    elif args.verify_staged:
        require(args.expected_commit is None,"E_MODE_PAYLOAD");verify_staged()
    else:
        require(args.expected_commit is not None and is_oid(args.expected_commit),"E_MODE_PAYLOAD")
        verify_persistence(args.expected_commit)
    print(f"PASS_P067_STEP88_GIT_ARGV {git_passed}/{git_total}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
