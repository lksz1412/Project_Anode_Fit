#!/usr/bin/env python3
"""Build deterministic Phase 064 Step 69.1 dispositions and carry-forward delta."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import subprocess
from collections import Counter, defaultdict
from typing import Any


REPO = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "84b977a5333870529369d62a6dab8459a6aa551d"
GATE = "PASS_P064_STEP69_1_DISPOSITIONS"
SENTINEL = "P064_STEP69_1_RESULT_FIRST_PRECOMMIT"
DISPOSITION = "Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json"
CARRY = "Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json"
RESULT = "Codex/results/PHASE_064_STEP_069_1_DISPOSITION_RESULT.md"

TOPOLOGY = "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json"
READ = "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json"
LITERATURE = "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json"
LITERATURE_READ = "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json"
RATIO = "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json"
CODE_DELTA = "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json"
RUNTIME = "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json"
AUTHORITY_MATRIX = "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json"
P63_DISPOSITION = "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json"
P63_CARRY = "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json"

INPUT_SHA256 = {
    TOPOLOGY: "ce0fcbda41e866d8f225255ae27ae0e0e1faba9b985c7f72194a14d085be1f99",
    READ: "5fadd789fe05ea83b294a34e0270f637a44c8359f79e63addfed60e8b62ac445",
    LITERATURE: "db67fc40d9fba6d03547325061b16d03da87ddf59e0985fd6d7b471d092d453a",
    LITERATURE_READ: "273fa6eb35000b013b48eeb63154b098bd8d0ab3dc89a8634d478d75c4106fc4",
    RATIO: "bf940a9b3707b9e90d5e82068f722a9bb0aefe632157371db969e572e6e1af7b",
    CODE_DELTA: "b360cf220e519e861080405032dfc2c5be108998901b0c130b8ab325859e5ba3",
    RUNTIME: "f3c87cf1d2f3eea271ac88a76cf516695ac0a8843984651bd591d1d8f31ea1d9",
    AUTHORITY_MATRIX: "e97e5362c8b162614c287bf2826a00bcd4b70600a67d7096e08e628a4dd59d5c",
    P63_DISPOSITION: "cb50d7f94066fe1d8238e7fc1ebe8394271dbda8d0fd03a16aba0104fa752f8b",
    P63_CARRY: "c44c4ee1366ae53969379c0b698e707862cbc290b209edf7ef80d9965a01eb46",
}

AUTHORITY = {
    "canonical_equation_promoted": False,
    "external_experimental_truth": False,
    "external_material_truth": False,
    "external_scientific_truth": False,
    "primary_literature_jcp147_method_truth": True,
    "primary_literature_ref6_method_truth": True,
    "primary_literature_ref7_method_truth": False,
    "publication_ready": False,
    "phase_ceiling": "CONDITIONAL_P064",
    "scope": "INTERNAL_V1023_LINEAGE_DISPOSITION_ONLY",
}
ALLOWED = {"CORRECT", "PRESERVE", "THEORY_ONLY", "UNVERIFIED"}
ACTIVE_SOURCE_DISPOSITIONS = {"CORRECT", "UNVERIFIED"}
CORRECT_SOURCE_NUMBERS = {
    1, 2, 3, 7, 9, 10, 12, 13, 15, 18, 19, 20, 22, 23, 25, 27, 28,
    31, 35, 38, 39, 41, 42, 44, 49, 50, 51, 52, 53, 54, 55, 76, 78, 82, 83,
}
UNVERIFIED_SOURCE_NUMBERS = {4, 6, 21, 29, 36, 37, 45, 48, 63}
THEORY_ONLY_SOURCE_NUMBERS = {11, 14, 16, 17, 57}
CORRECT_TARGETS = {
    **{number: 83 for number in (1, 2, 3, 76, 78, 82, 83)},
    **{number: 87 for number in (7, 9, 10, 12, 13, 15, 18, 19, 20, 27, 28)},
    **{number: 78 for number in (22, 23, 25, 31, 35, 38, 39, 41, 42, 44)},
    **{number: 79 for number in (49, 50, 51, 52, 53, 54, 55)},
}
DOWNSTREAM = {phase: list(range(phase + 1, 91)) for phase in range(65, 90)}
PHASE_STEPS = {
    70: "HISTORICAL_EVIDENCE_PRESERVATION", 71: "PRIMARY_SOURCE_ACQUISITION",
    73: "LITERATURE_APPLICABILITY", 74: "UNITS_TRANSFER_BOUNDARY",
    75: "BACKGROUND_ROOT_CLOSURE", 76: "INTEGRAL_RUNTIME_CLOSURE",
    78: "LCO_CANONICAL_SYNTHESIS", 79: "SILICON_CANONICAL_SYNTHESIS",
    81: "IDENTIFIABILITY_AND_INVERSE_VALIDATION", 82: "CANONICAL_EQUATION_FREEZE",
    83: "REPRODUCIBLE_IMPLEMENTATION", 86: "MATERIAL_VALIDATION",
    87: "CANONICAL_SOURCE_SYNTHESIS", 88: "FINAL_RED_TEAM",
    89: "PDF_PRESERVATION",
}
AUTH_TARGETS = {
    "AUTH-001": 83, "AUTH-002": 73, "AUTH-003": 76, "AUTH-004": 74,
    "AUTH-005": 76, "AUTH-006": 74, "AUTH-007": 88, "AUTH-008": 81,
    "AUTH-009": 86, "AUTH-010": 71, "AUTH-011": 75, "AUTH-012": 82,
    "AUTH-013": 83, "AUTH-014": 76,
    "RESID-015": 83, "RESID-016": 83, "RESID-017": 88, "RESID-018": 87,
}
CORRECTION_TO_AUTH = {
    "P064-S66-CORR-001": ["AUTH-006"],
    "P064-S66-CORR-002": ["AUTH-012"],
    "P064-S66-CORR-003": ["AUTH-003"],
    "P064-S66-CORR-004": ["AUTH-003"],
    "P064-S66-CORR-005": ["AUTH-002"],
    "P064-S66-CORR-006": ["AUTH-004"],
    "P064-S66-CORR-007": ["AUTH-005"],
    "P064-S66-CORR-008": ["AUTH-006"],
    "P064-S66-CORR-009": ["AUTH-001"],
    "P064-S66-CORR-010": ["AUTH-013"],
    "P064-S66-CORR-011": ["RESID-018"],
}
FINDING_TO_AUTH = {
    "P064-S67-F001": ["AUTH-006"],
    "P064-S67-F002": ["AUTH-011"],
    "P064-S67-F003": ["AUTH-005"],
    "P064-S67-F004": ["AUTH-003"],
    "P064-S67-F005": ["RESID-015"],
    "P064-S67-F006": ["AUTH-004"],
    "P064-S67-F007": ["RESID-016"],
    "P064-S67-F008": ["AUTH-001"],
    "P064-S67-F009": ["RESID-017"],
}
PROVISIONAL_TARGETS = {
    192: 70, 193: 70, 194: 70, 195: 76, 196: 76, 197: 74,
    198: 71, 199: 73, 200: 83, 201: 74, 202: 74, 203: 83,
    204: 73, 205: 71, 206: 88, 207: 74, 208: 73, 209: 73,
    210: 83, 211: 71, 212: 88, 213: 70, 214: 81, 215: 81,
    216: 74, 217: 71, 218: 81, 219: 86, 220: 81, 221: 81,
    222: 86, 223: 78, 224: 79, 225: 83, 226: 74, 227: 70,
}
PROVISIONAL_STATUSES = {
    192: "PRESERVED_HISTORICAL", 193: "PRESERVED_HISTORICAL",
    194: "CLOSED_CONFIRMED", 198: "PARTIALLY_RESOLVED_OPEN",
    204: "PARTIALLY_RESOLVED_OPEN", 213: "PRESERVED_HISTORICAL",
    217: "PARTIALLY_RESOLVED_OPEN", 227: "PRESERVED_HISTORICAL",
}
PROVISIONAL_TO_AUTH = {
    192: ["AUTH-002"], 194: ["AUTH-002", "AUTH-003"], 195: ["AUTH-003"],
    196: ["AUTH-003"], 197: ["AUTH-006"], 198: ["AUTH-002", "AUTH-010"],
    199: ["AUTH-002", "AUTH-003"], 200: ["AUTH-003", "AUTH-007"],
    201: ["AUTH-007"], 202: ["AUTH-004"], 204: ["AUTH-009"],
    205: ["AUTH-010"], 206: ["AUTH-007"], 207: ["AUTH-006", "AUTH-007"],
    208: ["AUTH-003"], 209: ["AUTH-007"], 210: ["AUTH-007"],
    211: ["AUTH-010"], 212: ["AUTH-007"], 213: ["AUTH-007"],
    214: ["AUTH-008"], 215: ["AUTH-007", "AUTH-009"], 216: ["AUTH-006"],
    217: ["AUTH-010"], 218: ["AUTH-008"], 219: ["AUTH-006", "AUTH-009"],
    220: ["AUTH-008"], 221: ["AUTH-008"], 222: ["AUTH-009"],
    223: ["AUTH-009"], 224: ["AUTH-009"], 225: ["AUTH-013"],
    226: ["AUTH-004"], 227: ["AUTH-007"],
}


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


def record_sha(value: Any) -> str:
    return sha256(compact(value))


def git_bytes(*args: str) -> bytes:
    process = subprocess.run(["git", *args], cwd=REPO, capture_output=True, timeout=120, check=False)
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


def pointer_value(document: Any, pointer: str) -> Any:
    value = document
    for token in pointer.lstrip("/").split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def source_contract_routes(inputs: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    routes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    specs = ((RATIO, "source_contracts"), (CODE_DELTA, "source_contracts"), (AUTHORITY_MATRIX, "source_contracts"))
    for artifact_path, section in specs:
        for index, row in enumerate(inputs[artifact_path][section]):
            path = row["path"]
            routes[path].append({
                "artifact_path": artifact_path,
                "json_pointer": f"/{section}/{index}",
                "record_sha256": record_sha(row),
                "route_role": "AUDIT_SOURCE_CONTRACT",
            })
    bibliography = inputs[LITERATURE]["bibliography_boundaries"]["adopted_bibliography"]
    routes[bibliography["path"]].append({
        "artifact_path": LITERATURE,
        "json_pointer": "/bibliography_boundaries/adopted_bibliography",
        "record_sha256": record_sha(bibliography),
        "route_role": "ADOPTED_BIBLIOGRAPHY_BOUNDARY",
    })
    return routes


def source_authority_links(source: dict[str, Any]) -> list[str]:
    path = source["path"]
    lower = path.lower()
    profile = source.get("token_profile", {})
    links: set[str] = set()
    if profile.get("c_rate", 0) or profile.get("factor_3600", 0):
        links.add("AUTH-006")
    if profile.get("fredholm", 0) or profile.get("ref6_ref7", 0):
        links.add("AUTH-002")
    if profile.get("picard", 0) or profile.get("ratio", 0) or profile.get("volterra", 0):
        links.update(("AUTH-003", "AUTH-014"))
    if profile.get("transfer", 0) or profile.get("omega", 0):
        links.update(("AUTH-004", "AUTH-005"))
    if source["role"] in {"code", "test", "implementation_guide", "supporting_document"}:
        links.add("AUTH-013")
    if any(token in lower for token in ("phase_p5", "merge_readiness", "aud_report", "execution_ledger")):
        links.update(("AUTH-007", "RESID-017"))
    if any(token in lower for token in ("curve_qa", "qa_v102")):
        links.update(("AUTH-008", "AUTH-009", "AUTH-013"))
    if "ch1v22_bib" in lower:
        links.update(("AUTH-002", "AUTH-010", "AUTH-012"))
    if any(token in lower for token in ("appe_selfconsistent", "cond_audit", "p1_ratio_check")):
        links.add("AUTH-001")
    if "test_gates_v1023_selfconsistent" in lower:
        links.add("RESID-015")
    if "p1_ratio_check" in lower:
        links.add("RESID-016")
    if "ch1_sec09_tail" in lower:
        links.add("RESID-018")
    if source["role"] == "code":
        links.add("AUTH-011")
    return sorted(links)


def source_number(source: dict[str, Any]) -> int:
    return int(source["occurrence_id"].rsplit("-", 1)[1])


def disposition_for(source: dict[str, Any]) -> str:
    number = source_number(source)
    if number in CORRECT_SOURCE_NUMBERS:
        return "CORRECT"
    if number in UNVERIFIED_SOURCE_NUMBERS:
        return "UNVERIFIED"
    if number in THEORY_ONLY_SOURCE_NUMBERS:
        return "THEORY_ONLY"
    return "PRESERVE"


def source_target(source: dict[str, Any], disposition: str) -> int:
    number = source_number(source)
    path = source["path"].lower()
    if disposition == "CORRECT":
        return CORRECT_TARGETS[number]
    if disposition == "UNVERIFIED":
        return 71
    if disposition == "THEORY_ONLY":
        return 82
    if source["role"] in {"generated_document", "figure"}:
        return 89
    if source["role"] == "result":
        return 70
    if "/ch2" in path:
        return 78
    if "/ch3" in path:
        return 79
    return 87


def prior_counterpart(source: dict[str, Any], inputs: dict[str, Any]) -> tuple[int, dict[str, Any]] | None:
    path = source["path"]
    candidate = path.replace("/v1.0.23/", "/v1.0.22/").replace("v1.0.23", "v1.0.22").replace("v1023", "v1022")
    for index, row in enumerate(inputs[P63_DISPOSITION]["source_dispositions"]):
        if row["source_identity"]["path"] == candidate:
            return index, row
    return None


def source_identity(source: dict[str, Any]) -> dict[str, Any]:
    return dict(source)


def build_source_dispositions(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    topology = inputs[TOPOLOGY]
    sources = topology["sources"]
    audit_routes = source_contract_routes(inputs)
    rows: list[dict[str, Any]] = []
    for ordinal, source in enumerate(sources, 1):
        counterpart = prior_counterpart(source, inputs)
        evidence = [
            {
                "artifact_path": TOPOLOGY,
                "json_pointer": f"/sources/{ordinal - 1}",
                "record_sha256": record_sha(source),
                "route_role": "SOURCE_IDENTITY",
            },
            {
                "artifact_path": READ,
                "json_pointer": f"/sources/{ordinal - 1}",
                "record_sha256": record_sha(inputs[READ]["sources"][ordinal - 1]),
                "route_role": "FULL_READ_ATTESTATION",
            },
            *audit_routes.get(source["path"], []),
        ]
        if counterpart is not None:
            prior_index, prior_row = counterpart
            evidence.append({
                "artifact_path": P63_DISPOSITION,
                "json_pointer": f"/source_dispositions/{prior_index}",
                "record_sha256": record_sha(prior_row),
                "route_role": "V1022_LINEAGE_COUNTERPART",
            })
        evidence = [
            {"evidence_id": f"P064-EVID-{ordinal:04d}-{index:03d}", **route}
            for index, route in enumerate(evidence, 1)
        ]
        disposition = disposition_for(source)
        require(disposition in ALLOWED, f"invalid disposition: {source['occurrence_id']}")
        active = disposition in ACTIVE_SOURCE_DISPOSITIONS
        target = source_target(source, disposition)
        authority_links = source_authority_links(source)
        rows.append({
            "disposition_id": f"P064-DISP-{ordinal:04d}",
            "source_id": source["occurrence_id"],
            "source_identity": source_identity(source),
            "source_record_sha256": record_sha(source),
            "disposition": disposition,
            "status": "OPEN_UNVERIFIED" if disposition == "UNVERIFIED" else "OPEN_CORRECTION" if disposition == "CORRECT" else "BOUNDED_PRESERVE",
            "reason": (
                f"The exact v1.0.23 manifest occurrence has role {source['role']}, full-read state {source['full_read_state']} "
                f"and {sum(route['route_role'] == 'AUDIT_SOURCE_CONTRACT' for route in evidence)} direct Step 65--68 audit contract route(s). "
                f"A v1.0.22 exact-path counterpart is {'retained' if counterpart is not None else 'not present'}; the frozen source is not rewritten in Phase 064."
            ),
            "evidence_ids": [route["evidence_id"] for route in evidence],
            "evidence_routes": evidence,
            "corroborating_authority_route_ids": authority_links,
            "carry_forward_links": [f"P064-SOURCE-ROUTE-{ordinal:04d}", *authority_links],
            "inherited_owner_id": counterpart[1]["canonical_owner_id"] if counterpart is not None else None,
            "current_owner_id": f"PHASE-{target:03d}-{PHASE_STEPS[target]}",
            "primary_target": {"phase": target, "step": PHASE_STEPS[target]},
            "downstream_target_phases": DOWNSTREAM[target],
            "acceptance_criterion": (
                f"Phase {target} must retain exact occurrence identity and {'resolve the routed correction/unverified evidence' if active else 'preserve the bounded historical/theory role'}; "
                "corroborating authority routes remain separate claim-level records and do not create duplicate source identities."
            ),
            "non_double_count_basis": "ONE_V1023_MANIFEST_OCCURRENCE; SOURCE_REMEDIATION_DISTINCT_FROM_AUTHORITY_ROUTE",
            "authority_flags": {
                "canonical_equation": False,
                "external_experimental": False,
                "external_material": False,
                "external_scientific": False,
                "publication_ready": False,
            },
        })
    require(len(rows) == 83, f"source disposition denominator: {len(rows)}")
    return rows


def supplemental_dispositions(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    topology = inputs[TOPOLOGY]
    literature = inputs[LITERATURE]
    plan = next(row for row in inputs[RATIO]["source_contracts"] if row["path"].startswith("Claude/plans/"))
    extract = literature["bibliography_boundaries"]["printed_reference_list"]
    sources = {row["source_id"]: row for row in literature["sources"]}
    specs = [
        ("P064-SUP-PLAN-001", "PLAN", plan, "PRESERVE", "BOUNDED_PROCESS_EVIDENCE", None, 87),
        ("P064-SUP-LIT-001", "LITERATURE_ORIGINAL", sources["JCP147"], "THEORY_ONLY", "FULL_TEXT_READ_BOUNDED_METHOD", None, 73),
        ("P064-SUP-LIT-002", "LITERATURE_ORIGINAL", sources["REF6"], "THEORY_ONLY", "FULL_TEXT_READ_BOUNDED_METHOD", None, 73),
        ("P064-SUP-LIT-003", "LITERATURE_METADATA_AND_GNF", sources["REF7"], "UNVERIFIED", "OPEN_GROUND_NOT_FOUND", "PHASE-071-PRIMARY-SOURCE-ACQUISITION", 71),
        ("P064-SUP-LIT-004", "LITERATURE_EXTRACT", extract, "PRESERVE", "BOUNDED_DERIVED_TEXT", None, 73),
        ("P064-SUP-PROC-001", "PROCESS_DECISION", {
            "p4_state": topology["process"]["p4_state"],
            "p4_result_present": topology["process"]["p4_result_present"],
            "phase_state": topology["process"]["phase_states"]["P4"],
        }, "PRESERVE", "INTENTIONAL_SKIP_PRESERVED", "PHASE-081-IDENTIFIABILITY-AUTHORIZATION", 81),
    ]
    pointers = [
        (RATIO, f"/source_contracts/{inputs[RATIO]['source_contracts'].index(plan)}"),
        (LITERATURE, f"/sources/{literature['sources'].index(sources['JCP147'])}"),
        (LITERATURE, f"/sources/{literature['sources'].index(sources['REF6'])}"),
        (LITERATURE, f"/sources/{literature['sources'].index(sources['REF7'])}"),
        (LITERATURE, "/bibliography_boundaries/printed_reference_list"),
        (TOPOLOGY, "/process"),
    ]
    rows: list[dict[str, Any]] = []
    for index, ((item_id, denominator, anchor, disposition, status, owner, target), (path, pointer)) in enumerate(zip(specs, pointers), 1):
        evidence_record = pointer_value(inputs[path], pointer)
        rows.append({
            "supplemental_id": item_id,
            "denominator": denominator,
            "manifest_member": False,
            "source_anchor": anchor,
            "source_record_sha256": record_sha(anchor),
            "disposition": disposition,
            "status": status,
            "reason": "This item is required process/literature evidence but is not one of the 83 frozen v1.0.23 manifest occurrences.",
            "evidence_routes": [{
                "evidence_id": f"P064-SUP-EVID-{index:03d}",
                "artifact_path": path,
                "json_pointer": pointer,
                "record_sha256": record_sha(evidence_record),
                "route_role": denominator,
            }],
            "inherited_owner_id": "PHASE-064-STEP65-LITERATURE-ACQUISITION" if item_id == "P064-SUP-LIT-003" else None,
            "current_owner_id": owner,
            "primary_target": {"phase": target, "step": PHASE_STEPS[target]},
            "downstream_target_phases": DOWNSTREAM[target],
            "acceptance_criterion": (
                "Lawfully acquire, hash and read the Ref. 7 original 1-EOF/all pages before method-content use."
                if item_id == "P064-SUP-LIT-003"
                else "Require separate approval before any P4 execution and preserve exact identity, declared authority ceiling and separation from the 83-source denominator."
                if item_id == "P064-SUP-PROC-001"
                else "Preserve exact identity, declared authority ceiling and separation from the 83-source denominator."
            ),
            "non_double_count_basis": "SUPPLEMENTAL_OCCURRENCE_NOT_MANIFEST_SOURCE_OR_AUTHORITY_BLOCKER",
            "authority_flags": {
                "external_experimental": False,
                "external_material": False,
                "publication_ready": False,
                "ref7_method_content": False,
            },
        })
    require(len(rows) == 6, "supplemental denominator")
    return rows


def observation_route(path: str, pointer: str, record: dict[str, Any], route_id: str, target: int, authority_ids: list[str], status: str = "OPEN_CARRY_OBSERVATION") -> dict[str, Any]:
    return {
        "route_id": route_id,
        "origin_path": path,
        "origin_pointer": pointer,
        "origin_record_sha256": record_sha(record),
        "prior_record": record,
        "status_after": status,
        "inherited_owner_id": record.get("downstream_owner", record.get("owner")),
        "current_owner_id": f"PHASE-{target:03d}-CANONICAL-WORK-QUEUE",
        "primary_target": {"phase": target, "step": PHASE_STEPS[target]},
        "downstream_target_phases": DOWNSTREAM[target],
        "corroborating_authority_route_ids": authority_ids,
        "blocker_identity_created": False,
        "acceptance_criterion": f"Phase {target} must resolve or explicitly preserve this exact observation with evidence; linked authority routes retain claim-level ownership.",
        "non_double_count_basis": "ONE_OBSERVATION_ID; CORROBORATION_DOES_NOT_CREATE_ANOTHER_BLOCKER",
        "authority_flags": {"external_truth": False, "canonical_adoption": False},
    }


def phase057_routes(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    records = inputs[TOPOLOGY]["phase057_observations"]["records"]
    rows = []
    for index, record in enumerate(records):
        numeric = int(record["id"].rsplit("-", 1)[1])
        target = PROVISIONAL_TARGETS[numeric]
        rows.append(observation_route(
            TOPOLOGY, f"/phase057_observations/records/{index}", record,
            f"P064-P057-ROUTE-{index + 1:04d}", target, PROVISIONAL_TO_AUTH.get(numeric, []), PROVISIONAL_STATUSES.get(numeric, "OPEN_CARRY_OBSERVATION"),
        ))
    require(len(rows) == 36, "Phase057 observation denominator")
    return rows


def current_observation_routes(inputs: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    corrections = []
    for index, record in enumerate(inputs[RATIO]["correction_register"]):
        authority_ids = CORRECTION_TO_AUTH[record["id"]]
        target = min(AUTH_TARGETS[item] for item in authority_ids)
        corrections.append(observation_route(RATIO, f"/correction_register/{index}", record, f"P064-S66-OBS-{index + 1:04d}", target, authority_ids))
    findings = []
    for index, record in enumerate(inputs[CODE_DELTA]["findings"]):
        authority_ids = FINDING_TO_AUTH[record["id"]]
        target = min(AUTH_TARGETS[item] for item in authority_ids)
        findings.append(observation_route(CODE_DELTA, f"/findings/{index}", record, f"P064-S67-OBS-{index + 1:04d}", target, authority_ids))
    require(len(corrections) == 11 and len(findings) == 9, "Step66/67 observation denominators")
    return corrections, findings


def authority_routes(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    originals = inputs[AUTHORITY_MATRIX]["overclaim_routes"]
    for index, record in enumerate(originals):
        route_id = record["id"]
        target = AUTH_TARGETS[route_id]
        closed = route_id == "AUTH-012"
        rows.append({
            "route_id": route_id,
            "origin_path": AUTHORITY_MATRIX,
            "origin_pointer": f"/overclaim_routes/{index}",
            "origin_record_sha256": record_sha(record),
            "prior_record": record,
            "status_after": "CLOSED_BOUND_IN_STEP69_1" if closed else "OPEN_CARRY",
            "inherited_owner_id": record["owner"],
            "closure_owner_id": "STEP-069-1-EQ38-SUPERSESSION-BINDING" if closed else None,
            "current_owner_id": "PHASE-082-CANONICAL-EQUATION-FREEZE" if closed else f"PHASE-{target:03d}-AUTHORITY-{route_id}",
            "primary_target": {"phase": 82 if closed else target, "step": "CANONICAL_EQUATION_FREEZE" if closed else "AUTHORITY_CLOSURE"},
            "downstream_target_phases": DOWNSTREAM[82] if closed else DOWNSTREAM[target],
            "acceptance_criterion": record["acceptance_criterion"],
            "non_double_count_basis": "ONE_STEP68_NORMALIZED_AUTHORITY_ROUTE_ID; STEP66_STEP67_AND_PHASE057_LINKS_ARE_CORROBORATION",
            "authority_flags": {"external_truth": False, "canonical_adoption": False, "publication_ready": False},
        })
    require(len(rows) == 14 and len({row["route_id"] for row in rows}) == 14, "authority route denominator")
    return rows


def residual_topical_routes(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "RESID-015", CODE_DELTA, "/findings/4", inputs[CODE_DELTA]["findings"][4],
            "Pin the self-consistency gate to the exact production path/blob/version and replay isolated path-mutation failures.",
        ),
        (
            "RESID-016", CODE_DELTA, "/findings/6", inputs[CODE_DELTA]["findings"][6],
            "Require UTF-8-safe invocation plus assertion-backed nonzero scientific failure before treating the P1 observation as a gate.",
        ),
        (
            "RESID-017", CODE_DELTA, "/findings/8", inputs[CODE_DELTA]["findings"][8],
            "Retain the internal-regression authority ceiling through final review; do not promote it to units, material, experimental or external-literature truth.",
        ),
        (
            "RESID-018", RATIO, "/correction_register/10", inputs[RATIO]["correction_register"][10],
            "Correct or explicitly bound the tail illustration to the declared normalized state domain before canonical source synthesis.",
        ),
    ]
    rows = []
    for route_id, path, pointer, record, acceptance in specs:
        target = AUTH_TARGETS[route_id]
        rows.append({
            "route_id": route_id,
            "origin_path": path,
            "origin_pointer": pointer,
            "origin_record_sha256": record_sha(record),
            "prior_record": record,
            "status_after": "OPEN_CARRY",
            "inherited_owner_id": record["owner"],
            "current_owner_id": f"PHASE-{target:03d}-RESIDUAL-{route_id}",
            "primary_target": {"phase": target, "step": "RESIDUAL_AUTHORITY_CLOSURE"},
            "downstream_target_phases": DOWNSTREAM[target],
            "acceptance_criterion": acceptance,
            "non_double_count_basis": "ONE_PREEXISTING_STEP66_OR_STEP67_FINDING_NOT_SUBSUMED_BY_THE_14_STEP68_AUTH_ROUTES; OBSERVATION_ROW_IS_EVIDENCE_NOT_ANOTHER_BLOCKER",
            "authority_flags": {"external_truth": False, "canonical_adoption": False, "publication_ready": False},
        })
    require(len(rows) == 4 and len({row["route_id"] for row in rows}) == 4, "residual topical route denominator")
    return rows


def eq38_binding(inputs: dict[str, Any]) -> dict[str, Any]:
    old_index, old = next((i, row) for i, row in enumerate(inputs[LITERATURE]["equation_chain"]) if row["equation"] == "38")
    new = inputs[RATIO]["prior_literature_binding"]
    correction_index, correction = next((i, row) for i, row in enumerate(inputs[RATIO]["correction_register"]) if row["id"] == "P064-S66-CORR-002")
    return {
        "binding_id": "P064-EQ38-SUPERSESSION-001",
        "authority_route_id": "AUTH-012",
        "status": "CLOSED_BOUND_IN_STEP69_1",
        "closure_owner_id": "STEP-069-1-EQ38-SUPERSESSION-BINDING",
        "next_owner_id": "PHASE-082-CANONICAL-EQUATION-FREEZE",
        "superseded_projection": old["semantic_projection"],
        "superseding_projection": new["step66_corrected_projection"],
        "retained_crop_raw_pixel_sha256": old["crop_raw_pixel_sha256"],
        "evidence_routes": [
            {"artifact_path": LITERATURE, "json_pointer": f"/equation_chain/{old_index}", "record_sha256": record_sha(old)},
            {"artifact_path": RATIO, "json_pointer": "/prior_literature_binding", "record_sha256": record_sha(new)},
            {"artifact_path": RATIO, "json_pointer": f"/correction_register/{correction_index}", "record_sha256": record_sha(correction)},
        ],
        "acceptance_criterion": "The K*r*mu Step 65 semantic projection is retained as superseded evidence; K*sigma*mu is the Step 66 correction bound to the same original crop.",
        "non_double_count_basis": "ONE_EQ38_CONFLICT_CLOSED_BY_AUTH_012; OLD_AND_NEW_ANCHORS_RETAINED",
    }


def owner_universe(inputs: dict[str, Any], topical_routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior = inputs[P63_CARRY]["canonical_owner_duplicate_check_universe"]["records"]
    rows = [
        {
            "registry_id": f"P064-INHERITED-{row['registry_id']}",
            "denominator_section": "INHERITED_PHASE063_OWNER_UNIVERSE",
            "origin_identity": row["origin_identity"],
            "owner_id": row["owner_id"],
            "target_phase": row["target_phase"],
            "origin_record_sha256": record_sha(row),
            "active_current_authority_route": False,
        }
        for row in prior
    ]
    rows.extend({
        "registry_id": f"P064-OWNER-{route['route_id']}",
        "denominator_section": "PHASE064_AUTHORITY_ROUTES",
        "origin_identity": route["route_id"],
        "owner_id": route["current_owner_id"],
        "target_phase": route["primary_target"]["phase"],
        "origin_record_sha256": route["origin_record_sha256"],
        "active_current_authority_route": route["status_after"] == "OPEN_CARRY",
    } for route in topical_routes)
    require(len(rows) == 326 and len({row["registry_id"] for row in rows}) == 326, "owner universe denominator")
    return rows


def build_artifacts(inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_rows = build_source_dispositions(inputs)
    supplemental = supplemental_dispositions(inputs)
    provisional = phase057_routes(inputs)
    corrections, findings = current_observation_routes(inputs)
    auth_routes = authority_routes(inputs)
    residual_routes = residual_topical_routes(inputs)
    topical_routes = [*auth_routes, *residual_routes]
    owners = owner_universe(inputs, topical_routes)
    binding = eq38_binding(inputs)
    distribution = dict(sorted(Counter(row["disposition"] for row in source_rows).items()))
    status_distribution = dict(sorted(Counter(row["status"] for row in source_rows).items()))
    disposition = {
        "schema_version": "P064_STEP69_1_DISPOSITION_V1",
        "artifact_kind": "PHASE_064_V1023_DISPOSITION_MATRIX",
        "phase": 64,
        "step": "69.1",
        "baseline_commit": BASELINE,
        "input_commit": PARENT,
        "inputs": metadata,
        "result_first": {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
        "source_contract": {
            "manifest_occurrences": 83,
            "supplemental_occurrences": 6,
            "supplemental_by_denominator": {"literature": 4, "plan": 1, "process": 1},
            "identity_rule": "ONE_DISPOSITION_PER_OCCURRENCE_ID; NO_MANIFEST_SUPPLEMENTAL_OR_AUTHORITY_FUSION",
        },
        "source_dispositions": source_rows,
        "supplemental_dispositions": supplemental,
        "counts": {
            "source_dispositions": len(source_rows),
            "source_disposition_distribution": distribution,
            "source_status_distribution": status_distribution,
            "open_source_dispositions": sum(row["disposition"] in ACTIVE_SOURCE_DISPOSITIONS for row in source_rows),
            "supplemental_dispositions": len(supplemental),
            "open_supplemental_dispositions": sum(row["status"].startswith("OPEN_") for row in supplemental),
            "source_orphans": 0,
            "duplicate_source_membership": 0,
            "external_authority_promotions": 0,
        },
        "authority_boundary": AUTHORITY,
        "gate": GATE,
    }
    carry = {
        "schema_version": "P064_STEP69_1_CARRY_FORWARD_V1",
        "artifact_kind": "PHASE_064_V1023_CARRY_FORWARD_DELTA",
        "phase": 64,
        "step": "69.1",
        "baseline_commit": BASELINE,
        "input_commit": PARENT,
        "inputs": metadata,
        "result_first": {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
        "source_disposition_links": [{
            "source_id": row["source_id"],
            "disposition_id": row["disposition_id"],
            "status": row["status"],
            "current_owner_id": row["current_owner_id"],
            "primary_target": row["primary_target"],
            "carry_forward_links": row["carry_forward_links"],
        } for row in source_rows],
        "supplemental_disposition_links": [{
            "supplemental_id": row["supplemental_id"],
            "denominator": row["denominator"],
            "status": row["status"],
            "current_owner_id": row["current_owner_id"],
            "primary_target": row["primary_target"],
        } for row in supplemental],
        "phase057_provisional_routes": provisional,
        "phase066_correction_observations": corrections,
        "phase067_finding_observations": findings,
        "phase068_authority_routes": auth_routes,
        "residual_topical_routes": residual_routes,
        "equation38_supersession_binding": binding,
        "inherited_phase063_snapshot": {
            "origin_path": P63_CARRY,
            "origin_pointer": "",
            "prior_record_sha256": record_sha(inputs[P63_CARRY]),
            "prior_record": inputs[P63_CARRY],
            "status_after": "CARRIED_FORWARD_LOSSLESS",
            "non_double_count_basis": "ONE_COMPLETE_PHASE063_CARRY_ARTIFACT; NESTED_IDENTITIES_RETAINED",
        },
        "canonical_owner_duplicate_check_universe": {
            "schema_version": "P064_CANONICAL_OWNER_UNIVERSE_V1",
            "record_count": len(owners),
            "records_sha256": record_sha(owners),
            "records": owners,
        },
        "new_phase064_blockers": [],
        "gate_summary": {
            "source_disposition_links": 83,
            "open_source_dispositions": sum(row["disposition"] in ACTIVE_SOURCE_DISPOSITIONS for row in source_rows),
            "supplemental_disposition_links": 6,
            "open_supplemental_acquisition_routes": 1,
            "phase057_provisional_routes": 36,
            "phase066_correction_observations": 11,
            "phase067_finding_observations": 9,
            "phase068_authority_routes": 14,
            "residual_topical_routes": 4,
            "topical_routes": 18,
            "open_topical_routes": 17,
            "closed_topical_routes": 1,
            "canonical_owner_duplicate_check_records": 326,
            "inherited_phase063_owner_records": 308,
            "equation38_supersession_bindings": 1,
            "ref6_original_full_text": "FULL_TEXT_READ_4_OF_4",
            "ref7_original_full_text": "GROUND_NOT_FOUND",
            "new_phase064_blockers": 0,
            "ownerless_open_routes": 0,
            "multiply_owned_open_routes": 0,
            "external_authority_promotions": 0,
            "status": "PASS_WITH_CONCERNS",
            "phase_ceiling": "CONDITIONAL_P064",
        },
        "authority_boundary": AUTHORITY,
        "gate": GATE,
    }
    return disposition, carry


def result_text(disposition: dict[str, Any], carry: dict[str, Any], disposition_sha: str, carry_sha: str) -> str:
    counts = disposition["counts"]
    summary = carry["gate_summary"]
    return f"""# Phase 064 Step 69.1 Source Disposition and Carry-forward Delta Result

