#!/usr/bin/env python3
"""Validate Phase 059 Step 38.3 Einstein-theory audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDITOR = Path(__file__).with_name("audit_phase059_v1018_2_einstein_theory.py")
OUT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    d = json.loads(OUT.read_text(encoding="utf-8"))
    r = REPORT.read_text(encoding="utf-8")
    v = d["validation"]
    n = d["normalization_scope"]
    s = d["summary"]
    checks = {
        "schema": d["schema_version"] == 1,
        "step": d["step"] == "38.3",
        "status": d["status"].startswith("CONDITIONAL_P059_V1018_2_EINSTEIN"),
        "rows": len(d["numeric_rows"]) == 8,
        "identity": v["max_A_plus_TS_minus_U_J_per_mol"] < 1e-10,
        "entropy_fd": v["max_entropy_finite_difference_error_J_per_mol_K"] < 1e-7,
        "code_entropy": v["max_code_entropy_error_J_per_mol_K"] < 1e-12,
        "code_voltage": v["max_code_centered_voltage_error_V"] < 1e-12,
        "code_centered_entropy": v["max_code_centered_entropy_error_J_per_mol_K"] < 1e-12,
        "roundtrip": v["max_roundtrip_error_uV_per_K"] < 1e-6,
        "reported_values": v["reported_four_temperature_values_match"],
        "zpe_cancel": d["derivation"]["zero_point_centered_voltage_max_difference_V"] < 1e-15,
        "low_limit": d["limits"]["low_T_relative_error"] < 1e-12,
        "high_limit": d["limits"]["high_T_relative_error"] < 1e-10,
        "one_mode": n["implemented_mode_multiplicity"] == 1.0,
        "no_amplitude": not n["explicit_amplitude_parameter_present"],
        "no_pair": not n["reactant_and_product_theta_pair_present"],
        "no_dos": not n["phonon_DOS_integral_present"],
        "counterexample": n["reaction_counterexample"]["delta_S_reaction_at_Tref_J_per_mol_K"] > 0,
        "findings": len(d["findings"]) == 12,
        "algebra_pass": s["algebra_pass"],
        "reference_pass": s["reference_roundtrip_pass"],
        "general_fail": not s["general_reaction_vibrational_model_pass"],
        "material_fail": not s["material_validation_pass"],
        "next": s["next_step"] == "38.4",
        "report_title": r.startswith("# Phase 059 v1.0.18.2 Einstein 열역학 재유도"),
        "report_values": "-3.738/0/3.700/9.138" in r,
        "report_spectrum": "lithiated와 delithiated phonon spectrum" in r,
        "report_700": "700 K는 capability demo" in r,
        "report_next": "Step 38.4" in r,
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
    print(f"PASS_P059_V1018_2_EINSTEIN_THEORY_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
