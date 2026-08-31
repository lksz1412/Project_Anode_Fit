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
import sys
import tempfile
from collections.abc import Callable
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
VALIDATOR_PATH = "Codex/work/v1024_phase065/validate_phase065_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_065_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_065_V1024_V1024_1_LINEAGE_REPORT_H.md"
GATE_RESULT_PATH = "Codex/results/PHASE_065_STEP_075_2_GATE_RESULT.md"
PHASE_RESULT_PATH = "Codex/results/PHASE_065_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT_COMMIT = "26e2ce9559220d5782e1303d68b4449a36309e94"
SUBJECT = "audit(phase065): close v1024 lineage gate"
GATE = "CONDITIONAL_P065"
PERSISTENCE = "PASS_P065_STEP75_2_PERSISTENCE"
STATUS = "CONDITIONAL_WITH_OPEN_EXTERNAL_AUTHORITY"
CANONICAL_FULL_COLLECT_SEMANTIC_SHA256 = "6c3803eb4888e47d3aedfb1fc0d5dee26e669f4429c70ced56e46df8cbbbf21b"
CANONICAL_METADATA_CHECKPOINT_SEMANTIC_SHA256 = "ce1a434c27d751a3bbfe18dbb9311884a06522bb1b36965d97f6313d03b1ff2e"
CANONICAL_HARDENING_CHECKPOINT_SEMANTIC_SHA256 = "ff46391d8a2beab23da64eb37f2420cefc8d2115cdfcbb371a62a0d200a154b1"
ALLOWED_IMPORT_ROOTS = frozenset({
    "__future__", "argparse", "ast", "collections", "copy", "hashlib", "json", "math", "os", "pathlib", "re",
    "shutil", "stat", "subprocess", "sys", "tempfile", "typing",
})
SUBORDINATE_RUNTIME_PROBE = "import PIL,numpy,pypdf,sys;print(sys.executable)"
LEDGER_PROGRESS = "Steps 70–75.1 complete; Step 75.2 precommit evidence and Gate selected, persistence pending"
PHASE_RESULT_PROGRESS_LINE = (
    "Plan activation과 cumulative Steps 70–75.1은 commit/push/persistence까지 완료했다. Step 75.2는 precommit evidence와 "
    "`CONDITIONAL_P065` Gate를 선택했으며 exact-eight commit/push/persistence는 아직 남아 있다. Frozen v1.0.24/v1.0.24.1 source "
    "occurrences `261`, unique blobs `131`, text `125/21,618`, PDF `3/148`, image `3/3`, release process `38`, routed process `98`, "
    "runtime runs `18`, conformance rows `41`, source dispositions `261`, carry observations `192`, active obligations `94`를 통합했다."
)
NEXT_EXACT_STEP_BODY = (
    "Controller validates and stages exactly the Step 75.2 eight declared paths: final validator, `PHASE_065_VALIDATION.json`, "
    "Lineage Report H, Step 75.2 Gate Result, Phase Result, both execution ledgers and active handover. Run Python 3.12/3.14 staged "
    "validation and independent science/validator/records reviews, require P0/P1/P2=`0/0/0`, commit with subject "
    "`audit(phase065): close v1024 lineage gate` and parent `26e2ce9559220d5782e1303d68b4449a36309e94`, push and verify "
    "local/upstream/tracking/live-origin equality, exact committed paths/blob bytes, protected/main/Claude non-change and clean status. "
    "Only after `PASS_P065_STEP75_2_PERSISTENCE` may the Phase 066 detailed plan be saved and activated; cumulative Step 76 begins only after that plan activation."
)

FINAL_PATHS = [
    VALIDATOR_PATH,
    ARTIFACT_PATH,
    REPORT_PATH,
    GATE_RESULT_PATH,
    PHASE_RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_PATH_SET = set(FINAL_PATHS)
NONSELF_PATHS = [path for path in FINAL_PATHS if path != ARTIFACT_PATH]
ARTIFACT = ROOT / ARTIFACT_PATH
VALIDATOR = ROOT / VALIDATOR_PATH

AUTHORITY_BOUNDARY = (
    "CONDITIONAL_P065 certifies complete internal v1.0.24/v1.0.24.1 lineage/read/process/static/runtime/science/conformance/disposition auditing, "
    "but Ref. 7 original full text remains GROUND_NOT_FOUND under Phase 071 ownership. It does not certify Ref. 7 proposition content, external material or experimental truth, "
    "canonical selection, defect repair, parameter identifiability, held-out fitting, final equation freeze, final LaTeX/PDF or publication readiness."
)
ORIGIN_IDENTITY_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
REMOTE_HELPER_BYTES = b"""#!/bin/sh
while IFS= read -r command; do
    case "$command" in
        capabilities) printf '\\n' ;;
        list)
            git --git-dir="$PHASE065_FIXTURE_ORIGIN" for-each-ref --format='%(objectname) %(refname)' refs/heads
            printf '\\n'
            ;;
        '') exit 0 ;;
        *) printf '\\n' ;;
    esac
done
"""


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def validate_python_execution_argv(argv: list[str], cwd: pathlib.Path = ROOT) -> None:
    require(bool(argv), "E_SOURCE_POLICY_EXECUTION_ALLOWLIST", "empty argv")
    launcher = pathlib.Path(argv[0]).name.lower()
    require(launcher in {"git", "git.exe", "py", "py.exe", "python", "python.exe", "python3", "python3.exe"},
            "E_SOURCE_POLICY_EXECUTION_ALLOWLIST", launcher)
    if launcher in {"git", "git.exe"}:
        require(argv[0] in {"git", "git.exe"}, "E_SOURCE_POLICY_GIT", repr(argv))
        git_args = argv[1:]
        require(bool(git_args), "E_SOURCE_POLICY_GIT", "missing subcommand")
        if git_args[0] == "--git-dir":
            require(len(git_args) >= 4 and git_args[2] == "update-ref",
                    "E_SOURCE_POLICY_GIT", repr(argv))
            git_dir = pathlib.Path(git_args[1])
            require(git_dir.is_absolute(), "E_SOURCE_POLICY_GIT", repr(argv))
            try:
                git_dir.resolve().relative_to(pathlib.Path(tempfile.gettempdir()).resolve())
            except (OSError, ValueError) as error:
                raise ValidationError("E_SOURCE_POLICY_GIT", repr(argv)) from error
            subcommand = "update-ref"
            subcommand_args = git_args[3:]
        else:
            subcommand = git_args[0]
            subcommand_args = git_args[1:]
        allowed_subcommands = {
            "add", "branch", "checkout", "clone", "commit", "config", "diff", "diff-tree", "init",
            "ls-files", "ls-remote", "ls-tree", "merge-base", "mv", "push", "remote", "reset",
            "rev-parse", "rm", "show", "status", "switch", "update-index", "update-ref",
        }
        require(subcommand in allowed_subcommands, "E_SOURCE_POLICY_GIT", repr(argv))
        lowered = [item.lower() for item in git_args]
        forbidden_exact = {"--config-env", "--upload-pack", "--receive-pack", "--exec-path"}
        require(not any(item in forbidden_exact or any(item.startswith(prefix + "=") for prefix in forbidden_exact)
                        for item in lowered), "E_SOURCE_POLICY_GIT", repr(argv))
        require(not any(item.startswith(("alias.", "protocol.")) or "ext::" in item
                        for item in lowered), "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand == "config":
            require(tuple(git_args) in {
                ("config", "core.autocrlf", "false"),
                ("config", "core.autocrlf", "true"),
                ("config", "remote.origin.vcs", "phase065"),
                ("config", "user.email", "phase065-fixture@example.invalid"),
                ("config", "user.name", "Phase 065 Fixture"),
            }, "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand == "push":
            require(not any(item in {"-f", "--delete", "--force", "--mirror", "--prune", "-e"}
                            or item.startswith(("--force-with-lease", "--prune=", "--exec=", "+", ":"))
                            or item == "--exec" or item.endswith(":")
                            for item in subcommand_args), "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand == "clone":
            require(not any(item == "-u" or item == "-c" or item.startswith(("-u", "-c", "--config"))
                            for item in subcommand_args), "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand == "branch":
            require("-D" not in subcommand_args, "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand in {"checkout", "switch"}:
            require(not any(item in {"-f", "--force"} for item in subcommand_args),
                    "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand == "reset":
            require("--hard" not in subcommand_args, "E_SOURCE_POLICY_GIT", repr(argv))
        if subcommand == "update-ref" and "-d" in subcommand_args:
            try:
                cwd.resolve().relative_to(pathlib.Path(tempfile.gettempdir()).resolve())
            except (OSError, ValueError) as error:
                raise ValidationError("E_SOURCE_POLICY_GIT", repr(argv)) from error
        return
    allowed = {spec["validator"] for spec in UNIT_SPECS} | {
        "Codex/work/v1024_phase065/build_phase065_step74.py",
        "Codex/work/v1024_phase065/build_phase065_step75_1.py",
    }
    script_operands = [item for item in argv[1:] if pathlib.PurePath(item).suffix.lower() == ".py"]
    if script_operands:
        require(len(script_operands) == 1, "E_SOURCE_POLICY_EXECUTION_ALLOWLIST", repr(script_operands))
        require(len(argv) >= 2 and argv[1] == script_operands[0],
                "E_SOURCE_POLICY_EXECUTION_ALLOWLIST", repr(argv))
        script = pathlib.Path(script_operands[0])
        resolved = script.resolve() if script.is_absolute() else (cwd / script).resolve()
        try:
            normalized = resolved.relative_to(cwd.resolve()).as_posix()
        except ValueError as error:
            raise ValidationError("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", str(resolved)) from error
        require(normalized in allowed, "E_SOURCE_POLICY_EXECUTION_ALLOWLIST", normalized)
        return
    require(argv == ["py", "-3.12", "-c", SUBORDINATE_RUNTIME_PROBE],
            "E_SOURCE_POLICY_EXECUTION_ALLOWLIST", repr(argv))


def run_process(
    argv: list[str], *, cwd: pathlib.Path = ROOT, timeout: int = 300, check: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    validate_python_execution_argv(argv, cwd)
    process = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=timeout, check=False, shell=False, env=env)
    if check and process.returncode != 0:
        raise ValidationError("E_PROCESS", f"{argv!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}")
    return process


def git(
    args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True, timeout: int = 300,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, timeout=timeout, check=check, env=env)


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT) -> str:
    return git(args, cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str, *, cwd: pathlib.Path = ROOT) -> bytes:
    return git(["show", f"{commit}:{path}"], cwd=cwd, timeout=600).stdout


def nul_paths(raw: bytes) -> set[str]:
    return {part.decode("utf-8") for part in raw.split(b"\0") if part}


def status_paths(cwd: pathlib.Path = ROOT) -> set[str]:
    staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=cwd).stdout)
    unstaged = nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=cwd).stdout)
    untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=cwd).stdout)
    return staged | unstaged | untracked


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT, env: dict[str, str] | None = None) -> str:
    process = git(["ls-remote", "--exit-code", "origin", f"refs/heads/{branch}"], cwd=cwd, timeout=180, env=env)
    fields = process.stdout.decode("utf-8").strip().split()
    require(len(fields) == 2 and re.fullmatch(r"[0-9a-f]{40}", fields[0]) is not None, "E_LIVE_REF", branch)
    return fields[0]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ValidationError("E_DUPLICATE_JSON", key)
        output[key] = value
    return output


def reject_constant(value: str) -> None:
    raise ValidationError("E_NONFINITE_JSON", value)


def strict_load_bytes(raw: bytes, label: str) -> tuple[Any, dict[str, int]]:
    try:
        text = raw.decode("utf-8")
        value = json.loads(text, object_pairs_hook=reject_duplicate, parse_constant=reject_constant)
    except ValidationError:
        raise
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError("E_STRICT_JSON", label) from error
    nodes = 0
    scalars = 0
    max_depth = 0

    def walk(item: Any, depth: int = 0) -> None:
        nonlocal nodes, scalars, max_depth
        nodes += 1
        max_depth = max(max_depth, depth)
        if isinstance(item, dict):
            for key, child in item.items():
                require(type(key) is str, "E_JSON_KEY", label)
                walk(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                walk(child, depth + 1)
        else:
            scalars += 1
            if isinstance(item, float):
                require(math.isfinite(item), "E_NONFINITE_JSON", label)

    walk(value)
    return value, {"traversal_nodes": nodes, "scalar_nodes": scalars, "max_depth": max_depth + 1}


def semantic_hash(document: dict[str, Any]) -> str:
    projection = copy.deepcopy(document)
    projection.pop("semantic_sha256", None)
    return sha256(canonical_bytes(projection))


ACTIVATION = "83323ebfff1c468e4ada5e695ced10c69e24fb32"
STEP70 = "d6f680b26fb59c24098f44ed633873a2c6419a4e"
STEP71 = "5978da8626406879609b0dd5792f79143015e67f"
STEP72 = "272b8d331c55448182e96c75363a56061adf58f2"
STEP73 = "5c5c555462f1dbf0603eedda6a1d5b62684cffdf"
STEP74 = "a04bca9c73941e1a4fbc0ab6e4f4e49514dcce12"
STEP75_1 = PARENT_COMMIT


def unit(unit: str, commit: str, parent: str, subject: str, validator: str, validator_sha256: str,
         paths: list[str], invocations: list[dict[str, Any]], persistence_args: list[str],
         persistence_terminal: str, fixture: str | None = None) -> dict[str, Any]:
    return {"unit": unit, "commit": commit, "parent": parent, "subject": subject, "validator": validator,
            "validator_sha256": validator_sha256, "paths": paths, "invocations": invocations,
            "persistence_args": persistence_args, "persistence_terminal": persistence_terminal, "fixture": fixture}


def invocation(args: list[str], terminal: str) -> dict[str, Any]:
    return {"args": args, "terminal_prefix": terminal}


UNIT_SPECS = [
    unit("ACTIVATION", ACTIVATION, "60ec2d2ad08a029224b86ddc3dcf6ff718c6d310", "docs(phase065): plan v1024 lineage reaudit",
         "Codex/work/v1024_phase065/validate_phase065_plan.py", "b2073eb701eab52a71fc6b33b2e12973874935e9d113bcdf340baf25b5bdeffe",
         ["Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md", HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
          "Codex/results/PHASE_065_PLAN_ACTIVATION_RESULT.md", "Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json",
          "Codex/work/v1024_phase065/validate_phase065_plan.py"],
         [invocation(["--collect"], "PASS_P065_PLAN_ACTIVATION collect="),
          invocation(["--content-only"], "PASS_P065_PLAN_CONTENT"),
          invocation(["--verify-staged"], "PASS_P065_PLAN_ACTIVATION_STAGED")],
         ["--verify-persistence", "--expected-commit", ACTIVATION], "PASS_P065_PLAN_ACTIVATION_PERSISTENCE"),
    unit("STEP70", STEP70, ACTIVATION, "audit(phase065): freeze v1024 source process topology",
         "Codex/work/v1024_phase065/validate_phase065_step70.py", "f169eff832a079234326f9731a7c95afd45dc37cef843ee0332cd7f911d07420",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json",
          "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json", "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
          "Codex/work/v1024_phase065/build_phase065_step70.py", "Codex/work/v1024_phase065/validate_phase065_step70.py"],
         [invocation(["--content-only"], "PASS_P065_STEP70_CONTENT"), invocation(["--staged"], "PASS_P065_STEP70_STAGED"),
          invocation(["--hardening-selftest"], "PASS_P065_STEP70_HARDENING_SELFTEST")],
         ["--persistence", "--expected-commit", STEP70], "PASS_P065_STEP70_PERSISTENCE"),
    unit("STEP71", STEP71, STEP70, "audit(phase065): trace v1024 code profile defaults",
         "Codex/work/v1024_phase065/validate_phase065_step71.py", "a5986401463b2c7fbe0bbe4ed794ac77880fc1d7a018bca5502954ee190d531a",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json",
          "Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json", "Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md",
          "Codex/work/v1024_phase065/build_phase065_step71.py", "Codex/work/v1024_phase065/validate_phase065_step71.py"],
         [invocation(["--content-only"], "PASS_P065_STEP71_CONTENT"), invocation(["--staged"], "PASS_P065_STEP71_STAGED")],
         ["--persistence", "--expected-commit", STEP71], "PASS_P065_STEP71_PERSISTENCE"),
    unit("STEP72", STEP72, STEP71, "audit(phase065): bound v1024 skew material authority",
         "Codex/work/v1024_phase065/validate_phase065_step72.py", "3de181d55fa46611821c5e53187c24dc40b8e64d75b6883d6bfb8f3572f0ae83",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json",
          "Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md", "Codex/work/v1024_phase065/build_phase065_step72.py",
          "Codex/work/v1024_phase065/validate_phase065_step72.py"],
         [invocation([], "PASS_P065_STEP72_AUTHORITY_WITH_CONCERNS"), invocation(["--staged"], "PASS_P065_STEP72_AUTHORITY_WITH_CONCERNS")],
         ["--persistence", "--expected-commit", STEP72], "PASS_P065_STEP72_PERSISTENCE"),
    unit("STEP73", STEP73, STEP72, "audit(phase065): separate v1024 initialization routes",
         "Codex/work/v1024_phase065/validate_phase065_step73.py", "d47410c3f5e7f7dc4750047c529a8de1eddb00f467d58d47ad7b5416132ad344",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json",
          "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json", "Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md",
          "Codex/work/v1024_phase065/build_phase065_step73.py", "Codex/work/v1024_phase065/validate_phase065_step73.py"],
         [invocation([], "PASS_P065_STEP73_CONTENT"), invocation(["--staged"], "PASS_P065_STEP73_CONTENT")],
         ["--persistence", "--expected-commit", STEP73], "PASS_P065_STEP73_PERSISTENCE"),
    unit("STEP74", STEP74, STEP73, "audit(phase065): adjudicate v1024 doc code guide",
         "Codex/work/v1024_phase065/validate_phase065_step74.py", "1826c9e3a2b22a17500206f4081b0b3ca367128a2780e6f576aab7ff5ce40c7d",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json",
          "Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md", "Codex/work/v1024_phase065/build_phase065_step74.py",
          "Codex/work/v1024_phase065/validate_phase065_step74.py"],
         [invocation(["{STEP74_FIXTURES}"], "PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS")],
         ["{STEP74_FIXTURES}", "--persistence", "--expected-commit", STEP74], "PASS_P065_STEP74_PERSISTENCE", "step74"),
    unit("STEP75_1", STEP75_1, STEP74, "audit(phase065): disposition v1024 lineage",
         "Codex/work/v1024_phase065/validate_phase065_step75_1.py", "16136f5f8d0cd0c504df39c888054c28f91840ee25fddaa66417ff6959edce71",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json",
          "Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json", "Codex/results/PHASE_065_STEP_075_1_DISPOSITION_RESULT.md",
          "Codex/work/v1024_phase065/build_phase065_step75_1.py", "Codex/work/v1024_phase065/validate_phase065_step75_1.py"],
         [invocation(["{STEP75_1_FIXTURES}"], "PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS")],
         ["{STEP75_1_FIXTURES}", "--persistence", "--expected-commit", STEP75_1], "PASS_P065_STEP75_1_PERSISTENCE", "step75_1"),
]


