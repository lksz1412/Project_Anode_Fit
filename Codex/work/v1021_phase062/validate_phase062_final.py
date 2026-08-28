#!/usr/bin/env python3
"""Phase 062 Step 57.2 integrated, fail-closed lineage validator.

The validator is also the sole collector for PHASE_062_VALIDATION.json.  It
never imports Phase builders, validators, or frozen production modules.
Historical validators execute only as subprocesses in disposable repositories
that reproduce their exact staged pre-commit state.
"""

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
import time
from collections import Counter
from typing import Any, Callable


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[3]
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PARENT_COMMIT = "247e9b0b28d185604753f40ee0244cfe0bf068cf"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
SUBJECT = "audit(phase062): close v1021 lineage gate"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

VALIDATOR_PATH = "Codex/work/v1021_phase062/validate_phase062_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_062_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_062_V1021_LINEAGE_REPORT_E.md"
GATE_RESULT_PATH = "Codex/results/PHASE_062_STEP_057_2_GATE_RESULT.md"
PHASE_RESULT_PATH = "Codex/results/PHASE_062_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
ARTIFACT = ROOT / ARTIFACT_PATH
VALIDATOR = ROOT / VALIDATOR_PATH

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

AUTHORITY_BOUNDARY = (
    "PASS_P062_LINEAGE_E establishes frozen v1.0.21 internal lineage-audit, "
    "derivation, scope, code/runtime, adoption/build, disposition and lossless "
    "routing coverage only. It does not establish external scientific, material, "
    "experimental or primary-literature truth, canonical model selection, defect "
    "repair, final LaTeX/PDF, parameter identifiability or publication readiness."
)


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}{': ' + detail if detail else ''}")
        self.code = code
        self.detail = detail


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, "E_DUPLICATE_JSON", key)
        output[key] = value
    return output


def reject_constant(value: str) -> None:
    raise ValidationError("E_NONFINITE_JSON", value)


def finite_float(value: str) -> float:
    parsed = float(value)
    require(math.isfinite(parsed), "E_NONFINITE_JSON", value)
    return parsed


def full_traversal(value: Any) -> dict[str, int]:
    values = 0
    keys = 0
    depth = 0

    def walk(node: Any, level: int) -> None:
        nonlocal values, keys, depth
        values += 1
        depth = max(depth, level)
        if isinstance(node, float):
            require(math.isfinite(node), "E_NONFINITE_JSON", repr(node))
        if isinstance(node, dict):
            keys += len(node)
            for child in node.values():
                walk(child, level + 1)
        elif isinstance(node, list):
            for child in node:
                walk(child, level + 1)

    walk(value, 0)
    return {"value_nodes": values, "key_nodes": keys, "total_nodes": values + keys, "max_depth": depth}


def strict_load_bytes(raw: bytes, label: str) -> tuple[Any, dict[str, int]]:
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except ValidationError:
        raise
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ValidationError("E_STRICT_JSON", f"{label}: {error}") from error
    return value, full_traversal(value)


