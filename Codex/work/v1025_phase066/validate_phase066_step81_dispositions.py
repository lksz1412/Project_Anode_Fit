from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step81_dispositions.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step81_dispositions.py"
DISPOSITION_PATH = "Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json"
CARRY_PATH = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_081_1_DISPOSITION_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXACT_PATHS = {
    BUILDER_PATH,
    VALIDATOR_PATH,
    DISPOSITION_PATH,
    CARRY_PATH,
    RESULT_PATH,
    PARENT_LEDGER,
    ACTIVE_LEDGER,
    HANDOVER,
}
EXPECTED_PARENT = "ec02d8e0017c4441d9d02c08e22ad432b8c47bc5"
EXPECTED_SUBJECT = "audit(phase066): disposition v1025 lineage evidence"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BUILDER_SHA256 = "be25cddfeacd8d0e212aea422fe09190f649833ba792f491c4c3e338336b10fd"
BUILDER_POLICY_AST_SHA256 = {
    (3, 12): "b95c5567cc7785b28e1c0197d722b319edef4348cb52cc937fec0e4414c4c4b8",
    (3, 14): "f2dafca76d1b6d5413341373a22b8aab040da9a377d1a8515f263864eeda85e5",
}
ALLOWED_DISPOSITIONS = {"PRESERVE", "CORRECT", "WITHHOLD", "DISCARD", "GROUND_NOT_FOUND"}
DOC_SHA256 = {
    RESULT_PATH: "f81669d3fd9c0a033ea15c2f7422b997798fd0db44a328ab38519c00ea9e4b17",
    PARENT_LEDGER: "f4666e4a873fdd704f359241dd5bb95370e6068bcc91fcbede7eca22fa237b2c",
    ACTIVE_LEDGER: "0cb0efe47f382687c8a3573196a65960d4e8465bfc8e857d0a52248234f30af9",
    HANDOVER: "5d30f5435651bcd7b99223d98e1b9756b90d06a1d813613bd8030ab26684cbe7",
}


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(code if not detail else f"{code}:{detail}")


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def record_sha(value: Any) -> str:
    return sha256(compact(value))


def strict_load(raw: bytes) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, "E_DUPLICATE_JSON_KEY", key)
            result[key] = value
        return result

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def verify_seal(obj: dict[str, Any], code: str) -> None:
    claimed = obj.get("semantic_sha256")
    body = dict(obj)
    body.pop("semantic_sha256", None)
    require(claimed == sha256(compact(body)), code)


