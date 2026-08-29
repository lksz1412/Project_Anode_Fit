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
VALIDATOR_PATH = "Codex/work/v1022_phase063/validate_phase063_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_063_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_063_V1022_LINEAGE_REPORT_F.md"
GATE_RESULT_PATH = "Codex/results/PHASE_063_STEP_063_2_GATE_RESULT.md"
PHASE_RESULT_PATH = "Codex/results/PHASE_063_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT_COMMIT = "6c46cf81bf88394dc23e0b86943297cca1affa89"
SUBJECT = "audit(phase063): close v1022 lineage gate"
GATE = "PASS_P063_LINEAGE_F"
PERSISTENCE = "PASS_P063_STEP63_2_PERSISTENCE"

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
    "PASS_P063_LINEAGE_F certifies internal v1.0.22 lineage-audit completeness only; "
    "it does not certify external scientific, material, experimental or primary-literature truth, "
    "canonical selection, defect repair, parameter identifiability, held-out fitting, final equation "
    "freeze, final LaTeX/PDF or publication readiness."
)


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def run_process(argv: list[str], *, cwd: pathlib.Path = ROOT, timeout: int = 300, check: bool = False) -> subprocess.CompletedProcess[bytes]:
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
    entries = [part.decode("utf-8") for part in git(["status", "--porcelain=v1", "-z"], cwd=cwd).stdout.split(b"\0") if part]
    paths: set[str] = set()
    index = 0
    while index < len(entries):
        entry = entries[index]
        require(len(entry) >= 4 and entry[2] == " ", "E_STATUS_PARSE", repr(entry))
        paths.add(entry[3:])
        if entry[0] in {"R", "C"}:
            index += 1
            require(index < len(entries), "E_STATUS_PARSE", "rename source missing")
        index += 1
    return paths


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


ACTIVATION = "4e7686ec623a2e82a0ef5433e60a8565b0ad039f"
STEP58 = "2ccee1af3a59a3a1e5c9fe7192e4f916c454521a"
STEP59 = "07a0f3ead16a072550919b86d1d41580682fd92d"
STEP60 = "4088f48ca191fdb8abe52e8f4fb10de10f2eeba3"
STEP61 = "89bd7c7c27a827ec2322db25fe9e2634874c2f9d"
STEP62 = "eb847ea85018b7703c7adcfe74b8b665ec8c9b1c"
STEP63_1 = PARENT_COMMIT


def unit(unit: str, commit: str, parent: str, subject: str, validator: str, validator_sha256: str, paths: list[str], invocations: list[dict[str, Any]]) -> dict[str, Any]:
    return {"unit": unit, "commit": commit, "parent": parent, "subject": subject, "validator": validator,
            "validator_sha256": validator_sha256, "paths": paths, "invocations": invocations}


def invocation(args: list[str], terminal: str) -> dict[str, Any]:
    return {"args": args, "terminal_prefix": terminal}


UNIT_SPECS = [
    unit("ACTIVATION", ACTIVATION, "69d938da0f5649d6342364c96bf612488879a8f8", "docs(phase063): plan v1022 lineage reaudit",
         "Codex/work/v1022_phase063/validate_phase063_plan.py", "3817cc1c01aae71835eeb58bfc780dbd8038179d651852fcf8162a4e3d7b1f54",
         ["Codex/plans/2026-08-28-phase063-v1022-lineage-detailed-plan.md", HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
          "Codex/results/PHASE_063_PLAN_ACTIVATION_RESULT.md", "Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json", "Codex/work/v1022_phase063/validate_phase063_plan.py"],
         [invocation(["--content-only", "--run-negative-probes", "--determinism-check"], "PASS_P063_PLAN_CONTENT"),
          invocation(["--verify-staged"], "PASS_P063_PLAN_ACTIVATION_STAGED")]),
    unit("STEP58", STEP58, ACTIVATION, "audit(phase063): freeze v1022 source process topology",
         "Codex/work/v1022_phase063/validate_phase063_step58.py", "2cc604d0b5be9a2af68f2d4ce19e5148364e95c971cac90cbe0f8b2b4eed7b8b",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_063_STEP_058_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
          "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json", "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json",
          "Codex/work/v1022_phase063/build_phase063_step58_source_process_topology.py", "Codex/work/v1022_phase063/validate_phase063_step58.py"],
         [invocation(["--verify-staged", "--run-negative-probes", "--determinism-check"], "PASS_P063_STEP58_STAGED")]),
    unit("STEP59", STEP59, STEP58, "audit(phase063): rederive v1022 equation material",
         "Codex/work/v1022_phase063/validate_phase063_step59.py", "355008dd78f0d362f25e592e4c6583f24fd60f5f26b1d9721d47f5fa6edaf1ca",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_063_STEP_059_EQUATION_MATERIAL_REDERIVATION_RESULT.md",
          "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json", "Codex/work/v1022_phase063/build_phase063_step59_equation_material_rederivation.py",
          "Codex/work/v1022_phase063/validate_phase063_step59.py"],
         [invocation(["--verify-staged", "--run-negative-probes", "--determinism-check"], "PASS_P063_STEP59_STAGED")]),
    unit("STEP60", STEP60, STEP59, "audit(phase063): bound v1022 literature scope",
         "Codex/work/v1022_phase063/validate_phase063_step60.py", "bbd73b931dd1c5d838c8d371a03d2e927c88ec3cf5f179984f5732b495a91c59",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_063_STEP_060_LITERATURE_SCOPE_RESULT.md",
          "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json", "Codex/work/v1022_phase063/build_phase063_step60_literature_scope.py",
          "Codex/work/v1022_phase063/validate_phase063_step60.py"],
         [invocation(["--verify-staged", "--run-negative-probes", "--determinism-check"], "PASS_P063_STEP60_STAGED")]),
    unit("STEP61", STEP61, STEP60, "audit(phase063): attest v1022 code runtime delta",
         "Codex/work/v1022_phase063/validate_phase063_step61.py", "cdb4d307455a02be988edb243c929e8b81d5fab0221b10349e41a8ebbb1e6d37",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_063_STEP_061_CODE_RUNTIME_DELTA_RESULT.md",
          "Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json", "Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json",
          "Codex/work/v1022_phase063/build_phase063_step61_code_runtime_delta.py", "Codex/work/v1022_phase063/validate_phase063_step61.py"],
         [invocation(["--verify-staged", "--run-negative-probes", "--determinism-check"], "PASS_P063_STEP61_STAGED")]),
    unit("STEP62", STEP62, STEP61, "audit(phase063): close v1022 review adoption build",
         "Codex/work/v1022_phase063/validate_phase063_step62.py", "5cca0fda1a3f19eb36881d96b37c3ef1f5fd1ea9d6e0e83698f7130499a75586",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_063_STEP_062_REVIEW_ADOPTION_CLOSURE_RESULT.md",
          "Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json", "Codex/work/v1022_phase063/build_phase063_step62_review_adoption_closure.py",
          "Codex/work/v1022_phase063/validate_phase063_step62.py"],
         [invocation(["--verify-staged", "--run-negative-probes", "--determinism-check"], "PASS_P063_STEP62_STAGED")]),
    unit("STEP63_1", STEP63_1, STEP62, "audit(phase063): disposition v1022 lineage",
         "Codex/work/v1022_phase063/validate_phase063_step63_dispositions.py", "6bb50892bb9d81d01be911b6f4825b8bfd35c90f4c1fac1bc9b839004d2853a9",
         [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_063_STEP_063_1_DISPOSITION_RESULT.md",
          "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json", "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json",
          "Codex/work/v1022_phase063/build_phase063_step63_dispositions.py", "Codex/work/v1022_phase063/validate_phase063_step63_dispositions.py"],
         [invocation(["--verify-staged", "--run-negative-probes", "--determinism-check"], "PASS_P063_STEP63_1_STAGED")]),
]