def semantic_hash(document: dict[str, Any]) -> str:
    clone = copy.deepcopy(document)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def run_process(
    argv: list[str],
    *,
    cwd: pathlib.Path = ROOT,
    timeout: int = 120,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired as error:
        raise ValidationError("E_SUBPROCESS_TIMEOUT", repr(argv)) from error


def git(
    args: list[str],
    *,
    cwd: pathlib.Path = ROOT,
    timeout: int = 120,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    process = run_process(["git", *args], cwd=cwd, timeout=timeout, env=env)
    if check and process.returncode:
        raise ValidationError(
            "E_GIT_COMMAND",
            f"{args}: {process.stderr.decode('utf-8', errors='replace').strip()}",
        )
    return process


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT) -> str:
    return git(args, cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str, *, cwd: pathlib.Path = ROOT) -> bytes:
    require("\\" not in path and not path.startswith("/"), "E_GIT_PATH", path)
    return git(["show", f"{commit}:{path}"], cwd=cwd).stdout


def nul_paths(raw: bytes) -> set[str]:
    return {item.decode("utf-8").replace("\\", "/") for item in raw.split(b"\0") if item}


def status_paths(cwd: pathlib.Path = ROOT) -> set[str]:
    records = [row for row in git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=cwd).stdout.split(b"\0") if row]
    output: set[str] = set()
    index = 0
    while index < len(records):
        row = records[index]
        require(len(row) >= 4, "E_STATUS_PARSE", repr(row))
        xy = row[:2].decode("ascii")
        output.add(row[3:].decode("utf-8").replace("\\", "/"))
        index += 1
        if "R" in xy or "C" in xy:
            require(index < len(records), "E_STATUS_PARSE", "rename/copy")
            output.add(records[index].decode("utf-8").replace("\\", "/"))
            index += 1
    return output


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT) -> str:
    rows = git_text(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"], cwd=cwd).splitlines()
    require(len(rows) == 1, "E_REMOTE_CARDINALITY", branch)
    return rows[0].split()[0]


ACTIVATION_COMMIT = "76dccbaee0efdd16a4d22c25527a1a8ab3108559"
STEP52_COMMIT = "51ccba6c248a3e710e1a4ddd6017c18043f8a7a2"
STEP53_COMMIT = "9dee2f4d6bdde48f248227cdede08d0d307cc8bc"
STEP54_COMMIT = "ce069dde91f1332cc2852312cd2cbccd7cdf38db"
STEP55_COMMIT = "c700d4ff887af6bb66f2c0118f75832202856bf8"
STEP56_COMMIT = "1c8541fdea2cd69aa09e6b99d2f371c41a0bb727"
STEP57_COMMIT = PARENT_COMMIT

UNIT_SPECS: list[dict[str, Any]] = [
    {
        "unit": "ACTIVATION",
        "commit": ACTIVATION_COMMIT,
        "parent": "86b4acbf9ed41ae12bd5ae95c4d2a5c2adb0dfe2",
        "subject": "docs(phase062): plan v1021 lineage reaudit",
        "validator": "Codex/work/v1021_phase062/validate_phase062_plan.py",
        "validator_sha256": "59c309ab3859ad49dae6f389eb17c978f3e42e6f8041e86955f0517f3a018dfa",
        "paths": [
            "Codex/plans/2026-08-27-phase062-v1021-lineage-detailed-plan.md",
            "Codex/work/v1021_phase062/validate_phase062_plan.py",
            "Codex/results/PHASE_062_PLAN_ACTIVATION_VALIDATION.json",
            "Codex/results/PHASE_062_PLAN_ACTIVATION_RESULT.md",
            PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH,
        ],
        "invocations": [
            {
                "args": ["--verify-staged"],
                "terminal_prefix": "PASS_P062_PLAN_ACTIVATION_STAGED 7/7",
                "required_prefixes": ["PASS_P062_PLAN_ACTIVATION 115/115"],
            },
            {
                "args": ["--content-only", "--run-negative-probes", "--determinism-check"],
                "terminal_prefix": "PASS_P062_PLAN_CONTENT",
                "required_prefixes": [
                    "PASS_P062_PLAN_NEGATIVE_CONTROLS",
                    "PASS_P062_PLAN_DETERMINISM 2/2",
                ],
            },
        ],
    },
    {
        "unit": "STEP52", "commit": STEP52_COMMIT, "parent": ACTIVATION_COMMIT,
        "subject": "audit(phase062): freeze v1021 source process topology",
        "validator": "Codex/work/v1021_phase062/validate_phase062_step52.py",
        "validator_sha256": "0b47e0664d0af66391d2adde18ac1f9ec02ee9263b679bc6cee7dc1d66bfad54",
        "paths": [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_062_STEP_052_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
            "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json",
            "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json",
            "Codex/work/v1021_phase062/build_phase062_step52_source_process_topology.py",
            "Codex/work/v1021_phase062/validate_phase062_step52.py"],
        "args": ["--verify-staged", "--run-negative-probes", "--determinism-check"],
        "terminal_prefix": "PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY",
        "required_prefixes": ["PASS_P062_STEP52_NEGATIVE_CONTROLS 50/50", "PASS_P062_STEP52_MARKDOWN_NEGATIVE_CONTROLS 11/11", "PASS_P062_STEP52_DETERMINISM 2/2"],
    },
    {
        "unit": "STEP53", "commit": STEP53_COMMIT, "parent": STEP52_COMMIT,
        "subject": "audit(phase062): rederive v1021 statmech tst",
        "validator": "Codex/work/v1021_phase062/validate_phase062_step53.py",
        "validator_sha256": "1cde46743478ea6c584f728862a3a4a8a931b52f6c0a60311b3b3d91351b6fef",
        "paths": [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md",
            "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json",
            "Codex/work/v1021_phase062/build_phase062_step53_statmech_tst.py",
            "Codex/work/v1021_phase062/validate_phase062_step53.py"],
        "args": ["--verify-staged", "--run-negative-probes", "--determinism-check"],
        "terminal_prefix": "PASS_P062_STEP53_STATMECH_TST_REDERIVATION",
        "required_prefixes": ["PASS_P062_STEP53_NEGATIVE_CONTROLS 36/36", "PASS_P062_STEP53_MARKDOWN_NEGATIVE_CONTROLS 9/9", "PASS_P062_STEP53_BUILDER_POLICY_NEGATIVE_CONTROLS 11/11", "PASS_P062_STEP53_DETERMINISM 2/2", "PASS_P062_STEP53_SYMBOLIC_CHECKS 15/15", "PASS_P062_STEP53_NUMERIC_CHECKS 20/20"],
    },
    {
        "unit": "STEP54", "commit": STEP54_COMMIT, "parent": STEP53_COMMIT,
        "subject": "audit(phase062): bound v1021 lco si scope",
        "validator": "Codex/work/v1021_phase062/validate_phase062_step54.py",
        "validator_sha256": "737b0fdcada7bc52733d771d855063400b1f8b631cc723a344eb98edf08025b0",
        "paths": [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md",
            "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json",
            "Codex/work/v1021_phase062/build_phase062_step54_lco_si_scope.py",
            "Codex/work/v1021_phase062/validate_phase062_step54.py"],
        "args": ["--mode", "precommit", "--staged"],
        "terminal_prefix": "PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS",
        "required_prefixes": ["PASS_P062_STEP54_NEGATIVE_CONTROLS 28/28", "PASS_P062_STEP54_BOUNDARY_CONTROLS 2/2", "PASS_P062_STEP54_DETERMINISM 2/2"],
    },
    {
        "unit": "STEP55", "commit": STEP55_COMMIT, "parent": STEP54_COMMIT,
        "subject": "audit(phase062): compare v1021 code runtime",
        "validator": "Codex/work/v1021_phase062/validate_phase062_step55.py",
        "validator_sha256": "71e78cf8b3cd05b58581dab55979c4d541d2324daa7bb5870a64975194463836",
        "paths": [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md",
            "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json",
            "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json",
            "Codex/work/v1021_phase062/build_phase062_step55_code_runtime_delta.py",
            "Codex/work/v1021_phase062/validate_phase062_step55.py"],
        "args": ["--verify-staged", "--run-negative-probes", "--determinism-check"],
        "terminal_prefix": "PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS",
        "required_prefixes": ["PASS schema queue=11/11", "PASS_P062_STEP55_NEGATIVE_CONTROLS 78/78", "PASS_P062_STEP55_DETERMINISM 2/2"],
    },
    {
        "unit": "STEP56", "commit": STEP56_COMMIT, "parent": STEP55_COMMIT,
        "subject": "audit(phase062): adjudicate v1021 physics closure",
        "validator": "Codex/work/v1021_phase062/validate_phase062_step56.py",
        "validator_sha256": "e627ac27e2738627ac7f09f61d8507436af9c64c263441ff3695f524de197344",
        "paths": [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_062_STEP_056_PHYSICS_CLOSURE_RESULT.md",
            "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json",
            "Codex/work/v1021_phase062/build_phase062_step56_physics_closure.py",
            "Codex/work/v1021_phase062/validate_phase062_step56.py"],
        "args": ["--verify-staged", "--run-negative-probes", "--determinism-check"],
        "terminal_prefix": "PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS",
        "required_prefixes": ["PASS_P062_STEP56_ALL_CONTROLS named=74 attack_fixtures=112", "PASS_P062_STEP56_DETERMINISM 2/2", "PASS_P062_STEP56_CLEAN_BUILD"],
    },
    {
        "unit": "STEP57_1", "commit": STEP57_COMMIT, "parent": STEP56_COMMIT,
        "subject": "audit(phase062): disposition v1021 lineage",
        "validator": "Codex/work/v1021_phase062/validate_phase062_step57_dispositions.py",
        "validator_sha256": "992a94ce960468b7168a4716ec92920f19fd0c8e8b0bff7b0e8bb90fcf4e81bb",
        "paths": [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_062_STEP_057_1_DISPOSITION_RESULT.md",
            "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json",
            "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json",
            "Codex/work/v1021_phase062/build_phase062_step57_dispositions.py",
            "Codex/work/v1021_phase062/validate_phase062_step57_dispositions.py"],
        "args": ["--mode", "precommit"],
        "terminal_prefix": "PASS_P062_STEP57_1_DISPOSITIONS",
        "required_prefixes": ["PASS negative_controls=73/73", "PASS determinism=2/2", "PASS release=68 supplemental=1"],
    },
]

ARTIFACT_SPECS: dict[str, dict[str, str]] = {
    "Codex/results/PHASE_062_PLAN_ACTIVATION_VALIDATION.json": {"commit": ACTIVATION_COMMIT, "sha256": "5f893a4d0abbfd55f056f5a62d6a4439edf51e5a3d0edbbac2e8c594a756ea24"},
    "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json": {"commit": STEP52_COMMIT, "sha256": "cb8eda3efa2b50da49ddc6d4e67d0c9679bce7540a622b584828e44e042bc283"},
    "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json": {"commit": STEP52_COMMIT, "sha256": "0f646e7089016d81e1e1bb73391478454f31fde4fa8560285e239d7634e279ea"},
    "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json": {"commit": STEP53_COMMIT, "sha256": "934be5273a91578b712d3ab44ef96eebb4cf7645973ec101b4e233b49426de16"},
    "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json": {"commit": STEP54_COMMIT, "sha256": "9af82c1997f0b31282b353ae1006324e8a9913fc7e5c579709a4c9b1bb32901d"},
    "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json": {"commit": STEP55_COMMIT, "sha256": "ba0e6f7eee956294f0b38c2497c9f90b3976321718d262406e57d77853c058d4"},
    "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json": {"commit": STEP55_COMMIT, "sha256": "7c6d8486ddf66749527cb4171932bbe737405e1d640657884859b1330e6edf77"},
    "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json": {"commit": STEP56_COMMIT, "sha256": "1c24478c01692dca82465db273f3b432dac7b65739475f015999922137e1e27d"},
    "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json": {"commit": STEP57_COMMIT, "sha256": "2a75fe6ef35ee71a0de8c576ef81fa27eadffc0101a90ad6c491c1b8f410f62c"},
    "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json": {"commit": STEP57_COMMIT, "sha256": "9df1a9203d8b9df60232073130e5abec857cfc7a7973bf591bb7d7488e4f2614"},
}

RESULT_SPECS: dict[str, dict[str, str]] = {
    "Codex/results/PHASE_062_PLAN_ACTIVATION_RESULT.md": {"commit": ACTIVATION_COMMIT, "sha256": "98b030c2a99ac53b4b9fd3ea2f0ae403560ab45aaf3b8327e6f62ce64c571aa8"},
    "Codex/results/PHASE_062_STEP_052_SOURCE_PROCESS_TOPOLOGY_RESULT.md": {"commit": STEP52_COMMIT, "sha256": "157a07464d6157194083e331ab55c1423a32cc3504d9e0b0dd46a52e0955fbd4"},
    "Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md": {"commit": STEP53_COMMIT, "sha256": "9e96ee4729d888af8c96369fbc5006e3dc4dd7dd0f7ce7cae3904895ce0a85e1"},
    "Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md": {"commit": STEP54_COMMIT, "sha256": "a4a8e0c44254d08fe8891b2eadf7c20e6b7c884fa6aa476871323504b7f50ffa"},
    "Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md": {"commit": STEP55_COMMIT, "sha256": "8edd00e1118a2150f415baecd95f9e6400897c298825a3ae75c48bb4ecf9a330"},
    "Codex/results/PHASE_062_STEP_056_PHYSICS_CLOSURE_RESULT.md": {"commit": STEP56_COMMIT, "sha256": "8ca0c7a26f61ba9dcfd223357db32f5d3d980908bd8b3a2e17e7632bbd5a1179"},
    "Codex/results/PHASE_062_STEP_057_1_DISPOSITION_RESULT.md": {"commit": STEP57_COMMIT, "sha256": "a8530fc519bccfbba25980f2e4d091031ebfa430e4adcfd42a434537639763e7"},
}

EXPECTED_TOP_KEYS: dict[str, set[str]] = {
    "Codex/results/PHASE_062_PLAN_ACTIVATION_VALIDATION.json": {"artifact_hashes_nonself","checks","content_projection_sha256","control_contract","determinism","deterministic_projection_sha256","exact_allowlist","expected_parent","expected_subject","gate","generated_date","manifest_contract","negative_controls","phase","plan_contract","repository_state","routing_contract","schema_version","semantic_sha256","summary","supplemental_contract","unit"},
    "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json": {"activation_commit","artifact_kind","authority_boundary","baseline_commit","builder","counts","denominator_policy","duplicates","extension_counts","generated_date","ground_not_found","history","manifest","path_blob_set_sha256","path_set_sha256","pdf_source_relationships","phase","phase057_navigation_inputs","phase057_observation_id_sha256","phase057_observations","process_aliases","process_artifacts","q1_comparison_report","review_mode_counts","role_counts","same_relative_v1020_v1021","schema_version","sources","status","step","supplemental_process_control"},
    "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json": {"artifact_kind","authority_boundary","baseline_commit","counts","generated_date","human_review_contract_sha256","partitions","pdf_records","pdf_variant_relationships","phase","q1_comparison_text_record","release_text_records","schema_version","snapshot_records","source_topology_semantic_sha256","status","step","supplemental_text_record"},
    "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json": {"artifact_kind","authority_boundary","claim_rows","equation_inventory","findings","gate","generated_date","git","grand_canonical_derivation","negative_control_contract","patches","phase","schema_version","snapshot_evidence","source_attestations","source_spans","status","step","summary","tst_rederivation"},
    "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json": {"adopted_release_text_inventory","artifact_id","authority_contract","bibliography_audit","builder_sha256","citation_denominators","citation_occurrences","finding_summary","findings","gate","ground_not_found_records","material_claim_contract","negative_control_contract","provenance","q6_lco_audit","q7_si_audit","reference_ledger_self_report_inventory","result_first_contract","routing_summary","schema_version","scope_matrix","semantic_sha256","source_attestations","source_claim_coverage","source_claim_manifest","source_line_inventory","status"},
    "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json": {"adjacent_comparison_count","adjacent_comparisons","authority","builder_lf_sha256","claim_consumer_count","claim_consumers","code_matched_claim_count","code_matched_claims","comparison_endpoint_count","comparison_endpoints","counterpart_count","counterpart_matrix","endpoint_disposition_count","endpoint_dispositions","finding_counts","findings","frozen_baseline","gate","input_commit","patches","production_normalized_ast_identical","queue","queue_count","required_negative_control_count","required_negative_controls","result_first","schema","static_python","static_python_count"},
    "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json": {"authority","cleanup","environment_dependent_fields_excluded","facts","frozen_baseline","independent_probe","input_commit","official_runs","runtime_scope","schema"},
    "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json": {"acceptance","authority","build_audit","code_mentions","content_denominator","controlled_assets","delta_classification","evidence_links","findings","frozen_baseline","gate","input_commit","layout_findings","page_genealogy","physics_closure","release","required_attack_fixture_count","required_document_control_count","required_document_controls","required_git_control_count","required_git_controls","required_negative_control_count","required_negative_controls","required_source_control_count","required_source_controls","required_total_control_count","result_first","review_vote_authority","schema","source_contract","structural_schema_contract","terminal"},
    "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json": {"artifact_kind","authority_boundary","baseline_commit","gate_summary","generation","input_commit","inputs","phase","release_dispositions","release_source_contract","schema_version","source_commit","step","supplemental_process_disposition"},
    "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json": {"artifact_kind","authority_boundary","baseline_commit","canonical_debt_routing","gate_summary","generation","inherited_carry_items","inherited_phase060_blockers","inherited_phase061_blockers","input_commit","inputs","new_phase062_blockers","open_finding_ownership","phase","phase061_target62_contract","phase061_target62_routes","schema_version","source_commit","step"},
}


def validate_source_policy() -> None:
    raw = lf_bytes(VALIDATOR.read_bytes())
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=VALIDATOR_PATH)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name for alias in node.names]
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            require(not any(name == "Claude" or name.startswith("Claude.") or name in {"importlib", "runpy"} for name in names), "E_VALIDATOR_SOURCE_POLICY", repr(names))
        if isinstance(node, ast.Call):
            require(not (isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "__import__"}), "E_VALIDATOR_SOURCE_POLICY", ast.dump(node.func, include_attributes=False))
            for keyword in node.keywords:
                require(not (keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True), "E_VALIDATOR_SOURCE_POLICY", "shell=True")


