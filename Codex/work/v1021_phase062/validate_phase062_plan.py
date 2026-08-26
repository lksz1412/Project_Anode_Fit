#!/usr/bin/env python3
"""Validate the Phase 062 detailed-plan activation and Git checkpoint."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
PLAN = REPO / "Codex/plans/2026-08-27-phase062-v1021-lineage-detailed-plan.md"
VALIDATOR = REPO / "Codex/work/v1021_phase062/validate_phase062_plan.py"
OUTPUT = REPO / "Codex/results/PHASE_062_PLAN_ACTIVATION_VALIDATION.json"
RESULT = REPO / "Codex/results/PHASE_062_PLAN_ACTIVATION_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
DISPOSITION = REPO / "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json"
CARRY = REPO / "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "86b4acbf9ed41ae12bd5ae95c4d2a5c2adb0dfe2"
EXPECTED_SUBJECT = "docs(phase062): plan v1021 lineage reaudit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EXPECTED_PLAN_SHA256 = "e393e488c374cbaba90bdcd2bc5fe74f90a8ca08c2266ec5a2b424a6f7816db4"
EXPECTED_MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
SUPPLEMENTAL_PATH = "Claude/plans/2026-07-16-v1021-master-plan.md"
SUPPLEMENTAL_BLOB = "de26c03b53bedbe1cc4363bb07f66e9ca9da77f7"
EXPECTED_BLOCKER_SHA256 = "5b3a03166d5e9a6733920c12cad187999f043160e9fc551e68fb04f7f5918e35"
EXPECTED_TARGET62_ID_SHA256 = "68267522dbda5c3a47fccfaad0babb2617331f2208831f36f91ec2ea284f11a5"
EXPECTED_DEBT_IDENTITY_SHA256 = "d373830b0f9e2dbea982f2ee50ac8153985b2d7e7889c0ab5dba8e457cb1807d"
EXPECTED_BLOCKER_DEBT_ID_SHA256 = "e3d9f0e1e91b98eccf8f248dc934db701792f72d90cfa65996ca53f72de544a0"
EXPECTED_TARGET62_FULL_SHA256 = "91b4c9c04e6419e23dfa40dc32ec21ac876d2b756866ce5bf5ba4343b6bdca79"
EXPECTED_INHERITED52_FULL_SHA256 = "a732fca7fd937977bd98521a22ff9cc8631041c8e4f1359ae7a56a243555bc28"
EXPECTED_INHERITED_BLOCKER5_FULL_SHA256 = "92558bb8c0383184c296054a20597d35237e231aec3f2bdbe4906edbaf6b4c23"
EXPECTED_NEW_BLOCKER5_FULL_SHA256 = "836d9c05a379b1d101344068173f388a8fa2ffdb498c61d3cc5d524a13dc61e0"
EXPECTED_MANIFEST_OBJECT_SHA256 = "3829bb24881e84cbf97ac5ad9d3fad55f9befec0bc4743b3300448330518e777"
GIT_TIMEOUT = 60

EXACT_SEVEN = [
    "Codex/plans/2026-08-27-phase062-v1021-lineage-detailed-plan.md",
    "Codex/work/v1021_phase062/validate_phase062_plan.py",
    "Codex/results/PHASE_062_PLAN_ACTIVATION_VALIDATION.json",
    "Codex/results/PHASE_062_PLAN_ACTIVATION_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]
EXACT_SEVEN_SET = set(EXACT_SEVEN)
NONSELF_SURFACES = [path for path in EXACT_SEVEN if path != OUTPUT.relative_to(REPO).as_posix()]

MANIFEST_TOP_KEYS = {
    "schema_version", "generated_date", "baseline_commit", "version_scope",
    "path_count", "unique_blob_count", "counts", "validation", "entries",
}
ENTRY_BASE_KEYS = {
    "path", "version", "blob_sha", "dedup_group", "git_mode", "size_bytes",
    "extension", "role", "review_mode", "extent",
}
DISPOSITION_TOP_KEYS = {
    "artifact_kind", "authority_boundary", "baseline_commit", "dispositions",
    "gate_summary", "generation", "input_artifact_commit", "inputs", "phase",
    "schema_version", "source_commit", "source_manifest_sha256", "step",
}
CARRY_TOP_KEYS = {
    "artifact_kind", "authority_boundary", "baseline_commit", "debt_routing",
    "gate_summary", "generation", "inherited_carry_items",
    "inherited_phase060_blockers", "input_artifact_commit", "inputs",
    "new_blockers", "phase", "schema_version", "source_commit", "step",
}

SECTIONS = [
    "## Summary", "## Current Ground Truth", "## Phase Range", "## Exact Read Inputs",
    "## Non-goals and Scope Guards", "## Implementation Changes",
    "## Plan Activation Unit — Save Before Step 52", "## Phase 062 — v1.0.21 Reaudit",
    "## Phase Gate", "## Implementation Interfaces", "## Test and Validation Plan",
    "## Stop Conditions", "## Assumptions", "## Correction History",
]
STEP_PREFIXES = [
    "### Step 52 ", "### Step 53 ", "### Step 54 ", "### Step 55 ",
    "### Step 56 ", "### Step 57.1 ", "### Step 57.2 ",
]
SUBJECTS = [
    EXPECTED_SUBJECT,
    "audit(phase062): freeze v1021 source process topology",
    "audit(phase062): rederive v1021 statmech tst",
    "audit(phase062): bound v1021 lco si scope",
    "audit(phase062): compare v1021 code runtime",
    "audit(phase062): adjudicate v1021 physics closure",
    "audit(phase062): disposition v1021 lineage",
    "audit(phase062): close v1021 lineage gate",
]
GATES = [
    "PASS_P062_PLAN_ACTIVATION", "PASS_P062_PLAN_ACTIVATION_PERSISTENCE",
    "PASS_P062_STEP52_PROCESS_SOURCE_TOPOLOGY", "PASS_P062_STEP52_PERSISTENCE",
    "PASS_P062_STEP53_STATMECH_TST_REDERIVATION", "PASS_P062_STEP54_LCO_SI_SCOPE",
    "PASS_P062_STEP55_CODE_RUNTIME_DELTA", "PASS_P062_STEP56_PHYSICS_CLOSURE",
    "PASS_P062_STEP57_1_DISPOSITIONS", "PASS_P062_STEP53_PERSISTENCE",
    "PASS_P062_STEP54_PERSISTENCE", "PASS_P062_STEP55_PERSISTENCE",
    "PASS_P062_STEP56_PERSISTENCE", "PASS_P062_STEP57_1_PERSISTENCE",
    "PASS_P062_STEP57_2_PERSISTENCE", "PASS_P062_LINEAGE_E", "CONDITIONAL_P062", "FAIL_P062",
]
DECLARED_OUTPUTS = [
    *EXACT_SEVEN,
    "Codex/work/v1021_phase062/build_phase062_step52_source_process_topology.py",
    "Codex/work/v1021_phase062/validate_phase062_step52.py",
    "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json",
    "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json",
    "Codex/results/PHASE_062_STEP_052_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
    "Codex/work/v1021_phase062/build_phase062_step53_statmech_tst.py",
    "Codex/work/v1021_phase062/validate_phase062_step53.py",
    "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json",
    "Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md",
    "Codex/work/v1021_phase062/build_phase062_step54_lco_si_scope.py",
    "Codex/work/v1021_phase062/validate_phase062_step54.py",
    "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json",
    "Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md",
    "Codex/work/v1021_phase062/build_phase062_step55_code_runtime_delta.py",
    "Codex/work/v1021_phase062/validate_phase062_step55.py",
    "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json",
    "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md",
    "Codex/work/v1021_phase062/build_phase062_step56_physics_closure.py",
    "Codex/work/v1021_phase062/validate_phase062_step56.py",
    "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json",
    "Codex/results/PHASE_062_STEP_056_PHYSICS_CLOSURE_RESULT.md",
    "Codex/work/v1021_phase062/build_phase062_step57_dispositions.py",
    "Codex/work/v1021_phase062/validate_phase062_step57_dispositions.py",
    "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json",
    "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json",
    "Codex/results/PHASE_062_STEP_057_1_DISPOSITION_RESULT.md",
    "Codex/work/v1021_phase062/validate_phase062_final.py",
    "Codex/results/PHASE_062_VALIDATION.json",
    "Codex/results/PHASE_062_V1021_LINEAGE_REPORT_E.md",
    "Codex/results/PHASE_062_STEP_057_2_GATE_RESULT.md",
    "Codex/results/PHASE_062_RESULT.md",
]
PHASE057_INPUTS = [
    ("Codex/plans/2026-07-28-phase057-v1021-read-map.md", 85),
    ("Codex/results/PHASE_057J_V1021_CONTROL_DOCUMENT_INTENT_OBSERVATIONS.md", 197),
    ("Codex/results/PHASE_057K_V1021_Q0_BASELINE_OBSERVATIONS.md", 79),
    ("Codex/results/PHASE_057L_V1021_Q2_Q3_SNAPSHOT_OBSERVATIONS.md", 126),
    ("Codex/results/PHASE_057M_V1021_Q4_Q5NAV_SNAPSHOT_OBSERVATIONS.md", 97),
    ("Codex/results/PHASE_057N_V1021_Q5_Q5B_SNAPSHOT_OBSERVATIONS.md", 101),
    ("Codex/results/PHASE_057O_V1021_Q6_Q7_AND_VERSION_CLOSE_OBSERVATIONS.md", 134),
]


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


class GitCommandError(RuntimeError):
    pass


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


def walk_json(value: Any, path: str = "$", stats: dict[str, int] | None = None) -> dict[str, int]:
    if stats is None:
        stats = {"nodes": 0, "max_depth": 0, "objects": 0, "arrays": 0, "scalars": 0}
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], path.count(".") + path.count("["))
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(path)
    if isinstance(value, dict):
        stats["objects"] += 1
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(f"non-string JSON key at {path}")
            walk_json(child, f"{path}.{key}", stats)
    elif isinstance(value, list):
        stats["arrays"] += 1
        for index, child in enumerate(value):
            walk_json(child, f"{path}[{index}]", stats)
    elif value is None or isinstance(value, (str, int, float, bool)):
        stats["scalars"] += 1
    else:
        raise TypeError(f"unsupported JSON type at {path}: {type(value).__name__}")
    return stats


def strict_load_bytes(data: bytes) -> tuple[Any, dict[str, int]]:
    value = json.loads(
        data.decode("utf-8"), object_pairs_hook=strict_pairs,
        parse_constant=reject_constant, parse_float=strict_float,
    )
    return value, walk_json(value)


def strict_load(path: Path) -> tuple[Any, dict[str, int]]:
    return strict_load_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_lf_bytes(path: Path) -> bytes:
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def eol_evidence(path: Path) -> tuple[bool, dict[str, Any]]:
    raw = path.read_bytes()
    raw.decode("utf-8")
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n")
    bare_cr = raw.replace(b"\r\n", b"").count(b"\r")
    normalized = normalized_lf_bytes(path)
    return bare_cr == 0 and not (crlf and lf != crlf), {
        "utf8": True, "eol": "CRLF" if crlf else "LF", "bare_cr": bare_cr,
        "normalized_bytes": len(normalized), "normalized_lines": len(normalized.decode("utf-8").splitlines()),
        "normalized_sha256": sha256_bytes(normalized),
    }


def run_git_bytes(*args: str, check: bool = True) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, timeout=GIT_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise GitCommandError(f"timeout: git {' '.join(args)}") from exc
    if check and proc.returncode != 0:
        error = proc.stderr.decode("utf-8", errors="replace").strip()
        raise GitCommandError(f"git {' '.join(args)} failed ({proc.returncode}): {error}")
    return proc.stdout


def run_git(*args: str, check: bool = True) -> str:
    return run_git_bytes(*args, check=check).decode("utf-8", errors="strict").strip()


def remote_tip(branch: str) -> str:
    row = run_git("ls-remote", "--heads", "origin", branch)
    parts = row.split()
    return parts[0] if len(parts) == 2 else ""


def git_blob(commit: str, path: str) -> tuple[str, str, bytes]:
    raw = run_git_bytes("ls-tree", "--full-tree", "-z", commit, "--", path)
    rows = [row for row in raw.split(b"\0") if row]
    if len(rows) != 1:
        raise FileNotFoundError(f"{commit}:{path}")
    metadata, actual_path = rows[0].split(b"\t", 1)
    if actual_path.decode("utf-8") != path:
        raise FileNotFoundError(f"path identity mismatch: {path}")
    mode, object_type, blob = metadata.decode("ascii").split()
    if object_type != "blob":
        raise TypeError(f"not a blob: {path}")
    return mode, blob, run_git_bytes("cat-file", "blob", blob)


def porcelain_paths() -> set[str]:
    raw = run_git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all")
    fields = raw.split(b"\0")
    paths: set[str] = set()
    index = 0
    while index < len(fields) and fields[index]:
        field = fields[index].decode("utf-8")
        status = field[:2]
        paths.add(field[3:].replace("\\", "/"))
        if "R" in status or "C" in status:
            index += 1
            if index < len(fields) and fields[index]:
                paths.add(fields[index].decode("utf-8").replace("\\", "/"))
        index += 1
    return paths


def nul_paths(*args: str) -> set[str]:
    return {row.decode("utf-8").replace("\\", "/") for row in run_git_bytes(*args).split(b"\0") if row}


def activation_dirty_paths(prospective_output: bool = False) -> set[str]:
    paths = porcelain_paths()
    for relative in EXACT_SEVEN:
        path = REPO / relative
        tracked = run_git("ls-files", "--error-unmatch", relative, check=False)
        if path.exists() and not tracked:
            paths.add(relative)
    if prospective_output:
        paths.add(OUTPUT.relative_to(REPO).as_posix())
    return paths


def record(checks: list[dict[str, Any]], code: str, passed: bool, evidence: Any) -> None:
    checks.append({"code": code, "passed": bool(passed), "evidence": evidence})


def selected_manifest_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    manifest, traversal = strict_load(MANIFEST)
    normalized_sha = sha256_bytes(normalized_lf_bytes(MANIFEST))
    record(checks, "MANIFEST_NORMALIZED_SHA", normalized_sha == EXPECTED_MANIFEST_SHA256, normalized_sha)
    record(checks, "MANIFEST_TOP_SCHEMA", set(manifest) == MANIFEST_TOP_KEYS, sorted(manifest))
    record(checks, "MANIFEST_BASELINE", manifest.get("baseline_commit") == BASELINE, manifest.get("baseline_commit"))
    entries = manifest.get("entries", [])
    record(checks, "MANIFEST_FULL_ROW_COUNT", manifest.get("path_count") == len(entries) == 1520, len(entries))
    schema_bad: list[dict[str, Any]] = []
    allowed_shapes = {frozenset(ENTRY_BASE_KEYS), frozenset(ENTRY_BASE_KEYS | {"candidate_tex_paths"})}
    extent_shapes = {
        "FULL_TEXT": {"lines", "encoding_check"},
        "FULL_PDF": {"pages", "encrypted"},
        "FULL_IMAGE": {"width", "height", "mode", "format", "frames"},
        "BINARY_INTROSPECTION": {"arrays"},
        "GENERATED_ONLY": {"bytes"},
    }
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or frozenset(entry) not in allowed_shapes:
            schema_bad.append({"index": index, "kind": "entry", "keys": sorted(entry) if isinstance(entry, dict) else type(entry).__name__})
            continue
        if set(entry.get("extent", {})) != extent_shapes.get(entry.get("review_mode"), set()):
            schema_bad.append({"index": index, "kind": "extent", "keys": sorted(entry.get("extent", {}))})
    record(checks, "MANIFEST_FULL_SCHEMA", not schema_bad, schema_bad)

    selected = [(index, entry) for index, entry in enumerate(entries, start=1) if entry.get("version") == "v1.0.21"]
    mismatches: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    nonblank = 0
    text_lines = 0
    pdf_pages = 0
    for index, entry in selected:
        try:
            mode, blob, data = git_blob(BASELINE, entry["path"])
        except Exception as exc:
            mismatches.append({"index": index, "path": entry.get("path"), "error": str(exc)})
            continue
        bad: list[str] = []
        if mode != entry["git_mode"]:
            bad.append("git_mode")
        if blob != entry["blob_sha"]:
            bad.append("blob_sha")
        if len(data) != entry["size_bytes"]:
            bad.append("size_bytes")
        extent = entry["extent"]
        if entry["review_mode"] == "FULL_TEXT":
            try:
                lines = data.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                lines = []
                bad.append("utf8")
            if len(lines) != extent["lines"]:
                bad.append("lines")
            text_lines += len(lines)
            nonblank += sum(bool(line.strip()) for line in lines)
        elif entry["review_mode"] == "FULL_PDF":
            pdf_pages += extent["pages"]
        if bad:
            mismatches.append({"index": index, "path": entry["path"], "fields": bad})
        records.append({
            "manifest_index": index, "path": entry["path"], "blob_sha1": blob,
            "git_mode": mode, "size_bytes": len(data), "extension": entry["extension"],
            "role": entry["role"], "review_mode": entry["review_mode"], "extent": extent,
            "sha256": sha256_bytes(data),
        })
    paths = [entry["path"] for _, entry in selected]
    blobs = [entry["blob_sha"] for _, entry in selected]
    groups: dict[str, list[str]] = defaultdict(list)
    for _, entry in selected:
        groups[entry["blob_sha"]].append(entry["path"])
    duplicates = [{"blob_sha1": blob, "paths": sorted(paths_)} for blob, paths_ in sorted(groups.items()) if len(paths_) > 1]
    summary = {
        "paths": len(selected), "unique_paths": len(set(paths)), "unique_blobs": len(set(blobs)),
        "total_bytes": sum(entry["size_bytes"] for _, entry in selected),
        "indices": [index for index, _ in selected],
        "mode_counts": dict(sorted(Counter(entry["review_mode"] for _, entry in selected).items())),
        "role_counts": dict(sorted(Counter(entry["role"] for _, entry in selected).items())),
        "extension_counts": dict(sorted(Counter(entry["extension"] for _, entry in selected).items())),
        "text_files": sum(entry["review_mode"] == "FULL_TEXT" for _, entry in selected),
        "text_lines": text_lines, "text_nonblank_lines": nonblank,
        "pdf_files": sum(entry["review_mode"] == "FULL_PDF" for _, entry in selected),
        "pdf_pages": pdf_pages, "duplicate_groups": duplicates,
    }
    expected = expected_manifest_summary()
    for code, key in manifest_summary_fields():
        record(checks, code, summary.get(key) == expected[key], {"actual": summary.get(key), "expected": expected[key]})
    record(checks, "V1021_GIT_IDENTITIES", not mismatches and len(records) == 68, mismatches)
    return {
        "path": MANIFEST.relative_to(REPO).as_posix(), "normalized_sha256": normalized_sha,
        "traversal": traversal, "summary": summary, "records": records,
        "path_set_sha256": sha256_bytes(("\n".join(sorted(paths)) + "\n").encode("utf-8")),
        "path_blob_set_sha256": sha256_bytes(("\n".join(f"{entry['path']}\t{entry['blob_sha']}" for _, entry in sorted(selected, key=lambda row: row[1]["path"])) + "\n").encode("utf-8")),
    }


def expected_manifest_summary() -> dict[str, Any]:
    return {
        "paths": 68, "unique_paths": 68, "unique_blobs": 68, "total_bytes": 4071795,
        "indices": list(range(472, 540)),
        "mode_counts": {"FULL_PDF": 5, "FULL_TEXT": 63},
        "role_counts": {"code": 1, "generated_document": 5, "implementation_guide": 1, "result": 15, "test": 1, "theory": 45},
        "extension_counts": {"json": 9, "md": 5, "pdf": 5, "py": 3, "tex": 46},
        "text_files": 63, "text_lines": 21048, "text_nonblank_lines": 20424,
        "pdf_files": 5, "pdf_pages": 214, "duplicate_groups": [],
    }


def manifest_summary_fields() -> list[tuple[str, str]]:
    return [
        ("MANIFEST_RELEASE_COUNT", "paths"), ("MANIFEST_UNIQUE_PATHS", "unique_paths"),
        ("MANIFEST_UNIQUE_BLOBS", "unique_blobs"), ("MANIFEST_TOTAL_BYTES", "total_bytes"),
        ("MANIFEST_INDEX_RANGE", "indices"), ("MANIFEST_MODE_COUNTS", "mode_counts"),
        ("MANIFEST_ROLE_COUNTS", "role_counts"), ("MANIFEST_EXTENSION_COUNTS", "extension_counts"),
        ("MANIFEST_TEXT_FILES", "text_files"), ("MANIFEST_TEXT_LINES", "text_lines"),
        ("MANIFEST_NONBLANK_LINES", "text_nonblank_lines"), ("MANIFEST_PDF_FILES", "pdf_files"),
        ("MANIFEST_PDF_PAGES", "pdf_pages"), ("MANIFEST_DUPLICATES", "duplicate_groups"),
    ]


def supplemental_contract(checks: list[dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    mode, blob, data = git_blob(BASELINE, SUPPLEMENTAL_PATH)
    lines = data.decode("utf-8").splitlines()
    summary = {
        "path": SUPPLEMENTAL_PATH, "manifest_member": any(row["path"] == SUPPLEMENTAL_PATH for row in manifest["records"]),
        "git_mode": mode, "blob_sha1": blob, "bytes": len(data), "lines": len(lines),
        "nonblank_lines": sum(bool(line.strip()) for line in lines), "sha256": sha256_bytes(data),
    }
    expected = {
        "path": SUPPLEMENTAL_PATH, "manifest_member": False, "git_mode": "100644",
        "blob_sha1": SUPPLEMENTAL_BLOB, "bytes": 10664, "lines": 76, "nonblank_lines": 59,
    }
    for code, key in [
        ("SUPPLEMENTAL_PATH", "path"), ("SUPPLEMENTAL_DENOMINATOR_SEPARATE", "manifest_member"),
        ("SUPPLEMENTAL_MODE", "git_mode"), ("SUPPLEMENTAL_BLOB", "blob_sha1"),
        ("SUPPLEMENTAL_BYTES", "bytes"), ("SUPPLEMENTAL_LINES", "lines"),
        ("SUPPLEMENTAL_NONBLANK", "nonblank_lines"),
    ]:
        record(checks, code, summary[key] == expected[key], {"actual": summary[key], "expected": expected[key]})
    return summary


def routing_contract(
    checks: list[dict[str, Any]],
    disposition_override: dict[str, Any] | None = None,
    carry_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if disposition_override is None:
        disposition, disp_traversal = strict_load(DISPOSITION)
    else:
        disposition = copy.deepcopy(disposition_override)
        disp_traversal = walk_json(disposition)
    if carry_override is None:
        carry, carry_traversal = strict_load(CARRY)
    else:
        carry = copy.deepcopy(carry_override)
        carry_traversal = walk_json(carry)
    record(checks, "DISPOSITION_TOP_SCHEMA", set(disposition) == DISPOSITION_TOP_KEYS, sorted(disposition))
    record(checks, "CARRY_TOP_SCHEMA", set(carry) == CARRY_TOP_KEYS, sorted(carry))
    rows = disposition.get("dispositions", [])
    target_rows = [row for row in rows if row.get("target_phase") == 62]
    inherited = carry.get("inherited_carry_items", [])
    blockers = carry.get("inherited_phase060_blockers", [])
    debt = carry.get("debt_routing", [])
    new_blockers = carry.get("new_blockers", [])
    blocker = next((row for row in new_blockers if row.get("blocker_id") == "P061-BD-NEW-001"), {})
    components = blocker.get("acceptance_components", [])
    target_ids = sorted(str(row.get("source_id")) for row in target_rows)
    carry_link_counts = Counter(link for row in target_rows for link in row.get("carry_forward_links", []))
    debt_projection_keys = [
        "debt_id", "origin_path", "origin_pointer", "origin_record_sha256",
        "primary_owner_type", "primary_owner_id", "owner_acceptance_criterion",
        "owner_target_phase", "origin_target_phase", "effective_target_phase",
        "route_state", "status", "duplicate_or_refinement_of",
    ]
    debt_projection = [
        {key: row.get(key) for key in debt_projection_keys}
        for row in sorted(debt, key=lambda item: item.get("debt_id", ""))
    ]
    effective_projection = {
        row.get("debt_id"): {
            "primary_owner_type": row.get("primary_owner_type"),
            "primary_owner_id": row.get("primary_owner_id"),
            "owner_target_phase": row.get("owner_target_phase"),
            "route_state": row.get("route_state"),
            "duplicate_or_refinement_of": row.get("duplicate_or_refinement_of"),
        }
        for row in debt if row.get("effective_target_phase") == 62
    }
    blocker_debt_ids = sorted(blocker.get("source_debt_ids", []))
    target_rows_sorted = sorted(target_rows, key=lambda item: item.get("source_id", ""))
    inherited_sorted = sorted(inherited, key=lambda item: item.get("carry_forward_id", ""))
    inherited_blockers_sorted = sorted(blockers, key=lambda item: item.get("blocker_id", ""))
    new_blockers_sorted = sorted(new_blockers, key=lambda item: item.get("blocker_id", ""))
    carry_external_promotions = sum(
        bool(row.get("external_scientific_truth")) or bool(row.get("external_material_truth"))
        for row in [*inherited, *blockers, *new_blockers]
    )
    summary = {
        "disposition_rows": len(rows), "target62_count": len(target_rows),
        "target62_dispositions": dict(sorted(Counter(row.get("disposition") for row in target_rows).items())),
        "target62_statuses": dict(sorted(Counter(row.get("status") for row in target_rows).items())),
        "target62_unique_sources": len({row.get("source_id") for row in target_rows}),
        "target62_id_set_sha256": sha256_bytes("\n".join(target_ids).encode("utf-8")),
        "target62_carry_link_counts": dict(sorted(carry_link_counts.items())),
        "target62_full_projection_sha256": sha256_bytes(canonical_bytes(target_rows_sorted)),
        "direct_inherited_target62": sum(row.get("target_phase_after") == 62 for row in inherited),
        "direct_blocker_target62": sum(row.get("target_phase_after") == 62 for row in blockers),
        "debt_rows": len(debt),
        "debt_origin_target62": sum(row.get("origin_target_phase") == 62 for row in debt),
        "debt_effective_target62": sum(row.get("effective_target_phase") == 62 for row in debt),
        "debt_identity_sha256": sha256_bytes(canonical_bytes(debt_projection)),
        "effective_debt_projection": effective_projection,
        "inherited52_full_projection_sha256": sha256_bytes(canonical_bytes(inherited_sorted)),
        "inherited_blocker5_full_projection_sha256": sha256_bytes(canonical_bytes(inherited_blockers_sorted)),
        "new_blocker5_full_projection_sha256": sha256_bytes(canonical_bytes(new_blockers_sorted)),
        "carry_external_promotion_count": carry_external_promotions,
        "component_ids": [row.get("component_id") for row in components],
        "component_targets": {row.get("component_id"): row.get("target_phase") for row in components},
        "component_statuses": {row.get("component_id"): row.get("status") for row in components},
        "parent_operator": blocker.get("closure_operator"), "parent_target": blocker.get("target_phase"),
        "parent_status": blocker.get("status"), "parent_sha256": sha256_bytes(canonical_bytes(blocker)) if blocker else None,
        "blocker_source_debt_ids": blocker_debt_ids,
        "blocker_source_debt_id_sha256": sha256_bytes("\n".join(blocker_debt_ids).encode("utf-8")),
        "external_promotion_count": sum(bool(row.get("external_scientific_truth")) or bool(row.get("external_material_truth")) for row in rows),
    }
    expected = expected_routing_summary()
    for code, key in routing_summary_fields():
        record(checks, code, summary.get(key) == expected[key], {"actual": summary.get(key), "expected": expected[key]})
    record(checks, "ROUTING_BASELINES", disposition.get("baseline_commit") == carry.get("baseline_commit") == BASELINE, {"disposition": disposition.get("baseline_commit"), "carry": carry.get("baseline_commit")})
    record(checks, "ROUTING_SOURCE_IDENTITIES", len(rows) == 232 and len({row.get("source_id") for row in rows}) == 232 and len({row.get("disposition_id") for row in rows}) == 232, len(rows))
    return {
        "disposition_path": DISPOSITION.relative_to(REPO).as_posix(), "carry_path": CARRY.relative_to(REPO).as_posix(),
        "disposition_traversal": disp_traversal, "carry_traversal": carry_traversal,
        "summary": summary,
    }


def expected_routing_summary() -> dict[str, Any]:
    return {
        "disposition_rows": 232, "target62_count": 149,
        "target62_dispositions": {"COMPETING_ONLY": 116, "CORRECT": 2, "PRESERVE": 28, "UNVERIFIED": 3},
        "target62_statuses": {"OPEN": 121, "PRESERVED_ACTIVE": 28}, "target62_unique_sources": 149,
        "target62_id_set_sha256": EXPECTED_TARGET62_ID_SHA256,
        "target62_carry_link_counts": {
            "P059-CFR-CF-08": 5, "P059-CFR-CF-11": 141,
            "P059-CFR-ED-03": 3, "P059-CFR-NS-05": 3,
            "P059-CFR-RB-11": 5, "P059-CFR-RB-12": 93,
            "P059-CFR-RM-011": 3,
        },
        "target62_full_projection_sha256": EXPECTED_TARGET62_FULL_SHA256,
        "direct_inherited_target62": 0, "direct_blocker_target62": 0, "debt_rows": 91,
        "debt_origin_target62": 15, "debt_effective_target62": 4,
        "debt_identity_sha256": EXPECTED_DEBT_IDENTITY_SHA256,
        "effective_debt_projection": {
            "P061-GNF-004": {
                "primary_owner_type": "SOURCE_DISPOSITION", "primary_owner_id": "P061-DISP-0044",
                "owner_target_phase": 62, "route_state": "OPEN", "duplicate_or_refinement_of": None,
            },
            "P061-STEP48-GNF-005": {
                "primary_owner_type": "SOURCE_DISPOSITION", "primary_owner_id": "P061-DISP-0044",
                "owner_target_phase": 62, "route_state": "OPEN_DUPLICATE_ALIAS", "duplicate_or_refinement_of": "P061-GNF-004",
            },
            "P061-STEP48-UNV-008": {
                "primary_owner_type": "SOURCE_DISPOSITION", "primary_owner_id": "P061-DISP-0044",
                "owner_target_phase": 62, "route_state": "OPEN_DUPLICATE_ALIAS", "duplicate_or_refinement_of": "P061-GNF-004",
            },
            "P061-UNV-008": {
                "primary_owner_type": "SOURCE_DISPOSITION", "primary_owner_id": "P061-DISP-0044",
                "owner_target_phase": 62, "route_state": "OPEN_DUPLICATE_ALIAS", "duplicate_or_refinement_of": "P061-GNF-004",
            },
        },
        "inherited52_full_projection_sha256": EXPECTED_INHERITED52_FULL_SHA256,
        "inherited_blocker5_full_projection_sha256": EXPECTED_INHERITED_BLOCKER5_FULL_SHA256,
        "new_blocker5_full_projection_sha256": EXPECTED_NEW_BLOCKER5_FULL_SHA256,
        "carry_external_promotion_count": 0,
        "component_ids": ["A01", "A02", "A03", "A04", "A05", "A06", "A07"],
        "component_targets": {"A01": 62, "A02": 62, "A03": 62, "A04": 62, "A05": 62, "A06": 82, "A07": 82},
        "component_statuses": {"A01": "OPEN", "A02": "OPEN", "A03": "OPEN", "A04": "OPEN", "A05": "OPEN", "A06": "OPEN", "A07": "OPEN"},
        "parent_operator": "ALL_OF", "parent_target": 82, "parent_status": "OPEN",
        "blocker_source_debt_ids": [
            "P061-GNF-005", "P061-GNF-006", "P061-STEP50-GNF-001",
            "P061-STEP50-GNF-002", "P061-STEP50-GNF-008",
            "P061-STEP50-GNF-009", "P061-STEP50-GNF-011",
            "P061-STEP50-UNV-004", "P061-UNV-007", "P061-UNV-009", "P061-UNV-010",
        ],
        "blocker_source_debt_id_sha256": EXPECTED_BLOCKER_DEBT_ID_SHA256,
        "parent_sha256": EXPECTED_BLOCKER_SHA256, "external_promotion_count": 0,
    }


def routing_summary_fields() -> list[tuple[str, str]]:
    return [
        ("ROUTING_DISPOSITION_ROWS", "disposition_rows"), ("ROUTING_TARGET62_COUNT", "target62_count"),
        ("ROUTING_TARGET62_DISTRIBUTION", "target62_dispositions"), ("ROUTING_TARGET62_STATUS", "target62_statuses"),
        ("ROUTING_TARGET62_IDENTITY", "target62_unique_sources"), ("ROUTING_INHERITED_DIRECT_ZERO", "direct_inherited_target62"),
        ("ROUTING_TARGET62_ID_SET", "target62_id_set_sha256"), ("ROUTING_TARGET62_CARRY_LINKS", "target62_carry_link_counts"),
        ("ROUTING_TARGET62_FULL_BIJECTION", "target62_full_projection_sha256"),
        ("ROUTING_BLOCKER_DIRECT_ZERO", "direct_blocker_target62"), ("ROUTING_DEBT_ROWS", "debt_rows"),
        ("ROUTING_DEBT_ORIGIN62", "debt_origin_target62"), ("ROUTING_DEBT_EFFECTIVE62", "debt_effective_target62"),
        ("ROUTING_DEBT_IDENTITY", "debt_identity_sha256"), ("ROUTING_DEBT_ALIAS_OWNER", "effective_debt_projection"),
        ("ROUTING_INHERITED52_FULL_BIJECTION", "inherited52_full_projection_sha256"),
        ("ROUTING_INHERITED_BLOCKER5_FULL_BIJECTION", "inherited_blocker5_full_projection_sha256"),
        ("ROUTING_NEW_BLOCKER5_FULL_BIJECTION", "new_blocker5_full_projection_sha256"),
        ("ROUTING_CARRY_AUTHORITY_PROMOTION", "carry_external_promotion_count"),
        ("ROUTING_COMPONENT_IDS", "component_ids"), ("ROUTING_COMPONENT_OWNERS", "component_targets"),
        ("ROUTING_COMPONENT_STATUS", "component_statuses"), ("ROUTING_PARENT_OPERATOR", "parent_operator"),
        ("ROUTING_PARENT_TARGET", "parent_target"), ("ROUTING_PARENT_STATUS", "parent_status"),
        ("ROUTING_BLOCKER_DEBT_MEMBERS", "blocker_source_debt_ids"), ("ROUTING_BLOCKER_DEBT_ID_SET", "blocker_source_debt_id_sha256"),
        ("ROUTING_BLOCKER_IDENTITY", "parent_sha256"), ("ROUTING_AUTHORITY_PROMOTION", "external_promotion_count"),
    ]


def plan_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    exists = PLAN.exists()
    text = normalized_lf_bytes(PLAN).decode("utf-8") if exists else ""
    lines = text.splitlines()
    record(checks, "PLAN_EXISTS", exists, PLAN.relative_to(REPO).as_posix())
    if not exists:
        return {"path": PLAN.relative_to(REPO).as_posix(), "lines": 0, "normalized_sha256": None}
    eol_ok, eol = eol_evidence(PLAN)
    record(checks, "PLAN_UTF8_EOL", eol_ok, eol)
    record(checks, "PLAN_NORMALIZED_SHA", sha256_bytes(normalized_lf_bytes(PLAN)) == EXPECTED_PLAN_SHA256, sha256_bytes(normalized_lf_bytes(PLAN)))
    record(checks, "PLAN_LINE_COUNT", len(lines) == 762, len(lines))
    positions = [text.find(section) for section in SECTIONS]
    record(checks, "PLAN_SECTION_ORDER", all(pos >= 0 for pos in positions) and positions == sorted(positions) and len(set(positions)) == len(positions) and all(text.count(section) == 1 for section in SECTIONS), dict(zip(SECTIONS, positions, strict=True)))
    executable = text[text.find("## Phase 062 — v1.0.21 Reaudit"):]
    headings = [line for line in executable.splitlines() if line.startswith("### Step ")]
    record(checks, "PLAN_CUMULATIVE_STEPS", len(headings) == 7 and all(row.startswith(prefix) for row, prefix in zip(headings, STEP_PREFIXES, strict=True)), headings)
    record(checks, "PLAN_NO_STEP_RESTART", "### Step 1 " not in text and "### Step 58 " not in text, "52..57.2 only")
    output_missing = [path for path in DECLARED_OUTPUTS if path not in text]
    record(checks, "PLAN_OUTPUTS", not output_missing, output_missing)
    subject_missing = [value for value in SUBJECTS if value not in text]
    record(checks, "PLAN_SUBJECTS", not subject_missing, subject_missing)
    gate_missing = [value for value in GATES if value not in text]
    record(checks, "PLAN_GATES", not gate_missing, gate_missing)
    exact_tokens = {
        "PLAN_RELEASE_DENOMINATOR": "68 path occurrences / 68 unique paths / 68 unique Git blobs / 4,071,795 bytes",
        "PLAN_TEXT_DENOMINATOR": "21,048 physical lines, 20,424 nonblank lines",
        "PLAN_PDF_DENOMINATOR": "5 files / 214 pages",
        "PLAN_SUPPLEMENTAL_DENOMINATOR": "68 release occurrences + 1 supplemental process-control occurrence",
        "PLAN_ROUTE_DENOMINATOR": "target Phase 062인 evidence route는 149건",
        "PLAN_DEBT_DENOMINATOR": "origin target Phase 062는 15, effective target Phase 062는 4",
        "PLAN_AUTHORITY_BOUNDARY": "Do not treat plan, change log, execution ledger, handover, snapshot, build success, test exit, code-match self-report or generated PDF as primary scientific authority",
        "PLAN_CODE_FREE_BOUNDARY": "Do not introduce code discussion into a future scholarly main body",
        "PLAN_STEP58_BLOCK": "Phase 063 Step 58 may not begin before `PASS_P062_STEP57_2_PERSISTENCE` and a new Phase 063 detailed plan is saved, reviewed, validated, atomically committed, pushed and remote-verified",
        "PLAN_ALL_OF_BOUNDARY": "A01–A05를 모두 충족해도 `P061-BD-NEW-001` 전체 status는 `OPEN`으로 유지",
        "PLAN_FIRST_ORDER_AUTHORITY": "이 파일만으로 first-order `USER_REQUIREMENT`를 복원하지 않는다",
        "PLAN_Q1_PARTIAL_REPORT": "Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md` 1–291",
        "PLAN_SNAPSHOT_STRICT": "Strict-parse all nine snapshot JSON files with duplicate-key/non-finite rejection",
        "PLAN_DERIVATION_AXES": "derivation_state = CONFIRMED_INTERNAL_DERIVATION | CONDITIONAL_ASSUMPTIONS | CONFLICTING | NOT_DERIVED",
        "PLAN_SOURCE_DISPOSITION_AXIS": "source_disposition = PRESERVE | CORRECT | UNVERIFIED | REJECT",
        "PLAN_RUNTIME_EXACT_QUEUE": "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
        "PLAN_RUNTIME_EXACT_QUEUE_LAST": "Claude/docs/v1.0.21/FITTING_GUIDE.md",
        "PLAN_A05_REQUIRED": "A05 is mandatory",
        "PLAN_A07_CORROBORATING": "as `corroborating_route` only",
        "PLAN_CARRY_MEMBERSHIP": "`P059-CFR-CF-11=141`",
        "PLAN_PERSISTENCE_SPLIT": "`PASS_P062_STEP52_PERSISTENCE`, `PASS_P062_STEP53_PERSISTENCE`",
        "PLAN_CODE_ALLOWLIST": "`_sections/ch1_appB_codemap.tex` and `_sections/ch2_appB_codemap.tex`",
        "PLAN_SUPPLEMENTAL_DISPOSITION": "### Supplemental process disposition row",
        "PLAN_PROCESS_ARTIFACT_SCHEMA": "### Q-phase process artifact row",
        "PLAN_SUPPLEMENTAL_RECOVERY_FIELDS": "Empty or missing source/evidence/reason/owner/acceptance fields are invalid",
    }
    for code, token in exact_tokens.items():
        record(checks, code, token in text, token)
    phase057 = []
    for relative, expected_lines in PHASE057_INPUTS:
        path = REPO / relative
        actual_lines = len(normalized_lf_bytes(path).decode("utf-8").splitlines()) if path.exists() else None
        phase057.append({"path": relative, "listed": relative in text, "lines": actual_lines, "expected_lines": expected_lines})
    record(checks, "PLAN_PHASE057_INPUTS", all(row["listed"] and row["lines"] == row["expected_lines"] for row in phase057) and sum(row["lines"] or 0 for row in phase057) == 819, phase057)
    return {
        "path": PLAN.relative_to(REPO).as_posix(), "lines": len(lines),
        "normalized_bytes": len(normalized_lf_bytes(PLAN)), "normalized_sha256": sha256_bytes(normalized_lf_bytes(PLAN)),
        "sections": SECTIONS, "step_headings": headings, "outputs": DECLARED_OUTPUTS,
        "subjects": SUBJECTS, "gates": GATES,
    }


def markdown_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def unique_prefixed(lines: list[str], prefix: str) -> list[str]:
    return [line for line in lines if line.startswith(prefix)]


CURRENT_TERMINAL_PATTERNS = [
    re.compile(r"^overall\s+gate\s*:", re.IGNORECASE),
    re.compile(r"^phase\s*0*62.*\bstatus\s*:", re.IGNORECASE),
    re.compile(r"^phase_?0*62_(?:fail|pass|conditional)\b", re.IGNORECASE),
]


def current_terminal_contradictions(text: str) -> list[str]:
    return [
        line for line in text.splitlines()
        if any(pattern.search(line.strip()) for pattern in CURRENT_TERMINAL_PATTERNS)
    ]


def current_terminal_diagnostics(surfaces: dict[str, str]) -> set[str]:
    return {
        "CONTROL_CURRENT_TERMINAL_CONTRADICTION"
        for text in surfaces.values() if current_terminal_contradictions(text)
    }


def result_and_controls(checks: list[dict[str, Any]]) -> dict[str, Any]:
    result = RESULT.read_text(encoding="utf-8") if RESULT.exists() else ""
    active = ACTIVE_LEDGER.read_text(encoding="utf-8") if ACTIVE_LEDGER.exists() else ""
    parent = PARENT_LEDGER.read_text(encoding="utf-8") if PARENT_LEDGER.exists() else ""
    handover = HANDOVER.read_text(encoding="utf-8") if HANDOVER.exists() else ""
    result_lines = result.splitlines()
    active_lines = active.splitlines()
    parent_lines = parent.splitlines()
    handover_lines = handover.splitlines()
    control_surfaces = {"result": result, "active": active, "parent": parent, "handover": handover}
    contradictions = {name: current_terminal_contradictions(text) for name, text in control_surfaces.items()}
    record(
        checks, "CONTROL_CURRENT_TERMINAL_CONTRADICTION",
        not current_terminal_diagnostics(control_surfaces), contradictions,
    )

    record(checks, "ACTIVATION_RESULT_MISSING", RESULT.exists(), RESULT.relative_to(REPO).as_posix())
    result_metadata = {
        "h1": result_lines[:1],
        "status": unique_prefixed(result_lines, "상태:"),
        "gate": unique_prefixed(result_lines, "Gate:"),
        "commit": unique_prefixed(result_lines, "Containing commit:"),
        "persistence": unique_prefixed(result_lines, "Postcommit persistence:"),
        "outcome_sections": [line for line in result_lines if line == "## 1. Outcome"],
    }
    result_structure_ok = (
        result_metadata["h1"] == ["# Phase 062 v1.0.21 Lineage Reaudit Plan Activation Result"]
        and result_metadata["status"] == ["상태: precommit content Gate 준비 완료; containing commit `PENDING_AT_PRECOMMIT_BY_DESIGN`"]
        and result_metadata["gate"] == ["Gate: `PASS_P062_PLAN_ACTIVATION`"]
        and result_metadata["commit"] == ["Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`"]
        and result_metadata["persistence"] == ["Postcommit persistence: `PENDING`"]
        and len(result_metadata["outcome_sections"]) == 1
        and "Gate: `FAIL_P062_PLAN_ACTIVATION`" not in result_lines
    )
    record(checks, "ACTIVATION_RESULT_STRUCTURE", result_structure_ok, result_metadata)
    result_required = [EXPECTED_SUBJECT, "Step 52", "Claude", "68", "149", "15", "4", "A01", "A07"]
    record(checks, "ACTIVATION_RESULT_CONTRACT", RESULT.exists() and all(token in result for token in result_required), {token: token in result for token in result_required})

    active_rows_raw = [line for line in active_lines if line.startswith("| 062 |")]
    parent_rows_raw = [line for line in parent_lines if line.startswith("| 062 |")]
    active_rows = [markdown_cells(line) for line in active_rows_raw]
    parent_rows = [markdown_cells(line) for line in parent_rows_raw]
    plan_path = PLAN.relative_to(REPO).as_posix()
    result_path = RESULT.relative_to(REPO).as_posix()
    output_path = OUTPUT.relative_to(REPO).as_posix()
    active_ok = (
        len(active_rows) == 1 and len(active_rows[0]) == 10
        and active_rows[0][0] == "062" and active_rows[0][4] == "IN_PROGRESS"
        and plan_path in active_rows[0][5] and result_path in active_rows[0][6]
        and output_path in active_rows[0][7]
        and "PASS_P062_PLAN_ACTIVATION" in active_rows[0][8]
        and "PENDING_AT_PRECOMMIT_BY_DESIGN" in active_rows[0][8]
        and "PASS_P062_PLAN_ACTIVATION_PERSISTENCE" in active_rows[0][9]
        and "Step 52" in active_rows[0][9]
    )
    parent_ok = (
        len(parent_rows) == 1 and len(parent_rows[0]) == 12
        and parent_rows[0][0] == "062" and parent_rows[0][5] == "IN_PROGRESS"
        and plan_path in parent_rows[0][6] and result_path in parent_rows[0][7]
        and output_path in parent_rows[0][8]
        and "PASS_P062_PLAN_ACTIVATION" in parent_rows[0][9]
        and "PENDING_AT_PRECOMMIT_BY_DESIGN" in parent_rows[0][9]
        and "PASS_P062_PLAN_ACTIVATION_PERSISTENCE" in parent_rows[0][11]
        and "Step 52" in parent_rows[0][11]
    )
    record(checks, "CONTROL_ACTIVE_LEDGER_STRUCTURE", active_ok, active_rows)
    record(checks, "CONTROL_PARENT_LEDGER_STRUCTURE", parent_ok, parent_rows)

    commit_rows_raw = [line for line in active_lines if line.startswith("| Phase 062 plan activation |")]
    commit_rows = [markdown_cells(line) for line in commit_rows_raw]
    commit_row_ok = (
        len(commit_rows) == 1 and len(commit_rows[0]) == 6
        and commit_rows[0][2] == "`PENDING_AT_PRECOMMIT_BY_DESIGN`"
        and commit_rows[0][3] == "exact-seven checkpoint prepared"
        and commit_rows[0][4] == "verify after atomic commit"
        and "PASS_P062_PLAN_ACTIVATION" in commit_rows[0][5]
        and "PASS_P062_PLAN_ACTIVATION_PERSISTENCE" in commit_rows[0][5]
    )
    record(checks, "CONTROL_COMMIT_LEDGER_STRUCTURE", commit_row_ok, commit_rows)

    phase61_rows = [line for line in [*active_lines, *parent_lines] if line.startswith("| 061 |")]
    phase61_persist = len(phase61_rows) == 2 and all(EXPECTED_PARENT in line and "PASS_P061_STEP51_2_PERSISTENCE" in line for line in phase61_rows)
    record(checks, "CONTROL_PHASE061_PERSISTENCE", phase61_persist, phase61_rows)

    current_state = unique_prefixed(handover_lines, "14. 현재 Phase 상태:")
    handover_chain_raw = [line for line in handover_lines if line.startswith("| Phase 062 detailed plan activation |")]
    handover_chain = [markdown_cells(line) for line in handover_chain_raw]
    exact_next_index = handover_lines.index("## Exact Next Action") if "## Exact Next Action" in handover_lines else -1
    exact_next_text = "\n".join(handover_lines[exact_next_index + 1:]) if exact_next_index >= 0 else ""
    handover_ok = (
        current_state == ["14. 현재 Phase 상태: Phase 062 `IN_PROGRESS`, Current checkpoint: detailed-plan activation precommit Gate"]
        and len(handover_chain) == 1 and len(handover_chain[0]) == 4
        and "PASS_P062_PLAN_ACTIVATION" in handover_chain[0][2]
        and "PENDING_AT_PRECOMMIT_BY_DESIGN" in handover_chain[0][2]
        and "PASS_P062_PLAN_ACTIVATION_PERSISTENCE" in handover_chain[0][3]
        and EXPECTED_SUBJECT in exact_next_text and EXPECTED_PARENT in exact_next_text
        and "exactly the seven" in exact_next_text and "Step 52" in exact_next_text
    )
    record(checks, "CONTROL_HANDOVER_STRUCTURE", handover_ok, {"current_state": current_state, "chain": handover_chain, "exact_next": exact_next_text})
    return {
        "result_exists": RESULT.exists(), "result_metadata": result_metadata,
        "active_rows": active_rows, "parent_rows": parent_rows,
        "commit_rows": commit_rows, "handover_current_state": current_state,
        "handover_chain": handover_chain,
    }


def repository_precommit(checks: list[dict[str, Any]], prospective_output: bool) -> dict[str, Any]:
    state: dict[str, Any] = {}
    try:
        state = {
            "branch": run_git("branch", "--show-current"), "head": run_git("rev-parse", "HEAD"),
            "upstream": run_git("rev-parse", "@{upstream}"),
            "origin_tracking": run_git("rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"),
            "live_active": remote_tip(ACTIVE_BRANCH),
            "protected_tracking": run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"),
            "protected_live": remote_tip(PROTECTED_BRANCH),
            "main_tracking": run_git("rev-parse", "refs/remotes/origin/main"),
            "main_live": remote_tip("main"),
        }
        state["claude_tracked"] = run_git("diff", "--name-only", f"refs/remotes/origin/{PROTECTED_BRANCH}", "--", "Claude").splitlines()
        state["claude_untracked"] = sorted(path for path in porcelain_paths() if path.startswith("Claude/"))
        record(checks, "REPOSITORY_BRANCH", state["branch"] == ACTIVE_BRANCH, state["branch"])
        record(checks, "REPOSITORY_ACTIVE_PARENT", state["head"] == state["upstream"] == state["origin_tracking"] == state["live_active"] == EXPECTED_PARENT, state)
        record(checks, "REPOSITORY_PROTECTED", state["protected_tracking"] == state["protected_live"] == EXPECTED_PROTECTED, state)
        record(checks, "REPOSITORY_MAIN", state["main_tracking"] == state["main_live"] == EXPECTED_MAIN, state)
        record(checks, "REPOSITORY_CLAUDE_UNCHANGED", not state["claude_tracked"] and not state["claude_untracked"], {"tracked": state["claude_tracked"], "untracked": state["claude_untracked"]})
    except Exception as exc:
        record(checks, "REPOSITORY_GIT_ERROR", False, str(exc))
    dirty = activation_dirty_paths(prospective_output)
    record(checks, "DIRTY_EXACT_SEVEN", dirty == EXACT_SEVEN_SET, {"actual": sorted(dirty), "missing": sorted(EXACT_SEVEN_SET - dirty), "extra": sorted(dirty - EXACT_SEVEN_SET)})
    record(checks, "DIFF_CHECK", not run_git("diff", "--check") and not run_git("diff", "--cached", "--check"), "working and cached")
    state["dirty_paths"] = sorted(dirty)
    return state


def summary_diagnostics(actual: dict[str, Any], expected: dict[str, Any], fields: list[tuple[str, str]]) -> set[str]:
    return {code for code, key in fields if actual.get(key) != expected.get(key)}


def abstract_plan_diagnostics(value: dict[str, Any]) -> set[str]:
    expected = {
        "sections": SECTIONS, "steps": STEP_PREFIXES, "outputs": DECLARED_OUTPUTS,
        "subjects": SUBJECTS, "gates": GATES, "step58_blocked": True,
        "authority_boundary": True, "first_order_boundary": True,
        "q1_partial_boundary": True, "snapshot_strict": True,
        "derivation_axes": True, "runtime_exact_queue": True,
        "a05_required": True, "a07_corroborating": True,
        "carry_membership": True, "persistence_split": True,
        "code_allowlist": True, "supplemental_disposition": True,
        "process_artifact_schema": True, "supplemental_recovery_fields": True,
    }
    codes = {
        "sections": "NEG_PLAN_SECTIONS", "steps": "NEG_PLAN_STEPS",
        "outputs": "NEG_PLAN_OUTPUTS", "subjects": "NEG_PLAN_SUBJECTS",
        "gates": "NEG_PLAN_GATES", "step58_blocked": "NEG_PLAN_STEP58",
        "authority_boundary": "NEG_PLAN_AUTHORITY",
        "first_order_boundary": "USER_TRANSCRIPT_FALSE_PRESENT",
        "q1_partial_boundary": "NEG_Q1_PARTIAL_PROMOTION",
        "snapshot_strict": "NEG_SNAPSHOT_STRICT_TRAVERSAL",
        "derivation_axes": "NEG_DERIVATION_AXIS_COLLAPSE",
        "runtime_exact_queue": "NEG_RUNTIME_DENOMINATOR",
        "a05_required": "NEG_A05_MISSING_BUILD",
        "a07_corroborating": "NEG_A07_OWNER_PROMOTION",
        "carry_membership": "NEG_CARRY_COUNT_ONLY",
        "persistence_split": "NEG_PERSISTENCE_SELF_REFERENCE",
        "code_allowlist": "NEG_CODE_ALLOWLIST_BASENAME",
        "supplemental_disposition": "NEG_SUPPLEMENTAL_DISPOSITION_FUSION",
        "process_artifact_schema": "NEG_PROCESS_ARTIFACT_SCHEMA",
        "supplemental_recovery_fields": "NEG_SUPPLEMENTAL_RECOVERY_FIELDS",
    }
    return {codes[key] for key in expected if value.get(key) != expected[key]}


def dirty_diagnostics(paths: set[str]) -> set[str]:
    return set() if paths == EXACT_SEVEN_SET else {"NEG_DIRTY_EXACT_SEVEN"}


def git_diagnostics(value: dict[str, str]) -> set[str]:
    expected = {"parent": EXPECTED_PARENT, "subject": EXPECTED_SUBJECT, "branch": ACTIVE_BRANCH, "protected": EXPECTED_PROTECTED, "main": EXPECTED_MAIN}
    codes = {"parent": "NEG_GIT_PARENT", "subject": "NEG_GIT_SUBJECT", "branch": "NEG_GIT_BRANCH", "protected": "NEG_GIT_PROTECTED", "main": "NEG_GIT_MAIN"}
    return {codes[key] for key in expected if value.get(key) != expected[key]}


def actual_manifest_diagnostics(value: dict[str, Any]) -> set[str]:
    return set() if sha256_bytes(canonical_bytes(value)) == EXPECTED_MANIFEST_OBJECT_SHA256 else {"NEG_ACTUAL_MANIFEST_OBJECT"}


def actual_target62_diagnostics(value: dict[str, Any]) -> set[str]:
    rows = sorted(
        (row for row in value.get("dispositions", []) if row.get("target_phase") == 62),
        key=lambda item: item.get("source_id", ""),
    )
    return set() if sha256_bytes(canonical_bytes(rows)) == EXPECTED_TARGET62_FULL_SHA256 else {"NEG_ACTUAL_TARGET62_BIJECTION"}


def actual_carry_partition_diagnostics(value: dict[str, Any], partition: str) -> set[str]:
    contracts = {
        "inherited_carry_items": ("carry_forward_id", EXPECTED_INHERITED52_FULL_SHA256, "NEG_ACTUAL_INHERITED52_BIJECTION"),
        "inherited_phase060_blockers": ("blocker_id", EXPECTED_INHERITED_BLOCKER5_FULL_SHA256, "NEG_ACTUAL_INHERITED_BLOCKER5_BIJECTION"),
        "new_blockers": ("blocker_id", EXPECTED_NEW_BLOCKER5_FULL_SHA256, "NEG_ACTUAL_NEW_BLOCKER5_BIJECTION"),
    }
    id_key, expected_sha, code = contracts[partition]
    rows = sorted(value.get(partition, []), key=lambda item: item.get(id_key, ""))
    return set() if sha256_bytes(canonical_bytes(rows)) == expected_sha else {code}


def actual_plan_token_diagnostics(text: str, token: str, code: str) -> set[str]:
    return set() if text.count(token) == 1 else {code}


def actual_result_gate_diagnostics(text: str) -> set[str]:
    lines = text.splitlines()
    gates = unique_prefixed(lines, "Gate:")
    return set() if gates == ["Gate: `PASS_P062_PLAN_ACTIVATION`"] else {"NEG_ACTUAL_RESULT_GATE"}


def actual_active_phase_row_diagnostics(text: str) -> set[str]:
    rows = [markdown_cells(line) for line in text.splitlines() if line.startswith("| 062 |")]
    return set() if len(rows) == 1 and len(rows[0]) == 10 and rows[0][4] == "IN_PROGRESS" else {"NEG_ACTUAL_ACTIVE_STATUS"}


def actual_handover_state_diagnostics(text: str) -> set[str]:
    rows = unique_prefixed(text.splitlines(), "14. 현재 Phase 상태:")
    expected = ["14. 현재 Phase 상태: Phase 062 `IN_PROGRESS`, Current checkpoint: detailed-plan activation precommit Gate"]
    return set() if rows == expected else {"NEG_ACTUAL_HANDOVER_STATE"}


def run_negative_controls() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []

    def add(case_id: str, expected: str | set[str], observed: set[str]) -> None:
        expected_codes = {expected} if isinstance(expected, str) else set(expected)
        cases.append({
            "case_id": case_id, "expected_codes": sorted(expected_codes),
            "observed_codes": sorted(observed), "passed": observed == expected_codes,
        })

    def full_routing_failures(disposition_value: dict[str, Any], carry_value: dict[str, Any]) -> set[str]:
        mutation_checks: list[dict[str, Any]] = []
        routing_contract(mutation_checks, disposition_value, carry_value)
        return {row["code"] for row in mutation_checks if not row["passed"]}

    json_cases = [
        ("NEG_JSON_DUPLICATE", b'{"a":1,"a":2}', DuplicateKeyError, "NEG_JSON_DUPLICATE"),
        ("NEG_JSON_NAN", b'{"a":NaN}', NonFiniteNumberError, "NEG_JSON_NAN"),
        ("NEG_JSON_POSITIVE_OVERFLOW", b'{"a":1e9999}', NonFiniteNumberError, "NEG_JSON_POSITIVE_OVERFLOW"),
        ("NEG_JSON_NEGATIVE_OVERFLOW", b'{"a":-1e9999}', NonFiniteNumberError, "NEG_JSON_NEGATIVE_OVERFLOW"),
    ]
    for case_id, data, exception_type, expected in json_cases:
        try:
            strict_load_bytes(data)
            observed: set[str] = set()
        except exception_type:
            observed = {expected}
        except Exception:
            observed = {"UNRELATED_EXCEPTION"}
        add(case_id, expected, observed)

    expected_manifest = expected_manifest_summary()
    for code, key in manifest_summary_fields():
        mutated = copy.deepcopy(expected_manifest)
        value = mutated[key]
        if isinstance(value, int):
            mutated[key] = value + 1
        elif isinstance(value, list):
            mutated[key] = value[:-1] if value else ["unexpected"]
        elif isinstance(value, dict):
            mutated[key] = {**value, "unexpected": 1}
        add(f"NEG_{code}", code, summary_diagnostics(mutated, expected_manifest, manifest_summary_fields()))

    expected_routing = expected_routing_summary()
    for code, key in routing_summary_fields():
        mutated = copy.deepcopy(expected_routing)
        value = mutated[key]
        if isinstance(value, bool):
            mutated[key] = not value
        elif isinstance(value, int):
            mutated[key] = value + 1
        elif isinstance(value, str):
            mutated[key] = value + "_MUTATED"
        elif isinstance(value, list):
            mutated[key] = value[:-1]
        elif isinstance(value, dict):
            first = next(iter(value))
            mutated[key][first] = "MUTATED" if isinstance(mutated[key][first], str) else 999
        add(f"NEG_{code}", code, summary_diagnostics(mutated, expected_routing, routing_summary_fields()))

    good_plan = {
        "sections": SECTIONS, "steps": STEP_PREFIXES, "outputs": DECLARED_OUTPUTS,
        "subjects": SUBJECTS, "gates": GATES, "step58_blocked": True,
        "authority_boundary": True, "first_order_boundary": True,
        "q1_partial_boundary": True, "snapshot_strict": True,
        "derivation_axes": True, "runtime_exact_queue": True,
        "a05_required": True, "a07_corroborating": True,
        "carry_membership": True, "persistence_split": True,
        "code_allowlist": True, "supplemental_disposition": True,
        "process_artifact_schema": True, "supplemental_recovery_fields": True,
    }
    for key, expected in [
        ("sections", "NEG_PLAN_SECTIONS"), ("steps", "NEG_PLAN_STEPS"),
        ("outputs", "NEG_PLAN_OUTPUTS"), ("subjects", "NEG_PLAN_SUBJECTS"),
        ("gates", "NEG_PLAN_GATES"), ("step58_blocked", "NEG_PLAN_STEP58"),
        ("authority_boundary", "NEG_PLAN_AUTHORITY"),
        ("first_order_boundary", "USER_TRANSCRIPT_FALSE_PRESENT"),
        ("q1_partial_boundary", "NEG_Q1_PARTIAL_PROMOTION"),
        ("snapshot_strict", "NEG_SNAPSHOT_STRICT_TRAVERSAL"),
        ("derivation_axes", "NEG_DERIVATION_AXIS_COLLAPSE"),
        ("runtime_exact_queue", "NEG_RUNTIME_DENOMINATOR"),
        ("a05_required", "NEG_A05_MISSING_BUILD"),
        ("a07_corroborating", "NEG_A07_OWNER_PROMOTION"),
        ("carry_membership", "NEG_CARRY_COUNT_ONLY"),
        ("persistence_split", "NEG_PERSISTENCE_SELF_REFERENCE"),
        ("code_allowlist", "NEG_CODE_ALLOWLIST_BASENAME"),
        ("supplemental_disposition", "NEG_SUPPLEMENTAL_DISPOSITION_FUSION"),
        ("process_artifact_schema", "NEG_PROCESS_ARTIFACT_SCHEMA"),
        ("supplemental_recovery_fields", "NEG_SUPPLEMENTAL_RECOVERY_FIELDS"),
    ]:
        mutated = copy.deepcopy(good_plan)
        mutated[key] = False if isinstance(mutated[key], bool) else mutated[key][:-1]
        add(expected, expected, abstract_plan_diagnostics(mutated))

    add("NEG_DIRTY_MISSING", "NEG_DIRTY_EXACT_SEVEN", dirty_diagnostics(EXACT_SEVEN_SET - {EXACT_SEVEN[0]}))
    add("NEG_DIRTY_EXTRA", "NEG_DIRTY_EXACT_SEVEN", dirty_diagnostics(EXACT_SEVEN_SET | {"Codex/work/v1021_phase062/unexpected.tmp"}))
    good_git = {"parent": EXPECTED_PARENT, "subject": EXPECTED_SUBJECT, "branch": ACTIVE_BRANCH, "protected": EXPECTED_PROTECTED, "main": EXPECTED_MAIN}
    for key, expected in [("parent", "NEG_GIT_PARENT"), ("subject", "NEG_GIT_SUBJECT"), ("branch", "NEG_GIT_BRANCH"), ("protected", "NEG_GIT_PROTECTED"), ("main", "NEG_GIT_MAIN")]:
        mutated = copy.deepcopy(good_git)
        mutated[key] += "_MUTATED"
        add(expected, expected, git_diagnostics(mutated))

    actual_manifest, _ = strict_load(MANIFEST)
    actual_disposition, _ = strict_load(DISPOSITION)
    actual_carry, _ = strict_load(CARRY)
    actual_plan = normalized_lf_bytes(PLAN).decode("utf-8")

    manifest_mutation = copy.deepcopy(actual_manifest)
    manifest_row = next(row for row in manifest_mutation["entries"] if row.get("version") == "v1.0.21")
    manifest_row["size_bytes"] += 1
    add("NEG_ACTUAL_MANIFEST_OBJECT", "NEG_ACTUAL_MANIFEST_OBJECT", actual_manifest_diagnostics(manifest_mutation))

    target_rows = [row for row in actual_disposition["dispositions"] if row.get("target_phase") == 62]
    link_mutation = copy.deepcopy(actual_disposition)
    link_rows = [row for row in link_mutation["dispositions"] if row.get("target_phase") == 62]
    pair = next((pair for i, left in enumerate(link_rows) for pair in [(left, link_rows[i + 1])] if i + 1 < len(link_rows) and left.get("carry_forward_links") != pair[1].get("carry_forward_links")), None)
    if pair is None:
        raise AssertionError("target-62 carry-link mutation pair unavailable")
    pair[0]["carry_forward_links"], pair[1]["carry_forward_links"] = pair[1]["carry_forward_links"], pair[0]["carry_forward_links"]
    add("NEG_ACTUAL_PER_SOURCE_LINK_SWAP", "ROUTING_TARGET62_FULL_BIJECTION", full_routing_failures(link_mutation, actual_carry))

    disposition_mutation = copy.deepcopy(actual_disposition)
    disposition_rows = [row for row in disposition_mutation["dispositions"] if row.get("target_phase") == 62]
    left = disposition_rows[0]
    right = next(row for row in disposition_rows[1:] if row.get("disposition") != left.get("disposition"))
    left["disposition"], right["disposition"] = right["disposition"], left["disposition"]
    add("NEG_ACTUAL_PER_SOURCE_DISPOSITION_SWAP", "ROUTING_TARGET62_FULL_BIJECTION", full_routing_failures(disposition_mutation, actual_carry))

    inherited_mutation = copy.deepcopy(actual_carry)
    inherited_mutation["inherited_carry_items"][0]["external_scientific_truth"] = True
    add(
        "NEG_ACTUAL_INHERITED_TRUTH_PROMOTION",
        {"ROUTING_INHERITED52_FULL_BIJECTION", "ROUTING_CARRY_AUTHORITY_PROMOTION"},
        full_routing_failures(actual_disposition, inherited_mutation),
    )

    blocker_mutation = copy.deepcopy(actual_carry)
    blocker_mutation["inherited_phase060_blockers"][0]["target_phase_after"] += 1
    add("NEG_ACTUAL_INHERITED_BLOCKER_TARGET", "ROUTING_INHERITED_BLOCKER5_FULL_BIJECTION", full_routing_failures(actual_disposition, blocker_mutation))

    new_blocker_mutation = copy.deepcopy(actual_carry)
    new_blocker_mutation["new_blockers"][0]["external_material_truth"] = True
    add(
        "NEG_ACTUAL_NEW_BLOCKER_TRUTH",
        {"ROUTING_NEW_BLOCKER5_FULL_BIJECTION", "ROUTING_CARRY_AUTHORITY_PROMOTION", "ROUTING_BLOCKER_IDENTITY"},
        full_routing_failures(actual_disposition, new_blocker_mutation),
    )

    first_order_token = "이 파일만으로 first-order `USER_REQUIREMENT`를 복원하지 않는다"
    add("USER_TRANSCRIPT_FALSE_PRESENT_ACTUAL", "USER_TRANSCRIPT_FALSE_PRESENT_ACTUAL", actual_plan_token_diagnostics(actual_plan.replace(first_order_token, "", 1), first_order_token, "USER_TRANSCRIPT_FALSE_PRESENT_ACTUAL"))

    actual_result = RESULT.read_text(encoding="utf-8")
    result_mutation = actual_result.replace("Gate: `PASS_P062_PLAN_ACTIVATION`", "Gate: `FAIL_P062_PLAN_ACTIVATION`", 1)
    add("NEG_ACTUAL_RESULT_GATE", "NEG_ACTUAL_RESULT_GATE", actual_result_gate_diagnostics(result_mutation))

    actual_active = ACTIVE_LEDGER.read_text(encoding="utf-8")
    active_mutation = actual_active.replace("| 062 | 52–57 | plan activation; Steps 52–57.2 pending | v1.0.21 reaudit | IN_PROGRESS |", "| 062 | 52–57 | plan activation; Steps 52–57.2 pending | v1.0.21 reaudit | FAIL |", 1)
    add("NEG_ACTUAL_ACTIVE_STATUS", "NEG_ACTUAL_ACTIVE_STATUS", actual_active_phase_row_diagnostics(active_mutation))

    actual_handover = HANDOVER.read_text(encoding="utf-8")
    handover_mutation = actual_handover.replace("14. 현재 Phase 상태: Phase 062 `IN_PROGRESS`", "14. 현재 Phase 상태: Phase 062 `FAIL`", 1)
    add("NEG_ACTUAL_HANDOVER_STATE", "NEG_ACTUAL_HANDOVER_STATE", actual_handover_state_diagnostics(handover_mutation))

    base_surfaces = {
        "result": actual_result, "active": actual_active,
        "parent": PARENT_LEDGER.read_text(encoding="utf-8"), "handover": actual_handover,
    }
    terminal_mutations = {
        "RESULT_OVERALL_FAIL": ("result", "Overall gate: FAIL"),
        "ACTIVE_PHASE062_FAIL": ("active", "PHASE062_FAIL"),
        "PARENT_PHASE062_STATUS_FAIL": ("parent", "Phase 062 Step 52 Status: FAIL"),
        "HANDOVER_OVERALL_FAIL": ("handover", "Overall Gate: FAIL"),
    }
    for case_id, (surface, terminal) in terminal_mutations.items():
        mutated_surfaces = copy.deepcopy(base_surfaces)
        mutated_surfaces[surface] += f"\n{terminal}\n"
        add(case_id, "CONTROL_CURRENT_TERMINAL_CONTRADICTION", current_terminal_diagnostics(mutated_surfaces))
    return {"total": len(cases), "passed": sum(row["passed"] for row in cases), "failed": [row["case_id"] for row in cases if not row["passed"]], "cases": cases}


def content_projection(plan: dict[str, Any], manifest: dict[str, Any], supplemental: dict[str, Any], routing: dict[str, Any], negative_ids: list[str]) -> dict[str, Any]:
    return {
        "plan": {"lines": plan.get("lines"), "normalized_sha256": plan.get("normalized_sha256"), "step_headings": plan.get("step_headings")},
        "manifest": {"normalized_sha256": manifest["normalized_sha256"], "summary": manifest["summary"], "path_set_sha256": manifest["path_set_sha256"], "path_blob_set_sha256": manifest["path_blob_set_sha256"]},
        "supplemental": supplemental, "routing": routing["summary"], "exact_seven": EXACT_SEVEN,
        "negative_case_ids": negative_ids,
    }


def build_content() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    plan = plan_contract(checks)
    manifest = selected_manifest_contract(checks)
    supplemental = supplemental_contract(checks, manifest)
    routing = routing_contract(checks)
    negatives = run_negative_controls()
    record(checks, "NEGATIVE_CONTROLS", negatives["passed"] == negatives["total"] and negatives["total"] >= 40, negatives)
    negative_ids = [row["case_id"] for row in negatives["cases"]]
    projection = content_projection(plan, manifest, supplemental, routing, negative_ids)
    return checks, {"plan": plan, "manifest": manifest, "supplemental": supplemental, "routing": routing, "negative_controls": negatives, "projection": projection}


def nonself_hashes() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for relative in NONSELF_SURFACES:
        path = REPO / relative
        normalized = normalized_lf_bytes(path) if path.exists() else b""
        result[relative] = {"exists": path.exists(), "normalized_bytes": len(normalized) if path.exists() else None, "normalized_sha256": sha256_bytes(normalized) if path.exists() else None}
    return result


def build_payload_core(prospective_output: bool) -> dict[str, Any]:
    checks, content = build_content()
    controls = result_and_controls(checks)
    repository = repository_precommit(checks, prospective_output)
    hashes = nonself_hashes()
    record(checks, "NONSELF_SURFACES", all(row["exists"] for row in hashes.values()), hashes)
    return {
        "content": content, "controls": controls, "repository": repository,
        "hashes": hashes, "checks": checks,
    }


def full_core_projection(core: dict[str, Any]) -> dict[str, Any]:
    content = core["content"]
    return {
        "schema_version": 1, "generated_date": "2026-08-27", "phase": 62,
        "unit": "PLAN_ACTIVATION", "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT, "exact_allowlist": EXACT_SEVEN,
        "plan_contract": content["plan"], "manifest_contract": content["manifest"],
        "supplemental_contract": content["supplemental"], "routing_contract": content["routing"],
        "control_contract": core["controls"], "repository_state": core["repository"],
        "artifact_hashes_nonself": core["hashes"], "checks": core["checks"],
        "negative_controls": content["negative_controls"],
    }


def build_payload(prospective_output: bool = False) -> dict[str, Any]:
    first_core = build_payload_core(prospective_output)
    second_core = build_payload_core(prospective_output)
    first = canonical_bytes(full_core_projection(first_core))
    second = canonical_bytes(full_core_projection(second_core))
    second_failed = [row["code"] for row in second_core["checks"] if not row["passed"]]
    determinism = {
        "runs": 2, "scope": "FULL_SEMANTIC_PAYLOAD_EXCLUDING_SELF_REFERENTIAL_DETERMINISM_AND_SUMMARY",
        "byte_identical": first == second, "sha256_run1": sha256_bytes(first),
        "sha256_run2": sha256_bytes(second), "second_run_failed_codes": second_failed,
    }
    checks = first_core["checks"]
    content = first_core["content"]
    record(checks, "DETERMINISM_2_OF_2", first == second and not second_failed, determinism)
    failed = [row["code"] for row in checks if not row["passed"]]
    payload: dict[str, Any] = {
        "schema_version": 1, "generated_date": "2026-08-27", "phase": 62, "unit": "PLAN_ACTIVATION",
        "gate": "PASS_P062_PLAN_ACTIVATION" if not failed else "FAIL_P062_PLAN_ACTIVATION",
        "expected_parent": EXPECTED_PARENT, "expected_subject": EXPECTED_SUBJECT, "exact_allowlist": EXACT_SEVEN,
        "plan_contract": content["plan"], "manifest_contract": content["manifest"],
        "supplemental_contract": content["supplemental"], "routing_contract": content["routing"],
        "control_contract": first_core["controls"], "repository_state": first_core["repository"], "artifact_hashes_nonself": first_core["hashes"],
        "checks": checks, "negative_controls": content["negative_controls"], "determinism": determinism,
        "deterministic_projection_sha256": sha256_bytes(first),
        "content_projection_sha256": sha256_bytes(canonical_bytes(content["projection"])),
        "summary": {"checks_total": len(checks), "checks_passed": len(checks) - len(failed), "checks_failed": len(failed), "failed_codes": failed},
    }
    semantic = copy.deepcopy(payload)
    payload["semantic_sha256"] = sha256_bytes(canonical_bytes(semantic))
    return payload


def semantic_hash_ok(payload: dict[str, Any]) -> bool:
    expected = payload.get("semantic_sha256")
    projection = copy.deepcopy(payload)
    projection.pop("semantic_sha256", None)
    return isinstance(expected, str) and expected == sha256_bytes(canonical_bytes(projection))


def validate_stored() -> int:
    if not OUTPUT.exists():
        print("FAIL STORED_ARTIFACT_MISSING")
        return 1
    try:
        stored, traversal = strict_load(OUTPUT)
        current = build_payload()
    except Exception as exc:
        print(f"FAIL STORED_VALIDATION_ERROR:{type(exc).__name__}:{exc}")
        return 1
    failures: list[str] = []
    if not semantic_hash_ok(stored):
        failures.append("STORED_SEMANTIC_HASH")
    if stored != current:
        failures.append("STORED_CURRENT_MISMATCH")
    if stored.get("gate") != "PASS_P062_PLAN_ACTIVATION":
        failures.append("STORED_GATE")
    if failures:
        print("FAIL " + " ".join(failures))
        return 1
    print(f"PASS_P062_PLAN_ACTIVATION {stored['summary']['checks_passed']}/{stored['summary']['checks_total']} nodes={traversal['nodes']}")
    return 0


def verify_staged() -> int:
    if validate_stored() != 0:
        return 1
    failures: list[str] = []
    try:
        staged = nul_paths("diff", "--cached", "--name-only", "-z")
        unstaged = nul_paths("diff", "--name-only", "-z")
        dirty = activation_dirty_paths()
        if staged != EXACT_SEVEN_SET:
            failures.append("STAGED_EXACT_SEVEN")
        if unstaged:
            failures.append("STAGED_UNSTAGED_PRESENT")
        if dirty != EXACT_SEVEN_SET:
            failures.append("STAGED_DIRTY_EXACT_SEVEN")
        for relative in EXACT_SEVEN:
            staged_bytes = run_git_bytes("show", f":{relative}", check=False)
            if not (REPO / relative).exists() or staged_bytes != (REPO / relative).read_bytes():
                failures.append(f"STAGED_WORKTREE_BYTES:{relative}")
        if run_git("diff", "--cached", "--check"):
            failures.append("STAGED_DIFF_CHECK")
    except (GitCommandError, OSError, UnicodeError) as exc:
        failures.append(f"STAGED_GIT_ERROR:{type(exc).__name__}")
    if failures:
        print("FAIL " + " ".join(failures))
        return 1
    print("PASS_P062_PLAN_ACTIVATION_STAGED 7/7")
    return 0


def verify_persistence(expected_commit: str | None) -> int:
    if not OUTPUT.exists():
        print("FAIL PERSISTENCE_ARTIFACT_MISSING")
        return 1
    failures: list[str] = []
    try:
        stored, _ = strict_load(OUTPUT)
        content_checks, current = build_content()
        if not semantic_hash_ok(stored) or stored.get("gate") != "PASS_P062_PLAN_ACTIVATION":
            failures.append("PERSISTENCE_STORED_ARTIFACT")
        if [row["code"] for row in content_checks if not row["passed"]]:
            failures.append("PERSISTENCE_CONTENT")
        if stored.get("content_projection_sha256") != sha256_bytes(canonical_bytes(current["projection"])):
            failures.append("PERSISTENCE_RECONSTRUCTION")
        for relative, expected in stored.get("artifact_hashes_nonself", {}).items():
            path = REPO / relative
            actual = normalized_lf_bytes(path) if path.exists() else b""
            if not path.exists() or len(actual) != expected.get("normalized_bytes") or sha256_bytes(actual) != expected.get("normalized_sha256"):
                failures.append(f"PERSISTENCE_SURFACE:{relative}")
        head = run_git("rev-parse", "HEAD")
        if expected_commit and head != expected_commit:
            failures.append("PERSISTENCE_EXPECTED_COMMIT")
        parent = run_git("rev-parse", "HEAD^")
        subject = run_git("show", "-s", "--format=%s", "HEAD")
        committed = nul_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD")
        branch = run_git("branch", "--show-current")
        upstream = run_git("rev-parse", "@{upstream}")
        tracking = run_git("rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}")
        live = remote_tip(ACTIVE_BRANCH)
        protected_tracking = run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")
        protected_live = remote_tip(PROTECTED_BRANCH)
        main_tracking = run_git("rev-parse", "refs/remotes/origin/main")
        main_live = remote_tip("main")
        claude = run_git("diff", "--name-only", f"refs/remotes/origin/{PROTECTED_BRANCH}", "--", "Claude")
        if parent != EXPECTED_PARENT:
            failures.append("PERSISTENCE_PARENT")
        if subject != EXPECTED_SUBJECT:
            failures.append("PERSISTENCE_SUBJECT")
        if committed != EXACT_SEVEN_SET:
            failures.append("PERSISTENCE_EXACT_SEVEN")
        if porcelain_paths():
            failures.append("PERSISTENCE_DIRTY")
        if not (branch == ACTIVE_BRANCH and head == upstream == tracking == live):
            failures.append("PERSISTENCE_ACTIVE_REMOTE")
        if protected_tracking != protected_live or protected_live != EXPECTED_PROTECTED:
            failures.append("PERSISTENCE_PROTECTED")
        if main_tracking != main_live or main_live != EXPECTED_MAIN:
            failures.append("PERSISTENCE_MAIN")
        if claude:
            failures.append("PERSISTENCE_CLAUDE")
        if run_git("diff", "--check"):
            failures.append("PERSISTENCE_DIFF_CHECK")
    except Exception as exc:
        failures.append(f"PERSISTENCE_EXCEPTION:{type(exc).__name__}:{exc}")
        head = "UNKNOWN"
    if failures:
        print("FAIL " + " ".join(failures))
        return 1
    print(f"PASS_P062_PLAN_ACTIVATION_PERSISTENCE head={head}")
    return 0


def run_content_only(show_negative: bool, show_determinism: bool) -> int:
    try:
        checks, content = build_content()
    except Exception as exc:
        print(f"FAIL CONTENT_EXCEPTION:{type(exc).__name__}:{exc}")
        return 1
    failed = [row["code"] for row in checks if not row["passed"]]
    if failed:
        print("FAIL " + " ".join(failed))
        return 1
    if show_negative:
        neg = content["negative_controls"]
        print(f"PASS_P062_PLAN_NEGATIVE_CONTROLS {neg['passed']}/{neg['total']}")
    if show_determinism:
        try:
            payload = build_payload(prospective_output=not OUTPUT.exists())
        except Exception as exc:
            print(f"FAIL PLAN_DETERMINISM_EXCEPTION:{type(exc).__name__}:{exc}")
            return 1
        determinism = payload["determinism"]
        if payload["gate"] != "PASS_P062_PLAN_ACTIVATION" or not determinism["byte_identical"] or determinism["second_run_failed_codes"]:
            print("FAIL PLAN_FULL_SEMANTIC_DETERMINISM")
            return 1
        print(f"PASS_P062_PLAN_DETERMINISM 2/2 scope=FULL_SEMANTIC_PAYLOAD sha256={determinism['sha256_run1']}")
    print(f"PASS_P062_PLAN_CONTENT {len(checks)}/{len(checks)}")
    return 0


def collect() -> int:
    try:
        payload = build_payload(prospective_output=True)
    except Exception as exc:
        print(f"FAIL COLLECTION_EXCEPTION:{type(exc).__name__}:{exc}")
        return 1
    failed = payload["summary"]["failed_codes"]
    if failed:
        print("FAIL " + " ".join(failed))
        print(f"FAIL_P062_PLAN_ACTIVATION {payload['summary']['checks_passed']}/{payload['summary']['checks_total']}")
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_bytes(payload))
    print(f"PASS_P062_PLAN_ACTIVATION {payload['summary']['checks_passed']}/{payload['summary']['checks_total']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.verify_persistence:
        return verify_persistence(args.expected_commit)
    if args.verify_staged:
        return verify_staged()
    if args.collect:
        return collect()
    if args.content_only or args.run_negative_probes or args.determinism_check:
        return run_content_only(args.run_negative_probes, args.determinism_check)
    return validate_stored()


if __name__ == "__main__":
    sys.exit(main())
