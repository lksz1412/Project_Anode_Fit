from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import stat
import subprocess
import tempfile
from collections import Counter
from typing import Any, Callable


ROOT = pathlib.Path(__file__).resolve().parents[3]
PLAN_PATH = "Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md"
VALIDATOR_PATH = "Codex/work/v1024_phase065/validate_phase065_plan.py"
OUTPUT_PATH = "Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json"
RESULT_PATH = "Codex/results/PHASE_065_PLAN_ACTIVATION_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"

PLAN = ROOT / PLAN_PATH
VALIDATOR = ROOT / VALIDATOR_PATH
OUTPUT = ROOT / OUTPUT_PATH

EXPECTED_PARENT = "60ec2d2ad08a029224b86ddc3dcf6ff718c6d310"
EXPECTED_PARENT_PARENT = "ec1fb2eda54feb35cd6c15d2ab15f2478b26fc6d"
EXPECTED_PARENT_SUBJECT = "audit(phase064): close v1023 lineage gate"
EXPECTED_SUBJECT = "docs(phase065): plan v1024 lineage reaudit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
GATE = "PASS_P065_PLAN_ACTIVATION"
PERSISTENCE = "PASS_P065_PLAN_ACTIVATION_PERSISTENCE"

PLAN_SHA256_LF = "618eef080d2b893c1555fee967c0d66bfd331a0d60c076bcb8be46be1e291cf3"
MANIFEST_SHA256_LF = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
PATH_SET_SHA256 = "815f37a830da3e5d6539d53bf6dc24c35dec012f39241818b070154b7b729aa7"
PATH_BLOB_SHA256 = "35c224df31807c02ab7d0f8ace3aad7edb36369b6d4d2dd97895589dd5624c0d"
UNIQUE_BLOB_SHA256 = "0cc9e04e676dd9c5024842eeaf57180b515bbe2bb7d068dc7aa8eb10c83c8cdd"
PROCESS_SHA256_LF = "5ab99355b7221e324e022051bb9d9a6d90e8df63907c487b3782257a39954b18"
ROUTED_PROCESS_SHA256_LF = "3579de45ef774036ae3e74ce2cba2c753c37d43721880a8d5316339c54a95bd4"
VALIDATOR_SOURCE_SHA256_LF = "73b33b16ceb9777f3edb81230f66ec466ebe1d7160f56fed34c918f1e9aa5dfb"
VALIDATOR_AST_SHA256 = "f72629db9d5264febbd32c350e00d99e2ff9042b1fa401341f99cb0797f0e14c"

PINNED_FUNCTION_SHA256_LF = {
    "run_process": "a24440c290fe52b6cb9190478c894ef34cacbcb20e647ab3cd41eb30f9ddb8c1",
    "git": "be3ad83b1e079727235638fe327a5f9ee03860179828bdf46939bb90d67af945",
    "git_text": "a6e7f468295f36100d58d80c520fb9baa47b12a9c0a88cc937830bce171a0adc",
    "git_blob": "e0747643936bbdc72e1957af76bad8ab3f0bb9d6f8f71527794dc21ec411ab1c",
    "live_tip": "5da8d1c59c8904eece9db111b10fe35b866c8fee65d143d9d8e9aa21f994f2c1",
    "lf_bytes": "0dd78041c9a5ca4a3869b6ebdcd6624d4993b10410fb3ec143d7deb1107c9758",
    "remove_temp_tree": "65247548b60c0fbeba7adb9ed0ed7410de1a8d1bf540e5b8bbb8e36afddf3c5c",
    "make_git_fixture": "67afca23743e13390dd9ac48ed17c292483f4421eb7041ef6332c68e19a7a635",
    "fixture_delete_allowlisted": "5c54ca0b4036045baeab9af18118bb1335bab28ca117998fd98b6734a894f416",
    "fixture_rename_escape": "ba9a622cfd289c611545ebd26087f38646765f3aafe6c60d2f10e11eba7e1247",
    "fixture_wrong_status": "91c6e959ace0c1f5343665c09e5571ab316b7c8b02473c0c6e5c55cd41f5ee28",
    "run_git_controls": "72f8fd5effad5f3374d5c267b0c42d3b452a6db20497956764862753814e9aef",
    "atomic_collect": "a9ffd1880dcd8caebe7fda3b9395618c7a425e4f7b84e68f64073aa9e962f743",
    "run_source_policy_controls": "8eecb7730715d42a2ef011395b3cc7ef8f931f9d1b8e21062d491e49cb3b03b7",
    "source_policy_diagnostics": "af543073e6c287464f16b0af06dce6aee862bc50b523a9aa91d9b21a84b8a171",
    "repository_snapshot": "c7a881c91437e3303e274f4daabefc37c59de99288c0ad5db8aa9c64985f0814",
    "validate_worktree": "90dee6c1a0f3d4333bc40f650a153a08936199677050623a6a1f98d577a54211",
    "supplemental_contract": "1e9eee6da73e69b42b7aa2fed113eda71acbffd1371d196953fb950810a31af5",
    "process_contract": "22e72425c106302252c0b4fcc804a5b46df0c76a15ea1499b5f9840c4775a3a3",
    "fixture_snapshot": "f43f3cb24992a5e07c72a056e9a784717fdaf0da653056291acb6f3bee4f70d0",
    "persistence_diagnostics": "55c3b11254a329f5adca7fb471d5532789925be4575105586d8cf3ee30f51146",
}

CONTROL_SHA256_LF = {
    RESULT_PATH: "711d7f24e27fae5c115aeef4b554c1f595c16da893f689ed9c5ec473cc537e3c",
    PARENT_LEDGER_PATH: "39393f89c9dfbdf623e5b130ab823f591443b1244a8c47ae5299b4246b51ff01",
    ACTIVE_LEDGER_PATH: "e459a30f7547a65e3ada1739d6d7377661d8e0047ddec49403a1728c5a75c500",
    HANDOVER_PATH: "eed09f245cae0e8f518de93b86692ee7da57e1b6505d7f854bcfed30a126ffd6",
}