def load_pinned_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    objects: dict[str, Any] = {}
    records: list[dict[str, Any]] = []
    for path, spec in ARTIFACT_SPECS.items():
        raw = git_blob(spec["commit"], path)
        require(sha256(raw) == spec["sha256"], "E_INPUT_SHA", path)
        require((ROOT / path).read_bytes() == raw, "E_INPUT_WORKTREE", path)
        value, traversal = strict_load_bytes(raw, path)
        require(type(value) is dict, "E_INPUT_TOP_TYPE", path)
        require(set(value) == EXPECTED_TOP_KEYS[path], "E_INPUT_TOP_SCHEMA", path)
        objects[path] = value
        records.append({"path":path,"commit":spec["commit"],"sha256":spec["sha256"],"bytes":len(raw),"physical_lines":len(raw.decode("utf-8").splitlines()),**traversal})
    result_records: list[dict[str, Any]] = []
    for path, spec in RESULT_SPECS.items():
        raw = git_blob(spec["commit"], path)
        require(sha256(raw) == spec["sha256"], "E_RESULT_SHA", path)
        require((ROOT / path).read_bytes() == raw, "E_RESULT_WORKTREE", path)
        text = raw.decode("utf-8")
        result_records.append({"path":path,"commit":spec["commit"],"sha256":spec["sha256"],"bytes":len(raw),"physical_lines":len(text.splitlines())})
    return objects, {"machine_count":10,"machine_records":records,"result_count":7,"result_records":result_records,"strict_duplicate_keys":True,"nonfinite_rejected":True,"full_recursive_traversal":True}


def step_commit_inventory() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        commit = spec["commit"]
        require(git_text(["rev-parse", f"{commit}^"]) == spec["parent"], "E_UNIT_PARENT", spec["unit"])
        require(git_text(["show", "-s", "--format=%s", commit]) == spec["subject"], "E_UNIT_SUBJECT", spec["unit"])
        changed = nul_paths(git(["diff-tree","--no-commit-id","--name-only","-r","-z",commit]).stdout)
        require(changed == set(spec["paths"]) and len(changed) == len(spec["paths"]), "E_UNIT_PATH_SET", spec["unit"])
        require(git(["merge-base","--is-ancestor",commit,PARENT_COMMIT],check=False).returncode == 0, "E_UNIT_ANCESTRY", spec["unit"])
        require(git(["merge-base","--is-ancestor",commit,f"origin/{ACTIVE_BRANCH}"],check=False).returncode == 0, "E_UNIT_REMOTE_ANCESTRY", spec["unit"])
        validator_raw = git_blob(commit, spec["validator"])
        require(sha256(validator_raw) == spec["validator_sha256"], "E_UNIT_VALIDATOR_SHA", spec["unit"])
        records.append({"unit":spec["unit"],"commit":commit,"parent":spec["parent"],"subject":spec["subject"],"path_count":len(spec["paths"]),"paths":sorted(spec["paths"]),"validator_path":spec["validator"],"validator_sha256":spec["validator_sha256"],"in_active_ancestry":True,"in_origin_active_ancestry":True})
    return records


def remove_temp_tree(path: pathlib.Path, prefix: str) -> None:
    resolved = path.resolve()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    require(resolved.parent == temp_root, "E_TEMP_BOUNDARY", str(resolved))
    require(resolved.name.startswith(prefix), "E_TEMP_PREFIX", resolved.name)

    def clear_readonly(function: Callable[[str], Any], target: str, error: BaseException) -> None:
        if not isinstance(error, PermissionError):
            raise error
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(resolved, onexc=clear_readonly)
    require(not resolved.exists(), "E_TEMP_CLEANUP", str(resolved))


def subordinate_python() -> str:
    process = run_process(["py", "-3.12", "-c", "import PIL,pypdf,sys;print(sys.executable)"], timeout=45)
    require(process.returncode == 0 and process.stderr == b"", "E_SUBORDINATE_RUNTIME", process.stderr.decode("utf-8", errors="replace"))
    executable = process.stdout.decode("utf-8").strip()
    require(pathlib.Path(executable).is_file(), "E_SUBORDINATE_RUNTIME", executable)
    return executable


def make_historical_clone(spec: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path]:
    prefix = f"phase062-step572-{spec['unit'].lower()}-"
    parent = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    clone = parent / "repo"
    process = run_process(["git","clone","--shared","--no-checkout",str(ROOT),str(clone)], timeout=180)
    require(process.returncode == 0, "E_FIXTURE_CLONE", process.stderr.decode("utf-8", errors="replace"))
    try:
        git(["config","core.autocrlf","false"],cwd=clone)
        git(["config","core.eol","lf"],cwd=clone)
        git(["checkout","-B",ACTIVE_BRANCH,spec["parent"]],cwd=clone)
        git(["update-ref",f"refs/remotes/origin/{ACTIVE_BRANCH}",spec["parent"]],cwd=clone)
        git(["update-ref",f"refs/remotes/origin/{PROTECTED_BRANCH}",PROTECTED_TIP],cwd=clone)
        git(["update-ref","refs/remotes/origin/main",MAIN_TIP],cwd=clone)
        git(["update-ref",f"refs/heads/{PROTECTED_BRANCH}",PROTECTED_TIP],cwd=clone)
        git(["update-ref","refs/heads/main",MAIN_TIP],cwd=clone)
        git(["remote","set-url","origin","."],cwd=clone)
        git(["branch","--set-upstream-to",f"origin/{ACTIVE_BRANCH}",ACTIVE_BRANCH],cwd=clone)
        git(["checkout",spec["commit"],"--",*spec["paths"]],cwd=clone,timeout=300)
        staged = nul_paths(git(["diff","--cached","--name-only","-z"],cwd=clone).stdout)
        unstaged = nul_paths(git(["diff","--name-only","-z"],cwd=clone).stdout)
        untracked = nul_paths(git(["ls-files","--others","--exclude-standard","-z"],cwd=clone).stdout)
        require(staged == set(spec["paths"]), "E_SUBORDINATE_STAGED_SET", spec["unit"])
        require(not unstaged and not untracked, "E_SUBORDINATE_DIRT", spec["unit"])
        require(git_text(["branch","--show-current"],cwd=clone) == ACTIVE_BRANCH, "E_SUBORDINATE_BRANCH", spec["unit"])
        require(git_text(["rev-parse","HEAD"],cwd=clone) == spec["parent"], "E_SUBORDINATE_PARENT", spec["unit"])
        require(git_text(["rev-parse","@{upstream}"],cwd=clone) == spec["parent"], "E_SUBORDINATE_UPSTREAM", spec["unit"])
        require(live_tip(ACTIVE_BRANCH,cwd=clone) == spec["parent"], "E_SUBORDINATE_LIVE", spec["unit"])
    except Exception:
        remove_temp_tree(parent, prefix)
        raise
    return parent, clone


