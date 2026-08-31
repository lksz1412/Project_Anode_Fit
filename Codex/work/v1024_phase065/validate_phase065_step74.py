#!/usr/bin/env python3
"""Validate Phase 065 Step 74 document/code/guide conformance evidence.

The validator never imports or executes the frozen v1.0.24 implementation.  It
reconstructs evidence from immutable Git blobs, validates the JSON recursively,
and enforces the exact-seven result-first commit boundary.
"""

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
import subprocess
import sys
import tempfile
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "5c5c555462f1dbf0603eedda6a1d5b62684cffdf"
EXPECTED_SUBJECT = "audit(phase065): adjudicate v1024 doc code guide"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS"
MATRIX = Path("Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json")
BUILDER = Path("Codex/work/v1024_phase065/build_phase065_step74.py")
VALIDATOR = Path("Codex/work/v1024_phase065/validate_phase065_step74.py")
RESULT = Path("Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md")
PARENT_LEDGER = Path("Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md")
CANONICAL_LEDGER = Path("Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md")
HANDOVER = Path("Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md")
EXACT_PATHS = sorted(str(p).replace("\\", "/") for p in (
    BUILDER, VALIDATOR, MATRIX, RESULT, PARENT_LEDGER,
    CANONICAL_LEDGER, HANDOVER,
))
EXPECTED_ROW_IDS = [f"D74-{n:03d}" for n in range(1, 42)]
EXPECTED_ROUTE_IDS = [
    *[f"P065-S70-F{n:02d}" for n in (6, 8, 10, 11, 14, 34, 35, 36, 39, 41, 42, 43, 44)],
    "P065-S71-F01", "P065-S71-F06", "P065-S72-F02", "P065-S72-F05",
]
F41_PATHS = [
    "bdd_vs_savgol.png", "cathode_fit.png", "consistency.png",
    "gr_4vs6_transitions.png", "gr_angular_diag.png", "gr_sym_vs_asym.png",
    "model_vs_data.png", "new_materials.png", "param_distributions.png",
    "quality_vs_r2.png", "rate_broadening.png", "rate_quant.png",
    "regsol_proto.png", "temperature_entropy.png", "wavelet_denoise_check.png",
]
RUNTIME_POINTERS = {
    "explicit_profile.scope_boundaries": ("explicit", "scope_boundaries"),
    "explicit_profile.lco_electronic_entropy": ("explicit", "lco_electronic_entropy"),
    "explicit_profile.root_behavior": ("explicit", "root_validation"),
    "explicit_profile.seconds_hour": ("explicit", "seconds_hour"),
    "explicit_profile.width_derivative": ("explicit", "width_fallback"),
    "explicit_profile.blend_host_arguments": ("explicit", "blend_current_capacity"),
    "explicit_profile.profile_surfaces": ("explicit", "profiles"),
    "explicit_profile.regsol": ("explicit", "kernel"),
    "explicit_profile.xrd_omega": ("explicit", "kernel"),
    "explicit_profile.msmr6": ("explicit", "profiles"),
    "explicit_profile.kernel_fallback": ("explicit", "kernel"),
    "explicit_profile.delta_fallback": ("explicit", "kernel"),
    "explicit_profile.zero_current_direction": ("explicit", "seconds_hour"),
    "explicit_profile.transition_alias": ("explicit", "mutable_profile_alias"),
    "legacy_restoration": ("legacy", "runtime_observation_is_not_exhaustive_static_proof"),
}
EXPECTED_FUNCTION_AST = {
    "builder.run_process": "e73f73cec441415d82c82ec509a127a286985697d698433f85bb9145798cb2a0",
    "builder.git": "9ccdf9b89bf44a41a95248aeda573790f2a8ade7d148c8b0df99f89d74a2b1f5",
    "builder.guard_output": "854fb668ba2c2b51546b9c6069570bdecf43c01ded258ef82f4657735da332c8",
    "builder.atomic_write": "0efe91e642697a64810586cb0c3802af7c46a3ad6391e5a5772a7b2eb828931f",
    "builder.is_link_like": "fd0b13b9ef5b86b20d4684f02df51c7fb7b1333fa2c34077c986e11e7457c602",
    "validator.run_process": "3da80ea535e009ffea0da4ba41c70a711698400a678a8940597c7222715ff20e",
    "validator.git": "e085d04aab94a5c0689c63be893bead6accfa4cca796fc84e8cc9f6e6f4c4f3d",
}
EXPECTED_BUILDER_MODULE_AST = "8efceadc3698fefa0a83565661c18f471e18a223262c3f18bc57e61550381d7b"
EXPECTED_IMPORTS = {
    "builder": {
        ("from", "__future__", "annotations", ""),
        ("import", "", "argparse", ""), ("import", "", "copy", ""),
        ("import", "", "hashlib", ""), ("import", "", "json", ""),
        ("import", "", "os", ""), ("from", "pathlib", "Path", ""),
        ("import", "", "subprocess", ""), ("import", "", "tempfile", ""),
        ("from", "typing", "Any", ""),
    },
    "validator": {
        ("from", "__future__", "annotations", ""),
        ("import", "", "argparse", ""), ("import", "", "ast", ""),
        ("import", "", "copy", ""), ("import", "", "hashlib", ""),
        ("import", "", "json", ""), ("import", "", "math", ""),
        ("import", "", "os", ""), ("from", "pathlib", "Path", ""),
        ("import", "", "re", ""), ("import", "", "subprocess", ""),
        ("import", "", "sys", ""), ("import", "", "tempfile", ""),
        ("from", "typing", "Any", ""),
    },
}
EXPECTED_FUNCTION_NAMES = {
    "builder": {
        "run_process", "git", "blob", "sha256", "canonical", "binding",
        "control_binding", "anchor", "authority", "runtime", "row", "rows",
        "is_link_like", "guard_output", "atomic_write", "build", "main",
    },
    "validator": {
        "require", "run_process", "git", "sha256", "canonical", "reject_constant",
        "reject_duplicate", "strict_load", "traverse", "dotted",
        "function_owner", "canonical_ast", "function_ast_hashes", "normalized_module_hash",
        "extract_string_constant",
        "is_literal", "git_call_errors", "mutate_function_source",
        "source_policy_errors", "validate_source_policy", "blob",
        "verify_binding", "validate_matrix_pin", "validate_matrix", "verify_controls", "verify_docs",
        "validate_precommit_porcelain", "verify_exact_stage", "live_tip",
        "verify_refs", "validate_fixture_path", "validate_determinism_fixtures",
        "validate_output_sentinel", "transaction_negative_tests",
        "negative_tests", "main",
    },
}
TOP_KEYS = {
    "schema_version", "generated_date", "artifact_kind", "baseline_commit",
    "expected_parent", "expected_subject", "branch", "gate", "authority",
    "source_policy", "control_source_bindings", "source_bindings",
    "artifact_genealogy", "authority_precedence", "input_routes",
    "conformance_rows", "findings", "counts", "next_gate", "semantic_sha256",
}
ROW_KEYS = {
    "row_id", "claim_class", "claim", "claim_surface", "source_authority",
    "code_authority", "runtime_authority", "artifact_class", "verdict",
    "severity", "status", "owner", "acceptance_criterion", "target_phase",
    "origin_routes", "authority_ceiling",
}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(f"{code}: {detail}".rstrip())


def run_process(argv: list[str], *, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=text, encoding="utf-8" if text else None,
    )


def git(*args: str, text: bool = True) -> str | bytes:
    cp = run_process(["git", *args], text=text)
    require(cp.returncode == 0, "E_GIT", cp.stderr if text else "binary git failure")
    return cp.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def reject_constant(value: str) -> None:
    raise ValidationError(f"E_JSON_NONFINITE: {value}")


def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, "E_JSON_DUPLICATE", key)
        out[key] = value
    return out


