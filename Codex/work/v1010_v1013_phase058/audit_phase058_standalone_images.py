#!/usr/bin/env python3
"""Inventory the eight standalone images in the Phase 058 frozen scope."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Codex" / "results" / "PHASE_058_STANDALONE_IMAGE_AUDIT.json"
IMAGES = [
    {
        "path": "Claude/docs/v1.0.10/figs/Anode_Fit_v1.0.10_sample_test.png",
        "generator": "Claude/docs/v1.0.10/sample_test_v1010.py",
    },
    {
        "path": "Claude/docs/v1.0.10/figs/P4_lco_heat_validation.png",
        "generator": "Claude/docs/v1.0.10/demo_lco_heat.py",
    },
    {
        "path": "Claude/docs/v1.0.10/figs/P5_graph_suite.png",
        "generator": "Claude/docs/v1.0.10/graph_suite_p5.py",
    },
    {
        "path": "Claude/docs/v1.0.10/figs/anode_fit_v1_0_10_dqdv.png",
        "generator": "Claude/docs/v1.0.10/plot_dqdv.py",
    },
    {
        "path": "Claude/docs/v1.0.12/sample_test_v1012.png",
        "generator": "Claude/docs/v1.0.12/sample_test_v1012.py",
    },
    {
        "path": "Claude/docs/v1.0.13/figs/P4_lco_heat_validation.png",
        "generator": "Claude/docs/v1.0.13/demo_lco_heat.py",
    },
    {
        "path": "Claude/docs/v1.0.13/figs/graph_suite_v1013.png",
        "generator": "Claude/docs/v1.0.13/graph_suite_v1013.py",
    },
    {
        "path": "Claude/docs/v1.0.13/sample_test_v1013.png",
        "generator": "Claude/docs/v1.0.13/sample_test_v1013.py",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_metrics(item: dict[str, str]) -> dict:
    source = ROOT / item["path"]
    generator = ROOT / item["generator"]
    with Image.open(source) as opened:
        image = opened.convert("RGB")
        metadata = dict(opened.info)
        width, height = opened.size
        source_mode = opened.mode

    pixels = np.asarray(image, dtype=np.uint8)
    grayscale = np.asarray(image.convert("L"), dtype=np.uint8)
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
            "right_px": int(width - 1 - bbox[2]),
            "bottom_px": int(height - 1 - bbox[3]),
        }
    else:
        bbox = None
        margins = None

    edge_dark = np.concatenate(
        [
            dark[:3, :].ravel(),
            dark[-3:, :].ravel(),
            dark[:, :3].ravel(),
            dark[:, -3:].ravel(),
        ]
    )
    return {
        **item,
        "source_exists": source.is_file(),
        "generator_exists": generator.is_file(),
        "sha256": sha256(source),
        "generator_sha256": sha256(generator) if generator.is_file() else None,
        "byte_size": source.stat().st_size,
        "format": "PNG",
        "mode": source_mode,
        "width_px": width,
        "height_px": height,
        "aspect_ratio": width / height,
        "dpi": list(metadata["dpi"]) if "dpi" in metadata else None,
        "mean_rgb": [float(value) for value in pixels.mean(axis=(0, 1))],
        "nonwhite_fraction_lt245": float(nonwhite.mean()),
        "dark_fraction_lt180": float(dark.mean()),
        "content_bbox_lt245": bbox,
        "content_margins_px": margins,
        "edge_dark_fraction_3px": float(edge_dark.mean()),
        "edge_touch_candidate": bool(edge_dark.any()),
    }


def pairwise(records: list[dict]) -> list[dict]:
    comparisons = []
    for left, right in itertools.combinations(records, 2):
        left_path = ROOT / left["path"]
        right_path = ROOT / right["path"]
        same_dimensions = (
            left["width_px"] == right["width_px"]
            and left["height_px"] == right["height_px"]
        )
        record = {
            "left": left["path"],
            "right": right["path"],
            "byte_identical": left["sha256"] == right["sha256"],
            "same_dimensions": same_dimensions,
            "pixel_identical": False,
            "rgb_rmse": None,
        }
        if same_dimensions:
            with Image.open(left_path) as image:
                left_pixels = np.asarray(image.convert("RGB"), dtype=np.float64)
            with Image.open(right_path) as image:
                right_pixels = np.asarray(image.convert("RGB"), dtype=np.float64)
            delta = left_pixels - right_pixels
            record["pixel_identical"] = bool(np.array_equal(left_pixels, right_pixels))
            record["rgb_rmse"] = float(np.sqrt(np.mean(delta * delta)))
        comparisons.append(record)
    return comparisons


def main() -> int:
    records = [image_metrics(item) for item in IMAGES]
    result = {
        "schema_version": "phase058-standalone-image-audit-v1",
        "scope": {
            "versions": ["v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13"],
            "image_paths": len(IMAGES),
            "unique_image_blobs": len({record["sha256"] for record in records}),
            "visual_inspection": "MANUAL_REVIEW_RECORDED_SEPARATELY",
        },
        "images": records,
        "pairwise_comparisons": pairwise(records),
        "machine_checks": {
            "all_images_exist": all(record["source_exists"] for record in records),
            "all_generators_exist": all(record["generator_exists"] for record in records),
            "all_png_rgb_or_rgba": all(
                record["format"] == "PNG" and record["mode"] in {"RGB", "RGBA"}
                for record in records
            ),
            "all_nonblank": all(
                record["nonwhite_fraction_lt245"] > 0.001 for record in records
            ),
            "all_positive_dimensions": all(
                record["width_px"] > 0 and record["height_px"] > 0
                for record in records
            ),
        },
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUT.relative_to(ROOT)),
                "images": len(records),
                "unique_blobs": result["scope"]["unique_image_blobs"],
                "checks": result["machine_checks"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
