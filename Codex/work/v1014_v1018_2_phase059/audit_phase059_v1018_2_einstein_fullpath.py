#!/usr/bin/env python3
"""Phase 059 Step 38.4: Einstein optional/full-path implementation audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
P181 = ROOT / "Claude/docs/v1.0.18.1/Anode_Fit_v1.0.18.1.py"
P182 = ROOT / "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py"
OUT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def maxdiff(a, b) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def main() -> None:
    m181, m182 = load(P181, "anodefit181"), load(P182, "anodefit182")
    base = {
        "dH_rxn": -13000.0, "dS_rxn": -16.0, "n": 1.0, "Q": 1.0,
        "Omega": 0.0, "gamma": 0.0, "L_V": 0.0,
    }
    active = dict(base, theta_E=700.0, theta_E_Tref=298.15)
    V = np.linspace(0.0, 0.20, 4001)
    Tcurve = np.linspace(278.15, 338.15, V.size)
    a181, a182 = m181.GraphiteAnodeDischargeDQDV([base]), m182.GraphiteAnodeDischargeDQDV([base])

    absent = {
        "equilibrium_max_abs": maxdiff(a181.equilibrium(V, 318.15), a182.equilibrium(V, 318.15)),
        "dqdv_isothermal_max_abs": maxdiff(
            a181.dqdv(V, 318.15, 0.2, 1.0, +1),
            a182.dqdv(V, 318.15, 0.2, 1.0, +1),
        ),
        "dqdv_nonisothermal_max_abs": maxdiff(
            a181.dqdv(V, Tcurve, 0.2, 1.0, +1),
            a182.dqdv(V, Tcurve, 0.2, 1.0, +1),
        ),
        "entropy_max_abs": maxdiff(a181.entropy_coefficient(V, 318.15), a182.entropy_coefficient(V, 318.15)),
        "heat_max_abs": maxdiff(a181.reversible_heat(V, 318.15, 1.0), a182.reversible_heat(V, 318.15, 1.0)),
    }

    model = m182.GraphiteAnodeDischargeDQDV([active])
    tref, theta = 298.15, 700.0
    active_rows = []
    for T in [278.15, 298.15, 318.15, 348.15]:
        center = float(m182.func_U_j(T, active["dH_rxn"], active["dS_rxn"]) + model._vib_dU(active, T))
        eq = np.asarray(model.equilibrium(V, T))
        peak_V = float(V[int(np.argmax(eq))])
        h = 1e-3
        center_fd = (
            float(m182.func_U_j(T + h, active["dH_rxn"], active["dS_rxn"]) + model._vib_dU(active, T + h))
            - float(m182.func_U_j(T - h, active["dH_rxn"], active["dS_rxn"]) + model._vib_dU(active, T - h))
        ) / (2 * h)
        ec_center = float(np.asarray(model.entropy_coefficient(np.array([center]), T))[0])
        qrev_center = float(np.asarray(model.reversible_heat(np.array([center]), T, 1.0))[0])
        active_rows.append({
            "T_K": T,
            "analytic_center_V": center,
            "grid_peak_V": peak_V,
            "grid_peak_error_V": peak_V - center,
            "center_finite_difference_V_per_K": center_fd,
            "entropy_coefficient_at_center_V_per_K": ec_center,
            "fullpath_roundtrip_error_V_per_K": ec_center - center_fd,
            "reversible_heat_at_center_W_per_A": qrev_center,
            "heat_identity_error_W_per_A": qrev_center + T * ec_center,
        })

    # theta_E on U-only transition is accepted by helpers but ignored by public paths.
    u_only_plain = {"U": 0.085, "w": 0.02, "Q": 1.0}
    u_only_theta = dict(u_only_plain, theta_E=700.0)
    up = m182.GraphiteAnodeDischargeDQDV([u_only_plain])
    ut = m182.GraphiteAnodeDischargeDQDV([u_only_theta])
    u_only = {
        "equilibrium_difference": maxdiff(up.equilibrium(V, 318.15), ut.equilibrium(V, 318.15)),
        "entropy_difference": maxdiff(up.entropy_coefficient(V, 318.15), ut.entropy_coefficient(V, 318.15)),
        "helper_vib_dU_nonzero_V": float(ut._vib_dU(u_only_theta, 318.15)),
        "silently_ignored": True,
    }

    boundary = {}
    for value in [0.0, -10.0]:
        tr = dict(active, theta_E_Tref=value)
        probe = m182.GraphiteAnodeDischargeDQDV([tr])
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                result = np.asarray(probe.equilibrium(V[:5], 298.15), dtype=float)
                boundary[str(value)] = {
                    "raised": False,
                    "all_finite": bool(np.all(np.isfinite(result))),
                    "warning_count": len(caught),
                }
            except Exception as exc:
                boundary[str(value)] = {
                    "raised": True, "exception": type(exc).__name__,
                    "message": str(exc), "warning_count": len(caught),
                }

    release_files = [
        ROOT / "Claude/docs/v1.0.18.2/test_regression_graphite.py",
        ROOT / "Claude/docs/v1.0.18.2/sample_test_v1018_2.py",
        ROOT / "Claude/docs/v1.0.18.2/graph_suite_v1018_2.py",
    ]
    coverage = [{
        "path": str(p.relative_to(ROOT)),
        "theta_E_occurrences": p.read_text(encoding="utf-8").count("theta_E"),
        "_vib_occurrences": p.read_text(encoding="utf-8").count("_vib"),
    } for p in release_files]

    max_active_roundtrip = max(abs(x["fullpath_roundtrip_error_V_per_K"]) for x in active_rows)
    max_heat_identity = max(abs(x["heat_identity_error_W_per_A"]) for x in active_rows)
    max_peak_error = max(abs(x["grid_peak_error_V"]) for x in active_rows)
    findings = [
        {"id": "FP-001", "disposition": "PRESERVE", "text": "Without theta_E, equilibrium, isothermal/nonisothermal dQdV, entropy coefficient and reversible heat are exactly equal to v1.0.18.1 for the independent probe."},
        {"id": "FP-002", "disposition": "PRESERVE", "text": "With theta_E active, equilibrium peak centers follow func_U_j plus the tangent-subtracted vibrational voltage."},
        {"id": "FP-003", "disposition": "PRESERVE", "text": "At each active temperature, the finite-difference center derivative equals entropy_coefficient at the center."},
        {"id": "FP-004", "disposition": "PRESERVE", "text": "reversible_heat equals -I*T*entropy_coefficient on the active branch."},
        {"id": "FP-005", "disposition": "PRESERVE", "text": "Nonisothermal dQdV receives pointwise _vib_dU through the same equilibrium-center path."},
        {"id": "FP-006", "disposition": "CORRECT", "text": "theta_E is silently ignored for U-only transitions although the private helper returns a nonzero correction; the public parameter contract is type-unsafe."},
        {"id": "FP-007", "disposition": "CORRECT", "text": "theta_E_Tref is checked only for finiteness, not positivity; zero/negative values do not fail cleanly at the input boundary."},
        {"id": "FP-008", "disposition": "CORRECT", "text": "Released regression, sample and graph-suite files contain zero theta_E and _vib occurrences, so no persistent release test exercises the feature."},
        {"id": "FP-009", "disposition": "CORRECT", "text": "The handover's roundtrip evidence is not recoverable from the distributed regression harness."},
        {"id": "FP-010", "disposition": "CARRY_FORWARD", "text": "The active branch does not fix the LCO frozen electronic gate or the default no-key dwdT defect."},
        {"id": "FP-011", "disposition": "EMPIRICAL_ONLY", "text": "Full-path numerical conformance establishes a capability, not a graphite/LCO material fit."},
        {"id": "FP-012", "disposition": "CORRECT", "text": "A durable test must cover absent-key equality, active scalar/array paths, Tref positivity, U-only rejection, and derivative/heat identities."},
    ]

    data = {
        "schema_version": 1,
        "phase": 59,
        "step": "38.4",
        "status": "CONDITIONAL_P059_V1018_2_EINSTEIN_ABSENT_KEY_AND_ACTIVE_FULLPATH_CONFORMANCE_PASS_BUT_PARAMETER_CONTRACT_AND_PERSISTENT_REGRESSION_FAIL",
        "source_hashes": {
            "v1018_1": hashlib.sha256(P181.read_bytes()).hexdigest(),
            "v1018_2": hashlib.sha256(P182.read_bytes()).hexdigest(),
        },
        "absent_key_comparison": absent,
        "active_branch_rows": active_rows,
        "u_only_transition_probe": u_only,
        "theta_E_Tref_boundary": boundary,
        "release_test_coverage": coverage,
        "validation": {
            "absent_key_all_exact": all(v == 0.0 for v in absent.values()),
            "active_fullpath_roundtrip_max_error_V_per_K": max_active_roundtrip,
            "active_heat_identity_max_error_W_per_A": max_heat_identity,
            "active_peak_grid_max_error_V": max_peak_error,
            "u_only_public_ignore_confirmed": (
                u_only["equilibrium_difference"] == 0.0
                and u_only["entropy_difference"] == 0.0
                and u_only["helper_vib_dU_nonzero_V"] != 0.0
            ),
            "tref_positive_failfast_pass": False,
            "persistent_release_regression_pass": False,
        },
        "findings": findings,
        "summary": {
            "finding_count": len(findings),
            "capability_conformance_pass": True,
            "public_parameter_contract_pass": False,
            "material_validation_pass": False,
            "next_step": "38.5",
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(f"""# Phase 059 v1.0.18.2 Einstein full-path 감사

