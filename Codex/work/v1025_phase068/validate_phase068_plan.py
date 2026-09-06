from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
from collections import Counter
from typing import Any, Callable


ROOT = pathlib.Path(__file__).resolve().parents[3]
PLAN_PATH = "Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md"
VALIDATOR_PATH = "Codex/work/v1025_phase068/validate_phase068_plan.py"
OUTPUT_PATH = "Codex/results/PHASE_068_PLAN_ACTIVATION_VALIDATION.json"
RESULT_PATH = "Codex/results/PHASE_068_PLAN_ACTIVATION_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
OUTPUT = ROOT / OUTPUT_PATH

EXPECTED_PARENT = "0371387f582fb63f5c3858d7e6905ed83eee885f"
EXPECTED_PARENT_PARENT = "ba29277a6d6b4469e8718e025bd1c676d8c7d65e"
EXPECTED_PARENT_SUBJECT = "audit(phase067): close code history gate"
EXPECTED_SUBJECT = "docs(phase068): plan claude codex fork adjudication"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
ACTIVE_REMOTE_REF = f"refs/remotes/origin/{ACTIVE_BRANCH}"
UPSTREAM = f"origin/{ACTIVE_BRANCH}"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
CLAUDE_BRANCH = "claude/version-1026-regsol-review-kl88j7"
CLAUDE_TIP = "e3e1a634f34b711aa4803fd190fe9120f1755f13"
CODEX_FORK_BRANCH = "codex/v1025_2-physics-conformance"
CODEX_FORK_TIP = "11f90544865dd179739ca5bc5062b28c1078e504"
CODEX_MERGE = "4316d8a5423d0ba229931a3c43c1f833fdc2fe1e"
CODEX_MERGE_PARENTS = ["eed5d4850215b22ea7775de3365cd3d3cbfc4414", BASELINE]
CLAUDE_UNIQUE_COMMITS = [
    "2802395dd03e6cabe3e981bddddbba139e3963bc", CLAUDE_TIP,
]
CODEX_UNIQUE_COMMITS = [
    "2abf019c7fee9bebd84b49cc9530f6983b08a8fa",
    "eed5d4850215b22ea7775de3365cd3d3cbfc4414",
    CODEX_MERGE,
    "30a874e906f2be72a36efaac7cb8fd8138e7b401",
    CODEX_FORK_TIP,
]

GATE = "PASS_P068_PLAN_ACTIVATION"
STAGED_GATE = "PASS_P068_PLAN_ACTIVATION_STAGED"
PERSISTENCE = "PASS_P068_PLAN_ACTIVATION_PERSISTENCE"
FINAL_GATE = "PASS_P068_FORK_ADJUDICATION"
PRECOMMIT_STATUS = "PASS_PENDING_PERSISTENCE"
PENDING_COMMIT = "PENDING_AT_PRECOMMIT_BY_DESIGN"
PREDECESSOR_TERMINAL = "PASS_P067_STEP90_2_PERSISTENCE"
SELF_TEST_COUNT = 29
CURRENT_STATE_MARKER = "P068_PLAN_ACTIVATION_PRECOMMIT"
CURRENT_STATE_LINE = f"Current-state marker: `{CURRENT_STATE_MARKER}`"
CURRENT_STATE_AUTHORITY = (
    "State-marker authority: this exact field is the machine-authoritative current unit; "
    "narrative references to earlier precommit states are historical."
)
VALIDATOR_IDENTITY_AUTHORITY = (
    "Validator-identity authority: the exact current-validator marker is the sole "
    "machine-authoritative current validator identity; other revisions are correction history."
)

FINAL_PATHS = [
    PLAN_PATH, VALIDATOR_PATH, OUTPUT_PATH, RESULT_PATH,
    PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH,
]
FINAL_STATUS = {
    PLAN_PATH: "A", VALIDATOR_PATH: "A", OUTPUT_PATH: "A", RESULT_PATH: "A",
    PARENT_LEDGER_PATH: "M", ACTIVE_LEDGER_PATH: "M", HANDOVER_PATH: "M",
}
NONSELF_PATHS = [path for path in FINAL_PATHS if path != OUTPUT_PATH]
NONSELF_STATUS = {path: FINAL_STATUS[path] for path in NONSELF_PATHS}
PREDECESSOR_PATHS = [
    "Codex/work/v1025_phase067/validate_phase067_final.py",
    "Codex/results/PHASE_067_VALIDATION.json",
    "Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md",
    "Codex/results/PHASE_067_STEP_090_2_GATE_RESULT.md",
    "Codex/results/PHASE_067_RESULT.md",
    PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH,
]
PREDECESSOR_STATUS = {
    path: "A" if index < 5 else "M" for index, path in enumerate(PREDECESSOR_PATHS)
}
EXPECTED_STEPS = [str(number) for number in range(91, 99)]
DISPOSITIONS = ["ADOPT", "REWRITE", "REFERENCE_ONLY", "REJECT", "UNVERIFIED"]
RECOVERY_PATHS = [PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH]
STEP_OUTPUTS = {
    "91": [
        "Codex/work/v1025_phase068/build_phase068_step91.py",
        "Codex/work/v1025_phase068/validate_phase068_step91.py",
        "Codex/results/PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json",
        "Codex/results/PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json",
        "Codex/results/PHASE_068_STEP_091_CLAUDE_FORK_REVIEW_RESULT.md", *RECOVERY_PATHS,
    ],
    "92": [
        "Codex/work/v1025_phase068/build_phase068_step92.py",
        "Codex/work/v1025_phase068/validate_phase068_step92.py",
        "Codex/results/PHASE_068_CODEX_FORK_DIFF_INVENTORY.json",
        "Codex/results/PHASE_068_CODEX_FORK_FULL_READ_ATTESTATION.json",
        "Codex/results/PHASE_068_STEP_092_CODEX_FORK_REVIEW_RESULT.md", *RECOVERY_PATHS,
    ],
    "93": [
        "Codex/work/v1025_phase068/build_phase068_step93.py",
        "Codex/work/v1025_phase068/validate_phase068_step93.py",
        "Codex/results/PHASE_068_PHASE044_054_REAUDIT_MATRIX.json",
        "Codex/results/PHASE_068_STEP_093_PHASE044_054_REAUDIT_RESULT.md", *RECOVERY_PATHS,
    ],
    "94": [
        "Codex/work/v1025_phase068/build_phase068_step94.py",
        "Codex/work/v1025_phase068/validate_phase068_step94.py",
        "Codex/results/PHASE_068_U13_REGSOL_REDERIVATION.json",
        "Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md", *RECOVERY_PATHS,
    ],
    "95": [
        "Codex/work/v1025_phase068/build_phase068_step95.py",
        "Codex/work/v1025_phase068/validate_phase068_step95.py",
        "Codex/results/PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json",
        "Codex/results/PHASE_068_STEP_095_CONFORMANCE_MODEL_ADJUDICATION_RESULT.md", *RECOVERY_PATHS,
    ],
    "96": [
        "Codex/work/v1025_phase068/build_phase068_step96.py",
        "Codex/work/v1025_phase068/validate_phase068_step96.py",
        "Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json",
        "Codex/results/PHASE_068_STEP_096_FORK_CONFLICT_ADJUDICATION_RESULT.md", *RECOVERY_PATHS,
    ],
    "97": [
        "Codex/work/v1025_phase068/build_phase068_step97.py",
        "Codex/work/v1025_phase068/validate_phase068_step97.py",
        "Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json",
        "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json",
        "Codex/results/PHASE_068_STEP_097_FORK_DISPOSITION_RESULT.md", *RECOVERY_PATHS,
    ],
    "98": [
        "Codex/work/v1025_phase068/validate_phase068_final.py",
        "Codex/results/PHASE_068_VALIDATION.json",
        "Codex/results/PHASE_068_FORK_ADJUDICATION_REPORT.md",
        "Codex/results/PHASE_068_STEP_098_GATE_RESULT.md",
        "Codex/results/PHASE_068_RESULT.md", *RECOVERY_PATHS,
    ],
}
STEP_SUBJECTS = {
    "91": "audit(phase068): read claude fork history",
    "92": "audit(phase068): read codex fork history",
    "93": "audit(phase068): revalidate phase044 phase054 reviews",
    "94": "audit(phase068): rederive u13 threshold regularity",
    "95": "audit(phase068): adjudicate conformance model",
    "96": "audit(phase068): adjudicate fork claim conflicts",
    "97": "audit(phase068): classify fork evidence",
    "98": "audit(phase068): close fork adjudication gate",
}
STEP_CONTENT_TERMINALS = {
    "91": "`PASS_P068_STEP91_CLAUDE_FORK_READ`",
    "92": "`PASS_P068_STEP92_CODEX_FORK_READ`",
    "93": "`PASS_P068_STEP93_PRIOR_REVIEW_REAUDIT`",
    "94": "`PASS_P068_STEP94_U13_REDERIVATION`",
    "95": "`PASS_P068_STEP95_CONFORMANCE_MODEL`",
    "96": "`PASS_P068_STEP96_CONFLICT_ADJUDICATION`",
    "97": "`PASS_P068_STEP97_DISPOSITION`",
    "98": "selected `PASS_P068_FORK_ADJUDICATION` or `NOT_ACHIEVED`",
}
REQUIRED_HEADINGS = [
    "## Summary", "## Current Ground Truth", "## Phase Range",
    "## Exact Read Inputs", "## Non-goals and Scope Guards",
    "## Implementation Changes", "## Plan Activation Unit — Save Before Step 91",
    "## Phase 068", "## Phase Gate", "## Canonical-Evidence Reuse Protocol",
    "## Implementation Interfaces", "## Test and Validation Plan",
    "## Stop Conditions", "## Assumptions", "## Correction History",
]