ARTIFACT_SPECS = {
    "Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json": (ACTIVATION, "21153c00a0359a6c77f469e0cb8815df6a06a9fa8bcd3b43525fecb10bb94bd0"),
    "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json": (STEP70, "2cc9eb7a50cde201eabc6247bd18c5449fcc1ebec9ca66caf02d29146af44461"),
    "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json": (STEP70, "08e2529b2a6163d0d87855dea72e30ade2df26c92e024da404fe34776ec37d68"),
    "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json": (STEP71, "571a4b781d292201f07868045d98cbe5f4c2a71a9ca568f66d8bcb6b509d86d9"),
    "Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json": (STEP71, "7d0be484080c9fdbd4f3ffb7247d7d704ed852c3bd2e1ccbdada244a4c9a5b91"),
    "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json": (STEP72, "070fccb26410dd62fcf75e2d251420943229ca7e3cdc2ab0fa66e455d58f40e4"),
    "Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json": (STEP73, "6a8425c8c9e90b88f683c170a19918d70a551efad013ed21ef74f8da7764ddf3"),
    "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json": (STEP73, "d42bda649d2fc6efee7413254ea57519b7434f5433a051f2534a3fc744c8266e"),
    "Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json": (STEP74, "bb8b38f8c882e6fe55497cc06af6109bf72b7ff87798307bf15e8e24d6d85adb"),
    "Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json": (STEP75_1, "8588a5e4b794da355cef7c1c8b21ed13c2cd4a05649679342bad3dc32c188d22"),
    "Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json": (STEP75_1, "33e29ecfa6572277b70c1fc119bc070c9dbb382d9a52932742096ec20605f673"),
}

RESULT_SPECS = {
    "Codex/results/PHASE_065_PLAN_ACTIVATION_RESULT.md": (ACTIVATION, "711d7f24e27fae5c115aeef4b554c1f595c16da893f689ed9c5ec473cc537e3c"),
    "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md": (STEP70, "8ce35af53cf946b92cdacb0f4bb6cd72ac0838f65dda0acddcaf191d8a29ba45"),
    "Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md": (STEP71, "aaadd5822e49991aca492854475832baec244c96d9ffff038818be4130f3d81e"),
    "Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md": (STEP72, "5775360484fbec34b5327001187ea4f66e249bef426ed7ab218650b68c9ea8fc"),
    "Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md": (STEP73, "cc769bec5c658537db2421f77b5b416b680e36f62b017e0e29607d0ad5c621df"),
    "Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md": (STEP74, "c0b6b3fb779f6aff82a753bb5458fca9c608cd7b108a9ef4faa36c869f2be569"),
    "Codex/results/PHASE_065_STEP_075_1_DISPOSITION_RESULT.md": (STEP75_1, "9e3cf1a4a74c7840c2cdc385aa4ef2b27e7a37d8413128eaed7f500df040c585"),
}

EXPECTED_TOP_KEYS = {
    "Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json": "authority controls determinism exact_seven expected_parent expected_subject gate generated_date manifest negative_contract persistence_terminal phase plan process repository runtime_gate_contract schema_version semantic_sha256 status supplemental validator_identity".split(),
    "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json": "authority baseline_commit bindings coverage expected_parent gate generated_date human_evidence_sha256 image_visual output_truncation_rechecks output_truncation_unresolved pdf_visual process_patch_read readers result_path result_sha256_lf schema_version semantic_deferred_intervals semantic_sha256 topology_semantic_sha256 unreviewed_intervals".split(),
    "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json": "authority baseline_commit branch comp_v24 derived_artifacts expected_parent findings generated_date human_evidence_sha256 manifest mirror narrative occurrences phase057_observations process schema_version semantic_sha256 supplemental tex unique_sources".split(),
    "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json": "artifact_kind authority baseline_commit defect_boundaries endpoint_summary endpoints expected_parent feature_routes findings gate generated_date grammar initialization_rows lineage_pairs mirror profile_surfaces route_outcomes schema_version semantic_sha256 source_policy step".split(),
    "Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json": "artifact_kind authority baseline_commit coverage expected_parent finding_summary gate generated_date matrix_semantic_sha256 matrix_sha256_lf result_path result_sha256_lf route_outcomes schema_version semantic_sha256 step unresolved_runtime_routes".split(),
    "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json": "artifact_kind authority baseline_commit bibliographic_conflicts branch consumed_parent_evidence control_source_bindings derivations expected_parent findings gate genealogy generated_date input_routes material_claims metadata_verifications next_gate non_graft schema_version semantic_sha256 source_bindings source_policy tex_census".split(),
    "Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json": "artifact_kind authority_boundary baseline_commit branch consumed_step71 control_source_bindings counts exact_initialization_mapping exact_profile_mapping expected_parent expected_subject feature_observation_owners gate generated_date negative_controls outcome_vocabulary phase profile_runtime_routes result_first_contract routes runtime_attestation_binding schema_version semantic_sha256 source_policy step".split(),
    "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json": "artifact_kind authority_boundary baseline_commit branch changed_order_controls counts expected_parent expected_subject gate generated_date isolation official_runs phase result_first_contract route_runs runtime_environments schema_version semantic_sha256 step".split(),
    "Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json": "artifact_genealogy artifact_kind authority authority_precedence baseline_commit branch conformance_rows control_source_bindings counts expected_parent expected_subject findings gate generated_date input_routes next_gate schema_version semantic_sha256 source_bindings source_policy".split(),
    "Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json": "artifact_kind authority baseline_commit blob_disposition_groups branch control_source_bindings counts expected_parent expected_subject gate inputs phase schema_version semantic_sha256 source_contract source_dispositions step".split(),
    "Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json": "active_obligations artifact_kind authority baseline_commit branch control_source_bindings current_owner_duplicate_check_universe expected_parent expected_subject gate gate_summary inherited_phase064_routes inputs new_phase065_blockers observation_records phase prior_phase064_owner_universe_snapshot schema_version semantic_duplicate_groups semantic_sha256 step".split(),
}


