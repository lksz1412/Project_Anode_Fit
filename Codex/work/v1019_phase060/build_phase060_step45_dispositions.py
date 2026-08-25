#!/usr/bin/env python3
"""Build Phase 060 Step 45.1 lineage-disposition machine artifacts.

This builder reads prior audit artifacts only.  It never imports or calls the
frozen Anode Fit production modules and does not make external-science claims.
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
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PRE_STEP45_COMMIT = "70b14fd102fca40ef17bee44e924c09dde1d9eff"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
AUTHORITY = (
    "Internal lineage disposition only; external material truth remains false; "
    "external scientific truth remains false."
)
ACTIVATION_GATE = "PASS_P060_LINEAGE_C"
ALLOWED_DISPOSITIONS = (
    "PRESERVE",
    "CORRECT",
    "SUPERSEDE",
    "EMPIRICAL_ONLY",
    "THEORY_ONLY",
    "REJECT",
    "UNVERIFIED",
)

DEFAULT_DISPOSITION_OUTPUT = ROOT / "Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json"
DEFAULT_DELTA_OUTPUT = ROOT / "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json"

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

S40_JSON = INPUT_PATHS[0]
S40_RESULT = INPUT_PATHS[1]
S41_JSON = INPUT_PATHS[2]
S41_RESULT = INPUT_PATHS[3]
S42_RUNTIME = INPUT_PATHS[4]
S42_ARTIFACT = INPUT_PATHS[5]
S42_RESULT = INPUT_PATHS[6]
S43_JSON = INPUT_PATHS[7]
S43_RESULT = INPUT_PATHS[8]
S44_JSON = INPUT_PATHS[9]
S44_MD = INPUT_PATHS[10]
S44_RESULT = INPUT_PATHS[11]
P59_REGISTER = INPUT_PATHS[12]


class DuplicateKey(ValueError):
    """Raised when a JSON object repeats a key."""


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(f"duplicate JSON key: {key}")
        result[key] = value
    return result


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
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def physical_lines(raw: bytes) -> int:
    if not raw:
        return 0
    return raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def read_inputs() -> tuple[dict[str, Any], dict[str, bytes], list[dict[str, Any]]]:
    parsed: dict[str, Any] = {}
    raw_inputs: dict[str, bytes] = {}
    metadata: list[dict[str, Any]] = []
    for relative in INPUT_PATHS:
        raw = (ROOT / relative).read_bytes()
        raw_inputs[relative] = raw
        if relative.endswith(".json"):
            parsed[relative] = strict_load(raw)
            parse_mode = "STRICT_JSON_DUPLICATE_KEY_AND_NONFINITE_REJECTED"
        else:
            parsed[relative] = raw.decode("utf-8")
            parse_mode = "FULL_UTF8_TEXT"
        metadata.append(
            {
                "bytes": len(raw),
                "git_blob_sha1": git_blob_sha1(raw),
                "parse_mode": parse_mode,
                "path": relative,
                "physical_lines": physical_lines(raw),
                "sha256": sha256(raw),
            }
        )
    return parsed, raw_inputs, metadata


def source_summary(record: Any) -> str:
    if isinstance(record, str):
        return record
    for key in (
        "claim",
        "defect_summary",
        "title",
        "item",
        "finding",
        "summary",
        "statement",
        "topic",
        "text",
    ):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValueError(f"source record lacks a usable summary: {record!r}")


def manifest_record(
    source_id: str,
    source_family: str,
    artifact_path: str,
    collection: str,
    index: int,
    record: Any,
    result_path: str,
    anchor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "evidence_paths": [artifact_path, result_path],
        "source_anchors": [
            anchor
            or {
                "artifact_path": artifact_path,
                "json_pointer": f"$.{collection}[{index}]",
            }
        ],
        "source_artifact_path": artifact_path,
        "source_collection": collection,
        "source_family": source_family,
        "source_id": source_id,
        "source_index": index,
        "source_record_sha256": sha256(record_bytes(record)),
        "source_summary": source_summary(record),
    }


def reconstruct_source_manifest(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    step40_lines = inputs[S40_RESULT].splitlines()
    for index, (source_id, start, end) in enumerate(
        (
            ("P060-S40-F01", 190, 192),
            ("P060-S40-F02", 194, 196),
            ("P060-S40-F03", 198, 200),
        )
    ):
        record = {
            "end_line": end,
            "start_line": start,
            "text": "\n".join(step40_lines[start - 1 : end]),
        }
        rows.append(
            manifest_record(
                source_id,
                "STEP40_SOURCE_FINDING",
                S40_RESULT,
                "confirmed_source_findings",
                index,
                record,
                S40_JSON,
                {"artifact_path": S40_RESULT, "end_line": end, "start_line": start},
            )
        )
    for index, line_number in enumerate(range(206, 211), 1):
        record = step40_lines[line_number - 1]
        rows.append(
            manifest_record(
                f"P060-S40-GNF-{index:03d}",
                "STEP40_GROUND_NOT_FOUND",
                S40_RESULT,
                "ground_not_found",
                index - 1,
                record,
                S40_JSON,
                {
                    "artifact_path": S40_RESULT,
                    "end_line": line_number,
                    "start_line": line_number,
                },
            )
        )

    step41 = inputs[S41_JSON]
    for index, record in enumerate(step41["claims"]):
        rows.append(
            manifest_record(
                record["claim_id"], "STEP41_CLAIM", S41_JSON, "claims", index, record, S41_RESULT
            )
        )
    for index, record in enumerate(step41["defect_correction_records"]):
        rows.append(
            manifest_record(
                f"DCR-CU-{index + 2:02d}",
                "STEP41_DEFECT_CORRECTION",
                S41_JSON,
                "defect_correction_records",
                index,
                record,
                S41_RESULT,
            )
        )
    for index, record in enumerate(step41["contradictions"]):
        rows.append(
            manifest_record(
                record["contradiction_id"],
                "STEP41_CONTRADICTION",
                S41_JSON,
                "contradictions",
                index,
                record,
                S41_RESULT,
            )
        )
    for index, record in enumerate(step41["unresolved_queue"]):
        rows.append(
            manifest_record(
                record["unresolved_id"],
                "STEP41_UNRESOLVED",
                S41_JSON,
                "unresolved_queue",
                index,
                record,
                S41_RESULT,
            )
        )

    step42 = inputs[S42_RUNTIME]
    for severity, prefix in (("P1", "P060-S42-RT-P1"), ("P2", "P060-S42-RT-P2")):
        for index, record in enumerate(step42["findings"][severity]):
            rows.append(
                manifest_record(
                    f"{prefix}-{index + 1:03d}",
                    "STEP42_RUNTIME_FINDING",
                    S42_RUNTIME,
                    f"findings.{severity}",
                    index,
                    record,
                    S42_RESULT,
                    {
                        "artifact_path": S42_RUNTIME,
                        "json_pointer": f"$.findings.{severity}[{index}]",
                    },
                )
            )
    visual_findings = inputs[S42_ARTIFACT]["manual_visual_attestation"]["findings"]
    for index, record in enumerate(visual_findings):
        rows.append(
            manifest_record(
                record["id"],
                "STEP42_VISUAL_FINDING",
                S42_ARTIFACT,
                "manual_visual_attestation.findings",
                index,
                record,
                S42_RESULT,
                {
                    "artifact_path": S42_ARTIFACT,
                    "json_pointer": f"$.manual_visual_attestation.findings[{index}]",
                },
            )
        )

    step43 = inputs[S43_JSON]
    for index, record in enumerate(step43["trace_rows"]):
        rows.append(
            manifest_record(
                record["trace_id"],
                "STEP43_TRACE_ROW",
                S43_JSON,
                "trace_rows",
                index,
                record,
                S43_RESULT,
            )
        )
    for severity in ("P1", "P2"):
        for index, record in enumerate(step43["findings"][severity]):
            rows.append(
                manifest_record(
                    record["id"],
                    "STEP43_FINDING",
                    S43_JSON,
                    f"findings.{severity}",
                    index,
                    record,
                    S43_RESULT,
                    {
                        "artifact_path": S43_JSON,
                        "json_pointer": f"$.findings.{severity}[{index}]",
                    },
                )
            )

    step44 = inputs[S44_JSON]
    for index, record in enumerate(step44["findings"]):
        rows.append(
            manifest_record(
                record["finding_id"],
                "STEP44_PHYSICS_FINDING",
                S44_JSON,
                "findings",
                index,
                record,
                S44_RESULT,
            )
        )
    for index, record in enumerate(step44["source_conflicts"]):
        rows.append(
            manifest_record(
                record["conflict_id"],
                "STEP44_SOURCE_CONFLICT",
                S44_JSON,
                "source_conflicts",
                index,
                record,
                S44_RESULT,
            )
        )
    if len(rows) != 173 or len({row["source_id"] for row in rows}) != 173:
        raise ValueError("source universe is not exactly 173 unique identities")
    return rows


S41_PRESERVE = {
    "CLM-001", "CLM-002", "CLM-003", "CLM-004", "CLM-005", "CLM-007",
    "CLM-009", "CLM-010", "CLM-011", "CLM-013", "CLM-014", "CLM-016",
    "CLM-018", "CLM-019", "CLM-020", "CLM-023", "CLM-024", "CLM-025",
    "CLM-026", "CLM-033", "CLM-034",
}
S41_THEORY = {"CLM-006", "CLM-012"}

TRACE_PRESERVE = {
    "TRC-CH1-CHARGE-BALANCE",
    "TRC-CH1-CENTER-THERMO",
    "TRC-CH1-WIDTH-LOGISTIC",
    "TRC-CH1-LOW-CURRENT-HYS-LIMIT",
    "TRC-CH1-REVERSIBLE-BASELINE",
    "TRC-CH1-LCO-HYSTERESIS",
    "TRC-CH1-LCO-PEAK",
    "TRC-CH2-CONFIGURATIONAL",
    "TRC-CH2-MIXING-WEIGHTED",
    "TRC-CH2-REVERSIBLE-HEAT",
    "TRC-CH2-REGRESSION-WITNESSES",
    "TRC-CH2-DOC-LEADS-BOUNDARY",
}
TRACE_EMPIRICAL = {
    "TRC-CH1-HYSTERESIS", "TRC-CH1-LAG-LENGTH", "TRC-CH1-TAIL-CAUSAL"
}
TRACE_THEORY = {
    "TRC-CH1-BROADENING-BUDGET",
    "TRC-CH1-MSMR-MAP",
    "TRC-CH2-PARTITION-LOGISTIC",
    "TRC-CH2-PARTITION-BW",
    "TRC-CH2-HYSTERESIS-REVERSIBLE",
}

STEP44_FINDING_DISPOSITIONS = {
    "P060-PHY-P1-001": "CORRECT",
    "P060-PHY-P1-002": "CORRECT",
    "P060-PHY-P1-003": "PRESERVE",
    "P060-PHY-P1-004": "CORRECT",
    "P060-PHY-P1-005": "CORRECT",
    "P060-PHY-P1-006": "CORRECT",
    "P060-PHY-P1-007": "THEORY_ONLY",
    "P060-PHY-P1-008": "PRESERVE",
    "P060-PHY-P1-009": "UNVERIFIED",
    "P060-PHY-P1-010": "THEORY_ONLY",
    "P060-PHY-P1-011": "CORRECT",
    "P060-PHY-P1-012": "UNVERIFIED",
    "P060-PHY-P2-001": "EMPIRICAL_ONLY",
    "P060-PHY-P2-002": "UNVERIFIED",
    "P060-PHY-P2-003": "UNVERIFIED",
    "P060-PHY-P2-004": "UNVERIFIED",
    "P060-PHY-P2-005": "UNVERIFIED",
    "P060-PHY-P2-006": "UNVERIFIED",
    "P060-PHY-P2-007": "PRESERVE",
    "P060-PHY-P2-008": "CORRECT",
}
STEP44_CONFLICT_DISPOSITIONS = {
    "CONFLICT-DISCHARGE-LABEL": "PRESERVE",
    "CONFLICT-X-XBAR": "CORRECT",
    "CONFLICT-WIDTH-STATE": "CORRECT",
    "CONFLICT-BACKGROUND-PRIMITIVE": "CORRECT",
    "CONFLICT-POINTWISE-REPRESENTATIVE-T": "CORRECT",
    "CONFLICT-CONTROL-VOLUME": "PRESERVE",
    "CONFLICT-LAG-TIMEBASE": "CORRECT",
    "CONFLICT-LCO-T-CURVATURE": "CORRECT",
    "CONFLICT-SIGNED-ICA": "CORRECT",
    "CONFLICT-ZERO-CURRENT-HYSTERESIS": "UNVERIFIED",
}


def primary_disposition(source: dict[str, Any]) -> str:
    source_id = source["source_id"]
    family = source["source_family"]
    if family == "STEP40_SOURCE_FINDING":
        return {"P060-S40-F01": "CORRECT", "P060-S40-F02": "UNVERIFIED", "P060-S40-F03": "CORRECT"}[source_id]
    if family == "STEP40_GROUND_NOT_FOUND":
        return "UNVERIFIED"
    if family == "STEP41_CLAIM":
        if source_id in S41_PRESERVE:
            return "PRESERVE"
        if source_id in S41_THEORY:
            return "THEORY_ONLY"
        if source_id == "CLM-031":
            return "EMPIRICAL_ONLY"
        return "UNVERIFIED"
    if family == "STEP41_DEFECT_CORRECTION":
        return "CORRECT"
    if family == "STEP41_CONTRADICTION":
        return "PRESERVE"
    if family == "STEP41_UNRESOLVED":
        return "PRESERVE" if source_id == "UNR-008" else "UNVERIFIED"
    if family == "STEP42_RUNTIME_FINDING":
        if source_id == "P060-S42-RT-P1-006" or source_id == "P060-S42-RT-P2-009":
            return "PRESERVE"
        return "CORRECT"
    if family == "STEP42_VISUAL_FINDING":
        return "UNVERIFIED" if source_id == "VIS-P2-04" else "CORRECT"
    if family == "STEP43_TRACE_ROW":
        if source_id in TRACE_PRESERVE:
            return "PRESERVE"
        if source_id in TRACE_EMPIRICAL:
            return "EMPIRICAL_ONLY"
        if source_id in TRACE_THEORY:
            return "THEORY_ONLY"
        return "CORRECT"
    if family == "STEP43_FINDING":
        if source_id in {"P1-43-003", "P1-43-011"}:
            return "THEORY_ONLY"
        if source_id == "P1-43-005":
            return "UNVERIFIED"
        if source_id == "P2-43-013":
            return "PRESERVE"
        return "CORRECT"
    if family == "STEP44_PHYSICS_FINDING":
        return STEP44_FINDING_DISPOSITIONS[source_id]
    if family == "STEP44_SOURCE_CONFLICT":
        return STEP44_CONFLICT_DISPOSITIONS[source_id]
    raise ValueError(f"unmapped source family: {family}")


TARGET_OVERRIDES = {
    "P060-S40-F01": 61,
    "P060-S40-F02": 69,
    "P060-S40-F03": 69,
    "P060-S40-GNF-001": 71,
    "P060-S40-GNF-002": 71,
    "P060-S40-GNF-003": 78,
    "P060-S40-GNF-004": 78,
    "P060-S40-GNF-005": 78,
    "CLM-006": 73,
    "CLM-008": 67,
    "CLM-012": 73,
    "CLM-014": 74,
    "CLM-015": 67,
    "CLM-017": 67,
    "CLM-021": 67,
    "CLM-022": 73,
    "CLM-027": 67,
    "CLM-028": 69,
    "CLM-029": 67,
    "CLM-030": 71,
    "CLM-031": 67,
    "CLM-032": 67,
    "CLM-035": 67,
    "CLM-036": 78,
    "DCR-CU-11": 73,
    "UNR-001": 78,
    "UNR-002": 81,
    "UNR-003": 71,
    "UNR-004": 67,
    "UNR-005": 67,
    "UNR-006": 71,
    "UNR-007": 69,
    "UNR-008": 69,
    "UNR-009": 69,
    "UNR-010": 71,
    "UNR-011": 71,
    "P060-S42-RT-P2-009": 68,
    "VIS-P2-01": 89,
    "VIS-P2-02": 89,
    "VIS-P2-03": 89,
    "VIS-P2-04": 89,
    "TRC-CH1-CENTER-THERMO": 73,
    "TRC-CH1-HYSTERESIS": 75,
    "TRC-CH1-BROADENING-BUDGET": 77,
    "TRC-CH1-LAG-LENGTH": 76,
    "TRC-CH1-TAIL-CAUSAL": 76,
    "TRC-CH1-LOW-CURRENT-HYS-LIMIT": 76,
    "TRC-CH1-LCO-DIRECTION-CENTER": 78,
    "TRC-CH1-LCO-HYSTERESIS": 78,
    "TRC-CH1-LCO-ENTROPY-ELECTRONIC": 78,
    "TRC-CH1-LCO-PEAK": 78,
    "TRC-CH1-MSMR-MAP": 73,
    "TRC-CH1-LCO-FULL-PLUGIN": 78,
    "TRC-CH2-PARTITION-LOGISTIC": 73,
    "TRC-CH2-PARTITION-BW": 75,
    "TRC-CH2-CONFIGURATIONAL": 73,
    "TRC-CH2-VIBRATIONAL-ELECTRONIC": 81,
    "TRC-CH2-EINSTEIN-ROUNDTRIP": 81,
    "TRC-CH2-MIXING-IMPLICIT": 74,
    "TRC-CH2-MIXING-WEIGHTED": 73,
    "TRC-CH2-WIDTH-T-DEPENDENCE": 73,
    "TRC-CH2-HYSTERESIS-REVERSIBLE": 81,
    "TRC-CH2-REVERSIBLE-HEAT": 81,
    "TRC-CH2-COMPLETE-SYNTHESIS": 69,
    "TRC-CH2-REGRESSION-WITNESSES": 67,
    "TRC-CH2-DOC-LEADS-BOUNDARY": 69,
    "P1-43-001": 73,
    "P1-43-002": 78,
    "P1-43-003": 81,
    "P1-43-004": 69,
    "P1-43-005": 76,
    "P1-43-011": 77,
    "P1-43-012": 81,
    "P2-43-008": 68,
    "P2-43-013": 69,
    "P060-PHY-P1-001": 76,
    "P060-PHY-P1-002": 74,
    "P060-PHY-P1-003": 75,
    "P060-PHY-P1-004": 73,
    "P060-PHY-P1-005": 76,
    "P060-PHY-P1-006": 78,
    "P060-PHY-P1-007": 81,
    "P060-PHY-P1-008": 74,
    "P060-PHY-P1-009": 71,
    "P060-PHY-P1-010": 77,
    "P060-PHY-P1-011": 67,
    "P060-PHY-P1-012": 76,
    "P060-PHY-P2-001": 81,
    "P060-PHY-P2-002": 76,
    "P060-PHY-P2-003": 73,
    "P060-PHY-P2-004": 74,
    "P060-PHY-P2-005": 81,
    "P060-PHY-P2-006": 78,
    "P060-PHY-P2-007": 67,
    "P060-PHY-P2-008": 73,
    "CONFLICT-DISCHARGE-LABEL": 74,
    "CONFLICT-X-XBAR": 74,
    "CONFLICT-WIDTH-STATE": 73,
    "CONFLICT-BACKGROUND-PRIMITIVE": 74,
    "CONFLICT-POINTWISE-REPRESENTATIVE-T": 67,
    "CONFLICT-CONTROL-VOLUME": 74,
    "CONFLICT-LAG-TIMEBASE": 76,
    "CONFLICT-LCO-T-CURVATURE": 78,
    "CONFLICT-SIGNED-ICA": 67,
    "CONFLICT-ZERO-CURRENT-HYSTERESIS": 76,
}


def target_phase(source: dict[str, Any]) -> int:
    source_id = source["source_id"]
    if source_id in TARGET_OVERRIDES:
        return TARGET_OVERRIDES[source_id]
    family = source["source_family"]
    if family.startswith("STEP40") or family.startswith("STEP41"):
        return 61
    if family == "STEP42_RUNTIME_FINDING" or family == "STEP43_FINDING" or family == "STEP43_TRACE_ROW":
        return 67
    raise ValueError(f"target phase missing for {source_id}")


def acceptance(source_id: str, disposition: str, target: int, summary: str) -> str:
    verb = {
        "PRESERVE": "Preserve as an active internal-lineage constraint and add a regression or audit gate preventing loss of",
        "CORRECT": "Correct the documented implementation, test, or artifact contract and add a persistent failure gate for",
        "EMPIRICAL_ONLY": "Retain only as bounded empirical evidence, record its observed domain, and prohibit theoretical promotion of",
        "THEORY_ONLY": "Retain only as a bounded theoretical obligation and withhold implementation or material promotion until evidence closes",
        "UNVERIFIED": f"Keep unverified until Phase {target} records source-backed evidence and a persistent acceptance gate for",
    }[disposition]
    return f"{source_id}: {verb} {summary}"


NEW_BLOCKER_MEMBERSHIP = {
    "P060-BD-NEW-001": (
        "P060-PHY-P1-002", "P060-PHY-P2-004", "CONFLICT-BACKGROUND-PRIMITIVE"
    ),
    "P060-BD-NEW-002": ("P060-PHY-P1-011", "CONFLICT-SIGNED-ICA"),
    "P060-BD-NEW-003": (
        "P060-PHY-P1-007", "TRC-CH2-HYSTERESIS-REVERSIBLE", "P1-43-003"
    ),
    "P060-BD-NEW-004": ("P060-PHY-P1-009",),
    "P060-BD-NEW-005": ("CONFLICT-POINTWISE-REPRESENTATIVE-T",),
}


TOUCH_MAP = {
    "P059-CFR-RM-001": ["P060-PHY-P2-005"],
    "P059-CFR-RM-002": ["P060-PHY-P2-001"],
    "P059-CFR-RM-005": ["P060-PHY-P1-010"],
    "P059-CFR-RM-006": ["P060-PHY-P1-004", "P060-PHY-P2-008"],
    "P059-CFR-RM-007": ["P060-PHY-P1-004", "P060-PHY-P1-010"],
    "P059-CFR-RM-008": ["P060-PHY-P1-009"],
    "P059-CFR-RM-009": ["P060-PHY-P1-006", "P060-PHY-P2-006"],
    "P059-CFR-RM-010": ["P060-PHY-P1-006", "P060-PHY-P2-006"],
    "P059-CFR-RM-012": [f"P060-PHY-P2-{index:03d}" for index in range(1, 7)],
    "P059-CFR-CF-01": ["P060-PHY-P2-003", "P060-PHY-P2-007"],
    "P059-CFR-CF-02": ["P060-PHY-P2-001"],
    "P059-CFR-CF-03": ["P060-PHY-P1-001", "P060-PHY-P1-002", "P060-PHY-P1-011", "P060-PHY-P2-004"],
    "P059-CFR-CF-04": ["P060-PHY-P1-008"],
    "P059-CFR-CF-05": ["P060-PHY-P1-005"],
    "P059-CFR-CF-06": ["P060-PHY-P1-007", "P060-PHY-P1-008"],
    "P059-CFR-CF-07": ["P060-PHY-P1-006"],
    "P059-CFR-CF-09": ["P060-PHY-P1-009"],
    "P059-CFR-CF-11": ["P060-PHY-P2-007"],
    "P059-CFR-RB-01": ["P060-PHY-P1-001"],
    "P059-CFR-RB-02": ["P060-PHY-P1-003", "P060-PHY-P2-001"],
    "P059-CFR-RB-03": ["P060-PHY-P1-003"],
    "P059-CFR-RB-04": ["P060-PHY-P1-004", "P060-PHY-P2-008"],
    "P059-CFR-RB-05": ["P060-PHY-P1-001", "P060-PHY-P2-002"],
    "P059-CFR-RB-06": ["P060-PHY-P1-012"],
    "P059-CFR-RB-07": ["P060-PHY-P1-005"],
    "P059-CFR-RB-08": ["P060-PHY-P1-005", "P060-PHY-P1-012"],
    "P059-CFR-RB-09": ["P060-PHY-P1-006", "P060-PHY-P1-009", "P060-PHY-P2-006"],
    "P059-CFR-RB-10": ["P060-PHY-P1-002", "P060-PHY-P1-010", "P060-PHY-P1-011"],
    "P059-CFR-NS-04": [f"P060-PHY-P2-{index:03d}" for index in range(1, 7)],
    "P059-CFR-ED-02": ["P060-PHY-P1-006", "P060-PHY-P1-009", "P060-PHY-P2-006"],
    "P059-CFR-BD-NEW-002": ["P060-PHY-P2-005"],
    "P059-CFR-BD-NEW-004": ["P060-PHY-P2-001"],
    "P059-CFR-BD-NEW-006": ["P060-PHY-P1-010"],
}


def affected_surface(source: dict[str, Any], target: int) -> list[str]:
    return [
        source["source_artifact_path"],
        f"Phase {target} implementation/test/artifact acceptance surface for {source['source_id']}",
    ]


def build_dispositions(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    carry_by_source: dict[str, list[str]] = defaultdict(list)
    for carry_id, source_ids in TOUCH_MAP.items():
        for source_id in source_ids:
            carry_by_source[source_id].append(carry_id)
    blocker_by_source: dict[str, str] = {}
    for blocker_id, members in NEW_BLOCKER_MEMBERSHIP.items():
        for source_id in members:
            if source_id in blocker_by_source:
                raise ValueError(f"source assigned to two new blockers: {source_id}")
            blocker_by_source[source_id] = blocker_id
    dispositions: list[dict[str, Any]] = []
    for ordinal, source in enumerate(manifest, 1):
        primary = primary_disposition(source)
        if primary not in ALLOWED_DISPOSITIONS or primary in {"SUPERSEDE", "REJECT"}:
            raise ValueError(f"invalid active disposition for {source['source_id']}: {primary}")
        target = target_phase(source)
        horizon = "PRE_FREEZE_061_069" if target <= 69 else "CONDITIONAL_070_PLUS"
        dispositions.append(
            {
                "acceptance_criterion": acceptance(
                    source["source_id"], primary, target, source["source_summary"]
                ),
                "activation_gate": ACTIVATION_GATE,
                "affected_implementation_test_artifact": affected_surface(source, target),
                "authority_boundary": AUTHORITY,
                "blocker_family_id": blocker_by_source.get(source["source_id"]),
                "carry_forward_links": sorted(carry_by_source[source["source_id"]]),
                "disposition_id": f"P060-DISP-{ordinal:04d}",
                "downstream_target_phases": [],
                "evidence_paths": source["evidence_paths"],
                "external_material_truth_validated": False,
                "external_scientific_truth_validated": False,
                "primary_disposition": primary,
                "source_anchors": source["source_anchors"],
                "source_family": source["source_family"],
                "source_ids": [source["source_id"]],
                "source_record_sha256": source["source_record_sha256"],
                "target_horizon": horizon,
                "target_phase": target,
            }
        )
    return dispositions


def build_disposition_artifact(
    input_metadata: list[dict[str, Any]], manifest: list[dict[str, Any]]
) -> dict[str, Any]:
    dispositions = build_dispositions(manifest)
    primary_counts = dict(sorted(Counter(row["primary_disposition"] for row in dispositions).items()))
    all_members = [source_id for row in dispositions for source_id in row["source_ids"]]
    source_ids = [row["source_id"] for row in manifest]
    orphan_count = len(set(source_ids) - set(all_members))
    duplicate_memberships = len(all_members) - len(set(all_members))
    return {
        "artifact_kind": "PHASE_060_V1019_DISPOSITION_MATRIX",
        "authority_boundary": AUTHORITY,
        "dispositions": dispositions,
        "gate_summary": {
            "activation_gate": ACTIVATION_GATE,
            "allowed_primary_dispositions": list(ALLOWED_DISPOSITIONS),
            "disposition_conflict_count": duplicate_memberships,
            "disposition_count": len(dispositions),
            "duplicate_disposition_membership_count": duplicate_memberships,
            "duplicate_source_identity_count": len(source_ids) - len(set(source_ids)),
            "external_validity_promotion_count": sum(
                row["external_material_truth_validated"] or row["external_scientific_truth_validated"]
                for row in dispositions
            ),
            "missing_acceptance_authority_target_affected_count": sum(
                not row["acceptance_criterion"]
                or not row["authority_boundary"]
                or not row["affected_implementation_test_artifact"]
                or not (61 <= row["target_phase"] <= 90)
                for row in dispositions
            ),
            "primary_disposition_counts": primary_counts,
            "source_expected": 173,
            "source_manifest_count": len(manifest),
            "source_orphan_count": orphan_count,
            "status": "PASS",
        },
        "generation": {
            "active_branch": ACTIVE_BRANCH,
            "builder": "Codex/work/v1019_phase060/build_phase060_step45_dispositions.py",
            "canonical_json": "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true",
            "deterministic": True,
            "production_imported": False,
        },
        "inputs": input_metadata,
        "phase": 60,
        "schema_version": "phase060-step45-dispositions-v1",
        "source_commit": SOURCE_COMMIT,
        "source_manifest": manifest,
        "step": "45.1",
    }


def check_new_blocker_collisions() -> None:
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PRE_STEP45_COMMIT, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError(
            "the immutable pre-Step45 collision baseline is not an ancestor of HEAD: "
            f"{PRE_STEP45_COMMIT}: {ancestor.stderr.strip()}"
        )
    for blocker_id in NEW_BLOCKER_MEMBERSHIP:
        completed = subprocess.run(
            ["git", "grep", "-n", "-F", blocker_id, PRE_STEP45_COMMIT, "--", "Codex"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0:
            raise ValueError(
                "new blocker ID already occurs in the immutable pre-Step45 Codex baseline: "
                f"{blocker_id}: "
                f"{completed.stdout.strip()}"
            )
        if completed.returncode not in (0, 1):
            raise RuntimeError(completed.stderr.strip())


NEW_BLOCKER_DEFINITIONS = (
    {
        "blocker_id": "P060-BD-NEW-001",
        "category": "REPAIR_BLOCKER",
        "target_phase": 74,
        "acceptance_criterion": "Define the background charge primitive Q_bg, its reference state, and whether it enters the composition residual; add charge-conservation and reference-state tests that distinguish C_bg=dQ_bg/dV from Q_bg.",
        "old_collision_candidates": ["CF-03"],
        "non_double_count_basis": "P059-CFR-CF-03 preserves charge conservation and capacity accounting, but its inherited acceptance does not define the missing background charge primitive or reference state.",
    },
    {
        "blocker_id": "P060-BD-NEW-002",
        "category": "REPAIR_BLOCKER",
        "target_phase": 67,
        "acceptance_criterion": "Freeze separate public observables for the signed derivative dQ/dV and the positive ICA magnitude, map charge/discharge direction explicitly, and add sign-regression tests for both contracts.",
        "old_collision_candidates": ["RB-10", "CF-04"],
        "non_double_count_basis": "P059-CFR-RB-10 covers measurement mapping and P059-CFR-CF-04 preserves reaction-direction labels; neither inherited acceptance separates the signed derivative from the positive ICA magnitude.",
    },
    {
        "blocker_id": "P060-BD-NEW-003",
        "category": "NEW_SCOPE_BLOCKER",
        "target_phase": 81,
        "acceptance_criterion": "Derive and implement the reversible charge/discharge branch-average heat path, state the small-hysteresis linear-order domain, and test exact branch averaging against the bounded equilibrium-center approximation.",
        "old_collision_candidates": ["CF-06"],
        "non_double_count_basis": "P059-CFR-CF-06 preserves bounded reversible-heat sign identities, but its inherited acceptance does not require branch-average heat closure or the approximation-error domain.",
    },
    {
        "blocker_id": "P060-BD-NEW-004",
        "category": "EVIDENCE_DEBT",
        "target_phase": 71,
        "acceptance_criterion": "Establish primary-source authority for transition-specific Graphite kinetic and interaction parameters, retain fit-only values as unverified, and record exact claim-to-source adjudication before material use.",
        "old_collision_candidates": ["RM-008", "ED-02"],
        "non_double_count_basis": "P059-CFR-RM-008 and P059-CFR-ED-02 concern LCO parameters and validation; this blocker is limited to transition-specific Graphite kinetic and interaction parameter authority.",
    },
    {
        "blocker_id": "P060-BD-NEW-005",
        "category": "REPAIR_BLOCKER",
        "target_phase": 67,
        "acceptance_criterion": "Select and document pointwise T(V) or representative T_rep for each branch, lag, equilibrium, and heat path, then add tests proving every path consumes the selected temperature state.",
        "old_collision_candidates": [],
        "non_double_count_basis": "No inherited carry-forward acceptance criterion selects pointwise T(V) versus representative T_rep for each implementation path.",
    },
)


def build_new_blockers(manifest_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    check_new_blocker_collisions()
    blockers = []
    for definition in NEW_BLOCKER_DEFINITIONS:
        blocker_id = definition["blocker_id"]
        source_ids = list(NEW_BLOCKER_MEMBERSHIP[blocker_id])
        target = definition["target_phase"]
        evidence_paths = sorted(
            {path for source_id in source_ids for path in manifest_by_id[source_id]["evidence_paths"]}
        )
        source_hashes = {
            source_id: manifest_by_id[source_id]["source_record_sha256"] for source_id in source_ids
        }
        source_anchors = [
            {
                "source_anchors": manifest_by_id[source_id]["source_anchors"],
                "source_id": source_id,
            }
            for source_id in source_ids
        ]
        blockers.append(
            {
                **definition,
                "activation_gate": ACTIVATION_GATE,
                "affected_implementation_test_artifact": [
                    f"Phase {target} implementation/test/artifact acceptance surface for {blocker_id}"
                ],
                "authority_boundary": AUTHORITY,
                "evidence_paths": evidence_paths,
                "external_material_truth_validated": False,
                "external_scientific_truth_validated": False,
                "source_anchors": source_anchors,
                "source_ids": source_ids,
                "source_record_sha256": source_hashes,
                "status": "OPEN",
                "target_horizon": "PRE_FREEZE_061_069" if target <= 69 else "CONDITIONAL_070_PLUS",
            }
        )
    return blockers


def build_delta_artifact(
    input_metadata: list[dict[str, Any]],
    inputs: dict[str, Any],
    manifest: list[dict[str, Any]],
) -> dict[str, Any]:
    manifest_by_id = {row["source_id"]: row for row in manifest}
    inherited = []
    for source in inputs[P59_REGISTER]["items"]:
        carry_id = source["carry_forward_id"]
        touch_ids = TOUCH_MAP.get(carry_id, [])
        unknown = set(touch_ids) - set(manifest_by_id)
        if unknown:
            raise ValueError(f"unknown touch source IDs for {carry_id}: {sorted(unknown)}")
        touch_evidence = sorted(
            {path for source_id in touch_ids for path in manifest_by_id[source_id]["evidence_paths"]}
        )
        inherited.append(
            {
                "acceptance_criterion_after": source["acceptance_criterion"],
                "acceptance_criterion_before": source["acceptance_criterion"],
                "acceptance_satisfied": False,
                "activation_gate_after": source["activation_gate"],
                "activation_gate_before": source["activation_gate"],
                "authority_boundary_after": source["authority_boundary"],
                "authority_boundary_before": source["authority_boundary"],
                "carry_forward_id": carry_id,
                "category_after": source["category"],
                "category_before": source["category"],
                "delta_status": "TOUCHED_NEW_EVIDENCE" if touch_ids else "UNCHANGED",
                "external_material_truth_validated": False,
                "external_scientific_truth_validated": False,
                "prior_record": source,
                "prior_record_sha256": sha256(record_bytes(source)),
                "resolution_status": "NOT_RESOLVED",
                "source_route_source_id": source["source_route"]["source_id"],
                "status_after": source["status"],
                "status_before": source["status"],
                "target_horizon_after": source["target_horizon"],
                "target_horizon_before": source["target_horizon"],
                "target_phase_after": source["target_phase"],
                "target_phase_before": source["target_phase"],
                "touch_evidence_paths": touch_evidence,
                "touch_source_ids": touch_ids,
            }
        )
    if len(inherited) != 52:
        raise ValueError("Phase 059 carry-forward register does not contain 52 items")
    before = Counter(row["status_before"] for row in inherited)
    after = Counter(row["status_after"] for row in inherited)
    if before != Counter({"OPEN": 41, "PRESERVED_ACTIVE": 11}) or after != before:
        raise ValueError(f"carry status invariant failed: before={before}, after={after}")
    blockers = build_new_blockers(manifest_by_id)
    delta_counts = Counter(row["delta_status"] for row in inherited)
    return {
        "artifact_kind": "PHASE_060_V1019_CARRY_FORWARD_DELTA",
        "authority_boundary": AUTHORITY,
        "gate_summary": {
            "acceptance_satisfied_count": sum(row["acceptance_satisfied"] for row in inherited),
            "activation_gate": ACTIVATION_GATE,
            "carry_forward_duplicate_count": len(inherited)
            - len({row["carry_forward_id"] for row in inherited}),
            "carry_forward_expected": 52,
            "carry_forward_missing_count": 52 - len(inherited),
            "delta_status_counts": dict(sorted(delta_counts.items())),
            "external_validity_promotion_count": sum(
                row["external_material_truth_validated"] or row["external_scientific_truth_validated"]
                for row in inherited + blockers
            ),
            "new_blocker_count": len(blockers),
            "new_blocker_duplicate_count": len(blockers)
            - len({row["blocker_id"] for row in blockers}),
            "resolution_status_counts": dict(
                sorted(Counter(row["resolution_status"] for row in inherited).items())
            ),
            "status_after_counts": dict(sorted(after.items())),
            "status_before_counts": dict(sorted(before.items())),
            "status": "PASS",
        },
        "generation": {
            "active_branch": ACTIVE_BRANCH,
            "builder": "Codex/work/v1019_phase060/build_phase060_step45_dispositions.py",
            "canonical_json": "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true",
            "deterministic": True,
            "production_imported": False,
        },
        "inherited_items": inherited,
        "inputs": input_metadata,
        "new_blockers": blockers,
        "phase": 60,
        "schema_version": "phase060-step45-carry-forward-delta-v1",
        "source_commit": SOURCE_COMMIT,
        "step": "45.1",
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
        ["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    if branch != ACTIVE_BRANCH:
        raise RuntimeError(f"unexpected active branch: {branch}")
    inputs, _raw_inputs, input_metadata = read_inputs()
    manifest = reconstruct_source_manifest(inputs)
    disposition = build_disposition_artifact(input_metadata, manifest)
    delta = build_delta_artifact(input_metadata, inputs, manifest)
    write_output(args.disposition_output, disposition)
    write_output(args.delta_output, delta)
    print(
        "PASS build Phase060 Step45.1 "
        f"sources={len(manifest)} dispositions={len(disposition['dispositions'])} "
        f"carry={len(delta['inherited_items'])} blockers={len(delta['new_blockers'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