MAX_JSON_BYTES = 8 * 1024 * 1024
MAX_JSON_DEPTH = 20
MAX_JSON_NODES = 1_000_000
MAX_JSON_STRING_BYTES = 2 * 1024 * 1024
READABLE_GIT_PATHS = set(FINAL_PATHS) | set(PREDECESSOR_PATHS)
FIXED_OIDS = {
    EXPECTED_PARENT, EXPECTED_PARENT_PARENT, PROTECTED_TIP, MAIN_TIP, BASELINE,
    CLAUDE_TIP, CODEX_FORK_TIP, CODEX_MERGE, *CLAUDE_UNIQUE_COMMITS,
    *CODEX_UNIQUE_COMMITS, *CODEX_MERGE_PARENTS,
}
LIVE_BRANCHES = {
    ACTIVE_BRANCH, PROTECTED_BRANCH, "main", CLAUDE_BRANCH, CODEX_FORK_BRANCH,
}
TRACKING_REFS = {
    ACTIVE_REMOTE_REF, f"refs/remotes/origin/{PROTECTED_BRANCH}",
    "refs/remotes/origin/main", f"refs/remotes/origin/{CLAUDE_BRANCH}",
    f"refs/remotes/origin/{CODEX_FORK_BRANCH}",
}
LOCAL_REFS = {f"refs/heads/{PROTECTED_BRANCH}", "refs/heads/main"}


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
    return len(raw.splitlines())


def canonical_bytes(document: dict[str, Any]) -> bytes:
    text = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("utf-8")


def semantic_hash(document: dict[str, Any]) -> str:
    candidate = copy.deepcopy(document)
    candidate.pop("semantic_sha256", None)
    return sha256(canonical_bytes(candidate))


def reject_constant(value: str) -> None:
    raise ValidationError("E_JSON_NONFINITE", value)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE_KEY", key)
        result[key] = value
    return result


def inspect_json(value: Any, depth: int = 0) -> tuple[int, int]:
    require(depth <= MAX_JSON_DEPTH, "E_JSON_DEPTH", str(depth))
    if type(value) is dict:
        nodes, maximum = 1, depth
        for key, child in value.items():
            require(type(key) is str, "E_JSON_KEY_TYPE")
            require(len(key.encode()) <= MAX_JSON_STRING_BYTES, "E_JSON_STRING_SIZE")
            child_nodes, child_depth = inspect_json(child, depth + 1)
            nodes += child_nodes + 1
            maximum = max(maximum, child_depth)
            require(nodes <= MAX_JSON_NODES, "E_JSON_NODES", str(nodes))
        return nodes, maximum
    if type(value) is list:
        nodes, maximum = 1, depth
        for child in value:
            child_nodes, child_depth = inspect_json(child, depth + 1)
            nodes += child_nodes
            maximum = max(maximum, child_depth)
            require(nodes <= MAX_JSON_NODES, "E_JSON_NODES", str(nodes))
        return nodes, maximum
    require(value is None or type(value) in {str, int, float, bool}, "E_JSON_TYPE")
    if type(value) is str:
        require(len(value.encode()) <= MAX_JSON_STRING_BYTES, "E_JSON_STRING_SIZE")
    if type(value) is float:
        require(math.isfinite(value), "E_JSON_NONFINITE")
    return 1, depth


def strict_load(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    require(len(raw) <= MAX_JSON_BYTES, "E_JSON_SIZE", f"{label}:{len(raw)}")
    require(not raw.startswith(b"\xef\xbb\xbf"), "E_JSON_BOM", label)
    try:
        text = raw.decode("utf-8", errors="strict")
        document = json.loads(text, object_pairs_hook=reject_pairs, parse_constant=reject_constant)
    except UnicodeDecodeError as error:
        raise ValidationError("E_JSON_UTF8", label) from error
    except json.JSONDecodeError as error:
        raise ValidationError("E_JSON_SYNTAX", f"{label}:{error.msg}") from error
    except RecursionError as error:
        raise ValidationError("E_JSON_RECURSION", label) from error
    require(type(document) is dict, "E_JSON_ROOT", label)
    try:
        nodes, depth = inspect_json(document)
    except RecursionError as error:
        raise ValidationError("E_JSON_RECURSION", label) from error
    return document, nodes, depth


def read_lf(path: str) -> bytes:
    full = ROOT / path
    require(full.is_file() and not full.is_symlink(), "E_INPUT_MISSING_OR_NONREGULAR", path)
    return lf_bytes(full.read_bytes())


def read_text(path: str) -> str:
    try:
        return read_lf(path).decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValidationError("E_INPUT_UTF8", path) from error


def is_oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def validate_git_argv(args: list[str]) -> None:
    require(args and all(type(x) is str and not any(c in x for c in "\0\r\n") for x in args),
            "E_GIT_ARGV", repr(args))
    command = args[0]
    if command == "branch":
        valid = args == ["branch", "--show-current"]
    elif command == "remote":
        valid = args == ["remote", "get-url", "origin"]
    elif command == "rev-parse":
        valid = (len(args) == 2 and (args[1] in {"HEAD", "@{upstream}", *TRACKING_REFS,
                                                 *LOCAL_REFS, *FIXED_OIDS} or is_oid(args[1])))
        valid = valid or args == ["rev-parse", "--abbrev-ref", "@{upstream}"]
    elif command == "show-ref":
        valid = len(args) == 4 and args[:3] == ["show-ref", "--verify", "--quiet"] \
            and args[3] in LOCAL_REFS
    elif command == "ls-remote":
        valid = len(args) == 3 and args[1] == "origin" \
            and args[2].startswith("refs/heads/") and args[2][11:] in LIVE_BRANCHES
    elif command == "cat-file":
        target = args[2] if len(args) == 3 else ""
        oid = target.removesuffix("^{commit}")
        valid = len(args) == 3 and args[1] == "-e" and target == f"{oid}^{{commit}}" \
            and is_oid(oid) and oid in FIXED_OIDS
    elif command == "show":
        metadata = len(args) == 4 and args[1] == "-s" \
            and args[2] in {"--format=%P", "--format=%s"} and is_oid(args[3])
        blob = False
        if len(args) == 2 and ":" in args[1]:
            revision, path = args[1].split(":", 1)
            blob = (revision == "" or is_oid(revision)) and path in READABLE_GIT_PATHS
        valid = metadata or blob
    elif command == "diff-tree":
        valid = len(args) == 7 and args[1:6] == [
            "--no-commit-id", "--no-renames", "--name-status", "-z", "-r",
        ] and is_oid(args[6])
    elif command == "diff":
        status = len(args) == 7 and args[1:4] == ["--no-renames", "--name-status", "-z"] \
            and is_oid(args[4]) and is_oid(args[5]) and args[6] == "--"
        quiet = len(args) == 6 and args[1] == "--quiet" and is_oid(args[2]) \
            and is_oid(args[3]) and args[4:] == ["--", "Claude"]
        simple = tuple(args) in {
            ("diff", "--check"), ("diff", "--cached", "--check"),
            ("diff", "--no-renames", "--name-status", "-z"),
            ("diff", "--cached", "--no-renames", "--name-status", "-z"),
        }
        valid = status or quiet or simple
    elif command == "ls-files":
        others = args == ["ls-files", "--others", "--exclude-standard", "-z"]
        staged = len(args) >= 5 and args[1:4] == ["--stage", "-z", "--"] \
            and set(args[4:]) <= set(FINAL_PATHS) and len(args[4:]) == len(set(args[4:]))
        valid = others or staged
    elif command == "ls-tree":
        valid = len(args) >= 5 and args[1] == "-z" and is_oid(args[2]) and args[3] == "--" \
            and set(args[4:]) <= READABLE_GIT_PATHS and len(args[4:]) == len(set(args[4:]))
    elif command == "merge-base":
        valid = args == ["merge-base", CLAUDE_TIP, CODEX_FORK_TIP]
    elif command == "rev-list":
        valid = args in [
            ["rev-list", "--reverse", "--topo-order", f"{BASELINE}..{CLAUDE_TIP}"],
            ["rev-list", "--reverse", "--topo-order", f"{BASELINE}..{CODEX_FORK_TIP}"],
        ]
    else:
        raise ValidationError("E_GIT_SUBCOMMAND", repr(args))
    require(valid, "E_GIT_ARGV_SHAPE", repr(args))


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    validate_git_argv(args)
    process = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, timeout=300, check=False, shell=False,
    )
    if check and process.returncode != 0:
        detail = process.stderr.decode("utf-8", errors="replace")[-800:]
        raise ValidationError("E_GIT_PROCESS", f"{args!r}:{detail}")
    return process