def load_builder() -> Any:
    raw = (ROOT / BUILDER_PATH).read_bytes()
    require(sha256(raw) == BUILDER_SHA256, "E_BUILDER_SOURCE_SHA")
    spec = importlib.util.spec_from_file_location("p066_step81_builder", ROOT / BUILDER_PATH)
    require(spec is not None and spec.loader is not None, "E_BUILDER_IMPORT")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_source(obj: dict[str, Any], builder: Any, expected: dict[str, Any], *, check_recompute: bool = True) -> None:
    verify_seal(obj, "E_SOURCE_SEAL")
    if check_recompute:
        require(obj == expected, "E_SOURCE_RECOMPUTE")
    require(obj["schema_version"] == "P066_STEP81_1_SOURCE_DISPOSITION_V1", "E_SOURCE_SCHEMA")
    rows = obj["source_dispositions"]
    groups = obj["blob_disposition_groups"]
    supplements = obj["supplemental_dispositions"]
    processes = obj["process_dispositions"]
    require(len(rows) == 433 and len(groups) == 167, "E_SOURCE_DENOMINATOR")
    require(len(supplements) == 2 and all(row["separate_from_manifest_occurrences"] for row in supplements), "E_SUPPLEMENTAL_DENOMINATOR")
    source_paths = {row["source_path"] for row in rows}
    for row in supplements:
        raw = git("show", f"3b5fd059ed09cdcdde38668c399cb35b8afbcca9:{row['path']}")
        require(row["path"] not in source_paths and row["blob_sha1"] == git("rev-parse", f"3b5fd059ed09cdcdde38668c399cb35b8afbcca9:{row['path']}").decode().strip(), "E_SUPPLEMENTAL_IDENTITY")
        require(row["bytes"] == len(raw) and row["raw_sha256"] == sha256(raw) == row["lf_sha256"] and row["read_status"] == "READ_FULL" and row["routed_commits"], "E_SUPPLEMENTAL_BINDING")
    require(len(processes) == 20, "E_PROCESS_DENOMINATOR")
    require(len({row["manifest_index"] for row in rows}) == 433, "E_DUPLICATE_DISPOSITION")
    require(len({(row["source_path"], row["manifest_index"]) for row in rows}) == 433, "E_ORPHAN_OCCURRENCE")
    require(all(row["disposition"] in ALLOWED_DISPOSITIONS for row in rows), "E_DISPOSITION_ENUM")
    require(all(row["inventory_identity_disposition"] == "PRESERVE" for row in rows), "E_INVENTORY_IDENTITY")
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["blob_sha1"], []).append(row)
        require(row["read_attestation"]["status"] in {"READ_FULL", "MACHINE_COMPLETE_HUMAN_AUTHORED_READ"}, "E_READ_STATUS")
        require(row["read_attestation"]["machine_status"] == "MACHINE_READ_FULL", "E_MACHINE_READ")
        require(row["release_build_disposition"] == row["disposition"], "E_RELEASE_DISPOSITION_AXIS")
        require(row["external_authority_promoted"] is False, "E_SOURCE_AUTHORITY_PROMOTION")
    require(set(grouped) == {row["blob_sha1"] for row in groups}, "E_BLOB_PROJECTION")
    for group in groups:
        members = grouped[group["blob_sha1"]]
        require(len(members) == group["occurrence_count"], "E_BLOB_COUNT")
        dispositions = sorted({row["disposition"] for row in members})
        require(group["occurrence_dispositions"] == dispositions, "E_BLOB_GROUP_DISPOSITION")
        require(group["contextual_mixed_disposition"] == (len(dispositions) > 1), "E_BLOB_CONTEXT")
    stale = [row for row in rows if row["release_build_disposition"] == "WITHHOLD"]
    stale_pdfs = [row for row in stale if row["source_path"].endswith(".pdf")]
    require(len(stale_pdfs) == 3 and all(row["version"] == "v1.0.25.2" and row["inventory_identity_disposition"] == "PRESERVE" for row in stale_pdfs), "E_STALE_PDF_CLOSURE")
    require(obj["counts"]["distribution"] == {"CORRECT": 3, "PRESERVE": 424, "WITHHOLD": 6}, "E_SOURCE_DISTRIBUTION")
    require(obj["source_contract"]["manifest_raw_sha256"] == "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef", "E_MANIFEST_BINDING")
    process = obj["process_commit_coverage"]
    require((process["release_commit_count"], process["routed_commit_count"], process["routed_only_commit_count"], process["supplemental_touch_commit_count"], process["supplemental_only_commit_count"]) == (17, 20, 3, 5, 3), "E_PROCESS_COUNTS")
    require(process["release_orphan_count"] == process["routed_orphan_count"] == process["empty_path_union_count"] == 0, "E_PROCESS_ORPHAN")
    require(all(row["relevant_release_paths"] or row["relevant_supplemental_paths"] for row in processes), "E_PROCESS_PATH_ORPHAN")


