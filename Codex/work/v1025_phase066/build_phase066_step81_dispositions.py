from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "ec02d8e0017c4441d9d02c08e22ad432b8c47bc5"
EXPECTED_SUBJECT = "audit(phase066): disposition v1025 lineage evidence"
DISPOSITION_PATH = "Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json"
CARRY_PATH = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"
ALLOWED_DISPOSITIONS = {"PRESERVE", "CORRECT", "WITHHOLD", "DISCARD", "GROUND_NOT_FOUND"}

INPUT_REVISIONS = {
    "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json": "58a5a32ed2f647d1749bb413c19039715983f668",
    "Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json": "26e2ce9559220d5782e1303d68b4449a36309e94",
    "Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json": "26e2ce9559220d5782e1303d68b4449a36309e94",
    "Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json": "38e00020906e3a024e493c214c1a99a6f8ab07d2",
    "Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json": "38e00020906e3a024e493c214c1a99a6f8ab07d2",
    "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json": "5d26e0746864cea7a8bd37a22874093b73c1a12f",
    "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json": "5d26e0746864cea7a8bd37a22874093b73c1a12f",
    "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json": "fedb2031fbfabeaba84f86427c35334526234d73",
    "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json": "d091e7881f9f22d5dfe9511427afdf4ef22e3280",
    "Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json": "ec02d8e0017c4441d9d02c08e22ad432b8c47bc5",
    "Codex/results/PHASE_066_RUNTIME_ATTESTATION.json": "ec02d8e0017c4441d9d02c08e22ad432b8c47bc5",
}

OWNERS = {
    66: "P066-STEP81-DISPOSITION",
    71: "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
    72: "PHASE-072-DATA-PROVENANCE",
    75: "PHASE-075-EQUILIBRIUM-PHASE",
    76: "PHASE-076-NONEQUILIBRIUM-KINETICS",
    77: "PHASE-077-GRAPHITE-CLOSURE",
    78: "PHASE-078-LCO-CLOSURE",
    79: "PHASE-079-SILICON-CLOSURE",
    80: "PHASE-080-BLEND-COUPLING-CLOSURE",
    81: "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION",
    82: "PHASE-082-CANONICAL-EQUATION-FREEZE",
    83: "PHASE-083-IMPLEMENTATION-CONTRACT",
    85: "PHASE-085-STRUCTURE-DEFAULT-CONTRACT",
    86: "PHASE-086-CALIBRATION-VALIDATION",
    87: "PHASE-087-CANONICAL-SOURCE-SYNTHESIS",
    88: "PHASE-088-SCIENTIFIC-REDTEAM",
    89: "PHASE-089-LATEX-PDF-RELEASE-QA",
    90: "PHASE-090-CLEAN-CLONE-RELEASE",
}

PHASE057_TARGETS = {
    71: set(),
    72: {293, 303, 312, 327, 328, 332, 347, 357},
    75: {306},
    76: {319},
    77: {296, 298, 310, 311, 317, 318, 336, 344, 358, 365, 367, 369, 381},
    81: {305, 308, 335, 337, 338, 351, 368},
    82: {294, 297, 316, 321, 339, 340, 370, 371, 379, 382},
    83: {301, 320, 346, 359, 366, 373, 374, 384},
    85: {364},
    86: {295, 304, 307, 309, 313, 377},
    87: {300, 315, 330, 331, 343, 348, 349, 350, 372, 375, 376, 380, 383},
    88: {322, 341, 342, 353, 356, 360, 385, 387},
    89: {299, 323, 324, 329, 333, 334, 361},
    90: {302, 314, 325, 326, 345, 352, 354, 355, 362, 363, 378, 386},
}

BOUNDED_PHASE057 = {302, 314, 325, 326, 335, 345, 352, 354, 355, 363, 378, 386}


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def run_git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout


