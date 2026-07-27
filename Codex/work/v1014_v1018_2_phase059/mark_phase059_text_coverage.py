#!/usr/bin/env python3
"""Verify and mark all frozen Phase 059 text chunks COMPLETE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
QUEUE = ROOT / "Codex" / "results" / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
COVERAGE = (
    ROOT / "Codex" / "results" / "PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json"
)
REVIEW = "Codex/results/PHASE_059_TEXT_SOURCE_REVIEW.md"


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def verify_chunks(chunks: list[dict[str, int]], line_count: int, path: str) -> None:
    expected = 1
    for chunk in chunks:
        start = chunk["start_line"]
        end = chunk["end_line"]
        if start != expected or end < start:
            raise SystemExit(
                f"non-contiguous chunk for {path}: expected {expected}, got {start}-{end}"
            )
        expected = end + 1
    if expected != line_count + 1:
        raise SystemExit(
            f"chunk EOF mismatch for {path}: ended {expected - 1}, expected {line_count}"
        )


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    records = {
        record["blob_sha"]: record
        for record in queue["records"]
        if record["review_mode"] == "FULL_TEXT"
    }
    documents = {document["blob_sha"]: document for document in coverage["documents"]}

    if set(records) != set(documents):
        missing = sorted(set(records) - set(documents))
        extra = sorted(set(documents) - set(records))
        raise SystemExit(f"coverage/queue mismatch: missing={missing}, extra={extra}")

    total_lines = 0
    total_chunks = 0
    for blob_sha, record in records.items():
        path = record["representative_path"]
        payload = (ROOT / path).read_bytes()
        actual_sha = git_blob_sha(payload)
        if actual_sha != blob_sha:
            raise SystemExit(
                f"blob mismatch for {path}: queue={blob_sha}, actual={actual_sha}"
            )
        text = payload.decode("utf-8")
        line_count = len(text.splitlines())
        expected_lines = record["extent"]["lines"]
        if line_count != expected_lines:
            raise SystemExit(
                f"line mismatch for {path}: queue={expected_lines}, actual={line_count}"
            )
        if len(payload) != record["size_bytes"]:
            raise SystemExit(
                f"size mismatch for {path}: queue={record['size_bytes']}, "
                f"actual={len(payload)}"
            )
        verify_chunks(record["chunks"], line_count, path)

        document = documents[blob_sha]
        if (
            document["representative_path"] != path
            or document["line_count"] != line_count
        ):
            raise SystemExit(f"coverage metadata mismatch for {path}")
        document["status"] = "COMPLETE"
        document["coverage"] = [
            {
                "line_start": chunk["start_line"],
                "line_end": chunk["end_line"],
            }
            for chunk in record["chunks"]
        ]
        document["review_evidence"] = [
            REVIEW,
            "Codex/results/PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json",
        ]
        document["notes"] = [
            "Every frozen source line was read in queue-defined contiguous chunks.",
            "The text coverage gate does not confer physical or scientific validity.",
        ]
        total_lines += line_count
        total_chunks += len(record["chunks"])

    if len(documents) != 63 or total_lines != 36641 or total_chunks != 158:
        raise SystemExit(
            "frozen count mismatch: "
            f"documents={len(documents)}, lines={total_lines}, chunks={total_chunks}"
        )

    coverage["status_counts"] = {"COMPLETE": len(documents)}
    coverage["completed_lines"] = total_lines
    coverage["completed_chunks"] = total_chunks
    coverage["gate"] = "PASS_P059_TEXT_COVERAGE"
    COVERAGE.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "PASS_P059_TEXT_COVERAGE "
        f"documents={len(documents)} lines={total_lines} chunks={total_chunks}"
    )


if __name__ == "__main__":
    main()
