"""Validate Phase 057 queue completeness and read-coverage closure."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "hash-object", path],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


def physical_line_count(path: str) -> int:
    data = (REPO_ROOT / path).read_bytes()
    count = data.count(b"\n")
    if data and not data.endswith(b"\n"):
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--coverage-state",
        choices=("initial", "complete"),
        default="complete",
    )
    arguments = parser.parse_args()

    queue = read_json(QUEUE_PATH)
    coverage = read_json(COVERAGE_PATH)
    documents = queue["documents"]
    coverage_documents = coverage["documents"]

    assert queue["baseline_commit"] == BASELINE
    assert coverage["baseline_commit"] == BASELINE
    assert coverage["source_queue"] == str(QUEUE_PATH.relative_to(REPO_ROOT))
    assert queue["document_count"] == 271
    assert queue["total_lines"] == 57_795
    assert queue["chunk_count"] == 341
    assert coverage["document_count"] == queue["document_count"]
    assert coverage["total_lines"] == queue["total_lines"]
    assert coverage["chunk_count"] == queue["chunk_count"]
    assert queue["validation"]["missing_introduction_count"] == 0
    assert len(documents) == queue["document_count"]
    assert len(coverage_documents) == coverage["document_count"]
    assert sum(item["line_count"] for item in documents) == queue["total_lines"]
    assert sum(len(item["chunks"]) for item in documents) == queue["chunk_count"]
    assert len({item["blob_sha"] for item in documents}) == len(documents)
    assert len(
        {item["representative_path"] for item in documents}
    ) == len(documents)

    coverage_by_blob = {item["blob_sha"]: item for item in coverage_documents}
    assert len(coverage_by_blob) == len(coverage_documents)
    assert len(
        {item["representative_path"] for item in coverage_documents}
    ) == len(coverage_documents)

    all_claim_ids: set[str] = set()
    checked_paths: set[str] = set()

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

        for path in document["all_paths"]:
            if path in checked_paths:
                continue
            checked_paths.add(path)
            source = REPO_ROOT / path
            assert source.is_file(), path
            data = source.read_bytes()
            assert hashlib.sha256(data).hexdigest() == document["sha256"], path
            assert git_blob(path) == document["blob_sha"], path

        representative = document["representative_path"]
        assert physical_line_count(representative) == document["line_count"]

        tracked = coverage_by_blob[document["blob_sha"]]
        assert tracked["representative_path"] == document["representative_path"]
        assert tracked["line_count"] == document["line_count"]
        assert tracked["category"] == document["category"]
        if arguments.coverage_state == "initial":
            assert tracked["status"] == "UNREAD"
            assert tracked["coverage"] == []
            assert tracked["review_evidence"] == []
            assert tracked["claim_ids"] == []
        else:
            assert tracked["status"] == "READ"
            assert tracked["coverage"] == [
                {"start_line": 1, "end_line": document["line_count"]}
            ]
            assert tracked["review_evidence"]
            assert tracked["claim_ids"]
            for evidence in tracked["review_evidence"]:
                assert (REPO_ROOT / evidence).is_file(), evidence
            for claim_id in tracked["claim_ids"]:
                assert re.fullmatch(r"INTENT-PROV-\d{4}", claim_id)
                all_claim_ids.add(claim_id)

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

    if arguments.coverage_state == "initial":
        assert coverage["status_counts"] == {"UNREAD": 271}
        assert coverage["completed_lines"] == 0
    else:
        assert coverage["status_counts"] == {"READ": 271}
        assert coverage["completed_lines"] == queue["total_lines"]
        claim_numbers = sorted(
            int(claim_id.rsplit("-", 1)[1]) for claim_id in all_claim_ids
        )
        assert claim_numbers == list(range(1, 405))
        assert (REPO_ROOT / coverage["last_applied_batch"]).is_file()
        assert (REPO_ROOT / coverage["last_applied_result"]).is_file()

    print(
        json.dumps(
            {
                "status": "PASS",
                "coverage_state": arguments.coverage_state,
                "documents": len(documents),
                "lines": queue["total_lines"],
                "chunks": queue["chunk_count"],
                "all_paths_checked": len(checked_paths),
                "claim_ids": len(all_claim_ids),
                "all_introduction_commits_are_baseline_ancestors": True,
                "all_chunks_are_contiguous": True,
                "all_source_blobs_and_sha256_match": True,
                "all_physical_extents_reach_eof": True,
                "all_coverage_ranges_are_complete": (
                    arguments.coverage_state == "complete"
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
