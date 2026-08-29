#!/usr/bin/env python3
"""Validate Phase 064 Step 68 authority evidence and Git persistence."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any, Callable, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[3]
MATRIX_PATH = ROOT / "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json"
BUILDER = ROOT / "Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py"
RESULT = ROOT / "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "4dec72387220e7210fc15d0323ca481a172111fd"
EXPECTED_SUBJECT = "audit(phase064): adjudicate v1023 validation authority"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P064_STEP68_AUTHORITY"
PERSISTENCE = "PASS_P064_STEP68_PERSISTENCE"

EXACT_PATHS = [
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md",
    "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json",
    "Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py",
    "Codex/work/v1023_phase064/validate_phase064_step68.py",
]
EXACT_SET = set(EXACT_PATHS)

PLANNED_IDS = [
    "EXE-G1", "EXE-G2", "EXE-G3", "EXE-NT", "EXE-R6-G1", "EXE-R6-G2",
    "EXE-R6-G3", "EXE-R6-COV", "EXE-GE1", "EXE-GE2", "EXE-GE3", "EXE-GE4",
    "EXE-GE5", "DECL-P1-A", "DECL-P1-B", "DECL-P1-C", "DECL-P2-01",
    "DECL-P2-02", "DECL-P2-03", "DECL-P2-04", "DECL-P2-05", "DECL-P2-06",
    "DECL-P2-07", "DECL-P2-08", "DECL-P3-01", "DECL-P3-02", "DECL-P3-03",
    "DECL-P3-04", "DECL-P3-05", "DECL-P3-06", "DECL-P4-SKIP", "DECL-P5-01",
    "DECL-P5-02", "DECL-P5-03", "DECL-P5-04", "DECL-P5-05", "DECL-P5-06",
]
EXTRA_IDS = [
    "CUR-P064-ACT", "CUR-P064-S64", "CUR-P064-S65", "CUR-P064-S66", "CUR-P064-S67",
    "HIST-P0-BASELINE", "DECL-P1-STOP", "STATIC-STRUCTURE", "OBS-CURVE-QA", "OBS-P1-RATIO",
]
EXPECTED_IDS = PLANNED_IDS + EXTRA_IDS

AXES = [
    "synthetic_numerical", "implementation_regression", "picard_iteration_behavior",
    "transfer_identity", "material_validation", "experimental_validation",
    "external_primary_literature_validation",
]
AXIS_VALUES = {
    "NOT_EVALUATED", "NOT_ESTABLISHED", "ESTABLISHED_BOUNDED_INTERNAL",
    "ESTABLISHED_BOUNDED_JCP147_REF6_METHOD_ONLY",
}

EXPECTED_COUNTS = {
    "additional_boundary_records": 5,
    "complete_authority_records": 47,
    "current_phase_gate_records": 5,
    "executable_hard_gates": 13,
    "experimental_validated_gates": 0,
    "external_comprehensive_validated_gates": 0,
    "material_validated_gates": 0,
    "overclaim_routes": 14,
    "planned_core_gate_records": 37,
    "planned_phase_gate_declarations": 24,
    "supplemental_evidence_records": 7,
}

EXPECTED_HUMAN = {
    "axis_count": 7,
    "complete_authority_record_denominator": 47,
    "executable_hard_gates": 13,
    "experimental_validated_gates": 0,
    "external_comprehensive_validated_gates": 0,
    "gate": GATE,
    "material_validated_gates": 0,
    "overclaim_routes": 14,
    "phase_ceiling": "CONDITIONAL_P064",
    "planned_core_gate_denominator": 37,
    "planned_phase_gate_declarations": 24,
    "ref7_original_status": "GROUND_NOT_FOUND",
    "supplemental_evidence_records": 7,
}

EXPECTED_SOURCE_SPECS: dict[str, tuple[str, int, tuple[tuple[int, int], ...]]] = {
    "Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md": (EXPECTED_PARENT, 179, ((1,28),(155,179))),
    "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md": (EXPECTED_PARENT, 272, ((230,272),)),
    "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md": (EXPECTED_PARENT, 254, ((5,28),(210,254))),
    "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md": (EXPECTED_PARENT, 308, ((217,264),(296,308))),
    "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md": (EXPECTED_PARENT, 238, ((118,180),(190,238))),
    "Claude/docs/v1.0.23/test_gates_v1023.py": (BASELINE, 626, ((162,188),(196,325),(336,385),(389,431),(439,482),(485,526),(529,565),(568,622))),
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": (BASELINE, 128, ((26,37),(39,58),(60,88),(90,105),(107,128))),
    "Claude/docs/v1.0.23/results/PHASE_P1_RESULT.md": (BASELINE, 112, ((63,85),(87,95))),
    "Claude/docs/v1.0.23/results/PHASE_P2_RESULT.md": (BASELINE, 114, ((76,93),)),
    "Claude/docs/v1.0.23/results/PHASE_P3_RESULT.md": (BASELINE, 102, ((51,81),)),
    "Claude/docs/v1.0.23/results/PHASE_P5_RESULT.md": (BASELINE, 95, ((43,76),(85,91))),
    "Claude/docs/v1.0.23/results/comp_v23/AUD_REPORT_v23.md": (BASELINE, 65, ((1,13),(20,40),(52,65))),
    "Claude/docs/v1.0.23/results/MERGE_READINESS_v23.md": (BASELINE, 52, ((1,13),(31,52))),
    "Claude/docs/v1.0.23/results/qa_images/CURVE_QA_v23.md": (BASELINE, 38, ((1,20),(22,38))),
    "Claude/docs/v1.0.23/results/V1023_EXECUTION_LEDGER.md": (BASELINE, 12, ((1,12),)),
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": (BASELINE, 68, ((1,18),(45,68))),
    "Claude/docs/v1.0.23/results/tools_check_structure.py": (BASELINE, 170, ((95,121),(154,170))),
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py": (BASELINE, 156, ((18,30),(50,106),(109,156))),
}

PRIOR_INPUTS = [
    "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json",
    "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json",
    "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json",
    "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json",
    "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json",
]
DOC_PATHS = [
    "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]

ROOT_KEYS = {
    "artifact_kind", "authority_axes", "authority_records", "authority_summary",
    "baseline_commit", "containing_commit", "counts", "document_contracts",
    "expected_parent", "expected_subject", "gate", "generated_by", "generated_date",
    "high_risk_bindings", "human_evidence", "human_evidence_semantic_sha256", "json_type_projection_sha256",
    "literature_boundary", "non_double_count", "overclaim_routes", "phase",
    "phase_ceiling", "prior_machine_inputs", "repository_boundary", "schema_version",
    "semantic_sha256", "source_contracts", "status", "step", "supplemental_evidence",
}
RECORD_KEYS = {
    "axes", "counts_once_in_gate_denominator", "depends_on", "evidence_class", "id",
    "label", "limitation", "max_authority", "record_kind", "source", "verdict",
}
SOURCE_ROW_KEYS = {
    "path", "commit", "git_blob", "sha256", "bytes", "lines", "read_coverage",
    "read_status", "source_spans",
}
SPAN_KEYS = {"start", "end", "sha256"}
ROUTE_KEYS = {"id", "claim", "disposition", "owner", "acceptance_criterion"}
SUPPLEMENTAL_KEYS = {"id", "kind", "source", "axes", "fresh_status", "limitation"}
PRIOR_KEYS = {"path", "git_blob", "sha256", "bytes", "semantic_sha256"}
DOCUMENT_KEYS = {"path", "sha256", "bytes", "required_snippets"}
EXPECTED_RECORDS_SHA256 = "bf1b48e84ed610a1e1b9cfca27651e0173ee99a72079212be4a664f4568cd17d"
EXPECTED_SUPPLEMENTAL_SHA256 = "1d8965337e15362840299ce726b3a1d1d288a2a0e8faa88fc1c7f4077681a427"
EXPECTED_ROUTES_SHA256 = "8f6713048e1e52afc3eb9cec52f35e2a217ffe4ca1c3ae32c3292e4aba2d9ca3"
EXPECTED_SOURCES_SHA256 = "5baa029585749462df25f399838519657f052995e893fd126a54e45c8e57a8c6"
EXPECTED_PRIOR_SHA256 = "1e8d95a7d6fa34042cc0a9a880853430039f07e2b382ee8586fb0d4ffd157601"
EXPECTED_DOCS_SHA256 = "e40ca9cf05d3c4934cd2b494664f3aa8d41a59b7f1e3be09f9d1cb3f8ab495de"
EXPECTED_NONDOUBLE_SHA256 = "54ea21e6315c07bfa116fbd3096e81ce2b4635ad9f9362339631d6e94ddaca6e"
EXPECTED_LITERATURE_SHA256 = "b0a21f05ae66371dea7fd5723b3bb5f2d6d520250355b328caed1a4e1ffb10d9"
EXPECTED_AUTHORITY_SHA256 = "372f5dc82beec1a8d09c597d2d92a3417e6b67123fc9a1f8667e9c84da96c28c"
EXPECTED_REPO_SHA256 = "52345e09ceff24a023d7ef4e8e9a5c97f95b8f9d48891484a4dbb5342c3e162e"
EXPECTED_HUMAN_SHA256 = "77734cac360c9c398930af803905fcb2b6f34cbf242acd8fb1ce32960b4ebd6f"
EXPECTED_HIGH_RISK_SHA256 = "b65c4ea98430774bf81674d43d78034a7349e6e7ea9695f2d066679b6d0dd44c"
EXPECTED_TYPE_SHA256 = "a8f0db6390fc5a4fc744ea5f1afdecc66f0b4c322bce1c075287c5c248757c0f"
EXPECTED_BUILDER_GIT_BLOB = "c3b27b701b2bb8b70cb3f47e968eed2f1cd308fa"
EXPECTED_VALIDATOR_CANONICAL_SHA256 = "a1a93dd74489e2095e5d99f7e3a96e58140c0b4955072bdabd3cfdf85be51d4a"
EXPECTED_VALIDATOR_AST_SHA256_312 = "ed22d16abb93888e5039131554668017955cb18c99b9bba9c55847feed0adc8b"
EXPECTED_VALIDATOR_AST_SHA256_314 = "e6758b7e363f0fa8c406c44dcd7cab354157a33ae01908bde03c9373952801fa"


class ValidationError(RuntimeError):
    pass


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def json_type_projection(value: Any) -> Any:
    if value is None: return "null"
    if type(value) is bool: return "bool"
    if type(value) is int: return "int"
    if type(value) is float: return "float"
    if type(value) is str: return "str"
    if type(value) is list: return [json_type_projection(item) for item in value]
    if type(value) is dict: return {key: json_type_projection(value[key]) for key in sorted(value)}
    raise ValidationError(f"E_JSON_TYPE_PROJECTION:{type(value)!r}")


def rehash(payload: dict[str, Any], *, type_hash: bool = True) -> None:
    payload.pop("semantic_sha256", None)
    if type_hash:
        payload.pop("json_type_projection_sha256", None)
        payload["json_type_projection_sha256"] = sha256(compact_bytes(json_type_projection(payload)))
    payload["semantic_sha256"] = sha256(compact_bytes(payload))


def traverse(value: Any, depth: int = 0) -> int:
    if depth > 80:
        raise ValidationError("E_JSON_DEPTH")
    if type(value) is dict:
        if len(value) > 10000: raise ValidationError("E_JSON_CONTAINER")
        return 1 + sum(traverse(k, depth + 1) + traverse(v, depth + 1) for k, v in value.items())
    if type(value) is list:
        if len(value) > 10000: raise ValidationError("E_JSON_CONTAINER")
        return 1 + sum(traverse(v, depth + 1) for v in value)
    if type(value) is str and len(value) > 1_000_000:
        raise ValidationError("E_JSON_STRING")
    return 1


def strict_load_bytes(raw: bytes, source: str) -> tuple[Any, int]:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"E_JSON_PARSE:{source}:utf8") from exc

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out: raise ValidationError(f"E_JSON_DUPLICATE:{source}:{key}")
            out[key] = value
        return out

    def constant(value: str) -> Any:
        raise ValidationError(f"E_JSON_NONFINITE:{source}:{value}")

    def bounded_int(value: str) -> int:
        digits = value.lstrip("+-")
        if len(digits) > 128: raise ValidationError(f"E_JSON_HUGE_INT:{source}")
        return int(value)

    def bounded_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed): raise ValidationError(f"E_JSON_NUMERIC_OVERFLOW:{source}")
        return parsed

    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant,
                           parse_int=bounded_int, parse_float=bounded_float)
    except ValidationError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValidationError(f"E_JSON_PARSE:{source}") from exc
    nodes = traverse(value)
    return value, nodes


def strict_load(path: pathlib.Path) -> tuple[dict[str, Any], int, bytes]:
    raw = path.read_bytes()
    value, nodes = strict_load_bytes(raw, path.as_posix())
    if type(value) is not dict:
        raise ValidationError("E_JSON_ROOT")
    return value, nodes, raw


def run(args: Iterable[str], *, cwd: pathlib.Path = ROOT, check: bool = True,
        timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(list(args), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=timeout, check=False)
    if check and cp.returncode:
        raise ValidationError(f"E_COMMAND:{list(args)!r}:{cp.stderr.decode('utf-8','replace')}")
    return cp


def git(args: list[str], *, check: bool = True, cwd: pathlib.Path = ROOT) -> subprocess.CompletedProcess[bytes]:
    return run(("git", *args), cwd=cwd, check=check)


def git_text(*args: str, cwd: pathlib.Path = ROOT) -> str:
    return git(list(args), cwd=cwd).stdout.decode("utf-8", "strict").strip()


def git_bytes(commit: str, path: str) -> bytes:
    return git(["show", f"{commit}:{path}"]).stdout


def span_hash(raw: bytes, start: int, end: int) -> str:
    lines = raw.decode("utf-8", "strict").splitlines(keepends=True)
    if not (1 <= start <= end <= len(lines)):
        raise ValidationError("E_SOURCE_SPAN")
    return sha256("".join(lines[start - 1:end]).encode("utf-8"))


def type_errors(payload: dict[str, Any]) -> list[str]:
    if type(payload) is not dict: return ["E_JSON_ROOT"]
    if set(payload) != ROOT_KEYS: return ["E_ROOT_KEYS"]
    required_ints = ("schema_version", "phase")
    required_strs = ("artifact_kind", "step", "generated_date", "generated_by", "baseline_commit",
                     "expected_parent", "expected_subject", "containing_commit", "status", "gate",
                     "phase_ceiling", "json_type_projection_sha256", "semantic_sha256",
                     "human_evidence_semantic_sha256")
    if any(type(payload[k]) is not int for k in required_ints): return ["E_JSON_TYPE_PROJECTION"]
    if any(type(payload[k]) is not str for k in required_strs): return ["E_JSON_TYPE_PROJECTION"]
    if type(payload["counts"]) is not dict or any(type(v) is not int for v in payload["counts"].values()): return ["E_JSON_TYPE_PROJECTION"]
    if any(type(payload[k]) is not dict for k in ("human_evidence", "high_risk_bindings", "non_double_count", "literature_boundary", "authority_summary", "repository_boundary")): return ["E_NESTED_KEYS"]
    if type(payload["authority_axes"]) is not list or any(type(v) is not str for v in payload["authority_axes"]): return ["E_JSON_TYPE_PROJECTION"]
    if any(type(payload[k]) is not list for k in ("authority_records", "supplemental_evidence", "overclaim_routes", "source_contracts", "prior_machine_inputs", "document_contracts")): return ["E_JSON_TYPE_PROJECTION"]
    for record in payload["authority_records"]:
        if type(record) is not dict or set(record) != RECORD_KEYS: return ["E_NESTED_KEYS"]
        if any(type(record[k]) is not str for k in ("id", "record_kind", "label", "verdict", "evidence_class", "max_authority", "limitation")): return ["E_JSON_TYPE_PROJECTION"]
        if type(record["counts_once_in_gate_denominator"]) is not bool or record["counts_once_in_gate_denominator"] is not True: return ["E_JSON_TYPE_PROJECTION"]
        if type(record["depends_on"]) is not list or any(type(v) is not str for v in record["depends_on"]): return ["E_JSON_TYPE_PROJECTION"]
        if type(record["axes"]) is not dict or list(record["axes"]) != sorted(AXES): return ["E_JSON_TYPE_PROJECTION"]
        if any(type(v) is not str for v in record["axes"].values()): return ["E_JSON_TYPE_PROJECTION"]
        if type(record["source"]) is not dict or set(record["source"]) != {"path", "commit", "start", "end", "sha256"}: return ["E_NESTED_KEYS"]
        if any(type(record["source"][k]) is not str for k in ("path", "commit", "sha256")) or any(type(record["source"][k]) is not int for k in ("start", "end")): return ["E_JSON_TYPE_PROJECTION"]
    for row in payload["supplemental_evidence"]:
        if type(row) is not dict or set(row) != SUPPLEMENTAL_KEYS: return ["E_NESTED_KEYS"]
        if any(type(row[k]) is not str for k in ("id", "kind", "fresh_status", "limitation")): return ["E_JSON_TYPE_PROJECTION"]
        if type(row["axes"]) is not dict or list(row["axes"]) != sorted(AXES) or any(type(v) is not str for v in row["axes"].values()): return ["E_JSON_TYPE_PROJECTION"]
        source = row["source"]
        if type(source) is not dict or set(source) not in ({"path", "start", "end"}, {"path", "commit"}): return ["E_NESTED_KEYS"]
        if type(source["path"]) is not str or ("commit" in source and type(source["commit"]) is not str) or ("start" in source and (type(source["start"]) is not int or type(source["end"]) is not int)): return ["E_JSON_TYPE_PROJECTION"]
    for row in payload["overclaim_routes"]:
        if type(row) is not dict or set(row) != ROUTE_KEYS: return ["E_NESTED_KEYS"]
        if any(type(row[k]) is not str for k in ROUTE_KEYS): return ["E_JSON_TYPE_PROJECTION"]
    for row in payload["source_contracts"]:
        if type(row) is not dict or set(row) != SOURCE_ROW_KEYS: return ["E_NESTED_KEYS"]
        if any(type(row[k]) is not str for k in ("path", "commit", "git_blob", "sha256", "read_status")) or any(type(row[k]) is not int for k in ("bytes", "lines")): return ["E_JSON_TYPE_PROJECTION"]
        if type(row["read_coverage"]) is not list or len(row["read_coverage"]) != 2 or any(type(v) is not int for v in row["read_coverage"]): return ["E_JSON_TYPE_PROJECTION"]
        if type(row["source_spans"]) is not list: return ["E_JSON_TYPE_PROJECTION"]
        for span in row["source_spans"]:
            if type(span) is not dict or set(span) != SPAN_KEYS: return ["E_NESTED_KEYS"]
            if type(span["start"]) is not int or type(span["end"]) is not int or type(span["sha256"]) is not str: return ["E_JSON_TYPE_PROJECTION"]
    for row in payload["prior_machine_inputs"]:
        if type(row) is not dict or set(row) != PRIOR_KEYS: return ["E_NESTED_KEYS"]
        if any(type(row[k]) is not str for k in ("path", "git_blob", "sha256", "semantic_sha256")) or type(row["bytes"]) is not int: return ["E_JSON_TYPE_PROJECTION"]
    for row in payload["document_contracts"]:
        if type(row) is not dict or set(row) != DOCUMENT_KEYS: return ["E_NESTED_KEYS"]
        if any(type(row[k]) is not str for k in ("path", "sha256")) or type(row["bytes"]) is not int: return ["E_JSON_TYPE_PROJECTION"]
        if type(row["required_snippets"]) is not list or any(type(v) is not str for v in row["required_snippets"]): return ["E_JSON_TYPE_PROJECTION"]
    return []


def matrix_errors(payload: dict[str, Any]) -> list[str]:
    errors = type_errors(payload)
    if errors: return errors
    if (payload["artifact_kind"], payload["schema_version"], payload["phase"], payload["step"]) != ("PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX", 1, 64, "68"): return ["E_MATRIX_IDENTITY"]
    if (payload["baseline_commit"], payload["expected_parent"], payload["expected_subject"], payload["gate"], payload["phase_ceiling"]) != (BASELINE, EXPECTED_PARENT, EXPECTED_SUBJECT, GATE, "CONDITIONAL_P064"): return ["E_MATRIX_IDENTITY"]
    if payload["containing_commit"] != "PENDING_AT_PRECOMMIT_BY_DESIGN" or payload["status"] != "PASS_WITH_CONCERNS": return ["E_MATRIX_STATUS"]
    unsigned = copy.deepcopy(payload); stored_semantic = unsigned.pop("semantic_sha256")
    if stored_semantic != sha256(compact_bytes(unsigned)): return ["E_SEMANTIC_SHA"]
    records = payload["authority_records"]
    ids = [record["id"] for record in records]
    if ids.count("DECL-P4-SKIP") != 1: return ["E_P4_PROCESS_STATE"]
    if ids != EXPECTED_IDS or len(ids) != 47 or len(set(ids)) != 47: return ["E_GATE_DENOMINATOR"]
    if payload["counts"] != EXPECTED_COUNTS: return ["E_COUNTS"]
    if payload["authority_axes"] != AXES: return ["E_AUTHORITY_AXES"]
    by_id = {record["id"]: record for record in records}
    if by_id["DECL-P4-SKIP"]["verdict"] != "INTENTIONALLY_SKIPPED_NOT_EXECUTED" or any(by_id["DECL-P4-SKIP"]["axes"][axis] != ("NOT_ESTABLISHED" if axis in AXES[4:] else "NOT_EVALUATED") for axis in AXES): return ["E_P4_PROCESS_STATE"]
    if by_id["DECL-P2-08"]["verdict"] != "RESERVED_FOR_P3": return ["E_GATE_HISTORY"]
    if by_id["STATIC-STRUCTURE"]["verdict"] != "FAIL_WITH_BASELINE_EXCEPTION": return ["E_STRUCTURE_HISTORY"]
    if by_id["OBS-CURVE-QA"]["verdict"] != "PRINTED_PASS_NON_ENFORCING": return ["E_CURVE_HISTORY"]
    if by_id["OBS-P1-RATIO"]["verdict"] != "UTF8_EXIT0_NON_ENFORCING": return ["E_P1_OBSERVATION_HISTORY"]
    if "general convergence" not in by_id["EXE-GE3"]["limitation"]: return ["E_PICARD_AUTHORITY"]
    if "time/EIS/instrument response" not in by_id["EXE-GE4"]["limitation"]: return ["E_TRANSFER_AUTHORITY"]
    for record in records:
        if set(record["axes"]) != set(AXES) or any(value not in AXIS_VALUES for value in record["axes"].values()): return ["E_AUTHORITY_AXES"]
        if record["axes"]["material_validation"] != "NOT_ESTABLISHED" or record["axes"]["experimental_validation"] != "NOT_ESTABLISHED": return ["E_AUTHORITY_PROMOTION"]
        ext = record["axes"]["external_primary_literature_validation"]
        allowed_ext = "ESTABLISHED_BOUNDED_JCP147_REF6_METHOD_ONLY" if record["id"] in {"DECL-P1-B", "CUR-P064-S65"} else "NOT_ESTABLISHED"
        if ext != allowed_ext: return ["E_AUTHORITY_PROMOTION"]
        if any(dep not in EXPECTED_IDS for dep in record["depends_on"]): return ["E_GATE_BIJECTION"]
        src = record["source"]
        if set(src) != {"path", "commit", "start", "end", "sha256"}: return ["E_GATE_ANCHOR"]
        try: raw = git_bytes(src["commit"], src["path"])
        except Exception: return ["E_GATE_ANCHOR"]
        if src["sha256"] != span_hash(raw, src["start"], src["end"]): return ["E_GATE_ANCHOR"]
    if payload["human_evidence"] != EXPECTED_HUMAN or payload["human_evidence_semantic_sha256"] != sha256(compact_bytes(EXPECTED_HUMAN)): return ["E_HUMAN_EVIDENCE"]
    lit = payload["literature_boundary"]
    if lit.get("ref7_bibliography") != "OFFICIAL_METADATA_DOI_10.1063/1.4802584": return ["E_REF7_DOI"]
    if lit.get("ref6_original") != "FULL_TEXT_READ_PRIMARY_VOR_METHOD_CONTENT_ONLY": return ["E_REF6_IDENTITY"]
    if lit.get("ref7_original") == "JCP147_AS_SUBSTITUTE": return ["E_JCP_SUBSTITUTE"]
    if lit.get("ref7_original") != "GROUND_NOT_FOUND" or lit.get("jcp_ref_to_graphite_material_applicability") != "NOT_ESTABLISHED": return ["E_REF7_GNF"]
    authority = payload["authority_summary"]
    if any(authority.get(k) is not False for k in ("material_validation", "experimental_validation", "comprehensive_external_primary_literature_validation", "canonical_model_selection", "publication_readiness")): return ["E_AUTHORITY_PROMOTION"]
    routes = payload["overclaim_routes"]
    route_ids = [row.get("id") for row in routes]
    if route_ids != [f"AUTH-{i:03d}" for i in range(1, 15)] or len(set(route_ids)) != 14: return ["E_ROUTE_BIJECTION"]
    expected_owners = ["Phase 083", "Phase 073", "Phase 076", "Phase 074", "Phase 076", "Phase 074", "Phase 088", "Phase 081", "Phase 086", "Phase 071", "Phase 075", "Step 69.1", "Phase 083", "Phase 076"]
    for route, owner in zip(routes, expected_owners):
        if set(route) != {"id", "claim", "disposition", "owner", "acceptance_criterion"}: return ["E_ROUTE_SCHEMA"]
        if type(route["owner"]) is not str or not route["owner"] or any(sep in route["owner"] for sep in ("/", ";", ",")): return ["E_ROUTE_OWNER_CARDINALITY"]
        if route["owner"] != owner: return ["E_ROUTE_OWNER_REGISTRY"]
        if type(route["acceptance_criterion"]) is not str or not route["acceptance_criterion"].strip(): return ["E_ROUTE_ACCEPTANCE"]
    by_route = {route["id"]: route for route in routes}
    if by_route["AUTH-006"]["disposition"] != "REJECTED_FACTOR_3600": return ["E_FACTOR_3600_BINDING"]
    if by_route["AUTH-014"]["disposition"] != "NOT_ESTABLISHED": return ["E_COMPUTATIONAL_BENEFIT_BINDING"]
    sources = payload["source_contracts"]
    if [row.get("path") for row in sources] != list(EXPECTED_SOURCE_SPECS): return ["E_SOURCE_IDENTITY"]
    for row in sources:
        if set(row) != SOURCE_ROW_KEYS: return ["E_SOURCE_SCHEMA"]
        path = row["path"]; commit, line_count, spans = EXPECTED_SOURCE_SPECS[path]
        raw = git_bytes(commit, path)
        if (row["commit"], row["git_blob"], row["sha256"], row["bytes"], row["lines"], row["read_coverage"], row["read_status"]) != (commit, git_text("rev-parse", f"{commit}:{path}"), sha256(raw), len(raw), line_count, [1, line_count], "READ_FULL_STEP68"): return ["E_SOURCE_IDENTITY"]
        got_spans = [(sp.get("start"), sp.get("end"), sp.get("sha256")) for sp in row["source_spans"]]
        expected_spans = [(a, b, span_hash(raw, a, b)) for a, b in spans]
        if got_spans != expected_spans: return ["E_SOURCE_SPAN"]
    prior = payload["prior_machine_inputs"]
    if [row.get("path") for row in prior] != PRIOR_INPUTS: return ["E_PRIOR_INPUT"]
    for row in prior:
        raw = git_bytes(EXPECTED_PARENT, row["path"]); parsed, _ = strict_load_bytes(raw, row["path"])
        if type(parsed) is not dict: return ["E_PRIOR_INPUT"]
        expected = {"path": row["path"], "git_blob": git_text("rev-parse", f"{EXPECTED_PARENT}:{row['path']}"), "sha256": sha256(raw), "bytes": len(raw), "semantic_sha256": parsed.get("semantic_sha256")}
        if row != expected: return ["E_PRIOR_INPUT"]
    docs = payload["document_contracts"]
    if [row.get("path") for row in docs] != DOC_PATHS: return ["E_DOCUMENT_IDENTITY"]
    for row in docs:
        raw = (ROOT / row["path"]).read_bytes(); text = raw.decode("utf-8", "strict")
        if row.get("sha256") != sha256(raw) or row.get("bytes") != len(raw): return ["E_DOCUMENT_IDENTITY"]
        if any(snippet not in text for snippet in row.get("required_snippets", [])): return ["E_DOCUMENT_DECLARATIONS"]
    repo = payload["repository_boundary"]
    if repo != {"exact_paths": ["Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py", "Codex/work/v1023_phase064/validate_phase064_step68.py", "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json", "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md", "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md", "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md", "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"], "claude_modified": False, "production_modified": False}: return ["E_REPOSITORY_BOUNDARY"]
    high_risk = payload["high_risk_bindings"]
    if sha256(compact_bytes(high_risk)) != EXPECTED_HIGH_RISK_SHA256: return ["E_HIGH_RISK_BINDING"]
    non_double = payload["non_double_count"]
    if non_double.get("reference_ledger_vs_adopted_bibliography") != "separate process and adopted-source authorities; neither substitutes for the other": return ["E_REFERENCE_LEDGER_CONFLATION"]
    expected_hashes = (
        (records, EXPECTED_RECORDS_SHA256, "E_RECORD_COLLECTION"),
        (payload["supplemental_evidence"], EXPECTED_SUPPLEMENTAL_SHA256, "E_SUPPLEMENTAL_COLLECTION"),
        (routes, EXPECTED_ROUTES_SHA256, "E_ROUTE_COLLECTION"),
        (sources, EXPECTED_SOURCES_SHA256, "E_SOURCE_COLLECTION"),
        (prior, EXPECTED_PRIOR_SHA256, "E_PRIOR_COLLECTION"),
        (docs, EXPECTED_DOCS_SHA256, "E_DOCUMENT_COLLECTION"),
        (non_double, EXPECTED_NONDOUBLE_SHA256, "E_NONDOUBLE_COLLECTION"),
        (lit, EXPECTED_LITERATURE_SHA256, "E_LITERATURE_COLLECTION"),
        (authority, EXPECTED_AUTHORITY_SHA256, "E_AUTHORITY_COLLECTION"),
        (repo, EXPECTED_REPO_SHA256, "E_REPOSITORY_COLLECTION"),
        (payload["human_evidence"], EXPECTED_HUMAN_SHA256, "E_HUMAN_COLLECTION"),
        (high_risk, EXPECTED_HIGH_RISK_SHA256, "E_HIGH_RISK_BINDING"),
    )
    for value, expected, code in expected_hashes:
        if sha256(compact_bytes(value)) != expected: return [code]
    projected = copy.deepcopy(payload); projected.pop("semantic_sha256"); projected.pop("json_type_projection_sha256")
    actual_type_hash = sha256(compact_bytes(json_type_projection(projected)))
    if payload["json_type_projection_sha256"] != EXPECTED_TYPE_SHA256 or actual_type_hash != EXPECTED_TYPE_SHA256: return ["E_JSON_TYPE_PROJECTION"]
    return []


def mutation_tests(payload: dict[str, Any]) -> int:
    tests: list[tuple[str, Callable[[dict[str, Any]], None], str, bool]] = []
    def add(name: str, mutator: Callable[[dict[str, Any]], None], code: str, type_hash: bool = True) -> None:
        tests.append((name, mutator, code, type_hash))
    add("drop_record", lambda p: p["authority_records"].pop(), "E_GATE_DENOMINATOR")
    add("duplicate_record", lambda p: p["authority_records"].append(copy.deepcopy(p["authority_records"][-1])), "E_GATE_DENOMINATOR")
    add("swap_order", lambda p: p["authority_records"].__setitem__(slice(0,2), list(reversed(p["authority_records"][:2]))), "E_GATE_DENOMINATOR")
    add("p4_missing", lambda p: p["authority_records"].pop(next(i for i,r in enumerate(p["authority_records"]) if r["id"]=="DECL-P4-SKIP")), "E_P4_PROCESS_STATE")
    add("p4_fabricated", lambda p: next(r for r in p["authority_records"] if r["id"]=="DECL-P4-SKIP").__setitem__("verdict", "PASS"), "E_P4_PROCESS_STATE")
    add("p2_history", lambda p: next(r for r in p["authority_records"] if r["id"]=="DECL-P2-08").__setitem__("verdict", "PASS"), "E_GATE_HISTORY")
    add("structure_pass", lambda p: next(r for r in p["authority_records"] if r["id"]=="STATIC-STRUCTURE").__setitem__("verdict", "PASS"), "E_STRUCTURE_HISTORY")
    add("curve_hardpass", lambda p: next(r for r in p["authority_records"] if r["id"]=="OBS-CURVE-QA").__setitem__("verdict", "PASS"), "E_CURVE_HISTORY")
    add("p1_hardpass", lambda p: next(r for r in p["authority_records"] if r["id"]=="OBS-P1-RATIO").__setitem__("verdict", "PASS"), "E_P1_OBSERVATION_HISTORY")
    add("material_promotion", lambda p: next(r for r in p["authority_records"] if r["id"]=="EXE-G1")["axes"].__setitem__("material_validation", "ESTABLISHED_BOUNDED_INTERNAL"), "E_AUTHORITY_PROMOTION")
    add("experimental_promotion", lambda p: next(r for r in p["authority_records"] if r["id"]=="DECL-P5-01")["axes"].__setitem__("experimental_validation", "ESTABLISHED_BOUNDED_INTERNAL"), "E_AUTHORITY_PROMOTION")
    add("external_promotion", lambda p: next(r for r in p["authority_records"] if r["id"]=="EXE-GE4")["axes"].__setitem__("external_primary_literature_validation", "ESTABLISHED_BOUNDED_JCP147_REF6_METHOD_ONLY"), "E_AUTHORITY_PROMOTION")
    add("picard_general", lambda p: next(r for r in p["authority_records"] if r["id"]=="EXE-GE3").__setitem__("limitation", "Exact general solution."), "E_PICARD_AUTHORITY")
    add("transfer_time", lambda p: next(r for r in p["authority_records"] if r["id"]=="EXE-GE4").__setitem__("limitation", "Validated time response."), "E_TRANSFER_AUTHORITY")
    add("ref7_false_present", lambda p: p["literature_boundary"].__setitem__("ref7_original", "FULL_TEXT_READ"), "E_REF7_GNF")
    add("ref6_identity", lambda p: p["literature_boundary"].__setitem__("ref6_original", "UNBOUND"), "E_REF6_IDENTITY")
    add("jcp147_as_ref7_substitute", lambda p: p["literature_boundary"].__setitem__("ref7_original", "JCP147_AS_SUBSTITUTE"), "E_JCP_SUBSTITUTE")
    add("ref7_wrong_doi", lambda p: p["literature_boundary"].__setitem__("ref7_bibliography", "OFFICIAL_METADATA_DOI_10.1063/1.4802005"), "E_REF7_DOI")
    add("reference_ledger_conflation", lambda p: p["non_double_count"].__setitem__("reference_ledger_vs_adopted_bibliography", "CONFLATED"), "E_REFERENCE_LEDGER_CONFLATION")
    add("empty_owner", lambda p: p["overclaim_routes"][0].__setitem__("owner", ""), "E_ROUTE_OWNER_CARDINALITY")
    add("multiple_owner", lambda p: p["overclaim_routes"][0].__setitem__("owner", "Phase 083/Phase 076"), "E_ROUTE_OWNER_CARDINALITY")
    add("wrong_owner", lambda p: p["overclaim_routes"][0].__setitem__("owner", "Phase 071"), "E_ROUTE_OWNER_REGISTRY")
    add("duplicate_route", lambda p: p["overclaim_routes"][1].__setitem__("id", "AUTH-001"), "E_ROUTE_BIJECTION")
    add("missing_acceptance", lambda p: p["overclaim_routes"][0].__setitem__("acceptance_criterion", ""), "E_ROUTE_ACCEPTANCE")
    add("factor_3600_inversion", lambda p: next(r for r in p["overclaim_routes"] if r["id"]=="AUTH-006").__setitem__("disposition", "ACCEPTED"), "E_FACTOR_3600_BINDING")
    add("positive_speedup_without_benchmark", lambda p: next(r for r in p["overclaim_routes"] if r["id"]=="AUTH-014").__setitem__("disposition", "ESTABLISHED"), "E_COMPUTATIONAL_BENEFIT_BINDING")
    add("source_path", lambda p: p["source_contracts"][0].__setitem__("path", p["source_contracts"][1]["path"]), "E_SOURCE_IDENTITY")
    add("source_blob", lambda p: p["source_contracts"][0].__setitem__("git_blob", "0"*40), "E_SOURCE_IDENTITY")
    add("source_bytes", lambda p: p["source_contracts"][0].__setitem__("bytes", p["source_contracts"][0]["bytes"]-1), "E_SOURCE_IDENTITY")
    add("source_lines", lambda p: p["source_contracts"][0].__setitem__("lines", p["source_contracts"][0]["lines"]-1), "E_SOURCE_IDENTITY")
    add("source_extent", lambda p: p["source_contracts"][0].__setitem__("read_coverage", [1, p["source_contracts"][0]["lines"]-1]), "E_SOURCE_IDENTITY")
    add("source_span", lambda p: p["source_contracts"][0]["source_spans"][0].__setitem__("start", 2), "E_SOURCE_SPAN")
    add("gate_anchor", lambda p: p["authority_records"][0]["source"].__setitem__("start", 163), "E_GATE_ANCHOR")
    add("prior_hash", lambda p: p["prior_machine_inputs"][0].__setitem__("sha256", "0"*64), "E_PRIOR_INPUT")
    add("doc_hash", lambda p: p["document_contracts"][0].__setitem__("sha256", "0"*64), "E_DOCUMENT_IDENTITY")
    add("result_status_conflict", lambda p: p["document_contracts"][0].__setitem__("sha256", "1"*64), "E_DOCUMENT_IDENTITY")
    add("parent_ledger_parent_conflict", lambda p: p["document_contracts"][1].__setitem__("sha256", "2"*64), "E_DOCUMENT_IDENTITY")
    add("active_ledger_subject_conflict", lambda p: p["document_contracts"][2].__setitem__("sha256", "3"*64), "E_DOCUMENT_IDENTITY")
    add("handover_persistence_conflict", lambda p: p["document_contracts"][3].__setitem__("sha256", "4"*64), "E_DOCUMENT_IDENTITY")
    add("manifest_identity", lambda p: p["high_risk_bindings"].__setitem__("step64_manifest_header_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("manifest_path_omission", lambda p: p["high_risk_bindings"].__setitem__("step64_manifest_path_projection_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("manifest_blob_omission", lambda p: p["high_risk_bindings"].__setitem__("step64_manifest_blob_projection_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("manifest_extent_omission", lambda p: p["high_risk_bindings"].__setitem__("step64_manifest_extent_projection_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("manifest_page_omission", lambda p: p["high_risk_bindings"].__setitem__("step64_pdf_page_projection_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("manifest_line_omission", lambda p: p["high_risk_bindings"].__setitem__("step64_text_line_projection_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("manifest_read_attestation_omission", lambda p: p["high_risk_bindings"].__setitem__("step64_read_attestation_sources_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    for equation in ("32", "33", "34", "37", "39"):
        add(f"equation_{equation}_anchor", lambda p, eq=equation: p["high_risk_bindings"]["step65_equation_row_sha256"].__setitem__(eq, "0"*64), "E_HIGH_RISK_BINDING")
    add("jcp_applicability_omission", lambda p: p["high_risk_bindings"].__setitem__("step65_applicability_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("fredholm_volterra_class_swap", lambda p: p["high_risk_bindings"].__setitem__("step67_problem_classes_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("algebraic_root_kernel_promotion", lambda p: p["high_risk_bindings"].__setitem__("step67_problem_classes_sha256", "1"*64), "E_HIGH_RISK_BINDING")
    add("interaction_double_count", lambda p: p["high_risk_bindings"].__setitem__("step67_non_double_count_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("timebase_binding", lambda p: p["high_risk_bindings"].__setitem__("step66_timebase_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("benchmark_binding", lambda p: p["high_risk_bindings"].__setitem__("step66_benchmark_sha256", "0"*64), "E_HIGH_RISK_BINDING")
    add("human", lambda p: p["human_evidence"].__setitem__("material_validated_gates", 1), "E_HUMAN_EVIDENCE")
    add("summary_promotion", lambda p: p["authority_summary"].__setitem__("material_validation", True), "E_AUTHORITY_PROMOTION")
    add("count_float", lambda p: p["counts"].__setitem__("complete_authority_records", 47.0), "E_JSON_TYPE_PROJECTION")
    add("count_bool", lambda p: p["counts"].__setitem__("complete_authority_records", True), "E_JSON_TYPE_PROJECTION")
    add("nested_prior_scalar", lambda p: p["prior_machine_inputs"].__setitem__(0, 0), "E_NESTED_KEYS")
    add("nested_source_scalar", lambda p: p["source_contracts"].__setitem__(0, 0), "E_NESTED_KEYS")
    add("nested_document_scalar", lambda p: p["document_contracts"].__setitem__(0, 0), "E_NESTED_KEYS")
    add("nested_route_scalar", lambda p: p["overclaim_routes"].__setitem__(0, 0), "E_NESTED_KEYS")
    add("nested_span_scalar", lambda p: p["source_contracts"][0]["source_spans"].__setitem__(0, 0), "E_NESTED_KEYS")
    add("nested_supplemental_scalar", lambda p: p["supplemental_evidence"].__setitem__(0, 0), "E_NESTED_KEYS")
    add("nested_record_source_scalar", lambda p: p["authority_records"][0].__setitem__("source", 0), "E_NESTED_KEYS")
    add("nested_human_scalar", lambda p: p.__setitem__("human_evidence", 0), "E_NESTED_KEYS")
    add("nested_high_risk_scalar", lambda p: p.__setitem__("high_risk_bindings", 0), "E_NESTED_KEYS")
    add("nested_non_double_scalar", lambda p: p.__setitem__("non_double_count", 0), "E_NESTED_KEYS")
    add("nested_literature_scalar", lambda p: p.__setitem__("literature_boundary", 0), "E_NESTED_KEYS")
    add("nested_authority_scalar", lambda p: p.__setitem__("authority_summary", 0), "E_NESTED_KEYS")
    add("nested_repository_scalar", lambda p: p.__setitem__("repository_boundary", 0), "E_NESTED_KEYS")
    add("root_unknown", lambda p: p.__setitem__("unknown", 1), "E_ROOT_KEYS")
    for name, mutator, expected, update_type in tests:
        changed = copy.deepcopy(payload); mutator(changed); rehash(changed, type_hash=update_type)
        got = matrix_errors(changed)
        if got != [expected]:
            raise ValidationError(f"E_NEGATIVE_DIAGNOSTIC:{name}:{got}!=[{expected}]")
    return len(tests)


def strict_json_tests() -> int:
    fixtures = [
        (b'{"a":1,"a":2}', "E_JSON_DUPLICATE"),
        (b'{"a":NaN}', "E_JSON_NONFINITE"),
        (b'{"a":Infinity}', "E_JSON_NONFINITE"),
        (b'{"a":-Infinity}', "E_JSON_NONFINITE"),
        (b'{"a":1e9999}', "E_JSON_NUMERIC_OVERFLOW"),
        (b'{"a":-1e9999}', "E_JSON_NUMERIC_OVERFLOW"),
        (b'{"a":' + b'9'*1000 + b'}', "E_JSON_HUGE_INT"),
        (b'{"a":', "E_JSON_PARSE"),
        (b'\xff', "E_JSON_PARSE"),
    ]
    for index, (raw, expected) in enumerate(fixtures):
        try: strict_load_bytes(raw, f"fixture-{index}")
        except ValidationError as exc:
            if not str(exc).startswith(expected): raise
        else: raise ValidationError(f"E_JSON_FIXTURE_ESCAPED:{index}")
    for raw in (b'[]', b'1'):
        value, _ = strict_load_bytes(raw, "root")
        if type(value) is dict: raise ValidationError("E_JSON_ROOT_FIXTURE")
    return len(fixtures)


SELF_PIN_NAMES = {
    "EXPECTED_VALIDATOR_CANONICAL_SHA256", "EXPECTED_VALIDATOR_AST_SHA256_312",
    "EXPECTED_VALIDATOR_AST_SHA256_314",
}


def canonical_validator_source(raw: bytes) -> bytes:
    text = raw.decode("utf-8", "strict")
    for name in SELF_PIN_NAMES:
        text, count = re.subn(rf'(?m)^{name} = "[^"]*"$', f'{name} = "<SELF_PIN>"', text)
        if count != 1: raise ValidationError("E_VALIDATOR_SOURCE_POLICY")
    return text.encode("utf-8")


class SelfNormalizer(ast.NodeTransformer):
    def visit_Assign(self, node: ast.Assign) -> ast.AST:
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in SELF_PIN_NAMES:
            node.value = ast.Constant(value="<SELF_PIN>")
        return self.generic_visit(node)


def canonical_validator_ast(raw: bytes) -> bytes:
    tree = ast.parse(raw.decode("utf-8", "strict"))
    tree = SelfNormalizer().visit(tree); ast.fix_missing_locations(tree)
    return ast.dump(tree, include_attributes=False, annotate_fields=True).encode("utf-8")


def validator_identity_errors(raw: bytes) -> list[str]:
    errors = []
    try:
        if sha256(canonical_validator_source(raw)) != EXPECTED_VALIDATOR_CANONICAL_SHA256: errors.append("E_VALIDATOR_SOURCE_SHA")
    except Exception:
        errors.append("E_VALIDATOR_SOURCE_POLICY")
    try:
        digest = sha256(canonical_validator_ast(raw))
        expected = EXPECTED_VALIDATOR_AST_SHA256_312 if sys.version_info[:2] == (3,12) else EXPECTED_VALIDATOR_AST_SHA256_314 if sys.version_info[:2] == (3,14) else None
        if expected is None or digest != expected: errors.append("E_VALIDATOR_AST_SHA")
    except (SyntaxError, UnicodeDecodeError):
        errors.append("E_VALIDATOR_SYNTAX")
    return sorted(set(errors))


def validator_self_tests() -> int:
    raw = pathlib.Path(__file__).read_bytes()
    if validator_identity_errors(raw): raise ValidationError(f"E_VALIDATOR_SELF_BASE:{validator_identity_errors(raw)}")
    fixtures = [
        (raw + b"# appended\n", ["E_VALIDATOR_SOURCE_SHA"]),
        (raw.replace(b'GATE = "PASS_P064_STEP68_AUTHORITY"', b'GATE = "FAIL"', 1), ["E_VALIDATOR_AST_SHA", "E_VALIDATOR_SOURCE_SHA"]),
        (raw + b"\nif (:\n", ["E_VALIDATOR_SOURCE_SHA", "E_VALIDATOR_SYNTAX"]),
    ]
    for mutated, expected in fixtures:
        got = validator_identity_errors(mutated)
        if got != expected: raise ValidationError(f"E_VALIDATOR_SELF_FIXTURE:{got}!={expected}")
    return len(fixtures)


def builder_policy() -> None:
    raw = BUILDER.read_bytes(); text = raw.decode("utf-8", "strict")
    if git_text("hash-object", BUILDER.relative_to(ROOT).as_posix()) != EXPECTED_BUILDER_GIT_BLOB: raise ValidationError("E_BUILDER_BLOB")
    forbidden = ("importlib", "shell=True", "eval(", "exec(", "__import__", "os.system")
    if any(token in text for token in forbidden): raise ValidationError("E_BUILDER_POLICY")
    ast.parse(text)


def builder_determinism(stored: bytes) -> tuple[int, int, int]:
    before = git(["status", "--porcelain=v1"]).stdout
    outputs: dict[str, list[bytes]] = {"3.12": [], "3.14": []}
    for runtime in outputs:
        for _ in range(2):
            cp = run(("py", f"-{runtime}", str(BUILDER)), timeout=300)
            if GATE.encode() not in cp.stdout: raise ValidationError("E_BUILDER_TERMINAL")
            outputs[runtime].append(MATRIX_PATH.read_bytes())
    if any(raw != stored for rows in outputs.values() for raw in rows): raise ValidationError("E_BUILDER_CROSS_RUN")
    if outputs["3.12"][0] != outputs["3.14"][0]: raise ValidationError("E_BUILDER_CROSS_RUNTIME")
    if git(["status", "--porcelain=v1"]).stdout != before: raise ValidationError("E_BUILDER_REPOSITORY_PROJECTION")
    return 2, 2, 1


def fixture_git(args: list[str], *, cwd: pathlib.Path, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=False)
    if check and cp.returncode: raise ValidationError(f"E_GIT_FIXTURE_COMMAND:{args}:{cp.stderr.decode('utf-8','replace')}")
    return cp


def fixture_text(repo: pathlib.Path, *args: str) -> str:
    return fixture_git(list(args), cwd=repo).stdout.decode("utf-8", "strict").strip()


def fixture_errors(repo: pathlib.Path, bare: pathlib.Path, *, base: str, active: str,
                   allowed: set[str]) -> list[str]:
    if fixture_text(repo, "rev-parse", "--abbrev-ref", "HEAD") != "active": return ["E_GIT_BRANCH"]
    if fixture_text(repo, "rev-parse", "HEAD") != active: return ["E_GIT_HEAD"]
    if fixture_text(repo, "rev-parse", "--symbolic-full-name", "@{u}") != "refs/remotes/origin/active": return ["E_GIT_UPSTREAM_SYMBOLIC"]
    if fixture_text(repo, "rev-parse", "origin/active") != active: return ["E_GIT_TRACKING"]
    if fixture_text(bare, "rev-parse", "refs/heads/active") != active: return ["E_GIT_LIVE"]
    if fixture_text(repo, "rev-parse", "protected") != base or fixture_text(repo, "rev-parse", "origin/protected") != base or fixture_text(bare, "rev-parse", "refs/heads/protected") != base: return ["E_GIT_PROTECTED"]
    if fixture_text(repo, "rev-parse", "origin/main") != base or fixture_text(bare, "rev-parse", "refs/heads/main") != base: return ["E_GIT_MAIN"]
    if fixture_text(repo, "rev-parse", f"{base}:Claude") != fixture_text(repo, "rev-parse", "HEAD:Claude") or fixture_text(repo, "diff", "--", "Claude") or fixture_text(repo, "status", "--porcelain=v1", "--", "Claude"): return ["E_GIT_CLAUDE"]
    staged = set(filter(None, fixture_text(repo, "diff", "--cached", "--name-only").splitlines()))
    if staged != allowed: return ["E_GIT_STAGED_SET"]
    if fixture_text(repo, "diff", "--name-only"): return ["E_GIT_UNSTAGED"]
    if fixture_text(repo, "ls-files", "--others", "--exclude-standard"): return ["E_GIT_UNTRACKED"]
    for path in allowed:
        if fixture_git(["show", f":{path}"], cwd=repo).stdout != (repo / path).read_bytes(): return ["E_GIT_INDEX_WORKTREE_BYTES"]
    if fixture_git(["diff", "--check", "--cached"], cwd=repo, check=False).returncode: return ["E_GIT_DIFF_CHECK"]
    return []


def disposable_git_fixtures() -> int:
    cases = [
        ("branch", "E_GIT_BRANCH"), ("head", "E_GIT_HEAD"),
        ("upstream_symbolic", "E_GIT_UPSTREAM_SYMBOLIC"), ("tracking", "E_GIT_TRACKING"),
        ("live", "E_GIT_LIVE"), ("protected", "E_GIT_PROTECTED"),
        ("protected_tracking", "E_GIT_PROTECTED"), ("protected_live", "E_GIT_PROTECTED"),
        ("main", "E_GIT_MAIN"), ("main_live", "E_GIT_MAIN"),
        ("claude", "E_GIT_CLAUDE"), ("claude_untracked", "E_GIT_CLAUDE"),
        ("staged", "E_GIT_STAGED_SET"), ("unstaged", "E_GIT_UNSTAGED"),
        ("untracked", "E_GIT_UNTRACKED"), ("index_worktree", "E_GIT_INDEX_WORKTREE_BYTES"),
        ("diffcheck", "E_GIT_DIFF_CHECK"),
    ]
    with tempfile.TemporaryDirectory(prefix="p064_s68_git_") as td:
        root = pathlib.Path(td); bare = root / "remote.git"; seed = root / "seed"
        fixture_git(["init", "--bare", str(bare)], cwd=root)
        fixture_git(["init", "-b", "main", str(seed)], cwd=root)
        fixture_git(["config", "user.email", "p064@example.invalid"], cwd=seed)
        fixture_git(["config", "user.name", "P064 Fixture"], cwd=seed)
        (seed / "Claude").mkdir(); (seed / "Claude/frozen.txt").write_text("frozen\n", encoding="utf-8", newline="\n")
        (seed / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
        fixture_git(["add", "Claude/frozen.txt", "seed.txt"], cwd=seed); fixture_git(["commit", "-m", "base"], cwd=seed)
        base = fixture_text(seed, "rev-parse", "HEAD")
        fixture_git(["branch", "protected", base], cwd=seed); fixture_git(["switch", "-c", "active"], cwd=seed)
        (seed / "allowed.txt").write_text("allowed\n", encoding="utf-8", newline="\n"); fixture_git(["add", "allowed.txt"], cwd=seed); fixture_git(["commit", "-m", "active"], cwd=seed)
        active = fixture_text(seed, "rev-parse", "HEAD")
        fixture_git(["branch", "alias", active], cwd=seed); fixture_git(["switch", "-c", "divergent"], cwd=seed)
        (seed / "div.txt").write_text("div\n", encoding="utf-8", newline="\n"); fixture_git(["add", "div.txt"], cwd=seed); fixture_git(["commit", "-m", "div"], cwd=seed)
        divergent = fixture_text(seed, "rev-parse", "HEAD")
        fixture_git(["remote", "add", "origin", str(bare)], cwd=seed); fixture_git(["push", "origin", "main", "protected", "active", "alias", "divergent"], cwd=seed)
        for name, expected in cases:
            repo = root / f"repo-{name}"; fixture_git(["clone", str(bare), str(repo)], cwd=root)
            fixture_git(["switch", "--track", "-c", "active", "origin/active"], cwd=repo); fixture_git(["branch", "protected", "origin/protected"], cwd=repo)
            (repo / "allowed.txt").write_text("allowed staged\n", encoding="utf-8", newline="\n"); fixture_git(["add", "allowed.txt"], cwd=repo)
            if name == "branch": fixture_git(["switch", "-f", "main"], cwd=repo)
            elif name == "head": fixture_git(["update-ref", "refs/heads/active", divergent], cwd=repo)
            elif name == "upstream_symbolic": fixture_git(["branch", "--set-upstream-to=origin/alias", "active"], cwd=repo)
            elif name == "tracking": fixture_git(["update-ref", "refs/remotes/origin/active", divergent], cwd=repo)
            elif name == "live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/active", divergent], cwd=repo)
            elif name == "protected": fixture_git(["update-ref", "refs/heads/protected", divergent], cwd=repo)
            elif name == "protected_tracking": fixture_git(["update-ref", "refs/remotes/origin/protected", divergent], cwd=repo)
            elif name == "protected_live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/protected", divergent], cwd=repo)
            elif name == "main": fixture_git(["update-ref", "refs/remotes/origin/main", divergent], cwd=repo)
            elif name == "main_live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/main", divergent], cwd=repo)
            elif name == "claude": (repo / "Claude/frozen.txt").write_text("changed\n", encoding="utf-8", newline="\n")
            elif name == "claude_untracked": (repo / "Claude/new.txt").write_text("new\n", encoding="utf-8", newline="\n")
            elif name == "staged": (repo / "extra.txt").write_text("extra\n", encoding="utf-8", newline="\n"); fixture_git(["add", "extra.txt"], cwd=repo)
            elif name == "unstaged": (repo / "seed.txt").write_text("unstaged\n", encoding="utf-8", newline="\n")
            elif name == "untracked": (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8", newline="\n")
            elif name == "index_worktree": fixture_git(["update-index", "--assume-unchanged", "allowed.txt"], cwd=repo); (repo / "allowed.txt").write_text("different worktree\n", encoding="utf-8", newline="\n")
            elif name == "diffcheck": (repo / "allowed.txt").write_text("bad space \n", encoding="utf-8", newline="\n"); fixture_git(["add", "allowed.txt"], cwd=repo)
            got = fixture_errors(repo, bare, base=base, active=active, allowed={"allowed.txt"})
            if got != [expected]: raise ValidationError(f"E_GIT_FIXTURE:{name}:{got}!=[{expected}]")
            if name == "live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/active", active], cwd=repo)
            elif name == "protected_live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/protected", base], cwd=repo)
            elif name == "main_live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/main", base], cwd=repo)
        return len(cases) + disposable_persistence_fixtures(root, bare, active, divergent)


def fixture_persistence_errors(repo: pathlib.Path, bare: pathlib.Path, *, expected_parent: str,
                               head: str, allowed: set[str]) -> list[str]:
    if fixture_text(repo, "rev-parse", "HEAD^") != expected_parent: return ["E_GIT_PARENT"]
    if fixture_text(repo, "show", "-s", "--format=%s", "HEAD") != EXPECTED_SUBJECT: return ["E_GIT_SUBJECT"]
    committed = set(filter(None, fixture_text(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines()))
    if committed != allowed: return ["E_GIT_COMMIT_SET"]
    if fixture_text(repo, "rev-parse", "@{u}") != head or fixture_text(repo, "rev-parse", "origin/active") != head or fixture_text(bare, "rev-parse", "refs/heads/active") != head: return ["E_GIT_PERSISTENCE"]
    if fixture_text(repo, "status", "--porcelain=v1"): return ["E_GIT_DIRTY"]
    for path in allowed:
        if fixture_git(["show", f"{head}:{path}"], cwd=repo).stdout != (repo / path).read_bytes(): return ["E_GIT_COMMIT_WORKTREE_BYTES"]
    if fixture_git(["show", "--check", "--oneline", "HEAD"], cwd=repo, check=False).returncode: return ["E_GIT_DIFF_CHECK"]
    return []


def disposable_persistence_fixtures(root: pathlib.Path, bare: pathlib.Path,
                                    active: str, divergent: str) -> int:
    cases = [
        ("parent", "E_GIT_PARENT"), ("subject", "E_GIT_SUBJECT"),
        ("commit_set", "E_GIT_COMMIT_SET"), ("tracking", "E_GIT_PERSISTENCE"),
        ("live", "E_GIT_PERSISTENCE"), ("dirty", "E_GIT_DIRTY"),
        ("worktree", "E_GIT_COMMIT_WORKTREE_BYTES"), ("diffcheck", "E_GIT_DIFF_CHECK"),
    ]
    for name, expected in cases:
        repo = root / f"persist-{name}"; fixture_git(["clone", str(bare), str(repo)], cwd=root)
        fixture_git(["switch", "--track", "-c", "active", "origin/active"], cwd=repo)
        fixture_git(["config", "user.email", "p064@example.invalid"], cwd=repo)
        fixture_git(["config", "user.name", "P064 Fixture"], cwd=repo)
        case_parent = fixture_text(repo, "rev-parse", "HEAD")
        if name == "parent":
            (repo / "seed.txt").write_text("intermediate\n", encoding="utf-8", newline="\n")
            fixture_git(["add", "seed.txt"], cwd=repo); fixture_git(["commit", "-m", "intermediate"], cwd=repo)
        content = "bad space \n" if name == "diffcheck" else f"persisted {name}\n"
        (repo / "allowed.txt").write_text(content, encoding="utf-8", newline="\n"); fixture_git(["add", "allowed.txt"], cwd=repo)
        if name == "commit_set":
            (repo / "extra.txt").write_text("extra\n", encoding="utf-8", newline="\n"); fixture_git(["add", "extra.txt"], cwd=repo)
        subject = "wrong subject" if name == "subject" else EXPECTED_SUBJECT
        fixture_git(["commit", "-m", subject], cwd=repo); fixture_git(["push", "origin", "active"], cwd=repo)
        head = fixture_text(repo, "rev-parse", "HEAD")
        if name == "tracking": fixture_git(["update-ref", "refs/remotes/origin/active", divergent], cwd=repo)
        elif name == "live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/active", divergent], cwd=repo)
        elif name == "dirty": (repo / "seed.txt").write_text("dirty\n", encoding="utf-8", newline="\n")
        elif name == "worktree": fixture_git(["update-index", "--assume-unchanged", "allowed.txt"], cwd=repo); (repo / "allowed.txt").write_text("different worktree\n", encoding="utf-8", newline="\n")
        got = fixture_persistence_errors(repo, bare, expected_parent=case_parent, head=head, allowed={"allowed.txt"})
        if got != [expected]: raise ValidationError(f"E_GIT_PERSISTENCE_FIXTURE:{name}:{got}!=[{expected}]")
        if name == "live": fixture_git(["--git-dir", str(bare), "update-ref", "refs/heads/active", head], cwd=repo)
    return len(cases)


def live_tip(branch: str) -> str:
    out = git(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"]).stdout.decode("utf-8", "strict").strip()
    parts = out.split()
    if len(parts) != 2: raise ValidationError("E_GIT_LIVE")
    return parts[0]


def validate_git_mode(mode: str) -> None:
    if mode == "artifact": return
    branch = git_text("rev-parse", "--abbrev-ref", "HEAD")
    if branch != ACTIVE_BRANCH: raise ValidationError("E_GIT_BRANCH")
    upstream_symbolic = git_text("rev-parse", "--symbolic-full-name", "@{u}")
    if upstream_symbolic != f"refs/remotes/origin/{ACTIVE_BRANCH}": raise ValidationError("E_GIT_UPSTREAM_SYMBOLIC")
    if git_text("rev-parse", PROTECTED_BRANCH) != PROTECTED_TIP or git_text("rev-parse", f"origin/{PROTECTED_BRANCH}") != PROTECTED_TIP or live_tip(PROTECTED_BRANCH) != PROTECTED_TIP: raise ValidationError("E_GIT_PROTECTED")
    if git_text("rev-parse", "origin/main") != MAIN_TIP or live_tip("main") != MAIN_TIP: raise ValidationError("E_GIT_MAIN")
    if git_text("rev-parse", f"{BASELINE}:Claude") != git_text("rev-parse", "HEAD:Claude") or git_text("diff", "--", "Claude") or git_text("status", "--porcelain=v1", "--", "Claude"): raise ValidationError("E_GIT_CLAUDE")
    if mode == "precommit":
        if git_text("rev-parse", "HEAD") != EXPECTED_PARENT: raise ValidationError("E_GIT_HEAD")
        if git_text("rev-parse", f"origin/{ACTIVE_BRANCH}") != EXPECTED_PARENT or live_tip(ACTIVE_BRANCH) != EXPECTED_PARENT: raise ValidationError("E_GIT_REMOTE_PARENT")
        staged = set(filter(None, git_text("diff", "--cached", "--name-only").splitlines()))
        if staged != EXACT_SET: raise ValidationError("E_GIT_STAGED_SET")
        if git_text("diff", "--name-only"): raise ValidationError("E_GIT_UNSTAGED")
        if git_text("ls-files", "--others", "--exclude-standard"): raise ValidationError("E_GIT_UNTRACKED")
        for path in EXACT_PATHS:
            if git(["show", f":{path}"]).stdout != (ROOT / path).read_bytes(): raise ValidationError("E_GIT_INDEX_WORKTREE_BYTES")
        if git(["diff", "--check", "--cached"], check=False).returncode: raise ValidationError("E_GIT_DIFF_CHECK")
        return
    if mode != "persistence": raise ValidationError("E_MODE")
    head = git_text("rev-parse", "HEAD")
    if git_text("rev-parse", "HEAD^") != EXPECTED_PARENT: raise ValidationError("E_GIT_PARENT")
    if git_text("show", "-s", "--format=%s", "HEAD") != EXPECTED_SUBJECT: raise ValidationError("E_GIT_SUBJECT")
    committed = set(filter(None, git_text("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines()))
    if committed != EXACT_SET: raise ValidationError("E_GIT_COMMIT_SET")
    if git_text("rev-parse", "@{u}") != head or git_text("rev-parse", f"origin/{ACTIVE_BRANCH}") != head or live_tip(ACTIVE_BRANCH) != head: raise ValidationError("E_GIT_PERSISTENCE")
    if git_text("status", "--porcelain=v1"): raise ValidationError("E_GIT_DIRTY")
    for path in EXACT_PATHS:
        if git_bytes(head, path) != (ROOT / path).read_bytes(): raise ValidationError("E_GIT_COMMIT_WORKTREE_BYTES")
    if git(["show", "--check", "--oneline", "HEAD"], check=False).returncode: raise ValidationError("E_GIT_DIFF_CHECK")


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="artifact")
    args = parser.parse_args()
    payload, nodes, raw = strict_load(MATRIX_PATH)
    errors = matrix_errors(payload)
    if errors: raise ValidationError(":".join(errors))
    builder_policy()
    self_count = validator_self_tests()
    negative = mutation_tests(payload)
    strict = strict_json_tests()
    git_fixtures = disposable_git_fixtures()
    deterministic = (0, 0, 0) if args.mode == "persistence" else builder_determinism(raw)
    validate_git_mode(args.mode)
    print(f"PASS_P064_STEP68_NEGATIVE {negative}/{negative} strict_json={strict}/{strict}")
    print("PASS_P064_STEP68_OWNER_BIJECTION routes=14/14 open=14/14")
    print(f"PASS_P064_STEP68_GIT_FIXTURES {git_fixtures}/{git_fixtures}")
    print(f"PASS_P064_STEP68_VALIDATOR_SELF {self_count}/{self_count}")
    print(f"PASS_P064_STEP68_TRAVERSAL artifact={nodes} sources={len(payload['source_contracts'])}/{len(EXPECTED_SOURCE_SPECS)} core=37/37 complete=47/47")
    if args.mode != "persistence": print(f"PASS_P064_STEP68_DETERMINISM py312={deterministic[0]}/2 py314={deterministic[1]}/2 cross_runtime={deterministic[2]}/1")
    print(PERSISTENCE if args.mode == "persistence" else GATE)


if __name__ == "__main__":
    main()
