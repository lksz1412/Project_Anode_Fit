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
import subprocess
from typing import Any, Callable


ROOT = pathlib.Path(__file__).resolve().parents[3]

PLAN_PATH = "Codex/plans/2026-09-02-phase067-plan-activation-persistence-repair-addendum.md"
VALIDATOR_PATH = "Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py"
OUTPUT_PATH = "Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_VALIDATION.json"
RESULT_PATH = "Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ORIGINAL_PLAN_PATH = "Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md"
ORIGINAL_VALIDATOR_PATH = "Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py"
ORIGINAL_JSON_PATH = "Codex/results/PHASE_067_PLAN_ACTIVATION_VALIDATION.json"
ORIGINAL_RESULT_PATH = "Codex/results/PHASE_067_PLAN_ACTIVATION_RESULT.md"

ACTIVATION_COMMIT = "7e5529658ef15443df7e8bea6f8aefaa081f0d2d"
ACTIVATION_PARENT = "7241b331ff76bc8d43cb1bc6b69634977e0884a0"
ACTIVATION_SUBJECT = "docs(phase067): plan code test fitting cross-audit"
REPAIR_SUBJECT = "fix(phase067): repair activation persistence proof"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{ACTIVE_BRANCH}"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
CLAUDE_BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"

CONTENT_GATE = "PASS_P067_ACTIVATION_REPAIR"
PERSISTENCE_TERMINAL = "PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR"
PRECOMMIT_STATUS = "PASS_PENDING_PERSISTENCE"
SCHEMA = "phase067-activation-persistence-repair-v1"

