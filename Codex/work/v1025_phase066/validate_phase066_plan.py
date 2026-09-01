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
import subprocess
import tempfile
from collections import Counter
from collections.abc import Callable
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
PLAN_PATH = "Codex/plans/2026-09-01-phase066-v1025-v1025_2-lineage-detailed-plan.md"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_plan.py"
OUTPUT_PATH = "Codex/results/PHASE_066_PLAN_ACTIVATION_VALIDATION.json"
RESULT_PATH = "Codex/results/PHASE_066_PLAN_ACTIVATION_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
PREDECESSOR_VALIDATOR_PATH = "Codex/work/v1024_phase065/validate_phase065_final.py"
PREDECESSOR_JSON_PATH = "Codex/results/PHASE_065_VALIDATION.json"

PLAN = ROOT / PLAN_PATH
VALIDATOR = ROOT / VALIDATOR_PATH
OUTPUT = ROOT / OUTPUT_PATH

EXPECTED_PARENT = "a2920fba07ab9ce75191134f0d68ed3b6ffda4e5"
EXPECTED_PARENT_PARENT = "26e2ce9559220d5782e1303d68b4449a36309e94"
EXPECTED_PARENT_SUBJECT = "audit(phase065): close v1024 lineage gate"
EXPECTED_SUBJECT = "docs(phase066): plan v1025 lineage reaudit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
GATE = "PASS_P066_PLAN_ACTIVATION"
PERSISTENCE = "PASS_P066_PLAN_ACTIVATION_PERSISTENCE"

MANIFEST_SHA256_LF = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
PATH_SET_SHA256 = "3c9bf954a5db4df5ce01a96ff8834f9e9284e6e35fdcecbfae0c3ae6b430b382"
PATH_BLOB_SHA256 = "b3620bf1a76758cad818e9ea7ece5441ea88b86f8f030bb715f48e054086655c"
UNIQUE_BLOB_SHA256 = "f1982cf050f88b7145d5ea1a6afdf124316da1332afec9028ae6119730080bfa"
PROCESS_SHA256_LF = "f09417ef085ee7139fa11869f6f123937d6492dcc53d1f0b51e71a2c8a124860"
ROUTED_PROCESS_SHA256_LF = "57062f623809de1f3fb66b8241117363a0ec18626bc58a40f4f0e41cbed93418"
PREDECESSOR_VALIDATOR_SHA256 = "e7daf416b6d437e75ebb6a51ec3e93e443f9dba54c3ed8956db746cbfc04dd08"
PREDECESSOR_JSON_SHA256 = "2363a35208642220fdbe133f5db99a9cbdc4263d43d2347c59b1590339e0db84"
PREDECESSOR_SEMANTIC_SHA256 = "47f876ba0f033cda9e9bc94233b4e2f42303e90d6fb87c80246358ec0d2b3de6"
SOURCE_POLICY_SHA256_LF = "9c7c43abfe3ed11443cdbeb523231a725756717d5aa7ba67a5f8683b535fbc71"

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
    (
        "Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md",
        "c471f29944d766588b71dc026bc179f84f419e95",
        240,
        "aff3e9089026dc50ee1923515c7545c800a2ea1add5152f9a86806fc2b29b382",
    ),
    (
        "Claude/results/HANDOVER_v1025_2_CARRYOVER.md",
        "76c248e76430dbfcd3915b4cbebadce46a5d3593",
        415,
        "84116f4ce35303aaffd5ff0173505c658799485b9cd7d4930a05b8a77b91e66c",
    ),
]

REQUIRED_HEADINGS = [
    "## Summary",
    "## Current Ground Truth",
    "## Phase Range",
    "## Exact Read Inputs",
    "## Non-goals and Scope Guards",
    "## Implementation Changes",
    "## Plan Activation Unit — Save Before Step 76",
    "## Phase 066 — v1.0.25/v1.0.25.2 Reaudit",
    "## Phase Gate",
    "## Implementation Interfaces",
    "## Test and Validation Plan",
    "## Stop Conditions",
    "## Assumptions",
    "## Correction History",
]
REQUIRED_PLAN_TOKENS = [
    "433", "167", "30,597", "308", "26,391,541", "12,483,701",
    "Step 76", "Step 77", "Step 78", "Step 79", "Step 80", "Step 81",
    "PASS_P066_LINEAGE_I", "CONDITIONAL_P065", "FAIL_P066",
    "result-first", "validation-JSON-last", "fresh import", "direct-14",
    "eight-digit", "optimizer state", "4+2", "7+7", "temperature dependence",
    "empirical", "physical authority", "v1.0.26A", "v1.0.26B",
    "comparison", "not a release", "stale", "N10", "background",
    "GROUND_NOT_FOUND", "no source", "no code",
]
CONTROL_TOKENS = {
    RESULT_PATH: [
        GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", EXPECTED_PARENT, EXPECTED_SUBJECT,
        "A/A/A/A/M/M/M", "CONDITIONAL_P065", "Step 76",
    ],
    PARENT_LEDGER_PATH: [
        "Phase 066", "76–81", "PASS_PENDING_PERSISTENCE",
        EXPECTED_PARENT, "CONDITIONAL_P065",
    ],
    ACTIVE_LEDGER_PATH: [
        "Phase 066", "76–81", "PASS_PENDING_PERSISTENCE",
        "PASS_P066_LINEAGE_I", EXPECTED_PARENT,
    ],
    HANDOVER_PATH: [
        "Phase 066", "Step 76", "PASS_PENDING_PERSISTENCE",
        EXPECTED_PARENT, EXPECTED_SUBJECT, "CONDITIONAL_P065",
    ],
}
LEDGER_PHASE066_ROW_TOKENS = {
    PARENT_LEDGER_PATH: [
        "| 066 | 76–81 | plan activation | lineage I |",
        "| PASS_PENDING_PERSISTENCE |", PLAN_PATH, RESULT_PATH, OUTPUT_PATH,
        VALIDATOR_PATH, GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", PERSISTENCE,
        "exact-seven activation commit/push/persistence before Step 76",
    ],
    ACTIVE_LEDGER_PATH: [
        "| 066 | 76–81 | plan activation |",
        "| PASS_PENDING_PERSISTENCE |", PLAN_PATH, RESULT_PATH, OUTPUT_PATH,
        VALIDATOR_PATH, GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", PERSISTENCE,
        "PASS_P066_LINEAGE_I", "CONDITIONAL_P066", "FAIL_P066",
        "exact-seven activation commit/push/persistence before Step 76",
    ],
}

ALLOWED_IMPORT_ROOTS = frozenset({
    "__future__", "argparse", "ast", "collections", "copy", "hashlib", "json",
    "math", "os", "pathlib", "re", "shutil", "subprocess", "tempfile", "typing",
})


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


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


