#!/usr/bin/env python3
"""Validate the Phase 060 Step 43 document-led implementation trace.

This proves bounded source identity, trace coverage, AST reachability, source-
gate attribution, deterministic generation, and authority boundaries.  It does
not promote internal artifacts to literature, physics, or experimental truth.
"""

from __future__ import annotations

import copy
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TRACE_MATRIX = ROOT / "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json"
BUILDER = ROOT / "Codex/work/v1019_phase060/build_phase060_step43_doc_code_trace.py"
TOPOLOGY = ROOT / "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
CODE_PATHS = [
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
    "Claude/docs/v1.0.19/fit_roundtrip_demo.py",
    "Claude/docs/v1.0.19/graph_suite_v1019.py",
    "Claude/docs/v1.0.19/test_regression_v1019.py",
]
MAIN_CODE = CODE_PATHS[0]

AUTH_LEXICAL = "LEXICAL_SOURCE_ANCHOR_ONLY_NOT_SCIENTIFIC_TRUTH"
AUTH_CODE = "FROZEN_SOURCE_BEHAVIOR_NOT_SCIENTIFIC_TRUTH"
AUTH_TEST = "INTERNAL_SOURCE_GATE_NOT_EXPERIMENTAL_VALIDATION"
AUTH_ARTIFACT = "STORED_OR_REBUILT_ARTIFACT_NOT_SCIENTIFIC_TRUTH"
AUTH_TRACE = "IMPLEMENTATION_CONFORMANCE_ONLY_EXTERNAL_TRUTH_DEFERRED"

TOP_KEYS = {
    "schema_version", "phase", "step", "source_commit", "generation",
    "authority_policy", "enumerations", "input_evidence",
    "candidate_dispositions", "document_obligations",
    "public_entry_obligations", "implementation_definitions",
    "call_edge_index", "test_gate_index", "artifact_consumer_index",
    "optional_input_disposition_groups", "trace_rows", "contradiction_routes",
    "findings", "fingerprints", "gate_summary",
}
INPUT_HASHES = {
    "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json": "c246a05e2d13d1d33dab1682bda712611367412d241cd277694a35aaf7bcf140",
    "Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json": "36616b86f934b7c594e68e1b991c261c7b391b70e2c4c52375d452b3d69a06ad",
    "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json": "d61e514712a91b7eea89e723cf33745b00a20ee59387abcb450db778122174f7",
    "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json": "4f38d3678870c32b1910701e62506547f2bc471684ceb0578775ba29fb57e2af",
    "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json": "9fc8d1f4bd797c394effe5d72771cca0a3d4b6426e53c3a2d95d0f9f5e446bcf",
}
EXPECTED_FINGERPRINTS = {
    "artifact_consumer_index": "fa03c58fef34e31b76a3eb37a5ba4dae21dacb9c200ec1e3a672dde59ded3e2f",
    "call_edge_index": "7b81889533c4d67bd02f98405ef952226d8e2ce1a6d72681b1c6c4dce462880b",
    "candidate_dispositions": "0f851a1212b522e99c3a1ce00dfae8f93023506443370da0df3ed51ed01851e1",
    "contradiction_routes": "0fe61b3866e94e70dbc846c2df5da23d9c4de61786c20f6e6e4062f8376c75ab",
    "document_obligations": "a908cc2389caac7046992dce4fdc22ac5702bd2a4eb0d4903978a2d99d332f11",
    "findings": "1bd3b928a9720672684672c1fcc0738d1783ce3cc669499f6f8a15ded2e56e6a",
    "implementation_definitions": "ee23a46a3db64513843a2db979fe31f4a26d9a0631b5d27b3f45fb1a9dea4b55",
    "optional_input_disposition_groups": "97cffdbc8f10238ef4bd450b2efcb736d3839991cb3fdccdd6dccc7634c424b6",
    "public_entry_obligations": "2723aa20e553177527c0d9efb78ce615a55cc2dfd266715dfc951b7cf7996bc6",
    "test_gate_index": "162490cf968a5cfff0c6dc06a5c8b141defaa28115e3902f75d17d001ef3a121",
    "trace_rows": "53e3c695be80c0c3899e50656eb7c9cd3fb6fcb5faa297e080d6e46346ef9f42",
}
TRACE_IDS = [
    "TRC-CH1-CHARGE-BALANCE", "TRC-CH1-CENTER-THERMO", "TRC-CH1-HYSTERESIS",
    "TRC-CH1-WIDTH-LOGISTIC", "TRC-CH1-BROADENING-BUDGET", "TRC-CH1-LAG-LENGTH",
    "TRC-CH1-TAIL-CAUSAL", "TRC-CH1-LOW-CURRENT-HYS-LIMIT",
    "TRC-CH1-REVERSIBLE-BASELINE", "TRC-CH1-LCO-DIRECTION-CENTER",
    "TRC-CH1-LCO-HYSTERESIS", "TRC-CH1-LCO-ENTROPY-ELECTRONIC",
    "TRC-CH1-LCO-PEAK", "TRC-CH1-MSMR-MAP", "TRC-CH1-LCO-FULL-PLUGIN",
    "TRC-CH2-PARTITION-LOGISTIC", "TRC-CH2-PARTITION-BW",
    "TRC-CH2-CONFIGURATIONAL", "TRC-CH2-VIBRATIONAL-ELECTRONIC",
    "TRC-CH2-EINSTEIN-ROUNDTRIP", "TRC-CH2-MIXING-IMPLICIT",
    "TRC-CH2-MIXING-WEIGHTED", "TRC-CH2-WIDTH-T-DEPENDENCE",
    "TRC-CH2-HYSTERESIS-REVERSIBLE", "TRC-CH2-REVERSIBLE-HEAT",
    "TRC-CH2-COMPLETE-SYNTHESIS", "TRC-CH2-REGRESSION-WITNESSES",
    "TRC-CH2-DOC-LEADS-BOUNDARY",
]
FOCUS_FAMILIES = {
    "CH1_CHARGE_BALANCE", "CH1_CENTERS", "CH1_HYSTERESIS", "CH1_WIDTH",
    "CH1_BROADENING", "CH1_LAG_TAIL", "CH1_LCO", "CH1_MSMR",
    "CH2_PARTITION", "CH2_CONFIG", "CH2_VIBRATIONAL", "CH2_ELECTRONIC",
    "CH2_MIXING", "CH2_REVERSIBLE_HEAT",
}
PRODUCTION = [
    ("func_w", 82, 83), ("func_U_j", 86, 87), ("func_ksi_eq", 90, 93),
    ("func_L_q", 96, 103), ("func_dU_hys", 139, 146),
    ("func_U_branch", 149, 153), ("func_dH_a_eff", 157, 160),
    ("func_chi_d", 163, 168), ("func_dSe_molar", 175, 191),
    ("GraphiteAnodeDischargeDQDV", 220, 856),
    ("GraphiteAnodeDischargeDQDV.equilibrium", 450, 467),
    ("GraphiteAnodeDischargeDQDV.dqdv", 470, 586),
    ("GraphiteAnodeDischargeDQDV.curve", 589, 619),
    ("GraphiteAnodeDischargeDQDV.entropy_coefficient", 633, 694),
    ("GraphiteAnodeDischargeDQDV.reversible_heat", 696, 707),
    ("GraphiteAnodeDischargeDQDV.solve_U_oc", 710, 788),
    ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", 790, 817),
    ("GraphiteAnodeDischargeDQDV.reversible_heat_x", 819, 830),
    ("GraphiteAnodeDischargeDQDV.irreversible_heat", 832, 840),
    ("LCOCathodeDQDV", 891, 934),
]
CANDIDATE_KINDS = {
    "DISPLAYED_EQUATION", "DEFINITION_CANDIDATE", "ASSUMPTION_CANDIDATE",
    "SIGN_UNIT_DECLARATION_CANDIDATE", "CODE_MENTION_CANDIDATE",
    "FORWARD_REFERENCE_CANDIDATE",
}

