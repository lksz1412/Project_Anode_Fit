#!/usr/bin/env python3
"""Validate Phase 063 Step 61 frozen-code and isolated-runtime evidence."""

from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any, Iterable


REPO = pathlib.Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1022_phase063/build_phase063_step61_code_runtime_delta.py"
VALIDATOR = pathlib.Path(__file__).resolve()
CODE_ARTIFACT = REPO / "Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json"
RUNTIME_ARTIFACT = REPO / "Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_061_CODE_RUNTIME_DELTA_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "4088f48ca191fdb8abe52e8f4fb10de10f2eeba3"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase063): attest v1022 code runtime delta"
GATE = "PASS_P063_STEP61_CODE_RUNTIME_DELTA_WITH_CONCERNS"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EVIDENCE_BEGIN = "<!-- P063_STEP61_CODE_RUNTIME_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P063_STEP61_CODE_RUNTIME_EVIDENCE_END -->"
TIMEOUT = 300

EXACT_EIGHT = (
    "Codex/work/v1022_phase063/build_phase063_step61_code_runtime_delta.py",
    "Codex/work/v1022_phase063/validate_phase063_step61.py",
    "Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json",
    "Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_063_STEP_061_CODE_RUNTIME_DELTA_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_EIGHT_SET = set(EXACT_EIGHT)

# Filled only after the four result/control documents reach their final
# precommit LF-only bytes. The validator itself is deliberately excluded.
CONTROL_SHA256 = {
    "result": "6eb6e6d3972e15f66996e2b5deb2c21ae5e7142713c17236061e49d498299370",
    "active_ledger": "77b03a0ded1cfcfb32ab60bfb13abc14062658f5543cbb01fe472bb44f4e5add",
    "parent_ledger": "3c6b08cd242c5d33db48741fad22b22325fbe5f6e1d3f08b103afa938470e70d",
    "handover": "319b56af9bc263992ff17aa63c6190452c849f3516ec26062612c3d917c7ad61",
}

# path: (Git blob, SHA-256, bytes, physical lines)
EXPECTED_ENDPOINTS = {
    "Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py": ("7588fe782a027511c2407d9b7caea6ef0ca6c3bd", "d50612413f9f956486594ddafde37776f9592b75e2c8a2266927eaaa23267eaf", 69343, 1152),
    "Claude/docs/v1.0.21/FITTING_GUIDE.md": ("f097793b69237d6f63705cc07708f8a1adbe7192", "f7ca9038e163cfba6313f85e0cd4f3095ac2890a9ff9eb6f8aa4a8cdf12409e1", 24415, 137),
    "Claude/docs/v1.0.21/results/tools_check_structure.py": ("c929b7502f67e8799843744da729e15ee391a473", "7389bfce4c204e1d57801d84d43bb464c5bc918a9e9ad678f353f7880cd670b3", 8313, 165),
    "Claude/docs/v1.0.21/test_gates_v1021.py": ("742506b061d872afdd094781ea2157faae800943", "a8de4944ea304b0106a7cfe0c495f2d7939f9cda74c2eae131fba55dd7e67d36", 22050, 427),
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py": ("c822c4e7ef9b8676e3a9bde675a718169ce79d5b", "a08378b555ca79f92d31bbad506e8c78551a93721cc90d705bf9390b93434783", 92292, 1500),
    "Claude/docs/v1.0.22/FITTING_GUIDE.md": ("f097793b69237d6f63705cc07708f8a1adbe7192", "f7ca9038e163cfba6313f85e0cd4f3095ac2890a9ff9eb6f8aa4a8cdf12409e1", 24415, 137),
    "Claude/docs/v1.0.22/results/tools_check_structure.py": ("e2a87242db1c879d09c426ac390ca8f0aeab8a1b", "a370dd49002013f60d5c351320ca6177d3d53f716b6d22761686e2156c9dc534", 8629, 170),
    "Claude/docs/v1.0.22/test_gates_v1022.py": ("5683f9f6701792f8603ce311a3d1702b341ad150", "b8e501e93eaa2dd2a6c85b1b8f5d5861169ef4e6834e9f5ca8c022caa15e44a1", 33361, 626),
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": ("554425dd566c20314357eddfcf4261517df907ee", "0298bb5fdf47ed5faf2f8301b6d84dc88fd580a69c8e616daa3942d35ceae7cf", 97860, 1585),
    "Claude/docs/v1.0.23/CODE_GUIDE_v23.md": ("28e02a91e3351ded3f218a6b36e670c5f9087157", "660ee229159ad6b6890e0204bef9b9614108caff09d6e7a2c07c1d528c2d0869", 10612, 196),
    "Claude/docs/v1.0.23/FITTING_GUIDE.md": ("f097793b69237d6f63705cc07708f8a1adbe7192", "f7ca9038e163cfba6313f85e0cd4f3095ac2890a9ff9eb6f8aa4a8cdf12409e1", 24415, 137),
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": ("b3b62159919fce6d4c4665b234d74456fa0fcf10", "279b711ef3c33b046136f7b962c76f65ccacbaca369f571ab8f3ed50524f86dc", 2866, 68),
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py": ("07a07aebd981b4f57bed352165bdd236c6b0a408", "2f00abff807425d6aa24a8caed83475f332c3365af3723d2a159455c6e37df85", 8523, 156),
    "Claude/docs/v1.0.23/results/tools_check_structure.py": ("e2a87242db1c879d09c426ac390ca8f0aeab8a1b", "a370dd49002013f60d5c351320ca6177d3d53f716b6d22761686e2156c9dc534", 8629, 170),
    "Claude/docs/v1.0.23/test_gates_v1023.py": ("a636c6f21d97f8a1af57b61a6e4afda974b86dca", "78205fed4f6ed9ff731e11eddf14f1e871ef15759cb75344f098b8d014173832", 33361, 626),
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": ("cf330bfc14e0291474ea9490a5b206c2f060a319", "1417277231ea795515037f470ec160e5077e04d8ab351df7e85c6467671fcef4", 6502, 128),
}

RUNTIME_COPY_PATHS = {
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
}

EXPECTED_SYMBOL_COUNTS = {
    "Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py": 41,
    "Claude/docs/v1.0.21/results/tools_check_structure.py": 7,
    "Claude/docs/v1.0.21/test_gates_v1021.py": 10,
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py": 51,
    "Claude/docs/v1.0.22/results/tools_check_structure.py": 7,
    "Claude/docs/v1.0.22/test_gates_v1022.py": 15,
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": 54,
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": 5,
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py": 9,
    "Claude/docs/v1.0.23/results/tools_check_structure.py": 7,
    "Claude/docs/v1.0.23/test_gates_v1023.py": 15,
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": 6,
}

EXPECTED_FINDINGS = {f"P063-S61-F{number:03d}" for number in range(1, 14)}
EXPECTED_CONCORDANCE = {f"P063-CONC-{number:03d}" for number in range(1, 11)}
EXPECTED_STATIC_CONTRACTS = {f"P063-STATIC-{number:03d}" for number in range(1, 8)}
EXPECTED_OFFICIAL = {
    (runtime, stem): expected
    for runtime in ("3.12", "3.14")
    for stem, expected in (
        ("V1021", "PASS"), ("V1022", "PASS"), ("V1023", "PASS"),
        ("V1023-SC", "PASS"), ("V1023-P1", "PASS"),
        ("V1023-CURVE-QA", "EXPECTED_FAIL_NONPORTABLE_PATH_OR_OPTIONAL_DEPENDENCY"),
    )
}

# Populated from independently replayed, environment-pinned Step 61 rows after
# every semantic field is finalized. These are not artifact self-hashes.
EXPECTED_FINDING_SUMMARY_SHA256 = {
    "P063-S61-F001": "675c00ec66339942a6475a74039275e0d7006b6333e3f7f4824f3d658172368c",
    "P063-S61-F002": "009570c47d260f67777f864ee3c6e15022643321c191f63dda801c16b8a1a2a2",
    "P063-S61-F003": "3ed5a55baa4f3fd052ede199562dd72fc468288dff8db45e519a3dbe67ebdebc",
    "P063-S61-F004": "1459160af810f198a0bbf093f53f50c2196ab5984a7e82fd3f49dbfeabd01b33",
    "P063-S61-F005": "e570a36935c6bc375a1ccbd031fd277ead094abf64a8ac01645a381bea8c30e3",
    "P063-S61-F006": "e4c7ae2ef88f3e138f9d751ce7bbdb9c68bd5e3368ba1af7bee25ecceb21bc1e",
    "P063-S61-F007": "3635c24883fa5fce97585e6ad386b73294a3003179f03595e8d6a9263721c4a1",
    "P063-S61-F008": "f19d0dd40e924347857e9f736ecc9f7940f1e0108c2e29cc745c2c4351e4f9c2",
    "P063-S61-F009": "3d90f1ab738642157234c223bbfddbb835984a75ba4f8b39e34022ed309dc47a",
    "P063-S61-F010": "985377fab62f0937a206756109a20a010a9b00ab2a00bfc9ca3ec0a1786aaf35",
    "P063-S61-F011": "ccd6e1a4728887ff6113c712be1bd42ca54c17a13b1d9bdd83ffbdfaf0930baa",
    "P063-S61-F012": "16e617f2d9e3faaa4dc7c74a6f42c02ba0a883210d98c27b2f8ce867e07f5d37",
    "P063-S61-F013": "50f6a335b56f958c056951079fc6e82d28e12d87d03ceb97567cccd0bbf5ec05",
}
EXPECTED_OFFICIAL_IO_SHA256 = {
    "P063-OFFICIAL-V1021-312": "6b4d2a8e4e335013ca7789e19e6ea96d80c8b3cc32a960dabbca3633f25a82ba",
    "P063-OFFICIAL-V1022-312": "75b012906d7bb309cde3d21c7854ae4d23d0e5f3834cb7075033f6bb88717a32",
    "P063-OFFICIAL-V1023-312": "75b012906d7bb309cde3d21c7854ae4d23d0e5f3834cb7075033f6bb88717a32",
    "P063-OFFICIAL-V1023-SC-312": "2a5318301f3e379e1014c062dd9b598662d0eee323b670e3b24bee05b22b7804",
    "P063-OFFICIAL-V1023-P1-312": "845cfc61158dfa5b67dc0a5e1681e3c71b1195da0824636aec3d7f9b64822930",
    "P063-OFFICIAL-V1023-CURVE-QA-312": "2cbb0b8c52513edc8ee894014d95122ee1f0e89d1af639a56f80e85456bdd58f",
    "P063-OFFICIAL-V1021-314": "6b4d2a8e4e335013ca7789e19e6ea96d80c8b3cc32a960dabbca3633f25a82ba",
    "P063-OFFICIAL-V1022-314": "75b012906d7bb309cde3d21c7854ae4d23d0e5f3834cb7075033f6bb88717a32",
    "P063-OFFICIAL-V1023-314": "75b012906d7bb309cde3d21c7854ae4d23d0e5f3834cb7075033f6bb88717a32",
    "P063-OFFICIAL-V1023-SC-314": "2a5318301f3e379e1014c062dd9b598662d0eee323b670e3b24bee05b22b7804",
    "P063-OFFICIAL-V1023-P1-314": "845cfc61158dfa5b67dc0a5e1681e3c71b1195da0824636aec3d7f9b64822930",
    "P063-OFFICIAL-V1023-CURVE-QA-314": "2a0a08f2e4d319d513e21b9eed382c59f5c76f607844d99b8b07d1e578b2034a",
}
EXPECTED_PROBE_RESULTS_SHA256 = {
    "3.12": "98e5d1be970da20132225438767b390503ec37ef33a0b6ad72fb4d6f01b44627",
    "3.14": "98e5d1be970da20132225438767b390503ec37ef33a0b6ad72fb4d6f01b44627",
}
EXPECTED_PROBE_PROGRAM_SHA256 = "197fbfefbe43f7589838e46e3ab726b6ff9efa82ab42c4a288bacdee202789ab"


class ValidationError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise ValidationError(f"non-finite JSON constant: {value}")


def strict_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValidationError(f"non-finite JSON float: {value}")
    return result


def strict_pairs(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def traverse(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(1 + traverse(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(traverse(item) for item in value)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError("non-finite value in traversal")
    return 1


def strict_load_text(text: str) -> tuple[Any, int]:
    value = json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_constant, parse_float=strict_float)
    return value, traverse(value)


def strict_load(path: pathlib.Path) -> tuple[Any, int]:
    return strict_load_text(path.read_text(encoding="utf-8"))


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def semantic_digest(data: dict[str, Any]) -> str:
    projected = copy.deepcopy(data)
    projected.pop("semantic_sha256", None)
    return digest(compact(projected))


def run(args: list[str], *, cwd: pathlib.Path = REPO, timeout: int = TIMEOUT,
        env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)


def git_bytes(*args: str, check: bool = True) -> bytes:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise ValidationError(f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.decode('utf-8', errors='replace').strip()}")
    return proc.stdout


def git_text(*args: str, check: bool = True) -> str:
    return git_bytes(*args, check=check).decode("utf-8", "strict").strip()


def git_paths(*args: str) -> set[str]:
    return {item.decode("utf-8", "strict").replace("\\", "/") for item in git_bytes(*args).split(b"\0") if item}


def ref_hash(ref: str) -> str | None:
    value = git_text("show-ref", "--verify", "--hash", ref, check=False)
    return value or None


def remote_head(branch: str) -> str:
    ref = f"refs/heads/{branch}"
    rows = [line.split() for line in git_text("ls-remote", "--heads", "origin", ref).splitlines() if line.strip()]
    if len(rows) != 1 or rows[0][1] != ref:
        raise ValidationError(f"remote head cardinality: {branch}: {rows}")
    return rows[0][0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def exact_keys(value: Any, keys: set[str], message: str) -> None:
    require(isinstance(value, dict) and set(value) == keys, f"{message} keys")


def replay_version(path: str) -> str:
    match = re.search(r"/v(1\.0\.2[123])/", path)
    require(match is not None, f"endpoint version path {path}")
    return match.group(1)


def replay_role(path: str) -> str:
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
    raise ValidationError(f"unclassified endpoint {path}")


@functools.lru_cache(maxsize=None)
def frozen_raw(path: str) -> bytes:
    return git_bytes("show", f"{BASELINE}:{path}")


@functools.lru_cache(maxsize=None)
def frozen_blob(path: str) -> str:
    return git_text("rev-parse", f"{BASELINE}:{path}")


@functools.lru_cache(maxsize=None)
def frozen_lines(path: str) -> tuple[str, ...]:
    return tuple(frozen_raw(path).decode("utf-8", "strict").splitlines())


class ReplayStripDocstrings(ast.NodeTransformer):
    def strip(self, node: ast.AST) -> ast.AST:
        body = getattr(node, "body", None)
        if (isinstance(body, list) and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)):
            node.body = body[1:]
        return node

    def visit_Module(self, node: ast.Module) -> ast.AST:
        self.generic_visit(node)
        return self.strip(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        self.generic_visit(node)
        return self.strip(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        self.generic_visit(node)
        return self.strip(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
        self.generic_visit(node)
        return self.strip(node)


def replay_ast_dump(node: ast.AST) -> str:
    try:
        return ast.dump(node, include_attributes=False, show_empty=True)
    except TypeError:
        return ast.dump(node, include_attributes=False)


def replay_ast_hash(node: ast.AST) -> str:
    clean = ReplayStripDocstrings().visit(copy.deepcopy(node))
    ast.fix_missing_locations(clean)
    return digest(replay_ast_dump(clean).encode())


def replay_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    defaults: dict[str, str] = {}
    offset = len(positional) - len(args.defaults)
    for index, default in enumerate(args.defaults):
        defaults[positional[offset + index].arg] = ast.unparse(default)
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        if default is not None:
            defaults[arg.arg] = ast.unparse(default)
    return {
        "posonly": [arg.arg for arg in args.posonlyargs],
        "positional": [arg.arg for arg in args.args],
        "vararg": None if args.vararg is None else args.vararg.arg,
        "kwonly": [arg.arg for arg in args.kwonlyargs],
        "kwarg": None if args.kwarg is None else args.kwarg.arg,
        "defaults": defaults,
    }


def replay_exception(node: ast.AST | None) -> str:
    if node is None:
        return "RERAISE"
    target = node.func if isinstance(node, ast.Call) else node
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return replay_ast_dump(target)


def replay_ast_inventory(text: str) -> dict[str, Any]:
    tree = ast.parse(text)
    symbols: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.scope: list[str] = []

        def name(self, local: str) -> str:
            return ".".join((*self.scope, local))

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            symbols.append({
                "kind": "CLASS", "qualified_name": self.name(node.name),
                "start_line": node.lineno, "end_line": node.end_lineno,
                "bases": [ast.unparse(base) for base in node.bases],
                "code_ast_sha256": replay_ast_hash(node),
            })
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            symbols.append({
                "kind": "ASYNC_FUNCTION" if isinstance(node, ast.AsyncFunctionDef) else "FUNCTION",
                "qualified_name": self.name(node.name), "start_line": node.lineno,
                "end_line": node.end_lineno, "signature": replay_signature(node),
                "code_ast_sha256": replay_ast_hash(node),
            })
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        visit_FunctionDef = function
        visit_AsyncFunctionDef = function

    Visitor().visit(tree)
    parent: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node
    guards: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    imports: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            owner = "<module>"
            cursor: ast.AST | None = node
            while cursor in parent:
                cursor = parent[cursor]
                if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner = cursor.name
                    break
            guards.append({"line": node.lineno, "end_line": node.end_lineno,
                           "owner": owner, "exception": replay_exception(node.exc)})
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "warn":
            warnings.append({"line": node.lineno, "end_line": node.end_lineno})
        if isinstance(node, ast.Import):
            imports.append({"line": node.lineno, "modules": [alias.name for alias in node.names]})
        elif isinstance(node, ast.ImportFrom):
            imports.append({"line": node.lineno, "modules": [node.module or ""]})
    return {
        "module_code_ast_sha256": replay_ast_hash(tree),
        "symbols": sorted(symbols, key=lambda row: (row["start_line"], row["qualified_name"])),
        "guards": sorted(guards, key=lambda row: row["line"]),
        "warning_calls": sorted(warnings, key=lambda row: row["line"]),
        "imports": sorted(imports, key=lambda row: row["line"]),
    }


@functools.lru_cache(maxsize=None)
def replay_endpoint(path: str, number: int) -> dict[str, Any]:
    raw = frozen_raw(path)
    text = raw.decode("utf-8", "strict")
    lines = text.splitlines()
    row: dict[str, Any] = {
        "endpoint_id": f"P063-END-{number:03d}", "path": path,
        "version": replay_version(path), "role": replay_role(path),
        "git_blob": frozen_blob(path), "sha256": digest(raw),
        "bytes": len(raw), "lines": len(lines),
        "nonblank_lines": sum(bool(line.strip()) for line in lines),
        "utf8_decode": "PASS", "full_blob_traversal": True,
        "line_ending": "LF" if b"\r" not in raw else "CONTAINS_CR",
    }
    if path.endswith(".py"):
        row["ast"] = replay_ast_inventory(text)
    else:
        row["headings"] = [
            {"line": index, "text": line}
            for index, line in enumerate(lines, 1) if line.startswith("#")
        ]
        row["code_identifiers"] = sorted(set(re.findall(r"`([A-Za-z_][A-Za-z0-9_.]*)`", text)))
    return row


def replay_delta(left: dict[str, Any], right: dict[str, Any], delta_id: str) -> dict[str, Any]:
    a = {row["qualified_name"]: row for row in left["ast"]["symbols"]}
    b = {row["qualified_name"]: row for row in right["ast"]["symbols"]}
    common = sorted(set(a) & set(b))
    changed = [name for name in common if a[name]["code_ast_sha256"] != b[name]["code_ast_sha256"]]
    signature_changed = [name for name in common if a[name].get("signature") != b[name].get("signature")]
    return {
        "delta_id": delta_id, "left_endpoint_id": left["endpoint_id"],
        "right_endpoint_id": right["endpoint_id"], "left_path": left["path"],
        "right_path": right["path"], "same_blob": left["git_blob"] == right["git_blob"],
        "added_symbols": sorted(set(b) - set(a)), "removed_symbols": sorted(set(a) - set(b)),
        "changed_symbol_code": changed, "changed_signatures": signature_changed,
        "unchanged_common_symbols": sorted(set(common) - set(changed)),
    }


def verify_span(span: dict[str, Any], by_path: dict[str, dict[str, Any]], message: str) -> None:
    path = span.get("path")
    require(path in by_path, f"{message} path")
    endpoint = by_path[path]
    require(span.get("endpoint_id") == endpoint["endpoint_id"] and span.get("git_blob") == endpoint["git_blob"], f"{message} identity")
    start, end = span.get("start_line"), span.get("end_line")
    require(isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= endpoint["lines"], f"{message} bounds")
    if "symbol" in span:
        exact_keys(span, {"endpoint_id", "path", "git_blob", "symbol", "start_line", "end_line", "code_ast_sha256"}, message)
        symbols = {row["qualified_name"]: row for row in endpoint["ast"]["symbols"]}
        symbol = symbols.get(span["symbol"])
        require(symbol is not None, f"{message} symbol")
        require((start, end, span.get("code_ast_sha256")) == (symbol["start_line"], symbol["end_line"], symbol["code_ast_sha256"]), f"{message} symbol replay")
    else:
        exact_keys(span, {"endpoint_id", "path", "git_blob", "start_line", "end_line", "text_sha256"}, message)
        text = frozen_lines(path)
        payload = ("\n".join(text[start - 1:end]) + "\n").encode("utf-8")
        require(span.get("text_sha256") == digest(payload), f"{message} literal digest")


@functools.lru_cache(maxsize=None)
def replay_assignment_by_path(path: str, name: str) -> dict[str, Any]:
    endpoint = replay_endpoint(path, list(EXPECTED_ENDPOINTS).index(path) + 1)
    text = frozen_raw(path).decode("utf-8")
    tree = ast.parse(text, filename=endpoint["path"])
    matches: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            matches.append(node)
    require(len(matches) == 1, f"static assignment denominator {endpoint['path']} {name}")
    node = matches[0]
    if name == "SI_CASE_SETS":
        require(isinstance(node.value, ast.Dict), "SI_CASE_SETS literal")
        value = {
            ast.literal_eval(key): val.id
            for key, val in zip(node.value.keys, node.value.values)
            if key is not None and isinstance(val, ast.Name)
        }
        require(len(value) == len(node.value.values), "SI_CASE_SETS names")
    else:
        value = ast.literal_eval(node.value)
    lines = text.splitlines()
    payload = ("\n".join(lines[node.lineno - 1:node.end_lineno]) + "\n").encode("utf-8")
    return {
        "name": name, "value": value, "endpoint_id": endpoint["endpoint_id"],
        "path": endpoint["path"], "git_blob": endpoint["git_blob"],
        "start_line": node.lineno, "end_line": node.end_lineno,
        "text_sha256": digest(payload),
    }


def replay_assignment(endpoint: dict[str, Any], name: str) -> dict[str, Any]:
    return replay_assignment_by_path(endpoint["path"], name)


def validate_header(data: dict[str, Any], kind: str) -> None:
    require(data.get("artifact_kind") == kind, f"{kind} artifact kind")
    require(data.get("schema_version") == 1, f"{kind} schema")
    require(data.get("phase") == 63 and data.get("step") == 61, f"{kind} phase/step")
    require(data.get("generated_date") == "2026-08-29", f"{kind} date")
    require(data.get("baseline_commit") == BASELINE, f"{kind} baseline")
    require(data.get("expected_parent") == EXPECTED_PARENT, f"{kind} parent")
    require(data.get("semantic_sha256") == semantic_digest(data), f"{kind} semantic digest")
    contract = data.get("result_first_contract", {})
    exact_keys(contract, {"gate", "containing_commit", "postcommit_terminal"}, f"{kind} result contract")
    require(contract.get("gate") == GATE, f"{kind} result gate")
    require(contract.get("containing_commit") == "PENDING_AT_PRECOMMIT_BY_DESIGN", f"{kind} containing sentinel")
    require(contract.get("postcommit_terminal") == "PENDING_AT_PRECOMMIT_BY_DESIGN", f"{kind} terminal sentinel")


def validate_code(data: dict[str, Any]) -> None:
    validate_header(data, "PHASE_063_V1022_CODE_DELTA_MATRIX")
    exact_keys(data, {
        "artifact_kind", "schema_version", "phase", "step", "generated_date",
        "baseline_commit", "expected_parent", "expected_subject", "endpoint_predicate",
        "endpoints", "shared_blob_groups", "symbol_deltas", "theory_code_concordance",
        "static_contracts", "findings", "finding_summary", "counts", "authority_boundary",
        "result_first_contract", "semantic_sha256",
    }, "code artifact")
    require(data.get("expected_subject") == SUBJECT, "code expected subject")
    require(data.get("endpoint_predicate") == "all *.py plus filenames containing GUIDE under exact v1.0.21/v1.0.22/v1.0.23 frozen directories", "endpoint predicate")
    require(data.get("counts") == {
        "ast_symbols": 227, "endpoint_occurrences": 16, "findings": 13, "guide_endpoints": 4,
        "official_gates": 4, "production_modules": 3, "python_endpoints": 12,
        "static_contracts": 7, "theory_code_rows": 10, "unique_blobs": 13,
    }, "code counts")
    rows = data.get("endpoints")
    require(isinstance(rows, list) and len(rows) == 16, "endpoint cardinality")
    by_path = {row.get("path"): row for row in rows if isinstance(row, dict)}
    require(set(by_path) == set(EXPECTED_ENDPOINTS) and len(by_path) == len(rows), "endpoint path denominator")
    replayed = [replay_endpoint(path, number) for number, path in enumerate(EXPECTED_ENDPOINTS, 1)]
    require(rows == replayed, "full independent endpoint projection")
    require(sum(len(row.get("ast", {}).get("symbols", [])) for row in replayed) == 227, "recursive AST denominator")

    groups: dict[str, list[str]] = {}
    for row in replayed:
        groups.setdefault(row["git_blob"], []).append(row["path"])
    expected_shared = [
        {"git_blob": blob, "paths": paths, "occurrences": len(paths)}
        for blob, paths in sorted(groups.items()) if len(paths) > 1
    ]
    require(data.get("shared_blob_groups") == expected_shared, "full shared-blob projection")

    replay_by_path = {row["path"]: row for row in replayed}
    expected_deltas = [
        replay_delta(replay_by_path["Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py"], replay_by_path["Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py"], "P063-DELTA-PROD-21-22"),
        replay_delta(replay_by_path["Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py"], replay_by_path["Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py"], "P063-DELTA-PROD-22-23"),
        replay_delta(replay_by_path["Claude/docs/v1.0.21/test_gates_v1021.py"], replay_by_path["Claude/docs/v1.0.22/test_gates_v1022.py"], "P063-DELTA-GATE-21-22"),
        replay_delta(replay_by_path["Claude/docs/v1.0.22/test_gates_v1022.py"], replay_by_path["Claude/docs/v1.0.23/test_gates_v1023.py"], "P063-DELTA-GATE-22-23"),
    ]
    require(data.get("symbol_deltas") == expected_deltas, "full independent symbol delta projection")

    expected_concordance = {
        "P063-CONC-001": (["P063-DER-007"], ["func_ksi_eq", "GraphiteAnodeDischargeDQDV.equilibrium"], "CONCORDANT_STATIC", "equilibrium logistic derivative path"),
        "P063-CONC-002": (["P063-DER-009"], ["_causal_memory_pointwise", "GraphiteAnodeDischargeDQDV.dqdv"], "CONCORDANT_STATIC_WITH_FROZEN_LOCAL_APPROXIMATION", "causal memory is implemented; local state-dependent kinetics is frozen"),
        "P063-CONC-003": (["P063-DER-014"], ["BlendedAnodeDQDV.__init__", "BlendedAnodeDQDV.solve_U_oc", "GraphiteAnodeDischargeDQDV.solve_U_oc"], "CONDITIONAL_CONCORDANCE_STATIC_WITH_DOMAIN_GUARD_GAP", "pooled common-potential charge balance has a unique monotone root only under the unguarded per-transition domain Q_j>0 and n_j(T)>0"),
        "P063-CONC-004": (["P063-DER-015"], ["BlendedAnodeDQDV.from_wt"], "FORMULA_CONCORDANT_BASIS_UNVERIFIED", "mass-to-capacity algebra matches; capacity/utilization/ICE basis is not closed"),
        "P063-CONC-005": (["P063-DER-016", "P063-DER-017"], ["BlendedAnodeDQDV.__init__", "BlendedAnodeDQDV.plastic_hysteresis_loop"], "HOOK_ONLY_PATH_CLOSURE_UNSUPPORTED", "static stress offset exists; plastic history closure raises NotImplementedError"),
        "P063-CONC-006": (["P063-DER-018"], ["BlendedAnodeDQDV.dqdv", "BlendedAnodeDQDV.nonadditive_correction"], "FINITE_RATE_CURRENT_PARTITION_UNSUPPORTED", "both hosts receive the same full current; nonadditive correction raises NotImplementedError"),
        "P063-CONC-007": (["P063-DER-019", "P063-DER-020"], ["GraphiteAnodeDischargeDQDV.curve", "func_L_q"], "CONFLICT_HOUR_TO_SECOND_CONVERSION_MISSING", "curve maps c_rate*Q_cell directly into an SI kinetic prefactor without division by 3600"),
        "P063-CONC-008": (["P063-DER-021", "P063-DER-022"], ["GraphiteAnodeDischargeDQDV._resolve_lag_length"], "CONCORDANT_APPROXIMATION_ONLY", "cut/cap and frozen-local lag resolver are explicit approximation operators"),
        "P063-CONC-009": (["P063-DER-023"], ["GraphiteAnodeDischargeDQDV.reversible_heat", "GraphiteAnodeDischargeDQDV.irreversible_heat"], "CONCORDANT_STATIC_WITH_SIGN_SCOPE", "separate reversible and lumped irreversible exits exist; branch dissipation closure remains outside this row"),
        "P063-CONC-010": (["P063-DER-025"], ["LCOCathodeDQDV._effective_dS_rxn"], "FROZEN_REFERENCE_APPROXIMATION", "electronic entropy is evaluated at fixed T_ref and x_center, not local composition-temperature closure"),
    }
    concordance = data.get("theory_code_concordance", [])
    require({row.get("concordance_id") for row in concordance} == EXPECTED_CONCORDANCE and len(concordance) == 10, "concordance ids")
    for row in concordance:
        exact_keys(row, {"concordance_id", "theory_derivation_ids", "code_spans", "state", "basis", "authority", "external_science"}, f"concordance {row.get('concordance_id')}")
        derivations, symbols, state, basis = expected_concordance[row["concordance_id"]]
        require(row["theory_derivation_ids"] == derivations and row["state"] == state and row["basis"] == basis, f"concordance semantics {row['concordance_id']}")
        require([span.get("symbol") for span in row["code_spans"]] == symbols, f"concordance symbol join {row['concordance_id']}")
        for index, span in enumerate(row["code_spans"]):
            verify_span(span, by_path, f"concordance {row['concordance_id']} span {index}")
        require(row["authority"] == "STATIC_CODE_CONCORDANCE_ONLY" and row["external_science"] is False, f"concordance authority {row['concordance_id']}")

    prod22_path = "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py"
    prod23_path = "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py"
    static_expected = {
        "P063-STATIC-001": ("DEMO_SET_LITERALS_EXACT", "Exact U/w/Q demo literals and selector-to-constant mapping; these remain labelled placeholders, not material truth.", [(path, name) for path in (prod22_path, prod23_path) for name in ("SI_ELEMENTAL_LIT", "SIOX_LIT", "SIC_LIT", "SI_CASE_SETS")]),
        "P063-STATIC-002": ("SPECIFIC_CAPACITY_DEFAULTS_EXACT", "Exact case-specific q_Si and graphite q_gr defaults used by from_wt; mixed basis remains an open finding.", [(path, name) for path in (prod22_path, prod23_path) for name in ("SI_SPECIFIC_CAPACITY", "GRAPHITE_SPECIFIC_CAPACITY")]),
        "P063-STATIC-003": ("FSI_ZERO_LIMIT_PATH_EXACT", "Constructor scaling path that removes all positive-Q silicon transitions when f_Si=0.", [(prod22_path, "BlendedAnodeDQDV.__init__"), (prod23_path, "BlendedAnodeDQDV.__init__")]),
        "P063-STATIC-004": ("SINGLE_BACKGROUND_OWNER_PATH_EXACT", "Constructor assigns Cbg to graphite and zero to the silicon host.", [(prod22_path, "BlendedAnodeDQDV.__init__"), (prod23_path, "BlendedAnodeDQDV.__init__")]),
        "P063-STATIC-005": ("GS1_UNSUPPORTED_PATH_EXACT", "GS-1 plastic closure is an explicit NotImplementedError boundary.", [(prod22_path, "BlendedAnodeDQDV.plastic_hysteresis_loop"), (prod23_path, "BlendedAnodeDQDV.plastic_hysteresis_loop")]),
        "P063-STATIC-006": ("GS2_UNSUPPORTED_PATH_EXACT", "GS-2 nonadditive finite-rate closure is an explicit NotImplementedError boundary.", [(prod22_path, "BlendedAnodeDQDV.nonadditive_correction"), (prod23_path, "BlendedAnodeDQDV.nonadditive_correction")]),
        "P063-STATIC-007": ("FROM_WT_GUARD_AND_MAPPING_PATH_EXACT", "Mass-fraction guard and mass-to-capacity mapping path.", [(prod22_path, "BlendedAnodeDQDV.from_wt"), (prod23_path, "BlendedAnodeDQDV.from_wt")]),
    }
    static_rows = data.get("static_contracts", [])
    require({row.get("static_contract_id") for row in static_rows} == EXPECTED_STATIC_CONTRACTS and len(static_rows) == 7, "static contract ids")
    for row in static_rows:
        cid = row["static_contract_id"]
        exact_keys(row, {"static_contract_id", "state", "occurrences", "basis", "authority", "external_science"}, f"static contract {cid}")
        state, basis, occurrence_spec = static_expected[cid]
        require(row["state"] == state and row["basis"] == basis, f"static state/basis {cid}")
        require(row["authority"] == "EXACT_FROZEN_STATIC_CONTRACT_ONLY" and row["external_science"] is False, f"static authority {cid}")
        require(len(row["occurrences"]) == len(occurrence_spec), f"static occurrence denominator {cid}")
        for index, occurrence in enumerate(row["occurrences"]):
            expected_path, expected_locator = occurrence_spec[index]
            require(occurrence.get("path") == expected_path, f"static occurrence path {cid}/{index}")
            if "name" in occurrence:
                require(occurrence["name"] == expected_locator, f"static assignment name {cid}/{index}")
                endpoint = by_path.get(occurrence.get("path"))
                require(endpoint is not None and occurrence == replay_assignment(endpoint, occurrence["name"]), f"static assignment replay {cid}/{index}")
            else:
                require(occurrence.get("symbol") == expected_locator, f"static occurrence symbol {cid}/{index}")
                verify_span(occurrence, by_path, f"static span {cid}/{index}")
    static_by_id = {row["static_contract_id"]: row for row in static_rows}
    require([row["name"] for row in static_by_id["P063-STATIC-001"]["occurrences"]] == ["SI_ELEMENTAL_LIT", "SIOX_LIT", "SIC_LIT", "SI_CASE_SETS"] * 2, "demo assignment order")
    require([row["name"] for row in static_by_id["P063-STATIC-002"]["occurrences"]] == ["SI_SPECIFIC_CAPACITY", "GRAPHITE_SPECIFIC_CAPACITY"] * 2, "capacity assignment order")

    require(data.get("finding_summary") == {"P0": 3, "P1": 4, "P2": 6}, "finding priorities")
    findings = data.get("findings", [])
    require({row.get("finding_id") for row in findings} == EXPECTED_FINDINGS and len(findings) == 13, "finding ids")
    require(Counter(row.get("priority") for row in findings) == Counter({"P0": 3, "P1": 4, "P2": 6}), "finding priority rows")
    finding_fields = {
        "P063-S61-F001": ("P0", "Phase 076", ["P063-RUN-SI-TIME-22", "P063-RUN-SI-TIME-23"], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "GraphiteAnodeDischargeDQDV.curve"), ("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "func_L_q")]),
        "P063-S61-F002": ("P0", "Phase 080", ["P063-RUN-CURRENT-PARTITION-22", "P063-RUN-CURRENT-PARTITION-23"], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "BlendedAnodeDQDV.dqdv"), ("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "BlendedAnodeDQDV.nonadditive_correction")]),
        "P063-S61-F003": ("P0", "Phase 071/080", ["P063-RUN-FROM-WT-22", "P063-RUN-FROM-WT-23"], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "BlendedAnodeDQDV.from_wt"), ("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", (1049, 1058))]),
        "P063-S61-F004": ("P1", "Phase 076/081", ["P063-RUN-MISSING-KINETICS-22", "P063-RUN-MISSING-KINETICS-23"], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "GraphiteAnodeDischargeDQDV._resolve_lag_length")]),
        "P063-S61-F005": ("P1", "Phase 081", ["P063-OFFICIAL-V1023-CURVE-QA-312", "P063-OFFICIAL-V1023-CURVE-QA-314"], [("Claude/docs/v1.0.23/results/qa_images/curve_qa.py", (8, 9)), ("Claude/docs/v1.0.23/results/qa_images/curve_qa.py", (14, 14)), ("Claude/docs/v1.0.23/results/qa_images/curve_qa.py", (109, 109))]),
        "P063-S61-F006": ("P1", "Phase 081", ["P063-RUN-ROOT-22", "P063-RUN-ROOT-23"], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "GraphiteAnodeDischargeDQDV.solve_U_oc")]),
        "P063-S61-F007": ("P2", "Phase 081", [], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", (3, 3))]),
        "P063-S61-F008": ("P2", "Phase 081", ["P063-RUN-FROM-WT-22", "P063-RUN-FROM-WT-23"], [("Claude/docs/v1.0.22/test_gates_v1022.py", (519, 520)), ("Claude/docs/v1.0.23/test_gates_v1023.py", (519, 520))]),
        "P063-S61-F009": ("P2", "Phase 081", [], [("Claude/docs/v1.0.23/CODE_GUIDE_v23.md", (189, 189))]),
        "P063-S61-F010": ("P2", "Phase 081", [], [("Claude/docs/v1.0.21/FITTING_GUIDE.md", (1, 5)), ("Claude/docs/v1.0.22/FITTING_GUIDE.md", (1, 5)), ("Claude/docs/v1.0.23/FITTING_GUIDE.md", (1, 5))]),
        "P063-S61-F011": ("P2", "Phase 081", ["P063-OFFICIAL-V1023-P1-312", "P063-OFFICIAL-V1023-P1-314"], [("Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py", (51, 68))]),
        "P063-S61-F012": ("P2", "Phase 081", [], [("Claude/docs/v1.0.21/test_gates_v1021.py", (23, 23)), ("Claude/docs/v1.0.22/test_gates_v1022.py", (35, 35)), ("Claude/docs/v1.0.23/test_gates_v1023.py", (35, 35))]),
        "P063-S61-F013": ("P1", "Phase 081", ["P063-RUN-ROOT-DOMAIN-22", "P063-RUN-ROOT-DOMAIN-23"], [("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "GraphiteAnodeDischargeDQDV.__init__"), ("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "GraphiteAnodeDischargeDQDV.solve_U_oc"), ("Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "BlendedAnodeDQDV.__init__")]),
    }
    for row in findings:
        fid = row["finding_id"]
        exact_keys(row, {"finding_id", "priority", "status", "summary", "evidence", "runtime_probe_ids", "owner", "external_truth_validated"}, f"finding {fid}")
        priority, owner, probes, evidence_spec = finding_fields[fid]
        require((row["priority"], row["status"], row["owner"], row["runtime_probe_ids"], row["external_truth_validated"]) == (priority, "OPEN_ROUTED", owner, probes, False), f"finding fields {fid}")
        require(EXPECTED_FINDING_SUMMARY_SHA256.get(fid) == digest(row["summary"].encode("utf-8")), f"finding summary {fid}")
        require(len(row["evidence"]) == len(evidence_spec), f"finding evidence denominator {fid}")
        for index, (span, (path, locator)) in enumerate(zip(row["evidence"], evidence_spec)):
            require(span.get("path") == path, f"finding evidence path {fid}/{index}")
            if isinstance(locator, str):
                require(span.get("symbol") == locator, f"finding evidence symbol {fid}/{index}")
            else:
                require((span.get("start_line"), span.get("end_line")) == locator, f"finding evidence lines {fid}/{index}")
            verify_span(span, by_path, f"finding {fid} evidence {index}")
    authority = data.get("authority_boundary", {})
    exact_keys(authority, {"static_identity_complete", "runtime_claim_owner", "scientific_truth", "material_truth", "experimental_truth", "primary_literature_truth", "canonical_adoption", "publication_readiness"}, "code authority")
    require(authority.get("runtime_claim_owner") == "PHASE_063_V1022_RUNTIME_ATTESTATION.json", "runtime claim owner")
    for key in ("scientific_truth", "material_truth", "experimental_truth", "primary_literature_truth", "canonical_adoption", "publication_readiness"):
        require(authority.get(key) is False, f"code authority {key}")
    require(authority.get("static_identity_complete") is True, "static identity completion")


def validate_runtime(data: dict[str, Any]) -> None:
    validate_header(data, "PHASE_063_V1022_RUNTIME_ATTESTATION")
    exact_keys(data, {
        "artifact_kind", "schema_version", "phase", "step", "generated_date",
        "baseline_commit", "expected_parent", "isolation", "runtimes", "official_runs",
        "independent_probes", "counts", "authority_boundary", "result_first_contract",
        "semantic_sha256",
    }, "runtime artifact")
    require(data.get("counts") == {"official_expectations_met": 12, "official_runs": 12, "probe_runtime_sets": 2, "runtimes": 2}, "runtime counts")
    isolation = data.get("isolation", {})
    exact_keys(isolation, {"source_imported", "copied_git_blobs_only", "disposable_external_directories", "external_temp_root_verified", "materialized_paths_contained", "bytecode_disabled", "network_used", "copied_blob_manifest"}, "runtime isolation")
    require(isolation.get("source_imported") is False, "runtime source imported")
    for key in ("copied_git_blobs_only", "disposable_external_directories", "external_temp_root_verified", "materialized_paths_contained", "bytecode_disabled"):
        require(isolation.get(key) is True, f"isolation {key}")
    require(isolation.get("network_used") is False, "runtime network")
    manifest = isolation.get("copied_blob_manifest", [])
    require({row.get("path") for row in manifest} == RUNTIME_COPY_PATHS and len(manifest) == len(RUNTIME_COPY_PATHS), "runtime copy denominator")
    for row in manifest:
        exact_keys(row, {"path", "git_blob", "sha256", "bytes"}, f"runtime manifest {row.get('path')}")
        raw = git_bytes("show", f"{BASELINE}:{row['path']}")
        require(row.get("git_blob") == git_text("rev-parse", f"{BASELINE}:{row['path']}"), f"runtime copy blob {row['path']}")
        require(row.get("sha256") == digest(raw) and row.get("bytes") == len(raw), f"runtime copy bytes {row['path']}")
    runtimes = data.get("runtimes", [])
    require({row.get("runtime") for row in runtimes} == {"3.12", "3.14"} and len(runtimes) == 2, "runtime denominator")
    expected_runtime = {
        "3.12": ("3.12.10", "2.3.5", ["py", "-3.12"]),
        "3.14": ("3.14.4", "2.5.0", ["py", "-3.14"]),
    }
    for row in runtimes:
        exact_keys(row, {"runtime", "python_version", "numpy_version", "launcher"}, f"runtime metadata {row.get('runtime')}")
        require((row["python_version"], row["numpy_version"], row["launcher"]) == expected_runtime[row["runtime"]], f"runtime metadata values {row['runtime']}")
    official = data.get("official_runs", [])
    require(len(official) == 12 and len({row.get("run_id") for row in official}) == 12, "official run denominator")
    observed: dict[tuple[str, str], str] = {}
    for row in official:
        exact_keys(row, {"run_id", "runtime", "command", "cwd", "exit_code", "expected_state", "expected_failure_kind", "diagnostic_matched", "expectation_met", "stdout_tail", "stderr_tail", "authority", "external_science"}, f"official row {row.get('run_id')}")
        runtime = row.get("runtime")
        run_id = row.get("run_id", "")
        suffix = runtime.replace(".", "")
        require(run_id.endswith("-" + suffix), f"official id suffix {run_id}")
        stem = run_id.removeprefix("P063-OFFICIAL-").removesuffix("-" + suffix)
        observed[(runtime, stem)] = row.get("expected_state")
        require(row.get("expectation_met") is True, f"official expectation {run_id}")
        require(row.get("diagnostic_matched") is True, f"official diagnostic {run_id}")
        require(row.get("authority") == "EXACT_COPIED_OFFICIAL_GATE_ONLY" and row.get("external_science") is False, f"official authority {run_id}")
        script_map = {
            "V1021": ("v1.0.21", "test_gates_v1021.py"),
            "V1022": ("v1.0.22", "test_gates_v1022.py"),
            "V1023": ("v1.0.23", "test_gates_v1023.py"),
            "V1023-SC": ("v1.0.23", "test_gates_v1023_selfconsistent.py"),
            "V1023-P1": ("v1.0.23/results/comp_v23", "p1_ratio_check.py"),
            "V1023-CURVE-QA": ("v1.0.23/results/qa_images", "curve_qa.py"),
        }
        cwd, script = script_map[stem]
        require(row.get("cwd") == cwd and row.get("command") == ["py", f"-{runtime}", "-B", "-I", "-X", "utf8", script], f"official command/cwd {run_id}")
        if row.get("expected_state") == "PASS":
            require(row.get("exit_code") == 0 and row.get("expected_failure_kind") is None and row.get("stderr_tail") == [], f"official pass exit {run_id}")
        else:
            expected_kind = "FILE_NOT_FOUND_HARDCODED_PROJECT_PATH" if runtime == "3.12" else "OPTIONAL_DEPENDENCY_MATPLOTLIB_MISSING"
            require(row.get("exit_code") != 0 and row.get("expected_failure_kind") == expected_kind, f"official pinned failure {run_id}")
            diagnostic_text = "\n".join(row.get("stderr_tail", []))
            if runtime == "3.12":
                require("FileNotFoundError" in diagnostic_text and "home/user/Project_Anode_Fit" in diagnostic_text, f"official path diagnostic {run_id}")
            else:
                require("ModuleNotFoundError" in diagnostic_text and "matplotlib" in diagnostic_text, f"official dependency diagnostic {run_id}")
        require(EXPECTED_OFFICIAL_IO_SHA256.get(run_id) == digest(compact({"stdout_tail": row["stdout_tail"], "stderr_tail": row["stderr_tail"]})), f"official output replay digest {run_id}")
    require(observed == EXPECTED_OFFICIAL, "official run matrix")
    probes = data.get("independent_probes", [])
    require({row.get("runtime") for row in probes} == {"3.12", "3.14"} and len(probes) == 2, "probe runtime denominator")
    require(probes[0].get("results") == probes[1].get("results"), "cross-runtime probe drift")
    for runtime_row in probes:
        exact_keys(runtime_row, {"runtime", "probe_program_sha256", "results"}, f"probe runtime {runtime_row.get('runtime')}")
        require(runtime_row.get("probe_program_sha256") == EXPECTED_PROBE_PROGRAM_SHA256, f"probe program digest {runtime_row.get('runtime')}")
        require(EXPECTED_PROBE_RESULTS_SHA256.get(runtime_row["runtime"]) == digest(compact(runtime_row["results"])), f"full probe result digest {runtime_row['runtime']}")
        results = runtime_row.get("results", {})
        require(set(results) == {"v1.0.22", "v1.0.23", "cross_version"}, f"probe top schema {runtime_row['runtime']}")
        require(results.get("cross_version", {}).get("pass") is True, "cross-version probe")
        require(results["cross_version"].get("v22_v23_default_array_equal") is True, "v22-v23 default equality")
        require(results["cross_version"].get("v23_ratio_liveness_max_abs_diff", 0) > 1e-6, "v23 ratio liveness")
        for version in ("v1.0.22", "v1.0.23"):
            group = results.get(version, {})
            require(set(group) == {"background", "capacity", "continuity", "current_partition", "f_si_zero", "from_wt", "missing_kinetics", "root_domain_guards", "root_solver", "scope_boundaries", "si_time"}, f"probe set {version}")
            require(all(row.get("pass") is True for row in group.values()), f"probe pass {version}")
            require(all(row.get("authority") == "ISOLATED_INTERNAL_RUNTIME_ONLY" and row.get("external_science") is False for row in group.values()), f"probe authority {version}")
            require(group["f_si_zero"].get("checks") == {"curve": True, "dqdv_chg": True, "dqdv_dis": True, "equilibrium": True, "solve_U_oc": True}, f"fSi0 {version}")
            require(group["background"].get("si_host_background") == 0.0 and group["background"].get("single_background_max_abs_error", 1) < 1e-12, f"background {version}")
            require(group["capacity"].get("relative_error", 1) <= 1e-6, f"capacity {version}")
            require(group["from_wt"].get("observed_f_si") == group["from_wt"].get("expected_f_si") == group["from_wt"].get("capacity_ratio"), f"from_wt {version}")
            require(abs(group["from_wt"].get("observed_f_si", 0) - 0.7821831869510665) < 1e-15, f"from_wt numeric {version}")
            require(group["root_solver"].get("valid_path_pass") is True and group["root_solver"].get("invalid_control_guard_pass") is False and group["root_solver"].get("finding_reproduced") is True, f"root guard finding {version}")
            require(group["root_domain_guards"].get("negative_Q_constructor_raises") is False and group["root_domain_guards"].get("negative_n_constructor_raises") is False, f"root domain guards {version}")
            require(group["root_domain_guards"].get("finding_reproduced") is True and group["root_domain_guards"].get("negative_Q_case", {}).get("root_count_lower_bound", 0) >= 3 and group["root_domain_guards"].get("negative_n_case", {}).get("root_count_lower_bound", 0) >= 3, f"root multi-root reproduction {version}")
            require(group["missing_kinetics"].get("silent_equilibrium_fallback_observed") is True, f"kinetics fallback {version}")
            continuity = group["continuity"]
            require(continuity.get("coarse_max_step", 0) > continuity.get("fine_max_step", 0) > 0 and abs(continuity.get("refinement_ratio", 0) - continuity["fine_max_step"] / continuity["coarse_max_step"]) < 1e-15 and 0.40 < continuity["refinement_ratio"] < 0.62, f"continuity observations {version}")
            require(group["si_time"].get("curve_equals_raw_hour_number") is True and abs(group["si_time"].get("lag_raw_over_corrected", 0) - 3600.0) < 1e-8, f"SI time {version}")
            require(group["current_partition"].get("same_full_current_to_both_hosts") is True and group["current_partition"].get("host_partition_solver_present") is False, f"current partition {version}")
    authority = data.get("authority_boundary", {})
    exact_keys(authority, {"static_or_runtime_internal_pass", "scientific_truth", "material_truth", "experimental_truth", "primary_literature_truth", "canonical_adoption", "publication_readiness"}, "runtime authority")
    require(authority.get("static_or_runtime_internal_pass") is True, "runtime internal authority")
    for key in ("scientific_truth", "material_truth", "experimental_truth", "primary_literature_truth", "canonical_adoption", "publication_readiness"):
        require(authority.get(key) is False, f"runtime authority {key}")


def validate_frozen_replay(code: dict[str, Any]) -> None:
    expected = [replay_endpoint(path, number) for number, path in enumerate(EXPECTED_ENDPOINTS, 1)]
    require(code["endpoints"] == expected, "independent full frozen endpoint replay")
    for row in expected:
        if row["path"].endswith(".py"):
            require(len(row["ast"]["symbols"]) == EXPECTED_SYMBOL_COUNTS[row["path"]], f"recursive AST denominator {row['path']}")


def evidence_block() -> dict[str, Any]:
    text = RESULT.read_text(encoding="utf-8")
    require(text.count(EVIDENCE_BEGIN) == 1 and text.count(EVIDENCE_END) == 1, "result evidence marker cardinality")
    block = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    require(block.startswith("```json\n") and block.endswith("\n```"), "result evidence fence")
    value, _ = strict_load_text(block[len("```json\n"):-len("\n```")])
    require(isinstance(value, dict), "result evidence root")
    return value


def lf_only(path: pathlib.Path) -> bool:
    raw = path.read_bytes()
    return b"\r" not in raw and raw.endswith(b"\n")


def control_document_checks(code: dict[str, Any], runtime: dict[str, Any]) -> None:
    paths = {"result": RESULT, "active_ledger": ACTIVE_LEDGER, "parent_ledger": PARENT_LEDGER, "handover": HANDOVER}
    for key, path in paths.items():
        expected = CONTROL_SHA256[key]
        require(path.is_file(), f"control document missing: {key}")
        require(expected != "PENDING" and lf_only(path) and digest(path.read_bytes()) == expected, f"control document digest drift: {key}")
    expected_evidence = {
        "baseline_commit": BASELINE, "code_semantic_sha256": code["semantic_sha256"],
        "endpoint_occurrences": 16, "finding_summary": {"P0": 3, "P1": 4, "P2": 6},
        "gate": GATE, "official_expectations_met": "12/12", "probe_runtime_sets": 2,
        "runtime_semantic_sha256": runtime["semantic_sha256"],
    }
    require(evidence_block() == expected_evidence, "result evidence content")
    result_text = RESULT.read_text(encoding="utf-8")
    require(GATE in result_text and "PENDING_AT_PRECOMMIT_BY_DESIGN" in result_text, "result gate/sentinel")
    require(SUBJECT in result_text and EXPECTED_PARENT in result_text, "result commit contract")
    for path in (ACTIVE_LEDGER, PARENT_LEDGER, HANDOVER):
        text = path.read_text(encoding="utf-8")
        require("Step 61" in text and GATE in text and "PENDING_AT_PRECOMMIT_BY_DESIGN" in text, f"Step 61 recovery marker {path.name}")


def mutate_at(root: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def negative_probes(code: dict[str, Any], runtime: dict[str, Any]) -> tuple[int, int]:
    delete_marker = object()
    cases: list[tuple[str, str, tuple[Any, ...], Any]] = [
        ("code-kind", "code", ("artifact_kind",), "BAD"), ("code-schema", "code", ("schema_version",), 2),
        ("code-phase", "code", ("phase",), 64), ("code-step", "code", ("step",), 60),
        ("code-baseline", "code", ("baseline_commit",), "0" * 40), ("code-parent", "code", ("expected_parent",), "0" * 40),
        ("code-subject", "code", ("expected_subject",), "bad"), ("code-count", "code", ("counts", "endpoint_occurrences"), 15),
        ("endpoint-path", "code", ("endpoints", 0, "path"), "Claude/docs/bad.py"), ("endpoint-blob", "code", ("endpoints", 0, "git_blob"), "0" * 40),
        ("endpoint-sha", "code", ("endpoints", 0, "sha256"), "0" * 64), ("endpoint-bytes", "code", ("endpoints", 0, "bytes"), 1),
        ("endpoint-lines", "code", ("endpoints", 0, "lines"), 1), ("endpoint-traversal", "code", ("endpoints", 0, "full_blob_traversal"), False),
        ("endpoint-version", "code", ("endpoints", 0, "version"), "9.9.9"), ("endpoint-role", "code", ("endpoints", 0, "role"), "BAD"),
        ("endpoint-nonblank", "code", ("endpoints", 0, "nonblank_lines"), 1), ("endpoint-line-ending", "code", ("endpoints", 0, "line_ending"), "CRLF"),
        ("symbol-count", "code", ("endpoints", 0, "ast", "symbols"), []),
        ("symbol-name", "code", ("endpoints", 0, "ast", "symbols", 0, "qualified_name"), "forged"),
        ("symbol-code-hash", "code", ("endpoints", 0, "ast", "symbols", 0, "code_ast_sha256"), "0" * 64),
        ("guide-heading", "code", ("endpoints", 1, "headings", 0, "text"), "# forged"),
        ("finding-count", "code", ("counts", "findings"), 11),
        ("finding-summary", "code", ("finding_summary", "P0"), 2), ("finding-id", "code", ("findings", 0, "finding_id"), "BAD"),
        ("finding-priority", "code", ("findings", 0, "priority"), "P9"), ("finding-status", "code", ("findings", 0, "status"), "CLOSED"),
        ("finding-authority", "code", ("findings", 0, "external_truth_validated"), True), ("finding-text", "code", ("findings", 0, "summary"), "forged"),
        ("finding-owner", "code", ("findings", 0, "owner"), "Phase 999"), ("finding-probes", "code", ("findings", 0, "runtime_probe_ids"), []),
        ("finding-evidence", "code", ("findings", 0, "evidence", 0, "start_line"), 1),
        ("concordance-id", "code", ("theory_code_concordance", 0, "concordance_id"), "BAD"),
        ("concordance-authority", "code", ("theory_code_concordance", 0, "external_science"), True),
        ("concordance-state", "code", ("theory_code_concordance", 0, "state"), "FORGED"),
        ("concordance-span", "code", ("theory_code_concordance", 0, "code_spans", 0, "code_ast_sha256"), "0" * 64),
        ("delta-content", "code", ("symbol_deltas", 0, "added_symbols"), []),
        ("shared-paths", "code", ("shared_blob_groups", 0, "paths"), []),
        ("static-value", "code", ("static_contracts", 0, "occurrences", 0, "value", 0, "Q"), 99.0),
        ("code-science-authority", "code", ("authority_boundary", "scientific_truth"), True),
        ("code-semantic", "code", ("semantic_sha256",), "0" * 64),
        ("runtime-kind", "runtime", ("artifact_kind",), "BAD"), ("runtime-count", "runtime", ("counts", "official_runs"), 11),
        ("runtime-source-import", "runtime", ("isolation", "source_imported"), True),
        ("runtime-copy", "runtime", ("isolation", "copied_git_blobs_only"), False), ("runtime-network", "runtime", ("isolation", "network_used"), True),
        ("runtime-external-temp", "runtime", ("isolation", "external_temp_root_verified"), False),
        ("runtime-manifest-path", "runtime", ("isolation", "copied_blob_manifest", 0, "path"), "bad"),
        ("runtime-manifest-sha", "runtime", ("isolation", "copied_blob_manifest", 0, "sha256"), "0" * 64),
        ("official-id", "runtime", ("official_runs", 0, "run_id"), "BAD"),
        ("official-expectation", "runtime", ("official_runs", 0, "expectation_met"), False),
        ("official-exit", "runtime", ("official_runs", 0, "exit_code"), 1), ("official-command", "runtime", ("official_runs", 0, "command"), ["py"]),
        ("official-cwd", "runtime", ("official_runs", 0, "cwd"), "forged"), ("official-output", "runtime", ("official_runs", 0, "stdout_tail"), ["forged"]),
        ("official-authority", "runtime", ("official_runs", 0, "external_science"), True),
        ("runtime-version", "runtime", ("runtimes", 0, "python_version"), "0.0.0"), ("runtime-launcher", "runtime", ("runtimes", 0, "launcher"), ["forged"]),
        ("probe-runtime", "runtime", ("independent_probes", 0, "runtime"), "9.99"),
        ("probe-program", "runtime", ("independent_probes", 0, "probe_program_sha256"), "0" * 64),
        ("probe-cross", "runtime", ("independent_probes", 0, "results", "cross_version", "pass"), False),
        ("probe-fsi0", "runtime", ("independent_probes", 0, "results", "v1.0.22", "f_si_zero", "pass"), False),
        ("probe-capacity", "runtime", ("independent_probes", 0, "results", "v1.0.22", "capacity", "relative_error"), 1.0),
        ("probe-root", "runtime", ("independent_probes", 0, "results", "v1.0.22", "root_solver", "finding_reproduced"), False),
        ("probe-root-domain", "runtime", ("independent_probes", 0, "results", "v1.0.22", "root_domain_guards", "finding_reproduced"), False),
        ("probe-continuity", "runtime", ("independent_probes", 0, "results", "v1.0.22", "continuity", "coarse_max_step"), 0.0),
        ("probe-si-time", "runtime", ("independent_probes", 0, "results", "v1.0.22", "si_time", "lag_raw_over_corrected"), 1.0),
        ("probe-current", "runtime", ("independent_probes", 0, "results", "v1.0.22", "current_partition", "host_partition_solver_present"), True),
        ("runtime-science-authority", "runtime", ("authority_boundary", "scientific_truth"), True),
        ("runtime-semantic", "runtime", ("semantic_sha256",), "0" * 64),
        ("code-contract", "code", ("result_first_contract", "containing_commit"), EXPECTED_PARENT),
        ("runtime-contract", "runtime", ("result_first_contract", "postcommit_terminal"), "PASS"),
        ("omit-symbol-hash", "code", ("endpoints", 0, "ast", "symbols", 0, "code_ast_sha256"), delete_marker),
        ("omit-guide-headings", "code", ("endpoints", 1, "headings"), delete_marker),
        ("omit-finding-summary", "code", ("findings", 0, "summary"), delete_marker),
        ("omit-concordance-spans", "code", ("theory_code_concordance", 0, "code_spans"), delete_marker),
        ("omit-delta-added", "code", ("symbol_deltas", 0, "added_symbols"), delete_marker),
        ("omit-static-occurrences", "code", ("static_contracts", 0, "occurrences"), delete_marker),
        ("omit-runtime-launcher", "runtime", ("runtimes", 0, "launcher"), delete_marker),
        ("omit-official-output", "runtime", ("official_runs", 0, "stdout_tail"), delete_marker),
        ("omit-probe-program", "runtime", ("independent_probes", 0, "probe_program_sha256"), delete_marker),
        ("omit-external-temp", "runtime", ("isolation", "external_temp_root_verified"), delete_marker),
    ]
    rejected = 0
    for name, target_name, path, value in cases:
        c, r = copy.deepcopy(code), copy.deepcopy(runtime)
        target = c if target_name == "code" else r
        if value is delete_marker:
            owner: Any = target
            for key in path[:-1]:
                owner = owner[key]
            del owner[path[-1]]
        else:
            mutate_at(target, path, value)
        if name not in {"code-semantic", "runtime-semantic"}:
            target["semantic_sha256"] = semantic_digest(target)
        try:
            validate_code(c)
            validate_runtime(r)
        except (KeyError, TypeError, ValueError, ValidationError):
            rejected += 1
            continue
        raise ValidationError(f"negative mutation accepted: {name}")
    return rejected, len(cases)


def strict_json_negative_probes() -> tuple[int, int]:
    fixtures = ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}', '{"a":[1,2}')
    rejected = 0
    for fixture in fixtures:
        try:
            strict_load_text(fixture)
        except (json.JSONDecodeError, ValidationError, ValueError):
            rejected += 1
    require(rejected == len(fixtures), "strict JSON negative probes")
    return rejected, len(fixtures)


def run_builder(directory: pathlib.Path) -> tuple[bytes, bytes]:
    proc = run([sys.executable, "-B", "-I", "-X", "utf8", str(BUILDER), "--output-dir", str(directory)], timeout=TIMEOUT)
    if proc.returncode:
        raise ValidationError("builder failed: " + (proc.stdout + proc.stderr).decode("utf-8", "replace").strip())
    return (directory / CODE_ARTIFACT.name).read_bytes(), (directory / RUNTIME_ARTIFACT.name).read_bytes()


def determinism_check() -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="p063-step61-a-") as first, tempfile.TemporaryDirectory(prefix="p063-step61-b-") as second:
        first_raw = run_builder(pathlib.Path(first))
        second_raw = run_builder(pathlib.Path(second))
        current = CODE_ARTIFACT.read_bytes(), RUNTIME_ARTIFACT.read_bytes()
        require(first_raw == second_raw == current, "builder determinism drift")
    return 2, 2


def verify_external_temp_policy() -> None:
    resolved_repo = REPO.resolve()
    with tempfile.TemporaryDirectory(prefix="p063-step61-validator-") as directory:
        resolved_temp = pathlib.Path(directory).resolve()
        require(resolved_temp != resolved_repo and resolved_repo not in resolved_temp.parents, "validator temp root is inside repository")
        probe = (resolved_temp / "nested" / "probe.py").resolve()
        require(resolved_temp in probe.parents, "validator materialized path escapes temp root")


def replay_probe_source() -> str:
    tree = ast.parse(BUILDER.read_text(encoding="utf-8"), filename=str(BUILDER))
    matches = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "PROBE_SOURCE" for target in node.targets)
    ]
    require(len(matches) == 1, "builder PROBE_SOURCE assignment denominator")
    source = ast.literal_eval(matches[0].value)
    require(isinstance(source, str) and digest(source.encode("utf-8")) == EXPECTED_PROBE_PROGRAM_SHA256, "independent probe source digest")
    return source


def normalized_runtime_tail(raw: bytes, temp_root: pathlib.Path, limit: int = 24) -> list[str]:
    text = raw.decode("utf-8", "replace").replace(str(temp_root), "<TMP>")
    text = text.replace(str(temp_root).replace("\\", "/"), "<TMP>")
    return [line.rstrip() for line in text.splitlines() if line.strip()][-limit:]


def independent_runtime_replay(runtime: dict[str, Any]) -> tuple[int, int]:
    source = replay_probe_source()
    by_runtime = {row["runtime"]: row for row in runtime["independent_probes"]}
    runtime_meta = {row["runtime"]: row for row in runtime["runtimes"]}
    official_by_runtime: dict[str, list[dict[str, Any]]] = {"3.12": [], "3.14": []}
    for row in runtime["official_runs"]:
        official_by_runtime[row["runtime"]].append(row)
    completed = 0
    with tempfile.TemporaryDirectory(prefix="p063-step61-independent-runtime-") as directory:
        temp_root = pathlib.Path(directory).resolve()
        resolved_repo = REPO.resolve()
        require(temp_root != resolved_repo and resolved_repo not in temp_root.parents, "independent runtime root inside repository")
        for path in sorted(RUNTIME_COPY_PATHS):
            target = temp_root / pathlib.PurePosixPath(path).relative_to("Claude/docs")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(frozen_raw(path))
            require(temp_root in target.resolve().parents, f"independent runtime copy escaped root: {path}")
        probe_path = temp_root / "independent_validator_probe.py"
        probe_path.write_text(source, encoding="utf-8", newline="\n")
        require(temp_root in probe_path.resolve().parents, "independent probe escaped root")
        for label in ("3.12", "3.14"):
            launcher = ["py", f"-{label}"]
            version_proc = run([*launcher, "-B", "-I", "-X", "utf8", "-c", "import sys,numpy;print(sys.version.split()[0]);print(numpy.__version__)"], cwd=temp_root)
            require(version_proc.returncode == 0, f"independent runtime metadata exit {label}")
            versions = version_proc.stdout.decode("utf-8").splitlines()
            require(versions == [runtime_meta[label]["python_version"], runtime_meta[label]["numpy_version"]], f"independent runtime metadata {label}")
            for row in official_by_runtime[label]:
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"
                env["PYTHONDONTWRITEBYTECODE"] = "1"
                env["ANODEFIT_TMP"] = str(temp_root / f"variant_{row['run_id']}")
                proc = run(row["command"], cwd=temp_root / row["cwd"], env=env)
                require(proc.returncode == row["exit_code"], f"independent official exit {row['run_id']}")
                require(normalized_runtime_tail(proc.stdout, temp_root) == row["stdout_tail"], f"independent official stdout {row['run_id']}")
                require(normalized_runtime_tail(proc.stderr, temp_root) == row["stderr_tail"], f"independent official stderr {row['run_id']}")
                completed += 1
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            proc = run([
                *launcher, "-B", "-I", "-X", "utf8", str(probe_path),
                str(temp_root / "v1.0.22/Anode_Fit_v1.0.22.py"),
                str(temp_root / "v1.0.23/Anode_Fit_v1.0.23.py"),
            ], cwd=temp_root, env=env)
            require(proc.returncode == 0, f"independent probe exit {label}")
            observed, _ = strict_load_text(proc.stdout.decode("utf-8"))
            require(observed == by_runtime[label]["results"], f"independent full probe replay {label}")
            completed += 1
    require(completed == 14, "independent runtime replay denominator")
    return completed, 14


def verify_branch_guards() -> None:
    errors = []
    if ref_hash(f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("protected local")
    if ref_hash(f"refs/remotes/origin/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("protected tracking")
    if remote_head(PROTECTED_BRANCH) != PROTECTED_TIP:
        errors.append("protected live")
    if ref_hash("refs/heads/main") is not None:
        errors.append("unexpected local main")
    if ref_hash("refs/remotes/origin/main") != MAIN_TIP or remote_head("main") != MAIN_TIP:
        errors.append("main drift")
    if git_paths("diff", "--name-only", "-z", BASELINE, "HEAD", "--", "Claude"):
        errors.append("Claude committed diff")
    if git_paths("diff", "--name-only", "-z", "--", "Claude"):
        errors.append("Claude worktree diff")
    if git_paths("diff", "--cached", "--name-only", "-z", "--", "Claude"):
        errors.append("Claude staged diff")
    require(not errors, "branch guard drift: " + ", ".join(errors))


def verify_staged() -> str:
    require(git_text("branch", "--show-current") == BRANCH, "wrong branch")
    require(git_text("rev-parse", "HEAD") == EXPECTED_PARENT, "wrong precommit parent")
    require(git_text("rev-parse", "@{upstream}") == EXPECTED_PARENT and remote_head(BRANCH) == EXPECTED_PARENT, "upstream/live not at parent")
    staged = git_paths("diff", "--cached", "--name-only", "-z", "HEAD")
    require(staged == EXACT_EIGHT_SET, f"staged path mismatch: {sorted(staged ^ EXACT_EIGHT_SET)}")
    unstaged = git_paths("diff", "--name-only", "-z")
    untracked = git_paths("ls-files", "--others", "--exclude-standard", "-z")
    require(not unstaged and not untracked, f"unstaged/untracked paths remain: {sorted(unstaged | untracked)}")
    for path in EXACT_EIGHT:
        require(git_bytes("show", f":{path}") == (REPO / path).read_bytes(), f"staged/worktree byte mismatch: {path}")
    for args in (["git", "diff", "--check"], ["git", "diff", "--cached", "--check"]):
        proc = run(args)
        require(proc.returncode == 0, "staged whitespace check: " + (proc.stdout + proc.stderr).decode("utf-8", "replace").strip())
    verify_branch_guards()
    return EXPECTED_PARENT


def verify_persistence(expected_commit: str | None) -> str:
    require(bool(expected_commit and re.fullmatch(r"[0-9a-f]{40}", expected_commit)), "--expected-commit full hash required")
    require(git_text("branch", "--show-current") == BRANCH, "wrong branch")
    head = git_text("rev-parse", "HEAD")
    require(head == expected_commit and git_text("rev-parse", "HEAD^") == EXPECTED_PARENT, "local HEAD/parent mismatch")
    require(git_text("show", "-s", "--format=%s", "HEAD") == SUBJECT, "commit subject mismatch")
    require(git_text("rev-parse", "@{upstream}") == head and remote_head(BRANCH) == head, "upstream/live mismatch")
    changed = git_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD")
    require(changed == EXACT_EIGHT_SET, f"commit path mismatch: {sorted(changed ^ EXACT_EIGHT_SET)}")
    require(not git_paths("status", "--porcelain=v1", "-z") and not git_paths("diff", "--cached", "--name-only", "-z"), "worktree/index not clean")
    for path in EXACT_EIGHT:
        require(git_bytes("show", f"HEAD:{path}") == (REPO / path).read_bytes(), f"commit/worktree byte mismatch: {path}")
    proc = run(["git", "diff", "--check", "HEAD^", "HEAD"])
    require(proc.returncode == 0, "commit whitespace check: " + (proc.stdout + proc.stderr).decode("utf-8", "replace").strip())
    verify_branch_guards()
    return head


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if sum((args.content_only, args.verify_staged, args.verify_persistence)) != 1:
        print("select exactly one primary mode", file=sys.stderr)
        return 2
    try:
        require(CODE_ARTIFACT.is_file(), f"E_CODE_ARTIFACT_MISSING: {CODE_ARTIFACT.relative_to(REPO)}")
        require(RUNTIME_ARTIFACT.is_file(), f"E_RUNTIME_ARTIFACT_MISSING: {RUNTIME_ARTIFACT.relative_to(REPO)}")
        code, code_nodes = strict_load(CODE_ARTIFACT)
        runtime, runtime_nodes = strict_load(RUNTIME_ARTIFACT)
        require(isinstance(code, dict) and isinstance(runtime, dict), "artifact roots")
        validate_code(code)
        validate_runtime(runtime)
        validate_frozen_replay(code)
        verify_external_temp_policy()
        runtime_replay = independent_runtime_replay(runtime)
        control_document_checks(code, runtime)
        terminal = args.verify_staged or args.verify_persistence
        run_negative = args.run_negative_probes or terminal
        run_determinism = args.determinism_check or terminal
        negative = negative_probes(code, runtime) if run_negative else (0, 0)
        strict_negative = strict_json_negative_probes() if run_negative else (0, 0)
        determinism = determinism_check() if run_determinism else (0, 0)
        suffix = f"runtime_replay={runtime_replay[0]}/{runtime_replay[1]} negative={negative[0]}/{negative[1]} strict={strict_negative[0]}/{strict_negative[1]} determinism={determinism[0]}/{determinism[1]} nodes={code_nodes + runtime_nodes}"
        if args.verify_staged:
            print(f"PASS_P063_STEP61_STAGED parent={verify_staged()} paths=8/8 {suffix}")
        elif args.verify_persistence:
            print(f"PASS_P063_STEP61_PERSISTENCE head={verify_persistence(args.expected_commit)} paths=8/8 {suffix}")
        else:
            print(f"PASS_P063_STEP61_CONTENT endpoints=16/16 official=12/12 probes=2/2 {suffix}")
        return 0
    except (OSError, UnicodeError, KeyError, TypeError, ValueError, ValidationError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL_P063_STEP61: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
