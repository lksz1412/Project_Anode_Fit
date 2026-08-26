#!/usr/bin/env python3
"""Build Phase 061 Step 51.1 source-disposition and carry-forward artifacts.

The builder consumes only frozen Phase 061 audit artifacts and the Phase 060
carry-forward baseline.  It does not import or execute any Claude production,
test, rendering, or snapshot-generation module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
STEP50_COMMIT = "a90c6e8659f4fcd24945af81e50c712bbc71ef30"
ACTIVATION_GATE = "PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS"
INPUT_ARTIFACT_COMMIT = STEP50_COMMIT
AUTHORITY_BOUNDARY = {
    "ceiling": "INTERNAL_LINEAGE_DISPOSITION_ONLY",
    "external_material_truth": False,
    "external_scientific_truth": False,
    "frozen_source_mutation": False,
    "primary_literature_truth": False,
}
ALLOWED_DISPOSITIONS = (
    "PRESERVE",
    "CORRECT",
    "DISCARD",
    "SUPERSEDE",
    "COMPETING_ONLY",
    "UNVERIFIED",
)

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
    TOPOLOGY,
    STEP46_RESULT,
    PROCESS,
    STEP47_RESULT,
    LINEAGE,
    STEP48_RESULT,
    CITATION,
    STEP49_RESULT,
    REVIEW,
    VISUAL,
    STEP50_RESULT,
    P60_DISPOSITION,
    P60_DELTA,
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

DEFAULT_DISPOSITION_OUTPUT = ROOT / "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json"
DEFAULT_DELTA_OUTPUT = ROOT / "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json"


class DuplicateKey(ValueError):
    """Raised when strict JSON parsing finds a repeated object key."""


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise DuplicateKey(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def ensure_finite(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"nonfinite JSON number at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            ensure_finite(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            ensure_finite(child, f"{path}[{index}]")


def strict_load(raw: bytes) -> Any:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicates,
        parse_constant=reject_constant,
    )
    ensure_finite(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def record_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def physical_lines(raw: bytes) -> int:
    return 0 if not raw else raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def read_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parsed: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for relative in INPUT_PATHS:
        raw = (ROOT / relative).read_bytes()
        if sha256(raw) != EXPECTED_INPUT_SHA256[relative]:
            raise ValueError(f"input fingerprint changed: {relative}")
        if relative.endswith(".json"):
            parsed[relative] = strict_load(raw)
            parse_mode = "STRICT_JSON_FULL_TRAVERSAL_DUPLICATE_KEY_AND_NONFINITE_REJECTED"
        else:
            parsed[relative] = raw.decode("utf-8")
            parse_mode = "FULL_UTF8_TEXT"
        metadata.append(
            {
                "bytes": len(raw),
                "git_blob_sha1": git_blob_sha1(raw),
                "git_commit": INPUT_ARTIFACT_COMMIT,
                "parse_mode": parse_mode,
                "path": relative,
                "physical_lines": physical_lines(raw),
                "sha256": sha256(raw),
            }
        )
    return parsed, metadata


def source_number(source_id: str) -> int:
    return int(source_id.rsplit("-", 1)[1])


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
            route = {
                "artifact_path": artifact_path,
                "json_pointer": pointer,
                "record_sha256": record_hash,
            }
            if route not in catalog[evidence_id]:
                catalog[evidence_id].append(route)
    return catalog


def preferred_evidence_path(evidence_id: str) -> str:
    if evidence_id.startswith("P060-") or evidence_id.startswith("P059-"):
        return P60_DELTA
    if evidence_id.startswith("P061-STEP50-"):
        return REVIEW
    if evidence_id.startswith("P061-STEP49-"):
        return CITATION
    if evidence_id.startswith("P061-STEP48-") or evidence_id.startswith("P061-DELTA-"):
        return LINEAGE
    if evidence_id.startswith(("P061-CON-", "P061-GNF-", "P061-UNV-")):
        return PROCESS
    if evidence_id.startswith("P061-SRC-"):
        return TOPOLOGY
    return CITATION


def route_role(path: str) -> str:
    return {
        TOPOLOGY: "SOURCE_IDENTITY",
        PROCESS: "PROCESS_AUTHORITY",
        LINEAGE: "LINEAGE_DELTA_OR_DEBT",
        CITATION: "CITATION_AUTHORITY_OR_DEBT",
        REVIEW: "REVIEW_OR_VISUAL_DEBT",
        P60_DELTA: "INHERITED_CARRY_OR_BLOCKER",
    }.get(path, "BOUNDED_CONTEXT")


def evidence_routes_for(
    source: dict[str, Any], indexes: dict[str, Any], evidence_ids: list[str],
) -> list[dict[str, Any]]:
    source_id = source["source_id"]
    ordinal = source["manifest_index_v1020"] - 1
    routes = [
        {
            "artifact_path": TOPOLOGY,
            "evidence_ids": [source_id],
            "json_pointer": f"/sources/{ordinal}",
            "record_sha256": sha256(record_bytes(source)),
            "route_role": "SOURCE_IDENTITY",
        },
        {
            "artifact_path": LINEAGE,
            "evidence_ids": [indexes["delta_by_id"][source_id]["delta_id"]],
            "json_pointer": f"/delta_rows/{ordinal}",
            "record_sha256": sha256(record_bytes(indexes["delta_by_id"][source_id])),
            "route_role": "LINEAGE_DELTA_OR_DEBT",
        },
    ]
    for evidence_id in evidence_ids:
        if evidence_id in {source_id, indexes["delta_by_id"][source_id]["delta_id"]}:
            continue
        candidates = indexes["evidence_catalog"].get(evidence_id, [])
        preferred = preferred_evidence_path(evidence_id)
        matches = [candidate for candidate in candidates if candidate["artifact_path"] == preferred]
        if not matches:
            raise ValueError(f"no preferred evidence anchor for {source_id}:{evidence_id}:{preferred}")
        selected = matches[0]
        routes.append({
            **selected,
            "evidence_ids": [evidence_id],
            "route_role": route_role(selected["artifact_path"]),
        })
    return sorted(
        routes,
        key=lambda row: (row["artifact_path"], row["json_pointer"], row["evidence_ids"]),
    )


SUPERSEDE_EVIDENCE: dict[str, tuple[str, ...]] = {}

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
    "P061-SRC-0064",
    "P061-SRC-0065",
    "P061-SRC-0066",
    "P061-SRC-0067",
    "P061-SRC-0090",
    "P061-SRC-0091",
    "P061-SRC-0092",
    "P061-SRC-0093",
}

COMPETING_SOURCE_OVERRIDES = {"P061-SRC-0043", "P061-SRC-0044"}
COMPETITIVE_REVIEW_PRESERVE = {
    f"P061-SRC-{index:04d}" for index in range(193, 205)
}

CORRECTION_TARGETS = {
    "P061-STEP49-FINDING-001": 72,
    "P061-STEP49-FINDING-002": 71,
    "P061-STEP49-FINDING-003": 71,
    "P061-STEP49-FINDING-004": 72,
    "P061-STEP50-P2-008": 62,
    "P061-STEP50-P2-009": 62,
    "P061-STEP50-P2-010": 62,
    "P061-CON-004": 62,
    "P061-CON-006": 62,
    "P061-CON-007": 62,
    "P061-CON-010": 62,
    "P061-STEP50-P1-001": 62,
    "P060-BD-NEW-003": 81,
    "P060-BD-NEW-005": 67,
}

P61_DIRECT_CARRY_EVIDENCE: dict[str, tuple[str, ...]] = {
    "P059-CFR-CF-08": ("P061-STEP48-GNF-002", "P061-STEP48-GNF-004"),
    "P059-CFR-CF-11": (
        "P061-CON-004",
        "P061-CON-006",
        "P061-CON-007",
        "P061-CON-010",
        "P061-STEP50-P1-001",
    ),
    "P059-CFR-RM-011": tuple(f"P061-STEP49-NEW-SOURCE-{index:03d}" for index in range(1, 9)),
    "P059-CFR-NS-05": ("P061-STEP49-GNF-001", "P061-STEP49-UNV-001"),
    "P059-CFR-ED-03": ("P061-STEP49-GNF-001", "P061-STEP49-UNV-003"),
    "P059-CFR-BD-NEW-003": ("P061-STEP49-GNF-002", "P061-STEP49-UNV-002"),
    "P059-CFR-RB-11": ("P061-STEP48-UNV-001", "P061-STEP48-UNV-002"),
    "P059-CFR-RB-12": (
        "P061-STEP50-P1-002",
        "P061-STEP50-P1-003",
        "P061-STEP50-P2-002",
        "P061-STEP50-P2-003",
        "P061-STEP50-P2-004",
        "P061-STEP50-P2-005",
        "P061-STEP50-P2-006",
        "P061-STEP50-P2-007",
        "P061-STEP50-P2-008",
        "P061-STEP50-P2-009",
        "P061-STEP50-P2-010",
    ),
    "P059-CFR-RB-13": ("P061-STEP49-FINDING-001",),
    "P059-CFR-ED-04": (
        "P061-STEP48-GNF-001",
        "P061-STEP48-GNF-003",
        "P061-STEP48-UNV-006",
        "P061-STEP48-UNV-007",
    ),
}

P61_DIRECT_BLOCKER_EVIDENCE: dict[str, tuple[str, ...]] = {
    "P060-BD-NEW-001": ("P061-SRC-0005", "P061-SRC-0023"),
    "P060-BD-NEW-002": ("P061-SRC-0001", "P061-SRC-0004"),
    "P060-BD-NEW-003": ("P061-SRC-0029", "P061-SRC-0039", "P061-SRC-0040"),
    "P060-BD-NEW-004": ("P061-SRC-0006", "P061-STEP49-GNF-001"),
    "P060-BD-NEW-005": ("P061-SRC-0017", "P061-SRC-0040"),
}

REFINED_CARRY_IDS = {
    "P059-CFR-CF-11",
    "P059-CFR-RM-011",
    "P059-CFR-NS-05",
    "P059-CFR-ED-03",
    "P059-CFR-BD-NEW-003",
    "P059-CFR-RB-12",
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

# debt_id|route_state|owner_type|owner_id|duplicate_or_refinement_of|corroborating_owner_ids
DEBT_ROUTE_TABLE = """
P061-CON-001|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-002|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|P060-BD-NEW-001
P061-CON-003|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-004|OPEN|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-005|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-006|OPEN|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-007|OPEN|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-008|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-CON-009|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-CON-010|OPEN|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-GNF-001|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-GNF-002|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-GNF-003|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-GNF-004|OPEN|SOURCE_DISPOSITION|P061-DISP-0044|-|-
P061-GNF-005|OPEN|PHASE061_BLOCKER|P061-BD-NEW-001|-|P059-CFR-RB-12
P061-GNF-006|OPEN|PHASE061_BLOCKER|P061-BD-NEW-001|-|P059-CFR-CF-11
P061-GNF-007|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-UNV-001|OPEN|INHERITED_CARRY|P059-CFR-NS-05|-|-
P061-UNV-002|OPEN|INHERITED_CARRY|P059-CFR-NS-01|-|-
P061-UNV-003|OPEN|INHERITED_CARRY|P059-CFR-RB-11|-|-
P061-UNV-004|OPEN|INHERITED_CARRY|P059-CFR-BD-NEW-003|-|-
P061-UNV-005|OPEN|PHASE061_BLOCKER|P061-BD-NEW-002|-|P059-CFR-RB-12,P059-CFR-NS-01
P061-UNV-006|OPEN|PHASE061_BLOCKER|P061-BD-NEW-003|-|P059-CFR-RM-007,P059-CFR-NS-01
P061-UNV-007|OPEN|PHASE061_BLOCKER|P061-BD-NEW-001|-|P059-CFR-CF-11,P061-DISP-0065,P061-DISP-0066,P061-DISP-0067
P061-UNV-008|OPEN_DUPLICATE_ALIAS|SOURCE_DISPOSITION|P061-DISP-0044|P061-GNF-004|-
P061-UNV-009|OPEN_DUPLICATE_ALIAS|PHASE061_BLOCKER|P061-BD-NEW-001|P061-GNF-005|P059-CFR-RB-12
P061-UNV-010|OPEN_DUPLICATE_ALIAS|PHASE061_BLOCKER|P061-BD-NEW-001|P061-GNF-006|P059-CFR-CF-11
P061-UNV-011|OPEN_DUPLICATE_ALIAS|INHERITED_CARRY|P059-CFR-ED-04|P061-GNF-007|-
P061-STEP48-GNF-001|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-STEP48-GNF-002|OPEN|INHERITED_CARRY|P059-CFR-CF-08|-|-
P061-STEP48-GNF-003|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-STEP48-GNF-004|OPEN|INHERITED_CARRY|P059-CFR-CF-08|-|-
P061-STEP48-GNF-005|OPEN_DUPLICATE_ALIAS|SOURCE_DISPOSITION|P061-DISP-0044|P061-GNF-004|-
P061-STEP48-UNV-001|OPEN|INHERITED_CARRY|P059-CFR-RB-11|-|-
P061-STEP48-UNV-002|OPEN|INHERITED_CARRY|P059-CFR-RB-11|-|-
P061-STEP48-UNV-003|OPEN_DUPLICATE_ALIAS|INHERITED_CARRY|P059-CFR-NS-05|P061-UNV-001|-
P061-STEP48-UNV-004|OPEN_DUPLICATE_ALIAS|INHERITED_CARRY|P059-CFR-BD-NEW-003|P061-UNV-004|-
P061-STEP48-UNV-005|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-002|P061-UNV-005|P059-CFR-RB-12
P061-STEP48-UNV-006|OPEN|INHERITED_CARRY|P059-CFR-ED-04|-|-
P061-STEP48-UNV-007|OPEN|INHERITED_CARRY|P059-CFR-ED-05|-|-
P061-STEP48-UNV-008|OPEN_DUPLICATE_ALIAS|SOURCE_DISPOSITION|P061-DISP-0044|P061-GNF-004|-
P061-STEP49-FINDING-001|OPEN|INHERITED_CARRY|P059-CFR-RB-13|-|-
P061-STEP49-FINDING-002|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-BD-NEW-003|P061-UNV-004|-
P061-STEP49-FINDING-003|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-BD-NEW-003|P061-UNV-004|P059-CFR-RB-11
P061-STEP49-FINDING-004|OPEN|INHERITED_CARRY|P059-CFR-RB-13|-|-
P061-STEP49-FINDING-005|RESOLVED_INFORMATIONAL|INHERITED_CARRY|P059-CFR-CF-11|-|-
P061-STEP49-GNF-001|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-NS-05|P061-UNV-001|P059-CFR-ED-03,P060-BD-NEW-004
P061-STEP49-GNF-002|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-BD-NEW-003|P061-UNV-004|-
P061-STEP49-UNV-001|OPEN_DUPLICATE_ALIAS|INHERITED_CARRY|P059-CFR-NS-05|P061-UNV-001|P059-CFR-ED-03
P061-STEP49-UNV-002|OPEN_DUPLICATE_ALIAS|INHERITED_CARRY|P059-CFR-BD-NEW-003|P061-UNV-004|-
P061-STEP49-UNV-003|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-ED-03|P061-UNV-001|P059-CFR-NS-05
P061-STEP49-NEW-SOURCE-001|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-002|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-003|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-004|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-005|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-006|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-007|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP49-NEW-SOURCE-008|OPEN|INHERITED_CARRY|P059-CFR-RM-011|-|-
P061-STEP50-P1-001|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-CF-11|P061-CON-004|-
P061-STEP50-P1-002|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P1-003|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-001|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-CF-11|P061-CON-004|-
P061-STEP50-P2-002|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-003|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-004|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-005|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-006|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-007|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-008|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-009|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-010|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-P2-011|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-BD-NEW-003|P061-UNV-004|P059-CFR-CF-11
P061-STEP50-GNF-001|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-001|P061-GNF-006|P059-CFR-CF-11
P061-STEP50-GNF-002|OPEN_DUPLICATE_ALIAS|PHASE061_BLOCKER|P061-BD-NEW-001|P061-GNF-005|P059-CFR-RB-12
P061-STEP50-GNF-003|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-GNF-004|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-GNF-005|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-GNF-006|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-GNF-007|OPEN|INHERITED_CARRY|P059-CFR-RB-12|-|-
P061-STEP50-GNF-008|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-001|P061-GNF-006|P059-CFR-RB-12,P059-CFR-CF-11
P061-STEP50-GNF-009|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-001|P061-UNV-007|P059-CFR-CF-11
P061-STEP50-GNF-010|OPEN|INHERITED_CARRY|P059-CFR-NS-01|-|-
P061-STEP50-GNF-011|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-001|P061-GNF-006|P059-CFR-CF-11
P061-STEP50-UNV-001|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-002|P061-UNV-005|P059-CFR-RB-12
P061-STEP50-UNV-002|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-002|P061-UNV-005|P059-CFR-NS-01
P061-STEP50-UNV-003|OPEN_DUPLICATE_ALIAS|INHERITED_CARRY|P059-CFR-NS-05|P061-UNV-001|-
P061-STEP50-UNV-004|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-001|P061-UNV-007|P059-CFR-CF-11
P061-STEP50-UNV-005|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-004|P061-UNV-004|P059-CFR-BD-NEW-003,P059-CFR-NS-05,P059-CFR-RB-11,P059-CFR-NS-01
P061-STEP50-UNV-006|OPEN_REFINEMENT|PHASE061_BLOCKER|P061-BD-NEW-005|P061-UNV-006|P059-CFR-RM-007,P060-BD-NEW-003
P061-STEP50-UNV-007|OPEN_REFINEMENT|INHERITED_CARRY|P059-CFR-NS-05|P061-UNV-001|-
""".strip()


def parsed_debt_route_specs() -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for line in DEBT_ROUTE_TABLE.splitlines():
        debt_id, state, owner_type, owner_id, duplicate_of, corroborating = line.split("|")
        if debt_id in specs:
            raise ValueError(f"duplicate debt route spec: {debt_id}")
        specs[debt_id] = {
            "corroborating_owner_ids": [] if corroborating == "-" else corroborating.split(","),
            "duplicate_or_refinement_of": None if duplicate_of == "-" else duplicate_of,
            "owner_id": owner_id,
            "owner_type": owner_type,
            "route_state": state,
        }
    if len(specs) != 91:
        raise ValueError(f"debt route table is not exactly 91 rows: {len(specs)}")
    return specs


NEW_BLOCKER_SPECS: dict[str, dict[str, Any]] = {
    "P061-BD-NEW-001": {
        "authority_domain": "INTERNAL_ADOPTION_BUILD_AND_DERIVATION_AUTHORITY_ONLY",
        "validity_domain": "V1020_TO_V1021_COMPETITIVE_FIGURE_PNG_Q2_Q3_AND_DIRECTION_REPORT_ADOPTION_AND_DERIVATION",
        "source_debt_ids": [
            "P061-GNF-005", "P061-GNF-006", "P061-UNV-007", "P061-UNV-009",
            "P061-UNV-010", "P061-STEP50-GNF-001", "P061-STEP50-GNF-002",
            "P061-STEP50-GNF-008", "P061-STEP50-GNF-009", "P061-STEP50-GNF-011",
            "P061-STEP50-UNV-004",
        ],
        "acceptance_components": [
            ("A01", 62, "Enumerate exactly the 31 figure candidates, five packaged PNG occurrences, and every Q2/Q3 forward-content member without identity collapse."),
            ("A02", 62, "Record one explicit adoption or rejection decision for every enumerated member with bounded authority."),
            ("A03", 62, "For each adopted member, persist candidate-to-judgment-to-TeX-include-to-release-PDF-page edges and final placement, density, and label checks."),
            ("A04", 62, "Persist candidate-level reviewer-vote edges for all 31 figure candidates or retain each missing edge as GROUND_NOT_FOUND."),
            ("A05", 62, "Produce a clean selected-asset build with no unresolved references and preserve the build evidence."),
            ("A06", 82, "For every adopted Q2/Q3 equation claim, provide an evidence-backed final derivation or a justified exclusion in the final equation-freeze review."),
            ("A07", 82, "For direction-report occurrences P061-SRC-0065, P061-SRC-0066, and P061-SRC-0067, record an approved plan and one adoption or non-adoption decision each; for every adopted report persist an evidence-backed final derivation or justified exclusion, exact release-text target, and adoption edge while retaining scientific propositions for Phase 71 primary-source review."),
        ],
    },
    "P061-BD-NEW-002": {
        "authority_domain": "MIXED_INTERNAL_REPRODUCTION_AND_EXTERNAL_EXPERIMENTAL_AUTHORITY",
        "validity_domain": "FIGURE_NUMERICAL_AND_EXPERIMENTAL_VALIDITY",
        "source_debt_ids": [
            "P061-UNV-005", "P061-STEP48-UNV-005", "P061-STEP50-UNV-001",
            "P061-STEP50-UNV-002",
        ],
        "acceptance_components": [
            ("A01", 67, "Recreate every affected figure numerically from persisted source data and parameters with automated tolerance and provenance gates."),
            ("A02", 86, "Validate the recreated curves against provenance-controlled public experimental data with held-out uncertainty and failure gates."),
        ],
    },
    "P061-BD-NEW-003": {
        "authority_domain": "MIXED_THERMAL_MODEL_AND_EXTERNAL_DATA_AUTHORITY",
        "validity_domain": "TWO_PHASE_WIDTH_AND_LCO_DATA_GAPS",
        "source_debt_ids": ["P061-UNV-006"],
        "acceptance_components": [
            ("A01", 75, "Measure and model the two-phase width-temperature law while separating heterogeneity, kinetics, phase-field, and measurement-resolution contributions."),
            ("A02", 86, "Close the LCO OCV, entropy, and tier-2/tier-3 measurement gaps with provenance-controlled data and held-out validation."),
        ],
    },
    "P061-BD-NEW-004": {
        "authority_domain": "MIXED_PRIMARY_REFERENCE_THEORY_NUMERICAL_MATERIAL_EXPERIMENTAL_AUTHORITY",
        "validity_domain": "Q2_Q3_FULL_TRUTH_CHAIN",
        "source_debt_ids": ["P061-STEP50-UNV-005"],
        "acceptance_components": [
            ("A01", 71, "Verify every load-bearing Q2/Q3 DOI and proposition against primary full text."),
            ("A02", 82, "Provide an evidence-backed derivation or justified exclusion for every Q2/Q3 equation claim."),
            ("A03", 67, "Reproduce every Q2/Q3 numerical claim with deterministic tolerance and provenance gates."),
            ("A04", 86, "Validate every Q2/Q3 material and experimental claim against provenance-controlled data with uncertainty and failure gates."),
        ],
    },
    "P061-BD-NEW-005": {
        "authority_domain": "MIXED_THERMAL_MODEL_AND_HEAT_SIGN_AUTHORITY",
        "validity_domain": "TWO_PHASE_THERMAL_FORM_AND_HEAT_SIGN",
        "source_debt_ids": ["P061-STEP50-UNV-006"],
        "acceptance_components": [
            ("A01", 75, "Derive and validate the two-phase-width thermal form with explicit assumptions and held-out temperature tests."),
            ("A02", 81, "Derive and test the reversible-heat sign near xbar=0.75 under the declared branch-average and current-sign conventions."),
        ],
    },
}


def build_indexes(inputs: dict[str, Any]) -> dict[str, Any]:
    topology = inputs[TOPOLOGY]
    process = inputs[PROCESS]
    lineage = inputs[LINEAGE]
    sources = topology["sources"]
    if topology["baseline_commit"] != SOURCE_COMMIT:
        raise ValueError("frozen source commit changed")
    if inputs[P60_DISPOSITION]["gate_summary"]["status"] != "PASS":
        raise ValueError("Phase 060 disposition gate is not PASS")
    if ACTIVATION_GATE not in inputs[STEP50_RESULT]:
        raise ValueError("Step 50 activation gate token is absent")
    expected_ids = [f"P061-SRC-{index:04d}" for index in range(1, 233)]
    source_ids_ordered = [row["source_id"] for row in sources]
    if len(sources) != 232 or len(set(source_ids_ordered)) != 232:
        raise ValueError("topology source universe is not exactly 232 unique occurrences")
    if source_ids_ordered != expected_ids:
        raise ValueError("topology source order or stable identity changed")
    if any(row["manifest_index_v1020"] != index for index, row in enumerate(sources, 1)):
        raise ValueError("topology manifest index changed")
    if len({row["path"] for row in sources}) != 232:
        raise ValueError("topology path identity is not unique")
    process_rows = process["source_routes"]
    lineage_rows = lineage["delta_rows"]
    if len(process_rows) != 232 or len(lineage_rows) != 232:
        raise ValueError("process or lineage row count is not exactly 232")
    process_ids = [row["source_id"] for row in process_rows]
    lineage_ids = [row["v1020_source_id"] for row in lineage_rows]
    if len(set(process_ids)) != 232 or len(set(lineage_ids)) != 232:
        raise ValueError("duplicate process or lineage source identity")
    if process_ids != expected_ids or lineage_ids != expected_ids:
        raise ValueError("process or lineage source order differs from topology")
    process_by_id = {row["source_id"]: row for row in process_rows}
    delta_by_id = {row["v1020_source_id"]: row for row in lineage_rows}
    source_ids = set(source_ids_ordered)
    if set(process_by_id) != source_ids or set(delta_by_id) != source_ids:
        raise ValueError("process or lineage source universe differs from topology")
    for source, route, delta in zip(sources, process_rows, lineage_rows):
        for key in ("manifest_index_v1020", "path", "blob_sha1", "sha256", "manifest_extent", "review_mode"):
            if route[key] != source[key]:
                raise ValueError(f"process source identity mismatch: {source['source_id']}:{key}")
        if delta["manifest_index_v1020"] != source["manifest_index_v1020"]:
            raise ValueError(f"lineage manifest identity mismatch: {source['source_id']}")
        v1020 = delta["v1020"]
        expected_v1020 = {
            "blob_sha1": source["blob_sha1"],
            "extent": source["manifest_extent"],
            "path": source["path"],
            "review_mode": source["review_mode"],
            "role": source["manifest_role"],
            "sha256": source["sha256"],
            "sha256_lf_normalized": source["sha256"] if source["review_mode"] == "FULL_TEXT" else None,
            "size_bytes": source["size_bytes"],
        }
        if v1020 != expected_v1020:
            raise ValueError(f"lineage v1020 identity mismatch: {source['source_id']}")
        authority = delta["step47_authority"]
        for key in (
            "authority_ceiling", "external_scientific_truth", "scientific_authority_promoted",
            "source_authority_class",
        ):
            if authority[key] != route[key]:
                raise ValueError(f"lineage authority mismatch: {source['source_id']}:{key}")
    competitive_ids = {
        row["source_id"] for row in inputs[REVIEW]["competitive_source_records"]
    }
    adopted_ids = {
        row["source_id"] for row in inputs[REVIEW]["adopted_source_references"]
    }
    if competitive_ids & adopted_ids:
        raise ValueError("competitive and adopted identities overlap")
    if len(competitive_ids) != 126 or len(adopted_ids) != 43:
        raise ValueError("competitive/adopted source counts changed")
    citation_ids: dict[str, list[str]] = defaultdict(list)
    for row in inputs[CITATION]["authority_rows"]:
        citation_ids[row["source_id"]].append(row["asset_id"])
    return {
        "adopted_ids": adopted_ids,
        "citation_ids": citation_ids,
        "competitive_ids": competitive_ids,
        "delta_by_id": delta_by_id,
        "evidence_catalog": build_evidence_catalog(inputs),
        "process_by_id": process_by_id,
        "sources": sources,
    }


def disposition_for(source: dict[str, Any], indexes: dict[str, Any]) -> str:
    source_id = source["source_id"]
    route = indexes["process_by_id"][source_id]
    if source_id in COMPETING_SOURCE_OVERRIDES:
        return "COMPETING_ONLY"
    if (
        source_id in indexes["competitive_ids"]
        and source_id not in COMPETITIVE_REVIEW_PRESERVE
    ) or route["source_authority_class"] == "COMPETING_DRAFT":
        return "COMPETING_ONLY"
    if source_id in SUPERSEDE_EVIDENCE:
        return "SUPERSEDE"
    if source_id in CORRECTION_EVIDENCE:
        return "CORRECT"
    if source_id in UNVERIFIED_SOURCE_IDS:
        return "UNVERIFIED"
    return "PRESERVE"


def target_for(source: dict[str, Any], disposition: str, indexes: dict[str, Any]) -> int:
    source_id = source["source_id"]
    if disposition in {"COMPETING_ONLY", "SUPERSEDE"}:
        return 62
    if disposition == "UNVERIFIED":
        if source_id == "P061-SRC-0064":
            return 67
        if source_id in {"P061-SRC-0065", "P061-SRC-0066", "P061-SRC-0067"}:
            return 62
        return 71
    if disposition == "CORRECT":
        evidence = CORRECTION_EVIDENCE[source_id]
        return max(CORRECTION_TARGETS.get(item, 69) for item in evidence)
    if source_id in {"P061-SRC-0001", "P061-SRC-0002", "P061-SRC-0231", "P061-SRC-0232"}:
        return 67
    if 43 <= source_number(source_id) <= 49 or 193 <= source_number(source_id) <= 230:
        return 62
    if 54 <= source_number(source_id) <= 94:
        return 68
    if 4 <= source_number(source_id) <= 42:
        return 71
    if source_id in {"P061-SRC-0051", "P061-SRC-0053"}:
        return 69
    return 62


def carry_links(source: dict[str, Any], disposition: str) -> list[str]:
    source_id = source["source_id"]
    path = source["path"]
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
        "P061-SRC-0008", "P061-SRC-0009", "P061-SRC-0012",
        "P061-SRC-0017", "P061-SRC-0019", "P061-SRC-0021",
        "P061-SRC-0027", "P061-SRC-0028", "P061-SRC-0030",
        "P061-SRC-0036", "P061-SRC-0040",
    }:
        links.add("P059-CFR-RB-13")
    for blocker_id, evidence in P61_DIRECT_BLOCKER_EVIDENCE.items():
        if source_id in evidence:
            links.add(blocker_id)
    return sorted(links)


def evidence_ids_for(source: dict[str, Any], indexes: dict[str, Any]) -> list[str]:
    source_id = source["source_id"]
    delta = indexes["delta_by_id"][source_id]
    evidence = {source_id, delta["delta_id"]}
    evidence.update(SUPERSEDE_EVIDENCE.get(source_id, ()))
    evidence.update(CORRECTION_EVIDENCE.get(source_id, ()))
    evidence.update(CONTEXT_EVIDENCE.get(source_id, ()))
    evidence.update(indexes["citation_ids"].get(source_id, ()))
    return sorted(evidence)


def reason_for(source: dict[str, Any], disposition: str, indexes: dict[str, Any]) -> str:
    source_id = source["source_id"]
    route = indexes["process_by_id"][source_id]
    delta = indexes["delta_by_id"][source_id]
    if disposition == "COMPETING_ONLY":
        return (
            "This frozen occurrence belongs to the competitive/non-adopted corpus. "
            "Content or blob overlap cannot merge it with an adopted occurrence; an explicit "
            "future adoption edge is required."
        )
    if disposition == "SUPERSEDE":
        return (
            "Later frozen process evidence supersedes this occurrence for forward authority; "
            f"the earlier record remains preserved as history under {', '.join(SUPERSEDE_EVIDENCE[source_id])}."
        )
    if disposition == "CORRECT":
        return (
            "Direct Phase 061 evidence identifies a bounded source or process defect under "
            f"{', '.join(CORRECTION_EVIDENCE[source_id])}; correction applies only to a future "
            "Codex-controlled descendant, never to the frozen Claude occurrence."
        )
    if disposition == "UNVERIFIED":
        return (
            "The source is retained only at its recorded external-science-unverified ceiling; "
            "no primary-source, material, or experimental truth was established in Phase 061."
        )
    if source_id in CONTEXT_EVIDENCE:
        return (
            "This frozen occurrence remains necessary as bounded historical, structural, or review "
            f"evidence. Direct concerns {', '.join(CONTEXT_EVIDENCE[source_id])} constrain its use "
            "but do not justify deleting or rewriting the frozen occurrence."
        )
    return (
        f"The occurrence is a lossless {route['source_authority_class']} record with "
        f"{delta['comparison_class']} lineage and no direct Phase 061 evidence requiring "
        "source-level correction, supersession, or discard."
    )


def acceptance_for(
    source: dict[str, Any], disposition: str, target: int, indexes: dict[str, Any]
) -> str:
    source_id = source["source_id"]
    path = source["path"]
    if disposition == "PRESERVE":
        return (
            f"Phase {target} retains {source_id} as the distinct frozen occurrence at {path}, "
            "preserves its blob and authority ceiling, and records any later adoption or rejection "
            "without promoting scientific or material truth."
        )
    if disposition == "CORRECT":
        return (
            f"Phase {target} resolves every cited defect for {source_id} in a Codex-controlled "
            "descendant, adds a persistent source-specific gate, and keeps the frozen occurrence "
            "and its defect evidence unchanged for lineage recovery."
        )
    if disposition == "SUPERSEDE":
        return (
            f"Phase {target} records the exact later authority that supersedes {source_id}, keeps "
            "this occurrence as historical process evidence, and prevents its obsolete instruction "
            "or status from controlling canonical synthesis."
        )
    if disposition == "COMPETING_ONLY":
        return (
            f"Phase {target} keeps {source_id} separate from all adopted identities and either "
            "records an explicit source-to-target adoption edge with bounded authority or retains "
            "the occurrence as non-adopted competitive evidence."
        )
    if disposition == "UNVERIFIED":
        if source_id == "P061-SRC-0064":
            return (
                "Phase 67 executes a fresh isolated build/test of P061-SRC-0064, persists the "
                "environment and full result, and retains every unexecuted runtime claim as unverified."
            )
        if source_id in {"P061-SRC-0065", "P061-SRC-0066", "P061-SRC-0067"}:
            return (
                f"Phase 62 records an explicit adoption or non-adoption edge for {source_id}; any "
                "scientific proposition remains separately unverified until Phase 71 primary-source review."
            )
        return (
            f"Phase {target} performs primary-source and proposition-level verification for "
            f"{source_id}; until then it remains unverified and cannot support scientific, material, "
            "or experimental truth."
        )
    return (
        f"Phase {target} records an evidence-backed exclusion of {source_id} while preserving the "
        "frozen occurrence and explaining all downstream replacements."
    )


def build_dispositions(indexes: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in indexes["sources"]:
        source_id = source["source_id"]
        route = indexes["process_by_id"][source_id]
        delta = indexes["delta_by_id"][source_id]
        disposition = disposition_for(source, indexes)
        target = target_for(source, disposition, indexes)
        evidence_ids = evidence_ids_for(source, indexes)
        rows.append(
            {
                "acceptance_criterion": acceptance_for(source, disposition, target, indexes),
                "authority_ceiling": route["authority_ceiling"],
                "carry_forward_links": carry_links(source, disposition),
                "disposition": disposition,
                "disposition_id": f"P061-DISP-{source_number(source_id):04d}",
                "evidence_ids": evidence_ids,
                "evidence_routes": evidence_routes_for(source, indexes, evidence_ids),
                "external_material_truth": False,
                "external_scientific_truth": False,
                "process_authority_anchor": {
                    "artifact_path": PROCESS,
                    "json_pointer": f"/source_routes/{source['manifest_index_v1020'] - 1}",
                    "record_sha256": sha256(record_bytes(route)),
                    "source_id": source_id,
                },
                "reason": reason_for(source, disposition, indexes),
                "source_authority_class": route["source_authority_class"],
                "source_identity": {
                    "blob_sha1": source["blob_sha1"],
                    "dedup_group": source["dedup_group"],
                    "manifest_index_v1020": source["manifest_index_v1020"],
                    "path": source["path"],
                    "sha256": source["sha256"],
                },
                "source_id": source_id,
                "source_record_sha256": sha256(record_bytes(source)),
                "status": "PRESERVED_ACTIVE" if disposition == "PRESERVE" else "OPEN",
                "target_phase": target,
                "v1019_comparison_class": delta["comparison_class"],
            }
        )
    return rows


def build_disposition_artifact(
    inputs: dict[str, Any], metadata: list[dict[str, Any]], indexes: dict[str, Any]
) -> dict[str, Any]:
    rows = build_dispositions(indexes)
    membership = [row["source_id"] for row in rows]
    competitive = [row for row in rows if row["disposition"] == "COMPETING_ONLY"]
    adopted_overlap = sum(row["source_id"] in indexes["adopted_ids"] for row in competitive)
    counts = Counter(row["disposition"] for row in rows)
    return {
        "artifact_kind": "PHASE_061_V1020_DISPOSITION_MATRIX",
        "authority_boundary": AUTHORITY_BOUNDARY,
        "baseline_commit": inputs[TOPOLOGY]["baseline_commit"],
        "dispositions": rows,
        "gate_summary": {
            "allowed_dispositions": list(ALLOWED_DISPOSITIONS),
            "competitive_adopted_identity_overlap_count": adopted_overlap,
            "competitive_disposition_count": len(competitive),
            "disposition_counts": dict(sorted(counts.items())),
            "disposition_rows": len(rows),
            "duplicate_disposition_id_count": len(rows) - len({row["disposition_id"] for row in rows}),
            "duplicate_source_membership_count": len(membership) - len(set(membership)),
            "external_authority_promotion_count": sum(
                row["external_material_truth"] or row["external_scientific_truth"]
                for row in rows
            ),
            "missing_acceptance_reason_target_status_count": sum(
                not row["acceptance_criterion"]
                or not row["reason"]
                or not isinstance(row["target_phase"], int)
                or row["status"] not in {"OPEN", "PRESERVED_ACTIVE", "RESOLVED"}
                for row in rows
            ),
            "source_expected": 232,
            "source_orphan_count": len(set(source["source_id"] for source in indexes["sources"]) - set(membership)),
            "status": "PASS",
        },
        "generation": {
            "active_branch": ACTIVE_BRANCH,
            "builder": "Codex/work/v1020_phase061/build_phase061_step51_dispositions.py",
            "canonical_json": "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true",
            "deterministic": True,
            "production_imported_or_executed": False,
        },
        "input_artifact_commit": INPUT_ARTIFACT_COMMIT,
        "inputs": metadata,
        "phase": 61,
        "schema_version": "phase061-step51.1-dispositions-v2",
        "source_commit": SOURCE_COMMIT,
        "source_manifest_sha256": sha256(record_bytes(indexes["sources"])),
        "step": "51.1",
    }


def build_inherited_carry(prior_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    route_specs = parsed_debt_route_specs()
    for prior in prior_rows:
        carry_id = prior["carry_forward_id"]
        routed = {
            debt_id for debt_id, spec in route_specs.items()
            if spec["owner_id"] == carry_id or carry_id in spec["corroborating_owner_ids"]
        }
        evidence = sorted(set(P61_DIRECT_CARRY_EVIDENCE.get(carry_id, ())) | routed)
        primary_open = sorted(
            debt_id for debt_id, spec in route_specs.items()
            if spec["owner_id"] == carry_id and spec["route_state"].startswith("OPEN")
        )
        if carry_id in REFINED_CARRY_IDS or primary_open:
            delta_status = "REFINED_DIRECT_EVIDENCE"
            refinement = (
                f"Phase 061 evidence {', '.join(evidence)} directly refines the inherited acceptance "
                f"clause `{prior['acceptance_criterion_after']}`. The inherited target, authority, "
                "and open/preserved status remain verbatim and no resolution is claimed."
            )
        elif evidence:
            delta_status = "TOUCHED_DIRECT_EVIDENCE"
            refinement = None
        else:
            delta_status = "UNCHANGED"
            refinement = None
        rows.append(
            {
                "acceptance_criterion_after": prior["acceptance_criterion_after"],
                "acceptance_criterion_before": prior["acceptance_criterion_after"],
                "acceptance_satisfied": False,
                "authority_boundary_after": prior["authority_boundary_after"],
                "authority_boundary_before": prior["authority_boundary_after"],
                "carry_forward_id": carry_id,
                "category_after": prior["category_after"],
                "category_before": prior["category_after"],
                "delta_status": delta_status,
                "external_material_truth": False,
                "external_scientific_truth": False,
                "prior_record": prior,
                "prior_record_sha256": sha256(record_bytes(prior)),
                "refinement_note": refinement,
                "resolution_status": "NOT_RESOLVED",
                "status_after": prior["status_after"],
                "status_before": prior["status_after"],
                "target_phase_after": prior["target_phase_after"],
                "target_phase_before": prior["target_phase_after"],
                "touch_evidence_ids": evidence,
            }
        )
    return rows


def build_inherited_blockers(prior_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    route_specs = parsed_debt_route_specs()
    for prior in prior_rows:
        blocker_id = prior["blocker_id"]
        routed = {
            debt_id for debt_id, spec in route_specs.items()
            if spec["owner_id"] == blocker_id or blocker_id in spec["corroborating_owner_ids"]
        }
        evidence = sorted(set(P61_DIRECT_BLOCKER_EVIDENCE.get(blocker_id, ())) | routed)
        rows.append(
            {
                "acceptance_criterion_after": prior["acceptance_criterion"],
                "acceptance_criterion_before": prior["acceptance_criterion"],
                "acceptance_satisfied": False,
                "authority_boundary_after": prior["authority_boundary"],
                "authority_boundary_before": prior["authority_boundary"],
                "blocker_id": blocker_id,
                "category_after": prior["category"],
                "category_before": prior["category"],
                "delta_status": "TOUCHED_DIRECT_EVIDENCE" if evidence else "UNCHANGED",
                "external_material_truth": False,
                "external_scientific_truth": False,
                "prior_record": prior,
                "prior_record_sha256": sha256(record_bytes(prior)),
                "refinement_note": None,
                "resolution_status": "NOT_RESOLVED",
                "status_after": prior["status"],
                "status_before": prior["status"],
                "target_phase_after": prior["target_phase"],
                "target_phase_before": prior["target_phase"],
                "touch_evidence_ids": evidence,
            }
        )
    return rows


def debt_requirement(record: dict[str, Any]) -> str:
    for key in ("required_evidence", "object", "finding", "description"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValueError("debt record lacks a usable requirement")


def owner_type_for(owner_id: str) -> str:
    if owner_id.startswith("P061-DISP-"):
        return "SOURCE_DISPOSITION"
    if owner_id.startswith("P061-BD-"):
        return "PHASE061_BLOCKER"
    if owner_id.startswith("P060-BD-"):
        return "PHASE060_BLOCKER"
    return "INHERITED_CARRY"


def canonical_debt_records(inputs: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path, section, id_key in DEBT_SECTION_SPECS:
        for index, record in enumerate(inputs[path][section]):
            debt_id = record[id_key]
            if debt_id in records:
                raise ValueError(f"duplicate canonical debt origin: {debt_id}")
            records[debt_id] = {
                "origin_path": path,
                "origin_pointer": f"/{section}/{index}",
                "origin_record_sha256": sha256(record_bytes(record)),
                "record": record,
            }
    if len(records) != 91:
        raise ValueError(f"canonical debt universe is not 91: {len(records)}")
    return records


def build_new_blockers(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    origins = canonical_debt_records(inputs)
    rows: list[dict[str, Any]] = []
    claimed_debts: set[str] = set()
    for blocker_id, spec in NEW_BLOCKER_SPECS.items():
        source_debt_ids = spec["source_debt_ids"]
        if claimed_debts & set(source_debt_ids):
            raise ValueError(f"new blocker debt membership overlap: {blocker_id}")
        claimed_debts.update(source_debt_ids)
        components = [
            {"component_id": component_id, "criterion": criterion, "status": "OPEN", "target_phase": target}
            for component_id, target, criterion in spec["acceptance_components"]
        ]
        component_ids = [row["component_id"] for row in components]
        origin_anchors = [
            {
                "debt_id": debt_id,
                "origin_path": origins[debt_id]["origin_path"],
                "origin_pointer": origins[debt_id]["origin_pointer"],
                "origin_record_sha256": origins[debt_id]["origin_record_sha256"],
            }
            for debt_id in source_debt_ids
        ]
        rows.append({
            "acceptance_components": components,
            "acceptance_criterion": (
                f"ALL_OF components {', '.join(component_ids)} must PASS with persistent evidence; "
                "no partial component result may close the blocker."
            ),
            "authority_domain": spec["authority_domain"],
            "blocker_id": blocker_id,
            "closure_operator": "ALL_OF",
            "external_material_truth": False,
            "external_scientific_truth": False,
            "non_double_count_basis": (
                f"{blocker_id} is the sole primary acceptance surface for source debts "
                f"{', '.join(source_debt_ids)}; inherited carry and source dispositions are "
                "corroborating only where listed in debt_routing."
            ),
            "origin_anchors": origin_anchors,
            "source_debt_ids": source_debt_ids,
            "status": "OPEN",
            "target_phase": max(row["target_phase"] for row in components),
            "validity_domain": spec["validity_domain"],
        })
    if len(rows) != 5 or len(claimed_debts) != 18:
        raise ValueError(f"new blocker cardinality changed: blockers={len(rows)} debts={len(claimed_debts)}")
    return rows


def build_owner_catalog(
    dispositions: list[dict[str, Any]], carry: list[dict[str, Any]], blockers: list[dict[str, Any]],
    new_blockers: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    owners: dict[str, dict[str, Any]] = {}
    for row in dispositions:
        owners[row["disposition_id"]] = {
            "acceptance_criterion": row["acceptance_criterion"],
            "owner_type": "SOURCE_DISPOSITION",
            "status": row["status"],
            "target_phase": row["target_phase"],
        }
    for row in carry:
        owners[row["carry_forward_id"]] = {
            "acceptance_criterion": row["acceptance_criterion_after"],
            "owner_type": "INHERITED_CARRY",
            "status": row["status_after"],
            "target_phase": row["target_phase_after"],
        }
    for row in blockers:
        owners[row["blocker_id"]] = {
            "acceptance_criterion": row["acceptance_criterion_after"],
            "owner_type": "PHASE060_BLOCKER",
            "status": row["status_after"],
            "target_phase": row["target_phase_after"],
        }
    for row in new_blockers:
        owners[row["blocker_id"]] = {
            "acceptance_criterion": row["acceptance_criterion"],
            "owner_type": "PHASE061_BLOCKER",
            "status": row["status"],
            "target_phase": row["target_phase"],
        }
    return owners


def build_debt_routing(
    inputs: dict[str, Any], dispositions: list[dict[str, Any]],
    carry: list[dict[str, Any]], blockers: list[dict[str, Any]], new_blockers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    specs = parsed_debt_route_specs()
    owners = build_owner_catalog(dispositions, carry, blockers, new_blockers)
    records: list[tuple[str, str, str, dict[str, Any]]] = []
    for path, section, id_key in DEBT_SECTION_SPECS:
        for index, record in enumerate(inputs[path][section]):
            records.append((record[id_key], path, f"/{section}/{index}", record))
    debt_ids = [record[0] for record in records]
    if len(debt_ids) != 91 or len(set(debt_ids)) != 91 or set(debt_ids) != set(specs):
        raise ValueError("canonical debt universe or route membership changed")
    routing: list[dict[str, Any]] = []
    for debt_id, path, pointer, record in records:
        spec = specs[debt_id]
        owner = owners.get(spec["owner_id"])
        if owner is None or owner["owner_type"] != spec["owner_type"]:
            raise ValueError(f"invalid primary owner for {debt_id}: {spec['owner_id']}")
        origin_target = record.get("target_phase")
        owner_target = owner["target_phase"]
        effective_target = max(
            value for value in (origin_target, owner_target) if isinstance(value, int)
        )
        if origin_target is None:
            schedule_relation = "ORIGIN_TARGET_NOT_SPECIFIED"
        elif owner_target == origin_target:
            schedule_relation = "MATCH"
        elif owner_target > origin_target:
            schedule_relation = "OWNER_LATER_THAN_ORIGIN"
        else:
            schedule_relation = "OWNER_EARLIER_THAN_ORIGIN"
        corroborating_routes = []
        for corroborating_id in spec["corroborating_owner_ids"]:
            corroborating_owner = owners.get(corroborating_id)
            if corroborating_owner is None:
                raise ValueError(f"invalid corroborating owner for {debt_id}: {corroborating_id}")
            corroborating_routes.append({
                "edge_kind": "CORROBORATING_OVERLAP",
                "owner_id": corroborating_id,
                "owner_type": corroborating_owner["owner_type"],
                "target_phase": corroborating_owner["target_phase"],
            })
        requirement = debt_requirement(record)
        routing.append({
            "corroborating_routes": corroborating_routes,
            "debt_id": debt_id,
            "debt_requirement": requirement,
            "duplicate_or_refinement_of": spec["duplicate_or_refinement_of"],
            "effective_target_phase": effective_target,
            "non_double_count_basis": (
                f"{debt_id} is the sole canonical origin row. Primary closure belongs only to "
                f"{spec['owner_id']}; duplicate/refinement and corroborating edges do not create "
                "additional closure claims."
            ),
            "origin_path": path,
            "origin_pointer": pointer,
            "origin_record_sha256": sha256(record_bytes(record)),
            "origin_target_phase": origin_target,
            "owner_acceptance_criterion": owner["acceptance_criterion"],
            "owner_target_phase": owner_target,
            "primary_owner_id": spec["owner_id"],
            "primary_owner_type": spec["owner_type"],
            "route_state": spec["route_state"],
            "schedule_relation": schedule_relation,
            "status": "RESOLVED" if spec["route_state"] == "RESOLVED_INFORMATIONAL" else "OPEN",
        })
    return routing


def build_delta_artifact(
    inputs: dict[str, Any], metadata: list[dict[str, Any]], dispositions: list[dict[str, Any]]
) -> dict[str, Any]:
    prior_delta = inputs[P60_DELTA]
    carry = build_inherited_carry(prior_delta["inherited_items"])
    blockers = build_inherited_blockers(prior_delta["new_blockers"])
    new_blockers = build_new_blockers(inputs)
    if len(carry) != 52 or len(blockers) != 5:
        raise ValueError("Phase 060 inheritance is not exactly 52 carry plus 5 blockers")
    all_ids = [row["carry_forward_id"] for row in carry] + [row["blocker_id"] for row in blockers]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("inherited carry/blocker identity collision")
    all_rows = carry + blockers
    debt_routing = build_debt_routing(inputs, dispositions, carry, blockers, new_blockers)
    delta_counts = Counter(row["delta_status"] for row in all_rows)
    route_counts = Counter(row["route_state"] for row in debt_routing)
    primary_owner_counts = Counter(row["primary_owner_type"] for row in debt_routing)
    return {
        "artifact_kind": "PHASE_061_V1020_CARRY_FORWARD_DELTA",
        "authority_boundary": AUTHORITY_BOUNDARY,
        "baseline_commit": inputs[TOPOLOGY]["baseline_commit"],
        "debt_routing": debt_routing,
        "gate_summary": {
            "acceptance_satisfied_count": sum(row["acceptance_satisfied"] for row in all_rows),
            "delta_status_counts": dict(sorted(delta_counts.items())),
            "external_authority_promotion_count": sum(
                row["external_material_truth"] or row["external_scientific_truth"]
                for row in all_rows
            ),
            "inherited_carry_count": len(carry),
            "inherited_identity_duplicate_count": len(all_ids) - len(set(all_ids)),
            "inherited_phase060_blocker_count": len(blockers),
            "new_blocker_count": len(new_blockers),
            "new_blocker_rationale": (
                "Five Phase 061 blockers are required because inherited carry and source dispositions "
                "do not individually own the full adoption, numerical-plus-experimental, two-phase-plus-LCO, "
                "Q2/Q3 full-truth-chain, or thermal-law-plus-heat-sign acceptance domains. Each new "
                "blocker uses ALL_OF atomic components and exact canonical debt anchors."
            ),
            "open_debt_count": sum(row["status"] == "OPEN" for row in debt_routing),
            "orphan_open_debt_count": sum(
                row["status"] == "OPEN" and not row["primary_owner_id"] for row in debt_routing
            ),
            "primary_owner_type_counts": dict(sorted(primary_owner_counts.items())),
            "resolution_status_counts": dict(
                sorted(Counter(row["resolution_status"] for row in all_rows).items())
            ),
            "status": "PASS",
            "status_after_counts": dict(
                sorted(Counter(row["status_after"] for row in all_rows).items())
            ),
            "total_debt_count": len(debt_routing),
            "debt_route_state_counts": dict(sorted(route_counts.items())),
        },
        "generation": {
            "active_branch": ACTIVE_BRANCH,
            "builder": "Codex/work/v1020_phase061/build_phase061_step51_dispositions.py",
            "canonical_json": "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true",
            "deterministic": True,
            "production_imported_or_executed": False,
        },
        "input_artifact_commit": INPUT_ARTIFACT_COMMIT,
        "inherited_carry_items": carry,
        "inherited_phase060_blockers": blockers,
        "inputs": metadata,
        "new_blockers": new_blockers,
        "phase": 61,
        "schema_version": "phase061-step51.1-carry-forward-delta-v2",
        "source_commit": SOURCE_COMMIT,
        "step": "51.1",
    }


def write_output(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disposition-output", type=Path, default=DEFAULT_DISPOSITION_OUTPUT)
    parser.add_argument("--delta-output", type=Path, default=DEFAULT_DELTA_OUTPUT)
    args = parser.parse_args()
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    if branch != ACTIVE_BRANCH:
        raise RuntimeError(f"unexpected active branch: {branch}")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", STEP50_COMMIT, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Step 50 checkpoint is not an ancestor of HEAD")
    inputs, metadata = read_inputs()
    indexes = build_indexes(inputs)
    disposition = build_disposition_artifact(inputs, metadata, indexes)
    delta = build_delta_artifact(inputs, metadata, disposition["dispositions"])
    write_output(args.disposition_output, disposition)
    write_output(args.delta_output, delta)
    print(
        "PASS build Phase061 Step51.1 "
        f"sources={len(disposition['dispositions'])} "
        f"carry={len(delta['inherited_carry_items'])} "
        f"phase060_blockers={len(delta['inherited_phase060_blockers'])} "
        f"new_blockers={len(delta['new_blockers'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
