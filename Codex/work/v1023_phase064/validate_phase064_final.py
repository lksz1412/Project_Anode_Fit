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
from collections.abc import Callable
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
VALIDATOR_PATH = "Codex/work/v1023_phase064/validate_phase064_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_064_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_064_V1023_LINEAGE_REPORT_G.md"
GATE_RESULT_PATH = "Codex/results/PHASE_064_STEP_069_2_GATE_RESULT.md"
PHASE_RESULT_PATH = "Codex/results/PHASE_064_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT_COMMIT = "ec1fb2eda54feb35cd6c15d2ab15f2478b26fc6d"
SUBJECT = "audit(phase064): close v1023 lineage gate"
GATE = "CONDITIONAL_P064"
PERSISTENCE = "PASS_P064_STEP69_2_PERSISTENCE"
STATUS = "CONDITIONAL_WITH_OPEN_EXTERNAL_AUTHORITY"
ALLOWED_IMPORT_ROOTS = frozenset({
    "__future__", "argparse", "ast", "collections", "copy", "hashlib", "json", "math", "os", "pathlib", "re",
    "shutil", "stat", "subprocess", "tempfile", "typing",
})
SUBORDINATE_RUNTIME_PROBE = "import PIL,numpy,pypdf,sys;print(sys.executable)"
LEDGER_PROGRESS = "Steps 64–69.1 complete; Step 69.2 precommit evidence and Gate selected, persistence pending"
PHASE_RESULT_PROGRESS_LINE = (
    "Plan activation과 cumulative Steps 64–69.1은 commit/push/persistence까지 완료했다. Step 69.2는 precommit evidence와 "
    "`CONDITIONAL_P064` Gate를 선택했으며 exact-eight commit/push/persistence는 아직 남아 있다. Frozen v1.0.23 source `83/83`, "
    "text `78/12,508`, PDF `3/129`, image `2/2`, process commit `14`, literature equation crops `8/8`, Ref. 6 VOR `4/4`, "
    "scientific rederivation, dual-runtime evidence, authority records `47/47`, source dispositions `83/83`, supplemental dispositions `6/6`, "
    "topical owner routes `18/18`을 통합했다."
)
NEXT_EXACT_STEP_BODY = (
    "Controller validates and stages exactly the Step 69.2 eight declared paths: final validator, `PHASE_064_VALIDATION.json`, "
    "Lineage Report G, Step 69.2 Gate Result, Phase Result, both execution ledgers and active handover. Run Python 3.12/3.14 staged "
    "validation and independent science/validator/records reviews, require P0/P1/P2=`0/0/0`, commit with subject "
    "`audit(phase064): close v1023 lineage gate` and parent `ec1fb2eda54feb35cd6c15d2ab15f2478b26fc6d`, push and verify "
    "local/upstream/tracking/live-origin equality, exact committed paths/blob bytes, protected/main/Claude non-change and clean status. "
    "Only after `PASS_P064_STEP69_2_PERSISTENCE` may the Phase 065 detailed plan be saved and activated; Step 70 begins only after that plan activation."
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
    "CONDITIONAL_P064 certifies complete internal v1.0.23 lineage/read/derivation/runtime auditing at the declared evidence tiers, "
    "but Ref. 7 original full text remains GROUND_NOT_FOUND. It does not certify Ref. 7 method content, external material or experimental truth, "
    "canonical selection, defect repair, parameter identifiability, held-out fitting, final equation freeze, final LaTeX/PDF or publication readiness."
)


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
        return
    allowed = {spec["validator"] for spec in globals().get("UNIT_SPECS", ())}
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


def run_process(argv: list[str], *, cwd: pathlib.Path = ROOT, timeout: int = 300, check: bool = False) -> subprocess.CompletedProcess[bytes]:
    validate_python_execution_argv(argv, cwd)
    process = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=timeout, check=False)
    if check and process.returncode != 0:
        raise ValidationError("E_PROCESS", f"{argv!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}")
    return process


def git(args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True, timeout: int = 300) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, timeout=timeout, check=check)


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


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT) -> str:
    process = git(["ls-remote", "--exit-code", "origin", f"refs/heads/{branch}"], cwd=cwd, timeout=180)
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

    def walk(item: Any) -> None:
        nonlocal nodes, scalars
        nodes += 1
        if isinstance(item, dict):
            for key, child in item.items():
                require(type(key) is str, "E_JSON_KEY", label)
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)
        else:
            scalars += 1
            if isinstance(item, float):
                require(math.isfinite(item), "E_NONFINITE_JSON", label)

    walk(value)
    return value, {"traversal_nodes": nodes, "scalar_nodes": scalars}


def semantic_hash(document: dict[str, Any]) -> str:
    projection = copy.deepcopy(document)
    projection.pop("semantic_sha256", None)
    return sha256(canonical_bytes(projection))


ACTIVATION = "ea0438fcceec6e5fbc02805b3caf86e36732e35c"
STEP64 = "fd8e192f031bb302933d925ceb9ba599a7975837"
STEP65 = "5fb19384e3df7a73c96fcf26e8f599b42c331ae7"
STEP66 = "0be2e45e56081e141fbd2f58be7a01b023ca16a3"
STEP67 = "4dec72387220e7210fc15d0323ca481a172111fd"
STEP68 = "84b977a5333870529369d62a6dab8459a6aa551d"
STEP69_1 = PARENT_COMMIT


def unit(unit: str, commit: str, parent: str, subject: str, validator: str, validator_sha256: str, paths: list[str], invocations: list[dict[str, Any]], persistence_args: list[str], persistence_terminal: str) -> dict[str, Any]:
    return {"unit": unit, "commit": commit, "parent": parent, "subject": subject, "validator": validator,
            "validator_sha256": validator_sha256, "paths": paths, "invocations": invocations,
            "persistence_args": persistence_args, "persistence_terminal": persistence_terminal}


def invocation(args: list[str], terminal: str) -> dict[str, Any]:
    return {"args": args, "terminal_prefix": terminal}