def validate_carry(obj: dict[str, Any], builder: Any, expected: dict[str, Any], inputs: dict[str, Any], *, check_recompute: bool = True) -> None:
    verify_seal(obj, "E_CARRY_SEAL")
    if check_recompute:
        require(obj == expected, "E_CARRY_RECOMPUTE")
    require(obj["schema_version"] == "P066_STEP81_1_CARRY_FORWARD_V1", "E_CARRY_SCHEMA")
    prior = inputs["Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json"]
    require(obj["inherited_phase065_observations"] == prior["observation_records"], "E_INHERITED_OBSERVATION_LOSS")
    require(obj["active_obligations"][:94] == prior["active_obligations"], "E_INHERITED_ACTIVE_LOSS")
    prior_registry = prior["current_owner_duplicate_check_universe"]["records"]
    registry = obj["current_owner_duplicate_check_universe"]["records"]
    require(registry[:192] == prior_registry, "E_INHERITED_REGISTRY_LOSS")
    require(len(registry) == 355 and obj["current_owner_duplicate_check_universe"]["records_sha256"] == sha256(compact(registry)), "E_REGISTRY_COUNT")
    origins = [row["origin_identity"] for row in registry]
    require(len(origins) == len(set(origins)), "E_MULTIPLE_OWNER")
    routes = obj["phase057_route_adjudications"]
    new = [row for row in routes if row["route_class"] == "NEW_P066_INTAKE"]
    shared = [row for row in routes if row["route_class"] == "SHARED_P065_REFERENCE"]
    require((len(routes), len(new), len(shared)) == (105, 95, 10), "E_PHASE057_DENOMINATOR")
    require({row["numeric_id"] for row in new} == set(range(293, 388)), "E_AO_AW_MISSING")
    require({row["numeric_id"] for row in shared} == set(range(395, 405)), "E_AY_IDS")
    lineage = obj["phase057_lineage"]
    require((lineage["prior_count"], lineage["new_count"], lineage["ay_overlap_count"], lineage["union_count"]) == (82, 95, 10, 177), "E_PHASE057_LINEAGE")
    require(lineage["union_numeric_range"] == [228, 404] and lineage["prior_only_ax_ids"] == list(range(388, 395)), "E_PHASE057_RANGE")
    require(lineage["lost_id_count"] == lineage["duplicate_new_id_count"] == 0, "E_PHASE057_LOSS")
    prior_by_id = {row["origin_identity"]: row for row in prior_registry}
    for row in shared:
        prior_row = prior_by_id[row["observation_id"]]
        require(row["canonical_owner"] == prior_row["owner_id"], "E_AY_OWNER_DRIFT")
        require(row["target_phase"] == prior_row["target_phase"] and row["current_state"] == prior_row["state"], "E_AY_STATE_DRIFT")
    for row in new:
        require(row["canonical_owner"] and row["acceptance_criterion"], "E_OWNERLESS_PHASE057")
        require(row["current_state"] in {"OPEN_CARRY", "BOUNDED_HISTORICAL"}, "E_PHASE057_STATE")
        require(row["external_authority_promoted"] is False, "E_PHASE057_AUTHORITY")
    steps = obj["step76_80_disposition_records"]
    require(len(steps) == 68 and len({row["observation_id"] for row in steps}) == 68, "E_STEP_RECORD_DENOMINATOR")
    require(all(row["disposition"] in ALLOWED_DISPOSITIONS for row in steps), "E_STEP_DISPOSITION_ENUM")
    require(all(row["external_authority_promoted"] is False for row in steps), "E_STEP_AUTHORITY_PROMOTION")
    direct = next(row for row in steps if row["observation_id"] == "P066-E79-01")
    require(direct["disposition"] == "PRESERVE" and direct["state"] == "BOUNDED_INTERNAL", "E_EMPIRICAL_PHYSICAL_MERGE")
    require(direct["authority_axes"]["empirical"]["pass"] is True and direct["authority_axes"]["empirical"]["disposition"] == "PRESERVE", "E_EMPIRICAL_AXIS")
    require(direct["authority_axes"]["physical"]["authority"] is False and direct["authority_axes"]["physical"]["disposition"] == "WITHHOLD", "E_PHYSICAL_AXIS")
    step79 = [row for row in steps if row["origin_step"] == "Phase 066 Step 79"]
    require(len(step79) == 8, "E_STEP79_COUNT")
    for row in step79:
        axes = row["authority_axes"]
        require(axes["physical"]["authority"] is False and axes["phase"]["authority"] is False and axes["proposition"]["authority"] is False and axes["external"]["authority"] is False, "E_STEP79_AUTHORITY", row["observation_id"])
    source_claims = {row["id"]: row for row in inputs["Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json"]["claim_rows"]}
    for row in step79:
        source_id = row["observation_id"].removeprefix("P066-")
        require(row["source_owner"] == source_claims[source_id]["owner"], "E_STEP79_SOURCE_OWNER")
    availability = [row for row in steps if row["observation_id"].startswith("P066-S78-ORIGINAL-STATE-")]
    require(len(availability) == 25 and all(row["disposition"] == "GROUND_NOT_FOUND" and row["state"] == "OPEN_CARRY" for row in availability), "E_ORIGINAL_STATE_PROMOTION")
    require(next(row for row in steps if row["observation_id"] == "P066-S77-NONCONVERGED")["state"] == "OPEN_CARRY", "E_NONCONVERGED_CLOSURE")
    contradiction_ids = {"P066-S80-EVIDENCE-DIVERGENT_7_7_PAIR_EXAMPLES", "P066-S80-EVIDENCE-STALE_ALPHA_COMMENT", "P066-S80-EVIDENCE-STALE_CLASS_DOCSTRING", "P066-S80-EVIDENCE-STALE_HEADER_COMMENT"}
    contradiction_rows = [row for row in steps if row["observation_id"] in contradiction_ids]
    require(len(contradiction_rows) == 4 and all(row["disposition"] == "CORRECT" and row["state"] == "OPEN_CARRY" for row in contradiction_rows), "E_STEP80_CONTRADICTION_CLOSURE")
    ref7_observation = next(row for row in steps if row["observation_id"] == "P066-P79-08")
    require(ref7_observation["state"] == "BOUNDED_REFERENCE" and ref7_observation["relation_links"] == ["D74-006", "P065-SEM-002"], "E_REF7_DUPLICATE")
    r80_14 = next(row for row in steps if row["observation_id"] == "P066-R80-14")
    require(r80_14["canonical_owner"] == "P067-CODE-HISTORY" and r80_14["state"] == "OPEN_CARRY" and r80_14["authority_axes"]["serialized_compatibility"]["status"] == "CURRENT_PUBLIC_LOGISTIC_ONLY_KERNEL_METADATA_NOT_DISPATCHED", "E_R80_14_ROUTE")
    p071_rows = [row for row in steps if row.get("source_owner") == "P071-PRIMARY-SOURCE-ACQUISITION"]
    require(len(p071_rows) == 4 and all(row["canonical_owner"] == "PHASE-071-PRIMARY-SOURCE-ACQUISITION" for row in p071_rows), "E_OWNER_ALIAS")
    step80_routes = [row for row in steps if re.fullmatch(r"P066-R80-\d{2}", row["observation_id"])]
    require(len(step80_routes) == 16, "E_STEP80_ROUTE_COUNT")
    source_routes = {row["id"]: row for row in inputs["Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"]["route_rows"]}
    for row in step80_routes:
        source_id = row["observation_id"].removeprefix("P066-")
        original = source_routes[source_id]
        require(row["source_owner"] == original["owner"], "E_STEP80_SOURCE_OWNER")
        require(row["authority_axes"]["profile_selection"]["authority"] is False and row["authority_axes"]["external_material"]["authority"] is False and row["authority_axes"]["multi_temperature_experimental"]["authority"] is False, "E_STEP80_AUTHORITY")
        require(row["authority_axes"]["serialized_compatibility"]["status"] == original["serialized_compatibility"], "E_STEP80_STATUS")
    optimizer_contract = next(row for row in steps if row["observation_id"] == "P066-S77-OPTIMIZER-CONTRACT")
    expected_links = {row["observation_id"] for row in availability}
    require(set(optimizer_contract["relation_links"]) == expected_links and len(optimizer_contract["relation_links"]) == 25, "E_OPTIMIZER_RELATION")
    relation_targets = {row["observation_id"] for row in steps} | {row["observation_id"] for row in prior["observation_records"]} | {row["group_id"] for row in prior["semantic_duplicate_groups"]}
    require(all(link in relation_targets for row in steps for link in row["relation_links"]), "E_DANGLING_RELATION")
    active = obj["active_obligations"]
    active_origins = [row["origin_identity"] for row in active]
    require(len(active_origins) == len(set(active_origins)), "E_MULTIPLE_ACTIVE_OWNER")
    require(all(row["canonical_owner"] and row["acceptance_criterion"] for row in active), "E_OWNERLESS_ACTIVE")
    open_origins = {row["observation_id"] for row in [*new, *steps] if row.get("current_state") == "OPEN_CARRY" or row.get("state") == "OPEN_CARRY"}
    inherited_active_origins = {row["origin_identity"] for row in prior["active_obligations"]}
    require(set(active_origins) == inherited_active_origins | open_origins and len(active) == 219, "E_ACTIVE_PARTITION")
    require("P066-P79-08" not in active_origins and active_origins.count("D74-006") == 1, "E_REF7_MULTIPLE_ACTIVE")
    ref7 = obj["ref7_canonical_route"]
    require(ref7 == {"origin_identity": "D74-006", "status": "GROUND_NOT_FOUND", "canonical_owner": "PHASE-071-PRIMARY-SOURCE-ACQUISITION", "target_phase": 71, "external_authority_promoted": False, "acceptance_criterion": next(row for row in active if row["origin_identity"] == "D74-006")["acceptance_criterion"]}, "E_REF7_PROMOTION")
    summary = obj["gate_summary"]
    require(summary["ownerless_active_obligations"] == summary["multiply_owned_active_obligations"] == summary["lost_inherited_ids"] == summary["external_authority_promotions"] == 0, "E_GATE_SUMMARY")
    require(summary["phase_ceiling"] == "CONDITIONAL_P066", "E_PHASE_CEILING")
    require(summary["active_obligations"] == 219 and summary["owner_registry_records"] == 355 and summary["step76_80_records"] == 68, "E_GATE_COUNTS")


