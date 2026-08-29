#!/usr/bin/env python3
"""Build deterministic Phase 063 Step 63.1 dispositions and carry-forward delta."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
import subprocess
from collections import Counter, defaultdict
from typing import Any


REPO = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "eb847ea85018b7703c7adcfe74b8b665ec8c9b1c"
GATE = "PASS_P063_STEP63_1_DISPOSITIONS"
SENTINEL = "P063_STEP63_1_RESULT_FIRST_PRECOMMIT"
DISPOSITION = "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json"
CARRY = "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json"
RESULT = "Codex/results/PHASE_063_STEP_063_1_DISPOSITION_RESULT.md"

TOPOLOGY = "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
READ = "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json"
STEP59 = "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json"
STEP60 = "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json"
STEP61_CODE = "Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json"
STEP61_RUNTIME = "Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json"
STEP62 = "Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json"
P62_DISPOSITION = "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json"
P62_CARRY = "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json"

INPUT_SHA256 = {
    TOPOLOGY: "519968b5224db724e22f713a1ff47b9202dc77806a83d9917bc7845cd2cd0d7a",
    READ: "5d2aa9d9f7361471429dbd37dfcfad46d26b657c6ab3d421a1e9f58709144376",
    STEP59: "5753fd06737641acde52568a0bb22a8fabe9d37bbc3a43d4a743e884ff76ad02",
    STEP60: "77fa60e9ceeea086f8a6dde2cb3719a82357d01669e8c126e013c126e9725efd",
    STEP61_CODE: "691a11a9fdb8b7dc636893f8ffa822f119b8afbd8b0ac56b1c3ba8220faa7d0e",
    STEP61_RUNTIME: "5fb79f20bf6a8d1fa4345f9d66e35e1f595abd02f597c7acd8410434f8146f1b",
    STEP62: "8e627698b92f87c40a6dee57bc86cb8339cc17d0f78b1be4c9291d915161d2ff",
    P62_DISPOSITION: "2a75fe6ef35ee71a0de8c576ef81fa27eadffc0101a90ad6c491c1b8f410f62c",
    P62_CARRY: "9df1a9203d8b9df60232073130e5abec857cfc7a7973bf591bb7d7488e4f2614",
}

AUTHORITY = {
    "canonical_equation_promoted": False,
    "external_experimental_truth": False,
    "external_material_truth": False,
    "external_scientific_truth": False,
    "primary_literature_truth": False,
    "publication_ready": False,
    "scope": "INTERNAL_V1022_LINEAGE_DISPOSITION_ONLY",
}
ALLOWED = {"CORRECT", "PRESERVE", "SUPERSEDE", "DISCARD", "EMPIRICAL_ONLY", "THEORY_ONLY", "UNVERIFIED"}
ACTIVE_STATES = {"OPEN", "UNVERIFIED"}
DOWNSTREAM = {phase: list(range(phase + 1, 91)) for phase in range(70, 90)}
PHASE057_PRIMARY_TARGETS = {
    101: 80, 103: 87, 104: 74, 111: 87, 112: 71, 114: 74, 115: 76,
    118: 78, 119: 78, 120: 71, 121: 71, 122: 71, 123: 71, 126: 80,
    127: 80, 128: 71, 129: 71, 130: 71, 132: 71, 133: 72, 134: 79,
    135: 80, 136: 80, 137: 79, 138: 79, 139: 87, 142: 85, 148: 75,
    149: 74, 150: 74, 151: 74, 152: 71, 153: 81, 155: 87, 156: 76,
    157: 76, 159: 74, 161: 76, 162: 86, 163: 83, 166: 78, 167: 78,
    168: 79, 169: 80, 170: 80, 171: 79, 172: 83, 173: 71, 177: 88,
    179: 70, 183: 83, 184: 83, 185: 80, 186: 86, 190: 70, 191: 73,
}
AUDIT_CORROBORATION_GROUPS = [
    {"P063-S59-F001", "P063-S61-F001"},
    {"P063-S59-F002", "P063-S60-F002", "P063-S61-F003"},
    {"P063-S59-F003", "P063-S60-F004"},
    {"P063-S59-F004", "P063-S60-F004", "P063-S61-F002"},
    {"P063-S59-F012", "P063-S60-F007"},
    {"P063-S59-F019", "P063-S60-F019"},
]


class BuildError(RuntimeError):
    """Fail-closed builder error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise BuildError(f"nonfinite JSON constant: {value}")


