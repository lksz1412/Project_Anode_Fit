#!/usr/bin/env python3
"""Validate Phase 059 theory contracts and their frozen source anchors."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
MATRIX = RESULTS / "PHASE_059_THEORY_CONTRACT_MATRIX.json"
SUMMARY = RESULTS / "PHASE_059_THEORY_CONTRACT_REVIEW.md"
INDEX = RESULTS / "PHASE_059_THEORY_SOURCE_INDEX.json"

EXPECTED_TOPICS = {
    "coordinates",
    "phase_separation",
    "width",
    "memory",
    "n_of_T",
    "entropy_heat",
    "einstein_vibration",
    "lco_electronic",
}
ALLOWED_DISPOSITIONS = {
    "PRESERVE",
    "CORRECT",
    "EMPIRICAL_ONLY",
    "THEORY_ONLY",
    "REJECT",
    "UNVERIFIED",
}


def compact(text: str, limit: int = 500) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


def source_excerpt(path: str, line_start: int, line_end: int) -> str:
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    start = max(line_start - 2, 0)
    end = min(line_end + 1, len(lines))
    return compact("\n".join(lines[start:end]))


def main() -> None:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    records = matrix["records"]
    checks: list[tuple[str, bool]] = []
    checks.append(("summary exists", SUMMARY.is_file()))
    checks.append(
        (
            "gate exact",
            matrix["status"] == "PASS_P059_THEORY_CONTRACT_EXTRACTION",
        )
    )
    checks.append(("record count field", matrix["record_count"] == 38))
    checks.append(("record list count", len(records) == 38))
    checks.append(
        ("record ids unique", len({record["id"] for record in records}) == 38)
    )
    checks.append(
        (
            "record ids exact sequence",
            [record["id"] for record in records]
            == [f"P059-CON-{number:03d}" for number in range(1, 39)],
        )
    )
    checks.append(
        ("all required topics", {record["topic"] for record in records} == EXPECTED_TOPICS)
    )
    checks.append(
        (
            "all dispositions allowed",
            all(record["disposition"] in ALLOWED_DISPOSITIONS for record in records),
        )
    )
    checks.append(
        (
            "contract fields nonempty",
            all(
                record["symbols"]
                and record["quantity"]
                and record["unit"]
                and record["sign_or_orientation"]
                and record["assumptions"]
                and record["required_action"]
                and record["evidence"]
                for record in records
            ),
        )
    )
    index_paths = {document["representative_path"] for document in index["documents"]}
    checks.append(
        (
            "all evidence paths indexed theory",
            all(
                evidence["path"] in index_paths
                for record in records
                for evidence in record["evidence"]
            ),
        )
    )

    evidence_exact = True
    label_exact = True
    indexed_labels = {
        (label["path"], label["label"], label["line"])
        for label in index["labels"]
    }
    for record in records:
        for evidence in record["evidence"]:
            evidence_exact &= (
                source_excerpt(
                    evidence["path"],
                    evidence["line_start"],
                    evidence["line_end"],
                )
                == evidence["source_excerpt"]
            )
            if evidence["kind"] == "equation_or_label":
                label_exact &= (
                    evidence["path"],
                    evidence["label"],
                    evidence["line_start"],
                ) in indexed_labels
            elif evidence["kind"] == "prose_regex":
                source_line = (ROOT / evidence["path"]).read_text(
                    encoding="utf-8"
                ).splitlines()[evidence["line_start"] - 1]
                evidence_exact &= bool(re.search(evidence["pattern"], source_line))
    checks.append(("all evidence excerpts exact", evidence_exact))
    checks.append(("all label anchors exact", label_exact))

    by_id = {record["id"]: record for record in records}
    checks.append(
        (
            "unit blocker retained",
            by_id["P059-CON-003"]["closure_state"] == "OPEN_DIMENSIONAL_BLOCKER",
        )
    )
    checks.append(
        (
            "two-phase semantic blocker retained",
            by_id["P059-CON-015"]["closure_state"]
            == "OPEN_TWO_PHASE_SEMANTIC_CONTRADICTION",
        )
    )
    checks.append(
        (
            "frozen affinity rejected",
            by_id["P059-CON-020"]["disposition"] == "REJECT",
        )
    )
    checks.append(
        (
            "Einstein reaction definition open",
            by_id["P059-CON-032"]["closure_state"]
            == "OPEN_REACTION_QUANTITY_DEFINITION",
        )
    )
    checks.append(
        (
            "high-voltage goal open",
            by_id["P059-CON-033"]["closure_state"]
            == "OPEN_USER_GOAL_HIGH_VOLTAGE_LCO",
        )
    )
    checks.append(
        (
            "topic counts aggregate",
            sum(matrix["topic_counts"].values()) == 38
            and set(matrix["topic_counts"]) == EXPECTED_TOPICS,
        )
    )
    checks.append(
        (
            "disposition counts aggregate",
            sum(matrix["disposition_counts"].values()) == 38,
        )
    )

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 THEORY CONTRACT FAIL: {failed}")
    print(
        "PASS_P059_THEORY_CONTRACTS "
        f"checks={len(checks)}/{len(checks)} records=38 topics=8"
    )


if __name__ == "__main__":
    main()
