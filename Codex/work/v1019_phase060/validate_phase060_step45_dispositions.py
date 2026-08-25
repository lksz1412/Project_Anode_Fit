#!/usr/bin/env python3
"""Independently validate Phase 060 Step 45.1 disposition artifacts.

This validator reconstructs the source universe from prior audit artifacts. It
does not import the Step 45 builder or any frozen production module.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
DISPOSITION_PATH = ROOT / "Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json"
DELTA_PATH = ROOT / "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json"
BUILDER_PATH = ROOT / "Codex/work/v1019_phase060/build_phase060_step45_dispositions.py"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PRE_STEP45_COMMIT = "70b14fd102fca40ef17bee44e924c09dde1d9eff"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
AUTHORITY = (
    "Internal lineage disposition only; external material truth remains false; "
    "external scientific truth remains false."
)
BUILDER_RELATIVE_PATH = "Codex/work/v1019_phase060/build_phase060_step45_dispositions.py"
CANONICAL_JSON_DECLARATION = (
    "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true"
)
EXPECTED_BUILDER_SHA256 = (
    "3b8f9326896888b4fd973655f7e1e545aecffce16fe20f4514ab7fe4eb2ba225"
)
ALLOWED_DISPOSITIONS = {
    "PRESERVE", "CORRECT", "SUPERSEDE", "EMPIRICAL_ONLY",
    "THEORY_ONLY", "REJECT", "UNVERIFIED",
}
EXPECTED_DISPOSITIONS = Counter(
    {"CORRECT": 71, "PRESERVE": 48, "UNVERIFIED": 38,
     "THEORY_ONLY": 11, "EMPIRICAL_ONLY": 5}
)
EXPECTED_FAMILIES = Counter(
    {
        "STEP40_SOURCE_FINDING": 3,
        "STEP40_GROUND_NOT_FOUND": 5,
        "STEP41_CLAIM": 36,
        "STEP41_DEFECT_CORRECTION": 10,
        "STEP41_CONTRADICTION": 6,
        "STEP41_UNRESOLVED": 11,
        "STEP42_RUNTIME_FINDING": 15,
        "STEP42_VISUAL_FINDING": 4,
        "STEP43_TRACE_ROW": 28,
        "STEP43_FINDING": 25,
        "STEP44_PHYSICS_FINDING": 20,
        "STEP44_SOURCE_CONFLICT": 10,
    }
)
EXPECTED_BLOCKERS = {
    "P060-BD-NEW-001": 74,
    "P060-BD-NEW-002": 67,
    "P060-BD-NEW-003": 81,
    "P060-BD-NEW-004": 71,
    "P060-BD-NEW-005": 67,
}
EXPECTED_DISPOSITION_SEMANTIC_SHA256 = (
    "e850efd3280e2bca7091a267e4905d5ca5f4c47cfbd19e9528177966d8bf8042"
)
EXPECTED_CARRY_SEMANTIC_SHA256 = (
    "9b583ff3d422ada144263c38bb766a4c09e9d5ec90a355853586ea563c4b8dc9"
)
EXPECTED_BLOCKER_SEMANTIC_SHA256 = (
    "6aeaba8c720b893b0c8aa7684bfc5983875343a5757266d3a0559c6bc900bce7"
)
EXPECTED_DISPOSITION_GATE_SHA256 = (
    "349f236c7dd9f406ceacd7ac92c7657bf4035c79e0e98b0fb83d351781a3d9ad"
)
EXPECTED_DELTA_GATE_SHA256 = (
    "1a5dd4772d4b505501669867aaf7e77b88cf2628d55556b03268ea504dec4b91"
)

INPUT_PATHS = (
    "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json",
    "Codex/results/PHASE_060_STEP_040_SOURCE_TOPOLOGY_RESULT.md",
    "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json",
    "Codex/results/PHASE_060_STEP_041_PROCESS_AUTHORITY_RESULT.md",
    "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json",
    "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json",
    "Codex/results/PHASE_060_STEP_042_RUNTIME_ARTIFACT_RESULT.md",
    "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json",
    "Codex/results/PHASE_060_STEP_043_DOC_CODE_CONFORMANCE_RESULT.md",
    "Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json",
    "Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md",
    "Codex/results/PHASE_060_STEP_044_PHYSICS_REDERIVATION_RESULT.md",
    "Codex/results/PHASE_059_CARRY_FORWARD_REGISTER.json",
    "Codex/results/PHASE_059_VALIDATION.json",
    "Codex/results/PHASE_059_RESULT.md",
    "Codex/results/PHASE_059_STEP_039_4_CARRY_FORWARD_RESULT.md",
    "Codex/results/PHASE_059_STEP_039_6_GATE_RESULT.md",
)
S40_JSON, S40_RESULT, S41_JSON, S41_RESULT = INPUT_PATHS[:4]
S42_RUNTIME, S42_ARTIFACT, S42_RESULT = INPUT_PATHS[4:7]
S43_JSON, S43_RESULT = INPUT_PATHS[7:9]
S44_JSON, _S44_MD, S44_RESULT, P59_REGISTER = INPUT_PATHS[9:13]

DISPOSITION_TOP_KEYS = {
    "artifact_kind", "authority_boundary", "dispositions", "gate_summary",
    "generation", "inputs", "phase", "schema_version", "source_commit",
    "source_manifest", "step",
}
DELTA_TOP_KEYS = {
    "artifact_kind", "authority_boundary", "gate_summary", "generation",
    "inherited_items", "inputs", "new_blockers", "phase", "schema_version",
    "source_commit", "step",
}
MANIFEST_KEYS = {
    "evidence_paths", "source_anchors", "source_artifact_path",
    "source_collection", "source_family", "source_id", "source_index",
    "source_record_sha256", "source_summary",
}
DISPOSITION_KEYS = {
    "acceptance_criterion", "activation_gate",
    "affected_implementation_test_artifact", "authority_boundary",
    "blocker_family_id", "carry_forward_links", "disposition_id",
    "downstream_target_phases", "evidence_paths",
    "external_material_truth_validated", "external_scientific_truth_validated",
    "primary_disposition", "source_anchors", "source_family", "source_ids",
    "source_record_sha256", "target_horizon", "target_phase",
}
CARRY_KEYS = {
    "acceptance_criterion_after", "acceptance_criterion_before",
    "acceptance_satisfied", "activation_gate_after", "activation_gate_before",
    "authority_boundary_after", "authority_boundary_before", "carry_forward_id",
    "category_after", "category_before", "delta_status",
    "external_material_truth_validated", "external_scientific_truth_validated",
    "prior_record", "prior_record_sha256", "resolution_status",
    "source_route_source_id", "status_after", "status_before",
    "target_horizon_after", "target_horizon_before", "target_phase_after",
    "target_phase_before", "touch_evidence_paths", "touch_source_ids",
}
BLOCKER_KEYS = {
    "acceptance_criterion", "activation_gate",
    "affected_implementation_test_artifact", "authority_boundary", "blocker_id",
    "category", "evidence_paths", "external_material_truth_validated",
    "external_scientific_truth_validated", "non_double_count_basis",
    "old_collision_candidates", "source_anchors", "source_ids",
    "source_record_sha256", "status", "target_horizon", "target_phase",
}
GENERATION_KEYS = {
    "active_branch", "builder", "canonical_json", "deterministic",
    "production_imported",
}


class ValidationError(RuntimeError):
    """Raised when a Step 45.1 gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValidationError(f"nonfinite JSON constant: {value}")