def predecessor_semantic_hash(document: dict[str, Any]) -> str:
    candidate = copy.deepcopy(document)
    candidate.pop("semantic_sha256", None)
    raw = json.dumps(
        candidate, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    return sha256(raw)


def reject_constant(value: str) -> None:
    raise ValidationError("E_JSON_NONFINITE", value)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def inspect_json_value(value: Any, depth: int = 0) -> tuple[int, int]:
    require(depth <= 32, "E_JSON_DEPTH", str(depth))
    if isinstance(value, float):
        require(math.isfinite(value), "E_JSON_NONFINITE", repr(value))
    if isinstance(value, dict):
        count = 1
        maximum = depth
        for key, item in value.items():
            require(type(key) is str, "E_JSON_KEY", repr(key))
            child_count, child_depth = inspect_json_value(item, depth + 1)
            count += child_count
            maximum = max(maximum, child_depth)
        return count, maximum
    if isinstance(value, list):
        count = 1
        maximum = depth
        for item in value:
            child_count, child_depth = inspect_json_value(item, depth + 1)
            count += child_count
            maximum = max(maximum, child_depth)
        return count, maximum
    require(value is None or type(value) in {str, int, float, bool}, "E_JSON_TYPE", str(type(value)))
    return 1, depth


def strict_load_bytes(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValidationError("E_JSON_UTF8", label) from error
    try:
        document = json.loads(text, object_pairs_hook=reject_pairs, parse_constant=reject_constant)
    except json.JSONDecodeError as error:
        raise ValidationError("E_JSON_SYNTAX", f"{label}:{error.msg}") from error
    require(type(document) is dict, "E_JSON_ROOT", label)
    nodes, depth = inspect_json_value(document)
    return document, nodes, depth


def is_within_temp(path: pathlib.Path) -> bool:
    try:
        path.resolve().relative_to(pathlib.Path(tempfile.gettempdir()).resolve())
    except (OSError, ValueError):
        return False
    return True


def validate_git_argv(argv: list[str], cwd: pathlib.Path = ROOT) -> None:
    require(bool(argv) and argv[0] in {"git", "git.exe"}, "E_SOURCE_POLICY_GIT_LAUNCHER", repr(argv))
    args = argv[1:]
    require(bool(args), "E_SOURCE_POLICY_GIT", "missing subcommand")
    git_dir: pathlib.Path | None = None
    if args[0] == "--git-dir":
        require(len(args) >= 3, "E_SOURCE_POLICY_GIT", repr(argv))
        git_dir = pathlib.Path(args[1])
        require(git_dir.is_absolute() and is_within_temp(git_dir), "E_SOURCE_POLICY_GIT", repr(argv))
        subcommand = args[2]
        subargs = args[3:]
    else:
        subcommand = args[0]
        subargs = args[1:]
    allowed = {
        "add", "branch", "checkout", "clone", "commit", "config", "diff", "diff-tree",
        "init", "log", "ls-files", "ls-remote", "mv", "rev-parse", "rm", "show",
        "show-ref", "status", "update-ref",
    }
    require(subcommand in allowed, "E_SOURCE_POLICY_GIT", repr(argv))
    lowered = [item.lower() for item in args]
    forbidden = {"--config-env", "--upload-pack", "--receive-pack", "--exec-path"}
    require(not any(
        item in forbidden or any(item.startswith(prefix + "=") for prefix in forbidden)
        or item.startswith(("alias.", "protocol.")) or "ext::" in item
        for item in lowered
    ), "E_SOURCE_POLICY_GIT", repr(argv))
    mutating = {"add", "branch", "checkout", "clone", "commit", "config", "init", "mv", "rm", "update-ref"}
    if subcommand == "config":
        require(tuple(args) in {
            ("config", "core.autocrlf", "false"),
            ("config", "user.email", "phase066-fixture@example.invalid"),
            ("config", "user.name", "Phase 066 Fixture"),
        }, "E_SOURCE_POLICY_GIT", repr(argv))
    if subcommand == "clone":
        require(not any(
            item == "-u" or item == "-c" or item.startswith(("-u", "-c", "--config"))
            for item in subargs
        ), "E_SOURCE_POLICY_GIT", repr(argv))
    if subcommand == "branch":
        require(not any(item in {"-d", "-D", "--delete"} for item in subargs), "E_SOURCE_POLICY_GIT", repr(argv))
    if subcommand == "checkout":
        require(not any(item in {"-f", "--force"} for item in subargs), "E_SOURCE_POLICY_GIT", repr(argv))
    if subcommand == "ls-remote":
        require(len(subargs) == 2 and subargs[0] == "origin" and subargs[1].startswith("refs/heads/"),
                "E_SOURCE_POLICY_GIT", repr(argv))
    if subcommand == "update-ref":
        require("-d" not in subargs, "E_SOURCE_POLICY_GIT", repr(argv))
    read_only_branch_query = subcommand == "branch" and subargs == ["--show-current"]
    if subcommand in mutating and not read_only_branch_query:
        boundary = git_dir if git_dir is not None else cwd
        require(is_within_temp(boundary), "E_SOURCE_POLICY_GIT_MUTATION_BOUNDARY", repr(argv))


def run_process(
    argv: list[str], *, cwd: pathlib.Path = ROOT, timeout: int = 300, check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    validate_git_argv(argv, cwd)
    process = subprocess.run(
        argv, cwd=cwd, capture_output=True, timeout=timeout, check=False, shell=False,
    )
    if check and process.returncode != 0:
        raise ValidationError(
            "E_PROCESS",
            f"{argv!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}",
        )
    return process


def git(args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, check=check)


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT) -> str:
    return git(args, cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str, *, cwd: pathlib.Path = ROOT) -> bytes:
    return git(["show", f"{commit}:{path}"], cwd=cwd).stdout


def live_tip(branch: str) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"]).splitlines()
    require(len(lines) == 1, "E_GIT_LIVE_REF", branch)
    return lines[0].split("\t", 1)[0]


def attribute_chain(node: ast.AST) -> tuple[str, ...]:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return tuple(reversed(parts))
    return ()


def sensitive_reference(node: ast.AST) -> bool:
    if isinstance(node, ast.Name):
        return node.id in {"git", "run_process", "open", "os", "pathlib", "shutil", "subprocess", "tempfile"}
    if isinstance(node, ast.Call):
        return attribute_chain(node.func) == ("sys", "modules", "get")
    if isinstance(node, ast.Subscript):
        chain = attribute_chain(node.value)
        return bool(chain and chain[0] in {"os", "pathlib", "shutil", "subprocess", "sys", "tempfile"})
    if isinstance(node, ast.Attribute):
        chain = attribute_chain(node)
        return bool(chain and chain[0] in {"os", "pathlib", "shutil", "subprocess", "sys", "tempfile"})
    return False


def validate_source_policy_text(source: str, filename: str) -> None:
    tree = ast.parse(source, filename=filename)
    parents = {id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    top_names = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    require(len(top_names) == len(set(top_names)), "E_SOURCE_POLICY_DUPLICATE_OWNER", repr(top_names))
    owner_by_node: dict[int, str] = {}
    outer_by_node: dict[int, str] = {}

    def assign_scope(node: ast.AST, owner: str, outer: str) -> None:
        owner_by_node[id(node)] = owner
        outer_by_node[id(node)] = outer
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                assign_scope(child, f"<nested:{child.name}>", outer)
            elif isinstance(child, ast.Lambda):
                assign_scope(child, "<lambda>", outer)
            else:
                assign_scope(child, owner, outer)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assign_scope(node, node.name, node.name)

    run_process_owners = {"git"}
    git_owners = {
        "git_text", "git_blob", "live_tip", "repository_snapshot", "supplemental_contract",
        "process_contract", "validate_worktree", "validate_persistence", "make_git_boundary_fixture",
        "validate_index_worktree", "fixture_snapshot", "fixture_delete_allowlisted", "fixture_rename_escape",
        "fixture_wrong_status", "run_git_boundary_controls",
    }
    git_text_owners = {
        "live_tip", "repository_snapshot", "supplemental_contract", "make_git_boundary_fixture",
        "fixture_snapshot", "validate_persistence",
    }
    git_blob_owners = {"supplemental_contract", "validate_persistence"}
    live_tip_owners = {"repository_snapshot"}
    filesystem_owners = {
        "make_git_boundary_fixture", "fixture_delete_allowlisted", "fixture_rename_escape",
        "run_git_boundary_controls", "remove_temp_tree", "atomic_collect",
    }
    subprocess_count = 0
    prohibited_path_methods = {
        "chmod", "hardlink_to", "link_to", "mkdir", "open", "rename", "replace", "rmdir",
        "symlink_to", "touch", "unlink", "write_bytes", "write_text",
    }

    for node in ast.walk(tree):
        owner = owner_by_node.get(id(node))
        outer = outer_by_node.get(id(node))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            defaults = list(node.args.defaults) + [value for value in node.args.kw_defaults if value is not None]
            require(not any(sensitive_reference(child) for default in defaults for child in ast.walk(default)),
                    "E_SOURCE_POLICY_DEFAULT", ast.dump(node, include_attributes=False))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            roots = {name.split(".", 1)[0] for name in modules}
            require(roots <= ALLOWED_IMPORT_ROOTS, "E_SOURCE_POLICY_IMPORT_ALLOWLIST", repr(sorted(roots)))
            require(all(alias.asname is None for alias in node.names), "E_SOURCE_POLICY_IMPORT_ALIAS",
                    ast.dump(node, include_attributes=False))
            require(not (isinstance(node, ast.ImportFrom) and node.module in {
                "os", "pathlib", "shutil", "subprocess", "sys", "tempfile",
            }), "E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", (node.module if isinstance(node, ast.ImportFrom) else "") or "")
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            require(not sensitive_reference(node.value), "E_SOURCE_POLICY_CALLABLE_ALIAS",
                    ast.dump(node.value, include_attributes=False))
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            parent = parents.get(id(node))
            allowed = (
                node.attr == "__init__" and isinstance(parent, ast.Call) and parent.func is node
                and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "super"
            )
            require(allowed, "E_SOURCE_POLICY_DYNAMIC_NAMESPACE", node.attr)
        if not isinstance(node, ast.Call):
            continue
        require(not isinstance(node.func, ast.Lambda), "E_SOURCE_POLICY_DYNAMIC", "lambda call")
        require(not isinstance(node.func, ast.Subscript), "E_SOURCE_POLICY_DYNAMIC",
                ast.dump(node.func, include_attributes=False))
        if isinstance(node.func, ast.Name):
            require(node.func.id not in {"exec", "eval", "__import__", "globals", "locals", "open", "vars", "getattr"},
                    "E_SOURCE_POLICY_DYNAMIC", node.func.id)
            if node.func.id == "run_process":
                require(owner in run_process_owners, "E_SOURCE_POLICY_PROCESS_OWNER", str(owner))
            if node.func.id == "git":
                require(owner in git_owners or (owner == "<lambda>" and outer == "run_git_boundary_controls"),
                        "E_SOURCE_POLICY_GIT_OWNER", str(owner))
            if node.func.id == "git_text":
                require(owner in git_text_owners, "E_SOURCE_POLICY_GIT_OWNER", str(owner))
            if node.func.id == "git_blob":
                require(owner in git_blob_owners, "E_SOURCE_POLICY_GIT_OWNER", str(owner))
            if node.func.id == "live_tip":
                require(owner in live_tip_owners, "E_SOURCE_POLICY_GIT_OWNER", str(owner))
        if isinstance(node.func, ast.Attribute):
            chain = attribute_chain(node.func)
            if chain and chain[0] == "subprocess":
                require(chain == ("subprocess", "run"), "E_SOURCE_POLICY_SUBPROCESS", ".".join(chain))
                subprocess_count += 1
                require(owner == "run_process", "E_SOURCE_POLICY_SUBPROCESS_OWNER", str(owner))
            if chain and chain[0] == "os":
                require(chain in {("os", "chmod"), ("os", "replace")},
                        "E_SOURCE_POLICY_OS", ".".join(chain))
            if chain and chain[0] == "shutil":
                require(chain == ("shutil", "rmtree"), "E_SOURCE_POLICY_SHUTIL", ".".join(chain))
            if chain and chain[0] == "tempfile":
                require(chain in {("tempfile", "gettempdir"), ("tempfile", "mkdtemp")},
                        "E_SOURCE_POLICY_TEMPFILE", ".".join(chain))
            if chain and chain[0] == "pathlib":
                require(chain in {("pathlib", "Path"), ("pathlib", "PurePath")},
                        "E_SOURCE_POLICY_PATHLIB", ".".join(chain))
            if node.func.attr in prohibited_path_methods:
                allowed_owner = owner in filesystem_owners or (
                    owner == "<lambda>" and outer == "run_git_boundary_controls"
                ) or (
                    node.func.attr == "replace" and owner in {"lf_bytes", "inject_after", "run_named_controls"}
                ) or (
                    owner == "<nested:clear_readonly>" and outer == "remove_temp_tree"
                )
                require(allowed_owner, "E_SOURCE_POLICY_FILESYSTEM_OWNER", f"{owner}:{node.func.attr}")
            if chain in {("os", "chmod"), ("os", "replace"), ("shutil", "rmtree"), ("tempfile", "mkdtemp")}:
                allowed_owner = owner in filesystem_owners or (
                    owner == "<nested:clear_readonly>" and outer == "remove_temp_tree"
                )
                require(allowed_owner, "E_SOURCE_POLICY_FILESYSTEM_OWNER", f"{owner}:{'.'.join(chain)}")
        for keyword in node.keywords:
            require(not (keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True),
                    "E_SOURCE_POLICY_SHELL", "shell=True")
    require(subprocess_count == 1, "E_SOURCE_POLICY_SUBPROCESS_COUNT", str(subprocess_count))


def neutralized_source(raw: bytes) -> bytes:
    normalized = lf_bytes(raw)
    pattern = rb'(?m)^SOURCE_POLICY_SHA256_LF = "[0-9a-f]{64}"$'
    replacement = b'SOURCE_POLICY_SHA256_LF = "' + (b"0" * 64) + b'"'
    neutralized, count = re.subn(pattern, replacement, normalized)
    require(count == 1, "E_SOURCE_POLICY_HASH_SENTINEL", str(count))
    return neutralized


def validate_source_policy() -> None:
    raw = VALIDATOR.read_bytes()
    require(raw == lf_bytes(raw), "E_VALIDATOR_LF", VALIDATOR_PATH)
    require(sha256(neutralized_source(raw)) == SOURCE_POLICY_SHA256_LF,
            "E_SOURCE_POLICY_SELF_HASH", sha256(neutralized_source(raw)))
    validate_source_policy_text(raw.decode("utf-8"), VALIDATOR_PATH)


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
        "local_main_absent": git(["show-ref", "--verify", "--quiet", "refs/heads/main"], check=False).returncode != 0,
        "staged_status": name_status_map(git(["diff", "--cached", "--no-renames", "--name-status", "-z"]).stdout),
        "unstaged_status": name_status_map(git(["diff", "--no-renames", "--name-status", "-z"]).stdout),
        "untracked": nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout),
        "claude_dirty": bool(git(["status", "--porcelain=v1", "--", "Claude"]).stdout),
        "claude_parent_diff": bool(git(["diff", "--name-only", EXPECTED_PARENT, "--", "Claude"]).stdout),
        "claude_baseline_diff": bool(git(["diff", "--name-only", BASELINE, "--", "Claude"]).stdout),
        "diff_check": git(["diff", "--check"], check=False).returncode == 0,
        "cached_diff_check": git(["diff", "--cached", "--check"], check=False).returncode == 0,
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
        ("E_GIT_CLAUDE", not snapshot["claude_dirty"] and not snapshot["claude_parent_diff"]),
        ("E_GIT_CLAUDE_BASELINE", not snapshot["claude_baseline_diff"]),
    )
    return {code for code, passed in checks if not passed}


def validate_index_worktree(paths: set[str]) -> None:
    for path in sorted(paths):
        index_raw = git(["show", f":{path}"]).stdout
        work_raw = (ROOT / path).read_bytes()
        require(index_raw == lf_bytes(work_raw), "E_GIT_INDEX_WORKTREE", path)


def validate_worktree(expected_paths: set[str], *, staged: bool) -> None:
    snapshot = repository_snapshot()
    failures = ref_diagnostics(snapshot, EXPECTED_PARENT)
    if staged:
        expected_status = {path: FINAL_STATUS[path] for path in expected_paths}
        if snapshot["staged_status"] != expected_status:
            failures.add("E_GIT_STAGED_STATUS")
        if snapshot["unstaged_status"]:
            failures.add("E_GIT_UNSTAGED")
        if snapshot["untracked"]:
            failures.add("E_GIT_UNTRACKED")
        if not snapshot["cached_diff_check"]:
            failures.add("E_GIT_DIFF_CHECK")
        if not failures:
            validate_index_worktree(expected_paths)
    else:
        if snapshot["staged_status"]:
            failures.add("E_GIT_PREMATURE_STAGE")
        expected_untracked = {path for path in expected_paths if FINAL_STATUS[path] == "A"}
        expected_modified = {path: "M" for path in expected_paths if FINAL_STATUS[path] == "M"}
        if snapshot["untracked"] != expected_untracked or snapshot["unstaged_status"] != expected_modified:
            failures.add("E_GIT_WORKTREE_STATUS")
        if not snapshot["diff_check"]:
            failures.add("E_GIT_DIFF_CHECK")
    require(not failures, "E_REPOSITORY", repr(sorted(failures)))


def predecessor_contract() -> dict[str, Any]:
    validator_raw = (ROOT / PREDECESSOR_VALIDATOR_PATH).read_bytes()
    require(validator_raw == lf_bytes(validator_raw), "E_PREDECESSOR_VALIDATOR_LF")
    require(sha256(validator_raw) == PREDECESSOR_VALIDATOR_SHA256, "E_PREDECESSOR_VALIDATOR_HASH")
    raw = (ROOT / PREDECESSOR_JSON_PATH).read_bytes()
    require(raw == lf_bytes(raw), "E_PREDECESSOR_JSON_LF")
    require(sha256(raw) == PREDECESSOR_JSON_SHA256, "E_PREDECESSOR_JSON_HASH")
    document, _, _ = strict_load_bytes(raw, PREDECESSOR_JSON_PATH)
    require(canonical_bytes(document) == raw, "E_PREDECESSOR_JSON_CANONICAL")
    require(document.get("semantic_sha256") == PREDECESSOR_SEMANTIC_SHA256, "E_PREDECESSOR_SEMANTIC_PIN")
    require(document.get("semantic_sha256") == predecessor_semantic_hash(document), "E_PREDECESSOR_SEMANTIC")
    require(document.get("gate") == "CONDITIONAL_P065" and document.get("step") == "75.2", "E_PREDECESSOR_GATE")
    require(document.get("expected_parent") == EXPECTED_PARENT_PARENT, "E_PREDECESSOR_PARENT")
    require(document.get("expected_subject") == EXPECTED_PARENT_SUBJECT, "E_PREDECESSOR_SUBJECT")
    require(document.get("exact_eight", {}).get("count") == 8, "E_PREDECESSOR_EXACT_EIGHT")
    require(document.get("validator_identity", {}).get("sha256_lf") == PREDECESSOR_VALIDATOR_SHA256,
            "E_PREDECESSOR_VALIDATOR_IDENTITY")
    negative = document.get("negative_control_contract", {})
    require(negative == {
        "git_boundary_count": 17,
        "named_count": 90,
        "singleton_required": True,
        "strict_json_count": 6,
    }, "E_PREDECESSOR_NEGATIVE", repr(negative))
    history = document.get("historical_execution", {})
    precommit = history.get("precommit", {})
    persistence = history.get("persistence", {})
    require(history.get("invocation_count") == history.get("pass_count") == 21, "E_PREDECESSOR_HISTORY")
    require(precommit.get("invocation_count") == precommit.get("pass_count") == 14, "E_PREDECESSOR_PRECOMMIT")
    require(persistence.get("invocation_count") == persistence.get("pass_count") == 7, "E_PREDECESSOR_PERSISTENCE")
    require(precommit.get("cleanup_pass_count") == persistence.get("cleanup_pass_count") == 7,
            "E_PREDECESSOR_CLEANUP")
    pre_records = precommit.get("records", [])
    persistence_records = persistence.get("records", [])
    require([row.get("unit") for row in pre_records] == [
        "ACTIVATION", "ACTIVATION", "ACTIVATION", "STEP70", "STEP70", "STEP70",
        "STEP71", "STEP71", "STEP72", "STEP72", "STEP73", "STEP73", "STEP74", "STEP75_1",
    ], "E_PREDECESSOR_UNIT_ORDER")
    require([row.get("unit") for row in persistence_records] == [
        "ACTIVATION", "STEP70", "STEP71", "STEP72", "STEP73", "STEP74", "STEP75_1",
    ], "E_PREDECESSOR_PERSISTENCE_ORDER")
    for row in [*pre_records, *persistence_records]:
        require(row.get("exit_code") == 0 and row.get("stderr_bytes") == 0 and row.get("terminal_count") == 1,
                "E_PREDECESSOR_RECORD_TERMINAL", repr(row.get("unit")))
        for argument in row.get("args", []):
            require(not re.search(r"(?i)([a-z]:[\\/]|/users/|\\users\\)", argument),
                    "E_PREDECESSOR_ABSOLUTE_ARG", argument)
            if "fixtures/" in argument:
                require(argument.startswith("<TEMP>/"), "E_PREDECESSOR_TEMP_ARG", argument)
    return {
        "commit": EXPECTED_PARENT,
        "parent": EXPECTED_PARENT_PARENT,
        "subject": EXPECTED_PARENT_SUBJECT,
        "gate": "CONDITIONAL_P065",
        "validator_path": PREDECESSOR_VALIDATOR_PATH,
        "validator_sha256_lf": PREDECESSOR_VALIDATOR_SHA256,
        "json_path": PREDECESSOR_JSON_PATH,
        "json_sha256_lf": PREDECESSOR_JSON_SHA256,
        "semantic_sha256": PREDECESSOR_SEMANTIC_SHA256,
        "historical_reused": 21,
        "historical_precommit": 14,
        "historical_persistence": 7,
        "fresh_historical_replay": 0,
        "git_boundary_reused": 17,
    }


def manifest_contract() -> dict[str, Any]:
    raw = (ROOT / MANIFEST_PATH).read_bytes()
    require(sha256(lf_bytes(raw)) == MANIFEST_SHA256_LF, "E_MANIFEST_HASH")
    document, _, _ = strict_load_bytes(raw, MANIFEST_PATH)
    selected = [(index, row) for index, row in enumerate(document["entries"])
                if row.get("version") in {"v1.0.25", "v1.0.25.1", "v1.0.25.2"}]
    indices = [index for index, _ in selected]
    rows = [row for _, row in selected]
    require(indices == list(range(1087, 1520)), "E_MANIFEST_INDICES")
    versions = Counter(row["version"] for row in rows)
    roles = Counter(row["role"] for row in rows)
    modes = Counter(row["review_mode"] for row in rows)
    unique = {row["blob_sha"]: row for row in rows}
    unique_roles = Counter(row["role"] for row in unique.values())
    unique_modes = Counter(row["review_mode"] for row in unique.values())
    path_set = sha256(("\n".join(sorted(row["path"] for row in rows)) + "\n").encode("utf-8"))
    path_blob = sha256(("\n".join(sorted(row["path"] + "\0" + row["blob_sha"] for row in rows)) + "\n").encode("utf-8"))
    blob_set = sha256(("\n".join(sorted(unique)) + "\n").encode("utf-8"))
    require(path_set == PATH_SET_SHA256 and path_blob == PATH_BLOB_SHA256 and blob_set == UNIQUE_BLOB_SHA256,
            "E_MANIFEST_SET_HASH")
    text_lines = sum(int(row.get("extent", {}).get("lines") or 0) for row in unique.values())
    pdf_pages = sum(int(row.get("extent", {}).get("pages") or 0) for row in unique.values())
    occurrence_bytes = sum(int(row["size_bytes"]) for row in rows)
    unique_bytes = sum(int(row["size_bytes"]) for row in unique.values())
    require(len(rows) == len({row["path"] for row in rows}) == 433 and len(unique) == 167, "E_MANIFEST_COUNTS")
    require(versions == {"v1.0.25": 143, "v1.0.25.1": 144, "v1.0.25.2": 146}, "E_MANIFEST_VERSIONS")
    require(roles == {
        "code": 3, "figure": 9, "generated_document": 9, "implementation_guide": 6,
        "result": 211, "supporting_document": 6, "test": 12, "theory": 177,
    }, "E_MANIFEST_ROLES")
    require(unique_roles == {
        "code": 2, "figure": 3, "generated_document": 6, "implementation_guide": 2,
        "result": 72, "supporting_document": 4, "test": 5, "theory": 73,
    }, "E_MANIFEST_UNIQUE_ROLES")
    require(modes == {"FULL_TEXT": 415, "FULL_PDF": 9, "FULL_IMAGE": 9}, "E_MANIFEST_MODES")
    require(unique_modes == {"FULL_TEXT": 158, "FULL_PDF": 6, "FULL_IMAGE": 3}, "E_MANIFEST_UNIQUE_MODES")
    require((text_lines, pdf_pages, occurrence_bytes, unique_bytes) == (30597, 308, 26391541, 12483701),
            "E_MANIFEST_EXTENTS")
    by_version: dict[str, dict[str, dict[str, Any]]] = {}
    for version in versions:
        prefix = f"Claude/docs/{version}/"
        by_version[version] = {
            row["path"][len(prefix):]: row for row in rows if row["path"].startswith(prefix)
        }
        require(len({row["blob_sha"] for row in by_version[version].values()}) == len(by_version[version]),
                "E_MANIFEST_VERSION_DUPLICATE", version)
    left = by_version["v1.0.25"]
    middle = by_version["v1.0.25.1"]
    right = by_version["v1.0.25.2"]
    changed_25_251 = {path for path in left.keys() & middle.keys() if left[path]["blob_sha"] != middle[path]["blob_sha"]}
    changed_251_252 = {path for path in middle.keys() & right.keys() if middle[path]["blob_sha"] != right[path]["blob_sha"]}
    require(changed_25_251 == {
        "ARCHIVE_NOTE.md", "_sections/ch1_sec05_width.tex", "_sections/ch1_sec06_eqpeak.tex",
        "_sections/ch3v22_sec02b_sifr.tex", "ch1_graphite_v1.0.24.pdf", "ch1_graphite_v1.0.24.tex",
        "ch2_lco_v1.0.24.pdf", "ch2_lco_v1.0.24.tex", "ch3_si_v1.0.24.pdf", "ch3_si_v1.0.24.tex",
    }, "E_MANIFEST_DELTA_25_251")
    require(set(middle) - set(left) == {"results/V1025_1_TOUCHUP_NOTE.md"} and not (set(left) - set(middle)),
            "E_MANIFEST_ADDITION_251")
    require(changed_251_252 == {
        "ARCHIVE_NOTE.md", "Anode_Fit_v1.0.24.py", "_sections/ch1_appB_codemap.tex",
        "_sections/ch1_sec05b_gr2L.tex", "_sections/ch1_sec18_inputs.tex",
        "_sections/ch3v22_sec02b_sifr.tex", "_sections/ch3v22_sec05_code.tex",
        "ch1_graphite_v1.0.24.tex", "ch2_lco_v1.0.24.tex", "ch3_si_v1.0.24.tex",
        "test_gates_v1024.py",
    }, "E_MANIFEST_DELTA_251_252")
    require(set(right) - set(middle) == {
        "results/HANDOVER_v1025_2.md", "results/KERNEL_COMPARISON_REPORT_v1025_2.html",
    } and not (set(middle) - set(right)), "E_MANIFEST_ADDITION_252")
    pdfs = {path for path, row in middle.items() if row["review_mode"] == "FULL_PDF"}
    require(len(pdfs) == 3 and all(middle[path]["blob_sha"] == right[path]["blob_sha"] for path in pdfs),
            "E_MANIFEST_STALE_PDF")
    common_all = set(left) & set(middle) & set(right)
    all_same = sum(len({left[path]["blob_sha"], middle[path]["blob_sha"], right[path]["blob_sha"]}) == 1
                   for path in common_all)
    require(len(common_all) == 143 and all_same == 127, "E_MANIFEST_THREE_WAY")
    return {
        "path": MANIFEST_PATH,
        "sha256_lf": MANIFEST_SHA256_LF,
        "versions": dict(sorted(versions.items())),
        "zero_based_indices": [1087, 1519],
        "one_based_ordinals": [1088, 1520],
        "occurrences": 433,
        "unique_paths": 433,
        "unique_blobs": 167,
        "occurrence_roles": dict(sorted(roles.items())),
        "unique_roles": dict(sorted(unique_roles.items())),
        "occurrence_review_modes": dict(sorted(modes.items())),
        "unique_review_modes": dict(sorted(unique_modes.items())),
        "unique_text_lines": text_lines,
        "unique_pdf_pages": pdf_pages,
        "occurrence_bytes": occurrence_bytes,
        "unique_bytes": unique_bytes,
        "path_set_sha256": path_set,
        "path_blob_sha256": path_blob,
        "unique_blob_sha256": blob_set,
        "all_common": len(common_all),
        "all_same": all_same,
        "v1025_2_pdfs_identical_to_v1025_1": True,
        "v1025_2_pdfs_are_build_evidence": False,
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
            "path": path,
            "blob": blob,
            "lines": expected_lines,
            "sha256_lf": expected_hash,
            "read_required": "FULL_TEXT",
        })
    return {"count": 2, "lines": 655, "records": records, "separate_from_manifest": True}