ARTIFACT_SPECS = {
    "Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json": (ACTIVATION, "ec6e78c33202bc05c42bbc618850e5f21feae9570f069a01688f89cf341004c9"),
    "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json": (STEP58, "519968b5224db724e22f713a1ff47b9202dc77806a83d9917bc7845cd2cd0d7a"),
    "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json": (STEP58, "5d2aa9d9f7361471429dbd37dfcfad46d26b657c6ab3d421a1e9f58709144376"),
    "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json": (STEP59, "5753fd06737641acde52568a0bb22a8fabe9d37bbc3a43d4a743e884ff76ad02"),
    "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json": (STEP60, "77fa60e9ceeea086f8a6dde2cb3719a82357d01669e8c126e013c126e9725efd"),
    "Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json": (STEP61, "691a11a9fdb8b7dc636893f8ffa822f119b8afbd8b0ac56b1c3ba8220faa7d0e"),
    "Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json": (STEP61, "5fb79f20bf6a8d1fa4345f9d66e35e1f595abd02f597c7acd8410434f8146f1b"),
    "Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json": (STEP62, "8e627698b92f87c40a6dee57bc86cb8339cc17d0f78b1be4c9291d915161d2ff"),
    "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json": (STEP63_1, "cb50d7f94066fe1d8238e7fc1ebe8394271dbda8d0fd03a16aba0104fa752f8b"),
    "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json": (STEP63_1, "c44c4ee1366ae53969379c0b698e707862cbc290b209edf7ef80d9965a01eb46"),
}

RESULT_SPECS = {
    "Codex/results/PHASE_063_PLAN_ACTIVATION_RESULT.md": (ACTIVATION, "fe6b481e1e962ea9ca2964b4e1b5b1c91dcd875d36b33b1218af03023c5ae082"),
    "Codex/results/PHASE_063_STEP_058_SOURCE_PROCESS_TOPOLOGY_RESULT.md": (STEP58, "8b9a7d4f3276af54796a82dfcef6885b5b8cf23df20822b601f24950152af180"),
    "Codex/results/PHASE_063_STEP_059_EQUATION_MATERIAL_REDERIVATION_RESULT.md": (STEP59, "6d7cb13ca9fd3c820900bfd00a8d1071272ae7c6e10ffa804554291753f815e1"),
    "Codex/results/PHASE_063_STEP_060_LITERATURE_SCOPE_RESULT.md": (STEP60, "a8d589821dade9e0e0bb3abbfb5c08d16908be1597d39e3230760cbb7a86c0c1"),
    "Codex/results/PHASE_063_STEP_061_CODE_RUNTIME_DELTA_RESULT.md": (STEP61, "6eb6e6d3972e15f66996e2b5deb2c21ae5e7142713c17236061e49d498299370"),
    "Codex/results/PHASE_063_STEP_062_REVIEW_ADOPTION_CLOSURE_RESULT.md": (STEP62, "e852f89349171fa1be7c0f5a4baa4d9c0cc377998a4e5aa72d0a239d6fcc8dee"),
    "Codex/results/PHASE_063_STEP_063_1_DISPOSITION_RESULT.md": (STEP63_1, "e8af9152f57ad778345e1ec68773a4ac1db1bd1446cfe27db5e03cca59f2936b"),
}

