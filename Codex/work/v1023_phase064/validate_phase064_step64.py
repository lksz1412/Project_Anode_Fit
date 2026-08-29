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
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "ea0438fcceec6e5fbc02805b3caf86e36732e35c"
EXPECTED_SUBJECT = "audit(phase064): freeze v1023 source process topology"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P064_STEP64_SOURCE_PROCESS"
PERSISTENCE = "PASS_P064_STEP64_PERSISTENCE"
EXPECTED_BUILDER_LF_SHA256 = "1e2684d509c42cbec6b502f9e43e663caecb629ef3935998ad1490c512bedb3e"
EXPECTED_RESULT_CONTRACT_SHA256 = "67b1b8f212b645b126a4adfabf50a69971162022f7857eccb0b1b1e2bda9ba6a"
EXPECTED_PARENT_LEDGER_LF_SHA256 = "c4010132b1fb5adfebc92194252316ed5ddbd005e30da5b6553bb49b8ab70ff4"
EXPECTED_ACTIVE_LEDGER_LF_SHA256 = "07652a343283e73b19a3db45f6ed04ac2a0deb3704cd8e0c92b1df1ba9494387"
EXPECTED_HANDOVER_LF_SHA256 = "68100fbd88f007646fce980ba0f5cfd3ce268298d327bca45cae5971a92ebeac"
EXPECTED_VALIDATOR_HASH_LINE_INDEX = 241

BUILDER_PATH = "Codex/work/v1023_phase064/build_phase064_step64_source_process_topology.py"
VALIDATOR_PATH = "Codex/work/v1023_phase064/validate_phase064_step64.py"
TOPOLOGY_PATH = "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION_PATH = "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
PLAN_PATH = "Codex/plans/2026-08-29-phase064-v1023-lineage-detailed-plan.md"

FINAL_PATHS = [
    BUILDER_PATH,
    VALIDATOR_PATH,
    TOPOLOGY_PATH,
    ATTESTATION_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_SET = set(FINAL_PATHS)
TOPOLOGY = ROOT / TOPOLOGY_PATH
ATTESTATION = ROOT / ATTESTATION_PATH
BUILDER = ROOT / BUILDER_PATH

PROCESS_COMMITS = [
    "9cb1ad900b6b170976fa41f31dd5a2ca8330b2d6",
    "63972cfc0af6ba232a361c3d96fcedc656f647d0",
    "d47d4dbb79fdaba284f15faca62ee9d6a280c3d8",
    "ee0371f74524460e908bb548d10e9592e1807fe9",
    "a722313ac19ece6bb72c87b7cd99e498fca25876",
    "3aa791aeb7357f23dbfb1d232277fd84276ca16b",
    "802673049bc54f0f11282af1334970042584229d",
    "ff840987a99348c092d3ab535c934ac7f303c5b1",
    "b6e51105341696ad97a5d5d6ec0c414c8bd0c62d",
    "4b781d31d31771ee6275805be8931c2a510df010",
    "4d56dc9f78a9aaf5d00e3479298371fde91a170e",
    "ce1e5e7e0b1407f6f5fd366bd30f3c9c8fa41bde",
    "ae6c967830d866e8b45e6087ba128b50790f2840",
    "1ad0e2c70ff213e2fc89ff77d50e74da25080d06",
]
PROCESS_STAGES = [
    "PLAN_INITIAL", "SURVEY_SYNTHESIS", "P0_BASELINE", "P1_PARTIAL", "PLAN_CORRECTION",
    "P1_CONDITION_GATE", "P2_APPENDIX", "P3_CODE", "P5_AUDIT", "P5_LEDGER", "CURVE_QA",
    "REF7_METADATA", "CODE_GUIDE", "REF6_METADATA_LATER",
]
STAGE_BY_COMMIT = dict(zip(PROCESS_COMMITS, PROCESS_STAGES))
OBSERVATION_PATHS = [
    "Codex/results/PHASE_057AA_V1023_P0_CONTROL_OBSERVATIONS.md",
    "Codex/results/PHASE_057AB_V1023_CONDITION_P1_OBSERVATIONS.md",
    "Codex/results/PHASE_057AC_V1023_P2_P3_OBSERVATIONS.md",
    "Codex/results/PHASE_057AD_V1023_P5_AUD_OBSERVATIONS.md",
    "Codex/results/PHASE_057AE_V1023_HANDOVER_MERGE_OBSERVATIONS.md",
    "Codex/results/PHASE_057AF_V1023_CURVE_CODEGUIDE_OBSERVATIONS.md",
]
PHASE057_READ_MAP = "Codex/plans/2026-07-28-phase057-v1023-read-map.md"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def token_profile(text: str) -> dict[str, int]:
    terms = {
        "fredholm": r"(?i)fredholm",
        "volterra": r"(?i)volterra",
        "ratio": r"(?i)ratio",
        "picard": r"(?i)picard",
        "transfer": r"(?i)transfer|전달함수",
        "omega": r"omega|\\omega|ω",
        "c_rate": r"(?i)c[- ]?rate|율속",
        "factor_3600": r"3600|3,600",
        "p4": r"(?<![A-Za-z0-9])P4(?![A-Za-z0-9])",
        "ref6_ref7": r"(?i)ref\.?\s*[67]|Ref\.6|Ref\.7",
        "code_implementation": r"(?i)code|function|class|api|코드|구현",
    }
    return {name: len(re.findall(pattern, text)) for name, pattern in terms.items()}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def reject_constant(value: str) -> Any:
    raise ValidationError(f"E_NONFINITE_JSON: {value}")


def finite_float(value: str) -> float:
    result = float(value)
    require(math.isfinite(result), "E_NONFINITE_JSON", value)
    return result


def bounded_int(value: str) -> int:
    require(len(value.lstrip("-")) <= 78, "E_INTEGER_RANGE", value[:80])
    result = int(value)
    require(abs(result) <= 2**256 - 1, "E_INTEGER_RANGE", value[:80])
    return result


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON", key)
        result[key] = value
    return result


def strict_load_bytes(raw: bytes, source: str) -> tuple[Any, dict[str, int]]:
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique_pairs,
            parse_constant=reject_constant,
            parse_float=finite_float,
            parse_int=bounded_int,
        )
    except (UnicodeError, json.JSONDecodeError, OverflowError) as error:
        raise ValidationError(f"E_STRICT_JSON: {source}") from error
    counts = {"containers": 0, "scalars": 0, "keys": 0, "max_depth": 0}

    def walk(node: Any, depth: int) -> None:
        counts["max_depth"] = max(counts["max_depth"], depth)
        if type(node) is dict:
            counts["containers"] += 1
            counts["keys"] += len(node)
            for child in node.values():
                walk(child, depth + 1)
        elif type(node) is list:
            counts["containers"] += 1
            for child in node:
                walk(child, depth + 1)
        else:
            counts["scalars"] += 1
            if type(node) is float:
                require(math.isfinite(node), "E_NONFINITE_JSON", source)

    walk(value, 0)
    counts["value_nodes"] = counts["containers"] + counts["scalars"]
    counts["all_nodes"] = counts["value_nodes"] + counts["keys"]
    return value, counts


def strict_load(path: pathlib.Path) -> tuple[dict[str, Any], dict[str, int], bytes]:
    raw = path.read_bytes()
    value, traversal = strict_load_bytes(raw, path.as_posix())
    require(type(value) is dict, "E_JSON_ROOT", path.as_posix())
    return value, traversal, raw


def run_process(
    args: list[str], *, cwd: pathlib.Path = ROOT, timeout: int = 300, check: bool = True
) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout, check=False)
    if check and process.returncode != 0:
        raise ValidationError(
            f"E_SUBPROCESS: {args!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}"
        )
    return process


def git(args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, check=check)


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT) -> str:
    return git(args, cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str) -> bytes:
    return git(["show", f"{commit}:{path}"]).stdout


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"], cwd=cwd).splitlines()
    require(len(lines) == 1, "E_LIVE_REF", branch)
    return lines[0].split("\t", 1)[0]


def expected_manifest_rows() -> list[dict[str, Any]]:
    manifest, _, _ = strict_load(ROOT / MANIFEST_PATH)
    rows = manifest.get("entries")
    require(type(rows) is list, "E_MANIFEST_SCHEMA")
    selected = rows[743:826]
    require(len(selected) == 83, "E_MANIFEST_SLICE")
    return selected


