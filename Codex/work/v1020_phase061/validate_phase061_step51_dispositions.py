#!/usr/bin/env python3
"""Independently validate Phase 061 Step 51.1 disposition artifacts."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
DISPOSITION_PATH = ROOT / "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json"
DELTA_PATH = ROOT / "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json"
BUILDER_PATH = ROOT / "Codex/work/v1020_phase061/build_phase061_step51_dispositions.py"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
STEP50_COMMIT = "a90c6e8659f4fcd24945af81e50c712bbc71ef30"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
COMMIT_SUBJECT = "audit(phase061): disposition v1020 lineage"
EXPECTED_BUILDER_SHA256 = "d6eaa462bb5fa4c2285e8093e0d8f584246907f93d43ddd805d9075ec52bfe3a"
EXPECTED_BUILDER_AST_SHA256_BY_RUNTIME = {
    (3, 12): "6ab08589f986f93df0c283863278be4da4ef07a343bead34b22b1e187ed0f043",
    (3, 14): "9281365ecd96f7aa15c4e58a38dba2386c4b7dc94815c36fe1bcb04efbfd2510",
}
EXPECTED_DISPOSITION_SEMANTIC_SHA256 = "8caa5e57333d81727d6703697aa5104e083d1c651cf3aeeb50df30dfe6f59fa2"
EXPECTED_CARRY_SEMANTIC_SHA256 = "1577c6926a3a786e6095704d57cc8973cb49a57fc148c7bdc4e65927e58df328"
EXPECTED_DEBT_ROUTING_SEMANTIC_SHA256 = "50a442f512fe58cbcc3cb041cc1cf9b0aa9eb1060d1f9c1292441e953f436ea3"
AUTHORITY_BOUNDARY = {
    "ceiling": "INTERNAL_LINEAGE_DISPOSITION_ONLY",
    "external_material_truth": False,
    "external_scientific_truth": False,
    "frozen_source_mutation": False,
    "primary_literature_truth": False,
}
ALLOWED_DISPOSITIONS = {
    "PRESERVE", "CORRECT", "DISCARD", "SUPERSEDE", "COMPETING_ONLY", "UNVERIFIED",
}
CANONICAL_JSON_DECLARATION = "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true"
EVIDENCE_ID_PATTERN = re.compile(r"\bP\d{3}-[A-Z0-9][A-Z0-9.-]*(?:-[A-Z0-9.]+)*\b")

TOPOLOGY = "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
STEP46_RESULT = "Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md"
PROCESS = "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json"
STEP47_RESULT = "Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md"
LINEAGE = "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json"
STEP48_RESULT = "Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md"
CITATION = "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json"
STEP49_RESULT = "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md"
REVIEW = "Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json"
VISUAL = "Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json"
STEP50_RESULT = "Codex/results/PHASE_061_STEP_050_REVIEW_ARTIFACT_RESULT.md"
P60_DISPOSITION = "Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json"
P60_DELTA = "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json"
INPUT_PATHS = (
    TOPOLOGY, STEP46_RESULT, PROCESS, STEP47_RESULT, LINEAGE, STEP48_RESULT,
    CITATION, STEP49_RESULT, REVIEW, VISUAL, STEP50_RESULT, P60_DISPOSITION, P60_DELTA,
)
EXPECTED_INPUT_SHA256 = {
    TOPOLOGY: "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c",
    STEP46_RESULT: "c26dda8533c2fd9abbe625c4025a0a7d98815d4e15890a484799395730eaea48",
    PROCESS: "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403",
    STEP47_RESULT: "4035e6c3302a856e19fb379cb8a52cb416bbe3ce001b5d499befce935adaaeb0",
    LINEAGE: "25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914",
    STEP48_RESULT: "c899437ece2851a2ebc5c68c1f39d4174ef07a73b453d5b7d03b7021b7c9fd9e",
    CITATION: "73004354e80635d3feb0543670c45eceee62086a1e1b6c67ff8b6e1293810ce9",
    STEP49_RESULT: "a8dab6f35b886230478d299bc3466bac22217c123a39cb2b53261a71bb066d50",
    REVIEW: "22b3b0cdb06b376a97076c30c73eecc1148dbd6dca5b49f60c09a85c4cd26d7b",
    VISUAL: "e204190857a60727f4d24855b03ec75683e7fdf7ed0addedaa7096dbb0309089",
    STEP50_RESULT: "385b672150044e990e53af3410b78f25e56177367d5ab65a9b3ef4847d411e58",
    P60_DISPOSITION: "1656e75871d33b438b48d17e861c4398debd027a5067c40108366259141afe50",
    P60_DELTA: "72848094865e0b2cad1110df92e7543dc287607af45dc2346e2040bd65812271",
}
EXPECTED_PATHS = {
    "Codex/work/v1020_phase061/build_phase061_step51_dispositions.py",
    "Codex/work/v1020_phase061/validate_phase061_step51_dispositions.py",
    "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json",
    "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json",
    "Codex/results/PHASE_061_STEP_051_1_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
}
RESULT_CONTROL_PATH = "Codex/results/PHASE_061_STEP_051_1_DISPOSITION_RESULT.md"
PARENT_LEDGER_CONTROL_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_CONTROL_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_CONTROL_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
CONTROL_DOCUMENT_REQUIREMENTS = {
    RESULT_CONTROL_PATH: (
        "PASS_P061_STEP51_1_DISPOSITIONS", "232/232", "PRESERVE 92", "COMPETING_ONLY 116",
        "52+5", "84", "91", "Step 51.2", "PENDING_AT_PRECOMMIT_BY_DESIGN",
    ),
    PARENT_LEDGER_CONTROL_PATH: (
        "Step 51.1", "PHASE_061_STEP_051_1_DISPOSITION_RESULT.md", "PASS_P061_STEP51_1_DISPOSITIONS", "Step 51.2",
    ),
    ACTIVE_LEDGER_CONTROL_PATH: (
        "Step 51.1", "PHASE_061_STEP_051_1_DISPOSITION_RESULT.md", "PASS_P061_STEP51_1_DISPOSITIONS", "Step 51.2",
    ),
    HANDOVER_CONTROL_PATH: (
        "Current checkpoint: Phase 061 Step 51.1", "PASS_P061_STEP51_1_DISPOSITIONS",
        "84", "91", "Step 51.2", "PENDING_AT_PRECOMMIT_BY_DESIGN",
    ),
}

DISPOSITION_TOP_KEYS = {
    "artifact_kind", "authority_boundary", "baseline_commit", "dispositions",
    "gate_summary", "generation", "inputs", "phase", "schema_version",
    "input_artifact_commit", "source_commit", "source_manifest_sha256", "step",
}
DISPOSITION_KEYS = {
    "acceptance_criterion", "authority_ceiling", "carry_forward_links",
    "disposition", "disposition_id", "evidence_ids", "evidence_routes",
    "external_material_truth", "external_scientific_truth", "reason",
    "process_authority_anchor", "source_authority_class", "source_identity", "source_id",
    "source_record_sha256", "status", "target_phase", "v1019_comparison_class",
}
DELTA_TOP_KEYS = {
    "artifact_kind", "authority_boundary", "baseline_commit", "debt_routing", "gate_summary",
    "generation", "inherited_carry_items", "inherited_phase060_blockers",
    "input_artifact_commit", "inputs", "new_blockers", "phase", "schema_version", "source_commit", "step",
}
EVIDENCE_ROUTE_KEYS = {
    "artifact_path", "evidence_ids", "json_pointer", "record_sha256", "route_role",
}
PROCESS_AUTHORITY_ANCHOR_KEYS = {"artifact_path", "json_pointer", "record_sha256", "source_id"}
DEBT_ROUTE_KEYS = {
    "corroborating_routes", "debt_id", "debt_requirement", "duplicate_or_refinement_of",
    "effective_target_phase", "non_double_count_basis", "origin_path", "origin_pointer",
    "origin_record_sha256", "origin_target_phase", "owner_acceptance_criterion",
    "owner_target_phase", "primary_owner_id", "primary_owner_type", "route_state",
    "schedule_relation", "status",
}
CORROBORATING_ROUTE_KEYS = {"edge_kind", "owner_id", "owner_type", "target_phase"}
NEW_BLOCKER_KEYS = {
    "acceptance_components", "acceptance_criterion", "authority_domain", "blocker_id",
    "closure_operator", "external_material_truth", "external_scientific_truth",
    "non_double_count_basis", "origin_anchors", "source_debt_ids", "status",
    "target_phase", "validity_domain",
}
ACCEPTANCE_COMPONENT_KEYS = {"component_id", "criterion", "status", "target_phase"}
ORIGIN_ANCHOR_KEYS = {"debt_id", "origin_path", "origin_pointer", "origin_record_sha256"}
CARRY_KEYS = {
    "acceptance_criterion_after", "acceptance_criterion_before", "acceptance_satisfied",
    "authority_boundary_after", "authority_boundary_before", "carry_forward_id",
    "category_after", "category_before", "delta_status", "external_material_truth",
    "external_scientific_truth", "prior_record", "prior_record_sha256",
    "refinement_note", "resolution_status", "status_after", "status_before",
    "target_phase_after", "target_phase_before", "touch_evidence_ids",
}
BLOCKER_INHERIT_KEYS = (CARRY_KEYS - {"carry_forward_id"}) | {"blocker_id"}
GENERATION_KEYS = {
    "active_branch", "builder", "canonical_json", "deterministic",
    "production_imported_or_executed",
}

CORRECTION_EVIDENCE: dict[str, tuple[str, ...]] = {
    "P061-SRC-0008": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0009": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0012": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0017": ("P061-STEP49-FINDING-001", "P060-BD-NEW-005"),
    "P061-SRC-0019": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0021": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0024": ("P061-STEP49-FINDING-002",),
    "P061-SRC-0027": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0028": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0029": ("P061-STEP49-FINDING-003", "P060-BD-NEW-003"),
    "P061-SRC-0030": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0036": ("P061-STEP49-FINDING-001",),
    "P061-SRC-0040": ("P061-STEP49-FINDING-001", "P061-STEP49-FINDING-003"),
    "P061-SRC-0045": ("P061-STEP50-P2-008",),
    "P061-SRC-0046": ("P061-STEP50-P2-009",),
    "P061-SRC-0053": ("P061-STEP49-FINDING-004",),
}
CONTEXT_EVIDENCE: dict[str, tuple[str, ...]] = {
    "P061-SRC-0003": ("P061-CON-008", "P061-CON-009", "P061-CON-010"),
    "P061-SRC-0043": ("P061-GNF-004", "P061-UNV-008"),
    "P061-SRC-0044": ("P061-GNF-004", "P061-UNV-008"),
    "P061-SRC-0047": ("P061-STEP50-P2-010",),
    "P061-SRC-0048": ("P061-STEP50-P2-010",),
    "P061-SRC-0049": ("P061-STEP50-P2-010",),
    "P061-SRC-0056": ("P061-CON-005",),
    "P061-SRC-0058": ("P061-CON-001",),
    "P061-SRC-0059": ("P061-CON-002",),
    "P061-SRC-0062": ("P061-CON-004", "P061-STEP50-P1-001"),
    "P061-SRC-0064": ("P061-UNV-003",),
    "P061-SRC-0065": ("P061-UNV-007",),
    "P061-SRC-0066": ("P061-UNV-007",),
    "P061-SRC-0067": ("P061-UNV-007",),
    "P061-SRC-0076": ("P061-CON-003",),
    "P061-SRC-0077": ("P061-CON-004", "P061-CON-009", "P061-STEP50-P1-001"),
    "P061-SRC-0085": ("P061-CON-003", "P061-CON-004", "P061-STEP50-P1-001"),
    "P061-SRC-0090": ("P061-UNV-001", "P061-STEP49-GNF-001"),
    "P061-SRC-0091": ("P061-CON-006", "P061-UNV-001", "P061-STEP49-GNF-001"),
    "P061-SRC-0092": ("P061-CON-007", "P061-UNV-001", "P061-STEP49-GNF-001"),
    "P061-SRC-0093": ("P061-UNV-001", "P061-STEP49-GNF-001"),
}
UNVERIFIED_SOURCE_IDS = {
    "P061-SRC-0064", "P061-SRC-0065", "P061-SRC-0066", "P061-SRC-0067",
    "P061-SRC-0090", "P061-SRC-0091", "P061-SRC-0092", "P061-SRC-0093",
}
COMPETING_SOURCE_OVERRIDES = {"P061-SRC-0043", "P061-SRC-0044"}
COMPETITIVE_REVIEW_PRESERVE = {f"P061-SRC-{index:04d}" for index in range(193, 205)}
CORRECTION_TARGETS = {
    "P061-STEP49-FINDING-001": 72, "P061-STEP49-FINDING-002": 71,
    "P061-STEP49-FINDING-003": 71, "P061-STEP49-FINDING-004": 72,
    "P061-STEP50-P2-008": 62, "P061-STEP50-P2-009": 62,
    "P060-BD-NEW-003": 81, "P060-BD-NEW-005": 67,
}
DIRECT_CARRY_EVIDENCE: dict[str, tuple[str, ...]] = {
    "P059-CFR-CF-08": ("P061-STEP48-GNF-002", "P061-STEP48-GNF-004"),
    "P059-CFR-CF-11": (
        "P061-CON-004", "P061-CON-006", "P061-CON-007", "P061-CON-010",
        "P061-STEP50-P1-001",
    ),
    "P059-CFR-RM-011": tuple(f"P061-STEP49-NEW-SOURCE-{i:03d}" for i in range(1, 9)),
    "P059-CFR-NS-05": ("P061-STEP49-GNF-001", "P061-STEP49-UNV-001"),
    "P059-CFR-ED-03": ("P061-STEP49-GNF-001", "P061-STEP49-UNV-003"),
    "P059-CFR-BD-NEW-003": ("P061-STEP49-GNF-002", "P061-STEP49-UNV-002"),
    "P059-CFR-RB-11": ("P061-STEP48-UNV-001", "P061-STEP48-UNV-002"),
    "P059-CFR-RB-12": (
        "P061-STEP50-P1-002", "P061-STEP50-P1-003", "P061-STEP50-P2-002",
        "P061-STEP50-P2-003", "P061-STEP50-P2-004", "P061-STEP50-P2-005",
        "P061-STEP50-P2-006", "P061-STEP50-P2-007", "P061-STEP50-P2-008",
        "P061-STEP50-P2-009", "P061-STEP50-P2-010",
    ),
    "P059-CFR-RB-13": ("P061-STEP49-FINDING-001",),
    "P059-CFR-ED-04": (
        "P061-STEP48-GNF-001", "P061-STEP48-GNF-003",
        "P061-STEP48-UNV-006", "P061-STEP48-UNV-007",
    ),
}
DIRECT_BLOCKER_EVIDENCE: dict[str, tuple[str, ...]] = {
    "P060-BD-NEW-001": ("P061-SRC-0005", "P061-SRC-0023"),
    "P060-BD-NEW-002": ("P061-SRC-0001", "P061-SRC-0004"),
    "P060-BD-NEW-003": ("P061-SRC-0029", "P061-SRC-0039", "P061-SRC-0040"),
    "P060-BD-NEW-004": ("P061-SRC-0006", "P061-STEP49-GNF-001"),
    "P060-BD-NEW-005": ("P061-SRC-0017", "P061-SRC-0040"),
}
REFINED_CARRY_IDS = {
    "P059-CFR-CF-11", "P059-CFR-RM-011", "P059-CFR-NS-05",
    "P059-CFR-ED-03", "P059-CFR-BD-NEW-003", "P059-CFR-RB-12",
    "P059-CFR-RB-13",
}
DEBT_SECTION_SPECS = (
    (PROCESS, "contradictions", "contradiction_id"),
    (PROCESS, "ground_not_found", "ground_id"),
    (PROCESS, "unverified_queue", "queue_id"),
    (LINEAGE, "ground_not_found", "ground_id"),
    (LINEAGE, "unverified_queue", "queue_id"),
    (CITATION, "bounded_semantic_findings", "finding_id"),
    (CITATION, "ground_not_found", "gnf_id"),
    (CITATION, "unverified_external_queue", "queue_id"),
    (CITATION, "genuinely_new_source_identity_debts", "queue_id"),
    (REVIEW, "review_findings", "id"),
    (REVIEW, "ground_not_found", "id"),
    (REVIEW, "unverified_queue", "id"),
)


class ValidationError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ValidationError(code, message)


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise ValidationError("JSON_DUPLICATE", f"duplicate key {key}")
        value[key] = child
    return value


def reject_constant(value: str) -> None:
    raise ValidationError("JSON_NONFINITE", f"nonfinite constant {value}")


def ensure_finite(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError("JSON_NONFINITE", f"nonfinite number at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            ensure_finite(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            ensure_finite(child, f"{path}[{index}]")


def strict_load_bytes(raw: bytes) -> Any:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicates, parse_constant=reject_constant)
    ensure_finite(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def record_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def physical_lines(raw: bytes) -> int:
    return 0 if not raw else raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parsed: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for relative in INPUT_PATHS:
        path = ROOT / relative
        require(path.is_file(), "INPUT_MISSING", relative)
        raw = path.read_bytes()
        require(sha256(raw) == EXPECTED_INPUT_SHA256[relative], "INPUT_PIN", relative)
        if relative.endswith(".json"):
            parsed[relative] = strict_load_bytes(raw)
            parse_mode = "STRICT_JSON_FULL_TRAVERSAL_DUPLICATE_KEY_AND_NONFINITE_REJECTED"
        else:
            parsed[relative] = raw.decode("utf-8")
            parse_mode = "FULL_UTF8_TEXT"
        metadata.append({
            "bytes": len(raw), "git_blob_sha1": git_blob_sha1(raw), "git_commit": STEP50_COMMIT,
            "parse_mode": parse_mode,
            "path": relative, "physical_lines": physical_lines(raw), "sha256": sha256(raw),
        })
    require(len(metadata) == 13, "INPUT_COUNT", "input count is not 13")
    return parsed, metadata


def build_indexes(inputs: dict[str, Any]) -> dict[str, Any]:
    sources = inputs[TOPOLOGY]["sources"]
    require(len(sources) == 232, "SOURCE_UNIVERSE", "source count")
    source_ids = [row["source_id"] for row in sources]
    require(len(set(source_ids)) == 232, "SOURCE_UNIVERSE", "duplicate topology source")
    expected_ids = [f"P061-SRC-{index:04d}" for index in range(1, 233)]
    require(source_ids == expected_ids, "SOURCE_ORDER", "topology")
    require([row["manifest_index_v1020"] for row in sources] == list(range(1, 233)), "SOURCE_INDEX", "topology")
    require(len({row["path"] for row in sources}) == 232, "SOURCE_PATH", "duplicate topology path")
    process_rows = inputs[PROCESS]["source_routes"]
    lineage_rows = inputs[LINEAGE]["delta_rows"]
    require(len(process_rows) == 232, "PROCESS_COUNT", "source routes")
    require(len(lineage_rows) == 232, "LINEAGE_COUNT", "delta rows")
    process_ids = [row["source_id"] for row in process_rows]
    lineage_ids = [row["v1020_source_id"] for row in lineage_rows]
    require(len(set(process_ids)) == 232, "PROCESS_DUPLICATE", "source routes")
    require(len(set(lineage_ids)) == 232, "LINEAGE_DUPLICATE", "delta rows")
    require(process_ids == expected_ids, "PROCESS_ORDER", "source routes")
    require(lineage_ids == expected_ids, "LINEAGE_ORDER", "delta rows")
    process_by_id = {row["source_id"]: row for row in process_rows}
    delta_by_id = {row["v1020_source_id"]: row for row in lineage_rows}
    for source, route, delta in zip(sources, process_rows, lineage_rows):
        for key in ("manifest_index_v1020", "path", "blob_sha1", "sha256", "manifest_extent", "review_mode"):
            require(route[key] == source[key], "PROCESS_SOURCE_IDENTITY", f"{source['source_id']}:{key}")
        require(delta["manifest_index_v1020"] == source["manifest_index_v1020"], "LINEAGE_SOURCE_IDENTITY", source["source_id"])
        require(delta["v1020"] == {
            "blob_sha1": source["blob_sha1"], "extent": source["manifest_extent"],
            "path": source["path"], "review_mode": source["review_mode"],
            "role": source["manifest_role"], "sha256": source["sha256"],
            "sha256_lf_normalized": source["sha256"] if source["review_mode"] == "FULL_TEXT" else None,
            "size_bytes": source["size_bytes"],
        }, "LINEAGE_SOURCE_IDENTITY", f"{source['source_id']}:v1020")
        authority = delta["step47_authority"]
        for key in ("authority_ceiling", "external_scientific_truth", "scientific_authority_promoted", "source_authority_class"):
            require(authority[key] == route[key], "LINEAGE_SOURCE_IDENTITY", f"{source['source_id']}:{key}")
    competitive_ids = {row["source_id"] for row in inputs[REVIEW]["competitive_source_records"]}
    adopted_ids = {row["source_id"] for row in inputs[REVIEW]["adopted_source_references"]}
    require(len(competitive_ids) == 126, "COMPETITIVE_COUNT", "competitive count")
    require(len(adopted_ids) == 43, "ADOPTED_COUNT", "adopted count")
    require(not competitive_ids & adopted_ids, "IDENTITY_COLLAPSE", "competitive/adopted overlap")
    citation_ids: dict[str, list[str]] = defaultdict(list)
    for row in inputs[CITATION]["authority_rows"]:
        citation_ids[row["source_id"]].append(row["asset_id"])
    return {
        "adopted_ids": adopted_ids, "citation_ids": citation_ids,
        "competitive_ids": competitive_ids, "delta_by_id": delta_by_id,
        "evidence_catalog": build_evidence_catalog(inputs),
        "process_by_id": process_by_id, "sources": sources,
    }


def source_number(source_id: str) -> int:
    return int(source_id.rsplit("-", 1)[1])


def expected_disposition(source_id: str, indexes: dict[str, Any]) -> str:
    route = indexes["process_by_id"][source_id]
    if source_id in COMPETING_SOURCE_OVERRIDES:
        return "COMPETING_ONLY"
    if ((source_id in indexes["competitive_ids"] and source_id not in COMPETITIVE_REVIEW_PRESERVE)
            or route["source_authority_class"] == "COMPETING_DRAFT"):
        return "COMPETING_ONLY"
    if source_id in CORRECTION_EVIDENCE:
        return "CORRECT"
    if source_id in UNVERIFIED_SOURCE_IDS:
        return "UNVERIFIED"
    return "PRESERVE"


def expected_target(source_id: str, disposition: str, indexes: dict[str, Any]) -> int:
    if disposition == "COMPETING_ONLY":
        return 62
    if disposition == "UNVERIFIED":
        if source_id == "P061-SRC-0064":
            return 67
        if source_id in {"P061-SRC-0065", "P061-SRC-0066", "P061-SRC-0067"}:
            return 62
        return 71
    if disposition == "CORRECT":
        return max(CORRECTION_TARGETS.get(item, 69) for item in CORRECTION_EVIDENCE[source_id])
    number = source_number(source_id)
    if source_id in {"P061-SRC-0001", "P061-SRC-0002", "P061-SRC-0231", "P061-SRC-0232"}:
        return 67
    if 43 <= number <= 49 or 193 <= number <= 230:
        return 62
    if 54 <= number <= 94:
        return 68
    if 4 <= number <= 42:
        return 71
    if source_id in {"P061-SRC-0051", "P061-SRC-0053"}:
        return 69
    return 62


def expected_evidence_ids(source_id: str, indexes: dict[str, Any]) -> list[str]:
    evidence = {source_id, indexes["delta_by_id"][source_id]["delta_id"]}
    evidence.update(CORRECTION_EVIDENCE.get(source_id, ()))
    evidence.update(CONTEXT_EVIDENCE.get(source_id, ()))
    evidence.update(indexes["citation_ids"].get(source_id, ()))
    return sorted(evidence)


def pointer_escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def collect_scalar_records(
    value: Any, path: str, pointer: str = "", parent: Any = None,
    parent_pointer: str = "",
) -> list[tuple[str, str, str, str]]:
    records: list[tuple[str, str, str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}/{pointer_escape(str(key))}"
            records.extend(collect_scalar_records(child, path, child_pointer, value, pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_pointer = f"{pointer}/{index}"
            records.extend(collect_scalar_records(child, path, child_pointer, value, pointer))
    elif isinstance(value, str):
        record = parent if isinstance(parent, (dict, list)) else value
        records.append((value, path, parent_pointer, sha256(record_bytes(record))))
    return records


def build_evidence_catalog(inputs: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    catalog: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in INPUT_PATHS:
        if not path.endswith(".json"):
            continue
        for evidence_id, artifact_path, pointer, record_hash in collect_scalar_records(inputs[path], path):
            route = {"artifact_path": artifact_path, "json_pointer": pointer, "record_sha256": record_hash}
            if route not in catalog[evidence_id]:
                catalog[evidence_id].append(route)
    return catalog


def preferred_evidence_path(evidence_id: str) -> str:
    if evidence_id.startswith(("P060-", "P059-")):
        return P60_DELTA
    if evidence_id.startswith("P061-STEP50-"):
        return REVIEW
    if evidence_id.startswith("P061-STEP49-"):
        return CITATION
    if evidence_id.startswith(("P061-STEP48-", "P061-DELTA-")):
        return LINEAGE
    if evidence_id.startswith(("P061-CON-", "P061-GNF-", "P061-UNV-")):
        return PROCESS
    if evidence_id.startswith("P061-SRC-"):
        return TOPOLOGY
    return CITATION


def expected_route_role(path: str) -> str:
    return {
        TOPOLOGY: "SOURCE_IDENTITY", PROCESS: "PROCESS_AUTHORITY",
        LINEAGE: "LINEAGE_DELTA_OR_DEBT", CITATION: "CITATION_AUTHORITY_OR_DEBT",
        REVIEW: "REVIEW_OR_VISUAL_DEBT", P60_DELTA: "INHERITED_CARRY_OR_BLOCKER",
    }.get(path, "BOUNDED_CONTEXT")


def expected_evidence_routes(
    source: dict[str, Any], indexes: dict[str, Any], inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    source_id = source["source_id"]
    ordinal = source["manifest_index_v1020"] - 1
    delta = indexes["delta_by_id"][source_id]
    routes = [
        {"artifact_path": TOPOLOGY, "evidence_ids": [source_id], "json_pointer": f"/sources/{ordinal}",
         "record_sha256": sha256(record_bytes(source)), "route_role": "SOURCE_IDENTITY"},
        {"artifact_path": LINEAGE, "evidence_ids": [delta["delta_id"]], "json_pointer": f"/delta_rows/{ordinal}",
         "record_sha256": sha256(record_bytes(delta)), "route_role": "LINEAGE_DELTA_OR_DEBT"},
    ]
    catalog = indexes["evidence_catalog"]
    for evidence_id in expected_evidence_ids(source_id, indexes):
        if evidence_id in {source_id, delta["delta_id"]}:
            continue
        preferred = preferred_evidence_path(evidence_id)
        matches = [candidate for candidate in catalog.get(evidence_id, []) if candidate["artifact_path"] == preferred]
        require(bool(matches), "EVIDENCE_ROUTE_ANCHOR", f"{source_id}:{evidence_id}")
        routes.append({**matches[0], "evidence_ids": [evidence_id], "route_role": expected_route_role(preferred)})
    return sorted(routes, key=lambda row: (row["artifact_path"], row["json_pointer"], row["evidence_ids"]))


def expected_carry_links(source: dict[str, Any], disposition: str) -> list[str]:
    source_id, path = source["source_id"], source["path"]
    links: set[str] = set()
    if "/plans/" in path or "/results/" in path or disposition in {"SUPERSEDE", "COMPETING_ONLY"}:
        links.add("P059-CFR-CF-11")
    if path.endswith((".pdf", ".png")) or "comp_P7_figs" in path:
        links.add("P059-CFR-RB-12")
    if path.endswith(".py"):
        links.update({"P059-CFR-CF-08", "P059-CFR-RB-11"})
    if "bib" in path.lower() or disposition == "UNVERIFIED":
        links.update({"P059-CFR-RM-011", "P059-CFR-NS-05", "P059-CFR-ED-03"})
    if source_id in {
        "P061-SRC-0008", "P061-SRC-0009", "P061-SRC-0012", "P061-SRC-0017",
        "P061-SRC-0019", "P061-SRC-0021", "P061-SRC-0027", "P061-SRC-0028",
        "P061-SRC-0030", "P061-SRC-0036", "P061-SRC-0040",
    }:
        links.add("P059-CFR-RB-13")
    for blocker_id, evidence in DIRECT_BLOCKER_EVIDENCE.items():
        if source_id in evidence:
            links.add(blocker_id)
    return sorted(links)


def expected_reason(source: dict[str, Any], disposition: str, indexes: dict[str, Any]) -> str:
    source_id = source["source_id"]
    route, delta = indexes["process_by_id"][source_id], indexes["delta_by_id"][source_id]
    if disposition == "COMPETING_ONLY":
        return ("This frozen occurrence belongs to the competitive/non-adopted corpus. Content or blob overlap "
                "cannot merge it with an adopted occurrence; an explicit future adoption edge is required.")
    if disposition == "CORRECT":
        return ("Direct Phase 061 evidence identifies a bounded source or process defect under "
                f"{', '.join(CORRECTION_EVIDENCE[source_id])}; correction applies only to a future "
                "Codex-controlled descendant, never to the frozen Claude occurrence.")
    if disposition == "UNVERIFIED":
        return ("The source is retained only at its recorded external-science-unverified ceiling; no primary-source, "
                "material, or experimental truth was established in Phase 061.")
    if source_id in CONTEXT_EVIDENCE:
        return ("This frozen occurrence remains necessary as bounded historical, structural, or review evidence. "
                f"Direct concerns {', '.join(CONTEXT_EVIDENCE[source_id])} constrain its use but do not justify "
                "deleting or rewriting the frozen occurrence.")
    return (f"The occurrence is a lossless {route['source_authority_class']} record with "
            f"{delta['comparison_class']} lineage and no direct Phase 061 evidence requiring source-level "
            "correction, supersession, or discard.")


def expected_acceptance(source: dict[str, Any], disposition: str, target: int) -> str:
    source_id, path = source["source_id"], source["path"]
    if disposition == "PRESERVE":
        return (f"Phase {target} retains {source_id} as the distinct frozen occurrence at {path}, preserves its blob "
                "and authority ceiling, and records any later adoption or rejection without promoting scientific or material truth.")
    if disposition == "CORRECT":
        return (f"Phase {target} resolves every cited defect for {source_id} in a Codex-controlled descendant, adds "
                "a persistent source-specific gate, and keeps the frozen occurrence and its defect evidence unchanged "
                "for lineage recovery.")
    if disposition == "COMPETING_ONLY":
        return (f"Phase {target} keeps {source_id} separate from all adopted identities and either records an explicit "
                "source-to-target adoption edge with bounded authority or retains the occurrence as non-adopted competitive evidence.")
    if disposition == "UNVERIFIED":
        if source_id == "P061-SRC-0064":
            return ("Phase 67 executes a fresh isolated build/test of P061-SRC-0064, persists the environment and full "
                    "result, and retains every unexecuted runtime claim as unverified.")
        if source_id in {"P061-SRC-0065", "P061-SRC-0066", "P061-SRC-0067"}:
            return (f"Phase 62 records an explicit adoption or non-adoption edge for {source_id}; any scientific "
                    "proposition remains separately unverified until Phase 71 primary-source review.")
        return (f"Phase {target} performs primary-source and proposition-level verification for {source_id}; until "
                "then it remains unverified and cannot support scientific, material, or experimental truth.")
    raise ValidationError("DISPOSITION_SEMANTIC", f"unsupported disposition {disposition}")


def collect_evidence_ids(value: Any) -> set[str]:
    evidence_ids: set[str] = set()
    if isinstance(value, dict):
        for child in value.values():
            evidence_ids.update(collect_evidence_ids(child))
    elif isinstance(value, list):
        for child in value:
            evidence_ids.update(collect_evidence_ids(child))
    elif isinstance(value, str):
        evidence_ids.update(EVIDENCE_ID_PATTERN.findall(value))
    return evidence_ids


def validate_evidence_membership(evidence_ids: list[str], evidence_universe: set[str], context: str) -> None:
    missing = sorted(set(evidence_ids) - evidence_universe)
    require(not missing, "EVIDENCE_UNIVERSE", f"{context}: {missing}")


def validate_generation(document: dict[str, Any]) -> None:
    require(document["phase"] == 61 and document["step"] == "51.1", "PHASE_STEP", "phase/step")
    require(document["source_commit"] == SOURCE_COMMIT, "SOURCE_COMMIT", "source commit")
    require(document["baseline_commit"] == SOURCE_COMMIT, "BASELINE_COMMIT", "baseline commit")
    require(document["input_artifact_commit"] == STEP50_COMMIT, "INPUT_COMMIT", "input artifact commit")
    require(document["authority_boundary"] == AUTHORITY_BOUNDARY, "AUTHORITY", "authority boundary")
    generation = document["generation"]
    require(set(generation) == GENERATION_KEYS, "GENERATION_SCHEMA", "generation keys")
    require(generation["active_branch"] == ACTIVE_BRANCH, "BRANCH_METADATA", "branch")
    require(generation["builder"] == "Codex/work/v1020_phase061/build_phase061_step51_dispositions.py", "BUILDER_PATH", "builder")
    require(generation["canonical_json"] == CANONICAL_JSON_DECLARATION, "CANONICAL_DECLARATION", "canonical JSON")
    require(generation["deterministic"] is True, "DETERMINISM_DECLARATION", "determinism")
    require(generation["production_imported_or_executed"] is False, "PRODUCTION_BOUNDARY", "production")


def validate_disposition(
    document: dict[str, Any], metadata: list[dict[str, Any]], indexes: dict[str, Any],
    evidence_universe: set[str], inputs: dict[str, Any],
) -> None:
    require(set(document) == DISPOSITION_TOP_KEYS, "DISPOSITION_TOP_SCHEMA", "top keys")
    validate_generation(document)
    require(document["inputs"] == metadata, "INPUT_FINGERPRINT", "input fingerprints")
    require(document["artifact_kind"] == "PHASE_061_V1020_DISPOSITION_MATRIX", "ARTIFACT_KIND", "disposition kind")
    require(document["schema_version"] == "phase061-step51.1-dispositions-v2", "SCHEMA_VERSION", "disposition schema")
    require(document["source_manifest_sha256"] == sha256(record_bytes(indexes["sources"])), "MANIFEST_HASH", "manifest hash")
    rows = document["dispositions"]
    require(len(rows) == 232, "SOURCE_COUNT", "disposition count")
    require(all(set(row) == DISPOSITION_KEYS for row in rows), "DISPOSITION_ROW_SCHEMA", "row keys")
    expected_ids = [source["source_id"] for source in indexes["sources"]]
    require([row["source_id"] for row in rows] == expected_ids, "SOURCE_MEMBERSHIP", "source order/membership")
    require(len({row["disposition_id"] for row in rows}) == 232, "DISPOSITION_ID", "duplicate id")
    for ordinal, (source, row) in enumerate(zip(indexes["sources"], rows), 1):
        source_id = source["source_id"]
        route = indexes["process_by_id"][source_id]
        delta = indexes["delta_by_id"][source_id]
        require(row["disposition"] in ALLOWED_DISPOSITIONS, "DISPOSITION_VALUE", source_id)
        expected = expected_disposition(source_id, indexes)
        require(row["disposition"] == expected, "DISPOSITION_SEMANTIC", source_id)
        require(row["disposition_id"] == f"P061-DISP-{ordinal:04d}", "DISPOSITION_ID", source_id)
        require(row["source_identity"] == {
            "blob_sha1": source["blob_sha1"], "dedup_group": source["dedup_group"],
            "manifest_index_v1020": source["manifest_index_v1020"],
            "path": source["path"], "sha256": source["sha256"],
        }, "SOURCE_IDENTITY", source_id)
        require(row["source_record_sha256"] == sha256(record_bytes(source)), "SOURCE_HASH", source_id)
        require(row["source_authority_class"] == route["source_authority_class"], "SOURCE_AUTHORITY", source_id)
        require(row["authority_ceiling"] == route["authority_ceiling"], "AUTHORITY_CEILING", source_id)
        require(row["v1019_comparison_class"] == delta["comparison_class"], "LINEAGE_CLASS", source_id)
        require(row["evidence_ids"] == expected_evidence_ids(source_id, indexes), "EVIDENCE_IDS", source_id)
        validate_evidence_membership(row["evidence_ids"], evidence_universe, source_id)
        require(all(set(route_record) == EVIDENCE_ROUTE_KEYS for route_record in row["evidence_routes"]), "EVIDENCE_ROUTE_SCHEMA", source_id)
        routed_ids = [evidence_id for route_record in row["evidence_routes"] for evidence_id in route_record["evidence_ids"]]
        require(Counter(routed_ids) == Counter(row["evidence_ids"]) and len(routed_ids) == len(set(routed_ids)), "EVIDENCE_ROUTE_BIJECTION", source_id)
        require(row["evidence_routes"] == expected_evidence_routes(source, indexes, inputs), "EVIDENCE_ROUTES", source_id)
        require(set(row["process_authority_anchor"]) == PROCESS_AUTHORITY_ANCHOR_KEYS, "PROCESS_ANCHOR_SCHEMA", source_id)
        require(row["process_authority_anchor"] == {
            "artifact_path": PROCESS,
            "json_pointer": f"/source_routes/{source['manifest_index_v1020'] - 1}",
            "record_sha256": sha256(record_bytes(route)),
            "source_id": source_id,
        }, "PROCESS_ANCHOR", source_id)
        require(row["reason"] == expected_reason(source, expected, indexes), "REASON", source_id)
        require(row["acceptance_criterion"] == expected_acceptance(source, expected, expected_target(source_id, expected, indexes)), "ACCEPTANCE", source_id)
        require(row["carry_forward_links"] == expected_carry_links(source, expected), "CARRY_LINKS", source_id)
        require(row["target_phase"] == expected_target(source_id, expected, indexes), "TARGET", source_id)
        expected_status = "PRESERVED_ACTIVE" if expected == "PRESERVE" else "OPEN"
        require(row["status"] == expected_status, "STATUS_SEMANTIC", source_id)
        require(row["external_material_truth"] is False and row["external_scientific_truth"] is False, "EXTERNAL_PROMOTION", source_id)
        if expected == "COMPETING_ONLY":
            require(source_id not in indexes["adopted_ids"], "IDENTITY_COLLAPSE", source_id)
    observed_counts = Counter(row["disposition"] for row in rows)
    require(observed_counts == Counter({
        "COMPETING_ONLY": 116, "CORRECT": 16, "PRESERVE": 92, "UNVERIFIED": 8,
    }), "DISPOSITION_DISTRIBUTION", str(observed_counts))
    if EXPECTED_DISPOSITION_SEMANTIC_SHA256 != "TO_BE_PINNED":
        require(sha256(record_bytes(rows)) == EXPECTED_DISPOSITION_SEMANTIC_SHA256, "DISPOSITION_DIGEST", "semantic digest")
    summary = document["gate_summary"]
    require(summary["status"] == "PASS", "SUMMARY_STATUS", "disposition summary")
    require(summary["source_expected"] == 232 and summary["disposition_rows"] == 232, "SUMMARY_COUNT", "disposition summary")
    require(summary["competitive_disposition_count"] == 116, "SUMMARY_COUNT", "competitive disposition")
    require(summary["disposition_counts"] == dict(sorted(observed_counts.items())), "SUMMARY_DISTRIBUTION", "disposition summary")
    for key in (
        "source_orphan_count", "duplicate_source_membership_count", "duplicate_disposition_id_count",
        "competitive_adopted_identity_overlap_count", "external_authority_promotion_count",
        "missing_acceptance_reason_target_status_count",
    ):
        require(summary[key] == 0, "SUMMARY_NONZERO", key)


def routed_evidence_for_owner(debt_routing: list[dict[str, Any]], owner_id: str) -> set[str]:
    evidence: set[str] = set()
    for row in debt_routing:
        if row["primary_owner_id"] == owner_id:
            evidence.add(row["debt_id"])
        if owner_id in {route["owner_id"] for route in row["corroborating_routes"]}:
            evidence.add(row["debt_id"])
    return evidence


def validate_new_blockers(rows: list[dict[str, Any]], inputs: dict[str, Any], inherited_ids: set[str]) -> None:
    require(len(rows) == 5, "NEW_BLOCKER_COUNT", "Phase 061 blockers")
    require(not inherited_ids & {row["blocker_id"] for row in rows}, "NEW_BLOCKER_COLLISION", "inherited/new")
    require([row["blocker_id"] for row in rows] == [f"P061-BD-NEW-{index:03d}" for index in range(1, 6)], "NEW_BLOCKER_ID", "stable order")
    origins: dict[str, tuple[str, str, str]] = {}
    for path, section, id_key in DEBT_SECTION_SPECS:
        for index, record in enumerate(inputs[path][section]):
            origins[record[id_key]] = (path, f"/{section}/{index}", sha256(record_bytes(record)))
    claimed: set[str] = set()
    for row in rows:
        blocker_id = row["blocker_id"]
        require(set(row) == NEW_BLOCKER_KEYS, "NEW_BLOCKER_SCHEMA", blocker_id)
        require(row["closure_operator"] == "ALL_OF" and row["status"] == "OPEN", "NEW_BLOCKER_STATUS", blocker_id)
        require(isinstance(row["authority_domain"], str) and row["authority_domain"].strip(), "NEW_BLOCKER_DOMAIN", blocker_id)
        require(isinstance(row["validity_domain"], str) and row["validity_domain"].strip(), "NEW_BLOCKER_DOMAIN", blocker_id)
        require(row["external_material_truth"] is False and row["external_scientific_truth"] is False, "EXTERNAL_PROMOTION", blocker_id)
        components = row["acceptance_components"]
        require(bool(components) and all(set(component) == ACCEPTANCE_COMPONENT_KEYS for component in components), "NEW_BLOCKER_COMPONENT_SCHEMA", blocker_id)
        require([component["component_id"] for component in components] == [f"A{index:02d}" for index in range(1, len(components) + 1)], "NEW_BLOCKER_COMPONENT_ID", blocker_id)
        require(all(component["status"] == "OPEN" and isinstance(component["target_phase"], int) and component["criterion"].strip() for component in components), "NEW_BLOCKER_COMPONENT", blocker_id)
        require(row["target_phase"] == max(component["target_phase"] for component in components), "NEW_BLOCKER_TARGET", blocker_id)
        component_ids = [component["component_id"] for component in components]
        require(row["acceptance_criterion"] == (
            f"ALL_OF components {', '.join(component_ids)} must PASS with persistent evidence; "
            "no partial component result may close the blocker."
        ), "NEW_BLOCKER_ACCEPTANCE", blocker_id)
        source_debt_ids = row["source_debt_ids"]
        require(bool(source_debt_ids) and len(source_debt_ids) == len(set(source_debt_ids)), "NEW_BLOCKER_DEBT_MEMBERSHIP", blocker_id)
        require(not claimed & set(source_debt_ids), "NEW_BLOCKER_DEBT_OVERLAP", blocker_id)
        claimed.update(source_debt_ids)
        require(len(row["origin_anchors"]) == len(source_debt_ids), "NEW_BLOCKER_ANCHOR", blocker_id)
        for debt_id, anchor in zip(source_debt_ids, row["origin_anchors"]):
            require(set(anchor) == ORIGIN_ANCHOR_KEYS and debt_id in origins, "NEW_BLOCKER_ANCHOR", f"{blocker_id}:{debt_id}")
            path, pointer, record_hash = origins[debt_id]
            require(anchor == {
                "debt_id": debt_id, "origin_path": path, "origin_pointer": pointer,
                "origin_record_sha256": record_hash,
            }, "NEW_BLOCKER_ANCHOR", f"{blocker_id}:{debt_id}")
        require(row["non_double_count_basis"] == (
            f"{blocker_id} is the sole primary acceptance surface for source debts "
            f"{', '.join(source_debt_ids)}; inherited carry and source dispositions are "
            "corroborating only where listed in debt_routing."
        ), "NEW_BLOCKER_NON_DOUBLE_COUNT", blocker_id)
    require(len(claimed) == 18, "NEW_BLOCKER_DEBT_MEMBERSHIP", f"claimed={len(claimed)}")


def debt_requirement(record: dict[str, Any]) -> str:
    for key in ("required_evidence", "object", "finding", "description"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValidationError("DEBT_REQUIREMENT", "origin record")


def validate_debt_routing(
    rows: list[dict[str, Any]], inputs: dict[str, Any], dispositions: list[dict[str, Any]],
    carry: list[dict[str, Any]], blockers: list[dict[str, Any]], new_blockers: list[dict[str, Any]],
) -> None:
    require(len(rows) == 91, "DEBT_COUNT", "canonical debt rows")
    require(all(set(row) == DEBT_ROUTE_KEYS for row in rows), "DEBT_SCHEMA", "debt route keys")
    origins: list[tuple[str, str, str, dict[str, Any]]] = []
    for path, section, id_key in DEBT_SECTION_SPECS:
        for index, record in enumerate(inputs[path][section]):
            origins.append((record[id_key], path, f"/{section}/{index}", record))
    require(len(origins) == 91 and len({row[0] for row in origins}) == 91, "DEBT_UNIVERSE", "origin identity")
    require([row["debt_id"] for row in rows] == [origin[0] for origin in origins], "DEBT_MEMBERSHIP", "origin order")
    owners: dict[str, tuple[str, int, str]] = {}
    for row in dispositions:
        owners[row["disposition_id"]] = ("SOURCE_DISPOSITION", row["target_phase"], row["acceptance_criterion"])
    for row in carry:
        owners[row["carry_forward_id"]] = ("INHERITED_CARRY", row["target_phase_after"], row["acceptance_criterion_after"])
    for row in blockers:
        owners[row["blocker_id"]] = ("PHASE060_BLOCKER", row["target_phase_after"], row["acceptance_criterion_after"])
    for row in new_blockers:
        owners[row["blocker_id"]] = ("PHASE061_BLOCKER", row["target_phase"], row["acceptance_criterion"])
    allowed_states = {"OPEN", "OPEN_DUPLICATE_ALIAS", "OPEN_REFINEMENT", "RESOLVED_INFORMATIONAL"}
    for row, (debt_id, path, pointer, record) in zip(rows, origins):
        require(row["origin_path"] == path and row["origin_pointer"] == pointer, "DEBT_ORIGIN", debt_id)
        require(row["origin_record_sha256"] == sha256(record_bytes(record)), "DEBT_ORIGIN_HASH", debt_id)
        require(row["origin_target_phase"] == record.get("target_phase"), "DEBT_ORIGIN_TARGET", debt_id)
        require(row["debt_requirement"] == debt_requirement(record), "DEBT_REQUIREMENT", debt_id)
        require(row["route_state"] in allowed_states, "DEBT_STATE", debt_id)
        expected_status = "RESOLVED" if row["route_state"] == "RESOLVED_INFORMATIONAL" else "OPEN"
        require(row["status"] == expected_status, "DEBT_STATUS", debt_id)
        if row["route_state"] in {"OPEN_DUPLICATE_ALIAS", "OPEN_REFINEMENT"}:
            require(row["duplicate_or_refinement_of"] in {origin[0] for origin in origins}, "DEBT_ALIAS", debt_id)
        else:
            require(row["duplicate_or_refinement_of"] is None, "DEBT_ALIAS", debt_id)
        require(row["primary_owner_id"] in owners, "DEBT_OWNER", debt_id)
        owner_type, owner_target, owner_acceptance = owners[row["primary_owner_id"]]
        require(row["primary_owner_type"] == owner_type, "DEBT_OWNER_TYPE", debt_id)
        require(row["owner_target_phase"] == owner_target, "DEBT_OWNER_TARGET", debt_id)
        require(row["owner_acceptance_criterion"] == owner_acceptance, "DEBT_OWNER_ACCEPTANCE", debt_id)
        origin_target = record.get("target_phase")
        effective_target = max(value for value in (origin_target, owner_target) if isinstance(value, int))
        require(row["effective_target_phase"] == effective_target, "DEBT_EFFECTIVE_TARGET", debt_id)
        if origin_target is None:
            relation = "ORIGIN_TARGET_NOT_SPECIFIED"
        elif owner_target == origin_target:
            relation = "MATCH"
        elif owner_target > origin_target:
            relation = "OWNER_LATER_THAN_ORIGIN"
        else:
            relation = "OWNER_EARLIER_THAN_ORIGIN"
        require(row["schedule_relation"] == relation, "DEBT_SCHEDULE", debt_id)
        expected_basis = (
            f"{debt_id} is the sole canonical origin row. Primary closure belongs only to "
            f"{row['primary_owner_id']}; duplicate/refinement and corroborating edges do not create "
            "additional closure claims."
        )
        require(row["non_double_count_basis"] == expected_basis, "DEBT_NON_DOUBLE_COUNT", debt_id)
        corroborating_ids: set[str] = set()
        for route in row["corroborating_routes"]:
            require(set(route) == CORROBORATING_ROUTE_KEYS, "DEBT_CORROBORATING_SCHEMA", debt_id)
            require(route["edge_kind"] == "CORROBORATING_OVERLAP", "DEBT_CORROBORATING_EDGE", debt_id)
            require(route["owner_id"] in owners and route["owner_id"] != row["primary_owner_id"], "DEBT_CORROBORATING_OWNER", debt_id)
            corroborating_type, corroborating_target, _ = owners[route["owner_id"]]
            require(route["owner_type"] == corroborating_type and route["target_phase"] == corroborating_target, "DEBT_CORROBORATING_OWNER", debt_id)
            require(route["owner_id"] not in corroborating_ids, "DEBT_CORROBORATING_DUPLICATE", debt_id)
            corroborating_ids.add(route["owner_id"])
    counts = Counter(row["route_state"] for row in rows)
    require(counts == Counter({"OPEN": 53, "OPEN_DUPLICATE_ALIAS": 12, "OPEN_REFINEMENT": 19, "RESOLVED_INFORMATIONAL": 7}), "DEBT_DISTRIBUTION", str(counts))
    require(sum(row["status"] == "OPEN" for row in rows) == 84, "DEBT_OPEN_COUNT", "open debt")
    if EXPECTED_DEBT_ROUTING_SEMANTIC_SHA256 != "TO_BE_PINNED":
        require(sha256(record_bytes(rows)) == EXPECTED_DEBT_ROUTING_SEMANTIC_SHA256, "DEBT_DIGEST", "debt routing")


def validate_delta(
    document: dict[str, Any], metadata: list[dict[str, Any]], inputs: dict[str, Any],
    evidence_universe: set[str], dispositions: list[dict[str, Any]],
) -> None:
    require(set(document) == DELTA_TOP_KEYS, "DELTA_TOP_SCHEMA", "top keys")
    validate_generation(document)
    require(document["inputs"] == metadata, "INPUT_FINGERPRINT", "delta fingerprints")
    require(document["artifact_kind"] == "PHASE_061_V1020_CARRY_FORWARD_DELTA", "ARTIFACT_KIND", "delta kind")
    require(document["schema_version"] == "phase061-step51.1-carry-forward-delta-v2", "SCHEMA_VERSION", "delta schema")
    prior_delta = inputs[P60_DELTA]
    carry = document["inherited_carry_items"]
    blockers = document["inherited_phase060_blockers"]
    new_blockers = document["new_blockers"]
    require(len(carry) == 52, "CARRY_COUNT", "carry count")
    require(len(blockers) == 5, "BLOCKER_COUNT", "inherited blocker count")
    require(all(set(row) == CARRY_KEYS for row in carry), "CARRY_SCHEMA", "carry keys")
    require(all(set(row) == BLOCKER_INHERIT_KEYS for row in blockers), "BLOCKER_INHERIT_SCHEMA", "blocker keys")
    inherited_ids = {row["carry_forward_id"] for row in carry} | {row["blocker_id"] for row in blockers}
    require(len(inherited_ids) == 57, "INHERITED_COLLISION", "52+5 collision")
    validate_new_blockers(new_blockers, inputs, inherited_ids)
    validate_debt_routing(document["debt_routing"], inputs, dispositions, carry, blockers, new_blockers)
    prior_carry = prior_delta["inherited_items"]
    prior_blockers = prior_delta["new_blockers"]
    require([row["carry_forward_id"] for row in carry] == [row["carry_forward_id"] for row in prior_carry], "CARRY_MEMBERSHIP", "carry order")
    require([row["blocker_id"] for row in blockers] == [row["blocker_id"] for row in prior_blockers], "BLOCKER_MEMBERSHIP", "blocker order")
    for row, prior in zip(carry, prior_carry):
        carry_id = row["carry_forward_id"]
        require(row["prior_record"] == prior and row["prior_record_sha256"] == sha256(record_bytes(prior)), "CARRY_PRIOR", carry_id)
        expected_evidence = sorted(set(DIRECT_CARRY_EVIDENCE.get(carry_id, ())) | routed_evidence_for_owner(document["debt_routing"], carry_id))
        primary_open = {
            route["debt_id"] for route in document["debt_routing"]
            if route["primary_owner_id"] == carry_id and route["route_state"].startswith("OPEN")
        }
        if carry_id in REFINED_CARRY_IDS or primary_open:
            expected_delta = "REFINED_DIRECT_EVIDENCE"
        elif expected_evidence:
            expected_delta = "TOUCHED_DIRECT_EVIDENCE"
        else:
            expected_delta = "UNCHANGED"
        require(row["touch_evidence_ids"] == expected_evidence and row["delta_status"] == expected_delta, "CARRY_DELTA", carry_id)
        expected_refinement = None
        if expected_delta == "REFINED_DIRECT_EVIDENCE":
            expected_refinement = (
                f"Phase 061 evidence {', '.join(expected_evidence)} directly refines the inherited acceptance "
                f"clause `{prior['acceptance_criterion_after']}`. The inherited target, authority, "
                "and open/preserved status remain verbatim and no resolution is claimed."
            )
        require(row["refinement_note"] == expected_refinement, "CARRY_REFINEMENT", carry_id)
        validate_evidence_membership(row["touch_evidence_ids"], evidence_universe, carry_id)
        require(row["status_before"] == prior["status_after"] and row["status_after"] == prior["status_after"], "CARRY_INHERITANCE", carry_id)
        require(row["target_phase_before"] == prior["target_phase_after"] and row["target_phase_after"] == prior["target_phase_after"], "CARRY_INHERITANCE", carry_id)
        require(row["acceptance_criterion_before"] == prior["acceptance_criterion_after"] and row["acceptance_criterion_after"] == prior["acceptance_criterion_after"], "CARRY_INHERITANCE", carry_id)
        require(row["authority_boundary_before"] == prior["authority_boundary_after"] and row["authority_boundary_after"] == prior["authority_boundary_after"], "CARRY_INHERITANCE", carry_id)
        require(row["category_before"] == prior["category_after"] and row["category_after"] == prior["category_after"], "CARRY_INHERITANCE", carry_id)
        require(row["acceptance_satisfied"] is False and row["resolution_status"] == "NOT_RESOLVED", "CARRY_RESOLUTION", carry_id)
        require(row["external_material_truth"] is False and row["external_scientific_truth"] is False, "EXTERNAL_PROMOTION", carry_id)
    for row, prior in zip(blockers, prior_blockers):
        blocker_id = row["blocker_id"]
        require(row["prior_record"] == prior and row["prior_record_sha256"] == sha256(record_bytes(prior)), "BLOCKER_PRIOR", blocker_id)
        expected_evidence = sorted(set(DIRECT_BLOCKER_EVIDENCE.get(blocker_id, ())) | routed_evidence_for_owner(document["debt_routing"], blocker_id))
        require(row["touch_evidence_ids"] == expected_evidence and row["delta_status"] == ("TOUCHED_DIRECT_EVIDENCE" if expected_evidence else "UNCHANGED"), "BLOCKER_DELTA", blocker_id)
        require(row["refinement_note"] is None, "BLOCKER_REFINEMENT", blocker_id)
        validate_evidence_membership(row["touch_evidence_ids"], evidence_universe, blocker_id)
        require(row["status_before"] == prior["status"] and row["status_after"] == prior["status"], "CARRY_INHERITANCE", blocker_id)
        require(row["target_phase_before"] == prior["target_phase"] and row["target_phase_after"] == prior["target_phase"], "CARRY_INHERITANCE", blocker_id)
        require(row["acceptance_criterion_before"] == prior["acceptance_criterion"] and row["acceptance_criterion_after"] == prior["acceptance_criterion"], "CARRY_INHERITANCE", blocker_id)
        require(row["authority_boundary_before"] == prior["authority_boundary"] and row["authority_boundary_after"] == prior["authority_boundary"], "CARRY_INHERITANCE", blocker_id)
        require(row["category_before"] == prior["category"] and row["category_after"] == prior["category"], "CARRY_INHERITANCE", blocker_id)
        require(row["acceptance_satisfied"] is False and row["resolution_status"] == "NOT_RESOLVED", "CARRY_RESOLUTION", blocker_id)
        require(row["external_material_truth"] is False and row["external_scientific_truth"] is False, "EXTERNAL_PROMOTION", blocker_id)
    if EXPECTED_CARRY_SEMANTIC_SHA256 != "TO_BE_PINNED":
        projection = {"carry": carry, "blockers": blockers, "new": document["new_blockers"]}
        require(sha256(record_bytes(projection)) == EXPECTED_CARRY_SEMANTIC_SHA256, "CARRY_DIGEST", "semantic digest")
    summary = document["gate_summary"]
    require(summary["status"] == "PASS", "SUMMARY_STATUS", "delta summary")
    require(summary["inherited_carry_count"] == 52 and summary["inherited_phase060_blocker_count"] == 5, "SUMMARY_COUNT", "52+5")
    require(summary["new_blocker_count"] == 5 and summary["acceptance_satisfied_count"] == 0, "SUMMARY_COUNT", "closure/blocker")
    require(summary["external_authority_promotion_count"] == 0 and summary["inherited_identity_duplicate_count"] == 0, "SUMMARY_NONZERO", "delta")
    require(summary["resolution_status_counts"] == {"NOT_RESOLVED": 57}, "SUMMARY_RESOLUTION", "delta")
    require(summary["delta_status_counts"] == {
        "REFINED_DIRECT_EVIDENCE": 12, "TOUCHED_DIRECT_EVIDENCE": 6, "UNCHANGED": 39,
    }, "SUMMARY_DELTA_STATUS", "delta")
    require(summary["status_after_counts"] == {"OPEN": 46, "PRESERVED_ACTIVE": 11}, "SUMMARY_STATUS_AFTER", "delta")
    require(summary["total_debt_count"] == 91 and summary["open_debt_count"] == 84, "SUMMARY_DEBT_COUNT", "delta")
    require(summary["orphan_open_debt_count"] == 0, "SUMMARY_DEBT_ORPHAN", "delta")
    require(summary["debt_route_state_counts"] == {
        "OPEN": 53, "OPEN_DUPLICATE_ALIAS": 12, "OPEN_REFINEMENT": 19,
        "RESOLVED_INFORMATIONAL": 7,
    }, "SUMMARY_DEBT_STATE", "delta")
    require(summary["primary_owner_type_counts"] == {
        "INHERITED_CARRY": 69, "PHASE061_BLOCKER": 18, "SOURCE_DISPOSITION": 4,
    }, "SUMMARY_DEBT_OWNER", "delta")
    expected_rationale = (
        "Five Phase 061 blockers are required because inherited carry and source dispositions "
        "do not individually own the full adoption, numerical-plus-experimental, two-phase-plus-LCO, "
        "Q2/Q3 full-truth-chain, or thermal-law-plus-heat-sign acceptance domains. Each new "
        "blocker uses ALL_OF atomic components and exact canonical debt anchors."
    )
    require(summary["new_blocker_rationale"] == expected_rationale, "SUMMARY_BLOCKER_RATIONALE", "delta")


def validate_payloads(disposition: dict[str, Any], delta: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]], indexes: dict[str, Any]) -> None:
    evidence_universe = collect_evidence_ids(inputs)
    require(inputs[P60_DISPOSITION]["gate_summary"]["status"] == "PASS", "PHASE060_GATE", "disposition")
    validate_disposition(disposition, metadata, indexes, evidence_universe, inputs)
    validate_delta(delta, metadata, inputs, evidence_universe, disposition["dispositions"])


def validate_import_boundary(source: str, allowed: set[str], role: str) -> ast.Module:
    tree = ast.parse(source)
    prohibited = {
        "__builtins__", "__import__", "compile", "eval", "exec", "getattr", "globals",
        "importlib", "locals", "runpy", "vars",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                require(alias.name.split(".", 1)[0] in allowed, "IMPORT_BOUNDARY", f"{role}:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            require(module.split(".", 1)[0] in allowed, "IMPORT_BOUNDARY", f"{role}:{module}")
            require(module != "subprocess", "SUBPROCESS_POLICY", f"{role}:from subprocess")
        if isinstance(node, ast.Name):
            require(node.id not in prohibited, "DYNAMIC_EXECUTION", f"{role}:{node.id}")
        if isinstance(node, ast.Attribute):
            require(node.attr not in {"__dict__", "import_module", "run_path"}, "DYNAMIC_EXECUTION", f"{role}:{node.attr}")
    return tree


def require_final_pin(value: str, name: str) -> None:
    require(
        bool(re.fullmatch(r"[0-9a-f]{64}", value)) and value != "0" * 64,
        "PIN_MISSING", name,
    )


def normalized_ast_sha256(tree: ast.AST) -> str:
    projection = ast.dump(tree, annotate_fields=True, include_attributes=False)
    return sha256(projection.encode("utf-8"))


def validate_builder_ast_policy(source: str) -> ast.Module:
    tree = validate_import_boundary(
        source,
        {"__future__", "argparse", "collections", "hashlib", "json", "math", "pathlib", "subprocess", "typing"},
        "builder",
    )
    subprocess_imports = 0
    calls: list[tuple[str, dict[str, str]]] = []
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess":
                    subprocess_imports += 1
                    require(alias.asname is None, "BUILDER_AST_POLICY", "aliased subprocess")
        if isinstance(node, ast.Subscript) and (
            isinstance(node.value, ast.Name) and node.value.id == "subprocess"
            or isinstance(node.value, ast.Attribute) and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "subprocess"
        ):
            raise ValidationError("BUILDER_AST_POLICY", "subprocess subscript")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "subprocess":
            require(node.attr == "run", "BUILDER_AST_POLICY", f"subprocess.{node.attr}")
            parent = parents.get(node)
            require(isinstance(parent, ast.Call) and parent.func is node, "BUILDER_AST_POLICY", "indirect subprocess.run access")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(node.func.id not in {"run", "Popen", "call", "check_call", "check_output"}, "BUILDER_AST_POLICY", node.func.id)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"):
            require(node.func.attr == "run", "BUILDER_AST_POLICY", node.func.attr)
            require(len(node.args) == 1 and isinstance(node.args[0], ast.List), "BUILDER_AST_POLICY", "argv")
            kwargs = {keyword.arg: ast.unparse(keyword.value) for keyword in node.keywords}
            require(None not in kwargs, "BUILDER_AST_POLICY", "star kwargs")
            calls.append((ast.unparse(node.args[0]), kwargs))
    require(subprocess_imports == 1, "BUILDER_AST_POLICY", "subprocess import count")
    expected_calls = [
        ("['git', 'branch', '--show-current']", {
            "capture_output": "True", "check": "True", "cwd": "ROOT", "text": "True", "timeout": "30",
        }),
        ("['git', 'merge-base', '--is-ancestor', STEP50_COMMIT, 'HEAD']", {
            "capture_output": "True", "check": "False", "cwd": "ROOT", "text": "True", "timeout": "30",
        }),
    ]
    require(sorted(calls, key=lambda item: item[0]) == sorted(expected_calls, key=lambda item: item[0]), "BUILDER_AST_POLICY", f"subprocess calls {calls}")
    return tree


def validate_source_policy() -> None:
    builder_raw = BUILDER_PATH.read_bytes()
    builder_source = builder_raw.decode("utf-8")
    for name, value in (
        ("builder", EXPECTED_BUILDER_SHA256),
        *[(f"builder AST {runtime}", digest) for runtime, digest in EXPECTED_BUILDER_AST_SHA256_BY_RUNTIME.items()],
        ("disposition", EXPECTED_DISPOSITION_SEMANTIC_SHA256),
        ("carry", EXPECTED_CARRY_SEMANTIC_SHA256),
        ("debt routing", EXPECTED_DEBT_ROUTING_SEMANTIC_SHA256),
    ):
        require_final_pin(value, name)
    require(sha256(builder_raw) == EXPECTED_BUILDER_SHA256, "BUILDER_DIGEST", "builder raw bytes")
    tree = validate_builder_ast_policy(builder_source)
    runtime = sys.version_info[:2]
    require(runtime in EXPECTED_BUILDER_AST_SHA256_BY_RUNTIME, "BUILDER_AST_RUNTIME", str(runtime))
    require(normalized_ast_sha256(tree) == EXPECTED_BUILDER_AST_SHA256_BY_RUNTIME[runtime], "BUILDER_AST_DIGEST", "builder AST")
    validate_import_boundary(
        Path(__file__).read_text(encoding="utf-8"),
        {"__future__", "argparse", "ast", "collections", "copy", "hashlib", "json", "math", "os", "pathlib", "re", "subprocess", "sys", "tempfile", "typing"},
        "validator",
    )


def deterministic_rebuild(disposition_raw: bytes, delta_raw: bytes) -> None:
    validate_source_policy()
    with tempfile.TemporaryDirectory(prefix="p061_step51_validate_") as temp:
        base = Path(temp)
        outputs: list[tuple[bytes, bytes]] = []
        for run in (1, 2):
            left = base / f"disposition_{run}.json"
            right = base / f"delta_{run}.json"
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            process = subprocess.run(
                [sys.executable, str(BUILDER_PATH), "--disposition-output", str(left), "--delta-output", str(right)],
                cwd=ROOT, env=env, capture_output=True, text=True, check=False, timeout=120,
            )
            require(process.returncode == 0, "REBUILD", process.stdout + process.stderr)
            outputs.append((left.read_bytes(), right.read_bytes()))
        require(outputs[0] == outputs[1], "DETERMINISM", "two rebuilds differ")
        require(outputs[0][0] == disposition_raw, "REBUILD", "disposition differs")
        require(outputs[0][1] == delta_raw, "REBUILD", "delta differs")


def run_negative_controls(disposition: dict[str, Any], delta: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]], indexes: dict[str, Any]) -> tuple[int, int]:
    controls: list[tuple[str, str, Callable[[], None]]] = [
        ("duplicate_json_key", "JSON_DUPLICATE", lambda: strict_load_bytes(b'{"x":1,"x":2}')),
        ("nonfinite_json", "JSON_NONFINITE", lambda: strict_load_bytes(b'{"x":NaN}')),
    ]

    def add(name: str, code: str, mutate: Callable[[dict[str, Any], dict[str, Any]], None]) -> None:
        def execute() -> None:
            left, right = copy.deepcopy(disposition), copy.deepcopy(delta)
            mutate(left, right)
            validate_payloads(left, right, inputs, metadata, indexes)
        controls.append((name, code, execute))

    add("missing_source", "SOURCE_COUNT", lambda a, _b: a["dispositions"].pop())
    add("duplicate_source", "SOURCE_MEMBERSHIP", lambda a, _b: a["dispositions"].__setitem__(-1, copy.deepcopy(a["dispositions"][0])))
    add("illegal_disposition", "DISPOSITION_VALUE", lambda a, _b: a["dispositions"][0].__setitem__("disposition", "ADOPT"))
    add("missing_target", "TARGET", lambda a, _b: a["dispositions"][0].__setitem__("target_phase", None))
    add("false_authority", "EXTERNAL_PROMOTION", lambda a, _b: a["dispositions"][0].__setitem__("external_scientific_truth", True))
    add("source_hash", "SOURCE_HASH", lambda a, _b: a["dispositions"][0].__setitem__("source_record_sha256", "0" * 64))
    add("missing_evidence", "EVIDENCE_IDS", lambda a, _b: a["dispositions"][0]["evidence_ids"].pop())
    add("evidence_route_mutation", "EVIDENCE_ROUTE_BIJECTION", lambda a, _b: a["dispositions"][0]["evidence_routes"].pop())
    add("generic_reason", "REASON", lambda a, _b: a["dispositions"][0].__setitem__("reason", "x"))
    add("generic_acceptance", "ACCEPTANCE", lambda a, _b: a["dispositions"][0].__setitem__("acceptance_criterion", "x"))
    add("carry_link_mutation", "CARRY_LINKS", lambda a, _b: a["dispositions"][0].__setitem__("carry_forward_links", []))
    add("wrong_status", "STATUS_SEMANTIC", lambda a, _b: a["dispositions"][0].__setitem__("status", "RESOLVED"))
    add("competitive_promoted", "DISPOSITION_SEMANTIC", lambda a, _b: a["dispositions"][42].__setitem__("disposition", "PRESERVE"))
    add("carry_status_mutation", "CARRY_INHERITANCE", lambda _a, b: b["inherited_carry_items"][0].__setitem__("status_after", "RESOLVED"))
    add("carry_false_resolution", "CARRY_RESOLUTION", lambda _a, b: b["inherited_carry_items"][0].__setitem__("resolution_status", "RESOLVED"))
    add("carry_evidence_mutation", "CARRY_DELTA", lambda _a, b: b["inherited_carry_items"][0]["touch_evidence_ids"].append("UNKNOWN"))
    add("missing_phase060_blocker", "BLOCKER_COUNT", lambda _a, b: b["inherited_phase060_blockers"].pop())
    add("blocker_category_mutation", "CARRY_INHERITANCE", lambda _a, b: b["inherited_phase060_blockers"][0].__setitem__("category_after", "OTHER"))
    add("blocker_authority_mutation", "CARRY_INHERITANCE", lambda _a, b: b["inherited_phase060_blockers"][0].__setitem__("authority_boundary_after", "OTHER"))
    add("blocker_refinement_mutation", "BLOCKER_REFINEMENT", lambda _a, b: b["inherited_phase060_blockers"][0].__setitem__("refinement_note", "x"))
    add("missing_debt", "DEBT_COUNT", lambda _a, b: b["debt_routing"].pop())
    add("debt_origin_hash", "DEBT_ORIGIN_HASH", lambda _a, b: b["debt_routing"][0].__setitem__("origin_record_sha256", "0" * 64))
    add("debt_owner_target", "DEBT_OWNER_TARGET", lambda _a, b: b["debt_routing"][0].__setitem__("owner_target_phase", 90))
    add("debt_status", "DEBT_STATUS", lambda _a, b: b["debt_routing"][0].__setitem__("status", "OPEN"))

    def add_input(name: str, code: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        def execute() -> None:
            changed = copy.deepcopy(inputs)
            mutate(changed)
            build_indexes(changed)
        controls.append((name, code, execute))

    add_input("duplicate_process", "PROCESS_COUNT", lambda value: value[PROCESS]["source_routes"].append(copy.deepcopy(value[PROCESS]["source_routes"][0])))
    add_input("duplicate_lineage", "LINEAGE_COUNT", lambda value: value[LINEAGE]["delta_rows"].append(copy.deepcopy(value[LINEAGE]["delta_rows"][0])))
    add_input("process_identity", "PROCESS_SOURCE_IDENTITY", lambda value: value[PROCESS]["source_routes"][0].__setitem__("path", "wrong"))
    add_input("lineage_authority", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["step47_authority"].__setitem__("authority_ceiling", "wrong"))
    add_input("lineage_v1020_blob", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("blob_sha1", "0" * 40))
    add_input("lineage_v1020_extent", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("extent", {}))
    add_input("lineage_v1020_path", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("path", "wrong"))
    add_input("lineage_v1020_review_mode", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("review_mode", "FULL_IMAGE"))
    add_input("lineage_v1020_role", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("role", "wrong"))
    add_input("lineage_v1020_sha256", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("sha256", "0" * 64))
    add_input("lineage_v1020_lf_sha256", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("sha256_lf_normalized", None))
    add_input("lineage_v1020_size", "LINEAGE_SOURCE_IDENTITY", lambda value: value[LINEAGE]["delta_rows"][0]["v1020"].__setitem__("size_bytes", -1))

    builder_source = BUILDER_PATH.read_text(encoding="utf-8")
    controls.extend([
        ("missing_pin", "PIN_MISSING", lambda: require_final_pin("TO_BE_PINNED", "fixture")),
        ("ast_git_clean", "BUILDER_AST_POLICY", lambda: validate_builder_ast_policy(
            builder_source.replace("[\"git\", \"branch\", \"--show-current\"]", "[\"git\", \"clean\", \"-fdx\"]", 1)
        )),
        ("ast_from_subprocess", "SUBPROCESS_POLICY", lambda: validate_builder_ast_policy(
            builder_source.replace("import subprocess", "from subprocess import run", 1)
        )),
        ("ast_subprocess_dict", "DYNAMIC_EXECUTION", lambda: validate_builder_ast_policy(
            builder_source.replace("subprocess.run(", "subprocess.__dict__[\"run\"](", 1)
        )),
        ("ast_subprocess_alias", "BUILDER_AST_POLICY", lambda: validate_builder_ast_policy(
            builder_source.replace("import subprocess", "import subprocess as sp", 1)
        )),
        ("ast_timeout_removed", "BUILDER_AST_POLICY", lambda: validate_builder_ast_policy(
            builder_source.replace("        timeout=30,\n", "", 1)
        )),
        ("ast_assigned_subprocess_run", "BUILDER_AST_POLICY", lambda: validate_builder_ast_policy(
            builder_source.replace("\ndef main() -> int:\n", "\n_evil = subprocess.run\n\ndef main() -> int:\n", 1)
        )),
        ("ast_subprocess_run_dunder_call", "BUILDER_AST_POLICY", lambda: validate_builder_ast_policy(
            builder_source.replace("subprocess.run(", "subprocess.run.__call__(", 1)
        )),
    ])

    add("acceptance_free_new_blocker", "NEW_BLOCKER_ACCEPTANCE", lambda _a, b: b["new_blockers"][0].__setitem__("acceptance_criterion", ""))
    add("new_blocker_collision", "NEW_BLOCKER_COLLISION", lambda _a, b: b["new_blockers"][0].__setitem__(
        "blocker_id", b["inherited_carry_items"][0]["carry_forward_id"],
    ))

    control_documents = {path: (ROOT / path).read_text(encoding="utf-8") for path in CONTROL_DOCUMENT_REQUIREMENTS}

    def invalid_gate_fixture() -> None:
        changed = dict(control_documents)
        changed[RESULT_CONTROL_PATH] += "\nGate: `FAIL_P061_STEP51_1_DISPOSITIONS`\n"
        validate_control_documents(changed)

    def invalid_handover_gate_fixture() -> None:
        changed = dict(control_documents)
        changed[HANDOVER_CONTROL_PATH] = changed[HANDOVER_CONTROL_PATH].replace(
            "| Phase 061 Step 51.1 | Step 51.1 | `PASS_P061_STEP51_1_DISPOSITIONS`;",
            "| Phase 061 Step 51.1 | Step 51.1 | `FAIL_P061_STEP51_1_DISPOSITIONS`;",
            1,
        )
        validate_control_documents(changed)

    def conflicting_current_gate_fixture(path: str, row_prefix: str) -> None:
        changed = dict(control_documents)
        lines = changed[path].splitlines()
        matching_indexes = [index for index, line in enumerate(lines) if line.startswith(row_prefix)]
        if len(matching_indexes) != 1:
            raise RuntimeError(f"fixture row count {path}: {len(matching_indexes)}")
        index = matching_indexes[0]
        original = lines[index]
        lines[index] = original.replace(
            "`PASS_P061_STEP51_1_DISPOSITIONS`",
            "`PASS_P061_STEP51_1_DISPOSITIONS`; `FAIL_P061_STEP51_1_DISPOSITIONS`",
            1,
        )
        if lines[index] == original:
            raise RuntimeError(f"fixture substitution failed: {path}")
        changed[path] = "\n".join(lines) + "\n"
        validate_control_documents(changed)

    controls.extend([
        ("invalid_gate_combination", "HUMAN_GATE", invalid_gate_fixture),
        ("invalid_handover_gate", "HUMAN_GATE", invalid_handover_gate_fixture),
        ("conflicting_parent_ledger_gate", "HUMAN_GATE", lambda: conflicting_current_gate_fixture(
            PARENT_LEDGER_CONTROL_PATH, "| 061 |",
        )),
        ("conflicting_active_ledger_gate", "HUMAN_GATE", lambda: conflicting_current_gate_fixture(
            ACTIVE_LEDGER_CONTROL_PATH, "| 061 |",
        )),
        ("conflicting_handover_gate", "HUMAN_GATE", lambda: conflicting_current_gate_fixture(
            HANDOVER_CONTROL_PATH, "| Phase 061 Step 51.1 |",
        )),
        ("extra_dirty_path", "EXACT_WORKTREE_SET", lambda: validate_precommit_path_sets(
            set(EXPECTED_PATHS), set(), set(EXPECTED_PATHS) | {"Codex/results/UNEXPECTED.txt"},
        )),
        ("protected_drift", "PROTECTED_DRIFT", lambda: validate_protected_tips("0" * 40, MAIN_TIP)),
    ])
    passed = 0
    for name, expected_code, control in controls:
        try:
            control()
        except ValidationError as error:
            require(error.code == expected_code, "NEGATIVE_DIAGNOSTIC", f"{name}: expected {expected_code}, got {error.code}")
            passed += 1
        else:
            raise ValidationError("NEGATIVE_ACCEPTED", name)
    return passed, len(controls)


def git_bytes(args: list[str], code: str = "GIT_COMMAND") -> bytes:
    try:
        process = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False, timeout=30)
    except subprocess.TimeoutExpired as error:
        raise ValidationError("GIT_TIMEOUT", str(args)) from error
    require(process.returncode == 0, code, f"{args}: {process.stderr.decode('utf-8', errors='replace').strip()}")
    return process.stdout


def git_output(args: list[str]) -> str:
    return git_bytes(args).decode("utf-8").strip()


def nul_paths(raw: bytes) -> set[str]:
    return {item.decode("utf-8").replace("\\", "/") for item in raw.split(b"\0") if item}


def validate_input_commit_blobs() -> None:
    for path in INPUT_PATHS:
        committed = git_bytes(["show", f"{STEP50_COMMIT}:{path}"])
        require(committed == (ROOT / path).read_bytes(), "INPUT_COMMIT_BLOB", path)


def validate_control_documents(documents: dict[str, str]) -> None:
    require(set(documents) == set(CONTROL_DOCUMENT_REQUIREMENTS), "HUMAN_CONTROL_SET", "control documents")
    for path, tokens in CONTROL_DOCUMENT_REQUIREMENTS.items():
        text_value = documents[path]
        for token in tokens:
            require(token in text_value, "HUMAN_CONTROL", f"{path}:{token}")
    result_gates = re.findall(r"(?m)^Gate: `([^`]+)`\s*$", documents[RESULT_CONTROL_PATH])
    require(result_gates == ["PASS_P061_STEP51_1_DISPOSITIONS"], "HUMAN_GATE", f"result gates={result_gates}")
    for path in (PARENT_LEDGER_CONTROL_PATH, ACTIVE_LEDGER_CONTROL_PATH):
        phase_rows = [line for line in documents[path].splitlines() if line.startswith("| 061 |")]
        require(len(phase_rows) == 1, "HUMAN_PHASE_ROW", f"{path}:rows={len(phase_rows)}")
        require("IN_PROGRESS" in phase_rows[0] and "PASS_P061_STEP51_1_DISPOSITIONS" in phase_rows[0], "HUMAN_PHASE_ROW", path)
        gate_tokens = re.findall(r"\b(?:PASS|FAIL|CONDITIONAL)_P061_STEP51_1_DISPOSITIONS\b", phase_rows[0])
        require(gate_tokens == ["PASS_P061_STEP51_1_DISPOSITIONS"], "HUMAN_GATE", f"{path}:gates={gate_tokens}")
    handover_rows = [line for line in documents[HANDOVER_CONTROL_PATH].splitlines() if line.startswith("| Phase 061 Step 51.1 |")]
    require(len(handover_rows) == 1, "HUMAN_GATE", f"handover rows={len(handover_rows)}")
    handover_cells = [cell.strip() for cell in handover_rows[0].split("|")[1:-1]]
    require(
        len(handover_cells) == 4
        and handover_cells[0] == "Phase 061 Step 51.1"
        and handover_cells[1] == "Step 51.1"
        and handover_cells[2].startswith("`PASS_P061_STEP51_1_DISPOSITIONS`;"),
        "HUMAN_GATE", f"handover gate row={handover_rows[0]}",
    )
    handover_gate_tokens = re.findall(
        r"\b(?:PASS|FAIL|CONDITIONAL)_P061_STEP51_1_DISPOSITIONS\b", handover_rows[0],
    )
    require(
        handover_gate_tokens == ["PASS_P061_STEP51_1_DISPOSITIONS"],
        "HUMAN_GATE", f"handover gates={handover_gate_tokens}",
    )


def validate_human_controls() -> None:
    validate_control_documents({
        path: (ROOT / path).read_text(encoding="utf-8")
        for path in CONTROL_DOCUMENT_REQUIREMENTS
    })


def validate_protected_tips(protected_tip: str, main_tip: str) -> None:
    require(protected_tip == PROTECTED_TIP, "PROTECTED_DRIFT", PROTECTED_BRANCH)
    require(main_tip == MAIN_TIP, "PROTECTED_DRIFT", "main")


def validate_protected_state() -> None:
    validate_protected_tips(
        git_output(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]),
        git_output(["rev-parse", "refs/remotes/origin/main"]),
    )
    changed = git_output(["diff", "--name-only", STEP50_COMMIT, "--", "Claude"])
    require(not changed, "CLAUDE_DRIFT", changed)


def validate_precommit_path_sets(staged: set[str], unstaged: set[str], status_paths: set[str]) -> None:
    require(staged == EXPECTED_PATHS, "EXACT_STAGED_SET", f"{sorted(staged)}")
    require(not unstaged, "UNSTAGED_DELTA", f"{sorted(unstaged)}")
    require(status_paths == EXPECTED_PATHS, "EXACT_WORKTREE_SET", f"{sorted(status_paths)}")


def validate_precommit() -> None:
    require(git_output(["branch", "--show-current"]) == ACTIVE_BRANCH, "ACTIVE_BRANCH", "precommit")
    require(git_output(["rev-parse", "HEAD"]) == STEP50_COMMIT, "PARENT_COMMIT", "precommit parent")
    staged = nul_paths(git_bytes(["diff", "--cached", "--name-only", "-z"]))
    unstaged = nul_paths(git_bytes(["diff", "--name-only", "-z"]))
    status_records = [item for item in git_bytes(["status", "--porcelain=v1", "-z", "--untracked-files=all"]).split(b"\0") if item]
    status_paths = {record[3:].decode("utf-8").replace("\\", "/") for record in status_records}
    validate_precommit_path_sets(staged, unstaged, status_paths)
    for path in EXPECTED_PATHS:
        require(git_bytes(["show", f":{path}"]) == (ROOT / path).read_bytes(), "STAGED_WORKTREE_MISMATCH", path)
    for args in (["diff", "--cached", "--check"], ["diff", "--check"]):
        git_bytes(args, "DIFF_CHECK")
    validate_human_controls()
    validate_input_commit_blobs()
    validate_protected_state()


def live_tip(branch: str) -> str:
    output = git_output(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"])
    require(bool(output), "REMOTE_TIP", branch)
    return output.split()[0]


def validate_persistence(expected_commit: str) -> None:
    require(git_output(["branch", "--show-current"]) == ACTIVE_BRANCH, "ACTIVE_BRANCH", "persistence")
    require(git_output(["rev-parse", "HEAD"]) == expected_commit, "PERSISTENCE_HEAD", expected_commit)
    require(git_output(["rev-parse", "@{upstream}"]) == expected_commit, "PERSISTENCE_UPSTREAM", expected_commit)
    require(live_tip(ACTIVE_BRANCH) == expected_commit, "PERSISTENCE_REMOTE", expected_commit)
    require(git_output(["show", "-s", "--format=%s", expected_commit]) == COMMIT_SUBJECT, "COMMIT_SUBJECT", expected_commit)
    require(git_output(["rev-parse", f"{expected_commit}^"]) == STEP50_COMMIT, "PARENT_COMMIT", expected_commit)
    changed = set(filter(None, git_output(["diff-tree", "--no-commit-id", "--name-only", "-r", expected_commit]).splitlines()))
    require(changed == EXPECTED_PATHS, "EXACT_COMMIT_SET", f"{sorted(changed)}")
    for path in EXPECTED_PATHS:
        require(git_bytes(["show", f"{expected_commit}:{path}"]) == (ROOT / path).read_bytes(), "COMMITTED_WORKTREE_MISMATCH", path)
    require(not git_output(["status", "--porcelain=v1", "--untracked-files=all"]), "DIRTY_AFTER_COMMIT", "worktree")
    validate_human_controls()
    validate_input_commit_blobs()
    validate_protected_state()
    require(live_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "PROTECTED_REMOTE_DRIFT", PROTECTED_BRANCH)
    require(live_tip("main") == MAIN_TIP, "PROTECTED_REMOTE_DRIFT", "main")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="artifact")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    try:
        require(DISPOSITION_PATH.is_file() and DELTA_PATH.is_file(), "ARTIFACT_MISSING", "Step 51.1 JSON")
        disposition_raw = DISPOSITION_PATH.read_bytes()
        delta_raw = DELTA_PATH.read_bytes()
        disposition = strict_load_bytes(disposition_raw)
        delta = strict_load_bytes(delta_raw)
        require(canonical_bytes(disposition) == disposition_raw, "CANONICAL_JSON", "disposition")
        require(canonical_bytes(delta) == delta_raw, "CANONICAL_JSON", "delta")
        inputs, metadata = load_inputs()
        indexes = build_indexes(inputs)
        validate_payloads(disposition, delta, inputs, metadata, indexes)
        negative_passed, negative_total = run_negative_controls(disposition, delta, inputs, metadata, indexes)
        deterministic_rebuild(disposition_raw, delta_raw)
        if args.mode == "precommit":
            validate_precommit()
        elif args.mode == "persistence":
            require(bool(args.expected_commit), "EXPECTED_COMMIT", "--expected-commit is required")
            validate_persistence(args.expected_commit)
    except (ValidationError, ValueError, KeyError, TypeError, OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"FAIL {error}")
        print("FAIL_P061_STEP51_1_DISPOSITIONS")
        return 1
    print("PASS source_occurrences=232 disposition_rows=232 orphan=0 duplicate=0")
    print("PASS inherited_carry=52 inherited_phase060_blockers=5 resolutions=0")
    print("PASS canonical_debts=91 open=84 resolved_informational=7 orphan_open=0 new_blockers=5")
    print(f"PASS negative_controls={negative_passed}/{negative_total}")
    print("PASS determinism=2/2 production_imported_or_executed=false")
    print("PASS_P061_STEP51_1_PERSISTENCE" if args.mode == "persistence" else "PASS_P061_STEP51_1_DISPOSITIONS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
