#!/usr/bin/env python3
"""Render and mechanically inspect every page of all 18 Phase 059 PDFs."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pdfplumber
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
TMP = ROOT / "tmp" / "pdfs" / "phase059"
OUT = ROOT / "Codex" / "results" / "PHASE_059_PDF_RENDER_METRICS.json"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
VERSIONS = [
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
]
PDF_NAMES = [
    "appendix_phase_separation.pdf",
    "graphite_ica_ch1_{version}.pdf",
    "graphite_ica_ch2_{version}.pdf",
]
PDFS = [
    f"Claude/docs/{version}/{name.format(version=version)}"
    for version in VERSIONS
    for name in PDF_NAMES
]
EXPECTED_PAGES = {
    "v1.0.14": [8, 57, 14],
    "v1.0.15": [8, 58, 16],
    "v1.0.16": [8, 58, 16],
    "v1.0.17": [8, 58, 16],
    "v1.0.18.1": [8, 59, 16],
    "v1.0.18.2": [8, 59, 17],
}
RENDER_DPI = 96
CONTACT_COLUMNS = 4
CONTACT_ROWS = 4
THUMBNAIL_WIDTH = 300
LABEL_HEIGHT = 26


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_id(relative: str) -> str:
    path = Path(relative)
    version = path.parent.name.replace(".", "_")
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem)
    return f"{version}__{stem}"


def tex_for_pdf(relative: str) -> Path:
    return ROOT / str(Path(relative).with_suffix(".tex"))


def page_number(path: Path) -> int:
    match = re.search(r"-(\d+)\.png$", path.name)
    if not match:
        raise ValueError(f"cannot parse page number: {path}")
    return int(match.group(1))


def verify_png(path: Path) -> bool:
    try:
        with Image.open(path) as image:
            image.verify()
        return True
    except Exception:
        return False


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
    edge_1 = np.concatenate(
        [
            dark[:1, :].ravel(),
            dark[-1:, :].ravel(),
            dark[:, :1].ravel(),
            dark[:, -1:].ravel(),
        ]
    )
    edge_3 = np.concatenate(
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
        "render_sha256": sha256(path),
        "pixel_width": int(grayscale.shape[1]),
        "pixel_height": int(grayscale.shape[0]),
        "mean_gray": float(np.mean(grayscale)),
        "std_gray": float(np.std(grayscale)),
        "nonwhite_fraction_lt245": nonwhite_fraction,
        "dark_fraction_lt180": float(np.mean(dark)),
        "edge_dark_fraction_1px": float(np.mean(edge_1)),
        "edge_dark_fraction_3px": float(np.mean(edge_3)),
        "content_bbox_lt245": bbox,
        "content_margins_px": margins,
        "blank_candidate": bool(
            (nonwhite_fraction < 0.0005 or float(np.std(grayscale)) < 2.0)
            and text_char_count < 10
        ),
        "edge_touch_candidate": bool(np.any(edge_1)),
        "near_edge_candidate": bool(
            margins is not None and min(margins.values()) <= 3
        ),
    }


def pdfplumber_metrics(page) -> dict:
    width = float(page.width)
    height = float(page.height)
    chars = page.chars
    words = page.extract_words() or []
    out_of_bounds_chars = [
        {
            "text": str(char.get("text", "")),
            "x0": float(char["x0"]),
            "x1": float(char["x1"]),
            "top": float(char["top"]),
            "bottom": float(char["bottom"]),
        }
        for char in chars
        if float(char["x0"]) < -0.01
        or float(char["x1"]) > width + 0.01
        or float(char["top"]) < -0.01
        or float(char["bottom"]) > height + 0.01
    ]
    out_of_bounds_words = [
        {
            "text": str(word.get("text", "")),
            "x0": float(word["x0"]),
            "x1": float(word["x1"]),
            "top": float(word["top"]),
            "bottom": float(word["bottom"]),
        }
        for word in words
        if float(word["x0"]) < -0.01
        or float(word["x1"]) > width + 0.01
        or float(word["top"]) < -0.01
        or float(word["bottom"]) > height + 0.01
    ]
    return {
        "pdfplumber_width_points": width,
        "pdfplumber_height_points": height,
        "char_count": len(chars),
        "word_count": len(words),
        "out_of_bounds_char_count": len(out_of_bounds_chars),
        "out_of_bounds_word_count": len(out_of_bounds_words),
        "out_of_bounds_chars": out_of_bounds_chars,
        "out_of_bounds_words": out_of_bounds_words,
    }


def parse_pdffonts(stdout: str) -> dict:
    lines = [line for line in stdout.splitlines() if line.strip()]
    records = []
    if len(lines) >= 3:
        for line in lines[2:]:
            parts = line.split()
            if len(parts) < 9:
                continue
            records.append(
                {
                    "name": parts[0],
                    "type": " ".join(parts[1:-6]),
                    "encoding": parts[-6],
                    "embedded": parts[-5].lower() == "yes",
                    "subset": parts[-4].lower() == "yes",
                    "unicode": parts[-3].lower() == "yes",
                    "object_id": " ".join(parts[-2:]),
                }
            )
    return {
        "font_count": len(records),
        "all_embedded": bool(records) and all(row["embedded"] for row in records),
        "all_unicode": bool(records) and all(row["unicode"] for row in records),
        "fonts": records,
    }


def make_contact_sheets(document_id: str, page_paths: list[Path]) -> list[dict]:
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
            target_height = round(image.height * THUMBNAIL_WIDTH / image.width)
            image.thumbnail(
                (THUMBNAIL_WIDTH, target_height), Image.Resampling.LANCZOS
            )
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
            draw.rectangle(
                [x, y, x + THUMBNAIL_WIDTH - 1, y + cell_height - 1],
                outline=(150, 150, 150),
                width=1,
            )
            draw.text(
                (x + 5, y + 5),
                f"{document_id} p.{page_number(path)}",
                fill="black",
                font=font,
            )
            sheet.paste(image, (x, y + LABEL_HEIGHT))
        first_page = page_number(group[0])
        last_page = page_number(group[-1])
        output = (
            contacts_dir
            / f"{document_id}_pages_{first_page:03d}_{last_page:03d}.png"
        )
        sheet.save(output)
        records.append(
            {
                "path": str(output.relative_to(ROOT)),
                "sha256": sha256(output),
                "first_page": first_page,
                "last_page": last_page,
                "page_count": len(group),
                "pixel_width": sheet.width,
                "pixel_height": sheet.height,
            }
        )
    return records


def render_pdf(relative: str, reuse_renders: bool) -> dict:
    source = ROOT / relative
    document_id = pdf_id(relative)
    render_dir = TMP / "pages" / document_id
    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / "page"
    page_paths = sorted(render_dir.glob("page-*.png"), key=page_number)
    expected_page_count = len(PdfReader(source).pages)
    can_reuse = (
        reuse_renders
        and len(page_paths) == expected_page_count
        and all(verify_png(path) for path in page_paths)
    )
    if not can_reuse:
        if render_dir.exists():
            shutil.rmtree(render_dir)
        render_dir.mkdir(parents=True)
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
            raise RuntimeError(
                f"pdftoppm failed for {relative}: {completed.stderr}"
            )
        page_paths = sorted(render_dir.glob("page-*.png"), key=page_number)
    invalid_renders = [
        page_number(path) for path in page_paths if not verify_png(path)
    ]
    reader = PdfReader(source)
    pages = []
    extracted_texts = []
    with pdfplumber.open(source) as plumber:
        if len(plumber.pages) != len(reader.pages):
            raise RuntimeError(f"reader page-count disagreement for {relative}")
        for index, (page, plumber_page) in enumerate(
            zip(reader.pages, plumber.pages), start=1
        ):
            text = page.extract_text() or ""
            extracted_texts.append(text)
            media = page.mediabox
            crop = page.cropbox
            raster = raster_metrics(page_paths[index - 1], len(text))
            page_record = {
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
                **pdfplumber_metrics(plumber_page),
                **raster,
            }
            pages.append(page_record)
    font_result = subprocess.run(
        ["pdffonts", str(source)],
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    font_metrics = parse_pdffonts(font_result.stdout)
    tex = tex_for_pdf(relative)
    version = Path(relative).parent.name
    return {
        "pdf_id": document_id,
        "version": version,
        "document_kind": (
            "appendix"
            if source.name.startswith("appendix")
            else "chapter1"
            if "_ch1_" in source.name
            else "chapter2"
        ),
        "path": relative,
        "sha256": sha256(source),
        "size_bytes": source.stat().st_size,
        "page_count_expected_manifest": EXPECTED_PAGES[version][
            PDF_NAMES.index(
                "appendix_phase_separation.pdf"
                if source.name.startswith("appendix")
                else "graphite_ica_ch1_{version}.pdf"
                if "_ch1_" in source.name
                else "graphite_ica_ch2_{version}.pdf"
            )
        ],
        "page_count_pdf": len(reader.pages),
        "page_count_rendered": len(page_paths),
        "invalid_render_pages": invalid_renders,
        "encrypted": bool(reader.is_encrypted),
        "metadata": {
            str(key): str(value) for key, value in (reader.metadata or {}).items()
        },
        "tex_path": str(tex.relative_to(ROOT)) if tex.exists() else None,
        "tex_sha256": sha256(tex) if tex.exists() else None,
        "tex_line_count": (
            len(tex.read_text(encoding="utf-8").splitlines())
            if tex.exists()
            else None
        ),
        "total_extracted_text_chars": sum(len(text) for text in extracted_texts),
        "replacement_char_count": sum(
            text.count("\ufffd") for text in extracted_texts
        ),
        "nul_char_count": sum(text.count("\x00") for text in extracted_texts),
        "blank_candidate_pages": [
            page["page"] for page in pages if page["blank_candidate"]
        ],
        "edge_touch_candidate_pages": [
            page["page"] for page in pages if page["edge_touch_candidate"]
        ],
        "near_edge_candidate_pages": [
            page["page"] for page in pages if page["near_edge_candidate"]
        ],
        "crop_differs_from_media_pages": [
            page["page"] for page in pages if page["crop_differs_from_media"]
        ],
        "out_of_bounds_char_pages": [
            page["page"] for page in pages if page["out_of_bounds_char_count"]
        ],
        "out_of_bounds_word_pages": [
            page["page"] for page in pages if page["out_of_bounds_word_count"]
        ],
        "pdffonts_returncode": font_result.returncode,
        "pdffonts_stderr": font_result.stderr,
        "font_metrics": font_metrics,
        "contact_sheets": make_contact_sheets(document_id, page_paths),
        "pages": pages,
    }


def main() -> None:
    reuse_renders = "--reuse" in sys.argv
    if TMP.exists() and not reuse_renders:
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    source_before = {relative: sha256(ROOT / relative) for relative in PDFS}
    documents = [render_pdf(relative, reuse_renders) for relative in PDFS]
    source_after = {relative: sha256(ROOT / relative) for relative in PDFS}
    summary = {
        "page_count_matches_all": all(
            document["page_count_pdf"]
            == document["page_count_rendered"]
            == document["page_count_expected_manifest"]
            for document in documents
        ),
        "invalid_render_count": sum(
            len(document["invalid_render_pages"]) for document in documents
        ),
        "blank_candidate_count": sum(
            len(document["blank_candidate_pages"]) for document in documents
        ),
        "replacement_char_count": sum(
            document["replacement_char_count"] for document in documents
        ),
        "nul_char_count": sum(
            document["nul_char_count"] for document in documents
        ),
        "crop_differs_from_media_count": sum(
            len(document["crop_differs_from_media_pages"])
            for document in documents
        ),
        "edge_touch_candidate_count": sum(
            len(document["edge_touch_candidate_pages"])
            for document in documents
        ),
        "near_edge_candidate_count": sum(
            len(document["near_edge_candidate_pages"])
            for document in documents
        ),
        "out_of_bounds_char_page_count": sum(
            len(document["out_of_bounds_char_pages"])
            for document in documents
        ),
        "out_of_bounds_word_page_count": sum(
            len(document["out_of_bounds_word_pages"])
            for document in documents
        ),
        "all_pdffonts_commands_succeeded": all(
            document["pdffonts_returncode"] == 0 for document in documents
        ),
        "all_fonts_embedded": all(
            document["font_metrics"]["all_embedded"] for document in documents
        ),
        "all_fonts_have_unicode_maps": all(
            document["font_metrics"]["all_unicode"] for document in documents
        ),
    }
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "render_dpi": RENDER_DPI,
        "pdf_count": len(documents),
        "total_pdf_pages": sum(
            document["page_count_pdf"] for document in documents
        ),
        "total_rendered_pages": sum(
            document["page_count_rendered"] for document in documents
        ),
        "total_contact_sheets": sum(
            len(document["contact_sheets"]) for document in documents
        ),
        "source_hashes_before": source_before,
        "source_hashes_after": source_after,
        "sources_unchanged": source_before == source_after,
        "documents": documents,
        "summary": summary,
        "status": "PENDING_P059_PDF_VISUAL_INSPECTION",
        "next_action": "Inspect every contact sheet and every mechanical candidate at full rendered resolution; then write visual dispositions.",
    }
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