def verify_docs() -> None:
    for path, expected_sha in DOC_SHA256.items():
        require(sha256((ROOT / path).read_bytes()) == expected_sha, "E_DOC_SHA", path)
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    parent = (ROOT / PARENT_LEDGER).read_text(encoding="utf-8")
    active = (ROOT / ACTIVE_LEDGER).read_text(encoding="utf-8")
    handover = (ROOT / HANDOVER).read_text(encoding="utf-8")
    for marker in ["433", "167", "95", "CONDITIONAL_P066", "GROUND_NOT_FOUND", "PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS"]:
        require(marker in result, "E_RESULT_MARKER", marker)
    for document, code in [(parent, "E_PARENT_LEDGER"), (active, "E_ACTIVE_LEDGER"), (handover, "E_HANDOVER")]:
        require("Step 81.1" in document and "PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS" in document, code)
        require("ec02d8e0017c4441d9d02c08e22ad432b8c47bc5" in document, code + "_PARENT")
    require("현재 Phase 상태: Phase 066 `CONDITIONAL_PENDING_PERSISTENCE`" in handover, "E_HANDOVER_CURRENT_STATE")
    require("Step 80 profile/default/temperature verification is current at `PASS_PENDING_PERSISTENCE`" not in handover, "E_HANDOVER_STALE_STEP80")
    require("Run Step 81.1 content validation" in handover and "Step 81.2 starts only after" in handover, "E_HANDOVER_NEXT")