FINAL_PATHS = [
    PLAN_PATH,
    VALIDATOR_PATH,
    OUTPUT_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_PATH_SET = set(FINAL_PATHS)
NONSELF_PATHS = [path for path in FINAL_PATHS if path != OUTPUT_PATH]
FINAL_STATUS = {
    PLAN_PATH: "A",
    VALIDATOR_PATH: "A",
    OUTPUT_PATH: "A",
    RESULT_PATH: "A",
    PARENT_LEDGER_PATH: "M",
    ACTIVE_LEDGER_PATH: "M",
    HANDOVER_PATH: "M",
}

SUPPLEMENTAL = [
    ("Claude/plans/2026-07-18-v1024-completeness-validation-plan.md", "b9286c77e686d8666033de553e6bbd8e66d2ad9d", 198, "0935ba2daa90bdaee860a0fe159f8772e0b74cb38f4b3a712876d0b3217dd252"),
    ("Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md", "ed1f2defdae29dc8a4351e63461fd1f1f6c21995", 215, "fa3bdcdcb4bb9cf07d307ef52344730dee295b1f2c6c1ffea48be4c455feb842"),
    ("Claude/plans/2026-07-22-v1024-feedback-revision-plan.md", "c6ec2d6c5b59e5fe7f3020b2d84e1ad325d0b401", 226, "8ae96b72514b412ac2d0a8b6bde1d39235e3ddb9a2c3bb4ec926d51c40bf33a0"),
    ("Claude/results/V1024_EXECUTION_LEDGER.md", "44fcc0042274d5453ed8d8c635d5fe90ec243e5b", 14, "b96103432ac5aa2ae60bacb160d12e3345470d0cd717c7d13f81e4cd4e63aa5f"),
    ("Claude/results/V1024_PROGRESS_SUMMARY.md", "d1a6ec7a3dc9244d6284216c704a75909b3fc02c", 51, "c6932755290032b786fda9ebe60d01a9d4b3bbfde9e20af033de3626a42c33c1"),
    ("Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md", "eb82d88311d81d932dbb16a01684356052a0e7c5", 24, "44cbbf4cc13af7001fa23685ca120b5ef96fc834d2cae07e2f7ba27583cff296"),
]

REQUIRED_HEADINGS = [
    "## Summary",
    "## Current Ground Truth",
    "## Phase Range",
    "## Exact Read Inputs",
    "## Non-goals and Scope Guards",
    "## Implementation Changes",
    "## Plan Activation Unit — Save Before Step 70",
    "## Phase 065 — v1.0.24/v1.0.24.1 Reaudit",
    "## Phase Gate",
    "## Implementation Interfaces",
    "## Test and Validation Plan",
    "## Stop Conditions",
    "## Assumptions",
    "## Correction History",
]

REQUIRED_TOKENS = [
    "261", "131", "21,618", "148", "7,812,647", "15,622,368",
    "fresh import", "explicit profile", "legacy restoration",
    "Step 70", "Step 71", "Step 72", "Step 73", "Step 74", "Step 75.1", "Step 75.2",
    "PASS_P065_LINEAGE_H", "CONDITIONAL_P065", "FAIL_P065",
    "result-first", "validation-JSON-last", "GROUND_NOT_FOUND",
    "external scientific", "v1.0.24.1", "archive note", "38 commits",
    "98 distinct commits", "74 documents / 7,232 lines", "95 bibliography-item",
    "561 citation", "91 DOI occurrences", "IMPLEMENTED_AND_OBSERVED",
    "ABSENT_IN_FROZEN_SOURCE",
]


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def run_process(
    args: list[str], *, cwd: pathlib.Path = ROOT, input_bytes: bytes | None = None,
    timeout: int = 300, check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(
        args, cwd=cwd, input=input_bytes, capture_output=True, timeout=timeout, check=False,
    )
    if check and process.returncode != 0:
        raise ValidationError(
            "E_SUBPROCESS",
            f"{args!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}",
        )
    return process


def git(args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, check=check)


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT) -> str:
    return git(args, cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str, *, cwd: pathlib.Path = ROOT) -> bytes:
    return git(["show", f"{commit}:{path}"], cwd=cwd).stdout


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"], cwd=cwd).splitlines()
    require(len(lines) == 1, "E_LIVE_REF", branch)
    return lines[0].split("\t", 1)[0]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def line_count(raw: bytes) -> int:
    return len(lf_bytes(raw).splitlines())


def canonical_bytes(document: dict[str, Any]) -> bytes:
    return (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def semantic_hash(document: dict[str, Any]) -> str:
    candidate = copy.deepcopy(document)
    candidate["semantic_sha256"] = ""
    return sha256(canonical_bytes(candidate))


def reject_constant(value: str) -> None:
    raise ValidationError("E_NONFINITE_JSON", value)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON", key)
        result[key] = value
    return result


def strict_load_bytes(raw: bytes, label: str) -> tuple[dict[str, Any], int]:
    try:
        document = json.loads(
            raw.decode("utf-8"), parse_constant=reject_constant, object_pairs_hook=reject_pairs,
        )
    except (UnicodeError, json.JSONDecodeError, OverflowError) as error:
        raise ValidationError("E_STRICT_JSON", f"{label}:{error}") from error
    require(isinstance(document, dict), "E_JSON_ROOT", label)
    count = 0
    stack: list[Any] = [document]
    while stack:
        item = stack.pop()
        count += 1
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, float):
            require(math.isfinite(item), "E_NONFINITE_JSON", label)
    return document, count


def neutralized_validator_source(raw: bytes) -> bytes:
    text = lf_bytes(raw).decode("utf-8")
    for name in ("VALIDATOR_SOURCE_SHA256_LF", "VALIDATOR_AST_SHA256"):
        pattern = rf'(?m)^{name} = "[0-9a-f]{{64}}"$'
        text, count = re.subn(pattern, f'{name} = "' + ("0" * 64) + '"', text)
        require(count == 1, "E_SOURCE_HASH_FIELD", name)
    return text.encode("utf-8")


def validator_ast_hash(raw: bytes) -> str:
    tree = ast.parse(neutralized_validator_source(raw).decode("utf-8"), filename=VALIDATOR_PATH)

    def project(value: Any) -> Any:
        if isinstance(value, ast.AST):
            fields = {
                name: project(child)
                for name, child in ast.iter_fields(value)
                if not (name == "type_params" and child == [])
            }
            return [type(value).__name__, fields]
        if isinstance(value, list):
            return [project(child) for child in value]
        if isinstance(value, bytes):
            return ["bytes", value.hex()]
        if value is Ellipsis:
            return ["ellipsis"]
        return value

    return sha256(json.dumps(project(tree), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def source_policy_diagnostics(raw: bytes) -> set[str]:
    failures: set[str] = set()
    try:
        tree = ast.parse(lf_bytes(raw).decode("utf-8"), filename=VALIDATOR_PATH)
    except (SyntaxError, UnicodeError):
        return {"E_SOURCE_PARSE"}
    allowed = {
        "__future__", "argparse", "ast", "copy", "hashlib", "json", "math", "os",
        "pathlib", "re", "shutil", "stat", "subprocess", "tempfile", "collections", "typing",
    }
    forbidden_calls = {
        "eval", "exec", "compile", "__import__", "open", "input", "breakpoint",
        "getattr", "setattr", "delattr", "globals", "locals", "vars", "__builtins__",
        "__loader__", "__spec__", "__package__", "__cached__",
    }
    forbidden_attributes = {
        "__dict__", "__getattribute__", "__globals__", "__builtins__", "__subclasses__",
        "__class__", "__base__", "__bases__", "__mro__", "__code__", "__closure__",
        "__func__", "__self__", "gi_frame", "cr_frame", "ag_frame", "tb_frame",
        "f_builtins", "f_globals", "f_locals", "f_code", "f_back", "tb_next",
    }
    allowed_dunder_attributes = {"__init__", "__name__", "__setitem__"}
    allowed_from = {
        "__future__": {"annotations"},
        "collections": {"Counter"},
        "typing": {"Any", "Callable"},
    }
    allowed_mutator_owners = {
        "atomic_collect", "make_git_fixture", "remove_temp_tree", "remove_temp_tree.clear_readonly",
        "fixture_delete_allowlisted", "fixture_rename_escape", "run_git_controls", "lf_bytes",
        "run_source_policy_controls",
    }
    path_mutators = {
        "write_bytes", "write_text", "unlink", "mkdir", "rmdir", "rename", "replace",
        "touch", "chmod", "symlink_to", "hardlink_to", "open", "write", "writelines",
        "truncate", "link_to", "lchmod", "copy", "copy_into", "move", "move_into",
    }
    module_mutators = {
        "os": {"replace", "remove", "unlink", "mkdir", "makedirs", "rmdir", "removedirs", "rename", "renames", "chmod", "lchmod", "open", "write", "truncate", "ftruncate", "utime", "chown", "lchown", "setxattr", "removexattr", "chflags", "link", "symlink", "mkfifo", "mknod"},
        "shutil": {"rmtree", "copy", "copy2", "copyfile", "move", "copytree", "copymode", "copystat", "chown", "make_archive", "unpack_archive"},
        "tempfile": {"mkdtemp", "mkstemp", "mktemp", "NamedTemporaryFile", "TemporaryFile", "SpooledTemporaryFile", "TemporaryDirectory"},
    }
    allowed_git_owners = {
        "git_text", "git_blob", "repository_snapshot", "validate_worktree", "process_contract",
        "make_git_fixture", "fixture_snapshot", "fixture_delete_allowlisted",
        "fixture_rename_escape", "fixture_wrong_status", "run_git_controls",
        "persistence_diagnostics",
    }
    allowed_git_text_owners = {
        "live_tip", "repository_snapshot", "supplemental_contract", "make_git_fixture",
        "fixture_snapshot", "persistence_diagnostics",
    }
    allowed_git_blob_owners = {"supplemental_contract", "persistence_diagnostics"}
    allowed_live_tip_owners = {"repository_snapshot"}
    privileged_callables = {"run_process", "git", "git_text", "git_blob", "live_tip"}
    allowed_module_attributes = {
        "argparse": {"ArgumentParser"},
        "ast": {"AST", "AnnAssign", "Assign", "AsyncFunctionDef", "Attribute", "Call", "ClassDef", "Constant", "FunctionDef", "Import", "ImportFrom", "List", "Load", "Name", "NamedExpr", "iter_child_nodes", "iter_fields", "parse", "walk"},
        "copy": {"deepcopy"},
        "hashlib": {"sha256"},
        "json": {"JSONDecodeError", "dumps", "loads"},
        "math": {"isfinite"},
        "os": {"chmod", "replace"},
        "pathlib": {"Path"},
        "re": {"fullmatch", "subn"},
        "shutil": {"rmtree"},
        "stat": {"S_IWRITE"},
        "subprocess": {"CompletedProcess", "TimeoutExpired", "run"},
        "tempfile": {"gettempdir", "mkdtemp"},
    }
    controlled_modules = set(allowed_module_attributes)
    allowed_git_commands = {
        "show", "ls-remote", "rev-parse", "branch", "diff", "status", "show-ref",
        "log", "init", "config", "add", "commit", "switch", "remote", "push",
        "fetch", "rm", "mv", "update-ref", "diff-tree", "ls-files", "--git-dir",
    }
    functions = Counter(
        node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )
    if any(count != 1 for count in functions.values()):
        failures.add("E_SOURCE_DUPLICATE_FUNCTION")
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    def owner(node: ast.AST) -> str | None:
        names: list[str] = []
        cursor = parents.get(node)
        while cursor is not None:
            if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.append(cursor.name)
            cursor = parents.get(cursor)
        return ".".join(reversed(names)) if names else None

    def root_name(node: ast.AST) -> str | None:
        cursor = node
        while isinstance(cursor, ast.Attribute):
            cursor = cursor.value
        return cursor.id if isinstance(cursor, ast.Name) else None

    lines = lf_bytes(raw).splitlines(keepends=True)
    top_functions = {
        node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    for name, expected_hash in PINNED_FUNCTION_SHA256_LF.items():
        node = top_functions.get(name)
        if node is None:
            failures.add("E_SOURCE_PINNED_CALLSITE")
            continue
        observed = sha256(b"".join(lines[node.lineno - 1:node.end_lineno]))
        if observed != expected_hash:
            failures.add("E_SOURCE_PINNED_CALLSITE")

    def inspect_git_argv(call: ast.Call) -> None:
        if not call.args or not isinstance(call.args[0], ast.List) or not call.args[0].elts:
            failures.add("E_SOURCE_GIT_DYNAMIC_ARGV")
            return
        argv = call.args[0]
        first = argv.elts[0]
        if not isinstance(first, ast.Constant) or not isinstance(first.value, str):
            failures.add("E_SOURCE_GIT_DYNAMIC_ARGV")
            return
        command = first.value
        if command == "--git-dir":
            if len(argv.elts) < 3 or not isinstance(argv.elts[2], ast.Constant) or argv.elts[2].value not in {"rev-parse", "update-ref"}:
                failures.add("E_SOURCE_GIT_COMMAND")
        elif command not in allowed_git_commands:
            failures.add("E_SOURCE_GIT_COMMAND")
        literals = [child.value for child in ast.walk(argv) if isinstance(child, ast.Constant) and isinstance(child.value, str)]
        if any(value.startswith("alias.") or value.startswith("!") or value.startswith("ext::") for value in literals):
            failures.add("E_SOURCE_GIT_ESCAPE")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".", 1)[0] not in allowed for alias in node.names):
                failures.add("E_SOURCE_IMPORT")
            if any(alias.asname is not None for alias in node.names):
                failures.add("E_SOURCE_IMPORT_ALIAS")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".", 1)[0] not in allowed:
                failures.add("E_SOURCE_IMPORT")
            if module not in allowed_from or any(alias.name not in allowed_from[module] or alias.asname is not None for alias in node.names):
                failures.add("E_SOURCE_FROM_IMPORT")
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in forbidden_calls:
            failures.add("E_SOURCE_FORBIDDEN_CALL")
        elif isinstance(node, ast.Attribute):
            root = root_name(node)
            parent = parents.get(node)
            if root in controlled_modules:
                direct = isinstance(node.value, ast.Name) and node.value.id == root
                if not direct or node.attr not in allowed_module_attributes[root]:
                    failures.add("E_SOURCE_MODULE_BYPASS")
            if root == "subprocess":
                allowed_annotation = node.attr in {"CompletedProcess", "TimeoutExpired"}
                allowed_run = (
                    node.attr == "run" and isinstance(parent, ast.Call)
                    and parent.func is node and owner(node) == "run_process"
                )
                if not (allowed_annotation or allowed_run):
                    failures.add("E_SOURCE_SUBPROCESS_BYPASS")
            if (
                node.attr in {"system", "popen", "startfile", "execv", "execve", "execvp", "execvpe", "posix_spawn", "posix_spawnp", "fork", "forkpty", "Popen"}
                or node.attr in forbidden_attributes
                or (node.attr.startswith("__") and node.attr not in allowed_dunder_attributes)
            ):
                failures.add("E_SOURCE_EXECUTION_ESCAPE")
            if root == "os" and (node.attr.startswith("spawn") or node.attr.startswith("exec")):
                failures.add("E_SOURCE_EXECUTION_ESCAPE")
            if node.attr in path_mutators and owner(node) not in allowed_mutator_owners:
                failures.add("E_SOURCE_FILESYSTEM_MUTATOR")
            if root in module_mutators and node.attr in module_mutators[root] and owner(node) not in allowed_mutator_owners:
                failures.add("E_SOURCE_FILESYSTEM_MUTATOR")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "run_process":
            if owner(node) != "git":
                failures.add("E_SOURCE_RUN_PROCESS_BYPASS")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "git":
            if owner(node) not in allowed_git_owners:
                failures.add("E_SOURCE_GIT_CALLSITE")
            if owner(node) not in {"git_text", "git_blob"}:
                inspect_git_argv(node)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "git_text":
            if owner(node) not in allowed_git_text_owners:
                failures.add("E_SOURCE_GIT_CALLSITE")
            inspect_git_argv(node)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "git_blob":
            if owner(node) not in allowed_git_blob_owners:
                failures.add("E_SOURCE_GIT_CALLSITE")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "live_tip":
            if owner(node) not in allowed_live_tip_owners:
                failures.add("E_SOURCE_GIT_CALLSITE")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in privileged_callables:
            parent = parents.get(node)
            if not (isinstance(parent, ast.Call) and parent.func is node):
                failures.add("E_SOURCE_CALLABLE_ALIAS")
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            value = node.value
            if isinstance(value, ast.Name) and value.id in {"run_process", "git", "git_text", "git_blob", "live_tip"}:
                failures.add("E_SOURCE_CALLABLE_ALIAS")
            if isinstance(value, ast.Attribute) and root_name(value) == "subprocess":
                failures.add("E_SOURCE_SUBPROCESS_BYPASS")
        if isinstance(node, ast.Name) and node.id in controlled_modules:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute):
                failures.add("E_SOURCE_SUBPROCESS_BYPASS" if node.id == "subprocess" else "E_SOURCE_MODULE_BYPASS")
    return failures