def process_contract() -> dict[str, Any]:
    release_paths = [
        "Claude/docs/v1.0.25/**", "Claude/docs/v1.0.25.1/**", "Claude/docs/v1.0.25.2/**",
    ]
    raw = lf_bytes(git(["log", "--reverse", "--format=%H", "--all", "--", *release_paths]).stdout)
    commits = raw.decode("ascii").splitlines()
    require(len(commits) == 17, "E_PROCESS_COUNT")
    require(commits[0] == "edbc4a2c68cda0dd21662cb6dd68ba8bed699a76", "E_PROCESS_FIRST")
    require(commits[-1] == "e3e1a634f34b711aa4803fd190fe9120f1755f13", "E_PROCESS_LAST")
    require(sha256(raw) == PROCESS_SHA256_LF, "E_PROCESS_HASH")
    routed_paths = [release_paths[0], release_paths[1], release_paths[2], SUPPLEMENTAL[0][0], SUPPLEMENTAL[1][0]]
    routed_raw = lf_bytes(git(["log", "--reverse", "--format=%H", "--all", "--", *routed_paths]).stdout)
    routed = routed_raw.decode("ascii").splitlines()
    require(len(routed) == 20, "E_ROUTED_PROCESS_COUNT")
    require(routed[0] == commits[0] and routed[-1] == commits[-1], "E_ROUTED_PROCESS_TERMINALS")
    require(sha256(routed_raw) == ROUTED_PROCESS_SHA256_LF, "E_ROUTED_PROCESS_HASH")
    return {
        "release_query": release_paths,
        "release_count": 17,
        "release_first": commits[0],
        "release_last": commits[-1],
        "release_sha256_lf": PROCESS_SHA256_LF,
        "routed_query": routed_paths,
        "routed_count": 20,
        "routed_first": routed[0],
        "routed_last": routed[-1],
        "routed_sha256_lf": ROUTED_PROCESS_SHA256_LF,
    }


