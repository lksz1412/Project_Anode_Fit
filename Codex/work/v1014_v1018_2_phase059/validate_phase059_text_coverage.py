#!/usr/bin/env python3
"""Read-only validator for the completed Phase 059 text coverage gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
QUEUE = ROOT / "Codex" / "results" / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
COVERAGE = (
    ROOT / "Codex" / "results" / "PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json"
)
REVIEW = ROOT / "Codex" / "results" / "PHASE_059_TEXT_SOURCE_REVIEW.md"


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    records = {
        record["blob_sha"]: record
        for record in queue["records"]
        if record["review_mode"] == "FULL_TEXT"
    }
    checks: list[tuple[str, bool]] = []

    checks.append(("review artifact exists", REVIEW.is_file()))
    checks.append(("document count frozen", len(coverage["documents"]) == 63))
    checks.append(("coverage count field", coverage["document_count"] == 63))
    checks.append(("line count field", coverage["total_lines"] == 36641))
    checks.append(("completed line count", coverage["completed_lines"] == 36641))
    checks.append(("completed chunk count", coverage["completed_chunks"] == 158))
    checks.append(
        ("status count complete", coverage["status_counts"] == {"COMPLETE": 63})
    )
    checks.append(
        ("gate exact", coverage["gate"] == "PASS_P059_TEXT_COVERAGE")
    )
    checks.append(
        (
            "queue/coverage blob set",
            set(records)
            == {document["blob_sha"] for document in coverage["documents"]},
        )
    )

    covered_lines = 0
    covered_chunks = 0
    all_paths = True
    all_hashes = True
    all_ranges = True
    all_evidence = True
    for document in coverage["documents"]:
        record = records[document["blob_sha"]]
        path = record["representative_path"]
        payload = (ROOT / path).read_bytes()
        all_paths &= document["representative_path"] == path
        all_hashes &= git_blob_sha(payload) == document["blob_sha"]
        all_evidence &= (
            "Codex/results/PHASE_059_TEXT_SOURCE_REVIEW.md"
            in document["review_evidence"]
        )

        expected = 1
        for chunk in document["coverage"]:
            start = chunk["line_start"]
            end = chunk["line_end"]
            all_ranges &= start == expected and end >= start
            covered_lines += end - start + 1
            covered_chunks += 1
            expected = end + 1
        all_ranges &= expected == document["line_count"] + 1
        all_ranges &= document["status"] == "COMPLETE"

    checks.append(("representative paths exact", all_paths))
    checks.append(("all blob hashes exact", all_hashes))
    checks.append(("all chunk ranges contiguous", all_ranges))
    checks.append(("all documents cite source review", all_evidence))
    checks.append(("coverage line sum", covered_lines == 36641))
    checks.append(("coverage chunk sum", covered_chunks == 158))

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 TEXT COVERAGE FAIL: {failed}")
    print(
        "PASS_P059_TEXT_COVERAGE "
        f"checks={len(checks)}/{len(checks)} documents=63 lines=36641 chunks=158"
    )


if __name__ == "__main__":
    main()
