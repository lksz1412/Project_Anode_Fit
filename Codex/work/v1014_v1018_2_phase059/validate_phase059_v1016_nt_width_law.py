#!/usr/bin/env python3
"""Validate Phase 059 Step 37.4 v1.0.16 n(T) width-law audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex/work/v1014_v1018_2_phase059/"
    "audit_phase059_v1016_nt_width_law.py"
)
DATA = ROOT / "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md"
STATUS = (
    "CONDITIONAL_P059_V1016_NT_DWDT_ALGEBRA_AND_OPT_IN_ROUNDTRIP_"
    "PASS_BUT_EMPIRICAL_STATUS_DEFAULT_BRANCH_POSITIVITY_AND_"
    "IDENTIFIABILITY_GAPS_REMAIN"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    delta = data["exact_delta"]
    nt = data["opt_in_nt_roundtrip"]
    exact = data["constant_n_v1015_comparison"]
    fixed = data["fixed_w_branch"]
    default = data["missing_n_and_w_default_branch"]
    array_t = data["array_temperature"]
    guards = data["guards"]
    ident = data["parameter_identifiability"]
    coverage = data["persistent_test_coverage"]
    summary = data["summary"]
    dispositions = {
        item["topic"]: item["disposition"] for item in data["findings"]
    }
    report = REPORT.read_text(encoding="utf-8")

    checks = [
        ("schema", data["schema_version"] == 1),
        ("phase_step", data["phase"] == 59 and data["step"] == "37.4"),
        ("status", data["status"] == STATUS),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_hashes",
            data["source_hashes_before"] == data["source_hashes_after"],
        ),
        ("code_numstat", delta["production_code"] == {"added": 55, "deleted": 20}),
        ("ch1_numstat", delta["chapter_1"] == {"added": 11, "deleted": 8}),
        ("ch2_numstat", delta["chapter_2"] == {"added": 18, "deleted": 6}),
        ("guide_numstat", delta["fitting_guide"] == {"added": 23, "deleted": 7}),
        ("test_numstat", delta["regression_harness"] == {"added": 2, "deleted": 2}),
        (
            "dwdt_added",
            next(row for row in delta["method_ast"] if row["method"] == "_dwdT")[
                "added"
            ],
        ),
        ("nt_n", nt["code_n"] == 1.0),
        ("nt_product_rule", abs(nt["analytic_dwdT_V_per_K"] - nt["code_dwdT_V_per_K"]) < 1e-18),
        ("nt_code", nt["analytic_code_abs_V_per_K"] < 1e-18),
        ("nt_fd", nt["analytic_fd_abs_V_per_K"] < 1e-12),
        ("constant_rows", len(exact["rows"]) == 4),
        ("constant_exact", exact["all_four_bit_exact"]),
        ("constant_zero", all(row["max_abs"] == 0.0 for row in exact["rows"])),
        ("fixed_width", abs(fixed["width_V"] - 0.02) < 1e-15),
        ("fixed_dwdt", fixed["dwdT_V_per_K"] == 0.0),
        (
            "fixed_entropy",
            abs(
                fixed["code_dUdT_V_per_K"]
                - fixed["expected_center_only_V_per_K"]
            )
            < 1e-18,
        ),
        ("default_n", default["declared_n_fallback"] == 1.0),
        ("default_thermal", default["width_is_RT_over_F"]),
        ("default_zero_dwdt", default["code_dwdT_V_per_K"] == 0.0),
        ("default_actual_dwdt", default["actual_dwdT_V_per_K"] > 8e-5),
        ("default_mismatch", default["mismatch_V_per_K"] > 1.19e-4),
        ("array_t", array_t["max_abs"] == 0.0),
        ("key_guard", guards["n_T1_without_n"]["raised"]),
        (
            "key_guard_type",
            guards["n_T1_without_n"]["type"] == "ValueError",
        ),
        (
            "negative_example",
            guards["positivity"]["example_n_at_273p15"] < 0.0
            and guards["positivity"]["example_n_at_298p15"] > 0.0,
        ),
        (
            "width_guard",
            guards["positivity"]["low_temperature_width_guard"]["raised"],
        ),
        (
            "no_domain_bound",
            not guards["positivity"]["domain_bound_documented_in_guide"]
            and not guards["positivity"]["fitting_schema_enforces_domain_bound"],
        ),
        ("single_t_rank", ident["single_temperature_rank"] == 1),
        (
            "one_sided_condition",
            ident["one_sided_20K"]["condition_number"] > 36.0,
        ),
        (
            "one_sided_correlation",
            ident["one_sided_20K"]["parameter_correlation"] > 0.75,
        ),
        ("coverage_claim", coverage["execution_ledger_claims_nt_roundtrip"]),
        ("coverage_no_nt", coverage["n_T1_occurrence_count"] == 0),
        ("coverage_no_dwdt", coverage["_dwdT_occurrence_count"] == 0),
        ("coverage_fail", not coverage["persistent_nt_test_present"]),
        ("finding_count", summary["finding_count"] == 16),
        (
            "empirical",
            dispositions["nt_status"]
            == "EMPIRICAL_WIDTH_LAW_NOT_MICROSCOPIC_MULTIPLICITY",
        ),
        ("algebra", dispositions["dwdt_algebra"] == "PRESERVE_PRODUCT_RULE"),
        (
            "roundtrip",
            dispositions["nt_roundtrip"]
            == "PRESERVE_OPT_IN_NUMERICAL_CONFORMANCE",
        ),
        (
            "default_fail",
            dispositions["default_branch"]
            == "FAIL_DEFAULT_N1_THERMAL_WIDTH_DWDT_MISMATCH",
        ),
        (
            "positivity_bound",
            dispositions["positivity"] == "REQUIRE_DOMAIN_WIDE_ENDPOINT_BOUNDS",
        ),
        (
            "test_fail",
            dispositions["persistent_tests"]
            == "FAIL_NO_PERSISTENT_NT_REGRESSION",
        ),
        (
            "phase_guard",
            dispositions["two_phase_interpretation"]
            == "DO_NOT_PROMOTE_NT_TO_PHASE_MECHANISM",
        ),
        ("summary_product", summary["product_rule_pass"]),
        ("summary_roundtrip", summary["opt_in_nt_roundtrip_pass"]),
        ("summary_exact", summary["constant_n_bit_exact_pass"]),
        ("summary_fixed", summary["fixed_w_branch_pass"]),
        ("summary_default_fail", not summary["default_branch_conformance_pass"]),
        (
            "summary_positivity_fail",
            not summary["domain_wide_positivity_contract_pass"],
        ),
        (
            "summary_test_fail",
            not summary["persistent_nt_regression_pass"],
        ),
        (
            "summary_micro_fail",
            not summary["microscopic_nt_authority_pass"],
        ),
        (
            "summary_ident_fail",
            not summary["single_temperature_n0_n1_identifiability_pass"],
        ),
        ("summary_array", summary["array_temperature_pointwise_pass"]),
        ("next", summary["next_step"] == "37.5"),
        ("report_title", report.startswith("# Phase 059 v1.0.16")),
        ("report_status", STATUS in report),
        ("report_default", "0.119455 mV/K" in report),
        ("report_empirical", "empirical width law" in report),
        ("report_bound", "endpoint 제약" in report),
        ("report_coverage", "occurrence가 0" in report),
        ("report_next", "Step 37.5" in report),
        ("report_source", "원본 `Claude/`, `main`" in report),
    ]

    initial = (digest(DATA), digest(REPORT))
    run = subprocess.run(
        ["python", str(AUDITOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
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
    print(f"PASS_P059_V1016_NT_WIDTH_LAW_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
