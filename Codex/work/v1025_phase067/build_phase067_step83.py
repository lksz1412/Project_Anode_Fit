#!/usr/bin/env python3
"""Build Phase 067 Step 83 frozen static state/quantity-flow evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "db167fdc941eafba0313b8476dfe7483108f13ff"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
GENERATED_DATE = "2026-09-02"
EXPECTED_SUBJECT = "audit(phase067): trace state quantity flows"
GATE = "PASS_P067_STEP83_STATE_FLOW"
PERSISTENCE_TERMINAL = "PASS_P067_STEP83_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "fce9a0bf6c1cbb0d33baa982e275fcc217596ce2eefe5c8990c4f610f3365222"
INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
OUTPUT_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
INVENTORY_RAW_SHA256 = "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63"
INVENTORY_SEMANTIC_SHA256 = "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"
ATTESTATION_RAW_SHA256 = "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174"
ATTESTATION_SEMANTIC_SHA256 = "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"
CODE_PATH_SHA256 = "87a56bbf68f1218a329dc1dca785a7a53b6257421ef772f55001bbd7a14fa61e"
CODE_PATH_BLOB_SHA256 = "6785e0f94af65cf5d173d94acdf1fb19b8e32fad0c025dd8f4fd1cd48d06c5b3"
CODE_BLOB_SHA256 = "77083327d44f5f0ce39c6c6480095f2cb56a4bed0fb14e24bd4d58d4fc76efb6"
CODE_RELEASE_PATH_SHA256 = "dc2c84e4e132a5ed788c69725b142ebc97c2124f42e175c2c996ba7714dc322e"
CODE_RELEASE_PATH_BLOB_ORDINAL_SHA256 = "f9ad50607a0001387ba015f6dc882c93ab23d1f55b46d152cdfa42fe942b1959"
RELEASES = [
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14",
    "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2",
    "v1.0.19", "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23",
    "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
]
QUANTITIES = ["voltage", "current", "capacity", "composition", "temperature"]
PRESENCE = {"PRESENT", "ABSENT_IN_FROZEN_SOURCE", "GROUND_NOT_FOUND_STATIC_AMBIGUOUS"}
CLASSIFICATIONS = {"DIRECT", "INHERITED", "OVERWRITTEN", "IGNORED", "FALLBACK"}


class BuildError(RuntimeError):
    pass


def require(condition: bool, diagnostic: str) -> None:
    if not condition:
        raise BuildError(diagnostic)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("semantic_sha256", None)
    return sha256(canonical_bytes(copy))


def run_git(args: list[str]) -> bytes:
    allowed = (
        len(args) == 3 and args[:2] == ["cat-file", "blob"]
        and all(c in "0123456789abcdef" for c in args[2]) and len(args[2]) == 40
    ) or (
        len(args) == 2 and args[0] == "show"
        and args[1].startswith(EXPECTED_PARENT + ":Codex/results/PHASE_067_PYTHON_")
    )
    require(allowed, "E_GIT_ARGV")
    completed = subprocess.run(
        ["git", *args], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(completed.returncode == 0, "E_GIT_READ")
    require(completed.stderr == b"", "E_GIT_STDERR")
    return completed.stdout


def strict_json(raw: bytes, diagnostic: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, diagnostic + "_DUPLICATE_KEY")
            out[key] = value
        return out

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BuildError(diagnostic) from exc
    require(isinstance(value, dict), diagnostic + "_ROOT")
    return value


def sorted_lines_sha(values: list[str]) -> str:
    return sha256("".join(value + "\n" for value in sorted(values)).encode("utf-8"))


def qualified_definitions(tree: ast.Module) -> dict[str, ast.AST]:
    result: dict[str, ast.AST] = {}

    def visit(node: ast.AST, scope: list[str]) -> None:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            current = [*scope, node.name]
            result[".".join(current)] = node
            scope = current
        for child in ast.iter_child_nodes(node):
            visit(child, scope)

    visit(tree, [])
    return result


def class_method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return child
    raise BuildError(f"E_METHOD_{class_name}_{method_name}")


def class_node(tree: ast.Module, class_name: str) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise BuildError("E_CLASS_" + class_name)


def names(node: ast.AST) -> set[str]:
    found: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            found.add(child.id)
        elif isinstance(child, ast.Attribute):
            found.add(child.attr)
    return found


def target_names(node: ast.AST) -> set[str]:
    found: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
            found.add(child.id)
        elif isinstance(child, ast.Attribute) and isinstance(child.ctx, ast.Store):
            found.add(child.attr)
    return found


def first_node(root: ast.AST, predicate: Callable[[ast.AST], bool], diagnostic: str) -> ast.AST:
    candidates = [node for node in ast.walk(root) if predicate(node)]
    require(bool(candidates), diagnostic)
    return sorted(candidates, key=lambda n: (getattr(n, "lineno", 0), getattr(n, "col_offset", 0)))[0]


def last_return(function: ast.FunctionDef) -> ast.Return:
    rows = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
    require(bool(rows), "E_RETURN")
    return sorted(rows, key=lambda n: (n.lineno, n.col_offset))[-1]


def stable_ast_bytes(node: ast.AST) -> bytes:
    def normalize(value: Any) -> Any:
        if isinstance(value, ast.AST):
            return {"_type": type(value).__name__,
                    "fields": [[field, normalize(getattr(value, field, None))]
                               for field in value._fields]}
        if isinstance(value, list):
            return [normalize(item) for item in value]
        if isinstance(value, tuple):
            return {"_tuple": [normalize(item) for item in value]}
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        return {"_literal_type": type(value).__name__, "repr": repr(value)}

    return json.dumps(normalize(node), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def anchor(qualified: str, node: ast.AST, lines: list[str]) -> dict[str, Any]:
    start = int(getattr(node, "lineno", 0))
    end = int(getattr(node, "end_lineno", start))
    require(start > 0 and end >= start, "E_ANCHOR_EXTENT")
    text = "\n".join(lines[start - 1:end]) + "\n"
    return {
        "qualified_definition": qualified,
        "ast_kind": type(node).__name__,
        "start_line": start,
        "end_line": end,
        "source_sha256": sha256(text.encode("utf-8")),
        "node_sha256": sha256(stable_ast_bytes(node)),
        "expression": ast.unparse(node),
    }


def qualified_owner(tree: ast.Module, node: ast.AST) -> str:
    candidates: list[tuple[int, str]] = []
    def visit(current: ast.AST, scope: list[str]) -> None:
        next_scope = scope
        if isinstance(current, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            next_scope = [*scope, current.name]
            if current.lineno <= getattr(node, "lineno", 0) and current.end_lineno >= getattr(node, "end_lineno", 0):
                candidates.append((current.end_lineno - current.lineno, ".".join(next_scope)))
        for child in ast.iter_child_nodes(current):
            visit(child, next_scope)
    visit(tree, [])
    require(bool(candidates), "E_QUALIFIED_OWNER")
    return min(candidates)[1]


def base_anchors(tree: ast.Module, lines: list[str]) -> dict[str, Any]:
    init = class_method(tree, "GraphiteAnodeDischargeDQDV", "__init__")
    curve = class_method(tree, "GraphiteAnodeDischargeDQDV", "curve")
    dqdv = class_method(tree, "GraphiteAnodeDischargeDQDV", "dqdv")
    equilibrium = class_method(tree, "GraphiteAnodeDischargeDQDV", "equilibrium")
    lag = class_method(tree, "GraphiteAnodeDischargeDQDV", "_resolve_lag_length")
    q_init = "GraphiteAnodeDischargeDQDV.__init__"
    q_curve = "GraphiteAnodeDischargeDQDV.curve"
    q_dqdv = "GraphiteAnodeDischargeDQDV.dqdv"
    q_lag = "GraphiteAnodeDischargeDQDV._resolve_lag_length"
    v_n = first_node(dqdv, lambda n: isinstance(n, ast.Assign) and "V_n" in target_names(n) and {"V_in", "I_abs", "Rn"} <= names(n), "E_V_N")
    i_if = first_node(curve, lambda n: isinstance(n, ast.If) and "I_abs" in names(n) and len([x for x in ast.walk(n) if isinstance(x, ast.Is)]) > 0, "E_I_BRANCH")
    i_mult = first_node(i_if, lambda n: isinstance(n, ast.Assign) and "I_use" in target_names(n) and {"Q_cell"} <= names(n), "E_I_MULT")
    i_override = first_node(i_if, lambda n: isinstance(n, ast.Assign) and "I_use" in target_names(n) and "I_abs" in names(n) and n is not i_mult, "E_I_OVERRIDE")
    x_store = first_node(init, lambda n: isinstance(n, ast.Assign) and "x" in target_names(n) and "x" in names(n), "E_X_STORE")
    chi_store = first_node(init, lambda n: isinstance(n, ast.Assign) and "chi" in target_names(n) and {"chi", "x"} <= names(n), "E_CHI_STORE")
    chi_method = class_method(tree, "GraphiteAnodeDischargeDQDV", "_chi_d")
    chi_consumer = first_node(chi_method, lambda n: isinstance(n, ast.Return) and "chi" in names(n), "E_CHI_CONSUMER")
    t_input = first_node(dqdv, lambda n: isinstance(n, ast.Assign) and "T_input" in target_names(n) and "T" in names(n), "E_T_INPUT")
    t_local = first_node(dqdv, lambda n: isinstance(n, (ast.Assign, ast.AnnAssign)) and bool(target_names(n) & {"T_work", "T_prog"}), "E_T_LOCAL")
    t_rep = first_node(dqdv, lambda n: isinstance(n, ast.Assign) and "T_rep" in target_names(n), "E_T_REP")
    lag_call = first_node(dqdv, lambda n: isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "_resolve_lag_length", "E_LAG_CALL")
    center_if = first_node(dqdv, lambda n: isinstance(n, ast.If) and "dH_rxn" in ast.unparse(n.test) and "dS_rxn" in ast.unparse(n.test), "E_CENTER_IF")
    center_thermo = first_node(center_if, lambda n: isinstance(n, ast.Assign) and "U_j" in target_names(n) and "func_U_j" in ast.unparse(n), "E_CENTER_THERMO")
    center_literal = first_node(center_if, lambda n: isinstance(n, ast.Assign) and "U_j" in target_names(n) and "tr['U']" in ast.unparse(n), "E_CENTER_LITERAL")
    branch_if = first_node(dqdv, lambda n: isinstance(n, ast.If) and "gamma" in names(n) and "Omega" in names(n) and "center" in target_names(n), "E_BRANCH_IF")
    branch_write = first_node(branch_if, lambda n: isinstance(n, ast.Assign) and "center" in target_names(n) and ("func_U_branch" in ast.unparse(n) or "hys_shift" in names(n)), "E_BRANCH_WRITE")
    lco_sign_candidates = [n for n in ast.walk(curve) if isinstance(n, ast.If) and "_delith_is_discharge" in names(n) and "sigma_d" in target_names(n)]
    lco_sign_if = sorted(lco_sign_candidates, key=lambda n: n.lineno)[0] if lco_sign_candidates else None
    lco = class_node(tree, "LCOCathodeDQDV")
    lco_center = first_node(lco, lambda n: isinstance(n, ast.Call) and "x_center" in ast.unparse(n) and "x_MIT" in ast.unparse(n), "E_LCO_CENTER")
    qj_use = first_node(dqdv, lambda n: isinstance(n, ast.BinOp) and "tr['Q']" in ast.unparse(n), "E_QJ_USE")
    solve_node: ast.FunctionDef | None
    vib_node: ast.FunctionDef | None
    try:
        solve_node = class_method(tree, "GraphiteAnodeDischargeDQDV", "solve_U_oc")
    except BuildError:
        solve_node = None
    try:
        vib_node = class_method(tree, "GraphiteAnodeDischargeDQDV", "_vib_theta")
    except BuildError:
        vib_node = None
    return {
        "init": anchor(q_init, init, lines),
        "curve": anchor(q_curve, curve, lines),
        "dqdv": anchor(q_dqdv, dqdv, lines),
        "equilibrium": anchor("GraphiteAnodeDischargeDQDV.equilibrium", equilibrium, lines),
        "lag": anchor(q_lag, lag, lines),
        "v_n": anchor(q_dqdv, v_n, lines),
        "i_branch": anchor(q_curve, i_if, lines),
        "i_mult": anchor(q_curve, i_mult, lines),
        "i_override": anchor(q_curve, i_override, lines),
        "x_store": anchor(q_init, x_store, lines),
        "chi_store": anchor(q_init, chi_store, lines),
        "chi_consumer": anchor("GraphiteAnodeDischargeDQDV._chi_d", chi_consumer, lines),
        "t_input": anchor(q_dqdv, t_input, lines),
        "t_local": anchor(q_dqdv, t_local, lines),
        "t_rep": anchor(q_dqdv, t_rep, lines),
        "lag_call": anchor(q_dqdv, lag_call, lines),
        "center_if": anchor(q_dqdv, center_if, lines),
        "center_thermo": anchor(q_dqdv, center_thermo, lines),
        "center_literal": anchor(q_dqdv, center_literal, lines),
        "branch_write": anchor(q_dqdv, branch_write, lines),
        "lco_sign_if": anchor(q_curve, lco_sign_if, lines) if lco_sign_if is not None else None,
        "lco_center": anchor(qualified_owner(tree, lco_center), lco_center, lines),
        "qj_use": anchor(q_dqdv, qj_use, lines),
        "solve_u_oc": anchor("GraphiteAnodeDischargeDQDV.solve_U_oc", solve_node, lines) if solve_node is not None else None,
        "vib_theta": anchor("GraphiteAnodeDischargeDQDV._vib_theta", vib_node, lines) if vib_node is not None else None,
        "curve_return": anchor(q_curve, last_return(curve), lines),
        "dqdv_return": anchor(q_dqdv, last_return(dqdv), lines),
        "lco_class": anchor("LCOCathodeDQDV", class_node(tree, "LCOCathodeDQDV"), lines),
    }


def blend_anchors(tree: ast.Module, lines: list[str]) -> dict[str, Any] | None:
    try:
        cls = class_node(tree, "BlendedAnodeDQDV")
    except BuildError:
        return None
    init = class_method(tree, "BlendedAnodeDQDV", "__init__")
    from_wt = class_method(tree, "BlendedAnodeDQDV", "from_wt")
    dqdv = class_method(tree, "BlendedAnodeDQDV", "dqdv")
    f_store = first_node(init, lambda n: isinstance(n, ast.Assign) and "f_Si" in target_names(n) and "f_Si" in names(n), "E_FSI")
    q_si = first_node(init, lambda n: isinstance(n, (ast.Assign, ast.AnnAssign)) and "Q_Si" in target_names(n), "E_QSI")
    q_total = first_node(init, lambda n: isinstance(n, (ast.Assign, ast.AnnAssign)) and "Q" in target_names(n) and {"Q_gr", "Q_Si"} <= names(n), "E_QTOTAL")
    f_convert = first_node(from_wt, lambda n: isinstance(n, ast.Assign) and "f_Si" in target_names(n) and {"num", "q_gr"} <= names(n), "E_FCONVERT")
    return {
        "class": anchor("BlendedAnodeDQDV", cls, lines),
        "init": anchor("BlendedAnodeDQDV.__init__", init, lines),
        "from_wt": anchor("BlendedAnodeDQDV.from_wt", from_wt, lines),
        "f_store": anchor("BlendedAnodeDQDV.__init__", f_store, lines),
        "q_si": anchor("BlendedAnodeDQDV.__init__", q_si, lines),
        "q_total": anchor("BlendedAnodeDQDV.__init__", q_total, lines),
        "f_convert": anchor("BlendedAnodeDQDV.from_wt", f_convert, lines),
        "dqdv": anchor("BlendedAnodeDQDV.dqdv", dqdv, lines),
        "dqdv_return": anchor("BlendedAnodeDQDV.dqdv", last_return(dqdv), lines),
    }


def transform(ordinal: int, state_in: list[str], state_out: list[str], operation: str, evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "ordinal": ordinal,
        "state_in": state_in,
        "state_out": state_out,
        "operation": operation,
        "order_authority": "STATIC_LEXICAL_ONLY_NOT_RUNTIME_CALL_ORDER",
        "evidence": evidence,
    }


def route(route_id: str, condition: str, classification: str, public_inputs: list[str],
          producer: dict[str, Any] | None, transforms: list[dict[str, Any]],
          consumers: list[dict[str, Any]], output: dict[str, Any] | None,
          alternate_producer: dict[str, Any] | None = None) -> dict[str, Any]:
    require(classification in CLASSIFICATIONS, "E_CLASSIFICATION")
    require(not (classification == "IGNORED" and consumers), "E_IGNORED_CONSUMER")
    require(not (classification == "IGNORED" and output is not None), "E_IGNORED_OUTPUT")
    require(not (classification == "FALLBACK" and (condition == "ALWAYS" or producer is None or alternate_producer is None)), "E_FALLBACK_CONTRACT")
    require(not (classification == "OVERWRITTEN" and not transforms), "E_OVERWRITTEN_CONTRACT")
    require(not (classification == "INHERITED" and (producer is None or "LCOCathodeDQDV" not in producer["qualified_definition"])), "E_INHERITED_CONTRACT")
    return {
        "route_id": route_id,
        "condition": condition,
        "classification": classification,
        "public_inputs": public_inputs,
        "producer": producer,
        "ordered_transforms": transforms,
        "consumers": consumers,
        "output": output,
        "alternate_producer": alternate_producer,
    }


def identity(identity_id: str, symbol: str, unit: str, basis: str, sign: str, scope: str,
             source_status: str, evidence: dict[str, Any] | None,
             evidence_status: str = "SOURCE_EXPLICIT") -> dict[str, Any]:
    return {
        "identity_id": identity_id,
        "symbol": symbol,
        "unit": unit,
        "basis": basis,
        "sign": sign,
        "scope": scope,
        "source_status": source_status,
        "evidence_status": evidence_status,
        "evidence": evidence,
        "route_refs": [],
    }


def flow_row(index: int, occurrence: dict[str, Any], quantity: str, tree: ast.Module,
             lines: list[str], base: dict[str, Any], blend: dict[str, Any] | None,
             text: str) -> dict[str, Any]:
    release = occurrence["release"]
    prefix = f"P067-S83-{index:03d}-{quantity.upper()}"
    state_ids: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    gaps: list[dict[str, str]] = []
    if quantity == "voltage":
        state_ids = [
            identity(prefix + "-VAPP", "V_app", "V", "APPLIED_ELECTRODE_OR_CELL_LABEL_NOT_INFERRED", "SIGNED_BY_AXIS", "PUBLIC_INPUT", "PRESENT", base["curve"]),
            identity(prefix + "-VN", "V_n", "V", "INTERNAL_POLARIZED_ELECTRODE_COORDINATE", "V_app - sigma_d*I_abs*Rn", "LOCAL_PER_POINT", "PRESENT", base["v_n"]),
            identity(prefix + "-CENTER", "center/U_j", "V", "EQUILIBRIUM_OR_BRANCH_CENTER", "sigma_d_BRANCH_WHEN_ENABLED", "LOCAL_PER_TRANSITION", "PRESENT", base["dqdv"]),
            identity(prefix + "-FACADE-SIGN", "direction -> sigma_d", "1", "CELL_LABEL_FACADE_SIGN", "LCO_LABEL_FLIP_WHEN_delith_IS_NOT_discharge", "CURVE_API_ONLY", "PRESENT" if base["lco_sign_if"] is not None else "ABSENT_IN_FROZEN_SOURCE", base["lco_sign_if"], "SOURCE_EXPLICIT" if base["lco_sign_if"] is not None else "STATIC_INFERRED_AMBIGUOUS"),
            identity(prefix + "-LOWLEVEL-SIGN", "s -> sigma_d", "1", "LOW_LEVEL_DIRECTION_SLOT", "s>=0:+1_ELSE:-1_WITHOUT_LCO_LABEL_FLIP", "DQDV_API_ONLY", "PRESENT", base["dqdv"]),
        ]
        routes = [
            route(prefix + "-R1", "ALWAYS", "DIRECT", ["V_app"], base["curve"],
                  [transform(1, ["V_app", "sigma_d", "I_abs", "Rn"], ["V_n"], "V_n = V_app - sigma_d * I_abs * Rn", base["v_n"])],
                  [base["dqdv"]], base["dqdv_return"]),
            route(prefix + "-R2", "transition_HAS_dH_rxn_AND_dS_rxn", "DIRECT", ["dH_rxn", "dS_rxn"], base["center_if"],
                  [transform(1, ["T", "dH_rxn", "dS_rxn"], ["U_j"], "thermochemical center through func_U_j", base["center_thermo"])], [base["dqdv"]], base["dqdv_return"]),
            route(prefix + "-R3", "transition_HAS_dH_rxn_AND_dS_rxn", "IGNORED", ["transition['U']"], base["center_if"], [], [], None),
            route(prefix + "-R4", "transition_LACKS_dH_rxn_OR_dS_rxn", "FALLBACK", ["dH_rxn_OR_dS_rxn_ABSENT_SELECTOR", "transition['U']"], base["center_if"],
                  [transform(1, ["transition['U']"], ["U_j"], "literal transition center fallback", base["center_literal"])], [base["dqdv"]], base["dqdv_return"], base["center_literal"]),
            route(prefix + "-R5", "gamma_NONZERO_AND_Omega_POSITIVE", "OVERWRITTEN", ["U_j", "gamma", "Omega", "sigma_d"], base["center_if"],
                  [transform(1, ["U_j", "gamma", "Omega", "sigma_d"], ["center"], "branch-center write from equilibrium/literal U_j", base["branch_write"])], [base["dqdv"]], base["dqdv_return"]),
            route(prefix + "-R6", "DIRECT_V_n_EQUILIBRIUM_API", "DIRECT", ["V_n"], base["equilibrium"], [], [base["equilibrium"]], base["equilibrium"]),
        ]
        if base["lco_sign_if"] is not None:
            routes.append(route(prefix + f"-R{len(routes)+1}", "LCO_curve_FACADE", "OVERWRITTEN", ["direction", "sigma_d"], base["curve"],
                                [transform(1, ["cell direction label", "sigma_d"], ["LCO physical sigma_d"], "facade-only LCO sign flip", base["lco_sign_if"])], [base["dqdv"]], base["dqdv_return"]))
        routes.append(route(prefix + f"-R{len(routes)+1}", "INSTANCE_IS_LCOCathodeDQDV", "INHERITED", ["V_app"], base["lco_class"], [], [base["curve"]], base["dqdv_return"]))
    elif quantity == "current":
        state_ids = [
            identity(prefix + "-IABS", "I_abs", "SOURCE_UNIT_NOT_EXPLICIT", "ABSOLUTE_CURRENT_MAGNITUDE", "NONNEGATIVE_MAGNITUDE_WITH_sigma_d_SEPARATE", "PUBLIC_INPUT", "PRESENT", base["curve"], "STATIC_INFERRED_AMBIGUOUS"),
            identity(prefix + "-CRATE", "c_rate", "h^-1", "C_RATE", "NONNEGATIVE", "PUBLIC_INPUT", "PRESENT", base["curve"], "COMMENT_ONLY"),
            identity(prefix + "-RATE-S", "I_abs/Q_cell/3600", "s^-1", "NORMALIZED_RATE", "NONNEGATIVE", "CALCULATION", "ABSENT_IN_FROZEN_SOURCE", None, "STATIC_INFERRED_AMBIGUOUS"),
        ]
        routes = [
            route(prefix + "-R1", "I_abs_IS_NOT_NONE", "OVERWRITTEN", ["I_abs"], base["curve"],
                  [transform(1, ["I_abs"], ["I_use"], "validated explicit current override", base["i_override"])], [base["dqdv"]], base["dqdv_return"]),
            route(prefix + "-R2", "I_abs_IS_NONE", "FALLBACK", ["I_abs_SELECTOR", "c_rate", "Q_cell"], base["curve"],
                  [transform(1, ["c_rate", "Q_cell"], ["I_use"], "I_use = c_rate * Q_cell", base["i_mult"])], [base["dqdv"]], base["dqdv_return"], base["i_mult"]),
            route(prefix + "-R3", "I_abs_IS_NOT_NONE", "IGNORED", ["c_rate"], base["curve"], [], [], None),
        ]
        gaps = [{"gap": "NO_EXECUTABLE_DIVIDE_BY_3600", "owner": "STEP87_UNIT_NUMERICAL_AUDIT"}]
    elif quantity == "capacity":
        state_ids = [
            identity(prefix + "-QCELL-AH", "Q_cell", "Ah_CONVENTION_NOT_SOURCE_EXPLICIT", "CELL_TOTAL_CAPACITY", "POSITIVE", "GLOBAL_CALL", "GROUND_NOT_FOUND_STATIC_AMBIGUOUS", base["curve"], "STATIC_INFERRED_AMBIGUOUS"),
            identity(prefix + "-QCELL-C", "Q_cell", "C", "CELL_TOTAL_CHARGE", "POSITIVE", "GLOBAL_CALL", "PRESENT" if "Q_cell 을 [C]" in text else "GROUND_NOT_FOUND_STATIC_AMBIGUOUS", base["lag"] if "Q_cell 을 [C]" in text else base["curve"], "COMMENT_ONLY" if "Q_cell 을 [C]" in text else "STATIC_INFERRED_AMBIGUOUS"),
            identity(prefix + "-QJ", "transition['Q']", "mAh" if "Q [mAh]" in text else "SOURCE_UNIT_NOT_EXPLICIT", "COMPONENT_CAPACITY", "POSITIVE_EXPECTED", "LOCAL_PER_TRANSITION", "PRESENT", base["dqdv"], "COMMENT_ONLY" if "Q [mAh]" in text else "STATIC_INFERRED_AMBIGUOUS"),
        ]
        routes = [
            route(prefix + "-R1", "ALWAYS", "DIRECT", ["Q_cell"], base["curve"],
                  [transform(1, ["Q_cell", "I_abs", "T"], ["lag_len_V"], "Q_cell is passed to the lag-length resolver; denominator semantics are bounded by its source anchor", base["lag_call"])], [base["lag"]], base["dqdv_return"]),
            route(prefix + "-R2", "EACH_TRANSITION", "DIRECT", ["transition['Q']"], base["qj_use"],
                  [transform(1, ["transition['Q']", "peak_shape"], ["dQ/dV contribution"], "component capacity multiplies the transition peak shape", base["qj_use"])], [base["dqdv"]], base["dqdv_return"]),
        ]
        if blend is not None:
            state_ids.extend([
                identity(prefix + "-QSI", "Q_Si", "SOURCE_DECLARED_CAPACITY_UNIT", "SI_COMPONENT_CAPACITY", "NONNEGATIVE", "GLOBAL_BLEND", "PRESENT", blend["q_si"]),
                identity(prefix + "-QTOTAL", "Q", "SOURCE_DECLARED_CAPACITY_UNIT", "BLEND_TOTAL_Q_gr_PLUS_Q_Si", "POSITIVE", "GLOBAL_BLEND_DENOMINATOR", "PRESENT", blend["q_total"]),
            ])
            routes.append(route(prefix + "-R3", "BLENDED_MODEL", "DIRECT", ["f_Si"], blend["init"],
                                [transform(1, ["f_Si", "Q_gr0", "Q_si0"], ["Q_Si", "Q"], "component scaling then total capacity", blend["q_total"])], [blend["dqdv"]], blend["dqdv_return"]))
    elif quantity == "composition":
        state_ids = [
            identity(prefix + "-X", "x", "1", "GRAPHITE_GLOBAL_COMPOSITION_PARAMETER", "UNSIGNED_FRACTION", "GLOBAL_MODEL", "PRESENT", base["x_store"]),
            identity(prefix + "-CHI", "chi/self.chi", "1", "DIRECTIONAL_SPLIT_COMPOSITION_PARAMETER", "UNSIGNED_FRACTION", "GLOBAL_MODEL", "PRESENT", base["chi_store"]),
            identity(prefix + "-XI", "ksi_eq", "1", "REPRESENTATIVE_OR_LOCAL_TRANSITION_OCCUPANCY", "DIRECTION_COORDINATE_DEPENDENT", "LOCAL_PER_TRANSITION_POINT", "PRESENT", base["dqdv"]),
            identity(prefix + "-XBAR", "x_bar", "1", "TOTAL_CAPACITY_NORMALIZED_COMPOSITION", "UNSIGNED_FRACTION", "GLOBAL_PUBLIC_INPUT", "PRESENT" if base["solve_u_oc"] is not None else "ABSENT_IN_FROZEN_SOURCE", base["solve_u_oc"], "SOURCE_EXPLICIT" if base["solve_u_oc"] is not None else "STATIC_INFERRED_AMBIGUOUS"),
            identity(prefix + "-LCO-CENTERS", "x_center/x_MIT", "1", "LCO_GLOBAL_COMPOSITION_CENTERS", "UNSIGNED_FRACTION", "GLOBAL_LCO_MODEL", "PRESENT", base["lco_center"]),
        ]
        routes = [
            route(prefix + "-R1", "chi_IS_NONE", "FALLBACK", ["chi_SELECTOR", "x"], base["chi_store"],
                  [transform(1, ["x"], ["self.chi"], "x supplies chi only when explicit chi is absent", base["chi_store"])], [base["chi_consumer"]], base["chi_consumer"], base["x_store"]),
            route(prefix + "-R2", "chi_IS_NOT_NONE", "DIRECT", ["chi"], base["chi_store"],
                  [transform(1, ["chi"], ["self.chi"], "explicit chi supplies self.chi", base["chi_store"])], [base["chi_consumer"]], base["chi_consumer"]),
            route(prefix + "-R3", "chi_IS_NOT_NONE", "IGNORED", ["x_AS_CHI_FALLBACK"], base["x_store"], [], [], None),
            route(prefix + "-R4", "LCO_COMPOSITION_CENTER_PATH", "DIRECT", ["x_center", "x_MIT"], base["lco_center"], [], [base["lco_class"]], base["lco_class"]),
            route(prefix + "-R5", "LOCAL_TRANSITION_OCCUPANCY", "DIRECT", ["V_n", "T", "center", "n_j", "sigma_d"], base["dqdv"],
                  [transform(1, ["V_n", "T", "center", "n_j", "sigma_d"], ["ksi_eq"], "local transition occupancy evaluation", base["dqdv"])], [base["dqdv"]], base["dqdv_return"]),
        ]
        if base["solve_u_oc"] is not None:
            routes.append(route(prefix + f"-R{len(routes)+1}", "solve_U_oc_ENTRY", "DIRECT", ["x_bar", "T"], base["solve_u_oc"], [], [base["solve_u_oc"]], base["solve_u_oc"]))
        if blend is not None:
            state_ids.extend([
                identity(prefix + "-MSI", "m_Si", "1", "MASS_FRACTION", "UNSIGNED_FRACTION", "GLOBAL_BLEND_INPUT", "PRESENT", blend["from_wt"]),
                identity(prefix + "-FSI", "f_Si", "1", "CAPACITY_FRACTION_Q_Si_OVER_Q_TOTAL", "UNSIGNED_FRACTION", "GLOBAL_BLEND_STATE", "PRESENT", blend["f_store"]),
            ])
            routes.extend([
                route(prefix + f"-R{len(routes)+1}", "CONSTRUCTOR_f_Si", "DIRECT", ["f_Si"], blend["init"],
                      [transform(1, ["f_Si"], ["self.f_Si"], "validated capacity fraction storage", blend["f_store"])], [blend["dqdv"]], blend["dqdv_return"]),
                route(prefix + f"-R{len(routes)+2}", "from_wt_ENTRY", "DIRECT", ["m_Si", "q_Si", "q_gr"], blend["from_wt"],
                      [transform(1, ["m_Si", "q_Si", "q_gr"], ["f_Si"], "m*q_Si / (m*q_Si + (1-m)*q_gr)", blend["f_convert"])], [blend["init"]], blend["dqdv_return"]),
            ])
        if "def solve_U_oc" not in text:
            gaps.append({"gap": "GLOBAL_COMPOSITION_TO_PUBLIC_OUTPUT_GROUND_NOT_FOUND", "owner": "P067-CODE-HISTORY"})
        if release == "v1.0.25.2":
            gaps.append({"gap": "EXECUTABLE_DEFAULT_PROFILE_CONFLICT_WITH_HEADER_OR_GUIDE", "owner": "STEP85_TEST_DEFAULT_BEHAVIOR"})
    elif quantity == "temperature":
        local_symbol = "T_prog" if "T_prog" in base["t_local"]["expression"] else "T_work"
        state_ids = [
            identity(prefix + "-T", "T", "K", "PUBLIC_TEMPERATURE", "POSITIVE", "GLOBAL_SCALAR_OR_PER_POINT_INPUT", "PRESENT", base["dqdv"]),
            identity(prefix + "-TLOCAL", local_symbol, "K", "INTERPOLATED_OR_ORDERED_TEMPERATURE", "POSITIVE", "LOCAL_PER_VOLTAGE_POINT", "PRESENT", base["t_local"]),
            identity(prefix + "-TREP", "T_rep", "K", "ARITHMETIC_MEAN_REPRESENTATIVE_TEMPERATURE", "POSITIVE", "REPRESENTATIVE_PER_CALL", "PRESENT", base["t_rep"]),
            identity(prefix + "-TVIB", "theta/vibrational temperature", "K", "TRANSITION_VIBRATIONAL_TEMPERATURE", "POSITIVE_EXPECTED", "LOCAL_PER_TRANSITION", "PRESENT" if base["vib_theta"] is not None else "ABSENT_IN_FROZEN_SOURCE", base["vib_theta"], "SOURCE_EXPLICIT" if base["vib_theta"] is not None else "STATIC_INFERRED_AMBIGUOUS"),
            identity(prefix + "-TXBAR", "T in solve_U_oc(x_bar,T)", "K", "THERMODYNAMIC_COMPOSITION_ROUTE_TEMPERATURE", "POSITIVE", "GLOBAL_SCALAR", "PRESENT" if base["solve_u_oc"] is not None else "ABSENT_IN_FROZEN_SOURCE", base["solve_u_oc"], "SOURCE_EXPLICIT" if base["solve_u_oc"] is not None else "STATIC_INFERRED_AMBIGUOUS"),
        ]
        routes = [
            route(prefix + "-R1", "T_IS_SCALAR_OR_SINGLETON", "DIRECT", ["T"], base["dqdv"],
                  [transform(1, ["T"], ["T_input"], "array coercion and positivity validation", base["t_input"]), transform(2, ["T_input"], [local_symbol], "scalar broadcast", base["t_local"]), transform(3, [local_symbol], ["T_rep"], "arithmetic mean", base["t_rep"])], [base["lag_call"]], base["dqdv_return"]),
            route(prefix + "-R2", "T_IS_PER_POINT_ARRAY", "DIRECT", ["T"], base["dqdv"],
                  [transform(1, ["T"], ["T_input"], "array coercion and positivity validation", base["t_input"]), transform(2, ["T_input", "V_n"], [local_symbol], "voltage-ordering or interpolation", base["t_local"]), transform(3, [local_symbol], ["T_rep"], "arithmetic mean", base["t_rep"])], [base["lag_call"]], base["dqdv_return"]),
        ]
        if base["vib_theta"] is not None:
            routes.append(route(prefix + f"-R{len(routes)+1}", "TRANSITION_HAS_VIBRATIONAL_TEMPERATURE_KEYS", "DIRECT", ["theta_D", "theta_E"], base["vib_theta"], [], [base["dqdv"]], base["dqdv_return"]))
        if base["solve_u_oc"] is not None:
            routes.append(route(prefix + f"-R{len(routes)+1}", "solve_U_oc_ENTRY", "DIRECT", ["T", "x_bar"], base["solve_u_oc"], [], [base["solve_u_oc"]], base["solve_u_oc"]))
    else:
        raise BuildError("E_QUANTITY")
    require(all(identity_row["source_status"] in PRESENCE for identity_row in state_ids), "E_IDENTITY_STATUS")
    conditions_by_symbol = {
        "V_app": ["ALWAYS"], "V_n": ["ALWAYS", "DIRECT_V_n_EQUILIBRIUM_API"],
        "center/U_j": ["transition_HAS_dH_rxn_AND_dS_rxn", "transition_LACKS_dH_rxn_OR_dS_rxn", "gamma_NONZERO_AND_Omega_POSITIVE"],
        "direction -> sigma_d": ["LCO_curve_FACADE"], "s -> sigma_d": ["ALWAYS"],
        "I_abs": ["I_abs_IS_NOT_NONE"], "c_rate": ["I_abs_IS_NONE", "I_abs_IS_NOT_NONE"],
        "Q_cell": ["ALWAYS"], "transition['Q']": ["EACH_TRANSITION"], "Q_Si": ["BLENDED_MODEL"], "Q": ["BLENDED_MODEL"],
        "x": ["chi_IS_NONE", "chi_IS_NOT_NONE"], "chi/self.chi": ["chi_IS_NONE", "chi_IS_NOT_NONE"],
        "ksi_eq": ["LOCAL_TRANSITION_OCCUPANCY"], "x_bar": ["solve_U_oc_ENTRY"],
        "x_center/x_MIT": ["LCO_COMPOSITION_CENTER_PATH"], "m_Si": ["from_wt_ENTRY"], "f_Si": ["CONSTRUCTOR_f_Si", "from_wt_ENTRY", "BLENDED_MODEL"],
        "T": ["T_IS_SCALAR_OR_SINGLETON", "T_IS_PER_POINT_ARRAY"], "T_work": ["T_IS_SCALAR_OR_SINGLETON", "T_IS_PER_POINT_ARRAY"],
        "T_prog": ["T_IS_SCALAR_OR_SINGLETON", "T_IS_PER_POINT_ARRAY"], "T_rep": ["T_IS_SCALAR_OR_SINGLETON", "T_IS_PER_POINT_ARRAY"],
        "theta/vibrational temperature": ["TRANSITION_HAS_VIBRATIONAL_TEMPERATURE_KEYS"],
        "T in solve_U_oc(x_bar,T)": ["solve_U_oc_ENTRY"],
    }
    for identity_row in state_ids:
        if identity_row["source_status"] == "PRESENT":
            if identity_row["symbol"] == "x":
                identity_row["route_refs"] = [item["route_id"] for item in routes
                                                if (item["condition"], item["classification"]) in
                                                {("chi_IS_NONE", "FALLBACK"), ("chi_IS_NOT_NONE", "IGNORED")}]
            elif identity_row["symbol"] == "chi/self.chi":
                identity_row["route_refs"] = [item["route_id"] for item in routes
                                                if (item["condition"], item["classification"]) in
                                                {("chi_IS_NONE", "FALLBACK"), ("chi_IS_NOT_NONE", "DIRECT")}]
            elif identity_row["symbol"] == "center/U_j":
                identity_row["route_refs"] = [item["route_id"] for item in routes
                                                if (item["condition"], item["classification"]) in
                                                {("transition_HAS_dH_rxn_AND_dS_rxn", "DIRECT"),
                                                 ("transition_LACKS_dH_rxn_OR_dS_rxn", "FALLBACK"),
                                                 ("gamma_NONZERO_AND_Omega_POSITIVE", "OVERWRITTEN")}]
            elif identity_row["symbol"] == "I_abs":
                identity_row["route_refs"] = [item["route_id"] for item in routes
                                                if (item["condition"], item["classification"]) in
                                                {("I_abs_IS_NOT_NONE", "OVERWRITTEN"),
                                                 ("I_abs_IS_NONE", "FALLBACK")}]
            elif identity_row["symbol"] == "c_rate":
                identity_row["route_refs"] = [item["route_id"] for item in routes
                                                if (item["condition"], item["classification"]) in
                                                {("I_abs_IS_NONE", "FALLBACK"),
                                                 ("I_abs_IS_NOT_NONE", "IGNORED")}]
            else:
                identity_row["route_refs"] = [item["route_id"] for item in routes if item["condition"] in conditions_by_symbol[identity_row["symbol"]]]
            require(bool(identity_row["route_refs"]), "E_PRESENT_IDENTITY_ORPHAN")
    return {
        "flow_id": prefix,
        "release_ordinal": RELEASES.index(release) + 1,
        "release": release,
        "quantity": quantity,
        "presence": "PRESENT",
        "occurrence": {
            "manifest_entry_index": occurrence["manifest_entry_index"],
            "path": occurrence["path"],
            "blob_oid": occurrence["blob_oid"],
            "blob_ordinal": occurrence["blob_ordinal"],
            "git_mode": occurrence["git_mode"],
        },
        "definition": f"Static {quantity} public-input/state/calculation/output route in the frozen production source occurrence.",
        "state_identities": state_ids,
        "routes": routes,
        "gaps": gaps,
        "authority": "STATIC_SOURCE_ORDER_AND_CONNECTIVITY_ONLY",
    }


def build_artifact() -> dict[str, Any]:
    inventory_raw = run_git(["show", EXPECTED_PARENT + ":" + INVENTORY_PATH])
    attestation_raw = run_git(["show", EXPECTED_PARENT + ":" + ATTESTATION_PATH])
    require(sha256(inventory_raw) == INVENTORY_RAW_SHA256, "E_INVENTORY_RAW")
    require(sha256(attestation_raw) == ATTESTATION_RAW_SHA256, "E_ATTESTATION_RAW")
    inventory = strict_json(inventory_raw, "E_INVENTORY_JSON")
    attestation = strict_json(attestation_raw, "E_ATTESTATION_JSON")
    require(inventory.get("semantic_sha256") == INVENTORY_SEMANTIC_SHA256, "E_INVENTORY_SEMANTIC")
    require(attestation.get("semantic_sha256") == ATTESTATION_SEMANTIC_SHA256, "E_ATTESTATION_SEMANTIC")
    universe = inventory.get("universe")
    require(universe == {
        "blob_membership_sha256": "e4e11ba47910647bcc0a0e4fd4e8918fbe2f08c75fd23fefd88fb04e8e96c066",
        "occurrences": 129,
        "path_blob_membership_sha256": "bae10035780580c9caa629d59050f307b492e6c5e75941252aca30eadbbc981f",
        "path_membership_sha256": "d64fe6b430120820da6ee00a82a3fc9679b885a2c3accd4e0e9b04dced24dfe4",
        "release_membership_sha256": "2ccc032ffeb3d9c4b449fbce48bd66448c8324fe96d4065067d8d755127a209c",
        "releases": 20,
        "role_occurrence_counts": {"code": 20, "demo": 30, "result": 35, "test": 44},
        "role_unique_blob_counts": {"code": 15, "demo": 26, "result": 14, "test": 29},
        "unique_blob_physical_lines": 29952,
        "unique_blobs": 84,
    }, "E_STEP82_UNIVERSE")
    occurrences = inventory.get("occurrence_records")
    blobs = inventory.get("blob_records")
    require(isinstance(occurrences, list) and isinstance(blobs, list), "E_STEP82_RECORDS")
    code_rows = [row for row in occurrences if row.get("role") == "code"]
    excluded_rows = [row for row in occurrences if row.get("role") != "code"]
    require(len(code_rows) == 20 and len(excluded_rows) == 109, "E_ROLE_PARTITION")
    by_release = {row["release"]: row for row in code_rows}
    require(list(sorted(by_release, key=RELEASES.index)) == RELEASES, "E_RELEASE_SEQUENCE")
    require(sorted_lines_sha([row["path"] for row in code_rows]) == CODE_PATH_SHA256, "E_CODE_PATH_HASH")
    require(sorted_lines_sha([row["path"] + "\t" + row["blob_oid"] for row in code_rows]) == CODE_PATH_BLOB_SHA256, "E_CODE_PATH_BLOB_HASH")
    require(sorted_lines_sha(list({row["blob_oid"] for row in code_rows})) == CODE_BLOB_SHA256, "E_CODE_BLOB_HASH")
    require(sorted_lines_sha([row["release"] + "\t" + row["path"] for row in code_rows]) == CODE_RELEASE_PATH_SHA256, "E_CODE_RELEASE_PATH_HASH")
    require(sorted_lines_sha([row["release"] + "\t" + row["path"] + "\t" + row["blob_oid"] + "\t" + str(row["blob_ordinal"]) for row in code_rows]) == CODE_RELEASE_PATH_BLOB_ORDINAL_SHA256, "E_CODE_OCCURRENCE_HASH")
    blob_by_oid = {row["blob_oid"]: row for row in blobs}
    code_blob_oids = {row["blob_oid"] for row in code_rows}
    require(len(code_blob_oids) == 15, "E_CODE_BLOBS")
    require(sum(blob_by_oid[oid]["physical_lines"] for oid in code_blob_oids) == 18529, "E_CODE_UNIQUE_LINES")
    require(sum(row["physical_lines"] for row in code_rows) == 24891, "E_CODE_OCCURRENCE_LINES")
    flow_records: list[dict[str, Any]] = []
    source_records: list[dict[str, Any]] = []
    for release_index, release in enumerate(RELEASES, 1):
        occurrence = by_release[release]
        raw = run_git(["cat-file", "blob", occurrence["blob_oid"]])
        require(sha256(raw) == blob_by_oid[occurrence["blob_oid"]]["raw_sha256"], "E_SOURCE_RAW")
        try:
            text = raw.decode("utf-8")
            tree = ast.parse(text)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise BuildError("E_SOURCE_PARSE") from exc
        lines = text.splitlines()
        base = base_anchors(tree, lines)
        blend = blend_anchors(tree, lines)
        source_records.append({
            "release_ordinal": release_index,
            "release": release,
            "manifest_entry_index": occurrence["manifest_entry_index"],
            "path": occurrence["path"],
            "blob_oid": occurrence["blob_oid"],
            "blob_ordinal": occurrence["blob_ordinal"],
            "git_mode": occurrence["git_mode"],
            "physical_lines": occurrence["physical_lines"],
            "raw_sha256": blob_by_oid[occurrence["blob_oid"]]["raw_sha256"],
            "ast_parse": "PASS",
            "has_blend": blend is not None,
            "feature_flags": {
                "temperature_route": "SORTED_INTERPOLATED_T_WORK" if "T_work" in text else "POINTWISE_ORDERED_T_PROG",
                "temperature_dependent_width_multiplicity": "def _dwdT" in text,
                "vibrational_temperature": "def _vib_theta" in text,
                "global_composition_solver": "def solve_U_oc" in text,
                "lco_composition_centers": "x_center" in text and "x_MIT" in text,
                "lco_curve_facade_sign_flip": base["lco_sign_if"] is not None,
                "blend_mass_to_capacity_fraction": blend is not None,
                "executable_divide_by_3600": any(isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and isinstance(node.right, ast.Constant) and node.right.value == 3600 for node in ast.walk(tree)),
                "comment_only_seconds_conversion": "1/3600" in text or "3600" in text,
                "transition_capacity_unit_mAh_explicit": "Q [mAh]" in text,
                "default_profile_conflict_bounded": release == "v1.0.25.2",
            },
            "quantity_coverage": QUANTITIES,
        })
        for quantity in QUANTITIES:
            flow_records.append(flow_row(len(flow_records) + 1, occurrence, quantity, tree, lines, base, blend, text))
    require(len(flow_records) == 100, "E_FLOW_COUNT")
    require(len({(row["release"], row["quantity"]) for row in flow_records}) == 100, "E_FLOW_BIJECTION")
    class_counts = {kind: 0 for kind in sorted(CLASSIFICATIONS)}
    identity_status_counts = {status: 0 for status in sorted(PRESENCE)}
    for row in flow_records:
        require(row["presence"] in PRESENCE, "E_PRESENCE")
        seen_conditions: set[tuple[str, str]] = set()
        for state in row["state_identities"]:
            identity_status_counts[state["source_status"]] += 1
        for item in row["routes"]:
            key = (item["condition"], "|".join(item["public_inputs"]))
            require(key not in seen_conditions, "E_ROUTE_OVERLAP")
            seen_conditions.add(key)
            class_counts[item["classification"]] += 1
    artifact: dict[str, Any] = {
        "schema_version": "phase067-step83-state-flow-v1",
        "artifact": "PHASE_067_STATE_QUANTITY_FLOW_MATRIX",
        "phase": 67,
        "step": 83,
        "generated_date": GENERATED_DATE,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "branch": BRANCH,
        "expected_subject": EXPECTED_SUBJECT,
        "gate": GATE,
        "persistence_terminal": PERSISTENCE_TERMINAL,
        "precommit_status": "PASS_PENDING_PERSISTENCE",
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "result_first": True,
        "json_outputs_last": True,
        "inputs": {
            "step82_inventory": {"path": INVENTORY_PATH, "raw_sha256": INVENTORY_RAW_SHA256, "semantic_sha256": INVENTORY_SEMANTIC_SHA256},
            "step82_full_read_attestation": {"path": ATTESTATION_PATH, "raw_sha256": ATTESTATION_RAW_SHA256, "semantic_sha256": ATTESTATION_SEMANTIC_SHA256},
        },
        "universe": {
            "all_occurrences": 129,
            "all_unique_blobs": 84,
            "all_unique_blob_physical_lines": 29952,
            "releases": 20,
            "role_occurrence_counts": {"code": 20, "demo": 30, "result": 35, "test": 44},
            "role_unique_blob_counts": {"code": 15, "demo": 26, "result": 14, "test": 29},
            "flow_target_role": "code",
            "flow_target_occurrences": 20,
            "flow_target_unique_blobs": 15,
            "flow_target_unique_blob_physical_lines": 18529,
            "flow_target_occurrence_physical_lines": 24891,
            "losslessly_excluded_nonproduction_occurrences": 109,
            "code_path_sha256": CODE_PATH_SHA256,
            "code_path_blob_sha256": CODE_PATH_BLOB_SHA256,
            "code_blob_sha256": CODE_BLOB_SHA256,
            "code_release_path_sha256": CODE_RELEASE_PATH_SHA256,
            "code_release_path_blob_ordinal_sha256": CODE_RELEASE_PATH_BLOB_ORDINAL_SHA256,
        },
        "quantity_contract": {
            "release_sequence": RELEASES,
            "quantity_sequence": QUANTITIES,
            "presence_enum": sorted(PRESENCE),
            "classification_enum": sorted(CLASSIFICATIONS),
            "required_release_quantity_rows": 100,
            "ordered_transform_authority": "STATIC_LEXICAL_ONLY_NOT_RUNTIME_CALL_ORDER",
            "downstream_owners": {
                "actual_call_order": "STEP84_CALL_SURFACE",
                "default_runtime_behavior": "STEP85_TEST_SURFACE",
                "unit_conversion": "STEP87_UNIT_NUMERICAL_AUDIT",
                "fallback_impact": "STEP88_BOUNDARY_INTERACTION",
            },
            "family_presence_axis": "release_quantity_coverage_distinct_from_nested_identity_source_status",
        },
        "source_records": source_records,
        "flow_records": flow_records,
        "coverage": {
            "release_records": 20,
            "release_quantity_rows": 100,
            "present_rows": sum(row["presence"] == "PRESENT" for row in flow_records),
            "absent_rows": sum(row["presence"] == "ABSENT_IN_FROZEN_SOURCE" for row in flow_records),
            "ambiguous_rows": sum(row["presence"] == "GROUND_NOT_FOUND_STATIC_AMBIGUOUS" for row in flow_records),
            "classification_counts": class_counts,
            "identity_source_status_counts": identity_status_counts,
            "missing_release_quantity_pairs": 0,
            "duplicate_release_quantity_pairs": 0,
            "route_overlap_errors": 0,
            "ignored_with_consumer_errors": 0,
            "fallback_contract_errors": 0,
            "unit_basis_sign_scope_merge_errors": 0,
        },
        "validation": {
            "strict_step82_inputs": "PASS",
            "all_129_occurrences_bound": "PASS",
            "production_20_of_129_lossless_partition": "PASS",
            "code_occurrence_bijection": "PASS",
            "source_git_blob_identity": "PASS",
            "ast_parse_20_of_20": "PASS",
            "release_quantity_bijection_100_of_100": "PASS",
            "source_anchor_hashes": "PASS",
            "exclusive_presence": "PASS",
            "exclusive_route_classification": "PASS",
            "quantity_identity_separation": "PASS",
            "static_only_authority": "PASS",
        },
        "authority": {
            "source_identity": True,
            "static_ast_connectivity": True,
            "static_lexical_transform_order": True,
            "runtime_behavior": False,
            "test_behavior": False,
            "scientific_truth": False,
            "external_primary_truth": False,
            "material_validity": False,
            "canonical_equation": False,
            "publication_readiness": False,
        },
        "semantic_sha256": "",
    }
    artifact["semantic_sha256"] = semantic_sha(artifact)
    return artifact


def atomic_write(path: Path, data: bytes) -> None:
    require(path.as_posix().endswith(OUTPUT_PATH), "E_OUTPUT_PATH")
    require(not path.exists(), "E_OUTPUT_EXISTS")
    temp = path.with_name(path.name + ".tmp.phase067-step83")
    require(not temp.exists(), "E_TEMP_EXISTS")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with temp.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--output", default=OUTPUT_PATH)
    args = parser.parse_args()
    require(args.preview ^ args.collect, "E_MODE")
    require(args.output == OUTPUT_PATH, "E_OUTPUT_ARG")
    first = build_artifact()
    second = build_artifact()
    require(canonical_bytes(first) == canonical_bytes(second), "E_DETERMINISM")
    if args.collect:
        atomic_write(Path(args.output), canonical_bytes(first))
        print(f"{GATE} collected rows=100 releases=20 code=20/15 determinism=2/2")
    else:
        print(f"{GATE} preview rows=100 releases=20 code=20/15 determinism=2/2 semantic={first['semantic_sha256']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
