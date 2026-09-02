#!/usr/bin/env python3
"""Validate Phase 067 Step 83 static state/quantity-flow evidence."""

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
EXPECTED_PARENT = "db167fdc941eafba0313b8476dfe7483108f13ff"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GENERATED_DATE = "2026-09-02"
EXPECTED_SUBJECT = "audit(phase067): trace state quantity flows"
GATE = "PASS_P067_STEP83_STATE_FLOW"
PERSISTENCE = "PASS_P067_STEP83_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "fce9a0bf6c1cbb0d33baa982e275fcc217596ce2eefe5c8990c4f610f3365222"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "3d6063f59219f97689fef793cf759cb4cb932ef50b49e9c51587e30c06d21a20"

BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step83.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step83.py"
MATRIX_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_083_STATE_FLOW_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
FINAL_PATHS = [BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RESULT_PATH,
               PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH]
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if index < 4 else "M") for index, path in enumerate(FINAL_PATHS)}
CONTROL_DOCUMENT_SHA256 = {
    RESULT_PATH: "06672cc5d5ed83a5243a0243fdcda539b07828c584a2a56319202bb575a207e4",
    PARENT_LEDGER_PATH: "4179735edeb464aa6cd7aed79477f938359601e739ddc2a16f5f2c8152e2a402",
    ACTIVE_LEDGER_PATH: "66a133886cbd0bc6808b5f5c3d8b1c3a5365667637a1e6841eda61af5fbec5d7",
    HANDOVER_PATH: "a397015988d84ec6eb1e7368d98d5295e4377a60b12b57f721993d4242bd235d",
}
INVENTORY_RAW_SHA256 = "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63"
INVENTORY_SEMANTIC_SHA256 = "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"
ATTESTATION_RAW_SHA256 = "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174"
ATTESTATION_SEMANTIC_SHA256 = "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"
CODE_PATH_SHA256 = "87a56bbf68f1218a329dc1dca785a7a53b6257421ef772f55001bbd7a14fa61e"
CODE_PATH_BLOB_SHA256 = "6785e0f94af65cf5d173d94acdf1fb19b8e32fad0c025dd8f4fd1cd48d06c5b3"
CODE_BLOB_SHA256 = "77083327d44f5f0ce39c6c6480095f2cb56a4bed0fb14e24bd4d58d4fc76efb6"
CODE_RELEASE_PATH_SHA256 = "dc2c84e4e132a5ed788c69725b142ebc97c2124f42e175c2c996ba7714dc322e"
CODE_OCCURRENCE_SHA256 = "f9ad50607a0001387ba015f6dc882c93ab23d1f55b46d152cdfa42fe942b1959"
RELEASES = [
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14",
    "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2",
    "v1.0.19", "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23",
    "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
]
QUANTITIES = ["voltage", "current", "capacity", "composition", "temperature"]
PRESENCE = ["ABSENT_IN_FROZEN_SOURCE", "GROUND_NOT_FOUND_STATIC_AMBIGUOUS", "PRESENT"]
CLASSIFICATIONS = ["DIRECT", "FALLBACK", "IGNORED", "INHERITED", "OVERWRITTEN"]

TOP_KEYS = {
    "schema_version", "artifact", "phase", "step", "generated_date", "baseline_commit",
    "expected_parent", "branch", "expected_subject", "gate", "persistence_terminal",
    "precommit_status", "containing_commit", "result_first", "json_outputs_last", "inputs",
    "universe", "quantity_contract", "source_records", "flow_records", "coverage",
    "validation", "authority", "semantic_sha256",
}
INPUT_KEYS = {"step82_inventory", "step82_full_read_attestation"}
INPUT_RECORD_KEYS = {"path", "raw_sha256", "semantic_sha256"}
OCCURRENCE_KEYS = {"manifest_entry_index", "path", "blob_oid", "blob_ordinal", "git_mode"}
SOURCE_KEYS = {"release_ordinal", "release", "manifest_entry_index", "path", "blob_oid",
               "blob_ordinal", "git_mode", "physical_lines", "raw_sha256", "ast_parse",
               "has_blend", "feature_flags", "quantity_coverage"}
FLOW_KEYS = {"flow_id", "release_ordinal", "release", "quantity", "presence", "occurrence",
             "definition", "state_identities", "routes", "gaps", "authority"}
IDENTITY_KEYS = {"identity_id", "symbol", "unit", "basis", "sign", "scope", "source_status", "evidence_status", "evidence", "route_refs"}
ROUTE_KEYS = {"route_id", "condition", "classification", "public_inputs", "producer",
              "ordered_transforms", "consumers", "output", "alternate_producer"}
TRANSFORM_KEYS = {"ordinal", "state_in", "state_out", "operation", "order_authority", "evidence"}
ANCHOR_KEYS = {"qualified_definition", "ast_kind", "start_line", "end_line", "source_sha256",
               "node_sha256", "expression"}
GAP_KEYS = {"gap", "owner"}
FEATURE_KEYS = {"temperature_route", "temperature_dependent_width_multiplicity",
                "vibrational_temperature", "global_composition_solver",
                "lco_composition_centers", "lco_curve_facade_sign_flip",
                "blend_mass_to_capacity_fraction", "executable_divide_by_3600",
                "comment_only_seconds_conversion", "default_profile_conflict_bounded"}
FEATURE_KEYS.add("transition_capacity_unit_mAh_explicit")
AUTHORITY_EXPECTED = {
    "source_identity": True, "static_ast_connectivity": True,
    "static_lexical_transform_order": True, "runtime_behavior": False,
    "test_behavior": False, "scientific_truth": False,
    "external_primary_truth": False, "material_validity": False,
    "canonical_equation": False, "publication_readiness": False,
}


