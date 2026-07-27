#!/usr/bin/env python3
"""Finalize the Phase 059 PDF visual, link, and provenance review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
METRICS_PATH = ROOT / "Codex/results/PHASE_059_PDF_RENDER_METRICS.json"
OUTPUT_PATH = ROOT / "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json"
REPORT_PATH = ROOT / "Codex/results/PHASE_059_ARTIFACT_RENDER_AUDIT.md"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"

TARGET_PAGES = [
    {
        "pdf_id": "v1_0_16__appendix_phase_separation",
        "page": 1,
        "selection_basis": "version-label provenance check",
        "observation": (
            "Rendered cleanly, but the visible title says version 1.0.15 "
            "inside the v1.0.16 directory."
        ),
    },
    {
        "pdf_id": "v1_0_18_2__appendix_phase_separation",
        "page": 5,
        "selection_basis": "densest appendix page with two figures",
        "observation": "Both figures, axes, captions, and following heading are intact.",
    },
    {
        "pdf_id": "v1_0_14__graphite_ica_ch1_v1.0.14",
        "page": 20,
        "selection_basis": "densest v1.0.14 Chapter 1 page",
        "observation": "Figure, caption, equations, and body remain inside the page.",
    },
    {
        "pdf_id": "v1_0_17__graphite_ica_ch1_v1.0.17",
        "page": 25,
        "selection_basis": "densest v1.0.17 Chapter 1 page",
        "observation": "Dense prose and inline mathematics remain legible and unclipped.",
    },
    {
        "pdf_id": "v1_0_18_2__graphite_ica_ch1_v1.0.18.2",
        "page": 25,
        "selection_basis": "densest latest Chapter 1 page",
        "observation": "Dense prose and inline mathematics remain legible and unclipped.",
    },
    {
        "pdf_id": "v1_0_18_2__graphite_ica_ch1_v1.0.18.2",
        "page": 50,
        "selection_basis": "high NUL-extraction count and boxed equations",
        "observation": (
            "All visible mathematical delimiters and boxed equations render; "
            "the defect is extraction, not display."
        ),
    },
    {
        "pdf_id": "v1_0_18_2__graphite_ica_ch1_v1.0.18.2",
        "page": 55,
        "selection_basis": "smallest measured right margin and two wide tables",
        "observation": "Both tables remain within the page; no right-edge clipping is visible.",
    },
    {
        "pdf_id": "v1_0_14__graphite_ica_ch1_v1.0.14",
        "page": 49,
        "selection_basis": "high NUL-extraction count and equation-flow diagram",
        "observation": (
            "Integral delimiters, arrows, equations, and flow diagram render visibly."
        ),
    },
    {
        "pdf_id": "v1_0_14__graphite_ica_ch2_v1.0.14",
        "page": 12,
        "selection_basis": "densest v1.0.14 Chapter 2 page",
        "observation": "Boxed heat equations and body text remain intact.",
    },
    {
        "pdf_id": "v1_0_16__graphite_ica_ch2_v1.0.16",
        "page": 10,
        "selection_basis": "densest v1.0.16 Chapter 2 page",
        "observation": "Bullets, equations, and headings remain intact.",
    },
    {
        "pdf_id": "v1_0_18_2__graphite_ica_ch2_v1.0.18.2",
        "page": 7,
        "selection_basis": "latest Chapter 2 page containing an extracted NUL",
        "observation": (
            "Large mathematical brackets and equations render visibly; "
            "the single NUL is a text-extraction defect."
        ),
    },
    {
        "pdf_id": "v1_0_18_2__graphite_ica_ch2_v1.0.18.2",
        "page": 11,
        "selection_basis": "densest latest Chapter 2 page",
        "observation": "Dense bullets and equations remain legible and unclipped.",
    },
    {
        "pdf_id": "v1_0_18_2__graphite_ica_ch2_v1.0.18.2",
        "page": 17,
        "selection_basis": "new final reference page",
        "observation": (
            "References are intact; the lower-page whitespace is intentional, not blank loss."
        ),
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_links_and_labels(document: dict) -> dict:
    path = ROOT / document["path"]
    reader = PdfReader(path)
    named = reader.named_destinations
    invalid_named_destinations = []
    for name, destination in named.items():
        try:
            page_number = reader.get_destination_page_number(destination)
        except Exception as exc:  # pragma: no cover - recorded as audit evidence
            invalid_named_destinations.append(
                {"name": name, "error": type(exc).__name__}
            )
            continue
        if page_number < 0 or page_number >= len(reader.pages):
            invalid_named_destinations.append(
                {"name": name, "page_index": page_number}
            )

    link_count = 0
    goto_link_count = 0
    unresolved_goto_links = []
    unsupported_link_actions = []
    unresolved_marker_count = 0
    page_one_text = ""
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if page_number == 1:
            page_one_text = text
        unresolved_marker_count += text.count("??")
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if str(annotation.get("/Subtype")) != "/Link":
                continue
            link_count += 1
            action = annotation.get("/A")
            destination = annotation.get("/Dest")
            if action is not None:
                action = action.get_object()
                action_kind = str(action.get("/S"))
                destination = action.get("/D")
                if action_kind != "/GoTo":
                    unsupported_link_actions.append(
                        {"page": page_number, "action": action_kind}
                    )
                    continue
            if destination is None:
                unresolved_goto_links.append(
                    {"page": page_number, "destination": None}
                )
                continue
            goto_link_count += 1
            if isinstance(destination, str) and destination not in named:
                unresolved_goto_links.append(
                    {"page": page_number, "destination": destination}
                )

    expected_version = document["version"].removeprefix("v")
    version_label_applicable = document["document_kind"] in {
        "appendix",
        "chapter1",
    }
    version_match = (
        expected_version in page_one_text if version_label_applicable else None
    )
    return {
        "named_destination_count": len(named),
        "invalid_named_destinations": invalid_named_destinations,
        "link_count": link_count,
        "goto_link_count": goto_link_count,
        "unresolved_goto_links": unresolved_goto_links,
        "unsupported_link_actions": unsupported_link_actions,
        "unresolved_double_question_mark_count": unresolved_marker_count,
        "first_page_version_label_applicable": version_label_applicable,
        "first_page_contains_expected_version": version_match,
        "expected_version": expected_version,
        "first_page_version_disposition": (
            "MATCH"
            if version_match
            else "MISMATCH"
            if version_label_applicable
            else "NOT_APPLICABLE_NO_TITLE_PAGE_VERSION"
        ),
    }


def selected_page_record(document: dict, page_number: int) -> dict:
    page = next(page for page in document["pages"] if page["page"] == page_number)
    render = ROOT / page["render_path"]
    return {
        "render_path": page["render_path"],
        "render_sha256": page["render_sha256"],
        "render_exists_at_review": render.exists(),
        "render_hash_matches_at_review": (
            render.exists() and sha256(render) == page["render_sha256"]
        ),
        "content_margins_px": page["content_margins_px"],
        "nonwhite_fraction_lt245": page["nonwhite_fraction_lt245"],
        "nul_char_count": page["nul_char_count"],
    }


def build_report(payload: dict) -> str:
    lines = [
        "# Phase 059 PDF artifact render audit",
        "",
        "정본일: 2026-07-28",
        "",
        f"판정: `{payload['status']}`",
        "",
        "## 범위와 경계",
        "",
        (
            "v1.0.14–v1.0.18.2의 18 PDF, 492 pages를 96 dpi로 전부 "
            "render했고 37 contact sheets를 모두 육안 검독했다. 기계적으로 "
            "선별한 고밀도·최소여백·수식추출·표·마지막 페이지 13쪽은 "
            "원해상도로 다시 확인했다."
        ),
        "",
        (
            "이 판정은 artifact 가독성, 내부 link, 글꼴 embedding과 provenance에 "
            "대한 것이다. 식의 물리적 타당성, 문헌 진실성, 코드 정합 또는 "
            "실험 데이터 설명력을 이 결과만으로 승인하지 않는다."
        ),
        "",
        (
            "전 페이지 PNG와 contact sheet는 검증 후 삭제하는 일시 중간물이다. "
            "재현 가능한 script, source/render hash, 기계 metrics와 육안 판정만 "
            "repository에 보존한다."
        ),
        "",
        "## 결론",
        "",
        (
            "- 가시적 render는 통과했다. blank, 깨진 PNG, crop/media 불일치, "
            "page-boundary 밖 문자·단어, edge-touch, 잘린 식·표·그림을 찾지 못했다."
        ),
        "",
        (
            "- 18 PDF의 모든 font는 embedded 상태다. 그러나 모든 PDF에 "
            "ToUnicode map이 없는 CMEX10이 있고 Chapter 1에는 CMSY10도 있어, "
            "pypdf 추출에서 NUL 3,117자가 발생한다. 화면 표시가 아니라 "
            "검색·복사·접근성 결함이다."
        ),
        "",
        (
            "- v1.0.16 `appendix_phase_separation`은 v1.0.15 TeX와 exact-identical이고 "
            "8쪽 render도 전부 exact-identical이다. 표지에는 실제로 "
            "`버전 1.0.15 초안`이 남아 있으므로 v1.0.16 provenance를 주장할 수 없다."
        ),
        "",
        (
            "- 등록된 named destination 자체는 모두 유효 page를 가리키고 본문의 "
            "`??` 표지는 0이다. 그러나 각주 복귀용 `Hfootnote.*` GoTo link "
            "26개는 name tree에 목적지가 없어 끊겨 있다."
        ),
        "",
        "## 문서별 기계·링크 검사",
        "",
        "| version | document | pages | contacts | NUL | fonts embedded | all ToUnicode | links | version label |",
        "|---|---|---:|---:|---:|---|---|---:|---|",
    ]
    for document in payload["documents"]:
        lines.append(
            "| {version} | {kind} | {pages} | {contacts} | {nul} | {embedded} | "
            "{unicode} | {links} | {label} |".format(
                version=document["version"],
                kind=document["document_kind"],
                pages=document["page_count"],
                contacts=document["contact_sheet_count"],
                nul=document["nul_char_count"],
                embedded="yes" if document["all_fonts_embedded"] else "no",
                unicode="yes" if document["all_fonts_have_unicode_maps"] else "no",
                links=document["link_audit"]["link_count"],
                label=document["link_audit"]["first_page_version_disposition"],
            )
        )
    lines.extend(
        [
            "",
            "## 원해상도 표적 검수",
            "",
            "| PDF | page | 선별 이유 | 판정 |",
            "|---|---:|---|---|",
        ]
    )
    for target in payload["full_resolution_targets"]:
        lines.append(
            f"| `{target['pdf_id']}` | {target['page']} | "
            f"{target['selection_basis']} | {target['observation']} |"
        )
    lines.extend(
        [
            "",
            "## Finding register",
            "",
            "| ID | 판정 | 내용 | 후속 처리 |",
            "|---|---|---|---|",
            (
                "| PDF-059-01 | PASS | 492/492 pages와 37/37 contact sheets의 "
                "가시적 layout 이상 없음 | Phase 35.3에서 생성 계보 연결 |"
            ),
            (
                "| PDF-059-02 | EVIDENCE_DEBT | 18/18 PDF에 non-ToUnicode math "
                "font; 추출 NUL 3,117 | 최종 문건 build에서 Unicode math 또는 "
                "actual-text layer 검증 gate 추가 |"
            ),
            (
                "| PDF-059-03 | PROVENANCE_DEFECT | v1.0.16 appendix가 v1.0.15 "
                "source/render copy이고 표지도 v1.0.15 | v1.0.16의 새 appendix "
                "증거로 계수 금지 |"
            ),
            (
                "| PDF-059-04 | LINK_DEFECT | 등록된 named destination은 유효하고 "
                "`??`는 0이나 `Hfootnote.*` 목적지 26개가 누락 | 최종 build에서 "
                "각주 복귀 link target 검증 gate 추가 |"
            ),
            "",
            "## 다음 단계",
            "",
            (
                "Step 35.2에서 10 standalone image의 원해상도 축·단위·legend·조건·"
                "peak morphology와 생성 source를 감사한다."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    documents_by_id = {
        document["pdf_id"]: document for document in metrics["documents"]
    }
    documents = []
    for document in metrics["documents"]:
        links = audit_links_and_labels(document)
        documents.append(
            {
                "pdf_id": document["pdf_id"],
                "version": document["version"],
                "document_kind": document["document_kind"],
                "path": document["path"],
                "sha256": document["sha256"],
                "tex_path": document["tex_path"],
                "tex_sha256": document["tex_sha256"],
                "page_count": document["page_count_pdf"],
                "contact_sheet_count": len(document["contact_sheets"]),
                "contact_sheets": [
                    {
                        **contact,
                        "visual_status": "VISUALLY_INSPECTED_PASS",
                    }
                    for contact in document["contact_sheets"]
                ],
                "nul_char_count": document["nul_char_count"],
                "replacement_char_count": document["replacement_char_count"],
                "all_fonts_embedded": document["font_metrics"]["all_embedded"],
                "all_fonts_have_unicode_maps": document["font_metrics"]["all_unicode"],
                "fonts_without_unicode_maps": [
                    font
                    for font in document["font_metrics"]["fonts"]
                    if not font["unicode"]
                ],
                "link_audit": links,
            }
        )

    targets = []
    for target in TARGET_PAGES:
        document = documents_by_id[target["pdf_id"]]
        targets.append(
            {
                **target,
                **selected_page_record(document, target["page"]),
                "visual_status": "FULL_RESOLUTION_VISUALLY_INSPECTED",
            }
        )

    v15_appendix = documents_by_id["v1_0_15__appendix_phase_separation"]
    v16_appendix = documents_by_id["v1_0_16__appendix_phase_separation"]
    v15_render_hashes = [
        page["render_sha256"] for page in v15_appendix["pages"]
    ]
    v16_render_hashes = [
        page["render_sha256"] for page in v16_appendix["pages"]
    ]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "metrics_path": str(METRICS_PATH.relative_to(ROOT)),
        "metrics_sha256": sha256(METRICS_PATH),
        "scope": {
            "pdf_count": metrics["pdf_count"],
            "pdf_page_count": metrics["total_pdf_pages"],
            "rendered_page_count": metrics["total_rendered_pages"],
            "contact_sheet_count": metrics["total_contact_sheets"],
            "contact_sheets_visually_inspected": metrics["total_contact_sheets"],
            "pages_covered_by_contact_sheets": metrics["total_pdf_pages"],
            "full_resolution_target_count": len(targets),
        },
        "intermediate_render_policy": (
            "TRANSIENT_DELETE_AFTER_VALIDATION_REGENERATE_WITH_RENDER_SCRIPT"
        ),
        "mechanical_summary": metrics["summary"],
        "documents": documents,
        "full_resolution_targets": targets,
        "v1016_appendix_provenance": {
            "v1015_tex_sha256": v15_appendix["tex_sha256"],
            "v1016_tex_sha256": v16_appendix["tex_sha256"],
            "tex_exact_identical": (
                v15_appendix["tex_sha256"] == v16_appendix["tex_sha256"]
            ),
            "rendered_page_hashes_exact_identical": (
                v15_render_hashes == v16_render_hashes
            ),
            "v1016_first_page_contains_v1016": documents[
                list(documents_by_id).index("v1_0_16__appendix_phase_separation")
            ]["link_audit"]["first_page_contains_expected_version"],
            "disposition": "STALE_COPY_FORWARD_NOT_NEW_V1016_EVIDENCE",
        },
        "findings": [
            {
                "id": "PDF-059-01",
                "status": "PASS",
                "claim": (
                    "All 492 pages rendered and all 37 contact sheets plus 13 "
                    "full-resolution target pages were visually inspected without "
                    "visible clipping, blank loss, or glyph-display failure."
                ),
            },
            {
                "id": "PDF-059-02",
                "status": "EVIDENCE_DEBT",
                "claim": (
                    "All 18 PDFs contain at least one math font without a ToUnicode "
                    "map, causing 3,117 extracted NUL characters."
                ),
            },
            {
                "id": "PDF-059-03",
                "status": "PROVENANCE_DEFECT",
                "claim": (
                    "The v1.0.16 appendix is an exact v1.0.15 TeX/render carry-forward "
                    "and visibly retains the v1.0.15 version label."
                ),
            },
            {
                "id": "PDF-059-04",
                "status": "LINK_DEFECT",
                "claim": (
                    "Registered named destinations resolve to in-range pages and no "
                    "extracted '??' marker is present, but 26 Hfootnote.* GoTo links "
                    "refer to destinations absent from the PDF name tree."
                ),
            },
        ],
        "claim_boundary": (
            "Render/link checks do not establish equation correctness, literature "
            "validity, code conformance, or experimental-data validity."
        ),
        "status": (
            "CONDITIONAL_P059_PDF_RENDER_PASS_WITH_ACCESSIBILITY_AND_PROVENANCE_DEBTS"
        ),
        "next_action": (
            "Run Step 35.2 standalone-image inspection, then connect artifact "
            "blobs to source and commit provenance in Step 35.3."
        ),
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    REPORT_PATH.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
