#!/usr/bin/env python3
"""Mark the three fully read production code blobs COMPLETE."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COVERAGE = ROOT / "Codex" / "results" / "PHASE_058_V1010_V1013_TEXT_COVERAGE.json"
CODE_PATHS = {
    "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py",
    "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
}


def main() -> None:
    data = json.loads(COVERAGE.read_text(encoding="utf-8"))
    found = set()
    for document in data["documents"]:
        path = document["representative_path"]
        if path not in CODE_PATHS:
            continue
        found.add(path)
        document["status"] = "COMPLETE"
        document["coverage"] = [{"line_start": 1, "line_end": document["line_count"]}]
        document["review_evidence"] = [
            "Codex/results/PHASE_058_CODE_BEHAVIOR_MATRIX.json",
            "Codex/results/PHASE_058_CODE_SOURCE_REVIEW.md",
        ]
        document["notes"] = [
            "Every production-code line was read.",
            "Execution probes, tests, demos, and external physical validity remain pending.",
        ]
    if found != CODE_PATHS:
        raise SystemExit(f"missing code paths: {sorted(CODE_PATHS - found)}")
    counts: dict[str, int] = {}
    completed_lines = 0
    for document in data["documents"]:
        counts[document["status"]] = counts.get(document["status"], 0) + 1
        if document["status"] == "COMPLETE":
            completed_lines += document["line_count"]
    data["status_counts"] = counts
    data["completed_lines"] = completed_lines
    COVERAGE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