def git_text(args: list[str]) -> str:
    return run_git(args).stdout.decode("utf-8", errors="strict").strip()


def git_blob(commit: str, path: str) -> bytes:
    return run_git(["show", f"{commit}:{path}"]).stdout


def index_blob(path: str) -> bytes:
    return run_git(["show", f":{path}"]).stdout


def live_tip(
    branch: str,
    runner: Callable[[list[str]], subprocess.CompletedProcess[bytes]] | None = None,
) -> str:
    execute = run_git if runner is None else runner
    preflight = ["remote", "get-url", "origin"]
    validate_git_argv(preflight)
    origin_process = execute(preflight)
    require(origin_process.returncode == 0, "E_ORIGIN_PREFLIGHT_PROCESS")
    origin_url = origin_process.stdout.decode("utf-8", errors="strict").strip()
    require(origin_url == ORIGIN_URL, "E_ORIGIN_URL", origin_url)

    ref = f"refs/heads/{branch}"
    query = ["ls-remote", "origin", ref]
    validate_git_argv(query)
    live_process = execute(query)
    require(live_process.returncode == 0, "E_LIVE_PROCESS", branch)
    lines = live_process.stdout.decode("utf-8", errors="strict").strip().splitlines()
    require(len(lines) == 1, "E_LIVE_CARDINALITY", repr(lines))
    fields = lines[0].split("\t")
    require(len(fields) == 2 and is_oid(fields[0]) and fields[1] == ref,
            "E_LIVE_PARSE", lines[0])
    return fields[0]


def require_fixed_commit(
    oid: str,
    runner: Callable[[list[str]], subprocess.CompletedProcess[bytes]] | None = None,
) -> None:
    require(oid in FIXED_OIDS and is_oid(oid), "E_FIXED_COMMIT_ALLOWLIST", oid)
    argv = ["cat-file", "-e", f"{oid}^{{commit}}"]
    validate_git_argv(argv)
    process = run_git(argv, check=False) if runner is None else runner(argv)
    require(process.returncode == 0, "E_FIXED_COMMIT_OBJECT", oid)


def parse_status(raw: bytes) -> dict[str, str]:
    fields = raw.decode("utf-8", errors="strict").split("\0")
    if fields and fields[-1] == "":
        fields.pop()
    require(len(fields) % 2 == 0, "E_STATUS_PARSE")
    result: dict[str, str] = {}
    for index in range(0, len(fields), 2):
        status, path = fields[index:index + 2]
        require(status in {"A", "M", "D"}, "E_STATUS_RENAME_OR_TYPE", status)
        require(path not in result, "E_STATUS_DUPLICATE", path)
        result[path] = status
    return result


def staged_status() -> dict[str, str]:
    return parse_status(run_git(["diff", "--cached", "--no-renames", "--name-status", "-z"]).stdout)


def unstaged_status() -> dict[str, str]:
    return parse_status(run_git(["diff", "--no-renames", "--name-status", "-z"]).stdout)


def untracked_paths() -> list[str]:
    raw = run_git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout
    return sorted(x for x in raw.decode("utf-8", errors="strict").split("\0") if x)


def worktree_status() -> dict[str, str]:
    result = unstaged_status()
    for path in untracked_paths():
        require(path not in result, "E_WORKTREE_COLLISION", path)
        result[path] = "A"
    return result


def tree_entries(commit: str, paths: list[str]) -> dict[str, dict[str, str]]:
    raw = run_git(["ls-tree", "-z", commit, "--", *paths]).stdout
    result: dict[str, dict[str, str]] = {}
    for field in raw.decode("utf-8", errors="strict").split("\0"):
        if field:
            metadata, path = field.split("\t", 1)
            mode, kind, oid = metadata.split(" ", 2)
            require(kind == "blob" and path not in result, "E_TREE_ENTRY", path)
            result[path] = {"mode": mode, "blob_oid": oid}
    return result


def index_entries(paths: list[str]) -> dict[str, dict[str, str]]:
    raw = run_git(["ls-files", "--stage", "-z", "--", *paths]).stdout
    result: dict[str, dict[str, str]] = {}
    for field in raw.decode("utf-8", errors="strict").split("\0"):
        if field:
            metadata, path = field.split("\t", 1)
            mode, oid, stage = metadata.split(" ", 2)
            require(stage == "0" and path not in result, "E_INDEX_ENTRY", path)
            result[path] = {"mode": mode, "blob_oid": oid}
    return result


def counts(status: dict[str, str]) -> dict[str, int]:
    found = Counter(status.values())
    return {key: found.get(key, 0) for key in ("A", "M", "D")}


def path_hash(status: dict[str, str]) -> str:
    return sha256("\n".join(f"{status[p]}\t{p}" for p in sorted(status)).encode())


def optional_local_ref(ref: str) -> str | None:
    result = run_git(["show-ref", "--verify", "--quiet", ref], check=False)
    require(result.returncode in {0, 1}, "E_LOCAL_REF_QUERY", ref)
    return git_text(["rev-parse", ref]) if result.returncode == 0 else None


def fixed_boundaries() -> dict[str, Any]:
    require(git_text(["remote", "get-url", "origin"]) == ORIGIN_URL, "E_ORIGIN_URL")
    for oid in sorted(FIXED_OIDS):
        require_fixed_commit(oid)
        require(git_text(["rev-parse", oid]) == oid, "E_FIXED_OBJECT", oid)
    expected = {
        "protected": PROTECTED_TIP, "main": MAIN_TIP,
        "claude": CLAUDE_TIP, "codex_fork": CODEX_FORK_TIP,
    }
    tracking = {
        "protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"]),
        "main": git_text(["rev-parse", "refs/remotes/origin/main"]),
        "claude": git_text(["rev-parse", f"refs/remotes/origin/{CLAUDE_BRANCH}"]),
        "codex_fork": git_text(["rev-parse", f"refs/remotes/origin/{CODEX_FORK_BRANCH}"]),
    }
    require(tracking == expected, "E_FIXED_TRACKING", repr(tracking))
    live = {
        "protected": live_tip(PROTECTED_BRANCH), "main": live_tip("main"),
        "claude": live_tip(CLAUDE_BRANCH), "codex_fork": live_tip(CODEX_FORK_BRANCH),
    }
    require(live == expected, "E_FIXED_LIVE", repr(live))
    protected_local = optional_local_ref(f"refs/heads/{PROTECTED_BRANCH}")
    main_local = optional_local_ref("refs/heads/main")
    require(protected_local == PROTECTED_TIP, "E_PROTECTED_LOCAL")
    require(main_local in {None, MAIN_TIP}, "E_MAIN_LOCAL")
    require(git_text(["merge-base", CLAUDE_TIP, CODEX_FORK_TIP]) == BASELINE,
            "E_FORK_MERGE_BASE")
    return {
        "origin_url": ORIGIN_URL, "expected": expected, "tracking": tracking, "live": live,
        "protected_local": protected_local, "main_local": main_local, "baseline": BASELINE,
    }