def _artifact_errors(topology: dict[str, Any], attestation: dict[str, Any]) -> set[str]:
    errors: set[str] = set()

    def add(condition: bool, code: str) -> None:
        if condition:
            errors.add(code)

    def exact_keys(value: Any, expected: set[str], code: str) -> None:
        add(type(value) is not dict or set(value) != expected, code)

    exact_keys(topology, {
        "schema_version", "artifact_kind", "phase", "step", "gate", "status", "frozen_commit",
        "manifest", "sources", "process", "phase057_observations", "builder_identity",
        "downstream_guardrails", "authority", "next_step", "semantic_sha256",
    }, "E_SCHEMA_TOP_ROOT")
    exact_keys(topology.get("manifest"), {
        "source_path", "source_sha256_lf", "strict_traversal", "indices", "sources", "paths",
        "unique_blobs", "bytes", "sorted_path_set_sha256", "review_modes", "roles", "text_lines",
        "pdf_pages", "image_occurrences",
    }, "E_SCHEMA_TOP_MANIFEST")
    exact_keys(topology.get("manifest", {}).get("strict_traversal"), {
        "containers", "scalars", "keys", "max_depth", "all_nodes",
    }, "E_SCHEMA_TOP_TRAVERSAL")
    exact_keys(topology.get("manifest", {}).get("review_modes"), {"FULL_TEXT", "FULL_PDF", "FULL_IMAGE"}, "E_SCHEMA_TOP_REVIEW_MODES")
    exact_keys(topology.get("manifest", {}).get("roles"), {"theory", "result", "generated_document", "figure", "code", "test", "implementation_guide", "supporting_document"}, "E_SCHEMA_TOP_ROLES")
    exact_keys(topology.get("builder_identity"), {"path", "sha256_raw", "execution_policy"}, "E_SCHEMA_BUILDER_IDENTITY")
    exact_keys(topology.get("authority"), {
        "internal_inventory_read_complete", "external_scientific", "external_material",
        "external_experimental", "primary_literature_ref6_ref7", "canonical_selection", "publication_ready",
    }, "E_SCHEMA_TOP_AUTHORITY")

    guardrails = topology.get("downstream_guardrails", {})
    exact_keys(guardrails, {"literature", "equations", "coordinates_units", "authority", "routing"}, "E_SCHEMA_GUARD_ROOT")
    exact_keys(guardrails.get("literature"), {
        "ref6_original_full_text", "ref7_original_full_text", "jcp147_substitute_for_ref6_ref7",
        "rejected_ref7_doi", "reference_ledger_equals_adopted_bibliography",
    }, "E_SCHEMA_GUARD_LITERATURE")
    exact_keys(guardrails.get("equations"), {
        "required_jcp_equation_anchors", "required_jcp_applicability_condition_count",
        "fredholm_volterra_same_problem", "algebraic_roots_promoted_to_integral_kernel",
        "first_ratio_picard_is_exact_or_general_convergence", "interaction_double_count_allowed",
    }, "E_SCHEMA_GUARD_EQUATIONS")
    exact_keys(guardrails.get("coordinates_units"), {
        "c_rate_factor_3600_state", "voltage_fourier_promoted_to_time_eis_instrument",
    }, "E_SCHEMA_GUARD_COORDINATES")
    exact_keys(guardrails.get("authority"), {
        "internal_gate_promoted_to_material_experimental", "positive_speedup_claimed", "speedup_benchmark_status",
    }, "E_SCHEMA_GUARD_AUTHORITY")
    exact_keys(guardrails.get("routing"), {
        "correction_owner", "acceptance_criterion", "ownerless_evidence_allowed",
    }, "E_SCHEMA_GUARD_ROUTING")

    exact_keys(attestation, {
        "schema_version", "artifact_kind", "phase", "step", "gate", "status", "frozen_commit", "sources",
        "partitions", "human_evidence", "human_evidence_semantic_sha256", "totals", "coverage_gap_count",
        "duplicate_route_count", "source_mutation_count", "human_attestation_complete", "authority", "semantic_sha256",
    }, "E_SCHEMA_ATT_ROOT")
    exact_keys(attestation.get("totals"), {
        "sources", "text_files", "text_lines", "pdf_files", "pdf_pages", "image_files", "image_occurrences",
    }, "E_SCHEMA_ATT_TOTALS")

    add(topology.get("schema_version") != "P064-STEP64-1", "E_TOP_SCHEMA")
    add(topology.get("artifact_kind") != "V1023_SOURCE_PROCESS_TOPOLOGY", "E_TOP_KIND")
    add(topology.get("gate") != GATE, "E_TOP_GATE")
    add(topology.get("frozen_commit") != BASELINE, "E_TOP_BASELINE")
    add(topology.get("status") != "PASS_INTERNAL_SOURCE_PROCESS_READ_COMPLETENESS", "E_TOP_STATUS")
    add(topology.get("phase") != "064" or topology.get("step") != "64", "E_TOP_PHASE_STEP")
    add(topology.get("next_step") != "Phase 064 Step 65 literature authority", "E_TOP_NEXT_STEP")
    add(attestation.get("schema_version") != "P064-STEP64-1", "E_ATT_SCHEMA")
    add(attestation.get("artifact_kind") != "V1023_READ_ATTESTATION", "E_ATT_KIND")
    add(attestation.get("gate") != GATE, "E_ATT_GATE")
    add(attestation.get("frozen_commit") != BASELINE, "E_ATT_BASELINE")
    add(attestation.get("status") != "READ_FULL", "E_ATT_STATUS")
    add(attestation.get("phase") != "064" or attestation.get("step") != "64", "E_ATT_PHASE_STEP")
    add(attestation.get("authority") != "INTERNAL_READ_COMPLETENESS_ONLY", "E_ATT_AUTHORITY")
    add(attestation.get("human_attestation_complete") is not True, "E_ATT_HUMAN_COMPLETE")

    sources = topology.get("sources")
    reads = attestation.get("sources")
    if type(sources) is not list or len(sources) != 83:
        errors.add("E_TOP_SOURCE_COUNT")
        return errors
    if type(reads) is not list or len(reads) != 83:
        errors.add("E_ATT_SOURCE_COUNT")
        return errors
    expected = expected_manifest_rows()
    expected_paths = [row["path"] for row in expected]
    _, expected_manifest_traversal, expected_manifest_raw = strict_load(ROOT / MANIFEST_PATH)
    expected_manifest_summary = {
        "source_path": MANIFEST_PATH,
        "source_sha256_lf": sha256(lf_bytes(expected_manifest_raw)),
        "strict_traversal": {key: value for key, value in expected_manifest_traversal.items() if key != "value_nodes"},
        "indices": [744, 826],
        "sources": 83,
        "paths": 83,
        "unique_blobs": 83,
        "bytes": 3_338_330,
        "sorted_path_set_sha256": sha256(canonical(sorted(expected_paths))),
        "review_modes": {"FULL_IMAGE": 2, "FULL_PDF": 3, "FULL_TEXT": 78},
        "roles": {"code": 1, "figure": 2, "generated_document": 3, "implementation_guide": 1, "result": 17, "supporting_document": 1, "test": 2, "theory": 56},
        "text_lines": 12_508,
        "pdf_pages": 129,
        "image_occurrences": 2,
    }
    add(topology.get("manifest") != expected_manifest_summary, "E_TOP_MANIFEST_SUMMARY")
    add([row.get("path") for row in sources] != expected_paths, "E_TOP_PATH_ORDER")
    add([row.get("path") for row in reads] != expected_paths, "E_ATT_PATH_ORDER")
    add(len({row.get("occurrence_id") for row in sources}) != 83, "E_TOP_SOURCE_IDS")
    add(len({row.get("blob_sha1") for row in sources}) != 83, "E_TOP_UNIQUE_BLOBS")
    add(sum(row.get("size_bytes", -1) for row in sources) != 3_338_330, "E_TOP_BYTES")
    add(Counter(row.get("review_mode") for row in sources) != {"FULL_TEXT": 78, "FULL_PDF": 3, "FULL_IMAGE": 2}, "E_TOP_MODES")
    add(Counter(row.get("role") for row in sources) != {"theory": 56, "result": 17, "generated_document": 3, "figure": 2, "code": 1, "test": 2, "implementation_guide": 1, "supporting_document": 1}, "E_TOP_ROLES")
    expected_path_hash = sha256(canonical(sorted(expected_paths)))
    add(topology.get("manifest", {}).get("sorted_path_set_sha256") != expected_path_hash, "E_TOP_PATH_SET_SHA")
    for index, (source, read, manifest) in enumerate(zip(sources, reads, expected), start=1):
        prefix = f"E_ROW_{index:03d}"
        source_keys = {
            "occurrence_id", "manifest_index", "path", "blob_sha1", "sha256_raw", "size_bytes", "role",
            "review_mode", "extent", "first_commit", "last_touch_commit", "last_touch_stage",
            "path_history_commit_count", "reader_partition", "full_read_state", "read_attestation_pointer",
            "human_evidence_pointer",
        }
        read_keys = {
            "occurrence_id", "path", "blob_sha1", "sha256_raw", "review_mode", "reader_partition", "reader",
            "read_state", "source_mutated", "coverage",
        }
        if manifest["review_mode"] == "FULL_TEXT":
            source_keys |= {"sha256_lf", "physical_lines", "nonblank_lines", "token_profile"}
            read_keys |= {"decode"}
        elif manifest["review_mode"] == "FULL_PDF":
            source_keys |= {"page_text_records", "extracted_text_nonempty_pages"}
            read_keys |= {"visual_review", "render_blank_pages", "render_failures"}
        else:
            source_keys |= {"observed_image_extent"}
            read_keys |= {"visual_review"}
        exact_keys(source, source_keys, prefix + "_SOURCE_SCHEMA")
        exact_keys(read, read_keys, prefix + "_READ_SCHEMA")
        exact_keys(source.get("extent"), set(manifest["extent"]), prefix + "_EXTENT_SCHEMA")
        add(source.get("occurrence_id") != f"V1023-SRC-{index:03d}", prefix + "_ID")
        add(source.get("manifest_index") != index + 743, prefix + "_MANIFEST_INDEX")
        add(source.get("path") != manifest["path"], prefix + "_PATH")
        add(source.get("blob_sha1") != manifest["blob_sha"], prefix + "_BLOB")
        add(source.get("size_bytes") != manifest["size_bytes"], prefix + "_SIZE")
        add(source.get("role") != manifest["role"], prefix + "_ROLE")
        add(source.get("review_mode") != manifest["review_mode"], prefix + "_MODE")
        add(source.get("extent") != manifest["extent"], prefix + "_EXTENT")
        add(read.get("occurrence_id") != source.get("occurrence_id"), prefix + "_READ_ID")
        add(read.get("path") != source.get("path"), prefix + "_READ_PATH")
        add(read.get("blob_sha1") != source.get("blob_sha1"), prefix + "_READ_BLOB")
        add(read.get("read_state") != "READ_FULL", prefix + "_READ_STATE")
        add(read.get("source_mutated") is not False, prefix + "_MUTATED")
        expected_partition = "A" if index <= 29 else "B" if index <= 57 else "C"
        expected_reader = {"A": "Kierkegaard", "B": "Leibniz", "C": "Singer"}[expected_partition]
        add(source.get("reader_partition") != expected_partition, prefix + "_TOP_PARTITION")
        add(read.get("reader_partition") != expected_partition, prefix + "_PARTITION")
        add(read.get("reader") != expected_reader, prefix + "_READER")
        add(source.get("full_read_state") != "READ_FULL", prefix + "_TOP_READ_STATE")
        add(source.get("read_attestation_pointer") != f"{ATTESTATION_PATH}#/sources/{index - 1}", prefix + "_READ_POINTER")
        expected_partition_index = ord(expected_partition) - ord("A")
        add(source.get("human_evidence_pointer") != f"{ATTESTATION_PATH}#/human_evidence/partitions/{expected_partition_index}", prefix + "_HUMAN_POINTER")
        if manifest["review_mode"] == "FULL_TEXT":
            lines = manifest["extent"]["lines"]
            exact_keys(source.get("token_profile"), {
                "fredholm", "volterra", "ratio", "picard", "transfer", "omega", "c_rate", "factor_3600",
                "p4", "ref6_ref7", "code_implementation",
            }, prefix + "_TOKEN_SCHEMA")
            exact_keys(read.get("coverage"), {"kind", "start", "end", "expected", "observed"}, prefix + "_COVERAGE_SCHEMA")
            add(read.get("coverage") != {"kind": "LINES", "start": 1, "end": lines, "expected": lines, "observed": lines}, prefix + "_TEXT_COVERAGE")
            add(read.get("decode") != "UTF-8", prefix + "_DECODE")
        elif manifest["review_mode"] == "FULL_PDF":
            pages = manifest["extent"]["pages"]
            exact_keys(read.get("coverage"), {"kind", "start", "end", "expected", "observed"}, prefix + "_COVERAGE_SCHEMA")
            add(read.get("coverage") != {"kind": "PAGES", "start": 1, "end": pages, "expected": pages, "observed": pages}, prefix + "_PDF_COVERAGE")
            add(read.get("visual_review") != "ALL_PAGES_RENDERED_AND_READ", prefix + "_PDF_VISUAL")
            add(source.get("extracted_text_nonempty_pages") != pages, prefix + "_PDF_TEXT_COUNT")
            page_records = source.get("page_text_records")
            if type(page_records) is list:
                for page_record in page_records:
                    exact_keys(page_record, {"page", "text_empty"}, prefix + "_PDF_TEXT_SCHEMA")
            add(
                type(page_records) is not list
                or [row.get("page") for row in page_records] != list(range(1, pages + 1))
                or any(row.get("text_empty") is not False for row in page_records),
                prefix + "_PDF_TEXT_RECORDS",
            )
        else:
            exact_keys(read.get("coverage"), {"kind", "occurrences", "observed"}, prefix + "_COVERAGE_SCHEMA")
            exact_keys(source.get("observed_image_extent"), set(manifest["extent"]), prefix + "_IMAGE_EXTENT_SCHEMA")
            add(read.get("coverage") != {"kind": "IMAGE", "occurrences": 1, "observed": 1}, prefix + "_IMAGE_COVERAGE")
            add(read.get("visual_review") != "ORIGINAL_RESOLUTION_READ", prefix + "_IMAGE_VISUAL")

    totals = attestation.get("totals", {})
    add(totals.get("sources") != 83, "E_ATT_TOTAL_SOURCES")
    add(totals.get("text_files") != 78 or totals.get("text_lines") != 12_508, "E_ATT_TOTAL_TEXT")
    add(totals.get("pdf_files") != 3 or totals.get("pdf_pages") != 129, "E_ATT_TOTAL_PDF")
    add(totals.get("image_files") != 2 or totals.get("image_occurrences") != 2, "E_ATT_TOTAL_IMAGE")
    add(attestation.get("coverage_gap_count") != 0, "E_ATT_GAPS")
    add(attestation.get("duplicate_route_count") != 0, "E_ATT_DUPLICATES")
    add(attestation.get("source_mutation_count") != 0, "E_ATT_MUTATION_COUNT")
    partitions = attestation.get("partitions")
    add(type(partitions) is not list or [(row.get("id"), row.get("source_count")) for row in partitions] != [("A", 29), ("B", 28), ("C", 26)], "E_ATT_PARTITIONS")
    if type(partitions) is list:
        for row in partitions:
            exact_keys(row, {"id", "reader", "source_count", "text_files", "text_lines", "pdf_files", "pdf_pages", "image_files", "status", "evidence"}, "E_SCHEMA_ATT_PARTITION")
        add([row.get("reader") for row in partitions] != ["Kierkegaard", "Leibniz", "Singer"], "E_ATT_PARTITION_READERS")
        add([row.get("status") for row in partitions] != ["READ_FULL", "READ_FULL", "READ_FULL"], "E_ATT_PARTITION_STATUS")
        add([(row.get("text_files"), row.get("text_lines"), row.get("pdf_files"), row.get("pdf_pages"), row.get("image_files")) for row in partitions] != [(29, 7057, 0, 0, 0), (28, 3158, 0, 0, 0), (21, 2293, 3, 129, 2)], "E_ATT_PARTITION_TOTALS")
        expected_partition_evidence = [
            {"coverage": "1-EOF for every UTF-8 text blob", "independent_blob_extent_errors": 0, "scope": "manifest local rows 1-29", "text_files": 29, "text_lines": 7057},
            {"coverage": "1-EOF for every UTF-8 text blob", "independent_blob_extent_errors": 0, "scope": "manifest local rows 30-57", "text_files": 28, "text_lines": 3158},
            {"coverage": "1-EOF text; every PDF page; both images at original resolution", "image_files": 2, "image_original_resolution_reads": 2, "independent_blob_extent_errors": 0, "pdf_blank_pages": 0, "pdf_files": 3, "pdf_pages": 129, "pdf_render_dpi": 110, "pdf_render_failures": 0, "pdf_rendered_page_images": 129, "scope": "manifest local rows 58-83", "text_files": 21, "text_lines": 2293},
        ]
        add([row.get("evidence") for row in partitions] != expected_partition_evidence, "E_ATT_PARTITION_EVIDENCE")
    human = attestation.get("human_evidence")
    add(type(human) is not dict, "E_HUMAN_EVIDENCE")
    if type(human) is dict:
        exact_keys(human, {"authority_ceiling", "coverage_gap_count", "evidence_date", "evidence_id", "evidence_kind", "image_reviews", "partitions", "pdf_reviews", "source_mutation_count"}, "E_SCHEMA_HUMAN_ROOT")
        add(human.get("evidence_id") != "P064-HUMAN-REVIEW-STEP64-001", "E_HUMAN_EVIDENCE_ID")
        add(human.get("coverage_gap_count") != 0, "E_HUMAN_EVIDENCE_GAPS")
        add(human.get("authority_ceiling") != "INTERNAL_HUMAN_READ_COMPLETENESS_ONLY_NOT_EXTERNAL_SCIENTIFIC_TRUTH", "E_HUMAN_AUTHORITY")
        add(human.get("evidence_date") != "2026-08-29" or human.get("evidence_kind") != "CONTROLLER_AGGREGATED_INDEPENDENT_FULL_READ", "E_HUMAN_METADATA")
        add(human.get("source_mutation_count") != 0, "E_HUMAN_MUTATION_COUNT")
        add([row.get("source_count") for row in human.get("partitions", [])] != [29, 28, 26], "E_HUMAN_EVIDENCE_PARTITIONS")
        add(sum(row.get("pages", -1) for row in human.get("pdf_reviews", [])) != 129, "E_HUMAN_EVIDENCE_PDF")
        add(len(human.get("image_reviews", [])) != 2, "E_HUMAN_EVIDENCE_IMAGE")
        add(attestation.get("human_evidence_semantic_sha256") != sha256(canonical(human)), "E_HUMAN_EVIDENCE_SHA")
        for row in human.get("partitions", []):
            exact_keys(row, {"coverage", "id", "image_files", "pdf_pages", "reader", "source_count", "text_binding_contract", "text_binding_sha256", "text_files", "text_lines"}, "E_SCHEMA_HUMAN_PARTITION")
        for row in human.get("pdf_reviews", []):
            exact_keys(row, {"blob_sha1", "human_visual_review", "page_interval", "pages", "path", "render_dpi", "render_engine", "render_failures", "sha256_raw"}, "E_SCHEMA_HUMAN_PDF")
        for row in human.get("image_reviews", []):
            exact_keys(row, {"blob_sha1", "extent", "human_visual_review", "path", "sha256_raw"}, "E_SCHEMA_HUMAN_IMAGE")
            exact_keys(row.get("extent"), {"format", "frames", "height", "mode", "width"}, "E_SCHEMA_HUMAN_IMAGE_EXTENT")
        expected_human_partitions = [
            ("A", "Kierkegaard", 29, 29, 7057, 0, 0),
            ("B", "Leibniz", 28, 28, 3158, 0, 0),
            ("C", "Singer", 26, 21, 2293, 129, 2),
        ]
        observed_human_partitions = [
            (row.get("id"), row.get("reader"), row.get("source_count"), row.get("text_files"), row.get("text_lines"), row.get("pdf_pages"), row.get("image_files"))
            for row in human.get("partitions", [])
        ]
        add(observed_human_partitions != expected_human_partitions, "E_HUMAN_PARTITION_IDENTITY")
        if type(sources) is list:
            for partition, evidence in zip(("A", "B", "C"), human.get("partitions", [])):
                binding_rows = [
                    {
                        "coverage": "1-EOF",
                        "occurrence_id": row["occurrence_id"],
                        "path": row["path"],
                        "blob_sha1": row["blob_sha1"],
                        "physical_lines": row["physical_lines"],
                    }
                    for row in sources
                    if row.get("reader_partition") == partition and row.get("review_mode") == "FULL_TEXT"
                ]
                add(evidence.get("text_binding_contract") != "ORDERED_OCCURRENCE_PATH_BLOB_LINES_COVERAGE", "E_HUMAN_TEXT_BINDING_CONTRACT")
                add(evidence.get("text_binding_sha256") != sha256(canonical(binding_rows)), "E_HUMAN_TEXT_BINDING")
        pdf_sources = [row for row in sources if row.get("review_mode") == "FULL_PDF"]
        expected_pdf_reviews = [
            {
                "blob_sha1": row["blob_sha1"],
                "human_visual_review": "ALL_PAGES_RENDERED_AND_READ",
                "page_interval": [1, row["extent"]["pages"]],
                "pages": row["extent"]["pages"],
                "path": row["path"],
                "render_dpi": 110,
                "render_engine": "POPPLER",
                "render_failures": 0,
                "sha256_raw": row["sha256_raw"],
            }
            for row in pdf_sources
        ]
        add(human.get("pdf_reviews") != expected_pdf_reviews, "E_HUMAN_PDF_IDENTITY")
        image_sources = [row for row in sources if row.get("review_mode") == "FULL_IMAGE"]
        expected_image_reviews = [
            {
                "blob_sha1": row["blob_sha1"],
                "extent": row["extent"],
                "human_visual_review": "ORIGINAL_RESOLUTION_READ",
                "path": row["path"],
                "sha256_raw": row["sha256_raw"],
            }
            for row in image_sources
        ]
        add(human.get("image_reviews") != expected_image_reviews, "E_HUMAN_IMAGE_IDENTITY")

    process = topology.get("process", {})
    exact_keys(process, {"commits", "commit_count", "phase_states", "p4_state", "p4_result_present", "p0_result_present", "reference_ledger_role", "adopted_bibliography_path"}, "E_SCHEMA_PROCESS_ROOT")
    exact_keys(process.get("phase_states"), {"P0", "P1", "P2", "P3", "P4", "P5"}, "E_SCHEMA_PROCESS_STATES")
    commits = process.get("commits")
    if type(commits) is list:
        for row in commits:
            exact_keys(row, {"stage", "commit", "parents", "subject", "author_time", "committer_time", "changed_v1023_paths"}, "E_SCHEMA_PROCESS_COMMIT")
    add(type(commits) is not list or [row.get("commit") for row in commits] != PROCESS_COMMITS, "E_PROCESS_COMMITS")
    add(process.get("commit_count") != 14, "E_PROCESS_COMMIT_COUNT")
    add(process.get("phase_states") != {"P0": "COMMIT_LEDGER_EVIDENCE", "P1": "EXECUTED", "P2": "EXECUTED", "P3": "EXECUTED", "P4": "SKIPPED_D3_NOT_APPROVED", "P5": "EXECUTED"}, "E_PROCESS_PHASE_STATES")
    add(process.get("p4_state") != "SKIPPED_D3_NOT_APPROVED", "E_PROCESS_P4_STATE")
    add(process.get("p4_result_present") is not False, "E_PROCESS_P4_RESULT")
    add(process.get("p0_result_present") is not False, "E_PROCESS_P0_RESULT")
    add(process.get("reference_ledger_role") != "INHERITED_PARTIAL_LEDGER_NOT_ADOPTED_BIBLIOGRAPHY_INVENTORY", "E_PROCESS_REFERENCE_LEDGER_ROLE")
    add(process.get("adopted_bibliography_path") != "Claude/docs/v1.0.23/_sections/ch1v22_bib.tex", "E_PROCESS_ADOPTED_BIBLIOGRAPHY")
    observations = topology.get("phase057_observations", {})
    exact_keys(observations, {"count", "records", "source_records", "read_map", "authority"}, "E_SCHEMA_OBSERVATION_ROOT")
    exact_keys(observations.get("read_map"), {"path", "physical_lines", "sha256_lf"}, "E_SCHEMA_OBSERVATION_READ_MAP")
    records = observations.get("records")
    add(observations.get("authority") != "PROVISIONAL_ROUTING_INPUT_ONLY", "E_OBSERVATION_ROOT_AUTHORITY")
    add(type(records) is not list or len(records) != 36, "E_OBSERVATION_COUNT")
    if type(records) is list:
        for row in records:
            exact_keys(row, {"id", "title", "source_path", "source_line", "authority", "step64_disposition", "downstream_owner"}, "E_SCHEMA_OBSERVATION_RECORD")
        add([row.get("id") for row in records] != [f"INTENT-PROV-{number:04d}" for number in range(192, 228)], "E_OBSERVATION_IDS")
        add(any(row.get("authority") != "PROVISIONAL_ROUTING_INPUT" for row in records), "E_OBSERVATION_AUTHORITY")
    for row in observations.get("source_records", []):
        exact_keys(row, {"path", "physical_lines", "sha256_lf"}, "E_SCHEMA_OBSERVATION_SOURCE")
    authority = topology.get("authority", {})
    add(authority.get("internal_inventory_read_complete") is not True, "E_AUTH_INTERNAL")
    for key in ("external_scientific", "external_material", "external_experimental", "primary_literature_ref6_ref7", "canonical_selection", "publication_ready"):
        add(authority.get(key) is not False, "E_AUTH_" + key.upper())

    builder_identity = topology.get("builder_identity", {})
    add(builder_identity.get("path") != BUILDER_PATH, "E_BUILDER_IDENTITY_PATH")
    add(builder_identity.get("sha256_raw") != sha256(BUILDER.read_bytes()), "E_BUILDER_IDENTITY_SHA")
    add(builder_identity.get("execution_policy") != "DECLARED_GIT_READS_ONLY_NO_FROZEN_PRODUCTION_IMPORT", "E_BUILDER_IDENTITY_POLICY")

    literature = guardrails.get("literature", {})
    add(literature.get("ref6_original_full_text") != "GROUND_NOT_FOUND", "E_GUARD_REF6")
    add(literature.get("ref7_original_full_text") != "GROUND_NOT_FOUND", "E_GUARD_REF7")
    add(literature.get("jcp147_substitute_for_ref6_ref7") is not False, "E_GUARD_JCP_SUBSTITUTE")
    add(literature.get("rejected_ref7_doi") != "10.1063/1.4802005", "E_GUARD_REF7_DOI")
    add(literature.get("reference_ledger_equals_adopted_bibliography") is not False, "E_GUARD_BIB_CONFLATION")
    equations = guardrails.get("equations", {})
    add(equations.get("required_jcp_equation_anchors") != [32, 33, 34, 37, 39], "E_GUARD_EQ_ANCHORS")
    add(equations.get("required_jcp_applicability_condition_count") != 3, "E_GUARD_JCP_CONDITIONS")
    add(equations.get("fredholm_volterra_same_problem") is not False, "E_GUARD_FREDHOLM_VOLTERRA")
    add(equations.get("algebraic_roots_promoted_to_integral_kernel") is not False, "E_GUARD_ALGEBRAIC_KERNEL")
    add(equations.get("first_ratio_picard_is_exact_or_general_convergence") is not False, "E_GUARD_PICARD_EXACT")
    add(equations.get("interaction_double_count_allowed") is not False, "E_GUARD_DOUBLE_COUNT")
    coordinates = guardrails.get("coordinates_units", {})
    add(coordinates.get("c_rate_factor_3600_state") != "OPEN_MUST_RESOLVE_BEFORE_REGIME_APPROVAL", "E_GUARD_C_RATE_3600")
    add(coordinates.get("voltage_fourier_promoted_to_time_eis_instrument") is not False, "E_GUARD_VOLTAGE_COORDINATE")
    guard_authority = guardrails.get("authority", {})
    add(guard_authority.get("internal_gate_promoted_to_material_experimental") is not False, "E_GUARD_EXTERNAL_PROMOTION")
    add(guard_authority.get("positive_speedup_claimed") is not False, "E_GUARD_SPEEDUP_CLAIM")
    add(guard_authority.get("speedup_benchmark_status") != "NOT_YET_BENCHMARKED", "E_GUARD_SPEEDUP_STATUS")
    routing = guardrails.get("routing", {})
    add(routing.get("correction_owner") != "Phase 064 Step 69.1", "E_GUARD_OWNER")
    add(routing.get("acceptance_criterion") != "LOSSLESS_OWNER_COMPLETE_DISPOSITION", "E_GUARD_ACCEPTANCE")
    add(routing.get("ownerless_evidence_allowed") is not False, "E_GUARD_OWNERLESS")

    top_semantic = topology.get("semantic_sha256")
    top_projection = copy.deepcopy(topology)
    top_projection.pop("semantic_sha256", None)
    add(top_semantic != sha256(canonical(top_projection)), "E_TOP_SEMANTIC_SHA")
    att_semantic = attestation.get("semantic_sha256")
    att_projection = copy.deepcopy(attestation)
    att_projection.pop("semantic_sha256", None)
    add(att_semantic != sha256(canonical(att_projection)), "E_ATT_SEMANTIC_SHA")
    return errors


