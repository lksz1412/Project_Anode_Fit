#!/usr/bin/env python3
"""Validate the 2026-08-25 canonical-completion plan activation package."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[3]
MASTER_MD = ROOT / "Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md"
MASTER_JSON = ROOT / "Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.json"
PHASE_PLAN = ROOT / "Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md"
LEDGER = ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
OUT = ROOT / "Codex/results/PLAN_ACTIVATION_CANONICAL_COMPLETION_VALIDATION.json"


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    files = [MASTER_MD, MASTER_JSON, PHASE_PLAN, LEDGER, HANDOVER]
    master_text = MASTER_MD.read_text(encoding="utf-8")
    phase_text = PHASE_PLAN.read_text(encoding="utf-8")
    ledger_text = LEDGER.read_text(encoding="utf-8")
    handover_text = HANDOVER.read_text(encoding="utf-8")
    data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    phases = data["phases"]

    ranges: list[tuple[int, int, int]] = []
    for phase in phases:
        start_text, end_text = phase["steps"].split("-")
        ranges.append((phase["phase"], int(start_text), int(end_text)))

    contiguous = ranges[0] == (55, 1, 8)
    for previous, current in zip(ranges, ranges[1:]):
        contiguous = contiguous and current[0] == previous[0] + 1
        contiguous = contiguous and current[1] == previous[2] + 1
    contiguous = contiguous and ranges[-1] == (90, 342, 351)

    current_branch = run_git("branch", "--show-current")
    current_head = run_git("rev-parse", "HEAD")
    claude_diff = run_git(
        "diff", "--name-only",
        "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71", "--", "Claude"
    )
    changed_existing_controls = run_git(
        "diff", "--name-only",
        "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71", "--",
        "Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md",
        "Codex/plans/2026-07-28-phase059-v1014-v1018_2-lineage-detailed-plan.md",
        "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
        "Codex/results/ACTIVE_HANDOVER_V1010_V1025_2_REAUDIT.md",
        "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md",
        "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json",
    )

    required_master_sections = [
        "## Summary",
        "## Current Ground Truth",
        "## Phase Range",
        "## Non-goals and Scope Guards",
        "## Implementation Changes and Canonical Files",
        "## Test and Validation Plan",
        "## Assumptions",
        "## Correction History",
    ]
    required_phase_units = [
        "## Step 38.5",
        "## Step 39.1",
        "## Step 39.2",
        "## Step 39.3",
        "## Step 39.4",
        "## Step 39.5",
        "## Step 39.6",
    ]
    result_paths = [
        data["paths"]["execution_ledger"],
        data["paths"]["active_handover"],
        data["paths"]["activation_result"],
    ]
    posix_paths = all("\\" not in p and PurePosixPath(p).as_posix() == p for p in result_paths)

    checks = {
        "all_control_files_exist": all(path.is_file() for path in files),
        "json_schema": data["schema_version"] == 1,
        "approved_status": data["status"] == "ACTIVE_APPROVED",
        "active_branch": current_branch == "codex/anode-fit-v1025_2-canonical-completion",
        "activation_head_is_base": current_head == "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71",
        "phase_count_36": len(phases) == 36,
        "phase_step_ranges_contiguous": contiguous,
        "exact_next_38_5": data["current_position"]["substep"] == "38.5",
        "post_audit_starts_108": next(p for p in phases if p["phase"] == 70)["steps"] == "108-115",
        "all_master_sections": all(section in master_text for section in required_master_sections),
        "all_phase_units": all(unit in phase_text for unit in required_phase_units),
        "plans_under_codex_plans": (
            data["paths"]["plans"] == "Codex/plans"
            and all(
                data["paths"][key].startswith("Codex/plans/")
                for key in {"master_plan", "master_plan_json", "phase059_resume_plan"}
            )
        ),
        "results_under_codex_results": all(path.startswith("Codex/results/") for path in result_paths),
        "machine_paths_posix": posix_paths,
        "step_commit_push_rule": "EVERY_COMPLETED_STEP_OR_SUBSTEP" == data["execution_policy"]["commit_frequency"] == data["execution_policy"]["push_frequency"],
        "theory_code_mentions_forbidden": data["document_policy"]["canonical_theory_code_mentions"] == "FORBIDDEN",
        "fabricated_citation_forbidden": data["evidence_policy"]["fabricated_or_unresolved_citation_allowed"] is False,
        "portability_debt_recorded": "KNOWN_VALIDATOR_PORTABILITY_DEBT_001" in master_text and "KNOWN_VALIDATOR_PORTABILITY_DEBT_001" in ledger_text and "KNOWN_VALIDATOR_PORTABILITY_DEBT_001" in handover_text,
        "handover_exact_next": "Step 38.5" in handover_text,
        "ledger_phase059_in_progress": re.search(r"\| 059 \| 33–39 \| 33\.1–38\.4 .*\| IN_PROGRESS \|", ledger_text) is not None,
        "no_todo_or_tbd": re.search(r"\b(?:TODO|TBD)\b", master_text + phase_text, flags=re.IGNORECASE) is None,
        "claude_unchanged": claude_diff == "",
        "existing_controls_unchanged": changed_existing_controls == "",
    }

    validation = {
        "schema_version": 1,
        "validation_id": "PLAN_ACTIVATION_CANONICAL_COMPLETION",
        "branch": current_branch,
        "base_head": current_head,
        "checks": checks,
        "counts": {
            "checks": len(checks),
            "passed": sum(checks.values()),
            "phases": len(phases),
            "cumulative_steps": ranges[-1][2],
            "files_validated": len(files),
        },
        "file_sha256": {
            path.relative_to(ROOT).as_posix(): sha256(path)
            for path in files
        },
        "known_debts": ["KNOWN_VALIDATOR_PORTABILITY_DEBT_001"],
        "status": "PASS" if all(checks.values()) else "FAIL",
        "next_step": "38.5",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name, passed in checks.items():
        print("PASS" if passed else "FAIL", name)
    print(f"SUMMARY {sum(checks.values())}/{len(checks)} checks passed")
    if not all(checks.values()):
        return 1
    print(f"PASS_PLAN_ACTIVATION_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
