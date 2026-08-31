#!/usr/bin/env python3
"""Build deterministic Phase 065 Step 75.1 disposition artifacts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any


REPO = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "a04bca9c73941e1a4fbc0ab6e4f4e49514dcce12"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase065): disposition v1024 lineage"
GATE = "PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS"

TOPOLOGY = "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json"
READ = "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json"
CODE = "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"
STATIC = "Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json"
SCIENCE = "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json"
INIT = "Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json"
RUNTIME = "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json"
CONFORMANCE = "Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json"
P64_DISPOSITION = "Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json"
P64_CARRY = "Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json"
INPUT_PATHS = (TOPOLOGY, READ, CODE, STATIC, SCIENCE, INIT, RUNTIME, CONFORMANCE, P64_DISPOSITION, P64_CARRY)

BUILDER = "Codex/work/v1024_phase065/build_phase065_step75_1.py"
VALIDATOR = "Codex/work/v1024_phase065/validate_phase065_step75_1.py"
DISPOSITION = "Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json"
CARRY = "Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json"
RESULT = "Codex/results/PHASE_065_STEP_075_1_DISPOSITION_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
CONTROL_PATHS = (BUILDER, VALIDATOR, RESULT, PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)

ALLOWED_DISPOSITIONS = {"PRESERVE", "CORRECT", "THEORY_ONLY", "UNVERIFIED", "REJECTED_SOURCE", "DISCARD"}
UNVERIFIED_ROWS = {"D74-004", "D74-005", "D74-012", "D74-014", "D74-039", "D74-040", "D74-041"}
REJECTED_NORMAL_PATHS = {"Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex"}
OPEN_SOURCE_DISPOSITIONS = {"CORRECT", "UNVERIFIED"}

SOURCE_OWNER = {
    "PRESERVE": (90, "PHASE-090-RELEASE-PRESERVATION"),
    "CORRECT": (87, "PHASE-087-CANONICAL-SOURCE-SYNTHESIS"),
    "THEORY_ONLY": (82, "PHASE-082-CANONICAL-EQUATION-FREEZE"),
    "UNVERIFIED": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
    "REJECTED_SOURCE": (87, "PHASE-087-MANUSCRIPT-ASSEMBLY"),
    "DISCARD": (89, "PHASE-089-RELEASE-QA"),
}

P57_OWNERS = {
    "INTENT-PROV-0230": (74, "PHASE-074-FOUNDATION"),
    "INTENT-PROV-0266": (74, "PHASE-074-FOUNDATION"),
    "INTENT-PROV-0267": (75, "PHASE-075-EQUILIBRIUM-PHASE"),
    "INTENT-PROV-0284": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0285": (75, "PHASE-075-EQUILIBRIUM-PHASE"),
    "INTENT-PROV-0286": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0390": (89, "PHASE-089-RELEASE-QA"),
    "INTENT-PROV-0392": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0393": (75, "PHASE-075-EQUILIBRIUM-PHASE"),
    "INTENT-PROV-0395": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0397": (81, "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION"),
    "INTENT-PROV-0398": (81, "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION"),
    "INTENT-PROV-0399": (77, "PHASE-077-GRAPHITE-CLOSURE"),
    "INTENT-PROV-0400": (86, "PHASE-086-CALIBRATION-VALIDATION"),
    "INTENT-PROV-0401": (75, "PHASE-075-EQUILIBRIUM-PHASE"),
    "INTENT-PROV-0402": (82, "PHASE-082-CANONICAL-EQUATION-FREEZE"),
    "INTENT-PROV-0403": (88, "PHASE-088-SCIENTIFIC-REDTEAM"),
}

S71_OWNERS = {
    "P065-S71-F01": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F02": (80, "PHASE-080-BLEND-CLOSURE"),
    "P065-S71-F03": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F04": (74, "PHASE-074-FOUNDATION"),
    "P065-S71-F05": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F06": (78, "PHASE-078-LCO-CLOSURE"),
    "P065-S71-F07": (85, "PHASE-085-STRUCTURE-FREEZE"),
    "P065-S71-F08": (77, "PHASE-077-GRAPHITE-CLOSURE"),
    "P065-S71-F09": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F10": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F11": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F12": (86, "PHASE-086-CALIBRATION-VALIDATION"),
    "P065-S71-F13": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
}

S72_OWNERS = {
    "S72-F01": (66, "P066-LINEAGE"),
    "S72-F02": (78, "PHASE-078-LCO-CLOSURE"),
    "S72-F03": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
    "S72-F04": (67, "P067-CODE-HISTORY"),
    "S72-F05": (65, "P065-STEP75-DISPOSITION"),
    "S72-F06": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
}

REF7_SUPERSEDED = {"P065-S70-F09", "P065-S70-F24", "P065-S71-F13", "P065-S72-F06"}
REF7_OWNER = "PHASE-071-PRIMARY-SOURCE-ACQUISITION"
REF7_ACCEPTANCE = "Superseded by the D74-006 Ref. 7 primary-source acquisition route; D74-006 alone carries the active proposition/page/equation acceptance criterion."
ADDITIONAL_REFINES = {
    "P065-S72-F06": ["P065-S71-F13"],
    "D74-006": ["P065-S72-F06"],
}

INHERITED = {
    "P059-CFR-CF-01": (65, "P059-CFR-CF-01", "PRESERVED_ACTIVE"),
    "P059-CFR-CF-02": (65, "P059-CFR-CF-02", "PRESERVED_ACTIVE"),
    "P059-CFR-CF-06": (65, "P059-CFR-CF-06", "PRESERVED_ACTIVE"),
    "P059-CFR-CF-07": (65, "P059-CFR-CF-07", "PRESERVED_ACTIVE"),
    "P059-CFR-RB-02": (65, "P059-CFR-RB-02", "OPEN_CARRY"),
    "P059-CFR-RB-03": (65, "P059-CFR-RB-03", "OPEN_CARRY"),
}

AUTHORITY = {
    "internal_lineage_disposition": True,
    "external_scientific_truth": False,
    "external_material_truth": False,
    "external_experimental_truth": False,
    "external_proposition_support": False,
    "canonical_model_selected": False,
    "production_repair_complete": False,
    "publication_ready": False,
    "new_phase065_blocker_created": False,
    "ceiling": "Complete internal v1.0.24/v1.0.24.1 disposition and single-owner routing only.",
}


class BuildError(RuntimeError):
    pass


def require(condition: bool, code: str) -> None:
    if not condition:
        raise BuildError(code)


def run_process(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, text: bool = False) -> bytes | str:
    proc = run_process(["git", *args])
    if proc.returncode:
        raise BuildError(f"E_GIT:{' '.join(args)}:{proc.stderr.decode('utf-8', errors='replace')}")
    return proc.stdout.decode("utf-8") if text else proc.stdout


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def record_sha(value: Any) -> str:
    return sha256(compact(value))


def strict_load(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, "E_DUPLICATE_KEY")
            out[key] = value
        return out

    def constant(value: str) -> None:
        raise BuildError(f"E_NONFINITE:{value}")

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, float):
            require(math.isfinite(item), "E_NONFINITE")
        elif isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return value


def traverse(value: Any) -> tuple[int, int]:
    count = 0
    depth = 0
    stack = [(value, 1)]
    while stack:
        item, level = stack.pop()
        count += 1
        depth = max(depth, level)
        if isinstance(item, dict):
            stack.extend((child, level + 1) for child in item.values())
        elif isinstance(item, list):
            stack.extend((child, level + 1) for child in item)
    return count, depth


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    objects: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for path in INPUT_PATHS:
        raw = git("show", f"{PARENT}:{path}")
        assert isinstance(raw, bytes)
        obj = strict_load(raw)
        nodes, depth = traverse(obj)
        objects[path] = obj
        metadata.append({
            "path": path,
            "revision": PARENT,
            "git_blob": str(git("rev-parse", f"{PARENT}:{path}", text=True)).strip(),
            "sha256": sha256(raw),
            "size_bytes": len(raw),
            "nodes": nodes,
            "depth": depth,
            "read_status": "MACHINE_FULL_TRAVERSAL",
        })
    return objects, metadata


def control_binding(path: str) -> dict[str, Any]:
    raw = git("show", f":{path}")
    assert isinstance(raw, bytes)
    return {
        "path": path,
        "git_blob": str(git("rev-parse", f":{path}", text=True)).strip(),
        "sha256": sha256(raw),
        "size_bytes": len(raw),
    }


def normalized_path(path: str) -> str:
    return path.replace("/v1.0.24.1/", "/v1.0.24/")


def linked_conformance_rows(conformance: dict[str, Any]) -> dict[str, set[str]]:
    links: dict[str, set[str]] = {}
    for row in conformance["conformance_rows"]:
        for surface in row["claim_surface"]:
            path = surface["path"]
            if path.startswith("Claude/"):
                links.setdefault(normalized_path(path), set()).add(row["row_id"])
    return links


def disposition_for(role: str, path: str, row_ids: set[str], row_map: dict[str, dict[str, Any]]) -> str:
    if path in REJECTED_NORMAL_PATHS:
        return "REJECTED_SOURCE"
    if row_ids & UNVERIFIED_ROWS:
        return "UNVERIFIED"
    if any(row_map[row_id]["status"] == "OPEN_ROUTED" for row_id in row_ids):
        return "CORRECT"
    if role == "theory":
        return "THEORY_ONLY"
    return "PRESERVE"


def source_acceptance(disposition: str, target: int) -> str:
    actions = {
        "PRESERVE": "preserve the exact historical identity and authority ceiling",
        "CORRECT": "retain only corrected propositions and repair every linked conformance route without rewriting frozen source",
        "THEORY_ONLY": "preserve the derivation only within its stated assumptions and with no material-truth promotion",
        "UNVERIFIED": "obtain primary/material/held-out authority or keep the proposition explicitly unverified",
        "REJECTED_SOURCE": "preserve the non-graft decision and exclude this candidate from canonical assembly",
        "DISCARD": "exclude the artifact from release while retaining this audit identity",
    }
    return f"Phase {target:03d} must {actions[disposition]}."


def source_dispositions(inputs: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    topology = inputs[TOPOLOGY]
    conformance = inputs[CONFORMANCE]
    occurrences = topology["occurrences"]
    unique = topology["unique_sources"]
    row_map = {row["row_id"]: row for row in conformance["conformance_rows"]}
    links = linked_conformance_rows(conformance)
    unique_index = {row["blob"]: index for index, row in enumerate(unique)}
    by_blob: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for index, occurrence in enumerate(occurrences):
        by_blob.setdefault(occurrence["blob"], []).append((index, occurrence))
    group_rows: list[dict[str, Any]] = []
    group_disposition: dict[str, str] = {}
    for blob, members in sorted(by_blob.items()):
        role_set = {member["role"] for _, member in members}
        require(len(role_set) == 1, "E_BLOB_ROLE_CONFLICT")
        path_set = {normalized_path(member["path"]) for _, member in members}
        linked = set().union(*(links.get(path, set()) for path in path_set))
        candidates = {disposition_for(next(iter(role_set)), path, linked, row_map) for path in path_set}
        require(len(candidates) == 1, "E_BLOB_DISPOSITION_CONFLICT")
        disposition = next(iter(candidates))
        group_disposition[blob] = disposition
        group_rows.append({
            "blob": blob,
            "dedup_group": members[0][1]["dedup_group"],
            "occurrence_ids": [member["ordinal"] for _, member in members],
            "paths": [member["path"] for _, member in members],
            "disposition": disposition,
            "linked_conformance_rows": sorted(linked),
            "unique_source_pointer": f"/unique_sources/{unique_index[blob]}",
            "unique_source_record_sha256": record_sha(unique[unique_index[blob]]),
        })
    require(len(group_rows) == 131, "E_UNIQUE_BLOB_DENOMINATOR")
    rows: list[dict[str, Any]] = []
    status_map = {
        "PRESERVE": "BOUNDED_PRESERVE", "CORRECT": "OPEN_CORRECTION",
        "THEORY_ONLY": "BOUNDED_THEORY_ONLY", "UNVERIFIED": "OPEN_UNVERIFIED",
        "REJECTED_SOURCE": "CLOSED_REJECTED_SOURCE", "DISCARD": "CLOSED_DISCARD",
    }
    for index, occurrence in enumerate(occurrences):
        disposition = group_disposition[occurrence["blob"]]
        require(disposition in ALLOWED_DISPOSITIONS, "E_DISPOSITION_ENUM")
        target, owner = SOURCE_OWNER[disposition]
        row_ids = sorted(links.get(normalized_path(occurrence["path"]), set()))
        evidence = [{
            "artifact_path": TOPOLOGY,
            "json_pointer": f"/occurrences/{index}",
            "record_sha256": record_sha(occurrence),
            "role": "OCCURRENCE_IDENTITY",
        }]
        for row_id in row_ids:
            row_index = next(i for i, row in enumerate(conformance["conformance_rows"]) if row["row_id"] == row_id)
            evidence.append({
                "artifact_path": CONFORMANCE,
                "json_pointer": f"/conformance_rows/{row_index}",
                "record_sha256": record_sha(conformance["conformance_rows"][row_index]),
                "role": "CONFORMANCE_ROUTE",
            })
        rows.append({
            "disposition_id": f"P065-DISP-{index + 1:04d}",
            "source_path": occurrence["path"],
            "blob": occurrence["blob"],
            "occurrence_identity": copy.deepcopy(occurrence),
            "dedup_group": occurrence["dedup_group"],
            "role": occurrence["role"],
            "read_status": occurrence["read_status"],
            "read_ranges": occurrence["read_ranges"],
            "disposition": disposition,
            "status": status_map[disposition],
            "reason": f"Exact occurrence is classified from its frozen role, 131-blob dedup identity, and linked Step 74 rows {row_ids}; v1.0.24.1 mirror membership does not add authority.",
            "evidence_routes": evidence,
            "open_routes": [row_id for row_id in row_ids if row_map[row_id]["status"] == "OPEN_ROUTED" and row_id != "D74-007"],
            "canonical_owner": owner,
            "acceptance_criterion": source_acceptance(disposition, target),
            "target_phase": target,
            "external_authority_promoted": False,
        })
    require(len(rows) == 261, "E_OCCURRENCE_DENOMINATOR")
    return rows, group_rows


def phase_from_owner(owner: str, fallback: int) -> int:
    match = re.search(r"(?:PHASE-|P)(\d{3})", owner)
    return int(match.group(1)) if match else fallback


def fingerprint(text: str) -> str:
    normalized = " ".join(re.findall(r"[a-z0-9가-힣]+", text.lower()))
    return sha256(normalized.encode("utf-8"))


def observation(
    observation_id: str, origin_step: str, origin_path: str, pointer: str,
    record: dict[str, Any], claim: str, state: str, severity: str,
    inherited_owner: str | None, owner: str, target: int,
    acceptance: str, refines: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "observation_id": observation_id,
        "origin_step": origin_step,
        "origin_path": origin_path,
        "origin_pointer": pointer,
        "origin_record_sha256": record_sha(record),
        "origin_record": record,
        "claim": claim,
        "state": state,
        "severity": severity,
        "inherited_owner": inherited_owner,
        "canonical_owner": owner,
        "target_phase": target,
        "acceptance_criterion": acceptance,
        "semantic_fingerprint": fingerprint(claim),
        "refines": sorted(refines or []),
        "refined_by": [],
        "external_authority_promoted": False,
    }


def deepest_carry_record(value: Any, wanted: str, path: str = "") -> tuple[str, dict[str, Any]] | None:
    best: tuple[str, dict[str, Any]] | None = None
    if isinstance(value, dict):
        if value.get("carry_forward_id") == wanted and "acceptance_criterion" in value:
            best = (path, value)
        for key, child in value.items():
            found = deepest_carry_record(child, wanted, f"{path}/{key}")
            if found is not None and (best is None or found[0].count("/") > best[0].count("/")):
                best = found
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found = deepest_carry_record(child, wanted, f"{path}/{index}")
            if found is not None and (best is None or found[0].count("/") > best[0].count("/")):
                best = found
    return best


def step74_successors(conformance: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    successors: dict[str, list[dict[str, Any]]] = {}
    for row in conformance["conformance_rows"]:
        for origin in row["origin_routes"]:
            successors.setdefault(origin, []).append(row)
    return successors


def supersession_contract(origin_id: str, successors: dict[str, list[dict[str, Any]]]) -> tuple[str, int, str] | None:
    rows = successors.get(origin_id, [])
    if not rows:
        return None
    active_successors = [row for row in rows if row["status"] == "OPEN_ROUTED" and row["row_id"] != "D74-007"]
    governing = active_successors or rows
    owners = {row["owner"] for row in governing}
    require(len(owners) == 1, f"E_SUPERSESSION_MULTIPLE_OWNER:{origin_id}")
    owner = next(iter(owners))
    target = phase_from_owner(owner, 65)
    row_ids = sorted(row["row_id"] for row in rows)
    acceptance = f"Superseded by Step 74 rows {row_ids}; their exact row-level acceptance criteria govern and this origin is not counted as a second active obligation."
    return owner, target, acceptance


def build_observations(inputs: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    successors = step74_successors(inputs[CONFORMANCE])
    p57 = inputs[TOPOLOGY]["phase057_observations"]["records"]
    for index, record in enumerate(p57):
        is_open = record["open_in_v1024_mirror"]
        if is_open:
            target, owner = P57_OWNERS[record["id"]]
            state = "OPEN_CARRY"
            acceptance = f"{owner} must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24."
        else:
            target, owner, state = 65, "P065-STEP75-DISPOSITION", "BOUNDED_HISTORICAL"
            acceptance = "Preserve the exact Phase 057 observation as bounded history; it creates no active owner obligation."
        rows.append(observation(record["id"], "Phase 057", TOPOLOGY, f"/phase057_observations/records/{index}", record, record["title"], state, "P1" if is_open else "NONE", None, owner, target, acceptance))

    s70 = inputs[TOPOLOGY]["findings"]
    for index, record in enumerate(s70):
        is_open = record["status"] == "OPEN_ROUTED"
        owner = record.get("owner") or "P065-STEP75-DISPOSITION"
        target = phase_from_owner(owner, 65)
        state = "OPEN_CARRY" if is_open else "CLOSED_OR_BOUND"
        acceptance = f"{owner} must satisfy the exact Step 70 finding or preserve its confirmed/corrected/bound state without authority promotion."
        supersession = supersession_contract(record["id"], successors)
        if supersession is not None:
            owner, target, acceptance = supersession
            state = "SUPERSEDED_BY_STEP74"
        if record["id"] in REF7_SUPERSEDED:
            owner, target, acceptance, state = REF7_OWNER, 71, REF7_ACCEPTANCE, "SUPERSEDED_BY_STEP74"
        rows.append(observation(record["id"], "Step 70", TOPOLOGY, f"/findings/{index}", record, record.get("finding", record.get("summary", "")), state, record.get("severity", "NONE"), record.get("owner"), owner, target, acceptance))

    s71 = inputs[CODE]["findings"]
    for index, record in enumerate(s71):
        target, owner = S71_OWNERS[record["finding_id"]]
        state = "OPEN_CARRY"
        acceptance = f"{owner} must close the static finding using the Step 73 bounded runtime evidence where applicable."
        supersession = supersession_contract(record["finding_id"], successors)
        if supersession is not None:
            owner, target, acceptance = supersession
            state = "SUPERSEDED_BY_STEP74"
        if record["finding_id"] in REF7_SUPERSEDED:
            owner, target, acceptance, state = REF7_OWNER, 71, REF7_ACCEPTANCE, "SUPERSEDED_BY_STEP74"
        rows.append(observation(record["finding_id"], "Step 71", CODE, f"/findings/{index}", record, record["title"], state, record["severity"], "P065-STEP73-RUNTIME" if record["finding_id"] not in {"P065-S71-F12", "P065-S71-F13"} else None, owner, target, acceptance, record["step70_routes"]))

    s72 = inputs[SCIENCE]["findings"]
    for index, record in enumerate(s72):
        target, owner = S72_OWNERS[record["id"]]
        closed = record["id"] == "S72-F05"
        observation_id = f"P065-{record['id']}"
        state = "CLOSED_REJECTED_SOURCE" if closed else "OPEN_CARRY"
        acceptance = "Preserve the explicit non-graft decision." if closed else f"{owner} must satisfy the bounded scientific-authority finding without promoting missing external evidence."
        supersession = supersession_contract(observation_id, successors)
        if supersession is not None:
            owner, target, acceptance = supersession
            state = "SUPERSEDED_BY_STEP74"
        if observation_id in REF7_SUPERSEDED:
            owner, target, acceptance, state = REF7_OWNER, 71, REF7_ACCEPTANCE, "SUPERSEDED_BY_STEP74"
        rows.append(observation(observation_id, "Step 72", SCIENCE, f"/findings/{index}", record, record["finding"], state, record["severity"], record["owner"], owner, target, acceptance, ADDITIONAL_REFINES.get(observation_id)))

    s74 = inputs[CONFORMANCE]["conformance_rows"]
    for index, record in enumerate(s74):
        is_open = record["status"] == "OPEN_ROUTED" and record["row_id"] != "D74-007"
        target = phase_from_owner(record["owner"], 65)
        state = "OPEN_CARRY" if is_open else "CLOSED_SUPERSEDED_IN_STEP75_1" if record["row_id"] == "D74-007" else record["status"]
        refines = sorted(set(record["origin_routes"] + ADDITIONAL_REFINES.get(record["row_id"], [])))
        rows.append(observation(record["row_id"], "Step 74", CONFORMANCE, f"/conformance_rows/{index}", record, record["claim"], state, record["severity"], record["owner"], record["owner"], target, record["acceptance_criterion"], refines))

    inherited_rows: list[dict[str, Any]] = []
    for item_id, (target, owner, state) in INHERITED.items():
        found = deepest_carry_record(inputs[P64_CARRY], item_id)
        require(found is not None, f"E_INHERITED_GROUND_NOT_FOUND:{item_id}")
        pointer, record = found
        inherited_rows.append(observation(item_id, "Phase 064 inherited", P64_CARRY, pointer, record, record["acceptance_criterion"], state, "P1" if state == "OPEN_CARRY" else "NONE", item_id, owner, target, record["acceptance_criterion"]))
    rows.extend(inherited_rows)

    by_id = {row["observation_id"]: row for row in rows}
    require(len(by_id) == len(rows), "E_OBSERVATION_DUPLICATE_ID")
    for row in rows:
        for origin in row["refines"]:
            if origin in by_id:
                by_id[origin]["refined_by"].append(row["observation_id"])
    for row in rows:
        row["refined_by"] = sorted(set(row["refined_by"]))
    require(len(rows) == 192, "E_OBSERVATION_DENOMINATOR")
    return rows, inherited_rows


def build(inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    sources, blob_groups = source_dispositions(inputs)
    observations, inherited = build_observations(inputs)
    active = [row for row in observations if row["state"] in {"OPEN_CARRY", "PRESERVED_ACTIVE"}]
    by_fingerprint: dict[str, list[str]] = {}
    for row in observations:
        by_fingerprint.setdefault(row["semantic_fingerprint"], []).append(row["observation_id"])
    duplicate_groups = []
    for key, members in sorted(by_fingerprint.items()):
        if len(members) <= 1:
            continue
        member_rows = [next(row for row in observations if row["observation_id"] == member) for member in members]
        owners = {row["canonical_owner"] for row in member_rows}
        targets = {row["target_phase"] for row in member_rows}
        require(len(owners) == 1 and len(targets) == 1, "E_UNRESOLVED_SEMANTIC_DUPLICATE")
        require(sorted(members) == ["D74-028", "P065-S70-F44"], "E_UNEXPECTED_SEMANTIC_DUPLICATE")
        require(any("P065-S70-F44" in row["refines"] for row in member_rows if row["observation_id"] == "D74-028"), "E_DUPLICATE_RELATION_MISSING")
        duplicate_groups.append({
            "group_id": "P065-SEM-001",
            "match_type": "EXACT_NORMALIZED_TEXT",
            "fingerprint": key,
            "members": sorted(members),
            "canonical_member": "D74-028",
            "canonical_owner": next(iter(owners)),
            "target_phase": next(iter(targets)),
            "status": "RESOLVED_BY_STEP74_REFINEMENT",
        })
    ref7_members = ["P065-S70-F09", "P065-S70-F24", "P065-S71-F13", "P065-S72-F06", "D74-006"]
    observation_ids = {row["observation_id"] for row in observations}
    require(all(identity in observation_ids for identity in ref7_members), "E_REF7_SEMANTIC_GROUP_MEMBER")
    duplicate_groups.append({
        "group_id": "P065-SEM-002",
        "match_type": "SEMANTIC_PRIMARY_SOURCE_AUTHORITY_CHAIN",
        "fingerprint": sha256(b"REF7_PRIMARY_SOURCE_PROPOSITION_AUTHORITY"),
        "members": sorted(ref7_members),
        "canonical_member": "D74-006",
        "canonical_owner": REF7_OWNER,
        "target_phase": 71,
        "status": "RESOLVED_BY_STEP74_REFINEMENT",
    })
    controls = [control_binding(path) for path in CONTROL_PATHS]
    distribution: dict[str, int] = {}
    for row in sources:
        distribution[row["disposition"]] = distribution.get(row["disposition"], 0) + 1
    source = {
        "schema_version": "P065_STEP75_1_SOURCE_DISPOSITION_V1",
        "artifact_kind": "PHASE_065_SOURCE_DISPOSITION_MATRIX",
        "phase": 65, "step": "75.1", "baseline_commit": BASELINE,
        "expected_parent": PARENT, "branch": BRANCH, "expected_subject": SUBJECT,
        "gate": GATE, "inputs": metadata, "control_source_bindings": controls,
        "authority": AUTHORITY,
        "source_contract": {
            "occurrences": 261, "unique_blobs": 131, "mirror_pairs": 130,
            "archive_only_occurrences": 1,
            "allowed_dispositions": sorted(ALLOWED_DISPOSITIONS),
            "identity_rule": "ONE_ROW_PER_OCCURRENCE; ONE_CONSISTENT_DISPOSITION_PER_BLOB; MIRROR_IS_NOT_CORROBORATION",
        },
        "source_dispositions": sources,
        "blob_disposition_groups": blob_groups,
        "counts": {
            "source_dispositions": len(sources), "blob_groups": len(blob_groups),
            "distribution": dict(sorted(distribution.items())),
            "open_source_dispositions": sum(row["disposition"] in OPEN_SOURCE_DISPOSITIONS for row in sources),
            "contradictory_blob_dispositions": 0, "ownerless_sources": 0,
            "external_authority_promotions": 0,
        },
    }
    source_payload = copy.deepcopy(source)
    source["semantic_sha256"] = sha256(canonical(source_payload))

    prior_owner = inputs[P64_CARRY]["canonical_owner_duplicate_check_universe"]
    current_owner_rows = [{
        "registry_id": f"P065-OWNER-{index + 1:04d}",
        "origin_identity": row["observation_id"],
        "owner_id": row["canonical_owner"],
        "target_phase": row["target_phase"],
        "state": row["state"],
        "origin_record_sha256": row["origin_record_sha256"],
    } for index, row in enumerate(observations)]
    carry = {
        "schema_version": "P065_STEP75_1_CARRY_FORWARD_V1",
        "artifact_kind": "PHASE_065_CARRY_FORWARD_DELTA",
        "phase": 65, "step": "75.1", "baseline_commit": BASELINE,
        "expected_parent": PARENT, "branch": BRANCH, "expected_subject": SUBJECT,
        "gate": GATE, "inputs": metadata, "control_source_bindings": controls,
        "authority": AUTHORITY,
        "observation_records": observations,
        "active_obligations": [{
            "obligation_id": f"P065-OBL-{index + 1:04d}",
            "origin_identity": row["observation_id"],
            "state": row["state"],
            "canonical_owner": row["canonical_owner"],
            "target_phase": row["target_phase"],
            "acceptance_criterion": row["acceptance_criterion"],
            "semantic_fingerprint": row["semantic_fingerprint"],
            "relation_links": sorted(set(row["refines"] + row["refined_by"])),
            "external_authority_promoted": False,
        } for index, row in enumerate(active)],
        "inherited_phase064_routes": inherited,
        "prior_phase064_owner_universe_snapshot": {
            "origin_path": P64_CARRY,
            "record_count": prior_owner["record_count"],
            "records_sha256": prior_owner["records_sha256"],
            "artifact_sha256": next(item["sha256"] for item in metadata if item["path"] == P64_CARRY),
            "status": "PRESERVED_BY_REFERENCE_NOT_REACTIVATED_WHOLESALE",
        },
        "current_owner_duplicate_check_universe": {
            "record_count": len(current_owner_rows),
            "records_sha256": record_sha(current_owner_rows),
            "records": current_owner_rows,
        },
        "semantic_duplicate_groups": duplicate_groups,
        "new_phase065_blockers": [],
        "gate_summary": {
            "source_occurrences": len(sources), "unique_blobs": len(blob_groups),
            "phase057_records": 82, "phase057_open": 17,
            "step70_findings": 44, "step70_open": 39,
            "step71_findings": 13, "step71_open": 13,
            "step72_findings": 6, "step72_open": 5,
            "step74_rows": 41, "step74_open_input": 35, "step74_open_after_disposition": 34,
            "inherited_phase064_routes": 6,
            "step74_origin_routes_superseded": 17,
            "semantic_chain_superseded": 4,
            "active_obligations": len(active),
            "ownerless_active_obligations": sum(not row["canonical_owner"] for row in active),
            "multiply_owned_active_obligations": 0,
            "semantic_duplicate_groups": len(duplicate_groups),
            "unresolved_semantic_duplicates": 0,
            "new_phase065_blockers": 0,
            "external_authority_promotions": 0,
            "phase_ceiling": "CONDITIONAL_P065",
            "status": "PASS_WITH_CONCERNS",
        },
    }
    carry_payload = copy.deepcopy(carry)
    carry["semantic_sha256"] = sha256(canonical(carry_payload))
    return source, carry


def is_link_like(path: Path) -> bool:
    if not path.exists() and not path.is_symlink():
        return False
    if path.is_symlink():
        return True
    return os.name == "nt" and bool(path.lstat().st_file_attributes & 0x400)


def guard_outputs(disposition: Path, carry: Path) -> None:
    defaults = (Path(os.path.abspath(REPO / DISPOSITION)), Path(os.path.abspath(REPO / CARRY)))
    lexical = (Path(os.path.abspath(disposition)), Path(os.path.abspath(carry)))
    if lexical == defaults:
        for path in lexical:
            require(not path.exists() or not is_link_like(path), "E_OUTPUT_LINK")
            require(path.parent.resolve() == path.parent, "E_OUTPUT_PARENT_LINK")
        return
    temp_root = Path(tempfile.gettempdir()).resolve()
    require(lexical[0].parent == lexical[1].parent, "E_OUTPUT_PARENT")
    require(lexical[0].parent.parent == temp_root, "E_OUTPUT_TEMP_ROOT")
    require(lexical[0].parent.name == "p065-step75_1-fixtures", "E_OUTPUT_TEMP_NAME")
    require(not lexical[0].parent.exists() or not is_link_like(lexical[0].parent), "E_OUTPUT_PARENT_LINK")
    require(not lexical[0].parent.exists() or lexical[0].parent.resolve() == lexical[0].parent, "E_OUTPUT_PARENT_ESCAPE")
    require(lexical[0].name in {"source-disposition-one.json", "source-disposition-two.json"}, "E_OUTPUT_DISPOSITION_NAME")
    require(lexical[1].name in {"carry-forward-one.json", "carry-forward-two.json"}, "E_OUTPUT_CARRY_NAME")
    for path in lexical:
        require(not path.exists() or not is_link_like(path), "E_OUTPUT_LINK")


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disposition", type=Path, default=REPO / DISPOSITION)
    parser.add_argument("--carry", type=Path, default=REPO / CARRY)
    args = parser.parse_args()
    guard_outputs(args.disposition, args.carry)
    require((REPO / RESULT).exists(), "E_RESULT_FIRST_MISSING")
    inputs, metadata = load_inputs()
    disposition, carry = build(inputs, metadata)
    disposition_raw, carry_raw = canonical(disposition), canonical(carry)
    atomic_write(args.disposition, disposition_raw)
    atomic_write(args.carry, carry_raw)
    print(GATE, json.dumps({
        "occurrences": len(disposition["source_dispositions"]),
        "blobs": len(disposition["blob_disposition_groups"]),
        "observations": len(carry["observation_records"]),
        "active": len(carry["active_obligations"]),
        "disposition_sha256": sha256(disposition_raw),
        "carry_sha256": sha256(carry_raw),
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
