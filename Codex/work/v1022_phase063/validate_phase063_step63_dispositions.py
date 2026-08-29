#!/usr/bin/env python3
"""Fail-closed validation for Phase 063 Step 63.1 disposition routing."""

from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any, Callable


REPO = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "eb847ea85018b7703c7adcfe74b8b665ec8c9b1c"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
SUBJECT = "audit(phase063): disposition v1022 lineage"
GATE = "PASS_P063_STEP63_1_DISPOSITIONS"
PERSISTENCE = "PASS_P063_STEP63_1_PERSISTENCE"
SENTINEL = "P063_STEP63_1_RESULT_FIRST_PRECOMMIT"

BUILDER = "Codex/work/v1022_phase063/build_phase063_step63_dispositions.py"
VALIDATOR = "Codex/work/v1022_phase063/validate_phase063_step63_dispositions.py"
DISPOSITION = "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json"
CARRY = "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json"
RESULT = "Codex/results/PHASE_063_STEP_063_1_DISPOSITION_RESULT.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXACT_PATHS = [BUILDER, VALIDATOR, DISPOSITION, CARRY, RESULT, ACTIVE_LEDGER, PARENT_LEDGER, HANDOVER]

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
BUILDER_RAW_SHA256 = "27b3396c950e3f953b667fd4c16146f84702223ca950d22327b92ed293a9b234"
BUILDER_AST_SHA256 = "e66d75ca22c49de848a229519e0926a5ae8ce1b9c2940ab49878e5d207609660"
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
TARGETS = set(range(70, 91))
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