def validator_contract() -> dict[str, Any]:
    raw = VALIDATOR.read_bytes()
    require(sha256(neutralized_validator_source(raw)) == VALIDATOR_SOURCE_SHA256_LF, "E_VALIDATOR_SOURCE_HASH")
    require(validator_ast_hash(raw) == VALIDATOR_AST_SHA256, "E_VALIDATOR_AST_HASH")
    require(not source_policy_diagnostics(raw), "E_VALIDATOR_SOURCE_POLICY", repr(source_policy_diagnostics(raw)))
    return {
        "path": VALIDATOR_PATH,
        "sha256_lf": sha256(lf_bytes(raw)),
        "neutralized_sha256_lf": VALIDATOR_SOURCE_SHA256_LF,
        "normalized_ast_sha256": VALIDATOR_AST_SHA256,
        "source_policy": "PASS",
        "production_source_imported": False,
    }


def nul_paths(raw: bytes) -> set[str]:
    return {part.decode("utf-8") for part in raw.split(b"\0") if part}


def name_status_map(raw: bytes) -> dict[str, str]:
    parts = [part for part in raw.split(b"\0") if part]
    require(len(parts) % 2 == 0, "E_GIT_STATUS_PARSE", repr(parts[-3:]))
    result: dict[str, str] = {}
    for offset in range(0, len(parts), 2):
        status = parts[offset].decode("ascii")
        path = parts[offset + 1].decode("utf-8")
        require(status in {"A", "M", "D", "T", "U"}, "E_GIT_STATUS_CODE", status)
        require(path not in result, "E_GIT_STATUS_DUPLICATE", path)
        result[path] = status
    return result


def repository_snapshot() -> dict[str, Any]:
    return {
        "branch": git_text(["branch", "--show-current"]),
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]),
        "upstream": git_text(["rev-parse", "@{upstream}"]),
        "origin_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"]),
        "live_active": live_tip(ACTIVE_BRANCH),
        "local_protected": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]),
        "origin_protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"]),
        "live_protected": live_tip(PROTECTED_BRANCH),
        "origin_main": git_text(["rev-parse", "refs/remotes/origin/main"]),
        "live_main": live_tip("main"),
        "staged_status": name_status_map(git(["diff", "--cached", "--no-renames", "--name-status", "-z"]).stdout),
        "unstaged_status": name_status_map(git(["diff", "--no-renames", "--name-status", "-z"]).stdout),
        "untracked": nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout),
        "claude_dirty": bool(git(["status", "--porcelain=v1", "--", "Claude"]).stdout),
        "claude_baseline_diff": bool(git(["diff", "--name-only", BASELINE, "--", "Claude"]).stdout),
        "claude_parent_diff": bool(git(["diff", "--name-only", EXPECTED_PARENT, "--", "Claude"]).stdout),
        "claude_untracked": bool(git(["ls-files", "--others", "--exclude-standard", "--", "Claude"]).stdout),
        "local_main_absent": git(["show-ref", "--verify", "--quiet", "refs/heads/main"], check=False).returncode != 0,
        "diff_check": git(["diff", "--check"], check=False).returncode == 0,
    }


def ref_diagnostics(snapshot: dict[str, Any], expected_active: str) -> set[str]:
    checks = (
        ("E_GIT_BRANCH", snapshot["branch"] == ACTIVE_BRANCH),
        ("E_GIT_UPSTREAM_NAME", snapshot["upstream_name"] == f"origin/{ACTIVE_BRANCH}"),
        ("E_GIT_HEAD", snapshot["head"] == expected_active),
        ("E_GIT_UPSTREAM", snapshot["upstream"] == expected_active),
        ("E_GIT_ACTIVE_TRACKING", snapshot["origin_active"] == expected_active),
        ("E_GIT_ACTIVE_LIVE", snapshot["live_active"] == expected_active),
        ("E_GIT_LOCAL_PROTECTED", snapshot["local_protected"] == PROTECTED_TIP),
        ("E_GIT_PROTECTED_TRACKING", snapshot["origin_protected"] == PROTECTED_TIP),
        ("E_GIT_PROTECTED_LIVE", snapshot["live_protected"] == PROTECTED_TIP),
        ("E_GIT_MAIN_TRACKING", snapshot["origin_main"] == MAIN_TIP),
        ("E_GIT_MAIN_LIVE", snapshot["live_main"] == MAIN_TIP),
        ("E_GIT_LOCAL_MAIN", snapshot["local_main_absent"] is True),
        ("E_GIT_CLAUDE", snapshot["claude_dirty"] is False and snapshot["claude_baseline_diff"] is False and snapshot["claude_parent_diff"] is False and snapshot["claude_untracked"] is False),
    )
    return {code for code, passed in checks if not passed}