def fixed_predecessor() -> dict[str, Any]:
    """Commit-addressed certificate: intentionally does not inspect current HEAD."""
    require_fixed_commit(EXPECTED_PARENT)
    parents = git_text(["show", "-s", "--format=%P", EXPECTED_PARENT]).split()
    subject = git_text(["show", "-s", "--format=%s", EXPECTED_PARENT])
    require(parents == [EXPECTED_PARENT_PARENT], "E_PREDECESSOR_PARENT", repr(parents))
    require(subject == EXPECTED_PARENT_SUBJECT, "E_PREDECESSOR_SUBJECT")
    status = parse_status(run_git([
        "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-z", "-r",
        EXPECTED_PARENT,
    ]).stdout)
    require(status == PREDECESSOR_STATUS, "E_PREDECESSOR_PATHS", repr(status))
    entries = tree_entries(EXPECTED_PARENT, PREDECESSOR_PATHS)
    require(set(entries) == set(PREDECESSOR_PATHS), "E_PREDECESSOR_TREE")
    require(all(row["mode"] == "100644" for row in entries.values()), "E_PREDECESSOR_MODES")
    identities = []
    for path in PREDECESSOR_PATHS:
        raw = git_blob(EXPECTED_PARENT, path)
        identities.append({
            "path": path, "status": PREDECESSOR_STATUS[path], "mode": entries[path]["mode"],
            "blob_oid": entries[path]["blob_oid"], "raw_bytes": len(raw), "raw_sha256": sha256(raw),
        })
    raw_json = git_blob(EXPECTED_PARENT, "Codex/results/PHASE_067_VALIDATION.json")
    document, _, _ = strict_load(raw_json, "phase067-final@predecessor")
    require(document.get("schema_version") == "phase067-final-conformance-v1",
            "E_PREDECESSOR_SCHEMA")
    require(document.get("persistence_terminal") == PREDECESSOR_TERMINAL,
            "E_PREDECESSOR_TERMINAL")
    require(b"CONDITIONAL_P067" in raw_json, "E_PREDECESSOR_GATE")
    return {
        "commit": EXPECTED_PARENT, "parents": parents, "subject": subject,
        "head_independent": True, "path_identities": identities,
        "phase067_schema": document["schema_version"],
        "phase067_terminal": document["persistence_terminal"],
    }


def edge_record(parent: str, child: str) -> dict[str, Any]:
    status = parse_status(run_git([
        "diff", "--no-renames", "--name-status", "-z", parent, child, "--",
    ]).stdout)
    return {
        "parent": parent, "child": child, "changed_paths": len(status),
        "status_counts": counts(status), "path_list_sha256": path_hash(status),
    }


def fork_topology() -> dict[str, Any]:
    for oid in sorted({BASELINE, CLAUDE_TIP, CODEX_FORK_TIP, CODEX_MERGE,
                       *CLAUDE_UNIQUE_COMMITS, *CODEX_UNIQUE_COMMITS}):
        require_fixed_commit(oid)
    claude = git_text([
        "rev-list", "--reverse", "--topo-order", f"{BASELINE}..{CLAUDE_TIP}",
    ]).splitlines()
    codex = git_text([
        "rev-list", "--reverse", "--topo-order", f"{BASELINE}..{CODEX_FORK_TIP}",
    ]).splitlines()
    require(claude == CLAUDE_UNIQUE_COMMITS, "E_CLAUDE_UNIQUE", repr(claude))
    require(codex == CODEX_UNIQUE_COMMITS, "E_CODEX_UNIQUE", repr(codex))
    claude_net = parse_status(run_git([
        "diff", "--no-renames", "--name-status", "-z", BASELINE, CLAUDE_TIP, "--",
    ]).stdout)
    codex_net = parse_status(run_git([
        "diff", "--no-renames", "--name-status", "-z", BASELINE, CODEX_FORK_TIP, "--",
    ]).stdout)
    require(len(claude_net) == 3 and set(claude_net.values()) == {"M"}
            and all(path.startswith("Claude/") for path in claude_net), "E_CLAUDE_NET")
    require(len(codex_net) == 69 and set(codex_net.values()) == {"A"}, "E_CODEX_NET")
    require(sum(path.startswith("Codex/") for path in codex_net) == 68, "E_CODEX_NET_SCOPE")
    require({p for p in codex_net if not p.startswith("Codex/")} == {
        "output/pdf/Anode_Physics_v1.0.25.3_conformance.pdf",
    }, "E_CODEX_NET_OUTPUT")
    claude_edges, codex_edges = [], []
    for commit in claude:
        parents = git_text(["show", "-s", "--format=%P", commit]).split()
        require(len(parents) == 1, "E_CLAUDE_PARENT_COUNT", commit)
        claude_edges.append(edge_record(parents[0], commit))
    for commit in codex:
        parents = git_text(["show", "-s", "--format=%P", commit]).split()
        require(len(parents) in {1, 2}, "E_CODEX_PARENT_COUNT", commit)
        codex_edges.extend(edge_record(parent, commit) for parent in parents)
    merge_parents = git_text(["show", "-s", "--format=%P", CODEX_MERGE]).split()
    require(merge_parents == CODEX_MERGE_PARENTS, "E_CODEX_MERGE_PARENTS")
    merge_edges = [row for row in codex_edges if row["child"] == CODEX_MERGE]
    require([row["changed_paths"] for row in merge_edges] == [6, 59], "E_MERGE_EDGE_PATHS")
    require(len(claude_edges) == 2 and len(codex_edges) == 6, "E_PARENT_EDGE_COUNTS")
    return {
        "merge_base": BASELINE,
        "claude": {"tip": CLAUDE_TIP, "unique_count": 2, "commits": claude,
                   "parent_edge_count": 2, "edges": claude_edges,
                   "net_path_count": 3, "net_status": counts(claude_net),
                   "net_path_list_sha256": path_hash(claude_net)},
        "codex": {"tip": CODEX_FORK_TIP, "unique_count": 5, "commits": codex,
                  "parent_edge_count": 6, "edges": codex_edges, "merge_commit": CODEX_MERGE,
                  "merge_parents": merge_parents, "merge_parent_path_counts": [6, 59],
                  "net_path_count": 69, "net_status": counts(codex_net),
                  "net_path_list_sha256": path_hash(codex_net)},
    }


def require_tokens(text: str, tokens: list[str], code: str) -> None:
    missing = [token for token in tokens if token not in text]
    require(not missing, code, repr(missing))


def require_tokens_casefold(text: str, tokens: list[str], code: str) -> None:
    folded = text.casefold()
    missing = [token for token in tokens if token.casefold() not in folded]
    require(not missing, code, repr(missing))


def bounded_section(text: str, start: str, end: str, code: str) -> str:
    require(text.count(start) == 1 and text.count(end) == 1, code, "boundary")
    left, right = text.index(start), text.index(end)
    require(left < right, code, "order")
    return text[left:right]


