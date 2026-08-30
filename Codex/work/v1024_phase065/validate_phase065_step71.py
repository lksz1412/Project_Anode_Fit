#!/usr/bin/env python3
"""Validate Phase 065 Step 71 static code/profile/default evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import math
import pathlib
import re
import subprocess
import sys
import unicodedata
from functools import lru_cache
from typing import Any, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[3]
BUILDER = ROOT / "Codex/work/v1024_phase065/build_phase065_step71.py"
VALIDATOR = pathlib.Path(__file__).resolve()
MATRIX = ROOT / "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"
ATTESTATION = ROOT / "Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json"
RESULT = ROOT / "Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md"
PARENT_LEDGER = ROOT / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "d6f680b26fb59c24098f44ed633873a2c6419a4e"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase065): trace v1024 code profile defaults"
GATE = "PASS_P065_STEP71_STATIC_WITH_CONCERNS"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

V23_PATHS = (
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.23/test_gates_v1023.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py",
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py",
    "Claude/docs/v1.0.23/results/tools_check_structure.py",
)
V24_PATHS = (
    "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py",
    "Claude/docs/v1.0.24/test_gates_v1024.py",
    "Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py",
    "Claude/docs/v1.0.24/test_gates_v1024_reflect.py",
    "Claude/docs/v1.0.24/results/tools_check_structure.py",
    "Claude/docs/v1.0.24/results/v1024_final_sample.py",
    "Claude/docs/v1.0.24/results/v1024_reflect_curves.py",
)
V241_PATHS = tuple(path.replace("/v1.0.24/", "/v1.0.24.1/") for path in V24_PATHS)
EXPECTED_PATHS = V23_PATHS + V24_PATHS + V241_PATHS
MSMR6_DOC_PATHS = (
    "Claude/docs/v1.0.24/CODE_GUIDE_v24.md",
    "Claude/docs/v1.0.24/CODE_GUIDE_v24.html",
    "Claude/docs/v1.0.24/results/HANDOVER_v24.md",
    "Claude/docs/v1.0.24/results/INDEX_v24.md",
)

EXACT_EIGHT = (
    "Codex/work/v1024_phase065/build_phase065_step71.py",
    "Codex/work/v1024_phase065/validate_phase065_step71.py",
    "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json",
    "Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json",
    "Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_EIGHT_SET = set(EXACT_EIGHT)

MATRIX_KEYS = {
    "artifact_kind", "authority", "baseline_commit", "defect_boundaries",
    "endpoint_summary", "endpoints", "expected_parent", "feature_routes",
    "findings", "gate", "generated_date", "grammar", "initialization_rows",
    "lineage_pairs", "mirror", "profile_surfaces", "route_outcomes",
    "schema_version", "semantic_sha256", "source_policy", "step",
}
ATTESTATION_KEYS = {
    "artifact_kind", "authority", "baseline_commit", "coverage",
    "expected_parent", "finding_summary", "gate", "generated_date",
    "matrix_semantic_sha256", "matrix_sha256_lf", "result_path",
    "result_sha256_lf", "route_outcomes", "schema_version",
    "semantic_sha256", "step", "unresolved_runtime_routes",
}
INITIALIZATION_KEYS = {
    "argument", "callable", "conflicts", "declared_default", "factory_default",
    "fallback", "line_range", "profile_routes", "registry_default",
    "restore_key", "source_blob", "source_path",
}
PROFILE_KEYS = {
    "ast_kind", "ast_sha256", "contains_kernel_key", "default_routes",
    "entry_count", "kernel_values", "line_range", "profile_id",
    "recursive_transition_keys", "registry_authority", "runtime_behavior_validated",
    "source_blob", "source_path", "top_level_keys",
}
LINEAGE_KEYS = {
    "status", "symbol", "v1023_ast_sha256", "v1023_executable_sha256",
    "v1023_line_range", "v1023_signature", "v1024_ast_sha256",
    "v1024_executable_sha256", "v1024_line_range", "v1024_signature",
}
AUTHORITY_FALSE = {
    "canonical_model_selected", "external_experimental", "external_material",
    "external_primary_literature", "external_scientific", "publication_ready",
    "runtime_behavior_validated", "v1024_1_independent_corroboration",
}
PROFILE_NAMES = (
    "GRAPHITE_STAGING_LIT", "GRAPHITE_STAGING_XRD_v1024",
    "GRAPHITE_STAGING_MSMR6_LIT", "LCO_MSMR_LIT",
    "SI_ELEMENTAL_LIT", "SIOX_LIT", "SIC_LIT", "SI_CASE_SETS",
    "SI_CASE_GAPS", "SI_SPECIFIC_CAPACITY", "GRAPHITE_SPECIFIC_CAPACITY",
)
SELECTED_CALLABLES = (
    "GraphiteAnodeDischargeDQDV.__init__",
    "GraphiteAnodeDischargeDQDV.curve",
    "LCOCathodeDQDV.__init__",
    "BlendedAnodeDQDV.__init__",
    "BlendedAnodeDQDV.from_wt",
    "BlendedAnodeDQDV.curve",
)
SAFE_GIT_SUBCOMMANDS = {
    "cat-file", "diff", "diff-tree", "ls-remote", "rev-parse", "show", "status",
}


class ValidationFailure(RuntimeError):
    pass


def fail(code: str, detail: str = "") -> None:
    raise ValidationFailure(f"{code}: {detail}" if detail else code)


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        fail(code, detail)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    projected = dict(value)
    projected.pop("semantic_sha256", None)
    return sha256_bytes(canonical_bytes(projected))


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {
            "_type": type(value).__name__,
            **{field: stable_ast(value.__dict__[field]) for field in value._fields},
        }
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, tuple):
        return {"_tuple": [stable_ast(item) for item in value]}
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if isinstance(value, complex):
        return {"_complex": [value.real, value.imag]}
    if value is Ellipsis:
        return {"_ellipsis": True}
    return value


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value}")


def strict_pairs(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def traverse(value: Any, depth: int = 0) -> dict[str, int]:
    require(depth <= 128, "E_JSON_DEPTH", str(depth))
    counts = {"all_nodes": 1, "containers": 0, "keys": 0, "scalars": 0, "max_depth": depth}
    if isinstance(value, dict):
        counts["containers"] += 1
        counts["keys"] += len(value)
        children = value.values()
    elif isinstance(value, list):
        counts["containers"] += 1
        children = value
    else:
        require(value is None or isinstance(value, (str, bool, int, float)), "E_JSON_TYPE", type(value).__name__)
        require(not isinstance(value, float) or math.isfinite(value), "E_JSON_NONFINITE")
        counts["scalars"] += 1
        return counts
    for child in children:
        nested = traverse(child, depth + 1)
        for key in ("all_nodes", "containers", "keys", "scalars"):
            counts[key] += nested[key]
        counts["max_depth"] = max(counts["max_depth"], nested["max_depth"])
    return counts


def strict_load_bytes(raw: bytes) -> tuple[dict[str, Any], dict[str, int]]:
    require(lf_bytes(raw) == raw, "E_JSON_LF")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs,
                       parse_constant=reject_constant)
    require(isinstance(value, dict), "E_JSON_ROOT")
    require(canonical_bytes(value) == raw, "E_JSON_CANONICAL")
    return value, traverse(value)


def run_process(args: list[str]) -> bytes:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, check=False)
    if proc.returncode:
        fail("E_GIT_PROCESS", f"{args!r}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout


def run_git(*args: str, binary: bool = False) -> bytes | str:
    raw = run_process(["git", *args])
    return raw if binary else raw.decode("utf-8", "strict")


@lru_cache(maxsize=None)
def git_blob(path: str) -> str:
    return str(run_git("rev-parse", f"{BASELINE}:{path}")).strip()


@lru_cache(maxsize=None)
def git_raw(path: str) -> bytes:
    return bytes(run_git("cat-file", "blob", f"{BASELINE}:{path}", binary=True))


def parse_name_status(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        require(len(parts) == 2 and not parts[0].startswith(("R", "C")), "E_RENAME", line)
        require(parts[1] not in rows, "E_DUPLICATE_PATH", parts[1])
        rows[parts[1]] = parts[0]
    return rows


@lru_cache(maxsize=None)
def endpoint_replay(path: str) -> dict[str, Any]:
    raw = git_raw(path)
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=path, mode="exec", feature_version=(3, 12))
    functions = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
    classes = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
    imports = sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
    lf = lf_bytes(raw)
    return {
        "path": path,
        "version": "v1.0.23" if "/v1.0.23/" in path else "v1.0.24.1" if "/v1.0.24.1/" in path else "v1.0.24",
        "blob": git_blob(path),
        "bytes": len(raw),
        "lines": len(lf.decode("utf-8").splitlines()),
        "sha256_raw": sha256_bytes(raw),
        "sha256_lf": sha256_bytes(lf),
        "ast_sha256": sha256_bytes(canonical_bytes(stable_ast(tree))),
        "parse_grammar": "PYTHON_3_12_AST",
        "parse_status": "STATIC_PARSE_PASS_NO_IMPORT",
        "function_nodes": functions,
        "class_nodes": classes,
        "import_nodes": imports,
    }


def assignment_index(tree: ast.Module) -> dict[str, ast.Assign | ast.AnnAssign]:
    rows: dict[str, ast.Assign | ast.AnnAssign] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            rows[node.targets[0].id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            rows[node.target.id] = node
    return rows


def assignment_value(node: ast.Assign | ast.AnnAssign) -> ast.AST:
    require(node.value is not None, "E_STATIC_ASSIGNMENT_VALUE")
    return node.value


def recursive_dict_keys(node: ast.AST) -> list[str]:
    keys: set[str] = set()
    for current in ast.walk(node):
        if isinstance(current, ast.Dict):
            for key in current.keys:
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    keys.add(key.value)
    return sorted(keys)


def recursive_kernel_values(node: ast.AST) -> list[str]:
    values: set[str] = set()
    for current in ast.walk(node):
        if isinstance(current, ast.Dict):
            for key, value in zip(current.keys, current.values):
                if isinstance(key, ast.Constant) and key.value == "kernel":
                    values.add(ast.unparse(value))
    return sorted(values)


def top_level_keys(node: ast.AST) -> list[str]:
    if not isinstance(node, ast.Dict):
        return []
    return [ast.unparse(key) if key is not None else "**" for key in node.keys]


def independent_profile_rows(tree: ast.Module) -> list[dict[str, Any]]:
    assignments = assignment_index(tree)
    rows: list[dict[str, Any]] = []
    callables = callable_index(tree)

    def references(callable_name: str, symbol: str) -> bool:
        return any(isinstance(current, ast.Name) and current.id == symbol
                   for current in ast.walk(callables[callable_name]))

    default_routes: dict[str, list[str]] = {name: [] for name in PROFILE_NAMES}
    if references("BlendedAnodeDQDV.__init__", "GRAPHITE_STAGING_LIT"):
        default_routes["GRAPHITE_STAGING_LIT"] = ["BlendedAnodeDQDV.graphite_transitions=None"]
    if references("BlendedAnodeDQDV.__init__", "SI_CASE_SETS"):
        default_routes["SI_CASE_SETS"] = ["BlendedAnodeDQDV.si_transitions=None"]
    if references("BlendedAnodeDQDV.__init__", "SI_CASE_GAPS"):
        default_routes["SI_CASE_GAPS"] = ["BlendedAnodeDQDV.gaps"]
    if references("BlendedAnodeDQDV.from_wt", "SI_SPECIFIC_CAPACITY"):
        default_routes["SI_SPECIFIC_CAPACITY"] = ["BlendedAnodeDQDV.from_wt.q_Si=None"]
    if references("BlendedAnodeDQDV.from_wt", "GRAPHITE_SPECIFIC_CAPACITY"):
        default_routes["GRAPHITE_SPECIFIC_CAPACITY"] = ["BlendedAnodeDQDV.from_wt.q_gr"]
    for name in PROFILE_NAMES:
        require(name in assignments, "E_STATIC_PROFILE_SYMBOL", name)
        node = assignments[name]
        value = assignment_value(node)
        if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
            count: int | None = len(value.elts)
        elif isinstance(value, ast.Dict):
            count = len(value.keys)
        else:
            count = None
        kernels = recursive_kernel_values(value)
        rows.append({
            "profile_id": name,
            "source_path": V24_PATHS[0],
            "source_blob": git_blob(V24_PATHS[0]),
            "line_range": [node.lineno, node.end_lineno],
            "ast_kind": type(value).__name__,
            "ast_sha256": sha256_bytes(canonical_bytes(stable_ast(value))),
            "entry_count": count,
            "top_level_keys": top_level_keys(value),
            "recursive_transition_keys": recursive_dict_keys(value),
            "kernel_values": kernels,
            "contains_kernel_key": bool(kernels),
            "default_routes": default_routes[name],
            "registry_authority": "STATIC_SOURCE_ONLY",
            "runtime_behavior_validated": False,
        })
    return rows


def callable_index(tree: ast.Module) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    rows: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            rows[node.name] = node
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    rows[f"{node.name}.{child.name}"] = child
    return rows


def independent_argument_defaults(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[tuple[str, str]]:
    args = node.args
    positional = list(args.posonlyargs) + list(args.args)
    leading = len(positional) - len(args.defaults)
    defaults: dict[str, str] = {}
    for index, arg in enumerate(positional):
        defaults[arg.arg] = "REQUIRED" if index < leading else ast.unparse(args.defaults[index - leading])
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        defaults[arg.arg] = "REQUIRED" if default is None else ast.unparse(default)
    rows = [(arg.arg, defaults[arg.arg]) for arg in positional if arg.arg not in {"self", "cls"}]
    if args.vararg is not None:
        rows.append((f"*{args.vararg.arg}", "VAR_POSITIONAL"))
    rows.extend((arg.arg, defaults[arg.arg]) for arg in args.kwonlyargs)
    if args.kwarg is not None:
        rows.append((f"**{args.kwarg.arg}", "VAR_KEYWORD"))
    return rows


def signature_text(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    suffix = "" if node.returns is None else f" -> {ast.unparse(node.returns)}"
    return f"{prefix} {node.name}({ast.unparse(node.args)}){suffix}"


def executable_sha(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    body = list(node.body)
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    return sha256_bytes(canonical_bytes(stable_ast(ast.Module(body=body, type_ignores=[]))))


def independent_lineage_rows(old_tree: ast.Module, new_tree: ast.Module) -> list[dict[str, Any]]:
    old = callable_index(old_tree)
    new = callable_index(new_tree)
    rows: list[dict[str, Any]] = []
    for name in sorted(set(old) | set(new)):
        left = old.get(name)
        right = new.get(name)
        if left is None:
            status = "ADDED_V1024"
        elif right is None:
            status = "REMOVED_V1024"
        elif canonical_bytes(stable_ast(left)) == canonical_bytes(stable_ast(right)):
            status = "AST_IDENTICAL"
        elif signature_text(left) != signature_text(right):
            status = "SIGNATURE_CHANGED"
        elif executable_sha(left) == executable_sha(right):
            status = "DOCSTRING_OR_ANNOTATION_CHANGED_EXECUTABLE_IDENTICAL"
        else:
            status = "EXECUTABLE_BODY_CHANGED_SIGNATURE_STABLE"
        rows.append({
            "symbol": name, "status": status,
            "v1023_line_range": None if left is None else [left.lineno, left.end_lineno],
            "v1024_line_range": None if right is None else [right.lineno, right.end_lineno],
            "v1023_ast_sha256": None if left is None else sha256_bytes(canonical_bytes(stable_ast(left))),
            "v1024_ast_sha256": None if right is None else sha256_bytes(canonical_bytes(stable_ast(right))),
            "v1023_executable_sha256": None if left is None else executable_sha(left),
            "v1024_executable_sha256": None if right is None else executable_sha(right),
            "v1023_signature": None if left is None else signature_text(left),
            "v1024_signature": None if right is None else signature_text(right),
        })
    return rows


def callable_source(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    return ast.unparse(ast.Module(body=[node], type_ignores=[]))


def persistence_callable_census(tree: ast.Module) -> list[str]:
    persistence_names = {
        "save", "load", "restore", "serialize", "serialise", "deserialize",
        "deserialise", "to_dict", "from_dict", "state_dict", "load_state_dict",
        "__getstate__", "__setstate__",
    }
    return sorted(symbol for symbol in callable_index(tree)
                  if "." in symbol
                  and symbol.rsplit(".", 1)[-1].lower() in persistence_names)


def factory_callable_census(tree: ast.Module) -> list[str]:
    return sorted(symbol for symbol in callable_index(tree)
                  if symbol.rsplit(".", 1)[-1].startswith("from_"))


def restoration_key_census(tree: ast.Module) -> list[str]:
    restoration_keys = {
        "restore_key", "saved_state", "state_dict", "schema_version",
        "model_version", "migration_version",
    }
    return sorted({current.value for current in ast.walk(tree)
                   if isinstance(current, ast.Constant)
                   and isinstance(current.value, str)
                   and current.value.lower() in restoration_keys})


def symbol_load_anchors(paths: Iterable[str], symbol: str) -> list[str]:
    anchors: list[str] = []
    for path in paths:
        tree = ast.parse(git_raw(path).decode("utf-8"), filename=path,
                         mode="exec", feature_version=(3, 12))
        anchors.extend(
            f"{path}:{node.lineno}" for node in ast.walk(tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
            and node.id == symbol)
    return sorted(anchors)


def text_reference_anchors(paths: Iterable[str], symbol: str) -> list[str]:
    anchors: list[str] = []
    for path in paths:
        text = git_raw(path).decode("utf-8")
        anchors.extend(f"{path}:{line_no}" for line_no, line in enumerate(
            text.splitlines(), start=1) if symbol in line)
    return anchors


def independent_dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = independent_dotted_name(node.value)
        return None if prefix is None else f"{prefix}.{node.attr}"
    return None


def independent_static_literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = independent_static_literal_string(node.left)
        right = independent_static_literal_string(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def independent_target_names(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, (ast.Tuple, ast.List)):
        names: set[str] = set()
        for item in node.elts:
            names.update(independent_target_names(item))
        return names
    return set()


def independent_direct_bindings(statement: ast.stmt) -> set[str]:
    names: set[str] = set()

    class IndependentSameScopeVisitor(ast.NodeVisitor):
        def visit_Name(self, node: ast.Name) -> None:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                names.add(node.id)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            names.add(node.name)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            names.add(node.name)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            names.add(node.name)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            for alias in node.names:
                names.add(alias.asname or alias.name)

        def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
            if node.name:
                names.add(node.name)
            self.generic_visit(node)

        def visit_MatchAs(self, node: ast.MatchAs) -> None:
            if node.name:
                names.add(node.name)
            self.generic_visit(node)

        def visit_MatchStar(self, node: ast.MatchStar) -> None:
            if node.name:
                names.add(node.name)

        def visit_MatchMapping(self, node: ast.MatchMapping) -> None:
            if node.rest:
                names.add(node.rest)
            self.generic_visit(node)

    IndependentSameScopeVisitor().visit(statement)
    return names


def independent_mutation_root_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, (ast.Attribute, ast.Subscript, ast.Starred)):
        return independent_mutation_root_name(node.value)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in {"getattr", "vars"} and node.args):
        return independent_mutation_root_name(node.args[0])
    return None


def independent_direct_mutation_roots(statement: ast.stmt) -> set[str]:
    roots: set[str] = set()

    class IndependentSameScopeMutationVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            return

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                root = independent_mutation_root_name(node)
                if root is not None:
                    roots.add(root)
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                root = independent_mutation_root_name(node)
                if root is not None:
                    roots.add(root)
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:
            target: ast.AST | None = None
            if (isinstance(node.func, ast.Name)
                    and node.func.id in {"setattr", "delattr"} and node.args):
                target = node.args[0]
            elif (isinstance(node.func, ast.Attribute)
                  and node.func.attr in {"__setattr__", "__delattr__"}):
                target = node.func.value
            elif (isinstance(node.func, ast.Call)
                  and isinstance(node.func.func, ast.Name)
                  and node.func.func.id == "getattr" and len(node.func.args) >= 2
                  and isinstance(node.func.args[1], ast.Constant)
                  and node.func.args[1].value in {"__setattr__", "__delattr__"}):
                target = node.func.args[0]
            if target is not None:
                root = independent_mutation_root_name(target)
                if root is not None:
                    roots.add(root)
            self.generic_visit(node)

    IndependentSameScopeMutationVisitor().visit(statement)
    return roots


def independent_loaded_names(node: ast.AST) -> set[str]:
    return {candidate.id for candidate in ast.walk(node)
            if isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)}


def independent_contains_loader_danger(
        node: ast.AST, allowed_semantic_load_ids: set[int]) -> bool:
    dangerous_names = {
        "globals", "locals", "vars", "builtins", "__builtins__",
        "eval", "exec", "compile", "__import__", "import_module",
        "_getframe", "currentframe", "f_locals", "f_globals", "__globals__",
        "__getattribute__", "sys", "inspect", "importlib", "getattr", "operator",
        "_operator",
        "attrgetter", "methodcaller",
    }
    dangerous_attributes = {
        "eval", "exec", "compile", "import_module", "_getframe",
        "currentframe", "f_locals", "f_globals", "__globals__",
        "__getattribute__", "modules", "attrgetter", "methodcaller",
    }
    for candidate in ast.walk(node):
        if isinstance(candidate, ast.Import):
            exact_frozen_mixed_import = (
                sha256_bytes(canonical_bytes(stable_ast(candidate)))
                == "998b812e8c1f1a1db0043a14acea6d81bce0068ac3987f440bf6987493464570")
            for alias in candidate.names:
                module_root = alias.name.split(".")[0]
                exact_importlib_util = (
                    alias.name == "importlib.util" and alias.asname is None)
                if (module_root in {
                        "builtins", "inspect", "operator", "_operator"}
                        or module_root == "importlib" and not exact_importlib_util
                        or module_root == "sys" and not exact_frozen_mixed_import):
                    return True
        if isinstance(candidate, ast.ImportFrom):
            module = (candidate.module or "").split(".")[0]
            if module in {
                    "sys", "importlib", "inspect", "builtins", "operator", "_operator"}:
                return True
        if (isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)
                and candidate.id in dangerous_names
                and id(candidate) not in allowed_semantic_load_ids):
            return True
        if isinstance(candidate, ast.Attribute):
            if candidate.attr in dangerous_attributes:
                return True
        if (isinstance(candidate, ast.Attribute) and candidate.attr in dangerous_names
                and any(isinstance(root, ast.Name)
                        and root.id in {"builtins", "__builtins__"}
                        for root in ast.walk(candidate.value))):
            return True
        if (isinstance(candidate, ast.Subscript)
                and isinstance(candidate.slice, ast.Constant)
                and candidate.slice.value in dangerous_names
                and any(isinstance(root, ast.Name)
                        and root.id in {"builtins", "__builtins__"}
                        for root in ast.walk(candidate.value))):
            return True
        if (isinstance(candidate, ast.Call) and isinstance(candidate.func, ast.Name)
                and candidate.func.id == "getattr"):
            exact_attribute = (
                candidate.args[1].value if len(candidate.args) >= 2
                and isinstance(candidate.args[1], ast.Constant)
                and isinstance(candidate.args[1].value, str) else None)
            if (exact_attribute is None or exact_attribute in dangerous_attributes
                    or any(isinstance(root, ast.Name)
                           and root.id in {
                               "sys", "importlib", "inspect", "builtins", "__builtins__",
                           } for root in ast.walk(candidate.args[0]))):
                return True
        if (isinstance(candidate, ast.Subscript)
                and independent_static_literal_string(candidate.slice) in dangerous_attributes):
            return True
    return False


def independent_lexical_scopes(
        tree: ast.Module) -> list[
            ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda]:
    scopes: list[
        ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda] = [tree]
    scopes.extend(candidate for candidate in ast.walk(tree)
                  if isinstance(candidate, (
                      ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)))
    return scopes


INDEPENDENT_FROZEN_LOADER_TREE_SHA256 = {
    "6c61f53ceef871e3320aad63d32d82b4e084abbeb9734d80866c3204e6e1ea26",
    "d5a0ad5e8355c7cbc4d8003590d165614f70af13ff7861f98d7d8df839b41886",
    "d9e3a89a37339aed1f5ea6b19f93825cf758d1ebb4336edc911d58607529ea9c",
    "9ffb4f9428986a86473914d305aafebc8dacd29124b5aca3ac649c6d95f657c5",
    "97e800c289c709f65edf6f9a0b3e36dbb4b9720260d32a1ed08bc10706f548e2",
}

INDEPENDENT_LOADER_RESERVED_ROLE_NAMES = {
    "eval", "exec", "compile", "__import__", "import_module",
    "_getframe", "currentframe", "f_locals", "f_globals", "__globals__",
    "__getattribute__", "getattr", "attrgetter", "methodcaller",
    "subprocess", "os", "importlib", "sys", "inspect", "builtins",
    "__builtins__", "operator", "_operator", "globals", "locals", "vars",
}


def independent_strict_precompletion_loader_danger(
        statement: ast.stmt, approved_call_ids: set[int]) -> bool:
    if (isinstance(statement, ast.Import) and len(statement.names) == 1
            and statement.names[0].name == "importlib.util"
            and statement.names[0].asname is None):
        return False
    if (isinstance(statement, ast.Assign) and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
            and isinstance(statement.value, ast.Call)
            and id(statement.value) in approved_call_ids):
        value = statement.value
        function = independent_dotted_name(value.func)
        if (function == "importlib.util.spec_from_file_location"
                and len(value.args) == 2 and not value.keywords
                and all(isinstance(argument, ast.Constant)
                        and isinstance(argument.value, str)
                        for argument in value.args)):
            return False
        if (function == "importlib.util.module_from_spec"
                and len(value.args) == 1 and not value.keywords
                and isinstance(value.args[0], ast.Name)):
            return False
    if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
            and id(statement.value) in approved_call_ids):
        call = statement.value
        if (len(call.args) == 1 and not call.keywords
                and isinstance(call.args[0], ast.Name)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "exec_module"
                and isinstance(call.func.value, ast.Attribute)
                and call.func.value.attr == "loader"
                and isinstance(call.func.value.value, ast.Name)):
            return False
    return True


def independent_exact_trusted_importlib_statement(statement: ast.stmt) -> bool:
    return (
        isinstance(statement, ast.Import)
        and any(alias.name == "importlib.util" and alias.asname is None
                for alias in statement.names)
        and all((alias.asname or alias.name.split(".")[0]) != "importlib"
                or alias.name == "importlib.util" and alias.asname is None
                for alias in statement.names))


def independent_same_scope_importlib_namespace_mutation(statement: ast.stmt) -> bool:
    namespace_names = {"globals", "locals", "vars"}
    namespace_attributes = {
        "__globals__", "f_globals", "f_locals", "_getframe", "currentframe",
    }
    mutation_calls = {
        "update", "__setitem__", "setdefault", "pop", "popitem", "clear",
    }
    has_namespace = False
    has_key = False
    has_mutation = False

    class IndependentNamespaceMutationVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            return

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Name(self, node: ast.Name) -> None:
            nonlocal has_namespace, has_mutation
            if isinstance(node.ctx, ast.Load) and node.id in namespace_names:
                has_namespace = True
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                has_mutation = True

        def visit_Attribute(self, node: ast.Attribute) -> None:
            nonlocal has_namespace, has_mutation
            if node.attr in namespace_attributes:
                has_namespace = True
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                has_mutation = True
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            nonlocal has_mutation
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                has_mutation = True
            self.generic_visit(node)

        def visit_Constant(self, node: ast.Constant) -> None:
            nonlocal has_key
            if node.value == "importlib":
                has_key = True

        def visit_Call(self, node: ast.Call) -> None:
            nonlocal has_mutation
            if isinstance(node.func, ast.Attribute) and node.func.attr in mutation_calls:
                has_mutation = True
            self.generic_visit(node)

    IndependentNamespaceMutationVisitor().visit(statement)
    return has_namespace and has_key and has_mutation


def independent_same_scope_global_importlib_declaration(statement: ast.stmt) -> bool:
    found = False

    class IndependentGlobalDeclarationVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            return

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Global(self, node: ast.Global) -> None:
            nonlocal found
            found = found or "importlib" in node.names

        def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
            nonlocal found
            found = found or "importlib" in node.names

    IndependentGlobalDeclarationVisitor().visit(statement)
    return found


def independent_definition_mutates_enclosing_importlib(
        node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if any(isinstance(candidate, (ast.Global, ast.Nonlocal))
           and "importlib" in candidate.names for candidate in ast.walk(node)):
        return True
    return any(independent_same_scope_importlib_namespace_mutation(statement)
               for statement in node.body)


def independent_same_scope_called_names(statement: ast.stmt) -> set[str]:
    names: set[str] = set()

    class IndependentCalledNameVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            return

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Call(self, node: ast.Call) -> None:
            if isinstance(node.func, ast.Name):
                names.add(node.func.id)
            self.generic_visit(node)

    IndependentCalledNameVisitor().visit(statement)
    return names


def independent_importlib_scope_entry_trust(
        tree: ast.Module) -> dict[int, bool]:
    scope_types = (
        ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda,
    )
    parents: dict[int, ast.AST] = {}

    class IndependentScopeParentVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[ast.AST] = [tree]

        def record(self, node: ast.AST) -> None:
            parents[id(node)] = self.stack[-1]
            self.stack.append(node)
            self.generic_visit(node)
            self.stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.record(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.record(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.record(node)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            self.record(node)

    IndependentScopeParentVisitor().visit(tree)
    cache: dict[int, bool] = {id(tree): False}

    def statement_revokes(statement: ast.stmt) -> bool:
        if independent_exact_trusted_importlib_statement(statement):
            return False
        return (
            "importlib" in independent_direct_bindings(statement)
            or independent_same_scope_global_importlib_declaration(statement)
            or independent_same_scope_importlib_namespace_mutation(statement))

    def replay(
            statements: list[ast.stmt], initial: bool,
            stop: ast.AST | None = None) -> tuple[bool, int | None, set[str]]:
        trusted = initial
        mutators: set[str] = set()
        for index, statement in enumerate(statements):
            if statement is stop:
                return trusted, index, mutators
            if (isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and independent_definition_mutates_enclosing_importlib(statement)):
                mutators.add(statement.name)
            if independent_same_scope_called_names(statement) & mutators:
                trusted = False
            if independent_exact_trusted_importlib_statement(statement):
                trusted = True
            elif statement_revokes(statement):
                trusted = False
        return trusted, None, mutators

    def resolve(scope: ast.AST) -> bool:
        cached = cache.get(id(scope))
        if cached is not None:
            return cached
        parent = parents.get(id(scope))
        if not isinstance(parent, scope_types) or isinstance(parent, ast.Lambda):
            cache[id(scope)] = False
            return False
        statements = parent.body
        inherited = resolve(parent)
        trusted, index, mutators = replay(statements, inherited, scope)
        if index is None:
            cache[id(scope)] = False
            return False
        for statement in statements[index + 1:]:
            if (isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and independent_definition_mutates_enclosing_importlib(statement)):
                mutators.add(statement.name)
            if (independent_same_scope_called_names(statement) & mutators
                    or statement_revokes(statement)):
                trusted = False
                break
        cache[id(scope)] = trusted
        return trusted

    for scope in independent_lexical_scopes(tree):
        resolve(scope)
    return cache


def independent_canonical_nonfrozen_loader_exec_lines(tree: ast.Module) -> list[int]:
    if len(tree.body) < 4:
        return []
    import_statement, spec_statement, module_statement, exec_statement = tree.body[:4]
    if not (isinstance(import_statement, ast.Import)
            and len(import_statement.names) == 1
            and import_statement.names[0].name == "importlib.util"
            and import_statement.names[0].asname is None):
        return []
    if not (isinstance(spec_statement, ast.Assign)
            and len(spec_statement.targets) == 1
            and isinstance(spec_statement.targets[0], ast.Name)
            and isinstance(spec_statement.value, ast.Call)
            and independent_dotted_name(spec_statement.value.func)
            == "importlib.util.spec_from_file_location"
            and len(spec_statement.value.args) == 2
            and not spec_statement.value.keywords
            and all(isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                    for argument in spec_statement.value.args)):
        return []
    spec_name = spec_statement.targets[0].id
    if spec_name in INDEPENDENT_LOADER_RESERVED_ROLE_NAMES:
        return []
    if not (isinstance(module_statement, ast.Assign)
            and len(module_statement.targets) == 1
            and isinstance(module_statement.targets[0], ast.Name)
            and isinstance(module_statement.value, ast.Call)
            and independent_dotted_name(module_statement.value.func)
            == "importlib.util.module_from_spec"
            and len(module_statement.value.args) == 1
            and not module_statement.value.keywords
            and isinstance(module_statement.value.args[0], ast.Name)
            and module_statement.value.args[0].id == spec_name):
        return []
    module_name = module_statement.targets[0].id
    if (module_name == spec_name
            or module_name in INDEPENDENT_LOADER_RESERVED_ROLE_NAMES):
        return []
    call = (exec_statement.value if isinstance(exec_statement, ast.Expr)
            and isinstance(exec_statement.value, ast.Call) else None)
    if not (call is not None and len(call.args) == 1 and not call.keywords
            and isinstance(call.args[0], ast.Name)
            and call.args[0].id == module_name
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == "exec_module"
            and isinstance(call.func.value, ast.Attribute)
            and call.func.value.attr == "loader"
            and isinstance(call.func.value.value, ast.Name)
            and call.func.value.value.id == spec_name):
        return []
    return [call.lineno]


def independent_lexical_loader_exec_lines(tree: ast.Module) -> list[int]:
    result: list[int] = []
    next_generation = 0
    exact_frozen_loader_tree = (
        sha256_bytes(canonical_bytes(stable_ast(tree)))
        in INDEPENDENT_FROZEN_LOADER_TREE_SHA256)
    if not exact_frozen_loader_tree:
        return independent_canonical_nonfrozen_loader_exec_lines(tree)
    entry_trust = independent_importlib_scope_entry_trust(tree)
    for scope in independent_lexical_scopes(tree):
        if scope is not tree and not exact_frozen_loader_tree:
            continue
        live_specs: dict[str, int] = {}
        live_modules: dict[str, tuple[str, int]] = {}
        danger_seen = False
        trusted_importlib = entry_trust[id(scope)]
        if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            arguments = scope.args
            parameter_names = {
                argument.arg for argument in (
                    [*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs]
                    + ([arguments.vararg] if arguments.vararg is not None else [])
                    + ([arguments.kwarg] if arguments.kwarg is not None else []))}
            danger_seen = "importlib" in parameter_names
            if not isinstance(scope, ast.Lambda) and any(
                   "importlib" in independent_direct_bindings(statement)
                   and not (isinstance(statement, ast.Import)
                            and any(alias.name == "importlib.util"
                                    and alias.asname is None
                                    for alias in statement.names))
                   for statement in scope.body):
                danger_seen = True
        statements = ([ast.Expr(value=scope.body)] if isinstance(scope, ast.Lambda)
                      else scope.body)
        for statement in statements:
            rebound = independent_direct_bindings(statement)
            mutation_roots = independent_direct_mutation_roots(statement)
            trusted_import_statement = independent_exact_trusted_importlib_statement(statement)
            if trusted_import_statement:
                trusted_importlib = True
            elif "importlib" in rebound:
                trusted_importlib = False
                danger_seen = True
            if any(isinstance(node, (ast.Global, ast.Nonlocal))
                   and "importlib" in node.names for node in ast.walk(statement)):
                trusted_importlib = False
                danger_seen = True

            def invalidate(name: str) -> None:
                live_specs.pop(name, None)
                live_modules.pop(name, None)
                for module_name, binding in list(live_modules.items()):
                    if binding[0] == name:
                        del live_modules[module_name]

            for name in rebound | mutation_roots:
                invalidate(name)
            value: ast.AST | None = None
            targets: list[ast.AST] = []
            if isinstance(statement, ast.Assign):
                value = statement.value
                targets = list(statement.targets)
            elif isinstance(statement, ast.AnnAssign):
                value = statement.value
                targets = [statement.target]
            target_name = (targets[0].id if len(targets) == 1
                           and isinstance(targets[0], ast.Name) else None)
            function_name = (independent_dotted_name(value.func)
                             if isinstance(value, ast.Call) else None)
            exact_spec_call = (
                target_name is not None and isinstance(value, ast.Call)
                and function_name == "importlib.util.spec_from_file_location"
                and len(value.args) == 2 and not value.keywords)
            module_spec_name = (value.args[0].id if target_name is not None
                                and function_name == "importlib.util.module_from_spec"
                                and len(value.args) == 1 and not value.keywords
                                and isinstance(value.args[0], ast.Name) else None)
            call = (statement.value if isinstance(statement, ast.Expr)
                    and isinstance(statement.value, ast.Call) else None)
            exec_names: tuple[str, str] | None = None
            if (call is not None and len(call.args) == 1 and not call.keywords
                    and isinstance(call.func, ast.Attribute) and call.func.attr == "exec_module"
                    and isinstance(call.func.value, ast.Attribute)
                    and call.func.value.attr == "loader"
                    and isinstance(call.func.value.value, ast.Name)
                    and isinstance(call.args[0], ast.Name)):
                exec_names = (call.func.value.value.id, call.args[0].id)
            allowed_semantic_loads: set[int] = set()
            if ((exact_spec_call and not danger_seen and trusted_importlib)
                    or module_spec_name in live_specs):
                require(isinstance(value, ast.Call), "E_LOADER_CALL_SHAPE")
                allowed_semantic_loads.update(
                    id(candidate) for candidate in ast.walk(value.func)
                    if isinstance(candidate, ast.Name)
                    and isinstance(candidate.ctx, ast.Load)
                    and candidate.id == "importlib")
            approved_call_ids: set[int] = set()
            if exact_spec_call and not danger_seen and trusted_importlib:
                approved_call_ids.add(id(value))
            if module_spec_name in live_specs:
                approved_call_ids.add(id(value))
            if exec_names is not None:
                spec_name, module_name = exec_names
                if live_modules.get(module_name) == (
                        spec_name, live_specs.get(spec_name)):
                    approved_call_ids.add(id(call))
            if (not exact_frozen_loader_tree
                    and independent_strict_precompletion_loader_danger(
                        statement, approved_call_ids)):
                danger_seen = True
                for name in list(live_specs) + list(live_modules):
                    invalidate(name)
            if independent_contains_loader_danger(statement, allowed_semantic_loads):
                danger_seen = True
                for name in list(live_specs) + list(live_modules):
                    invalidate(name)
            permitted_live_loads: set[str] = set()
            if module_spec_name in live_specs:
                permitted_live_loads.add(module_spec_name)
            if exec_names is not None:
                spec_name, module_name = exec_names
                if live_modules.get(module_name) == (spec_name, live_specs.get(spec_name)):
                    permitted_live_loads.update(exec_names)
            live_names = set(live_specs) | set(live_modules)
            for name in (independent_loaded_names(statement) & live_names) - permitted_live_loads:
                invalidate(name)
            if target_name is not None and isinstance(value, ast.Call):
                if exact_spec_call and not danger_seen and trusted_importlib:
                    next_generation += 1
                    live_specs[target_name] = next_generation
                elif module_spec_name in live_specs:
                    live_modules[target_name] = (
                        module_spec_name, live_specs[module_spec_name])
            if call is not None and exec_names is not None:
                spec_name, module_name = exec_names
                if live_modules.get(module_name) == (spec_name, live_specs.get(spec_name)):
                    result.append(call.lineno)
    return sorted(result)


def fresh_loader_census() -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    for path in V24_PATHS:
        tree = ast.parse(git_raw(path).decode("utf-8"), filename=path,
                         mode="exec", feature_version=(3, 12))
        rows.extend((path, line) for line in independent_lexical_loader_exec_lines(tree))
    return sorted(rows)


def independent_initialization_rows(
        old_tree: ast.Module, new_tree: ast.Module) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    callables = callable_index(new_tree)
    old_callables = callable_index(old_tree)
    require(persistence_callable_census(new_tree) == [], "E_STATIC_PERSISTENCE_CENSUS")
    require(restoration_key_census(new_tree) == [], "E_STATIC_RESTORE_KEY_CENSUS")
    require(factory_callable_census(new_tree) == ["BlendedAnodeDQDV.from_wt"],
            "E_STATIC_FACTORY_CENSUS")

    special_evidence = {
        ("GraphiteAnodeDischargeDQDV.__init__", "chi"): (
            "self.chi = _finite('chi', chi) if chi is not None else self.x",),
        ("GraphiteAnodeDischargeDQDV.__init__", "use_dH_eff"): (
            "self.use_dH_eff = bool(use_dH_eff)",),
        ("GraphiteAnodeDischargeDQDV.__init__", "lag_ratio_correction"): (
            "self.lag_ratio_correction = bool(lag_ratio_correction)",),
        ("GraphiteAnodeDischargeDQDV.curve", "I_abs"): (
            "if I_abs is None", "I_use = c * Q_cell"),
        ("LCOCathodeDQDV.__init__", "include_electronic_entropy"): (
            "self.include_electronic_entropy = bool(include_electronic_entropy)",),
        ("BlendedAnodeDQDV.__init__", "graphite_transitions"): (
            "GRAPHITE_STAGING_LIT if graphite_transitions is None else graphite_transitions",),
        ("BlendedAnodeDQDV.__init__", "si_transitions"): (
            "if si_transitions is None", "si_src = SI_CASE_SETS[si_case]"),
        ("BlendedAnodeDQDV.__init__", "si_case"): (
            "self.si_case = si_case", "if si_transitions is None",
            "if si_case not in SI_CASE_SETS", "SI_CASE_SETS[si_case]",
            "SI_CASE_GAPS.get(si_case, [])"),
        ("BlendedAnodeDQDV.__init__", "si_stress_offset"): (
            "self.si_stress_offset = si_stress_offset",
            "if si_stress_offset is not None",
            "_finite('si_stress_offset', si_stress_offset)", "for tr in si_trs"),
        ("BlendedAnodeDQDV.from_wt", "q_Si"): (
            "if q_Si is None", "q_Si = SI_SPECIFIC_CAPACITY.get(si_case)"),
        ("BlendedAnodeDQDV.from_wt", "q_gr"): (
            "q_gr = _finite_pos('q_gr', q_gr)",),
        ("BlendedAnodeDQDV.curve", "I_abs"): (
            "self.gr_host.curve(V_app, direction, c_rate, Q_cell, T, I_abs)",
            "self.si_host.curve(V_app, direction, c_rate, Q_cell, T, I_abs)"),
    }
    for key, needles in special_evidence.items():
        source = callable_source(callables[key[0]])
        if not all(needle in source for needle in needles):
            errors.append(f"initialization source evidence {key[0]}.{key[1]}")
    old_lco_init = old_callables.get("LCOCathodeDQDV.__init__")
    if old_lco_init is not None and "include_electronic_entropy" in dict(
            independent_argument_defaults(old_lco_init)):
        errors.append("v1023 LCO electronic argument absence")
    direction_source = callable_source(
        callables["GraphiteAnodeDischargeDQDV._direction_to_sigma"])
    if not all(needle in direction_source for needle in (
            "direction.strip().lower()", "return +1 if val >= 0 else -1")):
        errors.append("direction fallback evidence")

    rows: list[dict[str, Any]] = []
    for callable_name in SELECTED_CALLABLES:
        node = callables[callable_name]
        source = callable_source(node)
        for argument, declared in independent_argument_defaults(node):
            registry: Any = "ABSENT_IN_FROZEN_SOURCE"
            factory: Any = "ABSENT_IN_FROZEN_SOURCE"
            fallback = "NO_IMPLICIT_FALLBACK_IDENTIFIED"
            routes: list[str] = []
            conflicts: list[str] = []
            key = (callable_name, argument)
            if key == ("GraphiteAnodeDischargeDQDV.__init__", "transitions"):
                routes = ["EXPLICIT_TRANSITION_LIST", *PROFILE_NAMES[:3]]
            elif key == ("GraphiteAnodeDischargeDQDV.__init__", "chi"):
                fallback = "None -> x; explicit zero is retained"
            elif key == ("GraphiteAnodeDischargeDQDV.__init__", "use_dH_eff"):
                fallback = "bool(value); absent=True, False/0/None off, truthy on"
                routes = ["BOOLEAN_OPTION_GATE"]
            elif key == ("GraphiteAnodeDischargeDQDV.__init__", "lag_ratio_correction"):
                fallback = "bool(value); absent=False, False/0/None off, truthy on"
                routes = ["BOOLEAN_OPTION_GATE"]
            elif key == ("GraphiteAnodeDischargeDQDV.curve", "direction"):
                fallback = "fixed string aliases; numeric direction >= 0 -> +1 and < 0 -> -1"
                conflicts = ["numeric zero maps to the positive direction"]
            elif key == ("GraphiteAnodeDischargeDQDV.curve", "I_abs"):
                fallback = "None -> abs(c_rate * Q_cell); explicit zero overrides c_rate"
                conflicts = ["absent/None and explicit zero are behaviorally distinct"]
            elif key == ("LCOCathodeDQDV.__init__", "include_electronic_entropy"):
                fallback = "bool(value); absent=False, False/0/None off, truthy on"
                conflicts = ["v1.0.23 has no argument and applies the electronic term unconditionally"]
                routes = ["EXPLICIT_FALSE_OR_ZERO", "EXPLICIT_TRUE"]
            elif key == ("BlendedAnodeDQDV.__init__", "graphite_transitions"):
                registry = "GRAPHITE_STAGING_LIT"
                fallback = "None -> GRAPHITE_STAGING_LIT; explicit empty list reaches positive-Q guard"
                routes = ["DEFAULT_GRAPHITE_4", "EXPLICIT_GRAPHITE_5", "EXPLICIT_GRAPHITE_6", "CUSTOM"]
            elif key == ("BlendedAnodeDQDV.__init__", "si_transitions"):
                registry = "SI_CASE_SETS[si_case]"
                fallback = "None -> named si_case; explicit list bypasses si_case membership check"
                routes = ["NAMED_SI_CASE", "CUSTOM"]
            elif key == ("BlendedAnodeDQDV.__init__", "si_case"):
                registry = "SI_CASE_SETS"
                fallback = ("default 'sic'; always stored and used by SI_CASE_GAPS.get; "
                            "when si_transitions is None also validates/selects SI_CASE_SETS[si_case]")
                routes = ["SI_CASE_SETS_WHEN_TRANSITIONS_NONE", "SI_CASE_GAPS_ALWAYS"]
            elif key == ("BlendedAnodeDQDV.__init__", "si_stress_offset"):
                fallback = ("None skips the offset route; explicit zero passes finite validation and "
                            "the transition loop but applies zero offset")
                routes = ["NONE_SKIP", "EXPLICIT_FINITE_OFFSET"]
            elif key == ("BlendedAnodeDQDV.from_wt", "q_Si"):
                registry = "SI_SPECIFIC_CAPACITY[si_case]"
                fallback = "None -> SI_SPECIFIC_CAPACITY.get(si_case); missing key raises"
            elif key == ("BlendedAnodeDQDV.from_wt", "q_gr"):
                registry = "GRAPHITE_SPECIFIC_CAPACITY"
                fallback = "declared symbol default"
            elif key == ("LCOCathodeDQDV.__init__", "**kwargs"):
                forwarded = any(isinstance(current, ast.keyword) and current.arg is None
                                and isinstance(current.value, ast.Name)
                                and current.value.id == argument[2:]
                                for current in ast.walk(node))
                if not forwarded or "super().__init__" not in source:
                    errors.append(f"kwargs forwarding evidence {callable_name}.{argument}")
                fallback = "forwarded through super().__init__ to GraphiteAnodeDischargeDQDV without schema registry"
            elif key == ("BlendedAnodeDQDV.__init__", "**host_kwargs"):
                forwarded = sum(isinstance(current, ast.keyword) and current.arg is None
                                and isinstance(current.value, ast.Name)
                                and current.value.id == "host_kwargs"
                                for current in ast.walk(node))
                if forwarded != 3 or "GraphiteAnodeDischargeDQDV" not in source:
                    errors.append(f"kwargs forwarding evidence {callable_name}.{argument}")
                fallback = "forwarded to GraphiteAnodeDischargeDQDV without schema registry"
            elif key == ("BlendedAnodeDQDV.from_wt", "**kwargs"):
                forwarded = any(isinstance(current, ast.keyword) and current.arg is None
                                and isinstance(current.value, ast.Name)
                                and current.value.id == "kwargs"
                                for current in ast.walk(node))
                if not forwarded or "return cls(" not in source:
                    errors.append(f"kwargs forwarding evidence {callable_name}.{argument}")
                fallback = "forwarded to BlendedAnodeDQDV.__init__; host kwargs are then forwarded without schema registry"
            elif key == ("BlendedAnodeDQDV.curve", "I_abs"):
                fallback = "forwarded to both host curve methods; None -> each host derives abs(c_rate * Q_cell)"
            rows.append({
                "callable": callable_name,
                "source_path": V24_PATHS[0],
                "source_blob": git_blob(V24_PATHS[0]),
                "line_range": [node.lineno, node.end_lineno],
                "argument": argument,
                "declared_default": declared,
                "registry_default": registry,
                "factory_default": factory,
                "restore_key": "ABSENT_IN_FROZEN_SOURCE",
                "fallback": fallback,
                "profile_routes": routes,
                "conflicts": conflicts,
            })
    return rows, errors


def independent_route(route_id: str, static_state: str,
                      source_anchors: list[str], **extra: Any) -> dict[str, Any]:
    row = {
        "route_id": route_id,
        "static_state": static_state,
        "source_anchors": source_anchors,
        "runtime_behavior_validated": False,
        "authority_promoted": False,
    }
    row.update(extra)
    return row


def independent_feature_routes(
        old_tree: ast.Module,
        new_tree: ast.Module) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    old_callables = callable_index(old_tree)
    callables = callable_index(new_tree)
    assignments = assignment_index(new_tree)
    callable_text = {name: callable_source(node) for name, node in callables.items()}
    if "tr.get('kernel') == 'regsol'" not in callable_text["GraphiteAnodeDischargeDQDV.equilibrium"]:
        errors.append("regsol equilibrium selector evidence")
    for name in ("GraphiteAnodeDischargeDQDV.dqdv",
                 "GraphiteAnodeDischargeDQDV.entropy_coefficient",
                 "GraphiteAnodeDischargeDQDV.solve_U_oc"):
        if "regsol" in callable_text[name]:
            errors.append(f"regsol other-method absence {name}")
    named_kernels = {
        name: recursive_kernel_values(assignment_value(assignments[name]))
        for name in PROFILE_NAMES
    }
    if any(named_kernels.values()):
        errors.append("named registry kernel absence")
    if len(assignment_value(assignments["GRAPHITE_STAGING_XRD_v1024"]).elts) != 5:
        errors.append("XRD5 entry census")
    if len(assignment_value(assignments["GRAPHITE_STAGING_MSMR6_LIT"]).elts) != 6:
        errors.append("MSMR6 entry census")
    if recursive_dict_keys(assignment_value(assignments["LCO_MSMR_LIT"])).count("Omega"):
        errors.append("LCO Omega absence")
    lco_defaults = dict(independent_argument_defaults(callables["LCOCathodeDQDV.__init__"]))
    if lco_defaults.get("include_electronic_entropy") != "False":
        errors.append("LCO electronic default evidence")
    old_lco = callable_source(old_callables["LCOCathodeDQDV._effective_dS_rxn"])
    if ("if tr.get('electronic')" not in old_lco
            or "include_electronic_entropy" in old_lco):
        errors.append("v1023 LCO electronic unconditional evidence")
    blend_dqdv = callable_text["BlendedAnodeDQDV.dqdv"]
    if not all(needle in blend_dqdv for needle in (
            "self.gr_host.dqdv(V_app, T, I_abs, Q_cell, s=s)",
            "self.si_host.dqdv(V_app, T, I_abs, Q_cell, s=s)")):
        errors.append("blend full-current route evidence")
    if persistence_callable_census(new_tree) or restoration_key_census(new_tree):
        errors.append("saved-state route absence")
    if factory_callable_census(new_tree) != ["BlendedAnodeDQDV.from_wt"]:
        errors.append("factory route census")
    expected_loaders = sorted([
        ("Claude/docs/v1.0.24/test_gates_v1024.py", 73),
        ("Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py", 17),
        ("Claude/docs/v1.0.24/test_gates_v1024_reflect.py", 5),
        ("Claude/docs/v1.0.24/results/v1024_final_sample.py", 11),
        ("Claude/docs/v1.0.24/results/v1024_reflect_curves.py", 8),
    ])
    if fresh_loader_census() != expected_loaders:
        errors.append("fresh loader census")
    msrm_python = symbol_load_anchors(V24_PATHS, "GRAPHITE_STAGING_MSMR6_LIT")
    if msrm_python:
        errors.append("MSMR6 Python endpoint activation absence")
    msrm_docs = text_reference_anchors(MSMR6_DOC_PATHS, "GRAPHITE_STAGING_MSMR6_LIT")
    expected_docs = [
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.md:284",
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.md:334",
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.html:183",
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.html:210",
        "Claude/docs/v1.0.24/results/HANDOVER_v24.md:73",
        "Claude/docs/v1.0.24/results/INDEX_v24.md:17",
    ]
    if msrm_docs != expected_docs:
        errors.append("MSMR6 documentation reference census")

    all_paths = list(EXPECTED_PATHS)
    rows = [
        independent_route("P065-S71-ROUTE-REGSOL-EQUILIBRIUM", "EXPLICIT_OPT_IN_ONLY",
                          [f"{V24_PATHS[0]}:119-145", f"{V24_PATHS[0]}:597-602"],
                          entry="tr.get('kernel') == 'regsol'", scope="Graphite.equilibrium only"),
        independent_route("P065-S71-ROUTE-REGSOL-NAMED", "ABSENT_FROM_NAMED_PROFILES",
                          [f"{V24_PATHS[0]}:1009-1280"],
                          detail="No frozen named graphite, LCO, or Si registry contains a kernel key."),
        independent_route("P065-S71-ROUTE-REGSOL-OTHER-METHODS", "KERNEL_KEY_IGNORED_LOGISTIC",
                          [f"{V24_PATHS[0]}:679-726", f"{V24_PATHS[0]}:813-834", f"{V24_PATHS[0]}:884-910"],
                          methods=["dqdv", "entropy_coefficient", "solve_U_oc"]),
        independent_route("P065-S71-ROUTE-GRAPHITE-XRD5", "OPT_IN_LOGISTIC_FIVE_FEATURE",
                          [f"{V24_PATHS[0]}:1157-1183"], profile="GRAPHITE_STAGING_XRD_v1024",
                          kernel_keys=0, omega_does_not_select_regsol=True),
        independent_route("P065-S71-ROUTE-GRAPHITE-MSMR6",
                          "DECLARED_OPT_IN_LOGISTIC_NO_PYTHON_ENDPOINT_ACTIVATION_REFERENCE",
                          [f"{V24_PATHS[0]}:1187-1205"], profile="GRAPHITE_STAGING_MSMR6_LIT",
                          kernel_keys=0, python_endpoint_activation_references=msrm_python,
                          documentation_references=msrm_docs),
        independent_route("P065-S71-ROUTE-LCO-INTERACTION", "GROUND_NOT_FOUND_IN_NAMED_LCO_PROFILE",
                          [f"{V24_PATHS[0]}:1011-1032"], profile="LCO_MSMR_LIT", omega_keys=0),
        independent_route("P065-S71-ROUTE-LCO-ELECTRONIC", "DECLARED_DEFAULT_OFF",
                          [f"{V24_PATHS[0]}:1061-1105"], declared_default="False",
                          v1023_state="ARGUMENT_ABSENT_ELECTRONIC_TERM_UNCONDITIONAL"),
        independent_route("P065-S71-ROUTE-BLEND-DEFAULT", "NAMED_DEFAULT_AND_EXPLICIT_OVERRIDE",
                          [f"{V24_PATHS[0]}:1356-1433"], si_case_default="'sic'",
                          graphite_none_default="GRAPHITE_STAGING_LIT"),
        independent_route("P065-S71-ROUTE-BLEND-CURRENT", "SAME_FULL_CURRENT_AND_CAPACITY_TO_BOTH_HOSTS",
                          [f"{V24_PATHS[0]}:1480-1501"], current_partition="ABSENT_IN_FROZEN_SOURCE"),
        independent_route("P065-S71-ROUTE-EXPLICIT-PROFILE", "STATIC_ENTRYPOINT_PRESENT_RUNTIME_PENDING",
                          [f"{V24_PATHS[0]}:368-401", f"{V24_PATHS[0]}:1356-1381"]),
        independent_route("P065-S71-ROUTE-FRESH-IMPORT", "STATIC_TEST_LOADERS_PRESENT_RUNTIME_PENDING", [
            "Claude/docs/v1.0.24/test_gates_v1024.py:70-74",
            "Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py:14-17",
            "Claude/docs/v1.0.24/test_gates_v1024_reflect.py:4-5",
            "Claude/docs/v1.0.24/results/v1024_final_sample.py:9-11",
            "Claude/docs/v1.0.24/results/v1024_reflect_curves.py:7-8",
        ]),
        independent_route("P065-S71-ROUTE-LEGACY-RESTORE", "ABSENT_IN_FROZEN_SOURCE", all_paths),
        independent_route("P065-S71-ROUTE-CURRENT-SAVED-STATE", "ABSENT_IN_FROZEN_SOURCE", all_paths),
    ]
    return rows, errors


def independent_root_validation_uses(
        node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    watched = {"tol", "max_iter"}
    allowed_calls = {"int(max_iter)", "range(int(max_iter))"}
    allowed_test = "hi - lo < tol"
    findings: set[str] = set()
    parents = {
        id(child): parent for parent in ast.walk(node)
        for child in ast.iter_child_nodes(parent)
    }
    operational_max_iter: list[ast.Name] = []
    operational_tol: list[ast.Name] = []
    for candidate in ast.walk(node):
        if (isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)
                and candidate.id == "max_iter"):
            int_call = parents.get(id(candidate))
            range_call = parents.get(id(int_call)) if int_call is not None else None
            loop = parents.get(id(range_call)) if range_call is not None else None
            if (isinstance(int_call, ast.Call) and len(int_call.args) == 1
                    and int_call.args[0] is candidate and not int_call.keywords
                    and isinstance(int_call.func, ast.Name) and int_call.func.id == "int"
                    and isinstance(range_call, ast.Call) and len(range_call.args) == 1
                    and range_call.args[0] is int_call and not range_call.keywords
                    and isinstance(range_call.func, ast.Name) and range_call.func.id == "range"
                    and isinstance(loop, ast.For) and loop.iter is range_call
                    and isinstance(loop.target, ast.Name) and loop.target.id == "_"):
                operational_max_iter.append(candidate)
        if (isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)
                and candidate.id == "tol"):
            comparison = parents.get(id(candidate))
            conditional = parents.get(id(comparison)) if comparison is not None else None
            if (isinstance(comparison, ast.Compare) and len(comparison.ops) == 1
                    and isinstance(comparison.ops[0], ast.Lt)
                    and len(comparison.comparators) == 1
                    and comparison.comparators[0] is candidate
                    and isinstance(comparison.left, ast.BinOp)
                    and isinstance(comparison.left.op, ast.Sub)
                    and isinstance(comparison.left.left, ast.Name)
                    and comparison.left.left.id == "hi"
                    and isinstance(comparison.left.right, ast.Name)
                    and comparison.left.right.id == "lo"
                    and isinstance(conditional, ast.If) and conditional.test is comparison
                    and len(conditional.body) == 1
                    and isinstance(conditional.body[0], ast.Break)
                    and not conditional.orelse):
                operational_tol.append(candidate)
    allowed_watched_load_ids = (
        {id(operational_max_iter[0])} if len(operational_max_iter) == 1 else set())
    if len(operational_tol) == 1:
        allowed_watched_load_ids.add(id(operational_tol[0]))
    for candidate in ast.walk(node):
        if (isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)
                and candidate.id in watched and id(candidate) not in allowed_watched_load_ids):
            findings.add(f"unexpected-load:{candidate.id}:{candidate.lineno}")

    def namespace_reference(value: ast.AST, aliases: set[str]) -> bool:
        namespace_names = {
            "globals", "locals", "vars", "builtins", "__builtins__",
            "getattr", "eval", "exec", "compile", "__import__", "import_module",
            "_getframe", "currentframe", "f_locals", "f_globals",
        } | aliases
        danger_attributes = {
            "getattr", "vars", "globals", "locals", "eval", "exec", "compile",
            "import_module", "_getframe", "currentframe", "f_locals", "f_globals", "modules",
            "__globals__", "__builtins__", "__getattribute__",
        }
        for candidate in ast.walk(value):
            if isinstance(candidate, ast.Import):
                for alias in candidate.names:
                    if alias.name in {"sys", "inspect", "builtins", "importlib"}:
                        return True
                    if alias.name == "importlib.util" and alias.asname is not None:
                        return True
            if isinstance(candidate, ast.ImportFrom):
                module = (candidate.module or "").split(".")[0]
                imported = {alias.name for alias in candidate.names}
                if (module == "builtins"
                        or module == "importlib" and "import_module" in imported
                        or module == "sys" and imported & {"_getframe", "modules"}
                        or module == "inspect" and "currentframe" in imported):
                    return True
            if (isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)
                    and candidate.id in namespace_names):
                return True
            if isinstance(candidate, ast.Attribute):
                if candidate.attr in danger_attributes:
                    return True
            if (isinstance(candidate, ast.Attribute)
                    and candidate.attr in {"globals", "locals", "vars"}
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(candidate.value))):
                return True
            if (isinstance(candidate, ast.Subscript)
                    and isinstance(candidate.slice, ast.Constant)
                    and candidate.slice.value in {"globals", "locals", "vars"}
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(candidate.value))):
                return True
            if (isinstance(candidate, ast.Call) and isinstance(candidate.func, ast.Name)
                    and candidate.func.id == "getattr" and len(candidate.args) >= 2
                    and (independent_static_literal_string(candidate.args[1])
                         in danger_attributes
                         or any(isinstance(root, ast.Name)
                                and root.id in {
                                    "sys", "importlib", "inspect", "builtins", "__builtins__",
                                } for root in ast.walk(candidate.args[0])))):
                return True
            if (isinstance(candidate, ast.Subscript)
                    and independent_static_literal_string(candidate.slice)
                    in danger_attributes):
                return True
        return False

    def bound_names(target: ast.AST) -> set[str]:
        return {candidate.id for candidate in ast.walk(target)
                if isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Store)}

    namespace_marker_present = namespace_reference(node, set())
    if namespace_marker_present:
        findings.add("dynamic-function:tol")
        findings.add("dynamic-function:max_iter")
    namespace_aliases: set[str] = set()
    changed = True
    while changed:
        changed = False
        for candidate in ast.walk(node):
            value: ast.AST | None = None
            targets: list[ast.AST] = []
            if isinstance(candidate, ast.Assign):
                value = candidate.value
                targets = list(candidate.targets)
            elif isinstance(candidate, ast.AnnAssign) and candidate.value is not None:
                value = candidate.value
                targets = [candidate.target]
            elif isinstance(candidate, ast.NamedExpr):
                value = candidate.value
                targets = [candidate.target]
            if value is not None and namespace_reference(value, namespace_aliases):
                additions = set().union(*(bound_names(target) for target in targets))
                if not additions.issubset(namespace_aliases):
                    namespace_aliases.update(additions)
                    changed = True

    def dynamic_watched_lookup(value: ast.AST) -> bool:
        descendants = list(ast.walk(value))
        namespace_present = namespace_reference(value, namespace_aliases)
        watched_key_present = False
        for candidate in descendants:
            text = independent_static_literal_string(candidate)
            if text is None:
                continue
            for token in watched:
                start = 0
                while True:
                    position = text.find(token, start)
                    if position < 0:
                        break
                    before = text[position - 1] if position else ""
                    end = position + len(token)
                    after = text[end] if end < len(text) else ""
                    if ((not before or not (before.isalnum() or before == "_"))
                            and (not after or not (after.isalnum() or after == "_"))):
                        watched_key_present = True
                        break
                    start = position + 1
                if watched_key_present:
                    break
            if watched_key_present:
                break
        return (namespace_present or namespace_marker_present) and watched_key_present

    def contains_watched_load(value: ast.AST) -> bool:
        return (any(isinstance(candidate, ast.Name)
                    and isinstance(candidate.ctx, ast.Load)
                    and candidate.id in watched for candidate in ast.walk(value))
                or dynamic_watched_lookup(value))

    def watched_pattern_names(pattern: ast.pattern) -> set[str]:
        names: set[str] = set()
        for candidate in ast.walk(pattern):
            if (isinstance(candidate, (ast.MatchAs, ast.MatchStar))
                    and candidate.name in watched):
                names.add(candidate.name)
            elif isinstance(candidate, ast.MatchMapping) and candidate.rest in watched:
                names.add(candidate.rest)
        return names

    def record_dynamic_control(value: ast.AST, label: str) -> None:
        if namespace_reference(value, namespace_aliases):
            findings.add(f"dynamic-control:{label}:tol")
            findings.add(f"dynamic-control:{label}:max_iter")

    for candidate in ast.walk(node):
        if isinstance(candidate, ast.Call):
            inputs = [*candidate.args, *(keyword.value for keyword in candidate.keywords)]
            if any(contains_watched_load(value) for value in inputs):
                rendered = ast.unparse(candidate)
                if rendered not in allowed_calls:
                    findings.add(f"call:{rendered}")
        if isinstance(candidate, ast.Compare) and contains_watched_load(candidate):
            rendered = ast.unparse(candidate)
            if rendered != allowed_test:
                findings.add(f"compare:{rendered}")
        if isinstance(candidate, ast.Compare):
            record_dynamic_control(candidate, "compare")
        if isinstance(candidate, (ast.If, ast.While, ast.IfExp, ast.Assert)):
            condition = candidate.test
            record_dynamic_control(condition, "conditional")
            if contains_watched_load(condition) and ast.unparse(condition) != allowed_test:
                findings.add(f"conditional:{ast.unparse(condition)}")
        if isinstance(candidate, ast.Match):
            record_dynamic_control(candidate.subject, "match-subject")
            if contains_watched_load(candidate.subject):
                findings.add(f"match-subject:{ast.unparse(candidate.subject)}")
            for case in candidate.cases:
                bindings = watched_pattern_names(case.pattern)
                if bindings:
                    findings.add(f"match-pattern:{','.join(sorted(bindings))}")
                if case.guard is not None and contains_watched_load(case.guard):
                    findings.add(f"match-guard:{ast.unparse(case.guard)}")
                if case.guard is not None:
                    record_dynamic_control(case.guard, "match-guard")
        if isinstance(candidate, (ast.For, ast.AsyncFor)):
            record_dynamic_control(candidate.iter, "loop-control")
            if contains_watched_load(candidate.iter):
                rendered = ast.unparse(candidate.iter)
                if rendered != "range(int(max_iter))":
                    findings.add(f"loop-control:{rendered}")
        if isinstance(candidate, ast.comprehension):
            record_dynamic_control(candidate.iter, "comprehension-iter")
            if contains_watched_load(candidate.iter):
                findings.add(f"comprehension-iter:{ast.unparse(candidate.iter)}")
            for condition in candidate.ifs:
                record_dynamic_control(condition, "comprehension-if")
                if contains_watched_load(condition):
                    findings.add(f"comprehension-if:{ast.unparse(condition)}")
        if isinstance(candidate, (ast.With, ast.AsyncWith)):
            for item in candidate.items:
                record_dynamic_control(item.context_expr, "with-control")
                if contains_watched_load(item.context_expr):
                    findings.add(f"with-control:{ast.unparse(item.context_expr)}")
    return sorted(findings)


def independent_midpoint_after_iteration_loop(
        node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for outer_loop in ast.walk(node):
        if not isinstance(outer_loop, ast.For):
            continue
        for index, statement in enumerate(outer_loop.body):
            if (not isinstance(statement, ast.For)
                    or ast.unparse(statement.iter) != "range(int(max_iter))"):
                continue
            for successor in outer_loop.body[index + 1:]:
                if not isinstance(successor, (ast.Assign, ast.AnnAssign)):
                    continue
                targets = successor.targets if isinstance(successor, ast.Assign) else [successor.target]
                if (successor.value is not None
                        and any(ast.unparse(target) == "out[k]" for target in targets)
                        and ast.unparse(successor.value) == "0.5 * (lo + hi)"):
                    return True
    return False


def independent_defect_boundaries(
        old_tree: ast.Module, new_tree: ast.Module) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    lineage = {row["symbol"]: row["status"]
               for row in independent_lineage_rows(old_tree, new_tree)}
    required_identical = {
        "func_L_q", "BlendedAnodeDQDV.__init__", "BlendedAnodeDQDV.dqdv",
        "BlendedAnodeDQDV.curve", "GraphiteAnodeDischargeDQDV.solve_U_oc",
        "GraphiteAnodeDischargeDQDV._n_factor",
        "GraphiteAnodeDischargeDQDV._dwdT",
        "GraphiteAnodeDischargeDQDV._resolve_lag_length",
    }
    for symbol in required_identical:
        if lineage.get(symbol) != "AST_IDENTICAL":
            errors.append(f"defect lineage {symbol}")
    old_callables = callable_index(old_tree)
    new_callables = callable_index(new_tree)
    for tree_index in (old_callables, new_callables):
        func_l_q = tree_index["func_L_q"]
        if any(isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
               and isinstance(node.right, ast.Constant) and node.right.value == 3600
               for node in ast.walk(func_l_q)):
            errors.append("seconds /3600 absence predicate")
        blend_init = tree_index["BlendedAnodeDQDV.__init__"]
        if not any(isinstance(node, ast.Attribute)
                   and isinstance(node.value, ast.Name) and node.value.id == "self"
                   and node.attr == "Q" and isinstance(node.ctx, ast.Store)
                   for node in ast.walk(blend_init)):
            errors.append("blend self.Q assignment predicate")
        for symbol in ("BlendedAnodeDQDV.dqdv", "BlendedAnodeDQDV.curve"):
            if any(isinstance(node, ast.Attribute)
                   and isinstance(node.value, ast.Name) and node.value.id == "self"
                   and node.attr == "Q" and isinstance(node.ctx, ast.Load)
                   for node in ast.walk(tree_index[symbol])):
                errors.append(f"external Q_cell self.Q binding absence {symbol}")
        root = tree_index["GraphiteAnodeDischargeDQDV.solve_U_oc"]
        root_source = callable_source(root)
        if not all(needle in root_source for needle in (
                "range(int(max_iter))", "if hi - lo < tol", "out[k] = 0.5 * (lo + hi)")):
            errors.append("root iteration midpoint predicate")
        guard_uses = independent_root_validation_uses(root)
        if guard_uses:
            errors.append(f"root tol max_iter guard absence {guard_uses!r}")
        if not independent_midpoint_after_iteration_loop(root):
            errors.append("root post-loop midpoint structure")
    for symbol, needles in {
        "func_L_q": ("T_attempt = I / Q_cell * h / kB",),
        "BlendedAnodeDQDV.dqdv": (
            "self.gr_host.dqdv(V_app, T, I_abs, Q_cell, s=s)",
            "self.si_host.dqdv(V_app, T, I_abs, Q_cell, s=s)"),
        "GraphiteAnodeDischargeDQDV.solve_U_oc": ("0.5 * (lo + hi)",),
    }.items():
        for tree_index in (old_callables, new_callables):
            source = callable_source(tree_index[symbol])
            if not all(needle in source for needle in needles):
                errors.append(f"defect source evidence {symbol}")
    new_sources = {name: callable_source(node) for name, node in new_callables.items()}
    if not all(needle in new_sources["GraphiteAnodeDischargeDQDV.equilibrium"]
               for needle in ("tr.get('kernel') == 'regsol'", "tr.get('delta', w)")):
        errors.append("fallback kernel delta predicate")
    if "max(float(delta), 1e-09)" not in new_sources["_regsol_dqdv"]:
        errors.append("fallback nonpositive delta predicate")
    if ("return 1.0" not in new_sources["GraphiteAnodeDischargeDQDV._n_factor"]
            or "if tr.get('n') is None:\n        return 0.0" not in
            new_sources["GraphiteAnodeDischargeDQDV._dwdT"]):
        errors.append("fallback width derivative predicate")
    rows = [
        {
            "boundary_id": "SECONDS_HOUR", "static_change": "COMMENT_ONLY_EXECUTABLE_AST_IDENTICAL",
            "v1023_anchors": [f"{V23_PATHS[0]}:105-112", f"{V23_PATHS[0]}:675-705"],
            "v1024_anchors": [f"{V24_PATHS[0]}:148-164", f"{V24_PATHS[0]}:733-763"],
            "finding": "No executable /3600 conversion or explicit unit profile was added.",
            "validated_static_predicates": [
                "func_L_q callable AST is inherited", "no AST division by numeric 3600"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "CURRENT_PARTITION", "static_change": "INHERITED_UNCHANGED_ABSENT_PARTITION",
            "v1023_anchors": [f"{V23_PATHS[0]}:1331-1352"],
            "v1024_anchors": [f"{V24_PATHS[0]}:1480-1501"],
            "finding": "The inherited blend route sends the same full current and external Q_cell to both hosts.",
            "validated_static_predicates": [
                "both host dqdv calls receive I_abs and Q_cell unchanged"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "CAPACITY_BASIS", "static_change": "INHERITED_UNCHANGED_INTERNAL_Q_EXTERNAL_Q_CELL_UNBOUND",
            "v1023_anchors": [f"{V23_PATHS[0]}:1252-1270", f"{V23_PATHS[0]}:1331-1352"],
            "v1024_anchors": [f"{V24_PATHS[0]}:1401-1419", f"{V24_PATHS[0]}:1480-1501"],
            "finding": "The inherited self.Q calculation has no static validation binding external Q_cell to it.",
            "validated_static_predicates": [
                "self.Q is assigned in blend initialization",
                "blend dqdv and curve contain no load of self.Q"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "ROOT_VALIDATION", "static_change": "INHERITED_WITH_SILENT_EXHAUSTION",
            "v1023_anchors": [f"{V23_PATHS[0]}:796-874"],
            "v1024_anchors": [f"{V24_PATHS[0]}:854-932"],
            "finding": "Per-transition Q/n contracts remain incomplete; tol/max_iter have no explicit validation use outside their loop/convergence operations, and exhaustion returns the post-loop midpoint.",
            "validated_static_predicates": [
                "tol appears in no conditional/assertion/helper-call validation beyond hi-lo < tol",
                "max_iter appears in no conditional/assertion/helper-call validation beyond range(int(max_iter))",
                "out[k] midpoint assignment is structurally after the max_iter loop"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "FALLBACK_ROUTES", "static_change": "MIXED_ADDED_AND_INHERITED_SILENT_FALLBACKS",
            "v1023_anchors": [f"{V23_PATHS[0]}:363-400", f"{V23_PATHS[0]}:463-508"],
            "v1024_anchors": [f"{V24_PATHS[0]}:421-458", f"{V24_PATHS[0]}:521-566", f"{V24_PATHS[0]}:597-602"],
            "finding": "Absent, None, zero, typo, and default routes are not uniformly distinguished.",
            "validated_static_predicates": [
                "kernel get selects regsol only by exact equality",
                "missing delta falls back to width",
                "nonpositive delta clamps to 1e-9",
                "missing n returns 1.0 while dwdT returns 0.0"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
    ]
    return rows, errors


def independent_static_errors(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    old_text = git_raw(V23_PATHS[0]).decode("utf-8")
    new_text = git_raw(V24_PATHS[0]).decode("utf-8")
    old_tree = ast.parse(old_text, filename=V23_PATHS[0], feature_version=(3, 12))
    new_tree = ast.parse(new_text, filename=V24_PATHS[0], feature_version=(3, 12))
    if matrix.get("profile_surfaces") != independent_profile_rows(new_tree):
        errors.append("independent profile replay")
    lineage = matrix.get("lineage_pairs", [])
    if lineage != independent_lineage_rows(old_tree, new_tree):
        errors.append("independent lineage replay")
    expected_initialization, initialization_errors = independent_initialization_rows(
        old_tree, new_tree)
    errors.extend(initialization_errors)
    if matrix.get("initialization_rows", []) != expected_initialization:
        errors.append("independent initialization replay")
    expected_routes, route_errors = independent_feature_routes(old_tree, new_tree)
    errors.extend(route_errors)
    if matrix.get("feature_routes", []) != expected_routes:
        errors.append("independent feature route replay")
    expected_defects, defect_errors = independent_defect_boundaries(old_tree, new_tree)
    errors.extend(defect_errors)
    if matrix.get("defect_boundaries", []) != expected_defects:
        errors.append("independent defect replay")
    required_text = {
        "regsol selector": "tr.get('kernel') == 'regsol'",
        "current pass gr": "self.gr_host.dqdv(V_app, T, I_abs, Q_cell, s=s)",
        "current pass si": "self.si_host.dqdv(V_app, T, I_abs, Q_cell, s=s)",
        "seconds expression": "T_attempt = (I / Q_cell) * h / kB",
        "silent root exhaustion": "return 0.5 * (lo + hi)",
    }
    for name, needle in required_text.items():
        if needle not in new_text:
            errors.append(f"source claim {name}")
    for symbol in PROFILE_NAMES:
        node = assignment_index(new_tree)[symbol]
        if recursive_kernel_values(assignment_value(node)):
            errors.append(f"named kernel absence {symbol}")
    persistence_rows: list[str] = []
    restore_keys: list[str] = []
    for path in EXPECTED_PATHS:
        tree = ast.parse(git_raw(path).decode("utf-8"), filename=path,
                         mode="exec", feature_version=(3, 12))
        persistence_rows.extend(f"{path}:{symbol}"
                                for symbol in persistence_callable_census(tree))
        restore_keys.extend(f"{path}:{key}" for key in restoration_key_census(tree))
    if persistence_rows or restore_keys:
        errors.append("saved-state absence census")
    findings = {row.get("finding_id"): row for row in matrix.get("findings", [])}
    if findings.get("P065-S71-F07", {}).get("title") != "No saved-state restoration or migration contract exists":
        errors.append("factory overclaim")
    return errors


def load_builder() -> Any:
    require(BUILDER.is_file(), "E_BUILDER_MISSING", str(BUILDER.relative_to(ROOT)))
    spec = importlib.util.spec_from_file_location("phase065_step71_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "E_BUILDER_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(hasattr(module, "build_artifacts"), "E_BUILDER_INTERFACE")
    return module


def artifact_errors(matrix: dict[str, Any], attestation: dict[str, Any], *, deep: bool = True) -> list[str]:
    errors: list[str] = []

    def check(condition: bool, name: str) -> None:
        if not condition:
            errors.append(name)

    check(set(matrix) == MATRIX_KEYS, "matrix exact keys")
    check(set(attestation) == ATTESTATION_KEYS, "attestation exact keys")
    check(matrix.get("schema_version") == "P065-S71-CODE-PROFILE-1", "matrix schema")
    check(attestation.get("schema_version") == "P065-S71-STATIC-ATTESTATION-1", "attestation schema")
    check(matrix.get("grammar") == {
        "parser": "ast.parse", "feature_version": [3, 12],
        "checkout_imported": False, "source_execution": False,
        "input_transport": "git cat-file blob at frozen baseline",
    }, "grammar contract")
    for row in (matrix, attestation):
        check(row.get("step") == 71, "step")
        check(row.get("baseline_commit") == BASELINE, "baseline")
        check(row.get("expected_parent") == EXPECTED_PARENT, "expected parent")
        check(row.get("gate") == GATE, "gate")
        check(row.get("semantic_sha256") == semantic_hash(row), "semantic hash")
        authority = row.get("authority", {})
        check(set(authority) == AUTHORITY_FALSE | {"internal_static_provenance"}, "authority keys")
        check(authority.get("internal_static_provenance") is True, "internal authority")
        check(all(authority.get(key) is False for key in AUTHORITY_FALSE), "authority ceiling")

    endpoints = matrix.get("endpoints", [])
    check(len(endpoints) == len(EXPECTED_PATHS), "endpoint count")
    check([row.get("path") for row in endpoints] == list(EXPECTED_PATHS), "endpoint ordering")
    if len(endpoints) == len(EXPECTED_PATHS):
        for row, path in zip(endpoints, EXPECTED_PATHS):
            try:
                check(row == endpoint_replay(path), f"endpoint replay {path}")
            except (UnicodeDecodeError, SyntaxError, ValidationFailure) as exc:
                errors.append(f"endpoint replay exception {path}: {exc}")
    summary = matrix.get("endpoint_summary", {})
    check(summary.get("occurrences") == 20, "endpoint occurrences")
    check(summary.get("v1023") == 6 and summary.get("v1024") == 7 and summary.get("v1024_1") == 7, "endpoint versions")
    check(summary.get("unique_blobs") == 12, "endpoint unique blobs")
    check(summary.get("mirror_pairs") == 7, "endpoint mirror pairs")
    check(summary.get("parse_failures") == 0, "parse failures")

    mirror = matrix.get("mirror", {})
    check(mirror.get("pairs") == 7, "mirror count")
    check(mirror.get("all_blob_identical") is True, "mirror identity")
    check(mirror.get("independent_corroboration") is False, "mirror authority")
    check(len(mirror.get("rows", [])) == 7, "mirror rows")
    for left, right in zip(V24_PATHS, V241_PATHS):
        rows = [row for row in mirror.get("rows", []) if row.get("v1024_path") == left]
        check(len(rows) == 1 and rows[0].get("v1024_1_path") == right, f"mirror row {left}")
        if rows:
            check(rows[0].get("blob") == git_blob(left) == git_blob(right), f"mirror blob {left}")

    initialization = matrix.get("initialization_rows", [])
    check(bool(initialization), "initialization rows")
    check(all(set(row) == INITIALIZATION_KEYS for row in initialization), "initialization exact keys")
    init_ids = [(row.get("callable"), row.get("argument")) for row in initialization]
    check(len(init_ids) == len(set(init_ids)), "initialization identity")
    check(all(row.get("source_path") == V24_PATHS[0] for row in initialization), "initialization source")
    check(all(row.get("source_blob") == git_blob(V24_PATHS[0]) for row in initialization), "initialization blob")
    check(all(isinstance(row.get("line_range"), list) and len(row["line_range"]) == 2 for row in initialization), "initialization ranges")

    profiles = matrix.get("profile_surfaces", [])
    profile_ids = [row.get("profile_id") for row in profiles]
    check(len(profile_ids) == len(set(profile_ids)) and len(profile_ids) >= 10, "profile identity")
    check(all(set(row) == PROFILE_KEYS for row in profiles), "profile exact keys")
    check(all(row.get("source_blob") == git_blob(V24_PATHS[0]) for row in profiles), "profile blob")
    check(all(row.get("runtime_behavior_validated") is False for row in profiles), "profile runtime ceiling")

    lineage = matrix.get("lineage_pairs", [])
    check(len(lineage) == 52, "lineage count")
    check(all(set(row) == LINEAGE_KEYS for row in lineage), "lineage exact keys")
    check(sum(row.get("status") == "ADDED_V1024" for row in lineage) == 3, "lineage additions")
    check(sum(row.get("status") == "EXECUTABLE_BODY_CHANGED_SIGNATURE_STABLE" for row in lineage) == 2, "lineage executable changes")
    check(not any(row.get("status") in {"REMOVED_V1024", "SIGNATURE_CHANGED"} for row in lineage), "lineage removal signature")

    feature_routes = matrix.get("feature_routes", [])
    feature_ids = [row.get("route_id") for row in feature_routes]
    check(len(feature_ids) == len(set(feature_ids)) and len(feature_ids) == 13, "feature routes")
    check(all(row.get("runtime_behavior_validated") is False for row in feature_routes), "route runtime ceiling")
    check(any(row.get("route_id") == "P065-S71-ROUTE-REGSOL-NAMED" and row.get("static_state") == "ABSENT_FROM_NAMED_PROFILES" for row in feature_routes), "named regsol absence")
    check(any(row.get("route_id") == "P065-S71-ROUTE-LEGACY-RESTORE" and row.get("static_state") == "ABSENT_IN_FROZEN_SOURCE" for row in feature_routes), "legacy absence")
    check(any(row.get("route_id") == "P065-S71-ROUTE-LCO-ELECTRONIC" and row.get("declared_default") == "False" for row in feature_routes), "LCO default")

    outcomes = matrix.get("route_outcomes", {})
    check(outcomes.get("fresh_import") == "STATIC_TEST_LOADERS_PRESENT_RUNTIME_PENDING", "fresh route")
    check(outcomes.get("explicit_profile") == "STATIC_ENTRYPOINT_PRESENT_RUNTIME_PENDING", "profile route")
    check(outcomes.get("legacy_restoration") == "ABSENT_IN_FROZEN_SOURCE", "legacy route")
    check(outcomes.get("current_saved_state") == "ABSENT_IN_FROZEN_SOURCE", "saved route")
    check(attestation.get("route_outcomes") == outcomes, "outcome cross binding")
    check(set(attestation.get("unresolved_runtime_routes", [])) == {"fresh_import", "explicit_profile", "legacy_restoration"}, "runtime unresolved")

    findings = matrix.get("findings", [])
    finding_ids = [row.get("finding_id") for row in findings]
    check(len(finding_ids) == len(set(finding_ids)) and bool(finding_ids), "finding identity")
    check(all(row.get("severity") in {"P0", "P1", "P2"} for row in findings), "finding severity")
    check(all(row.get("authority_promoted") is False for row in findings), "finding authority")
    summary_expected = {severity: sum(row.get("severity") == severity for row in findings) for severity in ("P0", "P1", "P2")}
    check(attestation.get("finding_summary") == summary_expected, "finding summary")

    defects = matrix.get("defect_boundaries", [])
    defect_ids = [row.get("boundary_id") for row in defects]
    check(len(defect_ids) == len(set(defect_ids)) and set(defect_ids) == {
        "SECONDS_HOUR", "CURRENT_PARTITION", "CAPACITY_BASIS", "ROOT_VALIDATION", "FALLBACK_ROUTES"
    }, "defect boundary identity")
    check(all(row.get("runtime_conclusion") == "WITHHELD_TO_STEP_73" for row in defects), "defect runtime ceiling")

    policy = matrix.get("source_policy", {})
    expected_policy = {
        "active_branch": BRANCH,
        "expected_subject": SUBJECT,
        "protected_branch": PROTECTED_BRANCH,
        "protected_tip": PROTECTED_TIP,
        "main_tip": MAIN_TIP,
        "exact_paths": list(EXACT_EIGHT),
        "result_first": True,
        "json_last": True,
        "frozen_checkout_imported": False,
        "frozen_source_executed": False,
        "network_access": False,
        "git_reads": [
            "cat-file blob",
            "rev-parse <commit>:<path>",
            "diff --cached --name-status -- <result>",
            "show :<result>",
        ],
        "guide_as_default_authority": False,
    }
    check(policy == expected_policy, "source policy contract")

    check(attestation.get("matrix_semantic_sha256") == matrix.get("semantic_sha256"), "matrix semantic cross binding")
    check(attestation.get("matrix_sha256_lf") == sha256_bytes(canonical_bytes(matrix)), "matrix byte cross binding")
    if RESULT.is_file():
        check(attestation.get("result_path") == str(RESULT.relative_to(ROOT)).replace("\\", "/"), "result path")
        check(attestation.get("result_sha256_lf") == sha256_bytes(lf_bytes(RESULT.read_bytes())), "result hash")
    else:
        errors.append("result missing")
    coverage = attestation.get("coverage", {})
    check(coverage.get("endpoint_occurrences") == 20, "coverage endpoints")
    check(coverage.get("mirror_pairs") == 7, "coverage mirrors")
    check(coverage.get("static_parse_pass") == 20, "coverage parse")
    check(coverage.get("initialization_rows") == len(initialization), "coverage initialization")
    check(coverage.get("profile_surfaces") == len(profiles), "coverage profiles")
    check(coverage.get("feature_routes") == len(feature_routes), "coverage routes")
    if deep:
        errors.extend(independent_static_errors(matrix))
    return errors


def control_document_errors() -> list[str]:
    errors: list[str] = []
    files = (RESULT, PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)
    if not all(path.is_file() for path in files):
        return ["control file missing"]
    result = RESULT.read_text(encoding="utf-8")
    parent = PARENT_LEDGER.read_text(encoding="utf-8")
    canonical = CANONICAL_LEDGER.read_text(encoding="utf-8")
    handover = HANDOVER.read_text(encoding="utf-8")
    expected = {
        "result status": (result, "Status: `PASS_PENDING_PERSISTENCE`"),
        "result gate": (result, "Current Step 71 gate: `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; commit/push persistence is pending."),
        "handover checkpoint": (handover, "Current checkpoint: Step 71 `PASS_PENDING_PERSISTENCE`"),
        "handover next": (handover, "after persistence execute Step 72"),
    }
    for name, (text, needle) in expected.items():
        if needle not in text:
            errors.append(name)
    authoritative_lines = {
        "parent": [line for line in parent.splitlines()
                   if re.match(r"^\|\s*065\s*\|", line, re.IGNORECASE)
                   and re.search(r"\bstep\s*71\b", line, re.IGNORECASE)],
        "canonical": [line for line in canonical.splitlines()
                      if ((re.match(r"^\|\s*065\s*\|", line, re.IGNORECASE)
                           and re.search(r"\bstep\s*71\b", line, re.IGNORECASE))
                          or re.match(r"^\|\s*step\s*71\s*\|", line, re.IGNORECASE))],
        "handover": [line for line in handover.splitlines()
                     if (re.match(r"^\|\s*phase\s*065\s+step\s*71\s*\|", line,
                                 re.IGNORECASE)
                         or re.match(r"^-\s*step\s*71\s+final\b", line,
                                     re.IGNORECASE))],
    }
    expected_counts = {"parent": 1, "canonical": 2, "handover": 2}
    expected_counters = (488, 361, 6)
    expected_final_policy = (
        "Current final-policy counters: v35; "
        "semantic/source-policy/loader-negative/loader-positive/strict-JSON "
        "`488/361/247/10/6`.")
    final_policy_lines = [line for line in result.splitlines()
                          if line.startswith("Current final-policy counters:")]
    if final_policy_lines != [expected_final_policy]:
        errors.append(f"result final-policy:{final_policy_lines}")

    def sign_character(value: str) -> bool:
        if not value:
            return False
        normalized = unicodedata.normalize("NFKC", value)
        name = unicodedata.name(value, "")
        return (normalized in {"+", "-", "±", "−"}
                or "PLUS" in name or "MINUS" in name)

    def trailing_digit_before_text_or_row(text: str, start: int) -> bool:
        for value in text[start:]:
            if value == "|" or value.isalpha():
                return False
            if value.isdigit():
                return True
        return False

    def counter_evidence(
            line: str) -> tuple[
                list[tuple[int, int, int]], dict[str, list[int]], list[str]]:
        triplets: list[tuple[int, int, int]] = []
        malformed: list[str] = []
        for match in re.finditer(r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)", line):
            left_index = match.start() - 1
            while left_index >= 0 and line[left_index].isspace():
                left_index -= 1
            left_value = line[left_index] if left_index >= 0 else ""
            right = line[match.end():]
            invalid_left = bool(
                left_value and (
                    left_value.isalnum() or left_value == "."
                    or sign_character(left_value)))
            invalid_right = bool(
                right and right[0].isalnum()
                or trailing_digit_before_text_or_row(line, match.end()))
            if invalid_left or invalid_right:
                malformed.append(f"triplet@{match.start()}")
            else:
                triplets.append(tuple(int(value) for value in match.groups()))
        label_patterns = {
            "semantic": r"(?<![A-Za-z0-9])semantic(?:[\W_]*(?:negative|case)s?)?(?![A-Za-z0-9])",
            "source": r"(?<![A-Za-z0-9])source[\W_]*policy(?:[\W_]*(?:negative|case)s?)?(?![A-Za-z0-9])",
            "strict": r"(?<![A-Za-z0-9])strict[\W_]*json(?:[\W_]*cases?)?(?![A-Za-z0-9])",
        }
        named_source = re.sub(
            r"(?<![A-Za-z0-9])semantic[\W_]*source[\W_]*policy[\W_]*strict[\W_]*json(?![A-Za-z0-9])",
            lambda match: " " * len(match.group(0)), line, flags=re.IGNORECASE)
        named: dict[str, list[int]] = {name: [] for name in label_patterns}
        labels = sorted(
            (match.start(), match.end(), name)
            for name, pattern in label_patterns.items()
            for match in re.finditer(pattern, named_source, re.IGNORECASE))
        for index, (start, end, name) in enumerate(labels):
            segment_end = labels[index + 1][0] if index + 1 < len(labels) else len(named_source)
            row_boundary = named_source.find("|", end, segment_end)
            if row_boundary >= 0:
                segment_end = row_boundary
            segment = named_source[end:segment_end]
            digit_runs = list(re.finditer(r"[0-9]+", segment))
            valid = len(digit_runs) == 1
            if valid:
                token = digit_runs[0]
                before = segment[token.start() - 1] if token.start() else ""
                after = segment[token.end()] if token.end() < len(segment) else ""
                valid = (
                    len(token.group(0)) <= 3
                    and (not before or not sign_character(before)
                         and before != "." and not before.isalnum())
                    and (not after or after != "." and not after.isalnum()))
            if not valid:
                malformed.append(f"{name}@{start}")
            else:
                named[name].append(int(digit_runs[0].group(0)))
        return triplets, named, malformed

    for document, lines in authoritative_lines.items():
        if len(lines) != expected_counts[document]:
            errors.append(
                f"authoritative row count:{document}:{len(lines)}!={expected_counts[document]}")
        for row_number, line in enumerate(lines, start=1):
            folded = line.casefold()
            release_spans = [
                match.span() for match in re.finditer(
                    r"(?<![A-Za-z0-9])v\d+(?:\.\d+){2,}(?![\d.])", folded)]
            marker_pattern = re.compile(
                r"(?<![A-Za-z0-9])(?:version|attempt|v)(?!\d{3,})(?=[\W_]*\d)",
                re.IGNORECASE)
            valid_pattern = re.compile(
                r"(?:version|attempt|v)(?!\d{3,})([^A-Za-z0-9]*?)"
                r"(\d{1,2})(?![A-Za-z0-9])",
                re.IGNORECASE)
            versions: list[int] = []
            malformed_attempt = False
            for marker in marker_pattern.finditer(folded):
                if any(start <= marker.start() < end for start, end in release_spans):
                    continue
                parsed = valid_pattern.match(folded, marker.start())
                if (parsed is None
                        or any(sign_character(value) for value in parsed.group(1))
                        or trailing_digit_before_text_or_row(
                            folded, parsed.end(2))):
                    malformed_attempt = True
                else:
                    versions.append(int(parsed.group(2)))
            if malformed_attempt or not versions or set(versions) != {35}:
                errors.append(
                    f"authoritative row:{document}:{row_number}:version:"
                    f"{versions}:malformed={malformed_attempt}")
            if GATE.casefold() not in folded:
                errors.append(f"authoritative row:{document}:{row_number}:gate")
            if re.search(
                    r"\bpass[\s_`-]*pending[\s_`-]*persistence\b", folded) is None:
                errors.append(f"authoritative row:{document}:{row_number}:state")
            triplets, named, malformed = counter_evidence(line)
            if malformed:
                errors.append(
                    f"authoritative row:{document}:{row_number}:malformed-counter:"
                    f"{malformed}")
            expected_named = dict(zip(("semantic", "source", "strict"), expected_counters))
            complete_named = all(named[name] for name in expected_named)
            has_expected = (expected_counters in triplets or (
                complete_named and all(expected_named[name] in named[name]
                                       for name in expected_named)))
            conflicting = (any(counter != expected_counters for counter in triplets)
                           or any(value != expected_named[name]
                                  for name, values in named.items() for value in values))
            if not has_expected or conflicting:
                errors.append(
                    f"authoritative row:{document}:{row_number}:counter:"
                    f"triplets={triplets}:named={named}")
    return errors


def source_policy_source_errors(
        source: str, *, expected_shape: str | None = None,
        tree_override: ast.Module | None = None) -> list[str]:
    tree = ast.parse(source, type_comments=True) if tree_override is None else tree_override
    errors: list[str] = []
    for node in ast.walk(tree):
        if getattr(node, "type_comment", None) is not None:
            errors.append(f"E_TYPE_COMMENT:{node.lineno}")
    for ignore in tree.type_ignores:
        errors.append(f"E_TYPE_IGNORE:{ignore.lineno}:{ignore.tag}")
    forbidden_imports = {"requests", "urllib", "httpx", "socket", "shutil"}
    sensitive_functions = {
        "run_process", "run_git", "atomic_json_last_collect", "load_builder",
    }
    top_level: dict[str, list[ast.FunctionDef | ast.AsyncFunctionDef]] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            top_level.setdefault(node.name, []).append(node)
    direct_sensitive_definition_ids = {
        id(node) for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in sensitive_functions
    }
    for name in sensitive_functions:
        if len(top_level.get(name, [])) > 1:
            errors.append(f"E_POLICY_DUPLICATE_FUNCTION:{name}")
    expected_definitions = {
        "builder": {
            "run_process": 1, "run_git": 1,
            "atomic_json_last_collect": 1, "load_builder": 0,
        },
        "validator": {
            "run_process": 1, "run_git": 1,
            "atomic_json_last_collect": 0, "load_builder": 1,
        },
    }
    expected_import_signatures = {
        "builder": (
            "from __future__ import annotations",
            "import argparse", "import ast", "import hashlib", "import json",
            "import os", "import pathlib", "import subprocess", "import sys",
            "from typing import Any, Iterable",
        ),
        "validator": (
            "from __future__ import annotations",
            "import argparse", "import ast", "import hashlib", "import importlib.util",
            "import json", "import math", "import pathlib", "import re",
            "import subprocess", "import sys", "import unicodedata",
            "from functools import lru_cache", "from typing import Any, Iterable",
            "import copy",
        ),
    }
    allowed_import_statements = set().union(*expected_import_signatures.values())
    import_nodes = sorted(
        (node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))),
        key=lambda node: (node.lineno, node.col_offset))
    if (expected_shape in expected_import_signatures
            and tuple(ast.unparse(node) for node in import_nodes)
            != expected_import_signatures[expected_shape]):
        errors.append(f"E_IMPORT_SIGNATURE:{expected_shape}")
    if expected_shape is not None:
        if expected_shape not in expected_definitions:
            errors.append(f"E_POLICY_UNKNOWN_SHAPE:{expected_shape}")
        else:
            for name, expected_count in expected_definitions[expected_shape].items():
                actual_count = len(top_level.get(name, []))
                if actual_count != expected_count:
                    errors.append(
                        f"E_POLICY_DEFINITION_SET:{name}:{actual_count}!={expected_count}")

    allowed_subprocess_calls: set[int] = set()
    allowed_run_process_calls: set[int] = set()
    allowed_mutator_calls: set[int] = set()
    allowed_loader_calls: set[int] = set()
    allowed_loader_predicates: set[int] = set()
    allowed_sensitive_calls: set[int] = set()
    allowed_filesystem_calls: set[int] = set()
    allowed_getattr_calls: set[int] = set()

    exact_wrapper_hashes = {
        "run_process": {
            "0b1d3e578761533f81677cef85da228d179204cf6bb05f6e4bce19a0baea4dab",
            "e2fffc5996b828c67000c8577d555f14504a2e1721769f32c3bd662bd12ca5ae",
        },
        "run_git": {
            "b340a7fe4cec2568ef544d375a226b2f8a884a01a0e8abb5bcf246b323fa13b8",
        },
    }
    for name, allowed_hashes in exact_wrapper_hashes.items():
        definitions = top_level.get(name, [])
        if len(definitions) == 1:
            wrapper_hash = sha256_bytes(canonical_bytes(stable_ast(definitions[0])))
            if wrapper_hash not in allowed_hashes:
                errors.append(f"E_{name.upper()}_AST")

    process_defs = top_level.get("run_process", [])
    if len(process_defs) == 1:
        process_calls = [node for node in ast.walk(process_defs[0])
                         if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Attribute)
                         and isinstance(node.func.value, ast.Name)
                         and node.func.value.id == "subprocess"
                         and node.func.attr == "run"]
        valid_process = len(process_calls) == 1
        if valid_process:
            call = process_calls[0]
            keywords = {keyword.arg: keyword.value for keyword in call.keywords}
            valid_process = (
                len(call.args) == 1 and isinstance(call.args[0], ast.Name)
                and call.args[0].id == "args"
                and set(keywords) == {"cwd", "capture_output", "check"}
                and isinstance(keywords["cwd"], ast.Name) and keywords["cwd"].id == "ROOT"
                and isinstance(keywords["capture_output"], ast.Constant)
                and keywords["capture_output"].value is True
                and isinstance(keywords["check"], ast.Constant)
                and keywords["check"].value is False)
        if valid_process:
            allowed_subprocess_calls.add(id(process_calls[0]))
        else:
            errors.append("E_RUN_PROCESS_SHAPE")

    git_defs = top_level.get("run_git", [])
    if len(git_defs) == 1:
        process_calls = [node for node in ast.walk(git_defs[0])
                         if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Name)
                         and node.func.id == "run_process"]
        valid_git = len(process_calls) == 1
        if valid_git:
            call = process_calls[0]
            valid_git = (
                len(call.args) == 1 and not call.keywords
                and isinstance(call.args[0], ast.List)
                and len(call.args[0].elts) == 2
                and isinstance(call.args[0].elts[0], ast.Constant)
                and call.args[0].elts[0].value == "git"
                and isinstance(call.args[0].elts[1], ast.Starred)
                and isinstance(call.args[0].elts[1].value, ast.Name)
                and call.args[0].elts[1].value.id == "args")
        if valid_git:
            allowed_run_process_calls.add(id(process_calls[0]))
        else:
            errors.append("E_RUN_GIT_SHAPE")

    loader_defs = top_level.get("load_builder", [])
    if len(loader_defs) == 1:
        loader = loader_defs[0]
        loader_hash = sha256_bytes(canonical_bytes(stable_ast(loader)))
        expected_loader_hash = (
            "dfd5928feeb7e19936d1d5be31d1c7315854c22d8e78734644b1baba6bd579ca")
        loader_calls = sorted((
            node for node in ast.walk(loader)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr in {
                "spec_from_file_location", "module_from_spec", "exec_module",
            }
        ), key=lambda node: (node.lineno, node.col_offset))
        expected_loader_calls = (
            "importlib.util.spec_from_file_location('phase065_step71_builder', BUILDER)",
            "importlib.util.module_from_spec(spec)",
            "spec.loader.exec_module(module)",
        )
        if (loader_hash == expected_loader_hash
                and tuple(ast.unparse(node) for node in loader_calls) == expected_loader_calls):
            allowed_loader_calls.update(id(node) for node in loader_calls)
            spec_predicates = [
                node.args[0] for node in ast.walk(loader)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "require" and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value == "E_BUILDER_SPEC"]
            if (len(spec_predicates) == 1 and ast.unparse(spec_predicates[0])
                    == "spec is not None and spec.loader is not None"):
                allowed_loader_predicates.add(id(spec_predicates[0]))
            else:
                errors.append("E_LOAD_BUILDER_PREDICATE")
        else:
            errors.append("E_LOAD_BUILDER_AST")

    collector_defs = top_level.get("atomic_json_last_collect", [])
    if len(collector_defs) == 1:
        collector = collector_defs[0]
        expected_mutators = {
            "destination.mkdir(parents=True, exist_ok=True)",
            "matrix_temp.write_bytes(canonical_bytes(matrix))",
            "attestation_temp.write_bytes(canonical_bytes(attestation))",
            "os.replace(matrix_temp, matrix_path)",
            "os.replace(attestation_temp, attestation_path)",
        }
        actual_mutators: list[tuple[ast.Call, str]] = []
        for node in ast.walk(collector):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr in {"mkdir", "write_text", "write_bytes", "replace"}:
                actual_mutators.append((node, ast.unparse(node)))
        actual_text = {text for _, text in actual_mutators}
        expected_prefix_source = """def atomic_json_last_collect(output_dir):
    destination = output_dir.resolve()
    repository_results = (ROOT / 'Codex/results').resolve()
    require(destination == repository_results, 'E_REPOSITORY_WRITE_BOUNDARY', str(destination))
    result_status = str(run_git('diff', '--cached', '--name-status', '--', RESULT_PATH)).strip()
    require(result_status == f'A\\t{RESULT_PATH}', 'E_RESULT_NOT_STAGED_FIRST', result_status)
    result_index = bytes(run_git('show', f':{RESULT_PATH}', binary=True))
    require(result_index == (ROOT / RESULT_PATH).read_bytes(), 'E_RESULT_INDEX_WORKTREE')