def validate_worktree(expected_paths: set[str], *, staged: bool) -> None:
    snapshot = repository_snapshot()
    diagnostics = ref_diagnostics(snapshot, EXPECTED_PARENT)
    dirty = set(snapshot["staged_status"]) | set(snapshot["unstaged_status"]) | snapshot["untracked"]
    if dirty != expected_paths:
        diagnostics.add("E_GIT_DIRTY_PATHS")
    if staged:
        if snapshot["staged_status"] != FINAL_STATUS:
            diagnostics.add("E_GIT_STAGED_STATUS")
        if snapshot["unstaged_status"] or snapshot["untracked"]:
            diagnostics.add("E_GIT_UNSTAGED")
        if git(["diff", "--cached", "--check"], check=False).returncode != 0:
            diagnostics.add("E_GIT_DIFF_CHECK")
        for path in FINAL_PATHS:
            if git(["show", f":{path}"], check=False).stdout != (ROOT / path).read_bytes():
                diagnostics.add("E_GIT_INDEX")
    elif not snapshot["diff_check"]:
        diagnostics.add("E_GIT_DIFF_CHECK")
    elif snapshot["staged_status"]:
        diagnostics.add("E_GIT_PREMATURE_STAGE")
    else:
        expected_untracked = {path for path in expected_paths if FINAL_STATUS[path] == "A"}
        expected_unstaged = {path: "M" for path in expected_paths if FINAL_STATUS[path] == "M"}
        if snapshot["untracked"] != expected_untracked or snapshot["unstaged_status"] != expected_unstaged:
            diagnostics.add("E_GIT_WORKTREE_STATUS")
    require(not diagnostics, "E_REPOSITORY", repr(sorted(diagnostics)))


def manifest_contract() -> dict[str, Any]:
    raw = (ROOT / MANIFEST_PATH).read_bytes()
    require(sha256(lf_bytes(raw)) == MANIFEST_SHA256_LF, "E_MANIFEST_HASH")
    document, _ = strict_load_bytes(raw, MANIFEST_PATH)
    entries = document["entries"]
    selected = [(index, row) for index, row in enumerate(entries) if row.get("version") in {"v1.0.24", "v1.0.24.1"}]
    indices = [index for index, _ in selected]
    rows = [row for _, row in selected]
    require(indices == list(range(826, 1087)), "E_MANIFEST_INDICES")
    versions = Counter(row["version"] for row in rows)
    roles = Counter(row["role"] for row in rows)
    modes = Counter(row["review_mode"] for row in rows)
    unique = {row["blob_sha"]: row for row in rows}
    unique_modes = Counter(row["review_mode"] for row in unique.values())
    unique_roles = Counter(row["role"] for row in unique.values())
    path_set_hash = sha256(("\n".join(sorted(row["path"] for row in rows)) + "\n").encode("utf-8"))
    path_blob_hash = sha256(("\n".join(sorted(row["path"] + "\0" + row["blob_sha"] for row in rows)) + "\n").encode("utf-8"))
    blob_set_hash = sha256(("\n".join(sorted(unique)) + "\n").encode("utf-8"))
    require(path_set_hash == PATH_SET_SHA256, "E_MANIFEST_PATH_HASH")
    require(path_blob_hash == PATH_BLOB_SHA256, "E_MANIFEST_PATH_BLOB_HASH")
    require(blob_set_hash == UNIQUE_BLOB_SHA256, "E_MANIFEST_BLOB_HASH")
    text_lines = sum(int(row.get("extent", {}).get("lines") or 0) for row in unique.values())
    pdf_pages = sum(int(row.get("extent", {}).get("pages") or 0) for row in unique.values())
    occurrence_bytes = sum(int(row["size_bytes"]) for row in rows)
    unique_bytes = sum(int(row["size_bytes"]) for row in unique.values())
    require(len(rows) == 261 and len(unique) == 131, "E_MANIFEST_COUNTS")
    require(versions == {"v1.0.24": 130, "v1.0.24.1": 131}, "E_MANIFEST_VERSIONS")
    require(modes == {"FULL_TEXT": 249, "FULL_PDF": 6, "FULL_IMAGE": 6}, "E_MANIFEST_MODES")
    require(unique_modes == {"FULL_TEXT": 125, "FULL_PDF": 3, "FULL_IMAGE": 3}, "E_MANIFEST_UNIQUE_MODES")
    require(text_lines == 21618 and pdf_pages == 148, "E_MANIFEST_EXTENTS")
    require(occurrence_bytes == 15622368 and unique_bytes == 7812647, "E_MANIFEST_BYTES")
    prefix24 = "Claude/docs/v1.0.24/"
    prefix241 = "Claude/docs/v1.0.24.1/"
    by24 = {row["path"][len(prefix24):]: row for row in rows if row["path"].startswith(prefix24)}
    by241 = {row["path"][len(prefix241):]: row for row in rows if row["path"].startswith(prefix241)}
    common = sorted(set(by24) & set(by241))
    require(len(common) == 130, "E_MIRROR_COMMON")
    require(all(by24[path]["blob_sha"] == by241[path]["blob_sha"] for path in common), "E_MIRROR_BLOB")
    require(set(by241) - set(by24) == {"ARCHIVE_NOTE.md"} and not (set(by24) - set(by241)), "E_MIRROR_DELTA")
    return {
        "manifest_path": MANIFEST_PATH,
        "manifest_sha256_lf": MANIFEST_SHA256_LF,
        "zero_based_indices": [826, 1086],
        "one_based_ordinals": [827, 1087],
        "occurrences": len(rows),
        "unique_paths": len({row["path"] for row in rows}),
        "unique_blobs": len(unique),
        "versions": dict(sorted(versions.items())),
        "occurrence_roles": dict(sorted(roles.items())),
        "unique_roles": dict(sorted(unique_roles.items())),
        "occurrence_review_modes": dict(sorted(modes.items())),
        "unique_review_modes": dict(sorted(unique_modes.items())),
        "unique_text_lines": text_lines,
        "unique_pdf_pages": pdf_pages,
        "occurrence_bytes": occurrence_bytes,
        "unique_bytes": unique_bytes,
        "path_set_sha256": path_set_hash,
        "path_blob_sha256": path_blob_hash,
        "unique_blob_sha256": blob_set_hash,
        "shared_relative_paths": len(common),
        "shared_byte_identical": sum(by24[path]["blob_sha"] == by241[path]["blob_sha"] for path in common),
        "v1024_1_only": ["ARCHIVE_NOTE.md"],
        "independent_validation_corpus": False,
    }


def supplemental_contract() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path, expected_blob, expected_lines, expected_hash in SUPPLEMENTAL:
        raw = git_blob(BASELINE, path)
        blob = git_text(["rev-parse", f"{BASELINE}:{path}"])
        require(blob == expected_blob, "E_SUPPLEMENTAL_BLOB", path)
        require(line_count(raw) == expected_lines, "E_SUPPLEMENTAL_LINES", path)
        require(sha256(lf_bytes(raw)) == expected_hash, "E_SUPPLEMENTAL_HASH", path)
        records.append({
            "path": path, "blob": blob, "lines": expected_lines,
            "sha256_lf": expected_hash, "read_required": "FULL_TEXT",
        })
    return {"count": len(records), "lines": sum(row[2] for row in SUPPLEMENTAL), "records": records, "separate_from_manifest": True}


