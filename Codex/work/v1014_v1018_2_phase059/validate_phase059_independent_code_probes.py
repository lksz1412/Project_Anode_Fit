#!/usr/bin/env python3
"""Validate Phase 059 Step 34.4 independent probe evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
OUTPUT = RESULTS / "PHASE_059_INDEPENDENT_CODE_PROBES.json"
REVIEW = RESULTS / "PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md"
RUNNER = (
    ROOT
    / "Codex"
    / "work"
    / "v1014_v1018_2_phase059"
    / "run_phase059_independent_code_probes.py"
)

EXPECTED_IDS = [
    "MEM-001",
    "MEM-002",
    "MEM-003",
    "ORD-001",
    "ORD-002",
    "CUR-001",
    "CUR-002",
    "UNT-001",
    "WID-001",
    "WID-002",
    "WID-003",
    "WID-004",
    "WID-005",
    "WID-006",
    "VIB-001",
    "VIB-002",
    "VIB-003",
    "VIB-004",
    "LCO-001",
    "LCO-002",
    "LCO-003",
    "KIN-001",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks: list[tuple[str, bool]] = []
    checks.append(("result exists", OUTPUT.is_file()))
    checks.append(("review exists", REVIEW.is_file()))
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    probes = payload["probes"]
    by_id = {item["probe_id"]: item for item in probes}

    checks.append(
        (
            "status conditional",
            payload["status"] == "CONDITIONAL_P059_CODE_CONFORMANCE",
        )
    )
    checks.append(
        (
            "execution gate exact",
            payload["execution_gate"]
            == "PASS_P059_INDEPENDENT_CODE_PROBE_EXECUTION",
        )
    )
    checks.append(("source unchanged", payload["sources_unchanged"] is True))
    checks.append(
        (
            "source hashes stable",
            payload["source_sha256_before"] == payload["source_sha256_after"],
        )
    )
    checks.append(
        (
            "source hashes current",
            all(
                digest == sha256(ROOT / relative)
                for relative, digest in payload["source_sha256_after"].items()
            ),
        )
    )
    checks.append(("probe count", payload["probe_count"] == len(probes) == 22))
    checks.append(
        (
            "probe ids exact and ordered",
            [item["probe_id"] for item in probes] == EXPECTED_IDS,
        )
    )
    checks.append(("probe ids unique", len(by_id) == len(probes)))
    checks.append(
        (
            "verdict counts exact",
            payload["verdict_counts"]
            == {
                "BLOCKER_CONFIRMED": 8,
                "IDENTIFIABILITY_CAUTION": 1,
                "PASS_GUARD": 1,
                "PASS_IDENTITY": 10,
                "SCOPE_ABSENT_CONFIRMED": 2,
            },
        )
    )

    lineage = payload["feature_lineage"]
    checks.append(
        (
            "feature versions exact",
            [item["version"] for item in lineage]
            == ["v1.0.14", "v1.0.15", "v1.0.16", "v1.0.18.2"],
        )
    )
    checks.append(
        (
            "pointwise onset v1015",
            [item["has_pointwise_memory"] for item in lineage]
            == [False, True, True, True],
        )
    )
    checks.append(
        (
            "grid lowpass retired v1015",
            [item["has_grid_lowpass"] for item in lineage]
            == [True, False, False, False],
        )
    )
    checks.append(
        (
            "dwdT onset v1016",
            [item["has_dwdT"] for item in lineage]
            == [False, False, True, True],
        )
    )
    checks.append(
        (
            "vibration onset v1018_2",
            [item["has_vib_theta"] for item in lineage]
            == [False, False, False, True]
            and [item["has_vib_entropy"] for item in lineage]
            == [False, False, False, True],
        )
    )

    mem1 = by_id["MEM-001"]["measurements"]
    checks.append(
        (
            "memory recurrence exact",
            mem1["constant_source_max_abs_error"] < 1e-12
            and mem1["linear_source_max_abs_error"] < 1e-12,
        )
    )
    mem2 = by_id["MEM-002"]["measurements"]
    checks.append(
        (
            "memory capacity conserved",
            abs(mem2["equilibrium_area"] - 1.0) < 1e-8
            and abs(mem2["lagged_area"] - 1.0) < 1e-8,
        )
    )
    checks.append(
        (
            "memory suppresses and broadens",
            mem2["lagged_peak"] < mem2["equilibrium_peak"]
            and mem2["lagged_fwhm_V"] > mem2["equilibrium_fwhm_V"],
        )
    )
    mem3 = by_id["MEM-003"]["measurements"]
    checks.append(
        (
            "small LV converges",
            mem3["difference_strictly_decreases"] is True
            and all(abs(item["area"] - 1.0) < 1e-8 for item in mem3["sweep"]),
        )
    )
    checks.append(
        (
            "direction mirror exact",
            by_id["ORD-001"]["measurements"]["mirror_max_abs_error"] < 1e-12,
        )
    )
    order = by_id["ORD-002"]["measurements"]
    checks.append(
        (
            "chronology blocker reproduced",
            order["sorted_vs_shuffled_then_restored_max_abs"] == 0.0
            and order["model_shuffled_vs_true_input_order_memory_max_abs"] > 1.0,
        )
    )
    checks.append(
        (
            "derived I0 limit exact",
            by_id["CUR-001"]["measurements"]["I0_vs_equilibrium_max_abs"] == 0.0
            and by_id["CUR-001"]["measurements"]["resolved_lag_lengths_V"]["0.0"]
            == 0.0,
        )
    )
    direct = by_id["CUR-002"]["measurements"]
    checks.append(
        (
            "direct LV blocker reproduced",
            direct["I0_vs_I1_max_abs"] == 0.0
            and direct["I0_vs_equilibrium_max_abs"] > 1.0,
        )
    )
    units = by_id["UNT-001"]["measurements"]
    checks.append(
        (
            "factor 3600 reproduced",
            abs(units["func_Lq_code_to_SI_ratio"] - 3600.0) < 1e-9
            and units["code_implied_current_A"] == 3600.0
            and units["physical_current_A"] == 1.0,
        )
    )
    checks.append(
        (
            "constant n derivative exact",
            by_id["WID-001"]["measurements"]["abs_error"] < 1e-12,
        )
    )
    width_n_t = by_id["WID-002"]["measurements"]
    checks.append(
        (
            "nT width entropy chain exact",
            width_n_t["width_abs_error"] < 1e-10
            and width_n_t["entropy_abs_error"] < 1e-10,
        )
    )
    width_w = by_id["WID-003"]["measurements"]
    checks.append(
        (
            "w only frozen",
            abs(width_w["finite_difference_V_per_K"]) < 1e-12
            and width_w["code_dwdT_V_per_K"] == 0.0
            and width_w["width_258K_V"] == width_w["width_318K_V"],
        )
    )
    width_default = by_id["WID-004"]["measurements"]
    checks.append(
        (
            "default derivative mismatch reproduced",
            abs(
                width_default["finite_difference_V_per_K"]
                - width_default["expected_R_over_F"]
            )
            < 1e-12
            and width_default["code_dwdT_V_per_K"] == 0.0,
        )
    )
    checks.append(
        (
            "width positivity guard",
            by_id["WID-005"]["measurements"]["exception"].startswith(
                "ValueError:"
            ),
        )
    )
    checks.append(
        (
            "n shadows w",
            by_id["WID-006"]["measurements"]["curve_max_abs_difference"] == 0.0,
        )
    )

    vib_derivative = by_id["VIB-001"]["measurements"]
    checks.append(
        (
            "vibration derivative identity",
            vib_derivative["max_abs_error"] < 1e-10
            and vib_derivative["DeltaU_at_reference_V"] == -0.0
            and vib_derivative["DeltaS_at_reference_J_per_molK"] == 0.0,
        )
    )
    vib_thermo = by_id["VIB-002"]["measurements"]
    checks.append(
        (
            "vibration thermodynamic identities",
            vib_thermo["max_U_identity_abs_error_J_per_mol"] < 1e-8
            and vib_thermo["low_T_entropy_J_per_molK"] < 1e-10
            and vib_thermo["high_T_relative_error"] < 1e-6
            and all(row["all_finite"] for row in vib_thermo["rows"]),
        )
    )
    invalid_refs = by_id["VIB-003"]["measurements"]["cases"]
    checks.append(
        (
            "invalid reference blocker",
            all(
                row["exception"] is None
                and row["returned_finite"] is False
                and row["returned_is_nan"] is True
                and row["returned_value_repr"] == "nan"
                for row in invalid_refs
            ),
        )
    )
    checks.append(
        (
            "vibration defaults dormant",
            by_id["VIB-004"]["measurements"]["theta_E_key_count"] == 0
            and by_id["VIB-004"]["measurements"]["theta_E_Tref_key_count"] == 0,
        )
    )
    checks.append(
        (
            "LCO electronic entropy frozen",
            by_id["LCO-001"]["measurements"]["range_J_per_molK"] == 0.0,
        )
    )
    lco_rate = by_id["LCO-002"]["measurements"]
    checks.append(
        (
            "LCO default rate invariant",
            lco_rate["I0_vs_I1_Rn0_max_abs"] == 0.0
            and lco_rate["all_transitions_missing_dH_a"] is True
            and lco_rate["all_transitions_missing_L_V"] is True,
        )
    )
    lco_scope = by_id["LCO-003"]["measurements"]
    checks.append(
        (
            "high voltage doped LCO absent",
            lco_scope["maximum_literal_U_V"] == 4.05
            and lco_scope["recognized_dopant_or_degradation_keys"] == [],
        )
    )
    kinetics = by_id["KIN-001"]["measurements"]
    checks.append(
        (
            "local barrier state absent",
            kinetics["voltage_or_affinity_parameter_present"] is False
            and kinetics["absolute_difference_V"] == 0.0,
        )
    )

    review_text = REVIEW.read_text(encoding="utf-8")
    checks.append(
        (
            "review authority boundary",
            "BLOCKER_CONFIRMED`를 과학적 PASS로 세지 않는다" in review_text
            and "실험 적합성도 부여하지 않는다" in review_text,
        )
    )
    checks.append(
        (
            "review next step",
            "다음 Step 34.5" in review_text
            and payload["next_step"] == "34.5",
        )
    )

    before = (sha256(OUTPUT), sha256(REVIEW))
    completed = subprocess.run(
        [sys.executable, "-W", "error::SyntaxWarning", str(RUNNER)],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    after = (sha256(OUTPUT), sha256(REVIEW))
    checks.append(("runner rerun exits zero", completed.returncode == 0))
    checks.append(("result and review deterministic", before == after))
    checks.append(
        (
            "runner rerun clean stderr",
            completed.stderr == "",
        )
    )
    claude_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "Claude"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout
    checks.append(("Claude tree untouched", claude_status == ""))

    failures = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    if failures:
        raise SystemExit(
            "FAIL_P059_INDEPENDENT_CODE_PROBES: " + ", ".join(failures)
        )
    print(f"PASS_P059_INDEPENDENT_CODE_PROBES {len(checks)}/{len(checks)}")


if __name__ == "__main__":
    main()
