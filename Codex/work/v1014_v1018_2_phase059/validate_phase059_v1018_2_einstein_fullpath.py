#!/usr/bin/env python3
"""Validate Phase 059 Step 38.4 outputs."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDITOR = Path(__file__).with_name("audit_phase059_v1018_2_einstein_fullpath.py")
OUT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    d = json.loads(OUT.read_text(encoding="utf-8"))
    r = REPORT.read_text(encoding="utf-8")
    v, s = d["validation"], d["summary"]
    checks = {
        "schema": d["schema_version"] == 1,
        "step": d["step"] == "38.4",
        "status": d["status"].startswith("CONDITIONAL_P059_V1018_2_EINSTEIN_ABSENT"),
        "absent_exact": v["absent_key_all_exact"],
        "five_absent_paths": len(d["absent_key_comparison"]) == 5,
        "active_rows": len(d["active_branch_rows"]) == 4,
        "active_roundtrip": v["active_fullpath_roundtrip_max_error_V_per_K"] < 1e-10,
        "heat_identity": v["active_heat_identity_max_error_W_per_A"] < 1e-12,
        "peak_grid": v["active_peak_grid_max_error_V"] < 5.1e-5,
        "u_only": v["u_only_public_ignore_confirmed"],
        "tref_fail": not v["tref_positive_failfast_pass"],
        "coverage_files": len(d["release_test_coverage"]) == 3,
        "coverage_zero": all(x["theta_E_occurrences"] == 0 and x["_vib_occurrences"] == 0 for x in d["release_test_coverage"]),
        "regression_fail": not v["persistent_release_regression_pass"],
        "findings": len(d["findings"]) == 12,
        "capability": s["capability_conformance_pass"],
        "contract_fail": not s["public_parameter_contract_pass"],
        "material_fail": not s["material_validation_pass"],
        "next": s["next_step"] == "38.5",
        "report_title": r.startswith("# Phase 059 v1.0.18.2 Einstein full-path 감사"),
        "report_exact": "모두 exact 동일" in r,
        "report_u_only": "U-only transition" in r,
        "report_coverage": "각각 0건" in r,
        "report_next": "Step 38.5" in r,
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
    print(f"PASS_P059_V1018_2_EINSTEIN_FULLPATH_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