class ValidationFailure(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationFailure(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def _constant(token: str) -> None:
    raise ValidationFailure("E_JSON_NONFINITE", token)


def walk_json(value: Any, depth: int = 0) -> tuple[int, int]:
    require(depth <= 64, "E_JSON_DEPTH")
    if isinstance(value, dict):
        children = [walk_json(child, depth + 1) for child in value.values()]
    elif isinstance(value, list):
        require(len(value) <= 20000, "E_JSON_ARRAY")
        children = [walk_json(child, depth + 1) for child in value]
    else:
        require(value is None or isinstance(value, (str, int, float, bool)), "E_JSON_TYPE")
        if isinstance(value, float):
            require(math.isfinite(value), "E_JSON_NONFINITE")
        return 1, depth
    return 1 + sum(row[0] for row in children), max([depth, *(row[1] for row in children)])


def strict_load(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    require(len(raw) <= 100_000_000, "E_JSON_SIZE", label)
    require(raw == lf_bytes(raw) and raw.endswith(b"\n") and not raw.startswith(b"\xef\xbb\xbf"), "E_JSON_BYTES", label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationFailure("E_JSON_PARSE", label) from exc
    require(isinstance(value, dict), "E_JSON_ROOT", label)
    nodes, depth = walk_json(value)
    require(canonical_bytes(value) == raw, "E_JSON_CANONICAL", label)
    require(value.get("semantic_sha256") == semantic_hash(value), "E_JSON_SEMANTIC", label)
    return value, nodes, depth


def strict_input_load(raw: bytes, label: str) -> dict[str, Any]:
    require(raw == lf_bytes(raw) and raw.endswith(b"\n") and not raw.startswith(b"\xef\xbb\xbf"), "E_INPUT_JSON_BYTES", label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationFailure("E_INPUT_JSON_PARSE", label) from exc
    require(isinstance(value, dict), "E_INPUT_JSON_ROOT", label)
    walk_json(value)
    return value


def validate_git_argv(args: tuple[str, ...]) -> None:
    oid = r"[0-9a-f]{40}"
    shapes = [
        re.fullmatch(r"cat-file blob [0-9a-f]{40}", " ".join(args)),
        re.fullmatch(r"cat-file blob [0-9a-f]{40}:Codex/results/PHASE_067_PYTHON_(SOURCE_INVENTORY|FULL_READ_ATTESTATION)\.json", " ".join(args)),
        re.fullmatch(r"rev-parse (--abbrev-ref )?(HEAD|@\{upstream\}|origin/codex/anode-fit-v1025_2-canonical-completion|refs/remotes/origin/codex/anode-fit-v1025_2-canonical-completion|refs/remotes/origin/codex/lib-physics-endgame-v1025_2|refs/remotes/origin/main|[0-9a-f]{40}\^)", " ".join(args)),
        re.fullmatch(r"status --porcelain(=v1 --untracked-files=all)?", " ".join(args)),
        re.fullmatch(r"ls-files -s", " ".join(args)),
        re.fullmatch(r"ls-files --others --exclude-standard", " ".join(args)),
        re.fullmatch(r"diff --name-only", " ".join(args)),
        re.fullmatch(r"diff --cached --check", " ".join(args)),
        re.fullmatch(r"diff --cached --name-status --no-renames HEAD", " ".join(args)),
        re.fullmatch(r"diff --name-only [0-9a-f]{40} -- Claude", " ".join(args)),
        re.fullmatch(r"diff-tree --no-commit-id --name-status --no-renames -r [0-9a-f]{40}\^ [0-9a-f]{40}", " ".join(args)),
        re.fullmatch(r"ls-tree -r [0-9a-f]{40}", " ".join(args)),
        re.fullmatch(r"show -s --format=%(P|s) [0-9a-f]{40}", " ".join(args)),
        re.fullmatch(r"show :.+", " ".join(args)),
        re.fullmatch(r"show [0-9a-f]{40}:.+", " ".join(args)),
        re.fullmatch(r"show-ref --verify --hash refs/heads/(codex/lib-physics-endgame-v1025_2|main)", " ".join(args)),
        re.fullmatch(r"ls-remote --heads origin refs/heads/(codex/anode-fit-v1025_2-canonical-completion|codex/lib-physics-endgame-v1025_2|main)", " ".join(args)),
        re.fullmatch(r"ls-remote --get-url origin", " ".join(args)),
    ]
    require(any(shapes), "E_GIT_ARGV", repr(args))
    require(not any(token.startswith("-") and token in {"--output", "-D", "--delete"} for token in args), "E_GIT_WRITE_OPTION")


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    validate_git_argv(args)
    completed = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if check:
        require(completed.returncode == 0, "E_GIT", repr(args))
    elif completed.returncode != 0:
        require(args == ("show-ref", "--verify", "--hash", "refs/heads/main"), "E_GIT_OPTIONAL")
        return b"" if binary else ""
    require(completed.stderr == b"", "E_GIT_STDERR", repr(args))
    return completed.stdout if binary else completed.stdout.decode("utf-8").rstrip("\r\n")


def sorted_lines_sha(values: list[str]) -> str:
    return sha256("".join(value + "\n" for value in sorted(values)).encode("utf-8"))


def neutralized_source(raw: bytes, name: str) -> bytes:
    pattern = re.compile(rb'(?m)^' + re.escape(name.encode()) + rb' = "[0-9a-f]{64}"$')
    updated, count = pattern.subn(name.encode() + b' = "' + b"0" * 64 + b'"', lf_bytes(raw))
    require(count == 1, "E_SOURCE_POLICY_PIN", name)
    return updated


def assert_source_policy_hash(raw: bytes, name: str, expected: str, code: str) -> None:
    require(sha256(neutralized_source(raw, name)) == expected, code)


def verify_source_policy() -> None:
    builder = (ROOT / BUILDER_PATH).read_bytes()
    validator = (ROOT / VALIDATOR_PATH).read_bytes()
    assert_source_policy_hash(builder, "BUILDER_SOURCE_POLICY_SHA256_LF",
                              BUILDER_SOURCE_POLICY_SHA256_LF, "E_BUILDER_POLICY_HASH")
    assert_source_policy_hash(validator, "VALIDATOR_SOURCE_POLICY_SHA256_LF",
                              VALIDATOR_SOURCE_POLICY_SHA256_LF, "E_VALIDATOR_POLICY_HASH")
    for label, raw in (("builder", builder), ("validator", validator)):
        try:
            tree = ast.parse(lf_bytes(raw).decode("utf-8"))
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise ValidationFailure("E_SOURCE_PARSE", label) from exc
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        require(sum(isinstance(node.func, ast.Attribute) and node.func.attr == "run" and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" for node in calls) == 1, "E_SUBPROCESS_CARDINALITY", label)
        require(not any(isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"} for node in calls), "E_DYNAMIC_EXECUTION", label)


def assert_control_document_hash(raw: bytes, expected: str, path: str) -> None:
    require(sha256(raw) == expected, "E_CONTROL_HASH", path)


def verify_control_documents() -> None:
    for path, expected_hash in CONTROL_DOCUMENT_SHA256.items():
        raw = (ROOT / path).read_bytes()
        assert_control_document_hash(raw, expected_hash, path)
        text = raw.decode("utf-8")
        require("PASS_P067_STEP83_STATE_FLOW" in text, "E_CONTROL_GATE", path)
        require("PASS_P067_STEP83_PERSISTENCE" in text, "E_CONTROL_TERMINAL", path)
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    require(result.count("Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`") == 1, "E_RESULT_BOUNDARY")
    canonical = (ROOT / ACTIVE_LEDGER_PATH).read_text(encoding="utf-8")
    handover = (ROOT / HANDOVER_PATH).read_text(encoding="utf-8")
    require(canonical.count("| Phase 067 Step 83 |") == 1, "E_CANONICAL_STEP83_ROW")
    require(handover.count("| Phase 067 Step 83 |") == 1, "E_HANDOVER_STEP83_ROW")
    require(canonical.count("## Next Exact Step") == 1 and handover.count("## Exact Next Action") == 1, "E_NEXT_HEADING")
    require("Begin Step 84 only after both runtimes return `PASS_P067_STEP83_PERSISTENCE`" in canonical, "E_CANONICAL_NEXT")
    require("Begin Step 84 only after both runtimes return `PASS_P067_STEP83_PERSISTENCE`" in handover, "E_HANDOVER_NEXT")


def exact_keys(value: Any, expected: set[str], code: str) -> None:
    require(isinstance(value, dict) and set(value) == expected, code, repr(set(value) if isinstance(value, dict) else type(value)))


def anchor_nodes(tree: ast.Module) -> dict[tuple[int, int, str], list[ast.AST]]:
    result: dict[tuple[int, int, str], list[ast.AST]] = {}
    for node in ast.walk(tree):
        start = getattr(node, "lineno", None)
        end = getattr(node, "end_lineno", None)
        if start is not None and end is not None:
            key = (int(start), int(end), type(node).__name__)
            result.setdefault(key, []).append(node)
    return result


def stable_ast_bytes(node: ast.AST) -> bytes:
    def normalize(value: Any) -> Any:
        if isinstance(value, ast.AST):
            return {"_type": type(value).__name__,
                    "fields": [[field, normalize(getattr(value, field, None))]
                               for field in value._fields]}
        if isinstance(value, list):
            return [normalize(item) for item in value]
        if isinstance(value, tuple):
            return {"_tuple": [normalize(item) for item in value]}
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        return {"_literal_type": type(value).__name__, "repr": repr(value)}

    return json.dumps(normalize(node), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def qualified_owner(tree: ast.Module, node: ast.AST) -> str:
    candidates: list[tuple[int, str]] = []

    def visit(current: ast.AST, scope: list[str]) -> None:
        next_scope = scope
        if isinstance(current, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            next_scope = [*scope, current.name]
            if current.lineno <= getattr(node, "lineno", 0) and current.end_lineno >= getattr(node, "end_lineno", 0):
                candidates.append((current.end_lineno - current.lineno, ".".join(next_scope)))
        for child in ast.iter_child_nodes(current):
            visit(child, next_scope)

    visit(tree, [])
    require(bool(candidates), "E_ANCHOR_OWNER")
    return min(candidates)[1]


def validate_anchor(value: Any, tree: ast.Module, lines: list[str]) -> None:
    exact_keys(value, ANCHOR_KEYS, "E_ANCHOR_KEYS")
    key = (value["start_line"], value["end_line"], value["ast_kind"])
    candidates = anchor_nodes(tree).get(key, [])
    node = next((item for item in candidates if value["node_sha256"] == sha256(stable_ast_bytes(item)) and value["expression"] == ast.unparse(item)), None)
    require(node is not None, "E_ANCHOR_NODE", repr(key))
    text = "\n".join(lines[key[0] - 1:key[1]]) + "\n"
    require(value["source_sha256"] == sha256(text.encode("utf-8")), "E_ANCHOR_SOURCE")
    require(value["node_sha256"] == sha256(stable_ast_bytes(node)), "E_ANCHOR_AST")
    require(value["expression"] == ast.unparse(node), "E_ANCHOR_EXPRESSION")
    observed_owner = qualified_owner(tree, node)
    require(value["qualified_definition"] == observed_owner, "E_ANCHOR_QUALIFIED",
            f"stored={value['qualified_definition']} observed={observed_owner} lines={key[0]}-{key[1]} kind={key[2]}")


def anchors_in(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if set(value) == ANCHOR_KEYS:
            found.append(value)
        else:
            for child in value.values():
                found.extend(anchors_in(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(anchors_in(child))
    return found


def node_names(node: ast.AST) -> set[str]:
    found: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            found.add(child.id)
        elif isinstance(child, ast.Attribute):
            found.add(child.attr)
    return found


def node_targets(node: ast.AST) -> set[str]:
    found: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
            found.add(child.id)
        elif isinstance(child, ast.Attribute) and isinstance(child.ctx, ast.Store):
            found.add(child.attr)
    return found


def selected_class(tree: ast.Module, name: str) -> ast.ClassDef:
    rows = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name]
    require(len(rows) == 1, "E_ROLE_CLASS", name)
    return rows[0]


def selected_method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef:
    cls = selected_class(tree, class_name)
    rows = [node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == method_name]
    require(len(rows) == 1, "E_ROLE_METHOD", class_name + "." + method_name)
    return rows[0]


def selected_first(root: ast.AST, predicate: Any, code: str) -> ast.AST:
    rows = [node for node in ast.walk(root) if predicate(node)]
    require(bool(rows), code)
    return sorted(rows, key=lambda node: (getattr(node, "lineno", 0), getattr(node, "col_offset", 0)))[0]


def selected_last_return(function: ast.FunctionDef) -> ast.Return:
    rows = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
    require(bool(rows), "E_ROLE_RETURN")
    return sorted(rows, key=lambda node: (node.lineno, node.col_offset))[-1]


def observed_anchor(tree: ast.Module, node: ast.AST, lines: list[str]) -> dict[str, Any]:
    start = int(getattr(node, "lineno", 0))
    end = int(getattr(node, "end_lineno", start))
    require(start > 0 and end >= start, "E_ROLE_EXTENT")
    text = "\n".join(lines[start - 1:end]) + "\n"
    return {"qualified_definition": qualified_owner(tree, node),
            "ast_kind": type(node).__name__, "start_line": start, "end_line": end,
            "source_sha256": sha256(text.encode("utf-8")),
            "node_sha256": sha256(stable_ast_bytes(node)), "expression": ast.unparse(node)}


def independent_anchor_roles(tree: ast.Module, lines: list[str]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    init = selected_method(tree, "GraphiteAnodeDischargeDQDV", "__init__")
    curve = selected_method(tree, "GraphiteAnodeDischargeDQDV", "curve")
    dqdv = selected_method(tree, "GraphiteAnodeDischargeDQDV", "dqdv")
    equilibrium = selected_method(tree, "GraphiteAnodeDischargeDQDV", "equilibrium")
    lag = selected_method(tree, "GraphiteAnodeDischargeDQDV", "_resolve_lag_length")
    chi_method = selected_method(tree, "GraphiteAnodeDischargeDQDV", "_chi_d")
    v_n = selected_first(dqdv, lambda n: isinstance(n, ast.Assign) and "V_n" in node_targets(n) and {"V_in", "I_abs", "Rn"} <= node_names(n), "E_ROLE_VN")
    i_if = selected_first(curve, lambda n: isinstance(n, ast.If) and "I_abs" in node_names(n) and any(isinstance(x, ast.Is) for x in ast.walk(n)), "E_ROLE_I_BRANCH")
    i_mult = selected_first(i_if, lambda n: isinstance(n, ast.Assign) and "I_use" in node_targets(n) and "Q_cell" in node_names(n), "E_ROLE_I_MULT")
    i_override = selected_first(i_if, lambda n: isinstance(n, ast.Assign) and "I_use" in node_targets(n) and "I_abs" in node_names(n) and n is not i_mult, "E_ROLE_I_OVERRIDE")
    x_store = selected_first(init, lambda n: isinstance(n, ast.Assign) and "x" in node_targets(n) and "x" in node_names(n), "E_ROLE_X")
    chi_store = selected_first(init, lambda n: isinstance(n, ast.Assign) and "chi" in node_targets(n) and {"chi", "x"} <= node_names(n), "E_ROLE_CHI")
    chi_consumer = selected_first(chi_method, lambda n: isinstance(n, ast.Return) and "chi" in node_names(n), "E_ROLE_CHI_CONSUMER")
    t_input = selected_first(dqdv, lambda n: isinstance(n, ast.Assign) and "T_input" in node_targets(n) and "T" in node_names(n), "E_ROLE_T_INPUT")
    t_local = selected_first(dqdv, lambda n: isinstance(n, (ast.Assign, ast.AnnAssign)) and bool(node_targets(n) & {"T_work", "T_prog"}), "E_ROLE_T_LOCAL")
    t_rep = selected_first(dqdv, lambda n: isinstance(n, ast.Assign) and "T_rep" in node_targets(n), "E_ROLE_T_REP")
    lag_call = selected_first(dqdv, lambda n: isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "_resolve_lag_length", "E_ROLE_LAG_CALL")
    center_if = selected_first(dqdv, lambda n: isinstance(n, ast.If) and "dH_rxn" in ast.unparse(n.test) and "dS_rxn" in ast.unparse(n.test), "E_ROLE_CENTER_IF")
    center_thermo = selected_first(center_if, lambda n: isinstance(n, ast.Assign) and "U_j" in node_targets(n) and "func_U_j" in ast.unparse(n), "E_ROLE_CENTER_THERMO")
    center_literal = selected_first(center_if, lambda n: isinstance(n, ast.Assign) and "U_j" in node_targets(n) and "tr['U']" in ast.unparse(n), "E_ROLE_CENTER_LITERAL")
    branch_if = selected_first(dqdv, lambda n: isinstance(n, ast.If) and "gamma" in node_names(n) and "Omega" in node_names(n) and "center" in node_targets(n), "E_ROLE_BRANCH")
    branch_write = selected_first(branch_if, lambda n: isinstance(n, ast.Assign) and "center" in node_targets(n) and ("func_U_branch" in ast.unparse(n) or "hys_shift" in node_names(n)), "E_ROLE_BRANCH_WRITE")
    lco_sign_rows = [node for node in ast.walk(curve) if isinstance(node, ast.If) and "_delith_is_discharge" in node_names(node) and "sigma_d" in node_targets(node)]
    lco_sign = sorted(lco_sign_rows, key=lambda node: node.lineno)[0] if lco_sign_rows else None
    lco_class = selected_class(tree, "LCOCathodeDQDV")
    lco_center = selected_first(lco_class, lambda n: isinstance(n, ast.Call) and "x_center" in ast.unparse(n) and "x_MIT" in ast.unparse(n), "E_ROLE_LCO_CENTER")
    qj_use = selected_first(dqdv, lambda n: isinstance(n, ast.BinOp) and "tr['Q']" in ast.unparse(n), "E_ROLE_QJ")
    optional = {node.name: node for node in selected_class(tree, "GraphiteAnodeDischargeDQDV").body if isinstance(node, ast.FunctionDef)}
    role_nodes: dict[str, ast.AST | None] = {
        "init": init, "curve": curve, "dqdv": dqdv, "equilibrium": equilibrium,
        "lag": lag, "v_n": v_n, "i_branch": i_if, "i_mult": i_mult,
        "i_override": i_override, "x_store": x_store, "chi_store": chi_store,
        "chi_consumer": chi_consumer, "t_input": t_input, "t_local": t_local,
        "t_rep": t_rep, "lag_call": lag_call, "center_if": center_if,
        "center_thermo": center_thermo, "center_literal": center_literal,
        "branch_write": branch_write, "lco_sign_if": lco_sign,
        "lco_center": lco_center, "qj_use": qj_use,
        "solve_u_oc": optional.get("solve_U_oc"), "vib_theta": optional.get("_vib_theta"),
        "curve_return": selected_last_return(curve), "dqdv_return": selected_last_return(dqdv),
        "lco_class": lco_class,
    }
    roles = {name: (observed_anchor(tree, node, lines) if node is not None else None)
             for name, node in role_nodes.items()}
    try:
        blend_class = selected_class(tree, "BlendedAnodeDQDV")
    except ValidationFailure:
        return roles, None
    blend_init = selected_method(tree, "BlendedAnodeDQDV", "__init__")
    from_wt = selected_method(tree, "BlendedAnodeDQDV", "from_wt")
    blend_dqdv = selected_method(tree, "BlendedAnodeDQDV", "dqdv")
    blend_nodes = {
        "class": blend_class, "init": blend_init, "from_wt": from_wt, "dqdv": blend_dqdv,
        "f_store": selected_first(blend_init, lambda n: isinstance(n, ast.Assign) and "f_Si" in node_targets(n) and "f_Si" in node_names(n), "E_ROLE_FSI"),
        "q_si": selected_first(blend_init, lambda n: isinstance(n, (ast.Assign, ast.AnnAssign)) and "Q_Si" in node_targets(n), "E_ROLE_QSI"),
        "q_total": selected_first(blend_init, lambda n: isinstance(n, (ast.Assign, ast.AnnAssign)) and "Q" in node_targets(n) and {"Q_gr", "Q_Si"} <= node_names(n), "E_ROLE_QTOTAL"),
        "f_convert": selected_first(from_wt, lambda n: isinstance(n, ast.Assign) and "f_Si" in node_targets(n) and {"num", "q_gr"} <= node_names(n), "E_ROLE_FCONVERT"),
        "dqdv_return": selected_last_return(blend_dqdv),
    }
    return roles, {name: observed_anchor(tree, node, lines) for name, node in blend_nodes.items()}


def expected_route_contract(quantity: str, source: dict[str, Any]) -> tuple[list[str], list[str]]:
    has_blend = source["has_blend"]
    features = source["feature_flags"]
    classes = {
        "voltage": ["DIRECT", "DIRECT", "IGNORED", "FALLBACK", "OVERWRITTEN", "DIRECT"] + (["OVERWRITTEN"] if features["lco_curve_facade_sign_flip"] else []) + ["INHERITED"],
        "current": ["OVERWRITTEN", "FALLBACK", "IGNORED"],
        "capacity": ["DIRECT", "DIRECT"] + (["DIRECT"] if has_blend else []),
        "composition": ["FALLBACK", "DIRECT", "IGNORED", "DIRECT", "DIRECT"] + (["DIRECT"] if features["global_composition_solver"] else []) + (["DIRECT", "DIRECT"] if has_blend else []),
        "temperature": ["DIRECT", "DIRECT"] + (["DIRECT"] if features["vibrational_temperature"] else []) + (["DIRECT"] if features["global_composition_solver"] else []),
    }[quantity]
    conditions = {
        "voltage": ["ALWAYS", "transition_HAS_dH_rxn_AND_dS_rxn", "transition_HAS_dH_rxn_AND_dS_rxn", "transition_LACKS_dH_rxn_OR_dS_rxn", "gamma_NONZERO_AND_Omega_POSITIVE", "DIRECT_V_n_EQUILIBRIUM_API"] + (["LCO_curve_FACADE"] if features["lco_curve_facade_sign_flip"] else []) + ["INSTANCE_IS_LCOCathodeDQDV"],
        "current": ["I_abs_IS_NOT_NONE", "I_abs_IS_NONE", "I_abs_IS_NOT_NONE"],
        "capacity": ["ALWAYS", "EACH_TRANSITION"] + (["BLENDED_MODEL"] if has_blend else []),
        "composition": ["chi_IS_NONE", "chi_IS_NOT_NONE", "chi_IS_NOT_NONE", "LCO_COMPOSITION_CENTER_PATH", "LOCAL_TRANSITION_OCCUPANCY"] + (["solve_U_oc_ENTRY"] if features["global_composition_solver"] else []) + (["CONSTRUCTOR_f_Si", "from_wt_ENTRY"] if has_blend else []),
        "temperature": ["T_IS_SCALAR_OR_SINGLETON", "T_IS_PER_POINT_ARRAY"] + (["TRANSITION_HAS_VIBRATIONAL_TEMPERATURE_KEYS"] if features["vibrational_temperature"] else []) + (["solve_U_oc_ENTRY"] if features["global_composition_solver"] else []),
    }[quantity]
    return classes, conditions


def expected_identity_contract(quantity: str, source: dict[str, Any]) -> list[tuple[str, str, str, str, str, str, str]]:
    features = source["feature_flags"]
    explicit_c = features["comment_only_seconds_conversion"]
    explicit_m_ah = features["transition_capacity_unit_mAh_explicit"]
    base: dict[str, list[tuple[str, str, str, str, str, str, str]]] = {
        "voltage": [
            ("V_app", "V", "APPLIED_ELECTRODE_OR_CELL_LABEL_NOT_INFERRED", "SIGNED_BY_AXIS", "PUBLIC_INPUT", "PRESENT", "SOURCE_EXPLICIT"),
            ("V_n", "V", "INTERNAL_POLARIZED_ELECTRODE_COORDINATE", "V_app - sigma_d*I_abs*Rn", "LOCAL_PER_POINT", "PRESENT", "SOURCE_EXPLICIT"),
            ("center/U_j", "V", "EQUILIBRIUM_OR_BRANCH_CENTER", "sigma_d_BRANCH_WHEN_ENABLED", "LOCAL_PER_TRANSITION", "PRESENT", "SOURCE_EXPLICIT"),
            ("direction -> sigma_d", "1", "CELL_LABEL_FACADE_SIGN", "LCO_LABEL_FLIP_WHEN_delith_IS_NOT_discharge", "CURVE_API_ONLY", "PRESENT" if features["lco_curve_facade_sign_flip"] else "ABSENT_IN_FROZEN_SOURCE", "SOURCE_EXPLICIT" if features["lco_curve_facade_sign_flip"] else "STATIC_INFERRED_AMBIGUOUS"),
            ("s -> sigma_d", "1", "LOW_LEVEL_DIRECTION_SLOT", "s>=0:+1_ELSE:-1_WITHOUT_LCO_LABEL_FLIP", "DQDV_API_ONLY", "PRESENT", "SOURCE_EXPLICIT"),
        ],
        "current": [
            ("I_abs", "SOURCE_UNIT_NOT_EXPLICIT", "ABSOLUTE_CURRENT_MAGNITUDE", "NONNEGATIVE_MAGNITUDE_WITH_sigma_d_SEPARATE", "PUBLIC_INPUT", "PRESENT", "STATIC_INFERRED_AMBIGUOUS"),
            ("c_rate", "h^-1", "C_RATE", "NONNEGATIVE", "PUBLIC_INPUT", "PRESENT", "COMMENT_ONLY"),
            ("I_abs/Q_cell/3600", "s^-1", "NORMALIZED_RATE", "NONNEGATIVE", "CALCULATION", "ABSENT_IN_FROZEN_SOURCE", "STATIC_INFERRED_AMBIGUOUS"),
        ],
        "capacity": [
            ("Q_cell", "Ah_CONVENTION_NOT_SOURCE_EXPLICIT", "CELL_TOTAL_CAPACITY", "POSITIVE", "GLOBAL_CALL", "GROUND_NOT_FOUND_STATIC_AMBIGUOUS", "STATIC_INFERRED_AMBIGUOUS"),
            ("Q_cell", "C", "CELL_TOTAL_CHARGE", "POSITIVE", "GLOBAL_CALL", "PRESENT" if explicit_c else "GROUND_NOT_FOUND_STATIC_AMBIGUOUS", "COMMENT_ONLY" if explicit_c else "STATIC_INFERRED_AMBIGUOUS"),
            ("transition['Q']", "mAh" if explicit_m_ah else "SOURCE_UNIT_NOT_EXPLICIT", "COMPONENT_CAPACITY", "POSITIVE_EXPECTED", "LOCAL_PER_TRANSITION", "PRESENT", "COMMENT_ONLY" if explicit_m_ah else "STATIC_INFERRED_AMBIGUOUS"),
        ],
        "composition": [
            ("x", "1", "GRAPHITE_GLOBAL_COMPOSITION_PARAMETER", "UNSIGNED_FRACTION", "GLOBAL_MODEL", "PRESENT", "SOURCE_EXPLICIT"),
            ("chi/self.chi", "1", "DIRECTIONAL_SPLIT_COMPOSITION_PARAMETER", "UNSIGNED_FRACTION", "GLOBAL_MODEL", "PRESENT", "SOURCE_EXPLICIT"),
            ("ksi_eq", "1", "REPRESENTATIVE_OR_LOCAL_TRANSITION_OCCUPANCY", "DIRECTION_COORDINATE_DEPENDENT", "LOCAL_PER_TRANSITION_POINT", "PRESENT", "SOURCE_EXPLICIT"),
            ("x_bar", "1", "TOTAL_CAPACITY_NORMALIZED_COMPOSITION", "UNSIGNED_FRACTION", "GLOBAL_PUBLIC_INPUT", "PRESENT" if features["global_composition_solver"] else "ABSENT_IN_FROZEN_SOURCE", "SOURCE_EXPLICIT" if features["global_composition_solver"] else "STATIC_INFERRED_AMBIGUOUS"),
            ("x_center/x_MIT", "1", "LCO_GLOBAL_COMPOSITION_CENTERS", "UNSIGNED_FRACTION", "GLOBAL_LCO_MODEL", "PRESENT", "SOURCE_EXPLICIT"),
        ],
        "temperature": [
            ("T", "K", "PUBLIC_TEMPERATURE", "POSITIVE", "GLOBAL_SCALAR_OR_PER_POINT_INPUT", "PRESENT", "SOURCE_EXPLICIT"),
            ("T_prog" if features["temperature_route"] == "POINTWISE_ORDERED_T_PROG" else "T_work", "K", "INTERPOLATED_OR_ORDERED_TEMPERATURE", "POSITIVE", "LOCAL_PER_VOLTAGE_POINT", "PRESENT", "SOURCE_EXPLICIT"),
            ("T_rep", "K", "ARITHMETIC_MEAN_REPRESENTATIVE_TEMPERATURE", "POSITIVE", "REPRESENTATIVE_PER_CALL", "PRESENT", "SOURCE_EXPLICIT"),
            ("theta/vibrational temperature", "K", "TRANSITION_VIBRATIONAL_TEMPERATURE", "POSITIVE_EXPECTED", "LOCAL_PER_TRANSITION", "PRESENT" if features["vibrational_temperature"] else "ABSENT_IN_FROZEN_SOURCE", "SOURCE_EXPLICIT" if features["vibrational_temperature"] else "STATIC_INFERRED_AMBIGUOUS"),
            ("T in solve_U_oc(x_bar,T)", "K", "THERMODYNAMIC_COMPOSITION_ROUTE_TEMPERATURE", "POSITIVE", "GLOBAL_SCALAR", "PRESENT" if features["global_composition_solver"] else "ABSENT_IN_FROZEN_SOURCE", "SOURCE_EXPLICIT" if features["global_composition_solver"] else "STATIC_INFERRED_AMBIGUOUS"),
        ],
    }
    rows = list(base[quantity])
    if quantity == "capacity" and source["has_blend"]:
        rows += [("Q_Si", "SOURCE_DECLARED_CAPACITY_UNIT", "SI_COMPONENT_CAPACITY", "NONNEGATIVE", "GLOBAL_BLEND", "PRESENT", "SOURCE_EXPLICIT"),
                 ("Q", "SOURCE_DECLARED_CAPACITY_UNIT", "BLEND_TOTAL_Q_gr_PLUS_Q_Si", "POSITIVE", "GLOBAL_BLEND_DENOMINATOR", "PRESENT", "SOURCE_EXPLICIT")]
    if quantity == "composition" and source["has_blend"]:
        rows += [("m_Si", "1", "MASS_FRACTION", "UNSIGNED_FRACTION", "GLOBAL_BLEND_INPUT", "PRESENT", "SOURCE_EXPLICIT"),
                 ("f_Si", "1", "CAPACITY_FRACTION_Q_Si_OVER_Q_TOTAL", "UNSIGNED_FRACTION", "GLOBAL_BLEND_STATE", "PRESENT", "SOURCE_EXPLICIT")]
    return rows


def expected_route_projection(quantity: str, source: dict[str, Any]) -> list[tuple[str, list[str], list[str]]]:
    features = source["feature_flags"]
    rows: dict[str, list[tuple[str, list[str], list[str]]]] = {
        "voltage": [
            ("ALWAYS", ["V_app"], ["V_n = V_app - sigma_d * I_abs * Rn"]),
            ("transition_HAS_dH_rxn_AND_dS_rxn", ["dH_rxn", "dS_rxn"], ["thermochemical center through func_U_j"]),
            ("transition_HAS_dH_rxn_AND_dS_rxn", ["transition['U']"], []),
            ("transition_LACKS_dH_rxn_OR_dS_rxn", ["dH_rxn_OR_dS_rxn_ABSENT_SELECTOR", "transition['U']"], ["literal transition center fallback"]),
            ("gamma_NONZERO_AND_Omega_POSITIVE", ["U_j", "gamma", "Omega", "sigma_d"], ["branch-center write from equilibrium/literal U_j"]),
            ("DIRECT_V_n_EQUILIBRIUM_API", ["V_n"], []),
        ] + ([('LCO_curve_FACADE', ["direction", "sigma_d"], ["facade-only LCO sign flip"])] if features["lco_curve_facade_sign_flip"] else []) + [
            ("INSTANCE_IS_LCOCathodeDQDV", ["V_app"], []),
        ],
        "current": [
            ("I_abs_IS_NOT_NONE", ["I_abs"], ["validated explicit current override"]),
            ("I_abs_IS_NONE", ["I_abs_SELECTOR", "c_rate", "Q_cell"], ["I_use = c_rate * Q_cell"]),
            ("I_abs_IS_NOT_NONE", ["c_rate"], []),
        ],
        "capacity": [
            ("ALWAYS", ["Q_cell"], ["Q_cell is passed to the lag-length resolver; denominator semantics are bounded by its source anchor"]),
            ("EACH_TRANSITION", ["transition['Q']"], ["component capacity multiplies the transition peak shape"]),
        ] + ([('BLENDED_MODEL', ["f_Si"], ["component scaling then total capacity"])] if source["has_blend"] else []),
        "composition": [
            ("chi_IS_NONE", ["chi_SELECTOR", "x"], ["x supplies chi only when explicit chi is absent"]),
            ("chi_IS_NOT_NONE", ["chi"], ["explicit chi supplies self.chi"]),
            ("chi_IS_NOT_NONE", ["x_AS_CHI_FALLBACK"], []),
            ("LCO_COMPOSITION_CENTER_PATH", ["x_center", "x_MIT"], []),
            ("LOCAL_TRANSITION_OCCUPANCY", ["V_n", "T", "center", "n_j", "sigma_d"], ["local transition occupancy evaluation"]),
        ] + ([('solve_U_oc_ENTRY', ["x_bar", "T"], [])] if features["global_composition_solver"] else []) + ([
            ("CONSTRUCTOR_f_Si", ["f_Si"], ["validated capacity fraction storage"]),
            ("from_wt_ENTRY", ["m_Si", "q_Si", "q_gr"], ["m*q_Si / (m*q_Si + (1-m)*q_gr)"]),
        ] if source["has_blend"] else []),
        "temperature": [
            ("T_IS_SCALAR_OR_SINGLETON", ["T"], ["array coercion and positivity validation", "scalar broadcast", "arithmetic mean"]),
            ("T_IS_PER_POINT_ARRAY", ["T"], ["array coercion and positivity validation", "voltage-ordering or interpolation", "arithmetic mean"]),
        ] + ([('TRANSITION_HAS_VIBRATIONAL_TEMPERATURE_KEYS', ["theta_D", "theta_E"], [])] if features["vibrational_temperature"] else []) + ([
            ("solve_U_oc_ENTRY", ["T", "x_bar"], []),
        ] if features["global_composition_solver"] else []),
    }
    return rows[quantity]


def validate_semantic_roles(flow: dict[str, Any], source: dict[str, Any],
                            roles: dict[str, Any], blend: dict[str, Any] | None) -> None:
    quantity = flow["quantity"]
    features = source["feature_flags"]
    has_blend = source["has_blend"]
    prefix = flow["flow_id"]

    def rid(index: int) -> str:
        return prefix + f"-R{index}"

    identity_evidence: dict[str, list[Any]] = {
        "voltage": [roles["curve"], roles["v_n"], roles["dqdv"], roles["lco_sign_if"], roles["dqdv"]],
        "current": [roles["curve"], roles["curve"], None],
        "capacity": [roles["curve"], roles["lag"] if features["comment_only_seconds_conversion"] else roles["curve"], roles["dqdv"]]
                    + ([blend["q_si"], blend["q_total"]] if has_blend and blend is not None else []),
        "composition": [roles["x_store"], roles["chi_store"], roles["dqdv"], roles["solve_u_oc"], roles["lco_center"]]
                       + ([blend["from_wt"], blend["f_store"]] if has_blend and blend is not None else []),
        "temperature": [roles["dqdv"], roles["t_local"], roles["t_rep"], roles["vib_theta"], roles["solve_u_oc"]],
    }
    refs: dict[str, list[list[str]]] = {
        "voltage": [[rid(1)], [rid(1), rid(6)], [rid(2), rid(4), rid(5)],
                    ([rid(7)] if features["lco_curve_facade_sign_flip"] else []), [rid(1)]],
        "current": [[rid(1), rid(2)], [rid(2), rid(3)], []],
        "capacity": [[], ([rid(1)] if features["comment_only_seconds_conversion"] else []), [rid(2)]]
                    + ([[rid(3)], [rid(3)]] if has_blend else []),
        "composition": [[rid(1), rid(3)], [rid(1), rid(2)], [rid(5)],
                        ([rid(6)] if features["global_composition_solver"] else []), [rid(4)]],
        "temperature": [[rid(1), rid(2)], [rid(1), rid(2)], [rid(1), rid(2)],
                        ([rid(3)] if features["vibrational_temperature"] else []),
                        ([rid(4 if features["vibrational_temperature"] else 3)]
                         if features["global_composition_solver"] else [])],
    }
    if quantity == "composition" and has_blend:
        constructor = 6 + int(features["global_composition_solver"])
        refs["composition"] += [[rid(constructor + 1)], [rid(constructor), rid(constructor + 1)]]
    require([row["evidence"] for row in flow["state_identities"]] == identity_evidence[quantity],
            "E_IDENTITY_EVIDENCE_ROLE", flow["release"] + ":" + quantity)
    require([row["route_refs"] for row in flow["state_identities"]] == refs[quantity],
            "E_IDENTITY_ROUTE_REFS", flow["release"] + ":" + quantity)

    def role(producer: Any, transforms: list[tuple[list[str], list[str], Any]],
             consumers: list[Any], output: Any, alternate: Any = None) -> dict[str, Any]:
        return {"producer": producer, "transforms": transforms, "consumers": consumers,
                "output": output, "alternate": alternate}

    expected: dict[str, list[dict[str, Any]]] = {
        "voltage": [
            role(roles["curve"], [(["V_app", "sigma_d", "I_abs", "Rn"], ["V_n"], roles["v_n"])], [roles["dqdv"]], roles["dqdv_return"]),
            role(roles["center_if"], [(["T", "dH_rxn", "dS_rxn"], ["U_j"], roles["center_thermo"])], [roles["dqdv"]], roles["dqdv_return"]),
            role(roles["center_if"], [], [], None),
            role(roles["center_if"], [(["transition['U']"], ["U_j"], roles["center_literal"])], [roles["dqdv"]], roles["dqdv_return"], roles["center_literal"]),
            role(roles["center_if"], [(["U_j", "gamma", "Omega", "sigma_d"], ["center"], roles["branch_write"])], [roles["dqdv"]], roles["dqdv_return"]),
            role(roles["equilibrium"], [], [roles["equilibrium"]], roles["equilibrium"]),
        ] + ([role(roles["curve"], [(["cell direction label", "sigma_d"], ["LCO physical sigma_d"], roles["lco_sign_if"])], [roles["dqdv"]], roles["dqdv_return"])]
             if features["lco_curve_facade_sign_flip"] else []) + [
            role(roles["lco_class"], [], [roles["curve"]], roles["dqdv_return"]),
        ],
        "current": [
            role(roles["curve"], [(["I_abs"], ["I_use"], roles["i_override"])], [roles["dqdv"]], roles["dqdv_return"]),
            role(roles["curve"], [(["c_rate", "Q_cell"], ["I_use"], roles["i_mult"])], [roles["dqdv"]], roles["dqdv_return"], roles["i_mult"]),
            role(roles["curve"], [], [], None),
        ],
        "capacity": [
            role(roles["curve"], [(["Q_cell", "I_abs", "T"], ["lag_len_V"], roles["lag_call"])], [roles["lag"]], roles["dqdv_return"]),
            role(roles["qj_use"], [(["transition['Q']", "peak_shape"], ["dQ/dV contribution"], roles["qj_use"])], [roles["dqdv"]], roles["dqdv_return"]),
        ] + ([role(blend["init"], [(["f_Si", "Q_gr0", "Q_si0"], ["Q_Si", "Q"], blend["q_total"])], [blend["dqdv"]], blend["dqdv_return"])]
             if has_blend and blend is not None else []),
        "composition": [
            role(roles["chi_store"], [(["x"], ["self.chi"], roles["chi_store"])], [roles["chi_consumer"]], roles["chi_consumer"], roles["x_store"]),
            role(roles["chi_store"], [(["chi"], ["self.chi"], roles["chi_store"])], [roles["chi_consumer"]], roles["chi_consumer"]),
            role(roles["x_store"], [], [], None),
            role(roles["lco_center"], [], [roles["lco_class"]], roles["lco_class"]),
            role(roles["dqdv"], [(["V_n", "T", "center", "n_j", "sigma_d"], ["ksi_eq"], roles["dqdv"])], [roles["dqdv"]], roles["dqdv_return"]),
        ] + ([role(roles["solve_u_oc"], [], [roles["solve_u_oc"]], roles["solve_u_oc"])]
             if features["global_composition_solver"] else []) + ([
            role(blend["init"], [(["f_Si"], ["self.f_Si"], blend["f_store"])], [blend["dqdv"]], blend["dqdv_return"]),
            role(blend["from_wt"], [(["m_Si", "q_Si", "q_gr"], ["f_Si"], blend["f_convert"])], [blend["init"]], blend["dqdv_return"]),
        ] if has_blend and blend is not None else []),
        "temperature": [
            role(roles["dqdv"], [(["T"], ["T_input"], roles["t_input"]), (["T_input"], ["T_prog" if source["feature_flags"]["temperature_route"] == "POINTWISE_ORDERED_T_PROG" else "T_work"], roles["t_local"]), (["T_prog" if source["feature_flags"]["temperature_route"] == "POINTWISE_ORDERED_T_PROG" else "T_work"], ["T_rep"], roles["t_rep"])], [roles["lag_call"]], roles["dqdv_return"]),
            role(roles["dqdv"], [(["T"], ["T_input"], roles["t_input"]), (["T_input", "V_n"], ["T_prog" if source["feature_flags"]["temperature_route"] == "POINTWISE_ORDERED_T_PROG" else "T_work"], roles["t_local"]), (["T_prog" if source["feature_flags"]["temperature_route"] == "POINTWISE_ORDERED_T_PROG" else "T_work"], ["T_rep"], roles["t_rep"])], [roles["lag_call"]], roles["dqdv_return"]),
        ] + ([role(roles["vib_theta"], [], [roles["dqdv"]], roles["dqdv_return"])]
             if features["vibrational_temperature"] else []) + ([role(roles["solve_u_oc"], [], [roles["solve_u_oc"]], roles["solve_u_oc"])]
             if features["global_composition_solver"] else []),
    }
    actual = []
    for route_row in flow["routes"]:
        actual.append(role(route_row["producer"],
                           [(row["state_in"], row["state_out"], row["evidence"])
                            for row in route_row["ordered_transforms"]],
                           route_row["consumers"], route_row["output"], route_row["alternate_producer"]))
    require(actual == expected[quantity], "E_ROUTE_ANCHOR_ROLES", flow["release"] + ":" + quantity)


def artifact_errors(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    def check(condition: bool, name: str) -> None:
        if not condition:
            errors.append(name)
    try:
        exact_keys(matrix, TOP_KEYS, "E_TOP_KEYS")
        check(matrix["schema_version"] == "phase067-step83-state-flow-v1", "schema")
        check(matrix["artifact"] == "PHASE_067_STATE_QUANTITY_FLOW_MATRIX", "artifact")
        check((matrix["phase"], matrix["step"], matrix["generated_date"]) == (67, 83, GENERATED_DATE), "phase")
        check(matrix["baseline_commit"] == BASELINE and matrix["expected_parent"] == EXPECTED_PARENT, "commits")
        check(matrix["branch"] == BRANCH and matrix["expected_subject"] == EXPECTED_SUBJECT, "branch_subject")
        check(matrix["gate"] == GATE and matrix["persistence_terminal"] == PERSISTENCE, "gate")
        check(matrix["precommit_status"] == "PASS_PENDING_PERSISTENCE" and matrix["containing_commit"] == "PENDING_AT_PRECOMMIT_BY_DESIGN", "precommit")
        check(matrix["result_first"] is True and matrix["json_outputs_last"] is True, "ordering")
        exact_keys(matrix["inputs"], INPUT_KEYS, "E_INPUT_KEYS")
        for row in matrix["inputs"].values(): exact_keys(row, INPUT_RECORD_KEYS, "E_INPUT_RECORD_KEYS")
        check(matrix["inputs"] == {
            "step82_inventory": {"path": INVENTORY_PATH, "raw_sha256": INVENTORY_RAW_SHA256, "semantic_sha256": INVENTORY_SEMANTIC_SHA256},
            "step82_full_read_attestation": {"path": ATTESTATION_PATH, "raw_sha256": ATTESTATION_RAW_SHA256, "semantic_sha256": ATTESTATION_SEMANTIC_SHA256},
        }, "inputs")
        universe = matrix["universe"]
        check(universe == {
            "all_occurrences": 129, "all_unique_blobs": 84, "all_unique_blob_physical_lines": 29952,
            "releases": 20, "role_occurrence_counts": {"code": 20, "demo": 30, "result": 35, "test": 44},
            "role_unique_blob_counts": {"code": 15, "demo": 26, "result": 14, "test": 29},
            "flow_target_role": "code", "flow_target_occurrences": 20, "flow_target_unique_blobs": 15,
            "flow_target_unique_blob_physical_lines": 18529, "flow_target_occurrence_physical_lines": 24891,
            "losslessly_excluded_nonproduction_occurrences": 109, "code_path_sha256": CODE_PATH_SHA256,
            "code_path_blob_sha256": CODE_PATH_BLOB_SHA256, "code_blob_sha256": CODE_BLOB_SHA256,
            "code_release_path_sha256": CODE_RELEASE_PATH_SHA256,
            "code_release_path_blob_ordinal_sha256": CODE_OCCURRENCE_SHA256,
        }, "universe")
        check(matrix["quantity_contract"] == {
            "release_sequence": RELEASES, "quantity_sequence": QUANTITIES,
            "presence_enum": PRESENCE, "classification_enum": CLASSIFICATIONS,
            "required_release_quantity_rows": 100,
            "ordered_transform_authority": "STATIC_LEXICAL_ONLY_NOT_RUNTIME_CALL_ORDER",
            "downstream_owners": {"actual_call_order": "STEP84_CALL_SURFACE",
                                  "default_runtime_behavior": "STEP85_TEST_SURFACE",
                                  "unit_conversion": "STEP87_UNIT_NUMERICAL_AUDIT",
                                  "fallback_impact": "STEP88_BOUNDARY_INTERACTION"},
            "family_presence_axis": "release_quantity_coverage_distinct_from_nested_identity_source_status",
        }, "quantity_contract")
        check(matrix["authority"] == AUTHORITY_EXPECTED, "authority")
        sources = matrix["source_records"]
        flows = matrix["flow_records"]
        check(isinstance(sources, list) and len(sources) == 20, "sources")
        check(isinstance(flows, list) and len(flows) == 100, "flows")
        source_map: dict[str, dict[str, Any]] = {}
        for index, row in enumerate(sources, 1):
            exact_keys(row, SOURCE_KEYS, "E_SOURCE_KEYS")
            check(row["release_ordinal"] == index and row["release"] == RELEASES[index - 1], "source_order")
            check(row["ast_parse"] == "PASS" and row["quantity_coverage"] == QUANTITIES, "source_coverage")
            exact_keys(row["feature_flags"], FEATURE_KEYS, "E_FEATURE_KEYS")
            source_map[row["release"]] = row
        check(len(source_map) == 20, "source_unique")
        pair_set: set[tuple[str, str]] = set()
        for index, row in enumerate(flows, 1):
            exact_keys(row, FLOW_KEYS, "E_FLOW_KEYS")
            release = RELEASES[(index - 1) // 5]
            quantity = QUANTITIES[(index - 1) % 5]
            check((row["release"], row["quantity"], row["release_ordinal"]) == (release, quantity, RELEASES.index(release) + 1), "flow_order")
            check(row["flow_id"] == f"P067-S83-{index:03d}-{quantity.upper()}", "flow_id")
            check(row["presence"] == "PRESENT" and row["authority"] == "STATIC_SOURCE_ORDER_AND_CONNECTIVITY_ONLY", "flow_authority")
            exact_keys(row["occurrence"], OCCURRENCE_KEYS, "E_OCCURRENCE_KEYS")
            source = source_map[release]
            check(row["occurrence"] == {key: source[key] for key in OCCURRENCE_KEYS}, "occurrence_projection")
            pair_set.add((release, quantity))
            identities = row["state_identities"]
            expected_identity_count = {"voltage": 5, "current": 3, "capacity": 3 + 2 * source["has_blend"], "composition": 5 + 2 * source["has_blend"], "temperature": 5}[quantity]
            check(isinstance(identities, list) and len(identities) == expected_identity_count, "identity_count")
            for identity in identities:
                exact_keys(identity, IDENTITY_KEYS, "E_IDENTITY_KEYS")
                check(identity["source_status"] in PRESENCE, "identity_status")
                check(identity["evidence_status"] in {"SOURCE_EXPLICIT", "COMMENT_ONLY", "STATIC_INFERRED_AMBIGUOUS"}, "identity_evidence_status")
                check(all(isinstance(identity[key], str) and identity[key] for key in ("identity_id", "symbol", "unit", "basis", "sign", "scope")), "identity_fields")
            actual_identity_projection = [(item["symbol"], item["unit"], item["basis"], item["sign"], item["scope"], item["source_status"], item["evidence_status"]) for item in identities]
            check(actual_identity_projection == expected_identity_contract(quantity, source), "identity_projection")
            classes, conditions = expected_route_contract(quantity, source)
            routes = row["routes"]
            check([route["classification"] for route in routes] == classes, "route_classes")
            check([route["condition"] for route in routes] == conditions, "route_conditions")
            check([(route["condition"], route["public_inputs"], [item["operation"] for item in route["ordered_transforms"]]) for route in routes] == expected_route_projection(quantity, source), "route_projection")
            for route_index, route_row in enumerate(routes, 1):
                exact_keys(route_row, ROUTE_KEYS, "E_ROUTE_KEYS")
                check(route_row["route_id"] == row["flow_id"] + f"-R{route_index}", "route_id")
                check(route_row["classification"] in CLASSIFICATIONS, "route_class")
                check(not (route_row["classification"] == "IGNORED" and route_row["consumers"]), "ignored_consumer")
                check(not (route_row["classification"] == "IGNORED" and route_row["output"] is not None), "ignored_output")
                check(not (route_row["classification"] == "FALLBACK" and (route_row["condition"] == "ALWAYS" or route_row["producer"] is None or route_row["alternate_producer"] is None)), "fallback")
                check(not (route_row["classification"] == "OVERWRITTEN" and not route_row["ordered_transforms"]), "overwritten")
                check(not (route_row["classification"] == "INHERITED" and (route_row["producer"] is None or "LCOCathodeDQDV" not in route_row["producer"]["qualified_definition"])), "inherited")
                for transform_index, transform in enumerate(route_row["ordered_transforms"], 1):
                    exact_keys(transform, TRANSFORM_KEYS, "E_TRANSFORM_KEYS")
                    check(transform["ordinal"] == transform_index and transform["order_authority"] == "STATIC_LEXICAL_ONLY_NOT_RUNTIME_CALL_ORDER", "transform_order")
            route_ids = {item["route_id"] for item in routes}
            for identity in identities:
                check(isinstance(identity["route_refs"], list) and len(identity["route_refs"]) == len(set(identity["route_refs"])), "identity_route_refs")
                check(set(identity["route_refs"]) <= route_ids, "identity_route_unknown")
                check((identity["source_status"] == "PRESENT" and bool(identity["route_refs"]) and identity["evidence"] is not None) or
                      (identity["source_status"] != "PRESENT" and not identity["route_refs"]), "present_identity_route_resolution")
            for gap in row["gaps"]: exact_keys(gap, GAP_KEYS, "E_GAP_KEYS")
            expected_gaps: list[dict[str, str]] = []
            if quantity == "current":
                expected_gaps.append({"gap": "NO_EXECUTABLE_DIVIDE_BY_3600", "owner": "STEP87_UNIT_NUMERICAL_AUDIT"})
            if quantity == "composition" and not source["feature_flags"]["global_composition_solver"]:
                expected_gaps.append({"gap": "GLOBAL_COMPOSITION_TO_PUBLIC_OUTPUT_GROUND_NOT_FOUND", "owner": "P067-CODE-HISTORY"})
            if quantity == "composition" and release == "v1.0.25.2":
                expected_gaps.append({"gap": "EXECUTABLE_DEFAULT_PROFILE_CONFLICT_WITH_HEADER_OR_GUIDE", "owner": "STEP85_TEST_DEFAULT_BEHAVIOR"})
            check(row["gaps"] == expected_gaps, "gap_projection")
        check(len(pair_set) == 100, "pair_bijection")
        class_counts = {kind: 0 for kind in CLASSIFICATIONS}
        identity_counts = {status: 0 for status in PRESENCE}
        for row in flows:
            for route_row in row["routes"]: class_counts[route_row["classification"]] += 1
            for identity in row["state_identities"]: identity_counts[identity["source_status"]] += 1
        check(matrix["coverage"] == {
            "release_records": 20, "release_quantity_rows": 100,
            "present_rows": 100, "absent_rows": 0, "ambiguous_rows": 0,
            "classification_counts": class_counts,
            "identity_source_status_counts": identity_counts,
            "missing_release_quantity_pairs": 0, "duplicate_release_quantity_pairs": 0,
            "route_overlap_errors": 0, "ignored_with_consumer_errors": 0,
            "fallback_contract_errors": 0, "unit_basis_sign_scope_merge_errors": 0,
        }, "coverage")
        check(matrix["validation"] == {
            "strict_step82_inputs": "PASS", "all_129_occurrences_bound": "PASS",
            "production_20_of_129_lossless_partition": "PASS", "code_occurrence_bijection": "PASS",
            "source_git_blob_identity": "PASS", "ast_parse_20_of_20": "PASS",
            "release_quantity_bijection_100_of_100": "PASS", "source_anchor_hashes": "PASS",
            "exclusive_presence": "PASS", "exclusive_route_classification": "PASS",
            "quantity_identity_separation": "PASS", "static_only_authority": "PASS",
        }, "validation")
    except (KeyError, TypeError, IndexError, ValidationFailure) as exc:
        errors.append("schema:" + str(exc))
    return errors


def independent_projection(matrix: dict[str, Any]) -> tuple[int, int, int]:
    inventory_raw = bytes(git("cat-file", "blob", f"{EXPECTED_PARENT}:{INVENTORY_PATH}", binary=True))
    attestation_raw = bytes(git("cat-file", "blob", f"{EXPECTED_PARENT}:{ATTESTATION_PATH}", binary=True))
    require(sha256(inventory_raw) == INVENTORY_RAW_SHA256 and sha256(attestation_raw) == ATTESTATION_RAW_SHA256, "E_STEP82_INPUT_HASH")
    inventory = strict_input_load(inventory_raw, INVENTORY_PATH)
    attestation = strict_input_load(attestation_raw, ATTESTATION_PATH)
    require(inventory["semantic_sha256"] == INVENTORY_SEMANTIC_SHA256 and attestation["semantic_sha256"] == ATTESTATION_SEMANTIC_SHA256, "E_STEP82_SEMANTIC")
    all_rows = inventory["occurrence_records"]
    code_rows = [row for row in all_rows if row["role"] == "code"]
    excluded = [row for row in all_rows if row["role"] != "code"]
    require(len(all_rows) == 129 and len(code_rows) == 20 and len(excluded) == 109, "E_ROLE_PARTITION")
    require(len({row["blob_oid"] for row in code_rows}) == 15, "E_CODE_BLOBS")
    require(sorted_lines_sha([row["path"] for row in code_rows]) == CODE_PATH_SHA256, "E_CODE_PATH_HASH")
    require(sorted_lines_sha([row["path"] + "\t" + row["blob_oid"] for row in code_rows]) == CODE_PATH_BLOB_SHA256, "E_CODE_PATH_BLOB_HASH")
    require(sorted_lines_sha(list({row["blob_oid"] for row in code_rows})) == CODE_BLOB_SHA256, "E_CODE_BLOB_HASH")
    require(sorted_lines_sha([row["release"] + "\t" + row["path"] for row in code_rows]) == CODE_RELEASE_PATH_SHA256, "E_CODE_RELEASE_HASH")
    require(sorted_lines_sha([row["release"] + "\t" + row["path"] + "\t" + row["blob_oid"] + "\t" + str(row["blob_ordinal"]) for row in code_rows]) == CODE_OCCURRENCE_SHA256, "E_CODE_OCCURRENCE_HASH")
    expected_by_release = {row["release"]: row for row in code_rows}
    require(set(expected_by_release) == set(RELEASES), "E_RELEASES")
    source_map = {row["release"]: row for row in matrix["source_records"]}
    for release in RELEASES:
        expected = expected_by_release[release]
        stored = source_map[release]
        for key in ("manifest_entry_index", "path", "blob_oid", "blob_ordinal", "git_mode", "physical_lines"):
            require(stored[key] == expected[key], "E_SOURCE_PROJECTION", f"{release}:{key}")
        raw = bytes(git("cat-file", "blob", expected["blob_oid"], binary=True))
        require(sha256(raw) == stored["raw_sha256"], "E_SOURCE_RAW", release)
        text = raw.decode("utf-8")
        tree = ast.parse(text)
        lines = text.splitlines()
        roles, blend_roles = independent_anchor_roles(tree, lines)
        for flow in matrix["flow_records"]:
            if flow["release"] == release:
                for stored_anchor in anchors_in(flow):
                    validate_anchor(stored_anchor, tree, lines)
                validate_semantic_roles(flow, stored, roles, blend_roles)
        has_blend = any(isinstance(node, ast.ClassDef) and node.name == "BlendedAnodeDQDV" for node in tree.body)
        require(stored["has_blend"] is has_blend, "E_BLEND_PROJECTION", release)
        normalized_division = any(isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and isinstance(node.right, ast.Constant) and node.right.value == 3600 for node in ast.walk(tree))
        expected_features = {
            "temperature_route": "SORTED_INTERPOLATED_T_WORK" if "T_work" in text else "POINTWISE_ORDERED_T_PROG",
            "temperature_dependent_width_multiplicity": "def _dwdT" in text,
            "vibrational_temperature": "def _vib_theta" in text,
            "global_composition_solver": "def solve_U_oc" in text,
            "lco_composition_centers": "x_center" in text and "x_MIT" in text,
            "lco_curve_facade_sign_flip": "_delith_is_discharge" in text,
            "blend_mass_to_capacity_fraction": has_blend,
            "executable_divide_by_3600": normalized_division,
            "comment_only_seconds_conversion": "1/3600" in text or "3600" in text,
            "transition_capacity_unit_mAh_explicit": "Q [mAh]" in text,
            "default_profile_conflict_bounded": release == "v1.0.25.2",
        }
        require(stored["feature_flags"] == expected_features, "E_FEATURE_PROJECTION", release)
        current_flow = next(row for row in matrix["flow_records"] if row["release"] == release and row["quantity"] == "current")
        rate_state = next(row for row in current_flow["state_identities"] if row["symbol"] == "I_abs/Q_cell/3600")
        require(rate_state["source_status"] == ("PRESENT" if normalized_division else "ABSENT_IN_FROZEN_SOURCE"), "E_RATE_SECONDS")
        if has_blend:
            composition = next(row for row in matrix["flow_records"] if row["release"] == release and row["quantity"] == "composition")
            m_state = next(row for row in composition["state_identities"] if row["symbol"] == "m_Si")
            f_state = next(row for row in composition["state_identities"] if row["symbol"] == "f_Si")
            require(m_state["basis"] == "MASS_FRACTION" and f_state["basis"] == "CAPACITY_FRACTION_Q_Si_OVER_Q_TOTAL", "E_FRACTION_BASIS")
    return len(code_rows), len({row["blob_oid"] for row in code_rows}), len(matrix["flow_records"])


def negative_controls(matrix: dict[str, Any]) -> tuple[int, int]:
    mutations: list[tuple[str, Any]] = []
    def add(name: str, mutator: Any) -> None:
        mutations.append((name, mutator))

    def flow(value: dict[str, Any], release: str, quantity: str) -> dict[str, Any]:
        return next(row for row in value["flow_records"]
                    if row["release"] == release and row["quantity"] == quantity)

    def source(value: dict[str, Any], release: str) -> dict[str, Any]:
        return next(row for row in value["source_records"] if row["release"] == release)

    def identity(value: dict[str, Any], release: str, quantity: str, symbol: str) -> dict[str, Any]:
        return next(row for row in flow(value, release, quantity)["state_identities"]
                    if row["symbol"] == symbol)

    def route(value: dict[str, Any], release: str, quantity: str, condition: str) -> dict[str, Any]:
        return next(row for row in flow(value, release, quantity)["routes"]
                    if row["condition"] == condition)

    def mutate_source_occurrence(value: dict[str, Any], key: str, replacement: Any) -> None:
        release = RELEASES[0]
        source(value, release)[key] = replacement
        for row in value["flow_records"]:
            if row["release"] == release:
                row["occurrence"][key] = replacement

    add("top_extra", lambda x: x.update({"extra": 1}))
    add("metadata_parent", lambda x: x.__setitem__("expected_parent", "0" * 40))
    add("authority_runtime", lambda x: x["authority"].__setitem__("runtime_behavior", True))
    add("universe_exclusion", lambda x: x["universe"].__setitem__("losslessly_excluded_nonproduction_occurrences", 108))
    add("release_drop", lambda x: x["source_records"].pop())
    add("release_order", lambda x: x["source_records"].__setitem__(slice(0, 2), list(reversed(x["source_records"][:2]))))
    add("occurrence_path", lambda x: mutate_source_occurrence(x, "path", "Claude/docs/WRONG.py"))
    add("occurrence_blob", lambda x: mutate_source_occurrence(x, "blob_oid", "0" * 40))
    add("shared_blob_collapse", lambda x: mutate_source_occurrence(
        x, "blob_oid", next(row["blob_oid"] for row in x["source_records"]
                            if row["blob_oid"] != x["source_records"][0]["blob_oid"])))
    add("remove_flow", lambda x: x["flow_records"].pop())
    add("presence", lambda x: x["flow_records"][0].__setitem__("presence", "ABSENT_IN_FROZEN_SOURCE"))
    add("occurrence_blob_ordinal", lambda x: x["flow_records"][0]["occurrence"].__setitem__("blob_ordinal", 84))
    add("feature_drift", lambda x: source(x, "v1.0.24")["feature_flags"].__setitem__("vibrational_temperature", False))
    add("comment_to_executable", lambda x: source(x, "v1.0.24")["feature_flags"].__setitem__("executable_divide_by_3600", True))
    add("identity_unit", lambda x: x["flow_records"][0]["state_identities"][0].__setitem__("unit", "A"))
    add("identity_basis", lambda x: x["flow_records"][0]["state_identities"][0].__setitem__("basis", "CELL_VOLTAGE"))
    add("identity_sign", lambda x: x["flow_records"][0]["state_identities"][1].__setitem__("sign", "UNSIGNED"))
    add("identity_scope", lambda x: x["flow_records"][4]["state_identities"][1].__setitem__("scope", "GLOBAL_MODEL"))
    add("identity_status", lambda x: x["flow_records"][1]["state_identities"][2].__setitem__("source_status", "PRESENT"))
    add("present_identity_orphan", lambda x: x["flow_records"][0]["state_identities"][0].__setitem__("route_refs", []))
    add("classification", lambda x: x["flow_records"][0]["routes"][0].__setitem__("classification", "OVERWRITTEN"))
    add("direct_vn_to_vapp", lambda x: route(x, "v1.0.10", "voltage", "DIRECT_V_n_EQUILIBRIUM_API").__setitem__("public_inputs", ["V_app"]))
    add("i_abs_c_rate_branch", lambda x: route(x, "v1.0.10", "current", "I_abs_IS_NONE").__setitem__("public_inputs", ["I_abs_SELECTOR", "c_rate"]))
    add("q_basis_promotion", lambda x: identity(x, "v1.0.24", "capacity", "Q_cell").__setitem__("unit", "Ah"))
    add("ignored_consumer", lambda x: x["flow_records"][1]["routes"][2]["consumers"].append(x["flow_records"][1]["routes"][0]["producer"]))
    add("fallback_alternate", lambda x: x["flow_records"][1]["routes"][1].__setitem__("alternate_producer", None))
    add("transform_order", lambda x: x["flow_records"][4]["routes"][0]["ordered_transforms"][0].__setitem__("ordinal", 2))
    add("transform_state_in", lambda x: x["flow_records"][0]["routes"][0]["ordered_transforms"][0].__setitem__("state_in", ["V_app"]))
    add("transform_state_out", lambda x: x["flow_records"][0]["routes"][0]["ordered_transforms"][0].__setitem__("state_out", ["V_app"]))
    add("route_refs_swap", lambda x: x["flow_records"][0]["state_identities"][0].__setitem__("route_refs", [x["flow_records"][0]["routes"][1]["route_id"]]))
    add("producer_consumer_swap", lambda x: x["flow_records"][0]["routes"][0].__setitem__("producer", x["flow_records"][0]["routes"][0]["consumers"][0]))
    add("consumer_producer_swap", lambda x: x["flow_records"][0]["routes"][0].__setitem__("consumers", [x["flow_records"][0]["routes"][0]["producer"]]))
    add("output_role_swap", lambda x: x["flow_records"][0]["routes"][0].__setitem__("output", x["flow_records"][0]["routes"][0]["producer"]))
    add("alternate_role_swap", lambda x: x["flow_records"][0]["routes"][3].__setitem__("alternate_producer", x["flow_records"][0]["routes"][3]["producer"]))
    add("public_input", lambda x: x["flow_records"][0]["routes"][0].__setitem__("public_inputs", ["V_n"]))
    add("operation", lambda x: x["flow_records"][0]["routes"][0]["ordered_transforms"][0].__setitem__("operation", "V_n = V_app"))
    add("condition", lambda x: x["flow_records"][0]["routes"][0].__setitem__("condition", "SOMETIMES"))
    add("anchor_hash", lambda x: x["flow_records"][0]["routes"][0]["producer"].__setitem__("node_sha256", "0" * 64))
    add("nested_extra_key", lambda x: x["flow_records"][0]["routes"][0].update({"extra": 1}))
    add("source_raw_pin", lambda x: x["source_records"][0].__setitem__("raw_sha256", "0" * 64))
    add("gap_owner", lambda x: flow(x, "v1.0.10", "current")["gaps"][0].__setitem__("owner", "STEP84_CALL_SURFACE"))
    add("coverage_zero", lambda x: x["coverage"].__setitem__("route_overlap_errors", 1))
    add("validation", lambda x: x["validation"].__setitem__("source_anchor_hashes", "FAIL"))
    add("m_f_merge", lambda x: identity(x, "v1.0.22", "composition", "m_Si").__setitem__("basis", "CAPACITY_FRACTION_Q_Si_OVER_Q_TOTAL"))
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(matrix)
        mutate(candidate)
        candidate["semantic_sha256"] = semantic_hash(candidate)
        if artifact_errors(candidate):
            passed += 1
        else:
            try:
                independent_projection(candidate)
            except ValidationFailure:
                passed += 1
            else:
                raise ValidationFailure("E_NEGATIVE_FALSE_PASS", name)

    contract_controls: list[tuple[str, Any]] = []
    builder_raw = (ROOT / BUILDER_PATH).read_bytes()
    result_raw = (ROOT / RESULT_PATH).read_bytes()
    contract_controls.append(("source_policy_pin", lambda: assert_source_policy_hash(
        builder_raw, "BUILDER_SOURCE_POLICY_SHA256_LF", "0" * 64, "E_BUILDER_POLICY_HASH")))
    contract_controls.append(("control_document_pin", lambda: assert_control_document_hash(
        result_raw, "0" * 64, RESULT_PATH)))
    merge_parents = [EXPECTED_PARENT, "0" * 40]
    contract_controls.append(("merge_parent", lambda: assert_single_parent(merge_parents)))
    ref_record = expected_repository_record(EXPECTED_PARENT)
    ref_record["active_tracking_oid"] = "0" * 40
    contract_controls.append(("repository_ref_drift", lambda: assert_repository_record(
        ref_record, EXPECTED_PARENT)))
    entry = {"repository_refs": expected_repository_record(EXPECTED_PARENT), "status": {}, "index": {}}
    terminal = copy.deepcopy(entry)
    terminal["status"] = {MATRIX_PATH: " M"}
    contract_controls.append(("transaction_toctou", lambda: assert_transaction_unchanged(entry, terminal)))
    for name, operation in contract_controls:
        try:
            operation()
        except ValidationFailure:
            passed += 1
        else:
            raise ValidationFailure("E_NEGATIVE_FALSE_PASS", name)
    return passed, len(mutations) + len(contract_controls)


def strict_json_controls() -> tuple[int, int]:
    controls = [b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'\xef\xbb\xbf{}\n', b'{"semantic_sha256":"0"}\n']
    passed = 0
    for raw in controls:
        try:
            strict_load(raw, "negative")
        except ValidationFailure:
            passed += 1
    require(passed == len(controls), "E_JSON_NEGATIVES")
    return passed, len(controls)


def parse_porcelain(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4, "E_STATUS_LINE")
        status, path = line[:2], line[3:].replace("\\", "/")
        require(" -> " not in path, "E_STATUS_RENAME")
        require(path not in result, "E_STATUS_DUPLICATE")
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


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    return text.removesuffix(".git").strip("/")


def live_oid(ref: str) -> str:
    text = str(git("ls-remote", "--heads", "origin", ref))
    require("\t" in text, "E_LIVE_REF", ref)
    return text.split("\t", 1)[0]


def expected_repository_record(expected_tip: str) -> dict[str, Any]:
    return {"branch": BRANCH, "head": expected_tip, "upstream_name": UPSTREAM,
            "upstream_oid": expected_tip, "active_tracking_oid": expected_tip,
            "active_live_oid": expected_tip, "origin": "github.com/lksz1412/project_anode_fit",
            "protected_local_oid": PROTECTED_TIP, "protected_tracking_oid": PROTECTED_TIP,
            "protected_live_oid": PROTECTED_TIP, "main_local": "",
            "main_tracking_oid": MAIN_TIP, "main_live_oid": MAIN_TIP}


def assert_repository_record(record: dict[str, Any], expected_tip: str) -> None:
    require(record == expected_repository_record(expected_tip), "E_REPOSITORY_REFS", repr(record))


def repository_refs(expected_tip: str) -> dict[str, Any]:
    record = {
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"), "head": git("rev-parse", "HEAD"),
        "upstream_name": git("rev-parse", "--abbrev-ref", "@{upstream}"), "upstream_oid": git("rev-parse", UPSTREAM),
        "active_tracking_oid": git("rev-parse", f"refs/remotes/{UPSTREAM}"),
        "active_live_oid": live_oid(f"refs/heads/{BRANCH}"),
        "origin": canonical_origin(str(git("ls-remote", "--get-url", "origin"))),
        "protected_local_oid": git("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        "protected_tracking_oid": git("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        "protected_live_oid": live_oid("refs/heads/codex/lib-physics-endgame-v1025_2"),
        "main_local": git("show-ref", "--verify", "--hash", "refs/heads/main", check=False),
        "main_tracking_oid": git("rev-parse", "refs/remotes/origin/main"),
        "main_live_oid": live_oid("refs/heads/main"),
    }
    assert_repository_record(record, expected_tip)
    return record


def worktree_status() -> dict[str, str]:
    return parse_porcelain(str(git("status", "--porcelain=v1", "--untracked-files=all")))


def index_snapshot() -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in str(git("ls-files", "-s")).splitlines():
        meta, path = line.split("\t", 1)
        if path in FINAL_SET:
            mode, oid, stage = meta.split()
            require(stage == "0", "E_INDEX_STAGE")
            result[path] = (mode, oid)
    return result


def transaction_seal(expected_tip: str) -> dict[str, Any]:
    return {"repository_refs": repository_refs(expected_tip), "status": worktree_status(),
            "index": index_snapshot(),
            "path_hashes": {path: sha256((ROOT / path).read_bytes()) for path in FINAL_PATHS if (ROOT / path).exists()},
            "step82_inventory_git_sha256": sha256(bytes(git("cat-file", "blob", f"{EXPECTED_PARENT}:{INVENTORY_PATH}", binary=True))),
            "step82_attestation_git_sha256": sha256(bytes(git("cat-file", "blob", f"{EXPECTED_PARENT}:{ATTESTATION_PATH}", binary=True)))}


def verify_content_worktree() -> None:
    expected = {path: ("??" if FINAL_STATUS[path] == "A" else " M") for path in FINAL_PATHS}
    status = worktree_status()
    require(status == expected, "E_CONTENT_PATHS", repr(status))
    require(not any(path.startswith("Claude/") for path in status), "E_CLAUDE_DIRTY")


def verify_staged() -> None:
    require(git("rev-parse", "HEAD") == EXPECTED_PARENT and git("rev-parse", UPSTREAM) == EXPECTED_PARENT, "E_STAGED_PARENT")
    require(parse_name_status(str(git("diff", "--cached", "--name-status", "--no-renames", "HEAD"))) == FINAL_STATUS, "E_STAGED_PATHS")
    require(git("diff", "--name-only") == "" and git("ls-files", "--others", "--exclude-standard") == "", "E_STAGED_DIRTY")
    require(git("diff", "--cached", "--check") == "", "E_DIFF_CHECK")
    index = index_snapshot()
    require(set(index) == FINAL_SET and all(mode == "100644" for mode, _ in index.values()), "E_INDEX_MODES")
    for path, (_, oid) in index.items():
        raw = (ROOT / path).read_bytes()
        require(git("show", f":{path}", binary=True) == raw and git("cat-file", "blob", oid, binary=True) == raw, "E_INDEX_BYTES", path)


def verify_persistence(commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "E_EXPECTED_COMMIT")
    parents = str(git("show", "-s", "--format=%P", commit)).split()
    assert_single_parent(parents)
    require(git("rev-parse", f"{commit}^") == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(git("show", "-s", "--format=%s", commit) == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT")
    changed = parse_name_status(str(git("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r", f"{commit}^", commit)))
    require(changed == FINAL_STATUS, "E_COMMIT_PATHS")
    tree = parse_ls_tree(str(git("ls-tree", "-r", commit)))
    require(set(tree) == FINAL_SET and all(mode == "100644" for mode, _ in tree.values()), "E_COMMIT_MODES")
    require(git("status", "--porcelain") == "", "E_WORKTREE_DIRTY")
    require(git("diff", "--name-only", PROTECTED_TIP, "--", "Claude") == "", "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        require(git("show", f"{commit}:{path}", binary=True) == (ROOT / path).read_bytes(), "E_COMMITTED_BYTES", path)


def assert_single_parent(parents: list[str]) -> None:
    require(parents == [EXPECTED_PARENT], "E_COMMIT_PARENTS", repr(parents))


def assert_transaction_unchanged(entry: dict[str, Any], terminal: dict[str, Any]) -> None:
    require(entry == terminal, "E_TRANSACTION_SEAL")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content-only", action="store_true")
    group.add_argument("--verify-staged", action="store_true")
    group.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require((args.verify_persistence and args.expected_commit is not None) or (not args.verify_persistence and args.expected_commit is None), "E_EXPECTED_COMMIT_MODE")
    if args.verify_persistence:
        require(re.fullmatch(r"[0-9a-f]{40}", args.expected_commit or "") is not None, "E_EXPECTED_COMMIT")
    expected_tip = args.expected_commit if args.verify_persistence else EXPECTED_PARENT
    entry = transaction_seal(expected_tip or "")
    verify_source_policy()
    verify_control_documents()
    matrix, nodes, depth = strict_load((ROOT / MATRIX_PATH).read_bytes(), MATRIX_PATH)
    errors = artifact_errors(matrix)
    require(not errors, "E_ARTIFACT", repr(errors[:12]))
    code_occurrences, code_blobs, flows = independent_projection(matrix)
    semantic_passed, semantic_total = negative_controls(matrix)
    json_passed, json_total = strict_json_controls()
    if args.content_only:
        verify_content_worktree()
    elif args.verify_staged:
        verify_staged()
    else:
        verify_persistence(args.expected_commit or "")
    terminal = transaction_seal(expected_tip or "")
    assert_transaction_unchanged(entry, terminal)
    print(f"PASS_P067_STEP83_CONTROLS semantic={semantic_passed}/{semantic_total} json={json_passed}/{json_total} nodes={nodes} depth={depth}")
    print(f"{PERSISTENCE if args.verify_persistence else GATE} code={code_occurrences}/{code_blobs} flows={flows} releases=20 quantities=5 determinism=2/2")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationFailure as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