"""
        expected_prefix = ast.parse(expected_prefix_source).body[0].body
        actual_prefix = collector.body[:len(expected_prefix)]
        prefix_matches = ([ast.dump(node, include_attributes=False) for node in actual_prefix]
                          == [ast.dump(node, include_attributes=False) for node in expected_prefix])
        mutation_after_prefix = (bool(actual_mutators)
                                 and min(node.lineno for node, _ in actual_mutators)
                                 > max(node.end_lineno or node.lineno for node in actual_prefix))
        if actual_text == expected_mutators and prefix_matches and mutation_after_prefix:
            allowed_mutator_calls.update(id(node) for node, _ in actual_mutators)
        else:
            errors.append("E_ATOMIC_COLLECTOR_SHAPE")

    exact_git_contract = {
        "git_blob": ("run_git('rev-parse', f'{BASELINE}:{path}')",),
        "git_raw": ("run_git('cat-file', 'blob', f'{BASELINE}:{path}', binary=True)",),
        "atomic_json_last_collect": (
            "run_git('diff', '--cached', '--name-status', '--', RESULT_PATH)",
            "run_git('show', f':{RESULT_PATH}', binary=True)",
        ),
        "verify_branch_guards": (
            "run_git('rev-parse', '--abbrev-ref', 'HEAD')",
            "run_git('rev-parse', 'HEAD')",
            "run_git('rev-parse', '--abbrev-ref', '@{upstream}')",
            "run_git('rev-parse', '@{upstream}')",
            "run_git('rev-parse', f'refs/remotes/origin/{BRANCH}')",
            "run_git('rev-parse', PROTECTED_BRANCH)",
            "run_git('rev-parse', f'refs/remotes/origin/{PROTECTED_BRANCH}')",
            "run_git('rev-parse', 'refs/remotes/origin/main')",
            "run_git('diff', '--name-only', PROTECTED_TIP, 'HEAD', '--', 'Claude')",
        ),
        "verify_staged": (
            "run_git('diff', '--cached', '--name-status')",
            "run_git('diff', '--name-only')",
            "run_git('status', '--porcelain')",
            "run_git('show', f':{path}', binary=True)",
            "run_git('diff', '--cached', '--check')",
        ),
        "remote_tip": (
            "run_git('ls-remote', '--heads', 'origin', f'refs/heads/{branch}')",
        ),
        "verify_persistence": (
            "run_git('rev-parse', '--abbrev-ref', 'HEAD')",
            "run_git('rev-parse', '--abbrev-ref', '@{upstream}')",
            "run_git('rev-parse', 'HEAD')",
            "run_git('rev-parse', f'{head}^1')",
            "run_git('show', '-s', '--format=%s', head)",
            "run_git('diff-tree', '--no-commit-id', '--name-status', '-r', head)",
            "run_git('rev-parse', '@{upstream}')",
            "run_git('rev-parse', f'refs/remotes/origin/{BRANCH}')",
            "run_git('rev-parse', PROTECTED_BRANCH)",
            "run_git('rev-parse', f'refs/remotes/origin/{PROTECTED_BRANCH}')",
            "run_git('rev-parse', 'refs/remotes/origin/main')",
            "run_git('status', '--porcelain')",
            "run_git('diff', '--name-only', PROTECTED_TIP, head, '--', 'Claude')",
            "run_git('show', f'{head}:{path}', binary=True)",
        ),
    }
    exact_git_caller_hashes = {
        "git_blob": {
            "cdcca16dacdeee9cdb6847e60cdded308ff0e75e66455e79c80e19c0edd31cb7",
            "3022a2b8af4b9df174450105bb85509619648f8156840c3f6f3a96e7a93e7bb4",
        },
        "git_raw": {
            "beeeba17260eb7312eabcc6c3ed243ee76b7bde9397e9eb642373318bd202f9f",
            "66f4ccbcc9b6d3e16d54236c1c80307b4e8ab4c75a5684e73e41fc9f067fc5a1",
        },
        "atomic_json_last_collect": {
            "b98f67d2d28af1f3a88201a20115086f1cf1ba67ffd5e233380a4c0b2719345c",
        },
        "verify_branch_guards": {
            "e45cec3ba063d1eacd4060598639d7b62e28da8c3f3281379912cd0560557118",
        },
        "verify_staged": {
            "8379e066a954b9f475478fa62d86bfdf70eb9f2b988e6819507d8d920bb48db1",
        },
        "remote_tip": {
            "58de1cfd60709288aa8dcb5a7eb48542a71ce303ef976f8de5e5556524707e72",
        },
        "verify_persistence": {
            "8051ad210d75b025d7009373c639e8d8f6a946dd1c7905e47200404f457934ac",
        },
    }
    allowed_git_calls: set[int] = set()
    required_git_callers = {
        "builder": {"git_blob", "git_raw", "atomic_json_last_collect"},
        "validator": {
            "git_blob", "git_raw", "verify_branch_guards", "verify_staged",
            "remote_tip", "verify_persistence",
        },
    }
    for caller, expected_calls in exact_git_contract.items():
        definitions = top_level.get(caller, [])
        if not definitions:
            if caller in required_git_callers.get(expected_shape or "", set()):
                errors.append(f"E_GIT_CALLER_MISSING:{caller}")
            continue
        if len(definitions) != 1:
            errors.append(f"E_GIT_CALLER_DEFINITION_COUNT:{caller}:{len(definitions)}")
            continue
        caller_hash = sha256_bytes(canonical_bytes(stable_ast(definitions[0])))
        if caller_hash not in exact_git_caller_hashes[caller]:
            errors.append(f"E_GIT_CALLER_AST:{caller}")
        calls = sorted((node for node in ast.walk(definitions[0])
                 if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name)
                 and node.func.id == "run_git"),
                       key=lambda node: (node.lineno, node.col_offset))
        actual_calls = tuple(ast.unparse(node) for node in calls)
        if actual_calls != expected_calls:
            errors.append(f"E_GIT_CALL_CONTRACT:{caller}")
        else:
            allowed_git_calls.update(id(node) for node in calls)

    sensitive_application_contract = {
        "builder": ("main", "atomic_json_last_collect(args.output_dir)"),
        "validator": ("validate", "load_builder()"),
    }
    if expected_shape in sensitive_application_contract:
        caller, expected_call = sensitive_application_contract[expected_shape]
        definitions = top_level.get(caller, [])
        calls: list[ast.Call] = []
        if len(definitions) == 1:
            sensitive_name = ("atomic_json_last_collect" if expected_shape == "builder"
                              else "load_builder")
            calls = [node for node in ast.walk(definitions[0])
                     if isinstance(node, ast.Call)
                     and isinstance(node.func, ast.Name)
                     and node.func.id == sensitive_name]
        if len(calls) == 1 and ast.unparse(calls[0]) == expected_call:
            allowed_sensitive_calls.add(id(calls[0]))
        else:
            errors.append(f"E_SENSITIVE_APPLICATION_CONTRACT:{caller}")

    filesystem_sensitive_attributes = {
        "open", "write", "writelines", "truncate", "touch", "replace", "rename",
        "move", "write_text", "write_bytes", "mkdir", "unlink", "rmdir", "remove",
        "rmtree", "symlink_to", "hardlink_to", "link_to", "chmod", "lchmod",
        "copy", "copy_into", "move_into",
    }
    filesystem_read_only_methods = {
        "exists", "is_file", "read_bytes", "read_text", "relative_to", "resolve",
    }
    filesystem_stream_read_methods = {"read"}
    filesystem_read_only_attributes = filesystem_read_only_methods | {
        "anchor", "drive", "name", "parent", "parents", "parts", "root",
        "stem", "suffix", "suffixes",
    }
    safe_nonfilesystem_replace_calls = {
        "path.replace('/v1.0.24/', '/v1.0.24.1/')",
        "raw.replace(b'\\r\\n', b'\\n')",
        "raw.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')",
        "str(RESULT.relative_to(ROOT)).replace('\\\\', '/')",
        "stale_row.replace(token, value)",
        "parent_text.replace(parent_line, parent_line.replace(f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}/{STRICT_JSON_CASES}`', f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}`'))",
        "parent_line.replace(f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}/{STRICT_JSON_CASES}`', f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}`')",
        "parent_text.replace(f'semantic/source-policy/strict-JSON `{current_counters[0]}/{current_counters[1]}/{current_counters[2]}`', f'semantic/source-policy `{current_counters[0]}/{current_counters[1]}`')",
        "positive_row.replace(token, value)",
        "line[3:].replace('\\\\', '/')",
    }

    def direct_read_only_open_call(node: ast.Call) -> bool:
        direct_builtin = isinstance(node.func, ast.Name) and node.func.id == "open"
        direct_path_method = isinstance(node.func, ast.Attribute) and node.func.attr == "open"
        if not (direct_builtin or direct_path_method):
            return False
        if (any(isinstance(argument, ast.Starred) for argument in node.args)
                or any(keyword.arg is None for keyword in node.keywords)):
            return False
        positional_index = 1 if direct_builtin else 0
        mode_values = list(node.args[positional_index:positional_index + 1])
        mode_values.extend(keyword.value for keyword in node.keywords
                           if keyword.arg == "mode")
        if not mode_values:
            return True
        return (len(mode_values) == 1
                and isinstance(mode_values[0], ast.Constant)
                and isinstance(mode_values[0].value, str)
                and mode_values[0].value in {"r", "rb", "rt", "br", "tr"})

    def direct_literal_getattr_call(node: ast.Call) -> bool:
        return (
            isinstance(node.func, ast.Name) and node.func.id == "getattr"
            and len(node.args) in {2, 3} and not node.keywords
            and not any(isinstance(argument, ast.Starred) for argument in node.args)
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str))

    path_sensitive_names = {
        "ROOT", "BUILDER", "VALIDATOR", "MATRIX", "ATTESTATION", "RESULT",
        "PARENT_LEDGER", "CANONICAL_LEDGER", "HANDOVER", "destination",
        "output_dir", "matrix_temp", "attestation_temp", "matrix_path",
        "attestation_path", "resolved", "path",
    }

    path_constructor_names = {
        "Path", "PurePath", "PurePosixPath", "PureWindowsPath",
        "PosixPath", "WindowsPath",
    }
    path_returning_methods = {
        "absolute", "cwd", "expanduser", "home", "joinpath", "relative_to",
        "resolve", "with_name", "with_stem", "with_suffix",
    }

    def path_name_convention(name: str) -> bool:
        folded = name.casefold()
        return (folded in {"path", "filepath"}
                or folded.endswith(("_path", "_file")))

    path_sensitive_names.update(
        node.id for node in ast.walk(tree)
        if isinstance(node, ast.Name) and path_name_convention(node.id))

    def path_name_is_sensitive(name: str) -> bool:
        return name in path_sensitive_names or name in path_constructor_names

    def path_constructor_reference(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
            and node.id in path_constructor_names
            or isinstance(node, ast.Attribute)
            and isinstance(node.ctx, ast.Load)
            and isinstance(node.value, ast.Name) and node.value.id == "pathlib"
            and node.attr in path_constructor_names)

    def path_sensitive_value_expression(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return isinstance(node.ctx, ast.Load) and path_name_is_sensitive(node.id)
        if path_constructor_reference(node):
            return True
        if isinstance(node, ast.Attribute):
            return path_sensitive_value_expression(node.value)
        if isinstance(node, ast.Subscript):
            return (path_sensitive_value_expression(node.value)
                    or path_sensitive_value_expression(node.slice))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return (path_sensitive_value_expression(node.left)
                    or path_sensitive_value_expression(node.right))
        if isinstance(node, ast.BoolOp):
            return any(path_sensitive_value_expression(value) for value in node.values)
        if isinstance(node, ast.IfExp):
            return (path_sensitive_value_expression(node.body)
                    or path_sensitive_value_expression(node.orelse))
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return any(path_sensitive_value_expression(value) for value in node.elts)
        if isinstance(node, ast.Dict):
            return (any(key is not None and path_sensitive_value_expression(key)
                        for key in node.keys)
                    or any(path_sensitive_value_expression(value)
                           for value in node.values))
        if isinstance(node, (ast.Starred, ast.NamedExpr)):
            return path_sensitive_value_expression(node.value)
        if isinstance(node, ast.Slice):
            return any(value is not None and path_sensitive_value_expression(value)
                       for value in (node.lower, node.upper, node.step))
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            return (path_sensitive_value_expression(node.elt)
                    or any(path_sensitive_value_expression(generator.iter)
                           or any(path_sensitive_value_expression(condition)
                                  for condition in generator.ifs)
                           for generator in node.generators))
        if isinstance(node, ast.DictComp):
            return (path_sensitive_value_expression(node.key)
                    or path_sensitive_value_expression(node.value)
                    or any(path_sensitive_value_expression(generator.iter)
                           or any(path_sensitive_value_expression(condition)
                                  for condition in generator.ifs)
                           for generator in node.generators))
        if isinstance(node, ast.Call):
            if path_constructor_reference(node.func):
                return True
            return (isinstance(node.func, ast.Attribute)
                    and node.func.attr in path_returning_methods
                    and path_sensitive_value_expression(node.func.value))
        return False

    def path_sensitive_receiver(node: ast.AST) -> bool:
        return path_sensitive_value_expression(node)

    def direct_literal_path_constructor_call(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Call) and path_constructor_reference(node.func)
            and len(node.args) == 1 and not node.keywords
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str))

    alias_values: dict[str, list[ast.AST]] = {}
    for current in ast.walk(tree):
        value: ast.AST | None = None
        targets: list[ast.AST] = []
        if isinstance(current, ast.Assign):
            value = current.value
            targets = list(current.targets)
        elif isinstance(current, ast.AnnAssign) and current.value is not None:
            value = current.value
            targets = [current.target]
        if value is None:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                alias_values.setdefault(target.id, []).append(value)

    changed = True
    while changed:
        changed = False
        for name, values in alias_values.items():
            if path_name_is_sensitive(name):
                continue
            if any(path_sensitive_value_expression(value) for value in values):
                path_sensitive_names.add(name)
                changed = True

    allowed_filesystem_calls.update(allowed_mutator_calls)
    for current in ast.walk(tree):
        if not isinstance(current, ast.Call):
            continue
        if direct_literal_getattr_call(current):
            allowed_getattr_calls.add(id(current))
        if (direct_read_only_open_call(current)
                or ast.unparse(current) in safe_nonfilesystem_replace_calls
                or (isinstance(current.func, ast.Attribute)
                    and current.func.attr in filesystem_read_only_methods
                    and path_sensitive_receiver(current.func.value))
                or (isinstance(current.func, ast.Attribute)
                    and current.func.attr in filesystem_stream_read_methods
                    and isinstance(current.func.value, ast.Call)
                    and direct_read_only_open_call(current.func.value))):
            allowed_filesystem_calls.add(id(current))

    pinned_path_statement_sha256 = {
        "builder": set("""