def plan_contract() -> dict[str, Any]:
    require(PLAN.is_file(), "E_PLAN_MISSING", PLAN_PATH)
    raw = PLAN.read_bytes()
    require(raw == lf_bytes(raw) and raw.endswith(b"\n"), "E_PLAN_LF", PLAN_PATH)
    text = raw.decode("utf-8")
    positions = [text.find(heading) for heading in REQUIRED_HEADINGS]
    require(all(position >= 0 for position in positions), "E_PLAN_HEADING")
    require(positions == sorted(positions), "E_PLAN_HEADING_ORDER")
    missing = [token for token in REQUIRED_PLAN_TOKENS if token not in text]
    require(not missing, "E_PLAN_TOKEN", repr(missing))
    step_headings = re.findall(r"^### Step (\d+(?:\.\d+)?)\b", text, flags=re.MULTILINE)
    require(step_headings == ["76", "77", "78", "79", "80", "81.1", "81.2"],
            "E_PLAN_STEP_NUMBERING", repr(step_headings))
    require("### Step 82" not in text, "E_PLAN_SCOPE")
    return {
        "path": PLAN_PATH,
        "sha256_lf": sha256(raw),
        "lines": line_count(raw),
        "heading_count": len(REQUIRED_HEADINGS),
        "steps": step_headings,
        "first_step_released_only_after_persistence": True,
    }


