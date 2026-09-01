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
from collections import Counter
from typing import Any, Callable


ROOT = pathlib.Path(__file__).resolve().parents[3]
PLAN_PATH = "Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md"
VALIDATOR_PATH = "Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py"
OUTPUT_PATH = "Codex/results/PHASE_067_PLAN_ACTIVATION_VALIDATION.json"
RESULT_PATH = "Codex/results/PHASE_067_PLAN_ACTIVATION_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
CARRY_PATH = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"
PREDECESSOR_JSON_PATH = "Codex/results/PHASE_066_VALIDATION.json"
PREDECESSOR_VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_final.py"
PREDECESSOR_RESULT_PATH = "Codex/results/PHASE_066_RESULT.md"

PLAN = ROOT / PLAN_PATH
VALIDATOR = ROOT / VALIDATOR_PATH
OUTPUT = ROOT / OUTPUT_PATH

EXPECTED_PARENT = "7241b331ff76bc8d43cb1bc6b69634977e0884a0"
EXPECTED_PARENT_PARENT = "bdad7375d70c3734cc63265d94a61dd82afd143d"
EXPECTED_PARENT_SUBJECT = "audit(phase066): close v1025 lineage gate"
EXPECTED_SUBJECT = "docs(phase067): plan code test fitting cross-audit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{ACTIVE_BRANCH}"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
GATE = "PASS_P067_PLAN_ACTIVATION"
PERSISTENCE = "PASS_P067_PLAN_ACTIVATION_PERSISTENCE"

PREDECESSOR_JSON_SHA256 = "2893670d87ab414c7243d0ed862ba19d2055d84260ca2f6f5c2ebc3ff5407577"
PREDECESSOR_SEMANTIC_SHA256 = "925556e534b9be49f4aed6d1889729d4f567350c5d09c6b09685d08442e3419e"
PREDECESSOR_VALIDATOR_SHA256 = "7ae55f2d1d541aacc89ba7b067d3027f1f9af18635fb9b90dbdc7515d33bc164"

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
NONSELF_STATUS = {path: status for path, status in FINAL_STATUS.items() if path != OUTPUT_PATH}

PREDECESSOR_FINAL_STATUS = {
    "Codex/work/v1025_phase066/validate_phase066_final.py": "A",
    "Codex/results/PHASE_066_VALIDATION.json": "A",
    "Codex/results/PHASE_066_V1025_V1025_2_LINEAGE_REPORT_I.md": "A",
    "Codex/results/PHASE_066_STEP_081_2_GATE_RESULT.md": "A",
    "Codex/results/PHASE_066_RESULT.md": "A",
    PARENT_LEDGER_PATH: "M",
    ACTIVE_LEDGER_PATH: "M",
    HANDOVER_PATH: "M",
}

SUPPLEMENTAL_FIT_INPUTS = [
    ("Claude/results/comp_v24/sintef_data/sigr.csv", "DIRECT14_RAW_DATA_CANDIDATE", False),
    ("Claude/results/comp_v24/sintef_data/SOURCES.md", "SOURCE_PROVENANCE_STATEMENT", False),
    ("Claude/results/comp_v26_data/build_two_versions.py", "COMPARISON_BUILDER", False),
    ("Claude/results/comp_v26_data/test_skew_regsol_v2.py", "COMPARISON_TEST", False),
    ("Claude/results/comp_v26_data/bdd_dqdv.py", "COMPARISON_CALCULATION_HELPER", False),
    ("Claude/results/comp_v26_data/test_gallery_vs_regsol.py", "COMPARISON_TEST", False),
    ("Claude/results/comp_v26_data/out_versions/summary_versions.json", "SAVED_COMPARISON_SUMMARY", False),
    ("Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json", "SAVED_REGULAR_SOLUTION_PROFILE", True),
    ("Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json", "SAVED_GALLERY_PROFILE", True),
    ("Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json", "SAVED_SKEW_PROFILE", True),
]

RECOVERY_PATHS = [PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH]
STEP_OUTPUTS = {
    "82": [
        "Codex/work/v1025_phase067/build_phase067_step82.py",
        "Codex/work/v1025_phase067/validate_phase067_step82.py",
        "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json",
        "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json",
        "Codex/results/PHASE_067_STEP_082_SOURCE_TOPOLOGY_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "83": [
        "Codex/work/v1025_phase067/build_phase067_step83.py",
        "Codex/work/v1025_phase067/validate_phase067_step83.py",
        "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json",
        "Codex/results/PHASE_067_STEP_083_STATE_FLOW_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "84": [
        "Codex/work/v1025_phase067/build_phase067_step84.py",
        "Codex/work/v1025_phase067/validate_phase067_step84.py",
        "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json",
        "Codex/results/PHASE_067_STEP_084_PHYSICS_CALL_GRAPH_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "85": [
        "Codex/work/v1025_phase067/build_phase067_step85.py",
        "Codex/work/v1025_phase067/validate_phase067_step85.py",
        "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json",
        "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json",
        "Codex/results/PHASE_067_STEP_085_STATE_DEFAULT_IMPORT_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "86": [
        "Codex/work/v1025_phase067/build_phase067_step86.py",
        "Codex/work/v1025_phase067/validate_phase067_step86.py",
        "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json",
        "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json",
        "Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "87": [
        "Codex/work/v1025_phase067/build_phase067_step87.py",
        "Codex/work/v1025_phase067/validate_phase067_step87.py",
        "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json",
        "Codex/results/PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "88": [
        "Codex/work/v1025_phase067/build_phase067_step88.py",
        "Codex/work/v1025_phase067/validate_phase067_step88.py",
        "Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json",
        "Codex/results/PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "89": [
        "Codex/work/v1025_phase067/build_phase067_step89.py",
        "Codex/work/v1025_phase067/validate_phase067_step89.py",
        "Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json",
        "Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json",
        "Codex/results/PHASE_067_STEP_089_FITTING_AUTHORITY_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "90.1": [
        "Codex/work/v1025_phase067/build_phase067_step90_dispositions.py",
        "Codex/work/v1025_phase067/validate_phase067_step90_dispositions.py",
        "Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json",
        "Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json",
        "Codex/results/PHASE_067_STEP_090_1_DISPOSITION_RESULT.md",
        *RECOVERY_PATHS,
    ],
    "90.2": [
        "Codex/work/v1025_phase067/validate_phase067_final.py",
        "Codex/results/PHASE_067_VALIDATION.json",
        "Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md",
        "Codex/results/PHASE_067_STEP_090_2_GATE_RESULT.md",
        "Codex/results/PHASE_067_RESULT.md",
        *RECOVERY_PATHS,
    ],
}

EXPECTED_IMPORT_SEAL = [
    ("from", "__future__", (("annotations", None),)),
    ("import", None, (("argparse", None),)),
    ("import", None, (("ast", None),)),
    ("import", None, (("copy", None),)),
    ("import", None, (("hashlib", None),)),
    ("import", None, (("json", None),)),
    ("import", None, (("math", None),)),
    ("import", None, (("os", None),)),
    ("import", None, (("pathlib", None),)),
    ("import", None, (("re", None),)),
    ("import", None, (("subprocess", None),)),
    ("from", "collections", (("Counter", None),)),
    ("from", "typing", (("Any", None), ("Callable", None))),
]

EXPECTED_RELEASES = [
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14",
    "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2",
    "v1.0.19", "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23",
    "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
]
EXPECTED_OWNERS = [
    ("P065-OBL-0054", "P065-S72-F04"),
    ("P066-OBL-0120", "P066-P79-07"),
    ("P066-OBL-0125", "P066-R80-14"),
]
EXPECTED_STEPS = ["82", "83", "84", "85", "86", "87", "88", "89", "90.1", "90.2"]
EXPECTED_FINAL_GATES = ["PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067"]

REQUIRED_HEADINGS = [
    "## Summary",
    "## Current Ground Truth",
    "## Phase Range",
    "## Exact Read Inputs",
    "## Non-goals and Scope Guards",
    "## Implementation Changes",
    "## Plan Activation Unit — Save Before Step 82",
    "## Phase 067 — Code, Test, and Fitting Cross-Audit",
    "## Phase Gate",
    "## Canonical-Evidence Reuse Protocol",
    "## Implementation Interfaces",
    "## Test and Validation Plan",
    "## Stop Conditions",
    "## Assumptions",
    "## Correction History",
]
REQUIRED_PLAN_TOKENS = [
    "129", "84", "29,952", "20", "44", "29", "30", "26", "8", "2", "35",
    "14", "854", "Step 82", "Step 83", "Step 84", "Step 85", "Step 86",
    "Step 87", "Step 88", "Step 89", "Step 90.1", "Step 90.2",
    "PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067",
    "P065-OBL-0054", "P065-S72-F04", "P066-OBL-0120", "P066-P79-07",
    "P066-OBL-0125", "P066-R80-14", "P067-CODE-HISTORY",
    "result-first", "JSON-last", "untested code", "FITTING_GUIDE",
    "Ref. 7", "original optimizer", "held-out", "external", "material", "stale",
    "No production", "main scholarly body", "CANONICAL_REUSED_14/14",
    "fresh_historical_replay=0/14",
]
CONTROL_TOKENS = {
    RESULT_PATH: [
        GATE, "PASS_PENDING_PERSISTENCE", "PENDING_AT_PRECOMMIT_BY_DESIGN",
        EXPECTED_PARENT, EXPECTED_SUBJECT, "A/A/A/A/M/M/M", "Step 82",
        "PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067",
    ],
    PARENT_LEDGER_PATH: [
        "| 067 | 82–90 |", "PASS_PENDING_PERSISTENCE", PLAN_PATH, RESULT_PATH,
        OUTPUT_PATH, VALIDATOR_PATH, GATE, EXPECTED_PARENT, PERSISTENCE,
    ],
    ACTIVE_LEDGER_PATH: [
        "| 067 | 82–90 |", "PASS_PENDING_PERSISTENCE", PLAN_PATH, RESULT_PATH,
        OUTPUT_PATH, VALIDATOR_PATH, GATE, EXPECTED_PARENT,
        "PENDING_AT_PRECOMMIT_BY_DESIGN", PERSISTENCE,
        "PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067",
    ],
    HANDOVER_PATH: [
        "Phase 067", "PASS_P067_PLAN_ACTIVATION", "PASS_PENDING_PERSISTENCE",
        EXPECTED_PARENT, EXPECTED_SUBJECT, "PENDING_AT_PRECOMMIT_BY_DESIGN",
        PERSISTENCE, "Step 82", "129/84/29,952", "20/8/854",
    ],
}

ALLOWED_IMPORT_ROOTS = {
    "__future__", "argparse", "ast", "collections", "copy", "hashlib", "json",
    "math", "os", "pathlib", "re", "subprocess", "typing",
}


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def validate_terminal_seal(entry: dict[str, Any], terminal: dict[str, Any], code: str) -> None:
    require(entry == terminal, code)


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
    raise ValidationError("E_JSON_NONFINITE", value)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def inspect_json_value(value: Any, depth: int = 0) -> tuple[int, int, int]:
    require(depth <= 32, "E_JSON_DEPTH", str(depth))
    if isinstance(value, float):
        require(math.isfinite(value), "E_JSON_NONFINITE", repr(value))
    if isinstance(value, dict):
        nodes = 1
        scalars = 0
        maximum = depth
        for key, item in value.items():
            require(type(key) is str, "E_JSON_KEY", repr(key))
            child_nodes, child_scalars, child_depth = inspect_json_value(item, depth + 1)
            nodes += child_nodes
            scalars += child_scalars
            maximum = max(maximum, child_depth)
        return nodes, scalars, maximum
    if isinstance(value, list):
        nodes = 1
        scalars = 0
        maximum = depth
        for item in value:
            child_nodes, child_scalars, child_depth = inspect_json_value(item, depth + 1)
            nodes += child_nodes
            scalars += child_scalars
            maximum = max(maximum, child_depth)
        return nodes, scalars, maximum
    require(value is None or type(value) in {str, int, float, bool}, "E_JSON_TYPE", str(type(value)))
    return 1, 1, depth


def strict_load_bytes(raw: bytes, label: str) -> tuple[dict[str, Any], int, int, int]:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValidationError("E_JSON_UTF8", label) from error
    try:
        document = json.loads(text, object_pairs_hook=reject_pairs, parse_constant=reject_constant)
    except json.JSONDecodeError as error:
        raise ValidationError("E_JSON_SYNTAX", f"{label}:{error.msg}") from error
    require(type(document) is dict, "E_JSON_ROOT", label)
    nodes, scalars, depth = inspect_json_value(document)
    return document, nodes, scalars, depth


def read_lf(path: str) -> bytes:
    full = ROOT / path
    require(full.is_file(), "E_INPUT_MISSING", path)
    return lf_bytes(full.read_bytes())


def git_oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def git_read_paths(paths: list[str], *, claude_root_allowed: bool = False) -> bool:
    allowed = FINAL_PATH_SET | set(PREDECESSOR_FINAL_STATUS) | {
        path for path, _, _ in SUPPLEMENTAL_FIT_INPUTS
    } | {MANIFEST_PATH, CARRY_PATH, PREDECESSOR_RESULT_PATH}
    if claude_root_allowed:
        allowed.add("Claude")
    return bool(paths) and len(paths) == len(set(paths)) and set(paths) <= allowed


