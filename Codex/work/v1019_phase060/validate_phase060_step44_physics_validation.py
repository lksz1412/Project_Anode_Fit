#!/usr/bin/env python3
"""Strict validator for Phase 060 Step 44 physics evidence.

The frozen production module is never imported or called.  This program checks
Git-blob provenance, schemas, derivation dispositions, independent numerical
witnesses, deterministic generation, and controlled negative mutations.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json"
MARKDOWN = ROOT / "Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md"
BUILDER = ROOT / "Codex/work/v1019_phase060/build_phase060_step44_physics_validation.py"
TRACE = ROOT / "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
R, FARADAY, KB, EV_J = 8.31446261815324, 96485.33212, 1.380649e-23, 1.602176634e-19

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
EXPECTED_RESULTS = {
    **{f"P060-PHY-{i:03d}": result for i, result in enumerate([
        "CONDITIONAL", "PASS", "FAIL", "PASS", "CONDITIONAL", "PASS",
        "CONDITIONAL", "FAIL", "CONDITIONAL", "FAIL", "PASS", "FAIL",
        "CONDITIONAL", "PASS", "FAIL", "CONDITIONAL", "CONDITIONAL",
        "CONDITIONAL", "UNVERIFIED", "UNVERIFIED", "CONDITIONAL", "FAIL",
    ], 1)}
}
RESULT_COUNTS = {"PASS": 5, "FAIL": 6, "CONDITIONAL": 9, "UNVERIFIED": 2, "NOT_APPLICABLE": 0}
SEVERITY_COUNTS = {"P0": 0, "P1": 12, "P2": 8}
PROBE_IDS = {"LOGISTIC", "IMPLICIT", "HYSTERESIS", "CAUSAL_MEMORY", "EINSTEIN", "LCO_ELECTRONIC", "LAG_TIMEBASE"}
SEMANTIC_DIGESTS = {
    "trace": "2410791de926c26363a4f5ec95edad7e745072ee00e281a61666d3b427620a88",
    "conventions": "3bdf3a0acbb5a2bc18012642fdf9285e47e1c668074f1a8cd84a098b4445971a",
    "identifiability": "109e843734d6fda0860702e9a7a920f352e4645dc1065f716eaec4edd2bdd045",
    "parameter_authority": "73b883d158d7f01d88ef40f62b5333a73003ce2e94e191cf66a6ebfcbf3fa582",
    "findings": "f47b329a829c6c1358bd1975c85bc712cdfbfda51d30b669273e13ae39e987d3",
    "check_semantics": "398011ff23b4a8720e485cebb5644f15b7b189d7379acbd997aab5ed786e9156",
    "independent_probes": "5fb0ea83a2aa14dc838157e42544e60e8f3c0b0dba9bb2fe23974d254b6895b1",
}
PROBE_SCHEMAS = {
    "LOGISTIC": {"T_K", "w_V", "center_xi", "analytic_peak_height_per_V", "finite_difference_peak_height_per_V", "truncated_area", "area_abs_error"},
    "IMPLICIT": {"T_K", "xbar", "U_V", "target_charge_Qcell", "F_U_Qcell_per_V", "dQdU_Qcell_per_V", "dUdQ_V_per_Qcell_analytic", "dUdQ_V_per_Qcell_fd", "reciprocal_product", "simple_dUdT_V_per_K", "complete_dUdT_V_per_K", "finite_difference_dUdT_V_per_K", "thermal_abs_error_V_per_K", "charge_sensitivity_abs_error_V_per_Qcell", "qrev_over_I_V", "transition_states"},
    "HYSTERESIS": {"T_K", "critical_Omega_J_per_mol", "gap_below_V", "gap_at_critical_V", "gap_near_above_V", "gap_at_4RT_V", "positive_above"},
    "CAUSAL_MEMORY": {"w_arbitrary", "L_over_w", "grid_step_over_w", "kernel_normalization_exact", "minimum_discharge_peak", "minimum_charge_peak", "mirror_max_abs_error", "small_L_max_abs_error_per_w"},
    "EINSTEIN": {"theta_E_K", "T_ref_K", "delta_S_at_ref_J_per_molK", "delta_U_at_ref_V", "samples", "max_roundtrip_error_V_per_K"},
    "LCO_ELECTRONIC": {"T_K", "T_ref_K", "gmax_states_per_eV_atom", "delta_x", "sigma_center", "a_e_J_per_molK2", "delta_S_e_J_per_molK", "dU_dT_V_per_K", "finite_difference_T2_dU_dT_V_per_K", "roundtrip_abs_error_V_per_K"},
    "LAG_TIMEBASE": {"c_rate_per_hour", "k_per_second", "dimensionally_closed_Lq", "unconverted_numeric_Lq", "error_factor"},
}
EXPECTED_EDGES = {
    ("protocol", "I_abs"), ("protocol", "I_signed"), ("protocol", "sigma_d"), ("V_app", "V_n"),
    ("I_abs", "V_n"), ("sigma_d", "V_n"), ("T", "U_j"), ("T", "w_j"),
    ("T_rep", "branch_center"), ("U_j", "branch_center"), ("branch_center", "xi_eq"),
    ("w_j", "xi_eq"), ("U_oc", "xi_eq"), ("xi_eq", "charge_residual"),
    ("Q_bg", "charge_residual"), ("charge_residual", "U_oc"), ("xi_eq", "g_j"),
    ("g_j", "dQdV"), ("dQdV", "dVdQ"), ("g_j", "dUdT"), ("U_j", "dUdT"),
    ("w_j", "dUdT"), ("dUdT", "q_rev"), ("I_signed", "q_rev"), ("T", "q_rev"),
    ("T_rep", "kinetic_rate"), ("I_abs", "L_q"), ("kinetic_rate", "L_q"),
    ("L_q", "L_V"), ("protocol", "history_state"), ("history_state", "xi_lag"),
    ("xi_eq", "xi_lag"), ("L_V", "xi_lag"), ("xi_lag", "peak_shape"),
    ("xi_eq", "peak_shape"),
}


class DuplicateKey(ValueError):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def semantic_digest(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return sha(raw)


def pairs_unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value}")


def strict_load(raw: bytes) -> dict[str, Any]:
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_unique, parse_constant=reject_constant)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON is not an object")
    return data


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def keys(errors: list[str], obj: Any, expected: set[str], path: str) -> bool:
    if not isinstance(obj, dict):
        errors.append(f"{path}: not an object")
        return False
    if set(obj) != expected:
        errors.append(f"{path}: exact-key mismatch")
        return False
    return True


def text(errors: list[str], value: Any, path: str) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: empty/non-string")


def finite(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        errors.append(f"{path}: non-finite")
    elif isinstance(value, dict):
        for key, child in value.items():
            finite(child, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            finite(child, f"{path}[{index}]", errors)


def source_truth() -> tuple[dict[str, dict[str, Any]], set[str], bytes]:
    truth: dict[str, dict[str, Any]] = {}
    for path in SOURCE_FILES:
        raw = git_bytes("show", f"{SOURCE_COMMIT}:{path}")
        truth[path] = {
            "raw": raw,
            "lines": raw.decode("utf-8").splitlines(),
            "blob": git_text("rev-parse", f"{SOURCE_COMMIT}:{path}"),
            "sha": sha(raw),
        }
    trace_raw = TRACE.read_bytes()
    trace_data = strict_load(trace_raw)
    trace_ids = {row["trace_id"] for row in trace_data["trace_rows"]}
    return truth, trace_ids, trace_raw


def ast_policy_errors() -> list[str]:
    errors: list[str] = []
    allowed = {
        "__future__", "argparse", "ast", "copy", "hashlib", "json", "math",
        "subprocess", "sys", "tempfile", "collections", "pathlib", "typing",
    }
    for path in (BUILDER, Path(__file__).resolve()):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [(node.module or "").split(".")[0]]
            else:
                modules = []
            for module in modules:
                if module not in allowed:
                    errors.append(f"AST import policy: {path.name} imports {module}")
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in {"__import__", "exec", "eval", "import_module", "run_module", "run_path"}:
                    errors.append(f"AST dynamic execution policy: {path.name} calls {name}")
        source_text = path.read_text(encoding="utf-8")
        if ("Anode_Fit_v1.0.19" + ".py") in source_text or ("Claude" + ".docs") in source_text:
            errors.append(f"AST production-path policy: {path.name} names production Python")
    return errors


def anchor(errors: list[str], row: Any, path: str, truth: dict[str, dict[str, Any]]) -> None:
    expected = {"anchor_id", "path", "start_line", "end_line", "git_blob_sha1", "slice_sha256"}
    if not keys(errors, row, expected, path):
        return
    source = row["path"]
    if source not in truth:
        errors.append(f"{path}: unknown source")
        return
    start, end, lines = row["start_line"], row["end_line"], truth[source]["lines"]
    if not isinstance(start, int) or not isinstance(end, int) or not 1 <= start <= end <= len(lines):
        errors.append(f"{path}: invalid interval")
        return
    slice_sha = sha("\n".join(lines[start - 1:end]).encode("utf-8"))
    if row["anchor_id"] != f"SRC:{source}:{start}-{end}" or row["git_blob_sha1"] != truth[source]["blob"] or row["slice_sha256"] != slice_sha:
        errors.append(f"{path}: frozen anchor fingerprint mismatch")


def close(actual: Any, expected: float, tolerance: float) -> bool:
    return isinstance(actual, (int, float)) and math.isfinite(actual) and abs(actual - expected) <= tolerance


def logistic(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def numeric_errors(probes: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(probes, dict) or set(probes) != PROBE_IDS:
        return ["independent_probes: exact IDs mismatch"]
    for probe_id, expected_keys in PROBE_SCHEMAS.items():
        if not isinstance(probes[probe_id], dict) or set(probes[probe_id]) != expected_keys:
            errors.append(f"{probe_id}: exact schema mismatch")
    if errors:
        return errors
    implicit_state_keys = {"name", "center_V", "width_V", "xi", "g_per_V", "weight", "config_V_per_K"}
    if len(probes["IMPLICIT"]["transition_states"]) != 4 or any(
        not isinstance(row, dict) or set(row) != implicit_state_keys
        for row in probes["IMPLICIT"]["transition_states"]
    ):
        errors.append("IMPLICIT.transition_states: exact schema/count mismatch")
    einstein_sample_keys = {"T_K", "delta_S_J_per_molK", "analytic_dU_dT_V_per_K", "finite_difference_dU_dT_V_per_K", "abs_error_V_per_K"}
    if len(probes["EINSTEIN"]["samples"]) != 4 or any(
        not isinstance(row, dict) or set(row) != einstein_sample_keys
        for row in probes["EINSTEIN"]["samples"]
    ):
        errors.append("EINSTEIN.samples: exact schema/count mismatch")
    lp = probes["LOGISTIC"]
    width = R * 298.15 / FARADAY
    height = 1.0 / (4.0 * width)
    exact_area = logistic(20.0) - logistic(-20.0)
    if not close(lp.get("T_K"), 298.15, 1e-14) or not close(lp.get("w_V"), width, 1e-15) or not close(lp.get("center_xi"), .5, 1e-15):
        errors.append("LOGISTIC width/center")
    if not close(lp.get("analytic_peak_height_per_V"), height, 1e-11) or abs(lp.get("finite_difference_peak_height_per_V", 0)-height) > 1e-5:
        errors.append("LOGISTIC height")
    if not close(lp.get("truncated_area"), exact_area, 2e-12) or not close(lp.get("area_abs_error"), abs(1-lp.get("truncated_area", math.inf)), 2e-15) or lp.get("area_abs_error", math.inf) > 1e-8:
        errors.append("LOGISTIC area")

    transitions = [(-11700., 29., .10), (-13500., 0., .12), (-13100., -5., .25), (-13000., -16., .50)]
    target = sum(q for _, _, q in transitions) * .25

    def residual(u: float, temp: float, requested_target: float = target) -> float:
        w = R * temp / FARADAY
        return sum(q * logistic((u - (-dh + temp*ds)/FARADAY)/w) for dh, ds, q in transitions) - requested_target

    def solve(temp: float, requested_target: float = target) -> float:
        lo, hi = -1., 1.
        for _ in range(120):
            mid = (lo+hi)/2
            if residual(mid, temp, requested_target) < 0: lo = mid
            else: hi = mid
        return (lo+hi)/2

    ip, temp = probes["IMPLICIT"], 298.15
    u, w = solve(temp), R*temp/FARADAY
    state = []
    for dh, ds, q in transitions:
        z = (u - (-dh+temp*ds)/FARADAY)/w
        state.append((z, logistic(z)*(1-logistic(z))/w, q, ds))
    f_u = sum(q*g for z, g, q, ds in state)
    complete = sum(q*g/f_u*(ds/FARADAY + R/FARADAY*z) for z, g, q, ds in state)
    simple = sum(q*g/f_u*(ds/FARADAY) for z, g, q, ds in state)
    fd = (solve(temp+1e-3)-solve(temp-1e-3))/2e-3
    fd_q = (solve(temp, target+1e-7)-solve(temp, target-1e-7))/2e-7
    for name, actual, expected, tol in [
        ("T", ip.get("T_K"), temp, 1e-14), ("xbar", ip.get("xbar"), .25, 1e-15),
        ("target", ip.get("target_charge_Qcell"), target, 1e-15),
        ("root", ip.get("U_V"), u, 2e-15), ("F_U", ip.get("F_U_Qcell_per_V"), f_u, 2e-12),
        ("dQdU", ip.get("dQdU_Qcell_per_V"), f_u, 2e-12),
        ("dUdQ", ip.get("dUdQ_V_per_Qcell_analytic"), 1/f_u, 2e-12),
        ("dUdQ-fd", ip.get("dUdQ_V_per_Qcell_fd"), fd_q, 2e-10),
        ("simple-dUdT", ip.get("simple_dUdT_V_per_K"), simple, 2e-14),
        ("dUdT", ip.get("complete_dUdT_V_per_K"), complete, 2e-14),
        ("dUdT-fd", ip.get("finite_difference_dUdT_V_per_K"), fd, 2e-14),
        ("qrev", ip.get("qrev_over_I_V"), -temp*complete, 2e-14),
    ]:
        if not close(actual, expected, tol): errors.append(f"IMPLICIT {name}")
    if abs(fd-complete) > 2e-11 or not close(ip.get("thermal_abs_error_V_per_K"), abs(complete-fd), 2e-16) or not close(ip.get("charge_sensitivity_abs_error_V_per_Qcell"), abs(1/f_u-fd_q), 2e-12) or not close(ip.get("reciprocal_product"), 1., 1e-14):
        errors.append("IMPLICIT finite-difference/reciprocal")
    expected_names = ["4->3", "3->2L", "2L->2", "2->1"]
    for row, expected_name, (dh, ds, q), (z, g, _, _) in zip(ip["transition_states"], expected_names, transitions, state):
        center = (-dh+temp*ds)/FARADAY
        if row.get("name") != expected_name or not close(row.get("center_V"), center, 2e-15) or not close(row.get("width_V"), w, 2e-15) or not close(row.get("xi"), logistic(z), 2e-15) or not close(row.get("g_per_V"), g, 2e-12) or not close(row.get("weight"), q*g/f_u, 2e-14) or not close(row.get("config_V_per_K"), R/FARADAY*z, 2e-14):
            errors.append("IMPLICIT transition-state witness mismatch")

    hp = probes["HYSTERESIS"]
    critical = 2*R*298.15
    def gap(omega: float) -> float:
        if omega <= critical: return 0.0
        u = math.sqrt(1-critical/omega)
        return 2*(omega*u-critical*math.atanh(u))/FARADAY
    if not close(hp.get("T_K"), 298.15, 1e-14) or not close(hp.get("critical_Omega_J_per_mol"), critical, 1e-10) or hp.get("gap_below_V") != 0 or hp.get("gap_at_critical_V") != 0 or not close(hp.get("gap_near_above_V"), gap(critical*(1+1e-8)), 1e-18) or not close(hp.get("gap_at_4RT_V"), gap(4*R*298.15), 1e-14) or hp.get("positive_above") != 1.0:
        errors.append("HYSTERESIS threshold/gap")

    cp = probes["CAUSAL_MEMORY"]
    if cp.get("w_arbitrary") != 1.0 or cp.get("L_over_w") != .02 or cp.get("grid_step_over_w") != .001 or cp.get("kernel_normalization_exact") != 1.0 or cp.get("minimum_discharge_peak", -1) < -1e-10 or cp.get("minimum_charge_peak", -1) < -1e-10 or cp.get("mirror_max_abs_error", math.inf) > 1e-11 or cp.get("small_L_max_abs_error_per_w", math.inf) > .004:
        errors.append("CAUSAL_MEMORY normalization/positivity/mirror/limit")

    ep = probes["EINSTEIN"]
    if ep.get("theta_E_K") != 700.0 or ep.get("T_ref_K") != 298.15 or abs(ep.get("delta_S_at_ref_J_per_molK", math.inf)) > 1e-14 or abs(ep.get("delta_U_at_ref_V", math.inf)) > 1e-14 or ep.get("max_roundtrip_error_V_per_K", math.inf) > 1e-12:
        errors.append("EINSTEIN reference/roundtrip")
    samples = ep.get("samples", [])
    expected_uv = [-3.738, 0., 3.700, 9.138]
    if len(samples) != 4 or [row.get("T_K") for row in samples] != [278.15, 298.15, 318.15, 348.15] or any(abs(row.get("analytic_dU_dT_V_per_K", math.inf)*1e6-exp) > .001 or not close(row.get("analytic_dU_dT_V_per_K"), row.get("delta_S_J_per_molK", math.inf)/FARADAY, 2e-15) or not close(row.get("abs_error_V_per_K"), abs(row.get("analytic_dU_dT_V_per_K", math.inf)-row.get("finite_difference_dU_dT_V_per_K", -math.inf)), 2e-18) for row, exp in zip(samples, expected_uv)):
        errors.append("EINSTEIN slope samples")

    xp = probes["LCO_ELECTRONIC"]
    ae = -(math.pi**2/3)*R*(KB/EV_J)*(13/.05)*.25
    if xp.get("T_K") != 300.0 or xp.get("T_ref_K") != 298.15 or xp.get("gmax_states_per_eV_atom") != 13.0 or xp.get("delta_x") != .05 or xp.get("sigma_center") != .5 or not close(xp.get("a_e_J_per_molK2"), ae, 1e-13) or not close(xp.get("delta_S_e_J_per_molK"), ae*300, 1e-10) or not close(xp.get("dU_dT_V_per_K"), ae*300/FARADAY, 2e-15) or not close(xp.get("finite_difference_T2_dU_dT_V_per_K"), xp.get("dU_dT_V_per_K", math.inf), 2e-12) or not close(xp.get("roundtrip_abs_error_V_per_K"), abs(xp.get("dU_dT_V_per_K", math.inf)-xp.get("finite_difference_T2_dU_dT_V_per_K", -math.inf)), 2e-18) or xp.get("delta_S_e_J_per_molK", 1) >= 0:
        errors.append("LCO_ELECTRONIC unit/sign/T2")

    lag = probes["LAG_TIMEBASE"]
    if lag.get("c_rate_per_hour") != .1 or lag.get("k_per_second") != 2.5 or not close(lag.get("dimensionally_closed_Lq"), (.1/3600)/2.5, 1e-18) or not close(lag.get("unconverted_numeric_Lq"), .1/2.5, 1e-16) or not close(lag.get("error_factor"), 3600., 1e-10):
        errors.append("LAG_TIMEBASE 3600 factor")
    if semantic_digest(probes) != SEMANTIC_DIGESTS["independent_probes"]:
        errors.append("independent_probes: exact canonical witness digest mismatch")
    return errors


def validate(data: dict[str, Any], truth: dict[str, dict[str, Any]], trace_ids: set[str], trace_raw: bytes, markdown_raw: bytes) -> list[str]:
    errors: list[str] = []
    finite(data, "$", errors)
    top = {"schema_version", "phase", "step", "source_commit", "authority_policy", "inputs", "conventions", "source_conflicts", "dependency_graph", "derivation_checks", "independent_probes", "identifiability", "parameter_authority", "findings", "summary", "generation"}
    keys(errors, data, top, "$")
    if (data.get("schema_version"), data.get("phase"), data.get("step"), data.get("source_commit")) != ("phase060-step44-v1", 60, 44, SOURCE_COMMIT):
        errors.append("identity tuple mismatch")

    policy = data.get("authority_policy")
    if keys(errors, policy, {"scientific_truth", "production_imported_or_called", "numerical_match_authority", "result_meaning"}, "authority_policy"):
        if policy != {"scientific_truth": "DEFERRED_TO_PHASE071_AND_LATER_CANONICAL_DERIVATION", "production_imported_or_called": False, "numerical_match_authority": "INTERNAL_EQUATION_CONSISTENCY_ONLY", "result_meaning": "AUDIT_COMPLETE_WITH_OPEN_DEFECTS_NOT_MODEL_ADOPTION"}:
            errors.append("authority_policy mismatch/promotion")

    inputs = data.get("inputs")
    if keys(errors, inputs, {"step43_trace_path", "step43_trace_sha256", "source_files"}, "inputs"):
        if inputs["step43_trace_path"] != "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json" or inputs["step43_trace_sha256"] != sha(trace_raw):
            errors.append("Step43 trace provenance mismatch")
        rows = inputs["source_files"]
        if not isinstance(rows, list) or len(rows) != 31 or [r.get("path") for r in rows] != SOURCE_FILES:
            errors.append("source coverage exact path/count mismatch")
        else:
            coverage_keys = {"path", "git_blob_sha1", "sha256", "physical_lines", "coverage", "coverage_status", "authority_boundary"}
            for i, row in enumerate(rows):
                p = f"inputs.source_files[{i}]"
                if not keys(errors, row, coverage_keys, p): continue
                t = truth[row["path"]]
                n = len(t["lines"])
                if row["git_blob_sha1"] != t["blob"] or row["sha256"] != t["sha"] or row["physical_lines"] != n or row["coverage"] != [{"start": 1, "end": n}] or row["coverage_status"] != "READ_FULL" or row["authority_boundary"] != "FROZEN_SOURCE_CONTENT_NOT_EXTERNAL_TRUTH":
                    errors.append(f"{p}: frozen READ_FULL proof mismatch")

    conflicts = data.get("source_conflicts")
    conflict_ids: set[str] = set()
    if not isinstance(conflicts, list) or len(conflicts) != 10:
        errors.append("source_conflicts count")
    else:
        for i, row in enumerate(conflicts):
            if keys(errors, row, {"conflict_id", "status", "statement"}, f"source_conflicts[{i}]"):
                conflict_ids.add(row["conflict_id"]); text(errors, row["statement"], f"source_conflicts[{i}].statement")
                if row["status"] != "PRESERVED": errors.append(f"source_conflicts[{i}].status")
        if len(conflict_ids) != 10 or not {"CONFLICT-SIGNED-ICA", "CONFLICT-ZERO-CURRENT-HYSTERESIS", "CONFLICT-LAG-TIMEBASE", "CONFLICT-LCO-T-CURVATURE"}.issubset(conflict_ids):
            errors.append("source_conflicts IDs")

    conventions = data.get("conventions")
    if not isinstance(conventions, list) or len(conventions) != 12:
        errors.append("conventions count")
    else:
        ids = []
        for i, row in enumerate(conventions):
            p = f"conventions[{i}]"
            if not keys(errors, row, {"symbol_id", "symbols", "definition", "unit", "source_anchor", "conflict_ids"}, p): continue
            ids.append(row["symbol_id"])
            for field in ("symbol_id", "symbols", "definition", "unit"): text(errors, row[field], f"{p}.{field}")
            anchor(errors, row["source_anchor"], f"{p}.source_anchor", truth)
            if not isinstance(row["conflict_ids"], list) or any(c not in conflict_ids for c in row["conflict_ids"]): errors.append(f"{p}.conflict_ids")
        if len(ids) != len(set(ids)): errors.append("duplicate convention ID")
        convention_semantics = [(r["symbol_id"], r["symbols"], r["definition"], r["unit"], r["conflict_ids"]) for r in conventions]
        if semantic_digest(convention_semantics) != SEMANTIC_DIGESTS["conventions"]:
            errors.append("conventions: exact semantic mapping mismatch")

    check_rows = data.get("derivation_checks")
    by_id: dict[str, dict[str, Any]] = {}
    check_keys = {"check_id", "family", "title", "equation_or_claim_ids", "source_anchors", "assumptions", "derivation_steps", "dimensions", "sign_convention", "domain", "analytic_limits", "independent_probe", "result", "derivation_status", "implementation_conformance", "implementation_impact", "result_rationale", "authority_boundary"}
    if not isinstance(check_rows, list) or len(check_rows) != 22:
        errors.append("derivation_checks count")
        check_rows = []
    for i, row in enumerate(check_rows):
        p = f"derivation_checks[{i}]"
        if not keys(errors, row, check_keys, p): continue
        cid = row["check_id"]
        if cid in by_id: errors.append(f"{p}: duplicate ID")
        by_id[cid] = row
        for field in ("family", "title", "sign_convention", "domain", "result_rationale"): text(errors, row[field], f"{p}.{field}")
        if row["authority_boundary"] != "INTERNAL_SOURCE_MODEL_REDERIVATION_NOT_EXTERNAL_SCIENTIFIC_TRUTH": errors.append(f"{p}.authority_boundary")
        if not isinstance(row["source_anchors"], list) or not row["source_anchors"]: errors.append(f"{p}.source_anchors")
        else:
            for j, item in enumerate(row["source_anchors"]): anchor(errors, item, f"{p}.source_anchors[{j}]", truth)
        if not isinstance(row["assumptions"], list) or not row["assumptions"] or not isinstance(row["dimensions"], dict) or not row["dimensions"]: errors.append(f"{p}: assumptions/dimensions empty")
        steps = row["derivation_steps"]
        if not isinstance(steps, list) or len(steps) < 3: errors.append(f"{p}.derivation_steps")
        else:
            for j, step in enumerate(steps):
                if keys(errors, step, {"ordinal", "statement"}, f"{p}.derivation_steps[{j}]"):
                    if step["ordinal"] != j+1: errors.append(f"{p}.derivation_steps[{j}].ordinal")
                    text(errors, step["statement"], f"{p}.derivation_steps[{j}].statement")
        for field in ("equation_or_claim_ids", "implementation_impact"):
            refs = row[field]
            if not isinstance(refs, list) or not refs or any(ref not in trace_ids for ref in refs): errors.append(f"{p}.{field}")
        probe = row["independent_probe"]
        if keys(errors, probe, {"probe_id", "status", "production_imported"}, f"{p}.independent_probe"):
            if probe["production_imported"] is not False: errors.append(f"{p}: production imported")
            if probe["probe_id"] is None and probe["status"] != "NOT_APPLICABLE": errors.append(f"{p}: probe N/A mismatch")
            if probe["probe_id"] is not None and (probe["probe_id"] not in PROBE_IDS or probe["status"] != "PASS"): errors.append(f"{p}: probe mismatch")
        if row["result"] not in RESULT_COUNTS or row["derivation_status"] not in {"CLOSED", "BOUNDED", "CONFLICTING", "NOT_DERIVABLE"} or row["implementation_conformance"] not in {"ALIGNED", "PARTIAL", "ABSENT", "MISALIGNED", "UNVERIFIED", "NOT_APPLICABLE"}: errors.append(f"{p}: enum mismatch")
    if set(by_id) != set(EXPECTED_RESULTS): errors.append("check ID set")
    for cid, expected in EXPECTED_RESULTS.items():
        if cid in by_id and by_id[cid]["result"] != expected: errors.append(f"{cid}: result promotion/change")
    if {k: Counter(r.get("result") for r in check_rows).get(k, 0) for k in RESULT_COUNTS} != RESULT_COUNTS: errors.append("check result counts")
    trace_semantics = [(r["check_id"], r["equation_or_claim_ids"], r["implementation_impact"]) for r in check_rows]
    check_semantics = [(r["check_id"], r["family"], r["title"], r["assumptions"], r["derivation_steps"], r["dimensions"], r["sign_convention"], r["domain"], r["analytic_limits"], r["result"], r["derivation_status"], r["implementation_conformance"], r["result_rationale"]) for r in check_rows]
    if semantic_digest(trace_semantics) != SEMANTIC_DIGESTS["trace"]:
        errors.append("checks: exact Step43 trace mapping mismatch")
    if semantic_digest(check_semantics) != SEMANTIC_DIGESTS["check_semantics"]:
        errors.append("checks: exact derivation semantics mismatch")

    findings = data.get("findings")
    covered: set[str] = set(); severities: Counter[str] = Counter(); finding_ids: set[str] = set()
    if not isinstance(findings, list) or len(findings) != 20:
        errors.append("findings count"); findings = []
    for i, row in enumerate(findings):
        p = f"findings[{i}]"
        if not keys(errors, row, {"finding_id", "severity", "check_ids", "statement", "disposition"}, p): continue
        if row["finding_id"] in finding_ids: errors.append(f"{p}: duplicate ID")
        finding_ids.add(row["finding_id"]); severities[row["severity"]] += 1
        refs = row["check_ids"]
        if row["severity"] not in SEVERITY_COUNTS or not isinstance(refs, list) or not refs or any(ref not in by_id for ref in refs): errors.append(f"{p}: severity/check refs")
        else: covered.update(refs)
        text(errors, row["statement"], f"{p}.statement"); text(errors, row["disposition"], f"{p}.disposition")
    if {k: severities.get(k, 0) for k in SEVERITY_COUNTS} != SEVERITY_COUNTS: errors.append("finding severity counts")
    nonpass = {cid for cid, result in EXPECTED_RESULTS.items() if result != "PASS"}
    if not nonpass.issubset(covered): errors.append(f"uncovered non-PASS checks {sorted(nonpass-covered)}")
    if semantic_digest(findings) != SEMANTIC_DIGESTS["findings"]:
        errors.append("findings: exact semantic mapping mismatch")

    ident = data.get("identifiability")
    if not isinstance(ident, list) or len(ident) != 7 or len({r.get("id") for r in ident}) != 7: errors.append("identifiability count/IDs")
    else:
        for i, row in enumerate(ident):
            p=f"identifiability[{i}]"
            if keys(errors, row, {"id", "combination", "unresolved_primitives", "required_evidence"}, p):
                if not row["unresolved_primitives"]: errors.append(f"{p}.unresolved_primitives")
                text(errors, row["combination"], f"{p}.combination"); text(errors, row["required_evidence"], f"{p}.required_evidence")
        if semantic_digest(ident) != SEMANTIC_DIGESTS["identifiability"]:
            errors.append("identifiability: exact semantic mapping mismatch")

    allowed_authority = {"SOURCE_CITED_TIER_B_OR_C_NOT_PRIMARY_VERIFIED", "SOURCE_CITED_RANGE_OR_PROFILE_NOT_TRANSITION_SPECIFIC_TRUTH", "FIT_INITIAL_OR_TREND_ONLY_GROUND_NOT_FOUND_TRANSITION_SPECIFIC", "EMPIRICAL_FIT_ONLY", "ILLUSTRATIVE_OR_DATA_DRIVEN_NOT_MATERIAL_DEFAULT", "SOURCE_CITED_SINGLE_ENDPOINT_NOT_PRIMARY_VERIFIED_HERE", "SOURCE_CITED_RANGE_PLUS_MODEL_ASSUMPTION_FIT_ONLY", "TIER_C_INITIAL_OR_UNVERIFIED_PENDING_ROUNDTRIP"}
    params = data.get("parameter_authority")
    if not isinstance(params, list) or len(params) != 8 or len({r.get("id") for r in params}) != 8 or {r.get("disposition") for r in params} != allowed_authority: errors.append("parameter authority count/IDs/dispositions")
    else:
        for i, row in enumerate(params):
            p=f"parameter_authority[{i}]"
            if keys(errors, row, {"id", "parameters", "disposition", "anchor"}, p):
                if not row["parameters"]: errors.append(f"{p}.parameters")
                anchor(errors, row["anchor"], f"{p}.anchor", truth)
        parameter_semantics = [(r["id"], r["parameters"], r["disposition"]) for r in params]
        if semantic_digest(parameter_semantics) != SEMANTIC_DIGESTS["parameter_authority"]:
            errors.append("parameter authority: exact ID/disposition mapping mismatch")

    graph = data.get("dependency_graph")
    if keys(errors, graph, {"nodes", "edges", "cycle_analysis"}, "dependency_graph"):
        nodes = graph["nodes"]; node_set = set(nodes) if isinstance(nodes, list) else set()
        if not node_set or len(nodes) != len(node_set): errors.append("graph nodes")
        actual_edges: set[tuple[str, str]] = set()
        for i, edge in enumerate(graph["edges"]):
            if keys(errors, edge, {"from", "to"}, f"graph.edges[{i}]"):
                actual_edges.add((edge["from"], edge["to"]))
                if edge["from"] not in node_set or edge["to"] not in node_set: errors.append(f"graph.edges[{i}]: unknown node")
        if actual_edges != EXPECTED_EDGES or len(graph["edges"]) != len(EXPECTED_EDGES):
            errors.append("graph edges: exact set/count mismatch")
        structures = graph["cycle_analysis"]
        expected_structures = {
            "CYCLE-IMPLICIT-CHARGE": ("CLOSED_CYCLE", "DEFINITIONAL_IMPLICIT_SYSTEM", ["U_oc", "xi_eq", "charge_residual", "U_oc"]),
            "PATH-THERMAL-DEPENDENCY": ("OPEN_PATH", "OPEN_THERMAL_DEPENDENCY_PATH", ["T", "U_j", "branch_center", "xi_eq", "charge_residual", "U_oc"]),
            "PATH-HISTORY-DEPENDENCY": ("OPEN_PATH", "OPEN_STATEFUL_PROTOCOL_PATH", ["protocol", "history_state", "xi_lag", "peak_shape"]),
        }
        if not isinstance(structures, list) or len(structures) != 3: errors.append("graph cycle analysis")
        else:
            found: set[str] = set()
            for i, structure in enumerate(structures):
                path = f"graph.cycle_analysis[{i}]"
                if keys(errors, structure, {"structure_id", "nodes", "topology", "classification", "closure"}, path):
                    sid = structure["structure_id"]; found.add(sid)
                    if sid not in expected_structures or (structure["topology"], structure["classification"], structure["nodes"]) != expected_structures.get(sid):
                        errors.append(f"{path}: exact topology/classification/path mismatch")
                    if any(n not in node_set for n in structure["nodes"]): errors.append(f"{path}: unknown node")
                    pairs = list(zip(structure["nodes"], structure["nodes"][1:]))
                    if any(pair not in actual_edges for pair in pairs): errors.append(f"{path}: non-contiguous edge sequence")
                    is_closed = len(structure["nodes"]) > 1 and structure["nodes"][0] == structure["nodes"][-1]
                    if (structure["topology"] == "CLOSED_CYCLE") != is_closed: errors.append(f"{path}: closure topology mismatch")
                    text(errors, structure["closure"], f"{path}.closure")
            if found != set(expected_structures): errors.append("graph cycle-analysis IDs")

    errors.extend(numeric_errors(data.get("independent_probes")))
    expected_lines = sum(len(truth[p]["lines"]) for p in SOURCE_FILES)
    expected_summary = {"status": "PASS_WITH_CONCERNS", "gate": "PASS_P060_STEP44_PHYSICS_REDERIVATION", "source_files_expected": 31, "source_files_read_full": 31, "source_lines_expected": expected_lines, "source_lines_read_full": expected_lines, "checks": 22, "check_results": RESULT_COUNTS, "findings": SEVERITY_COUNTS, "conflicts_preserved": 10, "identifiability_rows": 7, "parameter_authority_rows": 8, "next_step": "45.1"}
    if expected_lines != 4544 or data.get("summary") != expected_summary: errors.append("summary/4544-line invariant")

    generation = data.get("generation")
    expected_generation = {"builder_path": "Codex/work/v1019_phase060/build_phase060_step44_physics_validation.py", "validator_path": "Codex/work/v1019_phase060/validate_phase060_step44_physics_validation.py", "markdown_path": "Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md", "markdown_sha256": sha(markdown_raw), "canonical_json": "UTF-8 LF indent=2 sort_keys=true allow_nan=false"}
    if generation != expected_generation: errors.append("generation/markdown fingerprint")
    try: markdown = markdown_raw.decode("utf-8")
    except UnicodeDecodeError: markdown = ""; errors.append("markdown UTF-8")
    if b"\r" in markdown_raw: errors.append("markdown CR bytes")
    for required in ["# Phase 060 v1.0.19 독립 물리 재유도", "## 2. 규약 동결", "## 3. 지배 잔차와 관측 변환", "## 4. Check 판정", "## 5. 독립 수치 probe", "## 6. Parameter authority", "## 7. 구조적 식별성", "## 8. Findings", "## 9. 판정 경계", "PASS_WITH_CONCERNS", "Step 45.1"]:
        if required not in markdown: errors.append(f"markdown missing {required}")
    return errors


def find_check(data: dict[str, Any], cid: str) -> dict[str, Any]:
    return next(row for row in data["derivation_checks"] if row["check_id"] == cid)


def negatives(data: dict[str, Any], truth: dict[str, dict[str, Any]], trace_ids: set[str], trace_raw: bytes, markdown_raw: bytes) -> tuple[int, int, list[str]]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("width-pass", lambda d: find_check(d,"P060-PHY-008").__setitem__("result","PASS")),
        ("anchor-empty", lambda d: find_check(d,"P060-PHY-001").__setitem__("source_anchors",[])),
        ("dimensions-empty", lambda d: find_check(d,"P060-PHY-002").__setitem__("dimensions",{})),
        ("sign-empty", lambda d: find_check(d,"P060-PHY-003").__setitem__("sign_convention","")),
        ("production-import", lambda d: d["authority_policy"].__setitem__("production_imported_or_called",True)),
        ("lag-factor", lambda d: d["independent_probes"]["LAG_TIMEBASE"].__setitem__("error_factor",1.)),
        ("electronic-sign", lambda d: d["independent_probes"]["LCO_ELECTRONIC"].__setitem__("delta_S_e_J_per_molK",45.)),
        ("background-pass", lambda d: find_check(d,"P060-PHY-005").__setitem__("result","PASS")),
        ("finite-window-pass", lambda d: find_check(d,"P060-PHY-012").__setitem__("result","PASS")),
        ("lco-pass", lambda d: find_check(d,"P060-PHY-015").__setitem__("result","PASS")),
        ("signed-ica-pass", lambda d: find_check(d,"P060-PHY-003").__setitem__("result","PASS")),
        ("zero-current-pass", lambda d: find_check(d,"P060-PHY-022").__setitem__("result","PASS")),
        ("primary-authority", lambda d: d["parameter_authority"][0].__setitem__("disposition","PRIMARY_VERIFIED")),
        ("duplicate-check", lambda d: d["derivation_checks"][1].__setitem__("check_id",d["derivation_checks"][0]["check_id"])),
        ("unknown-result", lambda d: d["derivation_checks"][0].__setitem__("result","MAYBE")),
        ("missing-finding", lambda d: d.__setitem__("findings",d["findings"][1:])),
        ("invalid-trace", lambda d: find_check(d,"P060-PHY-001").__setitem__("implementation_impact",["TRC-NO"])),
        ("coverage-gap", lambda d: d["inputs"]["source_files"][0].__setitem__("coverage",[{"start":2,"end":d["inputs"]["source_files"][0]["physical_lines"]}])),
        ("source-sha", lambda d: d["inputs"]["source_files"][0].__setitem__("sha256","0"*64)),
        ("markdown-sha", lambda d: d["generation"].__setitem__("markdown_sha256","0"*64)),
        ("edge-node", lambda d: d["dependency_graph"]["edges"][0].__setitem__("to","NO_NODE")),
        ("remove-conflict", lambda d: d.__setitem__("source_conflicts",d["source_conflicts"][1:])),
        ("step", lambda d: d.__setitem__("step",45)),
        ("commit", lambda d: d.__setitem__("source_commit","0"*40)),
        ("summary", lambda d: d["summary"].__setitem__("checks",21)),
        ("probe-import", lambda d: find_check(d,"P060-PHY-003")["independent_probe"].__setitem__("production_imported",True)),
        ("anchor-slice", lambda d: find_check(d,"P060-PHY-002")["source_anchors"][0].__setitem__("slice_sha256","f"*64)),
        ("severity", lambda d: d["findings"][0].__setitem__("severity","P0")),
        ("truth-promotion", lambda d: d["authority_policy"].__setitem__("scientific_truth","VERIFIED")),
        ("missing-probe", lambda d: d["independent_probes"].pop("LOGISTIC")),
        ("cycle-node", lambda d: d["dependency_graph"]["cycle_analysis"][0]["nodes"].append("NO_NODE")),
        ("bad-conflict-ref", lambda d: d["conventions"][0]["conflict_ids"].append("NO_CONFLICT")),
        ("empty-graph-edges", lambda d: d["dependency_graph"].__setitem__("edges", [])),
        ("valid-but-wrong-trace", lambda d: find_check(d,"P060-PHY-001").__setitem__("equation_or_claim_ids", ["TRC-CH1-HYSTERESIS"])),
        ("swap-parameter-authority", lambda d: (d["parameter_authority"][0].__setitem__("disposition", d["parameter_authority"][1]["disposition"]), d["parameter_authority"][1].__setitem__("disposition", "SOURCE_CITED_TIER_B_OR_C_NOT_PRIMARY_VERIFIED"))),
        ("probe-extra-key", lambda d: d["independent_probes"]["LOGISTIC"].__setitem__("unexpected", 1)),
        ("stored-fd-corruption", lambda d: d["independent_probes"]["IMPLICIT"].__setitem__("finite_difference_dUdT_V_per_K", 999.0)),
        ("identifiability-id", lambda d: d["identifiability"][0].__setitem__("id", "ID-OTHER")),
        ("convention-garbage", lambda d: d["conventions"][0].__setitem__("definition", "garbage")),
        ("finding-garbage", lambda d: d["findings"][0].__setitem__("statement", "garbage")),
        ("logistic-temperature", lambda d: d["independent_probes"]["LOGISTIC"].__setitem__("T_K", 999.0)),
        ("logistic-area", lambda d: d["independent_probes"]["LOGISTIC"].__setitem__("truncated_area", 0.0)),
        ("hysteresis-gap", lambda d: d["independent_probes"]["HYSTERESIS"].__setitem__("gap_at_4RT_V", 1e9)),
        ("causal-scale", lambda d: d["independent_probes"]["CAUSAL_MEMORY"].__setitem__("L_over_w", 999.0)),
        ("einstein-temperature", lambda d: d["independent_probes"]["EINSTEIN"]["samples"][0].__setitem__("T_K", 999.0)),
        ("electronic-fd", lambda d: d["independent_probes"]["LCO_ELECTRONIC"].__setitem__("finite_difference_T2_dU_dT_V_per_K", 999.0)),
        ("lag-unconverted", lambda d: d["independent_probes"]["LAG_TIMEBASE"].__setitem__("unconverted_numeric_Lq", 999.0)),
    ]
    passed, escaped = 0, []
    for name, mutation in mutations:
        candidate = copy.deepcopy(data); mutation(candidate)
        if validate(candidate, truth, trace_ids, trace_raw, markdown_raw): passed += 1
        else: escaped.append(name)
    try: strict_load(b'{"x":1,"x":2}'); escaped.append("duplicate-key")
    except DuplicateKey: passed += 1
    try: strict_load(b'{"x":NaN}'); escaped.append("nonfinite")
    except ValueError: passed += 1
    return passed, len(mutations)+2, escaped


def determinism(artifact_raw: bytes, markdown_raw: bytes) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="p060_s44_") as tmp:
        outputs = []
        for n in (1, 2):
            jp, mp = Path(tmp)/f"{n}.json", Path(tmp)/f"{n}.md"
            run = subprocess.run([sys.executable, str(BUILDER), "--json-out", str(jp), "--markdown-out", str(mp)], cwd=ROOT, capture_output=True, text=True)
            if run.returncode: errors.append(f"determinism run {n}: {run.stderr.strip()}")
            else: outputs.append((jp.read_bytes(), mp.read_bytes()))
        if len(outputs)==2 and (outputs[0] != outputs[1] or outputs[0] != (artifact_raw, markdown_raw)): errors.append("determinism bytes mismatch")
    return errors


def main() -> int:
    if not ARTIFACT.is_file():
        print("FAIL missing_artifact: Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json")
        print("FAIL_P060_STEP44_PHYSICS_REDERIVATION 0/1")
        return 1
    if not MARKDOWN.is_file():
        print("FAIL missing_markdown: Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md")
        print("FAIL_P060_STEP44_PHYSICS_REDERIVATION 0/1")
        return 1
    artifact_raw, markdown_raw = ARTIFACT.read_bytes(), MARKDOWN.read_bytes()
    try: data = strict_load(artifact_raw)
    except (ValueError, UnicodeDecodeError) as exc:
        print(f"FAIL strict_json: {exc}"); print("FAIL_P060_STEP44_PHYSICS_REDERIVATION 0/1"); return 1
    canonical = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)+"\n").encode("utf-8")
    errors = [] if artifact_raw == canonical else ["noncanonical JSON bytes"]
    try: truth, trace_ids, trace_raw = source_truth()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL source_truth: {exc}"); print("FAIL_P060_STEP44_PHYSICS_REDERIVATION 0/1"); return 1
    errors.extend(validate(data, truth, trace_ids, trace_raw, markdown_raw))
    errors.extend(ast_policy_errors())
    passed, total, escaped = negatives(data, truth, trace_ids, trace_raw, markdown_raw)
    if escaped: errors.append(f"negative controls escaped: {escaped}")
    errors.extend(determinism(artifact_raw, markdown_raw))
    if errors:
        for error in errors: print(f"FAIL {error}")
        print(f"FAIL_P060_STEP44_PHYSICS_REDERIVATION errors={len(errors)} negatives={passed}/{total}")
        return 1
    print("PASS schema=phase060-step44-v1 checks=22 files=31 lines=4544 results=5/6/9/2/0 findings=0/12/8 conflicts=10")
    print(f"PASS negative_controls={passed}/{total}")
    print("PASS determinism=2/2 production_imported=false")
    print("PASS_P060_STEP44_PHYSICS_REDERIVATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