def source_policy_text(source: str) -> int:
    tree = ast.parse(source)
    runtime_key = (sys.version_info.major, sys.version_info.minor)
    require(runtime_key in BUILDER_POLICY_AST_SHA256, "E_SOURCE_POLICY_RUNTIME")
    require(sha256(ast.dump(tree, include_attributes=False).encode("utf-8")) == BUILDER_POLICY_AST_SHA256[runtime_key], "E_SOURCE_POLICY_AST_SHA")
    expected_imports = [
        ("from", "__future__", 0, (("annotations", None),)),
        ("import", None, 0, (("argparse", None),)),
        ("import", None, 0, (("hashlib", None),)),
        ("import", None, 0, (("json", None),)),
        ("import", None, 0, (("os", None),)),
        ("import", None, 0, (("re", None),)),
        ("import", None, 0, (("subprocess", None),)),
        ("import", None, 0, (("tempfile", None),)),
        ("from", "collections", 0, (("Counter", None), ("defaultdict", None))),
        ("from", "pathlib", 0, (("Path", None),)),
        ("from", "typing", 0, (("Any", None),)),
    ]
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(("import", None, 0, tuple((alias.name, alias.asname) for alias in node.names)))
        elif isinstance(node, ast.ImportFrom):
            imports.append(("from", node.module, node.level, tuple((alias.name, alias.asname) for alias in node.names)))
    require(imports == expected_imports, "E_SOURCE_POLICY_IMPORT", repr(imports))
    require(sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)) == len(expected_imports), "E_SOURCE_POLICY_NESTED_IMPORT")
    parent: dict[ast.AST, ast.AST] = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}

    def containing_function(node: ast.AST) -> str:
        current = node
        while current in parent:
            current = parent[current]
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return current.name
        return "<module>"

    allowed_name_calls = {"Counter", "Path", "RuntimeError", "SystemExit", "ValueError", "add", "all", "atomic_write_pair", "bool", "build_carry", "build_source", "canonical", "compact", "defaultdict", "dict", "enumerate", "int", "len", "load_inputs", "main", "max", "min", "next", "phase057_adjudications", "phase057_target", "print", "range", "record_sha", "require", "reversed", "run_git", "seal", "set", "sha256", "sorted", "source_classification", "staged_bytes", "step_records", "strict_load", "sum"}
    sensitive_attrs = {"system", "popen", "Popen", "run", "check_call", "check_output", "remove", "unlink", "replace", "rename", "rmdir", "removedirs", "mkdir", "makedirs", "write_text", "write_bytes", "open", "touch", "fdopen", "read_bytes"}
    expected_sensitive_calls = {
        "subprocess.run(['git', *args], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)",
        "path.parent.mkdir(parents=True, exist_ok=True)",
        "os.fdopen(descriptor, 'wb')",
        "os.unlink(temporary)",
        "path.read_bytes()",
        "os.replace(staged[path], path)",
        "os.unlink(path)",
        "os.replace(backup, path)",
    }
    observed_sensitive_calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            require(not node.attr.startswith("__"), "E_SOURCE_POLICY_DUNDER_ATTRIBUTE")
            if node.attr in sensitive_attrs:
                owner = parent.get(node)
                require(isinstance(owner, ast.Call) and owner.func is node, "E_SOURCE_POLICY_INDIRECT_ATTRIBUTE", ast.unparse(node))
                observed_sensitive_calls.append(ast.unparse(owner))
        if isinstance(node, ast.Call):
            require(isinstance(node.func, (ast.Name, ast.Attribute)), "E_SOURCE_POLICY_INDIRECT_CALL", ast.dump(node.func, include_attributes=False))
            if isinstance(node.func, ast.Name):
                require(node.func.id in allowed_name_calls, "E_SOURCE_POLICY_NAME_CALL", node.func.id)
    require(set(observed_sensitive_calls) == expected_sensitive_calls and len(observed_sensitive_calls) == 9, "E_SOURCE_POLICY_SENSITIVE_CALLS", repr(observed_sensitive_calls))
    reserved = allowed_name_calls | {"argparse", "hashlib", "json", "os", "re", "subprocess", "tempfile", "Counter", "defaultdict", "Path", "Any"}
    require(not {node.id for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)} & reserved, "E_SOURCE_POLICY_RESERVED_REBIND")
    require(source.count("def atomic_write_pair(") == 1 and source.count("atomic_write_pair([") == 1, "E_SOURCE_POLICY_WRITE")
    return len(list(ast.walk(tree)))


