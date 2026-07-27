#!/usr/bin/env python3
"""Mark only the six fully read theory blobs COMPLETE in Phase 058 coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COVERAGE = ROOT / "Codex" / "results" / "PHASE_058_V1010_V1013_TEXT_COVERAGE.json"
THEORY_PATHS = {
    "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex",
    "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex",
    "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex",
    "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex",
    "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
    "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
}


def main() -> None:
    data = json.loads(COVERAGE.read_text(encoding="utf-8"))
    found = set()
    for document in data["documents"]:
        path = document["representative_path"]
        if path not in THEORY_PATHS:
            continue
        found.add(path)
        line_count = document["line_count"]
        document["status"] = "COMPLETE"
        document["coverage"] = [{"line_start": 1, "line_end": line_count}]
        document["review_evidence"] = [
            "Codex/results/PHASE_058_THEORY_SOURCE_STRUCTURE_INDEX.md",
            "Codex/results/PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json",
            "Codex/results/PHASE_058_THEORY_SOURCE_REVIEW.md",
        ]
        document["notes"] = [
            "Every source line was read in contiguous chunks.",
            "Physical verdicts remain provisional until code, probes, and primary-literature checks.",
        ]
    missing = THEORY_PATHS - found
    if missing:
        raise SystemExit(f"missing theory paths in coverage manifest: {sorted(missing)}")

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
