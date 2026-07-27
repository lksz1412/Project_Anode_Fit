"""Apply a verified human-read batch to the Phase 057 coverage ledger."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
QUEUE_PATH = REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json"
COVERAGE_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_COVERAGE.json"
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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
    parser.add_argument("batch_json")
    arguments = parser.parse_args()

    batch_path = (REPO_ROOT / arguments.batch_json).resolve()
    batch = read_json(batch_path)
    queue = read_json(QUEUE_PATH)
    coverage = read_json(COVERAGE_PATH)

    queue_by_path = {
        item["representative_path"]: item for item in queue["documents"]
    }
    coverage_by_path = {
        item["representative_path"]: item for item in coverage["documents"]
    }

    applied: list[str] = []
    for record in batch["documents"]:
        path = record["representative_path"]
        if path not in queue_by_path or path not in coverage_by_path:
            raise KeyError(f"path not in Phase 057 queue: {path}")
        queue_item = queue_by_path[path]
        coverage_item = coverage_by_path[path]
        expected_lines = int(record["line_count"])
        expected_blob = queue_item["blob_sha"]

        if expected_lines != queue_item["line_count"]:
            raise ValueError(f"queue line mismatch: {path}")
        if physical_line_count(path) != expected_lines:
            raise ValueError(f"physical line mismatch: {path}")
        if git_blob(path) != expected_blob:
            raise ValueError(f"working-tree blob mismatch: {path}")
        if coverage_item["status"] not in {"UNREAD", "READ"}:
            raise ValueError(
                f"cannot apply read batch to {coverage_item['status']}: {path}"
            )

        expected_coverage = [{"start_line": 1, "end_line": expected_lines}]
        if coverage_item["status"] == "READ":
            if coverage_item["coverage"] != expected_coverage:
                raise ValueError(f"existing coverage mismatch: {path}")
        else:
            coverage_item["status"] = "READ"
            coverage_item["coverage"] = expected_coverage
            coverage_item["review_evidence"] = list(
                record["review_evidence"]
            )
            coverage_item["claim_ids"] = list(record["claim_ids"])
            coverage_item["notes"] = list(record.get("notes", []))
        applied.append(path)

    status_counts = Counter(item["status"] for item in coverage["documents"])
    coverage["status_counts"] = dict(sorted(status_counts.items()))
    coverage["completed_lines"] = sum(
        item["line_count"]
        for item in coverage["documents"]
        if item["status"] in {"READ", "VERIFIED"}
    )
    coverage["last_applied_batch"] = str(batch_path.relative_to(REPO_ROOT))
    coverage["last_applied_result"] = batch["result_path"]
    write_json(COVERAGE_PATH, coverage)

    print(
        json.dumps(
            {
                "status": "PASS",
                "applied_documents": len(applied),
                "completed_lines": coverage["completed_lines"],
                "status_counts": coverage["status_counts"],
                "batch": str(batch_path.relative_to(REPO_ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