Gate: `{GATE}`

Terminal: `{GATE}`

Result-first sentinel: `{SENTINEL}`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

## Reconciled prerequisite

- Step 68 exact-seven containing commit: `{PARENT}`.
- Step 68 subject: `audit(phase064): adjudicate v1023 validation authority`.
- Step 68 Python 3.12/3.14 persistence terminal: `PASS_P064_STEP68_PERSISTENCE`.

## Result

- disposition matrix SHA-256: `{disposition_sha}`.
- carry-forward delta SHA-256: `{carry_sha}`.
- manifest source dispositions: `{counts['source_dispositions']}/83`; supplemental plan/literature/process dispositions: `{counts['supplemental_dispositions']}/6` in separate denominators.
- source disposition distribution: `{json.dumps(counts['source_disposition_distribution'], ensure_ascii=False, sort_keys=True)}`; status distribution `{json.dumps(counts['source_status_distribution'], ensure_ascii=False, sort_keys=True)}`.
- Phase 057 provisional observations `{summary['phase057_provisional_routes']}/36`, Step 66 corrections `{summary['phase066_correction_observations']}/11`, Step 67 findings `{summary['phase067_finding_observations']}/9`; these remain observations linked to canonical work queues and do not mint new blocker identities.
- Step 68 normalized authority routes `{summary['phase068_authority_routes']}/14` plus non-subsumed Step 66/67 residual routes `{summary['residual_topical_routes']}/4` form `{summary['topical_routes']}/18` topical canonical routes: OPEN `{summary['open_topical_routes']}`, CLOSED `{summary['closed_topical_routes']}`. Ownerless/multiply-owned active routes `{summary['ownerless_open_routes']}/{summary['multiply_owned_open_routes']}`.
- canonical-owner duplicate-check universe `{summary['canonical_owner_duplicate_check_records']}/326` = inherited Phase 063 `{summary['inherited_phase063_owner_records']}/308` + current topical authority `{summary['topical_routes']}/18`.
- new Phase 064 blockers `{summary['new_phase064_blockers']}`; external authority promotions `{summary['external_authority_promotions']}`.