def process_contract() -> dict[str, Any]:
    raw = git([
        "log", "--reverse", "--format=%H", "--all", "--",
        "Claude/docs/v1.0.24/**", "Claude/docs/v1.0.24.1/**",
    ]).stdout
    normalized = lf_bytes(raw)
    commits = normalized.decode("ascii").splitlines()
    require(len(commits) == 38, "E_PROCESS_COUNT")
    require(commits[0] == "04ebc0cf8b36d34f776ddbc2b356ca0246983fe8", "E_PROCESS_FIRST")
    require(commits[-1] == "2147abfac3fb6c82279aefb2b21c749a521112dc", "E_PROCESS_LAST")
    require(sha256(normalized) == PROCESS_SHA256_LF, "E_PROCESS_HASH")
    routed_paths = [
        "Claude/docs/v1.0.24/**", "Claude/docs/v1.0.24.1/**",
        "Claude/plans/2026-07-18-v1024-completeness-validation-plan.md",
        "Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md",
        "Claude/plans/2026-07-22-v1024-feedback-revision-plan.md",
        "Claude/results/V1024_EXECUTION_LEDGER.md",
        "Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md",
        "Claude/results/V1024_PROGRESS_SUMMARY.md",
        "Claude/results/comp_v24/**",
    ]
    routed_raw = git(["log", "--reverse", "--format=%H", "--all", "--", *routed_paths]).stdout
    routed_normalized = lf_bytes(routed_raw)
    routed = routed_normalized.decode("ascii").splitlines()
    require(len(routed) == 98, "E_ROUTED_PROCESS_COUNT")
    require(routed[0] == "88374d578ea0a3bc9641693a8bd77c700f308874", "E_ROUTED_PROCESS_FIRST")
    require(routed[-1] == "2147abfac3fb6c82279aefb2b21c749a521112dc", "E_ROUTED_PROCESS_LAST")
    require(sha256(routed_normalized) == ROUTED_PROCESS_SHA256_LF, "E_ROUTED_PROCESS_HASH")
    return {
        "release_query": ["Claude/docs/v1.0.24/**", "Claude/docs/v1.0.24.1/**"],
        "release_commit_count": len(commits),
        "release_first": commits[0],
        "release_last": commits[-1],
        "release_sha256_lf": PROCESS_SHA256_LF,
        "routed_query": routed_paths,
        "routed_commit_count": len(routed),
        "routed_first": routed[0],
        "routed_last": routed[-1],
        "routed_sha256_lf": ROUTED_PROCESS_SHA256_LF,
        "full_parent_path_diff_read_required_step70": True,
    }


def plan_contract() -> dict[str, Any]:
    raw = PLAN.read_bytes()
    normalized = lf_bytes(raw)
    require(sha256(normalized) == PLAN_SHA256_LF, "E_PLAN_HASH")
    text = normalized.decode("utf-8")
    positions = [text.find(heading) for heading in REQUIRED_HEADINGS]
    require(all(position >= 0 for position in positions), "E_PLAN_HEADING")
    require(positions == sorted(positions), "E_PLAN_HEADING_ORDER")
    require(all(token in text for token in REQUIRED_TOKENS), "E_PLAN_TOKEN")
    require(text.count("### Step 70") == 2, "E_PLAN_STEP70")
    require(text.count("### Step 71") == 2, "E_PLAN_STEP71")
    require(text.count("### Step 72") == 2, "E_PLAN_STEP72")
    require(text.count("### Step 73") == 2, "E_PLAN_STEP73")
    require(text.count("### Step 74") == 2, "E_PLAN_STEP74")
    require(text.count("### Step 75.1") == 2, "E_PLAN_STEP751")
    require(text.count("### Step 75.2") == 2, "E_PLAN_STEP752")
    require("Phase 066 begins at Step 76" in text, "E_PLAN_CUMULATIVE")
    require("Step 73 must consume the exact symbol" in text, "E_PLAN_PROFILE_DEFERRED")
    require("immutable Phase 059 planning snapshots" in text, "E_PLAN_MASTER_JSON_BOUNDARY")
    return {
        "path": PLAN_PATH,
        "sha256_lf": PLAN_SHA256_LF,
        "bytes_lf": len(normalized),
        "physical_lines": line_count(normalized),
        "headings": REQUIRED_HEADINGS,
        "cumulative_steps": ["70", "71", "72", "73", "74", "75.1", "75.2"],
        "next_phase_step": 76,
    }


def control_contract() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path, expected_hash in CONTROL_SHA256_LF.items():
        raw = (ROOT / path).read_bytes()
        observed = sha256(lf_bytes(raw))
        require(observed == expected_hash, "E_CONTROL_HASH", path)
        text = lf_bytes(raw).decode("utf-8")
        records.append({"path": path, "sha256_lf": observed, "lines": line_count(raw)})
        if path == RESULT_PATH:
            require("PASS_P065_PLAN_ACTIVATION" in text and "PENDING_AT_PRECOMMIT_BY_DESIGN" in text, "E_CONTROL_RESULT")
        elif path == PARENT_LEDGER_PATH:
            require("PASS_P064_STEP69_2_PERSISTENCE" in text and "PLAN_ACTIVATION_PENDING_PERSISTENCE" in text, "E_CONTROL_PARENT_LEDGER")
        elif path == ACTIVE_LEDGER_PATH:
            require("Phase 065 plan activation" in text and "PASS_P064_STEP69_2_PERSISTENCE" in text, "E_CONTROL_ACTIVE_LEDGER")
        elif path == HANDOVER_PATH:
            require("Phase 065 plan activation" in text and "PASS_P064_STEP69_2_PERSISTENCE" in text, "E_CONTROL_HANDOVER")
    return {"count": len(records), "records": records, "result_first": True, "validation_json_last": True, "precommit_record_state": True}


def build_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "P065-PLAN-ACTIVATION-1",
        "phase": "065",
        "generated_date": "2026-08-30",
        "status": "PASS_PENDING_PERSISTENCE",
        "gate": GATE,
        "persistence_terminal": PERSISTENCE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "repository": {
            "branch": ACTIVE_BRANCH,
            "expected_parent": EXPECTED_PARENT,
            "expected_parent_parent": EXPECTED_PARENT_PARENT,
            "expected_parent_subject": EXPECTED_PARENT_SUBJECT,
            "protected_branch": PROTECTED_BRANCH,
            "protected_tip": PROTECTED_TIP,
            "main_tip": MAIN_TIP,
            "baseline": BASELINE,
            "operational_active_commit_masked": True,
            "claude_modification_allowed": False,
        },
        "plan": plan_contract(),
        "manifest": manifest_contract(),
        "supplemental": supplemental_contract(),
        "process": process_contract(),
        "controls": control_contract(),
        "exact_seven": {
            "count": 7,
            "paths": FINAL_PATHS,
            "result_first": True,
            "validation_json_last": True,
            "rename_allowed": False,
        },
        "runtime_gate_contract": {
            "fresh_import": "INDEPENDENT_REQUIRED_STEP73",
            "explicit_profile": "INDEPENDENT_REQUIRED_STEP73_AFTER_STEP71_MAPPING",
            "legacy_restoration": "INDEPENDENT_REQUIRED_STEP73",
            "separate_processes": True,
            "order_leakage_negative_control": True,
            "combined_outcome_forbidden": True,
        },
        "authority": {
            "internal_plan_inventory_only": True,
            "v1024_1_independent_corroboration": False,
            "external_scientific": False,
            "external_material": False,
            "external_experimental": False,
            "canonical": False,
            "publication_ready": False,
            "phase064_ref7_closed": False,
        },
        "negative_contract": {
            "semantic_cases": 24,
            "strict_json_cases": 6,
            "source_policy_cases": 64,
            "actual_git_cases": 19,
            "exact_singleton_diagnostics": True,
        },
        "determinism": {"reconstructions": 2, "byte_identical": True},
        "validator_identity": validator_contract(),
        "semantic_sha256": "",
    }
    payload["semantic_sha256"] = semantic_hash(payload)
    return payload


SECTION_CODES = {
    "schema_version": "E_SCHEMA",
    "phase": "E_PHASE",
    "generated_date": "E_DATE",
    "status": "E_STATUS",
    "gate": "E_GATE",
    "persistence_terminal": "E_PERSISTENCE",
    "expected_parent": "E_PARENT",
    "expected_subject": "E_SUBJECT",
    "repository": "E_REPOSITORY_DOCUMENT",
    "plan": "E_PLAN_DOCUMENT",
    "manifest": "E_MANIFEST_DOCUMENT",
    "supplemental": "E_SUPPLEMENTAL_DOCUMENT",
    "process": "E_PROCESS_DOCUMENT",
    "controls": "E_CONTROLS_DOCUMENT",
    "exact_seven": "E_EXACT_SEVEN",
    "runtime_gate_contract": "E_RUNTIME_GATE",
    "authority": "E_AUTHORITY",
    "negative_contract": "E_NEGATIVE_CONTRACT",
    "determinism": "E_DETERMINISM",
    "validator_identity": "E_VALIDATOR_DOCUMENT",
}


def document_diagnostics(document: dict[str, Any], expected: dict[str, Any]) -> set[str]:
    failures: set[str] = set()
    if set(document) != set(expected):
        failures.add("E_SCHEMA_KEYS")
    for key, code in SECTION_CODES.items():
        if document.get(key) != expected.get(key):
            failures.add(code)
    if document.get("semantic_sha256") != semantic_hash(document):
        failures.add("E_SEMANTIC_HASH")
    return failures


