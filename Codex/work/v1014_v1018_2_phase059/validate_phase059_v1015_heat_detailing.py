#!/usr/bin/env python3
"""Validate Phase 059 Step 37.3 v1.0.15 heat-detailing audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDITOR = (
    ROOT
    / "Codex/work/v1014_v1018_2_phase059/"
    "audit_phase059_v1015_heat_detailing.py"
)
DATA = ROOT / "Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1015_HEAT_DETAILING_REVIEW.md"
STATUS = (
    "CONDITIONAL_P059_V1015_HEAT_WORKED_EXAMPLE_NUMERICALLY_CLOSED_"
    "BUT_NO_NEW_HEAT_PHYSICS_AND_SIGN_API_BOUNDARY_REMAINS"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    delta = data["release_delta"]
    worked = data["worked_example"]
    contract = data["quantity_reference_sign_contract"]
    external = data["external_source_check"]
    inherited = data["inherited_v1014_blockers"]
    summary = data["summary"]
    dispositions = {
        item["topic"]: item["disposition"] for item in data["findings"]
    }
    report = REPORT.read_text(encoding="utf-8")
    rows = worked["rows"]
    point = rows[1]

    checks = [
        ("schema", data["schema_version"] == 1),
        ("phase_step", data["phase"] == 59 and data["step"] == "37.3"),
        ("status", data["status"] == STATUS),
        ("source_unchanged", data["source_unchanged"]),
        (
            "source_hashes",
            data["source_hashes_before"] == data["source_hashes_after"],
        ),
        ("ch2_numstat", (
            delta["ch2"]["added_line_count"] == 99
            and delta["ch2"]["deleted_line_count"] == 7
        )),
        ("code_numstat", (
            delta["production_code"]["added_line_count"] == 103
            and delta["production_code"]["deleted_line_count"] == 112
        )),
        ("worked_added", delta["ch2"]["added_worked_example"]),
        ("one_subsection", delta["ch2"]["added_subsection_count"] == 1),
        ("three_equations", delta["ch2"]["added_equation_star_count"] == 3),
        ("two_tables", delta["ch2"]["added_table_count"] == 2),
        (
            "two_code_mentions",
            len(delta["ch2"]["added_body_code_mention_lines"]) == 2,
        ),
        ("vib_caveat", delta["ch2"]["added_vibrational_caveat"]),
        (
            "width_caveat",
            delta["ch2"]["added_width_model_choice_caveat"],
        ),
        ("heat_ast_count", len(delta["heat_path_ast"]) == 6),
        (
            "heat_ast_identical",
            delta["all_heat_path_executable_ast_identical"],
        ),
        ("five_soc_rows", len(rows) == 5),
        ("xbar_point", point["xbar_delithiation_fraction"] == 0.25),
        ("point_voltage", abs(point["U_oc_V"] - 0.0743511412863) < 1e-12),
        (
            "point_dudt",
            abs(
                point["code_entropy_coefficient_V_per_K"]
                + 0.000203945972183
            )
            < 1e-15,
        ),
        (
            "point_entropy",
            abs(point["effective_entropy_J_per_mol_K"] + 19.6777271261)
            < 1e-9,
        ),
        (
            "point_heat",
            abs(point["qrev_per_I_V"] - 0.0608064916064) < 1e-12,
        ),
        (
            "analytic_code",
            worked["maximum_analytic_code_abs_V_per_K"] < 1e-18,
        ),
        (
            "analytic_fd",
            worked["maximum_analytic_fd_abs_V_per_K"] < 1e-10,
        ),
        (
            "fixed_width_limit",
            worked["maximum_fixed_width_center_abs_V_per_K"] < 3e-9,
        ),
        (
            "table_sign_pattern",
            [row["qrev_per_I_V"] > 0 for row in rows]
            == [True, True, True, False, False],
        ),
        ("opposite_labels", contract["labels_are_opposite_chemical_directions"]),
        (
            "label_disclosure",
            contract["label_difference_disclosed_in_text_and_docstring"],
        ),
        (
            "api_not_safe",
            not contract["api_type_enforces_reaction_coordinate"],
        ),
        (
            "no_full_cell_total",
            not contract["full_cell_total_available_from_graphite_only"],
        ),
        (
            "citation_doi",
            external["doi"] == "10.1149/1945-7111/ad4918",
        ),
        (
            "citation_not_specific_validation",
            not external["specific_graphite_four_transition_sign_scale_supported"],
        ),
        (
            "prior_reference_fail",
            not inherited["half_cell_reference_closure_pass"],
        ),
        (
            "prior_code_fail",
            not inherited["theory_code_electronic_conformance_pass"],
        ),
        (
            "prior_doping_fail",
            not inherited["doped_high_voltage_coverage_pass"],
        ),
        (
            "not_repaired",
            not inherited["unchanged_heat_ast_means_repaired"],
        ),
        ("finding_count", summary["finding_count"] == 13),
        (
            "release_class",
            dispositions["release_delta_class"]
            == "WORKED_EXPLANATION_NOT_NEW_HEAT_IMPLEMENTATION",
        ),
        (
            "numeric_preserve",
            dispositions["worked_example_numbers"]
            == "PRESERVE_NUMERIC_ROUND_TRIP",
        ),
        (
            "width_conditional",
            dispositions["width_temperature_model"]
            == "CONDITIONAL_MODEL_CHOICE_NOT_MATERIAL_FACT",
        ),
        (
            "half_cell_preserve",
            dispositions["graphite_half_cell_quantity"]
            == "PRESERVE_DECLARED_HALF_CELL_REACTION_QUANTITY",
        ),
        (
            "api_boundary",
            dispositions["direction_label_mapping"]
            == "DOCUMENTED_BUT_NOT_TYPE_SAFE",
        ),
        (
            "full_cell_guard",
            dispositions["full_cell_translation"]
            == "REQUIRE_CATHODE_MINUS_ANODE_ASSEMBLY",
        ),
        (
            "citation_reject",
            dispositions["calorimetry_citation_scope"]
            == "REJECT_AS_SPECIFIC_GRAPHITE_SIGN_SCALE_VALIDATION",
        ),
        (
            "manuscript_boundary",
            dispositions["manuscript_code_boundary"]
            == "FAIL_USER_THEORY_ONLY_BODY_CONSTRAINT",
        ),
        (
            "internal_only",
            dispositions["experimental_authority"]
            == "INTERNAL_SELF_CONSISTENCY_ONLY",
        ),
        ("summary_not_new", not summary["new_heat_implementation_pass"]),
        ("summary_algebra", summary["worked_example_algebra_pass"]),
        ("summary_code", summary["worked_example_code_match_pass"]),
        (
            "summary_half_cell",
            summary["graphite_half_cell_internal_quantity_pass"],
        ),
        (
            "summary_api_fail",
            not summary["reaction_coordinate_api_safety_pass"],
        ),
        (
            "summary_full_cell_fail",
            not summary["full_cell_heat_authority_pass"],
        ),
        (
            "summary_external_fail",
            not summary["external_material_validation_pass"],
        ),
        (
            "summary_boundary_fail",
            not summary["theory_only_manuscript_boundary_pass"],
        ),
        ("next", summary["next_step"] == "37.4"),
        ("report_title", report.startswith("# Phase 059 v1.0.15")),
        ("report_status", STATUS in report),
        ("report_worked", "74.351" in report and "60.806" in report),
        ("report_quantity", "quantity·reference·sign" in report),
        ("report_boundary", "생산 코드와 함수명을 직접 두 번" in report),
        ("report_next", "Step 37.4" in report),
        ("report_source_guard", "원본 `Claude/`, `main`" in report),
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
    print(f"PASS_P059_V1015_HEAT_DETAILING_{len(checks)}_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