GENERATION_KEYS = {"builder", "ordering", "json", "authority_boundary"}
AUTHORITY_POLICY_KEYS = {"document", "implementation", "test", "artifact", "trace", "scientific_truth"}
ENUMERATION_KEYS = {
    "relation", "status", "implementation_disposition", "candidate_disposition",
    "reachability", "execution_state", "consumer_anchor_disposition",
}
INPUT_KEYS = {"evidence_id", "path", "sha256", "size_bytes", "authority_boundary"}
CANDIDATE_KEYS = {"anchor_id", "path", "line_start", "line_end", "kind", "text_sha256", "disposition", "trace_ids", "authority_boundary"}
DOC_KEYS = {"claim_id", "trace_id", "focus_family", "topic", "summary", "theory_anchors", "authority_boundary"}
ANCHOR_KEYS = {"anchor_id", "path", "git_blob_sha1", "start_line", "end_line", "slice_sha256", "topology_anchor_ids", "authority_boundary"}
PUBLIC_KEYS = {"definition_id", "path", "qualified_name", "lines", "entry_scope", "trace_ids", "exclusion_reason", "authority_boundary"}
DEFINITION_KEYS = {"definition_id", "path", "git_blob_sha1", "qualified_name", "kind", "start_line", "end_line", "slice_sha256", "public_entry", "authority_boundary"}
EDGE_KEYS = {"edge_id", "path", "git_blob_sha1", "caller", "callee", "line", "col_offset", "ordinal", "ast_sha256", "authority_boundary"}
GATE_KEYS = {"gate_id", "path", "git_blob_sha1", "start_line", "end_line", "slice_sha256", "gate_semantics", "claim_type", "enforcement", "authority_boundary"}
SOURCE_ANCHOR_KEYS = {"path", "git_blob_sha1", "start_line", "end_line", "slice_sha256", "authority_boundary"}
CONSUMER_KEYS = {"consumer_id", "artifact_path", "artifact_kind", "git_blob_sha1", "sha256", "ground_status", "consumer_source_anchors", "consumer_anchor_disposition", "authority_boundary"}
OPTIONAL_GROUP_KEYS = {"group_id", "label", "member_names", "acceptance", "runtime_disposition", "evidence", "authority_boundary"}
TRACE_KEYS = {"trace_id", "claim_id", "focus_family", "topic", "theory_anchor_ids", "implementation_definition_ids", "call_paths", "test_gate_ids", "assertion_gate_ids", "artifact_consumer_ids", "relation", "status", "implementation_disposition", "execution_state", "reachability", "unit_check", "sign_check", "test_evidence_disposition", "scientific_truth", "authority_boundary"}
CALL_PATH_KEYS = {"path_id", "edge_ids", "definition_chain_ids", "definition_chain_names", "path_disposition", "authority_boundary"}
UNIT_KEYS = {"status", "statement", "document_anchor_ids", "implementation_definition_ids", "assertion_gate_ids"}
SIGN_KEYS = UNIT_KEYS | {"polarity"}
CONTRADICTION_KEYS = {"contradiction_id", "trace_ids", "disposition", "gate", "authority_boundary"}
FINDING_KEYS = {"id", "summary", "route"}
GATE_SUMMARY_KEYS = {
    "candidate_records", "candidate_disposition_orphan_count", "curated_overlap_anchor_records",
    "curated_document_obligations", "curated_doc_row_orphan_count", "focus_families_required",
    "focus_family_missing_count", "definitions_full_ast", "call_nodes_full_ast",
    "step42_definition_records", "step42_definition_body_call_edges", "public_entries_all",
    "production_public_entries", "support_public_entries", "public_call_orphan_count",
    "source_gates", "python_assert_nodes", "artifact_consumers", "optional_disposition_groups",
    "optional_member_names", "invalid_anchor_count", "missing_authority_boundary_count",
    "P0", "P1", "P2", "gate_result",
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


@lru_cache(maxsize=None)
def strict_json_load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          ValueError(f"non-finite JSON number: {value}")))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_fingerprint(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":"), allow_nan=False).encode("utf-8"))