UNIT_SPECS = [
    unit("ACTIVATION", ACTIVATION, "696e6300a63ba47d773ca211362818987790a63f", "docs(phase064): plan v1023 lineage reaudit",
         "Codex/work/v1023_phase064/validate_phase064_plan.py", "5ee24751d6eef45f7f3a0107f216ac0f2bc0d06843c48915351b5b6e5184c1e1",
         ["Codex/plans/2026-08-29-phase064-v1023-lineage-detailed-plan.md", HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
          "Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md", "Codex/results/PHASE_064_PLAN_ACTIVATION_VALIDATION.json",
          "Codex/work/v1023_phase064/validate_phase064_plan.py"],
         [invocation(["--content-only", "--run-negative-probes", "--determinism-check"], "PASS_P064_PLAN_CONTENT"),
          invocation(["--verify-staged"], "PASS_P064_PLAN_ACTIVATION_STAGED")],
         ["--verify-persistence", "--expected-commit", ACTIVATION], "PASS_P064_PLAN_ACTIVATION_PERSISTENCE"),
    unit("STEP64", STEP64, ACTIVATION, "audit(phase064): freeze v1023 source process topology",
         "Codex/work/v1023_phase064/validate_phase064_step64.py", "cc0a0e35537db1ed431e2867f2fa56ffe5da970e3d88b8a4ed3f8bd923f74ac9",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
          "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json", "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json",
          "Codex/work/v1023_phase064/build_phase064_step64_source_process_topology.py", "Codex/work/v1023_phase064/validate_phase064_step64.py"],
         [invocation(["--verify-staged"], "PASS_P064_STEP64_STAGED")],
         ["--verify-persistence", "--expected-commit", STEP64], "PASS_P064_STEP64_PERSISTENCE"),
    unit("STEP65", STEP65, STEP64, "audit(phase064): bound v1023 literature authority",
         "Codex/work/v1023_phase064/validate_phase064_step65.py", "110bae58229850da427318ba588b22ee6ebfea9fd89800ef32b1334810dc54d4",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md",
          "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json", "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json",
          "Codex/work/v1023_phase064/build_phase064_step65_literature_authority.py", "Codex/work/v1023_phase064/validate_phase064_step65.py"],
         [invocation(["--mode", "precommit"], "PASS_P064_STEP65_LITERATURE_BOUNDED_GNF")],
         ["--mode", "persistence", "--expected-commit", STEP65], "PASS_P064_STEP65_PERSISTENCE"),
    unit("STEP66", STEP66, STEP65, "audit(phase064): rederive v1023 ratio transfer closure",
         "Codex/work/v1023_phase064/validate_phase064_step66.py", "f811892f9d9738df1813559141b90e647654ddbbfbf55829cff5ccf37d241f4f",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md",
          "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json",
          "Codex/work/v1023_phase064/build_phase064_step66_ratio_transfer_rederivation.py", "Codex/work/v1023_phase064/validate_phase064_step66.py"],
         [invocation(["--mode", "precommit"], "PASS_P064_STEP66_REDERIVATION")],
         ["--mode", "persistence", "--expected-commit", STEP66], "PASS_P064_STEP66_PERSISTENCE"),
    unit("STEP67", STEP67, STEP66, "audit(phase064): bound v1023 algebraic volterra runtime",
         "Codex/work/v1023_phase064/validate_phase064_step67.py", "86871a214c7135b9e6ec93a1f64c2b55a0d8d8d2a9d13e0e7f971fa0272ddb1d",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md",
          "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json", "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json",
          "Codex/work/v1023_phase064/build_phase064_step67_problem_runtime_boundary.py", "Codex/work/v1023_phase064/validate_phase064_step67.py"],
         [invocation(["--mode", "precommit"], "PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS")],
         ["--mode", "persistence"], "PASS_P064_STEP67_PERSISTENCE"),
    unit("STEP68", STEP68, STEP67, "audit(phase064): adjudicate v1023 validation authority",
         "Codex/work/v1023_phase064/validate_phase064_step68.py", "ded8334580c54bf1abbf6a18d4e311f9ff315b755ecd4b246b70410d2b4cc1b9",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md",
          "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json",
          "Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py", "Codex/work/v1023_phase064/validate_phase064_step68.py"],
         [invocation(["--mode", "precommit"], "PASS_P064_STEP68_AUTHORITY")],
         ["--mode", "persistence"], "PASS_P064_STEP68_PERSISTENCE"),
    unit("STEP69_1", STEP69_1, STEP68, "audit(phase064): disposition v1023 lineage",
         "Codex/work/v1023_phase064/validate_phase064_step69_dispositions.py", "2fcc6f86f2e2cbc1ddba1341dd1b672be0a65174e2375ff6be90439a3da34a85",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_064_STEP_069_1_DISPOSITION_RESULT.md",
          "Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json", "Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json",
          "Codex/work/v1023_phase064/build_phase064_step69_dispositions.py", "Codex/work/v1023_phase064/validate_phase064_step69_dispositions.py"],
         [invocation(["--verify-staged"], "PASS_P064_STEP69_1_STAGED")],
         ["--verify-persistence", "--expected-commit", STEP69_1], "PASS_P064_STEP69_1_PERSISTENCE"),
]


ARTIFACT_SPECS = {
    "Codex/results/PHASE_064_PLAN_ACTIVATION_VALIDATION.json": (ACTIVATION, "4a07d611cd3fbc9a6376e156b2c0cf3599374d7f03bfcf3dbb34479a5ee5f2be"),
    "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json": (STEP64, "ce0fcbda41e866d8f225255ae27ae0e0e1faba9b985c7f72194a14d085be1f99"),
    "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json": (STEP64, "5fadd789fe05ea83b294a34e0270f637a44c8359f79e63addfed60e8b62ac445"),
    "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json": (STEP65, "db67fc40d9fba6d03547325061b16d03da87ddf59e0985fd6d7b471d092d453a"),
    "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json": (STEP65, "273fa6eb35000b013b48eeb63154b098bd8d0ab3dc89a8634d478d75c4106fc4"),
    "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json": (STEP66, "bf940a9b3707b9e90d5e82068f722a9bb0aefe632157371db969e572e6e1af7b"),
    "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json": (STEP67, "b360cf220e519e861080405032dfc2c5be108998901b0c130b8ab325859e5ba3"),
    "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json": (STEP67, "f3c87cf1d2f3eea271ac88a76cf516695ac0a8843984651bd591d1d8f31ea1d9"),
    "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json": (STEP68, "e97e5362c8b162614c287bf2826a00bcd4b70600a67d7096e08e628a4dd59d5c"),
    "Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json": (STEP69_1, "7e177afe8cefb1147c20869dc6dfa1cc6ab06948db9e227a595e542ff648da38"),
    "Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json": (STEP69_1, "584dfaaf90537bb3f12aaef9c27f4d066ead74197d089e6b68c1ad8eefc7527c"),
}

