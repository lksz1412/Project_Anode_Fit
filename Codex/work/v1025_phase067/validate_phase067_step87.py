#!/usr/bin/env python3
"""Validate Phase 067 Step 87 unit/numerical evidence and persistence."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = "origin/codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
DATE = "2026-09-02"
SUBJECT = "audit(phase067): verify units numerical invariants"
GATE = "PASS_P067_STEP87_UNIT_NUMERICAL"
PERSISTENCE = "PASS_P067_STEP87_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "c97ad94c35e8f4db3db5c207cf099a647cb363fca9d7816221e136c22bf4621f"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "092565c8aac4c2be215fd786af00d283a85b1f9e5fb9b0166b3dcc179f8628b0"

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STATE_FLOW_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
MATRIX_PATH = "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json"
BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step87.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step87.py"
RESULT_PATH = "Codex/results/PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RESULT_PATH,
               PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if i < 4 else "M") for i, path in enumerate(FINAL_PATHS)}
CONTROL_SHA256 = {
    RESULT_PATH: "5553bf37605bf671e0700bec47aecd259699403c40c014fd9defad0ca1a86b3f",
    PARENT_LEDGER: "212b3db9a7ec3c58f3b5f2845e29dc35ee559b0d710c62259770fe614a9d6faf",
    CANONICAL_LEDGER: "a968fe874fd02510ba1aa261d7fd54f981c1f1530e810527e663774c7fd6d501",
    HANDOVER: "3742c2ffbc9d677863ccddde94d7d88800f2743d9ecd61bf986f7da83ac2b774",
}
INVENTORY_RAW_SHA256 = "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63"
INVENTORY_SEMANTIC_SHA256 = "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"
ATTESTATION_RAW_SHA256 = "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174"
ATTESTATION_SEMANTIC_SHA256 = "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"
STATE_FLOW_RAW_SHA256 = "0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8"
STATE_FLOW_SEMANTIC_SHA256 = "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44"
PROBE_RECORDS_SHA256 = "a5022702d40cabd12b39a60d834868361c68de01c3def8b54357827a9342d503"
RELEASES = [
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14",
    "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2",
    "v1.0.19", "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23",
    "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
]


class ValidationError(RuntimeError):
    pass


def require(ok: bool, diagnostic: str, detail: str = "") -> None:
    if not ok:
        raise ValidationError(diagnostic + ((":" + detail) if detail else ""))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    clone = copy.deepcopy(value)
    clone.pop("semantic_sha256", None)
    return sha(canonical(clone))


def predecessor_semantic(value: dict[str, Any]) -> str:
    clone = copy.deepcopy(value)
    clone["semantic_sha256"] = ""
    return sha((json.dumps(clone, ensure_ascii=False, indent=2, sort_keys=True,
                           separators=(",", ": "), allow_nan=False) + "\n").encode("utf-8"))


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(typed_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def strict_load(raw: bytes, label: str, generated: bool = True) -> tuple[dict[str, Any], int, int]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, "E_JSON_DUPLICATE", label + ":" + key)
            out[key] = value
        return out
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValidationError("E_JSON_PARSE:" + label) from exc
    require(isinstance(value, dict), "E_JSON_ROOT", label)
    nodes = 0
    max_depth = 0
    stack = [(value, 0)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        if isinstance(current, dict):
            stack.extend((item, depth + 1) for item in current.values())
        elif isinstance(current, list):
            stack.extend((item, depth + 1) for item in current)
        elif isinstance(current, float):
            require(math.isfinite(current), "E_JSON_NONFINITE", label)
    if generated:
        require(raw == canonical(value), "E_JSON_CANONICAL", label)
        require(value.get("semantic_sha256") == semantic(value), "E_JSON_SEMANTIC", label)
    return value, nodes, max_depth


def is_oid(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value))


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    fixed = {
        ("rev-parse", "HEAD"), ("rev-parse", "--abbrev-ref", "HEAD"),
        ("rev-parse", "--abbrev-ref", "@{upstream}"), ("rev-parse", UPSTREAM),
        ("rev-parse", f"refs/remotes/{UPSTREAM}"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        ("show-ref", "--verify", "--hash", "refs/heads/main"),
        ("ls-remote", "--get-url", "origin"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("ls-remote", "--heads", "origin", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        ("ls-remote", "--heads", "origin", "refs/heads/main"),
        ("status", "--porcelain=v1", "--untracked-files=all"), ("status", "--porcelain"),
        ("ls-files", "-s"), ("ls-files", "--others", "--exclude-standard"),
        ("diff", "--name-only"), ("diff", "--cached", "--check"),
        ("diff", "--cached", "--name-status", "--no-renames", "HEAD"),
        ("diff", "--name-only", PROTECTED_TIP, "--", "Claude"),
    }
    if args in fixed:
        return True
    if len(args) == 2 and args[0] == "show" and ":" in args[1]:
        revision, path = args[1].split(":", 1)
        return ((revision in {EXPECTED_PARENT, BASELINE, ""} or is_oid(revision))
                and (path in {INVENTORY_PATH, ATTESTATION_PATH, STATE_FLOW_PATH, *FINAL_PATHS}
                     or path.startswith("Claude/docs/")))
    if len(args) == 3 and args[:2] == ("cat-file", "blob"):
        return is_oid(args[2])
    if len(args) == 4 and args[:2] == ("show", "-s") and args[2] in {"--format=%P", "--format=%s"}:
        return is_oid(args[3])
    if len(args) == 2 and args[0] == "rev-parse" and args[1].endswith("^"):
        return is_oid(args[1][:-1])
    if len(args) == 8 and args[:5] == ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r"):
        return is_oid(args[5][:-1]) and args[5].endswith("^") and is_oid(args[6]) and args[7] == "--"
    return False


def git(args: tuple[str, ...], allow_failure: bool = False) -> bytes:
    require(git_argv_allowed(args), "E_GIT_ARGV", repr(args))
    proc = subprocess.run(("git", *args), cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    require(allow_failure or proc.returncode == 0, "E_GIT_EXIT", repr(args))
    return proc.stdout


def gtext(args: tuple[str, ...], allow_failure: bool = False) -> str:
    return git(args, allow_failure).decode("utf-8").rstrip("\r\n")


def commit_bytes(path: str) -> bytes:
    return git(("show", f"{EXPECTED_PARENT}:{path}"))


def blob(oid: str) -> bytes:
    return git(("cat-file", "blob", oid))


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
            if node.lineno <= selected.lineno and node.end_lineno >= selected.end_lineno:
                found.append((node.end_lineno - node.lineno, ".".join(nested)))
        for child in ast.iter_child_nodes(node):
            walk(child, nested)
    walk(tree, [])
    return min(found)[1] if found else "<module>"


def anchor(tree: ast.Module, source: str, node: ast.AST) -> dict[str, Any]:
    lines = source.splitlines()
    start, end = node.lineno, node.end_lineno
    text = "\n".join(lines[start - 1:end]) + "\n"
    return {"qualified_owner": qualified_owner(tree, node), "ast_kind": type(node).__name__,
            "start_line": start, "end_line": end, "source_sha256": sha(text.encode()),
            "node_sha256": sha(canonical(stable_ast(node))), "expression": ast.unparse(node)}


def first(tree: ast.Module, predicate: Callable[[ast.AST, str], bool], diagnostic: str) -> ast.AST:
    rows = []
    for node in ast.walk(tree):
        try:
            expression = ast.unparse(node)
        except (TypeError, ValueError):
            expression = ""
        if predicate(node, expression):
            rows.append(node)
    require(bool(rows), diagnostic)
    return min(rows, key=lambda node: (node.lineno, node.col_offset))


def independent_features(oid: str) -> dict[str, Any]:
    raw = blob(oid)
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    predicates: dict[str, Callable[[ast.AST, str], bool]] = {
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
    anchors = {name: anchor(tree, source, first(tree, predicate, "E_FEATURE_" + name))
               for name, predicate in predicates.items()}
    optionals: dict[str, Callable[[ast.AST, str], bool]] = {
        "MASS_TO_CAPACITY_FRACTION": lambda n, e: isinstance(n, ast.Assign) and "f_Si" in e and "q_gr" in e and "num /" in e,
        "COMPONENT_CAPACITY_SCALE": lambda n, e: isinstance(n, ast.Assign) and "si_scale" in e and "Q_gr0 / Q_si0" in e,
    }
    for name, predicate in optionals.items():
        candidates = []
        for node in ast.walk(tree):
            try:
                expression = ast.unparse(node)
            except (TypeError, ValueError):
                expression = ""
            if predicate(node, expression):
                candidates.append(node)
        anchors[name] = anchor(tree, source, min(candidates, key=lambda n: (n.lineno, n.col_offset))) if candidates else None
    comments = [line.strip() for line in source.splitlines()
                if "3600" in line and line.lstrip().startswith("#")]
    divide = any(isinstance(node, (ast.BinOp, ast.AugAssign)) and "/ 3600" in ast.unparse(node)
                 for node in ast.walk(tree))
    return {"blob_oid": oid, "raw_sha256": sha(raw),
            "lf_sha256": sha(lf_bytes(raw)),
            "lf_normalization": "CRLF_AND_LONE_CR_TO_LF",
            "physical_lines": len(source.splitlines()),
            "encoding": "utf-8", "ast_parse": "PASS", "anchors": anchors,
            "comment_3600_sha256": sha(("\n".join(comments) + ("\n" if comments else "")).encode()),
            "comment_3600_count": len(comments), "executable_divide_3600": divide}


def input_documents() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    result = []
    for path, raw_pin, semantic_pin, modern in (
        (INVENTORY_PATH, INVENTORY_RAW_SHA256, INVENTORY_SEMANTIC_SHA256, False),
        (ATTESTATION_PATH, ATTESTATION_RAW_SHA256, ATTESTATION_SEMANTIC_SHA256, False),
        (STATE_FLOW_PATH, STATE_FLOW_RAW_SHA256, STATE_FLOW_SEMANTIC_SHA256, True),
    ):
        raw = commit_bytes(path)
        require(sha(raw) == raw_pin, "E_INPUT_RAW", path)
        value, _, _ = strict_load(raw, path, False)
        observed = semantic(value) if modern else predecessor_semantic(value)
        require(observed == semantic_pin, "E_INPUT_SEMANTIC", path)
        result.append(value)
    return result[0], result[1], result[2]


TOP_KEYS = {"schema_version", "artifact", "phase", "step", "generated_date", "baseline_commit",
            "expected_parent", "branch", "expected_subject", "gate", "persistence_terminal",
            "precommit_status", "containing_commit", "result_first", "json_output_last", "inputs",
            "universe", "source_occurrence_records", "source_feature_records", "probe_records",
            "tolerance_provenance_records", "limitation_records", "coverage", "authority",
            "validation", "semantic_sha256"}
SOURCE_KEYS = {"ordinal", "manifest_entry_index", "release", "path", "role", "blob_oid",
               "blob_ordinal", "git_mode", "size_bytes", "physical_lines"}
FEATURE_KEYS = {"blob_oid", "raw_sha256", "lf_sha256", "lf_normalization", "physical_lines",
                "size_bytes", "git_mode", "encoding", "ast_parse", "anchors",
                "comment_3600_sha256", "comment_3600_count", "executable_divide_3600",
                "blob_ordinal", "occurrence_refs"}
PROBE_KEYS = {"row_id", "family", "dimension", "basis", "sign_convention", "formula", "inputs",
              "expected", "observed", "error", "tolerance", "disposition", "source_feature_ids",
              "authority", "note"}
TOLERANCE_KEYS = {"provenance_id", "probe_id", "relation", "method_scope", "blob_oid",
                  "blob_ordinal", "git_mode", "raw_sha256", "lf_sha256", "lf_normalization",
                  "encoding", "size_bytes", "physical_lines", "occurrence_refs", "constants",
                  "gate_anchor", "comparison"}
LIMITATION_KEYS = {"limitation_id", "status", "excluded_conditions", "source_feature_ids",
                   "universal_dqdv_zero_equals_equilibrium", "authority"}


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v) for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return value is None or type(value) in {bool, int, str}


_EXPECTED_SOURCE_CACHE: tuple[list[dict[str, Any]], list[dict[str, Any]]] | None = None


def expected_sources(inventory: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    global _EXPECTED_SOURCE_CACHE
    if _EXPECTED_SOURCE_CACHE is not None:
        return _EXPECTED_SOURCE_CACHE
    occurrences = sorted([row for row in inventory["occurrence_records"] if row["role"] == "code"],
                         key=lambda row: RELEASES.index(row["release"]))
    sources = [{key: row[key] for key in SOURCE_KEYS} for row in occurrences]
    features = []
    for oid in sorted({row["blob_oid"] for row in sources}):
        item = independent_features(oid)
        refs = [row for row in sources if row["blob_oid"] == oid]
        item["blob_ordinal"] = refs[0]["blob_ordinal"]
        item["git_mode"] = refs[0]["git_mode"]
        item["size_bytes"] = refs[0]["size_bytes"]
        item["occurrence_refs"] = [{key: row[key] for key in (
            "ordinal", "manifest_entry_index", "release", "path")} for row in refs]
        features.append(item)
    _EXPECTED_SOURCE_CACHE = (sources, features)
    return _EXPECTED_SOURCE_CACHE


_EXPECTED_TOLERANCE_CACHE: list[dict[str, Any]] | None = None


def expected_tolerance_provenance(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    global _EXPECTED_TOLERANCE_CACHE
    if _EXPECTED_TOLERANCE_CACHE is not None:
        return _EXPECTED_TOLERANCE_CACHE
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
    _EXPECTED_TOLERANCE_CACHE = records
    return _EXPECTED_TOLERANCE_CACHE


_ORACLE_CACHE: dict[str, Any] | None = None


def expected_probe_observations() -> dict[str, Any]:
    global _ORACLE_CACHE
    if _ORACLE_CACHE is not None:
        return _ORACLE_CACHE
    m, q_si, q_gr = 0.3, 3117.0, 372.0
    fraction = (m * q_si) / (m * q_si + (1.0 - m) * q_gr)
    temperature, delta_t, d_h, d_s, n_value, x_value = 298.15, 3.0, -30000.0, -20.0, 1.0, 0.25
    gas, faraday = 8.314, 96485.0
    logit = math.log(x_value / (1.0 - x_value))
    primitive = lambda t: (-d_h + t*d_s)/faraday + n_value*gas*t*logit/faraday
    derivative = (primitive(temperature + delta_t) - primitive(temperature - delta_t))/(2.0*delta_t)
    lq_t, lq_i, lq_q, lq_dh, lq_ds, lq_x, lq_a = 298.15, 0.2, 1.0, 44000.0, 0.0, 0.5, 10000.0
    lq_r, planck, boltzmann = 8.314, 6.62607015e-34, 1.380649e-23
    def lq(rate: float, enthalpy: float) -> float:
        attempt = rate * planck / boltzmann
        return math.exp(math.log(attempt/lq_t)
                        - math.log(1.0+math.exp(-lq_a/(lq_r*lq_t)))
                        + (enthalpy-lq_t*lq_ds)/(lq_r*lq_t)
                        - lq_x*lq_a/(lq_r*lq_t))
    lq_raw_h = lq(lq_i/lq_q, lq_dh)
    lq_raw_s = lq((lq_i/lq_q)/3600.0, lq_dh)
    lq_shift = lq_r*lq_t*math.log(3600.0)
    lq_observed = {"raw_hour": lq_raw_h, "raw_second": lq_raw_s,
                   "hour_to_second_ratio": lq_raw_h/lq_raw_s,
                   "R_T_ln_3600_J_mol": lq_shift,
                   "compensated_second": lq((lq_i/lq_q)/3600.0, lq_dh+lq_shift)}
    zero_t, zero_u, zero_q, zero_n, zero_bg = 300.0, 3.5, 2.0, 1.0, 0.1
    zero_width = zero_n*8.314*zero_t/96485.0
    zero_observed = {}
    for label, direction in (("s_plus", 1), ("s_minus", -1)):
        values = []
        for voltage in [3.3, 3.5, 3.7]:
            sig = 1.0/(1.0+math.exp(-direction*(voltage-zero_u)/zero_width))
            values.append(zero_q*sig*(1.0-sig)/zero_width+zero_bg)
        zero_observed[label] = values
    center, width = 3.5, 0.08
    lo, hi, intervals = center - 20.0*width, center + 20.0*width, 400000
    def derivative_v(v: float) -> float:
        xi = 1.0 / (1.0 + math.exp(-(v-center)/width))
        return xi*(1.0-xi)/width
    spacing = (hi-lo)/intervals
    area = derivative_v(lo) + derivative_v(hi)
    area += 4.0*sum(derivative_v(lo+spacing*i) for i in range(1, intervals, 2))
    area += 2.0*sum(derivative_v(lo+spacing*i) for i in range(2, intervals, 2))
    area *= spacing/3.0
    _ORACLE_CACHE = {
        "N01": 2.0 / 3600.0, "N02": lq_observed, "N03": 3.68, "N04": 3.72,
        "N05": zero_observed, "N06": 9000.0, "N07": 900.0,
        "N08": 10.0 / 96485.0, "N09": 10.0 / 96485.33212,
        "N10": -2.0 * 300.0 * (10.0 / 96485.0),
        "N11": -2.0 * 300.0 * (-10.0 / 96485.0),
        "N12": fraction, "N13": {"Q_total": m*q_si+(1-m)*q_gr, "f_Si": fraction},
        "N14": 2.0 * (3.7 - 3.6),
        "N15": area,
        "N16": derivative,
    }
    return _ORACLE_CACHE


def expected_special_expectations() -> dict[str, Any]:
    t, rate, d_h, d_s, x, affinity = 298.15, 0.2, 44000.0, 0.0, 0.5, 10000.0
    gas, planck, boltzmann = 8.314, 6.62607015e-34, 1.380649e-23
    def product(rate_value: float, enthalpy: float) -> float:
        return ((rate_value*planck/(boltzmann*t))
                / (1.0+math.exp(-affinity/(gas*t)))
                * math.exp((enthalpy-t*d_s-x*affinity)/(gas*t)))
    shift = gas*t*math.log(3600.0)
    lq_expected = {"raw_hour": product(rate, d_h), "raw_second": product(rate/3600.0, d_h),
                   "hour_to_second_ratio": 3600.0, "R_T_ln_3600_J_mol": shift,
                   "compensated_second": product(rate/3600.0, d_h+shift)}
    zero_width = 8.314*300.0/96485.0
    zero_vector = [2.0/(4.0*zero_width*math.cosh((v-3.5)/(2.0*zero_width))**2)+0.1
                   for v in [3.3, 3.5, 3.7]]
    zero_expected = {"s_plus": zero_vector, "s_minus": list(zero_vector)}
    lo, hi = 3.5-20.0*0.08, 3.5+20.0*0.08
    area_expected = (1.0/(1.0+math.exp(-(hi-3.5)/0.08))
                     - 1.0/(1.0+math.exp(-(lo-3.5)/0.08)))
    return {"N02": lq_expected, "N05": zero_expected, "N15": area_expected}


def artifact_errors(matrix: dict[str, Any], inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    def check(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)
    probes_by_id = {row.get("row_id"): row for row in matrix.get("probe_records", [])
                    if isinstance(row, dict)}
    check(type(probes_by_id.get("N02", {}).get("observed")) is dict,
          "N02_LQ_BASIS_UNDERBOUND")
    check(type(probes_by_id.get("N05", {}).get("observed")) is dict
          and set(probes_by_id["N05"]["observed"]) == {"s_plus", "s_minus"},
          "N05_ZERO_CURRENT_SCOPE_UNDERBOUND")
    check(type(probes_by_id.get("N15", {}).get("observed")) is float
          and probes_by_id["N15"]["observed"] > 0.0,
          "N15_LOGISTIC_SIGN_WRONG")
    check(type(matrix.get("tolerance_provenance_records")) is list,
          "TOLERANCE_PROVENANCE_MISSING")
    check(all(type(row) is dict and type(row.get("lf_sha256")) is str
              for row in matrix.get("source_feature_records", [])),
          "SOURCE_LF_SHA_MISSING")
    check(set(matrix) == TOP_KEYS, "TOP_KEYS")
    exact_metadata = {"schema_version": "phase067-step87-unit-numerical-v1", "artifact": MATRIX_PATH,
                      "phase": 67, "step": 87, "generated_date": DATE, "baseline_commit": BASELINE,
                      "expected_parent": EXPECTED_PARENT, "branch": BRANCH, "expected_subject": SUBJECT,
                      "gate": GATE, "persistence_terminal": PERSISTENCE,
                      "precommit_status": "PASS_PENDING_PERSISTENCE",
                      "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
                      "result_first": True, "json_output_last": True}
    check(all(key in matrix and typed_equal(matrix[key], value) for key, value in exact_metadata.items()), "METADATA")
    expected_inputs = {
        "inventory": {"path": INVENTORY_PATH, "raw_sha256": INVENTORY_RAW_SHA256,
                      "semantic_sha256": INVENTORY_SEMANTIC_SHA256},
        "attestation": {"path": ATTESTATION_PATH, "raw_sha256": ATTESTATION_RAW_SHA256,
                        "semantic_sha256": ATTESTATION_SEMANTIC_SHA256},
        "state_flow": {"path": STATE_FLOW_PATH, "raw_sha256": STATE_FLOW_RAW_SHA256,
                       "semantic_sha256": STATE_FLOW_SEMANTIC_SHA256},
    }
    check(typed_equal(matrix.get("inputs"), expected_inputs), "INPUTS")
    check(typed_equal(matrix.get("universe"), {"code_occurrences": 20, "code_unique_blobs": 15,
                                               "probe_rows": 16, "release_count": 20}), "UNIVERSE")
    sources, features = expected_sources(inventory)
    check(isinstance(matrix.get("source_occurrence_records"), list)
          and all(type(row) is dict and set(row) == SOURCE_KEYS for row in matrix["source_occurrence_records"]),
          "SOURCE_SCHEMA")
    check(typed_equal(matrix.get("source_occurrence_records"), sources), "SOURCE_PROJECTION")
    check(isinstance(matrix.get("source_feature_records"), list)
          and all(type(row) is dict and set(row) == FEATURE_KEYS for row in matrix["source_feature_records"]),
          "FEATURE_SCHEMA")
    check(typed_equal(matrix.get("source_feature_records"), features), "FEATURE_PROJECTION")
    tolerance_records = expected_tolerance_provenance(inventory)
    check(isinstance(matrix.get("tolerance_provenance_records"), list)
          and all(type(row) is dict and set(row) == TOLERANCE_KEYS
                  for row in matrix["tolerance_provenance_records"]), "TOLERANCE_PROVENANCE_SCHEMA")
    check(typed_equal(matrix.get("tolerance_provenance_records"), tolerance_records),
          "TOLERANCE_PROVENANCE_PROJECTION")
    expected_limitations = [{
        "limitation_id": "L01_ZERO_CURRENT_NOT_UNIVERSAL",
        "status": "BOUNDED_NOT_GENERAL",
        "excluded_conditions": ["DIRECT_L_V_OVERRIDE", "HYSTERESIS_GAMMA_OR_OMEGA",
                                "REVERSED_DIRECTION_WITH_ALPHA_NE_1"],
        "source_feature_ids": ["L_V_OVERRIDE", "L_V_ZERO_CURRENT"],
        "universal_dqdv_zero_equals_equilibrium": False,
        "authority": "INTERNAL_SOFTWARE_NUMERICAL_ONLY",
    }]
    check(isinstance(matrix.get("limitation_records"), list)
          and all(type(row) is dict and set(row) == LIMITATION_KEYS
                  for row in matrix["limitation_records"]), "LIMITATION_SCHEMA")
    check(typed_equal(matrix.get("limitation_records"), expected_limitations), "LIMITATION_PROJECTION")
    probes = matrix.get("probe_records")
    check(isinstance(probes, list) and len(probes) == 16
          and all(type(row) is dict and set(row) == PROBE_KEYS for row in probes), "PROBE_SCHEMA")
    if isinstance(probes, list):
        check([row.get("row_id") for row in probes] == [f"N{i:02d}" for i in range(1, 17)], "PROBE_ORDER")
        try:
            check(sha(canonical(probes)) == PROBE_RECORDS_SHA256, "PROBE_PIN")
        except (TypeError, ValueError):
            check(False, "PROBE_PIN")
        check(finite_tree(probes), "PROBE_FINITE")
        oracle = expected_probe_observations()
        by_id = {row.get("row_id"): row for row in probes if isinstance(row, dict)}
        for rid, expected in oracle.items():
            check(rid in by_id and typed_equal(by_id[rid].get("observed"), expected), "ORACLE_" + rid)
        for rid, expected in expected_special_expectations().items():
            check(rid in by_id and typed_equal(by_id[rid].get("expected"), expected),
                  "EXPECTED_ORACLE_" + rid)
        check(by_id.get("N02", {}).get("inputs", {}).get("executable_seconds_correction") is False
              and by_id.get("N02", {}).get("basis") == "AMBIGUOUS_Ah_OR_C"
              and by_id.get("N02", {}).get("inputs", {}).get("basis_resolution") == "GROUND_NOT_FOUND"
              and [row.get("hypothesis") for row in
                   by_id.get("N02", {}).get("inputs", {}).get("basis_hypotheses", [])]
              == ["AH_COMMENT_PLACEHOLDER_ABSORPTION", "C_COMMENT_DIRECT_SI"]
              and all(row.get("selected") is False for row in
                      by_id.get("N02", {}).get("inputs", {}).get("basis_hypotheses", [])),
              "N02_BASIS_AUTHORITY")
        check(by_id.get("N05", {}).get("family") == "ZERO_CURRENT_CONDITIONAL",
              "N05_CONDITIONAL_SCOPE")
        for row in probes:
            if not isinstance(row, dict):
                continue
            check(type(row.get("error")) is float and row["error"] >= 0.0, "ERROR_TYPE")
            tolerance = row.get("tolerance")
            check(type(tolerance) is dict and set(tolerance) == {"kind", "absolute", "relative"}
                  and tolerance.get("kind") in {"EXACT", "APPROXIMATE"}
                  and type(tolerance.get("absolute")) is float and type(tolerance.get("relative")) is float,
                  "TOLERANCE_SCHEMA")
            check(row.get("authority") == "INTERNAL_SOFTWARE_NUMERICAL_ONLY", "ROW_AUTHORITY")
    expected_coverage = {"required_families": ["RATE_CONVERSION", "RATE_SOURCE_GAP", "CURRENT_SIGN",
        "ZERO_CURRENT_CONDITIONAL", "CAPACITY_CONVERSION", "ENERGY_HEAT_CONVERSION", "ENTROPY_COEFFICIENT",
        "REVERSIBLE_HEAT", "FRACTION_BASIS", "COMPONENT_TOTAL_CLOSURE", "IRREVERSIBLE_HEAT", "DQDV_AREA",
        "FINITE_DIFFERENCE_DERIVATIVE"], "source_anchor_occurrence_coverage": "20/20",
        "source_blob_feature_coverage": "15/15", "comment_only_3600_blob_count": 3,
        "executable_divide_3600_blob_count": 0, "blend_feature_blob_count": 5,
        "tolerance_provenance_blob_count": 6, "tolerance_provenance_record_count": 10,
        "zero_current_limitation_count": 1,
        "failed_tolerance_rows": 0}
    check(typed_equal(matrix.get("coverage"), expected_coverage), "COVERAGE")
    expected_authority = {"internal_software_consistency": True, "internal_numerical_consistency": True,
        "runtime_behavior": False, "external_scientific": False, "material_parameter": False,
        "experimental": False, "canonical": False, "publication": False,
        "open_unit_convention": "Q_cell_Ah_OR_C_AND_NO_EXECUTABLE_DIVIDE_BY_3600",
        "open_owner": "STEP88_IMPACT_AND_EXISTING_P066_OPEN_OWNERS"}
    check(typed_equal(matrix.get("authority"), expected_authority), "AUTHORITY")
    expected_validation = {"strict_json_inputs": True, "source_git_blob_bound": True,
        "release_order_exact": True, "typed_numeric_vectors": True, "nonfinite_count": 0,
        "duplicate_row_count": 0, "failed_tolerance_count": 0,
        "determinism_runs": 2, "determinism_matches": 2}
    check(typed_equal(matrix.get("validation"), expected_validation), "VALIDATION")
    check(matrix.get("semantic_sha256") == semantic(matrix), "SEMANTIC")
    return errors


def reseal(value: dict[str, Any]) -> None:
    value["semantic_sha256"] = semantic(value)


def negative_controls(matrix: dict[str, Any], inventory: dict[str, Any]) -> tuple[int, int]:
    expected_before = sha(canonical(expected_sources(inventory)))
    tolerance_before = sha(canonical(expected_tolerance_provenance(inventory)))
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("rate_3600_omit", lambda x: x["probe_records"][0].__setitem__("observed", 2.0)),
        ("rate_3600_duplicate", lambda x: x["probe_records"][0].__setitem__("observed", 2.0/3600.0/3600.0)),
        ("lq_raw_hour_wrong", lambda x: x["probe_records"][1]["observed"].__setitem__("raw_hour", 0.0)),
        ("lq_compensation_wrong_sign", lambda x: x["probe_records"][1]["inputs"].__setitem__("comment_only_compensation_sign", "dH_phys=dH-R*T*ln(3600)")),
        ("lq_compensation_omit", lambda x: x["probe_records"][1]["observed"].__setitem__("compensated_second", x["probe_records"][1]["observed"]["raw_second"])),
        ("lq_global_basis_promotion", lambda x: x["probe_records"][1].__setitem__("basis", "Ah")),
        ("lq_comment_to_executable", lambda x: x["probe_records"][1]["inputs"].__setitem__("executable_seconds_correction", True)),
        ("lq_basis_branch_delete", lambda x: x["probe_records"][1]["inputs"]["basis_hypotheses"].pop()),
        ("lq_basis_branch_swap", lambda x: x["probe_records"][1]["inputs"]["basis_hypotheses"].reverse()),
        ("lq_basis_branch_select", lambda x: x["probe_records"][1]["inputs"]["basis_hypotheses"][0].__setitem__("selected", True)),
        ("lq_basis_resolved", lambda x: x["probe_records"][1]["inputs"].__setitem__("basis_resolution", "Ah")),
        ("unit_value_coordinated", lambda x: (x["probe_records"][5].__setitem__("observed", 9.0), x["probe_records"][5].__setitem__("basis", "kC"))),
        ("current_sign_flip", lambda x: x["probe_records"][2].__setitem__("observed", 3.72)),
        ("direction_crosswire", lambda x: x["probe_records"][2].__setitem__("sign_convention", x["probe_records"][3]["sign_convention"] + "_X")),
        ("zero_nonzero", lambda x: x["probe_records"][4].__setitem__("observed", 3.700001)),
        ("zero_alpha1_direction_drift", lambda x: x["probe_records"][4]["observed"]["s_minus"].__setitem__(0, 0.2)),
        ("zero_general_promotion", lambda x: x["limitation_records"][0].__setitem__("universal_dqdv_zero_equals_equilibrium", True)),
        ("zero_limitation_drop", lambda x: x["limitation_records"][0]["excluded_conditions"].pop()),
        ("ah_c_invert", lambda x: x["probe_records"][5].__setitem__("formula", "Q_C=Q_Ah/3600")),
        ("energy_duplicate_3600", lambda x: x["probe_records"][6].__setitem__("observed", 3240000.0)),
        ("milli_factor_omit", lambda x: x["probe_records"][5].__setitem__("formula", "Q_C=Q_mAh*3600")),
        ("milli_factor_duplicate", lambda x: x["probe_records"][5].__setitem__("formula", "Q_C=(Q_mAh/1000/1000)*3600")),
        ("faraday_omit", lambda x: x["probe_records"][7].__setitem__("observed", 10.0)),
        ("faraday_duplicate", lambda x: x["probe_records"][7].__setitem__("observed", 10.0/96485.0/96485.0)),
        ("reversible_sign", lambda x: x["probe_records"][9].__setitem__("observed", -x["probe_records"][9]["observed"])),
        ("temperature_factor_omit", lambda x: x["probe_records"][9].__setitem__("observed", x["probe_records"][9]["observed"]/300.0)),
        ("mass_capacity_crosswire", lambda x: x["probe_records"][11].__setitem__("observed", 0.1)),
        ("component_total_crosswire", lambda x: x["probe_records"][12]["observed"].__setitem__("Q_total", x["probe_records"][12]["observed"]["f_Si"])),
        ("irreversible_universal_positive", lambda x: x["probe_records"][13]["inputs"].__setitem__("universal_nonnegative_guard", "ENFORCED")),
        ("area_sign", lambda x: x["probe_records"][14].__setitem__("observed", -x["probe_records"][14]["observed"])),
        ("derivative_reverse", lambda x: x["probe_records"][15].__setitem__("observed", -x["probe_records"][15]["observed"])),
        ("derivative_loose_tolerance", lambda x: x["probe_records"][15]["tolerance"].__setitem__("absolute", 1.0)),
        ("derivative_step_crosswire", lambda x: x["probe_records"][15]["inputs"].__setitem__("delta_T_K", 1.0)),
        ("derivative_domain_crosswire", lambda x: x["probe_records"][15]["inputs"].__setitem__("x", 1.0)),
        ("bool_int_type", lambda x: x["authority"].__setitem__("runtime_behavior", 0)),
        ("int_float_type", lambda x: x["universe"].__setitem__("probe_rows", 16.0)),
        ("nan", lambda x: x["probe_records"][0].__setitem__("observed", float("nan"))),
        ("inf", lambda x: x["probe_records"][0].__setitem__("observed", float("inf"))),
        ("complex_transport", lambda x: x["probe_records"][0].__setitem__("observed", {"complex": [1.0, 2.0]})),
        ("row_delete", lambda x: x["probe_records"].pop()),
        ("row_duplicate", lambda x: x["probe_records"].append(copy.deepcopy(x["probe_records"][0]))),
        ("row_order", lambda x: x["probe_records"].reverse()),
        ("source_path_crosswire", lambda x: x["source_occurrence_records"][0].__setitem__("path", x["source_occurrence_records"][1]["path"])),
        ("source_blob_crosswire", lambda x: x["source_occurrence_records"][0].__setitem__("blob_oid", x["source_occurrence_records"][2]["blob_oid"])),
        ("source_line_crosswire", lambda x: x["source_feature_records"][0]["anchors"]["T_ATTEMPT"].__setitem__("start_line", 1)),
        ("source_lf_crosswire", lambda x: x["source_feature_records"][0].__setitem__("lf_sha256", "0" * 64)),
        ("source_lf_normalization", lambda x: x["source_feature_records"][0].__setitem__("lf_normalization", "CRLF_ONLY")),
        ("tolerance_provenance_path", lambda x: x["tolerance_provenance_records"][0]["occurrence_refs"][0].__setitem__("path", "wrong.py")),
        ("tolerance_provenance_blob", lambda x: x["tolerance_provenance_records"][0].__setitem__("blob_oid", "0" * 40)),
        ("tolerance_provenance_release", lambda x: x["tolerance_provenance_records"][0]["occurrence_refs"][0].__setitem__("release", "v0")),
        ("tolerance_provenance_line", lambda x: x["tolerance_provenance_records"][0]["constants"][1]["anchor"].__setitem__("start_line", 1)),
        ("tolerance_provenance_slice", lambda x: x["tolerance_provenance_records"][0]["constants"][1]["anchor"].__setitem__("source_sha256", "0" * 64)),
        ("tolerance_provenance_ast", lambda x: x["tolerance_provenance_records"][0]["constants"][1]["anchor"].__setitem__("node_sha256", "0" * 64)),
        ("tolerance_provenance_size", lambda x: x["tolerance_provenance_records"][0].__setitem__("size_bytes", 0)),
        ("tolerance_provenance_lf_mode", lambda x: x["tolerance_provenance_records"][0].__setitem__("lf_normalization", "CRLF_ONLY")),
        ("tolerance_provenance_method_promotion", lambda x: x["tolerance_provenance_records"][0].__setitem__("relation", "SAME_METHOD")),
        ("tolerance_provenance_missing", lambda x: x["tolerance_provenance_records"].pop()),
        ("tolerance_provenance_extra", lambda x: x["tolerance_provenance_records"].append(copy.deepcopy(x["tolerance_provenance_records"][0]))),
        ("authority_promotion", lambda x: x["authority"].__setitem__("external_scientific", True)),
        ("gnf_promotion", lambda x: x["authority"].__setitem__("open_unit_convention", "RESOLVED")),
        ("nested_extra", lambda x: x["probe_records"][0]["tolerance"].__setitem__("extra", False)),
        ("top_extra", lambda x: x.__setitem__("extra", False)),
    ]
    passed = 0
    for name, mutation in mutations:
        candidate = copy.deepcopy(matrix)
        before = copy.deepcopy(candidate)
        mutation(candidate)
        require(not typed_equal(before, candidate), "E_NEGATIVE_NOOP", name)
        rejected = False
        try:
            reseal(candidate)
            rejected = bool(artifact_errors(candidate, inventory))
        except (TypeError, ValueError):
            rejected = True
        require(rejected, "E_NEGATIVE_FALSE_PASS", name)
        passed += 1
    require(sha(canonical(expected_sources(inventory))) == expected_before,
            "E_EXPECTED_CACHE_POISON")
    require(sha(canonical(expected_tolerance_provenance(inventory))) == tolerance_before,
            "E_TOLERANCE_CACHE_POISON")
    return passed, len(mutations)


def json_controls() -> tuple[int, int]:
    good = canonical({"semantic_sha256": "x", "v": [1, True, 2.0]})
    tests = [
        ("duplicate", b'{"a":1,"a":2}\n'),
        ("nan", b'{"a":NaN}\n'),
        ("noncanonical", b'{"v":[1,true,2.0],"semantic_sha256":"x"}\n'),
    ]
    passed = 0
    for name, raw in tests:
        try:
            strict_load(raw, name, True)
        except ValidationError:
            passed += 1
    require(good != tests[-1][1], "E_JSON_CONTROL_NOOP")
    return passed, len(tests)


def neutral_source_hash(path: Path, constant: str) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    pattern = rf'({constant}\s*=\s*")[^"]+("\n)'
    normalized, count = re.subn(pattern, rf'\1<NEUTRAL>\2', text)
    require(count == 1, "E_SOURCE_PIN_CARDINALITY", constant)
    return sha(normalized.encode("utf-8"))


def source_policy() -> None:
    builder = ROOT / BUILDER_PATH
    validator = ROOT / VALIDATOR_PATH
    require(neutral_source_hash(builder, "BUILDER_SOURCE_POLICY_SHA256_LF") == BUILDER_SOURCE_POLICY_SHA256_LF,
            "E_BUILDER_POLICY_HASH")
    require(neutral_source_hash(validator, "VALIDATOR_SOURCE_POLICY_SHA256_LF") == VALIDATOR_SOURCE_POLICY_SHA256_LF,
            "E_VALIDATOR_POLICY_HASH")
    expected_direct = {
        builder: {"argparse", "ast", "hashlib", "json", "math", "os", "subprocess", "sys"},
        validator: {"argparse", "ast", "copy", "hashlib", "json", "math", "re", "subprocess", "sys"},
    }
    for path in (builder, validator):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        direct = {alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names}
        require(direct == expected_direct[path], "E_SOURCE_IMPORT")
        imports = {(node.module or "", tuple(alias.name for alias in node.names))
                   for node in tree.body if isinstance(node, ast.ImportFrom)}
        require(all(module in {"__future__", "typing", "pathlib"} for module, _ in imports), "E_SOURCE_IMPORT_FROM")
        require(not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id in {"eval", "exec", "compile", "open"}
                        for node in ast.walk(tree)), "E_SOURCE_DYNAMIC")
        require(not any(isinstance(node, ast.Call) and any(
            keyword.arg == "shell" and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is True for keyword in node.keywords)
            for node in ast.walk(tree)), "E_SOURCE_PROCESS_SHELL")


def control_document_errors(documents: dict[str, str]) -> list[str]:
    errors = []
    parent_text = documents[PARENT_LEDGER]
    phase_rows = [line for line in parent_text.splitlines() if line.startswith("| 067 |")]
    if len(phase_rows) != 1:
        errors.append("PHASE067_ROW_CARDINALITY")
    else:
        row = phase_rows[0]
        for token in ("Steps 82–86 persisted", "Step 87 unit/numerical audit pending persistence",
                      "4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7",
                      "PASS_P067_STEP86_PERSISTENCE", "PASS_P067_STEP87_UNIT_NUMERICAL"):
            if token not in row:
                errors.append("PHASE067_ROW_" + token[:12])
        if "Step 86 test/demo/golden/guide/tool audit fixed pending persistence" in row:
            errors.append("PHASE067_STALE_STEP86_PENDING")
    handover_lines = [line for line in documents[HANDOVER].splitlines()
                      if line.startswith("20. 현재 result:")]
    expected_pointer = ("20. 현재 result: `Codex/results/PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md`; "
                        "Step 86 test/demo/golden, Step 85 state/default/import, Step 84 call-graph, "
                        "Step 83 state-flow, Step 82 source-topology, activation and repair results retained as prior evidence")
    if handover_lines != [expected_pointer]:
        errors.append("HANDOVER_CURRENT_RESULT")
    return errors


def control_document_controls(documents: dict[str, str]) -> tuple[int, int]:
    mutations = [
        ("stale_step86_pending", PARENT_LEDGER, "Steps 82–86 persisted", "Steps 82–85 persisted"),
        ("stale_current_result", HANDOVER, "PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md",
         "PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md"),
    ]
    passed = 0
    for name, path, old, new in mutations:
        candidate = dict(documents)
        require(old in candidate[path] and old != new, "E_DOC_CONTROL_PRECONDITION", name)
        candidate[path] = candidate[path].replace(old, new, 1)
        require(bool(control_document_errors(candidate)), "E_DOC_CONTROL_FALSE_PASS", name)
        passed += 1
    return passed, len(mutations)


def control_documents() -> tuple[int, int]:
    documents = {}
    for path, pin in CONTROL_SHA256.items():
        raw = (ROOT / path).read_bytes()
        require(sha(raw) == pin, "E_CONTROL_HASH", path)
        documents[path] = raw.decode("utf-8")
    combined = "\n".join(documents.values())
    for token in (EXPECTED_PARENT, SUBJECT, GATE, PERSISTENCE, "PASS_PENDING_PERSISTENCE",
                  "PASS_P067_STEP86_PERSISTENCE", "4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7",
                  "Step 88", "blocked"):
        require(token in combined, "E_CONTROL_TOKEN", token)
    require("Step 86" in combined and "pushed/live/clean" in combined, "E_STEP86_PERSISTED_DOC")
    require(not control_document_errors(documents), "E_CONTROL_DOCUMENT_SEMANTIC",
            ",".join(control_document_errors(documents)))
    return control_document_controls(documents)


def parse_porcelain(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4 and line[2] == " ", "E_STATUS_LINE")
        status_code, path = line[:2], line[3:].replace("\\", "/")
        require(" -> " not in path and path not in out, "E_STATUS_RENAME")
        out[path] = status_code
    return out


def parse_name_status(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        status_code, path = line.split("\t", 1)
        require(status_code in {"A", "M"} and path not in out, "E_NAME_STATUS")
        out[path] = status_code
    return out


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    return text.removesuffix(".git").strip("/")


def live(ref: str) -> str:
    value = gtext(("ls-remote", "--heads", "origin", ref))
    require("\t" in value, "E_LIVE_REF", ref)
    return value.split("\t", 1)[0]


def repository_refs(tip: str) -> dict[str, str]:
    actual = {"branch": gtext(("rev-parse", "--abbrev-ref", "HEAD")),
              "head": gtext(("rev-parse", "HEAD")),
              "upstream_name": gtext(("rev-parse", "--abbrev-ref", "@{upstream}")),
              "upstream_oid": gtext(("rev-parse", UPSTREAM)),
              "tracking_oid": gtext(("rev-parse", f"refs/remotes/{UPSTREAM}")),
              "live_oid": live(f"refs/heads/{BRANCH}"),
              "origin": canonical_origin(gtext(("ls-remote", "--get-url", "origin"))),
              "protected_local": gtext(("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2")),
              "protected_tracking": gtext(("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2")),
              "protected_live": live("refs/heads/codex/lib-physics-endgame-v1025_2"),
              "main_local": gtext(("show-ref", "--verify", "--hash", "refs/heads/main"), True),
              "main_tracking": gtext(("rev-parse", "refs/remotes/origin/main")),
              "main_live": live("refs/heads/main")}
    expected = {"branch": BRANCH, "head": tip, "upstream_name": UPSTREAM,
        "upstream_oid": tip, "tracking_oid": tip, "live_oid": tip,
        "origin": "github.com/lksz1412/project_anode_fit", "protected_local": PROTECTED_TIP,
        "protected_tracking": PROTECTED_TIP, "protected_live": PROTECTED_TIP,
        "main_local": "", "main_tracking": MAIN_TIP, "main_live": MAIN_TIP}
    require(actual == expected, "E_REPOSITORY_REFS", repr(actual))
    return actual


def status() -> dict[str, str]:
    return parse_porcelain(gtext(("status", "--porcelain=v1", "--untracked-files=all")))


def index_snapshot() -> dict[str, tuple[str, str]]:
    out = {}
    for line in gtext(("ls-files", "-s")).splitlines():
        metadata, path = line.split("\t", 1)
        if path in FINAL_SET:
            mode, oid, stage = metadata.split()
            require(stage == "0", "E_INDEX_STAGE")
            out[path] = (mode, oid)
    return out


def seal(tip: str) -> dict[str, Any]:
    return {"refs": repository_refs(tip), "status": status(), "index": index_snapshot(),
            "path_hashes": {path: sha((ROOT / path).read_bytes()) for path in FINAL_PATHS if (ROOT / path).exists()},
            "input_hashes": {path: sha(commit_bytes(path)) for path in (INVENTORY_PATH, ATTESTATION_PATH, STATE_FLOW_PATH)}}


def verify_content() -> None:
    expected = {path: ("??" if FINAL_STATUS[path] == "A" else " M") for path in FINAL_PATHS}
    require(status() == expected, "E_CONTENT_PATHS", repr(status()))


def verify_staged() -> None:
    require(gtext(("rev-parse", "HEAD")) == EXPECTED_PARENT, "E_STAGED_PARENT")
    require(parse_name_status(gtext(("diff", "--cached", "--name-status", "--no-renames", "HEAD"))) == FINAL_STATUS,
            "E_STAGED_PATHS")
    require(gtext(("diff", "--name-only")) == "" and gtext(("ls-files", "--others", "--exclude-standard")) == "",
            "E_STAGED_DIRTY")
    require(gtext(("diff", "--cached", "--check")) == "", "E_DIFF_CHECK")
    snapshot = index_snapshot()
    require(set(snapshot) == FINAL_SET and all(mode == "100644" for mode, _ in snapshot.values()), "E_INDEX_MODES")
    for path, (_, oid) in snapshot.items():
        require(git(("show", f":{path}")) == (ROOT / path).read_bytes() == blob(oid), "E_INDEX_BYTES", path)


def verify_persistence(commit: str) -> None:
    require(gtext(("show", "-s", "--format=%P", commit)).split() == [EXPECTED_PARENT], "E_COMMIT_PARENTS")
    require(gtext(("rev-parse", commit + "^")) == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(gtext(("show", "-s", "--format=%s", commit)) == SUBJECT, "E_COMMIT_SUBJECT")
    changed = parse_name_status(gtext(("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r",
                                       commit + "^", commit, "--")))
    require(changed == FINAL_STATUS, "E_COMMIT_PATHS")
    require(gtext(("status", "--porcelain")) == "", "E_WORKTREE_DIRTY")
    require(gtext(("diff", "--name-only", PROTECTED_TIP, "--", "Claude")) == "", "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        require(git(("show", f"{commit}:{path}")) == (ROOT / path).read_bytes(), "E_COMMITTED_BYTES", path)


def git_argv_controls() -> tuple[int, int]:
    prefix = ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r")
    accepted = (*prefix, EXPECTED_PARENT + "^", EXPECTED_PARENT, "--")
    require(git_argv_allowed(accepted), "E_GIT_ARGV_POSITIVE")
    rejected = [(*prefix, EXPECTED_PARENT, EXPECTED_PARENT, "--"),
                (*prefix, EXPECTED_PARENT + "^", EXPECTED_PARENT.upper(), "--"),
                (*prefix, EXPECTED_PARENT + "^", EXPECTED_PARENT, ""),
                (*prefix, EXPECTED_PARENT + "^", EXPECTED_PARENT, "Claude"),
                (*prefix, EXPECTED_PARENT + "^", EXPECTED_PARENT, "--", "extra")]
    require(all(not git_argv_allowed(item) for item in rejected), "E_GIT_ARGV_NEGATIVE")
    observed = parse_name_status(gtext(accepted))
    expected = {
        "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": "M",
        "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md": "M",
        "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md": "M",
        "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json": "A",
        "Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md": "A",
        "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json": "A",
        "Codex/work/v1025_phase067/build_phase067_step86.py": "A",
        "Codex/work/v1025_phase067/validate_phase067_step86.py": "A",
    }
    require(observed == expected, "E_GIT_ARGV_STEP86_FIXTURE")
    return 7, 7


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require((args.verify_persistence and args.expected_commit is not None)
            or (not args.verify_persistence and args.expected_commit is None), "E_EXPECTED_COMMIT_MODE")
    if args.verify_persistence:
        require(is_oid(args.expected_commit or ""), "E_EXPECTED_COMMIT")
    tip = args.expected_commit if args.verify_persistence else EXPECTED_PARENT
    entry = seal(tip or "")
    require((ROOT / MATRIX_PATH).exists(), "E_FILE_MISSING", MATRIX_PATH)
    source_policy()
    doc_result = control_documents()
    inventory, _, state_flow = input_documents()
    require(state_flow["universe"]["flow_target_occurrences"] == 20, "E_STATE_FLOW_INPUT")
    matrix, nodes, depth = strict_load((ROOT / MATRIX_PATH).read_bytes(), MATRIX_PATH)
    errors = artifact_errors(matrix, inventory)
    require(not errors, "E_ARTIFACT", ",".join(errors[:10]))
    negatives = negative_controls(matrix, inventory)
    json_result = json_controls()
    argv_result = git_argv_controls()
    if args.content_only:
        verify_content()
    elif args.verify_staged:
        verify_staged()
    else:
        verify_persistence(args.expected_commit or "")
    terminal = seal(tip or "")
    require(typed_equal(entry, terminal), "E_TRANSACTION_SEAL")
    print(f"PASS_P067_STEP87_CONTROLS semantic={negatives[0]}/{negatives[1]} "
          f"json={json_result[0]}/{json_result[1]} git_argv={argv_result[0]}/{argv_result[1]} "
          f"docs={doc_result[0]}/{doc_result[1]} "
          f"nodes={nodes} depth={depth}")
    print(f"{PERSISTENCE if args.verify_persistence else GATE} occurrences=20 blobs=15 "
          "probes=16 determinism=2/2 authority=internal-only")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