def control_contract() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path, tokens in CONTROL_TOKENS.items():
        full = ROOT / path
        require(full.is_file(), "E_CONTROL_MISSING", path)
        raw = full.read_bytes()
        require(raw == lf_bytes(raw) and raw.endswith(b"\n"), "E_CONTROL_LF", path)
        text = raw.decode("utf-8")
        missing = [token for token in tokens if token not in text]
        require(not missing, "E_CONTROL_TOKEN", f"{path}:{missing!r}")
        record = {"path": path, "sha256_lf": sha256(raw), "lines": line_count(raw)}
        if path in LEDGER_PHASE066_ROW_TOKENS:
            phase_rows = [line for line in text.splitlines() if line.startswith("| 066 |")]
            require(len(phase_rows) == 1, "E_CONTROL_PHASE066_ROW_COUNT",
                    f"{path}:{len(phase_rows)}")
            phase_row = phase_rows[0]
            row_missing = [token for token in LEDGER_PHASE066_ROW_TOKENS[path]
                           if token not in phase_row]
            require(not row_missing, "E_CONTROL_PHASE066_ROW",
                    f"{path}:{row_missing!r}")
            require("PLAN_ACTIVATION_PENDING_PERSISTENCE" not in phase_row,
                    "E_CONTROL_PHASE066_ROW_STALE", path)
            record["phase066_row_sha256_lf"] = sha256((phase_row + "\n").encode("utf-8"))
        records.append(record)
    return {
        "count": 4,
        "records": records,
        "result_first": True,
        "validation_json_last": True,
        "precommit_record_state": True,
    }


def validator_contract() -> dict[str, Any]:
    raw = VALIDATOR.read_bytes()
    require(raw == lf_bytes(raw), "E_VALIDATOR_LF", VALIDATOR_PATH)
    return {
        "path": VALIDATOR_PATH,
        "bytes_lf": len(raw),
        "lines": line_count(raw),
        "sha256_lf": sha256(raw),
        "neutralized_sha256_lf": sha256(neutralized_source(raw)),
        "source_policy": "PASS",
        "subprocess_run_sites": 1,
        "production_source_imported": False,
        "production_source_executed": False,
    }


def build_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "P066-PLAN-ACTIVATION-1",
        "phase": "066",
        "generated_date": "2026-09-01",
        "status": "PASS_PENDING_PERSISTENCE",
        "gate": GATE,
        "persistence_terminal": PERSISTENCE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "repository": {
            "branch": ACTIVE_BRANCH,
            "upstream": f"origin/{ACTIVE_BRANCH}",
            "expected_parent": EXPECTED_PARENT,
            "expected_parent_parent": EXPECTED_PARENT_PARENT,
            "expected_parent_subject": EXPECTED_PARENT_SUBJECT,
            "protected_branch": PROTECTED_BRANCH,
            "protected_tip": PROTECTED_TIP,
            "main_tip": MAIN_TIP,
            "local_main_absent": True,
            "baseline": BASELINE,
            "claude_modification_allowed": False,
        },
        "predecessor": predecessor_contract(),
        "plan": plan_contract(),
        "manifest": manifest_contract(),
        "supplemental": supplemental_contract(),
        "process": process_contract(),
        "controls": control_contract(),
        "exact_seven": {
            "count": 7,
            "paths": FINAL_PATHS,
            "status": ["A", "A", "A", "A", "M", "M", "M"],
            "rename_allowed": False,
            "result_first": True,
            "validation_json_last": True,
        },
        "authority": {
            "activation_inventory_only": True,
            "predecessor_gate": "CONDITIONAL_P065",
            "v1026a_v1026b_are_releases": False,
            "v1025_2_pdf_build_evidence": False,
            "fit_reproduced": False,
            "optimizer_state_reconciled": False,
            "external_scientific": False,
            "canonical": False,
            "publication_ready": False,
        },
        "negative_contract": {
            "semantic_cases": 21,
            "document_cases": 5,
            "strict_json_cases": 6,
            "policy_cases": 49,
            "named_count": 75,
            "actual_git_cases": 19,
            "actual_git_execution": "COLLECT_ONCE_THEN_CANONICAL_REUSE",
            "singleton_required": True,
        },
        "historical_execution": {
            "canonical_reused": 21,
            "precommit_reused": 14,
            "persistence_reused": 7,
            "fresh_replay": 0,
            "predecessor_git_boundary_reused": 17,
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
    "persistence_terminal": "E_PERSISTENCE_TERMINAL",
    "expected_parent": "E_PARENT",
    "expected_subject": "E_SUBJECT",
    "repository": "E_REPOSITORY_DOCUMENT",
    "predecessor": "E_PREDECESSOR_DOCUMENT",
    "plan": "E_PLAN_DOCUMENT",
    "manifest": "E_MANIFEST_DOCUMENT",
    "supplemental": "E_SUPPLEMENTAL_DOCUMENT",
    "process": "E_PROCESS_DOCUMENT",
    "controls": "E_CONTROLS_DOCUMENT",
    "exact_seven": "E_EXACT_SEVEN_DOCUMENT",
    "authority": "E_AUTHORITY_DOCUMENT",
    "negative_contract": "E_NEGATIVE_DOCUMENT",
    "historical_execution": "E_HISTORY_DOCUMENT",
    "determinism": "E_DETERMINISM_DOCUMENT",
    "validator_identity": "E_VALIDATOR_DOCUMENT",
    "semantic_sha256": "E_SEMANTIC",
}