def validate_source_policy_text(source: str, filename: str) -> None:
    tree = ast.parse(source, filename=filename)
    parent_by_node = {
        id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)
    }

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

    def sensitive_callable_reference(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id in {"git", "run_process", "open", "os", "pathlib", "shutil", "subprocess", "sys", "tempfile"}
        if isinstance(node, ast.Call):
            return attribute_chain(node.func) == ("sys", "modules", "get")
        if isinstance(node, ast.Subscript):
            chain = attribute_chain(node.value)
            return bool(chain and (chain[0] in {"os", "pathlib", "shutil", "subprocess", "tempfile"}
                                   or chain == ("sys", "modules")))
        if isinstance(node, ast.Attribute):
            chain = attribute_chain(node)
            return bool(chain and chain[0] in {"subprocess", "os", "pathlib", "shutil", "tempfile"})
        return False

    def default_references_sensitive_callable(node: ast.AST) -> bool:
        return any(sensitive_callable_reference(child) for child in ast.walk(node))

    top_level_function_names = [
        node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    require(len(top_level_function_names) == len(set(top_level_function_names)),
            "E_SOURCE_POLICY_DUPLICATE_OWNER", repr(top_level_function_names))
    owner_by_node: dict[int, str] = {}
    outer_owner_by_node: dict[int, str] = {}

    def assign_scope(node: ast.AST, owner: str, outer_owner: str) -> None:
        owner_by_node[id(node)] = owner
        outer_owner_by_node[id(node)] = outer_owner
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                assign_scope(child, f"<nested:{child.name}>", outer_owner)
            elif isinstance(child, ast.Lambda):
                assign_scope(child, "<lambda>", outer_owner)
            else:
                assign_scope(child, owner, outer_owner)

    for top_level in tree.body:
        if isinstance(top_level, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assign_scope(top_level, top_level.name, top_level.name)
    run_process_owners = {
        "git", "prepare_fixture_args", "configure_fixture_refs", "make_historical_staged_clone",
        "make_historical_persistence_clone", "execute_historical",
    }
    git_call_owners = {
        "configure_fixture_refs", "fresh_historical_precommit", "git_blob", "git_boundary_fixture_snapshot",
        "git_text", "live_tip", "make_git_boundary_fixture", "make_historical_persistence_clone",
        "make_historical_staged_clone", "restore_original_worktree_bytes", "run_git_boundary_controls",
        "status_paths", "step_commit_inventory", "validate_persistence", "validate_staged",
    }
    filesystem_mutation_owners = {
        "remove_temp_tree", "prepare_fixture_args", "restore_original_worktree_bytes",
        "make_historical_staged_clone", "make_historical_persistence_clone", "make_git_boundary_fixture",
        "configure_fixture_refs", "prepare_step70_hardening_state", "run_git_boundary_controls", "atomic_collect",
        "atomic_recollect",
    }
    prohibited_path_methods = {
        "chmod", "hardlink_to", "link_to", "move_into", "open", "rename", "replace", "rmdir", "symlink_to",
        "touch", "write_text",
    }
    subprocess_run_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            defaults = list(node.args.defaults) + [value for value in node.args.kw_defaults if value is not None]
            require(not any(default_references_sensitive_callable(value) for value in defaults),
                    "E_SOURCE_POLICY_DEFAULT", ast.dump(node, include_attributes=False))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            roots = {name.split(".", 1)[0] for name in modules}
            require(roots <= ALLOWED_IMPORT_ROOTS, "E_SOURCE_POLICY_IMPORT_ALLOWLIST", repr(sorted(roots - ALLOWED_IMPORT_ROOTS)))
            require(all(alias.asname is None for alias in node.names),
                    "E_SOURCE_POLICY_IMPORT_ALIAS", ast.dump(node, include_attributes=False))
            require(not (isinstance(node, ast.ImportFrom) and node.module in {
                "os", "pathlib", "shutil", "subprocess", "sys", "tempfile",
            }), "E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM",
                    (node.module if isinstance(node, ast.ImportFrom) else "") or "")
            require(not (isinstance(node, ast.ImportFrom) and node.module == "subprocess"),
                    "E_SOURCE_POLICY_SUBPROCESS", "from subprocess import")
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            require(not sensitive_callable_reference(node.value), "E_SOURCE_POLICY_CALLABLE_ALIAS",
                    ast.dump(node.value, include_attributes=False))
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            owner = owner_by_node.get(id(node))
            outer_owner = outer_owner_by_node.get(id(node))
            parent = parent_by_node.get(id(node))
            allowed_dunder = (
                node.attr == "__setitem__"
                and owner == "<lambda>"
                and outer_owner == "run_negative_controls"
                and isinstance(parent, ast.Call)
                and parent.func is node
            ) or (
                node.attr == "__init__"
                and isinstance(parent, ast.Call)
                and parent.func is node
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "super"
            )
            require(allowed_dunder, "E_SOURCE_POLICY_DYNAMIC_NAMESPACE", node.attr)
        if isinstance(node, ast.Call):
            require(not isinstance(node.func, ast.Lambda), "E_SOURCE_POLICY_DYNAMIC", "lambda call")
            require(not (isinstance(node.func, ast.Name) and node.func.id in {
                "exec", "eval", "__import__", "globals", "locals", "open", "vars",
            }), "E_SOURCE_POLICY_CALL", ast.dump(node.func, include_attributes=False))
            require(not (isinstance(node.func, ast.Name) and node.func.id == "getattr"),
                    "E_SOURCE_POLICY_DYNAMIC", "getattr")
            require(not isinstance(node.func, ast.Subscript), "E_SOURCE_POLICY_DYNAMIC",
                    ast.dump(node.func, include_attributes=False))
            owner = owner_by_node.get(id(node))
            outer_owner = outer_owner_by_node.get(id(node))
            if isinstance(node.func, ast.Name) and node.func.id == "run_process":
                require(owner in run_process_owners, "E_SOURCE_POLICY_PROCESS_OWNER", str(owner))
            if isinstance(node.func, ast.Name) and node.func.id == "git":
                require(owner in git_call_owners or (
                    owner == "<lambda>" and outer_owner == "run_git_boundary_controls"
                ), "E_SOURCE_POLICY_GIT_OWNER", str(owner))
            if isinstance(node.func, ast.Attribute):
                chain = attribute_chain(node.func)
                if chain and chain[0] == "subprocess":
                    require(chain == ("subprocess", "run"), "E_SOURCE_POLICY_SUBPROCESS", ".".join(chain))
                    subprocess_run_calls += 1
                    require(owner == "run_process", "E_SOURCE_POLICY_SUBPROCESS_OWNER", str(owner))
                if chain and chain[0] == "os":
                    require(chain in {("os", "chmod"), ("os", "replace"), ("os", "environ", "copy")},
                            "E_SOURCE_POLICY_OS", ".".join(chain))
                if chain and chain[0] == "shutil":
                    require(chain == ("shutil", "rmtree"), "E_SOURCE_POLICY_SHUTIL", ".".join(chain))
                if chain and chain[0] == "tempfile":
                    require(chain in {("tempfile", "gettempdir"), ("tempfile", "mkdtemp")},
                            "E_SOURCE_POLICY_TEMPFILE", ".".join(chain))
                if chain and chain[0] == "pathlib":
                    require(chain in {("pathlib", "Path"), ("pathlib", "PurePath"), ("pathlib", "PurePosixPath")},
                            "E_SOURCE_POLICY_PATHLIB", ".".join(chain))
                if node.func.attr in prohibited_path_methods:
                    allowed_nonpath = chain in {("os", "chmod"), ("os", "replace")} or (
                        node.func.attr == "replace" and owner in {
                            "lf_bytes", "prepare_step70_hardening_state", "run_negative_controls",
                        }
                    ) or (
                        node.func.attr == "replace"
                        and owner == "<lambda>"
                        and outer_owner == "run_negative_controls"
                    )
                    require(allowed_nonpath, "E_SOURCE_POLICY_FILESYSTEM_API", node.func.attr)
                if node.func.attr in {"write_bytes", "mkdir", "unlink"}:
                    allowed_filesystem_owner = owner in filesystem_mutation_owners or (
                        owner == "<lambda>" and outer_owner == "run_git_boundary_controls"
                    ) or (
                        owner == "<nested:clear_readonly>" and outer_owner == "remove_temp_tree"
                    )
                    require(allowed_filesystem_owner, "E_SOURCE_POLICY_FILESYSTEM_OWNER",
                            f"{owner}:{node.func.attr}")
                if isinstance(node.func.value, ast.Name) and node.func.value.id in {"os", "shutil", "tempfile"} and node.func.attr in {
                    "replace", "unlink", "chmod", "rmtree", "mkdtemp",
                }:
                    allowed_filesystem_owner = owner in filesystem_mutation_owners or (
                        owner == "<lambda>" and outer_owner == "run_git_boundary_controls"
                    ) or (
                        owner == "<nested:clear_readonly>" and outer_owner == "remove_temp_tree"
                    )
                    require(allowed_filesystem_owner, "E_SOURCE_POLICY_FILESYSTEM_OWNER",
                            f"{owner}:{node.func.value.id}.{node.func.attr}")
            for keyword in node.keywords:
                require(not (keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True), "E_SOURCE_POLICY_SHELL", "shell=True")
    require(subprocess_run_calls == 1, "E_SOURCE_POLICY_SUBPROCESS_COUNT", str(subprocess_run_calls))


def validate_source_policy() -> None:
    validate_source_policy_text(VALIDATOR.read_text(encoding="utf-8"), VALIDATOR_PATH)
    historical_validators = {spec["validator"] for spec in UNIT_SPECS}
    require(len(historical_validators) == 7, "E_SOURCE_POLICY_VALIDATOR_ALLOWLIST", repr(sorted(historical_validators)))
    require(all(path.startswith("Codex/work/v1024_phase065/validate_") and "/build_" not in path
                for path in historical_validators), "E_SOURCE_POLICY_VALIDATOR_ALLOWLIST", repr(sorted(historical_validators)))


def load_pinned_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    objects: dict[str, Any] = {}
    machine_records: list[dict[str, Any]] = []
    for path, (commit, expected_sha) in ARTIFACT_SPECS.items():
        raw = git_blob(commit, path)
        require(sha256(raw) == expected_sha, "E_INPUT_SHA", path)
        require((ROOT / path).read_bytes() == raw, "E_INPUT_WORKTREE", path)
        value, traversal = strict_load_bytes(raw, path)
        require(type(value) is dict, "E_INPUT_TYPE", path)
        require(set(value) == set(EXPECTED_TOP_KEYS[path]), "E_INPUT_SCHEMA", path)
        objects[path] = value
        machine_records.append({"path": path, "commit": commit, "sha256": expected_sha, "bytes": len(raw),
                                "physical_lines": len(raw.decode("utf-8").splitlines()), **traversal})
    result_records: list[dict[str, Any]] = []
    for path, (commit, expected_sha) in RESULT_SPECS.items():
        raw = git_blob(commit, path)
        require(sha256(raw) == expected_sha, "E_RESULT_SHA", path)
        require((ROOT / path).read_bytes() == raw, "E_RESULT_WORKTREE", path)
        result_records.append({"path": path, "commit": commit, "sha256": expected_sha, "bytes": len(raw),
                               "physical_lines": len(raw.decode("utf-8").splitlines())})
    require(sum(row["traversal_nodes"] for row in machine_records) == 87180, "E_INPUT_TRAVERSAL_TOTAL")
    require(max(row["max_depth"] for row in machine_records) == 10, "E_INPUT_DEPTH")
    return objects, {"machine_count": 11, "machine_records": machine_records, "result_count": 7,
                      "result_records": result_records, "strict_duplicate_keys": True,
                      "nonfinite_rejected": True, "full_recursive_traversal": True,
                      "traversal_nodes": 87180, "max_depth": 10}


def step_commit_inventory() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        require(git_text(["rev-parse", f"{spec['commit']}^"]) == spec["parent"], "E_UNIT_PARENT", spec["unit"])
        require(git_text(["show", "-s", "--format=%s", spec["commit"]]) == spec["subject"], "E_UNIT_SUBJECT", spec["unit"])
        changed = nul_paths(git(["diff-tree", "--no-commit-id", "--no-renames", "--name-only", "-r", "-z", spec["commit"]]).stdout)
        require(changed == set(spec["paths"]), "E_UNIT_PATHS", spec["unit"])
        validator_raw = git_blob(spec["commit"], spec["validator"])
        require(sha256(validator_raw) == spec["validator_sha256"], "E_UNIT_VALIDATOR_SHA", spec["unit"])
        require(git(["merge-base", "--is-ancestor", spec["commit"], PARENT_COMMIT], check=False).returncode == 0, "E_UNIT_ANCESTRY", spec["unit"])
        records.append({"unit": spec["unit"], "commit": spec["commit"], "parent": spec["parent"], "subject": spec["subject"],
                        "path_count": len(spec["paths"]), "paths": sorted(spec["paths"]), "validator_path": spec["validator"],
                        "validator_sha256": spec["validator_sha256"], "in_active_ancestry": True})
    return records


def repository_snapshot(*, allow_final_dirt: bool) -> dict[str, Any]:
    branch = git_text(["branch", "--show-current"])
    head = git_text(["rev-parse", "HEAD"])
    upstream_name = git_text(["rev-parse", "--abbrev-ref", "@{upstream}"])
    upstream = git_text(["rev-parse", "@{upstream}"])
    tracking = git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"])
    live = live_tip(ACTIVE_BRANCH)
    local_protected = git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"])
    tracked_protected = git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"])
    live_protected = live_tip(PROTECTED_BRANCH)
    tracked_main = git_text(["rev-parse", "refs/remotes/origin/main"])
    live_main = live_tip("main")
    dirt = status_paths()
    require(branch == ACTIVE_BRANCH, "E_ACTIVE_BRANCH", branch)
    require(upstream_name == f"origin/{ACTIVE_BRANCH}", "E_UPSTREAM_NAME", upstream_name)
    require(head == upstream == tracking == live, "E_ACTIVE_REMOTE", f"{head}/{upstream}/{tracking}/{live}")
    require(local_protected == tracked_protected == live_protected == PROTECTED_TIP, "E_PROTECTED_DRIFT", f"{local_protected}/{tracked_protected}/{live_protected}")
    require(tracked_main == live_main == MAIN_TIP, "E_MAIN_DRIFT", f"{tracked_main}/{live_main}")
    if allow_final_dirt:
        require(not (dirt - FINAL_PATH_SET), "E_EXTRA_DIRT", repr(sorted(dirt - FINAL_PATH_SET)))
    else:
        require(not dirt, "E_PERSISTENCE_DIRTY", repr(sorted(dirt)))
    claude_tracked = git_text(["diff", "--no-renames", "--name-only", PARENT_COMMIT, "--", "Claude"]).splitlines()
    claude_untracked = git_text(["ls-files", "--others", "--exclude-standard", "--", "Claude"]).splitlines()
    require(not claude_tracked and not claude_untracked, "E_CLAUDE_DRIFT", repr(claude_tracked + claude_untracked))
    return {"branch": branch, "head": head, "upstream_name": upstream_name, "upstream": upstream,
            "origin_active": tracking, "live_active": live, "local_protected": local_protected,
            "origin_protected": tracked_protected, "live_protected": live_protected,
            "origin_main": tracked_main, "live_main": live_main, "only_final_allowlist_dirty": True,
            "claude_tracked_diff_count": 0, "claude_untracked_count": 0}


def stable_repository_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(snapshot)
    for key in ("head", "upstream", "origin_active", "live_active"):
        require(re.fullmatch(r"[0-9a-f]{40}", projected[key]) is not None, "E_REPOSITORY_PROJECTION", key)
        projected[key] = "<OPERATIONAL_ACTIVE_COMMIT_MASKED>"
    projected["operational_active_commit_masked"] = True
    return projected


def remove_temp_tree(path: pathlib.Path, prefix: str) -> None:
    resolved = path.resolve()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    require(resolved.parent == temp_root and resolved.name.startswith(prefix), "E_TEMP_BOUNDARY", str(resolved))

    def clear_readonly(function: Callable[..., Any], target: str, _: Any) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(resolved, onerror=clear_readonly)
    require(not resolved.exists(), "E_TEMP_CLEANUP", str(resolved))


def subordinate_python() -> str:
    executable = sys.executable
    require(pathlib.Path(executable).is_file(), "E_SUBORDINATE_RUNTIME", executable)
    return executable


def historical_environment(clone: pathlib.Path) -> dict[str, str]:
    environment = os.environ.copy()
    environment["PATH"] = str(clone.parent) + os.pathsep + environment.get("PATH", "")
    environment["PHASE065_FIXTURE_ORIGIN"] = str(clone.parent / "origin.git")
    return environment


def prepare_fixture_args(executable: str, clone: pathlib.Path, spec: dict[str, Any]) -> tuple[list[str], pathlib.Path | None, str | None]:
    fixture = spec["fixture"]
    if fixture is None:
        return [], None, None
    if fixture == "step74":
        prefix = "p065-step74-final-fixtures"
        root = pathlib.Path(tempfile.gettempdir()).resolve() / prefix
        if root.exists():
            remove_temp_tree(root, prefix)
        root.mkdir()
        one = root / "matrix-step74-one.json"
        two = root / "matrix-step74-two.json"
        sentinel = root / "not-a-matrix-name.json"
        builder = "Codex/work/v1024_phase065/build_phase065_step74.py"
        for output in (one, two):
            process = run_process([executable, builder, "--output", str(output)], cwd=clone, timeout=2400,
                                  env=historical_environment(clone))
            require(process.returncode == 0 and b"PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS" in process.stdout,
                    "E_STEP74_FIXTURE_BUILD", process.stderr.decode("utf-8", errors="replace")[-1200:])
        sentinel.write_bytes(b"P065_STEP74_SENTINEL\n")
        return ["--determinism-one", str(one), "--determinism-two", str(two),
                "--output-sentinel", str(sentinel),
                "--expected-builder-sha256", "7d4c287758b7aec1ad44b175679c3f6ea88e05584339f434081d7d61dba00be5",
                "--expected-validator-sha256", "1826c9e3a2b22a17500206f4081b0b3ca367128a2780e6f576aab7ff5ce40c7d",
                "--expected-matrix-sha256", "bb8b38f8c882e6fe55497cc06af6109bf72b7ff87798307bf15e8e24d6d85adb"], root, prefix
    require(fixture == "step75_1", "E_FIXTURE_KIND", str(fixture))
    prefix = "p065-step75_1-fixtures"
    root = pathlib.Path(tempfile.gettempdir()).resolve() / prefix
    if root.exists():
        remove_temp_tree(root, prefix)
    root.mkdir()
    d1, d2 = root / "source-disposition-one.json", root / "source-disposition-two.json"
    c1, c2 = root / "carry-forward-one.json", root / "carry-forward-two.json"
    builder = "Codex/work/v1024_phase065/build_phase065_step75_1.py"
    for disposition, carry in ((d1, c1), (d2, c2)):
        process = run_process([executable, builder, "--disposition", str(disposition), "--carry", str(carry)],
                              cwd=clone, timeout=2400, env=historical_environment(clone))
        require(process.returncode == 0 and b"PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS" in process.stdout,
                "E_STEP75_1_FIXTURE_BUILD", process.stderr.decode("utf-8", errors="replace")[-1200:])
    return ["--disposition-one", str(d1), "--disposition-two", str(d2),
            "--carry-one", str(c1), "--carry-two", str(c2),
            "--expected-builder-sha256", "344dbc0a9bb93518e5b30dd78667749754cd15c636ebabced62aeb8ab299552a",
            "--expected-validator-sha256", "16136f5f8d0cd0c504df39c888054c28f91840ee25fddaa66417ff6959edce71",
            "--expected-disposition-sha256", "8588a5e4b794da355cef7c1c8b21ed13c2cd4a05649679342bad3dc32c188d22",
            "--expected-carry-sha256", "33e29ecfa6572277b70c1fc119bc070c9dbb382d9a52932742096ec20605f673"], root, prefix


def expanded_args(template: list[str], fixture_args: list[str]) -> list[str]:
    output: list[str] = []
    for item in template:
        if item in {"{STEP74_FIXTURES}", "{STEP75_1_FIXTURES}"}:
            output.extend(fixture_args)
        else:
            output.append(item)
    return output


def normalize_recorded_arg(argument: str) -> str:
    candidate = pathlib.Path(argument)
    if not candidate.is_absolute():
        return argument
    try:
        relative = candidate.resolve().relative_to(pathlib.Path(tempfile.gettempdir()).resolve())
    except (OSError, ValueError):
        return argument
    suffix = relative.as_posix()
    return "<TEMP>" if not suffix else f"<TEMP>/{suffix}"


def expected_recorded_fixture_args(spec: dict[str, Any]) -> list[str]:
    if spec["fixture"] is None:
        return []
    if spec["fixture"] == "step74":
        root = "<TEMP>/p065-step74-final-fixtures"
        return ["--determinism-one", f"{root}/matrix-step74-one.json",
                "--determinism-two", f"{root}/matrix-step74-two.json",
                "--output-sentinel", f"{root}/not-a-matrix-name.json",
                "--expected-builder-sha256", "7d4c287758b7aec1ad44b175679c3f6ea88e05584339f434081d7d61dba00be5",
                "--expected-validator-sha256", "1826c9e3a2b22a17500206f4081b0b3ca367128a2780e6f576aab7ff5ce40c7d",
                "--expected-matrix-sha256", "bb8b38f8c882e6fe55497cc06af6109bf72b7ff87798307bf15e8e24d6d85adb"]
    require(spec["fixture"] == "step75_1", "E_FIXTURE_KIND", str(spec["fixture"]))
    root = "<TEMP>/p065-step75_1-fixtures"
    return ["--disposition-one", f"{root}/source-disposition-one.json",
            "--disposition-two", f"{root}/source-disposition-two.json",
            "--carry-one", f"{root}/carry-forward-one.json",
            "--carry-two", f"{root}/carry-forward-two.json",
            "--expected-builder-sha256", "344dbc0a9bb93518e5b30dd78667749754cd15c636ebabced62aeb8ab299552a",
            "--expected-validator-sha256", "16136f5f8d0cd0c504df39c888054c28f91840ee25fddaa66417ff6959edce71",
            "--expected-disposition-sha256", "8588a5e4b794da355cef7c1c8b21ed13c2cd4a05649679342bad3dc32c188d22",
            "--expected-carry-sha256", "33e29ecfa6572277b70c1fc119bc070c9dbb382d9a52932742096ec20605f673"]


def historical_invocation_requires_stage(spec: dict[str, Any], args: list[str]) -> bool:
    return "--verify-staged" in args or "--staged" in args or spec["unit"] in {
        "STEP72", "STEP73", "STEP74", "STEP75_1",
    }


def configure_fixture_refs(clone: pathlib.Path, active_tip: str, origin: pathlib.Path) -> None:
    git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", active_tip], cwd=clone)
    git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=clone)
    git(["update-ref", "refs/remotes/origin/main", MAIN_TIP], cwd=clone)
    git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=clone)
    git(["update-ref", "-d", "refs/heads/main"], cwd=clone)
    process = run_process(["git", "clone", "--bare", "--shared", str(ROOT), str(origin)], cwd=origin.parent, timeout=300)
    require(process.returncode == 0, "E_FIXTURE_ORIGIN_INIT", process.stderr.decode("utf-8", errors="replace"))
    for branch, tip in ((ACTIVE_BRANCH, active_tip), (PROTECTED_BRANCH, PROTECTED_TIP), ("main", MAIN_TIP)):
        process = run_process(["git", "--git-dir", str(origin), "update-ref", f"refs/heads/{branch}", tip], cwd=origin.parent)
        require(process.returncode == 0, "E_FIXTURE_ORIGIN_REF", branch)
    helper = origin.parent / "git-remote-phase065"
    helper.write_bytes(REMOTE_HELPER_BYTES)
    os.chmod(helper, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    git(["remote", "set-url", "origin", ORIGIN_IDENTITY_URL], cwd=clone)
    git(["config", "remote.origin.vcs", "phase065"], cwd=clone)
    git(["branch", "--set-upstream-to", f"origin/{ACTIVE_BRANCH}", ACTIVE_BRANCH], cwd=clone)


def restore_original_worktree_bytes(clone: pathlib.Path, commit: str, excluded: set[str]) -> dict[str, str]:
    listed = git(["ls-tree", "-r", "--name-only", commit], cwd=clone).stdout.decode("utf-8").splitlines()
    changed_after_commit = set(git_text(["diff", "--no-renames", "--name-only", commit, PARENT_COMMIT]).splitlines())
    dirty_now = set(git_text(["diff", "--no-renames", "--name-only"]).splitlines()) | set(git_text(["diff", "--cached", "--no-renames", "--name-only"]).splitlines())
    restored: dict[str, str] = {}
    for path in listed:
        if path in excluded or pathlib.PurePosixPath(path).suffix.lower() != ".json":
            continue
        source = ROOT / path
        target = clone / path
        if path not in changed_after_commit and path not in dirty_now and source.is_file() and target.is_file():
            raw = source.read_bytes()
            target.write_bytes(raw)
            restored[path] = sha256(raw)
    return restored


def make_historical_staged_clone(spec: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    prefix = f"phase065-step752-stage-{spec['unit'].lower()}-"
    parent = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    clone = parent / "repo"
    process = run_process(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], timeout=300)
    require(process.returncode == 0, "E_FIXTURE_CLONE", process.stderr.decode("utf-8", errors="replace"))
    try:
        git(["config", "core.autocrlf", "true"], cwd=clone)
        git(["checkout", "-B", ACTIVE_BRANCH, spec["parent"]], cwd=clone)
        configure_fixture_refs(clone, spec["parent"], parent / "origin.git")
        git(["checkout", spec["commit"], "--", *spec["paths"]], cwd=clone, timeout=600)
        restored = restore_original_worktree_bytes(clone, spec["commit"], set(spec["paths"]))
        for path in spec["paths"]:
            (clone / path).write_bytes(git_blob(spec["commit"], path, cwd=clone))
        if restored:
            git(["update-index", "--assume-unchanged", "--", *sorted(restored)], cwd=clone)
        git(["reset", "--", *spec["paths"]], cwd=clone)
        expected_initial = set(spec["paths"])
        if spec["unit"] == "ACTIVATION":
            activation_artifact = clone / "Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json"
            activation_artifact.unlink()
            expected_initial.remove("Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json")
        require(not nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=clone).stdout),
                "E_FIXTURE_PREMATURE_STAGE", spec["unit"])
        require(status_paths(clone) == expected_initial, "E_FIXTURE_INITIAL_DIRT", spec["unit"])
        require(git_text(["rev-parse", "HEAD"], cwd=clone) == spec["parent"], "E_FIXTURE_PARENT", spec["unit"])
        require(live_tip(ACTIVE_BRANCH, cwd=clone, env=historical_environment(clone)) == spec["parent"],
                "E_FIXTURE_LIVE", spec["unit"])
    except Exception:
        remove_temp_tree(parent, prefix)
        raise
    return parent, clone, restored