def artifact_errors(topology: dict[str, Any], attestation: dict[str, Any]) -> set[str]:
    try:
        return _artifact_errors(topology, attestation)
    except (AttributeError, IndexError, KeyError, TypeError):
        return {"E_SCHEMA_STRUCTURE"}


def independent_frozen_errors(topology: dict[str, Any], attestation: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    expected = expected_manifest_rows()
    for index, manifest in enumerate(expected):
        source = topology["sources"][index]
        read = attestation["sources"][index]
        path = manifest["path"]
        blob = git_text(["rev-parse", f"{BASELINE}:{path}"])
        raw = git_blob(BASELINE, path)
        history = git_text(["log", "--format=%H", "--reverse", BASELINE, "--", path]).splitlines()
        if blob != manifest["blob_sha"] or source["blob_sha1"] != blob:
            errors.add(f"E_INDEPENDENT_BLOB_{index + 1:03d}")
        if len(raw) != manifest["size_bytes"] or source["sha256_raw"] != sha256(raw) or read["sha256_raw"] != sha256(raw):
            errors.add(f"E_INDEPENDENT_BYTES_{index + 1:03d}")
        if (
            not history
            or source.get("first_commit") != history[0]
            or source.get("last_touch_commit") != history[-1]
            or source.get("path_history_commit_count") != len(history)
            or source.get("last_touch_stage") != STAGE_BY_COMMIT.get(history[-1], "OTHER_ANCESTOR")
        ):
            errors.add(f"E_INDEPENDENT_HISTORY_{index + 1:03d}")
        if manifest["review_mode"] == "FULL_TEXT":
            try:
                text = raw.decode("utf-8")
                text_lines = text.splitlines()
                lines = len(text_lines)
            except UnicodeDecodeError:
                errors.add(f"E_INDEPENDENT_DECODE_{index + 1:03d}")
                continue
            if lines != manifest["extent"]["lines"]:
                errors.add(f"E_INDEPENDENT_LINES_{index + 1:03d}")
            if source.get("sha256_lf") != sha256(lf_bytes(raw)):
                errors.add(f"E_INDEPENDENT_TEXT_HASH_{index + 1:03d}")
            if source.get("nonblank_lines") != sum(bool(line.strip()) for line in text_lines) or source.get("token_profile") != token_profile(text):
                errors.add(f"E_INDEPENDENT_TEXT_PROFILE_{index + 1:03d}")
        elif manifest["review_mode"] == "FULL_PDF":
            import io

            reader = PdfReader(io.BytesIO(raw), strict=True)
            if len(reader.pages) != manifest["extent"]["pages"] or bool(reader.is_encrypted) != manifest["extent"]["encrypted"]:
                errors.add(f"E_INDEPENDENT_PDF_{index + 1:03d}")
            page_records = [
                {"page": page_number, "text_empty": not bool((page.extract_text() or "").strip())}
                for page_number, page in enumerate(reader.pages, start=1)
            ]
            if source.get("page_text_records") != page_records or source.get("extracted_text_nonempty_pages") != sum(not row["text_empty"] for row in page_records):
                errors.add(f"E_INDEPENDENT_PDF_TEXT_{index + 1:03d}")
        else:
            import io

            with Image.open(io.BytesIO(raw)) as image:
                extent = {"width": image.width, "height": image.height, "mode": image.mode, "format": image.format, "frames": image.n_frames}
            if extent != manifest["extent"]:
                errors.add(f"E_INDEPENDENT_IMAGE_{index + 1:03d}")
            if source.get("observed_image_extent") != extent:
                errors.add(f"E_INDEPENDENT_IMAGE_RECORD_{index + 1:03d}")

    process_rows = topology.get("process", {}).get("commits", [])
    for index, (stage, commit) in enumerate(zip(PROCESS_STAGES, PROCESS_COMMITS)):
        if index >= len(process_rows):
            errors.add("E_INDEPENDENT_PROCESS_COUNT")
            break
        row = process_rows[index]
        changed = git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--", "Claude/docs/v1.0.23"])
        expected_row = {
            "stage": stage,
            "commit": commit,
            "parents": git_text(["show", "-s", "--format=%P", commit]).split(),
            "subject": git_text(["show", "-s", "--format=%s", commit]),
            "author_time": git_text(["show", "-s", "--format=%aI", commit]),
            "committer_time": git_text(["show", "-s", "--format=%cI", commit]),
            "changed_v1023_paths": changed.splitlines() if changed else [],
        }
        if row != expected_row:
            errors.add(f"E_INDEPENDENT_PROCESS_{index + 1:02d}")

    observation_records: list[dict[str, Any]] = []
    observation_sources: list[dict[str, Any]] = []
    pattern = re.compile(r"^### (INTENT-PROV-\d{4}) — (.+)$")
    for path in OBSERVATION_PATHS:
        raw = (ROOT / path).read_bytes()
        lines = raw.decode("utf-8").splitlines()
        observation_sources.append({"path": path, "physical_lines": len(lines), "sha256_lf": sha256(lf_bytes(raw))})
        for line_number, line in enumerate(lines, start=1):
            match = pattern.match(line)
            if match:
                observation_records.append({
                    "id": match.group(1),
                    "title": match.group(2),
                    "source_path": path,
                    "source_line": line_number,
                    "authority": "PROVISIONAL_ROUTING_INPUT",
                    "step64_disposition": "ROUTE_WITHOUT_PROMOTION",
                    "downstream_owner": "Phase 064 Step 69.1",
                })
    observations = topology.get("phase057_observations", {})
    if observations.get("records") != observation_records or observations.get("source_records") != observation_sources:
        errors.add("E_INDEPENDENT_OBSERVATIONS")
    read_map_raw = (ROOT / PHASE057_READ_MAP).read_bytes()
    expected_read_map = {
        "path": PHASE057_READ_MAP,
        "physical_lines": len(read_map_raw.decode("utf-8").splitlines()),
        "sha256_lf": sha256(lf_bytes(read_map_raw)),
    }
    if observations.get("read_map") != expected_read_map:
        errors.add("E_INDEPENDENT_READ_MAP")
    return errors


def control_document_errors(texts: dict[str, str]) -> set[str]:
    errors: set[str] = set()
    result_text_lf = texts["result"].replace("\r\n", "\n").replace("\r", "\n")
    result_lines = result_text_lf.split("\n")
    live_validator_hash_line = f"- validator raw SHA-256: `{sha256((ROOT / VALIDATOR_PATH).read_bytes())}`."
    result_projection_lines = list(result_lines)
    if (
        len(result_projection_lines) > EXPECTED_VALIDATOR_HASH_LINE_INDEX
        and result_projection_lines[EXPECTED_VALIDATOR_HASH_LINE_INDEX] == live_validator_hash_line
    ):
        result_projection_lines[EXPECTED_VALIDATOR_HASH_LINE_INDEX] = "- validator raw SHA-256: `<VALIDATOR_RAW_SHA256>`."
    result_projection = "\n".join(result_projection_lines).encode("utf-8")
    if sha256(result_projection) != EXPECTED_RESULT_CONTRACT_SHA256:
        errors.add("E_CONTROL_RESULT_IDENTITY")
    control_identities = {
        "parent": (EXPECTED_PARENT_LEDGER_LF_SHA256, "E_CONTROL_PARENT_IDENTITY"),
        "active": (EXPECTED_ACTIVE_LEDGER_LF_SHA256, "E_CONTROL_ACTIVE_IDENTITY"),
        "handover": (EXPECTED_HANDOVER_LF_SHA256, "E_CONTROL_HANDOVER_IDENTITY"),
    }
    for name, (expected_hash, code) in control_identities.items():
        if sha256(lf_bytes(texts[name].encode("utf-8"))) != expected_hash:
            errors.add(code)
    if not result_lines or result_lines[0] != "# Phase 064 Step 64 Source/Process Topology Result":
        errors.add("E_CONTROL_RESULT_H1")
    required_result = [
        "Status: `PASS_PENDING_PERSISTENCE`",
        f"Gate: `{GATE}`",
        "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        f"Expected parent: `{EXPECTED_PARENT}`",
        f"Expected subject: `{EXPECTED_SUBJECT}`",
        f"Postcommit persistence terminal: `{PERSISTENCE}`",
    ]
    for line in required_result:
        if result_lines.count(line) != 1:
            errors.add("E_CONTROL_RESULT_FIELDS")
    result_declarations = {
        r"^(?:overall\s+)?status\s*:": required_result[0],
        r"^gate\s*:": required_result[1],
        r"^(?:containing\s+)?commit\s*:": required_result[2],
        r"^expected\s+parent\s*:": required_result[3],
        r"^expected\s+subject\s*:": required_result[4],
        r"^(?:postcommit\s+)?persistence(?:\s+terminal)?\s*:": required_result[5],
    }

    def normalized_declaration_line(line: str) -> str:
        normalized = re.sub(r"^[\s#>*+\-]+", "", line)
        normalized = normalized.replace("**", "").replace("__", "").replace("`", "")
        return re.sub(r"\s+", " ", normalized).strip()

    for pattern, expected in result_declarations.items():
        declarations = [
            line for line in result_lines
            if re.search(pattern, normalized_declaration_line(line), flags=re.IGNORECASE)
        ]
        if declarations != [expected]:
            errors.add("E_CONTROL_RESULT_DECLARATIONS")
    topology, _, top_raw = strict_load(TOPOLOGY)
    attestation, _, att_raw = strict_load(ATTESTATION)
    required_hash_lines = [
        f"- sorted path-set SHA-256: `{topology.get('manifest', {}).get('sorted_path_set_sha256', '')}`.",
        f"- topology raw SHA-256: `{sha256(top_raw)}`.",
        f"- topology semantic SHA-256: `{topology.get('semantic_sha256', '')}`.",
        f"- attestation raw SHA-256: `{sha256(att_raw)}`.",
        f"- attestation semantic SHA-256: `{attestation.get('semantic_sha256', '')}`.",
        f"- result-first human evidence semantic SHA-256: `{attestation.get('human_evidence_semantic_sha256', '')}`.",
        f"- builder raw SHA-256: `{sha256(BUILDER.read_bytes())}`.",
        f"- validator raw SHA-256: `{sha256((ROOT / VALIDATOR_PATH).read_bytes())}`.",
    ]
    if any(result_lines.count(line) != 1 for line in required_hash_lines):
        errors.add("E_CONTROL_RESULT_HASH_LABELS")

    def step64_control_rows(text: str) -> list[str]:
        rows: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if not cells:
                continue
            label = cells[0]
            if re.fullmatch(r"0*64", label) or re.search(r"(?i)\bstep\s*0*64\b", label):
                rows.append(stripped)
        return rows

    def step64_prose_claims(text: str) -> list[str]:
        claims: list[str] = []
        pattern = re.compile(
            r"^(?:phase\s*0*64\s+)?step\s*0*64\s+(?:is\s+)?(?:status|complete(?:d)?|pass(?:ed)?|persistence|commit)\b",
            flags=re.IGNORECASE,
        )
        for line in text.splitlines():
            if line.strip().startswith("|"):
                continue
            if pattern.search(normalized_declaration_line(line)):
                claims.append(line)
        return claims

    if step64_prose_claims(texts["result"]):
        errors.add("E_CONTROL_RESULT_DECLARATIONS")

    required_tokens = ("Step 64", GATE, EXPECTED_PARENT, EXPECTED_SUBJECT, PERSISTENCE, "PENDING_AT_PRECOMMIT_BY_DESIGN")
    parent_rows = [line.strip() for line in texts["parent"].splitlines() if line.strip().startswith("| 064 |")]
    if len(parent_rows) != 1 or len(step64_control_rows(texts["parent"])) != 1 or step64_prose_claims(texts["parent"]) or "| IN_PROGRESS |" not in parent_rows[0] or any(token not in parent_rows[0] for token in required_tokens):
        errors.add("E_CONTROL_PARENT_ROW")
    active_phase_rows = [line.strip() for line in texts["active"].splitlines() if line.strip().startswith("| 064 |")]
    if len(active_phase_rows) != 1 or len(step64_control_rows(texts["active"])) != 2 or step64_prose_claims(texts["active"]) or "| IN_PROGRESS |" not in active_phase_rows[0] or any(token not in active_phase_rows[0] for token in required_tokens):
        errors.add("E_CONTROL_ACTIVE_PHASE_ROW")
    active_step_rows = [line.strip() for line in texts["active"].splitlines() if line.strip().startswith("| Step 64 |")]
    if len(active_step_rows) != 1 or any(token not in active_step_rows[0] for token in required_tokens[1:]):
        errors.add("E_CONTROL_ACTIVE_STEP_ROW")
    handover_lines = texts["handover"].splitlines()
    expected_current = "15. 현재 Phase 상태: Phase 064 `IN_PROGRESS`, Current checkpoint: Step 64 `PASS_P064_STEP64_SOURCE_PROCESS` pending persistence"
    expected_result = f"16. 현재 result: `{RESULT_PATH}`"
    expected_machine = f"17. 현재 machine evidence: `{TOPOLOGY_PATH}`; `{ATTESTATION_PATH}`"
    for line in (expected_current, expected_result, expected_machine):
        if handover_lines.count(line) != 1:
            errors.add("E_CONTROL_HANDOVER_CURRENT")
    handover_rows = [line.strip() for line in handover_lines if line.strip().startswith("| Phase 064 Step 64 |")]
    if len(handover_rows) != 1 or len(step64_control_rows(texts["handover"])) != 1 or step64_prose_claims(texts["handover"]) or any(token not in handover_rows[0] for token in required_tokens):
        errors.add("E_CONTROL_HANDOVER_ROW")
    next_sections = texts["handover"].split("## Exact Next Action")
    if len(next_sections) != 2 or any(token not in next_sections[1] for token in (EXPECTED_PARENT, EXPECTED_SUBJECT, PERSISTENCE, "Step 65")):
        errors.add("E_CONTROL_HANDOVER_NEXT")
    for name, text in texts.items():
        if "PLAN_ACTIVATION_PENDING_PERSISTENCE" in text or "Overall gate: FAIL" in text or "FAIL_P064_STEP64" in text or "Status: `FAIL`" in text:
            errors.add("E_CONTROL_CONTRADICTION_" + name.upper())
    return errors


def control_errors() -> set[str]:
    errors: set[str] = set()
    controls = {
        "result": RESULT_PATH,
        "parent": PARENT_LEDGER_PATH,
        "active": ACTIVE_LEDGER_PATH,
        "handover": HANDOVER_PATH,
    }
    texts: dict[str, str] = {}
    for name, path in controls.items():
        target = ROOT / path
        if not target.is_file():
            errors.add("E_CONTROL_MISSING_" + name.upper())
        else:
            texts[name] = target.read_text(encoding="utf-8")
    if len(texts) == 4:
        errors.update(control_document_errors(texts))
    return errors


def source_policy_errors(source: str | None = None) -> set[str]:
    errors: set[str] = set()
    source = BUILDER.read_text(encoding="utf-8") if source is None else source
    if sha256(lf_bytes(source.encode("utf-8"))) != EXPECTED_BUILDER_LF_SHA256:
        errors.add("E_BUILDER_SOURCE_IDENTITY")
    try:
        tree = ast.parse(source, filename=BUILDER_PATH)
    except SyntaxError:
        errors.add("E_BUILDER_SYNTAX")
        return errors
    allowed_imports = {"__future__", "argparse", "copy", "hashlib", "io", "json", "math", "pathlib", "re", "subprocess", "collections", "typing", "PIL", "pypdf"}
    write_methods = {"write_text", "write_bytes", "rename", "unlink", "rmdir", "mkdir", "touch"}
    allowed_writes = {"atomic_write": {"write_bytes", "mkdir"}, "output_paths": {"mkdir"}}
    subprocess_calls = 0
    run_process_calls = 0
    atomic_write_calls = 0

    sensitive_names = {
        "atomic_write", "compile", "eval", "exec", "getattr", "globals", "locals",
        "open", "run_process", "setattr", "vars", "__import__",
    }
    sensitive_attributes = {
        "Popen", "call", "check_call", "check_output", "mkdir", "open", "rename",
        "replace", "rmdir", "run", "touch", "unlink", "write_bytes", "write_text",
    }

    def contains_sensitive_callable_reference(node: ast.AST | None) -> bool:
        if node is None:
            return False
        parent_by_id = {
            id(child): parent
            for parent in ast.walk(node)
            for child in ast.iter_child_nodes(parent)
        }
        for item in ast.walk(node):
            sensitive = (
                isinstance(item, ast.Name) and item.id in sensitive_names
            ) or (
                isinstance(item, ast.Attribute) and item.attr in sensitive_attributes
            )
            parent = parent_by_id.get(id(item))
            invoked_directly = isinstance(parent, ast.Call) and parent.func is item
            if sensitive and not invoked_directly:
                return True
        return False

    class PolicyVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.function = "<module>"

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            previous = self.function
            self.function = node.name
            defaults = [*node.args.defaults, *(item for item in node.args.kw_defaults if item is not None)]
            if any(contains_sensitive_callable_reference(item) for item in defaults):
                errors.add("E_BUILDER_ALIAS_BINDING")
            self.generic_visit(node)
            self.function = previous

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            previous = self.function
            self.function = node.name
            defaults = [*node.args.defaults, *(item for item in node.args.kw_defaults if item is not None)]
            if any(contains_sensitive_callable_reference(item) for item in defaults):
                errors.add("E_BUILDER_ALIAS_BINDING")
            self.generic_visit(node)
            self.function = previous

        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                if alias.name.split(".", 1)[0] not in allowed_imports:
                    errors.add("E_BUILDER_IMPORT")
                if alias.asname is not None:
                    errors.add("E_BUILDER_ALIAS_BINDING")

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            if (node.module or "").split(".", 1)[0] not in allowed_imports:
                errors.add("E_BUILDER_IMPORT")
            if any(alias.asname is not None for alias in node.names):
                errors.add("E_BUILDER_ALIAS_BINDING")

        def visit_Assign(self, node: ast.Assign) -> None:
            if contains_sensitive_callable_reference(node.value):
                errors.add("E_BUILDER_ALIAS_BINDING")
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            if contains_sensitive_callable_reference(node.value):
                errors.add("E_BUILDER_ALIAS_BINDING")
            self.generic_visit(node)

        def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
            if contains_sensitive_callable_reference(node.value):
                errors.add("E_BUILDER_ALIAS_BINDING")
            self.generic_visit(node)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            defaults = [*node.args.defaults, *(item for item in node.args.kw_defaults if item is not None)]
            if any(contains_sensitive_callable_reference(item) for item in defaults):
                errors.add("E_BUILDER_ALIAS_BINDING")
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:
            nonlocal subprocess_calls, run_process_calls, atomic_write_calls
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "getattr", "globals", "locals", "setattr", "vars", "__import__", "open"}:
                errors.add("E_BUILDER_DYNAMIC_EXECUTION")
            if isinstance(node.func, ast.Attribute) and node.func.attr in write_methods:
                if node.func.attr not in allowed_writes.get(self.function, set()):
                    errors.add("E_BUILDER_WRITE_ESCAPE")
            if isinstance(node.func, ast.Attribute) and node.func.attr == "replace":
                receiver = node.func.value
                allowed_replace = (
                    self.function == "lf_bytes" and isinstance(receiver, (ast.Name, ast.Call))
                ) or (
                    self.function == "atomic_write" and isinstance(receiver, ast.Name) and receiver.id == "temporary"
                )
                if not allowed_replace:
                    errors.add("E_BUILDER_WRITE_ESCAPE")
            if isinstance(node.func, ast.Attribute) and node.func.attr == "open":
                if not (self.function == "build_source_rows" and isinstance(node.func.value, ast.Name) and node.func.value.id == "Image"):
                    errors.add("E_BUILDER_WRITE_ESCAPE")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr in {"run", "call", "Popen", "check_call", "check_output"}:
                subprocess_calls += 1
                if self.function != "run_process" or node.func.attr != "run" or any(keyword.arg == "shell" and not (isinstance(keyword.value, ast.Constant) and keyword.value.value is False) for keyword in node.keywords):
                    errors.add("E_BUILDER_SUBPROCESS_GRAMMAR")
            if isinstance(node.func, ast.Name) and node.func.id == "run_process":
                run_process_calls += 1
                first = node.args[0] if node.args else None
                if self.function != "git" or not isinstance(first, ast.List) or not first.elts or not isinstance(first.elts[0], ast.Constant) or first.elts[0].value != "git":
                    errors.add("E_BUILDER_SUBPROCESS_GRAMMAR")
            if isinstance(node.func, ast.Name) and node.func.id == "atomic_write":
                atomic_write_calls += 1
                if self.function != "main":
                    errors.add("E_BUILDER_WRITE_ESCAPE")
            self.generic_visit(node)

    PolicyVisitor().visit(tree)
    if subprocess_calls != 1 or run_process_calls != 1:
        errors.add("E_BUILDER_SUBPROCESS_COUNT")
    if atomic_write_calls != 2:
        errors.add("E_BUILDER_WRITE_COUNT")
    required_policy_fragments = [
        'READ_ONLY_GIT_COMMANDS = {"cat-file", "diff-tree", "log", "merge-base", "rev-parse", "show"}',
        'args[0] in READ_ONLY_GIT_COMMANDS',
        'return run_process(["git", *args], check=check)',
    ]
    if any(fragment not in source for fragment in required_policy_fragments):
        errors.add("E_BUILDER_GIT_READ_ONLY_POLICY")
    return errors