def validate_git_argv(args: list[str]) -> None:
    require(bool(args), "E_GIT_ARGV", "empty")
    require(all(type(item) is str and "\0" not in item and "\n" not in item and "\r" not in item
                for item in args), "E_GIT_ARGV", repr(args))
    command = args[0]
    if command == "branch":
        require(args == ["branch", "--show-current"], "E_GIT_BRANCH_SHAPE", repr(args))
    elif command == "diff":
        status_shapes = {
            ("diff", "--cached", "--no-renames", "--name-status", "-z"),
            ("diff", "--no-renames", "--name-status", "-z"),
            ("diff", "--check"),
            ("diff", "--cached", "--check"),
        }
        quiet = (len(args) == 6 and args[1] == "--quiet" and git_oid(args[2])
                 and git_oid(args[3]) and args[4:] == ["--", "Claude"])
        require(tuple(args) in status_shapes or quiet, "E_GIT_DIFF_SHAPE", repr(args))
    elif command == "diff-tree":
        require(len(args) == 7
                and args[1:6] == [
                    "--no-commit-id", "--no-renames", "--name-status", "-z", "-r"
                ] and git_oid(args[6]),
                "E_GIT_DIFF_TREE_SHAPE", repr(args))
    elif command == "ls-files":
        other = args == ["ls-files", "--others", "--exclude-standard", "-z"]
        staged = len(args) >= 5 and args[1:4] == ["--stage", "-z", "--"] \
            and git_read_paths(args[4:])
        require(other or staged, "E_GIT_LS_FILES_SHAPE", repr(args))
    elif command == "ls-remote":
        require(len(args) == 3 and args[1] == "origin"
                and args[2] in {
                    f"refs/heads/{ACTIVE_BRANCH}", f"refs/heads/{PROTECTED_BRANCH}", "refs/heads/main",
                }, "E_GIT_LS_REMOTE_SHAPE", repr(args))
    elif command == "ls-tree":
        require(len(args) >= 5 and args[1] == "-z" and git_oid(args[2]) and args[3] == "--"
                and git_read_paths(args[4:]), "E_GIT_LS_TREE_SHAPE", repr(args))
    elif command == "remote":
        require(args == ["remote", "get-url", "origin"], "E_GIT_REMOTE_SHAPE", repr(args))
    elif command == "rev-parse":
        single = len(args) == 2 and (
            args[1] in {
                "HEAD", "@{upstream}", f"refs/remotes/origin/{ACTIVE_BRANCH}",
                f"refs/heads/{PROTECTED_BRANCH}", f"refs/remotes/origin/{PROTECTED_BRANCH}",
                "refs/remotes/origin/main",
            } or git_oid(args[1])
        )
        upstream_name = args == ["rev-parse", "--abbrev-ref", "@{upstream}"]
        require(single or upstream_name, "E_GIT_REV_PARSE_SHAPE", repr(args))
    elif command == "show":
        metadata = len(args) == 4 and args[1] == "-s" and args[2] in {"--format=%P", "--format=%s"} \
            and git_oid(args[3])
        blob = False
        if len(args) == 2 and ":" in args[1]:
            revision, path = args[1].split(":", 1)
            blob = (revision == "" or git_oid(revision)) and git_read_paths([path])
        require(metadata or blob, "E_GIT_SHOW_SHAPE", repr(args))
    elif command == "show-ref":
        require(args == ["show-ref", "--verify", "--quiet", "refs/heads/main"],
                "E_GIT_SHOW_REF_SHAPE", repr(args))
    elif command == "status":
        require(args == ["status", "--porcelain=v1", "--", "Claude"],
                "E_GIT_STATUS_SHAPE", repr(args))
    else:
        require(False, "E_GIT_SUBCOMMAND", repr(args))


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    validate_git_argv(args)
    process = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, timeout=300, check=False, shell=False,
    )
    if check and process.returncode != 0:
        raise ValidationError(
            "E_GIT_PROCESS",
            f"{args!r}:{process.stderr.decode('utf-8', errors='replace')[-800:]}",
        )
    return process


def git_text(args: list[str]) -> str:
    return run_git(args).stdout.decode("utf-8", errors="strict").strip()


def git_blob(commit: str, path: str) -> bytes:
    return run_git(["show", f"{commit}:{path}"]).stdout


def live_tip(branch: str) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"]).splitlines()
    require(len(lines) == 1, "E_GIT_LIVE_REF", branch)
    return lines[0].split("\t", 1)[0]


def parse_name_status(raw: bytes) -> dict[str, str]:
    fields = raw.decode("utf-8", errors="strict").split("\0")
    if fields and fields[-1] == "":
        fields.pop()
    require(len(fields) % 2 == 0, "E_STATUS_PARSE", repr(fields[-3:]))
    result: dict[str, str] = {}
    for index in range(0, len(fields), 2):
        status, path = fields[index], fields[index + 1]
        require(status in {"A", "M", "D"}, "E_STATUS_CODE", status)
        require(path not in result, "E_STATUS_DUPLICATE", path)
        result[path] = status
    return result


def untracked_paths() -> list[str]:
    fields = run_git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout.decode(
        "utf-8", errors="strict"
    ).split("\0")
    return sorted(path for path in fields if path)


def staged_status() -> dict[str, str]:
    return parse_name_status(run_git(["diff", "--cached", "--no-renames", "--name-status", "-z"]).stdout)


def unstaged_status() -> dict[str, str]:
    return parse_name_status(run_git(["diff", "--no-renames", "--name-status", "-z"]).stdout)


def worktree_status() -> dict[str, str]:
    result = unstaged_status()
    for path in untracked_paths():
        require(path not in result, "E_WORKTREE_STATUS_COLLISION", path)
        result[path] = "A"
    return result


def tree_entries(commit: str, paths: list[str]) -> dict[str, dict[str, str]]:
    raw = run_git(["ls-tree", "-z", commit, "--", *paths]).stdout
    fields = raw.decode("utf-8", errors="strict").split("\0")
    result: dict[str, dict[str, str]] = {}
    for field in fields:
        if not field:
            continue
        metadata, path = field.split("\t", 1)
        mode, kind, blob = metadata.split(" ", 2)
        require(kind == "blob", "E_TREE_KIND", f"{path}:{kind}")
        require(path not in result, "E_TREE_DUPLICATE", path)
        result[path] = {"mode": mode, "blob_oid": blob}
    return result


def tree_modes(commit: str, paths: list[str]) -> dict[str, str]:
    return {path: record["mode"] for path, record in tree_entries(commit, paths).items()}


def index_modes(paths: list[str]) -> dict[str, str]:
    raw = run_git(["ls-files", "--stage", "-z", "--", *paths]).stdout
    fields = raw.decode("utf-8", errors="strict").split("\0")
    result: dict[str, str] = {}
    for field in fields:
        if not field:
            continue
        metadata, path = field.split("\t", 1)
        mode, _, stage = metadata.split(" ", 2)
        require(stage == "0", "E_INDEX_STAGE", f"{path}:{stage}")
        require(path not in result, "E_INDEX_DUPLICATE", path)
        result[path] = mode
    return result


def repository_snapshot(expected_tip: str) -> dict[str, Any]:
    snapshot = {
        "branch": git_text(["branch", "--show-current"]),
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]),
        "upstream": git_text(["rev-parse", "@{upstream}"]),
        "tracking_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"]),
        "live_active": live_tip(ACTIVE_BRANCH),
        "protected_local": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]),
        "protected_tracking": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"]),
        "protected_live": live_tip(PROTECTED_BRANCH),
        "main_tracking": git_text(["rev-parse", "refs/remotes/origin/main"]),
        "main_live": live_tip("main"),
        "local_main_absent": run_git(
            ["show-ref", "--verify", "--quiet", "refs/heads/main"], check=False
        ).returncode != 0,
        "claude_dirty": bool(run_git(["status", "--porcelain=v1", "--", "Claude"]).stdout),
        "origin_url": git_text(["remote", "get-url", "origin"]),
        "expected_tip": expected_tip,
        "diff_check": run_git(["diff", "--check"], check=False).returncode == 0,
        "cached_diff_check": run_git(["diff", "--cached", "--check"], check=False).returncode == 0,
    }
    validate_repository_record(snapshot, expected_tip)
    return snapshot


def validate_repository_record(snapshot: dict[str, Any], expected_tip: str) -> None:
    checks = [
        (snapshot.get("branch") == ACTIVE_BRANCH, "E_REPOSITORY_BRANCH"),
        (snapshot.get("head") == expected_tip, "E_REPOSITORY_HEAD"),
        (snapshot.get("upstream_name") == UPSTREAM, "E_REPOSITORY_UPSTREAM_NAME"),
        (snapshot.get("upstream") == expected_tip, "E_REPOSITORY_UPSTREAM"),
        (snapshot.get("tracking_active") == expected_tip, "E_REPOSITORY_TRACKING"),
        (snapshot.get("live_active") == expected_tip, "E_REPOSITORY_LIVE"),
        (snapshot.get("protected_local") == PROTECTED_TIP, "E_REPOSITORY_PROTECTED_LOCAL"),
        (snapshot.get("protected_tracking") == PROTECTED_TIP, "E_REPOSITORY_PROTECTED_TRACKING"),
        (snapshot.get("protected_live") == PROTECTED_TIP, "E_REPOSITORY_PROTECTED_LIVE"),
        (snapshot.get("main_tracking") == MAIN_TIP, "E_REPOSITORY_MAIN_TRACKING"),
        (snapshot.get("main_live") == MAIN_TIP, "E_REPOSITORY_MAIN_LIVE"),
        (snapshot.get("local_main_absent") is True, "E_REPOSITORY_LOCAL_MAIN"),
        (snapshot.get("claude_dirty") is False, "E_REPOSITORY_CLAUDE_DIRTY"),
        (snapshot.get("origin_url") == ORIGIN_URL, "E_REPOSITORY_ORIGIN"),
        (snapshot.get("expected_tip") == expected_tip, "E_REPOSITORY_EXPECTED_TIP"),
        (snapshot.get("diff_check") is True, "E_REPOSITORY_DIFF_CHECK"),
        (snapshot.get("cached_diff_check") is True, "E_REPOSITORY_CACHED_DIFF_CHECK"),
        (all(type(snapshot.get(key)) is str and re.fullmatch(r"[0-9a-f]{40}", snapshot[key])
             for key in ("head", "upstream", "tracking_active", "live_active")),
         "E_REPOSITORY_OID_FORMAT"),
    ]
    for condition, code in checks:
        require(condition, code)


def attribute_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def import_seal(tree: ast.Module) -> list[tuple[str, str | None, tuple[tuple[str, str | None], ...]]]:
    imports = sorted(
        (node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))),
        key=lambda node: (node.lineno, node.col_offset),
    )
    seal = []
    for node in imports:
        if isinstance(node, ast.Import):
            seal.append(("import", None, tuple((alias.name, alias.asname) for alias in node.names)))
        else:
            seal.append(("from", node.module, tuple((alias.name, alias.asname) for alias in node.names)))
    return seal


