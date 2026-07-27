#!/usr/bin/env python3
"""Validate Phase 059 completion/authority/carry-forward claim evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
MATRIX = RESULTS / "PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json"
SUMMARY = RESULTS / "PHASE_059_COMPLETION_AUTHORITY_REVIEW.md"
LINEAGE = RESULTS / "PHASE_059_THEORY_LINEAGE_DIFF.json"
CONTRACTS = RESULTS / "PHASE_059_THEORY_CONTRACT_MATRIX.json"
COVERAGE = RESULTS / "PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json"
QUEUE = RESULTS / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"

EXPECTED_CLASSES = {
    "USER_REQUIREMENT",
    "PROCESS_HISTORY",
    "THEORY_CHANGE",
    "IMPLEMENTATION_CHANGE",
    "INTERNAL_VALIDATION",
    "SCIENTIFIC_SCOPE",
    "CARRY_FORWARD",
    "EXTERNAL_REVIEW",
}
EXPECTED_DISPOSITIONS = {
    "PRESERVE_REQUIREMENT",
    "PATCH_CONFIRMED",
    "PATCH_CONFIRMED_INTERNAL_ONLY",
    "SOURCE_STATEMENT_ONLY",
    "COPY_FORWARD_NO_NEW_VALIDATION",
    "PARTIAL",
    "OVERCLAIMED",
    "CARRY_FORWARD_OPEN",
    "REVIEW_INPUT_NOT_AUTHORITY",
    "SUPERSEDED",
}


def main() -> None:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    lineage = json.loads(LINEAGE.read_text(encoding="utf-8"))
    contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = matrix["records"]
    by_id = {record["id"]: record for record in records}
    patch_by_id = {item["pair_id"]: item for item in lineage["comparisons"]}
    contract_ids = {item["id"] for item in contracts["records"]}

    coverage_paths: set[str] = set()
    completed_blobs = {
        item["blob_sha"]
        for item in coverage["documents"]
        if item["status"] == "COMPLETE"
    }
    for item in queue["records"]:
        if item["blob_sha"] in completed_blobs:
            coverage_paths.add(item["representative_path"])
            coverage_paths.update(item["occurrence_paths"])

    checks: list[tuple[str, bool]] = []
    checks.append(("summary exists", SUMMARY.is_file()))
    checks.append(
        (
            "gate exact",
            matrix["status"] == "PASS_P059_COMPLETION_AUTHORITY_ADJUDICATION",
        )
    )
    checks.append(("record count field", matrix["record_count"] == 40))
    checks.append(("record list count", len(records) == 40))
    checks.append(("record ids unique", len(by_id) == 40))
    checks.append(
        (
            "record ids exact sequence",
            [record["id"] for record in records]
            == [f"P059-CLM-{number:03d}" for number in range(1, 41)],
        )
    )
    checks.append(
        (
            "claim classes exact",
            {record["claim_class"] for record in records} == EXPECTED_CLASSES,
        )
    )
    checks.append(
        (
            "dispositions allowed",
            all(
                record["disposition"] in EXPECTED_DISPOSITIONS
                for record in records
            ),
        )
    )
    checks.append(
        (
            "required fields nonempty",
            all(
                record["claim"]
                and record["source_evidence"]
                and record["authority_meaning"]
                and record["remaining_work"]
                and record["evidence_boundary"]
                for record in records
            ),
        )
    )

    anchors_exact = True
    anchors_in_coverage = True
    for record in records:
        for evidence in record["source_evidence"]:
            path = ROOT / evidence["path"]
            lines = path.read_text(encoding="utf-8").splitlines()
            anchors_exact &= (
                1 <= evidence["line"] <= len(lines)
                and lines[evidence["line"] - 1] == evidence["source_line"]
                and evidence["needle"] in evidence["source_line"]
            )
            anchors_in_coverage &= evidence["path"] in coverage_paths
    checks.append(("source anchors exact", anchors_exact))
    checks.append(("source anchors in frozen coverage", anchors_in_coverage))

    patch_evidence_exact = True
    for record in records:
        patch_evidence = {item["pair_id"]: item for item in record["patch_evidence"]}
        patch_evidence_exact &= set(record["patch_ids"]) == set(patch_evidence)
        for pair_id, evidence in patch_evidence.items():
            source = patch_by_id[pair_id]
            patch_evidence_exact &= (
                evidence["exact_unified_diff"] == source["exact_unified_diff"]
                and evidence["exact_unified_diff_sha256"]
                == source["exact_unified_diff_sha256"]
                and evidence["content_identical"] == source["content_identical"]
                and (ROOT / evidence["exact_unified_diff"]).is_file()
            )
    checks.append(("patch evidence exact", patch_evidence_exact))
    checks.append(
        (
            "contract links exact",
            all(
                set(record["contract_ids"]).issubset(contract_ids)
                for record in records
            ),
        )
    )
    checks.append(
        (
            "aggregate class counts",
            sum(matrix["claim_class_counts"].values()) == 40
            and set(matrix["claim_class_counts"]) == EXPECTED_CLASSES,
        )
    )
    checks.append(
        (
            "aggregate disposition counts",
            sum(matrix["disposition_counts"].values()) == 40,
        )
    )
    checks.append(
        (
            "actor counts aggregate",
            sum(matrix["actor_counts"].values()) == 40
            and matrix["actor_counts"]["USER"] == 10
            and matrix["actor_counts"]["EXTERNAL_REVIEWER"] == 1,
        )
    )
    checks.append(
        (
            "user constitution preserved",
            all(
                by_id[f"P059-CLM-{number:03d}"]["disposition"]
                == "PRESERVE_REQUIREMENT"
                for number in (1, 2, 3, 4, 5, 6, 7)
            ),
        )
    )
    checks.append(
        (
            "v15 pointwise patch bounded",
            by_id["P059-CLM-014"]["disposition"] == "PATCH_CONFIRMED"
            and "PHYSICAL_CLOSURE_OPEN"
            in by_id["P059-CLM-014"]["evidence_boundary"],
        )
    )
    checks.append(
        (
            "code claim deferred",
            by_id["P059-CLM-015"]["disposition"] == "SOURCE_STATEMENT_ONLY"
            and by_id["P059-CLM-015"]["evidence_boundary"]
            == "CODE_DIFF_AND_EXECUTION_DEFERRED_STEP_34",
        )
    )
    checks.append(
        (
            "copy-forward releases bounded",
            by_id["P059-CLM-029"]["disposition"]
            == "COPY_FORWARD_NO_NEW_VALIDATION"
            and by_id["P059-CLM-030"]["disposition"]
            == "COPY_FORWARD_NO_NEW_VALIDATION",
        )
    )
    checks.append(
        (
            "Einstein capability bounded",
            by_id["P059-CLM-033"]["disposition"] == "CARRY_FORWARD_OPEN"
            and "P059-CON-032" in by_id["P059-CLM-033"]["contract_ids"],
        )
    )
    checks.append(
        (
            "physical-version overclaim retained",
            by_id["P059-CLM-035"]["disposition"] == "OVERCLAIMED",
        )
    )
    checks.append(
        (
            "review verdict not authority",
            by_id["P059-CLM-036"]["disposition"]
            == "REVIEW_INPUT_NOT_AUTHORITY",
        )
    )
    checks.append(
        (
            "CH voltage-lag overclaim retained",
            by_id["P059-CLM-038"]["disposition"] == "OVERCLAIMED",
        )
    )
    checks.append(
        (
            "final carry-forward remains open",
            by_id["P059-CLM-039"]["disposition"] == "CARRY_FORWARD_OPEN",
        )
    )
    checks.append(
        (
            "v1026 excluded",
            all(record["version"] != "v1.0.26" for record in records),
        )
    )

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 COMPLETION CLAIM FAIL: {failed}")
    print(
        "PASS_P059_COMPLETION_CLAIMS "
        f"checks={len(checks)}/{len(checks)} records=40"
    )


if __name__ == "__main__":
    main()
