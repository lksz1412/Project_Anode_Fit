"""Build the deterministic v1.0.10-v1.0.25.2 audit manifest.

This script is workflow infrastructure, not battery-model code.  It reads the
frozen Git tree, records every path and unique blob, and initializes the
read-coverage queue without claiming that any source has already been read.
"""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from pypdf import PdfReader


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
VERSIONS = (
    "v1.0.10",
    "v1.0.11",
    "v1.0.12",
    "v1.0.13",
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
    "v1.0.19",
    "v1.0.20",
    "v1.0.21",
    "v1.0.22",
    "v1.0.23",
    "v1.0.24",
    "v1.0.24.1",
    "v1.0.25",
    "v1.0.25.1",
    "v1.0.25.2",
)
TEXT_EXTENSIONS = {".html", ".json", ".md", ".py", ".tex", ".txt"}
EXPECTED_PATHS = 1520
EXPECTED_UNIQUE_BLOBS = 862

REPO_ROOT = Path(__file__).resolve().parents[3]
RESULTS_ROOT = REPO_ROOT / "Codex" / "results"
MANIFEST_PATH = RESULTS_ROOT / "PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
COVERAGE_PATH = RESULTS_ROOT / "PHASE_056_V1010_V1025_2_READ_COVERAGE.json"


