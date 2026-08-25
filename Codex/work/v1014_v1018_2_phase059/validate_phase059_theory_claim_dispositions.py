#!/usr/bin/env python3
"""Validate the Phase 059 Step 39.1 theory-claim disposition matrix."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any


BASELINE_COMMIT = "893d662be4f0e7720a6c741ad8e3d462e38e6ace"
ARTIFACT_PATH = Path("Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json")
HASH_BASIS = "Git blob bytes at baseline commit"
EXPECTED_SEMANTIC_SHA256 = "b251537f717fa2ed0faa6bb6e2949ba94d25832921ac501cd7ffadc8bf5d1135"
EXPECTED_INPUT_PATHS = (
    "Codex/results/PHASE_059_THEORY_SOURCE_INDEX.json",
    "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json",
    "Codex/results/PHASE_059_THEORY_LINEAGE_DIFF.json",
    "Codex/results/PHASE_059_THEORY_SOURCE_STRUCTURE_INDEX.md",
    "Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_REVIEW.md",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_REVIEW.md",
    "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_AUDIT.json",
    "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md",
    "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json",
    "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md",
    "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json",
    "Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md",
    "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json",
    "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md",
    "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json",
    "Codex/results/PHASE_059_V1015_HEAT_DETAILING_REVIEW.md",
    "Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json",
    "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_REVIEW.md",
    "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_AUDIT.json",
    "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_REVIEW.md",
    "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json",
    "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md",
    "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json",
    "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md",
    "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json",
    "Codex/results/PHASE_059_V1017_DOC_CITATION_REVIEW.md",
    "Codex/results/PHASE_059_V1017_DOC_CITATION_AUDIT.json",
    "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_REVIEW.md",
    "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_AUDIT.json",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md",
    "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_DIFF.json",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json",
    "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md",
    "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json",
    "Codex/results/PHASE_059_GOLDEN_NPZ_REVIEW.md",
    "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json",
    "Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md",
)
ALLOWED_DISPOSITIONS = {
    "PRESERVE",
    "CORRECT",
    "SUPERSEDE",
    "EMPIRICAL_ONLY",
    "THEORY_ONLY",
    "REJECT",
    "UNVERIFIED",
}
CONTRACT_PRIMARY_LABEL = {
    "P059-CON-001": "eq:vn",
    "P059-CON-002": None,
    "P059-CON-003": "eq:n0map",
    "P059-CON-004": "eq:fermifn",
    "P059-CON-005": "eq:xieq",
    "P059-CON-006": "eq:gxi",
    "P059-CON-007": "eq:app-binodal",
    "P059-CON-008": "eq:dUhys",
    "P059-CON-009": "eq:app-ch-F",
    "P059-CON-010": None,
    "P059-CON-011": "eq:logistic",
    "P059-CON-012": "eq:wbase",
    "P059-CON-013": "eq:ensavg",
    "P059-CON-014": "eq:belliden",
    "P059-CON-015": "eq:dVdT_config",
    "P059-CON-016": "eq:kuniv",
    "P059-CON-017": "eq:LV",
    "P059-CON-018": "eq:reversal",
    "P059-CON-019": "eq:lag",
    "P059-CON-020": "eq:Acut",
    "P059-CON-021": "eq:Lq",
    "P059-CON-022": None,
    "P059-CON-023": "eq:dwdT-nT",
    "P059-CON-024": None,
    "P059-CON-025": "eq:Uj",
    "P059-CON-026": "eq:Sconfig",
    "P059-CON-027": "eq:weighted",
    "P059-CON-028": "eq:hys_branch",
    "P059-CON-029": "eq:qrev",
    "P059-CON-030": "eq:Svib-einstein",
    "P059-CON-031": "eq:dSvib",
    "P059-CON-032": "eq:Svib_mode",
    "P059-CON-033": None,
    "P059-CON-034": "eq:Se",
    "P059-CON-035": "eq:ggate",
    "P059-CON-036": "eq:lco-xmap",
    "P059-CON-037": "eq:lco-dope",
    "P059-CON-038": "eq:lco-decomp",
}
MIXED_DISPOSITION_RESOLUTIONS = {
    ("P059-CON-001", "P059-CON-003"): {
        "final_disposition": "CORRECT",
        "rationale": (
            "P059-CON-001 retains the observation-layer current convention as empirical, "
            "while P059-CON-003 identifies its 3600/basis ambiguity. Correction is required "
            "without promoting the empirical convention to mechanistic authority."
        ),
    },
    ("P059-CON-011", "P059-CON-012"): {
        "final_disposition": "CORRECT",
        "rationale": (
            "P059-CON-011 requires separate symbols for ideal thermal width and empirical "
            "ensemble/two-phase width, while P059-CON-012 limits the fitted width factor to "
            "empirical-only status absent microscopic derivation. The role/symbol split is "
            "correction-required; logistic algebra itself is not the correction target."
        ),
    },
    ("P059-CON-015", "P059-CON-026"): {
        "final_disposition": "CORRECT",
        "rationale": (
            "P059-CON-026 preserves the ideal configurational-entropy identity under its "
            "stated assumptions, while P059-CON-015 requires correction of the derivative "
            "decomposition. The bounded identity is retained inside a correction-required claim."
        ),
    },
    ("P059-CON-018", "P059-CON-019"): {
        "final_disposition": "CORRECT",
        "rationale": (
            "P059-CON-018 preserves the normalized lag identity under its infinite-past "
            "boundary assumptions, while P059-CON-019 requires an explicit initial state or "
            "preconditioning segment and a finite-window convergence test. The normalized "
            "kernel is retained, but initial-history closure is correction-required."
        ),
    },
}
OCCURRENCE_FIELDS = (
    "equation_id",
    "path",
    "version",
    "family",
    "line_start",
    "line_end",
    "environment",
    "labels",
    "section",
    "normalized_sha256",
    "source_excerpt",
    "is_mathematical_definition",
    "source_read_status",
)


class ValidationFailure(RuntimeError):
    """Raised when the Step 39.1 artifact violates its frozen contract."""


def fail(message: str) -> None:
    raise ValidationFailure(message)


@lru_cache(maxsize=None)
def git_blob(path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{BASELINE_COMMIT}:{path}"],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        fail(f"cannot read frozen Git blob {path}: {exc.stderr.decode(errors='replace').strip()}")
    raise AssertionError("unreachable")


def recursive_node_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(recursive_node_count(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(recursive_node_count(item) for item in value)
    return 1


def canonical_semantic_sha256(document: dict[str, Any]) -> str:
    candidate = json.loads(json.dumps(document, ensure_ascii=False))
    candidate["determinism"]["semantic_sha256"] = ""
    canonical = json.dumps(
        candidate,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def compact(text: str, limit: int = 360) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


def require_nonempty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be non-empty text")


def ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def require_evidence_block(value: Any, field: str) -> None:
    if not isinstance(value, dict):
        fail(f"{field} must be an object")
    for key in ("status", "assessment", "evidence_paths"):
        if key not in value:
            fail(f"{field} missing {key}")
    require_nonempty_text(value["status"], f"{field}.status")
    require_nonempty_text(value["assessment"], f"{field}.assessment")
    paths = value["evidence_paths"]
    if not isinstance(paths, list) or not paths:
        fail(f"{field}.evidence_paths must be a non-empty list")
    for path in paths:
        if path not in EXPECTED_INPUT_PATHS:
            fail(f"{field} references non-corpus path {path!r}")


def resolve_contract_dispositions(
    contract_ids: list[str],
    contracts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source_dispositions = [
        {"contract_id": contract_id, "disposition": contracts[contract_id]["disposition"]}
        for contract_id in contract_ids
    ]
    if not contract_ids:
        return {
            "status": "NO_APPLICABLE_CONTRACT",
            "source_dispositions": [],
            "final_disposition": "UNVERIFIED",
            "unresolved_conflict": False,
            "rationale": (
                "No equation_or_label relation from the 38 frozen theory contracts applies "
                "to this exact equation group; no stronger disposition is inferred."
            ),
        }
    dispositions = {row["disposition"] for row in source_dispositions}
    if len(contract_ids) == 1:
        final_disposition = source_dispositions[0]["disposition"]
        return {
            "status": "SINGLE_APPLICABLE_CONTRACT",
            "source_dispositions": source_dispositions,
            "final_disposition": final_disposition,
            "unresolved_conflict": False,
            "rationale": (
                f"{contract_ids[0]} is the sole directly applicable contract; its "
                f"{final_disposition} disposition governs without external-authority upgrade."
            ),
        }
    if len(dispositions) == 1:
        final_disposition = source_dispositions[0]["disposition"]
        return {
            "status": "MULTI_CONTRACT_AGREEMENT",
            "source_dispositions": source_dispositions,
            "final_disposition": final_disposition,
            "unresolved_conflict": False,
            "rationale": (
                f"All directly applicable contracts {', '.join(contract_ids)} agree on "
                f"{final_disposition}; every assumption and required action remains retained."
            ),
        }
    key = tuple(contract_ids)
    if key not in MIXED_DISPOSITION_RESOLUTIONS:
        fail(f"mixed contract dispositions lack an explicit resolution: {contract_ids}")
    resolution = MIXED_DISPOSITION_RESOLUTIONS[key]
    return {
        "status": "MULTI_CONTRACT_MIXED_RESOLVED",
        "source_dispositions": source_dispositions,
        "final_disposition": resolution["final_disposition"],
        "unresolved_conflict": False,
        "rationale": resolution["rationale"],
    }


def validate_input_coverage(document: dict[str, Any]) -> None:
    rows = document.get("input_coverage")
    if not isinstance(rows, list):
        fail("input_coverage must be a list")
    if [row.get("path") for row in rows] != list(EXPECTED_INPUT_PATHS):
        fail("input coverage ordered path contract mismatch")
    total_lines = 0
    combined = hashlib.sha256()
    for path, row in zip(EXPECTED_INPUT_PATHS, rows, strict=True):
        blob = git_blob(path)
        lines = len(blob.splitlines())
        total_lines += lines
        combined.update(path.encode("utf-8") + b"\0" + blob)
        if row.get("hash_basis") != HASH_BASIS:
            fail(f"hash_basis mismatch for {path}")
        if row.get("lines") != lines or row.get("read_range") != f"1-{lines}":
            fail(f"line coverage mismatch for {path}")
        if row.get("sha256") != hashlib.sha256(blob).hexdigest():
            fail(f"Git-blob SHA-256 mismatch for {path}")
        if path.endswith(".json"):
            parsed = json.loads(blob)
            if row.get("parse_mode") != "FULL_RECURSIVE_JSON_TRAVERSAL":
                fail(f"JSON parse mode mismatch for {path}")
            if row.get("recursive_node_count") != recursive_node_count(parsed):
                fail(f"recursive node coverage mismatch for {path}")
        else:
            if row.get("parse_mode") != "FULL_TEXT_1_TO_EOF":
                fail(f"text parse mode mismatch for {path}")
            if row.get("recursive_node_count") != 0:
                fail(f"text recursive node count must be zero for {path}")
    counts = document.get("counts", {})
    if counts.get("input_files") != len(EXPECTED_INPUT_PATHS):
        fail("input_files count mismatch")
    if counts.get("input_lines") != total_lines:
        fail("input_lines count mismatch")
    if document.get("input_corpus_sha256") != combined.hexdigest():
        fail("frozen input corpus SHA-256 mismatch")


def validate_occurrence(occurrence: dict[str, Any], expected: dict[str, Any]) -> None:
    for field in OCCURRENCE_FIELDS:
        if occurrence.get(field) != expected.get(field):
            fail(f"{expected['equation_id']} occurrence field mismatch: {field}")
    if occurrence.get("physical_adjudication") != expected.get("physical_adjudication"):
        fail(f"{expected['equation_id']} physical_adjudication mismatch")
    if occurrence["line_start"] < 1 or occurrence["line_end"] < occurrence["line_start"]:
        fail(f"{expected['equation_id']} invalid line range")
    source_lines = git_blob(occurrence["path"]).decode("utf-8").splitlines()
    if occurrence["line_end"] > len(source_lines):
        fail(f"{expected['equation_id']} source line out of bounds")
    body = "\n".join(
        source_lines[occurrence["line_start"] - 1 : occurrence["line_end"]]
    )
    if occurrence["source_excerpt"] != compact(body):
        fail(f"{expected['equation_id']} stored source text disagrees with Git blob")
    normalized = compact(body, 100000)
    if occurrence["normalized_sha256"] != hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest():
        fail(f"{expected['equation_id']} normalized equation SHA-256 disagreement")


def reconstruct_contract_evidence_relations(
    claims: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    source_index: dict[str, Any],
    contract_matrix: dict[str, Any],
) -> list[dict[str, Any]]:
    occurrence_owners: dict[str, list[str]] = {}
    for claim in claims:
        for occurrence_id in claim.get("mapped_occurrence_ids", []):
            occurrence_owners.setdefault(occurrence_id, []).append(claim.get("claim_id"))
    route_by_contract = {route.get("contract_id"): route for route in routes}
    expected: list[dict[str, Any]] = []
    relation_number = 0
    for contract in contract_matrix["records"]:
        contract_id = contract["id"]
        if contract_id not in route_by_contract:
            fail(f"{contract_id} missing governing route before evidence reconstruction")
        primary_label = CONTRACT_PRIMARY_LABEL[contract_id]
        for evidence_index, evidence in enumerate(contract["evidence"]):
            relation_number += 1
            path = evidence["path"]
            if "\\" in path:
                fail(f"{contract_id} evidence[{evidence_index}] path is not POSIX")
            source_lines = git_blob(path).decode("utf-8").splitlines()
            line_start = evidence["line_start"]
            line_end = evidence["line_end"]
            if line_start < 1 or line_end < line_start or line_end > len(source_lines):
                fail(f"{contract_id} evidence[{evidence_index}] invalid source line range")
            nearby = "\n".join(
                source_lines[max(0, line_start - 3) : min(len(source_lines), line_end + 2)]
            )
            if compact(evidence["source_excerpt"], 100000) not in compact(nearby, 100000):
                fail(f"{contract_id} evidence[{evidence_index}] excerpt is not at source anchor")

            if evidence["kind"] == "equation_or_label":
                label = evidence.get("label")
                require_nonempty_text(label, f"{contract_id} evidence[{evidence_index}].label")
                matches = [
                    row
                    for row in source_index["equations"]
                    if row["version"] == "v1.0.18.2"
                    and row["path"] == path
                    and label in row["labels"]
                    and row["line_start"] <= line_start
                    and row["line_end"] >= line_end
                ]
                if len(matches) != 1:
                    fail(
                        f"{contract_id} evidence[{evidence_index}] {label} does not map "
                        "to exactly one v1.0.18.2 source occurrence"
                    )
                occurrence_id = matches[0]["equation_id"]
                owners = occurrence_owners.get(occurrence_id, [])
                if len(owners) != 1:
                    fail(
                        f"{contract_id} evidence[{evidence_index}] {label} does not have "
                        "exactly one claim owner"
                    )
                claim_id = owners[0]
                role = (
                    "PRIMARY_GOVERNING_EQUATION"
                    if label == primary_label
                    else "SECONDARY_APPLICABLE_EQUATION"
                )
            elif evidence["kind"] == "prose_regex":
                pattern = evidence.get("pattern")
                require_nonempty_text(pattern, f"{contract_id} evidence[{evidence_index}].pattern")
                source_text = "\n".join(source_lines)
                if len(re.findall(pattern, source_text)) != evidence.get("match_count"):
                    fail(f"{contract_id} evidence[{evidence_index}] prose match count mismatch")
                occurrence_id = None
                claim_id = route_by_contract[contract_id].get("claim_id")
                role = (
                    "PRIMARY_GOVERNING_PROSE"
                    if primary_label is None and evidence_index == 0
                    else "CONTRACT_CONTEXT_PROSE"
                )
            else:
                fail(f"{contract_id} evidence[{evidence_index}] illegal evidence kind")
            expected.append(
                {
                    "evidence_relation_id": f"P059-EVR-{relation_number:03d}",
                    "contract_id": contract_id,
                    "evidence_index": evidence_index,
                    "evidence_kind": evidence["kind"],
                    "evidence": evidence,
                    "claim_id": claim_id,
                    "source_occurrence_id": occurrence_id,
                    "role": role,
                }
            )
    return expected


def validate_claims(document: dict[str, Any]) -> None:
    source_index = json.loads(git_blob(EXPECTED_INPUT_PATHS[0]))
    contract_matrix = json.loads(git_blob(EXPECTED_INPUT_PATHS[1]))
    expected_occurrences = {row["equation_id"]: row for row in source_index["equations"]}
    expected_contracts = {row["id"]: row for row in contract_matrix["records"]}
    if len(expected_occurrences) != 973:
        fail("frozen source index no longer contains exactly 973 occurrences")
    if len(expected_contracts) != 38:
        fail("frozen contract matrix no longer contains exactly 38 contracts")

    claims = document.get("claims")
    routes = document.get("contract_routes")
    if not isinstance(claims, list) or not claims:
        fail("claims must be a non-empty list")
    if not isinstance(routes, list):
        fail("contract_routes must be a list")
    claim_ids = [claim.get("claim_id") for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        fail("duplicate claim_id")
    if claim_ids != [f"P059-TCL-{index:03d}" for index in range(1, len(claims) + 1)]:
        fail("claim ID order is not deterministic and sequential")
    grouping_keys = [claim.get("grouping_key") for claim in claims]
    if len(grouping_keys) != len(set(grouping_keys)):
        fail("duplicate grouping_key")
    if grouping_keys != sorted(grouping_keys):
        fail("claim grouping keys are not in deterministic order")
    claim_by_id = dict(zip(claim_ids, claims, strict=True))

    expected_evidence_relations = reconstruct_contract_evidence_relations(
        claims, routes, source_index, contract_matrix
    )
    evidence_relations = document.get("contract_evidence_relations")
    if not isinstance(evidence_relations, list):
        sentinel = next(
            row
            for row in expected_evidence_relations
            if row["contract_id"] == "P059-CON-009" and row["evidence_index"] == 1
        )
        fail(
            "missing full equation evidence relation P059-CON-009 evidence[1] "
            f"eq:app-ch-R -> {sentinel['claim_id']}"
        )
    if evidence_relations != expected_evidence_relations:
        missing = next(
            (row for row in expected_evidence_relations if row not in evidence_relations),
            None,
        )
        if missing:
            label = missing["evidence"].get("label", missing["evidence_kind"])
            fail(
                f"missing contract evidence relation {missing['contract_id']} "
                f"evidence[{missing['evidence_index']}] {label} -> {missing['claim_id']}"
            )
        fail("contract evidence relations contain a duplicate or falsified relation")
    relation_ids = [row["evidence_relation_id"] for row in evidence_relations]
    if len(relation_ids) != len(set(relation_ids)):
        fail("duplicate contract evidence relation ID")
    evidence_kind_counts = Counter(row["evidence_kind"] for row in evidence_relations)
    evidence_role_counts = Counter(row["role"] for row in evidence_relations)
    if len(evidence_relations) != 80:
        fail("contract evidence relation count must be exactly 80")
    if evidence_kind_counts != Counter({"equation_or_label": 51, "prose_regex": 29}):
        fail("contract evidence kind reconciliation mismatch")
    if evidence_role_counts["PRIMARY_GOVERNING_EQUATION"] != 33:
        fail("primary equation evidence link count mismatch")
    if evidence_role_counts["SECONDARY_APPLICABLE_EQUATION"] != 18:
        fail("secondary equation evidence link count mismatch")
    if evidence_role_counts["PRIMARY_GOVERNING_PROSE"] != 5:
        fail("primary prose evidence relation count mismatch")
    if evidence_role_counts["CONTRACT_CONTEXT_PROSE"] != 24:
        fail("context prose evidence relation count mismatch")
    relations_by_claim: dict[str, list[dict[str, Any]]] = {}
    relations_by_contract: dict[str, list[dict[str, Any]]] = {}
    for relation in evidence_relations:
        relations_by_claim.setdefault(relation["claim_id"], []).append(relation)
        relations_by_contract.setdefault(relation["contract_id"], []).append(relation)

    assigned_occurrences: list[str] = []
    assigned_contracts: list[str] = []
    disposition_counts: Counter[str] = Counter()
    equation_group_count = 0
    contract_only_count = 0
    multi_contract_reconciliation_count = 0
    for claim in claims:
        claim_id = claim.get("claim_id")
        require_nonempty_text(claim_id, "claim_id")
        kind = claim.get("claim_kind")
        if kind not in {"EQUATION_GROUP", "CONTRACT_ONLY"}:
            fail(f"{claim_id} illegal claim_kind")
        disposition = claim.get("disposition")
        if disposition not in ALLOWED_DISPOSITIONS:
            fail(f"{claim_id} illegal or blank disposition")
        disposition_counts[disposition] += 1
        require_nonempty_text(claim.get("disposition_basis"), f"{claim_id}.disposition_basis")
        require_nonempty_text(claim.get("authority_boundary"), f"{claim_id}.authority_boundary")
        for field in ("derivation_audit", "literature_status", "code_impact", "data_authority"):
            require_evidence_block(claim.get(field), f"{claim_id}.{field}")

        occurrence_ids = claim.get("mapped_occurrence_ids")
        contract_ids = claim.get("mapped_contract_ids")
        occurrences = claim.get("occurrences")
        if not isinstance(occurrence_ids, list) or not isinstance(contract_ids, list):
            fail(f"{claim_id} mapping fields must be lists")
        if not isinstance(occurrences, list):
            fail(f"{claim_id}.occurrences must be a list")
        if len(occurrence_ids) != len(set(occurrence_ids)):
            fail(f"{claim_id} duplicates an occurrence internally")
        if len(contract_ids) != len(set(contract_ids)):
            fail(f"{claim_id} duplicates a contract internally")
        if len(contract_ids) > 1:
            fail(f"{claim_id} disposition conflict: more than one routed contract")
        if [item.get("equation_id") for item in occurrences] != occurrence_ids:
            fail(f"{claim_id} occurrence object/order mismatch")

        direct_relations = relations_by_claim.get(claim_id, [])
        expected_evidence_relation_ids = [
            relation["evidence_relation_id"] for relation in direct_relations
        ]
        expected_evidence_contract_ids = ordered_unique(
            [relation["contract_id"] for relation in direct_relations]
        )
        if claim.get("evidence_relation_ids") != expected_evidence_relation_ids:
            fail(f"{claim_id} reverse evidence relation membership mismatch")
        if claim.get("evidence_contract_ids") != expected_evidence_contract_ids:
            fail(f"{claim_id} evidence contract membership mismatch")
        expected_applicable_contract_evidence = []
        for contract_id in expected_evidence_contract_ids:
            contract = expected_contracts[contract_id]
            contract_relations = relations_by_contract[contract_id]
            claim_contract_relations = [
                relation
                for relation in contract_relations
                if relation["claim_id"] == claim_id
            ]
            expected_applicable_contract_evidence.append(
                {
                    "contract_id": contract_id,
                    "topic": contract["topic"],
                    "source_disposition": contract["disposition"],
                    "closure_state": contract["closure_state"],
                    "assumptions": contract["assumptions"],
                    "required_action": contract["required_action"],
                    "direct_claim_relation_ids": [
                        relation["evidence_relation_id"]
                        for relation in claim_contract_relations
                    ],
                    "direct_equation_relation_ids": [
                        relation["evidence_relation_id"]
                        for relation in claim_contract_relations
                        if relation["evidence_kind"] == "equation_or_label"
                    ],
                    "all_contract_evidence_relation_ids": [
                        relation["evidence_relation_id"] for relation in contract_relations
                    ],
                    "all_contract_evidence": contract["evidence"],
                }
            )
        if claim.get("applicable_contract_evidence") != expected_applicable_contract_evidence:
            fail(f"{claim_id} applicable contract assumptions/actions/evidence mismatch")
        expected_resolution = resolve_contract_dispositions(
            expected_evidence_contract_ids, expected_contracts
        )
        if claim.get("disposition_resolution") != expected_resolution:
            fail(f"{claim_id} disposition reconciliation mismatch")
        if disposition != expected_resolution["final_disposition"]:
            fail(f"{claim_id} final disposition does not match explicit resolution")
        if len(expected_evidence_contract_ids) > 1:
            multi_contract_reconciliation_count += 1
        derivation_audit = claim["derivation_audit"]
        expected_derivation_contract_fields = {
            "source_contract_ids": expected_evidence_contract_ids,
            "source_contract_topics": [
                expected_contracts[contract_id]["topic"]
                for contract_id in expected_evidence_contract_ids
            ],
            "source_contract_closure_states": [
                {
                    "contract_id": contract_id,
                    "closure_state": expected_contracts[contract_id]["closure_state"],
                }
                for contract_id in expected_evidence_contract_ids
            ],
            "source_contract_assumptions": [
                {
                    "contract_id": contract_id,
                    "assumptions": expected_contracts[contract_id]["assumptions"],
                }
                for contract_id in expected_evidence_contract_ids
            ],
            "source_contract_required_actions": [
                {
                    "contract_id": contract_id,
                    "required_action": expected_contracts[contract_id]["required_action"],
                }
                for contract_id in expected_evidence_contract_ids
            ],
            "source_contract_evidence": [
                {
                    "contract_id": contract_id,
                    "evidence": expected_contracts[contract_id]["evidence"],
                }
                for contract_id in expected_evidence_contract_ids
            ],
        }
        for field, expected_value in expected_derivation_contract_fields.items():
            if derivation_audit.get(field) != expected_value:
                fail(f"{claim_id} derivation audit does not retain all {field}")

        if kind == "EQUATION_GROUP":
            equation_group_count += 1
            if not occurrence_ids:
                fail(f"{claim_id} equation group has no occurrences")
            normalized = claim.get("normalized_sha256")
            family = claim.get("family")
            labels = claim.get("labels")
            require_nonempty_text(normalized, f"{claim_id}.normalized_sha256")
            require_nonempty_text(family, f"{claim_id}.family")
            if not isinstance(labels, list):
                fail(f"{claim_id}.labels must be a list")
            expected_key = f"equation|{family}|{'|'.join(labels)}|{normalized}"
            if claim.get("grouping_key") != expected_key:
                fail(f"{claim_id} grouping key mismatch")
            for occurrence in occurrences:
                occurrence_id = occurrence.get("equation_id")
                if occurrence_id not in expected_occurrences:
                    fail(f"{claim_id} invalid occurrence reference {occurrence_id!r}")
                expected = expected_occurrences[occurrence_id]
                validate_occurrence(occurrence, expected)
                if (
                    occurrence["family"] != family
                    or occurrence["labels"] != labels
                    or occurrence["normalized_sha256"] != normalized
                ):
                    fail(f"{claim_id} mixes non-identical equation occurrences")
            expected_anchors = [
                {
                    "path": item["path"],
                    "version": item["version"],
                    "line_start": item["line_start"],
                    "line_end": item["line_end"],
                    "environment": item["environment"],
                    "labels": item["labels"],
                    "normalized_sha256": item["normalized_sha256"],
                    "source_excerpt": item["source_excerpt"],
                }
                for item in occurrences
            ]
            if claim.get("source_anchors") != expected_anchors:
                fail(f"{claim_id} source anchors mismatch")
            lineage = claim.get("lineage")
            if not isinstance(lineage, dict):
                fail(f"{claim_id}.lineage must be an object")
            if lineage.get("versions") != [item["version"] for item in occurrences]:
                fail(f"{claim_id} lineage versions mismatch")
            if lineage.get("copy_forward_exact") != (len(occurrences) > 1):
                fail(f"{claim_id} copy-forward flag mismatch")
            variants = lineage.get("version_specific_variant_claim_ids")
            if not isinstance(variants, list) or claim_id not in variants:
                fail(f"{claim_id} missing explicit version-variant lineage")
        else:
            contract_only_count += 1
            if occurrence_ids or occurrences:
                fail(f"{claim_id} contract-only claim carries equation occurrences")
            if len(contract_ids) != 1:
                fail(f"{claim_id} contract-only claim must route exactly one contract")
            expected_key = f"contract-only|{contract_ids[0]}"
            if claim.get("grouping_key") != expected_key:
                fail(f"{claim_id} contract-only grouping key mismatch")
            if claim.get("normalized_sha256") is not None:
                fail(f"{claim_id} contract-only normalized_sha256 must be null")
            if claim.get("source_anchors") != expected_contracts[contract_ids[0]]["evidence"]:
                fail(f"{claim_id} contract-only source anchors mismatch")

        for occurrence_id in occurrence_ids:
            assigned_occurrences.append(occurrence_id)
        for contract_id in contract_ids:
            if contract_id not in expected_contracts:
                fail(f"{claim_id} invalid contract reference {contract_id!r}")
            assigned_contracts.append(contract_id)
            if contract_id not in claim["evidence_contract_ids"]:
                fail(f"{claim_id} governing contract lacks an evidence relation")

    if Counter(assigned_occurrences) != Counter({key: 1 for key in expected_occurrences}):
        fail("973-occurrence assignment is not exactly once")
    if Counter(assigned_contracts) != Counter({key: 1 for key in expected_contracts}):
        fail("38-contract routing is not exactly once")
    if multi_contract_reconciliation_count != 5:
        fail("multi-contract reconciliation count must be exactly 5")
    equation_claims = [claim for claim in claims if claim["claim_kind"] == "EQUATION_GROUP"]
    lineage_groups: dict[tuple[str, tuple[str, ...]], list[str]] = {}
    for claim in equation_claims:
        if claim["labels"]:
            key = (claim["family"], tuple(claim["labels"]))
            lineage_groups.setdefault(key, []).append(claim["claim_id"])
    for claim in equation_claims:
        if claim["labels"]:
            key = (claim["family"], tuple(claim["labels"]))
            expected_variants = lineage_groups[key]
        else:
            expected_variants = [claim["claim_id"]]
        if claim["lineage"]["version_specific_variant_claim_ids"] != expected_variants:
            fail(f"{claim['claim_id']} version-specific lineage mapping mismatch")

    route_contracts = [route.get("contract_id") for route in routes]
    if route_contracts != list(expected_contracts):
        fail("contract route order/coverage mismatch")
    for route in routes:
        contract_id = route["contract_id"]
        claim_id = route.get("claim_id")
        if claim_id not in claim_by_id:
            fail(f"{contract_id} route references invalid claim")
        claim = claim_by_id[claim_id]
        if claim["mapped_contract_ids"] != [contract_id]:
            fail(f"{contract_id} forward/reverse route mismatch")
        if route.get("source_contract_disposition") != expected_contracts[contract_id]["disposition"]:
            fail(f"{contract_id} route disposition mismatch")
        require_nonempty_text(route.get("route_basis"), f"{contract_id}.route_basis")
        anchor = route.get("primary_anchor")
        if not isinstance(anchor, dict):
            fail(f"{contract_id}.primary_anchor must be an object")
        for field in ("path", "line_start", "line_end", "source_excerpt"):
            if anchor.get(field) is None or anchor.get(field) == "":
                fail(f"{contract_id}.primary_anchor missing {field}")
        source_evidence = expected_contracts[contract_id]["evidence"]
        if anchor not in source_evidence:
            fail(f"{contract_id} primary anchor is not exact source-contract evidence")
        primary_role = (
            "PRIMARY_GOVERNING_EQUATION"
            if CONTRACT_PRIMARY_LABEL[contract_id] is not None
            else "PRIMARY_GOVERNING_PROSE"
        )
        primary_relations = [
            relation
            for relation in relations_by_contract[contract_id]
            if relation["role"] == primary_role
        ]
        if len(primary_relations) != 1:
            fail(f"{contract_id} does not have exactly one primary evidence relation")
        if (
            primary_relations[0]["claim_id"] != claim_id
            or primary_relations[0]["evidence"] != anchor
        ):
            fail(f"{contract_id} governing route/evidence relation mismatch")

    counts = document.get("counts", {})
    expected_counts = {
        "source_occurrences": 973,
        "source_occurrences_assigned": len(assigned_occurrences),
        "unique_claims": len(claims),
        "equation_group_claims": equation_group_count,
        "contract_only_claims": contract_only_count,
        "theory_contracts": 38,
        "theory_contracts_routed": len(assigned_contracts),
        "unassigned_occurrences": 0,
        "orphan_contracts": 0,
        "invalid_anchors": 0,
        "disposition_conflicts": 0,
        "unresolved_disposition_conflicts": 0,
        "multi_contract_reconciliation_count": multi_contract_reconciliation_count,
        "contract_evidence_records": len(evidence_relations),
        "equation_evidence_links": evidence_kind_counts["equation_or_label"],
        "prose_evidence_records": evidence_kind_counts["prose_regex"],
        "primary_equation_evidence_links": evidence_role_counts[
            "PRIMARY_GOVERNING_EQUATION"
        ],
        "secondary_equation_evidence_links": evidence_role_counts[
            "SECONDARY_APPLICABLE_EQUATION"
        ],
        "evidence_linked_equation_claims": sum(
            claim["claim_kind"] == "EQUATION_GROUP"
            and bool(claim["evidence_contract_ids"])
            for claim in claims
        ),
        "unmapped_equation_claims": sum(
            claim["claim_kind"] == "EQUATION_GROUP"
            and not claim["evidence_contract_ids"]
            for claim in claims
        ),
        "secondary_evidence_affected_claims": len(
            {
                relation["claim_id"]
                for relation in evidence_relations
                if relation["role"] == "SECONDARY_APPLICABLE_EQUATION"
            }
        ),
        "claim_disposition_counts": {
            disposition: disposition_counts[disposition]
            for disposition in sorted(ALLOWED_DISPOSITIONS)
        },
        "contract_disposition_counts": {
            disposition: Counter(
                contract["disposition"] for contract in contract_matrix["records"]
            )[disposition]
            for disposition in sorted(ALLOWED_DISPOSITIONS)
        },
        "disposition_counts": {
            disposition: disposition_counts[disposition]
            for disposition in sorted(ALLOWED_DISPOSITIONS)
        },
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"count reconciliation mismatch: {key}")
    unmapped_equation_groups = sum(
        claim["claim_kind"] == "EQUATION_GROUP" and not claim["evidence_contract_ids"]
        for claim in claims
    )
    unresolved = document.get("unresolved")
    if not isinstance(unresolved, list) or not unresolved:
        fail("unresolved must be a non-empty list")
    expected_unmapped_statement = (
        f"{unmapped_equation_groups} equation groups have no direct equation_or_label "
        "contract evidence and remain UNVERIFIED."
    )
    if unresolved[0] != expected_unmapped_statement:
        fail("unresolved unmapped-equation count mismatch")
    occurrence_sha = hashlib.sha256(
        "\n".join(expected_occurrences).encode("utf-8")
    ).hexdigest()
    contract_sha = hashlib.sha256("\n".join(expected_contracts).encode("utf-8")).hexdigest()
    if document.get("occurrence_universe_sha256") != occurrence_sha:
        fail("occurrence universe SHA-256 mismatch")
    if document.get("contract_universe_sha256") != contract_sha:
        fail("contract universe SHA-256 mismatch")


def validate() -> None:
    if not ARTIFACT_PATH.is_file():
        fail(f"missing artifact: {ARTIFACT_PATH.as_posix()}")
    document = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1:
        fail("schema_version mismatch")
    if document.get("baseline_commit") != BASELINE_COMMIT:
        fail("baseline_commit mismatch")
    if document.get("phase") != 59 or document.get("step") != "39.1":
        fail("phase/step mismatch")
    if document.get("status") != "PASS_P059_STEP_039_1_THEORY_CLAIM_DISPOSITION":
        fail("status mismatch")
    rules = document.get("rules_and_definitions", {})
    if rules.get("allowed_dispositions") != sorted(ALLOWED_DISPOSITIONS):
        fail("allowed disposition definition mismatch")
    require_nonempty_text(rules.get("grouping_key_definition"), "grouping_key_definition")
    require_nonempty_text(rules.get("contract_routing_rule"), "contract_routing_rule")
    require_nonempty_text(
        rules.get("contract_evidence_relation_rule"), "contract_evidence_relation_rule"
    )
    require_nonempty_text(
        rules.get("multi_contract_resolution_rule"), "multi_contract_resolution_rule"
    )
    require_nonempty_text(rules.get("unlabeled_lineage_rule"), "unlabeled_lineage_rule")
    require_nonempty_text(document.get("authority_boundary"), "authority_boundary")
    validate_input_coverage(document)
    validate_claims(document)
    actual_semantic = canonical_semantic_sha256(document)
    stored_semantic = document.get("determinism", {}).get("semantic_sha256")
    if stored_semantic != actual_semantic:
        fail("stored semantic SHA-256 mismatch")
    if actual_semantic != EXPECTED_SEMANTIC_SHA256:
        fail("canonical semantic SHA-256 lock mismatch")


def main() -> int:
    try:
        validate()
    except (ValidationFailure, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL_P059_STEP_039_1_THEORY_CLAIM_DISPOSITION: {exc}")
        return 1
    print("PASS_P059_STEP_039_1_THEORY_CLAIM_DISPOSITION")
    return 0


if __name__ == "__main__":
    sys.exit(main())