def git_bytes(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


@lru_cache(maxsize=None)
def raw_blob(path: str) -> bytes:
    return git_bytes("cat-file", "blob", f"{SOURCE_COMMIT}:{path}")


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def independent_ast_inventory(path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw = raw_blob(path)
    source = raw.decode("utf-8-sig")
    source_lines = source.splitlines()
    tree = ast.parse(source, filename=path)
    definitions: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    scope: list[str] = []
    ordinal = 0

    def definition_record(node: ast.AST, qualified_name: str, kind: str) -> dict[str, Any]:
        return {
            "definition_id": f"DEF:{path}:{qualified_name}:{node.lineno}-{node.end_lineno}",
            "path": path,
            "git_blob_sha1": git_blob_sha1(raw),
            "qualified_name": qualified_name,
            "kind": kind,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "slice_sha256": sha256_bytes("\n".join(source_lines[node.lineno - 1:node.end_lineno]).encode("utf-8")),
            "public_entry": not qualified_name.split(".")[-1].startswith("_"),
            "authority_boundary": AUTH_CODE,
        }

    class InventoryVisitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            qualified_name = ".".join(scope + [node.name])
            definitions.append(definition_record(node, qualified_name, "class"))
            scope.append(node.name)
            self.generic_visit(node)
            scope.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            qualified_name = ".".join(scope + [node.name])
            if scope and scope[-1] == "solve_U_oc" and node.name == "_charge":
                qualified_name = "GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge"
            definitions.append(definition_record(node, qualified_name, "function"))
            scope.append(node.name)
            self.generic_visit(node)
            scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, node: ast.Call) -> None:
            nonlocal ordinal
            ordinal += 1
            caller = ".".join(scope) if scope else "<module>"
            if scope == ["GraphiteAnodeDischargeDQDV", "solve_U_oc", "_charge"]:
                caller = "GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge"
            try:
                callee = ast.unparse(node.func)
            except Exception:
                callee = type(node.func).__name__
            calls.append({
                "edge_id": f"EDGE:{path}:{node.lineno}:{node.col_offset}:{ordinal:04d}",
                "path": path,
                "git_blob_sha1": git_blob_sha1(raw),
                "caller": caller,
                "callee": callee,
                "line": node.lineno,
                "col_offset": node.col_offset,
                "ordinal": ordinal,
                "ast_sha256": sha256_bytes(ast.dump(node, include_attributes=False).encode("utf-8")),
                "authority_boundary": AUTH_CODE,
            })
            self.generic_visit(node)

    InventoryVisitor().visit(tree)
    definitions.sort(key=lambda item: (item["start_line"], item["end_line"], item["qualified_name"]))
    calls.sort(key=lambda item: (item["line"], item["col_offset"], item["ordinal"]))
    return definitions, calls


def independently_rebuild_ast() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    definitions: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    for path in CODE_PATHS:
        path_definitions, path_calls = independent_ast_inventory(path)
        definitions.extend(path_definitions)
        calls.extend(path_calls)
    return definitions, calls


def independent_class_bases(path: str, class_name: str) -> list[str]:
    tree = ast.parse(raw_blob(path).decode("utf-8-sig"), filename=path)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return [ast.unparse(base) for base in node.bases]
    return []


def independent_method_contract(path: str, class_name: str, method_name: str,
                                parameter_name: str, assignment_target: str) -> tuple[str | None, bool]:
    tree = ast.parse(raw_blob(path).decode("utf-8-sig"), filename=path)
    for class_node in tree.body:
        if not isinstance(class_node, ast.ClassDef) or class_node.name != class_name:
            continue
        for method in class_node.body:
            if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) or method.name != method_name:
                continue
            positional = list(method.args.posonlyargs) + list(method.args.args)
            default_by_name: dict[str, ast.expr] = {}
            for arg, default in zip(positional[-len(method.args.defaults):], method.args.defaults):
                default_by_name[arg.arg] = default
            for arg, default in zip(method.args.kwonlyargs, method.args.kw_defaults):
                if default is not None:
                    default_by_name[arg.arg] = default
            default = default_by_name.get(parameter_name)
            assigned = any(
                isinstance(node, (ast.Assign, ast.AnnAssign))
                and any(
                    isinstance(target, ast.Attribute)
                    and ast.unparse(target) == assignment_target
                    for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
                )
                and isinstance(node.value, ast.Name)
                and node.value.id == parameter_name
                for node in ast.walk(method)
            )
            return (ast.unparse(default) if default is not None else None), assigned
    return None, False


def edge_targets_definition(edge: dict[str, Any], target_name: str, path_disposition: str) -> bool:
    callee = edge.get("callee")
    caller = edge.get("caller", "")
    if callee == target_name:
        return True
    if callee == "_charge" and target_name == "GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge":
        return caller == "GraphiteAnodeDischargeDQDV.solve_U_oc"
    if isinstance(callee, str) and callee.startswith("self."):
        method = callee[5:]
        if target_name == f"{caller.split('.', 1)[0]}.{method}":
            return True
        if target_name == f"GraphiteAnodeDischargeDQDV.{method}":
            return True
        if (path_disposition == "ORDERED_CONTIGUOUS_DYNAMIC_DISPATCH_PATH"
                and caller.startswith("GraphiteAnodeDischargeDQDV.")
                and target_name == f"LCOCathodeDQDV.{method}"):
            return True
        if (path_disposition == "ORDERED_CONTIGUOUS_DYNAMIC_DISPATCH_PATH"
                and caller == "GraphiteAnodeDischargeDQDV._chi_d"
                and callee == "self.chi_split" and target_name == "func_chi_d"):
            return True
    return False