def run_historical_invocation(
    clone: pathlib.Path,
    spec: dict[str, Any],
    invocation: dict[str, Any],
    executable: str,
) -> dict[str, Any]:
    validator = clone / spec["validator"]
    raw = validator.read_bytes()
    require(sha256(raw) == spec["validator_sha256"], "E_SUBORDINATE_VALIDATOR_SHA", spec["unit"])
    argv = [executable,spec["validator"],*invocation["args"]]
    process = run_process(argv,cwd=clone,timeout=1800)
    stdout = process.stdout.decode("utf-8")
    stderr = process.stderr.decode("utf-8")
    lines = stdout.splitlines()
    require(process.returncode == 0, "E_SUBORDINATE_EXIT", f"{spec['unit']}:{stdout[-1200:]}:{stderr[-1200:]}")
    require(process.stderr == b"", "E_SUBORDINATE_STDERR", f"{spec['unit']}:{stderr[-1200:]}")
    terminal = invocation["terminal_prefix"]
    require(sum(line.startswith(terminal) for line in lines) == 1, "E_SUBORDINATE_TERMINAL", f"{spec['unit']}:{terminal}")
    observed_required: list[str] = []
    for required_prefix in invocation["required_prefixes"]:
        matches = [line for line in lines if line.startswith(required_prefix)]
        require(len(matches) == 1, "E_SUBORDINATE_REQUIRED", f"{spec['unit']}:{required_prefix}")
        observed_required.append(required_prefix)
    return {
        "unit":spec["unit"],"commit":spec["commit"],"historical_parent":spec["parent"],
        "validator_path":spec["validator"],"validator_sha256":spec["validator_sha256"],
        "args":invocation["args"],"shell":False,"timeout_seconds":1800,
        "exit_code":0,"timed_out":False,"stderr_bytes":0,
        "stdout_lf_bytes":len(lf_bytes(process.stdout)),
        "stdout_lf_sha256":sha256(lf_bytes(process.stdout)),
        "banners":[line for line in lines if line.startswith(("PASS", "FAIL"))],
        "terminal_prefix":terminal,"terminal_count":1,
        "required_prefixes":observed_required,"required_prefix_count":len(observed_required),
        "python_policy":"PINNED_PYTHON_3_12_WITH_HISTORICAL_DEPENDENCIES",
        "execution_location":"DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE",
    }


def fresh_historical_validation() -> dict[str, Any]:
    before = repository_snapshot(allow_final_dirt=True)
    executable = subordinate_python()
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        parent, clone = make_historical_clone(spec)
        prefix = f"phase062-step572-{spec['unit'].lower()}-"
        try:
            invocations = spec.get("invocations") or [{"args":spec["args"],"terminal_prefix":spec["terminal_prefix"],"required_prefixes":spec["required_prefixes"]}]
            for invocation in invocations:
                records.append(run_historical_invocation(clone,spec,invocation,executable))
            staged = nul_paths(git(["diff","--cached","--name-only","-z"],cwd=clone).stdout)
            unstaged = nul_paths(git(["diff","--name-only","-z"],cwd=clone).stdout)
            untracked = nul_paths(git(["ls-files","--others","--exclude-standard","-z"],cwd=clone).stdout)
            require(staged == set(spec["paths"]) and not unstaged and not untracked, "E_SUBORDINATE_MUTATION", spec["unit"])
        finally:
            remove_temp_tree(parent,prefix)
    after = repository_snapshot(allow_final_dirt=True)
    require(canonical_bytes(before) == canonical_bytes(after), "E_ACTIVE_REPOSITORY_MUTATION", "historical runs")
    require(len(records) == 8, "E_SUBORDINATE_INVOCATION_COUNT", str(len(records)))
    return {"unit_count":7,"invocation_count":8,"pass_count":8,"records":records,"historical_exact_staged_context":True,"active_repository_unchanged":True,"cleanup_pass_count":7}


def repository_snapshot(*, allow_final_dirt: bool) -> dict[str, Any]:
    branch = git_text(["branch","--show-current"])
    head = git_text(["rev-parse","HEAD"])
    upstream_name = git_text(["rev-parse","--abbrev-ref","@{upstream}"])
    upstream = git_text(["rev-parse","@{upstream}"])
    tracking = git_text(["rev-parse",f"refs/remotes/origin/{ACTIVE_BRANCH}"])
    live = live_tip(ACTIVE_BRANCH)
    local_protected = git_text(["rev-parse",f"refs/heads/{PROTECTED_BRANCH}"])
    tracked_protected = git_text(["rev-parse",f"refs/remotes/origin/{PROTECTED_BRANCH}"])
    live_protected = live_tip(PROTECTED_BRANCH)
    tracked_main = git_text(["rev-parse","refs/remotes/origin/main"])
    live_main = live_tip("main")
    dirt = status_paths()
    require(branch == ACTIVE_BRANCH, "E_ACTIVE_BRANCH", branch)
    require(upstream_name == f"origin/{ACTIVE_BRANCH}", "E_UPSTREAM_NAME", upstream_name)
    require(head == upstream == tracking == live, "E_ACTIVE_REMOTE", f"{head}/{upstream}/{tracking}/{live}")
    require(local_protected == tracked_protected == live_protected == PROTECTED_TIP, "E_PROTECTED_DRIFT", f"{local_protected}/{tracked_protected}/{live_protected}")
    require(tracked_main == live_main == MAIN_TIP, "E_MAIN_DRIFT", f"{tracked_main}/{live_main}")
    if allow_final_dirt:
        require(not (dirt - FINAL_PATH_SET), "E_EXTRA_DIRT", str(sorted(dirt - FINAL_PATH_SET)))
    else:
        require(not dirt, "E_PERSISTENCE_DIRTY", str(sorted(dirt)))
    claude_tracked = git_text(["diff","--name-only",PARENT_COMMIT,"--","Claude"]).splitlines()
    claude_untracked = git_text(["ls-files","--others","--exclude-standard","--","Claude"]).splitlines()
    require(not claude_tracked and not claude_untracked, "E_CLAUDE_DRIFT", str(claude_tracked+claude_untracked))
    return {"branch":branch,"head":head,"upstream_name":upstream_name,"upstream":upstream,"origin_active":tracking,"live_active":live,"local_protected":local_protected,"origin_protected":tracked_protected,"live_protected":live_protected,"origin_main":tracked_main,"live_main":live_main,"only_final_allowlist_dirty":True,"claude_tracked_diff_count":0,"claude_untracked_count":0}