def source_policy() -> int:
    return source_policy_text((ROOT / BUILDER_PATH).read_text(encoding="utf-8"))


def source_policy_negative_tests() -> int:
    source = (ROOT / BUILDER_PATH).read_text(encoding="utf-8")
    mutations = [
        source.replace("import os\n", "import os\nfrom os import remove as r\n", 1),
        source.replace("def require(", "filesystem_escape = os.system\n\ndef require(", 1),
        source.replace("def require(", "Path('escape').write_text('x')\n\ndef require(", 1),
        source.replace("def require(", "os.remove('escape')\n\ndef require(", 1),
        source.replace("def require(", "os.__dict__['system']('x')\n\ndef require(", 1),
        source.replace("def require(", "getattr(os, 'system')('x')\n\ndef require(", 1),
        source.replace("def require(", "subprocess.Popen(['x'])\n\ndef require(", 1),
        source.replace("def require(", "Path('escape').unlink()\n\ndef require(", 1),
        source.replace("def require(", "def nested_import_escape():\n    import socket\n    return socket.socket()\n\ndef require(", 1),
    ]
    passed = 0
    for mutated in mutations:
        try:
            source_policy_text(mutated)
        except (RuntimeError, SyntaxError):
            passed += 1
        else:
            raise RuntimeError("E_SOURCE_POLICY_NEGATIVE_ACCEPTED")
    return passed


def transaction_negative_test(builder: Any) -> int:
    with tempfile.TemporaryDirectory(prefix="p066_step81_pair_") as temporary:
        root = Path(temporary)
        first = root / "first.json"
        second = root / "second.json"
        first.write_bytes(b"old-first")
        second.write_bytes(b"old-second")
        original_replace = builder.os.replace
        calls = 0

        def rejecting_replace(source: str, destination: str | Path) -> None:
            nonlocal calls
            if str(destination) == str(second) and str(source).endswith(".tmp"):
                calls += 1
                raise OSError("injected second replace failure")
            original_replace(source, destination)

        builder.os.replace = rejecting_replace
        try:
            try:
                builder.atomic_write_pair([(first, b"new-first"), (second, b"new-second")])
            except OSError:
                pass
            else:
                raise RuntimeError("E_TRANSACTION_FAILURE_ACCEPTED")
        finally:
            builder.os.replace = original_replace
        require(calls == 1 and first.read_bytes() == b"old-first" and second.read_bytes() == b"old-second", "E_TRANSACTION_ROLLBACK")
    return 1


