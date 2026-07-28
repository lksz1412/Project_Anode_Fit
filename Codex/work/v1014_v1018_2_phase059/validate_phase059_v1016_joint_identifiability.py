#!/usr/bin/env python3
"""Validate Phase 059 Step 37.5 joint-identifiability audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = ROOT / "Codex/work/v1014_v1018_2_phase059/audit_phase059_v1016_joint_identifiability.py"
DATA = ROOT / "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md"
STATUS = (
    "FAIL_P059_V1016_JOINT_IDENTIFIABILITY_WITHOUT_MULTI_TEMPERATURE_"
    "RATE_SERIES_AND_INDEPENDENT_ELECTRONIC_VIBRATIONAL_PRIORS"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    ranks = data["rank_analyses"]
    summary = data["summary"]
    dispositions = {x["topic"]: x["disposition"] for x in data["findings"]}
    report = REPORT.read_text(encoding="utf-8")
    checks = [
        ("schema", data["schema_version"] == 1),
        ("step", data["phase"] == 59 and data["step"] == "37.5"),
        ("status", data["status"] == STATUS),
        ("unchanged", data["source_unchanged"]),
        ("hashes", data["source_hashes_before"] == data["source_hashes_after"]),
        ("nt_rank1", ranks["n0_n1_single_temperature"]["rank"] == 1),
        ("nt_null1", ranks["n0_n1_single_temperature"]["nullity"] == 1),
        ("nt_multi_rank2", ranks["n0_n1_three_temperatures"]["rank"] == 2),
        ("act_one_rank1", ranks["activation_one_temperature_many_rates"]["rank"] == 1),
        ("act_many_rank2", ranks["activation_three_temperatures_many_rates"]["rank"] == 2),
        ("act_null", ranks["activation_three_temperatures_many_rates"]["nullity"] == 1),
        ("lco_rank1", ranks["lco_frozen_gate"]["rank"] == 1),
        ("lco_null3", ranks["lco_frozen_gate"]["nullity"] == 3),
        ("vib_rank0", ranks["vibrational"]["jacobian_rank"] == 0),
        ("scenario_count", len(data["scenario_matrix"]) == 4),
        ("contracts", set(data["minimum_evidence_contract"]) == {"width_nt", "activation", "lco_electronic", "vibrational"}),
        ("finding_count", summary["finding_count"] == 14),
        ("nt_fail", dispositions["n0_n1_single_temperature"] == "FAIL_STRUCTURAL_RANK_DEFICIENCY"),
        ("act_fail", dispositions["activation_single_temperature"] == "FAIL_ONLY_COMPOSITE_LAG_SCALE"),
        ("act_null_disposition", dispositions["activation_multi_temperature"] == "FAIL_DS_PREFACTOR_EXACT_NULL"),
        ("lco_fail", dispositions["lco_gate_current_code"] == "FAIL_FROZEN_GATE_RANK1"),
        ("vib_fail", dispositions["vibrational"] == "FAIL_FORWARD_TERM_ABSENT"),
        ("joint_fail", dispositions["electronic_vibrational"] == "FAIL_JOINT_CURVATURE_ATTRIBUTION"),
        ("data_req", dispositions["data_contract"] == "REQUIRE_MULTI_T_RATE_AND_INDEPENDENT_PRIORS"),
        ("guide", dispositions["guide_tiering"] == "PRESERVE_STAGED_INTENT_NOT_COMPLETED_IDENTIFICATION"),
        ("synthetic", dispositions["synthetic_roundtrip"] == "NOT_STATISTICAL_IDENTIFIABILITY_EVIDENCE"),
        ("summary_nt", not summary["single_temperature_nt_identifiable"]),
        ("summary_act", not summary["single_temperature_activation_identifiable"]),
        ("summary_allact", not summary["multi_temperature_activation_all_three_identifiable"]),
        ("summary_lco", not summary["current_lco_gate_parameters_jointly_identifiable"]),
        ("summary_vib", not summary["vibrational_parameter_identifiable"]),
        ("summary_joint", not summary["electronic_vibrational_separable_in_current_code"]),
        ("summary_requested", not summary["requested_joint_identification_without_required_data_pass"]),
        ("summary_guide", summary["guide_staged_strategy_directionally_sound"]),
        ("summary_material", not summary["experimental_material_fit_authority_pass"]),
        ("next", summary["next_step"] == "38.1"),
        ("report_title", report.startswith("# Phase 059 v1.0.16")),
        ("report_status", STATUS in report),
        ("report_ranks", all(token in report for token in ("1/2", "1/3", "2/3", "1/4"))),
        ("report_vib", "rank 0" in report),
        ("report_synthetic", "statistical identifiability" in report),
        ("report_next", "Step 38.1" in report),
        ("report_source", "원본 `Claude/`, `main`" in report),
    ]
    initial = (digest(DATA), digest(REPORT))
    run = subprocess.run(["python", str(AUDITOR)], cwd=ROOT, text=True, capture_output=True)
    checks += [
        ("rerun_exit", run.returncode == 0),
        ("rerun_deterministic", initial == (digest(DATA), digest(REPORT))),
    ]
    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"SUMMARY {len(checks)-len(failed)}/{len(checks)} checks passed")
    if failed:
        print("FAILED " + ", ".join(failed))
        return 1
    print(f"PASS_P059_V1016_JOINT_IDENTIFIABILITY_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
