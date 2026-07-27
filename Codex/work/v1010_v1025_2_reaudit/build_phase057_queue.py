"""Build the deterministic Phase 057 intent-recovery read queue."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
CHUNK_LINES = 400
EXPECTED_DOCUMENTS = 271
EXPECTED_LINES = 57_795

REPO_ROOT = Path(__file__).resolve().parents[3]
MASTER_COVERAGE = (
    REPO_ROOT / "Codex/results/PHASE_056_V1010_V1025_2_READ_COVERAGE.json"
)
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


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.removeprefix("v").split("."))


def version_from_path(path: str) -> str:
    return Path(path).parts[2]


def category(path: str) -> str:
    lowered = path.lower()
    name = Path(path).name.lower()
    parts = {part.lower() for part in Path(path).parts}

    if name.endswith(".json"):
        return "MACHINE_EVIDENCE"
    if "handover" in name:
        return "HANDOVER"
    if "change_log" in name or "changelog" in name:
        return "CHANGE_LOG"
    if "reference_ledger" in name or "refledger" in name:
        return "REFERENCE_LEDGER"
    if "execution_ledger" in name or name.endswith("_ledger.md"):
        return "EXECUTION_LEDGER"
    if "plans" in parts or name.startswith("plan_") or "master-plan" in name:
        return "PLAN"
    if name == "fitting_guide.md":
        return "FITTING_GUIDE"
    if name == "code_guide_v24.html":
        return "CODE_GUIDE"
    if (
        "audit" in name
        or "direction" in name
        or "judgment" in name
        or "review" in name
        or "problem_report" in name
        or "integrity_report" in name
    ):
        return "DIRECTION_OR_AUDIT"
    if "results" in parts or "result" in name or "report" in name:
        return "RESULT"
    if Path(path).suffix.lower() in {".txt", ".html"}:
        return "OTHER_SUPPORT"
    if "guide" in lowered:
        return "OTHER_SUPPORT"
    return "OTHER_SUPPORT"


def first_addition(path: str) -> dict[str, str | None]:
    completed = subprocess.run(
        [
            "git",
            "log",
            "--all",
            "--reverse",
            "--diff-filter=A",
            "--format=%H%x09%aI%x09%s",
            "--",
            path,
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    records = [line for line in completed.stdout.splitlines() if line.strip()]
    if not records:
        return {"commit": None, "date": None, "subject": None}
    fields = records[0].split("\t", 2)
    if len(fields) != 3:
        raise ValueError(f"unexpected git log record for {path}: {records[0]}")
    return {"commit": fields[0], "date": fields[1], "subject": fields[2]}


def chunks(line_count: int) -> list[dict[str, int | str]]:
    if line_count < 1:
        raise ValueError("Phase 057 text candidate has no lines")
    result: list[dict[str, int | str]] = []
    start = 1
    index = 1
    while start <= line_count:
        end = min(start + CHUNK_LINES - 1, line_count)
        result.append(
            {
                "chunk_id": f"C{index:04d}",
                "start_line": start,
                "end_line": end,
                "status": "UNREAD",
            }
        )
        start = end + 1
        index += 1
    return result


def main() -> None:
    master = read_json(MASTER_COVERAGE)
    candidates: list[dict[str, Any]] = []
    pattern = re.compile(r"\.(md|json|txt|html)$", re.IGNORECASE)
    for group in master["groups"]:
        representative = group["representative_path"]
        if group["review_mode"] != "FULL_TEXT" or not pattern.search(representative):
            continue
        line_count = int(group["extent"]["lines"])
        version = version_from_path(representative)
        candidates.append(
            {
                "blob_sha": group["blob_sha"],
                "sha256": group["sha256"],
                "representative_path": representative,
                "all_paths": group["paths"],
                "first_representative_version": version,
                "category": category(representative),
                "line_count": line_count,
                "introduction": first_addition(representative),
                "chunks": chunks(line_count),
                "status": "UNREAD",
                "observations": [],
            }
        )

    candidates.sort(
        key=lambda item: (
            version_key(item["first_representative_version"]),
            item["introduction"]["date"] or "",
            item["representative_path"],
        )
    )

    document_count = len(candidates)
    total_lines = sum(item["line_count"] for item in candidates)
    chunk_count = sum(len(item["chunks"]) for item in candidates)
    category_counts = dict(
        sorted(Counter(item["category"] for item in candidates).items())
    )
    version_counts = dict(
        sorted(
            Counter(
                item["first_representative_version"] for item in candidates
            ).items(),
            key=lambda pair: version_key(pair[0]),
        )
    )
    missing_introduction = [
        item["representative_path"]
        for item in candidates
        if item["introduction"]["commit"] is None
    ]

    queue = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "chunk_line_limit": CHUNK_LINES,
        "document_count": document_count,
        "total_lines": total_lines,
        "chunk_count": chunk_count,
        "counts": {
            "by_category": category_counts,
            "by_first_representative_version": version_counts,
        },
        "validation": {
            "expected_document_count": EXPECTED_DOCUMENTS,
            "expected_total_lines": EXPECTED_LINES,
            "document_count_matches": document_count == EXPECTED_DOCUMENTS,
            "total_lines_match": total_lines == EXPECTED_LINES,
            "missing_introduction_count": len(missing_introduction),
            "missing_introduction_paths": missing_introduction,
        },
        "documents": candidates,
    }
    coverage = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "source_queue": str(QUEUE_PATH.relative_to(REPO_ROOT)),
        "document_count": document_count,
        "total_lines": total_lines,
        "chunk_count": chunk_count,
        "status_counts": {"UNREAD": document_count},
        "completed_lines": 0,
        "documents": [
            {
                "blob_sha": item["blob_sha"],
                "representative_path": item["representative_path"],
                "line_count": item["line_count"],
                "category": item["category"],
                "status": "UNREAD",
                "coverage": [],
                "review_evidence": [],
                "claim_ids": [],
                "notes": [],
            }
            for item in candidates
        ],
    }

    write_json(QUEUE_PATH, queue)
    write_json(COVERAGE_PATH, coverage)
    print(
        json.dumps(
            {
                "queue": str(QUEUE_PATH.relative_to(REPO_ROOT)),
                "coverage": str(COVERAGE_PATH.relative_to(REPO_ROOT)),
                "document_count": document_count,
                "total_lines": total_lines,
                "chunk_count": chunk_count,
                "missing_introduction_count": len(missing_introduction),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