def make_historical_persistence_clone(spec: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    prefix = f"phase065-step752-persist-{spec['unit'].lower()}-"
    parent = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    clone = parent / "repo"
    process = run_process(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], timeout=300)
    require(process.returncode == 0, "E_PERSISTENCE_CLONE", process.stderr.decode("utf-8", errors="replace"))
    try:
        git(["config", "core.autocrlf", "true"], cwd=clone)
        git(["checkout", "-B", ACTIVE_BRANCH, spec["commit"]], cwd=clone)
        configure_fixture_refs(clone, spec["commit"], parent / "origin.git")
        restored = restore_original_worktree_bytes(clone, spec["commit"], set(spec["paths"]))
        for path in spec["paths"]:
            raw = git_blob(spec["commit"], path, cwd=clone)
            (clone / path).write_bytes(raw)
            restored[path] = sha256(raw)
        if restored:
            git(["update-index", "--assume-unchanged", "--", *sorted(restored)], cwd=clone)
        require(not status_paths(clone), "E_PERSISTENCE_FIXTURE_DIRT", spec["unit"])
    except Exception:
        remove_temp_tree(parent, prefix)
        raise
    return parent, clone, restored


def prepare_step70_hardening_state(clone: pathlib.Path) -> None:
    replacements = {
        "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md": (
            ("Status: `PASS_PENDING_PERSISTENCE`", "Status: `IN_PROGRESS_RESULT_FIRST`"),
            ("Current Step 70 gate: `PASS_P065_STEP70_PRECOMMIT`; commit/push persistence is pending.",
             "Current Step 70 gate: `IN_PROGRESS_RESULT_FIRST`."),
        ),
        PARENT_LEDGER_PATH: (
            ("detailed-plan activation persisted; Step 70 precommit validation complete; Steps 71–75 pending",
             "detailed-plan activation persisted; Step 70 result-first evidence collection and validator hardening in progress; Steps 71–75 pending"),
            ("`PASS_P065_STEP70_PRECOMMIT`; `PASS_PENDING_PERSISTENCE`",
             "`IN_PROGRESS_RESULT_FIRST`; evidence pending"),
            ("exact-eight Step 70 commit/push/persistence, then Step 71",
             "finish complete-read/visual evidence, then JSON-last collection and dual-runtime validation"),
        ),
        ACTIVE_LEDGER_PATH: (
            ("detailed-plan activation persisted; Step 70 precommit validation complete; Steps 71–75 pending",
             "detailed-plan activation persisted; Step 70 result-first evidence collection and validator hardening in progress; Steps 71–75 pending"),
            ("`PASS_P065_STEP70_PRECOMMIT`; `PASS_PENDING_PERSISTENCE`",
             "`IN_PROGRESS_RESULT_FIRST`; no Step 70 PASS selected"),
            ("exact-eight Step 70 commit/push/persistence, then Step 71",
             "finish complete-read/visual evidence, collect JSONs last, then dual-runtime staged validation"),
        ),
        HANDOVER_PATH: (
            ("17. 현재 Phase 상태: Phase 065 `IN_PROGRESS`, Current checkpoint: Step 70 `PASS_PENDING_PERSISTENCE`",
             "17. 현재 Phase 상태: Phase 065 `IN_PROGRESS`, Current checkpoint: Step 70 `IN_PROGRESS_RESULT_FIRST`"),
            ("after persistence execute Step 71",
             "integrate complete-read/visual evidence, collect JSONs last, validate and persist before Step 71"),
        ),
    }
    for path, substitutions in replacements.items():
        target = clone / path
        text = target.read_text(encoding="utf-8")
        for old, new in substitutions:
            require(text.count(old) == 1, "E_STEP70_HARDENING_RECONSTRUCTION", f"{path}:{old}")
            text = text.replace(old, new)
        target.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
    for path in (
        "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json",
        "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json",
    ):
        target = clone / path
        require(target.is_file(), "E_STEP70_HARDENING_RECONSTRUCTION", path)
        target.unlink()


def validate_historical_output(stdout: str, stderr: str, terminal: str, unit_name: str) -> list[str]:
    lines = stdout.splitlines()
    terminal_lines = [
        line for line in lines
        if line == terminal or line.startswith(terminal + " ") or (terminal.endswith("=") and line.startswith(terminal))
    ]
    require(len(terminal_lines) == 1, "E_HISTORICAL_TERMINAL", f"{unit_name}:{terminal}:{terminal_lines!r}")
    banners = [line for line in lines if line.startswith(("PASS", "FAIL"))]
    require(banners and all(line.startswith("PASS_") for line in banners), "E_HISTORICAL_BANNER", f"{unit_name}:{banners!r}")
    require(stderr == "", "E_HISTORICAL_STDERR", f"{unit_name}:{stderr[-1200:]}")
    return banners


def execute_historical(executable: str, clone: pathlib.Path, spec: dict[str, Any], args: list[str], terminal: str, location: str) -> dict[str, Any]:
    raw = (clone / spec["validator"]).read_bytes()
    require(sha256(raw) == spec["validator_sha256"], "E_HISTORICAL_VALIDATOR_SHA", spec["unit"])
    process = run_process([executable, spec["validator"], *args], cwd=clone, timeout=3600,
                          env=historical_environment(clone))
    stdout = process.stdout.decode("utf-8", errors="replace")
    stderr = process.stderr.decode("utf-8", errors="replace")
    require(process.returncode == 0, "E_HISTORICAL_EXIT", f"{spec['unit']}:{stdout[-1600:]}:{stderr[-1600:]}")
    banners = validate_historical_output(stdout, stderr, terminal, spec["unit"])
    return {"unit": spec["unit"], "commit": spec["commit"], "validator_path": spec["validator"],
            "validator_sha256": spec["validator_sha256"], "args": [normalize_recorded_arg(item) for item in args],
            "terminal_prefix": terminal,
            "terminal_count": 1, "exit_code": 0, "stderr_bytes": len(process.stderr),
            "stdout_lf_bytes": len(lf_bytes(process.stdout)), "stdout_lf_sha256": sha256(lf_bytes(process.stdout)),
            "banners": banners,
            "execution_location": location, "python_version": "CURRENT_OUTER_RUNTIME"}


def require_restored_inputs_unchanged(clone: pathlib.Path, restored: dict[str, str], unit_name: str) -> None:
    for path, expected in restored.items():
        require(sha256((clone / path).read_bytes()) == expected, "E_HISTORICAL_RESTORED_INPUT_MUTATION", f"{unit_name}:{path}")


def fresh_historical_precommit() -> dict[str, Any]:
    executable = subordinate_python()
    before = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        parent, clone, restored = make_historical_staged_clone(spec)
        prefix = f"phase065-step752-stage-{spec['unit'].lower()}-"
        fixture_root: pathlib.Path | None = None
        fixture_prefix: str | None = None
        try:
            if spec["unit"] in {"STEP74", "STEP75_1"}:
                git(["add", "--", *spec["paths"]], cwd=clone)
            fixture_args, fixture_root, fixture_prefix = prepare_fixture_args(executable, clone, spec)
            for current in spec["invocations"]:
                args = expanded_args(current["args"], fixture_args)
                if spec["unit"] == "STEP70" and args == ["--hardening-selftest"]:
                    hardening_parent, hardening_clone, hardening_restored = make_historical_staged_clone(spec)
                    hardening_prefix = "phase065-step752-stage-step70-"
                    try:
                        prepare_step70_hardening_state(hardening_clone)
                        records.append(execute_historical(
                            executable, hardening_clone, spec, args, current["terminal_prefix"],
                            "DISPOSABLE_RECONSTRUCTED_STEP70_PRE_EVIDENCE_CLONE",
                        ))
                        require_restored_inputs_unchanged(hardening_clone, hardening_restored, spec["unit"])
                    finally:
                        remove_temp_tree(hardening_parent, hardening_prefix)
                    continue
                if historical_invocation_requires_stage(spec, args):
                    git(["add", "--", *spec["paths"]], cwd=clone)
                records.append(execute_historical(executable, clone, spec, args, current["terminal_prefix"],
                                                  "DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE"))
            require_restored_inputs_unchanged(clone, restored, spec["unit"])
            require(nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=clone).stdout) == set(spec["paths"]), "E_HISTORICAL_STAGE_MUTATION", spec["unit"])
            require(not nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=clone).stdout), "E_HISTORICAL_WORKTREE_MUTATION", spec["unit"])
        finally:
            if fixture_root is not None and fixture_prefix is not None and fixture_root.exists():
                remove_temp_tree(fixture_root, fixture_prefix)
            remove_temp_tree(parent, prefix)
    after = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    require(canonical_bytes(before) == canonical_bytes(after), "E_ACTIVE_MUTATION", "precommit replay")
    require(len(records) == 14, "E_PRECOMMIT_COUNT", str(len(records)))
    return {"unit_count": 7, "invocation_count": 14, "pass_count": 14, "records": records,
            "historical_exact_staged_context": True, "cleanup_pass_count": 7, "active_repository_unchanged": True}


def fresh_historical_persistence() -> dict[str, Any]:
    executable = subordinate_python()
    before = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        parent, clone, restored = make_historical_persistence_clone(spec)
        prefix = f"phase065-step752-persist-{spec['unit'].lower()}-"
        fixture_root: pathlib.Path | None = None
        fixture_prefix: str | None = None
        try:
            fixture_args, fixture_root, fixture_prefix = prepare_fixture_args(executable, clone, spec)
            args = expanded_args(spec["persistence_args"], fixture_args)
            records.append(execute_historical(executable, clone, spec, args, spec["persistence_terminal"],
                                               "DISPOSABLE_CLEAN_HISTORICAL_PERSISTENCE_CLONE"))
            require_restored_inputs_unchanged(clone, restored, spec["unit"])
            require(not status_paths(clone), "E_HISTORICAL_PERSISTENCE_MUTATION", spec["unit"])
        finally:
            if fixture_root is not None and fixture_prefix is not None and fixture_root.exists():
                remove_temp_tree(fixture_root, fixture_prefix)
            remove_temp_tree(parent, prefix)
    after = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    require(canonical_bytes(before) == canonical_bytes(after), "E_ACTIVE_MUTATION", "persistence replay")
    return {"unit_count": 7, "invocation_count": 7, "pass_count": 7, "records": records,
            "historical_clean_persistence_context": True, "cleanup_pass_count": 7,
            "active_repository_unchanged": True}


def validate_reused_historical_evidence(document: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], int]:
    require(set(document) == FINAL_TOP_KEYS, "E_RECOLLECT_DOCUMENT_SCHEMA", repr(sorted(document)))
    require((document["phase"], document["step"], document["gate"], document["status"],
             document["expected_parent"], document["expected_subject"])
            == ("065", "75.2", GATE, STATUS, PARENT_COMMIT, SUBJECT),
            "E_RECOLLECT_DOCUMENT_IDENTITY", "stored artifact")
    require(document["exact_eight"] == {"count": 8, "paths": FINAL_PATHS, "result_first": True, "json_last": True},
            "E_RECOLLECT_DOCUMENT_ALLOWLIST", "stored artifact")
    historical = document.get("historical_execution")
    require(type(historical) is dict and set(historical) == {
        "invocation_count", "pass_count", "persistence", "precommit", "unit_count",
    }, "E_RECOLLECT_HISTORICAL_SCHEMA", "historical_execution")
    require((historical["unit_count"], historical["invocation_count"], historical["pass_count"])
            == (7, 21, 21), "E_RECOLLECT_HISTORICAL_COUNTS", repr(historical))

    precommit_sequence = [
        (spec, current["args"], current["terminal_prefix"])
        for spec in UNIT_SPECS for current in spec["invocations"]
    ]
    persistence_sequence = [
        (spec, spec["persistence_args"], spec["persistence_terminal"])
        for spec in UNIT_SPECS
    ]
    record_keys = {
        "args", "banners", "commit", "execution_location", "exit_code", "python_version",
        "stderr_bytes", "stdout_lf_bytes", "stdout_lf_sha256", "terminal_count", "terminal_prefix",
        "unit", "validator_path", "validator_sha256",
    }

    def validate_block(name: str, sequence: list[tuple[dict[str, Any], list[str], str]]) -> tuple[dict[str, Any], int]:
        block = historical[name]
        context_key = "historical_exact_staged_context" if name == "precommit" else "historical_clean_persistence_context"
        require(type(block) is dict and set(block) == {
            "active_repository_unchanged", "cleanup_pass_count", context_key,
            "invocation_count", "pass_count", "records", "unit_count",
        }, "E_RECOLLECT_HISTORICAL_SCHEMA", name)
        expected_count = len(sequence)
        require((block["unit_count"], block["invocation_count"], block["pass_count"],
                 block["cleanup_pass_count"], block["active_repository_unchanged"], block[context_key])
                == (7, expected_count, expected_count, 7, True, True),
                "E_RECOLLECT_HISTORICAL_COUNTS", name)
        require(type(block["records"]) is list and len(block["records"]) == expected_count,
                "E_RECOLLECT_HISTORICAL_COUNTS", f"{name}:records")
        normalized = copy.deepcopy(block)
        normalized_count = 0
        for index, (record, (spec, template, terminal)) in enumerate(zip(normalized["records"], sequence, strict=True)):
            require(type(record) is dict and set(record) == record_keys,
                    "E_RECOLLECT_RECORD_SCHEMA", f"{name}:{index}")
            require(type(record["args"]) is list and all(type(item) is str for item in record["args"]),
                    "E_RECOLLECT_RECORD_ARGS", f"{name}:{index}")
            recorded_args = [normalize_recorded_arg(item) for item in record["args"]]
            normalized_count += sum(before != after for before, after in zip(record["args"], recorded_args, strict=True))
            record["args"] = recorded_args
            expected_args = expanded_args(template, expected_recorded_fixture_args(spec))
            require(recorded_args == expected_args, "E_RECOLLECT_RECORD_ARGS", f"{name}:{index}")
            expected_location = (
                "DISPOSABLE_RECONSTRUCTED_STEP70_PRE_EVIDENCE_CLONE"
                if name == "precommit" and spec["unit"] == "STEP70" and template == ["--hardening-selftest"]
                else "DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE"
                if name == "precommit"
                else "DISPOSABLE_CLEAN_HISTORICAL_PERSISTENCE_CLONE"
            )
            require((record["unit"], record["commit"], record["validator_path"],
                     record["validator_sha256"], record["terminal_prefix"], record["terminal_count"],
                     record["exit_code"], record["stderr_bytes"], record["execution_location"],
                     record["python_version"])
                    == (spec["unit"], spec["commit"], spec["validator"], spec["validator_sha256"], terminal,
                        1, 0, 0, expected_location, "CURRENT_OUTER_RUNTIME"),
                    "E_RECOLLECT_RECORD_IDENTITY", f"{name}:{index}")
            require(type(record["stdout_lf_bytes"]) is int and record["stdout_lf_bytes"] > 0
                    and re.fullmatch(r"[0-9a-f]{64}", record["stdout_lf_sha256"]) is not None,
                    "E_RECOLLECT_RECORD_STDOUT", f"{name}:{index}")
            require(type(record["banners"]) is list and record["banners"]
                    and all(type(banner) is str and banner.startswith("PASS_") for banner in record["banners"]),
                    "E_RECOLLECT_RECORD_BANNERS", f"{name}:{index}")
            terminal_matches = [banner for banner in record["banners"] if banner == terminal
                                or banner.startswith(terminal + " ")
                                or (terminal.endswith("=") and banner.startswith(terminal))]
            require(len(terminal_matches) == 1, "E_RECOLLECT_RECORD_TERMINAL", f"{name}:{index}")
        return normalized, normalized_count

    normalized_precommit, precommit_normalized = validate_block("precommit", precommit_sequence)
    normalized_persistence, persistence_normalized = validate_block("persistence", persistence_sequence)
    return normalized_precommit, normalized_persistence, precommit_normalized + persistence_normalized


