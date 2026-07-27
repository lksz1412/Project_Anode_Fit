#!/usr/bin/env python3
"""Assign every Phase 058 equation occurrence a canonical disposition."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "Codex/results/PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json"

ALLOWED_DECISIONS = {
    "PRESERVE",
    "CORRECT",
    "SUPERSEDE",
    "EMPIRICAL_ONLY",
    "THEORY_ONLY",
    "REJECT",
    "UNVERIFIED",
}

CATEGORY_DEFAULTS = {
    "coordinate_and_conservation": "PRESERVE",
    "equilibrium_and_statistical_mechanics": "PRESERVE",
    "hysteresis_and_kinetics": "EMPIRICAL_ONLY",
    "lco_extension": "UNVERIFIED",
    "observation_and_fitting": "THEORY_ONLY",
    "peak_kernel_and_broadening": "PRESERVE",
    "thermal_and_entropy": "THEORY_ONLY",
}

LABEL_OVERRIDES = {
    "eq:Acut": "EMPIRICAL_ONLY",
    "eq:Lq": "THEORY_ONLY",
    "eq:Lqmid": "THEORY_ONLY",
    "eq:LV": "THEORY_ONLY",
    "eq:Sconfig": "PRESERVE",
    "eq:Se": "PRESERVE",
    "eq:Sedirect": "PRESERVE",
    "eq:Svib_mode": "PRESERVE",
    "eq:U1T2": "PRESERVE",
    "eq:Uj": "PRESERVE",
    "eq:Ujmid": "PRESERVE",
    "eq:branch": "REJECT",
    "eq:bv": "THEORY_ONLY",
    "eq:dSegate": "EMPIRICAL_ONLY",
    "eq:dSconfig": "PRESERVE",
    "eq:dSemolar": "PRESERVE",
    "eq:dSe": "PRESERVE",
    "eq:dUhys": "CORRECT",
    "eq:db": "THEORY_ONLY",
    "eq:dVdT_config": "PRESERVE",
    "eq:dxidT": "CORRECT",
    "eq:ensavg": "THEORY_ONLY",
    "eq:eqpeak": "PRESERVE",
    "eq:fd": "PRESERVE",
    "eq:ggate": "EMPIRICAL_ONLY",
    "eq:gunit": "PRESERVE",
    "eq:gj": "PRESERVE",
    "eq:hys_branch": "THEORY_ONLY",
    "eq:hys_rev": "THEORY_ONLY",
    "eq:hysdiff": "CORRECT",
    "eq:hyssub": "CORRECT",
    "eq:hyssym": "CORRECT",
    "eq:implicit": "CORRECT",
    "eq:implicit_diff": "CORRECT",
    "eq:intfactor": "PRESERVE",
    "eq:kuniv": "THEORY_ONLY",
    "eq:lco-J": "UNVERIFIED",
    "eq:lco-Sadd": "THEORY_ONLY",
    "eq:lco-SeV": "EMPIRICAL_ONLY",
    "eq:lco-U1V": "THEORY_ONLY",
    "eq:lco-Ubranch": "EMPIRICAL_ONLY",
    "eq:lco-Veq": "THEORY_ONLY",
    "eq:lco-Zfact": "THEORY_ONLY",
    "eq:lco-charge": "UNVERIFIED",
    "eq:lco-comp": "PRESERVE",
    "eq:lco-configsplit": "CORRECT",
    "eq:lco-decomp": "THEORY_ONLY",
    "eq:lco-dUdT": "PRESERVE",
    "eq:lco-dUhys": "CORRECT",
    "eq:lco-dope": "UNVERIFIED",
    "eq:lco-eqpeak": "UNVERIFIED",
    "eq:lco-gpp": "THEORY_ONLY",
    "eq:lco-gxi": "THEORY_ONLY",
    "eq:lco-mit": "UNVERIFIED",
    "eq:lco-msmrmap": "CORRECT",
    "eq:lco-msmrnorm": "PRESERVE",
    "eq:lco-msmrpeak": "CORRECT",
    "eq:lco-n0sub": "UNVERIFIED",
    "eq:lco-peakobs": "UNVERIFIED",
    "eq:lco-plugin": "THEORY_ONLY",
    "eq:lco-sigmaslot": "PRESERVE",
    "eq:lco-slots": "CORRECT",
    "eq:lco-spinodal": "THEORY_ONLY",
    "eq:lco-xmap": "EMPIRICAL_ONLY",
    "eq:lowpass": "THEORY_ONLY",
    "eq:memory": "THEORY_ONLY",
    "eq:msmr": "PRESERVE",
    "eq:n0map": "REJECT",
    "eq:peakshape": "THEORY_ONLY",
    "eq:qrev": "PRESERVE",
    "eq:reversal": "THEORY_ONLY",
    "eq:single_config": "CORRECT",
    "eq:sm-Smix": "PRESERVE",
    "eq:sm-factor": "PRESERVE",
    "eq:sm-mucount": "PRESERVE",
    "eq:sm-muideal": "PRESERVE",
    "eq:sm-resv": "PRESERVE",
    "eq:sm-taylor": "PRESERVE",
    "eq:sum": "CORRECT",
    "eq:vwork": "EMPIRICAL_ONLY",
    "eq:wbase": "EMPIRICAL_ONLY",
    "eq:weighted": "CORRECT",
    "eq:xieq": "CORRECT",
}

V1010_SUPERSEDED_BY_V1012 = {
    "eq:Veq_BW",
    "eq:lco-dUdT",
    "eq:lco-decomp",
    "eq:slope_BW",
}

PRE_V1013_SUPERSEDED_BY_V1013 = {
    "eq:Acut",
    "eq:U1T2",
    "eq:dxidT",
    "eq:fermifn",
    "eq:ggate",
    "eq:gj",
    "eq:implicit",
    "eq:lco-U1V",
    "eq:lco-configsplit",
    "eq:lco-peakobs",
    "eq:lco-plugin",
    "eq:lco-slots",
    "eq:muV",
    "eq:partfn",
    "eq:single_config",
}


def disposition(version: str, category: str, label: str) -> str:
    if version == "v1.0.10" and label in V1010_SUPERSEDED_BY_V1012:
        return "SUPERSEDE"
    if version in {"v1.0.10", "v1.0.12"} and label in PRE_V1013_SUPERSEDED_BY_V1013:
        return "SUPERSEDE"
    return LABEL_OVERRIDES.get(label, CATEGORY_DEFAULTS[category])


def assignments() -> list[dict[str, str]]:
    source = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = []
    for equation in source["equations"]:
        label = equation["labels"][0]
        decision = disposition(equation["version"], equation["category"], label)
        rows.append(
            {
                "equation_id": equation["equation_id"],
                "version": equation["version"],
                "category": equation["category"],
                "label": label,
                "decision": decision,
            }
        )
    return rows


def main() -> None:
    rows = assignments()
    serialized = "\n".join(
        f"{row['equation_id']}|{row['decision']}" for row in rows
    ).encode("utf-8")
    result = {
        "equation_occurrence_count": len(rows),
        "unique_equation_label_count": len({row["label"] for row in rows}),
        "decision_counts": dict(sorted(Counter(row["decision"] for row in rows).items())),
        "version_decision_counts": {
            version: dict(
                sorted(
                    Counter(
                        row["decision"] for row in rows if row["version"] == version
                    ).items()
                )
            )
            for version in ("v1.0.10", "v1.0.12", "v1.0.13")
        },
        "category_decision_counts": {
            category: dict(
                sorted(
                    Counter(
                        row["decision"] for row in rows if row["category"] == category
                    ).items()
                )
            )
            for category in sorted(CATEGORY_DEFAULTS)
        },
        "assignment_sha256": hashlib.sha256(serialized).hexdigest(),
        "invalid_decisions": sorted(
            {row["decision"] for row in rows} - ALLOWED_DECISIONS
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