FINAL_PATHS = [
    PLAN_PATH,
    VALIDATOR_PATH,
    OUTPUT_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
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
NONSELF_STATUS = {path: FINAL_STATUS[path] for path in NONSELF_PATHS}

ORIGINAL_PATHS = [
    ORIGINAL_PLAN_PATH,
    ORIGINAL_VALIDATOR_PATH,
    ORIGINAL_JSON_PATH,
    ORIGINAL_RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
ORIGINAL_STATUS = {
    ORIGINAL_PLAN_PATH: "A",
    ORIGINAL_VALIDATOR_PATH: "A",
    ORIGINAL_JSON_PATH: "A",
    ORIGINAL_RESULT_PATH: "A",
    PARENT_LEDGER_PATH: "M",
    ACTIVE_LEDGER_PATH: "M",
    HANDOVER_PATH: "M",
}
ORIGINAL_FIXED_LF_HASHES = {
    ORIGINAL_PLAN_PATH: "a1ab5865581da95d71a86e5e6763f66ab0a4b42470d9fc00171355994e49ebf7",
    ORIGINAL_VALIDATOR_PATH: "d12577840a66db8e28fd2d94fe53a2c7277c496fccbc947ad83a66e8688b0949",
    ORIGINAL_JSON_PATH: "b178b7bc25dfe9be9eaf478c9760702d240fb686ba393327c96dc048c463e15a",
    ORIGINAL_RESULT_PATH: "7bc7aad461247650e0bb2b4c170202420eed4367bcf875fa9dc1e9af7a497ce7",
}
ORIGINAL_JSON_SEMANTIC = "b3a3ea02404db412dc55e8182b42f726837b6e652540abe15e82a951fddc77a3"
IMMUTABLE_WORKTREE_PATHS = [
    ORIGINAL_PLAN_PATH,
    ORIGINAL_VALIDATOR_PATH,
    ORIGINAL_JSON_PATH,
    ORIGINAL_RESULT_PATH,
]

FAILURE_STDOUT = b"FAIL_P067_PLAN_CONTENT E_REPOSITORY_HEAD: E_REPOSITORY_HEAD\r\n"
FAILURE_STDOUT_SHA256 = "3aff633deb85e468551238987ded68176ce1b12e641e6487a9d71f9ba3b50140"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

ALL_READ_PATHS = set(FINAL_PATHS) | set(ORIGINAL_PATHS) | {"Claude"}


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_oid(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw, usedforsecurity=False).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def file_mode(path: str) -> str:
    full = ROOT / path
    require(full.is_file(), "E_FILE_MISSING", path)
    return "100755" if full.stat().st_mode & 0o111 else "100644"


def read_worktree_lf(path: str) -> bytes:
    full = ROOT / path
    require(full.is_file(), "E_FILE_MISSING", path)
    return lf_bytes(full.read_bytes())


def artifact_seal(path: str, raw: bytes, mode: str = "100644") -> dict[str, Any]:
    normalized = lf_bytes(raw)
    return {
        "path": path,
        "status": FINAL_STATUS[path],
        "mode": mode,
        "bytes_lf": len(normalized),
        "lines": len(normalized.splitlines()),
        "sha256_lf": sha256(normalized),
    }


def canonical_bytes(document: dict[str, Any]) -> bytes:
    return (json.dumps(
        document, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False,
    ) + "\n").encode("utf-8")


def semantic_hash(document: dict[str, Any]) -> str:
    candidate = copy.deepcopy(document)
    candidate["semantic_sha256"] = ""
    return sha256(canonical_bytes(candidate))


def reject_constant(value: str) -> None:
    raise ValidationError("E_JSON_NONFINITE", value)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def inspect_json(value: Any, depth: int = 0) -> tuple[int, int, int]:
    require(depth <= 32, "E_JSON_DEPTH", str(depth))
    if isinstance(value, float):
        require(math.isfinite(value), "E_JSON_NONFINITE", repr(value))
    if isinstance(value, dict):
        nodes = 1
        scalars = 0
        maximum = depth
        for key, item in value.items():
            require(type(key) is str, "E_JSON_KEY", repr(key))
            child_nodes, child_scalars, child_depth = inspect_json(item, depth + 1)
            nodes += child_nodes
            scalars += child_scalars
            maximum = max(maximum, child_depth)
        return nodes, scalars, maximum
    if isinstance(value, list):
        nodes = 1
        scalars = 0
        maximum = depth
        for item in value:
            child_nodes, child_scalars, child_depth = inspect_json(item, depth + 1)
            nodes += child_nodes
            scalars += child_scalars
            maximum = max(maximum, child_depth)
        return nodes, scalars, maximum
    require(value is None or type(value) in {str, int, float, bool}, "E_JSON_TYPE")
    return 1, 1, depth


def strict_load_bytes(raw: bytes, label: str) -> tuple[dict[str, Any], int, int, int]:
    require(not raw.startswith(b"\xef\xbb\xbf"), "E_JSON_BOM", label)
    require(b"\r" not in raw, "E_JSON_CR", label)
    require(raw.endswith(b"\n"), "E_JSON_TERMINAL_NEWLINE", label)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValidationError("E_JSON_UTF8", label) from error
    try:
        document = json.loads(
            text, object_pairs_hook=reject_pairs, parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValidationError("E_JSON_SYNTAX", f"{label}:{error.msg}") from error
    require(type(document) is dict, "E_JSON_ROOT", label)
    nodes, scalars, depth = inspect_json(document)
    return document, nodes, scalars, depth


def strict_canonical_document(raw: bytes, label: str) -> tuple[dict[str, Any], int, int, int]:
    document, nodes, scalars, depth = strict_load_bytes(raw, label)
    require(canonical_bytes(document) == raw, "E_JSON_CANONICAL", label)
    return document, nodes, scalars, depth


def git_oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def read_paths_shape(paths: list[str], *, claude_only: bool = False) -> bool:
    if claude_only:
        return paths == ["Claude"]
    return bool(paths) and len(paths) == len(set(paths)) and set(paths) <= ALL_READ_PATHS


def validate_git_argv(args: list[str]) -> None:
    require(bool(args), "E_GIT_EMPTY")
    command = args[0]
    if command == "branch":
        require(args == ["branch", "--show-current"], "E_GIT_BRANCH_SHAPE", repr(args))
    elif command == "rev-parse":
        allowed = [
            ["rev-parse", "HEAD"],
            ["rev-parse", "@{upstream}"],
            ["rev-parse", "--abbrev-ref", "@{upstream}"],
            ["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"],
            ["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"],
            ["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"],
            ["rev-parse", "refs/remotes/origin/main"],
        ]
        require(args in allowed,
                "E_GIT_REV_PARSE_SHAPE", repr(args))
    elif command == "remote":
        require(args == ["remote", "get-url", "origin"], "E_GIT_REMOTE_SHAPE", repr(args))
    elif command == "ls-remote":
        allowed = {
            f"refs/heads/{ACTIVE_BRANCH}",
            f"refs/heads/{PROTECTED_BRANCH}",
            "refs/heads/main",
        }
        require(len(args) == 3 and args[1] == "origin" and args[2] in allowed,
                "E_GIT_LS_REMOTE_SHAPE", repr(args))
    elif command == "show-ref":
        require(args == ["show-ref", "--verify", "--quiet", "refs/heads/main"],
                "E_GIT_SHOW_REF_SHAPE", repr(args))
    elif command == "show":
        metadata = (
            len(args) == 4
            and args[1] == "-s"
            and args[2] in {"--format=%P", "--format=%s"}
            and git_oid(args[3])
        )
        blob = False
        if len(args) == 2 and ":" in args[1]:
            revision, path = args[1].split(":", 1)
            blob = (revision == "" or git_oid(revision)) and path in ALL_READ_PATHS
        require(metadata or blob, "E_GIT_SHOW_SHAPE", repr(args))
    elif command == "diff-tree":
        require(
            len(args) == 7
            and args[1:6] == [
                "--no-commit-id", "--no-renames", "--name-status", "-z", "-r",
            ]
            and git_oid(args[6]),
            "E_GIT_DIFF_TREE_SHAPE",
            repr(args),
        )
    elif command == "diff":
        require(
            len(args) == 6
            and args[1] == "--quiet"
            and git_oid(args[2])
            and git_oid(args[3])
            and args[4:] == ["--", "Claude"],
            "E_GIT_DIFF_SHAPE",
            repr(args),
        )
    elif command == "ls-tree":
        require(
            len(args) >= 5
            and args[1] == "-z"
            and git_oid(args[2])
            and args[3] == "--"
            and read_paths_shape(args[4:]),
            "E_GIT_LS_TREE_SHAPE",
            repr(args),
        )
    elif command == "ls-files":
        require(
            args[:4] == ["ls-files", "--stage", "-z", "--"]
            and args[4:] == FINAL_PATHS,
            "E_GIT_LS_FILES_SHAPE",
            repr(args),
        )
    elif command == "status":
        require(args == ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
                "E_GIT_STATUS_SHAPE", repr(args))
    else:
        require(False, "E_GIT_SUBCOMMAND", repr(args))


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    actual = list(args)
    validate_git_argv(actual)
    process = subprocess.run(
        ["git", *actual], cwd=ROOT, capture_output=True, timeout=300,
        check=False, shell=False,
    )
    if check and process.returncode != 0:
        raise ValidationError(
            "E_GIT_PROCESS",
            f"{actual!r}:{process.stderr.decode('utf-8', errors='replace')[-800:]}",
        )
    return process


def git_text(args: list[str]) -> str:
    return run_git(args).stdout.decode("utf-8", errors="strict").strip()


def git_blob(commit: str, path: str) -> bytes:
    require(git_oid(commit), "E_COMMIT_OID", commit)
    require(path in ALL_READ_PATHS and path != "Claude", "E_GIT_BLOB_PATH", path)
    return run_git(["show", f"{commit}:{path}"]).stdout


def index_blob(path: str) -> bytes:
    require(path in FINAL_PATHS, "E_INDEX_BLOB_PATH", path)
    return run_git(["show", f":{path}"]).stdout


def live_tip(branch: str) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"]).splitlines()
    require(len(lines) == 1, "E_LIVE_REF", branch)
    fields = lines[0].split("\t", 1)
    require(len(fields) == 2 and git_oid(fields[0]), "E_LIVE_REF_PARSE", branch)
    return fields[0]


def parse_name_status(raw: bytes) -> dict[str, str]:
    fields = raw.decode("utf-8", errors="strict").split("\0")
    if fields and fields[-1] == "":
        fields.pop()
    require(len(fields) % 2 == 0, "E_NAME_STATUS_PARSE", repr(fields[-3:]))
    result: dict[str, str] = {}
    for index in range(0, len(fields), 2):
        status, path = fields[index], fields[index + 1]
        require(status in {"A", "M", "D"}, "E_NAME_STATUS_CODE", status)
        require(path not in result, "E_NAME_STATUS_DUPLICATE", path)
        result[path] = status
    return result


def commit_status(commit: str) -> dict[str, str]:
    return parse_name_status(run_git([
        "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-z", "-r", commit,
    ]).stdout)


def tree_entries(commit: str, paths: list[str]) -> dict[str, dict[str, str]]:
    raw = run_git(["ls-tree", "-z", commit, "--", *paths]).stdout
    fields = raw.decode("utf-8", errors="strict").split("\0")
    result: dict[str, dict[str, str]] = {}
    for field in fields:
        if not field:
            continue
        metadata, path = field.split("\t", 1)
        mode, kind, blob_oid = metadata.split(" ", 2)
        require(kind == "blob", "E_TREE_KIND", f"{path}:{kind}")
        require(path not in result, "E_TREE_DUPLICATE", path)
        result[path] = {"mode": mode, "blob_oid": blob_oid}
    return result


def index_entries() -> dict[str, dict[str, str]]:
    raw = run_git(["ls-files", "--stage", "-z", "--", *FINAL_PATHS]).stdout
    fields = raw.decode("utf-8", errors="strict").split("\0")
    result: dict[str, dict[str, str]] = {}
    for field in fields:
        if not field:
            continue
        metadata, path = field.split("\t", 1)
        mode, blob_oid, stage = metadata.split(" ", 2)
        require(stage == "0", "E_INDEX_STAGE", f"{path}:{stage}")
        require(path not in result, "E_INDEX_DUPLICATE", path)
        result[path] = {"mode": mode, "blob_oid": blob_oid}
    return result


def porcelain_records() -> dict[str, str]:
    raw = run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    fields = raw.decode("utf-8", errors="strict").split("\0")
    result: dict[str, str] = {}
    for field in fields:
        if not field:
            continue
        require(len(field) >= 4 and field[2] == " ", "E_STATUS_PARSE", repr(field))
        code = field[:2]
        path = field[3:]
        require("R" not in code and "C" not in code and "D" not in code,
                "E_STATUS_RENAME_COPY_DELETE", f"{code}:{path}")
        require(path not in result, "E_STATUS_DUPLICATE", path)
        result[path] = code
    return result


def validate_expected_commit(value: str | None) -> str:
    require(value is not None and git_oid(value), "E_EXPECTED_COMMIT", repr(value))
    return value


def validate_repository_record(record: dict[str, Any], expected_tip: str) -> None:
    require(record.get("active_branch") == ACTIVE_BRANCH,
            "E_REPOSITORY_BRANCH", str(record.get("active_branch")))
    require(record.get("head") == expected_tip,
            "E_REPOSITORY_HEAD", str(record.get("head")))
    require(record.get("upstream_name") == UPSTREAM,
            "E_REPOSITORY_UPSTREAM_NAME", str(record.get("upstream_name")))
    require(record.get("upstream_oid") == expected_tip,
            "E_REPOSITORY_UPSTREAM", str(record.get("upstream_oid")))
    require(record.get("active_tracking_oid") == expected_tip,
            "E_REPOSITORY_ACTIVE_TRACKING", str(record.get("active_tracking_oid")))
    require(record.get("live_origin") == expected_tip,
            "E_REPOSITORY_LIVE", str(record.get("live_origin")))
    require(record.get("origin_url") == ORIGIN_URL,
            "E_REPOSITORY_ORIGIN", str(record.get("origin_url")))
    require(record.get("protected_live_oid") == PROTECTED_TIP,
            "E_REPOSITORY_PROTECTED_LIVE", str(record.get("protected_live_oid")))
    require(record.get("protected_local_oid") == PROTECTED_TIP,
            "E_REPOSITORY_PROTECTED_LOCAL", str(record.get("protected_local_oid")))
    require(record.get("protected_tracking_oid") == PROTECTED_TIP,
            "E_REPOSITORY_PROTECTED_TRACKING", str(record.get("protected_tracking_oid")))
    require(record.get("main_live_oid") == MAIN_TIP,
            "E_REPOSITORY_MAIN_LIVE", str(record.get("main_live_oid")))
    require(record.get("main_tracking_oid") == MAIN_TIP,
            "E_REPOSITORY_MAIN_TRACKING", str(record.get("main_tracking_oid")))
    require(record.get("local_main_absent") is True, "E_REPOSITORY_LOCAL_MAIN")


def repository_refs(expected_tip: str) -> dict[str, Any]:
    require(git_oid(expected_tip), "E_EXPECTED_TIP", expected_tip)
    branch = git_text(["branch", "--show-current"])
    head = git_text(["rev-parse", "HEAD"])
    upstream_name = git_text(["rev-parse", "--abbrev-ref", "@{upstream}"])
    upstream_oid = git_text(["rev-parse", "@{upstream}"])
    active_tracking_oid = git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"])
    live = live_tip(ACTIVE_BRANCH)
    origin_url = git_text(["remote", "get-url", "origin"])
    protected_live = live_tip(PROTECTED_BRANCH)
    protected_local = git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"])
    protected_tracking = git_text([
        "rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}",
    ])
    main_live = live_tip("main")
    main_tracking = git_text(["rev-parse", "refs/remotes/origin/main"])
    local_main = run_git(
        ["show-ref", "--verify", "--quiet", "refs/heads/main"], check=False,
    ).returncode == 0
    record = {
        "active_branch": branch,
        "head": head,
        "upstream_name": upstream_name,
        "upstream_oid": upstream_oid,
        "active_tracking_oid": active_tracking_oid,
        "live_origin": live,
        "origin_url": origin_url,
        "protected_live_oid": protected_live,
        "protected_local_oid": protected_local,
        "protected_tracking_oid": protected_tracking,
        "main_live_oid": main_live,
        "main_tracking_oid": main_tracking,
        "local_main_absent": not local_main,
    }
    validate_repository_record(record, expected_tip)
    return record


def diff_quiet(left: str, right: str, path: str) -> bool:
    require(path == "Claude", "E_DIFF_PATH", path)
    return run_git(["diff", "--quiet", left, right, "--", path], check=False).returncode == 0


def protected_boundary(target_commit: str) -> dict[str, Any]:
    require(diff_quiet(CLAUDE_BASELINE, ACTIVATION_COMMIT, "Claude"),
            "E_CLAUDE_BASELINE_ACTIVATION")
    require(diff_quiet(ACTIVATION_COMMIT, target_commit, "Claude"),
            "E_CLAUDE_ACTIVATION_TARGET")
    return {
        "claude_baseline": CLAUDE_BASELINE,
        "activation_to_target_diff_zero": True,
        "baseline_to_activation_diff_zero": True,
        "protected_tip": PROTECTED_TIP,
        "main_tip": MAIN_TIP,
    }


def validate_activation_view(view: dict[str, Any]) -> None:
    require(view.get("commit") == ACTIVATION_COMMIT, "E_ORIGINAL_COMMIT")
    require(view.get("parents") == [ACTIVATION_PARENT], "E_ORIGINAL_PARENT")
    require(view.get("subject") == ACTIVATION_SUBJECT, "E_ORIGINAL_SUBJECT")
    require(view.get("paths") == ORIGINAL_PATHS, "E_ORIGINAL_PATHS")
    require(view.get("status") == [ORIGINAL_STATUS[path] for path in ORIGINAL_PATHS],
            "E_ORIGINAL_STATUS")
    require(view.get("modes") == ["100644"] * 7, "E_ORIGINAL_MODES")
    blobs = view.get("committed_blobs")
    require(type(blobs) is list and len(blobs) == 7, "E_ORIGINAL_BLOBS")
    for index, path in enumerate(ORIGINAL_PATHS):
        row = blobs[index]
        require(type(row) is dict and row.get("path") == path, "E_ORIGINAL_BLOB_PATH")
        require(row.get("status") == ORIGINAL_STATUS[path], "E_ORIGINAL_BLOB_STATUS", path)
        require(row.get("mode") == "100644", "E_ORIGINAL_BLOB_MODE", path)
        require(git_oid(row.get("blob_oid", "")), "E_ORIGINAL_BLOB_OID", path)
        require(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256_lf", "")) is not None,
                "E_ORIGINAL_BLOB_HASH", path)
        if path in ORIGINAL_FIXED_LF_HASHES:
            require(row["sha256_lf"] == ORIGINAL_FIXED_LF_HASHES[path],
                    "E_ORIGINAL_FIXED_HASH", path)
    require(view.get("current_head_independent") is True, "E_OLD_HEAD_CONFLATION")


def original_activation_certificate() -> dict[str, Any]:
    parents = git_text(["show", "-s", "--format=%P", ACTIVATION_COMMIT]).split()
    subject = git_text(["show", "-s", "--format=%s", ACTIVATION_COMMIT])
    status = commit_status(ACTIVATION_COMMIT)
    require(status == ORIGINAL_STATUS, "E_ORIGINAL_COMMIT_STATUS", repr(status))
    entries = tree_entries(ACTIVATION_COMMIT, ORIGINAL_PATHS)
    require(set(entries) == set(ORIGINAL_PATHS), "E_ORIGINAL_TREE_PATHS")
    blobs = []
    for path in ORIGINAL_PATHS:
        raw = git_blob(ACTIVATION_COMMIT, path)
        row = {
            "path": path,
            "status": ORIGINAL_STATUS[path],
            "mode": entries[path]["mode"],
            "blob_oid": entries[path]["blob_oid"],
            "bytes_lf": len(lf_bytes(raw)),
            "lines": len(lf_bytes(raw).splitlines()),
            "sha256_lf": sha256(lf_bytes(raw)),
        }
        blobs.append(row)
    original_json_raw = git_blob(ACTIVATION_COMMIT, ORIGINAL_JSON_PATH)
    original_json, _, _, _ = strict_canonical_document(
        original_json_raw, f"{ACTIVATION_COMMIT}:{ORIGINAL_JSON_PATH}",
    )
    require(sha256(lf_bytes(original_json_raw)) == ORIGINAL_FIXED_LF_HASHES[ORIGINAL_JSON_PATH],
            "E_ORIGINAL_JSON_RAW_HASH")
    require(original_json.get("semantic_sha256") == ORIGINAL_JSON_SEMANTIC,
            "E_ORIGINAL_JSON_SEMANTIC_FIELD")
    require(semantic_hash(original_json) == ORIGINAL_JSON_SEMANTIC,
            "E_ORIGINAL_JSON_SEMANTIC_RECONSTRUCTION")
    require(original_json.get("gate") == "PASS_P067_PLAN_ACTIVATION",
            "E_ORIGINAL_JSON_GATE")
    require(original_json.get("status") == "PASS_PENDING_PERSISTENCE",
            "E_ORIGINAL_JSON_PRECOMMIT")
    certificate = {
        "commit": ACTIVATION_COMMIT,
        "parents": parents,
        "subject": subject,
        "paths": ORIGINAL_PATHS,
        "status": [ORIGINAL_STATUS[path] for path in ORIGINAL_PATHS],
        "modes": [entries[path]["mode"] for path in ORIGINAL_PATHS],
        "committed_blobs": blobs,
        "original_gate": "PASS_P067_PLAN_ACTIVATION",
        "original_persistence_terminal_obtained": False,
        "original_persistence_diagnostic": "E_REPOSITORY_HEAD",
        "json_semantic_sha256": ORIGINAL_JSON_SEMANTIC,
        "current_head_independent": True,
    }
    validate_activation_view(certificate)
    return certificate


def validate_original_immutable_worktree() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in IMMUTABLE_WORKTREE_PATHS:
        committed = lf_bytes(git_blob(ACTIVATION_COMMIT, path))
        working = read_worktree_lf(path)
        require(working == committed, "E_ORIGINAL_IMMUTABLE_WORKTREE", path)
        hashes[path] = sha256(working)
    return hashes


def expected_status_codes(expected: dict[str, str], *, staged: bool) -> dict[str, str]:
    if staged:
        return {path: ("A " if status == "A" else "M ") for path, status in expected.items()}
    return {path: ("??" if status == "A" else " M") for path, status in expected.items()}


def validate_change_snapshot(*, include_output: bool, staged: bool) -> dict[str, Any]:
    expected = FINAL_STATUS if include_output else NONSELF_STATUS
    records = porcelain_records()
    require(records == expected_status_codes(expected, staged=staged),
            "E_REPAIR_STATUS", repr(records))
    modes = {path: file_mode(path) for path in expected}
    require(modes == {path: "100644" for path in expected}, "E_REPAIR_MODES", repr(modes))
    worktree_hashes = {path: sha256(read_worktree_lf(path)) for path in expected}
    if staged:
        entries = index_entries()
        require(set(entries) == set(FINAL_PATHS), "E_REPAIR_INDEX_PATHS", repr(entries))
        index_modes = {path: entries[path]["mode"] for path in FINAL_PATHS}
        require(index_modes == {path: "100644" for path in FINAL_PATHS},
                "E_REPAIR_INDEX_MODES")
        index_hashes = {}
        index_blob_oids = {}
        reconstructed_blob_oids = {}
        for path in FINAL_PATHS:
            raw = index_blob(path)
            normalized = lf_bytes(raw)
            require(normalized == read_worktree_lf(path), "E_REPAIR_INDEX_WORKTREE_BLOB", path)
            index_hashes[path] = sha256(normalized)
            index_blob_oids[path] = entries[path]["blob_oid"]
            reconstructed_blob_oids[path] = git_blob_oid(raw)
    else:
        index_modes = {}
        index_hashes = {}
        index_blob_oids = {}
        reconstructed_blob_oids = {}
    snapshot = {
        "paths": list(expected),
        "status": [expected[path] for path in expected],
        "modes": [modes[path] for path in expected],
        "worktree_hashes": worktree_hashes,
        "index_modes": index_modes,
        "index_hashes": index_hashes,
        "index_blob_oids": index_blob_oids,
        "reconstructed_blob_oids": reconstructed_blob_oids,
    }
    if staged:
        validate_staged_record(snapshot)
    return snapshot


def validate_staged_record(record: dict[str, Any]) -> None:
    require(record.get("paths") == FINAL_PATHS, "E_STAGED_PATHS")
    require(record.get("status") == [FINAL_STATUS[path] for path in FINAL_PATHS],
            "E_STAGED_STATUS")
    require(record.get("modes") == ["100644"] * 7, "E_STAGED_WORKTREE_MODES")
    require(record.get("index_modes") == {path: "100644" for path in FINAL_PATHS},
            "E_STAGED_INDEX_MODES")
    worktree_hashes = record.get("worktree_hashes")
    index_hashes = record.get("index_hashes")
    require(type(worktree_hashes) is dict and set(worktree_hashes) == set(FINAL_PATHS),
            "E_STAGED_WORKTREE_HASHES")
    require(index_hashes == worktree_hashes, "E_STAGED_INDEX_BLOB_HASH")
    index_oids = record.get("index_blob_oids")
    reconstructed = record.get("reconstructed_blob_oids")
    require(type(index_oids) is dict and set(index_oids) == set(FINAL_PATHS),
            "E_STAGED_INDEX_BLOB_OIDS")
    require(all(git_oid(index_oids[path]) for path in FINAL_PATHS),
            "E_STAGED_INDEX_BLOB_OID_FORMAT")
    require(reconstructed == index_oids, "E_STAGED_INDEX_BLOB_IDENTITY")


def validate_staged_document_binding(record: dict[str, Any], document: dict[str, Any]) -> None:
    recorded = {
        row["path"]: row["sha256_lf"]
        for row in document["repair_transaction"]["nonself_artifacts"]
    }
    require(
        {path: record["index_hashes"][path] for path in NONSELF_PATHS} == recorded,
        "E_STAGED_NONSELF_BINDING",
    )


def assert_control_documents(source_commit: str | None) -> None:
    def text(path: str) -> str:
        raw = git_blob(source_commit, path) if source_commit else read_worktree_lf(path)
        return lf_bytes(raw).decode("utf-8", errors="strict")

    plan = text(PLAN_PATH)
    result = text(RESULT_PATH)
    parent = text(PARENT_LEDGER_PATH)
    active = text(ACTIVE_LEDGER_PATH)
    handover = text(HANDOVER_PATH)
    shared = [parent, active, handover]
    for token in (
        ACTIVATION_COMMIT, ACTIVATION_PARENT, REPAIR_SUBJECT, CONTENT_GATE,
        PERSISTENCE_TERMINAL, "E_REPOSITORY_HEAD", "Step 82", "blocked",
    ):
        require(token in plan and token in result, "E_CONTROL_PLAN_RESULT_TOKEN", token)
        require(all(token in document for document in shared), "E_CONTROL_RECOVERY_TOKEN", token)
    for path in FINAL_PATHS:
        require(path in plan and path in result, "E_CONTROL_EXACT_PATH", path)
    require("PENDING_AT_PRECOMMIT_BY_DESIGN" in result, "E_CONTROL_PRECOMMIT_BOUNDARY")
    require("same repair child OID" in result, "E_CONTROL_SAME_CHILD")
    require("P0/P1=`0/0`" in result, "E_CONTROL_REVIEW_BOUNDARY")
    require(active.count("| Phase 067 plan activation |") == 1,
            "E_CONTROL_ACTIVATION_COMMIT_ROW")
    require(active.count("| Phase 067 activation persistence repair |") == 1,
            "E_CONTROL_REPAIR_COMMIT_ROW")
    require("original persistence terminal `NOT_OBTAINED`" in active,
            "E_CONTROL_ORIGINAL_TERMINAL")
    stale_next = "Complete the Phase 067 exact-seven activation snapshot"
    require(all(stale_next not in document for document in shared),
            "E_CONTROL_STALE_NEXT")
    require(active.count("## Next Exact Step") == 1, "E_CONTROL_NEXT_HEADING")
    require(handover.count("## Exact Next Action") == 1, "E_CONTROL_HANDOVER_NEXT_HEADING")


def validate_repair_view(view: dict[str, Any]) -> None:
    require(view.get("expected_parent") == ACTIVATION_COMMIT, "E_REPAIR_PARENT")
    require(view.get("expected_subject") == REPAIR_SUBJECT, "E_REPAIR_SUBJECT")
    require(view.get("paths") == FINAL_PATHS, "E_REPAIR_PATHS")
    require(view.get("status") == [FINAL_STATUS[path] for path in FINAL_PATHS],
            "E_REPAIR_ORDERED_STATUS")
    require(view.get("modes") == ["100644"] * 7, "E_REPAIR_ORDERED_MODES")
    artifacts = view.get("nonself_artifacts")
    require(type(artifacts) is list and len(artifacts) == 6, "E_REPAIR_NONSELF_COUNT")
    require([row.get("path") for row in artifacts] == NONSELF_PATHS,
            "E_REPAIR_NONSELF_PATHS")
    for row in artifacts:
        require(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256_lf", "")) is not None,
                "E_REPAIR_NONSELF_HASH", str(row.get("path")))
    require(OUTPUT_PATH not in {row["path"] for row in artifacts}, "E_REPAIR_SELF_HASH")
    refs = view.get("precommit_ref_boundary")
    require(type(refs) is dict, "E_REPAIR_REFS")
    require(refs.get("head") == ACTIVATION_COMMIT, "E_REPAIR_REF_HEAD")
    require(refs.get("upstream_oid") == ACTIVATION_COMMIT, "E_REPAIR_REF_UPSTREAM")
    require(refs.get("live_origin") == ACTIVATION_COMMIT, "E_REPAIR_REF_LIVE")
    require(refs.get("protected_live_oid") == PROTECTED_TIP, "E_REPAIR_REF_PROTECTED")
    require(refs.get("main_live_oid") == MAIN_TIP, "E_REPAIR_REF_MAIN")
    require(refs.get("origin_url") == ORIGIN_URL, "E_REPAIR_REF_ORIGIN")
    validate_repository_record(refs, ACTIVATION_COMMIT)
    require(view.get("containing_commit") == "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "E_REPAIR_CONTAINING_COMMIT")
    require(view.get("staged_verified") is False and view.get("persistence_verified") is False,
            "E_REPAIR_PRECOMMIT_CLAIM")
    require(view.get("dirty") is False, "E_REPAIR_DIRTY")
    require(view.get("claude_diff_zero") is True, "E_REPAIR_CLAUDE_DRIFT")


def expect_error(expected: str, operation: Callable[[], None]) -> None:
    try:
        operation()
    except ValidationError as error:
        require(error.code == expected, "E_NEGATIVE_DIAGNOSTIC", f"{expected}:{error.code}")
    else:
        raise ValidationError("E_NEGATIVE_FALSE_PASS", expected)


def run_negative_controls(
    certificate: dict[str, Any], repair: dict[str, Any],
) -> tuple[dict[str, int], list[dict[str, str]]]:
    cases: list[tuple[str, str, Callable[[], None], str]] = []

    def original_mutation(name: str, code: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        def operation() -> None:
            candidate = copy.deepcopy(certificate)
            mutate(candidate)
            validate_activation_view(candidate)
        cases.append(("original", name, operation, code))

    original_mutation("old_head_conflation", "E_OLD_HEAD_CONFLATION",
                      lambda value: value.__setitem__("current_head_independent", False))
    original_mutation("parent_drift", "E_ORIGINAL_PARENT",
                      lambda value: value.__setitem__("parents", ["0" * 40]))
    original_mutation("subject_drift", "E_ORIGINAL_SUBJECT",
                      lambda value: value.__setitem__("subject", "drift"))
    original_mutation("path_drift", "E_ORIGINAL_PATHS",
                      lambda value: value["paths"].__setitem__(0, "Codex/drift"))
    original_mutation("mode_drift", "E_ORIGINAL_MODES",
                      lambda value: value["modes"].__setitem__(0, "100755"))
    original_mutation("blob_drift", "E_ORIGINAL_FIXED_HASH",
                      lambda value: value["committed_blobs"][0].__setitem__("sha256_lf", "0" * 64))

    def repair_mutation(name: str, code: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        def operation() -> None:
            candidate = copy.deepcopy(repair)
            mutate(candidate)
            validate_repair_view(candidate)
        cases.append(("repair", name, operation, code))

    repair_mutation("parent_drift", "E_REPAIR_PARENT",
                    lambda value: value.__setitem__("expected_parent", "0" * 40))
    repair_mutation("subject_drift", "E_REPAIR_SUBJECT",
                    lambda value: value.__setitem__("expected_subject", "drift"))
    repair_mutation("renamed_path", "E_REPAIR_PATHS",
                    lambda value: value["paths"].__setitem__(0, "Codex/drift"))
    repair_mutation("missing_path", "E_REPAIR_PATHS",
                    lambda value: value["paths"].pop())
    repair_mutation("extra_path", "E_REPAIR_PATHS",
                    lambda value: value["paths"].append("Codex/extra"))
    repair_mutation("reordered_path", "E_REPAIR_PATHS",
                    lambda value: value["paths"].reverse())
    repair_mutation("status_drift", "E_REPAIR_ORDERED_STATUS",
                    lambda value: value["status"].__setitem__(0, "M"))
    repair_mutation("mode_drift", "E_REPAIR_ORDERED_MODES",
                    lambda value: value["modes"].__setitem__(0, "100755"))
    repair_mutation("blob_drift", "E_REPAIR_NONSELF_HASH",
                    lambda value: value["nonself_artifacts"][0].__setitem__("sha256_lf", "x"))
    repair_mutation("head_ref_drift", "E_REPAIR_REF_HEAD",
                    lambda value: value["precommit_ref_boundary"].__setitem__("head", "0" * 40))
    repair_mutation("upstream_ref_drift", "E_REPAIR_REF_UPSTREAM",
                    lambda value: value["precommit_ref_boundary"].__setitem__("upstream_oid", "0" * 40))
    repair_mutation("live_ref_drift", "E_REPAIR_REF_LIVE",
                    lambda value: value["precommit_ref_boundary"].__setitem__("live_origin", "0" * 40))
    repair_mutation("protected_ref_drift", "E_REPAIR_REF_PROTECTED",
                    lambda value: value["precommit_ref_boundary"].__setitem__("protected_live_oid", "0" * 40))
    repair_mutation("main_ref_drift", "E_REPAIR_REF_MAIN",
                    lambda value: value["precommit_ref_boundary"].__setitem__("main_live_oid", "0" * 40))
    repair_mutation("origin_ref_drift", "E_REPAIR_REF_ORIGIN",
                    lambda value: value["precommit_ref_boundary"].__setitem__("origin_url", "x"))
    repair_mutation("upstream_name_drift", "E_REPOSITORY_UPSTREAM_NAME",
                    lambda value: value["precommit_ref_boundary"].__setitem__("upstream_name", "origin/drift"))
    repair_mutation("active_tracking_drift", "E_REPOSITORY_ACTIVE_TRACKING",
                    lambda value: value["precommit_ref_boundary"].__setitem__("active_tracking_oid", "0" * 40))
    repair_mutation("protected_local_drift", "E_REPOSITORY_PROTECTED_LOCAL",
                    lambda value: value["precommit_ref_boundary"].__setitem__("protected_local_oid", "0" * 40))
    repair_mutation("protected_tracking_drift", "E_REPOSITORY_PROTECTED_TRACKING",
                    lambda value: value["precommit_ref_boundary"].__setitem__("protected_tracking_oid", "0" * 40))
    repair_mutation("main_tracking_drift", "E_REPOSITORY_MAIN_TRACKING",
                    lambda value: value["precommit_ref_boundary"].__setitem__("main_tracking_oid", "0" * 40))
    repair_mutation("dirty_transaction", "E_REPAIR_DIRTY",
                    lambda value: value.__setitem__("dirty", True))
    repair_mutation("claude_drift", "E_REPAIR_CLAUDE_DRIFT",
                    lambda value: value.__setitem__("claude_diff_zero", False))

    staged_good = {
        "paths": FINAL_PATHS,
        "status": [FINAL_STATUS[path] for path in FINAL_PATHS],
        "modes": ["100644"] * 7,
        "worktree_hashes": {path: "1" * 64 for path in FINAL_PATHS},
        "index_modes": {path: "100644" for path in FINAL_PATHS},
        "index_hashes": {path: "1" * 64 for path in FINAL_PATHS},
        "index_blob_oids": {path: "2" * 40 for path in FINAL_PATHS},
        "reconstructed_blob_oids": {path: "2" * 40 for path in FINAL_PATHS},
    }

    def staged_mutation(name: str, code: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        def operation() -> None:
            candidate = copy.deepcopy(staged_good)
            mutate(candidate)
            validate_staged_record(candidate)
        cases.append(("staged", name, operation, code))

    staged_mutation("index_mode_drift", "E_STAGED_INDEX_MODES",
                    lambda value: value["index_modes"].__setitem__(FINAL_PATHS[0], "100755"))
    staged_mutation("index_hash_drift", "E_STAGED_INDEX_BLOB_HASH",
                    lambda value: value["index_hashes"].__setitem__(FINAL_PATHS[0], "0" * 64))
    staged_mutation("index_blob_identity_drift", "E_STAGED_INDEX_BLOB_IDENTITY",
                    lambda value: value["reconstructed_blob_oids"].__setitem__(FINAL_PATHS[0], "0" * 40))
    binding_record = copy.deepcopy(staged_good)
    for row in repair["nonself_artifacts"]:
        binding_record["index_hashes"][row["path"]] = row["sha256_lf"]
        binding_record["worktree_hashes"][row["path"]] = row["sha256_lf"]

    def staged_nonself_binding_drift() -> None:
        candidate = copy.deepcopy(binding_record)
        candidate["index_hashes"][NONSELF_PATHS[0]] = "0" * 64
        validate_staged_document_binding(
            candidate, {"repair_transaction": {"nonself_artifacts": repair["nonself_artifacts"]}},
        )

    cases.append((
        "staged", "nonself_binding_drift", staged_nonself_binding_drift,
        "E_STAGED_NONSELF_BINDING",
    ))

    json_cases = [
        ("duplicate_key", "E_JSON_DUPLICATE", lambda: strict_load_bytes(b'{"a":1,"a":2}\n', "probe")),
        ("nonfinite", "E_JSON_NONFINITE", lambda: strict_load_bytes(b'{"a":NaN}\n', "probe")),
        ("bom", "E_JSON_BOM", lambda: strict_load_bytes(b'\xef\xbb\xbf{}\n', "probe")),
        ("cr", "E_JSON_CR", lambda: strict_load_bytes(b'{}\r\n', "probe")),
        ("terminal_newline", "E_JSON_TERMINAL_NEWLINE", lambda: strict_load_bytes(b'{}', "probe")),
        ("root", "E_JSON_ROOT", lambda: strict_load_bytes(b'[]\n', "probe")),
        ("canonical", "E_JSON_CANONICAL", lambda: strict_canonical_document(b'{"a":1}\n', "probe")),
    ]
    for name, code, operation in json_cases:
        cases.append(("strict_json", name, operation, code))

    git_cases = [
        ("branch_create", "E_GIT_BRANCH_SHAPE", lambda: validate_git_argv(["branch", "created-by-probe"])),
        ("branch_delete", "E_GIT_BRANCH_SHAPE", lambda: validate_git_argv(["branch", "-D", "main"])),
        ("remote_set_url", "E_GIT_REMOTE_SHAPE", lambda: validate_git_argv(["remote", "set-url", "origin", "x"])),
        ("diff_output", "E_GIT_DIFF_SHAPE", lambda: validate_git_argv(["diff", "--output=x"])),
        ("unknown_subcommand", "E_GIT_SUBCOMMAND", lambda: validate_git_argv(["clean", "-fd"])),
        ("status_unknown_option", "E_GIT_STATUS_SHAPE", lambda: validate_git_argv(["status", "--short"])),
    ]
    for name, code, operation in git_cases:
        cases.append(("git_argv", name, operation, code))

    cli_cases = [
        ("missing", "E_EXPECTED_COMMIT", lambda: validate_expected_commit(None)),
        ("uppercase", "E_EXPECTED_COMMIT", lambda: validate_expected_commit("A" * 40)),
        ("option_injection", "E_EXPECTED_COMMIT", lambda: validate_expected_commit("--help")),
    ]
    for name, code, operation in cli_cases:
        cases.append(("cli", name, operation, code))

    records = []
    counts: dict[str, int] = {}
    for family, name, operation, code in cases:
        expect_error(code, operation)
        counts[family] = counts.get(family, 0) + 1
        records.append({"family": family, "name": name, "diagnostic": code})
    return counts, records


def source_bytes(path: str, source_commit: str | None) -> bytes:
    return lf_bytes(git_blob(source_commit, path)) if source_commit else read_worktree_lf(path)


def build_payload(
    source_commit: str | None = None,
    precommit_refs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    certificate = original_activation_certificate()
    assert_control_documents(source_commit)
    if precommit_refs is None:
        precommit_refs = repository_refs(ACTIVATION_COMMIT)
    validate_repository_record(precommit_refs, ACTIVATION_COMMIT)
    artifacts = [
        artifact_seal(path, source_bytes(path, source_commit)) for path in NONSELF_PATHS
    ]
    repair = {
        "expected_parent": ACTIVATION_COMMIT,
        "expected_subject": REPAIR_SUBJECT,
        "paths": FINAL_PATHS,
        "status": [FINAL_STATUS[path] for path in FINAL_PATHS],
        "modes": ["100644"] * 7,
        "nonself_artifacts": artifacts,
        "precommit_ref_boundary": copy.deepcopy(precommit_refs),
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "staged_verified": False,
        "persistence_verified": False,
        "dirty": False,
        "claude_diff_zero": True,
        "step82_blocked": True,
        "step82_release_requires": {
            "same_child_dual_runtime": True,
            "pushed_live_equal": True,
            "clean_worktree": True,
            "independent_p0_p1": "0/0",
        },
    }
    validate_repair_view(repair)
    counts, records = run_negative_controls(certificate, repair)
    failure_records = []
    for version in ("3.12", "3.14"):
        failure_records.append({
            "runtime": f"Python {version}",
            "argv": [
                "py", f"-{version}", "-B", ORIGINAL_VALIDATOR_PATH,
                "--verify-persistence", "--expected-commit", ACTIVATION_COMMIT,
            ],
            "entry_head": ACTIVATION_COMMIT,
            "returncode": 1,
            "stdout_bytes": len(FAILURE_STDOUT),
            "stdout_sha256": FAILURE_STDOUT_SHA256,
            "stderr_bytes": 0,
            "stderr_sha256": EMPTY_SHA256,
            "diagnostic": "E_REPOSITORY_HEAD",
        })
    document: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_date": "2026-09-02",
        "content_gate": CONTENT_GATE,
        "precommit_status": PRECOMMIT_STATUS,
        "persistence_terminal": PERSISTENCE_TERMINAL,
        "root_cause": {
            "classification": "PREDECESSOR_CURRENT_HEAD_CONFLATION",
            "original_validator_immutable": True,
            "activation_artifacts_immutable": True,
            "original_commit_valid": True,
            "original_terminal_obtained": False,
            "failure_evidence": failure_records,
            "explanation": (
                "original predecessor_contract calls repository_snapshot with the fixed "
                "Phase 066 predecessor instead of separating it from the Phase 067 current tip"
            ),
        },
        "original_activation_certificate": certificate,
        "repair_transaction": repair,
        "negative_contract": {
            "counts": counts,
            "total": sum(counts.values()),
            "records": records,
        },
        "determinism": {"reconstructions": 2, "byte_identical": True},
        "source_policy": {
            "exact_import_seal": True,
            "single_git_subprocess_site": True,
            "read_only_git_argv": True,
            "atomic_collect_only_mutation": True,
            "checks": 4,
        },
        "authority": {
            "production_modified": False,
            "claude_modified": False,
            "scientific_authority_promoted": False,
            "ref7_original_full_text": "GROUND_NOT_FOUND",
            "optimizer_state": "GROUND_NOT_FOUND",
            "heldout_external_material_open": True,
            "stale_pdf_open": True,
        },
        "semantic_sha256": "",
    }
    document["semantic_sha256"] = semantic_hash(document)
    return document


def assert_payload(document: dict[str, Any]) -> None:
    require(set(document) == {
        "schema", "generated_date", "content_gate", "precommit_status",
        "persistence_terminal", "root_cause", "original_activation_certificate",
        "repair_transaction", "negative_contract", "determinism", "source_policy",
        "authority", "semantic_sha256",
    }, "E_PAYLOAD_KEYS")
    require(document.get("schema") == SCHEMA, "E_PAYLOAD_SCHEMA")
    require(document.get("generated_date") == "2026-09-02", "E_PAYLOAD_DATE")
    require(document.get("content_gate") == CONTENT_GATE, "E_PAYLOAD_GATE")
    require(document.get("precommit_status") == PRECOMMIT_STATUS, "E_PAYLOAD_STATUS")
    require(document.get("persistence_terminal") == PERSISTENCE_TERMINAL,
            "E_PAYLOAD_TERMINAL")
    validate_activation_view(document.get("original_activation_certificate", {}))
    validate_repair_view(document.get("repair_transaction", {}))
    require(document.get("semantic_sha256") == semantic_hash(document), "E_PAYLOAD_SEMANTIC")
    repair = document["repair_transaction"]
    require(len(repair["nonself_artifacts"]) == 6, "E_PAYLOAD_SIX_HASHES")
    require(not any(
        key in repair for key in ("raw_sha256", "json_raw_sha256", "future_child_oid")
    ), "E_PAYLOAD_FORBIDDEN_SELF_OR_CHILD")
    failure = document.get("root_cause", {}).get("failure_evidence")
    require(type(failure) is list and len(failure) == 2, "E_FAILURE_EVIDENCE")
    for row, version in zip(failure, ("3.12", "3.14"), strict=True):
        require(row.get("argv") == [
            "py", f"-{version}", "-B", ORIGINAL_VALIDATOR_PATH,
            "--verify-persistence", "--expected-commit", ACTIVATION_COMMIT,
        ], "E_FAILURE_ARGV")
        require(row.get("runtime") == f"Python {version}", "E_FAILURE_RUNTIME")
        require(row.get("entry_head") == ACTIVATION_COMMIT, "E_FAILURE_HEAD")
        require(row.get("returncode") == 1, "E_FAILURE_RC")
        require(row.get("stdout_bytes") == 61, "E_FAILURE_STDOUT_BYTES")
        require(row.get("stdout_sha256") == FAILURE_STDOUT_SHA256, "E_FAILURE_STDOUT_HASH")
        require(row.get("stderr_bytes") == 0 and row.get("stderr_sha256") == EMPTY_SHA256,
                "E_FAILURE_STDERR")


def read_stored() -> tuple[dict[str, Any], bytes, int, int, int]:
    full = ROOT / OUTPUT_PATH
    require(full.is_file(), "E_OUTPUT_MISSING", OUTPUT_PATH)
    raw = full.read_bytes()
    document, nodes, scalars, depth = strict_canonical_document(raw, OUTPUT_PATH)
    assert_payload(document)
    return document, raw, nodes, scalars, depth


def atomic_collect(raw: bytes) -> None:
    output = ROOT / OUTPUT_PATH
    require(not output.exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST")
    temp_path = output.with_name(output.name + ".tmp-phase067-repair")
    require(not temp_path.exists(), "E_COLLECT_TEMP_EXISTS", str(temp_path))
    try:
        with temp_path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        document, _, _, _ = strict_canonical_document(temp_path.read_bytes(), str(temp_path))
        require(canonical_bytes(document) == raw, "E_COLLECT_CANONICAL")
        os.replace(temp_path, output)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(output.read_bytes() == raw, "E_COLLECT_WRITE")


def source_transaction_seal(expected_tip: str, *, include_output: bool) -> dict[str, Any]:
    selected = FINAL_PATHS if include_output else NONSELF_PATHS
    records = porcelain_records()
    return {
        "repository": repository_refs(expected_tip),
        "protected": protected_boundary(expected_tip),
        "selected_status": {path: records.get(path) for path in selected},
        "unexpected_paths": sorted(set(records) - set(FINAL_PATHS)),
        "selected_hashes": {path: sha256(read_worktree_lf(path)) for path in selected},
        "immutable_original_hashes": validate_original_immutable_worktree(),
    }


def validate_source_policy() -> int:
    raw = read_worktree_lf(VALIDATOR_PATH)
    tree = ast.parse(raw.decode("utf-8", errors="strict"), filename=VALIDATOR_PATH)
    imports = []
    import_nodes = [
        node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    for node in sorted(import_nodes, key=lambda item: (item.lineno, item.col_offset)):
        if isinstance(node, ast.Import):
            imports.append(("import", tuple((item.name, item.asname) for item in node.names)))
        elif isinstance(node, ast.ImportFrom):
            imports.append(("from", node.module, tuple((item.name, item.asname) for item in node.names)))
    expected = [
        ("from", "__future__", (("annotations", None),)),
        ("import", (("argparse", None),)),
        ("import", (("ast", None),)),
        ("import", (("copy", None),)),
        ("import", (("hashlib", None),)),
        ("import", (("json", None),)),
        ("import", (("math", None),)),
        ("import", (("os", None),)),
        ("import", (("pathlib", None),)),
        ("import", (("re", None),)),
        ("import", (("subprocess", None),)),
        ("from", "typing", (("Any", None), ("Callable", None))),
    ]
    require(imports == expected, "E_SOURCE_IMPORT_SEAL", repr(imports))
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    def owner(node: ast.AST) -> str:
        current: ast.AST | None = node
        while current is not None:
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return current.name
            current = parents.get(current)
        return "<module>"

    subprocess_sites = 0
    mutation_sites = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in {
            "eval", "exec", "compile", "__import__",
        }:
            require(False, "E_SOURCE_DYNAMIC_EXEC", node.func.id)
        if isinstance(node.func, ast.Attribute):
            receiver = node.func.value
            if isinstance(receiver, ast.Name) and receiver.id == "subprocess":
                require(node.func.attr == "run" and owner(node) == "run_git",
                        "E_SOURCE_PROCESS_SITE", f"{owner(node)}:{node.func.attr}")
                subprocess_sites += 1
            if isinstance(receiver, ast.Name) and receiver.id == "os" and node.func.attr in {
                "replace", "fsync", "remove", "rename", "unlink", "system",
            }:
                require(owner(node) == "atomic_collect" and node.func.attr in {"replace", "fsync"},
                        "E_SOURCE_OS_MUTATION", f"{owner(node)}:{node.func.attr}")
                mutation_sites += 1
            if node.func.attr in {
                "write_bytes", "write_text", "unlink", "rename", "touch", "mkdir", "rmdir",
            }:
                require(owner(node) == "atomic_collect" and node.func.attr == "unlink",
                        "E_SOURCE_PATH_MUTATION", f"{owner(node)}:{node.func.attr}")
                mutation_sites += 1
            if node.func.attr == "open":
                require(
                    owner(node) == "atomic_collect"
                    and len(node.args) == 1
                    and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == "xb",
                    "E_SOURCE_FILE_OPEN",
                    owner(node),
                )
            if node.func.attr in {"write", "flush", "fileno"}:
                require(owner(node) == "atomic_collect", "E_SOURCE_FILE_HANDLE", owner(node))
    require(subprocess_sites == 1, "E_SOURCE_SUBPROCESS_CARDINALITY", str(subprocess_sites))
    require(mutation_sites == 3, "E_SOURCE_MUTATION_CARDINALITY", str(mutation_sites))
    return 4


def validate_stored_reconstruction(
    source_commit: str | None = None,
    precommit_refs: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], bytes, int, int, int]:
    document, raw, nodes, scalars, depth = read_stored()
    first = build_payload(source_commit, precommit_refs)
    second = build_payload(source_commit, precommit_refs)
    first_raw = canonical_bytes(first)
    require(first_raw == canonical_bytes(second), "E_DETERMINISM")
    require(raw == first_raw, "E_STORED_RECONSTRUCTION")
    return document, raw, nodes, scalars, depth


def persistence_seal(expected_commit: str, document: dict[str, Any], stored_raw: bytes) -> dict[str, Any]:
    repository = repository_refs(expected_commit)
    require(not porcelain_records(), "E_PERSISTENCE_DIRTY")
    parents = git_text(["show", "-s", "--format=%P", expected_commit]).split()
    require(parents == [ACTIVATION_COMMIT], "E_PERSISTENCE_PARENT", repr(parents))
    subject = git_text(["show", "-s", "--format=%s", expected_commit])
    require(subject == REPAIR_SUBJECT, "E_PERSISTENCE_SUBJECT", subject)
    status = commit_status(expected_commit)
    require(status == FINAL_STATUS, "E_PERSISTENCE_PATHS", repr(status))
    entries = tree_entries(expected_commit, FINAL_PATHS)
    require(set(entries) == set(FINAL_PATHS), "E_PERSISTENCE_TREE_PATHS")
    require({path: entries[path]["mode"] for path in FINAL_PATHS}
            == {path: "100644" for path in FINAL_PATHS}, "E_PERSISTENCE_MODES")
    recorded = {
        row["path"]: row for row in document["repair_transaction"]["nonself_artifacts"]
    }
    committed_hashes = {}
    for path in NONSELF_PATHS:
        raw = lf_bytes(git_blob(expected_commit, path))
        require(sha256(raw) == recorded[path]["sha256_lf"], "E_PERSISTENCE_BLOB", path)
        require(len(raw) == recorded[path]["bytes_lf"], "E_PERSISTENCE_BLOB_BYTES", path)
        require(raw == read_worktree_lf(path), "E_PERSISTENCE_WORKTREE_BLOB", path)
        committed_hashes[path] = sha256(raw)
    committed_json = git_blob(expected_commit, OUTPUT_PATH)
    require(committed_json == stored_raw, "E_PERSISTENCE_JSON_BLOB")
    strict_document, _, _, _ = strict_canonical_document(committed_json, f"{expected_commit}:{OUTPUT_PATH}")
    require(strict_document == document, "E_PERSISTENCE_JSON_DOCUMENT")
    fresh = canonical_bytes(build_payload(
        expected_commit, document["repair_transaction"]["precommit_ref_boundary"],
    ))
    require(committed_json == fresh, "E_PERSISTENCE_JSON_RECONSTRUCTION")
    for path in IMMUTABLE_WORKTREE_PATHS:
        require(git_blob(expected_commit, path) == git_blob(ACTIVATION_COMMIT, path),
                "E_PERSISTENCE_ORIGINAL_IMMUTABLE", path)
    protected = protected_boundary(expected_commit)
    return {
        "repository": repository,
        "parents": parents,
        "subject": subject,
        "status": status,
        "entries": entries,
        "nonself_hashes": committed_hashes,
        "json_blob_oid": entries[OUTPUT_PATH]["blob_oid"],
        "protected": protected,
        "clean": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    modes = (args.collect, args.content_only, args.verify_staged, args.verify_persistence)
    require(sum(modes) == 1, "E_CLI_MODE")
    require(
        (args.verify_persistence and args.expected_commit is not None)
        or (not args.verify_persistence and args.expected_commit is None),
        "E_EXPECTED_COMMIT_MODE",
    )
    source_checks = validate_source_policy()
    expected_commit = validate_expected_commit(args.expected_commit) if args.verify_persistence else None

    if args.collect:
        require(not (ROOT / OUTPUT_PATH).exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
        entry = source_transaction_seal(ACTIVATION_COMMIT, include_output=False)
        validate_change_snapshot(include_output=False, staged=False)
        first = build_payload(precommit_refs=entry["repository"])
        second = build_payload(precommit_refs=entry["repository"])
        raw = canonical_bytes(first)
        require(raw == canonical_bytes(second), "E_DETERMINISM")
        assert_payload(first)
        atomic_collect(raw)
        validate_change_snapshot(include_output=True, staged=False)
        stored, stored_raw, nodes, scalars, depth = read_stored()
        require(stored_raw == raw and stored == first, "E_COLLECT_STORED")
        terminal = source_transaction_seal(ACTIVATION_COMMIT, include_output=False)
        require(entry == terminal, "E_TRANSACTION_TOCTOU")
        counts = stored["negative_contract"]["counts"]
        print(
            f"{CONTENT_GATE} collect=JSON_LAST source_policy={source_checks}/4 "
            f"negative={sum(counts.values())}/{sum(counts.values())} "
            f"json_nodes={nodes} scalars={scalars} depth={depth} determinism=2/2"
        )
        return 0

    if args.content_only:
        entry = source_transaction_seal(ACTIVATION_COMMIT, include_output=True)
        validate_change_snapshot(include_output=True, staged=False)
        document, _, nodes, scalars, depth = validate_stored_reconstruction(
            precommit_refs=entry["repository"],
        )
        terminal = source_transaction_seal(ACTIVATION_COMMIT, include_output=True)
        require(entry == terminal, "E_TRANSACTION_TOCTOU")
        counts = document["negative_contract"]["counts"]
        print(
            f"{CONTENT_GATE} content_only=true source_policy={source_checks}/4 "
            f"negative={sum(counts.values())}/{sum(counts.values())} "
            f"json_nodes={nodes} scalars={scalars} depth={depth} determinism=2/2"
        )
        return 0

    if args.verify_staged:
        entry = source_transaction_seal(ACTIVATION_COMMIT, include_output=True)
        staged_entry = validate_change_snapshot(include_output=True, staged=True)
        document, _, _, _, _ = validate_stored_reconstruction(
            precommit_refs=entry["repository"],
        )
        validate_staged_document_binding(staged_entry, document)
        staged_terminal = validate_change_snapshot(include_output=True, staged=True)
        validate_staged_document_binding(staged_terminal, document)
        require(staged_entry == staged_terminal, "E_STAGED_INDEX_TOCTOU")
        terminal = source_transaction_seal(ACTIVATION_COMMIT, include_output=True)
        require(entry == terminal, "E_STAGED_TRANSACTION_TOCTOU")
        counts = document["negative_contract"]["counts"]
        print(
            f"{CONTENT_GATE} staged=true exact-seven=7/7 modes=100644/7 "
            f"source_policy={source_checks}/4 negative={sum(counts.values())}/{sum(counts.values())}"
        )
        return 0

    require(expected_commit is not None, "E_EXPECTED_COMMIT")
    document, stored_raw, _, _, _ = read_stored()
    entry = persistence_seal(expected_commit, document, stored_raw)
    terminal = persistence_seal(expected_commit, document, stored_raw)
    require(entry == terminal, "E_PERSISTENCE_TOCTOU")
    print(
        f"{PERSISTENCE_TERMINAL} commit={expected_commit} exact-seven=7/7 "
        "same-child-dual-runtime-required=true clean=true pushed-live=true"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ValidationError, KeyError, IndexError, TypeError, ValueError, OSError,
        UnicodeError, subprocess.TimeoutExpired,
    ) as error:
        code = error.code if isinstance(error, ValidationError) else type(error).__name__
        print(f"FAIL_P067_ACTIVATION_REPAIR {code}: {error}")
        raise SystemExit(1)
