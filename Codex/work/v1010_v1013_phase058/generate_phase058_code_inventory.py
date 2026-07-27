#!/usr/bin/env python3
"""Generate AST inventory, call graph, and exact diffs for Phase 058 code."""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "Codex" / "work" / "v1010_v1013_phase058" / "code_diffs"
OUT = ROOT / "Codex" / "results" / "PHASE_058_CODE_BEHAVIOR_MATRIX.json"
PATHS = [
    "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py",
    "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
]


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def call_names(node: ast.AST) -> list[str]:
    names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            name = dotted_name(child.func)
            if name:
                names.add(name)
    return sorted(names)


def literal_or_source(node: ast.AST | None, source: str) -> object:
    if node is None:
        return None
    try:
        return ast.literal_eval(node)
    except Exception:
        return ast.get_source_segment(source, node)


def function_record(node: ast.FunctionDef | ast.AsyncFunctionDef, source: str, owner: str | None) -> dict:
    positional = list(node.args.posonlyargs) + list(node.args.args)
    default_offset = len(positional) - len(node.args.defaults)
    arguments = []
    for index, argument in enumerate(positional):
        default = None
        if index >= default_offset:
            default = literal_or_source(node.args.defaults[index - default_offset], source)
        arguments.append({"name": argument.arg, "default": default})
    for argument, default_node in zip(node.args.kwonlyargs, node.args.kw_defaults):
        arguments.append({"name": argument.arg, "default": literal_or_source(default_node, source)})
    return {
        "qualified_name": f"{owner}.{node.name}" if owner else node.name,
        "name": node.name,
        "owner": owner,
        "line_start": node.lineno,
        "line_end": node.end_lineno,
        "arguments": arguments,
        "calls": call_names(node),
    }