af7e9102dbdfe0e0e391726a5c2814c3b45a3ff1689179801250542281e463be
41b4e866c0fb9c9593482b9dee325d3826950d753ef0b97e968ac8bf4cb85c2e
d8d8ed564372d6deb997a358c4c0d9d40890eb83baf606db1c547d95d19eb3d3
653f216bb9743c5bffdd95c054b486f62ddc8e2274000d5dcae1dee6bf0f1ff9
a50de54a6ea705c80ff26327753665148f0399151f0b658543f7271cf461afcd
72895811c43b3e578e7cfe7962a23e809c58e3be4f09283f17c6f453756f2f84
2f7a420d7f8e3af09eabcc4206ee5743810156dab3322f85a3de1ffd49d280fd
55ba6f0d2c2e7ac6f42be20bc1bb5f96a7f998e2711bcf3cdfc8cd70ae880b1c
aa98e288bfff5d183639c82b09d838920bbd4ae86a857aef376b9c24d7427069
5c47486dcb76903f66d11934bc147be0beb81ea0e96ceb6488621f72dacd979d
30e35dd297bf35b2bcd88f22b843355fae0621f83406b6aa1b102fb2227f343c
57829586ed2aa06648fc60d850872bd7f9c0a5fcb7c61c4fd5a29fdfe9c07687
44b75c28a7a18e6351ca7c20b1f5cc9fb9bf7de9d2dc2e50de53a0b53089c816
ec977af1e90198774463598d279d22173d36523a77187c6c8409e4aa680e42d7
e49d3fe68ff7178bddbcd94c9d94e9336d60e9de6830e07a790a37b6738f5eef
9c449d03a75efeb03853cc8de34a34a3d39d1a1ccf595493b6acb40d171d1ba3
459fd3d25c9c9e730ce42545b07fdd96fd20e59f9d4749c1c12dc410f0b94c02
70200f124280f86c8a0a3e9bdbd0d3f4d166e723c65a6582645d85fcaa42d356
d36810ac6f154e619d2d8f1c56bde55bd12f8105526673aa9c3b1f1d26c63310
5185fb7b5d3e4bc0a0528f549e310659606f47a4da4f6c9b2df7e8af751e7beb
27d818337090f65fc3abdc354e3f06c3bb703b07a0eb6bc6460a020885eb0750
f10c27b562586b63d43250c4d338c86c13b12060e4f01ece3870f44df5094dd5
4bd78c18df898699c566d05c1f2e3eb539937ccc2c0901f49c415dbb93f004fe
e04620f2da43d94680d15058dad6bccee587843cec725168fabc8fb2ed52c27d
67887e5008c4cd45ea2244bd803a0e21d80f359f3ce6baefd6adc534c7343ede
55ebe9263c0d80947bb188aed162956f9f3b36111c1d2dea75a30a5a2f82ad1c
20bd8233b3064ccac817315497b53e2a9d498fcccfbeed68595872fb22f85e56
5909c50c8451ec8df413115e7b5897ddc19a7d95ece5b9ab97a1dd0cc46872cf
13100ddfe10463c93064852c37220205a9a809b28633babffca5c988ac17c18b
f086680bbe40060efd71e9f2340d776a3112bcbe4e1fa06d2204bef98a170e0c
de3b0fbaa3b6d4559d67dc6fd8dd0ebce831314b3787747cfa3353c7354ce7e0
7a4b80a9d7fc86157c1d51117eaf973ca417996261519aad9a49ed76d79059e9
b3f455b410eb8739f61ff6881ceaa057f4fa3c5846eb23feba3527bf4513935f
6f4631ba34a045deba355d06c3ba7271e54d5ccfa035f2e668534eb7a1e42a5f
15362374542a90924c3d9a330d0a43faa04eb1c991bb6c89504815986627c47f
a9b11373a02f1dfc22e4026785810bf099cec5bdec26c793cd5c399d83df4b4b
b98f67d2d28af1f3a88201a20115086f1cf1ba67ffd5e233380a4c0b2719345c
b8cc383bc1a6b7ca7131e1c4478145c177afa10ad12a2b2b4ddcca36b29dbd53
2c5f7db6aa589798fb676965d7adf1c384b1d68cb72000894126c9f6b35aab60
04d7e3693c26618bc757a364637649eb11929b5359d9a7638c5c9a94235d5b90
""".split()),
        "validator": set("""