def negative_tests(source: dict[str, Any], carry: dict[str, Any], builder: Any, inputs: dict[str, Any], expected_source: dict[str, Any], expected_carry: dict[str, Any]) -> int:
    cases: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    mutations = [
        ("drop occurrence", lambda d, c: d["source_dispositions"].pop()),
        ("duplicate disposition", lambda d, c: d["source_dispositions"].append(copy.deepcopy(d["source_dispositions"][0]))),
        ("blob projection drift", lambda d, c: d["blob_disposition_groups"][0].__setitem__("occurrence_count", 999)),
        ("fold supplemental", lambda d, c: d["supplemental_dispositions"].pop()),
        ("stale closure", lambda d, c: d["source_dispositions"].__setitem__(next(i for i, r in enumerate(d["source_dispositions"]) if r["release_build_disposition"] == "WITHHOLD" and r["source_path"].endswith(".pdf")), {**next(r for r in d["source_dispositions"] if r["release_build_disposition"] == "WITHHOLD" and r["source_path"].endswith(".pdf")), "release_build_disposition": "PRESERVE"})),
        ("process orphan", lambda d, c: d["process_commit_coverage"].__setitem__("release_orphan_count", 1)),
        ("lost inherited", lambda d, c: c["inherited_phase065_observations"].pop()),
        ("AY duplicate", lambda d, c: c["current_owner_duplicate_check_universe"]["records"].append(copy.deepcopy(c["current_owner_duplicate_check_universe"]["records"][0]))),
        ("ownerless", lambda d, c: c["active_obligations"][0].__setitem__("canonical_owner", "")),
        ("Ref7 promotion", lambda d, c: c["ref7_canonical_route"].__setitem__("status", "VERIFIED")),
        ("physical promotion", lambda d, c: next(r for r in c["step76_80_disposition_records"] if r["observation_id"] == "P066-P79-03")["authority_axes"]["physical"].__setitem__("authority", True)),
        ("optimizer substitution", lambda d, c: next(r for r in c["step76_80_disposition_records"] if r["observation_id"].startswith("P066-S78-ORIGINAL-STATE-")).__setitem__("disposition", "PRESERVE")),
        ("dangling relation", lambda d, c: next(r for r in c["step76_80_disposition_records"] if r["observation_id"] == "P066-S77-OPTIMIZER-CONTRACT")["relation_links"].__setitem__(0, "P066-MISSING")),
        ("extra active", lambda d, c: c["active_obligations"].append({"obligation_id": "P066-OBL-EXTRA", "origin_identity": "P066-E79-01", "state": "OPEN_CARRY", "canonical_owner": "P066-STEP81-DISPOSITION", "target_phase": 66, "acceptance_criterion": "invalid", "semantic_fingerprint": "0" * 64, "relation_links": [], "external_authority_promoted": False})),
        ("missing AO", lambda d, c: c["phase057_route_adjudications"].pop(0)),
        ("step80 closure", lambda d, c: next(r for r in c["step76_80_disposition_records"] if r["observation_id"] == "P066-S80-EVIDENCE-STALE_HEADER_COMMENT").__setitem__("state", "BOUNDED_INTERNAL")),
    ]
    passed = 0
    for name, mutation in mutations:
        d = copy.deepcopy(source)
        c = copy.deepcopy(carry)
        mutation(d, c)
        d["semantic_sha256"] = sha256(compact({key: value for key, value in d.items() if key != "semantic_sha256"}))
        c["semantic_sha256"] = sha256(compact({key: value for key, value in c.items() if key != "semantic_sha256"}))
        try:
            validate_source(d, builder, expected_source, check_recompute=False)
            validate_carry(c, builder, expected_carry, inputs, check_recompute=False)
        except RuntimeError:
            passed += 1
        else:
            raise RuntimeError(f"E_NEGATIVE_ACCEPTED:{name}")
    return passed