RESULT_SPECS = {
    "Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md": (ACTIVATION, "fac2cf0449ba7f1e4a1331faf83abb6fba95788c2c99e1a986fc47e86f2cc87d"),
    "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md": (STEP64, "e112525d926f3e27c8e6b28b80f22203f477da776efd241aee6c9135fa225e64"),
    "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md": (STEP65, "eb9abd8b809d8b266689fead41ef207e3016494c721de03dcd9b387be9cc1534"),
    "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md": (STEP66, "1f5f85c51f9aa78eae0f04cb48ee9aac6c6c4cbe85884919148a8b6072378ae6"),
    "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md": (STEP67, "b62bb1b7d80c5da55630e4c07b96e9e3c2e0c8db62d26c1905d0933302aed5a5"),
    "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md": (STEP68, "1eccd230a93123b8dad5d4a0177373a3f5fd4817cdcbf12f427af2cf0b9f95c1"),
    "Codex/results/PHASE_064_STEP_069_1_DISPOSITION_RESULT.md": (STEP69_1, "a9e299ad86d846484b8410650b8a57a7c13615788e453bbe580a58408f6c4b3b"),
}

EXPECTED_TOP_KEYS = {
    "Codex/results/PHASE_064_PLAN_ACTIVATION_VALIDATION.json": "authority controls determinism exact_seven expected_parent expected_subject gate generated_date literature_boundary manifest negative_contract persistence_terminal phase plan process repository schema_version semantic_sha256 status supplemental validator_identity".split(),
    "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json": "artifact_kind authority builder_identity downstream_guardrails frozen_commit gate manifest next_step phase phase057_observations process schema_version semantic_sha256 sources status step".split(),
    "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json": "artifact_kind authority coverage_gap_count duplicate_route_count frozen_commit gate human_attestation_complete human_evidence human_evidence_semantic_sha256 partitions phase schema_version semantic_sha256 source_mutation_count sources status step totals".split(),
    "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json": "applicability artifact_kind authority_ceiling bibliography_boundaries builder_identity conflicts equation_chain gate open_items phase schema_version semantic_sha256 sources status step".split(),
    "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json": "access_date artifact_kind authority evidence_date evidence_id full_reads gate ground_not_found human_evidence human_evidence_semantic_sha256 matrix_semantic_sha256 phase schema_version semantic_sha256 source_mutation_count status step strict_traversal".split(),
    "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json": "authority authority_ceiling baseline_commit contraction correction_register deterministic_benchmark expected_parent expected_subject fredholm_rederivation gate generated_by ground_not_found human_evidence_semantic_sha256 independent_timing_observation non_applicable_targets prior_literature_binding schema semantic_sha256 source_contracts source_mutation_count status timebase transfer volterra_rederivation".split(),
    "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json": "artifact_kind authority baseline_commit call_edges counts equation_code_map expected_parent expected_subject findings gate generated_by generated_date human_evidence human_evidence_semantic_sha256 inherited_joins non_double_count omega_consumer_partition phase phase_ceiling problem_classes regular_solution_occupancy schema semantic_sha256 source_contracts source_mutation_count status step".split(),
    "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json": "artifact_kind authority baseline_commit counts expected_parent expected_subject gate generated_by generated_date independent_probes isolation official_and_mutation_runs phase phase_ceiling runtime_evidence_rows runtimes schema semantic_sha256 source_mutation_count status step".split(),
    "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json": "artifact_kind authority_axes authority_records authority_summary baseline_commit containing_commit counts document_contracts expected_parent expected_subject gate generated_by generated_date high_risk_bindings human_evidence human_evidence_semantic_sha256 json_type_projection_sha256 literature_boundary non_double_count overclaim_routes phase phase_ceiling prior_machine_inputs repository_boundary schema_version semantic_sha256 source_contracts status step supplemental_evidence".split(),
    "Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json": "artifact_kind authority_boundary baseline_commit counts gate input_commit inputs phase result_first schema_version source_contract source_dispositions step supplemental_dispositions".split(),
    "Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json": "artifact_kind authority_boundary baseline_commit canonical_owner_duplicate_check_universe equation38_supersession_binding gate gate_summary inherited_phase063_snapshot input_commit inputs new_phase064_blockers phase phase057_provisional_routes phase066_correction_observations phase067_finding_observations phase068_authority_routes residual_topical_routes result_first schema_version source_disposition_links step supplemental_disposition_links".split(),
}


def validate_source_policy_text(source: str, filename: str) -> None:
    tree = ast.parse(source, filename=filename)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            roots = {name.split(".", 1)[0] for name in modules}
            require(roots <= ALLOWED_IMPORT_ROOTS, "E_SOURCE_POLICY_IMPORT_ALLOWLIST", repr(sorted(roots - ALLOWED_IMPORT_ROOTS)))
        if isinstance(node, ast.Call):
            require(not (isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "__import__"}), "E_SOURCE_POLICY_CALL", ast.dump(node.func, include_attributes=False))
            for keyword in node.keywords:
                require(not (keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True), "E_SOURCE_POLICY_SHELL", "shell=True")