def ensure_finite(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError(f"nonfinite JSON number at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            ensure_finite(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            ensure_finite(child, f"{path}[{index}]")


def strict_load_bytes(raw: bytes) -> Any:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicates,
        parse_constant=reject_constant,
    )
    ensure_finite(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def record_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


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
        require(path.is_file(), f"missing input: {relative}")
        raw = path.read_bytes()
        if relative.endswith(".json"):
            parsed[relative] = strict_load_bytes(raw)
            parse_mode = "STRICT_JSON_DUPLICATE_KEY_AND_NONFINITE_REJECTED"
        else:
            parsed[relative] = raw.decode("utf-8")
            parse_mode = "FULL_UTF8_TEXT"
        metadata.append({
            "bytes": len(raw), "git_blob_sha1": git_blob_sha1(raw),
            "parse_mode": parse_mode, "path": relative,
            "physical_lines": physical_lines(raw), "sha256": sha256(raw),
        })
    require(len(metadata) == 17, "input fingerprint count is not 17")
    return parsed, metadata


def source_summary(record: Any) -> str:
    if isinstance(record, str):
        return record
    for key in (
        "claim", "defect_summary", "title", "item", "finding", "summary",
        "statement", "topic", "text",
    ):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValidationError("source record has no usable summary")


def manifest_record(
    source_id: str, family: str, artifact_path: str, collection: str,
    index: int, record: Any, result_path: str,
    anchor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "evidence_paths": [artifact_path, result_path],
        "source_anchors": [anchor or {
            "artifact_path": artifact_path,
            "json_pointer": f"$.{collection}[{index}]",
        }],
        "source_artifact_path": artifact_path,
        "source_collection": collection,
        "source_family": family,
        "source_id": source_id,
        "source_index": index,
        "source_record_sha256": sha256(record_bytes(record)),
        "source_summary": source_summary(record),
    }


def reconstruct_manifest(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    step40_lines = inputs[S40_RESULT].splitlines()
    for index, (source_id, start, end) in enumerate(
        (("P060-S40-F01", 190, 192), ("P060-S40-F02", 194, 196),
         ("P060-S40-F03", 198, 200))
    ):
        record = {"end_line": end, "start_line": start,
                  "text": "\n".join(step40_lines[start - 1:end])}
        rows.append(manifest_record(
            source_id, "STEP40_SOURCE_FINDING", S40_RESULT,
            "confirmed_source_findings", index, record, S40_JSON,
            {"artifact_path": S40_RESULT, "end_line": end, "start_line": start},
        ))
    for index, line_number in enumerate(range(206, 211), 1):
        record = step40_lines[line_number - 1]
        rows.append(manifest_record(
            f"P060-S40-GNF-{index:03d}", "STEP40_GROUND_NOT_FOUND", S40_RESULT,
            "ground_not_found", index - 1, record, S40_JSON,
            {"artifact_path": S40_RESULT, "end_line": line_number,
             "start_line": line_number},
        ))

    step41 = inputs[S41_JSON]
    for index, record in enumerate(step41["claims"]):
        rows.append(manifest_record(record["claim_id"], "STEP41_CLAIM", S41_JSON,
                                    "claims", index, record, S41_RESULT))
    for index, record in enumerate(step41["defect_correction_records"]):
        rows.append(manifest_record(f"DCR-CU-{index + 2:02d}",
                                    "STEP41_DEFECT_CORRECTION", S41_JSON,
                                    "defect_correction_records", index, record, S41_RESULT))
    for index, record in enumerate(step41["contradictions"]):
        rows.append(manifest_record(record["contradiction_id"],
                                    "STEP41_CONTRADICTION", S41_JSON,
                                    "contradictions", index, record, S41_RESULT))
    for index, record in enumerate(step41["unresolved_queue"]):
        rows.append(manifest_record(record["unresolved_id"], "STEP41_UNRESOLVED",
                                    S41_JSON, "unresolved_queue", index, record, S41_RESULT))

    step42 = inputs[S42_RUNTIME]
    for severity, prefix in (("P1", "P060-S42-RT-P1"), ("P2", "P060-S42-RT-P2")):
        for index, record in enumerate(step42["findings"][severity]):
            rows.append(manifest_record(
                f"{prefix}-{index + 1:03d}", "STEP42_RUNTIME_FINDING", S42_RUNTIME,
                f"findings.{severity}", index, record, S42_RESULT,
                {"artifact_path": S42_RUNTIME,
                 "json_pointer": f"$.findings.{severity}[{index}]"},
            ))
    visual = inputs[S42_ARTIFACT]["manual_visual_attestation"]["findings"]
    for index, record in enumerate(visual):
        rows.append(manifest_record(
            record["id"], "STEP42_VISUAL_FINDING", S42_ARTIFACT,
            "manual_visual_attestation.findings", index, record, S42_RESULT,
            {"artifact_path": S42_ARTIFACT,
             "json_pointer": f"$.manual_visual_attestation.findings[{index}]"},
        ))

    step43 = inputs[S43_JSON]
    for index, record in enumerate(step43["trace_rows"]):
        rows.append(manifest_record(record["trace_id"], "STEP43_TRACE_ROW", S43_JSON,
                                    "trace_rows", index, record, S43_RESULT))
    for severity in ("P1", "P2"):
        for index, record in enumerate(step43["findings"][severity]):
            rows.append(manifest_record(
                record["id"], "STEP43_FINDING", S43_JSON, f"findings.{severity}",
                index, record, S43_RESULT,
                {"artifact_path": S43_JSON,
                 "json_pointer": f"$.findings.{severity}[{index}]"},
            ))

    step44 = inputs[S44_JSON]
    for index, record in enumerate(step44["findings"]):
        rows.append(manifest_record(record["finding_id"], "STEP44_PHYSICS_FINDING",
                                    S44_JSON, "findings", index, record, S44_RESULT))
    for index, record in enumerate(step44["source_conflicts"]):
        rows.append(manifest_record(record["conflict_id"], "STEP44_SOURCE_CONFLICT",
                                    S44_JSON, "source_conflicts", index, record, S44_RESULT))
    require(len(rows) == 173, "source universe is not 173")
    require(len({row["source_id"] for row in rows}) == 173,
            "source universe has duplicate identity")
    require(Counter(row["source_family"] for row in rows) == EXPECTED_FAMILIES,
            "source family distribution mismatch")
    return rows


def validate_common(document: dict[str, Any], metadata: list[dict[str, Any]]) -> None:
    require(document["phase"] == 60 and document["step"] == "45.1",
            "phase/step mismatch")
    require(document["source_commit"] == SOURCE_COMMIT, "source commit mismatch")
    require(document["authority_boundary"] == AUTHORITY, "authority mismatch")
    require(document["inputs"] == metadata, "input fingerprint mismatch")
    generation = document["generation"]
    require(set(generation) == GENERATION_KEYS, "generation schema mismatch")
    require(generation["active_branch"] == ACTIVE_BRANCH, "active branch metadata mismatch")
    require(generation["builder"] == BUILDER_RELATIVE_PATH,
            "generation builder path mismatch")
    require(generation["canonical_json"] == CANONICAL_JSON_DECLARATION,
            "generation canonical JSON declaration mismatch")
    require(generation["deterministic"] is True, "determinism declaration false")
    require(generation["production_imported"] is False, "production imported")


def validate_payloads(
    disposition: dict[str, Any], delta: dict[str, Any],
    metadata: list[dict[str, Any]], manifest: list[dict[str, Any]],
    prior_items: list[dict[str, Any]],
) -> None:
    require(set(disposition) == DISPOSITION_TOP_KEYS, "disposition top schema mismatch")
    require(set(delta) == DELTA_TOP_KEYS, "delta top schema mismatch")
    validate_common(disposition, metadata)
    validate_common(delta, metadata)
    require(disposition["artifact_kind"] == "PHASE_060_V1019_DISPOSITION_MATRIX",
            "disposition artifact kind mismatch")
    require(delta["artifact_kind"] == "PHASE_060_V1019_CARRY_FORWARD_DELTA",
            "delta artifact kind mismatch")
    require(disposition["schema_version"] == "phase060-step45-dispositions-v1",
            "disposition schema mismatch")
    require(delta["schema_version"] == "phase060-step45-carry-forward-delta-v1",
            "delta schema mismatch")

    stored_manifest = disposition["source_manifest"]
    require(all(set(row) == MANIFEST_KEYS for row in stored_manifest),
            "manifest row schema mismatch")
    require(stored_manifest == manifest, "manifest differs from independent reconstruction")
    expected_by_id = {row["source_id"]: row for row in manifest}
    rows = disposition["dispositions"]
    require(len(rows) == 173, "disposition count mismatch")
    require(all(set(row) == DISPOSITION_KEYS for row in rows),
            "disposition row schema mismatch")
    membership: list[str] = []
    disposition_ids: list[str] = []
    for row in rows:
        require(isinstance(row["source_ids"], list) and len(row["source_ids"]) == 1,
                "disposition must own exactly one source")
        source_id = row["source_ids"][0]
        membership.append(source_id)
        disposition_ids.append(row["disposition_id"])
        require(source_id in expected_by_id, f"unknown source: {source_id}")
        source = expected_by_id[source_id]
        require(row["source_family"] == source["source_family"],
                f"source family mismatch: {source_id}")
        require(row["source_record_sha256"] == source["source_record_sha256"],
                f"source hash mismatch: {source_id}")
        require(row["source_anchors"] == source["source_anchors"],
                f"source anchor mismatch: {source_id}")
        require(row["evidence_paths"][:2] == source["evidence_paths"],
                f"source evidence mismatch: {source_id}")
        require(row["primary_disposition"] in ALLOWED_DISPOSITIONS,
                f"invalid disposition: {source_id}")
        require(row["external_material_truth_validated"] is False
                and row["external_scientific_truth_validated"] is False,
                f"external truth promoted: {source_id}")
        require(row["authority_boundary"] == AUTHORITY, f"authority mismatch: {source_id}")
        require(isinstance(row["acceptance_criterion"], str)
                and row["acceptance_criterion"].strip(),
                f"missing acceptance: {source_id}")
        require(isinstance(row["affected_implementation_test_artifact"], list)
                and row["affected_implementation_test_artifact"],
                f"missing affected surface: {source_id}")
        require(isinstance(row["target_phase"], int), f"invalid target: {source_id}")
        require(61 <= row["target_phase"] <= 90, f"out-of-program target: {source_id}")
        expected_horizon = (
            "PRE_FREEZE_061_069" if row["target_phase"] <= 69
            else "CONDITIONAL_070_PLUS"
        )
        require(row["target_horizon"] == expected_horizon,
                f"target horizon mismatch: {source_id}")
        require(row["activation_gate"] == "PASS_P060_LINEAGE_C",
                f"activation gate mismatch: {source_id}")
        require(all(isinstance(phase, int) and 61 <= phase <= 90
                    for phase in row["downstream_target_phases"]),
                f"invalid downstream target: {source_id}")
    require(len(set(membership)) == 173 and set(membership) == set(expected_by_id),
            "disposition duplicate or source orphan")
    require(len(set(disposition_ids)) == 173, "duplicate disposition id")
    observed = Counter(row["primary_disposition"] for row in rows)
    require(observed == EXPECTED_DISPOSITIONS, f"disposition distribution mismatch: {observed}")
    require(sha256(record_bytes(rows)) == EXPECTED_DISPOSITION_SEMANTIC_SHA256,
            "disposition semantic digest mismatch")
    summary = disposition["gate_summary"]
    require(summary["status"] == "PASS", "disposition gate status mismatch")
    for key in (
        "source_orphan_count", "duplicate_source_identity_count",
        "duplicate_disposition_membership_count", "disposition_conflict_count",
        "external_validity_promotion_count",
    ):
        require(summary[key] == 0, f"nonzero disposition summary: {key}")
    require(summary["missing_acceptance_authority_target_affected_count"] == 0,
            "missing required disposition field summary nonzero")
    require(summary["source_expected"] == 173 and summary["disposition_count"] == 173,
            "disposition summary count mismatch")
    require(Counter(summary["primary_disposition_counts"]) == EXPECTED_DISPOSITIONS,
            "disposition summary distribution mismatch")
    require(sha256(record_bytes(summary)) == EXPECTED_DISPOSITION_GATE_SHA256,
            "disposition gate-summary semantic digest mismatch")

    carry = delta["inherited_items"]
    require(len(prior_items) == 52 and len(carry) == 52, "carry count mismatch")
    require(all(set(row) == CARRY_KEYS for row in carry), "carry row schema mismatch")
    prior_by_id = {row["carry_forward_id"]: row for row in prior_items}
    require(len(prior_by_id) == 52, "prior carry duplicate")
    observed_ids: list[str] = []
    pairs = (
        ("status_before", "status_after", "status"),
        ("acceptance_criterion_before", "acceptance_criterion_after", "acceptance_criterion"),
        ("activation_gate_before", "activation_gate_after", "activation_gate"),
        ("authority_boundary_before", "authority_boundary_after", "authority_boundary"),
        ("category_before", "category_after", "category"),
        ("target_horizon_before", "target_horizon_after", "target_horizon"),
        ("target_phase_before", "target_phase_after", "target_phase"),
    )
    for row in carry:
        carry_id = row["carry_forward_id"]
        observed_ids.append(carry_id)
        require(carry_id in prior_by_id, f"unknown carry id: {carry_id}")
        prior = prior_by_id[carry_id]
        require(row["prior_record"] == prior, f"prior record mutation: {carry_id}")
        require(row["prior_record_sha256"] == sha256(record_bytes(prior)),
                f"prior hash mismatch: {carry_id}")
        require(row["source_route_source_id"] == prior["source_route"]["source_id"],
                f"source route mismatch: {carry_id}")
        for before, after, source_key in pairs:
            require(row[before] == prior[source_key] and row[after] == prior[source_key],
                    f"carry field changed: {carry_id}/{source_key}")
        require(row["acceptance_satisfied"] is False, f"false closure: {carry_id}")
        require(row["resolution_status"] == "NOT_RESOLVED", f"false resolution: {carry_id}")
        require(row["delta_status"] in {"TOUCHED_NEW_EVIDENCE", "UNCHANGED"},
                f"invalid delta: {carry_id}")
        require(row["external_material_truth_validated"] is False
                and row["external_scientific_truth_validated"] is False,
                f"external carry promotion: {carry_id}")
    require(len(set(observed_ids)) == 52 and set(observed_ids) == set(prior_by_id),
            "carry duplicate or orphan")
    require(Counter(row["status_after"] for row in carry)
            == Counter({"OPEN": 41, "PRESERVED_ACTIVE": 11}),
            "carry status distribution mismatch")
    require(Counter(row["delta_status"] for row in carry)
            == Counter({"TOUCHED_NEW_EVIDENCE": 33, "UNCHANGED": 19}),
            "carry touch distribution mismatch")
    require(sha256(record_bytes(carry)) == EXPECTED_CARRY_SEMANTIC_SHA256,
            "carry semantic digest mismatch")

    blockers = delta["new_blockers"]
    require(len(blockers) == 5 and all(set(row) == BLOCKER_KEYS for row in blockers),
            "blocker schema/count mismatch")
    blocker_ids = [row["blocker_id"] for row in blockers]
    require(len(set(blocker_ids)) == 5, "duplicate blocker")
    require({row["blocker_id"]: row["target_phase"] for row in blockers}
            == EXPECTED_BLOCKERS, "blocker identity/target mismatch")
    require(not (set(blocker_ids) & set(prior_by_id)), "blocker/carry collision")
    require(not (set(blocker_ids) & set(expected_by_id)), "blocker/source collision")
    for row in blockers:
        require(row["status"] == "OPEN", f"blocker status mismatch: {row['blocker_id']}")
        require(row["external_material_truth_validated"] is False
                and row["external_scientific_truth_validated"] is False,
                f"external blocker promotion: {row['blocker_id']}")
        require(isinstance(row["acceptance_criterion"], str)
                and row["acceptance_criterion"].strip(),
                f"missing blocker acceptance: {row['blocker_id']}")
        expected_horizon = (
            "PRE_FREEZE_061_069" if row["target_phase"] <= 69
            else "CONDITIONAL_070_PLUS"
        )
        require(row["target_horizon"] == expected_horizon,
                f"blocker horizon mismatch: {row['blocker_id']}")
        require(row["activation_gate"] == "PASS_P060_LINEAGE_C",
                f"blocker activation mismatch: {row['blocker_id']}")
    require(sha256(record_bytes(blockers)) == EXPECTED_BLOCKER_SEMANTIC_SHA256,
            "blocker semantic digest mismatch")
    delta_summary = delta["gate_summary"]
    require(delta_summary["status"] == "PASS", "delta gate status mismatch")
    require(delta_summary["carry_forward_expected"] == 52, "delta count summary mismatch")
    require(delta_summary["acceptance_satisfied_count"] == 0, "delta false acceptance")
    require(delta_summary["new_blocker_count"] == 5, "delta blocker summary mismatch")
    require(delta_summary["external_validity_promotion_count"] == 0,
            "delta external summary mismatch")
    require(delta_summary["status_after_counts"] == {"OPEN": 41, "PRESERVED_ACTIVE": 11},
            "delta status summary mismatch")
    require(delta_summary["delta_status_counts"]
            == {"TOUCHED_NEW_EVIDENCE": 33, "UNCHANGED": 19},
            "delta touch summary mismatch")
    require(delta_summary["resolution_status_counts"] == {"NOT_RESOLVED": 52},
            "delta resolution summary mismatch")
    require(sha256(record_bytes(delta_summary)) == EXPECTED_DELTA_GATE_SHA256,
            "delta gate-summary semantic digest mismatch")


def validate_import_boundary(
    source: str, allowed_import_roots: set[str], role: str,
) -> ast.Module:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                require(root in allowed_import_roots,
                        f"{role} non-allowlisted import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            require(root in allowed_import_roots,
                    f"{role} non-allowlisted import-from: {module}")
        if isinstance(node, ast.Name):
            require(node.id not in {
                "__builtins__", "__import__", "compile", "eval", "exec",
                "importlib", "runpy",
            }, f"{role} dynamic execution/import name: {node.id}")
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "getattr" and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)):
            require(node.args[1].value not in {
                "__import__", "compile", "eval", "exec", "import_module", "run_path",
            }, f"{role} dynamic getattr target: {node.args[1].value}")
        if isinstance(node, ast.Attribute):
            require(node.attr not in {"import_module", "run_path"},
                    f"{role} dynamic module execution attribute: {node.attr}")
    return tree


def validate_builder_source_policy(source: str, enforce_digest: bool) -> None:
    if enforce_digest:
        require(sha256(source.encode("utf-8")) == EXPECTED_BUILDER_SHA256,
                "reviewed builder source digest mismatch")
    tree = validate_import_boundary(
        source,
        {"__future__", "argparse", "collections", "hashlib", "json", "math",
         "pathlib", "subprocess", "typing"},
        "builder",
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess":
                    require(alias.asname is None,
                            "builder subprocess module import may not be aliased")
        if isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            raise ValidationError("builder subprocess from-import is prohibited")
    subprocess_methods = {"Popen", "call", "check_call", "check_output", "run"}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
                and node.func.attr in subprocess_methods):
            require(node.args and isinstance(node.args[0], (ast.List, ast.Tuple)),
                    "builder subprocess argv must be a literal list/tuple")
            argv = node.args[0].elts
            require(argv and isinstance(argv[0], ast.Constant) and argv[0].value == "git",
                    "builder subprocess executable is not allowlisted git")
            for keyword in node.keywords:
                if keyword.arg == "shell":
                    require(isinstance(keyword.value, ast.Constant)
                            and keyword.value.value is False,
                            "builder subprocess shell must be false")


def validate_validator_source_policy(source: str) -> None:
    validate_import_boundary(
        source,
        {"__future__", "ast", "collections", "copy", "hashlib", "json", "math",
         "os", "pathlib", "subprocess", "sys", "tempfile", "typing"},
        "validator",
    )


def validate_validator_independence() -> None:
    validate_validator_source_policy(Path(__file__).read_text(encoding="utf-8"))


def reject_builder_production_imports() -> None:
    validate_builder_source_policy(
        BUILDER_PATH.read_text(encoding="utf-8"), enforce_digest=True
    )
    validate_validator_independence()


def validate_collision_policy_source(source: str) -> None:
    tree = ast.parse(source)
    baseline_values = []
    grep_lists: list[ast.List] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name)
                        and target.id == "PRE_STEP45_COMMIT" for target in node.targets)
                and isinstance(node.value, ast.Constant)):
            baseline_values.append(node.value.value)
        if isinstance(node, ast.List):
            constants = [element.value for element in node.elts
                         if isinstance(element, ast.Constant)]
            if "git" in constants and "grep" in constants:
                grep_lists.append(node)
    require(baseline_values == [PRE_STEP45_COMMIT],
            "builder collision baseline constant mismatch")
    require(len(grep_lists) == 1, "builder collision grep command is not unique")
    grep_names = [element.id for element in grep_lists[0].elts
                  if isinstance(element, ast.Name)]
    grep_constants = [element.value for element in grep_lists[0].elts
                      if isinstance(element, ast.Constant)]
    require("PRE_STEP45_COMMIT" in grep_names,
            "builder collision grep does not use immutable pre-Step45 baseline")
    require("HEAD" not in grep_constants,
            "builder collision grep incorrectly uses moving HEAD")