598b21f1f6348066f90ba3fd6874fa60f7c7c77210e609109562cf9343682ca4
1223051606e49938884f6afaa03ce87f6f3dc08ae37ca130d4bfbdc70b52da93
120571dc53e585c83536249b853397b1f1bddfca36ae05eee01ae5fc0b1e8306
26c5a2a586999e6ceda984198f56aba5f6a0f4f30278a486fe47fa51806fe7c9
9f1259d94c9ce34a650b1394571e93a61b219d48b27bced6596b96fe8f2442c4
ef31f962e633d363eddeceb2f7873f5c782ebb0cd181b8752e5dd6596d708700
566286781dc4bca3ae4711d6a8f18d4ffc22df95859b4ffec585e12c490fcb04
365178669dd374132168ba922e280d097ef14c120050aa5023924b1d2176c764
5c33ee50e6d48c4a600e54fc16ecab946ee4788a21996b194afbf6043829d307
226039ebf38187ce2dd5fb10f23fadb9a840c4f6a11207f5e40f232061633047
6fafea1b8d59b24f29818f7cc6c1e6db40a2841fb0faf3f1b4d94be0addb0360
045b2190d5c4546b18a1cfa9fb1dddc2e58b338c96871542c9ea5dfd3a31f182
db47dabef51b1dd09a9123875880cfc13c4da32016b0737c3e9b46f4bfaf25d5
2f7a420d7f8e3af09eabcc4206ee5743810156dab3322f85a3de1ffd49d280fd
2b2160372edd5e42d53419f5376e5bf15602722040d1cb50a040610133b68f33
e2acacf12bea6bf5a91c760568dd361d28cebfd74eb2b26040a4afa9212d4406
20d7cc34c4ae02e483c438c2b7ddd16a034f8c9fcb9c8a2b11c86dd58d51aea3
5d457f22eb887bc5dd15c7fe5d6207a6bab772112b5b98ae6098ac1fa7fb242f
adf3b28140b52817a905a7c311ec686a518284274f3f1e18904dd91fc67809aa
7108ad580fe6c76cab21318c09cfe4d8a893f78b4fedb89d1bb5fad459af09f9
d6c8e1539a1dc643f10e5e9d52537615332cc5ad3be221bb57e5e331cbd9d780
bd7246c688f7d94cbcba6acce3b954fdb078245f3db45b1764c66cf0d4c65833
00f11512e1484284c1099f09591ec3c651e6cc8fe9171988d73a24906a557b49
ac2c0374df716083ce5f4419ea834b6d4a10be116776e9ce498678ab5898bc50
3f6f0578b820647b685217362642b77425385dd9b44b1dd9004bcc9b5a5a2316
3e6e17fbe39a0bd74fd384cf397f79f3a464ef9a05cd5df2a820a55e34673862
08c3d60b6bf894efbc06f89452c7538b66400b09da73033066639ea100c2dfec
8d10d0a864119378d86e71ff2503e0d33467f37312deb5d7efc360612b247d95
d8378bb4bccdce3551fdb5052b5fc279d46786f36d6a9ac6148550e25859dc10
f8f07b011f6f35b407111ee3b9e3aac1aecc4b9c3233ecc1ed8eaac676ed4289
1aefae5ff0a859015d9284256616caa9322158a1aa3c98502df2c7b993783181
c5177d6db00d29154d74b57f710ab2947d4a92b20d0f20cc105777e639f30649
c3e228b40a67fd2086503610267aab530d548752ba8a4bc7027754188f2bfe76
7142cc5ffa9419c23b158f9633cd12da556d9f1f33fc59afe66488d13091a499
e59fb5564242fa59bed677a93cb708b31e71838cf63f1ccd4b8cc0b6e50d3159
5228aad5010e5106f792249ec98090b8ee6cd2b1291b491fb6efbd8bc57ba3a3
70200f124280f86c8a0a3e9bdbd0d3f4d166e723c65a6582645d85fcaa42d356
d36810ac6f154e619d2d8f1c56bde55bd12f8105526673aa9c3b1f1d26c63310
79d0567e6d1f264e14f925340e35e2733a276f01f43710dfb3f8ff7242b107a6
27d818337090f65fc3abdc354e3f06c3bb703b07a0eb6bc6460a020885eb0750
ab61966efb62ee16e41e80958108b96df6ab35aa5af815dc0163ee845c61871f
d6811b7d25005f52e5a350231621878906174a9a24701de30fca2c419469baf0
08c3d60b6bf894efbc06f89452c7538b66400b09da73033066639ea100c2dfec
8d10d0a864119378d86e71ff2503e0d33467f37312deb5d7efc360612b247d95
ba33243911a543dda4e41522141f1fa30c2e9a4c6179aabe9c9c1c9a3db30eee
a06b913601013675c2eb91518d1dc0af964fc539323414a5582fc634bc64110d
ca6087098f5e136eff7f6165b4db5d8287e48fc8893d449b74c01e7cd2e6c20e
609ccfc0233bb755fdd0043ff4c7c752868664feb037c4a3625ae2cf022cd7ed
55ebe9263c0d80947bb188aed162956f9f3b36111c1d2dea75a30a5a2f82ad1c
e04620f2da43d94680d15058dad6bccee587843cec725168fabc8fb2ed52c27d
7916fe1026a631821f86e68b095e2e59be5484760b9612561af9fbef3189981e
2b85c95af3429859fdf64b5e11b57d41ff2d29cd15432bba9370382abd67eafb
dbb3547c2651ea293429082595a780e9ecddb1fb479fbbd4b48182d292b49600
6792f88a79c1a0edee8197b3abf374166daa4c8b37dfafb9ea47cfeafeee3939
5909c50c8451ec8df413115e7b5897ddc19a7d95ece5b9ab97a1dd0cc46872cf
13100ddfe10463c93064852c37220205a9a809b28633babffca5c988ac17c18b
99a0998b3cd67b5750685bebcb0a3f5f7451ee4522ae9dbf905b12757996f504
fadabaeeab895b88ae2c88268f1139bbfaab80c04434d6ea0bab2573692ea14c
5d30b699fe224da09afe86174d3077919b2840dfb651f4ef407395eaffd3666f
65e4781e28e6fcd08859a1db8442a367f0fad2f89b8c84838c7d4067785a7a9c
f086680bbe40060efd71e9f2340d776a3112bcbe4e1fa06d2204bef98a170e0c
a9ca7cf2aa601153c489fda7db37eb4439cd6b779fa73dd411ea8e2527a01924
3e6e17fbe39a0bd74fd384cf397f79f3a464ef9a05cd5df2a820a55e34673862
061b57ad512e47f4f823c5c5eea9ce2e529976f43448b45b6dccd4b5f3f157e9
a9b11373a02f1dfc22e4026785810bf099cec5bdec26c793cd5c399d83df4b4b
482f68460bac8a7bfef21e213689f78ec6f220d7ad9d6838882e31d0553fac78
8b0d248cf01dd69c5d30dd112fc6fd8874567141096e9835589d722ec43d3b44
78185ad2148a7d6869a6fcae84917111976a647e8bf9318448310d4719441c41
dcbd475d2d5570ad20337c3d54f87af7c54426a0a34f0d63b17a9ad81cc3f189
3aeb9c15e28edb0cac8c4ca5741f97f402b711b11d2dc25a0274482de3ad5ed8
""".split()),
    }
    statement_parents = {
        id(child): parent for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }

    def nearest_statement(node: ast.AST) -> ast.stmt | None:
        current = node
        while id(current) in statement_parents and not isinstance(current, ast.stmt):
            current = statement_parents[id(current)]
        return current if isinstance(current, ast.stmt) else None

    statement_hash_counts: dict[str, int] = {}
    for statement in (node for node in ast.walk(tree) if isinstance(node, ast.stmt)):
        statement_hash = sha256_bytes(canonical_bytes(stable_ast(statement)))
        statement_hash_counts[statement_hash] = statement_hash_counts.get(statement_hash, 0) + 1
    pinned_statement_hashes = pinned_path_statement_sha256.get(expected_shape or "", set())
    pinned_statement_counts = {
        "builder": {
            "f10c27b562586b63d43250c4d338c86c13b12060e4f01ece3870f44df5094dd5": 2,
            "e04620f2da43d94680d15058dad6bccee587843cec725168fabc8fb2ed52c27d": 2,
        },
        "validator": {
            "1aefae5ff0a859015d9284256616caa9322158a1aa3c98502df2c7b993783181": 2,
            "a06b913601013675c2eb91518d1dc0af964fc539323414a5582fc634bc64110d": 4,
            "65e4781e28e6fcd08859a1db8442a367f0fad2f89b8c84838c7d4067785a7a9c": 2,
        },
    }
    if expected_shape in pinned_path_statement_sha256:
        bad_contract = sorted(
            statement_hash for statement_hash in pinned_statement_hashes
            if statement_hash_counts.get(statement_hash)
            != pinned_statement_counts.get(expected_shape, {}).get(statement_hash, 1))
        if bad_contract:
            errors.append(f"E_FS_PATH_CONTEXT_CONTRACT:{expected_shape}:{bad_contract}")

    allowed_path_value_ids: set[int] = set()
    for current in ast.walk(tree):
        if (not isinstance(current, ast.expr)
                or not path_sensitive_value_expression(current)):
            continue
        statement = nearest_statement(current)
        if (statement is not None
                and sha256_bytes(canonical_bytes(stable_ast(statement)))
                in pinned_statement_hashes):
            allowed_path_value_ids.add(id(current))
    path_safe_calls = (
        allowed_mutator_calls | allowed_loader_calls
        | allowed_subprocess_calls | allowed_run_process_calls)
    for current in ast.walk(tree):
        if not isinstance(current, ast.Call) or id(current) not in path_safe_calls:
            continue
        for descendant in ast.walk(current):
            if (isinstance(descendant, ast.expr)
                    and path_sensitive_value_expression(descendant)):
                allowed_path_value_ids.add(id(descendant))
    for current in ast.walk(tree):
        if (not isinstance(current, ast.Call)
                or not direct_read_only_open_call(current)
                or not isinstance(current.func, ast.Attribute)
                or current.func.attr != "open"
                or not direct_literal_path_constructor_call(current.func.value)):
            continue
        for descendant in ast.walk(current.func):
            if (isinstance(descendant, ast.expr)
                    and path_sensitive_value_expression(descendant)):
                allowed_path_value_ids.add(id(descendant))
    for current in ast.walk(tree):
        if (isinstance(current, ast.expr)
                and path_sensitive_value_expression(current)
                and id(current) not in allowed_path_value_ids):
            errors.append(f"E_FS_PATH_ESCAPE:{getattr(current, 'lineno', 0)}")

    allowed_in_place_calls = (
        allowed_subprocess_calls | allowed_run_process_calls | allowed_mutator_calls
        | allowed_loader_calls | allowed_sensitive_calls | allowed_git_calls
        | allowed_filesystem_calls)
    allowed_sensitive_expression_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and id(node) in allowed_in_place_calls:
            allowed_sensitive_expression_ids.update(id(part) for part in ast.walk(node.func))
        if isinstance(node, ast.Call) and id(node) in allowed_getattr_calls:
            allowed_sensitive_expression_ids.update(id(part) for part in ast.walk(node.func))
        if id(node) in allowed_loader_predicates:
            allowed_sensitive_expression_ids.update(id(part) for part in ast.walk(node))

    def dynamic_namespace_reference(node: ast.AST) -> bool:
        namespace_names = {
            "globals", "locals", "vars", "builtins", "__builtins__",
            "__globals__", "f_globals", "f_locals", "_getframe", "currentframe",
            "__getattribute__",
        }
        for current in ast.walk(node):
            if (isinstance(current, ast.Name) and isinstance(current.ctx, ast.Load)
                    and current.id in namespace_names):
                return True
            if (isinstance(current, ast.Attribute) and current.attr in namespace_names
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(current.value))):
                return True
            if (isinstance(current, ast.Subscript)
                    and isinstance(current.slice, ast.Constant)
                    and current.slice.value in namespace_names
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(current.value))):
                return True
            if (isinstance(current, ast.Call) and isinstance(current.func, ast.Name)
                    and current.func.id == "getattr" and len(current.args) >= 2
                    and isinstance(current.args[1], ast.Constant)
                    and current.args[1].value in namespace_names
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(current.args[0]))):
                return True
        return False

    sensitive_target_names = sensitive_functions | {
        "subprocess", "os", "importlib", "builtins", "__builtins__", "sys",
    }
    prohibited_external_roots = {
        "requests", "urllib", "httpx", "socket", "ssl", "http", "ftplib",
        "smtplib", "imaplib", "poplib", "telnetlib", "multiprocessing", "asyncio",
    }
    sensitive_namespace_attributes = {
        "__globals__", "f_globals", "f_locals", "_getframe", "currentframe",
        "__getattribute__", "modules",
    }

    def sensitive_target_reference(target: ast.AST) -> bool:
        for current in ast.walk(target):
            if isinstance(current, ast.Name) and current.id in sensitive_target_names:
                return True
            if (isinstance(current, ast.Attribute)
                    and current.attr in sensitive_namespace_attributes):
                return True
        return False

    def sensitive_mutation_arguments(node: ast.Call) -> bool:
        mutator_names = {
            "setattr", "delattr", "mutate", "setitem", "__setitem__",
            "__setattr__", "__delattr__", "update", "append", "extend",
            "insert", "pop", "remove", "clear",
        }
        function_name = (node.func.id if isinstance(node.func, ast.Name)
                         else node.func.attr if isinstance(node.func, ast.Attribute)
                         else None)
        if function_name not in mutator_names:
            return False
        values = [*node.args, *(keyword.value for keyword in node.keywords)]
        if any(sensitive_target_reference(value) for value in values):
            return True
        if isinstance(node.func, ast.Attribute):
            if sensitive_target_reference(node.func.value):
                return True
        return False

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.functions: list[str] = []

        @property
        def function(self) -> str:
            return self.functions[-1] if self.functions else "<module>"

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if (node.name in sensitive_functions
                    and id(node) not in direct_sensitive_definition_ids):
                errors.append(f"E_POLICY_NESTED_FUNCTION:{node.lineno}")
            self.check_function_captures(node)
            self.functions.append(node.name)
            for statement in node.body:
                self.visit(statement)
            self.functions.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            if (node.name in sensitive_functions
                    and id(node) not in direct_sensitive_definition_ids):
                errors.append(f"E_POLICY_NESTED_FUNCTION:{node.lineno}")
            self.check_function_captures(node)
            self.functions.append(node.name)
            for statement in node.body:
                self.visit(statement)
            self.functions.pop()

        def check_arguments(self, arguments: ast.arguments, lineno: int) -> None:
            all_arguments = (
                list(arguments.posonlyargs) + list(arguments.args)
                + list(arguments.kwonlyargs)
                + ([arguments.vararg] if arguments.vararg is not None else [])
                + ([arguments.kwarg] if arguments.kwarg is not None else [])
            )
            if any(argument.arg in sensitive_functions for argument in all_arguments):
                errors.append(f"E_PROTECTED_BINDING:{lineno}")
            for argument in all_arguments:
                self.check_annotation(argument.annotation, lineno)
            defaults = list(arguments.defaults) + [
                default for default in arguments.kw_defaults if default is not None]
            if any(self.captured_sensitive_reference(default) for default in defaults):
                errors.append(f"E_EXEC_CAPTURE:{lineno}")
            for default in defaults:
                self.visit(default)

        def check_annotation(self, annotation: ast.AST | None, lineno: int) -> None:
            if annotation is None:
                return
            if self.captured_sensitive_reference(annotation):
                errors.append(f"E_EXEC_CAPTURE:{lineno}")
            self.visit(annotation)

        def check_type_parameters(self, owner: ast.AST, lineno: int) -> None:
            for parameter in getattr(owner, "type_params", []):
                if getattr(parameter, "name", None) in sensitive_functions:
                    errors.append(f"E_PROTECTED_BINDING:{lineno}")
                self.check_annotation(getattr(parameter, "bound", None), lineno)
                self.check_annotation(getattr(parameter, "default_value", None), lineno)

        def check_function_captures(
                self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            self.check_arguments(node.args, node.lineno)
            self.check_type_parameters(node, node.lineno)
            if any(self.captured_sensitive_reference(decorator)
                   for decorator in node.decorator_list):
                errors.append(f"E_EXEC_CAPTURE:{node.lineno}")
            for decorator in node.decorator_list:
                self.visit(decorator)
            self.check_annotation(node.returns, node.lineno)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            self.check_arguments(node.args, node.lineno)
            if self.captured_sensitive_reference(node.body):
                errors.append(f"E_EXEC_ESCAPE:{node.lineno}")
            self.visit(node.body)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            if node.name in sensitive_functions:
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")
            if any(self.captured_sensitive_reference(item)
                   for item in [*node.bases, *node.keywords, *node.decorator_list]):
                errors.append(f"E_EXEC_CAPTURE:{node.lineno}")
            self.check_type_parameters(node, node.lineno)
            self.generic_visit(node)

        def visit_Import(self, node: ast.Import) -> None:
            if ast.unparse(node) not in allowed_import_statements:
                errors.append(f"E_IMPORT_UNAPPROVED:{node.lineno}")
            if any(alias.name.split(".")[0] in forbidden_imports for alias in node.names):
                errors.append(f"E_IMPORT_FORBIDDEN:{node.lineno}")
            if any(alias.name.split(".")[0] in {"operator", "_operator"}
                   for alias in node.names):
                errors.append(f"E_IMPORT_OPERATOR:{node.lineno}")
            if any(alias.name.split(".")[0] == "builtins" for alias in node.names):
                errors.append(f"E_IMPORT_BUILTINS:{node.lineno}")
            if any(alias.name.split(".")[0] in {"subprocess", "os", "builtins", "importlib"}
                   and alias.asname is not None
                   for alias in node.names):
                errors.append(f"E_IMPORT_EXECUTION_ALIAS:{node.lineno}")
            if any((alias.asname or alias.name.split(".")[0]) in sensitive_functions
                   for alias in node.names):
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            if ast.unparse(node) not in allowed_import_statements:
                errors.append(f"E_IMPORT_UNAPPROVED:{node.lineno}")
            if (node.module or "").split(".")[0] in forbidden_imports:
                errors.append(f"E_IMPORT_FORBIDDEN:{node.lineno}")
            if (node.module or "").split(".")[0] in {"operator", "_operator"}:
                errors.append(f"E_IMPORT_OPERATOR:{node.lineno}")
            if (node.module or "").split(".")[0] in {"subprocess", "os", "builtins", "importlib"}:
                errors.append(f"E_IMPORT_FROM_EXECUTION:{node.lineno}")
            if any((alias.asname or alias.name) in sensitive_functions for alias in node.names):
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")

        @classmethod
        def sensitive_reference(cls, value: ast.AST) -> bool:
            if isinstance(value, ast.Name):
                return value.id in {
                    *sensitive_functions, "run", "Popen", "system", "popen", "replace",
                    "open",
                    "getattr", "operator", "_operator", "attrgetter", "methodcaller",
                    "subprocess", "os", "builtins", "__builtins__", "globals", "locals",
                    "vars", "importlib", "import_module", "__import__",
                     "eval", "exec", "compile",
                     "_getframe", "currentframe", "f_globals", "f_locals",
                     *prohibited_external_roots,
                 }
            if isinstance(value, ast.Attribute):
                if (isinstance(value.value, ast.Name)
                        and (value.value.id, value.attr) == ("sys", "modules")):
                    return True
                if value.attr in {
                    "spec_from_file_location", "module_from_spec", "exec_module", "loader",
                    *filesystem_sensitive_attributes,
                    "__globals__", "f_globals", "f_locals", "_getframe", "currentframe",
                    "__getattribute__", "modules", "attrgetter", "methodcaller",
                }:
                    return True
                return cls.sensitive_reference(value.value)
            if isinstance(value, ast.Subscript):
                literal_key = value.slice.value if isinstance(value.slice, ast.Constant) else None
                return (literal_key in {
                    "loader", "exec_module", "spec_from_file_location", "module_from_spec",
                    "__globals__", "f_globals", "f_locals", "_getframe", "currentframe",
                    "__getattribute__", "modules",
                } or cls.sensitive_reference(value.value))
            if isinstance(value, (ast.Tuple, ast.List, ast.Set)):
                return any(cls.sensitive_reference(item) for item in value.elts)
            if isinstance(value, ast.Dict):
                return any(cls.sensitive_reference(item) for item in value.keys + value.values
                           if item is not None)
            if isinstance(value, ast.Call):
                if id(value) in allowed_in_place_calls:
                    return False
                if id(value) in allowed_getattr_calls:
                    attribute = value.args[1].value
                    return (attribute in {
                        "modules", "loader", "exec_module", "spec_from_file_location",
                        "module_from_spec", "__globals__", "f_globals", "f_locals",
                        "_getframe", "currentframe", "__getattribute__",
                    } or cls.sensitive_reference(value.args[0])
                            or (isinstance(value.args[0], ast.Name)
                                and value.args[0].id == "sys"))
                if (isinstance(value.func, ast.Name) and value.func.id == "vars"
                        and value.args and (cls.sensitive_reference(value.args[0])
                                            or (isinstance(value.args[0], ast.Name)
                                                and value.args[0].id == "sys"))):
                    return True
                if (isinstance(value.func, ast.Name) and value.func.id == "getattr"
                        and value.args):
                    attribute = (value.args[1].value if len(value.args) >= 2
                                 and isinstance(value.args[1], ast.Constant) else None)
                    if (attribute in {
                            "modules", "loader", "exec_module", "spec_from_file_location",
                            "module_from_spec",
                    } or cls.sensitive_reference(value.args[0])
                            or (isinstance(value.args[0], ast.Name)
                                and value.args[0].id == "sys")):
                        return True
                return cls.sensitive_reference(value.func)
            return False

        @classmethod
        def captured_sensitive_reference(cls, value: ast.AST) -> bool:
            def captured(node: ast.AST) -> bool:
                if id(node) in allowed_loader_predicates:
                    return False
                if isinstance(node, ast.Call) and id(node) in allowed_in_place_calls:
                    return (any(captured(argument) for argument in node.args)
                            or any(captured(keyword.value) for keyword in node.keywords))
                if isinstance(node, ast.Call) and id(node) in allowed_getattr_calls:
                    return (cls.sensitive_reference(node)
                            or any(captured(argument) for argument in node.args)
                            or any(captured(keyword.value) for keyword in node.keywords))
                if cls.sensitive_reference(node):
                    return True
                return any(captured(child) for child in ast.iter_child_nodes(node))

            return captured(value)

        def visit_Name(self, node: ast.Name) -> None:
            if (isinstance(node.ctx, ast.Load)
                    and node.id in prohibited_external_roots):
                errors.append(f"E_EXEC_UNAPPROVED_ROOT:{node.lineno}")
            if (isinstance(node.ctx, ast.Load)
                    and node.id in {
                        "globals", "locals", "vars", "builtins", "__builtins__",
                    }):
                errors.append(f"E_DYNAMIC_NAMESPACE:{node.lineno}")
            if (isinstance(node.ctx, ast.Load)
                    and id(node) not in allowed_sensitive_expression_ids
                    and self.sensitive_reference(node)):
                errors.append(f"E_EXEC_SENSITIVE_LOAD:{getattr(node, 'lineno', 0)}")
            if isinstance(node.ctx, (ast.Store, ast.Del)) and node.id in sensitive_functions:
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if (isinstance(node.ctx, ast.Load)
                    and path_sensitive_receiver(node.value)
                    and node.attr not in filesystem_read_only_attributes | {"open"}
                    and id(node) not in allowed_sensitive_expression_ids):
                errors.append(f"E_EXEC_SENSITIVE_LOAD:{getattr(node, 'lineno', 0)}")
            if (isinstance(node.ctx, ast.Load)
                    and id(node) not in allowed_sensitive_expression_ids
                    and self.sensitive_reference(node)):
                errors.append(f"E_EXEC_SENSITIVE_LOAD:{getattr(node, 'lineno', 0)}")
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            if (isinstance(node.ctx, ast.Load)
                    and id(node) not in allowed_sensitive_expression_ids
                    and self.sensitive_reference(node)):
                errors.append(f"E_EXEC_SENSITIVE_LOAD:{getattr(node, 'lineno', 0)}")
            self.generic_visit(node)

        def visit_Global(self, node: ast.Global) -> None:
            if any(name in sensitive_functions for name in node.names):
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")

        def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
            if any(name in sensitive_functions for name in node.names):
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")

        def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
            if node.name in sensitive_functions:
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")
            self.generic_visit(node)

        def visit_MatchAs(self, node: ast.MatchAs) -> None:
            if node.name in sensitive_functions:
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")
            self.generic_visit(node)

        def visit_MatchStar(self, node: ast.MatchStar) -> None:
            if node.name in sensitive_functions:
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")
            self.generic_visit(node)

        def visit_MatchMapping(self, node: ast.MatchMapping) -> None:
            if node.rest in sensitive_functions:
                errors.append(f"E_PROTECTED_BINDING:{node.lineno}")
            self.generic_visit(node)

        def visit_Assign(self, node: ast.Assign) -> None:
            if any(sensitive_target_reference(target) for target in node.targets):
                errors.append(f"E_SENSITIVE_TARGET:{node.lineno}")
            if self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_ALIAS_SUBPROCESS:{node.lineno}")
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            if sensitive_target_reference(node.target):
                errors.append(f"E_SENSITIVE_TARGET:{node.lineno}")
            if self.captured_sensitive_reference(node.annotation):
                errors.append(f"E_EXEC_CAPTURE:{node.lineno}")
            if node.value is not None and self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_ANNOTATED_ALIAS:{node.lineno}")
            self.generic_visit(node)

        def visit_AugAssign(self, node: ast.AugAssign) -> None:
            if sensitive_target_reference(node.target):
                errors.append(f"E_SENSITIVE_TARGET:{node.lineno}")
            self.generic_visit(node)

        def visit_TypeAlias(self, node: ast.TypeAlias) -> None:
            if self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_CAPTURE:{node.lineno}")
            self.check_type_parameters(node, node.lineno)
            self.visit(node.name)
            self.visit(node.value)

        def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
            if sensitive_target_reference(node.target):
                errors.append(f"E_SENSITIVE_TARGET:{node.lineno}")
            if self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_WALRUS_ALIAS:{node.lineno}")
            self.generic_visit(node)

        def visit_Delete(self, node: ast.Delete) -> None:
            if any(sensitive_target_reference(target) for target in node.targets):
                errors.append(f"E_SENSITIVE_TARGET:{node.lineno}")
            self.generic_visit(node)

        def visit_Return(self, node: ast.Return) -> None:
            if node.value is not None and self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_ESCAPE:{node.lineno}")
            self.generic_visit(node)

        def visit_Yield(self, node: ast.Yield) -> None:
            if node.value is not None and self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_ESCAPE:{node.lineno}")
            self.generic_visit(node)

        def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
            if self.captured_sensitive_reference(node.value):
                errors.append(f"E_EXEC_ESCAPE:{node.lineno}")
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:
            func = node.func
            if sensitive_mutation_arguments(node):
                errors.append(f"E_SENSITIVE_TARGET:{node.lineno}")
            if dynamic_namespace_reference(node):
                errors.append(f"E_DYNAMIC_NAMESPACE:{node.lineno}")
            allowed_sensitive = id(node) in (
                allowed_subprocess_calls | allowed_run_process_calls | allowed_mutator_calls
                | allowed_loader_calls | allowed_sensitive_calls | allowed_git_calls
                | allowed_filesystem_calls | allowed_getattr_calls)
            if (any(self.captured_sensitive_reference(argument) for argument in node.args)
                    or any(self.captured_sensitive_reference(keyword.value)
                           for keyword in node.keywords)):
                errors.append(f"E_EXEC_CAPTURE:{node.lineno}")
            if self.captured_sensitive_reference(func) and not allowed_sensitive:
                errors.append(f"E_EXEC_INDIRECT_REFERENCE:{node.lineno}")
            if isinstance(func, ast.Name) and func.id in {
                    "eval", "exec", "compile", "__import__", "run", "Popen",
                    "call", "check_call", "check_output", "getoutput", "getstatusoutput",
                    "system", "popen", "replace"}:
                errors.append(f"E_EXEC_EVAL:{node.lineno}")
            if isinstance(func, ast.Attribute):
                owner = func.value.id if isinstance(func.value, ast.Name) else ""
                if (path_sensitive_receiver(func.value)
                        and id(node) not in allowed_mutator_calls | allowed_filesystem_calls
                        and func.attr not in filesystem_read_only_methods | {"open"}):
                    errors.append(f"E_FS_WRITE_OUTSIDE_COLLECTOR:{node.lineno}")
                if owner == "subprocess" and func.attr == "run" and id(node) not in allowed_subprocess_calls:
                    errors.append(f"E_EXEC_DIRECT_SUBPROCESS:{node.lineno}")
                if owner == "subprocess" and func.attr in {
                        "Popen", "call", "check_call", "check_output", "getoutput", "getstatusoutput"}:
                    errors.append(f"E_EXEC_SUBPROCESS_API:{node.lineno}")
                if (owner == "os" and (func.attr in {"system", "popen"}
                                       or func.attr.startswith(("exec", "spawn")))):
                    errors.append(f"E_EXEC_OS_SHELL:{node.lineno}")
                if (isinstance(func.value, ast.Call)
                        and isinstance(func.value.func, ast.Name)
                        and func.value.func.id == "__import__"):
                    errors.append(f"E_EXEC_DYNAMIC_IMPORT:{node.lineno}")
                if func.attr == "import_module":
                    errors.append(f"E_EXEC_DYNAMIC_IMPORT:{node.lineno}")
                if (func.attr in {"spec_from_file_location", "module_from_spec", "exec_module"}
                        and id(node) not in allowed_loader_calls):
                    errors.append(f"E_EXEC_FROZEN_LOADER:{node.lineno}")
                if owner == "builtins" and func.attr in {"eval", "exec", "compile", "__import__"}:
                    errors.append(f"E_EXEC_DYNAMIC_IMPORT:{node.lineno}")
                if func.attr in {
                        "write_text", "write_bytes", "mkdir", "touch", "move", "move_into",
                        "write", "writelines", "truncate",
                } and id(node) not in allowed_mutator_calls:
                    errors.append(f"E_FS_WRITE_OUTSIDE_COLLECTOR:{node.lineno}")
                if func.attr in {"unlink", "rmdir", "remove", "rmtree", "rename"}:
                    errors.append(f"E_FS_DELETE_OUTSIDE_COLLECTOR:{node.lineno}")
                if owner == "os" and func.attr == "replace" and id(node) not in allowed_mutator_calls:
                    errors.append(f"E_FS_REPLACE_OUTSIDE_COLLECTOR:{node.lineno}")
                if (func.attr == "replace" and owner != "os"
                        and ast.unparse(node) not in {
                            "path.replace('/v1.0.24/', '/v1.0.24.1/')",
                            "raw.replace(b'\\r\\n', b'\\n')",
                            "raw.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')",
                            "str(RESULT.relative_to(ROOT)).replace('\\\\', '/')",
                            "stale_row.replace(token, value)",
                            "parent_text.replace(parent_line, parent_line.replace(f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}/{STRICT_JSON_CASES}`', f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}`'))",
                            "parent_line.replace(f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}/{STRICT_JSON_CASES}`', f'`{SEMANTIC_CASES}/{SOURCE_POLICY_CASES}`')",
                            "parent_text.replace(f'semantic/source-policy/strict-JSON `{current_counters[0]}/{current_counters[1]}/{current_counters[2]}`', f'semantic/source-policy `{current_counters[0]}/{current_counters[1]}`')",
                            "positive_row.replace(token, value)",
                            "line[3:].replace('\\\\', '/')",
                        }):
                    errors.append(f"E_FS_WRITE_OUTSIDE_COLLECTOR:{node.lineno}")
            if isinstance(func, ast.Name) and func.id == "run_process" and id(node) not in allowed_run_process_calls:
                errors.append(f"E_EXEC_RUN_PROCESS_CALLSITE:{node.lineno}")
            if isinstance(func, ast.Name) and func.id == "run_git":
                if id(node) not in allowed_git_calls:
                    errors.append(f"E_GIT_CALLSITE_CONTRACT:{node.lineno}")
                if not node.args or not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, str):
                    errors.append(f"E_GIT_DYNAMIC_SUBCOMMAND:{node.lineno}")
                elif node.args[0].value not in SAFE_GIT_SUBCOMMANDS:
                    errors.append(f"E_GIT_UNSAFE_LITERAL:{node.lineno}")
                for argument in node.args:
                    if (isinstance(argument, ast.Constant) and isinstance(argument.value, str)
                            and (argument.value in {"-c", "--upload-pack", "--receive-pack"}
                                 or argument.value.startswith(("ext::", "file::")))):
                        errors.append(f"E_GIT_UNSAFE_PROTOCOL:{node.lineno}")
                safe_dynamic_names = {
                    "BASELINE", "BRANCH", "PROTECTED_BRANCH", "PROTECTED_TIP",
                    "MAIN_TIP", "EXPECTED_PARENT", "RESULT_PATH", "path", "branch", "head",
                }
                for argument in node.args[1:]:
                    dynamic_names = {current.id for current in ast.walk(argument)
                                     if isinstance(current, ast.Name)}
                    if not dynamic_names.issubset(safe_dynamic_names):
                        errors.append(f"E_GIT_DYNAMIC_ARGUMENT:{node.lineno}")
                if any(keyword.arg != "binary"
                       or not isinstance(keyword.value, ast.Constant)
                       or keyword.value.value not in {True, False}
                       for keyword in node.keywords):
                    errors.append(f"E_GIT_DYNAMIC_KEYWORD:{node.lineno}")
            if isinstance(func, ast.Name) and func.id == "getattr":
                attribute = node.args[1] if len(node.args) >= 2 else None
                target = node.args[0] if node.args else None
                exact_literal_attribute = (
                    isinstance(attribute, ast.Constant)
                    and isinstance(attribute.value, str)
                    and not any(isinstance(argument, ast.Starred) for argument in node.args)
                    and not any(keyword.arg is None for keyword in node.keywords))
                if not exact_literal_attribute:
                    errors.append(f"E_EXEC_DYNAMIC_ATTRIBUTE:{node.lineno}")
                if ((isinstance(target, ast.Name) and target.id in {"subprocess", "os", "builtins"})
                        or (isinstance(attribute, ast.Constant) and attribute.value in {
                            "run", "Popen", "call", "check_call", "check_output",
                            "getoutput", "getstatusoutput", "system", "popen", "__import__"})):
                    errors.append(f"E_EXEC_DYNAMIC_ATTRIBUTE:{node.lineno}")
                if (isinstance(attribute, ast.Constant)
                        and attribute.value in filesystem_sensitive_attributes):
                    errors.append(f"E_FS_DYNAMIC_ATTRIBUTE:{node.lineno}")
            if (isinstance(func, ast.Name) and func.id == "vars" and node.args
                    and isinstance(node.args[0], ast.Name)
                    and node.args[0].id in {"subprocess", "os", "builtins", "importlib"}):
                errors.append(f"E_EXEC_DYNAMIC_ATTRIBUTE:{node.lineno}")
            if isinstance(func, ast.Subscript) and any(
                    isinstance(current, ast.Name) and current.id in {"subprocess", "os", "builtins"}
                    for current in ast.walk(func)):
                errors.append(f"E_EXEC_DYNAMIC_ATTRIBUTE:{node.lineno}")
            if ((isinstance(func, ast.Name) and func.id == "open")
                    or (isinstance(func, ast.Attribute) and func.attr == "open")):
                if not direct_read_only_open_call(node):
                    errors.append(f"E_FS_OPEN_MODE:{node.lineno}")
            self.generic_visit(node)

    Visitor().visit(tree)
    return errors


def source_policy_errors(path: pathlib.Path) -> list[str]:
    resolved = path.resolve()
    shape = "builder" if resolved == BUILDER.resolve() else (
        "validator" if resolved == VALIDATOR.resolve() else None)
    return source_policy_source_errors(path.read_text(encoding="utf-8"), expected_shape=shape)


def source_policy_negative_probes() -> int:
    probes = (
        ("direct-subprocess", "import subprocess\nsubprocess.run(['x'])\n", "E_EXEC_DIRECT_SUBPROCESS"),
        ("aliased-subprocess", "import subprocess\nf = subprocess.run\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("import-alias", "import subprocess as sp\nsp.run(['x'])\n", "E_IMPORT_EXECUTION_ALIAS"),
        ("from-import", "from subprocess import run\nrun(['x'])\n", "E_IMPORT_FROM_EXECUTION"),
        ("dynamic-exec", "getattr(subprocess, 'run')(['x'])\n", "E_EXEC_DYNAMIC_ATTRIBUTE"),
        ("dynamic-exec-name", "def f(name):\n    getattr(subprocess, name)(['x'])\n", "E_EXEC_DYNAMIC_ATTRIBUTE"),
        ("dynamic-import", "__import__('subprocess').run(['x'])\n", "E_EXEC_DYNAMIC_IMPORT"),
        ("importlib-dynamic", "importlib.import_module('subprocess').run(['x'])\n", "E_EXEC_DYNAMIC_IMPORT"),
        ("importlib-from", "from importlib import import_module\nimport_module('subprocess').run(['x'])\n", "E_IMPORT_FROM_EXECUTION"),
        ("builtins-alias", "import builtins as b\nb.__import__('subprocess').run(['x'])\n", "E_IMPORT_EXECUTION_ALIAS"),
        ("module-assignment-alias", "m = subprocess\ndef f(name):\n    getattr(m, name)(['x'])\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("popen", "subprocess.Popen(['x'])\n", "E_EXEC_SUBPROCESS_API"),
        ("subprocess-call", "subprocess.call(['x'])\n", "E_EXEC_SUBPROCESS_API"),
        ("subprocess-check-output", "subprocess.check_output(['x'])\n", "E_EXEC_SUBPROCESS_API"),
        ("vars-subprocess", "vars(subprocess)['run'](['x'])\n", "E_EXEC_DYNAMIC_ATTRIBUTE"),
        ("run-process-escape", "def f():\n    run_process(['x'])\n", "E_EXEC_RUN_PROCESS_CALLSITE"),
        ("run-process-alias", "f = run_process\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("git-alias", "g = run_git\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("annotated-alias", "f: object = run_process\n", "E_EXEC_ANNOTATED_ALIAS"),
        ("walrus-alias", "(f := run_git)\n", "E_EXEC_WALRUS_ALIAS"),
        ("run-process-shape",
         "import subprocess\ndef run_process(args):\n    subprocess.run(args, cwd=ROOT, capture_output=True, check=False)\n    subprocess.run(['x'])\n",
         "E_RUN_PROCESS_SHAPE"),
        ("run-process-args-rebind",
         "import subprocess\ndef run_process(args):\n    args = ['git', 'push', 'origin', 'HEAD']\n    proc = subprocess.run(args, cwd=ROOT, capture_output=True, check=False)\n    require(proc.returncode == 0, 'E_GIT_READ')\n    return proc.stdout\n",
         "E_RUN_PROCESS_AST"),
        ("run-git-args-rebind",
         "def run_git(*args, binary=False):\n    args = ('push',)\n    raw = run_process(['git', *args])\n    return raw if binary else raw.decode('utf-8', 'strict')\n",
         "E_RUN_GIT_AST"),
        ("sys-modules-subprocess",
         "import sys\nsys.modules['subprocess'].run(['x'])\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("tuple-module-alias",
         "import subprocess\nm = (subprocess,)[0]\ndef f(name):\n    getattr(m, name)(['x'])\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("vars-importlib-subprocess",
         "import importlib\nvars(importlib)['import_module']('subprocess').run(['x'])\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("frozen-loader-outside-load-builder",
         "import importlib.util\ndef f(path):\n    spec = importlib.util.spec_from_file_location('x', path)\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n",
         "E_EXEC_FROZEN_LOADER"),
        ("load-builder-contract-tamper",
         "import importlib.util\ndef load_builder():\n    spec = importlib.util.spec_from_file_location('phase065_step71_builder', BUILDER)\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n    spec.loader.exec_module(module)\n    return module\n",
         "E_LOAD_BUILDER_AST"),
        ("post-definition-rebind-run-git",
         "def run_git(*args, binary=False):\n    return b''\nrun_git = harmless\n",
         "E_PROTECTED_BINDING"),
        ("post-definition-rebind-run-process",
         "def run_process(args):\n    return b''\nrun_process = harmless\n",
         "E_PROTECTED_BINDING"),
        ("post-definition-rebind-load-builder",
         "def load_builder():\n    return None\nload_builder = harmless\n",
         "E_PROTECTED_BINDING"),
        ("post-definition-rebind-atomic-collector",
         "def atomic_json_last_collect(output_dir):\n    return None\natomic_json_last_collect = harmless\n",
         "E_PROTECTED_BINDING"),
        ("missing-definition-assignment-run-git", "run_git = harmless\n", "E_PROTECTED_BINDING"),
        ("missing-definition-assignment-run-process", "run_process = harmless\n", "E_PROTECTED_BINDING"),
        ("missing-definition-assignment-load-builder", "load_builder = harmless\n", "E_PROTECTED_BINDING"),
        ("missing-definition-assignment-atomic-collector",
         "atomic_json_last_collect = harmless\n", "E_PROTECTED_BINDING"),
        ("partial-sensitive-positional",
         "import functools\ncallback = functools.partial(run_git, 'show')\n", "E_EXEC_CAPTURE"),
        ("partial-sensitive-keyword",
         "import functools\ncallback = functools.partial(run_process, args=['git'])\n", "E_EXEC_CAPTURE"),
        ("arbitrary-call-sensitive-positional", "capture(run_git)\n", "E_EXEC_CAPTURE"),
        ("arbitrary-call-sensitive-keyword", "capture(callback=run_process)\n", "E_EXEC_CAPTURE"),
        ("function-default-sensitive", "def f(callback=run_git):\n    return callback\n", "E_EXEC_CAPTURE"),
        ("function-kwonly-default-sensitive",
         "def f(*, callback=run_process):\n    return callback\n", "E_EXEC_CAPTURE"),
        ("lambda-default-sensitive", "f = lambda callback=run_git: callback\n", "E_EXEC_CAPTURE"),
        ("decorator-argument-sensitive", "@decorate(run_process)\ndef f():\n    pass\n", "E_EXEC_CAPTURE"),
        ("decorator-direct-sensitive", "@run_git\ndef f():\n    pass\n", "E_EXEC_CAPTURE"),
        ("destructuring-protected-rebind", "run_git, other = harmless, 1\n", "E_PROTECTED_BINDING"),
        ("annotated-protected-rebind", "run_process: object = harmless\n", "E_PROTECTED_BINDING"),
        ("walrus-protected-rebind", "(load_builder := harmless)\n", "E_PROTECTED_BINDING"),
        ("for-target-protected-rebind", "for run_git in values:\n    pass\n", "E_PROTECTED_BINDING"),
        ("comprehension-target-protected-rebind", "[run_process for run_process in values]\n", "E_PROTECTED_BINDING"),
        ("delete-protected-binding", "del atomic_json_last_collect\n", "E_PROTECTED_BINDING"),
        ("parameter-protected-shadow", "def f(run_git):\n    return run_git\n", "E_PROTECTED_BINDING"),
        ("import-protected-binding", "import harmless as run_process\n", "E_PROTECTED_BINDING"),
        ("from-import-protected-binding", "from harmless import value as load_builder\n", "E_PROTECTED_BINDING"),
        ("class-protected-binding", "class atomic_json_last_collect:\n    pass\n", "E_PROTECTED_BINDING"),
        ("except-protected-binding",
         "try:\n    pass\nexcept Exception as run_git:\n    pass\n", "E_PROTECTED_BINDING"),
        ("vars-sys-modules-indirect",
         "vars(sys)['modules']['subprocess'].run(['x'])\n", "E_EXEC_INDIRECT_REFERENCE"),
        ("getattr-sys-modules-indirect",
         "getattr(sys, 'modules')['subprocess'].run(['x'])\n", "E_EXEC_INDIRECT_REFERENCE"),
        ("spec-from-file-location-alias",
         "alias = importlib.util.spec_from_file_location\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("spec-from-file-location-getattr-alias",
         "alias = getattr(importlib.util, 'spec_from_file_location')\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("spec-from-file-location-vars-alias",
         "alias = vars(importlib.util)['spec_from_file_location']\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("exec-module-alias", "alias = spec.loader.exec_module\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("exec-module-getattr-alias",
         "alias = getattr(spec.loader, 'exec_module')\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("exec-module-vars-alias",
         "alias = vars(spec.loader)['exec_module']\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("exec-module-nested-getattr-loader-root",
         "alias = getattr(getattr(spec, 'loader'), 'exec_module')\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("exec-module-vars-loader-root",
         "alias = vars(spec)['loader'].exec_module\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("return-run-git-callable",
         "def expose():\n    return run_git\nexpose()('push', 'origin', 'HEAD')\n",
         "E_EXEC_ESCAPE"),
        ("return-subprocess-run-callable",
         "import subprocess\ndef expose():\n    return subprocess.run\nexpose()(['x'])\n",
         "E_EXEC_ESCAPE"),
        ("lambda-return-run-git-callable",
         "expose = lambda: run_git\nexpose()('push', 'origin', 'HEAD')\n",
         "E_EXEC_ESCAPE"),
        ("return-spec-from-file-location-callable",
         "def expose():\n    return importlib.util.spec_from_file_location\nexpose()('x', 'x.py')\n",
         "E_EXEC_ESCAPE"),
        ("return-exec-module-callable",
         "def expose(spec):\n    return spec.loader.exec_module\nexpose(spec)(module)\n",
         "E_EXEC_ESCAPE"),
        ("return-getattr-exec-module-callable",
         "def expose(spec):\n    return getattr(spec.loader, 'exec_module')\nexpose(spec)(module)\n",
         "E_EXEC_ESCAPE"),
        ("return-vars-exec-module-callable",
         "def expose(spec):\n    return vars(spec.loader)['exec_module']\nexpose(spec)(module)\n",
         "E_EXEC_ESCAPE"),
        ("yield-run-git-callable",
         "def expose():\n    yield run_git\nnext(expose())('push')\n", "E_EXEC_ESCAPE"),
        ("yield-from-run-git-container",
         "def expose():\n    yield from (run_git,)\nnext(expose())('push')\n",
         "E_EXEC_ESCAPE"),
        ("return-sensitive-container",
         "def expose():\n    return {'callback': run_process}\nexpose()['callback'](['git'])\n",
         "E_EXEC_ESCAPE"),
        ("return-sensitive-conditional-expression",
         "def expose(flag):\n    return run_git if flag else harmless\n",
         "E_EXEC_ESCAPE"),
        ("return-sensitive-generator-container",
         "def expose():\n    return (callback for callback in (run_git,))\n",
         "E_EXEC_ESCAPE"),
        ("property-sensitive-exposure",
         "class Exposer:\n    @property\n    def callback(self):\n        return run_git\n",
         "E_EXEC_ESCAPE"),
        ("return-binop-tuple-union-run-git",
         "def expose():\n    return (run_git,) + ()\n", "E_EXEC_ESCAPE"),
        ("return-binop-list-repeat-run-process",
         "def expose():\n    return [run_process] * 1\n", "E_EXEC_ESCAPE"),
        ("return-binop-dict-union-subprocess-run",
         "import subprocess\ndef expose():\n    return {'callback': subprocess.run} | {}\n",
         "E_EXEC_ESCAPE"),
        ("return-boolop-spec-from-file-location",
         "def expose():\n    return harmless or importlib.util.spec_from_file_location\n",
         "E_EXEC_ESCAPE"),
        ("return-unaryop-run-git",
         "def expose():\n    return not run_git\n", "E_EXEC_ESCAPE"),
        ("return-joinedstr-run-process",
         "def expose():\n    return f'{run_process}'\n", "E_EXEC_ESCAPE"),
        ("return-compare-exec-module",
         "def expose(spec):\n    return spec.loader.exec_module == harmless\n",
         "E_EXEC_ESCAPE"),
        ("return-slice-run-git",
         "def expose():\n    return (run_git,)[0:1]\n", "E_EXEC_ESCAPE"),
        ("return-subscript-subprocess-run",
         "import subprocess\ndef expose():\n    return {'callback': subprocess.run}['callback']\n",
         "E_EXEC_ESCAPE"),
        ("return-listcomp-spec-from-file-location",
         "def expose():\n    return [callback for callback in (importlib.util.spec_from_file_location,)]\n",
         "E_EXEC_ESCAPE"),
        ("return-dictcomp-exec-module",
         "def expose(spec):\n    return {name: callback for name, callback in [('x', spec.loader.exec_module)]}\n",
         "E_EXEC_ESCAPE"),
        ("call-argument-binop-run-git", "capture((run_git,) + ())\n", "E_EXEC_CAPTURE"),
        ("function-default-binop-run-process",
         "def expose(callback=[run_process] * 1):\n    return callback\n",
         "E_EXEC_CAPTURE"),
        ("decorator-joinedstr-run-git",
         "@decorate(f'{run_git}')\ndef expose():\n    pass\n", "E_EXEC_CAPTURE"),
        ("lambda-body-compare-spec-from-file-location",
         "expose = lambda: importlib.util.spec_from_file_location == harmless\n",
         "E_EXEC_ESCAPE"),
        ("yield-subscript-exec-module",
         "def expose(spec):\n    yield {'callback': spec.loader.exec_module}['callback']\n",
         "E_EXEC_ESCAPE"),
        ("yield-from-list-repeat-run-process",
         "def expose():\n    yield from [run_process] * 1\n", "E_EXEC_ESCAPE"),
        ("direct-call-binop-tuple-run-git",
         "((run_git,) + (harmless,))[0]('show')\n", "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-boolop-run-process",
         "(run_process or harmless)(['git'])\n", "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-ifexp-subprocess-run",
         "import subprocess\n(subprocess.run if flag else harmless)(['x'])\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-subscript-dict-union-run-git",
         "({'callback': run_git} | {'other': harmless})['callback']('show')\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-listcomp-spec-loader",
         "[callback for callback in (importlib.util.spec_from_file_location,)][0]('x', 'x.py')\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-dictcomp-exec-module",
         "{name: callback for name, callback in [('x', spec.loader.exec_module)]}['x'](module)\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-setcomp-pop-run-git",
         "{callback for callback in (run_git,)}.pop()('show')\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-generator-next-subprocess-run",
         "(callback for callback in (subprocess.run,)).__next__()(['x'])\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-nested-ifexp-binop-run-process",
         "(((run_process,) + ()) if flag else (harmless,))[0](['git'])\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("direct-call-nested-dict-union-spec-loader",
         "(({'x': spec.loader.exec_module} | {}) if flag else {'x': harmless})['x'](module)\n",
         "E_EXEC_INDIRECT_REFERENCE"),
        ("annotation-posonly-protected",
         "def expose(value: run_git, /):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-positional-protected",
         "def expose(value: run_process):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-kwonly-protected",
         "def expose(*, value: load_builder):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-vararg-protected",
         "def expose(*value: run_git):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-kwarg-protected",
         "def expose(**value: run_process):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-return-protected",
         "def expose() -> run_git:\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-return-dynamic-namespace",
         "def expose() -> globals():\n    pass\n", "E_DYNAMIC_NAMESPACE"),
        ("annotation-annassign-protected",
         "value: run_git = harmless\n", "E_EXEC_CAPTURE"),
        ("annotation-class-base-protected",
         "class Expose(run_git):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-class-keyword-protected",
         "class Expose(metaclass=run_process):\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-function-type-param-bound",
         "def expose[T: run_git]():\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-class-type-param-bound",
         "class Expose[T: run_process]:\n    pass\n", "E_EXEC_CAPTURE"),
        ("annotation-type-alias-value",
         "type Expose = run_git\n", "E_EXEC_CAPTURE"),
        ("annotation-type-alias-param-bound",
         "type Expose[T: run_process] = T\n", "E_EXEC_CAPTURE"),
        ("builtins-import-direct", "import builtins\n", "E_IMPORT_BUILTINS"),
        ("builtins-import-alias", "import builtins as namespace\n", "E_IMPORT_BUILTINS"),
        ("builtins-from-import", "from builtins import globals as namespace\n",
         "E_IMPORT_FROM_EXECUTION"),
        ("builtins-direct-reference", "namespace = builtins\n", "E_DYNAMIC_NAMESPACE"),
        ("dunder-builtins-direct-reference", "namespace = __builtins__\n",
         "E_DYNAMIC_NAMESPACE"),
        ("builtins-attribute-reference", "builtins.globals()\n", "E_DYNAMIC_NAMESPACE"),
        ("dunder-builtins-subscript-reference",
         "__builtins__['globals']()\n", "E_DYNAMIC_NAMESPACE"),
        ("builtins-computed-getattr-reference",
         "getattr((builtins if flag else fallback), name)()\n", "E_DYNAMIC_NAMESPACE"),
        ("match-as-protected-binding",
         "match value:\n    case run_git:\n        pass\n", "E_PROTECTED_BINDING"),
        ("match-star-protected-binding",
         "match value:\n    case [*run_process]:\n        pass\n", "E_PROTECTED_BINDING"),
        ("match-mapping-rest-protected-binding",
         "match value:\n    case {'x': item, **load_builder}:\n        pass\n",
         "E_PROTECTED_BINDING"),
        ("sensitive-load-for-iterator",
         "for item in run_git:\n    pass\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-comprehension-iterator",
         "[item for item in run_process]\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-match-subject",
         "match subprocess.run:\n    case _:\n        pass\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-match-guard",
         "match value:\n    case _ if spec.loader.exec_module:\n        pass\n",
         "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-with-context",
         "with load_builder as exposed:\n    pass\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-if-condition",
         "if importlib.util.spec_from_file_location:\n    pass\n",
         "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-while-condition",
         "while atomic_json_last_collect:\n    break\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-assert-expression",
         "assert os.system\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-standalone-container",
         "{'callback': run_git}\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-subscript-chain-iterator",
         "for callback in sys.modules['subprocess'].run:\n    pass\n",
         "E_EXEC_SENSITIVE_LOAD"),
        ("assignment-sensitive-type-comment",
         "callback = harmless  # type: run_git\n", "E_TYPE_COMMENT"),
        ("function-sensitive-type-comment",
         "def expose(callback):  # type: (run_process) -> None\n    pass\n",
         "E_TYPE_COMMENT"),
        ("sensitive-load-alias-eval",
         "callback = eval\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-return-exec",
         "def expose():\n    return exec\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-container-compile",
         "callbacks = {'compile': compile}\n", "E_EXEC_SENSITIVE_LOAD"),
        ("sensitive-load-indirect-call-eval",
         "(eval if enabled else harmless)('1')\n", "E_EXEC_SENSITIVE_LOAD"),
        ("plain-type-ignore",
         "value = harmless  # type: ignore\n", "E_TYPE_IGNORE"),
        ("tagged-type-ignore",
         "value = harmless  # type: ignore[assignment]\n", "E_TYPE_IGNORE"),
        ("protected-code-assign",
         "run_git.__code__ = replacement\n", "E_SENSITIVE_TARGET"),
        ("protected-defaults-delete",
         "del run_process.__defaults__\n", "E_SENSITIVE_TARGET"),
        ("protected-dict-subscript-assign",
         "load_builder.__dict__['callback'] = replacement\n", "E_SENSITIVE_TARGET"),
        ("protected-attribute-annassign",
         "atomic_json_last_collect.state: object = replacement\n", "E_SENSITIVE_TARGET"),
        ("protected-attribute-augassign",
         "run_git.state += 1\n", "E_SENSITIVE_TARGET"),
        ("protected-nested-tuple-target",
         "(run_process.__dict__['callback'], other) = values\n", "E_SENSITIVE_TARGET"),
        ("subprocess-member-replace",
         "subprocess.run = harmless\n", "E_SENSITIVE_TARGET"),
        ("os-dict-delete",
         "del os.__dict__['system']\n", "E_SENSITIVE_TARGET"),
        ("importlib-util-member-replace",
         "importlib.util.spec_from_file_location = harmless\n", "E_SENSITIVE_TARGET"),
        ("builtins-subscript-replace",
         "__builtins__['exec'] = harmless\n", "E_SENSITIVE_TARGET"),
        ("sys-modules-replace",
         "sys.modules['subprocess'] = harmless\n", "E_SENSITIVE_TARGET"),
        ("setattr-protected-identity",
         "setattr(run_git, '__code__', replacement)\n", "E_SENSITIVE_TARGET"),
        ("delattr-importlib-identity",
         "delattr(importlib.util, 'spec_from_file_location')\n", "E_SENSITIVE_TARGET"),
        ("object-setattr-subprocess-identity",
         "object.__setattr__(subprocess, 'run', harmless)\n", "E_SENSITIVE_TARGET"),
        ("dict-update-protected-identity",
         "run_git.__dict__.update({'callback': harmless})\n", "E_SENSITIVE_TARGET"),
        ("operator-setitem-importlib-identity",
         "operator.setitem(importlib.util.__dict__, 'module_from_spec', harmless)\n",
         "E_SENSITIVE_TARGET"),
        ("unknown-mutator-load-builder-identity",
         "mutate(load_builder)\n", "E_SENSITIVE_TARGET"),
        ("dynamic-namespace-globals-subscript-direct-call",
         "globals()['run_git']('show')\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-locals-get-direct-call",
         "locals().get('run_process')(['git'])\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-zero-vars-subscript-direct-call",
         "vars()['load_builder']()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-globals-container",
         "mapping = {'namespace': globals()}\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-locals-alias",
         "namespace = locals()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-zero-vars-return",
         "def expose():\n    return vars()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-globals-return",
         "def expose():\n    return globals()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-locals-call-argument",
         "capture(locals())\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-harmless-key-alias",
         "alias = globals()['harmless']\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-zero-vars-get",
         "vars().get('anything')\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-globals-unpacked-positional",
         "globals(*[])['run_git']('show')\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-locals-unpacked-keyword",
         "locals(**{}).get('run_process')(['git'])\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-vars-unpacked-positional",
         "vars(*())['load_builder']()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-direct-reference-alias-call",
         "namespace = globals\nnamespace()['run_git']('show')\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-tuple-index-reference",
         "namespace = (locals,)[0]\nnamespace()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-builtins-getattr",
         "import builtins\ngetattr(builtins, 'globals')()['run_git']('show')\n",
         "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-dunder-builtins-getattr",
         "getattr(__builtins__, 'locals')()\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-returned-reference",
         "def expose():\n    return vars\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-container-reference",
         "capture({'namespace': globals})\n", "E_DYNAMIC_NAMESPACE"),
        ("dynamic-namespace-vars-getattr-chain",
         "import builtins\ngetattr(vars(builtins), 'globals')()\n",
         "E_DYNAMIC_NAMESPACE"),
        ("module-if-nested-run-git-definition",
         "if enabled:\n    def run_git(*args, binary=False):\n        return b''\n",
         "E_POLICY_NESTED_FUNCTION"),
        ("module-try-nested-run-process-definition",
         "try:\n    def run_process(args):\n        return b''\nexcept Exception:\n    pass\n",
         "E_POLICY_NESTED_FUNCTION"),
        ("module-with-nested-run-git-definition",
         "with context():\n    def run_git(*args, binary=False):\n        return b''\n",
         "E_POLICY_NESTED_FUNCTION"),
        ("module-match-nested-run-process-definition",
         "match value:\n    case _:\n        def run_process(args):\n            return b''\n",
         "E_POLICY_NESTED_FUNCTION"),
        ("dunder-globals-indirect-call",
         "helper.__globals__['run_git']('show')\n", "E_EXEC_SENSITIVE_LOAD"),
        ("dunder-globals-get-indirect-call",
         "helper.__globals__.get('run_process')(['git'])\n", "E_EXEC_SENSITIVE_LOAD"),
        ("dunder-globals-mapping-update",
         "helper.__globals__.update({'run_git': harmless})\n", "E_SENSITIVE_TARGET"),
        ("dunder-globals-subscript-mutation",
         "helper.__globals__['run_git'] = harmless\n", "E_SENSITIVE_TARGET"),
        ("frame-f-globals-indirect-call",
         "frame.f_globals['run_git']('show')\n", "E_EXEC_SENSITIVE_LOAD"),
        ("frame-f-locals-mapping-update",
         "frame.f_locals.update({'run_process': harmless})\n", "E_SENSITIVE_TARGET"),
        ("sys-getframe-f-globals-call",
         "sys._getframe().f_globals['run_git']('show')\n", "E_EXEC_SENSITIVE_LOAD"),
        ("inspect-currentframe-f-locals-call",
         "inspect.currentframe().f_locals['run_process'](['git'])\n",
         "E_EXEC_SENSITIVE_LOAD"),
        ("dunder-getattribute-globals-call",
         "helper.__getattribute__('__globals__')['run_git']('show')\n",
         "E_EXEC_SENSITIVE_LOAD"),
        ("dunder-getattribute-dynamic-call",
         "helper.__getattribute__(dynamic_name)['run_git']('show')\n",
         "E_EXEC_SENSITIVE_LOAD"),
        ("git-dynamic", "def f(command):\n    run_git(command)\n", "E_GIT_DYNAMIC_SUBCOMMAND"),
        ("git-dynamic-argument", "def f(payload):\n    run_git('show', payload)\n", "E_GIT_DYNAMIC_ARGUMENT"),
        ("git-whitelisted-name-bypass", "def f(path):\n    run_git('show', path)\n", "E_GIT_CALLSITE_CONTRACT"),
        ("git-allowed-caller-tamper", "def git_raw(path):\n    return run_git('show', path)\n", "E_GIT_CALL_CONTRACT"),
        ("git-duplicate-exact-call",
         "def git_raw(path):\n    run_git('cat-file', 'blob', f'{BASELINE}:{path}', binary=True)\n    return run_git('cat-file', 'blob', f'{BASELINE}:{path}', binary=True)\n",
         "E_GIT_CALLER_AST"),
        ("git-control-flow-relocation",
         "def git_raw(path):\n    if path:\n        return run_git('cat-file', 'blob', f'{BASELINE}:{path}', binary=True)\n",
         "E_GIT_CALLER_AST"),
        ("git-dynamic-keyword", "def f(flag):\n    run_git('show', 'HEAD', binary=flag)\n", "E_GIT_DYNAMIC_KEYWORD"),
        ("git-protocol", "run_git('show', 'ext::payload')\n", "E_GIT_UNSAFE_PROTOCOL"),
        ("filesystem-write", "def f(p):\n    p.write_bytes(b'x')\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("collector-extra-write", "def atomic_json_last_collect(output_dir):\n    output_dir.write_bytes(b'x')\n", "E_ATOMIC_COLLECTOR_SHAPE"),
        ("collector-wrong-destination", "def atomic_json_last_collect(output_dir):\n    output_dir.mkdir(parents=True, exist_ok=True)\n", "E_ATOMIC_COLLECTOR_SHAPE"),
        ("collector-dead-string-gate",
         "def atomic_json_last_collect(output_dir):\n    'destination == repository_results; result_status == result; result_index == worktree'\n    destination.mkdir(parents=True, exist_ok=True)\n    matrix_temp.write_bytes(canonical_bytes(matrix))\n    attestation_temp.write_bytes(canonical_bytes(attestation))\n    os.replace(matrix_temp, matrix_path)\n    os.replace(attestation_temp, attestation_path)\n",
         "E_ATOMIC_COLLECTOR_SHAPE"),
        ("collector-post-prefix-rebind",
         "def atomic_json_last_collect(output_dir):\n    destination = output_dir.resolve()\n    repository_results = (ROOT / 'Codex/results').resolve()\n    require(destination == repository_results, 'E_REPOSITORY_WRITE_BOUNDARY', str(destination))\n    result_status = str(run_git('diff', '--cached', '--name-status', '--', RESULT_PATH)).strip()\n    require(result_status == f'A\\t{RESULT_PATH}', 'E_RESULT_NOT_STAGED_FIRST', result_status)\n    result_index = bytes(run_git('show', f':{RESULT_PATH}', binary=True))\n    require(result_index == (ROOT / RESULT_PATH).read_bytes(), 'E_RESULT_INDEX_WORKTREE')\n    destination = output_dir.parent\n    destination.mkdir(parents=True, exist_ok=True)\n    matrix_temp.write_bytes(canonical_bytes(matrix))\n    attestation_temp.write_bytes(canonical_bytes(attestation))\n    os.replace(matrix_temp, matrix_path)\n    os.replace(attestation_temp, attestation_path)\n",
         "E_GIT_CALLER_AST"),
        ("filesystem-delete", "def f(p):\n    p.unlink()\n", "E_FS_DELETE_OUTSIDE_COLLECTOR"),
        ("filesystem-replace", "import os\ndef f(a,b):\n    os.replace(a,b)\n", "E_FS_REPLACE_OUTSIDE_COLLECTOR"),
        ("filesystem-dynamic", "getattr(path, 'unlink')()\n", "E_FS_DYNAMIC_ATTRIBUTE"),
        ("filesystem-path-touch", "path.touch()\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-replace", "path.replace(other)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-move", "path.move(other)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-output-dir-move-into",
         "args.output_dir.move_into('x')\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-symlink-to", "RESULT.symlink_to(target)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-hardlink-to", "RESULT.hardlink_to(target)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-link-to", "RESULT.link_to(target)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-chmod", "RESULT.chmod(0o777)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-lchmod", "RESULT.lchmod(0o777)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-copy", "RESULT.copy(target)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-copy-into", "RESULT.copy_into(target)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-mutator-alias",
         "alias = RESULT\nalias.symlink_to(target)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-unknown-method",
         "RESULT.mutate_metadata(value)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-path-destructuring-alias",
         "(alias,) = (RESULT,)\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-container-subscript-alias",
         "alias = [RESULT][0]\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-walrus-receiver",
         "(alias := RESULT).mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-for-target-alias",
         "for alias in [RESULT]:\n    alias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-comprehension-capture",
         "values = [alias for alias in [RESULT]]\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-function-default",
         "def expose(alias=RESULT):\n    alias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-dict-container",
         "values = {'result': RESULT}\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-lambda-closure",
         "expose = lambda: RESULT\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-decorator-argument",
         "@decorate(RESULT)\ndef expose():\n    pass\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-return-value",
         "def expose():\n    return RESULT\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-call-argument",
         "consume(RESULT)\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-path-attribute-transport-chain",
         "holder.path = RESULT\nholder.path.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-lowercase-path-destructuring-alias",
         "(alias,) = (path,)\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-lowercase-path-container-subscript-alias",
         "alias = [path][0]\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-lowercase-path-function-default",
         "def expose(alias=path):\n    alias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-read-call-walrus-result-transport",
         "open((alias := RESULT), 'rb').read()\nalias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-read-call-walrus-lowercase-path-transport",
         "open((alias := path), 'rb').read()\nalias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-read-call-lambda-result-transport",
         "open((f := lambda: RESULT)(), 'rb').read()\nf().mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-relative-to-walrus-root-transport",
         "RESULT.relative_to(alias := ROOT)\nalias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-read-call-default-capture",
         "open((lambda candidate=RESULT: candidate)(), 'rb').read()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-read-call-generator-transport",
         "open(next(candidate for candidate in [RESULT]), 'rb').read()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-relative-to-lambda-root-argument",
         "RESULT.relative_to((lambda: ROOT)())\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-read-call-nested-walrus-container",
         "open([(alias := RESULT)][0], 'rb').read()\nalias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-uppercase-path-destructuring",
         "(alias,) = (PATH,)\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-result-path-container",
         "alias = [RESULT_PATH][0]\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-source-file-walrus",
         "(alias := source_file).mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-output-path-loop",
         "for alias in [output_path]:\n    alias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-title-path-default",
         "def expose(alias=Path):\n    alias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-filepath-container",
         "values = {'input': filepath}\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-file-path-default",
         "def expose(alias=file_path):\n    return alias\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-mixed-case-output-path-destructuring",
         "[alias] = [OuTpUt_PaTh]\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-source-file-direct-alias",
         "alias = source_file\nalias.mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-filepath-walrus-container",
         "values = [(alias := FilePath)]\nalias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-container",
         "values = [pathlib.Path('x')]\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-walrus",
         "(alias := pathlib.Path('x')).mutate_anything()\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-loop",
         "for alias in [pathlib.Path('x')]:\n    alias.mutate_anything()\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-comprehension",
         "values = [alias for alias in [pathlib.Path('x')]]\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-default",
         "def expose(alias=pathlib.Path('x')):\n    return alias\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-lambda-return",
         "expose = lambda: pathlib.Path('x')\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-call-argument",
         "consume(pathlib.Path('x'))\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-attribute-transport",
         "holder.value = pathlib.Path('x')\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-subscript-derived",
         "value = [pathlib.Path('x')][0]\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-division-derived",
         "value = pathlib.Path('x') / 'child'\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-ifexp-derived",
         "value = pathlib.Path('a') if flag else pathlib.Path('b')\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-purepath-dict",
         "value = {'input': pathlib.PurePath('x')}\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-purewindows-path-call-argument",
         "consume(pathlib.PureWindowsPath('x'))\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-imported-purepath-lambda-return",
         "expose = lambda: PurePath('x')\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-path-constructor-alias",
         "factory = pathlib.Path\nvalue = factory('x')\n", "E_FS_PATH_ESCAPE"),
        ("filesystem-pathlib-purepath-constructor-alias-container",
         "factory = pathlib.PurePath\nvalues = [factory('x')]\n",
         "E_FS_PATH_ESCAPE"),
        ("filesystem-stream-write", "stream.write(data)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-stream-writelines", "stream.writelines(lines)\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-stream-truncate", "stream.truncate()\n", "E_FS_WRITE_OUTSIDE_COLLECTOR"),
        ("filesystem-open-dynamic-mode", "open(path, mode_name)\n", "E_FS_OPEN_MODE"),
        ("filesystem-open-keyword-dynamic-mode", "open(path, mode=mode_name)\n", "E_FS_OPEN_MODE"),
        ("filesystem-path-open-dynamic-mode", "path.open(mode_name)\n", "E_FS_OPEN_MODE"),
        ("filesystem-open-write-mode", "open(path, 'w')\n", "E_FS_OPEN_MODE"),
        ("filesystem-path-open-update-mode", "path.open('r+')\n", "E_FS_OPEN_MODE"),
        ("filesystem-builtin-open-alias", "reader = open\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-builtin-open-container", "readers = (open,)\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-builtin-open-return", "def expose():\n    return open\n", "E_EXEC_ESCAPE"),
        ("filesystem-builtin-open-callback", "consume(open)\n", "E_EXEC_CAPTURE"),
        ("filesystem-method-open-alias", "reader = path.open\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-method-write-container", "writers = [stream.write]\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-method-writelines-return", "def expose(stream):\n    return stream.writelines\n", "E_EXEC_ESCAPE"),
        ("filesystem-method-truncate-callback", "consume(stream.truncate)\n", "E_EXEC_CAPTURE"),
        ("filesystem-method-touch-alias", "touch = path.touch\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-method-replace-return", "def expose(path):\n    return path.replace\n", "E_EXEC_ESCAPE"),
        ("filesystem-method-rename-container", "ops = {'rename': path.rename}\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-method-move-indirect-call", "ops = (path.move,)\nops[0](other)\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("filesystem-open-starred-positional", "open(*(path, 'r'))\n", "E_FS_OPEN_MODE"),
        ("filesystem-open-starred-empty", "open(path, *())\n", "E_FS_OPEN_MODE"),
        ("filesystem-open-unpacked-keywords", "open(path, **{'mode': 'r'})\n", "E_FS_OPEN_MODE"),
        ("filesystem-path-open-starred", "path.open(*('r',))\n", "E_FS_OPEN_MODE"),
        ("filesystem-path-open-unpacked-keywords", "path.open(**{'mode': 'r'})\n", "E_FS_OPEN_MODE"),
        ("getattr-dynamic-variable-general-receiver",
         "attribute_name = 'read_text'\noperation = getattr(path, attribute_name)\n",
         "E_EXEC_DYNAMIC_ATTRIBUTE"),
        ("getattr-folded-name-general-receiver",
         "operation = getattr(path, 'op' + 'en')\n", "E_EXEC_DYNAMIC_ATTRIBUTE"),
        ("getattr-dynamic-call-general-receiver",
         "getattr(path, attribute_name)()\n", "E_EXEC_DYNAMIC_ATTRIBUTE"),
        ("getattr-alias-assignment", "ga = getattr\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("getattr-alias-call",
         "ga = getattr\noperation = ga(path, attribute_name)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("getattr-container", "operations = (getattr,)\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("getattr-return", "def expose():\n    return getattr\n", "E_EXEC_ESCAPE"),
        ("getattr-callback", "consume(getattr)\n", "E_EXEC_CAPTURE"),
        ("operator-import", "import operator\n", "E_IMPORT_OPERATOR"),
        ("operator-import-from-attrgetter",
         "from operator import attrgetter\n", "E_IMPORT_OPERATOR"),
        ("operator-semantic-root", "operation = operator\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("operator-attrgetter-write",
         "operation = operator.attrgetter('write')(stream)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("operator-attrgetter-replace",
         "operation = operator.attrgetter('replace')(path)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("operator-methodcaller-touch",
         "operation = operator.methodcaller('touch')\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("operator-methodcaller-write",
         "operation = operator.methodcaller('write', data)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("underscore-operator-import", "import _operator\n", "E_IMPORT_OPERATOR"),
        ("underscore-operator-import-alias",
         "import _operator as operation_factory\n", "E_IMPORT_OPERATOR"),
        ("underscore-operator-import-from-attrgetter-alias",
         "from _operator import attrgetter as recover_attribute\n",
         "E_IMPORT_OPERATOR"),
        ("operator-import-from-methodcaller-alias",
         "from operator import methodcaller as recover_method\n",
         "E_IMPORT_OPERATOR"),
        ("underscore-operator-semantic-root",
         "operation_factory = _operator\n", "E_EXEC_ALIAS_SUBPROCESS"),
        ("arbitrary-receiver-attrgetter-write",
         "operation = helper.attrgetter('write')(stream)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("arbitrary-receiver-methodcaller-touch",
         "operation = helper.methodcaller('touch')(path)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("underscore-operator-attrgetter-write",
         "operation = _operator.attrgetter('write')(stream)\n",
         "E_EXEC_ALIAS_SUBPROCESS"),
        ("network-http-client-request",
         "import http.client\nhttp.client.HTTPSConnection(host).request('GET', '/')\n",
         "E_IMPORT_UNAPPROVED"),
        ("network-http-client-from-import",
         "from http.client import HTTPSConnection\nHTTPSConnection(host).request('GET', '/')\n",
         "E_IMPORT_UNAPPROVED"),
        ("network-ftplib-ftp",
         "import ftplib\nftplib.FTP(host)\n", "E_IMPORT_UNAPPROVED"),
        ("child-multiprocessing-process-start",
         "import multiprocessing\nmultiprocessing.Process(target=work).start()\n",
         "E_IMPORT_UNAPPROVED"),
        ("network-ssl-import", "import ssl\n", "E_IMPORT_UNAPPROVED"),
        ("network-smtplib-import", "import smtplib\n", "E_IMPORT_UNAPPROVED"),
        ("network-imaplib-import", "import imaplib\n", "E_IMPORT_UNAPPROVED"),
        ("network-poplib-import", "import poplib\n", "E_IMPORT_UNAPPROVED"),
        ("network-telnetlib-import", "import telnetlib\n", "E_IMPORT_UNAPPROVED"),
        ("child-asyncio-subprocess-import",
         "import asyncio.subprocess\n", "E_IMPORT_UNAPPROVED"),
        ("network-direct-http-client-root",
         "http.client.HTTPSConnection(host).request('GET', '/')\n",
         "E_EXEC_UNAPPROVED_ROOT"),
        ("network-direct-ftplib-root",
         "ftplib.FTP(host)\n", "E_EXEC_UNAPPROVED_ROOT"),
        ("child-direct-multiprocessing-root",
         "multiprocessing.Process(target=work).start()\n",
         "E_EXEC_UNAPPROVED_ROOT"),
        ("nested-sensitive", "def outer():\n    def run_git(*args):\n        return b''\n", "E_POLICY_NESTED_FUNCTION"),
        ("dynamic-eval", "eval('1+1')\n", "E_EXEC_EVAL"),
    )
    for name, source, expected in probes:
        errors = source_policy_source_errors(source)
        require(any(error.startswith(expected) for error in errors),
                "E_SOURCE_POLICY_NEGATIVE", f"{name}: {errors}")

    positive_probes = (
        ("filesystem-open-default-read", "data = open('input.txt').read()\n"),
        ("filesystem-open-literal-read", "data = open('input.txt', 'rb').read()\n"),
        ("filesystem-open-keyword-literal-read", "data = open('input.txt', mode='rt').read()\n"),
        ("filesystem-path-open-default-read",
         "data = pathlib.Path('input.txt').open().read()\n"),
        ("filesystem-path-open-literal-read",
         "data = pathlib.Path('input.txt').open('rt').read()\n"),
        ("getattr-exact-literal-safe", "line = getattr(node, 'lineno', 0)\n"),
    )
    for name, source in positive_probes:
        errors = source_policy_source_errors(source)
        require(not errors, "E_SOURCE_POLICY_POSITIVE", f"{name}: {errors}")

    default_tree = ast.parse("def expose[T]():\n    pass\n", feature_version=(3, 12))
    default_parameter = default_tree.body[0].type_params[0]
    default_parameter.default_value = ast.Name(id="run_git", ctx=ast.Load())
    ast.fix_missing_locations(default_tree)
    default_errors = source_policy_source_errors(
        ast.unparse(default_tree), tree_override=default_tree)
    require(any(error.startswith("E_EXEC_CAPTURE") for error in default_errors),
            "E_SOURCE_POLICY_NEGATIVE",
            f"annotation-type-param-default: {default_errors}")

    shape_probes = (
        ("builder-missing-required-definition", BUILDER, "builder", "run_git", None,
         "E_POLICY_DEFINITION_SET:run_git"),
        ("validator-missing-required-definition", VALIDATOR, "validator", "load_builder", None,
         "E_POLICY_DEFINITION_SET:load_builder"),
        ("builder-unexpected-loader-definition", BUILDER, "builder", None,
         "def load_builder():\n    return None\n", "E_POLICY_DEFINITION_SET:load_builder"),
        ("validator-unexpected-collector-definition", VALIDATOR, "validator", None,
         "def atomic_json_last_collect(output_dir):\n    return None\n",
         "E_POLICY_DEFINITION_SET:atomic_json_last_collect"),
        ("builder-missing-git-caller", BUILDER, "builder", "git_blob", None,
         "E_GIT_CALLER_MISSING:git_blob"),
        ("validator-missing-git-caller", VALIDATOR, "validator", "remote_tip", None,
         "E_GIT_CALLER_MISSING:remote_tip"),
    )
    for name, path, shape, removed_function, appended_source, expected in shape_probes:
        tree = ast.parse(path.read_text(encoding="utf-8"), feature_version=(3, 12))
        if removed_function is not None:
            tree.body = [node for node in tree.body
                         if not (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                                 and node.name == removed_function)]
        if appended_source is not None:
            tree.body.extend(ast.parse(appended_source, feature_version=(3, 12)).body)
        errors = source_policy_source_errors(ast.unparse(tree), expected_shape=shape)
        require(any(error.startswith(expected) for error in errors),
                "E_SOURCE_POLICY_NEGATIVE", f"{name}: {errors}")

    sticky_alias_cases = (
        "filesystem-sticky-alias-sensitive-before-scalar-rebind",
        "filesystem-sticky-alias-scalar-before-sensitive-rebind",
        "filesystem-sticky-alias-conditional-sensitive-rebind",
        "filesystem-sticky-alias-loop-sensitive-rebind",
        "filesystem-sticky-alias-try-sensitive-rebind",
        "filesystem-sticky-alias-other-scope-rebind",
        "filesystem-sticky-alias-pinned-relocation-count-preserved",
    )
    validator_source = VALIDATOR.read_text(encoding="utf-8")
    for name in sticky_alias_cases:
        tree = ast.parse(validator_source, type_comments=True, feature_version=(3, 12))
        functions = {
            node.name: node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        control = functions["control_document_negative_probes"]
        original_index = next(
            index for index, statement in enumerate(control.body)
            if isinstance(statement, ast.Assign)
            and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
            and statement.targets[0].id == "original"
            and isinstance(statement.value, ast.Name)
            and statement.value.id == "CANONICAL_LEDGER")
        pinned_statement = control.body[original_index]
        scalar_statement = ast.parse("original = None").body[0]
        mutation_statement = ast.parse("original.mutate_anything()").body[0]
        if name.endswith("sensitive-before-scalar-rebind"):
            replacement = [pinned_statement, scalar_statement, mutation_statement]
        elif name.endswith("scalar-before-sensitive-rebind"):
            replacement = [scalar_statement, pinned_statement, mutation_statement]
        elif name.endswith("conditional-sensitive-rebind"):
            replacement = [
                scalar_statement,
                ast.If(test=ast.Name(id="flag", ctx=ast.Load()),
                       body=[pinned_statement], orelse=[]),
                mutation_statement,
            ]
        elif name.endswith("loop-sensitive-rebind"):
            replacement = [
                scalar_statement,
                ast.For(target=ast.Name(id="item", ctx=ast.Store()),
                        iter=ast.Tuple(elts=[ast.Constant(value=0, kind=None)],
                                       ctx=ast.Load()),
                        body=[pinned_statement], orelse=[], type_comment=None),
                mutation_statement,
            ]
        elif name.endswith("try-sensitive-rebind"):
            replacement = [
                scalar_statement,
                ast.Try(body=[pinned_statement], handlers=[], orelse=[], finalbody=[]),
                mutation_statement,
            ]
        else:
            control.body[original_index:original_index + 1] = [
                scalar_statement, mutation_statement]
            target_function = functions[
                "strict_json_negative_probes" if name.endswith("other-scope-rebind")
                else "root_guard_negative_probes"]
            target_function.body.insert(0, pinned_statement)
            replacement = None
        if replacement is not None:
            control.body[original_index:original_index + 1] = replacement
        ast.fix_missing_locations(tree)
        pinned_count = sum(
            sha256_bytes(canonical_bytes(stable_ast(statement)))
            == "a06b913601013675c2eb91518d1dc0af964fc539323414a5582fc634bc64110d"
            for statement in (candidate for candidate in ast.walk(tree)
                              if isinstance(candidate, ast.stmt)))
        require(pinned_count == 4, "E_SOURCE_POLICY_NEGATIVE",
                f"{name}: pinned-count={pinned_count}")
        errors = source_policy_source_errors(
            ast.unparse(tree), expected_shape="validator", tree_override=tree)
        require(any(error.startswith("E_FS_PATH_ESCAPE") for error in errors),
                "E_SOURCE_POLICY_NEGATIVE", f"{name}: {errors}")
    return (len(probes) + len(positive_probes) + len(shape_probes)
            + len(sticky_alias_cases) + 1)


def strict_json_negative_probes() -> int:
    probes = (
        b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'{"a":Infinity}\n',
        b'{"a":-Infinity}\n', b'{"a":1}', b'[1,2,3]\n',
    )
    rejected = 0
    for raw in probes:
        try:
            strict_load_bytes(raw)
        except (ValidationFailure, ValueError, UnicodeDecodeError, json.JSONDecodeError):
            rejected += 1
    require(rejected == len(probes), "E_STRICT_JSON_NEGATIVE", str(rejected))
    return rejected


def mutated_root_trees(snippet: str) -> tuple[ast.Module, ast.Module]:
    trees: list[ast.Module] = []
    for path in (V23_PATHS[0], V24_PATHS[0]):
        tree = ast.parse(git_raw(path).decode("utf-8"), filename=path,
                         mode="exec", feature_version=(3, 12))
        root = callable_index(tree)["GraphiteAnodeDischargeDQDV.solve_U_oc"]
        insert_at = 1 if (root.body and isinstance(root.body[0], ast.Expr)
                          and isinstance(root.body[0].value, ast.Constant)
                          and isinstance(root.body[0].value.value, str)) else 0
        root.body[insert_at:insert_at] = ast.parse(snippet, feature_version=(3, 12)).body
        ast.fix_missing_locations(tree)
        trees.append(tree)
    return trees[0], trees[1]


def root_guard_negative_probes(builder: Any) -> int:
    probes = (
        ("tol-math-isfinite", "if not math.isfinite(tol):\n    raise ValueError\n"),
        ("tol-direct-positive", "if tol <= 0:\n    raise ValueError\n"),
        ("tol-helper-positional", "validate_positive(tol)\n"),
        ("tol-helper-keyword", "validate_positive(value=tol)\n"),
        ("max-iter-integer", "if not isinstance(max_iter, int):\n    raise ValueError\n"),
        ("max-iter-direct-positive", "if max_iter <= 0:\n    raise ValueError\n"),
        ("max-iter-helper-positional", "validate_positive(max_iter)\n"),
        ("max-iter-helper-keyword", "validate_positive(value=max_iter)\n"),
        ("tol-match-subject", "match tol:\n    case _:\n        raise ValueError\n"),
        ("max-iter-match-guard",
         "match value:\n    case _ if max_iter <= 0:\n        raise ValueError\n"),
        ("tol-match-pattern-binding",
         "match value:\n    case {'tol': tol}:\n        raise ValueError\n"),
        ("max-iter-match-pattern-binding",
         "match value:\n    case [max_iter]:\n        raise ValueError\n"),
        ("tol-locals-subscript",
         "if locals()['tol'] <= 0:\n    raise ValueError\n"),
        ("tol-zero-vars-subscript",
         "if vars()['tol'] <= 0:\n    raise ValueError\n"),
        ("max-iter-locals-get",
         "if locals().get('max_iter', 0) <= 0:\n    raise ValueError\n"),
        ("tol-globals-subscript",
         "if globals()['tol'] <= 0:\n    raise ValueError\n"),
        ("tol-dynamic-helper-keyword",
         "validate_positive(value=locals()['tol'])\n"),
        ("tol-dynamic-membership",
         "if 'tol' not in locals():\n    raise ValueError\n"),
        ("max-iter-globals-get",
         "if globals().get('max_iter') is None:\n    raise ValueError\n"),
        ("tol-zero-vars-helper-container",
         "if validate_lookup(vars(), {'key': 'tol'}):\n    raise ValueError\n"),
        ("tol-globals-unpacked-positional",
         "if globals(*[])['tol'] <= 0:\n    raise ValueError\n"),
        ("max-iter-locals-unpacked-keyword",
         "if locals(**{}).get('max_iter', 0) <= 0:\n    raise ValueError\n"),
        ("tol-vars-unpacked-positional",
         "if vars(*())['tol'] <= 0:\n    raise ValueError\n"),
        ("tol-dynamic-namespace-reference-alias",
         "namespace = globals\nif namespace()['tol'] <= 0:\n    raise ValueError\n"),
        ("max-iter-dynamic-namespace-tuple-index",
         "namespace = (locals,)[0]\nif namespace().get('max_iter') is None:\n    raise ValueError\n"),
        ("tol-builtins-getattr-namespace",
         "import builtins\nif getattr(builtins, 'globals')()['tol'] <= 0:\n    raise ValueError\n"),
        ("max-iter-dunder-builtins-getattr-namespace",
         "if getattr(__builtins__, 'locals')().get('max_iter') is None:\n    raise ValueError\n"),
        ("tol-dynamic-namespace-container-alias",
         "container = {'namespace': vars}\nif container['namespace']()['tol'] <= 0:\n    raise ValueError\n"),
        ("tol-namespace-helper-body-separated-key",
         "def namespace_helper():\n    return globals\nif validate_key('tol'):\n    raise ValueError\n"),
        ("max-iter-namespace-alias-separated-key",
         "namespace = locals\nif 'max_iter' in validation_config:\n    raise ValueError\n"),
        ("tol-builtins-helper-body-separated-key",
         "def namespace_helper():\n    return getattr(builtins, dynamic_name)\nif validate_key('tol'):\n    raise ValueError\n"),
        ("max-iter-dunder-builtins-computed-separated-key",
         "namespace = getattr((__builtins__ if flag else fallback), dynamic_name)\nif 'max_iter' in validation_config:\n    raise ValueError\n"),
        ("tol-import-builtins-alias-separated-key",
         "import builtins as namespace\nif validate_key('tol'):\n    raise ValueError\n"),
        ("max-iter-import-from-builtins-separated-key",
         "from builtins import locals as namespace\nif validate_key('max_iter'):\n    raise ValueError\n"),
        ("tol-dunder-import-builtins-separated-key",
         "namespace = __import__('builtins')\nif validate_key('tol'):\n    raise ValueError\n"),
        ("max-iter-computed-import-builtins-separated-key",
         "namespace = __import__('built' + 'ins')\nif validate_key('max_iter'):\n    raise ValueError\n"),
        ("tol-eval-danger-separated-key",
         "namespace = eval('1')\nif validate_key('tol'):\n    raise ValueError\n"),
        ("max-iter-exec-danger-separated-key",
         "exec('namespace = 1')\nif validate_key('max_iter'):\n    raise ValueError\n"),
        ("tol-compile-danger-separated-key",
         "namespace = compile('1', '<x>', 'eval')\nif validate_key('tol'):\n    raise ValueError\n"),
        ("tol-frame-f-locals-lookup",
         "if sys._getframe().f_locals['tol'] <= 0:\n    raise ValueError\n"),
        ("max-iter-currentframe-lookup",
         "if inspect.currentframe().f_locals.get('max_iter') is None:\n    raise ValueError\n"),
        ("tol-sys-modules-builtins-separated-key",
         "namespace = sys.modules['builtins']\nif validate_key('tol'):\n    raise ValueError\n"),
        ("max-iter-import-module-builtins-separated-key",
         "namespace = importlib.import_module('builtins')\nif validate_key('max_iter'):\n    raise ValueError\n"),
        ("tol-eval-attribute-content-key",
         "danger = helper.eval\nif validate_key('invalid tol value'):\n    raise ValueError\n"),
        ("max-iter-exec-attribute-content-key",
         "danger = helper.exec\nif validate_key('max_iter must be positive'):\n    raise ValueError\n"),
        ("tol-compile-name-folded-key",
         "danger = compile\nif validate_key('to' + 'l'):\n    raise ValueError\n"),
        ("max-iter-import-module-attribute-folded-key",
         "danger = helper.import_module\nif validate_key('max_' + 'iter'):\n    raise ValueError\n"),
        ("tol-getframe-alias-content-key",
         "danger = frame_api._getframe\nif validate_key('bad tol input'):\n    raise ValueError\n"),
        ("max-iter-currentframe-alias-content-key",
         "danger = frame_api.currentframe\nif validate_key('bad max_iter input'):\n    raise ValueError\n"),
        ("tol-modules-alias-content-key",
         "danger = runtime.modules['builtins']\nif validate_key('tol invalid'):\n    raise ValueError\n"),
        ("max-iter-computed-getattr-danger-folded-key",
         "danger = getattr(provider, 'import_' + 'module')\nif validate_key('max_' + 'iter'):\n    raise ValueError\n"),
        ("tol-computed-getattr-eval-content-key",
         "danger = getattr(provider, 'ev' + 'al')\nif validate_key('invalid tol'):\n    raise ValueError\n"),
        ("max-iter-f-locals-alias-content-key",
         "danger = frame.f_locals\nif validate_key('max_iter invalid'):\n    raise ValueError\n"),
        ("tol-eval-format-control-predicate",
         "if eval('{}{}'.format('to', 'l')):\n    raise ValueError\n"),
        ("max-iter-eval-join-control-predicate",
         "if eval(''.join(['max_', 'iter'])):\n    raise ValueError\n"),
        ("tol-eval-percent-control-predicate",
         "if eval('%s' % 'tol'):\n    raise ValueError\n"),
        ("max-iter-eval-alias-control-predicate",
         "runner = eval\nif runner('max_' + 'iter'):\n    raise ValueError\n"),
        ("dynamic-eval-nested-helper-outside-control",
         "def checker():\n    return eval(rule)\nmarker = checker\n"),
        ("dynamic-exec-alias-outside-control",
         "runner = exec\nmarker = runner\n"),
        ("dynamic-computed-frame-helper-outside-control",
         "def helper():\n    return getattr(sys, '_get' + 'frame')\nmarker = 1\n"),
        ("dynamic-inspect-helper-outside-control",
         "def helper():\n    return inspect.currentframe\nmarker = 1\n"),
        ("dynamic-getattr-nested-helper-outside-control",
         "def helper():\n    return getattr(provider, dynamic_name)\nmarker = helper\n"),
        ("dynamic-getattr-lambda-outside-control",
         "helper = lambda: getattr(provider, dynamic_name)\nmarker = helper\n"),
        ("dynamic-dunder-globals-nested-helper-outside-control",
         "def helper():\n    return checker.__globals__\nmarker = helper\n"),
        ("dynamic-dunder-globals-lambda-outside-control",
         "helper = lambda: checker.__globals__\nmarker = helper\n"),
        ("dynamic-dunder-builtins-helper-outside-control",
         "def helper():\n    return checker.__builtins__\nmarker = helper\n"),
        ("dynamic-dunder-getattribute-lambda-outside-control",
         "helper = lambda: checker.__getattribute__(dynamic_name)\nmarker = helper\n"),
        ("ordinary-tol-assignment-alias", "alias = tol\n"),
        ("ordinary-max-iter-container", "container = [max_iter]\n"),
        ("ordinary-watched-destructuring-value", "left, right = tol, max_iter\n"),
        ("ordinary-tol-helper-default", "def helper(value=tol):\n    return value\n"),
        ("ordinary-max-iter-lambda-capture", "helper = lambda: max_iter\n"),
    )
    for name, snippet in probes:
        old_tree, new_tree = mutated_root_trees(snippet)
        builder_rejected = False
        try:
            builder.defect_boundaries(old_tree, new_tree)
        except builder.BuildFailure as exc:
            builder_rejected = str(exc).startswith("E_ROOT_GUARD_BOUNDARY")
        _, independent_errors = independent_defect_boundaries(old_tree, new_tree)
        independent_rejected = any(error.startswith("root tol max_iter guard absence")
                                   for error in independent_errors)
        require(builder_rejected and independent_rejected, "E_ROOT_GUARD_NEGATIVE",
                f"{name}: builder={builder_rejected}, independent={independent_errors}")
    return len(probes)


def loader_dataflow_negative_probes(builder: Any) -> int:
    reserved_role_spellings = (
        "eval", "exec", "compile", "__import__", "import_module",
        "_getframe", "currentframe", "f_locals", "f_globals", "__globals__",
        "__getattribute__", "getattr", "attrgetter", "methodcaller",
        "subprocess", "os", "importlib", "sys", "inspect", "builtins",
        "__builtins__", "operator", "_operator", "globals", "locals", "vars",
    )
    probes = (
        ("loader-cross-function-same-spelling",
         "import importlib.util\ndef make_spec():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\ndef make_module():\n    module = importlib.util.module_from_spec(spec)\ndef execute():\n    spec.loader.exec_module(module)\n"),
        ("loader-spec-rebound",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-module-rebound",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nmodule = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-lambda-cross-scope",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nexecute = lambda: spec.loader.exec_module(module)\n"),
        ("loader-if-spec-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nif True:\n    spec = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-if-module-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nif True:\n    module = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-try-body-spec-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ntry:\n    spec = replacement\nexcept Exception:\n    pass\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-except-module-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\ntry:\n    pass\nexcept Exception:\n    module = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-finally-spec-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ntry:\n    pass\nfinally:\n    spec = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-loop-spec-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nfor item in values:\n    spec = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-with-module-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nwith context():\n    module = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-match-spec-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmatch value:\n    case _:\n        spec = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-while-module-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nwhile flag:\n    module = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-spec-loader-assign",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec.loader = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-spec-exec-module-assign",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-spec-dict-subscript-assign",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec.__dict__['loader'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-delete-spec-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndel spec.loader\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-augassign-spec-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec.loader += replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-annassign-spec-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec.loader: object = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-walrus-spec-rebind",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\n(spec := replacement)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-module-attribute-assign",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nmodule.state = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-setattr-spec-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nsetattr(spec, 'loader', replacement)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-delattr-spec-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndelattr(spec, 'loader')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-setattr-loader-exec-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nsetattr(spec.loader, 'exec_module', replacement)\nspec.loader.exec_module(module)\n"),
        ("loader-setattr-getattr-loader-exec-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nsetattr(getattr(spec, 'loader'), 'exec_module', replacement)\nspec.loader.exec_module(module)\n"),
        ("loader-getattr-setattr-helper",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\ngetattr(spec, '__setattr__')('loader', replacement)\nspec.loader.exec_module(module)\n"),
        ("loader-vars-spec-subscript-assign",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nvars(spec)['loader'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-getattr-spec-dict-subscript-assign",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ngetattr(spec, '__dict__')['loader'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-alias-spec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nalias = spec\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-alias-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nloader = spec.loader\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-alias-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nalias = module\nspec.loader.exec_module(module)\n"),
        ("loader-adjacent-alias-chain",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nloader = spec.loader\nalias = loader\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-object-setattr-spec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nobject.__setattr__(spec, 'loader', replacement)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-object-setattr-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nobject.__setattr__(spec.loader, 'exec_module', replacement)\nspec.loader.exec_module(module)\n"),
        ("loader-dict-update",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec.__dict__.update({'loader': replacement})\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dict-setitem",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nspec.__dict__.__setitem__('loader', replacement)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-operator-setitem",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\noperator.setitem(spec.__dict__, 'loader', replacement)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-unknown-mutator-spec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmutate(spec)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-unknown-mutator-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nmutate(module)\nspec.loader.exec_module(module)\n"),
        ("loader-unknown-mutator-loader",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nmutate(spec.loader)\nspec.loader.exec_module(module)\n"),
        ("loader-vars-mapping-update",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmapping = vars(spec)\nmapping.update({'loader': replacement})\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-getattr-loader-alias",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nloader = getattr(spec, 'loader')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-globals-spec-mutation",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nglobals()['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-locals-module-mutation",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nlocals()['module'] = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-zero-vars-spec-mutation",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nvars()['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-globals-spec-pass",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmutate(globals()['spec'])\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-locals-module-get",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nlocals().get('module')\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-namespace-alias",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nnamespace = globals()\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-namespace-container-pass",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ncapture({'namespace': locals()})\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-globals-unpacked-spec-mutation",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nglobals(*[])['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-locals-unpacked-module-pass",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nmutate(locals(**{}).get('module'))\nspec.loader.exec_module(module)\n"),
        ("loader-vars-unpacked-spec-pass",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmutate(vars(*())['spec'])\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-namespace-reference-alias",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nnamespace = globals\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-namespace-tuple-index",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nnamespace = (locals,)[0]\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-builtins-getattr-spec-mutation",
         "import builtins\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ngetattr(builtins, 'globals')()['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-builtins-getattr-module-pass",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nmutate(getattr(__builtins__, 'locals')().get('module'))\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-namespace-container-reference",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ncapture({'namespace': vars})\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-namespace-helper-before-candidate",
         "import importlib.util\ndef namespace_helper():\n    return globals\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-namespace-alias-before-candidate",
         "import importlib.util\nnamespace = locals\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-builtins-computed-before-candidate",
         "import importlib.util\nnamespace = getattr((builtins if flag else fallback), dynamic_name)\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-builtins-helper-before-candidate",
         "import importlib.util\ndef namespace_helper():\n    return __builtins__\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-builtins-alias-scopewide",
         "import builtins as namespace\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-builtins-scopewide",
         "from builtins import globals as namespace\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-import-builtins-scopewide",
         "import importlib.util\nnamespace = __import__('builtins')\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-computed-import-builtins-scopewide",
         "import importlib.util\nnamespace = __import__('built' + 'ins')\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-eval-before-spec",
         "import importlib.util\nnamespace = eval('1')\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-exec-between-spec-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nexec('namespace = 1')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-compile-between-module-exec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\ncompile('1', '<x>', 'eval')\nspec.loader.exec_module(module)\n"),
        ("loader-import-module-before-spec",
         "import importlib.util\nnamespace = importlib.import_module('builtins')\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-sys-getframe-f-locals",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nnamespace = sys._getframe().f_locals\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-inspect-currentframe",
         "import importlib.util\nnamespace = inspect.currentframe()\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-sys-modules-builtins",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nnamespace = sys.modules['builtins']\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-sys-alias-before-spec",
         "import importlib.util\nimport sys as runtime\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-sys-before-spec",
         "import importlib.util\nimport sys\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-inspect-alias-before-spec",
         "import importlib.util\nimport inspect as frame_api\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-bare-importlib-alias-before-spec",
         "import importlib as loader_api\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-import-module-before-spec",
         "from importlib import import_module as dynamic_import\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-getframe-before-spec",
         "from sys import _getframe as frame\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-currentframe-before-spec",
         "from inspect import currentframe as frame\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-aliased-import-module-attribute",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndanger = provider.import_module\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-computed-getattr-import-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndanger = getattr(provider, 'import_' + 'module')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-computed-getattr-sys-modules",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndanger = getattr(provider, 'mod' + 'ules')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-computed-getattr-currentframe",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndanger = getattr(provider, 'current' + 'frame')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frozen-mixed-import-sys-alias",
         "import numpy as np, importlib.util, sys\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nruntime = sys\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frozen-mixed-import-computed-getattr-sys",
         "import numpy as np, importlib.util, sys\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nruntime = getattr((sys,)[0], dynamic_name)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-sys-wildcard",
         "from sys import *\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-importlib-wildcard",
         "from importlib import *\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-inspect-wildcard",
         "from inspect import *\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-from-builtins-wildcard",
         "from builtins import *\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frozen-mixed-import-importlib-alias",
         "import numpy as np, importlib.util, sys\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nruntime = importlib\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frozen-mixed-import-importlib-container",
         "import numpy as np, importlib.util, sys\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nruntime = (importlib,)[0]\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frozen-mixed-import-stored-dynamic-spec-call",
         "import numpy as np, importlib.util, sys\nruntime = importlib\nspec = runtime.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frozen-mixed-import-stored-getattr-call",
         "import numpy as np, importlib.util, sys\nfactory = getattr(importlib.util, 'spec_from_file_location')\nspec = factory('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-untracked-exact-spec-consumer-before-chain",
         "import importlib.util\nconsume(importlib.util.spec_from_file_location('decoy', 'x.py'))\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-untracked-exact-spec-container-before-chain",
         "import importlib.util\nstash = [importlib.util.spec_from_file_location('decoy', 'x.py')]\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-untracked-exact-spec-attribute-target-before-chain",
         "import importlib.util\nholder.spec = importlib.util.spec_from_file_location('decoy', 'x.py')\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-untracked-exact-spec-multi-assignment-before-chain",
         "import importlib.util\nleft = right = importlib.util.spec_from_file_location('decoy', 'x.py')\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-untracked-exact-module-assignment-before-chain",
         "import importlib.util\ndecoy = importlib.util.module_from_spec(seed)\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-live-exact-module-multi-assignment",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nleft = right = importlib.util.module_from_spec(spec)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-globals-importlib-before-spec",
         "import importlib.util\nnamespace = helper.__globals__['importlib']\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-globals-spec-mutation",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nhelper.__globals__['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-globals-mapping-update",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nhelper.__globals__.update({'spec': replacement})\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-frame-f-globals-importlib",
         "import importlib.util\nnamespace = frame.f_globals['importlib']\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-sys-getframe-f-locals-spec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nsys._getframe().f_locals['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-inspect-currentframe-f-globals-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\ninspect.currentframe().f_globals['module'] = replacement\nspec.loader.exec_module(module)\n"),
        ("loader-dunder-getattribute-globals-spec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nhelper.__getattribute__('__globals__')['spec'] = replacement\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-getattr-general-receiver-before-spec",
         "import importlib.util\nattribute_name = '__globals__'\nnamespace = getattr(helper, attribute_name)\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dynamic-getattr-path-before-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\noperation = getattr(path, attribute_name)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-folded-getattr-frame-global-before-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nnamespace = getattr(frame, 'f_' + 'globals')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-folded-getattr-dunder-globals-before-exec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nnamespace = getattr(helper, '__glo' + 'bals__')\nspec.loader.exec_module(module)\n"),
        ("loader-getattr-alias-before-spec",
         "import importlib.util\nga = getattr\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-getattr-alias-call-before-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nga = getattr\noperation = ga(path, attribute_name)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-literal-getattr-before-exec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\noperation = getattr(path, 'read_text')\nspec.loader.exec_module(module)\n"),
        ("loader-operator-import-before-spec",
         "import operator\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-operator-import-from-before-spec",
         "from operator import attrgetter\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-operator-attrgetter-before-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\noperation = operator.attrgetter('touch')(path)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-operator-methodcaller-before-exec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\noperation = operator.methodcaller('replace', other)\nspec.loader.exec_module(module)\n"),
        ("loader-underscore-operator-import-before-spec",
         "import _operator\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-underscore-operator-import-alias-before-spec",
         "import _operator as operation_factory\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-underscore-operator-import-from-alias-before-spec",
         "from _operator import attrgetter as recover_attribute\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-underscore-operator-root-before-spec",
         "import importlib.util\noperation_factory = _operator\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-arbitrary-receiver-attrgetter-before-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\noperation = helper.attrgetter('write')(stream)\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-arbitrary-receiver-methodcaller-before-exec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\noperation = helper.methodcaller('touch')(path)\nspec.loader.exec_module(module)\n"),
        ("loader-dotted-operator-attrgetter-import-before-spec",
         "import operator.attrgetter as ag\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dotted-underscore-operator-attrgetter-import-before-spec",
         "import _operator.attrgetter as ag\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importlib-machinery-source-loader-before-spec",
         "import importlib.machinery as im\ndecoy = im.SourceFileLoader('x', 'x.py').load_module()\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importfrom-machinery-source-loader-before-spec",
         "from importlib.machinery import SourceFileLoader as L\ndecoy = L('x', 'x.py').load_module()\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dotted-operator-methodcaller-import-before-spec",
         "import operator.methodcaller as mc\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-dotted-underscore-operator-methodcaller-import-before-spec",
         "import _operator.methodcaller as mc\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importlib-abc-submodule-before-spec",
         "import importlib.abc as import_api\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importfrom-importlib-machinery-root-before-spec",
         "from importlib.machinery import ModuleSpec as ImportedSpec\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importlib-assignment-rebind",
         "import importlib.util\nimportlib = facade\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importlib-walrus-rebind",
         "import importlib.util\n(importlib := facade)\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-import-alias-as-importlib",
         "import facade as importlib\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-importfrom-alias-as-importlib",
         "from facade import loader_api as importlib\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-relative-import-importlib",
         "from . import importlib\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-function-parameter-importlib",
         "def load(importlib):\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-for-target-importlib",
         "import importlib.util\nfor importlib in providers:\n    pass\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-destructuring-importlib",
         "import importlib.util\n(importlib, marker) = pair\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-nested-after-module-assignment-rebind",
         "import importlib.util\nimportlib = facade\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-after-module-import-alias-rebind",
         "import importlib.util\nimport facade as importlib\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-after-module-for-target-rebind",
         "import importlib.util\nfor importlib in providers:\n    pass\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-after-module-with-target-rebind",
         "import importlib.util\nwith provider() as importlib:\n    pass\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-after-module-except-target-rebind",
         "import importlib.util\ntry:\n    pass\nexcept Exception as importlib:\n    pass\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-after-called-global-mutator-helper",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\nmutate()\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-after-globals-importlib-mutation",
         "import importlib.util\nglobals()['importlib'] = facade\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-nested-outer-closure-local-importlib",
         "import importlib.util\ndef outer():\n    importlib = facade\n    def load():\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\n    load()\nouter()\n"),
        ("loader-class-body-after-module-rebind",
         "import importlib.util\nimportlib = facade\nclass Loader:\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-class-method-after-module-rebind",
         "import importlib.util\nimport facade as importlib\nclass Loader:\n    def load(self):\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\nLoader().load()\n"),
        ("loader-definition-before-later-module-rebind",
         "import importlib.util\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nimportlib = facade\nload()\n"),
        ("loader-definition-after-relative-import-rebind",
         "import importlib.util\nfrom . import importlib\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-called-mutator-helper-alias",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\nalias = mutate\nalias()\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-called-mutator-function-default",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\ndef load(trigger=mutate()):\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-called-mutator-decorator",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\n@mutate()\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-called-mutator-container-indirect",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\n(mutate,)[0]()\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-facade-star-import-before-nested",
         "import importlib.util\nfrom facade import *\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-class-body-globals-importlib-mutation",
         "import importlib.util\nclass Trigger:\n    globals()['importlib'] = facade\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-class-base-called-mutator",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\nclass Loader(Trigger(mutate())):\n    def load(self):\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\nLoader().load()\n"),
        ("loader-class-keyword-called-mutator",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\nclass Loader(metaclass=Trigger(mutate())):\n    def load(self):\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\nLoader().load()\n"),
        ("loader-class-decorator-called-mutator",
         "import importlib.util\ndef mutate():\n    global importlib\n    importlib = facade\n@decorate(mutate())\nclass Loader:\n    def load(self):\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\nLoader().load()\n"),
        ("loader-nested-after-unknown-effectful-call",
         "import importlib.util\ntrigger_effect()\ndef load():\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\nload()\n"),
        ("loader-module-star-import-before-chain",
         "from facade import *\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-module-unknown-call-before-chain",
         "import importlib.util\ntrigger_effect()\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-module-uncertain-control-before-chain",
         "import importlib.util\nif flag:\n    marker = 1\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-property-read-before-chain",
         "import importlib.util\nmarker = source.property\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-subscript-read-before-chain",
         "import importlib.util\nmarker = source[key]\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-formatted-value-before-chain",
         "import importlib.util\nmarker = f'{source}'\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-comprehension-iteration-before-chain",
         "import importlib.util\nmarker = [item for item in source]\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-overloaded-binop-before-chain",
         "import importlib.util\nmarker = left + right\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-bare-decorator-before-chain",
         "import importlib.util\n@decorate\ndef helper():\n    pass\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-default-property-before-chain",
         "import importlib.util\ndef helper(value=source.property):\n    pass\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-yield-before-chain",
         "def load():\n    import importlib.util\n    yield marker\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-await-before-chain",
         "async def load():\n    import importlib.util\n    await marker\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-nested-function-canonical-chain",
         "def load():\n    import importlib.util\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-nested-class-method-canonical-chain",
         "class Loader:\n    def load(self):\n        import importlib.util\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\n"),
        ("loader-nested-function-default-poison",
         "def load(trigger=poison()):\n    import importlib.util\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-nested-function-call-decorator",
         "@decorate()\ndef load():\n    import importlib.util\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-nested-function-bare-decorator",
         "@decorate\ndef load():\n    import importlib.util\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-nested-after-enclosing-unknown-call",
         "poison()\ndef load():\n    import importlib.util\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-class-base-call-with-method-chain",
         "class Loader(poison()):\n    def load(self):\n        import importlib.util\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\n"),
        ("loader-class-metaclass-call-with-method-chain",
         "class Loader(metaclass=poison()):\n    def load(self):\n        import importlib.util\n        spec = importlib.util.spec_from_file_location('x', 'x.py')\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\n"),
        ("loader-nested-after-sys-modules-importlib-util-mutation",
         "import sys\nsys.modules['importlib.util'] = fake\ndef load():\n    import importlib.util\n    spec = importlib.util.spec_from_file_location('x', 'x.py')\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n"),
        ("loader-duplicate-canonical-import-before-spec",
         "import importlib.util\nimport importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-extra-literal-spec-before-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ndecoy = importlib.util.spec_from_file_location('y', 'y.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-extra-literal-spec-after-module",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\ndecoy = importlib.util.spec_from_file_location('y', 'y.py')\nspec.loader.exec_module(module)\n"),
        ("loader-extra-live-module-same-spec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\ndecoy = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"),
        ("loader-alternate-second-chain-before-first-exec",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nother_spec = importlib.util.spec_from_file_location('y', 'y.py')\nother_module = importlib.util.module_from_spec(other_spec)\nspec.loader.exec_module(module)\n"),
        ("loader-role-collision-same-target",
         "import importlib.util\nitem = importlib.util.spec_from_file_location('x', 'x.py')\nitem = importlib.util.module_from_spec(item)\nitem.loader.exec_module(item)\n"),
        ("loader-role-collision-importlib-spec-target",
         "import importlib.util\nimportlib = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(importlib)\nimportlib.loader.exec_module(module)\n"),
        ("loader-role-collision-importlib-module-target",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nimportlib = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(importlib)\n"),
        ("loader-role-collision-other-trusted-spec-target",
         "import importlib.util\nsys = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(sys)\nsys.loader.exec_module(module)\n"),
        ("loader-role-collision-other-trusted-module-target",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\ninspect = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(inspect)\n"),
        ("loader-role-near-adjacent-wrong-module-input",
         "import importlib.util\nitem_spec = importlib.util.spec_from_file_location('x', 'x.py')\nitem_module = importlib.util.module_from_spec(other_spec)\nitem_spec.loader.exec_module(item_module)\n"),
        ("loader-role-near-adjacent-wrong-exec-receiver",
         "import importlib.util\nitem_spec = importlib.util.spec_from_file_location('x', 'x.py')\nitem_module = importlib.util.module_from_spec(item_spec)\nitem_module.loader.exec_module(item_module)\n"),
        ("loader-role-near-adjacent-wrong-exec-argument",
         "import importlib.util\nitem_spec = importlib.util.spec_from_file_location('x', 'x.py')\nitem_module = importlib.util.module_from_spec(item_spec)\nitem_spec.loader.exec_module(item_spec)\n"),
    )
    probes += tuple(
        (f"loader-reserved-role-{spelling}-spec-target",
         "import importlib.util\n"
         f"{spelling} = importlib.util.spec_from_file_location('x', 'x.py')\n"
         f"module = importlib.util.module_from_spec({spelling})\n"
         f"{spelling}.loader.exec_module(module)\n")
        for spelling in reserved_role_spellings
    )
    probes += tuple(
        (f"loader-reserved-role-{spelling}-module-target",
         "import importlib.util\n"
         "spec = importlib.util.spec_from_file_location('x', 'x.py')\n"
         f"{spelling} = importlib.util.module_from_spec(spec)\n"
         f"spec.loader.exec_module({spelling})\n")
        for spelling in reserved_role_spellings
    )
    positive_probes = (
        ("loader-post-exec-independent-statements-and-mutation",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nmarker = 1\nnote = 'post-exec'\nspec.loader = replacement\n",
         4),
        ("loader-post-exec-dynamic-namespace",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nnamespace = globals()\n",
         4),
        ("loader-post-exec-sys-import",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nimport sys as runtime\n",
         4),
        ("loader-post-exec-mixed-import-no-retroactive-effect",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nimport numpy as np, sys\n",
         4),
        ("loader-post-exec-untracked-exact-call",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nconsume(importlib.util.spec_from_file_location('decoy', 'x.py'))\n",
         4),
        ("loader-post-exec-frame-namespace",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nnamespace = helper.__globals__\n",
         4),
        ("loader-post-exec-dynamic-getattr",
         "import importlib.util\nspec = importlib.util.spec_from_file_location('x', 'x.py')\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\noperation = getattr(path, attribute_name)\n",
         4),
        ("loader-distinct-near-adjacent-role-names",
         "import importlib.util\nitem_spec = importlib.util.spec_from_file_location('x', 'x.py')\nitem_module = importlib.util.module_from_spec(item_spec)\nitem_spec.loader.exec_module(item_module)\n",
         4),
        ("loader-role-case-sensitive-adjacent-spellings",
         "import importlib.util\nEval = importlib.util.spec_from_file_location('x', 'x.py')\nExec = importlib.util.module_from_spec(Eval)\nEval.loader.exec_module(Exec)\n",
         4),
        ("loader-role-dunder-adjacent-spellings",
         "import importlib.util\n__imported__ = importlib.util.spec_from_file_location('x', 'x.py')\n__globals_cache__ = importlib.util.module_from_spec(__imported__)\n__imported__.loader.exec_module(__globals_cache__)\n",
         4),
    )
    global git_raw
    validator_git_raw = git_raw
    builder_git_raw = builder.git_raw
    try:
        for name, source in probes:
            payload = source.encode("utf-8")

            def fake_git_raw(path: str, *, _payload: bytes = payload) -> bytes:
                return _payload if path == V24_PATHS[0] else b""

            git_raw = fake_git_raw
            builder.git_raw = fake_git_raw
            validator_rows = fresh_loader_census()
            builder_rows = builder.fresh_loader_census()
            require(not validator_rows and not builder_rows, "E_LOADER_DATAFLOW_NEGATIVE",
                    f"{name}: builder={builder_rows}, independent={validator_rows}")
        for name, source, expected_line in positive_probes:
            payload = source.encode("utf-8")

            def fake_git_raw(path: str, *, _payload: bytes = payload) -> bytes:
                return _payload if path == V24_PATHS[0] else b""

            git_raw = fake_git_raw
            builder.git_raw = fake_git_raw
            validator_rows = fresh_loader_census()
            builder_rows = builder.fresh_loader_census()
            expected = [(V24_PATHS[0], expected_line)]
            require(validator_rows == expected and builder_rows == expected,
                    "E_LOADER_DATAFLOW_POSITIVE",
                    f"{name}: builder={builder_rows}, independent={validator_rows}")
    finally:
        git_raw = validator_git_raw
        builder.git_raw = builder_git_raw
    return len(probes) + len(positive_probes)


def control_document_negative_probes() -> int:
    class TextDocument:
        def __init__(self, text: str) -> None:
            self.text = text

        def is_file(self) -> bool:
            return True

        def read_text(self, *, encoding: str) -> str:
            require(encoding == "utf-8", "E_CONTROL_DOCUMENT_ENCODING")
            return self.text

    stale_rows = (
        "| Step 71 | stale authoritative v4 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; semantic/source-policy/strict-JSON `53/46/6` |",
        "| Step 71 | stale authoritative v5 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; semantic/source-policy/strict-JSON `65/90/6` |",
        "| Step 71 | VERSION 5 pass-p065-step71-static-with-concerns; PASS PENDING persistence; semantic 65, source policy 90, strict json 6 |",
        "| Step 71 | v4: pass; semantic/source policy/strict json 53 / 46 / 6 |",
        "| Step 71 | version-6 PASS_PENDING; strict-json=6; source-policy=103; semantic=80 |",
        "| Step 71 | V 5 PASS; semantic:65 source-policy:90 strict JSON:6 |",
        "| Step 71 | v7 PASS_PENDING; semantic/source-policy/strict-JSON (65 / 90 / 6) |",
        "| Step 71 | v7 / VERSION 3 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic=102, source policy=120, strict JSON=6 |",
        "| Step 71 | v8 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `122/130/6`; semantic=53 |",
        "| Step 71 | V.8 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `122 / 130 / 6`; SOURCE_POLICY: 90 |",
        "| Step 71 | ATTEMPT 8 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `122/130/6`; Strict JSON=5 |",
        "| Step 71 | v8 / v.7 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `122/130/6` |",
        "| Step 71 | v8 / ATTEMPT: 7 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `122/130/6` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic ### <STALE_SEM> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; source policy === <STALE_SOURCE> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; strict JSON (<STALE_STRICT>) |",
        "| Step 71 | V#<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; STRICT JSON=<STRICT>, SOURCE POLICY=<STALE_SOURCE>, SEMANTIC=<SEM> |",
        "| Step 71 | attempt=<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic / <STALE_SEM> |",
        "| Step 71 | v<CURRENT> / v###8 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / ATTEMPT###8 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / VERSION(8) `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | version///<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; SOURCE POLICY / (<STALE_SOURCE>) |",
        "| Step 71 | v<CURRENT> / v8. `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic___<STALE_SEM> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; source_policy###<STALE_SOURCE> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; strict_JSON=(<STALE_STRICT>) |",
        "| Step 71 | v<CURRENT> / .v10. `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / _v10_ `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / .VERSION#10. `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / _ATTEMPT_10_ `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic unknown |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; source-policy= |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; strict-json=6.0 |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic=<SEM>x |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; source_policy=<SOURCE>.5 |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; strict_JSON=<STRICT>x |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic=<SEM>; source_policy unknown; strict_JSON=<STRICT> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic=<SEM>,<STALE_SEM> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; source-policy=<SOURCE>/<STALE_SOURCE> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; strict-json=-<STRICT> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; semantic=+<SEM> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; source-policy=x<SOURCE> |",
        "| Step 71 | v<CURRENT>old `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>`; strict-json=<STRICT> <STALE_STRICT> |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `-<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `+<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `.<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `x<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>.0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>x` |",
        "| Step 71 | v<CURRENT>.0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / v13.0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> / v13old `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `-   <SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `+  <SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>_0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>-0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>+0` |",
        "| Step 71 | version(-<CURRENT>) `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | attempt(+<CURRENT>) `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>_0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>-0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | version<CURRENT>.5 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `−   <SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>/0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>/ 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>: 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>,0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>; 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>. 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>_ 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>- 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>+ 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>− 0` |",
        "| Step 71 | version(− <CURRENT>) `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>/0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>/ 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>: 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>,0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>; 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>_ 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>− 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `－ <SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `± <SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `⁺ <SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | version(－ <CURRENT>) `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | attempt(± <CURRENT>) `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>?0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>! 0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>#0` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>· 0` |",
        "| Step 71 | v<CURRENT>?0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>! 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | version<CURRENT>#0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | attempt<CURRENT>· 0 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
    )
    positive_rows = (
        "| Step 71 | v<CURRENT>. release v1024 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | VERSION###<CURRENT>. `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic___<SEM>, SOURCE_POLICY==<SOURCE>, strict_JSON:(<STRICT>) |",
        "| Step 71 | attempt(<CURRENT>). release v1024 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> release v1024 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic___<SEM> ; SOURCE-POLICY:(<SOURCE>) ; strict_JSON###<STRICT> |",
        "| Step 71 | v<CURRENT>. `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `(<SEM>/<SOURCE>/<STRICT>)` |",
        "| Step 71 | v<CURRENT>. release v1.0.24 and v1024 `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT>? ordinary punctuation `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>` |",
        "| Step 71 | v<CURRENT> `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; PASS_PENDING_PERSISTENCE; semantic/source-policy/strict-JSON `<SEM>/<SOURCE>/<STRICT>? ordinary punctuation` |",
    )
    global CANONICAL_LEDGER, PARENT_LEDGER, RESULT
    original = CANONICAL_LEDGER
    original_parent = PARENT_LEDGER
    original_result = RESULT
    original_text = original.read_text(encoding="utf-8")
    current_row_match = re.search(
        r"^\|\s*Step\s*71\s*\|.*$", original_text,
        re.IGNORECASE | re.MULTILINE)
    require(current_row_match is not None, "E_CONTROL_DOCUMENT_NEGATIVE",
            "current authoritative row missing")
    current_row = current_row_match.group(0)
    current_attempt_match = re.search(r"\bv(\d{1,2})\b", current_row, re.IGNORECASE)
    require(current_attempt_match is not None, "E_CONTROL_DOCUMENT_NEGATIVE",
            "current attempt marker missing")
    current_attempt = current_attempt_match.group(1)
    current_counter_match = re.search(
        r"semantic/source-policy/strict-JSON\s*`?(\d+)\s*/\s*(\d+)\s*/\s*(\d+)",
        current_row, re.IGNORECASE)
    require(current_counter_match is not None, "E_CONTROL_DOCUMENT_NEGATIVE",
            "current counter triplet missing")
    current_counters = tuple(int(value) for value in current_counter_match.groups())
    replacements = {
        "<CURRENT>": current_attempt,
        "<SEM>": str(current_counters[0]),
        "<SOURCE>": str(current_counters[1]),
        "<STRICT>": str(current_counters[2]),
        "<STALE_SEM>": str(max(0, current_counters[0] - 1)),
        "<STALE_SOURCE>": str(max(0, current_counters[1] - 1)),
        "<STALE_STRICT>": str(max(0, current_counters[2] - 1)),
    }
    baseline_stale = [error for error in control_document_errors()
                      if error.startswith("authoritative row")]
    try:
        for index, stale_row in enumerate(stale_rows, start=1):
            for token, value in replacements.items():
                stale_row = stale_row.replace(token, value)
            mutated_text, replacement_count = re.subn(
                r"^\|\s*Step\s*71\s*\|.*$", stale_row, original_text,
                count=1, flags=re.IGNORECASE | re.MULTILINE)
            require(replacement_count == 1, "E_CONTROL_DOCUMENT_NEGATIVE",
                    f"case-{index}: authoritative Step 71 row replacement count "
                    f"{replacement_count}")
            CANONICAL_LEDGER = TextDocument(mutated_text)
            errors = control_document_errors()
            injected_stale = [error for error in errors
                              if error.startswith("authoritative row")]
            require(len(injected_stale) > len(baseline_stale),
                    "E_CONTROL_DOCUMENT_NEGATIVE", f"case-{index}: {errors}")
    finally:
        CANONICAL_LEDGER = original
    try:
        parent_text = original_parent.read_text(encoding="utf-8")
        PARENT_LEDGER = TextDocument(parent_text.replace(
            f"semantic/source-policy/strict-JSON "
            f"`{current_counters[0]}/{current_counters[1]}/{current_counters[2]}`",
            f"semantic/source-policy `{current_counters[0]}/{current_counters[1]}`"))
        errors = control_document_errors()
        require(any("parent" in error and "counter" in error for error in errors),
                "E_CONTROL_DOCUMENT_NEGATIVE", f"parent-missing-strict-json: {errors}")
    finally:
        PARENT_LEDGER = original_parent
    try:
        for index, positive_row in enumerate(positive_rows, start=1):
            for token, value in replacements.items():
                positive_row = positive_row.replace(token, value)
            positive_text, replacement_count = re.subn(
                r"^\|\s*Step\s*71\s*\|.*$", positive_row, original_text,
                count=1, flags=re.IGNORECASE | re.MULTILINE)
            require(replacement_count == 1, "E_CONTROL_DOCUMENT_POSITIVE",
                    f"case-{index}: row replacement count {replacement_count}")
            CANONICAL_LEDGER = TextDocument(positive_text)
            positive_errors = [error for error in control_document_errors()
                               if error.startswith("authoritative row")]
            require(not positive_errors, "E_CONTROL_DOCUMENT_POSITIVE",
                    f"case-{index}: {positive_errors}")
    finally:
        CANONICAL_LEDGER = original
    try:
        result_text = original_result.read_text(encoding="utf-8")
        final_policy_lines = [line for line in result_text.splitlines()
                              if line.startswith("Current final-policy counters:")]
        require(len(final_policy_lines) == 1, "E_CONTROL_DOCUMENT_NEGATIVE",
                f"final-policy marker count {len(final_policy_lines)}")
        final_policy_line = final_policy_lines[0]
        counter_match = re.fullmatch(
            r"Current final-policy counters: v(\d+); "
            r"semantic/source-policy/loader-negative/loader-positive/strict-JSON "
            r"`(\d+)/(\d+)/(\d+)/(\d+)/(\d+)`\.", final_policy_line)
        require(counter_match is not None, "E_CONTROL_DOCUMENT_NEGATIVE",
                f"final-policy marker malformed: {final_policy_line}")
        semantic_value = int(counter_match.group(2))
        stale_line = re.sub(
            r"`\d+/", f"`{max(0, semantic_value - 1)}/", final_policy_line, count=1)
        mutated_result, replacement_count = re.subn(
            rf"^{re.escape(final_policy_line)}$", stale_line, result_text,
            count=1, flags=re.MULTILINE)
        require(replacement_count == 1, "E_CONTROL_DOCUMENT_NEGATIVE",
                f"result-final-policy replacement count {replacement_count}")
        RESULT = TextDocument(mutated_result)
        errors = control_document_errors()
        require(any("result final-policy" in error for error in errors),
                "E_CONTROL_DOCUMENT_NEGATIVE", f"result-final-policy-stale: {errors}")
    finally:
        RESULT = original_result
    return len(stale_rows) + 2 + len(positive_rows)


def semantic_negative_probes(
        matrix: dict[str, Any], attestation: dict[str, Any], builder: Any) -> int:
    import copy

    source_mutation_cases = root_guard_negative_probes(builder)
    source_mutation_cases += loader_dataflow_negative_probes(builder)
    source_mutation_cases += control_document_negative_probes()

    init_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                      if row["callable"] == "BlendedAnodeDQDV.__init__"
                      and row["argument"] == "graphite_transitions")
    chi_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                     if row["callable"] == "GraphiteAnodeDischargeDQDV.__init__"
                     and row["argument"] == "chi")
    use_dh_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                        if row["callable"] == "GraphiteAnodeDischargeDQDV.__init__"
                        and row["argument"] == "use_dH_eff")
    lag_ratio_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                           if row["callable"] == "GraphiteAnodeDischargeDQDV.__init__"
                           and row["argument"] == "lag_ratio_correction")
    direction_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                           if row["callable"] == "GraphiteAnodeDischargeDQDV.curve"
                           and row["argument"] == "direction")
    blend_i_abs_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                             if row["callable"] == "BlendedAnodeDQDV.curve"
                             and row["argument"] == "I_abs")
    si_case_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                         if row["callable"] == "BlendedAnodeDQDV.__init__"
                         and row["argument"] == "si_case")
    si_stress_index = next(index for index, row in enumerate(matrix["initialization_rows"])
                           if row["callable"] == "BlendedAnodeDQDV.__init__"
                           and row["argument"] == "si_stress_offset")
    profile_index = next(index for index, row in enumerate(matrix["profile_surfaces"])
                         if row["profile_id"] == "GRAPHITE_STAGING_LIT")
    route_index = next(index for index, row in enumerate(matrix["feature_routes"])
                       if row["route_id"] == "P065-S71-ROUTE-BLEND-CURRENT")
    regsol_route_index = next(index for index, row in enumerate(matrix["feature_routes"])
                              if row["route_id"] == "P065-S71-ROUTE-REGSOL-EQUILIBRIUM")
    fresh_route_index = next(index for index, row in enumerate(matrix["feature_routes"])
                             if row["route_id"] == "P065-S71-ROUTE-FRESH-IMPORT")
    msrm6_route_index = next(index for index, row in enumerate(matrix["feature_routes"])
                             if row["route_id"] == "P065-S71-ROUTE-GRAPHITE-MSMR6")
    lco_route_index = next(index for index, row in enumerate(matrix["feature_routes"])
                           if row["route_id"] == "P065-S71-ROUTE-LCO-ELECTRONIC")
    defect_index = next(index for index, row in enumerate(matrix["defect_boundaries"])
                        if row["boundary_id"] == "CURRENT_PARTITION")
    seconds_defect_index = next(index for index, row in enumerate(matrix["defect_boundaries"])
                                if row["boundary_id"] == "SECONDS_HOUR")
    capacity_defect_index = next(index for index, row in enumerate(matrix["defect_boundaries"])
                                 if row["boundary_id"] == "CAPACITY_BASIS")
    root_defect_index = next(index for index, row in enumerate(matrix["defect_boundaries"])
                             if row["boundary_id"] == "ROOT_VALIDATION")
    fallback_defect_index = next(index for index, row in enumerate(matrix["defect_boundaries"])
                                 if row["boundary_id"] == "FALLBACK_ROUTES")
    finding_index = next(index for index, row in enumerate(matrix["findings"])
                         if row["finding_id"] == "P065-S71-F07")
    mutations: list[tuple[str, tuple[Any, ...], Any, str, bool]] = [
        ("expected-parent", ("matrix", "expected_parent"), "0" * 40, "expected parent", True),
        ("baseline", ("matrix", "baseline_commit"), "1" * 40, "baseline", True),
        ("gate", ("matrix", "gate"), "PASS_FALSE", "gate", True),
        ("step", ("matrix", "step"), 70, "step", True),
        ("grammar", ("matrix", "grammar", "feature_version"), [3, 14], "grammar contract", True),
        ("authority", ("matrix", "authority", "external_scientific"), True, "authority ceiling", True),
        ("endpoint-count", ("matrix", "endpoint_summary", "occurrences"), 19, "endpoint occurrences", True),
        ("unique-blob-count", ("matrix", "endpoint_summary", "unique_blobs"), 13, "endpoint unique blobs", True),
        ("endpoint-line", ("matrix", "endpoints", 0, "lines"), 1, "endpoint replay", True),
        ("endpoint-blob", ("matrix", "endpoints", 0, "blob"), "2" * 40, "endpoint replay", True),
        ("mirror-authority", ("matrix", "mirror", "independent_corroboration"), True, "mirror authority", True),
        ("mirror-blob", ("matrix", "mirror", "rows", 0, "blob"), "3" * 40, "mirror blob", True),
        ("branch", ("matrix", "source_policy", "active_branch"), "wrong", "source policy contract", True),
        ("protected-tip", ("matrix", "source_policy", "protected_tip"), "4" * 40, "source policy contract", True),
        ("main-tip", ("matrix", "source_policy", "main_tip"), "5" * 40, "source policy contract", True),
        ("exact-allowlist", ("matrix", "source_policy", "exact_paths"), [], "source policy contract", True),
        ("result-first", ("matrix", "source_policy", "result_first"), False, "source policy contract", True),
        ("json-last", ("matrix", "source_policy", "json_last"), False, "source policy contract", True),
        ("fresh-route", ("matrix", "route_outcomes", "fresh_import"), "IMPLEMENTED_AND_OBSERVED", "fresh route", True),
        ("explicit-profile-route", ("matrix", "route_outcomes", "explicit_profile"), "ABSENT_IN_FROZEN_SOURCE", "profile route", True),
        ("legacy-route", ("matrix", "route_outcomes", "legacy_restoration"), "IMPLEMENTED_AND_OBSERVED", "legacy route", True),
        ("saved-route", ("matrix", "route_outcomes", "current_saved_state"), "IMPLEMENTED_AND_OBSERVED", "saved route", True),
        ("independent-init-registry",
         ("matrix", "initialization_rows", init_index, "registry_default"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-fallback",
         ("matrix", "initialization_rows", init_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-chi-fallback",
         ("matrix", "initialization_rows", chi_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-use-dh-bool-gate",
         ("matrix", "initialization_rows", use_dh_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-lag-ratio-bool-gate",
         ("matrix", "initialization_rows", lag_ratio_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-si-case-routing",
         ("matrix", "initialization_rows", si_case_index, "profile_routes"), [],
         "independent initialization replay", True),
        ("independent-init-si-stress-zero",
         ("matrix", "initialization_rows", si_stress_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-direction-fallback",
         ("matrix", "initialization_rows", direction_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-init-blend-current-fallback",
         ("matrix", "initialization_rows", blend_i_abs_index, "fallback"), "WRONG",
         "independent initialization replay", True),
        ("independent-profile-route",
         ("matrix", "profile_surfaces", profile_index, "default_routes"), [],
         "independent profile replay", True),
        ("independent-feature-state",
         ("matrix", "feature_routes", route_index, "static_state"), "WRONG",
         "independent feature route replay", True),
        ("independent-feature-anchor",
         ("matrix", "feature_routes", route_index, "source_anchors"), [],
         "independent feature route replay", True),
        ("independent-feature-regsol-entry",
         ("matrix", "feature_routes", regsol_route_index, "entry"), "transition['kernel'] == 'regsol'",
         "independent feature route replay", True),
        ("independent-feature-fresh-loader",
         ("matrix", "feature_routes", fresh_route_index, "static_state"), "ABSENT_IN_FROZEN_SOURCE",
         "independent feature route replay", True),
        ("independent-feature-msmr6-state",
         ("matrix", "feature_routes", msrm6_route_index, "static_state"), "NO_RELEASE_REFERENCE",
         "independent feature route replay", True),
        ("independent-feature-msmr6-doc-census",
         ("matrix", "feature_routes", msrm6_route_index, "documentation_references"), [],
         "independent feature route replay", True),
        ("independent-feature-msmr6-python-census",
         ("matrix", "feature_routes", msrm6_route_index, "python_endpoint_activation_references"),
         ["wrong.py:1"], "independent feature route replay", True),
        ("independent-feature-v1023-lco-state",
         ("matrix", "feature_routes", lco_route_index, "v1023_state"), "OPTIONAL",
         "independent feature route replay", True),
        ("independent-defect-anchor",
         ("matrix", "defect_boundaries", defect_index, "v1024_anchors"), [],
         "independent defect replay", True),
        ("independent-defect-finding",
         ("matrix", "defect_boundaries", defect_index, "finding"), "WRONG",
         "independent defect replay", True),
        ("independent-defect-seconds-predicate",
         ("matrix", "defect_boundaries", seconds_defect_index,
          "validated_static_predicates"), [], "independent defect replay", True),
        ("independent-defect-capacity-predicate",
         ("matrix", "defect_boundaries", capacity_defect_index,
          "validated_static_predicates"), [], "independent defect replay", True),
        ("independent-defect-root-predicate",
         ("matrix", "defect_boundaries", root_defect_index,
          "validated_static_predicates"), [], "independent defect replay", True),
        ("independent-defect-fallback-predicate",
         ("matrix", "defect_boundaries", fallback_defect_index,
          "validated_static_predicates"), [], "independent defect replay", True),
        ("independent-saved-state-title",
         ("matrix", "findings", finding_index, "title"), "No model factory exists",
         "factory overclaim", True),
        ("defect-runtime", ("matrix", "defect_boundaries", 0, "runtime_conclusion"), "VALIDATED", "defect runtime ceiling", True),
        ("finding-severity", ("matrix", "findings", 0, "severity"), "P3", "finding severity", True),
        ("matrix-semantic", ("matrix", "semantic_sha256"), "6" * 64, "semantic hash", False),
        ("attestation-cross", ("attestation", "matrix_semantic_sha256"), "7" * 64, "matrix semantic cross binding", True),
        ("attestation-result", ("attestation", "result_sha256_lf"), "8" * 64, "result hash", True),
        ("attestation-semantic", ("attestation", "semantic_sha256"), "9" * 64, "semantic hash", False),
    ]
    rejected = 0
    for name, path, value, expected, rehash in mutations:
        m = copy.deepcopy(matrix)
        a = copy.deepcopy(attestation)
        target: Any = m if path[0] == "matrix" else a
        for key in path[1:-1]:
            target = target[key]
        target[path[-1]] = value
        if rehash and path[0] == "matrix":
            m["semantic_sha256"] = semantic_hash(m)
        elif rehash:
            a["semantic_sha256"] = semantic_hash(a)
        errors = artifact_errors(m, a, deep=name.startswith("independent-"))
        if any(expected in error for error in errors):
            rejected += 1
        else:
            fail("E_SEMANTIC_NEGATIVE", f"{name}: expected={expected!r}, errors={errors!r}")
    return rejected + source_mutation_cases


def determinism_check(builder: Any) -> int:
    first_matrix, first_attestation = builder.build_artifacts()
    second_matrix, second_attestation = builder.build_artifacts()
    first = (canonical_bytes(first_matrix), canonical_bytes(first_attestation))
    second = (canonical_bytes(second_matrix), canonical_bytes(second_attestation))
    require(first == second, "E_DETERMINISM")
    require(first == (MATRIX.read_bytes(), ATTESTATION.read_bytes()), "E_COLLECTED_DETERMINISM")
    return 2


def verify_branch_guards() -> None:
    require(str(run_git("rev-parse", "--abbrev-ref", "HEAD")).strip() == BRANCH, "E_BRANCH")
    require(str(run_git("rev-parse", "HEAD")).strip() == EXPECTED_PARENT, "E_PARENT")
    require(str(run_git("rev-parse", "--abbrev-ref", "@{upstream}")).strip() == f"origin/{BRANCH}", "E_UPSTREAM_NAME")
    require(str(run_git("rev-parse", "@{upstream}")).strip() == EXPECTED_PARENT, "E_UPSTREAM_PARENT")
    require(str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip() == EXPECTED_PARENT, "E_TRACKING_PARENT")
    require(remote_tip(BRANCH) == EXPECTED_PARENT, "E_LIVE_ACTIVE_PARENT")
    require(str(run_git("rev-parse", PROTECTED_BRANCH)).strip() == PROTECTED_TIP, "E_PROTECTED_LOCAL")
    require(str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip() == PROTECTED_TIP, "E_PROTECTED")
    require(remote_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_LIVE")
    require(str(run_git("rev-parse", "refs/remotes/origin/main")).strip() == MAIN_TIP, "E_MAIN")
    require(remote_tip("main") == MAIN_TIP, "E_MAIN_LIVE")
    require(not str(run_git("diff", "--name-only", PROTECTED_TIP, "HEAD", "--", "Claude")), "E_CLAUDE_DRIFT")


def verify_staged() -> None:
    rows = parse_name_status(str(run_git("diff", "--cached", "--name-status")))
    require(set(rows) == EXACT_EIGHT_SET, "E_STAGED_PATHS", repr(sorted(rows)))
    require(all(status in {"A", "M"} for status in rows.values()), "E_STAGED_STATUS", repr(rows))
    require(not str(run_git("diff", "--name-only")), "E_UNSTAGED")
    status = str(run_git("status", "--porcelain"))
    status_paths = {line[3:].replace("\\", "/") for line in status.splitlines() if line}
    require(status_paths == EXACT_EIGHT_SET, "E_STATUS_PATHS", repr(sorted(status_paths)))
    for path in EXACT_EIGHT:
        require(bytes(run_git("show", f":{path}", binary=True)) == (ROOT / path).read_bytes(), "E_INDEX_WORKTREE", path)
    require(not str(run_git("diff", "--cached", "--check")), "E_DIFF_CHECK")


def remote_tip(branch: str) -> str:
    output = str(run_git("ls-remote", "--heads", "origin", f"refs/heads/{branch}"))
    rows = [line.split()[0] for line in output.splitlines() if line.strip()]
    require(len(rows) == 1, "E_REMOTE_REF", branch)
    return rows[0]


def verify_persistence(expected_commit: str | None) -> None:
    require(expected_commit is not None and len(expected_commit) == 40, "E_EXPECTED_COMMIT")
    require(str(run_git("rev-parse", "--abbrev-ref", "HEAD")).strip() == BRANCH,
            "E_PERSIST_BRANCH")
    require(str(run_git("rev-parse", "--abbrev-ref", "@{upstream}")).strip() == f"origin/{BRANCH}",
            "E_PERSIST_UPSTREAM_NAME")
    head = str(run_git("rev-parse", "HEAD")).strip()
    require(head == expected_commit, "E_PERSIST_HEAD")
    require(str(run_git("rev-parse", f"{head}^1")).strip() == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(str(run_git("show", "-s", "--format=%s", head)).strip() == SUBJECT, "E_COMMIT_SUBJECT")
    rows = parse_name_status(str(run_git("diff-tree", "--no-commit-id", "--name-status", "-r", head)))
    require(set(rows) == EXACT_EIGHT_SET, "E_COMMIT_PATHS", repr(sorted(rows)))
    require(str(run_git("rev-parse", "@{upstream}")).strip() == head, "E_PERSIST_UPSTREAM")
    require(str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip() == head, "E_PERSIST_TRACKING")
    require(remote_tip(BRANCH) == head, "E_PERSIST_LIVE")
    require(str(run_git("rev-parse", PROTECTED_BRANCH)).strip() == PROTECTED_TIP, "E_PERSIST_PROTECTED_LOCAL")
    require(str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip() == PROTECTED_TIP,
            "E_PERSIST_PROTECTED_TRACKING")
    require(remote_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PERSIST_PROTECTED_LIVE")
    require(str(run_git("rev-parse", "refs/remotes/origin/main")).strip() == MAIN_TIP,
            "E_PERSIST_MAIN_TRACKING")
    require(remote_tip("main") == MAIN_TIP, "E_PERSIST_MAIN_LIVE")
    require(not str(run_git("status", "--porcelain")), "E_PERSIST_DIRTY")
    require(not str(run_git("diff", "--name-only", PROTECTED_TIP, head, "--", "Claude")), "E_PERSIST_CLAUDE_DRIFT")
    for path in EXACT_EIGHT:
        require(bytes(run_git("show", f"{head}:{path}", binary=True)) == (ROOT / path).read_bytes(), "E_COMMIT_WORKTREE", path)


def validate(mode: str, expected_commit: str | None) -> dict[str, Any]:
    for path in (BUILDER, VALIDATOR):
        errors = source_policy_errors(path)
        require(not errors, "E_SOURCE_POLICY", f"{path.relative_to(ROOT)}: {errors}")
    matrix, matrix_traversal = strict_load_bytes(MATRIX.read_bytes())
    attestation, attestation_traversal = strict_load_bytes(ATTESTATION.read_bytes())
    errors = artifact_errors(matrix, attestation)
    require(not errors, "E_ARTIFACT", repr(errors))
    control_errors = control_document_errors()
    require(not control_errors, "E_CONTROLS", repr(control_errors))
    builder = load_builder()
    rebuilt_matrix, rebuilt_attestation = builder.build_artifacts()
    require(matrix == rebuilt_matrix and attestation == rebuilt_attestation, "E_REBUILD")
    semantic_cases = semantic_negative_probes(matrix, attestation, builder)
    strict_cases = strict_json_negative_probes()
    source_policy_cases = source_policy_negative_probes()
    determinism = determinism_check(builder)
    if mode == "content":
        verify_branch_guards()
    elif mode == "staged":
        verify_branch_guards()
        verify_staged()
    elif mode == "persistence":
        verify_persistence(expected_commit)
    else:
        fail("E_MODE", mode)
    return {
        "attestation_nodes": attestation_traversal["all_nodes"],
        "determinism": f"{determinism}/2",
        "matrix_nodes": matrix_traversal["all_nodes"],
        "mode": mode,
        "semantic_cases": semantic_cases,
        "source_policy_cases": source_policy_cases,
        "strict_json_cases": strict_cases,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--staged", action="store_true")
    modes.add_argument("--persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    mode = "persistence" if args.persistence else "staged" if args.staged else "content"
    try:
        summary = validate(mode, args.expected_commit)
    except (ValidationFailure, OSError, UnicodeDecodeError, SyntaxError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL_P065_STEP71_{mode.upper()} {exc}")
        return 1
    terminal = "PASS_P065_STEP71_PERSISTENCE" if mode == "persistence" else "PASS_P065_STEP71_STAGED" if mode == "staged" else "PASS_P065_STEP71_CONTENT"
    print(f"{terminal} {json.dumps(summary, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
