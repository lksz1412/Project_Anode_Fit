#!/usr/bin/env python3
"""Build Phase 067 Step 90.1 lossless disposition and carry-forward records."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "38f93bd1638c674ff7fd7fb40ed57036a07fd8fd"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
DATE = "2026-09-06"
SUBJECT = "audit(phase067): disposition code test fitting evidence"
GATE = "PASS_P067_STEP90_1_DISPOSITION"
PERSISTENCE = "PASS_P067_STEP90_1_PERSISTENCE"
SOURCE_PATH = "Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json"
CARRY_PATH = "Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_090_1_DISPOSITION_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
HUMAN_PREREQUISITES = (RESULT_PATH, PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)

INVENTORY = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
FULL_READ = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STATE_FLOW = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
CALL_GRAPH = "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json"
STATE_DEFAULT = "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json"
SAVED_RUNTIME = "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json"
TEST_MATRIX = "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json"
GUIDE_MATRIX = "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json"
UNIT_MATRIX = "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json"
GUARD_MATRIX = "Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json"
FITTING_MATRIX = "Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json"
FITTING_RUNTIME = "Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json"
PRIOR_CARRY = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"

INPUT_PATHS = (
    INVENTORY, FULL_READ, STATE_FLOW, CALL_GRAPH, STATE_DEFAULT, SAVED_RUNTIME,
    TEST_MATRIX, GUIDE_MATRIX, UNIT_MATRIX, GUARD_MATRIX, FITTING_MATRIX,
    FITTING_RUNTIME, PRIOR_CARRY,
)
INPUT_EXPECTED = {
    INVENTORY: ("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63",
                "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"),
    FULL_READ: ("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174",
                "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"),
    STATE_FLOW: ("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8",
                 "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44"),
    CALL_GRAPH: ("54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f",
                 "63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc"),
    STATE_DEFAULT: ("b8ac7affbb31195ec8dde6015890cbb50b1f2b9cc5815fc33c325efc95286f23",
                    "845b676aea321134b648de41320e7baf4f39f925ad2a1abe96f36f713bc95542"),
    SAVED_RUNTIME: ("9bf610d2d09be7d95fd2493541d6c4336de330c37fb56d1f12c411b228dfbf82",
                    "0e2b0bd3f6120c9c8feaa879b5fe62a49934de5ea8dbddff14c700ddef32f196"),
    TEST_MATRIX: ("13a281c76282f5fae370d1c2b10f183937c685bceba466489a62b9e850049d4a",
                  "eadde68e51257e0daae9f9455be3a7331c77a56d1490b2291934ef75f45fa154"),
    GUIDE_MATRIX: ("474f09ebb1605d3190867cee9746079b10c04f6bfbdfbab028e9d6c1be70ec08",
                   "c556671b6fd4284d740fdb0cc3777087442d4abd2160ace42d4ff70749d4144c"),
    UNIT_MATRIX: ("62f5eb265121987b83398266895a11e8a84d7f1ffa90c59fe929efb6f00614be",
                  "099899de75edfde55a92ff31f577e178967212226cf4a13cdb951643b15e535c"),
    GUARD_MATRIX: ("525b33403667413446e374a2b931c90ec45c7eb24871205527dd9c6ddef2591d",
                   "201b2e65756ab8876c861216742f67b0305ef351cc84e8f4ebf434d49dfabb2b"),
    FITTING_MATRIX: ("dc76eeef9b0bb2f93a376fbe491f12b2c73b47d59b097e671e9745b28a6869f4",
                     "cf1b136028f126670a80ec60ce26db9edc110e0bff7c41cf7986f73c14f9ae3a"),
    FITTING_RUNTIME: ("c0859de686ea207be758fc6d32faaa88d2e95151e3c3bdb56615ff366f250486",
                      "b78cfa4ec96e3aeb42979e6aaf93407fed9267fd7abeeb8458064d78b3567846"),
    PRIOR_CARRY: ("847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003",
                  "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6"),
}

DISPOSITIONS = ("PRESERVE", "CORRECT", "WITHHOLD", "DISCARD", "GROUND_NOT_FOUND")
AUTHORITY_FALSE = {
    "canonical_model": False,
    "external_scientific": False,
    "held_out_validation": False,
    "identifiability": False,
    "material_mechanism": False,
    "primary_proposition": False,
    "publication": False,
    "specimen_protocol": False,
}


class BuildError(RuntimeError):
    pass


def require(ok: bool, code: str) -> None:
    if not ok:
        raise BuildError(code)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    copy_value = dict(value)
    copy_value.pop("semantic_sha256", None)
    return sha(canonical(copy_value))


def input_semantic(path: str, value: dict[str, Any]) -> str:
    copy_value = dict(value)
    if path in {INVENTORY, FULL_READ}:
        copy_value["semantic_sha256"] = ""
        raw = (json.dumps(copy_value, ensure_ascii=False, indent=2, sort_keys=True,
                          allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")
        return sha(raw)
    copy_value.pop("semantic_sha256", None)
    raw = json.dumps(copy_value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    if path != PRIOR_CARRY:
        raw += b"\n"
    return sha(raw)


def finish(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic(value)
    return value


def strict_json(raw: bytes, code: str) -> dict[str, Any]:
    require(len(raw) <= 8_000_000, code + "_BYTES")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, code + "_DUPLICATE")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise BuildError(code + "_PARSE") from exc
    require(isinstance(value, dict), code + "_ROOT")
    stack = [value]
    nodes = 0
    while stack:
        item = stack.pop()
        nodes += 1
        require(nodes <= 700_000, code + "_NODES")
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, float):
            require(math.isfinite(item), code + "_NONFINITE")
    return value


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    if not args or any(not isinstance(item, str) or any(c in item for c in "\0\n\r")
                       for item in args):
        return False
    if len(args) == 2 and args[0] == "show" and ":" in args[1]:
        ref, path = args[1].split(":", 1)
        return ref == EXPECTED_PARENT and path in INPUT_PATHS
    if args[:3] == ("ls-tree", EXPECTED_PARENT, "--"):
        return args[3:] == INPUT_PATHS
    return False


def git_bytes(args: list[str]) -> bytes:
    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV")
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(completed.returncode == 0, "E_GIT_READ")
    return completed.stdout


def read_inputs() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    tree_raw = git_bytes(["ls-tree", EXPECTED_PARENT, "--", *INPUT_PATHS])
    tree: dict[str, tuple[str, str]] = {}
    for line in tree_raw.decode("utf-8").splitlines():
        metadata, path = line.split("\t", 1)
        mode, kind, oid = metadata.split()
        require(kind == "blob" and mode == "100644" and len(oid) == 40, "E_TREE_ROW")
        tree[path] = (mode, oid)
    require(set(tree) == set(INPUT_PATHS), "E_TREE_COVERAGE")

    values: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []
    for path in INPUT_PATHS:
        raw = git_bytes(["show", f"{EXPECTED_PARENT}:{path}"])
        value = strict_json(raw, "E_INPUT_JSON")
        expected_raw, expected_semantic = INPUT_EXPECTED[path]
        require(sha(raw) == expected_raw, "E_INPUT_RAW")
        require(value.get("semantic_sha256") == expected_semantic, "E_INPUT_DECLARED")
        require(input_semantic(path, value) == expected_semantic, "E_INPUT_SEMANTIC")
        mode, oid = tree[path]
        values[path] = value
        manifest.append({
            "bytes": len(raw),
            "declared_semantic_sha256": expected_semantic,
            "git_blob_oid": oid,
            "mode": mode,
            "path": path,
            "raw_sha256": expected_raw,
            "recomputed_semantic_sha256": expected_semantic,
            "semantic_seal_status": "VERIFIED",
            "source_commit": EXPECTED_PARENT,
        })
    return values, manifest


def record_hash(value: Any) -> str:
    return sha(canonical(value))


def source_row(*, disposition_id: str, surface_kind: str, row: dict[str, Any],
               origin_path: str, origin_pointer: str, disposition: str, state: str,
               owner: str, criterion: str, ceiling: str,
               role_override: str | None = None) -> dict[str, Any]:
    require(disposition in DISPOSITIONS, "E_SOURCE_DISPOSITION")
    role = role_override or str(row.get("role", surface_kind.lower()))
    return {
        "acceptance_criterion": criterion,
        "authority_ceiling": ceiling,
        "blob_oid": row["blob_oid"],
        "canonical_owner": owner,
        "dedup_group": f"{surface_kind.lower()}:{row['blob_oid']}",
        "disposition": disposition,
        "disposition_id": disposition_id,
        "external_authority_promoted": False,
        "manifest_entry_index": row.get("manifest_entry_index"),
        "mode": row["git_mode"],
        "occurrence_ordinal": row.get("ordinal"),
        "origin_path": origin_path,
        "origin_pointer": origin_pointer,
        "origin_record_sha256": record_hash(row),
        "release": row["release"],
        "role": role,
        "source_path": row["path"],
        "state": state,
        "surface_kind": surface_kind,
    }


def build_source(values: dict[str, dict[str, Any]],
                 manifest: list[dict[str, Any]]) -> dict[str, Any]:
    inventory = values[INVENTORY]
    test_matrix = values[TEST_MATRIX]
    guide_matrix = values[GUIDE_MATRIX]
    guard_matrix = values[GUARD_MATRIX]

    occurrences = inventory["occurrence_records"]
    blobs = inventory["blob_records"]
    require(len(occurrences) == 129 and len(blobs) == 84, "E_PYTHON_DENOMINATOR")
    role_counts = {role: sum(row["role"] == role for row in occurrences)
                   for role in ("code", "test", "demo", "result")}
    require(role_counts == {"code": 20, "test": 44, "demo": 30, "result": 35},
            "E_ROLE_PARTITION")
    role_blob_counts = {
        role: len({row["blob_oid"] for row in occurrences if row["role"] == role})
        for role in ("code", "test", "demo", "result")
    }
    require(role_blob_counts == {"code": 15, "test": 29, "demo": 26, "result": 14},
            "E_ROLE_BLOB_PARTITION")
    require(sum(row["physical_lines"] for row in blobs) == 29_952, "E_LINE_DENOMINATOR")
    require(len({row["release"] for row in occurrences}) == 20, "E_RELEASE_DENOMINATOR")

    projection = test_matrix["occurrence_projection"]
    require(projection["result_tool"] == guide_matrix["tool_occurrence_projection"],
            "E_RESULT_TOOL_CROSS_BINDING")
    require(len(projection["golden"]) == 8, "E_GOLDEN_OCCURRENCES")
    require(len(test_matrix["golden_blob_records"]) == 2, "E_GOLDEN_BLOBS")
    require(len(guide_matrix["guide_occurrence_projection"]) == 20, "E_GUIDE_OCCURRENCES")
    require(len(guide_matrix["guide_blob_records"]) == 8, "E_GUIDE_BLOBS")
    require(sum(row["physical_lines"] for row in guide_matrix["guide_blob_records"]) == 854,
            "E_GUIDE_LINES")

    rows: list[dict[str, Any]] = []
    candidate_map = {row["blob_oid"]: row for row in guard_matrix["candidate_disposition_records"]}
    require(len(candidate_map) == 84, "E_CANDIDATE_BLOB_MAP")
    policies = {
        "code": ("PRESERVED_INTERNAL_PRODUCTION_SOURCE",
                 "PHASE-083-IMPLEMENTATION-CONTRACT",
                 "Reconcile the exact source occurrence with the frozen implementation contract.",
                 "INTERNAL_STATIC_SOURCE_ONLY"),
        "test": ("WITHHELD_FROM_CANONICAL_PRODUCTION_SOURCE_RETAINED_AS_TEST_EVIDENCE",
                 "PHASE-088-SCIENTIFIC-REDTEAM",
                 "Re-run the exact test under the final implementation and retain failures as evidence.",
                 "INTERNAL_TEST_EVIDENCE_ONLY"),
        "demo": ("WITHHELD_FROM_CANONICAL_AUTHORITY",
                 "PHASE-083-IMPLEMENTATION-CONTRACT",
                 "Use only as a demonstrator after its inputs, assertions and failure semantics are explicit.",
                 "DEMONSTRATION_ONLY_NOT_VALIDATION"),
        "result": ("WITHHELD_FROM_GATE_AUTHORITY",
                   "PHASE-083-IMPLEMENTATION-CONTRACT",
                   "Convert any retained tool route into an assertion-bearing, non-writing validation contract.",
                   "RESULT_TOOL_SELF_REPORT_ONLY"),
    }
    for index, row in enumerate(occurrences):
        state, owner, criterion, ceiling = policies[row["role"]]
        selected = candidate_map[row["blob_oid"]]["selected_for_step88"]
        disposition = "PRESERVE" if selected else "WITHHOLD"
        if selected:
            state = "PRESERVED_CANONICAL_PRODUCTION_OR_EXACT_OPTIMIZER_SOURCE"
        rows.append(source_row(
            disposition_id=f"P067-SRC-PY-{index + 1:04d}", surface_kind="PYTHON_OCCURRENCE",
            row=row, origin_path=INVENTORY, origin_pointer=f"/occurrence_records/{index}",
            disposition=disposition, state=state, owner=owner, criterion=criterion,
            ceiling=ceiling))

    for index, row in enumerate(projection["golden"]):
        rows.append(source_row(
            disposition_id=f"P067-SRC-GOLDEN-{index + 1:04d}",
            surface_kind="GOLDEN_OCCURRENCE", row=row,
            origin_path=TEST_MATRIX, origin_pointer=f"/occurrence_projection/golden/{index}",
            disposition="PRESERVE", state="PRESERVED_INTERNAL_REGRESSION_EVIDENCE",
            owner="PHASE-088-SCIENTIFIC-REDTEAM",
            criterion="Rebase only after the final equation and implementation contracts pass independent review.",
            ceiling="INTERNAL_REGRESSION_BYTES_ONLY", role_override="golden"))

    for index, row in enumerate(guide_matrix["guide_occurrence_projection"]):
        rows.append(source_row(
            disposition_id=f"P067-SRC-GUIDE-{index + 1:04d}",
            surface_kind="GUIDE_OCCURRENCE", row=row,
            origin_path=GUIDE_MATRIX, origin_pointer=f"/guide_occurrence_projection/{index}",
            disposition="WITHHOLD", state="WITHHELD_SELF_REPORT_OR_STALE_GUIDANCE",
            owner="PHASE-087-MANUSCRIPT-ASSEMBLY",
            criterion="Rewrite only after equation, source and validation states are fixed; keep code discussion outside the scholarly body.",
            ceiling="GUIDE_SELF_REPORT_NOT_SCIENTIFIC_AUTHORITY", role_override="guide"))
    require(len(rows) == 157 and len({row["disposition_id"] for row in rows}) == 157,
            "E_SOURCE_ROWS")

    blob_origins: dict[tuple[str, str], tuple[str, str, str]] = {}
    blob_collections = (
        ("PYTHON_OCCURRENCE", INVENTORY, "blob_records", blobs),
        ("GOLDEN_OCCURRENCE", TEST_MATRIX, "golden_blob_records",
         test_matrix["golden_blob_records"]),
        ("GUIDE_OCCURRENCE", GUIDE_MATRIX, "guide_blob_records",
         guide_matrix["guide_blob_records"]),
    )
    for surface, path, collection, blob_rows in blob_collections:
        for index, blob_row in enumerate(blob_rows):
            key = (surface, blob_row["blob_oid"])
            require(key not in blob_origins, "E_BLOB_ORIGIN_DUPLICATE")
            blob_origins[key] = (
                path, f"/{collection}/{index}", record_hash(blob_row)
            )
    require(len(blob_origins) == 94, "E_BLOB_ORIGIN_COVERAGE")

    groups: list[dict[str, Any]] = []
    for surface in ("PYTHON_OCCURRENCE", "GOLDEN_OCCURRENCE", "GUIDE_OCCURRENCE"):
        surface_rows = [row for row in rows if row["surface_kind"] == surface]
        for group_index, oid in enumerate(sorted({row["blob_oid"] for row in surface_rows})):
            members = [row for row in surface_rows if row["blob_oid"] == oid]
            dispositions = sorted({row["disposition"] for row in members})
            origin_path, origin_pointer, origin_hash = blob_origins[(surface, oid)]
            groups.append({
                "blob_group_id": f"P067-BLOB-{surface.split('_')[0]}-{group_index + 1:04d}",
                "blob_oid": oid,
                "blob_disposition": dispositions[0] if len(dispositions) == 1 else "CONTEXTUAL_MIXED",
                "contextual_mixed_disposition": len(dispositions) > 1,
                "occurrence_count": len(members),
                "occurrence_dispositions": dispositions,
                "origin_path": origin_path,
                "origin_pointer": origin_pointer,
                "origin_record_sha256": origin_hash,
                "row_record_sha256s": [record_hash(row) for row in members],
                "surface_kind": surface,
            })
    require(len(groups) == 94, "E_BLOB_GROUPS")

    for group in groups:
        if group["surface_kind"] != "PYTHON_OCCURRENCE":
            continue
        candidate = candidate_map[group["blob_oid"]]
        expected = "PRESERVE" if candidate["selected_for_step88"] else "WITHHOLD"
        require(group["occurrence_dispositions"] == [expected], "E_BLOB_OCCURRENCE_DISPOSITION")

    counts = {name: sum(row["disposition"] == name for row in rows)
              for name in DISPOSITIONS}
    source_contract = {
        "blob_disposition_groups": 94,
        "code_occurrences": 20,
        "code_unique_blobs": 15,
        "demo_occurrences": 30,
        "demo_unique_blobs": 26,
        "disposition_counts": counts,
        "golden_occurrences": 8,
        "golden_unique_blobs": 2,
        "guide_occurrences": 20,
        "guide_unique_blob_physical_lines": 854,
        "guide_unique_blobs": 8,
        "python_occurrences": 129,
        "python_releases": 20,
        "python_unique_blob_physical_lines": 29_952,
        "python_unique_blobs": 84,
        "result_tool_cross_binding": True,
        "result_tool_occurrences": 35,
        "result_tool_unique_blobs": 14,
        "source_disposition_records": 157,
        "test_occurrences": 44,
        "test_unique_blobs": 29,
    }
    return finish({
        "artifact": "PHASE_067_SOURCE_DISPOSITION_MATRIX",
        "authority": AUTHORITY_FALSE,
        "baseline_commit": BASELINE,
        "blob_disposition_groups": groups,
        "branch": BRANCH,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "disposition_enum": list(DISPOSITIONS),
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": SUBJECT,
        "gate": GATE,
        "generated_date": DATE,
        "inputs": manifest,
        "json_outputs_last": True,
        "persistence_terminal": PERSISTENCE,
        "phase": 67,
        "result_first": True,
        "schema_version": "P067-S90.1-SOURCE-DISPOSITION-V1",
        "source_contract": source_contract,
        "source_dispositions": rows,
        "step": "90.1",
    })


FINDING_SPECS = (
    (82, FULL_READ, "blob_attestations", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_COMPLETE_READ_ATTESTATION"),
    (82, INVENTORY, "genealogy_commit_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_GENEALOGY_ONLY"),
    (83, STATE_FLOW, "flow_records", "PHASE-074-FOUNDATION", "PRESERVE", "INTERNAL_STATIC_FLOW_ONLY"),
    (83, STATE_FLOW, "source_records", "PHASE-074-FOUNDATION", "PRESERVE", "INTERNAL_SOURCE_IDENTITY_ONLY"),
    (84, CALL_GRAPH, "behavior_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_RUNTIME_CALL_GRAPH_ONLY"),
    (84, CALL_GRAPH, "blob_graph_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_STATIC_CALL_GRAPH_ONLY"),
    (84, CALL_GRAPH, "coverage_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_COVERAGE_ONLY"),
    (84, CALL_GRAPH, "source_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_SOURCE_IDENTITY_ONLY"),
    (85, STATE_DEFAULT, "case_contract", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_STATE_CASE_ONLY"),
    (85, STATE_DEFAULT, "inputs", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_INPUT_BINDING_ONLY"),
    (85, STATE_DEFAULT, "saved_profiles", "PHASE-085-STRUCTURE-DEFAULT-CONTRACT", "WITHHOLD", "SAVED_PROFILE_NOT_DEFAULT_AUTHORITY"),
    (85, STATE_DEFAULT, "owner_resolution", "PHASE-083-IMPLEMENTATION-CONTRACT", "GROUND_NOT_FOUND", "EXACT_NAME_SEARCH_ONLY_NO_SERIALIZED_COMPATIBILITY"),
    (85, SAVED_RUNTIME, "runs", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_FRESH_PROCESS_BEHAVIOR_ONLY"),
    (85, SAVED_RUNTIME, "process_pair_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_CROSS_RUNTIME_BEHAVIOR_ONLY"),
    (86, TEST_MATRIX, "python_blob_static_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_STATIC_TEST_EVIDENCE_ONLY"),
    (86, TEST_MATRIX, "runtime_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_RUNTIME_TEST_EVIDENCE_ONLY"),
    (86, TEST_MATRIX, "golden_blob_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_REGRESSION_BYTES_ONLY"),
    (86, TEST_MATRIX, "golden_route_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_GOLDEN_ROUTE_ONLY"),
    (86, GUIDE_MATRIX, "guide_blob_records", "PHASE-087-MANUSCRIPT-ASSEMBLY", "WITHHOLD", "GUIDE_SELF_REPORT_NOT_SCIENTIFIC_AUTHORITY"),
    (86, GUIDE_MATRIX, "tool_blob_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "WITHHOLD", "TOOL_SELF_REPORT_NOT_GATE_AUTHORITY"),
    (87, UNIT_MATRIX, "limitation_records", "PHASE-076-NONEQUILIBRIUM-KINETICS", "WITHHOLD", "BOUNDED_NUMERICAL_LIMITATION"),
    (87, UNIT_MATRIX, "probe_records", "PHASE-082-CANONICAL-EQUATION-FREEZE", "PRESERVE", "INTERNAL_NUMERICAL_PROBE_ONLY"),
    (87, UNIT_MATRIX, "source_feature_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_SOURCE_FEATURE_ONLY"),
    (87, UNIT_MATRIX, "source_occurrence_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_SOURCE_OCCURRENCE_ONLY"),
    (87, UNIT_MATRIX, "tolerance_provenance_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_TOLERANCE_PROVENANCE_ONLY"),
    (88, GUARD_MATRIX, "candidate_disposition_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_CANDIDATE_CLASSIFICATION_ONLY"),
    (88, GUARD_MATRIX, "guard_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_NUMERICAL_GUARD_ONLY"),
    (88, GUARD_MATRIX, "impact_probe_records", "PHASE-088-SCIENTIFIC-REDTEAM", "PRESERVE", "INTERNAL_GUARD_IMPACT_ONLY"),
    (88, GUARD_MATRIX, "numerical_default_records", "PHASE-085-STRUCTURE-DEFAULT-CONTRACT", "WITHHOLD", "HISTORICAL_DEFAULT_NOT_CANONICAL_DEFAULT"),
    (88, GUARD_MATRIX, "open_gap_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "WITHHOLD", "OPEN_SOFTWARE_BOUNDARY"),
    (88, GUARD_MATRIX, "optimizer_route_records", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "WITHHOLD", "OPTIMIZER_RETURN_NOT_CONVERGENCE_AUTHORITY"),
    (88, GUARD_MATRIX, "source_feature_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_SOURCE_FEATURE_ONLY"),
    (88, GUARD_MATRIX, "source_occurrence_records", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "INTERNAL_SOURCE_OCCURRENCE_ONLY"),
    (88, GUARD_MATRIX, "supplemental_optimizer_source_record", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "WITHHOLD", "SUPPLEMENTAL_STATIC_SOURCE_ONLY"),
    (89, FITTING_MATRIX, "evidence_records", "PHASE-086-CALIBRATION-VALIDATION", "PRESERVE", "BOUNDED_REPOSITORY_FITTING_EVIDENCE_ONLY"),
    (89, FITTING_MATRIX, "absent_class_records", "PHASE-086-CALIBRATION-VALIDATION", "PRESERVE", "ABSENCE_CLASSIFICATION_ONLY"),
    (89, FITTING_MATRIX, "bounded_obligations", "PHASE-086-CALIBRATION-VALIDATION", "WITHHOLD", "EXPLICITLY_BOUNDED_NOT_RESOLVED"),
    (89, FITTING_MATRIX, "comparison_source_contracts", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "WITHHOLD", "STATIC_RECONSTRUCTION_CONTRACT_ONLY"),
    (89, FITTING_MATRIX, "saved_profile_records", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "WITHHOLD", "SAVED_ROUNDED_PROFILE_ONLY"),
    (89, FITTING_MATRIX, "phase066_inputs", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "PRESERVE", "SEALED_PHASE066_INPUT_ONLY"),
    (89, FITTING_MATRIX, "supplemental_inputs", "PHASE-072-DATA-PROVENANCE", "PRESERVE", "SUPPLEMENTAL_REPOSITORY_OBJECT_ONLY"),
    (89, FITTING_MATRIX, "supplemental_route_contracts", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "WITHHOLD", "UNEXECUTED_STATIC_ROUTE_ONLY"),
    (89, FITTING_MATRIX, "missing_evidence", "PHASE-086-CALIBRATION-VALIDATION", "GROUND_NOT_FOUND", "MISSING_EVIDENCE_EXPLICIT"),
    (89, FITTING_RUNTIME, "original_optimizer_state_availability", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "GROUND_NOT_FOUND", "ORIGINAL_OPTIMIZER_STATE_GROUND_NOT_FOUND"),
    (89, FITTING_RUNTIME, "saved_consistency_checks", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "PRESERVE", "SAVED_VALUE_CONSISTENCY_ONLY"),
    (89, FITTING_RUNTIME, "sealed_replay_records", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", "PRESERVE", "SEALED_PRIOR_REPLAY_ONLY"),
    (89, FITTING_RUNTIME, "static_source_checks", "PHASE-083-IMPLEMENTATION-CONTRACT", "PRESERVE", "STATIC_SOURCE_CHECK_ONLY"),
)


def pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def rows_for(value: dict[str, Any], collection: str) -> list[tuple[str | None, Any]]:
    item = value[collection]
    if isinstance(item, list):
        return [(str(index), row) for index, row in enumerate(item)]
    if isinstance(item, dict):
        if collection in {"owner_resolution", "supplemental_optimizer_source_record"}:
            return [(None, item)]
        return [(pointer_escape(str(key)), item[key]) for key in sorted(item)]
    raise BuildError("E_FINDING_COLLECTION")


def build_findings(values: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    records: list[dict[str, Any]] = []
    family_counts: dict[str, int] = {}
    for step, path, collection, owner, default_disposition, ceiling in FINDING_SPECS:
        source_rows = rows_for(values[path], collection)
        family = f"S{step}:{Path(path).stem}:{collection}"
        family_counts[family] = len(source_rows)
        for _index, (pointer_suffix, source) in enumerate(source_rows):
            disposition = default_disposition
            row_owner = owner
            target_phase = int(owner.split("-")[1]) if owner.startswith("PHASE-") else 67
            relation_links: list[str] = []
            state = "PRESERVED_BOUNDED_EVIDENCE"
            if path == GUARD_MATRIX and collection == "candidate_disposition_records":
                disposition = "PRESERVE" if source["selected_for_step88"] else "WITHHOLD"
            if path == GUARD_MATRIX and collection == "guard_records" and source.get("guard_id") == "G21":
                disposition = "GROUND_NOT_FOUND"
                relation_links = ["P067-OBL-0003"]
            if path == GUARD_MATRIX and collection == "open_gap_records":
                gap = source["gap_id"]
                if gap == "O01":
                    row_owner, target_phase = "PHASE-074-FOUNDATION", 74
                    disposition = "CORRECT"
                    relation_links = ["P065-OBL-0061"]
                elif gap == "O02":
                    relation_links = ["P067-OBL-0001"]
                elif gap == "O03":
                    disposition = "CORRECT"
                    relation_links = ["P065-OBL-0043", "P065-OBL-0060",
                                      "P066-OBL-0088", "P067-OBL-0002"]
            if path == FITTING_MATRIX and collection == "bounded_obligations":
                oid = source["obligation_id"]
                if oid in {"P065-OBL-0054", "P066-OBL-0120"}:
                    row_owner, target_phase = "PHASE-080-BLEND-CLOSURE", 80
                else:
                    row_owner, target_phase = "PHASE-086-CALIBRATION-VALIDATION", 86
                relation_links = [oid]
            if disposition == "GROUND_NOT_FOUND":
                state = "GROUND_NOT_FOUND"
            elif disposition == "WITHHOLD":
                state = "WITHHELD_OR_OPEN_BOUNDARY"
            records.append({
                "acceptance_criterion": f"{row_owner} must resolve or explicitly bound this exact record before its target gate.",
                "authority_ceiling": ceiling,
                "canonical_owner": row_owner,
                "disposition": disposition,
                "disposition_id": f"P067-FINDING-{len(records) + 1:05d}",
                "external_authority_promoted": False,
                "origin_path": path,
                "origin_pointer": (
                    f"/{collection}/{pointer_suffix}"
                    if pointer_suffix is not None else f"/{collection}"
                ),
                "origin_record_sha256": record_hash(source),
                "origin_step": step,
                "relation_links": relation_links,
                "state": state,
                "target_phase": target_phase,
            })
    require(len(records) == len({row["disposition_id"] for row in records}),
            "E_FINDING_IDS")
    return records, family_counts


TRANSITION_POLICIES = {
    "P065-OBL-0054": (
        "P065-S72-F04", "PHASE-080-BLEND-CLOSURE", 80,
        "Declare one consistent blend denominator and close the finite-rate current-partition/nonadditivity model contract without treating an in-sample fit as material proof.",
        "NO_FINITE_RATE_BLEND_OR_MATERIAL_AUTHORITY"),
    "P066-OBL-0120": (
        "P066-P79-07", "PHASE-080-BLEND-CLOSURE", 80,
        "Derive the finite-rate host current-partition and nonadditive blend closure; retain the distinct in-sample fit identity without treating it as proof.",
        "NO_FINITE_RATE_HOST_INDEPENDENCE_CURRENT_PARTITION_OR_NONADDITIVITY_AUTHORITY"),
    "P066-OBL-0125": (
        "P066-R80-14", "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
        "Dispatch serialized regular-solution kernel metadata through an explicit parser/constructor contract or reject it explicitly; do not infer support from saved keys.",
        "NO_SERIALIZED_REGSOL_COMPATIBILITY_OR_EXTERNAL_PROFILE_AUTHORITY"),
}

NEW_OBLIGATION_POLICIES = (
    ("P067-OBL-0001", "P067-S88-O02", "open_gap_records", 1,
     "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
     "Arbitrary nonmonotonic chronology is not represented by voltage sorting.",
     "Represent chronology explicitly or reject unsupported nonmonotonic inputs with a tested contract.",
     "NO_ARBITRARY_NONMONOTONIC_CHRONOLOGY_AUTHORITY", []),
    ("P067-OBL-0002", "P067-S88-O03", "open_gap_records", 2,
     "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
     "Root and optimizer exhaustion paths do not uniformly return checked convergence state.",
     "Return and test convergence/residual status for every root and optimizer exit, including exhaustion.",
     "NO_CONVERGENCE_CLAIM_FROM_RETURN_VALUE_ALONE",
     ["P065-OBL-0043", "P065-OBL-0060", "P066-OBL-0088"]),
    ("P067-OBL-0003", "P067-S88-G21", "guard_records", 20,
     "PHASE-083-IMPLEMENTATION-CONTRACT", 83,
     "Transfer-helper uniform-grid and length preconditions are prose-only executable guards.",
     "Enforce and test exact grid/length preconditions or revise the helper contract to its actual accepted domain.",
     "GROUND_NOT_FOUND_EXECUTABLE_TRANSFER_PRECONDITION", []),
)


def fingerprint(claim: str) -> str:
    return sha(canonical({"claim": claim}))


def build_carry(values: dict[str, dict[str, Any]], manifest: list[dict[str, Any]],
                source: dict[str, Any]) -> dict[str, Any]:
    prior = values[PRIOR_CARRY]
    findings, family_counts = build_findings(values)
    active = copy.deepcopy(prior["active_obligations"])
    require(len(active) == 219, "E_PRIOR_ACTIVE_COUNT")
    transitions: list[dict[str, Any]] = []
    for obligation_id, policy in TRANSITION_POLICIES.items():
        origin, owner, target, criterion, ceiling = policy
        matches = [row for row in active if row["obligation_id"] == obligation_id]
        require(len(matches) == 1, "E_TRANSITION_CARDINALITY")
        row = matches[0]
        require(row["origin_identity"] == origin and row["canonical_owner"] == "P067-CODE-HISTORY"
                and row["state"] == "OPEN_CARRY", "E_TRANSITION_PRIOR")
        counterpart_links = (
            ["P066-OBL-0120"] if obligation_id == "P065-OBL-0054" else
            ["P065-OBL-0054"] if obligation_id == "P066-OBL-0120" else []
        )
        transition = {
            "acceptance_criterion": criterion,
            "authority_ceiling": ceiling,
            "canonical_owner": owner,
            "disposition": "WITHHOLD",
            "external_authority_promoted": False,
            "obligation_id": obligation_id,
            "origin_identity": origin,
            "prior_owner": "P067-CODE-HISTORY",
            "prior_state": "OPEN_CARRY",
            "relation_links": counterpart_links,
            "state": "OPEN_CARRY_EXPLICITLY_BOUNDED_P067",
            "target_phase": target,
        }
        transitions.append(transition)
        row.update({
            "acceptance_criterion": criterion,
            "canonical_owner": owner,
            "external_authority_promoted": False,
            "relation_links": sorted(set(row.get("relation_links", [])) |
                                     set(counterpart_links)),
            "state": transition["state"],
            "target_phase": target,
        })

    new_obligations: list[dict[str, Any]] = []
    for (obligation_id, origin, origin_collection, origin_index, owner, target,
         claim, criterion, ceiling, links) in NEW_OBLIGATION_POLICIES:
        origin_record = values[GUARD_MATRIX][origin_collection][origin_index]
        require(origin_record.get("gap_id", origin_record.get("guard_id")) == origin.rsplit("-", 1)[-1],
                "E_NEW_OBLIGATION_ORIGIN")
        new_obligations.append({
            "acceptance_criterion": criterion,
            "authority_ceiling": ceiling,
            "canonical_owner": owner,
            "claim": claim,
            "external_authority_promoted": False,
            "obligation_id": obligation_id,
            "origin_identity": origin,
            "origin_path": GUARD_MATRIX,
            "origin_pointer": f"/{origin_collection}/{origin_index}",
            "origin_record_sha256": record_hash(origin_record),
            "relation_links": links,
            "semantic_fingerprint": fingerprint(claim),
            "state": "OPEN_CARRY",
            "target_phase": target,
        })
    active.extend(new_obligations)
    require(len(active) == 222 and len({row["obligation_id"] for row in active}) == 222,
            "E_ACTIVE_CARDINALITY")
    require(sum(row["canonical_owner"] == "P067-CODE-HISTORY" for row in active) == 0,
            "E_P067_OWNER_NOT_DISPOSITIONED")
    prior_ids = {row["obligation_id"] for row in prior["active_obligations"]}
    active_ids = {row["obligation_id"] for row in active}
    new_ids = {row["obligation_id"] for row in new_obligations}
    require(active_ids == prior_ids | new_ids and not (prior_ids & new_ids),
            "E_ACTIVE_ID_CONTINUITY")
    require(all(isinstance(row.get("canonical_owner"), str) and row["canonical_owner"]
                for row in active), "E_ACTIVE_OWNER")
    require(not any(row.get("external_authority_promoted") is True for row in active),
            "E_ACTIVE_EXTERNAL_PROMOTION")

    registry = copy.deepcopy(prior["current_owner_duplicate_check_universe"])
    require(registry["record_count"] == 355 and len(registry["records"]) == 355,
            "E_PRIOR_REGISTRY")
    by_origin = {row["origin_identity"]: row for row in registry["records"]}
    require(len(by_origin) == 355, "E_PRIOR_REGISTRY_ORIGIN_DUPLICATE")
    for transition in transitions:
        record = by_origin[transition["origin_identity"]]
        record.update({"owner_id": transition["canonical_owner"],
                       "state": transition["state"],
                       "target_phase": transition["target_phase"]})
    for index, obligation in enumerate(new_obligations, start=356):
        registry["records"].append({
            "origin_identity": obligation["origin_identity"],
            "origin_record_sha256": obligation["origin_record_sha256"],
            "owner_id": obligation["canonical_owner"],
            "registry_id": f"P067-OWNER-{index:04d}",
            "state": obligation["state"],
            "target_phase": obligation["target_phase"],
        })
    registry["record_count"] = len(registry["records"])
    registry["records_sha256"] = sha(canonical(registry["records"]))
    require(registry["record_count"] == 358, "E_CURRENT_REGISTRY")
    require(len({row["origin_identity"] for row in registry["records"]}) == 358
            and len({row["registry_id"] for row in registry["records"]}) == 358,
            "E_CURRENT_REGISTRY_DUPLICATE")

    disposition_counts = {name: sum(row["disposition"] == name for row in findings)
                          for name in DISPOSITIONS}
    authority_boundary = {
        **AUTHORITY_FALSE,
        "external_scientific_authority": False,
        "held_out_validation": False,
        "identifiability": False,
        "material_assignment": False,
        "original_optimizer_state": False,
        "phase_or_mechanism_identification": False,
        "protocol_binding": False,
        "publication": False,
        "stale_pdf_release": False,
        "ref7_original_full_text": "GROUND_NOT_FOUND",
        "named_debts_preserved": {
            "held_out_external": True,
            "material_phase_mechanism": True,
            "original_optimizer_fields": 25,
            "ref7_original_full_text": "GROUND_NOT_FOUND",
            "specimen_protocol_binding": "GROUND_NOT_FOUND",
            "stale_v1025_2_pdf_owner": "PHASE-089-LATEX-PDF-RELEASE-QA",
        },
        "named_obligation_routes": {
            "held_out_cells_rates_temperatures": ["P066-OBL-0087"],
            "material_phase_species": ["P066-OBL-0116", "P066-OBL-0117",
                                       "P066-OBL-0118", "P066-OBL-0119"],
            "missing_competing_profile_external_synthesis": ["P066-OBL-0115"],
            "original_optimizer_state": [f"P066-OBL-{number:04d}"
                                           for number in range(89, 114)],
            "raw_external_specimen_protocol": ["P066-OBL-0086"],
            "ref7": ["P065-OBL-0059"],
            "stale_pdf_release": ["P066-OBL-0007", "P066-OBL-0029",
                                  "P066-OBL-0030", "P066-OBL-0033",
                                  "P066-OBL-0037", "P066-OBL-0038",
                                  "P066-OBL-0060", "P066-OBL-0084",
                                  "P066-OBL-0085"],
        },
        "prior_source_disposition_semantic_sha256": prior["source_disposition_semantic_sha256"],
    }
    gate_summary = {
        "active_obligations": 222,
        "blob_disposition_groups": 94,
        "disposition_counts": disposition_counts,
        "external_authority_promotions": 0,
        "family_counts": family_counts,
        "gate": GATE,
        "lost_inherited_ids": 0,
        "lost_inherited_obligations": 0,
        "multiply_owned_active_obligations": 0,
        "new_obligations": 3,
        "owner_registry_records": 358,
        "owner_transitions": 3,
        "p067_owner_transitions": 3,
        "ownerless_active_obligations": 0,
        "prior_active_obligations": 219,
        "prior_owner_registry_records": 355,
        "source_dispositions": 157,
        "source_disposition_records": source["source_contract"]["source_disposition_records"],
        "status": "PASS_WITH_EXPLICIT_OPEN_CARRY",
    }
    return finish({
        "active_obligations": active,
        "artifact": "PHASE_067_CARRY_FORWARD_DELTA",
        "authority_boundary": authority_boundary,
        "baseline_commit": BASELINE,
        "branch": BRANCH,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "current_owner_duplicate_check_universe": registry,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": SUBJECT,
        "gate": GATE,
        "gate_summary": gate_summary,
        "generated_date": DATE,
        "inputs": manifest,
        "json_outputs_last": True,
        "new_obligations": new_obligations,
        "owner_transitions": transitions,
        "persistence_terminal": PERSISTENCE,
        "phase": 67,
        "prior_phase066_carry": prior,
        "result_first": True,
        "schema_version": "P067-S90.1-CARRY-FORWARD-V1",
        "source_disposition_semantic_sha256": source["semantic_sha256"],
        "step": "90.1",
        "step82_89_disposition_records": findings,
    })


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    values, manifest = read_inputs()
    source = build_source(values, manifest)
    carry = build_carry(values, manifest, source)
    return source, carry


def atomic_write(path: Path, raw: bytes) -> None:
    require(path.parent == (ROOT / path.relative_to(ROOT)).parent, "E_OUTPUT_PATH")
    temporary = path.with_name(path.name + ".tmp-p067-s90-1")
    temporary.write_bytes(raw)
    os.replace(temporary, path)


def verify_human_prerequisites() -> None:
    required_tokens = (
        "Step 90.1", GATE, EXPECTED_PARENT, SUBJECT,
        "PASS_PENDING_PERSISTENCE", "Step 90.2",
    )
    for path in HUMAN_PREREQUISITES:
        target = ROOT / path
        require(target.is_file(), "E_RESULT_FIRST_MISSING")
        raw = target.read_bytes()
        require(len(raw) <= 2_000_000, "E_RESULT_FIRST_BYTES")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BuildError("E_RESULT_FIRST_UTF8") from exc
        require(all(token in text for token in required_tokens),
                "E_RESULT_FIRST_CONTRACT")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    try:
        if not args.preview:
            verify_human_prerequisites()
        source, carry = build()
        if args.preview:
            sys.stdout.buffer.write(canonical({
                "carry_forward": carry,
                "source_disposition": source,
            }))
        else:
            atomic_write(ROOT / SOURCE_PATH, canonical(source))
            atomic_write(ROOT / CARRY_PATH, canonical(carry))
            print(GATE)
        return 0
    except (BuildError, OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
