#!/usr/bin/env python3
"""Validate the deterministic Phase 059 PDF render-audit artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
METRICS_PATH = ROOT / "Codex/results/PHASE_059_PDF_RENDER_METRICS.json"
VISUAL_PATH = ROOT / "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json"
REPORT_PATH = ROOT / "Codex/results/PHASE_059_ARTIFACT_RENDER_AUDIT.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    visual = json.loads(VISUAL_PATH.read_text(encoding="utf-8"))
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    check("metrics_schema", metrics["schema_version"] == 1)
    check("visual_schema", visual["schema_version"] == 1)
    check("pdf_count_18", metrics["pdf_count"] == 18)
    check("pdf_pages_492", metrics["total_pdf_pages"] == 492)
    check("rendered_pages_492", metrics["total_rendered_pages"] == 492)
    check("contact_sheets_37", metrics["total_contact_sheets"] == 37)
    check("source_hashes_unchanged", metrics["sources_unchanged"])
    check("all_page_counts_match", metrics["summary"]["page_count_matches_all"])
    check("invalid_renders_zero", metrics["summary"]["invalid_render_count"] == 0)
    check("blank_candidates_zero", metrics["summary"]["blank_candidate_count"] == 0)
    check(
        "replacement_chars_zero",
        metrics["summary"]["replacement_char_count"] == 0,
    )
    check("nul_count_3117", metrics["summary"]["nul_char_count"] == 3117)
    check(
        "crop_differences_zero",
        metrics["summary"]["crop_differs_from_media_count"] == 0,
    )
    check(
        "edge_touch_candidates_zero",
        metrics["summary"]["edge_touch_candidate_count"] == 0,
    )
    check(
        "near_edge_candidates_zero",
        metrics["summary"]["near_edge_candidate_count"] == 0,
    )
    check(
        "out_of_bounds_chars_zero",
        metrics["summary"]["out_of_bounds_char_page_count"] == 0,
    )
    check(
        "out_of_bounds_words_zero",
        metrics["summary"]["out_of_bounds_word_page_count"] == 0,
    )
    check(
        "pdffonts_commands_succeeded",
        metrics["summary"]["all_pdffonts_commands_succeeded"],
    )
    check("all_fonts_embedded", metrics["summary"]["all_fonts_embedded"])
    check(
        "unicode_map_debt_present",
        not metrics["summary"]["all_fonts_have_unicode_maps"],
    )
    check("visual_documents_18", len(visual["documents"]) == 18)
    check(
        "visual_contact_sheets_37",
        visual["scope"]["contact_sheets_visually_inspected"] == 37,
    )
    check(
        "visual_page_coverage_492",
        visual["scope"]["pages_covered_by_contact_sheets"] == 492,
    )
    check(
        "full_resolution_targets_13",
        visual["scope"]["full_resolution_target_count"] == 13,
    )
    check(
        "intermediate_render_policy",
        visual["intermediate_render_policy"]
        == "TRANSIENT_DELETE_AFTER_VALIDATION_REGENERATE_WITH_RENDER_SCRIPT",
    )
    check(
        "all_contacts_marked_inspected",
        all(
            contact["visual_status"] == "VISUALLY_INSPECTED_PASS"
            for document in visual["documents"]
            for contact in document["contact_sheets"]
        ),
    )
    check(
        "all_targets_marked_inspected",
        all(
            target["visual_status"] == "FULL_RESOLUTION_VISUALLY_INSPECTED"
            for target in visual["full_resolution_targets"]
        ),
    )
    check(
        "all_target_hashes_matched_at_review",
        all(
            target["render_exists_at_review"]
            and target["render_hash_matches_at_review"]
            for target in visual["full_resolution_targets"]
        ),
    )
    check(
        "all_named_destinations_valid",
        all(
            not document["link_audit"]["invalid_named_destinations"]
            for document in visual["documents"]
        ),
    )
    check(
        "broken_footnote_return_links_26",
        sum(
            len(document["link_audit"]["unresolved_goto_links"])
            for document in visual["documents"]
        )
        == 26
        and all(
            link["destination"].startswith("Hfootnote.")
            for document in visual["documents"]
            for link in document["link_audit"]["unresolved_goto_links"]
        ),
    )
    check(
        "no_unsupported_link_actions",
        all(
            not document["link_audit"]["unsupported_link_actions"]
            for document in visual["documents"]
        ),
    )
    check(
        "unresolved_markers_zero",
        sum(
            document["link_audit"]["unresolved_double_question_mark_count"]
            for document in visual["documents"]
        )
        == 0,
    )
    check(
        "only_v1016_appendix_version_mismatch",
        [
            document["pdf_id"]
            for document in visual["documents"]
            if document["link_audit"]["first_page_version_label_applicable"]
            and not document["link_audit"]["first_page_contains_expected_version"]
        ]
        == ["v1_0_16__appendix_phase_separation"],
    )
    check(
        "chapter2_title_version_not_applicable",
        all(
            not document["link_audit"]["first_page_version_label_applicable"]
            and document["link_audit"]["first_page_version_disposition"]
            == "NOT_APPLICABLE_NO_TITLE_PAGE_VERSION"
            for document in visual["documents"]
            if document["document_kind"] == "chapter2"
        ),
    )
    check(
        "v1016_appendix_tex_is_v1015_copy",
        visual["v1016_appendix_provenance"]["tex_exact_identical"],
    )
    check(
        "v1016_appendix_render_is_v1015_copy",
        visual["v1016_appendix_provenance"][
            "rendered_page_hashes_exact_identical"
        ],
    )
    check(
        "finding_ids_exact",
        [finding["id"] for finding in visual["findings"]]
        == ["PDF-059-01", "PDF-059-02", "PDF-059-03", "PDF-059-04"],
    )
    check(
        "status_conditional",
        visual["status"]
        == "CONDITIONAL_P059_PDF_RENDER_PASS_WITH_ACCESSIBILITY_AND_PROVENANCE_DEBTS",
    )
    check(
        "metrics_hash_linked",
        visual["metrics_sha256"] == sha256(METRICS_PATH),
    )
    check("report_exists", REPORT_PATH.exists())
    check(
        "report_has_claim_boundary",
        "식의 물리적 타당성" in REPORT_PATH.read_text(encoding="utf-8"),
    )

    failures = [name for name, passed in checks if not passed]
    for index, (name, passed) in enumerate(checks, start=1):
        print(f"{index:02d} {'PASS' if passed else 'FAIL'} {name}")
    print(f"SUMMARY {len(checks) - len(failures)}/{len(checks)} PASS")
    if failures:
        raise SystemExit("failed checks: " + ", ".join(failures))


if __name__ == "__main__":
    main()
