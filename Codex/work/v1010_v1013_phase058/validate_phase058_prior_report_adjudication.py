#!/usr/bin/env python3
"""Validate the Phase 058 v1.0.10 prior-report adjudication matrix."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "Codex/results/PHASE_058_V1010_PRIOR_REPORT_ADJUDICATION.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["schema"] = (
        data["schema_version"] == "phase058-v1010-prior-report-adjudication-v1"
    )
    checks["audit_boundary"] = (
        data["audit_boundary"] == "HISTORICAL_AUDIT_NOT_THEORY_CANON"
    )

    for source in data["sources"]:
        path = ROOT / source["path"]
        checks[f"source_exists:{source['path']}"] = path.is_file()
        checks[f"source_hash:{source['path']}"] = (
            path.is_file() and sha256(path) == source["sha256"]
        )

    claims = data["claims"]
    ids = [claim["id"] for claim in claims]
    checks["claim_ids_unique"] = len(ids) == len(set(ids))
    checks["claim_count"] = len(claims) == data["summary"]["claim_count"]
    checks["all_statuses_allowed"] = all(
        claim["status"] in data["allowed_statuses"] for claim in claims
    )
    checks["all_claims_have_reason"] = all(
        bool(claim["reason"].strip()) for claim in claims
    )
    checks["all_claims_have_carry_forward"] = all(
        bool(claim["carry_forward"].strip()) for claim in claims
    )

    counts = Counter(claim["status"].lower() for claim in claims)
    for status in ("confirmed", "partial", "rejected", "unresolved"):
        checks[f"summary_count:{status}"] = (
            counts[status] == data["summary"][status]
        )

    for evidence in data["evidence_files"]:
        checks[f"evidence_exists:{evidence}"] = (ROOT / evidence).is_file()

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "matrix": str(MATRIX.relative_to(ROOT)),
                "claim_count": len(claims),
                "counts": dict(sorted(counts.items())),
                "check_count": len(checks),
                "failures": failures,
                "gate": (
                    "PASS_P058_V1010_PRIOR_REPORT_ADJUDICATION"
                    if not failures
                    else "FAIL_P058_V1010_PRIOR_REPORT_ADJUDICATION"
                ),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
