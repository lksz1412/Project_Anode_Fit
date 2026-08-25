#!/usr/bin/env python3
"""Validate the Phase 060 v1.0.19 detailed-plan activation boundary."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


REPO = Path(__file__).resolve().parents[3]
PLAN = REPO / "Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md"
RESULT = REPO / "Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md"
OUTPUT = REPO / "Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROTECTED = "origin/codex/lib-physics-endgame-v1025_2"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

SUPPLEMENTARY_PATHS = [
    "Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md",
    "Claude/results/process/V1019_ASSET_CHECKLIST.md",
    "Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md",
    "Claude/results/process/V1019_CH2_FABLE_BRIEF.md",
    "Claude/results/process/V1019_CH2_UNION_DEFECTS.md",
    "Claude/results/process/V1019_CODE_FABLE_BRIEF.md",
    "Claude/results/process/V1019_CONTINUITY_JUDGMENT.md",
    "Claude/results/process/V1019_EXECUTION_LEDGER.md",
    "Claude/results/process/V1019_FABLE_BRIEF.md",
    "Claude/results/process/V1019_FINAL_REVIEW_UNION.md",
    "Claude/results/process/V1019_UNION_DEFECTS.md",
]

CROSS_WITNESS_PATHS = [
    "Claude/docs/v1.0.20/figs/graph_suite_v1019.png",
    "Claude/docs/v1.0.20/results/snapshot_v1019_baseline.json",
]

PLAN_ACTIVATION_PATHS = {
    "Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md",
    "Codex/work/v1019_phase060/validate_phase060_plan.py",
    "Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json",
    "Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
}


class DuplicateKeyError(ValueError):
    pass


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_pairs)


def run_git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_blob(path: str) -> tuple[str, bytes]:
    row = run_git("ls-tree", BASELINE, "--", path)
    if not row:
        raise FileNotFoundError(path)
    blob = row.split()[2]
    proc = subprocess.run(
        ["git", "cat-file", "blob", blob],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return blob, proc.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[dict[str, Any]] = []


def record(check_id: str, passed: bool, evidence: Any) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})


def main() -> int:
    plan_text = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    plan_lines = plan_text.splitlines()

    required_sections = [
        "## Summary",
        "## Current Ground Truth",
        "## Phase Range",
        "## Exact Read Inputs",
        "## Non-goals and Scope Guards",
        "## Implementation Changes",
        "## Plan Activation Unit — Save Before Step 40",
        "## Phase 060 — v1.0.19 Reaudit",
        "## Phase Gate",
        "## Implementation Interfaces",
        "## Test and Validation Plan",
        "## Stop Conditions",
        "## Assumptions",
        "## Correction History",
    ]
    positions = [plan_text.find(section) for section in required_sections]
    record("plan_exists", PLAN.exists(), PLAN.relative_to(REPO).as_posix())
    record("plan_utf8_lf", "\r" not in plan_text, {"lines": len(plan_lines)})
    record(
        "required_sections_ordered",
        all(position >= 0 for position in positions)
        and positions == sorted(positions)
        and len(set(positions)) == len(positions),
        {"sections": required_sections, "positions": positions},
    )

    step_headings = [
        line
        for line in plan_lines
        if line.startswith("### Step 4") and " — " in line
    ]
    expected_step_prefixes = [
        "### Step 40 ",
        "### Step 41 ",
        "### Step 42 ",
        "### Step 43 ",
        "### Step 44 ",
        "### Step 45.1 ",
        "### Step 45.2 ",
    ]
    record(
        "cumulative_step_headings",
        len(step_headings) == len(expected_step_prefixes)
        and all(
            heading.startswith(prefix)
            for heading, prefix in zip(step_headings, expected_step_prefixes, strict=True)
        ),
        step_headings,
    )
    record(
        "no_step_restart",
        "### Step 1 " not in plan_text and "Steps 1–" not in plan_text,
        "Phase 060 begins at cumulative Step 40",
    )

    required_phrases = [
        "77 paths, 77 unique blobs",
        "60 text files/8,784 physical lines/8,025 nonblank lines",
        "61 text files/9,904 physical lines/9,145 nonblank lines",
        "3 files / 95 pages",
        "13 unique images",
        "PASS_P060_LINEAGE_C",
        "CONDITIONAL_P060",
        "FAIL_P060",
        "atomic commit",
        "push and remote-tip verification",
        "external material validation",
        "Step 46 may not begin before that plan is saved and reviewed",
    ]
    record(
        "required_policy_phrases",
        all(phrase in plan_text for phrase in required_phrases),
        {phrase: phrase in plan_text for phrase in required_phrases},
    )

    manifest = strict_json(MANIFEST)
    release = [entry for entry in manifest["entries"] if entry["version"] == "v1.0.19"]
    release_blobs = {entry["blob_sha"] for entry in release}
    mode_counts = Counter(entry["review_mode"] for entry in release)
    role_counts = Counter(entry["role"] for entry in release)
    text_lines = sum(
        entry["extent"]["lines"]
        for entry in release
        if entry["review_mode"] == "FULL_TEXT"
    )
    release_nonblank_lines = 0
    release_blob_mismatches: list[str] = []
    for entry in release:
        if entry["review_mode"] != "FULL_TEXT":
            continue
        actual_blob, data = git_blob(entry["path"])
        if actual_blob != entry["blob_sha"]:
            release_blob_mismatches.append(entry["path"])
        release_nonblank_lines += sum(
            bool(line.strip()) for line in data.decode("utf-8").splitlines()
        )
    pdf_pages = sum(
        entry["extent"]["pages"]
        for entry in release
        if entry["review_mode"] == "FULL_PDF"
    )
    release_summary = {
        "paths": len(release),
        "unique_blobs": len(release_blobs),
        "mode_counts": dict(sorted(mode_counts.items())),
        "role_counts": dict(sorted(role_counts.items())),
        "text_lines": text_lines,
        "text_nonblank_lines": release_nonblank_lines,
        "blob_mismatches": release_blob_mismatches,
        "pdf_pages": pdf_pages,
    }
    record(
        "release_manifest_counts",
        release_summary
        == {
            "paths": 66,
            "unique_blobs": 66,
            "mode_counts": {
                "BINARY_INTROSPECTION": 1,
                "FULL_IMAGE": 13,
                "FULL_PDF": 3,
                "FULL_TEXT": 49,
            },
            "role_counts": {
                "code": 1,
                "data": 1,
                "demo": 2,
                "figure": 14,
                "generated_document": 3,
                "implementation_guide": 1,
                "result": 2,
                "test": 1,
                "theory": 41,
            },
            "text_lines": 7756,
            "text_nonblank_lines": 7136,
            "blob_mismatches": [],
            "pdf_pages": 95,
        },
        release_summary,
    )

    supplementary: list[dict[str, Any]] = []
    supplementary_blobs: set[str] = set()
    supplementary_lines = 0
    supplementary_nonblank_lines = 0
    supplementary_bytes = 0
    for path in SUPPLEMENTARY_PATHS:
        blob, data = git_blob(path)
        supplementary_blobs.add(blob)
        decoded_lines = data.decode("utf-8").splitlines()
        supplementary_lines += len(decoded_lines)
        supplementary_nonblank_lines += sum(bool(line.strip()) for line in decoded_lines)
        supplementary_bytes += len(data)
        supplementary.append(
            {
                "path": path,
                "blob_sha1": blob,
                "lines": len(data.decode("utf-8").splitlines()),
                "bytes": len(data),
            }
        )
    record(
        "supplementary_inventory",
        len(supplementary) == 11
        and len(supplementary_blobs) == 11
        and supplementary_lines == 1028
        and supplementary_nonblank_lines == 889
        and supplementary_bytes == 148934,
        {
            "paths": len(supplementary),
            "unique_blobs": len(supplementary_blobs),
            "lines": supplementary_lines,
            "nonblank_lines": supplementary_nonblank_lines,
            "bytes": supplementary_bytes,
            "records": supplementary,
        },
    )

    witness_entries = {
        entry["path"]: entry
        for entry in manifest["entries"]
        if entry["path"] in CROSS_WITNESS_PATHS
    }
    release_graph_blob = next(
        entry["blob_sha"]
        for entry in release
        if entry["path"] == "Claude/docs/v1.0.19/figs/graph_suite_v1019.png"
    )
    snapshot = witness_entries.get(CROSS_WITNESS_PATHS[1], {})
    duplicate_graph = witness_entries.get(CROSS_WITNESS_PATHS[0], {})
    _, snapshot_data = git_blob(CROSS_WITNESS_PATHS[1])
    snapshot_lines = snapshot_data.decode("utf-8").splitlines()
    snapshot_nonblank_lines = sum(bool(line.strip()) for line in snapshot_lines)
    record(
        "cross_witness_boundary",
        set(witness_entries) == set(CROSS_WITNESS_PATHS)
        and duplicate_graph.get("blob_sha") == release_graph_blob
        and snapshot.get("version") == "v1.0.20"
        and snapshot.get("extent", {}).get("lines") == 1120
        and len(snapshot_lines) == 1120
        and snapshot_nonblank_lines == 1120,
        {
            "occurrences": len(witness_entries),
            "new_unique_blobs": len(
                {entry["blob_sha"] for entry in witness_entries.values()} - release_blobs
            ),
            "duplicate_graph_blob": duplicate_graph.get("blob_sha"),
            "snapshot_lines": snapshot.get("extent", {}).get("lines"),
            "snapshot_nonblank_lines": snapshot_nonblank_lines,
        },
    )

    listed_paths = {
        line[3:-1]
        for line in plan_lines
        if line.startswith("- `") and line.endswith("`")
    }
    release_paths = {entry["path"] for entry in release}
    record(
        "exact_source_paths_listed",
        release_paths.issubset(listed_paths)
        and set(SUPPLEMENTARY_PATHS).issubset(listed_paths)
        and set(CROSS_WITNESS_PATHS).issubset(listed_paths),
        {
            "release_listed": len(release_paths & listed_paths),
            "release_expected": len(release_paths),
            "supplementary_listed": len(set(SUPPLEMENTARY_PATHS) & listed_paths),
            "supplementary_expected": len(SUPPLEMENTARY_PATHS),
            "witness_listed": len(set(CROSS_WITNESS_PATHS) & listed_paths),
            "witness_expected": len(CROSS_WITNESS_PATHS),
        },
    )

    planned_outputs = [
        "Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md",
        "Codex/results/PHASE_060_STEP_040_SOURCE_TOPOLOGY_RESULT.md",
        "Codex/results/PHASE_060_STEP_041_PROCESS_AUTHORITY_RESULT.md",
        "Codex/results/PHASE_060_STEP_042_RUNTIME_ARTIFACT_RESULT.md",
        "Codex/results/PHASE_060_STEP_043_DOC_CODE_CONFORMANCE_RESULT.md",
        "Codex/results/PHASE_060_STEP_044_PHYSICS_REDERIVATION_RESULT.md",
        "Codex/results/PHASE_060_STEP_045_1_DISPOSITION_RESULT.md",
        "Codex/results/PHASE_060_STEP_045_2_GATE_RESULT.md",
        "Codex/results/PHASE_060_RESULT.md",
        "Codex/results/PHASE_060_V1019_LINEAGE_REPORT_C.md",
        "Codex/results/PHASE_060_VALIDATION.json",
    ]
    record(
        "planned_result_paths",
        all(path in plan_text for path in planned_outputs),
        {path: path in plan_text for path in planned_outputs},
    )

    control_texts = {
        "active_ledger": ACTIVE_LEDGER.read_text(encoding="utf-8")
        if ACTIVE_LEDGER.exists()
        else "",
        "parent_ledger": PARENT_LEDGER.read_text(encoding="utf-8")
        if PARENT_LEDGER.exists()
        else "",
        "handover": HANDOVER.read_text(encoding="utf-8") if HANDOVER.exists() else "",
    }
    active_phase060_rows = [
        line
        for line in control_texts["active_ledger"].splitlines()
        if line.startswith("| 060 |")
    ]
    parent_phase060_rows = [
        line
        for line in control_texts["parent_ledger"].splitlines()
        if line.startswith("| 060 |")
    ]
    active_row_required = [
        "| IN_PROGRESS |",
        "Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md",
        "Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md",
        "Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json",
        "PASS_P060_PLAN_ACTIVATION",
        "Step 40 after plan activation atomic commit/push/remote verification",
    ]
    parent_row_required = [
        "| IN_PROGRESS |",
        "Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md",
        "Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md",
        "Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json",
        "PASS_P060_PLAN_ACTIVATION",
        "Step 40 after plan activation commit/push/remote verification",
    ]
    active_row_ok = len(active_phase060_rows) == 1 and all(
        token in active_phase060_rows[0] for token in active_row_required
    )
    parent_row_ok = len(parent_phase060_rows) == 1 and all(
        token in parent_phase060_rows[0] for token in parent_row_required
    )
    handover_required = [
        "5. 활성 Phase 060 plan: `Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md`",
        "13. 현재 Phase 상태: Phase 060 `IN_PROGRESS`, detailed-plan activation",
        "14. 현재 result: `Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md`",
        "15. 현재 machine evidence: `Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json`",
        "## Exact Next Action",
        "exactly the seven Phase 060 plan-activation paths",
        "execute Phase 060 Step 40 from the active detailed plan",
    ]
    stale_handover_phrases = [
        "Phase 060 detailed plan 미작성",
        "five Step 39.6 control documents require",
        "A Phase 060 detailed plan has not yet been created",
    ]
    handover_ok = all(
        token in control_texts["handover"] for token in handover_required
    ) and not any(
        token in control_texts["handover"] for token in stale_handover_phrases
    )
    record(
        "control_documents_activated",
        RESULT.exists()
        and active_row_ok
        and parent_row_ok
        and handover_ok,
        {
            "result_exists": RESULT.exists(),
            "active_phase060_row": {
                "count": len(active_phase060_rows),
                "required_tokens": {
                    token: len(active_phase060_rows) == 1
                    and token in active_phase060_rows[0]
                    for token in active_row_required
                },
            },
            "parent_phase060_row": {
                "count": len(parent_phase060_rows),
                "required_tokens": {
                    token: len(parent_phase060_rows) == 1
                    and token in parent_phase060_rows[0]
                    for token in parent_row_required
                },
            },
            "handover_required_tokens": {
                token: token in control_texts["handover"] for token in handover_required
            },
            "handover_stale_phrases": {
                token: token in control_texts["handover"]
                for token in stale_handover_phrases
            },
        },
    )

    current_branch = run_git("branch", "--show-current")
    head_tip = run_git("rev-parse", "HEAD")
    upstream_tip = run_git("rev-parse", "@{upstream}")
    remote_row = run_git("ls-remote", "--heads", "origin", ACTIVE_BRANCH)
    remote_parts = remote_row.split()
    remote_active_tip = remote_parts[0] if len(remote_parts) == 2 else ""
    protected_tip = run_git("rev-parse", PROTECTED)
    main_tip = run_git("rev-parse", "origin/main")
    claude_diff = run_git("diff", "--name-only", PROTECTED, "--", "Claude")
    record(
        "git_protection_state",
        current_branch == ACTIVE_BRANCH
        and head_tip == upstream_tip == remote_active_tip
        and protected_tip == EXPECTED_PROTECTED
        and main_tip == EXPECTED_MAIN
        and not claude_diff,
        {
            "branch": current_branch,
            "head": head_tip,
            "upstream": upstream_tip,
            "origin_active": remote_active_tip,
            "protected": protected_tip,
            "main": main_tip,
            "claude_diff_paths": claude_diff.splitlines() if claude_diff else [],
        },
    )

    status_proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status_proc.returncode != 0:
        raise RuntimeError(f"git status failed: {status_proc.stderr.strip()}")
    dirty_lines = status_proc.stdout.splitlines()
    dirty_paths = {
        line[3:].replace("\\", "/") for line in dirty_lines if len(line) >= 4
    }
    unexpected_dirty = sorted(dirty_paths - PLAN_ACTIVATION_PATHS)
    missing_dirty = sorted(PLAN_ACTIVATION_PATHS - dirty_paths)
    record(
        "plan_activation_exact_dirty_set",
        dirty_paths == PLAN_ACTIVATION_PATHS,
        {
            "dirty_paths": sorted(dirty_paths),
            "allowed_paths": sorted(PLAN_ACTIVATION_PATHS),
            "unexpected_paths": unexpected_dirty,
            "missing_paths": missing_dirty,
        },
    )

    passed = sum(1 for item in checks if item["passed"])
    failed = [item for item in checks if not item["passed"]]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-08-25",
        "phase": 60,
        "unit": "PLAN_ACTIVATION",
        "plan_path": PLAN.relative_to(REPO).as_posix(),
        "plan_lines": len(plan_lines),
        "plan_bytes": len(PLAN.read_bytes()) if PLAN.exists() else 0,
        "plan_sha256": sha256(PLAN) if PLAN.exists() else None,
        "baseline_commit": BASELINE,
        "counts": {
            "checks_total": len(checks),
            "checks_passed": passed,
            "checks_failed": len(failed),
            "release_paths": len(release),
            "release_unique_blobs": len(release_blobs),
            "primary_paths": len(release) + len(supplementary),
            "primary_unique_blobs": len(release_blobs | supplementary_blobs),
            "primary_text_lines": text_lines + supplementary_lines,
            "primary_text_nonblank_lines": release_nonblank_lines
            + supplementary_nonblank_lines,
            "witness_occurrences": len(witness_entries),
            "inspection_unique_blobs": len(
                release_blobs
                | supplementary_blobs
                | {entry["blob_sha"] for entry in witness_entries.values()}
            ),
            "inspection_text_lines": text_lines
            + supplementary_lines
            + len(snapshot_lines),
            "inspection_text_nonblank_lines": release_nonblank_lines
            + supplementary_nonblank_lines
            + snapshot_nonblank_lines,
        },
        "checks": checks,
        "status": "PASS_P060_PLAN_ACTIVATION" if not failed else "FAIL_P060_PLAN_ACTIVATION",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    if failed:
        for item in failed:
            print(f"FAIL {item['check_id']}: {item['evidence']}")
        print(f"FAIL_P060_PLAN_ACTIVATION {passed}/{len(checks)}")
        return 1

    print(f"PASS_P060_PLAN_ACTIVATION {passed}/{len(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
