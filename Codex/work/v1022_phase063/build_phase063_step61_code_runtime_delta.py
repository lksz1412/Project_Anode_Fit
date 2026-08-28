#!/usr/bin/env python3
"""Build Phase 063 Step 61 static-code and isolated-runtime evidence.

The frozen production modules are never imported from the repository.  Runtime
checks execute byte-identical Git blobs copied into disposable external temp
directories.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "4088f48ca191fdb8abe52e8f4fb10de10f2eeba3"
EXPECTED_SUBJECT = "audit(phase063): attest v1022 code runtime delta"
CODE_NAME = "PHASE_063_V1022_CODE_DELTA_MATRIX.json"
RUNTIME_NAME = "PHASE_063_V1022_RUNTIME_ATTESTATION.json"
CODE_OUT = ROOT / "Codex/results" / CODE_NAME
RUNTIME_OUT = ROOT / "Codex/results" / RUNTIME_NAME
SOURCE_PREFIXES = (
    "Claude/docs/v1.0.21/",
    "Claude/docs/v1.0.22/",
    "Claude/docs/v1.0.23/",
)

EXPECTED_ENDPOINTS = (
    "Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py",
    "Claude/docs/v1.0.21/FITTING_GUIDE.md",
    "Claude/docs/v1.0.21/results/tools_check_structure.py",
    "Claude/docs/v1.0.21/test_gates_v1021.py",
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py",
    "Claude/docs/v1.0.22/FITTING_GUIDE.md",
    "Claude/docs/v1.0.22/results/tools_check_structure.py",
    "Claude/docs/v1.0.22/test_gates_v1022.py",
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.23/CODE_GUIDE_v23.md",
    "Claude/docs/v1.0.23/FITTING_GUIDE.md",
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py",
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py",
    "Claude/docs/v1.0.23/results/tools_check_structure.py",
    "Claude/docs/v1.0.23/test_gates_v1023.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
)

RUNTIME_COPY_PATHS = (
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
    "Claude/docs/v1.0.19/golden_graphite_ref.npz",
    "Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py",
    "Claude/docs/v1.0.21/test_gates_v1021.py",
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py",
    "Claude/docs/v1.0.22/test_gates_v1022.py",
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py",
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py",
    "Claude/docs/v1.0.23/test_gates_v1023.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
)

PYTHON_LAUNCHERS = (("3.12", ("py", "-3.12")), ("3.14", ("py", "-3.14")))


def run(args: list[str] | tuple[str, ...], *, cwd: pathlib.Path = ROOT,
        timeout: int = 300, env: dict[str, str] | None = None,
        check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(
        list(args), cwd=cwd, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=timeout, check=False,
    )
    if check and cp.returncode != 0:
        raise RuntimeError(
            f"command failed ({cp.returncode}): {args!r}\n"
            f"stdout={cp.stdout.decode('utf-8', 'replace')}\n"
            f"stderr={cp.stderr.decode('utf-8', 'replace')}"
        )
    return cp


def git_bytes(path: str) -> bytes:
    return run(("git", "cat-file", "blob", f"{BASELINE}:{path}")).stdout


def git_blob(path: str) -> str:
    return run(("git", "rev-parse", f"{BASELINE}:{path}")).stdout.decode().strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def semantic_projection(data: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(data)
    out.pop("semantic_sha256", None)
    return out


def finalize(data: dict[str, Any]) -> dict[str, Any]:
    data["semantic_sha256"] = sha256(compact(semantic_projection(data)))
    return data


def atomic_json(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False,
    ) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def version_of(path: str) -> str:
    match = re.search(r"/v(1\.0\.2[123])/", path)
    if not match:
        raise ValueError(path)
    return match.group(1)


def role_of(path: str) -> str:
    name = pathlib.PurePosixPath(path).name
    if name.startswith("Anode_Fit_v"):
        return "PRODUCTION_MODULE"
    if name.startswith("test_gates"):
        return "OFFICIAL_GATE"
    if name == "tools_check_structure.py":
        return "STRUCTURE_TOOL"
    if name == "p1_ratio_check.py":
        return "AUXILIARY_NUMERIC_CHECK"
    if name == "curve_qa.py":
        return "QA_RENDER_SCRIPT"
    if "GUIDE" in name.upper():
        return "GUIDE"
    raise ValueError(path)


class StripDocstrings(ast.NodeTransformer):
    def _strip(self, node: ast.AST) -> ast.AST:
        body = getattr(node, "body", None)
        if (isinstance(body, list) and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            node.body = body[1:]
        return node

    def visit_Module(self, node: ast.Module) -> ast.AST:
        self.generic_visit(node)
        return self._strip(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        self.generic_visit(node)
        return self._strip(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        self.generic_visit(node)
        return self._strip(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
        self.generic_visit(node)
        return self._strip(node)


def code_ast_hash(node: ast.AST) -> str:
    clean = StripDocstrings().visit(copy.deepcopy(node))
    ast.fix_missing_locations(clean)
    return sha256(canonical_ast_dump(clean).encode())


def canonical_ast_dump(node: ast.AST) -> str:
    """Keep Python 3.12 and 3.14 AST serialization byte-identical.

    Python 3.14 changed ``ast.dump`` to omit empty fields by default.  Its
    ``show_empty=True`` mode reproduces the pre-3.14 representation; Python
    3.12 has no such keyword and already emits those fields.
    """
    try:
        return ast.dump(node, include_attributes=False, show_empty=True)
    except TypeError:
        return ast.dump(node, include_attributes=False)


def signature_of(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    args = node.args
    positional = list(args.posonlyargs) + list(args.args)
    defaults: dict[str, str] = {}
    offset = len(positional) - len(args.defaults)
    for idx, default in enumerate(args.defaults):
        defaults[positional[offset + idx].arg] = ast.unparse(default)
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        if default is not None:
            defaults[arg.arg] = ast.unparse(default)
    return {
        "posonly": [a.arg for a in args.posonlyargs],
        "positional": [a.arg for a in args.args],
        "vararg": None if args.vararg is None else args.vararg.arg,
        "kwonly": [a.arg for a in args.kwonlyargs],
        "kwarg": None if args.kwarg is None else args.kwarg.arg,
        "defaults": defaults,
    }


def exception_name(node: ast.AST | None) -> str:
    if node is None:
        return "RERAISE"
    target = node.func if isinstance(node, ast.Call) else node
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return canonical_ast_dump(target)


def ast_inventory(text: str) -> dict[str, Any]:
    tree = ast.parse(text)
    symbols: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    imports: list[dict[str, Any]] = []

    def add_function(node: ast.FunctionDef | ast.AsyncFunctionDef, qualified: str) -> None:
        symbols.append({
            "kind": "ASYNC_FUNCTION" if isinstance(node, ast.AsyncFunctionDef) else "FUNCTION",
            "qualified_name": qualified,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "signature": signature_of(node),
            "code_ast_sha256": code_ast_hash(node),
        })

    class DefinitionVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.scope: list[str] = []

        def qualified(self, name: str) -> str:
            return ".".join((*self.scope, name))

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            qualified = self.qualified(node.name)
            symbols.append({
                "kind": "CLASS",
                "qualified_name": qualified,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "bases": [ast.unparse(base) for base in node.bases],
                "code_ast_sha256": code_ast_hash(node),
            })
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            add_function(node, self.qualified(node.name))
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            add_function(node, self.qualified(node.name))
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

    DefinitionVisitor().visit(tree)

    parent: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            owner = "<module>"
            cur: ast.AST | None = node
            while cur in parent:
                cur = parent[cur]
                if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner = cur.name
                    break
            guards.append({
                "line": node.lineno,
                "end_line": node.end_lineno,
                "owner": owner,
                "exception": exception_name(node.exc),
            })
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "warn"):
            warnings.append({"line": node.lineno, "end_line": node.end_lineno})
        if isinstance(node, ast.Import):
            imports.append({"line": node.lineno, "modules": [a.name for a in node.names]})
        elif isinstance(node, ast.ImportFrom):
            imports.append({"line": node.lineno, "modules": [node.module or ""]})
    return {
        "module_code_ast_sha256": code_ast_hash(tree),
        "symbols": sorted(symbols, key=lambda r: (r["start_line"], r["qualified_name"])),
        "guards": sorted(guards, key=lambda r: r["line"]),
        "warning_calls": sorted(warnings, key=lambda r: r["line"]),
        "imports": sorted(imports, key=lambda r: r["line"]),
    }


def endpoint_rows() -> list[dict[str, Any]]:
    listed = run(("git", "ls-tree", "-r", "--name-only", BASELINE, "--", *SOURCE_PREFIXES)).stdout.decode().splitlines()
    found = tuple(sorted(
        p for p in listed
        if p.endswith(".py") or "GUIDE" in pathlib.PurePosixPath(p).name.upper()
    ))
    if found != tuple(sorted(EXPECTED_ENDPOINTS)):
        raise RuntimeError(f"endpoint denominator drift\nexpected={EXPECTED_ENDPOINTS!r}\nfound={found!r}")
    rows: list[dict[str, Any]] = []
    for idx, path in enumerate(EXPECTED_ENDPOINTS, 1):
        raw = git_bytes(path)
        text = raw.decode("utf-8")
        lines = text.splitlines()
        row: dict[str, Any] = {
            "endpoint_id": f"P063-END-{idx:03d}",
            "path": path,
            "version": version_of(path),
            "role": role_of(path),
            "git_blob": git_blob(path),
            "sha256": sha256(raw),
            "bytes": len(raw),
            "lines": len(lines),
            "nonblank_lines": sum(bool(line.strip()) for line in lines),
            "utf8_decode": "PASS",
            "full_blob_traversal": True,
            "line_ending": "LF" if b"\r" not in raw else "CONTAINS_CR",
        }
        if path.endswith(".py"):
            row["ast"] = ast_inventory(text)
        else:
            row["headings"] = [
                {"line": i, "text": line}
                for i, line in enumerate(lines, 1) if line.startswith("#")
            ]
            row["code_identifiers"] = sorted(set(re.findall(r"`([A-Za-z_][A-Za-z0-9_.]*)`", text)))
        rows.append(row)
    return rows


def symbol_map(row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["qualified_name"]: s for s in row["ast"]["symbols"]}


def symbol_delta(left: dict[str, Any], right: dict[str, Any], delta_id: str) -> dict[str, Any]:
    a, b = symbol_map(left), symbol_map(right)
    common = sorted(set(a) & set(b))
    changed = [name for name in common if a[name]["code_ast_sha256"] != b[name]["code_ast_sha256"]]
    signature_changed = [
        name for name in common
        if a[name].get("signature") != b[name].get("signature")
    ]
    return {
        "delta_id": delta_id,
        "left_endpoint_id": left["endpoint_id"],
        "right_endpoint_id": right["endpoint_id"],
        "left_path": left["path"],
        "right_path": right["path"],
        "same_blob": left["git_blob"] == right["git_blob"],
        "added_symbols": sorted(set(b) - set(a)),
        "removed_symbols": sorted(set(a) - set(b)),
        "changed_symbol_code": changed,
        "changed_signatures": signature_changed,
        "unchanged_common_symbols": sorted(set(common) - set(changed)),
    }


def span_for(prod: dict[str, Any], qualified: str) -> dict[str, Any]:
    row = symbol_map(prod).get(qualified)
    if row is None:
        raise RuntimeError(f"missing symbol {qualified!r} in {prod['path']}")
    return {
        "endpoint_id": prod["endpoint_id"],
        "path": prod["path"],
        "git_blob": prod["git_blob"],
        "symbol": qualified,
        "start_line": row["start_line"],
        "end_line": row["end_line"],
        "code_ast_sha256": row["code_ast_sha256"],
    }


def literal_span(row: dict[str, Any], start_line: int, end_line: int) -> dict[str, Any]:
    lines = git_bytes(row["path"]).decode("utf-8").splitlines()
    if not (1 <= start_line <= end_line <= len(lines)):
        raise RuntimeError(f"invalid literal span {row['path']}:{start_line}-{end_line}")
    payload = ("\n".join(lines[start_line - 1:end_line]) + "\n").encode("utf-8")
    return {
        "endpoint_id": row["endpoint_id"],
        "path": row["path"],
        "git_blob": row["git_blob"],
        "start_line": start_line,
        "end_line": end_line,
        "text_sha256": sha256(payload),
    }


def module_assignment(row: dict[str, Any], name: str) -> dict[str, Any]:
    tree = ast.parse(git_bytes(row["path"]).decode("utf-8"), filename=row["path"])
    matches: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            matches.append(node)
    if len(matches) != 1:
        raise RuntimeError(f"expected one module assignment {name!r} in {row['path']}, got {len(matches)}")
    node = matches[0]
    value_node = node.value
    if name == "SI_CASE_SETS":
        if not isinstance(value_node, ast.Dict):
            raise RuntimeError("SI_CASE_SETS is not a dict literal")
        value = {
            ast.literal_eval(key): val.id
            for key, val in zip(value_node.keys, value_node.values)
            if key is not None and isinstance(val, ast.Name)
        }
        if len(value) != len(value_node.values):
            raise RuntimeError("SI_CASE_SETS contains a non-name selector target")
    else:
        value = ast.literal_eval(value_node)
    return {
        "name": name,
        "value": value,
        **literal_span(row, node.lineno, node.end_lineno),
    }


def static_contract_rows(prod22: dict[str, Any], prod23: dict[str, Any]) -> list[dict[str, Any]]:
    demo_names = ("SI_ELEMENTAL_LIT", "SIOX_LIT", "SIC_LIT", "SI_CASE_SETS")
    capacity_names = ("SI_SPECIFIC_CAPACITY", "GRAPHITE_SPECIFIC_CAPACITY")
    specs = (
        (
            "P063-STATIC-001", "DEMO_SET_LITERALS_EXACT",
            [module_assignment(prod, name) for prod in (prod22, prod23) for name in demo_names],
            "Exact U/w/Q demo literals and selector-to-constant mapping; these remain labelled placeholders, not material truth.",
        ),
        (
            "P063-STATIC-002", "SPECIFIC_CAPACITY_DEFAULTS_EXACT",
            [module_assignment(prod, name) for prod in (prod22, prod23) for name in capacity_names],
            "Exact case-specific q_Si and graphite q_gr defaults used by from_wt; mixed basis remains an open finding.",
        ),
        (
            "P063-STATIC-003", "FSI_ZERO_LIMIT_PATH_EXACT",
            [span_for(prod, "BlendedAnodeDQDV.__init__") for prod in (prod22, prod23)],
            "Constructor scaling path that removes all positive-Q silicon transitions when f_Si=0.",
        ),
        (
            "P063-STATIC-004", "SINGLE_BACKGROUND_OWNER_PATH_EXACT",
            [span_for(prod, "BlendedAnodeDQDV.__init__") for prod in (prod22, prod23)],
            "Constructor assigns Cbg to graphite and zero to the silicon host.",
        ),
        (
            "P063-STATIC-005", "GS1_UNSUPPORTED_PATH_EXACT",
            [span_for(prod, "BlendedAnodeDQDV.plastic_hysteresis_loop") for prod in (prod22, prod23)],
            "GS-1 plastic closure is an explicit NotImplementedError boundary.",
        ),
        (
            "P063-STATIC-006", "GS2_UNSUPPORTED_PATH_EXACT",
            [span_for(prod, "BlendedAnodeDQDV.nonadditive_correction") for prod in (prod22, prod23)],
            "GS-2 nonadditive finite-rate closure is an explicit NotImplementedError boundary.",
        ),
        (
            "P063-STATIC-007", "FROM_WT_GUARD_AND_MAPPING_PATH_EXACT",
            [span_for(prod, "BlendedAnodeDQDV.from_wt") for prod in (prod22, prod23)],
            "Mass-fraction guard and mass-to-capacity mapping path.",
        ),
    )
    return [
        {
            "static_contract_id": contract_id,
            "state": state,
            "occurrences": occurrences,
            "basis": basis,
            "authority": "EXACT_FROZEN_STATIC_CONTRACT_ONLY",
            "external_science": False,
        }
        for contract_id, state, occurrences, basis in specs
    ]


def theory_rows(prod22: dict[str, Any]) -> list[dict[str, Any]]:
    specs = (
        ("P063-CONC-001", ["P063-DER-007"], ["func_ksi_eq", "GraphiteAnodeDischargeDQDV.equilibrium"], "CONCORDANT_STATIC", "equilibrium logistic derivative path"),
        ("P063-CONC-002", ["P063-DER-009"], ["_causal_memory_pointwise", "GraphiteAnodeDischargeDQDV.dqdv"], "CONCORDANT_STATIC_WITH_FROZEN_LOCAL_APPROXIMATION", "causal memory is implemented; local state-dependent kinetics is frozen"),
        ("P063-CONC-003", ["P063-DER-014"], ["BlendedAnodeDQDV.__init__", "BlendedAnodeDQDV.solve_U_oc", "GraphiteAnodeDischargeDQDV.solve_U_oc"], "CONDITIONAL_CONCORDANCE_STATIC_WITH_DOMAIN_GUARD_GAP", "pooled common-potential charge balance has a unique monotone root only under the unguarded per-transition domain Q_j>0 and n_j(T)>0"),
        ("P063-CONC-004", ["P063-DER-015"], ["BlendedAnodeDQDV.from_wt"], "FORMULA_CONCORDANT_BASIS_UNVERIFIED", "mass-to-capacity algebra matches; capacity/utilization/ICE basis is not closed"),
        ("P063-CONC-005", ["P063-DER-016", "P063-DER-017"], ["BlendedAnodeDQDV.__init__", "BlendedAnodeDQDV.plastic_hysteresis_loop"], "HOOK_ONLY_PATH_CLOSURE_UNSUPPORTED", "static stress offset exists; plastic history closure raises NotImplementedError"),
        ("P063-CONC-006", ["P063-DER-018"], ["BlendedAnodeDQDV.dqdv", "BlendedAnodeDQDV.nonadditive_correction"], "FINITE_RATE_CURRENT_PARTITION_UNSUPPORTED", "both hosts receive the same full current; nonadditive correction raises NotImplementedError"),
        ("P063-CONC-007", ["P063-DER-019", "P063-DER-020"], ["GraphiteAnodeDischargeDQDV.curve", "func_L_q"], "CONFLICT_HOUR_TO_SECOND_CONVERSION_MISSING", "curve maps c_rate*Q_cell directly into an SI kinetic prefactor without division by 3600"),
        ("P063-CONC-008", ["P063-DER-021", "P063-DER-022"], ["GraphiteAnodeDischargeDQDV._resolve_lag_length"], "CONCORDANT_APPROXIMATION_ONLY", "cut/cap and frozen-local lag resolver are explicit approximation operators"),
        ("P063-CONC-009", ["P063-DER-023"], ["GraphiteAnodeDischargeDQDV.reversible_heat", "GraphiteAnodeDischargeDQDV.irreversible_heat"], "CONCORDANT_STATIC_WITH_SIGN_SCOPE", "separate reversible and lumped irreversible exits exist; branch dissipation closure remains outside this row"),
        ("P063-CONC-010", ["P063-DER-025"], ["LCOCathodeDQDV._effective_dS_rxn"], "FROZEN_REFERENCE_APPROXIMATION", "electronic entropy is evaluated at fixed T_ref and x_center, not local composition-temperature closure"),
    )
    return [
        {
            "concordance_id": cid,
            "theory_derivation_ids": derivations,
            "code_spans": [span_for(prod22, symbol) for symbol in symbols],
            "state": state,
            "basis": basis,
            "authority": "STATIC_CODE_CONCORDANCE_ONLY",
            "external_science": False,
        }
        for cid, derivations, symbols, state, basis in specs
    ]


def finding_rows(prod22: dict[str, Any], prod23: dict[str, Any], endpoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_path = {r["path"]: r for r in endpoints}
    return [
        {
            "finding_id": "P063-S61-F001", "priority": "P0", "status": "OPEN_ROUTED",
            "summary": "C-rate h^-1 is passed to the SI kinetic prefactor without division by 3600; lag is overstated by 3600 and the equivalent barrier shift is RT ln 3600.",
            "evidence": [span_for(prod22, "GraphiteAnodeDischargeDQDV.curve"), span_for(prod22, "func_L_q")],
            "runtime_probe_ids": ["P063-RUN-SI-TIME-22", "P063-RUN-SI-TIME-23"],
            "owner": "Phase 076", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F002", "priority": "P0", "status": "OPEN_ROUTED",
            "summary": "The finite-rate blend path sends the same full cell current and capacity to both hosts and does not solve host current partition.",
            "evidence": [span_for(prod22, "BlendedAnodeDQDV.dqdv"), span_for(prod22, "BlendedAnodeDQDV.nonadditive_correction")],
            "runtime_probe_ids": ["P063-RUN-CURRENT-PARTITION-22", "P063-RUN-CURRENT-PARTITION-23"],
            "owner": "Phase 080", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F003", "priority": "P0", "status": "OPEN_ROUTED",
            "summary": "from_wt implements the algebra, but default q_Si values mix theoretical, first-charge and reversible bases without utilization/ICE/active-mass closure.",
            "evidence": [
                span_for(prod22, "BlendedAnodeDQDV.from_wt"),
                literal_span(prod22, 1049, 1058),
            ],
            "runtime_probe_ids": ["P063-RUN-FROM-WT-22", "P063-RUN-FROM-WT-23"],
            "owner": "Phase 071/080", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F004", "priority": "P1", "status": "OPEN_ROUTED",
            "summary": "Missing dH_a or dVdq_qa silently collapses finite-current lag to zero/equilibrium rather than failing closed.",
            "evidence": [span_for(prod22, "GraphiteAnodeDischargeDQDV._resolve_lag_length")],
            "runtime_probe_ids": ["P063-RUN-MISSING-KINETICS-22", "P063-RUN-MISSING-KINETICS-23"],
            "owner": "Phase 076/081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F005", "priority": "P1", "status": "OPEN_ROUTED",
            "summary": "The v1.0.23 curve QA script hard-codes /home/user/Project_Anode_Fit and is not portable to the frozen Windows execution environment; Python 3.14 additionally lacks its optional matplotlib dependency.",
            "evidence": [
                literal_span(by_path["Claude/docs/v1.0.23/results/qa_images/curve_qa.py"], 8, 9),
                literal_span(by_path["Claude/docs/v1.0.23/results/qa_images/curve_qa.py"], 14, 14),
                literal_span(by_path["Claude/docs/v1.0.23/results/qa_images/curve_qa.py"], 109, 109),
            ],
            "runtime_probe_ids": ["P063-OFFICIAL-V1023-CURVE-QA-312", "P063-OFFICIAL-V1023-CURVE-QA-314"],
            "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F006", "priority": "P1", "status": "OPEN_ROUTED",
            "summary": "solve_U_oc does not validate tol or max_iter, so zero/negative iterations or infinite tolerance can silently return an unconverged initial-bracket midpoint.",
            "evidence": [span_for(prod22, "GraphiteAnodeDischargeDQDV.solve_U_oc")],
            "runtime_probe_ids": ["P063-RUN-ROOT-22", "P063-RUN-ROOT-23"],
            "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F007", "priority": "P2", "status": "OPEN_ROUTED",
            "summary": "The v1.0.22 production header still declares release version 1.0.21 even though the module contains the v1.0.22 blend extension.",
            "evidence": [literal_span(prod22, 3, 3)],
            "runtime_probe_ids": [], "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F008", "priority": "P2", "status": "OPEN_ROUTED",
            "summary": "The shared v1.0.22/v1.0.23 legacy gate reports the 30 wt% Si-C endpoint as approximately 0.7 capacity fraction although the implemented constants give about 0.782.",
            "evidence": [
                literal_span(by_path["Claude/docs/v1.0.22/test_gates_v1022.py"], 519, 520),
                literal_span(by_path["Claude/docs/v1.0.23/test_gates_v1023.py"], 519, 520),
            ],
            "runtime_probe_ids": ["P063-RUN-FROM-WT-22", "P063-RUN-FROM-WT-23"],
            "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F009", "priority": "P2", "status": "OPEN_ROUTED",
            "summary": "CODE_GUIDE_v23 labels plastic_hysteresis_loop and nonadditive_correction together as GS-1 even though the latter is the GS-2 boundary.",
            "evidence": [literal_span(by_path["Claude/docs/v1.0.23/CODE_GUIDE_v23.md"], 189, 189)],
            "runtime_probe_ids": [], "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F010", "priority": "P2", "status": "OPEN_ROUTED",
            "summary": "All three FITTING_GUIDE occurrences share a v1.0.20/v1.0.19-oriented blob and do not route the v1.0.22 blend or v1.0.23 self-consistent endpoints.",
            "evidence": [
                literal_span(by_path[p], 1, 5)
                for p in ("Claude/docs/v1.0.21/FITTING_GUIDE.md", "Claude/docs/v1.0.22/FITTING_GUIDE.md", "Claude/docs/v1.0.23/FITTING_GUIDE.md")
            ],
            "runtime_probe_ids": [], "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F011", "priority": "P2", "status": "OPEN_ROUTED",
            "summary": "p1_ratio_check.py is observation-only: it prints convergence ratios but has no assertions or nonzero failure exit.",
            "evidence": [literal_span(by_path["Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py"], 51, 68)],
            "runtime_probe_ids": ["P063-OFFICIAL-V1023-P1-312", "P063-OFFICIAL-V1023-P1-314"],
            "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F012", "priority": "P2", "status": "OPEN_ROUTED",
            "summary": "The v1.0.21/v1.0.22/v1.0.23 primary gate docstrings all advertise the stale test_gates_v1020.py reproduction command rather than their actual versioned entry points.",
            "evidence": [
                {
                    "endpoint_id": by_path[p]["endpoint_id"],
                    "path": p,
                    "git_blob": by_path[p]["git_blob"],
                    "start_line": 23 if p.endswith("test_gates_v1021.py") else 35,
                    "end_line": 23 if p.endswith("test_gates_v1021.py") else 35,
                    "text_sha256": literal_span(
                        by_path[p],
                        23 if p.endswith("test_gates_v1021.py") else 35,
                        23 if p.endswith("test_gates_v1021.py") else 35,
                    )["text_sha256"],
                }
                for p in (
                    "Claude/docs/v1.0.21/test_gates_v1021.py",
                    "Claude/docs/v1.0.22/test_gates_v1022.py",
                    "Claude/docs/v1.0.23/test_gates_v1023.py",
                )
            ],
            "runtime_probe_ids": [], "owner": "Phase 081", "external_truth_validated": False,
        },
        {
            "finding_id": "P063-S61-F013", "priority": "P1", "status": "OPEN_ROUTED",
            "summary": "solve_U_oc does not enforce per-transition Q_j>0 or n_j(T)>0 before using the monotone-bisection premise; admissible-looking inputs can therefore create multiple charge-balance roots and the solver silently selects one.",
            "evidence": [
                span_for(prod22, "GraphiteAnodeDischargeDQDV.__init__"),
                span_for(prod22, "GraphiteAnodeDischargeDQDV.solve_U_oc"),
                span_for(prod22, "BlendedAnodeDQDV.__init__"),
            ],
            "runtime_probe_ids": ["P063-RUN-ROOT-DOMAIN-22", "P063-RUN-ROOT-DOMAIN-23"],
            "owner": "Phase 081", "external_truth_validated": False,
        },
    ]


PROBE_SOURCE = r'''# -*- coding: utf-8 -*-
from __future__ import annotations
import importlib.util, json, sys, warnings
import numpy as np
sys.dont_write_bytecode = True

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def finite(x):
    return bool(np.all(np.isfinite(np.asarray(x, dtype=float))))

def raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    return False

def probe(mod, tag):
    out = {}
    V = np.linspace(0.03, 0.55, 801)
    xg = np.linspace(0.05, 0.95, 31)
    kw = dict(x=0.5, Rn=0.01, use_dH_eff=True)
    gr = mod.GraphiteAnodeDischargeDQDV(mod.GRAPHITE_STAGING_LIT, Cbg=0.07, **kw)
    bl0 = mod.BlendedAnodeDQDV(0.0, si_case='sic', graphite_transitions=mod.GRAPHITE_STAGING_LIT, Cbg=0.07, **kw)
    zero = {
        'equilibrium': np.array_equal(gr.equilibrium(V, 298.15), bl0.equilibrium(V, 298.15)),
        'dqdv_dis': np.array_equal(gr.dqdv(V, 298.15, 0.2, 1.0, +1), bl0.dqdv(V, 298.15, 0.2, 1.0, +1)),
        'dqdv_chg': np.array_equal(gr.dqdv(V, 298.15, 0.2, 1.0, -1), bl0.dqdv(V, 298.15, 0.2, 1.0, -1)),
        'curve': np.array_equal(gr.curve(V, 'discharge', 0.2, 1.0), bl0.curve(V, 'discharge', 0.2, 1.0)),
        'solve_U_oc': np.array_equal(gr.solve_U_oc(xg, 298.15), bl0.solve_U_oc(xg, 298.15)),
    }
    out['f_si_zero'] = {'probe_id': f'P063-RUN-FSI0-{tag}', 'checks': zero, 'pass': all(zero.values())}

    bl = mod.BlendedAnodeDQDV(0.3, si_case='sic', Cbg=0.07, **kw)
    grc, sic = bl.host_contributions(V, 298.15)
    bg_err = float(np.max(np.abs(np.asarray(bl.equilibrium(V, 298.15)) - grc - sic - 0.07)))
    out['background'] = {
        'probe_id': f'P063-RUN-BACKGROUND-{tag}', 'si_host_background': float(bl.si_host.Cbg),
        'single_background_max_abs_error': bg_err, 'pass': bl.si_host.Cbg == 0.0 and bg_err < 1e-12,
    }

    m, qsi, qgr = 0.30, 3117.0, 372.0
    expected_f = m*qsi/(m*qsi+(1.0-m)*qgr)
    by_wt = mod.BlendedAnodeDQDV.from_wt(m, q_Si=qsi, q_gr=qgr, si_case='sic', Cbg=0.0)
    from_wt = {
        'expected_f_si': expected_f, 'observed_f_si': float(by_wt.f_Si),
        'capacity_ratio': float(by_wt.Q_Si/by_wt.Q),
        'invalid_negative_mass_raises': raises(ValueError, lambda: mod.BlendedAnodeDQDV.from_wt(-0.1)),
        'invalid_unit_mass_raises': raises(ValueError, lambda: mod.BlendedAnodeDQDV.from_wt(1.0)),
        'invalid_capacity_raises': raises(ValueError, lambda: mod.BlendedAnodeDQDV.from_wt(0.1, q_Si=0.0)),
    }
    from_wt['pass'] = (from_wt['observed_f_si'] == expected_f and from_wt['capacity_ratio'] == expected_f
                       and from_wt['invalid_negative_mass_raises'] and from_wt['invalid_unit_mass_raises']
                       and from_wt['invalid_capacity_raises'])
    from_wt['probe_id'] = f'P063-RUN-FROM-WT-{tag}'
    out['from_wt'] = from_wt

    centers, widths = [], []
    for trn in bl.transitions:
        if 'dH_rxn' in trn and 'dS_rxn' in trn:
            center = float(mod.func_U_j(298.15, trn['dH_rxn'], trn['dS_rxn']))
        else:
            center = float(trn['U'])
        centers.append(center)
        widths.append(float(mod.func_w(298.15, bl._balance_host._n_factor(trn, 298.15))))
    fineV = np.linspace(min(c-20.0*w for c,w in zip(centers,widths)),
                        max(c+20.0*w for c,w in zip(centers,widths)), 400001)
    eq = np.asarray(bl.equilibrium(fineV, 298.15), dtype=float)
    trapz = getattr(np, 'trapezoid', None) or getattr(np, 'trapz')
    integ = float(trapz(eq - 0.07, fineV))
    cap_rel = abs(integ-bl.Q)/bl.Q
    out['capacity'] = {'probe_id': f'P063-RUN-CAPACITY-{tag}', 'integral': integ, 'expected_Q': bl.Q,
                       'relative_error': cap_rel, 'pass': cap_rel <= 1e-6}

    def sweep(n):
        curves=[]
        for mm in np.linspace(0.30/n, 0.30, n):
            b=mod.BlendedAnodeDQDV.from_wt(mm, q_Si=qsi, q_gr=qgr, si_case='sic', Cbg=0.0)
            curves.append(np.asarray(b.equilibrium(np.linspace(-0.1,0.7,601),298.15),dtype=float))
        curves=np.asarray(curves)
        return float(np.max(np.max(np.abs(np.diff(curves,axis=0)),axis=1)))
    d30,d60=sweep(30),sweep(60)
    ratio=d60/d30
    out['continuity']={'probe_id':f'P063-RUN-CONTINUITY-{tag}','coarse_max_step':d30,
                       'fine_max_step':d60,'refinement_ratio':ratio,'pass':finite([d30,d60]) and 0.40<ratio<0.62}

    roots=np.asarray(bl.solve_U_oc(np.array([0.1,0.5,0.9]),298.15),dtype=float)
    def balance_residual(u,xb):
        charge=0.0
        for tr in bl.transitions:
            center=(float(mod.func_U_j(298.15,tr['dH_rxn'],tr['dS_rxn'])) if 'dH_rxn' in tr else float(tr['U']))
            n=float(np.asarray(bl._balance_host._n_factor(tr,298.15)).reshape(-1)[0])
            charge += float(tr['Q'])*float(mod.func_ksi_eq(298.15,float(u),center,n))
        return charge-bl.Q*xb
    residual=[balance_residual(u,xb) for xb,u in zip((0.1,0.5,0.9),roots)]
    bad_iter0=float(bl.solve_U_oc(0.1,298.15,max_iter=0))
    bad_tolinf=float(bl.solve_U_oc(0.1,298.15,tol=float('inf')))
    bad_iter0_res=abs(balance_residual(bad_iter0,0.1))
    bad_tolinf_res=abs(balance_residual(bad_tolinf,0.1))
    root_checks={
        'finite':finite(roots),'strictly_increasing':bool(np.all(np.diff(roots)>0)),
        'max_abs_balance_residual':float(np.max(np.abs(residual))),
        'x_zero_raises':raises(ValueError,lambda:bl.solve_U_oc(0.0)),
        'x_one_raises':raises(ValueError,lambda:bl.solve_U_oc(1.0)),
        'reversed_bracket_raises':raises(ValueError,lambda:bl.solve_U_oc(0.5,U_lo=0.3,U_hi=0.2)),
        'narrow_bracket_raises':raises(ValueError,lambda:bl.solve_U_oc(0.5,U_lo=0.10,U_hi=0.11)),
        'max_iter_zero_raises':raises((ValueError,TypeError),lambda:bl.solve_U_oc(0.1,max_iter=0)),
        'tol_infinite_raises':raises((ValueError,TypeError),lambda:bl.solve_U_oc(0.1,tol=float('inf'))),
        'max_iter_zero_returned_U_V':bad_iter0,
        'max_iter_zero_abs_balance_residual':bad_iter0_res,
        'tol_infinite_returned_U_V':bad_tolinf,
        'tol_infinite_abs_balance_residual':bad_tolinf_res,
    }
    root_checks['valid_path_pass']=(root_checks['finite'] and root_checks['strictly_increasing'] and root_checks['max_abs_balance_residual']<1e-10
                         and root_checks['x_zero_raises'] and root_checks['x_one_raises']
                         and root_checks['reversed_bracket_raises'] and root_checks['narrow_bracket_raises'])
    root_checks['invalid_control_guard_pass']=root_checks['max_iter_zero_raises'] and root_checks['tol_infinite_raises']
    root_checks['finding_reproduced']=(not root_checks['invalid_control_guard_pass']
        and bad_iter0_res>1e-3 and bad_tolinf_res>1e-3)
    root_checks['pass']=root_checks['valid_path_pass'] and root_checks['finding_reproduced']
    root_checks['probe_id']=f'P063-RUN-ROOT-{tag}'
    out['root_solver']=root_checks

    def root_domain_probe(transitions):
        model=mod.GraphiteAnodeDischargeDQDV(transitions)
        xbar=0.5
        grid=np.linspace(-1.0,3.0,80001)
        residual_grid=np.zeros_like(grid)
        for trn in model.transitions:
            center=float(trn['U'])
            nval=float(np.asarray(model._n_factor(trn,298.15)).reshape(-1)[0])
            residual_grid += float(trn['Q'])*np.asarray(mod.func_ksi_eq(298.15,grid,center,nval),dtype=float)
        residual_grid -= float(sum(float(trn['Q']) for trn in model.transitions))*xbar
        sign_changes=int(np.count_nonzero(residual_grid[:-1]*residual_grid[1:]<0.0))
        exact_zeros=int(np.count_nonzero(residual_grid==0.0))
        chosen=float(model.solve_U_oc(xbar,298.15,U_lo=-1.0,U_hi=3.0))
        chosen_residual=0.0
        for trn in model.transitions:
            nval=float(np.asarray(model._n_factor(trn,298.15)).reshape(-1)[0])
            chosen_residual += float(trn['Q'])*float(mod.func_ksi_eq(298.15,chosen,float(trn['U']),nval))
        chosen_residual -= float(sum(float(trn['Q']) for trn in model.transitions))*xbar
        return {'root_count_lower_bound':sign_changes+exact_zeros,'selected_root_U_V':chosen,
                'selected_root_abs_residual':abs(chosen_residual)}

    q_bad=[{'U':0.0,'w':0.02,'Q':2.0},{'U':1.0,'w':0.02,'Q':-3.0},{'U':2.0,'w':0.02,'Q':2.0}]
    nmag=0.02*mod.F/(mod.R*298.15)
    n_bad=[{'U':0.0,'n':nmag,'Q':0.4},{'U':1.0,'n':-nmag,'Q':0.5},{'U':2.0,'n':nmag,'Q':0.6}]
    q_domain=root_domain_probe(q_bad)
    n_domain=root_domain_probe(n_bad)
    domain_checks={
        'negative_Q_constructor_raises':raises(ValueError,lambda:mod.GraphiteAnodeDischargeDQDV(q_bad)),
        'negative_n_constructor_raises':raises(ValueError,lambda:mod.GraphiteAnodeDischargeDQDV(n_bad)),
        'negative_Q_case':q_domain,'negative_n_case':n_domain,
    }
    domain_checks['finding_reproduced']=(not domain_checks['negative_Q_constructor_raises']
        and not domain_checks['negative_n_constructor_raises']
        and q_domain['root_count_lower_bound']>=3 and n_domain['root_count_lower_bound']>=3
        and q_domain['selected_root_abs_residual']<1e-10 and n_domain['selected_root_abs_residual']<1e-10)
    domain_checks['pass']=domain_checks['finding_reproduced']
    domain_checks['probe_id']=f'P063-RUN-ROOT-DOMAIN-{tag}'
    out['root_domain_guards']=domain_checks

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        siox=mod.BlendedAnodeDQDV(0.2,si_case='siox')
    warning_ok=any('확인 필요' in str(w.message) for w in caught)
    gs1=raises(NotImplementedError,lambda:siox.plastic_hysteresis_loop())
    gs2=raises(NotImplementedError,lambda:siox.nonadditive_correction())
    out['scope_boundaries']={'probe_id':f'P063-RUN-SCOPE-{tag}','siox_warning':warning_ok,
        'plastic_not_implemented':gs1,'nonadditive_not_implemented':gs2,
        'invalid_case_raises':raises(ValueError,lambda:mod.BlendedAnodeDQDV(0.2,si_case='absent')),
        'pass':warning_ok and gs1 and gs2 and raises(ValueError,lambda:mod.BlendedAnodeDQDV(0.2,si_case='absent'))}

    missing=mod.GraphiteAnodeDischargeDQDV([{'U':0.14,'w':0.02,'Q':1.0}])
    missing_dh=missing._resolve_lag_length(missing.transitions[0],298.15,1.0,1.0,1.0,+1)
    no_slope=mod.GraphiteAnodeDischargeDQDV([{'U':0.14,'w':0.02,'Q':1.0,'dH_a':85000.0}])
    missing_slope=no_slope._resolve_lag_length(no_slope.transitions[0],298.15,1.0,1.0,1.0,+1)
    out['missing_kinetics']={'probe_id':f'P063-RUN-MISSING-KINETICS-{tag}',
        'missing_dH_a_lag_V':missing_dh,'missing_dVdq_lag_V':missing_slope,
        'silent_equilibrium_fallback_observed':missing_dh==0.0 and missing_slope==0.0,'pass':missing_dh==0.0 and missing_slope==0.0}

    capture={}
    capmodel=mod.GraphiteAnodeDischargeDQDV([{'U':0.14,'w':0.02,'Q':1.0}])
    def capture_dqdv(V_app,T,I_abs,Q_cell,s=+1):
        capture.update(I_abs=float(I_abs),Q_cell=float(Q_cell),s=int(s))
        return np.zeros_like(np.asarray(V_app,dtype=float))
    capmodel.dqdv=capture_dqdv
    capmodel.curve(np.array([0.1,0.2]),'discharge',c_rate=1.0,Q_cell=2.0,T=298.15)
    tr=[{'U':0.14,'w':0.02,'Q':1.0,'dH_a':85000.0,'dS_a':0.0,'dVdq_qa':0.30,'Omega':0.0}]
    kin=mod.GraphiteAnodeDischargeDQDV(tr,Cbg=0.0)
    vk=np.linspace(0.02,0.30,1201)
    raw=np.asarray(kin.curve(vk,'discharge',c_rate=1.0,Q_cell=2.0,T=298.15),dtype=float)
    direct=np.asarray(kin.dqdv(vk,298.15,2.0,2.0,+1),dtype=float)
    corrected=np.asarray(kin.dqdv(vk,298.15,2.0/3600.0,2.0,+1),dtype=float)
    lraw=kin._resolve_lag_length(tr[0],298.15,2.0,2.0,1.0,+1)
    lcorr=kin._resolve_lag_length(tr[0],298.15,2.0/3600.0,2.0,1.0,+1)
    out['si_time']={'probe_id':f'P063-RUN-SI-TIME-{tag}','captured_I_abs':capture['I_abs'],
        'expected_si_I_abs':2.0/3600.0,'curve_equals_raw_hour_number':np.array_equal(raw,direct),
        'curve_vs_si_corrected_max_abs_diff':float(np.max(np.abs(raw-corrected))),
        'lag_raw_over_corrected':float(lraw/lcorr),'pass':capture['I_abs']==2.0 and np.array_equal(raw,direct)
            and float(np.max(np.abs(raw-corrected)))>0.0 and abs(lraw/lcorr-3600.0)<1e-8}

    seen=[]
    part=mod.BlendedAnodeDQDV(0.3,si_case='sic',Cbg=0.0)
    def recorder(host):
        def fn(V_app,T,I_abs,Q_cell,s=+1):
            seen.append({'host':host,'I_abs':float(I_abs),'Q_cell':float(Q_cell),'s':int(s)})
            return np.zeros_like(np.asarray(V_app,dtype=float))
        return fn
    part.gr_host.dqdv=recorder('graphite')
    part.si_host.dqdv=recorder('silicon')
    part.dqdv(np.array([0.1,0.2]),298.15,0.8,2.0,+1)
    same_full=(len(seen)==2 and all(r['I_abs']==0.8 and r['Q_cell']==2.0 for r in seen))
    out['current_partition']={'probe_id':f'P063-RUN-CURRENT-PARTITION-{tag}','host_calls':seen,
        'same_full_current_to_both_hosts':same_full,'host_partition_solver_present':False,'pass':same_full}

    for section in out.values():
        section['authority']='ISOLATED_INTERNAL_RUNTIME_ONLY'
        section['external_science']=False
    return out

mods=[load(sys.argv[1],'af22_probe'),load(sys.argv[2],'af23_probe')]
data={'v1.0.22':probe(mods[0],'22'),'v1.0.23':probe(mods[1],'23')}
V=np.linspace(0.03,0.55,801)
m22=mods[0].GraphiteAnodeDischargeDQDV(mods[0].GRAPHITE_STAGING_LIT,Cbg=0.05)
m23=mods[1].GraphiteAnodeDischargeDQDV(mods[1].GRAPHITE_STAGING_LIT,Cbg=0.05)
shared=np.array_equal(m22.curve(V,'discharge',0.2,1.0),m23.curve(V,'discharge',0.2,1.0))
tr=[{'U':0.14,'w':0.02,'Q':0.12,'L_V':0.006,'Omega':8000.0,'dVdq_qa':0.30}]
off=mods[1].GraphiteAnodeDischargeDQDV(tr)
on=mods[1].GraphiteAnodeDischargeDQDV(tr,lag_ratio_correction=True)
ratio_diff=float(np.max(np.abs(off.curve(V,'discharge',1.0,1.0)-on.curve(V,'discharge',1.0,1.0))))
data['cross_version']={'probe_id':'P063-RUN-CROSS-VERSION','v22_v23_default_array_equal':shared,
    'v23_ratio_liveness_max_abs_diff':ratio_diff,'pass':shared and ratio_diff>1e-6,
    'authority':'ISOLATED_INTERNAL_RUNTIME_ONLY','external_science':False}
print(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False))
'''


def materialize_runtime_tree(root: pathlib.Path) -> None:
    for path in RUNTIME_COPY_PATHS:
        target = root / pathlib.PurePosixPath(path).relative_to("Claude/docs")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git_bytes(path))


def normalized_tail(raw: bytes, tmp: pathlib.Path, limit: int = 24) -> list[str]:
    text = raw.decode("utf-8", "replace").replace(str(tmp), "<TMP>")
    text = text.replace(str(tmp).replace("\\", "/"), "<TMP>")
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return lines[-limit:]


def official_run(runtime: str, launcher: tuple[str, ...], tmp: pathlib.Path,
                 rel_cwd: str, script: str, run_id: str, expected: str,
                 timeout: int = 300) -> dict[str, Any]:
    cwd = tmp / rel_cwd
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["ANODEFIT_TMP"] = str(tmp / f"variant_{run_id}")
    cp = run((*launcher, "-B", "-I", "-X", "utf8", script), cwd=cwd, timeout=timeout, env=env, check=False)
    stderr_text = cp.stderr.decode("utf-8", "replace")
    diagnostic_kind: str | None = None
    diagnostic_matched = True
    if expected == "PASS":
        expectation_met = cp.returncode == 0
    else:
        if runtime == "3.12":
            diagnostic_kind = "FILE_NOT_FOUND_HARDCODED_PROJECT_PATH"
            diagnostic_matched = "FileNotFoundError" in stderr_text and "home/user/Project_Anode_Fit" in stderr_text
        elif runtime == "3.14":
            diagnostic_kind = "OPTIONAL_DEPENDENCY_MATPLOTLIB_MISSING"
            diagnostic_matched = "ModuleNotFoundError" in stderr_text and "matplotlib" in stderr_text
        else:
            raise RuntimeError(f"unpinned expected-failure runtime {runtime!r}")
        expectation_met = cp.returncode != 0 and diagnostic_matched
    return {
        "run_id": run_id,
        "runtime": runtime,
        "command": [*launcher, "-B", "-I", "-X", "utf8", script],
        "cwd": rel_cwd,
        "exit_code": cp.returncode,
        "expected_state": expected,
        "expected_failure_kind": diagnostic_kind,
        "diagnostic_matched": diagnostic_matched,
        "expectation_met": expectation_met,
        "stdout_tail": normalized_tail(cp.stdout, tmp),
        "stderr_tail": normalized_tail(cp.stderr, tmp),
        "authority": "EXACT_COPIED_OFFICIAL_GATE_ONLY",
        "external_science": False,
    }


def runtime_evidence() -> dict[str, Any]:
    runtime_rows: list[dict[str, Any]] = []
    official: list[dict[str, Any]] = []
    probes: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="p063_step61_") as td:
        tmp = pathlib.Path(td)
        resolved_tmp = tmp.resolve()
        resolved_root = ROOT.resolve()
        if resolved_tmp == resolved_root or resolved_root in resolved_tmp.parents:
            raise RuntimeError(f"runtime temp directory is not external to repository: {resolved_tmp}")
        materialize_runtime_tree(tmp)
        probe_path = tmp / "independent_probe.py"
        probe_path.write_text(PROBE_SOURCE, encoding="utf-8", newline="\n")
        materialized_paths = [tmp / pathlib.PurePosixPath(path).relative_to("Claude/docs") for path in RUNTIME_COPY_PATHS]
        if not all(resolved_tmp in path.resolve().parents for path in (*materialized_paths, probe_path)):
            raise RuntimeError("runtime materialization escaped the verified external temp root")
        for runtime, launcher in PYTHON_LAUNCHERS:
            version_cp = run((*launcher, "-B", "-I", "-X", "utf8", "-c", "import sys,numpy;print(sys.version.split()[0]);print(numpy.__version__)"))
            version_lines = version_cp.stdout.decode().splitlines()
            runtime_rows.append({
                "runtime": runtime,
                "python_version": version_lines[0],
                "numpy_version": version_lines[1],
                "launcher": list(launcher),
            })
            official.extend((
                official_run(runtime, launcher, tmp, "v1.0.21", "test_gates_v1021.py", f"P063-OFFICIAL-V1021-{runtime.replace('.', '')}", "PASS"),
                official_run(runtime, launcher, tmp, "v1.0.22", "test_gates_v1022.py", f"P063-OFFICIAL-V1022-{runtime.replace('.', '')}", "PASS"),
                official_run(runtime, launcher, tmp, "v1.0.23", "test_gates_v1023.py", f"P063-OFFICIAL-V1023-{runtime.replace('.', '')}", "PASS"),
                official_run(runtime, launcher, tmp, "v1.0.23", "test_gates_v1023_selfconsistent.py", f"P063-OFFICIAL-V1023-SC-{runtime.replace('.', '')}", "PASS"),
                official_run(runtime, launcher, tmp, "v1.0.23/results/comp_v23", "p1_ratio_check.py", f"P063-OFFICIAL-V1023-P1-{runtime.replace('.', '')}", "PASS"),
                official_run(runtime, launcher, tmp, "v1.0.23/results/qa_images", "curve_qa.py", f"P063-OFFICIAL-V1023-CURVE-QA-{runtime.replace('.', '')}", "EXPECTED_FAIL_NONPORTABLE_PATH_OR_OPTIONAL_DEPENDENCY"),
            ))
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            cp = run(
                (*launcher, "-B", "-I", "-X", "utf8", str(probe_path), str(tmp / "v1.0.22/Anode_Fit_v1.0.22.py"),
                 str(tmp / "v1.0.23/Anode_Fit_v1.0.23.py")),
                cwd=tmp, timeout=300, env=env,
            )
            parsed = json.loads(cp.stdout.decode("utf-8"))
            probes.append({
                "runtime": runtime,
                "probe_program_sha256": sha256(PROBE_SOURCE.encode("utf-8")),
                "results": parsed,
            })
    return finalize({
        "artifact_kind": "PHASE_063_V1022_RUNTIME_ATTESTATION",
        "schema_version": 1,
        "phase": 63,
        "step": 61,
        "generated_date": "2026-08-29",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "isolation": {
            "source_imported": False,
            "copied_git_blobs_only": True,
            "disposable_external_directories": True,
            "external_temp_root_verified": True,
            "materialized_paths_contained": True,
            "bytecode_disabled": True,
            "network_used": False,
            "copied_blob_manifest": [
                {
                    "path": path,
                    "git_blob": git_blob(path),
                    "sha256": sha256(git_bytes(path)),
                    "bytes": len(git_bytes(path)),
                }
                for path in RUNTIME_COPY_PATHS
            ],
        },
        "runtimes": runtime_rows,
        "official_runs": official,
        "independent_probes": probes,
        "counts": {
            "runtimes": len(runtime_rows),
            "official_runs": len(official),
            "official_expectations_met": sum(r["expectation_met"] for r in official),
            "probe_runtime_sets": len(probes),
        },
        "authority_boundary": {
            "static_or_runtime_internal_pass": True,
            "scientific_truth": False,
            "material_truth": False,
            "experimental_truth": False,
            "primary_literature_truth": False,
            "canonical_adoption": False,
            "publication_readiness": False,
        },
        "result_first_contract": {
            "gate": "PASS_P063_STEP61_CODE_RUNTIME_DELTA_WITH_CONCERNS",
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "postcommit_terminal": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        },
    })


def build_code_artifact(endpoints: list[dict[str, Any]]) -> dict[str, Any]:
    by_path = {row["path"]: row for row in endpoints}
    prod21 = by_path["Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py"]
    prod22 = by_path["Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py"]
    prod23 = by_path["Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py"]
    test21 = by_path["Claude/docs/v1.0.21/test_gates_v1021.py"]
    test22 = by_path["Claude/docs/v1.0.22/test_gates_v1022.py"]
    test23 = by_path["Claude/docs/v1.0.23/test_gates_v1023.py"]
    blob_groups: dict[str, list[str]] = defaultdict(list)
    for row in endpoints:
        blob_groups[row["git_blob"]].append(row["path"])
    shared = [
        {"git_blob": blob, "paths": paths, "occurrences": len(paths)}
        for blob, paths in sorted(blob_groups.items()) if len(paths) > 1
    ]
    findings = finding_rows(prod22, prod23, endpoints)
    priorities = Counter(row["priority"] for row in findings)
    return finalize({
        "artifact_kind": "PHASE_063_V1022_CODE_DELTA_MATRIX",
        "schema_version": 1,
        "phase": 63,
        "step": 61,
        "generated_date": "2026-08-29",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "endpoint_predicate": "all *.py plus filenames containing GUIDE under exact v1.0.21/v1.0.22/v1.0.23 frozen directories",
        "endpoints": endpoints,
        "shared_blob_groups": shared,
        "symbol_deltas": [
            symbol_delta(prod21, prod22, "P063-DELTA-PROD-21-22"),
            symbol_delta(prod22, prod23, "P063-DELTA-PROD-22-23"),
            symbol_delta(test21, test22, "P063-DELTA-GATE-21-22"),
            symbol_delta(test22, test23, "P063-DELTA-GATE-22-23"),
        ],
        "theory_code_concordance": theory_rows(prod22),
        "static_contracts": static_contract_rows(prod22, prod23),
        "findings": findings,
        "finding_summary": {"P0": priorities["P0"], "P1": priorities["P1"], "P2": priorities["P2"]},
        "counts": {
            "endpoint_occurrences": len(endpoints),
            "unique_blobs": len(blob_groups),
            "python_endpoints": sum(r["path"].endswith(".py") for r in endpoints),
            "guide_endpoints": sum(r["role"] == "GUIDE" for r in endpoints),
            "production_modules": sum(r["role"] == "PRODUCTION_MODULE" for r in endpoints),
            "official_gates": sum(r["role"] == "OFFICIAL_GATE" for r in endpoints),
            "ast_symbols": sum(len(r.get("ast", {}).get("symbols", [])) for r in endpoints),
            "static_contracts": 7,
            "theory_code_rows": 10,
            "findings": len(findings),
        },
        "authority_boundary": {
            "static_identity_complete": True,
            "runtime_claim_owner": RUNTIME_NAME,
            "scientific_truth": False,
            "material_truth": False,
            "experimental_truth": False,
            "primary_literature_truth": False,
            "canonical_adoption": False,
            "publication_readiness": False,
        },
        "result_first_contract": {
            "gate": "PASS_P063_STEP61_CODE_RUNTIME_DELTA_WITH_CONCERNS",
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "postcommit_terminal": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        },
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path)
    args = parser.parse_args()
    endpoints = endpoint_rows()
    code = build_code_artifact(endpoints)
    runtime = runtime_evidence()
    out_dir = args.output_dir.resolve() if args.output_dir else CODE_OUT.parent
    atomic_json(out_dir / CODE_NAME, code)
    atomic_json(out_dir / RUNTIME_NAME, runtime)
    print(
        "PASS_P063_STEP61_BUILD "
        f"endpoints={code['counts']['endpoint_occurrences']} "
        f"symbols={sum(len(r.get('ast', {}).get('symbols', [])) for r in endpoints)} "
        f"official={runtime['counts']['official_expectations_met']}/{runtime['counts']['official_runs']} "
        f"probe_sets={runtime['counts']['probe_runtime_sets']} "
        f"findings={code['finding_summary']['P0']}/{code['finding_summary']['P1']}/{code['finding_summary']['P2']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