def validate_plan(text: str) -> dict[str, Any]:
    positions = []
    for heading in REQUIRED_HEADINGS:
        pattern = r"^## Phase 068\b.*$" if heading == "## Phase 068" else rf"^{re.escape(heading)}$"
        matches = list(re.finditer(pattern, text, re.MULTILINE))
        require(len(matches) == 1, "E_PLAN_HEADING", heading)
        positions.append(matches[0].start())
    require(positions == sorted(positions), "E_PLAN_HEADING_ORDER")
    matches = list(re.finditer(r"^### Step (\d+(?:\.\d+)?)\b.*$", text, re.MULTILINE))
    steps = [match.group(1) for match in matches]
    require(steps == EXPECTED_STEPS, "E_PLAN_STEPS", repr(steps))
    require(re.search(r"\bStep\s+99(?:\b|\.)", text) is None, "E_PLAN_STEP99")

    safety = bounded_section(text, "### Builder and validator safety", "### Common Git closeout",
                             "E_PLAN_NETWORK_GUARD")
    safety_normalized = " ".join(safety.split())
    exact_network_guard = (
        "No arbitrary network, package installation, dynamic import, dunder lookup, `eval`, `exec`, "
        "source checkout, source mutation or Git mutation is allowed in builders/validators. The sole "
        "network exception is the fixed-argv, read-only `git ls-remote origin <exact-ref>` query "
        "required to authenticate live refs."
    )
    require(exact_network_guard in safety_normalized, "E_PLAN_NETWORK_GUARD")
    require(
        "Read Git through fixed argv arrays with an explicit command allowlist; never invoke a shell string."
        in safety_normalized,
        "E_PLAN_GIT_SAFETY",
    )
    denied_network_phrases = [
        "unrestricted network", "arbitrary network is allowed", "network access is allowed",
        "additional network exception", "any remote ref",
    ]
    require(not any(token in safety.casefold() for token in denied_network_phrases),
            "E_PLAN_NETWORK_GUARD")
    require(safety.count("`git ls-remote origin <exact-ref>`") == 1,
            "E_PLAN_NETWORK_EXCEPTION_CARDINALITY")

    common = bounded_section(text, "### Common Git closeout",
                             "## Plan Activation Unit — Save Before Step 91",
                             "E_PLAN_ACTIVATION_MODES")
    common_normalized = " ".join(common.split())
    require("For every unit," in common_normalized and "ordered allowlist" in common_normalized
            and "all tracked files must be mode `100644`" in common_normalized,
            "E_PLAN_ACTIVATION_MODES")
    activation = bounded_section(text, "## Plan Activation Unit — Save Before Step 91",
                                 "## Phase 068", "E_PLAN_ACTIVATION_SECTION")
    activation_paths = re.findall(r"^\d+\. `([^`]+)`$", activation, re.MULTILINE)
    require(activation_paths == FINAL_PATHS, "E_PLAN_ACTIVATION_PATHS", repr(activation_paths))
    require(activation.count("Required precommit status map in this exact order: `A/A/A/A/M/M/M`.") == 1,
            "E_PLAN_ACTIVATION_STATUS")
    require("exact-seven status/modes" in activation and "result-first and JSON-last" in activation,
            "E_PLAN_ACTIVATION_MODE_LINK")
    require(re.findall(r"^Commit subject:.*$", activation, re.MULTILINE)
            == [f"Commit subject: `{EXPECTED_SUBJECT}`"], "E_PLAN_ACTIVATION_SUBJECT")
    require(re.findall(r"^Content terminal:.*$", activation, re.MULTILINE)
            == [f"Content terminal: `{GATE}`"], "E_PLAN_ACTIVATION_CONTENT_TERMINAL")
    require(re.findall(r"^Required terminal:.*$", activation, re.MULTILINE)
            == [f"Required terminal: `{PERSISTENCE}`"], "E_PLAN_ACTIVATION_TERMINAL")

    required = [
        EXPECTED_PARENT, PROTECTED_TIP, MAIN_TIP, BASELINE, CLAUDE_TIP, CODEX_FORK_TIP,
        CODEX_MERGE, EXPECTED_SUBJECT, GATE, PERSISTENCE, FINAL_GATE, PRECOMMIT_STATUS,
        PENDING_COMMIT, PREDECESSOR_TERMINAL, "A/A/A/A/M/M/M", "100644",
        "result-first", "JSON-last", "fixed predecessor certificate",
        "current precommit transaction", "persistence child transaction",
        "Claude unique commits: `2`", "Codex unique commits: `5`",
        "Claude net paths: `3`", "Codex net paths: `69`", "Codex parent edges: `6`",
        "whole-commit cherry-pick", "file/issue-specific", "not canonical",
        "main scholarly body", "commit-addressed", "merge parent", "Phase 044", "Phase 054",
        "U13", "regular-solution", "conformance_model", "original source", "equation",
        "runtime", "NOT_ACHIEVED", *DISPOSITIONS, *FINAL_PATHS,
    ]
    require_tokens(text, required, "E_PLAN_TOKEN")
    require("CONDITIONAL_P068" not in text and "FAIL_P068" not in text,
            "E_PLAN_UNDEFINED_GATE")
    require(text.count(f"### `{FINAL_GATE}`") == 1, "E_PLAN_POSITIVE_GATE")
    gate_start = text.index("## Phase Gate")
    records = []
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else gate_start
        section, step = text[match.start():end], match.group(1)
        sections[step] = section
        word = "eight" if len(STEP_OUTPUTS[step]) == 8 else "seven"
        require(re.findall(r"^\*\*Exact-[^\n]+ outputs:\*\*$", section, re.MULTILINE)
                == [f"**Exact-{word} outputs:**"], "E_STEP_OUTPUT_LABEL", step)
        terminal = f"PASS_P068_STEP{step}_PERSISTENCE"
        paths = re.findall(r"^\d+\. `([^`]+)`$", section, re.MULTILINE)
        require(paths == STEP_OUTPUTS[step], "E_STEP_OUTPUT_PATHS", f"{step}:{paths!r}")
        status = "/".join("M" if path in RECOVERY_PATHS else "A" for path in paths)
        require(section.count(f"Required status: `{status}`.") == 1,
                "E_STEP_STATUS", step)
        require(re.findall(r"^Commit subject:.*$", section, re.MULTILINE)
                == [f"Commit subject: `{STEP_SUBJECTS[step]}`"],
                "E_STEP_SUBJECT_EXACT", step)
        require(re.findall(r"^Content terminal:.*$", section, re.MULTILINE)
                == [f"Content terminal: {STEP_CONTENT_TERMINALS[step]}"],
                "E_STEP_CONTENT_TERMINAL", step)
        require(re.findall(r"^Required terminal:.*$", section, re.MULTILINE)
                == [f"Required terminal: `{terminal}`"], "E_STEP_TERMINAL_EXACT", step)
        records.append({"step": step, "outputs": paths, "status": status,
                        "subject": STEP_SUBJECTS[step], "terminal": terminal})
    require_tokens_casefold(sections["91"], ["Claude", "two fixed commits", "net modified paths"],
                            "E_STEP91_SCOPE")
    require_tokens_casefold(sections["92"], ["Codex", "five-commit", "six parent edges"],
                            "E_STEP92_SCOPE")
    require_tokens(sections["93"], ["Phase 044", "Phase 054"], "E_STEP93_SCOPE")
    require_tokens_casefold(sections["94"], ["U13", "regular-solution"], "E_STEP94_SCOPE")
    require_tokens(sections["95"], ["conformance_model", "authority", "duplication"],
                   "E_STEP95_SCOPE")
    require_tokens_casefold(sections["96"], ["source", "equation", "runtime"], "E_STEP96_SCOPE")
    require_tokens(sections["97"], DISPOSITIONS, "E_STEP97_SCOPE")
    require_tokens(sections["98"], ["whole-commit cherry-pick", "file/issue-specific"],
                   "E_STEP98_SCOPE")
    return {"heading_count": len(positions), "steps": steps, "step_contracts": records,
            "positive_gate_only": True, "first_step_blocked_by": PERSISTENCE}


def plan_mutation_self_tests(text: str) -> int:
    network_mutation = text.replace("No arbitrary network", "Unrestricted network is allowed", 1)
    path_mutation = text.replace(f"5. `{PARENT_LEDGER_PATH}`", "5. `WRONG.md`", 1)
    subject_line = f"Commit subject: `{STEP_SUBJECTS['91']}`"
    subject_mutation = text.replace(subject_line, "Commit subject: `audit(phase068): wrong`", 1)
    require(network_mutation != text and path_mutation != text and subject_mutation != text,
            "E_PLAN_MUTATION_SETUP")
    expect_code("E_PLAN_NETWORK_GUARD", lambda: validate_plan(network_mutation))
    expect_code("E_PLAN_ACTIVATION_PATHS", lambda: validate_plan(path_mutation))
    expect_code("E_STEP_SUBJECT_EXACT", lambda: validate_plan(subject_mutation))
    return 3


def require_control_current_state(path: str, text: str) -> None:
    normalized = " ".join(text.replace("`", "").split())
    state_lines = re.findall(r"^Current-state marker:.*$", text, re.MULTILINE)
    authority_lines = re.findall(r"^State-marker authority:.*$", text, re.MULTILINE)
    require(state_lines == [CURRENT_STATE_LINE], "E_CONTROL_CURRENT_STATE",
            f"{path}:{state_lines!r}")
    require(authority_lines == [CURRENT_STATE_AUTHORITY], "E_CONTROL_STATE_AUTHORITY",
            f"{path}:{authority_lines!r}")
    require(text.count(CURRENT_STATE_MARKER) == 1,
            "E_CONTROL_STATE_MARKER_CARDINALITY", path)
    stale_patterns = [
        r"\bStep 90\.2\s+(?:(?:is|remains)\s+)?(?:still\s+)?current\b",
        r"\bStep 90\.2\s+continues?\s+to\s+be\s+current\b",
        r"PASS_P067_STEP90_2_PERSISTENCE\s+(?:(?:is|remains)\s+)?(?:still\s+)?pending\b",
    ]
    require(not any(re.search(pattern, normalized, re.IGNORECASE)
                    for pattern in stale_patterns),
            "E_CONTROL_STALE_CURRENT_STATE", path)
    require(re.search(r"\bPhase 068 plan activation is (?:now )?current\b",
                      normalized, re.IGNORECASE) is None,
            "E_CONTROL_AMBIGUOUS_CURRENT_PROSE", path)
    if path == RESULT_PATH:
        require("Status: PASS_PENDING_PERSISTENCE" in normalized
                and "Step 91 remains blocked until" in normalized,
                "E_CONTROL_CURRENT_STATE", path)


