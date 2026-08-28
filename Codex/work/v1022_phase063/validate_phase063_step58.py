#!/usr/bin/env python3
"""Validate Phase 063 Step 58 source/process topology and read attestation."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
VALIDATOR = Path(__file__).resolve()
BUILDER = REPO / "Codex/work/v1022_phase063/build_phase063_step58_source_process_topology.py"
TOPOLOGY = REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION = REPO / "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_058_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
ACTIVATION = "4e7686ec623a2e82a0ef5433e60a8565b0ad039f"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase063): freeze v1022 source process topology"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
EXPECTED_BUILDER_SHA256 = "e873cac7f32d177b5a63e97b89c7a26e2e9dcf025147f9d81c0badc6bf71d6a9"
TIMEOUT = 300
HUMAN_EVIDENCE_BEGIN = "<!-- P063_STEP58_HUMAN_EVIDENCE_BEGIN -->"
HUMAN_EVIDENCE_END = "<!-- P063_STEP58_HUMAN_EVIDENCE_END -->"

EXACT_EIGHT = (
    "Codex/work/v1022_phase063/build_phase063_step58_source_process_topology.py",
    "Codex/work/v1022_phase063/validate_phase063_step58.py",
    "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json",
    "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json",
    "Codex/results/PHASE_063_STEP_058_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_EIGHT_SET = set(EXACT_EIGHT)
CONTROL_SHA256 = {
    "result": "8b9a7d4f3276af54796a82dfcef6885b5b8cf23df20822b601f24950152af180",
    "active_ledger": "870765fa0d1e4a26e2a5ad8f0434b4a63f1727f053d2c7a48ff3b8e236c16955",
    "parent_ledger": "7fa370d8d98032f13a1adabc7f1fb7741e6dc40b6998c3885f26defc9d3caeb2",
    "handover": "c69b1a2605f46a7e453fa9b56b7a5a9403d9690ca6c7a3772ff2a5fb755a6c19",
}

EXPECTED_COUNTS = {
    "source_occurrences": 204,
    "unique_paths": 204,
    "unique_blobs": 204,
    "bytes": 4_974_148,
    "review_modes": {"FULL_PDF": 4, "FULL_TEXT": 200},
    "text_physical_lines": 30_219,
    "text_nonblank_lines": 26_137,
    "pdf_pages": 133,
    "partition_counts": {
        "COMPETING_REVIEW_CANDIDATE": 125,
        "FINAL_RELEASE_SURFACE": 63,
        "STATUS_MACHINE_PROCESS": 10,
        "VERSION_PLAN": 6,
    },
    "partition_bytes": {
        "COMPETING_REVIEW_CANDIDATE": 1_800_475,
        "FINAL_RELEASE_SURFACE": 2_985_072,
        "STATUS_MACHINE_PROCESS": 158_352,
        "VERSION_PLAN": 30_249,
    },
    "partition_physical_lines": {
        "COMPETING_REVIEW_CANDIDATE": 17_072,
        "FINAL_RELEASE_SURFACE": 10_462,
        "STATUS_MACHINE_PROCESS": 2_398,
        "VERSION_PLAN": 287,
    },
    "partition_nonblank_lines": {
        "COMPETING_REVIEW_CANDIDATE": 13_926,
        "FINAL_RELEASE_SURFACE": 9_733,
        "STATUS_MACHINE_PROCESS": 2_236,
        "VERSION_PLAN": 242,
    },
    "partition_pdf_pages": {"FINAL_RELEASE_SURFACE": 133},
    "history_commits": 100,
    "observation_inputs": 11,
    "finding_routes": 96,
    "finding_source_candidates": 15,
    "finding_observation_only": 81,
    "process_findings": 7,
    "release_findings": 10,
    "competing_findings": 21,
    "competing_authority_subtypes": {
        "C_CANDIDATE_PROPOSAL_OR_DRAFT": 58,
        "D_DECISION_TRIAGE_OR_EXECUTION_RECORD": 9,
        "R_REVIEW_OR_SURVEY": 46,
        "S_SELF_REPORT_OR_STATUS": 4,
        "T_TASK_OR_BRIEF": 8,
    },
}


class ValidationError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def strict_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"non-finite JSON number: {value}")
    return number


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def traverse(value: Any) -> int:
    if value is None or isinstance(value, (str, bool, int)):
        return 1
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite JSON number")
        return 1
    if isinstance(value, list):
        return 1 + sum(traverse(item) for item in value)
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("non-string JSON key")
        return 1 + sum(1 + traverse(item) for item in value.values())
    raise ValueError(f"unsupported JSON node: {type(value).__name__}")


def strict_load(path: Path) -> tuple[Any, int]:
    return strict_load_text(path.read_text(encoding="utf-8"))


def strict_load_text(text: str) -> tuple[Any, int]:
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
        parse_float=strict_float,
    )
    return value, traverse(value)


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def human_review_evidence() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(HUMAN_EVIDENCE_BEGIN) != 1 or text.count(HUMAN_EVIDENCE_END) != 1:
        raise ValidationError("human-review evidence marker cardinality")
    block = text.split(HUMAN_EVIDENCE_BEGIN, 1)[1].split(HUMAN_EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise ValidationError("human-review evidence fence")
    evidence, _ = strict_load_text(block[len("```json\n"):-len("\n```")])
    if not isinstance(evidence, dict):
        raise ValidationError("human-review evidence root")
    return evidence, digest(compact(evidence))


def run(args: list[str], timeout: int = TIMEOUT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)


def git_bytes(*args: str, check: bool = True) -> bytes:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise ValidationError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def git_text(*args: str, check: bool = True) -> str:
    return git_bytes(*args, check=check).decode("utf-8", errors="strict").strip()


def git_paths(*args: str) -> set[str]:
    return {item.decode("utf-8").replace("\\", "/") for item in git_bytes(*args).split(b"\0") if item}


def ref_hash(ref: str) -> str | None:
    value = git_text("show-ref", "--verify", "--hash", ref, check=False)
    return value or None


def remote_head(branch: str) -> str:
    ref = f"refs/heads/{branch}"
    rows = [line.split() for line in git_text("ls-remote", "--heads", "origin", ref).splitlines() if line.strip()]
    if len(rows) != 1 or rows[0][1] != ref:
        raise ValidationError(f"remote head cardinality: {branch}: {rows}")
    return rows[0][0]


def run_builder() -> tuple[dict[str, Any], dict[str, Any], bytes, bytes, int, int]:
    with tempfile.TemporaryDirectory(prefix="p063-step58-") as directory:
        proc = run([sys.executable, str(BUILDER), "--output-dir", directory])
        if proc.returncode:
            raise ValidationError(
                f"builder failed ({proc.returncode}): "
                f"{proc.stdout.decode('utf-8', errors='replace')} {proc.stderr.decode('utf-8', errors='replace')}"
            )
        top_path = Path(directory) / TOPOLOGY.name
        att_path = Path(directory) / ATTESTATION.name
        top, top_nodes = strict_load(top_path)
        att, att_nodes = strict_load(att_path)
        return top, att, top_path.read_bytes(), att_path.read_bytes(), top_nodes, att_nodes


def add(errors: set[str], condition: bool, code: str) -> None:
    if condition:
        errors.add(code)


def artifact_diagnostics(top: dict[str, Any], att: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    add(errors, top.get("schema_version") != 1, "TOP_SCHEMA")
    add(errors, top.get("artifact_kind") != "V1022_SOURCE_PROCESS_TOPOLOGY", "TOP_KIND")
    add(errors, top.get("phase") != 63 or top.get("step") != 58, "TOP_PHASE_STEP")
    add(errors, top.get("gate") != "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY", "TOP_GATE")
    add(errors, top.get("baseline_commit") != BASELINE, "TOP_BASELINE")
    add(errors, top.get("activation_commit") != ACTIVATION, "TOP_ACTIVATION")
    add(errors, top.get("builder", {}).get("path") != EXACT_EIGHT[0], "TOP_BUILDER_PATH")
    add(errors, top.get("builder", {}).get("sha256") != EXPECTED_BUILDER_SHA256, "TOP_BUILDER_SHA")
    add(errors, top.get("manifest", {}).get("normalized_sha256") != MANIFEST_SHA256, "TOP_MANIFEST_SHA")
    for key, expected in EXPECTED_COUNTS.items():
        add(errors, top.get("counts", {}).get(key) != expected, "TOP_COUNT_" + key.upper())
    policy = top.get("denominator_policy", {})
    add(errors, policy.get("manifest_occurrences") != 204, "TOP_DENOMINATOR_MANIFEST")
    add(errors, policy.get("supplemental_process_control_occurrences") != 1, "TOP_DENOMINATOR_SUPPLEMENTAL")
    add(errors, policy.get("denominator_fusion_forbidden") is not True, "TOP_DENOMINATOR_FUSION")

    sources = top.get("sources")
    if not isinstance(sources, list):
        errors.add("TOP_SOURCE_ROWS")
        sources = []
    add(errors, len(sources) != 204, "TOP_SOURCE_ROWS")
    ids = [row.get("source_id") for row in sources if isinstance(row, dict)]
    source_by_id = {row.get("source_id"): row for row in sources if isinstance(row, dict)}
    source_by_path = {row.get("path"): row for row in sources if isinstance(row, dict)}
    add(errors, ids != [f"P063-SRC-{number:04d}" for number in range(1, 205)], "TOP_SOURCE_ID_SEQUENCE")
    paths = [row.get("path") for row in sources if isinstance(row, dict)]
    blobs = [row.get("blob_sha1") for row in sources if isinstance(row, dict)]
    add(errors, len(paths) != len(set(paths)), "TOP_SOURCE_PATH_UNIQUE")
    add(errors, len(blobs) != len(set(blobs)), "TOP_SOURCE_BLOB_UNIQUE")
    add(errors, [row.get("manifest_index") for row in sources] != list(range(540, 744)), "TOP_MANIFEST_INDEX_SEQUENCE")
    valid_authorities = {
        "FINAL_RELEASE_SURFACE": "FROZEN_RELEASE_CONTENT_OR_BUILD_ONLY",
        "VERSION_PLAN": "PROCESS_INTENT_ONLY",
        "STATUS_MACHINE_PROCESS": "SELF_REPORT_OR_MACHINE_STRUCTURE_ONLY",
        "COMPETING_REVIEW_CANDIDATE": "PROPOSAL_REVIEW_EVIDENCE_ONLY",
    }
    add(errors, any(valid_authorities.get(row.get("partition")) != row.get("authority_ceiling") for row in sources), "TOP_SOURCE_AUTHORITY")
    add(errors, any(not row.get("touch_commits") or row.get("first_add_commit") not in row.get("touch_commits", []) or row.get("last_touch_commit") != row.get("touch_commits", [])[-1] for row in sources), "TOP_SOURCE_HISTORY_LINK")
    competing = [row for row in sources if row.get("partition") == "COMPETING_REVIEW_CANDIDATE"]
    observed_subtypes: dict[str, int] = {}
    for row in competing:
        subtype = row.get("process_authority_subtype")
        observed_subtypes[subtype] = observed_subtypes.get(subtype, 0) + 1
    add(errors, observed_subtypes != EXPECTED_COUNTS["competing_authority_subtypes"], "TOP_COMPETING_SUBTYPES")
    add(errors, any(row.get("final_adoption_authority") is not False for row in competing), "TOP_COMPETING_ADOPTION_AUTHORITY")

    commits = top.get("commit_genealogy")
    if not isinstance(commits, list):
        errors.add("TOP_COMMIT_ROWS")
        commits = []
    add(errors, len(commits) != 100, "TOP_COMMIT_ROWS")
    add(errors, [row.get("event_id") for row in commits] != [f"P063-COMMIT-{number:03d}" for number in range(1, 101)], "TOP_COMMIT_ID_SEQUENCE")
    add(errors, len({row.get("commit") for row in commits}) != len(commits), "TOP_COMMIT_UNIQUE")
    add(errors, any(not isinstance(row.get("changed_paths"), list) or not row.get("changed_paths") for row in commits), "TOP_COMMIT_PATHS")
    history = top.get("history_summary", {})
    observed_single_parent = all(len(row.get("parents", [])) == 1 for row in commits)
    add(errors, history.get("all_single_parent") is not observed_single_parent or not observed_single_parent, "TOP_HISTORY_PARENT_CARDINALITY")
    observed_gaps = []
    for previous, current in zip(commits, commits[1:]):
        if previous.get("commit") not in current.get("parents", []):
            observed_gaps.append({
                "previous_touch_commit": previous.get("commit"),
                "current_touch_commit": current.get("commit"),
                "current_true_parents": current.get("parents"),
            })
    add(errors, history.get("filtered_adjacent_true_parent_count") != len(commits) - 1 - len(observed_gaps) or history.get("filtered_adjacency_gaps") != observed_gaps, "TOP_HISTORY_FILTERED_GAPS")
    observed_path_events = dict(sorted(Counter(
        change.get("status", "")[:1] for row in commits for change in row.get("changed_paths", [])
    ).items()))
    add(errors, history.get("path_event_counts") != observed_path_events or observed_path_events != {"A": 204, "M": 290}, "TOP_HISTORY_PATH_EVENTS")
    genealogy_projection = [
        {
            "index": index,
            "commit": row.get("commit"),
            "parents": row.get("parents"),
            "author_time": row.get("author_time"),
            "committer_time": row.get("committer_time"),
            "subject": row.get("subject"),
            "changes": row.get("changed_paths"),
        }
        for index, row in enumerate(commits, start=1)
    ]
    add(errors, history.get("genealogy_projection_sha256") != digest(compact(genealogy_projection)), "TOP_HISTORY_PROJECTION_SHA")
    actor_projection = [
        {
            "event_id": row.get("event_id"),
            "commit": row.get("commit"),
            "repository_actor": row.get("repository_actor"),
            "process_role": row.get("process_role"),
        }
        for row in commits
    ]
    add(errors, history.get("commit_actor_projection_sha256") != digest(compact(actor_projection)), "TOP_HISTORY_ACTOR_PROJECTION_SHA")
    source_history_projection = [
        {
            "source_id": row.get("source_id"),
            "path": row.get("path"),
            "blob_sha1": row.get("blob_sha1"),
            "first_add_commit": row.get("first_add_commit"),
            "first_add_subject": row.get("first_add_subject"),
            "last_touch_commit": row.get("last_touch_commit"),
            "last_touch_subject": row.get("last_touch_subject"),
            "touch_commit_count": row.get("touch_commit_count"),
            "touch_commits": row.get("touch_commits"),
        }
        for row in sources
    ]
    add(errors, history.get("source_history_row_projection_sha256") != digest(compact(source_history_projection)), "TOP_SOURCE_HISTORY_ROW_PROJECTION_SHA")
    add(errors, history.get("source_link_projection_sha256") != "106659376218c830aaf784706f87326300745e011ade2073c9588c59970e76eb", "TOP_SOURCE_LINK_PROJECTION_SHA")

    cross = top.get("cross_version_v1021_v1022", {})
    add(errors, cross.get("same_relative_count") != 42, "TOP_CROSS_SAME_RELATIVE")
    add(errors, cross.get("byte_identical_count") != 5, "TOP_CROSS_IDENTICAL")
    add(errors, cross.get("modified_count") != 37, "TOP_CROSS_MODIFIED")
    add(errors, len(cross.get("raw_v1022_only_relative_paths", [])) != 162, "TOP_CROSS_V1022_ONLY")
    add(errors, len(cross.get("raw_v1021_only_relative_paths", [])) != 26, "TOP_CROSS_V1021_ONLY")
    add(errors, cross.get("shared_blob_count") != 5, "TOP_CROSS_SHARED_BLOBS")
    add(errors, cross.get("identity_namespaces") != {"v1021": {"occurrences": 68}, "v1022": {"occurrences": 204}}, "TOP_CROSS_NAMESPACES")
    relations = cross.get("explicit_relation_rows", [])
    add(errors, [row.get("relation_id") for row in relations] != [f"P063-XVER-{number:03d}" for number in range(1, 5)], "TOP_CROSS_RELATIONS")
    observed_relation_counts = dict(sorted(Counter(row.get("relation") for row in relations).items()))
    add(errors, cross.get("explicit_relation_counts") != {"RENAMED": 2, "SPLIT": 2} or cross.get("explicit_relation_counts") != observed_relation_counts, "TOP_CROSS_RELATIONS")
    cross_evidence_invalid = False
    for row in relations:
        for evidence in row.get("process_evidence", []):
            source = source_by_id.get(evidence.get("source_id"))
            if source is None or source.get("path") != evidence.get("path") or source.get("blob_sha1") != evidence.get("blob_sha1"):
                cross_evidence_invalid = True
                continue
            for interval in evidence.get("line_intervals", []):
                if interval[0] < 1 or interval[1] < interval[0] or interval[1] > source.get("extent", {}).get("lines", 0):
                    cross_evidence_invalid = True
    add(errors, cross_evidence_invalid, "TOP_CROSS_RELATION_EVIDENCE")
    old_relation_paths = [item.get("relative_path") for row in relations for item in row.get("v1021_sources", [])]
    new_relation_paths = [item.get("relative_path") for row in relations for item in row.get("v1022_sources", [])]
    not_carried = cross.get("not_carried_forward_relative_paths", [])
    new_paths = cross.get("new_relative_paths", [])
    coverage = cross.get("coverage", {})
    add(errors, len(old_relation_paths) != 6 or len(set(old_relation_paths)) != 6 or len(not_carried) != 20 or len(set(not_carried)) != 20 or set(old_relation_paths) & set(not_carried), "TOP_CROSS_PRIMARY_COVERAGE")
    add(errors, len(new_relation_paths) != 8 or len(set(new_relation_paths)) != 8 or len(new_paths) != 154 or len(set(new_paths)) != 154 or set(new_relation_paths) & set(new_paths), "TOP_CROSS_PRIMARY_COVERAGE")
    add(errors, coverage != {"same_relative_shared_blob_secondary_overlap": 5, "v1021_exactly_once": True, "v1021_primary_count": 68, "v1022_exactly_once": True, "v1022_primary_count": 204}, "TOP_CROSS_PRIMARY_COVERAGE")
    add(errors, cross.get("removed_not_carried_forward_count") != 20 or digest(compact(not_carried)) != "4996c0855ebf17350062b6a45525cc600135e85b3ff5f446967be9c0abf60e4f", "TOP_CROSS_NOT_CARRIED")
    add(errors, cross.get("new_count") != 154 or digest(compact(new_paths)) != "8d8d04cd0ab416a942fd1dba7e618ce798be4a5b3cf0e21fd0e19e1b09364e46", "TOP_CROSS_NEW")
    add(errors, [item.get("status") for row in relations if row.get("relation") == "RENAMED" for item in row.get("git_copy_detection", [])] != ["C100", "C098"], "TOP_CROSS_RENAME_COPY_EVIDENCE")
    gnf_relations = cross.get("secondary_ground_not_found_relations", [])
    add(errors, [row.get("relation_id") for row in gnf_relations] != ["P063-XVER-GNF-001", "P063-XVER-GNF-002"] or any(row.get("denominator_consuming") is not False or not str(row.get("relation_state", "")).startswith("GROUND_NOT_FOUND") for row in gnf_relations), "TOP_CROSS_GNF_BOUNDARY")
    add(errors, cross.get("frozen_page_mapping_sidecars") != [], "TOP_CROSS_PAGE_SIDECARS")
    add(errors, len(top.get("pdf_root_edges", [])) != 4 or any(row.get("root_state") != "MANIFEST_MEMBER" for row in top.get("pdf_root_edges", [])), "TOP_PDF_ROOT_EDGES")
    add(errors, len(top.get("tex_dependency_edges", [])) != 55 or any(row.get("target_state") != "MANIFEST_MEMBER" for row in top.get("tex_dependency_edges", [])), "TOP_TEX_DEPENDENCY_EDGES")
    tex_summary = top.get("tex_structure_summary", {})
    expected_orphans = [
        "Claude/docs/v1.0.22/_sections/ch1_appD_si.tex",
        "Claude/docs/v1.0.22/_sections/ch1_preamble.tex",
        "Claude/docs/v1.0.22/_sections/ch2_preamble.tex",
    ]
    add(errors, [tex_summary.get(key) for key in ("dependency_edges", "input_occurrences", "unique_input_targets", "external_document_edges", "unresolved_dependency_edges")] != [55, 51, 49, 4, 0], "TOP_TEX_STRUCTURE_COUNTS")
    add(errors, tex_summary.get("manifest_orphan_tex_paths") != expected_orphans, "TOP_TEX_ORPHANS")
    expected_citation = [(39, 39), (15, 15), (34, 34)]
    observed_citation = [(row.get("cited_keys"), row.get("defined_keys")) for row in tex_summary.get("citation_closure", [])]
    add(errors, observed_citation != expected_citation or any(any(row.get(key) != 0 for key in ("missing_keys", "unused_keys", "duplicate_keys")) for row in tex_summary.get("citation_closure", [])), "TOP_CITATION_CLOSURE")
    citation = top.get("citation_genealogy", {})
    expected_citation_counts = {
        "root_routes": 4,
        "citation_routes": 88,
        "citation_commands": 210,
        "citation_source_lines": 199,
        "citation_occurrences": 258,
        "bibliography_definitions": 88,
        "closed_routes": 88,
        "pdf_page_mapped_routes": 0,
        "pdf_page_ground_not_found_routes": 88,
    }
    add(errors, citation.get("counts") != expected_citation_counts, "TOP_CITATION_GENEALOGY_COUNTS")
    root_routes = citation.get("root_routes", [])
    root_projection = [
        (
            row.get("root_tex_path"), len(row.get("reachable_tex_paths", [])),
            row.get("citation_key_count"), row.get("bibliography_key_count"),
            row.get("missing_keys"), row.get("unused_keys"), row.get("duplicate_keys"),
        )
        for row in root_routes
    ]
    expected_root_projection = [
        ("Claude/docs/v1.0.22/appendix_phase_separation.tex", 1, 0, 0, 0, 0, 0),
        ("Claude/docs/v1.0.22/ch1_graphite_v1.0.22.tex", 32, 39, 39, 0, 0, 0),
        ("Claude/docs/v1.0.22/ch2_lco_v1.0.22.tex", 12, 15, 15, 0, 0, 0),
        ("Claude/docs/v1.0.22/ch3_si_v1.0.22.tex", 10, 34, 34, 0, 0, 0),
    ]
    add(errors, root_projection != expected_root_projection, "TOP_CITATION_ROOT_ROUTES")
    citation_routes = citation.get("citation_routes", [])
    add(errors, [row.get("route_id") for row in citation_routes] != [f"P063-CITE-{number:03d}" for number in range(1, 89)], "TOP_CITATION_ROUTE_IDS")
    citation_anchor_invalid = False
    for row in citation_routes:
        if (
            row.get("closure_state") != "CLOSED"
            or len(row.get("bibliography_definitions", [])) != 1
            or not row.get("citation_occurrences")
            or row.get("pdf_page") is not None
            or row.get("pdf_page_mapping_state") != "GROUND_NOT_FOUND_NO_SYNCTEX_OR_TAGGED_SOURCE_MAP"
            or row.get("pdf_page_mapping_owner") != "Phase 063 Step 62 clean build/page genealogy"
        ):
            citation_anchor_invalid = True
        for anchor in [*row.get("citation_occurrences", []), *row.get("bibliography_definitions", [])]:
            source = source_by_id.get(anchor.get("source_id"))
            line = anchor.get("line")
            route = anchor.get("root_to_source_path", anchor.get("root_to_bibliography_path"))
            if (
                source is None
                or source.get("path") != anchor.get("source_path")
                or source.get("blob_sha1") != anchor.get("blob_sha1")
                or not isinstance(line, int)
                or line < 1
                or line > source.get("extent", {}).get("lines", 0)
                or not isinstance(route, list)
                or not route
                or route[0] != row.get("root_tex_path")
                or route[-1] != anchor.get("source_path")
            ):
                citation_anchor_invalid = True
    add(errors, citation_anchor_invalid, "TOP_CITATION_GENEALOGY_ANCHOR")
    add(errors, any(
        row.get("page_binding", {}).get("source_to_page_state") != "GROUND_NOT_FOUND"
        or row.get("page_binding", {}).get("citation_to_page_state") != "GROUND_NOT_FOUND"
        or row.get("page_binding", {}).get("bibitem_to_page_state") != "GROUND_NOT_FOUND"
        or row.get("page_binding", {}).get("downstream_owner") != "Phase 063 Step 62 Task 62B clean build/page genealogy"
        for row in root_routes
    ), "TOP_CITATION_PAGE_GNF_BOUNDARY")
    supplemental = top.get("supplemental_process_control", {})
    add(errors, supplemental.get("manifest_member") is not False or supplemental.get("blob_sha1") != "f50deee51df77dca8d07a2d9b9fd150fa93309cc", "TOP_SUPPLEMENTAL_IDENTITY")
    add(errors, [supplemental.get("bytes"), supplemental.get("physical_lines"), supplemental.get("nonblank_lines")] != [16_115, 99, 79], "TOP_SUPPLEMENTAL_EXTENT")
    observations = top.get("phase057_observation_inputs", [])
    add(errors, len(observations) != 11 or sum(row.get("physical_lines", 0) for row in observations) != 2_363, "TOP_OBSERVATION_INPUTS")
    routes = top.get("phase057_finding_routes", [])
    add(errors, [row.get("finding_id") for row in routes] != [f"INTENT-PROV-{number:04d}" for number in range(96, 192)], "TOP_FINDING_SEQUENCE")
    add(errors, any(not row.get("observation_source_id") or row.get("status_promoted") is not False or row.get("external_truth_promoted") is not False for row in routes), "TOP_FINDING_ROUTING")
    human_findings = top.get("human_read_findings", {})
    expected_finding_ids = {
        "process": [f"P063-PROC-{number:03d}" for number in range(1, 8)],
        "release": [f"P063-REL-{number:03d}" for number in range(1, 11)],
        "competing": [f"P063-COMP-{number:03d}" for number in range(1, 22)],
    }
    source_ids = set(ids) | {"P063-SUP-0001"}
    finding_source_by_id = dict(source_by_id)
    finding_source_by_id["P063-SUP-0001"] = supplemental
    for family, expected_ids in expected_finding_ids.items():
        finding_rows = human_findings.get(family, [])
        add(errors, [row.get("finding_id") for row in finding_rows] != expected_ids, "TOP_HUMAN_FINDING_IDS")
        add(errors, any(not row.get("source_ids") or not set(row.get("source_ids", [])).issubset(source_ids) for row in finding_rows), "TOP_HUMAN_FINDING_SOURCES")
        add(errors, any(row.get("status_promoted") is not False or row.get("external_truth_promoted") is not False or not row.get("downstream_owner") for row in finding_rows), "TOP_HUMAN_FINDING_AUTHORITY")
        evidence_invalid = False
        for row in finding_rows:
            evidence = row.get("evidence")
            if not isinstance(evidence, list) or not evidence or row.get("source_ids") != [item.get("source_id") for item in evidence]:
                evidence_invalid = True
                continue
            for item in evidence:
                source = finding_source_by_id.get(item.get("source_id"))
                if source is None or source.get("path") != item.get("path") or source.get("blob_sha1") != item.get("blob_sha1"):
                    evidence_invalid = True
                    continue
                max_line = source.get("extent", {}).get("lines", source.get("physical_lines", 0))
                intervals = item.get("line_intervals")
                if not isinstance(intervals, list):
                    evidence_invalid = True
                    continue
                for interval in intervals:
                    if (
                        not isinstance(interval, list) or len(interval) != 2
                        or not all(isinstance(number, int) for number in interval)
                        or interval[0] < 1 or interval[1] < interval[0] or interval[1] > max_line
                    ):
                        evidence_invalid = True
        add(errors, evidence_invalid, "TOP_HUMAN_FINDING_EVIDENCE")
    release_by_id = {
        row.get("finding_id"): row
        for row in human_findings.get("release", [])
        if isinstance(row, dict)
    }
    time_unit_finding = release_by_id.get("P063-REL-005", {})
    expected_time_unit_evidence = [
        {
            "path": "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py",
            "source_id": "P063-SRC-0001",
            "blob_sha1": "c822c4e7ef9b8676e3a9bde675a718169ce79d5b",
            "line_intervals": [[601, 617]],
        },
        {
            "path": "Claude/docs/v1.0.22/_sections/ch1_sec10_sum.tex",
            "source_id": "P063-SRC-0018",
            "blob_sha1": "10ab70e2e4a99cc72b122c75922bc178041b1923",
            "line_intervals": [[55, 55]],
        },
    ]
    time_unit_source_line = git_bytes(
        "show",
        f"{BASELINE}:Claude/docs/v1.0.22/_sections/ch1_sec10_sum.tex",
    ).decode("utf-8").splitlines()[54]
    add(
        errors,
        time_unit_finding.get("evidence") != expected_time_unit_evidence
        or time_unit_finding.get("source_ids") != ["P063-SRC-0001", "P063-SRC-0018"]
        or not all(token in time_unit_source_line for token in (r"\mathrm s^{-1}", "c-rate", "3600")),
        "TOP_HUMAN_FINDING_SEMANTIC_ANCHOR",
    )
    linkage = top.get("competing_phase057_linkage", {})
    add(errors, linkage.get("direct_origin_or_subject_correspondence") != [f"INTENT-PROV-{number:04d}" for number in range(111, 192)], "TOP_COMPETING_DIRECT_LINKS")
    add(errors, linkage.get("separate_corroboration_candidates") != [f"INTENT-PROV-{number:04d}" for number in range(99, 106)], "TOP_COMPETING_CORROBORATION_LINKS")
    add(errors, linkage.get("candidate_linked_count") != 88 or linkage.get("phase057_denominator") != 96 or linkage.get("status_promoted") is not False, "TOP_COMPETING_LINK_AUTHORITY")
    boundary = top.get("authority_boundary", {})
    false_keys = [
        "external_scientific_truth_promoted", "external_material_truth_promoted",
        "external_experimental_truth_promoted", "primary_literature_truth_promoted",
        "canonical_selection_promoted", "proposal_promoted_to_adoption",
    ]
    add(errors, boundary.get("source_process_identity_only") is not True, "TOP_AUTHORITY_INTERNAL")
    add(errors, any(boundary.get(key) is not False for key in false_keys), "TOP_AUTHORITY_PROMOTION")

    add(errors, att.get("schema_version") != 1, "ATT_SCHEMA")
    add(errors, att.get("artifact_kind") != "V1022_READ_ATTESTATION", "ATT_KIND")
    add(errors, att.get("phase") != 63 or att.get("step") != 58, "ATT_PHASE_STEP")
    expected_att_counts = {
        "manifest_records": 204, "text_records": 200, "text_physical_lines": 30_219,
        "text_nonblank_lines": 26_137, "pdf_records": 4, "pdf_pages": 133,
        "pdf_page_attestations": 133, "supplemental_records": 1,
        "observation_records": 11, "observation_physical_lines": 2_363,
    }
    for key, expected in expected_att_counts.items():
        add(errors, att.get("counts", {}).get(key) != expected, "ATT_COUNT_" + key.upper())
    records = att.get("manifest_read_records", [])
    add(errors, len(records) != 204, "ATT_READ_ROWS")
    add(errors, [row.get("source_id") for row in records] != ids, "ATT_SOURCE_ID_SEQUENCE")
    add(errors, any(row.get("read_status") != "READ_FULL" for row in records), "ATT_READ_STATUS")
    add(errors, any(row.get("review_mode") == "FULL_TEXT" and row.get("physical_interval") != [1, row.get("physical_lines")] for row in records), "ATT_TEXT_INTERVAL")
    add(errors, any(row.get("review_mode") == "FULL_PDF" and row.get("page_interval") != [1, row.get("pages")] for row in records), "ATT_PDF_INTERVAL")
    pages = att.get("pdf_page_attestations", [])
    page_keys = [(row.get("source_id"), row.get("page")) for row in pages]
    add(errors, len(pages) != 133 or len(page_keys) != len(set(page_keys)), "ATT_PAGE_ROWS")
    add(errors, any(row.get("render_status") != "PASS_POPPLER_RENDER" or row.get("human_visual_review") != "READ_FULL" for row in pages), "ATT_PAGE_STATUS")
    expected_page_keys = {
        (row["source_id"], page)
        for row in sources if row.get("review_mode") == "FULL_PDF"
        for page in range(1, row.get("extent", {}).get("pages", 0) + 1)
    }
    add(errors, set(page_keys) != expected_page_keys, "ATT_PAGE_ROWS")
    add(errors, any(not isinstance(row.get("extracted_nonblank_characters"), int) or row.get("extracted_nonblank_characters", 0) <= 0 for row in pages), "ATT_PAGE_TEXT_EXTRACTION")
    add(errors, any(row.get("unresolved_literal_question_mark_pairs") != 0 for row in pages), "ATT_PAGE_UNRESOLVED_MARKER")
    add(errors, att.get("supplemental_read_record") != supplemental, "ATT_SUPPLEMENTAL_LINK")
    add(errors, att.get("phase057_observation_read_records") != observations, "ATT_OBSERVATION_LINK")
    contract = att.get("human_review_contract", {})
    evidence, evidence_sha = human_review_evidence()
    evidence_input = contract.get("result_first_evidence_input", {})
    add(errors, evidence_input != {
        "path": EXACT_EIGHT[4],
        "evidence_id": evidence.get("evidence_id"),
        "semantic_sha256": evidence_sha,
        "evidence_kind": evidence.get("evidence_kind"),
        "evidence_date": evidence.get("evidence_date"),
    }, "ATT_HUMAN_EVIDENCE_INPUT")
    text_review_by_partition = {
        partition_name: review
        for review in evidence.get("text_reviews", [])
        for partition_name in review.get("partitions", [])
    }
    pdf_review_by_path = {row.get("path"): row for row in evidence.get("pdf_reviews", [])}
    add(errors, len(text_review_by_partition) != 4 or len(pdf_review_by_path) != 4, "ATT_HUMAN_EVIDENCE_SCHEMA")
    for record in records:
        source = source_by_id.get(record.get("source_id"))
        if source is None:
            continue
        if record.get("review_mode") == "FULL_TEXT":
            review = text_review_by_partition.get(source.get("partition"), {})
            add(errors, record.get("human_review_evidence_id") != review.get("review_id"), "ATT_HUMAN_EVIDENCE_BIJECTION")
        else:
            review = pdf_review_by_path.get(record.get("path"), {})
            add(errors, record.get("human_review_evidence_id") != review.get("review_id"), "ATT_HUMAN_EVIDENCE_BIJECTION")
    for page in pages:
        review = pdf_review_by_path.get(page.get("path"), {})
        expected_findings = [item for item in review.get("findings", []) if page.get("page") in item.get("pages", [])]
        add(errors, (
            page.get("human_review_evidence_id") != review.get("review_id")
            or page.get("visual_findings") != expected_findings
        ), "ATT_HUMAN_PDF_EVIDENCE")
    add(errors, att.get("supplemental_read_record", {}).get("human_review_evidence_id") != evidence.get("supplemental_review", {}).get("review_id"), "ATT_HUMAN_EVIDENCE_BIJECTION")
    add(errors, any(row.get("human_review_evidence_id") != evidence.get("observation_review", {}).get("review_id") for row in att.get("phase057_observation_read_records", [])), "ATT_HUMAN_EVIDENCE_BIJECTION")
    add(errors, contract.get("unread_manifest_intervals") != [], "ATT_UNREAD_MANIFEST")
    add(errors, contract.get("unread_pdf_pages") != [], "ATT_UNREAD_PDF")
    expected_read_summaries = {
        "FINAL_RELEASE_SURFACE": {"files": 63, "bytes": 2_985_072, "text_physical_lines": 10_462, "text_nonblank_lines": 9_733, "pdf_files": 4, "pdf_pages": 133, "read_status": "READ_FULL"},
        "COMPETING_REVIEW_CANDIDATE": {"files": 125, "bytes": 1_800_475, "text_physical_lines": 17_072, "text_nonblank_lines": 13_926, "read_status": "READ_FULL"},
        "VERSION_PLAN_AND_STATUS_MACHINE_PROCESS": {"files": 16, "bytes": 188_601, "text_physical_lines": 2_685, "text_nonblank_lines": 2_478, "read_status": "READ_FULL"},
        "SUPPLEMENTAL_PROCESS_CONTROL": {"files": 1, "bytes": 16_115, "text_physical_lines": 99, "text_nonblank_lines": 79, "read_status": "READ_FULL"},
    }
    add(errors, contract.get("partition_read_summary") != expected_read_summaries, "ATT_PARTITION_READ_SUMMARY")
    expected_visual_summary = {
        "rendered_pages": 133, "visually_read_pages": 133,
        "pages_without_extracted_text": 0, "unresolved_literal_question_mark_pairs": 0,
        "documents_untagged": 4, "clipping_findings": 0, "overlap_findings": 0,
        "missing_glyph_findings": 0, "broken_formula_findings": 0,
        "recorded_visual_findings": 8,
    }
    add(errors, contract.get("pdf_visual_summary") != expected_visual_summary, "ATT_PDF_VISUAL_SUMMARY")
    add(errors, contract.get("builder_reexecutes_human_visual_review") is not False, "ATT_HUMAN_EVIDENCE_AUTHORITY")
    add(errors, att.get("source_topology_semantic_sha256") != digest(canonical(top)), "ATT_TOPOLOGY_LINK")
    return errors


def independent_manifest_diagnostics(top: dict[str, Any], att: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    if digest(normalized_bytes(MANIFEST)) != MANIFEST_SHA256:
        return {"INDEPENDENT_MANIFEST_SHA"}
    manifest, _ = strict_load(MANIFEST)
    selected = [(index, row) for index, row in enumerate(manifest["entries"], start=1) if row.get("version") == "v1.0.22"]
    sources = top["sources"]
    expected = [(index, row["path"], row["blob_sha"], row["size_bytes"], row["review_mode"]) for index, row in selected]
    observed = [(row["manifest_index"], row["path"], row["blob_sha1"], row["extent"]["bytes"], row["review_mode"]) for row in sources]
    add(errors, observed != expected, "INDEPENDENT_MANIFEST_ROWS")
    tree_rows = git_text("ls-tree", "-r", "-l", BASELINE, "--", "Claude/docs/v1.0.22").splitlines()
    tree: dict[str, tuple[str, int]] = {}
    for line in tree_rows:
        left, path = line.split("\t", 1)
        _, kind, blob, size = left.split()
        if kind == "blob":
            tree[path] = (blob, int(size))
    add(errors, tree != {row["path"]: (row["blob_sha1"], row["extent"]["bytes"]) for row in sources}, "INDEPENDENT_FROZEN_TREE")
    history = git_text("log", "--reverse", "--format=%H", BASELINE, "--", "Claude/docs/v1.0.22").splitlines()
    add(errors, history != [row["commit"] for row in top["commit_genealogy"]], "INDEPENDENT_COMMIT_GENEALOGY")
    commit_rows_invalid = False
    for row in top["commit_genealogy"]:
        metadata = git_bytes("show", "-s", "--format=%H%x00%P%x00%an%x00%aI%x00%cI%x00%s", row["commit"])
        fields = metadata.rstrip(b"\n").decode("utf-8", errors="strict").split("\x00", 5)
        changes_raw = git_text(
            "diff-tree", "--root", "--no-commit-id", "--name-status", "-r", "-M", "-C",
            row["commit"], "--", "Claude/docs/v1.0.22",
        )
        changes = []
        for line in changes_raw.splitlines():
            cells = line.split("\t")
            if len(cells) in {2, 3}:
                changes.append({"status": cells[0], "paths": cells[1:]})
        if (
            len(fields) != 6
            or row.get("commit") != fields[0]
            or row.get("parents") != fields[1].split()
            or row.get("repository_actor") != fields[2]
            or row.get("author_time") != fields[3]
            or row.get("committer_time") != fields[4]
            or row.get("subject") != fields[5]
            or row.get("changed_paths") != changes
        ):
            commit_rows_invalid = True
    add(errors, commit_rows_invalid, "INDEPENDENT_COMMIT_ROWS")
    commit_by_id = {row["commit"]: row for row in top["commit_genealogy"]}
    source_history_invalid = False
    for source in top["sources"]:
        touches = []
        additions = []
        for commit in top["commit_genealogy"]:
            for change in commit["changed_paths"]:
                roles = ["path"] if len(change["paths"]) == 1 else ["old", "new"]
                for path, role in zip(change["paths"], roles):
                    if path == source["path"] and (not touches or touches[-1] != commit["commit"]):
                        touches.append(commit["commit"])
                    if path == source["path"] and role in {"path", "new"} and change["status"].startswith(("A", "R", "C")):
                        additions.append(commit["commit"])
        first_add = additions[0] if additions else (touches[0] if touches else None)
        last_touch = touches[-1] if touches else None
        if (
            source.get("touch_commits") != touches
            or source.get("touch_commit_count") != len(touches)
            or source.get("first_add_commit") != first_add
            or source.get("last_touch_commit") != last_touch
            or source.get("first_add_subject") != commit_by_id.get(first_add, {}).get("subject")
            or source.get("last_touch_subject") != commit_by_id.get(last_touch, {}).get("subject")
        ):
            source_history_invalid = True
    add(errors, source_history_invalid, "INDEPENDENT_SOURCE_HISTORY")
    add(errors, {row["source_id"] for row in att["manifest_read_records"]} != {row["source_id"] for row in sources}, "INDEPENDENT_READ_BIJECTION")
    return errors


def control_diagnostics() -> set[str]:
    errors: set[str] = set()
    documents = {"result": RESULT, "active_ledger": ACTIVE_LEDGER, "parent_ledger": PARENT_LEDGER, "handover": HANDOVER}
    texts = {name: path.read_text(encoding="utf-8") for name, path in documents.items()}
    for name, path in documents.items():
        add(errors, digest(normalized_bytes(path)) != CONTROL_SHA256[name], "CONTROL_SHA_" + name.upper())
    lines = texts["result"].splitlines()
    add(errors, [line for line in lines if line.startswith("Gate:")] != ["Gate: `PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY`"], "CONTROL_RESULT_GATE")
    add(errors, lines.count("Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`") != 1, "CONTROL_RESULT_COMMIT")
    add(errors, lines.count("Postcommit persistence: `PENDING`") != 1, "CONTROL_RESULT_PERSISTENCE")
    for name in ("active_ledger", "parent_ledger", "handover"):
        text = texts[name]
        add(errors, "Phase 063" not in text or "Step 58" not in text or "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY" not in text or "PENDING_AT_PRECOMMIT_BY_DESIGN" not in text, "CONTROL_TOKEN_" + name.upper())
    add(errors, any(ACTIVATION not in texts[name] for name in ("active_ledger", "parent_ledger", "handover")), "CONTROL_ACTIVATION_PERSISTENCE")
    return errors


def builder_policy_diagnostics() -> set[str]:
    errors: set[str] = set()
    source = BUILDER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    allowed_roots = {"__future__", "argparse", "hashlib", "json", "math", "posixpath", "re", "subprocess", "collections", "io", "pathlib", "typing", "pypdf"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".", 1)[0] not in allowed_roots for alias in node.names):
                errors.add("BUILDER_FORBIDDEN_IMPORT")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".", 1)[0] not in allowed_roots:
                errors.add("BUILDER_FORBIDDEN_IMPORT")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr != "run":
                errors.add("BUILDER_FORBIDDEN_SUBPROCESS_API")
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr == "run":
                command = node.args[0] if node.args else None
                if not (isinstance(command, ast.List) and command.elts and isinstance(command.elts[0], ast.Constant) and command.elts[0].value == "git"):
                    errors.add("BUILDER_NON_GIT_SUBPROCESS")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
            errors.add("BUILDER_DYNAMIC_EXECUTION")
    add(errors, "Claude.docs" in source or "import Claude" in source, "BUILDER_PRODUCTION_IMPORT")
    return errors


def negative_controls(top: dict[str, Any], att: dict[str, Any]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []

    def record(name: str, actual: list[str], expected: list[str]) -> None:
        controls.append({"name": name, "diagnostics": actual, "expected": expected, "rejected": actual == expected})

    strict_fixtures = (
        ("duplicate_key", '{"a":1,"a":2}', "STRICT_DUPLICATE_KEY", "duplicate JSON key"),
        ("nan", '{"a":NaN}', "STRICT_NONFINITE_CONSTANT", "non-finite JSON constant"),
        ("infinity", '{"a":Infinity}', "STRICT_NONFINITE_CONSTANT", "non-finite JSON constant"),
        ("positive_overflow", '{"a":1e9999}', "STRICT_NONFINITE_NUMBER", "non-finite JSON number"),
        ("negative_overflow", '{"a":-1e9999}', "STRICT_NONFINITE_NUMBER", "non-finite JSON number"),
        ("truncated", '{"a":', "STRICT_TRUNCATED_JSON", "Expecting value"),
    )
    for name, raw, code, fragment in strict_fixtures:
        actual: list[str] = []
        try:
            value = json.loads(raw, object_pairs_hook=strict_pairs, parse_constant=reject_constant, parse_float=strict_float)
            traverse(value)
        except (ValueError, json.JSONDecodeError) as exc:
            actual = [code] if fragment in str(exc) else ["UNEXPECTED:" + str(exc)]
        record(name, actual, [code])

    fixtures: list[tuple[str, str, tuple[Any, ...], Any, list[str]]] = [
        ("source_count", "top", ("counts", "source_occurrences"), 203, ["TOP_COUNT_SOURCE_OCCURRENCES"]),
        ("manifest_bytes", "top", ("counts", "bytes"), 4_974_147, ["TOP_COUNT_BYTES"]),
        ("partition_counts", "top", ("counts", "partition_counts"), {}, ["TOP_COUNT_PARTITION_COUNTS"]),
        ("history_count", "top", ("counts", "history_commits"), 99, ["TOP_COUNT_HISTORY_COMMITS"]),
        ("supplemental_fusion", "top", ("denominator_policy", "supplemental_process_control_occurrences"), 0, ["TOP_DENOMINATOR_SUPPLEMENTAL"]),
        ("manifest_fusion", "top", ("denominator_policy", "denominator_fusion_forbidden"), False, ["TOP_DENOMINATOR_FUSION"]),
        ("cross_same", "top", ("cross_version_v1021_v1022", "same_relative_count"), 41, ["TOP_CROSS_SAME_RELATIVE"]),
        ("cross_shared", "top", ("cross_version_v1021_v1022", "shared_blob_count"), 4, ["TOP_CROSS_SHARED_BLOBS"]),
        ("source_authority", "top", ("sources", 0, "authority_ceiling"), "EXTERNAL", ["TOP_SOURCE_AUTHORITY"]),
        ("finding_promotion", "top", ("phase057_finding_routes", 0, "external_truth_promoted"), True, ["TOP_FINDING_ROUTING"]),
        ("external_science", "top", ("authority_boundary", "external_scientific_truth_promoted"), True, ["TOP_AUTHORITY_PROMOTION"]),
        ("proposal_adoption", "top", ("authority_boundary", "proposal_promoted_to_adoption"), True, ["TOP_AUTHORITY_PROMOTION"]),
        ("competing_count", "top", ("counts", "competing_authority_subtypes"), {}, ["TOP_COUNT_COMPETING_AUTHORITY_SUBTYPES"]),
        ("competing_adoption", "top", ("sources", 76, "final_adoption_authority"), True, ["TOP_COMPETING_ADOPTION_AUTHORITY"]),
        ("tex_orphans", "top", ("tex_structure_summary", "manifest_orphan_tex_paths"), [], ["TOP_TEX_ORPHANS"]),
        ("human_finding_promotion", "top", ("human_read_findings", "competing", 0, "status_promoted"), True, ["TOP_HUMAN_FINDING_AUTHORITY"]),
        ("competing_link_promotion", "top", ("competing_phase057_linkage", "status_promoted"), True, ["TOP_COMPETING_LINK_AUTHORITY"]),
        ("att_text_count", "att", ("counts", "text_records"), 199, ["ATT_COUNT_TEXT_RECORDS"]),
        ("att_pdf_pages", "att", ("counts", "pdf_pages"), 132, ["ATT_COUNT_PDF_PAGES"]),
        ("att_read_status", "att", ("manifest_read_records", 0, "read_status"), "PARTIAL", ["ATT_READ_STATUS"]),
        ("att_unread_manifest", "att", ("human_review_contract", "unread_manifest_intervals"), [[1, 1]], ["ATT_UNREAD_MANIFEST"]),
        ("att_unread_pdf", "att", ("human_review_contract", "unread_pdf_pages"), [1], ["ATT_UNREAD_PDF"]),
        ("att_page_status", "att", ("pdf_page_attestations", 0, "human_visual_review"), "UNREAD", ["ATT_PAGE_STATUS"]),
    ]
    for name, target_name, route, value, expected in fixtures:
        altered_top = copy.deepcopy(top)
        altered_att = copy.deepcopy(att)
        target: Any = altered_top if target_name == "top" else altered_att
        for key in route[:-1]:
            target = target[key]
        target[route[-1]] = value
        if target_name == "top":
            altered_att["source_topology_semantic_sha256"] = digest(canonical(altered_top))
        record(name, sorted(artifact_diagnostics(altered_top, altered_att)), expected)

    def refresh_source_history_projection(value: dict[str, Any]) -> None:
        projection = [
            {
                "source_id": row.get("source_id"),
                "path": row.get("path"),
                "blob_sha1": row.get("blob_sha1"),
                "first_add_commit": row.get("first_add_commit"),
                "first_add_subject": row.get("first_add_subject"),
                "last_touch_commit": row.get("last_touch_commit"),
                "last_touch_subject": row.get("last_touch_subject"),
                "touch_commit_count": row.get("touch_commit_count"),
                "touch_commits": row.get("touch_commits"),
            }
            for row in value["sources"]
        ]
        value["history_summary"]["source_history_row_projection_sha256"] = digest(compact(projection))

    def mutated(name: str, mutate: Any, expected: list[str]) -> None:
        altered_top = copy.deepcopy(top)
        altered_att = copy.deepcopy(att)
        mutate(altered_top, altered_att)
        altered_att["source_topology_semantic_sha256"] = digest(canonical(altered_top))
        record(name, sorted(artifact_diagnostics(altered_top, altered_att)), expected)

    def duplicate_source_id(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["sources"][202]["source_id"] = value["sources"][201]["source_id"]
        evidence["manifest_read_records"][202]["source_id"] = evidence["manifest_read_records"][201]["source_id"]
        refresh_source_history_projection(value)

    def duplicate_source_path(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["sources"][202]["path"] = value["sources"][201]["path"]
        refresh_source_history_projection(value)

    def duplicate_source_blob(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["sources"][202]["blob_sha1"] = value["sources"][201]["blob_sha1"]
        refresh_source_history_projection(value)

    def lost_pdf_page(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        evidence["pdf_page_attestations"].pop()

    def commit_parent(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["commit_genealogy"][0]["parents"] = ["0" * 40]

    def commit_subject(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["commit_genealogy"][0]["subject"] += " tamper"

    def commit_changed_path(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["commit_genealogy"][0]["changed_paths"][0]["paths"][0] += ".tamper"

    def commit_actor(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["commit_genealogy"][0]["repository_actor"] = "tamper"

    def source_first_add(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["sources"][0]["first_add_commit"] = value["sources"][0]["touch_commits"][-1]

    def source_first_add_subject(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["sources"][0]["first_add_subject"] += " tamper"

    def finding_line_anchor(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["human_read_findings"]["process"][0]["evidence"][0]["line_intervals"][0][1] = 10_000

    def finding_semantic_anchor_swap(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        wrong_source = next(
            row
            for row in value["sources"]
            if row["path"] == "Claude/docs/v1.0.22/_sections/ch2_sec07_revheat.tex"
        )
        finding = value["human_read_findings"]["release"][4]
        finding["evidence"][1] = {
            "path": wrong_source["path"],
            "source_id": wrong_source["source_id"],
            "blob_sha1": wrong_source["blob_sha1"],
            "line_intervals": [[55, 55]],
        }
        finding["source_ids"][1] = wrong_source["source_id"]

    def citation_line_anchor(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["citation_genealogy"]["citation_routes"][0]["citation_occurrences"][0]["line"] = 10_000

    def citation_page_fabrication(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["citation_genealogy"]["citation_routes"][0]["pdf_page"] = 1

    def cross_relation_tamper(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["cross_version_v1021_v1022"]["explicit_relation_rows"][2]["relation"] = "ADOPTED"

    def cross_sidecar_fabrication(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        value["cross_version_v1021_v1022"]["frozen_page_mapping_sidecars"] = ["fake.synctex"]

    def page_text_loss(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        evidence["pdf_page_attestations"][0]["extracted_nonblank_characters"] = 0

    def human_evidence_digest(value: dict[str, Any], evidence: dict[str, Any]) -> None:
        evidence["human_review_contract"]["result_first_evidence_input"]["semantic_sha256"] = "0" * 64

    for name, mutate, expected in (
        ("duplicate_source_id", duplicate_source_id, ["TOP_SOURCE_ID_SEQUENCE"]),
        ("duplicate_source_path", duplicate_source_path, ["TOP_SOURCE_PATH_UNIQUE"]),
        ("duplicate_source_blob", duplicate_source_blob, ["TOP_SOURCE_BLOB_UNIQUE"]),
        ("lost_pdf_page_row", lost_pdf_page, ["ATT_PAGE_ROWS"]),
        ("commit_parent_tamper", commit_parent, ["TOP_HISTORY_PROJECTION_SHA"]),
        ("commit_subject_tamper", commit_subject, ["TOP_HISTORY_PROJECTION_SHA"]),
        ("commit_changed_path_tamper", commit_changed_path, ["TOP_HISTORY_PROJECTION_SHA"]),
        ("commit_actor_tamper", commit_actor, ["TOP_HISTORY_ACTOR_PROJECTION_SHA"]),
        ("source_first_add_tamper", source_first_add, ["TOP_SOURCE_HISTORY_ROW_PROJECTION_SHA"]),
        ("source_first_add_subject_tamper", source_first_add_subject, ["TOP_SOURCE_HISTORY_ROW_PROJECTION_SHA"]),
        ("finding_line_anchor", finding_line_anchor, ["TOP_HUMAN_FINDING_EVIDENCE"]),
        ("finding_semantic_anchor_swap", finding_semantic_anchor_swap, ["TOP_HUMAN_FINDING_SEMANTIC_ANCHOR"]),
        ("citation_line_anchor", citation_line_anchor, ["TOP_CITATION_GENEALOGY_ANCHOR"]),
        ("citation_page_fabrication", citation_page_fabrication, ["TOP_CITATION_GENEALOGY_ANCHOR"]),
        ("cross_relation_tamper", cross_relation_tamper, ["TOP_CROSS_RELATIONS"]),
        ("cross_sidecar_fabrication", cross_sidecar_fabrication, ["TOP_CROSS_PAGE_SIDECARS"]),
        ("page_text_loss", page_text_loss, ["ATT_PAGE_TEXT_EXTRACTION"]),
        ("human_evidence_digest", human_evidence_digest, ["ATT_HUMAN_EVIDENCE_INPUT"]),
    ):
        mutated(name, mutate, expected)
    return controls


def changed_paths() -> set[str]:
    return git_paths("diff", "HEAD", "--name-only", "-z") | git_paths("ls-files", "--others", "--exclude-standard", "-z")


def repository_diagnostics(mode: str, expected_commit: str | None = None) -> set[str]:
    errors: set[str] = set()
    head = git_text("rev-parse", "HEAD")
    add(errors, git_text("branch", "--show-current") != BRANCH, "GIT_BRANCH")
    add(errors, git_text("rev-parse", "--symbolic-full-name", "@{upstream}") != f"refs/remotes/origin/{BRANCH}", "GIT_UPSTREAM_REF")
    add(errors, ref_hash(f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP, "GIT_PROTECTED_LOCAL")
    add(errors, ref_hash(f"refs/remotes/origin/{PROTECTED_BRANCH}") != PROTECTED_TIP, "GIT_PROTECTED_TRACKING")
    add(errors, remote_head(PROTECTED_BRANCH) != PROTECTED_TIP, "GIT_PROTECTED_LIVE")
    add(errors, ref_hash("refs/heads/main") is not None, "GIT_MAIN_LOCAL")
    add(errors, ref_hash("refs/remotes/origin/main") != MAIN_TIP, "GIT_MAIN_TRACKING")
    add(errors, remote_head("main") != MAIN_TIP, "GIT_MAIN_LIVE")
    if mode in {"content", "staged"}:
        add(errors, head != ACTIVATION, "GIT_PRECOMMIT_HEAD")
        add(errors, git_text("rev-parse", "@{upstream}") != ACTIVATION, "GIT_PRECOMMIT_UPSTREAM")
        add(errors, remote_head(BRANCH) != ACTIVATION, "GIT_PRECOMMIT_LIVE")
        add(errors, changed_paths() != EXACT_EIGHT_SET, "GIT_CHANGED_EXACT_EIGHT")
        add(errors, git_text("diff", "--name-only", ACTIVATION, "--", "Claude") != "", "GIT_CLAUDE_TRACKED")
        add(errors, git_text("ls-files", "--others", "--exclude-standard", "--", "Claude") != "", "GIT_CLAUDE_UNTRACKED")
    if mode == "staged":
        add(errors, git_paths("diff", "--cached", "--name-only", "-z") != EXACT_EIGHT_SET, "GIT_STAGED_EXACT_EIGHT")
        add(errors, git_text("diff", "--name-only") != "", "GIT_NO_UNSTAGED_TRACKED")
        for rel in EXACT_EIGHT:
            index = git_bytes("show", f":{rel}")
            if index.replace(b"\r\n", b"\n").replace(b"\r", b"\n") != normalized_bytes(REPO / rel):
                errors.add("GIT_INDEX_WORKTREE_BYTES")
                break
        add(errors, run(["git", "diff", "--check", "--cached"]).returncode != 0, "GIT_DIFF_CHECK")
    if mode == "persistence":
        if expected_commit is None:
            return errors | {"GIT_EXPECTED_COMMIT_REQUIRED"}
        add(errors, head != expected_commit, "GIT_PERSIST_HEAD")
        add(errors, git_text("rev-parse", "@{upstream}") != expected_commit, "GIT_PERSIST_UPSTREAM")
        add(errors, remote_head(BRANCH) != expected_commit, "GIT_PERSIST_LIVE")
        add(errors, git_text("rev-parse", f"{expected_commit}^") != ACTIVATION, "GIT_PERSIST_PARENT")
        add(errors, git_text("show", "-s", "--format=%s", expected_commit) != SUBJECT, "GIT_PERSIST_SUBJECT")
        add(errors, git_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", expected_commit) != EXACT_EIGHT_SET, "GIT_PERSIST_EXACT_EIGHT")
        add(errors, bool(changed_paths()), "GIT_PERSIST_CLEAN")
        add(errors, git_text("diff", "--name-only", ACTIVATION, expected_commit, "--", "Claude") != "", "GIT_CLAUDE_TRACKED")
        for rel in EXACT_EIGHT:
            committed = git_bytes("show", f"{expected_commit}:{rel}")
            if committed.replace(b"\r\n", b"\n").replace(b"\r", b"\n") != normalized_bytes(REPO / rel):
                errors.add("GIT_PERSIST_BLOB_BYTES")
                break
    return errors


def require(errors: set[str], terminal: str) -> None:
    if errors:
        print("FAIL " + " ".join(sorted(errors)))
        print(f"FAIL_{terminal}")
        raise SystemExit(1)


def validate_content(repository_mode: str, expected_commit: str | None = None) -> tuple[dict[str, Any], dict[str, Any], int]:
    missing = [path for path in (TOPOLOGY, ATTESTATION) if not path.is_file()]
    if missing:
        print("FAIL E_STEP58_ARTIFACT_MISSING " + " ".join(path.relative_to(REPO).as_posix() for path in missing))
        print("FAIL_P063_STEP58_CONTENT 0/1")
        raise SystemExit(1)
    top, top_nodes = strict_load(TOPOLOGY)
    att, att_nodes = strict_load(ATTESTATION)
    rebuilt_top, rebuilt_att, top_bytes, att_bytes, _, _ = run_builder()
    errors = artifact_diagnostics(top, att) | independent_manifest_diagnostics(top, att)
    errors |= control_diagnostics() | builder_policy_diagnostics() | repository_diagnostics(repository_mode, expected_commit)
    add(errors, TOPOLOGY.read_bytes() != top_bytes, "STORED_TOPOLOGY_REBUILD")
    add(errors, ATTESTATION.read_bytes() != att_bytes, "STORED_ATTESTATION_REBUILD")
    add(errors, canonical(top) != canonical(rebuilt_top), "STORED_TOPOLOGY_SEMANTIC")
    add(errors, canonical(att) != canonical(rebuilt_att), "STORED_ATTESTATION_SEMANTIC")
    require(errors, "P063_STEP58_CONTENT")
    return top, att, top_nodes + att_nodes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    modes = sum(bool(value) for value in (args.content_only, args.verify_staged, args.verify_persistence))
    if modes != 1:
        raise SystemExit("select exactly one primary mode")
    if args.verify_persistence:
        if not args.expected_commit or len(args.expected_commit) != 40:
            raise SystemExit("--expected-commit requires full 40-character SHA")
        top, att, nodes = validate_content("persistence", args.expected_commit)
    elif args.verify_staged:
        top, att, nodes = validate_content("staged")
    else:
        top, att, nodes = validate_content("content")
    if args.run_negative_probes:
        controls = negative_controls(top, att)
        require({"NEGATIVE_" + row["name"] for row in controls if not row["rejected"]}, "P063_STEP58_NEGATIVE_CONTROLS")
        print(f"PASS_P063_STEP58_NEGATIVE_CONTROLS {len(controls)}/{len(controls)}")
    if args.determinism_check:
        _, _, top_a, att_a, _, _ = run_builder()
        _, _, top_b, att_b, _, _ = run_builder()
        require({"DETERMINISM"} if (top_a, att_a) != (top_b, att_b) else set(), "P063_STEP58_DETERMINISM")
        print("PASS_P063_STEP58_DETERMINISM 2/2")
    if args.verify_staged:
        print("PASS_P063_STEP58_STAGED 8/8")
    elif args.verify_persistence:
        print(f"PASS_P063_STEP58_PERSISTENCE head={args.expected_commit}")
    else:
        print(f"PASS_P063_STEP58_CONTENT nodes={nodes}")


if __name__ == "__main__":
    try:
        main()
    except (ValidationError, UnicodeDecodeError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"FAIL {type(exc).__name__}: {exc}")
        raise SystemExit(1)