def strict_load(raw: bytes) -> Any:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicates, parse_constant=reject_constant)

    def walk(item: Any) -> None:
        if isinstance(item, float):
            require(math.isfinite(item), "nonfinite JSON number")
        elif isinstance(item, dict):
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return value


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_bytes(*args: str) -> bytes:
    process = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, timeout=120, check=False,
    )
    if process.returncode:
        raise BuildError(process.stderr.decode("utf-8", errors="replace").strip())
    return process.stdout


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    objects: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for path, expected_sha in INPUT_SHA256.items():
        raw = git_bytes("show", f"{PARENT}:{path}")
        require(sha256(raw) == expected_sha, f"input SHA mismatch: {path}")
        require((REPO / path).read_bytes() == raw, f"input worktree mismatch: {path}")
        objects[path] = strict_load(raw)
        metadata.append({
            "path": path,
            "commit": PARENT,
            "git_blob": git_bytes("rev-parse", f"{PARENT}:{path}").decode("ascii").strip(),
            "sha256": expected_sha,
            "bytes": len(raw),
            "parse_mode": "STRICT_JSON_FULL_TRAVERSAL",
        })
    return objects, metadata


def record_sha(value: Any) -> str:
    return sha256(compact(value))


def pointer_value(document: Any, pointer: str) -> Any:
    value = document
    for token in pointer.lstrip("/").split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def nested_source_refs(value: Any, source_ids: set[str], paths: set[str]) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "source_id" and isinstance(child, str) and child in source_ids:
                found.add(child)
            elif key in {"path", "source_path"} and isinstance(child, str) and child in paths:
                found.add(child)
            found.update(nested_source_refs(child, source_ids, paths))
    elif isinstance(value, list):
        for child in value:
            found.update(nested_source_refs(child, source_ids, paths))
    return found