EXPECTED_TOP_KEYS = {
    "Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json": "active_branch authority_boundary baseline_commit checks control_contract date determinism exact_allowlist expected_parent expected_subject gate intent_contract main_fixed_tip manifest_contract negative_control_summary negative_controls output_contract phase plan_contract predecessor_snapshot protected_branch schema_version status supplemental_contract unit validation_summary".split(),
    "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json": "activation_commit artifact_kind authority_boundary baseline_commit builder citation_genealogy commit_genealogy competing_phase057_linkage counts cross_version_v1021_v1022 denominator_policy gate generated_date history_summary human_read_findings manifest pdf_root_edges phase phase057_finding_routes phase057_observation_inputs schema_version sources status step supplemental_process_control tex_dependency_edges tex_structure_summary".split(),
    "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json": "artifact_kind authority_boundary baseline_commit counts generated_date human_review_contract manifest_read_records pdf_page_attestations phase phase057_observation_read_records schema_version source_topology_semantic_sha256 status step supplemental_read_record".split(),
    "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json": "artifact_kind authority_boundary baseline_commit builder counts display_equation_inventory expected_parent finding_summary findings gate generated_date input_artifacts manual_rederivation_evidence numeric_rederivation phase phase057_provisional_routes result_first_contract schema_version semantic_sha256 source_inventory status step".split(),
    "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json": "artifact_kind authority_axis_profiles authority_boundary baseline_commit bibliography_identity_conflicts bibliography_occurrences_all_text_partitions builder citation_occurrences_all_text_partitions claim_candidate_lines_all_text_partitions counts denominator_policy doi_occurrences_all_text_partitions equation_candidates_all_text_partitions expected_parent final_release_citation_genealogy finding_summary findings gate generated_date independent_quantity_checks input_artifacts manual_literature_scope_evidence manual_unkeyed_bibliography_occurrences phase result_first_contract schema_version semantic_sha256 source_read_attestations status step tex_delimited_math_candidates_all_text_partitions".split(),
    "Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json": "artifact_kind authority_boundary baseline_commit counts endpoint_predicate endpoints expected_parent expected_subject finding_summary findings generated_date phase result_first_contract schema_version semantic_sha256 shared_blob_groups static_contracts step symbol_deltas theory_code_concordance".split(),
    "Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json": "artifact_kind authority_boundary baseline_commit counts expected_parent generated_date independent_probes isolation official_runs phase result_first_contract runtimes schema_version semantic_sha256 step".split(),
    "Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json": "adoption_routes authority build_audit code_mention_boundary competing_occurrences counts evidence_links finding_adjudications frozen_baseline gate input_commit phase proposal_families result_first schema state_chronology step".split(),
    "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json": "artifact_kind authority_boundary baseline_commit counts gate input_commit inputs phase result_first schema_version source_contract source_dispositions step supplemental_process_disposition".split(),
    "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json": "artifact_kind authority_boundary baseline_commit canonical_debt_routing canonical_owner_duplicate_check_universe gate gate_summary inherited_carry_items inherited_phase060_blockers inherited_phase061_blockers input_commit inputs new_phase063_blockers open_finding_ownership phase phase057_finding_routes phase063_audit_finding_routes result_first schema_version source_disposition_links step".split(),
}


def validate_source_policy() -> None:
    tree = ast.parse(VALIDATOR.read_text(encoding="utf-8"), filename=VALIDATOR_PATH)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name for alias in node.names]
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            require(not any(name == "Claude" or name.startswith("Claude.") or name in {"importlib", "runpy"} for name in names), "E_SOURCE_POLICY_IMPORT", repr(names))
        if isinstance(node, ast.Call):
            require(not (isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "__import__"}), "E_SOURCE_POLICY_CALL", ast.dump(node.func, include_attributes=False))
            for keyword in node.keywords:
                require(not (keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True), "E_SOURCE_POLICY_SHELL", "shell=True")


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
    return objects, {"machine_count": 10, "machine_records": machine_records, "result_count": 7,
                     "result_records": result_records, "strict_duplicate_keys": True,
                     "nonfinite_rejected": True, "full_recursive_traversal": True}


def step_commit_inventory() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        require(git_text(["rev-parse", f"{spec['commit']}^"]) == spec["parent"], "E_UNIT_PARENT", spec["unit"])
        require(git_text(["show", "-s", "--format=%s", spec["commit"]]) == spec["subject"], "E_UNIT_SUBJECT", spec["unit"])
        changed = nul_paths(git(["diff-tree", "--no-commit-id", "--name-only", "-r", "-z", spec["commit"]]).stdout)
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
    claude_tracked = git_text(["diff", "--name-only", PARENT_COMMIT, "--", "Claude"]).splitlines()
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
    process = run_process(["py", "-3.12", "-c", "import PIL,numpy,pypdf,sys;print(sys.executable)"], timeout=60)
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
    changed_after_commit = set(git_text(["diff", "--name-only", commit, PARENT_COMMIT]).splitlines())
    dirty_now = set(git_text(["diff", "--name-only"]).splitlines()) | set(git_text(["diff", "--cached", "--name-only"]).splitlines())
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
    prefix = f"phase063-step632-stage-{spec['unit'].lower()}-"
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
        staged = nul_paths(git(["diff", "--cached", "--name-only", "-z"], cwd=clone).stdout)
        require(staged == set(spec["paths"]), "E_FIXTURE_STAGED_SET", spec["unit"])
        require(not nul_paths(git(["diff", "--name-only", "-z"], cwd=clone).stdout), "E_FIXTURE_UNSTAGED", spec["unit"])
        require(not nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=clone).stdout), "E_FIXTURE_UNTRACKED", spec["unit"])
        require(git_text(["rev-parse", "HEAD"], cwd=clone) == spec["parent"], "E_FIXTURE_PARENT", spec["unit"])
        require(live_tip(ACTIVE_BRANCH, cwd=clone) == spec["parent"], "E_FIXTURE_LIVE", spec["unit"])
    except Exception:
        remove_temp_tree(parent, prefix)
        raise
    return parent, clone, restored


