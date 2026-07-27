#!/usr/bin/env python3
"""Validate R1-withdrawal consistency across v1.0.12 artifacts."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "Codex/results/PHASE_058_R1_WITHDRAWAL_CONSISTENCY_MATRIX.json"
CODE = ROOT / "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py"
THEORY = ROOT / "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex"
SAMPLE = ROOT / "Claude/docs/v1.0.12/sample_test_v1012.py"
REGRESSION = ROOT / "Claude/docs/v1.0.12/test_regression_graphite.py"
GENEALOGY = ROOT / "Codex/results/PHASE_058_ARTIFACT_GENEALOGY.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module():
    sys.dont_write_bytecode = True
    specification = importlib.util.spec_from_file_location(
        "phase058_v1012_r1_probe", CODE
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(CODE)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def local_maximum_count(values: np.ndarray) -> int:
    return sum(
        1
        for index in range(1, len(values) - 1)
        if values[index] > values[index - 1]
        and values[index] >= values[index + 1]
        and values[index] > 0.3
    )


def assert_count(path: Path) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def main() -> int:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    theory = THEORY.read_text(encoding="utf-8")
    sample = SAMPLE.read_text(encoding="utf-8")
    regression = REGRESSION.read_text(encoding="utf-8")
    genealogy = json.loads(GENEALOGY.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["schema"] = (
        data["schema_version"] == "phase058-r1-withdrawal-consistency-v1"
    )
    checks["boundary"] = (
        data["audit_boundary"] == "CROSS_ARTIFACT_CONSISTENCY_NOT_THEORY_CANON"
    )
    facet_ids = [facet["id"] for facet in data["facets"]]
    checks["facet_count"] = len(facet_ids) == data["summary"]["facet_count"]
    checks["facet_ids_unique"] = len(facet_ids) == len(set(facet_ids))

    allowed_decisions = {
        "PRESERVE",
        "CORRECT",
        "SUPERSEDE",
        "EMPIRICAL_ONLY",
        "THEORY_ONLY",
        "REJECT",
        "UNVERIFIED",
    }
    checks["facet_decisions_allowed"] = all(
        facet["decision"] in allowed_decisions for facet in data["facets"]
    )

    module = load_module()
    voltage = np.linspace(0.03, 0.34, 1400)
    default_model = module.GraphiteAnodeDischargeDQDV(
        module.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0
    )
    fitted_transitions = [dict(item, n=0.12) for item in module.GRAPHITE_STAGING_LIT]
    fitted_model = module.GraphiteAnodeDischargeDQDV(
        fitted_transitions, x=0.5, Rn=0.0, Cbg=0.0
    )
    default_curve = np.asarray(
        default_model.dqdv(voltage, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1)
    )
    fitted_curve = np.asarray(
        fitted_model.dqdv(voltage, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1)
    )
    default_i0 = np.asarray(
        default_model.dqdv(voltage, T=298.15, I_abs=0.0, Q_cell=1.0, s=+1)
    )
    default_i1 = np.asarray(
        default_model.dqdv(voltage, T=298.15, I_abs=1.0, Q_cell=1.0, s=+1)
    )
    default_width = float(module.func_w(298.15, 1.0))
    fitted_width = float(module.func_w(298.15, 0.12))
    default_peaks = local_maximum_count(default_curve)
    fitted_peaks = local_maximum_count(fitted_curve)
    current_difference = float(np.max(np.abs(default_i0 - default_i1)))

    numeric = data["numeric_probe"]
    checks["default_width"] = np.isclose(
        default_width, numeric["default_width_v"], rtol=0.0, atol=1e-15
    )
    checks["fitted_width"] = np.isclose(
        fitted_width, numeric["fitted_width_v"], rtol=0.0, atol=1e-15
    )
    checks["default_peak_count"] = (
        default_peaks == numeric["default_local_maximum_count"]
    )
    checks["fitted_peak_count"] = (
        fitted_peaks == numeric["fitted_local_maximum_count"]
    )
    checks["default_current_invariant"] = (
        current_difference
        == numeric["default_current_shape_change_rn0_i0_to_i1"]
        == 0.0
    )
    checks["all_default_n_one"] = all(
        item.get("n") == numeric["default_n"]
        for item in module.GRAPHITE_STAGING_LIT
    )
    checks["stored_w_shadowed"] = all(
        "_n_factor" in dir(default_model)
        and np.isclose(
            default_model._width(item, 298.15),
            module.func_w(298.15, item["n"]),
        )
        for item in module.GRAPHITE_STAGING_LIT
        if "w" in item and "n" in item
    )

    sample_asserts = assert_count(SAMPLE)
    regression_asserts = assert_count(REGRESSION)
    test_probe = data["test_probe"]
    checks["sample_assert_count"] = (
        sample_asserts == test_probe["sample_assert_statement_count"]
    )
    checks["regression_assert_count"] = (
        regression_asserts == test_probe["regression_assert_statement_count"]
    )
    checks["sample_report_only"] = (
        "report only; no physics assertion" in sample
        and "sys.exit" not in sample
        and test_probe["sample_peak_count_is_failure_gate"] is False
    )
    checks["regression_old_code_literal"] = (
        test_probe["regression_code_literal"] in regression
    )

    checks["theory_has_ensemble_integral"] = (
        "\\rho(U_\\app)" in theory and "\\label{eq:ensavg}" in theory
    )
    checks["code_lacks_explicit_rho"] = "rho" not in CODE.read_text(encoding="utf-8")
    checks["theory_says_lag_not_in_width"] = (
        "w_j$ 에 다시 넣지 않는다" in theory
    )
    checks["theory_keybox_says_all_three_in_width"] = (
        "셋을 한꺼번에 흡수하는 것이 \\emph{현상학적 자유 피팅 폭}" in theory
    )
    checks["sample_labels_default_and_fitted"] = (
        "default n=1 (broad, merged bell)" in sample
        and "fitted n=0.12 (4 staging resolved)" in sample
    )

    artifact = next(
        item
        for item in genealogy["artifacts"]
        if item["path"] == data["artifact_probe"]["path"]
    )
    generator = next(
        item
        for item in artifact["sources"]
        if item["path"] == data["artifact_probe"]["generator"]
    )
    checks["artifact_hash"] = (
        sha256(ROOT / artifact["path"])
        == artifact["sha256"]
        == data["artifact_probe"]["artifact_sha256"]
    )
    checks["generator_hash"] = (
        sha256(ROOT / generator["path"])
        == data["artifact_probe"]["generator_sha256"]
    )
    checks["artifact_same_commit"] = (
        generator["relation_to_artifact_commit"]
        == data["artifact_probe"]["commit_relation"]
        == "SAME_COMMIT"
    )

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "matrix": str(MATRIX.relative_to(ROOT)),
                "check_count": len(checks),
                "failures": failures,
                "default_width_v": default_width,
                "fitted_width_v": fitted_width,
                "default_peak_count": default_peaks,
                "fitted_peak_count": fitted_peaks,
                "default_i0_i1_max_difference": current_difference,
                "sample_assert_count": sample_asserts,
                "regression_assert_count": regression_asserts,
                "gate": (
                    "PASS_P058_R1_CROSS_ARTIFACT_ADJUDICATION"
                    if not failures
                    else "FAIL_P058_R1_CROSS_ARTIFACT_ADJUDICATION"
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
