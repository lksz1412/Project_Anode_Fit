#!/usr/bin/env python3
"""Validate Phase 059 Step 38.2 outputs."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDITOR = Path(__file__).with_name("audit_phase059_v1018_1_carryforward.py")
OUT = ROOT / "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_REVIEW.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    d = json.loads(OUT.read_text(encoding="utf-8"))
    r = REPORT.read_text(encoding="utf-8")
    c = d["claims"]
    checks = {
        "schema": d["schema_version"] == 1,
        "step": d["step"] == "38.2",
        "status": d["status"].startswith("CONDITIONAL_P059_V1018_1"),
        "versions": (d["source_version"], d["target_version"]) == ("v1.0.17", "v1.0.18.1"),
        "theory_pairs": len(d["theory_axis"]) == 3,
        "equation_counts": sum(x["labeled_equations"]["changed_count"] for x in d["theory_axis"]) == 1,
        "only_symbol_equation": d["theory_axis"][0]["labeled_equations"]["changed"][0]["label"] == "eq:sm-mucount",
        "code_test_pairs": len(d["code_test_axis"]) == 8,
        "production_exact": c["production_code_byte_identical"],
        "golden_exact": c["golden_byte_identical"],
        "figures": len(d["figure_axis"]) == 4 and c["all_carried_figures_byte_identical"],
        "logic_same": not c["calculation_or_assertion_changed"],
        "no_new_eq": not c["new_labeled_physical_equation_added"],
        "no_parameter": not c["new_material_parameter_added"],
        "no_validation": not c["new_external_validation_added"],
        "carryforward": c["physics_unchanged_carryforward"],
        "pedagogy": c["pedagogical_refinement_present"],
        "blockers": c["all_prior_blockers_remain"],
        "pdfs": d["summary"]["pdf_count"] == 6,
        "pages": d["summary"]["pdf_page_count"] == 165,
        "visual": all(x["all_pages_visually_inspected_pass"] for x in d["pdf_axis"]),
        "findings": len(d["findings"]) == 12,
        "next": d["summary"]["next_step"] == "38.3",
        "report_title": r.startswith("# Phase 059 v1.0.18.1 이월판 감사"),
        "report_byte": "byte-identical" in r,
        "report_pages": "165쪽" in r and "58→59쪽" in r,
        "report_no_physics": "새 forward physics" in r,
        "report_next": "Step 38.3" in r,
    }
    before = (sha(OUT), sha(REPORT))
    p = subprocess.run([sys.executable, str(AUDITOR)], cwd=ROOT, capture_output=True, text=True)
    checks["rerun_exit"] = p.returncode == 0
    checks["rerun_deterministic"] = before == (sha(OUT), sha(REPORT))
    passed = 0
    for name, ok in checks.items():
        print(("PASS" if ok else "FAIL"), name)
        passed += bool(ok)
    print(f"SUMMARY {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        return 1
    print(f"PASS_P059_V1018_1_CARRYFORWARD_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