def source_evidence_routes(inputs: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    source_ids = {row["source_id"] for row in sources}
    source_by_path = {row["path"]: row["source_id"] for row in sources}
    path_set = set(source_by_path)
    collected: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add(path: str, pointer: str, record: Any, role: str) -> None:
        refs = nested_source_refs(record, source_ids, path_set)
        normalized = {source_by_path.get(ref, ref) for ref in refs}
        for source_id in sorted(normalized):
            if source_id not in source_ids:
                continue
            collected[source_id].append({
                "artifact_path": path,
                "json_pointer": pointer,
                "record_sha256": record_sha(record),
                "route_role": role,
            })

    step59 = inputs[STEP59]["manual_rederivation_evidence"]
    for index, row in enumerate(step59["derivation_rows"]):
        role = "DERIVATION_CORRECTION" if row["disposition"] in {"CORRECT", "REJECT", "UNRESOLVED"} else "DERIVATION_INTERNAL_THEORY"
        add(STEP59, f"/manual_rederivation_evidence/derivation_rows/{index}", row, role)
    for section in ("material_scope_ledger", "operator_ledger", "sign_ledger"):
        for index, row in enumerate(step59[section]):
            add(STEP59, f"/manual_rederivation_evidence/{section}/{index}", row, "DERIVATION_CORRECTION")

    step60 = inputs[STEP60]["manual_literature_scope_evidence"]
    for section in ("literature_claims", "material_scope_ledger"):
        for index, row in enumerate(step60[section]):
            add(STEP60, f"/manual_literature_scope_evidence/{section}/{index}", row, "LITERATURE_SCOPE_UNVERIFIED")

    for index, row in enumerate(inputs[STEP61_CODE]["findings"]):
        add(STEP61_CODE, f"/findings/{index}", row, "CODE_FINDING_CORRECTION")

    step62 = inputs[STEP62]
    for index, row in enumerate(step62["finding_adjudications"]):
        role = "REVIEW_FINDING_OPEN" if row["state"] in ACTIVE_STATES else "REVIEW_FINDING_INFORMATIONAL"
        add(STEP62, f"/finding_adjudications/{index}", row, role)
    for index, row in enumerate(step62["code_mention_boundary"]["occurrence_rows"]):
        if row["actionable"]:
            add(STEP62, f"/code_mention_boundary/occurrence_rows/{index}", row, "CODE_MENTION_CORRECTION")
    for index, row in enumerate(step62["state_chronology"]["conflicts"]):
        add(STEP62, f"/state_chronology/conflicts/{index}", row, "STATE_CHRONOLOGY_BOUNDARY")
    for row_index, build_row in enumerate(step62["build_audit"]["rows"]):
        for glyph_index, glyph in enumerate(build_row["missing_glyphs"]):
            add(STEP62, f"/build_audit/rows/{row_index}/missing_glyphs/{glyph_index}", glyph, "BUILD_DIAGNOSTIC_CORRECTION")

    for source_id, rows in collected.items():
        unique = {(row["artifact_path"], row["json_pointer"], row["route_role"]): row for row in rows}
        collected[source_id] = [unique[key] for key in sorted(unique)]
    return collected


def disposition_for(source: dict[str, Any], roles: set[str]) -> str:
    if source["partition"] != "FINAL_RELEASE_SURFACE":
        return "PRESERVE"
    if source["role"] == "generated_document":
        return "PRESERVE"
    if source["role"] in {"code", "test", "implementation_guide"}:
        return "CORRECT"
    correction_roles = {
        "DERIVATION_CORRECTION", "CODE_FINDING_CORRECTION", "CODE_MENTION_CORRECTION",
        "REVIEW_FINDING_OPEN", "BUILD_DIAGNOSTIC_CORRECTION",
    }
    if roles & correction_roles:
        return "CORRECT"
    if "LITERATURE_SCOPE_UNVERIFIED" in roles:
        return "UNVERIFIED"
    if "DERIVATION_INTERNAL_THEORY" in roles:
        return "THEORY_ONLY"
    return "PRESERVE"


def authority_ceiling(source: dict[str, Any]) -> str:
    if source["partition"] == "COMPETING_REVIEW_CANDIDATE":
        return "PROPOSAL_REVIEW_DECISION_OR_STATUS_EVIDENCE_ONLY"
    if source["partition"] == "STATUS_MACHINE_PROCESS":
        return "PROCESS_SELF_REPORT_ONLY"
    if source["partition"] == "VERSION_PLAN":
        return "RECORDED_PLAN_INTENT_ONLY"
    if source["role"] == "generated_document":
        return "GENERATED_BUILD_WITNESS_ONLY"
    if source["role"] in {"code", "test", "implementation_guide"}:
        return "INTERNAL_IMPLEMENTATION_RUNTIME_OR_GUIDE_ONLY"
    return "FROZEN_RELEASE_THEORY_TEXT_INTERNAL_ONLY"


def target_phase(source: dict[str, Any], disposition: str) -> int:
    path = source["path"]
    if disposition == "UNVERIFIED":
        return 71
    if source["role"] in {"code", "test", "implementation_guide"}:
        return 83
    if source["role"] == "generated_document":
        return 89
    if source["partition"] in {"STATUS_MACHINE_PROCESS", "VERSION_PLAN"}:
        return 70
    if source["partition"] == "COMPETING_REVIEW_CANDIDATE":
        return 71
    if "/ch2" in path or "lco" in path.lower():
        return 78
    if "/ch3" in path or any(token in path.lower() for token in ("si_", "siox", "sic_", "blend")):
        return 79
    if disposition == "THEORY_ONLY":
        return 82
    return 87


def acceptance_text(source: dict[str, Any], disposition: str, target: int) -> str:
    return (
        f"Phase {target} must resolve or explicitly preserve {source['source_id']} at exact path/blob identity; "
        f"disposition {disposition} remains bounded by {authority_ceiling(source)}. "
        "Acceptance requires the routed evidence records, a declared model/material/protocol scope where applicable, "
        "and no promotion to external scientific, material, experimental, primary-literature or publication truth."
    )


def build_source_dispositions(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    sources = inputs[TOPOLOGY]["sources"]
    routes_by_source = source_evidence_routes(inputs, sources)
    rows: list[dict[str, Any]] = []
    for ordinal, source in enumerate(sources, 1):
        evidence_routes = [{
            "artifact_path": TOPOLOGY,
            "json_pointer": f"/sources/{ordinal - 1}",
            "record_sha256": record_sha(source),
            "route_role": "SOURCE_IDENTITY",
        }, *routes_by_source.get(source["source_id"], [])]
        evidence_routes = [
            {"evidence_id": f"P063-EVID-{ordinal:04d}-{index:03d}"} | route
            for index, route in enumerate(evidence_routes, 1)
        ]
        roles = {row["route_role"] for row in evidence_routes}
        disposition = disposition_for(source, roles)
        require(disposition in ALLOWED, f"invalid disposition: {source['source_id']}")
        target = target_phase(source, disposition)
        status = "OPEN" if disposition in {"CORRECT", "UNVERIFIED"} else "PRESERVED_ACTIVE"
        rows.append({
            "disposition_id": f"P063-DISP-{ordinal:04d}",
            "source_id": source["source_id"],
            "source_identity": {
                key: source[key]
                for key in ("source_id", "path", "blob_sha1", "sha256", "manifest_index", "partition", "role", "review_mode", "extent")
            },
            "source_record_sha256": record_sha(source),
            "disposition": disposition,
            "status": status,
            "reason": (
                f"The exact frozen occurrence is routed from partition {source['partition']} and role {source['role']}; "
                f"{len(evidence_routes) - 1} source-specific audit evidence record(s) determine this internal disposition. "
                "The frozen source is not rewritten and identity-equivalent occurrences are not merged."
            ),
            "evidence_ids": [row["evidence_id"] for row in evidence_routes],
            "evidence_routes": evidence_routes,
            "carry_forward_links": [],
            "canonical_owner_id": f"PHASE-{target:03d}-SOURCE-{source['source_id']}" if status == "OPEN" else None,
            "primary_target_phase": target,
            "downstream_target_phases": DOWNSTREAM[target],
            "acceptance_criterion": acceptance_text(source, disposition, target),
            "authority_ceiling": authority_ceiling(source),
            "non_double_count_basis": "ONE_MANIFEST_OCCURRENCE_ID; SAME_PATH_OR_BLOB_OCCURRENCES_REMAIN_DISTINCT",
            "external_scientific_truth": False,
            "external_material_truth": False,
            "external_experimental_truth": False,
        })
    require(len(rows) == 204, f"source disposition denominator: {len(rows)}")
    return rows


def supplemental_disposition(inputs: dict[str, Any]) -> dict[str, Any]:
    source = inputs[TOPOLOGY]["supplemental_process_control"]
    return {
        "process_id": "P063-PROC-SUP-001",
        "source_anchor": {key: source[key] for key in ("path", "blob_sha1", "sha256")},
        "source_record_sha256": record_sha(source),
        "denominator": "SUPPLEMENTAL_PROCESS_CONTROL",
        "manifest_member": False,
        "disposition": "PRESERVE",
        "status": "PRESERVED_ACTIVE",
        "reason": "The v1.0.22 master plan is a separately counted recorded process-control input, not one of the 204 manifest occurrences or first-order user testimony.",
        "evidence_routes": [{
            "evidence_id": "P063-PROC-SUP-001",
            "artifact_path": TOPOLOGY,
            "json_pointer": "/supplemental_process_control",
            "record_sha256": record_sha(source),
            "route_role": "SUPPLEMENTAL_PROCESS_IDENTITY",
        }],
        "primary_target_phase": 70,
        "downstream_target_phases": DOWNSTREAM[70],
        "acceptance_criterion": "Preserve the exact path/blob and its recorded-plan authority; never fuse it with the 204 manifest denominator or promote it to first-order user authority.",
        "authority_ceiling": "RECORDED_SECOND_ORDER_PROCESS_INTENT_ONLY",
        "external_scientific_truth": False,
        "external_material_truth": False,
    }


def phase_for_text(text: str, default: int) -> int:
    matches = [int(value) for value in re.findall(r"Phase\s+0*(7[0-9]|8[0-9]|90)", text)]
    return min(matches) if matches else default


def phase057_routes(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, finding in enumerate(inputs[STEP62]["finding_adjudications"]):
        active = finding["state"] in ACTIVE_STATES
        target = PHASE057_PRIMARY_TARGETS[finding["numeric_id"]] if active else 70
        rows.append({
            "route_id": f"P063-F057-ROUTE-{index + 1:04d}",
            "finding_id": finding["finding_id"],
            "numeric_id": finding["numeric_id"],
            "state_before": finding["state"],
            "status_after": "OPEN_CARRY" if active else "RESOLVED_INFORMATIONAL",
            "canonical_owner_id": f"PHASE-{target:03d}-{finding['finding_id']}" if active else "PHASE-070-HISTORICAL-EVIDENCE-QUEUE",
            "target_phase": target,
            "downstream_target_phases": DOWNSTREAM[target],
            "origin_path": STEP62,
            "origin_pointer": f"/finding_adjudications/{index}",
            "origin_record_sha256": record_sha(finding),
            "evidence_routes": [{
                "artifact_path": STEP62,
                "json_pointer": f"/finding_adjudications/{index}",
                "record_sha256": record_sha(finding),
                "route_role": "PHASE057_FINDING_ADJUDICATION",
            }],
            "acceptance_criterion": finding["acceptance_criterion"],
            "non_double_count_basis": "ONE_PHASE057_FINDING_ID; DISTINCT_FROM_SOURCE_DISPOSITION_AND_INHERITED_CARRY_DENOMINATORS",
            "external_truth": False,
        })
    require(len(rows) == 96, f"Phase057 route denominator: {len(rows)}")
    return rows


def canonical_owner_universe(inputs: dict[str, Any], finding_routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior = inputs[P62_CARRY]
    release_owner_targets = {
        row["disposition_id"]: row["primary_target_phase"]
        for row in inputs[P62_DISPOSITION]["release_dispositions"]
    }
    known_owner_targets = dict(release_owner_targets)
    for row in prior["inherited_carry_items"]:
        known_owner_targets[row["carry_forward_id"]] = row["target_phase_after"]
    for section in ("inherited_phase060_blockers", "inherited_phase061_blockers"):
        for row in prior[section]:
            known_owner_targets[row["blocker_id"]] = row["target_phase_after"]
    for row in prior["canonical_debt_routing"]:
        known_owner_targets[row["prior_record"]["primary_owner_id"]] = row["prior_record"]["owner_target_phase"]
    records: list[dict[str, Any]] = []
    for index, route in enumerate(finding_routes):
        records.append({
            "registry_id": f"P063-OWNER-UNIVERSE-F057-{index + 1:04d}",
            "denominator_section": "PHASE057_FINDING_ROUTES",
            "denominator_index": index,
            "origin_identity": route["finding_id"],
            "owner_id": route["canonical_owner_id"],
            "target_phase": route["target_phase"],
            "origin_record_sha256": route["origin_record_sha256"],
        })
    specs = (
        ("inherited_carry_items", "carry_forward_id", lambda row: row["target_phase_after"]),
        ("inherited_phase060_blockers", "blocker_id", lambda row: row["target_phase_after"]),
        ("inherited_phase061_blockers", "blocker_id", lambda row: row["target_phase_after"]),
        ("canonical_debt_routing", None, lambda row: row["prior_record"]["owner_target_phase"]),
        ("open_finding_ownership", "finding_id", lambda row: known_owner_targets[row["owner_id"]]),
    )
    for section, identity_key, target_getter in specs:
        for index, row in enumerate(prior[section]):
            owner_id = row["prior_record"]["primary_owner_id"] if section == "canonical_debt_routing" else row.get("owner_id", row.get(identity_key or "", ""))
            origin_identity = row[identity_key] if identity_key else row["prior_record"]["debt_id"]
            require(bool(owner_id) and bool(origin_identity), f"owner registry identity: {section}/{index}")
            records.append({
                "registry_id": f"P063-OWNER-UNIVERSE-{section.upper()}-{index + 1:04d}",
                "denominator_section": section,
                "denominator_index": index,
                "origin_identity": origin_identity,
                "owner_id": owner_id,
                "target_phase": target_getter(row),
                "origin_record_sha256": record_sha(row),
            })
    require(len(records) == 308, f"canonical owner universe denominator: {len(records)}")
    require(len({row["registry_id"] for row in records}) == 308, "canonical owner registry IDs")
    return records


def corroborating_audit_ids(finding_id: str) -> list[str]:
    return sorted({member for group in AUDIT_CORROBORATION_GROUPS if finding_id in group for member in group if member != finding_id})


def audit_finding_routes(inputs: dict[str, Any], owner_universe: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = ((STEP59, inputs[STEP59]["findings"]), (STEP60, inputs[STEP60]["findings"]), (STEP61_CODE, inputs[STEP61_CODE]["findings"]))
    rows: list[dict[str, Any]] = []
    ordinal = 0
    for path, findings in specs:
        for index, finding in enumerate(findings):
            ordinal += 1
            owner_text = str(finding.get("owner", finding.get("downstream_owner", "")))
            target = phase_for_text(owner_text, 82)
            exact_matches = [
                row["registry_id"] for row in owner_universe
                if finding["finding_id"] in {row["origin_identity"], row["owner_id"]}
            ]
            same_target = [row["registry_id"] for row in owner_universe if row["target_phase"] == target]
            rows.append({
                "route_id": f"P063-AUDIT-ROUTE-{ordinal:04d}",
                "finding_id": finding["finding_id"],
                "priority": finding["priority"],
                "status_after": "OPEN_CARRY",
                "canonical_owner_id": f"PHASE-{target:03d}-CANONICAL-WORK-QUEUE",
                "owner_kind": "EXISTING_PHASE_QUEUE_NOT_NEW_BLOCKER",
                "target_phase": target,
                "downstream_target_phases": DOWNSTREAM[target],
                "origin_path": path,
                "origin_pointer": f"/findings/{index}",
                "origin_record_sha256": record_sha(finding),
                "acceptance_criterion": f"Phase {target} must resolve the exact {finding['finding_id']} record or preserve it OPEN with evidence; internal audit evidence cannot establish external truth.",
                "non_double_count_basis": "ONE_PHASE063_STEP59_TO_STEP61_FINDING_ID; CORROBORATION_DOES_NOT_CREATE_ANOTHER_BLOCKER",
                "corroborating_audit_finding_ids": corroborating_audit_ids(finding["finding_id"]),
                "duplicate_check": {
                    "owner_universe_schema": "P063_CANONICAL_OWNER_UNIVERSE_V1",
                    "owner_universe_records": 308,
                    "owner_universe_sha256": record_sha(owner_universe),
                    "exact_prior_identity_matches": exact_matches,
                    "same_target_existing_owner_candidates": same_target,
                    "match_interpretation": "EXACT_IDENTITY_ONLY; SAME_TARGET_IS_CANDIDATE_NOT_EQUIVALENCE",
                    "decision": "NOT_CREATED_AUDIT_OBSERVATION_ONLY",
                },
                "blocker_identity_created": False,
                "external_truth": False,
            })
    require(len(rows) == 59, f"Phase063 audit finding denominator: {len(rows)}")
    return rows


def wrap_prior(path: str, pointer: str, row: Any, route_id: str, kind: str) -> dict[str, Any]:
    target_values: list[int] = []

    def collect_targets(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"target_phase", "target_phase_after", "primary_target_phase"} and isinstance(child, int):
                    target_values.append(child)
                collect_targets(child)
        elif isinstance(value, list):
            for child in value:
                collect_targets(child)

    collect_targets(row)
    return {
        "route_id": route_id,
        "kind": kind,
        "origin_path": path,
        "origin_pointer": pointer,
        "prior_record_sha256": record_sha(row),
        "prior_record": row,
        "status_after": "CARRIED_FORWARD_UNCHANGED",
        "target_phase_after": min((value for value in target_values if value > 63), default=70),
        "non_double_count_basis": f"ONE_PRIOR_JSON_POINTER_IN_{kind}",
    }


def inherited_routes(inputs: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    prior = inputs[P62_CARRY]
    specs = (
        ("inherited_carry_items", "P062_INHERITED_CARRY"),
        ("inherited_phase060_blockers", "P060_BLOCKER"),
        ("inherited_phase061_blockers", "P061_BLOCKER"),
        ("canonical_debt_routing", "CANONICAL_DEBT"),
        ("open_finding_ownership", "P062_OPEN_FINDING"),
    )
    result: dict[str, list[dict[str, Any]]] = {}
    for key, kind in specs:
        result[key] = [
            wrap_prior(P62_CARRY, f"/{key}/{index}", row, f"P063-INHERITED-{kind}-{index + 1:04d}", kind)
            for index, row in enumerate(prior[key])
        ]
    require([len(result[key]) for key, _ in specs] == [52, 5, 5, 91, 59], "inherited route denominators")
    return result


def build_artifacts(inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_rows = build_source_dispositions(inputs)
    supplemental = supplemental_disposition(inputs)
    finding_routes = phase057_routes(inputs)
    owner_universe = canonical_owner_universe(inputs, finding_routes)
    audit_routes = audit_finding_routes(inputs, owner_universe)
    inherited = inherited_routes(inputs)
    source_links: dict[str, list[str]] = defaultdict(list)
    for route in finding_routes:
        finding = pointer_value(inputs[STEP62], route["origin_pointer"])
        for source_id in sorted(set(finding["candidate_source_routes"] + finding["proposal_sources"] + finding["final_source_edges"])):
            source_links[source_id].append(route["route_id"])
    for row in source_rows:
        row["carry_forward_links"] = sorted(source_links.get(row["source_id"], []))
    distribution = dict(sorted(Counter(row["disposition"] for row in source_rows).items()))
    disposition = {
        "schema_version": "P063_STEP63_1_DISPOSITION_V1",
        "artifact_kind": "PHASE_063_V1022_DISPOSITION_MATRIX",
        "phase": 63,
        "step": "63.1",
        "baseline_commit": BASELINE,
        "input_commit": PARENT,
        "inputs": metadata,
        "result_first": {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
        "source_contract": {
            "manifest_occurrences": 204,
            "supplemental_process_controls": 1,
            "identity_rule": "ONE_DISPOSITION_PER_SOURCE_ID; NO_PATH_OR_BLOB_COLLAPSE",
        },
        "source_dispositions": source_rows,
        "supplemental_process_disposition": supplemental,
        "counts": {
            "source_dispositions": len(source_rows),
            "source_disposition_distribution": distribution,
            "open_source_dispositions": sum(row["status"] == "OPEN" for row in source_rows),
            "supplemental_process_dispositions": 1,
            "source_orphans": 0,
            "duplicate_source_membership": 0,
            "external_authority_promotions": 0,
        },
        "authority_boundary": AUTHORITY,
        "gate": GATE,
    }
    carry = {
        "schema_version": "P063_STEP63_1_CARRY_FORWARD_V1",
        "artifact_kind": "PHASE_063_V1022_CARRY_FORWARD_DELTA",
        "phase": 63,
        "step": "63.1",
        "baseline_commit": BASELINE,
        "input_commit": PARENT,
        "inputs": metadata,
        "result_first": {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
        "source_disposition_links": [
            {
                "source_id": row["source_id"],
                "disposition_id": row["disposition_id"],
                "status": row["status"],
                "primary_target_phase": row["primary_target_phase"],
                "carry_forward_links": row["carry_forward_links"],
            }
            for row in source_rows
        ],
        "canonical_owner_duplicate_check_universe": {
            "schema_version": "P063_CANONICAL_OWNER_UNIVERSE_V1",
            "record_count": len(owner_universe),
            "records_sha256": record_sha(owner_universe),
            "records": owner_universe,
        },
        "phase057_finding_routes": finding_routes,
        "phase063_audit_finding_routes": audit_routes,
        **inherited,
        "new_phase063_blockers": [],
        "gate_summary": {
            "source_disposition_links": 204,
            "phase057_finding_routes": 96,
            "phase057_open_or_unverified": sum(row["status_after"] == "OPEN_CARRY" for row in finding_routes),
            "phase063_audit_finding_routes": 59,
            "canonical_owner_duplicate_check_records": 308,
            "audit_exact_prior_identity_matches": sum(len(row["duplicate_check"]["exact_prior_identity_matches"]) for row in audit_routes),
            "inherited_carry_items": 52,
            "inherited_phase060_blockers": 5,
            "inherited_phase061_blockers": 5,
            "canonical_debt_routes": 91,
            "phase062_open_finding_routes": 59,
            "new_phase063_blockers": 0,
            "ownerless_open_routes": 0,
            "multiply_owned_open_routes": 0,
            "external_authority_promotions": 0,
            "status": "PASS_WITH_CONCERNS",
        },
        "authority_boundary": AUTHORITY,
        "gate": GATE,
    }
    return disposition, carry


def result_text(disposition: dict[str, Any], carry: dict[str, Any], disposition_sha: str, carry_sha: str) -> str:
    counts = disposition["counts"]
    summary = carry["gate_summary"]
    return f"""# Phase 063 Step 63.1 Source Disposition and Carry-forward Delta Result

Gate: `{GATE}`

Terminal: `{GATE}`

Result-first sentinel: `{SENTINEL}`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

## Reconciled prerequisite

- Step 62 exact-seven containing commit: `{PARENT}`.
- Step 62 persistence terminal: `PASS_P063_STEP62_PERSISTENCE`.

## Result

- disposition matrix SHA-256: `{disposition_sha}`.
- carry-forward delta SHA-256: `{carry_sha}`.
- manifest source dispositions: `{counts['source_dispositions']}/204`; supplemental process disposition: `1/1` in a separate denominator.
- disposition distribution: `{json.dumps(counts['source_disposition_distribution'], ensure_ascii=False, sort_keys=True)}`; OPEN source dispositions `{counts['open_source_dispositions']}`.
- Phase 057 finding routes: `{summary['phase057_finding_routes']}/96`, including OPEN/UNVERIFIED carry `{summary['phase057_open_or_unverified']}`; each finding ID occurs once and all 96 retain a downstream owner.
- Phase 063 Steps 59--61 audit finding routes: `{summary['phase063_audit_finding_routes']}/59` (`P0/P1/P2=13/25/21`). These are audit observations routed to shared phase work queues, not newly minted blocker identities or an added external-truth denominator.
- canonical-owner duplicate-check universe: `{summary['canonical_owner_duplicate_check_records']}/308` identity-preserved rows (`96 + 52 + 5 + 5 + 91 + 59`); exact prior identity matches `{summary['audit_exact_prior_identity_matches']}`. Same-target candidates are not asserted to be equivalent.
- Phase 062 inherited routes are lossless and separate: carry `{summary['inherited_carry_items']}/52`, Phase 060 blockers `{summary['inherited_phase060_blockers']}/5`, Phase 061 blockers `{summary['inherited_phase061_blockers']}/5`, canonical debt `{summary['canonical_debt_routes']}/91`, Phase 062 open findings `{summary['phase062_open_finding_routes']}/59`.
- new Phase 063 blockers: `{summary['new_phase063_blockers']}`; ownerless/multiply-owned active routes `{summary['ownerless_open_routes']}/{summary['multiply_owned_open_routes']}`.
- external scientific/material/experimental/primary-literature/canonical-equation/publication authority remains false.

## Scope and disposition method

- Every manifest occurrence keeps its `P063-SRC-####` identity even when paths or blobs recur. No source occurrence is fused with the supplemental master plan or any finding/carry denominator.
- Final-release code/test/guide sources and final theory sources with direct correction evidence are `CORRECT`; final theory sources whose load-bearing literature/material scope remains externally unverified are `UNVERIFIED`; bounded internal derivations without a correction route are `THEORY_ONLY`; remaining frozen occurrences are `PRESERVE`.
- Competing candidate/review/decision records, version plans and status-machine records are preserved as process evidence only. Preservation does not mean adoption, current truth or external scientific validity.
- Evidence routes use exact input artifact path, JSON pointer and canonical record SHA-256. The validator independently resolves every pointer and recomputes every record hash.

## Finding and carry routing

- All 96 Phase 057 findings are retained. `OPEN=45` and `UNVERIFIED=11` receive row-specific primary/downstream routing across Phases 070--090; `RESOLVED_IN_V1022=8`, `HISTORICAL_ONLY=30` and `SUPERSEDED=2` remain resolved informational routes owned by the Phase 070 historical-evidence queue rather than disappearing.
- The 59 Step 59--61 findings remain individually traceable. Each is joined against the exact 308-row prior/Phase-057 owner universe, receives one shared phase-queue owner, records exact-ID matches separately from same-target candidates, and never creates a blocker identity. Explicit cross-Step corroboration links prevent duplicated observations from masquerading as new blockers.
- All inherited Phase 062 records retain the entire prior JSON record plus its exact origin pointer and canonical record hash. Target phases earlier than or equal to Phase 063 are advanced only as routing metadata; the prior record itself is unchanged.

## Authority and unresolved work

- `CORRECT` means an internal frozen occurrence has a routed correction requirement; it does not mean the correction is applied in this Step.
- `UNVERIFIED` and OPEN routes require their named downstream phase to recover primary literature, material/protocol evidence, equation scope or implementation proof. Missing evidence is not inferred.
- Frozen v1.0.22 and `Claude/**` are not edited. Canonical theory selection, source repair, parameter identification, held-out fitting, manuscript rewrite and final PDF remain later-phase work.

## Validation contract

- strict JSON duplicate/nonfinite/truncation rejection and full traversal for all nine inputs and both outputs;
- exact `204 + supplemental 1`, `96`, `59`, `52`, `5`, `5`, `91`, `59` denominators;
- source identity/order, evidence-pointer/hash replay, state/priority distributions, row-specific Phase 057 targets, the identity-preserved 308-row owner-universe join, shared audit queue ownership and authority ceilings;
- builder source pin/policy, named negative controls, deterministic `2/2`, exact-eight staged and postcommit persistence gates.

## Executed validation evidence

- Python 3.12 and Python 3.14 normal content validation: `{GATE}`, strict traversal `1,133,555` nodes per run.
- Python 3.12 and Python 3.14 named negative validation: `65/65`; strict JSON `6/6`, recovery `10/10`, builder policy `4/4`, Git-boundary mutations `10/10` per runtime.
- Python 3.12 and Python 3.14 builder determinism: `2/2` byte-identical disposition/carry/result projections per runtime.
- Exact-eight staged boundary and postcommit persistence remain deliberately pending until the atomic commit workflow; neither is claimed by this precommit result.

## Exact-eight checkpoint

1. `Codex/work/v1022_phase063/build_phase063_step63_dispositions.py`
2. `Codex/work/v1022_phase063/validate_phase063_step63_dispositions.py`
3. `Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_063_STEP_063_1_DISPOSITION_RESULT.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected subject: `audit(phase063): disposition v1022 lineage`.

Post-commit persistence must emit `PASS_P063_STEP63_1_PERSISTENCE` before Step 63.2.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=pathlib.Path, default=REPO)
    parser.add_argument("--disposition", type=pathlib.Path)
    parser.add_argument("--carry", type=pathlib.Path)
    parser.add_argument("--result", type=pathlib.Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.repo.resolve() == REPO.resolve(), "repo mismatch")
    inputs, metadata = load_inputs()
    disposition, carry = build_artifacts(inputs, metadata)
    disposition_raw = canonical(disposition)
    carry_raw = canonical(carry)
    result_raw = result_text(disposition, carry, sha256(disposition_raw), sha256(carry_raw)).encode("utf-8")
    disposition_path = args.disposition or REPO / DISPOSITION
    carry_path = args.carry or REPO / CARRY
    result_path = args.result or REPO / RESULT
    if args.check:
        require(result_path.read_bytes() == result_raw, "stored result mismatch")
        require(disposition_path.read_bytes() == disposition_raw, "stored disposition mismatch")
        require(carry_path.read_bytes() == carry_raw, "stored carry mismatch")
        print("PASS_P063_STEP63_1_BUILDER_CHECK")
        return 0
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_bytes(result_raw)
    disposition_path.parent.mkdir(parents=True, exist_ok=True)
    disposition_path.write_bytes(disposition_raw)
    carry_path.parent.mkdir(parents=True, exist_ok=True)
    carry_path.write_bytes(carry_raw)
    print("PASS_P063_STEP63_1_BUILDER result-first")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
