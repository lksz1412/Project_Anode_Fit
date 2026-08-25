#!/usr/bin/env python3
"""Validate the frozen Phase 058 -> Phase 059 blocker-delta artifact."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "4ee5927ef8fb68bbb488b7debc1709c6f5fad8b0"
ARTIFACT = ROOT / "Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json"
EXPECTED_SEMANTIC_SHA256 = "0ed630ccb1ab148e2ee72bc155c6b6100147eab9d57b9727f6e20bbf8355a1f4"

INPUT_PATHS = [
    "Codex/results/PHASE_058_CARRY_FORWARD_BLOCKER_REGISTER.json",
    "Codex/results/PHASE_058_CARRY_FORWARD_BLOCKER_REVIEW.md",
    "Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_MATRIX.json",
    "Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_REVIEW.md",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_REVIEW.md",
    "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json",
    "Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md",
    "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_DIFF.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md",
    "Codex/results/PHASE_059_ISOLATED_RUNTIME_RESULTS.json",
    "Codex/results/PHASE_059_ISOLATED_RUNTIME_REVIEW.md",
    "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json",
    "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md",
    "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json",
    "Codex/results/PHASE_059_GOLDEN_NPZ_REVIEW.md",
    "Codex/results/PHASE_059_ARTIFACT_GENEALOGY.json",
    "Codex/results/PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md",
    "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json",
    "Codex/results/PHASE_059_ARTIFACT_RENDER_AUDIT.md",
    "Codex/results/PHASE_059_IMAGE_AUDIT.json",
    "Codex/results/PHASE_059_STANDALONE_IMAGE_REVIEW.md",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION_RESULT.md",
]

CATEGORY_FIELDS = [
    ("carry_forward_assets", "carry_forward_asset", 11),
    ("repair_blockers", "repair_blocker", 13),
    ("new_scope_blockers", "new_scope_blocker", 5),
    ("evidence_debts", "evidence_debt", 5),
]

ALLOWED_STATUSES = ["RESOLVED", "PARTIAL", "UNCHANGED", "REGRESSED", "NEW_EVIDENCE"]
EXPECTED_STATUS = {
    "CF-01": "NEW_EVIDENCE", "CF-02": "NEW_EVIDENCE", "CF-03": "NEW_EVIDENCE",
    "CF-04": "NEW_EVIDENCE", "CF-05": "NEW_EVIDENCE", "CF-06": "NEW_EVIDENCE",
    "CF-07": "NEW_EVIDENCE", "CF-08": "NEW_EVIDENCE", "CF-09": "NEW_EVIDENCE",
    "CF-10": "NEW_EVIDENCE", "CF-11": "NEW_EVIDENCE",
    "RB-01": "UNCHANGED", "RB-02": "PARTIAL", "RB-03": "UNCHANGED",
    "RB-04": "UNCHANGED", "RB-05": "UNCHANGED", "RB-06": "UNCHANGED",
    "RB-07": "PARTIAL", "RB-08": "UNCHANGED", "RB-09": "UNCHANGED",
    "RB-10": "UNCHANGED", "RB-11": "REGRESSED", "RB-12": "PARTIAL",
    "RB-13": "PARTIAL",
    "NS-01": "UNCHANGED", "NS-02": "UNCHANGED", "NS-03": "UNCHANGED",
    "NS-04": "UNCHANGED", "NS-05": "NEW_EVIDENCE",
    "ED-01": "UNCHANGED", "ED-02": "UNCHANGED", "ED-03": "NEW_EVIDENCE",
    "ED-04": "UNCHANGED", "ED-05": "NEW_EVIDENCE",
}

RB10_UNCHANGED_BASIS = (
    "Phase 059 adds no instrument-resolution, sampling, smoothing, differentiation, "
    "baseline, or noise forward operator mapping latent state to measured dQ/dV; the "
    "Phase 058 F4-08 conceptual ensemble integral remains code/test/artifact absent and "
    "is not acceptance progress."
)

RB04_UNCHANGED_BASIS = (
    "Phase 059 audits the required role split but does not demonstrate production use of "
    "distinct symbols and distinct tests for electron stoichiometry, site count, degeneracy, "
    "interaction, heterogeneity, kinetics, and observation widths; WID-004 confirms that the "
    "implicit default width and entropy derivative still disagree, so no acceptance element is satisfied."
)
RB09_UNCHANGED_BASIS = (
    "Phase 059 preserves bounded theory identities, but P059-CODE-010 and LCO-001 show that "
    "production freezes the LCO electronic term at 298.15 K instead of applying the temperature-dependent "
    "law, and no external data validate composition mapping, temperature curvature, phase assignments, "
    "or defaults; no acceptance element is satisfied."
)
RB11_REGRESSED_BASIS = (
    "Relative to the Phase 058 gate surface, v1.0.18.2 exposes an Einstein helper path that remains "
    "dormant in shipped defaults, while the complete copied harness contains no n_T1 or theta_E token "
    "and omits critical branch gates; strict bit equality also fails on the audited runtime."
)
NS02_IMAGE_ONLY_BASIS = (
    "IMG-059-05 shows that no audited image contains Si, graphite-Si, or experimental observations; "
    "this image-only evidence satisfies none of the old source-backed material-model, conservation, "
    "code, test, or external-data acceptance elements."
)

EXPECTED_EVIDENCE = {
    "CF-01": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-176")],
    "CF-02": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-061")],
    "CF-03": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-039")],
    "CF-04": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "ORD-001")],
    "CF-05": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "MEM-001"), ("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "MEM-003")],
    "CF-06": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-179")],
    "CF-07": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-033")],
    "CF-08": [("json", "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json", "GOLD-006")],
    "CF-09": [("json", "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json", "P059-CLM-028")],
    "CF-10": [("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-001")],
    "CF-11": [("lines", "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md", 153, 171)],
    "RB-01": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "UNT-001")],
    "RB-02": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-002"), ("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-009")],
    "RB-03": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-002")],
    "RB-04": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-153"), ("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "WID-004")],
    "RB-05": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "KIN-001")],
    "RB-06": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "CUR-002")],
    "RB-07": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "MEM-003")],
    "RB-08": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "ORD-002"), ("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-003")],
    "RB-09": [("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-010"), ("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "LCO-001")],
    "RB-10": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-007")],
    "RB-11": [("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-011"), ("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-013"), ("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-012"), ("json", "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json", "GOLD-003")],
    "RB-12": [("json", "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json", "PDF-059-01"), ("json", "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json", "PDF-059-02"), ("json", "Codex/results/PHASE_059_IMAGE_AUDIT.json", "IMG-059-03")],
    "RB-13": [("json", "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json", "P059-CLM-028")],
    "NS-01": [("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-013")],
    "NS-02": [("json", "Codex/results/PHASE_059_IMAGE_AUDIT.json", "IMG-059-05")],
    "NS-03": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "LCO-003")],
    "NS-04": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-012")],
    "NS-05": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-011")],
    "ED-01": [("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-013")],
    "ED-02": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "LCO-003")],
    "ED-03": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-011")],
    "ED-04": [("lines", "Codex/results/PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md", 20, 33)],
    "ED-05": [("json", "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json", "GOLD-003")],
}

EXPECTED_NEW = {
    "P059-BD-NEW-001": ("repair_blocker", "einstein_input_semantics_and_positive_reference_guard", [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "VIB-003"), ("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-001")]),
    "P059-BD-NEW-002": ("evidence_debt", "einstein_reaction_spectrum_amplitude_and_material_identifiability", [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "VIB-004"), ("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-001")]),
    "P059-BD-NEW-003": ("evidence_debt", "uncontracted_displayed_equation_claim_adjudication", [("lines", "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md", 167, 185)]),
    "P059-BD-NEW-004": ("new_scope_blocker", "composition_dependent_interaction_or_sublattice_law", [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-002")]),
    "P059-BD-NEW-005": ("new_scope_blocker", "signed_charge_transfer_and_transport_solver", [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-004")]),
    "P059-BD-NEW-006": ("new_scope_blocker", "quantitative_particle_size_psd_forward_model", [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-005")]),
}


class ValidationFailure(RuntimeError):
    """Raised when the blocker-delta contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def git_blob(path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)
    except subprocess.CalledProcessError as exc:
        raise ValidationFailure(f"missing frozen input Git blob: {path}") from exc


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def recursive_node_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(recursive_node_count(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(recursive_node_count(item) for item in value)
    return 1


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk_dicts(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_dicts(item)


def find_record(document: Any, record_id: str) -> tuple[str, dict[str, Any]]:
    id_keys = ("id", "claim_id", "item_id", "probe_id", "finding_id", "record_id", "contract_id")
    matches = []
    for obj in walk_dicts(document):
        for key in id_keys:
            if obj.get(key) == record_id:
                matches.append((key, obj))
                break
    if len(matches) > 1:
        largest = max(recursive_node_count(record) for _, record in matches)
        matches = [(key, record) for key, record in matches if recursive_node_count(record) == largest]
    require(len(matches) == 1, f"{record_id}: expected one substantive JSON record, found {len(matches)}")
    return matches[0]


def expected_coverage(blob_map: dict[str, bytes], parsed: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_PATHS:
        blob = blob_map[path]
        line_count = len(blob.splitlines())
        row = {
            "path": path,
            "byte_count": len(blob),
            "line_count": line_count,
            "read_range": f"1-{line_count}",
            "sha256": hashlib.sha256(blob).hexdigest(),
            "hash_basis": f"Git blob bytes at baseline {BASELINE}",
            "parse_mode": "recursive_json_all_nodes" if path.endswith(".json") else "full_text_1_to_EOF",
        }
        if path.endswith(".json"):
            row["recursive_node_count"] = recursive_node_count(parsed[path])
        rows.append(row)
    return rows


def validate_evidence(evidence: Any, expected_specs: list[tuple[Any, ...]], blob_map: dict[str, bytes], parsed: dict[str, Any], owner: str) -> None:
    require(isinstance(evidence, list) and evidence, f"{owner} missing Phase 059 evidence")
    require(len(evidence) == len(expected_specs), f"{owner} evidence count/mapping mismatch")
    for actual, spec in zip(evidence, expected_specs):
        require(isinstance(actual, dict), f"{owner} evidence row must be object")
        path = actual.get("path")
        require(path == spec[1] and path in INPUT_PATHS, f"{owner} invalid evidence path")
        require("\\" not in path and PurePosixPath(path).as_posix() == path, f"{owner} evidence path is not POSIX")
        require(bool(actual.get("authority_use")), f"{owner} missing evidence authority boundary")
        if spec[0] == "json":
            require(actual.get("anchor_kind") == "json_record", f"{owner} falsified evidence role")
            require(actual.get("record_id") == spec[2], f"{owner} JSON evidence ID mismatch")
            key, record = find_record(parsed[path], spec[2])
            require(actual.get("record_id_key") == key, f"{owner} JSON evidence ID-key mismatch")
            require(actual.get("record_sha256") == hashlib.sha256(canonical_bytes(record)).hexdigest(), f"{owner} JSON record hash mismatch")
            observed = {
                field: copy.deepcopy(record[field])
                for field in ("title", "topic", "category", "verdict", "disposition", "primary_classification", "claim", "interpretation", "acceptance", "authority_boundary")
                if field in record
            }
            require(actual.get("observed_fields") == observed, f"{owner} JSON evidence stored fields mismatch")
        elif spec[0] == "lines":
            require(actual.get("anchor_kind") == "line_range", f"{owner} falsified line evidence role")
            require(actual.get("line_start") == spec[2] and actual.get("line_end") == spec[3], f"{owner} line anchor mismatch")
            lines = blob_map[path].decode("utf-8").splitlines()
            require(1 <= spec[2] <= spec[3] <= len(lines), f"{owner} invalid source line")
            excerpt = "\n".join(lines[spec[2] - 1 : spec[3]])
            require(actual.get("source_excerpt") == excerpt, f"{owner} stored source text mismatch")
            require(actual.get("excerpt_sha256") == hashlib.sha256(excerpt.encode("utf-8")).hexdigest(), f"{owner} excerpt hash mismatch")
        else:
            raise ValidationFailure(f"{owner} unknown expected evidence kind")


def validate() -> None:
    require(ARTIFACT.is_file(), "missing artifact: Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json")
    try:
        document = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationFailure(f"artifact JSON parse failed: {exc}") from exc

    require(document.get("schema_version") == 1, "schema_version mismatch")
    require(document.get("phase") == 59 and document.get("step") == "39.2", "phase/step mismatch")
    require(document.get("status") == "PASS_P059_STEP_039_2_BLOCKER_DELTA", "status mismatch")
    require(document.get("baseline_commit") == BASELINE, "baseline_commit mismatch")
    require(bool(document.get("authority_boundary")), "missing global authority boundary")
    rules = document.get("rules_and_definitions", {})
    require(rules.get("allowed_delta_statuses") == ALLOWED_STATUSES, "allowed delta status contract mismatch")
    require(set(rules.get("delta_status_semantics", {})) == set(ALLOWED_STATUSES), "delta status semantics mismatch")
    require("self-report" in rules.get("resolved_rule", "") and "actual source/code/test/data" in rules.get("resolved_rule", ""), "RESOLVED semantics are not sharp")
    require("without implying closure" in rules.get("new_evidence_rule", ""), "NEW_EVIDENCE semantics are not sharp")

    blob_map = {path: git_blob(path) for path in INPUT_PATHS}
    parsed = {path: json.loads(blob_map[path].decode("utf-8")) for path in INPUT_PATHS if path.endswith(".json")}
    coverage = expected_coverage(blob_map, parsed)
    require(document.get("input_coverage") == coverage, "input coverage ordered path/hash/line/parse contract mismatch")
    require(document.get("input_corpus_sha256") == hashlib.sha256(canonical_bytes(coverage)).hexdigest(), "frozen input corpus SHA-256 mismatch")

    register = parsed[INPUT_PATHS[0]]
    four_axis = parsed[INPUT_PATHS[2]]
    preservation = document.get("source_register_preservation", {})
    require(preservation.get("path") == INPUT_PATHS[0], "source register path mismatch")
    require(preservation.get("snapshot") == register, "source register snapshot is lossy or tampered")
    require(preservation.get("snapshot_sha256") == hashlib.sha256(canonical_bytes(register)).hexdigest(), "source register snapshot hash mismatch")

    expected_rows = []
    expected_category_counts = {}
    for source_field, category, expected_count in CATEGORY_FIELDS:
        source_items = register.get(source_field)
        require(isinstance(source_items, list) and len(source_items) == expected_count, f"Phase 058 {source_field} count mismatch")
        expected_category_counts[category] = expected_count
        for index, original in enumerate(source_items):
            expected_rows.append((source_field, category, index, original))
    require(len(expected_rows) == 34, "Phase 058 old total is not 34")
    expected_ids = [row[3]["id"] for row in expected_rows]
    require(len(set(expected_ids)) == 34, "Phase 058 old IDs are not unique")
    require(set(EXPECTED_STATUS) == set(expected_ids), "expected old status universe mismatch")

    old_deltas = document.get("old_deltas")
    require(isinstance(old_deltas, list) and len(old_deltas) == 34, "old routed total must be exactly 34")
    actual_ids = [item.get("old_id") for item in old_deltas]
    require(actual_ids == expected_ids, "old item dropped, duplicated, orphaned, or reordered")
    require(len(set(actual_ids)) == 34, "duplicate old item assignment")
    f4_rows = {row["id"]: row for row in four_axis["rows"]}

    for actual, (source_field, category, index, original) in zip(old_deltas, expected_rows):
        old_id = original["id"]
        require(actual.get("old_category") == category, f"{old_id} category mismatch")
        require(actual.get("source_register_field") == source_field and actual.get("source_register_index") == index, f"{old_id} register anchor mismatch")
        require(actual.get("original_item") == original, f"{old_id} original fields/evidence were not preserved")
        require(actual.get("original_item_sha256") == hashlib.sha256(canonical_bytes(original)).hexdigest(), f"{old_id} original record hash mismatch")
        require(actual.get("original_acceptance_present") == ("acceptance" in original), f"{old_id} original acceptance-presence mismatch")
        require(actual.get("original_acceptance_criterion") == original.get("acceptance"), f"{old_id} original acceptance mismatch")
        effective = actual.get("effective_acceptance_criterion")
        require(isinstance(effective, str) and effective.strip(), f"{old_id} missing effective acceptance criterion")
        if "acceptance" in original:
            require(effective == original["acceptance"], f"{old_id} repair acceptance changed")

        expected_routes = []
        for route_index, route in enumerate(register["four_axis_routes"]):
            if route["route"] == old_id:
                row = f4_rows[route["row"]]
                expected_routes.append({"register_route_index": route_index, "route": route, "phase058_four_axis_record": row, "phase058_four_axis_record_sha256": hashlib.sha256(canonical_bytes(row)).hexdigest()})
        require(actual.get("source_four_axis_routes") == expected_routes, f"{old_id} Phase 058 route evidence mismatch")

        status = actual.get("delta_status")
        require(status in ALLOWED_STATUSES, f"{old_id} illegal or blank delta status")
        require(status == EXPECTED_STATUS[old_id], f"{old_id} unsupported delta disposition")
        require(bool(actual.get("delta_basis")), f"{old_id} missing delta basis")
        require(bool(actual.get("authority_boundary")), f"{old_id} missing authority boundary")
        validate_evidence(actual.get("phase059_evidence"), EXPECTED_EVIDENCE[old_id], blob_map, parsed, old_id)

        audit = actual.get("acceptance_criterion_audit")
        require(isinstance(audit, dict), f"{old_id} missing acceptance-criterion audit")
        require(audit.get("criterion") == effective, f"{old_id} acceptance audit criterion mismatch")
        require(isinstance(audit.get("satisfied_elements"), list), f"{old_id} satisfied-elements type mismatch")
        require(isinstance(audit.get("unsatisfied_elements"), list) and audit["unsatisfied_elements"], f"{old_id} unresolved acceptance elements missing")
        require(bool(audit.get("conclusion")) and bool(audit.get("resolution_authority_check")), f"{old_id} acceptance audit conclusion/boundary missing")
        if status == "RESOLVED":
            require(not audit["unsatisfied_elements"] and audit["conclusion"] == "SATISFIED", f"{old_id} unsupported RESOLVED")
        else:
            require(audit["conclusion"] != "SATISFIED", f"{old_id} non-resolved item claims satisfied acceptance")
        required_unchanged_basis = {
            "RB-04": RB04_UNCHANGED_BASIS,
            "RB-09": RB09_UNCHANGED_BASIS,
            "NS-02": NS02_IMAGE_ONLY_BASIS,
        }
        if old_id in required_unchanged_basis:
            required_basis = required_unchanged_basis[old_id]
            require(status == "UNCHANGED", f"{old_id} acceptance requires UNCHANGED")
            require(actual.get("delta_basis") == required_basis, f"{old_id} acceptance-bounded basis mismatch")
            require(audit.get("satisfied_elements") == [], f"{old_id} outside-acceptance progress is prohibited")
            require(audit.get("unsatisfied_elements") == [required_basis], f"{old_id} exact acceptance gaps mismatch")
            require(audit.get("conclusion") == "NOT_SATISFIED_UNCHANGED", f"{old_id} acceptance conclusion mismatch")
        if old_id == "RB-10":
            require(status == "UNCHANGED", "RB-10 observation-operator acceptance requires UNCHANGED")
            require(actual.get("delta_basis") == RB10_UNCHANGED_BASIS, "RB-10 acceptance-bounded basis mismatch")
            require(audit.get("satisfied_elements") == [], "RB-10 outside-acceptance width-role progress is prohibited")
            require(audit.get("unsatisfied_elements") == [RB10_UNCHANGED_BASIS], "RB-10 observation-operator gap mismatch")
            require(audit.get("conclusion") == "NOT_SATISFIED_UNCHANGED", "RB-10 acceptance conclusion mismatch")
            route_rows = [route["phase058_four_axis_record"] for route in expected_routes]
            require(
                route_rows == [{
                    "id": "F4-08",
                    "topic": "ensemble_heterogeneity_forward_integral",
                    "theory": "PRESENT_CONDITIONAL",
                    "code": "ABSENT",
                    "test": "ABSENT",
                    "artifact": "ABSENT",
                    "overall": "ABSENT",
                    "carry_decision": "THEORY_ONLY",
                    "pass_does_not_mean": "A conceptual integral is not an observation layer.",
                }],
                "RB-10 Phase 058 observation-layer boundary mismatch",
            )
        if old_id == "RB-11":
            require(actual.get("delta_basis") == RB11_REGRESSED_BASIS, "RB-11 comparative regression basis mismatch")
            require(
                [item.get("record_id") for item in actual.get("phase059_evidence", [])]
                == ["P059-TD-011", "P059-CODE-013", "P059-TD-012", "GOLD-003"],
                "RB-11 exact comparative evidence package mismatch",
            )

    status_counts = Counter(item["delta_status"] for item in old_deltas)
    require(status_counts == Counter(EXPECTED_STATUS.values()), "old delta status count reconciliation mismatch")

    new_blockers = document.get("new_blockers")
    require(isinstance(new_blockers, list) and len(new_blockers) == len(EXPECTED_NEW), "new blocker count mismatch")
    new_ids = [item.get("blocker_id") for item in new_blockers]
    require(new_ids == list(EXPECTED_NEW), "new blocker IDs dropped, duplicated, or reordered")
    require(len(set(new_ids)) == len(new_ids), "duplicate new blocker ID")
    require(not set(new_ids) & set(expected_ids), "new blocker ID collides with old ID")
    for item in new_blockers:
        blocker_id = item["blocker_id"]
        category, topic, evidence_specs = EXPECTED_NEW[blocker_id]
        require(item.get("category") == category and item.get("topic") == topic, f"{blocker_id} category/topic mismatch")
        require(item.get("source_phase") == 59, f"{blocker_id} source phase mismatch")
        require(isinstance(item.get("target_phase"), int) and 59 < item["target_phase"] <= 69, f"{blocker_id} invalid target phase")
        require(bool(item.get("acceptance_criterion")), f"{blocker_id} missing acceptance criterion")
        require(bool(item.get("blocking_authority")) and bool(item.get("authority_boundary")), f"{blocker_id} missing blocking/authority boundary")
        require(isinstance(item.get("overlap_old_ids"), list) and item["overlap_old_ids"], f"{blocker_id} missing old-overlap audit")
        require(set(item["overlap_old_ids"]) <= set(expected_ids), f"{blocker_id} invalid old-overlap reference")
        require(bool(item.get("deduplication_basis")), f"{blocker_id} missing deduplication basis")
        validate_evidence(item.get("phase059_evidence"), evidence_specs, blob_map, parsed, blocker_id)

    refinements = document.get("refinement_routes_not_double_counted")
    require(isinstance(refinements, list) and refinements, "missing refinement-to-old routing")
    for index, route in enumerate(refinements):
        require(bool(route.get("finding")) and bool(route.get("basis")), f"refinement route {index} missing finding/basis")
        require(isinstance(route.get("old_ids"), list) and route["old_ids"], f"refinement route {index} missing old IDs")
        require(set(route["old_ids"]) <= set(expected_ids), f"refinement route {index} invalid old ID")

    counts = document.get("counts", {})
    expected_counts = {
        "input_file_count": len(INPUT_PATHS),
        "input_line_count": sum(row["line_count"] for row in coverage),
        "old_category_counts": dict(sorted(expected_category_counts.items())),
        "old_total": 34,
        "old_routed": 34,
        "orphan_old": 0,
        "old_delta_status_counts": {status: status_counts.get(status, 0) for status in ALLOWED_STATUSES},
        "resolved_count": 0,
        "unsupported_resolved_count": 0,
        "new_blocker_count": len(EXPECTED_NEW),
        "new_blocker_category_counts": dict(sorted(Counter(item["category"] for item in new_blockers).items())),
        "new_id_collisions": 0,
        "invalid_evidence_paths_or_anchors": 0,
        "missing_acceptance_or_authority_boundary": 0,
        "illegal_delta_status": 0,
    }
    require(counts == expected_counts, "classification/count reconciliation mismatch")
    unresolved = document.get("unresolved", {})
    require(unresolved.get("old_items_not_resolved") == 34 and unresolved.get("new_blockers_open") == 6, "unresolved counts mismatch")
    require("UNVERIFIED" in unresolved.get("primary_literature_truth_audit", ""), "literature truth authority inflated")
    require("GROUND_NOT_FOUND" in unresolved.get("external_material_validation", ""), "external material authority inflated")

    determinism = document.get("determinism", {})
    stored_semantic = determinism.get("semantic_sha256")
    require(isinstance(stored_semantic, str) and len(stored_semantic) == 64, "semantic SHA-256 missing")
    candidate = copy.deepcopy(document)
    candidate["determinism"]["semantic_sha256"] = ""
    computed_semantic = hashlib.sha256(canonical_bytes(candidate)).hexdigest()
    require(stored_semantic == computed_semantic, "artifact semantic SHA-256 self-check mismatch")
    require(stored_semantic == EXPECTED_SEMANTIC_SHA256, "frozen canonical semantic SHA-256 lock mismatch")


def main() -> int:
    try:
        validate()
    except ValidationFailure as exc:
        print(f"FAIL_P059_STEP_039_2_BLOCKER_DELTA: {exc}", file=sys.stderr)
        return 1
    print("PASS_P059_STEP_039_2_BLOCKER_DELTA old=34 new=6 orphan=0 resolved=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