def strict_load(raw: bytes) -> dict[str, Any]:
    try:
        obj = json.loads(
            raw.decode("utf-8"), object_pairs_hook=reject_duplicate,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"E_JSON_PARSE: {exc}") from exc
    require(isinstance(obj, dict), "E_JSON_ROOT")
    return obj


def traverse(value: Any, depth: int = 0) -> tuple[int, int]:
    require(depth < 64, "E_JSON_DEPTH")
    if isinstance(value, dict):
        total = 1; deepest = depth
        for key, child in value.items():
            require(isinstance(key, str), "E_JSON_KEY")
            count, child_depth = traverse(child, depth + 1)
            total += count; deepest = max(deepest, child_depth)
        return total, deepest
    if isinstance(value, list):
        total = 1; deepest = depth
        for child in value:
            count, child_depth = traverse(child, depth + 1)
            total += count; deepest = max(deepest, child_depth)
        return total, deepest
    if isinstance(value, float):
        require(math.isfinite(value), "E_JSON_NONFINITE")
    require(value is None or isinstance(value, (str, int, float, bool)), "E_JSON_TYPE")
    return 1, depth


def dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted(node.value)
        return f"{parent}.{node.attr}" if parent else None
    return None


def function_owner(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> str:
    cursor = parents.get(node)
    while cursor is not None:
        if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return cursor.name
        cursor = parents.get(cursor)
    return "<module>"


def canonical_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return [
            type(value).__name__,
            [[field, canonical_ast(child)] for field, child in ast.iter_fields(value)],
        ]
    if isinstance(value, list):
        return [canonical_ast(item) for item in value]
    if isinstance(value, bytes):
        return ["bytes", value.hex()]
    if isinstance(value, complex):
        return ["complex", repr(value)]
    if value is Ellipsis:
        return ["ellipsis"]
    return value


def function_ast_hashes(tree: ast.Module) -> dict[str, str]:
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            payload = json.dumps(canonical_ast(node), ensure_ascii=False, separators=(",", ":"))
            out[node.name] = sha256(payload.encode("utf-8"))
    return out


def normalized_module_hash(tree: ast.Module, role: str) -> str:
    clone = copy.deepcopy(tree)
    if role == "validator":
        for node in clone.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "EXPECTED_BUILDER_MODULE_AST"
                for target in node.targets
            ):
                node.value = ast.Constant(value="CROSS_SEAL_VALUE")
    payload = json.dumps(canonical_ast(clone), ensure_ascii=False, separators=(",", ":"))
    return sha256(payload.encode("utf-8"))


def extract_string_constant(tree: ast.Module, name: str) -> str:
    matches = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == name and isinstance(node.value, ast.Constant):
                matches.append(node.value.value)
    require(len(matches) == 1 and isinstance(matches[0], str) and re.fullmatch(r"[0-9a-f]{64}", matches[0]) is not None, "E_CROSS_SEAL_CONSTANT", name)
    return matches[0]


def is_literal(node: ast.AST, value: str) -> bool:
    return isinstance(node, ast.Constant) and node.value == value


def git_call_errors(node: ast.Call, owner: str, role: str) -> list[str]:
    errors: list[str] = []
    if not node.args or not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, str):
        return [f"E_GIT_COMMAND_DYNAMIC:{owner}"]
    command = node.args[0].value
    if any(isinstance(arg, ast.Starred) for arg in node.args) and not (
        role in {"builder", "validator"} and command == "diff"
        and owner in {"guard_output", "verify_exact_stage"}
    ):
        errors.append(f"E_GIT_STARRED:{command}:{owner}")
    if role == "probe" and any(not isinstance(arg, ast.Constant) for arg in node.args[1:]):
        errors.append(f"E_GIT_DYNAMIC_ARGUMENT:{command}:{owner}")
    for arg in node.args[1:]:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            if (
                "::" in arg.value or "://" in arg.value
                or arg.value in {"-D", "--delete", "--force", "-o", "--ext-diff", "--textconv"}
                or arg.value.startswith(("--output", "--exec-path", "--upload-pack", "--receive-pack"))
            ):
                errors.append(f"E_GIT_PROTOCOL_OR_MUTATOR:{command}:{arg.value}")
    allowed = False
    if command == "show":
        allowed = (
            len(node.args) == 2
            and not (isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str) and node.args[1].value.startswith("-"))
        ) or (
            len(node.args) == 4 and is_literal(node.args[1], "-s")
            and isinstance(node.args[2], ast.Constant)
            and node.args[2].value in {"--format=%P", "--format=%s"}
        )
    elif command == "rev-parse":
        allowed = len(node.args) == 2 or (
            len(node.args) == 3 and is_literal(node.args[1], "--abbrev-ref")
            and is_literal(node.args[2], "@{upstream}")
        )
    elif command == "diff":
        allowed = (
            len(node.args) == 3 and is_literal(node.args[1], "--cached") and is_literal(node.args[2], "--name-only")
            or len(node.args) >= 4 and is_literal(node.args[1], "--name-only") and is_literal(node.args[2], "--")
            or len(node.args) >= 5 and is_literal(node.args[1], "--cached") and is_literal(node.args[2], "--name-only") and is_literal(node.args[3], "--")
            or len(node.args) == 2 and is_literal(node.args[1], "--check")
            or len(node.args) == 3 and is_literal(node.args[1], "--cached") and is_literal(node.args[2], "--check")
            or len(node.args) == 4 and is_literal(node.args[1], "--check")
        )
    elif command == "diff-tree":
        allowed = len(node.args) == 5 and all((
            is_literal(node.args[1], "--no-commit-id"), is_literal(node.args[2], "--name-only"),
            is_literal(node.args[3], "-r"),
        ))
    elif command == "branch":
        allowed = len(node.args) == 2 and is_literal(node.args[1], "--show-current")
    elif command == "status":
        allowed = (
            len(node.args) == 2 and is_literal(node.args[1], "--porcelain")
            or len(node.args) == 4 and is_literal(node.args[1], "--porcelain=v1")
            and is_literal(node.args[2], "-z") and is_literal(node.args[3], "--untracked-files=all")
        )
    elif command == "ls-remote":
        allowed = len(node.args) == 4 and is_literal(node.args[1], "--heads") and is_literal(node.args[2], "origin")
    if not allowed:
        errors.append(f"E_GIT_GRAMMAR:{command}:{owner}")
    if any(keyword.arg not in {"text"} for keyword in node.keywords):
        errors.append(f"E_GIT_KEYWORD:{command}:{owner}")
    return errors


