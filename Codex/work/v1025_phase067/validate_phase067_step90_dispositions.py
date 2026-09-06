#!/usr/bin/env python3
"""Validate Phase 067 Step 90.1 disposition and carry-forward closure."""

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
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "38f93bd1638c674ff7fd7fb40ed57036a07fd8fd"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
SUBJECT = "audit(phase067): disposition code test fitting evidence"
GATE = "PASS_P067_STEP90_1_DISPOSITION"
PERSISTENCE = "PASS_P067_STEP90_1_PERSISTENCE"

BUILDER = "Codex/work/v1025_phase067/build_phase067_step90_dispositions.py"
VALIDATOR = "Codex/work/v1025_phase067/validate_phase067_step90_dispositions.py"
SOURCE_PATH = "Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json"
CARRY_PATH = "Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json"
RESULT = "Codex/results/PHASE_067_STEP_090_1_DISPOSITION_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = (
    BUILDER,
    VALIDATOR,
    SOURCE_PATH,
    CARRY_PATH,
    RESULT,
    PARENT_LEDGER,
    CANONICAL_LEDGER,
    HANDOVER,
)
FINAL_STATUS = {path: ("A" if index < 5 else "M")
                for index, path in enumerate(FINAL_PATHS)}

INPUT_PATHS = (
    "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json",
    "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json",
    "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json",
    "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json",
    "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json",
    "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json",
    "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json",
    "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json",
    "Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json",
    "Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json",
    "Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json",
)
INPUT_EXPECTED = {
    INPUT_PATHS[0]: ("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63", "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1", "pretty", "step82_blank_pretty"),
    INPUT_PATHS[1]: ("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174", "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9", "pretty", "step82_blank_pretty"),
    INPUT_PATHS[2]: ("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8", "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44", "compact", "compact_lf"),
    INPUT_PATHS[3]: ("54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f", "63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc", "compact", "compact_lf"),
    INPUT_PATHS[4]: ("b8ac7affbb31195ec8dde6015890cbb50b1f2b9cc5815fc33c325efc95286f23", "845b676aea321134b648de41320e7baf4f39f925ad2a1abe96f36f713bc95542", "compact", "compact_lf"),
    INPUT_PATHS[5]: ("9bf610d2d09be7d95fd2493541d6c4336de330c37fb56d1f12c411b228dfbf82", "0e2b0bd3f6120c9c8feaa879b5fe62a49934de5ea8dbddff14c700ddef32f196", "compact", "compact_lf"),
    INPUT_PATHS[6]: ("13a281c76282f5fae370d1c2b10f183937c685bceba466489a62b9e850049d4a", "eadde68e51257e0daae9f9455be3a7331c77a56d1490b2291934ef75f45fa154", "compact", "compact_lf"),
    INPUT_PATHS[7]: ("474f09ebb1605d3190867cee9746079b10c04f6bfbdfbab028e9d6c1be70ec08", "c556671b6fd4284d740fdb0cc3777087442d4abd2160ace42d4ff70749d4144c", "compact", "compact_lf"),
    INPUT_PATHS[8]: ("62f5eb265121987b83398266895a11e8a84d7f1ffa90c59fe929efb6f00614be", "099899de75edfde55a92ff31f577e178967212226cf4a13cdb951643b15e535c", "compact", "compact_lf"),
    INPUT_PATHS[9]: ("525b33403667413446e374a2b931c90ec45c7eb24871205527dd9c6ddef2591d", "201b2e65756ab8876c861216742f67b0305ef351cc84e8f4ebf434d49dfabb2b", "compact", "compact_lf"),
    INPUT_PATHS[10]: ("dc76eeef9b0bb2f93a376fbe491f12b2c73b47d59b097e671e9745b28a6869f4", "cf1b136028f126670a80ec60ce26db9edc110e0bff7c41cf7986f73c14f9ae3a", "compact", "compact_lf"),
    INPUT_PATHS[11]: ("c0859de686ea207be758fc6d32faaa88d2e95151e3c3bdb56615ff366f250486", "b78cfa4ec96e3aeb42979e6aaf93407fed9267fd7abeeb8458064d78b3567846", "compact", "compact_lf"),
    INPUT_PATHS[12]: ("847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003", "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6", "pretty", "legacy_compact"),
}
ALLOWED_DISPOSITIONS = {
    "PRESERVE", "CORRECT", "WITHHOLD", "DISCARD", "GROUND_NOT_FOUND",
}
SOURCE_CONTRACT_EXPECTED = {
    "python_occurrences": 129,
    "python_unique_blobs": 84,
    "python_unique_blob_physical_lines": 29_952,
    "python_releases": 20,
    "code_occurrences": 20,
    "code_unique_blobs": 15,
    "test_occurrences": 44,
    "test_unique_blobs": 29,
    "demo_occurrences": 30,
    "demo_unique_blobs": 26,
    "result_tool_occurrences": 35,
    "result_tool_unique_blobs": 14,
    "golden_occurrences": 8,
    "golden_unique_blobs": 2,
    "guide_occurrences": 20,
    "guide_unique_blobs": 8,
    "guide_unique_blob_physical_lines": 854,
    "result_tool_cross_binding": True,
}
OWNER_TARGETS = {
    "P065-OBL-0054": ("P065-S72-F04", "PHASE-080-BLEND-CLOSURE", 80),
    "P066-OBL-0120": ("P066-P79-07", "PHASE-080-BLEND-CLOSURE", 80),
    "P066-OBL-0125": ("P066-R80-14", "PHASE-083-IMPLEMENTATION-CONTRACT", 83),
}
NEW_OBLIGATIONS = {
    "P067-OBL-0001": ("P067-S88-O02", "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
                      "open_gap_records", 1, []),
    "P067-OBL-0002": ("P067-S88-O03", "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
                      "open_gap_records", 2,
                      ["P065-OBL-0043", "P065-OBL-0060", "P066-OBL-0088"]),
    "P067-OBL-0003": ("P067-S88-G21", "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
                      "guard_records", 20, []),
}
OWNER_LINKS = {
    "P065-OBL-0054": ["P066-OBL-0120"],
    "P066-OBL-0120": ["P065-OBL-0054"],
    "P066-OBL-0125": [],
}
FINDING_FAMILIES = (
    (82, INPUT_PATHS[1], "blob_attestations"),
    (82, INPUT_PATHS[0], "genealogy_commit_records"),
    (83, INPUT_PATHS[2], "flow_records"),
    (83, INPUT_PATHS[2], "source_records"),
    (84, INPUT_PATHS[3], "behavior_records"),
    (84, INPUT_PATHS[3], "blob_graph_records"),
    (84, INPUT_PATHS[3], "coverage_records"),
    (84, INPUT_PATHS[3], "source_records"),
    (85, INPUT_PATHS[4], "case_contract"),
    (85, INPUT_PATHS[4], "inputs"),
    (85, INPUT_PATHS[4], "saved_profiles"),
    (85, INPUT_PATHS[4], "owner_resolution"),
    (85, INPUT_PATHS[5], "runs"),
    (85, INPUT_PATHS[5], "process_pair_records"),
    (86, INPUT_PATHS[6], "python_blob_static_records"),
    (86, INPUT_PATHS[6], "runtime_records"),
    (86, INPUT_PATHS[6], "golden_blob_records"),
    (86, INPUT_PATHS[6], "golden_route_records"),
    (86, INPUT_PATHS[7], "guide_blob_records"),
    (86, INPUT_PATHS[7], "tool_blob_records"),
    (87, INPUT_PATHS[8], "limitation_records"),
    (87, INPUT_PATHS[8], "probe_records"),
    (87, INPUT_PATHS[8], "source_feature_records"),
    (87, INPUT_PATHS[8], "source_occurrence_records"),
    (87, INPUT_PATHS[8], "tolerance_provenance_records"),
    (88, INPUT_PATHS[9], "candidate_disposition_records"),
    (88, INPUT_PATHS[9], "guard_records"),
    (88, INPUT_PATHS[9], "impact_probe_records"),
    (88, INPUT_PATHS[9], "numerical_default_records"),
    (88, INPUT_PATHS[9], "open_gap_records"),
    (88, INPUT_PATHS[9], "optimizer_route_records"),
    (88, INPUT_PATHS[9], "source_feature_records"),
    (88, INPUT_PATHS[9], "source_occurrence_records"),
    (88, INPUT_PATHS[9], "supplemental_optimizer_source_record"),
    (89, INPUT_PATHS[10], "evidence_records"),
    (89, INPUT_PATHS[10], "absent_class_records"),
    (89, INPUT_PATHS[10], "bounded_obligations"),
    (89, INPUT_PATHS[10], "comparison_source_contracts"),
    (89, INPUT_PATHS[10], "saved_profile_records"),
    (89, INPUT_PATHS[10], "phase066_inputs"),
    (89, INPUT_PATHS[10], "supplemental_inputs"),
    (89, INPUT_PATHS[10], "supplemental_route_contracts"),
    (89, INPUT_PATHS[10], "missing_evidence"),
    (89, INPUT_PATHS[11], "original_optimizer_state_availability"),
    (89, INPUT_PATHS[11], "saved_consistency_checks"),
    (89, INPUT_PATHS[11], "sealed_replay_records"),
    (89, INPUT_PATHS[11], "static_source_checks"),
)
AUTHORITY_BOUNDARY = {
    "external_scientific_authority": False,
    "held_out_validation": False,
    "identifiability": False,
    "material_assignment": False,
    "phase_or_mechanism_identification": False,
    "publication": False,
    "protocol_binding": False,
    "original_optimizer_state": False,
    "stale_pdf_release": False,
    "ref7_original_full_text": "GROUND_NOT_FOUND",
}
SOURCE_AUTHORITY = {
    "canonical_model": False,
    "external_scientific": False,
    "held_out_validation": False,
    "identifiability": False,
    "material_mechanism": False,
    "primary_proposition": False,
    "publication": False,
    "specimen_protocol": False,
}
GATE_SUMMARY_EXPECTED = {
    "source_dispositions": 157,
    "blob_disposition_groups": 94,
    "prior_active_obligations": 219,
    "active_obligations": 222,
    "prior_owner_registry_records": 355,
    "owner_registry_records": 358,
    "p067_owner_transitions": 3,
    "new_obligations": 3,
    "ownerless_active_obligations": 0,
    "multiply_owned_active_obligations": 0,
    "lost_inherited_ids": 0,
    "external_authority_promotions": 0,
    "gate": GATE,
}
MAX_JSON_BYTES = 8_000_000
MAX_JSON_DEPTH = 64
MAX_JSON_NODES = 600_000
BUILDER_SOURCE_SHA256_LF = "5b18eff2e10b1aad6a780871745ef1a96f8829b6898d36e4170b0c40c000df6a"
VALIDATOR_NEUTRAL_SHA256_LF = "920bae919c0a3ea6aa18ef4926acbfc9f71d606d2d818e86778ad6c1d00db0a0"


class ValidationError(RuntimeError):
    pass


def require(ok: bool, code: str, detail: str = "") -> None:
    if not ok:
        raise ValidationError(code + ((":" + detail) if detail else ""))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any], style: str) -> str:
    body = dict(value)
    if style == "step82_blank_pretty":
        body["semantic_sha256"] = ""
        return sha(pretty(body))
    body.pop("semantic_sha256", None)
    if style == "compact_lf":
        return sha(canonical(body))
    require(style == "legacy_compact", "E_SEMANTIC_STYLE")
    raw = json.dumps(body, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha(raw)


def record_sha(value: Any) -> str:
    return sha(canonical(value))


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            typed_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def strict_load(raw: bytes, label: str, raw_style: str,
                semantic_style: str) -> tuple[dict[str, Any], int, int]:
    require(len(raw) <= MAX_JSON_BYTES, label + "_BYTES")
    nesting = 0
    in_string = False
    escaped = False
    maximum_lexical_depth = 0
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
            maximum_lexical_depth = max(maximum_lexical_depth, nesting)
            require(nesting <= MAX_JSON_DEPTH, label + "_DEPTH")
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
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError,
            RecursionError, MemoryError) as exc:
        raise ValidationError(label + "_PARSE") from exc
    require(isinstance(value, dict), label + "_ROOT")
    nodes = 0
    depth = 0
    stack: list[tuple[Any, int]] = [(value, 0)]
    while stack:
        item, level = stack.pop()
        nodes += 1
        require(nodes <= MAX_JSON_NODES, label + "_NODES")
        require(level <= MAX_JSON_DEPTH, label + "_DEPTH")
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
            require(math.isfinite(item), label + "_NONFINITE")
        else:
            require(item is None or isinstance(item, (str, int, bool)), label + "_TREE")
    if raw_style == "compact":
        require(raw == canonical(value), label + "_NONCANONICAL")
    elif raw_style == "pretty":
        require(raw == pretty(value), label + "_NONCANONICAL")
    else:
        require(raw_style == "unchecked", label + "_STYLE")
    if semantic_style != "unchecked":
        require(value.get("semantic_sha256") == semantic(value, semantic_style),
                label + "_SEMANTIC")
    return value, nodes, max(depth, maximum_lexical_depth)


