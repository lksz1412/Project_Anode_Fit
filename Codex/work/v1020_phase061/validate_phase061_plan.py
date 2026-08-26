#!/usr/bin/env python3
"""Validate and persistence-check the Phase 061 detailed-plan activation unit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
PLAN = REPO / "Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md"
RESULT = REPO / "Codex/results/PHASE_061_PLAN_ACTIVATION_RESULT.md"
OUTPUT = REPO / "Codex/results/PHASE_061_PLAN_ACTIVATION_VALIDATION.json"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
CARRY_059 = REPO / "Codex/results/PHASE_059_CARRY_FORWARD_REGISTER.json"
CARRY_060 = REPO / "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json"
DISPOSITION_060 = REPO / "Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json"

PHASE057_INPUTS = [
    "Codex/results/PHASE_057E_V1020_FOUNDATION_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057F_V1020_P2_P6_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057G_V1020_P7_REVIEW_DIRECTION_OBSERVATIONS.md",
    "Codex/results/PHASE_057H_V1020_CLOSING_DIRECTION_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057I_V1020_SNAPSHOT_LINEAGE_OBSERVATIONS.md",
]

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "136a73804d714706bad1be6d58c99351e606fe0e"
EXPECTED_SUBJECT = "docs(phase061): plan v1020 lineage reaudit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EXPECTED_MANIFEST_NORMALIZED_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"

EXACT_SEVEN = [
    "Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md",
    "Codex/work/v1020_phase061/validate_phase061_plan.py",
    "Codex/results/PHASE_061_PLAN_ACTIVATION_VALIDATION.json",
    "Codex/results/PHASE_061_PLAN_ACTIVATION_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]
EXACT_SEVEN_SET = set(EXACT_SEVEN)
NONSELF_SURFACES = [path for path in EXACT_SEVEN if not path.endswith("VALIDATION.json")]

MANIFEST_TOP_KEYS = {
    "schema_version", "generated_date", "baseline_commit", "version_scope",
    "path_count", "unique_blob_count", "counts", "validation", "entries",
}
ENTRY_BASE_KEYS = {
    "path", "version", "blob_sha", "dedup_group", "git_mode", "size_bytes",
    "extension", "role", "review_mode", "extent",
}


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
    depth = path.count(".") + path.count("[")
    stats["max_depth"] = max(stats["max_depth"], depth)
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(path)
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(f"non-string key at {path}")
            walk_json(child, f"{path}.{key}", stats)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_json(child, f"{path}[{index}]", stats)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise TypeError(f"unsupported JSON type at {path}: {type(value).__name__}")
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
        data.decode("utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
    )
    walk_json(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_lf_bytes(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def valid_text_eol(path: Path) -> tuple[bool, dict[str, Any]]:
    raw = path.read_bytes()
    raw.decode("utf-8")
    crlf = raw.count(b"\r\n")
    all_lf = raw.count(b"\n")
    bare_cr = raw.replace(b"\r\n", b"").count(b"\r")
    mixed_lf = crlf > 0 and all_lf > crlf
    normalized = normalized_lf_bytes(path)
    return not bare_cr and not mixed_lf, {
        "encoding": "utf-8",
        "normalized_lines": len(normalized.decode("utf-8").splitlines()),
        "normalized_bytes": len(normalized),
        "normalized_sha256": sha256_bytes(normalized),
    }


def run_git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8", errors="strict",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def run_git_bytes(*args: str, check: bool = True) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.decode('utf-8', errors='replace').strip()}")
    return proc.stdout


def remote_tip(branch: str) -> str:
    row = run_git("ls-remote", "--heads", "origin", branch)
    parts = row.split()
    return parts[0] if len(parts) == 2 else ""


def git_blob(path: str) -> tuple[str, str, bytes]:
    row = run_git("ls-tree", BASELINE, "--", path)
    if not row:
        raise FileNotFoundError(path)
    meta, _ = row.split("\t", 1)
    mode, object_type, blob = meta.split()
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
        path = field[3:].replace("\\", "/")
        paths.add(path)
        if "R" in status or "C" in status:
            index += 1
            if index < len(fields) and fields[index]:
                paths.add(fields[index].decode("utf-8").replace("\\", "/"))
        index += 1
    return paths


def activation_dirty_paths() -> set[str]:
    """Return porcelain dirt plus existing expected ignored/untracked activation files."""
    paths = porcelain_paths()
    for relative in EXACT_SEVEN:
        path = REPO / relative
        tracked = run_git("ls-files", "--error-unmatch", relative, check=False)
        if path.exists() and not tracked:
            paths.add(relative)
    return paths


def nul_paths(*args: str) -> set[str]:
    raw = run_git_bytes(*args)
    return {item.decode("utf-8").replace("\\", "/") for item in raw.split(b"\0") if item}


def record(checks: list[dict[str, Any]], code: str, passed: bool, evidence: Any) -> None:
    checks.append({"code": code, "passed": bool(passed), "evidence": evidence})


def scheduled_steps(index: int, entry: dict[str, Any]) -> list[str]:
    path = entry["path"]
    steps = ["46", "51.1"]
    if 54 <= index <= 220 or "HANDOVER" in path:
        steps.append("47")
    if index <= 53 or index >= 221:
        steps.append("48")
    if index <= 53 and entry["extension"] in {"tex", "md"}:
        steps.append("49")
    if entry["review_mode"] in {"FULL_PDF", "FULL_IMAGE"} or "/comp_" in path:
        steps.append("50")
    return steps


def collect_manifest_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    manifest, traversal = strict_load(MANIFEST)
    manifest_sha = sha256_bytes(normalized_lf_bytes(MANIFEST))
    record(
        checks,
        "MANIFEST_NORMALIZED_SHA",
        manifest_sha == EXPECTED_MANIFEST_NORMALIZED_SHA256,
        {"basis": "UTF-8_LF_NORMALIZED", "sha256": manifest_sha},
    )
    record(checks, "MANIFEST_TOP_SCHEMA", set(manifest) == MANIFEST_TOP_KEYS, sorted(manifest))
    record(checks, "MANIFEST_BASELINE", manifest.get("baseline_commit") == BASELINE, manifest.get("baseline_commit"))
    record(checks, "MANIFEST_TOTAL_ROWS", manifest.get("path_count") == len(manifest.get("entries", [])) == 1520, manifest.get("path_count"))

    selected = [entry for entry in manifest["entries"] if entry.get("version") == "v1.0.20"]
    records: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    nonblank = 0
    text_lines = 0
    pdf_pages = 0
    image_frames = 0
    allowed_entry_shapes = {frozenset(ENTRY_BASE_KEYS), frozenset(ENTRY_BASE_KEYS | {"candidate_tex_paths"})}
    for index, entry in enumerate(selected, start=1):
        if frozenset(entry) not in allowed_entry_shapes:
            mismatches.append({"path": entry.get("path"), "kind": "entry_schema", "keys": sorted(entry)})
            continue
        mode = entry["review_mode"]
        expected_extent_keys = {
            "FULL_TEXT": {"lines", "encoding_check"},
            "FULL_PDF": {"pages", "encrypted"},
            "FULL_IMAGE": {"width", "height", "mode", "format", "frames"},
        }.get(mode, set())
        if set(entry["extent"]) != expected_extent_keys:
            mismatches.append({"path": entry["path"], "kind": "extent_schema", "keys": sorted(entry["extent"])})
            continue
        try:
            actual_mode, actual_blob, data = git_blob(entry["path"])
        except Exception as exc:  # converted to evidence, never a traceback-only gate
            mismatches.append({"path": entry.get("path"), "kind": "git_read", "error": str(exc)})
            continue
        local_mismatch: list[str] = []
        if actual_mode != entry["git_mode"]:
            local_mismatch.append("mode")
        if actual_blob != entry["blob_sha"]:
            local_mismatch.append("blob")
        if len(data) != entry["size_bytes"]:
            local_mismatch.append("size")
        if mode == "FULL_TEXT":
            lines = data.decode("utf-8").splitlines()
            if len(lines) != entry["extent"]["lines"]:
                local_mismatch.append("lines")
            text_lines += len(lines)
            nonblank += sum(bool(line.strip()) for line in lines)
        elif mode == "FULL_PDF":
            pdf_pages += entry["extent"]["pages"]
        elif mode == "FULL_IMAGE":
            image_frames += entry["extent"]["frames"]
        if local_mismatch:
            mismatches.append({"path": entry["path"], "kind": "identity", "fields": local_mismatch})
        records.append({
            "manifest_index_v1020": index,
            "path": entry["path"],
            "blob_sha1": entry["blob_sha"],
            "git_mode": entry["git_mode"],
            "size_bytes": entry["size_bytes"],
            "extension": entry["extension"],
            "role": entry["role"],
            "review_mode": mode,
            "extent": entry["extent"],
            "scheduled_steps": scheduled_steps(index, entry),
        })

    paths = [entry["path"] for entry in selected]
    blobs = [entry["blob_sha"] for entry in selected]
    mode_counts = Counter(entry["review_mode"] for entry in selected)
    role_counts = Counter(entry["role"] for entry in selected)
    ext_counts = Counter(entry["extension"] for entry in selected)
    blob_paths: dict[str, list[str]] = defaultdict(list)
    for entry in selected:
        blob_paths[entry["blob_sha"]].append(entry["path"])
    duplicate_groups = [
        {"blob_sha1": blob, "paths": sorted(group)}
        for blob, group in sorted(blob_paths.items()) if len(group) > 1
    ]
    exact = {
        "paths": len(selected),
        "unique_paths": len(set(paths)),
        "unique_blobs": len(set(blobs)),
        "total_bytes": sum(entry["size_bytes"] for entry in selected),
        "mode_counts": dict(sorted(mode_counts.items())),
        "role_counts": dict(sorted(role_counts.items())),
        "extension_counts": dict(sorted(ext_counts.items())),
        "text_lines": text_lines,
        "text_nonblank_lines": nonblank,
        "pdf_pages": pdf_pages,
        "image_frames": image_frames,
        "duplicate_groups": duplicate_groups,
    }
    expected = {
        "paths": 232, "unique_paths": 232, "unique_blobs": 231, "total_bytes": 8158832,
        "mode_counts": {"FULL_IMAGE": 23, "FULL_PDF": 14, "FULL_TEXT": 195},
        "role_counts": {"code": 1, "figure": 23, "generated_document": 14, "implementation_guide": 1, "plan": 10, "result": 141, "test": 1, "theory": 41},
        "extension_counts": {"json": 11, "md": 69, "pdf": 14, "png": 23, "py": 8, "tex": 105, "txt": 2},
        "text_lines": 31553, "text_nonblank_lines": 29335, "pdf_pages": 130, "image_frames": 23,
        "duplicate_groups": [{
            "blob_sha1": "8dfea239d1787582c6c37c41fe6d06f7b204d72b",
            "paths": [
                "Claude/docs/v1.0.20/results/snapshot_v1020_p5.json",
                "Claude/docs/v1.0.20/results/snapshot_v1020_p6.json",
            ],
        }],
    }
    record(checks, "V1020_EXACT_COUNTS", exact == expected, {"actual": exact, "expected": expected})
    record(checks, "V1020_GIT_IDENTITIES", not mismatches and len(records) == 232, mismatches)
    owner_bad = [row["path"] for row in records if not {"46", "51.1"}.issubset(row["scheduled_steps"]) or not set(row["scheduled_steps"]) & {"47", "48", "49", "50"}]
    record(checks, "V1020_STEP_OWNERS", not owner_bad, owner_bad)
    return {
        "manifest_path": MANIFEST.relative_to(REPO).as_posix(),
        "manifest_sha256": manifest_sha,
        "manifest_traversal": traversal,
        "summary": exact,
        "path_set_sha256": sha256_bytes(("\n".join(sorted(paths)) + "\n").encode("utf-8")),
        "path_blob_set_sha256": sha256_bytes(("\n".join(f"{entry['path']}\t{entry['blob_sha']}" for entry in sorted(selected, key=lambda row: row['path'])) + "\n").encode("utf-8")),
        "records": records,
    }


def check_plan(checks: list[dict[str, Any]]) -> dict[str, Any]:
    text = normalized_lf_bytes(PLAN).decode("utf-8") if PLAN.exists() else ""
    lines = text.splitlines()
    sections = [
        "## Summary", "## Current Ground Truth", "## Phase Range", "## Exact Read Inputs",
        "## Non-goals and Scope Guards", "## Implementation Changes",
        "## Plan Activation Unit — Save Before Step 46", "## Phase 061 — v1.0.20 Reaudit",
        "## Phase Gate", "## Implementation Interfaces", "## Test and Validation Plan",
        "## Stop Conditions", "## Assumptions", "## Correction History",
    ]
    positions = [text.find(section) for section in sections]
    record(checks, "PLAN_EXISTS", PLAN.exists(), PLAN.relative_to(REPO).as_posix())
    eol_ok, eol_evidence = valid_text_eol(PLAN) if PLAN.exists() else (False, {})
    record(checks, "PLAN_UTF8_EOL_NORMALIZED", eol_ok, eol_evidence)
    record(checks, "PLAN_SECTION_ORDER", all(pos >= 0 for pos in positions) and positions == sorted(positions) and len(set(positions)) == len(positions), dict(zip(sections, positions, strict=True)))
    executable_text = text[text.find("## Phase 061 — v1.0.20 Reaudit"):]
    step_headings = [line for line in executable_text.splitlines() if line.startswith("### Step ")]
    expected_prefixes = ["### Step 46 ", "### Step 47 ", "### Step 48 ", "### Step 49 ", "### Step 50 ", "### Step 51.1 ", "### Step 51.2 "]
    record(checks, "PLAN_CUMULATIVE_STEPS", len(step_headings) == 7 and all(row.startswith(prefix) for row, prefix in zip(step_headings, expected_prefixes, strict=True)), step_headings)
    record(checks, "PLAN_NO_RESTART_OR_STEP52", "### Step 1 " not in text and "### Step 52 " not in text, "Step 46..51.2 only")
    required = [
        "232 path occurrences, 231 unique Git blobs", "FULL_TEXT=195", "31,553 physical lines",
        "29,335 nonblank lines", "14 files / 130 pages", "FULL_IMAGE=23",
        "same-relative-path comparison pair는 47개", "target Phase 061인 evidence route는 36건",
        "PASS_P061_PLAN_ACTIVATION", "PASS_P061_LINEAGE_D", "CONDITIONAL_P061", "FAIL_P061",
        EXPECTED_SUBJECT, "audit(phase061): freeze v1020 source topology",
        "audit(phase061): adjudicate v1020 process authority", "audit(phase061): trace v1019-v1020 lineage delta",
        "audit(phase061): bound v1020 citation authority", "audit(phase061): adjudicate v1020 review artifacts",
        "audit(phase061): disposition v1020 lineage", "audit(phase061): close v1020 lineage gate",
        "primary literature", "competing draft", "adopted release", "code-free main-body",
        "Phase 062 Step 52 may not begin before a new Phase 062 detailed plan is saved",
    ]
    record(checks, "PLAN_POLICY_CONTRACT", all(token in text for token in required), {token: token in text for token in required})
    phase057_records = []
    for relative in PHASE057_INPUTS:
        path = REPO / relative
        phase057_records.append({
            "path": relative,
            "listed": relative in text,
            "exists": path.exists(),
            "lines": len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else None,
            "normalized_sha256": sha256_bytes(normalized_lf_bytes(path)) if path.exists() else None,
        })
    record(
        checks,
        "PLAN_PHASE057_EXACT_INPUTS",
        all(row["listed"] and row["exists"] for row in phase057_records)
        and [row["lines"] for row in phase057_records] == [180, 147, 236, 306, 183],
        phase057_records,
    )
    outputs = EXACT_SEVEN + [
        "Codex/work/v1020_phase061/build_phase061_step46_source_topology.py",
        "Codex/work/v1020_phase061/validate_phase061_step46.py",
        "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json",
        "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json",
        "Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md",
        "Codex/work/v1020_phase061/build_phase061_step47_process_authority.py",
        "Codex/work/v1020_phase061/validate_phase061_step47.py",
        "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json",
        "Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md",
        "Codex/work/v1020_phase061/build_phase061_step48_lineage_diff.py",
        "Codex/work/v1020_phase061/validate_phase061_step48.py",
        "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json",
        "Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json",
        "Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md",
        "Codex/work/v1020_phase061/build_phase061_step49_citation_authority.py",
        "Codex/work/v1020_phase061/validate_phase061_step49.py",
        "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json",
        "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md",
        "Codex/work/v1020_phase061/audit_phase061_step50_review_artifacts.py",
        "Codex/work/v1020_phase061/validate_phase061_step50.py",
        "Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json",
        "Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json",
        "Codex/results/PHASE_061_STEP_050_REVIEW_ARTIFACT_RESULT.md",
        "Codex/work/v1020_phase061/build_phase061_step51_dispositions.py",
        "Codex/work/v1020_phase061/validate_phase061_step51_dispositions.py",
        "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json",
        "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json",
        "Codex/results/PHASE_061_STEP_051_1_DISPOSITION_RESULT.md",
        "Codex/work/v1020_phase061/validate_phase061_final.py",
        "Codex/results/PHASE_061_VALIDATION.json",
        "Codex/results/PHASE_061_V1020_LINEAGE_REPORT_D.md",
        "Codex/results/PHASE_061_STEP_051_2_GATE_RESULT.md",
        "Codex/results/PHASE_061_RESULT.md",
    ]
    record(checks, "PLAN_OUTPUT_CONTRACT", all(path in text for path in outputs), {path: path in text for path in outputs})
    normalized = normalized_lf_bytes(PLAN) if PLAN.exists() else b""
    return {
        "path": PLAN.relative_to(REPO).as_posix(),
        "lines": len(lines),
        "normalized_bytes": len(normalized),
        "normalized_sha256": sha256_bytes(normalized) if PLAN.exists() else None,
    }


def check_carry_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    carry59, stats59 = strict_load(CARRY_059)
    carry60, stats60 = strict_load(CARRY_060)
    disp60, stats_disp = strict_load(DISPOSITION_060)
    inherited = carry60["inherited_items"]
    new = carry60["new_blockers"]
    dispositions = disp60["dispositions"]
    summary = {
        "phase059_items": len(carry59["items"]),
        "inherited_items": len(inherited),
        "inherited_status_after": dict(sorted(Counter(row["status_after"] for row in inherited).items())),
        "inherited_target_phase061": sum(row["target_phase_after"] == 61 for row in inherited),
        "new_blockers": len(new),
        "new_status": dict(sorted(Counter(row["status"] for row in new).items())),
        "new_target_phase061": sum(row["target_phase"] == 61 for row in new),
        "phase060_dispositions": len(dispositions),
        "phase060_disposition_target061": sum(row["target_phase"] == 61 for row in dispositions),
    }
    expected = {
        "phase059_items": 52, "inherited_items": 52,
        "inherited_status_after": {"OPEN": 41, "PRESERVED_ACTIVE": 11},
        "inherited_target_phase061": 0, "new_blockers": 5, "new_status": {"OPEN": 5},
        "new_target_phase061": 0, "phase060_dispositions": 173,
        "phase060_disposition_target061": 36,
    }
    record(checks, "CARRY_FORWARD_BOUNDARY", summary == expected, {"actual": summary, "expected": expected})
    return {"summary": summary, "traversal": {"phase059": stats59, "phase060_delta": stats60, "phase060_dispositions": stats_disp}}


def check_controls(checks: list[dict[str, Any]]) -> dict[str, Any]:
    active = ACTIVE_LEDGER.read_text(encoding="utf-8") if ACTIVE_LEDGER.exists() else ""
    parent = PARENT_LEDGER.read_text(encoding="utf-8") if PARENT_LEDGER.exists() else ""
    handover = HANDOVER.read_text(encoding="utf-8") if HANDOVER.exists() else ""
    active_rows = [line for line in active.splitlines() if line.startswith("| 061 |")]
    parent_rows = [line for line in parent.splitlines() if line.startswith("| 061 |")]
    active_required = [
        "| IN_PROGRESS |", PLAN.relative_to(REPO).as_posix(), RESULT.relative_to(REPO).as_posix(),
        OUTPUT.relative_to(REPO).as_posix(), "PASS_P061_PLAN_ACTIVATION",
        "Step 46 after plan activation atomic commit/push/remote verification",
    ]
    parent_required = [
        "| IN_PROGRESS |", PLAN.relative_to(REPO).as_posix(), RESULT.relative_to(REPO).as_posix(),
        OUTPUT.relative_to(REPO).as_posix(), "PASS_P061_PLAN_ACTIVATION",
        "Step 46 after plan activation commit/push/remote verification",
    ]
    active_ok = len(active_rows) == 1 and all(token in active_rows[0] for token in active_required)
    parent_ok = len(parent_rows) == 1 and all(token in parent_rows[0] for token in parent_required)
    p060_checkpoint = (
        f"| Step 45.2 | `Codex/results/PHASE_060_STEP_045_2_GATE_RESULT.md`; `Codex/results/PHASE_060_RESULT.md` | `{EXPECTED_PARENT}` | pushed | yes |" in active
        and "PASS_P060_STEP45_2_PERSISTENCE" in active
    )
    handover_required = [
        f"활성 Phase 061 plan: `{PLAN.relative_to(REPO).as_posix()}`",
        "Phase 061 `IN_PROGRESS`, detailed-plan activation",
        f"현재 result: `{RESULT.relative_to(REPO).as_posix()}`",
        f"현재 machine evidence: `{OUTPUT.relative_to(REPO).as_posix()}`",
        EXPECTED_PARENT, "PASS_P060_STEP45_2_PERSISTENCE",
        "직전 Phase result: `Codex/results/PHASE_060_RESULT.md`",
        "직전 final Step result: `Codex/results/PHASE_060_STEP_045_2_GATE_RESULT.md`",
        "직전 scientific result: `Codex/results/PHASE_060_V1019_LINEAGE_REPORT_C.md`",
        "직전 integrated machine evidence: `Codex/results/PHASE_060_VALIDATION.json`",
        "carry-forward machine evidence: `Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json`",
        "exactly the seven Phase 061 plan-activation paths",
        "Step 46 is blocked until activation commit/push/remote verification passes",
    ]
    stale = [
        "Step 45.2 exact-eight checkpoint는 `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "Phase 061 detailed plan은 Phase 060 final gate 뒤 생성",
    ]
    handover_ok = all(token in handover for token in handover_required) and not any(token in handover for token in stale)
    record(checks, "CONTROL_ACTIVE_LEDGER", active_ok, {"rows": active_rows, "required": active_required})
    record(checks, "CONTROL_PARENT_LEDGER", parent_ok, {"rows": parent_rows, "required": parent_required})
    record(checks, "CONTROL_P060_PERSISTENCE", p060_checkpoint, EXPECTED_PARENT)
    record(checks, "CONTROL_HANDOVER", handover_ok, {"required": {token: token in handover for token in handover_required}, "stale": {token: token in handover for token in stale}})
    return {"active_ledger_phase061_rows": active_rows, "parent_ledger_phase061_rows": parent_rows, "handover_required": {token: token in handover for token in handover_required}}


def check_repository_precommit(checks: list[dict[str, Any]]) -> dict[str, Any]:
    branch = run_git("branch", "--show-current")
    head = run_git("rev-parse", "HEAD")
    upstream = run_git("rev-parse", "@{upstream}")
    origin_tracking = run_git("rev-parse", f"origin/{ACTIVE_BRANCH}")
    live_active = remote_tip(ACTIVE_BRANCH)
    protected_local = run_git("rev-parse", f"origin/{PROTECTED_BRANCH}")
    protected_live = remote_tip(PROTECTED_BRANCH)
    main_local = run_git("rev-parse", "origin/main")
    main_live = remote_tip("main")
    claude_tracked = run_git("diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude")
    claude_untracked = [path for path in porcelain_paths() if path.startswith("Claude/")]
    state = {
        "branch": branch, "head": head, "upstream": upstream,
        "origin_tracking": origin_tracking, "live_active": live_active,
        "protected_local": protected_local, "protected_live": protected_live,
        "main_local": main_local, "main_live": main_live,
        "claude_tracked": claude_tracked.splitlines() if claude_tracked else [],
        "claude_untracked": claude_untracked,
    }
    passed = (
        branch == ACTIVE_BRANCH and head == upstream == origin_tracking == live_active == EXPECTED_PARENT
        and protected_local == protected_live == EXPECTED_PROTECTED
        and main_local == main_live == EXPECTED_MAIN and not claude_tracked and not claude_untracked
    )
    record(checks, "REPOSITORY_PRECOMMIT_STATE", passed, state)
    dirty = activation_dirty_paths()
    record(checks, "EXACT_SEVEN_DIRTY_SET", dirty == EXACT_SEVEN_SET, {"actual": sorted(dirty), "missing": sorted(EXACT_SEVEN_SET - dirty), "unexpected": sorted(dirty - EXACT_SEVEN_SET)})
    tracked_phase061 = [path for path in run_git("ls-files", "Codex/results/PHASE_061*", "Codex/work/v1020_phase061/*").splitlines() if path.replace("\\", "/") not in EXACT_SEVEN_SET]
    dirty_step46 = [path for path in dirty if "STEP_046" in path or "V1020_SOURCE_TOPOLOGY" in path or "V1020_READ_ATTESTATION" in path or "step46" in path.lower()]
    record(checks, "NO_STEP46_EXECUTION", not tracked_phase061 and not dirty_step46, {"tracked": tracked_phase061, "dirty": dirty_step46})
    return {**state, "dirty_paths": sorted(dirty)}


def plan_diagnostics(text: str) -> set[str]:
    diagnostics: set[str] = set()
    executable = text[text.find("## Phase 061 — v1.0.20 Reaudit"):]
    headings = [line for line in executable.splitlines() if line.startswith("### Step ")]
    prefixes = ["### Step 46 ", "### Step 47 ", "### Step 48 ", "### Step 49 ", "### Step 50 ", "### Step 51.1 ", "### Step 51.2 "]
    if len(headings) != 7 or not all(row.startswith(prefix) for row, prefix in zip(headings, prefixes, strict=True)):
        diagnostics.add("PLAN_STEPS")
    token_contract = {
        "PLAN_GATE": "PASS_P061_LINEAGE_D",
        "PLAN_SUBJECT": EXPECTED_SUBJECT,
        "PLAN_DRAFT_BOUNDARY": "competing draft",
        "PLAN_ADOPTED_BOUNDARY": "adopted release",
        "PLAN_PHASE062_BLOCK": "Phase 062 Step 52 may not begin",
        "PLAN_SOURCE_COUNT": "232 path occurrences, 231 unique Git blobs",
        "PLAN_PDF_COUNT": "14 files / 130 pages",
    }
    for code, token in token_contract.items():
        if token not in text:
            diagnostics.add(code)
    return diagnostics


def manifest_summary_diagnostics(summary: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    expected = {
        "MANIFEST_PATH_COUNT": ("paths", 232),
        "MANIFEST_BLOB_COUNT": ("unique_blobs", 231),
        "MANIFEST_LINE_COUNT": ("text_lines", 31553),
        "MANIFEST_NONBLANK_COUNT": ("text_nonblank_lines", 29335),
        "MANIFEST_PAGE_COUNT": ("pdf_pages", 130),
        "MANIFEST_FRAME_COUNT": ("image_frames", 23),
        "MANIFEST_TOTAL_BYTES": ("total_bytes", 8158832),
    }
    for code, (key, value) in expected.items():
        if summary.get(key) != value:
            diagnostics.add(code)
    mode_expected = {"FULL_IMAGE": 23, "FULL_PDF": 14, "FULL_TEXT": 195}
    if summary.get("mode_counts") != mode_expected:
        diagnostics.add("MANIFEST_MODE_COUNTS")
    expected_duplicate = [{
        "blob_sha1": "8dfea239d1787582c6c37c41fe6d06f7b204d72b",
        "paths": [
            "Claude/docs/v1.0.20/results/snapshot_v1020_p5.json",
            "Claude/docs/v1.0.20/results/snapshot_v1020_p6.json",
        ],
    }]
    if summary.get("duplicate_groups") != expected_duplicate:
        diagnostics.add("MANIFEST_DUPLICATE_GROUP")
    return diagnostics


def source_record_diagnostics(record_value: dict[str, Any], reference: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    field_codes = {
        "path": "SOURCE_PATH", "blob_sha1": "SOURCE_BLOB", "git_mode": "SOURCE_MODE",
        "size_bytes": "SOURCE_SIZE", "review_mode": "SOURCE_REVIEW_MODE",
        "role": "SOURCE_ROLE", "extent": "SOURCE_EXTENT",
    }
    for field, code in field_codes.items():
        if record_value.get(field) != reference.get(field):
            diagnostics.add(code)
    steps = set(record_value.get("scheduled_steps", []))
    if not {"46", "51.1"}.issubset(steps) or not steps & {"47", "48", "49", "50"}:
        diagnostics.add("SOURCE_STEP_OWNER")
    return diagnostics


def dirty_set_diagnostics(paths: set[str]) -> set[str]:
    return set() if paths == EXACT_SEVEN_SET else {"DIRTY_EXACT_SET"}


def git_contract_diagnostics(parent: str, subject: str, protected: str, main: str) -> set[str]:
    diagnostics: set[str] = set()
    if parent != EXPECTED_PARENT:
        diagnostics.add("GIT_PARENT")
    if subject != EXPECTED_SUBJECT:
        diagnostics.add("GIT_SUBJECT")
    if protected != EXPECTED_PROTECTED:
        diagnostics.add("GIT_PROTECTED")
    if main != EXPECTED_MAIN:
        diagnostics.add("GIT_MAIN")
    return diagnostics


def gate_diagnostics(selected: set[str]) -> set[str]:
    allowed = {"PASS_P061_LINEAGE_D", "CONDITIONAL_P061", "FAIL_P061"}
    return set() if len(selected) == 1 and selected.issubset(allowed) else {"GATE_EXCLUSIVE"}


def run_negative_controls(plan_text: str, manifest_contract: dict[str, Any]) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    def add(case_id: str, expected_code: str, observed: set[str]) -> None:
        cases.append({
            "case_id": case_id,
            "expected_code": expected_code,
            "observed_codes": sorted(observed),
            "passed": observed == {expected_code},
        })
    try:
        strict_load_bytes(b'{"a":1,"a":2}')
        add("NEG_DUPLICATE_KEY", "JSON_DUPLICATE_KEY", set())
    except DuplicateKeyError:
        add("NEG_DUPLICATE_KEY", "JSON_DUPLICATE_KEY", {"JSON_DUPLICATE_KEY"})
    try:
        strict_load_bytes(b'{"a":NaN}')
        add("NEG_NONFINITE", "JSON_NONFINITE", set())
    except NonFiniteNumberError:
        add("NEG_NONFINITE", "JSON_NONFINITE", {"JSON_NONFINITE"})

    plan_mutations = {
        "NEG_PLAN_STEPS": ("### Step 46 ", "PLAN_STEPS"),
        "NEG_PLAN_GATE": ("PASS_P061_LINEAGE_D", "PLAN_GATE"),
        "NEG_PLAN_SUBJECT": (EXPECTED_SUBJECT, "PLAN_SUBJECT"),
        "NEG_PLAN_DRAFT": ("competing draft", "PLAN_DRAFT_BOUNDARY"),
        "NEG_PLAN_ADOPTED": ("adopted release", "PLAN_ADOPTED_BOUNDARY"),
        "NEG_PLAN_PHASE062": ("Phase 062 Step 52 may not begin", "PLAN_PHASE062_BLOCK"),
        "NEG_PLAN_SOURCE_COUNT": ("232 path occurrences, 231 unique Git blobs", "PLAN_SOURCE_COUNT"),
        "NEG_PLAN_PDF_COUNT": ("14 files / 130 pages", "PLAN_PDF_COUNT"),
    }
    for case_id, (token, expected_code) in plan_mutations.items():
        mutated = plan_text.replace(token, f"MUTATED_{case_id}")
        add(case_id, expected_code, plan_diagnostics(mutated))

    summary = manifest_contract["summary"]
    summary_mutations = {
        "NEG_MANIFEST_PATH_COUNT": ("paths", "MANIFEST_PATH_COUNT"),
        "NEG_MANIFEST_BLOB_COUNT": ("unique_blobs", "MANIFEST_BLOB_COUNT"),
        "NEG_MANIFEST_LINE_COUNT": ("text_lines", "MANIFEST_LINE_COUNT"),
        "NEG_MANIFEST_NONBLANK_COUNT": ("text_nonblank_lines", "MANIFEST_NONBLANK_COUNT"),
        "NEG_MANIFEST_PAGE_COUNT": ("pdf_pages", "MANIFEST_PAGE_COUNT"),
        "NEG_MANIFEST_FRAME_COUNT": ("image_frames", "MANIFEST_FRAME_COUNT"),
        "NEG_MANIFEST_TOTAL_BYTES": ("total_bytes", "MANIFEST_TOTAL_BYTES"),
    }
    for case_id, (field, expected_code) in summary_mutations.items():
        mutated = copy.deepcopy(summary)
        mutated[field] += 1
        add(case_id, expected_code, manifest_summary_diagnostics(mutated))
    mutated = copy.deepcopy(summary)
    mutated["mode_counts"]["FULL_TEXT"] += 1
    add("NEG_MANIFEST_MODE_COUNTS", "MANIFEST_MODE_COUNTS", manifest_summary_diagnostics(mutated))
    mutated = copy.deepcopy(summary)
    mutated["duplicate_groups"][0]["blob_sha1"] = "0" * 40
    add("NEG_MANIFEST_DUPLICATE_GROUP", "MANIFEST_DUPLICATE_GROUP", manifest_summary_diagnostics(mutated))

    reference = manifest_contract["records"][0]
    record_mutations: dict[str, tuple[str, Any, str]] = {
        "NEG_SOURCE_PATH": ("path", reference["path"] + ".mutated", "SOURCE_PATH"),
        "NEG_SOURCE_BLOB": ("blob_sha1", "0" * 40, "SOURCE_BLOB"),
        "NEG_SOURCE_MODE": ("git_mode", "100755", "SOURCE_MODE"),
        "NEG_SOURCE_SIZE": ("size_bytes", reference["size_bytes"] + 1, "SOURCE_SIZE"),
        "NEG_SOURCE_REVIEW_MODE": ("review_mode", "FULL_IMAGE", "SOURCE_REVIEW_MODE"),
        "NEG_SOURCE_ROLE": ("role", "mutated", "SOURCE_ROLE"),
        "NEG_SOURCE_EXTENT": ("extent", {"lines": -1, "encoding_check": "utf-8"}, "SOURCE_EXTENT"),
        "NEG_SOURCE_STEP_OWNER": ("scheduled_steps", ["47"], "SOURCE_STEP_OWNER"),
    }
    for case_id, (field, value, expected_code) in record_mutations.items():
        mutated = copy.deepcopy(reference)
        mutated[field] = value
        add(case_id, expected_code, source_record_diagnostics(mutated, reference))

    dirty_missing = EXACT_SEVEN_SET - {EXACT_SEVEN[0]}
    add("NEG_DIRTY_MISSING", "DIRTY_EXACT_SET", dirty_set_diagnostics(dirty_missing))
    dirty_extra = EXACT_SEVEN_SET | {"Codex/work/v1020_phase061/unexpected.tmp"}
    add("NEG_DIRTY_EXTRA", "DIRTY_EXACT_SET", dirty_set_diagnostics(dirty_extra))
    add("NEG_PARENT", "GIT_PARENT", git_contract_diagnostics(EXPECTED_PARENT[:-1] + "0", EXPECTED_SUBJECT, EXPECTED_PROTECTED, EXPECTED_MAIN))
    add("NEG_SUBJECT", "GIT_SUBJECT", git_contract_diagnostics(EXPECTED_PARENT, EXPECTED_SUBJECT + " mutated", EXPECTED_PROTECTED, EXPECTED_MAIN))
    add("NEG_PROTECTED", "GIT_PROTECTED", git_contract_diagnostics(EXPECTED_PARENT, EXPECTED_SUBJECT, EXPECTED_PROTECTED[:-1] + "0", EXPECTED_MAIN))
    add("NEG_MAIN", "GIT_MAIN", git_contract_diagnostics(EXPECTED_PARENT, EXPECTED_SUBJECT, EXPECTED_PROTECTED, EXPECTED_MAIN[:-1] + "0"))
    add("NEG_GATE_EXCLUSIVE", "GATE_EXCLUSIVE", gate_diagnostics({"PASS_P061_LINEAGE_D", "FAIL_P061"}))
    return {
        "total": len(cases), "passed": sum(row["passed"] for row in cases),
        "failed": [row["case_id"] for row in cases if not row["passed"]],
        "cases": cases,
    }


def nonself_hashes() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for relative in NONSELF_SURFACES:
        path = REPO / relative
        normalized = normalized_lf_bytes(path) if path.exists() else b""
        result[relative] = {
            "exists": path.exists(),
            "normalized_bytes": len(normalized) if path.exists() else None,
            "normalized_sha256": sha256_bytes(normalized) if path.exists() else None,
        }
    return result


def deterministic_projection(
    plan_contract: dict[str, Any],
    manifest_contract: dict[str, Any],
    carry_contract: dict[str, Any],
    negative_case_ids: list[str],
) -> dict[str, Any]:
    return {
        "plan": plan_contract,
        "manifest_sha256": manifest_contract["manifest_sha256"],
        "manifest_summary": manifest_contract["summary"],
        "path_set_sha256": manifest_contract["path_set_sha256"],
        "path_blob_set_sha256": manifest_contract["path_blob_set_sha256"],
        "carry": carry_contract["summary"],
        "exact_seven": EXACT_SEVEN,
        "negative_codes": negative_case_ids,
    }


def build_payload() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    plan_contract = check_plan(checks)
    manifest_contract = collect_manifest_contract(checks)
    carry_contract = check_carry_contract(checks)
    control_contract = check_controls(checks)
    repository_state = check_repository_precommit(checks)
    record(checks, "ACTIVATION_RESULT_EXISTS", RESULT.exists(), RESULT.relative_to(REPO).as_posix())
    hashes = nonself_hashes()
    record(checks, "NONSELF_SURFACES_EXIST", all(item["exists"] for item in hashes.values()), hashes)
    negatives = run_negative_controls(PLAN.read_text(encoding="utf-8") if PLAN.exists() else "", manifest_contract)
    record(checks, "NEGATIVE_CONTROLS", negatives["passed"] == negatives["total"] and negatives["total"] >= 20, negatives)
    negative_case_ids = [row["case_id"] for row in negatives["cases"]]
    first_projection = deterministic_projection(plan_contract, manifest_contract, carry_contract, negative_case_ids)
    fresh_checks: list[dict[str, Any]] = []
    fresh_plan = check_plan(fresh_checks)
    fresh_manifest = collect_manifest_contract(fresh_checks)
    fresh_carry = check_carry_contract(fresh_checks)
    second_projection = deterministic_projection(fresh_plan, fresh_manifest, fresh_carry, negative_case_ids)
    first = canonical_bytes(first_projection)
    second = canonical_bytes(second_projection)
    fresh_failures = [row["code"] for row in fresh_checks if not row["passed"]]
    determinism = {
        "runs": 2,
        "independent_reconstruction": True,
        "byte_identical": first == second,
        "sha256_run1": sha256_bytes(first),
        "sha256_run2": sha256_bytes(second),
        "fresh_reconstruction_checks_total": len(fresh_checks),
        "fresh_reconstruction_failed_codes": fresh_failures,
    }
    record(checks, "DETERMINISM_2_OF_2", determinism["byte_identical"] and not fresh_failures, determinism)
    failed = [row["code"] for row in checks if not row["passed"]]
    payload: dict[str, Any] = {
        "schema_version": 2,
        "generated_date": "2026-08-26",
        "phase": 61,
        "unit": "PLAN_ACTIVATION",
        "gate": "PASS_P061_PLAN_ACTIVATION" if not failed else "FAIL_P061_PLAN_ACTIVATION",
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "exact_allowlist": EXACT_SEVEN,
        "plan_contract": plan_contract,
        "manifest_contract": manifest_contract,
        "carry_contract": carry_contract,
        "control_contract": control_contract,
        "repository_state": repository_state,
        "artifact_hashes_nonself": hashes,
        "checks": checks,
        "negative_controls": negatives,
        "determinism": determinism,
        "summary": {"checks_total": len(checks), "checks_passed": len(checks) - len(failed), "checks_failed": len(failed), "failed_codes": failed},
    }
    semantic = copy.deepcopy(payload)
    payload["semantic_sha256"] = sha256_bytes(canonical_bytes(semantic))
    return payload


def validate_semantic_hash(payload: dict[str, Any]) -> bool:
    expected = payload.get("semantic_sha256")
    projection = copy.deepcopy(payload)
    projection.pop("semantic_sha256", None)
    return isinstance(expected, str) and expected == sha256_bytes(canonical_bytes(projection))


def validate_stored() -> int:
    if not OUTPUT.exists():
        print("FAIL STORED_ARTIFACT_MISSING")
        return 1
    stored, _ = strict_load(OUTPUT)
    current = build_payload()
    if not validate_semantic_hash(stored):
        print("FAIL STORED_SEMANTIC_HASH")
        return 1
    if stored != current:
        print("FAIL STORED_CURRENT_MISMATCH")
        return 1
    if stored.get("gate") != "PASS_P061_PLAN_ACTIVATION":
        print(f"FAIL STORED_GATE {stored.get('gate')}")
        return 1
    print(f"PASS_P061_PLAN_ACTIVATION {stored['summary']['checks_passed']}/{stored['summary']['checks_total']}")
    return 0


def verify_staged() -> int:
    if validate_stored() != 0:
        return 1
    staged = nul_paths("diff", "--cached", "--name-only", "-z")
    unstaged = nul_paths("diff", "--name-only", "-z")
    dirty = activation_dirty_paths()
    ok = staged == EXACT_SEVEN_SET and not unstaged and dirty == EXACT_SEVEN_SET
    if not ok:
        print(f"FAIL STAGED_EXACT_SEVEN staged={sorted(staged)} unstaged={sorted(unstaged)} dirty={sorted(dirty)}")
        return 1
    print("PASS_P061_PLAN_ACTIVATION_STAGED 7/7")
    return 0


def verify_persistence() -> int:
    if not OUTPUT.exists():
        print("FAIL PERSISTENCE_ARTIFACT_MISSING")
        return 1
    stored, _ = strict_load(OUTPUT)
    failures: list[str] = []
    if not validate_semantic_hash(stored) or stored.get("gate") != "PASS_P061_PLAN_ACTIVATION":
        failures.append("PERSISTENCE_STORED_ARTIFACT")
    for relative, expected in stored.get("artifact_hashes_nonself", {}).items():
        path = REPO / relative
        actual = normalized_lf_bytes(path) if path.exists() else b""
        if (
            not path.exists()
            or sha256_bytes(actual) != expected.get("normalized_sha256")
            or len(actual) != expected.get("normalized_bytes")
        ):
            failures.append(f"PERSISTENCE_SURFACE_HASH:{relative}")
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
        failures.append("PERSISTENCE_PARENT")
    if subject != EXPECTED_SUBJECT:
        failures.append("PERSISTENCE_SUBJECT")
    if committed != EXACT_SEVEN_SET:
        failures.append("PERSISTENCE_EXACT_SEVEN")
    if porcelain_paths():
        failures.append("PERSISTENCE_DIRTY")
    if not (branch == ACTIVE_BRANCH and head == upstream == origin_tracking == live_active):
        failures.append("PERSISTENCE_ACTIVE_REMOTE")
    if protected_local != protected_live or protected_live != EXPECTED_PROTECTED:
        failures.append("PERSISTENCE_PROTECTED")
    if main_local != main_live or main_live != EXPECTED_MAIN:
        failures.append("PERSISTENCE_MAIN")
    if claude_diff:
        failures.append("PERSISTENCE_CLAUDE")
    if run_git("diff", "--check"):
        failures.append("PERSISTENCE_DIFF_CHECK")
    if failures:
        print("FAIL " + " ".join(failures))
        return 1
    print(f"PASS_P061_PLAN_ACTIVATION_PERSISTENCE head={head}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    if args.verify_persistence:
        return verify_persistence()
    if args.verify_staged:
        return verify_staged()
    if args.collect:
        payload = build_payload()
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(pretty_bytes(payload))
        failed = payload["summary"]["failed_codes"]
        if failed:
            print("FAIL " + " ".join(failed))
            print(f"FAIL_P061_PLAN_ACTIVATION {payload['summary']['checks_passed']}/{payload['summary']['checks_total']}")
            return 1
        print(f"PASS_P061_PLAN_ACTIVATION {payload['summary']['checks_passed']}/{payload['summary']['checks_total']}")
        return 0
    result = validate_stored()
    if result == 0 and args.run_negative_probes:
        stored, _ = strict_load(OUTPUT)
        neg = stored["negative_controls"]
        print(f"PASS_P061_PLAN_NEGATIVE_CONTROLS {neg['passed']}/{neg['total']}")
    if result == 0 and args.determinism_check:
        stored, _ = strict_load(OUTPUT)
        det = stored["determinism"]
        print(f"PASS_P061_PLAN_DETERMINISM {det['runs']}/{det['runs']}")
    return result


if __name__ == "__main__":
    sys.exit(main())