def mutate_function_source(source: str, name: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    require(len(matches) == 1, "E_SOURCE_MUTATION_TARGET", name)
    matches[0].body = [ast.Return(value=ast.Constant(value=0))]
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def source_policy_errors(source: str, role: str, independent_validator_seal: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"E_AST_PARSE:{exc}"]
    parents: dict[ast.AST, ast.AST] = {}
    import_records: set[tuple[str, str, str, str]] = set()
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                kind = "import" if isinstance(node, ast.Import) else "from"
                module = "" if isinstance(node, ast.Import) else (node.module or "")
                import_records.add((kind, module, alias.name, alias.asname or ""))
                if role == "probe":
                    errors.append(f"E_PROBE_IMPORT:{module or alias.name}")
                if alias.asname is not None:
                    errors.append(f"E_IMPORT_ALIAS:{alias.name}")
                if isinstance(node, ast.ImportFrom) and module in {"subprocess", "os", "tempfile", "shutil"}:
                    errors.append(f"E_IMPORT_FROM_SENSITIVE:{module}.{alias.name}")
        if isinstance(node, ast.Call):
            name = dotted(node.func); owner = function_owner(node, parents)
            if role == "probe":
                if isinstance(node.func, ast.Name):
                    errors.append(f"E_PROBE_NAME_CALL:{node.func.id}:{owner}")
                elif isinstance(node.func, ast.Attribute):
                    errors.append(f"E_PROBE_ATTRIBUTE_CALL:{node.func.attr}:{owner}")
                else:
                    errors.append(f"E_INDIRECT_CALL:{owner}")
            if name == "subprocess.run":
                if owner != "run_process":
                    errors.append(f"E_SUBPROCESS_OWNER:{owner}")
            elif name and name.startswith("subprocess."):
                errors.append(f"E_SUBPROCESS_API:{name}")
            if name in {
                "eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr",
                "globals", "locals", "vars", "os.system", "os.popen", "operator.attrgetter",
                "importlib.import_module",
            }:
                errors.append(f"E_DYNAMIC_EXEC:{name}")
            if name == "run_process" and owner != "git":
                errors.append(f"E_RUN_PROCESS_CALLER:{owner}")
            if name == "git":
                errors.extend(git_call_errors(node, owner, role))
            if name == "open":
                errors.append(f"E_BUILTIN_OPEN:{owner}")
            if name == "os.fdopen" and owner != "atomic_write":
                errors.append(f"E_FDOPEN:{owner}")
            if name in {"os.replace", "os.unlink", "tempfile.mkstemp"} and owner != "atomic_write":
                errors.append(f"E_FS_MUTATOR:{name}:{owner}")
            if name in {"os.remove", "os.rename", "os.rmdir", "shutil.rmtree", "shutil.move"}:
                errors.append(f"E_FS_FORBIDDEN:{name}")
            if isinstance(node.func, ast.Attribute) and node.func.attr in {
                "open", "write", "writelines", "truncate", "write_text", "write_bytes",
                "replace", "unlink", "rename", "mkdir", "rmdir", "touch", "symlink_to", "hardlink_to",
                "chmod", "lchmod", "chown", "lchown", "utime", "link", "symlink",
            }:
                safe_string_replace = (
                    node.func.attr == "replace" and (
                        isinstance(node.func.value, ast.Call) and dotted(node.func.value.func) == "str"
                        or owner == "transaction_negative_tests" and isinstance(node.func.value, ast.Name) and node.func.value.id == "base"
                        or owner == "validate_precommit_porcelain" and isinstance(node.func.value, ast.Subscript)
                    )
                )
                if not (
                    owner == "atomic_write" and (
                        name in {"os.fdopen", "os.replace", "os.unlink"} or node.func.attr == "write"
                    )
                    or safe_string_replace
                ):
                    errors.append(f"E_PATH_MUTATOR:{node.func.attr}:{owner}")
        if isinstance(node, ast.Attribute) and dotted(node) == "subprocess.run":
            parent = parents.get(node)
            if not (isinstance(parent, ast.Call) and parent.func is node):
                errors.append("E_SUBPROCESS_ESCAPE")
        if isinstance(node, ast.Attribute) and dotted(node) and dotted(node).startswith("subprocess."):
            if dotted(node) not in {"subprocess.run", "subprocess.PIPE", "subprocess.CompletedProcess"}:
                errors.append(f"E_SUBPROCESS_ATTRIBUTE:{dotted(node)}")
        if isinstance(node, ast.Attribute) and (
            dotted(node) == "sys.modules" or node.attr in {"__dict__", "__getattribute__", "__subclasses__"}
        ):
            errors.append(f"E_DYNAMIC_ATTRIBUTE:{dotted(node) or node.attr}")
        if isinstance(node, ast.Attribute) and dotted(node) in {
            "operator.attrgetter", "importlib.import_module", "os.system", "os.popen",
            "os.startfile", "os.spawnl", "os.spawnle", "os.spawnlp", "os.spawnlpe",
            "os.spawnv", "os.spawnve", "os.spawnvp", "os.spawnvpe", "os.execl",
            "os.execle", "os.execlp", "os.execlpe", "os.execv", "os.execve",
            "os.execvp", "os.execvpe",
        }:
            errors.append(f"E_DANGEROUS_ATTRIBUTE_REFERENCE:{dotted(node)}")
        if isinstance(node, ast.Attribute) and node.attr in {
            "eval", "__import__", "attrgetter", "methodcaller", "import_module",
            "create_subprocess_exec", "create_subprocess_shell", "posix_spawn", "posix_spawnp",
            "system", "popen", "startfile",
        }:
            errors.append(f"E_DANGEROUS_ATTRIBUTE_NAME:{node.attr}")
        if isinstance(node, ast.Attribute) and node.attr in {
            "open", "write", "writelines", "truncate", "write_text", "write_bytes",
            "replace", "remove", "unlink", "rename", "mkdir", "rmdir", "touch",
            "symlink_to", "hardlink_to", "move", "rmtree", "chmod", "lchmod",
            "chown", "lchown", "utime", "link", "symlink",
        }:
            parent = parents.get(node)
            if not (isinstance(parent, ast.Call) and parent.func is node):
                errors.append(f"E_FS_CALLABLE_ESCAPE:{dotted(node) or node.attr}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id == "subprocess":
            parent = parents.get(node)
            if not (
                isinstance(parent, ast.Attribute) and parent.value is node
                and dotted(parent) in {"subprocess.run", "subprocess.PIPE", "subprocess.CompletedProcess"}
            ):
                errors.append("E_SUBPROCESS_OBJECT_ESCAPE")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in {
            "eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr",
            "globals", "locals", "vars", "open", "__builtins__",
        }:
            errors.append(f"E_DANGEROUS_NAME_REFERENCE:{node.id}")
        if role == "probe" and isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in {
            "os", "sys", "subprocess", "tempfile", "shutil", "pathlib", "Path",
            "operator", "_operator", "importlib", "asyncio", "builtins", "multiprocessing",
        }:
            errors.append(f"E_PROBE_MODULE_REFERENCE:{node.id}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in {"run_process", "git", "open"}:
            parent = parents.get(node)
            if not (isinstance(parent, ast.Call) and parent.func is node):
                errors.append(f"E_CALLABLE_ESCAPE:{node.id}")

    subprocess_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and dotted(n.func) == "subprocess.run"]
    if role in {"builder", "validator"} and len(subprocess_calls) != 1:
        errors.append(f"E_SUBPROCESS_COUNT:{len(subprocess_calls)}")
    if role in {"builder", "validator"}:
        if import_records != EXPECTED_IMPORTS[role]:
            errors.append(f"E_IMPORT_SET:{role}")
        function_names = {
            node.name for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if function_names != EXPECTED_FUNCTION_NAMES[role]:
            errors.append(f"E_FUNCTION_SET:{role}")
        hashes = function_ast_hashes(tree)
        required = ("run_process", "git", "is_link_like", "guard_output", "atomic_write") if role == "builder" else ("run_process", "git")
        for name in required:
            if hashes.get(name) != EXPECTED_FUNCTION_AST[f"{role}.{name}"]:
                errors.append(f"E_FUNCTION_AST:{role}.{name}")
    if role == "builder":
        if normalized_module_hash(tree, role) != EXPECTED_BUILDER_MODULE_AST:
            errors.append("E_MODULE_AST:builder")
    if role == "validator":
        if independent_validator_seal is None:
            errors.append("E_VALIDATOR_SEAL_MISSING")
        elif normalized_module_hash(tree, role) != independent_validator_seal:
            errors.append("E_MODULE_AST:validator")
    return sorted(set(errors))


def validate_source_policy(rev: str, expected_builder_sha256: str, expected_validator_sha256: str) -> int:
    require(re.fullmatch(r"[0-9a-f]{64}", expected_builder_sha256) is not None, "E_EXPECTED_BUILDER_SHA")
    require(re.fullmatch(r"[0-9a-f]{64}", expected_validator_sha256) is not None, "E_EXPECTED_VALIDATOR_SHA")
    builder_raw = blob(rev, str(BUILDER).replace("\\", "/"))
    validator_raw = blob(rev, str(VALIDATOR).replace("\\", "/"))
    require(sha256(builder_raw) == expected_builder_sha256, "E_INDEPENDENT_BUILDER_PIN")
    require(sha256(validator_raw) == expected_validator_sha256, "E_INDEPENDENT_VALIDATOR_PIN")
    builder_source = builder_raw.decode("utf-8")
    validator_source = validator_raw.decode("utf-8")
    require(not source_policy_errors(builder_source, "builder"), "E_SOURCE_POLICY", "builder")
    independent_validator_seal = extract_string_constant(ast.parse(builder_source), "EXPECTED_VALIDATOR_MODULE_AST")
    require(not source_policy_errors(validator_source, "validator", independent_validator_seal), "E_SOURCE_POLICY", "validator")
    probes = {
        "direct-subprocess": "import subprocess\nsubprocess.run(['git','status'])\n",
        "subprocess-alias": "import subprocess\nf=subprocess.run\n",
        "subprocess-object-alias": "import subprocess\nsp=subprocess\nsp.run(['git'])\n",
        "subprocess-tuple-escape": "import subprocess\n(subprocess,)[0].run(['git'])\n",
        "subprocess-dict-escape": "import subprocess\nsubprocess.__dict__['run'](['git'])\n",
        "popen": "import subprocess\nsubprocess.Popen(['git'])\n",
        "dynamic-getattr": "import subprocess\ngetattr(subprocess,'run')(['git'])\n",
        "importfrom-subprocess-alias": "from subprocess import run as r\nr(['git','push'])\n",
        "importfrom-os-alias": "from os import remove as r\nr('x')\n",
        "git-push": "def git(*args): pass\ndef x(): git('push','origin','HEAD')\n",
        "git-branch-delete": "def git(*args): pass\ndef x(): git('branch','-D','victim')\n",
        "git-protocol": "def git(*args): pass\ndef x(): git('ls-remote','ext::payload')\n",
        "git-output-option": "def git(*args): pass\ndef x(): git('show','--output=Codex/escape')\n",
        "git-dynamic-show-arg": "def git(*args): pass\ndef x(arg): git('show',arg)\n",
        "git-starred-show-arg": "def git(*args): pass\ndef x(): git('show',*['--output=Codex/escape'])\n",
        "run-process-outside-git": "def run_process(x): pass\ndef x(): run_process(['python','evil.py'])\n",
        "os-remove": "import os\ndef x(): os.remove('x')\n",
        "path-write": "from pathlib import Path\ndef x(): Path('x').write_text('bad')\n",
        "path-replace": "from pathlib import Path\ndef x(): Path('x').replace('y')\n",
        "builtin-open-write": "def x(): open('x','w').write('bad')\n",
        "stream-write": "def x(handle): handle.write('bad')\n",
        "path-open": "from pathlib import Path\ndef x(): Path('x').open('w')\n",
        "fdopen-outside-collector": "import os\ndef x(fd): os.fdopen(fd,'wb')\n",
        "globals-subprocess": "def x(): globals()['subprocess'].run(['git'])\n",
        "vars-subprocess": "def x(): vars()['subprocess'].run(['git'])\n",
        "sys-modules-subprocess": "import sys\ndef x(): sys.modules['subprocess'].run(['git'])\n",
        "os-remove-callable-alias": "import os\ndef x():\n f=os.remove\n f('x')\n",
        "path-replace-callable-alias": "from pathlib import Path\ndef x():\n f=Path('x').replace\n f('y')\n",
        "path-replace-container": "from pathlib import Path\ndef x(): (Path('x').replace,)[0]('y')\n",
        "globals-callable-alias": "def x():\n f=globals\n ns=f()\n m=ns['subprocess']\n m.run(['git'])\n",
        "getattr-callable-alias": "def x(o):\n f=getattr\n w=f(o,'write')\n w('x')\n",
        "attrgetter-callable-alias": "import operator\ndef x(o):\n f=operator.attrgetter\n g=f('write')\n w=g(o)\n w('x')\n",
        "builtins-import-alias": "def x():\n i=__builtins__['__import__']\n m=i('subprocess')\n m.run(['git'])\n",
        "compile-exec-alias": "def x(s):\n c=compile\n e=exec\n code=c(s,'x','exec')\n e(code)\n",
        "os-system-alias": "import os\ndef x():\n f=os.system\n f('git push')\n",
        "os-popen-alias": "import os\ndef x():\n f=os.popen\n f('git push')\n",
        "builtins-eval": "import builtins\ndef x(s): builtins.eval(s)\n",
        "builtins-import": "import builtins\ndef x():\n i=builtins.__import__\n i('subprocess')\n",
        "operator-methodcaller": "import operator\ndef x(o): operator.methodcaller('write','bad')(o)\n",
        "private-operator-attrgetter": "import _operator\ndef x(o): _operator.attrgetter('write')(o)('bad')\n",
        "asyncio-subprocess": "import asyncio\ndef x(): asyncio.create_subprocess_exec('git','push')\n",
        "posix-spawn": "import os\ndef x(): os.posix_spawn('git',['git','push'],{})\n",
        "os-chmod": "import os\ndef x(): os.chmod('x',0o777)\n",
        "path-chmod": "from pathlib import Path\ndef x():\n p=Path('x')\n p.chmod(0o777)\n",
        "os-module-alias": "import os\ndef x():\n m=os\n m.system('git push')\n",
        "operator-module-alias": "import os,operator\ndef x():\n m=operator\n f=m.attrgetter\n f('system')(os)('git push')\n",
        "importlib-module-alias": "import importlib\ndef x():\n m=importlib\n f=m.import_module\n f('subprocess').run(['git'])\n",
        "parameter-subprocess-run": "def x(sp): sp.run(['git','push'])\n",
        "parameter-subprocess-popen": "def x(sp): sp.Popen(['git','push'])\n",
        "parameter-os-exec": "def x(m): m.execv('git',['git','push'])\n",
        "parameter-fs-remove": "def x(m): m.remove('x')\n",
        "parameter-fs-copy": "def x(m): m.copyfile('x','y')\n",
        "parameter-path-move": "def x(p): p.move_into('dir')\n",
    }
    for name, source in probes.items():
        require(bool(source_policy_errors(source, "probe")), "E_SOURCE_NEGATIVE", name)
    self_disabled = mutate_function_source(validator_source, "validate_source_policy")
    require(bool(source_policy_errors(self_disabled, "validator", independent_validator_seal)), "E_SOURCE_NEGATIVE", "validator-self-disable")
    mutated_validator_seal = normalized_module_hash(ast.parse(self_disabled), "validator")
    tampered_builder = re.sub(
        r'EXPECTED_VALIDATOR_MODULE_AST = "[0-9a-f]{64}"',
        f'EXPECTED_VALIDATOR_MODULE_AST = "{mutated_validator_seal}"',
        builder_source, count=1,
    )
    require(bool(source_policy_errors(tampered_builder, "builder")), "E_SOURCE_NEGATIVE", "coherent-cross-seal-update")
    require(
        sha256(tampered_builder.encode("utf-8")) != expected_builder_sha256
        and sha256(self_disabled.encode("utf-8")) != expected_validator_sha256,
        "E_SOURCE_NEGATIVE", "independent-raw-pin",
    )
    return len(probes) + 3


def blob(rev: str, path: str) -> bytes:
    spec = f":{path}" if rev == ":" else f"{rev}:{path}"
    return git("show", spec, text=False)  # type: ignore[return-value]


def verify_binding(row: dict[str, Any]) -> None:
    require(set(row) == {"path", "role", "revision", "git_blob", "sha256", "size_bytes", "lines", "read_status", "read_ranges"}, "E_BINDING_SCHEMA", str(row.get("path")))
    path = row["path"]; rev = row["revision"]
    raw = blob(rev, path)
    require(row["git_blob"] == str(git("rev-parse", f"{rev}:{path}")).strip(), "E_BINDING_BLOB", path)
    require(row["sha256"] == sha256(raw), "E_BINDING_HASH", path)
    require(row["size_bytes"] == len(raw), "E_BINDING_SIZE", path)
    lines = len(raw.decode("utf-8").splitlines())
    require(row["lines"] == lines, "E_BINDING_LINES", path)
    require(row["read_status"] in {"DIRECT_READ", "AGENT_FULL_READ", "MACHINE_FULL_TRAVERSAL"}, "E_BINDING_READ", path)
    require(row["read_ranges"] == ([[1, lines]] if lines else []), "E_BINDING_RANGE", path)


def validate_matrix_pin(raw: bytes, expected_sha256: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is not None, "E_EXPECTED_MATRIX_SHA")
    require(sha256(raw) == expected_sha256, "E_INDEPENDENT_MATRIX_PIN")


def validate_matrix(obj: dict[str, Any]) -> tuple[int, int]:
    require(set(obj) == TOP_KEYS, "E_TOP_SCHEMA", repr(sorted(set(obj) ^ TOP_KEYS)))
    require(obj["schema_version"] == "phase065-step74-v1", "E_SCHEMA_VERSION")
    require(obj["generated_date"] == "2026-08-31", "E_DATE")
    require(obj["artifact_kind"] == "document-code-guide-conformance-matrix", "E_KIND")
    require(obj["baseline_commit"] == BASELINE, "E_BASELINE")
    require(obj["expected_parent"] == EXPECTED_PARENT, "E_PARENT")
    require(obj["expected_subject"] == EXPECTED_SUBJECT, "E_SUBJECT")
    require(obj["branch"] == BRANCH, "E_BRANCH")
    require(obj["gate"] == GATE, "E_GATE")

    authority = obj["authority"]
    require(set(authority) == {
        "internal_conformance_audit", "external_scientific_truth",
        "external_material_truth", "external_experimental_truth",
        "external_proposition_support", "canonical_model_selected",
        "production_repair_complete", "publication_ready",
        "generated_artifact_independent_support", "ceiling",
    }, "E_AUTH_SCHEMA")
    require(authority["internal_conformance_audit"] is True, "E_AUTH_INTERNAL")
    for key in (
        "external_scientific_truth", "external_material_truth",
        "external_experimental_truth", "external_proposition_support",
        "canonical_model_selected", "production_repair_complete",
        "publication_ready", "generated_artifact_independent_support",
    ):
        require(authority[key] is False, "E_AUTH_OVERCLAIM", key)

    policy = obj["source_policy"]
    require(set(policy) == {
        "behavior_authority", "science_authority", "adoption_authority",
        "generated_artifact_rule", "external_scientific_evidence_network_used",
        "git_remote_reference_network_used", "frozen_source_execution",
        "claude_tree_written", "child_process_allowlist", "json_last",
    }, "E_POLICY_SCHEMA")
    require(policy["frozen_source_execution"] is False, "E_POLICY_EXEC")
    require(policy["claude_tree_written"] is False, "E_POLICY_CLAUDE")
    require(policy["external_scientific_evidence_network_used"] is False, "E_POLICY_SCIENCE_NETWORK")
    require(policy["git_remote_reference_network_used"] is True, "E_POLICY_GIT_REMOTE_NETWORK")
    require(policy["behavior_authority"] == "isolated Step 73 runtime plus frozen executable source", "E_POLICY_BEHAVIOR")
    require(policy["science_authority"] == "primary source text only; proposition support remains separately bounded", "E_POLICY_SCIENCE")
    require(policy["adoption_authority"] == "Git chronology and explicit disposition records", "E_POLICY_ADOPTION")
    require(policy["generated_artifact_rule"] == "HTML/PDF/image repetition does not multiply source support", "E_POLICY_GENERATED")
    require(policy["child_process_allowlist"] == ["git"], "E_POLICY_CHILD")
    require(policy["json_last"] is True, "E_POLICY_JSON_LAST")

    bindings = obj["source_bindings"]
    require(isinstance(bindings, list) and len(bindings) == 56, "E_BINDING_COUNT")
    paths = [row["path"] for row in bindings]
    require(len(paths) == len(set(paths)), "E_BINDING_DUP")
    for row in bindings:
        verify_binding(row)
    bound_paths = set(paths) | {x for x in EXACT_PATHS if x != str(MATRIX).replace("\\", "/")}

    expected_genealogy = [
        {"source":"Claude/docs/v1.0.24/CODE_GUIDE_v24.md","derived":"Claude/docs/v1.0.24/CODE_GUIDE_v24.html","relation":"GENERATED_FROM","generator_command":"GROUND_NOT_FOUND","independent_support":False},
        {"source":"Claude/docs/v1.0.24/ch1_graphite_v1.0.24.tex","derived":"Claude/docs/v1.0.24/ch1_graphite_v1.0.24.pdf","relation":"GENERATED_FROM_CLOSURE","generator_command":"GROUND_NOT_FOUND","independent_support":False},
        {"source":"Claude/docs/v1.0.24/ch2_lco_v1.0.24.tex","derived":"Claude/docs/v1.0.24/ch2_lco_v1.0.24.pdf","relation":"GENERATED_FROM_CLOSURE","generator_command":"GROUND_NOT_FOUND","independent_support":False},
        {"source":"Claude/docs/v1.0.24/ch3_si_v1.0.24.tex","derived":"Claude/docs/v1.0.24/ch3_si_v1.0.24.pdf","relation":"GENERATED_FROM_CLOSURE","generator_command":"GROUND_NOT_FOUND","independent_support":False},
        {"source":"Claude/docs/v1.0.24","derived":"Claude/docs/v1.0.24.1","relation":"130_BYTE_IDENTICAL_MIRROR_PAIRS_PLUS_ARCHIVE_NOTE","generator_command":"NOT_APPLICABLE","independent_support":False},
    ]
    require(obj["artifact_genealogy"] == expected_genealogy, "E_GENEALOGY")
    require(obj["authority_precedence"] == [
        {"claim_class":"behavior","authority":"isolated runtime, then frozen executable source","cannot_overrule":"scientific proposition or adoption"},
        {"claim_class":"science","authority":"primary full text and explicit derivation","cannot_overrule":"runtime behavior or Git adoption"},
        {"claim_class":"adoption","authority":"Git chronology and explicit disposition","cannot_overrule":"scientific truth or runtime behavior"},
        {"claim_class":"artifact","authority":"authoring source plus reproducible generator","cannot_overrule":"source content"},
    ], "E_AUTHORITY_PRECEDENCE")

    rows = obj["conformance_rows"]
    require(isinstance(rows, list) and len(rows) == len(EXPECTED_ROW_IDS), "E_ROW_COUNT")
    require([row.get("row_id") for row in rows] == EXPECTED_ROW_IDS, "E_ROW_IDS")
    allowed_verdicts = {
        "CONFORMS", "MISMATCH", "PARTIAL", "GROUND_NOT_FOUND",
        "DERIVED_ONLY", "CLOSED_NON_GRAFT", "ABSENT_NOT_A_PASS",
    }
    allowed_classes = {"behavior", "science", "adoption", "artifact", "units", "version", "scope", "record"}
    for row in rows:
        require(set(row) == ROW_KEYS, "E_ROW_SCHEMA", row.get("row_id", "?"))
        require(row["claim_class"] in allowed_classes, "E_ROW_CLASS", row["row_id"])
        require(row["verdict"] in allowed_verdicts, "E_ROW_VERDICT", row["row_id"])
        require(row["severity"] in {"NONE", "P1", "P2"}, "E_ROW_SEVERITY", row["row_id"])
        require(row["status"] in {"CLOSED", "OPEN_ROUTED", "PRESERVE_BOUNDARY"}, "E_ROW_STATUS", row["row_id"])
        require(isinstance(row["claim"], str) and row["claim"], "E_ROW_CLAIM", row["row_id"])
        require(isinstance(row["owner"], str) and row["owner"], "E_ROW_OWNER", row["row_id"])
        require(isinstance(row["acceptance_criterion"], str) and row["acceptance_criterion"], "E_ROW_ACCEPTANCE", row["row_id"])
        require(isinstance(row["origin_routes"], list), "E_ROW_ROUTES", row["row_id"])
        require(isinstance(row["claim_surface"], list) and row["claim_surface"], "E_ROW_SURFACE", row["row_id"])
        for anchor in row["claim_surface"]:
            require(set(anchor) == {"path", "lines", "role"}, "E_ANCHOR_SCHEMA", row["row_id"])
            require(anchor["path"] in bound_paths and anchor["lines"] and anchor["role"], "E_ANCHOR_BINDING", row["row_id"])
        for key in ("source_authority", "code_authority"):
            nested = row[key]
            require(set(nested) == {"status", "path", "lines"}, "E_NESTED_AUTH_SCHEMA", row["row_id"])
            require(nested["status"] and nested["path"] and nested["lines"], "E_NESTED_AUTH_VALUE", row["row_id"])
            if nested["path"] != "NOT_APPLICABLE":
                require(nested["path"] in bound_paths, "E_NESTED_AUTH_PATH", row["row_id"])
        run_auth = row["runtime_authority"]
        require(set(run_auth) == {"status", "artifact", "route"}, "E_RUNTIME_SCHEMA", row["row_id"])
        require(row["artifact_class"] in {"SOURCE", "GENERATED", "COPIED", "MIXED"}, "E_ROW_ARTIFACT", row["row_id"])
        if row["severity"] == "NONE":
            require(row["status"] != "OPEN_ROUTED", "E_ROW_NONE_OPEN", row["row_id"])
        else:
            require(row["status"] == "OPEN_ROUTED", "E_ROW_OPEN", row["row_id"])
            require(row["target_phase"] != "NOT_APPLICABLE", "E_ROW_TARGET", row["row_id"])

    route_ids = [row["route_id"] for row in obj["input_routes"]]
    require(route_ids == EXPECTED_ROUTE_IDS and len(set(route_ids)) == 17, "E_ROUTE_DENOMINATOR")
    require(sum(x.startswith("P065-S70-") for x in route_ids) == 13, "E_ROUTE_STEP70")
    require(sum(x.startswith("P065-S71-") for x in route_ids) == 2, "E_ROUTE_STEP71")
    require(sum(x.startswith("P065-S72-") for x in route_ids) == 2, "E_ROUTE_STEP72")
    expected_artifacts = {
        70: "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json",
        71: "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json",
        72: "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json",
    }
    topology = strict_load(blob(EXPECTED_PARENT, expected_artifacts[70]))
    code_matrix = strict_load(blob(EXPECTED_PARENT, expected_artifacts[71]))
    skew_matrix = strict_load(blob(EXPECTED_PARENT, expected_artifacts[72]))
    expected_records = {
        **{x["id"]: x for x in topology["findings"]},
        **{x["finding_id"]: x for x in code_matrix["findings"]},
        **{f"P065-{x['id']}": x for x in skew_matrix["findings"]},
    }
    for route in obj["input_routes"]:
        require(set(route) == {"route_id", "origin_step", "origin_artifact", "origin_record", "disposition"}, "E_ROUTE_SCHEMA", route.get("route_id", "?"))
        route_id = route["route_id"]
        step = int(route_id.split("-S", 1)[1].split("-", 1)[0])
        require(route["origin_step"] == step, "E_ROUTE_STEP", route_id)
        require(route["origin_artifact"] == expected_artifacts[step], "E_ROUTE_ARTIFACT", route_id)
        require(route["origin_record"] == expected_records[route_id], "E_ROUTE_ORIGIN_RECORD", route_id)
        require(route["disposition"] == "PRESERVE_EXACT_ORIGIN_RECORD", "E_ROUTE_DISPOSITION", route_id)
    for row in rows:
        require(all(route_id in route_ids for route_id in row["origin_routes"]), "E_ROW_UNKNOWN_ROUTE", row["row_id"])

    runtime_attestation = strict_load(blob(EXPECTED_PARENT, "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json"))
    for row in rows:
        run_auth = row["runtime_authority"]; pointer = run_auth["route"]
        if pointer == "NOT_APPLICABLE":
            require(run_auth["artifact"] == "NOT_APPLICABLE", "E_RUNTIME_NA_ARTIFACT", row["row_id"])
            continue
        require(run_auth["artifact"] == "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json", "E_RUNTIME_ARTIFACT", row["row_id"])
        if pointer == "explicit_profile.selfconsistent":
            ids = [x["run_id"] for x in runtime_attestation["official_runs"] if x["run_id"].startswith("P065-OFFICIAL-V1024-SELFCONSISTENT-")]
            require(ids == ["P065-OFFICIAL-V1024-SELFCONSISTENT-312", "P065-OFFICIAL-V1024-SELFCONSISTENT-314"], "E_RUNTIME_SELFCONSISTENT")
            continue
        require(pointer in RUNTIME_POINTERS, "E_RUNTIME_POINTER", pointer)
        route_name, observation = RUNTIME_POINTERS[pointer]
        matching = [x for x in runtime_attestation["route_runs"] if x["route"] == route_name and x["mutation"] == "none"]
        require(len(matching) == 4, "E_RUNTIME_RUN_DENOMINATOR", pointer)
        require(all(isinstance(x["observations"], dict) and observation in x["observations"] for x in matching), "E_RUNTIME_OBSERVATION", pointer)

    expected_findings = [
        {"id":"S74-F01","severity":"P1","finding":"Route-specific regular-solution, root, unit, width and blend behavior conflicts with blanket/full-conformance records.","owner":"PHASE-083-IMPLEMENTATION-CONTRACT"},
        {"id":"S74-F02","severity":"P1","finding":"LCO per-peak Omega, analytic real-fit, capacity-basis and main-body implementation claims exceed their authority.","owner":"PHASE-078-LCO-CLOSURE"},
        {"id":"S74-F03","severity":"P2","finding":"HTML generation, versioning, unit labels, portability, visual defects and exact output require repair.","owner":"PHASE-089-RELEASE-QA"},
        {"id":"S74-F04","severity":"P2","finding":"The inherited 17-image missing-glyph count conflicts with the fresh 15-path visual numerator; the remaining two identities are GROUND_NOT_FOUND.","owner":"PHASE-089-RELEASE-QA"},
    ]
    require(obj["findings"] == expected_findings, "E_FINDINGS")
    f41 = rows[22]
    require(f41["row_id"] == "D74-023" and f41["source_authority"] == {
        "status":"FRESH_VISUAL_COUNT_15_AND_REMAINDER_GROUND_NOT_FOUND",
        "path":"Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md", "lines":"182-190",
    }, "E_F41_AUTHORITY")
    require(all(name in f41["acceptance_criterion"] for name in F41_PATHS), "E_F41_PATHS")
    require("remaining two as GROUND_NOT_FOUND" in f41["acceptance_criterion"], "E_F41_REMAINDER")

    counts = obj["counts"]
    require(counts["conformance_rows"] == 41, "E_COUNT_ROWS")
    for severity in ("P1", "P2", "NONE"):
        require(counts[f"severity_{severity.lower()}"] == sum(r["severity"] == severity for r in rows), "E_COUNT_SEVERITY", severity)
    require(counts["open_routed"] == sum(r["status"] == "OPEN_ROUTED" for r in rows), "E_COUNT_OPEN")
    require(counts["input_routes"] == 17, "E_COUNT_ROUTES")
    require(counts["source_bindings"] == 56, "E_COUNT_BINDINGS")
    require(counts["step73_runtime_routes"] == 3, "E_COUNT_STEP73_ROUTES")

    clone = copy.deepcopy(obj); actual = clone.pop("semantic_sha256")
    require(actual == sha256(canonical(clone)), "E_SEMANTIC")
    nodes, depth = traverse(obj)
    require(nodes > 900 and depth >= 5, "E_TRAVERSAL", f"{nodes}/{depth}")
    return nodes, depth


def verify_controls(obj: dict[str, Any], rev: str) -> None:
    rows = obj["control_source_bindings"]
    require(len(rows) == 6, "E_CONTROL_COUNT")
    expected = sorted(x for x in EXACT_PATHS if x != str(MATRIX).replace("\\", "/"))
    require(sorted(row["path"] for row in rows) == expected, "E_CONTROL_PATHS")
    for row in rows:
        path = row["path"]
        raw = blob(rev, path)
        spec = f":{path}" if rev == ":" else f"{rev}:{path}"
        require(row["sha256"] == sha256(raw), "E_CONTROL_HASH", path)
        require(row["git_blob"] == str(git("rev-parse", spec)).strip(), "E_CONTROL_BLOB", path)
        require(row["size_bytes"] == len(raw), "E_CONTROL_SIZE", path)


def verify_docs() -> None:
    result = RESULT.read_text(encoding="utf-8")
    require(GATE in result, "E_RESULT_GATE")
    require("GROUND_NOT_FOUND" in result and "AGENT_FULL_READ" in result, "E_RESULT_BOUNDARY")
    require("fresh-observed 15-path numerator" in result and "나머지 2개 identity 부재" in result, "E_RESULT_F41_SUMMARY")
    require(all(name in result for name in F41_PATHS), "E_RESULT_F41_PATHS")
    require(all(marker in result for marker in (
        "lineage-detailed-plan.md`: 1–851.",
        "PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`: 1–138.",
        "ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`: 1–395.",
    )), "E_RESULT_READ_COVERAGE")
    for path in (PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER):
        text = path.read_text(encoding="utf-8")
        require("Step 74" in text and GATE in text, "E_RECORD_STEP74", str(path))
        require(EXPECTED_SUBJECT in text, "E_RECORD_SUBJECT", str(path))
    handover = HANDOVER.read_text(encoding="utf-8")
    chain = handover.split("## Canonical Chain", 1)[1].split("## Handover Chain", 1)[0]
    pairs = re.findall(r"^(\d+)\. (.+)$", chain, flags=re.MULTILINE)
    require(len(pairs) == 24 and [int(key) for key, _ in pairs] == list(range(1, 25)), "E_HANDOVER_CHAIN_TOPOLOGY")
    entries = {int(key): value for key, value in pairs}
    require(entries[18] == "현재 result: `Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md`", "E_HANDOVER_CURRENT_RESULT")
    require(entries[22] == "직전 final persistence: Step 73 commit `5c5c555462f1dbf0603eedda6a1d5b62684cffdf`; `PASS_P065_STEP73_PERSISTENCE`", "E_HANDOVER_LAST_PERSISTENCE")
    require("- 독립 final artifact 검독: `P0/P1/P2=0/0/0`." in result, "E_RESULT_REVIEW")


def validate_precommit_porcelain(raw: str) -> None:
    records = [record for record in raw.split("\0") if record]
    require(len(records) == len(EXACT_PATHS), "E_STATUS_COUNT", repr(records))
    paths: list[str] = []
    for record in records:
        require(len(record) >= 4 and record[2] == " ", "E_STATUS_FORMAT", repr(record))
        require(record[:2] in {"A ", "M "}, "E_STATUS_NOT_INDEX_ONLY", repr(record))
        paths.append(record[3:].replace("\\", "/"))
    require(sorted(paths) == EXACT_PATHS, "E_STATUS_PATHS", repr(sorted(paths)))


def verify_exact_stage() -> None:
    staged = sorted(x for x in str(git("diff", "--cached", "--name-only")).splitlines() if x)
    require(staged == EXACT_PATHS, "E_EXACT_STAGE", repr(staged))
    unstaged = [x for x in str(git("diff", "--name-only", "--", *EXACT_PATHS)).splitlines() if x]
    require(not unstaged, "E_UNSTAGED", repr(unstaged))
    require(not str(git("diff", "--name-only", "--", "Claude" )).strip(), "E_CLAUDE_DIRTY")
    require(not str(git("diff", "--cached", "--name-only", "--", "Claude" )).strip(), "E_CLAUDE_STAGED")
    validate_precommit_porcelain(str(git("status", "--porcelain=v1", "-z", "--untracked-files=all")))
    require(not str(git("diff", "--check")).strip(), "E_WORKTREE_DIFF_CHECK")
    require(not str(git("diff", "--cached", "--check")).strip(), "E_INDEX_DIFF_CHECK")
    for path in EXACT_PATHS:
        require(Path(path).read_bytes() == blob(":", path), "E_INDEX_WORKTREE_BYTES", path)


def live_tip(ref: str) -> str:
    fields = str(git("ls-remote", "--heads", "origin", ref)).strip().split()
    require(len(fields) >= 2 and fields[1] == ref, "E_LIVE_REF", repr(fields))
    return fields[0]


def verify_refs(expected_commit: str | None = None) -> None:
    head = str(git("rev-parse", "HEAD")).strip()
    branch = str(git("branch", "--show-current")).strip()
    require(branch == BRANCH, "E_ACTIVE_BRANCH", branch)
    require(str(git("rev-parse", "codex/lib-physics-endgame-v1025_2")).strip() == PROTECTED, "E_PROTECTED")
    require(str(git("rev-parse", "origin/codex/lib-physics-endgame-v1025_2")).strip() == PROTECTED, "E_PROTECTED_TRACKING")
    require(live_tip("refs/heads/codex/lib-physics-endgame-v1025_2") == PROTECTED, "E_PROTECTED_LIVE")
    require(str(git("rev-parse", "origin/main")).strip() == MAIN, "E_MAIN")
    require(live_tip("refs/heads/main") == MAIN, "E_MAIN_LIVE")
    require(str(git("rev-parse", "--abbrev-ref", "@{upstream}")).strip() == f"origin/{BRANCH}", "E_UPSTREAM_NAME")
    if expected_commit is None:
        require(head == EXPECTED_PARENT, "E_PRECOMMIT_PARENT", head)
        require(str(git("rev-parse", "@{upstream}")).strip() == EXPECTED_PARENT, "E_PRECOMMIT_UPSTREAM")
        require(str(git("rev-parse", f"origin/{BRANCH}")).strip() == EXPECTED_PARENT, "E_PRECOMMIT_TRACKING")
        require(live_tip(f"refs/heads/{BRANCH}") == EXPECTED_PARENT, "E_PRECOMMIT_LIVE")
    else:
        require(head == expected_commit, "E_PERSIST_HEAD", head)
        require(str(git("rev-parse", "@{upstream}")).strip() == expected_commit, "E_PERSIST_UPSTREAM")
        require(str(git("rev-parse", f"origin/{BRANCH}")).strip() == expected_commit, "E_PERSIST_TRACKING")
        require(live_tip(f"refs/heads/{BRANCH}") == expected_commit, "E_PERSIST_LIVE_REMOTE")
        require(str(git("show", "-s", "--format=%P", expected_commit)).strip() == EXPECTED_PARENT, "E_PERSIST_PARENT")
        require(str(git("show", "-s", "--format=%s", expected_commit)).strip() == EXPECTED_SUBJECT, "E_PERSIST_SUBJECT")
        changed = sorted(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", expected_commit)).splitlines())
        require(changed == EXACT_PATHS, "E_PERSIST_PATHS", repr(changed))
        require(not str(git("diff", "--check", EXPECTED_PARENT, expected_commit)).strip(), "E_PERSIST_DIFF_CHECK")
        for path in EXACT_PATHS:
            require(Path(path).read_bytes() == blob(expected_commit, path), "E_COMMIT_WORKTREE_BYTES", path)


def validate_fixture_path(path: Path, allowed_names: set[str]) -> Path:
    require(path.is_absolute(), "E_FIXTURE_NOT_ABSOLUTE", str(path))
    require(path.name in allowed_names, "E_FIXTURE_NAME", path.name)
    lexical = Path(os.path.abspath(str(path)))
    temp_root = Path(os.path.abspath(tempfile.gettempdir()))
    require(os.path.commonpath((str(lexical), str(temp_root))) == str(temp_root), "E_FIXTURE_BOUNDARY", str(path))
    cursor = lexical
    while cursor != temp_root:
        require(cursor.exists(), "E_FIXTURE_MISSING", str(cursor))
        require(not cursor.is_symlink(), "E_FIXTURE_SYMLINK", str(cursor))
        if hasattr(cursor, "is_junction"):
            require(not cursor.is_junction(), "E_FIXTURE_JUNCTION", str(cursor))
        cursor = cursor.parent
    return lexical


def validate_determinism_fixtures(one: Path, two: Path) -> tuple[str, str]:
    first = validate_fixture_path(one, {"matrix-step74-one.json"}).read_bytes()
    second = validate_fixture_path(two, {"matrix-step74-two.json"}).read_bytes()
    require(first == second, "E_DETERMINISM")
    require(first == MATRIX.read_bytes(), "E_DETERMINISM_STAGED")
    return sha256(first), sha256(second)


def validate_output_sentinel(path: Path) -> int:
    raw = validate_fixture_path(path, {"not-a-matrix-name.json"}).read_bytes()
    require(raw == b"P065_STEP74_SENTINEL\n", "E_OUTPUT_SENTINEL_WRITE")
    return 1


def transaction_negative_tests() -> int:
    matrix_path = str(MATRIX).replace("\\", "/")
    added = {matrix_path, str(RESULT).replace("\\", "/"), str(BUILDER).replace("\\", "/"), str(VALIDATOR).replace("\\", "/")}
    base = "".join(
        f"{'A ' if path in added else 'M '} {path}\0"
        for path in EXACT_PATHS
    )
    probes = [
        base + "?? Codex/rogue.tmp\0",
        base.replace(f"A  {matrix_path}", f" M {matrix_path}", 1),
        base.replace(f"A  {matrix_path}", f"R  {matrix_path}", 1),
        base.replace(f"A  {matrix_path}\0", "", 1),
    ]
    for raw in probes:
        try:
            validate_precommit_porcelain(raw)
        except ValidationError:
            pass
        else:
            raise ValidationError("E_TRANSACTION_NEGATIVE")
    return len(probes)


def negative_tests(obj: dict[str, Any], expected_matrix_sha256: str) -> int:
    bad_json = [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}']
    for raw in bad_json:
        try: strict_load(raw)
        except ValidationError: pass
        else: raise ValidationError("E_NEGATIVE_JSON")
    mutations = []
    m = copy.deepcopy(obj); m["authority"]["publication_ready"] = True; mutations.append(m)
    m = copy.deepcopy(obj); m["authority"]["new_external_truth"] = True; mutations.append(m)
    m = copy.deepcopy(obj); m["artifact_genealogy"][0]["independent_support"] = True; mutations.append(m)
    m = copy.deepcopy(obj); m["conformance_rows"][1]["row_id"] = "D74-001"; mutations.append(m)
    m = copy.deepcopy(obj); m["conformance_rows"][0]["owner"] = ""; mutations.append(m)
    m = copy.deepcopy(obj); m["conformance_rows"][0]["severity"] = "NONE"; mutations.append(m)
    m = copy.deepcopy(obj); m["counts"]["open_routed"] += 1; mutations.append(m)
    m = copy.deepcopy(obj); m["source_bindings"][0]["sha256"] = "0" * 64; mutations.append(m)
    m = copy.deepcopy(obj); m["input_routes"].pop(); mutations.append(m)
    m = copy.deepcopy(obj); m["input_routes"][0]["route_id"] = "P065-S70-F07"; mutations.append(m)
    m = copy.deepcopy(obj); m["input_routes"][0]["origin_record"] = {}; mutations.append(m)
    m = copy.deepcopy(obj); m["conformance_rows"][0]["runtime_authority"]["route"] = "fabricated.route.not.in.attestation"; mutations.append(m)
    m = copy.deepcopy(obj); m["findings"][3]["finding"] = "seventeen only"; mutations.append(m)
    m = copy.deepcopy(obj); m["conformance_rows"][22]["acceptance_criterion"] = "GROUND_NOT_FOUND"; mutations.append(m)
    m = copy.deepcopy(obj); m["semantic_sha256"] = "0" * 64; mutations.append(m)
    for mutation in mutations:
        try: validate_matrix(mutation)
        except ValidationError: pass
        else: raise ValidationError("E_NEGATIVE_SEMANTIC")
    coherent = copy.deepcopy(obj)
    coherent["conformance_rows"][38]["claim"] = "Omega > 2RT independently proves graphite phase identity."
    coherent["conformance_rows"][38]["owner"] = "MALICIOUS-OVERCLAIM-OWNER"
    coherent["conformance_rows"][38]["acceptance_criterion"] = "PROMOTE_WITHOUT_INDEPENDENT_AUTHORITY"
    payload = copy.deepcopy(coherent)
    payload.pop("semantic_sha256")
    coherent["semantic_sha256"] = sha256(canonical(payload))
    validate_matrix(coherent)
    coherent_raw = (json.dumps(coherent, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    try: validate_matrix_pin(coherent_raw, expected_matrix_sha256)
    except ValidationError: pass
    else: raise ValidationError("E_NEGATIVE_COHERENT_MATRIX_PIN")
    return len(bad_json) + len(mutations) + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--persistence", action="store_true")
    parser.add_argument("--expected-commit")
    parser.add_argument("--determinism-one", type=Path, required=True)
    parser.add_argument("--determinism-two", type=Path, required=True)
    parser.add_argument("--output-sentinel", type=Path, required=True)
    parser.add_argument("--expected-builder-sha256", required=True)
    parser.add_argument("--expected-validator-sha256", required=True)
    parser.add_argument("--expected-matrix-sha256", required=True)
    args = parser.parse_args()
    require(MATRIX.exists(), "E_CONFORMANCE_ARTIFACT_MISSING", str(MATRIX))
    matrix_raw = MATRIX.read_bytes()
    validate_matrix_pin(matrix_raw, args.expected_matrix_sha256)
    obj = strict_load(matrix_raw)
    nodes, depth = validate_matrix(obj)
    policy_negatives = validate_source_policy(
        args.expected_commit if args.persistence and args.expected_commit else ":",
        args.expected_builder_sha256, args.expected_validator_sha256,
    )
    negatives = negative_tests(obj, args.expected_matrix_sha256)
    output_negatives = validate_output_sentinel(args.output_sentinel)
    transaction_negatives = transaction_negative_tests()
    verify_docs()
    raw1, raw2 = validate_determinism_fixtures(args.determinism_one, args.determinism_two)
    if args.persistence:
        require(bool(args.expected_commit), "E_EXPECTED_COMMIT")
        verify_refs(args.expected_commit)
        verify_controls(obj, args.expected_commit)
        require(not str(git("status", "--porcelain")).strip(), "E_PERSIST_DIRTY")
        terminal = "PASS_P065_STEP74_PERSISTENCE"
    else:
        require(args.expected_commit is None, "E_UNEXPECTED_COMMIT")
        verify_refs()
        verify_exact_stage()
        verify_controls(obj, ":")
        terminal = GATE
    print(terminal, json.dumps({
        "rows": len(obj["conformance_rows"]), "routes": len(obj["input_routes"]),
        "nodes": nodes, "depth": depth, "negative": negatives,
        "source_policy_negative": policy_negatives,
        "builder_sha256": args.expected_builder_sha256,
        "validator_sha256": args.expected_validator_sha256,
        "matrix_sha256": args.expected_matrix_sha256,
        "output_negative": output_negatives,
        "transaction_negative": transaction_negatives,
        "determinism": [raw1, raw2],
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"FAIL_P065_STEP74 {exc}", file=sys.stderr)
        raise SystemExit(1)