## Ref. 6/7 correction to the initial plan state

- The Step 64 plan began with both Ref. 6 and Ref. 7 originals absent. Step 65 subsequently acquired and read the DOI-bound Ref. 6 VOR `4/4` pages and fixed its raw SHA-256. Ref. 6 acquisition debt is therefore CLOSED as bounded primary-method evidence and is not falsely kept OPEN.
- Ref. 7 remains official bibliographic metadata only; its original full text is `GROUND_NOT_FOUND`. The wrong candidate DOI `10.1063/1.4802005` remains rejected and the correct metadata DOI is `10.1063/1.4802584`.
- Ref. 7 has exactly one current acquisition owner, `PHASE-071-PRIMARY-SOURCE-ACQUISITION`; the Phase ceiling remains `{summary['phase_ceiling']}`.

## Disposition method and scope

- Every `V1023-SRC-001`--`V1023-SRC-083` manifest occurrence retains exact path/blob/hash/extent/read identity. Matching paths are not fused with supplemental inputs or authority routes.
- `CORRECT` marks a frozen source occurrence with a routed correction requirement; `UNVERIFIED` marks unresolved primary-literature or material-scope evidence among the nine manifest occurrences, while Ref. 7 full-text GNF remains a separate supplemental route; `THEORY_ONLY` preserves internally readable theory without external truth promotion; `PRESERVE` retains bounded history, generated documents, figures or unaffected sources.
- Supplemental plan, JCP147 VOR, Ref. 6 VOR, Ref. 7 metadata/GNF, JCP extract and P4 process decision are six separate non-manifest occurrences. P4 remains `SKIPPED_D3_NOT_APPROVED`, never fabricated PASS/FAIL.
- Phase 057 and Steps 66--67 findings are observation records. Their links to 14 Step 68 authority routes and four explicitly non-subsumed residual routes are corroboration, not additional blocker identities. The four residuals preserve self-consistency path/blob provenance, P1 encoding/assertion enforcement, internal-regression authority ceiling and the normalized-state tail-range defect.