정본일: 2026-07-28

판정: `{data["status"]}`

## 결론

theta_E가 없을 때 v1.0.18.1과 equilibrium, 등온/비등온 dQdV,
entropy coefficient, reversible heat가 모두 exact 동일했다.
theta_E=700 K 활성 branch도 중심 전위, 중심의 finite-difference
기울기, entropy coefficient와 -I*T*dU/dT 열 항등식이 같은
자유에너지 경로로 닫혔다.

그러나 public parameter contract는 닫히지 않았다. dH_rxn/dS_rxn이
없는 U-only transition에 theta_E를 넣으면 private helper는 nonzero
보정을 계산하지만 equilibrium과 entropy public path는 이를 조용히
무시한다. theta_E_Tref도 finite만 검사하고 양수 조건을 강제하지
않아 0 또는 음수에서 깨끗한 fail-fast가 없다.

배포 test_regression_graphite.py, sample_test, graph_suite에는 theta_E와
_vib 호출이 각각 0건이다. handover의 round-trip은 현재 배포
regression harness에서 재현·보존되는 test authority가 아니다.

따라서 구현 capability의 내부 정합은 보존하지만, 실제 사용 전에는
U-only 조합 reject 또는 명시 의미 부여, Tref>0 guard, absent/active
scalar-array/derivative/heat 회귀시험이 필요하다. 이 결과도 material
fit validation은 아니다.

## 다음 단계

Step 38.5에서 ROADMAP_future_physics의 항목을 implemented,
theory-only, new-scope와 data prerequisite로 전건 분류한다.

원본 `Claude/`, `main`은 수정하지 않았다.
""", encoding="utf-8")
    print(data["status"])
    print("absent_exact", data["validation"]["absent_key_all_exact"], "roundtrip", max_active_roundtrip)


if __name__ == "__main__":
    main()
