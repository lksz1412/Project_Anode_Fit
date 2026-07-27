#!/usr/bin/env python3
"""Validate complete Phase 058 equation-claim dispositions."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_058_THEORY_CLAIM_DISPOSITIONS.json"
MATRIX = ROOT / "Codex/results/PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json"
CLASSIFIER = (
    ROOT / "Codex/work/v1010_v1013_phase058/classify_phase058_equations.py"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_classifier():
    spec = importlib.util.spec_from_file_location("phase058_classifier", CLASSIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {CLASSIFIER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def nested_counts(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, int]]:
    values = sorted({row[key] for row in rows})
    return {
        value: dict(
            sorted(
                Counter(
                    row["decision"] for row in rows if row[key] == value
                ).items()
            )
        )
        for value in values
    }


def main() -> int:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    source = json.loads(MATRIX.read_text(encoding="utf-8"))
    classifier = load_classifier()
    rows = classifier.assignments()
    checks: dict[str, bool] = {}

    checks["matrix_hash"] = sha256(MATRIX) == data["source_matrix_sha256"]
    checks["classifier_hash"] = sha256(CLASSIFIER) == data["classifier_sha256"]
    checks["allowed_decisions"] = (
        set(data["allowed_decisions"]) == classifier.ALLOWED_DECISIONS
    )
    checks["category_default_count"] = (
        len(classifier.CATEGORY_DEFAULTS)
        == data["assignment_rule"]["category_default_count"]
    )
    checks["label_override_count"] = (
        len(classifier.LABEL_OVERRIDES)
        == data["assignment_rule"]["label_override_count"]
    )
    checks["v1010_superseded_count"] = (
        len(classifier.V1010_SUPERSEDED_BY_V1012)
        == data["assignment_rule"]["v1010_superseded_by_v1012_label_count"]
    )
    checks["pre_v1013_superseded_count"] = (
        len(classifier.PRE_V1013_SUPERSEDED_BY_V1013)
        == data["assignment_rule"]["pre_v1013_superseded_by_v1013_label_count"]
    )

    source_ids = [equation["equation_id"] for equation in source["equations"]]
    assigned_ids = [row["equation_id"] for row in rows]
    checks["source_ids_unique"] = len(source_ids) == len(set(source_ids))
    checks["assigned_ids_unique"] = len(assigned_ids) == len(set(assigned_ids))
    checks["complete_id_coverage"] = assigned_ids == source_ids
    checks["occurrence_count"] = (
        len(rows) == data["coverage"]["equation_occurrence_count"]
    )
    checks["assigned_count"] = (
        len(rows) == data["coverage"]["assigned_equation_occurrence_count"]
    )
    checks["unassigned_count"] = (
        len(set(source_ids) - set(assigned_ids))
        == data["coverage"]["unassigned_equation_occurrence_count"]
    )
    checks["unique_label_count"] = (
        len({row["label"] for row in rows})
        == data["coverage"]["unique_equation_label_count"]
    )

    serialized = "\n".join(
        f"{row['equation_id']}|{row['decision']}" for row in rows
    ).encode("utf-8")
    checks["assignment_hash"] = (
        hashlib.sha256(serialized).hexdigest()
        == data["coverage"]["assignment_sha256"]
    )
    checks["decision_counts"] = (
        dict(sorted(Counter(row["decision"] for row in rows).items()))
        == data["decision_counts"]
    )
    checks["version_counts"] = (
        nested_counts(rows, "version") == data["version_decision_counts"]
    )
    checks["category_counts"] = (
        nested_counts(rows, "category") == data["category_decision_counts"]
    )
    checks["no_invalid_decision"] = not (
        {row["decision"] for row in rows} - classifier.ALLOWED_DECISIONS
    )

    critical = {row["label"]: row["decision"] for row in data["critical_label_dispositions"]}
    checks["critical_count"] = len(critical) == 10
    checks["critical_unique"] = len(critical) == len(
        data["critical_label_dispositions"]
    )
    for label, expected in critical.items():
        latest = [
            row
            for row in rows
            if row["label"] == label and row["version"] == "v1.0.13"
        ]
        checks[f"critical_{label}"] = (
            len(latest) == 1 and latest[0]["decision"] == expected
        )

    expected_verdict = (
        "ALL_323_THEORY_EQUATION_OCCURRENCES_ARE_DISPOSED_WITH_"
        "LATEST_CORRECTIONS_NOT_MISTAKEN_FOR_EXTERNAL_VALIDATION"
    )
    checks["verdict"] = data["verdict"] == expected_verdict

    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "check_count": len(checks),
        "failures": failures,
        "gate": (
            "PASS_P058_THEORY_CLAIM_DISPOSITIONS"
            if not failures
            else "FAIL_P058_THEORY_CLAIM_DISPOSITIONS"
        ),
        "equation_occurrence_count": len(rows),
        "unique_equation_label_count": len({row["label"] for row in rows}),
        "decision_counts": data["decision_counts"],
        "assignment_sha256": data["coverage"]["assignment_sha256"],
        "verdict": data["verdict"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