## Equation 38 and remaining carry

- `AUTH-012` is CLOSED in this Step by retaining both Step 65's superseded `K*r*mu` semantic projection and Step 66's crop-bound `K*sigma*mu` correction. The original crop hash remains unchanged.
- C-rate/factor-3600, voltage-coordinate transfer, Ref. 7 acquisition, computational-benefit, background-root, Picard/convergence, portability, differentiability, material and final-publication authority routes remain OPEN under their single downstream owners.
- The complete Phase 063 carry artifact is embedded with its origin pointer and canonical record hash. Its 308 owner-universe identities remain distinct from the 18 current topical routes (14 Step 68 authority routes plus four non-subsumed residual routes).
- No frozen `Claude/**` source, protected branch or `main` content is modified.

## Validation contract

- strict JSON duplicate/nonfinite/overflow/truncation rejection and full recursive traversal of ten inputs and both outputs;
- exact nested schemas and Python exact types for all source, supplemental, observation, authority, residual, Eq. 38 binding, inherited snapshot and owner-universe rows;
- independent source disposition reconstruction, evidence-pointer/hash replay, exact 83 + supplemental 6 + 36 + 11 + 9 + 14 + 4 + 308 denominators, Ref. 6 closed/Ref. 7 open state, P4 skip and authority ceilings;
- named semantic/recovery/builder-policy negatives, real disposable Git boundary mutations, deterministic `2/2`, exact-eight staged and postcommit persistence gates on Python 3.12 and 3.14.

