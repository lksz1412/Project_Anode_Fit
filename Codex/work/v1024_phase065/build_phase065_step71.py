#!/usr/bin/env python3
"""Build Phase 065 Step 71 static code/profile/default evidence.

The frozen Claude tree is read as Git blobs and parsed as source text.  It is
never imported or executed.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import pathlib
import subprocess
import sys
from typing import Any, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "d6f680b26fb59c24098f44ed633873a2c6419a4e"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase065): trace v1024 code profile defaults"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P065_STEP71_STATIC_WITH_CONCERNS"
MAIN_V23 = "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py"
MAIN_V24 = "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py"
RESULT_PATH = "Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md"
MATRIX_NAME = "PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"
ATTESTATION_NAME = "PHASE_065_STATIC_ROUTE_ATTESTATION.json"

V23_PATHS = (
    MAIN_V23,
    "Claude/docs/v1.0.23/test_gates_v1023.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py",
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py",
    "Claude/docs/v1.0.23/results/tools_check_structure.py",
)
V24_PATHS = (
    MAIN_V24,
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
    RESULT_PATH,
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)

AUTHORITY = {
    "canonical_model_selected": False,
    "external_experimental": False,
    "external_material": False,
    "external_primary_literature": False,
    "external_scientific": False,
    "internal_static_provenance": True,
    "publication_ready": False,
    "runtime_behavior_validated": False,
    "v1024_1_independent_corroboration": False,
}

PROFILE_NAMES = (
    "GRAPHITE_STAGING_LIT",
    "GRAPHITE_STAGING_XRD_v1024",
    "GRAPHITE_STAGING_MSMR6_LIT",
    "LCO_MSMR_LIT",
    "SI_ELEMENTAL_LIT",
    "SIOX_LIT",
    "SIC_LIT",
    "SI_CASE_SETS",
    "SI_CASE_GAPS",
    "SI_SPECIFIC_CAPACITY",
    "GRAPHITE_SPECIFIC_CAPACITY",
)

SELECTED_CALLABLES = (
    "GraphiteAnodeDischargeDQDV.__init__",
    "GraphiteAnodeDischargeDQDV.curve",
    "LCOCathodeDQDV.__init__",
    "BlendedAnodeDQDV.__init__",
    "BlendedAnodeDQDV.from_wt",
    "BlendedAnodeDQDV.curve",
)


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(f"{code}: {detail}" if detail else code)


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


def run_process(args: list[str]) -> bytes:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, check=False)
    require(proc.returncode == 0, "E_GIT_READ", proc.stderr.decode("utf-8", "replace").strip())
    return proc.stdout


def run_git(*args: str, binary: bool = False) -> bytes | str:
    raw = run_process(["git", *args])
    return raw if binary else raw.decode("utf-8", "strict")


def git_raw(path: str) -> bytes:
    return bytes(run_git("cat-file", "blob", f"{BASELINE}:{path}", binary=True))


def git_blob(path: str) -> str:
    return str(run_git("rev-parse", f"{BASELINE}:{path}")).strip()


def source_tree(path: str) -> tuple[str, ast.Module]:
    text = git_raw(path).decode("utf-8")
    return text, ast.parse(text, filename=path, mode="exec", feature_version=(3, 12))


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


def node_sha(node: ast.AST) -> str:
    return sha256_bytes(canonical_bytes(stable_ast(node)))


def endpoint(path: str) -> dict[str, Any]:
    raw = git_raw(path)
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=path, mode="exec", feature_version=(3, 12))
    lf = lf_bytes(raw)
    return {
        "path": path,
        "version": "v1.0.23" if "/v1.0.23/" in path else "v1.0.24.1" if "/v1.0.24.1/" in path else "v1.0.24",
        "blob": git_blob(path),
        "bytes": len(raw),
        "lines": len(lf.decode("utf-8").splitlines()),
        "sha256_raw": sha256_bytes(raw),
        "sha256_lf": sha256_bytes(lf),
        "ast_sha256": node_sha(tree),
        "parse_grammar": "PYTHON_3_12_AST",
        "parse_status": "STATIC_PARSE_PASS_NO_IMPORT",
        "function_nodes": sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree)),
        "class_nodes": sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree)),
        "import_nodes": sum(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree)),
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
    value = node.value
    require(value is not None, "E_ASSIGNMENT_VALUE")
    return value


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
        if not isinstance(current, ast.Dict):
            continue
        for key, value in zip(current.keys, current.values):
            if isinstance(key, ast.Constant) and key.value == "kernel":
                values.add(ast.unparse(value))
    return sorted(values)


def top_level_keys(node: ast.AST) -> list[str]:
    if not isinstance(node, ast.Dict):
        return []
    result: list[str] = []
    for key in node.keys:
        result.append(ast.unparse(key) if key is not None else "**")
    return result


def profile_surface(name: str, node: ast.Assign | ast.AnnAssign) -> dict[str, Any]:
    value = assignment_value(node)
    kind = type(value).__name__
    if isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
        entry_count: int | None = len(value.elts) if hasattr(value, "elts") else len(value.keys)
    else:
        entry_count = None
    default_routes = {
        "GRAPHITE_STAGING_LIT": ["BlendedAnodeDQDV.graphite_transitions=None"],
        "SI_CASE_SETS": ["BlendedAnodeDQDV.si_transitions=None"],
        "SI_CASE_GAPS": ["BlendedAnodeDQDV.gaps"],
        "SI_SPECIFIC_CAPACITY": ["BlendedAnodeDQDV.from_wt.q_Si=None"],
        "GRAPHITE_SPECIFIC_CAPACITY": ["BlendedAnodeDQDV.from_wt.q_gr"],
    }.get(name, [])
    return {
        "profile_id": name,
        "source_path": MAIN_V24,
        "source_blob": git_blob(MAIN_V24),
        "line_range": [node.lineno, node.end_lineno],
        "ast_kind": kind,
        "ast_sha256": node_sha(value),
        "entry_count": entry_count,
        "top_level_keys": top_level_keys(value),
        "recursive_transition_keys": recursive_dict_keys(value),
        "kernel_values": recursive_kernel_values(value),
        "contains_kernel_key": bool(recursive_kernel_values(value)),
        "default_routes": default_routes,
        "registry_authority": "STATIC_SOURCE_ONLY",
        "runtime_behavior_validated": False,
    }


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


def callable_source(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    return ast.unparse(ast.Module(body=[node], type_ignores=[]))


def symbol_load_anchors(paths: Iterable[str], symbol: str) -> list[str]:
    anchors: list[str] = []
    for path in paths:
        _, tree = source_tree(path)
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


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted_name(node.value)
        return None if prefix is None else f"{prefix}.{node.attr}"
    return None


def static_literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = static_literal_string(node.left)
        right = static_literal_string(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def target_names(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, (ast.Tuple, ast.List)):
        return set().union(*(target_names(item) for item in node.elts))
    return set()


def direct_statement_bindings(statement: ast.stmt) -> set[str]:
    names: set[str] = set()

    class SameScopeBindingVisitor(ast.NodeVisitor):
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
            names.update(alias.asname or alias.name.split(".")[0] for alias in node.names)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            names.update(alias.asname or alias.name for alias in node.names)

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

    SameScopeBindingVisitor().visit(statement)
    return names


def mutation_root_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, (ast.Attribute, ast.Subscript, ast.Starred)):
        return mutation_root_name(node.value)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in {"getattr", "vars"} and node.args):
        return mutation_root_name(node.args[0])
    return None


def direct_statement_mutation_roots(statement: ast.stmt) -> set[str]:
    roots: set[str] = set()

    class SameScopeMutationVisitor(ast.NodeVisitor):
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
                root = mutation_root_name(node)
                if root is not None:
                    roots.add(root)
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                root = mutation_root_name(node)
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
                root = mutation_root_name(target)
                if root is not None:
                    roots.add(root)
            self.generic_visit(node)

    SameScopeMutationVisitor().visit(statement)
    return roots


def loaded_names(node: ast.AST) -> set[str]:
    return {candidate.id for candidate in ast.walk(node)
            if isinstance(candidate, ast.Name) and isinstance(candidate.ctx, ast.Load)}


def contains_loader_danger(
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
                node_sha(candidate)
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
                and static_literal_string(candidate.slice) in dangerous_attributes):
            return True
    return False


def lexical_scopes(
        tree: ast.Module) -> list[
            ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda]:
    scopes: list[
        ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda] = [tree]
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            scopes.append(node)
    return scopes


FROZEN_LOADER_TREE_SHA256 = {
    "6c61f53ceef871e3320aad63d32d82b4e084abbeb9734d80866c3204e6e1ea26",
    "d5a0ad5e8355c7cbc4d8003590d165614f70af13ff7861f98d7d8df839b41886",
    "d9e3a89a37339aed1f5ea6b19f93825cf758d1ebb4336edc911d58607529ea9c",
    "9ffb4f9428986a86473914d305aafebc8dacd29124b5aca3ac649c6d95f657c5",
    "97e800c289c709f65edf6f9a0b3e36dbb4b9720260d32a1ed08bc10706f548e2",
}

LOADER_RESERVED_ROLE_NAMES = {
    "eval", "exec", "compile", "__import__", "import_module",
    "_getframe", "currentframe", "f_locals", "f_globals", "__globals__",
    "__getattribute__", "getattr", "attrgetter", "methodcaller",
    "subprocess", "os", "importlib", "sys", "inspect", "builtins",
    "__builtins__", "operator", "_operator", "globals", "locals", "vars",
}


def strict_precompletion_loader_danger(
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
        function = dotted_name(value.func)
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


def exact_trusted_importlib_statement(statement: ast.stmt) -> bool:
    return (
        isinstance(statement, ast.Import)
        and any(alias.name == "importlib.util" and alias.asname is None
                for alias in statement.names)
        and all((alias.asname or alias.name.split(".")[0]) != "importlib"
                or alias.name == "importlib.util" and alias.asname is None
                for alias in statement.names))


def same_scope_importlib_namespace_mutation(statement: ast.stmt) -> bool:
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

    class NamespaceMutationVisitor(ast.NodeVisitor):
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

    NamespaceMutationVisitor().visit(statement)
    return has_namespace and has_key and has_mutation


def same_scope_global_importlib_declaration(statement: ast.stmt) -> bool:
    found = False

    class GlobalDeclarationVisitor(ast.NodeVisitor):
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

    GlobalDeclarationVisitor().visit(statement)
    return found


def definition_mutates_enclosing_importlib(
        node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if any(isinstance(candidate, (ast.Global, ast.Nonlocal))
           and "importlib" in candidate.names for candidate in ast.walk(node)):
        return True
    return any(same_scope_importlib_namespace_mutation(statement)
               for statement in node.body)


def same_scope_called_names(statement: ast.stmt) -> set[str]:
    names: set[str] = set()

    class CalledNameVisitor(ast.NodeVisitor):
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

    CalledNameVisitor().visit(statement)
    return names


def importlib_scope_entry_trust(
        tree: ast.Module) -> dict[int, bool]:
    scope_types = (
        ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda,
    )
    parents: dict[int, ast.AST] = {}

    class ScopeParentVisitor(ast.NodeVisitor):
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

    ScopeParentVisitor().visit(tree)
    cache: dict[int, bool] = {id(tree): False}

    def statement_revokes(statement: ast.stmt) -> bool:
        if exact_trusted_importlib_statement(statement):
            return False
        return (
            "importlib" in direct_statement_bindings(statement)
            or same_scope_global_importlib_declaration(statement)
            or same_scope_importlib_namespace_mutation(statement))

    def replay(
            statements: list[ast.stmt], initial: bool,
            stop: ast.AST | None = None) -> tuple[bool, int | None, set[str]]:
        trusted = initial
        mutators: set[str] = set()
        for index, statement in enumerate(statements):
            if statement is stop:
                return trusted, index, mutators
            if (isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and definition_mutates_enclosing_importlib(statement)):
                mutators.add(statement.name)
            if same_scope_called_names(statement) & mutators:
                trusted = False
            if exact_trusted_importlib_statement(statement):
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
                    and definition_mutates_enclosing_importlib(statement)):
                mutators.add(statement.name)
            if (same_scope_called_names(statement) & mutators
                    or statement_revokes(statement)):
                trusted = False
                break
        cache[id(scope)] = trusted
        return trusted

    for scope in lexical_scopes(tree):
        resolve(scope)
    return cache


def canonical_nonfrozen_loader_exec_lines(tree: ast.Module) -> list[int]:
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
            and dotted_name(spec_statement.value.func)
            == "importlib.util.spec_from_file_location"
            and len(spec_statement.value.args) == 2
            and not spec_statement.value.keywords
            and all(isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                    for argument in spec_statement.value.args)):
        return []
    spec_name = spec_statement.targets[0].id
    if spec_name in LOADER_RESERVED_ROLE_NAMES:
        return []
    if not (isinstance(module_statement, ast.Assign)
            and len(module_statement.targets) == 1
            and isinstance(module_statement.targets[0], ast.Name)
            and isinstance(module_statement.value, ast.Call)
            and dotted_name(module_statement.value.func)
            == "importlib.util.module_from_spec"
            and len(module_statement.value.args) == 1
            and not module_statement.value.keywords
            and isinstance(module_statement.value.args[0], ast.Name)
            and module_statement.value.args[0].id == spec_name):
        return []
    module_name = module_statement.targets[0].id
    if module_name == spec_name or module_name in LOADER_RESERVED_ROLE_NAMES:
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


def lexical_loader_exec_lines(tree: ast.Module) -> list[int]:
    lines: list[int] = []
    generation = 0
    exact_frozen_loader_tree = node_sha(tree) in FROZEN_LOADER_TREE_SHA256
    if not exact_frozen_loader_tree:
        return canonical_nonfrozen_loader_exec_lines(tree)
    entry_trust = importlib_scope_entry_trust(tree)
    for scope in lexical_scopes(tree):
        if scope is not tree and not exact_frozen_loader_tree:
            continue
        specs: dict[str, int] = {}
        modules: dict[str, tuple[str, int]] = {}
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
                   "importlib" in direct_statement_bindings(statement)
                   and not (isinstance(statement, ast.Import)
                            and any(alias.name == "importlib.util"
                                    and alias.asname is None
                                    for alias in statement.names))
                   for statement in scope.body):
                danger_seen = True
        statements = ([ast.Expr(value=scope.body)] if isinstance(scope, ast.Lambda)
                      else scope.body)
        for statement in statements:
            bindings = direct_statement_bindings(statement)
            mutation_roots = direct_statement_mutation_roots(statement)
            trusted_import_statement = exact_trusted_importlib_statement(statement)
            if trusted_import_statement:
                trusted_importlib = True
            elif "importlib" in bindings:
                trusted_importlib = False
                danger_seen = True
            if any(isinstance(node, (ast.Global, ast.Nonlocal))
                   and "importlib" in node.names for node in ast.walk(statement)):
                trusted_importlib = False
                danger_seen = True

            def invalidate(name: str) -> None:
                specs.pop(name, None)
                modules.pop(name, None)
                for module_name, binding in list(modules.items()):
                    if binding[0] == name:
                        del modules[module_name]

            for name in bindings | mutation_roots:
                invalidate(name)
            value = statement.value if isinstance(statement, (ast.Assign, ast.AnnAssign)) else None
            targets = statement.targets if isinstance(statement, ast.Assign) else (
                [statement.target] if isinstance(statement, ast.AnnAssign) else [])
            target = targets[0].id if len(targets) == 1 and isinstance(targets[0], ast.Name) else None
            function = dotted_name(value.func) if isinstance(value, ast.Call) else None
            exact_spec_call = (
                target is not None and isinstance(value, ast.Call)
                and function == "importlib.util.spec_from_file_location"
                and len(value.args) == 2 and not value.keywords)
            module_spec_name = (value.args[0].id if target is not None
                                and function == "importlib.util.module_from_spec"
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
                    or module_spec_name in specs):
                require(isinstance(value, ast.Call), "E_LOADER_CALL_SHAPE")
                allowed_semantic_loads.update(
                    id(current) for current in ast.walk(value.func)
                    if isinstance(current, ast.Name)
                    and isinstance(current.ctx, ast.Load)
                    and current.id == "importlib")
            approved_call_ids: set[int] = set()
            if exact_spec_call and not danger_seen and trusted_importlib:
                approved_call_ids.add(id(value))
            if module_spec_name in specs:
                approved_call_ids.add(id(value))
            if exec_names is not None:
                spec_name, module_name = exec_names
                if modules.get(module_name) == (spec_name, specs.get(spec_name)):
                    approved_call_ids.add(id(call))
            if (not exact_frozen_loader_tree
                    and strict_precompletion_loader_danger(
                        statement, approved_call_ids)):
                danger_seen = True
                for name in list(specs) + list(modules):
                    invalidate(name)
            if contains_loader_danger(statement, allowed_semantic_loads):
                danger_seen = True
                for name in list(specs) + list(modules):
                    invalidate(name)
            permitted_live_loads: set[str] = set()
            if module_spec_name in specs:
                permitted_live_loads.add(module_spec_name)
            if exec_names is not None:
                spec_name, module_name = exec_names
                if modules.get(module_name) == (spec_name, specs.get(spec_name)):
                    permitted_live_loads.update(exec_names)
            live_names = set(specs) | set(modules)
            for name in (loaded_names(statement) & live_names) - permitted_live_loads:
                invalidate(name)
            if target is not None and isinstance(value, ast.Call):
                if exact_spec_call and not danger_seen and trusted_importlib:
                    generation += 1
                    specs[target] = generation
                elif module_spec_name in specs:
                    modules[target] = (module_spec_name, specs[module_spec_name])
            if call is not None and exec_names is not None:
                spec_name, module_name = exec_names
                binding = modules.get(module_name)
                if binding is not None and binding == (spec_name, specs.get(spec_name)):
                    lines.append(call.lineno)
    return sorted(lines)


def fresh_loader_census() -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    for path in V24_PATHS:
        _, tree = source_tree(path)
        rows.extend((path, line) for line in lexical_loader_exec_lines(tree))
    return sorted(rows)


def argument_defaults(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[tuple[str, str]]:
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


def initialization_detail(callable_name: str, argument: str, declared: str) -> tuple[Any, Any, str, list[str], list[str]]:
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
        fallback = "forwarded through super().__init__ to GraphiteAnodeDischargeDQDV without schema registry"
    elif key == ("BlendedAnodeDQDV.__init__", "**host_kwargs"):
        fallback = "forwarded to GraphiteAnodeDischargeDQDV without schema registry"
    elif key == ("BlendedAnodeDQDV.from_wt", "**kwargs"):
        fallback = "forwarded to BlendedAnodeDQDV.__init__; host kwargs are then forwarded without schema registry"
    elif key == ("BlendedAnodeDQDV.curve", "I_abs"):
        fallback = "forwarded to both host curve methods; None -> each host derives abs(c_rate * Q_cell)"
    return registry, factory, fallback, routes, conflicts


def initialization_rows(tree: ast.Module) -> list[dict[str, Any]]:
    index = callable_index(tree)
    evidence = {
        ("GraphiteAnodeDischargeDQDV.__init__", "use_dH_eff"): (
            "self.use_dH_eff = bool(use_dH_eff)",),
        ("GraphiteAnodeDischargeDQDV.__init__", "lag_ratio_correction"): (
            "self.lag_ratio_correction = bool(lag_ratio_correction)",),
        ("BlendedAnodeDQDV.__init__", "si_case"): (
            "self.si_case = si_case", "if si_transitions is None",
            "SI_CASE_SETS[si_case]", "SI_CASE_GAPS.get(si_case, [])"),
        ("BlendedAnodeDQDV.__init__", "si_stress_offset"): (
            "self.si_stress_offset = si_stress_offset",
            "if si_stress_offset is not None",
            "_finite('si_stress_offset', si_stress_offset)", "for tr in si_trs"),
    }
    for (callable_name, argument), needles in evidence.items():
        source = callable_source(index[callable_name])
        require(all(needle in source for needle in needles), "E_INITIALIZATION_EVIDENCE",
                f"{callable_name}.{argument}")
    rows: list[dict[str, Any]] = []
    for callable_name in SELECTED_CALLABLES:
        require(callable_name in index, "E_CALLABLE", callable_name)
        node = index[callable_name]
        for argument, declared in argument_defaults(node):
            registry, factory, fallback, routes, conflicts = initialization_detail(
                callable_name, argument, declared)
            rows.append({
                "callable": callable_name,
                "source_path": MAIN_V24,
                "source_blob": git_blob(MAIN_V24),
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
    return node_sha(ast.Module(body=body, type_ignores=[]))


def lineage_pairs(v23_tree: ast.Module, v24_tree: ast.Module) -> list[dict[str, Any]]:
    old = callable_index(v23_tree)
    new = callable_index(v24_tree)
    rows: list[dict[str, Any]] = []
    for name in sorted(set(old) | set(new)):
        left = old.get(name)
        right = new.get(name)
        if left is None:
            status = "ADDED_V1024"
        elif right is None:
            status = "REMOVED_V1024"
        elif node_sha(left) == node_sha(right):
            status = "AST_IDENTICAL"
        elif signature_text(left) != signature_text(right):
            status = "SIGNATURE_CHANGED"
        elif executable_sha(left) == executable_sha(right):
            status = "DOCSTRING_OR_ANNOTATION_CHANGED_EXECUTABLE_IDENTICAL"
        else:
            status = "EXECUTABLE_BODY_CHANGED_SIGNATURE_STABLE"
        rows.append({
            "symbol": name,
            "status": status,
            "v1023_line_range": None if left is None else [left.lineno, left.end_lineno],
            "v1024_line_range": None if right is None else [right.lineno, right.end_lineno],
            "v1023_ast_sha256": None if left is None else node_sha(left),
            "v1024_ast_sha256": None if right is None else node_sha(right),
            "v1023_executable_sha256": None if left is None else executable_sha(left),
            "v1024_executable_sha256": None if right is None else executable_sha(right),
            "v1023_signature": None if left is None else signature_text(left),
            "v1024_signature": None if right is None else signature_text(right),
        })
    return rows


def route(route_id: str, static_state: str, source_anchors: list[str], **extra: Any) -> dict[str, Any]:
    row = {
        "route_id": route_id,
        "static_state": static_state,
        "source_anchors": source_anchors,
        "runtime_behavior_validated": False,
        "authority_promoted": False,
    }
    row.update(extra)
    return row


def feature_routes(v23_tree: ast.Module, v24_tree: ast.Module) -> list[dict[str, Any]]:
    old_callables = callable_index(v23_tree)
    new_callables = callable_index(v24_tree)
    assignments = assignment_index(v24_tree)
    old_lco = callable_source(old_callables["LCOCathodeDQDV._effective_dS_rxn"])
    require("if tr.get('electronic')" in old_lco
            and "include_electronic_entropy" not in old_lco,
            "E_V1023_LCO_UNCONDITIONAL")
    msrm_python = symbol_load_anchors(V24_PATHS, "GRAPHITE_STAGING_MSMR6_LIT")
    require(not msrm_python, "E_MSMR6_PYTHON_ACTIVATION", repr(msrm_python))
    msrm_docs = text_reference_anchors(MSMR6_DOC_PATHS, "GRAPHITE_STAGING_MSMR6_LIT")
    expected_docs = [
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.md:284",
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.md:334",
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.html:183",
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.html:210",
        "Claude/docs/v1.0.24/results/HANDOVER_v24.md:73",
        "Claude/docs/v1.0.24/results/INDEX_v24.md:17",
    ]
    require(msrm_docs == expected_docs, "E_MSMR6_DOCUMENT_CENSUS", repr(msrm_docs))
    loaders = fresh_loader_census()
    require(loaders == sorted([
        ("Claude/docs/v1.0.24/test_gates_v1024.py", 73),
        ("Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py", 17),
        ("Claude/docs/v1.0.24/test_gates_v1024_reflect.py", 5),
        ("Claude/docs/v1.0.24/results/v1024_final_sample.py", 11),
        ("Claude/docs/v1.0.24/results/v1024_reflect_curves.py", 8),
    ]), "E_FRESH_LOADER_DATAFLOW", repr(loaders))
    require("tr.get('kernel') == 'regsol'" in callable_source(
        new_callables["GraphiteAnodeDischargeDQDV.equilibrium"]),
        "E_REGSOL_SELECTOR")
    require(len(assignment_value(assignments["GRAPHITE_STAGING_XRD_v1024"]).elts) == 5,
            "E_XRD5_CENSUS")
    require(len(assignment_value(assignments["GRAPHITE_STAGING_MSMR6_LIT"]).elts) == 6,
            "E_MSMR6_CENSUS")
    return [
        route("P065-S71-ROUTE-REGSOL-EQUILIBRIUM", "EXPLICIT_OPT_IN_ONLY",
              [f"{MAIN_V24}:119-145", f"{MAIN_V24}:597-602"],
              entry="tr.get('kernel') == 'regsol'", scope="Graphite.equilibrium only"),
        route("P065-S71-ROUTE-REGSOL-NAMED", "ABSENT_FROM_NAMED_PROFILES",
              [f"{MAIN_V24}:1009-1280"],
              detail="No frozen named graphite, LCO, or Si registry contains a kernel key."),
        route("P065-S71-ROUTE-REGSOL-OTHER-METHODS", "KERNEL_KEY_IGNORED_LOGISTIC",
              [f"{MAIN_V24}:679-726", f"{MAIN_V24}:813-834", f"{MAIN_V24}:884-910"],
              methods=["dqdv", "entropy_coefficient", "solve_U_oc"]),
        route("P065-S71-ROUTE-GRAPHITE-XRD5", "OPT_IN_LOGISTIC_FIVE_FEATURE",
              [f"{MAIN_V24}:1157-1183"], profile="GRAPHITE_STAGING_XRD_v1024",
              kernel_keys=0, omega_does_not_select_regsol=True),
        route("P065-S71-ROUTE-GRAPHITE-MSMR6",
              "DECLARED_OPT_IN_LOGISTIC_NO_PYTHON_ENDPOINT_ACTIVATION_REFERENCE",
              [f"{MAIN_V24}:1187-1205"], profile="GRAPHITE_STAGING_MSMR6_LIT",
              kernel_keys=0, python_endpoint_activation_references=msrm_python,
              documentation_references=msrm_docs),
        route("P065-S71-ROUTE-LCO-INTERACTION", "GROUND_NOT_FOUND_IN_NAMED_LCO_PROFILE",
              [f"{MAIN_V24}:1011-1032"], profile="LCO_MSMR_LIT", omega_keys=0),
        route("P065-S71-ROUTE-LCO-ELECTRONIC", "DECLARED_DEFAULT_OFF",
              [f"{MAIN_V24}:1061-1105"], declared_default="False",
              v1023_state="ARGUMENT_ABSENT_ELECTRONIC_TERM_UNCONDITIONAL"),
        route("P065-S71-ROUTE-BLEND-DEFAULT", "NAMED_DEFAULT_AND_EXPLICIT_OVERRIDE",
              [f"{MAIN_V24}:1356-1433"], si_case_default="'sic'",
              graphite_none_default="GRAPHITE_STAGING_LIT"),
        route("P065-S71-ROUTE-BLEND-CURRENT", "SAME_FULL_CURRENT_AND_CAPACITY_TO_BOTH_HOSTS",
              [f"{MAIN_V24}:1480-1501"], current_partition="ABSENT_IN_FROZEN_SOURCE"),
        route("P065-S71-ROUTE-EXPLICIT-PROFILE", "STATIC_ENTRYPOINT_PRESENT_RUNTIME_PENDING",
              [f"{MAIN_V24}:368-401", f"{MAIN_V24}:1356-1381"]),
        route("P065-S71-ROUTE-FRESH-IMPORT", "STATIC_TEST_LOADERS_PRESENT_RUNTIME_PENDING", [
            "Claude/docs/v1.0.24/test_gates_v1024.py:70-74",
            "Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py:14-17",
            "Claude/docs/v1.0.24/test_gates_v1024_reflect.py:4-5",
            "Claude/docs/v1.0.24/results/v1024_final_sample.py:9-11",
            "Claude/docs/v1.0.24/results/v1024_reflect_curves.py:7-8",
        ]),
        route("P065-S71-ROUTE-LEGACY-RESTORE", "ABSENT_IN_FROZEN_SOURCE", EXPECTED_PATHS_LIST()),
        route("P065-S71-ROUTE-CURRENT-SAVED-STATE", "ABSENT_IN_FROZEN_SOURCE", EXPECTED_PATHS_LIST()),
    ]


def EXPECTED_PATHS_LIST() -> list[str]:
    return list(EXPECTED_PATHS)


def explicit_root_validation_uses(
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
    for current in ast.walk(node):
        if (isinstance(current, ast.Name) and isinstance(current.ctx, ast.Load)
                and current.id == "max_iter"):
            int_call = parents.get(id(current))
            range_call = parents.get(id(int_call)) if int_call is not None else None
            loop = parents.get(id(range_call)) if range_call is not None else None
            if (isinstance(int_call, ast.Call) and len(int_call.args) == 1
                    and int_call.args[0] is current and not int_call.keywords
                    and isinstance(int_call.func, ast.Name) and int_call.func.id == "int"
                    and isinstance(range_call, ast.Call) and len(range_call.args) == 1
                    and range_call.args[0] is int_call and not range_call.keywords
                    and isinstance(range_call.func, ast.Name) and range_call.func.id == "range"
                    and isinstance(loop, ast.For) and loop.iter is range_call
                    and isinstance(loop.target, ast.Name) and loop.target.id == "_"):
                operational_max_iter.append(current)
        if (isinstance(current, ast.Name) and isinstance(current.ctx, ast.Load)
                and current.id == "tol"):
            comparison = parents.get(id(current))
            conditional = parents.get(id(comparison)) if comparison is not None else None
            if (isinstance(comparison, ast.Compare) and len(comparison.ops) == 1
                    and isinstance(comparison.ops[0], ast.Lt)
                    and len(comparison.comparators) == 1
                    and comparison.comparators[0] is current
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
                operational_tol.append(current)
    allowed_watched_load_ids = (
        {id(operational_max_iter[0])} if len(operational_max_iter) == 1 else set())
    if len(operational_tol) == 1:
        allowed_watched_load_ids.add(id(operational_tol[0]))
    for current in ast.walk(node):
        if (isinstance(current, ast.Name) and isinstance(current.ctx, ast.Load)
                and current.id in watched and id(current) not in allowed_watched_load_ids):
            findings.add(f"unexpected-load:{current.id}:{current.lineno}")

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
        for current in ast.walk(value):
            if isinstance(current, ast.Import):
                for alias in current.names:
                    if alias.name in {"sys", "inspect", "builtins", "importlib"}:
                        return True
                    if alias.name == "importlib.util" and alias.asname is not None:
                        return True
            if isinstance(current, ast.ImportFrom):
                module = (current.module or "").split(".")[0]
                imported = {alias.name for alias in current.names}
                if (module == "builtins"
                        or module == "importlib" and "import_module" in imported
                        or module == "sys" and imported & {"_getframe", "modules"}
                        or module == "inspect" and "currentframe" in imported):
                    return True
            if (isinstance(current, ast.Name) and isinstance(current.ctx, ast.Load)
                    and current.id in namespace_names):
                return True
            if isinstance(current, ast.Attribute):
                if current.attr in danger_attributes:
                    return True
            if (isinstance(current, ast.Attribute)
                    and current.attr in {"globals", "locals", "vars"}
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(current.value))):
                return True
            if (isinstance(current, ast.Subscript)
                    and isinstance(current.slice, ast.Constant)
                    and current.slice.value in {"globals", "locals", "vars"}
                    and any(isinstance(root, ast.Name)
                            and root.id in {"builtins", "__builtins__"}
                            for root in ast.walk(current.value))):
                return True
            if (isinstance(current, ast.Call) and isinstance(current.func, ast.Name)
                    and current.func.id == "getattr" and len(current.args) >= 2
                    and (static_literal_string(current.args[1]) in danger_attributes
                         or any(isinstance(root, ast.Name)
                                and root.id in {
                                    "sys", "importlib", "inspect", "builtins", "__builtins__",
                                } for root in ast.walk(current.args[0])))):
                return True
            if (isinstance(current, ast.Subscript)
                    and static_literal_string(current.slice) in danger_attributes):
                return True
        return False

    def bound_names(target: ast.AST) -> set[str]:
        return {current.id for current in ast.walk(target)
                if isinstance(current, ast.Name) and isinstance(current.ctx, ast.Store)}

    namespace_marker_present = namespace_reference(node, set())
    if namespace_marker_present:
        findings.add("dynamic-function:tol")
        findings.add("dynamic-function:max_iter")
    namespace_aliases: set[str] = set()
    changed = True
    while changed:
        changed = False
        for current in ast.walk(node):
            value: ast.AST | None = None
            targets: list[ast.AST] = []
            if isinstance(current, ast.Assign):
                value = current.value
                targets = list(current.targets)
            elif isinstance(current, ast.AnnAssign) and current.value is not None:
                value = current.value
                targets = [current.target]
            elif isinstance(current, ast.NamedExpr):
                value = current.value
                targets = [current.target]
            if value is not None and namespace_reference(value, namespace_aliases):
                additions = set().union(*(bound_names(target) for target in targets))
                if not additions.issubset(namespace_aliases):
                    namespace_aliases.update(additions)
                    changed = True

    def dynamic_watched_lookup(value: ast.AST) -> bool:
        descendants = list(ast.walk(value))
        namespace_present = namespace_reference(value, namespace_aliases)
        watched_key_present = False
        for current in descendants:
            text = static_literal_string(current)
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

    def watched_load(value: ast.AST) -> bool:
        return (any(isinstance(current, ast.Name)
                    and isinstance(current.ctx, ast.Load)
                    and current.id in watched for current in ast.walk(value))
                or dynamic_watched_lookup(value))

    def watched_pattern_binding(pattern: ast.pattern) -> set[str]:
        names: set[str] = set()
        for current in ast.walk(pattern):
            if isinstance(current, (ast.MatchAs, ast.MatchStar)) and current.name in watched:
                names.add(current.name)
            elif isinstance(current, ast.MatchMapping) and current.rest in watched:
                names.add(current.rest)
        return names

    def record_dynamic_control(value: ast.AST, label: str) -> None:
        if namespace_reference(value, namespace_aliases):
            findings.add(f"dynamic-control:{label}:tol")
            findings.add(f"dynamic-control:{label}:max_iter")

    for current in ast.walk(node):
        if isinstance(current, ast.Call):
            values = [*current.args, *(keyword.value for keyword in current.keywords)]
            if any(watched_load(value) for value in values):
                rendered = ast.unparse(current)
                if rendered not in allowed_calls:
                    findings.add(f"call:{rendered}")
        if isinstance(current, ast.Compare) and watched_load(current):
            rendered = ast.unparse(current)
            if rendered != allowed_test:
                findings.add(f"compare:{rendered}")
        if isinstance(current, ast.Compare):
            record_dynamic_control(current, "compare")
        if isinstance(current, (ast.If, ast.While, ast.IfExp, ast.Assert)):
            test = current.test
            record_dynamic_control(test, "conditional")
            if watched_load(test) and ast.unparse(test) != allowed_test:
                findings.add(f"conditional:{ast.unparse(test)}")
        if isinstance(current, ast.Match):
            record_dynamic_control(current.subject, "match-subject")
            if watched_load(current.subject):
                findings.add(f"match-subject:{ast.unparse(current.subject)}")
            for case in current.cases:
                bindings = watched_pattern_binding(case.pattern)
                if bindings:
                    findings.add(f"match-pattern:{','.join(sorted(bindings))}")
                if case.guard is not None and watched_load(case.guard):
                    findings.add(f"match-guard:{ast.unparse(case.guard)}")
                if case.guard is not None:
                    record_dynamic_control(case.guard, "match-guard")
        if isinstance(current, (ast.For, ast.AsyncFor)):
            record_dynamic_control(current.iter, "loop-control")
            if watched_load(current.iter):
                rendered = ast.unparse(current.iter)
                if rendered != "range(int(max_iter))":
                    findings.add(f"loop-control:{rendered}")
        if isinstance(current, ast.comprehension):
            record_dynamic_control(current.iter, "comprehension-iter")
            if watched_load(current.iter):
                findings.add(f"comprehension-iter:{ast.unparse(current.iter)}")
            for condition in current.ifs:
                record_dynamic_control(condition, "comprehension-if")
                if watched_load(condition):
                    findings.add(f"comprehension-if:{ast.unparse(condition)}")
        if isinstance(current, (ast.With, ast.AsyncWith)):
            for item in current.items:
                record_dynamic_control(item.context_expr, "with-control")
                if watched_load(item.context_expr):
                    findings.add(f"with-control:{ast.unparse(item.context_expr)}")
    return sorted(findings)


def midpoint_after_iteration_loop(
        node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for outer in ast.walk(node):
        if not isinstance(outer, ast.For):
            continue
        for position, statement in enumerate(outer.body):
            if (not isinstance(statement, ast.For)
                    or ast.unparse(statement.iter) != "range(int(max_iter))"):
                continue
            for later in outer.body[position + 1:]:
                if not isinstance(later, (ast.Assign, ast.AnnAssign)):
                    continue
                targets = later.targets if isinstance(later, ast.Assign) else [later.target]
                value = later.value
                if (value is not None
                        and any(ast.unparse(target) == "out[k]" for target in targets)
                        and ast.unparse(value) == "0.5 * (lo + hi)"):
                    return True
    return False


def defect_boundaries(v23_tree: ast.Module, v24_tree: ast.Module) -> list[dict[str, Any]]:
    old = callable_index(v23_tree)
    new = callable_index(v24_tree)
    for index in (old, new):
        func_l_q = index["func_L_q"]
        require(not any(isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
                        and isinstance(node.right, ast.Constant) and node.right.value == 3600
                        for node in ast.walk(func_l_q)), "E_SECONDS_DIVISOR")
        blend_dqdv = callable_source(index["BlendedAnodeDQDV.dqdv"])
        require(all(needle in blend_dqdv for needle in (
            "self.gr_host.dqdv(V_app, T, I_abs, Q_cell, s=s)",
            "self.si_host.dqdv(V_app, T, I_abs, Q_cell, s=s)")),
            "E_BLEND_CURRENT_ROUTE")
        for symbol in ("BlendedAnodeDQDV.dqdv", "BlendedAnodeDQDV.curve"):
            require(not any(isinstance(node, ast.Attribute)
                            and isinstance(node.value, ast.Name)
                            and node.value.id == "self" and node.attr == "Q"
                            and isinstance(node.ctx, ast.Load)
                            for node in ast.walk(index[symbol])),
                    "E_EXTERNAL_INTERNAL_CAPACITY_BINDING", symbol)
        root = index["GraphiteAnodeDischargeDQDV.solve_U_oc"]
        root_source = callable_source(root)
        require(all(needle in root_source for needle in (
            "range(int(max_iter))", "if hi - lo < tol", "out[k] = 0.5 * (lo + hi)")),
            "E_ROOT_CONVERGENCE_BOUNDARY")
        guard_uses = explicit_root_validation_uses(root)
        require(not guard_uses, "E_ROOT_GUARD_BOUNDARY", repr(guard_uses))
        require(midpoint_after_iteration_loop(root), "E_ROOT_MIDPOINT_STRUCTURE")
    new_sources = {name: callable_source(node) for name, node in new.items()}
    require(all(needle in new_sources["GraphiteAnodeDischargeDQDV.equilibrium"]
                for needle in ("tr.get('kernel') == 'regsol'", "tr.get('delta', w)")),
            "E_FALLBACK_KERNEL_DELTA")
    require("max(float(delta), 1e-09)" in new_sources["_regsol_dqdv"],
            "E_FALLBACK_DELTA_CLAMP")
    require("return 1.0" in new_sources["GraphiteAnodeDischargeDQDV._n_factor"]
            and "if tr.get('n') is None:\n        return 0.0" in
            new_sources["GraphiteAnodeDischargeDQDV._dwdT"],
            "E_FALLBACK_WIDTH_DERIVATIVE")
    return [
        {
            "boundary_id": "SECONDS_HOUR", "static_change": "COMMENT_ONLY_EXECUTABLE_AST_IDENTICAL",
            "v1023_anchors": [f"{MAIN_V23}:105-112", f"{MAIN_V23}:675-705"],
            "v1024_anchors": [f"{MAIN_V24}:148-164", f"{MAIN_V24}:733-763"],
            "finding": "No executable /3600 conversion or explicit unit profile was added.",
            "validated_static_predicates": [
                "func_L_q callable AST is inherited", "no AST division by numeric 3600"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "CURRENT_PARTITION", "static_change": "INHERITED_UNCHANGED_ABSENT_PARTITION",
            "v1023_anchors": [f"{MAIN_V23}:1331-1352"], "v1024_anchors": [f"{MAIN_V24}:1480-1501"],
            "finding": "The inherited blend route sends the same full current and external Q_cell to both hosts.",
            "validated_static_predicates": [
                "both host dqdv calls receive I_abs and Q_cell unchanged"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "CAPACITY_BASIS", "static_change": "INHERITED_UNCHANGED_INTERNAL_Q_EXTERNAL_Q_CELL_UNBOUND",
            "v1023_anchors": [f"{MAIN_V23}:1252-1270", f"{MAIN_V23}:1331-1352"],
            "v1024_anchors": [f"{MAIN_V24}:1401-1419", f"{MAIN_V24}:1480-1501"],
            "finding": "The inherited self.Q calculation has no static validation binding external Q_cell to it.",
            "validated_static_predicates": [
                "self.Q is assigned in blend initialization",
                "blend dqdv and curve contain no load of self.Q"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "ROOT_VALIDATION", "static_change": "INHERITED_WITH_SILENT_EXHAUSTION",
            "v1023_anchors": [f"{MAIN_V23}:796-874"], "v1024_anchors": [f"{MAIN_V24}:854-932"],
            "finding": "Per-transition Q/n contracts remain incomplete; tol/max_iter have no explicit validation use outside their loop/convergence operations, and exhaustion returns the post-loop midpoint.",
            "validated_static_predicates": [
                "tol appears in no conditional/assertion/helper-call validation beyond hi-lo < tol",
                "max_iter appears in no conditional/assertion/helper-call validation beyond range(int(max_iter))",
                "out[k] midpoint assignment is structurally after the max_iter loop"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
        {
            "boundary_id": "FALLBACK_ROUTES", "static_change": "MIXED_ADDED_AND_INHERITED_SILENT_FALLBACKS",
            "v1023_anchors": [f"{MAIN_V23}:363-400", f"{MAIN_V23}:463-508"],
            "v1024_anchors": [f"{MAIN_V24}:421-458", f"{MAIN_V24}:521-566", f"{MAIN_V24}:597-602"],
            "finding": "Absent, None, zero, typo, and default routes are not uniformly distinguished.",
            "validated_static_predicates": [
                "kernel get selects regsol only by exact equality",
                "missing delta falls back to width",
                "nonpositive delta clamps to 1e-9",
                "missing n returns 1.0 while dwdT returns 0.0"],
            "runtime_conclusion": "WITHHELD_TO_STEP_73",
        },
    ]


def finding(finding_id: str, severity: str, title: str, anchors: list[str],
            next_steps: list[int], route_from_step70: list[str] | None = None) -> dict[str, Any]:
    return {
        "finding_id": finding_id,
        "severity": severity,
        "title": title,
        "source_anchors": anchors,
        "next_steps": next_steps,
        "step70_routes": route_from_step70 or [],
        "runtime_conclusion": "WITHHELD_TO_STEP_73" if 73 in next_steps else "NOT_A_RUNTIME_CLAIM",
        "authority_promoted": False,
    }


def findings() -> list[dict[str, Any]]:
    return [
        finding("P065-S71-F01", "P1", "Regular-solution activation is limited to equilibrium and absent from named profiles",
                [f"{MAIN_V24}:597-602", f"{MAIN_V24}:679-726", f"{MAIN_V24}:813-834", f"{MAIN_V24}:884-910"], [72, 73, 74], ["P065-S70-F08", "P065-S70-F25"]),
        finding("P065-S71-F02", "P1", "Blend current partition and capacity closure are absent",
                [f"{MAIN_V24}:1401-1419", f"{MAIN_V24}:1480-1501"], [72, 73], ["P065-S70-F35", "P065-S70-F36"]),
        finding("P065-S71-F03", "P1", "Root validation is incomplete and iteration exhaustion is silent",
                [f"{MAIN_V24}:854-932"], [72, 73]),
        finding("P065-S71-F04", "P1", "Seconds/hour correction is commentary, not executable migration",
                [f"{MAIN_V24}:148-164", f"{MAIN_V24}:733-763"], [72, 73, 75], ["P065-S70-F22"]),
        finding("P065-S71-F05", "P1", "Width fallback and temperature derivative use inconsistent absent/None semantics",
                [f"{MAIN_V24}:421-458"], [72, 73]),
        finding("P065-S71-F06", "P1", "LCO electronic entropy default changed and remains a fixed-center term",
                [f"{MAIN_V24}:1061-1105"], [72, 73, 74], ["P065-S70-F34"]),
        finding("P065-S71-F07", "P1", "No saved-state restoration or migration contract exists",
                list(EXPECTED_PATHS), [72, 73]),
        finding("P065-S71-F08", "P2", "Graphite five-feature Omega fields do not select regular-solution routing",
                [f"{MAIN_V24}:1157-1183", f"{MAIN_V24}:597-602"], [72, 73]),
        finding("P065-S71-F09", "P2", "Six-gallery profile has documentation references but no Python endpoint activation reference",
                [f"{MAIN_V24}:1187-1205"], [72, 73, 75], ["P065-S70-F23"]),
        finding("P065-S71-F10", "P2", "Kernel typo, None, or false silently selects logistic; nonpositive delta is clamped",
                [f"{MAIN_V24}:132-145", f"{MAIN_V24}:597-602"], [72, 73]),
        finding("P065-S71-F11", "P2", "Explicit zero current overrides c-rate while numeric direction zero maps positive",
                [f"{MAIN_V24}:733-763", f"{MAIN_V24}:982-1001"], [72, 73]),
        finding("P065-S71-F12", "P2", "Process fit outputs cannot promote static defaults or held-out authority",
                ["Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json"], [72, 75],
                ["P065-S70-F19", "P065-S70-F33", "P065-S70-F37", "P065-S70-F38", "P065-S70-F39", "P065-S70-F40"]),
        finding("P065-S71-F13", "P2", "Ref. 7 authority remains outside the frozen source and requires Step 72 binding",
                ["Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json"], [72], ["P065-S70-F09", "P065-S70-F24"]),
    ]


def build_artifacts() -> tuple[dict[str, Any], dict[str, Any]]:
    endpoints = [endpoint(path) for path in EXPECTED_PATHS]
    _, v23_tree = source_tree(MAIN_V23)
    _, v24_tree = source_tree(MAIN_V24)
    assignments = assignment_index(v24_tree)
    missing = [name for name in PROFILE_NAMES if name not in assignments]
    require(not missing, "E_PROFILE_SYMBOL", repr(missing))
    profiles = [profile_surface(name, assignments[name]) for name in PROFILE_NAMES]
    init = initialization_rows(v24_tree)
    routes = feature_routes(v23_tree, v24_tree)
    found = findings()
    mirror_rows = []
    for left, right in zip(V24_PATHS, V241_PATHS):
        mirror_rows.append({
            "v1024_path": left,
            "v1024_1_path": right,
            "blob": git_blob(left),
            "blob_identical": git_blob(left) == git_blob(right),
            "independent_corroboration": False,
        })
    matrix: dict[str, Any] = {
        "artifact_kind": "STATIC_CODE_PROFILE_DEFAULT_MATRIX",
        "authority": dict(AUTHORITY),
        "baseline_commit": BASELINE,
        "defect_boundaries": defect_boundaries(v23_tree, v24_tree),
        "endpoint_summary": {
            "occurrences": len(endpoints), "v1023": len(V23_PATHS),
            "v1024": len(V24_PATHS), "v1024_1": len(V241_PATHS),
            "unique_blobs": len({row["blob"] for row in endpoints}),
            "mirror_pairs": len(V24_PATHS), "parse_failures": 0,
        },
        "endpoints": endpoints,
        "expected_parent": EXPECTED_PARENT,
        "feature_routes": routes,
        "findings": found,
        "gate": GATE,
        "generated_date": "2026-08-30",
        "grammar": {
            "parser": "ast.parse", "feature_version": [3, 12],
            "checkout_imported": False, "source_execution": False,
            "input_transport": "git cat-file blob at frozen baseline",
        },
        "initialization_rows": init,
        "lineage_pairs": lineage_pairs(v23_tree, v24_tree),
        "mirror": {
            "pairs": len(mirror_rows), "rows": mirror_rows,
            "all_blob_identical": all(row["blob_identical"] for row in mirror_rows),
            "independent_corroboration": False,
        },
        "profile_surfaces": profiles,
        "route_outcomes": {
            "fresh_import": "STATIC_TEST_LOADERS_PRESENT_RUNTIME_PENDING",
            "explicit_profile": "STATIC_ENTRYPOINT_PRESENT_RUNTIME_PENDING",
            "legacy_restoration": "ABSENT_IN_FROZEN_SOURCE",
            "current_saved_state": "ABSENT_IN_FROZEN_SOURCE",
        },
        "schema_version": "P065-S71-CODE-PROFILE-1",
        "semantic_sha256": "",
        "source_policy": {
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
        },
        "step": 71,
    }
    matrix["semantic_sha256"] = semantic_hash(matrix)
    result_raw = lf_bytes((ROOT / RESULT_PATH).read_bytes())
    summary = {severity: sum(row["severity"] == severity for row in found)
               for severity in ("P0", "P1", "P2")}
    attestation: dict[str, Any] = {
        "artifact_kind": "STATIC_ROUTE_ATTESTATION",
        "authority": dict(AUTHORITY),
        "baseline_commit": BASELINE,
        "coverage": {
            "endpoint_occurrences": len(endpoints),
            "mirror_pairs": len(mirror_rows),
            "static_parse_pass": len(endpoints),
            "initialization_rows": len(init),
            "profile_surfaces": len(profiles),
            "feature_routes": len(routes),
            "lineage_symbols": len(matrix["lineage_pairs"]),
            "unread_intervals": [],
            "output_truncation_unresolved": [],
        },
        "expected_parent": EXPECTED_PARENT,
        "finding_summary": summary,
        "gate": GATE,
        "generated_date": "2026-08-30",
        "matrix_semantic_sha256": matrix["semantic_sha256"],
        "matrix_sha256_lf": sha256_bytes(canonical_bytes(matrix)),
        "result_path": RESULT_PATH,
        "result_sha256_lf": sha256_bytes(result_raw),
        "route_outcomes": dict(matrix["route_outcomes"]),
        "schema_version": "P065-S71-STATIC-ATTESTATION-1",
        "semantic_sha256": "",
        "step": 71,
        "unresolved_runtime_routes": ["fresh_import", "explicit_profile", "legacy_restoration"],
    }
    attestation["semantic_sha256"] = semantic_hash(attestation)
    return matrix, attestation


def atomic_json_last_collect(output_dir: pathlib.Path) -> None:
    destination = output_dir.resolve()
    repository_results = (ROOT / "Codex/results").resolve()
    require(destination == repository_results, "E_REPOSITORY_WRITE_BOUNDARY", str(destination))
    result_status = str(run_git(
        "diff", "--cached", "--name-status", "--", RESULT_PATH)).strip()
    require(result_status == f"A\t{RESULT_PATH}", "E_RESULT_NOT_STAGED_FIRST", result_status)
    result_index = bytes(run_git("show", f":{RESULT_PATH}", binary=True))
    require(result_index == (ROOT / RESULT_PATH).read_bytes(), "E_RESULT_INDEX_WORKTREE")
    destination.mkdir(parents=True, exist_ok=True)
    matrix, attestation = build_artifacts()
    matrix_path = destination / MATRIX_NAME
    attestation_path = destination / ATTESTATION_NAME
    matrix_temp = destination / f".{MATRIX_NAME}.step71.tmp"
    attestation_temp = destination / f".{ATTESTATION_NAME}.step71.tmp"
    require(not matrix_temp.exists() and not attestation_temp.exists(), "E_ATOMIC_TEMP_EXISTS")
    matrix_temp.write_bytes(canonical_bytes(matrix))
    attestation_temp.write_bytes(canonical_bytes(attestation))
    os.replace(matrix_temp, matrix_path)
    os.replace(attestation_temp, attestation_path)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path,
                        default=ROOT / "Codex/results")
    args = parser.parse_args()
    try:
        atomic_json_last_collect(args.output_dir)
    except (BuildFailure, OSError, UnicodeDecodeError, SyntaxError, ValueError, TypeError) as exc:
        print(f"FAIL_P065_STEP71_BUILD {exc}")
        return 1
    print("PASS_P065_STEP71_BUILD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