def run_git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def tree_records() -> list[dict[str, str]]:
    roots = [f"Claude/docs/{version}" for version in VERSIONS]
    raw = run_git("ls-tree", "-r", "-z", BASELINE, *roots)
    records: list[dict[str, str]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, raw_path = item.split(b"\t", 1)
        mode, object_type, blob_sha = metadata.decode("ascii").split()
        records.append(
            {
                "mode": mode,
                "object_type": object_type,
                "blob_sha": blob_sha,
                "path": raw_path.decode("utf-8"),
            }
        )
    return sorted(records, key=lambda item: item["path"])


def blob_bytes(blob_sha: str) -> bytes:
    return run_git("cat-file", "blob", blob_sha)


def version_from_path(path: str) -> str:
    version = Path(path).parts[2]
    if version not in VERSIONS:
        raise ValueError(f"path outside version scope: {path}")
    return version


def review_mode(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return "FULL_TEXT"
    if suffix == ".pdf":
        return "FULL_PDF"
    if suffix == ".png":
        return "FULL_IMAGE"
    if suffix == ".npz":
        return "BINARY_INTROSPECTION"
    if suffix == ".pyc":
        return "GENERATED_ONLY"
    return "BINARY_INTROSPECTION"


def role(path: str) -> str:
    lowered = path.lower()
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()
    parts = {part.lower() for part in Path(path).parts}

    if suffix == ".npz":
        return "data"
    if suffix == ".pyc":
        return "generated"
    if suffix == ".png" or "/figs/" in lowered or "/samples/" in lowered:
        return "figure"
    if suffix == ".pdf":
        return "generated_document"
    if "plans" in parts or name.startswith("plan_") or "master-plan" in name:
        return "plan"
    if (
        "results" in parts
        or "handover" in name
        or "closing" in name
        or "change_log" in name
        or "ledger" in name
        or "report" in name
        or "judgment" in name
        or "review" in name
        or "audit" in name
    ):
        return "result"
    if suffix == ".py":
        if (
            name.startswith("test")
            or "test_" in name
            or "sample_test" in name
            or "verify" in name
        ):
            return "test"
        if "demo" in name or "suite" in name or "plot" in name:
            return "demo"
        return "code"
    if suffix == ".tex":
        if "draft" in lowered or "harness" in lowered or "comp_" in lowered:
            return "draft"
        return "theory"
    if name == "fitting_guide.md" or name == "code_guide_v24.html":
        return "implementation_guide"
    if suffix in TEXT_EXTENSIONS:
        return "supporting_document"
    return "artifact"


def text_extent(data: bytes) -> dict[str, Any]:
    line_count = data.count(b"\n")
    if data and not data.endswith(b"\n"):
        line_count += 1
    decode_status = "utf-8"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        decode_status = "non-utf8"
    return {"lines": line_count, "encoding_check": decode_status}


def pdf_extent(data: bytes) -> dict[str, Any]:
    reader = PdfReader(io.BytesIO(data), strict=False)
    return {
        "pages": len(reader.pages),
        "encrypted": bool(reader.is_encrypted),
    }


def image_extent(data: bytes) -> dict[str, Any]:
    with Image.open(io.BytesIO(data)) as image:
        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "format": image.format,
            "frames": int(getattr(image, "n_frames", 1)),
        }


def npz_extent(data: bytes) -> dict[str, Any]:
    arrays: list[dict[str, Any]] = []
    with np.load(io.BytesIO(data), allow_pickle=False) as archive:
        for key in sorted(archive.files):
            array = archive[key]
            item: dict[str, Any] = {
                "key": key,
                "dtype": str(array.dtype),
                "shape": list(array.shape),
                "size": int(array.size),
            }
            if np.issubdtype(array.dtype, np.number) and array.size:
                finite = np.isfinite(array)
                item["finite_count"] = int(finite.sum())
                if finite.any():
                    finite_values = array[finite]
                    item["finite_min"] = float(np.min(finite_values))
                    item["finite_max"] = float(np.max(finite_values))
            arrays.append(item)
    return {"arrays": arrays}


def inspect_blob(path: str, blob_sha: str, data: bytes) -> dict[str, Any]:
    mode = review_mode(path)
    suffix = Path(path).suffix.lower()
    extent: dict[str, Any]
    inspection_error: str | None = None
    try:
        if mode == "FULL_TEXT":
            extent = text_extent(data)
        elif mode == "FULL_PDF":
            extent = pdf_extent(data)
        elif mode == "FULL_IMAGE":
            extent = image_extent(data)
        elif suffix == ".npz":
            extent = npz_extent(data)
        else:
            extent = {"bytes": len(data)}
    except Exception as exc:  # recorded as a manifest gate failure
        extent = {"bytes": len(data)}
        inspection_error = f"{type(exc).__name__}: {exc}"

    return {
        "blob_sha": blob_sha,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "review_mode": mode,
        "extent": extent,
        "inspection_error": inspection_error,
    }


def candidate_tex_paths(pdf_path: str, all_paths: set[str]) -> list[str]:
    direct = str(Path(pdf_path).with_suffix(".tex"))
    candidates = [direct] if direct in all_paths else []
    return candidates


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts = Counter(str(item[key]) for item in items)
    return dict(sorted(counts.items()))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    records = tree_records()
    paths = {record["path"] for record in records}
    grouped_paths: dict[str, list[str]] = defaultdict(list)
    for record in records:
        grouped_paths[record["blob_sha"]].append(record["path"])

    blob_metadata: dict[str, dict[str, Any]] = {}
    for blob_sha, blob_paths in sorted(grouped_paths.items()):
        representative = sorted(blob_paths)[0]
        data = blob_bytes(blob_sha)
        blob_metadata[blob_sha] = inspect_blob(
            representative,
            blob_sha,
            data,
        )

    manifest_entries: list[dict[str, Any]] = []
    for record in records:
        path = record["path"]
        metadata = blob_metadata[record["blob_sha"]]
        entry = {
            "path": path,
            "version": version_from_path(path),
            "blob_sha": record["blob_sha"],
            "dedup_group": f"blob:{record['blob_sha']}",
            "git_mode": record["mode"],
            "size_bytes": metadata["size_bytes"],
            "extension": Path(path).suffix.lower().lstrip(".") or "(none)",
            "role": role(path),
            "review_mode": metadata["review_mode"],
            "extent": metadata["extent"],
        }
        if Path(path).suffix.lower() == ".pdf":
            entry["candidate_tex_paths"] = candidate_tex_paths(path, paths)
        manifest_entries.append(entry)

    coverage_groups: list[dict[str, Any]] = []
    for blob_sha, blob_paths in sorted(grouped_paths.items()):
        metadata = blob_metadata[blob_sha]
        coverage_groups.append(
            {
                "blob_sha": blob_sha,
                "sha256": metadata["sha256"],
                "dedup_group": f"blob:{blob_sha}",
                "representative_path": sorted(blob_paths)[0],
                "paths": sorted(blob_paths),
                "review_mode": metadata["review_mode"],
                "extent": metadata["extent"],
                "inspection_error": metadata["inspection_error"],
                "status": "UNREAD",
                "coverage": [],
                "review_evidence": [],
                "notes": [],
            }
        )

    errors = [
        {
            "blob_sha": group["blob_sha"],
            "representative_path": group["representative_path"],
            "inspection_error": group["inspection_error"],
        }
        for group in coverage_groups
        if group["inspection_error"]
    ]

    manifest = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "version_scope": list(VERSIONS),
        "path_count": len(manifest_entries),
        "unique_blob_count": len(coverage_groups),
        "counts": {
            "by_version": count_by(manifest_entries, "version"),
            "by_extension": count_by(manifest_entries, "extension"),
            "by_role": count_by(manifest_entries, "role"),
            "by_review_mode": count_by(manifest_entries, "review_mode"),
        },
        "validation": {
            "expected_path_count": EXPECTED_PATHS,
            "expected_unique_blob_count": EXPECTED_UNIQUE_BLOBS,
            "path_count_matches": len(manifest_entries) == EXPECTED_PATHS,
            "unique_blob_count_matches": len(coverage_groups)
            == EXPECTED_UNIQUE_BLOBS,
            "duplicate_path_count": len(manifest_entries) - len(paths),
            "duplicate_content_occurrence_count": len(manifest_entries)
            - len(coverage_groups),
            "duplicate_blob_group_count": sum(
                1 for blob_paths in grouped_paths.values() if len(blob_paths) > 1
            ),
            "inspection_error_count": len(errors),
            "inspection_errors": errors,
        },
        "entries": manifest_entries,
    }
    coverage = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "policy": {
            "byte_identical_blob_read_once": True,
            "different_blobs_must_be_reviewed_separately": True,
            "full_text_requires_contiguous_1_to_eof_coverage": True,
            "full_pdf_requires_contiguous_1_to_last_page_coverage": True,
            "images_require_visual_review": True,
            "binary_artifacts_require_non_destructive_introspection": True,
        },
        "group_count": len(coverage_groups),
        "status_counts": {"UNREAD": len(coverage_groups)},
        "groups": coverage_groups,
    }

    write_json(MANIFEST_PATH, manifest)
    write_json(COVERAGE_PATH, coverage)

    print(
        json.dumps(
            {
                "manifest": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
                "coverage": str(COVERAGE_PATH.relative_to(REPO_ROOT)),
                "path_count": len(manifest_entries),
                "unique_blob_count": len(coverage_groups),
                "inspection_error_count": len(errors),
                "path_count_matches": len(manifest_entries) == EXPECTED_PATHS,
                "unique_blob_count_matches": len(coverage_groups)
                == EXPECTED_UNIQUE_BLOBS,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