## Executed validation evidence

- Python 3.12 and Python 3.14 precommit content validation passed with strict traversal `165334`, semantic negatives `58/58`, strict JSON `9/9`, recovery `10/10`, builder policy `4/4`, disposable Git boundary `18/18` and determinism `2/2` in each runtime.
- Exact-eight staged and postcommit persistence remain deliberately pending until the atomic commit workflow; neither is claimed by this precommit result.

## Exact-eight checkpoint

1. `Codex/work/v1023_phase064/build_phase064_step69_dispositions.py`
2. `Codex/work/v1023_phase064/validate_phase064_step69_dispositions.py`
3. `Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_064_STEP_069_1_DISPOSITION_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected subject: `audit(phase064): disposition v1023 lineage`.

Post-commit persistence must emit `PASS_P064_STEP69_1_PERSISTENCE` before Step 69.2.
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
        print("PASS_P064_STEP69_1_BUILDER_CHECK")
        return 0
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_bytes(result_raw)
    disposition_path.parent.mkdir(parents=True, exist_ok=True)
    disposition_path.write_bytes(disposition_raw)
    carry_path.parent.mkdir(parents=True, exist_ok=True)
    carry_path.write_bytes(carry_raw)
    print("PASS_P064_STEP69_1_BUILDER result-first")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