def is_oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    if not args or any(not isinstance(item, str) or "\0" in item or "\n" in item or "\r" in item
                       for item in args):
        return False
    fixed = {
        ("rev-parse", "HEAD"),
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--cached", "--name-only"),
        ("diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--"),
        ("diff", "--name-only"),
        ("rev-parse", "@{u}"),
        ("rev-parse", f"refs/remotes/origin/{BRANCH}"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("ls-files", "--stage", "--", *FINAL_PATHS),
        ("ls-tree", EXPECTED_PARENT, "--", *INPUT_PATHS),
    }
    if args in fixed:
        return True
    if len(args) == 2 and args[0] == "show" and ":" in args[1]:
        ref, path = args[1].split(":", 1)
        return ref == EXPECTED_PARENT and path in INPUT_PATHS
    if args[:3] == ("diff", "--name-only", PROTECTED_TIP) and len(args) == 6:
        return (args[3] == EXPECTED_PARENT or is_oid(args[3])) and args[4:] == ("--", "Claude")
    if len(args) == 4 and args[:2] == ("show", "--no-patch"):
        return args[2] in {"--format=%P", "--format=%s"} and is_oid(args[3])
    if len(args) == 7 and args[:5] == (
        "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames"
    ):
        return is_oid(args[5]) and args[6] == "--"
    if len(args) == 3 + len(FINAL_PATHS) and args[0] == "ls-tree" and args[2] == "--":
        return is_oid(args[1]) and args[3:] == FINAL_PATHS
    return False


def git_bytes(args: list[str], code: str) -> bytes:
    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV", repr(args))
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(completed.returncode == 0, code,
            completed.stderr.decode("utf-8", "replace")[:300])
    return completed.stdout


def git_text(args: list[str], code: str) -> str:
    return git_bytes(args, code).decode("utf-8").strip()


def input_tree() -> dict[str, tuple[str, str]]:
    raw = git_text(["ls-tree", EXPECTED_PARENT, "--", *INPUT_PATHS], "E_INPUT_TREE")
    rows: dict[str, tuple[str, str]] = {}
    for line in raw.splitlines():
        match = re.fullmatch(r"([0-9]{6}) blob ([0-9a-f]{40})\t(.+)", line)
        require(match is not None, "E_INPUT_TREE_PARSE")
        path = match.group(3).replace("\\", "/")
        require(path in INPUT_PATHS and path not in rows, "E_INPUT_TREE_PATH", path)
        rows[path] = (match.group(1), match.group(2))
    require(tuple(path for path in INPUT_PATHS if path in rows) == INPUT_PATHS,
            "E_INPUT_TREE_COVERAGE")
    return rows


def load_inputs() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    trees = input_tree()
    values: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    for path in INPUT_PATHS:
        raw = git_bytes(["show", f"{EXPECTED_PARENT}:{path}"], "E_INPUT_READ")
        raw_expected, semantic_expected, raw_style, semantic_style = INPUT_EXPECTED[path]
        require(sha(raw) == raw_expected, "E_INPUT_RAW_SHA", path)
        value, _, _ = strict_load(raw, "E_INPUT_JSON", raw_style, semantic_style)
        require(value.get("semantic_sha256") == semantic_expected,
                "E_INPUT_SEMANTIC_PIN", path)
        values[path] = value
        mode, oid = trees[path]
        require(mode == "100644", "E_INPUT_MODE", path)
        records.append({
            "bytes": len(raw),
            "declared_semantic_sha256": semantic_expected,
            "git_blob_oid": oid,
            "mode": mode,
            "path": path,
            "raw_sha256": raw_expected,
            "recomputed_semantic_sha256": semantic(value, semantic_style),
            "semantic_seal_status": "VERIFIED",
            "source_commit": EXPECTED_PARENT,
        })
    return values, records


def builder_preview() -> dict[str, Any]:
    completed = subprocess.run([sys.executable, "-B", str(ROOT / BUILDER), "--preview"],
                               cwd=ROOT, check=False, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    require(completed.returncode == 0, "E_BUILDER_PREVIEW",
            completed.stderr.decode("utf-8", "replace")[:500])
    value, _, _ = strict_load(completed.stdout, "E_PREVIEW", "unchecked", "unchecked")
    require(set(value) == {"carry_forward", "source_disposition"}, "E_PREVIEW_SCHEMA")
    return value


def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:
    require((ROOT / SOURCE_PATH).is_file(), "E_SOURCE_MISSING")
    require((ROOT / CARRY_PATH).is_file(), "E_CARRY_MISSING")
    source, sn, sd = strict_load((ROOT / SOURCE_PATH).read_bytes(), "E_SOURCE",
                                 "compact", "compact_lf")
    carry, cn, cd = strict_load((ROOT / CARRY_PATH).read_bytes(), "E_CARRY",
                                "compact", "compact_lf")
    return source, carry, sn + cn, max(sd, cd)


def require_metadata(value: dict[str, Any], artifact: str, schema: str) -> None:
    require(value.get("artifact") == artifact, "E_ARTIFACT", artifact)
    require(value.get("schema_version") == schema, "E_SCHEMA", artifact)
    require(value.get("phase") == 67 and value.get("step") == "90.1",
            "E_PHASE_STEP", artifact)
    require(value.get("baseline_commit") == BASELINE, "E_BASELINE", artifact)
    require(value.get("branch") == BRANCH, "E_BRANCH_METADATA", artifact)
    require(value.get("expected_parent") == EXPECTED_PARENT, "E_PARENT", artifact)
    require(value.get("expected_subject") == SUBJECT, "E_SUBJECT", artifact)
    require(value.get("gate") == GATE, "E_GATE", artifact)
    require(value.get("persistence_terminal") == PERSISTENCE, "E_TERMINAL", artifact)
    require(value.get("containing_commit") == "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "E_CONTAINING_COMMIT", artifact)
    require(value.get("result_first") is True and value.get("json_outputs_last") is True,
            "E_COLLECTION_ORDER", artifact)
    require(value.get("generated_date") == "2026-09-06", "E_GENERATED_DATE", artifact)


def normalized_role(role: Any) -> Any:
    return "result" if role == "result_tool" else role


def pointer_tokens(pointer: str) -> list[str]:
    require(pointer.startswith("/"), "E_POINTER_FORM")
    tokens: list[str] = []
    for token in pointer[1:].split("/"):
        require(re.search(r"~(?:[^01]|$)", token) is None, "E_POINTER_ESCAPE")
        tokens.append(token.replace("~1", "/").replace("~0", "~"))
    return tokens


def resolve_pointer(value: Any, pointer: str) -> Any:
    current = value
    for token in pointer_tokens(pointer):
        if isinstance(current, dict):
            require(token in current, "E_POINTER_KEY")
            current = current[token]
        elif isinstance(current, list):
            require(re.fullmatch(r"0|[1-9][0-9]*", token) is not None,
                    "E_POINTER_INDEX")
            index = int(token)
            require(index < len(current), "E_POINTER_RANGE")
            current = current[index]
        else:
            raise ValidationError("E_POINTER_TRAVERSAL")
    return current


def pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def expected_finding_crosswalk(
        inputs: dict[str, dict[str, Any]]) -> tuple[set[tuple[Any, ...]], dict[str, int]]:
    expected: set[tuple[Any, ...]] = set()
    family_counts: dict[str, int] = {}
    singleton_dicts = {"owner_resolution", "supplemental_optimizer_source_record"}
    for step, path, collection in FINDING_FAMILIES:
        item = inputs[path][collection]
        if isinstance(item, list):
            projected = [(f"/{collection}/{index}", value)
                         for index, value in enumerate(item)]
        elif isinstance(item, dict) and collection in singleton_dicts:
            projected = [(f"/{collection}", item)]
        elif isinstance(item, dict):
            projected = [(f"/{collection}/{pointer_token(key)}", item[key])
                         for key in sorted(item)]
        else:
            raise ValidationError("E_FINDING_COLLECTION:" + collection)
        family = f"S{step}:{Path(path).stem}:{collection}"
        family_counts[family] = len(projected)
        for pointer, value in projected:
            expected.add((step, path, pointer, record_sha(value)))
    return expected, family_counts


def expected_blob_origins(
        inputs: dict[str, dict[str, Any]]) -> dict[tuple[str, str], tuple[str, str, str]]:
    expected: dict[tuple[str, str], tuple[str, str, str]] = {}
    collections = (
        ("PYTHON_OCCURRENCE", INPUT_PATHS[0], "blob_records"),
        ("GOLDEN_OCCURRENCE", INPUT_PATHS[6], "golden_blob_records"),
        ("GUIDE_OCCURRENCE", INPUT_PATHS[7], "guide_blob_records"),
    )
    for surface, path, collection in collections:
        for index, row in enumerate(inputs[path][collection]):
            key = (surface, row["blob_oid"])
            require(key not in expected, "E_EXPECTED_BLOB_ORIGIN_DUPLICATE")
            expected[key] = (path, f"/{collection}/{index}", record_sha(row))
    require(len(expected) == 94, "E_EXPECTED_BLOB_ORIGIN_COUNT")
    return expected


def expected_source_identities(inputs: dict[str, dict[str, Any]]) -> set[tuple[Any, ...]]:
    inventory = inputs[INPUT_PATHS[0]]
    behavior = inputs[INPUT_PATHS[6]]
    guide = inputs[INPUT_PATHS[7]]
    expected: set[tuple[Any, ...]] = set()
    for row in inventory["occurrence_records"]:
        expected.add(("PYTHON_OCCURRENCE", row["path"], row["release"], row["role"],
                      row["blob_oid"], row["git_mode"]))
    for row in behavior["occurrence_projection"]["golden"]:
        expected.add(("GOLDEN_OCCURRENCE", row["path"], row["release"], "golden",
                      row["blob_oid"], row["git_mode"]))
    for row in guide["guide_occurrence_projection"]:
        expected.add(("GUIDE_OCCURRENCE", row["path"], row["release"], "guide",
                      row["blob_oid"], row["git_mode"]))
    require(len(expected) == 157, "E_EXPECTED_SOURCE_IDENTITIES")
    return expected


def validate_source(source: dict[str, Any], inputs: dict[str, dict[str, Any]],
                    input_records: list[dict[str, Any]]) -> None:
    require(set(source) == {
        "artifact", "authority", "baseline_commit", "blob_disposition_groups",
        "branch", "containing_commit", "disposition_enum", "expected_parent",
        "expected_subject", "gate", "generated_date", "inputs", "json_outputs_last",
        "persistence_terminal", "phase", "result_first", "schema_version",
        "semantic_sha256", "source_contract", "source_dispositions", "step",
    }, "E_SOURCE_SCHEMA")
    require_metadata(source, "PHASE_067_SOURCE_DISPOSITION_MATRIX",
                     "P067-S90.1-SOURCE-DISPOSITION-V1")
    require(typed_equal(source.get("inputs"), input_records), "E_SOURCE_INPUTS")
    require(source.get("authority") == SOURCE_AUTHORITY, "E_SOURCE_AUTHORITY")
    require(source.get("disposition_enum") == [
        "PRESERVE", "CORRECT", "WITHHOLD", "DISCARD", "GROUND_NOT_FOUND",
    ], "E_SOURCE_DISPOSITION_ENUM")
    contract = source.get("source_contract")
    require(isinstance(contract, dict), "E_SOURCE_CONTRACT")
    for key, value in SOURCE_CONTRACT_EXPECTED.items():
        require(contract.get(key) == value, "E_SOURCE_CONTRACT", key)
    require(set(contract) == set(SOURCE_CONTRACT_EXPECTED) | {
        "blob_disposition_groups", "disposition_counts", "source_disposition_records",
    }, "E_SOURCE_CONTRACT_SCHEMA")
    require(contract.get("blob_disposition_groups") == 94 and
            contract.get("source_disposition_records") == 157,
            "E_SOURCE_CONTRACT_DENOMINATOR")
    rows = source.get("source_dispositions")
    groups = source.get("blob_disposition_groups")
    require(isinstance(rows, list) and len(rows) == 157, "E_SOURCE_ROWS")
    require(isinstance(groups, list) and len(groups) == 94, "E_BLOB_GROUPS")
    required = {
        "disposition_id", "surface_kind", "source_path", "release", "role",
        "blob_oid", "mode", "dedup_group", "disposition", "state",
        "canonical_owner", "acceptance_criterion", "authority_ceiling",
        "origin_path", "origin_pointer", "origin_record_sha256",
        "external_authority_promoted", "manifest_entry_index", "occurrence_ordinal",
    }
    identifiers: list[str] = []
    identities: set[tuple[Any, ...]] = set()
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == required, "E_SOURCE_ROW_SCHEMA")
        identifiers.append(row["disposition_id"])
        require(row["surface_kind"] in {
            "PYTHON_OCCURRENCE", "GOLDEN_OCCURRENCE", "GUIDE_OCCURRENCE",
        },
                "E_SURFACE_KIND")
        require(row["disposition"] in ALLOWED_DISPOSITIONS, "E_DISPOSITION_ENUM")
        require(row["mode"] == "100644" and is_oid(row["blob_oid"]),
                "E_SOURCE_OBJECT_IDENTITY")
        require(isinstance(row["canonical_owner"], str) and row["canonical_owner"],
                "E_SOURCE_OWNER")
        require(isinstance(row["acceptance_criterion"], str) and
                row["acceptance_criterion"], "E_SOURCE_ACCEPTANCE")
        require(isinstance(row["authority_ceiling"], str) and row["authority_ceiling"],
                "E_SOURCE_CEILING")
        require(isinstance(row["state"], str) and row["state"], "E_SOURCE_STATE")
        require(row["dedup_group"] ==
                f"{row['surface_kind'].lower()}:{row['blob_oid']}", "E_SOURCE_DEDUP")
        require(row["origin_path"] in INPUT_PATHS[:-1] and
                isinstance(row["origin_pointer"], str) and row["origin_pointer"].startswith("/"),
                "E_SOURCE_ORIGIN")
        require(re.fullmatch(r"[0-9a-f]{64}", row["origin_record_sha256"]) is not None,
                "E_SOURCE_ORIGIN_HASH")
        require(row["origin_record_sha256"] == record_sha(
            resolve_pointer(inputs[row["origin_path"]], row["origin_pointer"])),
            "E_SOURCE_ORIGIN_BINDING")
        require(row["external_authority_promoted"] is False,
                "E_SOURCE_AUTHORITY_PROMOTION")
        role = normalized_role(row["role"])
        identities.add((row["surface_kind"], row["source_path"], row["release"], role,
                        row["blob_oid"], row["mode"]))
        key = (row["surface_kind"], row["blob_oid"])
        grouped.setdefault(key, []).append(row)
    require(len(identifiers) == len(set(identifiers)) == 157,
            "E_SOURCE_ROW_DUPLICATE")
    require(identities == expected_source_identities(inputs), "E_SOURCE_PROJECTION")
    require(len(grouped) == 94, "E_SOURCE_GROUP_PROJECTION")
    native_origins = expected_blob_origins(inputs)
    observed_groups: set[tuple[str, str]] = set()
    for group in groups:
        required_group = {
            "blob_group_id", "surface_kind", "blob_oid", "occurrence_count",
            "occurrence_dispositions", "contextual_mixed_disposition",
            "row_record_sha256s", "blob_disposition", "origin_path",
            "origin_pointer", "origin_record_sha256",
        }
        require(isinstance(group, dict) and set(group) == required_group,
                 "E_BLOB_GROUP_SCHEMA")
        key = (group["surface_kind"], group["blob_oid"])
        require(key in grouped and key not in observed_groups, "E_BLOB_GROUP_KEY")
        observed_groups.add(key)
        members = grouped[key]
        dispositions = sorted({row["disposition"] for row in members})
        require(group["occurrence_count"] == len(members), "E_BLOB_GROUP_COUNT")
        require(group["occurrence_dispositions"] == dispositions,
                "E_BLOB_GROUP_DISPOSITIONS")
        require(group["contextual_mixed_disposition"] == (len(dispositions) > 1),
                "E_BLOB_GROUP_CONTEXT")
        require(group["contextual_mixed_disposition"] is False and len(dispositions) == 1 and
                group["blob_disposition"] == dispositions[0],
                "E_BLOB_GROUP_SCALAR_DISPOSITION")
        require(group["row_record_sha256s"] == [record_sha(row) for row in members],
                "E_BLOB_GROUP_ROW_HASHES")
        require((group["origin_path"], group["origin_pointer"],
                 group["origin_record_sha256"]) == native_origins[key],
                "E_BLOB_GROUP_ORIGIN")
        origin_row = resolve_pointer(inputs[group["origin_path"]], group["origin_pointer"])
        require(isinstance(origin_row, dict) and origin_row.get("blob_oid") == group["blob_oid"] and
                record_sha(origin_row) == group["origin_record_sha256"],
                "E_BLOB_GROUP_ORIGIN_BINDING")
    require(observed_groups == set(grouped), "E_BLOB_GROUP_COVERAGE")
    counts = {name: sum(row["disposition"] == name for row in rows)
              for name in ALLOWED_DISPOSITIONS}
    require(contract.get("disposition_counts") == counts and sum(counts.values()) == 157,
            "E_SOURCE_DISPOSITION_COUNTS")


def validate_disposition_records(records: Any,
                                 inputs: dict[str, dict[str, Any]]) -> None:
    require(isinstance(records, list) and records, "E_FINDING_RECORDS")
    required = {
        "disposition_id", "origin_step", "origin_path", "origin_pointer",
        "origin_record_sha256", "disposition", "state", "canonical_owner",
        "target_phase", "acceptance_criterion", "authority_ceiling",
        "relation_links", "external_authority_promoted",
    }
    identifiers: list[str] = []
    for row in records:
        require(isinstance(row, dict) and set(row) == required, "E_FINDING_SCHEMA")
        identifiers.append(row["disposition_id"])
        step = row["origin_step"]
        require(type(step) is int and step in set(range(82, 90)), "E_FINDING_STEP")
        require(row["origin_path"] in INPUT_PATHS[:-1], "E_FINDING_ORIGIN_PATH")
        require(isinstance(row["origin_pointer"], str) and row["origin_pointer"].startswith("/"),
                "E_FINDING_ORIGIN_POINTER")
        require(re.fullmatch(r"[0-9a-f]{64}", row["origin_record_sha256"]) is not None,
                "E_FINDING_ORIGIN_HASH")
        require(row["origin_record_sha256"] == record_sha(
            resolve_pointer(inputs[row["origin_path"]], row["origin_pointer"])),
            "E_FINDING_ORIGIN_BINDING")
        require(row["disposition"] in ALLOWED_DISPOSITIONS, "E_FINDING_DISPOSITION")
        require(isinstance(row["canonical_owner"], str) and row["canonical_owner"],
                "E_FINDING_OWNER")
        require(type(row["target_phase"]) is int and row["target_phase"] > 0,
                "E_FINDING_TARGET")
        require(isinstance(row["acceptance_criterion"], str) and
                row["acceptance_criterion"], "E_FINDING_ACCEPTANCE")
        require(isinstance(row["authority_ceiling"], str) and row["authority_ceiling"],
                "E_FINDING_CEILING")
        require(isinstance(row["state"], str) and row["state"], "E_FINDING_STATE")
        require(isinstance(row["relation_links"], list) and
                all(isinstance(link, str) and link for link in row["relation_links"]),
                "E_FINDING_RELATIONS")
        require(row["external_authority_promoted"] is False,
                "E_FINDING_AUTHORITY_PROMOTION")
    require(len(identifiers) == len(set(identifiers)), "E_FINDING_DUPLICATE")


def validate_carry(carry: dict[str, Any], source: dict[str, Any],
                   inputs: dict[str, dict[str, Any]],
                   input_records: list[dict[str, Any]]) -> None:
    require(set(carry) == {
        "active_obligations", "artifact", "authority_boundary", "baseline_commit",
        "branch", "containing_commit", "current_owner_duplicate_check_universe",
        "expected_parent", "expected_subject", "gate", "gate_summary", "generated_date",
        "inputs", "json_outputs_last", "new_obligations", "owner_transitions",
        "persistence_terminal", "phase", "prior_phase066_carry", "result_first",
        "schema_version", "semantic_sha256", "source_disposition_semantic_sha256",
        "step", "step82_89_disposition_records",
    }, "E_CARRY_SCHEMA")
    require_metadata(carry, "PHASE_067_CARRY_FORWARD_DELTA",
                     "P067-S90.1-CARRY-FORWARD-V1")
    require(typed_equal(carry.get("inputs"), input_records), "E_CARRY_INPUTS")
    require(carry.get("source_disposition_semantic_sha256") == source["semantic_sha256"],
            "E_SOURCE_CARRY_BINDING")
    prior = inputs[INPUT_PATHS[12]]
    require(typed_equal(carry.get("prior_phase066_carry"), prior),
            "E_PRIOR_CARRY_LOSS")
    records = carry.get("step82_89_disposition_records")
    validate_disposition_records(records, inputs)
    expected_crosswalk, expected_family = expected_finding_crosswalk(inputs)
    observed_crosswalk = {
        (row["origin_step"], row["origin_path"], row["origin_pointer"],
         row["origin_record_sha256"])
        for row in records
    }
    require(len(records) == len(observed_crosswalk) == len(expected_crosswalk) and
            observed_crosswalk == expected_crosswalk, "E_FINDING_CROSSWALK")

    transitions = carry.get("owner_transitions")
    require(isinstance(transitions, list) and len(transitions) == 3,
            "E_OWNER_TRANSITIONS")
    by_id = {row.get("obligation_id"): row for row in transitions if isinstance(row, dict)}
    require(set(by_id) == set(OWNER_TARGETS), "E_OWNER_TRANSITION_IDS")
    required_transition = {
        "obligation_id", "origin_identity", "prior_owner", "prior_state",
        "disposition", "state", "canonical_owner", "target_phase",
        "acceptance_criterion", "authority_ceiling", "external_authority_promoted",
        "relation_links",
    }
    for obligation_id, (origin, owner, phase) in OWNER_TARGETS.items():
        row = by_id[obligation_id]
        require(set(row) == required_transition, "E_OWNER_TRANSITION_SCHEMA")
        require(row["origin_identity"] == origin and row["prior_owner"] ==
                "P067-CODE-HISTORY" and row["prior_state"] == "OPEN_CARRY",
                "E_OWNER_TRANSITION_PRIOR", obligation_id)
        require(row["disposition"] == "WITHHOLD" and
                row["state"] == "OPEN_CARRY_EXPLICITLY_BOUNDED_P067",
                "E_OWNER_FALSE_RESOLUTION", obligation_id)
        require(row["canonical_owner"] == owner and row["target_phase"] == phase,
                "E_OWNER_TRANSITION_TARGET", obligation_id)
        require(row["relation_links"] == OWNER_LINKS[obligation_id],
                "E_OWNER_TRANSITION_RELATIONS", obligation_id)
        require(isinstance(row["acceptance_criterion"], str) and
                row["acceptance_criterion"] and row["authority_ceiling"],
                "E_OWNER_TRANSITION_BOUND", obligation_id)
        require(row["external_authority_promoted"] is False,
                "E_OWNER_TRANSITION_PROMOTION", obligation_id)

    prior_active = prior["active_obligations"]
    active = carry.get("active_obligations")
    require(isinstance(active, list) and len(active) == 222, "E_ACTIVE_COUNT")
    prior_by_id = {row["obligation_id"]: row for row in prior_active}
    active_by_id = {row.get("obligation_id"): row for row in active if isinstance(row, dict)}
    require(len(active_by_id) == 222 and set(prior_by_id) <= set(active_by_id),
            "E_ACTIVE_IDENTITY")
    require(len(set(active_by_id) - set(prior_by_id)) == 3, "E_NEW_ACTIVE_COUNT")
    for obligation_id, prior_row in prior_by_id.items():
        current = active_by_id[obligation_id]
        if obligation_id not in OWNER_TARGETS:
            require(typed_equal(current, prior_row), "E_INHERITED_ACTIVE_DRIFT", obligation_id)
        else:
            transition = by_id[obligation_id]
            expected_current = copy.deepcopy(prior_row)
            links = set(prior_row.get("relation_links", [])) | \
                set(transition["relation_links"])
            expected_current.update({
                "acceptance_criterion": transition["acceptance_criterion"],
                "canonical_owner": transition["canonical_owner"],
                "external_authority_promoted": False,
                "relation_links": sorted(links),
                "state": transition["state"],
                "target_phase": transition["target_phase"],
            })
            require(typed_equal(current, expected_current),
                    "E_TRANSITION_ACTIVE", obligation_id)
    new_active = {key: active_by_id[key]
                  for key in set(active_by_id) - set(prior_by_id)}
    require(set(new_active) == set(NEW_OBLIGATIONS), "E_NEW_ACTIVE_IDS")
    new_rows = carry.get("new_obligations")
    require(isinstance(new_rows, list) and len(new_rows) == 3,
            "E_NEW_OBLIGATIONS")
    new_rows_by_id = {row.get("obligation_id"): row for row in new_rows
                      if isinstance(row, dict)}
    require(set(new_rows_by_id) == set(NEW_OBLIGATIONS), "E_NEW_OBLIGATION_IDS")
    new_schema = {
        "acceptance_criterion", "authority_ceiling", "canonical_owner", "claim",
        "external_authority_promoted", "obligation_id", "origin_identity",
        "origin_path", "origin_pointer", "origin_record_sha256", "relation_links",
        "semantic_fingerprint", "state", "target_phase",
    }
    for obligation_id, (origin, owner, phase, collection, index, links) in \
            NEW_OBLIGATIONS.items():
        row = new_rows_by_id[obligation_id]
        require(set(row) == new_schema, "E_NEW_OBLIGATION_SCHEMA", obligation_id)
        require(typed_equal(row, new_active[obligation_id]),
                "E_NEW_ACTIVE_BINDING", obligation_id)
        require(row.get("origin_identity") == origin and
                row.get("canonical_owner") == owner and
                row.get("target_phase") == phase and row.get("state") == "OPEN_CARRY",
                "E_NEW_OBLIGATION_ROUTE", obligation_id)
        expected_pointer = f"/{collection}/{index}"
        require(row.get("origin_path") == INPUT_PATHS[9] and
                row.get("origin_pointer") == expected_pointer and
                row.get("origin_record_sha256") == record_sha(
                    resolve_pointer(inputs[INPUT_PATHS[9]], expected_pointer)) and
                row.get("relation_links") == links,
                "E_NEW_OBLIGATION_ORIGIN", obligation_id)
        require(isinstance(row.get("claim"), str) and row["claim"] and
                isinstance(row.get("acceptance_criterion"), str) and
                row["acceptance_criterion"] and
                isinstance(row.get("authority_ceiling"), str) and
                row["authority_ceiling"], "E_NEW_OBLIGATION_BOUND", obligation_id)
        require(row.get("semantic_fingerprint") ==
                sha(canonical({"claim": row["claim"]})) and
                row.get("external_authority_promoted") is False,
                "E_NEW_OBLIGATION_SEAL", obligation_id)
    require(all(isinstance(row.get("canonical_owner"), str) and row["canonical_owner"] and
                isinstance(row.get("acceptance_criterion"), str) and
                row["acceptance_criterion"] for row in active), "E_OWNERLESS_ACTIVE")
    require(all(row.get("canonical_owner") != "P067-CODE-HISTORY" for row in active),
            "E_P067_OWNER_REMAINS")

    registry_envelope = carry.get("current_owner_duplicate_check_universe")
    require(isinstance(registry_envelope, dict), "E_REGISTRY_ENVELOPE")
    registry = registry_envelope.get("records")
    require(isinstance(registry, list) and len(registry) == 358 and
            registry_envelope.get("record_count") == 358, "E_REGISTRY_COUNT")
    require(registry_envelope.get("records_sha256") == record_sha(registry),
            "E_REGISTRY_SEAL")
    origins = [row.get("origin_identity") for row in registry if isinstance(row, dict)]
    require(len(origins) == len(set(origins)) == 358, "E_REGISTRY_DUPLICATE")
    prior_registry = prior["current_owner_duplicate_check_universe"]["records"]
    prior_registry_by_origin = {row["origin_identity"]: row for row in prior_registry}
    registry_by_origin = {row["origin_identity"]: row for row in registry}
    require(set(prior_registry_by_origin) <= set(registry_by_origin) and
            len(set(registry_by_origin) - set(prior_registry_by_origin)) == 3,
            "E_REGISTRY_INHERITANCE")
    for origin, prior_row in prior_registry_by_origin.items():
        current = registry_by_origin[origin]
        transition_id = next((key for key, value in OWNER_TARGETS.items()
                              if value[0] == origin), None)
        if transition_id is None:
            require(typed_equal(current, prior_row), "E_INHERITED_REGISTRY_DRIFT", origin)
        else:
            transition = by_id[transition_id]
            expected_current = copy.deepcopy(prior_row)
            expected_current.update({
                "owner_id": transition["canonical_owner"],
                "state": transition["state"],
                "target_phase": transition["target_phase"],
            })
            require(typed_equal(current, expected_current),
                    "E_TRANSITION_REGISTRY", origin)
    for obligation_id, row in new_rows_by_id.items():
        registry_row = registry_by_origin[row["origin_identity"]]
        require(registry_row.get("origin_record_sha256") == row["origin_record_sha256"] and
                registry_row.get("owner_id") == row["canonical_owner"] and
                registry_row.get("state") == row["state"] and
                registry_row.get("target_phase") == row["target_phase"],
                "E_NEW_REGISTRY_BINDING", obligation_id)
    active_origins = [row.get("origin_identity") for row in active]
    require(len(active_origins) == len(set(active_origins)) and
            set(active_origins) <= set(registry_by_origin), "E_ACTIVE_OWNER_CARDINALITY")

    authority = carry.get("authority_boundary")
    require(isinstance(authority, dict), "E_AUTHORITY_BOUNDARY")
    for key, value in AUTHORITY_BOUNDARY.items():
        require(authority.get(key) == value, "E_AUTHORITY_BOUNDARY", key)
    require(all(value is False for value in authority.values()
                if isinstance(value, bool)), "E_AUTHORITY_BOOLEAN")
    summary = carry.get("gate_summary")
    require(isinstance(summary, dict), "E_GATE_SUMMARY")
    require(set(summary) == {
        "active_obligations", "blob_disposition_groups", "disposition_counts",
        "external_authority_promotions", "family_counts", "gate",
        "lost_inherited_ids", "lost_inherited_obligations",
        "multiply_owned_active_obligations", "new_obligations",
        "owner_registry_records", "owner_transitions", "p067_owner_transitions",
        "ownerless_active_obligations", "prior_active_obligations",
        "prior_owner_registry_records", "source_dispositions",
        "source_disposition_records", "status",
    }, "E_GATE_SUMMARY_SCHEMA")
    for key, value in GATE_SUMMARY_EXPECTED.items():
        require(summary.get(key) == value, "E_GATE_SUMMARY", key)
    family_counts = summary.get("family_counts")
    require(isinstance(family_counts, dict) and family_counts,
            "E_FAMILY_COUNTS")
    observed_family: dict[str, int] = {}
    for row in records:
        tokens = pointer_tokens(row["origin_pointer"])
        require(tokens, "E_FAMILY_POINTER")
        key = f"S{row['origin_step']}:{Path(row['origin_path']).stem}:{tokens[0]}"
        observed_family[key] = observed_family.get(key, 0) + 1
    require(family_counts == observed_family == expected_family,
            "E_FAMILY_COUNT_BINDING")
    disposition_counts = {name: sum(row["disposition"] == name for row in records)
                          for name in ALLOWED_DISPOSITIONS}
    require(summary.get("disposition_counts") == disposition_counts and
            summary.get("owner_transitions") == 3 and
            summary.get("lost_inherited_obligations") == 0 and
            summary.get("source_disposition_records") == 157 and
            summary.get("status") == "PASS_WITH_EXPLICIT_OPEN_CARRY",
            "E_GATE_SUMMARY_BINDING")


def validate_preview(source: dict[str, Any], carry: dict[str, Any]) -> None:
    first = builder_preview()
    second = builder_preview()
    require(typed_equal(first, second), "E_BUILDER_NONDETERMINISTIC")
    require(typed_equal(first["source_disposition"], source), "E_SOURCE_REBUILD")
    require(typed_equal(first["carry_forward"], carry), "E_CARRY_REBUILD")


def put(mapping: Any, key: Any, value: Any) -> None:
    mapping[key] = value


def reseal(value: dict[str, Any]) -> None:
    value["semantic_sha256"] = semantic(value, "compact_lf")


def negative_controls(source: dict[str, Any], carry: dict[str, Any],
                      inputs: dict[str, dict[str, Any]],
                      input_records: list[dict[str, Any]]) -> int:
    mutations: list[tuple[str, str, Any]] = []

    def add(label: str, target: str, fn: Any) -> None:
        mutations.append((label, target, fn))

    add("source_drop", "source", lambda x: x["source_dispositions"].pop())
    add("source_duplicate", "source", lambda x: x["source_dispositions"].append(
        copy.deepcopy(x["source_dispositions"][0])))
    add("source_blob", "source", lambda x: put(x["source_dispositions"][0], "blob_oid", "0" * 40))
    add("source_role", "source", lambda x: put(x["source_dispositions"][0], "role", "demo"))
    add("source_disposition", "source", lambda x: put(x["source_dispositions"][0], "disposition", "ACCEPT"))
    add("source_promotion", "source", lambda x: put(x["source_dispositions"][0], "external_authority_promoted", True))
    add("source_contract", "source", lambda x: put(x["source_contract"], "python_occurrences", 128))
    add("blob_projection", "source", lambda x: put(x["blob_disposition_groups"][0], "occurrence_count", 999))
    add("carry_source_seal", "carry", lambda x: put(x, "source_disposition_semantic_sha256", "0" * 64))
    add("prior_carry_loss", "carry", lambda x: x["prior_phase066_carry"]["active_obligations"].pop())
    add("finding_drop", "carry", lambda x: x["step82_89_disposition_records"].pop())
    add("finding_duplicate", "carry", lambda x: x["step82_89_disposition_records"].append(
        copy.deepcopy(x["step82_89_disposition_records"][0])))
    add("finding_origin", "carry", lambda x: put(x["step82_89_disposition_records"][0], "origin_record_sha256", "0" * 64))
    add("finding_promotion", "carry", lambda x: put(x["step82_89_disposition_records"][0], "external_authority_promoted", True))
    add("transition_drop", "carry", lambda x: x["owner_transitions"].pop())
    add("transition_owner", "carry", lambda x: put(x["owner_transitions"][0], "canonical_owner", "OTHER"))
    add("transition_false_resolve", "carry", lambda x: put(x["owner_transitions"][0], "state", "RESOLVED"))
    add("active_loss", "carry", lambda x: x["active_obligations"].pop(0))
    add("active_duplicate", "carry", lambda x: x["active_obligations"].append(
        copy.deepcopy(x["active_obligations"][0])))
    add("active_ownerless", "carry", lambda x: put(x["active_obligations"][0], "canonical_owner", ""))
    add("registry_duplicate", "carry", lambda x: x["current_owner_duplicate_check_universe"]["records"].append(
        copy.deepcopy(x["current_owner_duplicate_check_universe"]["records"][0])))
    add("authority_promotion", "carry", lambda x: put(x["authority_boundary"], "publication", True))
    add("ref7_promotion", "carry", lambda x: put(x["authority_boundary"], "ref7_original_full_text", "VERIFIED"))
    add("summary_drift", "carry", lambda x: put(x["gate_summary"], "active_obligations", 221))

    passed = 0
    for label, target, mutate in mutations:
        source_copy = copy.deepcopy(source)
        carry_copy = copy.deepcopy(carry)
        mutate(source_copy if target == "source" else carry_copy)
        reseal(source_copy)
        reseal(carry_copy)
        try:
            validate_source(source_copy, inputs, input_records)
            validate_carry(carry_copy, source_copy, inputs, input_records)
        except ValidationError:
            passed += 1
        else:
            raise ValidationError("E_NEGATIVE_CONTROL:" + label)
    return passed


def json_controls() -> int:
    cases = [
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        b'{"a":' + b'[' * 65 + b'0' + b']' * 65 + b'}',
        b'{"a":1} trailing',
        b'[]',
    ]
    passed = 0
    for raw in cases:
        try:
            strict_load(raw, "E_JSON_CONTROL", "unchecked", "unchecked")
        except ValidationError:
            passed += 1
        else:
            raise ValidationError("E_JSON_CONTROL_ACCEPTED")
    return passed


def lf_bytes(raw: bytes) -> bytes:
    return raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def neutral_source_hash(raw: bytes, role: str) -> str:
    text = lf_bytes(raw).decode("utf-8")
    if role == "validator":
        text, count = re.subn(
            r'(?m)^VALIDATOR_NEUTRAL_SHA256_LF = "[0-9a-f]{64}"$',
            'VALIDATOR_NEUTRAL_SHA256_LF = "' + "0" * 64 + '"', text,
        )
        require(count == 1, "E_VALIDATOR_NEUTRAL_SLOT")
    return sha(text.encode("utf-8"))


def source_policy_errors(source: str, role: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return ["E_AST_PARSE:" + str(exc)]
    parents = {child: parent for parent in ast.walk(tree)
               for child in ast.iter_child_nodes(parent)}

    expected_imports = {
        "builder": {"argparse", "copy", "hashlib", "json", "math", "os",
                    "subprocess", "sys"},
        "validator": {"argparse", "ast", "copy", "hashlib", "json", "math", "re",
                      "subprocess", "sys"},
    }[role]
    expected_from = {("__future__", "annotations"), ("pathlib", "Path"),
                     ("typing", "Any")}
    imports: set[str] = set()
    from_imports: set[tuple[str, str]] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if not isinstance(parents.get(node), ast.Module):
                errors.append("E_NESTED_IMPORT")
            for alias in node.names:
                imports.add(alias.name)
                if alias.asname is not None:
                    errors.append("E_IMPORT_ALIAS")
        elif isinstance(node, ast.ImportFrom):
            if not isinstance(parents.get(node), ast.Module) or node.level != 0:
                errors.append("E_NESTED_FROM_IMPORT")
            for alias in node.names:
                from_imports.add((str(node.module), alias.name))
                if alias.asname is not None or alias.name == "*":
                    errors.append("E_FROM_IMPORT_ALIAS")
    if imports != expected_imports:
        errors.append("E_IMPORT_INVENTORY")
    if from_imports != expected_from:
        errors.append("E_FROM_IMPORT_INVENTORY")

    expected_module_bindings = {
        "builder": [
            "ROOT", "BASELINE", "EXPECTED_PARENT", "BRANCH", "DATE", "SUBJECT", "GATE",
            "PERSISTENCE", "SOURCE_PATH", "CARRY_PATH", "RESULT_PATH", "PARENT_LEDGER",
            "CANONICAL_LEDGER", "HANDOVER", "HUMAN_PREREQUISITES", "INVENTORY", "FULL_READ",
            "STATE_FLOW", "CALL_GRAPH", "STATE_DEFAULT", "SAVED_RUNTIME", "TEST_MATRIX",
            "GUIDE_MATRIX", "UNIT_MATRIX", "GUARD_MATRIX", "FITTING_MATRIX",
            "FITTING_RUNTIME", "PRIOR_CARRY", "INPUT_PATHS", "INPUT_EXPECTED",
            "DISPOSITIONS", "AUTHORITY_FALSE", "FINDING_SPECS", "TRANSITION_POLICIES",
            "NEW_OBLIGATION_POLICIES",
        ],
        "validator": [
            "ROOT", "BASELINE", "EXPECTED_PARENT", "BRANCH", "PROTECTED_TIP", "MAIN_TIP",
            "SUBJECT", "GATE", "PERSISTENCE", "BUILDER", "VALIDATOR", "SOURCE_PATH",
            "CARRY_PATH", "RESULT", "PARENT_LEDGER", "CANONICAL_LEDGER", "HANDOVER",
            "FINAL_PATHS", "FINAL_STATUS", "INPUT_PATHS", "INPUT_EXPECTED",
            "ALLOWED_DISPOSITIONS", "SOURCE_CONTRACT_EXPECTED", "OWNER_TARGETS",
            "NEW_OBLIGATIONS", "OWNER_LINKS", "FINDING_FAMILIES", "AUTHORITY_BOUNDARY",
            "SOURCE_AUTHORITY", "GATE_SUMMARY_EXPECTED", "MAX_JSON_BYTES", "MAX_JSON_DEPTH",
            "MAX_JSON_NODES", "BUILDER_SOURCE_SHA256_LF", "VALIDATOR_NEUTRAL_SHA256_LF",
        ],
    }[role]
    module_binding_names: list[str] = []
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            module_binding_names.extend(
                target.id for target in statement.targets if isinstance(target, ast.Name))
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            module_binding_names.append(statement.target.id)
    if module_binding_names != expected_module_bindings:
        errors.append("E_MODULE_BINDING_INVENTORY")

    expected_functions = {
        "builder": {
            "require", "sha", "canonical", "semantic", "input_semantic", "finish",
            "strict_json", "git_argv_allowed", "git_bytes", "read_inputs", "record_hash",
            "source_row", "build_source", "pointer_escape", "rows_for", "build_findings",
            "fingerprint", "build_carry", "build", "atomic_write",
            "verify_human_prerequisites", "main",
        },
        "validator": {
            "require", "sha", "canonical", "pretty", "semantic", "record_sha",
            "typed_equal", "strict_load", "is_oid", "git_argv_allowed", "git_bytes",
            "git_text", "input_tree", "load_inputs", "builder_preview", "load_outputs",
            "require_metadata", "normalized_role", "pointer_tokens", "resolve_pointer",
            "pointer_token", "expected_finding_crosswalk", "expected_blob_origins",
            "expected_source_identities",
            "validate_source", "validate_disposition_records", "validate_carry",
            "validate_preview", "put", "reseal", "negative_controls", "json_controls",
            "lf_bytes", "neutral_source_hash", "source_policy_errors",
            "source_policy_controls", "source_policy", "git_argv_controls", "parse_status",
            "parse_name_status", "require_index_modes", "require_tree_modes",
            "repository_guard", "control_documents", "main",
        },
    }[role]
    function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    class_names = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    if set(function_names) != expected_functions or len(function_names) != len(expected_functions):
        errors.append("E_FUNCTION_INVENTORY")
    expected_classes = {"BuildError"} if role == "builder" else {"ValidationError"}
    if set(class_names) != expected_classes or len(class_names) != len(expected_classes):
        errors.append("E_CLASS_INVENTORY")
    expected_nested = {"builder": {"pairs"},
                       "validator": {"pairs", "add", "owner", "unique_line"}}[role]
    all_function_names = [node.name for node in ast.walk(tree)
                          if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if sorted(all_function_names) != sorted(expected_functions | expected_nested):
        errors.append("E_ALL_FUNCTION_INVENTORY")
    all_class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    if sorted(all_class_names) != sorted(expected_classes):
        errors.append("E_ALL_CLASS_INVENTORY")
    default_inventory = {
        node.name: ([ast.unparse(value) for value in node.args.defaults],
                    [None if value is None else ast.unparse(value)
                     for value in node.args.kw_defaults])
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        (node.args.defaults or node.args.kw_defaults)
    }
    expected_defaults = {
        "builder": {"source_row": ([], [None, None, None, None, None, None,
                                         None, None, None, None, "None"])},
        "validator": {"require": (["''"], [])},
    }[role]
    if default_inventory != expected_defaults:
        errors.append("E_FUNCTION_DEFAULT_INVENTORY")

    sensitive_names = {
        "builder": {"atomic_write", "git_argv_allowed", "git_bytes", "read_inputs",
                    "verify_human_prerequisites", "main"},
        "validator": {"builder_preview", "control_documents", "git_argv_allowed", "git_bytes",
                      "git_text", "input_tree", "load_inputs", "load_outputs",
                      "repository_guard", "require_index_modes", "require_tree_modes",
                      "source_policy"},
    }[role]
    sensitive_function_hashes = {
        node.name: sha(ast.unparse(node).encode("utf-8"))
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in sensitive_names
    }
    expected_sensitive_hashes = {
        "builder": {
            "atomic_write": "9d1dfd3f56137bf06f1cd2437a9064cb545d992149bcba5eb926b23ca86c883a",
            "git_argv_allowed": "2a7af39b5cf2f653247a92c8bd7b441cebb0f492ffb08569808ceb8497609126",
            "git_bytes": "7f80cf6f731a00daf11c721dd98ee10f727555b2c9a1878697e9d88f1916f887",
            "read_inputs": "4aa57ea89375cfca647a09e2094eb4533eb1b15360328282d32b06b62474c01c",
            "verify_human_prerequisites": "c90a3361cbb6cfd21cff2b282bfd4b51d9bd3c791325faa9e59819ad44501c39",
            "main": "c49e1dea9a447cd382f481804b10b3c63011a9f4fb12cb727fe0a94ab9ca8ddc",
        },
        "validator": {
            "builder_preview": "f94fe45f069b8ea9adec7016769d80afaaa6827dab7055a32ebf29ba8e236880",
            "control_documents": "0f79ad1e642bd3654c78f68e4c1453fc916c7f93e6cb8730c89f558900c5e0b4",
            "git_argv_allowed": "8080e7dca456357105fc45fd8b5f48f3ea3db88a4c1822382a0a2beade5e5638",
            "git_bytes": "891f350b6ec9f55a31d3fade570de66b278a73082a3aa9329981100f2d8ce3f3",
            "git_text": "2803db0d40d74ddbbc033316d1670fb8ee8957999d3c1522a51184eca0ded93e",
            "input_tree": "a6dc593609d7ea0aa5d3deb75a00c2a1d9301f226a2783f99b26853781b2c2f5",
            "load_inputs": "e83e9c272d749ae9fbd8d4256562d968960886925d9e81569bd88bd3e1e3d3af",
            "load_outputs": "0f099c54f412181c20b5dd43bb9faf90fb61e9e802f40e777ebf3b71c25063f2",
            "repository_guard": "1b3d9a1c0b9652fea0303330449ea3d87f93f45708a631daf4624a2d27cc4e6c",
            "require_index_modes": "c7ff3d7f4f98239aaf05a55592a40b15760584853d3be7f3407f04db07937e75",
            "require_tree_modes": "b95ff386f00ccec3fd22db69df0d895538619b920416a75e2885da55ab477fba",
            "source_policy": "f71a1010c849f8358b74a0a307410015cad410d65c18c32631c9f8a377b23bdf",
        },
    }[role]
    if sensitive_function_hashes != expected_sensitive_hashes:
        errors.append("E_SENSITIVE_FUNCTION_HASHES")

    sensitive = {"eval", "exec", "compile", "__import__", "input", "open", "getattr",
                 "setattr", "delattr", "globals", "locals", "vars", "__builtins__",
                 "breakpoint"}
    modules = expected_imports
    protected_callables = expected_functions
    protected_builtins = {
        "all", "any", "bool", "dict", "enumerate", "int", "isinstance", "len", "list",
        "max", "min", "next", "print", "range", "repr", "set", "sorted", "str", "sum",
        "tuple", "type", "zip",
    }
    module_constants = set(expected_module_bindings)

    def owner(node: ast.AST) -> str:
        current = parents.get(node)
        while current is not None:
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return current.name
            current = parents.get(current)
        return "<module>"

    allowed_module_attributes = {
        "builder": {
            "argparse": {"ArgumentParser"}, "copy": {"deepcopy"},
            "hashlib": {"sha256"}, "json": {"JSONDecodeError", "dumps", "loads"},
            "math": {"isfinite"}, "os": {"replace"},
            "subprocess": {"PIPE", "run"}, "sys": {"stderr", "stdout"},
        },
        "validator": {
            "argparse": {"ArgumentParser"},
            "ast": {"AST", "AnnAssign", "Assign", "AsyncFunctionDef", "Attribute", "Call",
                    "ClassDef", "Del", "ExceptHandler", "Expr", "FunctionDef", "Import",
                    "ImportFrom", "Load", "MatchAs", "MatchMapping", "MatchStar", "Module",
                    "Name", "Return", "Store", "Try", "arg", "iter_child_nodes", "parse",
                    "unparse", "walk"},
            "copy": {"deepcopy"}, "hashlib": {"sha256"},
            "json": {"JSONDecodeError", "dumps", "loads"}, "math": {"isfinite"},
            "re": {"fullmatch", "search", "subn"}, "subprocess": {"PIPE", "run"},
            "sys": {"executable", "stderr"},
        },
    }[role]
    forbidden_attrs = {
        "Popen", "call", "check_call", "check_output", "system", "popen", "spawn",
        "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve", "spawnvp",
        "spawnvpe", "open", "touch", "write_text", "read_text", "unlink", "rmdir",
        "remove", "rmtree", "rename", "chmod", "lchmod", "symlink_to", "hardlink_to",
        "link_to", "copy", "copy_into", "move", "move_into", "stat", "lstat", "exists",
        "is_dir", "is_symlink", "is_junction", "iterdir", "glob", "rglob", "walk",
        "readlink", "samefile", "owner", "group", "resolve", "is_mount", "is_socket",
        "is_fifo", "is_block_device", "is_char_device",
    }
    protected_fs_attrs = forbidden_attrs | {"write_bytes", "read_bytes", "mkdir", "is_file",
                                            "replace"}
    protected_names = protected_callables | modules | protected_builtins | module_constants | {"Path"}
    allowed_name_calls = protected_callables | expected_nested | expected_classes | \
        protected_builtins | {"Path", "SystemExit", "ValueError", "mutate"}
    process_calls: list[tuple[str, str]] = []
    argparse_calls: list[tuple[str, str]] = []
    path_calls: list[tuple[str, str]] = []
    fs_calls: list[tuple[str, str, str]] = []
    protected_git_calls: list[tuple[str, str]] = []
    replace_calls: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                (node.decorator_list or node.type_params):
            errors.append("E_FUNCTION_DECORATOR_OR_TYPE_PARAMS:" + node.name)
        if isinstance(node, ast.ClassDef):
            if node.decorator_list or node.keywords or node.type_params:
                errors.append("E_CLASS_DECORATOR_KEYWORD_OR_TYPE_PARAMS:" + node.name)
            if [ast.unparse(base) for base in node.bases] != ["RuntimeError"]:
                errors.append("E_CLASS_BASE_INVENTORY:" + node.name)
        if isinstance(node, ast.arg) and node.arg in protected_names:
            errors.append("E_PROTECTED_ARGUMENT:" + node.arg)
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and \
                node.id in protected_names:
            original = node.id in module_constants and owner(node) == "<module>" and \
                isinstance(node.ctx, ast.Store) and parents.get(node) in tree.body
            if not original:
                errors.append("E_PROTECTED_REBIND:" + node.id)
        if isinstance(node, ast.ExceptHandler) and node.name in protected_names:
            errors.append("E_PROTECTED_EXCEPTION_BINDING:" + str(node.name))
        if isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name in protected_names:
            errors.append("E_PROTECTED_PATTERN_BINDING:" + str(node.name))
        if isinstance(node, ast.MatchMapping) and node.rest in protected_names:
            errors.append("E_PROTECTED_PATTERN_REST:" + str(node.rest))
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in sensitive:
                errors.append("E_SENSITIVE_NAME:" + node.id)
            if node.id in modules:
                parent = parents.get(node)
                if not isinstance(parent, ast.Attribute) or parent.value is not node:
                    errors.append("E_MODULE_ESCAPE:" + node.id)
            if node.id in protected_callables:
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_CALLABLE_ESCAPE:" + node.id)
            if node.id == "Path":
                parent = parents.get(node)
                annotation = isinstance(parent, ast.arg) and parent.annotation is node
                if not annotation and (not isinstance(parent, ast.Call) or parent.func is not node):
                    errors.append("E_PATH_ESCAPE")
        if isinstance(node, ast.Attribute):
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                errors.append("E_ATTRIBUTE_MUTATION:" + node.attr)
            if node.attr.startswith("__"):
                errors.append("E_DUNDER_ATTRIBUTE:" + node.attr)
            if isinstance(node.value, ast.Name) and node.value.id in modules and \
                    node.attr not in allowed_module_attributes[node.value.id]:
                errors.append("E_MODULE_ATTRIBUTE_INVENTORY:" + node.value.id + "." + node.attr)
            if isinstance(node.value, ast.Name) and node.value.id == "subprocess" and \
                    node.attr == "run" and not (
                        isinstance(parents.get(node), ast.Call) and parents[node].func is node):
                errors.append("E_BOUND_SUBPROCESS_RUN")
            if isinstance(node.value, ast.Name) and node.value.id == "argparse" and \
                    node.attr == "ArgumentParser" and not (
                        isinstance(parents.get(node), ast.Call) and parents[node].func is node):
                errors.append("E_BOUND_ARGUMENT_PARSER")
            if node.attr in protected_fs_attrs:
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_BOUND_FILESYSTEM_METHOD:" + node.attr)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                errors.append("E_INDIRECT_CALL")
            if any(keyword.arg is None or keyword.arg == "shell" for keyword in node.keywords):
                errors.append("E_DYNAMIC_OR_SHELL_KEYWORD")
            if isinstance(node.func, ast.Name) and node.func.id == "Path":
                path_calls.append((owner(node), ast.unparse(node)))
            if isinstance(node.func, ast.Name) and node.func.id not in allowed_name_calls:
                errors.append("E_NAME_CALL_INVENTORY:" + node.func.id)
            if isinstance(node.func, ast.Name) and node.func.id in sensitive:
                errors.append("E_SENSITIVE_CALL:" + node.func.id)
            if isinstance(node.func, ast.Name) and node.func.id in {"git_bytes", "git_text"}:
                protected_git_calls.append((owner(node), ast.unparse(node)))
            if isinstance(node.func, ast.Attribute):
                module_attribute = isinstance(node.func.value, ast.Name) and \
                    node.func.value.id in modules and \
                    node.func.attr in allowed_module_attributes[node.func.value.id]
                regex_group = node.func.attr == "group" and owner(node) in {
                    "input_tree", "require_index_modes", "require_tree_modes"
                }
                root_resolve = node.func.attr == "resolve" and owner(node) == "<module>" and \
                    ast.unparse(node) == "Path(__file__).resolve()"
                if node.func.attr in forbidden_attrs and not (
                        module_attribute or regex_group or root_resolve):
                    errors.append("E_FORBIDDEN_ATTRIBUTE_CALL:" + node.func.attr)
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    process_calls.append((owner(node), ast.unparse(node)))
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "argparse" and \
                        node.func.attr == "ArgumentParser":
                    argparse_calls.append((owner(node), ast.unparse(node)))
                    if node.keywords:
                        errors.append("E_ARGUMENT_PARSER_KEYWORDS")
                if node.func.attr in {"read_bytes", "write_bytes", "mkdir", "is_file"}:
                    fs_calls.append((owner(node), node.func.attr, ast.unparse(node)))
                if node.func.attr == "replace":
                    replace_calls.append((owner(node), ast.unparse(node)))

    replace_owner_counts: dict[str, int] = {}
    for replace_owner, _replace_call in replace_calls:
        replace_owner_counts[replace_owner] = replace_owner_counts.get(replace_owner, 0) + 1
    expected_replace_owner_counts = {
        "builder": {"atomic_write": 1, "pointer_escape": 2},
        "validator": {
            "input_tree": 1,
            "lf_bytes": 2,
            "parse_name_status": 1,
            "parse_status": 1,
            "pointer_token": 2,
            "pointer_tokens": 2,
            "require_index_modes": 1,
            "require_tree_modes": 1,
            "source_policy_controls": 13,
        },
    }[role]
    if replace_owner_counts != expected_replace_owner_counts:
        errors.append("E_REPLACE_CALL_INVENTORY")
    expected_replace_call_sha256 = {
        "builder": "bebf93d5724b70e4d8beff34a2d594f2c4c8eed602009f921d83fc5778a34e8f",
        "validator": "ad477cc74ec3ce719d24c5cc729e53aeb5fce2c35e7c84e4b96aebcb94122caa",
    }[role]
    if sha(canonical(sorted(replace_calls))) != expected_replace_call_sha256:
        errors.append("E_REPLACE_CALL_SEAL")

    expected_process = {
        "builder": [("git_bytes", "subprocess.run(['git', *args], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)")],
        "validator": [
            ("git_bytes", "subprocess.run(['git', *args], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
            ("builder_preview", "subprocess.run([sys.executable, '-B', str(ROOT / BUILDER), '--preview'], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
        ],
    }[role]
    if process_calls != expected_process:
        errors.append("E_PROCESS_INVENTORY")
    if argparse_calls != [("main", "argparse.ArgumentParser()")]:
        errors.append("E_ARGUMENT_PARSER_INVENTORY")
    expected_paths = {
        "builder": [("<module>", "Path(__file__)"), ("build_findings", "Path(path)")],
        "validator": [("<module>", "Path(__file__)"),
                      ("expected_finding_crosswalk", "Path(path)"),
                      ("validate_carry", "Path(row['origin_path'])")],
    }[role]
    if path_calls != expected_paths:
        errors.append("E_PATH_CONSTRUCTOR_INVENTORY")
    expected_fs = {
        "builder": [
            ("atomic_write", "write_bytes", "temporary.write_bytes(raw)"),
            ("verify_human_prerequisites", "is_file", "target.is_file()"),
            ("verify_human_prerequisites", "read_bytes", "target.read_bytes()"),
        ],
        "validator": [
            ("load_outputs", "is_file", "(ROOT / SOURCE_PATH).is_file()"),
            ("load_outputs", "is_file", "(ROOT / CARRY_PATH).is_file()"),
            ("load_outputs", "read_bytes", "(ROOT / SOURCE_PATH).read_bytes()"),
            ("load_outputs", "read_bytes", "(ROOT / CARRY_PATH).read_bytes()"),
            ("source_policy", "read_bytes", "(ROOT / BUILDER).read_bytes()"),
            ("source_policy", "read_bytes", "(ROOT / VALIDATOR).read_bytes()"),
            ("control_documents", "read_bytes", "(ROOT / path).read_bytes()"),
        ],
    }[role]
    if sorted(fs_calls) != sorted(expected_fs):
        errors.append("E_FILESYSTEM_INVENTORY")
    expected_git_calls = {
        "builder": [
            ("read_inputs", "git_bytes(['ls-tree', EXPECTED_PARENT, '--', *INPUT_PATHS])"),
            ("read_inputs", "git_bytes(['show', f'{EXPECTED_PARENT}:{path}'])"),
        ],
        "validator": [
            ("git_text", "git_bytes(args, code)"),
            ("input_tree", "git_text(['ls-tree', EXPECTED_PARENT, '--', *INPUT_PATHS], 'E_INPUT_TREE')"),
            ("load_inputs", "git_bytes(['show', f'{EXPECTED_PARENT}:{path}'], 'E_INPUT_READ')"),
            ("repository_guard", "git_bytes(['status', '--porcelain=v1', '--untracked-files=all'], 'E_STATUS')"),
            ("repository_guard", "git_text(['diff', '--cached', '--name-only'], 'E_CONTENT_STAGED')"),
            ("repository_guard", "git_text(['diff', '--cached', '--name-status', '--no-renames', EXPECTED_PARENT, '--'], 'E_STAGED_DIFF')"),
            ("repository_guard", "git_text(['diff', '--name-only'], 'E_STAGED_WORKTREE')"),
            ("repository_guard", "git_text(['diff', '--name-only', PROTECTED_TIP, compare_head, '--', 'Claude'], 'E_CLAUDE_DRIFT')"),
            ("repository_guard", "git_text(['diff-tree', '--no-commit-id', '--name-status', '-r', '--no-renames', commit, '--'], 'E_COMMIT_DIFF')"),
            ("repository_guard", "git_text(['ls-remote', '--heads', 'origin', f'refs/heads/{BRANCH}'], 'E_LIVE_REMOTE')"),
            ("repository_guard", "git_text(['rev-parse', '@{u}'], 'E_UPSTREAM')"),
            ("repository_guard", "git_text(['rev-parse', 'HEAD'], 'E_HEAD')"),
            ("repository_guard", "git_text(['rev-parse', 'refs/remotes/origin/codex/lib-physics-endgame-v1025_2'], 'E_PROTECTED_TIP')"),
            ("repository_guard", "git_text(['rev-parse', 'refs/remotes/origin/main'], 'E_MAIN_TIP')"),
            ("repository_guard", "git_text(['rev-parse', f'refs/remotes/origin/{BRANCH}'], 'E_TRACKING')"),
            ("repository_guard", "git_text(['show', '--no-patch', '--format=%P', commit], 'E_COMMIT_PARENT')"),
            ("repository_guard", "git_text(['show', '--no-patch', '--format=%s', commit], 'E_COMMIT_SUBJECT')"),
            ("repository_guard", "git_text(['symbolic-ref', '--quiet', '--short', 'HEAD'], 'E_BRANCH')"),
            ("require_index_modes", "git_text(['ls-files', '--stage', '--', *FINAL_PATHS], 'E_INDEX_MODES')"),
            ("require_tree_modes", "git_text(['ls-tree', commit, '--', *FINAL_PATHS], 'E_TREE_MODES')"),
        ],
    }[role]
    if sorted(protected_git_calls) != sorted(expected_git_calls):
        errors.append("E_GIT_CALL_SITE_INVENTORY")
    expected_module_calls = {
        "builder": ["Path(__file__)", "Path(__file__).resolve()", "SystemExit(main())", "main()"],
        "validator": ["Path(__file__)", "Path(__file__).resolve()", "enumerate(FINAL_PATHS)",
                      "SystemExit(main())", "main()"],
    }[role]
    module_calls = [ast.unparse(node) for node in ast.walk(tree)
                    if isinstance(node, ast.Call) and owner(node) == "<module>"]
    if sorted(module_calls) != sorted(expected_module_calls):
        errors.append("E_MODULE_CALL_INVENTORY")
    if role == "validator":
        main_node = next((node for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name == "main"), None)
        if main_node is None:
            errors.append("E_MAIN_ABSENT")
        else:
            if len(main_node.body) != 5 or not isinstance(main_node.body[0], ast.Try) or \
                    not all(isinstance(node, ast.Expr) for node in main_node.body[1:4]) or \
                    not isinstance(main_node.body[4], ast.Return):
                errors.append("E_MAIN_BODY_SHAPE")
            first_try = main_node.body[0] if main_node.body else None
            if not isinstance(first_try, ast.Try) or first_try.orelse or first_try.finalbody or \
                    len(first_try.handlers) != 1:
                errors.append("E_MAIN_FIRST_TRY_SHAPE")
            elif len(first_try.body) < 3 or [ast.unparse(node) for node in first_try.body[:3]] != [
                "source_negative = source_policy()",
                "git_controls = git_argv_controls()",
                "parser = argparse.ArgumentParser()",
            ]:
                errors.append("E_MAIN_POLICY_PREFIX")
            calls = sorted((node for node in ast.walk(main_node) if isinstance(node, ast.Call)),
                           key=lambda node: (node.lineno, node.col_offset))
            call_names = [ast.unparse(node.func) for node in calls]
            if call_names[:2] != ["source_policy", "git_argv_controls"] or \
                    "argparse.ArgumentParser" not in call_names or \
                    call_names.index("source_policy") > call_names.index("argparse.ArgumentParser"):
                errors.append("E_POLICY_ORDER")
    else:
        main_node = next((node for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name == "main"), None)
        if main_node is None:
            errors.append("E_BUILDER_MAIN_ABSENT")
        else:
            prefix = [ast.unparse(node) for node in main_node.body[:3]]
            if len(main_node.body) != 4 or prefix != [
                "parser = argparse.ArgumentParser()",
                "parser.add_argument('--preview', action='store_true')",
                "args = parser.parse_args()",
            ] or not isinstance(main_node.body[3], ast.Try):
                errors.append("E_BUILDER_MAIN_SHAPE")
            main_try = main_node.body[3] if len(main_node.body) == 4 else None
            if not isinstance(main_try, ast.Try) or main_try.orelse or main_try.finalbody or \
                    len(main_try.handlers) != 1 or len(main_try.body) != 4:
                errors.append("E_BUILDER_MAIN_TRY_SHAPE")
            elif [ast.unparse(node) for node in main_try.body[:2]] != [
                "if not args.preview:\n    verify_human_prerequisites()",
                "source, carry = build()",
            ]:
                errors.append("E_BUILDER_PREREQUISITE_ORDER")
    return errors


def source_policy_controls(builder_source: str, validator_source: str) -> int:
    snippets = [
        "import subprocess as sp", "from pathlib import Path as P",
        "def nested():\n    import socket", "runner = subprocess.run",
        "runner = getattr(subprocess, 'run')", "subprocess.__getattribute__('run')",
        "__import__('os')", "(lambda: 1)()",
        "subprocess.run(['x'], shell=True)", "subprocess.run(['x'], shell=bool(1))",
        "subprocess.run(['x'], **{'shell': True})", "subprocess.Popen(['x'])",
        "os.system('x')", "Path('x').open('w')", "Path('x').touch()",
        "Path('x').write_text('x')", "writer = Path('x').write_bytes",
        "Path(r'\\\\server\\share\\x').read_bytes()", "argparse.FileType('w')",
        "argparse.ArgumentParser(fromfile_prefix_chars='@')", "reader = git_bytes",
        "git_bytes(['fetch'], 'E')", "source_policy = lambda: 1",
        "def git_argv_allowed(args):\n    return True\ngit_bytes(['fetch'], 'E')",
        "breakpoint()", "parser.fromfile_prefix_chars = '@'", "del source_policy",
        "match (lambda: 1):\n    case source_policy:\n        pass",
        "match {}:\n    case {**source_policy}:\n        pass",
        "match []:\n    case [*source_policy]:\n        pass",
        "try:\n    pass\nexcept Exception as source_policy:\n    pass",
        "all = lambda value: True", "bool = lambda value: True", "FINAL_PATHS = ()",
        "EXPECTED_PARENT = '0' * 40", "MAX_JSON_BYTES = 10 ** 100",
        "if True:\n    FINAL_PATHS = ()",
    ]
    passed = 0
    for index, snippet in enumerate(snippets):
        candidate = validator_source + "\n" + snippet + "\n"
        require(bool(source_policy_errors(candidate, "validator")),
                "E_SOURCE_POLICY_CONTROL", str(index))
        passed += 1
    builder_snippets = [
        "breakpoint()", "parser.fromfile_prefix_chars = '@'",
        "git_bytes(['clean', '-fd'])", "(ROOT / 'x').move(ROOT / 'outside')",
        "(ROOT / r'\\\\server\\share\\x').stat()",
        "os.replace('victim', 'outside')",
    ]
    for index, snippet in enumerate(builder_snippets):
        candidate = builder_source + "\n" + snippet + "\n"
        require(bool(source_policy_errors(candidate, "builder")),
                "E_BUILDER_SOURCE_POLICY_CONTROL", str(index))
        passed += 1
    reordered = validator_source.replace(
        "source_negative = source_policy()\n        git_controls = git_argv_controls()",
        "git_controls = git_argv_controls()\n        source_negative = source_policy()",
    )
    require(reordered != validator_source and bool(source_policy_errors(reordered, "validator")),
            "E_SOURCE_POLICY_ORDER_CONTROL")
    decorated = validator_source.replace(
        "def source_policy() -> int:",
        "@lambda original: (lambda: 1)\ndef source_policy() -> int:",
    )
    require(decorated != validator_source and bool(source_policy_errors(decorated, "validator")),
            "E_SOURCE_POLICY_DECORATOR_CONTROL")
    dead_order = validator_source.replace(
        "    try:\n        source_negative = source_policy()\n"
        "        git_controls = git_argv_controls()\n"
        "        parser = argparse.ArgumentParser()",
        "    if False:\n        source_negative = source_policy()\n"
        "        git_controls = git_argv_controls()\n"
        "    try:\n        source_negative = 0\n"
        "        git_controls = 0\n"
        "        parser = argparse.ArgumentParser()",
    )
    require(dead_order != validator_source and
            bool(source_policy_errors(dead_order, "validator")),
            "E_SOURCE_POLICY_DEAD_ORDER_CONTROL")
    eager_default = validator_source.replace(
        "def control_documents() -> None:",
        "def control_documents(_preview=builder_preview()) -> None:",
    )
    require(eager_default != validator_source and
            bool(source_policy_errors(eager_default, "validator")),
            "E_SOURCE_POLICY_EAGER_DEFAULT_CONTROL")
    git_toctou = builder_source.replace(
        '    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV")',
        '    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV")\n'
        '    args[:] = ["clean", "-fd"]',
    )
    require(git_toctou != builder_source and
            bool(source_policy_errors(git_toctou, "builder")),
            "E_SOURCE_POLICY_GIT_TOCTOU_CONTROL")
    write_toctou = builder_source.replace(
        "    require(path.parent == (ROOT / path.relative_to(ROOT)).parent, \"E_OUTPUT_PATH\")",
        "    path = ROOT / '//server/share/outside'\n"
        "    require(path.parent == (ROOT / path.relative_to(ROOT)).parent, \"E_OUTPUT_PATH\")",
    )
    require(write_toctou != builder_source and
            bool(source_policy_errors(write_toctou, "builder")),
            "E_SOURCE_POLICY_WRITE_TOCTOU_CONTROL")
    read_toctou = validator_source.replace(
        "def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:",
        "def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:\n"
        "    SOURCE_PATH = '//server/share/payload'",
    )
    require(read_toctou != validator_source and
            bool(source_policy_errors(read_toctou, "validator")),
            "E_SOURCE_POLICY_READ_TOCTOU_CONTROL")
    path_replace = builder_source.replace(
        "os.replace(temporary, path)",
        "os.replace(temporary, path)\n    path.replace('outside')",
    )
    second_replace = builder_source.replace(
        "os.replace(temporary, path)",
        "os.replace(temporary, path)\n    os.replace('victim', 'outside')",
    )
    require(path_replace != builder_source and bool(source_policy_errors(path_replace, "builder")),
            "E_SOURCE_POLICY_PATH_REPLACE_CONTROL")
    require(second_replace != builder_source and
            bool(source_policy_errors(second_replace, "builder")),
            "E_SOURCE_POLICY_SECOND_REPLACE_CONTROL")
    missing_prerequisite = builder_source.replace(
        "        if not args.preview:\n            verify_human_prerequisites()\n"
        "        source, carry = build()",
        "        source, carry = build()",
    )
    bypassed_prerequisite = builder_source.replace(
        "        if not args.preview:\n            verify_human_prerequisites()",
        "        if False:\n            verify_human_prerequisites()",
    )
    build_before_prerequisite = builder_source.replace(
        "        if not args.preview:\n            verify_human_prerequisites()\n"
        "        source, carry = build()",
        "        source, carry = build()\n"
        "        if not args.preview:\n            verify_human_prerequisites()",
    )
    write_before_prerequisite = builder_source.replace(
        "        if not args.preview:\n            verify_human_prerequisites()",
        "        atomic_write(ROOT / SOURCE_PATH, b'')\n"
        "        if not args.preview:\n            verify_human_prerequisites()",
    )
    for label, candidate in (
        ("MISSING", missing_prerequisite),
        ("BYPASSED", bypassed_prerequisite),
        ("BUILD_BEFORE", build_before_prerequisite),
        ("WRITE_BEFORE", write_before_prerequisite),
    ):
        require(candidate != builder_source and
                bool(source_policy_errors(candidate, "builder")),
                "E_SOURCE_POLICY_PREREQUISITE_" + label + "_CONTROL")
    return passed + 13


def source_policy() -> int:
    builder_raw = (ROOT / BUILDER).read_bytes()
    validator_raw = (ROOT / VALIDATOR).read_bytes()
    builder_source = builder_raw.decode("utf-8")
    validator_source = validator_raw.decode("utf-8")
    builder_errors = source_policy_errors(builder_source, "builder")
    validator_errors = source_policy_errors(validator_source, "validator")
    require(not builder_errors, "E_BUILDER_SOURCE_POLICY", ",".join(builder_errors[:5]))
    require(not validator_errors, "E_VALIDATOR_SOURCE_POLICY", ",".join(validator_errors[:5]))
    require(neutral_source_hash(builder_raw, "builder") == BUILDER_SOURCE_SHA256_LF,
            "E_BUILDER_SOURCE_HASH")
    require(neutral_source_hash(validator_raw, "validator") == VALIDATOR_NEUTRAL_SHA256_LF,
            "E_VALIDATOR_SOURCE_HASH")
    return source_policy_controls(builder_source, validator_source)


def git_argv_controls() -> int:
    good = [
        ("show", f"{EXPECTED_PARENT}:{INPUT_PATHS[0]}"),
        ("ls-tree", EXPECTED_PARENT, "--", *INPUT_PATHS),
        ("rev-parse", "HEAD"),
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--cached", "--name-only"),
        ("diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--"),
        ("diff", "--name-only"),
        ("diff", "--name-only", PROTECTED_TIP, EXPECTED_PARENT, "--", "Claude"),
        ("show", "--no-patch", "--format=%P", EXPECTED_PARENT),
        ("show", "--no-patch", "--format=%s", EXPECTED_PARENT),
        ("diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames",
         EXPECTED_PARENT, "--"),
        ("ls-tree", EXPECTED_PARENT, "--", *FINAL_PATHS),
        ("ls-files", "--stage", "--", *FINAL_PATHS),
        ("rev-parse", "@{u}"),
        ("rev-parse", f"refs/remotes/origin/{BRANCH}"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
    ]
    bad = [
        (), ("fetch",), ("status", "--short"),
        ("show", f"main:{INPUT_PATHS[0]}"),
        ("ls-tree", EXPECTED_PARENT, "--", *INPUT_PATHS[:-1]),
        ("diff", "--name-only", PROTECTED_TIP, EXPECTED_PARENT, "--", "Claude", "Codex"),
        ("show", "--no-patch", "--format=%P", "HEAD"),
        ("diff-tree", "--no-commit-id", "--name-status", "-r", EXPECTED_PARENT, "--"),
        ("ls-remote", "--heads", "origin", "refs/heads/main"),
    ]
    require(all(git_argv_allowed(case) for case in good), "E_GIT_ARGV_GOOD_CONTROL")
    require(all(not git_argv_allowed(case) for case in bad), "E_GIT_ARGV_BAD_CONTROL")
    return len(good) + len(bad)


def parse_status(raw: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not raw:
        return rows
    for line in raw.splitlines():
        require(len(line) >= 4, "E_STATUS_PARSE")
        code = line[:2]
        path = line[3:].replace("\\", "/")
        require(path not in rows, "E_STATUS_DUPLICATE")
        rows[path] = code
    return rows


def parse_name_status(raw: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not raw:
        return rows
    for line in raw.splitlines():
        parts = line.split("\t")
        require(len(parts) == 2 and parts[0] in {"A", "M"}, "E_DIFF_PARSE")
        path = parts[1].replace("\\", "/")
        require(path not in rows, "E_DIFF_DUPLICATE")
        rows[path] = parts[0]
    return rows


def require_index_modes() -> None:
    raw = git_text(["ls-files", "--stage", "--", *FINAL_PATHS], "E_INDEX_MODES")
    rows: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.fullmatch(r"([0-9]{6}) ([0-9a-f]{40}) 0\t(.+)", line)
        require(match is not None, "E_INDEX_MODE_PARSE")
        rows[match.group(3).replace("\\", "/")] = match.group(1)
    require(rows == {path: "100644" for path in FINAL_PATHS}, "E_INDEX_MODES")


def require_tree_modes(commit: str) -> None:
    raw = git_text(["ls-tree", commit, "--", *FINAL_PATHS], "E_TREE_MODES")
    rows: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.fullmatch(r"([0-9]{6}) blob [0-9a-f]{40}\t(.+)", line)
        require(match is not None, "E_TREE_MODE_PARSE")
        rows[match.group(2).replace("\\", "/")] = match.group(1)
    require(rows == {path: "100644" for path in FINAL_PATHS}, "E_TREE_MODES")


def repository_guard(mode: str, commit: str | None) -> None:
    head = git_text(["rev-parse", "HEAD"], "E_HEAD")
    require(git_text(["symbolic-ref", "--quiet", "--short", "HEAD"], "E_BRANCH") == BRANCH,
            "E_BRANCH")
    if mode in {"content", "staged"}:
        require(head == EXPECTED_PARENT, "E_HEAD_PARENT")
    else:
        require(commit is not None and re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
                "E_COMMIT_ARG")
        require(head == commit, "E_HEAD_COMMIT")
    require(git_text(["rev-parse", "refs/remotes/origin/main"], "E_MAIN_TIP") == MAIN_TIP,
            "E_MAIN_TIP")
    require(git_text([
        "rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"
    ], "E_PROTECTED_TIP") == PROTECTED_TIP, "E_PROTECTED_TIP")
    compare_head = commit if commit is not None else EXPECTED_PARENT
    claude = git_text(["diff", "--name-only", PROTECTED_TIP, compare_head, "--", "Claude"],
                      "E_CLAUDE_DRIFT")
    require(claude == "", "E_CLAUDE_DRIFT")

    status_raw = git_bytes(
        ["status", "--porcelain=v1", "--untracked-files=all"], "E_STATUS"
    ).decode("utf-8").rstrip("\r\n")
    status = parse_status(status_raw)
    if mode == "content":
        expected = {path: ("??" if index < 5 else " M")
                    for index, path in enumerate(FINAL_PATHS)}
        require(status == expected, "E_CONTENT_STATUS")
        require(git_text(["diff", "--cached", "--name-only"], "E_CONTENT_STAGED") == "",
                "E_CONTENT_STAGED")
    elif mode == "staged":
        expected = {path: ("A " if index < 5 else "M ")
                    for index, path in enumerate(FINAL_PATHS)}
        require(status == expected, "E_STAGED_STATUS")
        diff = parse_name_status(git_text([
            "diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--"
        ], "E_STAGED_DIFF"))
        require(diff == FINAL_STATUS, "E_STAGED_DIFF")
        require(git_text(["diff", "--name-only"], "E_STAGED_WORKTREE") == "",
                "E_STAGED_WORKTREE")
        require_index_modes()
    else:
        require(status == {}, "E_PERSISTENCE_DIRTY")
        assert commit is not None
        parent = git_text(["show", "--no-patch", "--format=%P", commit], "E_COMMIT_PARENT")
        subject = git_text(["show", "--no-patch", "--format=%s", commit], "E_COMMIT_SUBJECT")
        require(parent == EXPECTED_PARENT, "E_COMMIT_PARENT")
        require(subject == SUBJECT, "E_COMMIT_SUBJECT")
        diff = parse_name_status(git_text([
            "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames",
            commit, "--"
        ], "E_COMMIT_DIFF"))
        require(diff == FINAL_STATUS, "E_COMMIT_DIFF")
        require_tree_modes(commit)
        require(git_text(["rev-parse", "@{u}"], "E_UPSTREAM") == commit, "E_UPSTREAM")
        require(git_text(["rev-parse", f"refs/remotes/origin/{BRANCH}"], "E_TRACKING") ==
                commit, "E_TRACKING")
        live = git_text(["ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"],
                        "E_LIVE_REMOTE")
        require(live == f"{commit}\trefs/heads/{BRANCH}", "E_LIVE_REMOTE")


def control_documents() -> None:
    checks = {
        RESULT: ["# Phase 067 Step 90.1 Disposition Result", GATE, EXPECTED_PARENT,
                 SUBJECT, SOURCE_PATH, CARRY_PATH, "157", "94", "222", "358",
                 "Step 90.2"],
        PARENT_LEDGER: [EXPECTED_PARENT, "Step 90.1", GATE, SUBJECT, "Step 90.2"],
        CANONICAL_LEDGER: [EXPECTED_PARENT, "Step 90.1", GATE, SUBJECT, "Step 90.2"],
        HANDOVER: [EXPECTED_PARENT, "Step 90.1", GATE, SUBJECT, "Step 90.2"],
    }
    for path, tokens in checks.items():
        raw = (ROOT / path).read_bytes()
        require(len(raw) <= 2_000_000, "E_CONTROL_BYTES", path)
        text = raw.decode("utf-8")
        for token in tokens:
            require(token in text, "E_CONTROL_TOKEN", path + ":" + token)
        lines = text.splitlines()

        def unique_line(prefix: str) -> str:
            matches = [line for line in lines if line.startswith(prefix)]
            require(len(matches) == 1, "E_CONTROL_CURRENT_LINE", path + ":" + prefix)
            return matches[0]

        if path in {PARENT_LEDGER, CANONICAL_LEDGER}:
            phase_row = unique_line("| 067 |")
            for token in ("Steps 82–89 persisted", "Step 90.1", "PASS_PENDING_PERSISTENCE",
                          EXPECTED_PARENT, SUBJECT, GATE, "Step 90.2"):
                require(token in phase_row, "E_CONTROL_PHASE_ROW", path + ":" + token)
        if path == CANONICAL_LEDGER:
            step_row = unique_line("| Phase 067 Step 90.1 |")
            for token in ("PENDING_AT_PRECOMMIT_BY_DESIGN", "A/A/A/A/A/M/M/M",
                          EXPECTED_PARENT, SUBJECT, GATE, PERSISTENCE, "Step 90.2"):
                require(token in step_row, "E_CONTROL_STEP_ROW", token)
        if path == HANDOVER:
            current = unique_line("19. 현재 Phase 상태:")
            current_state = unique_line("- Phase 067 plan activation은 ")
            table_row = unique_line("| Phase 067 Step 90.1 |")
            for line in (current, current_state, table_row):
                for token in ("Step 90.1", GATE, "PASS_PENDING_PERSISTENCE", "Step 90.2"):
                    require(token in line, "E_CONTROL_HANDOVER_CURRENT", token)
            require(EXPECTED_PARENT in current and PERSISTENCE in current_state and
                    EXPECTED_PARENT in table_row and SUBJECT in table_row,
                    "E_CONTROL_HANDOVER_IDENTITY")
        if path == RESULT:
            require(text.startswith("# Phase 067 Step 90.1 Disposition Result\n\n"),
                    "E_CONTROL_RESULT_HEADING")
            gate_index = text.find("## Gate and Next Condition")
            require(gate_index >= 0, "E_CONTROL_RESULT_GATE_SECTION")
            gate_section = text[gate_index:]
            for token in (GATE, PERSISTENCE, "Step 90.2"):
                require(token in gate_section, "E_CONTROL_RESULT_GATE", token)


def main() -> int:
    try:
        source_negative = source_policy()
        git_controls = git_argv_controls()
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--verify-content", action="store_true")
        group.add_argument("--verify-staged", action="store_true")
        group.add_argument("--verify-persistence", metavar="COMMIT")
        args = parser.parse_args()
        mode = "content" if args.verify_content else \
            "staged" if args.verify_staged else "persistence"
        commit = args.verify_persistence if mode == "persistence" else None
        inputs, input_records = load_inputs()
        source, carry, nodes, depth = load_outputs()
        validate_source(source, inputs, input_records)
        validate_carry(carry, source, inputs, input_records)
        validate_preview(source, carry)
        negatives = negative_controls(source, carry, inputs, input_records)
        json_negative = json_controls()
        control_documents()
        repository_guard(mode, commit)
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"PASS_P067_STEP90_1_SOURCE_POLICY {source_negative}/{source_negative} "
          f"git_argv={git_controls}/{git_controls}")
    print(f"PASS_P067_STEP90_1_CONTROLS semantic={negatives}/{negatives} "
          f"json={json_negative}/{json_negative} nodes={nodes} depth={depth}")
    print(PERSISTENCE if mode == "persistence" else GATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