def current_validator_marker(validator_raw: bytes) -> str:
    return (
        f"Current-validator marker: sha256={sha256(validator_raw)}; "
        f"raw_bytes={len(validator_raw)}; physical_lines={line_count(validator_raw)}; "
        f"self_tests={SELF_TEST_COUNT}"
    )


def current_validator_section(validator_raw: bytes) -> str:
    validator_lines = line_count(validator_raw)
    return "\n".join([
        "Current validator identity:",
        "",
        f"- `{len(validator_raw):,}` raw bytes and `{validator_lines:,}` physical lines;",
        f"- SHA-256 `{sha256(validator_raw)}`;",
        "- machine collection and final review must bind this identity.",
    ])


def require_result_validator_identity(text: str, validator_raw: bytes) -> None:
    validator_lines = line_count(validator_raw)
    marker = current_validator_marker(validator_raw)
    marker_lines = re.findall(r"^Current-validator marker:.*$", text, re.MULTILINE)
    require(marker_lines == [marker], "E_RESULT_VALIDATOR_MARKER", repr(marker_lines))
    require(text.count(marker) == 1, "E_RESULT_VALIDATOR_MARKER_CARDINALITY")
    authority_lines = re.findall(r"^Validator-identity authority:.*$", text, re.MULTILINE)
    require(authority_lines == [VALIDATOR_IDENTITY_AUTHORITY],
            "E_RESULT_VALIDATOR_AUTHORITY", repr(authority_lines))
    coverage_line = (
        f"| `{VALIDATOR_PATH}` | current `1–{validator_lines}`, no gap | "
        "final repair candidate and current activation validator |"
    )
    coverage_lines = re.findall(
        rf"^\| `{re.escape(VALIDATOR_PATH)}` \| current .*$", text, re.MULTILINE,
    )
    require(coverage_lines == [coverage_line], "E_RESULT_VALIDATOR_COVERAGE",
            repr(coverage_lines))
    section = bounded_section(text, "Current validator identity:",
                              "## Activated Step Range", "E_RESULT_VALIDATOR_SECTION")
    require(section.strip() == current_validator_section(validator_raw),
            "E_RESULT_VALIDATOR_SECTION")
    heading = f"| Check on current {validator_lines:,}-line validator | Python 3.12 | Python 3.14 |"
    self_test_row = (
        f"| direct `self_test_core()` | exit `0`, `{SELF_TEST_COUNT}/{SELF_TEST_COUNT}` | "
        f"exit `0`, `{SELF_TEST_COUNT}/{SELF_TEST_COUNT}` |"
    )
    heading_lines = re.findall(r"^\| Check on current .*line validator \|.*$",
                               text, re.MULTILINE)
    self_test_lines = re.findall(r"^\| direct `self_test_core\(\)` \|.*$",
                                 text, re.MULTILINE)
    require(heading_lines == [heading], "E_RESULT_VALIDATOR_TEST_HEADING",
            repr(heading_lines))
    require(self_test_lines == [self_test_row], "E_RESULT_VALIDATOR_SELF_TEST",
            repr(self_test_lines))
    current_ranges = re.findall(r"\bcurrent\s+`?1[–-]([0-9,]+)`?", text, re.IGNORECASE)
    require(current_ranges == [str(validator_lines)],
            "E_RESULT_VALIDATOR_AMBIGUOUS", repr(current_ranges))


def control_identities() -> list[dict[str, Any]]:
    shared = [
        "Phase 068", PLAN_PATH, VALIDATOR_PATH, OUTPUT_PATH, RESULT_PATH, EXPECTED_PARENT,
        EXPECTED_SUBJECT, GATE, PRECOMMIT_STATUS, PENDING_COMMIT, PERSISTENCE,
        PREDECESSOR_TERMINAL, "Step 91",
    ]
    records = []
    for path in (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH):
        raw, text = read_lf(path), read_text(path)
        require_tokens(text, shared, "E_CONTROL_TOKEN")
        require_control_current_state(path, text)
        require("CONDITIONAL_P068" not in text and "FAIL_P068" not in text,
                "E_CONTROL_UNDEFINED_GATE", path)
        if path == RESULT_PATH:
            require_result_validator_identity(text, read_lf(VALIDATOR_PATH))
            require_tokens(text, ["A/A/A/A/M/M/M", "100644", FINAL_GATE,
                                  "result-first", "JSON-last"], "E_RESULT_CONTRACT")
        elif path in {PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH}:
            require(re.search(r"\|\s*068\s*\|\s*91[–-]98\s*\|", text) is not None,
                    "E_LEDGER_PHASE068_ROW", path)
        records.append({"path": path, "lf_bytes": len(raw), "lf_lines": line_count(raw),
                        "lf_sha256": sha256(raw)})
    return records


def identities(paths: list[str]) -> list[dict[str, Any]]:
    records = []
    for path in paths:
        raw = read_lf(path)
        records.append({"path": path, "lf_bytes": len(raw), "lf_lines": line_count(raw),
                        "lf_sha256": sha256(raw)})
    return records


def build_payload() -> dict[str, Any]:
    plan_raw = read_lf(PLAN_PATH)
    plan_text = plan_raw.decode("utf-8", errors="strict")
    plan_contract = validate_plan(plan_text)
    plan_negative_controls = plan_mutation_self_tests(plan_text)
    boundaries = fixed_boundaries()
    predecessor = fixed_predecessor()
    topology = fork_topology()
    document: dict[str, Any] = {
        "schema_version": "P068-PLAN-ACTIVATION-1", "generated_date": "2026-09-07",
        "phase": "068", "status": PRECOMMIT_STATUS, "gate": GATE,
        "containing_commit": PENDING_COMMIT, "persistence_terminal": PERSISTENCE,
        "expected_subject": EXPECTED_SUBJECT,
        "transaction": {"count": 7, "paths": FINAL_PATHS,
                        "status": [FINAL_STATUS[path] for path in FINAL_PATHS],
                        "modes": ["100644"] * 7, "rename_allowed": False,
                        "result_first": True, "validation_json_last": True},
        "plan": {"path": PLAN_PATH, "lf_bytes": len(plan_raw),
                 "lf_lines": line_count(plan_raw), "lf_sha256": sha256(plan_raw),
                 "negative_mutation_controls": plan_negative_controls, **plan_contract},
        "nonself_artifact_identities": identities(NONSELF_PATHS),
        "control_document_identities": control_identities(),
        "fixed_predecessor": predecessor,
        "fixed_boundaries": boundaries,
        "fork_topology": topology,
        "authority_ceiling": {
            "activation_only": True, "canonical_model": False, "canonical_release": False,
            "production_modified": False, "scholarly_main_body_modified": False,
            "external_scientific_validated": False, "held_out_validated": False,
            "material_assignment_validated": False, "whole_commit_cherry_pick_authorized": False,
            "unresolved_route": "UNVERIFIED", "final_positive_gate": FINAL_GATE,
        },
        "strict_json_contract": {
            "duplicate_keys_rejected": True, "nonfinite_rejected": True,
            "canonical_bytes_required": True, "max_bytes": MAX_JSON_BYTES,
            "max_depth": MAX_JSON_DEPTH, "max_nodes": MAX_JSON_NODES,
            "max_string_bytes": MAX_JSON_STRING_BYTES,
        },
        "git_execution": {"argv_arrays_only": True, "shell": False,
                          "allowlisted_subcommands": True},
        "repository_state_contract": {
            "precommit_head": EXPECTED_PARENT, "persistence_parent": EXPECTED_PARENT,
            "active_branch": ACTIVE_BRANCH, "active_upstream": UPSTREAM,
            "fixed_predecessor_is_commit_addressed": True,
            "fixed_predecessor_requires_current_head": False,
            "precommit_and_persistence_head_checks_are_separate": True,
        },
    }
    document["semantic_sha256"] = semantic_hash(document)
    return document


