#!/usr/bin/env python3
"""Create a byte-level adjacent-version diff index for v1.0.10--v1.0.25.2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
DOCS = REPO / "Claude/docs"
OUTPUT = REPO / "Codex/results/PHASE_044_LINEAGE_DIFF.json"

VERSIONS = [
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
]

TEXT_SUFFIXES = {".csv", ".html", ".json", ".md", ".py", ".tex", ".txt"}
EXCLUDED_PATHS = {
    "Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html",
}
EXCLUDED_RELATIVE_PATHS: set[str] = set()


def file_map(version: str) -> dict[str, dict]:
    base = DOCS / version
    result: dict[str, dict] = {}
    for path in sorted(base.rglob("*")):
        relative_repo = path.relative_to(REPO).as_posix()
        relative_version = path.relative_to(base).as_posix()
        if (
            not path.is_file()
            or path.suffix.lower() not in TEXT_SUFFIXES
            or "__pycache__" in path.parts
            or relative_repo in EXCLUDED_PATHS
            or relative_version in EXCLUDED_RELATIVE_PATHS
        ):
            continue
        data = path.read_bytes()
        result[relative_version] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "lines": data.count(b"\n") + (0 if not data or data.endswith(b"\n") else 1),
        }
    return result


def main() -> None:
    maps = {version: file_map(version) for version in VERSIONS}
    versions = []
    previous_version = None
    for version in VERSIONS:
        current = maps[version]
        item: dict[str, object] = {
            "version": version,
            "text_file_count": len(current),
        }
        if previous_version is not None:
            previous = maps[previous_version]
            current_paths = set(current)
            previous_paths = set(previous)
            common = current_paths & previous_paths
            added = sorted(current_paths - previous_paths)
            removed = sorted(previous_paths - current_paths)
            changed = sorted(
                path
                for path in common
                if current[path]["sha256"] != previous[path]["sha256"]
            )
            item["compared_to"] = previous_version
            item["adjacent_diff"] = {
                "added_count": len(added),
                "removed_count": len(removed),
                "changed_count": len(changed),
                "unchanged_count": len(common) - len(changed),
                "added": added,
                "removed": removed,
                "changed": changed,
            }
        versions.append(item)
        previous_version = version

    payload = {
        "schema": "phase044-lineage-adjacent-byte-diff-v1",
        "notice": (
            "Byte-level index only. A changed file is not automatically a "
            "scientific change, and an unchanged file is not automatically valid."
        ),
        "excluded_scientific_versions": ["v1.0.26A-regsol", "v1.0.26B-gallery"],
        "excluded_working_tree_paths": sorted(EXCLUDED_PATHS),
        "excluded_relative_paths_for_adjacent_comparison": sorted(
            EXCLUDED_RELATIVE_PATHS
        ),
        "versions": versions,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
