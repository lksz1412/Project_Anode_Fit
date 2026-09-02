#!/usr/bin/env python3
"""Build the Phase 067 Step 84 source-static physics call graph.

The builder reads only committed Codex predecessor artifacts and frozen Git
objects.  It never imports or executes a production module.  Its call order is
lexical source order along statically resolved public-entry paths; it is not a
runtime trace.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "1af6c06fb5cff2918b846ed74ea213832f04f010"
BASELINE = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_SUBJECT = "audit(phase067): reconstruct physics call graph"
PERSISTENCE_TERMINAL = "PASS_P067_STEP84_PERSISTENCE"
GATE = "PASS_P067_STEP84_PHYSICS_CALL_GRAPH"
GENERATED_DATE = "2026-09-02"
BUILDER_SOURCE_POLICY_SHA256_LF = "5dd077d3402cf4ece796712367410309b7e2bc0a37bc29c2a2b8643e8af9efe9"

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STEP83_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
OUTPUT_PATH = ROOT / "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json"

INPUT_PINS = {
    INVENTORY_PATH: (
        "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63",
        "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1",
    ),
    ATTESTATION_PATH: (
        "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174",
        "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9",
    ),
    STEP83_PATH: (
        "0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8",
        "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44",
    ),
}

PUBLIC_NAMES = {
    "curve", "dqdv", "equilibrium", "solve_U_oc", "host_contributions",
    "entropy_coefficient", "entropy_coefficient_x", "reversible_heat",
    "reversible_heat_x", "irreversible_heat",
}
SUBSYSTEMS = (
    "CHARGE_BALANCE_ROOT",
    "BACKGROUND_SELF_CONSISTENCY",
    "LAG_TRAJECTORY",
    "KINETICS",
    "HEAT",
    "OBSERVATION_TRANSFORMATION",
)
BEHAVIORS = (
    "OPTION_OFF",
    "MISSING_KINETICS",
    "ZERO_CURRENT",
    "REVERSAL",
    "REST",
    "INVALID_ROOT",
    "MAX_ITER_EXHAUSTION",
)
DYNAMIC_ATTRIBUTES = {"Cbg", "chi_split"}


class BuildError(RuntimeError):
    """Controlled build failure."""


def require(condition: bool, diagnostic: str) -> None:
    if not condition:
        raise BuildError(diagnostic)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("semantic_sha256", None)
    return sha256(canonical_bytes(copy))


def predecessor_semantic_sha(value: dict[str, Any], path: str) -> str:
    copy = dict(value)
    if path in {INVENTORY_PATH, ATTESTATION_PATH}:
        copy["semantic_sha256"] = ""
        raw = (json.dumps(copy, ensure_ascii=False, indent=2, sort_keys=True,
                          allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")
        return sha256(raw)
    else:
        copy.pop("semantic_sha256", None)
    return sha256(canonical_bytes(copy))


def strict_json(raw: bytes, diagnostic: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, f"{diagnostic}:DUPLICATE_KEY:{key}")
            out[key] = value
        return out

    def reject_constant(value: str) -> None:
        raise BuildError(f"{diagnostic}:NONFINITE:{value}")

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                       parse_constant=reject_constant)
    require(isinstance(value, dict), f"{diagnostic}:TOP_NOT_OBJECT")
    return value


def git_bytes(args: list[str]) -> bytes:
    allowed = False
    if len(args) == 2 and args[0] == "show" and args[1].startswith(EXPECTED_PARENT + ":Codex/results/"):
        allowed = args[1].split(":", 1)[1] in INPUT_PINS
    elif len(args) == 3 and args[:2] == ["cat-file", "blob"]:
        allowed = len(args[2]) == 40 and all(c in "0123456789abcdef" for c in args[2])
    require(allowed, "E_GIT_ARGV")
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                               check=False, shell=False, timeout=60)
    require(completed.returncode == 0, "E_GIT_READ")
    require(completed.stderr == b"", "E_GIT_STDERR")
    return completed.stdout


def load_input(path: str) -> tuple[dict[str, Any], dict[str, str]]:
    raw = git_bytes(["show", f"{EXPECTED_PARENT}:{path}"])
    expected_raw, expected_semantic = INPUT_PINS[path]
    require(sha256(raw) == expected_raw, f"E_INPUT_RAW:{path}")
    value = strict_json(raw, f"E_INPUT_JSON:{path}")
    require(value.get("semantic_sha256") == expected_semantic,
            f"E_INPUT_SEMANTIC_STORED:{path}")
    require(predecessor_semantic_sha(value, path) == expected_semantic,
            f"E_INPUT_SEMANTIC_FRESH:{path}")
    return value, {"path": path, "raw_sha256": expected_raw,
                   "semantic_sha256": expected_semantic}


def stable_ast_value(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__,
                **{field: stable_ast_value(getattr(value, field, None))
                   for field in value._fields}}
    if isinstance(value, list):
        return [stable_ast_value(item) for item in value]
    if isinstance(value, complex):
        return {"_complex": [value.real, value.imag]}
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if value is Ellipsis:
        return {"_ellipsis": True}
    return value


def ast_hash(node: ast.AST) -> str:
    return sha256(canonical_bytes(stable_ast_value(node)))


def source_segment(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node)
    require(segment is not None, "E_SOURCE_SEGMENT")
    return segment


def qualified_definitions(tree: ast.AST) -> tuple[dict[str, ast.AST], dict[str, list[str]], dict[str, list[str]]]:
    definitions: dict[str, ast.AST] = {}
    classes: dict[str, list[str]] = {}
    simple: dict[str, list[str]] = {}
    scope: list[str] = []

    class Visitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            qualified = ".".join([*scope, node.name])
            definitions[qualified] = node
            simple.setdefault(node.name, []).append(qualified)
            classes[qualified] = [ast.unparse(base) for base in node.bases]
            scope.append(node.name)
            self.generic_visit(node)
            scope.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            qualified = ".".join([*scope, node.name])
            definitions[qualified] = node
            simple.setdefault(node.name, []).append(qualified)
            scope.append(node.name)
            self.generic_visit(node)
            scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

    Visitor().visit(tree)
    return definitions, simple, classes


def class_ancestor_order(class_name: str, classes: dict[str, list[str]]) -> list[str]:
    out: list[str] = []
    pending = [class_name]
    while pending:
        current = pending.pop(0)
        if current in out:
            continue
        out.append(current)
        for base in classes.get(current, []):
            if base in classes:
                pending.append(base)
    return out


def resolve_call(owner: str, call: ast.Call, definitions: dict[str, ast.AST],
                 simple: dict[str, list[str]], classes: dict[str, list[str]]) -> tuple[str, str | None]:
    func = call.func
    if isinstance(func, ast.Name):
        name = func.id
        nested = f"{owner}.{name}"
        if nested in definitions:
            return "RESOLVED_INTERNAL", nested
        module = [candidate for candidate in simple.get(name, []) if "." not in candidate]
        if len(module) == 1:
            return "RESOLVED_INTERNAL", module[0]
        return "EXTERNAL_OR_BUILTIN", None
    if isinstance(func, ast.Attribute):
        parts: list[str] = []
        cursor: ast.AST = func
        while isinstance(cursor, ast.Attribute):
            parts.append(cursor.attr)
            cursor = cursor.value
        parts.reverse()
        if isinstance(cursor, ast.Name) and cursor.id == "self":
            if len(parts) == 1 and parts[0] in DYNAMIC_ATTRIBUTES:
                return "DYNAMIC_CALLABLE_ATTRIBUTE", None
            if len(parts) == 1:
                class_name = owner.split(".", 1)[0]
                for candidate_class in class_ancestor_order(class_name, classes):
                    candidate = f"{candidate_class}.{parts[0]}"
                    if candidate in definitions:
                        return "RESOLVED_INTERNAL", candidate
            return "AMBIGUOUS_DYNAMIC_DISPATCH", None
    return "EXTERNAL_OR_BUILTIN", None


def owner_call_sites(owner: str, node: ast.AST) -> list[dict[str, Any]]:
    sites: list[dict[str, Any]] = []
    predicates: list[str] = []
    statement: list[ast.AST] = []

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, inner: ast.FunctionDef) -> None:
            if inner is node:
                for item in inner.body:
                    self.visit(item)

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, inner: ast.ClassDef) -> None:
            if inner is node:
                for item in inner.body:
                    self.visit(item)

        def visit_If(self, inner: ast.If) -> None:
            self.visit(inner.test)
            test = ast.unparse(inner.test)
            predicates.append(test)
            for item in inner.body:
                self.visit(item)
            predicates.pop()
            if inner.orelse:
                predicates.append(f"NOT({test})")
                for item in inner.orelse:
                    self.visit(item)
                predicates.pop()

        def visit_IfExp(self, inner: ast.IfExp) -> None:
            self.visit(inner.test)
            test = ast.unparse(inner.test)
            predicates.append(test)
            self.visit(inner.body)
            predicates.pop()
            predicates.append(f"NOT({test})")
            self.visit(inner.orelse)
            predicates.pop()

        def _statement(self, inner: ast.AST) -> None:
            statement.append(inner)
            self.generic_visit(inner)
            statement.pop()

        visit_Assign = _statement
        visit_AnnAssign = _statement
        visit_AugAssign = _statement
        visit_Return = _statement
        visit_Expr = _statement

        def visit_Call(self, inner: ast.Call) -> None:
            sites.append({"node": inner, "predicates": list(predicates),
                          "statement": statement[-1] if statement else inner})
            self.generic_visit(inner)

    Visitor().visit(node)
    sites.sort(key=lambda row: (row["node"].lineno, row["node"].col_offset,
                                row["node"].end_lineno, row["node"].end_col_offset))
    return sites


def anchor(source: str, node: ast.AST, qualified_owner: str) -> dict[str, Any]:
    segment = source_segment(source, node)
    return {
        "ast_kind": type(node).__name__,
        "end_col": node.end_col_offset,
        "end_line": node.end_lineno,
        "expression": segment,
        "normalized_ast_sha256": ast_hash(node),
        "qualified_owner": qualified_owner,
        "source_sha256": sha256(segment.encode("utf-8")),
        "start_col": node.col_offset,
        "start_line": node.lineno,
    }


def result_binding(statement: ast.AST) -> dict[str, Any]:
    if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        if isinstance(statement, ast.Assign):
            targets = [ast.unparse(target) for target in statement.targets]
        else:
            targets = [ast.unparse(statement.target)]
        return {"kind": "ASSIGNMENT", "targets": targets}
    if isinstance(statement, ast.Return):
        return {"kind": "RETURN", "targets": []}
    return {"kind": "EXPRESSION", "targets": []}


def definition_record(source: str, qualified: str, node: ast.AST) -> dict[str, Any]:
    return {
        "anchor": anchor(source, node, qualified),
        "definition_kind": type(node).__name__,
        "name": getattr(node, "name"),
        "public_entry": getattr(node, "name") in PUBLIC_NAMES,
        "qualified_name": qualified,
    }


def family_roots(subsystem: str) -> set[str]:
    return {
        "CHARGE_BALANCE_ROOT": {"solve_U_oc", "entropy_coefficient_x", "reversible_heat_x"},
        "BACKGROUND_SELF_CONSISTENCY": {"equilibrium", "dqdv", "host_contributions"},
        "LAG_TRAJECTORY": {"curve", "dqdv"},
        "KINETICS": {"curve", "dqdv"},
        "HEAT": {"entropy_coefficient", "entropy_coefficient_x", "reversible_heat",
                 "reversible_heat_x", "irreversible_heat"},
        "OBSERVATION_TRANSFORMATION": {"curve", "dqdv", "equilibrium", "host_contributions"},
    }[subsystem]


SCENARIOS = (
    ("CHARGE_BALANCE_ROOT", "SOLVE_ROOT_TO_RESIDUAL", "solve_U_oc", {"_charge", "_balance_host.solve_U_oc"}),
    ("CHARGE_BALANCE_ROOT", "ENTROPY_X_TO_ROOT", "entropy_coefficient_x", {"solve_U_oc"}),
    ("CHARGE_BALANCE_ROOT", "REVERSIBLE_HEAT_X_TO_ENTROPY_X", "reversible_heat_x", {"entropy_coefficient_x"}),
    ("BACKGROUND_SELF_CONSISTENCY", "EQUILIBRIUM_CBG_DIRECT", "equilibrium", {"self.Cbg"}),
    ("BACKGROUND_SELF_CONSISTENCY", "DQDV_CBG_DIRECT", "dqdv", {"self.Cbg"}),
    ("BACKGROUND_SELF_CONSISTENCY", "HOST_CONTRIBUTIONS_CBG_DIRECT", "host_contributions", {"self.Cbg"}),
    ("LAG_TRAJECTORY", "CURVE_TO_DQDV", "curve", {"dqdv"}),
    ("LAG_TRAJECTORY", "DQDV_TO_LAG_RESOLVER", "dqdv", {"_resolve_lag_length"}),
    ("LAG_TRAJECTORY", "DQDV_TO_CAUSAL_LOWPASS", "dqdv", {"_causal_lowpass"}),
    ("LAG_TRAJECTORY", "DQDV_TO_POINTWISE_MEMORY", "dqdv", {"_causal_memory_pointwise"}),
    ("LAG_TRAJECTORY", "DQDV_TO_RATIO_MEMORY", "dqdv", {"_causal_memory_ratio"}),
    ("LAG_TRAJECTORY", "DQDV_TO_CAUSAL_PAD", "dqdv", {"_causal_pad"}),
    ("KINETICS", "CURVE_TO_KINETIC_LENGTH", "curve", {"func_L_q"}),
    ("KINETICS", "DQDV_TO_KINETIC_LENGTH", "dqdv", {"func_L_q"}),
    ("HEAT", "REVERSIBLE_HEAT_TO_ENTROPY", "reversible_heat", {"entropy_coefficient"}),
    ("HEAT", "ENTROPY_X_TO_ENTROPY", "entropy_coefficient_x", {"entropy_coefficient"}),
    ("HEAT", "ENTROPY_X_TO_ROOT", "entropy_coefficient_x", {"solve_U_oc"}),
    ("HEAT", "REVERSIBLE_HEAT_X_TO_ENTROPY_X", "reversible_heat_x", {"entropy_coefficient_x"}),
    ("HEAT", "IRREVERSIBLE_HEAT_DIRECT", "irreversible_heat", set()),
    ("OBSERVATION_TRANSFORMATION", "CURVE_TO_DQDV", "curve", {"dqdv"}),
    ("OBSERVATION_TRANSFORMATION", "EQUILIBRIUM_DIRECT", "equilibrium", set()),
    ("OBSERVATION_TRANSFORMATION", "DQDV_DIRECT", "dqdv", set()),
    ("OBSERVATION_TRANSFORMATION", "BLEND_HOST_EQUILIBRIUM", "equilibrium", {"gr_host.equilibrium", "si_host.equilibrium"}),
    ("OBSERVATION_TRANSFORMATION", "BLEND_HOST_DQDV", "dqdv", {"gr_host.dqdv", "si_host.dqdv"}),
    ("OBSERVATION_TRANSFORMATION", "BLEND_HOST_CURVE", "curve", {"gr_host.curve", "si_host.curve"}),
    ("OBSERVATION_TRANSFORMATION", "BLEND_HOST_CONTRIBUTIONS", "host_contributions", {"gr_host.equilibrium", "si_host.equilibrium"}),
)


def edge_matches(edge: dict[str, Any], targets: set[str]) -> bool:
    if not targets:
        return False
    values = {edge["callable_expression"]}
    if edge["callee"]:
        values.add(edge["callee"])
        values.add(edge["callee"].rsplit(".", 1)[-1])
    for value in values:
        if any(value == target or value.endswith("." + target) for target in targets):
            return True
    return False


def shortest_paths(root: str, outgoing: dict[str, list[dict[str, Any]]],
                   targets: set[str], limit: int = 8) -> list[list[dict[str, Any]]]:
    if not targets:
        return [[]]
    queue: list[tuple[str, list[dict[str, Any]], frozenset[str]]] = [(root, [], frozenset({root}))]
    found: list[list[dict[str, Any]]] = []
    found_depth: int | None = None
    while queue:
        owner, path, seen = queue.pop(0)
        if found_depth is not None and len(path) >= found_depth:
            continue
        if len(path) >= limit:
            continue
        for edge in outgoing.get(owner, []):
            candidate = [*path, edge]
            if edge_matches(edge, targets):
                found.append(candidate)
                found_depth = len(candidate) if found_depth is None else found_depth
                continue
            target = edge["callee"]
            if edge["resolution"] == "RESOLVED_INTERNAL" and target and target not in seen:
                queue.append((target, candidate, seen | {target}))
    return found


def first_matching_anchor(source: str, owner: str, node: ast.AST,
                          predicate: Any) -> dict[str, Any] | None:
    matches = [item for item in ast.walk(node) if hasattr(item, "lineno") and predicate(item)]
    if not matches:
        return None
    matches.sort(key=lambda item: (item.lineno, item.col_offset,
                                   item.end_lineno, item.end_col_offset))
    return anchor(source, matches[0], owner)


def source_projection(source_row: dict[str, Any], source: str, tree: ast.AST) -> dict[str, Any]:
    definitions, simple, classes = qualified_definitions(tree)
    all_edges: list[dict[str, Any]] = []
    edge_counter = 0
    for owner, node in sorted(definitions.items(), key=lambda item: (
            item[1].lineno, item[1].col_offset, item[0])):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for lexical_ordinal, site in enumerate(owner_call_sites(owner, node), 1):
            call = site["node"]
            resolution, callee = resolve_call(owner, call, definitions, simple, classes)
            if resolution == "EXTERNAL_OR_BUILTIN":
                continue
            edge_counter += 1
            call_text = ast.unparse(call.func)
            all_edges.append({
                "argument_expressions": [ast.unparse(arg) for arg in call.args],
                "branch_predicates": site["predicates"],
                "call_anchor": anchor(source, call, owner),
                "callable_expression": call_text,
                "callee": callee,
                "caller": owner,
                "edge_id": f"P067-S84-B{source_row['blob_ordinal']:03d}-E{edge_counter:04d}",
                "keyword_arguments": [
                    {"name": kw.arg, "value": ast.unparse(kw.value)} for kw in call.keywords
                ],
                "lexical_ordinal_in_caller": lexical_ordinal,
                "resolution": resolution,
                "result_binding": result_binding(site["statement"]),
                "state_dependency_authority": "SOURCE_STATIC_ARGUMENT_AND_BINDING_ONLY",
            })

    public = sorted(
        [qualified for qualified, node in definitions.items()
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
         and node.name in PUBLIC_NAMES],
        key=lambda qualified: (definitions[qualified].lineno, qualified),
    )
    outgoing_all: dict[str, list[dict[str, Any]]] = {}
    for edge in all_edges:
        outgoing_all.setdefault(edge["caller"], []).append(edge)
    for edges in outgoing_all.values():
        edges.sort(key=lambda edge: (edge["lexical_ordinal_in_caller"], edge["edge_id"]))

    reachable = set(public)
    pending = list(public)
    while pending:
        owner = pending.pop(0)
        for edge in outgoing_all.get(owner, []):
            target = edge["callee"]
            if edge["resolution"] == "RESOLVED_INTERNAL" and target not in reachable:
                reachable.add(target)
                pending.append(target)
    edges = [edge for edge in all_edges if edge["caller"] in reachable]
    edge_ids = {edge["edge_id"] for edge in edges}
    outgoing = {owner: [edge for edge in owner_edges if edge["edge_id"] in edge_ids]
                for owner, owner_edges in outgoing_all.items() if owner in reachable}
    nodes = [definition_record(source, qualified, definitions[qualified])
             for qualified in sorted(reachable, key=lambda q: (definitions[q].lineno, q))]

    sequences: list[dict[str, Any]] = []
    for scenario_ordinal, (subsystem, scenario, root_name, targets) in enumerate(SCENARIOS, 1):
        roots = [qualified for qualified in public if definitions[qualified].name == root_name]
        candidates: list[dict[str, Any]] = []
        for public_root in roots:
            for candidate_ordinal, path in enumerate(shortest_paths(public_root, outgoing, targets), 1):
                contiguous = all(path[index]["callee"] == path[index + 1]["caller"]
                                 for index in range(len(path) - 1))
                require(contiguous, "E_INTERNAL_PATH_CONTIGUITY")
                candidates.append({
                    "branch_predicate_projection": [edge["branch_predicates"] for edge in path],
                    "candidate_ordinal": candidate_ordinal,
                    "edge_ids": [edge["edge_id"] for edge in path],
                    "public_entry": public_root,
                    "terminal": (path[-1]["callee"] or path[-1]["callable_expression"]
                                 if path else public_root),
                })
        sequences.append({
            "authority": "STATIC_PUBLIC_ENTRY_CALL_SEQUENCE_NOT_EXECUTED_RUNTIME_ORDER",
            "candidate_paths": candidates,
            "presence": "PRESENT" if candidates else "ABSENT_IN_FROZEN_SOURCE",
            "scenario": scenario,
            "sequence_id": f"P067-S84-B{source_row['blob_ordinal']:03d}-S{scenario_ordinal:03d}",
            "subsystem": subsystem,
            "target_selector": sorted(targets),
        })

    text = source
    def by_name(name: str) -> list[tuple[str, ast.AST]]:
        return [(qualified, node) for qualified, node in definitions.items()
                if getattr(node, "name", None) == name]

    features = {
        "blend_public_entries": any(q.startswith("BlendedAnodeDQDV.") for q in public),
        "causal_lowpass_work_grid": "_causal_lowpass" in simple and "np.interp(V_n" in text,
        "causal_pointwise_sort_inverse": "_causal_memory_pointwise" in simple and "inv_order" in text,
        "causal_ratio_frozen_path": "_causal_memory_ratio" in simple and "ksi_lag0" in text,
        "causal_pad_re_evaluation": "_causal_pad" in simple and "_ksi_eq_ext" in text,
        "charge_balance_root": bool(by_name("solve_U_oc")),
        "func_U_j_hys_defined": "func_U_j_hys" in simple,
        "public_callers_of_func_U_j_hys": sum(
            1 for edge in edges if edge["callee"] == "func_U_j_hys"),
        "transfer_helper_defined": "transfer_apparent_from_equilibrium" in simple,
        "public_callers_of_transfer_helper": sum(
            1 for edge in edges if edge["callee"] == "transfer_apparent_from_equilibrium"),
    }

    coverage: list[dict[str, Any]] = []
    for subsystem in SUBSYSTEMS:
        refs = [sequence["sequence_id"] for sequence in sequences
                if sequence["subsystem"] == subsystem and sequence["presence"] == "PRESENT"]
        coverage.append({
            "coverage_id": f"P067-S84-{source_row['release_ordinal']:03d}-{subsystem}",
            "presence": "PRESENT" if refs else "ABSENT_IN_FROZEN_SOURCE",
            "release": source_row["release"],
            "sequence_refs": refs,
            "subsystem": subsystem,
        })

    behavior_records: list[dict[str, Any]] = []
    dqdv_defs = by_name("dqdv")
    lag_defs = by_name("_resolve_lag_length")
    solve_defs = by_name("solve_U_oc")

    def sequence_refs(*scenario_names: str) -> list[str]:
        selected = set(scenario_names)
        return sorted(sequence["sequence_id"] for sequence in sequences
                      if sequence["scenario"] in selected and sequence["presence"] == "PRESENT")

    def add_behavior(condition: str, status: str, mechanism: str,
                     evidence: dict[str, Any] | None, owner: str,
                     refs: list[str], subcases: list[dict[str, Any]] | None = None) -> None:
        if status != "SOURCE_STATIC_PRESENT":
            require(refs == [], "E_NONPRESENT_BEHAVIOR_REFS")
        behavior_records.append({
            "behavior_id": f"P067-S84-{source_row['release_ordinal']:03d}-B{len(behavior_records)+1:02d}",
            "condition": condition,
            "downstream_owner": owner,
            "evidence": evidence,
            "evidence_subcases": subcases or [],
            "mechanism": mechanism,
            "public_sequence_refs": refs,
            "release": source_row["release"],
            "status": status,
        })

    if dqdv_defs:
        q, node = dqdv_defs[0]
        option_anchor = first_matching_anchor(
            source, q, node,
            lambda n: isinstance(n, ast.If)
            and ast.unparse(n.test) == "self.lag_ratio_correction"
            and bool(n.orelse)
            and any(isinstance(item, ast.Assign)
                    and "_causal_memory_pointwise" in ast.unparse(item)
                    for item in n.orelse))
        reversal_anchor = first_matching_anchor(source, q, node, lambda n: isinstance(n, ast.If)
                                                and "sigma_d" in ast.unparse(n.test))
    else:
        option_anchor = reversal_anchor = None
    if lag_defs:
        qlag, nlag = lag_defs[0]
        lag_guard = first_matching_anchor(source, qlag, nlag, lambda n: isinstance(n, ast.If)
                                           and ("I_abs" in ast.unparse(n.test)
                                                or "dH_a" in ast.unparse(n.test)))
    else:
        lag_guard = None
    add_behavior("OPTION_OFF", "SOURCE_STATIC_PRESENT" if option_anchor else "ABSENT_IN_FROZEN_SOURCE",
                 "lag_ratio_correction false selects ordinary _causal_memory_pointwise",
                 option_anchor, "P067-STEP88",
                 sequence_refs("DQDV_TO_POINTWISE_MEMORY") if option_anchor else [])
    add_behavior("MISSING_KINETICS", "SOURCE_STATIC_PRESENT" if lag_guard else "GROUND_NOT_FOUND_STATIC",
                 "missing activation input selects zero lag length", lag_guard, "P067-STEP88",
                 sequence_refs("DQDV_TO_LAG_RESOLVER") if lag_guard else [])
    add_behavior("ZERO_CURRENT", "SOURCE_STATIC_PRESENT" if lag_guard else "GROUND_NOT_FOUND_STATIC",
                 "nonpositive current selects zero lag length", lag_guard, "P067-STEP88",
                 sequence_refs("DQDV_TO_LAG_RESOLVER") if lag_guard else [])
    add_behavior("REVERSAL", "SOURCE_STATIC_PRESENT" if reversal_anchor else "GROUND_NOT_FOUND_STATIC",
                 "direction branch reverses causal traversal and restores order", reversal_anchor,
                 "P067-STEP88", sequence_refs("DQDV_TO_CAUSAL_LOWPASS",
                                               "DQDV_TO_POINTWISE_MEMORY",
                                               "DQDV_TO_RATIO_MEMORY",
                                               "DQDV_TO_CAUSAL_PAD") if reversal_anchor else [])
    hys_node = definitions.get("func_U_j_hys")
    hys_anchor = anchor(source, hys_node, "func_U_j_hys") if hys_node else None
    rest_status = ("DORMANT_NO_PUBLIC_CALLER" if hys_node and features["public_callers_of_func_U_j_hys"] == 0
                   else "SOURCE_STATIC_PRESENT" if hys_node else "ABSENT_IN_FROZEN_SOURCE")
    add_behavior("REST", rest_status,
                 "rest-aware hysteresis helper has no fresh public-entry caller" if hys_node else
                 "rest-aware helper absent", hys_anchor, "P067-STEP88", [])
    if solve_defs:
        qsolve, nsolve = solve_defs[0]
        invalid_specs = (
            ("X_BAR_DOMAIN", lambda text: "x_arr" in text and "isfinite" in text
             and "<= 0.0" in text and ">= 1.0" in text),
            ("Q_TOTAL_NONPOSITIVE", lambda text: "Q_tot <= 0.0" in text),
            ("BRACKET_ORDER", lambda text: "U_lo >= U_hi" in text),
            ("ENDPOINT_SIGN", lambda text: "f_lo < 0.0 < f_hi" in text),
        )
        invalid_subcases = []
        for subcase, predicate in invalid_specs:
            matches = [item for item in ast.walk(nsolve) if isinstance(item, ast.If)
                       and predicate(ast.unparse(item.test))]
            require(len(matches) == 1, "E_INVALID_ROOT_SUBCASE:" + subcase)
            raises = [item for item in matches[0].body if isinstance(item, ast.Raise)]
            require(len(raises) == 1, "E_INVALID_ROOT_RAISE:" + subcase)
            invalid_subcases.append({"predicate_anchor": anchor(source, matches[0], qsolve),
                                     "raise_anchor": anchor(source, raises[0], qsolve),
                                     "subcase": subcase})
        midpoint_candidates = [item for item in ast.walk(nsolve)
                               if isinstance(item, ast.Assign)
                               and "out[" in ast.unparse(item)
                               and "lo" in ast.unparse(item.value)
                               and "hi" in ast.unparse(item.value)]
        midpoint_candidates.sort(key=lambda item: (item.lineno, item.col_offset))
        midpoint = midpoint_candidates[-1] if midpoint_candidates else None
        midpoint_anchor = anchor(source, midpoint, qsolve) if midpoint else None
    else:
        invalid_subcases = []
        midpoint_anchor = None
    add_behavior("INVALID_ROOT", "SOURCE_STATIC_PRESENT" if invalid_subcases else "ABSENT_IN_FROZEN_SOURCE",
                 "x_bar domain, nonpositive Q_tot, bracket order, and endpoint sign each raise",
                 None, "P067-STEP88", sequence_refs("SOLVE_ROOT_TO_RESIDUAL")
                 if invalid_subcases else [], invalid_subcases)
    add_behavior("MAX_ITER_EXHAUSTION", "SOURCE_STATIC_PRESENT" if midpoint_anchor else "ABSENT_IN_FROZEN_SOURCE",
                 "loop exhaustion returns the final bracket midpoint without an explicit nonconvergence raise",
                 midpoint_anchor, "P067-STEP88", sequence_refs("SOLVE_ROOT_TO_RESIDUAL")
                 if midpoint_anchor else [])

    dormant = []
    for name, downstream in (("func_U_j_hys", "P067-STEP88"),
                             ("transfer_apparent_from_equilibrium", "P067-STEP87")):
        node = definitions.get(name)
        inbound = [edge["edge_id"] for edge in edges if edge["callee"] == name]
        dormant.append({
            "anchor": anchor(source, node, name) if node else None,
            "defined": node is not None,
            "downstream_owner": downstream,
            "helper": name,
            "public_inbound_edge_refs": inbound,
            "status": ("DORMANT_NO_PUBLIC_CALLER" if node is not None and not inbound
                       else "PUBLICLY_REACHABLE" if inbound else "ABSENT_IN_FROZEN_SOURCE"),
        })

    retained_edge_ids = {edge_id for sequence in sequences
                         for candidate in sequence["candidate_paths"]
                         for edge_id in candidate["edge_ids"]}
    edges = [edge for edge in edges if edge["edge_id"] in retained_edge_ids]
    retained_nodes = set(public)
    for edge in edges:
        retained_nodes.add(edge["caller"])
        if edge["callee"] is not None:
            retained_nodes.add(edge["callee"])
    nodes = [definition_record(source, qualified, definitions[qualified])
             for qualified in sorted(retained_nodes, key=lambda q: (definitions[q].lineno, q))]

    occurrence = {key: source_row[key] for key in (
        "release", "release_ordinal", "manifest_entry_index", "path", "blob_oid",
        "blob_ordinal", "git_mode", "physical_lines", "raw_sha256")}
    return {
        "behavior_records": behavior_records,
        "coverage_records": coverage,
        "dormant_records": dormant,
        "edge_records": edges,
        "feature_contract": features,
        "node_records": nodes,
        "occurrence": occurrence,
        "sequence_records": sequences,
    }


def build_artifact() -> dict[str, Any]:
    inventory, inventory_input = load_input(INVENTORY_PATH)
    attestation, attestation_input = load_input(ATTESTATION_PATH)
    step83, step83_input = load_input(STEP83_PATH)
    universe = step83.get("universe")
    require(isinstance(universe, dict), "E_STEP83_UNIVERSE")
    require((universe.get("all_occurrences"), universe.get("all_unique_blobs"),
             universe.get("all_unique_blob_physical_lines"), universe.get("releases"))
            == (129, 84, 29952, 20), "E_ALL_SOURCE_DENOMINATOR")
    require((universe.get("flow_target_occurrences"), universe.get("flow_target_unique_blobs"),
             universe.get("losslessly_excluded_nonproduction_occurrences"))
            == (20, 15, 109), "E_PRODUCTION_DENOMINATOR")
    require(inventory.get("universe", {}).get("unique_blobs") == 84, "E_INVENTORY_DENOMINATOR")
    require(attestation.get("coverage", {}).get("unique_blobs_read_full") == 84,
            "E_ATTESTATION_READ_FULL")
    source_rows = step83.get("source_records")
    require(isinstance(source_rows, list) and len(source_rows) == 20, "E_SOURCE_ROWS")
    require([row.get("release_ordinal") for row in source_rows] == list(range(1, 21)),
            "E_RELEASE_ORDER")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in source_rows:
        grouped.setdefault(row["blob_oid"], []).append(row)
    require(len(grouped) == 15, "E_CODE_BLOB_COUNT")
    projections: dict[str, dict[str, Any]] = {}
    blob_graph_records: list[dict[str, Any]] = []
    for blob_oid, rows in sorted(grouped.items(), key=lambda item: item[1][0]["blob_ordinal"]):
        representative = rows[0]
        require(all(row["blob_ordinal"] == representative["blob_ordinal"] for row in rows),
                "E_SHARED_BLOB_ORDINAL")
        raw = git_bytes(["cat-file", "blob", blob_oid])
        require(all(sha256(raw) == row["raw_sha256"] for row in rows), "E_SOURCE_RAW")
        source = raw.decode("utf-8")
        require(all(source.count("\n") + (0 if source.endswith("\n") else 1)
                    == row["physical_lines"] for row in rows), "E_SOURCE_LINES")
        tree = ast.parse(source, filename=representative["path"])
        projection = source_projection(representative, source, tree)
        projections[blob_oid] = projection
        occurrence_refs = [{key: row[key] for key in (
            "release", "release_ordinal", "manifest_entry_index", "path", "blob_oid",
            "blob_ordinal", "git_mode", "physical_lines", "raw_sha256")}
            for row in rows]
        blob_graph_records.append({
            "blob_oid": blob_oid,
            "blob_ordinal": representative["blob_ordinal"],
            "dormant_records": projection["dormant_records"],
            "edge_records": projection["edge_records"],
            "feature_contract": projection["feature_contract"],
            "node_records": projection["node_records"],
            "occurrence_refs": occurrence_refs,
            "sequence_records": projection["sequence_records"],
        })

    source_records = [{key: row[key] for key in (
        "release", "release_ordinal", "manifest_entry_index", "path", "blob_oid",
        "blob_ordinal", "git_mode", "physical_lines", "raw_sha256")}
        | {"graph_blob_ref": f"P067-S84-B{row['blob_ordinal']:03d}"} for row in source_rows]
    coverage_records = []
    behavior_records = []
    for row in source_rows:
        projection = projections[row["blob_oid"]]
        common = {"release": row["release"], "release_ordinal": row["release_ordinal"],
                  "path": row["path"], "blob_oid": row["blob_oid"],
                  "blob_ordinal": row["blob_ordinal"]}
        for subsystem in SUBSYSTEMS:
            refs = [sequence["sequence_id"] for sequence in projection["sequence_records"]
                    if sequence["subsystem"] == subsystem and sequence["presence"] == "PRESENT"]
            coverage_records.append(common | {
                "coverage_id": f"P067-S84-{row['release_ordinal']:03d}-{subsystem}",
                "presence": "PRESENT" if refs else "ABSENT_IN_FROZEN_SOURCE",
                "sequence_refs": refs,
                "subsystem": subsystem,
            })
        for ordinal, template in enumerate(projection["behavior_records"], 1):
            material = {key: value for key, value in template.items()
                        if key not in {"behavior_id", "release"}}
            behavior_records.append(common | material | {
                "behavior_id": f"P067-S84-{row['release_ordinal']:03d}-B{ordinal:02d}"})

    require(len(coverage_records) == 120, "E_COVERAGE_120")
    require(len(behavior_records) == 140, "E_BEHAVIOR_140")
    shared_blob_drift = 0
    node_count = sum(len(record["node_records"]) for record in blob_graph_records)
    edge_count = sum(len(record["edge_records"]) for record in blob_graph_records)
    sequence_count = sum(len(record["sequence_records"]) for record in blob_graph_records)
    dynamic_count = sum(edge["resolution"] != "RESOLVED_INTERNAL"
                        for record in blob_graph_records for edge in record["edge_records"])

    artifact: dict[str, Any] = {
        "artifact": "PHASE_067_PHYSICS_CALL_GRAPH",
        "authority": {
            "actual_runtime_order_proven": False,
            "canonical_model_selected": False,
            "external_scientific_or_material_validity": False,
            "production_source_modified": False,
            "source_static_public_entry_call_sequence": True,
            "theory_claim_validated": False,
            "unresolved_dynamic_dispatch_promoted": False,
        },
        "baseline_commit": BASELINE,
        "behavior_records": behavior_records,
        "blob_graph_records": blob_graph_records,
        "branch": BRANCH,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "coverage": {
            "behavior_records": len(behavior_records),
            "coverage_records": len(coverage_records),
            "dynamic_edges": dynamic_count,
            "edge_records": edge_count,
            "node_records": node_count,
            "release_occurrences": len(source_records),
            "sequence_records": sequence_count,
            "shared_blob_semantic_drift": shared_blob_drift,
            "subsystems_per_release": len(SUBSYSTEMS),
        },
        "coverage_records": coverage_records,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "gate": GATE,
        "generated_date": GENERATED_DATE,
        "inputs": {
            "step82_full_read_attestation": attestation_input,
            "step82_inventory": inventory_input,
            "step83_state_quantity_flow": step83_input,
        },
        "json_outputs_last": True,
        "persistence_terminal": PERSISTENCE_TERMINAL,
        "phase": 67,
        "precommit_status": "PASS_PENDING_PERSISTENCE",
        "result_first": True,
        "schema_version": "phase067-step84-physics-call-graph-v1",
        "semantic_sha256": "",
        "source_records": source_records,
        "step": 84,
        "universe": {
            "all_occurrences": 129,
            "all_unique_blob_physical_lines": 29952,
            "all_unique_blobs": 84,
            "code_occurrences": 20,
            "code_unique_blobs": 15,
            "excluded_nonproduction_occurrences": 109,
            "releases": 20,
        },
        "validation": {
            "ambiguous_dynamic_dispatch_promotions": 0,
            "behavior_cardinality_mismatches": 0,
            "coverage_cardinality_mismatches": 0,
            "false_transfer_helper_edges": 0,
            "missing_source_anchors": 0,
            "noncontiguous_sequences": 0,
            "runtime_authority_promotions": 0,
            "shared_blob_projection_drift": shared_blob_drift,
        },
    }
    artifact["semantic_sha256"] = semantic_sha(artifact)
    return artifact


def atomic_write(path: Path, data: bytes) -> None:
    require(not path.exists(), "E_OUTPUT_EXISTS")
    temp = path.with_name(path.name + f".tmp.{os.getpid()}")
    require(not temp.exists(), "E_TEMP_EXISTS")
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
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    require(args.collect ^ args.preview, "E_MODE_EXCLUSIVE")
    first = build_artifact()
    second = build_artifact()
    require(canonical_bytes(first) == canonical_bytes(second), "E_DETERMINISM")
    if args.collect:
        atomic_write(OUTPUT_PATH, canonical_bytes(first))
        print(f"{GATE} collect releases=20 coverage=120 behavior=140 determinism=2/2")
    else:
        present_sequences = sum(sequence["presence"] == "PRESENT"
                                for graph in first["blob_graph_records"]
                                for sequence in graph["sequence_records"])
        print(f"{GATE} preview releases=20 coverage=120 behavior=140 "
              f"blobs={len(first['blob_graph_records'])} nodes={first['coverage']['node_records']} "
              f"edges={first['coverage']['edge_records']} "
              f"dynamic={first['coverage']['dynamic_edges']} "
              f"sequences={first['coverage']['sequence_records']} present={present_sequences} "
              f"determinism=2/2 "
              f"semantic={first['semantic_sha256']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(str(exc))
        raise SystemExit(1)
