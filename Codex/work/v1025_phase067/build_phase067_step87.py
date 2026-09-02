#!/usr/bin/env python3
"""Build Phase 067 Step 87 source-grounded unit/numerical evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
DATE = "2026-09-02"
SUBJECT = "audit(phase067): verify units numerical invariants"
GATE = "PASS_P067_STEP87_UNIT_NUMERICAL"
PERSISTENCE = "PASS_P067_STEP87_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "c97ad94c35e8f4db3db5c207cf099a647cb363fca9d7816221e136c22bf4621f"

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STATE_FLOW_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
OUTPUT_PATH = "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json"
INVENTORY_RAW_SHA256 = "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63"
INVENTORY_SEMANTIC_SHA256 = "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"
ATTESTATION_RAW_SHA256 = "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174"
ATTESTATION_SEMANTIC_SHA256 = "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"
STATE_FLOW_RAW_SHA256 = "0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8"
STATE_FLOW_SEMANTIC_SHA256 = "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44"
RELEASES = [
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14",
    "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2",
    "v1.0.19", "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23",
    "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
]


class BuildError(RuntimeError):
    pass


def require(ok: bool, diagnostic: str) -> None:
    if not ok:
        raise BuildError(diagnostic)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("semantic_sha256", None)
    return sha(canonical(copy))


def predecessor_semantic(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy["semantic_sha256"] = ""
    raw = (json.dumps(copy, ensure_ascii=False, indent=2, sort_keys=True,
                      separators=(",", ": "), allow_nan=False) + "\n").encode("utf-8")
    return sha(raw)


def finish(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic(value)
    return value


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, label + "_DUPLICATE")
            out[key] = value
        return out
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise BuildError(label) from exc
    require(isinstance(value, dict), label + "_ROOT")
    return value


def input_json(path: str, raw_pin: str, semantic_pin: str, modern: bool = False) -> dict[str, Any]:
    completed = subprocess.run(
        ["git", "show", f"{EXPECTED_PARENT}:{path}"], check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(completed.returncode == 0 and completed.stderr == b"", "E_GIT_INPUT")
    raw = completed.stdout
    require(sha(raw) == raw_pin, "E_INPUT_RAW_" + path)
    value = strict_json(raw, "E_INPUT_JSON")
    observed_semantic = semantic(value) if modern else predecessor_semantic(value)
    require(observed_semantic == semantic_pin, "E_INPUT_SEMANTIC_" + path)
    return value


def blob(oid: str) -> bytes:
    require(len(oid) == 40 and all(c in "0123456789abcdef" for c in oid), "E_BLOB_OID")
    completed = subprocess.run(["git", "cat-file", "blob", oid], check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(completed.returncode == 0 and completed.stderr == b"", "E_GIT_BLOB")
    return completed.stdout


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__, "fields": [
            [field, stable_ast(getattr(value, field, None))] for field in value._fields
        ]}
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, tuple):
        return {"_tuple": [stable_ast(item) for item in value]}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return {"_literal_type": type(value).__name__, "repr": repr(value)}


def qualified_owner(tree: ast.Module, selected: ast.AST) -> str:
    found: list[tuple[int, str]] = []
    def walk(node: ast.AST, scope: list[str]) -> None:
        nested = scope
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            nested = [*scope, node.name]
            if (node.lineno <= getattr(selected, "lineno", 0)
                    and node.end_lineno >= getattr(selected, "end_lineno", 0)):
                found.append((node.end_lineno - node.lineno, ".".join(nested)))
        for child in ast.iter_child_nodes(node):
            walk(child, nested)
    walk(tree, [])
    return min(found)[1] if found else "<module>"


def anchor(tree: ast.Module, source: str, node: ast.AST) -> dict[str, Any]:
    lines = source.splitlines()
    start = int(getattr(node, "lineno", 0))
    end = int(getattr(node, "end_lineno", start))
    require(start > 0 and end >= start, "E_ANCHOR_EXTENT")
    text = "\n".join(lines[start - 1:end]) + "\n"
    return {
        "qualified_owner": qualified_owner(tree, node),
        "ast_kind": type(node).__name__,
        "start_line": start,
        "end_line": end,
        "source_sha256": sha(text.encode("utf-8")),
        "node_sha256": sha(canonical(stable_ast(node))),
        "expression": ast.unparse(node),
    }


def first(tree: ast.Module, predicate: Callable[[ast.AST, str], bool], code: str) -> ast.AST:
    rows: list[ast.AST] = []
    for node in ast.walk(tree):
        try:
            expression = ast.unparse(node)
        except (TypeError, ValueError):
            expression = ""
        if predicate(node, expression):
            rows.append(node)
    require(bool(rows), code)
    return min(rows, key=lambda node: (node.lineno, node.col_offset))


def source_features(oid: str) -> dict[str, Any]:
    raw = blob(oid)
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    required: dict[str, Callable[[ast.AST, str], bool]] = {
        "T_ATTEMPT": lambda n, e: isinstance(n, ast.Assign) and "T_attempt" in e and "I / Q_cell" in e,
        "I_FROM_CRATE": lambda n, e: isinstance(n, ast.Assign) and "I_use" in e and "c * Q_cell" in e,
        "DIRECTION_SIGMA": lambda n, e: isinstance(n, ast.Assign) and "sigma_d" in e and "if s >= 0 else -1" in e,
        "VOLTAGE_SHIFT": lambda n, e: isinstance(n, ast.Assign) and "V_n" in e and "sigma_d * I_abs * self.Rn" in e,
        "ENTROPY_FARADAY": lambda n, e: isinstance(n, ast.Assign) and "dS_eff / F" in e and "num" in e,
        "REVERSIBLE_HEAT": lambda n, e: isinstance(n, ast.Return) and "entropy_coefficient" in e and "float(I)" in e,
        "IRREVERSIBLE_HEAT": lambda n, e: isinstance(n, ast.Return) and "np.asarray(I)" in e and "np.asarray(U_oc" in e and "np.asarray(V" in e,
        "LOGISTIC_DERIVATIVE": lambda n, e: isinstance(n, ast.Assign) and "xi * (1.0 - xi) / w" in e,
        "L_V_OVERRIDE": lambda n, e: isinstance(n, ast.Assign) and "L_V_override" in e and "transition.get('L_V')" in e,
        "L_V_ZERO_CURRENT": lambda n, e: isinstance(n, ast.If) and "I <= 0" in e and "dH_a" in e,
    }
    anchors = {name: anchor(tree, source, first(tree, pred, "E_FEATURE_" + name))
               for name, pred in required.items()}
    optional: dict[str, Callable[[ast.AST, str], bool]] = {
        "MASS_TO_CAPACITY_FRACTION": lambda n, e: isinstance(n, ast.Assign) and "f_Si" in e and "q_gr" in e and "num /" in e,
        "COMPONENT_CAPACITY_SCALE": lambda n, e: isinstance(n, ast.Assign) and "si_scale" in e and "Q_gr0 / Q_si0" in e,
    }
    for name, pred in optional.items():
        rows = []
        for node in ast.walk(tree):
            try:
                expression = ast.unparse(node)
            except (TypeError, ValueError):
                expression = ""
            if pred(node, expression):
                rows.append(node)
        anchors[name] = anchor(tree, source, min(rows, key=lambda n: (n.lineno, n.col_offset))) if rows else None
    comments = [line.strip() for line in source.splitlines()
                if "3600" in line and line.lstrip().startswith("#")]
    executable_divide_3600 = any(
        isinstance(node, (ast.BinOp, ast.AugAssign)) and "/ 3600" in ast.unparse(node)
        for node in ast.walk(tree)
    )
    return {
        "blob_oid": oid,
        "raw_sha256": sha(raw),
        "lf_sha256": sha(lf_bytes(raw)),
        "lf_normalization": "CRLF_AND_LONE_CR_TO_LF",
        "physical_lines": len(source.splitlines()),
        "encoding": "utf-8",
        "ast_parse": "PASS",
        "anchors": anchors,
        "comment_3600_sha256": sha(("\n".join(comments) + ("\n" if comments else "")).encode("utf-8")),
        "comment_3600_count": len(comments),
        "executable_divide_3600": executable_divide_3600,
    }


def dimension(symbol: str, exponents: dict[str, int]) -> dict[str, Any]:
    return {"symbol": symbol, "si_base_exponents": exponents}


def exact() -> dict[str, Any]:
    return {"kind": "EXACT", "absolute": 0.0, "relative": 0.0}


def approximate(atol: float, rtol: float) -> dict[str, Any]:
    return {"kind": "APPROXIMATE", "absolute": atol, "relative": rtol}


def row(row_id: str, family: str, dim: dict[str, Any], basis: str, sign: str,
        formula: str, inputs: dict[str, Any], expected: Any, observed: Any,
        error: float, tolerance: dict[str, Any], disposition: str,
        source_feature_ids: list[str], note: str) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "family": family,
        "dimension": dim,
        "basis": basis,
        "sign_convention": sign,
        "formula": formula,
        "inputs": inputs,
        "expected": expected,
        "observed": observed,
        "error": error,
        "tolerance": tolerance,
        "disposition": disposition,
        "source_feature_ids": source_feature_ids,
        "authority": "INTERNAL_SOFTWARE_NUMERICAL_ONLY",
        "note": note,
    }


def simpson_logistic_area(lo: float, hi: float, center: float, width: float, n: int) -> float:
    require(n > 0 and n % 2 == 0, "E_SIMPSON_N")
    def derivative(v: float) -> float:
        x = 1.0 / (1.0 + math.exp(-(v - center) / width))
        return x * (1.0 - x) / width
    h = (hi - lo) / n
    total = derivative(lo) + derivative(hi)
    total += 4.0 * sum(derivative(lo + h * i) for i in range(1, n, 2))
    total += 2.0 * sum(derivative(lo + h * i) for i in range(2, n, 2))
    return total * h / 3.0


def tolerance_provenance(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    n15_oids = {"5683f9f6701792f8603ce311a3d1702b341ad150",
                "a636c6f21d97f8a1af57b61a6e4afda974b86dca",
                "8ef4ab235a86d623bfc277fb8ba04f30b238b10a",
                "ebce978caa4a21467619443a8e9c333774ad34a6"}
    n16_oids = {*n15_oids,
                "82155e9b0664b4dc50369326679e348727b2c906",
                "742506b061d872afdd094781ea2157faae800943"}
    records = []
    for probe_id, oids, constant_names, gate_name, comparison, method_scope in (
        ("N15", n15_oids, ("R6_G3_K", "R6_G3_RTOL", "R6_G3_NPTS"), "gate_R6_G3",
         {"operator": "<=", "value": 1e-6, "unit": "relative", "converted_value_V_K": None},
         "FROZEN_BLEND_TRAPEZOID_PRECEDENT_FOR_SINGLE_LOGISTIC_SIMPSON"),
        ("N16", n16_oids, ("G2_FD_ANALYTIC_UVK",), "gate_G2",
         {"operator": "<", "value": 0.001, "unit": "uV K^-1", "converted_value_V_K": 1e-9},
         "FROZEN_PRODUCTION_CENTERED_SECANT_PRECEDENT_FOR_INDEPENDENT_PRIMITIVE"),
    ):
        for oid in sorted(oids):
            raw = blob(oid)
            source = raw.decode("utf-8")
            tree = ast.parse(source)
            constants = []
            for name in constant_names:
                node = first(tree, lambda n, _e, expected=name: isinstance(n, ast.Assign)
                             and any(isinstance(target, ast.Name) and target.id == expected
                                     for target in n.targets), "E_TOLERANCE_ANCHOR_" + name)
                require(isinstance(node, ast.Assign), "E_TOLERANCE_ASSIGN")
                constants.append({"name": name, "value": ast.literal_eval(node.value),
                                  "anchor": anchor(tree, source, node)})
            gate = first(tree, lambda n, _e, expected=gate_name:
                         isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == expected,
                         "E_TOLERANCE_GATE_" + gate_name)
            occurrences = sorted(
                [row for row in inventory["occurrence_records"] if row["blob_oid"] == oid],
                key=lambda row: row["ordinal"],
            )
            require(bool(occurrences) and all(row["role"] == "test" for row in occurrences),
                    "E_TOLERANCE_OCCURRENCES")
            records.append({
                "provenance_id": probe_id + "-" + oid[:12], "probe_id": probe_id,
                "relation": "TOLERANCE_PRECEDENT_ONLY", "method_scope": method_scope,
                "blob_oid": oid, "blob_ordinal": occurrences[0]["blob_ordinal"],
                "git_mode": occurrences[0]["git_mode"], "raw_sha256": sha(raw),
                "lf_sha256": sha(lf_bytes(raw)),
                "lf_normalization": "CRLF_AND_LONE_CR_TO_LF", "encoding": "utf-8",
                "size_bytes": len(raw), "physical_lines": len(source.splitlines()),
                "occurrence_refs": [{key: row[key] for key in (
                    "ordinal", "manifest_entry_index", "release", "path")} for row in occurrences],
                "constants": constants, "gate_anchor": anchor(tree, source, gate),
                "comparison": comparison,
            })
    return records


def probe_records() -> list[dict[str, Any]]:
    none = {"kg": 0, "m": 0, "s": 0, "A": 0, "K": 0, "mol": 0}
    voltage = {"kg": 1, "m": 2, "s": -3, "A": -1, "K": 0, "mol": 0}
    current = {"kg": 0, "m": 0, "s": 0, "A": 1, "K": 0, "mol": 0}
    charge = {"kg": 0, "m": 0, "s": 1, "A": 1, "K": 0, "mol": 0}
    power = {"kg": 1, "m": 2, "s": -3, "A": 0, "K": 0, "mol": 0}
    energy = {"kg": 1, "m": 2, "s": -2, "A": 0, "K": 0, "mol": 0}
    entropy_v = {"kg": 1, "m": 2, "s": -3, "A": -1, "K": -1, "mol": 0}
    rows: list[dict[str, Any]] = []
    rate_h = 2.0
    rows.append(row("N01", "RATE_CONVERSION", dimension("s^-1", {**none, "s": -1}),
                    "PHYSICAL_RATE", "NONNEGATIVE_MAGNITUDE", "r_s = r_h / 3600",
                    {"rate_h_inverse": rate_h}, 1.0 / 1800.0, rate_h / 3600.0, 0.0, exact(),
                    "PASS_EXACT", ["T_ATTEMPT", "I_FROM_CRATE"],
                    "A single physical rate is represented in h^-1 and normalized s^-1 with exact factor 3600."))
    lq_t, lq_i, lq_q, lq_dh, lq_ds, lq_x, lq_a = 298.15, 0.2, 1.0, 44000.0, 0.0, 0.5, 10000.0
    lq_r, planck, boltzmann = 8.314, 6.62607015e-34, 1.380649e-23
    def lq_log_formula(rate: float, enthalpy: float) -> float:
        attempt = rate * planck / boltzmann
        log_value = (math.log(attempt / lq_t)
                     - math.log(1.0 + math.exp(-lq_a / (lq_r * lq_t)))
                     + (enthalpy - lq_t * lq_ds) / (lq_r * lq_t)
                     - lq_x * lq_a / (lq_r * lq_t))
        return math.exp(log_value)
    def lq_product_oracle(rate: float, enthalpy: float) -> float:
        return ((rate * planck / (boltzmann * lq_t))
                / (1.0 + math.exp(-lq_a / (lq_r * lq_t)))
                * math.exp((enthalpy - lq_t * lq_ds - lq_x * lq_a) / (lq_r * lq_t)))
    raw_hour = lq_log_formula(lq_i / lq_q, lq_dh)
    raw_second = lq_log_formula((lq_i / lq_q) / 3600.0, lq_dh)
    enthalpy_shift = lq_r * lq_t * math.log(3600.0)
    compensated_second = lq_log_formula((lq_i / lq_q) / 3600.0, lq_dh + enthalpy_shift)
    expected_lq = {
        "raw_hour": lq_product_oracle(lq_i / lq_q, lq_dh),
        "raw_second": lq_product_oracle((lq_i / lq_q) / 3600.0, lq_dh),
        "hour_to_second_ratio": 3600.0,
        "R_T_ln_3600_J_mol": enthalpy_shift,
        "compensated_second": lq_product_oracle((lq_i / lq_q) / 3600.0, lq_dh + enthalpy_shift),
    }
    observed_lq = {"raw_hour": raw_hour, "raw_second": raw_second,
                   "hour_to_second_ratio": raw_hour / raw_second,
                   "R_T_ln_3600_J_mol": enthalpy_shift,
                   "compensated_second": compensated_second}
    lq_error = max(abs(observed_lq[key] - expected_lq[key]) for key in expected_lq)
    rows.append(row("N02", "RATE_SOURCE_GAP", dimension("1", none), "AMBIGUOUS_Ah_OR_C",
                    "POSITIVE", "independent func_L_q algebra for Ah-style and C-style rate bases",
                    {"T_K": lq_t, "I_A_CONVENTION": lq_i, "Q_Ah_STYLE": lq_q,
                     "Q_C_STYLE": 3600.0, "dH_J_mol": lq_dh, "dS_J_mol_K": lq_ds,
                     "x": lq_x, "A_J_mol": lq_a, "executable_seconds_correction": False,
                     "comment_only_compensation_sign": "dH_phys=dH+R*T*ln(3600)",
                     "basis_resolution": "GROUND_NOT_FOUND",
                     "basis_hypotheses": [
                         {"hypothesis": "AH_COMMENT_PLACEHOLDER_ABSORPTION", "selected": False,
                          "comment_scope": "I_over_Q_is_per_hour_and_missing_divide_3600_absorbed_in_dH"},
                         {"hypothesis": "C_COMMENT_DIRECT_SI", "selected": False,
                          "comment_scope": "I_over_Q_is_per_second_and_needs_no_absorption"},
                     ]},
                    expected_lq, observed_lq, lq_error, approximate(1e-12, 1e-12),
                    "COMMENT_ONLY_BASIS_SPLIT_GLOBAL_BASIS_UNRESOLVED", ["T_ATTEMPT", "I_FROM_CRATE"],
                    "The Ah-style and C-style cases are separate; the frozen comment is not an executable correction and no global Q_cell basis is promoted."))
    for rid, sigma, expected, label in (("N03", 1, 3.68, "DISCHARGE"),
                                         ("N04", -1, 3.72, "CHARGE")):
        observed = 3.7 - sigma * 2.0 * 0.01
        rows.append(row(rid, "CURRENT_SIGN", dimension("V", voltage), "ELECTRODE_VOLTAGE",
                        "V_n=V_app-sigma_d*|I|*R_n", "V_n=V_app-sigma_d*I_abs*R_n",
                        {"V_app_V": 3.7, "I_abs_A_convention": 2.0, "R_n_ohm": 0.01,
                         "sigma_d": sigma, "direction_label": label},
                        expected, observed, abs(observed - expected), exact(), "PASS_EXACT",
                        ["DIRECTION_SIGMA", "VOLTAGE_SHIFT"],
                        "Direction label is source-local; current Ampere authority remains a convention, not an external calibration."))
    zero_t, zero_u, zero_q, zero_n, zero_bg = 300.0, 3.5, 2.0, 1.0, 0.1
    zero_r, zero_f = 8.314, 96485.0
    zero_width = zero_n * zero_r * zero_t / zero_f
    zero_v = [3.3, 3.5, 3.7]
    zero_vector = [zero_q / (4.0 * zero_width * math.cosh((v-zero_u)/(2.0*zero_width))**2) + zero_bg
                   for v in zero_v]
    zero_expected = {"s_plus": zero_vector, "s_minus": list(zero_vector)}
    zero_observed = {}
    for label, direction in (("s_plus", 1), ("s_minus", -1)):
        values = []
        for v in zero_v:
            sig = 1.0 / (1.0 + math.exp(-direction*(v-zero_u)/zero_width))
            values.append(zero_q * sig * (1.0-sig) / zero_width + zero_bg)
        zero_observed[label] = values
    rows.append(row("N05", "ZERO_CURRENT_CONDITIONAL", dimension("V^-1", {**none, "kg": -1, "m": -2, "s": 3, "A": 1}),
                    "SOURCE_DECLARED_ZERO_LAG_FIXTURE", "POSITIVE_DQDV",
                    "dQdV=Q*sigmoid*(1-sig)/w+Cbg when I=0 and no direct L_V/dH_a/gamma/Omega",
                    {"V_V": zero_v, "T_K": zero_t, "U_V": zero_u, "Q": zero_q,
                     "n": zero_n, "Cbg": zero_bg, "I_abs": 0.0, "Rn_ohm": 0.01,
                     "L_V": None, "dH_a": None, "gamma": None, "Omega": None,
                     "alpha": 1.0, "s_values": [1, -1]},
                    zero_expected, zero_observed,
                    max(abs(zero_expected[label][i]-zero_observed[label][i])
                        for label in zero_expected for i in range(len(zero_v))),
                    approximate(1e-12, 1e-12), "PASS_CONDITIONAL_TOLERANCE",
                    ["LOGISTIC_DERIVATIVE", "L_V_ZERO_CURRENT", "VOLTAGE_SHIFT"],
                    "This bounded zero-lag fixture is not a universal dqdv(I=0)=equilibrium claim."))
    charge_c = 2.5 * 3600.0
    rows.append(row("N06", "CAPACITY_CONVERSION", dimension("C", charge), "TOTAL_CELL_CAPACITY",
                    "POSITIVE_CHARGE", "Q_C=(Q_mAh/1000)*3600",
                    {"capacity_mAh": 2500.0}, 9000.0, charge_c, 0.0, exact(), "PASS_EXACT",
                    ["I_FROM_CRATE"], "mAh to Ah applies 1000 once; Ah to C applies 3600 once."))
    energy_j = charge_c * 0.1
    rows.append(row("N07", "ENERGY_HEAT_CONVERSION", dimension("J", energy), "INTEGRATED_HEAT",
                    "POSITIVE_DISSIPATION_MAGNITUDE", "E=Q_C*DeltaV",
                    {"capacity_Ah": 2.5, "delta_V": 0.1, "seconds_factor_count": 1,
                     "production_energy_integration_route": "GROUND_NOT_FOUND"},
                    900.0, energy_j, abs(energy_j - 900.0), exact(),
                    "GROUND_NOT_FOUND_PRODUCTION_INDEPENDENT_IDENTITY_PASS",
                    ["I_FROM_CRATE"], "The Ah-to-C factor occurs once; duplicate 3600 would produce 3,240,000 J and is rejected."))
    for rid, faraday in (("N08", 96485.0), ("N09", 96485.33212)):
        expected = 10.0 / faraday
        observed = (10.0 / 2.0) / (faraday / 2.0)
        rows.append(row(rid, "ENTROPY_COEFFICIENT", dimension("V K^-1", entropy_v),
                        "MOLAR_ENTROPY_OVER_FARADAY", "dUdT=dS/F", "dUdT=dS/F",
                        {"dS_J_mol_K": 10.0, "F_C_mol": faraday}, expected, observed,
                        abs(expected - observed), approximate(1e-15, 1e-15), "PASS_TOLERANCE",
                        ["ENTROPY_FARADAY"], "Legacy and SI Faraday constants remain distinct exact input profiles."))
    for rid, d_s, sign in (("N10", 10.0, "NEGATIVE"), ("N11", -10.0, "POSITIVE")):
        expected = -2.0 * 300.0 * (d_s / 96485.0)
        observed = -(2.0 * 300.0 * d_s) / 96485.0
        rows.append(row(rid, "REVERSIBLE_HEAT", dimension("W", power), "INSTANTANEOUS_HEAT",
                        "q_rev=-I*T*dUdT", "q_rev=-I*T*(dS/F)",
                        {"I_A_convention": 2.0, "T_K": 300.0, "dS_J_mol_K": d_s,
                         "expected_sign": sign}, expected, observed, abs(expected - observed),
                        approximate(1e-14, 1e-14), "PASS_TOLERANCE",
                        ["ENTROPY_FARADAY", "REVERSIBLE_HEAT"],
                        "This verifies the frozen software sign convention, not material truth."))
    m, q_si, q_gr = 0.3, 3117.0, 372.0
    numerator = m * q_si
    denominator = numerator + (1.0 - m) * q_gr
    fraction = numerator / denominator
    rows.append(row("N12", "FRACTION_BASIS", dimension("1", none), "CAPACITY_FRACTION_NOT_MASS_FRACTION",
                    "BOUNDED_0_TO_1", "f_Si=m*q_Si/(m*q_Si+(1-m)*q_gr)",
                    {"mass_fraction": m, "q_Si_mAh_g": q_si, "q_gr_mAh_g": q_gr},
                    3117.0 / 3985.0, fraction, abs(fraction - 3117.0 / 3985.0),
                    approximate(1e-15, 1e-15), "PASS_TOLERANCE",
                    ["MASS_TO_CAPACITY_FRACTION"], "m_Si and f_Si are distinct bases."))
    q_si_part, q_gr_part = numerator, (1.0 - m) * q_gr
    rows.append(row("N13", "COMPONENT_TOTAL_CLOSURE", dimension("mAh g^-1", {**charge, "kg": -1}),
                    "ONE_GRAM_MIXTURE_SPECIFIC_CAPACITY", "POSITIVE_COMPONENTS",
                    "Q_total=Q_Si+Q_gr; f_Si=Q_Si/Q_total",
                    {"Q_Si_mAh_g_mix": q_si_part, "Q_gr_mAh_g_mix": q_gr_part},
                    {"Q_total": denominator, "f_Si": fraction},
                    {"Q_total": q_si_part + q_gr_part, "f_Si": q_si_part / (q_si_part + q_gr_part)},
                    0.0, exact(), "PASS_EXACT", ["MASS_TO_CAPACITY_FRACTION", "COMPONENT_CAPACITY_SCALE"],
                    "Component and total capacities close without equating mass and capacity fractions."))
    q_irr = 2.0 * (3.7 - 3.6)
    rows.append(row("N14", "IRREVERSIBLE_HEAT", dimension("W", power), "INSTANTANEOUS_HEAT",
                    "SIGNED_I_TIMES_SIGNED_OVERPOTENTIAL", "q_irr=I*(U_oc-V)",
                    {"I_A_convention": 2.0, "U_oc_V": 3.7, "V_V": 3.6,
                     "universal_nonnegative_guard": "GROUND_NOT_FOUND"},
                    0.2, q_irr, abs(q_irr - 0.2), approximate(1e-15, 1e-15), "PASS_TOLERANCE",
                    ["IRREVERSIBLE_HEAT"],
                    "Nonnegativity is conditional on the signs of I and U_oc-V; the frozen source has no universal guard."))
    center, width = 3.5, 0.08
    lo, hi = center - 20.0 * width, center + 20.0 * width
    analytic_area = (1.0 / (1.0 + math.exp(-(hi - center) / width))
                     - 1.0 / (1.0 + math.exp(-(lo - center) / width)))
    numeric_area = simpson_logistic_area(lo, hi, center, width, 400000)
    rows.append(row("N15", "DQDV_AREA", dimension("1", none), "NORMALIZED_CAPACITY_FRACTION",
                    "INCREASING_LOGISTIC_POSITIVE_AREA", "integral(dxi/dV)dV=xi(hi)-xi(lo)",
                    {"domain_V": [lo, hi], "center_V": center, "width_V": width,
                     "method": "COMPOSITE_SIMPSON", "points": 400001,
                     "window_width_multiples": 20.0, "tolerance_source": "FROZEN_GATE_RTOL_1E-6"},
                    analytic_area, numeric_area, abs(numeric_area - analytic_area),
                    approximate(0.0, 1e-6), "PASS_TOLERANCE", ["LOGISTIC_DERIVATIVE"],
                    "Finite-domain area closes to the analytic endpoint difference."))
    temperature, step_t, d_h, d_s, n_value, x_value = 298.15, 3.0, -30000.0, -20.0, 1.0, 0.25
    gas, faraday = 8.314, 96485.0
    logit = math.log(x_value / (1.0 - x_value))
    primitive = lambda t: (-d_h + t*d_s) / faraday + n_value*gas*t*logit/faraday
    expected_derivative = d_s/faraday + n_value*gas*logit/faraday
    numeric_derivative = (primitive(temperature + step_t) - primitive(temperature - step_t)) / (2.0*step_t)
    rows.append(row("N16", "FINITE_DIFFERENCE_DERIVATIVE", dimension("V K^-1", entropy_v),
                    "THERMODYNAMIC_TEMPERATURE_DERIVATIVE", "SIGNED_DUDT",
                    "centered_secant(U,T,deltaT) versus dS/F+nR/F*log(x/(1-x))",
                    {"T_K": temperature, "delta_T_K": step_t, "dH_J_mol": d_h,
                     "dS_J_mol_K": d_s, "n": n_value, "x": x_value,
                     "method": "CENTERED_SECANT", "tolerance_source": "FROZEN_ENTROPY_GATE_1E-3_uV_PER_K"},
                    expected_derivative, numeric_derivative, abs(numeric_derivative - expected_derivative),
                    approximate(1e-9, 0.0), "PASS_TOLERANCE", ["ENTROPY_FARADAY"],
                    "The independent closed-form primitive supplies the finite-difference oracle; production is only the audited subject."))
    return rows


def build() -> dict[str, Any]:
    inventory = input_json(INVENTORY_PATH, INVENTORY_RAW_SHA256, INVENTORY_SEMANTIC_SHA256)
    attestation = input_json(ATTESTATION_PATH, ATTESTATION_RAW_SHA256, ATTESTATION_SEMANTIC_SHA256)
    state_flow = input_json(STATE_FLOW_PATH, STATE_FLOW_RAW_SHA256, STATE_FLOW_SEMANTIC_SHA256, True)
    occurrences = sorted(
        [row for row in inventory["occurrence_records"] if row["role"] == "code"],
        key=lambda row: RELEASES.index(row["release"]),
    )
    require(len(occurrences) == 20, "E_CODE_OCCURRENCE_COUNT")
    require([row["release"] for row in occurrences] == RELEASES, "E_RELEASE_ORDER")
    require(len({row["blob_oid"] for row in occurrences}) == 15, "E_CODE_BLOB_COUNT")
    source_records = [{key: row[key] for key in (
        "ordinal", "manifest_entry_index", "release", "path", "role", "blob_oid",
        "blob_ordinal", "git_mode", "size_bytes", "physical_lines")}
        for row in occurrences]
    feature_records = []
    for oid in sorted({row["blob_oid"] for row in occurrences}):
        item = source_features(oid)
        refs = [row for row in source_records if row["blob_oid"] == oid]
        item["blob_ordinal"] = refs[0]["blob_ordinal"]
        item["git_mode"] = refs[0]["git_mode"]
        item["size_bytes"] = refs[0]["size_bytes"]
        item["occurrence_refs"] = [{key: row[key] for key in (
            "ordinal", "manifest_entry_index", "release", "path")} for row in refs]
        feature_records.append(item)
    probes = probe_records()
    tolerance_records = tolerance_provenance(inventory)
    require(len(probes) == 16 and [r["row_id"] for r in probes] == [f"N{i:02d}" for i in range(1, 17)],
            "E_PROBE_ORDER")
    require(all(math.isfinite(float(r["error"])) for r in probes), "E_PROBE_FINITE")
    require(all((r["error"] <= r["tolerance"]["absolute"]
                 + r["tolerance"]["relative"] * abs(float(r["expected"])))
                if isinstance(r["expected"], (int, float))
                else r["error"] <= r["tolerance"]["absolute"]
                for r in probes if r["disposition"].startswith("PASS")), "E_PROBE_TOLERANCE")
    require(sum(row["comment_3600_count"] > 0 for row in feature_records) == 3,
            "E_COMMENT_3600_BLOBS")
    require(not any(row["executable_divide_3600"] for row in feature_records),
            "E_EXECUTABLE_3600")
    require(sum(row["anchors"]["MASS_TO_CAPACITY_FRACTION"] is not None for row in feature_records) == 5,
            "E_BLEND_FEATURE_COUNT")
    require(state_flow["universe"]["flow_target_occurrences"] == 20
            and state_flow["universe"]["flow_target_unique_blobs"] == 15, "E_STEP83_PROJECTION")
    result = {
        "schema_version": "phase067-step87-unit-numerical-v1",
        "artifact": OUTPUT_PATH,
        "phase": 67,
        "step": 87,
        "generated_date": DATE,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "branch": BRANCH,
        "expected_subject": SUBJECT,
        "gate": GATE,
        "persistence_terminal": PERSISTENCE,
        "precommit_status": "PASS_PENDING_PERSISTENCE",
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "result_first": True,
        "json_output_last": True,
        "inputs": {
            "inventory": {"path": INVENTORY_PATH, "raw_sha256": INVENTORY_RAW_SHA256,
                          "semantic_sha256": INVENTORY_SEMANTIC_SHA256},
            "attestation": {"path": ATTESTATION_PATH, "raw_sha256": ATTESTATION_RAW_SHA256,
                            "semantic_sha256": ATTESTATION_SEMANTIC_SHA256},
            "state_flow": {"path": STATE_FLOW_PATH, "raw_sha256": STATE_FLOW_RAW_SHA256,
                           "semantic_sha256": STATE_FLOW_SEMANTIC_SHA256},
        },
        "universe": {"code_occurrences": 20, "code_unique_blobs": 15,
                     "probe_rows": 16, "release_count": 20},
        "source_occurrence_records": source_records,
        "source_feature_records": feature_records,
        "probe_records": probes,
        "tolerance_provenance_records": tolerance_records,
        "limitation_records": [{
            "limitation_id": "L01_ZERO_CURRENT_NOT_UNIVERSAL",
            "status": "BOUNDED_NOT_GENERAL",
            "excluded_conditions": ["DIRECT_L_V_OVERRIDE", "HYSTERESIS_GAMMA_OR_OMEGA",
                                    "REVERSED_DIRECTION_WITH_ALPHA_NE_1"],
            "source_feature_ids": ["L_V_OVERRIDE", "L_V_ZERO_CURRENT"],
            "universal_dqdv_zero_equals_equilibrium": False,
            "authority": "INTERNAL_SOFTWARE_NUMERICAL_ONLY",
        }],
        "coverage": {
            "required_families": ["RATE_CONVERSION", "RATE_SOURCE_GAP", "CURRENT_SIGN",
                                  "ZERO_CURRENT_CONDITIONAL", "CAPACITY_CONVERSION", "ENERGY_HEAT_CONVERSION",
                                  "ENTROPY_COEFFICIENT", "REVERSIBLE_HEAT", "FRACTION_BASIS",
                                  "COMPONENT_TOTAL_CLOSURE", "IRREVERSIBLE_HEAT", "DQDV_AREA",
                                  "FINITE_DIFFERENCE_DERIVATIVE"],
            "source_anchor_occurrence_coverage": "20/20",
            "source_blob_feature_coverage": "15/15",
            "comment_only_3600_blob_count": 3,
            "executable_divide_3600_blob_count": 0,
            "blend_feature_blob_count": 5,
            "tolerance_provenance_blob_count": 6,
            "tolerance_provenance_record_count": 10,
            "zero_current_limitation_count": 1,
            "failed_tolerance_rows": 0,
        },
        "authority": {
            "internal_software_consistency": True,
            "internal_numerical_consistency": True,
            "runtime_behavior": False,
            "external_scientific": False,
            "material_parameter": False,
            "experimental": False,
            "canonical": False,
            "publication": False,
            "open_unit_convention": "Q_cell_Ah_OR_C_AND_NO_EXECUTABLE_DIVIDE_BY_3600",
            "open_owner": "STEP88_IMPACT_AND_EXISTING_P066_OPEN_OWNERS",
        },
        "validation": {
            "strict_json_inputs": True,
            "source_git_blob_bound": True,
            "release_order_exact": True,
            "typed_numeric_vectors": True,
            "nonfinite_count": 0,
            "duplicate_row_count": 0,
            "failed_tolerance_count": 0,
            "determinism_runs": 2,
            "determinism_matches": 2,
        },
        "semantic_sha256": "",
    }
    return finish(result)


def atomic_write(path: Path, raw: bytes) -> None:
    require(not path.exists(), "E_OUTPUT_EXISTS")
    temp = path.with_name(path.name + ".tmp-phase067-step87")
    require(not temp.exists(), "E_TEMP_EXISTS")
    try:
        with temp.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preview", action="store_true")
    group.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    first_value = build()
    second_value = build()
    require(canonical(first_value) == canonical(second_value), "E_NONDETERMINISTIC")
    if args.collect:
        atomic_write(ROOT / OUTPUT_PATH, canonical(first_value))
    print("PASS_P067_STEP87_PREVIEW"
          if args.preview else GATE,
          "occurrences=20 blobs=15 probes=16 determinism=2/2",
          "semantic=" + first_value["semantic_sha256"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