def read_stored() -> tuple[dict[str, Any], bytes, int, int]:
    require(OUTPUT.is_file() and not OUTPUT.is_symlink(), "E_OUTPUT_MISSING")
    raw = OUTPUT.read_bytes()
    require(raw == lf_bytes(raw), "E_OUTPUT_LINE_ENDINGS")
    document, nodes, depth = strict_load(raw, OUTPUT_PATH)
    require(raw == canonical_bytes(document), "E_OUTPUT_NONCANONICAL")
    require(document.get("semantic_sha256") == semantic_hash(document), "E_OUTPUT_SEMANTIC")
    return document, raw, nodes, depth


def validate_expected_commit(value: str | None) -> str:
    require(value is not None and is_oid(value), "E_EXPECTED_COMMIT", repr(value))
    return value


def active_snapshot(expected: str, stage: str) -> dict[str, str]:
    state = {
        "branch": git_text(["branch", "--show-current"]),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]),
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream": git_text(["rev-parse", "@{upstream}"]),
        "tracking": git_text(["rev-parse", ACTIVE_REMOTE_REF]),
        "live": live_tip(ACTIVE_BRANCH),
    }
    require(state["branch"] == ACTIVE_BRANCH, f"E_{stage}_BRANCH")
    require(state["upstream_name"] == UPSTREAM, f"E_{stage}_UPSTREAM_NAME")
    require(all(state[key] == expected for key in ("head", "upstream", "tracking", "live")),
            f"E_{stage}_HEAD", repr(state))
    return state


def validate_worktree(expected: dict[str, str], staged: bool) -> dict[str, Any]:
    require(all((ROOT / path).is_file() and not (ROOT / path).is_symlink() for path in expected),
            "E_TRANSACTION_FILE_TYPE")
    if staged:
        status = staged_status()
        require(status == expected, "E_STAGED_STATUS", repr(status))
        require(not unstaged_status() and not untracked_paths(), "E_STAGED_COMPANIONS")
        entries = index_entries(list(expected))
        require(set(entries) == set(expected), "E_STAGED_INDEX_PATHS")
        require(all(row["mode"] == "100644" for row in entries.values()), "E_STAGED_MODES")
        worktree_hashes = {path: sha256(read_lf(path)) for path in expected}
        index_hashes = {path: sha256(index_blob(path)) for path in expected}
        require(worktree_hashes == index_hashes, "E_STAGED_WORKTREE_BYTES")
        require(run_git(["diff", "--cached", "--check"], check=False).returncode == 0,
                "E_STAGED_DIFF_CHECK")
        return {"status": status, "worktree": worktree_hashes, "index": index_hashes}
    require(not staged_status(), "E_WORKTREE_HAS_STAGED")
    status = worktree_status()
    require(status == expected, "E_WORKTREE_STATUS", repr(status))
    require(run_git(["diff", "--check"], check=False).returncode == 0,
            "E_WORKTREE_DIFF_CHECK")
    return {"status": status, "worktree": {path: sha256(read_lf(path)) for path in expected}}