def stable_repository_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Retain verified ref topology without serializing the moving active tip."""
    projected = copy.deepcopy(snapshot)
    for key in ("head", "upstream", "origin_active", "live_active"):
        require(re.fullmatch(r"[0-9a-f]{40}", projected[key]) is not None, "E_REPOSITORY_PROJECTION", key)
        projected[key] = "<OPERATIONAL_ACTIVE_COMMIT_MASKED>"
    projected["operational_active_commit_masked"] = True
    return projected


def independent_gc_tst(step53: dict[str, Any]) -> dict[str, Any]:
    gas = 8.31446261815324
    faraday = 96485.33212
    temperature = 298.15
    weights = [2.0,3.0,5.0]
    energies = [-4000.0,0.0,6000.0]
    target = 0.41

    def occupation(voltage: float) -> list[float]:
        chemical_potential = -faraday * voltage
        output: list[float] = []
        for energy in energies:
            exponent = (energy-chemical_potential)/(gas*temperature)
            if exponent >= 0:
                e = math.exp(-exponent)
                output.append(e/(1.0+e))
            else:
                e = math.exp(exponent)
                output.append(1.0/(1.0+e))
        return output

    def residual(voltage: float) -> float:
        theta = occupation(voltage)
        return sum(weight*(1.0-value) for weight,value in zip(weights,theta))/sum(weights)-target

    lo,hi = -0.5,0.5
    require(residual(lo)*residual(hi) < 0, "E_GC_EXISTENCE", "bracket")
    for _ in range(160):
        mid = (lo+hi)/2.0
        if residual(lo)*residual(mid) <= 0:
            hi = mid
        else:
            lo = mid
    root = (lo+hi)/2.0
    theta = occupation(root)
    analytic = faraday/(gas*temperature)*sum(weight*value*(1-value) for weight,value in zip(weights,theta))/sum(weights)
    h = 1e-6
    finite_difference = (residual(root+h)-residual(root-h))/(2*h)
    single_target = 0.37
    single_energy = 1250.0
    single_closed = (gas*temperature*math.log(single_target/(1-single_target))-single_energy)/faraday
    zero_variance_strict = False

    tst = step53["tst_rederivation"]["numeric_probe"]
    t1,t2 = 600.0,1200.0
    k1,k2 = 1.0,0.5
    ratio_changes = k1 != k2 and abs(t1*k1-t2*k2) < 1e-14
    t0 = 298.15
    a,b = 1.5,200.0
    ln_k = a*math.log(t0/t0)+b*(1/t0-1/t0)
    dln = a/t0-b/(t0*t0)
    entropy = gas*(ln_k+t0*dln)
    kappa = 0.37
    omitted_factor = 1.0/kappa
    stored_gc = step53["grand_canonical_derivation"]["numeric_probe"]["multiclass"]
    stored_tst = tst["temperature_dependent_partition_ratio"]
    require(abs(root-stored_gc["root_V"]) < 2e-12, "E_GC_ROOT", repr(root))
    require(abs(analytic-stored_gc["analytic_dresidual_dV_per_V"]) < 2e-10, "E_GC_DERIVATIVE", repr(analytic))
    require(abs(finite_difference-analytic) < 2e-8, "E_GC_FINITE_DIFFERENCE", repr(finite_difference))
    require(abs(single_closed-step53["grand_canonical_derivation"]["numeric_probe"]["single_class"]["closed_root_V"]) < 2e-12, "E_GC_SINGLE_CLASS", repr(single_closed))
    require(not zero_variance_strict and analytic > 0, "E_GC_UNIQUENESS", "variance boundary")
    require(ratio_changes, "E_TST_TEMPERATURE_RATIO", "constant ratio")
    require(abs(entropy-stored_tst["correct_delta_S_J_per_molK"]) < 2e-12, "E_TST_ENTROPY", repr(entropy))
    require(abs(omitted_factor-tst["rate"]["relative_omission_factor"]) < 2e-12, "E_TST_KAPPA", repr(omitted_factor))
    require("electrode overpotential/current law" in step53["tst_rederivation"]["scope_separation"]["not_derived"], "E_TST_SCOPE", "electrode")
    return {"gc":{"weights":weights,"target":target,"root_V":root,"analytic_derivative":analytic,"finite_difference_derivative":finite_difference,"positive_variance":True,"zero_variance_strict_uniqueness":False,"single_class_closed_root_V":single_closed},"tst":{"T1_K":t1,"T2_K":t2,"K_ratio_changes":ratio_changes,"T_times_K_constant":True,"deltaS_J_per_molK":entropy,"kappa":kappa,"omitted_kappa_factor":omitted_factor,"electrode_barrier_derived":False,"peak_width_derived":False},"independent_implementation":True}


def integrated_contracts(objects: dict[str, Any]) -> dict[str, Any]:
    activation = objects["Codex/results/PHASE_062_PLAN_ACTIVATION_VALIDATION.json"]
    topology = objects["Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json"]
    reads = objects["Codex/results/PHASE_062_V1021_READ_ATTESTATION.json"]
    step53 = objects["Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json"]
    step54 = objects["Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"]
    code = objects["Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json"]
    runtime = objects["Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json"]
    closure = objects["Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json"]
    disposition = objects["Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json"]
    carry = objects["Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json"]

    require(activation["gate"] == "PASS_P062_PLAN_ACTIVATION" and activation["summary"] == {"checks_failed":0,"checks_passed":115,"checks_total":115,"failed_codes":[]}, "E_ACTIVATION_CONTRACT", "115/115")
    source_expected = {"release_occurrences":68,"release_unique_paths":68,"release_unique_blobs":68,"release_text_files":63,"release_text_physical_lines":21048,"release_text_nonblank_lines":20424,"release_pdf_files":5,"release_pdf_pages":214,"release_snapshot_files":9,"supplemental_occurrences":1}
    require({key:topology["counts"][key] for key in source_expected} == source_expected, "E_SOURCE_COUNTS", repr(topology["counts"]))
    read_expected = {"release_text_files":63,"release_text_physical_lines":21048,"release_text_nonblank_lines":20424,"release_pdf_files":5,"release_pdf_pages":214,"snapshot_files":9,"supplemental_files":1,"supplemental_physical_lines":76}
    require({key:reads["counts"][key] for key in read_expected} == read_expected, "E_READ_COUNTS", repr(reads["counts"]))
    require(len(topology["sources"]) == 68 and len({row["source_id"] for row in topology["sources"]}) == 68 and len({row["path"] for row in topology["sources"]}) == 68, "E_SOURCE_IDENTITIES", "68")
    require(len(reads["release_text_records"]) == 63 and len(reads["pdf_records"]) == 5, "E_READ_RECORDS", "63/5")
    require(sum(len(row["pages"]) for row in reads["pdf_records"]) == 214, "E_PDF_PAGES", "214")

    require(step53["gate"] == "PASS_P062_STEP53_STATMECH_TST_REDERIVATION", "E_STEP53_GATE", str(step53.get("gate")))
    require(step53["summary"]["findings"] == {"P0":0,"P1":5,"P2":5}, "E_STEP53_FINDINGS", repr(step53["summary"]["findings"]))
    physics = independent_gc_tst(step53)

    require(len(step54["bibliography_audit"]["rows"]) == 28, "E_LCO_BIBLIOGRAPHY", "28")
    require(len(step54["citation_occurrences"]) == 72, "E_LCO_CITATIONS", "72")
    require(len(step54["source_claim_manifest"]) == 482 and len(step54["scope_matrix"]) == 482, "E_LCO_SCOPE_BIJECTION", "482")
    require(len(step54["ground_not_found_records"]) == 17, "E_LCO_GNF", "17")
    require(step54["authority_contract"] == {"canonical_equation_accepted":False,"external_experimental_truth_validated":False,"external_material_truth_validated":False,"external_scientific_truth_validated":False,"final_manuscript_ready":False,"scope":"internal lineage, arithmetic, unit/basis, source-tier, proposition and owner routing"}, "E_LCO_AUTHORITY", repr(step54["authority_contract"]))

    code_expected = {"queue_count":11,"comparison_endpoint_count":14,"endpoint_disposition_count":14,"counterpart_count":7,"adjacent_comparison_count":7,"static_python_count":9,"claim_consumer_count":4,"code_matched_claim_count":1,"required_negative_control_count":78}
    require({key:code[key] for key in code_expected} == code_expected, "E_CODE_COUNTS", repr({key:code.get(key) for key in code_expected}))
    require(code["finding_counts"] == {"P0":0,"P1":5,"P2":4}, "E_CODE_FINDINGS", repr(code["finding_counts"]))
    require(runtime["facts"]["behavior_delta_count"] == 0 and runtime["facts"]["v1020_v1021_behavior_identical"] is True and runtime["facts"]["regression_13_of_13_bit_exact"] is True, "E_RUNTIME_FACTS", repr(runtime["facts"]))
    require(runtime["authority"] == {"experimental":False,"external_science":False,"material":False,"static_to_runtime_promotion":False}, "E_RUNTIME_AUTHORITY", repr(runtime["authority"]))
    require(runtime["cleanup"]["completed"] is True and len(runtime["official_runs"]) == 5, "E_RUNTIME_RUNS", "5")

    require(closure["content_denominator"]["count"] == 48 and closure["content_denominator"]["decision_counts"] == {"ADOPTED":12,"NON_ADOPTED":36}, "E_CLOSURE_DECISIONS", repr(closure["content_denominator"]))
    require(closure["acceptance"] == {"A01":"PASS","A02":"PASS","A03":"PASS","A04":"PASS","A05":"PASS","A06":"OPEN","A07":"OPEN","P061-BD-NEW-001":"OPEN"}, "E_CLOSURE_ACCEPTANCE", repr(closure["acceptance"]))
    require(closure["controlled_assets"]["family_counts"] == {"A":10,"C":18,"N":5,"R":5}, "E_CONTROLLED_ASSETS", repr(closure["controlled_assets"]["family_counts"]))
    require(len(closure["controlled_assets"]["numbered_equations"]) == 9 and len(closure["controlled_assets"]["unnumbered_displays"]) == 6, "E_EQUATION_COUNTS", "9/6")
    require(closure["code_mentions"]["forbidden_rendered_count"] == 21, "E_CODE_MENTIONS", "21")
    require(closure["review_vote_authority"] == {"aggregate_counts_not_votes":True,"candidate_routes":31,"ground_not_found":31,"individual_votes":0}, "E_REVIEW_VOTES", repr(closure["review_vote_authority"]))
    builds = closure["build_audit"]["builds"]
    require(len(builds) == 5 and [row["pages"] for row in builds] == [8,76,78,26,26] and all(row["exit_codes"] == [0,0,0] for row in builds), "E_BUILD_AUDIT", "5x3")
    require(closure["authority"] == {"canonical":False,"experimental":False,"external_scientific":False,"final_release":False,"material":False}, "E_CLOSURE_AUTHORITY", repr(closure["authority"]))

    gate = disposition["gate_summary"]
    require(gate["release_disposition_count"] == 68 and gate["supplemental_disposition_count"] == 1 and gate["disposition_counts"] == {"CORRECT":30,"PRESERVE":16,"THEORY_ONLY":13,"UNVERIFIED":9}, "E_DISPOSITION_COUNTS", repr(gate))
    require(len({row["source_id"] for row in disposition["release_dispositions"]}) == 68, "E_DISPOSITION_BIJECTION", "68")
    cgate = carry["gate_summary"]
    carry_expected = {"phase061_target62_route_count":149,"inherited_carry_count":52,"inherited_phase060_blocker_count":5,"canonical_debt_count":91,"inherited_phase061_blocker_count":5,"new_phase062_blocker_count":0,"open_finding_count":59,"open_finding_ownerless_count":0,"open_finding_multiply_owned_count":0,"external_authority_promotion_count":0,"status":"PASS_WITH_CONCERNS"}
    require(cgate == carry_expected, "E_CARRY_COUNTS", repr(cgate))
    require(len(carry["phase061_target62_routes"]) == 149 and sum(len(row["carry_forward_links"]) for row in carry["phase061_target62_routes"]) == 253, "E_CARRY_LINKS", "149/253")
    require(len(carry["inherited_carry_items"]) == 52 and len(carry["inherited_phase060_blockers"]) == 5 and len(carry["canonical_debt_routing"]) == 91 and len(carry["inherited_phase061_blockers"]) == 5 and not carry["new_phase062_blockers"], "E_CARRY_LAYERS", "52+5+91+5+0")

    return {
        "activation":{"checks":115,"gate":"PASS_P062_PLAN_ACTIVATION"},
        "source":{"release":68,"blobs":68,"text":63,"physical_lines":21048,"nonblank_lines":20424,"pdfs":5,"pdf_pages":214,"snapshots":9,"supplemental":1},
        "statmech_tst":{"findings":{"P0":0,"P1":5,"P2":5},"independent_checks":physics},
        "lco_si":{"bibliography":28,"citations":72,"claims":482,"scope_rows":482,"ground_not_found":17,"authority_promotions":0},
        "code_runtime":{"queue":11,"endpoints":14,"dispositions":14,"counterparts":7,"adjacent":7,"static":9,"consumers":4,"q8":1,"runtime_runs":5,"behavior_delta":0,"findings":{"P0":0,"P1":5,"P2":4}},
        "closure":{"proposals":48,"adopted":12,"nonadopted":36,"controlled_assets":38,"numbered_equations":9,"unnumbered_displays":6,"rendered_code_mentions":21,"builds":5,"passes":15,"pages":[8,76,78,26,26],"A01_A05_pass":5,"A06_A07_parent_open":3},
        "disposition_carry":{"release":68,"supplemental":1,"distribution":{"CORRECT":30,"PRESERVE":16,"THEORY_ONLY":13,"UNVERIFIED":9},"target62":149,"links":253,"inherited":52,"phase060_blockers":5,"debts":91,"phase061_blockers":5,"new_blockers":0,"open_findings":59,"ownerless":0,"multiply_owned":0},
        "authority":{"external_scientific":False,"external_material":False,"experimental":False,"primary_literature":False,"canonical":False,"final_latex_pdf":False},
    }


FINAL_TOP_KEYS = {
    "schema_version", "phase", "step", "generated_date", "gate", "status",
    "expected_parent", "expected_subject", "authority_boundary", "authority",
    "validator_identity", "exact_eight", "repository", "input_inventory",
    "step_commit_inventory", "historical_execution", "integrated_contracts",
    "output_contract", "negative_control_contract", "determinism", "semantic_sha256",
}

PERSISTENCE_ARGS: dict[str, tuple[list[str], str]] = {
    "ACTIVATION": (["--verify-persistence", "--expected-commit", ACTIVATION_COMMIT], "PASS_P062_PLAN_ACTIVATION_PERSISTENCE"),
    "STEP52": (["--verify-persistence", "--expected-commit", STEP52_COMMIT], "PASS_P062_STEP52_PERSISTENCE"),
    "STEP53": (["--verify-persistence", "--expected-commit", STEP53_COMMIT], "PASS_P062_STEP53_PERSISTENCE"),
    "STEP54": (["--mode", "persistence"], "PASS_P062_STEP54_PERSISTENCE"),
    "STEP55": (["--verify-persistence"], "PASS_P062_STEP55_PERSISTENCE"),
    "STEP56": (["--verify-persistence"], "PASS_P062_STEP56_PERSISTENCE"),
    "STEP57_1": (["--mode", "persistence", "--expected-commit", STEP57_COMMIT], "PASS_P062_STEP57_1_PERSISTENCE"),
}


def markdown_lines(path: str) -> tuple[bytes, list[str]]:
    require((ROOT / path).is_file(), "E_OUTPUT_MISSING", path)
    raw = (ROOT / path).read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeError as error:
        raise ValidationError("E_OUTPUT_UTF8", path) from error
    return raw, text.splitlines()


def exact_line_count(lines: list[str], pattern: str) -> int:
    regex = re.compile(pattern)
    return sum(regex.fullmatch(line) is not None for line in lines)


def output_inventory() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    content: dict[str, list[str]] = {}
    for path in NONSELF_PATHS:
        raw, lines = markdown_lines(path) if path.endswith(".md") else ((ROOT / path).read_bytes(), [])
        records.append({"path": path, "sha256_lf": sha256(lf_bytes(raw)), "bytes": len(raw), "physical_lines": len(raw.decode("utf-8").splitlines())})
        if lines:
            content[path] = lines
    require({row["path"] for row in records} == set(NONSELF_PATHS), "E_OUTPUT_SET", "seven nonself")
    report = content[REPORT_PATH]
    gate = content[GATE_RESULT_PATH]
    phase = content[PHASE_RESULT_PATH]
    require(exact_line_count(report, r"Gate: `PASS_P062_LINEAGE_E`") == 1, "E_REPORT_GATE", REPORT_PATH)
    require(exact_line_count(gate, r"Selected Gate: `PASS_P062_LINEAGE_E`") == 1, "E_GATE_RESULT_GATE", GATE_RESULT_PATH)
    require(exact_line_count(phase, r"Exclusive Gate: `PASS_P062_LINEAGE_E`") == 1, "E_PHASE_RESULT_GATE", PHASE_RESULT_PATH)
    for path, lines in ((REPORT_PATH, report), (GATE_RESULT_PATH, gate), (PHASE_RESULT_PATH, phase)):
        require(exact_line_count(lines, r"Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`") == 1, "E_RESULT_FIRST", path)
        text = "\n".join(lines)
        require(SUBJECT in text and PARENT_COMMIT in text and "PASS_P062_STEP57_2_PERSISTENCE" in text and "Phase 063" in text and "Step 58" in text, "E_RESULT_CONTRACT", path)
        require(not re.search(r"(?im)^(?:selected |exclusive )?gate\s*[:=]\s*`?(?:FAIL|CONDITIONAL)", text), "E_RESULT_CONTRADICTION", path)
    parent = content[PARENT_LEDGER_PATH]
    active = content[ACTIVE_LEDGER_PATH]
    handover = content[HANDOVER_PATH]
    require(sum(line.startswith("| 062 |") for line in parent) == 1, "E_PARENT_LEDGER_ROW", "Phase062")
    require(sum(line.startswith("| 062 |") for line in active) == 1, "E_ACTIVE_LEDGER_ROW", "Phase062")
    require(sum(line.startswith("| Step 57.2 |") for line in active) == 1, "E_ACTIVE_COMMIT_ROW", "Step57.2")
    require(sum(line.startswith("| Phase 062 Step 57.2 |") for line in handover) == 1, "E_HANDOVER_ROW", "Step57.2")
    for path, lines in ((PARENT_LEDGER_PATH, parent), (ACTIVE_LEDGER_PATH, active), (HANDOVER_PATH, handover)):
        joined = "\n".join(lines)
        require(all(token in joined for token in (PARENT_COMMIT, "PASS_P062_LINEAGE_E", "PASS_P062_STEP57_2_PERSISTENCE", "Phase 063", "Step 58")), "E_CONTROL_CONTRACT", path)
        if path != PARENT_LEDGER_PATH:
            require(SUBJECT in joined, "E_CONTROL_CONTRACT", f"{path}: subject")
    return {"count": 7, "paths": sorted(NONSELF_PATHS), "records": sorted(records, key=lambda row: row["path"]), "result_first": True, "validation_json_written_last": True, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"}


def make_persistence_clone(spec: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path]:
    prefix = f"phase062-step572-persist-{spec['unit'].lower()}-"
    parent = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    clone = parent / "repo"
    process = run_process(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], timeout=180)
    require(process.returncode == 0, "E_PERSISTENCE_FIXTURE_CLONE", process.stderr.decode("utf-8", errors="replace"))
    try:
        git(["config", "core.autocrlf", "false"], cwd=clone)
        git(["checkout", "-B", ACTIVE_BRANCH, spec["commit"]], cwd=clone)
        git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", spec["commit"]], cwd=clone)
        git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=clone)
        git(["update-ref", "refs/remotes/origin/main", MAIN_TIP], cwd=clone)
        git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=clone)
        git(["update-ref", "refs/heads/main", MAIN_TIP], cwd=clone)
        git(["remote", "set-url", "origin", "."], cwd=clone)
        git(["branch", "--set-upstream-to", f"origin/{ACTIVE_BRANCH}", ACTIVE_BRANCH], cwd=clone)
        require(not status_paths(clone), "E_PERSISTENCE_FIXTURE_DIRT", spec["unit"])
    except Exception:
        remove_temp_tree(parent, prefix)
        raise
    return parent, clone


def fresh_historical_persistence() -> dict[str, Any]:
    executable = subordinate_python()
    records: list[dict[str, Any]] = []
    before = repository_snapshot(allow_final_dirt=True)
    for spec in UNIT_SPECS:
        parent, clone = make_persistence_clone(spec)
        prefix = f"phase062-step572-persist-{spec['unit'].lower()}-"
        try:
            args, terminal = PERSISTENCE_ARGS[spec["unit"]]
            process = run_process([executable, spec["validator"], *args], cwd=clone, timeout=1800)
            stdout = process.stdout.decode("utf-8", errors="replace")
            stderr = process.stderr.decode("utf-8", errors="replace")
            require(process.returncode == 0, "E_HISTORICAL_PERSISTENCE_EXIT", f"{spec['unit']}:{stdout[-1000:]}:{stderr[-1000:]}")
            require(sum(line.startswith(terminal) for line in stdout.splitlines()) == 1, "E_HISTORICAL_PERSISTENCE_TERMINAL", spec["unit"])
            require(not status_paths(clone), "E_HISTORICAL_PERSISTENCE_MUTATION", spec["unit"])
            records.append({"unit": spec["unit"], "commit": spec["commit"], "args": args,
                "terminal_prefix": terminal, "terminal_count": 1, "exit_code": 0,
                "stderr_bytes": len(process.stderr), "stdout_lf_bytes": len(lf_bytes(process.stdout)),
                "stdout_lf_sha256": sha256(lf_bytes(process.stdout)),
                "banners": [line for line in stdout.splitlines() if line.startswith(("PASS", "FAIL"))],
                "execution_location": "DISPOSABLE_CLEAN_HISTORICAL_PERSISTENCE_CLONE"})
        finally:
            remove_temp_tree(parent, prefix)
    require(canonical_bytes(before) == canonical_bytes(repository_snapshot(allow_final_dirt=True)), "E_ACTIVE_REPOSITORY_MUTATION", "persistence runs")
    return {"unit_count": 7, "pass_count": 7, "records": records, "historical_clean_persistence_context": True, "cleanup_pass_count": 7}


def build_document(precommit_runs: dict[str, Any], persistence_runs: dict[str, Any]) -> dict[str, Any]:
    validate_source_policy()
    objects, inputs = load_pinned_inputs()
    integrated = integrated_contracts(objects)
    outputs = output_inventory()
    validator_raw = lf_bytes(VALIDATOR.read_bytes())
    document: dict[str, Any] = {
        "schema_version": "P062-STEP57.2-1",
        "phase": "062", "step": "57.2", "generated_date": "2026-08-27",
        "gate": "PASS_P062_LINEAGE_E", "status": "PASS_WITH_CONCERNS",
        "expected_parent": PARENT_COMMIT, "expected_subject": SUBJECT,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "authority": copy.deepcopy(integrated["authority"]),
        "validator_identity": {"path": VALIDATOR_PATH, "sha256_lf": sha256(validator_raw), "bytes_lf": len(validator_raw), "source_policy": "NO_PRODUCTION_IMPORT_OR_EXECUTION"},
        "exact_eight": {"count": 8, "paths": FINAL_PATHS, "result_first": True, "json_last": True},
        "repository": stable_repository_projection(repository_snapshot(allow_final_dirt=True)),
        "input_inventory": inputs,
        "step_commit_inventory": step_commit_inventory(),
        "historical_execution": {"precommit": precommit_runs, "persistence": persistence_runs, "unit_count": 7, "invocation_count": 15, "pass_count": 15},
        "integrated_contracts": integrated,
        "output_contract": outputs,
        "negative_control_contract": {"named_count": 24, "strict_json_count": 5, "git_boundary_count": 13, "singleton_required": True},
        "determinism": {"projections": 2, "byte_identical": True, "environment_fields_excluded": True},
    }
    document["semantic_sha256"] = semantic_hash(document)
    full_traversal(document)
    return document


def document_diagnostics(document: Any, expected: dict[str, Any]) -> set[str]:
    if type(document) is not dict or set(document) != FINAL_TOP_KEYS:
        return {"E_FINAL_SCHEMA"}
    failures: set[str] = set()
    comparisons = (
        ("E_FINAL_IDENTITY", (document["phase"], document["step"], document["generated_date"]), ("062", "57.2", "2026-08-27")),
        ("E_FINAL_GATE", (document["gate"], document["status"]), ("PASS_P062_LINEAGE_E", "PASS_WITH_CONCERNS")),
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
    if document.get("semantic_sha256") != semantic_hash(document):
        failures.add("E_FINAL_SEMANTIC_HASH")
    return failures


def run_negative_controls(baseline: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = []
    def add(code: str, mutation: Callable[[dict[str, Any]], None], rehash: bool = True) -> None:
        cases.append((code, mutation, rehash))
    add("E_FINAL_SCHEMA", lambda d: d.__setitem__("unexpected", 1), False)
    add("E_FINAL_IDENTITY", lambda d: d.__setitem__("step", "58"))
    add("E_FINAL_GATE", lambda d: d.__setitem__("gate", "CONDITIONAL_P062"))
    add("E_FINAL_PARENT_SUBJECT", lambda d: d.__setitem__("expected_parent", "0" * 40))
    add("E_FINAL_AUTHORITY", lambda d: d["authority"].__setitem__("external_scientific", True))
    add("E_FINAL_VALIDATOR", lambda d: d["validator_identity"].__setitem__("sha256_lf", "0" * 64))
    add("E_FINAL_ALLOWLIST", lambda d: d["exact_eight"]["paths"].pop())
    add("E_FINAL_REPOSITORY", lambda d: d["repository"].__setitem__("live_active", "0" * 40))
    add("E_FINAL_INPUTS", lambda d: d["input_inventory"].__setitem__("machine_count", 9))
    add("E_FINAL_COMMITS", lambda d: d["step_commit_inventory"].pop())
    add("E_FINAL_HISTORICAL", lambda d: d["historical_execution"].__setitem__("pass_count", 14))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["source"].__setitem__("pdf_pages", 213))
    add("E_FINAL_OUTPUTS", lambda d: d["output_contract"].__setitem__("result_first", False))
    add("E_FINAL_NEGATIVE_CONTRACT", lambda d: d["negative_control_contract"].__setitem__("singleton_required", False))
    add("E_FINAL_DETERMINISM", lambda d: d["determinism"].__setitem__("byte_identical", False))
    add("E_FINAL_AUTHORITY_BOUNDARY", lambda d: d.__setitem__("authority_boundary", "overclaim"))
    add("E_FINAL_SEMANTIC_HASH", lambda d: d.__setitem__("semantic_sha256", "0" * 64), False)
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["statmech_tst"]["independent_checks"]["gc"].__setitem__("positive_variance", False))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["statmech_tst"]["independent_checks"]["tst"].__setitem__("electrode_barrier_derived", True))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["lco_si"].__setitem__("claims", 481))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["code_runtime"].__setitem__("behavior_delta", 1))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["closure"].__setitem__("A01_A05_pass", 4))
    add("E_FINAL_INTEGRATED", lambda d: d["integrated_contracts"]["disposition_carry"].__setitem__("new_blockers", 1))
    add("E_FINAL_HISTORICAL", lambda d: d["historical_execution"]["precommit"].__setitem__("invocation_count", 7))
    passed = 0
    for wanted, mutation, rehash in cases:
        candidate = copy.deepcopy(baseline)
        mutation(candidate)
        if rehash and set(candidate) == FINAL_TOP_KEYS:
            candidate["semantic_sha256"] = semantic_hash(candidate)
        observed = document_diagnostics(candidate, baseline)
        require(observed == {wanted}, "E_NEGATIVE_NOT_SINGLETON", f"{wanted}:{sorted(observed)}")
        passed += 1
    strict_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e9999}']
    for raw in strict_cases:
        try:
            strict_load_bytes(raw, "negative")
        except ValidationError as error:
            require(error.code in {"E_DUPLICATE_JSON", "E_NONFINITE_JSON"}, "E_STRICT_NEGATIVE_CODE", error.code)
        else:
            raise ValidationError("E_STRICT_NEGATIVE_ESCAPE", raw.decode("ascii"))
    return passed, len(cases)


def fixture_snapshot(repo: pathlib.Path) -> dict[str, Any]:
    staged = nul_paths(git(["diff", "--cached", "--name-only", "-z"], cwd=repo).stdout)
    return {
        "branch": git_text(["branch", "--show-current"], cwd=repo),
        "head": git_text(["rev-parse", "HEAD"], cwd=repo),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"], cwd=repo),
        "upstream": git_text(["rev-parse", "@{upstream}"], cwd=repo),
        "origin_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"], cwd=repo),
        "live_active": live_tip(ACTIVE_BRANCH, cwd=repo),
        "local_protected": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=repo),
        "origin_protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"], cwd=repo),
        "live_protected": live_tip(PROTECTED_BRANCH, cwd=repo),
        "origin_main": git_text(["rev-parse", "refs/remotes/origin/main"], cwd=repo),
        "live_main": live_tip("main", cwd=repo),
        "staged": sorted(staged),
        "unstaged": sorted(nul_paths(git(["diff", "--name-only", "-z"], cwd=repo).stdout)),
        "untracked": sorted(nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=repo).stdout)),
        "index_worktree_equal": all(git(["show", f":{path}"], cwd=repo).stdout == (repo / path).read_bytes() for path in staged),
    }


def boundary_diagnostics(snapshot: dict[str, Any], parent: str) -> set[str]:
    checks = (
        ("E_GIT_BRANCH", snapshot["branch"] == ACTIVE_BRANCH),
        ("E_GIT_UPSTREAM_NAME", snapshot["upstream_name"] == f"origin/{ACTIVE_BRANCH}"),
        ("E_GIT_HEAD", snapshot["head"] == parent),
        ("E_GIT_UPSTREAM", snapshot["upstream"] == parent),
        ("E_GIT_ACTIVE_TRACKING", snapshot["origin_active"] == parent),
        ("E_GIT_ACTIVE_LIVE", snapshot["live_active"] == parent),
        ("E_GIT_LOCAL_PROTECTED", snapshot["local_protected"] == parent),
        ("E_GIT_PROTECTED_TRACKING", snapshot["origin_protected"] == parent),
        ("E_GIT_PROTECTED_LIVE", snapshot["live_protected"] == parent),
        ("E_GIT_MAIN_TRACKING", snapshot["origin_main"] == parent),
        ("E_GIT_MAIN_LIVE", snapshot["live_main"] == parent),
        ("E_GIT_STAGED_SET", set(snapshot["staged"]) == FINAL_PATH_SET),
        ("E_GIT_INDEX_WORKTREE", snapshot["index_worktree_equal"] and not snapshot["unstaged"] and not snapshot["untracked"]),
    )
    return {code for code, passed in checks if not passed}


def run_git_boundary_controls() -> tuple[int, int]:
    prefix = "phase062-step572-git-"
    parent_dir = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    repo = parent_dir / "repo"
    origin = parent_dir / "origin.git"
    try:
        require(run_process(["git", "init", "--bare", str(origin)], cwd=parent_dir).returncode == 0, "E_GIT_FIXTURE_INIT", "bare")
        require(run_process(["git", "init", str(repo)], cwd=parent_dir).returncode == 0, "E_GIT_FIXTURE_INIT", "repo")
        git(["config", "user.name", "Phase062 Fixture"], cwd=repo)
        git(["config", "user.email", "phase062-fixture@example.invalid"], cwd=repo)
        git(["checkout", "-b", ACTIVE_BRANCH], cwd=repo)
        for index, path in enumerate(FINAL_PATHS):
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"baseline-{index}\n", encoding="utf-8", newline="\n")
        git(["add", "--", *FINAL_PATHS], cwd=repo)
        git(["commit", "-m", "fixture parent"], cwd=repo)
        fixture_parent = git_text(["rev-parse", "HEAD"], cwd=repo)
        git(["remote", "add", "origin", str(origin)], cwd=repo)
        git(["push", "-u", "origin", ACTIVE_BRANCH], cwd=repo)
        git(["push", "origin", f"HEAD:refs/heads/{PROTECTED_BRANCH}"], cwd=repo)
        git(["push", "origin", "HEAD:refs/heads/main"], cwd=repo)
        git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", fixture_parent], cwd=repo)
        git(["update-ref", "refs/remotes/origin/main", fixture_parent], cwd=repo)
        git(["branch", PROTECTED_BRANCH, fixture_parent], cwd=repo)
        for index, path in enumerate(FINAL_PATHS):
            (repo / path).write_text(f"candidate-{index}\n", encoding="utf-8", newline="\n")
        git(["add", "--", *FINAL_PATHS], cwd=repo)
        baseline = fixture_snapshot(repo)
        require(not boundary_diagnostics(baseline, fixture_parent), "E_GIT_FIXTURE_BASELINE", repr(boundary_diagnostics(baseline, fixture_parent)))
        cases = [
            ("E_GIT_BRANCH", "branch", "detached"),
            ("E_GIT_UPSTREAM_NAME", "upstream_name", "origin/wrong"),
            ("E_GIT_HEAD", "head", "0" * 40),
            ("E_GIT_UPSTREAM", "upstream", "0" * 40),
            ("E_GIT_ACTIVE_TRACKING", "origin_active", "0" * 40),
            ("E_GIT_ACTIVE_LIVE", "live_active", "0" * 40),
            ("E_GIT_LOCAL_PROTECTED", "local_protected", "0" * 40),
            ("E_GIT_PROTECTED_TRACKING", "origin_protected", "0" * 40),
            ("E_GIT_PROTECTED_LIVE", "live_protected", "0" * 40),
            ("E_GIT_MAIN_TRACKING", "origin_main", "0" * 40),
            ("E_GIT_MAIN_LIVE", "live_main", "0" * 40),
            ("E_GIT_STAGED_SET", "staged", FINAL_PATHS[:-1]),
            ("E_GIT_INDEX_WORKTREE", "index_worktree_equal", False),
        ]
        for wanted, key, value in cases:
            candidate = copy.deepcopy(baseline)
            candidate[key] = value
            require(boundary_diagnostics(candidate, fixture_parent) == {wanted}, "E_GIT_NEGATIVE_NOT_SINGLETON", f"{wanted}:{sorted(boundary_diagnostics(candidate, fixture_parent))}")
        return len(cases), len(cases)
    finally:
        remove_temp_tree(parent_dir, prefix)


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
    require(git(["diff", "--check"]).returncode == 0 and git(["diff", "--cached", "--check"]).returncode == 0, "E_DIFF_CHECK", "precommit")


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


def deterministic_pair(precommit_runs: dict[str, Any], persistence_runs: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    first = build_document(precommit_runs, persistence_runs)
    second = build_document(copy.deepcopy(precommit_runs), copy.deepcopy(persistence_runs))
    first_raw, second_raw = pretty_bytes(first), pretty_bytes(second)
    require(first_raw == second_raw, "E_DETERMINISM", "2/2")
    return first, first_raw


def atomic_collect(raw: bytes) -> None:
    require(not ARTIFACT.exists(), "E_COLLECT_REFUSES_OVERWRITE", ARTIFACT_PATH)
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST", "seven nonself outputs")
    temp_path = ARTIFACT.with_name(ARTIFACT.name + ".tmp-step572")
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
    precommit_runs = fresh_historical_validation()
    persistence_runs = fresh_historical_persistence()
    expected, expected_raw = deterministic_pair(precommit_runs, persistence_runs)
    failures = document_diagnostics(expected, expected)
    require(not failures, "E_FRESH_DOCUMENT", repr(sorted(failures)))
    if collect:
        negative_passed, negative_total = run_negative_controls(expected)
        git_passed, git_total = run_git_boundary_controls()
        atomic_collect(expected_raw)
        print(f"PASS_P062_STEP57_2_NEGATIVE_CONTROLS {negative_passed}/{negative_total} strict_json=5/5 singleton=true")
        print(f"PASS_P062_STEP57_2_GIT_CONTROLS {git_passed}/{git_total} disposable_fixture=true cleanup=true")
        print("PASS_P062_STEP57_2_DETERMINISM 2/2")
        print("PASS_P062_LINEAGE_E collect=JSON_LAST result_first=true historical=15/15")
        return 0
    failures = document_diagnostics(stored, expected)
    require(not failures, "E_STORED_DOCUMENT", repr(sorted(failures)))
    require(stored_raw == expected_raw, "E_STORED_BYTE_IDENTITY", ARTIFACT_PATH)
    automatic_full = mode in {"precommit", "persistence"}
    if run_negative or automatic_full:
        negative_passed, negative_total = run_negative_controls(stored)
        git_passed, git_total = run_git_boundary_controls()
        print(f"PASS_P062_STEP57_2_NEGATIVE_CONTROLS {negative_passed}/{negative_total} strict_json=5/5 singleton=true")
        print(f"PASS_P062_STEP57_2_GIT_CONTROLS {git_passed}/{git_total} disposable_fixture=true cleanup=true")
    if run_determinism or automatic_full:
        print("PASS_P062_STEP57_2_DETERMINISM 2/2")
    if mode == "precommit":
        validate_staged()
        print("PASS_P062_STEP57_2_PRECOMMIT exact_eight=8/8 historical=15/15")
    elif mode == "persistence":
        require(expected_commit is not None, "E_EXPECTED_COMMIT", "required")
        validate_persistence(expected_commit)
        print(f"PASS_P062_STEP57_2_PERSISTENCE commit={expected_commit}")
    else:
        print("PASS_P062_LINEAGE_E artifact=true historical=15/15")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="artifact")
    parser.add_argument("--expected-commit")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    if not args.collect and not ARTIFACT.is_file():
        raise ValidationError("E_VALIDATION_ARTIFACT_MISSING", ARTIFACT_PATH)
    require(not (args.collect and args.mode != "artifact"), "E_CLI_MODE", "collect with repository mode")
    return execute_validation(collect=args.collect, mode=args.mode, expected_commit=args.expected_commit, run_negative=args.run_negative_probes, run_determinism=args.determinism_check)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, TypeError, ValueError, OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL_P062_LINEAGE_E: {error}")
        raise SystemExit(1)
