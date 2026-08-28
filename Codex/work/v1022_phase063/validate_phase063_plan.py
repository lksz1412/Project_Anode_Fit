#!/usr/bin/env python3
"""Validate the Phase 063 detailed-plan activation and its Git checkpoint."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
import re
import subprocess
from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any

from pypdf import PdfReader


REPO = Path(__file__).resolve().parents[3]
PLAN = REPO / "Codex/plans/2026-08-28-phase063-v1022-lineage-detailed-plan.md"
SCRIPT = Path(__file__).resolve()
OUTPUT = REPO / "Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json"
RESULT = REPO / "Codex/results/PHASE_063_PLAN_ACTIVATION_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
INTENT = REPO / "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json"

EXPECTED_PARENT = "69d938da0f5649d6342364c96bf612488879a8f8"
EXPECTED_PARENT_PARENT = "247e9b0b28d185604753f40ee0244cfe0bf068cf"
EXPECTED_PARENT_SUBJECT = "audit(phase062): close v1021 lineage gate"
EXPECTED_SUBJECT = "docs(phase063): plan v1022 lineage reaudit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
EXPECTED_PLAN_SHA256 = "c5c6b763841ce62cd12f6b8b4de18d916f0198e9c7c40b821a2e906ec930547d"
EXPECTED_INTENT96_SHA256 = "f5fa315bfcdc24545feab0dabc4f4d45df96e2f561aebc838145228bee88ce37"
EXPECTED_CONTROL_SHA256 = {
    "result": "fe6b481e1e962ea9ca2964b4e1b5b1c91dcd875d36b33b1218af03023c5ae082",
    "active_ledger": "f10014b96126863906d68c75ad4a41693f522d8ffc905a610b63f7655eec6ad8",
    "parent_ledger": "6728da30d9200dd4f0fdb40004f37df60354c38810b02f2c97994d137307224a",
    "handover": "6a9aa17fb5de7af6f819144a3799e204c05c99d944416566a8123d532ef6e93b",
}
EXPECTED_GIT_HELPER_AST_SHA256 = {
    "git": "f5525c5b3b3014a13b626f9d6878ede775a1421ec0b35dae84f1770b459276e4",
    "git_bytes": "35c817369f04c8827f7b92a58de320d79f7167f53e94fa162a83a023dc9102a6",
}
SUPPLEMENTAL_PATH = "Claude/plans/2026-07-17-v1022-master-plan.md"
SUPPLEMENTAL_BLOB = "f50deee51df77dca8d07a2d9b9fd150fa93309cc"
GIT_TIMEOUT = 90

EXACT_SEVEN = [
    "Codex/plans/2026-08-28-phase063-v1022-lineage-detailed-plan.md",
    "Codex/work/v1022_phase063/validate_phase063_plan.py",
    "Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json",
    "Codex/results/PHASE_063_PLAN_ACTIVATION_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]
EXACT_SEVEN_SET = set(EXACT_SEVEN)
OUTPUT_REL = OUTPUT.relative_to(REPO).as_posix()
NONSELF = [path for path in EXACT_SEVEN if path != OUTPUT_REL]

OBSERVATIONS = [
    ("Codex/results/PHASE_057P_V1022_R1_CONTROL_AND_LINEAGE_OBSERVATIONS.md", 214, "0d67dcfa3bbce07f82b5530db699b3795110ea4a2b351a980657191262abaa10"),
    ("Codex/results/PHASE_057Q_V1022_R1_SNAPSHOT_OBSERVATIONS.md", 130, "d6ed22e77a4d83f33b039de602f8a91d33cbd7f7ee5518ba994403ea78d83513"),
    ("Codex/results/PHASE_057R_V1022_R2_CH1_COMPLETION_OBSERVATIONS.md", 173, "2be5735eb8bb8b7109a705de0ed7875cbab7586e7fca1eefc2080eb8ef85d0ba"),
    ("Codex/results/PHASE_057S_V1022_R3_LCO_COMPLETION_OBSERVATIONS.md", 166, "7994051df9c1f4beeb3707b4d57e59da9a31161c1a7d7ca53faa5545f2524d68"),
    ("Codex/results/PHASE_057T_V1022_R4_MATERIAL_SURVEY_OBSERVATIONS.md", 201, "5fe61fe155bc5136afa18cda999a853a1f865b1f2e5c7c50ad19b533f74ecb6a"),
    ("Codex/results/PHASE_057U_V1022_R5_RV_SM2_OBSERVATIONS.md", 214, "038f2c2e0b8e827e5c21a9907f2be881e1309fc43a75ca141654377bff69c7b3"),
    ("Codex/results/PHASE_057V_V1022_FR_A01_A08_A20_OBSERVATIONS.md", 284, "3f67eae26afe10e2c0febdac882d636cd928ab0dbb8c76b6050c56d8cefd7abc"),
    ("Codex/results/PHASE_057W_V1022_FR_A09_A16_OBSERVATIONS.md", 241, "7b00318e9bc7996f68e2bec53bfbe34bf570eb4b7d3f6e52bba87955e6cf7eb3"),
    ("Codex/results/PHASE_057X_V1022_FR_A17_A19_A21_A23_OBSERVATIONS.md", 283, "f84dbd3357fc622a2a3f6adc195f179b63ef970bb72a9a3b782c6290b0e69d49"),
    ("Codex/results/PHASE_057Y_V1022_FR_CONTROL_TRIAGE_EXEC_OBSERVATIONS.md", 198, "bdffda0188bef7e395934f704655ad97d97caccbf3d54fe71b602445be55ccce"),
    ("Codex/results/PHASE_057Z_V1022_R6_R9_AUD_V23_SURVEY_OBSERVATIONS.md", 259, "79d82adccb8b83878250a4306407a059c21a530dc4ab7f5090718586bc9e2632"),
]


class ValidationError(RuntimeError):
    pass


READ_ONLY_GIT_COMMANDS = {
    "cat-file", "diff", "diff-tree", "ls-files", "ls-remote", "ls-tree",
    "rev-parse", "show", "show-ref",
}


def read_only_git_argv(args: tuple[str, ...]) -> bool:
    def is_hex40(value: str) -> bool:
        return len(value) == 40 and all(char in "0123456789abcdef" for char in value)

    if args == ("branch", "--show-current") or args == ("symbolic-ref", "-q", "HEAD"):
        return True
    if len(args) == 4 and args[:3] == ("show-ref", "--verify", "--hash"):
        return args[3].startswith(("refs/heads/", "refs/remotes/origin/"))
    if len(args) == 4 and args[:3] == ("ls-remote", "--heads", "origin"):
        return args[3] in {
            f"refs/heads/{ACTIVE_BRANCH}", f"refs/heads/{PROTECTED_BRANCH}", "refs/heads/main",
        }
    if args == ("ls-tree", "-r", "-l", BASELINE, "--", "Claude/docs/v1.0.22"):
        return True
    if len(args) == 2 and args[0] == "rev-parse":
        value = args[1]
        return value in {
            "HEAD", "@{upstream}", f"{EXPECTED_PARENT}^", f"{BASELINE}:{SUPPLEMENTAL_PATH}",
        } or (value.endswith("^") and is_hex40(value[:-1]))
    if args == ("rev-parse", "--symbolic-full-name", "@{upstream}"):
        return True
    if len(args) == 4 and args[:3] == ("show", "-s", "--format=%s"):
        return is_hex40(args[3])
    if len(args) == 2 and args[0] == "show":
        spec = args[1]
        if spec.startswith(":"):
            return spec[1:] in EXACT_SEVEN_SET
        commit, separator, rel = spec.partition(":")
        return separator == ":" and is_hex40(commit) and rel in EXACT_SEVEN_SET
    if len(args) == 3 and args[:2] == ("cat-file", "blob"):
        return is_hex40(args[2])
    if args in {
        ("diff", "--name-only"),
        ("diff", "HEAD", "--name-only", "-z"),
        ("diff", "--cached", "--name-only", "-z"),
        ("ls-files", "--others", "--exclude-standard", "-z"),
        ("ls-files", "--others", "--exclude-standard", "--", "Claude"),
    }:
        return True
    if len(args) == 5 and args[:2] == ("diff", "--name-only"):
        return is_hex40(args[2]) and args[3:] == ("--", "Claude")
    if len(args) == 6 and args[:2] == ("diff", "--name-only"):
        return is_hex40(args[2]) and is_hex40(args[3]) and args[4:] == ("--", "Claude")
    if len(args) == 6 and args[:5] == (
        "diff-tree", "--no-commit-id", "--name-only", "-r", "-z",
    ):
        return is_hex40(args[5])
    return False


def git(*args: str, check: bool = True) -> str:
    if not read_only_git_argv(args):
        raise ValidationError(f"E_FORBIDDEN_GIT_COMMAND: {args!r}")
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=GIT_TIMEOUT, check=False,
    )
    if check and proc.returncode:
        raise ValidationError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout.decode("utf-8", errors="strict").strip()


def git_bytes(*args: str) -> bytes:
    if not read_only_git_argv(args):
        raise ValidationError(f"E_FORBIDDEN_GIT_COMMAND: {args!r}")
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=GIT_TIMEOUT, check=False,
    )
    if proc.returncode:
        raise ValidationError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def ref_hash_or_none(ref: str) -> str | None:
    value = git("show-ref", "--verify", "--hash", ref, check=False)
    return value or None


def ls_remote_head(ref: str) -> str:
    output = git("ls-remote", "--heads", "origin", ref)
    rows = [line.split() for line in output.splitlines() if line.strip()]
    if len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != ref:
        raise ValidationError(f"E_LS_REMOTE_HEAD_CARDINALITY: {ref}: {rows}")
    return rows[0][0]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_bytes(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def reject_constant(value: str) -> Any:
    raise ValueError(f"non-finite JSON constant: {value}")


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def traverse(value: Any) -> int:
    if value is None or isinstance(value, (str, bool, int)):
        return 1
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite JSON number")
        return 1
    if isinstance(value, list):
        return 1 + sum(traverse(item) for item in value)
    if isinstance(value, dict):
        return 1 + sum(1 + traverse(item) for key, item in value.items() if isinstance(key, str))
    raise ValueError(f"unsupported JSON node: {type(value).__name__}")


def strict_load(path: Path) -> tuple[Any, int]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique_pairs,
        parse_constant=reject_constant,
    )
    return value, traverse(value)


def source_policy_errors(source_text: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return ["SOURCE_SYNTAX_ERROR"]
    aliases: dict[str, str] = {}
    allowed_import_roots = {
        "__future__", "argparse", "ast", "collections", "copy", "hashlib", "io",
        "json", "math", "os", "pathlib", "pypdf", "re", "subprocess", "typing",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                root = item.name.split(".", 1)[0]
                aliases[item.asname or root] = item.name
                if root not in allowed_import_roots:
                    errors.append("FORBIDDEN_IMPORT_" + root.upper())
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            if root not in allowed_import_roots:
                errors.append("FORBIDDEN_IMPORTFROM_" + root.upper())
            for item in node.names:
                aliases[item.asname or item.name] = module + "." + item.name
    def qualified_name(node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            parent = qualified_name(node.value)
            return (parent + "." if parent else "") + node.attr
        return ""

    assignments = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.Assign, ast.AnnAssign))
    ]
    for _ in range(len(assignments) + 1):
        changed = False
        for node in assignments:
            value = node.value
            resolved_value = qualified_name(value) if value is not None else ""
            if not resolved_value:
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and aliases.get(target.id) != resolved_value:
                    aliases[target.id] = resolved_value
                    changed = True
        if not changed:
            break

    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }

    helper_names = set(EXPECTED_GIT_HELPER_AST_SHA256)
    for helper_name, expected_digest in EXPECTED_GIT_HELPER_AST_SHA256.items():
        definitions = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == helper_name
        ]
        if definitions:
            valid = (
                len(definitions) == 1
                and isinstance(parents.get(definitions[0]), ast.Module)
                and hashlib.sha256(
                    (ast.get_source_segment(source_text, definitions[0]) or "")
                    .replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
                ).hexdigest() == expected_digest
            )
            if not valid:
                errors.append("FORBIDDEN_GIT_HELPER_DEFINITION")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and node.id in helper_names:
            errors.append("FORBIDDEN_GIT_HELPER_BINDING")
        elif isinstance(node, ast.arg) and node.arg in helper_names:
            errors.append("FORBIDDEN_GIT_HELPER_BINDING")
        elif isinstance(node, ast.Import):
            if any((item.asname or item.name.split(".", 1)[0]) in helper_names for item in node.names):
                errors.append("FORBIDDEN_GIT_HELPER_BINDING")
        elif isinstance(node, ast.ImportFrom):
            if any((item.asname or item.name) in helper_names for item in node.names):
                errors.append("FORBIDDEN_GIT_HELPER_BINDING")

    def enclosing_function(node: ast.AST) -> str:
        current = parents.get(node)
        while current is not None:
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return current.name
            current = parents.get(current)
        return ""

    def exact_constant_list(node: ast.expr, values: list[str]) -> bool:
        return (
            isinstance(node, (ast.List, ast.Tuple))
            and len(node.elts) == len(values)
            and all(
                isinstance(element, ast.Constant) and element.value == expected
                for element, expected in zip(node.elts, values)
            )
        )

    def allowed_git_subprocess(node: ast.Call, command: ast.expr) -> bool:
        function = enclosing_function(node)
        if function in {"git", "git_bytes"}:
            return (
                isinstance(command, (ast.List, ast.Tuple))
                and len(command.elts) == 2
                and isinstance(command.elts[0], ast.Constant)
                and command.elts[0].value == "git"
                and isinstance(command.elts[1], ast.Starred)
                and isinstance(command.elts[1].value, ast.Name)
                and command.elts[1].value.id == "args"
            )
        if function == "cat_file_batch":
            return exact_constant_list(command, ["git", "cat-file", "--batch"])
        if function == "verify_staged":
            return exact_constant_list(command, ["git", "diff", "--check", "--cached"])
        return False

    subprocess_execution_calls = {
        "subprocess.run", "subprocess.Popen", "subprocess.call",
        "subprocess.check_call", "subprocess.check_output", "subprocess.getoutput",
        "subprocess.getstatusoutput",
    }
    os_command_calls = {"os.system", "os.popen", "os.spawnl", "os.spawnv"}
    os_execution_calls = os_command_calls | {
        "os.execl", "os.execle", "os.execlp", "os.execlpe", "os.execv", "os.execve",
        "os.execvp", "os.execvpe", "os.posix_spawn", "os.posix_spawnp", "os.spawnle",
        "os.spawnlp", "os.spawnlpe", "os.spawnve", "os.spawnvp", "os.spawnvpe",
        "os.startfile",
    }

    def is_direct_call(node: ast.expr, parent: ast.AST | None) -> bool:
        return isinstance(parent, ast.Call) and parent.func is node

    def is_simple_name_alias(node: ast.expr, parent: ast.AST | None) -> bool:
        if isinstance(parent, ast.Assign) and parent.value is node:
            return bool(parent.targets) and all(isinstance(target, ast.Name) for target in parent.targets)
        return isinstance(parent, ast.AnnAssign) and parent.value is node and isinstance(parent.target, ast.Name)

    def allowed_os_replace(node: ast.Call) -> bool:
        return (
            enclosing_function(node) == "write_output"
            and len(node.args) == 2
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == "temp"
            and isinstance(node.args[1], ast.Name)
            and node.args[1].id == "OUTPUT"
            and not node.keywords
        )

    for node in ast.walk(tree):
        parent = parents.get(node)
        if isinstance(node, (ast.Name, ast.Attribute)):
            resolved_reference = qualified_name(node)
            if resolved_reference in subprocess_execution_calls:
                if not is_direct_call(node, parent) and not is_simple_name_alias(node, parent):
                    errors.append("FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE")
            elif resolved_reference in os_execution_calls:
                if not is_direct_call(node, parent) and not is_simple_name_alias(node, parent):
                    errors.append("FORBIDDEN_OS_CALLABLE_REFERENCE")
            if isinstance(node, ast.Attribute) and (
                resolved_reference.startswith("subprocess.__dict__")
                or resolved_reference.startswith("subprocess.__getattribute__")
            ):
                errors.append("FORBIDDEN_SUBPROCESS_DYNAMIC_ACCESS")
            if (
                isinstance(node, ast.Name)
                and resolved_reference == "subprocess"
                and not isinstance(parent, ast.Attribute)
            ):
                errors.append("FORBIDDEN_SUBPROCESS_DYNAMIC_ACCESS")
            if isinstance(node, ast.Attribute) and (
                resolved_reference.startswith("os.__dict__")
                or resolved_reference.startswith("os.__getattribute__")
            ):
                errors.append("FORBIDDEN_OS_DYNAMIC_ACCESS")
            if (
                isinstance(node, ast.Name)
                and resolved_reference == "os"
                and not isinstance(parent, ast.Attribute)
            ):
                errors.append("FORBIDDEN_OS_DYNAMIC_ACCESS")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        resolved_call = qualified_name(node.func)
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in {"__import__", "eval", "exec", "getattr", "globals", "locals", "vars"}:
                errors.append("FORBIDDEN_DYNAMIC_CALL_" + name.upper())
            if resolved_call.endswith("runpy.run_path") or resolved_call.endswith("importlib.util.spec_from_file_location"):
                errors.append("FORBIDDEN_SOURCE_LOADER")
        elif isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            if attr in {"run_path", "spec_from_file_location"}:
                errors.append("FORBIDDEN_SOURCE_LOADER")
            if attr == "run":
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        errors.append("FORBIDDEN_SHELL_TRUE")
        if resolved_call == "subprocess.run":
            command = node.args[0] if node.args else None
            is_git = (
                isinstance(command, (ast.List, ast.Tuple))
                and bool(command.elts)
                and isinstance(command.elts[0], ast.Constant)
                and command.elts[0].value == "git"
            )
            if not is_git:
                errors.append("FORBIDDEN_NON_GIT_SUBPROCESS")
            elif command is None or not allowed_git_subprocess(node, command):
                errors.append("FORBIDDEN_GIT_SUBPROCESS_CALLSITE")
        elif resolved_call.startswith("subprocess."):
            errors.append("FORBIDDEN_SUBPROCESS_API")
        if resolved_call in {"git", "git_bytes"} and node.args:
            if all(isinstance(argument, ast.Constant) and isinstance(argument.value, str) for argument in node.args):
                literal_argv = tuple(argument.value for argument in node.args)
                if not read_only_git_argv(literal_argv):
                    errors.append("FORBIDDEN_GIT_HELPER_COMMAND")
            else:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    if first.value not in READ_ONLY_GIT_COMMANDS | {"branch", "symbolic-ref"}:
                        errors.append("FORBIDDEN_GIT_HELPER_COMMAND")
        if resolved_call in os_command_calls:
            errors.append("FORBIDDEN_OS_COMMAND")
        elif resolved_call.startswith("os.") and not (
            resolved_call == "os.replace" and allowed_os_replace(node)
        ):
            errors.append("FORBIDDEN_OS_API")
    return sorted(set(errors))


def record(checks: list[dict[str, Any]], code: str, passed: bool, observed: Any) -> None:
    checks.append({"code": code, "pass": bool(passed), "observed": observed})


def require_all(checks: list[dict[str, Any]], terminal: str) -> None:
    failed = [check["code"] for check in checks if not check["pass"]]
    if failed:
        print("FAIL " + " ".join(failed))
        print(f"FAIL_{terminal} {len(checks) - len(failed)}/{len(checks)}")
        raise SystemExit(1)


def cat_file_batch(shas: list[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(shas))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input=("\n".join(ordered) + "\n").encode("ascii"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=GIT_TIMEOUT, check=False,
    )
    if proc.returncode:
        raise ValidationError(proc.stderr.decode("utf-8", errors="replace"))
    out = proc.stdout
    pos = 0
    blobs: dict[str, bytes] = {}
    for requested in ordered:
        end = out.find(b"\n", pos)
        if end < 0:
            raise ValidationError("truncated git cat-file batch header")
        header = out[pos:end].decode("ascii").split()
        pos = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise ValidationError(f"invalid cat-file header for {requested}: {header}")
        size = int(header[2])
        data = out[pos:pos + size]
        pos += size
        if len(data) != size or out[pos:pos + 1] != b"\n":
            raise ValidationError(f"truncated cat-file body for {requested}")
        pos += 1
        blobs[requested] = data
    if pos != len(out):
        raise ValidationError("unexpected cat-file batch trailer")
    return blobs


def partition(path: str) -> str:
    root = "Claude/docs/v1.0.22/"
    rel = path[len(root):]
    if rel.startswith("plans/"):
        return "VERSION_PLAN"
    if rel.startswith("results/comp_"):
        return "COMPETING_REVIEW_CANDIDATE"
    if rel.startswith("results/"):
        return "STATUS_MACHINE_PROCESS"
    return "FINAL_RELEASE_SURFACE"


def manifest_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    manifest, traversal = strict_load(MANIFEST)
    normalized_sha = sha256(normalized_bytes(MANIFEST))
    record(checks, "MANIFEST_NORMALIZED_SHA", normalized_sha == EXPECTED_MANIFEST_SHA256, normalized_sha)
    record(checks, "MANIFEST_BASELINE", manifest.get("baseline_commit") == BASELINE, manifest.get("baseline_commit"))
    entries = manifest.get("entries", [])
    record(checks, "MANIFEST_FULL_ROWS", manifest.get("path_count") == len(entries) == 1520, len(entries))
    selected = [(index, row) for index, row in enumerate(entries, start=1) if row.get("version") == "v1.0.22"]
    indices = [index for index, _ in selected]
    rows = [row for _, row in selected]
    record(checks, "V1022_INDEX_RANGE", indices == list(range(540, 744)), [min(indices), max(indices), len(indices)])
    paths = [row.get("path") for row in rows]
    shas = [row.get("blob_sha") for row in rows]
    record(checks, "V1022_PATH_IDENTITY", len(paths) == len(set(paths)) == 204, len(set(paths)))
    record(checks, "V1022_BLOB_IDENTITY", len(shas) == len(set(shas)) == 204, len(set(shas)))

    tree_lines = git("ls-tree", "-r", "-l", BASELINE, "--", "Claude/docs/v1.0.22").splitlines()
    tree: dict[str, tuple[str, int]] = {}
    for line in tree_lines:
        left, path = line.split("\t", 1)
        mode, objtype, blob, size = left.split()
        if objtype == "blob":
            tree[path] = (blob, int(size))
    mismatch = [path for path, row in zip(paths, rows) if tree.get(path) != (row["blob_sha"], row["size_bytes"])]
    record(checks, "V1022_FROZEN_TREE_MATCH", not mismatch and set(tree) == set(paths), mismatch[:10])

    blobs = cat_file_batch(shas)
    text_lines = 0
    nonblank = 0
    pdf_pages: list[int] = []
    mode_counts: Counter[str] = Counter()
    partition_counts: Counter[str] = Counter()
    partition_bytes: Counter[str] = Counter()
    partition_lines: Counter[str] = Counter()
    partition_nonblank: Counter[str] = Counter()
    partition_pdf_pages: Counter[str] = Counter()
    extent_mismatch: list[str] = []
    for row in rows:
        data = blobs[row["blob_sha"]]
        part = partition(row["path"])
        mode = row["review_mode"]
        mode_counts[mode] += 1
        partition_counts[part] += 1
        partition_bytes[part] += len(data)
        if len(data) != row["size_bytes"]:
            extent_mismatch.append(row["path"] + ":bytes")
        if mode == "FULL_TEXT":
            lines = data.decode("utf-8").splitlines()
            line_count = len(lines)
            nonblank_count = sum(bool(line.strip()) for line in lines)
            text_lines += line_count
            nonblank += nonblank_count
            partition_lines[part] += line_count
            partition_nonblank[part] += nonblank_count
            if row["extent"].get("lines") != line_count:
                extent_mismatch.append(row["path"] + ":lines")
        elif mode == "FULL_PDF":
            try:
                pages = len(PdfReader(BytesIO(data), strict=True).pages)
            except Exception as exc:
                raise ValidationError(f"E_PDF_PAGE_PARSE: {row['path']}: {exc}") from exc
            pdf_pages.append(pages)
            partition_pdf_pages[part] += pages
            if row["extent"].get("pages") != pages:
                extent_mismatch.append(row["path"] + ":pages")
        else:
            extent_mismatch.append(row["path"] + ":mode")
    summary = {
        "manifest_traversal_nodes": traversal,
        "manifest_normalized_sha256": normalized_sha,
        "indices": [indices[0], indices[-1]],
        "path_occurrences": len(rows),
        "unique_paths": len(set(paths)),
        "unique_blobs": len(set(shas)),
        "bytes": sum(len(blobs[row["blob_sha"]]) for row in rows),
        "review_modes": dict(sorted(mode_counts.items())),
        "text_lines": text_lines,
        "nonblank_lines": nonblank,
        "pdf_pages": pdf_pages,
        "partition_counts": dict(sorted(partition_counts.items())),
        "partition_bytes": dict(sorted(partition_bytes.items())),
        "partition_lines": dict(sorted(partition_lines.items())),
        "partition_nonblank": dict(sorted(partition_nonblank.items())),
        "partition_pdf_pages": dict(sorted(partition_pdf_pages.items())),
    }
    expected = {
        "path_occurrences": 204, "unique_paths": 204, "unique_blobs": 204,
        "bytes": 4_974_148,
        "review_modes": {"FULL_PDF": 4, "FULL_TEXT": 200},
        "text_lines": 30_219, "nonblank_lines": 26_137,
        "pdf_pages": [8, 83, 25, 17],
        "partition_counts": {
            "COMPETING_REVIEW_CANDIDATE": 125, "FINAL_RELEASE_SURFACE": 63,
            "STATUS_MACHINE_PROCESS": 10, "VERSION_PLAN": 6,
        },
        "partition_bytes": {
            "COMPETING_REVIEW_CANDIDATE": 1_800_475, "FINAL_RELEASE_SURFACE": 2_985_072,
            "STATUS_MACHINE_PROCESS": 158_352, "VERSION_PLAN": 30_249,
        },
        "partition_lines": {
            "COMPETING_REVIEW_CANDIDATE": 17_072, "FINAL_RELEASE_SURFACE": 10_462,
            "STATUS_MACHINE_PROCESS": 2_398, "VERSION_PLAN": 287,
        },
        "partition_nonblank": {
            "COMPETING_REVIEW_CANDIDATE": 13_926, "FINAL_RELEASE_SURFACE": 9_733,
            "STATUS_MACHINE_PROCESS": 2_236, "VERSION_PLAN": 242,
        },
        "partition_pdf_pages": {"FINAL_RELEASE_SURFACE": 133},
    }
    for key, value in expected.items():
        record(checks, "V1022_" + key.upper(), summary[key] == value, summary[key])
    record(checks, "V1022_EXTENT_MATCH", not extent_mismatch, extent_mismatch[:10])
    return summary


def supplemental_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    blob = git("rev-parse", f"{BASELINE}:{SUPPLEMENTAL_PATH}")
    data = git_bytes("cat-file", "blob", blob)
    lines = data.decode("utf-8").splitlines()
    summary = {
        "path": SUPPLEMENTAL_PATH,
        "manifest_member": False,
        "blob_sha1": blob,
        "bytes": len(data),
        "lines": len(lines),
        "nonblank_lines": sum(bool(line.strip()) for line in lines),
        "sha256": sha256(data),
    }
    expected = {"manifest_member": False, "blob_sha1": SUPPLEMENTAL_BLOB, "bytes": 16_115, "lines": 99, "nonblank_lines": 79}
    for key, value in expected.items():
        record(checks, "SUPPLEMENTAL_" + key.upper(), summary[key] == value, summary[key])
    manifest, _ = strict_load(MANIFEST)
    member = any(row.get("path") == SUPPLEMENTAL_PATH for row in manifest.get("entries", []))
    record(checks, "SUPPLEMENTAL_DENOMINATOR_SEPARATE", not member, member)
    return summary


def intent_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    docs: list[dict[str, Any]] = []
    for rel, expected_lines, expected_sha in OBSERVATIONS:
        path = REPO / rel
        data = path.read_bytes()
        observed = {"path": rel, "lines": len(data.decode("utf-8").splitlines()), "sha256": sha256(data)}
        record(checks, "OBS_" + Path(rel).name.split("_")[1] + "_LINES", observed["lines"] == expected_lines, observed["lines"])
        record(checks, "OBS_" + Path(rel).name.split("_")[1] + "_SHA", observed["sha256"] == expected_sha, observed["sha256"])
        docs.append(observed)
    ledger, traversal = strict_load(INTENT)
    records = [row for row in ledger.get("records", []) if 96 <= row.get("numeric_id", -1) <= 191]
    ids = [row.get("claim_id") for row in records]
    referenced = dict(sorted(Counter(row.get("referenced_actor") for row in records).items()))
    confidence = dict(sorted(Counter(row.get("actor_confidence") for row in records).items()))
    full_row_sha = sha256(canonical_bytes(records)[:-1])
    record(checks, "INTENT_96_COUNT", len(records) == 96, len(records))
    record(checks, "INTENT_96_SEQUENCE", ids == [f"INTENT-PROV-{number:04d}" for number in range(96, 192)], [ids[:1], ids[-1:]])
    record(checks, "INTENT_ACTORS", referenced == {"IMPLEMENTED_STATE": 8, "MODEL_PROPOSAL": 10, "REVIEW_FINDING": 72, "USER_REQUIREMENT": 6}, referenced)
    record(checks, "INTENT_CONFIDENCE", confidence == {"DIRECT_REAUDIT_FINDING": 72, "EXPLICIT_MODEL_OR_PLAN_ATTRIBUTION": 10, "PATCH_CONFIRMATION_REQUIRED": 8, "REPOSITORY_REPORTED": 6}, confidence)
    record(checks, "INTENT_FULL_ROW_SHA", full_row_sha == EXPECTED_INTENT96_SHA256, full_row_sha)
    return {
        "observation_documents": docs,
        "observation_document_count": len(docs),
        "observation_physical_lines": sum(row["lines"] for row in docs),
        "prior_review_documents": 101,
        "prior_review_physical_lines": 16_855,
        "finding_count": len(records),
        "finding_range": [ids[0], ids[-1]],
        "full_row_canonical_sha256": full_row_sha,
        "referenced_actor_counts": referenced,
        "confidence_counts": confidence,
        "ledger_traversal_nodes": traversal,
    }


def plan_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    data = normalized_bytes(PLAN)
    text = data.decode("utf-8")
    digest = sha256(data)
    lines = text.splitlines()
    record(checks, "PLAN_NORMALIZED_SHA", digest == EXPECTED_PLAN_SHA256, digest)
    record(checks, "PLAN_LINE_COUNT", len(lines) == 681, len(lines))
    headings = [
        "## Summary", "## Current Ground Truth", "## Phase Range", "## Exact Read Inputs",
        "## Non-goals and Scope Guards", "## Implementation Changes", "## Phase Gate",
        "## Implementation Interfaces", "## Test and Validation Plan", "## Stop Conditions",
        "## Assumptions", "## Correction History",
    ]
    for heading in headings:
        record(checks, "PLAN_HEADING_" + hashlib.sha1(heading.encode()).hexdigest()[:8], heading in text, heading)
    tokens = [
        "누적 Step 범위: 58–63", "Step 58", "Step 59", "Step 60", "Step 61", "Step 62",
        "Step 63.1", "Step 63.2", "PASS_P063_PLAN_ACTIVATION", "PASS_P063_LINEAGE_F",
        "CONDITIONAL_P063", "FAIL_P063", "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "PASS_P063_PLAN_ACTIVATION_PERSISTENCE", EXPECTED_PARENT, EXPECTED_SUBJECT,
        "204 manifest occurrences + 1 supplemental process-control occurrence",
        "63/6/10/125", "30,219/26,137", "4/133", "INTENT-PROV-0096", "INTENT-PROV-0191",
        "External scientific/material/experimental/primary-literature truth",
        "# Phase 063 v1.0.22 Lineage Reaudit Implementation Plan", "Result-first", "JSON-last",
    ] + EXACT_SEVEN
    for token in tokens:
        record(checks, "PLAN_TOKEN_" + hashlib.sha1(token.encode()).hexdigest()[:8], token in text, token)
    step_positions = [text.index(f"### Step {step}") for step in ["58", "59", "60", "61", "62", "63.1", "63.2"]]
    record(checks, "PLAN_CUMULATIVE_STEP_ORDER", step_positions == sorted(step_positions) and len(set(step_positions)) == 7, step_positions)
    record(checks, "PLAN_NO_PHASE_STEP_RESET", "Phase 063 — Step 1" not in text and "### Step 1 " not in text, True)
    return {"path": PLAN.relative_to(REPO).as_posix(), "lines": len(lines), "bytes": len(data), "normalized_sha256": digest, "required_headings": len(headings), "required_tokens": len(tokens)}


def control_semantic_errors(result: str, active: str, parent: str, handover: str) -> list[str]:
    errors: list[str] = []
    result_gate_lines = [line for line in result.splitlines() if line.startswith("Gate:")]
    if result_gate_lines != ["Gate: `PASS_P063_PLAN_ACTIVATION`"]:
        errors.append("RESULT_GATE_SINGLETON")
    if result.splitlines().count("Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`") != 1:
        errors.append("RESULT_COMMIT_SINGLETON")
    if result.splitlines().count("Postcommit persistence: `PENDING`") != 1:
        errors.append("RESULT_PERSISTENCE_SINGLETON")
    active_rows = [line for line in active.splitlines() if line.startswith("| 063 |")]
    if len(active_rows) != 1 or not all(token in active_rows[0] for token in [
        "IN_PROGRESS", "PASS_P063_PLAN_ACTIVATION", "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "PASS_P063_PLAN_ACTIVATION_PERSISTENCE", "then Step 58",
    ]):
        errors.append("ACTIVE_PHASE063_ROW_SINGLETON")
    if re.search(r"(?im)^.*Phase 063.*\b(?:FAIL|BLOCKED|CONDITIONAL)(?:\b|_)", active):
        errors.append("ACTIVE_PHASE063_CONTRADICTION")
    parent_rows = [line for line in parent.splitlines() if line.startswith("| 063 |")]
    if len(parent_rows) != 1 or not all(token in parent_rows[0] for token in [
        "IN_PROGRESS", "PASS_P063_PLAN_ACTIVATION", "PENDING_AT_PRECOMMIT_BY_DESIGN",
        EXPECTED_SUBJECT, "then Step 58",
    ]):
        errors.append("PARENT_PHASE063_ROW_SINGLETON")
    if re.search(r"(?im)^.*Phase 063.*\b(?:FAIL|BLOCKED|CONDITIONAL)(?:\b|_)", parent):
        errors.append("PARENT_PHASE063_CONTRADICTION")
    required_handover = [
        "현재 Phase 상태: Phase 063 `IN_PROGRESS`, Current checkpoint: plan activation precommit `PASS_P063_PLAN_ACTIVATION`",
        "exact-seven containing commit `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "Only after `PASS_P063_PLAN_ACTIVATION_PERSISTENCE` may Step 58 begin.",
    ]
    if not all(handover.count(token) == 1 for token in required_handover):
        errors.append("HANDOVER_PHASE063_SINGLETON")
    if re.search(r"(?i)Step 58 may begin before persistence", handover):
        errors.append("HANDOVER_STEP58_BARRIER")
    return errors


def control_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    result = RESULT.read_text(encoding="utf-8")
    active = ACTIVE_LEDGER.read_text(encoding="utf-8")
    parent = PARENT_LEDGER.read_text(encoding="utf-8")
    handover = HANDOVER.read_text(encoding="utf-8")
    result_tokens = ["PASS_P063_PLAN_ACTIVATION", "PENDING_AT_PRECOMMIT_BY_DESIGN", EXPECTED_PARENT, EXPECTED_SUBJECT, "204 manifest occurrences + 1 supplemental process-control occurrence", "FAIL E_VALIDATION_ARTIFACT_MISSING"]
    for token in result_tokens:
        record(checks, "RESULT_TOKEN_" + hashlib.sha1(token.encode()).hexdigest()[:8], token in result, token)
    for name, text in [("ACTIVE", active), ("PARENT", parent), ("HANDOVER", handover)]:
        for token in ["Phase 063", "PASS_P063_PLAN_ACTIVATION", "PENDING_AT_PRECOMMIT_BY_DESIGN", EXPECTED_SUBJECT]:
            record(checks, f"{name}_TOKEN_" + hashlib.sha1(token.encode()).hexdigest()[:8], token in text, token)
    record(checks, "CONTROL_PHASE062_ACTUAL_COMMIT_ACTIVE", EXPECTED_PARENT in active and "PASS_P062_STEP57_2_PERSISTENCE" in active, True)
    record(checks, "CONTROL_PHASE062_ACTUAL_COMMIT_PARENT", EXPECTED_PARENT in parent and "PASS_P062_STEP57_2_PERSISTENCE" in parent, True)
    record(checks, "CONTROL_PHASE062_ACTUAL_COMMIT_HANDOVER", EXPECTED_PARENT in handover and "PASS_P062_STEP57_2_PERSISTENCE" in handover, True)
    hashes = {
        "result_sha256": sha256(normalized_bytes(RESULT)),
        "active_ledger_sha256": sha256(normalized_bytes(ACTIVE_LEDGER)),
        "parent_ledger_sha256": sha256(normalized_bytes(PARENT_LEDGER)),
        "handover_sha256": sha256(normalized_bytes(HANDOVER)),
    }
    for key, expected in EXPECTED_CONTROL_SHA256.items():
        observed = hashes[key + "_sha256"]
        record(checks, "CONTROL_PIN_" + key.upper(), observed == expected, observed)
    semantic_errors = control_semantic_errors(result, active, parent, handover)
    record(checks, "CONTROL_SEMANTIC_CONTRACT", not semantic_errors, semantic_errors)
    return hashes


def predecessor_expected_snapshot() -> dict[str, Any]:
    return {
        "head": EXPECTED_PARENT,
        "head_symbolic": f"refs/heads/{ACTIVE_BRANCH}",
        "branch": ACTIVE_BRANCH,
        "parent": EXPECTED_PARENT_PARENT,
        "subject": EXPECTED_PARENT_SUBJECT,
        "upstream_ref": f"refs/remotes/origin/{ACTIVE_BRANCH}",
        "upstream": EXPECTED_PARENT,
        "active_local": EXPECTED_PARENT,
        "active_tracking": EXPECTED_PARENT,
        "active_live": EXPECTED_PARENT,
        "protected_local": EXPECTED_PROTECTED,
        "protected_tracking": EXPECTED_PROTECTED,
        "protected_live": EXPECTED_PROTECTED,
        "main_local": None,
        "main_tracking": EXPECTED_MAIN,
        "main_live": EXPECTED_MAIN,
        "claude_tracked_diff": "",
        "claude_untracked": "",
    }


def current_predecessor_snapshot() -> dict[str, Any]:
    return {
        "head": git("rev-parse", "HEAD"),
        "head_symbolic": git("symbolic-ref", "-q", "HEAD"),
        "branch": git("branch", "--show-current"),
        "parent": git("rev-parse", f"{EXPECTED_PARENT}^"),
        "subject": git("show", "-s", "--format=%s", EXPECTED_PARENT),
        "upstream_ref": git("rev-parse", "--symbolic-full-name", "@{upstream}"),
        "upstream": git("rev-parse", "@{upstream}"),
        "active_local": ref_hash_or_none(f"refs/heads/{ACTIVE_BRANCH}"),
        "active_tracking": ref_hash_or_none(f"refs/remotes/origin/{ACTIVE_BRANCH}"),
        "active_live": ls_remote_head(f"refs/heads/{ACTIVE_BRANCH}"),
        "protected_local": ref_hash_or_none(f"refs/heads/{PROTECTED_BRANCH}"),
        "protected_tracking": ref_hash_or_none(f"refs/remotes/origin/{PROTECTED_BRANCH}"),
        "protected_live": ls_remote_head(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_local": ref_hash_or_none("refs/heads/main"),
        "main_tracking": ref_hash_or_none("refs/remotes/origin/main"),
        "main_live": ls_remote_head("refs/heads/main"),
        "claude_tracked_diff": git("diff", "--name-only", EXPECTED_PARENT, "--", "Claude"),
        "claude_untracked": git("ls-files", "--others", "--exclude-standard", "--", "Claude"),
    }


def predecessor_snapshot_errors(snapshot: dict[str, Any]) -> list[str]:
    expected = predecessor_expected_snapshot()
    return ["GIT_PREDECESSOR_" + key.upper() for key, value in expected.items() if snapshot.get(key) != value]


def predecessor_contract(checks: list[dict[str, Any]], *, live: bool) -> dict[str, Any]:
    values = current_predecessor_snapshot() if live else predecessor_expected_snapshot()
    for key, value in predecessor_expected_snapshot().items():
        record(checks, "GIT_PREDECESSOR_" + key.upper(), values.get(key) == value, values.get(key))
    return values


def nonself_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    missing = [rel for rel in NONSELF if not (REPO / rel).is_file()]
    record(checks, "NONSELF_SURFACES_PRESENT", not missing, missing)
    hashes = {rel: sha256(normalized_bytes(REPO / rel)) for rel in NONSELF if (REPO / rel).is_file()}
    return {"result_first": True, "validation_written_last": True, "nonself_normalized_lf_sha256": hashes}


def build_payload(predecessor_mode: str = "live") -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    plan = plan_contract(checks)
    manifest = manifest_contract(checks)
    supplemental = supplemental_contract(checks)
    intent = intent_contract(checks)
    controls = control_contract(checks)
    nonself = nonself_contract(checks)
    if predecessor_mode not in {"live", "golden"}:
        raise ValueError(f"invalid predecessor mode: {predecessor_mode}")
    predecessor = predecessor_contract(checks, live=predecessor_mode == "live")
    script_text = SCRIPT.read_text(encoding="utf-8")
    forbidden = source_policy_errors(script_text)
    record(checks, "VALIDATOR_SOURCE_POLICY", not forbidden, forbidden)
    record(checks, "EXACT_ALLOWLIST_UNIQUE", len(EXACT_SEVEN) == len(EXACT_SEVEN_SET) == 7, EXACT_SEVEN)
    payload = {
        "schema_version": "1.0",
        "phase": 63,
        "unit": "plan_activation",
        "gate": "PASS_P063_PLAN_ACTIVATION",
        "status": "PASS",
        "date": "2026-08-28",
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "active_branch": ACTIVE_BRANCH,
        "protected_branch": {"name": PROTECTED_BRANCH, "fixed_tip": EXPECTED_PROTECTED},
        "main_fixed_tip": EXPECTED_MAIN,
        "baseline_commit": BASELINE,
        "exact_allowlist": EXACT_SEVEN,
        "plan_contract": plan,
        "manifest_contract": manifest,
        "supplemental_contract": supplemental,
        "intent_contract": intent,
        "control_contract": controls,
        "predecessor_snapshot": predecessor,
        "output_contract": nonself,
        "authority_boundary": {
            "internal_plan_and_inventory_only": True,
            "external_scientific_truth_promoted": False,
            "external_material_truth_promoted": False,
            "external_experimental_truth_promoted": False,
            "primary_literature_truth_promoted": False,
            "canonical_selection_promoted": False,
        },
        "checks": checks,
    }
    return payload, checks


def payload_contract_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def expect(route: tuple[str, ...], expected: Any, code: str) -> None:
        current: Any = value
        try:
            for key in route:
                current = current[key]
        except (KeyError, TypeError):
            errors.append(code + "_MISSING")
            return
        if current != expected:
            errors.append(code)

    expect(("schema_version",), "1.0", "SCHEMA")
    expect(("phase",), 63, "PHASE")
    expect(("unit",), "plan_activation", "UNIT")
    expect(("gate",), "PASS_P063_PLAN_ACTIVATION", "GATE")
    expect(("status",), "PASS", "STATUS")
    expect(("expected_parent",), EXPECTED_PARENT, "PARENT")
    expect(("expected_subject",), EXPECTED_SUBJECT, "SUBJECT")
    expect(("active_branch",), ACTIVE_BRANCH, "BRANCH")
    expect(("baseline_commit",), BASELINE, "BASELINE")
    expect(("exact_allowlist",), EXACT_SEVEN, "ALLOWLIST")
    expect(("plan_contract", "normalized_sha256"), EXPECTED_PLAN_SHA256, "PLAN_SHA")
    expect(("plan_contract", "lines"), 681, "PLAN_LINES")
    expect(("manifest_contract", "path_occurrences"), 204, "MANIFEST_COUNT")
    expect(("manifest_contract", "unique_paths"), 204, "MANIFEST_PATHS")
    expect(("manifest_contract", "unique_blobs"), 204, "MANIFEST_BLOBS")
    expect(("manifest_contract", "bytes"), 4_974_148, "MANIFEST_BYTES")
    expect(("manifest_contract", "review_modes"), {"FULL_PDF": 4, "FULL_TEXT": 200}, "REVIEW_MODES")
    expect(("manifest_contract", "text_lines"), 30_219, "TEXT_LINES")
    expect(("manifest_contract", "nonblank_lines"), 26_137, "NONBLANK_LINES")
    expect(("manifest_contract", "pdf_pages"), [8, 83, 25, 17], "PDF_PAGES")
    expect(("manifest_contract", "partition_counts"), {
        "COMPETING_REVIEW_CANDIDATE": 125, "FINAL_RELEASE_SURFACE": 63,
        "STATUS_MACHINE_PROCESS": 10, "VERSION_PLAN": 6,
    }, "PARTITIONS")
    expect(("supplemental_contract", "manifest_member"), False, "SUPPLEMENTAL_SEPARATION")
    expect(("supplemental_contract", "blob_sha1"), SUPPLEMENTAL_BLOB, "SUPPLEMENTAL_BLOB")
    expect(("supplemental_contract", "bytes"), 16_115, "SUPPLEMENTAL_BYTES")
    expect(("supplemental_contract", "lines"), 99, "SUPPLEMENTAL_LINES")
    expect(("intent_contract", "finding_count"), 96, "FINDING_COUNT")
    expect(("intent_contract", "finding_range"), ["INTENT-PROV-0096", "INTENT-PROV-0191"], "FINDING_RANGE")
    expect(("intent_contract", "full_row_canonical_sha256"), EXPECTED_INTENT96_SHA256, "FINDING_FULL_ROW_SHA")
    expect(("intent_contract", "observation_document_count"), 11, "OBSERVATION_COUNT")
    expect(("intent_contract", "observation_physical_lines"), 2_363, "OBSERVATION_LINES")
    expect(("output_contract", "result_first"), True, "RESULT_FIRST")
    expect(("output_contract", "validation_written_last"), True, "JSON_LAST")
    for key in [
        "external_scientific_truth_promoted", "external_material_truth_promoted",
        "external_experimental_truth_promoted", "primary_literature_truth_promoted",
        "canonical_selection_promoted",
    ]:
        expect(("authority_boundary", key), False, "AUTHORITY_" + key.upper())
    checks = value.get("checks")
    if not isinstance(checks, list) or not checks or not all(isinstance(row, dict) and row.get("pass") is True for row in checks):
        errors.append("CHECKS_NOT_ALL_PASS")
    hashes = value.get("output_contract", {}).get("nonself_normalized_lf_sha256")
    if not isinstance(hashes, dict) or set(hashes) != set(NONSELF):
        errors.append("NONSELF_HASH_MEMBERSHIP")
    return errors


def negative_controls(payload: dict[str, Any]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []

    def add(name: str, actual: list[str], expected: list[str]) -> None:
        controls.append({
            "name": name,
            "rejected": actual == expected,
            "diagnostics": actual,
            "expected_diagnostics": expected,
        })

    for name, raw, expected, message_fragment in [
        ("duplicate_key", '{"a":1,"a":2}', "STRICT_DUPLICATE_KEY", "duplicate JSON key"),
        ("nonfinite_nan", '{"a":NaN}', "STRICT_NONFINITE_CONSTANT", "non-finite JSON constant"),
        ("nonfinite_infinity", '{"a":Infinity}', "STRICT_NONFINITE_CONSTANT", "non-finite JSON constant"),
        ("positive_overflow", '{"a":1e9999}', "STRICT_NONFINITE_NUMBER", "non-finite JSON number"),
        ("negative_overflow", '{"a":-1e9999}', "STRICT_NONFINITE_NUMBER", "non-finite JSON number"),
        ("truncated_json", '{"a":', "STRICT_TRUNCATED_JSON", "Expecting value"),
    ]:
        diagnostic: list[str] = []
        try:
            value = json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=reject_constant)
            traverse(value)
        except (ValueError, json.JSONDecodeError) as exc:
            if message_fragment in str(exc):
                diagnostic = [expected]
            else:
                diagnostic = ["UNEXPECTED_STRICT_DIAGNOSTIC:" + str(exc)]
        add(name, diagnostic, [expected])

    mutations = [
        ("manifest_count", ("manifest_contract", "path_occurrences"), 203, "MANIFEST_COUNT"),
        ("manifest_bytes", ("manifest_contract", "bytes"), 4_974_147, "MANIFEST_BYTES"),
        ("partition_count", ("manifest_contract", "partition_counts"), {}, "PARTITIONS"),
        ("supplemental_fusion", ("supplemental_contract", "manifest_member"), True, "SUPPLEMENTAL_SEPARATION"),
        ("finding_count", ("intent_contract", "finding_count"), 95, "FINDING_COUNT"),
        ("finding_range", ("intent_contract", "finding_range"), ["INTENT-PROV-0096", "INTENT-PROV-0190"], "FINDING_RANGE"),
        ("finding_full_row_sha", ("intent_contract", "full_row_canonical_sha256"), "0" * 64, "FINDING_FULL_ROW_SHA"),
        ("plan_sha", ("plan_contract", "normalized_sha256"), "0" * 64, "PLAN_SHA"),
        ("allowlist_duplicate", ("exact_allowlist",), EXACT_SEVEN[:-1] + [EXACT_SEVEN[-2]], "ALLOWLIST"),
        ("external_science_promotion", ("authority_boundary", "external_scientific_truth_promoted"), True, "AUTHORITY_EXTERNAL_SCIENTIFIC_TRUTH_PROMOTED"),
        ("external_material_promotion", ("authority_boundary", "external_material_truth_promoted"), True, "AUTHORITY_EXTERNAL_MATERIAL_TRUTH_PROMOTED"),
        ("canonical_promotion", ("authority_boundary", "canonical_selection_promoted"), True, "AUTHORITY_CANONICAL_SELECTION_PROMOTED"),
        ("result_first_false", ("output_contract", "result_first"), False, "RESULT_FIRST"),
    ]
    for name, route, value, expected in mutations:
        altered = copy.deepcopy(payload)
        target: Any = altered
        for key in route[:-1]:
            target = target[key]
        target[route[-1]] = value
        add(name, payload_contract_errors(altered), [expected])

    source_fixtures = [
        ("source_alias_runpy", "import runpy as rp\nrp.run_path('Claude/x.py')\n", ["FORBIDDEN_IMPORT_RUNPY", "FORBIDDEN_SOURCE_LOADER"]),
        ("source_dynamic_import", "__import__('Claude.evil')\n", ["FORBIDDEN_DYNAMIC_CALL___IMPORT__"]),
        ("source_getattr_loader", "getattr(__import__('subprocess'), 'run')(['Claude/x.py'])\n", ["FORBIDDEN_DYNAMIC_CALL_GETATTR", "FORBIDDEN_DYNAMIC_CALL___IMPORT__"]),
        ("source_shell_true", "import subprocess\nsubprocess.run(['x'], shell=True)\n", ["FORBIDDEN_NON_GIT_SUBPROCESS", "FORBIDDEN_SHELL_TRUE"]),
        ("source_direct_production", "import subprocess\nsubprocess.run(['py', 'Claude/x.py'])\n", ["FORBIDDEN_NON_GIT_SUBPROCESS"]),
        ("source_alias_production", "from subprocess import run as execute\nexecute(['py', 'Claude/x.py'])\n", ["FORBIDDEN_NON_GIT_SUBPROCESS"]),
        ("source_assigned_production", "import subprocess\nexecute = subprocess.run\nexecute(['py', 'Claude/x.py'])\n", ["FORBIDDEN_NON_GIT_SUBPROCESS", "FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE"]),
        ("source_namedexpr_callable", "import subprocess\n(execute := subprocess.run)(['py', 'Claude/x.py'])\n", ["FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE"]),
        ("source_tuple_assigned_callable", "import subprocess\n(execute,) = (subprocess.run,)\nexecute(['py', 'Claude/x.py'])\n", ["FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE"]),
        ("source_default_arg_callable", "import subprocess\ndef f(execute=subprocess.run):\n    execute(['py', 'Claude/x.py'])\nf()\n", ["FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE"]),
        ("source_subprocess_dict", "import subprocess\nsubprocess.__dict__['run'](['py', 'Claude/x.py'])\n", ["FORBIDDEN_SUBPROCESS_DYNAMIC_ACCESS"]),
        ("source_list_index_callable", "import subprocess\n[subprocess.run][0](['py', 'Claude/x.py'])\n", ["FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE"]),
        ("source_conditional_callable", "import subprocess\n(subprocess.run if True else subprocess.call)(['py', 'Claude/x.py'])\n", ["FORBIDDEN_SUBPROCESS_CALLABLE_REFERENCE"]),
        ("source_subprocess_getoutput", "import subprocess\nsubprocess.getoutput('py Claude/x.py')\n", ["FORBIDDEN_SUBPROCESS_API"]),
        ("source_subprocess_getstatusoutput", "import subprocess\nsubprocess.getstatusoutput('py Claude/x.py')\n", ["FORBIDDEN_SUBPROCESS_API"]),
        ("source_os_system", "import os\nos.system('py Claude/x.py')\n", ["FORBIDDEN_OS_COMMAND"]),
        ("source_os_execv", "import os\nimport sys\nos.execv(sys.executable, [sys.executable, 'Claude/x.py'])\n", ["FORBIDDEN_IMPORT_SYS", "FORBIDDEN_OS_API"]),
        ("source_os_startfile", "import os\nos.startfile('Claude/x.py')\n", ["FORBIDDEN_OS_API"]),
        ("source_asyncio_subprocess", "import asyncio\nasyncio.run(asyncio.create_subprocess_exec('py', 'Claude/x.py'))\n", ["FORBIDDEN_IMPORT_ASYNCIO"]),
        ("source_git_wrong_callsite", "import subprocess\nsubprocess.run(['git', 'status'])\n", ["FORBIDDEN_GIT_SUBPROCESS_CALLSITE"]),
        ("source_git_helper_reset", "git('reset', '--hard')\n", ["FORBIDDEN_GIT_HELPER_COMMAND"]),
        ("source_git_bytes_helper_reset", "git_bytes('checkout', '--', 'Claude/x.py')\n", ["FORBIDDEN_GIT_HELPER_COMMAND"]),
        ("source_git_helper_output_eq", "git('diff', '--output=Claude/evil', 'HEAD')\n", ["FORBIDDEN_GIT_HELPER_COMMAND"]),
        ("source_git_bytes_helper_output_split", "git_bytes('show', '--output', 'Claude/evil', 'HEAD')\n", ["FORBIDDEN_GIT_HELPER_COMMAND"]),
        ("source_shadow_git_definition", "import subprocess\ndef git(*args):\n    subprocess.run(['git', *args])\nargv = ('reset', '--hard')\ngit(*argv)\n", ["FORBIDDEN_GIT_HELPER_DEFINITION"]),
        ("source_shadow_git_bytes_definition", "import subprocess\ndef git_bytes(*args):\n    subprocess.run(['git', *args])\nargv = ('checkout', '--', 'Claude/x.py')\ngit_bytes(*argv)\n", ["FORBIDDEN_GIT_HELPER_DEFINITION"]),
        ("source_nested_shadow_git_definition", "import subprocess\ndef outer():\n    def git(*args):\n        subprocess.run(['git', *args])\n    argv = ('branch', '-D', 'main')\n    git(*argv)\nouter()\n", ["FORBIDDEN_GIT_HELPER_DEFINITION"]),
        ("source_git_assignment_shadow", "git = object()\n", ["FORBIDDEN_GIT_HELPER_BINDING"]),
    ]
    for name, source, expected in source_fixtures:
        add(name, source_policy_errors(source), expected)

    control_texts = {
        "result": RESULT.read_text(encoding="utf-8"),
        "active": ACTIVE_LEDGER.read_text(encoding="utf-8"),
        "parent": PARENT_LEDGER.read_text(encoding="utf-8"),
        "handover": HANDOVER.read_text(encoding="utf-8"),
    }
    control_fixtures = [
        ("control_result_fail_gate", "result", "\nGate: FAIL_P063\n", "RESULT_GATE_SINGLETON"),
        ("control_active_fail", "active", "\nPhase 063 current status: FAIL\n", "ACTIVE_PHASE063_CONTRADICTION"),
        ("control_parent_conditional", "parent", "\nPhase 063 gate: CONDITIONAL_P063\n", "PARENT_PHASE063_CONTRADICTION"),
        ("control_handover_early_step58", "handover", "\nStep 58 may begin before persistence\n", "HANDOVER_STEP58_BARRIER"),
    ]
    for name, target_name, suffix, expected in control_fixtures:
        altered = dict(control_texts)
        altered[target_name] += suffix
        actual = control_semantic_errors(altered["result"], altered["active"], altered["parent"], altered["handover"])
        add(name, actual, [expected])

    git_mutations = [
        ("git_head", "head", "0" * 40, "GIT_PREDECESSOR_HEAD"),
        ("git_head_symbolic", "head_symbolic", "refs/heads/wrong", "GIT_PREDECESSOR_HEAD_SYMBOLIC"),
        ("git_branch", "branch", "wrong", "GIT_PREDECESSOR_BRANCH"),
        ("git_parent", "parent", "0" * 40, "GIT_PREDECESSOR_PARENT"),
        ("git_subject", "subject", "wrong", "GIT_PREDECESSOR_SUBJECT"),
        ("git_upstream_ref", "upstream_ref", "refs/remotes/origin/wrong", "GIT_PREDECESSOR_UPSTREAM_REF"),
        ("git_upstream", "upstream", "0" * 40, "GIT_PREDECESSOR_UPSTREAM"),
        ("git_active_local", "active_local", "0" * 40, "GIT_PREDECESSOR_ACTIVE_LOCAL"),
        ("git_active_tracking", "active_tracking", "0" * 40, "GIT_PREDECESSOR_ACTIVE_TRACKING"),
        ("git_active_live", "active_live", "0" * 40, "GIT_PREDECESSOR_ACTIVE_LIVE"),
        ("git_protected_local", "protected_local", "0" * 40, "GIT_PREDECESSOR_PROTECTED_LOCAL"),
        ("git_protected_tracking", "protected_tracking", "0" * 40, "GIT_PREDECESSOR_PROTECTED_TRACKING"),
        ("git_protected_live", "protected_live", "0" * 40, "GIT_PREDECESSOR_PROTECTED_LIVE"),
        ("git_main_local", "main_local", "0" * 40, "GIT_PREDECESSOR_MAIN_LOCAL"),
        ("git_main_tracking", "main_tracking", "0" * 40, "GIT_PREDECESSOR_MAIN_TRACKING"),
        ("git_main_live", "main_live", "0" * 40, "GIT_PREDECESSOR_MAIN_LIVE"),
        ("git_claude_diff", "claude_tracked_diff", "Claude/evil", "GIT_PREDECESSOR_CLAUDE_TRACKED_DIFF"),
        ("git_claude_untracked", "claude_untracked", "Claude/evil", "GIT_PREDECESSOR_CLAUDE_UNTRACKED"),
    ]
    for name, key, value, expected in git_mutations:
        altered = predecessor_expected_snapshot()
        altered[key] = value
        add(name, predecessor_snapshot_errors(altered), [expected])
    return controls


def write_output(payload: dict[str, Any], fresh_second: dict[str, Any]) -> None:
    output = copy.deepcopy(payload)
    controls = negative_controls(payload)
    output["negative_controls"] = controls
    output["negative_control_summary"] = {"passed": sum(row["rejected"] for row in controls), "total": len(controls)}
    projection_a = canonical_bytes(payload)
    projection_b = canonical_bytes(fresh_second)
    output["determinism"] = {
        "runs": 2, "mode": "TWO_FRESH_RECONSTRUCTIONS", "byte_identical": projection_a == projection_b,
        "semantic_sha256": sha256(projection_a),
    }
    output["validation_summary"] = {
        "passed": sum(check["pass"] for check in payload["checks"]),
        "total": len(payload["checks"]),
        "all_passed": all(check["pass"] for check in payload["checks"]),
    }
    temp = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
    temp.write_bytes(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    os.replace(temp, OUTPUT)


def verify_stored(checks: list[dict[str, Any]]) -> dict[str, Any]:
    stored, nodes = strict_load(OUTPUT)
    expected_core, _ = build_payload(predecessor_mode="golden")
    extra_keys = {"negative_controls", "negative_control_summary", "determinism", "validation_summary"}
    expected_top_keys = set(expected_core) | extra_keys
    record(checks, "STORED_TOP_SCHEMA", set(stored) == expected_top_keys, sorted(set(stored) ^ expected_top_keys))
    stored_core = {key: stored.get(key) for key in expected_core}
    record(checks, "STORED_FULL_GOLDEN", canonical_bytes(stored_core) == canonical_bytes(expected_core), sha256(canonical_bytes(stored_core)))
    semantic_errors = payload_contract_errors(stored)
    record(checks, "STORED_SEMANTIC_CONTRACT", not semantic_errors, semantic_errors)
    record(checks, "STORED_SCHEMA", stored.get("schema_version") == "1.0", stored.get("schema_version"))
    record(checks, "STORED_GATE", stored.get("gate") == "PASS_P063_PLAN_ACTIVATION", stored.get("gate"))
    record(checks, "STORED_STATUS", stored.get("status") == "PASS", stored.get("status"))
    record(checks, "STORED_ALLOWLIST", stored.get("exact_allowlist") == EXACT_SEVEN, stored.get("exact_allowlist"))
    current_hashes = {rel: sha256(normalized_bytes(REPO / rel)) for rel in NONSELF}
    record(checks, "STORED_NONSELF_HASHES", stored.get("output_contract", {}).get("nonself_normalized_lf_sha256") == current_hashes, current_hashes)
    neg = stored.get("negative_controls", [])
    expected_neg = negative_controls(expected_core)
    record(checks, "STORED_NEGATIVE_CONTROLS", neg == expected_neg and all(row.get("rejected") is True for row in neg), [len(neg), sum(bool(row.get("rejected")) for row in neg)])
    det = stored.get("determinism", {})
    expected_det = {"runs": 2, "mode": "TWO_FRESH_RECONSTRUCTIONS", "byte_identical": True, "semantic_sha256": sha256(canonical_bytes(expected_core))}
    record(checks, "STORED_DETERMINISM", det == expected_det, det)
    expected_summary = {"passed": len(expected_core["checks"]), "total": len(expected_core["checks"]), "all_passed": True}
    record(checks, "STORED_VALIDATION_ALL_PASS", stored.get("validation_summary") == expected_summary, stored.get("validation_summary"))
    expected_neg_summary = {"passed": len(expected_neg), "total": len(expected_neg)}
    record(checks, "STORED_NEGATIVE_SUMMARY", stored.get("negative_control_summary") == expected_neg_summary, stored.get("negative_control_summary"))
    return {"traversal_nodes": nodes, "sha256": sha256(OUTPUT.read_bytes())}


def git_paths(*args: str) -> set[str]:
    raw = git_bytes(*args)
    return {item.decode("utf-8").replace("\\", "/") for item in raw.split(b"\0") if item}


def changed_paths() -> set[str]:
    tracked = git_paths("diff", "HEAD", "--name-only", "-z")
    untracked = git_paths("ls-files", "--others", "--exclude-standard", "-z")
    return tracked | untracked


def verify_staged() -> None:
    checks: list[dict[str, Any]] = []
    predecessor_contract(checks, live=True)
    verify_stored(checks)
    staged = git_paths("diff", "--cached", "--name-only", "-z")
    record(checks, "STAGED_EXACT_SEVEN", staged == EXACT_SEVEN_SET, sorted(staged))
    record(checks, "WORKTREE_CHANGED_EXACT_SEVEN", changed_paths() == EXACT_SEVEN_SET, sorted(changed_paths()))
    unstaged = git("diff", "--name-only")
    record(checks, "NO_UNSTAGED_TRACKED", unstaged == "", unstaged)
    mismatch: list[str] = []
    for rel in EXACT_SEVEN:
        index_bytes = git_bytes("show", f":{rel}")
        if index_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n") != normalized_bytes(REPO / rel):
            mismatch.append(rel)
    record(checks, "INDEX_WORKTREE_BYTES", not mismatch, mismatch)
    diff_check = subprocess.run(["git", "diff", "--check", "--cached"], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    record(checks, "STAGED_DIFF_CHECK", diff_check.returncode == 0, diff_check.stdout.decode("utf-8", errors="replace"))
    require_all(checks, "P063_PLAN_ACTIVATION_STAGED")
    print("PASS_P063_PLAN_ACTIVATION_STAGED 7/7")


def verify_persistence(expected_commit: str) -> None:
    if len(expected_commit) != 40 or any(char not in "0123456789abcdef" for char in expected_commit):
        raise SystemExit("E_EXPECTED_COMMIT_FULL_SHA_REQUIRED")
    checks: list[dict[str, Any]] = []
    stored = verify_stored(checks)
    head = git("rev-parse", "HEAD")
    head_symbolic = git("symbolic-ref", "-q", "HEAD")
    branch = git("branch", "--show-current")
    upstream_ref = git("rev-parse", "--symbolic-full-name", "@{upstream}")
    upstream = git("rev-parse", "@{upstream}")
    active_local = ref_hash_or_none(f"refs/heads/{ACTIVE_BRANCH}")
    tracking = ref_hash_or_none(f"refs/remotes/origin/{ACTIVE_BRANCH}")
    live = ls_remote_head(f"refs/heads/{ACTIVE_BRANCH}")
    record(checks, "PERSIST_HEAD", head == expected_commit, head)
    record(checks, "PERSIST_HEAD_SYMBOLIC", head_symbolic == f"refs/heads/{ACTIVE_BRANCH}", head_symbolic)
    record(checks, "PERSIST_BRANCH", branch == ACTIVE_BRANCH, branch)
    record(checks, "PERSIST_UPSTREAM_REF", upstream_ref == f"refs/remotes/origin/{ACTIVE_BRANCH}", upstream_ref)
    record(checks, "PERSIST_UPSTREAM", upstream == expected_commit, upstream)
    record(checks, "PERSIST_ACTIVE_LOCAL", active_local == expected_commit, active_local)
    record(checks, "PERSIST_TRACKING", tracking == expected_commit, tracking)
    record(checks, "PERSIST_LIVE", live == expected_commit, live)
    record(checks, "PERSIST_PARENT", git("rev-parse", f"{expected_commit}^") == EXPECTED_PARENT, git("rev-parse", f"{expected_commit}^"))
    record(checks, "PERSIST_SUBJECT", git("show", "-s", "--format=%s", expected_commit) == EXPECTED_SUBJECT, git("show", "-s", "--format=%s", expected_commit))
    committed = git_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", expected_commit)
    record(checks, "PERSIST_EXACT_SEVEN", committed == EXACT_SEVEN_SET, sorted(committed))
    blob_mismatch: list[str] = []
    for rel in EXACT_SEVEN:
        committed_bytes = git_bytes("show", f"{expected_commit}:{rel}")
        if committed_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n") != normalized_bytes(REPO / rel):
            blob_mismatch.append(rel)
    record(checks, "PERSIST_BLOB_BYTES", not blob_mismatch, blob_mismatch)
    dirty = changed_paths()
    record(checks, "PERSIST_CLEAN", not dirty, sorted(dirty))
    protected_values = [
        ref_hash_or_none(f"refs/heads/{PROTECTED_BRANCH}"),
        ref_hash_or_none(f"refs/remotes/origin/{PROTECTED_BRANCH}"),
        ls_remote_head(f"refs/heads/{PROTECTED_BRANCH}"),
    ]
    main_values = [ref_hash_or_none("refs/heads/main"), ref_hash_or_none("refs/remotes/origin/main"), ls_remote_head("refs/heads/main")]
    record(checks, "PERSIST_PROTECTED_FIXED", protected_values == [EXPECTED_PROTECTED] * 3, protected_values)
    record(checks, "PERSIST_MAIN_FIXED", main_values == [None, EXPECTED_MAIN, EXPECTED_MAIN], main_values)
    claude = git("diff", "--name-only", EXPECTED_PARENT, expected_commit, "--", "Claude")
    record(checks, "PERSIST_CLAUDE_ZERO", claude == "", claude)
    claude_untracked = git("ls-files", "--others", "--exclude-standard", "--", "Claude")
    record(checks, "PERSIST_CLAUDE_UNTRACKED_ZERO", claude_untracked == "", claude_untracked)
    record(checks, "PERSIST_VALIDATION_SHA", len(stored["sha256"]) == 64 and stored["traversal_nodes"] > 0, stored)
    require_all(checks, "P063_PLAN_ACTIVATION_PERSISTENCE")
    print(f"PASS_P063_PLAN_ACTIVATION_PERSISTENCE head={expected_commit}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    modes = sum(bool(value) for value in [args.collect, args.content_only, args.verify_staged, args.verify_persistence])
    if modes != 1:
        raise SystemExit("select exactly one primary mode")
    if args.verify_staged:
        verify_staged()
        return
    if args.verify_persistence:
        if not args.expected_commit:
            raise SystemExit("--expected-commit is required")
        verify_persistence(args.expected_commit)
        return
    if args.content_only and not OUTPUT.is_file():
        print("FAIL E_VALIDATION_ARTIFACT_MISSING")
        print("FAIL_P063_PLAN_CONTENT 0/1")
        raise SystemExit(1)
    payload, checks = build_payload(predecessor_mode="live")
    require_all(checks, "P063_PLAN_CONTENT")
    if args.run_negative_probes:
        controls = negative_controls(payload)
        if not all(row["rejected"] for row in controls):
            print("FAIL P063_PLAN_NEGATIVE_CONTROLS")
            raise SystemExit(1)
        print(f"PASS_P063_PLAN_NEGATIVE_CONTROLS {len(controls)}/{len(controls)}")
    fresh_second: dict[str, Any] | None = None
    if args.determinism_check or args.collect:
        fresh_second, second_checks = build_payload(predecessor_mode="live")
        require_all(second_checks, "P063_PLAN_SECOND_RECONSTRUCTION")
        first = canonical_bytes(payload)
        second = canonical_bytes(fresh_second)
        if first != second:
            print("FAIL P063_PLAN_DETERMINISM")
            raise SystemExit(1)
        print("PASS_P063_PLAN_DETERMINISM 2/2")
    if args.collect:
        if OUTPUT.exists():
            raise SystemExit("E_VALIDATION_ARTIFACT_MUST_BE_ABSENT_FOR_COLLECT")
        if fresh_second is None:
            raise SystemExit("E_FRESH_SECOND_RECONSTRUCTION_MISSING")
        write_output(payload, fresh_second)
        print("PASS_P063_PLAN_ACTIVATION collect=JSON_LAST result_first=true")
    else:
        stored_checks: list[dict[str, Any]] = []
        stored = verify_stored(stored_checks)
        require_all(stored_checks, "P063_PLAN_STORED")
        print(f"PASS_P063_PLAN_CONTENT {len(checks)}/{len(checks)} strict_nodes={stored['traversal_nodes']}")


if __name__ == "__main__":
    try:
        main()
    except (ValidationError, UnicodeDecodeError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"FAIL {type(exc).__name__}: {exc}")
        raise SystemExit(1)