class ValidationError(RuntimeError):
    """Fail-closed Step 63.1 error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def run_git(*args: str, text: bool = True, cwd: pathlib.Path = REPO) -> str | bytes:
    process = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=text,
        encoding="utf-8" if text else None, errors="strict" if text else None,
        timeout=120, check=True,
    )
    return process.stdout


@functools.lru_cache(maxsize=None)
def git_bytes(revision: str, path: str) -> bytes:
    return run_git("show", f"{revision}:{path}", text=False)  # type: ignore[return-value]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def strict_load_bytes(raw: bytes) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            require(key not in result, f"E_JSON_DUPLICATE_KEY:{key}")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{value}")

    def finite(value: str) -> float:
        parsed = float(value)
        require(math.isfinite(parsed), f"E_JSON_NONFINITE:{value}")
        return parsed

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant, parse_float=finite)
    except UnicodeDecodeError as exc:
        raise ValidationError(f"E_JSON_UTF8:{exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"E_JSON_SYNTAX:{exc.msg}") from exc


def strict_load(path: pathlib.Path) -> Any:
    return strict_load_bytes(path.read_bytes())


def traversal_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + len(value) + sum(traversal_count(child) for child in value.values())
    if isinstance(value, list):
        return 1 + sum(traversal_count(child) for child in value)
    if isinstance(value, float):
        require(math.isfinite(value), "E_TRAVERSAL_NONFINITE")
    return 1


def pointer_value(document: Any, pointer: str) -> Any:
    value = document
    for token in pointer.lstrip("/").split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    objects: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for path, expected_sha in INPUT_SHA256.items():
        raw = git_bytes(PARENT, path)
        require(sha256(raw) == expected_sha, f"E_INPUT_SHA:{path}")
        require((REPO / path).read_bytes() == raw, f"E_INPUT_WORKTREE:{path}")
        objects[path] = strict_load_bytes(raw)
        metadata.append({
            "path": path, "commit": PARENT,
            "git_blob": str(run_git("rev-parse", f"{PARENT}:{path}")).strip(),
            "sha256": expected_sha, "bytes": len(raw), "parse_mode": "STRICT_JSON_FULL_TRAVERSAL",
        })
    return objects, metadata


def portable_ast_value(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"node": type(value).__name__, "fields": {name: portable_ast_value(child) for name, child in ast.iter_fields(value) if name != "type_params"}}
    if isinstance(value, list):
        return [portable_ast_value(child) for child in value]
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    return value


def portable_ast_sha(raw: bytes) -> str:
    tree = ast.parse(raw.decode("utf-8"), filename=BUILDER)
    packed = json.dumps(portable_ast_value(tree), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(packed)


def validate_builder_policy(candidate: bytes | None = None, *, raw_pin: bool = True, ast_pin: bool = True) -> None:
    raw = (REPO / BUILDER).read_bytes() if candidate is None else candidate
    if raw_pin:
        require(sha256(raw) == BUILDER_RAW_SHA256, "E_BUILDER_RAW_SHA256")
    tree = ast.parse(raw.decode("utf-8"), filename=BUILDER)
    if ast_pin:
        require(portable_ast_sha(raw) == BUILDER_AST_SHA256, "E_BUILDER_AST_SHA256")
    allowed = {"__future__", "argparse", "hashlib", "json", "math", "pathlib", "re", "subprocess", "collections", "typing"}
    imports: set[str] = set()
    subprocess_calls: list[ast.Call] = []
    git_node: ast.AST | None = None
    forbidden: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
            forbidden.append(node.func.id)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
            subprocess_calls.append(node)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "git_bytes":
            require(git_node is None, "E_BUILDER_GIT_FUNCTION_DUPLICATE")
            git_node = node
    require(imports <= allowed, f"E_BUILDER_IMPORT_POLICY:{sorted(imports - allowed)}")
    require(not forbidden, f"E_BUILDER_DYNAMIC_EXEC:{forbidden}")
    require(git_node is not None, "E_BUILDER_GIT_FUNCTION_MISSING")
    require(len(subprocess_calls) == 1, f"E_BUILDER_SUBPROCESS_POLICY:{len(subprocess_calls)}")
    call = subprocess_calls[0]
    require(call in set(ast.walk(git_node)), "E_BUILDER_SUBPROCESS_SCOPE")
    require(bool(call.args) and isinstance(call.args[0], ast.List), "E_BUILDER_SUBPROCESS_ARGV")
    values = call.args[0].elts
    require(len(values) == 2 and isinstance(values[0], ast.Constant) and values[0].value == "git" and isinstance(values[1], ast.Starred), "E_BUILDER_SUBPROCESS_ARGV")


def expected_projection() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    with tempfile.TemporaryDirectory(prefix="p063-step63-1-projection-") as tmp:
        root = pathlib.Path(tmp)
        disposition = root / "disposition.json"
        carry = root / "carry.json"
        result = root / "result.md"
        subprocess.run(
            [sys.executable, "-B", str(REPO / BUILDER), "--repo", str(REPO), "--disposition", str(disposition), "--carry", str(carry), "--result", str(result)],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=240, check=True,
        )
        return strict_load(disposition), strict_load(carry), result.read_bytes()


def validate_evidence_route(route: dict[str, Any], inputs: dict[str, Any]) -> Any:
    require(route["artifact_path"] in inputs, f"E_EVIDENCE_PATH:{route['artifact_path']}")
    try:
        record = pointer_value(inputs[route["artifact_path"]], route["json_pointer"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ValidationError(f"E_EVIDENCE_POINTER:{route['artifact_path']}:{route['json_pointer']}") from exc
    require(sha256(compact(record)) == route["record_sha256"], "E_EVIDENCE_RECORD_SHA")
    return record


def independent_disposition(source: dict[str, Any], roles: set[str]) -> str:
    if source["partition"] != "FINAL_RELEASE_SURFACE" or source["role"] == "generated_document":
        return "PRESERVE"
    if source["role"] in {"code", "test", "implementation_guide"}:
        return "CORRECT"
    correction = {"DERIVATION_CORRECTION", "CODE_FINDING_CORRECTION", "CODE_MENTION_CORRECTION", "REVIEW_FINDING_OPEN", "BUILD_DIAGNOSTIC_CORRECTION"}
    if roles & correction:
        return "CORRECT"
    if "LITERATURE_SCOPE_UNVERIFIED" in roles:
        return "UNVERIFIED"
    if "DERIVATION_INTERNAL_THEORY" in roles:
        return "THEORY_ONLY"
    return "PRESERVE"


def expected_corroborating_ids(finding_id: str) -> list[str]:
    return sorted({member for group in AUDIT_CORROBORATION_GROUPS if finding_id in group for member in group if member != finding_id})


def independent_owner_universe(inputs: dict[str, Any], routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior = inputs[P62_CARRY]
    owner_targets = {row["disposition_id"]: row["primary_target_phase"] for row in inputs[P62_DISPOSITION]["release_dispositions"]}
    for row in prior["inherited_carry_items"]:
        owner_targets[row["carry_forward_id"]] = row["target_phase_after"]
    for section in ("inherited_phase060_blockers", "inherited_phase061_blockers"):
        for row in prior[section]: owner_targets[row["blocker_id"]] = row["target_phase_after"]
    for row in prior["canonical_debt_routing"]:
        owner_targets[row["prior_record"]["primary_owner_id"]] = row["prior_record"]["owner_target_phase"]
    records = [{
        "registry_id": f"P063-OWNER-UNIVERSE-F057-{index + 1:04d}", "denominator_section": "PHASE057_FINDING_ROUTES",
        "denominator_index": index, "origin_identity": route["finding_id"], "owner_id": route["canonical_owner_id"],
        "target_phase": route["target_phase"], "origin_record_sha256": route["origin_record_sha256"],
    } for index, route in enumerate(routes)]
    specs = (
        ("inherited_carry_items", "carry_forward_id", lambda row: row["target_phase_after"]),
        ("inherited_phase060_blockers", "blocker_id", lambda row: row["target_phase_after"]),
        ("inherited_phase061_blockers", "blocker_id", lambda row: row["target_phase_after"]),
        ("canonical_debt_routing", None, lambda row: row["prior_record"]["owner_target_phase"]),
        ("open_finding_ownership", "finding_id", lambda row: owner_targets[row["owner_id"]]),
    )
    for section, identity_key, target_getter in specs:
        for index, row in enumerate(prior[section]):
            owner_id = row["prior_record"]["primary_owner_id"] if section == "canonical_debt_routing" else row.get("owner_id", row.get(identity_key or "", ""))
            origin_identity = row[identity_key] if identity_key else row["prior_record"]["debt_id"]
            records.append({
                "registry_id": f"P063-OWNER-UNIVERSE-{section.upper()}-{index + 1:04d}", "denominator_section": section,
                "denominator_index": index, "origin_identity": origin_identity, "owner_id": owner_id,
                "target_phase": target_getter(row), "origin_record_sha256": sha256(compact(row)),
            })
    require(len(records) == 308 and len({row["registry_id"] for row in records}) == 308, "E_OWNER_UNIVERSE_COUNT")
    return records


def validate_semantics(disposition: dict[str, Any], carry: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]], projection: tuple[dict[str, Any], dict[str, Any], bytes]) -> None:
    require(set(disposition) == {"artifact_kind", "authority_boundary", "baseline_commit", "counts", "gate", "input_commit", "inputs", "phase", "result_first", "schema_version", "source_contract", "source_dispositions", "step", "supplemental_process_disposition"}, "E_DISPOSITION_SCHEMA")
    require(set(carry) == {"artifact_kind", "authority_boundary", "baseline_commit", "canonical_debt_routing", "canonical_owner_duplicate_check_universe", "gate", "gate_summary", "inherited_carry_items", "inherited_phase060_blockers", "inherited_phase061_blockers", "input_commit", "inputs", "new_phase063_blockers", "open_finding_ownership", "phase", "phase057_finding_routes", "phase063_audit_finding_routes", "result_first", "schema_version", "source_disposition_links", "step"}, "E_CARRY_SCHEMA")
    require(disposition["schema_version"] == "P063_STEP63_1_DISPOSITION_V1" and carry["schema_version"] == "P063_STEP63_1_CARRY_FORWARD_V1", "E_SCHEMA_VERSION")
    require(disposition["phase"] == carry["phase"] == 63 and disposition["step"] == carry["step"] == "63.1", "E_PHASE_STEP")
    require(disposition["baseline_commit"] == carry["baseline_commit"] == BASELINE and disposition["input_commit"] == carry["input_commit"] == PARENT, "E_INPUT_IDENTITY")
    require(disposition["inputs"] == carry["inputs"] == metadata, "E_INPUT_METADATA")
    require(disposition["gate"] == carry["gate"] == GATE, "E_GATE")
    require(disposition["result_first"] == carry["result_first"] == {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"}, "E_RESULT_FIRST")
    require(disposition["authority_boundary"] == carry["authority_boundary"] == AUTHORITY, "E_AUTHORITY_BOUNDARY")
    require(disposition["source_contract"] == {"manifest_occurrences": 204, "supplemental_process_controls": 1, "identity_rule": "ONE_DISPOSITION_PER_SOURCE_ID; NO_PATH_OR_BLOB_COLLAPSE"}, "E_SOURCE_CONTRACT")

    sources = inputs[TOPOLOGY]["sources"]
    rows = disposition["source_dispositions"]
    require(len(sources) == len(rows) == 204, "E_SOURCE_COUNT")
    require(len({row["source_id"] for row in rows}) == 204 and len({row["disposition_id"] for row in rows}) == 204, "E_SOURCE_DUPLICATE")
    expected_distribution = {"CORRECT": 29, "PRESERVE": 160, "THEORY_ONLY": 6, "UNVERIFIED": 9}
    global_evidence_ids: list[str] = []
    for index, (source, row) in enumerate(zip(sources, rows), 1):
        require(row["source_id"] == source["source_id"] and row["disposition_id"] == f"P063-DISP-{index:04d}", "E_SOURCE_ORDER")
        expected_identity = {key: source[key] for key in ("source_id", "path", "blob_sha1", "sha256", "manifest_index", "partition", "role", "review_mode", "extent")}
        require(row["source_identity"] == expected_identity and row["source_record_sha256"] == sha256(compact(source)), "E_SOURCE_IDENTITY")
        require(row["disposition"] in ALLOWED, "E_DISPOSITION_VOCABULARY")
        require(row["evidence_ids"] == [route["evidence_id"] for route in row["evidence_routes"]], "E_EVIDENCE_IDS")
        require(bool(row["evidence_routes"]) and row["evidence_routes"][0]["route_role"] == "SOURCE_IDENTITY", "E_SOURCE_IDENTITY_ROUTE")
        require(row["evidence_routes"][0]["json_pointer"] == f"/sources/{index - 1}", "E_SOURCE_IDENTITY_POINTER")
        for route in row["evidence_routes"]:
            validate_evidence_route(route, inputs)
            global_evidence_ids.append(route["evidence_id"])
        roles = {route["route_role"] for route in row["evidence_routes"]}
        require(row["disposition"] == independent_disposition(source, roles), "E_DISPOSITION_RULE")
        expected_status = "OPEN" if row["disposition"] in {"CORRECT", "UNVERIFIED"} else "PRESERVED_ACTIVE"
        require(row["status"] == expected_status, "E_SOURCE_STATUS")
        require(row["primary_target_phase"] in TARGETS and row["primary_target_phase"] < 90 and row["downstream_target_phases"] == list(range(row["primary_target_phase"] + 1, 91)), "E_SOURCE_TARGET")
        if expected_status == "OPEN":
            require(row["canonical_owner_id"] == f"PHASE-{row['primary_target_phase']:03d}-SOURCE-{row['source_id']}", "E_SOURCE_OWNER")
        else:
            require(row["canonical_owner_id"] is None, "E_SOURCE_OWNER")
        require(bool(row["reason"].strip()) and bool(row["acceptance_criterion"].strip()) and bool(row["authority_ceiling"].strip()), "E_SOURCE_RECOVERY_FIELDS")
        require(row["external_scientific_truth"] is row["external_material_truth"] is row["external_experimental_truth"] is False, "E_SOURCE_AUTHORITY")
    require(len(global_evidence_ids) == len(set(global_evidence_ids)), "E_EVIDENCE_ID_DUPLICATE")
    distribution = dict(sorted(Counter(row["disposition"] for row in rows).items()))
    require(distribution == expected_distribution, "E_DISPOSITION_DISTRIBUTION")
    require(disposition["counts"] == {"source_dispositions": 204, "source_disposition_distribution": expected_distribution, "open_source_dispositions": 38, "supplemental_process_dispositions": 1, "source_orphans": 0, "duplicate_source_membership": 0, "external_authority_promotions": 0}, "E_DISPOSITION_COUNTS")

    supplemental = disposition["supplemental_process_disposition"]
    expected_supplemental = inputs[TOPOLOGY]["supplemental_process_control"]
    require(supplemental["disposition"] == "PRESERVE" and supplemental["manifest_member"] is False and supplemental["denominator"] == "SUPPLEMENTAL_PROCESS_CONTROL", "E_SUPPLEMENTAL_DENOMINATOR")
    require(supplemental["source_anchor"] == {key: expected_supplemental[key] for key in ("path", "blob_sha1", "sha256")}, "E_SUPPLEMENTAL_IDENTITY")
    validate_evidence_route(supplemental["evidence_routes"][0], inputs)
    require(supplemental["external_scientific_truth"] is supplemental["external_material_truth"] is False, "E_SUPPLEMENTAL_AUTHORITY")

    links = carry["source_disposition_links"]
    require(len(links) == 204 and [row["source_id"] for row in links] == [row["source_id"] for row in rows], "E_SOURCE_LINK_COUNT")
    require(all(link["disposition_id"] == row["disposition_id"] and link["status"] == row["status"] and link["primary_target_phase"] == row["primary_target_phase"] and link["carry_forward_links"] == row["carry_forward_links"] for link, row in zip(links, rows)), "E_SOURCE_LINK_PROJECTION")

    findings = inputs[STEP62]["finding_adjudications"]
    routes = carry["phase057_finding_routes"]
    require(len(findings) == len(routes) == 96 and len({row["finding_id"] for row in routes}) == 96, "E_PHASE057_COUNT")
    state_counts = Counter(row["state_before"] for row in routes)
    require(state_counts == Counter({"HISTORICAL_ONLY": 30, "OPEN": 45, "RESOLVED_IN_V1022": 8, "SUPERSEDED": 2, "UNVERIFIED": 11}), "E_PHASE057_STATES")
    active_owners: list[str] = []
    for index, (finding, route) in enumerate(zip(findings, routes), 1):
        require(route["route_id"] == f"P063-F057-ROUTE-{index:04d}" and route["finding_id"] == finding["finding_id"] and route["numeric_id"] == finding["numeric_id"], "E_PHASE057_IDENTITY")
        require(route["origin_path"] == STEP62 and route["origin_pointer"] == f"/finding_adjudications/{index - 1}" and route["origin_record_sha256"] == sha256(compact(finding)), "E_PHASE057_ORIGIN")
        validate_evidence_route(route["evidence_routes"][0], inputs)
        require(route["state_before"] == finding["state"] and route["acceptance_criterion"] == finding["acceptance_criterion"], "E_PHASE057_CONTENT")
        active = finding["state"] in ACTIVE_STATES
        expected_target = PHASE057_PRIMARY_TARGETS[finding["numeric_id"]] if active else 70
        require(route["target_phase"] == expected_target and route["downstream_target_phases"] == list(range(expected_target + 1, 91)), "E_PHASE057_TARGET")
        if active:
            require(route["status_after"] == "OPEN_CARRY" and route["canonical_owner_id"] == f"PHASE-{expected_target:03d}-{finding['finding_id']}", "E_PHASE057_OWNER")
            active_owners.append(route["canonical_owner_id"])
        else:
            require(route["status_after"] == "RESOLVED_INFORMATIONAL" and route["canonical_owner_id"] == "PHASE-070-HISTORICAL-EVIDENCE-QUEUE", "E_PHASE057_RESOLUTION")
        require(bool(route["non_double_count_basis"]) and route["external_truth"] is False, "E_PHASE057_AUTHORITY")
    require(len(active_owners) == len(set(active_owners)) == 56, "E_PHASE057_OWNER_DUPLICATE")

    expected_universe = independent_owner_universe(inputs, routes)
    universe = carry["canonical_owner_duplicate_check_universe"]
    require(universe["schema_version"] == "P063_CANONICAL_OWNER_UNIVERSE_V1" and universe["record_count"] == 308, "E_OWNER_UNIVERSE_COUNT")
    require(universe["records"] == expected_universe and universe["records_sha256"] == sha256(compact(expected_universe)), "E_OWNER_UNIVERSE_IDENTITY")

    audit_inputs = [(STEP59, inputs[STEP59]["findings"]), (STEP60, inputs[STEP60]["findings"]), (STEP61_CODE, inputs[STEP61_CODE]["findings"])]
    expected_audit = [(path, index, finding) for path, group in audit_inputs for index, finding in enumerate(group)]
    audit = carry["phase063_audit_finding_routes"]
    require(len(audit) == len(expected_audit) == 59 and Counter(row["priority"] for row in audit) == Counter({"P0": 13, "P1": 25, "P2": 21}), "E_AUDIT_COUNT")
    for ordinal, (route, (path, index, finding)) in enumerate(zip(audit, expected_audit), 1):
        require(route["route_id"] == f"P063-AUDIT-ROUTE-{ordinal:04d}" and route["finding_id"] == finding["finding_id"] and route["priority"] == finding["priority"], "E_AUDIT_IDENTITY")
        require(route["origin_path"] == path and route["origin_pointer"] == f"/findings/{index}" and route["origin_record_sha256"] == sha256(compact(finding)), "E_AUDIT_ORIGIN")
        owner_text = str(finding.get("owner", finding.get("downstream_owner", "")))
        explicit_targets = [int(value) for value in re.findall(r"Phase\s+0*(7[0-9]|8[0-9]|90)", owner_text)]
        expected_target = min(explicit_targets) if explicit_targets else 82
        require(route["status_after"] == "OPEN_CARRY" and route["target_phase"] == expected_target and route["downstream_target_phases"] == list(range(expected_target + 1, 91)), "E_AUDIT_TARGET")
        require(route["canonical_owner_id"] == f"PHASE-{expected_target:03d}-CANONICAL-WORK-QUEUE" and route["owner_kind"] == "EXISTING_PHASE_QUEUE_NOT_NEW_BLOCKER", "E_AUDIT_OWNER")
        expected_exact = [row["registry_id"] for row in expected_universe if finding["finding_id"] in {row["origin_identity"], row["owner_id"]}]
        expected_same_target = [row["registry_id"] for row in expected_universe if row["target_phase"] == expected_target]
        require(route["duplicate_check"] == {"owner_universe_schema": "P063_CANONICAL_OWNER_UNIVERSE_V1", "owner_universe_records": 308, "owner_universe_sha256": sha256(compact(expected_universe)), "exact_prior_identity_matches": expected_exact, "same_target_existing_owner_candidates": expected_same_target, "match_interpretation": "EXACT_IDENTITY_ONLY; SAME_TARGET_IS_CANDIDATE_NOT_EQUIVALENCE", "decision": "NOT_CREATED_AUDIT_OBSERVATION_ONLY"}, "E_AUDIT_DUPLICATE_CHECK")
        require(route["corroborating_audit_finding_ids"] == expected_corroborating_ids(finding["finding_id"]) and route["blocker_identity_created"] is False, "E_AUDIT_CORROBORATION")
        require(route["external_truth"] is False and bool(route["acceptance_criterion"]) and bool(route["non_double_count_basis"]), "E_AUDIT_AUTHORITY")

    prior = inputs[P62_CARRY]
    inherited_specs = [("inherited_carry_items", 52), ("inherited_phase060_blockers", 5), ("inherited_phase061_blockers", 5), ("canonical_debt_routing", 91), ("open_finding_ownership", 59)]
    for key, count in inherited_specs:
        wrapped = carry[key]
        require(len(wrapped) == len(prior[key]) == count, f"E_INHERITED_COUNT:{key}")
        for index, (route, old) in enumerate(zip(wrapped, prior[key])):
            require(route["origin_path"] == P62_CARRY and route["origin_pointer"] == f"/{key}/{index}" and route["prior_record"] == old and route["prior_record_sha256"] == sha256(compact(old)), f"E_INHERITED_LOSS:{key}")
            require(route["status_after"] == "CARRIED_FORWARD_UNCHANGED" and 64 <= route["target_phase_after"] <= 90, f"E_INHERITED_ROUTE:{key}")
    require(carry["new_phase063_blockers"] == [], "E_NEW_BLOCKER")
    require(carry["gate_summary"] == {"source_disposition_links": 204, "phase057_finding_routes": 96, "phase057_open_or_unverified": 56, "phase063_audit_finding_routes": 59, "canonical_owner_duplicate_check_records": 308, "audit_exact_prior_identity_matches": 0, "inherited_carry_items": 52, "inherited_phase060_blockers": 5, "inherited_phase061_blockers": 5, "canonical_debt_routes": 91, "phase062_open_finding_routes": 59, "new_phase063_blockers": 0, "ownerless_open_routes": 0, "multiply_owned_open_routes": 0, "external_authority_promotions": 0, "status": "PASS_WITH_CONCERNS"}, "E_GATE_SUMMARY")
    require(canonical(disposition) == canonical(projection[0]) and canonical(carry) == canonical(projection[1]), "E_EXACT_PROJECTION")


def validate_recovery_texts(result: str, active: str, parent: str, handover: str, disposition_sha: str, carry_sha: str) -> None:
    result_lines = result.splitlines()
    require([line for line in result_lines if line.startswith("Gate:")] == [f"Gate: `{GATE}`"], "E_RESULT_GATE_SURFACE")
    require([line for line in result_lines if line.startswith("Terminal:")] == [f"Terminal: `{GATE}`"], "E_RESULT_GATE_SURFACE")
    require([line for line in result_lines if line.startswith("Result-first sentinel:")] == [f"Result-first sentinel: `{SENTINEL}`"], "E_RESULT_GATE_SURFACE")
    require([line for line in result_lines if line.startswith("Containing commit:")] == ["Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`"], "E_RESULT_GATE_SURFACE")
    require(not re.search(r"(?im)^(?:overall status|status|gate|terminal):.*(?:\bFAIL(?:_P063)?\b|\bCONDITIONAL(?:_P063)?\b)", result), "E_RESULT_GATE_SURFACE")
    require(SENTINEL in result and PARENT in result and disposition_sha in result and carry_sha in result, "E_RESULT_RECOVERY")
    require(result.count("P0/P1/P2=13/25/21") == 1 and "204/204" in result and "96/96" in result, "E_RESULT_DENOMINATORS")
    require(result.count("strict traversal `1,133,555` nodes per run") == 1, "E_RESULT_VALIDATION_EVIDENCE")
    require(result.count("named negative validation: `65/65`; strict JSON `6/6`, recovery `10/10`, builder policy `4/4`, Git-boundary mutations `10/10` per runtime") == 1, "E_RESULT_VALIDATION_EVIDENCE")
    active_rows = [line for line in active.splitlines() if line.startswith("| 063 | 58–63 |")]
    active_step_rows = [line for line in active.splitlines() if line.startswith("| Step 63.1 |")]
    parent_rows = [line for line in parent.splitlines() if line.startswith("| 063 | 58–63 |")]
    handover_rows = [line for line in handover.splitlines() if line.startswith("| Phase 063 Step 63.1 |")]
    require(len(active_rows) == 1, "E_ACTIVE_LEDGER_ROW_COUNT")
    require(len(active_step_rows) == 1, "E_ACTIVE_STEP_LEDGER_ROW_COUNT")
    require(len(parent_rows) == 1, "E_PARENT_LEDGER_ROW_COUNT")
    require(len(handover_rows) == 1, "E_HANDOVER_ROW_COUNT")
    active_row, active_step_row, parent_row, handover_row = active_rows[0], active_step_rows[0], parent_rows[0], handover_rows[0]
    contradiction = re.compile(r"\bFAIL(?:_P063)?\b|\bCONDITIONAL(?:_P063)?\b")
    required_row_tokens = (GATE, PARENT, SUBJECT, SENTINEL, disposition_sha, carry_sha, "PENDING_AT_PRECOMMIT_BY_DESIGN")
    require("Step 63.1 precommit" in active_row and all(active_row.count(token) == 1 for token in required_row_tokens) and not contradiction.search(active_row), "E_ACTIVE_LEDGER_RECOVERY")
    require(all(active_step_row.count(token) == 1 for token in required_row_tokens) and not contradiction.search(active_step_row), "E_ACTIVE_STEP_LEDGER_RECOVERY")
    require("Step 63.1 precommit" in parent_row and all(parent_row.count(token) == 1 for token in required_row_tokens) and not contradiction.search(parent_row), "E_PARENT_LEDGER_RECOVERY")
    require(all(handover_row.count(token) == 1 for token in required_row_tokens) and not contradiction.search(handover_row), "E_HANDOVER_RECOVERY")
    require(f"16. 현재 result: `{RESULT}`" in handover and DISPOSITION in handover and CARRY in handover and "Steps 58–62 evidence" in handover, "E_HANDOVER_CURRENT_SURFACES")
    for text, diagnostic in ((active, "E_ACTIVE_LEDGER_DETAIL"), (parent, "E_PARENT_LEDGER_DETAIL"), (handover, "E_HANDOVER_DETAIL")):
        require(disposition_sha in text and carry_sha in text and SENTINEL in text and SUBJECT in text, diagnostic)


def validate_result_and_recovery() -> None:
    process = subprocess.run([sys.executable, "-B", str(REPO / BUILDER), "--repo", str(REPO), "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=240, check=True)
    require("PASS_P063_STEP63_1_BUILDER_CHECK" in process.stdout, "E_BUILDER_CHECK_TERMINAL")
    validate_recovery_texts(
        (REPO / RESULT).read_text(encoding="utf-8"),
        (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8"),
        (REPO / PARENT_LEDGER).read_text(encoding="utf-8"),
        (REPO / HANDOVER).read_text(encoding="utf-8"),
        sha256((REPO / DISPOSITION).read_bytes()), sha256((REPO / CARRY).read_bytes()),
    )


def validate_staged_snapshot(snapshot: dict[str, Any], *, parent: str, branch: str, upstream_name: str, protected: str, main: str, paths: list[str]) -> None:
    require(snapshot["head"] == parent, "E_STAGED_PARENT")
    require(snapshot["branch"] == branch, "E_STAGED_BRANCH")
    require(snapshot["upstream_name"] == upstream_name and snapshot["upstream_commit"] == parent, "E_STAGED_UPSTREAM")
    require(snapshot["active_tracking"] == snapshot["active_live"] == parent, "E_STAGED_ACTIVE_REMOTE")
    require(snapshot["protected_local"] == snapshot["protected_tracking"] == snapshot["protected_live"] == protected, "E_STAGED_PROTECTED_REMOTE")
    require(snapshot["main_tracking"] == snapshot["main_live"] == main, "E_STAGED_MAIN_REMOTE")
    require(snapshot["staged"] == sorted(paths), f"E_STAGED_PATHS:{snapshot['staged']}")
    require(snapshot["unstaged"] == [] and snapshot["diff_check"], "E_STAGED_DIRTY")
    require(len(snapshot["status"]) == len(paths) and all(line[:2] in {"A ", "M "} for line in snapshot["status"]), "E_STAGED_STATUS")
    require(snapshot["claude_status"] == [] and not any(path.startswith("Claude/") for path in snapshot["staged"]), "E_STAGED_CLAUDE")
    require(snapshot["equal"] == {path: True for path in paths}, "E_STAGED_INDEX_WORKTREE")


def validate_persistence_snapshot(snapshot: dict[str, Any], *, commit: str, parent: str, subject: str, branch: str, upstream_name: str, protected: str, main: str, paths: list[str]) -> None:
    require(len(commit) == 40 and snapshot["head"] == commit, "E_PERSIST_HEAD")
    require(snapshot["parent"] == parent, "E_PERSIST_PARENT")
    require(snapshot["subject"] == subject, "E_PERSIST_SUBJECT")
    require(snapshot["committed"] == sorted(paths), "E_PERSIST_PATHS")
    require(snapshot["branch"] == branch and snapshot["upstream_name"] == upstream_name, "E_PERSIST_BRANCH")
    require(snapshot["upstream_commit"] == snapshot["active_tracking"] == snapshot["active_live"] == commit, "E_PERSIST_ACTIVE_REMOTE")
    require(snapshot["protected_local"] == snapshot["protected_tracking"] == snapshot["protected_live"] == protected, "E_PERSIST_PROTECTED")
    require(snapshot["main_tracking"] == snapshot["main_live"] == main, "E_PERSIST_MAIN")
    require(snapshot["claude_diff"] == snapshot["claude_status"] == [], "E_PERSIST_CLAUDE")
    require(snapshot["status"] == [] and snapshot["equal"] == {path: True for path in paths}, "E_PERSIST_DIRTY")


def live_ref(ref: str) -> str:
    output = str(run_git("ls-remote", "origin", ref)).strip()
    require(bool(output), f"E_LIVE_REF:{ref}")
    return output.split()[0]


def safe_index_worktree_equal(path: str) -> bool:
    try:
        return run_git("show", f":{path}", text=False) == (REPO / path).read_bytes()
    except (OSError, subprocess.CalledProcessError):
        return False


def safe_commit_worktree_equal(commit: str, path: str) -> bool:
    try:
        return git_bytes(commit, path) == (REPO / path).read_bytes()
    except (OSError, subprocess.CalledProcessError):
        return False


def production_staged_snapshot() -> dict[str, Any]:
    staged = str(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines()
    return {
        "head": str(run_git("rev-parse", "HEAD")).strip(), "branch": str(run_git("branch", "--show-current")).strip(),
        "upstream_name": str(run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")).strip(), "upstream_commit": str(run_git("rev-parse", "@{u}")).strip(),
        "active_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip(), "active_live": live_ref(f"refs/heads/{BRANCH}"),
        "protected_local": str(run_git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}")).strip(), "protected_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip(), "protected_live": live_ref(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_tracking": str(run_git("rev-parse", "refs/remotes/origin/main")).strip(), "main_live": live_ref("refs/heads/main"),
        "staged": staged, "unstaged": str(run_git("diff", "--name-only")).splitlines(),
        "status": str(run_git("status", "--porcelain=v1", "--untracked-files=all")).splitlines(),
        "diff_check": subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, timeout=60).returncode == 0,
        "claude_status": str(run_git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")).splitlines(),
        "equal": {path: safe_index_worktree_equal(path) for path in EXACT_PATHS},
    }


def production_persistence_snapshot(commit: str) -> dict[str, Any]:
    return {
        "head": str(run_git("rev-parse", "HEAD")).strip(), "parent": str(run_git("rev-parse", f"{commit}^")).strip(),
        "subject": str(run_git("show", "-s", "--format=%s", commit)).rstrip("\r\n"),
        "committed": str(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", commit)).splitlines(),
        "branch": str(run_git("branch", "--show-current")).strip(), "upstream_name": str(run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")).strip(),
        "upstream_commit": str(run_git("rev-parse", "@{u}")).strip(), "active_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip(), "active_live": live_ref(f"refs/heads/{BRANCH}"),
        "protected_local": str(run_git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}")).strip(), "protected_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip(), "protected_live": live_ref(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_tracking": str(run_git("rev-parse", "refs/remotes/origin/main")).strip(), "main_live": live_ref("refs/heads/main"),
        "claude_diff": str(run_git("diff", "--name-only", PARENT, commit, "--", "Claude")).splitlines(), "claude_status": str(run_git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")).splitlines(),
        "status": str(run_git("status", "--porcelain=v1", "--untracked-files=all")).splitlines(),
        "equal": {path: safe_commit_worktree_equal(commit, path) for path in EXACT_PATHS},
    }


def git_boundary_fixture() -> tuple[int, int]:
    tmp = tempfile.TemporaryDirectory(prefix="p063-step63-1-git-fixture-")
    root = pathlib.Path(tmp.name); work = root / "work"; origin = root / "origin.git"
    paths = [f"evidence-{number}.txt" for number in range(1, 9)]

    def fg(cwd: pathlib.Path, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=60, check=True).stdout.strip()

    def fgb(cwd: pathlib.Path, *args: str) -> bytes:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, timeout=60, check=True).stdout

    def flive(ref: str) -> str:
        return fg(root, "--git-dir", str(origin), "rev-parse", ref)

    def staged_snapshot() -> dict[str, Any]:
        staged = fg(work, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
        equal: dict[str, bool] = {}
        for path in paths:
            try: equal[path] = fgb(work, "show", f":{path}") == (work / path).read_bytes()
            except (OSError, subprocess.CalledProcessError): equal[path] = False
        return {
            "head": fg(work, "rev-parse", "HEAD"), "branch": fg(work, "branch", "--show-current"),
            "upstream_name": fg(work, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"), "upstream_commit": fg(work, "rev-parse", "@{u}"),
            "active_tracking": fg(work, "rev-parse", "refs/remotes/origin/active"), "active_live": flive("refs/heads/active"),
            "protected_local": fg(work, "rev-parse", "refs/heads/protected"), "protected_tracking": fg(work, "rev-parse", "refs/remotes/origin/protected"), "protected_live": flive("refs/heads/protected"),
            "main_tracking": fg(work, "rev-parse", "refs/remotes/origin/main"), "main_live": flive("refs/heads/main"),
            "staged": staged, "unstaged": fg(work, "diff", "--name-only").splitlines(), "status": fg(work, "status", "--porcelain=v1", "--untracked-files=all").splitlines(),
            "diff_check": subprocess.run(["git", "diff", "--cached", "--check"], cwd=work, capture_output=True, timeout=60).returncode == 0,
            "claude_status": fg(work, "status", "--porcelain=v1", "--untracked-files=all", "--", "Claude").splitlines(), "equal": equal,
        }

    def persisted_snapshot(commit: str) -> dict[str, Any]:
        equal: dict[str, bool] = {}
        for path in paths:
            try: equal[path] = fgb(work, "show", f"{commit}:{path}") == (work / path).read_bytes()
            except (OSError, subprocess.CalledProcessError): equal[path] = False
        return {
            "head": fg(work, "rev-parse", "HEAD"), "parent": fg(work, "rev-parse", f"{commit}^"), "subject": fg(work, "show", "-s", "--format=%s", commit),
            "committed": fg(work, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines(), "branch": fg(work, "branch", "--show-current"),
            "upstream_name": fg(work, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"), "upstream_commit": fg(work, "rev-parse", "@{u}"),
            "active_tracking": fg(work, "rev-parse", "refs/remotes/origin/active"), "active_live": flive("refs/heads/active"),
            "protected_local": fg(work, "rev-parse", "refs/heads/protected"), "protected_tracking": fg(work, "rev-parse", "refs/remotes/origin/protected"), "protected_live": flive("refs/heads/protected"),
            "main_tracking": fg(work, "rev-parse", "refs/remotes/origin/main"), "main_live": flive("refs/heads/main"),
            "claude_diff": fg(work, "diff", "--name-only", parent, commit, "--", "Claude").splitlines(), "claude_status": fg(work, "status", "--porcelain=v1", "--untracked-files=all", "--", "Claude").splitlines(),
            "status": fg(work, "status", "--porcelain=v1", "--untracked-files=all").splitlines(), "equal": equal,
        }

    passed = 0
    def expect(name: str, diagnostic: str, action: Callable[[], None], evaluator: Callable[[], None]) -> None:
        nonlocal passed
        action()
        try: evaluator()
        except ValidationError as exc:
            require(str(exc).split(":", 1)[0] == diagnostic, f"E_GIT_FIXTURE_DIAGNOSTIC:{name}:{exc}!={diagnostic}"); passed += 1
        else: raise ValidationError(f"E_GIT_FIXTURE_ESCAPED:{name}")

    try:
        work.mkdir(); fg(work, "init", "--initial-branch=main"); fg(work, "config", "user.email", "step63-fixture@example.invalid"); fg(work, "config", "user.name", "Step 63 Fixture")
        (work / "base.txt").write_bytes(b"base\n"); (work / "Claude").mkdir(); (work / "Claude" / "keep.txt").write_bytes(b"protected\n")
        fg(work, "add", "base.txt", "Claude/keep.txt"); fg(work, "commit", "-m", "base"); parent = fg(work, "rev-parse", "HEAD")
        fg(work, "branch", "protected", parent); fg(work, "branch", "active", parent); fg(work, "switch", "-c", "drift", parent); fg(work, "commit", "--allow-empty", "-m", "drift"); drift = fg(work, "rev-parse", "HEAD"); fg(work, "switch", "active")
        fg(root, "init", "--bare", str(origin)); fg(work, "remote", "add", "origin", str(origin)); fg(work, "push", "origin", "main", "protected", "drift:fixture-drift"); fg(work, "push", "-u", "origin", "active")
        for path in paths: (work / path).write_bytes((path + "\n").encode())
        fg(work, "add", *paths)
        staged_eval = lambda: validate_staged_snapshot(staged_snapshot(), parent=parent, branch="active", upstream_name="origin/active", protected=parent, main=parent, paths=paths)
        staged_eval()
        extra = work / "extra.txt"
        expect("extra_staged", "E_STAGED_PATHS", lambda: (extra.write_bytes(b"x\n"), fg(work, "add", "extra.txt")), staged_eval); fg(work, "restore", "--staged", "extra.txt"); extra.unlink()
        expect("missing_staged", "E_STAGED_PATHS", lambda: fg(work, "restore", "--staged", paths[-1]), staged_eval); fg(work, "add", paths[-1])
        original = (work / paths[0]).read_bytes()
        expect("index_worktree", "E_STAGED_INDEX_WORKTREE", lambda: ((work / paths[0]).write_bytes(b"changed\n"), fg(work, "update-index", "--assume-unchanged", paths[0])), staged_eval)
        (work / paths[0]).write_bytes(original); fg(work, "update-index", "--no-assume-unchanged", paths[0])
        expect("wrong_upstream", "E_STAGED_UPSTREAM", lambda: fg(work, "branch", "--set-upstream-to", "origin/main", "active"), staged_eval); fg(work, "branch", "--set-upstream-to", "origin/active", "active")
        expect("active_drift", "E_STAGED_ACTIVE_REMOTE", lambda: fg(root, "--git-dir", str(origin), "update-ref", "refs/heads/active", drift), staged_eval); fg(root, "--git-dir", str(origin), "update-ref", "refs/heads/active", parent)
        expect("protected_drift", "E_STAGED_PROTECTED_REMOTE", lambda: fg(root, "--git-dir", str(origin), "update-ref", "refs/heads/protected", drift), staged_eval); fg(root, "--git-dir", str(origin), "update-ref", "refs/heads/protected", parent)
        expect("main_drift", "E_STAGED_MAIN_REMOTE", lambda: fg(root, "--git-dir", str(origin), "update-ref", "refs/heads/main", drift), staged_eval); fg(root, "--git-dir", str(origin), "update-ref", "refs/heads/main", parent)
        fg(work, "commit", "-m", "wrong subject"); wrong = fg(work, "rev-parse", "HEAD")
        persist_eval_wrong = lambda: validate_persistence_snapshot(persisted_snapshot(wrong), commit=wrong, parent=parent, subject=SUBJECT, branch="active", upstream_name="origin/active", protected=parent, main=parent, paths=paths)
        expect("wrong_subject", "E_PERSIST_SUBJECT", lambda: None, persist_eval_wrong)
        fg(work, "commit", "--amend", "-m", SUBJECT); committed = fg(work, "rev-parse", "HEAD"); fg(work, "push", "origin", "active")
        persist_eval = lambda: validate_persistence_snapshot(persisted_snapshot(committed), commit=committed, parent=parent, subject=SUBJECT, branch="active", upstream_name="origin/active", protected=parent, main=parent, paths=paths)
        persist_eval()
        drift_file = work / "Claude" / "drift.txt"
        expect("claude_drift", "E_PERSIST_CLAUDE", lambda: drift_file.write_bytes(b"drift\n"), persist_eval); drift_file.unlink()
        fg(work, "reset", "--hard", drift)
        for path in paths: (work / path).write_bytes((path + "\n").encode())
        fg(work, "add", *paths); fg(work, "commit", "-m", SUBJECT); wrong_parent = fg(work, "rev-parse", "HEAD")
        wrong_parent_eval = lambda: validate_persistence_snapshot(persisted_snapshot(wrong_parent), commit=wrong_parent, parent=parent, subject=SUBJECT, branch="active", upstream_name="origin/active", protected=parent, main=parent, paths=paths)
        expect("wrong_parent", "E_PERSIST_PARENT", lambda: None, wrong_parent_eval)
        fg(work, "reset", "--hard", committed)
    finally:
        tmp.cleanup()
    require(not root.exists(), "E_GIT_FIXTURE_CLEANUP")
    return passed, 10


def run_negative_probes(disposition: dict[str, Any], carry: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]], projection: tuple[dict[str, Any], dict[str, Any], bytes]) -> None:
    probes: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], None], str]] = []
    def add(name: str, mutate: Callable[[dict[str, Any], dict[str, Any]], None], diagnostic: str) -> None:
        probes.append((name, mutate, diagnostic))
    add("schema", lambda d, c: d.__setitem__("invented", True), "E_DISPOSITION_SCHEMA")
    add("step", lambda d, c: d.__setitem__("step", "63.2"), "E_PHASE_STEP")
    add("input", lambda d, c: d.__setitem__("input_commit", "0" * 40), "E_INPUT_IDENTITY")
    add("gate", lambda d, c: c.__setitem__("gate", "PASS"), "E_GATE")
    add("source_loss", lambda d, c: d["source_dispositions"].pop(), "E_SOURCE_COUNT")
    add("source_duplicate", lambda d, c: d["source_dispositions"][1].__setitem__("source_id", d["source_dispositions"][0]["source_id"]), "E_SOURCE_DUPLICATE")
    add("source_identity", lambda d, c: d["source_dispositions"][0]["source_identity"].__setitem__("blob_sha1", "0" * 40), "E_SOURCE_IDENTITY")
    add("vocabulary", lambda d, c: d["source_dispositions"][0].__setitem__("disposition", "ADOPT"), "E_DISPOSITION_VOCABULARY")
    add("evidence_pointer", lambda d, c: d["source_dispositions"][0]["evidence_routes"][0].__setitem__("json_pointer", "/sources/999"), "E_SOURCE_IDENTITY_POINTER")
    add("evidence_hash", lambda d, c: d["source_dispositions"][0]["evidence_routes"][0].__setitem__("record_sha256", "0" * 64), "E_EVIDENCE_RECORD_SHA")
    add("disposition_rule", lambda d, c: next(r for r in d["source_dispositions"] if r["disposition"] == "PRESERVE").__setitem__("disposition", "CORRECT"), "E_DISPOSITION_RULE")
    add("owner", lambda d, c: next(r for r in d["source_dispositions"] if r["status"] == "OPEN").__setitem__("canonical_owner_id", None), "E_SOURCE_OWNER")
    add("source_downstream", lambda d, c: next(r for r in d["source_dispositions"] if r["primary_target_phase"] == 79)["downstream_target_phases"].remove(80), "E_SOURCE_TARGET")
    add("source_authority", lambda d, c: d["source_dispositions"][0].__setitem__("external_scientific_truth", True), "E_SOURCE_AUTHORITY")
    add("supplemental_fusion", lambda d, c: d["supplemental_process_disposition"].__setitem__("manifest_member", True), "E_SUPPLEMENTAL_DENOMINATOR")
    add("link_loss", lambda d, c: c["source_disposition_links"].pop(), "E_SOURCE_LINK_COUNT")
    add("finding_loss", lambda d, c: c["phase057_finding_routes"].pop(), "E_PHASE057_COUNT")
    add("finding_state", lambda d, c: c["phase057_finding_routes"][0].__setitem__("state_before", "OPEN"), "E_PHASE057_STATES")
    add("finding_origin", lambda d, c: c["phase057_finding_routes"][0].__setitem__("origin_record_sha256", "0" * 64), "E_PHASE057_ORIGIN")
    add("finding_owner", lambda d, c: next(r for r in c["phase057_finding_routes"] if r["status_after"] == "OPEN_CARRY").__setitem__("canonical_owner_id", None), "E_PHASE057_OWNER")
    add("finding_target", lambda d, c: next(r for r in c["phase057_finding_routes"] if r["numeric_id"] == 101).__setitem__("target_phase", 71), "E_PHASE057_TARGET")
    add("finding_resolution", lambda d, c: c["phase057_finding_routes"][0].__setitem__("canonical_owner_id", None), "E_PHASE057_RESOLUTION")
    add("owner_universe_loss", lambda d, c: c["canonical_owner_duplicate_check_universe"]["records"].pop(), "E_OWNER_UNIVERSE_IDENTITY")
    add("audit_loss", lambda d, c: c["phase063_audit_finding_routes"].pop(), "E_AUDIT_COUNT")
    add("audit_priority", lambda d, c: c["phase063_audit_finding_routes"][0].__setitem__("priority", "P2"), "E_AUDIT_COUNT")
    add("audit_owner", lambda d, c: c["phase063_audit_finding_routes"][0].__setitem__("canonical_owner_id", "generic"), "E_AUDIT_OWNER")
    add("audit_phase081", lambda d, c: next(r for r in c["phase063_audit_finding_routes"] if r["finding_id"] == "P063-S61-F005").__setitem__("target_phase", 82), "E_AUDIT_TARGET")
    add("audit_duplicate_check", lambda d, c: c["phase063_audit_finding_routes"][0]["duplicate_check"].__setitem__("owner_universe_records", 307), "E_AUDIT_DUPLICATE_CHECK")
    add("audit_corroboration", lambda d, c: next(r for r in c["phase063_audit_finding_routes"] if r["finding_id"] == "P063-S59-F001").__setitem__("corroborating_audit_finding_ids", []), "E_AUDIT_CORROBORATION")
    add("carry_loss", lambda d, c: c["inherited_carry_items"].pop(), "E_INHERITED_COUNT")
    add("carry_mutation", lambda d, c: c["canonical_debt_routing"][0]["prior_record"].__setitem__("invented", True), "E_INHERITED_LOSS")
    add("new_blocker", lambda d, c: c["new_phase063_blockers"].append({"id": "invented"}), "E_NEW_BLOCKER")
    add("summary", lambda d, c: c["gate_summary"].__setitem__("ownerless_open_routes", 1), "E_GATE_SUMMARY")
    add("authority", lambda d, c: c["authority_boundary"].__setitem__("primary_literature_truth", True), "E_AUTHORITY_BOUNDARY")
    add("projection", lambda d, c: d["source_dispositions"][0].__setitem__("reason", "invented"), "E_EXACT_PROJECTION")
    passed = 0
    for name, mutate, diagnostic in probes:
        d = copy.deepcopy(disposition); c = copy.deepcopy(carry); mutate(d, c)
        try:
            validate_semantics(d, c, inputs, metadata, projection)
        except ValidationError as exc:
            require(str(exc).split(":", 1)[0] == diagnostic, f"E_NEGATIVE_DIAGNOSTIC:{name}:{exc}!={diagnostic}"); passed += 1
        else:
            raise ValidationError(f"E_NEGATIVE_ESCAPED:{name}")
    strict_fixtures = [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":', b'{"a":1} x', b'{"a":1e9999}']
    for raw in strict_fixtures:
        try: strict_load_bytes(raw)
        except ValidationError: passed += 1
        else: raise ValidationError("E_STRICT_JSON_ESCAPED")
    disposition_sha = sha256((REPO / DISPOSITION).read_bytes()); carry_sha = sha256((REPO / CARRY).read_bytes())
    docs = [(REPO / RESULT).read_text(encoding="utf-8"), (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8"), (REPO / PARENT_LEDGER).read_text(encoding="utf-8"), (REPO / HANDOVER).read_text(encoding="utf-8")]
    phase_row_prefix = "| 063 | 58–63 | activation and Steps 58–62 complete; Step 63.1 precommit |"
    handover_prefix = "| Phase 063 Step 63.1 | Step 63.1 |"
    active_current = next(line for line in docs[1].splitlines() if line.startswith("| 063 | 58–63 |"))
    active_step_current = next(line for line in docs[1].splitlines() if line.startswith("| Step 63.1 |"))
    handover_current = next(line for line in docs[3].splitlines() if line.startswith("| Phase 063 Step 63.1 |"))

    def replace_row_token(text: str, row: str, old: str, new: str) -> str:
        require(text.count(row) == 1 and row.count(old) == 1, "E_RECOVERY_FIXTURE_SETUP")
        return text.replace(row, row.replace(old, new, 1), 1)

    recovery = [
        ("result_overall_fail", 0, lambda text: text + "\nOverall status: FAIL\n", "E_RESULT_GATE_SURFACE"),
        ("active_current_fail", 1, lambda text: text.replace(phase_row_prefix, phase_row_prefix + " FAIL", 1), "E_ACTIVE_LEDGER_RECOVERY"),
        ("parent_current_conditional", 2, lambda text: text.replace(phase_row_prefix, phase_row_prefix + " CONDITIONAL", 1), "E_PARENT_LEDGER_RECOVERY"),
        ("handover_current_fail", 3, lambda text: text.replace(handover_prefix, handover_prefix + " FAIL", 1), "E_HANDOVER_RECOVERY"),
        ("active_duplicate_current", 1, lambda text: text + "\n" + active_current + "\n", "E_ACTIVE_LEDGER_ROW_COUNT"),
        ("active_phase_row_hash_corrupt", 1, lambda text: replace_row_token(text, active_current, disposition_sha, "0" * 64), "E_ACTIVE_LEDGER_RECOVERY"),
        ("active_step_row_hash_corrupt", 1, lambda text: replace_row_token(text, active_step_current, disposition_sha, "0" * 64), "E_ACTIVE_STEP_LEDGER_RECOVERY"),
        ("active_step_row_duplicate", 1, lambda text: text + "\n" + active_step_current + "\n", "E_ACTIVE_STEP_LEDGER_ROW_COUNT"),
        ("handover_current_hash_corrupt", 3, lambda text: replace_row_token(text, handover_current, disposition_sha, "0" * 64), "E_HANDOVER_RECOVERY"),
        ("handover_current_subject_corrupt", 3, lambda text: replace_row_token(text, handover_current, SUBJECT, "audit(phase063): corrupted subject"), "E_HANDOVER_RECOVERY"),
    ]
    for name, index, mutate_recovery, diagnostic in recovery:
        mutated = list(docs); mutated[index] = mutate_recovery(mutated[index])
        try: validate_recovery_texts(*mutated, disposition_sha, carry_sha)
        except ValidationError as exc: require(str(exc).split(":", 1)[0] == diagnostic, f"E_RECOVERY_DIAGNOSTIC:{exc}"); passed += 1
        else: raise ValidationError(f"E_RECOVERY_ESCAPED:{name}")
    builder_raw = (REPO / BUILDER).read_bytes(); text = builder_raw.decode("utf-8")
    policies = [(builder_raw + b"\n# mutate\n", True, True, "E_BUILDER_RAW_SHA256"), (text.replace("timeout=120", "timeout=121", 1).encode(), False, True, "E_BUILDER_AST_SHA256"), (text.replace("    process = subprocess.run(", "    subprocess.run(['git', '--version'])\n    process = subprocess.run(", 1).encode(), False, False, "E_BUILDER_SUBPROCESS_POLICY"), (text.replace('["git", *args]', '["cmd", *args]', 1).encode(), False, False, "E_BUILDER_SUBPROCESS_ARGV")]
    for raw, raw_pin, ast_pin, diagnostic in policies:
        try: validate_builder_policy(raw, raw_pin=raw_pin, ast_pin=ast_pin)
        except ValidationError as exc: require(str(exc).split(":", 1)[0] == diagnostic, f"E_POLICY_DIAGNOSTIC:{exc}"); passed += 1
        else: raise ValidationError("E_POLICY_ESCAPED")
    git_passed, git_total = git_boundary_fixture(); passed += git_passed
    total = len(probes) + len(strict_fixtures) + len(recovery) + len(policies) + git_total
    print(f"PASS_P063_STEP63_1_NEGATIVE {passed}/{total} strict_json=6/6 recovery={len(recovery)}/{len(recovery)} builder_policy=4/4 git_boundary={git_passed}/{git_total}")


def determinism_check() -> None:
    with tempfile.TemporaryDirectory(prefix="p063-step63-1-determinism-") as tmp:
        root = pathlib.Path(tmp); outputs: list[tuple[bytes, bytes, bytes]] = []
        for run in (1, 2):
            d = root / f"d-{run}.json"; c = root / f"c-{run}.json"; r = root / f"r-{run}.md"
            subprocess.run([sys.executable, "-B", str(REPO / BUILDER), "--repo", str(REPO), "--disposition", str(d), "--carry", str(c), "--result", str(r)], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=240, check=True)
            outputs.append((d.read_bytes(), c.read_bytes(), r.read_bytes()))
        require(outputs[0] == outputs[1], "E_DETERMINISM_2X")
        require(outputs[0] == ((REPO / DISPOSITION).read_bytes(), (REPO / CARRY).read_bytes(), (REPO / RESULT).read_bytes()), "E_DETERMINISM_STORED")
    print("PASS_P063_STEP63_1_DETERMINISM 2/2")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    try:
        require(not (args.verify_staged and args.verify_persistence), "E_MODE_CONFLICT")
        validate_builder_policy()
        inputs, metadata = load_inputs()
        disposition = strict_load(REPO / DISPOSITION); carry = strict_load(REPO / CARRY)
        projection = expected_projection()
        validate_semantics(disposition, carry, inputs, metadata, projection)
        validate_result_and_recovery()
        nodes = sum(traversal_count(value) for value in [*inputs.values(), disposition, carry])
        strong = args.verify_staged or args.verify_persistence
        if args.run_negative_probes or strong: run_negative_probes(disposition, carry, inputs, metadata, projection)
        if args.determinism_check or strong: determinism_check()
        if args.verify_staged:
            validate_staged_snapshot(production_staged_snapshot(), parent=PARENT, branch=BRANCH, upstream_name=f"origin/{BRANCH}", protected=PROTECTED_TIP, main=MAIN_TIP, paths=EXACT_PATHS)
            print("PASS_P063_STEP63_1_STAGED exact-eight")
        elif args.verify_persistence:
            require(bool(args.expected_commit), "E_EXPECTED_COMMIT_REQUIRED")
            validate_persistence_snapshot(production_persistence_snapshot(str(args.expected_commit)), commit=str(args.expected_commit), parent=PARENT, subject=SUBJECT, branch=BRANCH, upstream_name=f"origin/{BRANCH}", protected=PROTECTED_TIP, main=MAIN_TIP, paths=EXACT_PATHS)
            print(PERSISTENCE)
        else:
            print(f"{GATE} strict_traversal={nodes}")
        return 0
    except (KeyError, IndexError, OSError, subprocess.CalledProcessError, SyntaxError, TypeError, ValidationError) as exc:
        print(f"FAIL_P063_STEP63_1: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
