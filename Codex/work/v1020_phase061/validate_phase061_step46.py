#!/usr/bin/env python3
"""Validate Phase 061 Step 46 source topology, read coverage and persistence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1020_phase061/build_phase061_step46_source_topology.py"
VALIDATOR = Path(__file__).resolve()
TOPOLOGY = REPO / "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
ATTESTATION = REPO / "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json"
RESULT = REPO / "Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
EXPECTED_PARENT = "0c18bb48401675bd5154649baa2d6a151d272d9c"
EXPECTED_SUBJECT = "audit(phase061): freeze v1020 source topology"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

EXACT_EIGHT = [
    "Codex/work/v1020_phase061/build_phase061_step46_source_topology.py",
    "Codex/work/v1020_phase061/validate_phase061_step46.py",
    "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json",
    "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json",
    "Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]
EXACT_EIGHT_SET = set(EXACT_EIGHT)

EXPECTED_COUNTS = {
    "paths": 232,
    "unique_blobs": 231,
    "text_files": 195,
    "text_physical_lines": 31553,
    "text_nonblank_lines": 29335,
    "pdf_files": 14,
    "pdf_pages": 130,
    "image_occurrences": 23,
    "same_relative_pairs": 47,
    "same_relative_identical": 18,
    "same_relative_changed": 29,
    "v1019_identical_overlap": 18,
    "v1019_new_blob_or_source": 214,
}
EXPECTED_GROUPS = {
    "COMPETITIVE_CANDIDATE_REVIEW": 126,
    "CORE_PROCESS_RESULT": 31,
    "FINAL_RELEASE_SURFACE": 53,
    "PLAN_P0_P8": 10,
    "STRUCTURAL_SNAPSHOT": 10,
    "STRUCTURE_TOOL": 1,
    "TEST_GATE": 1,
}
EXPECTED_DUPLICATE = [{
    "blob_sha1": "8dfea239d1787582c6c37c41fe6d06f7b204d72b",
    "paths": [
        "Claude/docs/v1.0.20/results/snapshot_v1020_p5.json",
        "Claude/docs/v1.0.20/results/snapshot_v1020_p6.json",
    ],
}]


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


def reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def walk_json(value: Any, path: str = "$", stats: dict[str, int] | None = None) -> dict[str, int]:
    if stats is None:
        stats = {"nodes": 0, "max_depth": 0}
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], path.count(".") + path.count("["))
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(path)
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(path)
            walk_json(child, f"{path}.{key}", stats)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_json(child, f"{path}[{index}]", stats)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise TypeError(path)
    return stats


def strict_load(path: Path) -> tuple[Any, dict[str, int]]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
    )
    return value, walk_json(value)


def strict_load_bytes(data: bytes) -> Any:
    value = json.loads(
        data.decode("utf-8"), object_pairs_hook=strict_pairs, parse_constant=reject_constant
    )
    walk_json(value)
    return value


def normalize_lf(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def run_git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8", errors="strict",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def run_git_bytes(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def remote_tip(branch: str) -> str:
    parts = run_git("ls-remote", "--heads", "origin", branch).split()
    return parts[0] if len(parts) == 2 else ""


def porcelain_paths() -> set[str]:
    fields = run_git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all").split(b"\0")
    result: set[str] = set()
    index = 0
    while index < len(fields) and fields[index]:
        row = fields[index].decode("utf-8")
        status = row[:2]
        result.add(row[3:].replace("\\", "/"))
        if "R" in status or "C" in status:
            index += 1
            if index < len(fields) and fields[index]:
                result.add(fields[index].decode("utf-8").replace("\\", "/"))
        index += 1
    return result


def exact_dirty_paths() -> set[str]:
    paths = porcelain_paths()
    for relative in EXACT_EIGHT:
        path = REPO / relative
        tracked = run_git("ls-files", "--error-unmatch", relative, check=False)
        if path.exists() and not tracked:
            paths.add(relative)
    return paths


def nul_paths(*args: str) -> set[str]:
    return {
        item.decode("utf-8").replace("\\", "/")
        for item in run_git_bytes(*args).split(b"\0") if item
    }


def load_builder_module() -> Any:
    spec = importlib.util.spec_from_file_location("phase061_step46_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("builder import spec failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_authority_class(index: int) -> str:
    if 1 <= index <= 53:
        return "RELEASE_SURFACE_UNADJUDICATED"
    if 54 <= index <= 94:
        return "PROCESS_SELF_REPORT"
    if 95 <= index <= 220:
        return "COMPETITIVE_CANDIDATE_OR_REVIEW"
    if 221 <= index <= 230:
        return "GENERATED_STRUCTURAL_SNAPSHOT"
    return "SUPPORT_TOOL_OR_TEST"


def content_diagnostics(
    topology: dict[str, Any], attestation: dict[str, Any],
    expected_topology: dict[str, Any] | None = None,
    expected_attestation: dict[str, Any] | None = None,
) -> set[str]:
    diagnostics: set[str] = set()
    counts = topology.get("counts", {})
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            diagnostics.add(f"TOPOLOGY_COUNT_{key.upper()}")
    sources = topology.get("sources", [])
    if len(sources) != 232:
        diagnostics.add("SOURCE_RECORD_COUNT")
    source_ids = [row.get("source_id") for row in sources]
    paths = [row.get("path") for row in sources]
    if len(set(source_ids)) != len(source_ids) or len(set(paths)) != len(paths):
        diagnostics.add("SOURCE_ID_UNIQUE")
    if expected_topology is not None:
        expected_sources = expected_topology.get("sources", [])
        if [row.get("path") for row in sources] != [row.get("path") for row in expected_sources]:
            diagnostics.add("SOURCE_PATH_IDENTITY")
        blob_fields = ("source_id", "blob_sha1", "sha256", "git_mode", "size_bytes")
        if [tuple(row.get(key) for key in blob_fields) for row in sources] != [
            tuple(row.get(key) for key in blob_fields) for row in expected_sources
        ]:
            diagnostics.add("SOURCE_BLOB_IDENTITY")
    path_hash = sha256(("\n".join(sorted(paths)) + "\n").encode("utf-8")) if all(isinstance(path, str) for path in paths) else ""
    if topology.get("path_set_sha256") != path_hash:
        diagnostics.add("PATH_SET_HASH")
    if topology.get("authority_group_counts") != EXPECTED_GROUPS:
        diagnostics.add("AUTHORITY_GROUP_COUNTS")
    if topology.get("duplicates") != EXPECTED_DUPLICATE:
        diagnostics.add("DUPLICATE_GROUP")
    relations = Counter(row.get("blob_relation") for row in topology.get("same_relative_v1019_v1020", []))
    if len(topology.get("same_relative_v1019_v1020", [])) != 47 or relations != Counter({"CHANGED": 29, "IDENTICAL": 18}):
        diagnostics.add("SAME_RELATIVE_GENEALOGY")
    same_by_new = {
        row.get("v1020_path"): row for row in topology.get("same_relative_v1019_v1020", [])
    }
    row_topology_ok = True
    pairing_ok = True
    duplicate_paths = set(EXPECTED_DUPLICATE[0]["paths"])
    for index, row in enumerate(sources, start=1):
        path = row.get("path")
        pair = same_by_new.get(path)
        expected_overlap = (
            "IDENTICAL_OVERLAP"
            if pair is not None and pair.get("blob_relation") == "IDENTICAL"
            else "NEW_BLOB_OR_SOURCE"
        )
        expected_detail = (
            "IDENTICAL_SAME_RELATIVE" if expected_overlap == "IDENTICAL_OVERLAP"
            else "CHANGED_SAME_RELATIVE" if pair is not None
            else "NO_SAME_RELATIVE_SOURCE"
        )
        row_topology_ok &= (
            isinstance(path, str)
            and row.get("basename") == PurePosixPath(path).name
            and row.get("authority_class") == expected_authority_class(index)
            and row.get("duplicate_relation")
            == ("DUPLICATE_BLOB_OCCURRENCE" if path in duplicate_paths else "UNIQUE_BLOB")
            and row.get("v1019_overlap_class") == expected_overlap
            and row.get("v1019_path_relation") == expected_detail
        )
        if pair is None:
            pairing_ok &= (
                row.get("v1019_same_relative_path") is None
                and row.get("v1019_same_relative_blob_sha1") is None
            )
        else:
            relative = pair.get("relative_path")
            pairing_ok &= (
                pair.get("v1020_blob_sha1") == row.get("blob_sha1")
                and pair.get("v1020_path") == path
                and isinstance(relative, str)
                and pair.get("v1020_path", "").endswith(relative)
                and pair.get("v1019_path", "").endswith(relative)
                and row.get("v1019_same_relative_path") == pair.get("v1019_path")
                and row.get("v1019_same_relative_blob_sha1") == pair.get("v1019_blob_sha1")
            )
    if not row_topology_ok:
        diagnostics.add("SOURCE_ROW_TOPOLOGY")
    if not pairing_ok:
        diagnostics.add("SAME_RELATIVE_PAIRING")
    if "no scientific/material/experimental" not in topology.get("authority_boundary", ""):
        diagnostics.add("TOPOLOGY_AUTHORITY_BOUNDARY")

    att_counts = attestation.get("counts", {})
    att_expected = {
        "text_files": 195, "text_physical_lines": 31553,
        "text_nonblank_lines": 29335, "pdf_files": 14,
        "pdf_pages": 130, "image_occurrences": 23,
        "human_partitions_complete": 3, "human_partitions_total": 3,
    }
    for key, expected in att_expected.items():
        if att_counts.get(key) != expected:
            diagnostics.add(f"ATTESTATION_COUNT_{key.upper()}")
    if len(attestation.get("text_records", [])) != 195:
        diagnostics.add("TEXT_RECORD_COUNT")
    if len(attestation.get("pdf_records", [])) != 14:
        diagnostics.add("PDF_RECORD_COUNT")
    if sum(len(row.get("pages", [])) for row in attestation.get("pdf_records", [])) != 130:
        diagnostics.add("PDF_PAGE_RECORD_COUNT")
    if len(attestation.get("image_records", [])) != 23:
        diagnostics.add("IMAGE_RECORD_COUNT")
    if expected_attestation is not None:
        expected_text = expected_attestation.get("text_records", [])
        text_extent_fields = ("source_id", "physical_lines", "nonblank_lines", "bytes", "sha256")
        if [tuple(row.get(key) for key in text_extent_fields) for row in attestation.get("text_records", [])] != [
            tuple(row.get(key) for key in text_extent_fields) for row in expected_text
        ]:
            diagnostics.add("TEXT_SOURCE_EXTENT")
        expected_pdf = expected_attestation.get("pdf_records", [])
        if [
            (row.get("source_id"), row.get("pages_expected"), row.get("pages_observed"), row.get("pages"))
            for row in attestation.get("pdf_records", [])
        ] != [
            (row.get("source_id"), row.get("pages_expected"), row.get("pages_observed"), row.get("pages"))
            for row in expected_pdf
        ]:
            diagnostics.add("PDF_PAGE_COMPLETENESS")
        if [row.get("source_id") for row in attestation.get("image_records", [])] != [
            row.get("source_id") for row in expected_attestation.get("image_records", [])
        ]:
            diagnostics.add("IMAGE_OCCURRENCE_COMPLETENESS")

    source_by_id = {
        row.get("source_id"): row for row in sources if isinstance(row.get("source_id"), str)
    }
    mode_records = [
        ("FULL_TEXT", attestation.get("text_records", []), "TEXT_ATTESTATION_IDENTITY"),
        ("FULL_PDF", attestation.get("pdf_records", []), "PDF_ATTESTATION_IDENTITY"),
        ("FULL_IMAGE", attestation.get("image_records", []), "IMAGE_ATTESTATION_IDENTITY"),
    ]
    for review_mode, records, code in mode_records:
        expected_ids = {
            row.get("source_id") for row in sources if row.get("review_mode") == review_mode
        }
        observed_ids = [row.get("source_id") for row in records]
        identity_ok = (
            len(observed_ids) == len(set(observed_ids))
            and set(observed_ids) == expected_ids
            and all(
                row.get("source_id") in source_by_id
                and row.get("path") == source_by_id[row.get("source_id")].get("path")
                and row.get("sha256") == source_by_id[row.get("source_id")].get("sha256")
                for row in records
            )
        )
        if not identity_ok:
            diagnostics.add(code)
    if any(
        row.get("pages_expected") != row.get("pages_observed")
        or row.get("pages_observed") != len(row.get("pages", []))
        or [page.get("page") for page in row.get("pages", [])]
        != list(range(1, len(row.get("pages", [])) + 1))
        for row in attestation.get("pdf_records", [])
    ):
        diagnostics.add("PDF_PAGE_EXTENT")
    if (
        sum(row.get("physical_lines", 0) for row in attestation.get("text_records", []))
        != 31553
        or sum(row.get("nonblank_lines", 0) for row in attestation.get("text_records", []))
        != 29335
        or sum(row.get("pages_observed", 0) for row in attestation.get("pdf_records", []))
        != 130
    ):
        diagnostics.add("ATTESTATION_EXTENT_TOTALS")
    if any(row.get("status") != "PASS_HUMAN_FULL_REVIEW" for row in attestation.get("partitions", [])):
        diagnostics.add("HUMAN_PARTITION_STATUS")
    if any(row.get("human_read_state") != "READ_FULL" for row in attestation.get("text_records", [])):
        diagnostics.add("HUMAN_TEXT_STATE")
    if any(row.get("visual_review_state") != "VISUAL_FULL" for row in attestation.get("pdf_records", [])):
        diagnostics.add("HUMAN_PDF_STATE")
    if any(page.get("visual_state") != "VISUAL_FULL" for row in attestation.get("pdf_records", []) for page in row.get("pages", [])):
        diagnostics.add("HUMAN_PDF_PAGE_STATE")
    if any(row.get("visual_review_state") != "VISUAL_FULL" for row in attestation.get("image_records", [])):
        diagnostics.add("HUMAN_IMAGE_STATE")
    if attestation.get("status") != "PASS_FULL_READ_ATTESTATION":
        diagnostics.add("ATTESTATION_STATUS")
    if attestation.get("source_topology_semantic_sha256") != sha256(canonical_bytes(topology)):
        diagnostics.add("TOPOLOGY_ATTESTATION_LINK")
    if "do not establish scientific correctness" not in attestation.get("authority_boundary", ""):
        diagnostics.add("ATTESTATION_AUTHORITY_BOUNDARY")
    if "TEXT_SOURCE_EXTENT" in diagnostics:
        diagnostics.discard("ATTESTATION_EXTENT_TOTALS")
    if "PDF_PAGE_COMPLETENESS" in diagnostics:
        diagnostics.discard("PDF_PAGE_RECORD_COUNT")
        diagnostics.discard("PDF_PAGE_EXTENT")
    if "IMAGE_OCCURRENCE_COMPLETENESS" in diagnostics:
        diagnostics.discard("IMAGE_RECORD_COUNT")
        diagnostics.discard("IMAGE_ATTESTATION_IDENTITY")
    return diagnostics


def run_negative_controls(topology: dict[str, Any], attestation: dict[str, Any]) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    def add(case_id: str, expected: str, observed: set[str]) -> None:
        cases.append({
            "case_id": case_id, "expected_code": expected,
            "observed_codes": sorted(observed), "passed": observed == {expected},
        })
    def diagnose_topology_mutation(mutated_topology: dict[str, Any]) -> set[str]:
        linked_attestation = copy.deepcopy(attestation)
        linked_attestation["source_topology_semantic_sha256"] = sha256(
            canonical_bytes(mutated_topology)
        )
        return content_diagnostics(mutated_topology, linked_attestation)
    try:
        strict_load_bytes(b'{"x":1,"x":2}')
        add("NEG_DUPLICATE_KEY", "JSON_DUPLICATE_KEY", set())
    except DuplicateKeyError:
        add("NEG_DUPLICATE_KEY", "JSON_DUPLICATE_KEY", {"JSON_DUPLICATE_KEY"})
    try:
        strict_load_bytes(b'{"x":NaN}')
        add("NEG_NONFINITE", "JSON_NONFINITE", set())
    except NonFiniteNumberError:
        add("NEG_NONFINITE", "JSON_NONFINITE", {"JSON_NONFINITE"})

    count_fields = [
        "paths", "unique_blobs", "text_files", "text_physical_lines",
        "text_nonblank_lines", "pdf_files", "pdf_pages", "image_occurrences",
        "same_relative_pairs", "same_relative_identical", "same_relative_changed",
    ]
    for field in count_fields:
        mutated = copy.deepcopy(topology)
        mutated["counts"][field] += 1
        code = f"TOPOLOGY_COUNT_{field.upper()}"
        add(f"NEG_{code}", code, diagnose_topology_mutation(mutated))
    mutated = copy.deepcopy(topology)
    mutated["path_set_sha256"] = "0" * 64
    add("NEG_PATH_SET_HASH", "PATH_SET_HASH", diagnose_topology_mutation(mutated))
    mutated = copy.deepcopy(topology)
    mutated["authority_group_counts"]["FINAL_RELEASE_SURFACE"] += 1
    add("NEG_AUTHORITY_GROUPS", "AUTHORITY_GROUP_COUNTS", diagnose_topology_mutation(mutated))
    mutated = copy.deepcopy(topology)
    mutated["duplicates"][0]["blob_sha1"] = "0" * 40
    add("NEG_DUPLICATE_GROUP", "DUPLICATE_GROUP", diagnose_topology_mutation(mutated))
    mutated = copy.deepcopy(topology)
    mutated["authority_boundary"] = "mutated"
    add("NEG_TOPOLOGY_AUTHORITY", "TOPOLOGY_AUTHORITY_BOUNDARY", diagnose_topology_mutation(mutated))
    mutated = copy.deepcopy(topology)
    mutated_pair = mutated["same_relative_v1019_v1020"][0]
    mutated_pair["blob_relation"] = (
        "CHANGED"
        if mutated_pair["blob_relation"] == "IDENTICAL"
        else "IDENTICAL"
    )
    mutated_source = next(
        row for row in mutated["sources"] if row["path"] == mutated_pair["v1020_path"]
    )
    mutated_source["v1019_overlap_class"] = (
        "IDENTICAL_OVERLAP" if mutated_pair["blob_relation"] == "IDENTICAL"
        else "NEW_BLOB_OR_SOURCE"
    )
    mutated_source["v1019_path_relation"] = (
        "IDENTICAL_SAME_RELATIVE" if mutated_pair["blob_relation"] == "IDENTICAL"
        else "CHANGED_SAME_RELATIVE"
    )
    add("NEG_SAME_RELATIVE_GENEALOGY", "SAME_RELATIVE_GENEALOGY", diagnose_topology_mutation(mutated))

    att_count_fields = [
        "text_files", "text_physical_lines", "text_nonblank_lines",
        "pdf_files", "pdf_pages", "image_occurrences",
        "human_partitions_complete", "human_partitions_total",
    ]
    for field in att_count_fields:
        mutated = copy.deepcopy(attestation)
        mutated["counts"][field] += 1
        code = f"ATTESTATION_COUNT_{field.upper()}"
        add(f"NEG_{code}", code, content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["partitions"][0]["status"] = "PENDING_HUMAN_REVIEW"
    add("NEG_HUMAN_PARTITION", "HUMAN_PARTITION_STATUS", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["text_records"][0]["human_read_state"] = "PENDING_HUMAN_REVIEW"
    add("NEG_HUMAN_TEXT", "HUMAN_TEXT_STATE", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["pdf_records"][0]["visual_review_state"] = "PENDING_HUMAN_REVIEW"
    add("NEG_HUMAN_PDF", "HUMAN_PDF_STATE", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["pdf_records"][0]["pages"][0]["visual_state"] = "PENDING_HUMAN_REVIEW"
    add("NEG_HUMAN_PDF_PAGE", "HUMAN_PDF_PAGE_STATE", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["image_records"][0]["visual_review_state"] = "PENDING_HUMAN_REVIEW"
    add("NEG_HUMAN_IMAGE", "HUMAN_IMAGE_STATE", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["source_topology_semantic_sha256"] = "0" * 64
    add("NEG_TOPOLOGY_LINK", "TOPOLOGY_ATTESTATION_LINK", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["authority_boundary"] = "mutated"
    add("NEG_ATTEST_AUTHORITY", "ATTESTATION_AUTHORITY_BOUNDARY", content_diagnostics(topology, mutated))
    for records_key, case_id, expected_code in [
        ("text_records", "NEG_TEXT_ATTESTATION_IDENTITY", "TEXT_ATTESTATION_IDENTITY"),
        ("pdf_records", "NEG_PDF_ATTESTATION_IDENTITY", "PDF_ATTESTATION_IDENTITY"),
        ("image_records", "NEG_IMAGE_ATTESTATION_IDENTITY", "IMAGE_ATTESTATION_IDENTITY"),
    ]:
        mutated = copy.deepcopy(attestation)
        mutated[records_key][0]["source_id"] = mutated[records_key][1]["source_id"]
        add(case_id, expected_code, content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["pdf_records"][0]["pages"][0]["page"] = 2
    add("NEG_PDF_PAGE_EXTENT", "PDF_PAGE_EXTENT", content_diagnostics(topology, mutated))
    mutated = copy.deepcopy(attestation)
    mutated["text_records"][0]["physical_lines"] += 1
    add("NEG_ATTESTATION_EXTENT_TOTALS", "ATTESTATION_EXTENT_TOTALS", content_diagnostics(topology, mutated))

    mutated_topology = copy.deepcopy(topology)
    mutated_attestation = copy.deepcopy(attestation)
    missing_path = "Claude/docs/v1.0.20/__missing_source__.tex"
    no_pair_source = next(
        row for row in mutated_topology["sources"]
        if row["v1019_path_relation"] == "NO_SAME_RELATIVE_SOURCE"
    )
    original_source_id = no_pair_source["source_id"]
    no_pair_source["path"] = missing_path
    no_pair_source["basename"] = PurePosixPath(missing_path).name
    mutated_topology["path_set_sha256"] = sha256((
        "\n".join(sorted(row["path"] for row in mutated_topology["sources"])) + "\n"
    ).encode("utf-8"))
    mutated_text_record = next(
        row for row in mutated_attestation["text_records"]
        if row["source_id"] == original_source_id
    )
    mutated_text_record["path"] = missing_path
    mutated_attestation["source_topology_semantic_sha256"] = sha256(canonical_bytes(mutated_topology))
    add(
        "NEG_MISSING_PATH", "SOURCE_PATH_IDENTITY",
        content_diagnostics(mutated_topology, mutated_attestation, topology, attestation),
    )
    mutated_topology = copy.deepcopy(topology)
    no_pair_source = next(
        row for row in mutated_topology["sources"]
        if row["v1019_path_relation"] == "NO_SAME_RELATIVE_SOURCE"
    )
    no_pair_source["blob_sha1"] = "0" * 40
    linked = copy.deepcopy(attestation)
    linked["source_topology_semantic_sha256"] = sha256(canonical_bytes(mutated_topology))
    add(
        "NEG_BLOB_MISMATCH", "SOURCE_BLOB_IDENTITY",
        content_diagnostics(mutated_topology, linked, topology, attestation),
    )
    mutated_topology = copy.deepcopy(topology)
    pair = mutated_topology["same_relative_v1019_v1020"][0]
    pair["v1019_path"] = "Claude/docs/v1.0.19/__wrong_pair__.tex"
    source = next(row for row in mutated_topology["sources"] if row["path"] == pair["v1020_path"])
    source["v1019_same_relative_path"] = pair["v1019_path"]
    linked = copy.deepcopy(attestation)
    linked["source_topology_semantic_sha256"] = sha256(canonical_bytes(mutated_topology))
    add(
        "NEG_WRONG_OLD_NEW_PAIRING", "SAME_RELATIVE_PAIRING",
        content_diagnostics(mutated_topology, linked, topology, attestation),
    )
    mutated = copy.deepcopy(attestation)
    mutated["text_records"][0]["physical_lines"] -= 1
    add(
        "NEG_MISSING_TEXT_LINE", "TEXT_SOURCE_EXTENT",
        content_diagnostics(topology, mutated, topology, attestation),
    )
    mutated = copy.deepcopy(attestation)
    mutated["pdf_records"][0]["pages"].pop()
    add(
        "NEG_MISSING_PDF_PAGE", "PDF_PAGE_COMPLETENESS",
        content_diagnostics(topology, mutated, topology, attestation),
    )
    mutated = copy.deepcopy(attestation)
    mutated["image_records"].pop()
    add(
        "NEG_MISSING_IMAGE_OCCURRENCE", "IMAGE_OCCURRENCE_COMPLETENESS",
        content_diagnostics(topology, mutated, topology, attestation),
    )
    result_text = RESULT.read_text(encoding="utf-8")
    mutated_result = result_text.replace(
        "Gate: `PASS_P061_STEP46_SOURCE_TOPOLOGY`", "Gate: `MUTATED`", 1
    )
    add(
        "NEG_RESULT_CONTRACT", "RESULT_CONTRACT",
        result_diagnostics(mutated_result, topology, attestation),
    )
    _, repository = repository_diagnostics()
    mutated_repository = copy.deepcopy(repository)
    mutated_repository["dirty_paths"].append("Codex/results/__unexpected__.txt")
    add(
        "NEG_EXTRA_DIRTY_PATH", "REPOSITORY_EXACT_EIGHT_DIRT",
        evaluate_repository_state(mutated_repository),
    )
    mutated_repository = copy.deepcopy(repository)
    mutated_repository["protected_live"] = "0" * 40
    add(
        "NEG_PROTECTED_DRIFT", "REPOSITORY_PROTECTED_STATE",
        evaluate_repository_state(mutated_repository),
    )
    active_text = ACTIVE_LEDGER.read_text(encoding="utf-8")
    parent_text = PARENT_LEDGER.read_text(encoding="utf-8")
    handover_text = HANDOVER.read_text(encoding="utf-8")
    mutated_active = active_text.replace("negative 48/48", "negative 47/47", 1)
    add(
        "NEG_STALE_CONTROL_COUNT", "CONTROL_ACTIVE_LEDGER",
        control_diagnostics(mutated_active, parent_text, handover_text),
    )
    return {
        "total": len(cases), "passed": sum(row["passed"] for row in cases),
        "failed": [row["case_id"] for row in cases if not row["passed"]],
        "cases": cases,
    }


def result_diagnostics(text: str, topology: dict[str, Any], attestation: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    required = [
        "Gate: `PASS_P061_STEP46_SOURCE_TOPOLOGY`",
        "232 / 232", "231", "195 / 31,553 / 29,335", "14 / 130", "23",
        sha256(normalize_lf(TOPOLOGY)), sha256(normalize_lf(ATTESTATION)),
        sha256(normalize_lf(BUILDER)), sha256(normalize_lf(VALIDATOR)),
        "primary-reference/DOI truth", "GROUND_NOT_FOUND", "UNVERIFIED",
        "audit(phase061): freeze v1020 source topology",
        EXPECTED_PARENT, "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "Only after `PASS_P061_STEP46_PERSISTENCE` may Step 47 begin",
        f"PASS_P061_STEP46_NEGATIVE_CONTROLS 48/48",
        "PASS_P061_STEP46_DETERMINISM 2/2",
    ]
    if not all(token in text for token in required):
        diagnostics.add("RESULT_CONTRACT")
    if topology.get("counts", {}).get("v1019_identical_overlap") != 18 or topology.get("counts", {}).get("v1019_new_blob_or_source") != 214:
        diagnostics.add("RESULT_SOURCE_CONTRACT")
    if attestation.get("status") != "PASS_FULL_READ_ATTESTATION":
        diagnostics.add("RESULT_ATTESTATION_CONTRACT")
    return diagnostics


def control_diagnostics(
    active_text: str | None = None, parent_text: str | None = None,
    handover_text: str | None = None,
) -> set[str]:
    diagnostics: set[str] = set()
    active = active_text if active_text is not None else (
        ACTIVE_LEDGER.read_text(encoding="utf-8") if ACTIVE_LEDGER.exists() else ""
    )
    parent = parent_text if parent_text is not None else (
        PARENT_LEDGER.read_text(encoding="utf-8") if PARENT_LEDGER.exists() else ""
    )
    handover = handover_text if handover_text is not None else (
        HANDOVER.read_text(encoding="utf-8") if HANDOVER.exists() else ""
    )
    active_rows = [line for line in active.splitlines() if line.startswith("| 061 |")]
    parent_rows = [line for line in parent.splitlines() if line.startswith("| 061 |")]
    active_tokens = [
        "| IN_PROGRESS |", "plan activation; Step 46", RESULT.relative_to(REPO).as_posix(),
        TOPOLOGY.relative_to(REPO).as_posix(), ATTESTATION.relative_to(REPO).as_posix(),
        "PASS_P061_STEP46_SOURCE_TOPOLOGY",
        "Step 47 after Step 46 atomic commit/push/remote verification",
    ]
    parent_tokens = [
        "| IN_PROGRESS |", "plan activation; Step 46", RESULT.relative_to(REPO).as_posix(),
        TOPOLOGY.relative_to(REPO).as_posix(), ATTESTATION.relative_to(REPO).as_posix(),
        "PASS_P061_STEP46_SOURCE_TOPOLOGY",
        "Step 47 after Step 46 commit/push/remote verification",
    ]
    if (
        len(active_rows) != 1 or not all(token in active_rows[0] for token in active_tokens)
        or "negative 48/48" not in active
    ):
        diagnostics.add("CONTROL_ACTIVE_LEDGER")
    if (
        len(parent_rows) != 1 or not all(token in parent_rows[0] for token in parent_tokens)
        or "negative 48/48" not in parent_rows[0]
    ):
        diagnostics.add("CONTROL_PARENT_LEDGER")
    handover_tokens = [
        "Phase 061 `IN_PROGRESS`, Step 46 source topology/full-read attestation",
        f"현재 result: `{RESULT.relative_to(REPO).as_posix()}`",
        f"현재 machine evidence: `{TOPOLOGY.relative_to(REPO).as_posix()}`; `{ATTESTATION.relative_to(REPO).as_posix()}`",
        f"Phase 061 detailed plan activation | Steps 46–51 planning boundary | `PASS_P061_PLAN_ACTIVATION`; exact-seven commit `{EXPECTED_PARENT}` pushed and remote-verified",
        "Phase 061 Step 46 | Step 46 | `PASS_P061_STEP46_SOURCE_TOPOLOGY`; exact-eight containing checkpoint `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "exactly the eight Phase 061 Step 46 paths",
        "Step 47 is blocked until Step 46 commit/push/remote verification passes",
    ]
    if not all(token in handover for token in handover_tokens) or "negative 48/48" not in handover:
        diagnostics.add("CONTROL_HANDOVER")
    return diagnostics


def evaluate_repository_state(evidence: dict[str, Any], require_exact_dirt: bool = True) -> set[str]:
    diagnostics: set[str] = set()
    if not (
        evidence["branch"] == ACTIVE_BRANCH
        and evidence["head"] == evidence["upstream"] == evidence["origin_tracking"]
        == evidence["live_active"] == EXPECTED_PARENT
    ):
        diagnostics.add("REPOSITORY_ACTIVE_STATE")
    if evidence["protected_local"] != evidence["protected_live"] or evidence["protected_live"] != EXPECTED_PROTECTED:
        diagnostics.add("REPOSITORY_PROTECTED_STATE")
    if evidence["main_local"] != evidence["main_live"] or evidence["main_live"] != EXPECTED_MAIN:
        diagnostics.add("REPOSITORY_MAIN_STATE")
    if evidence["claude_diff"] or any(path.startswith("Claude/") for path in evidence["porcelain_paths"]):
        diagnostics.add("REPOSITORY_CLAUDE_DRIFT")
    if require_exact_dirt and set(evidence["dirty_paths"]) != EXACT_EIGHT_SET:
        diagnostics.add("REPOSITORY_EXACT_EIGHT_DIRT")
    return diagnostics


def repository_diagnostics(require_exact_dirt: bool = True) -> tuple[set[str], dict[str, Any]]:
    branch = run_git("branch", "--show-current")
    head = run_git("rev-parse", "HEAD")
    upstream = run_git("rev-parse", "@{upstream}")
    origin_tracking = run_git("rev-parse", f"origin/{ACTIVE_BRANCH}")
    live_active = remote_tip(ACTIVE_BRANCH)
    protected_local = run_git("rev-parse", f"origin/{PROTECTED_BRANCH}")
    protected_live = remote_tip(PROTECTED_BRANCH)
    main_local = run_git("rev-parse", "origin/main")
    main_live = remote_tip("main")
    claude_diff = run_git("diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude")
    dirty = exact_dirty_paths()
    evidence = {
        "branch": branch, "head": head, "upstream": upstream,
        "origin_tracking": origin_tracking, "live_active": live_active,
        "protected_local": protected_local, "protected_live": protected_live,
        "main_local": main_local, "main_live": main_live,
        "claude_diff": claude_diff.splitlines() if claude_diff else [],
        "porcelain_paths": sorted(porcelain_paths()),
        "dirty_paths": sorted(dirty),
    }
    return evaluate_repository_state(evidence, require_exact_dirt), evidence


def validate(content_only: bool = False) -> tuple[set[str], dict[str, Any]]:
    diagnostics: set[str] = set()
    evidence: dict[str, Any] = {}
    missing = [path.relative_to(REPO).as_posix() for path in (TOPOLOGY, ATTESTATION) if not path.exists()]
    if missing:
        diagnostics.add("STEP46_MISSING_ARTIFACT")
        evidence["missing"] = missing
        return diagnostics, evidence
    topology, top_stats = strict_load(TOPOLOGY)
    attestation, att_stats = strict_load(ATTESTATION)
    builder = load_builder_module()
    rebuilt_topology, rebuilt_attestation = builder.build()
    diagnostics |= content_diagnostics(
        topology, attestation, rebuilt_topology, rebuilt_attestation
    )
    if topology != rebuilt_topology:
        diagnostics.add("TOPOLOGY_REBUILD_MISMATCH")
    if attestation != rebuilt_attestation:
        diagnostics.add("ATTESTATION_REBUILD_MISMATCH")
    if topology.get("builder", {}).get("normalized_sha256") != sha256(normalize_lf(BUILDER)):
        diagnostics.add("BUILDER_HASH_MISMATCH")
    evidence.update({
        "topology_traversal": top_stats,
        "attestation_traversal": att_stats,
        "topology_normalized_sha256": sha256(normalize_lf(TOPOLOGY)),
        "attestation_normalized_sha256": sha256(normalize_lf(ATTESTATION)),
        "builder_normalized_sha256": sha256(normalize_lf(BUILDER)),
        "validator_normalized_sha256": sha256(normalize_lf(VALIDATOR)),
    })
    if not content_only:
        if not RESULT.exists():
            diagnostics.add("STEP46_RESULT_MISSING")
        else:
            diagnostics |= result_diagnostics(
                RESULT.read_text(encoding="utf-8"), topology, attestation
            )
        diagnostics |= control_diagnostics()
        repo_diag, repo_evidence = repository_diagnostics()
        diagnostics |= repo_diag
        evidence["repository"] = repo_evidence
    return diagnostics, evidence


def verify_staged() -> int:
    diagnostics, _ = validate()
    staged = nul_paths("diff", "--cached", "--name-only", "-z")
    unstaged = nul_paths("diff", "--name-only", "-z")
    dirty = exact_dirty_paths()
    if staged != EXACT_EIGHT_SET or unstaged or dirty != EXACT_EIGHT_SET:
        diagnostics.add("STAGED_EXACT_EIGHT")
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        return 1
    print("PASS_P061_STEP46_STAGED 8/8")
    return 0


def verify_persistence() -> int:
    diagnostics: set[str] = set()
    if not TOPOLOGY.exists() or not ATTESTATION.exists():
        diagnostics.add("PERSISTENCE_ARTIFACT_MISSING")
    else:
        topology, _ = strict_load(TOPOLOGY)
        attestation, _ = strict_load(ATTESTATION)
        builder = load_builder_module()
        expected_topology, expected_attestation = builder.build()
        diagnostics |= content_diagnostics(
            topology, attestation, expected_topology, expected_attestation
        )
        if topology != expected_topology:
            diagnostics.add("PERSISTENCE_TOPOLOGY_REBUILD")
        if attestation != expected_attestation:
            diagnostics.add("PERSISTENCE_ATTESTATION_REBUILD")
    head = run_git("rev-parse", "HEAD")
    parent = run_git("rev-parse", "HEAD^")
    subject = run_git("show", "-s", "--format=%s", "HEAD")
    committed = nul_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD")
    branch = run_git("branch", "--show-current")
    upstream = run_git("rev-parse", "@{upstream}")
    origin_tracking = run_git("rev-parse", f"origin/{ACTIVE_BRANCH}")
    live_active = remote_tip(ACTIVE_BRANCH)
    protected_local = run_git("rev-parse", f"origin/{PROTECTED_BRANCH}")
    protected_live = remote_tip(PROTECTED_BRANCH)
    main_local = run_git("rev-parse", "origin/main")
    main_live = remote_tip("main")
    claude_diff = run_git("diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude")
    if parent != EXPECTED_PARENT:
        diagnostics.add("PERSISTENCE_PARENT")
    if subject != EXPECTED_SUBJECT:
        diagnostics.add("PERSISTENCE_SUBJECT")
    if committed != EXACT_EIGHT_SET:
        diagnostics.add("PERSISTENCE_EXACT_EIGHT")
    if porcelain_paths():
        diagnostics.add("PERSISTENCE_DIRTY")
    if not (branch == ACTIVE_BRANCH and head == upstream == origin_tracking == live_active):
        diagnostics.add("PERSISTENCE_ACTIVE_REMOTE")
    if protected_local != protected_live or protected_live != EXPECTED_PROTECTED:
        diagnostics.add("PERSISTENCE_PROTECTED")
    if main_local != main_live or main_live != EXPECTED_MAIN:
        diagnostics.add("PERSISTENCE_MAIN")
    if claude_diff:
        diagnostics.add("PERSISTENCE_CLAUDE")
    if run_git("diff", "--check"):
        diagnostics.add("PERSISTENCE_DIFF_CHECK")
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        return 1
    print(f"PASS_P061_STEP46_PERSISTENCE head={head}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    args = parser.parse_args()
    if args.verify_staged:
        return verify_staged()
    if args.verify_persistence:
        return verify_persistence()
    diagnostics, evidence = validate(content_only=args.content_only)
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        print(f"FAIL_P061_STEP46_SOURCE_TOPOLOGY diagnostics={len(diagnostics)}")
        return 1
    topology, _ = strict_load(TOPOLOGY)
    attestation, _ = strict_load(ATTESTATION)
    if args.run_negative_probes:
        negatives = run_negative_controls(topology, attestation)
        if negatives["failed"]:
            print("FAIL STEP46_NEGATIVE_CONTROLS " + " ".join(negatives["failed"]))
            return 1
        print(f"PASS_P061_STEP46_NEGATIVE_CONTROLS {negatives['passed']}/{negatives['total']}")
    if args.determinism_check:
        builder = load_builder_module()
        first_topology, first_attestation = builder.build()
        second_topology, second_attestation = builder.build()
        if canonical_bytes(first_topology) != canonical_bytes(second_topology) or canonical_bytes(first_attestation) != canonical_bytes(second_attestation):
            print("FAIL STEP46_DETERMINISM")
            return 1
        print("PASS_P061_STEP46_DETERMINISM 2/2")
    print(
        "PASS_P061_STEP46_SOURCE_TOPOLOGY "
        f"paths={topology['counts']['paths']} text={attestation['counts']['text_files']}/{attestation['counts']['text_physical_lines']} "
        f"pdf={attestation['counts']['pdf_files']}/{attestation['counts']['pdf_pages']} image={attestation['counts']['image_occurrences']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
