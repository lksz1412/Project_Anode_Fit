#!/usr/bin/env python3
"""Build Phase 064 Step 67 problem-class and isolated-runtime evidence.

Frozen production code is copied from Git objects into disposable directories
outside the repository.  It is imported only by child probe processes, never
by this builder.  Human evidence is written first and JSON artifacts last.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import tempfile
from typing import Any, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "0be2e45e56081e141fbd2f58be7a01b023ca16a3"
EXPECTED_SUBJECT = "audit(phase064): bound v1023 algebraic volterra runtime"
GATE = "PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS"
CEILING = "CONDITIONAL_P064"
RESULT = ROOT / "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md"
CODE_OUT = ROOT / "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json"
RUNTIME_OUT = ROOT / "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json"
EVIDENCE_BEGIN = "<!-- P064_STEP67_HUMAN_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P064_STEP67_HUMAN_EVIDENCE_END -->"

PYTHON_LAUNCHERS = (("3.12", ("py", "-3.12")), ("3.14", ("py", "-3.14")))

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md": {
        "read": [1, 225], "read_status": "READ_FULL_STEP67",
        "spans": [[13, 20], [90, 113], [145, 176]],
    },
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py": {
        "read": [1, 1500], "read_status": "READ_FULL_INHERITED_STEP61_REVALIDATED_RUNTIME_STEP67",
        "spans": [[105, 177], [481, 525], [548, 705]],
    },
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": {
        "read": [1, 1585], "read_status": "READ_FULL_STEP67",
        "spans": [[99, 195], [456, 525], [528, 545], [548, 705], [796, 874], [1273, 1284], [1322, 1365]],
    },
    "Claude/docs/v1.0.23/test_gates_v1023.py": {
        "read": [1, 626], "read_status": "READ_FULL_STEP67", "spans": [[1, 25], [482, 626]],
    },
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": {
        "read": [1, 128], "read_status": "READ_FULL_STEP67", "spans": [[1, 17], [26, 128]],
    },
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": {
        "read": [1, 68], "read_status": "READ_FULL_STEP67", "spans": [[1, 18], [45, 68]],
    },
    "Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md": {
        "read": [1, 301], "read_status": "READ_FULL_STEP67", "spans": [[1, 25], [191, 221], [269, 301]],
    },
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": {
        "read": [1, 212], "read_status": "READ_FULL_STEP67", "spans": [[19, 27], [29, 70], [72, 135], [162, 198]],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec01_n0n1.tex": {
        "read": [1, 257], "read_status": "READ_FULL_STEP67", "spans": [[9, 22]],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec02b_part0.tex": {
        "read": [[188, 217], [282, 418]], "read_status": "READ_BOUNDED_STEP67_FULL_INHERITED_STEP64",
        "spans": [[320, 385]],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec06_eqpeak.tex": {
        "read": [1, 89], "read_status": "READ_FULL_STEP67", "spans": [[1, 45]],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": {
        "read": [1, 145], "read_status": "READ_FULL_STEP67", "spans": [[1, 96], [107, 145]],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex": {
        "read": [1, 245], "read_status": "READ_FULL_STEP67", "spans": [[1, 65], [91, 190], [229, 245]],
    },
    "Claude/docs/v1.0.23/_sections/ch3v22_sec03_blend.tex": {
        "read": [[1, 133], [229, 278]], "read_status": "READ_BOUNDED_STEP67_FULL_INHERITED_STEP64",
        "spans": [[69, 115], [229, 278]],
    },
}

REQUIRED_SNIPPETS: dict[str, tuple[str, ...]] = {
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": (
        "T_attempt = (I / Q_cell) * h / kB",
        "out[0] = float(ksi_eq[0])",
        "L_loc = lag_length * np.exp(g_eff * (1.0 - np.asarray(ksi_lag0, dtype=float)))",
        "dV = float(V_uniform[1] - V_uniform[0])",
        "I_use = c * Q_cell",
        "return self._balance_host.solve_U_oc(x_bar, T, **kw)",
    ),
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": (
        'spec_from_file_location("af1023", "Anode_Fit_v1.0.23.py")',
        "for _ in range(60)",
        "transfer_apparent_from_equilibrium",
    ),
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": (
        r"Q_\cell q=Q_\bg(V_n)+\sum_jQ_j\xi_j",
        r"\kappa(\xi)=\kappa_0\,\exp",
        r"\emph{Volterra}",
    ),
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": (
        r"\Delta H_{a,j}^\eff",
        r"L_{q,j}=\frac{|I|}{Q_\cell\,k_j}",
    ),
    "Claude/docs/v1.0.23/_sections/ch1_sec01_n0n1.tex": (
        r"\label{eq:n0map}",
        r"[1/h]$\cdot$[A\,h]$\to$[A]",
    ),
}

RUNTIME_COPY_PATHS = (
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py",
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py",
)


class BuildError(RuntimeError):
    pass


def run(args: Iterable[str], *, cwd: pathlib.Path = ROOT, timeout: int = 300,
        env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        cp = subprocess.run(
            list(args), cwd=cwd, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BuildError(f"command timeout: {list(args)!r}") from exc
    if check and cp.returncode:
        raise BuildError(
            f"command failed ({cp.returncode}): {list(args)!r}\n"
            f"stdout={cp.stdout.decode('utf-8', 'replace')}\n"
            f"stderr={cp.stderr.decode('utf-8', 'replace')}"
        )
    return cp


def git_bytes(path: str, commit: str = BASELINE) -> bytes:
    return run(("git", "show", f"{commit}:{path}")).stdout


def git_text(*args: str) -> str:
    return run(("git", *args)).stdout.decode("utf-8", "strict").strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def finalize(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("semantic_sha256", None)
    value["semantic_sha256"] = sha256(compact_bytes(value))
    return value


def atomic_write(path: pathlib.Path, raw: bytes) -> None:
    temporary: str | None = None
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = handle.name
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def line_count(raw: bytes) -> int:
    return len(raw.decode("utf-8", "strict").splitlines())


def span(raw: bytes, start: int, end: int) -> dict[str, Any]:
    lines = raw.decode("utf-8", "strict").splitlines(keepends=True)
    if not (1 <= start <= end <= len(lines)):
        raise BuildError(f"invalid line span {start}..{end}/{len(lines)}")
    selected = "".join(lines[start - 1:end]).encode("utf-8")
    return {"start": start, "end": end, "sha256": sha256(selected)}


def bound_span(path: str, start: int, end: int) -> dict[str, Any]:
    return {"path": path, **span(git_bytes(path), start, end)}


def source_contracts() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, spec in SOURCE_SPECS.items():
        raw = git_bytes(path)
        text = raw.decode("utf-8", "strict")
        for snippet in REQUIRED_SNIPPETS.get(path, ()):
            if snippet not in text:
                raise BuildError(f"required snippet absent: {path}: {snippet}")
        rows.append({
            "path": path,
            "git_blob": git_text("rev-parse", f"{BASELINE}:{path}"),
            "sha256": sha256(raw),
            "bytes": len(raw),
            "lines": line_count(raw),
            "read_coverage": spec["read"],
            "read_status": spec["read_status"],
            "source_spans": [span(raw, a, b) for a, b in spec["spans"]],
        })
    return rows


def read_human_evidence() -> tuple[dict[str, Any], str]:
    raw = RESULT.read_bytes()
    text = raw.decode("utf-8", "strict")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise BuildError("human evidence markers must occur exactly once")
    body = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0]
    match = re.fullmatch(r"\s*```json\s*\n(.*?)\n```\s*", body, flags=re.DOTALL)
    if match is None:
        raise BuildError("human evidence block malformed")
    value = json.loads(match.group(1))
    expected = {
        "algebraic_problem_classes": 2,
        "baseline_commit": BASELINE,
        "finding_summary": {"P0": 1, "P1": 5, "P2": 3},
        "gate": GATE,
        "phase_ceiling": CEILING,
        "problem_classes": 3,
        "ratio_applicable_classes": 1,
        "runtime_sets": 2,
    }
    if value != expected:
        raise BuildError(f"human evidence mismatch: {value!r}")
    return value, sha256(compact_bytes(value))


def problem_code_artifact() -> dict[str, Any]:
    human, human_hash = read_human_evidence()
    sources = source_contracts()
    problem_classes = [
        {
            "id": "P064-S67-CLASS-001",
            "name": "CHARGE_BALANCE_ALGEBRAIC_ROOT",
            "mathematical_class": "MONOTONE_ALGEBRAIC_ROOT_UNDER_POSITIVE_DOMAIN",
            "ratio_reference_applicable": False,
            "source_equations": ["eq:sm-mc-balance", "eq:blend-balance"],
            "code_symbols": ["GraphiteAnodeDischargeDQDV.solve_U_oc", "BlendedAnodeDQDV.solve_U_oc"],
            "boundary": "NO_INTEGRAL_KERNEL_NO_CAUSAL_MEMORY",
        },
        {
            "id": "P064-S67-CLASS-002",
            "name": "BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY",
            "mathematical_class": "ALGEBRAIC_ROOT",
            "ratio_reference_applicable": False,
            "source_equations": ["Q_cell*q=Q_bg(V_n)+sum_j Q_j*xi_j"],
            "code_symbols": ["GraphiteAnodeDischargeDQDV.equilibrium", "GraphiteAnodeDischargeDQDV.dqdv"],
            "solver_symbol": None,
            "implementation_state": "DOCUMENTED_ROOT_NOT_IMPLEMENTED_CBG_DERIVATIVE_ONLY",
            "boundary": "NO_INTEGRAL_KERNEL_RATIO_ROUTE_PROHIBITED",
        },
        {
            "id": "P064-S67-CLASS-003",
            "name": "CAUSAL_LAG_VOLTERRA_ODE",
            "mathematical_class": "NONLINEAR_CAUSAL_VOLTERRA_EQUIVALENT_FIRST_ORDER_ODE",
            "ratio_reference_applicable": True,
            "source_equations": ["eq:sc-frozen", "eq:sc-true", "eq:sc-volterra-eq", "eq:sc-ratio-local"],
            "code_symbols": ["_causal_memory_pointwise", "_causal_memory_ratio", "GraphiteAnodeDischargeDQDV._lag_ratio_geff", "GraphiteAnodeDischargeDQDV.dqdv"],
            "boundary": "FIRST_PICARD_ITERATE_ONLY_NOT_GENERAL_EXACT_SOLUTION",
        },
    ]
    maps = [
        {"id":"P064-S67-MAP-001","problem_class":"CHARGE_BALANCE_ALGEBRAIC_ROOT","source_equation":"eq:sm-mc-balance","operation":"EXACT_MONOTONE_NUMERICAL_ROOT_FOR_IMPLEMENTED_LOGISTIC_SUM","domain":"x_bar_IN_[0,1]_FINITE_POSITIVE_CAPACITIES_BRACKETED_VOLTAGE","directionality":"EQUILIBRIUM_DIRECTION_INVARIANT","boundary_initial_condition":"ALGEBRAIC_BRACKET_ENDPOINTS_NO_CAUSAL_INITIAL_STATE","variable_map":{"U_oc":"root voltage V","Q_j":"transition capacity","xi_eq_j":"implemented logistic occupancy complement"},"dimension_unit":"BOTH_BALANCE_SIDES_CAPACITY_U_OC_VOLT","limiting_recovery":"N_P_EQ_1_SINGLE_TRANSITION_LIMIT","non_applicable_target":["CAUSAL_LAG_VOLTERRA_ODE","BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY"],"code_symbol":"GraphiteAnodeDischargeDQDV.solve_U_oc","status":"STATIC_CONCORDANT_WITH_EXISTING_DOMAIN_GUARD_GAPS","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch1_sec02b_part0.tex",320,385)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",796,874)]}},
        {"id":"P064-S67-MAP-002","problem_class":"CHARGE_BALANCE_ALGEBRAIC_ROOT","source_equation":"eq:blend-balance","operation":"EXACT_POOLED_HOST_NUMERICAL_ROOT_FOR_IMPLEMENTED_LOGISTIC_SUM","domain":"x_bar_IN_[0,1]_FINITE_POSITIVE_HOST_CAPACITIES_BRACKETED_VOLTAGE","directionality":"EQUILIBRIUM_DIRECTION_INVARIANT","boundary_initial_condition":"ALGEBRAIC_BRACKET_ENDPOINTS_NO_CAUSAL_INITIAL_STATE","variable_map":{"U_oc":"shared host root voltage V","Q_host_j":"host transition capacity","f_Si":"capacity fraction"},"dimension_unit":"BOTH_BALANCE_SIDES_CAPACITY_U_OC_VOLT","limiting_recovery":"F_SI_TO_0_RECOVERS_GRAPHITE_HOST_ROOT","non_applicable_target":["CAUSAL_LAG_VOLTERRA_ODE","FINITE_RATE_NONADDITIVE_HOST_PARTITION"],"code_symbol":"BlendedAnodeDQDV.solve_U_oc","status":"POOLED_DELEGATE_STATIC_CONCORDANCE","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch3v22_sec03_blend.tex",60,115)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",1354,1365)],"applicability_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch3v22_sec03_blend.tex",229,278)]}},
        {"id":"P064-S67-MAP-003","problem_class":"BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY","source_equation":"Q_cell*q=Q_bg(V_n)+sum_j Q_j*xi_j","operation":"DOCUMENTED_ALGEBRAIC_ROOT_IMPLEMENTATION_ABSENT","domain":"DOCUMENTED_BACKGROUND_CAPACITY_FUNCTION_PLUS_TRANSITIONS","directionality":"ALGEBRAIC_NO_CAUSAL_DIRECTION","boundary_initial_condition":"ALGEBRAIC_ROOT_NO_CAUSAL_INITIAL_STATE","variable_map":{"Q_bg":"integral background capacity","Cbg":"implemented derivative-only background"},"dimension_unit":"Q_BG_AND_Q_J_CAPACITY_CBG_CAPACITY_PER_VOLT","limiting_recovery":"C_BG_TO_0_WOULD_RECOVER_TRANSITION_ONLY_BALANCE","non_applicable_target":["RATIO_REFERENCE_ROUTE","VOLTERRA_KERNEL"],"code_symbol":None,"status":"IMPLEMENTATION_GROUND_NOT_FOUND_CBG_DERIVATIVE_ONLY","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex",19,27)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",528,545)]}},
        {"id":"P064-S67-MAP-004","problem_class":"CAUSAL_LAG_VOLTERRA_ODE","source_equation":"eq:sc-ref","operation":"PIECEWISE_LINEAR_EXACT_INTERVAL_RECURRENCE_FOR_CONSTANT_L","domain":"MONOTONE_PROGRESS_VOLTAGE_FINITE_POSITIVE_L_V","directionality":"DISCHARGE_ASCENDING_CHARGE_DESCENDING_PROGRESS_COORDINATE","boundary_initial_condition":"REMOTE_PAST_EQUILIBRIUM_APPROXIMATED_BY_FIRST_SAMPLE_XI_EQ","variable_map":{"V_prog":"progress voltage V","xi_eq":"equilibrium progress","lag_length":"L_V V"},"dimension_unit":"VOLTAGE_COORDINATE_KERNEL_L_V_IN_VOLT","limiting_recovery":"L_V_TO_0_RECOVERS_LOCAL_EQUILIBRIUM_NUMERICALLY","non_applicable_target":["CHARGE_BALANCE_ALGEBRAIC_ROOT","BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY"],"code_symbol":"_causal_memory_pointwise","status":"CONDITIONAL_STATIC_CONCORDANCE_IMPLICIT_REMOTE_PAST_INITIALIZATION","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex",29,45)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",115,145)]}},
        {"id":"P064-S67-MAP-005","problem_class":"CAUSAL_LAG_VOLTERRA_ODE","source_equation":"eq:sc-ratio-local","operation":"FIRST_PICARD_ITERATE_WITH_FROZEN_REFERENCE_TRAJECTORY","domain":"MONOTONE_PROGRESS_VOLTAGE_FINITE_POSITIVE_L_LOC","directionality":"DISCHARGE_ASCENDING_CHARGE_DESCENDING_PROGRESS_COORDINATE","boundary_initial_condition":"REMOTE_PAST_EQUILIBRIUM_APPROXIMATED_BY_FIRST_SAMPLE_XI_EQ","variable_map":{"xi_lag0":"frozen reference trajectory","g_eff":"dimensionless feedback","L_loc":"state-dependent voltage lag V"},"dimension_unit":"G_EFF_DIMENSIONLESS_L_LOC_VOLTAGE","limiting_recovery":"G_EFF_EQ_0_BIT_EXACT_FROZEN_PATH","non_applicable_target":["GENERAL_EXACT_NONLINEAR_SOLUTION","ALGEBRAIC_ROOT_CLASSES"],"code_symbol":"_causal_memory_ratio","status":"FIRST_PICARD_STATIC_CONCORDANCE","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex",72,96)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",146,177)]}},
        {"id":"P064-S67-MAP-006","problem_class":"CAUSAL_LAG_VOLTERRA_ODE","source_equation":"eq:sc-transfer","operation":"UNPADDED_DISCRETE_FOURIER_VOLTAGE_COORDINATE_TRANSFER","domain":"IMPLEMENTATION_ACCEPTS_ARRAY_WITHOUT_UNIFORMITY_OR_LENGTH_GUARD","directionality":"FFT_PERIODIC_COORDINATE_NOT_CAUSAL_TIME_DIRECTION","boundary_initial_condition":"CIRCULAR_PERIODIC_BOUNDARY_NO_FINITE_INITIAL_STATE","variable_map":{"omega_V":"voltage angular frequency V^-1","L_V":"voltage lag V","H":"dimensionless transfer"},"dimension_unit":"OMEGA_V_TIMES_L_V_DIMENSIONLESS","limiting_recovery":"L_V_EQ_0_IDENTITY_TRANSFER","non_applicable_target":["TIME_DOMAIN_EIS","INSTRUMENT_RESPONSE","NONUNIFORM_GRID_IDENTITY"],"code_symbol":"transfer_apparent_from_equilibrium","status":"VOLTAGE_COORDINATE_CIRCULAR_DFT_UNIFORMITY_UNENFORCED","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex",162,198)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",180,195)]}},
        {"id":"P064-S67-MAP-007","problem_class":"CAUSAL_LAG_VOLTERRA_ODE","source_equation":"eq:n0map_AND_eq:Lq","operation":"C_RATE_TO_CURRENT_THEN_NORMALIZED_KINETIC_RATE","domain":"C_RATE_PER_HOUR_Q_CELL_AMPERE_HOUR_EYRING_RATE_PER_SECOND","directionality":"CURRENT_MAGNITUDE_WITH_SEPARATE_DIRECTION_SIGN","boundary_initial_condition":"NOT_APPLICABLE_TIMEBASE_PROJECTION","variable_map":{"I_abs":"current A","Q_cell":"capacity Ah at curve boundary but C required for I/Q in s^-1","c_rate":"h^-1"},"dimension_unit":"IR_CURRENT_A_UNCHANGED_KINETIC_I_OVER_Q_MUST_BE_S^-1","limiting_recovery":"C_RATE_TO_0_ZERO_CURRENT_EQUILIBRIUM_LIMIT","non_applicable_target":["DIVIDE_IR_CURRENT_BY_3600"],"code_symbol":"GraphiteAnodeDischargeDQDV.curve_AND_func_L_q","status":"CONFLICT_HOUR_TO_SECOND_CONVERSION_MISSING","evidence":{"equation_sources":[bound_span("Claude/docs/v1.0.23/_sections/ch1_sec01_n0n1.tex",9,22),bound_span("Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex",1,25)],"code_sources":[bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",99,112),bound_span("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",675,705)]}},
    ]
    call_edges = [
        {"caller": "GraphiteAnodeDischargeDQDV.curve", "callee": "GraphiteAnodeDischargeDQDV.dqdv", "class": "CAUSAL_LAG_VOLTERRA_ODE"},
        {"caller": "GraphiteAnodeDischargeDQDV.dqdv", "callee": "GraphiteAnodeDischargeDQDV._resolve_lag_length", "class": "CAUSAL_LAG_VOLTERRA_ODE"},
        {"caller": "GraphiteAnodeDischargeDQDV.dqdv", "callee": "_causal_memory_pointwise", "condition": "lag_ratio_correction=False"},
        {"caller": "GraphiteAnodeDischargeDQDV.dqdv", "callee": "_causal_memory_ratio", "condition": "lag_ratio_correction=True"},
        {"caller": "BlendedAnodeDQDV.solve_U_oc", "callee": "GraphiteAnodeDischargeDQDV.solve_U_oc", "condition": "pooled transitions"},
    ]
    findings = [
        ("P064-S67-F001", "P0", "OPEN_ROUTED", "Phase 076/081", "C-rate h^-1 enters second-based kinetics without /3600; lag is 3600 times the SI-corrected route."),
        ("P064-S67-F002", "P1", "OPEN_ROUTED", "Phase 081", "Documented background algebraic root has no production solver; Cbg is derivative-only."),
        ("P064-S67-F003", "P1", "OPEN_ROUTED", "Phase 081", "Transfer silently accepts nonuniform grids and uses an unpadded circular DFT."),
        ("P064-S67-F004", "P1", "OPEN_ROUTED", "Phase 076/081", "Lag functions hard-code xi_lag[0]=xi_eq[0] and expose no finite initial-state contract."),
        ("P064-S67-F005", "P1", "OPEN_ROUTED", "Phase 081", "Self-consistency gate loads production from cwd and does not pin path/blob/version identity."),
        ("P064-S67-F006", "P1", "OPEN_ROUTED", "Phase 068/081", "Transfer prose promotes a voltage-coordinate identity to instrument response."),
        ("P064-S67-F007", "P2", "OPEN_ROUTED", "Phase 081", "P1 observation requires UTF-8 on Windows CP949 and has no assertions/nonzero scientific failure."),
        ("P064-S67-F008", "P2", "GROUND_NOT_FOUND", "Phase 068", "Referenced scratchpad cond_audit_verify.py is absent from the frozen tree."),
        ("P064-S67-F009", "P2", "OPEN_ROUTED", "Phase 068", "Internal self-referential regressions do not establish units, material, experimental, or external literature truth."),
    ]
    finding_rows = [
        {"id": i, "priority": p, "status": s, "owner": o, "finding": f,
         "frozen_source_modified": False, "external_truth_validated": False}
        for i, p, s, o, f in findings
    ]
    return finalize({
        "artifact_kind": "PHASE_064_V1023_PROBLEM_CODE_DELTA",
        "schema": 1,
        "phase": 64,
        "step": 67,
        "generated_date": "2026-08-29",
        "generated_by": "build_phase064_step67_problem_runtime_boundary.py",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "gate": GATE,
        "phase_ceiling": CEILING,
        "status": "RESULT_FIRST_PRECOMMIT_EVIDENCE",
        "human_evidence": human,
        "human_evidence_semantic_sha256": human_hash,
        "source_contracts": sources,
        "problem_classes": problem_classes,
        "equation_code_map": maps,
        "call_edges": call_edges,
        "non_double_count": {
            "classification": "BASELINE_PLUS_STATE_DEVIATION_NOT_DUPLICATE_TOTAL_TERM",
            "baseline": "dH_eff=dH_a-chi_d*Omega at xi_to_1",
            "modulation": "L_loc=L0*exp(2*chi_d*Omega*(1-xi0)/(R*T))",
            "scope": "INTERNAL_REDUCED_FEEDBACK_HYPOTHESIS_ONLY",
            "external_physical_truth": False,
        },
        "omega_consumer_partition": [
            {"consumer": "hysteresis_center", "symbols": ["func_dU_hys", "func_U_branch", "dqdv"], "spans": [[200, 214], [628, 635]], "separate_role": True},
            {"consumer": "lag_baseline", "symbols": ["func_dH_a_eff", "_resolve_lag_length"], "spans": [[218, 221], [511, 525]], "separate_role": True},
            {"consumer": "lag_state_deviation", "symbols": ["_lag_ratio_geff", "_causal_memory_ratio"], "spans": [[146, 177], [466, 478]], "separate_role": True},
        ],
        "regular_solution_occupancy": {
            "implicit_omega_nonzero_equilibrium_implemented": False,
            "checked_symbols": ["func_ksi_eq", "GraphiteAnodeDischargeDQDV.solve_U_oc"],
            "status": "GROUND_NOT_FOUND_DO_NOT_PROMOTE_LAG_IDENTITY_TO_EQUILIBRIUM_IMPLEMENTATION",
        },
        "inherited_joins": [
            {"current": "P064-S67-F001", "prior": ["P063-S61-F001", "P064-S66-CORR-001"], "duplicate_new_finding": False},
            {"current": "P064-S67-F003", "prior": ["P064-S66-CORR-007"], "duplicate_new_finding": False},
            {"current": "P064-S67-F007", "prior": ["P063-S61-F011", "P064-S66-CORR-010"], "duplicate_new_finding": False},
            {"current": "P064-S67-F008", "prior": ["P064-S66-CORR-009"], "duplicate_new_finding": False},
        ],
        "findings": finding_rows,
        "counts": {"problem_classes": 3, "ratio_applicable": 1, "algebraic": 2, "P0": 1, "P1": 5, "P2": 3},
        "authority": {
            "static_internal_concordance": True,
            "runtime_internal_concordance": False,
            "material_truth": False,
            "experimental_truth": False,
            "external_primary_literature_truth": False,
            "canonical_adoption": False,
            "publication_readiness": False,
        },
        "source_mutation_count": 0,
    })


PROBE_SOURCE = r'''# -*- coding: utf-8 -*-
from __future__ import annotations
import importlib.util, json, sys
import numpy as np
sys.dont_write_bytecode = True

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

af22, af23 = load(sys.argv[1], "af22_p064s67"), load(sys.argv[2], "af23_p064s67")
V = np.linspace(0.05, 0.25, 600)
tr = [{'U':0.14,'w':0.02,'Q':0.12,'L_V':0.006,'Omega':8000.0,'dVdq_qa':0.30}]
m22 = af22.GraphiteAnodeDischargeDQDV(tr)
mdef = af23.GraphiteAnodeDischargeDQDV(tr)
mfalse = af23.GraphiteAnodeDischargeDQDV(tr, lag_ratio_correction=False)
mon = af23.GraphiteAnodeDischargeDQDV(tr, lag_ratio_correction=True)
y22 = np.asarray(m22.dqdv(V, 298.15, 1.0, 1.0, +1))
ydef = np.asarray(mdef.dqdv(V, 298.15, 1.0, 1.0, +1))
yfalse = np.asarray(mfalse.dqdv(V, 298.15, 1.0, 1.0, +1))
yon = np.asarray(mon.dqdv(V, 298.15, 1.0, 1.0, +1))

tr0 = tr[0]
n = float(np.asarray(mon._n_factor(tr0, 298.15)).reshape(-1)[0])
xeq = np.asarray(af23.func_ksi_eq(298.15, V, tr0['U'], n, +1), dtype=float)
x0 = af23._causal_memory_pointwise(V, xeq, tr0['L_V'])
geff = mon._lag_ratio_geff(tr0, 298.15, +1)
x1, lloc = af23._causal_memory_ratio(V, xeq, x0, tr0['L_V'], geff)
manual = tr0['Q'] * (xeq - x1) / lloc

tr_zero = [{'U':0.14,'w':0.02,'Q':0.12,'L_V':0.006,'Omega':0.0,'dVdq_qa':0.30}]
zoff = af23.GraphiteAnodeDischargeDQDV(tr_zero)
zon = af23.GraphiteAnodeDischargeDQDV(tr_zero, lag_ratio_correction=True)
yzoff = np.asarray(zoff.dqdv(V, 298.15, 1.0, 1.0, +1))
yzon = np.asarray(zon.dqdv(V, 298.15, 1.0, 1.0, +1))

capture = {}
cap = af23.GraphiteAnodeDischargeDQDV([{'U':0.14,'w':0.02,'Q':1.0}])
def capture_dqdv(V_app, T, I_abs, Q_cell, s=+1):
    capture.update(I_abs=float(I_abs), Q_cell=float(Q_cell), s=int(s))
    return np.zeros_like(np.asarray(V_app, dtype=float))
cap.dqdv = capture_dqdv
cap.curve(np.array([0.1,0.2]), 'discharge', c_rate=1.0, Q_cell=2.0, T=298.15)
dyn = {'U':0.14,'w':0.02,'Q':1.0,'dH_a':85000.0,'dS_a':0.0,'dVdq_qa':0.30,'Omega':0.0}
kin = af23.GraphiteAnodeDischargeDQDV([dyn])
lraw = kin._resolve_lag_length(dyn, 298.15, 2.0, 2.0, 1.0, +1)
lsi = kin._resolve_lag_length(dyn, 298.15, 2.0, 2.0*3600.0, 1.0, +1)

Vu = np.linspace(0.0, 1.0, 512, endpoint=False)
peak = np.sin(2*np.pi*3*Vu) + 0.25*np.cos(2*np.pi*11*Vu)
got = af23.transfer_apparent_from_equilibrium(Vu, peak, 0.02)
dV = float(Vu[1]-Vu[0])
omega = 2*np.pi*np.fft.fftfreq(Vu.size, d=dV)
expected = np.real(np.fft.ifft(np.fft.fft(peak)/(1+1j*omega*0.02)))
Vnu = Vu.copy(); Vnu[111] += 0.00031
nonuniform_raised = False
try:
    nonuniform = af23.transfer_apparent_from_equilibrium(Vnu, peak, 0.02)
except Exception:
    nonuniform_raised = True
    nonuniform = np.array([np.nan])
impulse = np.zeros(512); impulse[-1] = 1.0
wrapped = af23.transfer_apparent_from_equilibrium(Vu, impulse, 0.02)

Vlong = np.linspace(0.0, 0.3, 2000)
xeqlong = np.asarray(af23.func_ksi_eq(298.15, Vlong, 0.15, 0.02*af23.F/(af23.R*298.15), +1), dtype=float)
xfull = af23._causal_memory_pointwise(Vlong, xeqlong, 0.02)
cut = 533
xrestart = af23._causal_memory_pointwise(Vlong[cut:], xeqlong[cut:], 0.02)
restart_gap = abs(float(xrestart[0]-xfull[cut]))
restart_gap_100 = abs(float(xrestart[100]-xfull[cut+100]))

out = {
  'option_boundary': {
    'v22_default_equals_v23_default': bool(np.array_equal(y22,ydef)),
    'v23_default_equals_explicit_false': bool(np.array_equal(ydef,yfalse)),
    'g_eff_zero_on_equals_off': bool(np.array_equal(yzoff,yzon)),
    'ratio_liveness_max_abs_diff': float(np.max(np.abs(yon-yfalse))),
    'pass': bool(np.array_equal(y22,ydef) and np.array_equal(ydef,yfalse) and np.array_equal(yzoff,yzon) and np.max(np.abs(yon-yfalse))>1e-9),
  },
  'picard_identity': {
    'g_eff': float(geff),
    'ratio_vs_manual_first_picard_max_abs_diff': float(np.max(np.abs(yon-manual))),
    'pass': bool(np.max(np.abs(yon-manual))<1e-13),
    'claim_ceiling': 'FIRST_PICARD_ITERATE_ONLY',
  },
  'timebase': {
    'captured_curve_current_A': float(capture['I_abs']),
    'captured_curve_capacity_Ah': float(capture['Q_cell']),
    'si_current_A_unchanged': 2.0,
    'si_capacity_C': 2.0*3600.0,
    'normalized_rate_raw_per_h_numeric': 2.0/2.0,
    'normalized_rate_si_per_s': 2.0/(2.0*3600.0),
    'lag_raw_V': float(lraw),
    'lag_si_corrected_V': float(lsi),
    'lag_raw_over_corrected': float(lraw/lsi),
    'pass': bool(capture['I_abs']==2.0 and capture['Q_cell']==2.0 and abs(lraw/lsi-3600.0)<1e-8),
  },
  'transfer': {
    'manual_fft_max_abs_diff': float(np.max(np.abs(got-expected))),
    'nonuniform_grid_rejected': bool(nonuniform_raised),
    'nonuniform_output_finite': bool(np.all(np.isfinite(nonuniform))),
    'circular_wrap_first_value_abs': float(abs(wrapped[0])),
    'pass': bool(np.max(np.abs(got-expected))<1e-13 and (not nonuniform_raised) and np.all(np.isfinite(nonuniform)) and abs(wrapped[0])>0.0),
    'coordinate': 'VOLTAGE_ONLY',
  },
  'initial_condition': {
    'pointwise_first_equals_equilibrium_first': bool(x0[0]==xeq[0]),
    'ratio_first_equals_equilibrium_first': bool(x1[0]==xeq[0]),
    'finite_initial_state_parameter_present': False,
    'finite_window_restart_start_abs_gap': restart_gap,
    'finite_window_restart_after_100_abs_gap': restart_gap_100,
    'pass': bool(x0[0]==xeq[0] and x1[0]==xeq[0] and restart_gap>1e-3 and restart_gap_100>1e-3),
  },
}
for section in out.values():
    section['authority'] = 'ISOLATED_INTERNAL_RUNTIME_ONLY'
    section['material_truth'] = False
    section['experimental_truth'] = False
print(json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(',',':'), allow_nan=False))
'''


def normalized(raw: bytes, temp_root: pathlib.Path) -> bytes:
    text = raw.decode("utf-8", "replace")
    for candidate in (
        str(temp_root), str(temp_root).replace("\\", "/"),
        str(temp_root).replace("\\", "\\\\"),
    ):
        text = text.replace(candidate, "<TMP>")
    return text.replace("\r\n", "\n").encode("utf-8")


def run_row(runtime: str, launcher: tuple[str, ...], *, run_id: str,
            script: pathlib.Path, cwd: pathlib.Path, temp_root: pathlib.Path,
            encoding: str, expected: str) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if encoding == "cp949":
        command = (*launcher, "-B", "-I", "-X", "utf8", "-c",
                   "import runpy,sys;sys.stdout.reconfigure(encoding='cp949');runpy.run_path(sys.argv[1],run_name='__main__')",
                   str(script))
    else:
        command = (*launcher, "-B", "-I", "-X", "utf8", str(script))
    cp = run(command, cwd=cwd, env=env, check=False)
    stdout = normalized(cp.stdout, temp_root)
    stderr = normalized(cp.stderr, temp_root)
    stderr_text = stderr.decode("utf-8", "replace")
    if expected == "PASS":
        matched = cp.returncode == 0
        diagnostic = None
    elif expected == "FAIL_WRONG_CWD":
        matched = cp.returncode != 0 and "FileNotFoundError" in stderr_text and "Anode_Fit_v1.0.23.py" in stderr_text
        diagnostic = "FILE_NOT_FOUND_CWD_RELATIVE_LOAD"
    elif expected == "FAIL_CP949":
        matched = cp.returncode != 0 and "UnicodeEncodeError" in stderr_text
        diagnostic = "UNICODE_ENCODE_ERROR_CP949"
    else:
        raise BuildError(f"unknown expected state {expected}")
    return {
        "run_id": run_id, "runtime": runtime,
        "command": [*command[:-1], str(script.relative_to(temp_root))],
        "cwd": str(cwd.relative_to(temp_root)) if cwd != temp_root else ".",
        "encoding": encoding, "exit_code": cp.returncode,
        "expected_state": expected, "diagnostic": diagnostic,
        "expectation_met": matched,
        "stdout_sha256": sha256(stdout), "stderr_sha256": sha256(stderr),
        "stdout_tail": stdout.decode("utf-8", "replace").splitlines()[-8:],
        "stderr_tail": stderr.decode("utf-8", "replace").splitlines()[-8:],
        "authority": "INTERNAL_EXECUTION_ONLY", "external_truth": False,
    }


def repository_projection() -> dict[str, Any]:
    return {
        "head": git_text("rev-parse", "HEAD"),
        "branch": git_text("rev-parse", "--abbrev-ref", "HEAD"),
        "baseline_claude_tree": git_text("rev-parse", f"{BASELINE}:Claude"),
        "head_claude_tree": git_text("rev-parse", "HEAD:Claude"),
        "claude_diff": run(("git", "diff", "--binary", "--", "Claude")).stdout,
        "claude_status": run(("git", "status", "--porcelain=v1", "-z", "--", "Claude")).stdout,
        "full_diff": run(("git", "diff", "--binary")).stdout,
        "full_status": run(("git", "status", "--porcelain=v1", "-z", "-uall")).stdout,
    }


def stable_projection_record(projection: dict[str, Any]) -> dict[str, Any]:
    return {
        "head": projection["head"],
        "branch": projection["branch"],
        "baseline_claude_tree": projection["baseline_claude_tree"],
        "head_claude_tree": projection["head_claude_tree"],
        "claude_diff_sha256": sha256(projection["claude_diff"]),
        "claude_status_sha256": sha256(projection["claude_status"]),
    }


def runtime_artifact() -> dict[str, Any]:
    before = repository_projection()
    runtime_rows: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    probes: list[dict[str, Any]] = []
    temp_path: pathlib.Path | None = None
    with tempfile.TemporaryDirectory(prefix="p064_step67_") as td:
        tmp = pathlib.Path(td).resolve()
        temp_path = tmp
        root = ROOT.resolve()
        if tmp == root or root in tmp.parents:
            raise BuildError(f"temporary directory is not external: {tmp}")
        for path in RUNTIME_COPY_PATHS:
            target = tmp / pathlib.PurePosixPath(path).relative_to("Claude/docs")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(git_bytes(path))
        probe = tmp / "step67_probe.py"
        probe.write_text(PROBE_SOURCE, encoding="utf-8", newline="\n")
        mutation = tmp / "version_mutation"
        mutation.mkdir()
        prod_raw = git_bytes("Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
        mutated = prod_raw.replace(b"release \xeb\xb2\x84\xec\xa0\x84 = 1.0.23", b"release \xeb\xb2\x84\xec\xa0\x84 = 9.9.99", 1)
        if mutated == prod_raw:
            raise BuildError("version mutation did not apply")
        (mutation / "Anode_Fit_v1.0.23.py").write_bytes(mutated)
        (mutation / "test_gates_v1023_selfconsistent.py").write_bytes(
            git_bytes("Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py")
        )
        for runtime, launcher in PYTHON_LAUNCHERS:
            version = run((*launcher, "-B", "-I", "-X", "utf8", "-c", "import sys,numpy;print(sys.version.split()[0]);print(numpy.__version__)"))
            versions = version.stdout.decode("utf-8", "strict").splitlines()
            runtime_rows.append({"runtime": runtime, "python_version": versions[0], "numpy_version": versions[1], "launcher": list(launcher)})
            sc = tmp / "v1.0.23/test_gates_v1023_selfconsistent.py"
            p1 = tmp / "v1.0.23/results/comp_v23/p1_ratio_check.py"
            runs.extend((
                run_row(runtime, launcher, run_id=f"P064-S67-SC-UTF8-{runtime}", script=sc, cwd=sc.parent, temp_root=tmp, encoding="utf-8", expected="PASS"),
                run_row(runtime, launcher, run_id=f"P064-S67-SC-WRONG-CWD-{runtime}", script=sc, cwd=tmp, temp_root=tmp, encoding="utf-8", expected="FAIL_WRONG_CWD"),
                run_row(runtime, launcher, run_id=f"P064-S67-P1-UTF8-{runtime}", script=p1, cwd=p1.parent, temp_root=tmp, encoding="utf-8", expected="PASS"),
                run_row(runtime, launcher, run_id=f"P064-S67-P1-CP949-{runtime}", script=p1, cwd=p1.parent, temp_root=tmp, encoding="cp949", expected="FAIL_CP949"),
                run_row(runtime, launcher, run_id=f"P064-S67-SC-VERSION-MUTATION-{runtime}", script=mutation / "test_gates_v1023_selfconsistent.py", cwd=mutation, temp_root=tmp, encoding="utf-8", expected="PASS"),
            ))
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"
            cp = run((*launcher, "-B", "-I", "-X", "utf8", str(probe),
                      str(tmp / "v1.0.22/Anode_Fit_v1.0.22.py"),
                      str(tmp / "v1.0.23/Anode_Fit_v1.0.23.py")), cwd=tmp, env=env)
            data = json.loads(cp.stdout.decode("utf-8", "strict"))
            if not all(section["pass"] for section in data.values()):
                raise BuildError(f"independent probe failed for {runtime}: {data!r}")
            probes.append({"runtime": runtime, "probe_sha256": sha256(PROBE_SOURCE.encode("utf-8")), "results": data})
    cleanup = temp_path is not None and not temp_path.exists()
    after = repository_projection()
    projection_equal = all(before[key] == after[key] for key in before)
    before_projection_sha256 = sha256(compact_bytes(stable_projection_record(before)))
    after_projection_sha256 = sha256(compact_bytes(stable_projection_record(after)))
    if not cleanup or not projection_equal:
        raise BuildError(f"runtime isolation failed: cleanup={cleanup} projection_equal={projection_equal}")
    if not all(row["expectation_met"] for row in runs):
        failed = [
            {key: row[key] for key in ("run_id", "exit_code", "expected_state", "stderr_tail")}
            for row in runs if not row["expectation_met"]
        ]
        raise BuildError(f"official/mutation expectations not met: {failed!r}")
    copy_manifest = []
    for path in RUNTIME_COPY_PATHS:
        raw = git_bytes(path)
        copy_manifest.append({
            "path": path, "git_blob": git_text("rev-parse", f"{BASELINE}:{path}"),
            "sha256": sha256(raw), "bytes": len(raw), "lines": line_count(raw),
        })
    frozen_blobs = [
        {"path": row["path"], "git_blob": row["git_blob"], "sha256": row["sha256"]}
        for row in copy_manifest
    ]
    input_sha = sha256(compact_bytes({
        "frozen_blobs": frozen_blobs,
        "probe_sha256": sha256(PROBE_SOURCE.encode("utf-8")),
    }))
    versions_by_runtime = {row["runtime"]: row for row in runtime_rows}
    runtime_evidence_rows = []
    for probe_row in probes:
        runtime = probe_row["runtime"]
        launcher = dict(PYTHON_LAUNCHERS)[runtime]
        result = probe_row["results"]
        runtime_evidence_rows.append({
            "runtime": runtime,
            "frozen_blobs": frozen_blobs,
            "invocation": [*launcher, "-B", "-I", "-X", "utf8",
                           "<EXTERNAL>/step67_probe.py",
                           "<EXTERNAL>/v1.0.22/Anode_Fit_v1.0.22.py",
                           "<EXTERNAL>/v1.0.23/Anode_Fit_v1.0.23.py"],
            "environment": {
                "python_version": versions_by_runtime[runtime]["python_version"],
                "numpy_version": versions_by_runtime[runtime]["numpy_version"],
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONIOENCODING": "utf-8",
                "isolated_mode": True,
                "network_used": False,
            },
            "input_sha256": input_sha,
            "output_sha256": sha256(compact_bytes(result)),
            "metric": {
                "ratio_liveness_max_abs_diff": result["option_boundary"]["ratio_liveness_max_abs_diff"],
                "ratio_vs_manual_first_picard_max_abs_diff": result["picard_identity"]["ratio_vs_manual_first_picard_max_abs_diff"],
                "lag_raw_over_corrected": result["timebase"]["lag_raw_over_corrected"],
                "manual_fft_max_abs_diff": result["transfer"]["manual_fft_max_abs_diff"],
                "finite_window_restart_start_abs_gap": result["initial_condition"]["finite_window_restart_start_abs_gap"],
            },
            "tolerance": {
                "ratio_liveness_min": 1e-9,
                "picard_identity_max_abs": 1e-13,
                "timebase_ratio_abs_from_3600_max": 1e-8,
                "transfer_identity_max_abs": 1e-13,
                "restart_gap_min": 1e-3,
            },
            "complexity_observation": "LAG_RECURRENCES_O_N_TRANSFER_FFT_O_N_LOG_N_ANALYTICAL_NOT_BENCHMARKED",
            "repository_before_after_projection": {
                "equal": projection_equal,
                "hash_scope": "HEAD_BRANCH_CLAUDE_TREE_CLAUDE_DIFF_STATUS",
                "before_sha256": before_projection_sha256,
                "after_sha256": after_projection_sha256,
                "head": before["head"],
                "branch": before["branch"],
                "baseline_claude_tree": before["baseline_claude_tree"],
                "head_claude_tree": before["head_claude_tree"],
                "claude_clean_before_after": before["claude_diff"] == b"" and before["claude_status"] == b"",
                "full_worktree_projection_compared": True,
            },
            "cleanup_state": "VERIFIED_EXTERNAL_TEMP_REMOVED",
            "authority_ceiling": "INTERNAL_SYNTHETIC_IMPLEMENTATION_ONLY",
        })
    return finalize({
        "artifact_kind": "PHASE_064_V1023_RUNTIME_ATTESTATION",
        "schema": 1, "phase": 64, "step": 67,
        "generated_date": "2026-08-29",
        "generated_by": "build_phase064_step67_problem_runtime_boundary.py",
        "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT, "gate": GATE,
        "phase_ceiling": CEILING, "status": "RESULT_FIRST_PRECOMMIT_EVIDENCE",
        "isolation": {
            "production_imported_by_builder": False,
            "production_imported_by_validator": False,
            "production_imported_only_by_child_subprocess": True,
            "copied_git_blobs_only": True,
            "disposable_external_directories": True,
            "bytecode_disabled": True, "network_used": False,
            "repository_projection_equal_before_after": projection_equal,
            "repository_projection_hash_scope": "HEAD_BRANCH_CLAUDE_TREE_CLAUDE_DIFF_STATUS",
            "repository_projection_before_sha256": before_projection_sha256,
            "repository_projection_after_sha256": after_projection_sha256,
            "disposable_cleanup_verified": cleanup,
            "head": before["head"], "branch": before["branch"],
            "baseline_claude_tree": before["baseline_claude_tree"],
            "head_claude_tree": before["head_claude_tree"],
            "claude_clean_before_after": before["claude_diff"] == b"" and before["claude_status"] == b"",
            "copy_manifest": copy_manifest,
        },
        "runtimes": runtime_rows,
        "official_and_mutation_runs": runs,
        "independent_probes": probes,
        "runtime_evidence_rows": runtime_evidence_rows,
        "counts": {
            "runtimes": len(runtime_rows), "runs": len(runs),
            "run_expectations_met": sum(bool(row["expectation_met"]) for row in runs),
            "probe_runtime_sets": len(probes), "probe_sections_per_runtime": 5,
            "runtime_evidence_rows": len(runtime_evidence_rows),
        },
        "authority": {
            "synthetic_numerical": True, "implementation_regression": True,
            "picard_iteration": True, "voltage_transfer_identity": True,
            "material_validation": False, "experimental_validation": False,
            "external_primary_literature_validation": False,
            "canonical_adoption": False, "publication_readiness": False,
        },
        "source_mutation_count": 0,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=pathlib.Path, default=CODE_OUT.parent)
    args = parser.parse_args()
    if not RESULT.exists():
        raise BuildError("result-first human document is absent")
    code = problem_code_artifact()
    runtime = runtime_artifact()
    out = args.out_dir.resolve()
    atomic_write(out / CODE_OUT.name, pretty_bytes(code))
    atomic_write(out / RUNTIME_OUT.name, pretty_bytes(runtime))
    print(
        f"PASS_P064_STEP67_BUILD classes={code['counts']['problem_classes']} "
        f"runs={runtime['counts']['run_expectations_met']}/{runtime['counts']['runs']} "
        f"probes={runtime['counts']['probe_runtime_sets']}"
    )


if __name__ == "__main__":
    main()