def validate_matrix(matrix: dict[str, Any]) -> tuple[list[str], int]:
    errors: list[str] = []
    checks = 0

    def check(condition: bool, code: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(code)

    def check_keys(value: Any, expected: set[str], code: str) -> None:
        check(isinstance(value, dict) and set(value) == expected, code)

    check(set(matrix) == TOP_KEYS, "schema.top_keys")
    check(matrix.get("schema_version") == 2, "schema.version")
    check(matrix.get("phase") == 60 and matrix.get("step") == 43, "schema.phase_step")
    check(matrix.get("source_commit") == SOURCE_COMMIT, "schema.source_commit")
    check_keys(matrix.get("generation"), GENERATION_KEYS, "schema.generation_keys")
    authority = matrix.get("authority_policy", {})
    check_keys(authority, AUTHORITY_POLICY_KEYS, "schema.authority_policy_keys")
    check(authority.get("document") == AUTH_LEXICAL, "authority.document")
    check(authority.get("implementation") == AUTH_CODE, "authority.code")
    check(authority.get("test") == AUTH_TEST, "authority.test")
    check(authority.get("artifact") == AUTH_ARTIFACT, "authority.artifact")
    check(authority.get("trace") == AUTH_TRACE, "authority.trace")
    enumerations = matrix.get("enumerations", {})
    check_keys(enumerations, ENUMERATION_KEYS, "schema.enumeration_keys")
    check(enumerations.get("relation") == ["DIRECT", "RELATED_NOT_DIRECT", "NOT_APPLICABLE"], "schema.enum_relation")
    check(enumerations.get("reachability") == ["ACTIVE", "CONDITIONALLY_REACHABLE_DEFAULT_DORMANT", "NOT_REQUIRED_RELATED", "NO_CHAIN_IMPLEMENTATION_ABSENT"], "schema.enum_reachability")
    check(enumerations.get("consumer_anchor_disposition") == ["EXACT_FROZEN_TEX_SOURCE_ANCHOR", "EXACT_FROZEN_GENERATOR_ANCHOR", "EXACT_FROZEN_CONSUMER_AND_CAPTURE_ANCHOR", "NO_FROZEN_GENERATOR_GROUND"], "schema.enum_consumer_anchor")

    inputs = matrix.get("input_evidence", [])
    for item in inputs:
        check_keys(item, INPUT_KEYS, f"schema.input:{item.get('evidence_id') if isinstance(item, dict) else 'non_dict'}")
    by_input = {x.get("path"): x for x in inputs if isinstance(x, dict)}
    check(len(inputs) == len(by_input) == len(INPUT_HASHES) and set(by_input) == set(INPUT_HASHES), "inputs.paths")
    for path, expected in INPUT_HASHES.items():
        item = by_input.get(path, {})
        check(item.get("sha256") == expected == sha256_bytes((ROOT / path).read_bytes()), f"inputs.sha:{path}")
        check(item.get("size_bytes") == (ROOT / path).stat().st_size, f"inputs.size:{path}")
        check(item.get("authority_boundary") == AUTH_TRACE, f"inputs.authority:{path}")

    topology = strict_json_load(TOPOLOGY)
    source_records = [x for x in topology["content_index"]["records"] if x["kind"] in CANDIDATE_KINDS]
    source_by_id = {x["anchor_id"]: x for x in source_records}
    candidates = matrix.get("candidate_dispositions", [])
    for item in candidates:
        check_keys(item, CANDIDATE_KEYS, f"schema.candidate:{item.get('anchor_id') if isinstance(item, dict) else 'non_dict'}")
    candidate_by_id = {x.get("anchor_id"): x for x in candidates if isinstance(x, dict)}
    check(len(candidates) == len(candidate_by_id) == len(source_records) == 914, "candidates.denominator")
    check(set(candidate_by_id) == set(source_by_id), "candidates.id_set")
    for anchor_id, source in source_by_id.items():
        item = candidate_by_id.get(anchor_id, {})
        check(item.get("path") == source["path"], f"candidate.path:{anchor_id}")
        check(item.get("line_start") == source["line_start"] and item.get("line_end") == source["line_end"], f"candidate.lines:{anchor_id}")
        check(item.get("kind") == source["kind"] and item.get("text_sha256") == source["text_sha256"], f"candidate.source:{anchor_id}")
        check(item.get("disposition") in {"OVERLAPS_CURATED_OBLIGATION_ANCHOR", "SUPPORTING_OR_OUTSIDE_STEP43_CURATED_SCOPE"}, f"candidate.disposition:{anchor_id}")
        check(item.get("authority_boundary") == AUTH_LEXICAL, f"candidate.authority:{anchor_id}")

    docs = matrix.get("document_obligations", [])
    traces = matrix.get("trace_rows", [])
    for item in docs:
        check_keys(item, DOC_KEYS, f"schema.doc:{item.get('trace_id') if isinstance(item, dict) else 'non_dict'}")
    for item in traces:
        check_keys(item, TRACE_KEYS, f"schema.trace:{item.get('trace_id') if isinstance(item, dict) else 'non_dict'}")
    trace_ids = [x.get("trace_id") for x in traces if isinstance(x, dict)]
    check(trace_ids == TRACE_IDS, "trace.id_order")
    check([x.get("trace_id") for x in docs] == TRACE_IDS, "documents.id_order")
    check(len(set(trace_ids)) == len(TRACE_IDS), "trace.unique")
    check({x.get("focus_family") for x in traces} == FOCUS_FAMILIES, "trace.focus_families")

    doc_anchor_ids: set[str] = set()
    for doc in docs:
        check(doc.get("authority_boundary") == AUTH_LEXICAL, f"doc.authority:{doc.get('trace_id')}")
        check(bool(doc.get("summary")) and bool(doc.get("theory_anchors")), f"doc.complete:{doc.get('trace_id')}")
        for anchor in doc.get("theory_anchors", []):
            check_keys(anchor, ANCHOR_KEYS, f"schema.doc_anchor:{anchor.get('anchor_id') if isinstance(anchor, dict) else 'non_dict'}")
            aid = anchor.get("anchor_id")
            check(aid not in doc_anchor_ids, f"anchor.duplicate:{aid}")
            doc_anchor_ids.add(aid)
            path = anchor.get("path", "")
            raw = raw_blob(path)
            lines = raw.decode("utf-8-sig").splitlines()
            start, end = anchor.get("start_line"), anchor.get("end_line")
            check(isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= len(lines), f"anchor.bounds:{aid}")
            expected_slice = sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8"))
            check(anchor.get("slice_sha256") == expected_slice, f"anchor.slice:{aid}")
            check(anchor.get("git_blob_sha1") == git_blob_sha1(raw), f"anchor.blob:{aid}")
            check(anchor.get("authority_boundary") == AUTH_LEXICAL, f"anchor.authority:{aid}")
            overlap = [x["anchor_id"] for x in topology["content_index"]["records"]
                       if x["path"] == path and x["line_start"] <= end and x["line_end"] >= start]
            check(anchor.get("topology_anchor_ids") == overlap, f"anchor.topology_join:{aid}")

    definitions = matrix.get("implementation_definitions", [])
    edges = matrix.get("call_edge_index", [])
    for item in definitions:
        check_keys(item, DEFINITION_KEYS, f"schema.definition:{item.get('definition_id') if isinstance(item, dict) else 'non_dict'}")
    for item in edges:
        check_keys(item, EDGE_KEYS, f"schema.edge:{item.get('edge_id') if isinstance(item, dict) else 'non_dict'}")
    def_ids = [x.get("definition_id") for x in definitions]
    edge_ids = [x.get("edge_id") for x in edges]
    check(len(definitions) == len(set(def_ids)) == 57, "ast.definition_count")
    check(len(edges) == len(set(edge_ids)) == 882, "ast.call_count")
    check(any(x.get("qualified_name") == "_ok" and x.get("start_line") == 983 for x in definitions), "ast.main_ok_present")
    check(any(x.get("caller") == "<module>" for x in edges), "ast.module_calls_present")
    rebuilt_definitions, rebuilt_edges = independently_rebuild_ast()
    check(definitions == rebuilt_definitions, "ast.independent_definition_rebuild")
    check(edges == rebuilt_edges, "ast.independent_edge_rebuild")
    check(independent_class_bases(MAIN_CODE, "LCOCathodeDQDV") == ["GraphiteAnodeDischargeDQDV"], "ast.lco_inheritance")
    chi_default, chi_assignment = independent_method_contract(
        MAIN_CODE, "GraphiteAnodeDischargeDQDV", "__init__", "chi_split", "self.chi_split"
    )
    check(chi_default == "func_chi_d", "ast.chi_split_default")
    check(chi_assignment, "ast.chi_split_assignment")
    for item in definitions:
        raw = raw_blob(item.get("path", "")); lines = raw.decode("utf-8-sig").splitlines()
        start, end = item.get("start_line"), item.get("end_line")
        check(1 <= start <= end <= len(lines), f"definition.bounds:{item.get('definition_id')}")
        check(item.get("slice_sha256") == sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")), f"definition.slice:{item.get('definition_id')}")
        check(item.get("git_blob_sha1") == git_blob_sha1(raw), f"definition.blob:{item.get('definition_id')}")
        check(item.get("authority_boundary") == AUTH_CODE, f"definition.authority:{item.get('definition_id')}")
    for item in edges:
        raw = raw_blob(item.get("path", "")); lines = raw.decode("utf-8-sig").splitlines()
        check(1 <= item.get("line", 0) <= len(lines), f"edge.bounds:{item.get('edge_id')}")
        check(item.get("git_blob_sha1") == git_blob_sha1(raw), f"edge.blob:{item.get('edge_id')}")
        check(item.get("authority_boundary") == AUTH_CODE, f"edge.authority:{item.get('edge_id')}")

    public = matrix.get("public_entry_obligations", [])
    for item in public:
        check_keys(item, PUBLIC_KEYS, f"schema.public:{item.get('qualified_name') if isinstance(item, dict) else 'non_dict'}")
    prod = [x for x in public if x.get("entry_scope") == "PRODUCTION"]
    support = [x for x in public if x.get("entry_scope") == "SUPPORT_SCRIPT"]
    check([(x.get("qualified_name"), *x.get("lines", [None, None])) for x in prod] == PRODUCTION, "public.production_manifest")
    check(len(support) == 14 and len(public) == 34, "public.denominators")
    trace_by_id = {row.get("trace_id"): row for row in traces}
    for item in prod:
        check(bool(item.get("trace_ids")), f"public.orphan:{item.get('qualified_name')}")
        check(set(item.get("trace_ids", [])) <= set(trace_by_id), f"public.trace_exists:{item.get('qualified_name')}")
        for trace_id in item.get("trace_ids", []):
            check(item.get("definition_id") in trace_by_id.get(trace_id, {}).get("implementation_definition_ids", []), f"public.trace_join:{item.get('qualified_name')}:{trace_id}")
        check(item.get("exclusion_reason") is None, f"public.production_exclusion:{item.get('qualified_name')}")
        check(item.get("authority_boundary") == AUTH_CODE, f"public.authority:{item.get('qualified_name')}")
    for item in support:
        check(item.get("trace_ids") == [], f"support.no_production_trace:{item.get('qualified_name')}")
        check(bool(item.get("exclusion_reason")), f"support.exclusion:{item.get('qualified_name')}")
        check(item.get("authority_boundary") == AUTH_TEST, f"support.authority:{item.get('qualified_name')}")

    gate_index = matrix.get("test_gate_index", [])
    for item in gate_index:
        check_keys(item, GATE_KEYS, f"schema.gate:{item.get('gate_id') if isinstance(item, dict) else 'non_dict'}")
    gate_ids = {x.get("gate_id") for x in gate_index}
    check(len(gate_index) == len(gate_ids) == 46, "gates.denominator")
    check({x for x in gate_ids if isinstance(x, str) and x.startswith("MAIN-")} == {f"MAIN-{i:02d}" for i in range(1, 16)}, "gates.main_set")
    for gate in gate_index:
        raw = raw_blob(gate.get("path", "")); lines = raw.decode("utf-8-sig").splitlines()
        start, end = gate.get("start_line"), gate.get("end_line")
        check(1 <= start <= end <= len(lines), f"gate.bounds:{gate.get('gate_id')}")
        check(gate.get("slice_sha256") == sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")), f"gate.slice:{gate.get('gate_id')}")
        check(gate.get("authority_boundary") == AUTH_TEST, f"gate.authority:{gate.get('gate_id')}")

    consumers = matrix.get("artifact_consumer_index", [])
    for item in consumers:
        check_keys(item, CONSUMER_KEYS, f"schema.consumer:{item.get('consumer_id') if isinstance(item, dict) else 'non_dict'}")
    consumer_ids = {x.get("consumer_id") for x in consumers}
    check(len(consumers) == len(consumer_ids) == 17, "artifacts.denominator")
    check({"ART-PDF-CH1", "ART-PDF-CH2", "ART-GOLDEN", "ART-GRAPH", "ART-FIT", "ART-LCO-HEAT", "ART-VIB"} <= consumer_ids, "artifacts.required")
    for item in consumers:
        check(item.get("authority_boundary") == AUTH_ARTIFACT, f"artifact.authority:{item.get('consumer_id')}")
        check(bool(item.get("sha256")) and bool(item.get("git_blob_sha1")), f"artifact.hashes:{item.get('consumer_id')}")
        anchors = item.get("consumer_source_anchors", [])
        disposition = item.get("consumer_anchor_disposition")
        check(disposition in {"EXACT_FROZEN_TEX_SOURCE_ANCHOR", "EXACT_FROZEN_GENERATOR_ANCHOR", "EXACT_FROZEN_CONSUMER_AND_CAPTURE_ANCHOR", "NO_FROZEN_GENERATOR_GROUND"}, f"artifact.anchor_disposition:{item.get('consumer_id')}")
        check(bool(anchors) == (disposition != "NO_FROZEN_GENERATOR_GROUND"), f"artifact.anchor_presence:{item.get('consumer_id')}")
        for anchor in anchors:
            check_keys(anchor, SOURCE_ANCHOR_KEYS, f"schema.consumer_anchor:{item.get('consumer_id')}")
            raw = raw_blob(anchor.get("path", "")); lines = raw.decode("utf-8-sig").splitlines()
            start, end = anchor.get("start_line"), anchor.get("end_line")
            check(isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= len(lines), f"artifact.anchor_bounds:{item.get('consumer_id')}")
            check(anchor.get("git_blob_sha1") == git_blob_sha1(raw), f"artifact.anchor_blob:{item.get('consumer_id')}")
            check(anchor.get("slice_sha256") == sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")), f"artifact.anchor_slice:{item.get('consumer_id')}")
            expected_authority = AUTH_LEXICAL if str(anchor.get("path", "")).endswith(".tex") else AUTH_CODE
            check(anchor.get("authority_boundary") == expected_authority, f"artifact.anchor_authority:{item.get('consumer_id')}")
    consumer_by_id = {item.get("consumer_id"): item for item in consumers}
    for consumer_id in ("ART-PDF-CH1", "ART-PDF-CH2", "ART-PDF-APPENDIX"):
        item = consumer_by_id.get(consumer_id, {})
        check(item.get("ground_status") == "DIRECT_TEX_SOURCE" and item.get("consumer_anchor_disposition") == "EXACT_FROZEN_TEX_SOURCE_ANCHOR", f"artifact.pdf_tex_source:{consumer_id}")
        check(len(item.get("consumer_source_anchors", [])) == 1 and item.get("consumer_source_anchors", [{}])[0].get("path", "").endswith(".tex"), f"artifact.pdf_tex_anchor:{consumer_id}")

    def_set, edge_set = set(def_ids), set(edge_ids)
    def_by_id = {item["definition_id"]: item for item in definitions}
    edge_by_id = {item["edge_id"]: item for item in edges}
    gate_by_id = {item["gate_id"]: item for item in gate_index}
    for row in traces:
        tid = row.get("trace_id")
        check(row.get("relation") in {"DIRECT", "RELATED_NOT_DIRECT", "NOT_APPLICABLE"}, f"trace.relation:{tid}")
        check(row.get("status") in {"ALIGNED", "PARTIAL", "MISALIGNED", "ABSENT", "UNVERIFIED"}, f"trace.status:{tid}")
        check(row.get("implementation_disposition") in {"IMPLEMENTED", "PARTIAL", "MISSING", "NOT_REQUIRED", "UNVERIFIED"}, f"trace.disposition:{tid}")
        check(row.get("execution_state") in {"ACTIVE", "DORMANT_BY_DEFAULT"}, f"trace.execution_state:{tid}")
        check(row.get("reachability") in {"ACTIVE", "CONDITIONALLY_REACHABLE_DEFAULT_DORMANT", "NOT_REQUIRED_RELATED", "NO_CHAIN_IMPLEMENTATION_ABSENT"}, f"trace.reachability:{tid}")
        check(row.get("authority_boundary") == AUTH_TRACE, f"trace.authority:{tid}")
        check(row.get("scientific_truth") == "DEFERRED_TO_STEP44_AND_PHASE071", f"trace.science_boundary:{tid}")
        check(set(row.get("theory_anchor_ids", [])) <= doc_anchor_ids, f"trace.doc_anchors:{tid}")
        check(set(row.get("implementation_definition_ids", [])) <= def_set, f"trace.impl_anchors:{tid}")
        check(set(row.get("test_gate_ids", [])) <= gate_ids, f"trace.gate_missing:{tid}")
        check(set(row.get("assertion_gate_ids", [])) <= set(row.get("test_gate_ids", [])), f"trace.assertion_subset:{tid}")
        for gate_id in row.get("assertion_gate_ids", []):
            check(gate_by_id.get(gate_id, {}).get("enforcement") == "SOURCE_ENFORCED_OR_BOUNDED_RUNTIME_GATE", f"trace.assertion_strength:{tid}:{gate_id}")
        check(set(row.get("artifact_consumer_ids", [])) <= consumer_ids, f"trace.artifact_missing:{tid}")
        check(bool(row.get("test_gate_ids")) or row.get("status") == "ABSENT", f"trace.assertion_disposition:{tid}")
        paths = row.get("call_paths", [])
        path_ids: list[str] = []
        for path in paths:
            check_keys(path, CALL_PATH_KEYS, f"schema.call_path:{tid}")
            path_ids.append(path.get("path_id"))
            path_edge_ids = path.get("edge_ids", [])
            chain_ids = path.get("definition_chain_ids", [])
            chain_names = path.get("definition_chain_names", [])
            check(bool(path_edge_ids) and len(chain_ids) == len(path_edge_ids) + 1, f"trace.path_cardinality:{tid}:{path.get('path_id')}")
            check(len(chain_names) == len(chain_ids), f"trace.path_name_cardinality:{tid}:{path.get('path_id')}")
            check(set(path_edge_ids) <= edge_set, f"trace.edge_missing:{tid}:{path.get('path_id')}")
            check(set(chain_ids) <= set(row.get("implementation_definition_ids", [])), f"trace.path_endpoint_anchor:{tid}:{path.get('path_id')}")
            resolved_names = [def_by_id.get(definition_id, {}).get("qualified_name") for definition_id in chain_ids]
            check(chain_names == resolved_names, f"trace.path_definition_names:{tid}:{path.get('path_id')}")
            for index, edge_id in enumerate(path_edge_ids):
                edge = edge_by_id.get(edge_id, {})
                caller_name = chain_names[index] if index < len(chain_names) else None
                target_name = chain_names[index + 1] if index + 1 < len(chain_names) else None
                check(edge.get("caller") == caller_name, f"trace.path_caller:{tid}:{path.get('path_id')}:{index}")
                check(isinstance(target_name, str) and edge_targets_definition(edge, target_name, path.get("path_disposition", "")), f"trace.path_callee:{tid}:{path.get('path_id')}:{index}")
            check(path.get("path_disposition") in {"ORDERED_CONTIGUOUS_LOCAL_CALL_PATH", "ORDERED_CONTIGUOUS_DYNAMIC_DISPATCH_PATH"}, f"trace.path_disposition:{tid}:{path.get('path_id')}")
            check(path.get("authority_boundary") == AUTH_CODE, f"trace.path_authority:{tid}:{path.get('path_id')}")
        check(len(path_ids) == len(set(path_ids)), f"trace.path_unique:{tid}")
        if row.get("relation") == "DIRECT" and row.get("implementation_disposition") != "MISSING":
            path_definition_ids = {definition_id for path in paths for definition_id in path.get("definition_chain_ids", [])}
            nonclass_implementation_ids = {
                definition_id for definition_id in row.get("implementation_definition_ids", [])
                if def_by_id.get(definition_id, {}).get("kind") != "class"
            }
            check(nonclass_implementation_ids <= path_definition_ids, f"trace.unused_impl_anchor:{tid}")
        if row.get("relation") == "DIRECT" and row.get("implementation_disposition") != "MISSING":
            check(row.get("reachability") in {"ACTIVE", "CONDITIONALLY_REACHABLE_DEFAULT_DORMANT"} and bool(paths), f"trace.direct_no_active_chain:{tid}")
        if row.get("status") == "ALIGNED":
            check(row.get("relation") == "DIRECT" and row.get("reachability") == "ACTIVE", f"trace.aligned_rule:{tid}")
            check(row.get("unit_check", {}).get("status") == "PASS" and row.get("sign_check", {}).get("status") == "PASS", f"trace.aligned_unit_sign:{tid}")
            check(bool(row.get("assertion_gate_ids")), f"trace.aligned_strong_assertion:{tid}")
        if row.get("status") == "ABSENT":
            check(row.get("implementation_disposition") == "MISSING", f"trace.absent_rule:{tid}")
        for label, evidence, expected_keys in (
            ("unit", row.get("unit_check", {}), UNIT_KEYS),
            ("sign", row.get("sign_check", {}), SIGN_KEYS),
        ):
            check_keys(evidence, expected_keys, f"schema.trace_{label}:{tid}")
            check(evidence.get("status") in {"PASS", "PARTIAL", "NOT_APPLICABLE"}, f"trace.{label}_status:{tid}")
            check(isinstance(evidence.get("statement"), str) and len(evidence.get("statement")) >= 40 and "within Step 43 scope" not in evidence.get("statement"), f"trace.{label}_statement:{tid}")
            check(evidence.get("document_anchor_ids") == row.get("theory_anchor_ids"), f"trace.{label}_doc_anchor:{tid}")
            check(evidence.get("implementation_definition_ids") == row.get("implementation_definition_ids"), f"trace.{label}_impl_anchor:{tid}")
            check(evidence.get("assertion_gate_ids") == row.get("assertion_gate_ids"), f"trace.{label}_assertion_anchor:{tid}")

    by_trace = {x.get("trace_id"): x for x in traces}
    check(by_trace.get("TRC-CH1-LCO-HYSTERESIS", {}).get("execution_state") == "DORMANT_BY_DEFAULT", "trace.dormant_lco_hys")
    check(by_trace.get("TRC-CH1-LCO-HYSTERESIS", {}).get("reachability") == "CONDITIONALLY_REACHABLE_DEFAULT_DORMANT", "trace.dormant_lco_hys_reachability")
    check(by_trace.get("TRC-CH2-REVERSIBLE-HEAT", {}).get("sign_check", {}).get("polarity") == "QREV_EQUALS_NEGATIVE_I_T_DUDT", "trace.qrev_sign")
    check(by_trace.get("TRC-CH1-MSMR-MAP", {}).get("relation") == "RELATED_NOT_DIRECT", "trace.msmr_not_direct")
    check(by_trace.get("TRC-CH2-WIDTH-T-DEPENDENCE", {}).get("status") == "MISALIGNED", "trace.default_width_misalignment")
    lco_electronic_paths = by_trace.get("TRC-CH1-LCO-ENTROPY-ELECTRONIC", {}).get("call_paths", [])
    check({path.get("definition_chain_names", [None])[0] for path in lco_electronic_paths} == {
        "GraphiteAnodeDischargeDQDV.equilibrium",
        "GraphiteAnodeDischargeDQDV.dqdv",
        "GraphiteAnodeDischargeDQDV.entropy_coefficient",
    }, "trace.lco_electronic_public_starts")
    check(all(path.get("path_disposition") == "ORDERED_CONTIGUOUS_DYNAMIC_DISPATCH_PATH" for path in lco_electronic_paths), "trace.lco_electronic_dynamic_dispatch")

    optional = matrix.get("optional_input_disposition_groups", [])
    check(len(optional) == 29 == len({x.get("group_id") for x in optional}), "optional.denominator")
    for item in optional:
        check_keys(item, OPTIONAL_GROUP_KEYS, f"schema.optional:{item.get('group_id') if isinstance(item, dict) else 'non_dict'}")
        check(bool(item.get("label")) and bool(item.get("member_names")) and len(item.get("member_names", [])) == len(set(item.get("member_names", []))), f"optional.members:{item.get('group_id')}")
        check(bool(item.get("acceptance")) and bool(item.get("runtime_disposition")) and bool(item.get("evidence")), f"optional.complete:{item.get('group_id')}")
        check(item.get("authority_boundary") == AUTH_CODE, f"optional.authority:{item.get('group_id')}")

    contradictions = matrix.get("contradiction_routes", [])
    check([x.get("contradiction_id") for x in contradictions] == [f"CTR-43-{i:03d}" for i in range(1, 7)], "contradictions.manifest")
    for item in contradictions:
        check_keys(item, CONTRADICTION_KEYS, f"schema.contradiction:{item.get('contradiction_id') if isinstance(item, dict) else 'non_dict'}")
        check(bool(item.get("disposition")) and bool(item.get("gate")), f"contradiction.complete:{item.get('contradiction_id')}")
        check(item.get("authority_boundary") == AUTH_TRACE, f"contradiction.authority:{item.get('contradiction_id')}")

    findings = matrix.get("findings", {})
    check(set(findings) == {"P0", "P1", "P2"}, "schema.findings_keys")
    for item in findings.get("P1", []):
        check(isinstance(item, dict) and set(item) == {"id", "summary", "route"}, f"schema.finding_p1:{item.get('id') if isinstance(item, dict) else 'non_dict'}")
    for item in findings.get("P2", []):
        check(isinstance(item, dict) and set(item) == {"id", "summary"}, f"schema.finding_p2:{item.get('id') if isinstance(item, dict) else 'non_dict'}")
    check(len(findings.get("P0", [])) == 0, "findings.P0")
    check(len(findings.get("P1", [])) == 12, "findings.P1")
    check(len(findings.get("P2", [])) == 13, "findings.P2")
    fingerprints = matrix.get("fingerprints", {})
    check(set(fingerprints) == set(EXPECTED_FINGERPRINTS), "schema.fingerprint_keys")
    for key, expected in EXPECTED_FINGERPRINTS.items():
        check(fingerprints.get(key) == expected, f"fingerprint.recorded:{key}")
        check(canonical_fingerprint(matrix.get(key)) == expected, f"fingerprint.payload:{key}")

    summary = matrix.get("gate_summary", {})
    check_keys(summary, GATE_SUMMARY_KEYS, "schema.gate_summary_keys")
    expected_summary = {
        "candidate_records": 914, "candidate_disposition_orphan_count": 0,
        "curated_document_obligations": 28, "curated_doc_row_orphan_count": 0,
        "focus_families_required": 14, "focus_family_missing_count": 0,
        "definitions_full_ast": 57, "call_nodes_full_ast": 882,
        "step42_definition_records": 56, "step42_definition_body_call_edges": 444,
        "public_entries_all": 34, "production_public_entries": 20,
        "support_public_entries": 14, "public_call_orphan_count": 0,
        "source_gates": 46, "python_assert_nodes": 0,
        "artifact_consumers": 17, "optional_disposition_groups": 29,
        "invalid_anchor_count": 0, "missing_authority_boundary_count": 0,
        "P0": 0, "P1": 12, "P2": 13, "gate_result": "PASS_WITH_CONCERNS",
    }
    for key, value in expected_summary.items():
        check(summary.get(key) == value, f"summary.{key}")
    check(isinstance(summary.get("curated_overlap_anchor_records"), int) and summary.get("curated_overlap_anchor_records") > 0, "summary.curated_overlap")
    member_names = {member for group in optional for member in group.get("member_names", [])}
    check(summary.get("optional_member_names") == len(member_names), "summary.optional_members")
    return errors, checks


def run_determinism() -> tuple[list[str], int]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="p060_step43_") as tmp:
        a, b = Path(tmp) / "a.json", Path(tmp) / "b.json"
        for path in (a, b):
            proc = subprocess.run([sys.executable, str(BUILDER), "--output", str(path)], cwd=ROOT,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                errors.append("determinism.builder_exit")
        if not errors:
            if a.read_bytes() != b.read_bytes():
                errors.append("determinism.two_rebuilds")
            if a.read_bytes() != TRACE_MATRIX.read_bytes():
                errors.append("determinism.committed_artifact")
    return errors, 4


def run_negative_controls(matrix: dict[str, Any]) -> tuple[list[str], int]:
    failures: list[str] = []

    def expect(label: str, mutated: dict[str, Any], needle: str) -> None:
        errors, _ = validate_matrix(mutated)
        if not any(needle in item for item in errors):
            failures.append(f"negative.{label}")

    removed = copy.deepcopy(matrix)
    edge_id = removed["trace_rows"][0]["call_paths"][0]["edge_ids"][0]
    removed["call_edge_index"] = [x for x in removed["call_edge_index"] if x["edge_id"] != edge_id]
    expect("removed_call_edge", removed, "trace.edge_missing")

    swapped = copy.deepcopy(matrix)
    next(x for x in swapped["trace_rows"] if x["trace_id"] == "TRC-CH2-REVERSIBLE-HEAT")["sign_check"]["polarity"] = "QREV_EQUALS_POSITIVE_I_T_DUDT"
    expect("swapped_sign", swapped, "trace.qrev_sign")

    false_direct = copy.deepcopy(matrix)
    next(x for x in false_direct["trace_rows"] if x["trace_id"] == "TRC-CH1-MSMR-MAP")["relation"] = "DIRECT"
    expect("false_direct", false_direct, "trace.direct_no_active_chain")

    dormant = copy.deepcopy(matrix)
    next(x for x in dormant["trace_rows"] if x["trace_id"] == "TRC-CH1-LCO-HYSTERESIS")["execution_state"] = "ACTIVE"
    expect("dormant_as_active", dormant, "trace.dormant_lco_hys")

    missing_gate = copy.deepcopy(matrix)
    missing_gate["test_gate_index"] = [x for x in missing_gate["test_gate_index"] if x["gate_id"] != "MAIN-12"]
    expect("missing_assertion", missing_gate, "trace.gate_missing")

    duplicate = copy.deepcopy(matrix)
    duplicate["trace_rows"].append(copy.deepcopy(duplicate["trace_rows"][0]))
    expect("duplicate_trace", duplicate, "trace.id_order")

    unknown = copy.deepcopy(matrix)
    unknown["trace_rows"][0]["status"] = "CONFORMING"
    expect("unknown_enum", unknown, "trace.status")

    broken_order = copy.deepcopy(matrix)
    path = broken_order["trace_rows"][0]["call_paths"][0]
    path["edge_ids"][0], path["edge_ids"][1] = path["edge_ids"][1], path["edge_ids"][0]
    expect("broken_path_order", broken_order, "trace.path_caller")

    missing_endpoint = copy.deepcopy(matrix)
    row = missing_endpoint["trace_rows"][0]
    endpoint = row["call_paths"][0]["definition_chain_ids"][-1]
    row["implementation_definition_ids"].remove(endpoint)
    row["unit_check"]["implementation_definition_ids"].remove(endpoint)
    row["sign_check"]["implementation_definition_ids"].remove(endpoint)
    expect("missing_path_endpoint", missing_endpoint, "trace.path_endpoint_anchor")

    weak_aligned = copy.deepcopy(matrix)
    next(x for x in weak_aligned["trace_rows"] if x["trace_id"] == "TRC-CH1-LOW-CURRENT-HYS-LIMIT")["status"] = "ALIGNED"
    expect("weak_gate_as_aligned", weak_aligned, "trace.aligned_strong_assertion")

    extra_generation = copy.deepcopy(matrix)
    extra_generation["generation"]["unexpected"] = True
    expect("extra_generation_key", extra_generation, "schema.generation_keys")

    empty_enums = copy.deepcopy(matrix)
    empty_enums["enumerations"] = {}
    expect("empty_enumerations", empty_enums, "schema.enumeration_keys")

    duplicate_input = copy.deepcopy(matrix)
    duplicate_input["input_evidence"].append(copy.deepcopy(duplicate_input["input_evidence"][0]))
    expect("duplicate_input", duplicate_input, "inputs.paths")

    extra_summary = copy.deepcopy(matrix)
    extra_summary["gate_summary"]["unexpected"] = 1
    expect("extra_summary_key", extra_summary, "schema.gate_summary_keys")

    missing_consumer_anchor = copy.deepcopy(matrix)
    consumer = next(x for x in missing_consumer_anchor["artifact_consumer_index"] if x["consumer_anchor_disposition"] != "NO_FROZEN_GENERATOR_GROUND")
    consumer["consumer_source_anchors"] = []
    expect("missing_consumer_anchor", missing_consumer_anchor, "artifact.anchor_presence")

    private_lco_start = copy.deepcopy(matrix)
    lco_row = next(x for x in private_lco_start["trace_rows"] if x["trace_id"] == "TRC-CH1-LCO-ENTROPY-ELECTRONIC")
    lco_path = lco_row["call_paths"][0]
    lco_path["edge_ids"] = lco_path["edge_ids"][1:]
    lco_path["definition_chain_ids"] = lco_path["definition_chain_ids"][1:]
    lco_path["definition_chain_names"] = lco_path["definition_chain_names"][1:]
    expect("private_lco_start", private_lco_start, "trace.lco_electronic_public_starts")

    missing_pdf_tex = copy.deepcopy(matrix)
    pdf = next(x for x in missing_pdf_tex["artifact_consumer_index"] if x["consumer_id"] == "ART-PDF-CH1")
    pdf["consumer_source_anchors"] = []
    pdf["consumer_anchor_disposition"] = "NO_FROZEN_GENERATOR_GROUND"
    pdf["ground_status"] = "STORED_WITNESS"
    expect("missing_pdf_tex_source", missing_pdf_tex, "artifact.pdf_tex_source")

    unused_impl = copy.deepcopy(matrix)
    row = unused_impl["trace_rows"][0]
    extra_definition = next(x["definition_id"] for x in unused_impl["implementation_definitions"] if x["qualified_name"] == "GraphiteAnodeDischargeDQDV.irreversible_heat")
    row["implementation_definition_ids"].append(extra_definition)
    row["unit_check"]["implementation_definition_ids"].append(extra_definition)
    row["sign_check"]["implementation_definition_ids"].append(extra_definition)
    expect("unused_impl_anchor", unused_impl, "trace.unused_impl_anchor")

    false_static_dispatch = copy.deepcopy(matrix)
    lco_path = next(x for x in false_static_dispatch["trace_rows"] if x["trace_id"] == "TRC-CH1-LCO-ENTROPY-ELECTRONIC")["call_paths"][0]
    lco_path["path_disposition"] = "ORDERED_CONTIGUOUS_LOCAL_CALL_PATH"
    expect("false_static_dispatch", false_static_dispatch, "trace.path_callee")

    unrelated_public_trace = copy.deepcopy(matrix)
    public_item = next(x for x in unrelated_public_trace["public_entry_obligations"] if x["qualified_name"] == "GraphiteAnodeDischargeDQDV.irreversible_heat")
    public_item["trace_ids"] = ["TRC-CH1-CENTER-THERMO"]
    expect("unrelated_public_trace", unrelated_public_trace, "public.trace_join")

    return failures, 20


def main() -> int:
    if not TRACE_MATRIX.is_file():
        print("FAIL missing_artifact: Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json")
        print("FAIL_P060_STEP43_DOC_CODE_CONFORMANCE 0/1")
        return 2
    trace = strict_json_load(TRACE_MATRIX)
    if not isinstance(trace, dict):
        print("FAIL trace.root_type")
        print("FAIL_P060_STEP43_DOC_CODE_CONFORMANCE 0/1")
        return 1
    errors, checks = validate_matrix(trace)
    det_errors, det_checks = run_determinism()
    neg_errors, neg_checks = run_negative_controls(trace)
    errors.extend(det_errors); errors.extend(neg_errors)
    total = checks + det_checks + neg_checks
    passed = total - len(errors)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"FAIL_P060_STEP43_DOC_CODE_CONFORMANCE {passed}/{total}")
        return 1
    summary = trace["gate_summary"]
    print(f"PASS candidates={summary['candidate_records']} curated_claims={summary['curated_document_obligations']} production={summary['production_public_entries']} support={summary['support_public_entries']}")
    print(f"PASS definitions={summary['definitions_full_ast']} calls={summary['call_nodes_full_ast']} source_gates={summary['source_gates']} ast_asserts={summary['python_assert_nodes']}")
    print(f"PASS orphans candidate={summary['candidate_disposition_orphan_count']} curated_doc={summary['curated_doc_row_orphan_count']} public={summary['public_call_orphan_count']} focus_missing={summary['focus_family_missing_count']}")
    print(f"PASS findings P0={summary['P0']} P1={summary['P1']} P2={summary['P2']} result={summary['gate_result']}")
    print(f"PASS determinism=4/4 negative_controls={neg_checks}/{neg_checks}")
    print(f"PASS_P060_STEP43_DOC_CODE_CONFORMANCE {passed}/{total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