def independent_numeric_checks() -> dict[str, Any]:
    current_a = 2.0
    capacity_ah = 2.0
    capacity_c = 3600.0 * capacity_ah
    normalized_rate_h = current_a / capacity_ah
    normalized_rate_s = current_a / capacity_c
    require(normalized_rate_h == 1.0 and abs(normalized_rate_s - 1.0 / 3600.0) < 1e-18,
            "E_NUMERIC_TIMEBASE", repr((normalized_rate_h, normalized_rate_s)))
    require(abs(normalized_rate_h / normalized_rate_s - 3600.0) < 1e-9,
            "E_NUMERIC_TIMEBASE_FACTOR", repr(normalized_rate_h / normalized_rate_s))

    omega_x = 125.0
    length_v = 0.006
    transfer = 1.0 / complex(1.0, omega_x * length_v)
    require(abs(transfer.real - 0.64) < 1e-15 and abs(transfer.imag + 0.48) < 1e-15,
            "E_NUMERIC_TRANSFER", repr(transfer))
    require(abs(abs(transfer) - 0.8) < 1e-15, "E_NUMERIC_TRANSFER_MAGNITUDE", repr(abs(transfer)))

    sigma = 2.5
    radial_position = 7.0
    field_coupling = 0.4
    orientation = -0.3
    corrected = math.exp(field_coupling * sigma * orientation)
    superseded = math.exp(field_coupling * radial_position * orientation)
    require(corrected != superseded, "E_NUMERIC_EQ38_SEPARATION", repr((corrected, superseded)))
    return {
        "c_rate_timebase": {"current_A": current_a, "capacity_Ah": capacity_ah, "capacity_C": capacity_c,
                            "normalized_rate_h^-1": normalized_rate_h, "normalized_rate_s^-1": normalized_rate_s,
                            "hour_to_second_factor": 3600},
        "voltage_coordinate_transfer": {"omega_x_V^-1": omega_x, "L0_V": length_v,
                                        "H_real": transfer.real, "H_imag": transfer.imag, "H_magnitude": abs(transfer)},
        "equation38_witness": {"K": field_coupling, "sigma": sigma, "r": radial_position, "mu": orientation,
                               "exp_K_sigma_mu": corrected, "exp_K_r_mu": superseded, "distinct": True},
        "independent_implementation": True,
    }


def integrated_contracts(objects: dict[str, Any]) -> dict[str, Any]:
    activation = objects["Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json"]
    read = objects["Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json"]
    topology = objects["Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json"]
    static = objects["Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"]
    static_att = objects["Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json"]
    science = objects["Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json"]
    initialization = objects["Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json"]
    runtime = objects["Codex/results/PHASE_065_RUNTIME_ATTESTATION.json"]
    conformance = objects["Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json"]
    disposition = objects["Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json"]
    carry = objects["Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json"]

    def counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
        output: dict[str, int] = {}
        for row in rows:
            value = str(row[key])
            output[value] = output.get(value, 0) + 1
        return output

    require(activation["gate"] == "PASS_P065_PLAN_ACTIVATION", "E_ACTIVATION_GATE")
    manifest = topology["manifest"]
    occurrences = topology["occurrences"]
    unique_sources = topology["unique_sources"]
    require(len(occurrences) == manifest["occurrences"] == 261, "E_SOURCE_OCCURRENCES")
    require(len({row["path"] for row in occurrences}) == manifest["unique_paths"] == 261, "E_SOURCE_PATHS")
    require(len(unique_sources) == manifest["unique_blobs"] == len({row["blob"] for row in occurrences}) == 131,
            "E_SOURCE_BLOBS")
    require(manifest["versions"] == {"v1.0.24": 130, "v1.0.24.1": 131}, "E_SOURCE_VERSIONS")
    require(manifest["unique_review_modes"] == {"FULL_IMAGE": 3, "FULL_PDF": 3, "FULL_TEXT": 125},
            "E_SOURCE_REVIEW_MODES")
    require((manifest["unique_text_lines"], manifest["unique_bytes"], manifest["occurrence_bytes"])
            == (21618, 7812647, 15622368), "E_SOURCE_EXTENTS")
    require(topology["mirror"]["byte_identical_pairs"] == 130
            and topology["mirror"]["independent_corroboration"] is False
            and topology["mirror"]["v1024_1_only"] == ["ARCHIVE_NOTE.md"], "E_MIRROR_ARCHIVE")
    require({row["relative_path"] for row in topology["mirror"]["pairs"]} | {"ARCHIVE_NOTE.md"}
            == {path.removeprefix("Claude/docs/v1.0.24.1/") for path in
                (row["path"] for row in occurrences if row["version"] == "v1.0.24.1")},
            "E_MIRROR_PATH_SET")

    coverage = read["coverage"]
    require(coverage["unique_sources"] == {"read": 131, "required": 131}, "E_READ_UNIQUE")
    require(coverage["text"] == {"blobs": 125, "lines": 21618}, "E_READ_TEXT")
    require(coverage["pdf"] == {"documents": 3, "pages_extracted": 148, "pages_rendered": 148, "pages_visual": 148},
            "E_READ_PDF")
    require(coverage["image"] == {"images": 3, "original_resolution_visual": 3}, "E_READ_IMAGE")
    require(coverage["supplemental"] == {"documents": 6, "lines": 728}, "E_READ_SUPPLEMENTAL")
    require(coverage["narrative"] == {"documents": 74, "lines": 7470}, "E_READ_NARRATIVE")
    require(read["unreviewed_intervals"] == [] and read["output_truncation_unresolved"] == [],
            "E_READ_GAPS")
    require(len(read["semantic_deferred_intervals"]) == 3, "E_READ_DEFERRED")
    require(topology["narrative"]["copied_activation_claim"]["lines"] == 2068
            and topology["narrative"]["corrected_root_process"]["lines"] == 2306
            and topology["narrative"]["correction_delta_lines"] == 238, "E_NARRATIVE_CORRECTION")
    require(topology["comp_v24"]["extension_counts"] == {"csv": 10, "json": 16, "md": 31, "png": 33, "py": 29, "txt": 7},
            "E_COMP_COUNTS")
    require(topology["comp_v24"]["text_line_counts"] == {"csv": 45203, "json": 1650, "md": 2635, "py": 2932, "txt": 171},
            "E_COMP_LINES")

    release = topology["process"]["release"]
    routed = topology["process"]["routed"]
    require((release["count"], len(release["commits"]), release["patch_lines"], release["patch_bytes"])
            == (38, 38, 50787, 10872687), "E_PROCESS_RELEASE")
    require((routed["count"], len(routed["commits"]), routed["patch_lines"], routed["patch_bytes"])
            == (98, 98, 106801, 12505904), "E_PROCESS_ROUTED")
    require(all(row["complete_diff_read"] for row in release["commits"] + routed["commits"]), "E_PROCESS_FULL_READ")
    require(topology["phase057_observations"]["count"] == 82
            and len(topology["phase057_observations"]["records"]) == 82
            and len(topology["findings"]) == 44,
            "E_PROCESS_FINDINGS")
    require(counts(topology["findings"], "status")
            == {"BOUND": 1, "CONFIRMED": 3, "CORRECTED": 1, "OPEN_ROUTED": 39}, "E_PROCESS_FINDING_STATUS")

    require(static["endpoint_summary"] == {"mirror_pairs": 7, "occurrences": 20, "parse_failures": 0,
            "unique_blobs": 12, "v1023": 6, "v1024": 7, "v1024_1": 7}, "E_STATIC_ENDPOINTS")
    require(static_att["coverage"] == {"endpoint_occurrences": 20, "feature_routes": 13,
            "initialization_rows": 40, "lineage_symbols": 52, "mirror_pairs": 7,
            "output_truncation_unresolved": [], "profile_surfaces": 11, "static_parse_pass": 20,
            "unread_intervals": []}, "E_STATIC_COVERAGE")
    require(static_att["finding_summary"] == {"P0": 0, "P1": 7, "P2": 6}, "E_STATIC_FINDINGS")
    require(static_att["unresolved_runtime_routes"] == ["fresh_import", "explicit_profile", "legacy_restoration"],
            "E_STATIC_ROUTES")
    require(initialization["consumed_step71"]["semantic_sha256"] == static["semantic_sha256"]
            and initialization["consumed_step71"]["sha256"]
            == ARTIFACT_SPECS["Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"][1],
            "E_STATIC_RUNTIME_BINDING")

    require({row["id"] for row in science["derivations"]} == {"D72-B1", "D72-B2", "D72-B3", "D72-B4"},
            "E_SCIENCE_DERIVATIONS")
    require((len(science["material_claims"]), len(science["source_bindings"]), len(science["input_routes"]),
             len(science["findings"])) == (28, 28, 39, 6), "E_SCIENCE_COUNTS")
    require(counts(science["material_claims"], "validation_state")
            == {"CONTRADICTED": 2, "EXTERNAL_UNVERIFIED": 9, "GROUND_NOT_FOUND": 6,
                "INTERNAL_ONLY": 9, "SUPERSEDED": 2}, "E_SCIENCE_STATES")
    derivation_ids = {row["id"] for row in science["derivations"]}
    require(all(row["derivation_id"] in derivation_ids for row in science["material_claims"]), "E_SCIENCE_DERIVATION_JOIN")
    census = science["tex_census"]["summary"]
    require(census == {"bibitem_occurrences": 95, "citation_occurrences": 561, "doi_occurrences": 91,
            "files": 90, "globally_undefined_keys": ["fergusonbazant2014", "guo2016"],
            "globally_unused_bibitem_keys": [], "unique_bibitem_keys": 93,
            "unique_citation_keys": 95, "unique_doi_strings": 85}, "E_TEX_CENSUS")
    require(science["non_graft"]["decision"] == "REJECTED_SOURCE_NOT_GRAFTED"
            and science["non_graft"]["undefined_keys"] == ["fergusonbazant2014", "guo2016"], "E_NON_GRAFT")

    require(initialization["counts"] == {"absent_routes": 1, "control_bindings": 6,
            "ground_not_found_routes": 0, "implemented_routes": 2, "initialization_rows": 40,
            "profile_surfaces": 11, "routes": 3}, "E_INITIALIZATION_COUNTS")
    route_outcomes = {row["route"]: row["outcome"] for row in initialization["routes"]}
    require(route_outcomes == {"explicit_profile": "IMPLEMENTED_AND_OBSERVED",
            "fresh_import": "IMPLEMENTED_AND_OBSERVED", "legacy_restoration": "ABSENT_IN_FROZEN_SOURCE"},
            "E_INITIALIZATION_OUTCOMES")
    legacy = next(row for row in initialization["routes"] if row["route"] == "legacy_restoration")
    require(legacy["absence_is_not_a_passing_behavior_route"] is True
            and legacy["absence_corroboration_process_is_not_route_execution"] is True
            and legacy["passing_behavior_route"] is False, "E_LEGACY_ABSENCE_BOUNDARY")
    require(runtime["counts"] == {"absence_corroboration_expectations_met": 4,
            "absence_corroboration_runs": 4, "changed_order_checks": 6, "changed_order_equal": 6,
            "implemented_behavior_route_expectations_met": 8, "implemented_behavior_route_runs": 8,
            "mutation_runs": 6, "mutations_detected": 6, "official_expectations_met": 10,
            "official_runs": 10, "runtimes": 2}, "E_RUNTIME_COUNTS")
    require(len(runtime["route_runs"]) == 18 and len(runtime["official_runs"]) == 10, "E_RUNTIME_RUNS")
    require(all(row["exit_code"] == row["expected_exit_code"] and row["expectation_met"] is True
                and row["external_scientific_truth"] is False and row["source_unchanged"] is True
                for row in runtime["route_runs"]), "E_RUNTIME_EVIDENCE")

    require(conformance["counts"] == {"conformance_rows": 41, "input_routes": 17, "open_routed": 35,
            "severity_none": 6, "severity_p1": 17, "severity_p2": 18,
            "source_bindings": 56, "step73_runtime_routes": 3}, "E_CONFORMANCE_COUNTS")
    require(counts(conformance["conformance_rows"], "status")
            == {"CLOSED": 1, "OPEN_ROUTED": 35, "PRESERVE_BOUNDARY": 5}, "E_CONFORMANCE_STATUS")
    require(counts(conformance["conformance_rows"], "verdict")
            == {"ABSENT_NOT_A_PASS": 1, "CLOSED_NON_GRAFT": 1, "CONFORMS": 3, "DERIVED_ONLY": 1,
                "GROUND_NOT_FOUND": 2, "MISMATCH": 24, "PARTIAL": 9}, "E_CONFORMANCE_VERDICTS")
    require(all(row["owner"] and row["acceptance_criterion"] and row["target_phase"]
                for row in conformance["conformance_rows"] if row["status"] == "OPEN_ROUTED"),
            "E_CONFORMANCE_ROUTES")
    by_id = {row["row_id"]: row for row in conformance["conformance_rows"]}
    require(by_id["D74-006"]["verdict"] == "GROUND_NOT_FOUND"
            and by_id["D74-006"]["status"] == "OPEN_ROUTED"
            and by_id["D74-007"]["status"] == "OPEN_ROUTED", "E_REF7_CONFORMANCE")

    require(disposition["counts"] == {"blob_groups": 131, "contradictory_blob_dispositions": 0,
            "distribution": {"CORRECT": 41, "PRESERVE": 114, "REJECTED_SOURCE": 2,
                             "THEORY_ONLY": 96, "UNVERIFIED": 8},
            "external_authority_promotions": 0, "open_source_dispositions": 49,
            "ownerless_sources": 0, "source_dispositions": 261}, "E_DISPOSITION_COUNTS")
    require(len(disposition["source_dispositions"]) == 261 and len(disposition["blob_disposition_groups"]) == 131,
            "E_DISPOSITION_ROWS")
    require({(row["occurrence_identity"]["occurrence_index"], row["occurrence_identity"]["path"],
              row["occurrence_identity"]["blob"]) for row in disposition["source_dispositions"]}
            == {(row["occurrence_index"], row["path"], row["blob"]) for row in occurrences},
            "E_DISPOSITION_OCCURRENCE_JOIN")
    require({row["blob"] for row in disposition["blob_disposition_groups"]}
            == {row["blob"] for row in unique_sources}, "E_DISPOSITION_BLOB_JOIN")

    summary = carry["gate_summary"]
    require(summary == {"active_obligations": 94, "external_authority_promotions": 0,
            "inherited_phase064_routes": 6, "multiply_owned_active_obligations": 0,
            "new_phase065_blockers": 0, "ownerless_active_obligations": 0,
            "phase057_open": 17, "phase057_records": 82, "phase_ceiling": "CONDITIONAL_P065",
            "semantic_chain_superseded": 4, "semantic_duplicate_groups": 2,
            "source_occurrences": 261, "status": "PASS_WITH_CONCERNS", "step70_findings": 44,
            "step70_open": 39, "step71_findings": 13, "step71_open": 13,
            "step72_findings": 6, "step72_open": 5, "step74_open_after_disposition": 34,
            "step74_open_input": 35, "step74_origin_routes_superseded": 17,
            "step74_rows": 41, "unique_blobs": 131, "unresolved_semantic_duplicates": 0},
            "E_CARRY_SUMMARY")
    require(len(carry["observation_records"]) == 192 and len(carry["active_obligations"]) == 94,
            "E_CARRY_ROWS")
    require(counts(carry["active_obligations"], "state") == {"OPEN_CARRY": 90, "PRESERVED_ACTIVE": 4},
            "E_CARRY_STATES")
    inherited = {row["observation_id"] for row in carry["inherited_phase064_routes"]}
    require(inherited == {"P059-CFR-CF-01", "P059-CFR-CF-02", "P059-CFR-CF-06",
                           "P059-CFR-CF-07", "P059-CFR-RB-02", "P059-CFR-RB-03"}, "E_CARRY_INHERITED")
    require({row["group_id"]: row["canonical_member"] for row in carry["semantic_duplicate_groups"]}
            == {"P065-SEM-001": "D74-028", "P065-SEM-002": "D74-006"}
            and all(row["status"] == "RESOLVED_BY_STEP74_REFINEMENT"
                    for row in carry["semantic_duplicate_groups"]), "E_CARRY_SEMANTIC")
    ref7 = next(row for row in carry["active_obligations"] if row["obligation_id"] == "P065-OBL-0059")
    active_origins = {row["origin_identity"] for row in carry["active_obligations"]}
    require("D74-006" in active_origins and "D74-007" not in active_origins, "E_REF7_ACTIVE_SET")
    require(ref7["origin_identity"] == "D74-006"
            and ref7["canonical_owner"] == "PHASE-071-PRIMARY-SOURCE-ACQUISITION"
            and ref7["target_phase"] == 71 and ref7["state"] == "OPEN_CARRY"
            and ref7["external_authority_promoted"] is False
            and "GROUND_NOT_FOUND" in ref7["acceptance_criterion"], "E_REF7_CARRY")
    require(carry["new_phase065_blockers"] == [], "E_CARRY_NEW_BLOCKERS")

    authority = {"external_scientific": False, "external_material": False, "experimental": False,
                 "external_primary_literature": False, "proposition_truth": False,
                 "canonical": False, "defect_repair": False, "identifiability": False,
                 "held_out_fitting": False, "final_latex_pdf": False, "publication_ready": False}
    return {
        "activation": {"gate": "PASS_P065_PLAN_ACTIVATION", "occurrences": 261, "unique_blobs": 131},
        "source_read_process": {"occurrences": 261, "unique_blobs": 131, "text_blobs": 125,
            "text_lines": 21618, "pdfs": 3, "pdf_pages": 148, "images": 3,
            "narrative_documents": 74, "narrative_lines": 7470, "supplemental": 6,
            "release_commits": 38, "routed_commits": 98, "phase057_observations": 82,
            "step70_findings": 44, "coverage_gaps": 0},
        "static": {"endpoints": 20, "unique_blobs": 12, "mirror_pairs": 7,
            "lineage_pairs": 52, "initialization_rows": 40, "profiles": 11,
            "feature_routes": 13, "findings": {"P0": 0, "P1": 7, "P2": 6}},
        "science": {"derivations": 4, "claims": 28, "sources": 28, "input_routes": 39,
            "findings": 6, "tex_files": 90, "bibitems": 95, "citations": 561,
            "doi_occurrences": 91, "undefined_non_graft": ["fergusonbazant2014", "guo2016"]},
        "runtime": {"routes": route_outcomes, "route_runs": 18, "official_runs": 10,
            "implemented_runs": 8, "absence_runs": 4, "mutation_runs": 6,
            "runtimes": 2, "changed_order_equal": 6},
        "conformance": {"rows": 41, "input_routes": 17, "source_bindings": 56,
            "open_routed": 35, "preserve_boundary": 5, "closed": 1},
        "disposition_carry": {"occurrences": 261, "blob_groups": 131,
            "distribution": {"CORRECT": 41, "PRESERVE": 114, "REJECTED_SOURCE": 2,
                             "THEORY_ONLY": 96, "UNVERIFIED": 8, "DISCARD": 0},
            "open_source_rows": 49, "observations": 192, "active": 94,
            "semantic_groups": 2, "step74_supersessions": 17, "ref7_chain_supersessions": 4,
            "new_blockers": 0, "external_promotions": 0},
        "gate": {"selected": "CONDITIONAL_P065", "pass_rejected": "REF7_PRIMARY_TEXT_GROUND_NOT_FOUND",
                 "fail_rejected": "INTERNAL_AUDIT_COMPLETE", "owner": "PHASE-071-PRIMARY-SOURCE-ACQUISITION"},
        "independent_numeric": independent_numeric_checks(),
        "authority": authority,
    }