def atomic_collect(raw: bytes) -> None:
    require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST")
    temporary = OUTPUT.with_name(f"{OUTPUT.name}.tmp-{os.getpid()}")
    require(not temporary.exists(), "E_COLLECT_TEMP_EXISTS")
    linked = False
    try:
        with temporary.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        document, _, _ = strict_load(temporary.read_bytes(), str(temporary))
        require(canonical_bytes(document) == raw, "E_COLLECT_TEMP_CANONICAL")
        try:
            os.link(temporary, OUTPUT)
            linked = True
        except FileExistsError as error:
            raise ValidationError("E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH) from error
    finally:
        if temporary.exists():
            temporary.unlink()
    require(linked and OUTPUT.read_bytes() == raw, "E_COLLECT_WRITE")


def persistence_snapshot(commit: str) -> dict[str, Any]:
    active = active_snapshot(commit, "PERSISTENCE")
    require(not staged_status() and not unstaged_status() and not untracked_paths(),
            "E_PERSISTENCE_DIRTY")
    parents = git_text(["show", "-s", "--format=%P", commit]).split()
    subject = git_text(["show", "-s", "--format=%s", commit])
    require(parents == [EXPECTED_PARENT], "E_PERSISTENCE_PARENT", repr(parents))
    require(subject == EXPECTED_SUBJECT, "E_PERSISTENCE_SUBJECT")
    status = parse_status(run_git([
        "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-z", "-r", commit,
    ]).stdout)
    require(status == FINAL_STATUS, "E_PERSISTENCE_STATUS", repr(status))
    entries = tree_entries(commit, FINAL_PATHS)
    require(set(entries) == set(FINAL_PATHS), "E_PERSISTENCE_TREE")
    require(all(row["mode"] == "100644" for row in entries.values()), "E_PERSISTENCE_MODES")
    hashes = {}
    for path in FINAL_PATHS:
        committed, worktree = git_blob(commit, path), read_lf(path)
        require(committed == worktree, "E_PERSISTENCE_BLOB", path)
        hashes[path] = sha256(committed)
    diff = run_git(["diff", "--quiet", EXPECTED_PARENT, commit, "--", "Claude"], check=False)
    require(diff.returncode == 0, "E_PERSISTENCE_FORBIDDEN_CLAUDE_DRIFT")
    return {"active": active, "parents": parents, "subject": subject,
            "status": status, "entries": entries, "hashes": hashes}


def reconstruct_stored() -> tuple[dict[str, Any], int, int]:
    stored, raw, nodes, depth = read_stored()
    first, second = build_payload(), build_payload()
    expected = canonical_bytes(first)
    require(expected == canonical_bytes(second), "E_PAYLOAD_NONDETERMINISTIC")
    require(raw == expected, "E_STORED_RECONSTRUCTION")
    return stored, nodes, depth


def expect_code(code: str, operation: Callable[[], Any]) -> None:
    try:
        operation()
    except ValidationError as error:
        require(error.code == code, "E_SELF_TEST_WRONG_CODE", f"{code}:{error.code}")
    else:
        raise ValidationError("E_SELF_TEST_MISSED", code)


def self_test_core() -> int:
    expect_code("E_JSON_DUPLICATE_KEY", lambda: strict_load(b'{"a":1,"a":2}', "duplicate"))
    expect_code("E_JSON_NONFINITE", lambda: strict_load(b'{"a":NaN}', "nonfinite"))
    expect_code("E_JSON_ROOT", lambda: strict_load(b'[]', "root"))
    expect_code("E_EXPECTED_COMMIT", lambda: validate_expected_commit("A" * 40))
    expect_code("E_STATUS_RENAME_OR_TYPE", lambda: parse_status(b'R100\0a\0'))
    expect_code("E_GIT_SUBCOMMAND", lambda: validate_git_argv(["fetch"]))
    deep = b'{"a":' + b"[" * 3000 + b"0" + b"]" * 3000 + b"}"
    try:
        strict_load(deep, "deep-3000")
    except ValidationError as error:
        require(error.code in {"E_JSON_DEPTH", "E_JSON_RECURSION"},
                "E_SELF_TEST_DEEP_CODE", error.code)
    else:
        raise ValidationError("E_SELF_TEST_MISSED", "deep-3000")
    expect_code("E_GIT_ARGV_SHAPE", lambda: validate_git_argv([
        "cat-file", "-e", f"{'0' * 40}^{{commit}}",
    ]))
    cat_file_calls: list[list[str]] = []

    def noncommit_runner(args: list[str]) -> subprocess.CompletedProcess[bytes]:
        cat_file_calls.append(list(args))
        return subprocess.CompletedProcess(["git", *args], 1, b"", b"not a commit")

    expect_code("E_FIXED_COMMIT_OBJECT",
                lambda: require_fixed_commit(PROTECTED_TIP, noncommit_runner))
    require(cat_file_calls == [["cat-file", "-e", f"{PROTECTED_TIP}^{{commit}}"]],
            "E_SELF_TEST_CAT_FILE_ARGV")
    protected_ref = f"refs/heads/{PROTECTED_BRANCH}"
    expect_code("E_GIT_ARGV_SHAPE", lambda: validate_git_argv([
        "ls-remote", "origin", protected_ref, "refs/heads/main",
    ]))
    expect_code("E_GIT_ARGV_SHAPE", lambda: validate_git_argv([
        "ls-remote", "origin", "refs/heads/not-allowlisted",
    ]))
    expect_code("E_GIT_ARGV_SHAPE", lambda: validate_git_argv([
        "ls-remote", "upstream", protected_ref,
    ]))

    bad_calls: list[list[str]] = []

    def bad_origin_runner(args: list[str]) -> subprocess.CompletedProcess[bytes]:
        bad_calls.append(list(args))
        return subprocess.CompletedProcess(["git", *args], 0, b"https://example.invalid/wrong.git\n", b"")

    expect_code("E_ORIGIN_URL", lambda: live_tip(PROTECTED_BRANCH, bad_origin_runner))
    require(bad_calls == [["remote", "get-url", "origin"]], "E_SELF_TEST_PREFLIGHT_STOP")

    good_calls: list[list[str]] = []

    def ordered_runner(args: list[str]) -> subprocess.CompletedProcess[bytes]:
        good_calls.append(list(args))
        raw = (ORIGIN_URL + "\n").encode() if args[0] == "remote" else \
            f"{PROTECTED_TIP}\t{protected_ref}\n".encode()
        return subprocess.CompletedProcess(["git", *args], 0, raw, b"")

    require(live_tip(PROTECTED_BRANCH, ordered_runner) == PROTECTED_TIP,
            "E_SELF_TEST_LIVE_RESULT")
    require(good_calls == [
        ["remote", "get-url", "origin"], ["ls-remote", "origin", protected_ref],
    ], "E_SELF_TEST_PREFLIGHT_ORDER", repr(good_calls))
    marker_fixture = CURRENT_STATE_LINE + "\n" + CURRENT_STATE_AUTHORITY
    require_control_current_state(HANDOVER_PATH, marker_fixture)
    expect_code("E_CONTROL_STALE_CURRENT_STATE", lambda: require_control_current_state(
        HANDOVER_PATH,
        marker_fixture + "\n`Step 90.2` remains current at pending persistence.",
    ))
    expect_code("E_CONTROL_STALE_CURRENT_STATE", lambda: require_control_current_state(
        HANDOVER_PATH,
        marker_fixture + "\nStep 90.2 is still current.",
    ))
    expect_code("E_CONTROL_STALE_CURRENT_STATE", lambda: require_control_current_state(
        HANDOVER_PATH,
        marker_fixture + "\nStep 90.2 continues to be current.",
    ))
    expect_code("E_CONTROL_CURRENT_STATE", lambda: require_control_current_state(
        HANDOVER_PATH, "Step 90.2 subsequently persisted.",
    ))
    expect_code("E_CONTROL_CURRENT_STATE", lambda: require_control_current_state(
        HANDOVER_PATH, marker_fixture + "\nCurrent-state marker: `WRONG_STATE`",
    ))
    expect_code("E_CONTROL_STATE_AUTHORITY", lambda: require_control_current_state(
        HANDOVER_PATH, marker_fixture + "\nState-marker authority: conflicting authority.",
    ))
    expect_code("E_CONTROL_AMBIGUOUS_CURRENT_PROSE", lambda: require_control_current_state(
        HANDOVER_PATH, marker_fixture + "\nIt is false that Phase 068 plan activation is current.",
    ))
    expect_code("E_CONTROL_AMBIGUOUS_CURRENT_PROSE", lambda: require_control_current_state(
        HANDOVER_PATH,
        marker_fixture + "\nThe claim that Phase 068 plan activation is current is rejected.",
    ))
    expect_code("E_CONTROL_AMBIGUOUS_CURRENT_PROSE", lambda: require_control_current_state(
        HANDOVER_PATH,
        marker_fixture + "\nPhase 068 plan activation is current only in an obsolete report, not now.",
    ))
    identity_fixture = b"validator fixture\n"
    fixture_coverage = (
        f"| `{VALIDATOR_PATH}` | current `1–1`, no gap | "
        "final repair candidate and current activation validator |"
    )
    identity_text = "\n".join([
        current_validator_marker(identity_fixture),
        VALIDATOR_IDENTITY_AUTHORITY,
        fixture_coverage,
        current_validator_section(identity_fixture),
        "## Activated Step Range",
        "| Check on current 1-line validator | Python 3.12 | Python 3.14 |",
        f"| direct `self_test_core()` | exit `0`, `{SELF_TEST_COUNT}/{SELF_TEST_COUNT}` | "
        f"exit `0`, `{SELF_TEST_COUNT}/{SELF_TEST_COUNT}` |",
    ])
    require_result_validator_identity(identity_text, identity_fixture)
    expect_code("E_RESULT_VALIDATOR_MARKER", lambda: require_result_validator_identity(
        identity_text.replace(sha256(identity_fixture), "0" * 64), identity_fixture,
    ))
    expect_code("E_RESULT_VALIDATOR_MARKER", lambda: require_result_validator_identity(
        identity_text + "\nCurrent-validator marker: sha256=" + "0" * 64
        + "; raw_bytes=999999; physical_lines=999; self_tests=0",
        identity_fixture,
    ))
    expect_code("E_RESULT_VALIDATOR_AUTHORITY", lambda: require_result_validator_identity(
        identity_text + "\nValidator-identity authority: conflicting authority.",
        identity_fixture,
    ))
    expect_code("E_RESULT_VALIDATOR_COVERAGE", lambda: require_result_validator_identity(
        identity_text + f"\n| `{VALIDATOR_PATH}` | current `1–999`, no gap | wrong |",
        identity_fixture,
    ))
    expect_code("E_RESULT_VALIDATOR_AMBIGUOUS", lambda: require_result_validator_identity(
        identity_text + "\ncurrent 1–999; 999,999 raw bytes; SHA-256 " + "0" * 64,
        identity_fixture,
    ))
    require(canonical_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}\n',
            "E_SELF_TEST_CANONICAL")
    return SELF_TEST_COUNT


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    modes = [args.collect, args.content_only, args.verify_staged, args.verify_persistence]
    require(sum(bool(mode) for mode in modes) == 1, "E_CLI_MODE")
    require((args.verify_persistence and args.expected_commit is not None)
            or (not args.verify_persistence and args.expected_commit is None),
            "E_EXPECTED_COMMIT_MODE")
    expected_commit = validate_expected_commit(args.expected_commit) if args.verify_persistence else None
    self_tests = self_test_core()
    if args.collect:
        require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
        before = active_snapshot(EXPECTED_PARENT, "PRECOMMIT")
        validate_worktree(NONSELF_STATUS, False)
        first, second = build_payload(), build_payload()
        raw = canonical_bytes(first)
        require(raw == canonical_bytes(second), "E_PAYLOAD_NONDETERMINISTIC")
        atomic_collect(raw)
        stored, nodes, depth = reconstruct_stored()
        validate_worktree(FINAL_STATUS, False)
        require(before == active_snapshot(EXPECTED_PARENT, "PRECOMMIT"), "E_PRECOMMIT_TOCTOU")
        require(stored["transaction"]["validation_json_last"] is True, "E_JSON_LAST")
        print(f"{GATE} collect=JSON_LAST result_first=true exact-seven=7/7 "
              f"json_nodes={nodes} depth={depth} self_tests={self_tests}/{SELF_TEST_COUNT}")
        return 0
    stored, nodes, depth = reconstruct_stored()
    require(stored.get("gate") == GATE and stored.get("status") == PRECOMMIT_STATUS,
            "E_STORED_GATE_STATUS")
    if args.content_only:
        before = active_snapshot(EXPECTED_PARENT, "PRECOMMIT")
        validate_worktree(FINAL_STATUS, False)
        require(before == active_snapshot(EXPECTED_PARENT, "PRECOMMIT"), "E_PRECOMMIT_TOCTOU")
        print(f"{GATE} content-only=true exact-seven=7/7 json_nodes={nodes} "
              f"depth={depth} self_tests={self_tests}/{SELF_TEST_COUNT}")
    elif args.verify_staged:
        before = active_snapshot(EXPECTED_PARENT, "PRECOMMIT")
        validate_worktree(FINAL_STATUS, True)
        require(before == active_snapshot(EXPECTED_PARENT, "PRECOMMIT"), "E_STAGED_TOCTOU")
        print(f"{STAGED_GATE} exact-seven=7/7 modes=100644/7 companions=0")
    else:
        require(expected_commit is not None, "E_INTERNAL_EXPECTED_COMMIT")
        before = persistence_snapshot(expected_commit)
        fixed_boundaries()
        require(before == persistence_snapshot(expected_commit), "E_PERSISTENCE_TOCTOU")
        print(f"{PERSISTENCE} commit={expected_commit} exact-seven=7/7 modes=100644/7 clean=true")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, RecursionError,
            UnicodeError, subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, ValidationError) else \
            "E_JSON_RECURSION" if isinstance(error, RecursionError) else type(error).__name__
        print(f"FAIL_P068_PLAN_ACTIVATION {code}: {error}")
        raise SystemExit(1)
