#!/usr/bin/env python3
"""Validate Phase 058 carry-forward and blocker routing."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_058_CARRY_FORWARD_BLOCKER_REGISTER.json"
FOUR_AXIS = ROOT / "Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_MATRIX.json"


def main() -> int:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    four_axis = json.loads(FOUR_AXIS.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    groups = {
        "CF": data["carry_forward_assets"],
        "RB": data["repair_blockers"],
        "NS": data["new_scope_blockers"],
        "ED": data["evidence_debts"],
    }
    expected_counts = {"CF": 11, "RB": 13, "NS": 5, "ED": 5}

    all_ids: list[str] = []
    for prefix, rows in groups.items():
        checks[f"{prefix}_count"] = len(rows) == expected_counts[prefix]
        checks[f"{prefix}_ids"] = [row["id"] for row in rows] == [
            f"{prefix}-{number:02d}" for number in range(1, len(rows) + 1)
        ]
        checks[f"{prefix}_topics"] = len({row["topic"] for row in rows}) == len(rows)
        all_ids.extend(row["id"] for row in rows)
    checks["all_register_ids_unique"] = len(all_ids) == len(set(all_ids))
    checks["total_count"] = len(all_ids) == data["counts"]["total_register_item_count"]
    checks["stored_cf_count"] = (
        data["counts"]["carry_forward_asset_count"] == expected_counts["CF"]
    )
    checks["stored_rb_count"] = (
        data["counts"]["repair_blocker_count"] == expected_counts["RB"]
    )
    checks["stored_ns_count"] = (
        data["counts"]["new_scope_blocker_count"] == expected_counts["NS"]
    )
    checks["stored_ed_count"] = (
        data["counts"]["evidence_debt_count"] == expected_counts["ED"]
    )

    routes = data["four_axis_routes"]
    source_rows = [row["id"] for row in four_axis["rows"]]
    checks["route_count"] = len(routes) == data["counts"]["four_axis_route_count"]
    checks["route_rows_unique"] = len({row["row"] for row in routes}) == len(routes)
    checks["route_complete"] = [row["row"] for row in routes] == source_rows
    checks["route_targets_exist"] = all(row["route"] in all_ids for row in routes)

    checks["all_repair_acceptance"] = all(
        bool(row["acceptance"].strip()) for row in data["repair_blockers"]
    )
    checks["blocking_repair_exists"] = any(
        row["severity"] == "BLOCKING" for row in data["repair_blockers"]
    )
    checks["all_assets_reach_later_phase"] = all(
        all(59 <= phase <= 69 for phase in row["target_phases"])
        for row in data["carry_forward_assets"]
    )
    checks["all_repairs_reach_later_phase"] = all(
        all(59 <= phase <= 69 for phase in row["target_phases"])
        for row in data["repair_blockers"]
    )
    checks["new_scope_deferred_to_synthesis"] = all(
        row["target_phase"] == 69 for row in data["new_scope_blockers"]
    )
    checks["no_v1026_authority"] = "v1.0.26" not in json.dumps(data)

    expected_verdict = (
        "PHASE058_ASSETS_ARE_ROUTED_WITH_13_REPAIR_BLOCKERS_"
        "5_NEW_SCOPE_BLOCKERS_AND_5_EVIDENCE_DEBTS"
    )
    checks["verdict"] = data["verdict"] == expected_verdict

    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "check_count": len(checks),
        "failures": failures,
        "gate": (
            "PASS_P058_CARRY_FORWARD_ROUTING"
            if not failures
            else "FAIL_P058_CARRY_FORWARD_ROUTING"
        ),
        "counts": data["counts"],
        "verdict": data["verdict"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