def negative_controls(topology: dict[str, Any], attestation: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, set[str], set[str]]] = []

    def rebind(value: dict[str, Any]) -> None:
        projected = copy.deepcopy(value)
        projected.pop("semantic_sha256", None)
        value["semantic_sha256"] = sha256(canonical(projected))

    def mutate_top(name: str, expected: set[str], operation: Any, *, rebind_hash: bool = False) -> None:
        value = copy.deepcopy(topology)
        operation(value)
        if rebind_hash:
            rebind(value)
        cases.append((name, expected, artifact_errors(value, attestation)))

    def mutate_att(name: str, expected: set[str], operation: Any, *, rebind_hashes: bool = False) -> None:
        value = copy.deepcopy(attestation)
        operation(value)
        if rebind_hashes:
            value["human_evidence_semantic_sha256"] = sha256(canonical(value["human_evidence"]))
            rebind(value)
        cases.append((name, expected, artifact_errors(topology, value)))

    top_semantic = {"E_TOP_SEMANTIC_SHA"}
    att_semantic = {"E_ATT_SEMANTIC_SHA"}
    mutate_top("unknown_top_key", {"E_SCHEMA_TOP_ROOT"}, lambda value: value.__setitem__("UNDECLARED_ROOT_KEY", 1), rebind_hash=True)
    mutate_att("unknown_att_key", {"E_SCHEMA_ATT_ROOT"}, lambda value: value.__setitem__("UNDECLARED_ROOT_KEY", 1), rebind_hashes=True)
    mutate_top("source_path", {"E_TOP_PATH_ORDER", "E_ROW_001_PATH", "E_ROW_001_READ_PATH", "E_HUMAN_TEXT_BINDING"} | top_semantic, lambda value: value["sources"][0].__setitem__("path", "tampered"))
    mutate_top("source_blob", {"E_ROW_001_BLOB", "E_ROW_001_READ_BLOB", "E_HUMAN_TEXT_BINDING"} | top_semantic, lambda value: value["sources"][0].__setitem__("blob_sha1", "0" * 40))
    mutate_top("source_extent", {"E_ROW_001_EXTENT"} | top_semantic, lambda value: value["sources"][0]["extent"].__setitem__("lines", 1))
    mutate_top("missing_source", {"E_TOP_SOURCE_COUNT"}, lambda value: value["sources"].pop())
    mutate_top("p4_fabrication", {"E_PROCESS_P4_RESULT"} | top_semantic, lambda value: value["process"].__setitem__("p4_result_present", True))
    mutate_top("p4_state", {"E_PROCESS_P4_STATE"} | top_semantic, lambda value: value["process"].__setitem__("p4_state", "EXECUTED"))
    mutate_top("observation_authority", {"E_OBSERVATION_AUTHORITY"} | top_semantic, lambda value: value["phase057_observations"]["records"][0].__setitem__("authority", "CONCLUSION"))
    mutate_top("observation_missing", {"E_OBSERVATION_COUNT", "E_OBSERVATION_IDS"} | top_semantic, lambda value: value["phase057_observations"]["records"].pop())
    mutate_top("external_truth", {"E_AUTH_EXTERNAL_SCIENTIFIC"} | top_semantic, lambda value: value["authority"].__setitem__("external_scientific", True))
    mutate_top("topology_status", {"E_TOP_STATUS"} | top_semantic, lambda value: value.__setitem__("status", "PASS_EXTERNAL"))
    guard_cases = [
        ("ref6_false_present", "literature", "ref6_original_full_text", "READ_FULL", "E_GUARD_REF6"),
        ("ref7_false_present", "literature", "ref7_original_full_text", "READ_FULL", "E_GUARD_REF7"),
        ("jcp147_substitute", "literature", "jcp147_substitute_for_ref6_ref7", True, "E_GUARD_JCP_SUBSTITUTE"),
        ("wrong_ref7_doi", "literature", "rejected_ref7_doi", "10.1063/1.4802584", "E_GUARD_REF7_DOI"),
        ("bibliography_conflation", "literature", "reference_ledger_equals_adopted_bibliography", True, "E_GUARD_BIB_CONFLATION"),
        ("jcp_equation_anchor", "equations", "required_jcp_equation_anchors", [32, 33, 34, 37], "E_GUARD_EQ_ANCHORS"),
        ("jcp_condition_omission", "equations", "required_jcp_applicability_condition_count", 2, "E_GUARD_JCP_CONDITIONS"),
        ("fredholm_volterra_swap", "equations", "fredholm_volterra_same_problem", True, "E_GUARD_FREDHOLM_VOLTERRA"),
        ("algebraic_kernel_promotion", "equations", "algebraic_roots_promoted_to_integral_kernel", True, "E_GUARD_ALGEBRAIC_KERNEL"),
        ("picard_exact_promotion", "equations", "first_ratio_picard_is_exact_or_general_convergence", True, "E_GUARD_PICARD_EXACT"),
        ("interaction_double_count", "equations", "interaction_double_count_allowed", True, "E_GUARD_DOUBLE_COUNT"),
        ("c_rate_3600_removal", "coordinates_units", "c_rate_factor_3600_state", "REMOVED", "E_GUARD_C_RATE_3600"),
        ("voltage_to_time_eis", "coordinates_units", "voltage_fourier_promoted_to_time_eis_instrument", True, "E_GUARD_VOLTAGE_COORDINATE"),
        ("internal_to_material", "authority", "internal_gate_promoted_to_material_experimental", True, "E_GUARD_EXTERNAL_PROMOTION"),
        ("positive_speedup", "authority", "positive_speedup_claimed", True, "E_GUARD_SPEEDUP_CLAIM"),
        ("ownerless_correction", "routing", "correction_owner", "", "E_GUARD_OWNER"),
    ]
    for name, section, key, replacement, code in guard_cases:
        mutate_top(name, {code} | top_semantic, lambda value, s=section, k=key, r=replacement: value["downstream_guardrails"][s].__setitem__(k, r))
    mutate_top("reference_ledger_role", {"E_PROCESS_REFERENCE_LEDGER_ROLE"} | top_semantic, lambda value: value["process"].__setitem__("reference_ledger_role", "ADOPTED_BIBLIOGRAPHY"))
    mutate_top("adopted_bibliography", {"E_PROCESS_ADOPTED_BIBLIOGRAPHY"} | top_semantic, lambda value: value["process"].__setitem__("adopted_bibliography_path", "tampered"))
    mutate_att("read_state", {"E_ROW_001_READ_STATE"} | att_semantic, lambda value: value["sources"][0].__setitem__("read_state", "PARTIAL"))
    mutate_att("line_gap", {"E_ROW_001_TEXT_COVERAGE"} | att_semantic, lambda value: value["sources"][0]["coverage"].__setitem__("end", 100))
    mutate_att("pdf_page", {"E_ROW_058_PDF_COVERAGE"} | att_semantic, lambda value: value["sources"][57]["coverage"].__setitem__("end", 86))
    mutate_att("pdf_visual", {"E_ROW_058_PDF_VISUAL"} | att_semantic, lambda value: value["sources"][57].__setitem__("visual_review", "PARTIAL"))
    mutate_att("image_visual", {"E_ROW_079_IMAGE_VISUAL"} | att_semantic, lambda value: value["sources"][78].__setitem__("visual_review", "PARTIAL"))
    mutate_att("reader_partition", {"E_ROW_001_PARTITION"} | att_semantic, lambda value: value["sources"][0].__setitem__("reader_partition", "D"))
    mutate_att("coverage_gap", {"E_ATT_GAPS"} | att_semantic, lambda value: value.__setitem__("coverage_gap_count", 1))
    mutate_att("source_mutation_count", {"E_ATT_MUTATION_COUNT"} | att_semantic, lambda value: value.__setitem__("source_mutation_count", 1))
    mutate_att("human_evidence_sha", {"E_HUMAN_EVIDENCE_SHA"} | att_semantic, lambda value: value.__setitem__("human_evidence_semantic_sha256", "0" * 64))
    mutate_att("human_pdf_identity", {"E_HUMAN_PDF_IDENTITY"}, lambda value: value["human_evidence"]["pdf_reviews"][0].__setitem__("path", "tampered"), rebind_hashes=True)
    mutate_att("human_reader_identity", {"E_HUMAN_PARTITION_IDENTITY"}, lambda value: value["human_evidence"]["partitions"][0].__setitem__("reader", "tampered"), rebind_hashes=True)
    mutate_att("human_partition_scalar", {"E_SCHEMA_STRUCTURE"}, lambda value: value["human_evidence"].__setitem__("partitions", [1, 2, 3]))
    mutate_top("source_scalar", {"E_SCHEMA_STRUCTURE"}, lambda value: value.__setitem__("sources", [1] * 83))

    control_texts = {
        "result": (ROOT / RESULT_PATH).read_text(encoding="utf-8"),
        "parent": (ROOT / PARENT_LEDGER_PATH).read_text(encoding="utf-8"),
        "active": (ROOT / ACTIVE_LEDGER_PATH).read_text(encoding="utf-8"),
        "handover": (ROOT / HANDOVER_PATH).read_text(encoding="utf-8"),
    }
    control_mutations = [
        ("result_status_conflict", "result", "Status: `PASS_PENDING_PERSISTENCE`", "Status: `FAIL`", {"E_CONTROL_RESULT_IDENTITY", "E_CONTROL_RESULT_FIELDS", "E_CONTROL_RESULT_DECLARATIONS", "E_CONTROL_CONTRADICTION_RESULT"}),
        ("parent_status_conflict", "parent", "| IN_PROGRESS |", "| FAIL |", {"E_CONTROL_PARENT_IDENTITY", "E_CONTROL_PARENT_ROW"}),
        ("active_subject_conflict", "active", EXPECTED_SUBJECT, "wrong subject", {"E_CONTROL_ACTIVE_IDENTITY", "E_CONTROL_ACTIVE_PHASE_ROW", "E_CONTROL_ACTIVE_STEP_ROW"}),
        ("handover_persistence_conflict", "handover", PERSISTENCE, "WRONG_PERSISTENCE", {"E_CONTROL_HANDOVER_IDENTITY", "E_CONTROL_HANDOVER_ROW", "E_CONTROL_HANDOVER_NEXT"}),
    ]
    for name, document, old, new, expected in control_mutations:
        mutated = copy.deepcopy(control_texts)
        mutated[document] = mutated[document].replace(old, new)
        cases.append((name, expected, control_document_errors(mutated)))
    result_decoy = copy.deepcopy(control_texts)
    result_decoy["result"] += "\nStatus: `PASS`\nContaining commit: `deadbeef`\n"
    cases.append(("result_declaration_decoy", {"E_CONTROL_RESULT_IDENTITY", "E_CONTROL_RESULT_DECLARATIONS"}, control_document_errors(result_decoy)))
    for index, declaration in enumerate(("status: `PASS`", "Status : `PASS`", "**Status:** `PASS`", "Overall Status: `PASS`"), start=1):
        declaration_decoy = copy.deepcopy(control_texts)
        declaration_decoy["result"] += "\n" + declaration + "\n"
        cases.append((f"result_declaration_variant_{index}", {"E_CONTROL_RESULT_IDENTITY", "E_CONTROL_RESULT_DECLARATIONS"}, control_document_errors(declaration_decoy)))
    validator_hash_decoy = copy.deepcopy(control_texts)
    validator_hash_decoy["result"] += "\n- validator raw SHA-256: `" + "0" * 64 + "`.\n"
    cases.append(("result_validator_hash_decoy", {"E_CONTROL_RESULT_IDENTITY"}, control_document_errors(validator_hash_decoy)))
    validator_hash_relocation = copy.deepcopy(control_texts)
    relocated_lines = validator_hash_relocation["result"].splitlines()
    relocated_line = relocated_lines.pop(EXPECTED_VALIDATOR_HASH_LINE_INDEX)
    relocated_lines.insert(31, relocated_line)
    validator_hash_relocation["result"] = "\n".join(relocated_lines) + "\n"
    cases.append(("result_validator_hash_relocation", {"E_CONTROL_RESULT_IDENTITY"}, control_document_errors(validator_hash_relocation)))
    unicode_marker = "\n- first ratio는"
    for name, separator in (("vt", "\u000b"), ("ff", "\u000c"), ("nel", "\u0085"), ("ls", "\u2028"), ("ps", "\u2029")):
        unicode_decoy = copy.deepcopy(control_texts)
        unicode_decoy["result"] = unicode_decoy["result"].replace(unicode_marker, separator + "- first ratio는", 1)
        cases.append(("result_unicode_separator_" + name, {"E_CONTROL_RESULT_IDENTITY"}, control_document_errors(unicode_decoy)))
    for document, expected in (
        ("parent", {"E_CONTROL_PARENT_IDENTITY", "E_CONTROL_PARENT_ROW"}),
        ("active", {"E_CONTROL_ACTIVE_IDENTITY", "E_CONTROL_ACTIVE_PHASE_ROW"}),
        ("handover", {"E_CONTROL_HANDOVER_IDENTITY", "E_CONTROL_HANDOVER_ROW"}),
    ):
        row_decoy = copy.deepcopy(control_texts)
        row_decoy[document] += "\n  | Step 64 complete | PASS | PREMATURE PERSISTENCE CLAIM |\n"
        cases.append((document + "_row_decoy", expected, control_document_errors(row_decoy)))
    prose_decoy = copy.deepcopy(control_texts)
    prose_decoy["parent"] += "\nStep 64 is complete: PASS_P064_STEP64_PERSISTENCE\n"
    cases.append(("parent_prose_decoy", {"E_CONTROL_PARENT_IDENTITY", "E_CONTROL_PARENT_ROW"}, control_document_errors(prose_decoy)))
    for document, identity_code in (
        ("result", "E_CONTROL_RESULT_IDENTITY"),
        ("parent", "E_CONTROL_PARENT_IDENTITY"),
        ("active", "E_CONTROL_ACTIVE_IDENTITY"),
        ("handover", "E_CONTROL_HANDOVER_IDENTITY"),
    ):
        identity_decoy = copy.deepcopy(control_texts)
        identity_decoy[document] += "\n<!-- arbitrary non-semantic decoy -->\n"
        cases.append((document + "_identity_decoy", {identity_code}, control_document_errors(identity_decoy)))
    swapped = copy.deepcopy(control_texts)
    top_raw = sha256(TOPOLOGY.read_bytes())
    att_raw = sha256(ATTESTATION.read_bytes())
    swapped["result"] = swapped["result"].replace(top_raw, "SWAP_PLACEHOLDER").replace(att_raw, top_raw).replace("SWAP_PLACEHOLDER", att_raw)
    cases.append(("hash_label_swap", {"E_CONTROL_RESULT_IDENTITY", "E_CONTROL_RESULT_HASH_LABELS"}, control_document_errors(swapped)))

    builder_source = BUILDER.read_text(encoding="utf-8")
    policy_mutations = [
        ("builder_import", builder_source.replace("from __future__ import annotations\n", "from __future__ import annotations\nimport os\n", 1), {"E_BUILDER_IMPORT", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_write_escape", builder_source + '\npathlib.Path("Claude/ESCAPED").write_text("x")\n', {"E_BUILDER_SOURCE_IDENTITY", "E_BUILDER_WRITE_ESCAPE"}),
        ("builder_subprocess_escape", builder_source + '\nsubprocess.run(["python", "evil.py"])\n', {"E_BUILDER_SOURCE_IDENTITY", "E_BUILDER_SUBPROCESS_GRAMMAR", "E_BUILDER_SUBPROCESS_COUNT"}),
        ("builder_import_alias", builder_source + '\nimport subprocess as sp\nsp.run(["python", "evil.py"])\n', {"E_BUILDER_ALIAS_BINDING", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_default_alias", builder_source + '\ndef escape(fn=subprocess.run):\n    fn(["python", "evil.py"])\nescape()\n', {"E_BUILDER_ALIAS_BINDING", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_run_process_alias", builder_source + '\nrp=run_process\nrp(["python", "evil.py"])\n', {"E_BUILDER_ALIAS_BINDING", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_writer_alias", builder_source + '\nwriter=pathlib.Path.write_text\nwriter(pathlib.Path("Claude/ESCAPED"),"x")\n', {"E_BUILDER_ALIAS_BINDING", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_getattr_subprocess", builder_source + '\ngetattr(subprocess,"run")(["python", "evil.py"])\n', {"E_BUILDER_DYNAMIC_EXECUTION", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_getattr_exec", builder_source + '\ngetattr(__builtins__,"exec")("print(1)")\n', {"E_BUILDER_DYNAMIC_EXECUTION", "E_BUILDER_SOURCE_IDENTITY"}),
        ("builder_syntax", builder_source + "\ndef (\n", {"E_BUILDER_SOURCE_IDENTITY", "E_BUILDER_SYNTAX"}),
    ]
    for name, source, expected in policy_mutations:
        cases.append((name, expected, source_policy_errors(source)))

    passed = sum(observed == expected for _, expected, observed in cases)
    return passed, len(cases)


def strict_json_controls() -> tuple[int, int]:
    cases = [
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        b'{"a":1e9999}',
        bytes([123, 34, 97, 34, 58]) + b"9" * 1000 + bytes([125]),
        b'{"a":',
    ]
    passed = 0
    for index, raw in enumerate(cases):
        try:
            strict_load_bytes(raw, f"negative-{index}")
        except ValidationError:
            passed += 1
    return passed, len(cases)


def run_builder(output_dir: pathlib.Path) -> tuple[bytes, bytes]:
    process = run_process([sys.executable, BUILDER_PATH, "--output-dir", str(output_dir)])
    require(b"PASS_P064_STEP64_BUILD" in process.stdout, "E_BUILDER_TERMINAL")
    return (output_dir / pathlib.Path(TOPOLOGY_PATH).name).read_bytes(), (output_dir / pathlib.Path(ATTESTATION_PATH).name).read_bytes()


def collect_git_projection(
    cwd: pathlib.Path,
    *,
    active_branch: str,
    protected_branch: str,
    claude_base: str,
) -> dict[str, Any]:
    return {
        "branch": git_text(["branch", "--show-current"], cwd=cwd),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], cwd=cwd),
        "head": git_text(["rev-parse", "HEAD"], cwd=cwd),
        "upstream": git_text(["rev-parse", "@{upstream}"], cwd=cwd),
        "tracking": git_text(["rev-parse", f"refs/remotes/origin/{active_branch}"], cwd=cwd),
        "live": live_tip(active_branch, cwd=cwd),
        "protected_local": git_text(["rev-parse", f"refs/heads/{protected_branch}"], cwd=cwd),
        "protected_tracking": git_text(["rev-parse", f"refs/remotes/origin/{protected_branch}"], cwd=cwd),
        "protected_live": live_tip(protected_branch, cwd=cwd),
        "main_tracking": git_text(["rev-parse", "refs/remotes/origin/main"], cwd=cwd),
        "main_live": live_tip("main", cwd=cwd),
        "claude_tracked": git_text(["diff", "--name-only", claude_base, "--", "Claude"], cwd=cwd),
        "claude_untracked": git_text(["ls-files", "--others", "--exclude-standard", "--", "Claude"], cwd=cwd),
        "diff_check": git(["diff", "--check"], cwd=cwd, check=False).returncode,
        "cached_diff_check": git(["diff", "--cached", "--check"], cwd=cwd, check=False).returncode,
    }


def git_projection_errors(
    projection: dict[str, Any],
    *,
    active_branch: str,
    active_tip: str,
    protected_tip: str,
    main_tip: str,
) -> set[str]:
    errors: set[str] = set()
    if projection.get("branch") != active_branch:
        errors.add("E_GIT_BRANCH")
    if projection.get("upstream_name") != f"origin/{active_branch}":
        errors.add("E_GIT_UPSTREAM_NAME")
    for key in ("head", "upstream", "tracking", "live"):
        if projection.get(key) != active_tip:
            errors.add("E_GIT_ACTIVE_" + key.upper())
    for key in ("protected_local", "protected_tracking", "protected_live"):
        if projection.get(key) != protected_tip:
            errors.add("E_GIT_" + key.upper())
    for key in ("main_tracking", "main_live"):
        if projection.get(key) != main_tip:
            errors.add("E_GIT_" + key.upper())
    if projection.get("claude_tracked"):
        errors.add("E_GIT_CLAUDE_TRACKED")
    if projection.get("claude_untracked"):
        errors.add("E_GIT_CLAUDE_UNTRACKED")
    if projection.get("diff_check") != 0 or projection.get("cached_diff_check") != 0:
        errors.add("E_GIT_DIFF_CHECK")
    return errors


def content_path_errors(cwd: pathlib.Path, allowed: set[str]) -> set[str]:
    status_raw = git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=cwd).stdout.decode("utf-8")
    status_entries = [entry for entry in status_raw.split("\0") if entry]
    paths = {entry[3:] for entry in status_entries if len(entry) >= 4}
    return {"E_GIT_EXTRA_DIRT"} if paths - allowed else set()


def staged_contract_errors(cwd: pathlib.Path, expected_paths: set[str]) -> set[str]:
    errors: set[str] = set()
    staged = set(git_text(["diff", "--cached", "--name-only"], cwd=cwd).splitlines())
    status_raw = git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=cwd).stdout.decode("utf-8")
    status_entries = [entry for entry in status_raw.split("\0") if entry]
    status_paths = {entry[3:] for entry in status_entries if len(entry) >= 4}
    if staged != expected_paths:
        errors.add("E_GIT_STAGED_SET")
    if status_paths != expected_paths or any(entry[:2] not in {"A ", "M "} for entry in status_entries):
        errors.add("E_GIT_STATUS_SET")
    if git_text(["diff", "--name-only"], cwd=cwd):
        errors.add("E_GIT_UNSTAGED")
    for path in expected_paths:
        if git_text(["rev-parse", f":{path}"], cwd=cwd) != git_text(["hash-object", f"--path={path}", path], cwd=cwd):
            errors.add("E_GIT_INDEX_WORKTREE")
    return errors


def commit_contract_errors(
    cwd: pathlib.Path,
    *,
    commit: str,
    expected_parent: str,
    expected_subject: str,
    expected_paths: set[str],
) -> set[str]:
    errors: set[str] = set()
    if git_text(["rev-parse", f"{commit}^"] , cwd=cwd) != expected_parent:
        errors.add("E_GIT_PARENT")
    if git_text(["show", "-s", "--format=%s", commit], cwd=cwd) != expected_subject:
        errors.add("E_GIT_SUBJECT")
    committed = set(git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", commit], cwd=cwd).splitlines())
    if committed != expected_paths:
        errors.add("E_GIT_COMMITTED_SET")
    return errors


def repository_errors(mode: str, expected_commit: str | None) -> set[str]:
    active_tip = expected_commit if mode == "persistence" else EXPECTED_PARENT
    projection = collect_git_projection(
        ROOT,
        active_branch=ACTIVE_BRANCH,
        protected_branch=PROTECTED_BRANCH,
        claude_base=EXPECTED_PARENT,
    )
    errors = git_projection_errors(
        projection,
        active_branch=ACTIVE_BRANCH,
        active_tip=active_tip or "",
        protected_tip=PROTECTED_TIP,
        main_tip=MAIN_TIP,
    )
    head = projection["head"]
    if mode == "staged":
        errors.update(staged_contract_errors(ROOT, FINAL_SET))
    elif mode == "persistence":
        if expected_commit is None or head != expected_commit:
            errors.add("E_GIT_EXPECTED_COMMIT")
        else:
            errors.update(commit_contract_errors(
                ROOT,
                commit=expected_commit,
                expected_parent=EXPECTED_PARENT,
                expected_subject=EXPECTED_SUBJECT,
                expected_paths=FINAL_SET,
            ))
            for path in FINAL_PATHS:
                if git_text(["rev-parse", f"{expected_commit}:{path}"]) != git_text(["hash-object", f"--path={path}", path]):
                    errors.add("E_GIT_COMMIT_WORKTREE")
        if git_text(["status", "--porcelain=v1"]):
            errors.add("E_GIT_DIRTY")
    else:
        errors.update(content_path_errors(ROOT, FINAL_SET))
    return errors


def git_fixture_controls() -> tuple[int, int]:
    cases: list[tuple[str, set[str], set[str]]] = []
    active = "fixture/active"
    protected = "fixture/protected"

    with tempfile.TemporaryDirectory(prefix="p064-step64-git-fixture-") as directory:
        base = pathlib.Path(directory)
        bare = base / "remote.git"
        work = base / "work"
        run_process(["git", "init", "--bare", str(bare)], cwd=base)
        run_process(["git", "init", "--initial-branch=main", str(work)], cwd=base)
        git(["config", "user.name", "Phase064 Fixture"], cwd=work)
        git(["config", "user.email", "phase064-fixture@example.invalid"], cwd=work)
        (work / "Claude").mkdir()
        (work / "Claude" / "baseline.txt").write_text("baseline\n", encoding="utf-8")
        (work / "seed.txt").write_text("seed\n", encoding="utf-8")
        git(["add", "Claude/baseline.txt", "seed.txt"], cwd=work)
        git(["commit", "-m", "fixture seed"], cwd=work)
        seed = git_text(["rev-parse", "HEAD"], cwd=work)
        tree = git_text(["rev-parse", f"{seed}^{{tree}}"], cwd=work)
        drift = git_text(["commit-tree", tree, "-p", seed, "-m", "fixture drift"], cwd=work)
        git(["remote", "add", "origin", str(bare)], cwd=work)
        git(["push", "-u", "origin", "main"], cwd=work)
        git(["branch", protected, seed], cwd=work)
        git(["push", "origin", protected], cwd=work)
        git(["checkout", "-b", active, seed], cwd=work)
        git(["push", "-u", "origin", active], cwd=work)

        def projection() -> set[str]:
            value = collect_git_projection(work, active_branch=active, protected_branch=protected, claude_base=seed)
            return git_projection_errors(value, active_branch=active, active_tip=seed, protected_tip=seed, main_tip=seed)

        cases.append(("baseline", set(), projection()))
        git(["branch", "--set-upstream-to=origin/main", active], cwd=work)
        cases.append(("upstream_name", {"E_GIT_UPSTREAM_NAME"}, projection()))
        git(["branch", "--set-upstream-to", f"origin/{active}", active], cwd=work)

        git(["update-ref", f"refs/heads/{active}", drift], cwd=work)
        cases.append(("head", {"E_GIT_ACTIVE_HEAD"}, projection()))
        git(["update-ref", f"refs/heads/{active}", seed], cwd=work)

        git(["update-ref", f"refs/remotes/origin/{active}", drift], cwd=work)
        cases.append(("active_tracking", {"E_GIT_ACTIVE_UPSTREAM", "E_GIT_ACTIVE_TRACKING"}, projection()))
        git(["update-ref", f"refs/remotes/origin/{active}", seed], cwd=work)

        git(["push", "origin", f"{drift}:refs/heads/{active}"], cwd=work)
        git(["update-ref", f"refs/remotes/origin/{active}", seed], cwd=work)
        cases.append(("active_live", {"E_GIT_ACTIVE_LIVE"}, projection()))
        git(["push", "--force", "origin", f"{seed}:refs/heads/{active}"], cwd=work)
        git(["update-ref", f"refs/remotes/origin/{active}", seed], cwd=work)

        git(["update-ref", f"refs/heads/{protected}", drift], cwd=work)
        cases.append(("protected_local", {"E_GIT_PROTECTED_LOCAL"}, projection()))
        git(["update-ref", f"refs/heads/{protected}", seed], cwd=work)
        git(["update-ref", f"refs/remotes/origin/{protected}", drift], cwd=work)
        cases.append(("protected_tracking", {"E_GIT_PROTECTED_TRACKING"}, projection()))
        git(["update-ref", f"refs/remotes/origin/{protected}", seed], cwd=work)
        git(["push", "origin", f"{drift}:refs/heads/{protected}"], cwd=work)
        git(["update-ref", f"refs/remotes/origin/{protected}", seed], cwd=work)
        cases.append(("protected_live", {"E_GIT_PROTECTED_LIVE"}, projection()))
        git(["push", "--force", "origin", f"{seed}:refs/heads/{protected}"], cwd=work)
        git(["update-ref", f"refs/remotes/origin/{protected}", seed], cwd=work)

        git(["update-ref", "refs/remotes/origin/main", drift], cwd=work)
        cases.append(("main_tracking", {"E_GIT_MAIN_TRACKING"}, projection()))
        git(["update-ref", "refs/remotes/origin/main", seed], cwd=work)
        git(["push", "origin", f"{drift}:refs/heads/main"], cwd=work)
        git(["update-ref", "refs/remotes/origin/main", seed], cwd=work)
        cases.append(("main_live", {"E_GIT_MAIN_LIVE"}, projection()))
        git(["push", "--force", "origin", f"{seed}:refs/heads/main"], cwd=work)
        git(["update-ref", "refs/remotes/origin/main", seed], cwd=work)

        git(["checkout", "main"], cwd=work)
        cases.append(("branch", {"E_GIT_BRANCH", "E_GIT_UPSTREAM_NAME"}, projection()))
        git(["checkout", active], cwd=work)

        escaped = work / "Claude" / "escape.txt"
        escaped.write_text("escape\n", encoding="utf-8")
        cases.append(("claude", {"E_GIT_CLAUDE_UNTRACKED"}, projection()))
        escaped.unlink()

        seed_path = work / "seed.txt"
        seed_path.write_text("seed  \n", encoding="utf-8")
        cases.append(("diff_check", {"E_GIT_DIFF_CHECK"}, projection()))
        git(["restore", "--worktree", "--", "seed.txt"], cwd=work)

        extra = work / "extra.tmp"
        extra.write_text("extra\n", encoding="utf-8")
        cases.append(("path", {"E_GIT_EXTRA_DIRT"}, content_path_errors(work, set())))
        extra.unlink()

        cases.append(("commit_baseline", set(), commit_contract_errors(
            work, commit=drift, expected_parent=seed, expected_subject="fixture drift", expected_paths=set()
        )))
        cases.append(("commit_parent", {"E_GIT_PARENT"}, commit_contract_errors(
            work, commit=drift, expected_parent=drift, expected_subject="fixture drift", expected_paths=set()
        )))
        cases.append(("commit_subject", {"E_GIT_SUBJECT"}, commit_contract_errors(
            work, commit=drift, expected_parent=seed, expected_subject="wrong subject", expected_paths=set()
        )))
        cases.append(("commit_paths", {"E_GIT_COMMITTED_SET"}, commit_contract_errors(
            work, commit=drift, expected_parent=seed, expected_subject="fixture drift", expected_paths={"missing.txt"}
        )))

        staged_path = work / "stage.txt"
        staged_path.write_text("stage one\n", encoding="utf-8")
        git(["add", "stage.txt"], cwd=work)
        cases.append(("staged_baseline", set(), staged_contract_errors(work, {"stage.txt"})))
        extra_staged = work / "extra-stage.txt"
        extra_staged.write_text("extra staged\n", encoding="utf-8")
        git(["add", "extra-stage.txt"], cwd=work)
        cases.append(("staged_extra", {"E_GIT_STAGED_SET", "E_GIT_STATUS_SET"}, staged_contract_errors(work, {"stage.txt"})))
        git(["restore", "--staged", "--", "extra-stage.txt"], cwd=work)
        extra_staged.unlink()
        staged_path.write_text("stage two\n", encoding="utf-8")
        cases.append(("index_worktree", {"E_GIT_STATUS_SET", "E_GIT_UNSTAGED", "E_GIT_INDEX_WORKTREE"}, staged_contract_errors(work, {"stage.txt"})))
        git(["restore", "--worktree", "--", "stage.txt"], cwd=work)
        bad_staged = work / "bad-stage.txt"
        bad_staged.write_text("bad  \n", encoding="utf-8")
        git(["add", "bad-stage.txt"], cwd=work)
        cases.append(("cached_diff_check", {"E_GIT_DIFF_CHECK"}, projection()))
        git(["restore", "--staged", "--", "bad-stage.txt", "stage.txt"], cwd=work)
        bad_staged.unlink()
        staged_path.unlink()

    passed = sum(expected == observed for _, expected, observed in cases)
    return passed, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    require(sum((args.content_only, args.verify_staged, args.verify_persistence)) == 1, "E_CLI_MODE")
    if not TOPOLOGY.is_file() or not ATTESTATION.is_file():
        missing = [path for path in (TOPOLOGY_PATH, ATTESTATION_PATH) if not (ROOT / path).is_file()]
        raise ValidationError("E_STEP64_ARTIFACT_MISSING: " + ", ".join(missing))
    topology, top_traversal, top_raw = strict_load(TOPOLOGY)
    attestation, att_traversal, att_raw = strict_load(ATTESTATION)
    errors = artifact_errors(topology, attestation)
    if not errors:
        errors.update(independent_frozen_errors(topology, attestation))
    errors.update(control_errors())
    errors.update(source_policy_errors())
    mode = "persistence" if args.verify_persistence else "staged" if args.verify_staged else "content"
    errors.update(repository_errors(mode, args.expected_commit))
    require(not errors, "E_STEP64_CONTENT", repr(sorted(errors)))
    workspace_hashes = {path: sha256((ROOT / path).read_bytes()) for path in FINAL_PATHS}
    if args.run_negative_probes or args.verify_staged or args.verify_persistence:
        negative_passed, negative_total = negative_controls(topology, attestation)
        strict_passed, strict_total = strict_json_controls()
        require(negative_passed == negative_total, "E_NEGATIVE_CONTROLS")
        require(strict_passed == strict_total, "E_STRICT_CONTROLS")
        print(f"PASS_P064_STEP64_NEGATIVE {negative_passed}/{negative_total} strict_json={strict_passed}/{strict_total}")
        git_passed, git_total = git_fixture_controls()
        require(git_passed == git_total, "E_GIT_FIXTURE_CONTROLS", f"{git_passed}/{git_total}")
        print(f"PASS_P064_STEP64_GIT_FIXTURE {git_passed}/{git_total}")
    if args.determinism_check or args.verify_staged or args.verify_persistence:
        with tempfile.TemporaryDirectory(prefix="p064-step64-a-") as first_dir, tempfile.TemporaryDirectory(prefix="p064-step64-b-") as second_dir:
            first = run_builder(pathlib.Path(first_dir))
            second = run_builder(pathlib.Path(second_dir))
        require(first == second == (top_raw, att_raw), "E_DETERMINISM")
        print("PASS_P064_STEP64_DETERMINISM 2/2")
        post_hashes = {path: sha256((ROOT / path).read_bytes()) for path in FINAL_PATHS}
        require(post_hashes == workspace_hashes, "E_POST_BUILDER_WORKSPACE_MUTATION")
        post_repository = repository_errors(mode, args.expected_commit)
        require(not post_repository, "E_POST_BUILDER_REPOSITORY", repr(sorted(post_repository)))
        print("PASS_P064_STEP64_POST_BUILDER_BOUNDARY")
    nodes = top_traversal["all_nodes"] + att_traversal["all_nodes"]
    if args.content_only:
        print(f"{GATE} source=83/83 text=78/12508 pdf=3/129 image=2/2 strict_nodes={nodes}")
    elif args.verify_staged:
        print("PASS_P064_STEP64_STAGED exact-eight=8/8")
    else:
        require(args.expected_commit is not None, "E_EXPECTED_COMMIT")
        print(f"{PERSISTENCE} commit={args.expected_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, AttributeError, KeyError, IndexError, SyntaxError, TypeError, ValueError, OSError, UnicodeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL_P064_STEP64 {error}")
        raise SystemExit(1)
