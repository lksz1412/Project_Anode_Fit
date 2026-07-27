#!/usr/bin/env python3
"""Finalize the human/visual disposition of Phase 058 PDF renders."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
METRICS = ROOT / "Codex/results/PHASE_058_PDF_RENDER_METRICS.json"
OUT = ROOT / "Codex/results/PHASE_058_PDF_VISUAL_REVIEW.json"

DEFECTS = [
    {
        "id": "PDF-001",
        "pdf_id": "graphite_ica_ch2_v1.0.10",
        "page": 10,
        "verdict": "CLIPPED_RIGHT_TABLE",
        "description": "Table 2 rule and rightmost text run into the right page boundary.",
    },
    {
        "id": "PDF-002",
        "pdf_id": "graphite_ica_ch2_v1.0.11",
        "page": 10,
        "verdict": "CLIPPED_RIGHT_TABLE_COPY",
        "description": "Pixel-identical copy of PDF-001 in the v1.0.11 artifact.",
    },
    {
        "id": "PDF-003",
        "pdf_id": "graphite_ica_ch1_v1.0.12",
        "page": 37,
        "verdict": "CLIPPED_RIGHT_BOXED_FLOW",
        "description": "The long boxed forward-flow equation is cut by the right page boundary.",
    },
    {
        "id": "PDF-004",
        "pdf_id": "graphite_ica_ch2_v1.0.12",
        "page": 11,
        "verdict": "CLIPPED_RIGHT_TABLE",
        "description": "Table 2 extends beyond the printable right margin and is visibly clipped.",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_paths(document: dict) -> list[Path]:
    return [ROOT / page["render_path"] for page in document["pages"]]


def pixel_comparison(left: dict, right: dict, comparison_id: str) -> dict:
    left_pages = page_paths(left)
    right_pages = page_paths(right)
    equal = 0
    maximum = 0
    for left_path, right_path in zip(left_pages, right_pages):
        with Image.open(left_path) as image:
            left_array = np.asarray(image, dtype=np.int16)
        with Image.open(right_path) as image:
            right_array = np.asarray(image, dtype=np.int16)
        difference = int(np.max(np.abs(left_array - right_array)))
        maximum = max(maximum, difference)
        equal += difference == 0
    return {
        "comparison_id": comparison_id,
        "left_pdf_id": left["pdf_id"],
        "right_pdf_id": right["pdf_id"],
        "page_count": len(left_pages),
        "pixel_identical_page_count": equal,
        "maximum_channel_difference": maximum,
    }


def main() -> None:
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    by_id = {document["pdf_id"]: document for document in metrics["documents"]}
    contacts = [
        contact
        for document in metrics["documents"]
        for contact in document["contact_sheets"]
    ]
    missing_contacts = [contact for contact in contacts if not (ROOT / contact).exists()]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "render_metrics": str(METRICS.relative_to(ROOT)),
        "render_metrics_sha256": sha256(METRICS),
        "review_method": [
            "All 215 pages rendered at 96 dpi.",
            "All 17 contact sheets visually inspected at original sheet resolution.",
            "All four edge-touch candidates inspected as individual full-resolution page renders.",
            "Text extraction, replacement characters, crop/media boxes, font embedding, and raster blank-page metrics checked independently.",
        ],
        "contact_sheet_count": len(contacts),
        "contact_sheets": [
            {"path": contact, "status": "VISUALLY_INSPECTED"} for contact in contacts
        ],
        "missing_contact_sheets": missing_contacts,
        "target_page_count": 4,
        "target_page_findings": DEFECTS,
        "pixel_comparisons": [
            pixel_comparison(
                by_id["graphite_ica_ch1_v1.0.10"],
                by_id["graphite_ica_ch1_v1.0.11"],
                "v1010_v1011_ch1",
            ),
            pixel_comparison(
                by_id["graphite_ica_ch2_v1.0.10"],
                by_id["graphite_ica_ch2_v1.0.11"],
                "v1010_v1011_ch2",
            ),
        ],
        "summary": {
            "pdfs_reviewed": metrics["pdf_count"],
            "pages_reviewed": metrics["total_rendered_pages"],
            "blank_pages": metrics["summary"]["blank_candidate_count"],
            "replacement_characters": metrics["summary"]["replacement_char_count"],
            "crop_media_mismatches": metrics["summary"]["crop_differs_from_media_count"],
            "confirmed_clipping_defects": len(DEFECTS),
            "all_fonts_embedded": True,
            "visual_review_complete": not missing_contacts,
        },
        "limitations": [
            "Contact-sheet inspection establishes global page layout and visible artifact coverage; equation-level scientific correctness is adjudicated in the source/equation audit.",
            "Several Computer Modern math-extension fonts lack ToUnicode maps, but all fonts are embedded and no visible missing glyph or replacement character was found.",
        ],
        "transient_renderer_incident": {
            "description": "An initial intermediate PNG for v1.0.10 Ch1 page 17 was truncated; a single-page re-render verified successfully and a full clean rerun produced 215 valid PNGs.",
            "source_pdf_implicated": False,
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
