#!/usr/bin/env python3
"""Fail-closed validator for Phase 065 cumulative Step 75.1."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any


REPO = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "a04bca9c73941e1a4fbc0ab6e4f4e49514dcce12"
EXPECTED_SUBJECT = "audit(phase065): disposition v1024 lineage"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS"
PERSISTENCE_GATE = "PASS_P065_STEP75_1_PERSISTENCE"
EXPECTED_SOURCE_POLICY_HASHES = {
    "builder.module": "8adc29e2812cfd8e665799e67d3a69fcc8addc617ba2df6656ad410d55e42da6",
    "builder.atomic_write": "d504b9eb302421174691736419e0e5bc2c1c77b954a152c9d40a78df3930fd42",
    "builder.run_process": "15a74cdbe98b7f342b0ffa485c435c66e1d9e8562570a737215398a228564cd8",
    "builder.git": "ed00ee88c1016e38fc9004cbf5d72c2cc960ce5155e3b4627b9cff5770b1ec30",
    "builder.git_calls": "a03fee6d71dcf1c6dcc3e2825d9eeb72f66cd46f48b6b970a5563f119a3cc842",
    "validator.run_process": "15a74cdbe98b7f342b0ffa485c435c66e1d9e8562570a737215398a228564cd8",
    "validator.git": "7aea7590beb893c0eb1749e418f0df839828fb6d9e538d0303db9929f34dec2c",
    "validator.git_calls": "02c9e7a99f60b5c30eb7280c0f3919c1546094debc9cab07eebfd1ea57cadbbf",
}

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
EXACT_PATHS = sorted((*CONTROL_PATHS, DISPOSITION, CARRY))

ALLOWED_DISPOSITIONS = {"PRESERVE", "CORRECT", "THEORY_ONLY", "UNVERIFIED", "REJECTED_SOURCE", "DISCARD"}
UNVERIFIED_ROWS = {"D74-004", "D74-005", "D74-012", "D74-014", "D74-039", "D74-040", "D74-041"}
REJECTED_NORMAL_PATH = "Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex"
INHERITED_IDS = {
    "P059-CFR-CF-01": "PRESERVED_ACTIVE", "P059-CFR-CF-02": "PRESERVED_ACTIVE",
    "P059-CFR-CF-06": "PRESERVED_ACTIVE", "P059-CFR-CF-07": "PRESERVED_ACTIVE",
    "P059-CFR-RB-02": "OPEN_CARRY", "P059-CFR-RB-03": "OPEN_CARRY",
}
SOURCE_OWNER = {
    "PRESERVE": (90, "PHASE-090-RELEASE-PRESERVATION"),
    "CORRECT": (87, "PHASE-087-CANONICAL-SOURCE-SYNTHESIS"),
    "THEORY_ONLY": (82, "PHASE-082-CANONICAL-EQUATION-FREEZE"),
    "UNVERIFIED": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
    "REJECTED_SOURCE": (87, "PHASE-087-MANUSCRIPT-ASSEMBLY"),
    "DISCARD": (89, "PHASE-089-RELEASE-QA"),
}
P57_OWNERS = {
    "INTENT-PROV-0230": (74, "PHASE-074-FOUNDATION"), "INTENT-PROV-0266": (74, "PHASE-074-FOUNDATION"),
    "INTENT-PROV-0267": (75, "PHASE-075-EQUILIBRIUM-PHASE"), "INTENT-PROV-0284": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0285": (75, "PHASE-075-EQUILIBRIUM-PHASE"), "INTENT-PROV-0286": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0390": (89, "PHASE-089-RELEASE-QA"), "INTENT-PROV-0392": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0393": (75, "PHASE-075-EQUILIBRIUM-PHASE"), "INTENT-PROV-0395": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "INTENT-PROV-0397": (81, "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION"), "INTENT-PROV-0398": (81, "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION"),
    "INTENT-PROV-0399": (77, "PHASE-077-GRAPHITE-CLOSURE"), "INTENT-PROV-0400": (86, "PHASE-086-CALIBRATION-VALIDATION"),
    "INTENT-PROV-0401": (75, "PHASE-075-EQUILIBRIUM-PHASE"), "INTENT-PROV-0402": (82, "PHASE-082-CANONICAL-EQUATION-FREEZE"),
    "INTENT-PROV-0403": (88, "PHASE-088-SCIENTIFIC-REDTEAM"),
}
S71_OWNERS = {
    "P065-S71-F01": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"), "P065-S71-F02": (80, "PHASE-080-BLEND-CLOSURE"),
    "P065-S71-F03": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"), "P065-S71-F04": (74, "PHASE-074-FOUNDATION"),
    "P065-S71-F05": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"), "P065-S71-F06": (78, "PHASE-078-LCO-CLOSURE"),
    "P065-S71-F07": (85, "PHASE-085-STRUCTURE-FREEZE"), "P065-S71-F08": (77, "PHASE-077-GRAPHITE-CLOSURE"),
    "P065-S71-F09": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"), "P065-S71-F10": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"),
    "P065-S71-F11": (83, "PHASE-083-IMPLEMENTATION-CONTRACT"), "P065-S71-F12": (86, "PHASE-086-CALIBRATION-VALIDATION"),
    "P065-S71-F13": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
}
S72_OWNERS = {
    "P065-S72-F01": (66, "P066-LINEAGE"), "P065-S72-F02": (78, "PHASE-078-LCO-CLOSURE"),
    "P065-S72-F03": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"), "P065-S72-F04": (67, "P067-CODE-HISTORY"),
    "P065-S72-F05": (65, "P065-STEP75-DISPOSITION"), "P065-S72-F06": (71, "PHASE-071-PRIMARY-SOURCE-ACQUISITION"),
}
REF7_SUPERSEDED = {"P065-S70-F09", "P065-S70-F24", "P065-S71-F13", "P065-S72-F06"}
REF7_OWNER = "PHASE-071-PRIMARY-SOURCE-ACQUISITION"
REF7_ACCEPTANCE = "Superseded by the D74-006 Ref. 7 primary-source acquisition route; D74-006 alone carries the active proposition/page/equation acceptance criterion."
ADDITIONAL_REFINES = {"P065-S72-F06": ["P065-S71-F13"], "D74-006": ["P065-S72-F06"]}
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


class ValidationError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(f"{code}:{detail}" if detail else code)


def run_process(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, text: bool = True) -> str | bytes:
    proc = run_process(["git", *args])
    require(proc.returncode == 0, "E_GIT", f"{' '.join(args)}:{proc.stderr.decode('utf-8', errors='replace')}")
    return proc.stdout.decode("utf-8") if text else proc.stdout


def blob(revision: str, path: str) -> bytes:
    raw = git("show", revision_spec(revision, path), text=False)
    assert isinstance(raw, bytes)
    return raw


def revision_spec(revision: str, path: str) -> str:
    return f":{path}" if revision == ":" else f"{revision}:{path}"


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
            require(key not in out, "E_DUPLICATE_KEY", key)
            out[key] = value
        return out

    def constant(value: str) -> None:
        raise ValidationError(f"E_NONFINITE:{value}")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except UnicodeDecodeError as exc:
        raise ValidationError(f"E_UTF8:{exc}") from exc
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


def pointer(value: Any, route: str) -> Any:
    current = value
    for token in route.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def exact_keys(value: dict[str, Any], keys: set[str], code: str) -> None:
    require(set(value) == keys, code, repr(sorted(set(value) ^ keys)))


def fingerprint(text: str) -> str:
    normalized = " ".join(re.findall(r"[a-z0-9가-힣]+", text.lower()))
    return sha256(normalized.encode("utf-8"))


def phase_from_owner(owner: str, fallback: int = 65) -> int:
    match = re.search(r"(?:PHASE-|P)(\d{3})", owner)
    return int(match.group(1)) if match else fallback


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
    active_rows = [row for row in rows if row["status"] == "OPEN_ROUTED" and row["row_id"] != "D74-007"]
    governing = active_rows or rows
    owners = {row["owner"] for row in governing}
    require(len(owners) == 1, "E_EXPECTED_SUPERSESSION_OWNER", origin_id)
    owner = next(iter(owners))
    row_ids = sorted(row["row_id"] for row in rows)
    acceptance = f"Superseded by Step 74 rows {row_ids}; their exact row-level acceptance criteria govern and this origin is not counted as a second active obligation."
    return owner, phase_from_owner(owner), acceptance


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


def load_inputs() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    objects: dict[str, Any] = {}
    metadata: dict[str, dict[str, Any]] = {}
    for path in INPUT_PATHS:
        raw = blob(EXPECTED_PARENT, path)
        obj = strict_load(raw)
        nodes, depth = traverse(obj)
        objects[path] = obj
        metadata[path] = {
            "path": path,
            "revision": EXPECTED_PARENT,
            "git_blob": str(git("rev-parse", f"{EXPECTED_PARENT}:{path}")).strip(),
            "sha256": sha256(raw), "size_bytes": len(raw), "nodes": nodes,
            "depth": depth, "read_status": "MACHINE_FULL_TRAVERSAL",
        }
    return objects, metadata


def validate_common(obj: dict[str, Any], kind: str, schema: str) -> None:
    require(obj["schema_version"] == schema, "E_SCHEMA")
    require(obj["artifact_kind"] == kind, "E_KIND")
    require(obj["phase"] == 65 and obj["step"] == "75.1", "E_STEP")
    require(obj["baseline_commit"] == BASELINE, "E_BASELINE")
    require(obj["expected_parent"] == EXPECTED_PARENT, "E_PARENT")
    require(obj["branch"] == BRANCH, "E_BRANCH")
    require(obj["expected_subject"] == EXPECTED_SUBJECT, "E_SUBJECT")
    require(obj["gate"] == GATE, "E_GATE")
    require(obj["authority"] == AUTHORITY, "E_AUTHORITY")
    payload = copy.deepcopy(obj)
    semantic = payload.pop("semantic_sha256")
    require(semantic == sha256(canonical(payload)), "E_SEMANTIC_SHA")


def validate_inputs(obj: dict[str, Any], expected: dict[str, dict[str, Any]]) -> None:
    for row in obj["inputs"]:
        exact_keys(row, {"path", "revision", "git_blob", "sha256", "size_bytes", "nodes", "depth", "read_status"}, "E_INPUT_SCHEMA")
    require([row["path"] for row in obj["inputs"]] == list(INPUT_PATHS), "E_INPUT_ORDER")
    require({row["path"]: row for row in obj["inputs"]} == expected, "E_INPUT_BINDINGS")


def normalized_path(path: str) -> str:
    return path.replace("/v1.0.24.1/", "/v1.0.24/")


def conformance_links(conformance: dict[str, Any]) -> tuple[dict[str, set[str]], dict[str, dict[str, Any]]]:
    links: dict[str, set[str]] = {}
    rows = {row["row_id"]: row for row in conformance["conformance_rows"]}
    for row in conformance["conformance_rows"]:
        for surface in row["claim_surface"]:
            if surface["path"].startswith("Claude/"):
                links.setdefault(normalized_path(surface["path"]), set()).add(row["row_id"])
    return links, rows


def expected_disposition(role: str, path: str, row_ids: set[str], row_map: dict[str, dict[str, Any]]) -> str:
    if path == REJECTED_NORMAL_PATH:
        return "REJECTED_SOURCE"
    if row_ids & UNVERIFIED_ROWS:
        return "UNVERIFIED"
    if any(row_map[row_id]["status"] == "OPEN_ROUTED" for row_id in row_ids):
        return "CORRECT"
    return "THEORY_ONLY" if role == "theory" else "PRESERVE"


def expected_source_acceptance(disposition: str, target: int) -> str:
    actions = {
        "PRESERVE": "preserve the exact historical identity and authority ceiling",
        "CORRECT": "retain only corrected propositions and repair every linked conformance route without rewriting frozen source",
        "THEORY_ONLY": "preserve the derivation only within its stated assumptions and with no material-truth promotion",
        "UNVERIFIED": "obtain primary/material/held-out authority or keep the proposition explicitly unverified",
        "REJECTED_SOURCE": "preserve the non-graft decision and exclude this candidate from canonical assembly",
        "DISCARD": "exclude the artifact from release while retaining this audit identity",
    }
    return f"Phase {target:03d} must {actions[disposition]}."


def validate_source(obj: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, dict[str, Any]]) -> tuple[int, int]:
    exact_keys(obj, {
        "schema_version", "artifact_kind", "phase", "step", "baseline_commit", "expected_parent",
        "branch", "expected_subject", "gate", "inputs", "control_source_bindings", "authority",
        "source_contract", "source_dispositions", "blob_disposition_groups", "counts", "semantic_sha256",
    }, "E_SOURCE_TOP_SCHEMA")
    validate_common(obj, "PHASE_065_SOURCE_DISPOSITION_MATRIX", "P065_STEP75_1_SOURCE_DISPOSITION_V1")
    validate_inputs(obj, metadata)
    require(set(obj["source_contract"]["allowed_dispositions"]) == ALLOWED_DISPOSITIONS, "E_ENUM")
    require(obj["source_contract"] == {
        "occurrences": 261, "unique_blobs": 131, "mirror_pairs": 130,
        "archive_only_occurrences": 1, "allowed_dispositions": sorted(ALLOWED_DISPOSITIONS),
        "identity_rule": "ONE_ROW_PER_OCCURRENCE; ONE_CONSISTENT_DISPOSITION_PER_BLOB; MIRROR_IS_NOT_CORROBORATION",
    }, "E_SOURCE_CONTRACT")
    topology = inputs[TOPOLOGY]
    occurrences = topology["occurrences"]
    unique = topology["unique_sources"]
    require(len(occurrences) == 261 and len(unique) == 131, "E_TOPOLOGY_DENOMINATOR")
    require(sum(row["version"] == "v1.0.24" for row in occurrences) == 130, "E_V1024_COUNT")
    require(sum(row["version"] == "v1.0.24.1" for row in occurrences) == 131, "E_V1024_1_COUNT")
    archive = [row for row in occurrences if row["mirror_counterpart"] is None]
    require(len(archive) == 1 and archive[0]["path"] == "Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md", "E_ARCHIVE_ONLY")
    links, row_map = conformance_links(inputs[CONFORMANCE])
    rows = obj["source_dispositions"]
    groups = obj["blob_disposition_groups"]
    require(len(rows) == 261 and len(groups) == 131, "E_SOURCE_ROWS")
    by_blob: dict[str, list[dict[str, Any]]] = {}
    distribution: dict[str, int] = {}
    for index, (row, origin) in enumerate(zip(rows, occurrences, strict=True)):
        exact_keys(row, {
            "disposition_id", "source_path", "blob", "occurrence_identity", "dedup_group", "role",
            "read_status", "read_ranges", "disposition", "status", "reason", "evidence_routes",
            "open_routes", "canonical_owner", "acceptance_criterion", "target_phase", "external_authority_promoted",
        }, "E_SOURCE_ROW_SCHEMA")
        require(row["disposition_id"] == f"P065-DISP-{index + 1:04d}", "E_DISPOSITION_ID")
        require(row["source_path"] == origin["path"] and row["blob"] == origin["blob"], "E_SOURCE_IDENTITY")
        require(row["occurrence_identity"] == origin, "E_OCCURRENCE_IDENTITY")
        require(row["dedup_group"] == origin["dedup_group"] and row["role"] == origin["role"], "E_SOURCE_ROLE")
        require(row["read_status"] == origin["read_status"] and row["read_ranges"] == origin["read_ranges"], "E_READ_CARRY")
        normalized = normalized_path(origin["path"])
        row_ids = links.get(normalized, set())
        expected = expected_disposition(origin["role"], normalized, row_ids, row_map)
        require(row["disposition"] == expected and expected in ALLOWED_DISPOSITIONS, "E_DISPOSITION", row["disposition_id"])
        target, owner = SOURCE_OWNER[expected]
        require(row["canonical_owner"] == owner and row["target_phase"] == target, "E_SOURCE_OWNER")
        require(row["status"] == {
            "PRESERVE": "BOUNDED_PRESERVE", "CORRECT": "OPEN_CORRECTION",
            "THEORY_ONLY": "BOUNDED_THEORY_ONLY", "UNVERIFIED": "OPEN_UNVERIFIED",
            "REJECTED_SOURCE": "CLOSED_REJECTED_SOURCE", "DISCARD": "CLOSED_DISCARD",
        }[expected], "E_SOURCE_STATUS", row["disposition_id"])
        row_ids_sorted = sorted(row_ids)
        require(row["reason"] == f"Exact occurrence is classified from its frozen role, 131-blob dedup identity, and linked Step 74 rows {row_ids_sorted}; v1.0.24.1 mirror membership does not add authority.", "E_SOURCE_REASON", row["disposition_id"])
        require(row["acceptance_criterion"] == expected_source_acceptance(expected, target), "E_SOURCE_ACCEPTANCE", row["disposition_id"])
        require(row["external_authority_promoted"] is False, "E_SOURCE_AUTHORITY")
        require(row["open_routes"] == sorted(r for r in row_ids_sorted if row_map[r]["status"] == "OPEN_ROUTED" and r != "D74-007"), "E_OPEN_ROUTES")
        conformance = inputs[CONFORMANCE]["conformance_rows"]
        expected_evidence = [{
            "artifact_path": TOPOLOGY, "json_pointer": f"/occurrences/{index}",
            "record_sha256": record_sha(origin), "role": "OCCURRENCE_IDENTITY",
        }]
        for row_id in sorted(row_ids):
            conformance_index = next(i for i, item in enumerate(conformance) if item["row_id"] == row_id)
            expected_evidence.append({
                "artifact_path": CONFORMANCE, "json_pointer": f"/conformance_rows/{conformance_index}",
                "record_sha256": record_sha(conformance[conformance_index]), "role": "CONFORMANCE_ROUTE",
            })
        for evidence in row["evidence_routes"]:
            exact_keys(evidence, {"artifact_path", "json_pointer", "record_sha256", "role"}, "E_SOURCE_EVIDENCE_SCHEMA")
        require(row["evidence_routes"] == expected_evidence, "E_SOURCE_EVIDENCE", row["disposition_id"])
        by_blob.setdefault(row["blob"], []).append(row)
        distribution[expected] = distribution.get(expected, 0) + 1
    require(distribution == {"CORRECT": 41, "PRESERVE": 114, "REJECTED_SOURCE": 2, "THEORY_ONLY": 96, "UNVERIFIED": 8}, "E_DISTRIBUTION", repr(distribution))
    group_map = {row["blob"]: row for row in groups}
    require(len(group_map) == 131 and set(group_map) == set(by_blob), "E_GROUP_MEMBERSHIP")
    unique_index = {row["blob"]: index for index, row in enumerate(unique)}
    for blob_id, members in by_blob.items():
        dispositions = {row["disposition"] for row in members}
        require(len(dispositions) == 1, "E_BLOB_CONTRADICTION", blob_id)
        group = group_map[blob_id]
        exact_keys(group, {"blob", "dedup_group", "occurrence_ids", "paths", "disposition", "linked_conformance_rows", "unique_source_pointer", "unique_source_record_sha256"}, "E_GROUP_SCHEMA")
        require(group["blob"] == blob_id, "E_GROUP_BLOB")
        require(group["dedup_group"] == members[0]["dedup_group"], "E_GROUP_DEDUP")
        require(group["disposition"] == next(iter(dispositions)), "E_GROUP_DISPOSITION")
        require(group["occurrence_ids"] == [row["occurrence_identity"]["ordinal"] for row in members], "E_GROUP_OCCURRENCES")
        require(group["paths"] == [row["source_path"] for row in members], "E_GROUP_PATHS")
        expected_links = sorted(set().union(*(links.get(normalized_path(row["source_path"]), set()) for row in members)))
        require(group["linked_conformance_rows"] == expected_links, "E_GROUP_LINKS", blob_id)
        ui = unique_index[blob_id]
        require(group["unique_source_pointer"] == f"/unique_sources/{ui}", "E_GROUP_POINTER")
        require(group["unique_source_record_sha256"] == record_sha(unique[ui]), "E_GROUP_SHA")
    counts = obj["counts"]
    exact_keys(counts, {"source_dispositions", "blob_groups", "distribution", "open_source_dispositions", "contradictory_blob_dispositions", "ownerless_sources", "external_authority_promotions"}, "E_SOURCE_COUNTS_SCHEMA")
    require(counts["source_dispositions"] == 261 and counts["blob_groups"] == 131, "E_SOURCE_COUNTS")
    require(counts["distribution"] == distribution, "E_SOURCE_DISTRIBUTION_COUNT")
    require(counts["open_source_dispositions"] == 49, "E_OPEN_SOURCE_COUNT")
    require(counts["contradictory_blob_dispositions"] == counts["ownerless_sources"] == counts["external_authority_promotions"] == 0, "E_SOURCE_ZERO")
    return traverse(obj)


def validate_carry(obj: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, dict[str, Any]]) -> tuple[int, int]:
    exact_keys(obj, {
        "schema_version", "artifact_kind", "phase", "step", "baseline_commit", "expected_parent",
        "branch", "expected_subject", "gate", "inputs", "control_source_bindings", "authority",
        "observation_records", "active_obligations", "inherited_phase064_routes",
        "prior_phase064_owner_universe_snapshot", "current_owner_duplicate_check_universe",
        "semantic_duplicate_groups", "new_phase065_blockers", "gate_summary", "semantic_sha256",
    }, "E_CARRY_TOP_SCHEMA")
    validate_common(obj, "PHASE_065_CARRY_FORWARD_DELTA", "P065_STEP75_1_CARRY_FORWARD_V1")
    validate_inputs(obj, metadata)
    observations = obj["observation_records"]
    active = obj["active_obligations"]
    require(len(observations) == 192 and len(active) == 94, "E_CARRY_DENOMINATOR")
    by_id = {row["observation_id"]: row for row in observations}
    require(len(by_id) == 192, "E_OBSERVATION_DUPLICATE")
    expected_partition = {"Phase 057": (82, 17), "Step 70": (44, 24), "Step 71": (13, 10), "Step 72": (6, 3), "Step 74": (41, 34), "Phase 064 inherited": (6, 6)}
    for origin_step, (total, active_count) in expected_partition.items():
        members = [row for row in observations if row["origin_step"] == origin_step]
        require(len(members) == total, "E_PARTITION_TOTAL", origin_step)
        require(sum(row["state"] in {"OPEN_CARRY", "PRESERVED_ACTIVE"} for row in members) == active_count, "E_PARTITION_ACTIVE", origin_step)

    successors = step74_successors(inputs[CONFORMANCE])
    require(set(successors) == {
        "P065-S70-F06", "P065-S70-F08", "P065-S70-F10", "P065-S70-F11", "P065-S70-F14",
        "P065-S70-F34", "P065-S70-F35", "P065-S70-F36", "P065-S70-F39", "P065-S70-F41",
        "P065-S70-F42", "P065-S70-F43", "P065-S70-F44", "P065-S71-F01", "P065-S71-F06",
        "P065-S72-F02", "P065-S72-F05",
    }, "E_SUPERSESSION_ROUTE_SET")
    contracts: dict[str, dict[str, Any]] = {}

    def contract(identity: str, **values: Any) -> None:
        require(identity not in contracts, "E_EXPECTED_CONTRACT_DUPLICATE", identity)
        contracts[identity] = values

    for index, record in enumerate(inputs[TOPOLOGY]["phase057_observations"]["records"]):
        is_open = record["open_in_v1024_mirror"]
        if is_open:
            target, owner = P57_OWNERS[record["id"]]
            state = "OPEN_CARRY"
            acceptance = f"{owner} must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24."
        else:
            target, owner, state = 65, "P065-STEP75-DISPOSITION", "BOUNDED_HISTORICAL"
            acceptance = "Preserve the exact Phase 057 observation as bounded history; it creates no active owner obligation."
        contract(record["id"], origin_step="Phase 057", origin_path=TOPOLOGY, origin_pointer=f"/phase057_observations/records/{index}", claim=record["title"], state=state, severity="P1" if is_open else "NONE", inherited_owner=None, canonical_owner=owner, target_phase=target, acceptance_criterion=acceptance, refines=[])

    for index, record in enumerate(inputs[TOPOLOGY]["findings"]):
        owner = record.get("owner") or "P065-STEP75-DISPOSITION"
        target = phase_from_owner(owner)
        state = "OPEN_CARRY" if record["status"] == "OPEN_ROUTED" else "CLOSED_OR_BOUND"
        acceptance = f"{owner} must satisfy the exact Step 70 finding or preserve its confirmed/corrected/bound state without authority promotion."
        supersession = supersession_contract(record["id"], successors)
        if supersession is not None:
            owner, target, acceptance = supersession
            state = "SUPERSEDED_BY_STEP74"
        if record["id"] in REF7_SUPERSEDED:
            owner, target, acceptance, state = REF7_OWNER, 71, REF7_ACCEPTANCE, "SUPERSEDED_BY_STEP74"
        contract(record["id"], origin_step="Step 70", origin_path=TOPOLOGY, origin_pointer=f"/findings/{index}", claim=record.get("finding", record.get("summary", "")), state=state, severity=record.get("severity", "NONE"), inherited_owner=record.get("owner"), canonical_owner=owner, target_phase=target, acceptance_criterion=acceptance, refines=[])

    for index, record in enumerate(inputs[CODE]["findings"]):
        identity = record["finding_id"]
        target, owner = S71_OWNERS[identity]
        state = "OPEN_CARRY"
        acceptance = f"{owner} must close the static finding using the Step 73 bounded runtime evidence where applicable."
        supersession = supersession_contract(identity, successors)
        if supersession is not None:
            owner, target, acceptance = supersession
            state = "SUPERSEDED_BY_STEP74"
        if identity in REF7_SUPERSEDED:
            owner, target, acceptance, state = REF7_OWNER, 71, REF7_ACCEPTANCE, "SUPERSEDED_BY_STEP74"
        inherited_owner = "P065-STEP73-RUNTIME" if identity not in {"P065-S71-F12", "P065-S71-F13"} else None
        contract(identity, origin_step="Step 71", origin_path=CODE, origin_pointer=f"/findings/{index}", claim=record["title"], state=state, severity=record["severity"], inherited_owner=inherited_owner, canonical_owner=owner, target_phase=target, acceptance_criterion=acceptance, refines=sorted(record["step70_routes"]))

    for index, record in enumerate(inputs[SCIENCE]["findings"]):
        identity = f"P065-{record['id']}"
        target, owner = S72_OWNERS[identity]
        closed = record["id"] == "S72-F05"
        state = "CLOSED_REJECTED_SOURCE" if closed else "OPEN_CARRY"
        acceptance = "Preserve the explicit non-graft decision." if closed else f"{owner} must satisfy the bounded scientific-authority finding without promoting missing external evidence."
        supersession = supersession_contract(identity, successors)
        if supersession is not None:
            owner, target, acceptance = supersession
            state = "SUPERSEDED_BY_STEP74"
        if identity in REF7_SUPERSEDED:
            owner, target, acceptance, state = REF7_OWNER, 71, REF7_ACCEPTANCE, "SUPERSEDED_BY_STEP74"
        contract(identity, origin_step="Step 72", origin_path=SCIENCE, origin_pointer=f"/findings/{index}", claim=record["finding"], state=state, severity=record["severity"], inherited_owner=record["owner"], canonical_owner=owner, target_phase=target, acceptance_criterion=acceptance, refines=sorted(ADDITIONAL_REFINES.get(identity, [])))

    for index, record in enumerate(inputs[CONFORMANCE]["conformance_rows"]):
        identity = record["row_id"]
        state = "OPEN_CARRY" if record["status"] == "OPEN_ROUTED" and identity != "D74-007" else "CLOSED_SUPERSEDED_IN_STEP75_1" if identity == "D74-007" else record["status"]
        refines = sorted(set(record["origin_routes"] + ADDITIONAL_REFINES.get(identity, [])))
        contract(identity, origin_step="Step 74", origin_path=CONFORMANCE, origin_pointer=f"/conformance_rows/{index}", claim=record["claim"], state=state, severity=record["severity"], inherited_owner=record["owner"], canonical_owner=record["owner"], target_phase=phase_from_owner(record["owner"]), acceptance_criterion=record["acceptance_criterion"], refines=refines)

    for identity, state in INHERITED_IDS.items():
        found = deepest_carry_record(inputs[P64_CARRY], identity)
        require(found is not None, "E_INHERITED_GROUND_NOT_FOUND", identity)
        origin_pointer, origin_record = found
        contract(identity, origin_step="Phase 064 inherited", origin_path=P64_CARRY, origin_pointer=origin_pointer, claim=origin_record["acceptance_criterion"], state=state, severity="P1" if state == "OPEN_CARRY" else "NONE", inherited_owner=identity, canonical_owner=identity, target_phase=65, acceptance_criterion=origin_record["acceptance_criterion"], refines=[])

    require(set(contracts) == set(by_id), "E_CONTRACT_UNIVERSE")
    expected_refined_by: dict[str, list[str]] = {identity: [] for identity in contracts}
    for identity, expected in contracts.items():
        for refined in expected["refines"]:
            require(refined in expected_refined_by, "E_DANGLING_REFINES", f"{identity}:{refined}")
            expected_refined_by[refined].append(identity)
    for row in observations:
        exact_keys(row, {
            "observation_id", "origin_step", "origin_path", "origin_pointer", "origin_record_sha256",
            "origin_record", "claim", "state", "severity", "inherited_owner", "canonical_owner",
            "target_phase", "acceptance_criterion", "semantic_fingerprint", "refines", "refined_by",
            "external_authority_promoted",
        }, "E_OBSERVATION_SCHEMA")
        expected = contracts[row["observation_id"]]
        for key, value in expected.items():
            require(row[key] == value, "E_OBSERVATION_CONTRACT", f"{row['observation_id']}:{key}")
        require(row["refined_by"] == sorted(set(expected_refined_by[row["observation_id"]])), "E_REFINED_BY", row["observation_id"])
        require(row["semantic_fingerprint"] == fingerprint(row["claim"]), "E_FINGERPRINT", row["observation_id"])
        require(isinstance(row["canonical_owner"], str) and bool(row["canonical_owner"]), "E_OWNERLESS", row["observation_id"])
        require(isinstance(row["acceptance_criterion"], str) and bool(row["acceptance_criterion"]), "E_ACCEPTANCE", row["observation_id"])
        require(row["external_authority_promoted"] is False, "E_OBSERVATION_AUTHORITY")
        origin = pointer(inputs[row["origin_path"]], row["origin_pointer"])
        require(row["origin_record"] == origin and row["origin_record_sha256"] == record_sha(origin), "E_ORIGIN_RECORD", row["observation_id"])
    require(sum(row["state"] == "SUPERSEDED_BY_STEP74" for row in observations) == 21, "E_SUPERSEDED_COUNT")
    d74 = by_id["D74-007"]
    require(d74["state"] == "CLOSED_SUPERSEDED_IN_STEP75_1", "E_D74_007_STATE")
    require("default-false" in d74["claim"] or "default" in d74["claim"].lower(), "E_D74_007_CLAIM")
    inherited = obj["inherited_phase064_routes"]
    require({row["observation_id"]: row["state"] for row in inherited} == INHERITED_IDS, "E_INHERITED_SET")
    for row in inherited:
        require(row == by_id[row["observation_id"]], "E_INHERITED_RECORD_COPY")
        require(row["canonical_owner"] == row["observation_id"] == row["inherited_owner"], "E_INHERITED_OWNER")
        require(row["target_phase"] == 65, "E_INHERITED_TARGET")
    expected_active = [row for row in observations if row["state"] in {"OPEN_CARRY", "PRESERVED_ACTIVE"}]
    for index, (obligation, origin) in enumerate(zip(active, expected_active, strict=True)):
        exact_keys(obligation, {"obligation_id", "origin_identity", "state", "canonical_owner", "target_phase", "acceptance_criterion", "semantic_fingerprint", "relation_links", "external_authority_promoted"}, "E_OBLIGATION_SCHEMA")
        require(obligation["obligation_id"] == f"P065-OBL-{index + 1:04d}", "E_OBLIGATION_ID")
        require(obligation["origin_identity"] == origin["observation_id"], "E_OBLIGATION_ORIGIN")
        require(obligation["canonical_owner"] == origin["canonical_owner"] and obligation["target_phase"] == origin["target_phase"], "E_OBLIGATION_OWNER")
        require(obligation["state"] == origin["state"] and obligation["semantic_fingerprint"] == origin["semantic_fingerprint"], "E_OBLIGATION_STATE_FINGERPRINT")
        require(obligation["acceptance_criterion"] == origin["acceptance_criterion"], "E_OBLIGATION_ACCEPTANCE")
        require(obligation["relation_links"] == sorted(set(origin["refines"] + origin["refined_by"])), "E_RELATION_LINK")
        require(obligation["external_authority_promoted"] is False, "E_OBLIGATION_AUTHORITY")
    duplicates = obj["semantic_duplicate_groups"]
    fingerprints: dict[str, list[str]] = {}
    for row in observations:
        fingerprints.setdefault(row["semantic_fingerprint"], []).append(row["observation_id"])
    expected_duplicate_members = sorted(sorted(members) for members in fingerprints.values() if len(members) > 1)
    require(expected_duplicate_members == [["D74-028", "P065-S70-F44"]], "E_RECOMPUTED_SEMANTIC_DUPLICATES", repr(expected_duplicate_members))
    require(len(duplicates) == 2, "E_SEMANTIC_DUPLICATE_COUNT")
    for duplicate in duplicates:
        exact_keys(duplicate, {"group_id", "match_type", "fingerprint", "members", "canonical_member", "canonical_owner", "target_phase", "status"}, "E_SEMANTIC_DUPLICATE_SCHEMA")
    duplicate_map = {row["group_id"]: row for row in duplicates}
    require(set(duplicate_map) == {"P065-SEM-001", "P065-SEM-002"}, "E_SEMANTIC_GROUP_IDS")
    duplicate = duplicate_map["P065-SEM-001"]
    require(duplicate["match_type"] == "EXACT_NORMALIZED_TEXT" and duplicate["members"] == ["D74-028", "P065-S70-F44"], "E_SEMANTIC_DUPLICATE_MEMBERS")
    require(duplicate["fingerprint"] == by_id["D74-028"]["semantic_fingerprint"] == by_id["P065-S70-F44"]["semantic_fingerprint"], "E_SEMANTIC_DUPLICATE_FINGERPRINT")
    require(duplicate["canonical_member"] == "D74-028" and duplicate["canonical_owner"] == "PHASE-089-RELEASE-QA" and duplicate["target_phase"] == 89, "E_SEMANTIC_DUPLICATE_OWNER")
    require(duplicate["status"] == "RESOLVED_BY_STEP74_REFINEMENT", "E_SEMANTIC_DUPLICATE_STATUS")
    ref7 = duplicate_map["P065-SEM-002"]
    require(ref7["match_type"] == "SEMANTIC_PRIMARY_SOURCE_AUTHORITY_CHAIN", "E_REF7_GROUP_TYPE")
    require(ref7["fingerprint"] == sha256(b"REF7_PRIMARY_SOURCE_PROPOSITION_AUTHORITY"), "E_REF7_GROUP_FINGERPRINT")
    require(ref7["members"] == sorted(["P065-S70-F09", "P065-S70-F24", "P065-S71-F13", "P065-S72-F06", "D74-006"]), "E_REF7_GROUP_MEMBERS")
    require(ref7["canonical_member"] == "D74-006" and ref7["canonical_owner"] == REF7_OWNER and ref7["target_phase"] == 71, "E_REF7_GROUP_OWNER")
    require(all(by_id[identity]["canonical_owner"] == REF7_OWNER for identity in ref7["members"]), "E_REF7_MEMBER_OWNER")
    require(by_id["P065-S71-F13"]["refines"] == ["P065-S70-F09", "P065-S70-F24"] and by_id["P065-S72-F06"]["refines"] == ["P065-S71-F13"] and "P065-S72-F06" in by_id["D74-006"]["refines"], "E_REF7_RELATION_CHAIN")
    require(by_id["P065-S70-F44"]["canonical_owner"] == by_id["D74-028"]["canonical_owner"] == "PHASE-089-RELEASE-QA", "E_DUPLICATE_MULTIPLE_OWNER")
    require("P065-S70-F44" in by_id["D74-028"]["refines"] and "D74-028" in by_id["P065-S70-F44"]["refined_by"], "E_DUPLICATE_RELATION")
    prior = inputs[P64_CARRY]["canonical_owner_duplicate_check_universe"]
    snapshot = obj["prior_phase064_owner_universe_snapshot"]
    exact_keys(snapshot, {"origin_path", "record_count", "records_sha256", "artifact_sha256", "status"}, "E_PRIOR_OWNER_SCHEMA")
    require(snapshot["record_count"] == prior["record_count"] and snapshot["records_sha256"] == prior["records_sha256"], "E_PRIOR_OWNER_SNAPSHOT")
    require(snapshot["origin_path"] == P64_CARRY and snapshot["artifact_sha256"] == metadata[P64_CARRY]["sha256"] and snapshot["status"] == "PRESERVED_BY_REFERENCE_NOT_REACTIVATED_WHOLESALE", "E_PRIOR_OWNER_BINDING")
    current = obj["current_owner_duplicate_check_universe"]
    exact_keys(current, {"record_count", "records_sha256", "records"}, "E_CURRENT_OWNER_SCHEMA")
    require(current["record_count"] == 192 and len(current["records"]) == 192, "E_CURRENT_OWNER_UNIVERSE")
    require(current["records_sha256"] == record_sha(current["records"]), "E_OWNER_UNIVERSE_SHA")
    expected_owner_records = []
    for index, row in enumerate(observations):
        expected_owner_records.append({
            "registry_id": f"P065-OWNER-{index + 1:04d}", "origin_identity": row["observation_id"],
            "owner_id": row["canonical_owner"], "target_phase": row["target_phase"], "state": row["state"],
            "origin_record_sha256": row["origin_record_sha256"],
        })
    for row in current["records"]:
        exact_keys(row, {"registry_id", "origin_identity", "owner_id", "target_phase", "state", "origin_record_sha256"}, "E_OWNER_RECORD_SCHEMA")
    require(current["records"] == expected_owner_records, "E_OWNER_RECORDS")
    require(obj["new_phase065_blockers"] == [], "E_NEW_BLOCKER")
    summary = obj["gate_summary"]
    expected_summary = {
        "source_occurrences": 261, "unique_blobs": 131,
        "phase057_records": 82, "phase057_open": 17,
        "step70_findings": 44, "step70_open": 39,
        "step71_findings": 13, "step71_open": 13,
        "step72_findings": 6, "step72_open": 5,
        "step74_rows": 41, "step74_open_input": 35, "step74_open_after_disposition": 34,
        "inherited_phase064_routes": 6, "step74_origin_routes_superseded": 17,
        "semantic_chain_superseded": 4, "active_obligations": 94,
        "ownerless_active_obligations": 0, "multiply_owned_active_obligations": 0,
        "semantic_duplicate_groups": 2, "unresolved_semantic_duplicates": 0,
        "new_phase065_blockers": 0, "external_authority_promotions": 0,
        "phase_ceiling": "CONDITIONAL_P065", "status": "PASS_WITH_CONCERNS",
    }
    require(summary == expected_summary, "E_GATE_SUMMARY")
    return traverse(obj)


def verify_controls(obj: dict[str, Any], revision: str) -> None:
    expected = []
    require(len(obj["control_source_bindings"]) == len(CONTROL_PATHS), "E_CONTROL_COUNT")
    for row in obj["control_source_bindings"]:
        exact_keys(row, {"path", "git_blob", "sha256", "size_bytes"}, "E_CONTROL_SCHEMA")
    for path in CONTROL_PATHS:
        raw = blob(revision, path)
        expected.append({
            "path": path, "git_blob": str(git("rev-parse", revision_spec(revision, path))).strip(),
            "sha256": sha256(raw), "size_bytes": len(raw),
        })
    require(obj["control_source_bindings"] == expected, "E_CONTROL_BINDINGS")


def verify_docs() -> None:
    result = (REPO / RESULT).read_text(encoding="utf-8")
    require("Step 75.1" in result and GATE in result and PERSISTENCE_GATE in result, "E_RESULT_GATE")
    require("implementation-specific" in result and "계획서에 이미 존재하던 이름이라고 주장하지 않는다" in result, "E_GATE_PROVENANCE")
    require("261" in result and "131" in result and "192" in result and "94" in result, "E_RESULT_COUNTS")
    require("P059-CFR-RB-03" in result and "D74-007" in result and "P065-S70-F44" in result, "E_RESULT_ROUTES")
    for path in (PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER):
        text = (REPO / path).read_text(encoding="utf-8")
        require("Step 75.1" in text and GATE in text and EXPECTED_SUBJECT in text, "E_RECORD_CURRENT", path)
        require("a04bca9c73941e1a4fbc0ab6e4f4e49514dcce12" in text and "PASS_P065_STEP74_PERSISTENCE" in text, "E_STEP74_RECOVERY", path)


def source_policy_errors(source: str, role: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"E_AST_PARSE:{exc}"]
    parents: dict[ast.AST, ast.AST] = {}
    owners: dict[ast.AST, str] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    for node in ast.walk(tree):
        cursor: ast.AST | None = node
        owner = "<module>"
        while cursor is not None:
            if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                owner = cursor.name
                break
            cursor = parents.get(cursor)
        owners[node] = owner
    subprocess_runs = []
    run_process_calls = []
    replace_inventory: list[tuple[str, str]] = []
    allowed_git = {"builder": {"show", "rev-parse"}, "validator": {"show", "rev-parse", "branch", "ls-remote", "diff", "diff-tree", "status"}}[role]
    expected_imports = {
        "builder": ["argparse", "copy", "hashlib", "json", "math", "os", "re", "subprocess", "tempfile"],
        "validator": ["argparse", "ast", "copy", "hashlib", "json", "math", "os", "re", "subprocess", "sys", "tempfile"],
    }[role]
    expected_from_imports = [("__future__", ("annotations",)), ("pathlib", ("Path",)), ("typing", ("Any",))]
    import_inventory: list[str] = []
    from_import_inventory: list[tuple[str, tuple[str, ...]]] = []
    annotation_nodes: set[ast.AST] = set()
    for item in ast.walk(tree):
        annotations: list[ast.AST] = []
        if isinstance(item, ast.arg) and item.annotation is not None:
            annotations.append(item.annotation)
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.returns is not None:
            annotations.append(item.returns)
        elif isinstance(item, ast.AnnAssign) and item.annotation is not None:
            annotations.append(item.annotation)
        for annotation in annotations:
            annotation_nodes.update(ast.walk(annotation))
    protected_names = {"subprocess", "os", "Path", "run_process", "git"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_inventory.append(alias.name)
                if alias.asname is not None:
                    errors.append(f"E_IMPORT:{alias.name}:{alias.asname}")
        elif isinstance(node, ast.ImportFrom):
            from_import_inventory.append((node.module or "", tuple(alias.name for alias in node.names)))
            if node.level != 0:
                errors.append(f"E_IMPORT_FROM_LEVEL:{node.module}")
            if any(alias.name == "*" or alias.asname is not None for alias in node.names):
                errors.append(f"E_IMPORT_ALIAS:{node.module}")
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            targets: list[ast.AST] = []
            if isinstance(node, ast.Assign): targets = list(node.targets)
            elif isinstance(node, ast.AnnAssign): targets = [node.target]
            elif isinstance(node, ast.AugAssign): targets = [node.target]
            else: targets = [node.target]
            for target in targets:
                for child in ast.walk(target):
                    if isinstance(child, ast.Name) and child.id in protected_names:
                        errors.append(f"E_PROTECTED_REBIND:{child.id}:{owners[node]}")
                    if isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name) and child.value.id in {"subprocess", "os", "sys"}:
                        errors.append(f"E_PROTECTED_ATTRIBUTE_REBIND:{child.value.id}.{child.attr}:{owners[node]}")
    if sorted(import_inventory) != expected_imports:
        errors.append(f"E_IMPORT_INVENTORY:{sorted(import_inventory)}")
    if sorted(from_import_inventory) != sorted(expected_from_imports):
        errors.append(f"E_FROM_IMPORT_INVENTORY:{sorted(from_import_inventory)}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            parent = parents.get(node)
            if node.id in {"eval", "exec", "open", "compile", "__import__", "getattr", "setattr", "delattr", "globals", "locals", "vars", "__builtins__"}:
                errors.append(f"E_SENSITIVE_NAME_ESCAPE:{node.id}:{owners[node]}")
            if node.id in {"subprocess", "os", "sys"}:
                if not isinstance(parent, ast.Attribute) or parent.value is not node:
                    errors.append(f"E_MODULE_VALUE_ESCAPE:{node.id}:{owners[node]}")
            if node.id == "Path" and node not in annotation_nodes:
                direct_call = isinstance(parent, ast.Call) and parent.func is node
                argparse_type = isinstance(parent, ast.keyword) and parent.arg == "type"
                if not direct_call and not argparse_type:
                    errors.append(f"E_PATH_VALUE_ESCAPE:{owners[node]}")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "subprocess" and node.attr not in {"run", "PIPE", "CompletedProcess"}:
                errors.append(f"E_SUBPROCESS_ATTRIBUTE:{node.attr}:{owners[node]}")
            if node.value.id == "subprocess" and node.attr == "run":
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append(f"E_SUBPROCESS_RUN_ALIAS:{owners[node]}")
            if node.value.id == "subprocess" and node.attr == "PIPE" and owners[node] != "run_process":
                errors.append(f"E_SUBPROCESS_PIPE_SCOPE:{owners[node]}")
            if node.value.id == "subprocess" and node.attr == "CompletedProcess" and node not in annotation_nodes:
                errors.append(f"E_SUBPROCESS_COMPLETED_PROCESS_ESCAPE:{owners[node]}")
            if node.value.id == "sys" and node.attr not in {"stderr"}:
                errors.append(f"E_SYS_ATTRIBUTE:{node.attr}:{owners[node]}")
            if node.value.id == "sys" and node.attr == "stderr":
                parent = parents.get(node)
                if not isinstance(parent, ast.keyword) or parent.arg != "file":
                    errors.append(f"E_SYS_STDERR_ESCAPE:{owners[node]}")
            if node.value.id == "os":
                allowed_os = {"builder": {"name", "path", "fdopen", "fsync", "replace", "unlink"}, "validator": {"path"}}[role]
                if node.attr not in allowed_os:
                    errors.append(f"E_OS_ATTRIBUTE:{node.attr}:{owners[node]}")
                if node.attr in {"fdopen", "fsync", "replace", "unlink"}:
                    parent = parents.get(node)
                    if not isinstance(parent, ast.Call) or parent.func is not node:
                        errors.append(f"E_OS_CALLABLE_ESCAPE:{node.attr}:{owners[node]}")
                if node.attr == "path":
                    parent = parents.get(node)
                    if not isinstance(parent, ast.Attribute) or parent.value is not node:
                        errors.append(f"E_OS_PATH_ESCAPE:{owners[node]}")
            if node.value.id == "tempfile":
                allowed_tempfile = {"builder": {"gettempdir", "mkstemp"}, "validator": {"gettempdir"}}[role]
                if node.attr not in allowed_tempfile:
                    errors.append(f"E_TEMPFILE_ATTRIBUTE:{node.attr}:{owners[node]}")
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append(f"E_TEMPFILE_CALLABLE_ESCAPE:{node.attr}:{owners[node]}")
                if node.attr == "mkstemp" and owners[node] != "atomic_write":
                    errors.append(f"E_TEMPFILE_MUTATOR_SCOPE:{owners[node]}")
        if isinstance(node, ast.Attribute) and node.attr == "__dict__":
            errors.append(f"E_DUNDER_DICT_ESCAPE:{owners[node]}")
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in {"run", "Popen", "call", "check_call", "check_output", "system", "popen", "open", "remove", "removedirs", "rename", "renames", "chmod", "chown", "truncate", "touch", "symlink_to", "hardlink_to", "link_to", "write", "writelines", "write_text", "write_bytes"}:
                if not (func.attr == "run" and isinstance(func.value, ast.Name) and func.value.id == "subprocess" and owners[node] == "run_process"):
                    if not (role == "builder" and owners[node] == "atomic_write" and func.attr in {"write"}):
                        errors.append(f"E_SENSITIVE_ATTRIBUTE_CALL:{func.attr}:{owners[node]}")
            if isinstance(func, ast.Attribute) and func.attr == "replace":
                replace_inventory.append((owners[node], ast.unparse(func.value)))
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                full = f"{func.value.id}.{func.attr}"
                if full == "subprocess.run": subprocess_runs.append(node)
                if full in {"subprocess.Popen", "subprocess.call", "subprocess.check_call", "subprocess.check_output", "os.system", "os.popen", "os.remove", "os.removedirs", "os.rename", "os.renames"}:
                    errors.append(f"E_EXEC_API:{full}:{owners[node]}")
                if func.attr in {"unlink", "rmdir", "rename", "remove", "mkdir", "write_text", "write_bytes"} and role == "validator":
                    errors.append(f"E_VALIDATOR_MUTATOR:{func.attr}:{owners[node]}")
            if isinstance(func, ast.Name):
                if func.id == "run_process": run_process_calls.append(node)
                if func.id in {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "globals", "locals", "vars"}:
                    errors.append(f"E_DYNAMIC_EXEC:{func.id}:{owners[node]}")
                if func.id == "git":
                    if not node.args or not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, str) or node.args[0].value not in allowed_git:
                        errors.append(f"E_GIT_GRAMMAR:{owners[node]}")
    if len(subprocess_runs) != 1 or owners.get(subprocess_runs[0]) != "run_process":
        errors.append("E_RUN_PROCESS_SITE")
    if len(run_process_calls) != 1 or owners.get(run_process_calls[0]) != "git":
        errors.append("E_GIT_WRAPPER_SITE")
    if role == "builder":
        allowed_mutator_owner = "atomic_write"
        collectors = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "atomic_write"]
        if len(collectors) != 1:
            errors.append(f"E_ATOMIC_WRITE_COUNT:{len(collectors)}")
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            is_mutator = node.func.attr in {"unlink", "rmdir", "rename", "remove", "mkdir", "write_text", "write_bytes"}
            is_os_replace = node.func.attr == "replace" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os"
            if (is_mutator or is_os_replace) and owners[node] != allowed_mutator_owner:
                errors.append(f"E_BUILDER_MUTATOR:{node.func.attr}:{owners[node]}")
        if policy_ast_hash(source, "module") != EXPECTED_SOURCE_POLICY_HASHES["builder.module"]:
            errors.append("E_BUILDER_MODULE_AST_HASH")
        if len(collectors) == 1 and policy_ast_hash(source, "atomic_write") != EXPECTED_SOURCE_POLICY_HASHES["builder.atomic_write"]:
            errors.append("E_ATOMIC_WRITE_AST_HASH")
    expected_replace = {
        "builder": sorted([("atomic_write", "os"), ("normalized_path", "path")]),
        "validator": sorted([
            ("normalized_path", "path"), ("pointer", "token.replace('~1', '/')"), ("pointer", "token"),
            ("transaction_negative_tests", "base"), ("transaction_negative_tests", "base"),
            ("transaction_negative_tests", "base"), ("validate_precommit_porcelain", "record[3:]"),
        ]),
    }[role]
    if sorted(replace_inventory) != expected_replace:
        errors.append(f"E_REPLACE_INVENTORY:{replace_inventory}")
    return errors


def policy_ast_hash(source: str, kind: str) -> str:
    def stable_ast(value: Any) -> Any:
        if isinstance(value, ast.AST):
            return {"node": type(value).__name__, "fields": [[name, stable_ast(child)] for name, child in ast.iter_fields(value)]}
        if isinstance(value, list):
            return [stable_ast(child) for child in value]
        if isinstance(value, bytes):
            return {"bytes_hex": value.hex()}
        if isinstance(value, complex):
            return {"complex_repr": repr(value)}
        return value

    tree = ast.parse(source)
    if kind == "module":
        payload = json.dumps(stable_ast(tree), sort_keys=True, separators=(",", ":"))
    elif kind in {"run_process", "git", "atomic_write"}:
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == kind]
        require(len(functions) == 1, "E_POLICY_FUNCTION", kind)
        payload = json.dumps(stable_ast(functions[0]), sort_keys=True, separators=(",", ":"))
    elif kind == "git_calls":
        calls = [
            json.dumps(stable_ast(node), sort_keys=True, separators=(",", ":"))
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "git"
        ]
        payload = "\n".join(sorted(calls))
    else:
        raise ValidationError(f"E_POLICY_HASH_KIND:{kind}")
    return sha256(payload.encode("utf-8"))


def validate_source_policy(revision: str, builder_pin: str, validator_pin: str) -> int:
    builder_raw = blob(revision, BUILDER)
    validator_raw = blob(revision, VALIDATOR)
    require(sha256(builder_raw) == builder_pin, "E_BUILDER_PIN")
    require(sha256(validator_raw) == validator_pin, "E_VALIDATOR_PIN")
    builder_source = builder_raw.decode("utf-8")
    validator_source = validator_raw.decode("utf-8")
    require(not source_policy_errors(builder_source, "builder"), "E_BUILDER_SOURCE_POLICY", repr(source_policy_errors(builder_source, "builder")))
    require(not source_policy_errors(validator_source, "validator"), "E_VALIDATOR_SOURCE_POLICY", repr(source_policy_errors(validator_source, "validator")))
    for role, source in (("builder", builder_source), ("validator", validator_source)):
        for kind in ("run_process", "git", "git_calls"):
            require(policy_ast_hash(source, kind) == EXPECTED_SOURCE_POLICY_HASHES[f"{role}.{kind}"], "E_POLICY_AST_HASH", f"{role}.{kind}")
    probes = [
        (builder_source + "\ndef bad(): subprocess.Popen(['x'])\n", "builder"),
        (builder_source + "\ndef bad(): os.system('x')\n", "builder"),
        (builder_source + "\ndef bad(): os.remove('x')\n", "builder"),
        (builder_source + "\ndef bad(): eval('1')\n", "builder"),
        (builder_source + "\ndef bad(): getattr(subprocess, 'run')(['x'])\n", "builder"),
        (builder_source + "\ndef bad(): runner = subprocess.run; runner(['x'])\n", "builder"),
        (builder_source + "\ndef bad(): sys.modules['os'].system('x')\n", "builder"),
        (builder_source + "\ndef bad(): git('push')\n", "builder"),
        (builder_source + "\ndef bad(): git('show', '--output=payload', 'HEAD:x')\n", "builder"),
        (builder_source + "\ndef bad(): subprocess.run(['x'])\n", "builder"),
        (builder_source + "\ndef bad(p): p.replace('x')\n", "builder"),
        (validator_source + "\ndef bad(p): p.unlink()\n", "validator"),
        (validator_source + "\ndef bad(): git('fetch')\n", "validator"),
        (validator_source + "\ndef bad(): subprocess.call(['x'])\n", "validator"),
        (validator_source + "\ndef bad(): setattr(os, 'system', print)\n", "validator"),
        (builder_source + "\ndef bad():\n    m = subprocess\n    m.run(['x'])\n", "builder"),
        (builder_source + "\ndef bad(): (subprocess,)[0].run(['x'])\n", "builder"),
        (builder_source + "\ndef bad(m=subprocess): m.run(['x'])\n", "builder"),
        (builder_source + "\ndef bad(): return subprocess\n", "builder"),
        (builder_source + "\ndef bad(): return eval\n", "builder"),
        (builder_source + "\ndef bad(): return __builtins__['eval']\n", "builder"),
        (builder_source + "\ndef bad(): open('x', 'w')\n", "builder"),
        (builder_source + "\ndef bad(): os.open('x', os.O_WRONLY)\n", "builder"),
        (builder_source + "\ndef bad(): os.chmod('x', 0o777)\n", "builder"),
        (builder_source + "\nfrom os import system\ndef bad(): system('x')\n", "builder"),
        (builder_source + "\nfrom subprocess import Popen\ndef bad(): Popen(['x'])\n", "builder"),
        (builder_source + "\ndef bad(): f = compile; return f\n", "builder"),
        (builder_source + "\ndef bad(): return __import__\n", "builder"),
        (builder_source + "\ndef bad(): return (getattr,)\n", "builder"),
        (builder_source + "\ndef bad(): return os.replace\n", "builder"),
        (builder_source + "\ndef bad(): return os.unlink\n", "builder"),
        (builder_source + "\ndef bad(): return os.fdopen\n", "builder"),
        (builder_source + "\ndef bad(): return Path\n", "builder"),
        (builder_source + "\ndef bad(handle): handle.write(b'x')\n", "builder"),
        (builder_source + "\ndef bad(handle): handle.writelines([b'x'])\n", "builder"),
        (builder_source + "\ndef bad(): tempfile.mkstemp(dir=REPO)\n", "builder"),
        (builder_source + "\ndef bad(): tempfile.NamedTemporaryFile(mode='wb', dir=REPO).write(b'x')\n", "builder"),
        (builder_source + "\ndef bad(fd): os.fdopen(fd, 'wb').write(b'x')\n", "builder"),
        (builder_source + "\ndef atomic_write(path, raw): (REPO / 'pwn').write_bytes(raw)\n", "builder"),
        (builder_source + "\ndef bad(): os.path.__dict__['os'].__dict__['system']('x')\n", "builder"),
        (builder_source + "\ndef bad(callback): callback()\n", "builder"),
    ]
    for mutated, role in probes:
        source = builder_source if role == "builder" else validator_source
        rejected = bool(source_policy_errors(mutated, role)) or any(
            policy_ast_hash(mutated, kind) != policy_ast_hash(source, kind)
            for kind in ("run_process", "git", "git_calls")
        )
        require(rejected, "E_SOURCE_POLICY_NEGATIVE")
    return len(probes)


def validate_precommit_porcelain(raw: str) -> None:
    records = [record for record in raw.split("\0") if record]
    require(len(records) == len(EXACT_PATHS), "E_STATUS_COUNT", repr(records))
    paths = []
    for record in records:
        require(len(record) >= 4 and record[2] == " ", "E_STATUS_FORMAT", repr(record))
        require(record[:2] in {"A ", "M "}, "E_STATUS_NOT_INDEX_ONLY", repr(record))
        paths.append(record[3:].replace("\\", "/"))
    require(sorted(paths) == EXACT_PATHS, "E_STATUS_PATHS", repr(paths))


def validate_mode_arguments(persistence: bool, expected_commit: str | None) -> None:
    if persistence:
        require(isinstance(expected_commit, str) and re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None, "E_EXPECTED_COMMIT_FORMAT")
    else:
        require(expected_commit is None, "E_UNEXPECTED_COMMIT")


def persistence_argument_negative_tests() -> int:
    probes = [
        (True, None),
        (True, "--output=C"),
        (True, "A" * 40),
        (True, "a" * 39),
        (False, "a" * 40),
    ]
    for persistence, expected_commit in probes:
        try:
            validate_mode_arguments(persistence, expected_commit)
        except ValidationError:
            continue
        raise ValidationError("E_PERSISTENCE_ARGUMENT_NEGATIVE")
    return len(probes)


def verify_exact_stage() -> None:
    staged = sorted(x for x in str(git("diff", "--cached", "--name-only")).splitlines() if x)
    require(staged == EXACT_PATHS, "E_EXACT_STAGE", repr(staged))
    require(not str(git("diff", "--name-only", "--", *EXACT_PATHS)).strip(), "E_UNSTAGED")
    require(not str(git("diff", "--name-only", "--", "Claude")).strip(), "E_CLAUDE_DIRTY")
    require(not str(git("diff", "--cached", "--name-only", "--", "Claude")).strip(), "E_CLAUDE_STAGED")
    validate_precommit_porcelain(str(git("status", "--porcelain=v1", "-z", "--untracked-files=all")))
    require(not str(git("diff", "--check")).strip(), "E_DIFF_CHECK")
    require(not str(git("diff", "--cached", "--check")).strip(), "E_CACHED_DIFF_CHECK")
    for path in EXACT_PATHS:
        require((REPO / path).read_bytes() == blob(":", path), "E_INDEX_WORKTREE_BYTES", path)


def live_tip(ref: str) -> str:
    fields = str(git("ls-remote", "--heads", "origin", ref)).strip().split()
    require(len(fields) >= 2 and fields[1] == ref, "E_LIVE_REF", ref)
    return fields[0]


def verify_refs(expected_commit: str | None = None) -> None:
    head = str(git("rev-parse", "HEAD")).strip()
    require(str(git("branch", "--show-current")).strip() == BRANCH, "E_BRANCH")
    require(str(git("rev-parse", "codex/lib-physics-endgame-v1025_2")).strip() == PROTECTED, "E_PROTECTED")
    require(str(git("rev-parse", "origin/codex/lib-physics-endgame-v1025_2")).strip() == PROTECTED, "E_PROTECTED_TRACKING")
    require(live_tip("refs/heads/codex/lib-physics-endgame-v1025_2") == PROTECTED, "E_PROTECTED_LIVE")
    require(str(git("rev-parse", "origin/main")).strip() == MAIN, "E_MAIN")
    require(live_tip("refs/heads/main") == MAIN, "E_MAIN_LIVE")
    require(str(git("rev-parse", "--abbrev-ref", "@{upstream}")).strip() == f"origin/{BRANCH}", "E_UPSTREAM_NAME")
    if expected_commit is None:
        require(head == EXPECTED_PARENT, "E_PRECOMMIT_PARENT")
        require(str(git("rev-parse", "@{upstream}")).strip() == EXPECTED_PARENT, "E_PRECOMMIT_UPSTREAM")
        require(str(git("rev-parse", f"origin/{BRANCH}")).strip() == EXPECTED_PARENT, "E_PRECOMMIT_TRACKING")
        require(live_tip(f"refs/heads/{BRANCH}") == EXPECTED_PARENT, "E_PRECOMMIT_LIVE")
    else:
        require(head == expected_commit, "E_PERSIST_HEAD")
        require(str(git("rev-parse", "@{upstream}")).strip() == expected_commit, "E_PERSIST_UPSTREAM")
        require(str(git("rev-parse", f"origin/{BRANCH}")).strip() == expected_commit, "E_PERSIST_TRACKING")
        require(live_tip(f"refs/heads/{BRANCH}") == expected_commit, "E_PERSIST_LIVE")
        require(str(git("show", "-s", "--format=%P", expected_commit)).strip() == EXPECTED_PARENT, "E_PERSIST_PARENT")
        require(str(git("show", "-s", "--format=%s", expected_commit)).strip() == EXPECTED_SUBJECT, "E_PERSIST_SUBJECT")
        changed = sorted(x for x in str(git("diff-tree", "--no-commit-id", "--name-only", "-r", expected_commit)).splitlines() if x)
        require(changed == EXACT_PATHS, "E_PERSIST_PATHS", repr(changed))
        require(not str(git("diff", "--check", EXPECTED_PARENT, expected_commit)).strip(), "E_PERSIST_DIFF_CHECK")
        for path in EXACT_PATHS:
            require((REPO / path).read_bytes() == blob(expected_commit, path), "E_COMMIT_WORKTREE_BYTES", path)


def fixture_bytes(path: Path, allowed_name: str) -> bytes:
    require(path.is_absolute() and path.name == allowed_name, "E_FIXTURE_NAME", str(path))
    lexical = Path(os.path.abspath(path))
    temp_root = Path(os.path.abspath(tempfile.gettempdir()))
    require(lexical.parent.name == "p065-step75_1-fixtures" and lexical.parent.parent == temp_root, "E_FIXTURE_BOUNDARY")
    cursor = lexical
    while cursor != temp_root:
        require(cursor.exists() and not cursor.is_symlink(), "E_FIXTURE_LINK", str(cursor))
        if hasattr(cursor, "is_junction"):
            require(not cursor.is_junction(), "E_FIXTURE_JUNCTION", str(cursor))
        cursor = cursor.parent
    return lexical.read_bytes()


def validate_determinism(args: argparse.Namespace, disposition_raw: bytes, carry_raw: bytes) -> list[str]:
    d1 = fixture_bytes(args.disposition_one, "source-disposition-one.json")
    d2 = fixture_bytes(args.disposition_two, "source-disposition-two.json")
    c1 = fixture_bytes(args.carry_one, "carry-forward-one.json")
    c2 = fixture_bytes(args.carry_two, "carry-forward-two.json")
    require(d1 == d2 == disposition_raw, "E_DISPOSITION_DETERMINISM")
    require(c1 == c2 == carry_raw, "E_CARRY_DETERMINISM")
    return [sha256(d1), sha256(d2), sha256(c1), sha256(c2)]


def transaction_negative_tests() -> int:
    added = {BUILDER, VALIDATOR, DISPOSITION, CARRY, RESULT}
    base = "".join(f"{'A ' if path in added else 'M '} {path}\0" for path in EXACT_PATHS)
    probes = [
        base + "?? Codex/rogue.tmp\0",
        base.replace(f"A  {DISPOSITION}", f" M {DISPOSITION}", 1),
        base.replace(f"A  {DISPOSITION}", f"R  {DISPOSITION}", 1),
        base.replace(f"A  {DISPOSITION}\0", "", 1),
    ]
    for probe in probes:
        try:
            validate_precommit_porcelain(probe)
        except ValidationError:
            continue
        raise ValidationError("E_TRANSACTION_NEGATIVE")
    return len(probes)


def output_guard_checks(builder_source: str) -> int:
    required = [
        '"p065-step75_1-fixtures"', '"E_OUTPUT_TEMP_ROOT"', '"E_OUTPUT_PARENT_LINK"',
        '"E_OUTPUT_PARENT_ESCAPE"', '"E_OUTPUT_LINK"', "atomic_write(args.disposition",
    ]
    for token in required:
        require(token in builder_source, "E_OUTPUT_GUARD_TOKEN", token)
    require(builder_source.index("require((REPO / RESULT).exists()") < builder_source.index("inputs, metadata = load_inputs()") < builder_source.index("atomic_write(args.disposition"), "E_JSON_LAST_ORDER")
    return len(required) + 1


def negative_tests(source: dict[str, Any], carry: dict[str, Any]) -> int:
    def refresh_semantic(value: dict[str, Any]) -> None:
        payload = copy.deepcopy(value)
        payload.pop("semantic_sha256")
        value["semantic_sha256"] = sha256(canonical(payload))

    def coherent_owner_mutation(value: dict[str, Any], identity: str) -> None:
        observation = next(row for row in value["observation_records"] if row["observation_id"] == identity)
        observation["canonical_owner"] = "PHASE-999-NEGATIVE-PROBE"
        observation["target_phase"] = 999
        observation["acceptance_criterion"] = "Negative probe must be rejected by the independent observation contract."
        for obligation in value["active_obligations"]:
            if obligation["origin_identity"] == identity:
                obligation["canonical_owner"] = observation["canonical_owner"]
                obligation["target_phase"] = observation["target_phase"]
                obligation["acceptance_criterion"] = observation["acceptance_criterion"]
        universe = value["current_owner_duplicate_check_universe"]
        owner_record = next(row for row in universe["records"] if row["origin_identity"] == identity)
        owner_record["owner_id"] = observation["canonical_owner"]
        owner_record["target_phase"] = observation["target_phase"]
        universe["records_sha256"] = record_sha(universe["records"])
        refresh_semantic(value)

    bad_json = [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}']
    for raw in bad_json:
        try:
            strict_load(raw)
        except ValidationError:
            continue
        raise ValidationError("E_JSON_NEGATIVE")
    mutations: list[tuple[str, dict[str, Any]]] = []
    m = copy.deepcopy(source); m["expected_parent"] = "0" * 40; mutations.append(("source", m))
    m = copy.deepcopy(source); m["branch"] = "main"; mutations.append(("source", m))
    m = copy.deepcopy(source); m["authority"]["publication_ready"] = True; mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"].pop(); mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["occurrence_identity"] = {}; mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["disposition"] = "EMPIRICAL"; mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["canonical_owner"] = ""; mutations.append(("source", m))
    m = copy.deepcopy(source); m["blob_disposition_groups"].pop(); mutations.append(("source", m))
    m = copy.deepcopy(source); m["semantic_sha256"] = "0" * 64; mutations.append(("source", m))
    m = copy.deepcopy(carry); m["observation_records"].pop(); mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["active_obligations"][0]["canonical_owner"] = ""; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["inherited_phase064_routes"].pop(); mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["observation_records"][0]["origin_record"] = {}; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["new_phase065_blockers"] = [{"hidden": True}]; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["authority"]["external_scientific_truth"] = True; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["semantic_duplicate_groups"][0]["canonical_owner"] = "OTHER"; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["observation_records"][[r["observation_id"] for r in carry["observation_records"]].index("D74-007")]["state"] = "OPEN_CARRY"; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["gate_summary"]["active_obligations"] += 1; mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["semantic_sha256"] = "0" * 64; mutations.append(("carry", m))
    m = copy.deepcopy(source); m["coherent_extra"] = True; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["coherent_extra"] = True; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(carry); m["coherent_extra"] = True; refresh_semantic(m); mutations.append(("carry", m))
    m = copy.deepcopy(carry); m["observation_records"][0]["coherent_extra"] = True; refresh_semantic(m); mutations.append(("carry", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["status"] = "OPEN_UNVERIFIED"; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["reason"] = "Coherent but fabricated reason."; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["acceptance_criterion"] = "Coherent but fabricated acceptance."; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(source); m["blob_disposition_groups"][0]["dedup_group"] = "NEGATIVE-PROBE"; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(source); m["blob_disposition_groups"][0]["linked_conformance_rows"] = ["NEGATIVE-PROBE"]; refresh_semantic(m); mutations.append(("source", m))
    m = copy.deepcopy(source); m["source_dispositions"][0]["evidence_routes"][0] = {
        "artifact_path": TOPOLOGY, "json_pointer": "/occurrences/1",
        "record_sha256": record_sha(source["source_dispositions"][1]["occurrence_identity"]), "role": "OCCURRENCE_IDENTITY",
    }; refresh_semantic(m); mutations.append(("source", m))
    for identity in ("INTENT-PROV-0230", "P065-S71-F02", "P065-S72-F03"):
        m = copy.deepcopy(carry); coherent_owner_mutation(m, identity); mutations.append(("carry", m))
    inputs, metadata = load_inputs()
    for kind, mutation in mutations:
        try:
            validate_source(mutation, inputs, metadata) if kind == "source" else validate_carry(mutation, inputs, metadata)
        except (ValidationError, KeyError):
            continue
        raise ValidationError("E_SEMANTIC_NEGATIVE", kind)
    return len(bad_json) + len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--persistence", action="store_true")
    parser.add_argument("--expected-commit")
    parser.add_argument("--disposition-one", type=Path, required=True)
    parser.add_argument("--disposition-two", type=Path, required=True)
    parser.add_argument("--carry-one", type=Path, required=True)
    parser.add_argument("--carry-two", type=Path, required=True)
    parser.add_argument("--expected-builder-sha256", required=True)
    parser.add_argument("--expected-validator-sha256", required=True)
    parser.add_argument("--expected-disposition-sha256", required=True)
    parser.add_argument("--expected-carry-sha256", required=True)
    args = parser.parse_args()
    validate_mode_arguments(args.persistence, args.expected_commit)
    require((REPO / DISPOSITION).exists() and (REPO / CARRY).exists(), "E_ARTIFACT_MISSING")
    disposition_raw = (REPO / DISPOSITION).read_bytes()
    carry_raw = (REPO / CARRY).read_bytes()
    require(sha256(disposition_raw) == args.expected_disposition_sha256, "E_DISPOSITION_RAW_PIN")
    require(sha256(carry_raw) == args.expected_carry_sha256, "E_CARRY_RAW_PIN")
    source = strict_load(disposition_raw)
    carry = strict_load(carry_raw)
    inputs, metadata = load_inputs()
    source_nodes, source_depth = validate_source(source, inputs, metadata)
    carry_nodes, carry_depth = validate_carry(carry, inputs, metadata)
    verify_docs()
    revision = args.expected_commit if args.persistence and args.expected_commit else ":"
    policy = validate_source_policy(revision, args.expected_builder_sha256, args.expected_validator_sha256)
    verify_controls(source, revision)
    verify_controls(carry, revision)
    negatives = negative_tests(source, carry)
    transactions = transaction_negative_tests()
    persistence_arguments = persistence_argument_negative_tests()
    builder_source = blob(revision, BUILDER).decode("utf-8")
    output_checks = output_guard_checks(builder_source)
    deterministic = validate_determinism(args, disposition_raw, carry_raw)
    if args.persistence:
        verify_refs(str(args.expected_commit))
        require(not str(git("status", "--porcelain")).strip(), "E_PERSIST_DIRTY")
        terminal = PERSISTENCE_GATE
    else:
        verify_refs()
        verify_exact_stage()
        terminal = GATE
    print(terminal, json.dumps({
        "occurrences": len(source["source_dispositions"]),
        "blobs": len(source["blob_disposition_groups"]),
        "observations": len(carry["observation_records"]),
        "active": len(carry["active_obligations"]),
        "source_nodes": source_nodes, "source_depth": source_depth,
        "carry_nodes": carry_nodes, "carry_depth": carry_depth,
        "negative": negatives, "source_policy_negative": policy,
        "output_guard": output_checks, "transaction_negative": transactions,
        "persistence_argument_negative": persistence_arguments,
        "determinism": deterministic,
        "builder_sha256": args.expected_builder_sha256,
        "validator_sha256": args.expected_validator_sha256,
        "disposition_sha256": args.expected_disposition_sha256,
        "carry_sha256": args.expected_carry_sha256,
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, ValueError, TypeError) as exc:
        print(f"FAIL_P065_STEP75_1 {exc}", file=sys.stderr)
        raise SystemExit(1)
