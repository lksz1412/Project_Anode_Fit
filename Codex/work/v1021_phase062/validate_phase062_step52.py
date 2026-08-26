#!/usr/bin/env python3
"""Fail-closed validator for Phase 062 Step 52.

The validator never imports the builder or frozen Claude production code.  It
reconstructs the two machine artifacts in a disposable directory, independently
checks frozen Git identities and semantic contracts, and then applies repository
boundary checks appropriate to content, staged, or persistence mode.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
VALIDATOR = Path(__file__).resolve()
BUILDER = REPO / "Codex/work/v1021_phase062/build_phase062_step52_source_process_topology.py"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
TOPOLOGY = REPO / "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION = REPO / "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json"
RESULT = REPO / "Codex/results/PHASE_062_STEP_052_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
ACTIVATION = "76dccbaee0efdd16a4d22c25527a1a8ab3108559"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase062): freeze v1021 source process topology"
PROTECTED_REF = "refs/heads/codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_REF = "refs/remotes/origin/main"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BUILDER_SHA256 = "bfcccd8551cb69c4f1c4519e83ac31297122b7b630d9346a7fdb854185b1b598"
MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
SUPPLEMENTAL_PATH = "Claude/plans/2026-07-16-v1021-master-plan.md"
SUPPLEMENTAL_BLOB = "de26c03b53bedbe1cc4363bb07f66e9ca9da77f7"
Q1_PATH = "Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md"
Q1_BLOB = "3c5a20f8609b4a2cd1f9ce85d61c302b59180c50"
TIMEOUT = 240

EXACT_EIGHT = (
    "Codex/work/v1021_phase062/build_phase062_step52_source_process_topology.py",
    "Codex/work/v1021_phase062/validate_phase062_step52.py",
    "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json",
    "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json",
    "Codex/results/PHASE_062_STEP_052_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)

EXPECTED_COUNTS = {
    "release_occurrences": 68,
    "release_unique_paths": 68,
    "release_unique_blobs": 68,
    "release_bytes": 4_071_795,
    "release_text_files": 63,
    "release_text_physical_lines": 21_048,
    "release_text_nonblank_lines": 20_424,
    "release_pdf_files": 5,
    "release_pdf_pages": 214,
    "release_snapshot_files": 9,
    "shared_v1020_blob_identities": 23,
    "same_relative_pairs": 43,
    "same_relative_identical": 23,
    "same_relative_changed": 20,
    "same_relative_no_counterpart": 25,
    "supplemental_occurrences": 1,
    "q1_comparison_occurrences": 1,
    "implementation_chain_commits": 10,
    "supporting_history_commits": 3,
    "process_artifact_rows": 53,
    "ground_not_found_rows": 37,
    "phase057_navigation_inputs": 7,
    "phase057_navigation_lines": 819,
    "phase057_observation_rows": 30,
}
EXPECTED_ATTESTATION = {
    "release_text_files": 63,
    "release_text_physical_lines": 21_048,
    "release_text_nonblank_lines": 20_424,
    "release_pdf_files": 5,
    "release_pdf_pages": 214,
    "snapshot_files": 9,
    "snapshot_nodes": 10_425,
    "snapshot_mapping_keys": 6_847,
    "snapshot_traversal_items": 17_272,
    "supplemental_files": 1,
    "supplemental_physical_lines": 76,
    "q1_comparison_files": 1,
    "q1_comparison_physical_lines": 291,
    "human_partitions_complete": 4,
    "human_partitions_total": 4,
}
PROCESS_PHASES = ("Q0", "Q1", "Q2", "Q3", "Q4", "Q5NAV", "Q5", "Q5B", "Q6", "Q7", "Q8", "Q9", "Q10")
SNAPSHOT_PHASES = ("Q0", "Q2", "Q3", "Q4", "Q5NAV", "Q5", "Q5B", "Q6", "Q7")
GNF_SNAPSHOT_PHASES = ("Q1", "Q8", "Q9", "Q10")
PROCESS_DOCUMENT_CONTRACT = {
    "CHANGE_LOG": ("b4e939b0547cd4bf73bca30abe10fd164954c277", "9ea5cb23754061261923bab013e279d7f6938723", "CONTEMPORANEOUS", "PROCESS_EVIDENCE"),
    "EXECUTION_LEDGER": ("b4e939b0547cd4bf73bca30abe10fd164954c277", "5d815235de4e302ff5d7a076d525921ab417eadf", "DOWNSTREAM_AUTHORED", "INTERNAL_SUBSTITUTE_CLOSURE"),
    "REFERENCE_LEDGER": ("b4e939b0547cd4bf73bca30abe10fd164954c277", "9ea5cb23754061261923bab013e279d7f6938723", "CONTEMPORANEOUS", "PROCESS_EVIDENCE"),
    "HANDOVER": ("5d815235de4e302ff5d7a076d525921ab417eadf", "5d815235de4e302ff5d7a076d525921ab417eadf", "DOWNSTREAM_AUTHORED", "INTERNAL_SUBSTITUTE_CLOSURE"),
}
IMPLEMENTATION_HISTORY = (
    ("Q0", "b4e939b0547cd4bf73bca30abe10fd164954c277"),
    ("Q2", "1635bc97fb7bd9c3fabc720e91bf09e5ba31798f"),
    ("Q3", "c7420915dfae8ef076319737bddcc532a86d9505"),
    ("Q4", "46360bd0630ee6039d595b6980ad28862b362eb7"),
    ("Q5NAV", "287d38d36415103cc28822f33c2520f734f1d6a9"),
    ("Q5", "9d208db8cec382b5d7d0dc79b4fc6a2e88cdb444"),
    ("Q5B", "7316e7915db8727f794614b61f98d4df7f803bfd"),
    ("Q6", "bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17"),
    ("Q7", "9ea5cb23754061261923bab013e279d7f6938723"),
    ("Q8", "e96147fe4d5cefcccf733702e9bee78ba0beb025"),
)
SUPPORT_HISTORY = (
    ("MASTER_PLAN_V1", "66e3510d67162dd6bd88158557f96621cbedbbcf", "PRECURSOR_PLAN"),
    ("Q1_PARTIAL_REPORT_ORIGIN", "1e6c610f11682d87a416957b1cf65b4c8df53697", "PRE_Q0_PARTIAL_REPORT"),
    ("DOWNSTREAM_Q9_Q10_CLOSURE", "5d815235de4e302ff5d7a076d525921ab417eadf", "DOWNSTREAM_AUTHORED"),
)
SNAPSHOT_CONTRACT = {
    "Q0": ("Claude/docs/v1.0.21/results/snapshot_v1021_q0.json", IMPLEMENTATION_HISTORY[0][1]),
    "Q2": ("Claude/docs/v1.0.21/results/snapshot_v1021_q2.json", IMPLEMENTATION_HISTORY[1][1]),
    "Q3": ("Claude/docs/v1.0.21/results/snapshot_v1021_q3.json", IMPLEMENTATION_HISTORY[2][1]),
    "Q4": ("Claude/docs/v1.0.21/results/snapshot_v1021_q4.json", IMPLEMENTATION_HISTORY[3][1]),
    "Q5NAV": ("Claude/docs/v1.0.21/results/snapshot_v1021_q5nav.json", IMPLEMENTATION_HISTORY[4][1]),
    "Q5": ("Claude/docs/v1.0.21/results/snapshot_v1021_q5.json", IMPLEMENTATION_HISTORY[5][1]),
    "Q5B": ("Claude/docs/v1.0.21/results/snapshot_v1021_q5b.json", IMPLEMENTATION_HISTORY[6][1]),
    "Q6": ("Claude/docs/v1.0.21/results/snapshot_v1021_q6.json", IMPLEMENTATION_HISTORY[7][1]),
    "Q7": ("Claude/docs/v1.0.21/results/snapshot_v1021_q7.json", IMPLEMENTATION_HISTORY[8][1]),
}
PHASE057_OBSERVATION_RE = re.compile(r"^### (INTENT-PROV-(\d{4}))\s+—\s+(.+)$")
PHASE057_INPUT_CONTRACT = (
    ("P062-NAV-001", "Codex/plans/2026-07-28-phase057-v1021-read-map.md", 85),
    ("P062-NAV-002", "Codex/results/PHASE_057J_V1021_CONTROL_DOCUMENT_INTENT_OBSERVATIONS.md", 197),
    ("P062-NAV-003", "Codex/results/PHASE_057K_V1021_Q0_BASELINE_OBSERVATIONS.md", 79),
    ("P062-NAV-004", "Codex/results/PHASE_057L_V1021_Q2_Q3_SNAPSHOT_OBSERVATIONS.md", 126),
    ("P062-NAV-005", "Codex/results/PHASE_057M_V1021_Q4_Q5NAV_SNAPSHOT_OBSERVATIONS.md", 97),
    ("P062-NAV-006", "Codex/results/PHASE_057N_V1021_Q5_Q5B_SNAPSHOT_OBSERVATIONS.md", 101),
    ("P062-NAV-007", "Codex/results/PHASE_057O_V1021_Q6_Q7_AND_VERSION_CLOSE_OBSERVATIONS.md", 134),
)
PDF_SOURCE_PAIRS = (
    ("P062-PDF-SOURCE-001", "Claude/docs/v1.0.21/appendix_phase_separation.tex", "Claude/docs/v1.0.21/appendix_phase_separation.pdf"),
    ("P062-PDF-SOURCE-002", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf"),
    ("P062-PDF-SOURCE-003", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.tex", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf"),
    ("P062-PDF-SOURCE-004", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.tex", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf"),
    ("P062-PDF-SOURCE-005", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.tex", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf"),
)
PDF_PAGE_COUNTS = {
    "Claude/docs/v1.0.21/appendix_phase_separation.pdf": 8,
    "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf": 76,
    "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf": 78,
    "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf": 26,
    "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf": 26,
}


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


def normalize_lf(data: bytes) -> bytes:
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pdf_outline_nodes(items: list[Any]) -> int:
    return sum(pdf_outline_nodes(item) if isinstance(item, list) else 1 for item in items)


def pdf_annotation_count(reader: PdfReader) -> int:
    count = 0
    for page in reader.pages:
        annotations = page.get("/Annots", [])
        if hasattr(annotations, "get_object"):
            annotations = annotations.get_object()
        count += len(annotations)
    return count


def normalized_pdf_page_text(page: Any) -> str:
    return re.sub(r"\s+", " ", page.extract_text() or "").strip()


def word_cosine_similarity(left: str, right: str) -> float:
    left_counts = Counter(re.findall(r"\w+", left))
    right_counts = Counter(re.findall(r"\w+", right))
    numerator = sum(left_counts[key] * right_counts[key] for key in left_counts.keys() & right_counts.keys())
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


def reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def strict_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise NonFiniteNumberError(value)
    return parsed


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def walk(value: Any, path: str = "$", stats: dict[str, int] | None = None) -> dict[str, int]:
    if stats is None:
        stats = {"nodes": 0, "mapping_keys": 0, "objects": 0, "arrays": 0, "scalars": 0, "max_depth": 0}
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], path.count(".") + path.count("["))
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(path)
    if isinstance(value, dict):
        stats["objects"] += 1
        stats["mapping_keys"] += len(value)
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(path)
            walk(child, f"{path}.{key}", stats)
    elif isinstance(value, list):
        stats["arrays"] += 1
        for index, child in enumerate(value):
            walk(child, f"{path}[{index}]", stats)
    elif value is None or isinstance(value, (str, int, float, bool)):
        stats["scalars"] += 1
    else:
        raise TypeError(path)
    return stats


def strict_json_bytes(data: bytes) -> tuple[Any, dict[str, int]]:
    value = json.loads(
        data.decode("utf-8"), object_pairs_hook=strict_pairs,
        parse_constant=reject_constant, parse_float=strict_float,
    )
    return value, walk(value)


def run(args: list[str], timeout: int = TIMEOUT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=timeout)


def git_bytes(*args: str) -> bytes:
    proc = run(["git", *args], timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip())
    return proc.stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def git_blob(commit: str, path: str) -> tuple[str, str, bytes]:
    raw = git_bytes("ls-tree", "--full-tree", "-z", commit, "--", path)
    rows = [row for row in raw.split(b"\0") if row]
    if len(rows) != 1:
        raise FileNotFoundError(f"{commit}:{path}")
    meta, actual = rows[0].split(b"\t", 1)
    mode, kind, blob = meta.decode("ascii").split()
    if kind != "blob" or actual.decode("utf-8") != path:
        raise ValueError(path)
    return mode, blob, git_bytes("cat-file", "blob", blob)


@lru_cache(maxsize=1)
def manifest_metadata_rows() -> tuple[tuple[int, dict[str, Any]], ...]:
    manifest, _ = strict_json_bytes(normalize_lf(MANIFEST.read_bytes()))
    return tuple(
        (index, row)
        for index, row in enumerate(manifest.get("entries", []), start=1)
        if row.get("version") == "v1.0.21"
    )


@lru_cache(maxsize=1)
def phase057_expected_contract() -> tuple[tuple[dict[str, Any], ...], tuple[tuple[str, tuple[str, ...]], ...]]:
    observations: list[dict[str, Any]] = []
    nav_ids: list[tuple[str, tuple[str, ...]]] = []
    for nav_id, path, expected_lines in PHASE057_INPUT_CONTRACT:
        mode, blob, data = git_blob(ACTIVATION, path)
        lines = data.decode("utf-8").splitlines()
        if mode != "100644" or len(lines) != expected_lines:
            raise ValueError(f"Phase057 frozen input mismatch: {path}")
        if nav_id == "P062-NAV-001":
            nav_ids.append((nav_id, ()))
            continue
        headings = [
            (number, match)
            for number, line in enumerate(lines, start=1)
            if (match := PHASE057_OBSERVATION_RE.match(line))
        ]
        ids: list[str] = []
        for position, (line_start, match) in enumerate(headings):
            line_end = headings[position + 1][0] - 1 if position + 1 < len(headings) else len(lines)
            observation_id = match.group(1)
            ids.append(observation_id)
            section = ("\n".join(lines[line_start - 1:line_end]) + "\n").encode("utf-8")
            observations.append({
                "observation_id": observation_id, "source_path": path,
                "source_blob_sha1": blob, "source_sha256": digest(data),
                "line_start": line_start, "line_end": line_end, "heading": match.group(3),
                "section_sha256": digest(section),
            })
        nav_ids.append((nav_id, tuple(ids)))
    return tuple(observations), tuple(nav_ids)


def read_artifact(path: Path) -> tuple[Any, dict[str, int]]:
    return strict_json_bytes(path.read_bytes())


def rebuild() -> tuple[dict[str, Any], dict[str, Any], bytes, bytes]:
    with tempfile.TemporaryDirectory(prefix="p062-step52-") as temp:
        proc = run([sys.executable, str(BUILDER), "--output-dir", temp, "--determinism-check"])
        if proc.returncode != 0:
            raise RuntimeError("BUILDER_RECONSTRUCTION: " + proc.stderr.decode("utf-8", errors="replace"))
        if b"PASS_P062_STEP52_BUILDER_DETERMINISM 2/2" not in proc.stdout:
            raise RuntimeError("BUILDER_DETERMINISM_TERMINAL")
        top_bytes = (Path(temp) / TOPOLOGY.name).read_bytes()
        att_bytes = (Path(temp) / ATTESTATION.name).read_bytes()
        top, _ = strict_json_bytes(top_bytes)
        att, _ = strict_json_bytes(att_bytes)
        return top, att, top_bytes, att_bytes


def add_if(errors: set[str], condition: bool, code: str) -> None:
    if condition:
        errors.add(code)


def git_history_row_valid(row: dict[str, Any]) -> bool:
    commit = row.get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        return False
    parents = git_text("show", "-s", "--format=%P", commit).split()
    subject = git_text("show", "-s", "--format=%s", commit)
    paths = sorted(
        item.decode("utf-8").replace("\\", "/")
        for item in git_bytes("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", commit).split(b"\0")
        if item
    )
    raw = git_bytes("diff-tree", "--root", "--raw", "-r", "--no-renames", "-z", commit)
    patch = git_bytes("show", "--format=", "--binary", "--full-index", "--no-ext-diff", "--no-renames", commit)
    return (
        row.get("parents") == parents
        and row.get("subject") == subject
        and row.get("changed_paths") == paths
        and row.get("changed_path_set_sha256") == digest(("\n".join(paths) + "\n").encode("utf-8"))
        and row.get("raw_diff_tree_sha256") == digest(raw)
        and row.get("patch_sha256") == digest(patch)
    )


def is_ancestor(older: str, newer: str) -> bool:
    proc = run(["git", "merge-base", "--is-ancestor", older, newer], timeout=60)
    return proc.returncode == 0


def manifest_surface_contract(errors: set[str], top: dict[str, Any], att: dict[str, Any]) -> None:
    selected = manifest_metadata_rows()
    sources = top.get("sources", [])
    if len(selected) != 68 or len(sources) != 68:
        errors.add("SOURCE_COVERAGE")
        return
    text_by_id = {row.get("source_id"): row for row in att.get("release_text_records", [])}
    pdf_by_id = {row.get("source_id"): row for row in att.get("pdf_records", [])}
    snapshot_by_id = {row.get("source_id"): row for row in att.get("snapshot_records", [])}
    for release_index, ((manifest_index, entry), source) in enumerate(zip(selected, sources), start=1):
        expected = {
            "source_id": f"P062-SRC-{release_index:04d}",
            "release_occurrence_index": release_index,
            "manifest_index": manifest_index,
            "path": entry.get("path"), "blob_sha1": entry.get("blob_sha"),
            "git_mode": entry.get("git_mode"), "size_bytes": entry.get("size_bytes"),
            "extension": entry.get("extension"), "role": entry.get("role"),
            "review_mode": entry.get("review_mode"),
        }
        if any(source.get(key) != value for key, value in expected.items()):
            errors.add("SOURCE_GIT_IDENTITY")
        if source.get("manifest_extent") != entry.get("extent") or source.get("dedup_group") != entry.get("dedup_group"):
            errors.add("SOURCE_MANIFEST_LINK")
        record = text_by_id.get(source.get("source_id")) if entry.get("review_mode") == "FULL_TEXT" else pdf_by_id.get(source.get("source_id"))
        if record is None:
            errors.add("READ_RECORD_COVERAGE")
            continue
        if any(record.get(key) != source.get(key) for key in ("path", "blob_sha1", "sha256")):
            errors.add("READ_RECORD_IDENTITY")
        extent = source.get("extent", {})
        if entry.get("review_mode") == "FULL_TEXT":
            if record.get("physical_lines") != extent.get("lines") or record.get("nonblank_lines") != extent.get("nonblank_lines"):
                errors.add("TEXT_EXTENT")
            if record.get("human_read_state") != "READ_FULL":
                errors.add("HUMAN_TEXT_COVERAGE")
            if record.get("encoding") != "utf-8" or record.get("bom") is not False or record.get("newline_style") != "LF":
                errors.add("TEXT_ENCODING_NEWLINE")
            if entry.get("extension") == "json":
                snapshot = snapshot_by_id.get(source.get("source_id"), {})
                if record.get("strict_json_traversal") != snapshot.get("strict_json_traversal"):
                    errors.add("SNAPSHOT_INDEPENDENT_TRAVERSAL")
        else:
            if record.get("pages_observed") != extent.get("pages") or record.get("visual_review_state") != "VISUAL_FULL":
                errors.add("PDF_PAGE_VISUAL_COVERAGE")


def independent_manifest_rows(errors: set[str], top: dict[str, Any], att: dict[str, Any]) -> None:
    manifest_bytes = normalize_lf(MANIFEST.read_bytes())
    try:
        manifest, _ = strict_json_bytes(manifest_bytes)
    except Exception:
        errors.add("MANIFEST_STRICT_JSON")
        return
    add_if(errors, digest(manifest_bytes) != MANIFEST_SHA256, "MANIFEST_IDENTITY")
    add_if(errors, manifest.get("baseline_commit") != BASELINE, "MANIFEST_BASELINE")
    selected = [(index, row) for index, row in enumerate(manifest.get("entries", []), 1) if row.get("version") == "v1.0.21"]
    add_if(errors, len(selected) != 68 or [i for i, _ in selected] != list(range(472, 540)), "MANIFEST_DENOMINATOR")
    sources = top.get("sources", [])
    if len(sources) != 68 or len(selected) != 68:
        errors.add("SOURCE_COVERAGE")
        return
    expected_ids = [f"P062-SRC-{index:04d}" for index in range(1, 69)]
    add_if(errors, [row.get("source_id") for row in sources] != expected_ids, "SOURCE_IDS")
    seen_paths: set[str] = set()
    seen_blobs: set[str] = set()
    text_by_id = {row.get("source_id"): row for row in att.get("release_text_records", [])}
    pdf_by_id = {row.get("source_id"): row for row in att.get("pdf_records", [])}
    snapshot_by_id = {row.get("source_id"): row for row in att.get("snapshot_records", [])}
    pdf_metrics: dict[str, dict[str, Any]] = {}
    add_if(errors, len(snapshot_by_id) != 9, "SNAPSHOT_COVERAGE")
    for release_index, ((manifest_index, entry), source) in enumerate(zip(selected, sources), 1):
        try:
            mode, blob, data = git_blob(BASELINE, entry["path"])
        except Exception:
            errors.add("SOURCE_GIT_IDENTITY")
            continue
        expected = {
            "release_occurrence_index": release_index, "manifest_index": manifest_index,
            "path": entry["path"], "blob_sha1": blob, "sha256": digest(data),
            "git_mode": mode, "size_bytes": len(data), "extension": entry["extension"],
            "role": entry["role"], "review_mode": entry["review_mode"],
        }
        add_if(errors, any(source.get(k) != v for k, v in expected.items()), "SOURCE_GIT_IDENTITY")
        add_if(errors, source.get("manifest_extent") != entry.get("extent") or source.get("dedup_group") != entry.get("dedup_group"), "SOURCE_MANIFEST_LINK")
        seen_paths.add(source.get("path", "")); seen_blobs.add(source.get("blob_sha1", ""))
        record = text_by_id.get(source.get("source_id")) if entry["review_mode"] == "FULL_TEXT" else pdf_by_id.get(source.get("source_id"))
        if record is None:
            errors.add("READ_RECORD_COVERAGE")
        elif any(record.get(k) != expected[k] for k in ("path", "blob_sha1", "sha256")):
            errors.add("READ_RECORD_IDENTITY")
        elif entry["review_mode"] == "FULL_TEXT":
            lines = data.decode("utf-8").splitlines()
            expected_extent = {"lines": len(lines), "nonblank_lines": sum(bool(x.strip()) for x in lines), "pages": 0, "bytes": len(data)}
            if source.get("extent") != expected_extent or source.get("read_state") != "READ_FULL":
                errors.add("SOURCE_EXTENT_READ_STATE")
            if record.get("physical_lines") != len(lines) or record.get("nonblank_lines") != sum(bool(x.strip()) for x in lines):
                errors.add("TEXT_EXTENT")
            if record.get("human_read_state") != "READ_FULL":
                errors.add("HUMAN_TEXT_COVERAGE")
            expected_review_id = "P062-REVIEW-A-RELEASE-PDF-214" if release_index <= 54 else "P062-REVIEW-B-PROCESS-SNAPSHOT"
            if record.get("review_evidence_id") != expected_review_id:
                errors.add("HUMAN_TEXT_COVERAGE")
            if (record.get("encoding") != "utf-8" or record.get("bom") is not False
                    or record.get("newline_style") != "LF" or data.startswith(b"\xef\xbb\xbf") or b"\r" in data):
                errors.add("TEXT_ENCODING_NEWLINE")
            if entry["extension"] == "json":
                try:
                    _, traversal = strict_json_bytes(data)
                    snapshot = snapshot_by_id.get(source.get("source_id"), {})
                    if (record.get("strict_json_traversal") != traversal
                            or snapshot.get("path") != entry["path"]
                            or snapshot.get("blob_sha1") != blob
                            or snapshot.get("raw_sha256") != digest(data)
                            or snapshot.get("physical_lines") != len(lines)
                            or snapshot.get("strict_json_traversal") != traversal
                            or snapshot.get("parse_state") != "STRICT_FULL_TRAVERSAL"):
                        errors.add("SNAPSHOT_INDEPENDENT_TRAVERSAL")
                except Exception:
                    errors.add("SNAPSHOT_INDEPENDENT_TRAVERSAL")
        else:
            expected_extent = {"lines": 0, "nonblank_lines": 0, "pages": entry["extent"]["pages"], "bytes": len(data)}
            if source.get("extent") != expected_extent or source.get("read_state") != "VISUAL_FULL":
                errors.add("SOURCE_EXTENT_READ_STATE")
            if record.get("pages_observed") != entry["extent"]["pages"] or record.get("visual_review_state") != "VISUAL_FULL":
                errors.add("PDF_PAGE_VISUAL_COVERAGE")
            try:
                reader = PdfReader(io.BytesIO(data), strict=True)
                if reader.is_encrypted or len(reader.pages) != entry["extent"]["pages"]:
                    errors.add("PDF_INDEPENDENT_PARSE")
                pdf_metrics[entry["path"]] = {
                    "pages": len(reader.pages),
                    "outline_nodes": pdf_outline_nodes(reader.outline),
                    "annotations": pdf_annotation_count(reader),
                    "normalized_page_text": [normalized_pdf_page_text(page) for page in reader.pages],
                }
            except Exception:
                errors.add("PDF_INDEPENDENT_PARSE")
    for relationship in att.get("pdf_variant_relationships", []):
        base = pdf_metrics.get(relationship.get("base_pdf_path"), {})
        navigation = pdf_metrics.get(relationship.get("navigation_pdf_path"), {})
        base_text = base.get("normalized_page_text", [])
        navigation_text = navigation.get("normalized_page_text", [])
        exact_identity = sum(left == right for left, right in zip(base_text, navigation_text))
        byte_expected = {
            "base_pages": base.get("pages"),
            "navigation_pages": navigation.get("pages"),
            "base_outline_nodes": base.get("outline_nodes"),
            "navigation_outline_nodes": navigation.get("outline_nodes"),
            "base_annotations": base.get("annotations"),
            "navigation_annotations": navigation.get("annotations"),
            "exact_normalized_page_text_identity_pages": exact_identity,
        }
        if any(relationship.get(key) != value for key, value in byte_expected.items()):
            errors.add("PDF_VARIANT_BYTE_RECOMPUTATION")
        if relationship.get("relationship_id") == "P062-PDF-VARIANT-CH2":
            similarities = [word_cosine_similarity(left, right) for left, right in zip(base_text, navigation_text)]
            observed_range = [round(min(similarities), 4), round(max(similarities), 4)] if similarities else []
            stored_range = relationship.get("same_ordinal_page_text_similarity_range")
            if (not isinstance(stored_range, list) or len(stored_range) != 2
                    or any(abs(float(stored) - observed) > 0.00011 for stored, observed in zip(stored_range, observed_range))):
                errors.add("PDF_VARIANT_BYTE_RECOMPUTATION")
    add_if(errors, len(seen_paths) != 68 or len(seen_blobs) != 68, "SOURCE_UNIQUENESS")
    path_rows = sorted(sources, key=lambda row: row.get("path", ""))
    expected_path_set = digest(("\n".join(row.get("path", "") for row in path_rows) + "\n").encode("utf-8"))
    expected_path_blob_set = digest(("\n".join(f"{row.get('path', '')}\t{row.get('blob_sha1', '')}" for row in path_rows) + "\n").encode("utf-8"))
    add_if(errors, top.get("path_set_sha256") != expected_path_set or top.get("path_blob_set_sha256") != expected_path_blob_set, "SOURCE_SET_HASH")


def semantic_diagnostics(top: dict[str, Any], att: dict[str, Any], rebuilt_top: dict[str, Any], rebuilt_att: dict[str, Any], *, git_check: bool = True) -> set[str]:
    errors: set[str] = set()
    add_if(errors, top != rebuilt_top, "TOPOLOGY_RECONSTRUCTION")
    add_if(errors, att != rebuilt_att, "ATTESTATION_RECONSTRUCTION")
    add_if(errors, top.get("schema_version") != 1 or top.get("phase") != 62 or top.get("step") != "52", "TOPOLOGY_SCHEMA")
    add_if(errors, att.get("schema_version") != 1 or att.get("phase") != 62 or att.get("step") != "52", "ATTESTATION_SCHEMA")
    add_if(errors, top.get("baseline_commit") != BASELINE or top.get("activation_commit") != ACTIVATION, "COMMIT_IDENTITY")
    add_if(errors, top.get("counts") != EXPECTED_COUNTS, "TOPOLOGY_COUNTS")
    add_if(errors, att.get("counts") != EXPECTED_ATTESTATION, "ATTESTATION_COUNTS")
    add_if(errors, top.get("status") != "PASS_SOURCE_PROCESS_IDENTITY_TOPOLOGY", "TOPOLOGY_GATE")
    add_if(errors, att.get("status") != "PASS_FULL_READ_ATTESTATION", "ATTESTATION_GATE")
    manifest_surface_contract(errors, top, att)
    policy = top.get("denominator_policy", {})
    add_if(errors, policy != {"release": "V1021_RELEASE_68", "supplemental": "SUPPLEMENTAL_PROCESS_CONTROL", "q1_comparison": "Q1_COMPARISON_PROCESS_EVIDENCE", "fusion_allowed": False}, "DENOMINATOR_FUSION")
    add_if(errors, top.get("review_mode_counts") != {"FULL_PDF": 5, "FULL_TEXT": 63}, "REVIEW_MODE_COUNTS")
    add_if(errors, bool(top.get("duplicates")), "DUPLICATE_SOURCE_BLOB")
    supplemental = top.get("supplemental_process_control", {})
    add_if(errors, supplemental.get("path") != SUPPLEMENTAL_PATH or supplemental.get("blob_sha1") != SUPPLEMENTAL_BLOB, "SUPPLEMENTAL_IDENTITY")
    add_if(errors, supplemental.get("manifest_member") is not False or supplemental.get("denominator") != "SUPPLEMENTAL_PROCESS_CONTROL", "SUPPLEMENTAL_DENOMINATOR")
    add_if(errors, supplemental.get("extent") != {"bytes": 10664, "lines": 76, "nonblank_lines": 59}, "SUPPLEMENTAL_EXTENT")
    add_if(errors, supplemental.get("authority_class") != "RECORDED_SECOND_ORDER_REQUIREMENT" or supplemental.get("read_state") != "READ_FULL", "SUPPLEMENTAL_AUTHORITY_READ_STATE")
    add_if(errors, supplemental.get("first_order_user_transcript_state") != "GROUND_NOT_FOUND", "USER_TRANSCRIPT_FALSE_PRESENT")
    q1 = top.get("q1_comparison_report", {})
    add_if(errors, q1.get("path") != Q1_PATH or q1.get("blob_sha1") != Q1_BLOB, "Q1_IDENTITY")
    add_if(errors, q1.get("manifest_member") is not False or q1.get("supplemental_member") is not False, "Q1_DENOMINATOR")
    add_if(errors, q1.get("existence_state") != "PARTIAL_CONFLICT" or q1.get("chronology_state") != "CONFLICTING", "Q1_FALSE_COMPLETION")
    anchors = q1.get("section_anchors", [])
    add_if(errors, len(anchors) != 8 or [row.get("heading", "")[3:5] for row in anchors] != [f"§{i}" for i in range(1, 9)], "Q1_SECTION_ANCHORS")
    conflict = q1.get("chronology_conflict_anchors", {})
    report_anchor = conflict.get("report_complete", {})
    plan_anchor = conflict.get("master_plan_incomplete", {})
    add_if(errors, report_anchor.get("path") != Q1_PATH or report_anchor.get("line_start") != 285 or report_anchor.get("line_end") != 285 or report_anchor.get("match_count") != 1, "Q1_CHRONOLOGY_ANCHORS")
    add_if(errors, plan_anchor.get("path") != SUPPLEMENTAL_PATH or plan_anchor.get("line_start") != 76 or plan_anchor.get("line_end") != 76 or plan_anchor.get("match_count") != 1, "Q1_CHRONOLOGY_ANCHORS")
    add_if(errors, conflict.get("origin_commit") != SUPPORT_HISTORY[1][1] or q1.get("origin_commit") != SUPPORT_HISTORY[1][1], "Q1_CHRONOLOGY_ANCHORS")
    add_if(errors, q1.get("read_state") != "READ_FULL" or q1.get("review_evidence_id") != "P062-REVIEW-D-Q1-COMPARISON", "Q1_READ_STATE")
    process = top.get("process_artifacts", [])
    process_map = {row.get("process_artifact_id"): row for row in process}
    add_if(errors, len(process_map) != len(process) or len(process) != 53, "PROCESS_COVERAGE")
    process_docs = {row.get("artifact_kind"): row for row in process if row.get("q_id") == "CROSS_PHASE"}
    for kind, (created, modified, chronology, authority) in PROCESS_DOCUMENT_CONTRACT.items():
        row = process_docs.get(kind, {})
        if (row.get("created_commit") != created or row.get("last_modified_commit") != modified
                or row.get("commit") != modified or row.get("authored_commit") != modified
                or row.get("observed_at_commit") != BASELINE or row.get("chronology_state") != chronology
                or row.get("authority_class") != authority):
            errors.add("PROCESS_DOCUMENT_CHRONOLOGY")
        if git_check:
            try:
                _, created_blob, _ = git_blob(created, row.get("path", ""))
                _, modified_blob, _ = git_blob(modified, row.get("path", ""))
                if row.get("created_blob_sha1") != created_blob or row.get("blob_sha1") != modified_blob:
                    errors.add("PROCESS_DOCUMENT_CHRONOLOGY")
            except Exception:
                errors.add("PROCESS_DOCUMENT_CHRONOLOGY")
    aliases = top.get("process_aliases", [])
    expected_aliases = {
        "Q5NAV": ("Q5", "SUBPHASE_ALIAS", False),
        "Q5B": ("Q5", "SUBPHASE_ALIAS", False),
    }
    if len(aliases) != 2 or {row.get("alias_q_id") for row in aliases} != set(expected_aliases):
        errors.add("PROCESS_ALIAS_CONTRACT")
    else:
        for row in aliases:
            parent, state, dedicated = expected_aliases[row["alias_q_id"]]
            if row.get("parent_q_id") != parent or row.get("state") != state or row.get("dedicated_plan_step_log_result_expected") is not dedicated or not row.get("reason"):
                errors.add("PROCESS_ALIAS_CONTRACT")
    for q_id in PROCESS_PHASES:
        if q_id not in {"Q5NAV", "Q5B"}:
            for kind in ("PLAN", "STEP_LOG", "RESULT"):
                row = process_map.get(f"P062-PROC-{q_id}-{kind}", {})
                if row.get("existence_state") != "GROUND_NOT_FOUND" or any(row.get(k) is not None for k in ("path", "blob_sha1", "commit")):
                    errors.add("FALSE_PHASE_ARTIFACT_PRESENT")
        snap = process_map.get(f"P062-PROC-{q_id}-SNAPSHOT", {})
        if q_id in SNAPSHOT_PHASES:
            expected_path, expected_commit = SNAPSHOT_CONTRACT[q_id]
            source = next((row for row in top.get("sources", []) if row.get("path") == expected_path), {})
            if (snap.get("existence_state") != "PRESENT" or snap.get("chronology_state") != "CONTEMPORANEOUS"
                    or snap.get("path") != expected_path or snap.get("blob_sha1") != source.get("blob_sha1")
                    or snap.get("commit") != expected_commit or snap.get("authored_commit") != expected_commit
                    or snap.get("observed_at_commit") != BASELINE):
                errors.add("SNAPSHOT_TOPOLOGY")
            if git_check:
                try:
                    _, authored_blob, _ = git_blob(expected_commit, expected_path)
                    if authored_blob != snap.get("blob_sha1"):
                        errors.add("SNAPSHOT_TOPOLOGY")
                except Exception:
                    errors.add("SNAPSHOT_TOPOLOGY")
        elif q_id in GNF_SNAPSHOT_PHASES:
            if snap.get("existence_state") != "GROUND_NOT_FOUND" or snap.get("path") is not None:
                errors.add("INVENTED_SNAPSHOT")
    q1_partial = process_map.get("P062-PROC-Q1-PARTIAL-REPORT", {})
    add_if(errors, q1_partial.get("existence_state") != "PARTIAL_CONFLICT" or q1_partial.get("artifact_kind") != "PARTIAL_REPORT", "Q1_FALSE_COMPLETION")
    for q_id in ("Q9", "Q10"):
        row = process_map.get(f"P062-PROC-{q_id}-DOWNSTREAM-CLOSURE", {})
        add_if(errors, row.get("chronology_state") != "DOWNSTREAM_AUTHORED" or row.get("authority_class") != "INTERNAL_SUBSTITUTE_CLOSURE", "DOWNSTREAM_AS_CONTEMPORANEOUS")
    gnf = top.get("ground_not_found", [])
    add_if(errors, len(gnf) != 37 or len({row.get("ground_id") for row in gnf}) != 37, "GROUND_NOT_FOUND_COVERAGE")
    expected_gnf_ids = {
        f"P062-GNF-{q_id}-{kind}"
        for q_id in PROCESS_PHASES if q_id not in {"Q5NAV", "Q5B"}
        for kind in ("PLAN", "STEP_LOG", "RESULT")
    } | {f"P062-GNF-{q_id}-SNAPSHOT" for q_id in GNF_SNAPSHOT_PHASES}
    if {row.get("ground_id") for row in gnf} != expected_gnf_ids:
        errors.add("GROUND_NOT_FOUND_COVERAGE")
    for row in gnf:
        if (row.get("matches") != [] or row.get("supplemental_checked_as_master_plan_not_dedicated") is not True
                or not row.get("search_space") or not row.get("search_rule")
                or not isinstance(row.get("expected_by_anchor"), dict)
                or row["expected_by_anchor"].get("path") != SUPPLEMENTAL_PATH
                or row["expected_by_anchor"].get("match_count") != 1):
            errors.add("GROUND_NOT_FOUND_SEARCH")
    history = top.get("history", {})
    impl = history.get("implementation_chain", [])
    support = history.get("supporting_commits", [])
    add_if(errors, len(impl) != 10 or len(support) != 3, "HISTORY_COVERAGE")
    add_if(errors, [(row.get("event"), row.get("commit"), row.get("chronology_state")) for row in impl]
           != [(event, commit, "CONTEMPORANEOUS") for event, commit in IMPLEMENTATION_HISTORY], "HISTORY_EXACT_COMMITS")
    add_if(errors, [(row.get("event"), row.get("commit"), row.get("chronology_state")) for row in support]
           != list(SUPPORT_HISTORY), "HISTORY_EXACT_COMMITS")
    for index in range(1, len(impl)):
        if impl[index - 1].get("commit") not in impl[index].get("parents", []):
            errors.add("HISTORY_CHAIN")
    ancestry = history.get("ancestry_relationships", [])
    expected_ancestry = [
        ("P062-HIST-ANCESTRY-001", "66e3510d67162dd6bd88158557f96621cbedbbcf", "b4e939b0547cd4bf73bca30abe10fd164954c277"),
        ("P062-HIST-ANCESTRY-002", "1e6c610f11682d87a416957b1cf65b4c8df53697", "b4e939b0547cd4bf73bca30abe10fd164954c277"),
        ("P062-HIST-ANCESTRY-003", "e96147fe4d5cefcccf733702e9bee78ba0beb025", "5d815235de4e302ff5d7a076d525921ab417eadf"),
    ]
    add_if(errors, [(row.get("relationship_id"), row.get("older"), row.get("newer")) for row in ancestry] != expected_ancestry or any(row.get("state") != "ANCESTOR" for row in ancestry), "HISTORY_ANCESTRY")
    if git_check:
        try:
            if not all(git_history_row_valid(row) for row in impl + support):
                errors.add("HISTORY_PATCH_IDENTITY")
            if not all(is_ancestor(older, newer) for _, older, newer in expected_ancestry):
                errors.add("HISTORY_ANCESTRY")
            if not all(is_ancestor(commit, BASELINE) for _, commit, _ in SUPPORT_HISTORY):
                errors.add("HISTORY_ANCESTRY")
            _, q1_origin_blob, _ = git_blob(SUPPORT_HISTORY[1][1], Q1_PATH)
            if q1_origin_blob != Q1_BLOB or Q1_PATH not in support[1].get("changed_paths", []):
                errors.add("HISTORY_PATCH_IDENTITY")
        except Exception:
            errors.add("HISTORY_PATCH_IDENTITY")
    for row in process + top.get("sources", []):
        if row.get("external_scientific_truth_validated") is not False or row.get("external_material_truth_validated") is not False:
            errors.add("EXTERNAL_TRUTH_PROMOTION")
    for row in top.get("sources", []):
        if row.get("review_mode") == "FULL_PDF" and row.get("authority_class") != "GENERATED_VISUAL_WITNESS":
            errors.add("PDF_TO_SCIENCE_PROMOTION")
        if row.get("role") == "test" and row.get("authority_class") != "INTERNAL_TEST_SURFACE":
            errors.add("TEST_TO_SCIENCE_PROMOTION")
    nav = top.get("phase057_navigation_inputs", [])
    add_if(errors, len(nav) != 7 or sum(row.get("physical_lines", 0) for row in nav) != 819, "PHASE057_COVERAGE")
    for row in nav:
        if row.get("authority_class") != "PROVISIONAL_NAVIGATION_ONLY" or not row.get("reverification_evidence") or not row.get("unverified"):
            errors.add("PHASE057_AUTHORITY_BOUNDARY")
    observations = top.get("phase057_observations", [])
    expected_observation_ids = [f"INTENT-PROV-{index:04d}" for index in range(66, 96)]
    add_if(errors, [row.get("observation_id") for row in observations] != expected_observation_ids, "PHASE057_OBSERVATION_COVERAGE")
    add_if(errors, top.get("phase057_observation_id_sha256") != digest(("\n".join(expected_observation_ids) + "\n").encode("utf-8")), "PHASE057_OBSERVATION_COVERAGE")
    try:
        expected_observations, expected_nav_rows = phase057_expected_contract()
        expected_nav_observation_ids = {nav_id: list(ids) for nav_id, ids in expected_nav_rows}
        for navigation in nav:
            if navigation.get("observation_ids") != expected_nav_observation_ids.get(navigation.get("navigation_id")):
                errors.add("PHASE057_OBSERVATION_COVERAGE")
        if tuple(
            {key: row.get(key) for key in ("observation_id", "source_path", "source_blob_sha1", "source_sha256", "line_start", "line_end", "heading", "section_sha256")}
            for row in observations
        ) != expected_observations:
            errors.add("PHASE057_OBSERVATION_ANCHOR")
    except Exception:
        errors.add("PHASE057_OBSERVATION_ANCHOR")
    for row in observations:
        if (row.get("authority_class") != "PROVISIONAL_NAVIGATION_ONLY" or not row.get("source_path")
                or not isinstance(row.get("line_start"), int) or not isinstance(row.get("line_end"), int)
                or row.get("line_start", 0) > row.get("line_end", -1) or not row.get("section_sha256")
                or not row.get("unverified")):
            errors.add("PHASE057_OBSERVATION_AUTHORITY")
    by_observation = {row.get("observation_id"): row for row in observations}
    obs86 = by_observation.get("INTENT-PROV-0086", {})
    obs95 = by_observation.get("INTENT-PROV-0095", {})
    add_if(errors, obs86.get("contradiction_state") != "BYTE_INVARIANCE_LIMITATION_REPRODUCED", "PHASE057_OBSERVATION_SEMANTICS")
    add_if(errors, obs95.get("reproduction_state") != "PROVISIONAL_ADVICE_NOT_ADOPTED" or obs95.get("disposition_adoption_state") != "NOT_ADOPTED", "PHASE057_OBSERVATION_SEMANTICS")
    for observation_id, row in by_observation.items():
        if observation_id not in {"INTENT-PROV-0086", "INTENT-PROV-0095"}:
            add_if(errors, row.get("contradiction_state") != "NONE_FOUND_WITHIN_FROZEN_INTERNAL_TOPOLOGY"
                   or row.get("reproduction_state") != "REPRODUCED_WITH_AUTHORITY_BOUNDARY"
                   or row.get("disposition_adoption_state") != "NOT_APPLICABLE", "PHASE057_OBSERVATION_SEMANTICS")
    snapshots = att.get("snapshot_records", [])
    add_if(errors, len(snapshots) != 9, "SNAPSHOT_COVERAGE")
    for row in snapshots:
        traversal = row.get("strict_json_traversal")
        if row.get("parse_state") != "STRICT_FULL_TRAVERSAL" or not isinstance(traversal, dict) or traversal.get("nodes", 0) <= 0:
            errors.add("SNAPSHOT_STRICT_TRAVERSAL")
        if row.get("authority_class") != "PROCESS_EVIDENCE_NOT_SCIENTIFIC_TRUTH":
            errors.add("SNAPSHOT_TO_SCIENCE_PROMOTION")
    source_by_path = {row.get("path"): row for row in top.get("sources", [])}
    pdf_records = att.get("pdf_records", [])
    pdf_by_path = {row.get("path"): row for row in pdf_records}
    add_if(errors, set(pdf_by_path) != set(PDF_PAGE_COUNTS), "PDF_RECORD_COVERAGE")
    for path, page_count in PDF_PAGE_COUNTS.items():
        source = source_by_path.get(path, {})
        record = pdf_by_path.get(path, {})
        pages = record.get("pages", [])
        if ([row.get("page") for row in pages] != list(range(1, page_count + 1))
                or record.get("pages_expected") != page_count or record.get("pages_observed") != page_count
                or record.get("visual_review_state") != "VISUAL_FULL"
                or record.get("visual_review_method") != "POPPLER_120_DPI_FULL_PAGE"
                or record.get("review_evidence_id") != "P062-REVIEW-A-RELEASE-PDF-214"):
            errors.add("PDF_PAGE_ROWS")
        for page in pages:
            if (page.get("source_sha256") != source.get("sha256") or page.get("visual_state") != "VISUAL_FULL"
                    or page.get("review_evidence_id") != "P062-REVIEW-A-RELEASE-PDF-214"
                    or page.get("width_points") != 595.28 or page.get("height_points") != 841.89):
                errors.add("PDF_PAGE_ROWS")
    relationships = top.get("pdf_source_relationships", [])
    add_if(errors, [row.get("relationship_id") for row in relationships] != [row[0] for row in PDF_SOURCE_PAIRS], "PDF_SOURCE_RELATIONSHIPS")
    for row, (relationship_id, source_path, pdf_path) in zip(relationships, PDF_SOURCE_PAIRS):
        source = source_by_path.get(source_path, {})
        pdf = source_by_path.get(pdf_path, {})
        expected = {
            "relationship_id": relationship_id, "source_path": source_path, "pdf_path": pdf_path,
            "source_relationship_state": "SOURCE_DRIVER_PRESENT", "build_provenance_state": "UNVERIFIED",
            "authority_ceiling": "SOURCE_AND_DOCUMENT_IDENTITY_ONLY",
            "external_scientific_truth_validated": False, "external_material_truth_validated": False,
            "source_id": source.get("source_id"), "source_blob_sha1": source.get("blob_sha1"), "source_sha256": source.get("sha256"),
            "pdf_source_id": pdf.get("source_id"), "pdf_blob_sha1": pdf.get("blob_sha1"), "pdf_sha256": pdf.get("sha256"),
        }
        if row != expected:
            errors.add("PDF_SOURCE_RELATIONSHIPS")
    variants = att.get("pdf_variant_relationships", [])
    add_if(errors, [row.get("relationship_id") for row in variants] != ["P062-PDF-VARIANT-CH1", "P062-PDF-VARIANT-CH2"], "PDF_VARIANT_RELATIONSHIPS")
    exact_variant_values = {
        "P062-PDF-VARIANT-CH1": (
            "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf",
            76, 78, 81, 85, 1134, 1227, None,
            "navigation pages 73-74 add D.2 integrated symbol correspondence and Ch1-Ch2 relationship tables; references move from base pages 73-76 to navigation pages 75-78",
        ),
        "P062-PDF-VARIANT-CH2": (
            "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf",
            26, 26, 39, 39, 320, 323, [0.9691, 0.9997],
            "navigation title states global navigation edition and page 3 adds three links",
        ),
    }
    for row in variants:
        values = exact_variant_values.get(row.get("relationship_id"))
        if values is None:
            errors.add("PDF_VARIANT_RELATIONSHIPS")
            continue
        base_path, nav_path, base_pages, nav_pages, base_outline, nav_outline, base_ann, nav_ann, similarity, visual_difference = values
        base = pdf_by_path.get(base_path, {}); navigation = pdf_by_path.get(nav_path, {})
        if (row.get("base_pdf_path") != base_path or row.get("navigation_pdf_path") != nav_path
                or row.get("base_pages") != base_pages or row.get("navigation_pages") != nav_pages
                or row.get("base_outline_nodes") != base_outline or row.get("navigation_outline_nodes") != nav_outline
                or row.get("base_annotations") != base_ann or row.get("navigation_annotations") != nav_ann
                or row.get("exact_normalized_page_text_identity_pages") != 0
                or row.get("direct_visual_difference") != visual_difference
                or row.get("same_ordinal_page_text_similarity_range") != similarity
                or row.get("build_provenance_state") != "UNVERIFIED"
                or row.get("authority_ceiling") != "VISUAL_AND_DOCUMENT_STRUCTURE_ONLY"
                or row.get("base_source_id") != base.get("source_id") or row.get("base_blob_sha1") != base.get("blob_sha1") or row.get("base_sha256") != base.get("sha256")
                or row.get("navigation_source_id") != navigation.get("source_id") or row.get("navigation_blob_sha1") != navigation.get("blob_sha1") or row.get("navigation_sha256") != navigation.get("sha256")):
            errors.add("PDF_VARIANT_RELATIONSHIPS")
    partitions = att.get("partitions", [])
    add_if(errors, len(partitions) != 4 or {row.get("partition_id") for row in partitions} != {"A_RELEASE_ROOT_AND_PDF", "B_RELEASE_PROCESS_AND_SNAPSHOTS", "C_SUPPLEMENTAL_PROCESS_CONTROL", "D_Q1_COMPARISON_REPORT"}, "HUMAN_PARTITION_COVERAGE")
    human_evidence_contract = {
        "A_RELEASE_ROOT_AND_PDF": (
            "P062-REVIEW-A-RELEASE-PDF-214",
            ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_PDF_AUDITOR", "STEP52_CONTROLLER"],
            "UTF8_LINE_BY_LINE_AND_POPPLER_120_DPI_FULL_PAGE_VISUAL_REVIEW",
        ),
        "B_RELEASE_PROCESS_AND_SNAPSHOTS": (
            "P062-REVIEW-B-PROCESS-SNAPSHOT",
            ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_CONTROLLER"],
            "UTF8_LINE_BY_LINE_PLUS_STRICT_JSON_DUPLICATE_KEY_NONFINITE_REJECTION_AND_RECURSIVE_TRAVERSAL",
        ),
        "C_SUPPLEMENTAL_PROCESS_CONTROL": (
            "P062-REVIEW-C-SUPPLEMENTAL",
            ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_CONTROLLER"],
            "UTF8_LINE_BY_LINE",
        ),
        "D_Q1_COMPARISON_REPORT": (
            "P062-REVIEW-D-Q1-COMPARISON",
            ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_CONTROLLER"],
            "UTF8_LINE_BY_LINE_WITH_CHRONOLOGY_CONFLICT_COMPARISON",
        ),
    }
    release_sources = top.get("sources", [])
    expected_covered = {
        "A_RELEASE_ROOT_AND_PDF": [
            {key: row.get(key) for key in ("source_id", "path", "blob_sha1", "sha256")}
            for row in release_sources[:54]
        ],
        "B_RELEASE_PROCESS_AND_SNAPSHOTS": [
            {key: row.get(key) for key in ("source_id", "path", "blob_sha1", "sha256")}
            for row in release_sources[54:]
        ],
        "C_SUPPLEMENTAL_PROCESS_CONTROL": [
            {key: supplemental.get(key) for key in ("path", "blob_sha1", "sha256")}
        ],
        "D_Q1_COMPARISON_REPORT": [
            {key: q1.get(key) for key in ("path", "blob_sha1", "sha256")}
        ],
    }
    for row in partitions:
        actual = row.get("actual", {})
        expected = row.get("expected", {})
        extents_match = isinstance(actual, dict) and isinstance(expected, dict) and actual == expected
        if row.get("status") != "PASS_HUMAN_FULL_REVIEW" or not extents_match or not row.get("review_evidence"):
            errors.add("HUMAN_PARTITION_CONTRACT")
        partition_id = row.get("partition_id")
        evidence_id, reviewer_ids, method = human_evidence_contract.get(partition_id, (None, None, None))
        evidence = row.get("review_evidence", {})
        if (evidence.get("evidence_id") != evidence_id or evidence.get("reviewer_ids") != reviewer_ids
                or evidence.get("method") != method
                or (partition_id == "A_RELEASE_ROOT_AND_PDF" and evidence.get("renderer") != "Poppler pdftoppm 26.05.0")):
            errors.add("HUMAN_PARTITION_CONTRACT")
        stored_hash = row.get("review_contract_sha256")
        projection = copy.deepcopy(row)
        projection.pop("review_contract_sha256", None)
        covered = expected_covered.get(partition_id, [])
        if (stored_hash != digest(canonical(projection))
                or row.get("covered_source_set_sha256") != digest(canonical(covered))
                or row.get("covered_source_count") != len(covered)):
            errors.add("HUMAN_REVIEW_HASH")
    add_if(errors, att.get("human_review_contract_sha256") != digest(canonical(partitions)), "HUMAN_REVIEW_HASH")
    findings = [finding for row in partitions for finding in row.get("findings", [])]
    visual = next((row for row in findings if row.get("finding_id") == "P062-VIS-001"), None)
    expected_visual_paths = ["Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf"]
    add_if(errors, visual is None or visual.get("severity") != "P1_LAYOUT" or visual.get("state") != "CONFIRMED_VISUAL_DEFECT"
           or visual.get("paths") != expected_visual_paths or visual.get("pages") != [69]
           or visual.get("description") != "Table 8 rightmost column is clipped at the physical right page edge in both Ch1 variants."
           or visual.get("authority_ceiling") != "VISUAL_LAYOUT_ONLY", "VISUAL_FINDING_CONTRACT")
    add_if(errors, att.get("source_topology_semantic_sha256") != digest(canonical(top)), "TOPOLOGY_ATTESTATION_LINK")
    if git_check:
        independent_manifest_rows(errors, top, att)
        try:
            mode, blob, data = git_blob(BASELINE, SUPPLEMENTAL_PATH)
            add_if(errors, (mode, blob, len(data), len(data.decode("utf-8").splitlines())) != ("100644", SUPPLEMENTAL_BLOB, 10664, 76), "SUPPLEMENTAL_GIT_IDENTITY")
            mode, blob, data = git_blob(BASELINE, Q1_PATH)
            add_if(errors, (mode, blob, len(data), len(data.decode("utf-8").splitlines())) != ("100644", Q1_BLOB, 44969, 291), "Q1_GIT_IDENTITY")
        except Exception:
            errors.add("SUPPLEMENTAL_Q1_GIT_READ")
    return errors


def linked(top: dict[str, Any], att: dict[str, Any]) -> None:
    att["source_topology_semantic_sha256"] = digest(canonical(top))


def refresh_human_hashes(att: dict[str, Any]) -> None:
    for partition in att.get("partitions", []):
        projection = copy.deepcopy(partition)
        projection.pop("review_contract_sha256", None)
        partition["review_contract_sha256"] = digest(canonical(projection))
    att["human_review_contract_sha256"] = digest(canonical(att.get("partitions", [])))


def refresh_source_derivatives(top: dict[str, Any], att: dict[str, Any]) -> None:
    sources = top.get("sources", [])
    first = sources[0]
    for record in att.get("release_text_records", []) + att.get("pdf_records", []):
        if record.get("source_id") == first.get("source_id"):
            record["path"] = first.get("path")
            record["blob_sha1"] = first.get("blob_sha1")
    ordered = sorted(sources, key=lambda row: row.get("path", ""))
    top["path_set_sha256"] = digest(("\n".join(row.get("path", "") for row in ordered) + "\n").encode("utf-8"))
    top["path_blob_set_sha256"] = digest(("\n".join(f"{row.get('path', '')}\t{row.get('blob_sha1', '')}" for row in ordered) + "\n").encode("utf-8"))
    covered_sets = {
        "A_RELEASE_ROOT_AND_PDF": [
            {key: row.get(key) for key in ("source_id", "path", "blob_sha1", "sha256")}
            for row in sources[:54]
        ],
        "B_RELEASE_PROCESS_AND_SNAPSHOTS": [
            {key: row.get(key) for key in ("source_id", "path", "blob_sha1", "sha256")}
            for row in sources[54:]
        ],
    }
    for partition in att.get("partitions", []):
        covered = covered_sets.get(partition.get("partition_id"))
        if covered is not None:
            partition["covered_source_set_sha256"] = digest(canonical(covered))
    refresh_human_hashes(att)


def negative_controls(top: dict[str, Any], att: dict[str, Any]) -> tuple[int, list[str]]:
    controls: list[tuple[str, str, Callable[[dict[str, Any], dict[str, Any]], None]]] = []

    def control(name: str, code: str, mutation: Callable[[dict[str, Any], dict[str, Any]], None]) -> None:
        controls.append((name, code, mutation))

    control("release-count", "TOPOLOGY_COUNTS", lambda t, a: t["counts"].__setitem__("release_occurrences", 67))
    control("text-count", "ATTESTATION_COUNTS", lambda t, a: a["counts"].__setitem__("release_text_physical_lines", 21047))
    control("denominator-fusion", "DENOMINATOR_FUSION", lambda t, a: t["denominator_policy"].__setitem__("fusion_allowed", True))
    control("supplemental-user-transcript", "USER_TRANSCRIPT_FALSE_PRESENT", lambda t, a: t["supplemental_process_control"].__setitem__("first_order_user_transcript_state", "PRESENT"))
    control("q1-complete", "Q1_FALSE_COMPLETION", lambda t, a: t["q1_comparison_report"].__setitem__("existence_state", "COMPLETE"))
    control("invent-q1-snapshot", "INVENTED_SNAPSHOT", lambda t, a: next(x for x in t["process_artifacts"] if x["process_artifact_id"] == "P062-PROC-Q1-SNAPSHOT").update({"existence_state": "PRESENT", "path": Q1_PATH}))
    control("invent-q8-snapshot", "INVENTED_SNAPSHOT", lambda t, a: next(x for x in t["process_artifacts"] if x["process_artifact_id"] == "P062-PROC-Q8-SNAPSHOT").update({"existence_state": "PRESENT", "path": Q1_PATH}))
    control("invent-plan", "FALSE_PHASE_ARTIFACT_PRESENT", lambda t, a: next(x for x in t["process_artifacts"] if x["process_artifact_id"] == "P062-PROC-Q2-PLAN").update({"existence_state": "PRESENT", "path": SUPPLEMENTAL_PATH}))
    control("downstream-contemporary", "DOWNSTREAM_AS_CONTEMPORANEOUS", lambda t, a: next(x for x in t["process_artifacts"] if x["process_artifact_id"] == "P062-PROC-Q9-DOWNSTREAM-CLOSURE").__setitem__("chronology_state", "CONTEMPORANEOUS"))
    control("science-promotion", "EXTERNAL_TRUTH_PROMOTION", lambda t, a: t["sources"][0].__setitem__("external_scientific_truth_validated", True))
    control("pdf-promotion", "PDF_TO_SCIENCE_PROMOTION", lambda t, a: next(x for x in t["sources"] if x["review_mode"] == "FULL_PDF").__setitem__("authority_class", "SCIENTIFIC_TRUTH"))
    control("test-promotion", "TEST_TO_SCIENCE_PROMOTION", lambda t, a: next(x for x in t["sources"] if x["role"] == "test").__setitem__("authority_class", "SCIENTIFIC_TRUTH"))
    control("snapshot-promotion", "SNAPSHOT_TO_SCIENCE_PROMOTION", lambda t, a: a["snapshot_records"][0].__setitem__("authority_class", "SCIENTIFIC_TRUTH"))
    control("history-gap", "HISTORY_CHAIN", lambda t, a: t["history"]["implementation_chain"][1].__setitem__("parents", []))
    control("nav-authority", "PHASE057_AUTHORITY_BOUNDARY", lambda t, a: t["phase057_navigation_inputs"][0].__setitem__("authority_class", "CANONICAL_TRUTH"))
    control("human-partition", "HUMAN_PARTITION_CONTRACT", lambda t, a: a["partitions"][0].__setitem__("status", "PENDING_HUMAN_REVIEW"))
    control("human-text", "HUMAN_TEXT_COVERAGE", lambda t, a: a["release_text_records"][0].__setitem__("human_read_state", "PENDING_HUMAN_REVIEW"))
    control("human-pdf", "PDF_PAGE_ROWS", lambda t, a: a["pdf_records"][0].__setitem__("visual_review_method", "PENDING_VISUAL_REVIEW"))
    control("snapshot-traversal", "SNAPSHOT_STRICT_TRAVERSAL", lambda t, a: a["snapshot_records"][0].__setitem__("parse_state", "PARSED_ONLY"))
    control("visual-finding", "VISUAL_FINDING_CONTRACT", lambda t, a: next(f for p in a["partitions"] for f in p["findings"] if f["finding_id"] == "P062-VIS-001").__setitem__("pages", [68]))
    control("process-alias", "PROCESS_ALIAS_CONTRACT", lambda t, a: t["process_aliases"][0].__setitem__("dedicated_plan_step_log_result_expected", True))
    control("process-last-modified", "PROCESS_DOCUMENT_CHRONOLOGY", lambda t, a: next(x for x in t["process_artifacts"] if x.get("artifact_kind") == "EXECUTION_LEDGER").__setitem__("last_modified_commit", ACTIVATION))
    control("q1-conflict-anchor", "Q1_CHRONOLOGY_ANCHORS", lambda t, a: t["q1_comparison_report"]["chronology_conflict_anchors"]["report_complete"].__setitem__("line_start", 284))
    control("observation-0086", "PHASE057_OBSERVATION_SEMANTICS", lambda t, a: next(x for x in t["phase057_observations"] if x["observation_id"] == "INTENT-PROV-0086").__setitem__("contradiction_state", "NONE"))
    control("observation-0095", "PHASE057_OBSERVATION_SEMANTICS", lambda t, a: next(x for x in t["phase057_observations"] if x["observation_id"] == "INTENT-PROV-0095").__setitem__("disposition_adoption_state", "ADOPTED"))
    control("human-review-hash", "HUMAN_REVIEW_HASH", lambda t, a: a["partitions"][0].__setitem__("review_contract_sha256", "0" * 64))
    control("pdf-page-row", "PDF_PAGE_ROWS", lambda t, a: a["pdf_records"][0]["pages"][0].__setitem__("source_sha256", "0" * 64))
    control("pdf-source-relationship", "PDF_SOURCE_RELATIONSHIPS", lambda t, a: t["pdf_source_relationships"][0].__setitem__("build_provenance_state", "CONFIRMED"))
    control("pdf-variant-relationship", "PDF_VARIANT_RELATIONSHIPS", lambda t, a: a["pdf_variant_relationships"][0].__setitem__("base_pages", 75))
    control("source-path", "SOURCE_GIT_IDENTITY", lambda t, a: t["sources"][0].__setitem__("path", "Claude/docs/v1.0.21/MISSING"))
    control("source-blob", "SOURCE_GIT_IDENTITY", lambda t, a: t["sources"][0].__setitem__("blob_sha1", "0" * 40))
    control("source-mode", "SOURCE_GIT_IDENTITY", lambda t, a: t["sources"][0].__setitem__("git_mode", "100755"))
    control("source-size", "SOURCE_GIT_IDENTITY", lambda t, a: t["sources"][0].__setitem__("size_bytes", t["sources"][0]["size_bytes"] + 1))
    control("source-manifest-index", "SOURCE_GIT_IDENTITY", lambda t, a: t["sources"][0].__setitem__("manifest_index", 471))
    control("text-line", "TEXT_EXTENT", lambda t, a: a["release_text_records"][0].__setitem__("physical_lines", a["release_text_records"][0]["physical_lines"] - 1))
    control("pdf-page-missing", "PDF_PAGE_ROWS", lambda t, a: a["pdf_records"][0]["pages"].pop())
    control("snapshot-authored-commit", "SNAPSHOT_TOPOLOGY", lambda t, a: next(x for x in t["process_artifacts"] if x["process_artifact_id"] == "P062-PROC-Q2-SNAPSHOT").__setitem__("authored_commit", ACTIVATION))
    control("ground-search-match", "GROUND_NOT_FOUND_SEARCH", lambda t, a: t["ground_not_found"][0].__setitem__("matches", [SUPPLEMENTAL_PATH]))
    control("history-exact-commit", "HISTORY_EXACT_COMMITS", lambda t, a: t["history"]["supporting_commits"][0].__setitem__("chronology_state", "CONTEMPORANEOUS"))
    control("observation-heading", "PHASE057_OBSERVATION_ANCHOR", lambda t, a: t["phase057_observations"][0].__setitem__("heading", "mutated"))
    control("human-covered-source-hash", "HUMAN_REVIEW_HASH", lambda t, a: a["partitions"][0].__setitem__("covered_source_set_sha256", "0" * 64))
    control("human-review-method", "HUMAN_PARTITION_CONTRACT", lambda t, a: a["partitions"][0]["review_evidence"].__setitem__("method", "UNVERIFIED"))
    control("pdf-page-dimension", "PDF_PAGE_ROWS", lambda t, a: a["pdf_records"][0]["pages"][0].__setitem__("width_points", 1.0))
    control("pdf-variant-description", "PDF_VARIANT_RELATIONSHIPS", lambda t, a: a["pdf_variant_relationships"][0].__setitem__("direct_visual_difference", "mutated"))
    control("text-encoding", "TEXT_ENCODING_NEWLINE", lambda t, a: a["release_text_records"][0].__setitem__("newline_style", "CRLF"))
    control("snapshot-independent-traversal", "SNAPSHOT_INDEPENDENT_TRAVERSAL", lambda t, a: next(x for x in a["release_text_records"] if x.get("strict_json_traversal"))["strict_json_traversal"].__setitem__("max_depth", -1))

    failures: list[str] = []
    for name, expected, mutation in controls:
        mutated_top, mutated_att = copy.deepcopy(top), copy.deepcopy(att)
        expected_top, expected_att = copy.deepcopy(top), copy.deepcopy(att)
        mutation(mutated_top, mutated_att)
        mutation(expected_top, expected_att)
        if expected == "SOURCE_GIT_IDENTITY":
            refresh_source_derivatives(mutated_top, mutated_att)
            refresh_source_derivatives(expected_top, expected_att)
        if expected != "HUMAN_REVIEW_HASH":
            refresh_human_hashes(mutated_att); refresh_human_hashes(expected_att)
        linked(mutated_top, mutated_att); linked(expected_top, expected_att)
        observed = semantic_diagnostics(mutated_top, mutated_att, expected_top, expected_att, git_check=False)
        if observed != {expected}:
            failures.append(f"{name}: expected={expected} observed={','.join(sorted(observed)) or 'NONE'}")
    strict_cases = (
        ("duplicate-key", b'{"a":1,"a":2}'),
        ("nan", b'{"a":NaN}'),
        ("positive-overflow", b'{"a":1e999}'),
        ("negative-overflow", b'{"a":-1e999}'),
    )
    for name, payload in strict_cases:
        try:
            strict_json_bytes(payload)
        except (DuplicateKeyError, NonFiniteNumberError, ValueError):
            continue
        failures.append(f"{name}: expected=STRICT_JSON_REJECTION observed=NONE")
    return len(controls) + len(strict_cases), failures


def builder_policy() -> set[str]:
    errors: set[str] = set()
    data = normalize_lf(BUILDER.read_bytes())
    add_if(errors, digest(data) != BUILDER_SHA256, "BUILDER_HASH")
    try:
        tree = ast.parse(data.decode("utf-8"), filename=str(BUILDER))
    except SyntaxError:
        return {"BUILDER_AST_POLICY"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("Claude"):
            errors.add("BUILDER_AST_POLICY")
        if isinstance(node, ast.Import) and any(alias.name.startswith("Claude") for alias in node.names):
            errors.add("BUILDER_AST_POLICY")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
            errors.add("BUILDER_AST_POLICY")
    text = data.decode("utf-8")
    add_if(errors, "timeout=GIT_TIMEOUT" not in text or "git_blob(BASELINE" not in text, "BUILDER_READONLY_GIT_POLICY")
    for destructive in ("checkout", "reset", "clean", "commit", "push", "add", "rm"):
        if re.search(rf"git_(?:bytes|text)\([^\n]*[\"']{destructive}[\"']", text):
            errors.add("BUILDER_READONLY_GIT_POLICY")
    return errors


def parse_porcelain(raw: bytes) -> set[str]:
    paths: set[str] = set()
    for item in raw.split(b"\0"):
        if not item:
            continue
        text = item.decode("utf-8", errors="strict")
        path = text[3:].replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.add(path)
    return paths


def markdown_section(text: str, heading: str) -> str:
    match = re.search(rf"(?m)^{re.escape(heading)}\s*$", text)
    if not match:
        return ""
    start = match.end()
    following = re.search(r"(?m)^##\s+", text[start:])
    return text[start:start + following.start()] if following else text[start:]


def markdown_table_rows(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", line) is not None:
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows[1:] if rows else []


def row_has_conflicting_terminal(row: list[str]) -> bool:
    return any(re.search(r"\b(?:FAIL|BLOCKED|CONDITIONAL)\b", cell) is not None for cell in row)


def current_markdown_documents() -> tuple[dict[Path, str], set[str]]:
    documents: dict[Path, str] = {}
    errors: set[str] = set()
    for path, code in ((RESULT, "RESULT_CONTRACT"), (ACTIVE_LEDGER, "ACTIVE_LEDGER_CONTRACT"), (PARENT_LEDGER, "PARENT_LEDGER_CONTRACT"), (HANDOVER, "HANDOVER_CONTRACT")):
        if not path.exists():
            errors.add(code + "_MISSING")
        else:
            documents[path] = normalize_lf(path.read_bytes()).decode("utf-8")
    return documents, errors


def markdown_diagnostics(documents: dict[Path, str]) -> set[str]:
    errors: set[str] = set()
    result = documents.get(RESULT, "")
    result_section = markdown_section(result, "## Exact Eight Files")
    expected_eight = [f"{index}. `{path}`" for index, path in enumerate(EXACT_EIGHT, 1)]
    result_contract = (
        result.splitlines()[:1] == ["# Phase 062 Step 52 v1.0.21 Source/Process Topology and Full-read Attestation Result"]
        and result.splitlines().count("상태: `PASS_WITH_CONCERNS`") == 1
        and result.splitlines().count("Gate: `PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY`") == 1
        and all(result.count(heading) == 1 for heading in (
            "## Recovery and Activation Persistence", "## Machine Artifacts and Validation",
            "## Exact Eight Files", "## Protected Non-changes", "## Exact Commit Boundary and Next Condition",
        ))
        and [line for line in result_section.splitlines() if re.match(r"^\d+\. `", line)] == expected_eight
        and result.count(SUBJECT) == 1
        and result.count(f"Expected parent is `{ACTIVATION}`.") == 1
        and result.count("Containing commit is `PENDING_AT_PRECOMMIT_BY_DESIGN`.") == 1
        and result.count("Only after `PASS_P062_STEP52_PERSISTENCE` may Step 53 begin.") == 1
        and "68 / 68 / 68" in result and "5 / 214" in result and "10,425" in result
    )
    if not result_contract:
        errors.add("RESULT_CONTRACT")

    active = documents.get(ACTIVE_LEDGER, "")
    active_phase_rows = [row for row in markdown_table_rows(markdown_section(active, "## Execution Ledger")) if row and row[0] == "062"]
    active_commit_rows = [row for row in markdown_table_rows(markdown_section(active, "## Commit and Push Ledger")) if row and row[0] == "Step 52"]
    active_contract = (
        active.splitlines()[:1] == ["# Phase 059–090 Canonical Completion Execution Ledger"]
        and len(active_phase_rows) == 1 and len(active_phase_rows[0]) == 10
        and active_phase_rows[0][1:5] == ["52–57", "plan activation; Step 52 precommit complete; Steps 53–57.2 pending", "v1.0.21 reaudit", "IN_PROGRESS"]
        and all(token in active_phase_rows[0][8] for token in ("PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY", "PENDING_AT_PRECOMMIT_BY_DESIGN", "PASS_P062_LINEAGE_E"))
        and all(token in active_phase_rows[0][9] for token in ("PASS_P062_STEP52_PERSISTENCE", "Step 53"))
        and not row_has_conflicting_terminal(active_phase_rows[0])
        and len(active_commit_rows) == 1 and len(active_commit_rows[0]) == 6
        and active_commit_rows[0][2:5] == ["`PENDING_AT_PRECOMMIT_BY_DESIGN`", "exact-eight checkpoint prepared", "verify after atomic commit"]
        and all(token in active_commit_rows[0][5] for token in (SUBJECT, ACTIVATION, "release 68/68", "PDF 5/214", "Step 53 blocked until `PASS_P062_STEP52_PERSISTENCE`"))
        and not row_has_conflicting_terminal(active_commit_rows[0])
        and all(token in markdown_section(active, "## Next Exact Step") for token in (SUBJECT, ACTIVATION, "exact-eight", "PASS_P062_STEP52_PERSISTENCE", "Step 53"))
    )
    if not active_contract:
        errors.add("ACTIVE_LEDGER_CONTRACT")

    parent = documents.get(PARENT_LEDGER, "")
    parent_rows = [row for row in markdown_table_rows(markdown_section(parent, "## Ledger")) if row and row[0] == "062"]
    parent_contract = (
        parent.splitlines()[:1] == ["# Phase 055–069 전체 계보 재감사 실행 원장"]
        and len(parent_rows) == 1 and len(parent_rows[0]) == 12
        and parent_rows[0][1:7] == ["52–57", "plan activation; Step 52 precommit complete; Steps 53–57.2 pending", "lineage E", "v1.0.21 재감사", "IN_PROGRESS", "`Codex/plans/2026-08-27-phase062-v1021-lineage-detailed-plan.md`"]
        and all(token in parent_rows[0][9] for token in ("PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY", "PENDING_AT_PRECOMMIT_BY_DESIGN", "release 68/68", "PDF 5·214"))
        and parent_rows[0][10] == "`PASS_P062_LINEAGE_E` pending"
        and all(token in parent_rows[0][11] for token in ("PASS_P062_STEP52_PERSISTENCE", "Step 53"))
        and not row_has_conflicting_terminal(parent_rows[0])
    )
    if not parent_contract:
        errors.add("PARENT_LEDGER_CONTRACT")

    handover = documents.get(HANDOVER, "")
    handover_rows = [row for row in markdown_table_rows(markdown_section(handover, "## Handover Chain")) if row and row[0] == "Phase 062 Step 52"]
    handover_contract = (
        handover.splitlines()[:1] == ["# Project Anode Fit Canonical Completion Active Handover"]
        and len(handover_rows) == 1 and len(handover_rows[0]) == 4
        and handover_rows[0][1] == "Step 52"
        and all(token in handover_rows[0][2] for token in ("PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY", "PENDING_AT_PRECOMMIT_BY_DESIGN", "release 68/68", "PDF 5·214"))
        and all(token in handover_rows[0][3] for token in ("PASS_P062_STEP52_PERSISTENCE", "Step 53"))
        and not row_has_conflicting_terminal(handover_rows[0])
        and handover.count("Phase 062 Step 52 `PASS_WITH_CONCERNS`") == 1
        and handover.count("Step 52 containing commit은 `PENDING_AT_PRECOMMIT_BY_DESIGN`") == 1
        and all(token in markdown_section(handover, "## Exact Next Action") for token in (SUBJECT, ACTIVATION, "declared eight files", "PASS_P062_STEP52_PERSISTENCE", "Step 53"))
    )
    if not handover_contract:
        errors.add("HANDOVER_CONTRACT")

    for path, code in ((RESULT, "RESULT_CONTRACT"), (ACTIVE_LEDGER, "ACTIVE_LEDGER_CONTRACT"), (PARENT_LEDGER, "PARENT_LEDGER_CONTRACT"), (HANDOVER, "HANDOVER_CONTRACT")):
        if re.search(r"(?im)^\s*(?:Gate|Status|Overall Gate)\s*[:=]\s*(?:FAIL|BLOCKED|CONDITIONAL)\b", documents.get(path, "")):
            errors.add(code)
    return errors


def markdown_contract(errors: set[str]) -> None:
    documents, read_errors = current_markdown_documents()
    errors |= read_errors
    errors |= markdown_diagnostics(documents)


def markdown_negative_controls() -> tuple[int, list[str]]:
    documents, read_errors = current_markdown_documents()
    if read_errors:
        return 0, ["missing-current-documents:" + ",".join(sorted(read_errors))]
    token_fixture = f"example-only token list: Step 52 PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY PENDING_AT_PRECOMMIT_BY_DESIGN {SUBJECT} {ACTIVATION} PASS_P062_STEP52_PERSISTENCE Step 53 release 68/68 PDF 5/214 snapshot 9"
    fixtures: list[tuple[str, str, Path, Callable[[str], str]]] = [
        ("result-token-only", "RESULT_CONTRACT", RESULT, lambda text: token_fixture),
        ("active-token-only", "ACTIVE_LEDGER_CONTRACT", ACTIVE_LEDGER, lambda text: token_fixture),
        ("parent-token-only", "PARENT_LEDGER_CONTRACT", PARENT_LEDGER, lambda text: token_fixture),
        ("handover-token-only", "HANDOVER_CONTRACT", HANDOVER, lambda text: token_fixture),
        ("result-status", "RESULT_CONTRACT", RESULT, lambda text: text.replace("상태: `PASS_WITH_CONCERNS`", "상태: `PASS`", 1)),
        ("active-duplicate-row", "ACTIVE_LEDGER_CONTRACT", ACTIVE_LEDGER, lambda text: re.sub(r"(?m)^(\| 062 \|.*)$", r"\1\n\1", text, count=1)),
        ("parent-duplicate-row", "PARENT_LEDGER_CONTRACT", PARENT_LEDGER, lambda text: re.sub(r"(?m)^(\| 062 \|.*)$", r"\1\n\1", text, count=1)),
        ("handover-next-action", "HANDOVER_CONTRACT", HANDOVER, lambda text: text.replace("## Exact Next Action", "## Example Next Action", 1)),
        ("active-conflicting-outcome", "ACTIVE_LEDGER_CONTRACT", ACTIVE_LEDGER, lambda text: text.replace("`PASS_P062_LINEAGE_E` pending | Step 52 exact-eight", "`PASS_P062_LINEAGE_E` pending FAIL | Step 52 exact-eight", 1)),
        ("parent-conflicting-outcome", "PARENT_LEDGER_CONTRACT", PARENT_LEDGER, lambda text: text.replace("`PASS_P062_LINEAGE_E` pending | Step 52 exact-eight", "`PASS_P062_LINEAGE_E` pending FAIL | Step 52 exact-eight", 1)),
        ("handover-conflicting-outcome", "HANDOVER_CONTRACT", HANDOVER, lambda text: text.replace("snapshot 9·10,425 nodes | commit/push", "snapshot 9·10,425 nodes FAIL | commit/push", 1)),
    ]
    failures: list[str] = []
    for name, expected, path, mutation in fixtures:
        mutated = dict(documents)
        mutated[path] = mutation(mutated[path])
        observed = markdown_diagnostics(mutated)
        if observed != {expected}:
            failures.append(f"{name}: expected={expected} observed={','.join(sorted(observed)) or 'NONE'}")
    return len(fixtures), failures


def repository_diagnostics(mode: str, expected_commit: str | None) -> set[str]:
    errors: set[str] = set()
    add_if(errors, git_text("branch", "--show-current") != BRANCH, "BRANCH")
    try:
        add_if(errors, git_text("rev-parse", PROTECTED_REF) != PROTECTED_TIP, "PROTECTED_TIP")
        add_if(errors, git_text("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2") != PROTECTED_TIP, "PROTECTED_TRACKING_TIP")
        add_if(errors, git_text("rev-parse", MAIN_REF) != MAIN_TIP, "MAIN_TIP")
    except Exception:
        errors.add("PROTECTED_REF_READ")
    tracked_claude = [row for row in git_text("diff", "--name-only", ACTIVATION, "--", "Claude").splitlines() if row]
    untracked_claude = [path for path in parse_porcelain(git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all", "--", "Claude"))]
    add_if(errors, bool(tracked_claude or untracked_claude), "CLAUDE_DRIFT")
    if mode in {"content", "staged"}:
        dirty = parse_porcelain(git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all"))
        add_if(errors, dirty != set(EXACT_EIGHT), "EXACT_EIGHT_DIRT")
    if mode == "staged":
        staged = {row for row in git_bytes("diff", "--cached", "--name-only", "-z").decode("utf-8").split("\0") if row}
        add_if(errors, staged != set(EXACT_EIGHT), "EXACT_EIGHT_STAGED")
        for path in EXACT_EIGHT:
            work = (REPO / path).read_bytes()
            try:
                index = git_bytes("show", f":{path}")
            except Exception:
                errors.add("STAGED_WORKTREE_IDENTITY")
                continue
            add_if(errors, work != index, "STAGED_WORKTREE_IDENTITY")
        add_if(errors, git_text("rev-parse", "HEAD") != ACTIVATION, "EXPECTED_PARENT")
    if mode == "persistence":
        if not expected_commit or not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
            errors.add("EXPECTED_COMMIT_REQUIRED")
            return errors
        add_if(errors, git_text("rev-parse", "HEAD") != expected_commit, "PERSISTENCE_HEAD")
        add_if(errors, git_text("show", "-s", "--format=%P", expected_commit) != ACTIVATION, "PERSISTENCE_PARENT")
        add_if(errors, git_text("show", "-s", "--format=%s", expected_commit) != SUBJECT, "PERSISTENCE_SUBJECT")
        committed = {row for row in git_bytes("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", expected_commit).decode("utf-8").split("\0") if row}
        add_if(errors, committed != set(EXACT_EIGHT), "PERSISTENCE_PATHS")
        add_if(errors, bool(git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all")), "PERSISTENCE_DIRTY")
        upstream = git_text("rev-parse", "@{upstream}")
        add_if(errors, upstream != expected_commit, "PERSISTENCE_UPSTREAM")
        try:
            remote_rows = git_text(
                "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}",
                "refs/heads/codex/lib-physics-endgame-v1025_2", "refs/heads/main",
            ).splitlines()
            remote_heads = {
                fields[1]: fields[0]
                for row in remote_rows
                if len(fields := row.split()) == 2
            }
            add_if(errors, remote_heads.get(f"refs/heads/{BRANCH}") != expected_commit, "PERSISTENCE_LIVE_REMOTE")
            add_if(errors, remote_heads.get("refs/heads/codex/lib-physics-endgame-v1025_2") != PROTECTED_TIP, "PERSISTENCE_LIVE_PROTECTED")
            add_if(errors, remote_heads.get("refs/heads/main") != MAIN_TIP, "PERSISTENCE_LIVE_MAIN")
        except Exception:
            errors.add("PERSISTENCE_LIVE_REMOTE_READ")
    return errors


def missing_artifacts() -> list[Path]:
    return [path for path in (TOPOLOGY, ATTESTATION) if not path.exists()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    missing = missing_artifacts()
    if missing:
        for path in missing:
            print(f"FAIL STEP52_MISSING_ARTIFACT {path.relative_to(REPO).as_posix()}")
        print(f"FAIL_P062_STEP52_PROCESS_SOURCE_TOPOLOGY missing={len(missing)}")
        return 1
    try:
        top, top_stats = read_artifact(TOPOLOGY)
        att, att_stats = read_artifact(ATTESTATION)
        rebuilt_top, rebuilt_att, first_top_bytes, first_att_bytes = rebuild()
        errors = builder_policy()
        errors |= semantic_diagnostics(top, att, rebuilt_top, rebuilt_att)
        if args.determinism_check:
            second_top, second_att, second_top_bytes, second_att_bytes = rebuild()
            if canonical(rebuilt_top) != canonical(second_top) or canonical(rebuilt_att) != canonical(second_att) or first_top_bytes != second_top_bytes or first_att_bytes != second_att_bytes:
                errors.add("DETERMINISM")
            else:
                print("PASS_P062_STEP52_DETERMINISM 2/2")
        if args.run_negative_probes:
            count, failures = negative_controls(top, att)
            if failures:
                errors.add("NEGATIVE_CONTROLS")
                for failure in failures:
                    print("FAIL NEGATIVE " + failure)
            else:
                print(f"PASS_P062_STEP52_NEGATIVE_CONTROLS {count}/{count}")
            markdown_count, markdown_failures = markdown_negative_controls()
            if markdown_failures:
                errors.add("MARKDOWN_NEGATIVE_CONTROLS")
                for failure in markdown_failures:
                    print("FAIL MARKDOWN_NEGATIVE " + failure)
            else:
                print(f"PASS_P062_STEP52_MARKDOWN_NEGATIVE_CONTROLS {markdown_count}/{markdown_count}")
        if not args.content_only:
            markdown_contract(errors)
            mode = "persistence" if args.verify_persistence else "staged" if args.verify_staged else "content"
            errors |= repository_diagnostics(mode, args.expected_commit)
        if errors:
            for code in sorted(errors):
                print(f"FAIL {code}")
            print(f"FAIL_P062_STEP52_PROCESS_SOURCE_TOPOLOGY diagnostics={len(errors)}")
            return 1
        print(f"PASS_P062_STEP52_JSON_TRAVERSAL topology={top_stats['nodes'] + top_stats['mapping_keys']} attestation={att_stats['nodes'] + att_stats['mapping_keys']}")
        if args.verify_persistence:
            print("PASS_P062_STEP52_PERSISTENCE")
        else:
            print("PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY")
        return 0
    except (DuplicateKeyError, NonFiniteNumberError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"FAIL STRICT_JSON {type(exc).__name__}: {exc}")
    except (OSError, RuntimeError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL VALIDATOR_EXCEPTION {type(exc).__name__}: {exc}")
    print("FAIL_P062_STEP52_PROCESS_SOURCE_TOPOLOGY diagnostics=1")
    return 1


if __name__ == "__main__":
    sys.exit(main())