def make_historical_persistence_clone(spec: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    prefix = f"phase063-step632-persist-{spec['unit'].lower()}-"
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


def execute_historical(executable: str, clone: pathlib.Path, spec: dict[str, Any], args: list[str], terminal: str, location: str) -> dict[str, Any]:
    raw = (clone / spec["validator"]).read_bytes()
    require(sha256(raw) == spec["validator_sha256"], "E_HISTORICAL_VALIDATOR_SHA", spec["unit"])
    process = run_process([executable, spec["validator"], *args], cwd=clone, timeout=2400)
    stdout = process.stdout.decode("utf-8", errors="replace")
    stderr = process.stderr.decode("utf-8", errors="replace")
    require(process.returncode == 0, "E_HISTORICAL_EXIT", f"{spec['unit']}:{stdout[-1600:]}:{stderr[-1600:]}")
    require(sum(line.startswith(terminal) for line in stdout.splitlines()) == 1, "E_HISTORICAL_TERMINAL", f"{spec['unit']}:{terminal}")
    return {"unit": spec["unit"], "commit": spec["commit"], "validator_path": spec["validator"],
            "validator_sha256": spec["validator_sha256"], "args": args, "terminal_prefix": terminal,
            "terminal_count": 1, "exit_code": 0, "stderr_bytes": len(process.stderr),
            "stdout_lf_bytes": len(lf_bytes(process.stdout)), "stdout_lf_sha256": sha256(lf_bytes(process.stdout)),
            "banners": [line for line in stdout.splitlines() if line.startswith(("PASS", "FAIL"))],
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
        prefix = f"phase063-step632-stage-{spec['unit'].lower()}-"
        try:
            for current in spec["invocations"]:
                records.append(execute_historical(executable, clone, spec, current["args"], current["terminal_prefix"],
                                                  "DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE"))
            require_restored_inputs_unchanged(clone, restored, spec["unit"])
            require(nul_paths(git(["diff", "--cached", "--name-only", "-z"], cwd=clone).stdout) == set(spec["paths"]), "E_HISTORICAL_STAGE_MUTATION", spec["unit"])
            require(not nul_paths(git(["diff", "--name-only", "-z"], cwd=clone).stdout), "E_HISTORICAL_WORKTREE_MUTATION", spec["unit"])
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
        prefix = f"phase063-step632-persist-{spec['unit'].lower()}-"
        try:
            terminal = "PASS_P063_PLAN_ACTIVATION_PERSISTENCE" if spec["unit"] == "ACTIVATION" else f"PASS_P063_{spec['unit']}_PERSISTENCE"
            if spec["unit"] == "STEP63_1":
                terminal = "PASS_P063_STEP63_1_PERSISTENCE"
            args = ["--verify-persistence", "--expected-commit", spec["commit"]]
            records.append(execute_historical(executable, clone, spec, args, terminal,
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
    gas = 8.31446261815324
    faraday = 96485.33212
    temperature = 298.15
    si_molar_mass_g = 28.0855
    carbon_molar_mass_g = 12.011
    li15si4 = 3.75 * faraday / (3.6 * si_molar_mass_g)
    li44si = 4.4 * faraday / (3.6 * si_molar_mass_g)
    lic6 = faraday / (6.0 * 3.6 * carbon_molar_mass_g)
    barrier_kj = gas * temperature * math.log(3600.0) / 1000.0
    blend_fraction = 0.3 * 3117.0 / (0.3 * 3117.0 + 0.7 * 372.0)
    fwhm_factor = 4.0 * math.acosh(math.sqrt(2.0))
    omega = 3.0 * gas * temperature
    spinodal_lo = (1.0 - math.sqrt(1.0 - 2.0 * gas * temperature / omega)) / 2.0
    spinodal_hi = 1.0 - spinodal_lo
    require(abs(li15si4 - 3578.5567) < 0.001, "E_NUMERIC_LI15SI4", repr(li15si4))
    require(abs(li44si - 4198.8399) < 0.001, "E_NUMERIC_LI44SI", repr(li44si))
    require(abs(lic6 - 371.9019) < 0.001, "E_NUMERIC_LIC6", repr(lic6))
    require(abs(barrier_kj - 20.2994) < 0.0001, "E_NUMERIC_BARRIER", repr(barrier_kj))
    require(abs(blend_fraction - 0.7821831869510665) < 2e-15, "E_NUMERIC_BLEND", repr(blend_fraction))
    require(0.0 < spinodal_lo < 0.5 < spinodal_hi < 1.0, "E_NUMERIC_SPINODAL", repr((spinodal_lo, spinodal_hi)))
    return {"faraday_capacity_mAh_g": {"Li15Si4": li15si4, "Li4.4Si": li44si, "LiC6": lic6},
            "c_rate_timebase": {"hour_to_second_factor": 3600, "barrier_shift_kJ_mol_at_298_15K": barrier_kj},
            "blend_fraction": {"m_Si": 0.3, "q_Si": 3117.0, "q_graphite": 372.0, "f_Si": blend_fraction},
            "equilibrium_kernel": {"logistic_fwhm_over_w": fwhm_factor, "regular_solution_omega_over_RT": 3.0,
                                   "spinodal_roots": [spinodal_lo, spinodal_hi]},
            "independent_implementation": True}


def integrated_contracts(objects: dict[str, Any]) -> dict[str, Any]:
    activation = objects["Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json"]
    topology = objects["Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"]
    reads = objects["Codex/results/PHASE_063_V1022_READ_ATTESTATION.json"]
    equations = objects["Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json"]
    literature = objects["Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json"]
    code = objects["Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json"]
    runtime = objects["Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json"]
    closure = objects["Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json"]
    disposition = objects["Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json"]
    carry = objects["Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json"]

    require(activation["gate"] == "PASS_P063_PLAN_ACTIVATION" and activation["validation_summary"] == {"all_passed": True, "passed": 150, "total": 150}, "E_ACTIVATION", repr(activation["validation_summary"]))
    source_expected = {"source_occurrences": 204, "unique_paths": 204, "unique_blobs": 204, "bytes": 4974148,
                       "text_physical_lines": 30219, "text_nonblank_lines": 26137, "pdf_pages": 133,
                       "history_commits": 100, "finding_routes": 96, "observation_inputs": 11}
    require({key: topology["counts"][key] for key in source_expected} == source_expected, "E_SOURCE_COUNTS", repr(topology["counts"]))
    require(topology["counts"]["partition_counts"] == {"COMPETING_REVIEW_CANDIDATE": 125, "FINAL_RELEASE_SURFACE": 63, "STATUS_MACHINE_PROCESS": 10, "VERSION_PLAN": 6}, "E_PARTITIONS", repr(topology["counts"]["partition_counts"]))
    require(topology["counts"]["review_modes"] == {"FULL_PDF": 4, "FULL_TEXT": 200}, "E_REVIEW_MODES", repr(topology["counts"]["review_modes"]))
    require(len(topology["sources"]) == 204 and len({row["source_id"] for row in topology["sources"]}) == 204, "E_SOURCE_IDENTITIES", "204")
    read_expected = {"manifest_records": 204, "text_records": 200, "text_physical_lines": 30219, "text_nonblank_lines": 26137,
                     "pdf_records": 4, "pdf_pages": 133, "pdf_page_attestations": 133, "supplemental_records": 1,
                     "observation_records": 11, "observation_physical_lines": 2363}
    require({key: reads["counts"][key] for key in read_expected} == read_expected, "E_READ_COUNTS", repr(reads["counts"]))
    require(len(reads["manifest_read_records"]) == 204 and len(reads["pdf_page_attestations"]) == 133, "E_READ_ROWS", "204/133")

    equation_expected = {"reachable_tex_sources": 53, "display_equations": 231, "labeled_display_equations": 200,
                         "manual_derivation_rows": 25, "manual_sign_rows": 6, "manual_operator_rows": 6,
                         "manual_material_rows": 6, "phase057_routes": 55, "findings": 20}
    require({key: equations["counts"][key] for key in equation_expected} == equation_expected, "E_EQUATION_COUNTS", repr(equations["counts"]))
    require(equations["finding_summary"] == {"P0": 4, "P1": 8, "P2": 8}, "E_EQUATION_FINDINGS", repr(equations["finding_summary"]))

    literature_expected = {"all_reviewed_text_sources": 201, "all_physical_lines": 30318, "bibliography_occurrences": 91,
                           "manual_unkeyed_bibliography_occurrences": 5, "citation_commands": 641,
                           "citation_key_occurrences": 770, "doi_occurrences": 328, "equation_candidates": 339,
                           "tex_delimited_math_candidates": 14958, "claim_candidate_lines": 8751,
                           "manual_literature_claims": 12, "manual_material_scope_rows": 12, "findings": 26}
    require({key: literature["counts"][key] for key in literature_expected} == literature_expected, "E_LITERATURE_COUNTS", repr(literature["counts"]))
    require(literature["finding_summary"] == {"P0": 6, "P1": 13, "P2": 7}, "E_LITERATURE_FINDINGS", repr(literature["finding_summary"]))

    code_expected = {"endpoint_occurrences": 16, "unique_blobs": 13, "ast_symbols": 227, "static_contracts": 7,
                     "theory_code_rows": 10, "findings": 13, "python_endpoints": 12, "guide_endpoints": 4}
    require({key: code["counts"][key] for key in code_expected} == code_expected, "E_CODE_COUNTS", repr(code["counts"]))
    require(code["finding_summary"] == {"P0": 3, "P1": 4, "P2": 6}, "E_CODE_FINDINGS", repr(code["finding_summary"]))
    require(runtime["counts"] == {"official_expectations_met": 12, "official_runs": 12, "probe_runtime_sets": 2, "runtimes": 2}, "E_RUNTIME_COUNTS", repr(runtime["counts"]))

    closure_expected = {"competing_occurrences": 125, "proposal_families": 22, "adoption_routes": 19,
                        "finding_adjudications": 96, "state_conflicts": 11, "build_drivers": 4}
    require({key: closure["counts"][key] for key in closure_expected} == closure_expected, "E_CLOSURE_COUNTS", repr(closure["counts"]))
    require(closure["counts"]["finding_states"] == {"HISTORICAL_ONLY": 30, "OPEN": 45, "RESOLVED_IN_V1022": 8, "SUPERSEDED": 2, "UNVERIFIED": 11}, "E_FINDING_STATES", repr(closure["counts"]["finding_states"]))
    build = closure["build_audit"]
    require(build["raw_blob_materialization_verified"] == "204/204" and build["runs_exit_zero"] == "12/12" and build["page_text_equal"] == "133/133" and build["render_exact"] == "125/133", "E_BUILD", repr({key: build[key] for key in ("raw_blob_materialization_verified", "runs_exit_zero", "page_text_equal", "render_exact")}))
    require([row["built_pages"] for row in build["rows"]] == [8, 83, 25, 17] and all(row["exit_codes"] == [0, 0, 0] for row in build["rows"]), "E_BUILD_ROWS", "4x3")
    require(closure["code_mention_boundary"]["physics_main_body_manual_refinement"]["actionable_line_rows"] == 58 and closure["code_mention_boundary"]["physics_main_body_manual_refinement"]["actionable_occurrences"] == 80, "E_CODE_MENTIONS", "58/80")
    require(all(value is False for value in closure["authority"].values()), "E_CLOSURE_AUTHORITY", repr(closure["authority"]))

    disposition_expected = {"source_dispositions": 204, "supplemental_process_dispositions": 1,
                            "open_source_dispositions": 38, "source_orphans": 0,
                            "duplicate_source_membership": 0, "external_authority_promotions": 0}
    require({key: disposition["counts"][key] for key in disposition_expected} == disposition_expected, "E_DISPOSITION_COUNTS", repr(disposition["counts"]))
    require(disposition["counts"]["source_disposition_distribution"] == {"CORRECT": 29, "PRESERVE": 160, "THEORY_ONLY": 6, "UNVERIFIED": 9}, "E_DISPOSITION_DISTRIBUTION", repr(disposition["counts"]["source_disposition_distribution"]))
    carry_expected = {"phase057_finding_routes": 96, "phase057_open_or_unverified": 56, "phase063_audit_finding_routes": 59,
                      "inherited_carry_items": 52, "inherited_phase060_blockers": 5, "inherited_phase061_blockers": 5,
                      "canonical_debt_routes": 91, "phase062_open_finding_routes": 59,
                      "canonical_owner_duplicate_check_records": 308, "audit_exact_prior_identity_matches": 0,
                      "new_phase063_blockers": 0, "ownerless_open_routes": 0, "multiply_owned_open_routes": 0,
                      "external_authority_promotions": 0, "source_disposition_links": 204, "status": "PASS_WITH_CONCERNS"}
    require(carry["gate_summary"] == carry_expected, "E_CARRY", repr(carry["gate_summary"]))

    return {
        "activation": {"checks": 150, "gate": "PASS_P063_PLAN_ACTIVATION"},
        "source_read": {"manifest": 204, "supplemental": 1, "partitions": [63, 6, 10, 125], "text": 200,
                        "physical_lines": 30219, "nonblank_lines": 26137, "pdfs": 4, "pages": 133,
                        "history_commits": 100, "observations": 11, "provisional_findings": 96},
        "equation_material": {"tex": 53, "equations": 231, "derivations": 25, "routes": 55,
                              "findings": {"P0": 4, "P1": 8, "P2": 8}},
        "literature_scope": {"sources": 201, "bibliography": 91, "manual_bibliography": 5, "citations": 770,
                             "dois": 328, "equations": 339, "tex_math": 14958, "claims": 8751,
                             "findings": {"P0": 6, "P1": 13, "P2": 7}, "authority_promotions": 0},
        "code_runtime": {"endpoints": 16, "blobs": 13, "symbols": 227, "contracts": 7, "concordance": 10,
                         "official_runs": 12, "runtime_sets": 2, "findings": {"P0": 3, "P1": 4, "P2": 6}},
        "adoption_build": {"occurrences": 125, "families": 22, "routes": 19, "findings": 96,
                           "states": [30, 45, 8, 2, 11], "build_runs": 12, "pages": [8, 83, 25, 17],
                           "page_text": 133, "render_exact": 125, "code_mentions": [58, 80], "state_conflicts": 11},
        "disposition_carry": {"source": 204, "supplemental": 1, "distribution": {"CORRECT": 29, "PRESERVE": 160, "THEORY_ONLY": 6, "UNVERIFIED": 9},
                              "phase057": 96, "phase057_active": 56, "audit_findings": 59, "owner_universe": 308,
                              "inherited": [52, 5, 5, 91, 59], "new_blockers": 0, "external_promotions": 0},
        "independent_numeric": independent_numeric_checks(),
        "authority": {"external_scientific": False, "external_material": False, "experimental": False,
                      "primary_literature": False, "canonical": False, "defect_repair": False,
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


def validate_output_control_content(content: dict[str, list[str]]) -> None:
    report = content[REPORT_PATH]
    gate = content[GATE_RESULT_PATH]
    phase = content[PHASE_RESULT_PATH]
    document_specs = (
        (REPORT_PATH, report, "REPORT", "# Phase 063 v1.0.22 Lineage Report F", "Gate: ", "상태: "),
        (GATE_RESULT_PATH, gate, "GATE_RESULT", "# Phase 063 Step 63.2 Integrated Gate Result", "Selected Gate: ", "Status: "),
        (PHASE_RESULT_PATH, phase, "PHASE_RESULT", "# Phase 063 Result — v1.0.22 Full Lineage Reaudit", "Exclusive Gate: ", "Status: "),
    )
    for path, lines, diagnostic, h1, gate_prefix, status_prefix in document_specs:
        require(lines and lines[0] == h1 and lines.count(h1) == 1, f"E_{diagnostic}_H1", path)
        exact_prefixed_field(lines, gate_prefix, f"`{GATE}`", f"E_{diagnostic}_GATE")
        exact_prefixed_field(lines, status_prefix, "`PASS_WITH_CONCERNS`", f"E_{diagnostic}_STATUS")
        exact_prefixed_field(lines, "Containing commit: ", "`PENDING_AT_PRECOMMIT_BY_DESIGN`", f"E_{diagnostic}_CONTAINING_COMMIT")
        exact_prefixed_field(lines, "Expected parent: ", f"`{PARENT_COMMIT}`", f"E_{diagnostic}_PARENT")
        exact_prefixed_field(lines, "Expected subject: ", f"`{SUBJECT}`", f"E_{diagnostic}_SUBJECT")
        exact_prefixed_field(lines, "Postcommit persistence terminal: ", f"`{PERSISTENCE}`", f"E_{diagnostic}_PERSISTENCE")
        require(not any(re.match(r"^(?:Selected Gate|Exclusive Gate|Gate|Status|상태):\s*`?(?:FAIL|CONDITIONAL)", line, re.IGNORECASE) for line in lines), f"E_{diagnostic}_CONTRADICTION", path)
        joined = "\n".join(lines)
        require("Phase 064" in joined and "Step 64" in joined, "E_RESULT_NEXT", path)

    parent = content[PARENT_LEDGER_PATH]
    active = content[ACTIVE_LEDGER_PATH]
    handover = content[HANDOVER_PATH]
    parent_row, parent_cells = exact_table_row(parent, "| 063 |", "E_PARENT_LEDGER_ROW")
    require(len(parent_cells) == 12 and parent_cells[0] == "063" and parent_cells[5] == "PASS_PENDING_PERSISTENCE", "E_PARENT_LEDGER_STATUS", parent_row)
    require(all(token in parent_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 064", "Step 64")), "E_PARENT_LEDGER_RECOVERY", parent_row)
    active_phase_row, active_phase_cells = exact_table_row(active, "| 063 |", "E_ACTIVE_LEDGER_ROW")
    require(len(active_phase_cells) == 10 and active_phase_cells[0] == "063" and active_phase_cells[4] == "PASS_PENDING_PERSISTENCE", "E_ACTIVE_LEDGER_STATUS", active_phase_row)
    require(all(token in active_phase_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 064", "Step 64")), "E_ACTIVE_LEDGER_RECOVERY", active_phase_row)
    active_step_row, active_step_cells = exact_table_row(active, "| Step 63.2 |", "E_ACTIVE_STEP_ROW")
    require(len(active_step_cells) == 6 and active_step_cells[0] == "Step 63.2" and active_step_cells[2] == "`PENDING_AT_PRECOMMIT_BY_DESIGN`", "E_ACTIVE_STEP_STATUS", active_step_row)
    require(all(token in active_step_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 064", "Step 64")), "E_ACTIVE_STEP_RECOVERY", active_step_row)
    handover_step_row, handover_step_cells = exact_table_row(handover, "| Phase 063 Step 63.2 |", "E_HANDOVER_STEP_ROW")
    require(len(handover_step_cells) == 4 and handover_step_cells[:2] == ["Phase 063 Step 63.2", "Step 63.2"], "E_HANDOVER_STEP_STATUS", handover_step_row)
    require(all(token in handover_step_row for token in (PARENT_COMMIT, GATE, PERSISTENCE, SUBJECT, "Phase 064", "Step 64")), "E_HANDOVER_STEP_RECOVERY", handover_step_row)
    expected_current = "15. 현재 Phase 상태: Phase 063 `PASS_PENDING_PERSISTENCE`, Current checkpoint: Step 63.2 precommit `PASS_P063_LINEAGE_F`"
    require([line for line in handover if line.startswith("15. 현재 Phase 상태:")] == [expected_current], "E_HANDOVER_CURRENT_STATUS")


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
        "schema_version": "P063-STEP63.2-1", "phase": "063", "step": "63.2", "generated_date": "2026-08-29",
        "gate": GATE, "status": "PASS_WITH_CONCERNS", "expected_parent": PARENT_COMMIT, "expected_subject": SUBJECT,
        "authority_boundary": AUTHORITY_BOUNDARY, "authority": copy.deepcopy(integrated["authority"]),
        "validator_identity": {"path": VALIDATOR_PATH, "sha256_lf": sha256(validator_raw), "bytes_lf": len(validator_raw),
                               "source_policy": "NO_PRODUCTION_IMPORT_OR_EXECUTION"},
        "exact_eight": {"count": 8, "paths": FINAL_PATHS, "result_first": True, "json_last": True},
        "repository": stable_repository_projection(repository_snapshot(allow_final_dirt=True)),
        "input_inventory": inputs, "step_commit_inventory": step_commit_inventory(),
        "historical_execution": {"precommit": precommit, "persistence": persistence, "unit_count": 7,
                                 "invocation_count": 15, "pass_count": 15},
        "integrated_contracts": integrated, "output_contract": outputs,
        "negative_control_contract": {"named_count": 28, "strict_json_count": 6, "git_boundary_count": 15,
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
        ("E_FINAL_IDENTITY", (document["phase"], document["step"], document["generated_date"]), ("063", "63.2", "2026-08-29")),
        ("E_FINAL_GATE", (document["gate"], document["status"]), (GATE, "PASS_WITH_CONCERNS")),
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
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["source_read"].__setitem__("manifest", 203))
    add("E_FINAL_OUTPUTS", lambda d: d["output_contract"].__setitem__("result_first", False))
    add("E_FINAL_NEGATIVE_CONTRACT", lambda d: d["negative_control_contract"].__setitem__("singleton_required", False))
    add("E_FINAL_DETERMINISM", lambda d: d["determinism"].__setitem__("byte_identical", False))
    add("E_FINAL_AUTHORITY_BOUNDARY", lambda d: d.__setitem__("authority_boundary", "overclaim"))
    add("E_FINAL_SEMANTIC_HASH", lambda d: d.__setitem__("semantic_sha256", "0" * 64), False)
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["equation_material"].__setitem__("equations", 230))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["literature_scope"].__setitem__("authority_promotions", 1))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["code_runtime"].__setitem__("official_runs", 11))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["adoption_build"].__setitem__("render_exact", 124))
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
        ("E_GATE_RESULT_STATUS", lambda c: replace_exact(c[GATE_RESULT_PATH], "Status: `PASS_WITH_CONCERNS`", "Status: `FAIL`")),
        ("E_GATE_RESULT_PARENT", lambda c: (
            replace_exact(c[GATE_RESULT_PATH], f"Expected parent: `{PARENT_COMMIT}`", f"Expected parent: `{'0' * 40}`"),
            c[GATE_RESULT_PATH].append(f"Unbound parent witness: `{PARENT_COMMIT}`"),
        )),
        ("E_PHASE_RESULT_STATUS", lambda c: replace_exact(c[PHASE_RESULT_PATH], "Status: `PASS_WITH_CONCERNS`", "Status: `CONDITIONAL`")),
        ("E_ACTIVE_STEP_RECOVERY", lambda c: replace_exact(
            c[ACTIVE_LEDGER_PATH],
            next(line for line in c[ACTIVE_LEDGER_PATH] if line.startswith("| Step 63.2 |")),
            next(line for line in c[ACTIVE_LEDGER_PATH] if line.startswith("| Step 63.2 |")).replace(PARENT_COMMIT, "0" * 40),
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
    return passed, len(cases) + len(document_cases)


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
    staged = nul_paths(git(["diff", "--cached", "--name-only", "-z"], cwd=work).stdout)
    unstaged = nul_paths(git(["diff", "--name-only", "-z"], cwd=work).stdout)
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
    prefix = "phase063-step632-git-boundary-"
    root = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    work = root / "work"
    origin = root / "origin.git"
    expected_paths = set(FINAL_PATHS)
    try:
        work.mkdir()
        git(["init", "--initial-branch=main"], cwd=work)
        git(["config", "core.autocrlf", "false"], cwd=work)
        git(["config", "user.email", "phase063-fixture@example.invalid"], cwd=work)
        git(["config", "user.name", "Phase 063 Fixture"], cwd=work)
        (work / "base.txt").write_bytes(b"base\n")
        (work / "Claude").mkdir()
        (work / "Claude" / "keep.txt").write_bytes(b"protected\n")
        git(["add", "base.txt", "Claude/keep.txt"], cwd=work)
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
        ("extra_untracked", {"E_GIT_UNTRACKED"}, lambda work, origin, base, drift, paths: (work / "extra.txt").write_bytes(b"extra\n")),
        ("index_worktree", {"E_GIT_UNSTAGED", "E_GIT_INDEX_WORKTREE"}, lambda work, origin, base, drift, paths: (work / sorted(paths)[0]).write_bytes(b"mutated\n")),
        ("cached_whitespace", {"E_GIT_DIFF_CHECK"}, lambda work, origin, base, drift, paths: ((work / sorted(paths)[0]).write_bytes(b"trailing-space \n"), git(["add", "--", sorted(paths)[0]], cwd=work))),
    ]
    passed = 0
    for name, wanted, mutation in cases:
        root, work, origin, base, drift, expected_paths = make_git_boundary_fixture()
        prefix = "phase063-step632-git-boundary-"
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
    staged = nul_paths(git(["diff", "--cached", "--name-only", "-z"]).stdout)
    unstaged = nul_paths(git(["diff", "--name-only", "-z"]).stdout)
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
    changed = nul_paths(git(["diff-tree", "--no-commit-id", "--name-only", "-r", "-z", expected_commit]).stdout)
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
    temp_path = ARTIFACT.with_name(ARTIFACT.name + ".tmp-step632")
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
        print(f"PASS_P063_STEP63_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print("PASS_P063_STEP63_2_DETERMINISM 2/2")
        print("PASS_P063_LINEAGE_F collect=JSON_LAST result_first=true historical=15/15")
        return 0
    require(not document_diagnostics(stored, expected), "E_STORED_DOCUMENT", repr(sorted(document_diagnostics(stored, expected))))
    require(stored_raw == expected_raw, "E_STORED_BYTE_IDENTITY", ARTIFACT_PATH)
    automatic_full = mode in {"precommit", "persistence"}
    if run_negative or automatic_full:
        negative_passed, negative_total = run_negative_controls(stored)
        git_passed, git_total = run_git_boundary_controls()
        print(f"PASS_P063_STEP63_2_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
    if run_determinism or automatic_full:
        print("PASS_P063_STEP63_2_DETERMINISM 2/2")
    if mode == "precommit":
        validate_staged()
        print("PASS_P063_STEP63_2_STAGED exact-eight=8/8 historical=15/15")
    elif mode == "persistence":
        require(expected_commit is not None, "E_EXPECTED_COMMIT", "required")
        validate_persistence(expected_commit)
        print(f"{PERSISTENCE} commit={expected_commit}")
    else:
        print("PASS_P063_LINEAGE_F artifact=true historical=15/15")
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
        print(f"FAIL_P063_LINEAGE_F: {error}")
        raise SystemExit(1)
