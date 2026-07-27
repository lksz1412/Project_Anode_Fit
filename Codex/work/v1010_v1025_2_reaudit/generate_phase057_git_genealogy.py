"""Generate Git event genealogy for every Phase 057 intent document."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
REPO_ROOT = Path(__file__).resolve().parents[3]
QUEUE_PATH = REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json"
OUTPUT_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_GIT_DOCUMENT_GENEALOGY.json"
)
COMPLETION_PATTERN = re.compile(
    r"(?i)(?:\bPASS\b|\bGREEN\b|완료|완결|정본|bit[- ]?exact|"
    r"무변경|전건|merge[- ]?ready|마감)"
)


def run_git(*arguments: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def path_history(path: str) -> list[dict[str, Any]]:
    output = run_git(
        "log",
        "--reverse",
        "--format=@@C%x1f%H%x1f%aI%x1f%P%x1f%s",
        "--raw",
        "--full-index",
        "--no-abbrev",
        BASELINE,
        "--",
        path,
    )
    events: list[dict[str, Any]] = []
    metadata: dict[str, Any] | None = None
    for line in output.splitlines():
        if line.startswith("@@C\x1f"):
            fields = line.split("\x1f", 4)
            metadata = {
                "commit": fields[1],
                "date": fields[2],
                "parents": fields[3].split() if fields[3] else [],
                "subject": fields[4],
            }
        elif line.startswith(":"):
            assert metadata is not None, path
            raw, *raw_paths = line.split("\t")
            fields = raw.split()
            assert len(fields) == 5, line
            blob_before = fields[2]
            blob_after = fields[3]
            events.append(
                {
                    **metadata,
                    "kind_first_parent": fields[4],
                    "blob_before_first_parent": (
                        None if set(blob_before) == {"0"} else blob_before
                    ),
                    "blob_after": (
                        None if set(blob_after) == {"0"} else blob_after
                    ),
                    "raw_paths": raw_paths,
                }
            )
    return events


def main() -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    assert queue["baseline_commit"] == BASELINE

    topo_commits = run_git(
        "rev-list", "--reverse", "--topo-order", BASELINE
    ).splitlines()
    topo_index = {commit: index for index, commit in enumerate(topo_commits)}
    documents: list[dict[str, Any]] = []
    global_commits: set[str] = set()
    path_event_count = 0
    event_kind_counts: Counter[str] = Counter()
    relation_counts: Counter[str] = Counter()
    marker_commit_counts: Counter[str] = Counter()
    recorded_introduction_blob_mismatch_count = 0

    for document in queue["documents"]:
        introduction = document["introduction"]["commit"]
        assert introduction in topo_index
        path_records: list[dict[str, Any]] = []
        exact_blob_events: list[dict[str, str]] = []

        for path in document["all_paths"]:
            events: list[dict[str, Any]] = []
            for event in path_history(path):
                commit = event["commit"]
                if commit == introduction:
                    relation = "INTRODUCTION_COMMIT"
                elif topo_index[commit] > topo_index[introduction]:
                    relation = "POST_INTRODUCTION"
                else:
                    relation = "PRIOR_OR_PARALLEL"

                markers = sorted(
                    {match.group(0) for match in COMPLETION_PATTERN.finditer(
                        event["subject"]
                    )}
                )
                event["relation_to_recorded_introduction"] = relation
                event["completion_markers_in_subject"] = markers
                events.append(event)
                global_commits.add(commit)
                event_kind_counts[event["kind_first_parent"]] += 1
                relation_counts[relation] += 1
                if markers:
                    marker_commit_counts[commit] += 1
                if event["blob_after"] == document["blob_sha"]:
                    exact_blob_events.append(
                        {
                            "path": path,
                            "commit": commit,
                            "date": event["date"],
                            "relation_to_recorded_introduction": relation,
                        }
                    )

            path_event_count += len(events)
            path_records.append(
                {
                    "path": path,
                    "event_count": len(events),
                    "events": events,
                }
            )

        assert exact_blob_events, document["representative_path"]
        exact_blob_events.sort(
            key=lambda item: (item["date"], item["commit"], item["path"])
        )
        recorded_introduction_matches_blob = any(
            event["commit"] == introduction for event in exact_blob_events
        )
        if not recorded_introduction_matches_blob:
            recorded_introduction_blob_mismatch_count += 1
        documents.append(
            {
                "blob_sha": document["blob_sha"],
                "sha256": document["sha256"],
                "representative_path": document["representative_path"],
                "category": document["category"],
                "line_count": document["line_count"],
                "recorded_introduction": document["introduction"],
                "recorded_introduction_matches_current_blob": (
                    recorded_introduction_matches_blob
                ),
                "first_exact_blob_event": exact_blob_events[0],
                "all_exact_blob_events": exact_blob_events,
                "occurrence_path_count": len(path_records),
                "path_event_count": sum(
                    record["event_count"] for record in path_records
                ),
                "paths": path_records,
            }
        )

    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "source_queue": str(QUEUE_PATH.relative_to(REPO_ROOT)),
        "document_count": len(documents),
        "occurrence_path_count": sum(
            item["occurrence_path_count"] for item in documents
        ),
        "path_event_count": path_event_count,
        "unique_commit_count": len(global_commits),
        "event_kind_counts": dict(sorted(event_kind_counts.items())),
        "relation_counts": dict(sorted(relation_counts.items())),
        "completion_marker_commit_count": len(marker_commit_counts),
        "recorded_introduction_blob_mismatch_count": (
            recorded_introduction_blob_mismatch_count
        ),
        "documents": documents,
        "validation": {
            "all_queue_documents_present": len(documents)
            == queue["document_count"],
            "all_current_blobs_have_exact_history_event": True,
            "all_histories_limited_to_baseline": True,
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(encoded, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)),
                "documents": payload["document_count"],
                "paths": payload["occurrence_path_count"],
                "events": payload["path_event_count"],
                "commits": payload["unique_commit_count"],
                "completion_marker_commits": payload[
                    "completion_marker_commit_count"
                ],
                "recorded_introduction_blob_mismatches": payload[
                    "recorded_introduction_blob_mismatch_count"
                ],
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
