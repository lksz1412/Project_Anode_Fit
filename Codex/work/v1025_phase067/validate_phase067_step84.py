#!/usr/bin/env python3
"""Validate Phase 067 Step 84 without importing production or the builder."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "1af6c06fb5cff2918b846ed74ea213832f04f010"
BASELINE = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
EXPECTED_SUBJECT = "audit(phase067): reconstruct physics call graph"
GATE = "PASS_P067_STEP84_PHYSICS_CALL_GRAPH"
PERSISTENCE = "PASS_P067_STEP84_PERSISTENCE"

BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step84.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step84.py"
GRAPH_PATH = "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_084_PHYSICS_CALL_GRAPH_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = [BUILDER_PATH, VALIDATOR_PATH, GRAPH_PATH, RESULT_PATH,
               PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER]
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if index < 4 else "M")
                for index, path in enumerate(FINAL_PATHS)}

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STEP83_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
INPUT_PINS = {
    INVENTORY_PATH: ("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63",
                     "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"),
    ATTESTATION_PATH: ("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174",
                       "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"),
    STEP83_PATH: ("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8",
                  "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44"),
}
CONTROL_PINS = {
    RESULT_PATH: "4383e543fe5e3748754eed36b247c9c0e19808ee90f268bb6a0f7447529633d1",
    PARENT_LEDGER: "03f8ffa397b2d2f7074737ebb41b408c03ef2ffa5d7f293b1ada3c0d52c1afa8",
    CANONICAL_LEDGER: "ac7a3478253e5392494649846f88ba3a3cb72feaec08e75ca1f4f7179f1cb639",
    HANDOVER: "9a784fc239f6422e50369741cdf89d63660f1ecfd63030f7c6048cd6255a2338",
}
BUILDER_SOURCE_POLICY_SHA256_LF = "5dd077d3402cf4ece796712367410309b7e2bc0a37bc29c2a2b8643e8af9efe9"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "2d7e3dc34e02fbee69659237463b7085f44773bc69c6842f71361e72fc503ce8"

PUBLIC_NAMES = {"curve", "dqdv", "equilibrium", "solve_U_oc", "host_contributions",
                "entropy_coefficient", "entropy_coefficient_x", "reversible_heat",
                "reversible_heat_x", "irreversible_heat"}
SUBSYSTEMS = ("CHARGE_BALANCE_ROOT", "BACKGROUND_SELF_CONSISTENCY", "LAG_TRAJECTORY",
              "KINETICS", "HEAT", "OBSERVATION_TRANSFORMATION")
BEHAVIORS = ("OPTION_OFF", "MISSING_KINETICS", "ZERO_CURRENT", "REVERSAL", "REST",
             "INVALID_ROOT", "MAX_ITER_EXHAUSTION")
DYNAMIC_ATTRIBUTES = {"Cbg", "chi_split"}
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


class ValidationError(RuntimeError):
    """Controlled validation failure."""


def require(condition: bool, diagnostic: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(diagnostic + (":" + detail if detail else ""))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def strict_load(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    require(not raw.startswith(b"\xef\xbb\xbf"), "E_JSON_BOM", label)
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, "E_JSON_DUPLICATE", f"{label}:{key}")
            result[key] = value
        return result
    def constant(token: str) -> None:
        raise ValidationError("E_JSON_NONFINITE:" + label + ":" + token)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    require(isinstance(value, dict), "E_JSON_TOP", label)
    nodes = 0
    max_depth = 0
    stack = [(value, 1)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        require(nodes <= 500_000 and depth <= 16, "E_JSON_BOUNDS", label)
        if isinstance(current, dict):
            stack.extend((item, depth + 1) for item in current.values())
        elif isinstance(current, list):
            stack.extend((item, depth + 1) for item in current)
        elif isinstance(current, float):
            require(math.isfinite(current), "E_JSON_NONFINITE", label)
    return value, nodes, max_depth


def allowed_git_argv(args: tuple[str, ...]) -> bool:
    fixed = {
        ("rev-parse", "--abbrev-ref", "HEAD"),
        ("rev-parse", "--abbrev-ref", "@{upstream}"),
        ("rev-parse", "HEAD"), ("rev-parse", UPSTREAM),
        ("rev-parse", f"refs/remotes/{UPSTREAM}"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("ls-remote", "--get-url", "origin"),
        ("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2"),
        ("show-ref", "--verify", "--hash", "refs/heads/main"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("status", "--porcelain"), ("ls-files", "-s"),
        ("diff", "--name-only"), ("ls-files", "--others", "--exclude-standard"),
        ("diff", "--cached", "--check"),
        ("diff", "--cached", "--name-status", "--no-renames", "HEAD"),
        ("diff", "--name-only", PROTECTED_TIP, "--", "Claude"),
    }
    if args in fixed:
        return True
    if len(args) == 4 and args[:3] == ("ls-remote", "--heads", "origin"):
        return args[3] in {f"refs/heads/{BRANCH}",
                           "refs/heads/codex/lib-physics-endgame-v1025_2", "refs/heads/main"}
    if len(args) == 2 and args[0] == "show":
        value = args[1]
        if value.startswith(EXPECTED_PARENT + ":"):
            return value.split(":", 1)[1] in INPUT_PINS
        if value.startswith(":"):
            return value[1:] in FINAL_SET
        if re.fullmatch(r"[0-9a-f]{40}:.+", value):
            return value.split(":", 1)[1] in FINAL_SET
    if len(args) == 3 and args[:2] == ("cat-file", "blob"):
        return re.fullmatch(r"[0-9a-f]{40}", args[2]) is not None
    if len(args) == 4 and args[:3] == ("show", "-s", "--format=%P"):
        return re.fullmatch(r"[0-9a-f]{40}", args[3]) is not None
    if len(args) == 4 and args[:3] == ("show", "-s", "--format=%s"):
        return re.fullmatch(r"[0-9a-f]{40}", args[3]) is not None
    if len(args) == 2 and args[0] == "rev-parse" and args[1].endswith("^"):
        return re.fullmatch(r"[0-9a-f]{40}\^", args[1]) is not None
    if len(args) == 7 and args[:5] == ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r"):
        return (re.fullmatch(r"[0-9a-f]{40}\^", args[5]) is not None
                and re.fullmatch(r"[0-9a-f]{40}", args[6]) is not None)
    if len(args) == 3 and args[:2] == ("ls-tree", "-r"):
        return re.fullmatch(r"[0-9a-f]{40}", args[2]) is not None
    return False


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    require(allowed_git_argv(tuple(args)), "E_GIT_ARGV", repr(args))
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                               check=False, shell=False, timeout=60)
    if check:
        require(completed.returncode == 0, "E_GIT_RC", repr(args))
        require(completed.stderr == b"", "E_GIT_STDERR", repr(args))
    elif completed.returncode != 0:
        require(completed.stdout == b"", "E_GIT_OPTIONAL_STDOUT", repr(args))
        return b"" if binary else ""
    return completed.stdout if binary else completed.stdout.decode("utf-8").rstrip("\r\n")


def predecessor_semantic(value: dict[str, Any], path: str) -> str:
    clone = dict(value)
    if path in {INVENTORY_PATH, ATTESTATION_PATH}:
        clone["semantic_sha256"] = ""
        raw = (json.dumps(clone, ensure_ascii=False, indent=2, sort_keys=True,
                          allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")
        return sha256(raw)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def load_predecessor(path: str) -> tuple[dict[str, Any], dict[str, str]]:
    raw = bytes(git("show", f"{EXPECTED_PARENT}:{path}", binary=True))
    raw_pin, semantic_pin = INPUT_PINS[path]
    require(sha256(raw) == raw_pin, "E_INPUT_RAW", path)
    value, _, _ = strict_load(raw, path)
    require(value.get("semantic_sha256") == semantic_pin, "E_INPUT_SEMANTIC_STORED", path)
    require(predecessor_semantic(value, path) == semantic_pin, "E_INPUT_SEMANTIC_FRESH", path)
    return value, {"path": path, "raw_sha256": raw_pin, "semantic_sha256": semantic_pin}


def neutralized_policy_hash(path: str, constant: str) -> str:
    raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    pattern = re.compile(rb"(?m)^(" + constant.encode() + rb" = \x22)[^\x22]*(\x22)$")
    replaced, count = pattern.subn(rb"\1NEUTRALIZED\2", raw)
    require(count == 1, "E_POLICY_PIN_CARDINALITY", path)
    return sha256(replaced)


def safe_type_name_attribute(node: ast.Attribute) -> bool:
    return (node.attr == "__name__" and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name) and node.value.func.id == "type"
            and len(node.value.args) == 1 and not node.value.keywords)


def verify_source_policy() -> None:
    paths = [(BUILDER_PATH, "BUILDER_SOURCE_POLICY_SHA256_LF", BUILDER_SOURCE_POLICY_SHA256_LF),
             (VALIDATOR_PATH, "VALIDATOR_SOURCE_POLICY_SHA256_LF", VALIDATOR_SOURCE_POLICY_SHA256_LF)]
    allowed_imports = {"argparse", "ast", "copy", "hashlib", "json", "math", "os", "re",
                       "subprocess", "sys", "pathlib", "typing", "__future__"}
    for path, constant, expected in paths:
        require(neutralized_policy_hash(path, constant) == expected, "E_SOURCE_POLICY_HASH", path)
        source = (ROOT / path).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=path)
        parents: dict[ast.AST, ast.AST] = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent
        def enclosing_function(node: ast.AST) -> str | None:
            current = parents.get(node)
            while current is not None:
                if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return current.name
                current = parents.get(current)
            return None
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
        require(all(name.split(".", 1)[0] in allowed_imports for name in imports),
                "E_SOURCE_POLICY_IMPORT", path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                require(not node.attr.startswith("__") or safe_type_name_attribute(node),
                        "E_SOURCE_POLICY_DUNDER", path)
            if not isinstance(node, ast.Call):
                continue
            call_name = ast.unparse(node.func)
            require(call_name not in {"eval", "exec", "compile", "__import__"},
                    "E_SOURCE_POLICY_DYNAMIC", path)
            require(call_name not in {"os.system", "subprocess.Popen", "subprocess.call",
                                      "subprocess.check_call", "subprocess.check_output"},
                    "E_SOURCE_POLICY_PROCESS", path)
            for keyword in node.keywords:
                if keyword.arg == "shell":
                    require(isinstance(keyword.value, ast.Constant) and keyword.value.value is False,
                            "E_SOURCE_POLICY_SHELL", path)
            call_attr = node.func.attr if isinstance(node.func, ast.Attribute) else ""
            safe_value_replace = call_name in {
                "(ROOT / path).read_bytes().replace",
                "(ROOT / path).read_bytes().replace(b'\\r\\n', b'\\n').replace",
                "line[3:].replace", "value.lower().replace",
            }
            if call_attr in {"write_text", "write_bytes", "touch", "mkdir", "rename", "replace",
                             "unlink", "remove"} and not safe_value_replace:
                require(path == BUILDER_PATH and enclosing_function(node) == "atomic_write"
                        and call_name in {"os.replace", "temp.unlink"},
                        "E_SOURCE_POLICY_MUTATION", path + ":" + call_name)
            if call_attr == "open":
                require(path == BUILDER_PATH and enclosing_function(node) == "atomic_write"
                        and call_name == "temp.open" and len(node.args) == 1
                        and isinstance(node.args[0], ast.Constant) and node.args[0].value == "xb",
                        "E_SOURCE_POLICY_OPEN", path + ":" + call_name)
        run_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                     and ast.unparse(node.func) == "subprocess.run"]
        require(len(run_calls) == 1, "E_SOURCE_POLICY_RUN_CARDINALITY", path)
        mutation_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                          and ast.unparse(node.func) in {"os.replace", "temp.unlink"}]
        require((len(mutation_calls) == 2 if path == BUILDER_PATH else len(mutation_calls) == 0),
                "E_SOURCE_POLICY_MUTATION_CARDINALITY", path)
    dunder_probe = ast.parse("(lambda: 0).__globals__", mode="eval").body
    require(isinstance(dunder_probe, ast.Attribute) and dunder_probe.attr.startswith("__")
            and not safe_type_name_attribute(dunder_probe),
            "E_SOURCE_POLICY_DUNDER_NEGATIVE")


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


def ast_sha(node: ast.AST) -> str:
    return sha256(canonical_bytes(stable_ast_value(node)))


def segment(source: str, node: ast.AST) -> str:
    value = ast.get_source_segment(source, node)
    require(value is not None, "E_SOURCE_SEGMENT")
    return value


def anchor(source: str, node: ast.AST, owner: str) -> dict[str, Any]:
    text = segment(source, node)
    return {"ast_kind": type(node).__name__, "end_col": node.end_col_offset,
            "end_line": node.end_lineno, "expression": text,
            "normalized_ast_sha256": ast_sha(node), "qualified_owner": owner,
            "source_sha256": sha256(text.encode("utf-8")), "start_col": node.col_offset,
            "start_line": node.lineno}


def definitions(tree: ast.AST) -> tuple[dict[str, ast.AST], dict[str, list[str]], dict[str, list[str]]]:
    found: dict[str, ast.AST] = {}
    simple: dict[str, list[str]] = {}
    classes: dict[str, list[str]] = {}
    scope: list[str] = []
    class Visitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            qualified = ".".join([*scope, node.name])
            found[qualified] = node
            simple.setdefault(node.name, []).append(qualified)
            classes[qualified] = [ast.unparse(base) for base in node.bases]
            scope.append(node.name); self.generic_visit(node); scope.pop()
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            qualified = ".".join([*scope, node.name])
            found[qualified] = node
            simple.setdefault(node.name, []).append(qualified)
            scope.append(node.name); self.generic_visit(node); scope.pop()
        visit_AsyncFunctionDef = visit_FunctionDef
    Visitor().visit(tree)
    return found, simple, classes


def ancestor_order(class_name: str, classes: dict[str, list[str]]) -> list[str]:
    result: list[str] = []
    pending = [class_name]
    while pending:
        current = pending.pop(0)
        if current in result:
            continue
        result.append(current)
        pending.extend(base for base in classes.get(current, []) if base in classes)
    return result


def resolve(owner: str, call: ast.Call, found: dict[str, ast.AST],
            simple: dict[str, list[str]], classes: dict[str, list[str]]) -> tuple[str, str | None]:
    func = call.func
    if isinstance(func, ast.Name):
        nested = f"{owner}.{func.id}"
        if nested in found:
            return "RESOLVED_INTERNAL", nested
        module = [candidate for candidate in simple.get(func.id, []) if "." not in candidate]
        return ("RESOLVED_INTERNAL", module[0]) if len(module) == 1 else ("EXTERNAL_OR_BUILTIN", None)
    if isinstance(func, ast.Attribute):
        parts: list[str] = []
        cursor: ast.AST = func
        while isinstance(cursor, ast.Attribute):
            parts.append(cursor.attr); cursor = cursor.value
        parts.reverse()
        if isinstance(cursor, ast.Name) and cursor.id == "self":
            if len(parts) == 1 and parts[0] in DYNAMIC_ATTRIBUTES:
                return "DYNAMIC_CALLABLE_ATTRIBUTE", None
            if len(parts) == 1:
                class_name = owner.split(".", 1)[0]
                for candidate_class in ancestor_order(class_name, classes):
                    candidate = f"{candidate_class}.{parts[0]}"
                    if candidate in found:
                        return "RESOLVED_INTERNAL", candidate
            return "AMBIGUOUS_DYNAMIC_DISPATCH", None
    return "EXTERNAL_OR_BUILTIN", None


def call_sites(root: ast.AST) -> list[dict[str, Any]]:
    sites: list[dict[str, Any]] = []
    predicates: list[str] = []
    statement: list[ast.AST] = []
    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if node is root:
                for item in node.body: self.visit(item)
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            if node is root:
                for item in node.body: self.visit(item)
        def visit_If(self, node: ast.If) -> None:
            self.visit(node.test); test = ast.unparse(node.test)
            predicates.append(test)
            for item in node.body: self.visit(item)
            predicates.pop()
            if node.orelse:
                predicates.append(f"NOT({test})")
                for item in node.orelse: self.visit(item)
                predicates.pop()
        def visit_IfExp(self, node: ast.IfExp) -> None:
            self.visit(node.test); test = ast.unparse(node.test)
            predicates.append(test); self.visit(node.body); predicates.pop()
            predicates.append(f"NOT({test})"); self.visit(node.orelse); predicates.pop()
        def _statement(self, node: ast.AST) -> None:
            statement.append(node); self.generic_visit(node); statement.pop()
        visit_Assign = _statement
        visit_AnnAssign = _statement
        visit_AugAssign = _statement
        visit_Return = _statement
        visit_Expr = _statement
        def visit_Call(self, node: ast.Call) -> None:
            sites.append({"node": node, "predicates": list(predicates),
                          "statement": statement[-1] if statement else node})
            self.generic_visit(node)
    Visitor().visit(root)
    return sorted(sites, key=lambda row: (row["node"].lineno, row["node"].col_offset,
                                          row["node"].end_lineno, row["node"].end_col_offset))


def binding(statement: ast.AST) -> dict[str, Any]:
    if isinstance(statement, ast.Assign):
        return {"kind": "ASSIGNMENT", "targets": [ast.unparse(target) for target in statement.targets]}
    if isinstance(statement, (ast.AnnAssign, ast.AugAssign)):
        return {"kind": "ASSIGNMENT", "targets": [ast.unparse(statement.target)]}
    if isinstance(statement, ast.Return):
        return {"kind": "RETURN", "targets": []}
    return {"kind": "EXPRESSION", "targets": []}


def edge_matches(edge: dict[str, Any], targets: set[str]) -> bool:
    values = {edge["callable_expression"]}
    if edge["callee"]:
        values |= {edge["callee"], edge["callee"].rsplit(".", 1)[-1]}
    return any(value == target or value.endswith("." + target)
               for value in values for target in targets)


def shortest(root: str, outgoing: dict[str, list[dict[str, Any]]],
             targets: set[str]) -> list[list[dict[str, Any]]]:
    if not targets:
        return [[]]
    queue: list[tuple[str, list[dict[str, Any]], frozenset[str]]] = [(root, [], frozenset({root}))]
    found: list[list[dict[str, Any]]] = []
    depth: int | None = None
    while queue:
        owner, path, seen = queue.pop(0)
        if (depth is not None and len(path) >= depth) or len(path) >= 8:
            continue
        for edge in outgoing.get(owner, []):
            candidate = [*path, edge]
            if edge_matches(edge, targets):
                found.append(candidate); depth = len(candidate) if depth is None else depth
            elif edge["resolution"] == "RESOLVED_INTERNAL" and edge["callee"] not in seen:
                queue.append((edge["callee"], candidate, seen | {edge["callee"]}))
    return found


def first_anchor(source: str, owner: str, node: ast.AST, predicate: Any) -> dict[str, Any] | None:
    matches = [item for item in ast.walk(node) if hasattr(item, "lineno") and predicate(item)]
    if not matches:
        return None
    matches.sort(key=lambda item: (item.lineno, item.col_offset, item.end_lineno, item.end_col_offset))
    return anchor(source, matches[0], owner)


def reconstruct_blob(representative: dict[str, Any], rows: list[dict[str, Any]],
                     source: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    tree = ast.parse(source, filename=representative["path"])
    found, simple, classes = definitions(tree)
    all_edges: list[dict[str, Any]] = []
    counter = 0
    for owner, node in sorted(found.items(), key=lambda item: (item[1].lineno, item[1].col_offset, item[0])):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for ordinal, site in enumerate(call_sites(node), 1):
            resolution, callee = resolve(owner, site["node"], found, simple, classes)
            if resolution == "EXTERNAL_OR_BUILTIN":
                continue
            counter += 1
            call = site["node"]
            all_edges.append({"argument_expressions": [ast.unparse(arg) for arg in call.args],
                              "branch_predicates": site["predicates"],
                              "call_anchor": anchor(source, call, owner),
                              "callable_expression": ast.unparse(call.func), "callee": callee,
                              "caller": owner,
                              "edge_id": f"P067-S84-B{representative['blob_ordinal']:03d}-E{counter:04d}",
                              "keyword_arguments": [{"name": kw.arg, "value": ast.unparse(kw.value)}
                                                    for kw in call.keywords],
                              "lexical_ordinal_in_caller": ordinal,
                              "resolution": resolution, "result_binding": binding(site["statement"]),
                              "state_dependency_authority": "SOURCE_STATIC_ARGUMENT_AND_BINDING_ONLY"})
    public = sorted([qualified for qualified, node in found.items()
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                     and node.name in PUBLIC_NAMES], key=lambda q: (found[q].lineno, q))
    outgoing_all: dict[str, list[dict[str, Any]]] = {}
    for edge in all_edges: outgoing_all.setdefault(edge["caller"], []).append(edge)
    for values in outgoing_all.values():
        values.sort(key=lambda edge: (edge["lexical_ordinal_in_caller"], edge["edge_id"]))
    reachable = set(public); pending = list(public)
    while pending:
        owner = pending.pop(0)
        for edge in outgoing_all.get(owner, []):
            target = edge["callee"]
            if edge["resolution"] == "RESOLVED_INTERNAL" and target not in reachable:
                reachable.add(target); pending.append(target)
    reachable_edges = [edge for edge in all_edges if edge["caller"] in reachable]
    reachable_ids = {edge["edge_id"] for edge in reachable_edges}
    outgoing = {owner: [edge for edge in values if edge["edge_id"] in reachable_ids]
                for owner, values in outgoing_all.items() if owner in reachable}
    sequences = []
    for scenario_ordinal, (subsystem, scenario, root_name, targets) in enumerate(SCENARIOS, 1):
        roots = [qualified for qualified in public if found[qualified].name == root_name]
        candidates = []
        for public_root in roots:
            for candidate_ordinal, path in enumerate(shortest(public_root, outgoing, targets), 1):
                candidates.append({"branch_predicate_projection": [edge["branch_predicates"] for edge in path],
                                   "candidate_ordinal": candidate_ordinal,
                                   "edge_ids": [edge["edge_id"] for edge in path],
                                   "public_entry": public_root,
                                   "terminal": ((path[-1]["callee"] or path[-1]["callable_expression"])
                                                if path else public_root)})
        sequences.append({"authority": "STATIC_PUBLIC_ENTRY_CALL_SEQUENCE_NOT_EXECUTED_RUNTIME_ORDER",
                          "candidate_paths": candidates,
                          "presence": "PRESENT" if candidates else "ABSENT_IN_FROZEN_SOURCE",
                          "scenario": scenario,
                          "sequence_id": f"P067-S84-B{representative['blob_ordinal']:03d}-S{scenario_ordinal:03d}",
                          "subsystem": subsystem, "target_selector": sorted(targets)})
    retained_ids = {edge_id for sequence in sequences for candidate in sequence["candidate_paths"]
                    for edge_id in candidate["edge_ids"]}
    edges = [edge for edge in reachable_edges if edge["edge_id"] in retained_ids]
    retained_nodes = set(public)
    for edge in edges:
        retained_nodes.add(edge["caller"])
        if edge["callee"]: retained_nodes.add(edge["callee"])
    node_records = [{"anchor": anchor(source, found[q], q),
                     "definition_kind": type(found[q]).__name__,
                     "name": getattr(found[q], "name"),
                     "public_entry": getattr(found[q], "name") in PUBLIC_NAMES,
                     "qualified_name": q}
                    for q in sorted(retained_nodes, key=lambda q: (found[q].lineno, q))]
    features = {"blend_public_entries": any(q.startswith("BlendedAnodeDQDV.") for q in public),
                "causal_lowpass_work_grid": "_causal_lowpass" in simple and "np.interp(V_n" in source,
                "causal_pointwise_sort_inverse": "_causal_memory_pointwise" in simple and "inv_order" in source,
                "causal_ratio_frozen_path": "_causal_memory_ratio" in simple and "ksi_lag0" in source,
                "causal_pad_re_evaluation": "_causal_pad" in simple and "_ksi_eq_ext" in source,
                "charge_balance_root": bool(simple.get("solve_U_oc")),
                "func_U_j_hys_defined": "func_U_j_hys" in simple,
                "public_callers_of_func_U_j_hys": sum(edge["callee"] == "func_U_j_hys" for edge in reachable_edges),
                "transfer_helper_defined": "transfer_apparent_from_equilibrium" in simple,
                "public_callers_of_transfer_helper": sum(edge["callee"] == "transfer_apparent_from_equilibrium"
                                                         for edge in reachable_edges)}
    def by_name(name: str) -> list[tuple[str, ast.AST]]:
        return [(qualified, node) for qualified, node in found.items()
                if getattr(node, "name", None) == name]
    dqdv = by_name("dqdv")
    lag = by_name("_resolve_lag_length")
    solve = by_name("solve_U_oc")
    option_anchor = (first_anchor(source, dqdv[0][0], dqdv[0][1],
                                  lambda n: isinstance(n, ast.If)
                                  and ast.unparse(n.test) == "self.lag_ratio_correction"
                                  and bool(n.orelse)
                                  and any(isinstance(item, ast.Assign)
                                          and "_causal_memory_pointwise" in ast.unparse(item)
                                          for item in n.orelse))
                     if dqdv else None)
    reversal_anchor = (first_anchor(source, dqdv[0][0], dqdv[0][1],
                                    lambda n: isinstance(n, ast.If) and "sigma_d" in ast.unparse(n.test))
                       if dqdv else None)
    lag_guard = (first_anchor(source, lag[0][0], lag[0][1],
                              lambda n: isinstance(n, ast.If)
                              and ("I_abs" in ast.unparse(n.test) or "dH_a" in ast.unparse(n.test)))
                 if lag else None)
    def sequence_refs(*scenario_names: str) -> list[str]:
        selected = set(scenario_names)
        return sorted(sequence["sequence_id"] for sequence in sequences
                      if sequence["scenario"] in selected and sequence["presence"] == "PRESENT")
    behaviors: list[dict[str, Any]] = []
    def add(condition: str, status: str, mechanism: str,
            evidence: dict[str, Any] | None, owner: str, refs: list[str],
            subcases: list[dict[str, Any]] | None = None) -> None:
        if status != "SOURCE_STATIC_PRESENT":
            require(refs == [], "E_NONPRESENT_BEHAVIOR_REFS")
        behaviors.append({"behavior_id": f"P067-S84-{representative['release_ordinal']:03d}-B{len(behaviors)+1:02d}",
                          "condition": condition, "downstream_owner": owner,
                          "evidence": evidence, "evidence_subcases": subcases or [],
                          "mechanism": mechanism, "public_sequence_refs": refs,
                          "release": representative["release"], "status": status})
    add("OPTION_OFF", "SOURCE_STATIC_PRESENT" if option_anchor else "ABSENT_IN_FROZEN_SOURCE",
        "lag_ratio_correction false selects ordinary _causal_memory_pointwise",
        option_anchor, "P067-STEP88", sequence_refs("DQDV_TO_POINTWISE_MEMORY") if option_anchor else [])
    add("MISSING_KINETICS", "SOURCE_STATIC_PRESENT" if lag_guard else "GROUND_NOT_FOUND_STATIC",
        "missing activation input selects zero lag length", lag_guard, "P067-STEP88",
        sequence_refs("DQDV_TO_LAG_RESOLVER") if lag_guard else [])
    add("ZERO_CURRENT", "SOURCE_STATIC_PRESENT" if lag_guard else "GROUND_NOT_FOUND_STATIC",
        "nonpositive current selects zero lag length", lag_guard, "P067-STEP88",
        sequence_refs("DQDV_TO_LAG_RESOLVER") if lag_guard else [])
    add("REVERSAL", "SOURCE_STATIC_PRESENT" if reversal_anchor else "GROUND_NOT_FOUND_STATIC",
        "direction branch reverses causal traversal and restores order", reversal_anchor, "P067-STEP88",
        sequence_refs("DQDV_TO_CAUSAL_LOWPASS", "DQDV_TO_POINTWISE_MEMORY",
                      "DQDV_TO_RATIO_MEMORY", "DQDV_TO_CAUSAL_PAD") if reversal_anchor else [])
    hys = found.get("func_U_j_hys")
    hys_inbound = features["public_callers_of_func_U_j_hys"]
    rest_status = ("DORMANT_NO_PUBLIC_CALLER" if hys is not None and hys_inbound == 0
                   else "SOURCE_STATIC_PRESENT" if hys is not None else "ABSENT_IN_FROZEN_SOURCE")
    add("REST", rest_status,
        "rest-aware hysteresis helper has no fresh public-entry caller" if hys else "rest-aware helper absent",
        anchor(source, hys, "func_U_j_hys") if hys else None, "P067-STEP88", [])
    invalid_subcases: list[dict[str, Any]] = []
    midpoint = None
    if solve:
        qsolve, nsolve = solve[0]
        invalid_specs = (
            ("X_BAR_DOMAIN", lambda text: "x_arr" in text and "isfinite" in text
             and "<= 0.0" in text and ">= 1.0" in text),
            ("Q_TOTAL_NONPOSITIVE", lambda text: "Q_tot <= 0.0" in text),
            ("BRACKET_ORDER", lambda text: "U_lo >= U_hi" in text),
            ("ENDPOINT_SIGN", lambda text: "f_lo < 0.0 < f_hi" in text),
        )
        for subcase, predicate in invalid_specs:
            matches = [node for node in ast.walk(nsolve) if isinstance(node, ast.If)
                       and predicate(ast.unparse(node.test))]
            require(len(matches) == 1, "E_INVALID_ROOT_SUBCASE", subcase)
            raises = [node for node in matches[0].body if isinstance(node, ast.Raise)]
            require(len(raises) == 1, "E_INVALID_ROOT_RAISE", subcase)
            invalid_subcases.append({"predicate_anchor": anchor(source, matches[0], qsolve),
                                     "raise_anchor": anchor(source, raises[0], qsolve),
                                     "subcase": subcase})
        midpoint_candidates = sorted(
            [node for node in ast.walk(nsolve) if isinstance(node, ast.Assign)
             and "out[" in ast.unparse(node) and "lo" in ast.unparse(node.value)
             and "hi" in ast.unparse(node.value)],
            key=lambda node: (node.lineno, node.col_offset))
        middle = midpoint_candidates[-1] if midpoint_candidates else None
        midpoint = anchor(source, middle, qsolve) if middle else None
    add("INVALID_ROOT", "SOURCE_STATIC_PRESENT" if invalid_subcases else "ABSENT_IN_FROZEN_SOURCE",
        "x_bar domain, nonpositive Q_tot, bracket order, and endpoint sign each raise",
        None, "P067-STEP88", sequence_refs("SOLVE_ROOT_TO_RESIDUAL") if invalid_subcases else [],
        invalid_subcases)
    add("MAX_ITER_EXHAUSTION", "SOURCE_STATIC_PRESENT" if midpoint else "ABSENT_IN_FROZEN_SOURCE",
        "loop exhaustion returns the final bracket midpoint without an explicit nonconvergence raise",
        midpoint, "P067-STEP88", sequence_refs("SOLVE_ROOT_TO_RESIDUAL") if midpoint else [])
    dormant = []
    for name, downstream in (("func_U_j_hys", "P067-STEP88"),
                             ("transfer_apparent_from_equilibrium", "P067-STEP87")):
        node = found.get(name)
        inbound = [edge["edge_id"] for edge in reachable_edges if edge["callee"] == name]
        dormant.append({"anchor": anchor(source, node, name) if node else None,
                        "defined": node is not None, "downstream_owner": downstream,
                        "helper": name, "public_inbound_edge_refs": inbound,
                        "status": ("DORMANT_NO_PUBLIC_CALLER" if node is not None and not inbound
                                   else "PUBLICLY_REACHABLE" if inbound else "ABSENT_IN_FROZEN_SOURCE")})
    refs = [{key: row[key] for key in ("release", "release_ordinal", "manifest_entry_index",
             "path", "blob_oid", "blob_ordinal", "git_mode", "physical_lines", "raw_sha256")}
            for row in rows]
    graph = {"blob_oid": representative["blob_oid"],
             "blob_ordinal": representative["blob_ordinal"], "dormant_records": dormant,
             "edge_records": edges, "feature_contract": features,
             "node_records": node_records, "occurrence_refs": refs,
             "sequence_records": sequences}
    return graph, behaviors


def reconstruct_artifact() -> tuple[dict[str, Any], dict[str, Any]]:
    inventory, inventory_input = load_predecessor(INVENTORY_PATH)
    attestation, attestation_input = load_predecessor(ATTESTATION_PATH)
    step83, step83_input = load_predecessor(STEP83_PATH)
    require(inventory.get("universe", {}).get("unique_blobs") == 84, "E_INVENTORY_DENOMINATOR")
    require(attestation.get("coverage", {}).get("unique_blobs_read_full") == 84,
            "E_ATTESTATION_DENOMINATOR")
    universe = step83.get("universe", {})
    require((universe.get("all_occurrences"), universe.get("all_unique_blobs"),
             universe.get("all_unique_blob_physical_lines"), universe.get("releases"),
             universe.get("flow_target_occurrences"), universe.get("flow_target_unique_blobs"),
             universe.get("losslessly_excluded_nonproduction_occurrences"))
            == (129, 84, 29952, 20, 20, 15, 109), "E_STEP83_DENOMINATOR")
    rows = step83.get("source_records")
    require(isinstance(rows, list) and len(rows) == 20, "E_SOURCE_COUNT")
    require([row.get("release_ordinal") for row in rows] == list(range(1, 21)), "E_RELEASE_ORDER")
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows: grouped.setdefault(row["blob_oid"], []).append(row)
    require(len(grouped) == 15, "E_BLOB_COUNT")
    graph_records = []
    templates: dict[str, list[dict[str, Any]]] = {}
    for oid, members in sorted(grouped.items(), key=lambda item: item[1][0]["blob_ordinal"]):
        raw = bytes(git("cat-file", "blob", oid, binary=True))
        require(all(sha256(raw) == row["raw_sha256"] for row in members), "E_SOURCE_RAW", oid)
        source = raw.decode("utf-8")
        graph, behavior = reconstruct_blob(members[0], members, source)
        graph_records.append(graph); templates[oid] = behavior
    source_records = [{key: row[key] for key in ("release", "release_ordinal", "manifest_entry_index",
                      "path", "blob_oid", "blob_ordinal", "git_mode", "physical_lines", "raw_sha256")}
                      | {"graph_blob_ref": f"P067-S84-B{row['blob_ordinal']:03d}"} for row in rows]
    coverage_records = []
    behavior_records = []
    graph_by_oid = {record["blob_oid"]: record for record in graph_records}
    for row in rows:
        graph = graph_by_oid[row["blob_oid"]]
        common = {"release": row["release"], "release_ordinal": row["release_ordinal"],
                  "path": row["path"], "blob_oid": row["blob_oid"], "blob_ordinal": row["blob_ordinal"]}
        for subsystem in SUBSYSTEMS:
            refs = [sequence["sequence_id"] for sequence in graph["sequence_records"]
                    if sequence["subsystem"] == subsystem and sequence["presence"] == "PRESENT"]
            coverage_records.append(common | {
                "coverage_id": f"P067-S84-{row['release_ordinal']:03d}-{subsystem}",
                "presence": "PRESENT" if refs else "ABSENT_IN_FROZEN_SOURCE",
                "sequence_refs": refs, "subsystem": subsystem})
        for ordinal, template in enumerate(templates[row["blob_oid"]], 1):
            material = {key: value for key, value in template.items()
                        if key not in {"behavior_id", "release"}}
            behavior_records.append(common | material
                                    | {"behavior_id": f"P067-S84-{row['release_ordinal']:03d}-B{ordinal:02d}"})
    counts = {"behavior_records": len(behavior_records), "coverage_records": len(coverage_records),
              "dynamic_edges": sum(edge["resolution"] != "RESOLVED_INTERNAL"
                                   for graph in graph_records for edge in graph["edge_records"]),
              "edge_records": sum(len(graph["edge_records"]) for graph in graph_records),
              "node_records": sum(len(graph["node_records"]) for graph in graph_records),
              "release_occurrences": len(source_records),
              "sequence_records": sum(len(graph["sequence_records"]) for graph in graph_records),
              "shared_blob_semantic_drift": 0, "subsystems_per_release": 6}
    expected: dict[str, Any] = {
        "artifact": "PHASE_067_PHYSICS_CALL_GRAPH",
        "authority": {"actual_runtime_order_proven": False, "canonical_model_selected": False,
                      "external_scientific_or_material_validity": False,
                      "production_source_modified": False,
                      "source_static_public_entry_call_sequence": True,
                      "theory_claim_validated": False,
                      "unresolved_dynamic_dispatch_promoted": False},
        "baseline_commit": BASELINE, "behavior_records": behavior_records,
        "blob_graph_records": graph_records, "branch": BRANCH,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN", "coverage": counts,
        "coverage_records": coverage_records, "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT, "gate": GATE, "generated_date": "2026-09-02",
        "inputs": {"step82_full_read_attestation": attestation_input,
                   "step82_inventory": inventory_input, "step83_state_quantity_flow": step83_input},
        "json_outputs_last": True, "persistence_terminal": PERSISTENCE, "phase": 67,
        "precommit_status": "PASS_PENDING_PERSISTENCE", "result_first": True,
        "schema_version": "phase067-step84-physics-call-graph-v1", "semantic_sha256": "",
        "source_records": source_records, "step": 84,
        "universe": {"all_occurrences": 129, "all_unique_blob_physical_lines": 29952,
                     "all_unique_blobs": 84, "code_occurrences": 20,
                     "code_unique_blobs": 15, "excluded_nonproduction_occurrences": 109,
                     "releases": 20},
        "validation": {"ambiguous_dynamic_dispatch_promotions": 0,
                       "behavior_cardinality_mismatches": 0,
                       "coverage_cardinality_mismatches": 0,
                       "false_transfer_helper_edges": 0, "missing_source_anchors": 0,
                       "noncontiguous_sequences": 0, "runtime_authority_promotions": 0,
                       "shared_blob_projection_drift": 0}}
    expected["semantic_sha256"] = semantic_sha(expected)
    return expected, step83


def first_difference(actual: Any, expected: Any, path: str = "$") -> str | None:
    if type(actual) is not type(expected):
        return path + ":TYPE"
    if isinstance(actual, dict):
        if set(actual) != set(expected):
            return path + ":KEYS"
        for key in sorted(expected):
            difference = first_difference(actual[key], expected[key], path + "." + key)
            if difference: return difference
        return None
    if isinstance(actual, list):
        if len(actual) != len(expected): return path + ":LENGTH"
        for index, (left, right) in enumerate(zip(actual, expected)):
            difference = first_difference(left, right, f"{path}[{index}]")
            if difference: return difference
        return None
    return None if actual == expected else path + ":VALUE"


def validate_candidate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    require(candidate.get("semantic_sha256") == semantic_sha(candidate), "E_GRAPH_SEMANTIC")
    difference = first_difference(candidate, expected)
    require(difference is None, "E_GRAPH_PROJECTION", difference or "")


def negative_controls(expected: dict[str, Any]) -> tuple[int, int]:
    def mutate(name: str, operation: Any) -> None:
        candidate = copy.deepcopy(expected)
        operation(candidate)
        candidate["semantic_sha256"] = semantic_sha(candidate)
        try:
            validate_candidate(candidate, expected)
        except ValidationError:
            return
        raise ValidationError("E_NEGATIVE_FALSE_PASS:" + name)

    controls: list[tuple[str, Any]] = []
    controls.append(("top_extra_key", lambda x: x.update({"extra": 1})))
    controls.append(("wrong_parent", lambda x: x.update({"expected_parent": BASELINE})))
    controls.append(("runtime_authority", lambda x: x["authority"].update({"actual_runtime_order_proven": True})))
    controls.append(("theory_promotion", lambda x: x["authority"].update({"theory_claim_validated": True})))
    controls.append(("input_hash", lambda x: x["inputs"]["step83_state_quantity_flow"].update({"raw_sha256": "0" * 64})))
    controls.append(("release_drop", lambda x: x["source_records"].pop()))
    controls.append(("release_order", lambda x: x["source_records"].reverse()))
    controls.append(("source_path", lambda x: x["source_records"][0].update({"path": "wrong.py"})))
    controls.append(("source_blob", lambda x: x["source_records"][0].update({"blob_oid": "0" * 40})))
    controls.append(("blob_ordinal", lambda x: x["source_records"][0].update({"blob_ordinal": 84})))
    controls.append(("shared_blob_occurrence_ref", lambda x: x["blob_graph_records"][0]["occurrence_refs"][0].update({"path": "wrong.py"})))
    controls.append(("node_owner", lambda x: x["blob_graph_records"][0]["node_records"][0]["anchor"].update({"qualified_owner": "Wrong.owner"})))
    controls.append(("node_anchor_hash", lambda x: x["blob_graph_records"][0]["node_records"][0]["anchor"].update({"normalized_ast_sha256": "0" * 64})))
    controls.append(("edge_caller", lambda x: x["blob_graph_records"][0]["edge_records"][0].update({"caller": "Wrong.owner"})))
    controls.append(("edge_callee", lambda x: x["blob_graph_records"][0]["edge_records"][0].update({"callee": "Wrong.target"})))
    controls.append(("edge_order", lambda x: x["blob_graph_records"][0]["edge_records"][0].update({"lexical_ordinal_in_caller": 999})))
    controls.append(("edge_branch", lambda x: x["blob_graph_records"][0]["edge_records"][0].update({"branch_predicates": ["False"]})))
    controls.append(("edge_state_dependency", lambda x: x["blob_graph_records"][0]["edge_records"][0].update({"argument_expressions": ["wrong"]})))
    dynamic_location = next((gi, ei) for gi, graph in enumerate(expected["blob_graph_records"])
                            for ei, edge in enumerate(graph["edge_records"])
                            if edge["resolution"] != "RESOLVED_INTERNAL")
    controls.append(("dynamic_to_resolved", lambda x, g=dynamic_location[0], e=dynamic_location[1]:
                     x["blob_graph_records"][g]["edge_records"][e].update(
                         {"resolution": "RESOLVED_INTERNAL", "callee": "GraphiteAnodeDischargeDQDV.equilibrium"})))
    path_location = next((gi, si, ci) for gi, graph in enumerate(expected["blob_graph_records"])
                         for si, sequence in enumerate(graph["sequence_records"])
                         for ci, candidate in enumerate(sequence["candidate_paths"])
                         if len(candidate["edge_ids"]) >= 2)
    controls.append(("path_adjacency_skip", lambda x, g=path_location[0], s=path_location[1], c=path_location[2]:
                     x["blob_graph_records"][g]["sequence_records"][s]["candidate_paths"][c]["edge_ids"].pop(0)))
    controls.append(("path_order_reverse", lambda x, g=path_location[0], s=path_location[1], c=path_location[2]:
                     x["blob_graph_records"][g]["sequence_records"][s]["candidate_paths"][c]["edge_ids"].reverse()))
    controls.append(("scenario_drop", lambda x: x["blob_graph_records"][0]["sequence_records"].pop()))
    controls.append(("coverage_drop", lambda x: x["coverage_records"].pop()))
    controls.append(("behavior_drop", lambda x: x["behavior_records"].pop()))
    controls.append(("behavior_condition", lambda x: x["behavior_records"][0].update({"condition": "REST"})))
    option_absent = next(i for i, row in enumerate(expected["behavior_records"])
                         if row["condition"] == "OPTION_OFF"
                         and row["status"] == "ABSENT_IN_FROZEN_SOURCE")
    option_present = next(i for i, row in enumerate(expected["behavior_records"])
                          if row["condition"] == "OPTION_OFF"
                          and row["status"] == "SOURCE_STATIC_PRESENT")
    controls.append(("option_off_backport", lambda x, a=option_absent, p=option_present:
                     x["behavior_records"][a].update(
                         {"status": "SOURCE_STATIC_PRESENT",
                          "evidence": x["behavior_records"][p]["evidence"],
                          "public_sequence_refs": x["behavior_records"][p]["public_sequence_refs"]})))
    present_with_refs = [i for i, row in enumerate(expected["behavior_records"])
                         if row["status"] == "SOURCE_STATIC_PRESENT" and row["public_sequence_refs"]]
    crosswire_pair = next((left, right) for left in present_with_refs for right in present_with_refs
                          if expected["behavior_records"][left]["condition"]
                          != expected["behavior_records"][right]["condition"]
                          and expected["behavior_records"][left]["public_sequence_refs"]
                          != expected["behavior_records"][right]["public_sequence_refs"])
    controls.append(("behavior_sequence_crosswire", lambda x, left=crosswire_pair[0], right=crosswire_pair[1]:
                     x["behavior_records"][left].update(
                         {"public_sequence_refs": x["behavior_records"][right]["public_sequence_refs"]})))
    nonpresent = next(i for i, row in enumerate(expected["behavior_records"])
                      if row["status"] != "SOURCE_STATIC_PRESENT")
    controls.append(("nonpresent_behavior_nonempty_refs",
                     lambda x, i=nonpresent, p=present_with_refs[0]:
                     x["behavior_records"][i].update(
                         {"public_sequence_refs": x["behavior_records"][p]["public_sequence_refs"]})))
    invalid_row = next(i for i, row in enumerate(expected["behavior_records"])
                       if row["condition"] == "INVALID_ROOT"
                       and row["status"] == "SOURCE_STATIC_PRESENT")
    require(len(expected["behavior_records"][invalid_row]["evidence_subcases"]) == 4,
            "E_INVALID_ROOT_SUBCASE_GROUND")
    controls.append(("invalid_root_missing_subcase", lambda x, i=invalid_row:
                     x["behavior_records"][i]["evidence_subcases"].pop()))
    def swap_invalid_subcase_anchors(candidate: dict[str, Any], index: int) -> None:
        subcases = candidate["behavior_records"][index]["evidence_subcases"]
        subcases[0]["raise_anchor"], subcases[1]["raise_anchor"] = (
            subcases[1]["raise_anchor"], subcases[0]["raise_anchor"])
    controls.append(("invalid_root_swapped_subcase_anchor",
                     lambda x, i=invalid_row: swap_invalid_subcase_anchors(x, i)))
    max_iter_rows = [i for i, row in enumerate(expected["behavior_records"])
                     if row["condition"] == "MAX_ITER_EXHAUSTION"
                     and row["status"] == "SOURCE_STATIC_PRESENT"]
    require(bool(max_iter_rows), "E_MAX_ITER_MIDPOINT_GROUND")
    controls.append(("max_iter_wrong_absence", lambda x, i=max_iter_rows[0]:
                     x["behavior_records"][i].update({"status": "ABSENT_IN_FROZEN_SOURCE",
                                                        "evidence": None})))
    controls.append(("max_iter_raise_claim", lambda x, i=max_iter_rows[0]:
                     x["behavior_records"][i].update({"mechanism": "raises on nonconvergence"})))
    controls.append(("dormant_public_injection", lambda x: next(row for graph in x["blob_graph_records"]
                     for row in graph["dormant_records"] if row["status"] == "DORMANT_NO_PUBLIC_CALLER")
                     .update({"status": "PUBLICLY_REACHABLE", "public_inbound_edge_refs": ["fake"]})))
    controls.append(("transfer_false_edge", lambda x: next(row for graph in x["blob_graph_records"]
                     for row in graph["dormant_records"] if row["helper"] == "transfer_apparent_from_equilibrium"
                     and row["defined"]).update({"status": "PUBLICLY_REACHABLE", "public_inbound_edge_refs": ["fake"]})))
    early_graph = next(i for i, graph in enumerate(expected["blob_graph_records"])
                       if graph["feature_contract"]["causal_lowpass_work_grid"])
    point_graphs = [i for i, graph in enumerate(expected["blob_graph_records"])
                    if graph["feature_contract"]["causal_pointwise_sort_inverse"]]
    require(bool(point_graphs), "E_POINTWISE_INV_ORDER_FEATURE")
    point_graph = point_graphs[0]
    no_ratio = next(i for i, graph in enumerate(expected["blob_graph_records"])
                    if not graph["feature_contract"]["causal_ratio_frozen_path"])
    no_pad = next(i for i, graph in enumerate(expected["blob_graph_records"])
                  if not graph["feature_contract"]["causal_pad_re_evaluation"])
    controls.append(("lowpass_interp_omission", lambda x, i=early_graph:
                     x["blob_graph_records"][i]["feature_contract"].update({"causal_lowpass_work_grid": False})))
    controls.append(("pointwise_backport", lambda x, i=early_graph:
                     x["blob_graph_records"][i]["feature_contract"].update({"causal_pointwise_sort_inverse": True})))
    controls.append(("pointwise_inv_sort_substitution", lambda x, i=point_graph:
                     x["blob_graph_records"][i]["feature_contract"].update({"causal_pointwise_sort_inverse": False})))
    controls.append(("ratio_backport", lambda x, i=no_ratio:
                     x["blob_graph_records"][i]["feature_contract"].update({"causal_ratio_frozen_path": True})))
    controls.append(("pad_backport", lambda x, i=no_pad:
                     x["blob_graph_records"][i]["feature_contract"].update({"causal_pad_re_evaluation": True})))
    controls.append(("validation_nonzero", lambda x: x["validation"].update({"false_transfer_helper_edges": 1})))
    passed = 0
    for name, operation in controls:
        mutate(name, operation); passed += 1
    return passed, len(controls)


def strict_json_controls() -> tuple[int, int]:
    controls = [b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'\xef\xbb\xbf{}\n']
    passed = 0
    for raw in controls:
        try: strict_load(raw, "negative")
        except ValidationError: passed += 1
    require(passed == len(controls), "E_JSON_NEGATIVES")
    return passed, len(controls)


def verify_control_documents() -> None:
    for path, expected_hash in CONTROL_PINS.items():
        raw = (ROOT / path).read_bytes()
        require(sha256(raw) == expected_hash, "E_CONTROL_HASH", path)
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    for token in (GATE, "PASS_PENDING_PERSISTENCE", "PENDING_AT_PRECOMMIT_BY_DESIGN",
                  EXPECTED_PARENT, EXPECTED_SUBJECT, PERSISTENCE, "20", "15", "120", "140",
                  "static public-entry", "P0/P1/P2=0/0/0"):
        require(token in result, "E_RESULT_TOKEN", token)
    require("actual runtime order proven: true" not in result.lower(), "E_RESULT_OVERCLAIM")
    parent = (ROOT / PARENT_LEDGER).read_text(encoding="utf-8")
    canonical = (ROOT / CANONICAL_LEDGER).read_text(encoding="utf-8")
    handover = (ROOT / HANDOVER).read_text(encoding="utf-8")
    for text, label in ((parent, "parent"), (canonical, "canonical"), (handover, "handover")):
        require("1af6c06fb5cff2918b846ed74ea213832f04f010" in text,
                "E_STEP83_PERSISTENCE_ROW", label)
        require(GATE in text and EXPECTED_SUBJECT in text and PERSISTENCE in text,
                "E_STEP84_CURRENT_ROW", label)
        require("Step 84" in text and "PASS_PENDING_PERSISTENCE" in text,
                "E_STEP84_POINTER", label)
    require(canonical.count("| 067 |") == 1, "E_CANONICAL_PHASE_ROW")
    require(f"현재 result: `{RESULT_PATH}`" in handover, "E_HANDOVER_CURRENT_RESULT")
    require(f"현재 machine evidence: `{GRAPH_PATH}`" in handover, "E_HANDOVER_CURRENT_MACHINE")


def parse_porcelain(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4, "E_STATUS_LINE")
        require(line[2] == " ", "E_STATUS_SEPARATOR")
        status, path = line[:2], line[3:].replace("\\", "/")
        require(" -> " not in path and path not in result, "E_STATUS_RENAME")
        result[path] = status
    return result


def porcelain_controls() -> tuple[int, int]:
    ordered = [HANDOVER, PARENT_LEDGER, CANONICAL_LEDGER, BUILDER_PATH, VALIDATOR_PATH,
               GRAPH_PATH, RESULT_PATH]
    expected = {path: ("??" if FINAL_STATUS[path] == "A" else " M") for path in ordered}
    fixture = "\n".join(f"{expected[path]} {path}" for path in ordered)
    require(parse_porcelain(fixture) == expected, "E_PORCELAIN_POSITIVE")
    try:
        parse_porcelain(fixture.lstrip())
    except ValidationError as exc:
        require(str(exc) == "E_STATUS_SEPARATOR", "E_PORCELAIN_NEGATIVE_DIAGNOSTIC")
    else:
        raise ValidationError("E_PORCELAIN_NEGATIVE_FALSE_PASS")
    return 2, 2


def parse_name_status(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        status, path = line.split("\t", 1)
        require(status in {"A", "M"} and path not in result, "E_NAME_STATUS")
        result[path] = status
    return result


def parse_ls_tree(text: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        if path in FINAL_SET:
            require(kind == "blob", "E_TREE_KIND")
            result[path] = (mode, oid)
    return result


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    return text.removesuffix(".git").strip("/")


def live_oid(ref: str) -> str:
    text = str(git("ls-remote", "--heads", "origin", ref))
    require("\t" in text, "E_LIVE_REF", ref)
    return text.split("\t", 1)[0]


def repository_refs(expected_tip: str) -> dict[str, Any]:
    record = {"branch": git("rev-parse", "--abbrev-ref", "HEAD"),
              "head": git("rev-parse", "HEAD"),
              "upstream_name": git("rev-parse", "--abbrev-ref", "@{upstream}"),
              "upstream_oid": git("rev-parse", UPSTREAM),
              "active_tracking_oid": git("rev-parse", f"refs/remotes/{UPSTREAM}"),
              "active_live_oid": live_oid(f"refs/heads/{BRANCH}"),
              "origin": canonical_origin(str(git("ls-remote", "--get-url", "origin"))),
              "protected_local_oid": git("show-ref", "--verify", "--hash",
                                         "refs/heads/codex/lib-physics-endgame-v1025_2"),
              "protected_tracking_oid": git("rev-parse",
                                             "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
              "protected_live_oid": live_oid("refs/heads/codex/lib-physics-endgame-v1025_2"),
              "main_local": git("show-ref", "--verify", "--hash", "refs/heads/main", check=False),
              "main_tracking_oid": git("rev-parse", "refs/remotes/origin/main"),
              "main_live_oid": live_oid("refs/heads/main")}
    expected = {"branch": BRANCH, "head": expected_tip, "upstream_name": UPSTREAM,
                "upstream_oid": expected_tip, "active_tracking_oid": expected_tip,
                "active_live_oid": expected_tip, "origin": "github.com/lksz1412/project_anode_fit",
                "protected_local_oid": PROTECTED_TIP, "protected_tracking_oid": PROTECTED_TIP,
                "protected_live_oid": PROTECTED_TIP, "main_local": "",
                "main_tracking_oid": MAIN_TIP, "main_live_oid": MAIN_TIP}
    require(record == expected, "E_REPOSITORY_REFS", repr(record))
    return record


def worktree_status() -> dict[str, str]:
    return parse_porcelain(str(git("status", "--porcelain=v1", "--untracked-files=all")))


def index_snapshot() -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in str(git("ls-files", "-s")).splitlines():
        meta, path = line.split("\t", 1)
        if path in FINAL_SET:
            mode, oid, stage = meta.split()
            require(stage == "0", "E_INDEX_STAGE")
            result[path] = (mode, oid)
    return result


def transaction_seal(expected_tip: str) -> dict[str, Any]:
    return {"repository_refs": repository_refs(expected_tip), "status": worktree_status(),
            "index": index_snapshot(),
            "path_hashes": {path: sha256((ROOT / path).read_bytes())
                            for path in FINAL_PATHS if (ROOT / path).exists()},
            "input_hashes": {path: sha256(bytes(git("show", f"{EXPECTED_PARENT}:{path}", binary=True)))
                             for path in INPUT_PINS}}


def verify_content_worktree() -> None:
    expected = {path: ("??" if FINAL_STATUS[path] == "A" else " M") for path in FINAL_PATHS}
    require(worktree_status() == expected, "E_CONTENT_PATHS", repr(worktree_status()))


def verify_staged() -> None:
    require(git("rev-parse", "HEAD") == EXPECTED_PARENT and git("rev-parse", UPSTREAM) == EXPECTED_PARENT,
            "E_STAGED_PARENT")
    require(parse_name_status(str(git("diff", "--cached", "--name-status", "--no-renames", "HEAD")))
            == FINAL_STATUS, "E_STAGED_PATHS")
    require(git("diff", "--name-only") == "" and git("ls-files", "--others", "--exclude-standard") == "",
            "E_STAGED_DIRTY")
    require(git("diff", "--cached", "--check") == "", "E_DIFF_CHECK")
    index = index_snapshot()
    require(set(index) == FINAL_SET and all(mode == "100644" for mode, _ in index.values()),
            "E_INDEX_MODES")
    for path, (_, oid) in index.items():
        raw = (ROOT / path).read_bytes()
        require(git("show", f":{path}", binary=True) == raw, "E_INDEX_BYTES", path)
        require(git("cat-file", "blob", oid, binary=True) == raw, "E_INDEX_BLOB", path)


def verify_persistence(commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "E_EXPECTED_COMMIT")
    parents = str(git("show", "-s", "--format=%P", commit)).split()
    require(parents == [EXPECTED_PARENT], "E_COMMIT_PARENTS", repr(parents))
    require(git("rev-parse", f"{commit}^") == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(git("show", "-s", "--format=%s", commit) == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT")
    changed = parse_name_status(str(git("diff-tree", "--no-commit-id", "--name-status",
                                        "--no-renames", "-r", f"{commit}^", commit)))
    require(changed == FINAL_STATUS, "E_COMMIT_PATHS")
    tree = parse_ls_tree(str(git("ls-tree", "-r", commit)))
    require(set(tree) == FINAL_SET and all(mode == "100644" for mode, _ in tree.values()),
            "E_COMMIT_MODES")
    require(git("status", "--porcelain") == "", "E_WORKTREE_DIRTY")
    require(git("diff", "--name-only", PROTECTED_TIP, "--", "Claude") == "", "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        require(git("show", f"{commit}:{path}", binary=True) == (ROOT / path).read_bytes(),
                "E_COMMITTED_BYTES", path)


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
        require(re.fullmatch(r"[0-9a-f]{40}", args.expected_commit or "") is not None,
                "E_EXPECTED_COMMIT")
    expected_tip = args.expected_commit if args.verify_persistence else EXPECTED_PARENT
    entry = transaction_seal(expected_tip or "")
    verify_source_policy()
    verify_control_documents()
    actual, nodes, depth = strict_load((ROOT / GRAPH_PATH).read_bytes(), GRAPH_PATH)
    expected, _ = reconstruct_artifact()
    validate_candidate(actual, expected)
    semantic_passed, semantic_total = negative_controls(expected)
    json_passed, json_total = strict_json_controls()
    porcelain_passed, porcelain_total = porcelain_controls()
    if args.content_only: verify_content_worktree()
    elif args.verify_staged: verify_staged()
    else: verify_persistence(args.expected_commit or "")
    terminal = transaction_seal(expected_tip or "")
    require(entry == terminal, "E_TRANSACTION_SEAL")
    print(f"PASS_P067_STEP84_CONTROLS semantic={semantic_passed}/{semantic_total} "
          f"json={json_passed}/{json_total} porcelain={porcelain_passed}/{porcelain_total} "
          f"nodes={nodes} depth={depth}")
    print(f"{PERSISTENCE if args.verify_persistence else GATE} releases=20 blobs=15 "
          f"coverage=120 behavior=140 sequences={actual['coverage']['sequence_records']} determinism=2/2")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(str(exc))
        raise SystemExit(1)
