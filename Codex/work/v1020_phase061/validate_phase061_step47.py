#!/usr/bin/env python3
"""Validate Phase 061 Step 47 process-authority evidence and persistence."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable

from PIL import Image
from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1020_phase061/build_phase061_step47_process_authority.py"
VALIDATOR = Path(__file__).resolve()
MATRIX = REPO / "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json"
RESULT = REPO / "Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
EXPECTED_PARENT = "4c951f390c63f11f1c5a03cc47c7e3bce32926de"
EXPECTED_SUBJECT = "audit(phase061): adjudicate v1020 process authority"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EXPECTED_BUILDER_SHA256 = "09f7a0b0e5cfcdd0b1c1e9378aee8a5972bcf08dbc7d4b2dceac329295d12a1d"
EXPECTED_BUILDER_SECURITY_AST_SHA256 = "72aabe3da9b3a9b464b008832d461e0c7538cdc811fb06fa972ae0ba729890ac"
EXPECTED_MATRIX_SHA256 = "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403"
INPUT_COMMIT = EXPECTED_PARENT
BASELINE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
TOPOLOGY_PATH = "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
TOPOLOGY_SHA256_LF = "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c"
COMMAND_TIMEOUT = 30
BUILDER_TIMEOUT = 120
BOUNDARY_NEGATIVE_IDS = (
    "RESULT_MISSING", "RESULT_EXPLICIT_FAIL", "RESULT_TOKEN_ONLY_FAKE",
    "ACTIVE_LEDGER_MISSING", "ACTIVE_LEDGER_BAD_ROW",
    "PARENT_LEDGER_MISSING", "PARENT_LEDGER_BAD_ROW",
    "HANDOVER_MISSING", "HANDOVER_BAD_ROW", "EXTRA_DIRTY_PATH",
    "ACTIVE_REMOTE_DIVERGENCE", "PROTECTED_DRIFT", "MAIN_DRIFT",
    "CLAUDE_DRIFT", "CRLF_EQUIVALENCE", "CLAIM_SEMANTIC_CONTRACT",
    "BUILDER_AST_POLICY",
)
_UNSET = object()

EXACT_SEVEN = [
    "Codex/work/v1020_phase061/build_phase061_step47_process_authority.py",
    "Codex/work/v1020_phase061/validate_phase061_step47.py",
    "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json",
    "Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]
EXACT_SEVEN_SET = set(EXACT_SEVEN)

ALLOWED_AUTHORITY_CLASSES = {
    "USER_REQUIREMENT", "PLAN_INTENT", "PROCESS_SELF_ASSESSMENT",
    "INTERNAL_REVIEW", "COMPETING_DRAFT", "ADOPTED_RELEASE_SOURCE",
    "STRUCTURAL_WITNESS", "EXTERNAL_SCIENTIFIC_UNVERIFIED",
}
ALLOWED_CLAIM_TYPES = {
    "user_requirement", "plan", "self_review", "multi_review",
    "adoption", "completion", "scientific", "structural",
}
EXPECTED_SOURCE_CLASS_COUNTS = {
    "ADOPTED_RELEASE_SOURCE": 43, "COMPETING_DRAFT": 82,
    "EXTERNAL_SCIENTIFIC_UNVERIFIED": 7, "INTERNAL_REVIEW": 16,
    "PLAN_INTENT": 13, "PROCESS_SELF_ASSESSMENT": 22,
    "STRUCTURAL_WITNESS": 49,
}
EXPECTED_CLAIM_CLASS_COUNTS = {
    "ADOPTED_RELEASE_SOURCE": 1, "COMPETING_DRAFT": 4,
    "EXTERNAL_SCIENTIFIC_UNVERIFIED": 4, "INTERNAL_REVIEW": 10,
    "PLAN_INTENT": 2, "PROCESS_SELF_ASSESSMENT": 5,
    "STRUCTURAL_WITNESS": 6, "USER_REQUIREMENT": 8,
}
EXPECTED_CLAIM_CLASS_IDS = {
    "USER_REQUIREMENT": {26, 27, 28, 29, 30, 36, 47, 51},
    "PLAN_INTENT": {33, 48},
    "PROCESS_SELF_ASSESSMENT": {32, 37, 38, 45, 56},
    "INTERNAL_REVIEW": {34, 39, 40, 41, 42, 43, 44, 49, 57, 58},
    "COMPETING_DRAFT": {46, 52, 54, 55},
    "ADOPTED_RELEASE_SOURCE": {50},
    "EXTERNAL_SCIENTIFIC_UNVERIFIED": {31, 35, 53, 59},
    "STRUCTURAL_WITNESS": {60, 61, 62, 63, 64, 65},
}
EXPECTED_CLAIM_TYPE_IDS = {
    "adoption": {50, 61}, "completion": {37, 45, 56, 65},
    "multi_review": {39, 44, 57}, "plan": {33, 46, 48},
    "scientific": {31, 35, 40, 41, 42, 43, 52, 53, 54, 55, 59},
    "self_review": {34, 38, 58}, "structural": {32, 49, 60, 62, 63, 64},
    "user_requirement": {26, 27, 28, 29, 30, 36, 47, 51},
}
# Independently pinned SHA-256 over canonical JSON for each entire semantic claim row.
EXPECTED_CLAIM_ROW_SHA256 = {
    "INTENT-PROV-0026": "2b756f6ef2d7bf83eec5102e156b2734c5107d66072bc65c42b5285d6dde2a94",
    "INTENT-PROV-0027": "46e6aa5f3f8a5481a1d8444f74d2fb818bdfca30c2cb9c846f1b64ab3c9c334d",
    "INTENT-PROV-0028": "8a2fc04dfc89623f70030917b5b266883d0390f1f6de058f3ce2c076297723ac",
    "INTENT-PROV-0029": "d1c4217ec9e1516dc9687605a986c8154763f7c2b7a6b8dfb57b9efdea946bd5",
    "INTENT-PROV-0030": "7438758fa53571af60587f14bfad48f243998cf295d0d727819e0b1c348cc744",
    "INTENT-PROV-0031": "2171242194764a798d618926edb37653a3d3d31383650cf01f5d6f820dc98a60",
    "INTENT-PROV-0032": "9076816ac50d205256d864acadbb7bbd9453490bde0df5f37457cd54d2c07bbb",
    "INTENT-PROV-0033": "1a332cb325ed87e5c52d947df45036806c175ca30a248ba3218ea85b450f190f",
    "INTENT-PROV-0034": "770cca36ab5e8c821414ca00349f34df1949b1b65a711559f83dd37cfc89c08c",
    "INTENT-PROV-0035": "b0a9ec41e771b496ef05688ec29ce73b2f8a927085bda0da43b3907a9919cd3d",
    "INTENT-PROV-0036": "e0460f25ac6244521a4208f7dacedafd768e7cac553c61f74d07e090f794c8cf",
    "INTENT-PROV-0037": "07e8fd3ec687ee7324c03599baeab8e6cb153af0fc31daa349fb0e6d7e6d20c3",
    "INTENT-PROV-0038": "cfa9952fe7115320baa1b29a36b6074d20d70294e68fadd3fa825562c1f92bd1",
    "INTENT-PROV-0039": "932065847550827043bda3040e0b3d15e3f8e76eeedb86b99da825c7c41b88fb",
    "INTENT-PROV-0040": "096441256083d8e13b87d1681201d20d79cb204f934db6cac020f08df032bc18",
    "INTENT-PROV-0041": "32ec73b00a83cd141884ac902ca4a7309e498e36a97778f88d04d4f4753b3853",
    "INTENT-PROV-0042": "60dd1a46fc4fbcb5d75f18c8728539139c9be0947107042b16fda2aff7ad0254",
    "INTENT-PROV-0043": "a8ef8e4fa401bb9803228d3bc83d9cd7e9ea2520dcd7644dda7280ecddd086f2",
    "INTENT-PROV-0044": "e60ade75e7ae5da191458b75a7a46c4363c82c0b40566e5c58f41bfcd5ed09e4",
    "INTENT-PROV-0045": "72b3170392c400b7bc771214e6594c7384ade0663ea8280af5517dd0c5814613",
    "INTENT-PROV-0046": "78f2b010e1428625a96f24627275133ad6a95cc0daa5bf0924c8b258ee8060a2",
    "INTENT-PROV-0047": "41a0a7424f2723e90167abd66d1b9ffe33c5758c0b0651917d5328641f5bafe3",
    "INTENT-PROV-0048": "33f6aaceb90a4f7b18923b3886b117cbad39b7af767d34a50dffc9b07bcc1c9e",
    "INTENT-PROV-0049": "dae088492b070f8336e5a555821b5f77cd836f53fde1fae086cfd7a44beb8a49",
    "INTENT-PROV-0050": "d873109a593b8ec483fb20853519a5ed86d4f0cfeb16f00a5c277cf7c89ff6da",
    "INTENT-PROV-0051": "f923010653ae9a830cfa8352c4fb5c5063ee405eb402d01b7de1e9f500d1eb96",
    "INTENT-PROV-0052": "ffe675dd7f3444b8ef0e692ca31a4c37fb1f9e87ed98263bd71624b746d3f1e3",
    "INTENT-PROV-0053": "d51c2a8255767659e827f0ca11d755a442b842dd57259d0646a63d4fbd0f7438",
    "INTENT-PROV-0054": "17b8cb853838b44ccee8ee2b09c15b9ab12d5d7975604b1c35f63b2698cbb6a0",
    "INTENT-PROV-0055": "1f74c2ecb0f3d40c178d04d717c8a418e97c87370b7c5c51dfa97fae4d569fd5",
    "INTENT-PROV-0056": "2567643d3d4d13b3cfeadc1e0231e1c8d19f17c2b4126fa26f7bfa8c4ed2201e",
    "INTENT-PROV-0057": "bb7c2c69cc07a9812ef3418bfbe31ca015d219a1a98cd407850eb07ee0732600",
    "INTENT-PROV-0058": "9a4a8c650dcd2babded9dda549874dd9ff685fc46f7f0019572f69ed3868635f",
    "INTENT-PROV-0059": "5671339d65de9333057fcb3306c000b9b5dd72ecbceaed4ee562d526394ce971",
    "INTENT-PROV-0060": "e47c684979ed05d4a1bf32bdf05e8a5de3bb281a3521f2f3c534d18d0e84dbdd",
    "INTENT-PROV-0061": "5b2782137f4ba40f3a1cb46ecce6353e07d01b039ddc9f00ee251964569c8678",
    "INTENT-PROV-0062": "c4d04cbe8100a459704bdc7e6a9442161fc84427efb0c6899d1e41965e25c678",
    "INTENT-PROV-0063": "13ad90d5fa5d694b6703b0b7f17a3d01bbb37aa202461010d1f2adc0f737caa6",
    "INTENT-PROV-0064": "159dba0681b43c93f41d934bfb75e7fb90f10d4ad815bbf7cab69fb959b2b689",
    "INTENT-PROV-0065": "5b38c463dd0e172a652c2b3f6a81a214b01d2574f72333b6a29b55dbc3f26ecb",
}
EXPECTED_CLAIM_TOP_FIELDS = {
    "actual_evidence", "adoption_edge", "adoption_edge_state", "authority_ceiling",
    "claim_authority_class", "claim_id", "claim_type", "claimant", "components",
    "contradiction", "contradiction_ids", "evidence_gap", "evidence_route_ids",
    "expected_evidence", "external_scientific_truth", "intent_id", "machine_comparison_ids",
    "object", "provisional_observation", "scientific_authority_promoted", "status",
    "target_phase", "target_step",
}
EXPECTED_TOP_FIELDS = {
    "artifact_kind", "authority_classes", "authority_policy", "baseline_commit",
    "boundaries", "builder", "claims", "contradictions", "counts",
    "frozen_source_validation", "gate", "generated_date", "ground_not_found",
    "input_commit", "observation_inputs", "phase", "phase_table",
    "process_source_ids", "required_negative_controls", "schema_version",
    "snapshot_machine_comparisons", "source_routes", "status", "step",
    "topology", "unverified_queue",
}
EXPECTED_COMPARISON_IDS = [
    "P061-SNAP-CMP-0060", "P061-SNAP-CMP-0061-A",
    "P061-SNAP-CMP-0061-B", "P061-SNAP-CMP-0062",
    "P061-SNAP-CMP-0063", "P061-SNAP-CMP-0065",
]
EXPECTED_NEGATIVES = (
    "DUPLICATE_JSON_KEY", "NONFINITE_JSON", "INPUT_COMMIT_MISMATCH",
    "TOPOLOGY_FROZEN_HASH_MISMATCH", "OBSERVATION_BLOB_MISMATCH",
    "OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH", "MISSING_TOP_FIELD",
    "EXTRA_TOP_FIELD", "SOURCE_ROUTE_MISSING", "SOURCE_ROUTE_DUPLICATE",
    "SOURCE_ROUTE_ORPHAN", "SOURCE_BLOB_MISMATCH", "SOURCE_LINE_EXTENT_MISMATCH",
    "PDF_EXTENT_TAMPER", "IMAGE_EXTENT_TAMPER", "JSON_STRICT_PARSE_TAMPER",
    "SOURCE_AUTHORITY_CLASS_MULTIPLE", "SOURCE_AUTHORITY_ROUTE_MISMATCH",
    "ADOPTED_RELEASE_TOPOLOGY_MISSING", "ADOPTED_TEX_ORPHAN",
    "DIRECTION_SOURCE_PROMOTED", "AUTHOR_BRIEF_NOT_PLAN", "INTERCHAPTER_NOT_REVIEW",
    "CLAIM_MISSING", "CLAIM_DUPLICATE", "CLAIMANT_RANGE_INVALID",
    "CLAIMANT_SLICE_HASH_MISMATCH", "CLAIM_TYPE_NOT_SEMANTIC",
    "CLAIM_AUTHORITY_CLASS_INVALID", "CLAIM_EVIDENCE_EMPTY", "CLAIM_EVIDENCE_ORPHAN",
    "CLAIM_EVIDENCE_RANGE_OR_STATUS_INVALID", "CLAIM_EVIDENCE_SLICE_HASH_MISMATCH",
    "CLAIM_EXPECTED_EVIDENCE_OR_GAP_MISSING", "CIRCULAR_SELF_CERTIFICATION",
    "ADOPTION_EDGE_REQUIRED_MISSING", "ADOPTION_EDGE_SELF_REFERENCE",
    "ADOPTION_EDGE_PROCESS_TARGET", "CLAIM_0036_0037_INVALID_ADOPTION",
    "CLAIM_0049_0057_FALSE_ADOPTION", "CLAIM_0050_ADOPTION_MISSING",
    "CLAIM_0061_ADOPTION_TARGET_MISMATCH", "PLAN_TO_SCIENCE_PROMOTION",
    "REVIEW_TO_PRIMARY_PROMOTION", "SNAPSHOT_TO_PHYSICAL_VALIDITY",
    "STRUCTURE_PROJECTION_TAMPER", "STRUCTURE_DELTA_TAMPER",
    "TEST_PASS_TO_EXPERIMENT", "BIBLIOGRAPHY_PRESENCE_TO_PRIMARY_SUPPORT",
    "P5_P6_OCCURRENCE_COLLAPSE", "P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY",
    "UNLABELED_MOVE_AS_ADD_DELETE", "APPENDIX_PREFINAL_HISTORY_FALSE",
    "PREFINAL_APPENDIX_FALSE_ABSENCE", "SNAPSHOT_0063_INPUT_MISSING",
    "SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH", "SNAPSHOT_0063_FINAL_ROOT_MISMATCH",
    "SNAPSHOT_0063_PROJECTION_TAMPER", "P8_DEDICATED_RESULT_FALSE_PRESENT",
    "P8_DEDICATED_LOG_FALSE_PRESENT", "P8_TOTAL_EVIDENCE_FALSE_GNF",
    "P8_INTERNAL_PASS_TO_SCIENCE", "STATUS_CONFIRMED_WITH_GNF_EVIDENCE",
    "CONTRADICTED_WITH_NULL_CONTRADICTION", "CONTRADICTION_ROW_MISSING",
    "CONTRADICTION_ANCHOR_HASH_MISMATCH", "CONTRADICTION_ATTACHMENT_ORPHAN",
    "PHASE_TABLE_ROW_MISSING", "PHASE_TABLE_LEDGER_ANCHOR_MISMATCH",
    "PHASE_TABLE_GATE_OR_STEP_MISMATCH", "P8_COMMIT_CHAIN_MISMATCH",
    "USER_TRANSCRIPT_FALSE_PRESENT", "P8_PLAN_ANCHOR_MISMATCH",
    "UNVERIFIED_QUEUE_MISSING", "EXTERNAL_TRUTH_TRUE", "GATE_NOT_PASS_WITH_CONCERNS",
    "TARGET_MISSING", "DETERMINISM_MISMATCH",
)


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


class ValidationError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def walk_json(value: Any, depth: int = 0, stats: dict[str, int] | None = None) -> dict[str, int]:
    if stats is None:
        stats = {"nodes": 0, "max_depth": 0}
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], depth)
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(str(depth))
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(key)
            walk_json(child, depth + 1, stats)
    elif isinstance(value, list):
        for child in value:
            walk_json(child, depth + 1, stats)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise TypeError(type(value).__name__)
    return stats


def strict_load(path: Path) -> tuple[Any, dict[str, int]]:
    return strict_load_bytes(path.read_bytes())


def strict_load_bytes(data: bytes) -> tuple[Any, dict[str, int]]:
    value = json.loads(
        data.decode("utf-8-sig"), object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
    )
    return value, walk_json(value)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def lf_bytes(data: bytes) -> bytes:
    return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def normalize_lf(path: Path) -> bytes:
    return lf_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def line_slice(data: bytes, start: int, end: int) -> bytes:
    lines = lf_bytes(data).decode("utf-8").splitlines()
    if not (1 <= start <= end <= len(lines)):
        raise ValidationError(f"SLICE_RANGE:{start}:{end}:{len(lines)}")
    return ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")


def run_git(*args: str, check: bool = True) -> str:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=REPO, text=True, encoding="utf-8", errors="strict",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            timeout=COMMAND_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"GIT_COMMAND_TIMEOUT:{' '.join(args)}:{COMMAND_TIMEOUT}s") from exc
    if check and proc.returncode:
        raise ValidationError(
            f"GIT_COMMAND_FAILED:{' '.join(args)}:returncode={proc.returncode}:stderr={proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def run_git_bytes(*args: str) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=REPO, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False, timeout=COMMAND_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"GIT_COMMAND_TIMEOUT:{' '.join(args)}:{COMMAND_TIMEOUT}s") from exc
    if proc.returncode:
        raise ValidationError(
            f"GIT_COMMAND_FAILED:{' '.join(args)}:returncode={proc.returncode}:"
            f"stderr={proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    try:
        proc = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, timeout=COMMAND_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(
            f"GIT_COMMAND_TIMEOUT:merge-base --is-ancestor:{COMMAND_TIMEOUT}s"
        ) from exc
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    raise ValidationError(
        "GIT_COMMAND_FAILED:merge-base --is-ancestor:"
        f"returncode={proc.returncode}:"
        f"stderr={proc.stderr.decode('utf-8', errors='replace').strip()}"
    )


def git_blob_batch(commit: str, paths: Iterable[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(paths))
    request = b"".join(f"{commit}:{path}\n".encode("utf-8") for path in ordered)
    try:
        proc = subprocess.run(
            ["git", "cat-file", "--batch"], cwd=REPO, input=request,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            timeout=COMMAND_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"GIT_COMMAND_TIMEOUT:cat-file --batch:{COMMAND_TIMEOUT}s") from exc
    if proc.returncode:
        raise ValidationError(
            "GIT_COMMAND_FAILED:cat-file --batch:"
            f"returncode={proc.returncode}:stderr={proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    result: dict[str, bytes] = {}
    cursor = 0
    for path in ordered:
        newline = proc.stdout.find(b"\n", cursor)
        if newline < 0:
            raise ValidationError(f"GIT_BLOB_HEADER_TRUNCATED:{commit}:{path}")
        header = proc.stdout[cursor:newline].decode("ascii", errors="strict")
        cursor = newline + 1
        fields = header.split()
        if len(fields) == 2 and fields[1] == "missing":
            raise ValidationError(f"GIT_BLOB_MISSING:{commit}:{path}")
        if len(fields) != 3 or fields[1] != "blob":
            raise ValidationError(f"GIT_BLOB_HEADER:{commit}:{path}:{header}")
        size = int(fields[2])
        data = proc.stdout[cursor:cursor + size]
        cursor += size
        if len(data) != size or proc.stdout[cursor:cursor + 1] != b"\n":
            raise ValidationError(f"GIT_BLOB_TRUNCATED:{commit}:{path}")
        cursor += 1
        result[path] = data
    if cursor != len(proc.stdout):
        raise ValidationError(f"GIT_BLOB_TRAILING_OUTPUT:{len(proc.stdout) - cursor}")
    return result


def nul_paths(*args: str) -> set[str]:
    return {
        item.decode("utf-8").replace("\\", "/")
        for item in run_git_bytes(*args).split(b"\0") if item
    }


def porcelain_paths() -> set[str]:
    fields = run_git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all").split(b"\0")
    result: set[str] = set()
    index = 0
    while index < len(fields) and fields[index]:
        row = fields[index].decode("utf-8")
        result.add(row[3:].replace("\\", "/"))
        if "R" in row[:2] or "C" in row[:2]:
            index += 1
            if index < len(fields) and fields[index]:
                result.add(fields[index].decode("utf-8").replace("\\", "/"))
        index += 1
    return result


def exact_dirty_paths() -> set[str]:
    paths = porcelain_paths()
    for relative in EXACT_SEVEN:
        if (REPO / relative).exists() and not run_git("ls-files", "--error-unmatch", relative, check=False):
            paths.add(relative)
    return paths


def remote_tip(branch: str) -> str:
    parts = run_git("ls-remote", "--heads", "origin", branch).split()
    return parts[0] if len(parts) == 2 else ""


CLASS_CEILINGS = {
    "USER_REQUIREMENT": "RECORDED_SECOND_ORDER_REQUIREMENT_ONLY_ORIGINAL_USER_TRANSCRIPT_GROUND_NOT_FOUND",
    "PLAN_INTENT": "PLAN_INTENT_ONLY",
    "PROCESS_SELF_ASSESSMENT": "INTERNAL_PROCESS_ONLY",
    "INTERNAL_REVIEW": "INTERNAL_REVIEW_ONLY",
    "COMPETING_DRAFT": "COMPETING_NOT_ADOPTED",
    "ADOPTED_RELEASE_SOURCE": "RELEASE_CONTENT_ONLY",
    "STRUCTURAL_WITNESS": "STRUCTURE_LINEAGE_ONLY",
    "EXTERNAL_SCIENTIFIC_UNVERIFIED": "EXTERNAL_SCIENCE_UNVERIFIED",
}
SNAPSHOT_PATHS = {
    "baseline": "Claude/docs/v1.0.20/results/snapshot_v1019_baseline.json",
    "final": "Claude/docs/v1.0.20/results/snapshot_v1020_final.json",
    "p0": "Claude/docs/v1.0.20/results/snapshot_v1020_p0.json",
    "p2": "Claude/docs/v1.0.20/results/snapshot_v1020_p2.json",
    "p3": "Claude/docs/v1.0.20/results/snapshot_v1020_p3.json",
    "p4": "Claude/docs/v1.0.20/results/snapshot_v1020_p4.json",
    "p5": "Claude/docs/v1.0.20/results/snapshot_v1020_p5.json",
    "p6": "Claude/docs/v1.0.20/results/snapshot_v1020_p6.json",
    "p7": "Claude/docs/v1.0.20/results/snapshot_v1020_p7.json",
    "p7b": "Claude/docs/v1.0.20/results/snapshot_v1020_p7b.json",
}
OBSERVATION_FILES = (
    "Codex/results/PHASE_057E_V1020_FOUNDATION_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057F_V1020_P2_P6_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057G_V1020_P7_REVIEW_DIRECTION_OBSERVATIONS.md",
    "Codex/results/PHASE_057H_V1020_CLOSING_DIRECTION_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057I_V1020_SNAPSHOT_LINEAGE_OBSERVATIONS.md",
)
EXPECTED_P8_CHAIN = (
    "66e3510d67162dd6bd88158557f96621cbedbbcf",
    "c8853c83d79f22059e07c2a548759da6e8310d2d",
    "eb2cd1a32471a40de5511ed159aedf8272792a8a",
    "a0ae6b41e80983940e13851467a07b47e76531f6",
    "1e6c610f11682d87a416957b1cf65b4c8df53697",
    "ba41c9052e9b177268ef65e115dda500d0af3856",
    "c70bcb6f4e2ca0eba6f1b9cfbb0cff7c2f88d862",
)


def classify_eol(data: bytes) -> str:
    crlf = data.count(b"\r\n")
    bare_cr = data.count(b"\r") - crlf
    bare_lf = data.count(b"\n") - crlf
    kinds = sum(bool(value) for value in (crlf, bare_cr, bare_lf))
    if kinds > 1:
        return "MIXED"
    if crlf:
        return "CRLF"
    if bare_cr:
        return "CR"
    return "LF"


def canonical_ast_dump(node: ast.AST) -> str:
    options: dict[str, Any] = {"annotate_fields": True, "include_attributes": False}
    if sys.version_info >= (3, 13):
        options["show_empty"] = True
    return ast.dump(node, **options)


def builder_security_ast_projection(tree: ast.AST) -> dict[str, Any]:
    imports = [
        canonical_ast_dump(node)
        for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    subprocess_aliases = {
        alias.asname or "subprocess"
        for node in ast.walk(tree) if isinstance(node, ast.Import)
        for alias in node.names if alias.name == "subprocess"
    }
    subprocess_direct = {
        alias.asname or alias.name
        for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module == "subprocess"
        for alias in node.names
    }
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    subprocess_calls = [
        node for node in calls
        if (
            isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
            and node.func.value.id in subprocess_aliases
        ) or (
            isinstance(node.func, ast.Name) and node.func.id in subprocess_direct
        )
    ]
    helper_definitions = [
        canonical_ast_dump(node)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "_run_git_bytes"
    ]
    helper_references = [
        canonical_ast_dump(node)
        for node in ast.walk(tree) if isinstance(node, ast.Name) and node.id == "_run_git_bytes"
    ]
    return {
        "full_normalized_ast": canonical_ast_dump(tree),
        "imports": imports,
        "all_calls": [canonical_ast_dump(node) for node in calls],
        "subprocess_calls": [
            {
                "call": canonical_ast_dump(node),
                "argv": canonical_ast_dump(node.args[0]) if node.args else None,
                "keywords": [
                    {"arg": keyword.arg, "value": canonical_ast_dump(keyword.value)}
                    for keyword in node.keywords
                ],
            }
            for node in subprocess_calls
        ],
        "run_git_helper_definitions": helper_definitions,
        "run_git_helper_references": helper_references,
    }


def builder_ast_policy_diagnostics(data: bytes) -> set[str]:
    try:
        tree = ast.parse(lf_bytes(data).decode("utf-8"), filename=BUILDER.as_posix())
    except (SyntaxError, UnicodeError):
        return {"BUILDER_AST_POLICY"}
    diagnostics: set[str] = set()
    if sha256(canonical_bytes(builder_security_ast_projection(tree))) != EXPECTED_BUILDER_SECURITY_AST_SHA256:
        diagnostics.add("BUILDER_AST_POLICY")
    prohibited_calls = {"exec", "eval", "__import__"}
    subprocess_methods = {"run", "Popen", "call", "check_call", "check_output"}
    allowed_import_roots = {
        "__future__", "argparse", "hashlib", "io", "json", "math", "re",
        "subprocess", "collections", "pathlib", "typing", "PIL", "pypdf",
    }
    subprocess_aliases: set[str] = set()
    subprocess_functions: set[str] = set()
    dangerous_functions: set[str] = set(prohibited_calls)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
            for alias in node.names:
                if alias.name == "subprocess":
                    subprocess_aliases.add(alias.asname or "subprocess")
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
            if node.module == "subprocess":
                diagnostics.add("BUILDER_AST_POLICY")
                for alias in node.names:
                    if alias.name in subprocess_methods:
                        subprocess_functions.add(alias.asname or alias.name)
            if node.module == "builtins":
                for alias in node.names:
                    if alias.name in prohibited_calls:
                        dangerous_functions.add(alias.asname or alias.name)
        else:
            names = []
        if any(name.split(".", 1)[0] not in allowed_import_roots for name in names):
            diagnostics.add("BUILDER_AST_POLICY")
    # Track straightforward module/function aliases before checking calls.
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value = node.value
        target_names = [target.id for target in targets if isinstance(target, ast.Name)]
        if isinstance(value, ast.Name) and value.id in subprocess_aliases:
            subprocess_aliases.update(target_names)
        if (
            isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name)
            and value.value.id in subprocess_aliases and value.attr in subprocess_methods
        ):
            subprocess_functions.update(target_names)
        if isinstance(value, ast.Name) and value.id in dangerous_functions:
            dangerous_functions.update(target_names)
        if (
            isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
            and value.func.id == "getattr" and value.args
            and isinstance(value.args[0], ast.Name)
            and value.args[0].id in subprocess_aliases | {"builtins", "__builtins__"}
        ):
            diagnostics.add("BUILDER_AST_POLICY")
        if (
            isinstance(value, ast.Subscript)
            and isinstance(value.value, ast.Attribute)
            and value.value.attr == "__dict__"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id in subprocess_aliases
        ):
            diagnostics.add("BUILDER_AST_POLICY")

    def constant_string(node: ast.AST) -> str | None:
        return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None

    def readonly_git_tail(elements: list[ast.expr]) -> bool:
        command = constant_string(elements[0]) if elements else None
        if command == "rev-parse":
            argument = constant_string(elements[1]) if len(elements) == 2 else "-"
            return len(elements) == 2 and (argument is None or not argument.startswith("-"))
        if command == "diff":
            return (
                len(elements) == 6 and constant_string(elements[1]) == "--name-only"
                and constant_string(elements[4]) == "--"
                and all(constant_string(item) is None or not constant_string(item).startswith("-") for item in elements[2:4])
                and not (constant_string(elements[5]) or "").startswith("-")
            )
        if command == "merge-base":
            return (
                len(elements) == 4 and constant_string(elements[1]) == "--is-ancestor"
                and all(constant_string(item) is None or not constant_string(item).startswith("-") for item in elements[2:])
            )
        if command == "ls-tree":
            return (
                len(elements) == 6 and constant_string(elements[1]) == "--full-tree"
                and constant_string(elements[2]) == "-z" and constant_string(elements[4]) == "--"
                and (constant_string(elements[3]) is None or not constant_string(elements[3]).startswith("-"))
                and not (constant_string(elements[5]) or "").startswith("-")
            )
        if command == "cat-file":
            return (
                len(elements) == 2 and constant_string(elements[1]) == "--batch"
            ) or (
                len(elements) == 3 and constant_string(elements[1]) == "blob"
                and (constant_string(elements[2]) is None or not constant_string(elements[2]).startswith("-"))
            )
        return False

    helper_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        and node.func.id == "_run_git_bytes"
    ]
    helper_calls_read_only = bool(helper_calls) and all(
        len(node.args) >= 2
        and isinstance(node.args[1], (ast.List, ast.Tuple))
        and readonly_git_tail(node.args[1].elts)
        for node in helper_calls
    )
    function_owner: dict[int, str] = {}
    for function in (node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))):
        for child in ast.walk(function):
            function_owner[id(child)] = function.name

    def literal_git_argv(call: ast.Call) -> bool:
        argv = call.args[0] if call.args else None
        if not isinstance(argv, (ast.List, ast.Tuple)) or not argv.elts or constant_string(argv.elts[0]) != "git":
            return False
        tail = argv.elts[1:]
        if len(tail) == 1 and isinstance(tail[0], ast.Starred):
            return (
                function_owner.get(id(call)) == "_run_git_bytes"
                and isinstance(tail[0].value, ast.Name) and tail[0].value.id == "args"
                and helper_calls_read_only
            )
        return readonly_git_tail(tail)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in dangerous_functions:
            diagnostics.add("BUILDER_AST_POLICY")
        if isinstance(node.func, ast.Name) and node.func.id in subprocess_functions and not literal_git_argv(node):
            diagnostics.add("BUILDER_AST_POLICY")
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"import_module", "exec_module"}:
            diagnostics.add("BUILDER_AST_POLICY")
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in subprocess_aliases
            and (node.func.attr not in subprocess_methods or not literal_git_argv(node))
        ):
            diagnostics.add("BUILDER_AST_POLICY")
        if isinstance(node.func, ast.Call) and isinstance(node.func.func, ast.Name) and node.func.func.id == "getattr":
            getter = node.func
            target = getter.args[0] if getter.args else None
            attribute = getter.args[1] if len(getter.args) > 1 else None
            attribute_value = attribute.value if isinstance(attribute, ast.Constant) else None
            if (
                isinstance(target, ast.Name)
                and (
                    target.id in subprocess_aliases
                    or target.id in {"builtins", "__builtins__"}
                    or attribute_value in prohibited_calls
                )
            ):
                diagnostics.add("BUILDER_AST_POLICY")
        if (
            isinstance(node.func, ast.Subscript)
            and isinstance(node.func.value, ast.Attribute)
            and node.func.value.attr == "__dict__"
            and isinstance(node.func.value.value, ast.Name)
            and node.func.value.value.id in subprocess_aliases
        ):
            diagnostics.add("BUILDER_AST_POLICY")
        if (
            isinstance(node.func, ast.Subscript)
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Name)
            and node.func.value.func.id in {"globals", "locals", "vars"}
        ):
            diagnostics.add("BUILDER_AST_POLICY")
    return diagnostics


def builder_static_diagnostics(data: bytes) -> set[str]:
    # The normalized full-AST pin rejects semantic changes; this fixed LF source
    # hash separately rejects comment- or whitespace-only source changes.
    diagnostics = builder_ast_policy_diagnostics(data)
    if sha256(lf_bytes(data)) != EXPECTED_BUILDER_SHA256:
        diagnostics.add("BUILDER_FIXED_HASH_MISMATCH")
    return diagnostics


def expected_source_authority(row: dict[str, Any]) -> str:
    group = row["derived_authority_group"]
    basename = row["basename"]
    path = row["path"]
    extension = row["extension"]
    if group == "FINAL_RELEASE_SURFACE":
        if basename == "HANDOVER_v1.0.20.md":
            return "PROCESS_SELF_ASSESSMENT"
        if extension in {"pdf", "png"}:
            return "STRUCTURAL_WITNESS"
        if basename == "appendix_phase_separation.tex":
            return "COMPETING_DRAFT"
        return "ADOPTED_RELEASE_SOURCE"
    if group == "PLAN_P0_P8":
        return "PLAN_INTENT"
    if group in {"STRUCTURAL_SNAPSHOT", "STRUCTURE_TOOL", "TEST_GATE"}:
        return "STRUCTURAL_WITNESS"
    if group == "CORE_PROCESS_RESULT":
        if basename == "V1020_STYLE_RUBRIC.md":
            return "PLAN_INTENT"
        if basename in {
            "V1020_REFERENCE_LEDGER.md", "V1020_REFLEDGER_DRAFT_candidates.md",
            "V1020_REFLEDGER_DRAFT_existing.md", "V1020_P1_CITATION_BASELINE.md",
        } or basename.startswith("DIRECTION_"):
            return "EXTERNAL_SCIENTIFIC_UNVERIFIED"
        if basename in {"FIGS_PICK_JUDGMENT.md", "INTERCHAPTER_REPORT.md"}:
            return "INTERNAL_REVIEW"
        return "PROCESS_SELF_ASSESSMENT"
    if group == "COMPETITIVE_CANDIDATE_REVIEW":
        if extension in {"pdf", "png"} or row["manifest_role"] in {"figure", "generated_document"}:
            return "STRUCTURAL_WITNESS"
        if basename == "AUTHOR_BRIEF.md":
            return "PLAN_INTENT"
        if basename == "INTERCHAPTER_REPORT.md":
            return "INTERNAL_REVIEW"
        return "INTERNAL_REVIEW" if any(
            marker in path for marker in ("/REVIEW_", "/TRIAGE_", "/PICK_JUDGMENT")
        ) else "COMPETING_DRAFT"
    raise ValidationError(f"SOURCE_AUTHORITY_UNROUTED:{row.get('source_id')}:{group}")


def chapter_projection(chapter: dict[str, Any]) -> dict[str, Any]:
    return {
        "labels": sorted(chapter["labels"]),
        "eqblocks": [
            {"identifier": key, "hash": block["hash"], "boxed": block["boxed"], "file": block["file"]}
            for key, block in sorted(chapter["eqblocks"].items())
        ],
        "asset_unique": chapter["asset_unique"],
        "bibitems": sorted(chapter["bibitems"]),
    }


def snapshot_chapter(snapshot: dict[str, Any], number: int) -> dict[str, Any]:
    matches = [value for key, value in snapshot.items() if f"_ch{number}_" in key]
    if len(matches) != 1:
        raise ValidationError(f"SNAPSHOT_CHAPTER_CARDINALITY:{number}:{len(matches)}")
    return matches[0]


def document_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"ch1": chapter_projection(snapshot_chapter(snapshot, 1)), "ch2": chapter_projection(snapshot_chapter(snapshot, 2))}


def projection_with_sha(value: Any) -> dict[str, Any]:
    return {"projection": value, "projection_sha256": sha256(canonical_bytes(value))}


def eqblock_map(chapter: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["identifier"]: {key: row[key] for key in ("hash", "boxed", "file")} for row in chapter["eqblocks"]}


def eqblock_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    left, right = eqblock_map(before), eqblock_map(after)
    return {
        "added": [{"identifier": key, **right[key]} for key in sorted(set(right) - set(left))],
        "removed": [{"identifier": key, **left[key]} for key in sorted(set(left) - set(right))],
        "changed": [
            {"identifier": key, "before": left[key], "after": right[key]}
            for key in sorted(set(left) & set(right)) if left[key] != right[key]
        ],
    }


def set_delta(before: list[str], after: list[str]) -> dict[str, Any]:
    return {
        "count_before": len(before), "count_after": len(after), "count_delta": len(after) - len(before),
        "added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
    }


def substantive_eqblocks(chapter: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        ({"hash": row["hash"], "boxed": row["boxed"], "file": row["file"]} for row in chapter["eqblocks"]),
        key=lambda row: (row["hash"], row["boxed"], row["file"]),
    )


def claim_semantic_contract_mismatch(claims: Any) -> bool:
    if not isinstance(claims, list) or len(claims) != 40:
        return True
    provisional_keys = {"blob_sha1", "input_commit", "line_end", "line_start", "path", "slice_sha256_lf", "status"}
    evidence_keys = {
        "blob_sha1", "evidence_status", "input_commit", "line_end", "line_start",
        "path", "sha256", "slice_sha256_lf", "source_authority_class", "source_id",
    }
    expected_keys = {
        "external_primary_required_for_scientific_truth", "minimum_actual_anchors",
        "original_independent_user_transcript_required_for_first_order_requirement_authority",
        "semantic_standard",
    }
    gap_keys = {"description", "frozen_plan_or_process_record_role", "original_independent_user_transcript", "status"}
    observed_ids: list[str] = []
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != EXPECTED_CLAIM_TOP_FIELDS:
            return True
        intent = claim.get("intent_id")
        observed_ids.append(intent)
        if (
            not isinstance(claim.get("provisional_observation"), dict)
            or set(claim["provisional_observation"]) != provisional_keys
            or not isinstance(claim.get("claimant"), dict)
            or set(claim["claimant"]) != evidence_keys
            or not isinstance(claim.get("object"), dict)
            or set(claim["object"]) != {"kind", "title"}
            or not isinstance(claim.get("expected_evidence"), dict)
            or set(claim["expected_evidence"]) != expected_keys
            or not isinstance(claim.get("actual_evidence"), list)
            or any(not isinstance(row, dict) or set(row) != evidence_keys for row in claim["actual_evidence"])
            or not isinstance(claim.get("evidence_gap"), dict)
            or set(claim["evidence_gap"]) != gap_keys
        ):
            return True
        edge = claim.get("adoption_edge")
        if edge is not None and (
            not isinstance(edge, dict) or set(edge) != {"edge_type", "targets"}
            or not isinstance(edge.get("targets"), list)
            or any(not isinstance(row, dict) or set(row) != evidence_keys for row in edge["targets"])
        ):
            return True
        contradiction = claim.get("contradiction")
        if contradiction is not None and (
            not isinstance(contradiction, dict)
            or set(contradiction) != {"contradiction_ids", "exact_table_reference"}
        ):
            return True
        if not isinstance(intent, str) or sha256(canonical_bytes(claim)) != EXPECTED_CLAIM_ROW_SHA256.get(intent):
            return True
    return observed_ids != list(EXPECTED_CLAIM_ROW_SHA256)


def independent_frozen_diagnostics(matrix: dict[str, Any]) -> tuple[set[str], dict[str, Any]]:
    """Reconstruct frozen routing, extents, snapshots and Git boundaries without builder code."""
    diagnostics: set[str] = set()
    evidence: dict[str, Any] = {}
    topology_data = git_blob_batch(INPUT_COMMIT, [TOPOLOGY_PATH])[TOPOLOGY_PATH]
    if sha256(lf_bytes(topology_data)) != TOPOLOGY_SHA256_LF:
        diagnostics.add("TOPOLOGY_FROZEN_HASH_MISMATCH")
    topology, topology_traversal = strict_load_bytes(topology_data)
    if not isinstance(topology, dict):
        raise ValidationError("TOPOLOGY_NOT_OBJECT")
    sources = topology.get("sources", [])
    if not isinstance(sources, list) or len(sources) != 232:
        diagnostics.add("SOURCE_ROUTE_MISSING")
        return diagnostics, {"topology_traversal": topology_traversal}
    source_paths = [row.get("path") for row in sources]
    source_ids = [row.get("source_id") for row in sources]
    if (
        any(not isinstance(path, str) for path in source_paths)
        or len(set(source_paths)) != 232
        or source_ids != [f"P061-SRC-{number:04d}" for number in range(1, 233)]
        or [row.get("manifest_index_v1020") for row in sources] != list(range(1, 233))
    ):
        diagnostics.add("SOURCE_ROUTE_MISSING")
        return diagnostics, {"topology_traversal": topology_traversal}
    observed_path_hash = sha256(("\n".join(sorted(source_paths)) + "\n").encode("utf-8"))
    if topology.get("path_set_sha256") != observed_path_hash:
        diagnostics.add("TOPOLOGY_FROZEN_HASH_MISMATCH")
    blobs = git_blob_batch(BASELINE_COMMIT, source_paths)
    routes = matrix.get("source_routes", [])
    route_by_path = {
        row.get("path"): row for row in routes
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if set(source_paths) - set(route_by_path):
        diagnostics.add("SOURCE_ROUTE_MISSING")
    if set(route_by_path) - set(source_paths):
        diagnostics.add("SOURCE_ROUTE_ORPHAN")

    roots = (
        "Claude/docs/v1.0.20/graphite_ica_ch1_v1.0.20.tex",
        "Claude/docs/v1.0.20/graphite_ica_ch2_v1.0.20.tex",
    )
    by_source_path = {row["path"]: row for row in sources}
    include_edges: dict[str, dict[str, Any]] = {}
    for root in roots:
        for number, line in enumerate(lf_bytes(blobs[root]).decode("utf-8").splitlines(), 1):
            match = re.fullmatch(r"\\input\{([^}]+)\}", line.strip())
            if match is None:
                continue
            child = f"Claude/docs/v1.0.20/{match.group(1)}"
            if not child.endswith(".tex"):
                child += ".tex"
            if child in include_edges or child not in by_source_path:
                diagnostics.add("ADOPTED_TEX_ORPHAN")
                continue
            include_edges[child] = {
                "topology_type": "INCLUDED_RELEASE_SECTION",
                "parent_root_source_id": by_source_path[root]["source_id"],
                "parent_root_path": root,
                "input_line_start": number,
                "input_line_end": number,
                "input_slice_sha256_lf": sha256(line_slice(blobs[root], number, number)),
            }
    if len(include_edges) != 39:
        diagnostics.add("ADOPTED_TEX_ORPHAN")
    companions = {
        "Claude/docs/v1.0.20/Anode_Fit_v1.0.20.py",
        "Claude/docs/v1.0.20/FITTING_GUIDE.md",
    }
    observed_text = 0
    observed_text_records: list[dict[str, Any]] = []
    observed_json: list[dict[str, Any]] = []
    observed_pdf: list[dict[str, Any]] = []
    observed_image: list[dict[str, Any]] = []
    expected_class_counter: Counter[str] = Counter()
    for source in sources:
        path = source["path"]
        data = blobs[path]
        route = route_by_path.get(path)
        if route is None:
            continue
        if (
            route.get("source_id") != source.get("source_id")
            or route.get("manifest_index_v1020") != source.get("manifest_index_v1020")
        ):
            diagnostics.add("SOURCE_ROUTE_MISSING")
        if (
            route.get("blob_sha1") != blob_sha1(data)
            or source.get("blob_sha1") != blob_sha1(data)
            or route.get("sha256") != sha256(data)
            or source.get("sha256") != sha256(data)
        ):
            diagnostics.add("SOURCE_BLOB_MISMATCH")
        if route.get("review_mode") != source.get("review_mode") or route.get("manifest_extent") != source.get("manifest_extent"):
            diagnostics.add("SOURCE_LINE_EXTENT_MISMATCH")
        expected_class = expected_source_authority(source)
        expected_class_counter[expected_class] += 1
        actual_class = route.get("source_authority_class")
        if actual_class != expected_class:
            if "/DIRECTION_" in path:
                diagnostics.add("DIRECTION_SOURCE_PROMOTED")
            elif path.endswith("/AUTHOR_BRIEF.md"):
                diagnostics.add("AUTHOR_BRIEF_NOT_PLAN")
            elif path.endswith("/INTERCHAPTER_REPORT.md"):
                diagnostics.add("INTERCHAPTER_NOT_REVIEW")
            else:
                diagnostics.add("SOURCE_AUTHORITY_ROUTE_MISMATCH")
        expected_route_text = f"{source['source_id']} -> frozen Git blob {source['blob_sha1']} -> {expected_class} ceiling"
        if actual_class == expected_class and (
            route.get("authority_ceiling") != CLASS_CEILINGS[expected_class]
            or route.get("evidence_route") != expected_route_text
        ):
            diagnostics.add("SOURCE_AUTHORITY_ROUTE_MISMATCH")
        expected_topology: dict[str, Any] | None = None
        if expected_class == "ADOPTED_RELEASE_SOURCE":
            if path in roots:
                expected_topology = {"topology_type": "DIRECT_RELEASE_ROOT"}
            elif path in companions:
                expected_topology = {"topology_type": "PACKAGE_COMPANION_ROOT"}
            else:
                expected_topology = include_edges.get(path)
            if expected_topology is None:
                diagnostics.add("ADOPTED_TEX_ORPHAN")
            elif route.get("adoption_topology") != expected_topology:
                if route.get("adoption_topology") is None:
                    diagnostics.add("ADOPTED_RELEASE_TOPOLOGY_MISSING")
                elif expected_topology.get("topology_type") == "INCLUDED_RELEASE_SECTION":
                    diagnostics.add("ADOPTED_TEX_ORPHAN")
                else:
                    diagnostics.add("ADOPTED_RELEASE_TOPOLOGY_MISSING")
        elif actual_class == expected_class and route.get("adoption_topology") is not None:
            diagnostics.add("ADOPTED_RELEASE_TOPOLOGY_MISSING")
        mode = source.get("review_mode")
        extent = source.get("manifest_extent")
        if mode == "FULL_TEXT":
            observed_text += 1
            try:
                data.decode("utf-8", errors="strict")
            except UnicodeError:
                diagnostics.add("SOURCE_LINE_EXTENT_MISMATCH")
            if extent != {"encoding_check": "utf-8", "lines": len(data.splitlines())}:
                diagnostics.add("SOURCE_LINE_EXTENT_MISMATCH")
            observed_text_records.append({
                "source_id": source["source_id"], "path": path,
                "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
                "manifest_extent": extent,
                "observed_extent": {"encoding_check": "utf-8", "lines": len(data.splitlines())},
                "validation_status": "PASS_FULL_TEXT_EXTENT",
            })
            if source.get("extension") == "json":
                try:
                    _, stats = strict_load_bytes(data)
                    observed_json.append({
                        "source_id": source["source_id"], "path": path,
                        "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
                        "manifest_extent": extent, "traversal": stats,
                        "validation_status": "PASS_STRICT_DUPLICATE_NONFINITE_FULL_TRAVERSAL",
                    })
                except Exception:
                    diagnostics.add("JSON_STRICT_PARSE_TAMPER")
        elif mode == "FULL_PDF":
            try:
                reader = PdfReader(io.BytesIO(data), strict=True)
                actual_extent = {"encrypted": bool(reader.is_encrypted), "pages": len(reader.pages)}
            except Exception:
                diagnostics.add("PDF_EXTENT_TAMPER")
                actual_extent = {}
            if actual_extent != extent:
                diagnostics.add("PDF_EXTENT_TAMPER")
            observed_pdf.append({
                "source_id": source["source_id"], "path": path,
                "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
                "manifest_extent": extent, "observed_extent": actual_extent,
                "validation_status": "PASS_PDF_STRICT_METADATA_EXTENT",
            })
        elif mode == "FULL_IMAGE":
            try:
                with Image.open(io.BytesIO(data)) as image:
                    image.load()
                    actual_extent = {
                        "format": image.format, "frames": getattr(image, "n_frames", 1),
                        "height": image.height, "mode": image.mode, "width": image.width,
                    }
            except Exception:
                diagnostics.add("IMAGE_EXTENT_TAMPER")
                actual_extent = {}
            if actual_extent != extent:
                diagnostics.add("IMAGE_EXTENT_TAMPER")
            observed_image.append({
                "source_id": source["source_id"], "path": path,
                "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
                "manifest_extent": extent, "observed_extent": actual_extent,
                "validation_status": "PASS_IMAGE_PIXEL_METADATA_EXTENT",
            })
        else:
            diagnostics.add("SOURCE_LINE_EXTENT_MISMATCH")
    if dict(sorted(expected_class_counter.items())) != EXPECTED_SOURCE_CLASS_COUNTS:
        diagnostics.add("SOURCE_AUTHORITY_ROUTE_MISMATCH")
    if matrix.get("counts", {}).get("source_authority_classes") != EXPECTED_SOURCE_CLASS_COUNTS:
        diagnostics.add("SOURCE_AUTHORITY_ROUTE_MISMATCH")
    frozen = matrix.get("frozen_source_validation", {})
    expected_frozen_counts = {
        "full_text_extents_validated": observed_text,
        "strict_json_files_validated": len(observed_json),
        "strict_json_nodes_traversed": sum(row["traversal"]["nodes"] for row in observed_json),
        "pdf_extents_validated": len(observed_pdf),
        "pdf_pages_validated": sum(row["observed_extent"].get("pages", 0) for row in observed_pdf),
        "image_extents_validated": len(observed_image),
    }
    if observed_text != 195 or frozen.get("text_extent_records") != observed_text_records:
        diagnostics.add("SOURCE_LINE_EXTENT_MISMATCH")
    if len(observed_json) != 11 or frozen.get("strict_json_records") != observed_json:
        diagnostics.add("JSON_STRICT_PARSE_TAMPER")
    if len(observed_pdf) != 14 or expected_frozen_counts["pdf_pages_validated"] != 130 or frozen.get("pdf_extent_records") != observed_pdf:
        diagnostics.add("PDF_EXTENT_TAMPER")
    if len(observed_image) != 23 or frozen.get("image_extent_records") != observed_image:
        diagnostics.add("IMAGE_EXTENT_TAMPER")
    if frozen.get("counts") != expected_frozen_counts:
        mismatches = {
            "SOURCE_LINE_EXTENT_MISMATCH" if key == "full_text_extents_validated"
            else "JSON_STRICT_PARSE_TAMPER" if key.startswith("strict_json")
            else "PDF_EXTENT_TAMPER" if key.startswith("pdf_")
            else "IMAGE_EXTENT_TAMPER"
            for key, value in expected_frozen_counts.items() if frozen.get("counts", {}).get(key) != value
        }
        diagnostics.update(mismatches)

    snapshots: dict[str, dict[str, Any]] = {}
    projections: dict[str, dict[str, Any]] = {}
    for alias, path in SNAPSHOT_PATHS.items():
        snapshot, _ = strict_load_bytes(blobs[path])
        if not isinstance(snapshot, dict) or len(snapshot) not in {2, 3}:
            diagnostics.add("STRUCTURE_PROJECTION_TAMPER")
            continue
        try:
            for chapter in snapshot.values():
                if set(chapter) != {"labels", "eqblocks", "asset_unique", "bibitems"}:
                    raise ValidationError("SNAPSHOT_SCHEMA")
                if len(chapter["labels"]) != len(set(chapter["labels"])) or len(chapter["bibitems"]) != len(set(chapter["bibitems"])):
                    raise ValidationError("SNAPSHOT_DUPLICATE")
                if not isinstance(chapter["asset_unique"], int) or isinstance(chapter["asset_unique"], bool):
                    raise ValidationError("SNAPSHOT_ASSET")
                for block in chapter["eqblocks"].values():
                    if set(block) != {"hash", "boxed", "file"}:
                        raise ValidationError("SNAPSHOT_EQBLOCK")
            snapshots[alias] = snapshot
            projections[alias] = document_projection(snapshot)
        except Exception:
            diagnostics.add("STRUCTURE_PROJECTION_TAMPER")
    snapshot_inputs: dict[str, dict[str, Any]] = {}
    for alias, path in SNAPSHOT_PATHS.items():
        route = route_by_path[path]
        data = blobs[path]
        snapshot_inputs[alias] = {
            "source_id": route["source_id"], "path": path,
            "input_commit": BASELINE_COMMIT, "blob_sha1": route["blob_sha1"],
            "sha256": route["sha256"], "line_start": 1,
            "line_end": len(data.splitlines()),
            "slice_sha256_lf": sha256(line_slice(data, 1, len(data.splitlines()))),
            "evidence_status": "STRICT_PARSED_COMPLETE_SNAPSHOT_INPUT",
            "source_authority_class": route["source_authority_class"],
        }
    comparisons = {row.get("comparison_id"): row for row in matrix.get("snapshot_machine_comparisons", [])}
    if set(comparisons) != set(EXPECTED_COMPARISON_IDS) or len(comparisons) != 6:
        diagnostics.add("STRUCTURE_PROJECTION_TAMPER")
    else:
        cmp60 = comparisons["P061-SNAP-CMP-0060"]
        expected60 = (projection_with_sha(projections["baseline"]), projection_with_sha(projections["p0"]))
        if (cmp60.get("before"), cmp60.get("after")) != expected60 or cmp60.get("exact_equal") is not (projections["baseline"] == projections["p0"]):
            diagnostics.add("STRUCTURE_PROJECTION_TAMPER")
        pairs = {
            "P061-SNAP-CMP-0061-A": (projections["p0"]["ch1"], projections["p2"]["ch1"]),
            "P061-SNAP-CMP-0061-B": (projections["p7"]["ch1"], projections["p7b"]["ch1"]),
            "P061-SNAP-CMP-0062": (projections["p6"]["ch2"], projections["p7"]["ch2"]),
        }
        for comparison_id, (before, after) in pairs.items():
            row = comparisons[comparison_id]
            if row.get("before") != projection_with_sha(before) or row.get("after") != projection_with_sha(after):
                diagnostics.add("STRUCTURE_PROJECTION_TAMPER")
            if row.get("exact_diff") != eqblock_delta(before, after):
                diagnostics.add("UNLABELED_MOVE_AS_ADD_DELETE" if comparison_id.endswith("0062") else "STRUCTURE_DELTA_TAMPER")
        expected_0061 = {
            "P061-SNAP-CMP-0061-A": {
                "eq:sm-bare": {"hash": "89e15eaa3c66", "boxed": True, "file": "ch1_sec02a_part0.tex"},
                "eq:sm-baremid": {"hash": "ef6644a8eb30", "boxed": False, "file": "ch1_sec02a_part0.tex"},
                "eq:sm-baresum": {"hash": "bc43ee3bcfc6", "boxed": False, "file": "ch1_sec02a_part0.tex"},
            },
            "P061-SNAP-CMP-0061-B": {
                "eq:lco-mottcrit": {"hash": "1f15a2d56414", "boxed": False, "file": "ch1_sec15_lcoelec.tex"},
                "eq:sm-exch": {"hash": "8518ea77fc55", "boxed": False, "file": "ch1_sec02a_part0.tex"},
                "eq:sm-fdbe": {"hash": "7fe9ef50a5d9", "boxed": False, "file": "ch1_sec02a_part0.tex"},
            },
        }
        expected_0061_metadata = {
            "P061-SNAP-CMP-0061-A": (
                "P0_TO_P2_CH1_BARE_SITE_THREE_EQUATIONS", [snapshot_inputs["p0"], snapshot_inputs["p2"]],
            ),
            "P061-SNAP-CMP-0061-B": (
                "P7_TO_P7B_CH1_EXCHANGE_FDBE_MOTT_THREE_EQUATIONS", [snapshot_inputs["p7"], snapshot_inputs["p7b"]],
            ),
        }
        for comparison_id, expected in expected_0061.items():
            comparison = comparisons[comparison_id]
            actual_delta = comparison.get("exact_diff", {})
            actual = {
                row["identifier"]: {key: row[key] for key in ("hash", "boxed", "file")}
                for row in actual_delta.get("added", [])
            }
            expected_added = [{"identifier": key, **expected[key]} for key in sorted(expected)]
            expected_kind, expected_inputs = expected_0061_metadata[comparison_id]
            if (
                actual != expected or actual_delta.get("removed") != [] or actual_delta.get("changed") != []
                or comparison.get("expected_added") != expected_added
                or comparison.get("expected_added") != actual_delta.get("added")
                or comparison.get("inputs") != expected_inputs
                or comparison.get("claim_intent_ids") != ["INTENT-PROV-0061"]
                or comparison.get("comparison_kind") != expected_kind
                or comparison.get("asserted_result") != "EXACT_THREE_ADDED_NO_REMOVED_OR_CHANGED"
            ):
                diagnostics.add("STRUCTURE_DELTA_TAMPER")
            if comparison.get("authority_ceiling") != "STRUCTURE_LINEAGE_ONLY":
                diagnostics.add("SNAPSHOT_TO_PHYSICAL_VALIDITY")
            if comparison.get("external_scientific_truth") is not False:
                diagnostics.add("EXTERNAL_TRUTH_TRUE")
        expected_moves = {
            "ch2_sec00_intro.tex:44": "ch2_sec00_intro.tex:45",
            "ch2_sec08_synthesis.tex:49": "ch2_sec08_synthesis.tex:52",
            "ch2_sec08_synthesis.tex:78": "ch2_sec08_synthesis.tex:81",
            "ch2_sec08_synthesis.tex:96": "ch2_sec08_synthesis.tex:99",
        }
        delta62 = eqblock_delta(projections["p6"]["ch2"], projections["p7"]["ch2"])
        removed = {row["identifier"]: {k: row[k] for k in ("hash", "boxed", "file")} for row in delta62["removed"]}
        added = {row["identifier"]: {k: row[k] for k in ("hash", "boxed", "file")} for row in delta62["added"]}
        exact_moves = [{
            "before_identifier": old, "after_identifier": new,
            "before": removed.get(old), "after": added.get(new),
            "content_equal": removed.get(old) == added.get(new),
        } for old, new in sorted(expected_moves.items())]
        if comparisons["P061-SNAP-CMP-0062"].get("exact_moves") != exact_moves:
            diagnostics.add("UNLABELED_MOVE_AS_ADD_DELETE")
        cmp63 = comparisons["P061-SNAP-CMP-0063"]
        prefinal = ("p0", "p2", "p3", "p4", "p5", "p6", "p7", "p7b")
        pre_roots = {alias: sorted(snapshots[alias]) for alias in prefinal}
        final_roots = sorted(snapshots["final"])
        genealogy = {
            "prefinal_roots": pre_roots,
            "prefinal_appendix_occurrences": {
                alias: [root for root in roots_ if root == "appendix_phase_separation.tex"]
                for alias, roots_ in pre_roots.items()
            },
            "final_roots": final_roots,
            "final_appendix_occurrences": [root for root in final_roots if root == "appendix_phase_separation.tex"],
        }
        if not projection_hash_valid(cmp63.get("root_genealogy")):
            diagnostics.add("SNAPSHOT_0063_PROJECTION_TAMPER")
        stored_genealogy = cmp63.get("root_genealogy", {}).get("projection", {})
        prefinal_genealogy_mismatch = (
            stored_genealogy.get("prefinal_roots") != genealogy["prefinal_roots"]
            or stored_genealogy.get("prefinal_appendix_occurrences")
            != genealogy["prefinal_appendix_occurrences"]
        )
        if prefinal_genealogy_mismatch:
            diagnostics.add("SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH")
        if cmp63.get("prefinal_appendix_root_occurrences") != 0:
            diagnostics.add("PREFINAL_APPENDIX_FALSE_ABSENCE")
        final_genealogy_mismatch = (
            stored_genealogy.get("final_roots") != genealogy["final_roots"]
            or stored_genealogy.get("final_appendix_occurrences")
            != genealogy["final_appendix_occurrences"]
        )
        if final_genealogy_mismatch:
            diagnostics.add("SNAPSHOT_0063_FINAL_ROOT_MISMATCH")
        if (
            not prefinal_genealogy_mismatch and not final_genealogy_mismatch
            and cmp63.get("root_genealogy") != projection_with_sha(genealogy)
        ):
            diagnostics.add("SNAPSHOT_0063_PROJECTION_TAMPER")
        if cmp63.get("final_appendix_root_occurrences") != 1:
            diagnostics.add("SNAPSHOT_0063_FINAL_ROOT_MISMATCH")
        expected_0063_inputs = [snapshot_inputs[alias] for alias in (*prefinal, "final")]
        if (
            cmp63.get("inputs") != expected_0063_inputs
            or len({canonical_bytes(row) for row in cmp63.get("inputs", [])}) != 9
            or cmp63.get("prefinal_snapshot_aliases") != list(prefinal)
        ):
            diagnostics.add("SNAPSHOT_0063_INPUT_MISSING")
        if (
            cmp63.get("claim_intent_ids") != ["INTENT-PROV-0063"]
            or cmp63.get("comparison_kind")
            != "EXACT_EIGHT_PREFINAL_APPENDIX_ABSENCE_AND_FINAL_SINGLE_ROOT_PRESENCE"
            or cmp63.get("asserted_result")
            != "PREFINAL_GROUND_NOT_FOUND_FINAL_FIRST_OCCURRENCE_CONFIRMED"
            or cmp63.get("authority_ceiling") != "STRUCTURE_LINEAGE_ONLY"
            or cmp63.get("external_scientific_truth") is not False
        ):
            diagnostics.add("SNAPSHOT_0063_PROJECTION_TAMPER")
        baseline, final = projections["baseline"], projections["final"]
        ch1b, ch1a, ch2b, ch2a = baseline["ch1"], final["ch1"], baseline["ch2"], final["ch2"]
        delta65 = {
            "ch1": {
                "labels": set_delta(ch1b["labels"], ch1a["labels"]),
                "eqblock_count_before": len(ch1b["eqblocks"]), "eqblock_count_after": len(ch1a["eqblocks"]),
                "eqblock_count_delta": len(ch1a["eqblocks"]) - len(ch1b["eqblocks"]),
                "eqblock_exact_diff": eqblock_delta(ch1b, ch1a),
                "bibitems": set_delta(ch1b["bibitems"], ch1a["bibitems"]),
                "asset_unique_before": ch1b["asset_unique"], "asset_unique_after": ch1a["asset_unique"],
                "asset_unique_unchanged": ch1b["asset_unique"] == ch1a["asset_unique"],
            },
            "ch2": {
                "labels": set_delta(ch2b["labels"], ch2a["labels"]),
                "eqblock_count_before": len(ch2b["eqblocks"]), "eqblock_count_after": len(ch2a["eqblocks"]),
                "eqblock_count_delta": len(ch2a["eqblocks"]) - len(ch2b["eqblocks"]),
                "eqblock_exact_diff": eqblock_delta(ch2b, ch2a),
                "substantive_eqblocks_before": projection_with_sha(substantive_eqblocks(ch2b)),
                "substantive_eqblocks_after": projection_with_sha(substantive_eqblocks(ch2a)),
                "substantive_eqblocks_equal": substantive_eqblocks(ch2b) == substantive_eqblocks(ch2a),
                "bibitems": set_delta(ch2b["bibitems"], ch2a["bibitems"]),
                "asset_unique_before": ch2b["asset_unique"], "asset_unique_after": ch2a["asset_unique"],
                "asset_unique_unchanged": ch2b["asset_unique"] == ch2a["asset_unique"],
            },
        }
        cmp65 = comparisons["P061-SNAP-CMP-0065"]
        if cmp65.get("before") != projection_with_sha(baseline) or cmp65.get("after") != projection_with_sha(final):
            diagnostics.add("STRUCTURE_PROJECTION_TAMPER")
        if cmp65.get("exact_delta") != delta65:
            diagnostics.add("STRUCTURE_DELTA_TAMPER")

    p5, p6 = "730fc4087c7534aaa46433016ae98a1cc3d97c21", "8df0864d9522ec6fab29c52a473659f02ac195b6"
    if run_git("rev-parse", f"{p6}^") != p5:
        diagnostics.add("P5_P6_OCCURRENCE_COLLAPSE")
    changed = sorted(path for path in run_git("diff", "--name-only", p5, p6, "--", "Claude/docs/v1.0.20").splitlines() if path.endswith(".tex"))
    expected_changed = sorted((
        "Claude/docs/v1.0.20/_sections/ch1_appB_codemap.tex",
        "Claude/docs/v1.0.20/_sections/ch1_sec00_intro.tex",
        "Claude/docs/v1.0.20/appendix_phase_separation.tex",
    ))
    boundary56 = matrix.get("boundaries", {}).get("p5_p6", {})
    if changed != expected_changed or boundary56.get("changed_tex_paths") != expected_changed or boundary56.get("actual_source_tree_identical") is not False:
        diagnostics.add("P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY")
    if boundary56.get("snapshot_occurrences_distinct") is not True:
        diagnostics.add("P5_P6_OCCURRENCE_COLLAPSE")
    p5_data, p6_data = blobs[SNAPSHOT_PATHS["p5"]], blobs[SNAPSHOT_PATHS["p6"]]
    if (
        p5_data != p6_data
        or boundary56.get("snapshot_blob_identical") is not True
        or boundary56.get("snapshot_blob_sha1") != blob_sha1(p5_data)
        or boundary56.get("snapshot_sha256") != sha256(p5_data)
    ):
        diagnostics.add("P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY")
    for previous, current in zip(EXPECTED_P8_CHAIN, EXPECTED_P8_CHAIN[1:]):
        if run_git("rev-parse", f"{current}^") != previous:
            diagnostics.add("P8_COMMIT_CHAIN_MISMATCH")
    if not git_is_ancestor(EXPECTED_P8_CHAIN[-1], BASELINE_COMMIT) or matrix.get("boundaries", {}).get("p8", {}).get("complete_commit_chain") != list(EXPECTED_P8_CHAIN):
        diagnostics.add("P8_COMMIT_CHAIN_MISMATCH")
    evidence.update({
        "topology_traversal": topology_traversal, "sources": len(sources),
        "include_edges": len(include_edges), "text": observed_text, "json": len(observed_json),
        "pdf": len(observed_pdf), "pdf_pages": expected_frozen_counts["pdf_pages_validated"],
        "images": len(observed_image), "snapshots": len(snapshots), "comparisons": len(comparisons),
    })
    return diagnostics, evidence


def projection_hash_valid(record: Any) -> bool:
    return (
        isinstance(record, dict)
        and "projection" in record
        and record.get("projection_sha256") == sha256(canonical_bytes(record["projection"]))
    )


def evidence_records(matrix: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    baseline: list[dict[str, Any]] = []
    observation: list[dict[str, Any]] = []
    for claim in matrix.get("claims", []):
        if isinstance(claim.get("claimant"), dict):
            baseline.append(claim["claimant"])
        baseline.extend(item for item in claim.get("actual_evidence", []) if isinstance(item, dict))
        edge = claim.get("adoption_edge")
        if isinstance(edge, dict):
            baseline.extend(item for item in edge.get("targets", []) if isinstance(item, dict))
        if isinstance(claim.get("provisional_observation"), dict):
            observation.append(claim["provisional_observation"])
    for row in matrix.get("contradictions", []):
        baseline.extend(item for item in row.get("anchors", []) if isinstance(item, dict))
    for row in matrix.get("phase_table", []):
        for key in ("ledger_anchor", "plan_anchor"):
            if isinstance(row.get(key), dict):
                baseline.append(row[key])
    for row in matrix.get("snapshot_machine_comparisons", []):
        baseline.extend(item for item in row.get("inputs", []) if isinstance(item, dict))
    return baseline, observation


def provenance_diagnostics(matrix: dict[str, Any]) -> set[str]:
    wanted = lambda _code: True
    diagnostics: set[str] = set()
    routes = matrix.get("source_routes", [])
    route_by_path = {
        row.get("path"): row for row in routes if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    baseline_blobs: dict[str, bytes] = {}
    if any(wanted(code) for code in {
        "SOURCE_BLOB_MISMATCH", "SOURCE_LINE_EXTENT_MISMATCH", "PDF_EXTENT_TAMPER",
        "IMAGE_EXTENT_TAMPER", "JSON_STRICT_PARSE_TAMPER", "CLAIMANT_SLICE_HASH_MISMATCH",
        "CLAIM_EVIDENCE_SLICE_HASH_MISMATCH", "CONTRADICTION_ANCHOR_HASH_MISMATCH",
        "PHASE_TABLE_LEDGER_ANCHOR_MISMATCH", "P8_PLAN_ANCHOR_MISMATCH",
        "STRUCTURE_PROJECTION_TAMPER",
    }):
        try:
            baseline_blobs = git_blob_batch(BASELINE_COMMIT, route_by_path)
        except Exception:
            for code in (
                "SOURCE_BLOB_MISMATCH", "SOURCE_LINE_EXTENT_MISMATCH",
                "PDF_EXTENT_TAMPER", "IMAGE_EXTENT_TAMPER", "JSON_STRICT_PARSE_TAMPER",
            ):
                if wanted(code):
                    diagnostics.add(code)
            return diagnostics

    if wanted("SOURCE_BLOB_MISMATCH"):
        if any(
            path not in baseline_blobs
            or blob_sha1(baseline_blobs[path]) != row.get("blob_sha1")
            or sha256(baseline_blobs[path]) != row.get("sha256")
            for path, row in route_by_path.items()
        ):
            diagnostics.add("SOURCE_BLOB_MISMATCH")
    if wanted("SOURCE_LINE_EXTENT_MISMATCH"):
        text_routes = {
            row.get("path"): row for row in routes
            if row.get("review_mode") == "FULL_TEXT" and isinstance(row.get("path"), str)
        }
        if len(text_routes) != 195 or any(
            len(baseline_blobs.get(path, b"").splitlines())
            != row.get("manifest_extent", {}).get("lines")
            for path, row in text_routes.items()
        ):
            diagnostics.add("SOURCE_LINE_EXTENT_MISMATCH")

    frozen = matrix.get("frozen_source_validation", {})
    if wanted("PDF_EXTENT_TAMPER"):
        records = frozen.get("pdf_extent_records", [])
        expected_ids = {row.get("source_id") for row in routes if row.get("review_mode") == "FULL_PDF"}
        if (
            len(records) != 14
            or {row.get("source_id") for row in records} != expected_ids
            or any(row.get("manifest_extent") != row.get("observed_extent") for row in records)
            or sum(row.get("observed_extent", {}).get("pages", -1) for row in records) != 130
        ):
            diagnostics.add("PDF_EXTENT_TAMPER")
    if wanted("IMAGE_EXTENT_TAMPER"):
        records = frozen.get("image_extent_records", [])
        expected_ids = {row.get("source_id") for row in routes if row.get("review_mode") == "FULL_IMAGE"}
        if (
            len(records) != 23
            or {row.get("source_id") for row in records} != expected_ids
            or any(row.get("manifest_extent") != row.get("observed_extent") for row in records)
        ):
            diagnostics.add("IMAGE_EXTENT_TAMPER")
    if wanted("JSON_STRICT_PARSE_TAMPER"):
        records = frozen.get("strict_json_records", [])
        expected_paths = {
            row.get("path") for row in routes
            if row.get("review_mode") == "FULL_TEXT" and str(row.get("path", "")).endswith(".json")
        }
        valid = len(records) == 11 and {row.get("path") for row in records} == expected_paths
        if valid:
            try:
                for row in records:
                    value, stats = strict_load_bytes(baseline_blobs[row["path"]])
                    valid &= stats == row.get("traversal") and value is not None
            except Exception:
                valid = False
        if not valid:
            diagnostics.add("JSON_STRICT_PARSE_TAMPER")

    baseline_records, observation_records = evidence_records(matrix)

    def record_ok(record: dict[str, Any], blobs: dict[str, bytes]) -> tuple[bool, bool]:
        path = record.get("path")
        route = route_by_path.get(path)
        range_ok = (
            route is not None and record.get("source_id") == route.get("source_id")
            and record.get("input_commit") == BASELINE_COMMIT
            and record.get("blob_sha1") == route.get("blob_sha1")
            and record.get("sha256") == route.get("sha256")
            and isinstance(record.get("line_start"), int)
            and isinstance(record.get("line_end"), int)
            and isinstance(record.get("evidence_status"), str)
            and bool(record.get("evidence_status"))
        )
        if not range_ok or path not in blobs:
            return False, False
        try:
            sliced = line_slice(blobs[path], record["line_start"], record["line_end"])
        except Exception:
            return False, False
        return True, record.get("slice_sha256_lf") == sha256(sliced)

    claims = matrix.get("claims", [])
    if wanted("CLAIMANT_SLICE_HASH_MISMATCH"):
        candidates = [
            claim.get("claimant", {}) for claim in claims
            if isinstance(claim.get("claimant", {}).get("line_start"), int)
            and 1 <= claim["claimant"]["line_start"] <= claim["claimant"].get("line_end", 0)
        ]
        if any(not record_ok(record, baseline_blobs)[1] for record in candidates):
            diagnostics.add("CLAIMANT_SLICE_HASH_MISMATCH")
    if wanted("CLAIM_EVIDENCE_SLICE_HASH_MISMATCH"):
        actual = [
            item for claim in claims for item in claim.get("actual_evidence", [])
            if isinstance(item.get("line_start"), int)
            and 1 <= item["line_start"] <= item.get("line_end", 0)
            and isinstance(item.get("evidence_status"), str) and bool(item.get("evidence_status"))
        ]
        if any(not record_ok(item, baseline_blobs)[1] for item in actual):
            diagnostics.add("CLAIM_EVIDENCE_SLICE_HASH_MISMATCH")
    if wanted("CONTRADICTION_ANCHOR_HASH_MISMATCH"):
        anchors = [item for row in matrix.get("contradictions", []) for item in row.get("anchors", [])]
        if any(not record_ok(item, baseline_blobs)[1] for item in anchors):
            diagnostics.add("CONTRADICTION_ANCHOR_HASH_MISMATCH")
    if wanted("PHASE_TABLE_LEDGER_ANCHOR_MISMATCH"):
        anchors = [row.get("ledger_anchor", {}) for row in matrix.get("phase_table", [])]
        if any(not record_ok(item, baseline_blobs)[1] for item in anchors):
            diagnostics.add("PHASE_TABLE_LEDGER_ANCHOR_MISMATCH")
    if wanted("P8_PLAN_ANCHOR_MISMATCH"):
        phases = matrix.get("phase_table", [])
        p8 = next((row for row in phases if row.get("phase") == "P8"), {})
        anchor = p8.get("plan_anchor", {})
        if len(phases) == 9 and (
            (anchor.get("line_start"), anchor.get("line_end")) != (15, 25)
            or not record_ok(anchor, baseline_blobs)[1]
        ):
            diagnostics.add("P8_PLAN_ANCHOR_MISMATCH")

    if any(wanted(code) for code in {
        "TOPOLOGY_FROZEN_HASH_MISMATCH", "OBSERVATION_BLOB_MISMATCH",
        "OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH",
    }):
        obs_paths = [row.get("path") for row in matrix.get("observation_inputs", []) if isinstance(row.get("path"), str)]
        input_paths = [TOPOLOGY_PATH, *obs_paths]
        try:
            input_blobs = git_blob_batch(INPUT_COMMIT, input_paths)
        except Exception:
            input_blobs = {}
        if wanted("TOPOLOGY_FROZEN_HASH_MISMATCH"):
            topology = matrix.get("topology", {})
            data = input_blobs.get(TOPOLOGY_PATH, b"")
            if topology.get("sha256_lf_normalized") != TOPOLOGY_SHA256_LF or sha256(lf_bytes(data)) != TOPOLOGY_SHA256_LF:
                diagnostics.add("TOPOLOGY_FROZEN_HASH_MISMATCH")
        if wanted("OBSERVATION_BLOB_MISMATCH"):
            if len(obs_paths) != 5 or any(
                path not in input_blobs
                or row.get("input_commit") != INPUT_COMMIT
                or row.get("blob_sha1") != blob_sha1(input_blobs[path])
                or row.get("sha256_lf_normalized") != sha256(lf_bytes(input_blobs[path]))
                for row, path in zip(matrix.get("observation_inputs", []), obs_paths)
            ):
                diagnostics.add("OBSERVATION_BLOB_MISMATCH")
        if wanted("OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH"):
            valid = len(claims) != 40 or len(observation_records) == 40
            for record in observation_records:
                data = input_blobs.get(record.get("path"), b"")
                try:
                    sliced = line_slice(data, record.get("line_start"), record.get("line_end"))
                    valid &= (
                        record.get("input_commit") == INPUT_COMMIT
                        and record.get("blob_sha1") == blob_sha1(data)
                        and record.get("slice_sha256_lf") == sha256(sliced)
                    )
                except Exception:
                    valid = False
            if not valid:
                diagnostics.add("OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH")
    return diagnostics


def content_diagnostics(
    matrix: dict[str, Any], rebuilt: dict[str, Any] | None = None,
    verify_git: bool = True,
) -> set[str]:
    diagnostics: set[str] = set()

    def check(code: str, predicate: Callable[[], bool]) -> None:
        try:
            valid = bool(predicate())
        except Exception:
            valid = False
        if not valid:
            diagnostics.add(code)

    keys = set(matrix) if isinstance(matrix, dict) else set()
    check("MISSING_TOP_FIELD", lambda: not (EXPECTED_TOP_FIELDS - keys))
    check("EXTRA_TOP_FIELD", lambda: not (keys - EXPECTED_TOP_FIELDS))
    check("INPUT_COMMIT_MISMATCH", lambda: matrix.get("input_commit") == INPUT_COMMIT and matrix.get("baseline_commit") == BASELINE_COMMIT)
    check("GATE_NOT_PASS_WITH_CONCERNS", lambda: matrix.get("status") == matrix.get("gate") == "PASS_WITH_CONCERNS")

    routes = matrix.get("source_routes", [])
    expected_source_ids = [f"P061-SRC-{number:04d}" for number in range(1, 233)]
    route_ids = [row.get("source_id") for row in routes]
    route_paths = [row.get("path") for row in routes]
    check(
        "SOURCE_ROUTE_MISSING",
        lambda: not (set(expected_source_ids) - set(route_ids))
        and [row.get("manifest_index_v1020") for row in routes[:232]] == list(range(1, 233)),
    )
    check("SOURCE_ROUTE_DUPLICATE", lambda: len(routes) == len(set(route_ids)) == len(set(route_paths)) == 232)
    check(
        "SOURCE_AUTHORITY_CLASS_MULTIPLE",
        lambda: all(row.get("exact_one_class") is True and row.get("source_authority_class") in ALLOWED_AUTHORITY_CLASSES for row in routes),
    )
    check(
        "SOURCE_AUTHORITY_ROUTE_MISMATCH",
        lambda: all(
            "/DIRECTION_" in str(row.get("path", ""))
            or str(row.get("path", "")).endswith("/AUTHOR_BRIEF.md")
            or str(row.get("path", "")).endswith("/INTERCHAPTER_REPORT.md")
            or (
            isinstance(row.get("authority_ceiling"), str)
            and row.get("source_id", "") in row.get("evidence_route", "")
            and row.get("source_authority_class", "") in row.get("evidence_route", "")
            )
            for row in routes
        ),
    )
    adopted_routes = [row for row in routes if row.get("source_authority_class") == "ADOPTED_RELEASE_SOURCE"]
    check("ADOPTED_RELEASE_TOPOLOGY_MISSING", lambda: all(isinstance(row.get("adoption_topology"), dict) for row in adopted_routes))
    check(
        "ADOPTED_TEX_ORPHAN",
        lambda: all(
            not str(row.get("path", "")).endswith(".tex")
            or row.get("adoption_topology", {}).get("topology_type") in {"INCLUDED_RELEASE_SECTION", "DIRECT_RELEASE_ROOT"}
            for row in adopted_routes
        ),
    )
    direction = [row for row in routes if "/DIRECTION_" in str(row.get("path", ""))]
    check("DIRECTION_SOURCE_PROMOTED", lambda: bool(direction) and all(row.get("source_authority_class") == "EXTERNAL_SCIENTIFIC_UNVERIFIED" and not row.get("scientific_authority_promoted") for row in direction))
    briefs = [row for row in routes if str(row.get("path", "")).endswith("/AUTHOR_BRIEF.md")]
    check("AUTHOR_BRIEF_NOT_PLAN", lambda: len(briefs) == 2 and all(row.get("source_authority_class") == "PLAN_INTENT" for row in briefs))
    interchapter = [row for row in routes if str(row.get("path", "")).endswith("/INTERCHAPTER_REPORT.md")]
    check("INTERCHAPTER_NOT_REVIEW", lambda: len(interchapter) == 1 and interchapter[0].get("source_authority_class") == "INTERNAL_REVIEW")

    claims = matrix.get("claims", [])
    claim_semantic_mismatch = claim_semantic_contract_mismatch(claims)
    intent_ids = [row.get("intent_id") for row in claims]
    claim_ids = [row.get("claim_id") for row in claims]
    expected_intents = [f"INTENT-PROV-{number:04d}" for number in range(26, 66)]
    claim_identity_complete = len(claims) == 40 and set(intent_ids) == set(expected_intents)
    by_intent = {row.get("intent_id"): row for row in claims if isinstance(row, dict)}
    check("CLAIM_MISSING", lambda: not (set(expected_intents) - set(intent_ids)))
    check("CLAIM_DUPLICATE", lambda: len(claims) == len(set(intent_ids)) == len(set(claim_ids)) == 40)
    check(
        "CLAIMANT_RANGE_INVALID",
        lambda: all(
            isinstance(row.get("claimant"), dict)
            and isinstance(row["claimant"].get("line_start"), int)
            and 1 <= row["claimant"]["line_start"] <= row["claimant"].get("line_end", 0)
            for row in claims
        ),
    )
    check(
        "CLAIM_TYPE_NOT_SEMANTIC",
        lambda: not claim_identity_complete or all(
            int(row.get("intent_id", "-1").rsplit("-", 1)[-1]) in EXPECTED_CLAIM_TYPE_IDS.get(row.get("claim_type"), set())
            for row in claims
        ),
    )
    check(
        "CLAIM_AUTHORITY_CLASS_INVALID",
        lambda: not claim_identity_complete or (
            matrix.get("counts", {}).get("claim_authority_classes") == EXPECTED_CLAIM_CLASS_COUNTS
            and all(
                int(row.get("intent_id", "-1").rsplit("-", 1)[-1])
                in EXPECTED_CLAIM_CLASS_IDS.get(row.get("claim_authority_class"), set())
                for row in claims
            )
        ),
    )
    check("CLAIM_EVIDENCE_EMPTY", lambda: all(isinstance(row.get("actual_evidence"), list) and row["actual_evidence"] for row in claims))
    check(
        "CLAIM_EVIDENCE_ORPHAN",
        lambda: all(
            set(row.get("evidence_route_ids", []))
            == {item.get("source_id") for item in row.get("actual_evidence", [])}
            and set(row.get("evidence_route_ids", [])).issubset(set(route_ids))
            for row in claims
        ),
    )
    check(
        "SOURCE_ROUTE_ORPHAN",
        lambda: set(matrix.get("process_source_ids", [])).issubset(set(route_ids))
        and all(row.get("claimant", {}).get("source_id") in route_ids for row in claims),
    )
    check(
        "CLAIM_EVIDENCE_RANGE_OR_STATUS_INVALID",
        lambda: all(
            isinstance(item.get("line_start"), int)
            and 1 <= item["line_start"] <= item.get("line_end", 0)
            and isinstance(item.get("evidence_status"), str) and bool(item.get("evidence_status"))
            for row in claims for item in row.get("actual_evidence", [])
        ),
    )
    check(
        "CLAIM_EXPECTED_EVIDENCE_OR_GAP_MISSING",
        lambda: all(
            isinstance(row.get("expected_evidence", {}).get("semantic_standard"), str)
            and bool(row["expected_evidence"]["semantic_standard"])
            and isinstance(row.get("evidence_gap", {}).get("description"), str)
            and bool(row["evidence_gap"]["description"])
            for row in claims
        ),
    )
    policy = matrix.get("authority_policy", {})
    check("CIRCULAR_SELF_CERTIFICATION", lambda: policy.get("process_or_review_can_self_certify_science") is False)

    present = {row.get("intent_id") for row in claims if row.get("adoption_edge_state") == "PRESENT"}
    check("ADOPTION_EDGE_REQUIRED_MISSING", lambda: {"INTENT-PROV-0040", "INTENT-PROV-0061"}.issubset(present))
    check(
        "ADOPTION_EDGE_SELF_REFERENCE",
        lambda: all(
            row.get("adoption_edge", {}).get("edge_type") == "PROCESS_CLAIM_TO_ADOPTED_RELEASE_SOURCE"
            for row in claims if row.get("intent_id") in {"INTENT-PROV-0040", "INTENT-PROV-0050", "INTENT-PROV-0061"}
            and row.get("adoption_edge_state") == "PRESENT"
        ),
    )
    check(
        "ADOPTION_EDGE_PROCESS_TARGET",
        lambda: all(
            item.get("source_authority_class") == "ADOPTED_RELEASE_SOURCE"
            for row in claims if row.get("intent_id") in {"INTENT-PROV-0040", "INTENT-PROV-0050", "INTENT-PROV-0061"}
            and isinstance(row.get("adoption_edge"), dict)
            for item in row["adoption_edge"].get("targets", [])
        ),
    )
    check("CLAIM_0036_0037_INVALID_ADOPTION", lambda: all(by_intent.get(key, {}).get("adoption_edge") is None for key in ("INTENT-PROV-0036", "INTENT-PROV-0037")))
    check("CLAIM_0049_0057_FALSE_ADOPTION", lambda: all(by_intent.get(key, {}).get("adoption_edge_state") == "NOT_ADOPTED" for key in ("INTENT-PROV-0049", "INTENT-PROV-0057")))
    check("CLAIM_0050_ADOPTION_MISSING", lambda: by_intent.get("INTENT-PROV-0050", {}).get("adoption_edge_state") == "PRESENT")
    expected_0061_targets = {
        ("Claude/docs/v1.0.20/_sections/ch1_sec02a_part0.tex", 132, 195),
        ("Claude/docs/v1.0.20/_sections/ch1_sec15_lcoelec.tex", 39, 46),
    }
    check(
        "CLAIM_0061_ADOPTION_TARGET_MISMATCH",
        lambda: {
            (item.get("path"), item.get("line_start"), item.get("line_end"))
            for item in by_intent.get("INTENT-PROV-0061", {}).get("adoption_edge", {}).get("targets", [])
        } == expected_0061_targets,
    )
    check("PLAN_TO_SCIENCE_PROMOTION", lambda: all(not row.get("scientific_authority_promoted") for row in claims if row.get("claim_authority_class") == "PLAN_INTENT"))
    check("REVIEW_TO_PRIMARY_PROMOTION", lambda: all(not row.get("scientific_authority_promoted") for row in claims if row.get("claim_authority_class") == "INTERNAL_REVIEW"))
    check("SNAPSHOT_TO_PHYSICAL_VALIDITY", lambda: all(row.get("authority_ceiling") == "STRUCTURE_LINEAGE_ONLY" for row in matrix.get("snapshot_machine_comparisons", [])))
    check("TEST_PASS_TO_EXPERIMENT", lambda: not by_intent.get("INTENT-PROV-0045", {}).get("external_scientific_truth") and not by_intent.get("INTENT-PROV-0045", {}).get("scientific_authority_promoted"))
    check(
        "BIBLIOGRAPHY_PRESENCE_TO_PRIMARY_SUPPORT",
        lambda: any(row.get("queue_id") == "P061-UNV-001" and row.get("status") == "UNVERIFIED" for row in matrix.get("unverified_queue", [])),
    )

    comparisons = matrix.get("snapshot_machine_comparisons", [])
    comparison_ids = [row.get("comparison_id") for row in comparisons]
    by_comparison = {row.get("comparison_id"): row for row in comparisons}
    check("STRUCTURE_PROJECTION_TAMPER", lambda: comparison_ids == EXPECTED_COMPARISON_IDS and all(projection_hash_valid(row[key]) for row in comparisons for key in ("before", "after") if key in row))
    delta65 = by_comparison.get("P061-SNAP-CMP-0065", {}).get("exact_delta", {})
    check(
        "STRUCTURE_DELTA_TAMPER",
        lambda: (
            delta65.get("ch1", {}).get("labels", {}).get("count_delta"),
            delta65.get("ch1", {}).get("eqblock_count_delta"),
            delta65.get("ch1", {}).get("bibitems", {}).get("count_delta"),
            delta65.get("ch1", {}).get("asset_unique_before"),
            delta65.get("ch2", {}).get("labels", {}).get("count_delta"),
            delta65.get("ch2", {}).get("eqblock_count_delta"),
            delta65.get("ch2", {}).get("bibitems", {}).get("count_delta"),
            delta65.get("ch2", {}).get("asset_unique_before"),
            delta65.get("ch2", {}).get("substantive_eqblocks_equal"),
        ) == (6, 6, 8, 336, 0, 0, 2, 21, True),
    )
    boundaries = matrix.get("boundaries", {})
    check("P5_P6_OCCURRENCE_COLLAPSE", lambda: boundaries.get("p5_p6", {}).get("snapshot_occurrences_distinct") is True)
    check("P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY", lambda: boundaries.get("p5_p6", {}).get("snapshot_blob_identical") is True and boundaries.get("p5_p6", {}).get("actual_source_tree_identical") is False)
    moves = by_comparison.get("P061-SNAP-CMP-0062", {}).get("exact_moves", [])
    check("UNLABELED_MOVE_AS_ADD_DELETE", lambda: len(moves) == 4 and all(row.get("content_equal") is True for row in moves))
    claim63 = by_intent.get("INTENT-PROV-0063", {})
    check("APPENDIX_PREFINAL_HISTORY_FALSE", lambda: claim63.get("components", {}).get("prefinal_genealogy", {}).get("status") == "GROUND_NOT_FOUND")
    comparison63 = by_comparison.get("P061-SNAP-CMP-0063", {})
    check("PREFINAL_APPENDIX_FALSE_ABSENCE", lambda: comparison63.get("prefinal_appendix_root_occurrences") == 0)
    check("SNAPSHOT_0063_INPUT_MISSING", lambda: len(comparison63.get("inputs", [])) == 9 and comparison63.get("prefinal_snapshot_aliases") == ["p0", "p2", "p3", "p4", "p5", "p6", "p7", "p7b"])
    genealogy = comparison63.get("root_genealogy", {}).get("projection", {})
    check("SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH", lambda: all(not values for values in genealogy.get("prefinal_appendix_occurrences", {}).values()) and len(genealogy.get("prefinal_roots", {})) == 8)
    check("SNAPSHOT_0063_FINAL_ROOT_MISMATCH", lambda: genealogy.get("final_appendix_occurrences") == ["appendix_phase_separation.tex"] and comparison63.get("final_appendix_root_occurrences") == 1)
    check("SNAPSHOT_0063_PROJECTION_TAMPER", lambda: projection_hash_valid(comparison63.get("root_genealogy")))

    phases = matrix.get("phase_table", [])
    by_phase = {row.get("phase"): row for row in phases}
    p8 = by_phase.get("P8", {})
    check("P8_DEDICATED_RESULT_FALSE_PRESENT", lambda: len(phases) != 9 or (p8.get("result") is None and p8.get("dedicated_result_path_state") == "GROUND_NOT_FOUND"))
    check("P8_DEDICATED_LOG_FALSE_PRESENT", lambda: len(phases) != 9 or (p8.get("step_log") is None and p8.get("dedicated_step_log_path_state") == "GROUND_NOT_FOUND"))
    check("P8_TOTAL_EVIDENCE_FALSE_GNF", lambda: len(phases) != 9 or (isinstance(p8.get("substitute_result"), dict) and boundaries.get("p8", {}).get("completion_evidence_state") == "CONFIRMED_INTERNAL_WITH_HANDOVER_LEDGER_GIT"))
    check("P8_INTERNAL_PASS_TO_SCIENCE", lambda: len(phases) != 9 or (p8.get("external_scientific_truth") is False and p8.get("completion_authority_ceiling") == "INTERNAL_PROCESS_ONLY"))
    check("STATUS_CONFIRMED_WITH_GNF_EVIDENCE", lambda: claim63.get("status") == "CONFIRMED_WITH_GROUND_NOT_FOUND_SUBCLAIM" and claim63.get("components", {}).get("final_first_occurrence", {}).get("status") == "CONFIRMED")

    contradictions = matrix.get("contradictions", [])
    contradiction_ids = [row.get("contradiction_id") for row in contradictions]
    expected_contradictions = [f"P061-CON-{number:03d}" for number in range(1, 11)]
    check("CONTRADICTION_ROW_MISSING", lambda: contradiction_ids == expected_contradictions)
    check(
        "CONTRADICTED_WITH_NULL_CONTRADICTION",
        lambda: all(
            (bool(row.get("contradiction_ids")) and isinstance(row.get("contradiction"), dict))
            or (not row.get("contradiction_ids") and row.get("contradiction") is None)
            for row in claims
        ),
    )
    check("CONTRADICTION_ATTACHMENT_ORPHAN", lambda: {item for row in claims for item in row.get("contradiction_ids", [])} == set(expected_contradictions))

    check("PHASE_TABLE_ROW_MISSING", lambda: [row.get("phase") for row in phases] == [f"P{number}" for number in range(9)])
    phase_details = (
        ("1-10", "1-10", "PLAN_P0_setup.md", "RESULT_P0_setup.md", "STEP_LOG_P0.md", "PASS_P0_SETUP", "ALIGNED"),
        ("11-22", "11-22", "PLAN_P1_references.md", "RESULT_P1_references.md", "STEP_LOG_P1.md", "PASS_P1_REFERENCE_LEDGER", "PLAN_CHANGED_BIB_EDIT"),
        ("23-32", "23-32", "PLAN_P2_part0.md", "RESULT_P2_part0.md", "STEP_LOG_P2.md", "PASS_P2_PART0", "ALIGNED"),
        ("33-44", "33-44 (Step 39 rejected)", "PLAN_P3_graphite.md", "RESULT_P3_graphite.md", "STEP_LOG_P3.md", "PASS_P3_GRAPHITE", "KWW_STEP_REJECTED"),
        ("45-62", "45-62 (competition repeated)", "PLAN_P4_lco.md", "RESULT_P4_lco.md", "STEP_LOG_P4.md", "PASS_P4_LCO", "SCOPE_NARROWED_AFTER_FULL_READ"),
        ("63-72", "63-72 (environment rebuilt once)", "PLAN_P5_ch2.md", "RESULT_P5_ch2.md", "STEP_LOG_P5.md", "PASS_P5_CH2", "ALIGNED_DISTINCT_P5_SNAPSHOT_OCCURRENCE"),
        ("73-80", "73-80", "PLAN_P6_convention.md", "RESULT_P6_convention.md", "STEP_LOG_P6.md", "PASS_P6_CONVENTION", "PARTLY_SUPERSEDED_BY_P7_USER_DIRECTIVE"),
        ("81-90", "81-90 (two interruptions and restarts)", "PLAN_P7_review.md", "RESULT_P7_review.md", "STEP_LOG_P7.md", "PASS_P7_REVIEW", "REVIEW_COUNT_DRIFT_4_10_11"),
        ("91-98", "91-98 (one cap interruption and restart)", "PLAN_P8_closing.md", None, None, "PASS_P8_CLOSING", "DEDICATED_RESULT_AND_LOG_GROUND_NOT_FOUND_HANDOVER_SUBSTITUTE"),
    )
    def phase_details_valid() -> bool:
        if len(phases) != 9:
            return True
        for number, (planned, actual, plan_name, result_name, log_name, gate, relation) in enumerate(phase_details):
            row = phases[number]
            plan_path = f"Claude/docs/v1.0.20/plans/{plan_name}"
            result_path = None if result_name is None else f"Claude/docs/v1.0.20/results/{result_name}"
            log_path = None if log_name is None else f"Claude/docs/v1.0.20/results/{log_name}"
            plan_route = next((route for route in routes if route.get("path") == plan_path), None)
            result_route = next((route for route in routes if route.get("path") == result_path), None)
            log_route = next((route for route in routes if route.get("path") == log_path), None)
            expected_plan = None if plan_route is None else {"path": plan_path, "source_id": plan_route.get("source_id")}
            expected_result = None if result_path is None else ({"path": result_path, "source_id": result_route.get("source_id")} if result_route else None)
            expected_log = None if log_path is None else ({"path": log_path, "source_id": log_route.get("source_id")} if log_route else None)
            if (
                row.get("phase") != f"P{number}" or row.get("planned_steps") != planned
                or row.get("actual_steps") != actual or row.get("gate") != gate
                or row.get("plan") != expected_plan or row.get("result") != expected_result
                or row.get("step_log") != expected_log or row.get("relation") != relation
                or row.get("process_status") != "PROCESS_REPORTED_PASS_WITH_CONCERNS"
                or row.get("completion_authority_ceiling") != "INTERNAL_PROCESS_ONLY"
                or (number != 8 and row.get("external_scientific_truth") is not False)
            ):
                return False
        return True
    check("PHASE_TABLE_GATE_OR_STEP_MISMATCH", phase_details_valid)
    expected_chain = [
        "66e3510d67162dd6bd88158557f96621cbedbbcf",
        "c8853c83d79f22059e07c2a548759da6e8310d2d",
        "eb2cd1a32471a40de5511ed159aedf8272792a8a",
        "a0ae6b41e80983940e13851467a07b47e76531f6",
        "1e6c610f11682d87a416957b1cf65b4c8df53697",
        "ba41c9052e9b177268ef65e115dda500d0af3856",
        "c70bcb6f4e2ca0eba6f1b9cfbb0cff7c2f88d862",
    ]
    check("P8_COMMIT_CHAIN_MISMATCH", lambda: boundaries.get("p8", {}).get("complete_commit_chain") == expected_chain and boundaries.get("p8", {}).get("complete_commit_chain_parent_verified") is True)

    user_claims = [row for row in claims if row.get("claim_authority_class") == "USER_REQUIREMENT"]
    check(
        "USER_TRANSCRIPT_FALSE_PRESENT",
        lambda: len(user_claims) == 8
        and policy.get("original_independent_user_transcript_available") is False
        and policy.get("recorded_requirement_promoted_to_first_order_user_transcript") is False
        and all(row.get("evidence_gap", {}).get("original_independent_user_transcript") == "GROUND_NOT_FOUND_IN_FROZEN_232_SOURCE_CORPUS" for row in user_claims),
    )
    queue = matrix.get("unverified_queue", [])
    check("UNVERIFIED_QUEUE_MISSING", lambda: [row.get("queue_id") for row in queue] == [f"P061-UNV-{number:03d}" for number in range(1, 12)])
    ground = matrix.get("ground_not_found", [])
    check(
        "TARGET_MISSING",
        lambda: all(isinstance(row.get("target_phase"), int) for row in [*claims, *queue, *ground]),
    )
    check(
        "EXTERNAL_TRUTH_TRUE",
        lambda: matrix.get("counts", {}).get("external_truth_true") == 0
        and matrix.get("counts", {}).get("scientific_promotions_true") == 0
        and all(not row.get("external_scientific_truth") and not row.get("scientific_authority_promoted") for row in routes)
        and all(
            not row.get("external_scientific_truth")
            for row in claims if row.get("intent_id") != "INTENT-PROV-0045"
        )
        and all(
            not row.get("scientific_authority_promoted")
            for row in claims
            if row.get("claim_authority_class") not in {"PLAN_INTENT", "INTERNAL_REVIEW"}
            and row.get("intent_id") != "INTENT-PROV-0045"
        )
        and all(not row.get("external_scientific_truth") for row in comparisons)
        and matrix.get("frozen_source_validation", {}).get("visual_truth_promoted") is False,
    )
    check(
        "DETERMINISM_MISMATCH",
        lambda: rebuilt is None or canonical_bytes(matrix) == canonical_bytes(rebuilt),
    )

    counts = matrix.get("counts", {})
    independent_counts_ok = (
        counts.get("source_routes") == 232 and counts.get("claims") == 40
        and counts.get("contradictions") == 10 and counts.get("phase_rows") == 9
        and counts.get("snapshot_machine_comparisons") == 6
        and counts.get("ground_not_found") == 7 and counts.get("unverified_queue") == 11
        and counts.get("adoption_edges_present") == 3
    )
    if not independent_counts_ok:
        diagnostics.add("CONTENT_COUNT_CONTRACT")
    if matrix.get("required_negative_controls") != list(EXPECTED_NEGATIVES):
        diagnostics.add("NEGATIVE_CONTROL_IDENTITY")
    if matrix.get("authority_classes") != [
        "USER_REQUIREMENT", "PLAN_INTENT", "PROCESS_SELF_ASSESSMENT", "INTERNAL_REVIEW",
        "COMPETING_DRAFT", "ADOPTED_RELEASE_SOURCE", "STRUCTURAL_WITNESS",
        "EXTERNAL_SCIENTIFIC_UNVERIFIED",
    ]:
        diagnostics.add("AUTHORITY_CLASS_ORDER")
    frozen_counts = matrix.get("frozen_source_validation", {}).get("counts", {})
    if (
        frozen_counts.get("full_text_extents_validated"),
        frozen_counts.get("strict_json_files_validated"),
        frozen_counts.get("pdf_extents_validated"),
        frozen_counts.get("pdf_pages_validated"),
        frozen_counts.get("image_extents_validated"),
    ) != (195, 11, 14, 130, 23):
        diagnostics.add("FROZEN_SOURCE_VALIDATION_COUNTS")

    if verify_git:
        diagnostics |= provenance_diagnostics(matrix)
    claim_legacy_diagnostics = {
        "CLAIM_MISSING", "CLAIM_DUPLICATE", "CLAIMANT_RANGE_INVALID",
        "OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH",
        "CLAIMANT_SLICE_HASH_MISMATCH", "CLAIM_TYPE_NOT_SEMANTIC",
        "CLAIM_AUTHORITY_CLASS_INVALID", "CLAIM_EVIDENCE_EMPTY", "CLAIM_EVIDENCE_ORPHAN",
        "CLAIM_EVIDENCE_RANGE_OR_STATUS_INVALID", "CLAIM_EVIDENCE_SLICE_HASH_MISMATCH",
        "CLAIM_EXPECTED_EVIDENCE_OR_GAP_MISSING", "ADOPTION_EDGE_REQUIRED_MISSING",
        "ADOPTION_EDGE_SELF_REFERENCE", "ADOPTION_EDGE_PROCESS_TARGET",
        "CLAIM_0036_0037_INVALID_ADOPTION", "CLAIM_0049_0057_FALSE_ADOPTION",
        "CLAIM_0050_ADOPTION_MISSING", "CLAIM_0061_ADOPTION_TARGET_MISMATCH",
        "PLAN_TO_SCIENCE_PROMOTION", "REVIEW_TO_PRIMARY_PROMOTION", "TEST_PASS_TO_EXPERIMENT",
        "APPENDIX_PREFINAL_HISTORY_FALSE", "STATUS_CONFIRMED_WITH_GNF_EVIDENCE",
        "CONTRADICTED_WITH_NULL_CONTRADICTION", "CONTRADICTION_ATTACHMENT_ORPHAN",
        "TARGET_MISSING",
    }
    if claim_semantic_mismatch and not diagnostics.intersection(claim_legacy_diagnostics):
        diagnostics.add("CLAIM_SEMANTIC_CONTRACT")
    return diagnostics


def mutate_for_control(control: str, matrix: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(matrix)
    routes = mutated["source_routes"]
    claims = mutated["claims"]
    by_intent = {row["intent_id"]: row for row in claims}
    comparisons = {row["comparison_id"]: row for row in mutated["snapshot_machine_comparisons"]}
    phases = {row["phase"]: row for row in mutated["phase_table"]}

    if control == "INPUT_COMMIT_MISMATCH":
        mutated["input_commit"] = "0" * 40
    elif control == "TOPOLOGY_FROZEN_HASH_MISMATCH":
        mutated["topology"]["sha256_lf_normalized"] = "0" * 64
    elif control == "OBSERVATION_BLOB_MISMATCH":
        mutated["observation_inputs"][0]["blob_sha1"] = "0" * 40
    elif control == "OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH":
        claims[0]["provisional_observation"]["slice_sha256_lf"] = "0" * 64
    elif control == "MISSING_TOP_FIELD":
        mutated.pop("artifact_kind")
    elif control == "EXTRA_TOP_FIELD":
        mutated["unexpected"] = True
    elif control == "SOURCE_ROUTE_MISSING":
        routes[-1]["manifest_index_v1020"] = 999
    elif control == "SOURCE_ROUTE_DUPLICATE":
        routes.append(copy.deepcopy(routes[-1]))
    elif control == "SOURCE_ROUTE_ORPHAN":
        mutated["process_source_ids"].append("P061-SRC-9999")
    elif control == "SOURCE_BLOB_MISMATCH":
        routes[0]["sha256"] = "0" * 64
    elif control == "SOURCE_LINE_EXTENT_MISMATCH":
        next(row for row in routes if row["review_mode"] == "FULL_TEXT")["manifest_extent"]["lines"] += 1
    elif control == "PDF_EXTENT_TAMPER":
        mutated["frozen_source_validation"]["pdf_extent_records"][0]["observed_extent"]["pages"] += 1
    elif control == "IMAGE_EXTENT_TAMPER":
        mutated["frozen_source_validation"]["image_extent_records"][0]["observed_extent"]["width"] += 1
    elif control == "JSON_STRICT_PARSE_TAMPER":
        mutated["frozen_source_validation"]["strict_json_records"].pop()
    elif control == "SOURCE_AUTHORITY_CLASS_MULTIPLE":
        routes[0]["exact_one_class"] = False
    elif control == "SOURCE_AUTHORITY_ROUTE_MISMATCH":
        routes[0]["source_authority_class"] = "STRUCTURAL_WITNESS"
    elif control == "ADOPTED_RELEASE_TOPOLOGY_MISSING":
        next(row for row in routes if row["source_authority_class"] == "ADOPTED_RELEASE_SOURCE")["adoption_topology"] = None
    elif control == "ADOPTED_TEX_ORPHAN":
        row = next(row for row in routes if row["source_authority_class"] == "ADOPTED_RELEASE_SOURCE" and row["path"].endswith(".tex"))
        row["adoption_topology"]["topology_type"] = "PACKAGE_COMPANION_ROOT"
    elif control == "DIRECTION_SOURCE_PROMOTED":
        row = next(row for row in routes if "/DIRECTION_" in row["path"])
        row["source_authority_class"] = "ADOPTED_RELEASE_SOURCE"
        row["authority_ceiling"] = "RELEASE_CONTENT_ONLY"
        row["evidence_route"] = f"{row['source_id']} -> frozen Git blob {row['blob_sha1']} -> ADOPTED_RELEASE_SOURCE ceiling"
        row["adoption_topology"] = {"topology_type": "PACKAGE_COMPANION_ROOT"}
    elif control == "AUTHOR_BRIEF_NOT_PLAN":
        next(row for row in routes if row["path"].endswith("/AUTHOR_BRIEF.md"))["source_authority_class"] = "INTERNAL_REVIEW"
    elif control == "INTERCHAPTER_NOT_REVIEW":
        next(row for row in routes if row["path"].endswith("/INTERCHAPTER_REPORT.md"))["source_authority_class"] = "PLAN_INTENT"
    elif control == "CLAIM_MISSING":
        claims[-1]["intent_id"] = "INTENT-PROV-MISSING"
    elif control == "CLAIM_DUPLICATE":
        claims.append(copy.deepcopy(claims[-1]))
    elif control == "CLAIMANT_RANGE_INVALID":
        claims[0]["claimant"]["line_start"] = 0
    elif control == "CLAIMANT_SLICE_HASH_MISMATCH":
        claims[0]["claimant"]["slice_sha256_lf"] = "0" * 64
    elif control == "CLAIM_TYPE_NOT_SEMANTIC":
        claims[0]["claim_type"] = "authority"
    elif control == "CLAIM_AUTHORITY_CLASS_INVALID":
        next(row for row in claims if row["claim_authority_class"] == "STRUCTURAL_WITNESS")["claim_authority_class"] = "INVALID"
    elif control == "CLAIM_EVIDENCE_EMPTY":
        claims[0]["actual_evidence"] = []
        claims[0]["evidence_route_ids"] = []
    elif control == "CLAIM_EVIDENCE_ORPHAN":
        claims[0]["evidence_route_ids"].append("P061-SRC-9999")
    elif control == "CLAIM_EVIDENCE_RANGE_OR_STATUS_INVALID":
        claims[0]["actual_evidence"][0]["line_start"] = 0
    elif control == "CLAIM_EVIDENCE_SLICE_HASH_MISMATCH":
        claims[0]["actual_evidence"][0]["slice_sha256_lf"] = "0" * 64
    elif control == "CLAIM_EXPECTED_EVIDENCE_OR_GAP_MISSING":
        claims[0]["expected_evidence"]["semantic_standard"] = ""
    elif control == "CIRCULAR_SELF_CERTIFICATION":
        mutated["authority_policy"]["process_or_review_can_self_certify_science"] = True
    elif control == "ADOPTION_EDGE_REQUIRED_MISSING":
        by_intent["INTENT-PROV-0040"]["adoption_edge_state"] = "NOT_APPLICABLE"
    elif control == "ADOPTION_EDGE_SELF_REFERENCE":
        by_intent["INTENT-PROV-0040"]["adoption_edge"]["edge_type"] = "CLAIM_SELF_REFERENCE"
    elif control == "ADOPTION_EDGE_PROCESS_TARGET":
        by_intent["INTENT-PROV-0040"]["adoption_edge"]["targets"][0]["source_authority_class"] = "INTERNAL_REVIEW"
    elif control == "CLAIM_0036_0037_INVALID_ADOPTION":
        by_intent["INTENT-PROV-0036"]["adoption_edge"] = {"targets": []}
    elif control == "CLAIM_0049_0057_FALSE_ADOPTION":
        by_intent["INTENT-PROV-0049"]["adoption_edge_state"] = "PRESENT"
    elif control == "CLAIM_0050_ADOPTION_MISSING":
        by_intent["INTENT-PROV-0050"]["adoption_edge_state"] = "NOT_APPLICABLE"
    elif control == "CLAIM_0061_ADOPTION_TARGET_MISMATCH":
        by_intent["INTENT-PROV-0061"]["adoption_edge"]["targets"].pop()
    elif control == "PLAN_TO_SCIENCE_PROMOTION":
        next(row for row in claims if row["claim_authority_class"] == "PLAN_INTENT")["scientific_authority_promoted"] = True
    elif control == "REVIEW_TO_PRIMARY_PROMOTION":
        next(row for row in claims if row["claim_authority_class"] == "INTERNAL_REVIEW")["scientific_authority_promoted"] = True
    elif control == "SNAPSHOT_TO_PHYSICAL_VALIDITY":
        mutated["snapshot_machine_comparisons"][0]["authority_ceiling"] = "PHYSICAL_VALIDITY"
    elif control == "STRUCTURE_PROJECTION_TAMPER":
        comparisons["P061-SNAP-CMP-0060"]["before"]["projection_sha256"] = "0" * 64
    elif control == "STRUCTURE_DELTA_TAMPER":
        comparisons["P061-SNAP-CMP-0065"]["exact_delta"]["ch1"]["labels"]["count_delta"] = 7
    elif control == "TEST_PASS_TO_EXPERIMENT":
        by_intent["INTENT-PROV-0045"]["external_scientific_truth"] = True
    elif control == "BIBLIOGRAPHY_PRESENCE_TO_PRIMARY_SUPPORT":
        mutated["unverified_queue"][0]["status"] = "VERIFIED_FROM_BIBLIOGRAPHY_PRESENCE"
    elif control == "P5_P6_OCCURRENCE_COLLAPSE":
        mutated["boundaries"]["p5_p6"]["snapshot_occurrences_distinct"] = False
    elif control == "P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY":
        mutated["boundaries"]["p5_p6"]["actual_source_tree_identical"] = True
    elif control == "UNLABELED_MOVE_AS_ADD_DELETE":
        comparisons["P061-SNAP-CMP-0062"]["exact_moves"][0]["content_equal"] = False
    elif control == "APPENDIX_PREFINAL_HISTORY_FALSE":
        by_intent["INTENT-PROV-0063"]["components"]["prefinal_genealogy"]["status"] = "CONFIRMED"
    elif control == "PREFINAL_APPENDIX_FALSE_ABSENCE":
        comparisons["P061-SNAP-CMP-0063"]["prefinal_appendix_root_occurrences"] = 1
    elif control == "SNAPSHOT_0063_INPUT_MISSING":
        comparisons["P061-SNAP-CMP-0063"]["inputs"].pop()
    elif control == "SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH":
        comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection"]["prefinal_appendix_occurrences"]["p3"] = ["appendix_phase_separation.tex"]
        comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection_sha256"] = sha256(canonical_bytes(comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection"]))
    elif control == "SNAPSHOT_0063_FINAL_ROOT_MISMATCH":
        comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection"]["final_appendix_occurrences"] = []
        comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection_sha256"] = sha256(canonical_bytes(comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection"]))
    elif control == "SNAPSHOT_0063_PROJECTION_TAMPER":
        comparisons["P061-SNAP-CMP-0063"]["root_genealogy"]["projection_sha256"] = "0" * 64
    elif control == "P8_DEDICATED_RESULT_FALSE_PRESENT":
        phases["P8"]["dedicated_result_path_state"] = "PRESENT"
    elif control == "P8_DEDICATED_LOG_FALSE_PRESENT":
        phases["P8"]["dedicated_step_log_path_state"] = "PRESENT"
    elif control == "P8_TOTAL_EVIDENCE_FALSE_GNF":
        phases["P8"]["substitute_result"] = None
    elif control == "P8_INTERNAL_PASS_TO_SCIENCE":
        phases["P8"]["external_scientific_truth"] = True
    elif control == "STATUS_CONFIRMED_WITH_GNF_EVIDENCE":
        by_intent["INTENT-PROV-0063"]["status"] = "CONFIRMED"
    elif control == "CONTRADICTED_WITH_NULL_CONTRADICTION":
        next(row for row in claims if row["contradiction_ids"])["contradiction"] = None
    elif control == "CONTRADICTION_ROW_MISSING":
        mutated["contradictions"].pop()
    elif control == "CONTRADICTION_ANCHOR_HASH_MISMATCH":
        mutated["contradictions"][0]["anchors"][0]["slice_sha256_lf"] = "0" * 64
    elif control == "CONTRADICTION_ATTACHMENT_ORPHAN":
        claims[0]["contradiction_ids"] = ["P061-CON-999"]
        claims[0]["contradiction"] = {"contradiction_ids": ["P061-CON-999"]}
    elif control == "PHASE_TABLE_ROW_MISSING":
        mutated["phase_table"].pop()
    elif control == "PHASE_TABLE_LEDGER_ANCHOR_MISMATCH":
        mutated["phase_table"][0]["ledger_anchor"]["slice_sha256_lf"] = "0" * 64
    elif control == "PHASE_TABLE_GATE_OR_STEP_MISMATCH":
        phases["P0"]["gate"] = "MUTATED"
    elif control == "P8_COMMIT_CHAIN_MISMATCH":
        mutated["boundaries"]["p8"]["complete_commit_chain"].pop()
    elif control == "USER_TRANSCRIPT_FALSE_PRESENT":
        mutated["authority_policy"]["original_independent_user_transcript_available"] = True
    elif control == "P8_PLAN_ANCHOR_MISMATCH":
        phases["P8"]["plan_anchor"]["line_start"] = 14
    elif control == "UNVERIFIED_QUEUE_MISSING":
        mutated["unverified_queue"].pop()
    elif control == "EXTERNAL_TRUTH_TRUE":
        routes[0]["external_scientific_truth"] = True
    elif control == "GATE_NOT_PASS_WITH_CONCERNS":
        mutated["gate"] = "PASS"
    elif control == "TARGET_MISSING":
        claims[0]["target_phase"] = None
    elif control == "DETERMINISM_MISMATCH":
        mutated["generated_date"] = "2099-01-01"
    else:
        raise ValidationError(f"NEGATIVE_MUTATION_UNIMPLEMENTED:{control}")
    return mutated


def run_negative_controls(matrix: dict[str, Any]) -> dict[str, Any]:
    if matrix.get("required_negative_controls") != list(EXPECTED_NEGATIVES):
        raise ValidationError("NEGATIVE_CONTROL_IDENTITY")
    clean = content_diagnostics(matrix, verify_git=True)
    independent_clean, _ = independent_frozen_diagnostics(matrix)
    if clean or independent_clean:
        raise ValidationError(
            "NEGATIVE_BASELINE_NOT_CLEAN:"
            + ",".join(sorted(clean | independent_clean))
        )
    cases: list[dict[str, Any]] = []
    independent_controls = {
        "SOURCE_ROUTE_MISSING", "SOURCE_ROUTE_DUPLICATE", "SOURCE_BLOB_MISMATCH",
        "SOURCE_LINE_EXTENT_MISMATCH", "PDF_EXTENT_TAMPER", "IMAGE_EXTENT_TAMPER",
        "JSON_STRICT_PARSE_TAMPER", "SOURCE_AUTHORITY_ROUTE_MISMATCH",
        "ADOPTED_RELEASE_TOPOLOGY_MISSING", "ADOPTED_TEX_ORPHAN",
        "DIRECTION_SOURCE_PROMOTED", "AUTHOR_BRIEF_NOT_PLAN", "INTERCHAPTER_NOT_REVIEW",
        "STRUCTURE_PROJECTION_TAMPER", "STRUCTURE_DELTA_TAMPER",
        "P5_P6_OCCURRENCE_COLLAPSE", "P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY",
        "UNLABELED_MOVE_AS_ADD_DELETE", "PREFINAL_APPENDIX_FALSE_ABSENCE",
        "SNAPSHOT_0063_INPUT_MISSING", "SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH",
        "SNAPSHOT_0063_FINAL_ROOT_MISMATCH", "SNAPSHOT_0063_PROJECTION_TAMPER",
        "P8_COMMIT_CHAIN_MISMATCH",
    }
    for control in EXPECTED_NEGATIVES:
        subfixtures: list[dict[str, Any]] = []
        if control == "DUPLICATE_JSON_KEY":
            try:
                strict_load_bytes(b'{"x":1,"x":2}')
                observed: set[str] = set()
            except DuplicateKeyError:
                observed = {control}
            subfixtures.append({
                "subfixture_id": "strict_parser_fixture", "observed_codes": sorted(observed),
                "passed": observed == {control},
            })
        elif control == "NONFINITE_JSON":
            try:
                strict_load_bytes(b'{"x":NaN}')
                observed = set()
            except NonFiniteNumberError:
                observed = {control}
            subfixtures.append({
                "subfixture_id": "strict_parser_fixture", "observed_codes": sorted(observed),
                "passed": observed == {control},
            })
        else:
            mutations = [("primary_mutation", mutate_for_control(control, matrix))]
            if control == "SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH":
                fictional = copy.deepcopy(matrix)
                comparison = next(
                    row for row in fictional["snapshot_machine_comparisons"]
                    if row["comparison_id"] == "P061-SNAP-CMP-0063"
                )
                comparison["root_genealogy"]["projection"]["prefinal_roots"]["p3"].append("fictional_root.tex")
                comparison["root_genealogy"]["projection"]["prefinal_roots"]["p3"].sort()
                comparison["root_genealogy"]["projection_sha256"] = sha256(
                    canonical_bytes(comparison["root_genealogy"]["projection"])
                )
                mutations.append(("rehashed_fictional_p3_root", fictional))
            elif control == "SNAPSHOT_0063_INPUT_MISSING":
                duplicate = copy.deepcopy(matrix)
                comparison = next(
                    row for row in duplicate["snapshot_machine_comparisons"]
                    if row["comparison_id"] == "P061-SNAP-CMP-0063"
                )
                comparison["inputs"].append(copy.deepcopy(comparison["inputs"][0]))
                mutations.append(("duplicate_valid_input", duplicate))
            elif control == "STRUCTURE_DELTA_TAMPER":
                expected_added = copy.deepcopy(matrix)
                comparison = next(
                    row for row in expected_added["snapshot_machine_comparisons"]
                    if row["comparison_id"] == "P061-SNAP-CMP-0061-A"
                )
                comparison["expected_added"] = []
                mutations.append(("expected_added_removed", expected_added))
            subfixtures = []
            for mutation_id, mutated in mutations:
                codes = content_diagnostics(
                    mutated,
                    matrix if control == "DETERMINISM_MISMATCH" else None,
                    verify_git=True,
                )
                if control in independent_controls:
                    independent_observed, _ = independent_frozen_diagnostics(mutated)
                    codes |= independent_observed
                subfixtures.append({
                    "subfixture_id": mutation_id, "observed_codes": sorted(codes),
                    "passed": codes == {control},
                })
            observed = set().union(*(set(row["observed_codes"]) for row in subfixtures))
        cases.append(
            {
                "case_id": control,
                "expected_code": control,
                "observed_codes": sorted(observed),
                "passed": observed == {control} and all(row["passed"] for row in subfixtures),
                "subfixtures": subfixtures,
            }
        )
    if {row["case_id"] for row in cases} != set(EXPECTED_NEGATIVES):
        raise ValidationError("NEGATIVE_PROBE_IDENTITY")
    return {
        "total": len(cases),
        "passed": sum(row["passed"] for row in cases),
        "failed": [row["case_id"] for row in cases if not row["passed"]],
        "isolated": sum(row["passed"] for row in cases),
        "nonisolated": sum(not row["passed"] for row in cases),
        "full_unfiltered_diagnostics": True,
        "cases": cases,
    }


RESULT_H1 = "# Phase 061 Step 47 Process Authority Result"
RESULT_COUNTS = {
    "source_routes": "232", "claims": "40", "contradictions": "10",
    "phase_rows": "9", "snapshot_comparisons": "6", "ground_not_found": "7",
    "unverified_queue": "11", "full_text": "195", "strict_json": "11",
    "pdf_extents_pages": "14/130", "image_extents": "23",
}
RESULT_VALIDATION = {
    "content": "PASS_P061_STEP47_PROCESS_AUTHORITY",
    "matrix_negative_controls": "PASS_P061_STEP47_NEGATIVE_CONTROLS 78/78",
    "boundary_negative_controls": "PASS_P061_STEP47_BOUNDARY_NEGATIVE_CONTROLS 17/17",
    "determinism": "PASS_P061_STEP47_DETERMINISM 2/2",
    "builder_lf_sha256": EXPECTED_BUILDER_SHA256,
    "matrix_lf_sha256": EXPECTED_MATRIX_SHA256,
}
RESULT_PERSISTENCE = {
    "parent": EXPECTED_PARENT, "subject": EXPECTED_SUBJECT,
    "state": "PENDING_AT_PRECOMMIT_BY_DESIGN",
}
ACTIVE_LEDGER_ROW = (
    "| 061 | 46–51 | plan activation; Steps 46–47 | v1.0.20 reaudit | IN_PROGRESS | "
    "`Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md` | "
    "`Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md` | "
    "`Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json` | "
    "`PASS_P061_STEP47_PROCESS_AUTHORITY`; `PASS_WITH_CONCERNS`; counts `232/40/10/9/6/7/11`; "
    "negative `78/78`; boundary `17/17`; determinism `2/2`; persistence `PENDING_AT_PRECOMMIT_BY_DESIGN` | "
    "Step 48 is blocked until `PASS_P061_STEP47_PERSISTENCE` |"
)
PARENT_LEDGER_ROW = (
    "| 061 | 46–51 | plan activation; Steps 46–47 | lineage D | v1.0.20 재감사 | IN_PROGRESS | "
    "`Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md` | "
    "`Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md` | "
    "`Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json` | "
    "content PASS; counts `232/40/10/9/6/7/11`; negative `78/78`; boundary `17/17`; determinism `2/2`; "
    "persistence `PENDING_AT_PRECOMMIT_BY_DESIGN` | `PASS_P061_STEP47_PROCESS_AUTHORITY`; `PASS_WITH_CONCERNS` | "
    "Step 48 is blocked until `PASS_P061_STEP47_PERSISTENCE` |"
)
HANDOVER_POINTERS = (
    "13. 현재 Phase 상태: Phase 061 `IN_PROGRESS`, Step 47 process-authority adjudication",
    "14. 현재 result: `Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md`",
    "15. 현재 machine evidence: `Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json`",
)
HANDOVER_ROW = (
    "| Phase 061 Step 47 | Step 47 | `PASS_P061_STEP47_PROCESS_AUTHORITY`; `PASS_WITH_CONCERNS`; "
    "counts `232/40/10/9/6/7/11`; negative `78/78`; boundary `17/17`; determinism `2/2`; "
    "exact-seven containing checkpoint `PENDING_AT_PRECOMMIT_BY_DESIGN` | "
    "Step 48 is blocked until `PASS_P061_STEP47_PERSISTENCE` |"
)
FORBIDDEN_CONTROL_WORDS = re.compile(r"(?i)(?<![A-Z_])FAIL(?![A-Z_])|CONDITIONAL|stale|example-only|token-list")
GLOBAL_CURRENT_CONTROL_ASSERTION = re.compile(
    r"(?i)^\s*(?:[-*]\s*)?(?:\*\*|`)?(?:(?:Current|Overall|Global)\s+)?(?:Gate|Status)"
    r"(?:\*\*|`)?\s*[:=]\s*`?\s*"
    r"(?:FAIL\b|CONDITIONAL\b|STALE\b|EXAMPLE-ONLY\b|TOKEN-LIST\b)"
)
CURRENT_STEP_REFERENCE = re.compile(r"(?i)\bPhase\s*0*61\b|\bStep\s*0*47\b")
HISTORICAL_CONTROL_SCOPE = re.compile(
    r"(?i)\b(?:Historical|History|Previous|Prior|Status\s+Definitions?|"
    r"Known\s+Baseline\s+Debt|Baseline\s+Validation|Recovery|Archive|Archived)\b"
)
CURRENT_CONTROL_SCOPE = re.compile(
    r"(?i)\b(?:Current|Overall|Phase\s*0*61|Step\s*0*47|Gate)\b"
)
CURRENT_STATUS_HEADING = re.compile(r"(?i)^\s*Status\b(?!\s+Definitions?\b)")
STANDALONE_FORBIDDEN_CONTROL = re.compile(
    r"(?i)^(?:FAIL|CONDITIONAL|stale|example-only|token-list)$"
)
ACTIVE_LEDGER_HEADER = [
    "Phase", "Planned Steps", "Actual Steps", "Purpose", "Status", "Detailed Plan",
    "Canonical Result", "Machine Evidence", "Gate", "Exact Next",
]
PARENT_LEDGER_HEADER = [
    "Phase", "Planned Steps", "Actual Steps", "Block", "Purpose", "Status", "Plan",
    "Result", "Machine Artifacts", "Validation", "Gate", "Next Step",
]
HANDOVER_HEADER = ["Record", "Phase/Step Range", "Gate State", "Next Condition"]


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_table(text: str, heading: str) -> tuple[list[str], list[list[str]]] | None:
    lines = text.splitlines()
    if lines.count(heading) != 1:
        return None
    index = lines.index(heading) + 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index + 1 >= len(lines) or not lines[index].startswith("|") or not lines[index + 1].startswith("|"):
        return None
    header = table_cells(lines[index])
    separator = table_cells(lines[index + 1])
    if len(header) != len(separator) or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        return None
    rows: list[list[str]] = []
    index += 2
    while index < len(lines) and lines[index].startswith("|"):
        row = table_cells(lines[index])
        if len(row) != len(header):
            return None
        rows.append(row)
        index += 1
    return header, rows


def exact_two_column_table(text: str, heading: str, expected: dict[str, str]) -> bool:
    parsed = markdown_table(text, heading)
    if parsed is None:
        return False
    header, rows = parsed
    return header == ["Field", "Exact value"] and rows == [[key, value] for key, value in expected.items()]


def result_diagnostics(text: str | None) -> set[str]:
    if text is None:
        return {"RESULT_MISSING"}
    if FORBIDDEN_CONTROL_WORDS.search(text):
        return {"RESULT_EXPLICIT_FAIL"}
    required_tokens = {
        "PASS_P061_STEP47_PROCESS_AUTHORITY", "PASS_WITH_CONCERNS",
        "PASS_P061_STEP47_NEGATIVE_CONTROLS 78/78", "PASS_P061_STEP47_BOUNDARY_NEGATIVE_CONTROLS 17/17",
        "PASS_P061_STEP47_DETERMINISM 2/2", EXPECTED_BUILDER_SHA256, EXPECTED_MATRIX_SHA256,
    }
    structural = (
        text.splitlines().count(RESULT_H1) == 1
        and text.splitlines().count("Gate: `PASS_P061_STEP47_PROCESS_AUTHORITY`") == 1
        and text.splitlines().count("Status: `PASS_WITH_CONCERNS`") == 1
        and exact_two_column_table(text, "## Counts", RESULT_COUNTS)
        and exact_two_column_table(text, "## Validation", RESULT_VALIDATION)
        and exact_two_column_table(text, "## Persistence", RESULT_PERSISTENCE)
        and text.splitlines().count("Step 48 is blocked until `PASS_P061_STEP47_PERSISTENCE`.") == 1
    )
    if not structural and all(token in text for token in required_tokens):
        return {"RESULT_TOKEN_ONLY_FAKE"}
    return set() if structural else {"RESULT_CONTRACT"}


def exact_control_row(
    text: str | None, expected: str, missing: str, bad: str,
    heading: str, expected_header: list[str],
) -> set[str]:
    if text is None:
        return {missing}
    parsed = markdown_table(text, heading)
    if parsed is None:
        return {bad}
    header, rows = parsed
    phase_rows = [row for row in rows if row and row[0] == "061"]
    if (
        header != expected_header or phase_rows != [table_cells(expected)]
        or current_control_contradiction(text)
    ):
        return {bad}
    return set()


def handover_diagnostics(text: str | None) -> set[str]:
    if text is None:
        return {"HANDOVER_MISSING"}
    lines = text.splitlines()
    parsed = markdown_table(text, "## Handover Chain")
    canonical_start = lines.index("## Canonical Chain") if lines.count("## Canonical Chain") == 1 else -1
    canonical_end = lines.index("## Handover Chain") if lines.count("## Handover Chain") == 1 else -1
    canonical = lines[canonical_start + 1:canonical_end] if 0 <= canonical_start < canonical_end else []
    phase_rows = [] if parsed is None else [row for row in parsed[1] if row and row[0] == "Phase 061 Step 47"]
    if (
        parsed is None or parsed[0] != HANDOVER_HEADER
        or any(canonical.count(pointer) != 1 for pointer in HANDOVER_POINTERS)
        or phase_rows != [table_cells(HANDOVER_ROW)]
        or current_control_contradiction(text)
    ):
        return {"HANDOVER_BAD_ROW"}
    return set()


def current_control_contradiction(text: str) -> bool:
    heading_stack: list[tuple[int, str]] = []
    lines = text.splitlines()

    def unquote(line: str) -> str:
        return re.sub(r"^\s*(?:>\s*)+", "", line)

    for index, raw_line in enumerate(lines):
        normalized_line = unquote(raw_line)
        heading = re.match(r"^\s*(#{1,6})\s+(.+?)\s*$", normalized_line)
        setext = (
            re.fullmatch(r"\s*(=+|-+)\s*", unquote(lines[index + 1]))
            if index + 1 < len(lines) else None
        )
        assertion_line = normalized_line
        if heading is not None:
            level, title = len(heading.group(1)), heading.group(2).strip()
        elif normalized_line.strip() and setext is not None:
            level, title = (1 if setext.group(1).startswith("=") else 2), normalized_line.strip()
        else:
            level, title = 0, ""
        if level:
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
            assertion_line = title
        if CURRENT_STEP_REFERENCE.search(normalized_line) and FORBIDDEN_CONTROL_WORDS.search(normalized_line):
            return True
        control_scope = "NEUTRAL"
        for _, title in heading_stack:
            current_marker = bool(
                CURRENT_CONTROL_SCOPE.search(title) or CURRENT_STATUS_HEADING.search(title)
            )
            if current_marker:
                control_scope = "CURRENT"
            elif HISTORICAL_CONTROL_SCOPE.search(title):
                control_scope = "HISTORICAL"
        if control_scope == "HISTORICAL":
            continue
        if GLOBAL_CURRENT_CONTROL_ASSERTION.search(assertion_line):
            return True
        scalar_value = re.sub(r"[`*_]", "", assertion_line).strip()
        if control_scope == "CURRENT" and STANDALONE_FORBIDDEN_CONTROL.fullmatch(scalar_value):
            return True
        if normalized_line.lstrip().startswith("|"):
            cells = [re.sub(r"[`*_]", "", cell).strip() for cell in table_cells(normalized_line)]
            if (
                len(cells) == 2
                and re.fullmatch(r"(?i)(?:(?:Current|Overall|Global)\s+)?(?:Gate|Status)", cells[0])
                and FORBIDDEN_CONTROL_WORDS.search(cells[1])
            ):
                return True
    return False


def control_diagnostics(
    active_text: str | None | object = _UNSET,
    parent_text: str | None | object = _UNSET,
    handover_text: str | None | object = _UNSET,
) -> set[str]:
    active = (
        ACTIVE_LEDGER.read_text(encoding="utf-8") if ACTIVE_LEDGER.exists() else None
    ) if active_text is _UNSET else active_text
    parent = (
        PARENT_LEDGER.read_text(encoding="utf-8") if PARENT_LEDGER.exists() else None
    ) if parent_text is _UNSET else parent_text
    handover = (
        HANDOVER.read_text(encoding="utf-8") if HANDOVER.exists() else None
    ) if handover_text is _UNSET else handover_text
    if active is not None and not isinstance(active, str):
        raise TypeError("active_text")
    if parent is not None and not isinstance(parent, str):
        raise TypeError("parent_text")
    if handover is not None and not isinstance(handover, str):
        raise TypeError("handover_text")
    return (
        exact_control_row(active, ACTIVE_LEDGER_ROW, "ACTIVE_LEDGER_MISSING", "ACTIVE_LEDGER_BAD_ROW", "## Execution Ledger", ACTIVE_LEDGER_HEADER)
        | exact_control_row(parent, PARENT_LEDGER_ROW, "PARENT_LEDGER_MISSING", "PARENT_LEDGER_BAD_ROW", "## Ledger", PARENT_LEDGER_HEADER)
        | handover_diagnostics(handover)
    )


def evaluate_repository_state(evidence: dict[str, Any], require_exact_dirt: bool = True) -> set[str]:
    diagnostics: set[str] = set()
    if not (
        evidence.get("branch") == ACTIVE_BRANCH
        and evidence.get("head") == evidence.get("upstream") == evidence.get("origin_tracking")
        == evidence.get("live_active") == EXPECTED_PARENT
    ):
        diagnostics.add("REPOSITORY_ACTIVE_STATE")
    if evidence.get("protected_local") != evidence.get("protected_live") or evidence.get("protected_live") != EXPECTED_PROTECTED:
        diagnostics.add("REPOSITORY_PROTECTED_STATE")
    if evidence.get("main_local") != evidence.get("main_live") or evidence.get("main_live") != EXPECTED_MAIN:
        diagnostics.add("REPOSITORY_MAIN_STATE")
    if evidence.get("claude_diff") or any(str(path).startswith("Claude/") for path in evidence.get("porcelain_paths", [])):
        diagnostics.add("REPOSITORY_CLAUDE_DRIFT")
    if require_exact_dirt and set(evidence.get("dirty_paths", [])) != EXACT_SEVEN_SET:
        diagnostics.add("REPOSITORY_EXACT_SEVEN_DIRT")
    return diagnostics


def result_template() -> str:
    def table(rows: dict[str, str]) -> list[str]:
        return ["| Field | Exact value |", "|---|---|", *[f"| {key} | {value} |" for key, value in rows.items()]]
    return "\n".join([
        RESULT_H1, "", "Gate: `PASS_P061_STEP47_PROCESS_AUTHORITY`",
        "Status: `PASS_WITH_CONCERNS`", "", "## Counts", "", *table(RESULT_COUNTS),
        "", "## Validation", "", *table(RESULT_VALIDATION),
        "", "## Persistence", "", *table(RESULT_PERSISTENCE),
        "", "## Next step", "", "Step 48 is blocked until `PASS_P061_STEP47_PERSISTENCE`.", "",
    ])


def boundary_repository_diagnostics(evidence: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    if set(evidence.get("dirty_paths", [])) != EXACT_SEVEN_SET:
        diagnostics.add("EXTRA_DIRTY_PATH")
    if not (
        evidence.get("branch") == ACTIVE_BRANCH
        and evidence.get("head") == evidence.get("upstream") == evidence.get("origin_tracking")
        == evidence.get("live_active") == EXPECTED_PARENT
    ):
        diagnostics.add("ACTIVE_REMOTE_DIVERGENCE")
    if evidence.get("protected_local") != EXPECTED_PROTECTED or evidence.get("protected_live") != EXPECTED_PROTECTED:
        diagnostics.add("PROTECTED_DRIFT")
    if evidence.get("main_local") != EXPECTED_MAIN or evidence.get("main_live") != EXPECTED_MAIN:
        diagnostics.add("MAIN_DRIFT")
    if evidence.get("claude_diff") or any(str(path).startswith("Claude/") for path in evidence.get("porcelain_paths", [])):
        diagnostics.add("CLAUDE_DRIFT")
    return diagnostics


def run_boundary_negative_controls() -> dict[str, Any]:
    valid_result = result_template()
    valid_active = "\n".join((
        "# Active fixture", "", "## Execution Ledger", "",
        "| " + " | ".join(ACTIVE_LEDGER_HEADER) + " |",
        "|" + "|".join("---" for _ in ACTIVE_LEDGER_HEADER) + "|", ACTIVE_LEDGER_ROW, "",
    ))
    valid_parent = "\n".join((
        "# Parent fixture", "", "## Ledger", "",
        "| " + " | ".join(PARENT_LEDGER_HEADER) + " |",
        "|" + "|".join("---" for _ in PARENT_LEDGER_HEADER) + "|", PARENT_LEDGER_ROW, "",
    ))
    valid_handover = "\n".join((
        "# Handover fixture", "", "## Canonical Chain", "", *HANDOVER_POINTERS, "",
        "## Handover Chain", "", "| " + " | ".join(HANDOVER_HEADER) + " |",
        "|" + "|".join("---" for _ in HANDOVER_HEADER) + "|", HANDOVER_ROW, "",
    ))

    def replace_exact_table_row(text: str, first_cell: str, replacement: str) -> str:
        lines = text.splitlines()
        matches = [
            index for index, line in enumerate(lines)
            if line.startswith("|") and table_cells(line) and table_cells(line)[0] == first_cell
        ]
        if len(matches) != 1:
            raise ValidationError(f"REAL_CONTROL_ROW_CARDINALITY:{first_cell}:{len(matches)}")
        lines[matches[0]] = replacement
        return "\n".join(lines) + "\n"

    def virtualize_real_handover(text: str) -> str:
        lines = text.splitlines()
        for number, pointer in zip((13, 14, 15), HANDOVER_POINTERS):
            matches = [index for index, line in enumerate(lines) if line.startswith(f"{number}. ")]
            if len(matches) != 1:
                raise ValidationError(f"REAL_HANDOVER_POINTER_CARDINALITY:{number}:{len(matches)}")
            lines[matches[0]] = pointer
        current_matches = [
            index for index, line in enumerate(lines)
            if line.startswith("|") and table_cells(line)
            and table_cells(line)[0] == "Phase 061 Step 47"
        ]
        prior_matches = [
            index for index, line in enumerate(lines)
            if line.startswith("|") and table_cells(line)
            and table_cells(line)[0] == "Phase 061 Step 46"
        ]
        row_matches = current_matches if current_matches else prior_matches
        if len(row_matches) != 1 or len(current_matches) > 1 or len(prior_matches) > 1:
            raise ValidationError(
                f"REAL_HANDOVER_ROW_CARDINALITY:current={len(current_matches)}:prior={len(prior_matches)}"
            )
        lines[row_matches[0]] = HANDOVER_ROW
        return "\n".join(lines) + "\n"

    real_active = replace_exact_table_row(
        ACTIVE_LEDGER.read_text(encoding="utf-8"), "061", ACTIVE_LEDGER_ROW
    )
    real_parent = replace_exact_table_row(
        PARENT_LEDGER.read_text(encoding="utf-8"), "061", PARENT_LEDGER_ROW
    )
    real_handover = virtualize_real_handover(HANDOVER.read_text(encoding="utf-8"))
    if not (
        "CONDITIONAL_PENDING_P069" in real_active and "`FAIL`" in real_active
        and "`FAIL`" in real_parent and "stale top pointers" in real_handover
        and "Phase 060 Step 44 check" in real_handover
    ):
        raise ValidationError("REAL_CONTROL_HISTORY_NOT_PRESERVED")
    valid_repo = {
        "branch": ACTIVE_BRANCH, "head": EXPECTED_PARENT, "upstream": EXPECTED_PARENT,
        "origin_tracking": EXPECTED_PARENT, "live_active": EXPECTED_PARENT,
        "protected_local": EXPECTED_PROTECTED, "protected_live": EXPECTED_PROTECTED,
        "main_local": EXPECTED_MAIN, "main_live": EXPECTED_MAIN,
        "claude_diff": [], "porcelain_paths": [], "dirty_paths": sorted(EXACT_SEVEN_SET),
    }
    builder_data = BUILDER.read_bytes()
    builder_tree = ast.parse(lf_bytes(builder_data).decode("utf-8"), filename=BUILDER.as_posix())
    canonical_projection_sha = sha256(canonical_bytes(builder_security_ast_projection(builder_tree)))
    if (
        result_diagnostics(valid_result)
        or control_diagnostics(valid_active, valid_parent, valid_handover)
        or boundary_repository_diagnostics(valid_repo)
        or builder_ast_policy_diagnostics(builder_data)
        or canonical_projection_sha != EXPECTED_BUILDER_SECURITY_AST_SHA256
    ):
        raise ValidationError("BOUNDARY_BASELINE_NOT_CLEAN")
    token_fake = "\n".join((
        " ".join(("PASS_P061_STEP47_PROCESS_AUTHORITY", "PASS_WITH_CONCERNS")),
        "PASS_P061_STEP47_NEGATIVE_CONTROLS 78/78",
        "PASS_P061_STEP47_BOUNDARY_NEGATIVE_CONTROLS 17/17",
        "PASS_P061_STEP47_DETERMINISM 2/2", EXPECTED_BUILDER_SHA256, EXPECTED_MATRIX_SHA256,
    ))
    records: list[dict[str, Any]] = []

    def add_case(
        case_id: str,
        observations: list[tuple[str, set[str]] | tuple[str, set[str], set[str]]],
        expected: set[str] | None = None,
    ) -> None:
        wanted = {case_id} if expected is None else expected
        normalized = [
            (observation[0], observation[1], observation[2] if len(observation) == 3 else wanted)
            for observation in observations
        ]
        records.append({
            "case_id": case_id, "expected_codes": sorted(wanted),
            "observed_codes": sorted(set().union(*(codes for _, codes, _ in normalized))),
            "subfixtures": [
                {
                    "subfixture_id": name, "expected_codes": sorted(subwanted),
                    "observed_codes": sorted(codes), "passed": codes == subwanted,
                }
                for name, codes, subwanted in normalized
            ],
            "passed": all(codes == subwanted for _, codes, subwanted in normalized),
        })

    add_case("RESULT_MISSING", [("explicit_none", result_diagnostics(None))])
    add_case("RESULT_EXPLICIT_FAIL", [("status_fail", result_diagnostics(valid_result.replace("Status: `PASS_WITH_CONCERNS`", "Status: `FAIL`")))])
    add_case("RESULT_TOKEN_ONLY_FAKE", [("tokens_without_structure", result_diagnostics(token_fake))])
    malicious_current_assertions = (
        ("current_status_colon", "Current status: FAIL"),
        ("heading_status_colon", "## Status: FAIL"),
        ("overall_status_colon", "Overall status: FAIL"),
        ("two_column_status_row", "| Status | FAIL |"),
        ("gate_equals", "Gate = FAIL"),
    )
    malicious_split_heading_assertions = (
        ("historical_then_current_status", "## Historical\n### Current status\nStatus: FAIL"),
        ("historical_then_phase061_step47", "## Historical\n### Phase 061 Step 47\nStatus: FAIL"),
        ("historical_then_status_fail_heading", "## Historical\n### Status: FAIL"),
        ("historical_then_nested_status_row", "## Historical\n### Current status\n| Status | FAIL |"),
        ("recovery_then_current_gate", "## Recovery\n### Current gate\nGate: FAIL"),
    )
    residual_heading_assertions = (
        ("mixed_current_status_history", "## Historical\n### Current status history\nStatus: FAIL"),
        ("mixed_phase061_history", "## Historical\n### Phase 061 history\nStatus: FAIL"),
        ("setext_nested_current", "# Historical\nCurrent status\n---\nStatus: FAIL"),
        ("blockquoted_nested_current", "> ## Historical\n> ### Current status\n> Status: FAIL"),
    )
    standalone_current_values = (
        ("atx_status", "## Status\nFAIL"),
        ("atx_current_status", "## Current status\nFAIL"),
        ("setext_current_status", "Current status\n---\nFAIL"),
        ("blockquoted_current_status", "> ## Current status\n> FAIL"),
    )
    legitimate_historical_scopes = (
        "## Historical\n### Phase 060\nStatus: FAIL\n"
        "## Previous\nStatus: FAIL\n"
        "## Archive\nStatus: FAIL\n"
        "## Status Definitions\nStatus: FAIL"
    )
    add_case("ACTIVE_LEDGER_MISSING", [("explicit_none", control_diagnostics(None, valid_parent, valid_handover))])
    add_case("ACTIVE_LEDGER_BAD_ROW", [
        ("numeric_row_tamper", control_diagnostics(valid_active.replace("78/78", "77/78"), valid_parent, valid_handover)),
        ("valid_row_plus_explicit_fail", control_diagnostics(valid_active + "\nOverall gate: FAIL\n", valid_parent, valid_handover)),
        ("real_document_history_preserved", control_diagnostics(real_active, real_parent, real_handover), set()),
        ("real_document_current_contradiction", control_diagnostics(real_active + "\nOverall gate: FAIL\n", real_parent, real_handover)),
        ("historical_status_fail_clean", control_diagnostics(valid_active + "\n## Historical\nStatus: FAIL\n", valid_parent, valid_handover), set()),
        ("historical_phase061_fail_not_exempt", control_diagnostics(valid_active + "\n## Historical\nPhase 061 Status: FAIL\n", valid_parent, valid_handover)),
        *[
            (f"malicious_{name}", control_diagnostics(valid_active + f"\n{assertion}\n", valid_parent, valid_handover))
            for name, assertion in malicious_current_assertions
        ],
        ("historical_phase060_status_clean", control_diagnostics(valid_active + "\n## Historical\n### Phase 060\nStatus: FAIL\n", valid_parent, valid_handover), set()),
        *[
            (f"split_heading_{name}", control_diagnostics(valid_active + f"\n{assertion}\n", valid_parent, valid_handover))
            for name, assertion in malicious_split_heading_assertions
        ],
        ("legitimate_historical_scopes_clean", control_diagnostics(valid_active + f"\n{legitimate_historical_scopes}\n", valid_parent, valid_handover), set()),
        *[
            (f"residual_heading_{name}", control_diagnostics(valid_active + f"\n{assertion}\n", valid_parent, valid_handover))
            for name, assertion in residual_heading_assertions
        ],
        *[
            (f"standalone_value_{name}", control_diagnostics(valid_active + f"\n{assertion}\n", valid_parent, valid_handover))
            for name, assertion in standalone_current_values
        ],
    ])
    add_case("PARENT_LEDGER_MISSING", [("explicit_none", control_diagnostics(valid_active, None, valid_handover))])
    add_case("PARENT_LEDGER_BAD_ROW", [
        ("numeric_row_tamper", control_diagnostics(valid_active, valid_parent.replace("17/17", "16/17"), valid_handover)),
        ("valid_row_plus_explicit_fail", control_diagnostics(valid_active, valid_parent + "\nOverall gate: FAIL\n", valid_handover)),
        ("real_document_history_preserved", control_diagnostics(real_active, real_parent, real_handover), set()),
        ("real_document_current_contradiction", control_diagnostics(real_active, real_parent + "\nOverall gate: FAIL\n", real_handover)),
        ("historical_status_fail_clean", control_diagnostics(valid_active, valid_parent + "\n## Historical\nStatus: FAIL\n", valid_handover), set()),
        ("historical_phase061_fail_not_exempt", control_diagnostics(valid_active, valid_parent + "\n## Historical\nPhase 061 Status: FAIL\n", valid_handover)),
        *[
            (f"malicious_{name}", control_diagnostics(valid_active, valid_parent + f"\n{assertion}\n", valid_handover))
            for name, assertion in malicious_current_assertions
        ],
        ("historical_phase060_status_clean", control_diagnostics(valid_active, valid_parent + "\n## Historical\n### Phase 060\nStatus: FAIL\n", valid_handover), set()),
        *[
            (f"split_heading_{name}", control_diagnostics(valid_active, valid_parent + f"\n{assertion}\n", valid_handover))
            for name, assertion in malicious_split_heading_assertions
        ],
        ("legitimate_historical_scopes_clean", control_diagnostics(valid_active, valid_parent + f"\n{legitimate_historical_scopes}\n", valid_handover), set()),
        *[
            (f"residual_heading_{name}", control_diagnostics(valid_active, valid_parent + f"\n{assertion}\n", valid_handover))
            for name, assertion in residual_heading_assertions
        ],
        *[
            (f"standalone_value_{name}", control_diagnostics(valid_active, valid_parent + f"\n{assertion}\n", valid_handover))
            for name, assertion in standalone_current_values
        ],
    ])
    add_case("HANDOVER_MISSING", [("explicit_none", control_diagnostics(valid_active, valid_parent, None))])
    add_case("HANDOVER_BAD_ROW", [
        ("numeric_row_tamper", control_diagnostics(valid_active, valid_parent, valid_handover.replace("2/2", "1/2"))),
        ("valid_row_plus_explicit_fail", control_diagnostics(valid_active, valid_parent, valid_handover + "\nOverall gate: FAIL\n")),
        ("real_document_history_preserved", control_diagnostics(real_active, real_parent, real_handover), set()),
        ("real_document_current_contradiction", control_diagnostics(real_active, real_parent, real_handover + "\nOverall gate: FAIL\n")),
        ("historical_status_fail_clean", control_diagnostics(valid_active, valid_parent, valid_handover + "\n## Historical\nStatus: FAIL\n"), set()),
        ("historical_phase061_fail_not_exempt", control_diagnostics(valid_active, valid_parent, valid_handover + "\n## Historical\nPhase 061 Status: FAIL\n")),
        *[
            (f"malicious_{name}", control_diagnostics(valid_active, valid_parent, valid_handover + f"\n{assertion}\n"))
            for name, assertion in malicious_current_assertions
        ],
        ("historical_phase060_status_clean", control_diagnostics(valid_active, valid_parent, valid_handover + "\n## Historical\n### Phase 060\nStatus: FAIL\n"), set()),
        *[
            (f"split_heading_{name}", control_diagnostics(valid_active, valid_parent, valid_handover + f"\n{assertion}\n"))
            for name, assertion in malicious_split_heading_assertions
        ],
        ("legitimate_historical_scopes_clean", control_diagnostics(valid_active, valid_parent, valid_handover + f"\n{legitimate_historical_scopes}\n"), set()),
        *[
            (f"residual_heading_{name}", control_diagnostics(valid_active, valid_parent, valid_handover + f"\n{assertion}\n"))
            for name, assertion in residual_heading_assertions
        ],
        *[
            (f"standalone_value_{name}", control_diagnostics(valid_active, valid_parent, valid_handover + f"\n{assertion}\n"))
            for name, assertion in standalone_current_values
        ],
    ])
    for case_id, key, value in (
        ("EXTRA_DIRTY_PATH", "dirty_paths", sorted(EXACT_SEVEN_SET | {"unexpected.txt"})),
        ("ACTIVE_REMOTE_DIVERGENCE", "live_active", "0" * 40),
        ("PROTECTED_DRIFT", "protected_live", "0" * 40),
        ("MAIN_DRIFT", "main_live", "0" * 40),
        ("CLAUDE_DRIFT", "claude_diff", ["Claude/unexpected.tex"]),
    ):
        fixture = copy.deepcopy(valid_repo)
        fixture[key] = value
        add_case(case_id, [("repository_evidence", boundary_repository_diagnostics(fixture))])
    crlf_fixture = pretty_bytes({"a": [1, 2, {"finite": 3.5}], "b": False})
    crlf = crlf_fixture.replace(b"\n", b"\r\n")
    left, _ = strict_load_bytes(crlf_fixture)
    right, _ = strict_load_bytes(crlf)
    crlf_observed = set() if left == right and sha256(lf_bytes(crlf_fixture)) == sha256(lf_bytes(crlf)) else {"CRLF_EQUIVALENCE"}
    add_case("CRLF_EQUIVALENCE", [("lf_vs_crlf_semantic_equivalence", crlf_observed)], expected=set())

    matrix, _ = strict_load(MATRIX)
    claim_fixtures: list[tuple[str, dict[str, Any]]] = []
    mutated = copy.deepcopy(matrix); mutated["claims"][0].pop("object")
    claim_fixtures.append(("remove_object", mutated))
    mutated = copy.deepcopy(matrix); mutated["claims"][0]["unexpected"] = True
    claim_fixtures.append(("unexpected_top_key", mutated))
    mutated = copy.deepcopy(matrix); mutated["claims"][0]["object"] = {"kind": "CURATED_PROCESS_OR_SCIENCE_CLAIM", "title": "fictional replacement"}
    claim_fixtures.append(("replace_object", mutated))
    mutated = copy.deepcopy(matrix); mutated["claims"][0]["expected_evidence"]["semantic_standard"] = "fictional but nonempty"
    claim_fixtures.append(("replace_expected_semantic", mutated))
    mutated = copy.deepcopy(matrix); mutated["claims"][0]["target_phase"] = 90
    claim_fixtures.append(("target_phase_90", mutated))
    mutated = copy.deepcopy(matrix)
    mutated["claims"][0]["actual_evidence"] = copy.deepcopy(mutated["claims"][1]["actual_evidence"])
    mutated["claims"][0]["evidence_route_ids"] = copy.deepcopy(mutated["claims"][1]["evidence_route_ids"])
    claim_fixtures.append(("swap_valid_evidence_and_routes", mutated))
    mutated = copy.deepcopy(matrix)
    mutated["claims"][0]["provisional_observation"], mutated["claims"][1]["provisional_observation"] = (
        mutated["claims"][1]["provisional_observation"], mutated["claims"][0]["provisional_observation"],
    )
    claim_fixtures.append(("swap_valid_provisional_observations", mutated))
    add_case("CLAIM_SEMANTIC_CONTRACT", [
        (name, content_diagnostics(fixture, verify_git=True)) for name, fixture in claim_fixtures
    ])

    builder_source = lf_bytes(BUILDER.read_bytes()).decode("utf-8")

    def builder_variant(old: str, new: str) -> str:
        if builder_source.count(old) != 1:
            raise ValidationError("BUILDER_AST_FIXTURE_ANCHOR_CARDINALITY")
        return builder_source.replace(old, new, 1)

    ast_fixtures = (
        ("subprocess_module_alias", 'import subprocess as sp\nsp.run(["python", "x.py"])\n'),
        ("subprocess_direct_import", 'from subprocess import run\nrun(["python", "x.py"])\n'),
        ("subprocess_getattr", 'import subprocess\ngetattr(subprocess, "run")(["python", "x.py"])\n'),
        ("builtins_getattr_exec", 'import builtins\ngetattr(builtins, "exec")("x=1")\n'),
        ("builtins_eval_alias", 'from builtins import eval as evaluate\nevaluate("1+1")\n'),
        ("dunder_import", '__import__("subprocess").run(["python", "x.py"])\n'),
        ("subprocess_dynamic_getattr", 'import subprocess\nname = "run"\ngetattr(subprocess, name)(["python", "x.py"])\n'),
        ("subprocess_assigned_getattr", 'import subprocess\nr = getattr(subprocess, "run")\nr(["python", "x.py"])\n'),
        ("subprocess_assigned_dynamic_getattr", 'import subprocess\nmethod = "run"\nrunner = getattr(subprocess, method)\nrunner(["python", "x.py"])\n'),
        ("subprocess_importfrom_getoutput", 'from subprocess import getoutput\ngetoutput("python x.py")\n'),
        ("subprocess_module_getoutput", 'import subprocess\nsubprocess.getoutput("python x.py")\n'),
        ("subprocess_dunder_dict_run", 'import subprocess\nsubprocess.__dict__["run"](["python", "x.py"])\n'),
        ("builtins_dynamic_getattr", 'method = "exec"\ngetattr(__builtins__, method)("x = 1")\n'),
        ("globals_exec_subscription", 'globals()["exec"]("x = 1")\n'),
        ("git_clean_destructive", 'import subprocess\nsubprocess.run(["git", "clean", "-fdx"])\n'),
        ("git_config_alias_execution", 'import subprocess\nsubprocess.run(["git", "-c", "alias.x=!python x.py", "x"])\n'),
        ("git_diff_variable_no_index", 'import subprocess\nx = "--no-index"\nb = "abc"\np = "path"\nsubprocess.run(["git", "diff", "--name-only", x, b, "--", p])\n'),
        ("git_merge_base_variable_help", 'import subprocess\nx = "--help"\nb = "abc"\nsubprocess.run(["git", "merge-base", "--is-ancestor", x, b])\n'),
        ("git_ls_tree_variable_help", 'import subprocess\nx = "--help"\np = "path"\nsubprocess.run(["git", "ls-tree", "--full-tree", "-z", x, "--", p])\n'),
        ("run_git_helper_first_class_alias", 'def _run_git_bytes(repo, args, diagnostic):\n    return b""\n_run_git_bytes(None, ["rev-parse", "HEAD"], "safe")\nf = _run_git_bytes\nf(None, ["clean", "-fdx"], "bad")\n'),
        ("git_diff_variable_output", 'import subprocess\nx = "--output=evil.txt"\nb = "abc"\np = "path"\nsubprocess.run(["git", "diff", "--name-only", x, b, "--", p])\n'),
        ("git_diff_starred_output", 'import subprocess\nx = ["--output=evil.txt"]\nsubprocess.run(["git", "diff", "--name-only", *x, "a", "b", "--", "path"])\n'),
        ("run_git_helper_args_reassignment", 'import subprocess\ndef _run_git_bytes(repo, args, diagnostic):\n    args = ["clean", "-fdx"]\n    return subprocess.run(["git", *args])\n'),
        ("subprocess_executable_override", 'import subprocess\nsubprocess.run(["git", "rev-parse", "HEAD"], executable="python")\n'),
        ("subprocess_shell_true", 'import subprocess\nsubprocess.run(["git", "rev-parse", "HEAD"], shell=True)\n'),
        ("globals_exec_assigned", 'f = globals()["exec"]\nf("x = 1")\n'),
        ("builtins_exec_subscription", '__builtins__["exec"]("x = 1")\n'),
        (
            "actual_builder_ls_tree_commit_collision",
            builder_variant(
                'def git_blob(repo: Path, commit: str, path: str) -> bytes:\n    tree = subprocess.run(',
                'def git_blob(repo: Path, commit: str, path: str) -> bytes:\n    commit = "--help"\n    tree = subprocess.run(',
            ),
        ),
        (
            "actual_builder_merge_base_ancestor_collision",
            builder_variant(
                'def _git_is_ancestor(repo: Path, ancestor: str, descendant: str, diagnostic: str) -> bool:\n    proc = subprocess.run(',
                'def _git_is_ancestor(repo: Path, ancestor: str, descendant: str, diagnostic: str) -> bool:\n    ancestor = "--help"\n    proc = subprocess.run(',
            ),
        ),
        (
            "actual_builder_strict_load_eval_subscription",
            builder_variant(
                'def build(repo: Path) -> dict[str, Any]:\n    topology_bytes = ',
                'def build(repo: Path) -> dict[str, Any]:\n    strict_load_bytes = __builtins__["eval"]\n    topology_bytes = ',
            ),
        ),
        (
            "actual_builder_strict_load_eval_ifexp",
            builder_variant(
                'def build(repo: Path) -> dict[str, Any]:\n    topology_bytes = ',
                'def build(repo: Path) -> dict[str, Any]:\n    strict_load_bytes = eval if True else strict_load_bytes\n    topology_bytes = ',
            ),
        ),
    )
    add_case("BUILDER_AST_POLICY", [
        (name, builder_ast_policy_diagnostics(source.encode("utf-8"))) for name, source in ast_fixtures
    ])
    if tuple(row["case_id"] for row in records) != BOUNDARY_NEGATIVE_IDS:
        raise ValidationError("BOUNDARY_NEGATIVE_IDENTITY")
    return {
        "total": len(records), "passed": sum(row["passed"] for row in records),
        "failed": [row["case_id"] for row in records if not row["passed"]], "cases": records,
    }


def repository_diagnostics(require_exact_dirt: bool = True) -> tuple[set[str], dict[str, Any]]:
    branch = run_git("branch", "--show-current")
    head = run_git("rev-parse", "HEAD")
    upstream = run_git("rev-parse", "@{upstream}")
    origin_tracking = run_git("rev-parse", f"origin/{ACTIVE_BRANCH}")
    live_active = remote_tip(ACTIVE_BRANCH)
    protected_local = run_git("rev-parse", f"origin/{PROTECTED_BRANCH}")
    protected_live = remote_tip(PROTECTED_BRANCH)
    main_local = run_git("rev-parse", "origin/main")
    main_live = remote_tip("main")
    claude_diff = run_git("diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude")
    evidence = {
        "branch": branch, "head": head, "upstream": upstream,
        "origin_tracking": origin_tracking, "live_active": live_active,
        "protected_local": protected_local, "protected_live": protected_live,
        "main_local": main_local, "main_live": main_live,
        "claude_diff": claude_diff.splitlines() if claude_diff else [],
        "porcelain_paths": sorted(porcelain_paths()),
        "dirty_paths": sorted(exact_dirty_paths()),
    }
    return evaluate_repository_state(evidence, require_exact_dirt), evidence


def run_builder_determinism(matrix: dict[str, Any]) -> tuple[set[str], dict[str, Any]]:
    diagnostics = builder_static_diagnostics(BUILDER.read_bytes())
    evidence: dict[str, Any] = {"runs": 0, "production_imported": False}
    if diagnostics:
        evidence["execution_blocked_by_fixed_hash_or_ast"] = True
        return diagnostics, evidence
    outputs: list[bytes] = []
    with tempfile.TemporaryDirectory(prefix="p061-step47-validator-") as directory:
        temporary = Path(directory).resolve()
        try:
            temporary.relative_to(REPO.resolve())
        except ValueError:
            pass
        else:
            raise ValidationError("BUILDER_TEMP_INSIDE_WORKTREE")
        for number in (1, 2):
            output = temporary / f"matrix-{number}.json"
            try:
                proc = subprocess.run(
                    [sys.executable, str(BUILDER), "--repo", str(REPO), "--output", str(output)],
                    cwd=temporary, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    check=False, timeout=BUILDER_TIMEOUT,
                )
            except subprocess.TimeoutExpired as exc:
                raise ValidationError(f"BUILDER_SUBPROCESS_TIMEOUT:{number}:{BUILDER_TIMEOUT}s") from exc
            if proc.returncode:
                raise ValidationError(
                    f"BUILDER_SUBPROCESS_FAILED:{number}:returncode={proc.returncode}:"
                    f"stderr={proc.stderr.decode('utf-8', errors='replace').strip()}"
                )
            if proc.stdout or proc.stderr:
                evidence[f"run_{number}_stdout"] = proc.stdout.decode("utf-8", errors="replace")
                evidence[f"run_{number}_stderr"] = proc.stderr.decode("utf-8", errors="replace")
            data = output.read_bytes()
            value, _ = strict_load_bytes(data)
            if not isinstance(value, dict):
                diagnostics.add("DETERMINISM_MISMATCH")
            outputs.append(data)
    evidence["runs"] = len(outputs)
    first, second = outputs
    first_value, _ = strict_load_bytes(first)
    second_value, _ = strict_load_bytes(second)
    if canonical_bytes(first_value) != canonical_bytes(second_value):
        diagnostics.add("DETERMINISM_MISMATCH")
    if first_value != matrix or canonical_bytes(first_value) != canonical_bytes(matrix):
        diagnostics.add("DETERMINISM_MISMATCH")
    stored_lf = lf_bytes(MATRIX.read_bytes())
    if lf_bytes(first) != lf_bytes(second) or lf_bytes(first) != stored_lf:
        diagnostics.add("DETERMINISM_MISMATCH")
    evidence.update({
        "normalized_equal_2_of_2": not diagnostics,
        "run_1_sha256_lf": sha256(lf_bytes(first)),
        "run_2_sha256_lf": sha256(lf_bytes(second)),
        "stored_sha256_lf": sha256(stored_lf),
    })
    return diagnostics, evidence


def validate(content_only: bool = False) -> tuple[set[str], dict[str, Any]]:
    diagnostics: set[str] = set()
    evidence: dict[str, Any] = {}
    missing = [path.relative_to(REPO).as_posix() for path in (BUILDER, MATRIX) if not path.exists()]
    if missing:
        return {"STEP47_MISSING_ARTIFACT"}, {"missing": missing}
    builder_data = BUILDER.read_bytes()
    matrix_data = MATRIX.read_bytes()
    diagnostics |= builder_static_diagnostics(builder_data)
    if sha256(lf_bytes(matrix_data)) != EXPECTED_MATRIX_SHA256:
        diagnostics.add("MATRIX_FIXED_HASH_MISMATCH")
    matrix, traversal = strict_load(MATRIX)
    diagnostics |= content_diagnostics(matrix)
    independent_codes, independent_evidence = independent_frozen_diagnostics(matrix)
    diagnostics |= independent_codes
    builder_lf_hash = sha256(normalize_lf(BUILDER))
    if matrix.get("builder", {}).get("sha256_lf_normalized") != builder_lf_hash:
        diagnostics.add("BUILDER_SELF_HASH_MISMATCH")
    evidence.update(
        {
            "traversal": traversal,
            "builder_sha256_raw": sha256(builder_data),
            "builder_sha256_lf": builder_lf_hash,
            "matrix_sha256_raw": sha256(matrix_data),
            "matrix_sha256_lf": sha256(lf_bytes(matrix_data)),
            "builder_eol": classify_eol(builder_data),
            "matrix_eol": classify_eol(matrix_data),
            "validator_sha256_lf": sha256(normalize_lf(VALIDATOR)),
            "production_imported": False,
            "independent_reconstruction": independent_evidence,
        }
    )
    if not content_only:
        if not RESULT.exists():
            diagnostics.add("STEP47_RESULT_MISSING")
        else:
            diagnostics |= result_diagnostics(RESULT.read_text(encoding="utf-8"))
        diagnostics |= control_diagnostics()
        repository_codes, repository = repository_diagnostics()
        diagnostics |= repository_codes
        evidence["repository"] = repository
    return diagnostics, evidence


def verify_staged() -> int:
    diagnostics, _ = validate(content_only=False)
    staged = nul_paths("diff", "--cached", "--name-only", "-z")
    unstaged = nul_paths("diff", "--name-only", "-z")
    dirty = exact_dirty_paths()
    if staged != EXACT_SEVEN_SET or unstaged or dirty != EXACT_SEVEN_SET:
        diagnostics.add("STAGED_EXACT_SEVEN")
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        return 1
    print("PASS_P061_STEP47_STAGED 7/7")
    return 0


def verify_persistence() -> int:
    diagnostics, _ = validate(content_only=True)
    if not RESULT.exists():
        diagnostics.add("PERSISTENCE_RESULT_MISSING")
    else:
        diagnostics |= result_diagnostics(RESULT.read_text(encoding="utf-8"))
    diagnostics |= control_diagnostics()
    head = run_git("rev-parse", "HEAD")
    parent = run_git("rev-parse", "HEAD^")
    subject = run_git("show", "-s", "--format=%s", "HEAD")
    committed = nul_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD")
    branch = run_git("branch", "--show-current")
    upstream = run_git("rev-parse", "@{upstream}")
    origin_tracking = run_git("rev-parse", f"origin/{ACTIVE_BRANCH}")
    live_active = remote_tip(ACTIVE_BRANCH)
    protected_local = run_git("rev-parse", f"origin/{PROTECTED_BRANCH}")
    protected_live = remote_tip(PROTECTED_BRANCH)
    main_local = run_git("rev-parse", "origin/main")
    main_live = remote_tip("main")
    claude_diff = run_git("diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude")
    if parent != EXPECTED_PARENT:
        diagnostics.add("PERSISTENCE_PARENT")
    if subject != EXPECTED_SUBJECT:
        diagnostics.add("PERSISTENCE_SUBJECT")
    if committed != EXACT_SEVEN_SET:
        diagnostics.add("PERSISTENCE_EXACT_SEVEN")
    if porcelain_paths():
        diagnostics.add("PERSISTENCE_DIRTY")
    if not (branch == ACTIVE_BRANCH and head == upstream == origin_tracking == live_active):
        diagnostics.add("PERSISTENCE_ACTIVE_REMOTE")
    if protected_local != protected_live or protected_live != EXPECTED_PROTECTED:
        diagnostics.add("PERSISTENCE_PROTECTED")
    if main_local != main_live or main_live != EXPECTED_MAIN:
        diagnostics.add("PERSISTENCE_MAIN")
    if claude_diff:
        diagnostics.add("PERSISTENCE_CLAUDE")
    if run_git("diff", "--check"):
        diagnostics.add("PERSISTENCE_DIFF_CHECK")
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        return 1
    print(f"PASS_P061_STEP47_PERSISTENCE head={head}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    args = parser.parse_args()
    try:
        if args.verify_staged:
            return verify_staged()
        if args.verify_persistence:
            return verify_persistence()
        diagnostics, evidence = validate(content_only=args.content_only)
        if diagnostics:
            print("FAIL " + " ".join(sorted(diagnostics)))
            print(f"FAIL_P061_STEP47_PROCESS_AUTHORITY diagnostics={len(diagnostics)}")
            return 1
        matrix, _ = strict_load(MATRIX)
        if args.run_negative_probes:
            negatives = run_negative_controls(matrix)
            if negatives["failed"]:
                print("FAIL STEP47_NEGATIVE_CONTROLS " + " ".join(negatives["failed"]))
                return 1
            print(f"PASS_P061_STEP47_NEGATIVE_CONTROLS {negatives['passed']}/{negatives['total']}")
            print(
                "PASS_P061_STEP47_NEGATIVE_ISOLATION "
                f"isolated={negatives['isolated']} nonisolated={negatives['nonisolated']} "
                "full_unfiltered=true"
            )
            boundaries = run_boundary_negative_controls()
            if boundaries["failed"]:
                print("FAIL STEP47_BOUNDARY_NEGATIVE_CONTROLS " + " ".join(boundaries["failed"]))
                return 1
            print(
                f"PASS_P061_STEP47_BOUNDARY_NEGATIVE_CONTROLS "
                f"{boundaries['passed']}/{boundaries['total']}"
            )
        if args.determinism_check:
            determinism_codes, determinism_evidence = run_builder_determinism(matrix)
            if determinism_codes:
                print("FAIL STEP47_DETERMINISM " + " ".join(sorted(determinism_codes)))
                return 1
            print(
                "PASS_P061_STEP47_DETERMINISM "
                f"{determinism_evidence['runs']}/{determinism_evidence['runs']} "
                "production_imported=false"
            )
        counts = matrix["counts"]
        print(
            "PASS_P061_STEP47_PROCESS_AUTHORITY "
            f"routes={counts['source_routes']} claims={counts['claims']} "
            f"contradictions={counts['contradictions']} phases={counts['phase_rows']} "
            f"comparisons={counts['snapshot_machine_comparisons']} "
            f"GNF={counts['ground_not_found']} UNV={counts['unverified_queue']} "
            f"gate={matrix['gate']} production_imported={str(evidence['production_imported']).lower()}"
        )
        return 0
    except (ValidationError, DuplicateKeyError, NonFiniteNumberError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"FAIL STEP47_VALIDATOR_ERROR {type(exc).__name__}:{exc}")
        print("FAIL_P061_STEP47_PROCESS_AUTHORITY diagnostics=1")
        return 1


if __name__ == "__main__":
    sys.exit(main())
