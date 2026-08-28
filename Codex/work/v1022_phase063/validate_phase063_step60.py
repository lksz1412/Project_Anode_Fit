#!/usr/bin/env python3
"""Validate Phase 063 Step 60 literature, quantity, and scope authority."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1022_phase063/build_phase063_step60_literature_scope.py"
VALIDATOR = Path(__file__).resolve()
ARTIFACT = REPO / "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_060_LITERATURE_SCOPE_RESULT.md"
TOPOLOGY = REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
STEP59 = REPO / "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json"
PRIOR_SCOPE = REPO / "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "07a0f3ead16a072550919b86d1d41580682fd92d"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase063): bound v1022 literature scope"
GATE = "PASS_P063_STEP60_LITERATURE_SCOPE_WITH_CONCERNS"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EVIDENCE_BEGIN = "<!-- P063_STEP60_LITERATURE_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P063_STEP60_LITERATURE_EVIDENCE_END -->"
TIMEOUT = 300

EXACT_SEVEN = (
    "Codex/work/v1022_phase063/build_phase063_step60_literature_scope.py",
    "Codex/work/v1022_phase063/validate_phase063_step60.py",
    "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json",
    "Codex/results/PHASE_063_STEP_060_LITERATURE_SCOPE_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_SEVEN_SET = set(EXACT_SEVEN)

# Filled after the result, both ledgers, and handover reach final precommit
# raw LF-only bytes. The validator is excluded to avoid a self-referential digest.
CONTROL_SHA256: dict[str, str] = {
    "result": "a8d589821dade9e0e0bb3abbfb5c08d16908be1597d39e3230760cbb7a86c0c1",
    "active_ledger": "e4660280388af7d5d4b75cd1e3d8f630ddd6110ed45c58a0eff0d326e2605d4d",
    "parent_ledger": "9f66ba749f8b6856608b3d5be761e01398c6c363ac6792c2e0a165be3663fbc6",
    "handover": "49035a403b5a4f2579992d2d580cadc6d4413622c2a2fa90d668c62963ec2b95",
}

EXPECTED_COUNTS: dict[str, Any] = {
    "all_physical_lines": 30318,
    "all_reviewed_text_sources": 201,
    "bibliography_occurrences": 91,
    "manual_unkeyed_bibliography_occurrences": 5,
    "all_bibliography_record_occurrences": 96,
    "bibliography_partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 2,
        "FINAL_RELEASE_SURFACE": 88,
        "STATUS_MACHINE_PROCESS": 1,
    },
    "bibliography_unique_keys": 88,
    "citation_commands": 641,
    "citation_key_occurrences": 770,
    "citation_partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 487,
        "FINAL_RELEASE_SURFACE": 278,
        "STATUS_MACHINE_PROCESS": 5,
    },
    "claim_candidate_kind_memberships": {
        "BIBLIOGRAPHY_RECORD": 91,
        "CITATION": 580,
        "DOI_METADATA": 307,
        "MATERIAL_SCOPE": 2309,
        "NUMERIC_QUANTITY": 7268,
    },
    "claim_candidate_lines": 8751,
    "doi_occurrences": 328,
    "doi_partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 220,
        "FINAL_RELEASE_SURFACE": 84,
        "STATUS_MACHINE_PROCESS": 24,
    },
    "doi_unique_normalized": 128,
    "equation_candidates": 339,
    "equation_partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 107,
        "FINAL_RELEASE_SURFACE": 231,
        "STATUS_MACHINE_PROCESS": 1,
    },
    "tex_delimited_math_candidates": 14958,
    "tex_delimited_math_partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 8691,
        "FINAL_RELEASE_SURFACE": 6115,
        "STATUS_MACHINE_PROCESS": 139,
        "SUPPLEMENTAL_PROCESS_CONTROL": 9,
        "VERSION_PLAN": 4,
    },
    "findings": 26,
    "manifest_physical_lines": 30219,
    "manifest_text_sources": 200,
    "manual_literature_claims": 12,
    "manual_material_scope_rows": 12,
    "source_partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 125,
        "FINAL_RELEASE_SURFACE": 59,
        "STATUS_MACHINE_PROCESS": 10,
        "SUPPLEMENTAL_PROCESS_CONTROL": 1,
        "VERSION_PLAN": 6,
    },
    "supplemental_physical_lines": 99,
    "supplemental_text_sources": 1,
}

FALSE_AUTHORITY_FLAGS = {
    "frozen_source_modified",
    "network_contacted_by_builder",
    "bibliographic_existence_externally_validated",
    "fulltext_method_validated",
    "exact_equation_externally_validated",
    "exact_quantity_basis_externally_validated",
    "material_protocol_externally_validated",
    "model_mapping_externally_validated",
    "external_experimental_truth_validated",
    "primary_literature_truth_validated",
    "canonical_equation_accepted",
    "final_manuscript_ready",
}
LITERATURE_IDS = {f"P063-S60-LIT-{number:03d}" for number in range(1, 13)}
MATERIAL_IDS = {f"P063-S60-MAT-{number:03d}" for number in range(1, 13)}
FINDING_IDS = {f"P063-S60-F{number:03d}" for number in range(1, 27)}
MANUAL_REFERENCE_IDS = {f"P063-S60-MANREF-{number:05d}" for number in range(1, 6)}
AUTHORITY_AXIS_KEYS = {
    "bibliographic_existence",
    "fulltext_method",
    "exact_equation",
    "exact_value_unit_basis",
    "sample_material_composition_protocol",
    "current_model_mapping",
    "external_experimental_support",
}
LEXICAL_AUTHORITY_PROFILE_ID = "P063-AXIS-LEXICAL-UNVERIFIED"
LEXICAL_AUTHORITY_PROFILE = {
    "bibliographic_existence": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "fulltext_method": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "exact_equation": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "exact_value_unit_basis": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "sample_material_composition_protocol": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "current_model_mapping": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "external_experimental_support": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
}
PARTITION_CEILING = {
    "FINAL_RELEASE_SURFACE": "FROZEN_RELEASE_ASSERTION_OCCURRENCE_ONLY",
    "VERSION_PLAN": "PROCESS_INTENT_ONLY",
    "STATUS_MACHINE_PROCESS": "SELF_REPORT_OR_MACHINE_STRUCTURE_ONLY",
    "COMPETING_REVIEW_CANDIDATE": "PROPOSAL_REVIEW_CANDIDATE_ONLY",
    "SUPPLEMENTAL_PROCESS_CONTROL": "PROCESS_CONTROL_REPOSITORY_REPORTED_ONLY",
}
EXPECTED_INVENTORY_SUMMARY = {
    "manifest_sources": 204,
    "manifest_full_text": 200,
    "manifest_full_pdf": 4,
    "supplemental_process_control": 1,
    "all_reviewed_text_sources": 201,
    "all_reviewed_text_physical_lines": 30318,
    "final_root_citation_commands": 210,
    "final_root_citation_key_occurrences": 258,
    "final_root_routes": 88,
    "final_keyed_bibliography_definitions": 88,
    "final_unique_bibliography_keys": 87,
    "manual_unkeyed_references": 5,
    "final_doi_occurrences": 84,
    "final_unique_normalized_dois": 80,
    "process_candidate_supplemental_citation_commands": 414,
    "process_candidate_supplemental_citation_key_occurrences": 492,
    "process_candidate_supplemental_doi_occurrences": 244,
    "process_candidate_supplemental_unique_normalized_dois": 107,
    "all_text_display_equation_candidates": 339,
    "all_text_tex_delimited_math_candidates": 14958,
    "all_text_claim_candidate_lines": 8751,
}

DOI_RE = re.compile(r"(?i)(?<![A-Za-z0-9])10\.\d{4,9}/[-._;()/:A-Z0-9]+")
CITE_RE = re.compile(
    r"\\(?P<command>cite[a-zA-Z*]*)\s*(?:\[[^\]]*\]\s*){0,2}\{(?P<keys>[^{}]+)\}",
    re.MULTILINE,
)
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^{}]+)\}")
NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
UNIT_RE = re.compile(
    r"(?i)(?:mAh\s*/\s*g|Ah\s*/\s*g|mV\s*/\s*(?:K|GPa)|"
    r"(?:J|kJ)\s*/\s*\(?mol(?:\\,|\s)*K\)?|(?:micro|\\mu|μ)\s*V\s*/\s*K|"
    r"(?:mV|V|eV|K|GPa|MPa|Pa|nm|\\mu m|μm|cm\^?\{?2\}?/s|s\^?\{-?1\}?|h\^?\{-?1\}?|wt\\?%|\\?%))"
)
MATERIAL_RE = re.compile(
    r"(?i)(?:graphite|LiC_?\{?6\}?|LiCoO|LCO|cobalt oxide|silicon|"
    r"SiO(?:_?\{?x\}?)?|Si--C|Si-C|Si/graphite|graphite.?Si|"
    r"Li_?\{?15\}?Si_?\{?4\}?|dop(?:ed|ant|ing)|oxygen redox|charge.?order)"
)
DISPLAY_ENVS = ("equation", "align", "gather", "multline", "flalign", "alignat")
DISPLAY_BEGIN_RE = re.compile(
    r"\\begin\{(?P<environment>"
    + "|".join(
        re.escape(environment)
        for base in DISPLAY_ENVS
        for environment in (base, base + "*")
    )
    + r")\}"
)


class ValidationError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise ValidationError(f"non-finite JSON constant: {value}")


def strict_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValidationError(f"non-finite JSON float: {value}")
    return result


def strict_pairs(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def traverse(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(1 + traverse(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(traverse(item) for item in value)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError("non-finite value in traversal")
    return 1


def strict_load_text(text: str) -> tuple[Any, int]:
    value = json.loads(
        text, object_pairs_hook=strict_pairs, parse_constant=reject_constant,
        parse_float=strict_float,
    )
    return value, traverse(value)


def strict_load(path: Path) -> tuple[Any, int]:
    return strict_load_text(path.read_text(encoding="utf-8"))


def normalized_bytes(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8", "strict")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def lf_only(path: Path) -> bool:
    return b"\r" not in path.read_bytes()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def semantic_projection(data: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(data)
    projected.pop("semantic_sha256", None)
    return projected


def evidence_block() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise ValidationError("result evidence marker cardinality")
    block = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise ValidationError("result evidence fence")
    value, _ = strict_load_text(block[len("```json\n"):-len("\n```")])
    if not isinstance(value, dict):
        raise ValidationError("result evidence root")
    return value, digest(compact(value))


def run(args: list[str], timeout: int = TIMEOUT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=timeout, check=False,
    )


def git_bytes(*args: str, check: bool = True) -> bytes:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise ValidationError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def git_text(*args: str, check: bool = True) -> str:
    return git_bytes(*args, check=check).decode("utf-8", "strict").strip()


def git_paths(*args: str) -> set[str]:
    return {
        item.decode("utf-8", "strict").replace("\\", "/")
        for item in git_bytes(*args).split(b"\0") if item
    }


def ref_hash(ref: str) -> str | None:
    value = git_text("show-ref", "--verify", "--hash", ref, check=False)
    return value or None


def remote_head(branch: str) -> str:
    ref = f"refs/heads/{branch}"
    rows = [
        line.split() for line in
        git_text("ls-remote", "--heads", "origin", ref).splitlines()
        if line.strip()
    ]
    if len(rows) != 1 or rows[0][1] != ref:
        raise ValidationError(f"remote head cardinality: {branch}: {rows}")
    return rows[0][0]


def add(errors: set[str], condition: bool, code: str) -> None:
    if condition:
        errors.add(code)


def sequential_ids(rows: Any, key: str, prefix: str) -> bool:
    return (
        isinstance(rows, list)
        and all(isinstance(row, dict) for row in rows)
        and [row.get(key) for row in rows]
        == [f"{prefix}{number:05d}" for number in range(1, len(rows) + 1)]
    )


def input_artifact_diagnostics(value: Any) -> bool:
    expected = {
        "step58_topology": (TOPOLOGY, "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY"),
        "step59_rederivation": (STEP59, "PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS"),
        "phase062_material_scope": (PRIOR_SCOPE, "PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS"),
    }
    if not isinstance(value, dict) or set(value) != set(expected):
        return True
    for key, (path, gate) in expected.items():
        record = value.get(key)
        stored, _ = strict_load(path)
        if not isinstance(record, dict) or not isinstance(stored, dict):
            return True
        expected_record = {
            "path": path.relative_to(REPO).as_posix(),
            "raw_sha256": digest(path.read_bytes()),
            "semantic_sha256": stored.get("semantic_sha256"),
            "gate": gate,
            "authority_ceiling": "PRIOR_INTERNAL_AUDIT_ROUTE_ONLY",
        }
        if record != expected_record or stored.get("gate") != gate:
            return True
    return False


def row_contract_errors(
    literature: Any, materials: Any, findings: Any, manual_reference_ids: set[str],
) -> set[str]:
    errors: set[str] = set()
    if not all(isinstance(rows, list) for rows in (literature, materials, findings)):
        return {"ROW_SCHEMA"}
    required_lit = {
        "claim_id", "family", "source_evidence", "current_state", "axis_states",
        "disposition", "owner", "acceptance", "external_truth_promoted",
    }
    required_mat = {
        "material_id", "material", "scope", "source_evidence", "quantity_basis",
        "state", "axis_states", "forbidden_join", "owner", "external_truth_promoted",
    }
    required_finding = {
        "finding_id", "priority", "summary", "status", "evidence_refs",
        "disposition", "downstream_owner", "external_truth_promoted",
    }
    for row in literature:
        if set(row) != required_lit or not row.get("family") or not row.get("source_evidence") \
                or not row.get("current_state") or not row.get("disposition") \
                or not row.get("owner") or not row.get("acceptance"):
            errors.add("LITERATURE_SCHEMA")
        if not isinstance(row.get("axis_states"), dict) or set(row["axis_states"]) != AUTHORITY_AXIS_KEYS \
                or any(not value for value in row["axis_states"].values()):
            errors.add("LITERATURE_AXES")
    for row in materials:
        if set(row) != required_mat or not row.get("material") or not row.get("scope") \
                or not row.get("source_evidence") or not row.get("quantity_basis") \
                or not row.get("state") or not row.get("forbidden_join") or not row.get("owner"):
            errors.add("MATERIAL_SCHEMA")
        if not isinstance(row.get("axis_states"), dict) or set(row["axis_states"]) != AUTHORITY_AXIS_KEYS \
                or any(not value for value in row["axis_states"].values()):
            errors.add("MATERIAL_AXES")
    valid_refs = LITERATURE_IDS | MATERIAL_IDS | manual_reference_ids
    for row in findings:
        refs = row.get("evidence_refs")
        if set(row) != required_finding or not row.get("summary") or not row.get("status") \
                or not isinstance(refs, list) or not refs or not row.get("disposition") \
                or not row.get("downstream_owner"):
            errors.add("FINDING_SCHEMA")
        elif not set(refs) <= valid_refs:
            errors.add("FINDING_REFS")
    return errors


def artifact_diagnostics(data: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    add(errors, data.get("schema_version") != 1, "SCHEMA")
    add(errors, data.get("artifact_kind") != "V1022_LITERATURE_QUANTITY_SCOPE_AUTHORITY", "KIND")
    add(errors, data.get("phase") != 63 or data.get("step") != 60, "STEP")
    add(errors, data.get("status") != "PASS_WITH_CONCERNS", "STATUS")
    add(errors, data.get("gate") != GATE, "GATE")
    add(errors, data.get("baseline_commit") != BASELINE, "BASELINE")
    add(errors, data.get("expected_parent") != EXPECTED_PARENT, "PARENT")
    builder = data.get("builder", {})
    add(errors, builder.get("path") != EXACT_SEVEN[0], "BUILDER_PATH")
    add(errors, builder.get("normalized_sha256") != digest(normalized_bytes(BUILDER)), "BUILDER_HASH")
    add(errors, builder.get("raw_sha256") != digest(BUILDER.read_bytes()), "BUILDER_RAW_HASH")
    add(errors, builder.get("newline_policy") != "LF_ONLY" or not lf_only(BUILDER), "BUILDER_NEWLINES")
    add(errors, not lf_only(VALIDATOR), "VALIDATOR_NEWLINES")
    add(errors, input_artifact_diagnostics(data.get("input_artifacts")), "INPUT_ARTIFACTS")
    contract = data.get("result_first_contract", {})
    evidence, evidence_hash = evidence_block()
    add(errors, contract.get("result_path") != EXACT_SEVEN[3], "RESULT_PATH")
    add(errors, contract.get("evidence_semantic_sha256") != evidence_hash, "RESULT_EVIDENCE_HASH")
    add(errors, contract.get("containing_commit") != "PENDING_AT_PRECOMMIT_BY_DESIGN", "RESULT_FIRST")
    add(errors, contract.get("persistence_claimed") is not False, "PERSISTENCE_CLAIM")
    add(errors, contract.get("step61_blocked_until") != "PASS_P063_STEP60_PERSISTENCE", "STEP61_BLOCKER")
    add(errors, data.get("counts") != EXPECTED_COUNTS, "COUNTS")

    citations = data.get("citation_occurrences_all_text_partitions")
    bibliography = data.get("bibliography_occurrences_all_text_partitions")
    manual_references = data.get("manual_unkeyed_bibliography_occurrences")
    dois = data.get("doi_occurrences_all_text_partitions")
    equations = data.get("equation_candidates_all_text_partitions")
    tex_math = data.get("tex_delimited_math_candidates_all_text_partitions")
    claims = data.get("claim_candidate_lines_all_text_partitions")
    add(errors, not sequential_ids(citations, "citation_occurrence_id", "P063-S60-CITE-"), "CITATION_IDS")
    add(errors, not sequential_ids(bibliography, "bibliography_occurrence_id", "P063-S60-BIB-"), "BIBLIOGRAPHY_IDS")
    add(errors, not sequential_ids(manual_references, "manual_reference_occurrence_id", "P063-S60-MANREF-"), "MANUAL_REFERENCE_IDS")
    add(errors, not sequential_ids(dois, "doi_occurrence_id", "P063-S60-DOI-"), "DOI_IDS")
    add(errors, not sequential_ids(equations, "equation_candidate_id", "P063-S60-EQ-"), "EQUATION_IDS")
    add(errors, not sequential_ids(
        tex_math, "tex_math_candidate_id", "P063-S60-TEXMATH-"
    ), "TEX_MATH_IDS")
    add(errors, not sequential_ids(claims, "claim_candidate_id", "P063-S60-CLM-"), "CLAIM_CANDIDATE_IDS")
    profile = data.get("authority_axis_profiles")
    expected_profile = {
        LEXICAL_AUTHORITY_PROFILE_ID: {
            "axis_states": LEXICAL_AUTHORITY_PROFILE,
            "applies_to": [
                "equation_candidates_all_text_partitions",
                "tex_delimited_math_candidates_all_text_partitions",
                "claim_candidate_lines_all_text_partitions",
                "manual_unkeyed_bibliography_occurrences",
            ],
            "semantic_claim_adjudicated": False,
            "external_truth_promoted": False,
        }
    }
    add(errors, profile != expected_profile, "AUTHORITY_PROFILE")
    add(errors, not isinstance(equations, list) or any(
        row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
        or row.get("authority_axes_assigned") is not True for row in equations
    ), "EQUATION_AXIS_ASSIGNMENT")
    add(errors, not isinstance(equations, list) or not any(
        row.get("path") == "Claude/docs/v1.0.22/results/comp_FR/A03_REVIEW.md"
        and row.get("start_line") == 291 and row.get("end_line") == 295
        and row.get("body_sha256")
        == "a691fb856f0bf656999401ec6c68515a6ba50b3f9229179fefa319b8c658a60f"
        for row in equations
    ), "EQUATION_REQUIRED_MARKDOWN_ANCHOR")
    add(errors, not isinstance(equations, list) or not any(
        row.get("path") == "Claude/docs/v1.0.22/results/comp_FR/A11_REVIEW.md"
        and row.get("start_line") == 19 and row.get("end_line") == 19
        and row.get("environment") == "bracket"
        and row.get("body_sha256")
        == "8ce4c79f1aa3afe7750e059a6ab572556fe74f327a39c6341f8208f819fb9e84"
        for row in equations
    ), "EQUATION_INLINE_BRACKET_ANCHOR")
    a15_inline_equations = [
        row for row in equations
        if row.get("path") == "Claude/docs/v1.0.22/results/comp_FR/A15_REVIEW.md"
        and row.get("start_line") == 23
        and row.get("environment") == "equation*"
    ] if isinstance(equations, list) else []
    add(errors, len(a15_inline_equations) != 2 or len({
        row.get("start_column") for row in a15_inline_equations
    }) != 2, "EQUATION_MULTIPLE_SAME_LINE_OCCURRENCES")
    add(errors, not isinstance(claims, list) or any(
        row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
        or row.get("authority_axes_assigned") is not True
        or row.get("claim_occurrence_inventory_state")
        != "INVENTORIED_AUTHORITY_BOUNDED_NOT_SEMANTICALLY_NORMALIZED"
        for row in claims
    ), "CLAIM_AXIS_ASSIGNMENT")
    add(errors, not isinstance(tex_math, list) or any(
        row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
        or row.get("authority_axes_assigned") is not True
        or row.get("claim_occurrence_inventory_state")
        != "INVENTORIED_AUTHORITY_BOUNDED_NOT_SEMANTICALLY_NORMALIZED"
        or row.get("semantic_claim_adjudicated") is not False
        for row in tex_math
    ), "TEX_MATH_AXIS_ASSIGNMENT")
    required_tex_math_hashes = {
        "76df07d1b14aad45511a28e37346a640282e513c3da7b99611b7abb7cb391f2a",
        "c349d2daba0415214a9dbd2ea231bca0644c85fa72437b13367069a34c7d7cd8",
        "ea219dfb1f7b0384bb69ecfd761f5f6fa3fb49322f7876e875d75cb4a94c791c",
        "a6e1cea0c99116165c19408b0e12a7e561b2498fdac3f3f55bfb6a1a02c39b4a",
        "76ae9a98e47f8e10ac7c3df5d65895e96a42476fcbfb811a7dc72979a32b6348",
    }
    actual_required_hashes = {
        row.get("body_sha256") for row in tex_math
        if (row.get("source_id"), row.get("start_line"), row.get("end_line"))
        in {
            ("P063-SRC-0003", 23, 23),
            ("P063-SRC-0003", 34, 35),
            ("P063-SRC-0008", 51, 51),
        }
    } if isinstance(tex_math, list) else set()
    actual_required_hashes.update(
        row.get("body_sha256") for row in tex_math
        if row.get("path") == "Claude/docs/v1.0.22/results/R1B_SWEEP_LIST.md"
        and row.get("start_line") in {127, 143}
    ) if isinstance(tex_math, list) else None
    add(errors, not required_tex_math_hashes <= actual_required_hashes, "TEX_MATH_REQUIRED_ANCHOR")
    markdown_recovery_rows = {
        (row.get("start_line"), row.get("end_line"), row.get("body_sha256"))
        for row in tex_math
        if row.get("path") == "Claude/docs/v1.0.22/results/comp_FR/A05_REVIEW.md"
    } if isinstance(tex_math, list) else set()
    add(errors, not {
        (54, 54, "44c15fcc3206088522fbb5ab1f69696e2cac3a88a41406b0f099421195c8fbd0"),
        (157, 157, "0d7aa28953cf81fdce0deefdd7b1e3b827ea532d867f167c6da96c370679a60d"),
    } <= markdown_recovery_rows, "TEX_MATH_MARKDOWN_RECOVERY")
    markdown_multiline_rows = {
        (row.get("path"), row.get("start_line"), row.get("end_line"), row.get("body_sha256"))
        for row in tex_math
        if row.get("path", "").lower().endswith(".md")
    } if isinstance(tex_math, list) else set()
    add(errors, not {
        (
            "Claude/docs/v1.0.22/results/comp_FR/A06_REVIEW.md",
            42,
            43,
            "881481f1aec47e0ff6ad7b9675aa67fad532a160fa2fe9e8aa364e2d998ff454",
        ),
        (
            "Claude/docs/v1.0.22/results/comp_FR/A20_REVIEW.md",
            262,
            265,
            "0558039300e30482ca401587a17a80dbd9d104be0304f9d971a82a9a0741087f",
        ),
    } <= markdown_multiline_rows, "TEX_MATH_MARKDOWN_MULTILINE_RECOVERY")
    add(errors, not isinstance(tex_math, list) or Counter(
        row.get("syntax") for row in tex_math
    ) != Counter({
        "INLINE_DOLLAR": 14953,
        "UNPAIRED_INLINE_DOLLAR": 3,
        "UNTERMINATED_INLINE_DOLLAR": 1,
        "DISPLAY_DOLLAR": 1,
    }), "TEX_MATH_SYNTAX_COUNTS")
    add(errors, not isinstance(manual_references, list) or any(
        row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
        or row.get("authority_axes_assigned") is not True for row in manual_references
    ), "MANUAL_REFERENCE_AXES")

    stored_evidence = data.get("manual_literature_scope_evidence")
    add(errors, stored_evidence != evidence, "RESULT_EVIDENCE_PARITY")
    if isinstance(stored_evidence, dict):
        literature = stored_evidence.get("literature_claims", [])
        materials = stored_evidence.get("material_scope_ledger", [])
        findings = stored_evidence.get("findings", [])
        add(errors, {row.get("claim_id") for row in literature} != LITERATURE_IDS, "LITERATURE_IDS")
        add(errors, {row.get("material_id") for row in materials} != MATERIAL_IDS, "MATERIAL_IDS")
        add(errors, {row.get("finding_id") for row in findings} != FINDING_IDS, "FINDING_IDS")
        add(errors, stored_evidence.get("inventory_summary") != EXPECTED_INVENTORY_SUMMARY, "INVENTORY_SUMMARY")
        add(errors, set(stored_evidence.get("authority_axes", [])) != {
            key.upper() for key in AUTHORITY_AXIS_KEYS
        } or len(stored_evidence.get("authority_axes", [])) != 7, "AUTHORITY_AXES")
        attestation = stored_evidence.get("semantic_review_attestation", {})
        add(errors, attestation.get("authority") != "INTERNAL_SEMANTIC_REVIEW_ATTESTATION_ONLY"
            or attestation.get("full_text_source_count") != 33
            or attestation.get("full_text_physical_lines") != 4134
            or not isinstance(attestation.get("full_text_rows"), list)
            or len(attestation.get("full_text_rows", [])) != 33
            or attestation.get("additional_semantic_interval_count") != 11
            or attestation.get("additional_semantic_source_count") != 10
            or attestation.get("additional_semantic_unique_physical_lines") != 409
            or not isinstance(attestation.get("additional_semantic_intervals"), list)
            or len(attestation.get("additional_semantic_intervals", [])) != 11
            or attestation.get("manual_evidence_anchor_count") != 52
            or attestation.get("manual_evidence_anchor_path_count") != 30
            or attestation.get("manual_evidence_coverage_state")
            != "ALL_52_ANCHORS_COVERED_BY_SEMANTIC_ATTESTATION",
            "SEMANTIC_ATTESTATION")
        errors.update(row_contract_errors(
            literature, materials, findings, MANUAL_REFERENCE_IDS,
        ))
        add(errors, any(row.get("external_truth_promoted") is not False for row in literature), "LITERATURE_PROMOTION")
        add(errors, any(row.get("external_truth_promoted") is not False for row in materials), "MATERIAL_PROMOTION")
        add(errors, any(row.get("external_truth_promoted") is not False for row in findings), "FINDING_PROMOTION")
        add(errors, stored_evidence.get("primary_literature_truth_validated") is not False, "PRIMARY_TRUTH")
    else:
        errors.add("MANUAL_EVIDENCE")
    add(errors, data.get("findings") != evidence.get("findings"), "FINDING_PARITY")
    add(errors, data.get("finding_summary") != {"P0": 6, "P1": 13, "P2": 7}, "FINDING_SUMMARY")
    authority = data.get("authority_boundary", {})
    add(errors, any(authority.get(key) is not False for key in FALSE_AUTHORITY_FLAGS), "AUTHORITY_FLAGS")
    add(errors, data.get("semantic_sha256") != digest(compact(semantic_projection(data))), "SEMANTIC_HASH")

    q = data.get("independent_quantity_checks", {})
    expected_q = {
        "lco_slope_implied_reaction_entropy_J_per_molK": 96485.33212 * 0.00083,
        "charge_order_0p47_implied_microV_per_K": 0.47 / 96485.33212 * 1.0e6,
        "charge_order_1p49_implied_microV_per_K": 1.49 / 96485.33212 * 1.0e6,
        "si_Li3p75Si_mAh_per_g": 3.75 * (96485.33212 / 3.6) / 28.0855,
        "si_Li4p4Si_mAh_per_g": 4.4 * (96485.33212 / 3.6) / 28.0855,
        "sio_2p8125_e_per_SiO_mAh_per_g": 2.8125 * (96485.33212 / 3.6) / 44.0849,
        "si_c_first_charge_ICE_percent": 100.0 * 3117.0 / 3801.0,
    }
    add(errors, any(not math.isclose(q.get(key, math.nan), value, rel_tol=0.0, abs_tol=1e-10) for key, value in expected_q.items()), "QUANTITY_CHECKS")
    add(errors, q.get("external_truth_validated") is not False, "QUANTITY_PROMOTION")
    return errors


def normalize_doi(token: str) -> str:
    value = token.strip().rstrip(".,;:").lower()
    while value.endswith(")") and value.count("(") < value.count(")"):
        value = value[:-1]
    return value


def bibliography_conflicts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    by_doi: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_key[row["cite_key"]].append(row)
        for doi in row["doi_values"]:
            by_doi[doi].append(row)
    key_variants = []
    for key, values in sorted(by_key.items()):
        bodies = sorted({row["body_sha256"] for row in values})
        doi_sets = sorted({tuple(row["doi_values"]) for row in values})
        if len(bodies) > 1 or len(doi_sets) > 1:
            key_variants.append({
                "cite_key": key,
                "occurrence_ids": [row["bibliography_occurrence_id"] for row in values],
                "body_variants": len(bodies),
                "doi_set_variants": [list(value) for value in doi_sets],
                "state": "VERSION_OR_PROPOSAL_VARIANT_REQUIRES_MANUAL_ADJUDICATION",
                "external_metadata_validated": False,
            })
    doi_multi_keys = []
    for doi, values in sorted(by_doi.items()):
        keys = sorted({row["cite_key"] for row in values})
        if len(keys) > 1:
            doi_multi_keys.append({
                "doi": doi,
                "cite_keys": keys,
                "occurrence_ids": [row["bibliography_occurrence_id"] for row in values],
                "state": "SHARED_DOI_ACROSS_KEYS_REQUIRES_MANUAL_ADJUDICATION",
            })
    multi_doi_entries = [
        {"bibliography_occurrence_id": row["bibliography_occurrence_id"],
         "cite_key": row["cite_key"], "doi_values": row["doi_values"]}
        for row in rows if len(row["doi_values"]) > 1
    ]
    return {
        "same_key_variant_groups": key_variants,
        "same_doi_multiple_key_groups": doi_multi_keys,
        "multiple_doi_single_entry_occurrences": multi_doi_entries,
        "interpretation": "These are frozen internal identity conflicts or revision variants; they are not external metadata verdicts.",
    }


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def line_interval(text: str, start: int, end: int) -> tuple[int, int]:
    return line_number(text, start), line_number(text, max(start, end - 1))


def is_escaped(text: str, offset: int) -> bool:
    count = 0
    cursor = offset - 1
    while cursor >= 0 and text[cursor] == "\\":
        count += 1
        cursor -= 1
    return count % 2 == 1


def find_unescaped_token(text: str, token: str, start: int = 0) -> int:
    cursor = text.find(token, start)
    while cursor >= 0 and is_escaped(text, cursor):
        cursor = text.find(token, cursor + 1)
    return cursor


def markdown_tex_delimited_math_spans(text: str) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    line_offset = 0
    mode: str | None = None
    start = -1
    previous_line = ""
    physical_lines = text.splitlines(keepends=True)
    for line_index, physical_line in enumerate(physical_lines):
        line = physical_line.rstrip("\r\n")
        stripped = line.lstrip()
        previous_stripped = previous_line.lstrip()
        structural_boundary = (
            line_index > 0
            and mode == "INLINE_DOLLAR"
            and (
                not line.strip()
                or previous_stripped.startswith("|")
                or stripped.startswith("|")
                or stripped.startswith("#")
                or stripped.startswith("```")
                or stripped.startswith("~~~")
            )
        )
        if structural_boundary:
            spans.append((start, start + 1, "UNPAIRED_INLINE_DOLLAR"))
            mode, start = None, -1
        cursor = 0
        while cursor < len(line):
            if mode is None:
                if line.startswith(r"\(", cursor) and not is_escaped(line, cursor):
                    mode, start, cursor = "INLINE_PAREN", line_offset + cursor, cursor + 2
                    continue
                if line[cursor] == "$" and not is_escaped(line, cursor):
                    if line.startswith("$$", cursor):
                        mode, start, cursor = "DISPLAY_DOLLAR", line_offset + cursor, cursor + 2
                    elif cursor + 1 < len(line) and not line[cursor + 1].isspace():
                        mode, start, cursor = "INLINE_DOLLAR", line_offset + cursor, cursor + 1
                    else:
                        spans.append((
                            line_offset + cursor,
                            line_offset + cursor + 1,
                            "UNPAIRED_INLINE_DOLLAR",
                        ))
                        cursor += 1
                    continue
            elif mode == "INLINE_PAREN":
                if line.startswith(r"\)", cursor) and not is_escaped(line, cursor):
                    spans.append((start, line_offset + cursor + 2, mode))
                    mode, start, cursor = None, -1, cursor + 2
                    continue
                if line[cursor] == "$" and not is_escaped(line, cursor):
                    spans.append((
                        line_offset + cursor,
                        line_offset + cursor + 1,
                        "UNPAIRED_INLINE_DOLLAR",
                    ))
                    cursor += 1
                    continue
            elif mode == "INLINE_DOLLAR":
                if line[cursor] == "$" and not is_escaped(line, cursor):
                    spans.append((start, line_offset + cursor + 1, mode))
                    mode, start, cursor = None, -1, cursor + 1
                    continue
            elif mode == "DISPLAY_DOLLAR":
                if line.startswith("$$", cursor) and not is_escaped(line, cursor):
                    spans.append((start, line_offset + cursor + 2, mode))
                    mode, start, cursor = None, -1, cursor + 2
                    continue
                if line[cursor] == "$" and not is_escaped(line, cursor):
                    spans.append((
                        line_offset + cursor,
                        line_offset + cursor + 1,
                        "UNPAIRED_INLINE_DOLLAR",
                    ))
                    cursor += 1
                    continue
            cursor += 1
        previous_line = line
        line_offset += len(physical_line)
    if mode is not None:
        opening_width = 2 if mode in {"INLINE_PAREN", "DISPLAY_DOLLAR"} else 1
        syntax = (
            "UNPAIRED_INLINE_DOLLAR"
            if mode == "INLINE_DOLLAR"
            else f"UNTERMINATED_{mode}"
        )
        spans.append((start, start + opening_width, syntax))
    return spans


def tex_delimited_math_spans(text: str, path: str) -> list[tuple[int, int, str]]:
    if path.lower().endswith(".md"):
        return markdown_tex_delimited_math_spans(text)
    spans: list[tuple[int, int, str]] = []
    mode: str | None = None
    start = -1
    cursor = 0
    while cursor < len(text):
        if mode is None:
            if text.startswith(r"\(", cursor) and not is_escaped(text, cursor):
                mode, start, cursor = "INLINE_PAREN", cursor, cursor + 2
                continue
            if text[cursor] == "$" and not is_escaped(text, cursor):
                if text.startswith("$$", cursor):
                    mode, start, cursor = "DISPLAY_DOLLAR", cursor, cursor + 2
                else:
                    mode, start, cursor = "INLINE_DOLLAR", cursor, cursor + 1
                continue
        elif mode == "INLINE_PAREN":
            if text.startswith(r"\)", cursor) and not is_escaped(text, cursor):
                spans.append((start, cursor + 2, mode))
                mode, start, cursor = None, -1, cursor + 2
                continue
        elif mode == "INLINE_DOLLAR":
            if text[cursor] == "$" and not is_escaped(text, cursor):
                spans.append((start, cursor + 1, mode))
                mode, start, cursor = None, -1, cursor + 1
                continue
        elif mode == "DISPLAY_DOLLAR":
            if text.startswith("$$", cursor) and not is_escaped(text, cursor):
                spans.append((start, cursor + 2, mode))
                mode, start, cursor = None, -1, cursor + 2
                continue
        cursor += 1
    if mode is not None:
        opening_width = 2 if mode in {"INLINE_PAREN", "DISPLAY_DOLLAR"} else 1
        spans.append((start, start + opening_width, f"UNTERMINATED_{mode}"))
    return spans


def validate_dollar_endpoint_coverage(
    rows: list[dict[str, Any]], texts: dict[str, str],
) -> None:
    """Require every raw unescaped all-text `$` endpoint exactly once."""
    rows_by_path: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        rows_by_path[row["path"]].append(row)
    all_text_total = 0
    markdown_total = 0
    for path, text in texts.items():
        raw = Counter(
            index for index, character in enumerate(text)
            if character == "$" and not is_escaped(text, index)
        )
        all_text_total += raw.total()
        if path.lower().endswith(".md"):
            markdown_total += raw.total()
        represented: Counter[int] = Counter()
        line_starts = [0] + [
            index + 1 for index, character in enumerate(text) if character == "\n"
        ]
        for row in rows_by_path.get(path, []):
            syntax = row["syntax"]
            if "DOLLAR" not in syntax:
                continue
            start_line = row["start_line"]
            start_column = row["start_column"]
            absolute_start = line_starts[start_line - 1] + start_column - 1
            body = row["body"]
            if text[absolute_start:absolute_start + len(body)] != body:
                raise ValidationError(f"dollar row/source slice mismatch: {path}")
            absolute_end = absolute_start + len(body)
            if syntax == "INLINE_DOLLAR":
                endpoints = (absolute_start, absolute_end - 1)
            elif syntax == "DISPLAY_DOLLAR":
                endpoints = (
                    absolute_start,
                    absolute_start + 1,
                    absolute_end - 2,
                    absolute_end - 1,
                )
            elif syntax in {"UNPAIRED_INLINE_DOLLAR", "UNTERMINATED_INLINE_DOLLAR"}:
                endpoints = (absolute_start,)
            elif syntax == "UNTERMINATED_DISPLAY_DOLLAR":
                endpoints = (absolute_start, absolute_start + 1)
            else:
                raise ValidationError(f"unknown dollar syntax: {syntax}")
            represented.update(endpoints)
        if represented != raw:
            missing = sorted((raw - represented).elements())
            extra = sorted((represented - raw).elements())
            raise ValidationError(
                "dollar endpoint coverage mismatch: "
                f"{path} missing={missing[:8]} extra_or_duplicate={extra[:8]}"
            )
    if all_text_total != 29914 or markdown_total != 14075:
        raise ValidationError(
            "dollar endpoint frozen totals mismatch: "
            f"all_text={all_text_total} markdown={markdown_total}"
        )


def validate_display_opener_coverage(
    rows: list[dict[str, Any]], texts: dict[str, str],
) -> None:
    """Independently biject every raw display opener to one candidate row."""
    raw: Counter[tuple[str, int, str]] = Counter()
    for path, text in texts.items():
        for match in DISPLAY_BEGIN_RE.finditer(text):
            if not is_escaped(text, match.start()):
                raw[(path, match.start(), match.group("environment"))] += 1
        cursor = 0
        while True:
            start = find_unescaped_token(text, r"\[", cursor)
            if start < 0:
                break
            raw[(path, start, "bracket")] += 1
            cursor = start + 2
    represented: Counter[tuple[str, int, str]] = Counter()
    for row in rows:
        text = texts[row["path"]]
        line_starts = [0] + [
            index + 1 for index, character in enumerate(text) if character == "\n"
        ]
        absolute_start = (
            line_starts[row["start_line"] - 1] + row["start_column"] - 1
        )
        represented[(row["path"], absolute_start, row["environment"])] += 1
    if raw.total() != 339 or represented != raw:
        missing = list((raw - represented).elements())
        extra = list((represented - raw).elements())
        raise ValidationError(
            "display opener coverage mismatch: "
            f"raw={raw.total()} represented={represented.total()} "
            f"missing={missing[:4]} extra_or_duplicate={extra[:4]}"
        )


def display_equation_spans(text: str, path: str) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    for match in DISPLAY_BEGIN_RE.finditer(text):
        if is_escaped(text, match.start()):
            continue
        environment = match.group("environment")
        end_token = rf"\end{{{environment}}}"
        end_start = find_unescaped_token(text, end_token, match.end())
        if end_start < 0:
            raise ValidationError(
                f"unterminated display replay: {path}:{line_number(text, match.start())}"
            )
        spans.append((match.start(), end_start + len(end_token), environment))
    cursor = 0
    while True:
        start = find_unescaped_token(text, r"\[", cursor)
        if start < 0:
            break
        end_start = find_unescaped_token(text, r"\]", start + 2)
        if end_start < 0:
            raise ValidationError(
                f"unterminated bracket replay: {path}:{line_number(text, start)}"
            )
        spans.append((start, end_start + 2, "bracket"))
        cursor = end_start + 2
    return sorted(spans, key=lambda item: (item[0], item[1], item[2]))


def validate_frozen_replay(data: dict[str, Any]) -> None:
    topology, _ = strict_load(TOPOLOGY)
    if not isinstance(topology, dict):
        raise ValidationError("topology root")
    expected_sources = [
        source for source in topology["sources"]
        if source["review_mode"] == "FULL_TEXT"
    ]
    stored_sources = data.get("source_read_attestations")
    if not isinstance(stored_sources, list) or len(stored_sources) != 201:
        raise ValidationError("source attestation cardinality")
    supplemental = topology["supplemental_process_control"]
    expected_keys = [
        (source["source_id"], source["path"]) for source in expected_sources
    ] + [(supplemental["source_id"], supplemental["path"])]
    if [(row.get("source_id"), row.get("path")) for row in stored_sources] != expected_keys:
        raise ValidationError("source attestation ordering/identity")

    texts: dict[str, str] = {}
    source_map: dict[str, dict[str, Any]] = {}
    topology_map = {source["path"]: source for source in expected_sources}
    for row in stored_sources:
        path = row["path"]
        raw = git_bytes("show", f"{BASELINE}:{path}")
        text = raw.decode("utf-8", "strict")
        lines = text.splitlines()
        blob = git_text("rev-parse", f"{BASELINE}:{path}")
        if path in topology_map:
            source = topology_map[path]
            expected = (
                source["source_id"], source["partition"], source["blob_sha1"],
                source["sha256"], source["extent"]["lines"], True,
                source["role"], source["extension"],
                PARTITION_CEILING[source["partition"]],
            )
        elif path == supplemental["path"]:
            expected = (
                supplemental["source_id"], "SUPPLEMENTAL_PROCESS_CONTROL",
                supplemental["blob_sha1"], supplemental["sha256"],
                supplemental["physical_lines"], False,
                "SUPPLEMENTAL_PROCESS_CONTROL", Path(path).suffix.lower(),
                PARTITION_CEILING["SUPPLEMENTAL_PROCESS_CONTROL"],
            )
        else:
            raise ValidationError(f"unknown stored source: {path}")
        actual = (
            row.get("source_id"), row.get("partition"), blob,
            digest(raw), len(lines), row.get("manifest_member"),
            row.get("role"), row.get("extension"), row.get("authority_ceiling"),
        )
        if actual != expected:
            raise ValidationError(f"source identity replay mismatch: {path}")
        if row.get("git_blob") != blob or row.get("raw_sha256") != digest(raw):
            raise ValidationError(f"stored source digest mismatch: {path}")
        if row.get("bytes") != len(raw) or row.get("physical_lines") != len(lines):
            raise ValidationError(f"stored source extent mismatch: {path}")
        if row.get("read_interval") != [1, len(lines)]:
            raise ValidationError(f"stored source read interval mismatch: {path}")
        if row.get("read_state") != "READ_FULL_IN_STEP58_REPLAYED_FROM_FROZEN_GIT_BLOB":
            raise ValidationError(f"stored source read state mismatch: {path}")
        texts[path] = text
        source_map[path] = row

    manual = data["manual_literature_scope_evidence"]
    attestation = manual["semantic_review_attestation"]
    full_rows = attestation["full_text_rows"]
    semantic_coverage: defaultdict[str, set[int]] = defaultdict(set)
    if len({row.get("source_id") for row in full_rows}) != 33:
        raise ValidationError("semantic full-text source identity cardinality")
    semantic_lines = 0
    for row in full_rows:
        source = source_map.get(row.get("path"))
        if source is None:
            raise ValidationError("semantic full-text source missing")
        expected = {
            "source_id": source["source_id"],
            "path": source["path"],
            "git_blob": source["git_blob"],
            "read_interval": [1, source["physical_lines"]],
            "physical_lines": source["physical_lines"],
            "read_state": "READ_FULL_SEMANTIC",
        }
        if row != expected:
            raise ValidationError(f"semantic full-text attestation mismatch: {row.get('path')}")
        semantic_lines += row["physical_lines"]
        semantic_coverage[row["path"]].update(range(1, row["physical_lines"] + 1))
    if semantic_lines != 4134 or attestation.get("full_text_physical_lines") != semantic_lines:
        raise ValidationError("semantic full-text attestation line total")
    additional = attestation.get("additional_semantic_intervals")
    if not isinstance(additional, list) or len(additional) != 11:
        raise ValidationError("additional semantic interval cardinality")
    additional_coverage: defaultdict[str, set[int]] = defaultdict(set)
    for row in additional:
        source = source_map.get(row.get("path"))
        interval = row.get("read_interval")
        expected_keys = {
            "source_id", "path", "git_blob", "read_interval", "read_state",
        }
        if source is None or set(row) != expected_keys \
                or row.get("source_id") != source.get("source_id") \
                or row.get("git_blob") != source.get("git_blob") \
                or row.get("read_state") != "READ_SEMANTIC_EXPLICIT_INTERVAL" \
                or not isinstance(interval, list) or len(interval) != 2 \
                or not all(isinstance(number, int) for number in interval) \
                or not (1 <= interval[0] <= interval[1] <= source["physical_lines"]):
            raise ValidationError(f"additional semantic interval mismatch: {row.get('path')}")
        segment = set(range(interval[0], interval[1] + 1))
        if additional_coverage[row["path"]] & segment:
            raise ValidationError("additional semantic interval overlap")
        additional_coverage[row["path"]].update(segment)
        semantic_coverage[row["path"]].update(segment)
    additional_lines = sum(len(lines) for lines in additional_coverage.values())
    if len(additional_coverage) != 10 or additional_lines != 409 \
            or attestation.get("additional_semantic_interval_count") != 11 \
            or attestation.get("additional_semantic_source_count") != 10 \
            or attestation.get("additional_semantic_unique_physical_lines") != 409:
        raise ValidationError("additional semantic interval totals")
    code = attestation.get("partial_code_review", {})
    code_source = source_map.get(code.get("path"))
    intervals = code.get("read_intervals")
    if code_source is None or code_source.get("source_id") != "P063-SRC-0001" \
            or code.get("source_id") != code_source.get("source_id") \
            or code.get("git_blob") != code_source.get("git_blob") \
            or code.get("physical_lines") != code_source.get("physical_lines") \
            or code.get("read_state") != "PARTIAL_SEMANTIC_CODE_SCOPE" \
            or intervals != [[160, 198], [855, 1350]]:
        raise ValidationError("semantic partial-code attestation identity")
    covered: set[int] = set()
    for interval in intervals:
        start, end = interval
        if not (1 <= start <= end <= code_source["physical_lines"]):
            raise ValidationError("semantic partial-code interval bounds")
        segment = set(range(start, end + 1))
        if covered & segment:
            raise ValidationError("semantic partial-code interval overlap")
        covered.update(segment)
    if len(covered) != 535 or code.get("unique_physical_lines") != len(covered):
        raise ValidationError("semantic partial-code unique line total")
    semantic_coverage[code["path"]].update(covered)
    anchor_count = 0
    anchor_paths: set[str] = set()
    for collection in (manual["literature_claims"], manual["material_scope_ledger"]):
        for claim in collection:
            for anchor in claim.get("source_evidence", []):
                source = source_map.get(anchor.get("path"))
                interval = anchor.get("lines")
                if (
                    source is None
                    or anchor.get("source_id") != source.get("source_id")
                    or not isinstance(interval, list)
                    or len(interval) != 2
                    or not all(isinstance(number, int) for number in interval)
                    or not (1 <= interval[0] <= interval[1] <= source["physical_lines"])
                ):
                    raise ValidationError(
                        f"manual source anchor mismatch: {claim.get('claim_id') or claim.get('material_id')}"
                    )
                anchor_count += 1
                anchor_paths.add(anchor["path"])
                if not set(range(interval[0], interval[1] + 1)) <= semantic_coverage[anchor["path"]]:
                    raise ValidationError(
                        f"manual source anchor outside semantic attestation: "
                        f"{claim.get('claim_id') or claim.get('material_id')}"
                    )
    if anchor_count != 52 or len(anchor_paths) != 30 \
            or attestation.get("manual_evidence_anchor_count") != 52 \
            or attestation.get("manual_evidence_anchor_path_count") != 30 \
            or attestation.get("manual_evidence_coverage_state") \
            != "ALL_52_ANCHORS_COVERED_BY_SEMANTIC_ATTESTATION":
        raise ValidationError("manual source anchor semantic coverage totals")

    expected_citations = []
    expected_bibliography = []
    expected_dois = []
    expected_equations = []
    expected_tex_math = []
    expected_claims = []
    citation_commands = 0
    for path in sorted(texts):
        text = texts[path]
        source = source_map[path]
        lines = text.splitlines()
        for match in CITE_RE.finditer(text):
            citation_commands += 1
            start_line, end_line = line_interval(text, match.start(), match.end())
            for key_ordinal, raw_key in enumerate(match.group("keys").split(","), start=1):
                expected_citations.append((
                    source["source_id"], path, source["partition"], source["git_blob"],
                    start_line, end_line, match.group("command"), citation_commands,
                    key_ordinal,
                    raw_key.strip(), digest(match.group(0).encode("utf-8")),
                    source["authority_ceiling"],
                ))
        matches = list(BIBITEM_RE.finditer(text))
        for ordinal, match in enumerate(matches):
            next_start = matches[ordinal + 1].start() if ordinal + 1 < len(matches) else len(text)
            line_end = text.find("\n", match.end(), next_start)
            end = line_end if line_end >= 0 else next_start
            body = text[match.start():end].rstrip() + "\n"
            start_line, end_line = line_interval(text, match.start(), end)
            expected_bibliography.append((
                source["source_id"], path, source["partition"], source["git_blob"],
                start_line, end_line, match.group("key").strip(),
                sorted({normalize_doi(item.group(0)) for item in DOI_RE.finditer(body)}),
                digest(body.encode("utf-8")), body, source["authority_ceiling"],
            ))
        for match in DOI_RE.finditer(text):
            start_line, end_line = line_interval(text, match.start(), match.end())
            expected_dois.append((
                source["source_id"], path, source["partition"], source["git_blob"],
                start_line, end_line, match.group(0), normalize_doi(match.group(0)),
                lines[start_line - 1], digest((lines[start_line - 1] + "\n").encode("utf-8")),
            ))
        equation_ordinals: Counter[int] = Counter()
        for start, end, environment in display_equation_spans(text, path):
            start_line, end_line = line_interval(text, start, end)
            equation_ordinals[start_line] += 1
            body = text[start:end]
            last_newline = text.rfind("\n", 0, end)
            expected_equations.append((
                source["source_id"], path, source["partition"], source["git_blob"],
                start_line, end_line, equation_ordinals[start_line],
                start - text.rfind("\n", 0, start),
                end - last_newline - 1,
                environment, re.findall(r"\\label\{([^{}]+)\}", body), body,
                digest(body.encode("utf-8")), source["authority_ceiling"],
            ))
        ordinals: Counter[int] = Counter()
        for start, end, syntax in tex_delimited_math_spans(text, path):
            start_line, end_line = line_interval(text, start, end)
            ordinals[start_line] += 1
            body = text[start:end]
            expected_tex_math.append((
                source["source_id"], path, source["partition"], source["git_blob"],
                start_line, end_line, ordinals[start_line],
                start - text.rfind("\n", 0, start),
                end - text.rfind("\n", 0, end) - 1,
                syntax, body, digest(body.encode("utf-8")),
                source["authority_ceiling"],
            ))
        for number, line in enumerate(lines, start=1):
            kinds = []
            if DOI_RE.search(line):
                kinds.append("DOI_METADATA")
            if BIBITEM_RE.search(line):
                kinds.append("BIBLIOGRAPHY_RECORD")
            if CITE_RE.search(line):
                kinds.append("CITATION")
            if NUMBER_RE.search(line) and UNIT_RE.search(line):
                kinds.append("NUMERIC_QUANTITY")
            if MATERIAL_RE.search(line):
                kinds.append("MATERIAL_SCOPE")
            if kinds:
                expected_claims.append((
                    source["source_id"], path, source["partition"], source["git_blob"],
                    number, sorted(kinds), digest((line + "\n").encode("utf-8")),
                    line, source["authority_ceiling"],
                ))

    citations = data["citation_occurrences_all_text_partitions"]
    actual_citations = [(
        row["source_id"], row["path"], row["partition"], row["git_blob"],
        row["start_line"], row["end_line"], row["command"], row["command_ordinal"],
        row["key_ordinal_within_command"],
        row["cite_key"], row["command_sha256"], row["authority_ceiling"],
    ) for row in citations]
    if actual_citations != expected_citations or citation_commands != EXPECTED_COUNTS["citation_commands"]:
        raise ValidationError("citation occurrence replay mismatch")
    bibliography = data["bibliography_occurrences_all_text_partitions"]
    actual_bibliography = [(
        row["source_id"], row["path"], row["partition"], row["git_blob"],
        row["start_line"], row["end_line"], row["cite_key"], row["doi_values"],
        row["body_sha256"], row["body"], row["authority_ceiling"],
    ) for row in bibliography]
    if actual_bibliography != expected_bibliography:
        raise ValidationError("bibliography occurrence replay mismatch")
    if any(row.get("external_metadata_validated") is not False or row.get("fulltext_proposition_validated") is not False for row in bibliography):
        raise ValidationError("bibliography authority promotion")
    if data.get("bibliography_identity_conflicts") != bibliography_conflicts(bibliography):
        raise ValidationError("bibliography conflict replay mismatch")
    manual_path = "Claude/docs/v1.0.22/appendix_phase_separation.tex"
    manual_source = source_map[manual_path]
    manual_text = texts[manual_path]
    block_start = manual_text.index(
        r"\begin{enumerate}[label={[A\arabic*]},leftmargin=3.2em]",
        manual_text.index(r"\section*{참고문헌}"),
    ) + len(r"\begin{enumerate}[label={[A\arabic*]},leftmargin=3.2em]")
    block_end = manual_text.index(r"\end{enumerate}", block_start)
    item_matches = list(re.finditer(r"(?m)^\\item\s", manual_text[block_start:block_end]))
    expected_manual = []
    for ordinal, match in enumerate(item_matches, start=1):
        start = block_start + match.start()
        end = block_start + item_matches[ordinal].start() if ordinal < len(item_matches) else block_end
        body = manual_text[start:end].rstrip() + "\n"
        start_line, end_line = line_interval(manual_text, start, end)
        expected_manual.append((
            f"P063-S60-MANREF-{ordinal:05d}", f"A{ordinal}",
            manual_source["source_id"], manual_path, manual_source["partition"],
            manual_source["git_blob"], start_line, end_line,
            sorted({normalize_doi(item.group(0)) for item in DOI_RE.finditer(body)}),
            digest(body.encode("utf-8")), body, None, None,
            manual_source["authority_ceiling"], LEXICAL_AUTHORITY_PROFILE_ID, True,
            False, False,
        ))
    manual_references = data["manual_unkeyed_bibliography_occurrences"]
    actual_manual = [(
        row["manual_reference_occurrence_id"], row["manual_label"], row["source_id"],
        row["path"], row["partition"], row["git_blob"], row["start_line"],
        row["end_line"], row["doi_values"], row["body_sha256"], row["body"],
        row["cite_key"], row["citation_route"], row["authority_ceiling"],
        row["authority_axis_profile_id"], row["authority_axes_assigned"],
        row["external_metadata_validated"], row["fulltext_proposition_validated"],
    ) for row in manual_references]
    if len(item_matches) != 5 or actual_manual != expected_manual:
        raise ValidationError("manual unkeyed bibliography replay mismatch")
    dois = data["doi_occurrences_all_text_partitions"]
    actual_dois = [(
        row["source_id"], row["path"], row["partition"], row["git_blob"],
        row["start_line"], row["end_line"], row["raw"], row["normalized"],
        row["line_text"], row["line_sha256"],
    ) for row in dois]
    if actual_dois != expected_dois:
        raise ValidationError("DOI occurrence replay mismatch")
    if any(row.get("resolver_validated_in_step60") is not False or row.get("proposition_support_validated") is not False for row in dois):
        raise ValidationError("DOI authority promotion")
    equations = data["equation_candidates_all_text_partitions"]
    actual_equations = [(
        row["source_id"], row["path"], row["partition"], row["git_blob"],
        row["start_line"], row["end_line"], row["ordinal_within_start_line"],
        row["start_column"], row["end_column"], row["environment"], row["labels"],
        row["body"],
        row["body_sha256"], row["authority_ceiling"],
    ) for row in equations]
    if actual_equations != expected_equations:
        raise ValidationError("equation candidate replay mismatch")
    validate_display_opener_coverage(equations, texts)
    if any(row.get("exact_equation_externally_validated") is not False for row in equations):
        raise ValidationError("equation authority promotion")
    if any(row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
           or row.get("authority_axes_assigned") is not True for row in equations):
        raise ValidationError("equation authority-axis assignment")
    tex_math = data["tex_delimited_math_candidates_all_text_partitions"]
    actual_tex_math = [(
        row["source_id"], row["path"], row["partition"], row["git_blob"],
        row["start_line"], row["end_line"], row["ordinal_within_start_line"],
        row["start_column"], row["end_column"], row["syntax"], row["body"],
        row["body_sha256"], row["authority_ceiling"],
    ) for row in tex_math]
    if actual_tex_math != expected_tex_math:
        raise ValidationError("TeX delimited math candidate replay mismatch")
    validate_dollar_endpoint_coverage(tex_math, texts)
    if any(row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
           or row.get("authority_axes_assigned") is not True
           or row.get("claim_occurrence_inventory_state")
           != "INVENTORIED_AUTHORITY_BOUNDED_NOT_SEMANTICALLY_NORMALIZED"
           or row.get("semantic_claim_adjudicated") is not False
           for row in tex_math):
        raise ValidationError("TeX delimited math authority-axis assignment")
    claims = data["claim_candidate_lines_all_text_partitions"]
    actual_claims = [(
        row["source_id"], row["path"], row["partition"], row["git_blob"],
        row["line"], row["candidate_kinds"], row["line_sha256"], row["text"],
        row["authority_ceiling"],
    ) for row in claims]
    if actual_claims != expected_claims:
        raise ValidationError("claim candidate replay mismatch")
    if any(row.get("semantic_claim_adjudicated") is not False for row in claims):
        raise ValidationError("lexical claim semantic promotion")
    if any(row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
           or row.get("authority_axes_assigned") is not True
           or row.get("claim_occurrence_inventory_state")
           != "INVENTORIED_AUTHORITY_BOUNDED_NOT_SEMANTICALLY_NORMALIZED"
           for row in claims):
        raise ValidationError("claim authority-axis assignment")
    if data.get("final_release_citation_genealogy") != topology.get("citation_genealogy"):
        raise ValidationError("final citation genealogy drift")


def contract_projection(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": data["gate"],
        "baseline_commit": data["baseline_commit"],
        "counts": copy.deepcopy(data["counts"]),
        "input_artifacts": copy.deepcopy(data["input_artifacts"]),
        "result_contract": copy.deepcopy(data["result_first_contract"]),
        "authority_profiles": copy.deepcopy(data["authority_axis_profiles"]),
        "manual_references": copy.deepcopy(data["manual_unkeyed_bibliography_occurrences"]),
        "bibliography": copy.deepcopy(data["bibliography_occurrences_all_text_partitions"]),
        "bibliography_conflicts": copy.deepcopy(data["bibliography_identity_conflicts"]),
        "manual": copy.deepcopy(data["manual_literature_scope_evidence"]),
        "authority": copy.deepcopy(data["authority_boundary"]),
        "finding_summary": copy.deepcopy(data["finding_summary"]),
    }


def contract_diagnostics(value: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    add(errors, value.get("gate") != GATE, "GATE")
    add(errors, value.get("baseline_commit") != BASELINE, "BASELINE")
    add(errors, value.get("counts") != EXPECTED_COUNTS, "COUNTS")
    add(errors, input_artifact_diagnostics(value.get("input_artifacts")), "INPUT_ARTIFACTS")
    result_contract = value.get("result_contract", {})
    add(errors, result_contract.get("containing_commit") != "PENDING_AT_PRECOMMIT_BY_DESIGN"
        or result_contract.get("persistence_claimed") is not False
        or result_contract.get("step61_blocked_until") != "PASS_P063_STEP60_PERSISTENCE",
        "RESULT_CONTRACT")
    profile = value.get("authority_profiles", {}).get(LEXICAL_AUTHORITY_PROFILE_ID, {})
    add(errors, profile.get("axis_states") != LEXICAL_AUTHORITY_PROFILE
        or profile.get("semantic_claim_adjudicated") is not False
        or profile.get("external_truth_promoted") is not False,
        "AUTHORITY_PROFILE")
    manual_references = value.get("manual_references", [])
    add(errors, not sequential_ids(
        manual_references, "manual_reference_occurrence_id", "P063-S60-MANREF-"
    ) or len(manual_references) != 5, "MANUAL_REFERENCE_IDS")
    required_manual = {
        "manual_reference_occurrence_id", "manual_label", "source_id", "path",
        "partition", "git_blob", "start_line", "end_line", "doi_values",
        "body_sha256", "body", "cite_key", "citation_route", "authority_ceiling",
        "authority_axis_profile_id", "authority_axes_assigned",
        "external_metadata_validated", "fulltext_proposition_validated",
    }
    add(errors, not isinstance(manual_references, list) or any(
        set(row) != required_manual or not row.get("body")
        or row.get("cite_key") is not None or row.get("citation_route") is not None
        or row.get("authority_axis_profile_id") != LEXICAL_AUTHORITY_PROFILE_ID
        or row.get("authority_axes_assigned") is not True
        or row.get("external_metadata_validated") is not False
        or row.get("fulltext_proposition_validated") is not False
        for row in manual_references
    ), "MANUAL_REFERENCE_SCHEMA")
    bibliography = value.get("bibliography", [])
    add(errors, not isinstance(bibliography, list)
        or value.get("bibliography_conflicts") != bibliography_conflicts(bibliography),
        "BIBLIOGRAPHY_CONFLICTS")
    manual = value.get("manual", {})
    add(errors, manual.get("evidence_id") != "P063-STEP60-LITERATURE-QUANTITY-SCOPE-AUTHORITY", "EVIDENCE_ID")
    add(errors, manual.get("inventory_summary") != EXPECTED_INVENTORY_SUMMARY, "INVENTORY_SUMMARY")
    literature = manual.get("literature_claims", [])
    materials = manual.get("material_scope_ledger", [])
    findings = manual.get("findings", [])
    add(errors, {row.get("claim_id") for row in literature} != LITERATURE_IDS, "LITERATURE_IDS")
    add(errors, {row.get("material_id") for row in materials} != MATERIAL_IDS, "MATERIAL_IDS")
    add(errors, {row.get("finding_id") for row in findings} != FINDING_IDS, "FINDING_IDS")
    add(errors, Counter(row.get("priority") for row in findings) != Counter({"P0": 6, "P1": 13, "P2": 7}), "FINDING_PRIORITIES")
    add(errors, any(row.get("external_truth_promoted") is not False for row in literature + materials + findings), "EXTERNAL_PROMOTION")
    errors.update(row_contract_errors(
        literature, materials, findings, MANUAL_REFERENCE_IDS,
    ))
    attestation = manual.get("semantic_review_attestation", {})
    add(errors, attestation.get("authority") != "INTERNAL_SEMANTIC_REVIEW_ATTESTATION_ONLY"
        or attestation.get("full_text_source_count") != 33
        or attestation.get("full_text_physical_lines") != 4134
        or len(attestation.get("full_text_rows", [])) != 33
        or attestation.get("additional_semantic_interval_count") != 11
        or attestation.get("additional_semantic_source_count") != 10
        or attestation.get("additional_semantic_unique_physical_lines") != 409
        or len(attestation.get("additional_semantic_intervals", [])) != 11
        or attestation.get("manual_evidence_anchor_count") != 52
        or attestation.get("manual_evidence_anchor_path_count") != 30
        or attestation.get("manual_evidence_coverage_state")
        != "ALL_52_ANCHORS_COVERED_BY_SEMANTIC_ATTESTATION"
        or attestation.get("partial_code_review", {}).get("unique_physical_lines") != 535,
        "SEMANTIC_ATTESTATION")
    lit = {row.get("claim_id"): row for row in literature}
    mat = {row.get("material_id"): row for row in materials}
    add(errors, lit.get("P063-S60-LIT-002", {}).get("current_state") != "UNVERIFIED_EXTERNAL", "LCO_BASIS")
    add(errors, lit.get("P063-S60-LIT-003", {}).get("current_state") != "GROUND_NOT_FOUND", "CHARGE_ORDER")
    add(errors, lit.get("P063-S60-LIT-007", {}).get("current_state") != "INTERNAL_REGRESSION_ONLY", "INTERNAL_RECORD")
    add(errors, lit.get("P063-S60-LIT-009", {}).get("current_state") != "CONFLICTING_REPOSITORY_METADATA", "METADATA_CONFLICT")
    add(errors, "3578.5567" not in mat.get("P063-S60-MAT-004", {}).get("quantity_basis", ""), "SI_STOICHIOMETRY")
    add(errors, mat.get("P063-S60-MAT-006", {}).get("state") != "BASIS_GROUND_NOT_FOUND", "SIC_BASIS")
    add(errors, mat.get("P063-S60-MAT-002", {}).get("state") != "GROUND_NOT_FOUND", "DOPED_SCOPE")
    add(errors, "placeholder" not in mat.get("P063-S60-MAT-005", {}).get("quantity_basis", ""), "SIOX_PLACEHOLDER")
    add(errors, any(not row.get("owner") or not row.get("acceptance") for row in literature if "GROUND_NOT_FOUND" in str(row.get("current_state"))), "GNF_ROUTING")
    authority = value.get("authority", {})
    add(errors, any(authority.get(key) is not False for key in FALSE_AUTHORITY_FLAGS), "AUTHORITY_FLAGS")
    add(errors, value.get("finding_summary") != {"P0": 6, "P1": 13, "P2": 7}, "FINDING_SUMMARY")
    return errors


def run_negative_probes(data: dict[str, Any]) -> tuple[int, int]:
    base = contract_projection(data)
    probes: list[tuple[str, Any, str]] = []

    def register(name: str, mutation: Any, code: str) -> None:
        probes.append((name, mutation, code))

    register("gate", lambda d: d.__setitem__("gate", "PASS"), "GATE")
    register("baseline", lambda d: d.__setitem__("baseline_commit", "0" * 40), "BASELINE")
    register("source_count", lambda d: d["counts"].__setitem__("all_reviewed_text_sources", 200), "COUNTS")
    register("manifest_lines", lambda d: d["counts"].__setitem__("manifest_physical_lines", 30218), "COUNTS")
    register("supplement_fusion", lambda d: d["counts"].__setitem__("manifest_text_sources", 201), "COUNTS")
    register("citation_count", lambda d: d["counts"].__setitem__("citation_key_occurrences", 769), "COUNTS")
    register("bibliography_count", lambda d: d["counts"].__setitem__("bibliography_occurrences", 90), "COUNTS")
    register("doi_count", lambda d: d["counts"].__setitem__("doi_occurrences", 327), "COUNTS")
    register("equation_count", lambda d: d["counts"].__setitem__("equation_candidates", 338), "COUNTS")
    register("tex_math_count", lambda d: d["counts"].__setitem__("tex_delimited_math_candidates", 14957), "COUNTS")
    register("claim_count", lambda d: d["counts"].__setitem__("claim_candidate_lines", 8750), "COUNTS")
    register("evidence_id", lambda d: d["manual"].__setitem__("evidence_id", "DRIFT"), "EVIDENCE_ID")
    register("inventory_summary", lambda d: d["manual"]["inventory_summary"].__setitem__("final_root_routes", 87), "INVENTORY_SUMMARY")
    register("literature_drop", lambda d: d["manual"]["literature_claims"].pop(), "LITERATURE_IDS")
    register("material_duplicate", lambda d: d["manual"]["material_scope_ledger"].__setitem__(11, copy.deepcopy(d["manual"]["material_scope_ledger"][10])), "MATERIAL_IDS")
    register("finding_id", lambda d: d["manual"]["findings"][0].__setitem__("finding_id", "DRIFT"), "FINDING_IDS")
    register("finding_priority", lambda d: d["manual"]["findings"][0].__setitem__("priority", "P2"), "FINDING_PRIORITIES")
    register("external_promotion", lambda d: d["manual"]["literature_claims"][0].__setitem__("external_truth_promoted", True), "EXTERNAL_PROMOTION")
    register("metadata_to_fulltext", lambda d: d["manual"]["literature_claims"][3].__setitem__("external_truth_promoted", True), "EXTERNAL_PROMOTION")
    register("abstract_to_quantity", lambda d: d["manual"]["literature_claims"][4].__setitem__("external_truth_promoted", True), "EXTERNAL_PROMOTION")
    register("lco_basis", lambda d: d["manual"]["literature_claims"][1].__setitem__("current_state", "VERIFIED"), "LCO_BASIS")
    register("charge_order", lambda d: d["manual"]["literature_claims"][2].__setitem__("current_state", "VERIFIED"), "CHARGE_ORDER")
    register("internal_numverif", lambda d: d["manual"]["literature_claims"][6].__setitem__("current_state", "EXTERNAL_PRIMARY"), "INTERNAL_RECORD")
    register("metadata_conflict", lambda d: d["manual"]["literature_claims"][8].__setitem__("current_state", "RESOLVED"), "METADATA_CONFLICT")
    register("si_stoichiometry", lambda d: d["manual"]["material_scope_ledger"][3].__setitem__("quantity_basis", "Li15Si4 equals 4200 mAh/g"), "SI_STOICHIOMETRY")
    register("sic_basis", lambda d: d["manual"]["material_scope_ledger"][5].__setitem__("state", "VERIFIED_Q_SI"), "SIC_BASIS")
    register("doped_scope", lambda d: d["manual"]["material_scope_ledger"][1].__setitem__("state", "VERIFIED_FROM_PRISTINE"), "DOPED_SCOPE")
    register("siox_placeholder", lambda d: d["manual"]["material_scope_ledger"][4].__setitem__("quantity_basis", "U=0.300 V verified"), "SIOX_PLACEHOLDER")
    register("authority_flag", lambda d: d["authority"].__setitem__("primary_literature_truth_validated", True), "AUTHORITY_FLAGS")
    register("finding_summary", lambda d: d.__setitem__("finding_summary", {"P0": 5, "P1": 14, "P2": 7}), "FINDING_SUMMARY")
    register("material_promotion", lambda d: d["manual"]["material_scope_ledger"][0].__setitem__("external_truth_promoted", True), "EXTERNAL_PROMOTION")
    register("input_artifact_hash", lambda d: d["input_artifacts"]["step58_topology"].__setitem__("raw_sha256", "0" * 64), "INPUT_ARTIFACTS")
    register("result_blocker", lambda d: d["result_contract"].__setitem__("step61_blocked_until", "PASS"), "RESULT_CONTRACT")
    register("authority_profile_axis", lambda d: d["authority_profiles"][LEXICAL_AUTHORITY_PROFILE_ID]["axis_states"].pop("fulltext_method"), "AUTHORITY_PROFILE")
    register("manual_reference_drop", lambda d: d["manual_references"].pop(), "MANUAL_REFERENCE_IDS")
    register("manual_reference_body", lambda d: d["manual_references"][0].__setitem__("body", ""), "MANUAL_REFERENCE_SCHEMA")
    register("bibliography_conflict", lambda d: d["bibliography_conflicts"]["same_key_variant_groups"].clear(), "BIBLIOGRAPHY_CONFLICTS")
    register("literature_empty_source", lambda d: d["manual"]["literature_claims"][0].__setitem__("source_evidence", []), "LITERATURE_SCHEMA")
    register("literature_axis_drop", lambda d: d["manual"]["literature_claims"][0]["axis_states"].pop("fulltext_method"), "LITERATURE_AXES")
    register("material_empty_owner", lambda d: d["manual"]["material_scope_ledger"][0].__setitem__("owner", ""), "MATERIAL_SCHEMA")
    register("finding_empty_refs", lambda d: d["manual"]["findings"][0].__setitem__("evidence_refs", []), "FINDING_SCHEMA")
    register("semantic_full_drop", lambda d: d["manual"]["semantic_review_attestation"]["full_text_rows"].pop(), "SEMANTIC_ATTESTATION")
    register("semantic_code_count", lambda d: d["manual"]["semantic_review_attestation"]["partial_code_review"].__setitem__("unique_physical_lines", 534), "SEMANTIC_ATTESTATION")
    register("semantic_interval_drop", lambda d: d["manual"]["semantic_review_attestation"]["additional_semantic_intervals"].pop(), "SEMANTIC_ATTESTATION")

    for name, mutation, expected in probes:
        candidate = copy.deepcopy(base)
        mutation(candidate)
        diagnostics = contract_diagnostics(candidate)
        if diagnostics != {expected}:
            raise ValidationError(
                f"negative {name}: expected {[expected]}, got {sorted(diagnostics)}"
            )
    artifact_probes: list[tuple[str, Any, str]] = [
        (
            "equation_axis_assignment",
            lambda d: d["equation_candidates_all_text_partitions"][0].__setitem__(
                "authority_axes_assigned", False
            ),
            "EQUATION_AXIS_ASSIGNMENT",
        ),
        (
            "equation_markdown_anchor",
            lambda d: next(
                row for row in d["equation_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "a691fb856f0bf656999401ec6c68515a6ba50b3f9229179fefa319b8c658a60f"
            ).__setitem__("body_sha256", "0" * 64),
            "EQUATION_REQUIRED_MARKDOWN_ANCHOR",
        ),
        (
            "equation_inline_bracket_anchor",
            lambda d: next(
                row for row in d["equation_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "8ce4c79f1aa3afe7750e059a6ab572556fe74f327a39c6341f8208f819fb9e84"
            ).__setitem__("body_sha256", "0" * 64),
            "EQUATION_INLINE_BRACKET_ANCHOR",
        ),
        (
            "equation_multiple_same_line",
            lambda d: [
                row.__setitem__("start_column", 59)
                for row in d["equation_candidates_all_text_partitions"]
                if row["path"] == "Claude/docs/v1.0.22/results/comp_FR/A15_REVIEW.md"
                and row["start_line"] == 23
                and row["ordinal_within_start_line"] == 2
            ],
            "EQUATION_MULTIPLE_SAME_LINE_OCCURRENCES",
        ),
        (
            "claim_axis_assignment",
            lambda d: d["claim_candidate_lines_all_text_partitions"][0].__setitem__(
                "authority_axis_profile_id", "DRIFT"
            ),
            "CLAIM_AXIS_ASSIGNMENT",
        ),
        (
            "tex_math_axis_assignment",
            lambda d: d["tex_delimited_math_candidates_all_text_partitions"][0].__setitem__(
                "authority_axes_assigned", False
            ),
            "TEX_MATH_AXIS_ASSIGNMENT",
        ),
        (
            "tex_math_required_anchor",
            lambda d: next(
                row for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "76df07d1b14aad45511a28e37346a640282e513c3da7b99611b7abb7cb391f2a"
            ).__setitem__("body_sha256", "0" * 64),
            "TEX_MATH_REQUIRED_ANCHOR",
        ),
        (
            "tex_math_multiline_anchor",
            lambda d: next(
                row for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "c349d2daba0415214a9dbd2ea231bca0644c85fa72437b13367069a34c7d7cd8"
            ).__setitem__("body_sha256", "0" * 64),
            "TEX_MATH_REQUIRED_ANCHOR",
        ),
        (
            "tex_math_adjacent_delimiter_anchor",
            lambda d: [
                row.__setitem__("body_sha256", "0" * 64)
                for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "ea219dfb1f7b0384bb69ecfd761f5f6fa3fb49322f7876e875d75cb4a94c791c"
            ],
            "TEX_MATH_REQUIRED_ANCHOR",
        ),
        (
            "tex_math_markdown_anchor",
            lambda d: [
                row.__setitem__("body_sha256", "0" * 64)
                for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "a6e1cea0c99116165c19408b0e12a7e561b2498fdac3f3f55bfb6a1a02c39b4a"
            ],
            "TEX_MATH_REQUIRED_ANCHOR",
        ),
        (
            "tex_math_markdown_recovery_anchor",
            lambda d: [
                row.__setitem__("body_sha256", "0" * 64)
                for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["path"] == "Claude/docs/v1.0.22/results/comp_FR/A05_REVIEW.md"
                and row["start_line"] == 54
                and row["body_sha256"]
                == "44c15fcc3206088522fbb5ab1f69696e2cac3a88a41406b0f099421195c8fbd0"
            ],
            "TEX_MATH_MARKDOWN_RECOVERY",
        ),
        (
            "tex_math_markdown_multiline_anchor",
            lambda d: next(
                row for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["body_sha256"]
                == "0558039300e30482ca401587a17a80dbd9d104be0304f9d971a82a9a0741087f"
            ).__setitem__("body_sha256", "0" * 64),
            "TEX_MATH_MARKDOWN_MULTILINE_RECOVERY",
        ),
        (
            "tex_math_unterminated_syntax",
            lambda d: next(
                row for row in d["tex_delimited_math_candidates_all_text_partitions"]
                if row["syntax"] == "UNTERMINATED_INLINE_DOLLAR"
            ).__setitem__("syntax", "INLINE_DOLLAR"),
            "TEX_MATH_SYNTAX_COUNTS",
        ),
    ]
    for name, mutation, expected in artifact_probes:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        candidate["semantic_sha256"] = digest(compact(semantic_projection(candidate)))
        diagnostics = artifact_diagnostics(candidate)
        if diagnostics != {expected}:
            raise ValidationError(
                f"negative {name}: expected {[expected]}, got {sorted(diagnostics)}"
            )
    coverage_candidate = copy.deepcopy(data)
    coverage_candidate["manual_literature_scope_evidence"]["literature_claims"][3][
        "source_evidence"
    ][1]["lines"] = [174, 179]
    try:
        validate_frozen_replay(coverage_candidate)
    except ValidationError as exc:
        if "outside semantic attestation" not in str(exc):
            raise ValidationError(f"negative semantic anchor coverage: {exc}") from exc
    else:
        raise ValidationError("negative semantic anchor coverage was accepted")
    topology, _ = strict_load(TOPOLOGY)
    endpoint_texts = {
        source["path"]: git_bytes("show", f"{BASELINE}:{source['path']}").decode(
            "utf-8", "strict"
        )
        for source in topology["sources"]
        if source["review_mode"] == "FULL_TEXT"
    }
    supplemental = topology["supplemental_process_control"]
    endpoint_texts[supplemental["path"]] = git_bytes(
        "show", f"{BASELINE}:{supplemental['path']}"
    ).decode("utf-8", "strict")
    endpoint_candidate = copy.deepcopy(data)
    endpoint_rows = endpoint_candidate["tex_delimited_math_candidates_all_text_partitions"]
    endpoint_rows.pop(next(
        index for index, row in enumerate(endpoint_rows)
        if row["path"].lower().endswith(".md")
        and row["syntax"] in {"UNPAIRED_INLINE_DOLLAR", "UNTERMINATED_INLINE_DOLLAR"}
    ))
    try:
        validate_dollar_endpoint_coverage(endpoint_rows, endpoint_texts)
    except ValidationError as exc:
        if "dollar endpoint coverage mismatch" not in str(exc):
            raise ValidationError(f"negative dollar endpoint coverage: {exc}") from exc
    else:
        raise ValidationError("negative dollar endpoint coverage was accepted")
    equation_candidate = copy.deepcopy(data)
    equation_rows = equation_candidate["equation_candidates_all_text_partitions"]
    equation_rows.pop(next(
        index for index, row in enumerate(equation_rows)
        if row["path"] == "Claude/docs/v1.0.22/results/comp_FR/A15_REVIEW.md"
        and row["start_line"] == 23
    ))
    try:
        validate_display_opener_coverage(equation_rows, endpoint_texts)
    except ValidationError as exc:
        if "display opener coverage mismatch" not in str(exc):
            raise ValidationError(f"negative display opener coverage: {exc}") from exc
    else:
        raise ValidationError("negative display opener coverage was accepted")
    total = len(probes) + len(artifact_probes) + 3
    return total, total


def strict_json_negative_probes() -> tuple[int, int]:
    fixtures = (
        '{"a":1,"a":2}',
        '{"a":NaN}',
        '{"a":Infinity}',
        '{"a":-Infinity}',
        '{"a":[1,2}',
    )
    for fixture in fixtures:
        try:
            strict_load_text(fixture)
        except (json.JSONDecodeError, ValidationError, ValueError):
            continue
        raise ValidationError(f"strict JSON accepted invalid fixture: {fixture}")
    return len(fixtures), len(fixtures)


def run_builder_once(directory: str) -> tuple[dict[str, Any], bytes, int]:
    proc = run([sys.executable, str(BUILDER), "--output-dir", directory])
    if proc.returncode:
        raise ValidationError(
            "builder failed: "
            + (proc.stdout + proc.stderr).decode("utf-8", errors="replace").strip()
        )
    path = Path(directory) / ARTIFACT.name
    value, nodes = strict_load(path)
    if not isinstance(value, dict):
        raise ValidationError("builder output root")
    return value, path.read_bytes(), nodes


def control_document_checks() -> None:
    paths = {
        "result": RESULT,
        "active_ledger": ACTIVE_LEDGER,
        "parent_ledger": PARENT_LEDGER,
        "handover": HANDOVER,
    }
    for key, path in paths.items():
        expected = CONTROL_SHA256[key]
        if expected == "PENDING" or not lf_only(path) or digest(path.read_bytes()) != expected:
            raise ValidationError(f"control document digest drift: {key}")
    result_text = RESULT.read_text(encoding="utf-8")
    if GATE not in result_text or "PENDING_AT_PRECOMMIT_BY_DESIGN" not in result_text:
        raise ValidationError("result gate/sentinel drift")
    for path in (ACTIVE_LEDGER, PARENT_LEDGER, HANDOVER):
        text = path.read_text(encoding="utf-8")
        if "Step 60" not in text or GATE not in text:
            raise ValidationError(f"Step 60 recovery marker missing: {path.name}")


def verify_branch_guards() -> None:
    errors = []
    if ref_hash(f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("protected local")
    if ref_hash(f"refs/remotes/origin/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("protected tracking")
    if remote_head(PROTECTED_BRANCH) != PROTECTED_TIP:
        errors.append("protected live")
    if ref_hash("refs/heads/main") is not None:
        errors.append("unexpected local main")
    if ref_hash("refs/remotes/origin/main") != MAIN_TIP or remote_head("main") != MAIN_TIP:
        errors.append("main drift")
    if git_paths("diff", "--name-only", "-z", BASELINE, "HEAD", "--", "Claude"):
        errors.append("Claude committed diff")
    if git_paths("diff", "--name-only", "-z", "--", "Claude"):
        errors.append("Claude worktree diff")
    if git_paths("diff", "--cached", "--name-only", "-z", "--", "Claude"):
        errors.append("Claude staged diff")
    if errors:
        raise ValidationError("branch guard drift: " + ", ".join(errors))


def verify_staged() -> str:
    if git_text("branch", "--show-current") != BRANCH:
        raise ValidationError("wrong branch")
    if git_text("rev-parse", "HEAD") != EXPECTED_PARENT:
        raise ValidationError("wrong precommit parent")
    if git_text("rev-parse", "@{upstream}") != EXPECTED_PARENT or remote_head(BRANCH) != EXPECTED_PARENT:
        raise ValidationError("upstream/live not at parent")
    staged = git_paths("diff", "--cached", "--name-only", "-z", "HEAD")
    if staged != EXACT_SEVEN_SET:
        raise ValidationError(f"staged path mismatch: {sorted(staged ^ EXACT_SEVEN_SET)}")
    unstaged = git_paths("diff", "--name-only", "-z")
    untracked = git_paths("ls-files", "--others", "--exclude-standard", "-z")
    if unstaged or untracked:
        raise ValidationError(f"unstaged/untracked paths remain: {sorted(unstaged | untracked)}")
    for path in EXACT_SEVEN:
        if git_bytes("show", f":{path}") != (REPO / path).read_bytes():
            raise ValidationError(f"staged/worktree byte mismatch: {path}")
    for args in (["git", "diff", "--check"], ["git", "diff", "--cached", "--check"]):
        proc = run(args)
        if proc.returncode:
            raise ValidationError(
                "staged whitespace check failed: "
                + (proc.stdout + proc.stderr).decode("utf-8", errors="replace").strip()
            )
    verify_branch_guards()
    return EXPECTED_PARENT


def verify_persistence(expected_commit: str | None) -> str:
    if not expected_commit or not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
        raise ValidationError("--expected-commit full hash required")
    if git_text("branch", "--show-current") != BRANCH:
        raise ValidationError("wrong branch")
    head = git_text("rev-parse", "HEAD")
    if head != expected_commit or git_text("rev-parse", "HEAD^") != EXPECTED_PARENT:
        raise ValidationError("local HEAD/parent mismatch")
    if git_text("show", "-s", "--format=%s", "HEAD") != SUBJECT:
        raise ValidationError("commit subject mismatch")
    if git_text("rev-parse", "@{upstream}") != head or remote_head(BRANCH) != head:
        raise ValidationError("upstream/live mismatch")
    changed = git_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD")
    if changed != EXACT_SEVEN_SET:
        raise ValidationError(f"commit path mismatch: {sorted(changed ^ EXACT_SEVEN_SET)}")
    if git_paths("status", "--porcelain=v1", "-z") or git_paths("diff", "--cached", "--name-only", "-z"):
        raise ValidationError("worktree/index not clean")
    for path in EXACT_SEVEN:
        if git_bytes("show", f"HEAD:{path}") != (REPO / path).read_bytes():
            raise ValidationError(f"commit/worktree byte mismatch: {path}")
    proc = run(["git", "diff", "--check", "HEAD^", "HEAD"])
    if proc.returncode:
        raise ValidationError(
            "commit whitespace check failed: "
            + (proc.stdout + proc.stderr).decode("utf-8", errors="replace").strip()
        )
    verify_branch_guards()
    return head


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if sum((args.content_only, args.verify_staged, args.verify_persistence)) != 1:
        print("select exactly one primary mode", file=sys.stderr)
        return 2
    try:
        if not ARTIFACT.is_file():
            raise ValidationError(
                f"E_ARTIFACT_MISSING: {ARTIFACT.relative_to(REPO).as_posix()}"
            )
        data, nodes = strict_load(ARTIFACT)
        if not isinstance(data, dict):
            raise ValidationError("artifact root not object")
        diagnostics = artifact_diagnostics(data)
        if diagnostics:
            raise ValidationError("artifact diagnostics: " + ", ".join(sorted(diagnostics)))
        validate_frozen_replay(data)
        control_document_checks()
        terminal = args.verify_staged or args.verify_persistence
        run_negative = args.run_negative_probes or terminal
        run_determinism = args.determinism_check or terminal
        negative = run_negative_probes(data) if run_negative else (0, 0)
        strict_negative = strict_json_negative_probes() if run_negative else (0, 0)
        determinism = (0, 0)
        if run_determinism:
            with tempfile.TemporaryDirectory(prefix="p063-step60-a-") as first, tempfile.TemporaryDirectory(prefix="p063-step60-b-") as second:
                first_data, first_raw, _ = run_builder_once(first)
                second_data, second_raw, _ = run_builder_once(second)
                if first_raw != second_raw or first_raw != ARTIFACT.read_bytes() or first_data != data or second_data != data:
                    raise ValidationError("builder determinism drift")
                determinism = (2, 2)
        suffix = (
            f"negative={negative[0]}/{negative[1]} "
            f"strict={strict_negative[0]}/{strict_negative[1]} "
            f"determinism={determinism[0]}/{determinism[1]} nodes={nodes}"
        )
        if args.verify_staged:
            print(f"PASS_P063_STEP60_STAGED parent={verify_staged()} paths=7/7 {suffix}")
        elif args.verify_persistence:
            print(f"PASS_P063_STEP60_PERSISTENCE head={verify_persistence(args.expected_commit)} paths=7/7 {suffix}")
        else:
            print(
                "PASS_P063_STEP60_CONTENT "
                f"sources={EXPECTED_COUNTS['all_reviewed_text_sources']} "
                f"claims={EXPECTED_COUNTS['claim_candidate_lines']} {suffix}"
            )
        return 0
    except (OSError, UnicodeError, ValueError, ValidationError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL_P063_STEP60: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
