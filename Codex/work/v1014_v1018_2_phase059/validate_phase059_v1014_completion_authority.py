#!/usr/bin/env python3
"""Validate Phase 059 Step 36.5 v1.0.14 authority adjudication."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex/work/v1014_v1018_2_phase059/"
    "audit_phase059_v1014_completion_authority.py"
)
DATA = (
    ROOT / "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_AUDIT.json"
)
REPORT = (
    ROOT / "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_REVIEW.md"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    summary = data["summary"]
    source = data["source_contracts"]
    blockers = data["blocker_families"]
    claims = {item["id"]: item for item in data["claims"]}
    report = REPORT.read_text(encoding="utf-8")

    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("phase_step", data["phase"] == 59 and data["step"] == "36.5"),
        (
            "status",
            data["status"]
            == "CONDITIONAL_P059_V1014_PROCESS_COMPLETE_BUT_SCIENTIFIC_COMPLETION_AUTHORITY_REJECTED",
        ),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_hashes_equal",
            data["source_hashes_before"] == data["source_hashes_after"],
        ),
        ("process_files", source["process_file_count"] >= 30),
        ("review_reports", source["review_report_count"] == 20),
        ("authority_sources", source["authority_source_file_count"] >= 35),
        ("authority_lines", source["authority_source_line_count"] > 3000),
        (
            "trajectory",
            source["review_trajectory_reported"] == [22, 13, 16, 8, 18, 13, 8],
        ),
        (
            "trajectory_not_monotone",
            not source["review_trajectory_monotone_nonincreasing"],
        ),
        (
            "zero_round_criterion_not_met",
            not source["declared_consecutive_zero_round_criterion_met"],
        ),
        ("four_blocker_families", len(blockers) == 4),
        (
            "boundary_fail",
            blockers["theory_boundary"]["decisive_metrics"][
                "outside_boundary_violations"
            ]
            == 24
            and not blockers["theory_boundary"]["decisive_metrics"][
                "theory_only_boundary_pass"
            ],
        ),
        (
            "phase_separation_fails",
            not any(
                blockers["phase_separation"]["decisive_metrics"].values()
            ),
        ),
        (
            "lco_fails",
            not any(blockers["lco_heat"]["decisive_metrics"].values()),
        ),
        (
            "kinetics_fails",
            not any(blockers["kinetics"]["decisive_metrics"].values()),
        ),
        ("claim_count", summary["claim_count"] == 20),
        ("claims_unique", len(claims) == 20),
        (
            "claim_ids",
            set(claims)
            == {
                f"P059-V1014-AUTH-{number:03d}" for number in range(1, 21)
            },
        ),
        (
            "process_preserved",
            claims["P059-V1014-AUTH-001"]["disposition"]
            == "PRESERVE_PROCESS_COMPLETION",
        ),
        (
            "regression_scoped",
            claims["P059-V1014-AUTH-003"]["authority_scope"]
            == "LEGACY_OUTPUT_IDENTITY_ONLY",
        ),
        (
            "pedagogy_preserved",
            claims["P059-V1014-AUTH-005"]["disposition"]
            == "PRESERVE_PEDAGOGICAL_ASSET",
        ),
        (
            "boundary_claim_narrowed",
            claims["P059-V1014-AUTH-006"]["disposition"]
            == "NARROW_LITERAL_COUNT_ONLY_GLOBAL_CLAIM_REJECTED",
        ),
        (
            "convergence_scoped",
            claims["P059-V1014-AUTH-007"]["disposition"]
            == "PRESERVE_REVIEW_PROCESS_CLOSURE_ONLY",
        ),
        (
            "zero_defect_rejected",
            claims["P059-V1014-AUTH-008"]["disposition"]
            == "REJECT_GLOBAL_SCIENTIFIC_CLAIM",
        ),
        (
            "corner_cases_scoped",
            claims["P059-V1014-AUTH-009"]["disposition"]
            == "PRESERVE_SAMPLED_REVIEW_RESULT_ONLY",
        ),
        (
            "phase_separation_partial",
            claims["P059-V1014-AUTH-010"]["disposition"]
            == "PARTIAL_CORE_ALGEBRA_PRESERVED_CLOSURE_REJECTED",
        ),
        (
            "gmax_rejected",
            claims["P059-V1014-AUTH-012"]["disposition"]
            == "REJECT_UNVERIFIED_TIER_A_PROMOTION",
        ),
        (
            "lco_scope_rejected",
            claims["P059-V1014-AUTH-014"]["disposition"]
            == "REJECT_MATERIAL_SCOPE_COMPLETION",
        ),
        (
            "kinetics_completion_rejected",
            claims["P059-V1014-AUTH-015"]["disposition"]
            == "REJECT_SHIPPED_MODEL_COMPLETION",
        ),
        (
            "joint_target_rejected",
            claims["P059-V1014-AUTH-016"]["disposition"]
            == "REJECT_TARGET_COMPLETION",
        ),
        (
            "barrier_rejected",
            claims["P059-V1014-AUTH-017"]["disposition"]
            == "REJECT_FROZEN_AFFINITY_CLOSURE",
        ),
        (
            "copy_forward_repair_rejected",
            claims["P059-V1014-AUTH-018"]["disposition"]
            == "REJECT_REPAIR_CLAIM_COPY_FORWARD_CONFIRMED",
        ),
        (
            "open_admission_preserved",
            claims["P059-V1014-AUTH-019"]["disposition"]
            == "PRESERVE_BLOCKER_ADMISSION",
        ),
        (
            "final_authority_rejected",
            claims["P059-V1014-AUTH-020"]["disposition"]
            == "REJECT_SCIENTIFIC_COMPLETION_AUTHORITY",
        ),
        ("process_summary", summary["process_completion_preserved"]),
        (
            "internal_summary",
            summary["build_and_internal_regression_preserved"],
        ),
        ("pedagogy_summary", summary["pedagogical_asset_preserved"]),
        (
            "zero_defect_summary",
            not summary["global_zero_physics_defect_claim_pass"],
        ),
        (
            "convergence_summary",
            not summary["scientific_convergence_claim_pass"],
        ),
        (
            "authority_summary",
            not summary["scientific_completion_authority_pass"],
        ),
        ("material_summary", not summary["material_validation_pass"]),
        ("final_basis_summary", not summary["final_theory_code_basis_pass"]),
        ("next_step", summary["next_step"] == "37.1"),
        ("report_title", report.startswith("# Phase 059 v1.0.14")),
        ("report_status", data["status"] in report),
        ("report_process_science_split", "작업 절차와 릴리스 제작의 완료본" in report),
        ("report_blocker_total", f"합계 {summary['independent_finding_count']}건" in report),
        ("report_next", "Step 37.1" in report),
        ("report_source_untouched", "원본 `Claude/`, `main`" in report),
    ]

    initial_hashes = (digest(DATA), digest(REPORT))
    run = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.extend(
        [
            ("auditor_rerun_exit", run.returncode == 0),
            (
                "auditor_rerun_deterministic",
                initial_hashes == (digest(DATA), digest(REPORT)),
            ),
        ]
    )

    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"SUMMARY {len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        print("FAILED " + ", ".join(failed))
        return 1
    print("PASS_P059_V1014_COMPLETION_AUTHORITY_53_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
