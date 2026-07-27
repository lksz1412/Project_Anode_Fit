#!/usr/bin/env python3
"""Render and inspect every page of the eight Phase 058 legacy PDFs."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
TMP = ROOT / "tmp" / "pdfs" / "phase058"
OUT = ROOT / "Codex" / "results" / "PHASE_058_PDF_RENDER_METRICS.json"
PDFS = [
    "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.pdf",
    "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.pdf",
    "Claude/docs/v1.0.11/graphite_ica_ch1_v1.0.11.pdf",
    "Claude/docs/v1.0.11/graphite_ica_ch2_v1.0.11.pdf",
    "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.pdf",
    "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.pdf",
    "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.pdf",
    "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.pdf",
]
RENDER_DPI = 96
CONTACT_COLUMNS = 4
CONTACT_ROWS = 4
THUMBNAIL_WIDTH = 300
LABEL_HEIGHT = 26


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tex_for_pdf(relative_pdf: str) -> Path:
    return ROOT / str(Path(relative_pdf).with_suffix(".tex"))


def page_number(path: Path) -> int:
    match = re.search(r"-(\d+)\.png$", path.name)
    if not match:
        raise ValueError(f"Cannot parse page number: {path}")
    return int(match.group(1))


def verify_png(path: Path) -> bool:
    try:
        with Image.open(path) as image:
            image.verify()
        return True
    except Exception:
        return False


def repair_invalid_renders(source: Path, page_paths: list[Path]) -> list[int]:
    repaired = []
    for path in page_paths:
        if verify_png(path):
            continue
        number = page_number(path)
        replacement_prefix = path.parent / f"repair-{number:03d}"
        completed = subprocess.run(
            [
                "pdftoppm",
                "-f",
                str(number),
                "-l",
                str(number),
                "-singlefile",
                "-r",
                str(RENDER_DPI),
                "-png",
                str(source),
                str(replacement_prefix),
            ],
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        replacement = replacement_prefix.with_suffix(".png")
        if completed.returncode != 0 or not replacement.exists() or not verify_png(replacement):
            raise RuntimeError(
                f"Single-page render repair failed for {source} page {number}: "
                f"{completed.stderr}"
            )
        replacement.replace(path)
        repaired.append(number)
    return repaired


def raster_metrics(path: Path, text_char_count: int) -> dict:
    with Image.open(path) as source:
        grayscale = np.asarray(source.convert("L"), dtype=np.uint8)
    nonwhite = grayscale < 245
    dark = grayscale < 180
    rows, columns = np.nonzero(nonwhite)
    if rows.size:
        bbox = [
            int(columns.min()),
            int(rows.min()),
            int(columns.max()),
            int(rows.max()),
        ]
        margins = {
            "left_px": bbox[0],
            "top_px": bbox[1],
            "right_px": int(grayscale.shape[1] - 1 - bbox[2]),
            "bottom_px": int(grayscale.shape[0] - 1 - bbox[3]),
        }
    else:
        bbox = None
        margins = None
    edge = np.concatenate(
        [
            dark[:3, :].ravel(),
            dark[-3:, :].ravel(),
            dark[:, :3].ravel(),
            dark[:, -3:].ravel(),
        ]
    )
    nonwhite_fraction = float(np.mean(nonwhite))
    return {
        "render_path": str(path.relative_to(ROOT)),
        "pixel_width": int(grayscale.shape[1]),
        "pixel_height": int(grayscale.shape[0]),
        "mean_gray": float(np.mean(grayscale)),
        "std_gray": float(np.std(grayscale)),
        "nonwhite_fraction_lt245": nonwhite_fraction,
        "dark_fraction_lt180": float(np.mean(dark)),
        "edge_dark_fraction_3px": float(np.mean(edge)),
        "content_bbox_lt245": bbox,
        "content_margins_px": margins,
        "blank_candidate": bool(
            (nonwhite_fraction < 0.0005 or float(np.std(grayscale)) < 2.0)
            and text_char_count < 10
        ),
        "edge_touch_candidate": bool(np.any(edge)),
    }


def make_contact_sheets(pdf_id: str, page_paths: list[Path]) -> list[str]:
    contacts_dir = TMP / "contacts"
    contacts_dir.mkdir(parents=True, exist_ok=True)
    records = []
    per_sheet = CONTACT_COLUMNS * CONTACT_ROWS
    font = ImageFont.load_default()
    for start in range(0, len(page_paths), per_sheet):
        group = page_paths[start : start + per_sheet]
        thumbnails: list[tuple[Path, Image.Image]] = []
        max_height = 0
        for path in group:
            with Image.open(path) as source:
                image = source.convert("RGB")
            height = round(image.height * THUMBNAIL_WIDTH / image.width)
            image.thumbnail((THUMBNAIL_WIDTH, height), Image.Resampling.LANCZOS)
            max_height = max(max_height, image.height)
            thumbnails.append((path, image.copy()))
        cell_height = LABEL_HEIGHT + max_height
        sheet = Image.new(
            "RGB",
            (CONTACT_COLUMNS * THUMBNAIL_WIDTH, CONTACT_ROWS * cell_height),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        for index, (path, image) in enumerate(thumbnails):
            row, column = divmod(index, CONTACT_COLUMNS)
            x = column * THUMBNAIL_WIDTH
            y = row * cell_height
            label = f"{pdf_id} p.{page_number(path)}"
            draw.rectangle(
                [x, y, x + THUMBNAIL_WIDTH - 1, y + cell_height - 1],
                outline=(150, 150, 150),
                width=1,
            )
            draw.text((x + 5, y + 5), label, fill="black", font=font)
            sheet.paste(image, (x, y + LABEL_HEIGHT))
        first_page = page_number(group[0])
        last_page = page_number(group[-1])
        output = contacts_dir / f"{pdf_id}_pages_{first_page:03d}_{last_page:03d}.png"
        sheet.save(output)
        records.append(str(output.relative_to(ROOT)))
    return records


def render_pdf(relative: str) -> dict:
    source = ROOT / relative
    pdf_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", source.stem)
    render_dir = TMP / "pages" / pdf_id
    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / "page"
    completed = subprocess.run(
        [
            "pdftoppm",
            "-r",
            str(RENDER_DPI),
            "-png",
            str(source),
            str(prefix),
        ],
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"pdftoppm failed for {relative}: {completed.stderr}")
    page_paths = sorted(render_dir.glob("page-*.png"), key=page_number)
    repaired_pages = repair_invalid_renders(source, page_paths)
    reader = PdfReader(source)
    extracted_text = []
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        extracted_text.append(text)
        raster = raster_metrics(page_paths[index - 1], len(text))
        media = page.mediabox
        crop = page.cropbox
        pages.append(
            {
                "page": index,
                "text_char_count": len(text),
                "replacement_char_count": text.count("\ufffd"),
                "nul_char_count": text.count("\x00"),
                "media_box_points": [
                    float(media.left),
                    float(media.bottom),
                    float(media.right),
                    float(media.top),
                ],
                "crop_box_points": [
                    float(crop.left),
                    float(crop.bottom),
                    float(crop.right),
                    float(crop.top),
                ],
                "crop_differs_from_media": list(media) != list(crop),
                **raster,
            }
        )
    fonts = subprocess.run(
        ["pdffonts", str(source)],
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    tex = tex_for_pdf(relative)
    return {
        "pdf_id": pdf_id,
        "path": relative,
        "sha256": sha256(source),
        "size_bytes": source.stat().st_size,
        "page_count_pdf": len(reader.pages),
        "page_count_rendered": len(page_paths),
        "renderer_repaired_pages": repaired_pages,
        "encrypted": bool(reader.is_encrypted),
        "metadata": {str(key): str(value) for key, value in (reader.metadata or {}).items()},
        "tex_path": str(tex.relative_to(ROOT)) if tex.exists() else None,
        "tex_sha256": sha256(tex) if tex.exists() else None,
        "tex_line_count": len(tex.read_text(encoding="utf-8").splitlines()) if tex.exists() else None,
        "total_extracted_text_chars": sum(len(text) for text in extracted_text),
        "replacement_char_count": sum(text.count("\ufffd") for text in extracted_text),
        "blank_candidate_pages": [
            page["page"] for page in pages if page["blank_candidate"]
        ],
        "edge_touch_candidate_pages": [
            page["page"] for page in pages if page["edge_touch_candidate"]
        ],
        "crop_differs_from_media_pages": [
            page["page"] for page in pages if page["crop_differs_from_media"]
        ],
        "pdffonts_returncode": fonts.returncode,
        "pdffonts_stdout": fonts.stdout,
        "pdffonts_stderr": fonts.stderr,
        "contact_sheets": make_contact_sheets(pdf_id, page_paths),
        "pages": pages,
    }


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    before = {relative: sha256(ROOT / relative) for relative in PDFS}
    documents = [render_pdf(relative) for relative in PDFS]
    after = {relative: sha256(ROOT / relative) for relative in PDFS}
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "render_dpi": RENDER_DPI,
        "pdf_count": len(documents),
        "total_pdf_pages": sum(document["page_count_pdf"] for document in documents),
        "total_rendered_pages": sum(
            document["page_count_rendered"] for document in documents
        ),
        "total_contact_sheets": sum(
            len(document["contact_sheets"]) for document in documents
        ),
        "source_hashes_before": before,
        "source_hashes_after": after,
        "sources_unchanged": before == after,
        "documents": documents,
        "summary": {
            "page_count_matches_all": all(
                document["page_count_pdf"] == document["page_count_rendered"]
                for document in documents
            ),
            "blank_candidate_count": sum(
                len(document["blank_candidate_pages"]) for document in documents
            ),
            "replacement_char_count": sum(
                document["replacement_char_count"] for document in documents
            ),
            "crop_differs_from_media_count": sum(
                len(document["crop_differs_from_media_pages"]) for document in documents
            ),
            "edge_touch_candidate_count": sum(
                len(document["edge_touch_candidate_pages"]) for document in documents
            ),
        },
        "visual_review_status": "PENDING_CONTACT_SHEET_AND_TARGET_PAGE_INSPECTION",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
