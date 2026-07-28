#!/usr/bin/env python3
"""Validate Phase 059 Step 36.1 v1.0.14 boundary audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex/work/v1014_v1018_2_phase059/"
    "audit_phase059_v1014_register_boundary.py"
)
DATA = (
    ROOT / "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json"
)
REPORT = (
    ROOT / "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    summary = data["summary"]
    ch1 = data["comparisons"]["ch1"]
    ch2 = data["comparisons"]["ch2"]
    boundary = data["implementation_boundary"]
    decision_map = {item["topic"]: item for item in data["decisions"]}
    checks: list[tuple[str, bool]] = [
        ("schema", data["schema_version"] == 1),
        ("sources_unchanged", data["sources_unchanged"]),
        ("ch1_pair", ch1["pair_id"] == "ch1_v1013_to_v1014"),
        ("ch2_pair", ch2["pair_id"] == "ch2_v1013_to_v1014"),
        ("ch1_lines_2934_to_3445", ch1["old_line_count"] == 2934 and ch1["new_line_count"] == 3445),
        ("ch2_lines_776_to_794", ch2["old_line_count"] == 776 and ch2["new_line_count"] == 794),
        ("ch1_net_511", summary["ch1_net_line_change"] == 511),
        ("ch2_net_18", summary["ch2_net_line_change"] == 18),
        ("ch1_equations_101_10_5", ch1["equation_unchanged_count"] == 101 and ch1["equation_changed_count"] == 10 and ch1["equation_added_count"] == 5),
        ("ch2_equations_20_2_0", ch2["equation_unchanged_count"] == 20 and ch2["equation_changed_count"] == 2 and ch2["equation_added_count"] == 0),
        ("physics_changed_equations_5", summary["physics_derivation_changed_equation_count"] == 5),
        ("boundary_changed_equations_5", summary["implementation_boundary_changed_equation_count"] == 5),
        ("physics_added_equations_5", summary["physics_derivation_added_equation_count"] == 5),
        ("width_identity_preserved", data["width_budget_contract"]["identity_disposition"] == "PRESERVE"),
        ("width_role_split_required", data["width_budget_contract"]["semantic_disposition"] == "CORRECT_ROLE_SPLIT_REQUIRED"),
        ("required_width_symbols_4", len(data["width_budget_contract"]["required_final_symbols"]) == 4),
        ("v1014_boundary_not_pass", summary["theory_only_boundary_pass"] is False),
        ("v1014_outside_mentions_nonzero", summary["v1014_outside_allowed_implementation_line_count"] > 0),
        ("v1014_navigation_refs_nonzero", summary["v1014_outside_navigation_reference_count"] > 0),
        ("v1014_boundary_violations_nonzero", summary["v1014_outside_boundary_violation_count"] > 0),
        ("v1014_improves_v1013_boundary", summary["v1014_outside_boundary_violation_count"] < summary["v1013_outside_boundary_violation_count"]),
        ("v1014_allowed_section_nonzero", summary["v1014_inside_allowed_implementation_line_count"] > 0),
        ("ch1_v1014_outside_nonzero", boundary["ch1_v1014"]["outside_boundary_violation_count"] > 0),
        ("ch2_v1014_outside_nonzero", boundary["ch2_v1014"]["outside_boundary_violation_count"] > 0),
        ("comments_excluded", all(not item["text"].startswith("%") for name in boundary for region in ("outside_allowed_section", "inside_allowed_section") for item in boundary[name][region])),
        ("decision_count_6", summary["decision_count"] == 6),
        ("textbook_preserve_asset", decision_map["textbook_register"]["disposition"] == "PRESERVE_ASSET_NOT_FINAL_AUTHORITY"),
        ("review_depth_partial", decision_map["review_depth"]["disposition"] == "PARTIAL"),
        ("theory_boundary_fail", decision_map["theory_only_boundary"]["disposition"] == "FAIL_REQUIRES_CORRECTION"),
        ("one_way_partial", decision_map["one_way_theory_to_code"]["disposition"] == "PARTIAL"),
        ("scientific_validation_unverified", decision_map["scientific_validation"]["disposition"] == "UNVERIFIED"),
        ("conditional_status", data["status"].startswith("CONDITIONAL_P059_")),
        ("report_exists", REPORT.is_file()),
        ("report_core_findings", all(marker in REPORT.read_text(encoding="utf-8") for marker in ("PRESERVE_ASSET + CORRECT_BOUNDARY", "w_\\mathrm{int}", "Step 36.2"))),
        ("next_step_36_2", "Step 36.2" in data["next_action"]),
    ]
    before_data = digest(DATA)
    before_report = digest(REPORT)
    completed = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    checks.extend(
        [
            ("auditor_rerun_exit_zero", completed.returncode == 0),
            ("deterministic_data", digest(DATA) == before_data),
            ("deterministic_report", digest(REPORT) == before_report),
        ]
    )
    for index, (name, passed) in enumerate(checks, 1):
        print(f"{index:02d} {'PASS' if passed else 'FAIL'} {name}")
    passed = sum(value for _, value in checks)
    print(f"SUMMARY {passed}/{len(checks)} PASS")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