def document(path: str) -> dict:
    source = (ROOT / path).read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source, filename=path)
    functions = []
    classes = []
    module_assignments = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(function_record(node, source, None))
        elif isinstance(node, ast.ClassDef):
            methods = [
                function_record(child, source, node.name)
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            class_assignments = []
            for child in node.body:
                if isinstance(child, (ast.Assign, ast.AnnAssign)):
                    targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                    value_node = child.value
                    for target in targets:
                        name = dotted_name(target)
                        if name:
                            class_assignments.append(
                                {
                                    "name": name,
                                    "line": child.lineno,
                                    "value": literal_or_source(value_node, source),
                                }
                            )
            classes.append(
                {
                    "name": node.name,
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "bases": [dotted_name(base) for base in node.bases],
                    "class_assignments": class_assignments,
                    "methods": methods,
                }
            )
            functions.extend(methods)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value_node = node.value
            for target in targets:
                name = dotted_name(target)
                if name and name in {
                    "R",
                    "F",
                    "kB",
                    "h",
                    "EV_TO_J",
                    "LCO_MSMR_LIT",
                    "GRAPHITE_STAGING_LIT",
                }:
                    module_assignments.append(
                        {
                            "name": name,
                            "line": node.lineno,
                            "value": literal_or_source(value_node, source),
                        }
                    )

    all_calls = [call for function in functions for call in function["calls"]]
    return {
        "path": path,
        "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "line_count": len(lines),
        "read_coverage": [[1, len(lines)]],
        "read_status": "COMPLETE",
        "module_assignments": module_assignments,
        "classes": classes,
        "functions": functions,
        "call_counts": {
            name: all_calls.count(name)
            for name in sorted(set(all_calls))
            if name.startswith("func_") or name.startswith("self.")
        },
    }


def comparison(pair_id: str, old_path: str, new_path: str) -> dict:
    old_lines = (ROOT / old_path).read_text(encoding="utf-8").splitlines()
    new_lines = (ROOT / new_path).read_text(encoding="utf-8").splitlines()
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    counts = {"equal": 0, "replace_old": 0, "replace_new": 0, "delete": 0, "insert": 0}
    for tag, a0, a1, b0, b1 in matcher.get_opcodes():
        if tag == "equal":
            counts["equal"] += a1 - a0
        elif tag == "replace":
            counts["replace_old"] += a1 - a0
            counts["replace_new"] += b1 - b0
        elif tag == "delete":
            counts["delete"] += a1 - a0
        elif tag == "insert":
            counts["insert"] += b1 - b0
    patch_rel = f"Codex/work/v1010_v1013_phase058/code_diffs/{pair_id}.patch"
    patch = "".join(
        difflib.unified_diff(
            [line + "\n" for line in old_lines],
            [line + "\n" for line in new_lines],
            fromfile=old_path,
            tofile=new_path,
            n=3,
        )
    )
    (ROOT / patch_rel).write_text(patch, encoding="utf-8")
    return {
        "pair_id": pair_id,
        "old_path": old_path,
        "new_path": new_path,
        "sequence_ratio": matcher.ratio(),
        "opcode_line_counts": counts,
        "exact_unified_diff": patch_rel,
        "exact_unified_diff_sha256": hashlib.sha256(patch.encode("utf-8")).hexdigest(),
    }


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    documents = [document(path) for path in PATHS]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "status": "CODE_SOURCE_READ_COMPLETE; TEST_AND_PROBE_ADJUDICATION_PENDING",
        "document_count": len(documents),
        "total_lines": sum(item["line_count"] for item in documents),
        "documents": documents,
        "comparisons": [
            comparison("code_v1010_to_v1012", PATHS[0], PATHS[1]),
            comparison("code_v1012_to_v1013", PATHS[1], PATHS[2]),
        ],
        "provisional_findings": [
            {
                "id": "CODE-001",
                "verdict": "BLOCKER_UNIT_CONTRACT",
                "claim": "curve computes I_use = c_rate * Q_cell while the theory lineage also permits/declares Q_cell in coulombs.",
            },
            {
                "id": "CODE-002",
                "verdict": "EMPIRICAL_ONLY",
                "claim": "A is frozen per transition as min(z_cut*n*R*T, A_cap_RT*R*T); defaults n=1, z_cut=4.357, A_cap_RT=4 select 4RT.",
            },
            {
                "id": "CODE-003",
                "verdict": "REJECT_ROLE_OVERLOAD",
                "claim": "Default use_dH_eff=True subtracts chi_d*Omega from activation enthalpy, so equilibrium interaction values directly alter kinetics.",
            },
            {
                "id": "CODE-004",
                "verdict": "DEFAULT_SHADOWING",
                "claim": "GRAPHITE_STAGING_LIT and LCO_MSMR_LIT contain both w and n=1; _n_factor gives n precedence, making all listed w values inert.",
            },
            {
                "id": "CODE-005",
                "verdict": "NUMERICAL_SWITCH",
                "claim": "The lag/equilibrium handoff is controlled by min_lag_grid_steps times grid_step, not a physical asymptotic matching condition.",
            },
            {
                "id": "CODE-006",
                "verdict": "THEORY_NOT_IMPLEMENTED",
                "claim": "LCO electronic entropy is evaluated at x_center and T_ref=298.15, so the document's composition-local and T-proportional/T-squared chain is absent.",
            },
            {
                "id": "CODE-007",
                "verdict": "CORRECTED_IN_V1013",
                "claim": "v1.0.13 adds electrode-aware facade direction mapping through _delith_is_discharge=False for LCO.",
            },
            {
                "id": "CODE-008",
                "verdict": "MATERIAL_SCOPE_MISSING",
                "claim": "No silicon or graphite-silicon blend production model exists in this lineage.",
            },
            {
                "id": "CODE-009",
                "verdict": "LCO_KINETICS_INACTIVE_BY_DEFAULT",
                "claim": "LCO_MSMR_LIT has no Omega, gamma, dH_a, or L_V; finite-current lag and hysteresis are inactive unless supplied externally.",
            },
            {
                "id": "CODE-010",
                "verdict": "INTERNAL_CONSISTENCY_ONLY",
                "claim": "entropy_coefficient differentiates the imposed width law and uses clipping/overlap weighting; agreement with code finite differences does not validate experimental entropy.",
            },
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