def markdown_lines(path: str) -> tuple[bytes, list[str]]:
    target = ROOT / path
    require(target.is_file(), "E_OUTPUT_MISSING", path)
    raw = target.read_bytes()
    try:
        return raw, raw.decode("utf-8").splitlines()
    except UnicodeError as error:
        raise ValidationError("E_OUTPUT_UTF8", path) from error


def exact_prefixed_field(lines: list[str], prefix: str, expected: str, code: str) -> None:
    matches = [line for line in lines if line.startswith(prefix)]
    require(matches == [prefix + expected], code, repr(matches))


def exact_table_row(lines: list[str], prefix: str, code: str) -> tuple[str, list[str]]:
    matches = [line for line in lines if line.startswith(prefix)]
    require(len(matches) == 1, code, repr(matches))
    row = matches[0]
    cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
    return row, cells


def exact_section_body(lines: list[str], heading: str, expected_body: str, code: str) -> None:
    positions = [index for index, line in enumerate(lines) if line == heading]
    require(len(positions) == 1, code, f"heading_count={len(positions)}")
    start = positions[0] + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    require(lines[start:end] == ["", expected_body], code, repr(lines[start:end]))


def validate_output_control_content(content: dict[str, list[str]]) -> None:
    report = content[REPORT_PATH]
    gate = content[GATE_RESULT_PATH]
    phase = content[PHASE_RESULT_PATH]
    document_specs = (
        (REPORT_PATH, report, "REPORT", "# Phase 065 v1.0.24/v1.0.24.1 Lineage Report H", "Gate: ", "상태: "),
        (GATE_RESULT_PATH, gate, "GATE_RESULT", "# Phase 065 Step 75.2 Integrated Gate Result", "Selected Gate: ", "Status: "),
        (PHASE_RESULT_PATH, phase, "PHASE_RESULT", "# Phase 065 Result — v1.0.24/v1.0.24.1 Full Lineage Reaudit", "Exclusive Gate: ", "Status: "),
    )
    for path, lines, diagnostic, h1, gate_prefix, status_prefix in document_specs:
        require(lines and lines[0] == h1 and lines.count(h1) == 1, f"E_{diagnostic}_H1", path)
        exact_prefixed_field(lines, gate_prefix, f"`{GATE}`", f"E_{diagnostic}_GATE")
        exact_prefixed_field(lines, status_prefix, "`CONDITIONAL_WITH_OPEN_EXTERNAL_AUTHORITY`", f"E_{diagnostic}_STATUS")
        exact_prefixed_field(lines, "Containing commit: ", "`PENDING_AT_PRECOMMIT_BY_DESIGN`", f"E_{diagnostic}_CONTAINING_COMMIT")
        exact_prefixed_field(lines, "Expected parent: ", f"`{PARENT_COMMIT}`", f"E_{diagnostic}_PARENT")
        exact_prefixed_field(lines, "Expected subject: ", f"`{SUBJECT}`", f"E_{diagnostic}_SUBJECT")
        exact_prefixed_field(lines, "Postcommit persistence terminal: ", f"`{PERSISTENCE}`", f"E_{diagnostic}_PERSISTENCE")
        joined = "\n".join(lines)
        require("Ref. 7" in joined and "GROUND_NOT_FOUND" in joined
                and "PHASE-071-PRIMARY-SOURCE-ACQUISITION" in joined,
                f"E_{diagnostic}_REF7_ROUTE", path)
        require("PASS_P065_LINEAGE_H" in joined and "FAIL_P065" in joined
                and "Alternatives rejected" in joined, f"E_{diagnostic}_ALTERNATIVES", path)
        require("Phase 066 detailed plan" in joined and "Step 76" in joined, f"E_{diagnostic}_NEXT", path)

    parent = content[PARENT_LEDGER_PATH]
    active = content[ACTIVE_LEDGER_PATH]
    handover = content[HANDOVER_PATH]
    parent_row, parent_cells = exact_table_row(parent, "| 065 |", "E_PARENT_LEDGER_ROW")
    require(len(parent_cells) == 12 and parent_cells[0] == "065"
            and parent_cells[5] == "CONDITIONAL_PENDING_PERSISTENCE", "E_PARENT_LEDGER_STATUS", parent_row)
    require(LEDGER_PROGRESS in parent_row, "E_PARENT_LEDGER_PROGRESS", parent_row)
    required = (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 066 detailed-plan activation", "Step 76",
                "PASS_P065_STEP75_1_PERSISTENCE", "GROUND_NOT_FOUND")
    require(all(token in parent_row for token in required), "E_PARENT_LEDGER_RECOVERY", parent_row)

    active_phase_row, active_phase_cells = exact_table_row(active, "| 065 |", "E_ACTIVE_LEDGER_ROW")
    require(len(active_phase_cells) == 10 and active_phase_cells[0] == "065"
            and active_phase_cells[4] == "CONDITIONAL_PENDING_PERSISTENCE",
            "E_ACTIVE_LEDGER_STATUS", active_phase_row)
    require(LEDGER_PROGRESS in active_phase_row, "E_ACTIVE_LEDGER_PROGRESS", active_phase_row)
    require(all(token in active_phase_row for token in required), "E_ACTIVE_LEDGER_RECOVERY", active_phase_row)
    require([line for line in phase if line.startswith("Plan activation과 cumulative Steps 70–")]
            == [PHASE_RESULT_PROGRESS_LINE], "E_PHASE_RESULT_PROGRESS")
    exact_section_body(active, "## Next Exact Step", NEXT_EXACT_STEP_BODY, "E_ACTIVE_NEXT_EXACT_STEP")

    active_prior_row, active_prior_cells = exact_table_row(active, "| Step 75.1 |", "E_ACTIVE_PRIOR_STEP_ROW")
    require(len(active_prior_cells) == 6 and active_prior_cells[2] == f"`{PARENT_COMMIT}`"
            and active_prior_cells[3] == "pushed/live-remote verified"
            and active_prior_cells[4] == "yes", "E_ACTIVE_PRIOR_STEP_STATUS", active_prior_row)
    require(all(token in active_prior_row for token in
                (STEP74, "audit(phase065): disposition v1024 lineage", "PASS_P065_STEP75_1_PERSISTENCE")),
            "E_ACTIVE_PRIOR_STEP_RECOVERY", active_prior_row)
    active_step_row, active_step_cells = exact_table_row(active, "| Step 75.2 |", "E_ACTIVE_STEP_ROW")
    require(len(active_step_cells) == 6 and active_step_cells[0] == "Step 75.2"
            and active_step_cells[2] == "`PENDING_AT_PRECOMMIT_BY_DESIGN`",
            "E_ACTIVE_STEP_STATUS", active_step_row)
    require(all(token in active_step_row for token in
                (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 066 detailed-plan activation", "Step 76")),
            "E_ACTIVE_STEP_RECOVERY", active_step_row)

    handover_prior_row, handover_prior_cells = exact_table_row(
        handover, "| Phase 065 Step 75.1 |", "E_HANDOVER_PRIOR_STEP_ROW")
    require(len(handover_prior_cells) == 4
            and handover_prior_cells[:2] == ["Phase 065 Step 75.1", "Step 75.1"]
            and PARENT_COMMIT in handover_prior_row
            and "PASS_P065_STEP75_1_PERSISTENCE" in handover_prior_row,
            "E_HANDOVER_PRIOR_STEP_STATUS", handover_prior_row)
    handover_step_row, handover_step_cells = exact_table_row(
        handover, "| Phase 065 Step 75.2 |", "E_HANDOVER_STEP_ROW")
    require(len(handover_step_cells) == 4
            and handover_step_cells[:2] == ["Phase 065 Step 75.2", "Step 75.2"],
            "E_HANDOVER_STEP_STATUS", handover_step_row)
    require(all(token in handover_step_row for token in
                (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 066 detailed-plan activation", "Step 76")),
            "E_HANDOVER_STEP_RECOVERY", handover_step_row)
    expected_current = ("17. 현재 Phase 상태: Phase 065 `CONDITIONAL_PENDING_PERSISTENCE`, "
                        "Current checkpoint: Step 75.2 precommit `CONDITIONAL_P065`")
    require([line for line in handover if line.startswith("17. 현재 Phase 상태:")]
            == [expected_current], "E_HANDOVER_CURRENT_STATUS")
def load_output_content() -> dict[str, list[str]]:
    content: dict[str, list[str]] = {}
    for path in NONSELF_PATHS:
        if path.endswith(".md"):
            _, content[path] = markdown_lines(path)
    return content


def output_inventory() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    content: dict[str, list[str]] = {}
    for path in NONSELF_PATHS:
        raw, lines = markdown_lines(path) if path.endswith(".md") else ((ROOT / path).read_bytes(), [])
        normalized = lf_bytes(raw)
        records.append({"path": path, "sha256_lf": sha256(normalized), "bytes": len(normalized),
                        "physical_lines": len(raw.decode("utf-8").splitlines())})
        if lines:
            content[path] = lines
    validate_output_control_content(content)
    return {"count": 7, "paths": sorted(NONSELF_PATHS), "records": sorted(records, key=lambda row: row["path"]),
            "result_first": True, "validation_json_written_last": True,
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"}


FINAL_TOP_KEYS = {
    "schema_version", "phase", "step", "generated_date", "gate", "status",
    "expected_parent", "expected_subject", "authority_boundary", "authority",
    "validator_identity", "exact_eight", "repository", "input_inventory",
    "step_commit_inventory", "historical_execution", "integrated_contracts",
    "output_contract", "negative_control_contract", "determinism", "semantic_sha256",
}


def build_document(precommit: dict[str, Any], persistence: dict[str, Any]) -> dict[str, Any]:
    validate_source_policy()
    objects, inputs = load_pinned_inputs()
    integrated = integrated_contracts(objects)
    outputs = output_inventory()
    validator_raw = lf_bytes(VALIDATOR.read_bytes())
    document: dict[str, Any] = {
        "schema_version": "P065-STEP75.2-1", "phase": "065", "step": "75.2", "generated_date": "2026-08-31",
        "gate": GATE, "status": STATUS, "expected_parent": PARENT_COMMIT, "expected_subject": SUBJECT,
        "authority_boundary": AUTHORITY_BOUNDARY, "authority": copy.deepcopy(integrated["authority"]),
        "validator_identity": {"path": VALIDATOR_PATH, "sha256_lf": sha256(validator_raw), "bytes_lf": len(validator_raw),
                               "source_policy": "PINNED_HISTORICAL_EXECUTION_ONLY"},
        "exact_eight": {"count": 8, "paths": FINAL_PATHS, "result_first": True, "json_last": True},
        "repository": stable_repository_projection(repository_snapshot(allow_final_dirt=True)),
        "input_inventory": inputs, "step_commit_inventory": step_commit_inventory(),
        "historical_execution": {"precommit": precommit, "persistence": persistence, "unit_count": 7,
                                 "invocation_count": 21, "pass_count": 21},
        "integrated_contracts": integrated, "output_contract": outputs,
        "negative_control_contract": {"named_count": 90, "strict_json_count": 6, "git_boundary_count": 17,
                                      "singleton_required": True},
        "determinism": {"projections": 2, "byte_identical": True, "environment_fields_excluded": True},
    }
    document["semantic_sha256"] = semantic_hash(document)
    strict_load_bytes(pretty_bytes(document), "fresh-document")
    return document


def document_diagnostics(document: Any, expected: dict[str, Any]) -> set[str]:
    if type(document) is not dict or set(document) != FINAL_TOP_KEYS:
        return {"E_FINAL_SCHEMA"}
    failures: set[str] = set()
    comparisons = (
        ("E_FINAL_IDENTITY", (document["phase"], document["step"], document["generated_date"]), ("065", "75.2", "2026-08-31")),
        ("E_FINAL_GATE", (document["gate"], document["status"]), (GATE, STATUS)),
        ("E_FINAL_PARENT_SUBJECT", (document["expected_parent"], document["expected_subject"]), (PARENT_COMMIT, SUBJECT)),
        ("E_FINAL_AUTHORITY", document["authority"], expected["authority"]),
        ("E_FINAL_VALIDATOR", document["validator_identity"], expected["validator_identity"]),
        ("E_FINAL_ALLOWLIST", document["exact_eight"], expected["exact_eight"]),
        ("E_FINAL_REPOSITORY", document["repository"], expected["repository"]),
        ("E_FINAL_INPUTS", document["input_inventory"], expected["input_inventory"]),
        ("E_FINAL_COMMITS", document["step_commit_inventory"], expected["step_commit_inventory"]),
        ("E_FINAL_HISTORICAL", document["historical_execution"], expected["historical_execution"]),
        ("E_FINAL_INTEGRATED", document["integrated_contracts"], expected["integrated_contracts"]),
        ("E_FINAL_OUTPUTS", document["output_contract"], expected["output_contract"]),
        ("E_FINAL_NEGATIVE_CONTRACT", document["negative_control_contract"], expected["negative_control_contract"]),
        ("E_FINAL_DETERMINISM", document["determinism"], expected["determinism"]),
    )
    for code, observed, wanted in comparisons:
        if observed != wanted:
            failures.add(code)
    if document["authority_boundary"] != AUTHORITY_BOUNDARY:
        failures.add("E_FINAL_AUTHORITY_BOUNDARY")
    if document["semantic_sha256"] != semantic_hash(document):
        failures.add("E_FINAL_SEMANTIC_HASH")
    return failures


def run_negative_controls(baseline: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = []

    def add(code: str, mutation: Callable[[dict[str, Any]], None], rehash: bool = True) -> None:
        cases.append((code, mutation, rehash))

    add("E_FINAL_SCHEMA", lambda d: d.__setitem__("unexpected", 1), False)
    add("E_FINAL_IDENTITY", lambda d: d.__setitem__("step", "64"))
    add("E_FINAL_GATE", lambda d: d.__setitem__("gate", "CONDITIONAL_P063"))
    add("E_FINAL_PARENT_SUBJECT", lambda d: d.__setitem__("expected_parent", "0" * 40))
    add("E_FINAL_AUTHORITY", lambda d: d["authority"].__setitem__("external_scientific", True))
    add("E_FINAL_VALIDATOR", lambda d: d["validator_identity"].__setitem__("sha256_lf", "0" * 64))
    add("E_FINAL_ALLOWLIST", lambda d: d["exact_eight"]["paths"].pop())
    add("E_FINAL_REPOSITORY", lambda d: d["repository"].__setitem__("live_protected", "0" * 40))
    add("E_FINAL_INPUTS", lambda d: d["input_inventory"].__setitem__("machine_count", 9))
    add("E_FINAL_COMMITS", lambda d: d["step_commit_inventory"].pop())
    add("E_FINAL_HISTORICAL", lambda d: d["historical_execution"].__setitem__("pass_count", 14))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["source_read_process"].__setitem__("unique_blobs", 130))
    add("E_FINAL_OUTPUTS", lambda d: d["output_contract"].__setitem__("result_first", False))
    add("E_FINAL_NEGATIVE_CONTRACT", lambda d: d["negative_control_contract"].__setitem__("singleton_required", False))
    add("E_FINAL_DETERMINISM", lambda d: d["determinism"].__setitem__("byte_identical", False))
    add("E_FINAL_AUTHORITY_BOUNDARY", lambda d: d.__setitem__("authority_boundary", "overclaim"))
    add("E_FINAL_SEMANTIC_HASH", lambda d: d.__setitem__("semantic_sha256", "0" * 64), False)
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["source_read_process"].__setitem__("narrative_lines", 7232))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["science"].__setitem__("undefined_non_graft", []))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["runtime"]["routes"].__setitem__("legacy_restoration", "IMPLEMENTED_AND_OBSERVED"))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["conformance"].__setitem__("open_routed", 34))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["disposition_carry"].__setitem__("new_blockers", 1))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["independent_numeric"]["c_rate_timebase"].__setitem__("hour_to_second_factor", 1))
    add("E_FINAL_HISTORICAL", lambda d: d["historical_execution"]["precommit"].__setitem__("invocation_count", 13))
    passed = 0
    for wanted, mutation, rehash in cases:
        candidate = copy.deepcopy(baseline)
        mutation(candidate)
        if rehash and set(candidate) == FINAL_TOP_KEYS:
            candidate["semantic_sha256"] = semantic_hash(candidate)
        observed = document_diagnostics(candidate, baseline)
        require(observed == {wanted}, "E_NEGATIVE_SINGLETON", f"{wanted}:{sorted(observed)}")
        passed += 1
    strict_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e9999}', b'{"x":']
    for raw in strict_cases:
        try:
            strict_load_bytes(raw, "negative")
        except ValidationError as error:
            require(error.code in {"E_DUPLICATE_JSON", "E_NONFINITE_JSON", "E_STRICT_JSON"}, "E_STRICT_NEGATIVE_CODE", error.code)
        else:
            raise ValidationError("E_STRICT_NEGATIVE_ESCAPE", raw.decode("ascii"))

    def replace_exact(lines: list[str], old: str, new: str) -> None:
        require(lines.count(old) == 1, "E_DOCUMENT_NEGATIVE_FIXTURE", old)
        lines[lines.index(old)] = new

    document_cases: list[tuple[str, Callable[[dict[str, list[str]]], None]]] = [
        ("E_GATE_RESULT_STATUS", lambda c: replace_exact(c[GATE_RESULT_PATH], "Status: `CONDITIONAL_WITH_OPEN_EXTERNAL_AUTHORITY`", "Status: `FAIL`")),
        ("E_GATE_RESULT_PARENT", lambda c: (
            replace_exact(c[GATE_RESULT_PATH], f"Expected parent: `{PARENT_COMMIT}`", f"Expected parent: `{'0' * 40}`"),
            c[GATE_RESULT_PATH].append(f"Unbound parent witness: `{PARENT_COMMIT}`"),
        )),
        ("E_PHASE_RESULT_STATUS", lambda c: replace_exact(c[PHASE_RESULT_PATH], "Status: `CONDITIONAL_WITH_OPEN_EXTERNAL_AUTHORITY`", "Status: `CONDITIONAL`")),
        ("E_ACTIVE_STEP_RECOVERY", lambda c: replace_exact(
            c[ACTIVE_LEDGER_PATH],
            next(line for line in c[ACTIVE_LEDGER_PATH] if line.startswith("| Step 75.2 |")),
            next(line for line in c[ACTIVE_LEDGER_PATH] if line.startswith("| Step 75.2 |")).replace(PARENT_COMMIT, "0" * 40),
        )),
        ("E_ACTIVE_NEXT_EXACT_STEP", lambda c: replace_exact(
            c[ACTIVE_LEDGER_PATH], NEXT_EXACT_STEP_BODY,
            NEXT_EXACT_STEP_BODY.replace("Step 75.2 eight declared paths", "Step 75.1 eight declared paths"),
        )),
    ]
    for wanted, mutation in document_cases:
        candidate_content = copy.deepcopy(load_output_content())
        mutation(candidate_content)
        try:
            validate_output_control_content(candidate_content)
        except ValidationError as error:
            require(error.code == wanted, "E_DOCUMENT_NEGATIVE_SINGLETON", f"{wanted}:{error.code}")
            passed += 1
        else:
            raise ValidationError("E_DOCUMENT_NEGATIVE_ESCAPE", wanted)

    def inject_after_exact(source: str, marker: str, insertion: str) -> str:
        require(source.count(marker) == 1, "E_POLICY_NEGATIVE_FIXTURE", marker)
        offset = source.index(marker) + len(marker)
        return source[:offset] + insertion + source[offset:]

    policy_cases = (
        ("E_SOURCE_POLICY_IMPORT_ALLOWLIST", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nimport Codex.rogue\n", "negative-import.py")),
        ("E_SOURCE_POLICY_SUBPROCESS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nsubprocess.Popen(['git'])\n", "negative-popen.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\ngetattr(subprocess, 'run')\n", "negative-getattr.py")),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "Codex/work/v1024_phase065/build_unapproved.py"])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "-c", "exec(open('Codex/work/v1024_phase065/build_unapproved.py').read())"])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "-m", "rogue", UNIT_SPECS[0]["validator"]])),
        ("E_SOURCE_POLICY_OS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nos.system('echo pwn')\n", "negative-os-system.py")),
        ("E_SOURCE_POLICY_OS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nos.popen('echo pwn')\n", "negative-os-popen.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_API", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\npathlib.Path('x').write_text('pwn')\n", "negative-write-text.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_API", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\npathlib.Path('x').open('w')\n", "negative-path-open.py")),
        ("E_SOURCE_POLICY_SHUTIL", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nshutil.copy('x', 'y')\n", "negative-shutil-copy.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nsubprocess.__dict__['run'](['git'])\n", "negative-subprocess-dict.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nrunner = run_process\nrunner(['git'])\n", "negative-process-alias.py")),
        ("E_SOURCE_POLICY_IMPORT_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nimport subprocess as s\ns.run(['git'])\n", "negative-import-alias.py")),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "-c", "alias.pwn=!echo pwn", "pwn"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "clone", "ext::sh -c pwn", "x"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "pwn"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "config", "core.sshCommand", "pwn"])),
        ("E_SOURCE_POLICY_GIT_OWNER", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected():\n    git(['push', 'origin', 'main'])\n", "negative-git-owner.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected():\n    s = sys.modules['subprocess']\n    s.Popen(['git'])\n", "negative-sys-modules.py")),
        ("E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nfrom sys import modules\ns = modules['subprocess']\ns.Popen(['git'])\n",
            "negative-from-sys-modules.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ns = sys.modules.get('subprocess')\ns.Popen(['git'])\n", "negative-sys-modules-get.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected(g=git):\n    pass\n", "negative-default-git.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nf = lambda r=run_process: None\n", "negative-lambda-default-run-process.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected(o=open):\n    pass\n", "negative-default-open.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected(p=subprocess.Popen):\n    pass\n", "negative-default-subprocess.py")),
        ("E_SOURCE_POLICY_DEFAULT", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected(w=pathlib.Path.write_bytes):\n    pass\n", "negative-default-filesystem.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nwriter = open\n", "negative-alias-open.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nwriter = pathlib.Path.write_bytes\n", "negative-alias-path-write.py")),
        ("E_SOURCE_POLICY_CALLABLE_ALIAS", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nremover = os.__dict__['remove']\n", "negative-alias-os-dict.py")),
        ("E_SOURCE_POLICY_DYNAMIC", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\n(lambda: None)()\n", "negative-direct-lambda.py")),
        ("E_SOURCE_POLICY_DYNAMIC_NAMESPACE", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nx = (1).__class__\n", "negative-dunder-attribute.py")),
        ("E_SOURCE_POLICY_GIT_OWNER", lambda: validate_source_policy_text(
            inject_after_exact(
                VALIDATOR.read_text(encoding="utf-8"),
                "def status_paths(cwd: pathlib.Path = ROOT) -> set[str]:\n",
                "    def nested():\n        git(['push', 'origin', 'main'])\n    nested()\n",
            ), "negative-nested-git-owner.py")),
        ("E_SOURCE_POLICY_FILESYSTEM_OWNER", lambda: validate_source_policy_text(
            inject_after_exact(
                VALIDATOR.read_text(encoding="utf-8"),
                "def atomic_collect(raw: bytes) -> None:\n",
                "    def nested():\n        pathlib.Path('x').write_bytes(b'x')\n    nested()\n",
            ), "negative-nested-filesystem-owner.py")),
        ("E_SOURCE_POLICY_DYNAMIC_NAMESPACE", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef injected():\n    __builtins__.__import__('subprocess').Popen(['git'])\n", "negative-builtins-import.py")),
        ("E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nfrom os import system\nsystem('payload')\n", "negative-os-system-import.py")),
        ("E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nfrom os import remove\nremove('payload')\n", "negative-os-remove-import.py")),
        ("E_SOURCE_POLICY_SENSITIVE_IMPORT_FROM", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\nfrom shutil import rmtree\nrmtree('payload')\n", "negative-shutil-rmtree-import.py")),
        ("E_SOURCE_POLICY_DUPLICATE_OWNER", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8")
            + "\ndef status_paths():\n    git(['push', 'origin', 'main'])\n", "negative-duplicate-owner.py")),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "--force", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "--force-with-lease", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "-f", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "--mirror", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "--delete", "origin", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "origin", ":refs/heads/main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "origin", "+main:main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["C:\\tools\\git.exe", "status"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "origin", "main:"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "--prune", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "--exec", "pwn", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "push", "-e", "pwn", "origin"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "clone", "-u", "pwn", "src", "dst"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "clone", "-c", "core.sshCommand=pwn", "src", "dst"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "clone", "--config=core.sshCommand=pwn", "src", "dst"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "branch", "-D", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "checkout", "-f", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "switch", "-f", "main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "update-ref", "-d", "refs/heads/main"])),
        ("E_SOURCE_POLICY_GIT", lambda: validate_python_execution_argv(
            ["git", "reset", "--hard", "HEAD"])),
        ("E_EXPECTED_COMMIT_FORMAT", lambda: validate_cli_arguments(
            False, "persistence", "--output=C:\\escape")),
        ("E_HISTORICAL_BANNER", lambda: validate_historical_output(
            "PASS_EXPECTED\nFAIL_INJECTED\n", "", "PASS_EXPECTED", "NEGATIVE")),
    )
    for wanted, probe in policy_cases:
        try:
            probe()
        except ValidationError as error:
            require(error.code == wanted, "E_POLICY_NEGATIVE_SINGLETON", f"{wanted}:{error.code}")
            passed += 1
        else:
            raise ValidationError("E_POLICY_NEGATIVE_ESCAPE", wanted)
    return passed, len(cases) + len(document_cases) + len(policy_cases)


def repository_boundary_diagnostics(
    snapshot: dict[str, Any], *, expected_active: str, expected_protected: str,
    expected_main: str, expected_paths: set[str],
) -> set[str]:
    checks = (
        ("E_GIT_BRANCH", snapshot["branch"] == ACTIVE_BRANCH),
        ("E_GIT_UPSTREAM_NAME", snapshot["upstream_name"] == f"origin/{ACTIVE_BRANCH}"),
        ("E_GIT_HEAD", snapshot["head"] == expected_active),
        ("E_GIT_UPSTREAM", snapshot["upstream"] == expected_active),
        ("E_GIT_ACTIVE_TRACKING", snapshot["origin_active"] == expected_active),
        ("E_GIT_ACTIVE_LIVE", snapshot["live_active"] == expected_active),
        ("E_GIT_LOCAL_PROTECTED", snapshot["local_protected"] == expected_protected),
        ("E_GIT_PROTECTED_TRACKING", snapshot["origin_protected"] == expected_protected),
        ("E_GIT_PROTECTED_LIVE", snapshot["live_protected"] == expected_protected),
        ("E_GIT_MAIN_TRACKING", snapshot["origin_main"] == expected_main),
        ("E_GIT_MAIN_LIVE", snapshot["live_main"] == expected_main),
        ("E_GIT_STAGED", snapshot["staged"] == expected_paths),
        ("E_GIT_UNSTAGED", not snapshot["unstaged"]),
        ("E_GIT_UNTRACKED", not snapshot["untracked"]),
        ("E_GIT_CLAUDE", not snapshot["claude_status"]),
        ("E_GIT_INDEX_WORKTREE", snapshot["index_worktree_equal"] == {path: True for path in expected_paths}),
        ("E_GIT_DIFF_CHECK", snapshot["diff_check"] is True),
    )
    return {code for code, passed in checks if not passed}


def git_boundary_fixture_snapshot(work: pathlib.Path, expected_paths: set[str]) -> dict[str, Any]:
    staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=work).stdout)
    unstaged = nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=work).stdout)
    untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=work).stdout)
    return {
        "branch": git_text(["branch", "--show-current"], cwd=work),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"], cwd=work),
        "head": git_text(["rev-parse", "HEAD"], cwd=work),
        "upstream": git_text(["rev-parse", "@{upstream}"], cwd=work),
        "origin_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"], cwd=work),
        "live_active": live_tip(ACTIVE_BRANCH, cwd=work),
        "local_protected": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=work),
        "origin_protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"], cwd=work),
        "live_protected": live_tip(PROTECTED_BRANCH, cwd=work),
        "origin_main": git_text(["rev-parse", "refs/remotes/origin/main"], cwd=work),
        "live_main": live_tip("main", cwd=work),
        "staged": staged, "unstaged": unstaged, "untracked": untracked,
        "claude_status": bool(git(["status", "--porcelain=v1", "--", "Claude"], cwd=work).stdout),
        "index_worktree_equal": {path: git(["show", f":{path}"], cwd=work).stdout == (work / path).read_bytes() for path in expected_paths},
        "diff_check": git(["diff", "--cached", "--check"], cwd=work, check=False).returncode == 0,
    }