def validate_source_policy() -> None:
    validate_source_policy_text(VALIDATOR.read_text(encoding="utf-8"), VALIDATOR_PATH)
    historical_validators = {spec["validator"] for spec in UNIT_SPECS}
    require(len(historical_validators) == 7, "E_SOURCE_POLICY_VALIDATOR_ALLOWLIST", repr(sorted(historical_validators)))
    require(all(path.startswith("Codex/work/v1023_phase064/validate_") and "/build_" not in path
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
    return objects, {"machine_count": 11, "machine_records": machine_records, "result_count": 7,
                     "result_records": result_records, "strict_duplicate_keys": True,
                     "nonfinite_rejected": True, "full_recursive_traversal": True}


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
    process = run_process(["py", "-3.12", "-c", SUBORDINATE_RUNTIME_PROBE], timeout=60)
    require(process.returncode == 0, "E_SUBORDINATE_RUNTIME", process.stderr.decode("utf-8", errors="replace"))
    executable = process.stdout.decode("utf-8").strip()
    require(pathlib.Path(executable).is_file(), "E_SUBORDINATE_RUNTIME", executable)
    return executable


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
    git(["remote", "set-url", "origin", str(origin)], cwd=clone)
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
    prefix = f"phase064-step692-stage-{spec['unit'].lower()}-"
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
        git(["add", "--", *spec["paths"]], cwd=clone)
        staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=clone).stdout)
        require(staged == set(spec["paths"]), "E_FIXTURE_STAGED_SET", spec["unit"])
        require(not nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=clone).stdout), "E_FIXTURE_UNSTAGED", spec["unit"])
        require(not nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=clone).stdout), "E_FIXTURE_UNTRACKED", spec["unit"])
        require(git_text(["rev-parse", "HEAD"], cwd=clone) == spec["parent"], "E_FIXTURE_PARENT", spec["unit"])
        require(live_tip(ACTIVE_BRANCH, cwd=clone) == spec["parent"], "E_FIXTURE_LIVE", spec["unit"])
    except Exception:
        remove_temp_tree(parent, prefix)
        raise
    return parent, clone, restored


def make_historical_persistence_clone(spec: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    prefix = f"phase064-step692-persist-{spec['unit'].lower()}-"
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


def validate_historical_output(stdout: str, stderr: str, terminal: str, unit_name: str) -> list[str]:
    lines = stdout.splitlines()
    terminal_lines = [line for line in lines if line == terminal or line.startswith(terminal + " ")]
    require(len(terminal_lines) == 1, "E_HISTORICAL_TERMINAL", f"{unit_name}:{terminal}:{terminal_lines!r}")
    banners = [line for line in lines if line.startswith(("PASS", "FAIL"))]
    require(banners and all(line.startswith("PASS_") for line in banners), "E_HISTORICAL_BANNER", f"{unit_name}:{banners!r}")
    require(stderr == "", "E_HISTORICAL_STDERR", f"{unit_name}:{stderr[-1200:]}")
    return banners


def execute_historical(executable: str, clone: pathlib.Path, spec: dict[str, Any], args: list[str], terminal: str, location: str) -> dict[str, Any]:
    raw = (clone / spec["validator"]).read_bytes()
    require(sha256(raw) == spec["validator_sha256"], "E_HISTORICAL_VALIDATOR_SHA", spec["unit"])
    process = run_process([executable, spec["validator"], *args], cwd=clone, timeout=2400)
    stdout = process.stdout.decode("utf-8", errors="replace")
    stderr = process.stderr.decode("utf-8", errors="replace")
    require(process.returncode == 0, "E_HISTORICAL_EXIT", f"{spec['unit']}:{stdout[-1600:]}:{stderr[-1600:]}")
    banners = validate_historical_output(stdout, stderr, terminal, spec["unit"])
    return {"unit": spec["unit"], "commit": spec["commit"], "validator_path": spec["validator"],
            "validator_sha256": spec["validator_sha256"], "args": args, "terminal_prefix": terminal,
            "terminal_count": 1, "exit_code": 0, "stderr_bytes": len(process.stderr),
            "stdout_lf_bytes": len(lf_bytes(process.stdout)), "stdout_lf_sha256": sha256(lf_bytes(process.stdout)),
            "banners": banners,
            "execution_location": location}


def require_restored_inputs_unchanged(clone: pathlib.Path, restored: dict[str, str], unit_name: str) -> None:
    for path, expected in restored.items():
        require(sha256((clone / path).read_bytes()) == expected, "E_HISTORICAL_RESTORED_INPUT_MUTATION", f"{unit_name}:{path}")


def fresh_historical_precommit() -> dict[str, Any]:
    executable = subordinate_python()
    before = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        parent, clone, restored = make_historical_staged_clone(spec)
        prefix = f"phase064-step692-stage-{spec['unit'].lower()}-"
        try:
            for current in spec["invocations"]:
                records.append(execute_historical(executable, clone, spec, current["args"], current["terminal_prefix"],
                                                  "DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE"))
            require_restored_inputs_unchanged(clone, restored, spec["unit"])
            require(nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=clone).stdout) == set(spec["paths"]), "E_HISTORICAL_STAGE_MUTATION", spec["unit"])
            require(not nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=clone).stdout), "E_HISTORICAL_WORKTREE_MUTATION", spec["unit"])
        finally:
            remove_temp_tree(parent, prefix)
    after = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    require(canonical_bytes(before) == canonical_bytes(after), "E_ACTIVE_MUTATION", "precommit replay")
    require(len(records) == 8, "E_PRECOMMIT_COUNT", str(len(records)))
    return {"unit_count": 7, "invocation_count": 8, "pass_count": 8, "records": records,
            "historical_exact_staged_context": True, "cleanup_pass_count": 7, "active_repository_unchanged": True}