def run_negative_controls(expected: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("E_PARENT", lambda d: d.__setitem__("expected_parent", "0" * 40), True),
        ("E_REPOSITORY_DOCUMENT", lambda d: d["repository"].__setitem__("protected_tip", "0" * 40), True),
        ("E_PLAN_DOCUMENT", lambda d: d["plan"].__setitem__("next_phase_step", 75), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("occurrences", 131), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("unique_blobs", 261), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("unique_text_lines", 43196), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("unique_pdf_pages", 296), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("path_set_sha256", "0" * 64), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("shared_byte_identical", 129), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("v1024_1_only", []), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].__setitem__("independent_validation_corpus", True), True),
        ("E_SUPPLEMENTAL_DOCUMENT", lambda d: d["supplemental"].__setitem__("lines", 727), True),
        ("E_PROCESS_DOCUMENT", lambda d: d["process"].__setitem__("release_commit_count", 37), True),
        ("E_CONTROLS_DOCUMENT", lambda d: d["controls"].__setitem__("result_first", False), True),
        ("E_EXACT_SEVEN", lambda d: d["exact_seven"]["paths"].pop(), True),
        ("E_RUNTIME_GATE", lambda d: d["runtime_gate_contract"].__setitem__("fresh_import", "COMBINED"), True),
        ("E_RUNTIME_GATE", lambda d: d["runtime_gate_contract"].__setitem__("explicit_profile", "COMBINED"), True),
        ("E_RUNTIME_GATE", lambda d: d["runtime_gate_contract"].__setitem__("legacy_restoration", "OMITTED"), True),
        ("E_RUNTIME_GATE", lambda d: d["runtime_gate_contract"].__setitem__("separate_processes", False), True),
        ("E_RUNTIME_GATE", lambda d: d["runtime_gate_contract"].__setitem__("order_leakage_negative_control", False), True),
        ("E_AUTHORITY", lambda d: d["authority"].__setitem__("external_scientific", True), True),
        ("E_AUTHORITY", lambda d: d["authority"].__setitem__("v1024_1_independent_corroboration", True), True),
        ("E_AUTHORITY", lambda d: d["authority"].__setitem__("phase064_ref7_closed", True), True),
        ("E_SEMANTIC_HASH", lambda d: d.__setitem__("semantic_sha256", "0" * 64), False),
    ]
    passed = 0
    for wanted, mutation, rehash in cases:
        candidate = copy.deepcopy(expected)
        mutation(candidate)
        if rehash:
            candidate["semantic_sha256"] = semantic_hash(candidate)
        observed = document_diagnostics(candidate, expected)
        require(observed == {wanted}, "E_NEGATIVE_DIAGNOSTIC", f"{wanted}:{sorted(observed)}")
        passed += 1
    strict_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e9999}', b'{"x":']
    for raw in strict_cases:
        try:
            strict_load_bytes(raw, "negative")
        except ValidationError as error:
            require(error.code in {"E_DUPLICATE_JSON", "E_NONFINITE_JSON", "E_STRICT_JSON"}, "E_STRICT_NEGATIVE_CODE", error.code)
        else:
            raise ValidationError("E_STRICT_NEGATIVE_ESCAPE")
    return passed, len(cases)


def run_source_policy_controls(raw: bytes) -> tuple[int, int]:
    require(not source_policy_diagnostics(raw), "E_SOURCE_POLICY_BASELINE")
    cases = [
        (b"\nimport urllib.request\n", {"E_SOURCE_IMPORT"}),
        (b"\ndef injected_eval():\n    return eval('1')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_exec():\n    return os.system('whoami')\n", {"E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef sha256(raw):\n    return '0' * 64\n", {"E_SOURCE_DUPLICATE_FUNCTION"}),
        (b"\ndef injected_subprocess():\n    return subprocess.run(['python', 'Claude/forbidden.py'])\n", {"E_SOURCE_SUBPROCESS_BYPASS"}),
        (b"\ndef injected_subprocess_alias():\n    danger = subprocess.run\n    return danger(['python', 'Claude/forbidden.py'])\n", {"E_SOURCE_SUBPROCESS_BYPASS"}),
        (b"\ndef injected_getattr():\n    return getattr(os, 'system')('whoami')\n", {"E_SOURCE_FORBIDDEN_CALL", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_popen():\n    return subprocess.Popen(['python', 'Claude/forbidden.py'])\n", {"E_SOURCE_SUBPROCESS_BYPASS", "E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_run_process():\n    return run_process(['python', 'Claude/forbidden.py'])\n", {"E_SOURCE_RUN_PROCESS_BYPASS"}),
        (b"\ndef injected_write():\n    return (ROOT / 'Claude/forbidden.txt').write_bytes(b'x')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_delete():\n    return shutil.rmtree(ROOT / 'Claude')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_replace():\n    return os.replace(ROOT / 'x', ROOT / 'Claude/y')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_run_alias():\n    danger = run_process\n    return danger(['python'])\n", {"E_SOURCE_CALLABLE_ALIAS"}),
        (b"\ndef injected_git_alias():\n    return git(['-c', 'alias.x=!python Claude/forbidden.py', 'x'])\n", {"E_SOURCE_GIT_CALLSITE", "E_SOURCE_GIT_COMMAND", "E_SOURCE_GIT_ESCAPE"}),
        (b"\nimport subprocess as sp\n", {"E_SOURCE_IMPORT_ALIAS"}),
        (b"\ndef injected_dynamic_git():\n    argv = ['-c', 'alias.x=!python Claude/forbidden.py', 'x']\n    return git(argv)\n", {"E_SOURCE_GIT_CALLSITE", "E_SOURCE_GIT_DYNAMIC_ARGV"}),
        (b"\ndef injected_git_text():\n    return git_text(['-c', 'alias.x=!python Claude/forbidden.py', 'x'])\n", {"E_SOURCE_GIT_CALLSITE", "E_SOURCE_GIT_COMMAND", "E_SOURCE_GIT_ESCAPE"}),
        (b"\ndef injected_path_open():\n    return (ROOT / 'Claude/x').open('wb').write(b'x')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_os_open():\n    fd = os.open(ROOT / 'Claude/x', 1)\n    return os.write(fd, b'x')\n", {"E_SOURCE_FILESYSTEM_MUTATOR", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_spawn():\n    return os.spawnv(0, 'python', ['python'])\n", {"E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_copyfile():\n    return shutil.copyfile(ROOT / 'x', ROOT / 'Claude/y')\n", {"E_SOURCE_FILESYSTEM_MUTATOR", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_module_launder():\n    danger = (lambda x: x)(subprocess)\n    return danger.run(['python'])\n", {"E_SOURCE_SUBPROCESS_BYPASS"}),
        (b"\ndef injected_gitdir_shell():\n    return git(['--git-dir', '.', 'shell'])\n", {"E_SOURCE_GIT_CALLSITE", "E_SOURCE_GIT_COMMAND"}),
        (b"\ndef injected_git_text_alias():\n    danger = git_text\n    return danger(['status'])\n", {"E_SOURCE_CALLABLE_ALIAS"}),
        (b"\ndef clear_readonly():\n    return (ROOT / 'Claude/forbidden.txt').write_bytes(b'x')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_git_blob():\n    return git_blob('--output=Claude/forbidden', 'x')\n", {"E_SOURCE_GIT_CALLSITE"}),
        (b"\ndef injected_named_temp():\n    return tempfile.NamedTemporaryFile(dir=ROOT / 'Claude', delete=False)\n", {"E_SOURCE_FILESYSTEM_MUTATOR", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_symlink():\n    return os.symlink(ROOT / 'x', ROOT / 'Claude/y')\n", {"E_SOURCE_FILESYSTEM_MUTATOR", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_callable_launder():\n    return (lambda value: value)(git)(['status'])\n", {"E_SOURCE_CALLABLE_ALIAS"}),
        (b"\ndef injected_module_launder_os():\n    return (lambda value: value)(os).remove(ROOT / 'Claude/x')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_dunder_getattribute():\n    return (ROOT / 'Claude/x').__getattribute__('write_bytes')(b'x')\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\ndef injected_os_utime():\n    return os.utime(ROOT / 'Claude/x')\n", {"E_SOURCE_FILESYSTEM_MUTATOR", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_unpack_archive():\n    return shutil.unpack_archive('x.zip', ROOT / 'Claude')\n", {"E_SOURCE_FILESYSTEM_MUTATOR", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_eval_launder():\n    return (lambda value: value)(eval)('1')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_eval_alias():\n    danger = eval\n    return danger('1')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_builtins_eval():\n    return __builtins__['eval']('1')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_import_subprocess():\n    return (lambda value: value)(__import__)('subprocess').run(['python'])\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_import_os():\n    return (lambda value: value)(__import__)('os').remove(ROOT / 'Claude/x')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_pathlib_os():\n    return pathlib.os.remove(ROOT / 'Claude/x')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_tempfile_os():\n    return tempfile._os.remove(ROOT / 'Claude/x')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_tempfile_shutil():\n    return tempfile._shutil.rmtree(ROOT / 'Claude')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_shutil_os():\n    return shutil.os.makedirs(ROOT / 'Claude/x')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_function_globals():\n    return sha256.__globals__['__builtins__']['eval']('1')\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\ndef injected_posix_spawn():\n    return os.posix_spawn('python', ['python'], {})\n", {"E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_posix_spawnp():\n    return os.posix_spawnp('python', ['python'], {})\n", {"E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_fork():\n    return os.fork()\n", {"E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_forkpty():\n    return os.forkpty()\n", {"E_SOURCE_EXECUTION_ESCAPE", "E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_environ():\n    return os.environ.__setitem__('GIT_CONFIG_COUNT', '1')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_class_chain():\n    return ().__class__.__base__.__subclasses__()\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\ndef injected_object_subclasses():\n    return object.__subclasses__()\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\ndef injected_function_code():\n    return sha256.__code__\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\ndef injected_function_builtins():\n    return sha256.__builtins__['eval']('1')\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\nclass InjectedOwner:\n    def repository_snapshot(self):\n        return git(['status'])\n", {"E_SOURCE_GIT_CALLSITE"}),
        (b"\ndef injected_path_move():\n    return (ROOT / 'x').move(ROOT / 'Claude/y')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_path_link_to():\n    return (ROOT / 'x').link_to(ROOT / 'Claude/y')\n", {"E_SOURCE_FILESYSTEM_MUTATOR"}),
        (b"\ndef injected_argparse_os():\n    return argparse._os.remove(ROOT / 'Claude/x')\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_json_module_launder():\n    return (lambda value: value)(json)\n", {"E_SOURCE_MODULE_BYPASS"}),
        (b"\ndef injected_loader_os():\n    return __loader__.load_module('os').remove(ROOT / 'Claude/x')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_spec_subprocess():\n    return __spec__.loader.load_module('subprocess').run(['python'])\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_loader_builtins():\n    return __loader__.load_module('builtins').eval('1')\n", {"E_SOURCE_FORBIDDEN_CALL"}),
        (b"\ndef injected_generator_builtins():\n    return (x for x in ()).gi_frame.f_builtins['eval']('1')\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
        (b"\ndef injected_generator_globals():\n    return (x for x in ()).gi_frame.f_globals['__builtins__']['__import__']('os').remove(ROOT / 'Claude/x')\n", {"E_SOURCE_EXECUTION_ESCAPE"}),
    ]
    passed = 0
    for suffix, wanted in cases:
        observed = source_policy_diagnostics(lf_bytes(raw) + suffix)
        require(observed == wanted, "E_SOURCE_POLICY_NEGATIVE", f"{sorted(observed)}!={sorted(wanted)}")
        passed += 1
    replacements = [
        (
            b"def lf_bytes(raw: bytes) -> bytes:\n    return raw.replace(b\"\\r\\n\", b\"\\n\").replace(b\"\\r\", b\"\\n\")\n",
            b"def lf_bytes(raw: bytes) -> bytes:\n    os.replace(ROOT / 'x', ROOT / 'Claude/y')\n    return raw.replace(b\"\\r\\n\", b\"\\n\").replace(b\"\\r\", b\"\\n\")\n",
        ),
        (
            b"        temp_path.write_bytes(raw)\n",
            b"        (ROOT / 'Claude/forbidden.txt').write_bytes(raw)\n",
        ),
    ]
    for before, after in replacements:
        require(raw.count(before) == 1, "E_SOURCE_POLICY_REPLACEMENT_ANCHOR")
        observed = source_policy_diagnostics(raw.replace(before, after))
        require(observed == {"E_SOURCE_PINNED_CALLSITE"}, "E_SOURCE_POLICY_PIN_NEGATIVE", repr(sorted(observed)))
        passed += 1
    return passed, len(cases) + len(replacements)


def remove_temp_tree(path: pathlib.Path, prefix: str) -> None:
    resolved = path.resolve()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    require(resolved.parent == temp_root and resolved.name.startswith(prefix), "E_TEMP_BOUNDARY", str(resolved))

    def clear_readonly(function: Callable[..., Any], target: str, _: Any) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(resolved, onerror=clear_readonly)


def make_git_fixture() -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, str, str]:
    prefix = "phase065-plan-git-"
    root = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    work = root / "work"
    origin = root / "origin.git"
    try:
        work.mkdir()
        git(["init", "--initial-branch=main"], cwd=work)
        git(["config", "user.email", "phase065@example.invalid"], cwd=work)
        git(["config", "user.name", "Phase 065 Fixture"], cwd=work)
        git(["config", "core.autocrlf", "false"], cwd=work)
        (work / "base.txt").write_bytes(b"base\n")
        (work / "Claude").mkdir()
        (work / "Claude" / "keep.txt").write_bytes(b"protected\n")
        for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH):
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"old\n")
        (work / "outside.txt").write_bytes(b"outside\n")
        git(["add", "base.txt", "outside.txt", "Claude/keep.txt", PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH], cwd=work)
        git(["commit", "-m", "base"], cwd=work)
        base = git_text(["rev-parse", "HEAD"], cwd=work)
        git(["branch", PROTECTED_BRANCH, base], cwd=work)
        git(["branch", ACTIVE_BRANCH, base], cwd=work)
        git(["switch", "-c", "fixture/drift", base], cwd=work)
        git(["commit", "--allow-empty", "-m", "drift"], cwd=work)
        drift = git_text(["rev-parse", "HEAD"], cwd=work)
        git(["switch", ACTIVE_BRANCH], cwd=work)
        git(["init", "--bare", str(origin)], cwd=root)
        git(["remote", "add", "origin", str(origin)], cwd=work)
        git(["push", "origin", "main", PROTECTED_BRANCH, "fixture/drift"], cwd=work)
        git(["push", "-u", "origin", ACTIVE_BRANCH], cwd=work)
        git(["fetch", "origin"], cwd=work)
        git(["branch", "-D", "main"], cwd=work)
        for path in FINAL_PATHS:
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((path + "\n").encode("utf-8"))
        git(["add", "--", *FINAL_PATHS], cwd=work)
    except Exception:
        remove_temp_tree(root, prefix)
        raise
    return root, work, origin, base, drift


def fixture_snapshot(work: pathlib.Path, origin: pathlib.Path) -> dict[str, Any]:
    return {
        "branch": git_text(["branch", "--show-current"], cwd=work),
        "head": git_text(["rev-parse", "HEAD"], cwd=work),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"], cwd=work),
        "upstream": git_text(["rev-parse", "@{upstream}"], cwd=work),
        "origin_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"], cwd=work),
        "live_active": git_text(["--git-dir", str(origin), "rev-parse", f"refs/heads/{ACTIVE_BRANCH}"], cwd=work),
        "local_protected": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=work),
        "origin_protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"], cwd=work),
        "live_protected": git_text(["--git-dir", str(origin), "rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=work),
        "origin_main": git_text(["rev-parse", "refs/remotes/origin/main"], cwd=work),
        "live_main": git_text(["--git-dir", str(origin), "rev-parse", "refs/heads/main"], cwd=work),
        "staged_status": name_status_map(git(["diff", "--cached", "--no-renames", "--name-status", "-z"], cwd=work).stdout),
        "unstaged_status": name_status_map(git(["diff", "--no-renames", "--name-status", "-z"], cwd=work).stdout),
        "untracked": nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=work).stdout),
        "claude_dirty": bool(git(["status", "--porcelain=v1", "--", "Claude"], cwd=work).stdout),
        "local_main_absent": git(["show-ref", "--verify", "--quiet", "refs/heads/main"], cwd=work, check=False).returncode != 0,
        "diff_check": git(["diff", "--cached", "--check"], cwd=work, check=False).returncode == 0,
    }


def fixture_diagnostics(snapshot: dict[str, Any], active: str, protected: str, main: str) -> set[str]:
    checks = (
        ("E_GIT_BRANCH", snapshot["branch"] == ACTIVE_BRANCH),
        ("E_GIT_UPSTREAM_NAME", snapshot["upstream_name"] == f"origin/{ACTIVE_BRANCH}"),
        ("E_GIT_HEAD", snapshot["head"] == active),
        ("E_GIT_UPSTREAM", snapshot["upstream"] == active),
        ("E_GIT_ACTIVE_TRACKING", snapshot["origin_active"] == active),
        ("E_GIT_ACTIVE_LIVE", snapshot["live_active"] == active),
        ("E_GIT_LOCAL_PROTECTED", snapshot["local_protected"] == protected),
        ("E_GIT_PROTECTED_TRACKING", snapshot["origin_protected"] == protected),
        ("E_GIT_PROTECTED_LIVE", snapshot["live_protected"] == protected),
        ("E_GIT_MAIN_TRACKING", snapshot["origin_main"] == main),
        ("E_GIT_MAIN_LIVE", snapshot["live_main"] == main),
        ("E_GIT_LOCAL_MAIN", snapshot["local_main_absent"] is True),
        ("E_GIT_STAGED_STATUS", snapshot["staged_status"] == FINAL_STATUS),
        ("E_GIT_UNSTAGED", not snapshot["unstaged_status"]),
        ("E_GIT_UNTRACKED", not snapshot["untracked"]),
        ("E_GIT_CLAUDE", not snapshot["claude_dirty"]),
        ("E_GIT_DIFF_CHECK", snapshot["diff_check"] is True),
    )
    return {code for code, passed in checks if not passed}


def fixture_delete_allowlisted(work: pathlib.Path, _: pathlib.Path, __: str, ___: str) -> None:
    git(["rm", "--cached", "--", PLAN_PATH], cwd=work)
    (work / PLAN_PATH).unlink()


def fixture_rename_escape(work: pathlib.Path, _: pathlib.Path, __: str, ___: str) -> None:
    git(["rm", "--cached", "--", PLAN_PATH], cwd=work)
    (work / PLAN_PATH).unlink()
    git(["mv", "outside.txt", PLAN_PATH], cwd=work)


def fixture_wrong_status(work: pathlib.Path, _: pathlib.Path, __: str, ___: str) -> None:
    git(["rm", "-f", "--", PARENT_LEDGER_PATH], cwd=work)


def run_git_controls() -> tuple[int, int]:
    cases: list[tuple[set[str], Callable[[pathlib.Path, pathlib.Path, str, str], None]]] = [
        ({"E_GIT_BRANCH"}, lambda w, o, b, d: git(["branch", "-m", "fixture/wrong"], cwd=w)),
        ({"E_GIT_UPSTREAM_NAME", "E_GIT_UPSTREAM"}, lambda w, o, b, d: git(["branch", "--set-upstream-to=origin/fixture/drift", ACTIVE_BRANCH], cwd=w)),
        ({"E_GIT_HEAD"}, lambda w, o, b, d: git(["update-ref", f"refs/heads/{ACTIVE_BRANCH}", d], cwd=w)),
        ({"E_GIT_UPSTREAM", "E_GIT_ACTIVE_TRACKING"}, lambda w, o, b, d: git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", d], cwd=w)),
        ({"E_GIT_ACTIVE_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", f"refs/heads/{ACTIVE_BRANCH}", d], cwd=w)),
        ({"E_GIT_LOCAL_PROTECTED"}, lambda w, o, b, d: git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", d], cwd=w)),
        ({"E_GIT_PROTECTED_TRACKING"}, lambda w, o, b, d: git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", d], cwd=w)),
        ({"E_GIT_PROTECTED_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", f"refs/heads/{PROTECTED_BRANCH}", d], cwd=w)),
        ({"E_GIT_MAIN_TRACKING"}, lambda w, o, b, d: git(["update-ref", "refs/remotes/origin/main", d], cwd=w)),
        ({"E_GIT_MAIN_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", "refs/heads/main", d], cwd=w)),
        ({"E_GIT_LOCAL_MAIN"}, lambda w, o, b, d: git(["branch", "main", b], cwd=w)),
        ({"E_GIT_UNSTAGED", "E_GIT_CLAUDE"}, lambda w, o, b, d: (w / "Claude" / "keep.txt").write_bytes(b"mutated\n")),
        ({"E_GIT_STAGED_STATUS"}, lambda w, o, b, d: ((w / "extra.txt").write_bytes(b"x\n"), git(["add", "extra.txt"], cwd=w))),
        ({"E_GIT_STAGED_STATUS"}, fixture_delete_allowlisted),
        ({"E_GIT_STAGED_STATUS"}, fixture_rename_escape),
        ({"E_GIT_STAGED_STATUS"}, fixture_wrong_status),
        ({"E_GIT_UNTRACKED"}, lambda w, o, b, d: (w / "extra.txt").write_bytes(b"x\n")),
        ({"E_GIT_UNSTAGED"}, lambda w, o, b, d: (w / FINAL_PATHS[0]).write_bytes(b"mutated\n")),
        ({"E_GIT_DIFF_CHECK"}, lambda w, o, b, d: ((w / FINAL_PATHS[0]).write_bytes(b"bad-space \n"), git(["add", FINAL_PATHS[0]], cwd=w))),
    ]
    passed = 0
    for wanted, mutation in cases:
        root, work, origin, base, drift = make_git_fixture()
        try:
            require(not fixture_diagnostics(fixture_snapshot(work, origin), base, base, base), "E_GIT_BASELINE")
            mutation(work, origin, base, drift)
            observed = fixture_diagnostics(fixture_snapshot(work, origin), base, base, base)
            require(observed == wanted, "E_GIT_DIAGNOSTIC", f"{sorted(observed)}!={sorted(wanted)}")
            passed += 1
        finally:
            remove_temp_tree(root, "phase065-plan-git-")
    return passed, len(cases)


def persistence_diagnostics(expected_commit: str) -> set[str]:
    snapshot = repository_snapshot()
    failures = ref_diagnostics(snapshot, expected_commit)
    if snapshot["staged_status"] or snapshot["unstaged_status"] or snapshot["untracked"]:
        failures.add("E_PERSISTENCE_DIRTY")
    if git_text(["rev-parse", f"{expected_commit}^"]) != EXPECTED_PARENT:
        failures.add("E_PERSISTENCE_PARENT")
    if git_text(["show", "-s", "--format=%s", expected_commit]) != EXPECTED_SUBJECT:
        failures.add("E_PERSISTENCE_SUBJECT")
    status = name_status_map(git(["diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-r", "-z", expected_commit]).stdout)
    if status != FINAL_STATUS:
        failures.add("E_PERSISTENCE_PATHS")
    for path in FINAL_PATHS:
        if git_blob(expected_commit, path) != (ROOT / path).read_bytes():
            failures.add("E_PERSISTENCE_BYTES")
    return failures


def atomic_collect(raw: bytes) -> None:
    require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE")
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST")
    temp_path = OUTPUT.with_name(OUTPUT.name + ".tmp-p065-plan")
    require(not temp_path.exists(), "E_TEMP_EXISTS")
    try:
        temp_path.write_bytes(raw)
        strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        os.replace(temp_path, OUTPUT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(OUTPUT.read_bytes() == raw, "E_OUTPUT_WRITE")


def read_stored() -> tuple[dict[str, Any], bytes, int]:
    require(OUTPUT.is_file(), "E_VALIDATION_ARTIFACT_MISSING", OUTPUT_PATH)
    raw = OUTPUT.read_bytes()
    document, traversal = strict_load_bytes(raw, OUTPUT_PATH)
    require(canonical_bytes(document) == lf_bytes(raw), "E_OUTPUT_CANONICAL")
    return document, raw, traversal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    require(sum((args.collect, args.content_only, args.verify_staged, args.verify_persistence)) == 1, "E_CLI_MODE")
    if not args.collect and not OUTPUT.exists():
        raise ValidationError("E_VALIDATION_ARTIFACT_MISSING", OUTPUT_PATH)
    first = build_payload()
    second = build_payload()
    first_raw = canonical_bytes(first)
    second_raw = canonical_bytes(second)
    require(first_raw == second_raw, "E_DETERMINISM", "2/2")
    if args.collect:
        validate_worktree(set(NONSELF_PATHS), staged=False)
        negative_passed, negative_total = run_negative_controls(first)
        source_passed, source_total = run_source_policy_controls(VALIDATOR.read_bytes())
        git_passed, git_total = run_git_controls()
        require(git_total == 19, "E_GIT_CONTROL_COUNT", str(git_total))
        first_raw = canonical_bytes(first)
        atomic_collect(first_raw)
        print(f"PASS_P065_PLAN_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print(f"PASS_P065_PLAN_SOURCE_POLICY {source_passed}/{source_total} self_hash=PINNED")
        print("PASS_P065_PLAN_DETERMINISM 2/2")
        print("PASS_P065_PLAN_ACTIVATION collect=JSON_LAST result_first=true occurrences=261 unique_blobs=131")
        return 0
    stored, stored_raw, traversal = read_stored()
    expected = first
    expected_raw = canonical_bytes(expected)
    diagnostics = document_diagnostics(stored, expected)
    require(not diagnostics, "E_STORED_DOCUMENT", repr(sorted(diagnostics)))
    require(stored_raw == expected_raw, "E_STORED_BYTES")
    full = args.verify_staged or args.verify_persistence
    if args.run_negative_probes or full:
        negative_passed, negative_total = run_negative_controls(stored)
        source_passed, source_total = run_source_policy_controls(VALIDATOR.read_bytes())
        git_passed, git_total = run_git_controls()
        print(f"PASS_P065_PLAN_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print(f"PASS_P065_PLAN_SOURCE_POLICY {source_passed}/{source_total} self_hash=PINNED")
    if args.determinism_check or full:
        print("PASS_P065_PLAN_DETERMINISM 2/2")
    if args.content_only:
        validate_worktree(FINAL_PATH_SET, staged=False)
        print(f"PASS_P065_PLAN_CONTENT occurrences=261 unique_blobs=131 strict_nodes={traversal}")
    elif args.verify_staged:
        validate_worktree(FINAL_PATH_SET, staged=True)
        print("PASS_P065_PLAN_ACTIVATION_STAGED exact-seven=7/7")
    else:
        require(args.expected_commit is not None and re.fullmatch(r"[0-9a-f]{40}", args.expected_commit) is not None, "E_EXPECTED_COMMIT")
        failures = persistence_diagnostics(args.expected_commit)
        require(not failures, "E_PERSISTENCE_CONTRACT", repr(sorted(failures)))
        print(f"{PERSISTENCE} commit={args.expected_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ValidationError, KeyError, IndexError, TypeError, ValueError, OSError,
        UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired,
    ) as error:
        code = error.code if isinstance(error, ValidationError) else type(error).__name__
        print(f"FAIL_P065_PLAN_CONTENT {code}: {error}")
        raise SystemExit(1)