def document_diagnostics(document: dict[str, Any], expected: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    if set(document) != set(expected):
        diagnostics.add("E_DOCUMENT_SCHEMA")
    for key, code in SECTION_CODES.items():
        if key == "semantic_sha256":
            continue
        if document.get(key) != expected.get(key):
            diagnostics.add(code)
    if document.get("semantic_sha256") != semantic_hash(document):
        diagnostics.add("E_SEMANTIC")
    return diagnostics


def validate_document_bytes(raw: bytes, expected: dict[str, Any], expected_raw: bytes) -> None:
    require(b"\r" not in raw, "E_OUTPUT_LF")
    document, _, _ = strict_load_bytes(raw, "document")
    require(canonical_bytes(document) == raw, "E_OUTPUT_CANONICAL")
    diagnostics = document_diagnostics(document, expected)
    if diagnostics:
        code = sorted(diagnostics)[0]
        raise ValidationError(code, repr(sorted(diagnostics)))
    require(raw == expected_raw, "E_OUTPUT_BYTES")


def expect_error(wanted: str, operation: Callable[[], None]) -> None:
    try:
        operation()
    except ValidationError as error:
        require(error.code == wanted, "E_NEGATIVE_SINGLETON", f"{wanted}:{error.code}")
    else:
        raise ValidationError("E_NEGATIVE_ESCAPE", wanted)


def inject_after(source: str, marker: str, addition: str) -> str:
    require(source.count(marker) == 1, "E_NEGATIVE_MARKER", marker)
    return source.replace(marker, marker + addition, 1)


def run_named_controls(baseline: dict[str, Any]) -> tuple[int, int]:
    semantic_cases: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("E_DOCUMENT_SCHEMA", lambda d: d.update({"unexpected": 1}), True),
        ("E_SCHEMA", lambda d: d.update({"schema_version": "bad"}), True),
        ("E_PHASE", lambda d: d.update({"phase": "065"}), True),
        ("E_DATE", lambda d: d.update({"generated_date": "1970-01-01"}), True),
        ("E_STATUS", lambda d: d.update({"status": "FAIL"}), True),
        ("E_GATE", lambda d: d.update({"gate": "FAIL_P066"}), True),
        ("E_PERSISTENCE_TERMINAL", lambda d: d.update({"persistence_terminal": "bad"}), True),
        ("E_PARENT", lambda d: d.update({"expected_parent": "0" * 40}), True),
        ("E_SUBJECT", lambda d: d.update({"expected_subject": "bad"}), True),
        ("E_REPOSITORY_DOCUMENT", lambda d: d["repository"].update({"branch": "bad"}), True),
        ("E_PREDECESSOR_DOCUMENT", lambda d: d["predecessor"].update({"historical_reused": 20}), True),
        ("E_PLAN_DOCUMENT", lambda d: d["plan"].update({"steps": ["76"]}), True),
        ("E_MANIFEST_DOCUMENT", lambda d: d["manifest"].update({"occurrences": 432}), True),
        ("E_SUPPLEMENTAL_DOCUMENT", lambda d: d["supplemental"].update({"count": 1}), True),
        ("E_PROCESS_DOCUMENT", lambda d: d["process"].update({"release_count": 16}), True),
        ("E_CONTROLS_DOCUMENT", lambda d: d["controls"].update({"count": 3}), True),
        ("E_EXACT_SEVEN_DOCUMENT", lambda d: d["exact_seven"].update({"count": 8}), True),
        ("E_AUTHORITY_DOCUMENT", lambda d: d["authority"].update({"external_scientific": True}), True),
        ("E_NEGATIVE_DOCUMENT", lambda d: d["negative_contract"].update({"actual_git_cases": 18}), True),
        ("E_VALIDATOR_DOCUMENT", lambda d: d["validator_identity"].update({"sha256_lf": "0" * 64}), True),
        ("E_SEMANTIC", lambda d: d.update({"semantic_sha256": "0" * 64}), False),
    ]
    passed = 0
    for wanted, mutation, rehash in semantic_cases:
        candidate = copy.deepcopy(baseline)
        mutation(candidate)
        if rehash:
            candidate["semantic_sha256"] = semantic_hash(candidate)
        observed = document_diagnostics(candidate, baseline)
        require(observed == {wanted}, "E_SEMANTIC_SINGLETON", f"{wanted}:{sorted(observed)}")
        passed += 1

    expected_raw = canonical_bytes(baseline)
    document_cases: list[tuple[str, bytes]] = [
        ("E_OUTPUT_CANONICAL", json.dumps(baseline, sort_keys=True).encode("utf-8")),
        ("E_OUTPUT_LF", expected_raw.replace(b"\n", b"\r\n")),
        ("E_OUTPUT_CANONICAL", expected_raw + b" "),
        ("E_SEMANTIC", canonical_bytes({**baseline, "semantic_sha256": "0" * 64})),
        ("E_GATE", canonical_bytes({**baseline, "gate": "FAIL_P066", "semantic_sha256": ""})),
    ]
    document_cases[-1] = ("E_GATE", canonical_bytes({
        **baseline,
        "gate": "FAIL_P066",
        "semantic_sha256": semantic_hash({**baseline, "gate": "FAIL_P066", "semantic_sha256": ""}),
    }))
    for wanted, raw in document_cases:
        expect_error(wanted, lambda raw=raw: validate_document_bytes(raw, baseline, expected_raw))
        passed += 1

    strict_cases = [
        ("E_JSON_DUPLICATE", b'{"a":1,"a":2}\n'),
        ("E_JSON_NONFINITE", b'{"a":NaN}\n'),
        ("E_JSON_NONFINITE", b'{"a":Infinity}\n'),
        ("E_JSON_NONFINITE", b'{"a":1e9999}\n'),
        ("E_JSON_SYNTAX", b'{"a":1} trailing\n'),
        ("E_JSON_UTF8", b'{"a":"\xff"}\n'),
    ]
    for wanted, raw in strict_cases:
        expect_error(wanted, lambda raw=raw: strict_load_bytes(raw, "negative"))

    source = VALIDATOR.read_text(encoding="utf-8")
    policy_cases: list[tuple[str, Callable[[], None]]] = [
        ("E_SOURCE_POLICY_IMPORT_ALIAS", lambda: validate_source_policy_text(source + "\nimport subprocess as s\n", "alias.py")),
        ("E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", lambda: validate_source_policy_text(source + "\nfrom os import system\n", "from-os.py")),
        ("E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", lambda: validate_source_policy_text(source + "\nfrom shutil import rmtree\n", "from-shutil.py")),
        ("E_SOURCE_POLICY_SUBPROCESS", lambda: validate_source_policy_text(source + "\nsubprocess.Popen(['git'])\n", "popen.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(source + "\ngetattr(subprocess, 'run')(['git'])\n", "getattr.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(source + "\nexec('payload')\n", "exec.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(source + "\n__import__('subprocess')\n", "import.py")),
        ("E_SOURCE_POLICY_DYNAMIC_NAMESPACE", lambda: validate_source_policy_text(source + "\nx=(1).__class__\n", "dunder.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(source + "\nr=run_process\n", "alias-run.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(source + "\nr=subprocess.Popen\n", "alias-popen.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(source + "\ndef bad(g=git):\n    pass\n", "default-git.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(source + "\nf=lambda w=pathlib.Path.write_bytes: None\n", "default-write.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(source + "\n(lambda: None)()\n", "lambda.py")),
        ("E_SOURCE_POLICY_DUPLICATE_OWNER", lambda: validate_source_policy_text(source + "\ndef repository_snapshot():\n    pass\n", "duplicate.py")),
        ("E_SOURCE_POLICY_GIT_OWNER", lambda: validate_source_policy_text(inject_after(
            source, "def repository_snapshot() -> dict[str, Any]:\n",
            "    def nested():\n        git(['status'])\n    nested()\n",
        ), "nested-git.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_OWNER", lambda: validate_source_policy_text(inject_after(
            source, "def atomic_collect(raw: bytes) -> None:\n",
            "    def nested():\n        pathlib.Path('x').write_bytes(b'x')\n    nested()\n",
        ), "nested-fs.py")),
        ("E_SOURCE_POLICY_SUBPROCESS_OWNER", lambda: validate_source_policy_text(source + "\ndef bad():\n    subprocess.run(['git'])\n", "direct-run.py")),
        ("E_SOURCE_POLICY_SHELL", lambda: validate_source_policy_text(
            inject_after(source, "shell=" + "False", ", shell=True"), "shell.py")),
        ("E_SOURCE_POLICY_OS", lambda: validate_source_policy_text(source + "\nos.system('payload')\n", "os-system.py")),
        ("E_SOURCE_POLICY_OS", lambda: validate_source_policy_text(source + "\nos.remove('payload')\n", "os-remove.py")),
        ("E_SOURCE_POLICY_TEMPFILE", lambda: validate_source_policy_text(source + "\ntempfile.NamedTemporaryFile()\n", "tempfile.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_OWNER", lambda: validate_source_policy_text(source + "\npathlib.Path('x').write_text('x')\n", "write.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_OWNER", lambda: validate_source_policy_text(source + "\npathlib.Path('x').unlink()\n", "unlink.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_OWNER", lambda: validate_source_policy_text(source + "\nshutil.rmtree('x')\n", "rmtree.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(source + "\nopen('x','w')\n", "open.py")),
        ("E_SOURCE_POLICY_GIT_LAUNCHER", lambda: validate_git_argv(["C:/tools/git.exe", "status"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "arbitrary"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "-c", "alias.x=!payload", "x"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "-c", "protocol.ext.allow=always", "status"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "clone", "ext::payload", "dst"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "--config-env", "x=y", "status"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "config", "core.sshCommand", "payload"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "--force", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "--force-with-lease", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "--mirror", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "--delete", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "origin", ":main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "origin", "+main:main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "--prune", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "push", "--exec", "payload", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "clone", "-u", "payload", "src", "dst"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "clone", "-c", "core.sshCommand=payload", "src", "dst"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "branch", "-D", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "checkout", "-f", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "switch", "-f", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "reset", "--hard", "HEAD"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_git_argv(["git", "update-ref", "-d", "refs/heads/main"])),
        ("E_EXPECTED_COMMIT", lambda: validate_expected_commit("--output=C:/escape")),
        ("E_SOURCE_POLICY_DYNAMIC_NAMESPACE", lambda: validate_source_policy_text(source + "\nx=globals().__getitem__('git')\n", "globals.py")),
    ]
    require(len(policy_cases) == 49, "E_POLICY_CONTROL_COUNT", str(len(policy_cases)))
    for wanted, operation in policy_cases:
        expect_error(wanted, operation)
        passed += 1
    require(passed == 75, "E_NAMED_CONTROL_COUNT", str(passed))
    return passed, 75


def remove_temp_tree(root: pathlib.Path, prefix: str) -> None:
    require(root.name.startswith(prefix) and is_within_temp(root), "E_TEMP_BOUNDARY", str(root))

    def clear_readonly(function: Callable[..., Any], target: str, _: Any) -> None:
        os.chmod(target, 0o700)
        function(target)

    if root.exists():
        shutil.rmtree(root, onerror=clear_readonly)
    require(not root.exists(), "E_TEMP_CLEANUP", str(root))


def make_git_boundary_fixture() -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, str, str, set[str]]:
    prefix = "phase066-plan-git-boundary-"
    root = pathlib.Path(tempfile.mkdtemp(prefix=prefix)).resolve()
    seed = root / "seed"
    origin = root / "origin.git"
    work = root / "work"
    seed.mkdir()
    git(["init"], cwd=seed)
    git(["config", "user.email", "phase066-fixture@example.invalid"], cwd=seed)
    git(["config", "user.name", "Phase 066 Fixture"], cwd=seed)
    git(["config", "core.autocrlf", "false"], cwd=seed)
    for path in [PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH, "Claude/keep.txt", "outside.txt"]:
        full = seed / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(b"baseline\n")
    git(["add", "--", "."], cwd=seed)
    git(["commit", "-m", "base"], cwd=seed)
    base = git_text(["rev-parse", "HEAD"], cwd=seed)
    git(["branch", ACTIVE_BRANCH, base], cwd=seed)
    git(["branch", PROTECTED_BRANCH, base], cwd=seed)
    git(["branch", "main", base], cwd=seed)
    (seed / "drift.txt").write_bytes(b"drift\n")
    git(["add", "--", "drift.txt"], cwd=seed)
    git(["commit", "-m", "drift"], cwd=seed)
    drift = git_text(["rev-parse", "HEAD"], cwd=seed)
    git(["branch", "fixture/drift", drift], cwd=seed)
    git(["checkout", ACTIVE_BRANCH], cwd=seed)
    git(["clone", "--bare", str(seed), str(origin)], cwd=root)
    git(["clone", str(origin), str(work)], cwd=root)
    git(["branch", PROTECTED_BRANCH, base], cwd=work)
    for path in [PLAN_PATH, VALIDATOR_PATH, OUTPUT_PATH, RESULT_PATH]:
        full = work / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(b"new\n")
    for path in [PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH]:
        (work / path).write_bytes(b"modified\n")
    git(["add", "--", *FINAL_PATHS], cwd=work)
    return root, work, origin, base, drift, FINAL_PATH_SET


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
        "local_main_absent": git(["show-ref", "--verify", "--quiet", "refs/heads/main"], cwd=work, check=False).returncode != 0,
        "staged_status": name_status_map(git(["diff", "--cached", "--no-renames", "--name-status", "-z"], cwd=work).stdout),
        "unstaged_status": name_status_map(git(["diff", "--no-renames", "--name-status", "-z"], cwd=work).stdout),
        "untracked": nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=work).stdout),
        "claude_dirty": bool(git(["status", "--porcelain=v1", "--", "Claude"], cwd=work).stdout),
        "diff_check": git(["diff", "--cached", "--check"], cwd=work, check=False).returncode == 0,
    }


def fixture_diagnostics(snapshot: dict[str, Any], base: str, expected_paths: set[str]) -> set[str]:
    checks = (
        ("E_GIT_BRANCH", snapshot["branch"] == ACTIVE_BRANCH),
        ("E_GIT_UPSTREAM_NAME", snapshot["upstream_name"] == f"origin/{ACTIVE_BRANCH}"),
        ("E_GIT_HEAD", snapshot["head"] == base),
        ("E_GIT_UPSTREAM", snapshot["upstream"] == base),
        ("E_GIT_ACTIVE_TRACKING", snapshot["origin_active"] == base),
        ("E_GIT_ACTIVE_LIVE", snapshot["live_active"] == base),
        ("E_GIT_LOCAL_PROTECTED", snapshot["local_protected"] == base),
        ("E_GIT_PROTECTED_TRACKING", snapshot["origin_protected"] == base),
        ("E_GIT_PROTECTED_LIVE", snapshot["live_protected"] == base),
        ("E_GIT_MAIN_TRACKING", snapshot["origin_main"] == base),
        ("E_GIT_MAIN_LIVE", snapshot["live_main"] == base),
        ("E_GIT_LOCAL_MAIN", snapshot["local_main_absent"] is True),
        ("E_GIT_STAGED_STATUS", snapshot["staged_status"] == {path: FINAL_STATUS[path] for path in expected_paths}),
        ("E_GIT_UNSTAGED", not snapshot["unstaged_status"]),
        ("E_GIT_UNTRACKED", not snapshot["untracked"]),
        ("E_GIT_CLAUDE", not snapshot["claude_dirty"]),
        ("E_GIT_DIFF_CHECK", snapshot["diff_check"] is True),
    )
    return {code for code, passed in checks if not passed}


def fixture_delete_allowlisted(work: pathlib.Path) -> None:
    git(["rm", "--cached", "--", PLAN_PATH], cwd=work)
    (work / PLAN_PATH).unlink()


def fixture_rename_escape(work: pathlib.Path) -> None:
    git(["rm", "--cached", "--", PLAN_PATH], cwd=work)
    (work / PLAN_PATH).unlink()
    git(["mv", "outside.txt", PLAN_PATH], cwd=work)


def fixture_wrong_status(work: pathlib.Path) -> None:
    git(["rm", "-f", "--", PARENT_LEDGER_PATH], cwd=work)


def run_git_boundary_controls() -> tuple[int, int]:
    cases: list[tuple[str, set[str], Callable[[pathlib.Path, pathlib.Path, str, str], None]]] = [
        ("branch", {"E_GIT_BRANCH"}, lambda w, o, b, d: git(["branch", "-m", "fixture/wrong"], cwd=w)),
        ("upstream", {"E_GIT_UPSTREAM_NAME", "E_GIT_UPSTREAM"}, lambda w, o, b, d: git(["branch", "--set-upstream-to=origin/fixture/drift", ACTIVE_BRANCH], cwd=w)),
        ("head", {"E_GIT_HEAD", "E_GIT_STAGED_STATUS"},
         lambda w, o, b, d: git(["update-ref", f"refs/heads/{ACTIVE_BRANCH}", d], cwd=w)),
        ("active_tracking", {"E_GIT_UPSTREAM", "E_GIT_ACTIVE_TRACKING"}, lambda w, o, b, d: git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", d], cwd=w)),
        ("active_live", {"E_GIT_ACTIVE_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", f"refs/heads/{ACTIVE_BRANCH}", d], cwd=w)),
        ("local_protected", {"E_GIT_LOCAL_PROTECTED"}, lambda w, o, b, d: git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", d], cwd=w)),
        ("protected_tracking", {"E_GIT_PROTECTED_TRACKING"}, lambda w, o, b, d: git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", d], cwd=w)),
        ("protected_live", {"E_GIT_PROTECTED_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", f"refs/heads/{PROTECTED_BRANCH}", d], cwd=w)),
        ("main_tracking", {"E_GIT_MAIN_TRACKING"}, lambda w, o, b, d: git(["update-ref", "refs/remotes/origin/main", d], cwd=w)),
        ("main_live", {"E_GIT_MAIN_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", "refs/heads/main", d], cwd=w)),
        ("local_main", {"E_GIT_LOCAL_MAIN"}, lambda w, o, b, d: git(["branch", "main", b], cwd=w)),
        ("claude", {"E_GIT_UNSTAGED", "E_GIT_CLAUDE"}, lambda w, o, b, d: (w / "Claude/keep.txt").write_bytes(b"changed\n")),
        ("extra_staged", {"E_GIT_STAGED_STATUS"}, lambda w, o, b, d: ((w / "extra.txt").write_bytes(b"x\n"), git(["add", "--", "extra.txt"], cwd=w))),
        ("deletion", {"E_GIT_STAGED_STATUS"}, lambda w, o, b, d: fixture_delete_allowlisted(w)),
        ("rename", {"E_GIT_STAGED_STATUS"}, lambda w, o, b, d: fixture_rename_escape(w)),
        ("wrong_status", {"E_GIT_STAGED_STATUS"}, lambda w, o, b, d: fixture_wrong_status(w)),
        ("untracked", {"E_GIT_UNTRACKED"}, lambda w, o, b, d: (w / "extra.txt").write_bytes(b"x\n")),
        ("index_worktree", {"E_GIT_UNSTAGED"}, lambda w, o, b, d: (w / PLAN_PATH).write_bytes(b"changed\n")),
        ("diff_check", {"E_GIT_DIFF_CHECK"}, lambda w, o, b, d: ((w / PLAN_PATH).write_bytes(b"bad-space \n"), git(["add", "--", PLAN_PATH], cwd=w))),
    ]
    passed = 0
    for name, wanted, mutation in cases:
        root, work, origin, base, drift, paths = make_git_boundary_fixture()
        try:
            require(not fixture_diagnostics(fixture_snapshot(work, origin), base, paths), "E_GIT_FIXTURE_BASELINE", name)
            mutation(work, origin, base, drift)
            observed = fixture_diagnostics(fixture_snapshot(work, origin), base, paths)
            require(observed == wanted, "E_GIT_FIXTURE_DIAGNOSTIC", f"{name}:{sorted(observed)}!={sorted(wanted)}")
            passed += 1
        finally:
            remove_temp_tree(root, "phase066-plan-git-boundary-")
    return passed, len(cases)


def validate_expected_commit(value: str | None) -> str:
    require(value is not None and re.fullmatch(r"[0-9a-f]{40}", value) is not None,
            "E_EXPECTED_COMMIT", repr(value))
    return value


def validate_persistence(expected_commit: str) -> None:
    snapshot = repository_snapshot()
    failures = ref_diagnostics(snapshot, expected_commit)
    if snapshot["staged_status"] or snapshot["unstaged_status"] or snapshot["untracked"]:
        failures.add("E_GIT_DIRTY")
    require(not failures, "E_PERSISTENCE_REFS", repr(sorted(failures)))
    require(git_text(["rev-parse", f"{expected_commit}^"]) == EXPECTED_PARENT, "E_PERSISTENCE_PARENT")
    require(git_text(["show", "-s", "--format=%s", expected_commit]) == EXPECTED_SUBJECT, "E_PERSISTENCE_SUBJECT")
    status = name_status_map(git(["diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-z", "-r", expected_commit]).stdout)
    require(status == FINAL_STATUS, "E_PERSISTENCE_PATHS", repr(status))
    for path in FINAL_PATHS:
        committed = git_blob(expected_commit, path)
        work = (ROOT / path).read_bytes()
        require(committed == lf_bytes(work), "E_PERSISTENCE_BLOB", path)


def read_stored() -> tuple[dict[str, Any], bytes, int, int]:
    require(OUTPUT.is_file(), "E_VALIDATION_ARTIFACT_MISSING", OUTPUT_PATH)
    raw = OUTPUT.read_bytes()
    require(raw == lf_bytes(raw), "E_OUTPUT_LF", OUTPUT_PATH)
    document, nodes, depth = strict_load_bytes(raw, OUTPUT_PATH)
    require(canonical_bytes(document) == raw, "E_OUTPUT_CANONICAL", OUTPUT_PATH)
    require(document.get("semantic_sha256") == semantic_hash(document), "E_SEMANTIC", OUTPUT_PATH)
    return document, raw, nodes, depth


def atomic_collect(raw: bytes) -> None:
    require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST", "six nonself outputs")
    temp_path = OUTPUT.with_name(OUTPUT.name + ".tmp-phase066-plan")
    require(not temp_path.exists(), "E_COLLECT_TEMP_EXISTS", str(temp_path))
    try:
        temp_path.write_bytes(raw)
        document, _, _ = strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        require(canonical_bytes(document) == raw, "E_COLLECT_CANONICAL")
        os.replace(temp_path, OUTPUT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(OUTPUT.read_bytes() == raw, "E_COLLECT_WRITE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require(sum((args.collect, args.content_only, args.verify_staged, args.verify_persistence)) == 1, "E_CLI_MODE")
    require((args.verify_persistence and args.expected_commit is not None) or (
        not args.verify_persistence and args.expected_commit is None
    ), "E_EXPECTED_COMMIT_MODE")
    validate_source_policy()
    if args.collect:
        validate_worktree(set(NONSELF_PATHS), staged=False)
        first = build_payload()
        second = build_payload()
        first_raw = canonical_bytes(first)
        require(first_raw == canonical_bytes(second), "E_DETERMINISM", "2/2")
        named_passed, named_total = run_named_controls(first)
        git_passed, git_total = run_git_boundary_controls()
        require(git_total == 19, "E_GIT_CONTROL_COUNT", str(git_total))
        atomic_collect(first_raw)
        print(f"PASS_P066_PLAN_CONTROLS named={named_passed}/{named_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print("PASS_P066_PLAN_DETERMINISM 2/2")
        print("PASS_P066_PLAN_ACTIVATION collect=JSON_LAST result_first=true historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21")
        return 0

    stored, stored_raw, nodes, depth = read_stored()
    first = build_payload()
    second = build_payload()
    expected_raw = canonical_bytes(first)
    require(expected_raw == canonical_bytes(second), "E_DETERMINISM", "2/2")
    validate_document_bytes(stored_raw, first, expected_raw)
    named_passed, named_total = run_named_controls(stored)
    require(stored["negative_contract"]["actual_git_cases"] == 19, "E_GIT_BOUNDARY_STORED")
    require(stored["historical_execution"] == {
        "canonical_reused": 21,
        "precommit_reused": 14,
        "persistence_reused": 7,
        "fresh_replay": 0,
        "predecessor_git_boundary_reused": 17,
    }, "E_HISTORY_STORED")
    print(f"PASS_P066_PLAN_CONTROLS named={named_passed}/{named_total} strict_json=6/6 git_boundary=CANONICAL_REUSED_19/19")
    print("PASS_P066_PLAN_DETERMINISM 2/2")
    if args.content_only:
        validate_worktree(FINAL_PATH_SET, staged=False)
        print(f"PASS_P066_PLAN_CONTENT occurrences=433 unique_blobs=167 json_nodes={nodes} depth={depth} historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21")
    elif args.verify_staged:
        validate_worktree(FINAL_PATH_SET, staged=True)
        print("PASS_P066_PLAN_ACTIVATION_STAGED exact-seven=7/7 historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21")
    else:
        expected_commit = validate_expected_commit(args.expected_commit)
        validate_persistence(expected_commit)
        print(f"{PERSISTENCE} commit={expected_commit} historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError,
            subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, ValidationError) else str(type(error))
        print(f"FAIL_P066_PLAN_CONTENT {code}: {error}")
        raise SystemExit(1)
