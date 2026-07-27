#!/usr/bin/env python3
"""Validate Phase 059 test/demo assertion and evidence inventory."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
MATRIX = RESULTS / "PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json"
SUMMARY = RESULTS / "PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md"
QUEUE = RESULTS / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = matrix["records"]
    findings = matrix["findings"]
    by_finding = {item["id"]: item for item in findings}
    queue_map = {
        item["representative_path"]: item
        for item in queue["records"]
        if item["role"] in {"test", "demo"}
    }

    checks: list[tuple[str, bool]] = []
    checks.append(("summary exists", SUMMARY.is_file()))
    checks.append(
        (
            "gate exact",
            matrix["status"] == "PASS_P059_TEST_DEMO_ASSERTION_INVENTORY",
        )
    )
    checks.append(("record count", matrix["record_count"] == len(records) == 30))
    checks.append(("test count", matrix["test_record_count"] == 12))
    checks.append(("demo count", matrix["demo_record_count"] == 18))
    checks.append(("line count", matrix["total_line_count"] == 3372))
    checks.append(("assert count", matrix["total_assert_count"] == 0))
    checks.append(("logic family count", matrix["logic_family_count"] == 5))
    checks.append(
        (
            "family names exact",
            set(matrix["family_summary"])
            == {
                "sample_test",
                "regression",
                "graph_suite",
                "demo_lco_heat",
                "plot_dqdv",
            },
        )
    )
    checks.append(
        (
            "six files per family",
            all(
                item["file_count"] == 6
                for item in matrix["family_summary"].values()
            ),
        )
    )
    checks.append(
        (
            "one logic hash per family",
            all(
                len(item["logic_hashes"]) == 1
                for item in matrix["family_summary"].values()
            ),
        )
    )
    checks.append(
        (
            "logic groups six paths each",
            len(matrix["logic_groups"]) == 5
            and all(len(item["paths"]) == 6 for item in matrix["logic_groups"]),
        )
    )

    source_exact = True
    queue_exact = True
    ast_assert_exact = True
    for record in records:
        raw = (ROOT / record["representative_path"]).read_bytes()
        source_exact &= (
            record["sha256"] == sha256_bytes(raw)
            and record["line_count"] == len(raw.decode("utf-8").splitlines())
        )
        queue_item = queue_map[record["representative_path"]]
        queue_exact &= (
            record["git_blob_sha"] == queue_item["blob_sha"]
            and record["role"] == queue_item["role"]
            and record["occurrence_paths"] == queue_item["occurrence_paths"]
        )
        tree = ast.parse(raw.decode("utf-8"))
        ast_assert_exact &= record["assert_count"] == sum(
            isinstance(node, ast.Assert) for node in ast.walk(tree)
        )
    checks.append(("source hashes exact", source_exact))
    checks.append(("queue links exact", queue_exact))
    checks.append(("AST assert counts exact", ast_assert_exact))

    checks.append(
        (
            "only regression enforced",
            all(
                record["evidence_class"]
                == (
                    "ENFORCED_INTERNAL_REGRESSION"
                    if record["family"] == "regression"
                    else "PRINT_ONLY_VISUALIZATION"
                )
                for record in records
            ),
        )
    )
    checks.append(
        (
            "array_equal count",
            sum(len(record["array_equal_calls"]) for record in records) == 6,
        )
    )
    checks.append(
        (
            "no allclose gate",
            sum(len(record["allclose_calls"]) for record in records) == 0,
        )
    )
    checks.append(
        (
            "non-regression has no exit",
            sum(
                len(record["exit_calls"])
                for record in records
                if record["family"] != "regression"
            )
            == 0,
        )
    )
    checks.append(
        (
            "golden reads and writes regression only",
            sum(len(record["golden_read_calls"]) for record in records) == 6
            and sum(len(record["golden_write_calls"]) for record in records)
            == 6
            and all(
                not record["golden_read_calls"]
                and not record["golden_write_calls"]
                for record in records
                if record["family"] != "regression"
            ),
        )
    )
    checks.append(
        (
            "twenty-four figure writes",
            sum(len(record["figure_write_calls"]) for record in records) == 24,
        )
    )
    checks.append(
        (
            "headline feature tokens absent",
            all(
                record["feature_tokens"]["n_T1"] == 0
                and record["feature_tokens"]["theta_E"] == 0
                for record in records
            ),
        )
    )
    checks.append(
        (
            "critical branch tokens absent",
            all(
                record["feature_tokens"]["L_V"] == 0
                and record["feature_tokens"]["nonmonot"] == 0
                and record["feature_tokens"]["reversal"] == 0
                and record["feature_tokens"]["pulse"] == 0
                for record in records
            ),
        )
    )
    checks.append(
        (
            "measured data tokens absent",
            all(
                record["feature_tokens"]["experimental"] == 0
                and record["feature_tokens"]["measured"] == 0
                for record in records
            ),
        )
    )

    checks.append(("finding count", matrix["finding_count"] == 15))
    checks.append(("finding ids unique", len(by_finding) == 15))
    checks.append(
        (
            "finding ids exact sequence",
            [item["id"] for item in findings]
            == [f"P059-TD-{number:03d}" for number in range(1, 16)],
        )
    )
    anchors_exact = True
    for item in findings:
        for evidence in item["source_evidence"]:
            line = (
                (ROOT / evidence["path"])
                .read_text(encoding="utf-8")
                .splitlines()[evidence["line"] - 1]
            )
            anchors_exact &= (
                line == evidence["source_line"]
                and evidence["needle"] in evidence["source_line"]
            )
    checks.append(("finding anchors exact", anchors_exact))
    checks.append(
        (
            "area nongate retained",
            by_finding["P059-TD-003"]["disposition"] == "OVERCLAIM_RISK",
        )
    )
    checks.append(
        (
            "capture control retained",
            by_finding["P059-TD-004"]["disposition"] == "CONTROL_REQUIRED",
        )
    )
    checks.append(
        (
            "copy-forward retained",
            by_finding["P059-TD-010"]["disposition"] == "COPY_FORWARD",
        )
    )
    checks.append(
        (
            "headline branch gap retained",
            by_finding["P059-TD-011"]["disposition"] == "MISSING",
        )
    )
    checks.append(
        (
            "external validity absent",
            by_finding["P059-TD-013"]["disposition"] == "ABSENT",
        )
    )
    checks.append(
        (
            "authority overclaim retained",
            by_finding["P059-TD-014"]["disposition"] == "OVERCLAIMED",
        )
    )

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 TEST/DEMO MATRIX FAIL: {failed}")
    print(
        "PASS_P059_TEST_DEMO_ASSERTIONS "
        f"checks={len(checks)}/{len(checks)} files=30 findings=15"
    )


if __name__ == "__main__":
    main()