def parse_status(raw: bytes) -> set[str]:
    paths: set[str] = set()
    fields = raw.decode("utf-8", errors="strict").split("\0")
    for field in fields:
        if not field:
            continue
        require(len(field) >= 4, "E_STATUS_PARSE")
        path = field[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.add(path.replace("\\", "/"))
    return paths


def status_map(raw: bytes) -> dict[str, str]:
    result: dict[str, str] = {}
    for field in raw.decode("utf-8", errors="strict").split("\0"):
        if not field:
            continue
        require(len(field) >= 4 and " -> " not in field[3:], "E_STATUS_SHAPE")
        path = field[3:].replace("\\", "/")
        require(path not in result, "E_STATUS_DUPLICATE")
        result[path] = field[:2]
    return result


def verify_stage() -> None:
    staged = set(git("diff", "--cached", "--name-only", "-z").decode().split("\0")) - {""}
    require(staged == EXACT_PATHS, "E_EXACT_STAGE", repr(sorted(staged ^ EXACT_PATHS)))
    statuses = status_map(git("status", "--porcelain=v1", "-z"))
    require(set(statuses) == EXACT_PATHS, "E_EXACT_STATUS", repr(sorted(set(statuses) ^ EXACT_PATHS)))
    expected_status = {path: ("A " if path in {BUILDER_PATH, VALIDATOR_PATH, DISPOSITION_PATH, CARRY_PATH, RESULT_PATH} else "M ") for path in EXACT_PATHS}
    require(statuses == expected_status, "E_EXACT_STATUS_MODES", repr(statuses))
    require(not git("diff", "--name-only"), "E_UNSTAGED")
    require(git("rev-parse", "HEAD").decode().strip() == EXPECTED_PARENT, "E_PRECOMMIT_HEAD")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_PRECOMMIT_BRANCH")
    require(git("rev-parse", "@{upstream}").decode().strip() == EXPECTED_PARENT, "E_PRECOMMIT_UPSTREAM")
    require(live_tip(f"refs/heads/{BRANCH}") == EXPECTED_PARENT, "E_PRECOMMIT_LIVE")
    require(git("rev-parse", "refs/heads/codex/lib-physics-endgame-v1025_2").decode().strip() == PROTECTED, "E_PRECOMMIT_PROTECTED_LOCAL")
    require(git("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2").decode().strip() == PROTECTED and live_tip("refs/heads/codex/lib-physics-endgame-v1025_2") == PROTECTED, "E_PRECOMMIT_PROTECTED_REMOTE")
    require(git("rev-parse", "refs/remotes/origin/main").decode().strip() == MAIN and live_tip("refs/heads/main") == MAIN, "E_PRECOMMIT_MAIN")
    for path in EXACT_PATHS:
        index_line = git("ls-files", "-s", "--", path).decode().strip().split()
        require(len(index_line) >= 4 and index_line[0] == "100644", "E_INDEX_MODE", path)
        worktree_blob = git("hash-object", "--path", path, path).decode().strip()
        require(index_line[1] == worktree_blob, "E_INDEX_WORKTREE_BLOB", path)


def live_tip(ref: str) -> str:
    lines = git("ls-remote", "origin", ref).decode().strip().splitlines()
    require(len(lines) == 1, "E_LIVE_REF", ref)
    return lines[0].split()[0]


def verify_persistence(expected_commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None, "E_EXPECTED_COMMIT")
    head = git("rev-parse", "HEAD").decode().strip()
    require(head == expected_commit, "E_HEAD")
    require(git("rev-parse", "HEAD^").decode().strip() == EXPECTED_PARENT, "E_PARENT")
    require(git("show", "-s", "--format=%s", "HEAD").decode().strip() == EXPECTED_SUBJECT, "E_SUBJECT")
    changed = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").decode().splitlines())
    require(changed == EXACT_PATHS, "E_COMMIT_PATHS")
    require(not git("status", "--porcelain=v1"), "E_DIRTY")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "@{upstream}").decode().strip() == head, "E_UPSTREAM")
    require(live_tip(f"refs/heads/{BRANCH}") == head, "E_LIVE_ACTIVE")
    require(git("rev-parse", "refs/heads/codex/lib-physics-endgame-v1025_2").decode().strip() == PROTECTED, "E_PROTECTED_LOCAL")
    require(git("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2").decode().strip() == PROTECTED, "E_PROTECTED_REMOTE")
    require(live_tip("refs/heads/codex/lib-physics-endgame-v1025_2") == PROTECTED, "E_PROTECTED_LIVE")
    require(git("rev-parse", "refs/remotes/origin/main").decode().strip() == MAIN, "E_MAIN_REMOTE")
    require(live_tip("refs/heads/main") == MAIN, "E_MAIN_LIVE")
    require(not git("diff", "--name-only", f"{EXPECTED_PARENT}..HEAD", "--", "Claude"), "E_CLAUDE_MUTATION")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require(not (args.staged and args.persistence), "E_MODE")
    require((args.expected_commit is not None) == args.persistence, "E_EXPECTED_COMMIT_MODE")
    nodes = source_policy()
    policy_negatives = source_policy_negative_tests()
    builder = load_builder()
    source_raw = (ROOT / DISPOSITION_PATH).read_bytes()
    carry_raw = (ROOT / CARRY_PATH).read_bytes()
    source = strict_load(source_raw)
    carry = strict_load(carry_raw)
    inputs, metadata = builder.load_inputs()
    expected_source = builder.build_source(inputs, metadata)
    expected_carry = builder.build_carry(inputs, metadata, expected_source)
    validate_source(source, builder, expected_source)
    validate_carry(carry, builder, expected_carry, inputs)
    verify_docs()
    negatives = negative_tests(source, carry, builder, inputs, expected_source, expected_carry)
    transaction = transaction_negative_test(builder)
    subprocess.run([sys.executable, "-B", "-X", "utf8", str(ROOT / BUILDER_PATH)], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require((ROOT / DISPOSITION_PATH).read_bytes() == source_raw and (ROOT / CARRY_PATH).read_bytes() == carry_raw, "E_DETERMINISM_1")
    subprocess.run([sys.executable, "-B", "-X", "utf8", str(ROOT / BUILDER_PATH)], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require((ROOT / DISPOSITION_PATH).read_bytes() == source_raw and (ROOT / CARRY_PATH).read_bytes() == carry_raw, "E_DETERMINISM_2")
    if args.staged:
        verify_stage()
    if args.persistence:
        verify_persistence(args.expected_commit)
        print(f"PASS_P066_STEP81_1_PERSISTENCE commit={args.expected_commit} negative={negatives}/{negatives} source_policy={policy_negatives}/{policy_negatives} transaction={transaction}/{transaction}")
    else:
        print(f"PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS negative={negatives}/{negatives} source_policy={policy_negatives}/{policy_negatives} transaction={transaction}/{transaction} ast_nodes={nodes}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
