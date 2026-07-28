#!/usr/bin/env python3
"""Validate Phase 059 Step 38.1 outputs and deterministic regeneration."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDITOR = Path(__file__).with_name("audit_phase059_v1017_doc_citations.py")
JSON_PATH = ROOT / "Codex/results/PHASE_059_V1017_DOC_CITATION_AUDIT.json"
REPORT_PATH = ROOT / "Codex/results/PHASE_059_V1017_DOC_CITATION_REVIEW.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    d = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    report = REPORT_PATH.read_text(encoding="utf-8")
    checks = {
        "schema": d["schema_version"] == 1,
        "step": d["step"] == "38.1",
        "status": d["status"].startswith("CONDITIONAL_P059_V1017"),
        "versions": (d["source_version"], d["target_version"]) == ("v1.0.16", "v1.0.17"),
        "three_theory_diffs": set(d["theory_diffs"]) == {"chapter1", "chapter2", "appendix"},
        "theory_changed": all(x["old_sha256"] != x["new_sha256"] for x in d["theory_diffs"].values()),
        "four_assets": len(d["executable_comparison"]) == 4,
        "two_assets_identical": sum(x["byte_identical"] for x in d["executable_comparison"]) == 2,
        "two_version_only": sum(x["only_version_literals_changed"] for x in d["executable_comparison"]) == 2,
        "asset_logic_same": all(not x["calculation_logic_changed"] for x in d["executable_comparison"]),
        "test_paths_only": d["regression_harness_comparison"]["only_versioned_absolute_paths_changed"],
        "test_physics_same": not d["regression_harness_comparison"]["physical_assertion_change"],
        "citations": len(d["citation_adjudication"]) == 8,
        "occupation_fixed": next(x for x in d["citation_adjudication"] if x["key"] == "occupation2019")["new_doi"].endswith("134774"),
        "hysteresis_fixed": next(x for x in d["citation_adjudication"] if x["key"] == "hysteresis2018")["new_doi"].endswith("05.052"),
        "chemmater_scope_fail": next(x for x in d["citation_adjudication"] if x["key"] == "chemmater2015")["scope"] == "FAIL_ANNOTATION",
        "msmr_site_fail": next(x for x in d["citation_adjudication"] if x["key"] == "msmr_partI")["scope"] == "FAIL_AT_CITATION_SITE",
        "internal_not_lit": next(x for x in d["citation_adjudication"] if x["key"] == "numverif2026")["bibliography"] == "INTERNAL_NOT_LITERATURE",
        "boundary_fail": not d["theory_only_boundary"]["pass"],
        "boundary_hits": d["theory_only_boundary"]["outside_designated_section_hit_count"] >= 2,
        "no_physics_change": not d["claims"]["production_physics_changed"],
        "no_algorithm_change": not d["claims"]["algorithm_changed"],
        "no_external_validation": not d["claims"]["new_external_material_validation"],
        "two_dois": d["claims"]["two_wrong_dois_corrected"],
        "bib_incomplete": not d["claims"]["all_bibliography_complete"],
        "citation_scope_incomplete": not d["claims"]["all_citation_sites_directly_supported"],
        "doc_only": d["claims"]["v1017_is_doc_only_scientific_release"],
        "findings": len(d["findings"]) == 12,
        "next": d["summary"]["next_step"] == "38.2",
        "report_title": report.startswith("# Phase 059 v1.0.17 문건·인용 감사"),
        "report_doi": "134774" in report and "2018.05.052" in report,
        "report_article_numbers": "023502/103505" in report,
        "report_boundary": "theory-only body gate는 아직 FAIL" in report,
        "report_authority": "doped high-voltage LCO" in report,
        "report_next": "Step 38.2" in report,
        "report_source": "Haruyama" in report and "Zilberman" in report,
    }
    before = (digest(JSON_PATH), digest(REPORT_PATH))
    run = subprocess.run([sys.executable, str(AUDITOR)], cwd=ROOT, capture_output=True, text=True)
    after = (digest(JSON_PATH), digest(REPORT_PATH))
    checks["rerun_exit"] = run.returncode == 0
    checks["rerun_deterministic"] = before == after

    passed = 0
    for name, ok in checks.items():
        print(("PASS" if ok else "FAIL"), name)
        passed += bool(ok)
    print(f"SUMMARY {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        return 1
    print(f"PASS_P059_V1017_DOC_CITATIONS_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
