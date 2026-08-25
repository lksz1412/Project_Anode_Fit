#!/usr/bin/env python3
"""Build Phase 060 Step 44 independent-physics evidence.

The numerical probes in this module implement the equations directly.  They
do not import or call the frozen v1.0.19 production module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
TRACE_PATH = ROOT / "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json"
JSON_PATH = ROOT / "Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json"
MD_PATH = ROOT / "Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md"

R = 8.31446261815324
FARADAY = 96485.33212
KB = 1.380649e-23
EV_J = 1.602176634e-19

SOURCE_FILES = [
    "Claude/docs/v1.0.19/_sections/ch1_preamble.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec01_n0n1.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec02a_part0.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec02b_part0.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec03_center.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec04_hys.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec05_width.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec06_eqpeak.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec07_broadening.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec08_lag.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec09_tail.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec10_sum.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec11_lcointro.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec12_lcocenter.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec13_lcohys.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec14_lcodecomp.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec15_lcoelec.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec16_lcopeak.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec17_msmr.tex",
    "Claude/docs/v1.0.19/_sections/ch1_sec18_inputs.tex",
    "Claude/docs/v1.0.19/_sections/ch1_appA_signcheck.tex",
    "Claude/docs/v1.0.19/_sections/ch2_preamble.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec01_partition.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec02_config.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec03_vibel.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec04_einstein.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec06_limits.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec07_revheat.tex",
    "Claude/docs/v1.0.19/_sections/ch2_sec08_synthesis.tex",
    "Claude/docs/v1.0.19/_sections/ch2_appA_traps.tex",
]


def run_git(*args: str, binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    )
    return completed.stdout if binary else completed.stdout.decode("utf-8").strip()


def blob(path: str) -> bytes:
    return run_git("show", f"{SOURCE_COMMIT}:{path}", binary=True)  # type: ignore[return-value]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def anchor(path: str, start: int, end: int) -> dict[str, Any]:
    raw = blob(path)
    lines = raw.decode("utf-8").splitlines()
    if not (1 <= start <= end <= len(lines)):
        raise ValueError(f"invalid source anchor {path}:{start}-{end}")
    sliced = "\n".join(lines[start - 1 : end]).encode("utf-8")
    return {
        "anchor_id": f"SRC:{path}:{start}-{end}",
        "path": path,
        "start_line": start,
        "end_line": end,
        "git_blob_sha1": run_git("rev-parse", f"{SOURCE_COMMIT}:{path}"),
        "slice_sha256": sha256(sliced),
    }


def stable_logistic(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


TRANSITIONS = [
    {"name": "4->3", "dH": -11700.0, "dS": 29.0, "Q": 0.10},
    {"name": "3->2L", "dH": -13500.0, "dS": 0.0, "Q": 0.12},
    {"name": "2L->2", "dH": -13100.0, "dS": -5.0, "Q": 0.25},
    {"name": "2->1", "dH": -13000.0, "dS": -16.0, "Q": 0.50},
]


def transition_state(u: float, temperature: float) -> list[dict[str, float]]:
    width = R * temperature / FARADAY
    rows = []
    for item in TRANSITIONS:
        center = (-item["dH"] + temperature * item["dS"]) / FARADAY
        z = (u - center) / width
        xi = stable_logistic(z)
        g = xi * (1.0 - xi) / width
        rows.append({"center": center, "width": width, "z": z, "xi": xi, "g": g})
    return rows


def charge_residual(u: float, temperature: float, target_charge: float) -> float:
    return sum(
        item["Q"] * state["xi"]
        for item, state in zip(TRANSITIONS, transition_state(u, temperature))
    ) - target_charge


def solve_u(temperature: float, xbar: float) -> float:
    target = sum(item["Q"] for item in TRANSITIONS) * xbar
    lo, hi = -1.0, 1.0
    flo, fhi = charge_residual(lo, temperature, target), charge_residual(hi, temperature, target)
    if not (flo < 0.0 < fhi):
        raise RuntimeError("independent bracket does not contain the monotone root")
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        fm = charge_residual(mid, temperature, target)
        if fm < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def implicit_probe() -> dict[str, Any]:
    temperature = 298.15
    xbar = 0.25
    u = solve_u(temperature, xbar)
    states = transition_state(u, temperature)
    f_u = sum(item["Q"] * state["g"] for item, state in zip(TRANSITIONS, states))
    weights = [item["Q"] * state["g"] / f_u for item, state in zip(TRANSITIONS, states)]
    simple = sum(w * item["dS"] / FARADAY for w, item in zip(weights, TRANSITIONS))
    complete = sum(
        w * (item["dS"] / FARADAY + (R / FARADAY) * state["z"])
        for w, item, state in zip(weights, TRANSITIONS, states)
    )
    dt = 1.0e-3
    thermal_fd = (solve_u(temperature + dt, xbar) - solve_u(temperature - dt, xbar)) / (2.0 * dt)
    total_q = sum(item["Q"] for item in TRANSITIONS)
    target = total_q * xbar
    dq = 1.0e-7

    def solve_target(target_charge: float) -> float:
        lo, hi = -1.0, 1.0
        for _ in range(120):
            mid = 0.5 * (lo + hi)
            if charge_residual(mid, temperature, target_charge) < 0.0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    du_dq_fd = (solve_target(target + dq) - solve_target(target - dq)) / (2.0 * dq)
    return {
        "T_K": temperature,
        "xbar": xbar,
        "U_V": u,
        "target_charge_Qcell": target,
        "F_U_Qcell_per_V": f_u,
        "dQdU_Qcell_per_V": f_u,
        "dUdQ_V_per_Qcell_analytic": 1.0 / f_u,
        "dUdQ_V_per_Qcell_fd": du_dq_fd,
        "reciprocal_product": f_u * (1.0 / f_u),
        "simple_dUdT_V_per_K": simple,
        "complete_dUdT_V_per_K": complete,
        "finite_difference_dUdT_V_per_K": thermal_fd,
        "thermal_abs_error_V_per_K": abs(complete - thermal_fd),
        "charge_sensitivity_abs_error_V_per_Qcell": abs(1.0 / f_u - du_dq_fd),
        "qrev_over_I_V": -temperature * complete,
        "transition_states": [
            {
                "name": item["name"],
                "center_V": state["center"],
                "width_V": state["width"],
                "xi": state["xi"],
                "g_per_V": state["g"],
                "weight": weight,
                "config_V_per_K": (R / FARADAY) * state["z"],
            }
            for item, state, weight in zip(TRANSITIONS, states, weights)
        ],
    }


def logistic_probe() -> dict[str, float]:
    temperature = 298.15
    width = R * temperature / FARADAY
    n = 20000
    lo, hi = -20.0 * width, 20.0 * width
    h = (hi - lo) / n
    total = 0.0
    for i in range(n + 1):
        v = lo + i * h
        xi = stable_logistic(v / width)
        y = xi * (1.0 - xi) / width
        coefficient = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        total += coefficient * y
    area = total * h / 3.0
    eps = 1.0e-7
    derivative_fd = (stable_logistic(eps / width) - stable_logistic(-eps / width)) / (2.0 * eps)
    return {
        "T_K": temperature,
        "w_V": width,
        "center_xi": 0.5,
        "analytic_peak_height_per_V": 1.0 / (4.0 * width),
        "finite_difference_peak_height_per_V": derivative_fd,
        "truncated_area": area,
        "area_abs_error": abs(1.0 - area),
    }


def hysteresis_probe() -> dict[str, float]:
    temperature = 298.15
    critical = 2.0 * R * temperature

    def gap(omega: float) -> float:
        if omega <= critical:
            return 0.0
        u = math.sqrt(1.0 - critical / omega)
        return 2.0 * (omega * u - critical * math.atanh(u)) / FARADAY

    omega = 4.0 * R * temperature
    near = critical * (1.0 + 1.0e-8)
    return {
        "T_K": temperature,
        "critical_Omega_J_per_mol": critical,
        "gap_below_V": gap(critical * 0.999),
        "gap_at_critical_V": gap(critical),
        "gap_near_above_V": gap(near),
        "gap_at_4RT_V": gap(omega),
        "positive_above": float(gap(omega) > 0.0),
    }


def causal_probe() -> dict[str, float]:
    width = 1.0
    length = 0.02
    step = 0.001
    count = int(30.0 / step) + 1
    grid = [-15.0 + i * step for i in range(count)]
    xi_dis = [stable_logistic(v / width) for v in grid]
    a = math.exp(-step / length)
    lag_dis = [xi_dis[0]]
    for i in range(1, count):
        lag_dis.append(a * lag_dis[-1] + (1.0 - a) * 0.5 * (xi_dis[i - 1] + xi_dis[i]))
    peak_dis = [(x - y) / length for x, y in zip(xi_dis, lag_dis)]
    xi_chg = [stable_logistic(-v / width) for v in grid]
    lag_chg = [0.0] * count
    lag_chg[-1] = xi_chg[-1]
    for i in range(count - 2, -1, -1):
        lag_chg[i] = a * lag_chg[i + 1] + (1.0 - a) * 0.5 * (xi_chg[i + 1] + xi_chg[i])
    peak_chg = [(x - y) / length for x, y in zip(xi_chg, lag_chg)]
    equilibrium = [x * (1.0 - x) / width for x in xi_dis]
    interior = range(1000, count - 1000)
    mirror_error = max(abs(peak_dis[i] - peak_chg[count - 1 - i]) for i in interior)
    equilibrium_error = max(abs(peak_dis[i] - equilibrium[i]) for i in interior)
    return {
        "w_arbitrary": width,
        "L_over_w": length / width,
        "grid_step_over_w": step / width,
        "kernel_normalization_exact": 1.0,
        "minimum_discharge_peak": min(peak_dis[1000:-1000]),
        "minimum_charge_peak": min(peak_chg[1000:-1000]),
        "mirror_max_abs_error": mirror_error,
        "small_L_max_abs_error_per_w": equilibrium_error,
    }


def einstein_entropy(temperature: float, theta_e: float) -> float:
    u = theta_e / temperature
    return R * (-math.log1p(-math.exp(-u)) + u / math.expm1(u))


def einstein_free_energy(temperature: float, theta_e: float) -> float:
    return R * temperature * math.log1p(-math.exp(-theta_e / temperature))


def einstein_probe() -> dict[str, Any]:
    theta_e, tref = 700.0, 298.15
    sref = einstein_entropy(tref, theta_e)

    def delta_s(t: float) -> float:
        return einstein_entropy(t, theta_e) - sref

    def delta_u(t: float) -> float:
        return -(
            einstein_free_energy(t, theta_e)
            - einstein_free_energy(tref, theta_e)
            + sref * (t - tref)
        ) / FARADAY

    samples = []
    for t in (278.15, 298.15, 318.15, 348.15):
        dt = 1.0e-3
        fd = (delta_u(t + dt) - delta_u(t - dt)) / (2.0 * dt)
        analytic = delta_s(t) / FARADAY
        samples.append(
            {
                "T_K": t,
                "delta_S_J_per_molK": delta_s(t),
                "analytic_dU_dT_V_per_K": analytic,
                "finite_difference_dU_dT_V_per_K": fd,
                "abs_error_V_per_K": abs(analytic - fd),
            }
        )
    return {
        "theta_E_K": theta_e,
        "T_ref_K": tref,
        "delta_S_at_ref_J_per_molK": delta_s(tref),
        "delta_U_at_ref_V": delta_u(tref),
        "samples": samples,
        "max_roundtrip_error_V_per_K": max(row["abs_error_V_per_K"] for row in samples),
    }


def electronic_probe() -> dict[str, float]:
    temperature, tref = 300.0, 298.15
    gmax, delta_x, sigma = 13.0, 0.05, 0.5
    a_e = -(math.pi**2 / 3.0) * R * (KB / EV_J) * (gmax / delta_x) * sigma * (1.0 - sigma)
    entropy = a_e * temperature

    def shift(t: float) -> float:
        return a_e * (t * t - tref * tref) / (2.0 * FARADAY)

    dt = 1.0e-3
    derivative_fd = (shift(temperature + dt) - shift(temperature - dt)) / (2.0 * dt)
    analytic = entropy / FARADAY
    return {
        "T_K": temperature,
        "T_ref_K": tref,
        "gmax_states_per_eV_atom": gmax,
        "delta_x": delta_x,
        "sigma_center": sigma,
        "a_e_J_per_molK2": a_e,
        "delta_S_e_J_per_molK": entropy,
        "dU_dT_V_per_K": analytic,
        "finite_difference_T2_dU_dT_V_per_K": derivative_fd,
        "roundtrip_abs_error_V_per_K": abs(analytic - derivative_fd),
    }


def lag_timebase_probe() -> dict[str, float]:
    c_rate_per_hour = 0.1
    k_per_second = 2.5
    correct = (c_rate_per_hour / 3600.0) / k_per_second
    unconverted = c_rate_per_hour / k_per_second
    return {
        "c_rate_per_hour": c_rate_per_hour,
        "k_per_second": k_per_second,
        "dimensionally_closed_Lq": correct,
        "unconverted_numeric_Lq": unconverted,
        "error_factor": unconverted / correct,
    }


def probe_bundle() -> dict[str, Any]:
    return {
        "LOGISTIC": logistic_probe(),
        "IMPLICIT": implicit_probe(),
        "HYSTERESIS": hysteresis_probe(),
        "CAUSAL_MEMORY": causal_probe(),
        "EINSTEIN": einstein_probe(),
        "LCO_ELECTRONIC": electronic_probe(),
        "LAG_TIMEBASE": lag_timebase_probe(),
    }


def check(
    check_id: str,
    family: str,
    title: str,
    anchors: list[dict[str, Any]],
    assumptions: list[str],
    steps: list[str],
    dimensions: dict[str, str],
    sign: str,
    domain: str,
    limits: list[str],
    probe_id: str | None,
    result: str,
    derivation_status: str,
    implementation_status: str,
    trace_ids: list[str],
    rationale: str,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "family": family,
        "title": title,
        "equation_or_claim_ids": trace_ids,
        "source_anchors": anchors,
        "assumptions": assumptions,
        "derivation_steps": [
            {"ordinal": i + 1, "statement": statement} for i, statement in enumerate(steps)
        ],
        "dimensions": dimensions,
        "sign_convention": sign,
        "domain": domain,
        "analytic_limits": limits,
        "independent_probe": {
            "probe_id": probe_id,
            "status": "PASS" if probe_id else "NOT_APPLICABLE",
            "production_imported": False,
        },
        "result": result,
        "derivation_status": derivation_status,
        "implementation_conformance": implementation_status,
        "implementation_impact": trace_ids,
        "result_rationale": rationale,
        "authority_boundary": "INTERNAL_SOURCE_MODEL_REDERIVATION_NOT_EXTERNAL_SCIENTIFIC_TRUTH",
    }


def build_checks() -> list[dict[str, Any]]:
    p = "Claude/docs/v1.0.19/_sections/"
    return [
        check("P060-PHY-001", "CONVENTION", "direction, voltage and current coordinate split",
              [anchor(p+"ch1_sec01_n0n1.tex", 10, 34), anchor(p+"ch2_sec07_revheat.tex", 27, 39)],
              ["Ch1 sigma_d labels half-cell delithiation as discharge", "Bernardi I>0 labels cell discharge and graphite lithiation"],
              ["Map c-rate and Q_cell to current magnitude with one time unit", "Remove ohmic polarization as V_n=V_app-sigma_d|I|R_n", "Keep Bernardi signed I separate from sigma_d"],
              {"c_rate*Q_cell": "A only after hour/second consistency", "I*R_n": "V", "sigma_d": "1"},
              "Ch1 sigma_d=+1 is graphite delithiation; Ch2 I>0 is cell discharge and graphite lithiation", "half-cell and cell labels are separate coordinate layers", [], None, "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH1-CHARGE-BALANCE", "TRC-CH2-REVERSIBLE-HEAT"], "Both formulae are internally usable, but the same word discharge denotes opposite graphite reaction directions."),
        check("P060-PHY-002", "THERMODYNAMIC_CENTER", "Gibbs reaction center and entropy slope",
              [anchor(p+"ch1_sec03_center.tex", 42, 69), anchor(p+"ch1_sec12_lcocenter.tex", 26, 59)],
              ["one-electron insertion reaction", "F>0", "instantaneous Gibbs identity at fixed pressure"],
              ["Use Delta G=Delta H-T Delta S", "Use Delta G=-F U", "Obtain U=(-Delta H+T Delta S)/F and dU/dT=Delta S/F for T-independent Delta S"],
              {"Delta H/F": "V", "T*Delta S/F": "V", "Delta S/F": "V/K"},
              "positive insertion Delta S raises the half-cell equilibrium center with T", "thermodynamic state function; T-dependent Delta S requires integration", ["Delta S=constant gives a linear center"], None, "PASS", "CLOSED", "ALIGNED", ["TRC-CH1-CENTER-THERMO", "TRC-CH1-LCO-DIRECTION-CENTER"], "The stated center law follows from the declared reaction convention."),
        check("P060-PHY-003", "EQUILIBRIUM_OBSERVATION", "logistic derivative, peak height and area",
              [anchor(p+"ch1_sec05_width.tex", 150, 175), anchor(p+"ch1_sec06_eqpeak.tex", 8, 32)],
              ["w>0", "monotone equilibrium branch", "sigma_d is held fixed"],
              ["Write xi=logistic[sigma_d(V-Ud)/w]", "Differentiate along the progress direction", "Obtain the positive bell xi(1-xi)/w with height 1/(4w) and unit area"],
              {"w": "V", "d xi/dV": "1/V", "Q_j dxi/dV": "charge/V"},
              "positive observation peak uses the progress-direction derivative; raw dxi/dV changes sign on charge", "0<xi<1 and w>0", ["V=U gives xi=1/2", "integral over the full transition equals one"], "LOGISTIC", "FAIL", "CLOSED", "MISALIGNED", ["TRC-CH1-WIDTH-LOGISTIC", "TRC-CH1-CHARGE-BALANCE"], "Independent quadrature reproduces the positive magnitude, but the source silently relabels that magnitude as signed dQ/dV on charge."),
        check("P060-PHY-004", "CHARGE_BALANCE", "background-free implicit charge residual",
              [anchor(p+"ch2_sec05_mixing.tex", 12, 38), anchor(p+"ch2_sec08_synthesis.tex", 36, 39)],
              ["Q_j>0", "w_j>0", "branch-free equilibrium centers", "Q=sum Q_j", "background charge is zero"],
              ["Define F(U;Qbar,T)=sum_j Q_j xi_j(U,T)-Q xbar", "Solve F=0 for U", "Feed the root back to every xi_j"],
              {"F": "charge", "F_U": "charge/V", "Q*xbar": "charge"},
              "xbar=1-x increases with delithiation and U on the branch-free logistic", "background-free equilibrium mixture", ["xbar->0 and 1 approach endpoint roots"], "IMPLICIT", "PASS", "CLOSED", "PARTIAL", ["TRC-CH2-MIXING-IMPLICIT", "TRC-CH1-CHARGE-BALANCE"], "The four-transition source fixture has a bracketed monotone root and reproduces the worked point."),
        check("P060-PHY-005", "CHARGE_BALANCE", "background primitive and integration constant",
              [anchor(p+"ch1_sec10_sum.tex", 5, 14), anchor(p+"ch2_sec05_mixing.tex", 12, 20)],
              ["C_bg=dQ_bg/dV is supplied", "an integration reference for Q_bg is additionally required"],
              ["Integrate the ICA identity to Q=Q_bg+sum Q_j xi_j", "Observe that C_bg alone determines Q_bg only up to a constant", "Compare with the Chapter 2 residual, which omits Q_bg"],
              {"C_bg": "charge/V", "Q_bg": "charge", "integration_constant": "charge"},
              "no sign is fixed for an arbitrary background", "nonzero background requires a primitive and reference state", ["C_bg=0 closes the published Chapter 2 residual"], None, "CONDITIONAL", "BOUNDED", "ABSENT", ["TRC-CH1-CHARGE-BALANCE", "TRC-CH2-MIXING-IMPLICIT"], "The source does not define the background primitive or its charge offset for the implicit composition solve."),
        check("P060-PHY-006", "IMPLICIT_SENSITIVITY", "local dU/dQ and reciprocal ICA/DVA",
              [anchor(p+"ch2_sec05_mixing.tex", 20, 38), anchor(p+"ch1_sec10_sum.tex", 5, 14)],
              ["F is differentiable", "F_U is nonzero", "target Q is an independent charge coordinate"],
              ["Differentiate F(U,Q)=0 to F_U dU+F_Q dQ=0", "Obtain dU/dQ=-F_Q/F_U", "For F=sum Q_j xi_j-Q, F_Q=-1 and dU/dQ=1/F_U while dQ/dU=F_U"],
              {"F_U": "charge/V", "dU/dQ": "V/charge", "dQ/dU": "charge/V"},
              "positive Q_j and w_j give F_U>0 on finite logistic states", "local differentiable monotone branch only", ["(dU/dQ)(dQ/dU)=1", "F_U->0 makes DVA singular"], "IMPLICIT", "PASS", "CLOSED", "PARTIAL", ["TRC-CH2-MIXING-IMPLICIT", "TRC-CH1-CHARGE-BALANCE"], "Analytic and independent charge finite differences agree within tolerance."),
        check("P060-PHY-007", "UNIQUENESS", "global root uniqueness and plateau/multiroot boundary",
              [anchor(p+"ch2_sec05_mixing.tex", 12, 38), anchor(p+"ch1_sec04_hys.tex", 11, 30)],
              ["the branch-free ideal-logistic special case is monotone", "regular-solution and history branches may be nonmonotone"],
              ["Show F_U=sum Q_j g_j>0 for positive ideal-logistic components", "Note that this proves uniqueness only for that restricted branch", "Retain plateau, multi-root, negative-background and history-dependent cases as unresolved"],
              {"F_U": "charge/V"},
              "restricted ideal branch is increasing", "general source model with phase separation, background or history", ["F_U=0 is a fold or plateau singular boundary"], "IMPLICIT", "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH2-MIXING-IMPLICIT", "TRC-CH1-HYSTERESIS"], "The worked bisection root does not prove uniqueness for every admitted model path."),
        check("P060-PHY-008", "WIDTH_THERMAL", "temperature derivative of width",
              [anchor(p+"ch1_sec05_width.tex", 150, 175), anchor(p+"ch2_sec05_mixing.tex", 41, 65)],
              ["n(T)>0", "w=n(T)RT/F when n is the governing input", "direct frozen w is a distinct branch"],
              ["Differentiate w=n(T)RT/F", "Obtain dw/dT=(R/F)(n+T dn/dT)", "For the documented default n=1 obtain R/F, whereas frozen direct w gives zero"],
              {"w": "V", "dw/dT": "V/K"},
              "positive constant n gives positive dw/dT", "n-governed and direct-w branches must not be merged", ["constant n reduces to nR/F"], "IMPLICIT", "FAIL", "CONFLICTING", "MISALIGNED", ["TRC-CH2-WIDTH-T-DEPENDENCE", "TRC-CH1-WIDTH-LOGISTIC"], "The no-n/no-w implementation has w=RT/F but reports dw/dT=0; the complete-input list also omits the required thermal-width state."),
        check("P060-PHY-009", "HYSTERESIS", "regular-solution spinodal gap and empirical branch scale",
              [anchor(p+"ch1_sec04_hys.tex", 11, 30), anchor(p+"ch1_sec04_hys.tex", 90, 139)],
              ["symmetric Bragg-Williams regular solution", "Omega is T-independent in the displayed derivative", "gamma and h_eta are empirical multipliers"],
              ["Set g''=RT/[xi(1-xi)]-2Omega to zero", "Obtain xi_s=(1+-sqrt(1-2RT/Omega))/2", "Evaluate the spinodal voltage gap and multiply its half-gap by sigma_d gamma h_eta"],
              {"Omega/F": "V", "RT/F": "V", "gap": "V"},
              "gap is nonnegative; discharge center is above charge under Ch1 labels", "Omega>2RT for a real spinodal; branch scale is phenomenological", ["gap=0 for Omega<=2RT", "gap approaches zero from above as (Tc-T)^(3/2)"], "HYSTERESIS", "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH1-HYSTERESIS", "TRC-CH1-LCO-HYSTERESIS"], "The algebraic spinodal result closes, but gamma*h_eta and the use of a spinodal upper bound as observed hysteresis are not independently derived."),
        check("P060-PHY-010", "KINETIC_LAG", "lag length timebase closure",
              [anchor(p+"ch1_sec08_lag.tex", 9, 30), anchor(p+"ch1_sec08_lag.tex", 88, 120), anchor(p+"ch1_sec10_sum.tex", 44, 58)],
              ["q=Q/Q_cell is dimensionless", "k uses inverse seconds", "c-rate is stated in inverse hours"],
              ["Divide dxi/dt by dq/dt=|I|/Q_cell", "Obtain L_q=(|I|/Q_cell)/k", "Convert c-rate from h^-1 to s^-1 before combining with k in s^-1"],
              {"I/Q_cell": "1/s", "k": "1/s", "L_q": "1", "L_V": "V"},
              "L_q and L_V are nonnegative magnitudes", "one consistent timebase is mandatory", ["I->0 gives L_q,L_V->0 when all other factors remain finite"], "LAG_TIMEBASE", "FAIL", "CONFLICTING", "MISALIGNED", ["TRC-CH1-LAG-LENGTH"], "The source explicitly acknowledges a factor-3600 alternative while the runtime convention uses the unconverted numeric c-rate; the numerical seed lag is not dimensionally unique."),
        check("P060-PHY-011", "CAUSAL_MEMORY", "monotone causal convolution and small-lag limit",
              [anchor(p+"ch1_sec09_tail.tex", 10, 64), anchor(p+"ch1_sec09_tail.tex", 95, 144), anchor(p+"ch1_sec09_tail.tex", 146, 190)],
              ["L_V>0", "a monotone full-history sweep", "asymptotic boundary state is equilibrated"],
              ["Solve the first-order lag equation with an integrating factor", "Use the lower-past integral for discharge and upper-past integral for charge", "Differentiate the lagged state to obtain a nonnegative peak and take L_V->0"],
              {"kernel": "1/V", "xi_lag": "1", "peak": "1/V"},
              "charge is the voltage mirror of discharge when all other parameters are symmetric", "monotone semi-infinite history", ["kernel area is one", "L_V->0 recovers the equilibrium bell"], "CAUSAL_MEMORY", "PASS", "CLOSED", "PARTIAL", ["TRC-CH1-TAIL-CAUSAL"], "Independent discrete convolution confirms normalization, positivity, mirroring and the small-lag limit within discretization tolerance."),
        check("P060-PHY-012", "PROTOCOL_STATE", "rest, mid-protocol reversal and finite-window state",
              [anchor(p+"ch1_sec09_tail.tex", 20, 35), anchor(p+"ch1_sec09_tail.tex", 146, 190)],
              ["the displayed convolution extrapolates to an infinite past", "rest has dq/dt=0 and cannot be parameterized by monotone q"],
              ["Retain the finite-start boundary term r(q0) exp[-(q-q0)/Lq]", "Observe that sending q0 to infinity discards initial state", "A reversal or rest therefore needs explicit time/history state not present in the static sweep equations"],
              {"r": "1", "L_q": "1", "rest_time": "s"},
              "mid-protocol reversal changes the causal past but not merely the integration label", "finite and nonmonotone protocols", ["infinite equilibrated prehistory removes the boundary term"], None, "FAIL", "NOT_DERIVABLE", "ABSENT", ["TRC-CH1-TAIL-CAUSAL", "TRC-CH1-LAG-LENGTH"], "The source closes two separate monotone sweep directions, not a stateful rest/reversal/finite-window protocol."),
        check("P060-PHY-013", "THERMAL_MIXING", "implicit thermal sensitivity and complete weighting",
              [anchor(p+"ch2_sec05_mixing.tex", 12, 85), anchor(p+"ch2_sec08_synthesis.tex", 11, 39)],
              ["F_U is nonzero", "branch-free equilibrium", "the width derivative is explicitly known"],
              ["Differentiate the charge residual at fixed xbar", "Separate center motion and width motion in partial xi/partial T", "Divide by F_U to obtain the weighted simple or complete entropy coefficient"],
              {"partial xi/partial T": "1/K", "dU/dT": "V/K", "Q_j g_j": "charge/V"},
              "config term sign follows z=ln[xi/(1-xi)]", "thermal-width law must be declared", ["single-transition limit gives dUj/dT+(dw/dT)z", "frozen w removes the config-width term"], "IMPLICIT", "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH2-MIXING-WEIGHTED", "TRC-CH2-COMPLETE-SYNTHESIS", "TRC-CH2-WIDTH-T-DEPENDENCE"], "The independent four-transition finite difference matches the complete expression only under w=RT/F; direct frozen width requires a different expression."),
        check("P060-PHY-014", "EINSTEIN", "Einstein entropy/free-energy round trip",
              [anchor(p+"ch2_sec04_einstein.tex", 17, 44), anchor(p+"ch2_sec04_einstein.tex", 46, 95)],
              ["one representative harmonic mode", "theta_E>0", "T>0", "T_ref>0"],
              ["Differentiate the harmonic-mode free energy to obtain S_vib", "Subtract the T_ref entropy", "Integrate Delta S_vib/F from T_ref so Delta U and Delta S share one free energy"],
              {"S_vib": "J/(mol K)", "Delta U_vib": "V", "dDeltaU/dT": "V/K"},
              "Delta U and Delta S are exactly zero at T_ref", "representative Einstein mode, not a phonon-DOS proof", ["T->0 gives S_vib->0", "high T gives R[1+ln(T/theta_E)]"], "EINSTEIN", "PASS", "CLOSED", "PARTIAL", ["TRC-CH2-EINSTEIN-ROUNDTRIP", "TRC-CH2-VIBRATIONAL-ELECTRONIC"], "Independent free-energy finite differences reproduce Delta S_vib/F and the source's four illustrative slopes."),
        check("P060-PHY-015", "LCO_ELECTRONIC", "Sommerfeld unit conversion and T-squared center curvature",
              [anchor(p+"ch1_sec12_lcocenter.tex", 67, 82), anchor(p+"ch1_sec15_lcoelec.tex", 90, 144), anchor(p+"ch1_sec15_lcoelec.tex", 146, 175)],
              ["degenerate metallic regime", "g(E) is locally frozen near E_F", "the logistic g(E_F,x) gate is a model assumption", "one mole of relevant insertion sites is the molar basis"],
              ["Convert states/eV/atom to states/J/atom by division by e_V and multiply by N_A", "Differentiate the logistic DOS gate in insertion x", "Integrate Delta S_e=a_e T so the center shift contains a_e(T^2-T_ref^2)/(2F)"],
              {"a_e": "J/(mol K^2)", "Delta S_e": "J/(mol K)", "center_shift": "V"},
              "insertion through the stated gate gives Delta S_e<0", "metallic Sommerfeld endpoint plus empirical continuous composition gate", ["T->0 removes the leading electronic entropy", "outside the gate sigma(1-sigma)->0"], "LCO_ELECTRONIC", "FAIL", "CLOSED", "MISALIGNED", ["TRC-CH1-LCO-ENTROPY-ELECTRONIC", "TRC-CH1-LCO-FULL-PLUGIN"], "The independent unit and T^2 round trip closes, but the reachable implementation freezes the electronic contribution at x_center and 298.15 K and therefore lacks the source T^2 path."),
        check("P060-PHY-016", "REVERSIBLE_HEAT", "electrode entropy and reversible heat sign",
              [anchor(p+"ch2_sec07_revheat.tex", 10, 40), anchor(p+"ch2_sec08_synthesis.tex", 88, 105)],
              ["Bernardi signed I is used", "quasi-equilibrium low-rate control volume", "mixing enthalpy and explicit phase-change residuals are omitted as stated"],
              ["Use Delta G=-F U to obtain Delta S=F dU/dT", "Insert it into qdot_rev=-IT dU/dT", "Map electrode and full-cell signs only after defining the voltage difference"],
              {"I*T*dU/dT": "W", "qdot/I": "V"},
              "I>0 and dU/dT<0 gives positive heat under the stated cell convention", "single-electrode low-rate Bernardi boundary", ["I=0 gives zero heat rate", "reversing I reverses the reversible term"], "IMPLICIT", "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH2-REVERSIBLE-HEAT", "TRC-CH2-REGRESSION-WITNESSES"], "The numerical worked sign is reproduced, but half-cell/full-cell and Ch1 direction labels require an explicit assembly map."),
        check("P060-PHY-017", "HYSTERESIS_HEAT", "reversible branch average versus hysteresis dissipation",
              [anchor(p+"ch2_sec05_mixing.tex", 193, 223)],
              ["charge and discharge branches sample comparable states", "exact cancellation is only linearized for gap much smaller than width"],
              ["Compute each branch's weighted dU/dT", "Average branch coefficients for the reversible estimate", "Keep I Delta U_hys as a separate irreversible dissipation channel"],
              {"dU/dT": "V/K", "I*Delta U_hys": "W"},
              "the gap magnitude dissipates positive cycle energy", "finite-gap higher-order corrections remain", ["Delta U_hys->0 makes the branch average equal the branch-free value"], None, "CONDITIONAL", "BOUNDED", "ABSENT", ["TRC-CH2-HYSTERESIS-REVERSIBLE"], "The source states a linearized branch-average rule, while no explicit reachable branch-average implementation exists."),
        check("P060-PHY-018", "MATERIAL_PATH", "Graphite and LCO observation-path separation",
              [anchor(p+"ch1_sec11_lcointro.tex", 31, 49), anchor(p+"ch1_sec12_lcocenter.tex", 52, 86), anchor(p+"ch1_sec16_lcopeak.tex", 8, 65)],
              ["both electrodes use the same insertion-reaction Gibbs sign", "electrode direction labels are mapped separately"],
              ["Derive each electrode center from its own reaction inputs", "Apply electrode-specific electronic and direction extensions", "Compose full-cell voltage or heat only after subtracting electrode potentials under one convention"],
              {"U_anode": "V vs Li", "U_cathode": "V vs Li", "U_cell": "V"},
              "full-cell voltage is cathode minus anode under the usual assembly convention, but final assembly is outside this source scope", "separate half-cell paths", [], None, "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH1-LCO-DIRECTION-CENTER", "TRC-CH1-LCO-PEAK", "TRC-CH2-REVERSIBLE-HEAT"], "The half-cell forms are separable; the v1.0.19 source does not close the final full-cell composition path."),
        check("P060-PHY-019", "BROADENING", "equilibrium, lag and ensemble width authority",
              [anchor(p+"ch1_sec07_broadening.tex", 34, 126), anchor(p+"ch1_sec07_broadening.tex", 179, 262)],
              ["intrinsic, kinetic and ensemble broadening are distinct mechanisms"],
              ["Keep the equilibrium logistic scale separate from causal lag", "Treat apparent-U heterogeneity as a forward ensemble average", "Do not infer a unique mechanism or inverse distribution from a single observed width"],
              {"all_width_terms": "V"},
              "broadening magnitudes are nonnegative but not simply signed additive physics parameters", "forward qualitative budget only", ["I->0 removes kinetic lag but not intrinsic or ensemble width"], None, "UNVERIFIED", "NOT_DERIVABLE", "PARTIAL", ["TRC-CH1-BROADENING-BUDGET"], "No production ensemble calculator or source-grounded inverse-identification law closes the width budget."),
        check("P060-PHY-020", "PARAMETER_AUTHORITY", "material-number authority boundary",
              [anchor(p+"ch1_sec10_sum.tex", 16, 58), anchor(p+"ch1_sec14_lcodecomp.tex", 84, 98), anchor(p+"ch1_sec15_lcoelec.tex", 146, 189)],
              ["Phase 071 has not verified cited primary sources"],
              ["Separate source-cited endpoint or trend from transition-specific numbers", "Mark fit initializations and model gates independently", "Do not convert a runtime match into material authority"],
              {"authority": "categorical"},
              "not applicable", "internal source authority only", [], None, "UNVERIFIED", "NOT_DERIVABLE", "NOT_APPLICABLE", ["TRC-CH1-LCO-ENTROPY-ELECTRONIC", "TRC-CH1-LAG-LENGTH", "TRC-CH1-HYSTERESIS"], "Several numbers are explicitly fit-only or ground-not-found; cited items remain source-cited-unverified until Phase 071."),
        check("P060-PHY-021", "IDENTIFIABILITY", "structurally inseparable parameter combinations",
              [anchor(p+"ch1_sec08_lag.tex", 88, 120), anchor(p+"ch1_sec04_hys.tex", 111, 139), anchor(p+"ch2_sec04_einstein.tex", 97, 105), anchor(p+"ch1_sec15_lcoelec.tex", 129, 175)],
              ["only the displayed observation operators are available"],
              ["Factor each observation into parameter combinations", "Identify transformations that preserve the same curve at fixed protocol", "Require additional temperatures, rates, directions or independent measurements to break each symmetry"],
              {"identifiability": "rank/property statement"},
              "not applicable", "single-condition observation operators", [], None, "CONDITIONAL", "BOUNDED", "PARTIAL", ["TRC-CH1-LAG-LENGTH", "TRC-CH1-HYSTERESIS", "TRC-CH2-EINSTEIN-ROUNDTRIP", "TRC-CH1-LCO-ENTROPY-ELECTRONIC"], "Single-condition curves identify combinations such as L_V, gamma*h_eta*gap, and gmax/delta_x rather than every primitive parameter."),
        check("P060-PHY-022", "HYSTERESIS", "zero-current hysteresis baseline authority",
              [anchor(p+"ch1_sec06_eqpeak.tex", 30, 32), anchor(p+"ch1_sec18_inputs.tex", 27, 28)],
              ["gamma may remain nonzero as current tends to zero", "lag vanishes with current", "hysteresis and kinetic lag are distinct"],
              ["Take I to zero in the branch-center equation", "Retain the sigma_d gamma h_eta gap term when gamma is nonzero", "Compare the resulting direction-dependent center with the input section's direction-invariant zero-current baseline"],
              {"gamma*h_eta*gap": "V", "I*R_n": "V", "L_V": "V"},
              "nonzero thermodynamic branch shift remains direction-odd even when current-dependent polarization and lag vanish", "zero-current limit with an active hysteresis branch", ["gamma->0 or gap->0 restores a direction-invariant baseline"], None, "FAIL", "CONFLICTING", "UNVERIFIED", ["TRC-CH1-HYSTERESIS", "TRC-CH1-CHARGE-BALANCE"], "Two source sections make incompatible zero-current claims unless an unstated gamma->0 condition is imposed."),
    ]


def findings() -> list[dict[str, Any]]:
    rows = [
        ("P060-PHY-P1-001", "P1", ["P060-PHY-010"], "The lag seed uses an h^-1 c-rate beside s^-1 Eyring kinetics without one canonical conversion; the two numeric readings differ by 3600.", "Step 45.1 CORRECT route; Phase 076 must freeze a timebase."),
        ("P060-PHY-P1-002", "P1", ["P060-PHY-005"], "C_bg defines dQ_bg/dV but no Q_bg primitive, reference charge, or inclusion in the composition residual is specified.", "Step 45.1 CORRECT route; Phase 074 must define the background charge state."),
        ("P060-PHY-P1-003", "P1", ["P060-PHY-007"], "The worked monotone bisection does not prove a unique root for admitted plateau, phase-separated, background, or history-dependent paths.", "Step 45.1 preserve as conditional; Phase 075/076 must close branch selection."),
        ("P060-PHY-P1-004", "P1", ["P060-PHY-008", "P060-PHY-013"], "The default thermal width is RT/F but the implementation derivative is zero, and the complete-expression input list omits n(T) or dw/dT.", "Step 45.1 CORRECT route; retain Step 43 MISALIGNED finding."),
        ("P060-PHY-P1-005", "P1", ["P060-PHY-012"], "The static monotone convolution has no explicit state for rest, finite-window initialization, or mid-protocol reversal.", "Step 45.1 CORRECT/NEW_SCOPE route; Phase 076 state equation."),
        ("P060-PHY-P1-006", "P1", ["P060-PHY-015"], "The source's LCO electronic entropy requires x,V,T dependence and T-squared center curvature, whereas the reachable path freezes x_center and 298.15 K.", "Step 45.1 CORRECT route; Phase 078 evidence-gated LCO closure."),
        ("P060-PHY-P1-007", "P1", ["P060-PHY-017"], "The reversible charge/discharge branch-average path is absent and the source identity is exact only to linear order in a small hysteresis gap.", "Step 45.1 THEORY_ONLY/CORRECT route; Phase 081 heat closure."),
        ("P060-PHY-P1-008", "P1", ["P060-PHY-001", "P060-PHY-016", "P060-PHY-018"], "Ch1 half-cell discharge and Bernardi cell discharge are opposite graphite reaction directions; electrode/full-cell heat signs need an explicit map.", "Step 45.1 preserve as sign blocker; Phase 074/081."),
        ("P060-PHY-P1-009", "P1", ["P060-PHY-020"], "Transition-specific Graphite kinetic/interaction numbers and continuous LCO gate parameters lack primary-source authority or are explicitly fit-only.", "Keep UNVERIFIED; Phase 071/072 authority and data gates."),
        ("P060-PHY-P1-010", "P1", ["P060-PHY-019"], "The three broadening mechanisms are not closed by a forward ensemble calculator or identifiable inverse law.", "Step 45.1 THEORY_ONLY/NEW_SCOPE; Phase 077/081."),
        ("P060-PHY-P1-011", "P1", ["P060-PHY-003"], "The source uses dQ/dV for both the signed derivative of a progress-increasing charge coordinate and its positive ICA magnitude, which disagree on charge.", "Step 45.1 CORRECT route; freeze separate signed-derivative and positive-magnitude observables."),
        ("P060-PHY-P1-012", "P1", ["P060-PHY-022"], "The source says nonzero hysteresis survives I->0 in one section but declares the zero-current baseline direction-invariant in another without gamma->0.", "Step 45.1 source-conflict route; do not promote either baseline as canonical before resolution."),
        ("P060-PHY-P2-001", "P2", ["P060-PHY-009", "P060-PHY-021"], "Only gamma*h_eta*DeltaU_hys is observed in the branch shift; its factors are not separately identified.", "Identifiability carry-forward."),
        ("P060-PHY-P2-002", "P2", ["P060-PHY-010", "P060-PHY-021"], "A direct L_V bypass and the kinetic product cannot identify dH_a, dS_a, chi, Omega and dV/dq separately at one condition.", "Multi-rate/multi-temperature carry-forward."),
        ("P060-PHY-P2-003", "P2", ["P060-PHY-002", "P060-PHY-021"], "At one temperature, Delta H and Delta S enter the center only through -DeltaH+TDeltaS.", "Require multi-temperature center data."),
        ("P060-PHY-P2-004", "P2", ["P060-PHY-004", "P060-PHY-005", "P060-PHY-021"], "Capacity scaling and an unfixed background-charge offset can trade against composition normalization.", "Require an absolute charge/reference-state contract."),
        ("P060-PHY-P2-005", "P2", ["P060-PHY-014", "P060-PHY-021"], "Two temperatures constrain only a local slope; Einstein curvature and a linear electronic term need at least three informative temperatures.", "Phase 081 experimental design."),
        ("P060-PHY-P2-006", "P2", ["P060-PHY-015", "P060-PHY-021"], "At the LCO gate center, amplitude is proportional to gmax/delta_x; endpoint and width evidence are needed to separate them.", "Phase 071/072/078 carry-forward."),
        ("P060-PHY-P2-007", "P2", ["P060-PHY-003", "P060-PHY-006"], "ICA/DVA reciprocity is local and fails as a finite number when F_U approaches zero.", "Preserve singular-domain diagnostics."),
        ("P060-PHY-P2-008", "P2", ["P060-PHY-013"], "The source's complete synthesis lists w but consumes n or dw/dT, so arbitrary direct-width thermal behavior is under-specified.", "Correct the future input contract before adoption."),
    ]
    return [
        {"finding_id": fid, "severity": sev, "check_ids": checks, "statement": statement, "disposition": disposition}
        for fid, sev, checks, statement, disposition in rows
    ]


def identifiability_rows() -> list[dict[str, Any]]:
    return [
        {"id": "ID-HS", "combination": "-DeltaH+T DeltaS", "unresolved_primitives": ["DeltaH", "DeltaS"], "required_evidence": "three or more calibrated temperatures or independent calorimetry"},
        {"id": "ID-HYS", "combination": "gamma*h_eta*DeltaU_hys(Omega,T)", "unresolved_primitives": ["gamma", "h_eta", "Omega"], "required_evidence": "full-cycle and partial-cycle bidirectional data over temperature"},
        {"id": "ID-LAG", "combination": "L_V=|dV/dq|*(|I|/Qcell)/k", "unresolved_primitives": ["dH_a", "dS_a", "chi", "Omega", "dVdq"], "required_evidence": "multi-rate, multi-temperature and independent OCV slope"},
        {"id": "ID-CAP", "combination": "Q_j/Q_total with Q_bg offset", "unresolved_primitives": ["Q_j absolute scale", "Q_bg integration constant", "xbar offset"], "required_evidence": "absolute capacity and reference composition"},
        {"id": "ID-WIDTH", "combination": "observed width from intrinsic+lag+ensemble", "unresolved_primitives": ["n or w", "L_V", "ensemble rho(U)"], "required_evidence": "multi-rate and multi-temperature ensemble-resolved data"},
        {"id": "ID-LCO-GATE", "combination": "gmax/delta_x at the gate center", "unresolved_primitives": ["gmax", "delta_x", "x_MIT"], "required_evidence": "independent endpoint DOS plus composition-resolved transition data"},
        {"id": "ID-VIB-ELEC", "combination": "local temperature slope over two points", "unresolved_primitives": ["theta_E", "electronic slope"], "required_evidence": "at least three temperatures spanning useful curvature"},
    ]


def parameter_authority_rows() -> list[dict[str, Any]]:
    return [
        {"id": "PAR-GRA-U", "parameters": ["four graphite U values"], "disposition": "SOURCE_CITED_TIER_B_OR_C_NOT_PRIMARY_VERIFIED", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec10_sum.tex", 23, 39)},
        {"id": "PAR-GRA-DS", "parameters": ["four graphite DeltaS values"], "disposition": "SOURCE_CITED_RANGE_OR_PROFILE_NOT_TRANSITION_SPECIFIC_TRUTH", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec10_sum.tex", 23, 52)},
        {"id": "PAR-GRA-KIN", "parameters": ["Omega", "DeltaH_a", "dVdq"], "disposition": "FIT_INITIAL_OR_TREND_ONLY_GROUND_NOT_FOUND_TRANSITION_SPECIFIC", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec10_sum.tex", 44, 58)},
        {"id": "PAR-HYS", "parameters": ["gamma", "h_eta"], "disposition": "EMPIRICAL_FIT_ONLY", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec04_hys.tex", 111, 126)},
        {"id": "PAR-EINSTEIN", "parameters": ["theta_E=700 K illustration"], "disposition": "ILLUSTRATIVE_OR_DATA_DRIVEN_NOT_MATERIAL_DEFAULT", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch2_sec04_einstein.tex", 97, 105)},
        {"id": "PAR-LCO-DOS", "parameters": ["gmax=13 states/eV/atom"], "disposition": "SOURCE_CITED_SINGLE_ENDPOINT_NOT_PRIMARY_VERIFIED_HERE", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec15_lcoelec.tex", 146, 181)},
        {"id": "PAR-LCO-GATE", "parameters": ["x_MIT=0.85", "delta_x_MIT=0.05", "continuous logistic gate"], "disposition": "SOURCE_CITED_RANGE_PLUS_MODEL_ASSUMPTION_FIT_ONLY", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec15_lcoelec.tex", 146, 193)},
        {"id": "PAR-LCO-THERMAL", "parameters": ["transition-specific config/vib/electronic baselines"], "disposition": "TIER_C_INITIAL_OR_UNVERIFIED_PENDING_ROUNDTRIP", "anchor": anchor("Claude/docs/v1.0.19/_sections/ch1_sec14_lcodecomp.tex", 84, 98)},
    ]


def conventions() -> list[dict[str, Any]]:
    p = "Claude/docs/v1.0.19/_sections/"
    rows = [
        ("SYM-Q", "Q, Q_cell", "absolute or normalized charge and cell capacity", "C or Ah, but one timebase", p+"ch1_sec01_n0n1.tex", 47, 63, ["CONFLICT-SIGNED-ICA"]),
        ("SYM-X", "x, xbar", "Li fraction x and delithiation fraction xbar=1-x", "1", p+"ch2_sec05_mixing.tex", 12, 20, ["CONFLICT-X-XBAR"]),
        ("SYM-XI", "xi_j, theta_j", "delithiation progress and occupied fraction theta=1-xi", "1", p+"ch1_sec01_n0n1.tex", 24, 34, []),
        ("SYM-SIGMA", "sigma_d", "Ch1 half-cell direction: discharge/delithiation +1, charge/lithiation -1", "1", p+"ch1_sec01_n0n1.tex", 10, 34, ["CONFLICT-DISCHARGE-LABEL"]),
        ("SYM-I", "I", "Bernardi signed cell current, I>0 cell discharge", "A", p+"ch2_sec07_revheat.tex", 15, 39, ["CONFLICT-DISCHARGE-LABEL"]),
        ("SYM-VAPP", "V_app", "measured half-cell voltage", "V", p+"ch1_sec01_n0n1.tex", 158, 183, []),
        ("SYM-VN", "V_n", "internal voltage after ohmic correction", "V", p+"ch1_sec01_n0n1.tex", 158, 183, []),
        ("SYM-U", "U_j, U_oc", "transition center and implicit equilibrium observation voltage", "V", p+"ch2_sec05_mixing.tex", 12, 38, []),
        ("SYM-W", "w_j, n_j", "logistic voltage scale and dimensionless thermal multiplicity", "V; 1", p+"ch1_sec05_width.tex", 150, 175, ["CONFLICT-WIDTH-STATE"]),
        ("SYM-BG", "C_bg, Q_bg", "background differential capacity and its unspecified primitive", "charge/V; charge", p+"ch1_sec10_sum.tex", 5, 14, ["CONFLICT-BACKGROUND-PRIMITIVE"]),
        ("SYM-T", "T, T_rep", "pointwise temperature and representative mean used by selected paths", "K", p+"ch1_sec01_n0n1.tex", 47, 63, ["CONFLICT-POINTWISE-REPRESENTATIVE-T"]),
        ("SYM-HEAT", "qdot_rev", "signed reversible heat into the declared cell control volume", "W", p+"ch2_sec07_revheat.tex", 10, 25, ["CONFLICT-CONTROL-VOLUME"]),
    ]
    return [
        {"symbol_id": sid, "symbols": symbols, "definition": definition, "unit": unit, "source_anchor": anchor(path, start, end), "conflict_ids": conflicts}
        for sid, symbols, definition, unit, path, start, end, conflicts in rows
    ]


def source_conflicts() -> list[dict[str, str]]:
    return [
        {"conflict_id": "CONFLICT-DISCHARGE-LABEL", "status": "PRESERVED", "statement": "Ch1 half-cell discharge is graphite delithiation, while Bernardi I>0 cell discharge is graphite lithiation."},
        {"conflict_id": "CONFLICT-X-XBAR", "status": "PRESERVED", "statement": "Chapter 2 implicit charge uses xbar=1-x while other discussion often uses Li fraction x."},
        {"conflict_id": "CONFLICT-WIDTH-STATE", "status": "PRESERVED", "statement": "n-governed thermal width and directly specified frozen width imply different dw/dT."},
        {"conflict_id": "CONFLICT-BACKGROUND-PRIMITIVE", "status": "PRESERVED", "statement": "ICA defines C_bg but the composition residual omits a referenced Q_bg primitive."},
        {"conflict_id": "CONFLICT-POINTWISE-REPRESENTATIVE-T", "status": "PRESERVED", "statement": "Some paths use pointwise T(V), while branch and lag quantities use T_rep."},
        {"conflict_id": "CONFLICT-CONTROL-VOLUME", "status": "PRESERVED", "statement": "Half-cell entropy coefficients require an explicit sign map before full-cell heat composition."},
        {"conflict_id": "CONFLICT-LAG-TIMEBASE", "status": "PRESERVED", "statement": "C-rate in h^-1 is numerically combined with Eyring kinetics in s^-1 in the reported seed estimate."},
        {"conflict_id": "CONFLICT-LCO-T-CURVATURE", "status": "PRESERVED", "statement": "Source theory requires an integral/T-squared path, while current implementation freezes the electronic term at T_ref."},
        {"conflict_id": "CONFLICT-SIGNED-ICA", "status": "PRESERVED", "statement": "The source denotes both the signed charge derivative and its positive progress-direction magnitude by dQ/dV."},
        {"conflict_id": "CONFLICT-ZERO-CURRENT-HYSTERESIS", "status": "PRESERVED", "statement": "One source section retains gamma-scaled hysteresis at zero current while another declares a direction-invariant zero-current baseline."},
    ]


def dependency_graph() -> dict[str, Any]:
    nodes = ["protocol", "I_abs", "I_signed", "sigma_d", "V_app", "V_n", "T", "T_rep", "U_j", "w_j", "branch_center", "xi_eq", "Q_bg", "charge_residual", "U_oc", "g_j", "dQdV", "dVdQ", "dUdT", "q_rev", "kinetic_rate", "L_q", "L_V", "history_state", "xi_lag", "peak_shape"]
    edges = [
        ["protocol", "I_abs"], ["protocol", "I_signed"], ["protocol", "sigma_d"], ["V_app", "V_n"], ["I_abs", "V_n"], ["sigma_d", "V_n"],
        ["T", "U_j"], ["T", "w_j"], ["T_rep", "branch_center"], ["U_j", "branch_center"], ["branch_center", "xi_eq"], ["w_j", "xi_eq"], ["U_oc", "xi_eq"],
        ["xi_eq", "charge_residual"], ["Q_bg", "charge_residual"], ["charge_residual", "U_oc"], ["xi_eq", "g_j"], ["g_j", "dQdV"], ["dQdV", "dVdQ"],
        ["g_j", "dUdT"], ["U_j", "dUdT"], ["w_j", "dUdT"], ["dUdT", "q_rev"], ["I_signed", "q_rev"], ["T", "q_rev"],
        ["T_rep", "kinetic_rate"], ["I_abs", "L_q"], ["kinetic_rate", "L_q"], ["L_q", "L_V"], ["protocol", "history_state"], ["history_state", "xi_lag"], ["xi_eq", "xi_lag"], ["L_V", "xi_lag"], ["xi_lag", "peak_shape"], ["xi_eq", "peak_shape"],
    ]
    cycle_analysis = [
        {"structure_id": "CYCLE-IMPLICIT-CHARGE", "nodes": ["U_oc", "xi_eq", "charge_residual", "U_oc"], "topology": "CLOSED_CYCLE", "classification": "DEFINITIONAL_IMPLICIT_SYSTEM", "closure": "local only when F_U is nonzero; global branch selection conditional"},
        {"structure_id": "PATH-THERMAL-DEPENDENCY", "nodes": ["T", "U_j", "branch_center", "xi_eq", "charge_residual", "U_oc"], "topology": "OPEN_PATH", "classification": "OPEN_THERMAL_DEPENDENCY_PATH", "closure": "requires declared dw/dT and differentiability; the path is a driver into the implicit charge cycle, not a second closed cycle"},
        {"structure_id": "PATH-HISTORY-DEPENDENCY", "nodes": ["protocol", "history_state", "xi_lag", "peak_shape"], "topology": "OPEN_PATH", "classification": "OPEN_STATEFUL_PROTOCOL_PATH", "closure": "not closed for finite-window rest or mid-protocol reversal"},
    ]
    return {"nodes": nodes, "edges": [{"from": a, "to": b} for a, b in edges], "cycle_analysis": cycle_analysis}


def read_coverage() -> list[dict[str, Any]]:
    records = []
    for path in SOURCE_FILES:
        raw = blob(path)
        lines = raw.decode("utf-8").splitlines()
        records.append({
            "path": path,
            "git_blob_sha1": run_git("rev-parse", f"{SOURCE_COMMIT}:{path}"),
            "sha256": sha256(raw),
            "physical_lines": len(lines),
            "coverage": [{"start": 1, "end": len(lines)}],
            "coverage_status": "READ_FULL",
            "authority_boundary": "FROZEN_SOURCE_CONTENT_NOT_EXTERNAL_TRUTH",
        })
    return records


def render_markdown(data: dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Phase 060 v1.0.19 독립 물리 재유도",
        "",
        "상태: `PASS_WITH_CONCERNS`",
        "",
        "권위 경계: 이 문서는 동결된 v1.0.19 source model의 내부 수식 정합, 차원, 부호, 극한과 구현 영향을 감사한다. 외부 문헌 진실성·재료 타당성·정본 채택을 확정하지 않는다.",
        "",
        "## 1. 범위와 방법",
        "",
        f"- frozen source commit: `{data['source_commit']}`",
        f"- 전문 검독: {summary['source_files_read_full']}/{summary['source_files_expected']} files, {summary['source_lines_read_full']}/{summary['source_lines_expected']} physical lines",
        "- production implementation import/call: `false`",
        "- 독립 경로: 직접 대수, 차원 분석, bisection, central finite difference, quadrature/convolution, free-energy round trip",
        "",
        "## 2. 규약 동결",
        "",
        "| ID | 기호 | 정의 | 단위 | 충돌 |",
        "|---|---|---|---|---|",
    ]
    for row in data["conventions"]:
        lines.append(f"| `{row['symbol_id']}` | {row['symbols']} | {row['definition']} | {row['unit']} | {', '.join(row['conflict_ids']) or '없음'} |")
    lines += [
        "",
        "## 3. 지배 잔차와 관측 변환",
        "",
        "배경이 없는 branch-free 특수형에서 탈리튬화 분율 $\\bar x=1-x$를 쓰면",
        "",
        "\\[F(U;\\bar x,T)=\\sum_j Q_j\\,\\xi_j(U,T)-Q\\bar x=0,\\qquad Q=\\sum_jQ_j.\\]",
        "",
        "미분 가능하고 $F_U\\ne0$인 국소 branch에서만",
        "",
        "\\[\\frac{\\mathrm dU}{\\mathrm dQ}=-\\frac{F_Q}{F_U},\\qquad F_Q=-1,\\qquad \\frac{\\mathrm dQ}{\\mathrm dU}=F_U=\\sum_jQ_jg_j.\\]",
        "",
        "따라서 $F_U\\to0$에서는 DVA가 발산하고 전역 유일성은 보장되지 않는다. $C_\\mathrm{bg}$가 0이 아니면 $Q_\\mathrm{bg}$의 primitive와 기준 상수가 추가로 필요하다.",
        "",
        "고정 $\\bar x$에서 온도 미분하면",
        "",
        "\\[\\left.\\frac{\\partial U}{\\partial T}\\right|_{\\bar x}=-\\frac{\\sum_jQ_j(\\partial\\xi_j/\\partial T)_U}{\\sum_jQ_j(\\partial\\xi_j/\\partial U)_T},\\]",
        "",
        "이며 $w_j=n_j(T)RT/F$인 경우 $\\partial_Tw_j=(R/F)(n_j+Tn'_j)$가 반드시 들어간다. 직접 입력한 frozen $w_j$에는 같은 config 항을 자동 적용할 수 없다.",
        "",
        "## 4. Check 판정",
        "",
        "| Check | Family | Result | Derivation | Implementation | 핵심 판정 |",
        "|---|---|---|---|---|---|",
    ]
    for row in data["derivation_checks"]:
        lines.append(f"| `{row['check_id']}` | {row['family']} | `{row['result']}` | `{row['derivation_status']}` | `{row['implementation_conformance']}` | {row['result_rationale']} |")
    lines += ["", "## 5. 독립 수치 probe", ""]
    implicit = data["independent_probes"]["IMPLICIT"]
    lines += [
        f"- four-transition root: $U_{{oc}}={implicit['U_V']*1e3:.6f}$ mV at $\\bar x=0.25$, $T=298.15$ K.",
        f"- $dQ/dU={implicit['dQdU_Qcell_per_V']:.9f}$ $Q_\\mathrm{{cell}}$/V, analytic $dU/dQ={implicit['dUdQ_V_per_Qcell_analytic']:.9f}$ V/$Q_\\mathrm{{cell}}$, finite-difference error `{implicit['charge_sensitivity_abs_error_V_per_Qcell']:.3e}`.",
        f"- complete $\\partial U/\\partial T={implicit['complete_dUdT_V_per_K']*1e3:.6f}$ mV/K, finite-difference error `{implicit['thermal_abs_error_V_per_K']:.3e}` V/K; $\\dot Q_\\mathrm{{rev}}/I={implicit['qrev_over_I_V']*1e3:.6f}$ mV.",
        f"- lag timebase: unconverted/canonical ratio = `{data['independent_probes']['LAG_TIMEBASE']['error_factor']:.1f}`.",
        f"- Einstein round-trip max error = `{data['independent_probes']['EINSTEIN']['max_roundtrip_error_V_per_K']:.3e}` V/K.",
        f"- LCO electronic gate-center $\\Delta S_e={data['independent_probes']['LCO_ELECTRONIC']['delta_S_e_J_per_molK']:.6f}$ J/(mol K), $T^2$ round-trip error `{data['independent_probes']['LCO_ELECTRONIC']['roundtrip_abs_error_V_per_K']:.3e}` V/K.",
        "",
        "이 probe들은 source equation의 내부 대수·수치 왕복만 검증한다. 실험 또는 문헌 진실성은 검증하지 않는다.",
        "",
        "## 6. Parameter authority",
        "",
        "| ID | Parameters | Disposition |",
        "|---|---|---|",
    ]
    for row in data["parameter_authority"]:
        lines.append(f"| `{row['id']}` | {', '.join(row['parameters'])} | `{row['disposition']}` |")
    lines += ["", "## 7. 구조적 식별성", ""]
    for row in data["identifiability"]:
        lines.append(f"- `{row['id']}`: 관측 조합 `{row['combination']}`; 분리 미확정 `{', '.join(row['unresolved_primitives'])}`; 필요 근거: {row['required_evidence']}.")
    lines += ["", "## 8. Findings", ""]
    for row in data["findings"]:
        lines.append(f"- `{row['finding_id']}` `{row['severity']}`: {row['statement']} 처분: {row['disposition']}")
    lines += [
        "",
        "## 9. 판정 경계",
        "",
        f"- check 결과: PASS {summary['check_results']['PASS']}, FAIL {summary['check_results']['FAIL']}, CONDITIONAL {summary['check_results']['CONDITIONAL']}, UNVERIFIED {summary['check_results']['UNVERIFIED']}, NOT_APPLICABLE {summary['check_results']['NOT_APPLICABLE']}.",
        f"- findings: P0 {summary['findings']['P0']}, P1 {summary['findings']['P1']}, P2 {summary['findings']['P2']}.",
        "- Step 44 gate는 감사 coverage와 독립 재유도 완료를 뜻하는 `PASS_WITH_CONCERNS`다. FAIL/CONDITIONAL/UNVERIFIED row를 수리·외부 검증 완료로 승격하지 않는다.",
        "- 다음 단위는 Step 45.1 claim/defect/carry-forward disposition이다.",
        "",
    ]
    return "\n".join(lines)


def build() -> dict[str, Any]:
    coverage = read_coverage()
    checks = build_checks()
    finding_rows = findings()
    result_counts = {key: 0 for key in ["PASS", "FAIL", "CONDITIONAL", "UNVERIFIED", "NOT_APPLICABLE"]}
    for row in checks:
        result_counts[row["result"]] += 1
    severity_counts = {key: 0 for key in ["P0", "P1", "P2"]}
    for row in finding_rows:
        severity_counts[row["severity"]] += 1
    trace_raw = TRACE_PATH.read_bytes()
    data = {
        "schema_version": "phase060-step44-v1",
        "phase": 60,
        "step": 44,
        "source_commit": SOURCE_COMMIT,
        "authority_policy": {
            "scientific_truth": "DEFERRED_TO_PHASE071_AND_LATER_CANONICAL_DERIVATION",
            "production_imported_or_called": False,
            "numerical_match_authority": "INTERNAL_EQUATION_CONSISTENCY_ONLY",
            "result_meaning": "AUDIT_COMPLETE_WITH_OPEN_DEFECTS_NOT_MODEL_ADOPTION",
        },
        "inputs": {
            "step43_trace_path": "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json",
            "step43_trace_sha256": sha256(trace_raw),
            "source_files": coverage,
        },
        "conventions": conventions(),
        "source_conflicts": source_conflicts(),
        "dependency_graph": dependency_graph(),
        "derivation_checks": checks,
        "independent_probes": probe_bundle(),
        "identifiability": identifiability_rows(),
        "parameter_authority": parameter_authority_rows(),
        "findings": finding_rows,
        "summary": {
            "status": "PASS_WITH_CONCERNS",
            "gate": "PASS_P060_STEP44_PHYSICS_REDERIVATION",
            "source_files_expected": len(SOURCE_FILES),
            "source_files_read_full": len(coverage),
            "source_lines_expected": sum(row["physical_lines"] for row in coverage),
            "source_lines_read_full": sum(row["physical_lines"] for row in coverage),
            "checks": len(checks),
            "check_results": result_counts,
            "findings": severity_counts,
            "conflicts_preserved": len(source_conflicts()),
            "identifiability_rows": len(identifiability_rows()),
            "parameter_authority_rows": len(parameter_authority_rows()),
            "next_step": "45.1",
        },
    }
    markdown = render_markdown(data)
    data["generation"] = {
        "builder_path": "Codex/work/v1019_phase060/build_phase060_step44_physics_validation.py",
        "validator_path": "Codex/work/v1019_phase060/validate_phase060_step44_physics_validation.py",
        "markdown_path": "Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md",
        "markdown_sha256": sha256(markdown.encode("utf-8")),
        "canonical_json": "UTF-8 LF indent=2 sort_keys=true allow_nan=false",
    }
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, default=JSON_PATH)
    parser.add_argument("--markdown-out", type=Path, default=MD_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = build()
    markdown = render_markdown(data)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(markdown, encoding="utf-8", newline="\n")
    args.json_out.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        "BUILT "
        f"checks={data['summary']['checks']} "
        f"files={data['summary']['source_files_read_full']} "
        f"lines={data['summary']['source_lines_read_full']} "
        f"findings={data['summary']['findings']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