def validate_source_policy_text(source: str, label: str) -> dict[str, int]:
    tree = ast.parse(source, filename=label)
    require(import_seal(tree) == EXPECTED_IMPORT_SEAL, "E_SOURCE_POLICY_IMPORT_SEAL", label)
    function_for: dict[int, str] = {}

    def mark(node: ast.AST, owner: str) -> None:
        function_for[id(node)] = owner
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                mark(child, child.name)
            else:
                mark(child, owner)

    mark(tree, "<module>")
    path_variables: set[str] = set()
    callable_aliases: set[str] = set()
    module_escape_aliases: set[str] = set()
    sealed_modules = {"argparse", "ast", "copy", "hashlib", "json", "math", "os", "pathlib", "re", "subprocess"}
    restricted_callables = {
        "eval", "exec", "compile", "__import__", "open", "getattr", "globals", "locals",
    }
    filesystem_mutations = {
        "write_bytes", "write_text", "unlink", "rename", "replace", "touch", "mkdir",
        "rmdir", "chmod", "symlink_to", "hardlink_to", "open",
    }

    def restricted_rhs(node: ast.AST, restricted: set[str]) -> bool:
        if isinstance(node, ast.Name):
            return node.id in restricted
        if isinstance(node, ast.Call):
            dotted_func = attribute_name(node.func)
            direct_module = dotted_func is not None and len(dotted_func.split(".")) == 2 \
                and dotted_func.split(".", 1)[0] in sealed_modules
            direct_path_method = (
                isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call)
                and attribute_name(node.func.value.func) == "pathlib.Path"
            )
            approved_transform = (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in {"hexdigest", "encode"}
                and any(isinstance(item, ast.Call)
                        and attribute_name(item.func) in {"hashlib.sha256", "json.dumps"}
                        for item in ast.walk(node.func.value))
            )
            if direct_module or direct_path_method or approved_transform:
                return any(restricted_rhs(item, restricted) for item in (
                    [*node.args, *(keyword.value for keyword in node.keywords)]
                ))
        return any(restricted_rhs(child, restricted) for child in ast.iter_child_nodes(node))

    def module_transport(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id in sealed_modules
        if isinstance(node, ast.Call):
            return False
        return any(module_transport(child) for child in ast.iter_child_nodes(node))

    def transported_sensitive_callable(node: ast.AST) -> bool:
        parents = {
            id(child): parent for parent in ast.walk(node) for child in ast.iter_child_nodes(parent)
        }
        for item in ast.walk(node):
            parent = parents.get(id(item))
            directly_called = isinstance(parent, ast.Call) and parent.func is item
            if isinstance(item, ast.Name) and item.id in restricted_callables and not directly_called:
                return True
            if not isinstance(item, ast.Attribute):
                continue
            dotted_item = attribute_name(item)
            process_or_os = dotted_item is not None and dotted_item.startswith(("subprocess.", "os."))
            if (process_or_os or item.attr in filesystem_mutations) \
                    and not directly_called:
                return True
        return False

    def target_identifiers(nodes: list[ast.AST]) -> list[str]:
        return [item.id for node in nodes for item in ast.walk(node)
                if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Store)]

    bindings: list[tuple[list[ast.AST], ast.AST]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            bindings.append((list(node.targets), node.value))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            bindings.append(([node.target], node.value))
        elif isinstance(node, ast.NamedExpr):
            bindings.append(([node.target], node.value))
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            bindings.append(([node.target], node.iter))
        elif isinstance(node, ast.comprehension):
            bindings.append(([node.target], node.iter))

    def path_transport(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id in path_variables or node.id.endswith("_path")
        if isinstance(node, ast.Call):
            return attribute_name(node.func) == "pathlib.Path"
        return any(path_transport(child) for child in ast.iter_child_nodes(node))

    changed = True
    while changed:
        before = (len(path_variables), len(callable_aliases), len(module_escape_aliases))
        for targets, value in bindings:
            target_names = target_identifiers(targets)
            dotted = attribute_name(value)
            if module_transport(value):
                module_escape_aliases.update(target_names)
            if path_transport(value):
                path_variables.update(target_names)
            if restricted_rhs(value, restricted_callables) or transported_sensitive_callable(value):
                callable_aliases.update(target_names)
            if dotted is not None and dotted.startswith(("subprocess.", "os.")):
                callable_aliases.update(target_names)
            if isinstance(value, ast.Attribute):
                path_bound = (
                    isinstance(value.value, ast.Call)
                    and attribute_name(value.value.func) == "pathlib.Path"
                ) or (
                    isinstance(value.value, ast.Name)
                    and (value.value.id in path_variables or value.value.id.endswith("_path"))
                )
                if value.attr in filesystem_mutations and path_bound:
                    callable_aliases.update(target_names)
        changed = before != (len(path_variables), len(callable_aliases), len(module_escape_aliases))
    require(not callable_aliases, "E_SOURCE_POLICY_CALLABLE_ALIAS", repr(sorted(callable_aliases)))
    require(not module_escape_aliases, "E_SOURCE_POLICY_MODULE_ESCAPE_ALIAS",
            repr(sorted(module_escape_aliases)))

    def transported_value(node: ast.AST) -> bool:
        return (restricted_rhs(node, restricted_callables) or module_transport(node)
                or transported_sensitive_callable(node))

    definitions = [
        node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    for definition in definitions:
        defaults = [*definition.args.defaults, *(
            value for value in definition.args.kw_defaults if value is not None
        )]
        require(not any(transported_value(value) for value in defaults),
                "E_SOURCE_POLICY_DEFAULT_TRANSPORT", definition.name)
    for lambda_node in (node for node in ast.walk(tree) if isinstance(node, ast.Lambda)):
        defaults = [*lambda_node.args.defaults, *(
            value for value in lambda_node.args.kw_defaults if value is not None
        )]
        require(not any(transported_value(value) for value in defaults),
                "E_SOURCE_POLICY_DEFAULT_TRANSPORT", "lambda")
    for transfer in (node for node in ast.walk(tree)
                     if isinstance(node, (ast.Return, ast.Yield, ast.YieldFrom))
                     and node.value is not None):
        transfer_kind = "Return" if isinstance(transfer, ast.Return) \
            else "Yield" if isinstance(transfer, ast.Yield) else "YieldFrom"
        require(not transported_value(transfer.value), "E_SOURCE_POLICY_RETURN_TRANSPORT",
                transfer_kind)

    approved_definitions = {
        "expect_validation_error": ["code", "operation"],
        "expect_error": ["operation"],
    }
    for name, expected_arguments in approved_definitions.items():
        matches = [definition for definition in definitions if definition.name == name]
        exact = len(matches) == 1
        if exact:
            arguments = matches[0].args
            actual_arguments = [item.arg for item in arguments.args]
            exact = (not arguments.posonlyargs and actual_arguments == expected_arguments
                     and not arguments.kwonlyargs and arguments.vararg is None
                     and arguments.kwarg is None and not arguments.defaults
                     and not any(value is not None for value in arguments.kw_defaults))
        require(exact, "E_SOURCE_POLICY_APPROVED_DEF_SEAL", name)

    approved_parameter_calls = {
        ("lf_bytes", "raw.replace"),
        ("inspect_json_value", "value.items"),
        ("strict_load_bytes", "raw.decode"),
        ("parse_name_status", "raw.decode"),
        ("validate_repository_record", "snapshot.get"),
        ("validate_predecessor_document", "document.get"),
        ("exact_line", "text.splitlines"),
        ("unique_prefixed_line", "text.splitlines"),
        ("validate_plan_text", "text.find"),
        ("validate_plan_text", "text.count"),
        ("exact_line_count", "text.splitlines"),
        ("assert_payload", "document.get"),
        ("validate_activation_authority", "authority.get"),
        ("expect_validation_error", "operation"),
        ("expect_error", "operation"),
        ("run_authority_controls", "document.get"),
        ("validate_change_record", "status.values"),
        ("validate_payload_source_hashes", "document.get"),
        ("run_controls", "document.get"),
        ("path_transport", "node.id.endswith"),
    }
    for definition in definitions:
        parameters = {
            argument.arg for argument in (
                [*definition.args.posonlyargs, *definition.args.args, *definition.args.kwonlyargs]
            )
        }
        for item in ast.walk(definition):
            if not isinstance(item, ast.Call):
                continue
            called_name = item.func.id if isinstance(item.func, ast.Name) else attribute_name(item.func)
            called_parameter = called_name is not None and called_name.split(".", 1)[0] in parameters
            if called_parameter:
                require((definition.name, called_name) in approved_parameter_calls,
                        "E_SOURCE_POLICY_PARAMETER_CALL",
                        f"{definition.name}:{called_name}")
    subprocess_sites = 0
    filesystem_sites = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            require(node.id != "__builtins__", "E_SOURCE_POLICY_BUILTINS", node.id)
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            exact_super_init = (
                node.attr == "__init__" and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name) and node.value.func.id == "super"
            )
            require(exact_super_init, "E_SOURCE_POLICY_DUNDER", node.attr)
        if not isinstance(node, ast.Call):
            continue
        owner = function_for.get(id(node), "<module>")
        if not (isinstance(node.func, ast.Name) and node.func.id == "isinstance"):
            caller_name = attribute_name(node.func)
            direct_sealed_caller = caller_name is not None and len(caller_name.split(".")) == 2 \
                and caller_name.split(".", 1)[0] in sealed_modules
            for argument in [*node.args, *(keyword.value for keyword in node.keywords)]:
                dangerous_transport = (
                    restricted_rhs(argument, restricted_callables)
                    or (module_transport(argument) and not direct_sealed_caller)
                    or transported_sensitive_callable(argument)
                )
                require(not dangerous_transport, "E_SOURCE_POLICY_ARGUMENT_TRANSPORT",
                        f"{owner}:{node.lineno}")
        dotted_call = attribute_name(node.func)
        sealed_roots = {
            item.id for item in ast.walk(node.func)
            if isinstance(item, ast.Name) and item.id in sealed_modules
        }
        if sealed_roots:
            direct_module_call = dotted_call is not None and len(dotted_call.split(".")) == 2
            direct_path_method = (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Call)
                and attribute_name(node.func.value.func) == "pathlib.Path"
            )
            approved_result_transform = (
                isinstance(node.func, ast.Attribute)
                and (
                    (node.func.attr == "hexdigest" and isinstance(node.func.value, ast.Call)
                     and attribute_name(node.func.value.func) == "hashlib.sha256")
                    or (node.func.attr == "encode" and any(
                        isinstance(item, ast.Call) and attribute_name(item.func) == "json.dumps"
                        for item in ast.walk(node.func.value)
                    ))
                )
            )
            require(direct_module_call or direct_path_method or approved_result_transform,
                    "E_SOURCE_POLICY_MODULE_TRAVERSAL", repr(sorted(sealed_roots)))
        if isinstance(node.func, ast.Name):
            require(node.func.id not in {
                "exec", "eval", "compile", "__import__", "open", "getattr", "globals", "locals",
            }, "E_SOURCE_POLICY_DYNAMIC", node.func.id)
            require(node.func.id not in callable_aliases, "E_SOURCE_POLICY_INDIRECT_CALL", node.func.id)
            require(node.func.id not in module_escape_aliases,
                    "E_SOURCE_POLICY_MODULE_TRAVERSAL", node.func.id)
        elif not isinstance(node.func, ast.Attribute):
            require(False, "E_SOURCE_POLICY_INDIRECT_CALL", ast.dump(node.func, include_attributes=False))
        if isinstance(node.func, ast.Attribute):
            dotted = attribute_name(node.func)
            if dotted == "subprocess.run":
                subprocess_sites += 1
                require(owner == "run_git", "E_SOURCE_POLICY_SUBPROCESS_OWNER", owner)
                keywords = {keyword.arg: keyword.value for keyword in node.keywords}
                require(isinstance(keywords.get("shell"), ast.Constant)
                        and keywords["shell"].value is False,
                        "E_SOURCE_POLICY_SHELL", owner)
            elif dotted is not None and dotted.startswith("subprocess."):
                require(False, "E_SOURCE_POLICY_PROCESS", dotted)
            if dotted == "os.replace":
                filesystem_sites += 1
                require(owner == "atomic_collect", "E_SOURCE_POLICY_FILESYSTEM_OWNER", owner)
            elif dotted is not None and dotted.startswith("os."):
                require(False, "E_SOURCE_POLICY_OS", dotted)
            path_call = (
                isinstance(node.func.value, ast.Call)
                and attribute_name(node.func.value.func) == "pathlib.Path"
            ) or (
                isinstance(node.func.value, ast.Name) and node.func.value.id in path_variables
            ) or (
                isinstance(node.func.value, ast.Name) and node.func.value.id.endswith("_path")
            )
            mutation = node.func.attr in filesystem_mutations
            if mutation:
                scalar_replace = node.func.attr == "replace" and (
                    dotted == "os.replace"
                    or owner == "lf_bytes"
                    or (owner == "validate_source_policy" and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "source")
                    or (owner == "run_human_controls" and isinstance(node.func.value, ast.Subscript))
                    or (owner == "run_gate_controls" and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "plan")
                )
                if scalar_replace:
                    pass
                else:
                    filesystem_sites += 1
                    require(path_call and node.func.attr in {"write_bytes", "unlink"}
                            and owner == "atomic_collect",
                            "E_SOURCE_POLICY_FILESYSTEM_OWNER", f"{owner}:{node.func.attr}")
            super_init = (
                node.func.attr == "__init__"
                and isinstance(node.func.value, ast.Call)
                and isinstance(node.func.value.func, ast.Name)
                and node.func.value.func.id == "super"
            )
            require(not node.func.attr.startswith("__") or super_init,
                    "E_SOURCE_POLICY_DUNDER", node.func.attr)
    require(subprocess_sites == 1, "E_SOURCE_POLICY_SUBPROCESS_COUNT", str(subprocess_sites))
    require(filesystem_sites == 3, "E_SOURCE_POLICY_FILESYSTEM_COUNT", str(filesystem_sites))
    return {"subprocess_run_sites": subprocess_sites, "filesystem_mutation_sites": filesystem_sites}


def validate_source_policy() -> dict[str, int]:
    source = VALIDATOR.read_text(encoding="utf-8")
    metrics = validate_source_policy_text(source, VALIDATOR_PATH)
    probes = [
        (source + "\nfrom subprocess import run as hidden_run\nhidden_run(['git'])\n", "E_SOURCE_POLICY_IMPORT_SEAL"),
        (source + "\npathlib.Path('x').write_text('x')\n", "E_SOURCE_POLICY_FILESYSTEM_OWNER"),
        (source + "\nos.system('echo x')\n", "E_SOURCE_POLICY_OS"),
        (source + "\nhidden=eval\nhidden('1')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nsubprocess.Popen(['git'])\n", "E_SOURCE_POLICY_PROCESS"),
        (source + "\nsubprocess.call(['git'])\n", "E_SOURCE_POLICY_PROCESS"),
        (source + "\npathlib.Path('x').rename('y')\n", "E_SOURCE_POLICY_FILESYSTEM_OWNER"),
        (source + "\npathlib.Path('x').replace('y')\n", "E_SOURCE_POLICY_FILESYSTEM_OWNER"),
        (source + "\npathlib.Path('x').touch()\n", "E_SOURCE_POLICY_FILESYSTEM_OWNER"),
        (source + "\npathlib.Path('x').mkdir()\n", "E_SOURCE_POLICY_FILESYSTEM_OWNER"),
        (source + "\npathlib.Path('x').open('w')\n", "E_SOURCE_POLICY_FILESYSTEM_OWNER"),
        (source + "\nos.remove('x')\n", "E_SOURCE_POLICY_OS"),
        (source + "\nos.rename('x','y')\n", "E_SOURCE_POLICY_OS"),
        (source + "\npathlib.os.system('echo x')\n", "E_SOURCE_POLICY_MODULE_TRAVERSAL"),
        (source + "\npathlib.sys.modules['os'].system('echo x')\n", "E_SOURCE_POLICY_MODULE_TRAVERSAL"),
        (source + "\nshadow_os=os\nshadow_os.system('echo x')\n", "E_SOURCE_POLICY_MODULE_ESCAPE_ALIAS"),
        (source + "\nshadow_sp=subprocess\nshadow_sp.Popen(['git'])\n", "E_SOURCE_POLICY_MODULE_ESCAPE_ALIAS"),
        (source + "\nshadow_eval=[eval][0]\nshadow_eval('1')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nshadow_open=[open][0]\nshadow_open('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\n(lambda:0).__globals__['os'].system('echo x')\n", "E_SOURCE_POLICY_DUNDER"),
        (source + "\n(hidden,)=(eval,)\nhidden('1')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nhidden=__builtins__.eval\nhidden('1')\n", "E_SOURCE_POLICY_BUILTINS"),
        (source + "\nhidden=__builtins__.open\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\np=pathlib.Path('x')\nhidden=p.write_text\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nhidden=pathlib.Path('x').write_text\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nhidden=os.remove\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nhidden=subprocess.Popen\nhidden(['git'])\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nhidden=[pathlib.Path('x').write_text][0]\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\np=pathlib.Path('x')\nhidden=(p.write_text,)[0]\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nfor hidden in [eval]:\n    hidden('1')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\n[hidden('1') for hidden in [eval]]\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nif (hidden:=eval): pass\nhidden('1')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nif (hidden:=pathlib.Path('x').write_text): pass\nhidden('x')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\nfor hidden in [os]:\n    hidden.system('echo x')\n", "E_SOURCE_POLICY_MODULE_ESCAPE_ALIAS"),
        (source + "\n[hidden.Popen(['git']) for hidden in [subprocess]]\n", "E_SOURCE_POLICY_MODULE_ESCAPE_ALIAS"),
        (source + "\nasync def bad_async():\n    async for hidden in [eval]:\n        hidden('1')\n", "E_SOURCE_POLICY_CALLABLE_ALIAS"),
        (source + "\ndef invoke(fn): return fn('1')\ninvoke(eval)\n", "E_SOURCE_POLICY_PARAMETER_CALL"),
        (source + "\ndef invoke(fn): return fn(['git'])\ninvoke(subprocess.Popen)\n", "E_SOURCE_POLICY_PARAMETER_CALL"),
        (source + "\ndef invoke(mod): mod.system('echo x')\ninvoke(os)\n", "E_SOURCE_POLICY_PARAMETER_CALL"),
        (source + "\np=pathlib.Path('x')\ndef invoke(fn): return fn('x')\ninvoke(p.write_text)\n", "E_SOURCE_POLICY_PARAMETER_CALL"),
        (source + "\ndef expect_error(operation=eval): return operation('1')\nexpect_error()\n", "E_SOURCE_POLICY_DEFAULT_TRANSPORT"),
        (source + "\ndef bad_default(mod=os): return mod\n", "E_SOURCE_POLICY_DEFAULT_TRANSPORT"),
        (source + "\ndef bad_default(fn=pathlib.Path('x').write_text): return fn\n", "E_SOURCE_POLICY_DEFAULT_TRANSPORT"),
        (source + "\ndef supplier(): return eval\nhidden=supplier()\nhidden('1')\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef supplier(): return os\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef supplier(): return pathlib.Path('x').write_text\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef supplier():\n    yield eval\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef supplier():\n    yield os\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef supplier():\n    yield pathlib.Path('x').write_text\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef supplier():\n    yield from [eval]\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef expect_error(operation): return 0\n", "E_SOURCE_POLICY_APPROVED_DEF_SEAL"),
        (source + "\ndef Path(x): return pathlib.Path(x)\ndef supplier(): return Path('x').write_text\nhidden=supplier()\nhidden('x')\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef factory(x): return pathlib.Path(x)\ndef supplier(): return factory('x').write_text\nhidden=supplier()\nhidden('x')\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef Path(x): return pathlib.Path(x)\ndef supplier():\n    yield Path('x').write_text\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef factory(x): return pathlib.Path(x)\ndef supplier():\n    yield factory('x').write_text\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source + "\ndef factory(x): return pathlib.Path(x)\ndef supplier():\n    yield from [factory('x').write_text]\n", "E_SOURCE_POLICY_RETURN_TRANSPORT"),
        (source.replace("shell=False", "shell=True", 1), "E_SOURCE_POLICY_SHELL"),
        (source + "\ndef bad():\n    subprocess.run(['git', 'status'], shell=False)\n", "E_SOURCE_POLICY_SUBPROCESS_OWNER"),
    ]
    for index, (probe, code) in enumerate(probes, start=1):
        expect_validation_error(code, lambda probe=probe, index=index: validate_source_policy_text(
            probe, f"negative-{index}.py"
        ))
    git_probes = [
        ("E_GIT_DIFF_SHAPE", lambda: run_git(["diff", "--output=payload", "HEAD"])),
        ("E_GIT_BRANCH_SHAPE", lambda: run_git(["branch", "created-by-probe"])),
        ("E_GIT_BRANCH_SHAPE", lambda: run_git(["branch", "-D", "main"])),
        ("E_GIT_REMOTE_SHAPE", lambda: run_git(["remote", "set-url", "origin", "x"])),
    ]
    for code, operation in git_probes:
        expect_validation_error(code, operation)
    metrics["negative_cases"] = len(probes)
    metrics["git_argv_negative_cases"] = len(git_probes)
    return metrics


def manifest_contract() -> dict[str, Any]:
    raw = read_lf(MANIFEST_PATH)
    document, nodes, scalars, depth = strict_load_bytes(raw, MANIFEST_PATH)
    entries = document.get("entries")
    require(type(entries) is list and len(entries) == 1520, "E_MANIFEST_ENTRIES")
    python_rows = [row for row in entries if row.get("extension") == "py"]
    by_blob: dict[str, dict[str, Any]] = {}
    for row in python_rows:
        blob = row.get("blob_sha")
        require(type(blob) is str and re.fullmatch(r"[0-9a-f]{40}", blob) is not None,
                "E_MANIFEST_BLOB", repr(blob))
        extent = row.get("extent")
        require(type(extent) is dict and type(extent.get("lines")) is int,
                "E_MANIFEST_LINES", str(row.get("path")))
        if blob in by_blob:
            require(by_blob[blob]["extent"]["lines"] == extent["lines"],
                    "E_MANIFEST_BLOB_LINE_CONFLICT", blob)
        else:
            by_blob[blob] = row
    roles = Counter(row.get("role") for row in python_rows)
    role_unique = {
        role: len({row["blob_sha"] for row in python_rows if row.get("role") == role})
        for role in ("code", "test", "demo", "result")
    }
    releases = sorted({row.get("version") for row in python_rows}, key=EXPECTED_RELEASES.index)
    golden = [row for row in entries if "golden" in row.get("path", "").lower()
              and row.get("extension") == "npz"]
    guide = [row for row in entries if "FITTING_GUIDE" in row.get("path", "").upper()]
    guide_by_blob: dict[str, dict[str, Any]] = {}
    for row in guide:
        guide_by_blob.setdefault(row["blob_sha"], row)
    result = {
        "manifest_path": MANIFEST_PATH,
        "manifest_sha256_lf": sha256(raw),
        "manifest_nodes": nodes,
        "manifest_scalars": scalars,
        "manifest_depth": depth,
        "python_occurrences": len(python_rows),
        "python_unique_blobs": len(by_blob),
        "python_unique_physical_lines": sum(row["extent"]["lines"] for row in by_blob.values()),
        "release_count": len(releases),
        "releases": releases,
        "roles": {
            role: {"occurrences": roles[role], "unique_blobs": role_unique[role]}
            for role in ("code", "test", "demo", "result")
        },
        "golden": {
            "occurrences": len(golden),
            "unique_blobs": len({row["blob_sha"] for row in golden}),
        },
        "fitting_guide": {
            "occurrences": len(guide),
            "unique_blobs": len(guide_by_blob),
            "unique_physical_lines": sum(row["extent"]["lines"] for row in guide_by_blob.values()),
        },
    }
    require(result["python_occurrences"] == 129, "E_PYTHON_OCCURRENCES")
    require(result["python_unique_blobs"] == 84, "E_PYTHON_BLOBS")
    require(result["python_unique_physical_lines"] == 29952, "E_PYTHON_LINES")
    require(result["release_count"] == 20 and releases == EXPECTED_RELEASES, "E_RELEASES")
    require(result["roles"] == {
        "code": {"occurrences": 20, "unique_blobs": 15},
        "test": {"occurrences": 44, "unique_blobs": 29},
        "demo": {"occurrences": 30, "unique_blobs": 26},
        "result": {"occurrences": 35, "unique_blobs": 14},
    }, "E_ROLE_COUNTS", repr(result["roles"]))
    require(result["golden"] == {"occurrences": 8, "unique_blobs": 2}, "E_GOLDEN")
    require(result["fitting_guide"] == {
        "occurrences": 20, "unique_blobs": 8, "unique_physical_lines": 854,
    }, "E_FITTING_GUIDE")
    return result


def validate_predecessor_document(document: dict[str, Any]) -> None:
    require(document.get("schema_version") == "phase066-step81.2-final-validation-v1",
            "E_PREDECESSOR_SCHEMA")
    require(document.get("phase") == 66 and document.get("step") == "81.2",
            "E_PREDECESSOR_PHASE")
    require(document.get("gate") == "CONDITIONAL_P066", "E_PREDECESSOR_GATE")
    require(document.get("persistence_terminal") == "PASS_P066_STEP81_2_PERSISTENCE",
            "E_PREDECESSOR_TERMINAL")
    history = document.get("canonical_history_contract")
    require(type(history) is dict, "E_PREDECESSOR_HISTORY")
    require(history == {
        "collector_only_fresh_historical_replay": 14,
        "ordinary_fresh_historical_replay": 0,
        "persistence": 7,
        "precommit": 7,
        "total": 14,
        "units": ["ACTIVATION", "STEP76", "STEP77", "STEP78", "STEP79", "STEP80", "STEP81_1"],
    }, "E_PREDECESSOR_HISTORY", repr(history))
    authority = document.get("authority_ceiling")
    require(authority == {
        "external_authority": False,
        "held_out_authority": False,
        "main_scholarly_body_modified": False,
        "material_authority": False,
        "original_full_precision_optimizer_state": "GROUND_NOT_FOUND",
        "raw_exact_binding": "GROUND_NOT_FOUND",
        "ref7_original_full_text": "GROUND_NOT_FOUND",
        "stale_pdf_build_closed": False,
    }, "E_PREDECESSOR_AUTHORITY", repr(authority))
    repository = document.get("repository_contract")
    require(type(repository) is dict, "E_PREDECESSOR_REPOSITORY")
    require(repository.get("exact_paths") == list(PREDECESSOR_FINAL_STATUS)
            and repository.get("exact_path_count") == 8,
            "E_PREDECESSOR_EXACT_PATHS")
    require(repository.get("active_branch") == ACTIVE_BRANCH
            and repository.get("upstream") == UPSTREAM
            and repository.get("origin_url") == ORIGIN_URL
            and repository.get("protected_tip") == PROTECTED_TIP
            and repository.get("main_tip") == MAIN_TIP
            and repository.get("claude_changed") is False
            and repository.get("production_source_changed") is False,
            "E_PREDECESSOR_REPOSITORY")


def predecessor_contract() -> dict[str, Any]:
    json_raw = read_lf(PREDECESSOR_JSON_PATH)
    validator_raw = read_lf(PREDECESSOR_VALIDATOR_PATH)
    require(sha256(json_raw) == PREDECESSOR_JSON_SHA256, "E_PREDECESSOR_JSON_HASH")
    require(sha256(validator_raw) == PREDECESSOR_VALIDATOR_SHA256, "E_PREDECESSOR_VALIDATOR_HASH")
    document, nodes, scalars, depth = strict_load_bytes(json_raw, PREDECESSOR_JSON_PATH)
    require(document.get("semantic_sha256") == PREDECESSOR_SEMANTIC_SHA256,
            "E_PREDECESSOR_SEMANTIC")
    semantic_projection = copy.deepcopy(document)
    semantic_projection.pop("semantic_sha256", None)
    require(sha256(json.dumps(
        semantic_projection, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")) == PREDECESSOR_SEMANTIC_SHA256,
            "E_PREDECESSOR_SEMANTIC_RECONSTRUCTION")
    validate_predecessor_document(document)
    require(git_text(["rev-parse", EXPECTED_PARENT]) == EXPECTED_PARENT, "E_PREDECESSOR_COMMIT")
    parents = git_text(["show", "-s", "--format=%P", EXPECTED_PARENT]).split()
    require(parents == [EXPECTED_PARENT_PARENT], "E_PREDECESSOR_PARENT", repr(parents))
    require(git_text(["show", "-s", "--format=%s", EXPECTED_PARENT]) == EXPECTED_PARENT_SUBJECT,
            "E_PREDECESSOR_SUBJECT")
    require(git_blob(EXPECTED_PARENT, PREDECESSOR_JSON_PATH) == json_raw, "E_PREDECESSOR_JSON_COMMITTED")
    require(git_blob(EXPECTED_PARENT, PREDECESSOR_VALIDATOR_PATH) == validator_raw,
            "E_PREDECESSOR_VALIDATOR_COMMITTED")
    predecessor_paths = list(PREDECESSOR_FINAL_STATUS)
    predecessor_status = parse_name_status(run_git([
        "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-z", "-r",
        EXPECTED_PARENT,
    ]).stdout)
    require(predecessor_status == PREDECESSOR_FINAL_STATUS,
            "E_PREDECESSOR_COMMIT_PATHS", repr(predecessor_status))
    entries = tree_entries(EXPECTED_PARENT, predecessor_paths)
    require({path: row["mode"] for path, row in entries.items()}
            == {path: "100644" for path in predecessor_paths}, "E_PREDECESSOR_COMMIT_MODES")
    evidence_rows = document.get("output_evidence")
    require(type(evidence_rows) is list and len(evidence_rows) == 7, "E_PREDECESSOR_OUTPUT_EVIDENCE")
    evidence = {row.get("path"): row for row in evidence_rows if type(row) is dict}
    require(len(evidence) == 7, "E_PREDECESSOR_OUTPUT_EVIDENCE")
    blobs = []
    for path in predecessor_paths:
        raw = git_blob(EXPECTED_PARENT, path)
        record = {
            "path": path,
            "status": PREDECESSOR_FINAL_STATUS[path],
            "mode": entries[path]["mode"],
            "blob_oid": entries[path]["blob_oid"],
            "bytes": len(raw),
            "raw_sha256": sha256(raw),
        }
        if path == PREDECESSOR_JSON_PATH:
            require(record["raw_sha256"] == PREDECESSOR_JSON_SHA256,
                    "E_PREDECESSOR_JSON_COMMITTED_HASH")
        else:
            expected = evidence.get(path)
            require(type(expected) is dict
                    and expected.get("bytes") == len(raw)
                    and expected.get("raw_sha256") == sha256(raw),
                    "E_PREDECESSOR_BLOB_EVIDENCE", path)
        blobs.append(record)
    require(run_git(["diff", "--quiet", EXPECTED_PARENT_PARENT, EXPECTED_PARENT, "--", "Claude"],
                    check=False).returncode == 0, "E_PREDECESSOR_CLAUDE_DIFF")
    entry_snapshot = repository_snapshot(EXPECTED_PARENT)
    terminal_snapshot = repository_snapshot(EXPECTED_PARENT)
    validate_terminal_seal(
        entry_snapshot, terminal_snapshot, "E_PREDECESSOR_REPOSITORY_TOCTOU"
    )
    return {
        "commit": EXPECTED_PARENT,
        "parent": EXPECTED_PARENT_PARENT,
        "subject": EXPECTED_PARENT_SUBJECT,
        "gate": "CONDITIONAL_P066",
        "persistence_terminal": document["persistence_terminal"],
        "json_path": PREDECESSOR_JSON_PATH,
        "json_sha256_lf": PREDECESSOR_JSON_SHA256,
        "semantic_sha256": PREDECESSOR_SEMANTIC_SHA256,
        "validator_path": PREDECESSOR_VALIDATOR_PATH,
        "validator_sha256_lf": PREDECESSOR_VALIDATOR_SHA256,
        "history_contract": document["canonical_history_contract"],
        "authority_ceiling": document["authority_ceiling"],
        "exact_status": PREDECESSOR_FINAL_STATUS,
        "committed_blobs": blobs,
        "repository_entry": entry_snapshot,
        "repository_terminal": terminal_snapshot,
        "single_parent_verified": True,
        "claude_diff_zero": True,
        "json_nodes": nodes,
        "json_scalars": scalars,
        "json_depth": depth,
    }


def supplemental_fit_contract() -> dict[str, Any]:
    rows = []
    for path, role, routed in SUPPLEMENTAL_FIT_INPUTS:
        identities = []
        for label, commit in (("baseline", BASELINE), ("containing", EXPECTED_PARENT)):
            entries = tree_entries(commit, [path])
            require(set(entries) == {path}, "E_SUPPLEMENTAL_TREE", f"{label}:{path}")
            raw = git_blob(commit, path)
            identities.append({
                "commit_role": label,
                "commit": commit,
                "tree_path": path,
                "mode": entries[path]["mode"],
                "blob_oid": entries[path]["blob_oid"],
                "bytes": len(raw),
                "raw_sha256": sha256(raw),
            })
        require(identities[0]["blob_oid"] == identities[1]["blob_oid"]
                and identities[0]["mode"] == identities[1]["mode"],
                "E_SUPPLEMENTAL_IDENTITY_DRIFT", path)
        rows.append({
            "path": path,
            "bounded_role": role,
            "phase080_saved_profile_route": routed,
            "canonical_baseline_promoted": False,
            "git_identities": identities,
        })
    require(len(rows) == 10 and sum(row["phase080_saved_profile_route"] for row in rows) == 3,
            "E_SUPPLEMENTAL_COUNTS")
    return {"count": len(rows), "phase080_route_count": 3, "rows": rows}


def owner_contract() -> dict[str, Any]:
    raw = read_lf(CARRY_PATH)
    document, nodes, scalars, depth = strict_load_bytes(raw, CARRY_PATH)
    rows = document.get("active_obligations")
    require(type(rows) is list, "E_CARRY_ROWS")
    selected = [row for row in rows if row.get("canonical_owner") == "P067-CODE-HISTORY"]
    identities = sorted((row.get("obligation_id"), row.get("origin_identity")) for row in selected)
    require(identities == sorted(EXPECTED_OWNERS), "E_P067_OWNER_IDENTITIES", repr(identities))
    require(all(row.get("target_phase") == 67 and row.get("state") == "OPEN_CARRY"
                and row.get("external_authority_promoted") is False
                and type(row.get("acceptance_criterion")) is str
                for row in selected), "E_P067_OWNER_SCHEMA")
    return {
        "path": CARRY_PATH,
        "sha256_lf": sha256(raw),
        "owner": "P067-CODE-HISTORY",
        "active_count": len(selected),
        "identities": [
            {"obligation_id": obligation, "origin_identity": origin}
            for obligation, origin in sorted(EXPECTED_OWNERS)
        ],
        "external_authority_promoted": False,
        "nodes": nodes,
        "scalars": scalars,
        "depth": depth,
    }


def exact_line(text: str, line: str, code: str) -> None:
    require(text.splitlines().count(line) == 1, code, line)


def unique_prefixed_line(text: str, prefix: str, code: str) -> str:
    rows = [line for line in text.splitlines() if line.startswith(prefix)]
    require(len(rows) == 1, code, f"{prefix}:{len(rows)}")
    return rows[0]


def validate_control_documents(documents: dict[str, str]) -> None:
    result = documents[RESULT_PATH]
    for line in (
        "Status: `PASS_PENDING_PERSISTENCE`",
        "Selected Gate: `PASS_P067_PLAN_ACTIVATION`",
        "Persistence terminal: `PASS_P067_PLAN_ACTIVATION_PERSISTENCE`",
        "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        f"Expected parent: `{EXPECTED_PARENT}`",
        f"Expected subject: `{EXPECTED_SUBJECT}`",
    ):
        exact_line(result, line, "E_CONTROL_RESULT_SCHEMA")
    exact_line(result, "- Known Ref. 7, original-optimizer, held-out/external/material, and stale-PDF debt",
               "E_CONTROL_GATE_CEILING")
    exact_line(result, "  is an authority ceiling/open carry, not a PASS-versus-CONDITIONAL determinant.",
               "E_CONTROL_GATE_CEILING")

    parent = documents[PARENT_LEDGER_PATH]
    p66 = unique_prefixed_line(parent, "| 066 |", "E_CONTROL_PARENT_P066_ROW")
    p67 = unique_prefixed_line(parent, "| 067 |", "E_CONTROL_PARENT_P067_ROW")
    require(all(token in p66 for token in (
        EXPECTED_PARENT, EXPECTED_PARENT_PARENT, EXPECTED_PARENT_SUBJECT,
        "PASS_P066_STEP81_2_PERSISTENCE", "CONDITIONAL_P066", "14/14", "0/14",
    )), "E_CONTROL_PARENT_P066_SCHEMA")
    require(all(token in p67 for token in (
        PLAN_PATH, RESULT_PATH, OUTPUT_PATH, VALIDATOR_PATH, "PASS_PENDING_PERSISTENCE",
        GATE, EXPECTED_PARENT, "PENDING_AT_PRECOMMIT_BY_DESIGN", PERSISTENCE,
    )), "E_CONTROL_PARENT_P067_SCHEMA")

    active = documents[ACTIVE_LEDGER_PATH]
    a66 = unique_prefixed_line(active, "| 066 |", "E_CONTROL_ACTIVE_P066_ROW")
    a67 = unique_prefixed_line(active, "| 067 |", "E_CONTROL_ACTIVE_P067_ROW")
    require(all(token in a66 for token in (
        EXPECTED_PARENT, EXPECTED_PARENT_PARENT, EXPECTED_PARENT_SUBJECT,
        "PASS_P066_STEP81_2_PERSISTENCE", "CONDITIONAL_P066", "14/14", "0/14",
    )), "E_CONTROL_ACTIVE_P066_SCHEMA")
    require(all(token in a67 for token in (
        PLAN_PATH, RESULT_PATH, OUTPUT_PATH, VALIDATOR_PATH, "PASS_PENDING_PERSISTENCE",
        GATE, EXPECTED_PARENT, "PENDING_AT_PRECOMMIT_BY_DESIGN", PERSISTENCE,
        "PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067",
    )), "E_CONTROL_ACTIVE_P067_SCHEMA")
    unique_prefixed_line(active, "| Phase 066 Step 81.2 |", "E_CONTROL_ACTIVE_P066_EXECUTION")
    activation = unique_prefixed_line(
        active, "| Phase 067 plan activation |", "E_CONTROL_ACTIVE_P067_EXECUTION"
    )
    require(all(token in activation for token in (
        "PASS_P067_PLAN_ACTIVATION", "A/A/A/A/M/M/M", EXPECTED_PARENT,
        EXPECTED_SUBJECT, "14/14", "0/14", PERSISTENCE,
    )), "E_CONTROL_ACTIVE_P067_EXECUTION_SCHEMA")
    exact_line(active, "## Next Exact Step", "E_CONTROL_ACTIVE_NEXT_HEADING")

    handover = documents[HANDOVER_PATH]
    exact_line(
        handover,
        f"5. 활성 Phase 067 plan: `{PLAN_PATH}`",
        "E_CONTROL_HANDOVER_TOP_PLAN",
    )
    exact_line(
        handover,
        "19. 현재 Phase 상태: Phase 067 plan activation selected `PASS_P067_PLAN_ACTIVATION`; `PASS_PENDING_PERSISTENCE`; cumulative Step 82 blocked",
        "E_CONTROL_HANDOVER_TOP_STATUS",
    )
    exact_line(handover, "## Exact Next Action", "E_CONTROL_HANDOVER_NEXT_HEADING")
    next_lines = handover.split("## Exact Next Action", 1)[1].split("## Hard-stop Reminder", 1)[0]
    require(next_lines.count(EXPECTED_SUBJECT) == 1
            and next_lines.count(EXPECTED_PARENT) == 1
            and next_lines.count(PERSISTENCE) == 1
            and "Begin Step 82 only after" in next_lines,
            "E_CONTROL_HANDOVER_NEXT_SCHEMA")
    require("Run Step 81" not in next_lines and "Begin Step 81" not in next_lines,
            "E_CONTROL_HANDOVER_STALE_NEXT")


def control_contract() -> dict[str, Any]:
    records = []
    documents = {}
    for path, tokens in CONTROL_TOKENS.items():
        raw = read_lf(path)
        text = raw.decode("utf-8", errors="strict")
        missing = [token for token in tokens if token not in text]
        require(not missing, "E_CONTROL_TOKEN", f"{path}:{missing}")
        records.append({
            "path": path,
            "lines": line_count(raw),
            "sha256_lf": sha256(raw),
        })
        documents[path] = text
    validate_control_documents(documents)
    return {
        "count": len(records),
        "records": records,
        "result_first": True,
        "validation_json_last": True,
        "precommit_record_state": True,
    }


def validate_plan_text(text: str) -> dict[str, Any]:
    raw = read_lf(PLAN_PATH)
    positions = [text.find(heading) for heading in REQUIRED_HEADINGS]
    require(all(position >= 0 for position in positions), "E_PLAN_HEADING_MISSING")
    require(positions == sorted(positions), "E_PLAN_HEADING_ORDER")
    require(all(text.count(heading) == 1 for heading in REQUIRED_HEADINGS),
            "E_PLAN_HEADING_UNIQUE")
    missing = [token for token in REQUIRED_PLAN_TOKENS if token not in text]
    require(not missing, "E_PLAN_TOKEN", repr(missing))
    output_records = []
    for index, step in enumerate(EXPECTED_STEPS):
        matches = list(re.finditer(rf"^### Step {re.escape(step)} —", text, re.MULTILINE))
        require(len(matches) == 1, "E_PLAN_STEP", step)
        start = matches[0].start()
        next_start = len(text)
        if index + 1 < len(EXPECTED_STEPS):
            next_match = re.search(
                rf"^### Step {re.escape(EXPECTED_STEPS[index + 1])} —",
                text[matches[0].end():], re.MULTILINE,
            )
            require(next_match is not None, "E_PLAN_STEP", EXPECTED_STEPS[index + 1])
            next_start = matches[0].end() + next_match.start()
        section = text[start:next_start]
        expected_paths = STEP_OUTPUTS[step]
        word = "seven" if len(expected_paths) == 7 else "eight"
        exact_line(section, f"**Exact-{word} outputs:**", "E_PLAN_OUTPUT_LABEL")
        paths = re.findall(r"^\d+\. `([^`]+)`$", section, re.MULTILINE)
        require(paths == expected_paths and len(set(paths)) == len(paths),
                "E_PLAN_OUTPUT_PATHS", f"{step}:{paths!r}")
        status = "/".join("M" if path in RECOVERY_PATHS else "A" for path in expected_paths)
        exact_line(section, f"Required status in this order: `{status}`.", "E_PLAN_OUTPUT_STATUS")
        require(exact_line_count(section, "Commit subject:") == 1,
                "E_PLAN_OUTPUT_SUBJECT", step)
        require(exact_line_count(section, "Required terminal:") == 1,
                "E_PLAN_OUTPUT_TERMINAL", step)
        output_records.append({"step": step, "count": len(paths), "paths": paths, "status": status})
    require(text.count("### `PASS_P067_CODE_HISTORY`") == 1, "E_PLAN_GATE_PASS")
    require(text.count("### `CONDITIONAL_P067`") == 1, "E_PLAN_GATE_CONDITIONAL")
    require(text.count("### `FAIL_P067`") == 1, "E_PLAN_GATE_FAIL")
    require("Step 82는 `PASS_P067_PLAN_ACTIVATION_PERSISTENCE`" in text,
            "E_PLAN_FIRST_STEP_BLOCK")
    step82 = next(row for row in output_records if row["step"] == "82")
    require(all(token in text for token in (
        "first introducing commit", "touch commits", "rename/copy classification",
        "commit/tree/blob/mode/parent/time/subject", "contract를 모두 포함",
        "parent tree", "current tree", "ambiguous relation을 추정하지 않는다",
    )), "E_PLAN_GENEALOGY_CONTRACT")
    require(step82["count"] == 8, "E_PLAN_GENEALOGY_OUTPUT")
    table_paths = re.findall(
        r"^\| `(Claude/results/(?:comp_v24|comp_v26_data)/[^`]+)` \|", text, re.MULTILINE
    )
    require(table_paths == [path for path, _, _ in SUPPLEMENTAL_FIT_INPUTS],
            "E_PLAN_SUPPLEMENTAL_PATHS", repr(table_paths))
    require(all(token in text for token in (
        "baseline/containing commit", "Git blob OID", "raw bytes SHA-256",
        "comparison/saved-route evidence일 뿐 canonical baseline", "추정하지 않는다",
    )), "E_PLAN_SUPPLEMENTAL_IDENTITY")
    require(all(token in text for token in (
        "Phase 067 gate 선택 determinant가 아니다",
        "required internal code-history/test/behavior cell",
        "GROUND_NOT_FOUND", "NOT_TESTED", "PARTIAL",
        "mutually exclusive and exhaustive", "authority ceiling/open carry",
        "Steps 82–90.1의 persistence", "current Step 90.2 precommit review",
        "Step 90.2 자신의 commit/push/persistence", "content Gate의 선행조건으로 순환 참조하지 않는다",
    )), "E_PLAN_GATE_EXCLUSIVITY")
    return {"output_contracts": output_records}


def exact_line_count(text: str, prefix: str) -> int:
    return sum(line.startswith(prefix) for line in text.splitlines())


def plan_contract() -> dict[str, Any]:
    raw = read_lf(PLAN_PATH)
    text = raw.decode("utf-8", errors="strict")
    structured = validate_plan_text(text)
    return {
        "path": PLAN_PATH,
        "lines": line_count(raw),
        "sha256_lf": sha256(raw),
        "heading_count": len(REQUIRED_HEADINGS),
        "steps": EXPECTED_STEPS,
        "first_step_released_only_after_persistence": True,
        "step_output_contracts": structured["output_contracts"],
    }


def build_payload() -> dict[str, Any]:
    plan = plan_contract()
    manifest = manifest_contract()
    predecessor = predecessor_contract()
    supplemental = supplemental_fit_contract()
    owners = owner_contract()
    controls = control_contract()
    validator_raw = read_lf(VALIDATOR_PATH)
    result_raw = read_lf(RESULT_PATH)
    predecessor_result_raw = read_lf(PREDECESSOR_RESULT_PATH)
    document: dict[str, Any] = {
        "schema_version": "P067-PLAN-ACTIVATION-1",
        "generated_date": "2026-09-01",
        "phase": "067",
        "status": "PASS_PENDING_PERSISTENCE",
        "gate": GATE,
        "persistence_terminal": PERSISTENCE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "exact_seven": {
            "count": 7,
            "paths": FINAL_PATHS,
            "status": [FINAL_STATUS[path] for path in FINAL_PATHS],
            "modes": ["100644"] * 7,
            "rename_allowed": False,
            "result_first": True,
            "validation_json_last": True,
        },
        "plan": plan,
        "inventory": manifest,
        "active_phase067_owners": owners,
        "predecessor": predecessor,
        "supplemental_fitting_inputs": supplemental,
        "historical_execution": {
            "canonical_reused": 14,
            "precommit_reused": 7,
            "persistence_reused": 7,
            "fresh_replay": 0,
            "historical_optimizer_fit_replayed": False,
        },
        "authority": {
            "activation_inventory_only": True,
            "canonical": False,
            "production_modified": False,
            "external_scientific": False,
            "heldout_validated": False,
            "material_validated": False,
            "optimizer_state_recovered": False,
            "ref7_original_full_text": "GROUND_NOT_FOUND",
            "stale_pdf_closed": False,
            "untested_code_assumed_working": False,
            "phase066_gate": "CONDITIONAL_P066",
        },
        "phase_gate_alternatives": EXPECTED_FINAL_GATES,
        "controls": controls,
        "human_evidence": {
            "result_path": RESULT_PATH,
            "result_sha256_lf": sha256(result_raw),
            "result_lines": line_count(result_raw),
            "predecessor_result_path": PREDECESSOR_RESULT_PATH,
            "predecessor_result_sha256_lf": sha256(predecessor_result_raw),
            "checks": 2,
        },
        "repository": {
            "branch": ACTIVE_BRANCH,
            "upstream": UPSTREAM,
            "baseline": BASELINE,
            "protected_branch": PROTECTED_BRANCH,
            "protected_tip": PROTECTED_TIP,
            "main_tip": MAIN_TIP,
            "local_main_absent": True,
            "claude_modification_allowed": False,
            "production_modification_allowed": False,
        },
        "validator_identity": {
            "path": VALIDATOR_PATH,
            "sha256_lf": sha256(validator_raw),
            "bytes_lf": len(validator_raw),
            "lines": line_count(validator_raw),
            "production_source_imported": False,
            "production_source_executed": False,
            "source_policy": "PASS",
            "subprocess_run_sites": 1,
        },
        "negative_contract": {},
        "determinism": {"reconstructions": 2, "byte_identical": True},
        "semantic_sha256": "",
    }
    document["semantic_sha256"] = semantic_hash(document)
    document["negative_contract"] = negative_contract_counts(document)
    document["semantic_sha256"] = semantic_hash(document)
    assert_payload(document)
    return document


def assert_payload(document: dict[str, Any]) -> None:
    require(document.get("schema_version") == "P067-PLAN-ACTIVATION-1", "E_SCHEMA")
    require(document.get("phase") == "067", "E_PHASE")
    require(document.get("status") == "PASS_PENDING_PERSISTENCE", "E_STATUS")
    require(document.get("gate") == GATE, "E_GATE")
    require(document.get("persistence_terminal") == PERSISTENCE, "E_PERSISTENCE")
    require(document.get("expected_parent") == EXPECTED_PARENT, "E_PARENT")
    require(document.get("expected_subject") == EXPECTED_SUBJECT, "E_SUBJECT")
    exact = document.get("exact_seven", {})
    require(exact.get("count") == 7, "E_EXACT_COUNT")
    require(exact.get("paths") == FINAL_PATHS, "E_EXACT_PATHS")
    require(exact.get("status") == [FINAL_STATUS[path] for path in FINAL_PATHS], "E_EXACT_STATUS")
    require(exact.get("rename_allowed") is False, "E_RENAME")
    require(exact.get("modes") == ["100644"] * 7, "E_MODES")
    inventory = document.get("inventory", {})
    require(inventory.get("python_occurrences") == 129, "E_PYTHON_OCCURRENCES")
    require(inventory.get("python_unique_blobs") == 84, "E_PYTHON_BLOBS")
    require(inventory.get("python_unique_physical_lines") == 29952, "E_PYTHON_LINES")
    require(inventory.get("release_count") == 20, "E_RELEASE_COUNT")
    roles = inventory.get("roles", {})
    require(roles.get("code") == {"occurrences": 20, "unique_blobs": 15}, "E_CODE_ROLE")
    require(roles.get("test") == {"occurrences": 44, "unique_blobs": 29}, "E_TEST_ROLE")
    require(roles.get("demo") == {"occurrences": 30, "unique_blobs": 26}, "E_DEMO_ROLE")
    require(roles.get("result") == {"occurrences": 35, "unique_blobs": 14}, "E_RESULT_ROLE")
    require(inventory.get("golden") == {"occurrences": 8, "unique_blobs": 2}, "E_GOLDEN")
    require(inventory.get("fitting_guide") == {
        "occurrences": 20, "unique_blobs": 8, "unique_physical_lines": 854,
    }, "E_FITTING_GUIDE")
    owners = document.get("active_phase067_owners", {})
    require(owners.get("active_count") == 3, "E_OWNER_COUNT")
    require([(row.get("obligation_id"), row.get("origin_identity"))
             for row in owners.get("identities", [])] == sorted(EXPECTED_OWNERS),
            "E_OWNER_IDENTITIES")
    require(document.get("plan", {}).get("steps") == EXPECTED_STEPS, "E_STEPS")
    require(document.get("phase_gate_alternatives") == EXPECTED_FINAL_GATES, "E_FINAL_GATES")
    plan_outputs = document.get("plan", {}).get("step_output_contracts")
    require(type(plan_outputs) is list and [row.get("step") for row in plan_outputs] == EXPECTED_STEPS,
            "E_STEP_OUTPUT_CONTRACTS")
    require(all(row.get("paths") == STEP_OUTPUTS[row["step"]]
                and row.get("count") == len(STEP_OUTPUTS[row["step"]])
                and row.get("status") == "/".join(
                    "M" if path in RECOVERY_PATHS else "A" for path in STEP_OUTPUTS[row["step"]]
                ) for row in plan_outputs), "E_STEP_OUTPUT_CONTRACTS")
    supplemental = document.get("supplemental_fitting_inputs", {})
    require(supplemental.get("count") == 10 and supplemental.get("phase080_route_count") == 3,
            "E_SUPPLEMENTAL_COUNTS")
    require([(row.get("path"), row.get("bounded_role"), row.get("phase080_saved_profile_route"))
             for row in supplemental.get("rows", [])] == SUPPLEMENTAL_FIT_INPUTS,
            "E_SUPPLEMENTAL_ROWS")
    require(all(row.get("canonical_baseline_promoted") is False
                and len(row.get("git_identities", [])) == 2
                and row["git_identities"][0].get("blob_oid") == row["git_identities"][1].get("blob_oid")
                for row in supplemental.get("rows", [])), "E_SUPPLEMENTAL_IDENTITIES")
    predecessor = document.get("predecessor", {})
    require(predecessor.get("single_parent_verified") is True
            and predecessor.get("claude_diff_zero") is True
            and predecessor.get("exact_status") == PREDECESSOR_FINAL_STATUS
            and len(predecessor.get("committed_blobs", [])) == 8,
            "E_PREDECESSOR_CERTIFICATE")
    history = document.get("historical_execution", {})
    require(history.get("canonical_reused") == 14, "E_HISTORY_REUSE")
    require(history.get("fresh_replay") == 0, "E_HISTORY_REPLAY")
    validate_activation_authority(document.get("authority"))
    require(document.get("semantic_sha256") == semantic_hash(document), "E_SEMANTIC")


def validate_activation_authority(authority: Any) -> None:
    require(type(authority) is dict, "E_AUTHORITY_SCHEMA")
    require(authority.get("ref7_original_full_text") == "GROUND_NOT_FOUND", "E_AUTHORITY_REF7")
    require(authority.get("optimizer_state_recovered") is False, "E_AUTHORITY_OPTIMIZER")
    require(authority.get("heldout_validated") is False, "E_AUTHORITY_HELDOUT")
    require(authority.get("external_scientific") is False, "E_AUTHORITY_EXTERNAL")
    require(authority.get("material_validated") is False, "E_AUTHORITY_MATERIAL")
    require(authority.get("stale_pdf_closed") is False, "E_AUTHORITY_STALE_PDF")
    require(authority.get("production_modified") is False, "E_AUTHORITY_PRODUCTION")
    require(authority.get("untested_code_assumed_working") is False, "E_AUTHORITY_UNTESTED")


def set_nested(document: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    current: dict[str, Any] = document
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def expect_validation_error(code: str, operation: Callable[[], Any]) -> None:
    try:
        operation()
    except ValidationError as error:
        require(error.code == code, "E_NEGATIVE_WRONG_DIAGNOSTIC", f"{code}!={error.code}")
        return
    raise ValidationError("E_NEGATIVE_FALSE_PASS")


def expect_error(operation: Callable[[], Any]) -> None:
    try:
        operation()
    except (ValidationError, json.JSONDecodeError, UnicodeError, TypeError, ValueError):
        return
    raise ValidationError("E_NEGATIVE_FALSE_PASS")


def run_semantic_controls(document: dict[str, Any]) -> tuple[int, int]:
    mutations: list[tuple[tuple[str, ...], Any]] = [
        (("schema_version",), "bad"),
        (("phase",), "066"),
        (("status",), "PASS"),
        (("gate",), "PASS_P067_CODE_HISTORY"),
        (("persistence_terminal",), "bad"),
        (("expected_parent",), "0" * 40),
        (("expected_subject",), "bad"),
        (("exact_seven", "count"), 8),
        (("exact_seven", "paths"), FINAL_PATHS[:-1]),
        (("exact_seven", "status"), ["A"] * 7),
        (("exact_seven", "rename_allowed"), True),
        (("exact_seven", "modes"), ["100755"] + ["100644"] * 6),
        (("inventory", "python_occurrences"), 128),
        (("inventory", "python_unique_blobs"), 83),
        (("inventory", "python_unique_physical_lines"), 29951),
        (("inventory", "release_count"), 19),
        (("inventory", "roles", "code"), {"occurrences": 19, "unique_blobs": 15}),
        (("inventory", "roles", "code"), {"occurrences": 20, "unique_blobs": 14}),
        (("inventory", "roles", "test"), {"occurrences": 43, "unique_blobs": 29}),
        (("inventory", "roles", "test"), {"occurrences": 44, "unique_blobs": 28}),
        (("inventory", "roles", "demo"), {"occurrences": 29, "unique_blobs": 26}),
        (("inventory", "roles", "demo"), {"occurrences": 30, "unique_blobs": 25}),
        (("inventory", "roles", "result"), {"occurrences": 34, "unique_blobs": 14}),
        (("inventory", "roles", "result"), {"occurrences": 35, "unique_blobs": 13}),
        (("inventory", "golden"), {"occurrences": 7, "unique_blobs": 2}),
        (("inventory", "golden"), {"occurrences": 8, "unique_blobs": 1}),
        (("inventory", "fitting_guide"), {"occurrences": 19, "unique_blobs": 8, "unique_physical_lines": 854}),
        (("inventory", "fitting_guide"), {"occurrences": 20, "unique_blobs": 7, "unique_physical_lines": 854}),
        (("inventory", "fitting_guide"), {"occurrences": 20, "unique_blobs": 8, "unique_physical_lines": 853}),
        (("active_phase067_owners", "active_count"), 2),
        (("active_phase067_owners", "identities"), []),
        (("plan", "steps"), EXPECTED_STEPS[:-1]),
        (("phase_gate_alternatives",), ["PASS_P067_CODE_HISTORY"]),
        (("historical_execution", "canonical_reused"), 13),
        (("historical_execution", "fresh_replay"), 14),
    ]
    require(len(mutations) == 35, "E_SEMANTIC_CONTROL_COUNT")
    passed = 0
    for path, value in mutations:
        candidate = copy.deepcopy(document)
        set_nested(candidate, path, value)
        candidate["semantic_sha256"] = semantic_hash(candidate)
        expect_error(lambda candidate=candidate: assert_payload(candidate))
        passed += 1
    return passed, len(mutations)


def run_strict_json_controls() -> tuple[int, int]:
    cases = [
        (b'{"a":1,"a":2}\n', "E_JSON_DUPLICATE"),
        (b'{"a":NaN}\n', "E_JSON_NONFINITE"),
        (b'{"a":Infinity}\n', "E_JSON_NONFINITE"),
        (b'[]\n', "E_JSON_ROOT"),
        ((b'{"a":' * 34) + b'0' + (b'}' * 34), "E_JSON_DEPTH"),
        (b'\xff', "E_JSON_UTF8"),
    ]
    for index, (raw, code) in enumerate(cases, start=1):
        expect_validation_error(code, lambda raw=raw, index=index: strict_load_bytes(
            raw, f"strict-{index}"
        ))
    return len(cases), len(cases)


def control_documents() -> dict[str, str]:
    return {
        path: read_lf(path).decode("utf-8", errors="strict")
        for path in CONTROL_TOKENS
    }


def run_human_controls() -> tuple[int, int]:
    base = control_documents()
    p67_parent = unique_prefixed_line(base[PARENT_LEDGER_PATH], "| 067 |", "E_TEST_FIXTURE")
    p66_execution = unique_prefixed_line(
        base[ACTIVE_LEDGER_PATH], "| Phase 066 Step 81.2 |", "E_TEST_FIXTURE"
    )
    cases = [
        (RESULT_PATH, base[RESULT_PATH].replace("Status: `PASS_PENDING_PERSISTENCE`\n", "", 1),
         "E_CONTROL_RESULT_SCHEMA"),
        (RESULT_PATH, base[RESULT_PATH] + "\nStatus: `PASS_PENDING_PERSISTENCE`\n",
         "E_CONTROL_RESULT_SCHEMA"),
        (PARENT_LEDGER_PATH, base[PARENT_LEDGER_PATH] + "\n" + p67_parent + "\n",
         "E_CONTROL_PARENT_P067_ROW"),
        (ACTIVE_LEDGER_PATH, base[ACTIVE_LEDGER_PATH] + "\n" + p66_execution + "\n",
         "E_CONTROL_ACTIVE_P066_EXECUTION"),
        (HANDOVER_PATH, base[HANDOVER_PATH].replace(
            "Begin Step 82 only after", "Begin Step 81 only after", 1
        ), "E_CONTROL_HANDOVER_NEXT_SCHEMA"),
    ]
    for path, replacement, code in cases:
        candidate = copy.deepcopy(base)
        candidate[path] = replacement
        expect_validation_error(code, lambda candidate=candidate: validate_control_documents(candidate))
    return len(cases), len(cases)


def select_phase067_gate(
    *, coverage_complete: bool, owner_routing_complete: bool, validation_ok: bool,
    authority_promoted: bool, internal_cells: list[str], known_open_debts: list[str],
) -> str:
    require(bool(internal_cells), "E_GATE_INTERNAL_CELLS")
    allowed = {"COMPLETE", "GROUND_NOT_FOUND", "NOT_TESTED", "PARTIAL"}
    require(set(internal_cells) <= allowed, "E_GATE_INTERNAL_STATUS")
    require(all(type(item) is str for item in known_open_debts), "E_GATE_OPEN_DEBT_SCHEMA")
    if not coverage_complete or not owner_routing_complete or not validation_ok or authority_promoted:
        return "FAIL_P067"
    if all(cell == "COMPLETE" for cell in internal_cells):
        return "PASS_P067_CODE_HISTORY"
    if any(cell in {"GROUND_NOT_FOUND", "NOT_TESTED", "PARTIAL"} for cell in internal_cells):
        return "CONDITIONAL_P067"
    return "FAIL_P067"


def run_gate_controls() -> tuple[int, int]:
    debts = ["REF7", "ORIGINAL_OPTIMIZER", "HELDOUT", "EXTERNAL", "MATERIAL", "STALE_PDF"]
    cases = [
        ({"coverage_complete": True, "owner_routing_complete": True, "validation_ok": True,
          "authority_promoted": False, "internal_cells": ["COMPLETE"],
          "known_open_debts": debts}, "PASS_P067_CODE_HISTORY"),
        ({"coverage_complete": True, "owner_routing_complete": True, "validation_ok": True,
          "authority_promoted": False, "internal_cells": ["COMPLETE", "NOT_TESTED"],
          "known_open_debts": debts}, "CONDITIONAL_P067"),
        ({"coverage_complete": False, "owner_routing_complete": True, "validation_ok": True,
          "authority_promoted": False, "internal_cells": ["COMPLETE"],
          "known_open_debts": debts}, "FAIL_P067"),
        ({"coverage_complete": True, "owner_routing_complete": False, "validation_ok": True,
          "authority_promoted": False, "internal_cells": ["PARTIAL"],
          "known_open_debts": debts}, "FAIL_P067"),
        ({"coverage_complete": True, "owner_routing_complete": True, "validation_ok": True,
          "authority_promoted": True, "internal_cells": ["COMPLETE"],
          "known_open_debts": debts}, "FAIL_P067"),
    ]
    for arguments, expected in cases:
        require(select_phase067_gate(**arguments) == expected, "E_GATE_SELECTION", expected)
    no_debt = copy.deepcopy(cases[0][0])
    no_debt["known_open_debts"] = []
    require(select_phase067_gate(**no_debt) == "PASS_P067_CODE_HISTORY",
            "E_GATE_EXTERNAL_DEBT_DETERMINANT")
    plan = read_lf(PLAN_PATH).decode("utf-8", errors="strict")
    mutated = plan.replace("Phase 067 gate 선택 determinant가 아니다", "Phase 067 gate determinant다", 1)
    expect_validation_error("E_PLAN_GATE_EXCLUSIVITY", lambda: validate_plan_text(mutated))
    return len(cases) + 2, len(cases) + 2


def run_repository_controls() -> tuple[int, int]:
    good = repository_snapshot(EXPECTED_PARENT)
    mutation_specs = [
        ("branch", "other", "E_REPOSITORY_BRANCH"),
        ("head", "0" * 40, "E_REPOSITORY_HEAD"),
        ("upstream_name", "origin/other", "E_REPOSITORY_UPSTREAM_NAME"),
        ("upstream", "0" * 40, "E_REPOSITORY_UPSTREAM"),
        ("tracking_active", "0" * 40, "E_REPOSITORY_TRACKING"),
        ("live_active", "0" * 40, "E_REPOSITORY_LIVE"),
        ("protected_local", "0" * 40, "E_REPOSITORY_PROTECTED_LOCAL"),
        ("protected_tracking", "0" * 40, "E_REPOSITORY_PROTECTED_TRACKING"),
        ("protected_live", "0" * 40, "E_REPOSITORY_PROTECTED_LIVE"),
        ("main_tracking", "0" * 40, "E_REPOSITORY_MAIN_TRACKING"),
        ("main_live", "0" * 40, "E_REPOSITORY_MAIN_LIVE"),
        ("local_main_absent", False, "E_REPOSITORY_LOCAL_MAIN"),
        ("claude_dirty", True, "E_REPOSITORY_CLAUDE_DIRTY"),
        ("origin_url", "https://example.invalid/repo.git", "E_REPOSITORY_ORIGIN"),
        ("expected_tip", "0" * 40, "E_REPOSITORY_EXPECTED_TIP"),
        ("diff_check", False, "E_REPOSITORY_DIFF_CHECK"),
        ("cached_diff_check", False, "E_REPOSITORY_CACHED_DIFF_CHECK"),
        ("head", "not-an-oid", "E_REPOSITORY_HEAD"),
    ]
    for key, value, code in mutation_specs:
        candidate = copy.deepcopy(good)
        candidate[key] = value
        expect_validation_error(code, lambda candidate=candidate: validate_repository_record(
            candidate, EXPECTED_PARENT
        ))
    change_cases = [
        ({"unexpected_staged": True}, "E_CHANGE_DIRTY"),
        ({"status": {**FINAL_STATUS, "Codex/extra": "A"}}, "E_CHANGE_STATUS"),
        ({"status": {**FINAL_STATUS, PLAN_PATH: "R"}}, "E_CHANGE_RENAME"),
        ({"modes": {**{path: "100644" for path in FINAL_PATHS}, PLAN_PATH: "100755"}},
         "E_CHANGE_MODE"),
    ]
    defaults = {
        "status": FINAL_STATUS,
        "modes": {path: "100644" for path in FINAL_PATHS},
        "unexpected_staged": False,
    }
    for mutation, code in change_cases:
        candidate = {**defaults, **mutation}
        expect_validation_error(code, lambda candidate=candidate: validate_change_record(
            candidate["status"], candidate["modes"], FINAL_STATUS,
            unexpected_staged=candidate["unexpected_staged"],
        ))
    seal = {"refs": {"head": EXPECTED_PARENT}, "bytes": {PLAN_PATH: "same"}}
    changed_bytes = copy.deepcopy(seal)
    changed_bytes["bytes"][PLAN_PATH] = "changed"
    expect_validation_error(
        "E_CHANGE_TOCTOU",
        lambda: validate_terminal_seal(seal, changed_bytes, "E_CHANGE_TOCTOU"),
    )
    changed_ref = copy.deepcopy(seal)
    changed_ref["refs"]["head"] = "0" * 40
    expect_validation_error(
        "E_PERSISTENCE_TOCTOU",
        lambda: validate_terminal_seal(seal, changed_ref, "E_PERSISTENCE_TOCTOU"),
    )
    total = len(mutation_specs) + len(change_cases) + 2
    return total, total


def run_migration_controls() -> tuple[int, int]:
    raw = read_lf(PREDECESSOR_JSON_PATH)
    document, _, _, _ = strict_load_bytes(raw, PREDECESSOR_JSON_PATH)
    cases = [
        (("gate",), "PASS_P066_LINEAGE_I", "E_PREDECESSOR_GATE"),
        (("authority_ceiling", "external_authority"), True, "E_PREDECESSOR_AUTHORITY"),
        (("canonical_history_contract", "total"), 15, "E_PREDECESSOR_HISTORY"),
    ]
    for path, value, code in cases:
        candidate = copy.deepcopy(document)
        set_nested(candidate, path, value)
        expect_validation_error(code, lambda candidate=candidate: validate_predecessor_document(candidate))
    return len(cases), len(cases)


def run_authority_controls(document: dict[str, Any]) -> tuple[int, int]:
    cases = [
        ("ref7_original_full_text", "PRESENT", "E_AUTHORITY_REF7"),
        ("optimizer_state_recovered", True, "E_AUTHORITY_OPTIMIZER"),
        ("heldout_validated", True, "E_AUTHORITY_HELDOUT"),
        ("external_scientific", True, "E_AUTHORITY_EXTERNAL"),
        ("material_validated", True, "E_AUTHORITY_MATERIAL"),
        ("stale_pdf_closed", True, "E_AUTHORITY_STALE_PDF"),
    ]
    authority = document.get("authority")
    require(type(authority) is dict, "E_AUTHORITY_SCHEMA")
    for key, value, code in cases:
        candidate = copy.deepcopy(authority)
        candidate[key] = value
        expect_validation_error(code, lambda candidate=candidate: validate_activation_authority(candidate))
    return len(cases), len(cases)


def negative_contract_counts(document: dict[str, Any]) -> dict[str, int]:
    semantic_passed, _ = run_semantic_controls(document)
    strict_passed, _ = run_strict_json_controls()
    source = validate_source_policy()
    human_passed, _ = run_human_controls()
    gate_passed, _ = run_gate_controls()
    repository_passed, _ = run_repository_controls()
    migration_passed, _ = run_migration_controls()
    authority_passed, _ = run_authority_controls(document)
    return {
        "semantic_cases": semantic_passed,
        "strict_json_cases": strict_passed,
        "source_policy_cases": source["negative_cases"] + source["git_argv_negative_cases"],
        "human_cases": human_passed,
        "gate_cases": gate_passed,
        "repository_cases": repository_passed,
        "migration_cases": migration_passed,
        "authority_cases": authority_passed,
        "determinism_reconstructions": 2,
    }


def validate_change_record(
    status: dict[str, str], modes: dict[str, str], expected: dict[str, str], *,
    unexpected_staged: bool,
) -> None:
    require(not unexpected_staged, "E_CHANGE_DIRTY")
    require(all(value in {"A", "M", "D"} for value in status.values()), "E_CHANGE_RENAME")
    require(status == expected, "E_CHANGE_STATUS", repr(status))
    require(modes == {path: "100644" for path in expected}, "E_CHANGE_MODE", repr(modes))


def index_blob(path: str) -> bytes:
    return run_git(["show", f":{path}"]).stdout


def change_seal(expected: dict[str, str], *, staged: bool) -> dict[str, Any]:
    if staged:
        status = staged_status()
        modes = index_modes(list(expected))
        validate_change_record(status, modes, expected, unexpected_staged=False)
        unstaged = unstaged_status()
        untracked = untracked_paths()
        require(not unstaged and not untracked, "E_CHANGE_DIRTY", repr((unstaged, untracked)))
        require(run_git(["diff", "--cached", "--check"], check=False).returncode == 0,
                "E_STAGED_DIFF_CHECK")
        index_hashes = {path: sha256(index_blob(path)) for path in expected}
    else:
        staged_now = staged_status()
        status = worktree_status()
        tracked_modes = index_modes([path for path in expected if (ROOT / path).is_file()])
        require(all(mode == "100644" for mode in tracked_modes.values()),
                "E_CHANGE_MODE", repr(tracked_modes))
        modes = {path: "100644" for path in expected}
        validate_change_record(status, modes, expected, unexpected_staged=bool(staged_now))
        require(run_git(["diff", "--check"], check=False).returncode == 0,
                "E_WORKTREE_DIFF_CHECK")
        unstaged = unstaged_status()
        untracked = untracked_paths()
        index_hashes = {}
    require(not run_git(["status", "--porcelain=v1", "--", "Claude"]).stdout, "E_CLAUDE_DIRTY")
    worktree_hashes = {path: sha256(read_lf(path)) for path in expected}
    if staged:
        require(index_hashes == worktree_hashes, "E_STAGED_WORKTREE_BYTES")
    return {
        "staged": staged,
        "status": status,
        "modes": modes,
        "unstaged": unstaged,
        "untracked": untracked,
        "worktree_hashes": worktree_hashes,
        "index_hashes": index_hashes,
    }


def transaction_seal(expected_tip: str, mutable_paths: list[str]) -> dict[str, Any]:
    static_inputs = [
        MANIFEST_PATH, CARRY_PATH, PREDECESSOR_JSON_PATH,
        PREDECESSOR_VALIDATOR_PATH, PREDECESSOR_RESULT_PATH,
    ]
    paths = list(dict.fromkeys([*mutable_paths, *static_inputs]))
    path_set = set(paths)
    staged = {path: status for path, status in staged_status().items() if path in path_set}
    unstaged = {path: status for path, status in unstaged_status().items() if path in path_set}
    untracked = [path for path in untracked_paths() if path in path_set]
    modes = index_modes(paths)
    index_hashes = {path: sha256(index_blob(path)) for path in modes}
    worktree_hashes = {path: sha256(read_lf(path)) for path in paths}
    return {
        "repository": repository_snapshot(expected_tip),
        "paths": paths,
        "staged_status": staged,
        "unstaged_status": unstaged,
        "untracked_paths": untracked,
        "index_modes": modes,
        "index_hashes": index_hashes,
        "worktree_hashes": worktree_hashes,
        "exact_input_hashes": {path: worktree_hashes[path] for path in paths},
    }


def validate_payload_source_hashes(document: dict[str, Any], seal: dict[str, Any]) -> None:
    recorded = {
        PLAN_PATH: document.get("plan", {}).get("sha256_lf"),
        VALIDATOR_PATH: document.get("validator_identity", {}).get("sha256_lf"),
        RESULT_PATH: document.get("human_evidence", {}).get("result_sha256_lf"),
    }
    for row in document.get("controls", {}).get("records", []):
        if type(row) is dict and row.get("path") in RECOVERY_PATHS:
            recorded[row["path"]] = row.get("sha256_lf")
    require(recorded == {path: seal["worktree_hashes"][path] for path in NONSELF_PATHS},
            "E_TRANSACTION_RECORDED_SOURCE_HASH")
    static_recorded = {
        MANIFEST_PATH: document.get("inventory", {}).get("manifest_sha256_lf"),
        CARRY_PATH: document.get("active_phase067_owners", {}).get("sha256_lf"),
        PREDECESSOR_JSON_PATH: document.get("predecessor", {}).get("json_sha256_lf"),
        PREDECESSOR_VALIDATOR_PATH: document.get("predecessor", {}).get("validator_sha256_lf"),
        PREDECESSOR_RESULT_PATH: document.get("human_evidence", {}).get("predecessor_result_sha256_lf"),
    }
    require(static_recorded == {
        path: seal["exact_input_hashes"][path] for path in static_recorded
    }, "E_TRANSACTION_INPUT_HASH")


def validate_worktree(expected: dict[str, str], *, staged: bool) -> None:
    entry = change_seal(expected, staged=staged)
    terminal = change_seal(expected, staged=staged)
    validate_terminal_seal(entry, terminal, "E_CHANGE_TOCTOU")


def validate_expected_commit(value: str | None) -> str:
    require(value is not None and re.fullmatch(r"[0-9a-f]{40}", value) is not None,
            "E_EXPECTED_COMMIT", repr(value))
    return value


def persistence_seal(expected_commit: str) -> dict[str, Any]:
    repository = repository_snapshot(expected_commit)
    require(not staged_status() and not unstaged_status() and not untracked_paths(),
            "E_PERSISTENCE_DIRTY")
    parents = git_text(["show", "-s", "--format=%P", expected_commit]).split()
    require(parents == [EXPECTED_PARENT], "E_PERSISTENCE_PARENT", repr(parents))
    subject = git_text(["show", "-s", "--format=%s", expected_commit])
    require(subject == EXPECTED_SUBJECT, "E_PERSISTENCE_SUBJECT")
    status = parse_name_status(run_git([
        "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-z", "-r",
        expected_commit,
    ]).stdout)
    require(status == FINAL_STATUS, "E_PERSISTENCE_PATHS", repr(status))
    entries = tree_entries(expected_commit, FINAL_PATHS)
    modes = {path: row["mode"] for path, row in entries.items()}
    require(modes == {path: "100644" for path in FINAL_PATHS}, "E_PERSISTENCE_MODES", repr(modes))
    committed_hashes = {}
    worktree_hashes = {}
    for path in FINAL_PATHS:
        committed = git_blob(expected_commit, path)
        require(committed == read_lf(path), "E_PERSISTENCE_BLOB", path)
        committed_hashes[path] = sha256(committed)
        worktree_hashes[path] = sha256(read_lf(path))
    require(not run_git(["diff", "--quiet", EXPECTED_PARENT, expected_commit, "--", "Claude"],
                        check=False).returncode, "E_PERSISTENCE_CLAUDE_DIFF")
    return {
        "repository": repository,
        "parents": parents,
        "subject": subject,
        "status": status,
        "entries": entries,
        "committed_hashes": committed_hashes,
        "worktree_hashes": worktree_hashes,
    }


def validate_persistence(expected_commit: str) -> None:
    entry = persistence_seal(expected_commit)
    terminal = persistence_seal(expected_commit)
    validate_terminal_seal(entry, terminal, "E_PERSISTENCE_TOCTOU")


def read_stored() -> tuple[dict[str, Any], bytes, int, int, int]:
    require(OUTPUT.is_file(), "E_VALIDATION_ARTIFACT_MISSING", OUTPUT_PATH)
    raw = OUTPUT.read_bytes()
    require(raw == lf_bytes(raw), "E_OUTPUT_LF")
    document, nodes, scalars, depth = strict_load_bytes(raw, OUTPUT_PATH)
    require(canonical_bytes(document) == raw, "E_OUTPUT_CANONICAL")
    require(document.get("semantic_sha256") == semantic_hash(document), "E_SEMANTIC")
    return document, raw, nodes, scalars, depth


def atomic_collect(raw: bytes) -> None:
    require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST")
    temp_path = OUTPUT.with_name(OUTPUT.name + ".tmp-phase067-plan")
    require(not temp_path.exists(), "E_COLLECT_TEMP_EXISTS", str(temp_path))
    try:
        temp_path.write_bytes(raw)
        document, _, _, _ = strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        require(canonical_bytes(document) == raw, "E_COLLECT_CANONICAL")
        os.replace(temp_path, OUTPUT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(OUTPUT.read_bytes() == raw, "E_COLLECT_WRITE")


def run_controls(document: dict[str, Any]) -> dict[str, str]:
    counts = document.get("negative_contract")
    require(type(counts) is dict and counts == negative_contract_counts(document),
            "E_NEGATIVE_CONTRACT_RECONSTRUCTION")
    return {
        key.removesuffix("_cases"): f"{value}/{value}"
        for key, value in counts.items()
        if key.endswith("_cases")
    } | {
        "determinism": "2/2",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require(sum((args.collect, args.content_only, args.verify_staged, args.verify_persistence)) == 1,
            "E_CLI_MODE")
    require((args.verify_persistence and args.expected_commit is not None)
            or (not args.verify_persistence and args.expected_commit is None),
            "E_EXPECTED_COMMIT_MODE")
    validate_source_policy()
    expected_tip = validate_expected_commit(args.expected_commit) if args.verify_persistence \
        else EXPECTED_PARENT
    transaction_paths = NONSELF_PATHS if args.collect else FINAL_PATHS
    transaction_entry = transaction_seal(expected_tip, transaction_paths)

    if args.collect:
        require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE", OUTPUT_PATH)
        repository_snapshot(EXPECTED_PARENT)
        validate_worktree(NONSELF_STATUS, staged=False)
        first = build_payload()
        second = build_payload()
        first_raw = canonical_bytes(first)
        require(first_raw == canonical_bytes(second), "E_DETERMINISM")
        metrics = run_controls(first)
        atomic_collect(first_raw)
        validate_worktree(FINAL_STATUS, staged=False)
        transaction_terminal = transaction_seal(expected_tip, transaction_paths)
        validate_terminal_seal(transaction_entry, transaction_terminal, "E_TRANSACTION_TOCTOU")
        validate_payload_source_hashes(first, transaction_terminal)
        print("PASS_P067_PLAN_CONTROLS " + " ".join(f"{key}={value}" for key, value in metrics.items()))
        print("PASS_P067_PLAN_DETERMINISM 2/2")
        print("PASS_P067_PLAN_ACTIVATION collect=JSON_LAST result_first=true historical=CANONICAL_REUSED_14/14 fresh_historical_replay=0/14")
        return 0

    stored, stored_raw, nodes, scalars, depth = read_stored()
    first = build_payload()
    second = build_payload()
    expected_raw = canonical_bytes(first)
    require(expected_raw == canonical_bytes(second), "E_DETERMINISM")
    require(stored_raw == expected_raw, "E_STORED_RECONSTRUCTION")
    assert_payload(stored)
    metrics = run_controls(stored)
    if args.content_only:
        repository_snapshot(EXPECTED_PARENT)
        validate_worktree(FINAL_STATUS, staged=False)
    elif args.verify_staged:
        repository_snapshot(EXPECTED_PARENT)
        validate_worktree(FINAL_STATUS, staged=True)
    else:
        validate_persistence(expected_tip)
    transaction_terminal = transaction_seal(expected_tip, transaction_paths)
    validate_terminal_seal(transaction_entry, transaction_terminal, "E_TRANSACTION_TOCTOU")
    validate_payload_source_hashes(stored, transaction_terminal)
    print("PASS_P067_PLAN_CONTROLS " + " ".join(f"{key}={value}" for key, value in metrics.items()))
    print("PASS_P067_PLAN_DETERMINISM 2/2")
    if args.content_only:
        print(
            "PASS_P067_PLAN_CONTENT python=129/84/29952 releases=20 "
            f"json_nodes={nodes} scalars={scalars} depth={depth} "
            "historical=CANONICAL_REUSED_14/14 fresh_historical_replay=0/14"
        )
    elif args.verify_staged:
        print("PASS_P067_PLAN_ACTIVATION_STAGED exact-seven=7/7 modes=100644/7 historical=CANONICAL_REUSED_14/14 fresh_historical_replay=0/14")
    else:
        print(f"{PERSISTENCE} commit={expected_tip} exact-seven=7/7 historical=CANONICAL_REUSED_14/14 fresh_historical_replay=0/14")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError,
            subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, ValidationError) else str(type(error))
        print(f"FAIL_P067_PLAN_CONTENT {code}: {error}")
        raise SystemExit(1)