def strict_load(raw: bytes) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in values:
            require(key not in out, f"duplicate-json-key:{key}")
            out[key] = value
        return out

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def record_sha(value: Any) -> str:
    return sha256(compact(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    value = dict(value)
    value.pop("semantic_sha256", None)
    value["semantic_sha256"] = sha256(compact(value))
    return value


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    values: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for path, revision in INPUT_REVISIONS.items():
        raw = run_git("show", f"{revision}:{path}")
        blob = run_git("rev-parse", f"{revision}:{path}").decode().strip()
        values[path] = strict_load(raw)
        metadata.append({
            "path": path,
            "commit": revision,
            "blob_sha1": blob,
            "bytes": len(raw),
            "raw_sha256": sha256(raw),
            "semantic_sha256": values[path].get("semantic_sha256"),
        })
    return values, metadata


def source_classification(occurrence: dict[str, Any], stale: set[str], defects: set[str]) -> tuple[str, int, str]:
    blob = occurrence["blob_sha1"]
    path = occurrence["path"]
    if blob in stale and occurrence["version"] == "v1.0.25.2":
        return "WITHHOLD", 89, "stale PDF is not release evidence until rebuilt from the corresponding changed TeX and visually verified"
    if blob in defects:
        return "CORRECT", 89, "recorded visual defect must be repaired and the regenerated artifact visually verified"
    if blob == "62b67e12724d8e1a8bbdd9f9432e4fcff864f0be":
        return "CORRECT", 83, "executable behavior is retained while contradictory header, docstring and profile comments are corrected under the implementation contract"
    if path.endswith("snapshot_v1024_R0.json"):
        return "WITHHOLD", 83, "the non-JSON snapshot label cannot be promoted to a canonical machine artifact"
    return "PRESERVE", 87, "retain the frozen occurrence as lineage evidence; later synthesis may quote only independently verified propositions"


def build_source(inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> dict[str, Any]:
    delta = inputs["Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json"]
    read = inputs["Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json"]
    manifest_meta = next(row for row in metadata if row["path"] == "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json")
    require(manifest_meta["raw_sha256"] == delta["inputs"]["manifest"]["raw_sha256"], "manifest-binding-drift")
    bindings = {(row["manifest_index"], row["path"]): row for row in read["occurrence_bindings"]}
    machine = {row["attestation_id"]: row for row in read["machine_blob_attestations"]}
    stale = {row["pdf_blob_sha1"] for row in delta["stale_pdf_pairs"]}
    defects = {row["blob_sha1"] for row in delta["observed_defects"]}
    rows: list[dict[str, Any]] = []
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, occurrence in enumerate(delta["occurrences"], 1):
        key = (occurrence["manifest_index"], occurrence["path"])
        require(key in bindings, f"orphan-occurrence:{key}")
        attestation = machine[occurrence["attestation_id"]]
        disposition, target, reason = source_classification(occurrence, stale, defects)
        row = {
            "disposition_id": f"P066-DISP-{index:04d}",
            "source_path": occurrence["path"],
            "manifest_index": occurrence["manifest_index"],
            "ordinal": occurrence["ordinal"],
            "version": occurrence["version"],
            "role": occurrence["role"],
            "blob_sha1": occurrence["blob_sha1"],
            "dedup_group": f"blob:{occurrence['blob_sha1']}",
            "disposition": disposition,
            "inventory_identity_disposition": "PRESERVE",
            "release_build_disposition": disposition,
            "state": "OPEN_CORRECTION" if disposition in {"CORRECT", "WITHHOLD", "GROUND_NOT_FOUND"} else "PRESERVED_LINEAGE",
            "canonical_owner": OWNERS[target],
            "target_phase": target,
            "acceptance_criterion": reason,
            "reason": reason,
            "external_authority_promoted": False,
            "read_attestation": {
                "attestation_id": occurrence["attestation_id"],
                "status": attestation["human_coverage"]["status"],
                "coverage": attestation["human_coverage"],
                "machine_status": attestation["machine_coverage"]["status"],
                "record_sha256": record_sha(bindings[key]),
            },
            "occurrence_record_sha256": record_sha(occurrence),
        }
        require(disposition in ALLOWED_DISPOSITIONS, f"bad-disposition:{disposition}")
        rows.append(row)
        groups[occurrence["blob_sha1"]].append(row)

    blob_rows: list[dict[str, Any]] = []
    for index, (blob, members) in enumerate(sorted(groups.items()), 1):
        values = sorted({member["disposition"] for member in members})
        blob_rows.append({
            "blob_group_id": f"P066-BLOB-DISP-{index:04d}",
            "blob_sha1": blob,
            "dedup_group": f"blob:{blob}",
            "occurrence_dispositions": values,
            "contextual_mixed_disposition": len(values) > 1,
            "occurrence_count": len(members),
            "manifest_indices": [member["manifest_index"] for member in members],
            "paths": [member["source_path"] for member in members],
            "row_record_sha256s": [record_sha(member) for member in members],
        })

    supplemental = []
    for index, row in enumerate(delta["narrative"]["supplemental_records"], 1):
        raw = run_git("show", f"{BASELINE}:{row['path']}")
        git_blob = run_git("rev-parse", f"{BASELINE}:{row['path']}").decode().strip()
        require(git_blob == row["blob_sha1"], f"supplemental-blob-drift:{row['path']}")
        require(sha256(raw) == row["sha256_lf"], f"supplemental-hash-drift:{row['path']}")
        routed_commits = [record["commit"] for record in delta["process"]["records"] if row["path"] in record["relevant_supplemental_paths"]]
        supplemental.append({
            "supplemental_id": f"P066-SUPP-DISP-{index:02d}",
            "path": row["path"],
            "blob_sha1": row["blob_sha1"],
            "lines": row["lines"],
            "bytes": len(raw),
            "raw_sha256": sha256(raw),
            "lf_sha256": row["sha256_lf"],
            "read_status": row["human_coverage"]["status"],
            "disposition": "PRESERVE",
            "state": "PRESERVED_LINEAGE",
            "canonical_owner": OWNERS[87],
            "target_phase": 87,
            "separate_from_manifest_occurrences": True,
            "acceptance_criterion": "Retain the fully read supplemental narrative as a separate lineage record; do not fold it into the 433 manifest occurrences or treat it as scientific authority.",
            "routed_commits": routed_commits,
            "external_authority_promoted": False,
        })

    release = delta["process"]["release"]
    routed = delta["process"]["routed"]
    release_set = set(release["commits"])
    routed_set = set(routed["commits"])
    require(release_set <= routed_set, "release-process-orphan")
    process_rows = []
    for index, row in enumerate(delta["process"]["records"], 1):
        process_rows.append({
            "process_disposition_id": f"P066-PROCESS-DISP-{index:03d}",
            "commit": row["commit"],
            "ordinal": row["ordinal"],
            "memberships": row["memberships"],
            "relevant_release_paths": row["relevant_release_paths"],
            "relevant_supplemental_paths": row["relevant_supplemental_paths"],
            "disposition": "PRESERVE",
            "state": "PRESERVED_LINEAGE",
            "canonical_owner": OWNERS[87],
            "target_phase": 87,
            "origin_pointer": f"/process/records/{index - 1}",
            "origin_record_sha256": record_sha(row),
            "external_authority_promoted": False,
        })
        require(bool(row["relevant_release_paths"] or row["relevant_supplemental_paths"]), f"empty-process-route:{row['commit']}")
    process = {
        "release_commit_count": len(release_set),
        "routed_commit_count": len(routed_set),
        "release_commits": release["commits"],
        "routed_commits": routed["commits"],
        "release_orphan_count": len(release_set - routed_set),
        "routed_orphan_count": len(routed_set - {row["commit"] for row in delta["process"]["records"]}),
        "routed_only_commit_count": len(routed_set - release_set),
        "supplemental_touch_commit_count": sum(bool(row["relevant_supplemental_paths"]) for row in delta["process"]["records"]),
        "supplemental_only_commit_count": sum(bool(row["relevant_supplemental_paths"]) and not row["relevant_release_paths"] for row in delta["process"]["records"]),
        "empty_path_union_count": sum(not (row["relevant_release_paths"] or row["relevant_supplemental_paths"]) for row in delta["process"]["records"]),
    }
    require(process["release_orphan_count"] == 0 and process["routed_orphan_count"] == 0, "process-orphan")

    counts = Counter(row["disposition"] for row in rows)
    artifact = {
        "schema_version": "P066_STEP81_1_SOURCE_DISPOSITION_V1",
        "artifact_kind": "PHASE_066_SOURCE_DISPOSITION_MATRIX",
        "phase": 66,
        "step": "81.1",
        "branch": BRANCH,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "gate": "PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS",
        "authority": {"internal_lineage_complete": True, "external_scientific_authority": False, "publication_authority": False},
        "inputs": metadata,
        "source_contract": {
            "occurrence_count": len(rows),
            "unique_blob_count": len(blob_rows),
            "supplemental_count": len(supplemental),
            "allowed_dispositions": sorted(ALLOWED_DISPOSITIONS),
            "occurrence_path_set_sha256": delta["source_summary"]["path_set_sha256"],
            "occurrence_path_blob_set_sha256": delta["source_summary"]["path_blob_sha256"],
            "unique_blob_set_sha256": delta["source_summary"]["unique_blob_sha256"],
            "manifest_raw_sha256": manifest_meta["raw_sha256"],
        },
        "counts": {"source_occurrences": len(rows), "unique_blobs": len(blob_rows), "supplemental": len(supplemental), "distribution": dict(sorted(counts.items()))},
        "process_commit_coverage": process,
        "process_dispositions": process_rows,
        "source_dispositions": rows,
        "blob_disposition_groups": blob_rows,
        "supplemental_dispositions": supplemental,
    }
    return seal(artifact)


def phase057_target(numeric_id: int) -> int:
    matches = [phase for phase, ids in PHASE057_TARGETS.items() if numeric_id in ids]
    require(len(matches) == 1, f"phase057-owner-cardinality:{numeric_id}:{matches}")
    return matches[0]


def phase057_adjudications(delta: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for source in delta["phase057_routes"]["records"]:
        row = dict(source)
        if source["route_class"] == "NEW_P066_INTAKE":
            numeric_id = source["numeric_id"]
            target = phase057_target(numeric_id)
            bounded = numeric_id in BOUNDED_PHASE057
            row["canonical_owner"] = OWNERS[66] if bounded else OWNERS[target]
            row["target_phase"] = 66 if bounded else target
            row["current_state"] = "BOUNDED_HISTORICAL" if bounded else "OPEN_CARRY"
            row["owner_state"] = "ADJUDICATED_P066_STEP81_1"
            row["severity"] = "NONE" if bounded else "P1"
            row["acceptance_criterion"] = (
                "Preserve this exact user-intent observation as bounded history; it creates no active downstream obligation."
                if bounded
                else f"{OWNERS[target]} must resolve or explicitly bound this exact observation before canonical release without backward projection."
            )
        out.append(row)
    return out


def step_records(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    delta = inputs["Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json"]
    fit = inputs["Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"]
    provenance = inputs["Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"]
    optimizer = inputs["Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"]
    authority = inputs["Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json"]
    profile = inputs["Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"]
    rows: list[dict[str, Any]] = []

    def add(origin: str, step: int, claim: str, disposition: str, state: str, target: int, axis: str, pointer: str, source: Any, *, owner: str | None = None, authority_axes: dict[str, Any] | None = None, relation_links: list[str] | None = None) -> None:
        actual_owner = owner or OWNERS[target]
        rows.append({
            "observation_id": origin,
            "origin_step": f"Phase 066 Step {step}",
            "claim": claim,
            "disposition": disposition,
            "evidence_identity_disposition": "PRESERVE",
            "state": state,
            "canonical_owner": actual_owner,
            "target_phase": target,
            "authority_axis": axis,
            "authority_axes": authority_axes or {
                "evidence_identity": {"disposition": "PRESERVE", "authority": "INTERNAL_AUDIT_EVIDENCE"},
                "empirical": {"authority": False},
                "physical": {"authority": False},
                "external": {"authority": False},
            },
            "acceptance_criterion": (
                f"{actual_owner} must resolve or explicitly bound this observation before canonical release."
                if state == "OPEN_CARRY" else "Preserve this bounded internal or historical observation without external-authority promotion."
            ),
            "origin_path": pointer.split("#", 1)[0],
            "origin_pointer": pointer.split("#", 1)[1],
            "origin_record_sha256": record_sha(source),
            "semantic_fingerprint": sha256(claim.strip().casefold().encode("utf-8")),
            "relation_links": relation_links or [],
            "external_authority_promoted": False,
        })

    for defect in delta["observed_defects"]:
        add(defect["defect_id"], 76, defect["kind"], "CORRECT", "OPEN_CARRY", 89, "RELEASE_ARTIFACT", "Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json#/observed_defects", defect)

    add("P066-S77-RAW-BINDING", 77, "Exact original parquet, specimen UUID and extraction cryptographic binding remain unavailable.", "GROUND_NOT_FOUND", "OPEN_CARRY", 72, "EMPIRICAL_PROVENANCE", "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json#/raw_input", provenance["raw_input"])
    add("P066-S77-OPTIMIZER-CONTRACT", 77, "The source-explicit replay optimizer contract is preserved, while the absent historical execution state is enumerated field by field in Step 78.", "PRESERVE", "BOUNDED_INTERNAL", 66, "OPTIMIZER", "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json#/optimizer_contract", provenance["optimizer_contract"], relation_links=[f"P066-S78-ORIGINAL-STATE-{re.sub(r'[^A-Z0-9]+', '-', row['field'].upper()).strip('-')}" for row in optimizer["original_optimizer_state_availability"]])
    heldout = authority["claim_rows"][0]["held_out_evidence"]
    add("P066-S77-HELDOUT", 77, "Held-out cells, rates and temperatures were not tested.", "GROUND_NOT_FOUND", "OPEN_CARRY", 86, "EMPIRICAL_VALIDATION", "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json#/claim_rows/0/held_out_evidence", heldout)
    add("P066-S77-NONCONVERGED", 77, "The selected Direct14 replay trial is numerically retained but nonconverged.", "PRESERVE", "OPEN_CARRY", 86, "OPTIMIZER", "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json#/status", fit["status"], authority_axes={"evidence_identity": {"disposition": "PRESERVE", "authority": "INTERNAL_RUNTIME_FACT"}, "calibration_acceptance": {"disposition": "WITHHOLD", "authority": False}, "physical": {"authority": False}, "external": {"authority": False}})

    add("P066-S78-STORED-VECTOR", 78, "The rounded stored vector is within bounds and has one exact upper-bound component.", "PRESERVE", "BOUNDED_INTERNAL", 66, "OPTIMIZER_VECTOR", "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json#/vector_bound_classification/0", optimizer["vector_bound_classification"][0])
    add("P066-S78-REPLAY-VECTORS", 78, "Python 3.12 and 3.14 replay vectors agree and approach a different upper-bound component.", "PRESERVE", "BOUNDED_INTERNAL", 66, "OPTIMIZER_VECTOR", "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json#/vector_bound_classification/1", optimizer["vector_bound_classification"][1:3])
    availability_ids = []
    for index, item in enumerate(optimizer["original_optimizer_state_availability"]):
        field_id = re.sub(r"[^A-Z0-9]+", "-", item["field"].upper()).strip("-")
        origin = f"P066-S78-ORIGINAL-STATE-{field_id}"
        availability_ids.append(origin)
        add(origin, 78, f"Original historical optimizer field `{item['field']}` remains GROUND_NOT_FOUND.", "GROUND_NOT_FOUND", "OPEN_CARRY", 81, "IDENTIFIABILITY", f"Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json#/original_optimizer_state_availability/{index}", item)
    add("P066-S78-ORIGINAL-VECTOR-CLASS", 78, "The original historical vector classification is a bounded summary of the field-level GROUND_NOT_FOUND records.", "PRESERVE", "BOUNDED_INTERNAL", 66, "IDENTIFIABILITY", "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json#/vector_bound_classification/3", optimizer["vector_bound_classification"][3], relation_links=availability_ids)
    add("P066-S78-OBJECTIVE", 78, "Stored and replay vectors are not equivalent although their curves satisfy the bounded replay tolerance.", "PRESERVE", "OPEN_CARRY", 81, "IDENTIFIABILITY", "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json#/curve_objective_classification", optimizer["curve_objective_classification"], authority_axes={"evidence_identity": {"disposition": "PRESERVE", "authority": "INTERNAL_NUMERICAL_COMPARISON"}, "parameter_identifiability": {"disposition": "WITHHOLD", "authority": False}, "curve_replay": {"authority": "BOUNDED_TOLERANCE_EQUIVALENCE"}, "external": {"authority": False}})

    for index, claim in enumerate(authority["claim_rows"]):
        preserve = claim["id"] == "E79-01"
        ref7_reference = claim["id"] == "P79-08"
        disposition = "PRESERVE" if preserve else ("GROUND_NOT_FOUND" if claim["status"] == "GROUND_NOT_FOUND" else "WITHHOLD")
        state = "BOUNDED_INTERNAL" if preserve else ("BOUNDED_REFERENCE" if ref7_reference else "OPEN_CARRY")
        owner_digits = re.search(r"(?:PHASE-|P)(\d{3})", claim["owner"])
        require(owner_digits is not None, f"claim-owner-phase:{claim['id']}")
        target = int(owner_digits.group(1))
        axes = {
            "evidence_identity": {"disposition": "PRESERVE", "authority": "INTERNAL_AUDIT_EVIDENCE"},
            "empirical": {"pass": claim["empirical_pass"], "disposition": "PRESERVE" if claim["empirical_pass"] else disposition, "ceiling": claim["empirical_ceiling"]},
            "physical": {"authority": claim["physical_authority"], "disposition": "WITHHOLD", "ceiling": claim["physical_ceiling"]},
            "phase": {"authority": claim["phase_authority"]},
            "proposition": {"authority": claim["proposition_authority"]},
            "external": {"authority": claim["external_authority"]},
        }
        canonical_claim_owner = OWNERS[71] if claim["owner"] == "P071-PRIMARY-SOURCE-ACQUISITION" else claim["owner"]
        add(f"P066-{claim['id']}", 79, claim["claim"], disposition, state, target, "EMPIRICAL_AND_PHYSICAL_SEPARATED", f"Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json#/claim_rows/{index}", claim, owner=canonical_claim_owner, authority_axes=axes, relation_links=["D74-006", "P065-SEM-002"] if ref7_reference else [])
        rows[-1]["source_owner"] = claim["owner"]

    contradiction_keys = {"divergent_7_7_pair_examples", "stale_alpha_comment", "stale_class_docstring", "stale_header_comment"}
    evidence_targets = {"fitting_guide": 81, "production_assignment": 85, "test_mutation": 88}
    for key, evidence in sorted(profile["evidence_columns"].items()):
        is_open = key in contradiction_keys
        target = 83 if is_open else evidence_targets.get(key, 66)
        add(f"P066-S80-EVIDENCE-{key.upper()}", 80, evidence["claim"], "CORRECT" if is_open else "PRESERVE", "OPEN_CARRY" if is_open else "BOUNDED_INTERNAL", target, "IMPLEMENTATION_CONTRACT", f"Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json#/evidence_columns/{key}", evidence)
    for index, route in enumerate(profile["route_rows"]):
        owner_digits = re.search(r"(?:PHASE-|P)(\d{3})", route["owner"])
        require(owner_digits is not None, f"route-owner-phase:{route['id']}")
        target = int(owner_digits.group(1))
        open_code_history = route["id"] == "R80-14"
        add(f"P066-{route['id']}", 80, f"Bounded runtime route {route['route_id']} classified with no external material or profile-selection authority.", "WITHHOLD" if open_code_history else "PRESERVE", "OPEN_CARRY" if open_code_history else "BOUNDED_INTERNAL", target, "RUNTIME_PROFILE", f"Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json#/route_rows/{index}", route, owner=route["owner"], authority_axes={"evidence_identity": {"disposition": "PRESERVE", "authority": "INTERNAL_RUNTIME_OBSERVATION"}, "serialized_compatibility": {"disposition": "WITHHOLD" if open_code_history else "PRESERVE", "status": route["serialized_compatibility"]}, "profile_selection": {"authority": route["profile_selection_authority"]}, "external_material": {"authority": route["external_material_authority"]}, "multi_temperature_experimental": {"authority": route["multi_temperature_experimental_authority"]}})
        rows[-1]["source_owner"] = route["owner"]
    return rows


def build_carry(inputs: dict[str, Any], metadata: list[dict[str, Any]], source: dict[str, Any]) -> dict[str, Any]:
    prior = inputs["Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json"]
    delta = inputs["Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json"]
    routes = phase057_adjudications(delta)
    new_phase057 = [row for row in routes if row["route_class"] == "NEW_P066_INTAKE"]
    shared_phase057 = [row for row in routes if row["route_class"] == "SHARED_P065_REFERENCE"]
    prior_phase057 = [row for row in prior["observation_records"] if row["origin_step"] == "Phase 057"]
    prior_phase057_ids = {int(row["observation_id"].rsplit("-", 1)[1]) for row in prior_phase057}
    new_phase057_ids = {row["numeric_id"] for row in new_phase057}
    shared_phase057_ids = {row["numeric_id"] for row in shared_phase057}
    phase057_union = prior_phase057_ids | new_phase057_ids
    require(len(prior_phase057_ids) == 82, "prior-phase057-loss")
    require(new_phase057_ids == set(range(293, 388)), "new-phase057-loss")
    require(shared_phase057_ids == set(range(395, 405)) and shared_phase057_ids <= prior_phase057_ids, "ay-overlap-loss")
    require(phase057_union == set(range(228, 405)), "phase057-union-loss")
    step_rows = step_records(inputs)
    active_new = [row for row in [*new_phase057, *step_rows] if row.get("current_state") == "OPEN_CARRY" or row.get("state") == "OPEN_CARRY"]
    active = [dict(row) for row in prior["active_obligations"]]
    for index, row in enumerate(active_new, 1):
        identity = row.get("observation_id")
        active.append({
            "obligation_id": f"P066-OBL-{index:04d}",
            "origin_identity": identity,
            "state": "OPEN_CARRY",
            "canonical_owner": row["canonical_owner"],
            "target_phase": row["target_phase"],
            "acceptance_criterion": row["acceptance_criterion"],
            "semantic_fingerprint": row["semantic_fingerprint"],
            "relation_links": [],
            "external_authority_promoted": False,
        })

    prior_registry = prior["current_owner_duplicate_check_universe"]["records"]
    registry = [dict(row) for row in prior_registry]
    registry_origins = {row["origin_identity"] for row in registry}
    for row in [*new_phase057, *step_rows]:
        identity = row["observation_id"]
        require(identity not in registry_origins, f"lost-ay-dedup:{identity}")
        registry_origins.add(identity)
        registry.append({
            "registry_id": f"P066-OWNER-{len(registry)+1:04d}",
            "origin_identity": identity,
            "origin_record_sha256": record_sha(row),
            "owner_id": row["canonical_owner"],
            "state": row.get("current_state", row.get("state")),
            "target_phase": row["target_phase"],
        })

    origins = [row["origin_identity"] for row in registry]
    active_origins = [row["origin_identity"] for row in active]
    require(len(origins) == len(set(origins)), "multiple-owner-registry")
    require(len(active_origins) == len(set(active_origins)), "multiple-active-owner")
    require(all(row["canonical_owner"] for row in active), "ownerless-active")
    require({row["observation_id"] for row in shared_phase057} <= {row["origin_identity"] for row in prior_registry}, "lost-ay-reference")

    ref7 = next(row for row in active if row["origin_identity"] == "D74-006")
    require(ref7["canonical_owner"] == OWNERS[71], "ref7-owner-drift")
    artifact = {
        "schema_version": "P066_STEP81_1_CARRY_FORWARD_V1",
        "artifact_kind": "PHASE_066_CARRY_FORWARD_DELTA",
        "phase": 66,
        "step": "81.1",
        "branch": BRANCH,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "gate": "PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS",
        "authority": {"internal_audit_complete": True, "external_scientific_authority": False, "publication_authority": False},
        "inputs": metadata,
        "source_disposition_semantic_sha256": source["semantic_sha256"],
        "prior_phase065_snapshot": {
            "observation_count": len(prior["observation_records"]),
            "active_obligation_count": len(prior["active_obligations"]),
            "owner_registry_count": len(prior_registry),
            "observation_records_sha256": sha256(compact(prior["observation_records"])),
            "active_obligations_sha256": sha256(compact(prior["active_obligations"])),
            "owner_registry_sha256": sha256(compact(prior_registry)),
        },
        "inherited_phase065_observations": prior["observation_records"],
        "phase057_route_adjudications": routes,
        "phase057_lineage": {
            "prior_count": len(prior_phase057_ids),
            "new_count": len(new_phase057_ids),
            "ay_overlap_count": len(shared_phase057_ids),
            "union_count": len(phase057_union),
            "union_numeric_range": [min(phase057_union), max(phase057_union)],
            "prior_only_ax_ids": sorted(prior_phase057_ids - shared_phase057_ids - set(range(228, 293))),
            "lost_id_count": len(set(range(228, 405)) - phase057_union),
            "duplicate_new_id_count": len(new_phase057_ids & prior_phase057_ids),
        },
        "phase057_shared_reference_ids": [row["observation_id"] for row in shared_phase057],
        "step76_80_disposition_records": step_rows,
        "active_obligations": active,
        "current_owner_duplicate_check_universe": {
            "record_count": len(registry),
            "records_sha256": sha256(compact(registry)),
            "records": registry,
        },
        "ref7_canonical_route": {
            "origin_identity": "D74-006",
            "status": "GROUND_NOT_FOUND",
            "canonical_owner": OWNERS[71],
            "target_phase": 71,
            "external_authority_promoted": False,
            "acceptance_criterion": ref7["acceptance_criterion"],
        },
        "gate_summary": {
            "source_occurrences": source["counts"]["source_occurrences"],
            "unique_blobs": source["counts"]["unique_blobs"],
            "prior_observations": len(prior["observation_records"]),
            "prior_active_obligations": len(prior["active_obligations"]),
            "phase057_intake_rows": len(routes),
            "phase057_union": len(phase057_union),
            "phase057_prior": len(prior_phase057_ids),
            "phase057_new": len(new_phase057),
            "phase057_shared": len(shared_phase057),
            "ay_duplicate_new_obligations": 0,
            "step76_80_records": len(step_rows),
            "active_obligations": len(active),
            "owner_registry_records": len(registry),
            "ownerless_active_obligations": 0,
            "multiply_owned_active_obligations": 0,
            "lost_inherited_ids": 0,
            "external_authority_promotions": 0,
            "phase_ceiling": "CONDITIONAL_P066",
            "status": "PASS_WITH_CONCERNS",
        },
    }
    return seal(artifact)


def staged_bytes(path: Path, raw: bytes, suffix: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=suffix, dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        return temporary
    except Exception:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def atomic_write_pair(items: list[tuple[Path, bytes]]) -> None:
    require(len(items) == 2, "atomic-pair-cardinality")
    staged: dict[Path, str] = {}
    backups: dict[Path, str | None] = {}
    replaced: list[Path] = []
    try:
        for path, raw in items:
            staged[path] = staged_bytes(path, raw, ".tmp")
            backups[path] = staged_bytes(path, path.read_bytes(), ".bak") if path.exists() else None
        for path, _ in items:
            os.replace(staged[path], path)
            replaced.append(path)
    except Exception:
        for path in reversed(replaced):
            backup = backups[path]
            if backup is None:
                if path.exists():
                    os.unlink(path)
            else:
                os.replace(backup, path)
        raise
    finally:
        for temporary in [*staged.values(), *(value for value in backups.values() if value is not None)]:
            if os.path.exists(temporary):
                os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disposition", default=DISPOSITION_PATH)
    parser.add_argument("--carry", default=CARRY_PATH)
    args = parser.parse_args()
    require(args.disposition == DISPOSITION_PATH and args.carry == CARRY_PATH, "output-path-not-allowlisted")
    inputs, metadata = load_inputs()
    source = build_source(inputs, metadata)
    carry = build_carry(inputs, metadata, source)
    atomic_write_pair([
        (ROOT / args.disposition, canonical(source)),
        (ROOT / args.carry, canonical(carry)),
    ])
    print("PASS_P066_STEP81_1_BUILD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