def make_git_boundary_fixture() -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, str, str, set[str]]:
    prefix = "phase065-step752-git-boundary-"
    root = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    work = root / "work"
    origin = root / "origin.git"
    expected_paths = set(FINAL_PATHS)
    try:
        work.mkdir()
        git(["init", "--initial-branch=main"], cwd=work)
        git(["config", "core.autocrlf", "false"], cwd=work)
        git(["config", "user.email", "phase065-fixture@example.invalid"], cwd=work)
        git(["config", "user.name", "Phase 065 Fixture"], cwd=work)
        (work / "base.txt").write_bytes(b"base\n")
        (work / "victim.txt").write_bytes(b"tracked deletion sentinel\n")
        (work / "Claude").mkdir()
        (work / "Claude" / "keep.txt").write_bytes(b"protected\n")
        git(["add", "base.txt", "victim.txt", "Claude/keep.txt"], cwd=work)
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
        git(["update-ref", "-d", "refs/heads/main"], cwd=work)
        for path in expected_paths:
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f"{path}\n".encode("utf-8"))
        git(["add", "--", *sorted(expected_paths)], cwd=work)
    except Exception:
        remove_temp_tree(root, prefix)
        raise
    return root, work, origin, base, drift, expected_paths


def run_git_boundary_controls() -> tuple[int, int]:
    cases: list[tuple[str, set[str], Callable[[pathlib.Path, pathlib.Path, str, str, set[str]], None]]] = [
        ("branch", {"E_GIT_BRANCH"}, lambda work, origin, base, drift, paths: git(["branch", "-m", "fixture/wrong"], cwd=work)),
        ("upstream_name", {"E_GIT_UPSTREAM_NAME"}, lambda work, origin, base, drift, paths: git(["branch", "--set-upstream-to", f"origin/{PROTECTED_BRANCH}", ACTIVE_BRANCH], cwd=work)),
        ("head", {"E_GIT_HEAD"}, lambda work, origin, base, drift, paths: git(["update-ref", f"refs/heads/{ACTIVE_BRANCH}", drift], cwd=work)),
        ("active_tracking", {"E_GIT_UPSTREAM", "E_GIT_ACTIVE_TRACKING"}, lambda work, origin, base, drift, paths: git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", drift], cwd=work)),
        ("active_live", {"E_GIT_ACTIVE_LIVE"}, lambda work, origin, base, drift, paths: git(["--git-dir", str(origin), "update-ref", f"refs/heads/{ACTIVE_BRANCH}", drift], cwd=work)),
        ("local_protected", {"E_GIT_LOCAL_PROTECTED"}, lambda work, origin, base, drift, paths: git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", drift], cwd=work)),
        ("protected_tracking", {"E_GIT_PROTECTED_TRACKING"}, lambda work, origin, base, drift, paths: git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", drift], cwd=work)),
        ("protected_live", {"E_GIT_PROTECTED_LIVE"}, lambda work, origin, base, drift, paths: git(["--git-dir", str(origin), "update-ref", f"refs/heads/{PROTECTED_BRANCH}", drift], cwd=work)),
        ("main_tracking", {"E_GIT_MAIN_TRACKING"}, lambda work, origin, base, drift, paths: git(["update-ref", "refs/remotes/origin/main", drift], cwd=work)),
        ("main_live", {"E_GIT_MAIN_LIVE"}, lambda work, origin, base, drift, paths: git(["--git-dir", str(origin), "update-ref", "refs/heads/main", drift], cwd=work)),
        ("claude", {"E_GIT_UNSTAGED", "E_GIT_CLAUDE"}, lambda work, origin, base, drift, paths: (work / "Claude" / "keep.txt").write_bytes(b"mutated\n")),
        ("extra_staged", {"E_GIT_STAGED"}, lambda work, origin, base, drift, paths: ((work / "extra.txt").write_bytes(b"extra\n"), git(["add", "extra.txt"], cwd=work))),
        ("staged_deletion", {"E_GIT_STAGED"}, lambda work, origin, base, drift, paths: git(["rm", "victim.txt"], cwd=work)),
        ("staged_rename_escape", {"E_GIT_STAGED"}, lambda work, origin, base, drift, paths: (
            git(["reset", "--", sorted(paths)[0]], cwd=work),
            (work / sorted(paths)[0]).unlink(),
            git(["mv", "victim.txt", sorted(paths)[0]], cwd=work),
        )),
        ("extra_untracked", {"E_GIT_UNTRACKED"}, lambda work, origin, base, drift, paths: (work / "extra.txt").write_bytes(b"extra\n")),
        ("index_worktree", {"E_GIT_UNSTAGED", "E_GIT_INDEX_WORKTREE"}, lambda work, origin, base, drift, paths: (work / sorted(paths)[0]).write_bytes(b"mutated\n")),
        ("cached_whitespace", {"E_GIT_DIFF_CHECK"}, lambda work, origin, base, drift, paths: ((work / sorted(paths)[0]).write_bytes(b"trailing-space \n"), git(["add", "--", sorted(paths)[0]], cwd=work))),
    ]
    passed = 0
    for name, wanted, mutation in cases:
        root, work, origin, base, drift, expected_paths = make_git_boundary_fixture()
        prefix = "phase065-step752-git-boundary-"
        try:
            positive = git_boundary_fixture_snapshot(work, expected_paths)
            require(not repository_boundary_diagnostics(positive, expected_active=base, expected_protected=base, expected_main=base, expected_paths=expected_paths), "E_GIT_FIXTURE_BASELINE", name)
            mutation(work, origin, base, drift, expected_paths)
            observed = repository_boundary_diagnostics(git_boundary_fixture_snapshot(work, expected_paths), expected_active=base, expected_protected=base, expected_main=base, expected_paths=expected_paths)
            require(observed == wanted, "E_GIT_FIXTURE_DIAGNOSTIC", f"{name}:{sorted(observed)}!={sorted(wanted)}")
            passed += 1
        finally:
            remove_temp_tree(root, prefix)
    return passed, len(cases)


def validate_staged() -> None:
    snapshot = repository_snapshot(allow_final_dirt=True)
    require(snapshot["head"] == PARENT_COMMIT, "E_PRECOMMIT_PARENT", snapshot["head"])
    staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"]).stdout)
    unstaged = nul_paths(git(["diff", "--no-renames", "--name-only", "-z"]).stdout)
    untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout)
    require(staged == FINAL_PATH_SET, "E_PRECOMMIT_PATHS", repr(sorted(staged)))
    require(not unstaged and not untracked, "E_PRECOMMIT_DIRT", repr(sorted(unstaged | untracked)))
    for path in FINAL_PATHS:
        require(git(["show", f":{path}"]).stdout == (ROOT / path).read_bytes(), "E_PRECOMMIT_INDEX_WORKTREE", path)
    require(git(["diff", "--check"], check=False).returncode == 0 and git(["diff", "--cached", "--check"], check=False).returncode == 0, "E_DIFF_CHECK", "precommit")


def validate_persistence(expected_commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None, "E_EXPECTED_COMMIT", expected_commit)
    snapshot = repository_snapshot(allow_final_dirt=False)
    require(snapshot["head"] == expected_commit, "E_PERSISTENCE_HEAD", snapshot["head"])
    require(git_text(["rev-parse", f"{expected_commit}^"]) == PARENT_COMMIT, "E_PERSISTENCE_PARENT", expected_commit)
    require(git_text(["show", "-s", "--format=%s", expected_commit]) == SUBJECT, "E_PERSISTENCE_SUBJECT", expected_commit)
    changed = nul_paths(git(["diff-tree", "--no-commit-id", "--no-renames", "--name-only", "-r", "-z", expected_commit]).stdout)
    require(changed == FINAL_PATH_SET, "E_PERSISTENCE_PATHS", repr(sorted(changed)))
    for path in FINAL_PATHS:
        require(git_blob(expected_commit, path) == (ROOT / path).read_bytes(), "E_PERSISTENCE_BYTES", path)


def read_stored() -> tuple[dict[str, Any], bytes]:
    require(ARTIFACT.is_file(), "E_VALIDATION_ARTIFACT_MISSING", ARTIFACT_PATH)
    raw = ARTIFACT.read_bytes()
    document, _ = strict_load_bytes(raw, ARTIFACT_PATH)
    require(pretty_bytes(document) == lf_bytes(raw), "E_VALIDATION_ARTIFACT_CANONICAL", ARTIFACT_PATH)
    require(type(document) is dict and document.get("semantic_sha256") == semantic_hash(document),
            "E_VALIDATION_ARTIFACT_SEMANTIC", ARTIFACT_PATH)
    return document, raw


def deterministic_pair(precommit: dict[str, Any], persistence: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    first = build_document(precommit, persistence)
    second = build_document(copy.deepcopy(precommit), copy.deepcopy(persistence))
    first_raw, second_raw = pretty_bytes(first), pretty_bytes(second)
    require(first_raw == second_raw, "E_DETERMINISM", "2/2")
    return first, first_raw


def atomic_collect(raw: bytes) -> None:
    require(not ARTIFACT.exists(), "E_COLLECT_REFUSES_OVERWRITE", ARTIFACT_PATH)
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST", "seven nonself outputs")
    temp_path = ARTIFACT.with_name(ARTIFACT.name + ".tmp-step752")
    require(not temp_path.exists(), "E_COLLECT_TEMP_EXISTS", str(temp_path))
    try:
        temp_path.write_bytes(raw)
        document, _ = strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        require(pretty_bytes(document) == raw, "E_COLLECT_CANONICAL", str(temp_path))
        os.replace(temp_path, ARTIFACT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(ARTIFACT.read_bytes() == raw, "E_COLLECT_WRITE", ARTIFACT_PATH)


def atomic_recollect(raw: bytes) -> None:
    require(ARTIFACT.is_file(), "E_RECOLLECT_REQUIRES_EXISTING", ARTIFACT_PATH)
    temp_path = ARTIFACT.with_name(ARTIFACT.name + ".tmp-step752-recollect")
    require(not temp_path.exists(), "E_RECOLLECT_TEMP_EXISTS", str(temp_path))
    try:
        temp_path.write_bytes(raw)
        document, _ = strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        require(pretty_bytes(document) == raw and document.get("semantic_sha256") == semantic_hash(document),
                "E_RECOLLECT_CANONICAL", str(temp_path))
        os.replace(temp_path, ARTIFACT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(ARTIFACT.read_bytes() == raw, "E_RECOLLECT_WRITE", ARTIFACT_PATH)


def recollect_from_stored_history() -> int:
    validate_source_policy()
    stored, _ = read_stored()
    require(stored["semantic_sha256"] in {
        CANONICAL_FULL_COLLECT_SEMANTIC_SHA256, CANONICAL_METADATA_CHECKPOINT_SEMANTIC_SHA256,
        CANONICAL_HARDENING_CHECKPOINT_SEMANTIC_SHA256,
    },
            "E_RECOLLECT_CANONICAL_FULL_COLLECT_PIN", stored["semantic_sha256"])
    precommit, persistence, normalized_count = validate_reused_historical_evidence(stored)
    expected, expected_raw = deterministic_pair(precommit, persistence)
    require(not document_diagnostics(expected, expected), "E_FRESH_DOCUMENT",
            repr(sorted(document_diagnostics(expected, expected))))
    negative_passed, negative_total = run_negative_controls(expected)
    git_passed, git_total = run_git_boundary_controls()
    atomic_recollect(expected_raw)
    refreshed, refreshed_raw = read_stored()
    require(not document_diagnostics(refreshed, expected) and refreshed_raw == expected_raw,
            "E_RECOLLECT_POSTWRITE", ARTIFACT_PATH)
    print(f"PASS_P065_STEP75_2_METADATA_RECOLLECT reused_canonical_full_history=21/21 "
          f"fresh_historical_replay=0/21 normalized_temp_args={normalized_count} "
          f"negative={negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
    print("PASS_P065_STEP75_2_DETERMINISM 2/2")
    return 0


def execute_validation(*, collect: bool, mode: str, expected_commit: str | None, run_negative: bool, run_determinism: bool) -> int:
    validate_source_policy()
    if collect:
        precommit = fresh_historical_precommit()
        persistence = fresh_historical_persistence()
    else:
        stored, stored_raw = read_stored()
        precommit, persistence, _ = validate_reused_historical_evidence(stored)
    expected, expected_raw = deterministic_pair(precommit, persistence)
    require(not document_diagnostics(expected, expected), "E_FRESH_DOCUMENT", repr(sorted(document_diagnostics(expected, expected))))
    if collect:
        negative_passed, negative_total = run_negative_controls(expected)
        git_passed, git_total = run_git_boundary_controls()
        atomic_collect(expected_raw)
        print(f"PASS_P065_STEP75_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print("PASS_P065_STEP75_2_DETERMINISM 2/2")
        print("CONDITIONAL_P065 collect=JSON_LAST result_first=true historical=21/21 ref7=GROUND_NOT_FOUND")
        return 0
    require(not document_diagnostics(stored, expected), "E_STORED_DOCUMENT", repr(sorted(document_diagnostics(stored, expected))))
    require(stored_raw == expected_raw, "E_STORED_BYTE_IDENTITY", ARTIFACT_PATH)
    automatic_full = mode in {"precommit", "persistence"}
    if run_negative:
        negative_passed, negative_total = run_negative_controls(stored)
        git_passed, git_total = run_git_boundary_controls()
        print(f"PASS_P065_STEP75_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
    elif automatic_full:
        negative_passed, negative_total = run_negative_controls(stored)
        require(stored["negative_control_contract"]["git_boundary_count"] == 17,
                "E_GIT_BOUNDARY_STORED", repr(stored["negative_control_contract"]))
        print(f"PASS_P065_STEP75_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 "
              "git_boundary=CANONICAL_REUSED_17/17")
    if run_determinism or automatic_full:
        print("PASS_P065_STEP75_2_DETERMINISM 2/2")
    if mode == "precommit":
        validate_staged()
        print("PASS_P065_STEP75_2_STAGED exact-eight=8/8 historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21")
    elif mode == "persistence":
        require(expected_commit is not None, "E_EXPECTED_COMMIT", "required")
        validate_persistence(expected_commit)
        print(f"{PERSISTENCE} commit={expected_commit} historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21")
    else:
        print("CONDITIONAL_P065 artifact=true historical=CANONICAL_REUSED_21/21 fresh_historical_replay=0/21 ref7=GROUND_NOT_FOUND")
    return 0


def validate_cli_arguments(
    collect: bool, mode: str, expected_commit: str | None, recollect_from_history: bool = False,
) -> None:
    require(not (collect and recollect_from_history), "E_CLI_MODE", "collect and metadata recollect")
    require(not (collect and mode != "artifact"), "E_CLI_MODE", "collect with repository mode")
    require(not (recollect_from_history and mode != "artifact"),
            "E_CLI_MODE", "metadata recollect with repository mode")
    if mode == "persistence":
        require(expected_commit is not None and re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
                "E_EXPECTED_COMMIT_FORMAT", str(expected_commit))
    else:
        require(expected_commit is None, "E_UNEXPECTED_COMMIT", str(expected_commit))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--recollect-from-stored-history", action="store_true")
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="artifact")
    parser.add_argument("--expected-commit")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    validate_cli_arguments(args.collect, args.mode, args.expected_commit, args.recollect_from_stored_history)
    if not args.collect and not ARTIFACT.is_file():
        raise ValidationError("E_VALIDATION_ARTIFACT_MISSING", ARTIFACT_PATH)
    if args.recollect_from_stored_history:
        return recollect_from_stored_history()
    return execute_validation(collect=args.collect, mode=args.mode, expected_commit=args.expected_commit,
                              run_negative=args.run_negative_probes, run_determinism=args.determinism_check)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL_P065_STEP75_2: {error}")
        raise SystemExit(1)
