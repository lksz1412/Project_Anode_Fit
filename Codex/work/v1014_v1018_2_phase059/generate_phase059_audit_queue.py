"""Generate the content-addressed Phase 059 audit queue and coverage."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = (
    REPO_ROOT / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
)
QUEUE_PATH = (
    REPO_ROOT / "Codex/results/PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
)
COVERAGE_PATH = (
    REPO_ROOT / "Codex/results/PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json"
)
VERSIONS = (
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
)
VERSION_SET = set(VERSIONS)
TEXT_CHUNK_SIZE = 300
EXPECTED_ROLE_COUNTS = {
    "code": 4,
    "data": 2,
    "demo": 18,
    "figure": 10,
    "generated_document": 18,
    "implementation_guide": 3,
    "result": 8,
    "supporting_document": 1,
    "test": 12,
    "theory": 17,
}


def text_chunks(line_count: int) -> list[dict[str, int]]:
    return [
        {
            "start_line": start,
            "end_line": min(start + TEXT_CHUNK_SIZE - 1, line_count),
        }
        for start in range(1, line_count + 1, TEXT_CHUNK_SIZE)
    ]


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    selected = [
        entry
        for entry in manifest["entries"]
        if entry["version"] in VERSION_SET
    ]
    by_blob: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in selected:
        by_blob[entry["blob_sha"]].append(entry)

    records: list[dict[str, Any]] = []
    coverage_records: list[dict[str, Any]] = []
    for blob_sha, entries in sorted(
        by_blob.items(), key=lambda item: min(e["path"] for e in item[1])
    ):
        representative = min(entries, key=lambda entry: entry["path"])
        extent = representative["extent"]
        chunks = (
            text_chunks(extent["lines"])
            if representative["review_mode"] == "FULL_TEXT"
            else []
        )
        record = {
            "blob_sha": blob_sha,
            "representative_path": representative["path"],
            "occurrence_paths": sorted(entry["path"] for entry in entries),
            "versions": [
                version
                for version in VERSIONS
                if any(entry["version"] == version for entry in entries)
            ],
            "role": representative["role"],
            "review_mode": representative["review_mode"],
            "size_bytes": representative["size_bytes"],
            "extent": extent,
            "chunks": chunks,
        }
        records.append(record)
        if representative["review_mode"] == "FULL_TEXT":
            coverage_records.append(
                {
                    "blob_sha": blob_sha,
                    "representative_path": representative["path"],
                    "line_count": extent["lines"],
                    "status": "UNREAD",
                    "coverage": [],
                    "review_evidence": [],
                    "notes": [],
                }
            )

    role_counts = dict(
        sorted(Counter(record["role"] for record in records).items())
    )
    version_path_counts = {
        version: sum(entry["version"] == version for entry in selected)
        for version in VERSIONS
    }
    queue = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": manifest["baseline_commit"],
        "source_manifest": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
        "versions": list(VERSIONS),
        "absent_intermediate_versions": ["v1.0.18"],
        "path_count": len(selected),
        "unique_blob_count": len(records),
        "duplicate_path_occurrence_count": len(selected) - len(records),
        "text_blob_count": len(coverage_records),
        "text_line_count": sum(
            record["line_count"] for record in coverage_records
        ),
        "text_chunk_count": sum(len(record["chunks"]) for record in records),
        "version_path_counts": version_path_counts,
        "unique_role_counts": role_counts,
        "records": records,
        "validation": {
            "paths_match_frozen_scope": len(selected) == 117,
            "blobs_match_frozen_scope": len(records) == 93,
            "duplicates_match_frozen_scope": len(selected) - len(records) == 24,
            "text_blobs_match_frozen_scope": len(coverage_records) == 63,
            "text_lines_match_frozen_scope": sum(
                record["line_count"] for record in coverage_records
            )
            == 36641,
            "roles_match_frozen_scope": role_counts == EXPECTED_ROLE_COUNTS,
            "versions_match_frozen_scope": version_path_counts
            == {
                "v1.0.14": 19,
                "v1.0.15": 19,
                "v1.0.16": 20,
                "v1.0.17": 19,
                "v1.0.18.1": 19,
                "v1.0.18.2": 21,
            },
            "all_occurrence_paths_accounted": sum(
                len(record["occurrence_paths"]) for record in records
            )
            == 117,
            "no_unlisted_v1018_directory_in_scope": not any(
                entry["version"] == "v1.0.18"
                for entry in manifest["entries"]
            ),
        },
    }
    coverage = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": manifest["baseline_commit"],
        "source_queue": str(QUEUE_PATH.relative_to(REPO_ROOT)),
        "document_count": len(coverage_records),
        "total_lines": queue["text_line_count"],
        "status_counts": {"UNREAD": len(coverage_records)},
        "completed_lines": 0,
        "documents": coverage_records,
    }
    queue_encoded = json.dumps(queue, ensure_ascii=False, indent=2) + "\n"
    coverage_encoded = json.dumps(coverage, ensure_ascii=False, indent=2) + "\n"
    QUEUE_PATH.write_text(queue_encoded, encoding="utf-8")
    COVERAGE_PATH.write_text(coverage_encoded, encoding="utf-8")
    output = {
        "status": (
            "PASS_P059_AUDIT_QUEUE"
            if all(queue["validation"].values())
            else "FAIL_P059_AUDIT_QUEUE"
        ),
        "paths": queue["path_count"],
        "blobs": queue["unique_blob_count"],
        "duplicate_occurrences": queue["duplicate_path_occurrence_count"],
        "text_blobs": queue["text_blob_count"],
        "text_lines": queue["text_line_count"],
        "text_chunks": queue["text_chunk_count"],
        "queue_sha256": hashlib.sha256(queue_encoded.encode()).hexdigest(),
        "coverage_sha256": hashlib.sha256(
            coverage_encoded.encode()
        ).hexdigest(),
        "failures": [
            name
            for name, passed in queue["validation"].items()
            if not passed
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if output["failures"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
