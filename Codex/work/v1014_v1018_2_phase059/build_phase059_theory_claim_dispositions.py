#!/usr/bin/env python3
"""Build the Phase 059 Step 39.1 theory-claim disposition matrix."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from validate_phase059_theory_claim_dispositions import (
    ALLOWED_DISPOSITIONS,
    ARTIFACT_PATH,
    BASELINE_COMMIT,
    CONTRACT_PRIMARY_LABEL,
    EXPECTED_INPUT_PATHS,
    HASH_BASIS,
    canonical_semantic_sha256,
    recursive_node_count,
    resolve_contract_dispositions,
)


VERSION_ORDER = {
    "v1.0.14": 0,
    "v1.0.15": 1,
    "v1.0.16": 2,
    "v1.0.17": 3,
    "v1.0.18.1": 4,
    "v1.0.18.2": 5,
}
TOPIC_AUDIT_PATHS = {
    "coordinates": (
        "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md",
        "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json",
        "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_REVIEW.md",
        "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_AUDIT.json",
    ),
    "phase_separation": (
        "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md",
        "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json",
    ),
    "width": (
        "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md",
        "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md",
        "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json",
    ),
    "memory": (
        "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md",
        "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json",
        "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_REVIEW.md",
        "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json",
        "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_REVIEW.md",
        "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_AUDIT.json",
    ),
    "n_of_T": (
        "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md",
        "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json",
        "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md",
        "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json",
    ),
    "entropy_heat": (
        "Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md",
        "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json",
        "Codex/results/PHASE_059_V1015_HEAT_DETAILING_REVIEW.md",
        "Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json",
    ),
    "einstein_vibration": (
        "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md",
        "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json",
        "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md",
        "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json",
    ),
    "lco_electronic": (
        "Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md",
        "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json",
        "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md",
        "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json",
    ),
}


def git_blob(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{BASELINE_COMMIT}:{path}"],
        stderr=subprocess.PIPE,
    )


def json_blob(path: str) -> dict[str, Any]:
    return json.loads(git_blob(path))


def ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def occurrence_projection(row: dict[str, Any]) -> dict[str, Any]:
    fields = (
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
        "physical_adjudication",
    )
    return {field: deepcopy(row[field]) for field in fields}


def source_anchor_from_occurrence(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": row["path"],
        "version": row["version"],
        "line_start": row["line_start"],
        "line_end": row["line_end"],
        "environment": row["environment"],
        "labels": deepcopy(row["labels"]),
        "normalized_sha256": row["normalized_sha256"],
        "source_excerpt": row["source_excerpt"],
    }


def equation_grouping_key(row: dict[str, Any]) -> str:
    return (
        f"equation|{row['family']}|{'|'.join(row['labels'])}|"
        f"{row['normalized_sha256']}"
    )


def find_primary_anchor(contract: dict[str, Any], label: str | None) -> dict[str, Any]:
    if label is None:
        return deepcopy(contract["evidence"][0])
    matches = [row for row in contract["evidence"] if row.get("label") == label]
    if len(matches) != 1:
        raise RuntimeError(f"{contract['id']} does not have one primary anchor for {label}")
    return deepcopy(matches[0])


def common_evidence_blocks(
    topics: list[str],
    applicable_contracts: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    topic_paths = ordered_unique(
        [path for topic in topics for path in TOPIC_AUDIT_PATHS.get(topic, ())]
    )
    if applicable_contracts:
        contract_ids = [contract["id"] for contract in applicable_contracts]
        derivation_status = (
            "MULTI_CONTRACT_EVIDENCE_RECONCILED"
            if len(applicable_contracts) > 1
            else applicable_contracts[0]["disposition"]
        )
        derivation_assessment = (
            f"Directly applicable source contracts {', '.join(contract_ids)} are retained "
            "with every frozen assumption, required action, and evidence record. The claim's "
            "explicit disposition_resolution reconciles their dispositions."
        )
        contract_details = {
            "source_contract_ids": contract_ids,
            "source_contract_topics": [
                contract["topic"] for contract in applicable_contracts
            ],
            "source_contract_closure_states": [
                {
                    "contract_id": contract["id"],
                    "closure_state": contract["closure_state"],
                }
                for contract in applicable_contracts
            ],
            "source_contract_assumptions": [
                {
                    "contract_id": contract["id"],
                    "assumptions": deepcopy(contract["assumptions"]),
                }
                for contract in applicable_contracts
            ],
            "source_contract_required_actions": [
                {
                    "contract_id": contract["id"],
                    "required_action": contract["required_action"],
                }
                for contract in applicable_contracts
            ],
            "source_contract_evidence": [
                {
                    "contract_id": contract["id"],
                    "evidence": deepcopy(contract["evidence"]),
                }
                for contract in applicable_contracts
            ],
        }
    else:
        derivation_status = "UNVERIFIED_NOT_IN_38_CONTRACTS"
        derivation_assessment = (
            "This exact displayed-equation claim has source lineage evidence but no "
            "equation_or_label relation among the 38 source-linked theory contracts; a "
            "stronger derivation verdict is not inferred."
        )
        contract_details = {
            "source_contract_ids": [],
            "source_contract_topics": [],
            "source_contract_closure_states": [],
            "source_contract_assumptions": [],
            "source_contract_required_actions": [],
            "source_contract_evidence": [],
        }
    derivation_paths = ordered_unique(
        [
            "Codex/results/PHASE_059_THEORY_SOURCE_INDEX.json",
            "Codex/results/PHASE_059_THEORY_LINEAGE_DIFF.json",
            "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json",
            "Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md",
            *topic_paths,
        ]
    )
    derivation_audit = {
        "status": derivation_status,
        "assessment": derivation_assessment,
        "evidence_paths": derivation_paths,
        **contract_details,
    }
    literature_status = {
        "status": "UNVERIFIED_NO_PRIMARY_SOURCE_TRUTH_AUDIT",
        "assessment": (
            "Phase 059 verifies internal source/derivation lineage only. DOI metadata, "
            "primary full text, and exact claim support remain outside Step 39.1; no "
            "equation is promoted to externally verified literature authority."
        ),
        "evidence_paths": [
            "Codex/results/PHASE_059_V1017_DOC_CITATION_REVIEW.md",
            "Codex/results/PHASE_059_V1017_DOC_CITATION_AUDIT.json",
            "Codex/results/PHASE_059_COMPLETION_AUTHORITY_REVIEW.md",
        ],
    }
    required_action = (
        " ".join(contract["required_action"] for contract in applicable_contracts)
        if applicable_contracts
        else (
            "No implementation action may be inferred until a later conformance step maps "
            "this source equation to production behavior."
        )
    )
    code_impact = {
        "status": "DEFERRED_TO_STEP_39_3_NO_CODE_CHANGE",
        "assessment": (
            f"Step 39.1 changes no production code. {required_action} Full theory-code-"
            "test-artifact conformance is adjudicated in Step 39.3."
        ),
        "evidence_paths": ordered_unique(
            [
                "Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md",
                "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json",
                "Codex/results/PHASE_059_PRODUCTION_CODE_DIFF.json",
                *topic_paths,
            ]
        ),
    }
    data_authority = {
        "status": "INTERNAL_ONLY_NO_EXTERNAL_MATERIAL_VALIDATION",
        "assessment": (
            "The audited tests, probes, and golden files establish at most internal "
            "identities or derived-model snapshots. They load no public experimental "
            "dataset and grant no graphite/LCO/Si/blend material parameter authority."
        ),
        "evidence_paths": [
            "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md",
            "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json",
            "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md",
            "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json",
            "Codex/results/PHASE_059_GOLDEN_NPZ_REVIEW.md",
            "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json",
        ],
    }
    return derivation_audit, literature_status, code_impact, data_authority


def build_input_coverage() -> tuple[list[dict[str, Any]], int, str]:
    rows: list[dict[str, Any]] = []
    total_lines = 0
    combined = hashlib.sha256()
    for path in EXPECTED_INPUT_PATHS:
        blob = git_blob(path)
        lines = len(blob.splitlines())
        total_lines += lines
        combined.update(path.encode("utf-8") + b"\0" + blob)
        if path.endswith(".json"):
            parsed = json.loads(blob)
            parse_mode = "FULL_RECURSIVE_JSON_TRAVERSAL"
            nodes = recursive_node_count(parsed)
        else:
            blob.decode("utf-8")
            parse_mode = "FULL_TEXT_1_TO_EOF"
            nodes = 0
        rows.append(
            {
                "path": path,
                "lines": lines,
                "read_range": f"1-{lines}",
                "sha256": hashlib.sha256(blob).hexdigest(),
                "hash_basis": HASH_BASIS,
                "parse_mode": parse_mode,
                "recursive_node_count": nodes,
            }
        )
    return rows, total_lines, combined.hexdigest()


def build_claims(
    source_index: dict[str, Any],
    contract_matrix: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    occurrences = source_index["equations"]
    contracts = {row["id"]: row for row in contract_matrix["records"]}
    if set(CONTRACT_PRIMARY_LABEL) != set(contracts):
        raise RuntimeError("contract routing table does not cover the frozen 38-contract universe")

    groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for occurrence in occurrences:
        groups[equation_grouping_key(occurrence)].append(occurrence)
    if len(groups) != 180:
        raise RuntimeError(f"expected 180 exact equation groups, found {len(groups)}")

    draft_claims: list[dict[str, Any]] = []
    for grouping_key, rows in groups.items():
        rows = sorted(
            rows,
            key=lambda row: (
                VERSION_ORDER[row["version"]],
                row["path"],
                row["line_start"],
                row["equation_id"],
            ),
        )
        first = rows[0]
        draft_claims.append(
            {
                "claim_kind": "EQUATION_GROUP",
                "grouping_key": grouping_key,
                "family": first["family"],
                "labels": deepcopy(first["labels"]),
                "normalized_sha256": first["normalized_sha256"],
                "mapped_occurrence_ids": [row["equation_id"] for row in rows],
                "mapped_contract_ids": [],
                "_applicable_contract_ids": [],
                "_evidence_relation_ids": [],
                "occurrences": [occurrence_projection(row) for row in rows],
                "source_anchors": [source_anchor_from_occurrence(row) for row in rows],
            }
        )

    by_label: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in draft_claims:
        for label in claim["labels"]:
            by_label[label].append(claim)
    contract_to_claim: dict[str, dict[str, Any]] = {}
    for contract_id, label in CONTRACT_PRIMARY_LABEL.items():
        contract = contracts[contract_id]
        if label is None:
            draft = {
                "claim_kind": "CONTRACT_ONLY",
                "grouping_key": f"contract-only|{contract_id}",
                "family": None,
                "labels": [],
                "normalized_sha256": None,
                "mapped_occurrence_ids": [],
                "mapped_contract_ids": [contract_id],
                "_applicable_contract_ids": [],
                "_evidence_relation_ids": [],
                "occurrences": [],
                "source_anchors": deepcopy(contract["evidence"]),
            }
            draft_claims.append(draft)
            contract_to_claim[contract_id] = draft
            continue
        primary_anchor = find_primary_anchor(contract, label)
        candidates = [
            claim
            for claim in by_label[label]
            if any(
                row["version"] == "v1.0.18.2"
                and row["path"] == primary_anchor["path"]
                and label in row["labels"]
                for row in claim["occurrences"]
            )
        ]
        if len(candidates) != 1:
            raise RuntimeError(f"{contract_id}/{label}: expected one exact equation group")
        claim = candidates[0]
        if claim["mapped_contract_ids"]:
            raise RuntimeError(f"{contract_id}/{label}: duplicate contract disposition route")
        claim["mapped_contract_ids"] = [contract_id]
        contract_to_claim[contract_id] = claim

    draft_claims.sort(key=lambda claim: claim["grouping_key"])
    for index, claim in enumerate(draft_claims, start=1):
        claim["claim_id"] = f"P059-TCL-{index:03d}"

    occurrence_to_claim = {
        occurrence_id: claim
        for claim in draft_claims
        for occurrence_id in claim["mapped_occurrence_ids"]
    }
    contract_evidence_relations: list[dict[str, Any]] = []
    relation_number = 0
    for contract in contract_matrix["records"]:
        contract_id = contract["id"]
        primary_label = CONTRACT_PRIMARY_LABEL[contract_id]
        for evidence_index, evidence in enumerate(contract["evidence"]):
            relation_number += 1
            if evidence["kind"] == "equation_or_label":
                label = evidence["label"]
                matches = [
                    row
                    for row in occurrences
                    if row["version"] == "v1.0.18.2"
                    and row["path"] == evidence["path"]
                    and label in row["labels"]
                    and row["line_start"] <= evidence["line_start"]
                    and row["line_end"] >= evidence["line_end"]
                ]
                if len(matches) != 1:
                    raise RuntimeError(
                        f"{contract_id} evidence[{evidence_index}] {label}: expected one "
                        "v1.0.18.2 equation occurrence"
                    )
                source_occurrence_id = matches[0]["equation_id"]
                target_claim = occurrence_to_claim[source_occurrence_id]
                role = (
                    "PRIMARY_GOVERNING_EQUATION"
                    if label == primary_label
                    else "SECONDARY_APPLICABLE_EQUATION"
                )
            else:
                source_occurrence_id = None
                target_claim = contract_to_claim[contract_id]
                role = (
                    "PRIMARY_GOVERNING_PROSE"
                    if primary_label is None and evidence_index == 0
                    else "CONTRACT_CONTEXT_PROSE"
                )
            relation_id = f"P059-EVR-{relation_number:03d}"
            relation = {
                "evidence_relation_id": relation_id,
                "contract_id": contract_id,
                "evidence_index": evidence_index,
                "evidence_kind": evidence["kind"],
                "evidence": deepcopy(evidence),
                "claim_id": target_claim["claim_id"],
                "source_occurrence_id": source_occurrence_id,
                "role": role,
            }
            contract_evidence_relations.append(relation)
            target_claim["_evidence_relation_ids"].append(relation_id)
            if contract_id not in target_claim["_applicable_contract_ids"]:
                target_claim["_applicable_contract_ids"].append(contract_id)

    variant_groups: defaultdict[tuple[str, tuple[str, ...]], list[str]] = defaultdict(list)
    for claim in draft_claims:
        if claim["claim_kind"] == "EQUATION_GROUP" and claim["labels"]:
            variant_groups[(claim["family"], tuple(claim["labels"]))].append(claim["claim_id"])

    relations_by_contract: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in contract_evidence_relations:
        relations_by_contract[relation["contract_id"]].append(relation)

    claims: list[dict[str, Any]] = []
    for draft in draft_claims:
        applicable_contract_ids = draft.pop("_applicable_contract_ids")
        evidence_relation_ids = draft.pop("_evidence_relation_ids")
        applicable_contracts = [contracts[contract_id] for contract_id in applicable_contract_ids]
        topics = ordered_unique([contract["topic"] for contract in applicable_contracts])
        derivation, literature, code, data = common_evidence_blocks(
            topics, applicable_contracts
        )
        resolution = resolve_contract_dispositions(applicable_contract_ids, contracts)
        disposition = resolution["final_disposition"]
        disposition_basis = (
            f"{resolution['rationale']} This internal resolution does not upgrade literature "
            "or material authority."
        )
        applicable_contract_evidence = []
        for contract in applicable_contracts:
            contract_id = contract["id"]
            contract_relations = relations_by_contract[contract_id]
            direct_relations = [
                relation
                for relation in contract_relations
                if relation["claim_id"] == draft["claim_id"]
            ]
            applicable_contract_evidence.append(
                {
                    "contract_id": contract_id,
                    "topic": contract["topic"],
                    "source_disposition": contract["disposition"],
                    "closure_state": contract["closure_state"],
                    "assumptions": deepcopy(contract["assumptions"]),
                    "required_action": contract["required_action"],
                    "direct_claim_relation_ids": [
                        relation["evidence_relation_id"] for relation in direct_relations
                    ],
                    "direct_equation_relation_ids": [
                        relation["evidence_relation_id"]
                        for relation in direct_relations
                        if relation["evidence_kind"] == "equation_or_label"
                    ],
                    "all_contract_evidence_relation_ids": [
                        relation["evidence_relation_id"] for relation in contract_relations
                    ],
                    "all_contract_evidence": deepcopy(contract["evidence"]),
                }
            )
        if draft["claim_kind"] == "EQUATION_GROUP":
            if draft["labels"]:
                variants = variant_groups[(draft["family"], tuple(draft["labels"]))]
            else:
                # Empty labels carry no grounded cross-equation identity. Exact
                # copy-forward remains within the normalized-equation group, but
                # distinct unlabeled formulas are never inferred to be variants.
                variants = [draft["claim_id"]]
            count = len(draft["mapped_occurrence_ids"])
            if count > 1 and len(variants) > 1:
                lineage_status = "EXACT_COPY_FORWARD_WITH_VERSION_SPECIFIC_VARIANTS"
            elif count > 1:
                lineage_status = "EXACT_COPY_FORWARD"
            elif len(variants) > 1:
                lineage_status = "VERSION_SPECIFIC_VARIANT"
            else:
                lineage_status = "SINGLE_OCCURRENCE"
            lineage = {
                "status": lineage_status,
                "versions": [row["version"] for row in draft["occurrences"]],
                "copy_forward_exact": count > 1,
                "version_specific_variant_claim_ids": variants,
                "lineage_evidence_path": "Codex/results/PHASE_059_THEORY_LINEAGE_DIFF.json",
            }
        else:
            lineage = {
                "status": "CONTRACT_ONLY_SOURCE_CLAIM",
                "versions": [],
                "copy_forward_exact": False,
                "version_specific_variant_claim_ids": [],
                "lineage_evidence_path": "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json",
            }
        claims.append(
            {
                "claim_id": draft["claim_id"],
                "claim_kind": draft["claim_kind"],
                "grouping_key": draft["grouping_key"],
                "family": draft["family"],
                "labels": draft["labels"],
                "normalized_sha256": draft["normalized_sha256"],
                "disposition": disposition,
                "disposition_basis": disposition_basis,
                "mapped_occurrence_ids": draft["mapped_occurrence_ids"],
                "mapped_contract_ids": draft["mapped_contract_ids"],
                "evidence_contract_ids": applicable_contract_ids,
                "evidence_relation_ids": evidence_relation_ids,
                "applicable_contract_evidence": applicable_contract_evidence,
                "disposition_resolution": resolution,
                "occurrences": draft["occurrences"],
                "source_anchors": draft["source_anchors"],
                "lineage": lineage,
                "derivation_audit": derivation,
                "literature_status": literature,
                "code_impact": code,
                "data_authority": data,
                "authority_boundary": (
                    "This disposition is an internal frozen-corpus theory audit. It does "
                    "not establish primary-literature truth, production conformance, "
                    "parameter identifiability, or external material validity."
                ),
            }
        )

    routes: list[dict[str, Any]] = []
    for contract_id, contract in contracts.items():
        claim = contract_to_claim[contract_id]
        label = CONTRACT_PRIMARY_LABEL[contract_id]
        routes.append(
            {
                "contract_id": contract_id,
                "claim_id": claim["claim_id"],
                "source_contract_disposition": contract["disposition"],
                "primary_anchor": find_primary_anchor(contract, label),
                "route_basis": (
                    f"Contract {contract_id} is routed exactly once to "
                    + (
                        f"the exact equation group carrying primary label {label}; all "
                        "additional equation and prose evidence remains explicit in "
                        "contract_evidence_relations."
                        if label
                        else "a contract-only claim because its source claim has no single "
                        "displayed-equation anchor in the frozen 973-occurrence index."
                    )
                ),
            }
        )
    return claims, routes, contract_evidence_relations


def build_document() -> dict[str, Any]:
    source_index = json_blob(EXPECTED_INPUT_PATHS[0])
    contract_matrix = json_blob(EXPECTED_INPUT_PATHS[1])
    input_coverage, input_lines, input_corpus_sha = build_input_coverage()
    claims, routes, contract_evidence_relations = build_claims(source_index, contract_matrix)
    occurrence_ids = [row["equation_id"] for row in source_index["equations"]]
    contract_ids = [row["id"] for row in contract_matrix["records"]]
    disposition_counts = Counter(claim["disposition"] for claim in claims)
    complete_claim_disposition_counts = {
        disposition: disposition_counts[disposition]
        for disposition in sorted(ALLOWED_DISPOSITIONS)
    }
    equation_claims = sum(claim["claim_kind"] == "EQUATION_GROUP" for claim in claims)
    contract_only_claims = sum(claim["claim_kind"] == "CONTRACT_ONLY" for claim in claims)
    unmapped_equation_claims = sum(
        claim["claim_kind"] == "EQUATION_GROUP" and not claim["evidence_contract_ids"]
        for claim in claims
    )
    contract_disposition_counts = Counter(
        contract["disposition"] for contract in contract_matrix["records"]
    )
    complete_contract_disposition_counts = {
        disposition: contract_disposition_counts[disposition]
        for disposition in sorted(ALLOWED_DISPOSITIONS)
    }
    evidence_kind_counts = Counter(
        relation["evidence_kind"] for relation in contract_evidence_relations
    )
    evidence_role_counts = Counter(
        relation["role"] for relation in contract_evidence_relations
    )
    multi_contract_claims = [
        claim for claim in claims if len(claim["evidence_contract_ids"]) > 1
    ]
    document: dict[str, Any] = {
        "schema_version": 1,
        "generated_date": "2026-08-25",
        "baseline_commit": BASELINE_COMMIT,
        "phase": 59,
        "step": "39.1",
        "scope": (
            "Deterministic unique-claim disposition for all 973 Phase 059 displayed-"
            "equation occurrences and all 38 source-linked theory contracts."
        ),
        "status": "PASS_P059_STEP_039_1_THEORY_CLAIM_DISPOSITION",
        "authority_boundary": (
            "Internal source/derivation/lineage adjudication only. External literature "
            "truth, theory-code-test conformance, data provenance, parameter authority, "
            "and material validation remain unverified or deferred."
        ),
        "rules_and_definitions": {
            "allowed_dispositions": sorted(ALLOWED_DISPOSITIONS),
            "grouping_key_definition": (
                "Displayed-equation claims group only occurrences with identical family, "
                "ordered label list, and normalized equation SHA-256. This separates the "
                "973 occurrence ledger from 180 exact equation groups; changed normalized "
                "content remains a distinct version-specific claim even when a label is "
                "reused. Five prose-only source contracts become explicit CONTRACT_ONLY "
                "claims rather than being blanket-mapped to nearby equations."
            ),
            "contract_routing_rule": (
                "Each of the 38 contracts has exactly one primary/governing disposition "
                "route. This ownership route is separate from the complete evidence-relation "
                "ledger and never suppresses a secondary applicable equation relation."
            ),
            "contract_evidence_relation_rule": (
                "All 80 frozen contract evidence records remain exact ordered relations: "
                "51 equation_or_label records link to their exact v1.0.18.2 equation claim "
                "and 29 prose_regex records link to the governing claim as contract context. "
                "Each relation has one role and reverse claim membership."
            ),
            "multi_contract_resolution_rule": (
                "A claim disposition uses every directly applicable equation contract. Equal "
                "dispositions record agreement; mixed dispositions require an explicit bounded "
                "resolution retaining every source disposition, assumption, and required action."
            ),
            "unlabeled_lineage_rule": (
                "An empty label list supplies no cross-equation lineage identity. Exact "
                "copy-forward is retained inside the family+empty-label+normalized-hash "
                "equation group, while version_specific_variant_claim_ids remains self-only; "
                "line-number proximity or simultaneous presence never creates a variant link."
            ),
            "unverified_rule": (
                "An exact equation group without a direct equation_or_label evidence relation "
                "receives UNVERIFIED. No stronger derivation, literature, code, or material "
                "verdict is inferred from source presence, copying, internal tests, or self-report."
            ),
            "literature_rule": (
                "Step 39.1 performs no external full-text truth audit; literature status "
                "therefore remains UNVERIFIED_NO_PRIMARY_SOURCE_TRUTH_AUDIT."
            ),
        },
        "input_coverage": input_coverage,
        "input_corpus_sha256": input_corpus_sha,
        "occurrence_universe_sha256": hashlib.sha256(
            "\n".join(occurrence_ids).encode("utf-8")
        ).hexdigest(),
        "contract_universe_sha256": hashlib.sha256(
            "\n".join(contract_ids).encode("utf-8")
        ).hexdigest(),
        "counts": {
            "input_files": len(EXPECTED_INPUT_PATHS),
            "input_lines": input_lines,
            "source_occurrences": len(occurrence_ids),
            "source_occurrences_assigned": sum(
                len(claim["mapped_occurrence_ids"]) for claim in claims
            ),
            "unique_claims": len(claims),
            "equation_group_claims": equation_claims,
            "contract_only_claims": contract_only_claims,
            "theory_contracts": len(contract_ids),
            "theory_contracts_routed": sum(
                len(claim["mapped_contract_ids"]) for claim in claims
            ),
            "unassigned_occurrences": 0,
            "orphan_contracts": 0,
            "invalid_anchors": 0,
            "disposition_conflicts": 0,
            "unresolved_disposition_conflicts": 0,
            "multi_contract_reconciliation_count": len(multi_contract_claims),
            "contract_evidence_records": len(contract_evidence_relations),
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
            "unmapped_equation_claims": unmapped_equation_claims,
            "secondary_evidence_affected_claims": len(
                {
                    relation["claim_id"]
                    for relation in contract_evidence_relations
                    if relation["role"] == "SECONDARY_APPLICABLE_EQUATION"
                }
            ),
            "claim_disposition_counts": complete_claim_disposition_counts,
            "contract_disposition_counts": complete_contract_disposition_counts,
            "disposition_counts": complete_claim_disposition_counts,
        },
        "claims": claims,
        "contract_evidence_relations": contract_evidence_relations,
        "contract_routes": routes,
        "representative_dispositions": [
            {
                "contract_id": contract_id,
                "claim_id": next(
                    route["claim_id"] for route in routes if route["contract_id"] == contract_id
                ),
                "why": why,
            }
            for contract_id, why in (
                (
                    "P059-CON-006",
                    "PRESERVE only within the symmetric regular-solution assumptions; fitted Omega is not promoted to a universal material constant.",
                ),
                (
                    "P059-CON-003",
                    "CORRECT because the C-rate/capacity path retains a 3600 unit ambiguity.",
                ),
                (
                    "P059-CON-020",
                    "REJECT because a local affinity was frozen into one transition-level cutoff value.",
                ),
                (
                    "P059-CON-010",
                    "THEORY_ONLY because equilibrium convexification does not close a finite-width production observation kernel.",
                ),
                (
                    "P059-CON-035",
                    "EMPIRICAL_ONLY because the smooth LCO DOS gate lacks primary-data and phase-coexistence authority.",
                ),
                (
                    "P059-CON-024",
                    "UNVERIFIED because width, reaction, vibrational, and electronic temperature mechanisms are not jointly identifiable under current evidence.",
                ),
            )
        ]
        + [
            {
                "contract_id": "P059-CON-009",
                "claim_id": "P059-TCL-011",
                "why": (
                    "PRESERVE because the secondary eq:app-ch-R relation is directly "
                    "applicable and can no longer be discarded by the primary-route table."
                ),
            },
            {
                "contract_id": "P059-CON-015 + P059-CON-026",
                "claim_id": "P059-TCL-165",
                "why": (
                    "CORRECT overall while preserving the bounded ideal configurational-"
                    "entropy identity; the derivative decomposition still requires correction."
                ),
            },
        ],
        "unresolved": [
            f"{unmapped_equation_claims} equation groups have no direct equation_or_label contract evidence and remain UNVERIFIED.",
            "All primary-literature exact-claim support remains pending Phase 071 truth audit.",
            "Theory-code-test-artifact alignment is deferred to Step 39.3.",
            "No public experimental dataset or target-material parameter authority is established.",
            "Existing coordinate, phase-separation, kinetics, width, heat, LCO, and identifiability blockers remain open as recorded in the detailed audits.",
        ],
        "determinism": {
            "serialization": "UTF-8, LF, sorted keys, indent=2",
            "semantic_sha256": "",
        },
    }
    document["determinism"]["semantic_sha256"] = canonical_semantic_sha256(document)
    return document


def main() -> int:
    document = build_document()
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ARTIFACT_PATH.write_text(text, encoding="utf-8", newline="\n")
    artifact_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(
        "PASS_P059_STEP_039_1_THEORY_CLAIM_BUILD "
        f"occurrences={document['counts']['source_occurrences']} "
        f"claims={document['counts']['unique_claims']} "
        f"contracts={document['counts']['theory_contracts']} "
        f"artifact_sha256={artifact_sha}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