def fresh_historical_persistence() -> dict[str, Any]:
    executable = subordinate_python()
    before = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        parent, clone, restored = make_historical_persistence_clone(spec)
        prefix = f"phase064-step692-persist-{spec['unit'].lower()}-"
        try:
            records.append(execute_historical(executable, clone, spec, spec["persistence_args"], spec["persistence_terminal"],
                                              "DISPOSABLE_CLEAN_HISTORICAL_PERSISTENCE_CLONE"))
            require_restored_inputs_unchanged(clone, restored, spec["unit"])
            require(not status_paths(clone), "E_HISTORICAL_PERSISTENCE_MUTATION", spec["unit"])
        finally:
            remove_temp_tree(parent, prefix)
    after = stable_repository_projection(repository_snapshot(allow_final_dirt=True))
    require(canonical_bytes(before) == canonical_bytes(after), "E_ACTIVE_MUTATION", "persistence replay")
    return {"unit_count": 7, "pass_count": 7, "records": records,
            "historical_clean_persistence_context": True, "cleanup_pass_count": 7,
            "active_repository_unchanged": True}


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
    activation = objects["Codex/results/PHASE_064_PLAN_ACTIVATION_VALIDATION.json"]
    topology = objects["Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json"]
    reads = objects["Codex/results/PHASE_064_V1023_READ_ATTESTATION.json"]
    literature = objects["Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json"]
    literature_reads = objects["Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json"]
    ratio = objects["Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json"]
    code = objects["Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json"]
    runtime = objects["Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json"]
    authority = objects["Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json"]
    disposition = objects["Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json"]
    carry = objects["Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json"]

    require(activation["gate"] == "PASS_P064_PLAN_ACTIVATION", "E_ACTIVATION", activation["gate"])
    manifest_expected = {"source_count": 83, "unique_blob_count": 83, "bytes": 3338330,
                         "text_lines": 12508, "pdf_pages": 129}
    require({key: activation["manifest"][key] for key in manifest_expected} == manifest_expected,
            "E_ACTIVATION_MANIFEST", repr(activation["manifest"]))
    require(activation["process"]["commit_count"] == 14 and activation["process"]["phase_state"]["P4"] == "SKIPPED_D3_NOT_APPROVED",
            "E_ACTIVATION_PROCESS", repr(activation["process"]))

    topo_expected = {"sources": 83, "unique_blobs": 83, "bytes": 3338330, "text_lines": 12508,
                     "pdf_pages": 129, "image_occurrences": 2}
    require({key: topology["manifest"][key] for key in topo_expected} == topo_expected,
            "E_SOURCE_COUNTS", repr(topology["manifest"]))
    require(topology["manifest"]["review_modes"] == {"FULL_IMAGE": 2, "FULL_PDF": 3, "FULL_TEXT": 78},
            "E_REVIEW_MODES", repr(topology["manifest"]["review_modes"]))
    require(len(topology["sources"]) == 83 and len({row["occurrence_id"] for row in topology["sources"]}) == 83,
            "E_SOURCE_IDENTITIES", "83")
    require(topology["process"]["commit_count"] == 14 and topology["process"]["p4_state"] == "SKIPPED_D3_NOT_APPROVED",
            "E_SOURCE_PROCESS", repr(topology["process"]))
    require(topology["phase057_observations"]["count"] == 36, "E_PHASE057_OBSERVATIONS", repr(topology["phase057_observations"]))

    require(reads["totals"] == {"image_files": 2, "image_occurrences": 2, "pdf_files": 3, "pdf_pages": 129,
                                "sources": 83, "text_files": 78, "text_lines": 12508},
            "E_READ_COUNTS", repr(reads["totals"]))
    require((reads["coverage_gap_count"], reads["duplicate_route_count"], reads["source_mutation_count"], reads["human_attestation_complete"])
            == (0, 0, 0, True), "E_READ_COVERAGE", "gap/duplicate/mutation/human")
    require(len(reads["sources"]) == 83, "E_READ_ROWS", str(len(reads["sources"])))

    sources = {row["source_id"]: row for row in literature["sources"]}
    require(set(sources) == {"JCP147", "REF6", "REF7"}, "E_LITERATURE_SOURCES", repr(sorted(sources)))
    require((sources["JCP147"]["authority"]["pages_read"], sources["REF6"]["authority"]["pages_read"])
            == (10, 4), "E_LITERATURE_FULL_READ", repr(sources))
    require(sources["REF6"]["authority"]["raw_sha256"] == "c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460",
            "E_REF6_HASH", sources["REF6"]["authority"]["raw_sha256"])
    require(sources["REF7"]["bibliographic_identity"]["doi"] == "10.1063/1.4802584"
            and sources["REF7"]["authority"]["original_full_text_status"] == "GROUND_NOT_FOUND"
            and sources["REF7"]["allowed_use"] == "BIBLIOGRAPHIC_METADATA_ONLY", "E_REF7_BOUNDARY", repr(sources["REF7"]))
    require(len(literature["conflicts"]) == 1
            and literature["conflicts"][0]["candidate_ref7_doi"] == "10.1063/1.4802005"
            and literature["conflicts"][0]["disposition"] == "REJECT_AS_REF7_DOI", "E_REF7_FALSE_DOI", repr(literature["conflicts"]))
    require(len(literature["equation_chain"]) == 8 and len(literature["applicability"]["conditions"]) == 3,
            "E_LITERATURE_EQUATIONS", "8/3")
    require(literature_reads["ground_not_found"] == [{"authority_tier": "OFFICIAL_BIBLIOGRAPHIC_METADATA_ONLY", "bytes": None,
            "pages": None, "pages_read": 0, "raw_sha256": None, "source_id": "REF7", "status": "GROUND_NOT_FOUND"}],
            "E_LITERATURE_GNF", repr(literature_reads["ground_not_found"]))

    require(ratio["fredholm_rederivation"]["problem_class"] == "FREDHOLM_SECOND_KIND_FIXED_SEMI_INFINITE_DOMAIN"
            and ratio["fredholm_rederivation"]["literal_graphite_identity"] is False,
            "E_FREDHOLM_BOUNDARY", repr(ratio["fredholm_rederivation"]))
    require(ratio["volterra_rederivation"]["problem_class"] == "NONLINEAR_CAUSAL_VOLTERRA_SECOND_KIND"
            and ratio["volterra_rederivation"]["jcp_solution_ratio_identity"] is False,
            "E_VOLTERRA_BOUNDARY", repr(ratio["volterra_rederivation"]))
    require(ratio["fredholm_rederivation"]["eq38_angular_factor"] == "exp(K*sigma*mu)"
            and "exp(K*r*mu)" in ratio["prior_literature_binding"]["step65_eq38_stale_projection"]
            and "exp(K*sigma*mu)" in ratio["prior_literature_binding"]["step66_corrected_projection"],
            "E_EQ38_CORRECTION", repr(ratio["prior_literature_binding"]))
    require(ratio["timebase"]["legacy_overestimate_factor"] == 3600
            and ratio["transfer"]["formula"] == "H=1/(1+i*omega_x*L0)"
            and ratio["contraction"]["sufficient_condition"] == "q<1",
            "E_RATIO_CONTRACTS", "timebase/transfer/contraction")

    require(code["counts"] == {"P0": 1, "P1": 5, "P2": 3, "algebraic": 2, "problem_classes": 3, "ratio_applicable": 1},
            "E_CODE_COUNTS", repr(code["counts"]))
    require([row["ratio_reference_applicable"] for row in code["problem_classes"]] == [False, False, True],
            "E_PROBLEM_CLASSES", repr(code["problem_classes"]))
    require(runtime["counts"] == {"probe_runtime_sets": 2, "probe_sections_per_runtime": 5, "run_expectations_met": 10,
                                  "runs": 10, "runtime_evidence_rows": 2, "runtimes": 2},
            "E_RUNTIME_COUNTS", repr(runtime["counts"]))
    require(len(runtime["independent_probes"]) == 2 and all(
            all(section["pass"] for section in row["results"].values()) for row in runtime["independent_probes"]),
            "E_RUNTIME_PROBES", "2x5")

    require(len(authority["authority_axes"]) == 7 and len(authority["authority_records"]) == 47
            and len(authority["overclaim_routes"]) == 14, "E_AUTHORITY_ROWS", "7/47/14")
    authority_counts = {"planned_core_gate_records": 37, "complete_authority_records": 47,
                        "material_validated_gates": 0, "experimental_validated_gates": 0,
                        "external_comprehensive_validated_gates": 0, "overclaim_routes": 14}
    require({key: authority["counts"][key] for key in authority_counts} == authority_counts,
            "E_AUTHORITY_COUNTS", repr(authority["counts"]))
    require(authority["authority_summary"]["material_validation"] is False
            and authority["authority_summary"]["experimental_validation"] is False
            and authority["authority_summary"]["comprehensive_external_primary_literature_validation"] is False,
            "E_AUTHORITY_CEILING", repr(authority["authority_summary"]))

    disposition_expected = {"source_dispositions": 83, "supplemental_dispositions": 6,
                            "open_source_dispositions": 44, "open_supplemental_dispositions": 1,
                            "source_orphans": 0, "duplicate_source_membership": 0, "external_authority_promotions": 0}
    require({key: disposition["counts"][key] for key in disposition_expected} == disposition_expected, "E_DISPOSITION_COUNTS", repr(disposition["counts"]))
    require(disposition["counts"]["source_disposition_distribution"] == {"CORRECT": 35, "PRESERVE": 34, "THEORY_ONLY": 5, "UNVERIFIED": 9},
            "E_DISPOSITION_DISTRIBUTION", repr(disposition["counts"]["source_disposition_distribution"]))
    carry_expected = {"canonical_owner_duplicate_check_records": 326, "closed_topical_routes": 1,
                      "equation38_supersession_bindings": 1, "external_authority_promotions": 0,
                      "inherited_phase063_owner_records": 308, "multiply_owned_open_routes": 0,
                      "new_phase064_blockers": 0, "open_source_dispositions": 44,
                      "open_supplemental_acquisition_routes": 1, "open_topical_routes": 17,
                      "ownerless_open_routes": 0, "phase057_provisional_routes": 36,
                      "phase066_correction_observations": 11, "phase067_finding_observations": 9,
                      "phase068_authority_routes": 14, "phase_ceiling": "CONDITIONAL_P064",
                      "ref6_original_full_text": "FULL_TEXT_READ_4_OF_4", "ref7_original_full_text": "GROUND_NOT_FOUND",
                      "residual_topical_routes": 4, "source_disposition_links": 83, "status": "PASS_WITH_CONCERNS",
                      "supplemental_disposition_links": 6, "topical_routes": 18}
    require(carry["gate_summary"] == carry_expected, "E_CARRY", repr(carry["gate_summary"]))
    require(carry["equation38_supersession_binding"]["status"] == "CLOSED_BOUND_IN_STEP69_1"
            and carry["equation38_supersession_binding"]["retained_crop_raw_pixel_sha256"]
            == "63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978",
            "E_EQ38_BINDING", repr(carry["equation38_supersession_binding"]))

    return {
        "activation": {"gate": "PASS_P064_PLAN_ACTIVATION", "controls": 6},
        "source_process_read": {"sources": 83, "text_files": 78, "text_lines": 12508, "pdfs": 3, "pages": 129,
                                "images": 2, "history_commits": 14, "phase057_observations": 36,
                                "p4_state": "SKIPPED_D3_NOT_APPROVED", "coverage_gaps": 0},
        "literature": {"jcp147_pages": 10, "ref6_pages": 4, "ref6_sha256": sources["REF6"]["authority"]["raw_sha256"],
                       "ref7_doi": "10.1063/1.4802584", "ref7_state": "GROUND_NOT_FOUND",
                       "wrong_doi_rejected": "10.1063/1.4802005", "equation_chain": 8, "applicability_conditions": 3},
        "ratio_transfer": {"fredholm_class": ratio["fredholm_rederivation"]["problem_class"],
                           "volterra_class": ratio["volterra_rederivation"]["problem_class"],
                           "eq38_corrected": "exp(K*sigma*mu)", "timebase_factor": 3600,
                           "transfer_coordinate": "DIRECTED_VOLTAGE_X", "sufficient_condition": "q<1"},
        "problem_runtime": {"problem_classes": 3, "ratio_applicable": [False, False, True],
                            "findings": {"P0": 1, "P1": 5, "P2": 3}, "official_mutation_runs": 10,
                            "independent_runtime_sets": 2},
        "validation_authority": {"core_records": 37, "complete_records": 47, "axes": 7,
                                 "overclaim_routes": 14, "material_validated": 0,
                                 "experimental_validated": 0, "external_comprehensive_validated": 0},
        "disposition_carry": {"source": 83, "supplemental": 6,
                              "distribution": {"CORRECT": 35, "PRESERVE": 34, "THEORY_ONLY": 5, "UNVERIFIED": 9},
                              "observations": {"phase057": 36, "step66": 11, "step67": 9},
                              "topical_routes": 18, "open": 17, "closed": 1, "owner_universe": 326,
                              "new_blockers": 0, "external_promotions": 0},
        "independent_numeric": independent_numeric_checks(),
        "authority": {"external_scientific": False, "external_material": False, "experimental": False,
                      "comprehensive_external_primary_literature": False, "ref7_method_content": False,
                      "canonical": False, "defect_repair": False,
                      "identifiability": False, "held_out_fitting": False, "final_latex_pdf": False,
                      "publication_ready": False},
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
        (REPORT_PATH, report, "REPORT", "# Phase 064 v1.0.23 Lineage Report G", "Gate: ", "상태: "),
        (GATE_RESULT_PATH, gate, "GATE_RESULT", "# Phase 064 Step 69.2 Integrated Gate Result", "Selected Gate: ", "Status: "),
        (PHASE_RESULT_PATH, phase, "PHASE_RESULT", "# Phase 064 Result — v1.0.23 Full Lineage Reaudit", "Exclusive Gate: ", "Status: "),
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
        require("Ref. 7" in joined and "GROUND_NOT_FOUND" in joined and "PHASE-071-PRIMARY-SOURCE-ACQUISITION" in joined,
                f"E_{diagnostic}_REF7_ROUTE", path)
        require("PASS_P064_LINEAGE_G" in joined and "FAIL_P064" in joined and "Alternatives rejected" in joined,
                f"E_{diagnostic}_ALTERNATIVES", path)
        require("Phase 065 detailed plan" in joined and "Step 70" in joined, f"E_{diagnostic}_NEXT", path)

    parent = content[PARENT_LEDGER_PATH]
    active = content[ACTIVE_LEDGER_PATH]
    handover = content[HANDOVER_PATH]
    parent_row, parent_cells = exact_table_row(parent, "| 064 |", "E_PARENT_LEDGER_ROW")
    require(len(parent_cells) == 12 and parent_cells[0] == "064" and parent_cells[5] == "CONDITIONAL_PENDING_PERSISTENCE", "E_PARENT_LEDGER_STATUS", parent_row)
    require(LEDGER_PROGRESS in parent_row, "E_PARENT_LEDGER_PROGRESS", parent_row)
    require(all(token in parent_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 065 detailed plan", "Step 70")), "E_PARENT_LEDGER_RECOVERY", parent_row)
    active_phase_row, active_phase_cells = exact_table_row(active, "| 064 |", "E_ACTIVE_LEDGER_ROW")
    require(len(active_phase_cells) == 10 and active_phase_cells[0] == "064" and active_phase_cells[4] == "CONDITIONAL_PENDING_PERSISTENCE", "E_ACTIVE_LEDGER_STATUS", active_phase_row)
    require(LEDGER_PROGRESS in active_phase_row, "E_ACTIVE_LEDGER_PROGRESS", active_phase_row)
    require(all(token in active_phase_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 065 detailed plan", "Step 70")), "E_ACTIVE_LEDGER_RECOVERY", active_phase_row)
    require([line for line in phase if line.startswith("Plan activation과 cumulative Steps 64–")] == [PHASE_RESULT_PROGRESS_LINE],
            "E_PHASE_RESULT_PROGRESS")
    exact_section_body(active, "## Next Exact Step", NEXT_EXACT_STEP_BODY, "E_ACTIVE_NEXT_EXACT_STEP")
    active_prior_row, active_prior_cells = exact_table_row(active, "| Step 69.1 |", "E_ACTIVE_PRIOR_STEP_ROW")
    require(len(active_prior_cells) == 6 and active_prior_cells[2] == f"`{PARENT_COMMIT}`"
            and active_prior_cells[3] == "pushed/live-remote verified" and active_prior_cells[4] == "yes",
            "E_ACTIVE_PRIOR_STEP_STATUS", active_prior_row)
    require(all(token in active_prior_row for token in (STEP68, SUBJECT.replace("close v1023 lineage gate", "disposition v1023 lineage"),
                                                         "PASS_P064_STEP69_1_PERSISTENCE")),
            "E_ACTIVE_PRIOR_STEP_RECOVERY", active_prior_row)
    active_step_row, active_step_cells = exact_table_row(active, "| Step 69.2 |", "E_ACTIVE_STEP_ROW")
    require(len(active_step_cells) == 6 and active_step_cells[0] == "Step 69.2" and active_step_cells[2] == "`PENDING_AT_PRECOMMIT_BY_DESIGN`", "E_ACTIVE_STEP_STATUS", active_step_row)
    require(all(token in active_step_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 065 detailed plan", "Step 70")), "E_ACTIVE_STEP_RECOVERY", active_step_row)
    handover_prior_row, handover_prior_cells = exact_table_row(handover, "| Phase 064 Step 69.1 |", "E_HANDOVER_PRIOR_STEP_ROW")
    require(len(handover_prior_cells) == 4 and handover_prior_cells[:2] == ["Phase 064 Step 69.1", "Step 69.1"]
            and PARENT_COMMIT in handover_prior_row and "PASS_P064_STEP69_1_PERSISTENCE" in handover_prior_row,
            "E_HANDOVER_PRIOR_STEP_STATUS", handover_prior_row)
    handover_step_row, handover_step_cells = exact_table_row(handover, "| Phase 064 Step 69.2 |", "E_HANDOVER_STEP_ROW")
    require(len(handover_step_cells) == 4 and handover_step_cells[:2] == ["Phase 064 Step 69.2", "Step 69.2"], "E_HANDOVER_STEP_STATUS", handover_step_row)
    require(all(token in handover_step_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 065 detailed plan", "Step 70")), "E_HANDOVER_STEP_RECOVERY", handover_step_row)
    expected_current = "16. 현재 Phase 상태: Phase 064 `CONDITIONAL_PENDING_PERSISTENCE`, Current checkpoint: Step 69.2 precommit `CONDITIONAL_P064`"
    require([line for line in handover if line.startswith("16. 현재 Phase 상태:")] == [expected_current], "E_HANDOVER_CURRENT_STATUS")


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
        records.append({"path": path, "sha256_lf": sha256(lf_bytes(raw)), "bytes": len(raw),
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
        "schema_version": "P064-STEP69.2-1", "phase": "064", "step": "69.2", "generated_date": "2026-08-30",
        "gate": GATE, "status": STATUS, "expected_parent": PARENT_COMMIT, "expected_subject": SUBJECT,
        "authority_boundary": AUTHORITY_BOUNDARY, "authority": copy.deepcopy(integrated["authority"]),
        "validator_identity": {"path": VALIDATOR_PATH, "sha256_lf": sha256(validator_raw), "bytes_lf": len(validator_raw),
                               "source_policy": "NO_PRODUCTION_IMPORT_OR_EXECUTION"},
        "exact_eight": {"count": 8, "paths": FINAL_PATHS, "result_first": True, "json_last": True},
        "repository": stable_repository_projection(repository_snapshot(allow_final_dirt=True)),
        "input_inventory": inputs, "step_commit_inventory": step_commit_inventory(),
        "historical_execution": {"precommit": precommit, "persistence": persistence, "unit_count": 7,
                                 "invocation_count": 15, "pass_count": 15},
        "integrated_contracts": integrated, "output_contract": outputs,
        "negative_control_contract": {"named_count": 37, "strict_json_count": 6, "git_boundary_count": 17,
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
        ("E_FINAL_IDENTITY", (document["phase"], document["step"], document["generated_date"]), ("064", "69.2", "2026-08-30")),
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
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["source_process_read"].__setitem__("sources", 82))
    add("E_FINAL_OUTPUTS", lambda d: d["output_contract"].__setitem__("result_first", False))
    add("E_FINAL_NEGATIVE_CONTRACT", lambda d: d["negative_control_contract"].__setitem__("singleton_required", False))
    add("E_FINAL_DETERMINISM", lambda d: d["determinism"].__setitem__("byte_identical", False))
    add("E_FINAL_AUTHORITY_BOUNDARY", lambda d: d.__setitem__("authority_boundary", "overclaim"))
    add("E_FINAL_SEMANTIC_HASH", lambda d: d.__setitem__("semantic_sha256", "0" * 64), False)
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["ratio_transfer"].__setitem__("eq38_corrected", "exp(K*r*mu)"))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["literature"].__setitem__("ref7_state", "FULL_TEXT_READ"))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["problem_runtime"].__setitem__("official_mutation_runs", 9))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["validation_authority"].__setitem__("core_records", 36))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["disposition_carry"].__setitem__("new_blockers", 1))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["independent_numeric"]["c_rate_timebase"].__setitem__("hour_to_second_factor", 1))
    add("E_FINAL_HISTORICAL", lambda d: d["historical_execution"]["precommit"].__setitem__("invocation_count", 7))
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
            next(line for line in c[ACTIVE_LEDGER_PATH] if line.startswith("| Step 69.2 |")),
            next(line for line in c[ACTIVE_LEDGER_PATH] if line.startswith("| Step 69.2 |")).replace(PARENT_COMMIT, "0" * 40),
        )),
        ("E_ACTIVE_NEXT_EXACT_STEP", lambda c: replace_exact(
            c[ACTIVE_LEDGER_PATH], NEXT_EXACT_STEP_BODY,
            NEXT_EXACT_STEP_BODY.replace("Step 69.2 eight declared paths", "Step 69.1 eight declared paths"),
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
    policy_cases = (
        ("E_SOURCE_POLICY_IMPORT_ALLOWLIST", lambda: validate_source_policy_text(
            VALIDATOR.read_text(encoding="utf-8") + "\nimport Codex.rogue\n", "negative-import.py")),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "Codex/work/v1023_phase064/build_unapproved.py"])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "./Codex/work/v1023_phase064/build_unapproved.py"])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", str(ROOT / "Codex/work/v1023_phase064/build_unapproved.py")])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "-c", "exec(open('Codex/work/v1023_phase064/build_unapproved.py').read())"])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "-c", "print(1)", UNIT_SPECS[0]["validator"]])),
        ("E_SOURCE_POLICY_EXECUTION_ALLOWLIST", lambda: validate_python_execution_argv(
            ["python", "-m", "rogue", UNIT_SPECS[0]["validator"]])),
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
    prefix = "phase064-step692-git-boundary-"
    root = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    work = root / "work"
    origin = root / "origin.git"
    expected_paths = set(FINAL_PATHS)
    try:
        work.mkdir()
        git(["init", "--initial-branch=main"], cwd=work)
        git(["config", "core.autocrlf", "false"], cwd=work)
        git(["config", "user.email", "phase064-fixture@example.invalid"], cwd=work)
        git(["config", "user.name", "Phase 064 Fixture"], cwd=work)
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
        git(["branch", "-D", "main"], cwd=work)
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
        prefix = "phase064-step692-git-boundary-"
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
    temp_path = ARTIFACT.with_name(ARTIFACT.name + ".tmp-step692")
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


def execute_validation(*, collect: bool, mode: str, expected_commit: str | None, run_negative: bool, run_determinism: bool) -> int:
    validate_source_policy()
    if not collect:
        stored, stored_raw = read_stored()
    precommit = fresh_historical_precommit()
    persistence = fresh_historical_persistence()
    expected, expected_raw = deterministic_pair(precommit, persistence)
    require(not document_diagnostics(expected, expected), "E_FRESH_DOCUMENT", repr(sorted(document_diagnostics(expected, expected))))
    if collect:
        negative_passed, negative_total = run_negative_controls(expected)
        git_passed, git_total = run_git_boundary_controls()
        atomic_collect(expected_raw)
        print(f"PASS_P064_STEP69_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print("PASS_P064_STEP69_2_DETERMINISM 2/2")
        print("CONDITIONAL_P064 collect=JSON_LAST result_first=true historical=15/15 ref7=GROUND_NOT_FOUND")
        return 0
    require(not document_diagnostics(stored, expected), "E_STORED_DOCUMENT", repr(sorted(document_diagnostics(stored, expected))))
    require(stored_raw == expected_raw, "E_STORED_BYTE_IDENTITY", ARTIFACT_PATH)
    automatic_full = mode in {"precommit", "persistence"}
    if run_negative or automatic_full:
        negative_passed, negative_total = run_negative_controls(stored)
        git_passed, git_total = run_git_boundary_controls()
        print(f"PASS_P064_STEP69_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
    if run_determinism or automatic_full:
        print("PASS_P064_STEP69_2_DETERMINISM 2/2")
    if mode == "precommit":
        validate_staged()
        print("PASS_P064_STEP69_2_STAGED exact-eight=8/8 historical=15/15")
    elif mode == "persistence":
        require(expected_commit is not None, "E_EXPECTED_COMMIT", "required")
        validate_persistence(expected_commit)
        print(f"{PERSISTENCE} commit={expected_commit}")
    else:
        print("CONDITIONAL_P064 artifact=true historical=15/15 ref7=GROUND_NOT_FOUND")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="artifact")
    parser.add_argument("--expected-commit")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    require(not (args.collect and args.mode != "artifact"), "E_CLI_MODE", "collect with repository mode")
    if not args.collect and not ARTIFACT.is_file():
        raise ValidationError("E_VALIDATION_ARTIFACT_MISSING", ARTIFACT_PATH)
    return execute_validation(collect=args.collect, mode=args.mode, expected_commit=args.expected_commit,
                              run_negative=args.run_negative_probes, run_determinism=args.determinism_check)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL_P064_STEP69_2: {error}")
        raise SystemExit(1)
