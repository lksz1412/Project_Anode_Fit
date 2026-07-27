"""Validate Phase 057 queue completeness and chunk continuity."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
REPO_ROOT = Path(__file__).resolve().parents[3]
QUEUE_PATH = REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json"
COVERAGE_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_COVERAGE.json"
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    queue = read_json(QUEUE_PATH)
    coverage = read_json(COVERAGE_PATH)
    documents = queue["documents"]
    coverage_documents = coverage["documents"]

    assert queue["document_count"] == 271
    assert queue["total_lines"] == 57_795
    assert queue["chunk_count"] == 341
    assert queue["validation"]["missing_introduction_count"] == 0
    assert len(documents) == queue["document_count"]
    assert len(coverage_documents) == coverage["document_count"]
    assert sum(item["line_count"] for item in documents) == queue["total_lines"]
    assert sum(len(item["chunks"]) for item in documents) == queue["chunk_count"]
    assert len({item["blob_sha"] for item in documents}) == len(documents)
    assert len(
        {item["representative_path"] for item in documents}
    ) == len(documents)

    coverage_by_blob = {
        item["blob_sha"]: item for item in coverage_documents
    }
    assert len(coverage_by_blob) == len(coverage_documents)

    for document in documents:
        chunks = document["chunks"]
        assert chunks
        assert chunks[0]["start_line"] == 1
        assert chunks[-1]["end_line"] == document["line_count"]
        for previous, current in zip(chunks, chunks[1:], strict=False):
            assert current["start_line"] == previous["end_line"] + 1
        assert all(chunk["status"] == "UNREAD" for chunk in chunks)
        assert document["status"] == "UNREAD"
        assert document["introduction"]["commit"]

        tracked = coverage_by_blob[document["blob_sha"]]
        assert tracked["representative_path"] == document["representative_path"]
        assert tracked["line_count"] == document["line_count"]
        assert tracked["status"] == "UNREAD"
        assert tracked["coverage"] == []

        subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                document["introduction"]["commit"],
                BASELINE,
            ],
            cwd=REPO_ROOT,
            check=True,
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "documents": len(documents),
                "lines": queue["total_lines"],
                "chunks": queue["chunk_count"],
                "all_introduction_commits_are_baseline_ancestors": True,
                "all_chunks_are_contiguous": True,
                "all_statuses_are_unread": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