def validate_post_commit_collision_fixture() -> None:
    source = BUILDER_PATH.read_text(encoding="utf-8")
    validate_collision_policy_source(source)
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PRE_STEP45_COMMIT, "HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    require(ancestor.returncode == 0, "pre-Step45 collision baseline is not HEAD ancestor")
    current_step45_bytes = (
        BUILDER_PATH.read_bytes() + DISPOSITION_PATH.read_bytes() + DELTA_PATH.read_bytes()
    )
    for blocker_id in EXPECTED_BLOCKERS:
        require(blocker_id.encode("ascii") in current_step45_bytes,
                f"post-commit fixture lacks emitted blocker id: {blocker_id}")
        collision = subprocess.run(
            ["git", "grep", "-n", "-F", blocker_id, PRE_STEP45_COMMIT, "--", "Codex"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        require(collision.returncode == 1,
                f"blocker collides in pre-Step45 baseline: {blocker_id}")


def deterministic_rebuild(current_disposition: bytes, current_delta: bytes) -> None:
    reject_builder_production_imports()
    validate_post_commit_collision_fixture()
    with tempfile.TemporaryDirectory(prefix="p060_step45_validate_") as tmp:
        tmp_path = Path(tmp)
        outputs: list[tuple[bytes, bytes]] = []
        for run in (1, 2):
            disposition_path = tmp_path / f"disposition_{run}.json"
            delta_path = tmp_path / f"delta_{run}.json"
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            process = subprocess.run(
                [sys.executable, str(BUILDER_PATH),
                 "--disposition-output", str(disposition_path),
                 "--delta-output", str(delta_path)],
                cwd=ROOT, env=env, capture_output=True, text=True, check=False,
            )
            require(process.returncode == 0,
                    f"builder run {run} failed: {process.stdout}{process.stderr}")
            outputs.append((disposition_path.read_bytes(), delta_path.read_bytes()))
        require(outputs[0] == outputs[1], "builder output nondeterministic")
        require(outputs[0][0] == current_disposition, "disposition differs from rebuild")
        require(outputs[0][1] == current_delta, "delta differs from rebuild")


def run_negative_controls(
    disposition: dict[str, Any], delta: dict[str, Any],
    metadata: list[dict[str, Any]], manifest: list[dict[str, Any]],
    prior_items: list[dict[str, Any]],
) -> tuple[int, int]:
    controls: list[tuple[str, Callable[[], None]]] = [
        ("duplicate_json_key", lambda: strict_load_bytes(b'{"x":1,"x":2}')),
        ("nonfinite_json", lambda: strict_load_bytes(b'{"x":NaN}')),
    ]
    builder_source = BUILDER_PATH.read_text(encoding="utf-8")
    validator_source = Path(__file__).read_text(encoding="utf-8")
    controls.append((
        "builder_digest_pin",
        lambda: validate_builder_source_policy(builder_source + "\n# digest mutation\n", True),
    ))
    controls.append((
        "builder_to_validator_import",
        lambda: validate_builder_source_policy(
            builder_source + "\nimport validate_phase060_step45_dispositions\n", False
        ),
    ))
    controls.append((
        "validator_to_builder_import",
        lambda: validate_validator_source_policy(
            validator_source + "\nimport build_phase060_step45_dispositions\n"
        ),
    ))
    controls.append((
        "moving_head_collision_baseline",
        lambda: validate_collision_policy_source(
            builder_source.replace(
                "blocker_id, PRE_STEP45_COMMIT", 'blocker_id, "HEAD"', 1
            )
        ),
    ))

    def add(name: str, mutate: Callable[[dict[str, Any], dict[str, Any]], None]) -> None:
        def execute() -> None:
            left, right = copy.deepcopy(disposition), copy.deepcopy(delta)
            mutate(left, right)
            validate_payloads(left, right, metadata, manifest, prior_items)
        controls.append((name, execute))

    add("missing_disposition", lambda a, _b: a["dispositions"].pop())
    add("duplicate_disposition", lambda a, _b: a["dispositions"].append(copy.deepcopy(a["dispositions"][0])))
    add("invalid_disposition", lambda a, _b: a["dispositions"][0].__setitem__("primary_disposition", "ACCEPT"))
    add("scientific_promotion", lambda a, _b: a["dispositions"][0].__setitem__("external_scientific_truth_validated", True))
    add("material_promotion", lambda a, _b: a["dispositions"][0].__setitem__("external_material_truth_validated", True))
    add("fingerprint_mismatch", lambda a, _b: a["inputs"][0].__setitem__("sha256", "0" * 64))
    add("source_hash_mismatch", lambda a, _b: a["dispositions"][0].__setitem__("source_record_sha256", "0" * 64))
    add("missing_carry", lambda _a, b: b["inherited_items"].pop())
    add("carry_status_change", lambda _a, b: b["inherited_items"][0].__setitem__("status_after", "RESOLVED"))
    add("carry_acceptance", lambda _a, b: b["inherited_items"][0].__setitem__("acceptance_satisfied", True))
    add("carry_resolution", lambda _a, b: b["inherited_items"][0].__setitem__("resolution_status", "RESOLVED"))
    add("carry_prior_record", lambda _a, b: b["inherited_items"][0]["prior_record"].__setitem__("status", "RESOLVED"))
    add("missing_blocker", lambda _a, b: b["new_blockers"].pop())
    add("duplicate_blocker", lambda _a, b: b["new_blockers"].append(copy.deepcopy(b["new_blockers"][0])))
    add("blocker_collision", lambda _a, b: b["new_blockers"][0].__setitem__("blocker_id", b["inherited_items"][0]["carry_forward_id"]))
    add("blocker_target", lambda _a, b: b["new_blockers"][0].__setitem__("target_phase", 999))
    add("summary_promotion", lambda a, _b: a["gate_summary"].__setitem__("external_validity_promotion_count", 1))
    add("manifest_orphan", lambda a, _b: a["source_manifest"].pop())

    def swap_source_membership(a: dict[str, Any], _b: dict[str, Any]) -> None:
        left = a["dispositions"][0]["source_ids"]
        right = a["dispositions"][1]["source_ids"]
        a["dispositions"][0]["source_ids"] = right
        a["dispositions"][1]["source_ids"] = left

    def mutate_prior_target_with_hash(_a: dict[str, Any], b: dict[str, Any]) -> None:
        row = b["inherited_items"][0]
        row["prior_record"]["target_phase"] = 90
        row["prior_record_sha256"] = sha256(record_bytes(row["prior_record"]))

    def mutate_prior_acceptance_with_hash(_a: dict[str, Any], b: dict[str, Any]) -> None:
        row = b["inherited_items"][0]
        row["prior_record"]["acceptance_criterion"] = "mutated prior acceptance"
        row["prior_record_sha256"] = sha256(record_bytes(row["prior_record"]))

    add("source_membership_swap", swap_source_membership)
    add("empty_disposition_authority",
        lambda a, _b: a["dispositions"][0].__setitem__("authority_boundary", ""))
    add("empty_affected_surface",
        lambda a, _b: a["dispositions"][0].__setitem__(
            "affected_implementation_test_artifact", []
        ))
    add("missing_disposition_target",
        lambda a, _b: a["dispositions"][0].__setitem__("target_phase", None))
    add("disposition_horizon_mutation",
        lambda a, _b: a["dispositions"][0].__setitem__(
            "target_horizon", "CONDITIONAL_070_PLUS"
        ))
    add("disposition_activation_mutation",
        lambda a, _b: a["dispositions"][0].__setitem__("activation_gate", "BYPASS"))
    add("duplicate_carry",
        lambda _a, b: b["inherited_items"].append(copy.deepcopy(b["inherited_items"][0])))
    add("prior_target_rehashed_mutation", mutate_prior_target_with_hash)
    add("prior_acceptance_rehashed_mutation", mutate_prior_acceptance_with_hash)
    add("unknown_touch_source",
        lambda _a, b: b["inherited_items"][0]["touch_source_ids"].append("UNKNOWN"))
    add("unanchored_touch_evidence",
        lambda _a, b: b["inherited_items"][0]["touch_evidence_paths"].append("unanchored"))
    add("blocker_category_mutation",
        lambda _a, b: b["new_blockers"][0].__setitem__("category", "UNKNOWN"))
    add("blocker_non_double_count_basis_mutation",
        lambda _a, b: b["new_blockers"][0].__setitem__(
            "non_double_count_basis", "mutated basis"
        ))
    add("blocker_collision_candidates_mutation",
        lambda _a, b: b["new_blockers"][0]["old_collision_candidates"].append("UNKNOWN"))

    def swap_dispositions(a: dict[str, Any], _b: dict[str, Any]) -> None:
        left = a["dispositions"][0]["primary_disposition"]
        right = a["dispositions"][1]["primary_disposition"]
        a["dispositions"][0]["primary_disposition"] = right
        a["dispositions"][1]["primary_disposition"] = left

    def swap_targets(a: dict[str, Any], _b: dict[str, Any]) -> None:
        left = a["dispositions"][0]["target_phase"]
        right = a["dispositions"][1]["target_phase"]
        a["dispositions"][0]["target_phase"] = right
        a["dispositions"][1]["target_phase"] = left

    def swap_touch_status(_a: dict[str, Any], b: dict[str, Any]) -> None:
        left = b["inherited_items"][0]["delta_status"]
        right = b["inherited_items"][2]["delta_status"]
        b["inherited_items"][0]["delta_status"] = right
        b["inherited_items"][2]["delta_status"] = left

    add("disposition_semantic_swap", swap_dispositions)
    add("target_semantic_swap", swap_targets)
    add("carry_touch_semantic_swap", swap_touch_status)
    add("blocker_acceptance_semantic_mutation",
        lambda _a, b: b["new_blockers"][0].__setitem__(
            "acceptance_criterion", "mutated but nonempty"
        ))
    add("disposition_acceptance_semantic_mutation",
        lambda a, _b: a["dispositions"][0].__setitem__(
            "acceptance_criterion", "mutated but nonempty"
        ))
    add("disposition_unrelated_evidence",
        lambda a, _b: a["dispositions"][0]["evidence_paths"].append("unrelated"))
    add("carry_touch_sources_erased",
        lambda _a, b: b["inherited_items"][0].__setitem__("touch_source_ids", []))
    add("blocker_source_membership_erased",
        lambda _a, b: b["new_blockers"][0].__setitem__("source_ids", []))
    add("blocker_authority_mutation",
        lambda _a, b: b["new_blockers"][0].__setitem__(
            "authority_boundary", "internal but mutated"
        ))
    add("carry_missing_summary_mutation",
        lambda _a, b: b["gate_summary"].__setitem__("carry_forward_missing_count", 1))
    add("generation_builder_mutation",
        lambda a, b: (a["generation"].__setitem__("builder", "wrong-builder.py"),
                      b["generation"].__setitem__("builder", "wrong-builder.py")))
    add("generation_canonical_mutation",
        lambda a, b: (a["generation"].__setitem__("canonical_json", "wrong-format"),
                      b["generation"].__setitem__("canonical_json", "wrong-format")))
    add("generation_extra_key",
        lambda a, _b: a["generation"].__setitem__("unexpected", False))
    add("generation_missing_key",
        lambda _a, b: b["generation"].pop("builder"))

    for name, fixture in (
        ("builder_runpy_bypass", "\nimport runpy\nrunpy.run_path('production.py')\n"),
        ("builder_subprocess_python_bypass",
         "\nsubprocess.run([sys.executable, 'production.py'])\n"),
        ("builder_import_module_alias_bypass",
         "\nfrom importlib import import_module as load\nload('production')\n"),
        ("builder_getattr_importlib_bypass",
         "\nimport importlib\ngetattr(importlib, 'import_module')('production')\n"),
        ("builder_getattr_builtin_import_bypass",
         "\ngetattr(__builtins__, '__import__')('production')\n"),
        ("builder_eval_alias_bypass", "\nexecute = eval\nexecute('1 + 1')\n"),
        ("builder_subprocess_from_import_alias_bypass",
         "\nfrom subprocess import run as launch\n"
         "launch(['python', 'Claude/production.py'])\n"),
        ("builder_subprocess_module_alias_bypass",
         "\nimport subprocess as sp\nsp.run(['python', 'Claude/production.py'])\n"),
    ):
        controls.append((
            name,
            lambda fixture=fixture: validate_builder_source_policy(
                builder_source + fixture, enforce_digest=False
            ),
        ))

    passed = 0
    for name, control in controls:
        try:
            control()
        except (ValidationError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            passed += 1
        else:
            raise ValidationError(f"negative control accepted: {name}")
    return passed, len(controls)


def main() -> int:
    try:
        require(DISPOSITION_PATH.is_file(), "missing disposition artifact")
        require(DELTA_PATH.is_file(), "missing delta artifact")
        disposition_raw = DISPOSITION_PATH.read_bytes()
        delta_raw = DELTA_PATH.read_bytes()
        disposition = strict_load_bytes(disposition_raw)
        delta = strict_load_bytes(delta_raw)
        require(canonical_bytes(disposition) == disposition_raw,
                "disposition is not canonical JSON")
        require(canonical_bytes(delta) == delta_raw, "delta is not canonical JSON")
        inputs, metadata = load_inputs()
        manifest = reconstruct_manifest(inputs)
        prior_items = inputs[P59_REGISTER]["items"]
        validate_payloads(disposition, delta, metadata, manifest, prior_items)
        negative_passed, negative_total = run_negative_controls(
            disposition, delta, metadata, manifest, prior_items
        )
        deterministic_rebuild(disposition_raw, delta_raw)
    except (ValidationError, ValueError, KeyError, TypeError, OSError,
            UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"FAIL {error}")
        print("FAIL_P060_STEP45_DISPOSITIONS")
        return 1
    print("PASS schema/counts/distribution")
    print(f"PASS negative_controls={negative_passed}/{negative_total}")
    print("PASS determinism=2/2 production_imported=false")
    print("PASS_P060_STEP45_DISPOSITIONS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
