#!/usr/bin/env python3
"""Close Phase 067 with a persisted theory-code-test-data conformance gate."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_AST_SEAL = "42c77275d98f2eeecc6e035ccd99a19685b3d517332dcf0b47ca6085f8d9f771"
SOURCE_POLICY_ANCHOR = "c74e94476bb1819592c8016eac58d7e94911264bf23233a4140dc49a3ea21c7d"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "ba29277a6d6b4469e8718e025bd1c676d8c7d65e"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
SUBJECT = "audit(phase067): close code history gate"
GATE = "CONDITIONAL_P067"
PERSISTENCE = "PASS_P067_STEP90_2_PERSISTENCE"
PRECOMMIT_STATUS = "CONDITIONAL_PENDING_PERSISTENCE"
PHASE066_VALIDATION = "Codex/results/PHASE_066_VALIDATION.json"
PHASE066_VALIDATION_COMMIT = "7241b331ff76bc8d43cb1bc6b69634977e0884a0"
PHASE066_VALIDATION_RAW_SHA256 = "2893670d87ab414c7243d0ed862ba19d2055d84260ca2f6f5c2ebc3ff5407577"
PHASE066_VALIDATION_SEMANTIC_SHA256 = "925556e534b9be49f4aed6d1889729d4f567350c5d09c6b09685d08442e3419e"

VALIDATOR = "Codex/work/v1025_phase067/validate_phase067_final.py"
ARTIFACT = "Codex/results/PHASE_067_VALIDATION.json"
REPORT = "Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md"
GATE_RESULT = "Codex/results/PHASE_067_STEP_090_2_GATE_RESULT.md"
RESULT = "Codex/results/PHASE_067_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = (
    VALIDATOR,
    ARTIFACT,
    REPORT,
    GATE_RESULT,
    RESULT,
    PARENT_LEDGER,
    ACTIVE_LEDGER,
    HANDOVER,
)
FINAL_STATUS = {path: ("A" if index < 5 else "M")
                for index, path in enumerate(FINAL_PATHS)}
NONARTIFACT_PATHS = tuple(path for path in FINAL_PATHS if path != ARTIFACT)

UNIT_SPECS = (
    {
        "step": "82",
        "commit": "db167fdc941eafba0313b8476dfe7483108f13ff",
        "parent": "8975d6a6cc46686e38249b7971b5535dfa414a8b",
        "subject": "audit(phase067): freeze complete python topology",
        "gate": "PASS_P067_STEP82_SOURCE_TOPOLOGY",
        "terminal": "PASS_P067_STEP82_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step82.py",
            "Codex/work/v1025_phase067/validate_phase067_step82.py",
            "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json",
            "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json",
            "Codex/results/PHASE_067_STEP_082_SOURCE_TOPOLOGY_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 5,
    },
    {
        "step": "83",
        "commit": "1af6c06fb5cff2918b846ed74ea213832f04f010",
        "parent": "db167fdc941eafba0313b8476dfe7483108f13ff",
        "subject": "audit(phase067): trace state quantity flows",
        "gate": "PASS_P067_STEP83_STATE_FLOW",
        "terminal": "PASS_P067_STEP83_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step83.py",
            "Codex/work/v1025_phase067/validate_phase067_step83.py",
            "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json",
            "Codex/results/PHASE_067_STEP_083_STATE_FLOW_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 4,
    },
    {
        "step": "84",
        "commit": "f00bf2fa8f25c85f0c62cb901912763d98c8f070",
        "parent": "1af6c06fb5cff2918b846ed74ea213832f04f010",
        "subject": "audit(phase067): reconstruct physics call graph",
        "gate": "PASS_P067_STEP84_PHYSICS_CALL_GRAPH",
        "terminal": "PASS_P067_STEP84_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step84.py",
            "Codex/work/v1025_phase067/validate_phase067_step84.py",
            "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json",
            "Codex/results/PHASE_067_STEP_084_PHYSICS_CALL_GRAPH_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 4,
    },
    {
        "step": "85",
        "commit": "3f2c7635aa545bd617b6cd83b5e718683d5b2b1c",
        "parent": "f00bf2fa8f25c85f0c62cb901912763d98c8f070",
        "subject": "audit(phase067): separate defaults state persistence",
        "gate": "PASS_P067_STEP85_STATE_DEFAULT_IMPORT",
        "terminal": "PASS_P067_STEP85_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step85.py",
            "Codex/work/v1025_phase067/validate_phase067_step85.py",
            "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json",
            "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json",
            "Codex/results/PHASE_067_STEP_085_STATE_DEFAULT_IMPORT_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 5,
    },
    {
        "step": "86",
        "commit": "4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7",
        "parent": "3f2c7635aa545bd617b6cd83b5e718683d5b2b1c",
        "subject": "audit(phase067): adjudicate test demo golden behavior",
        "gate": "PASS_P067_STEP86_TEST_DEMO_GOLDEN",
        "terminal": "PASS_P067_STEP86_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step86.py",
            "Codex/work/v1025_phase067/validate_phase067_step86.py",
            "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json",
            "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json",
            "Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 5,
    },
    {
        "step": "87",
        "commit": "ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4",
        "parent": "4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7",
        "subject": "audit(phase067): verify units numerical invariants",
        "gate": "PASS_P067_STEP87_UNIT_NUMERICAL",
        "terminal": "PASS_P067_STEP87_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step87.py",
            "Codex/work/v1025_phase067/validate_phase067_step87.py",
            "Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json",
            "Codex/results/PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 4,
    },
    {
        "step": "88",
        "commit": "7b81814017ffd4207cc2a13fabbbe68281075b00",
        "parent": "ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4",
        "subject": "audit(phase067): bound numerical guard impacts",
        "gate": "PASS_P067_STEP88_NUMERICAL_GUARD",
        "terminal": "PASS_P067_STEP88_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step88.py",
            "Codex/work/v1025_phase067/validate_phase067_step88.py",
            "Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json",
            "Codex/results/PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 4,
    },
    {
        "step": "89",
        "commit": "38f93bd1638c674ff7fd7fb40ed57036a07fd8fd",
        "parent": "7b81814017ffd4207cc2a13fabbbe68281075b00",
        "subject": "audit(phase067): separate fitting evidence authority",
        "gate": "PASS_P067_STEP89_FITTING_AUTHORITY",
        "terminal": "PASS_P067_STEP89_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step89.py",
            "Codex/work/v1025_phase067/validate_phase067_step89.py",
            "Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json",
            "Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json",
            "Codex/results/PHASE_067_STEP_089_FITTING_AUTHORITY_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 5,
    },
    {
        "step": "90.1",
        "commit": EXPECTED_PARENT,
        "parent": "38f93bd1638c674ff7fd7fb40ed57036a07fd8fd",
        "subject": "audit(phase067): disposition code test fitting evidence",
        "gate": "PASS_P067_STEP90_1_DISPOSITION",
        "terminal": "PASS_P067_STEP90_1_PERSISTENCE",
        "paths": (
            "Codex/work/v1025_phase067/build_phase067_step90_dispositions.py",
            "Codex/work/v1025_phase067/validate_phase067_step90_dispositions.py",
            "Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json",
            "Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json",
            "Codex/results/PHASE_067_STEP_090_1_DISPOSITION_RESULT.md",
            PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER,
        ),
        "added": 5,
    },
)

MACHINE_SPECS = (
    ("Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json", UNIT_SPECS[0]["commit"],
     "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63",
     "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1", "pretty", "step82"),
    ("Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json", UNIT_SPECS[0]["commit"],
     "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174",
     "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9", "pretty", "step82"),
    ("Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json", UNIT_SPECS[1]["commit"],
     "0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8",
     "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44", "compact", "compact"),
    ("Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json", UNIT_SPECS[2]["commit"],
     "54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f",
     "63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc", "compact", "compact"),
    ("Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json", UNIT_SPECS[3]["commit"],
     "b8ac7affbb31195ec8dde6015890cbb50b1f2b9cc5815fc33c325efc95286f23",
     "845b676aea321134b648de41320e7baf4f39f925ad2a1abe96f36f713bc95542", "compact", "compact"),
    ("Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json", UNIT_SPECS[3]["commit"],
     "9bf610d2d09be7d95fd2493541d6c4336de330c37fb56d1f12c411b228dfbf82",
     "0e2b0bd3f6120c9c8feaa879b5fe62a49934de5ea8dbddff14c700ddef32f196", "compact", "compact"),
    ("Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json", UNIT_SPECS[4]["commit"],
     "13a281c76282f5fae370d1c2b10f183937c685bceba466489a62b9e850049d4a",
     "eadde68e51257e0daae9f9455be3a7331c77a56d1490b2291934ef75f45fa154", "compact", "compact"),
    ("Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json", UNIT_SPECS[4]["commit"],
     "474f09ebb1605d3190867cee9746079b10c04f6bfbdfbab028e9d6c1be70ec08",
     "c556671b6fd4284d740fdb0cc3777087442d4abd2160ace42d4ff70749d4144c", "compact", "compact"),
    ("Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json", UNIT_SPECS[5]["commit"],
     "62f5eb265121987b83398266895a11e8a84d7f1ffa90c59fe929efb6f00614be",
     "099899de75edfde55a92ff31f577e178967212226cf4a13cdb951643b15e535c", "compact", "compact"),
    ("Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json", UNIT_SPECS[6]["commit"],
     "525b33403667413446e374a2b931c90ec45c7eb24871205527dd9c6ddef2591d",
     "201b2e65756ab8876c861216742f67b0305ef351cc84e8f4ebf434d49dfabb2b", "compact", "compact"),
    ("Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json", UNIT_SPECS[7]["commit"],
     "dc76eeef9b0bb2f93a376fbe491f12b2c73b47d59b097e671e9745b28a6869f4",
     "cf1b136028f126670a80ec60ce26db9edc110e0bff7c41cf7986f73c14f9ae3a", "compact", "compact"),
    ("Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json", UNIT_SPECS[7]["commit"],
     "c0859de686ea207be758fc6d32faaa88d2e95151e3c3bdb56615ff366f250486",
     "b78cfa4ec96e3aeb42979e6aaf93407fed9267fd7abeeb8458064d78b3567846", "compact", "compact"),
    ("Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json", UNIT_SPECS[8]["commit"],
     "f9b8383cf10eb2cf7febd689171cdd2732ad7696b2a999c2bf6423150b3e1679",
     "b37c59d5909e1232bc3d96e7751642c84b950ebe079afafc24a1864eb9462d44", "compact", "compact"),
    ("Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json", UNIT_SPECS[8]["commit"],
     "9fd3f605185e9fe03a8f9f9e107097876c1478165096eb55fa39fe2d9ceedbf9",
     "e54262e36afed636331416561dbf953970d74800404f83d26973e84e10ca91c2", "compact", "compact"),
    ("Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json",
     "bdad7375d70c3734cc63265d94a61dd82afd143d",
     "847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003",
     "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6", "pretty", "legacy"),
)

MACHINE_PATHS = tuple(spec[0] for spec in MACHINE_SPECS)
KNOWN_COMMITS = frozenset(spec["commit"] for spec in UNIT_SPECS) | \
    frozenset(spec["parent"] for spec in UNIT_SPECS) | \
    frozenset(spec[1] for spec in MACHINE_SPECS) | \
    {BASELINE, PHASE066_VALIDATION_COMMIT, PROTECTED_TIP, MAIN_TIP}
KNOWN_PATHS = frozenset(
    path for spec in UNIT_SPECS for path in spec["paths"]
) | frozenset(FINAL_PATHS) | frozenset(MACHINE_PATHS) | {PHASE066_VALIDATION, "Claude"}

MAX_JSON_BYTES = 8_000_000
MAX_JSON_DEPTH = 64
MAX_JSON_NODES = 600_000


class ValidationError(RuntimeError):
    """Named fail-closed validation error."""


def require(ok: bool, code: str, detail: str = "") -> None:
    if not ok:
        raise ValidationError(code + ((":" + detail) if detail else ""))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(document: dict[str, Any], style: str) -> str:
    body = copy.deepcopy(document)
    if style == "step82":
        body["semantic_sha256"] = ""
        return sha256(pretty(body))
    body.pop("semantic_sha256", None)
    if style == "compact":
        return sha256(canonical(body))
    require(style == "legacy", "E_SEMANTIC_STYLE", style)
    return sha256(json.dumps(body, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":"), allow_nan=False).encode("utf-8"))


def record_sha(value: Any) -> str:
    return sha256(canonical(value))


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            typed_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def strict_load(raw: bytes, label: str, raw_style: str,
                semantic_style: str | None) -> tuple[dict[str, Any], int, int]:
    require(0 < len(raw) <= MAX_JSON_BYTES, label + "_BYTES")
    nesting = 0
    maximum = 0
    in_string = False
    escaped = False
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                in_string = False
        elif byte == 34:
            in_string = True
        elif byte in (91, 123):
            nesting += 1
            maximum = max(maximum, nesting)
            require(nesting <= MAX_JSON_DEPTH, label + "_DEPTH")
        elif byte in (93, 125):
            nesting -= 1
            require(nesting >= 0, label + "_LEXICAL")
    require(nesting == 0 and not in_string and not escaped, label + "_LEXICAL")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, label + "_DUPLICATE", key)
            result[key] = value
        return result

    def reject_constant(_: str) -> Any:
        raise ValueError("nonfinite")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError,
            RecursionError, MemoryError) as exc:
        raise ValidationError(label + "_PARSE") from exc
    require(isinstance(value, dict), label + "_ROOT")
    nodes = 0
    tree_depth = 0
    stack: list[tuple[Any, int]] = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        nodes += 1
        require(nodes <= MAX_JSON_NODES, label + "_NODES")
        require(depth <= MAX_JSON_DEPTH, label + "_DEPTH")
        tree_depth = max(tree_depth, depth)
        if isinstance(item, dict):
            for key, child in item.items():
                require(isinstance(key, str), label + "_TREE")
                stack.append((key, depth + 1))
                stack.append((child, depth + 1))
        elif isinstance(item, list):
            for child in item:
                stack.append((child, depth + 1))
        elif isinstance(item, float):
            require(math.isfinite(item), label + "_NONFINITE")
        else:
            require(item is None or isinstance(item, (str, int, bool)), label + "_TREE")
    if raw_style == "compact":
        require(raw == canonical(value), label + "_NONCANONICAL")
    elif raw_style == "pretty":
        require(raw == pretty(value), label + "_NONCANONICAL")
    else:
        require(raw_style == "unchecked", label + "_STYLE")
    if semantic_style is not None:
        require(value.get("semantic_sha256") == semantic_sha(value, semantic_style),
                label + "_SEMANTIC")
    return value, nodes, max(maximum, tree_depth)


def is_oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def call_owner_map(tree: ast.AST) -> dict[int, str]:
    owners: dict[int, str] = {}

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack = ["<module>"]

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_Call(self, node: ast.Call) -> None:
            owners[id(node)] = self.stack[-1]
            self.generic_visit(node)

    Visitor().visit(tree)
    return owners


def node_location(node: ast.AST) -> tuple[int, int]:
    return node.lineno, node.col_offset


def replacement_root(node: ast.AST) -> ast.AST:
    current = node
    while isinstance(current, ast.Call) and isinstance(current.func, ast.Attribute) and \
            current.func.attr == "replace":
        current = current.func.value
    return current


def filesystem_receiver(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and \
            isinstance(node.left, ast.Name) and node.left.id == "ROOT" and \
            isinstance(node.right, ast.Name):
        return "ROOT/" + node.right.id
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
            node.func.id == "Path" and len(node.args) == 1 and \
            isinstance(node.args[0], ast.Name) and node.args[0].id == "__file__" and \
            node.keywords == []:
        return "Path(__file__)"
    return "UNDECLARED_RECEIVER"


def source_policy_errors(source: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["E_SOURCE_PARSE"]
    seal_assignments = [
        node for node in tree.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and node.targets[0].id == "SOURCE_AST_SEAL"
    ]
    seal_shape_ok = len(seal_assignments) == 1 and \
        isinstance(seal_assignments[0].value, ast.Constant) and \
        isinstance(seal_assignments[0].value.value, str) and \
        re.fullmatch(r"[0-9a-f]{64}", seal_assignments[0].value.value) is not None
    if seal_shape_ok:
        declared_ast_seal = seal_assignments[0].value.value
        seal_value = seal_assignments[0].value
        source_lines = source.splitlines()
        seal_index = seal_value.lineno - 1
        seal_literal = '"' + declared_ast_seal + '"'
        seal_location_ok = seal_value.lineno == seal_value.end_lineno and \
            0 <= seal_index < len(source_lines) and \
            source_lines[seal_index][seal_value.col_offset:seal_value.end_col_offset] == \
            seal_literal
        if seal_location_ok:
            normalized_lines = source_lines[:seal_index] + [
                source_lines[seal_index][:seal_value.col_offset] +
                ('"' + "0" * 64 + '"') +
                source_lines[seal_index][seal_value.end_col_offset:]
            ] + source_lines[seal_index + 1:]
            normalized_source = "\n".join(normalized_lines) + "\n"
            computed_ast_seal = hashlib.sha256(
                normalized_source.encode("utf-8")
            ).hexdigest()
        else:
            computed_ast_seal = ""
        if computed_ast_seal != declared_ast_seal:
            errors.append("E_SOURCE_AST_SEAL")
    else:
        errors.append("E_SOURCE_AST_SEAL_SHAPE")
    anchor_assignments = [
        node for node in tree.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and node.targets[0].id == "SOURCE_POLICY_ANCHOR"
    ]
    anchor_shape_ok = len(anchor_assignments) == 1 and \
        isinstance(anchor_assignments[0].value, ast.Constant) and \
        isinstance(anchor_assignments[0].value.value, str) and \
        re.fullmatch(r"[0-9a-f]{64}", anchor_assignments[0].value.value) is not None
    if anchor_shape_ok and seal_shape_ok:
        declared_policy_anchor = anchor_assignments[0].value.value
        anchor_value = anchor_assignments[0].value
        anchor_lines = source.splitlines()
        anchor_locations_ok = True
        for value in (seal_value, anchor_value):
            index = value.lineno - 1
            literal = '"' + value.value + '"'
            location_ok = value.lineno == value.end_lineno and \
                0 <= index < len(anchor_lines) and \
                anchor_lines[index][value.col_offset:value.end_col_offset] == literal
            anchor_locations_ok = anchor_locations_ok and location_ok
            if location_ok:
                anchor_lines[index] = anchor_lines[index][:value.col_offset] + \
                    ('"' + "0" * 64 + '"') + anchor_lines[index][value.end_col_offset:]
        computed_policy_anchor = hashlib.sha256(
            ("\n".join(anchor_lines) + "\n").encode("utf-8")
        ).hexdigest() if anchor_locations_ok else ""
        if declared_policy_anchor != SOURCE_POLICY_ANCHOR or \
                computed_policy_anchor != SOURCE_POLICY_ANCHOR:
            errors.append("E_SOURCE_POLICY_ANCHOR")
    else:
        errors.append("E_SOURCE_POLICY_ANCHOR_SHAPE")
    expected_imports = (
        ("from", "__future__", 0, (("annotations", None),)),
        ("import", "", 0, (("argparse", None),)),
        ("import", "", 0, (("ast", None),)),
        ("import", "", 0, (("copy", None),)),
        ("import", "", 0, (("hashlib", None),)),
        ("import", "", 0, (("json", None),)),
        ("import", "", 0, (("math", None),)),
        ("import", "", 0, (("os", None),)),
        ("from", "pathlib", 0, (("Path", None),)),
        ("import", "", 0, (("re", None),)),
        ("import", "", 0, (("subprocess", None),)),
        ("import", "", 0, (("sys", None),)),
        ("from", "typing", 0, (("Any", None),)),
    )
    import_nodes = sorted(
        (node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))),
        key=node_location,
    )
    imports: list[tuple[str, str, int, tuple[tuple[str, str | None], ...]]] = []
    for node in import_nodes:
        kind = "import" if isinstance(node, ast.Import) else "from"
        module = "" if isinstance(node, ast.Import) else (node.module or "")
        level = 0 if isinstance(node, ast.Import) else node.level
        imports.append((kind, module, level,
                        tuple((alias.name, alias.asname) for alias in node.names)))
    if tuple(imports) != expected_imports:
        errors.append("E_IMPORT_INVENTORY")
    if any(isinstance(node, (ast.Lambda, ast.Yield, ast.YieldFrom,
                             ast.AsyncFunctionDef, ast.Await)) for node in ast.walk(tree)):
        errors.append("E_DYNAMIC_CALLABLE")
    if any(isinstance(node, ast.Match) for node in ast.walk(tree)):
        errors.append("E_PATTERN_MATCH")
    surface_nodes = sorted(
        (node for node in ast.walk(tree) if isinstance(node, (
            ast.Call, ast.Attribute, ast.Name, ast.FunctionDef, ast.ClassDef, ast.arg,
            ast.Global, ast.Nonlocal, ast.ExceptHandler,
        ))),
        key=node_location,
    )
    surface_tokens: list[str] = []
    for node in surface_nodes:
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                context = "S"
            elif isinstance(node.ctx, ast.Load):
                context = "L"
            else:
                context = "D"
            surface_tokens.append("N:" + context + ":" + node.id)
        elif isinstance(node, ast.FunctionDef):
            surface_tokens.append("F:" + node.name)
        elif isinstance(node, ast.ClassDef):
            surface_tokens.append("K:" + node.name)
        elif isinstance(node, ast.arg):
            surface_tokens.append("A:" + node.arg)
        elif isinstance(node, ast.Global):
            surface_tokens.append("G:" + ",".join(node.names))
        elif isinstance(node, ast.Nonlocal):
            surface_tokens.append("O:" + ",".join(node.names))
        elif isinstance(node, ast.ExceptHandler):
            surface_tokens.append("E:" + (node.name or ""))
        elif isinstance(node, ast.Attribute):
            surface_tokens.append("R:" + node.attr)
        elif isinstance(node.func, ast.Name):
            surface_tokens.append("C:N:" + node.func.id)
        elif isinstance(node.func, ast.Attribute):
            surface_tokens.append("C:A:" + node.func.attr)
        else:
            surface_tokens.append("C:DYNAMIC")
    surface_sha = hashlib.sha256("\n".join(surface_tokens).encode("utf-8")).hexdigest()
    if surface_sha != "830c9fa1b94df4019c9ab3c8a5a332daa646d278fb9840756bc4eb1339af4749":
        errors.append("E_AST_SYMBOL_SURFACE")
    function_inventory = tuple(node.name for node in sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)),
        key=node_location,
    ))
    expected_function_inventory = (
        "require", "sha256", "canonical", "pretty", "semantic_sha", "record_sha",
        "typed_equal", "strict_load", "pairs", "reject_constant", "is_oid",
        "call_owner_map", "__init__", "visit_FunctionDef", "visit_Call",
        "node_location", "replacement_root", "filesystem_receiver",
        "source_policy_errors", "validate_source_policy", "git_argv_allowed",
        "git_argv_controls", "run_git", "git_bytes", "git_text", "git_blob",
        "parse_name_status", "parse_ls_tree", "lf_bytes", "text_identity",
        "validate_units", "load_machine_inputs", "value_at", "expect",
        "validate_machine_facts", "build_conformance_rows", "select_gate",
        "gate_evaluation", "gate_controls", "read_human", "unique_prefixed_line",
        "validate_human_documents", "authority_boundary", "build_document",
        "nested_value", "singleton_diagnostics", "document_diagnostics",
        "semantic_controls", "json_controls", "load_artifact", "validate_document",
        "live_tip", "repository_identity_diagnostics", "repository_negative_controls",
        "parse_status", "status_diagnostics", "require_status",
        "common_repository_guard", "index_records", "validate_nonartifact_identities",
        "validate_repository", "atomic_collect", "execute", "main",
    )
    class_inventory = tuple(node.name for node in sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)),
        key=node_location,
    ))
    if function_inventory != expected_function_inventory or \
            class_inventory != ("ValidationError", "Visitor"):
        errors.append("E_FUNCTION_INVENTORY")
    module_allowed = {
        "argparse": {"ArgumentParser"},
        "ast": {
            "AST", "Add", "AnnAssign", "Assign", "AsyncFunctionDef", "Attribute", "AugAssign",
            "Await", "BinOp", "Call", "ClassDef", "Compare", "Constant", "Del", "Div",
            "Eq", "ExceptHandler", "FunctionDef", "Global", "If", "Import", "ImportFrom", "Lambda",
            "List", "Load", "Match", "Name", "NamedExpr", "NodeVisitor", "Nonlocal", "Raise",
            "Starred", "Store", "Subscript", "Yield", "YieldFrom", "arg", "dump",
            "iter_child_nodes", "parse", "walk",
        },
        "copy": {"deepcopy"},
        "hashlib": {"sha256"},
        "json": {"JSONDecodeError", "dumps", "loads"},
        "math": {"isfinite"},
        "os": {"fsync", "replace"},
        "re": {"fullmatch"},
        "subprocess": {"CompletedProcess", "DEVNULL", "PIPE", "TimeoutExpired", "run"},
        "sys": {"stderr"},
    }
    parents: dict[int, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[id(child)] = parent
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id.startswith("__") and \
                node.id not in {"__file__", "__name__"}:
            errors.append("E_DUNDER_NAME")
        if isinstance(node, ast.Name) and node.id in module_allowed:
            parent = parents.get(id(node))
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                errors.append("E_MODULE_TRANSPORT")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            errors.append("E_PRIVATE_ATTRIBUTE")
        if isinstance(node, ast.Call) and not isinstance(node.func, (ast.Name, ast.Attribute)):
            errors.append("E_DYNAMIC_CALL_TARGET")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and \
                node.value.id in module_allowed and \
                node.attr not in module_allowed[node.value.id]:
            errors.append("E_MODULE_API")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and \
                node.value.id == "subprocess" and node.attr not in {
                    "CompletedProcess", "DEVNULL", "PIPE", "TimeoutExpired", "run",
                }:
            errors.append("E_SUBPROCESS_API")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and \
                node.value.id == "os" and node.attr not in {"fsync", "replace"}:
            errors.append("E_OS_API")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and \
                node.value.id == "sys" and node.attr != "stderr":
            errors.append("E_SYS_API")
        if isinstance(node, ast.Attribute) and node.attr in {
                "Popen", "system", "popen", "spawn", "fork", "execv", "execve",
                "import_module", "run_module", "run_path", "write_text", "write_bytes",
                "mkdir", "makedirs", "rmdir", "removedirs", "remove", "rename", "renames",
                "touch", "chmod", "chown", "truncate", "symlink_to", "hardlink_to", "link_to",
                "copy", "copy_into", "move", "move_into", "lchmod", "kill", "killpg",
                "startfile", "read_text", "readlink", "iterdir", "glob", "rglob",
                "stat", "lstat", "samefile", "owner", "group", "is_dir", "is_symlink",
                "is_mount", "is_socket", "is_fifo", "is_block_device", "is_char_device",
                "is_junction", "writelines",
        }:
            errors.append("E_FORBIDDEN_ATTRIBUTE_REFERENCE")
        if isinstance(node, ast.Attribute) and node.attr == "walk" and not (
                isinstance(node.value, ast.Name) and node.value.id == "ast"):
            errors.append("E_FORBIDDEN_ATTRIBUTE_REFERENCE")
    attribute_targets: list[ast.Attribute] = []
    for node in ast.walk(tree):
        targets: list[ast.AST] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        for target in targets:
            attribute_targets.extend(
                part for part in ast.walk(target)
                if isinstance(part, ast.Attribute) and isinstance(part.ctx, ast.Store)
            )
    if len(attribute_targets) != 1 or not \
            isinstance(attribute_targets[0].value, ast.Name) or \
            attribute_targets[0].value.id != "self" or attribute_targets[0].attr != "stack":
        errors.append("E_ATTRIBUTE_ASSIGNMENT")
    forbidden_names = {
        "eval", "exec", "compile", "__import__", "breakpoint", "input", "open",
        "getattr", "setattr", "delattr", "globals", "locals", "vars",
        "run", "Popen", "system", "popen", "remove", "unlink", "rename", "quit", "exit",
        "help", "license", "credits", "copyright",
    }
    if any(isinstance(node, ast.Name) and node.id in forbidden_names
           for node in ast.walk(tree)):
        errors.append("E_FORBIDDEN_NAME_REFERENCE")
    forbidden_attributes = {
        "Popen", "system", "popen", "spawn", "fork", "execv", "execve",
        "import_module", "run_module", "run_path", "write_text", "write_bytes",
        "mkdir", "makedirs", "rmdir", "removedirs", "remove", "rename", "renames",
        "unlink", "touch", "chmod", "chown", "truncate", "symlink_to", "hardlink_to",
        "link_to", "copy", "copy_into", "move", "move_into", "lchmod",
        "is_dir", "is_symlink", "is_mount", "is_socket", "is_fifo", "is_block_device",
        "is_char_device", "is_junction", "writelines",
    }
    owners = call_owner_map(tree)
    if any(isinstance(node, ast.Name) and isinstance(node.ctx, ast.Del)
           for node in ast.walk(tree)):
        errors.append("E_NAME_DELETE")
    if any(isinstance(node, ast.ExceptHandler) and
           node.name in {"args", "frozen", "path", "temporary", "stream", "raw"}
           for node in ast.walk(tree)):
        errors.append("E_EXCEPTION_ALIAS")
    defined_symbols = set(expected_function_inventory) | set(class_inventory)
    if any(isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and
           node.id in defined_symbols for node in ast.walk(tree)):
        errors.append("E_DEFINED_SYMBOL_REBIND")
    critical_constants = (
        "ROOT", "SOURCE_AST_SEAL", "SOURCE_POLICY_ANCHOR", "BASELINE", "EXPECTED_PARENT", "BRANCH",
        "PROTECTED_BRANCH", "PROTECTED_TIP", "MAIN_TIP", "ORIGIN_URL", "SUBJECT",
        "GATE", "PERSISTENCE", "PRECOMMIT_STATUS", "PHASE066_VALIDATION",
        "PHASE066_VALIDATION_COMMIT", "PHASE066_VALIDATION_RAW_SHA256",
        "PHASE066_VALIDATION_SEMANTIC_SHA256", "VALIDATOR", "ARTIFACT", "REPORT",
        "GATE_RESULT", "RESULT", "PARENT_LEDGER", "ACTIVE_LEDGER", "HANDOVER",
        "FINAL_PATHS", "FINAL_STATUS", "NONARTIFACT_PATHS", "UNIT_SPECS",
        "MACHINE_SPECS", "MACHINE_PATHS", "KNOWN_COMMITS", "KNOWN_PATHS",
        "MAX_JSON_BYTES", "MAX_JSON_DEPTH", "MAX_JSON_NODES", "INCOMPLETE_STATUSES",
    )
    constant_store_counts = {name: 0 for name in critical_constants}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and \
                node.id in constant_store_counts:
            constant_store_counts[node.id] += 1
    if any(count != 1 for count in constant_store_counts.values()):
        errors.append("E_CRITICAL_CONSTANT_BINDING")
    critical_value_names = tuple(
        name for name in critical_constants
        if name not in {"SOURCE_AST_SEAL", "SOURCE_POLICY_ANCHOR"}
    )
    critical_value_assignments: dict[str, ast.AST] = {}
    critical_value_shape_ok = True
    for node in tree.body:
        target: ast.AST | None = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        elif isinstance(node, ast.AnnAssign):
            target = node.target
        if not isinstance(target, ast.Name) or target.id not in critical_value_names:
            continue
        if target.id in critical_value_assignments or node.end_lineno is None:
            critical_value_shape_ok = False
        critical_value_assignments[target.id] = node
    critical_value_shape_ok = critical_value_shape_ok and \
        set(critical_value_assignments) == set(critical_value_names)
    if critical_value_shape_ok:
        critical_value_tokens = []
        for name in critical_value_names:
            node = critical_value_assignments[name]
            segment = "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno])
            critical_value_tokens.append(name + "\0" + segment)
        critical_value_sha = hashlib.sha256(
            "\n\0".join(critical_value_tokens).encode("utf-8")
        ).hexdigest()
        if critical_value_sha != "1e74c9999d32b1e8243953648b03d3b0c64d42b1f5072dc610ed175efc303f1a":
            errors.append("E_CRITICAL_CONSTANT_VALUE")
    else:
        errors.append("E_CRITICAL_CONSTANT_VALUE")
    top_functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    critical_local_expected = {
        "run_git": {
            ("args", "Load"): 1,
            ("frozen", "Load"): 5,
            ("frozen", "Store"): 1,
        },
        "read_human": {
            ("path", "Load"): 3,
        },
        "load_artifact": {
            ("path", "Load"): 2,
            ("path", "Store"): 1,
        },
        "atomic_collect": {
            ("path", "Load"): 6,
            ("path", "Store"): 1,
            ("temporary", "Load"): 5,
            ("temporary", "Store"): 1,
            ("stream", "Load"): 3,
            ("stream", "Store"): 1,
            ("raw", "Load"): 1,
        },
    }
    critical_local_ok = set(top_functions) >= set(critical_local_expected)
    if critical_local_ok:
        for function_name, expected_contexts in critical_local_expected.items():
            relevant_names = {name for name, _ in expected_contexts}
            actual_contexts: dict[tuple[str, str], int] = {}
            for node in ast.walk(top_functions[function_name]):
                if not isinstance(node, ast.Name) or node.id not in relevant_names:
                    continue
                if isinstance(node.ctx, ast.Store):
                    context = "Store"
                elif isinstance(node.ctx, ast.Load):
                    context = "Load"
                else:
                    context = "Del"
                key = (node.id, context)
                actual_contexts[key] = actual_contexts.get(key, 0) + 1
            if actual_contexts != expected_contexts:
                critical_local_ok = False
    if not critical_local_ok:
        errors.append("E_CRITICAL_LOCAL_BINDING")
    root_assignments = [
        node for node in tree.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and node.targets[0].id == "ROOT"
    ]
    root_binding_ok = len(root_assignments) == 1
    if root_binding_ok:
        root_value = root_assignments[0].value
        root_binding_ok = isinstance(root_value, ast.Subscript) and \
            isinstance(root_value.slice, ast.Constant) and root_value.slice.value == 3 and \
            isinstance(root_value.value, ast.Attribute) and root_value.value.attr == "parents" and \
            isinstance(root_value.value.value, ast.Call) and \
            root_value.value.value.args == [] and root_value.value.value.keywords == [] and \
            isinstance(root_value.value.value.func, ast.Attribute) and \
            root_value.value.value.func.attr == "resolve" and \
            isinstance(root_value.value.value.func.value, ast.Call) and \
            len(root_value.value.value.func.value.args) == 1 and \
            isinstance(root_value.value.value.func.value.args[0], ast.Name) and \
            root_value.value.value.func.value.args[0].id == "__file__" and \
            root_value.value.value.func.value.keywords == [] and \
            isinstance(root_value.value.value.func.value.func, ast.Name) and \
            root_value.value.value.func.value.func.id == "Path"
    if not root_binding_ok:
        errors.append("E_ROOT_BINDING")
    artifact_assignments = [
        node for node in tree.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and node.targets[0].id == "ARTIFACT"
    ]
    if len(artifact_assignments) != 1 or \
            not isinstance(artifact_assignments[0].value, ast.Constant) or \
            artifact_assignments[0].value.value != "Codex/results/PHASE_067_VALIDATION.json":
        errors.append("E_ARTIFACT_BINDING")
    atomic_functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "atomic_collect"
    ]
    atomic_path_ok = len(atomic_functions) == 1 and len(atomic_functions[0].body) >= 5
    atomic_temp_ok = atomic_path_ok
    if atomic_path_ok:
        path_statement = atomic_functions[0].body[0]
        atomic_path_ok = isinstance(path_statement, ast.Assign) and \
            len(path_statement.targets) == 1 and \
            isinstance(path_statement.targets[0], ast.Name) and \
            path_statement.targets[0].id == "path" and \
            isinstance(path_statement.value, ast.BinOp) and \
            isinstance(path_statement.value.op, ast.Div) and \
            isinstance(path_statement.value.left, ast.Name) and \
            path_statement.value.left.id == "ROOT" and \
            isinstance(path_statement.value.right, ast.Name) and \
            path_statement.value.right.id == "ARTIFACT"
        temp_statement = atomic_functions[0].body[4]
        atomic_temp_ok = isinstance(temp_statement, ast.Assign) and \
            len(temp_statement.targets) == 1 and \
            isinstance(temp_statement.targets[0], ast.Name) and \
            temp_statement.targets[0].id == "temporary" and \
            isinstance(temp_statement.value, ast.Call) and \
            isinstance(temp_statement.value.func, ast.Attribute) and \
            isinstance(temp_statement.value.func.value, ast.Name) and \
            temp_statement.value.func.value.id == "path" and \
            temp_statement.value.func.attr == "with_name" and \
            len(temp_statement.value.args) == 1 and temp_statement.value.keywords == [] and \
            isinstance(temp_statement.value.args[0], ast.BinOp) and \
            isinstance(temp_statement.value.args[0].op, ast.Add) and \
            isinstance(temp_statement.value.args[0].left, ast.Attribute) and \
            isinstance(temp_statement.value.args[0].left.value, ast.Name) and \
            temp_statement.value.args[0].left.value.id == "path" and \
            temp_statement.value.args[0].left.attr == "name" and \
            isinstance(temp_statement.value.args[0].right, ast.Constant) and \
            temp_statement.value.args[0].right.value == ".tmp"
    if not atomic_path_ok:
        errors.append("E_ATOMIC_PATH_BINDING")
    if not atomic_temp_ok:
        errors.append("E_ATOMIC_TEMP_BINDING")
    load_functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "load_artifact"
    ]
    load_path_ok = len(load_functions) == 1 and len(load_functions[0].body) >= 1
    if load_path_ok:
        load_statement = load_functions[0].body[0]
        load_path_ok = isinstance(load_statement, ast.Assign) and \
            len(load_statement.targets) == 1 and \
            isinstance(load_statement.targets[0], ast.Name) and \
            load_statement.targets[0].id == "path" and \
            isinstance(load_statement.value, ast.BinOp) and \
            isinstance(load_statement.value.op, ast.Div) and \
            isinstance(load_statement.value.left, ast.Name) and \
            load_statement.value.left.id == "ROOT" and \
            isinstance(load_statement.value.right, ast.Name) and \
            load_statement.value.right.id == "ARTIFACT"
    if not load_path_ok:
        errors.append("E_LOAD_ARTIFACT_PATH_BINDING")
    read_human_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "read_human"
    ]
    read_human_ok = len(read_human_calls) == 1 and \
        owners.get(id(read_human_calls[0])) == "validate_human_documents" and \
        len(read_human_calls[0].args) == 1 and read_human_calls[0].keywords == [] and \
        isinstance(read_human_calls[0].args[0], ast.Name) and \
        read_human_calls[0].args[0].id == "path"
    if not read_human_ok:
        errors.append("E_READ_HUMAN_CALL_SHAPE")
    system_exit_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "SystemExit"
    ]
    system_exit_names = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "SystemExit"
    ]
    system_exit_ok = len(system_exit_calls) == 1 and len(system_exit_names) == 1 and \
        system_exit_calls[0].func is system_exit_names[0] and \
        owners.get(id(system_exit_calls[0])) == "<module>" and \
        len(system_exit_calls[0].args) == 1 and system_exit_calls[0].keywords == [] and \
        isinstance(system_exit_calls[0].args[0], ast.Call) and \
        isinstance(system_exit_calls[0].args[0].func, ast.Name) and \
        system_exit_calls[0].args[0].func.id == "main" and \
        system_exit_calls[0].args[0].args == [] and \
        system_exit_calls[0].args[0].keywords == []
    exit_raise = parents.get(id(system_exit_calls[0])) if system_exit_calls else None
    exit_guard = parents.get(id(exit_raise)) if exit_raise is not None else None
    guard_ok = isinstance(exit_raise, ast.Raise) and exit_raise.exc is system_exit_calls[0] and \
        isinstance(exit_guard, ast.If) and exit_guard.body == [exit_raise] and \
        exit_guard.orelse == [] and isinstance(exit_guard.test, ast.Compare) and \
        isinstance(exit_guard.test.left, ast.Name) and exit_guard.test.left.id == "__name__" and \
        len(exit_guard.test.ops) == 1 and isinstance(exit_guard.test.ops[0], ast.Eq) and \
        len(exit_guard.test.comparators) == 1 and \
        isinstance(exit_guard.test.comparators[0], ast.Constant) and \
        exit_guard.test.comparators[0].value == "__main__"
    if not system_exit_ok or not guard_ok:
        errors.append("E_SYSTEM_EXIT_SHAPE")
    parser_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and node.func.value.id == "argparse" and
        node.func.attr == "ArgumentParser"
    ]
    parser_attributes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and
        node.value.id == "argparse" and node.attr == "ArgumentParser"
    ]
    parser_ok = len(parser_calls) == 1 and len(parser_attributes) == 1 and \
        parser_calls[0].func is parser_attributes[0] and \
        owners.get(id(parser_calls[0])) == "main" and parser_calls[0].args == [] and \
        parser_calls[0].keywords == []
    if not parser_ok:
        errors.append("E_ARGUMENT_PARSER_SHAPE")
    parse_args_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
        node.func.attr == "parse_args"
    ]
    parse_args_attributes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and node.attr == "parse_args"
    ]
    parse_args_ok = len(parse_args_calls) == 1 and len(parse_args_attributes) == 1 and \
        parse_args_calls[0].func is parse_args_attributes[0] and \
        owners.get(id(parse_args_calls[0])) == "main" and \
        isinstance(parse_args_calls[0].func.value, ast.Name) and \
        parse_args_calls[0].func.value.id == "parser" and \
        parse_args_calls[0].args == [] and parse_args_calls[0].keywords == []
    if not parse_args_ok:
        errors.append("E_PARSE_ARGS_SHAPE")
    filesystem_attributes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and
        node.attr in {"exists", "is_file", "read_bytes", "resolve"}
    ]
    filesystem_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
        node.func.attr in {"exists", "is_file", "read_bytes", "resolve"}
    ]
    filesystem_surface_ok = len(filesystem_attributes) == len(filesystem_calls) and \
        len(filesystem_calls) == 12 and all(
            any(call.func is attribute for call in filesystem_calls)
            for attribute in filesystem_attributes
        )
    filesystem_surface = sorted(
        (node.func.attr, owners.get(id(node), "<module>"),
         filesystem_receiver(node.func.value))
        for node in filesystem_calls
    )
    expected_filesystem_surface = sorted((
        ("resolve", "<module>", "Path(__file__)"),
        ("read_bytes", "validate_source_policy", "ROOT/VALIDATOR"),
        ("read_bytes", "read_human", "ROOT/path"),
        ("read_bytes", "validate_human_documents", "ROOT/VALIDATOR"),
        ("read_bytes", "load_artifact", "path"),
        ("read_bytes", "validate_nonartifact_identities", "ROOT/path"),
        ("read_bytes", "validate_repository", "ROOT/path"),
        ("is_file", "load_artifact", "path"),
        ("exists", "validate_repository", "ROOT/ARTIFACT"),
        ("exists", "atomic_collect", "path"),
        ("exists", "atomic_collect", "temporary"),
        ("exists", "atomic_collect", "temporary"),
    ))
    if not filesystem_surface_ok or filesystem_surface != expected_filesystem_surface:
        errors.append("E_FILESYSTEM_READ_SURFACE")
    process_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and
        node.func.attr == "run"
    ]
    run_attributes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and
        node.value.id == "subprocess" and node.attr == "run"
    ]
    if len(process_calls) != 1 or len(run_attributes) != 1 or \
            (process_calls and run_attributes and process_calls[0].func is not run_attributes[0]):
        errors.append("E_PROCESS_CALL_COUNT")
    elif process_calls:
        call = process_calls[0]
        positional_ok = len(call.args) == 1 and isinstance(call.args[0], ast.List) and \
            len(call.args[0].elts) == 2 and isinstance(call.args[0].elts[0], ast.Constant) and \
            call.args[0].elts[0].value == "git" and isinstance(call.args[0].elts[1], ast.Starred) and \
            isinstance(call.args[0].elts[1].value, ast.Name) and \
            call.args[0].elts[1].value.id == "frozen"
        keywords = {item.arg: item.value for item in call.keywords if item.arg is not None}
        keyword_names_ok = len(keywords) == len(call.keywords) and set(keywords) == {
            "cwd", "stdin", "stdout", "stderr", "shell", "check", "timeout",
        }
        attribute_keywords_ok = all(
            isinstance(keywords.get(key), ast.Attribute) and
            isinstance(keywords[key].value, ast.Name) and
            keywords[key].value.id == "subprocess" and keywords[key].attr == value
            for key, value in (("stdin", "DEVNULL"), ("stdout", "PIPE"), ("stderr", "PIPE"))
        )
        scalar_keywords_ok = isinstance(keywords.get("cwd"), ast.Name) and \
            keywords["cwd"].id == "ROOT" and isinstance(keywords.get("shell"), ast.Constant) and \
            keywords["shell"].value is False and isinstance(keywords.get("check"), ast.Constant) and \
            keywords["check"].value is False and isinstance(keywords.get("timeout"), ast.Constant) and \
            keywords["timeout"].value == 60
        if not (owners.get(id(call)) == "run_git" and positional_ok and keyword_names_ok and
                attribute_keywords_ok and scalar_keywords_ok):
            errors.append("E_PROCESS_CALL_SHAPE")
    path_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "Path"
    ]
    path_names = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "Path"
    ]
    path_ok = len(path_calls) == 1 and len(path_names) == 1 and \
        path_calls[0].func is path_names[0] and owners.get(id(path_calls[0])) == "<module>" and \
        len(path_calls[0].args) == 1 and isinstance(path_calls[0].args[0], ast.Name) and \
        path_calls[0].args[0].id == "__file__" and path_calls[0].keywords == []
    if not path_ok:
        errors.append("E_PATH_CONSTRUCTOR_SHAPE")
    os_replace_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and
        node.func.attr == "replace"
    ]
    os_replace_attributes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and
        node.value.id == "os" and node.attr == "replace"
    ]
    replace_ok = len(os_replace_calls) == 1 and len(os_replace_attributes) == 1 and \
        os_replace_calls[0].func is os_replace_attributes[0] and \
        owners.get(id(os_replace_calls[0])) == "atomic_collect" and \
        len(os_replace_calls[0].args) == 2 and \
        all(isinstance(item, ast.Name) for item in os_replace_calls[0].args) and \
        [item.id for item in os_replace_calls[0].args] == ["temporary", "path"] and \
        os_replace_calls[0].keywords == []
    if not replace_ok:
        errors.append("E_ATOMIC_REPLACE_SHAPE")
    atomic_specs = (
        ("open", "temporary", ("xb",), "E_ATOMIC_OPEN_SHAPE"),
        ("write", "stream", ("raw",), "E_ATOMIC_WRITE_SHAPE"),
        ("flush", "stream", (), "E_ATOMIC_FLUSH_SHAPE"),
        ("unlink", "temporary", (), "E_ATOMIC_UNLINK_SHAPE"),
    )
    for attr, receiver, expected_args, error_code in atomic_specs:
        calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
            node.func.attr == attr
        ]
        attributes = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Attribute) and node.attr == attr
        ]
        shape_ok = len(calls) == 1 and len(attributes) == 1 and \
            calls[0].func is attributes[0] and owners.get(id(calls[0])) == "atomic_collect" and \
            isinstance(calls[0].func.value, ast.Name) and \
            calls[0].func.value.id == receiver and calls[0].keywords == []
        if shape_ok and attr == "open":
            shape_ok = len(calls[0].args) == 1 and \
                isinstance(calls[0].args[0], ast.Constant) and \
                calls[0].args[0].value == expected_args[0]
        elif shape_ok and attr == "write":
            shape_ok = len(calls[0].args) == 1 and isinstance(calls[0].args[0], ast.Name) and \
                calls[0].args[0].id == expected_args[0]
        elif shape_ok:
            shape_ok = calls[0].args == []
        if not shape_ok:
            errors.append(error_code)
    os_fsync_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and
        node.func.attr == "fsync"
    ]
    os_fsync_attributes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and
        node.value.id == "os" and node.attr == "fsync"
    ]
    fsync_ok = len(os_fsync_calls) == 1 and len(os_fsync_attributes) == 1 and \
        os_fsync_calls[0].func is os_fsync_attributes[0] and \
        owners.get(id(os_fsync_calls[0])) == "atomic_collect" and \
        len(os_fsync_calls[0].args) == 1 and os_fsync_calls[0].keywords == [] and \
        isinstance(os_fsync_calls[0].args[0], ast.Call) and \
        isinstance(os_fsync_calls[0].args[0].func, ast.Attribute) and \
        isinstance(os_fsync_calls[0].args[0].func.value, ast.Name) and \
        os_fsync_calls[0].args[0].func.value.id == "stream" and \
        os_fsync_calls[0].args[0].func.attr == "fileno" and \
        os_fsync_calls[0].args[0].args == [] and os_fsync_calls[0].args[0].keywords == []
    if not fsync_ok:
        errors.append("E_ATOMIC_FSYNC_SHAPE")
    text_replace_counts: dict[tuple[str, str], int] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or \
                node.func.attr != "replace":
            continue
        if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
            continue
        root = replacement_root(node.func.value)
        root_name = root.id if isinstance(root, ast.Name) else ""
        key = (owners.get(id(node), "<module>"), root_name)
        text_replace_counts[key] = text_replace_counts.get(key, 0) + 1
    if text_replace_counts != {
            ("validate_source_policy", "source"): 3,
            ("lf_bytes", "raw"): 2,
            ("value_at", "encoded"): 2,
    }:
        errors.append("E_TEXT_REPLACE_CALLS")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            value = node.value
            if isinstance(value, ast.Attribute) and value.attr in {"run", "Popen", "write_text",
                                                                   "write_bytes", "replace", "unlink"}:
                errors.append("E_CALLABLE_TRANSPORT")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        owner = owners.get(id(node), "<module>")
        if isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
            errors.append("E_FORBIDDEN_CALL")
        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            if attr in forbidden_attributes:
                allowed = attr == "unlink" and owner == "atomic_collect"
                if not allowed:
                    errors.append("E_MUTATION_CALL")
            if attr == "replace":
                os_replace = isinstance(node.func.value, ast.Name) and node.func.value.id == "os"
                root = replacement_root(node.func.value)
                safe_text_replace = isinstance(root, ast.Name) and \
                    (owner, root.id) in {
                        ("validate_source_policy", "source"),
                        ("lf_bytes", "raw"),
                        ("value_at", "encoded"),
                    }
                if (os_replace and owner != "atomic_collect") or \
                        (not os_replace and not safe_text_replace):
                    errors.append("E_MUTATION_CALL")
            if attr == "run":
                if not (owner == "run_git" and isinstance(node.func.value, ast.Name) and
                        node.func.value.id == "subprocess"):
                    errors.append("E_PROCESS_CALL")
                keywords = {item.arg: item.value for item in node.keywords if item.arg is not None}
                shell = keywords.get("shell")
                if not isinstance(shell, ast.Constant) or shell.value is not False:
                    errors.append("E_PROCESS_SHELL")
            if attr == "open":
                allowed = owner == "atomic_collect" and node.args and \
                    isinstance(node.args[0], ast.Constant) and node.args[0].value == "xb"
                if not allowed:
                    errors.append("E_OPEN_CALL")
        if isinstance(node.func, ast.Name) and node.func.id == "Path" and node.args and \
                isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str) and \
                (node.args[0].value.startswith("\\\\") or node.args[0].value.startswith("//")):
            errors.append("E_UNC_LITERAL")
    return sorted(set(errors))


def validate_source_policy() -> int:
    source = (ROOT / VALIDATOR).read_bytes().decode("utf-8")
    errors = source_policy_errors(source)
    require(errors == [], "E_SOURCE_POLICY", ",".join(errors))
    snippets = (
        "import socket",
        "from urllib import request",
        "eval('1')",
        "exec('x=1')",
        "__import__('os')",
        "runner = subprocess.run\nrunner(['git', 'status'])",
        "subprocess.run(['git', 'status'], shell=True)",
        "subprocess.Popen(['git', 'status'])",
        "os.system('git status')",
        "Path('x').write_text('x')",
        "Path('x').replace('y')",
        "Path('x').unlink()",
        "Path('x').open('w')",
        "Path(r'\\\\server\\share\\x').read_bytes()",
        "(lambda: 1)()",
        "breakpoint()",
        "from subprocess import run\nrun(['git', 'status'])",
        "def nested_process():\n    from subprocess import run\n    run(['git', 'status'])",
        "getattr(subprocess, 'run')(['git', 'status'], shell=False)",
        "from os import remove\nremove('x')",
        "runner = [subprocess.run][0]\nrunner(['git', 'status'])",
        "os.__dict__['remove']('x')",
        "subprocess.__dict__['run'](['git', 'status'], shell=True)",
        "subprocess.call(['git', 'status'])",
        "subprocess.check_output(['git', 'status'])",
        "os.write(1, b'x')",
        "os.spawnlp(0, 'git', 'git', 'status')",
        "__builtins__['open']('outside', 'w').write('x')",
        "Path(chr(92) * 2 + 'server/share/x').read_bytes()",
        "Path.__dict__['write_text'](Path('x'), 'x')",
        "sys.modules['subprocess'].call(['git', 'status'])",
        "sys.modules['subprocess'].check_output(['git', 'status'])",
        "sys.modules['pathlib'].Path(chr(92) * 2 + 'server/share/x').read_bytes()",
        "ROOT.replace(ROOT.with_name('moved'))",
        "ROOT.symlink_to('outside')",
        "process_module = subprocess\nprocess_module.call(['git', 'status'])",
        "operating_module = os\noperating_module.remove('x')",
        "ROOT.copy(ROOT.parent / 'outside')",
        "ROOT.copy_into(ROOT.parent / 'outside')",
        "ROOT.move(ROOT.parent / 'outside')",
        "ROOT.move_into(ROOT.parent / 'outside')",
        "ROOT.lchmod(0o777)",
        "mover = ROOT.rename\nmover(ROOT.parent / 'outside')",
        "maker = ROOT.mkdir\nmaker()",
        "mode_change = ROOT.chmod\nmode_change(0o777)",
        "copier = ROOT.copy\ncopier(ROOT.parent / 'outside')",
        "argparse._os.spawnlp(0, 'git', 'git', 'status')",
        "argparse._sys.exit(0)",
        "argparse._sys.modules['subprocess'].call(['git', 'status'], shell=True)",
        "argparse._sys.modules['builtins'].exec('import socket')",
        "argparse.FileType('w')('outside')",
        "argparse.FileType('r')(chr(92) * 2 + 'server/share/x')",
        "argparse.ArgumentParser(fromfile_prefix_chars='@').parse_args(['@outside'])",
        "(ROOT.parent / 'outside').read_bytes()",
        "quit()",
        "exit()",
        "raise SystemExit(0)",
        "writer = open\nwriter('outside', 'w')",
        "evaluator = eval\nevaluator('1')",
        "executor = exec\nexecutor('import socket')",
        "stopper = quit\nstopper()",
        "stopper = exit\nstopper()",
        "debugger = breakpoint\ndebugger()",
        "help('socket')",
        "license()",
        "credits()",
        "copyright()",
        "(ROOT.parent / 'outside').is_dir()",
        "match ('reset', '--hard'):\n    case frozen:\n        pass",
        "match '../outside':\n    case path:\n        pass",
    )
    for index, snippet in enumerate(snippets):
        require(source_policy_errors(source + "\n" + snippet + "\n") != [],
                "E_SOURCE_POLICY_CONTROL", str(index))
    needle = "    return result\n\n\ndef git_bytes"
    mutant = source.replace(
        needle,
        "    subprocess.run(['python', '-V'], shell=False)\n    return result\n\n\ndef git_bytes",
        1,
    )
    require(mutant != source and source_policy_errors(mutant) != [],
            "E_SOURCE_POLICY_CONTROL", "run_git_extra_process")
    mutation_controls = (
        ("        os.replace(temporary, path)\n",
         "        os.replace(temporary, path)\n        os.replace(temporary, path)\n",
         "E_ATOMIC_REPLACE_SHAPE", "atomic_extra_replace"),
        ('        with temporary.open("xb") as stream:\n',
         '        temporary.open("xb")\n        with temporary.open("xb") as stream:\n',
         "E_ATOMIC_OPEN_SHAPE", "atomic_extra_open"),
        ("            stream.write(raw)\n",
         "            stream.write(raw)\n            stream.write(raw)\n",
         "E_ATOMIC_WRITE_SHAPE", "atomic_extra_write"),
        ("            stream.flush()\n",
         "            stream.flush()\n            stream.flush()\n",
         "E_ATOMIC_FLUSH_SHAPE", "atomic_extra_flush"),
        ("            os.fsync(stream.fileno())\n",
         "            os.fsync(stream.fileno())\n            os.fsync(stream.fileno())\n",
         "E_ATOMIC_FSYNC_SHAPE", "atomic_extra_fsync"),
        ("            temporary.unlink()\n",
         "            temporary.unlink()\n            temporary.unlink()\n",
         "E_ATOMIC_UNLINK_SHAPE", "atomic_extra_unlink"),
        ("            stream.write(raw)\n",
         "            stream.write(raw)\n            stream.writelines([raw])\n",
         "E_AST_SYMBOL_SURFACE", "atomic_extra_writelines"),
        ("        raw, text = read_human(path)\n",
         '        raw, text = read_human("../outside")\n',
         "E_READ_HUMAN_CALL_SHAPE", "read_human_external_argument"),
    )
    for before, after, expected_error, label in mutation_controls:
        mutant = source.replace(before, after, 1)
        mutant_errors = source_policy_errors(mutant)
        require(mutant != source and expected_error in mutant_errors,
                "E_SOURCE_POLICY_CONTROL", label)
    binding_controls = (
        ("ROOT = Path(__file__).resolve().parents[3]\n",
         "ROOT = Path(__file__).resolve().parents[4]\n",
         "E_ROOT_BINDING", "root_parent_retarget"),
        ('ARTIFACT = "Codex/results/PHASE_067_VALIDATION.json"\n',
         'ARTIFACT = "../outside.json"\n',
         "E_ARTIFACT_BINDING", "artifact_constant_retarget"),
        ("    path = ROOT / ARTIFACT\n    require(path == ROOT / ARTIFACT, \"E_OUTPUT_PATH\")\n",
         "    path = ROOT.parent / \"outside\"\n    require(path == path, \"E_OUTPUT_PATH\")\n",
         "E_ATOMIC_PATH_BINDING", "atomic_destination_retarget"),
        ("def load_artifact() -> tuple[dict[str, Any], bytes, int, int]:\n    path = ROOT / ARTIFACT\n",
         "def load_artifact() -> tuple[dict[str, Any], bytes, int, int]:\n    path = ROOT.parent / \"outside\"\n",
         "E_LOAD_ARTIFACT_PATH_BINDING", "artifact_read_retarget"),
        ('    temporary = path.with_name(path.name + ".tmp")\n    require(not temporary.exists(), "E_TEMP_EXISTS")\n',
         '    temporary = path.with_name(path.name + ".tmp")\n    path = ROOT / PARENT_LEDGER\n    require(not temporary.exists(), "E_TEMP_EXISTS")\n',
         "E_CRITICAL_LOCAL_BINDING", "atomic_path_rebind"),
        ("        os.replace(temporary, path)\n",
         "        temporary = ROOT / PARENT_LEDGER\n        os.replace(temporary, path)\n",
         "E_CRITICAL_LOCAL_BINDING", "atomic_temporary_rebind"),
        ('        with temporary.open("xb") as stream:\n            stream.write(raw)\n',
         '        with temporary.open("xb") as stream:\n            stream = raw\n            stream.write(raw)\n',
         "E_CRITICAL_LOCAL_BINDING", "atomic_stream_rebind"),
        ("def atomic_collect(raw: bytes) -> None:\n    path = ROOT / ARTIFACT\n",
         "def atomic_collect(raw: bytes) -> None:\n    raw = b\"{}\"\n    path = ROOT / ARTIFACT\n",
         "E_CRITICAL_LOCAL_BINDING", "atomic_raw_rebind"),
        ('    require(git_argv_allowed(frozen), "E_GIT_ARGV", repr(frozen))\n    try:\n',
         '    require(git_argv_allowed(frozen), "E_GIT_ARGV", repr(frozen))\n    frozen = ("reset", "--hard")\n    try:\n',
         "E_CRITICAL_LOCAL_BINDING", "git_frozen_rebind"),
        ("def read_human(path: str) -> tuple[bytes, str]:\n    raw = (ROOT / path).read_bytes()\n",
         "def read_human(path: str) -> tuple[bytes, str]:\n    path = \"../outside\"\n    raw = (ROOT / path).read_bytes()\n",
         "E_CRITICAL_LOCAL_BINDING", "read_human_path_rebind"),
        ('    require(path.is_file(), "E_ARTIFACT_MISSING")\n    raw = path.read_bytes()\n',
         '    require(path.is_file(), "E_ARTIFACT_MISSING")\n    path = ROOT / PARENT_LEDGER\n    raw = path.read_bytes()\n',
         "E_CRITICAL_LOCAL_BINDING", "load_artifact_path_rebind"),
        ("\n\ndef main() -> int:\n",
         "\n\nrequire = print\n\n\ndef main() -> int:\n",
         "E_DEFINED_SYMBOL_REBIND", "require_rebind"),
        ("\n\ndef git_argv_allowed(args: tuple[str, ...]) -> bool:\n",
         "\n\ndef validate_source_policy() -> int:\n    return 107\n\n\ndef git_argv_allowed(args: tuple[str, ...]) -> bool:\n",
         "E_FUNCTION_INVENTORY", "duplicate_source_policy_gate"),
        ("        os.replace(temporary, path)\n",
         "        del temporary\n        os.replace(temporary, path)\n",
         "E_NAME_DELETE", "atomic_temporary_delete"),
        ('SUBJECT = "audit(phase067): close code history gate"\n',
         'SUBJECT = "audit(phase067): close code history gate"\nSUBJECT: str = "rewritten"\n',
         "E_CRITICAL_CONSTANT_BINDING", "subject_rebind"),
        ('BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"\n',
         'BASELINE = "0000000000000000000000000000000000000000"\n',
         "E_CRITICAL_CONSTANT_VALUE", "baseline_literal_retarget"),
        ('SUBJECT = "audit(phase067): close code history gate"\n',
         'SUBJECT = "audit(phase067): rewritten"\n',
         "E_CRITICAL_CONSTANT_VALUE", "subject_literal_retarget"),
        ('GATE = "CONDITIONAL_P067"\n',
         'GATE = "PASS_P067"\n',
         "E_CRITICAL_CONSTANT_VALUE", "gate_literal_retarget"),
        ('PERSISTENCE = "PASS_P067_STEP90_2_PERSISTENCE"\n',
         'PERSISTENCE = "PASS_REWRITTEN"\n',
         "E_CRITICAL_CONSTANT_VALUE", "persistence_literal_retarget"),
        ('PRECOMMIT_STATUS = "CONDITIONAL_PENDING_PERSISTENCE"\n',
         'PRECOMMIT_STATUS = "PASS_PENDING_PERSISTENCE"\n',
         "E_CRITICAL_CONSTANT_VALUE", "precommit_literal_retarget"),
        ("MAX_JSON_BYTES = 8_000_000\n",
         "MAX_JSON_BYTES = 80_000_000\n",
         "E_CRITICAL_CONSTANT_VALUE", "max_json_bytes_literal_retarget"),
        ('INCOMPLETE_STATUSES = frozenset({"PARTIAL", "NOT_TESTED", "GROUND_NOT_FOUND"})\n',
         'INCOMPLETE_STATUSES = frozenset({"PASS", "NOT_TESTED", "GROUND_NOT_FOUND"})\n',
         "E_CRITICAL_CONSTANT_VALUE", "incomplete_statuses_value_retarget"),
        ('REPORT = "Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md"\n',
         'REPORT = "../outside.md"\n',
         "E_CRITICAL_CONSTANT_VALUE", "report_path_retarget"),
        ("    except Exception:\n        if temporary.exists():\n",
         "    except Exception as temporary:\n        if temporary.exists():\n",
         "E_EXCEPTION_ALIAS", "atomic_exception_critical_alias"),
        ("    except Exception:\n        if temporary.exists():\n",
         "    except Exception as captured:\n        if temporary.exists():\n",
         "E_AST_SYMBOL_SURFACE", "atomic_exception_generic_alias"),
        ("def require(ok: bool, code: str, detail: str = \"\") -> None:\n    if not ok:\n",
         "def require(ok: bool, code: str, detail: str = \"\") -> None:\n    if not ok and False:\n",
         "E_SOURCE_POLICY_ANCHOR", "require_fail_closed_control_flow"),
        ("def validate_source_policy() -> int:\n    source = (ROOT / VALIDATOR).read_bytes().decode(\"utf-8\")\n",
         "def validate_source_policy() -> int:\n    return 0\n    source = (ROOT / VALIDATOR).read_bytes().decode(\"utf-8\")\n",
         "E_SOURCE_POLICY_ANCHOR", "source_policy_early_return"),
        ("def main() -> int:\n    try:\n",
         "def main() -> int:\n    return 0\n    try:\n",
         "E_SOURCE_POLICY_ANCHOR", "main_early_return"),
    )
    for before, after, expected_error, label in binding_controls:
        mutant = source.replace(before, after, 1)
        mutant_errors = source_policy_errors(mutant)
        require(mutant != source and expected_error in mutant_errors,
                "E_SOURCE_POLICY_CONTROL", label)
    return len(snippets) + 1 + len(mutation_controls) + len(binding_controls)


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    if not args or any(not isinstance(item, str) or any(ch in item for ch in "\0\r\n")
                       for item in args):
        return False
    fixed = {
        ("rev-parse", "HEAD"),
        ("rev-parse", "@{u}"),
        ("rev-parse", f"refs/remotes/origin/{BRANCH}"),
        ("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"),
        ("rev-parse", f"refs/heads/{PROTECTED_BRANCH}"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("remote", "get-url", "origin"),
        ("status", "--porcelain=v1", "-z", "--untracked-files=all"),
        ("diff", "--cached", "--name-only"),
        ("diff", "--name-only"),
        ("show-ref", "--verify", "--quiet", "refs/heads/main"),
        ("ls-files", "--stage", "--", *FINAL_PATHS),
    }
    if args in fixed:
        return True
    if len(args) == 4 and args[:3] == ("ls-remote", "--heads", "origin"):
        return args[3] in {
            f"refs/heads/{BRANCH}", f"refs/heads/{PROTECTED_BRANCH}", "refs/heads/main",
        }
    if len(args) == 4 and args[0] == "show" and args[1] == "--no-patch" and \
            args[2] in {"--format=%P", "--format=%s"}:
        return is_oid(args[3])
    if len(args) == 7 and args[:5] == (
            "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames"):
        return is_oid(args[5]) and args[6] == "--"
    if len(args) >= 4 and args[0] == "ls-tree" and is_oid(args[1]) and args[2] == "--":
        return all(path in KNOWN_PATHS for path in args[3:])
    if len(args) == 2 and args[0] == "show" and ":" in args[1]:
        commit, path = args[1].split(":", 1)
        return (is_oid(commit) or commit == "") and path in KNOWN_PATHS
    if len(args) == 6 and args[:4] == ("diff", "--cached", "--name-status", "--no-renames"):
        return args[4] == EXPECTED_PARENT and args[5] == "--"
    if len(args) == 5 and args[:2] == ("diff", "--name-only"):
        return args[2] == PROTECTED_TIP and is_oid(args[3]) and args[4] == "--"
    if len(args) == 6 and args[:2] == ("diff", "--name-only"):
        return args[2] == PROTECTED_TIP and is_oid(args[3]) and \
            args[4:] == ("--", "Claude")
    return False


def git_argv_controls() -> int:
    accepted = (
        ("rev-parse", "HEAD"),
        ("rev-parse", "@{u}"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("show", "--no-patch", "--format=%P", EXPECTED_PARENT),
        ("show", EXPECTED_PARENT + ":" + MACHINE_PATHS[-1]),
        ("ls-tree", EXPECTED_PARENT, "--", MACHINE_PATHS[-1]),
        ("diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames",
         EXPECTED_PARENT, "--"),
        ("diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--"),
        ("diff", "--name-only", PROTECTED_TIP, EXPECTED_PARENT, "--", "Claude"),
    )
    rejected = (
        ("fetch",),
        ("clean", "-fd"),
        ("reset", "--hard"),
        ("show", "--no-patch", "--format=%P", "-HEAD"),
        ("show", EXPECTED_PARENT + ":../outside"),
        ("ls-tree", EXPECTED_PARENT, "--", "outside"),
        ("diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames",
         EXPECTED_PARENT, "outside"),
        ("ls-remote", "--heads", "evil", f"refs/heads/{BRANCH}"),
        ("diff", "--name-only", PROTECTED_TIP, EXPECTED_PARENT, "--", "Codex"),
    )
    require(all(git_argv_allowed(item) for item in accepted), "E_GIT_ARGV_POSITIVE")
    require(not any(git_argv_allowed(item) for item in rejected), "E_GIT_ARGV_NEGATIVE")
    return len(accepted) + len(rejected)


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    frozen = tuple(args)
    require(git_argv_allowed(frozen), "E_GIT_ARGV", repr(frozen))
    try:
        result = subprocess.run(["git", *frozen], cwd=ROOT, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=False, check=False, timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise ValidationError("E_GIT_TIMEOUT:" + " ".join(frozen)) from exc
    if check:
        require(result.returncode == 0, "E_GIT_COMMAND",
                " ".join(frozen) + ":" + result.stderr.decode("utf-8", "replace").strip())
    return result


def git_bytes(args: list[str]) -> bytes:
    return run_git(args).stdout


def git_text(args: list[str]) -> str:
    return git_bytes(args).decode("utf-8").rstrip("\r\n")


def git_blob(commit: str, path: str) -> bytes:
    return git_bytes(["show", commit + ":" + path])


def parse_name_status(raw: bytes, label: str) -> dict[str, str]:
    result: dict[str, str] = {}
    text = raw.decode("utf-8")
    for line in text.splitlines():
        fields = line.split("\t")
        require(len(fields) == 2 and fields[0] in {"A", "M"}, label + "_ROW", line)
        require(fields[1] not in result, label + "_DUPLICATE", fields[1])
        result[fields[1]] = fields[0]
    return result


def parse_ls_tree(raw: bytes, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for line in raw.decode("utf-8").splitlines():
        left, path = line.split("\t", 1)
        mode, kind, oid = left.split(" ")
        require(kind == "blob" and mode == "100644" and is_oid(oid), label + "_ROW", path)
        require(path not in result, label + "_DUPLICATE", path)
        result[path] = {"mode": mode, "blob_oid": oid}
    return result


def lf_bytes(raw: bytes, label: str) -> bytes:
    require(not raw.startswith(b"\xef\xbb\xbf"), label + "_BOM")
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(label + "_UTF8") from exc
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def text_identity(path: str, raw: bytes) -> dict[str, Any]:
    normalized = lf_bytes(raw, "E_TEXT_" + path)
    return {
        "path": path,
        "lf_bytes": len(normalized),
        "lf_sha256": sha256(normalized),
    }


def validate_units() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    previous: str | None = None
    for spec in UNIT_SPECS:
        commit = spec["commit"]
        parent = git_text(["show", "--no-patch", "--format=%P", commit])
        subject = git_text(["show", "--no-patch", "--format=%s", commit])
        require(parent == spec["parent"], "E_UNIT_PARENT", spec["step"])
        require(subject == spec["subject"], "E_UNIT_SUBJECT", spec["step"])
        if previous is not None:
            require(parent == previous, "E_UNIT_CHAIN", spec["step"])
        previous = commit
        expected_status = {
            path: ("A" if index < spec["added"] else "M")
            for index, path in enumerate(spec["paths"])
        }
        actual_status = parse_name_status(git_bytes([
            "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames",
            commit, "--",
        ]), "E_UNIT_DIFF_" + spec["step"])
        require(actual_status == expected_status, "E_UNIT_DIFF", spec["step"])
        tree = parse_ls_tree(git_bytes(["ls-tree", commit, "--", *spec["paths"]]),
                             "E_UNIT_TREE_" + spec["step"])
        require(set(tree) == set(spec["paths"]), "E_UNIT_TREE", spec["step"])
        paths: list[dict[str, Any]] = []
        for path in spec["paths"]:
            raw = git_blob(commit, path)
            paths.append({
                "path": path,
                "status": expected_status[path],
                "mode": tree[path]["mode"],
                "blob_oid": tree[path]["blob_oid"],
                "raw_bytes": len(raw),
                "raw_sha256": sha256(raw),
            })
        records.append({
            "step": spec["step"],
            "commit": commit,
            "sole_parent": parent,
            "subject": subject,
            "content_gate": spec["gate"],
            "persistence_terminal": spec["terminal"],
            "changed_path_count": len(paths),
            "path_records": paths,
            "canonical_reuse": "COMMITTED_BYTES_NOT_FRESH_HISTORICAL_REPLAY",
        })
    require(previous == EXPECTED_PARENT, "E_UNIT_TIP")
    return records


def load_machine_inputs() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], int, int]:
    documents: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    total_nodes = 0
    maximum_depth = 0
    for path, introduced, raw_expected, semantic_expected, raw_style, semantic_style in MACHINE_SPECS:
        raw = git_blob(EXPECTED_PARENT, path)
        require(sha256(raw) == raw_expected, "E_INPUT_RAW", path)
        value, nodes, depth = strict_load(raw, "E_INPUT_" + path,
                                          raw_style, semantic_style)
        require(value.get("semantic_sha256") == semantic_expected,
                "E_INPUT_DECLARED_SEMANTIC", path)
        require(semantic_sha(value, semantic_style) == semantic_expected,
                "E_INPUT_RECOMPUTED_SEMANTIC", path)
        intro_raw = git_blob(introduced, path)
        require(intro_raw == raw, "E_INPUT_INTRODUCTION_DRIFT", path)
        tree = parse_ls_tree(git_bytes(["ls-tree", introduced, "--", path]),
                             "E_INPUT_TREE_" + path)
        require(set(tree) == {path}, "E_INPUT_TREE", path)
        documents[path] = value
        records.append({
            "path": path,
            "read_from_commit": EXPECTED_PARENT,
            "introduced_by_commit": introduced,
            "mode": tree[path]["mode"],
            "blob_oid": tree[path]["blob_oid"],
            "raw_bytes": len(raw),
            "raw_sha256": raw_expected,
            "declared_semantic_sha256": semantic_expected,
            "recomputed_semantic_sha256": semantic_expected,
            "raw_style": raw_style,
            "semantic_style": semantic_style,
            "nodes": nodes,
            "depth": depth,
        })
        total_nodes += nodes
        maximum_depth = max(maximum_depth, depth)
    return documents, records, total_nodes, maximum_depth


def value_at(document: Any, pointer: str, label: str) -> Any:
    require(pointer == "" or pointer.startswith("/"), label + "_POINTER")
    current = document
    if pointer == "":
        return current
    for encoded in pointer[1:].split("/"):
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            require(token in current, label + "_KEY", token)
            current = current[token]
        elif isinstance(current, list):
            require(token.isdigit(), label + "_INDEX", token)
            index = int(token)
            require(0 <= index < len(current), label + "_INDEX", token)
            current = current[index]
        else:
            raise ValidationError(label + "_SCALAR:" + token)
    return current


def expect(document: dict[str, Any], pointer: str, expected: Any, code: str) -> None:
    require(typed_equal(value_at(document, pointer, code), expected), code, pointer)


def validate_machine_facts(documents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    inventory = documents[MACHINE_PATHS[0]]
    attestation = documents[MACHINE_PATHS[1]]
    flow = documents[MACHINE_PATHS[2]]
    graph = documents[MACHINE_PATHS[3]]
    defaults = documents[MACHINE_PATHS[4]]
    saved_runtime = documents[MACHINE_PATHS[5]]
    tests = documents[MACHINE_PATHS[6]]
    guide = documents[MACHINE_PATHS[7]]
    units = documents[MACHINE_PATHS[8]]
    guards = documents[MACHINE_PATHS[9]]
    fitting = documents[MACHINE_PATHS[10]]
    fitting_runtime = documents[MACHINE_PATHS[11]]
    source = documents[MACHINE_PATHS[12]]
    carry = documents[MACHINE_PATHS[13]]
    phase066_raw = git_blob(EXPECTED_PARENT, PHASE066_VALIDATION)
    require(sha256(phase066_raw) == PHASE066_VALIDATION_RAW_SHA256,
            "E_FACT_P066_RAW")
    require(git_blob(PHASE066_VALIDATION_COMMIT, PHASE066_VALIDATION) == phase066_raw,
            "E_FACT_P066_INTRODUCTION_DRIFT")
    phase066, _, _ = strict_load(
        phase066_raw, "E_FACT_P066_VALIDATION", "pretty", "legacy",
    )
    require(phase066.get("semantic_sha256") == PHASE066_VALIDATION_SEMANTIC_SHA256,
            "E_FACT_P066_DECLARED_SEMANTIC")
    expect(phase066, "/gate", "CONDITIONAL_P066", "E_FACT_P066_GATE")
    expect(phase066, "/persistence_terminal", "PASS_P066_STEP81_2_PERSISTENCE",
           "E_FACT_P066_PERSISTENCE")
    expect(phase066, "/authority_ceiling/main_scholarly_body_modified", False,
           "E_FACT_P066_SCHOLARLY_BODY")

    expect(inventory, "/universe/occurrences", 129, "E_FACT_OCCURRENCES")
    expect(inventory, "/universe/unique_blobs", 84, "E_FACT_BLOBS")
    expect(inventory, "/universe/unique_blob_physical_lines", 29952, "E_FACT_LINES")
    expect(inventory, "/universe/releases", 20, "E_FACT_RELEASES")
    expect(inventory, "/universe/role_occurrence_counts",
           {"code": 20, "demo": 30, "result": 35, "test": 44}, "E_FACT_ROLE_OCC")
    expect(inventory, "/universe/role_unique_blob_counts",
           {"code": 15, "demo": 26, "result": 14, "test": 29}, "E_FACT_ROLE_BLOB")
    expect(attestation, "/coverage/unique_blobs_read_full", 84, "E_FACT_FULL_READ")
    expect(attestation, "/coverage/unread_lines", 0, "E_FACT_UNREAD")
    expect(attestation, "/coverage/parser_failures", 0, "E_FACT_PARSE")
    expect(attestation, "/coverage/truncation_unresolved", 0, "E_FACT_TRUNCATION")
    expect(flow, "/coverage/release_quantity_rows", 100, "E_FACT_FLOW")
    expect(flow, "/coverage/missing_release_quantity_pairs", 0, "E_FACT_FLOW_MISSING")
    expect(graph, "/coverage/edge_records", 219, "E_FACT_EDGES")
    expect(graph, "/coverage/coverage_records", 120, "E_FACT_GRAPH_COVERAGE")
    expect(graph, "/coverage/dynamic_edges", 80, "E_FACT_DYNAMIC_EDGES")
    expect(graph, "/authority/actual_runtime_order_proven", False, "E_FACT_RUNTIME_ORDER")
    expect(defaults, "/complete_python_search/searched_exact_names_status",
           "GROUND_NOT_FOUND", "E_FACT_LOADER_GNF")
    expect(defaults, "/owner_resolution/obligation_id", "P066-OBL-0125",
           "E_FACT_LOADER_OWNER")
    expect(defaults, "/owner_resolution/resolution_state", "BOUND_NOT_RESOLVED_OR_DISPATCHED",
           "E_FACT_LOADER_STATE")
    expect(saved_runtime, "/cross_runtime_behavior_equal", True, "E_FACT_DEFAULT_RUNTIME")
    expect(tests, "/universe",
           {"demo_blobs": 26, "demo_lines": 3300, "demo_occurrences": 30,
            "golden_blobs": 2, "golden_occurrences": 8, "guide_blobs": 8,
            "guide_lines": 854, "guide_occurrences": 20, "result_blobs": 14,
            "result_lines": 2081, "result_occurrences": 35, "test_blobs": 29,
            "test_lines": 6042, "test_occurrences": 44}, "E_FACT_TEST_UNIVERSE")
    outcomes: dict[str, int] = {}
    for row in value_at(tests, "/runtime_records", "E_FACT_RUNTIME_ROWS"):
        outcome = row.get("outcome")
        require(isinstance(outcome, str), "E_FACT_RUNTIME_OUTCOME")
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    require(outcomes == {"DEPENDENCY_MISSING": 34, "FAIL_EXIT_GATE": 5,
                         "MANUAL_OBSERVATION": 38, "PASS_EXIT_GATE": 33},
            "E_FACT_RUNTIME_COUNTS")
    expect(guide, "/guide_contract/guide_prose_is_self_report_until_exact_source_assertion_and_runtime_bound",
           True, "E_FACT_GUIDE_AUTHORITY")
    expect(units, "/coverage/executable_divide_3600_blob_count", 0, "E_FACT_3600")
    expect(units, "/authority/open_unit_convention",
           "Q_cell_Ah_OR_C_AND_NO_EXECUTABLE_DIVIDE_BY_3600", "E_FACT_UNIT_OPEN")
    expect(guards, "/coverage/guard_records", "24/24", "E_FACT_GUARDS")
    expect(guards, "/coverage/impact_probes", "27/27", "E_FACT_PROBES")
    expect(guards, "/open_gap_records/1/status", "OPEN", "E_FACT_CHRONOLOGY")
    expect(guards, "/open_gap_records/2/status", "OPEN", "E_FACT_CONVERGENCE")
    expect(guards, "/guard_records/20/behavior", "GROUND_NOT_FOUND_EXECUTABLE_GUARD",
           "E_FACT_TRANSFER")
    expect(fitting, "/exclusive_classification/counts",
           {"DEMO": 0, "REAL_DATA": 1, "RECONSTRUCTED": 6,
            "SAVED_ONLY": 5, "SYNTHETIC": 0}, "E_FACT_FIT_CLASSES")
    expect(fitting, "/missing_evidence/held_out_cells_rates_temperatures",
           "GROUND_NOT_FOUND", "E_FACT_HELDOUT")
    expect(fitting_runtime, "/execution_policy/fresh_historical_fit_execution_count", 0,
           "E_FACT_FIT_EXECUTION")
    expect(fitting_runtime, "/validation/historical_state_ground_not_found", 25,
           "E_FACT_OPTIMIZER_GNF")
    expect(source, "/source_contract/python_occurrences", 129, "E_FACT_SOURCE_DISPOSITION")
    expect(carry, "/gate_summary/active_obligations", 222, "E_FACT_ACTIVE")
    expect(carry, "/gate_summary/owner_registry_records", 358, "E_FACT_REGISTRY")
    expect(carry, "/gate_summary/ownerless_active_obligations", 0, "E_FACT_OWNERLESS")
    expect(carry, "/gate_summary/multiply_owned_active_obligations", 0, "E_FACT_MULTIPLE")
    expect(carry, "/gate_summary/lost_inherited_ids", 0, "E_FACT_LOST")
    expect(carry, "/gate_summary/external_authority_promotions", 0, "E_FACT_PROMOTION")
    expect(carry, "/gate_summary/disposition_counts",
           {"CORRECT": 2, "DISCARD": 0, "GROUND_NOT_FOUND": 33,
            "PRESERVE": 1016, "WITHHOLD": 117}, "E_FACT_DISPOSITIONS")
    expect(carry, "/gate_summary/source_dispositions", 157, "E_FACT_SOURCE_ROWS")
    expect(carry, "/gate_summary/blob_disposition_groups", 94, "E_FACT_BLOB_GROUPS")
    expect(carry, "/gate_summary/new_obligations", 3, "E_FACT_NEW_OBLIGATIONS")
    expect(carry, "/gate_summary/owner_transitions", 3, "E_FACT_OWNER_TRANSITIONS")
    runtime_dispositions = [
        row for row in value_at(carry, "/step82_89_disposition_records",
                                "E_FACT_DISPOSITION_ROWS")
        if row.get("origin_path") == MACHINE_PATHS[6] and
        isinstance(row.get("origin_pointer"), str) and
        row["origin_pointer"].startswith("/runtime_records/")
    ]
    require(len(runtime_dispositions) == 110 and
            {row.get("canonical_owner") for row in runtime_dispositions} == {
                "PHASE-088-SCIENTIFIC-REDTEAM",
            }, "E_FACT_RUNTIME_OWNER")
    numerical_limitations = [
        row for row in value_at(carry, "/step82_89_disposition_records",
                                "E_FACT_DISPOSITION_ROWS")
        if row.get("origin_path") == MACHINE_PATHS[8] and
        row.get("origin_pointer") == "/limitation_records/0"
    ]
    require(len(numerical_limitations) == 1 and
            numerical_limitations[0].get("canonical_owner") ==
            "PHASE-076-NONEQUILIBRIUM-KINETICS", "E_FACT_LIMITATION_OWNER")
    active_obligations = value_at(carry, "/active_obligations", "E_FACT_OBLIGATIONS")
    required_owners = {
        "P065-OBL-0054": "PHASE-080-BLEND-CLOSURE",
        "P065-OBL-0061": "PHASE-074-FOUNDATION",
        "P066-OBL-0086": "PHASE-072-DATA-PROVENANCE",
        "P066-OBL-0120": "PHASE-080-BLEND-CLOSURE",
        "P066-OBL-0125": "PHASE-083-IMPLEMENTATION-CONTRACT",
        "P067-OBL-0001": "PHASE-083-IMPLEMENTATION-CONTRACT",
        "P067-OBL-0002": "PHASE-083-IMPLEMENTATION-CONTRACT",
        "P067-OBL-0003": "PHASE-083-IMPLEMENTATION-CONTRACT",
    }
    observed_owners: dict[str, str] = {}
    optimizer_owners: dict[str, str] = {}
    for row in active_obligations:
        obligation_id = row.get("obligation_id")
        owner = row.get("canonical_owner")
        if obligation_id in required_owners:
            require(isinstance(owner, str) and obligation_id not in observed_owners,
                    "E_FACT_OBLIGATION_OWNER_UNIQUE", str(obligation_id))
            observed_owners[obligation_id] = owner
        if isinstance(obligation_id, str) and re.fullmatch(
                r"P066-OBL-(0089|009[0-9]|010[0-9]|011[0-3])", obligation_id):
            require(isinstance(owner, str) and obligation_id not in optimizer_owners,
                    "E_FACT_OPTIMIZER_OWNER_UNIQUE", obligation_id)
            optimizer_owners[obligation_id] = owner
    require(observed_owners == required_owners, "E_FACT_OBLIGATION_OWNERS")
    require(len(optimizer_owners) == 25 and
            set(optimizer_owners.values()) == {
                "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION",
            }, "E_FACT_OPTIMIZER_OWNERS")
    return {
        "python": {"occurrences": 129, "unique_blobs": 84,
                   "unique_blob_physical_lines": 29952, "releases": 20},
        "roles": {"code": [20, 15], "test": [44, 29],
                  "demo": [30, 26], "result_tool": [35, 14]},
        "golden": {"occurrences": 8, "unique_blobs": 2},
        "guide": {"occurrences": 20, "unique_blobs": 8, "physical_lines": 854},
        "test_runtime_outcomes": outcomes,
        "disposition": {"records": 1168, "families": 47,
                        "counts": value_at(carry, "/gate_summary/disposition_counts", "E_FACT")},
        "predecessor": {
            "phase": 66,
            "selected_gate": "CONDITIONAL_P066",
            "persistence_terminal": "PASS_P066_STEP81_2_PERSISTENCE",
            "validation_path": PHASE066_VALIDATION,
            "validation_raw_sha256": PHASE066_VALIDATION_RAW_SHA256,
            "validation_semantic_sha256": PHASE066_VALIDATION_SEMANTIC_SHA256,
            "main_scholarly_body_modified": False,
        },
        "carry": {"active_before": 219, "active_after": 222,
                  "registry_before": 355, "registry_after": 358,
                  "owner_transitions": 3, "new_obligations": 3,
                  "ownerless": 0, "multiply_owned": 0, "lost": 0,
                  "authority_promotions": 0},
    }


def build_conformance_rows(documents: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    na = "NOT_APPLICABLE"
    specs = (
        ("C01", "complete Python identity and full-read topology", MACHINE_PATHS[1], "/coverage",
         "SUPPORTED", na, na, na, "SUPPORTED", "PHASE-067-CODE-HISTORY", [], False,
         "SOURCE_IDENTITY_AND_COMPLETE_READ_ONLY"),
        ("C02", "voltage/current/capacity/composition/temperature static flow", MACHINE_PATHS[2], "/coverage",
         "SUPPORTED_BOUNDED", na, na, na, "SUPPORTED_BOUNDED", "PHASE-067-CODE-HISTORY", [], False,
         "STATIC_AST_AND_LEXICAL_ORDER_NOT_RUNTIME_ORDER"),
        ("C03", "charge/lag/kinetics/heat/observation call graph", MACHINE_PATHS[3],
         "/authority/actual_runtime_order_proven",
         "PARTIAL", "NOT_TESTED", na, na, "PARTIAL", "PHASE-083-IMPLEMENTATION-CONTRACT",
         [], True, "SOURCE_STATIC_GRAPH; 80 DYNAMIC EDGES AND RUNTIME ORDER UNPROVEN"),
        ("C04", "fresh defaults, mutable globals, import and reload behavior", MACHINE_PATHS[4],
         "/default_adjudication", "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED", na, na,
         "SUPPORTED_BOUNDED", "PHASE-067-CODE-HISTORY", [], False,
         "NAMED_SOURCE_AND_13 DUAL-RUNTIME ISOLATED CASES_ONLY"),
        ("C05", "saved profile loader and regular-solution metadata dispatch", MACHINE_PATHS[4],
         "/owner_resolution", "GROUND_NOT_FOUND", "NOT_TESTED", na, na,
         "GROUND_NOT_FOUND", "PHASE-083-IMPLEMENTATION-CONTRACT", ["P066-OBL-0125"], True,
         "DIRECT_CONSTRUCTOR_ACCEPTANCE_IS_NOT_SERIALIZED_DISPATCH"),
        ("C06", "test-path executable enforcement and cross-runtime outcomes", MACHINE_PATHS[6],
         "/runtime_records", na, "PARTIAL", "PARTIAL", na, "PARTIAL",
         "PHASE-088-SCIENTIFIC-REDTEAM", [], True,
         "33 PASS_EXIT_GATE; 5 FAIL_EXIT_GATE; 34 DEPENDENCY_MISSING; 38 MANUAL_OBSERVATION"),
        ("C07", "demo outputs", MACHINE_PATHS[6], "/enforcement_summary/demo", na,
         "WITHHELD_AS_AUTHORITY", na, na, "WITHHELD_AS_AUTHORITY",
         "PHASE-067-CODE-HISTORY", [], False, "PRINT_PLOT_OR_EXIT_IS_NOT_TEST_OR_SCIENCE"),
        ("C08", "golden archive structure and values", MACHINE_PATHS[6], "/golden_contract", na,
         "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED", na, "SUPPORTED_BOUNDED",
         "PHASE-067-CODE-HISTORY", [], False, "INTERNAL_REFERENCE_BYTES_NOT_EXTERNAL_TRUTH"),
        ("C09", "guide and result-tool claims", MACHINE_PATHS[7], "/guide_contract", na,
         "WITHHELD_AS_AUTHORITY", na, na, "WITHHELD_AS_AUTHORITY",
         "PHASE-067-CODE-HISTORY", [], False, "PROSE_AND_OUTPUT_REQUIRE_SOURCE_PLUS_RUNTIME"),
        ("C10", "rate/capacity/energy unit and basis closure", MACHINE_PATHS[8],
         "/coverage/executable_divide_3600_blob_count",
         "PARTIAL", "PARTIAL", na, "PARTIAL", "PARTIAL", "PHASE-074-FOUNDATION",
         ["P065-OBL-0061"], True, "Q_CELL_AH_OR_C; NO_EXECUTABLE_DIVIDE_BY_3600; ENERGY_ROUTE_GNF"),
        ("C11", "conditional zero-current numerical closure", MACHINE_PATHS[8],
         "/limitation_records/0", "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED", na, na,
         "SUPPORTED_BOUNDED", "PHASE-076-NONEQUILIBRIUM-KINETICS", [], False,
         "DECLARED_FIXTURE_ONLY_NOT_UNIVERSAL"),
        ("C12", "numerical guards and fixed-vector impact probes", MACHINE_PATHS[9], "/coverage",
         "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED", na, na, "SUPPORTED_BOUNDED",
         "PHASE-067-CODE-HISTORY", [], False, "INTERNAL_FIXED_VECTOR_AND_SOURCE_BOUNDARY_ONLY"),
        ("C13", "arbitrary nonmonotonic chronology", MACHINE_PATHS[9], "/open_gap_records/1",
         "PARTIAL", "NOT_TESTED", na, na, "PARTIAL", "PHASE-083-IMPLEMENTATION-CONTRACT",
         ["P067-OBL-0001"], True, "VOLTAGE_SORTING_IS_NOT_CHRONOLOGY"),
        ("C14", "root and optimizer exhaustion convergence state", MACHINE_PATHS[9],
         "/open_gap_records/2", "PARTIAL", "PARTIAL", na, na, "PARTIAL",
         "PHASE-083-IMPLEMENTATION-CONTRACT", ["P067-OBL-0002"], True,
         "RETURN_VALUE_ALONE_HAS_NO_CONVERGENCE_AUTHORITY"),
        ("C15", "transfer-helper grid and length preconditions", MACHINE_PATHS[9],
         "/guard_records/20", "GROUND_NOT_FOUND", "NOT_TESTED", na, na,
         "GROUND_NOT_FOUND", "PHASE-083-IMPLEMENTATION-CONTRACT", ["P067-OBL-0003"], True,
         "PROSE_ONLY; EXECUTABLE_GUARD_GROUND_NOT_FOUND"),
        ("C16", "fitting provenance classes and in-sample data route", MACHINE_PATHS[10],
         "/exclusive_classification", "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED",
         "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED",
         "PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS", [], False,
         "REAL_DATA_1_RECONSTRUCTED_6_SAVED_ONLY_5; IN_SAMPLE_ONLY"),
        ("C17", "historical fitting execution reuse", MACHINE_PATHS[11], "/execution_policy",
         na, "SUPPORTED_BOUNDED", "SUPPORTED_BOUNDED", na, "SUPPORTED_BOUNDED",
         "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION", [], False,
         "SEALED_PHASE066_REUSE; ZERO FRESH HISTORICAL FITS"),
        ("C18", "original optimizer state", MACHINE_PATHS[11],
         "/original_optimizer_state_availability", na, "GROUND_NOT_FOUND", na, na,
         "GROUND_NOT_FOUND", "PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION",
         [f"P066-OBL-{number:04d}" for number in range(89, 114)], False,
         "25 HISTORICAL FIELDS GROUND_NOT_FOUND; KNOWN EXTERNAL HISTORY DEBT"),
        ("C19", "specimen/protocol cryptographic binding", MACHINE_PATHS[10], "/missing_evidence",
         na, na, "PARTIAL", "GROUND_NOT_FOUND", "GROUND_NOT_FOUND",
         "PHASE-072-DATA-PROVENANCE", ["P066-OBL-0086"], False,
         "SOURCE_DECLARED_DATASET; EXACT SPECIMEN_AND_PARQUET_BINDING_GNF"),
        ("C20", "finite-rate blend host partition and nonadditivity", MACHINE_PATHS[10],
         "/finite_rate_boundary", "PARTIAL", na, "NOT_TESTED", "GROUND_NOT_FOUND",
         "GROUND_NOT_FOUND", "PHASE-080-BLEND-CLOSURE",
         ["P065-OBL-0054", "P066-OBL-0120"], False,
         "IN_SAMPLE_WHOLE_CURVE_FIT_IS_NOT_FINITE_RATE_HOST_PROOF"),
        ("C21", "held-out/material/phase/mechanism evidence", MACHINE_PATHS[13],
         "/authority_boundary/named_debts_preserved", na, na, "GROUND_NOT_FOUND",
         "GROUND_NOT_FOUND", "GROUND_NOT_FOUND", "EXISTING_DOWNSTREAM_OWNERS", [], False,
         "KNOWN_EXTERNAL_DEBT_EXCLUDED_FROM_PHASE067_GATE_DETERMINANT"),
        ("C22", "lossless source and finding disposition", MACHINE_PATHS[13], "/gate_summary",
         "AUDIT_COMPLETE", "AUDIT_COMPLETE", "AUDIT_COMPLETE", "AUDIT_COMPLETE",
         "AUDIT_COMPLETE", "PHASE-067-CODE-HISTORY", [], False,
         "PRESERVE_IS_ROUTING_NOT_CONFORMANCE_OR_AUTHORITY"),
    )
    supporting_specs = {
        "C03": ((MACHINE_PATHS[3], "/coverage/dynamic_edges"),),
        "C10": (
            (MACHINE_PATHS[8], "/authority/open_unit_convention"),
            (MACHINE_PATHS[8],
             "/probe_records/6/inputs/production_energy_integration_route"),
        ),
    }
    acceptance = {
        "C03": "DIRECT_RUNTIME_CALL_ORDER_AND_DYNAMIC_DISPATCH_EVIDENCE_FOR_NAMED_PHYSICS_ROUTES",
        "C05": "SERIALIZED_PROFILE_LOADER_AND_REGULAR_SOLUTION_KERNEL_DISPATCH_CONTRACT_WITH_EXECUTABLE_CROSS_RUNTIME_TEST",
        "C06": "REQUIRED_PHASE067_TEST_AND_DEMO_RUNTIME_CELLS_EXECUTE_UNDER_BOTH_RUNTIMES_OR_REMAIN_EXPLICITLY_WITHHELD_WITH_OWNER",
        "C10": "EXPLICIT_Q_CELL_UNIT_BASIS_EXECUTABLE_CONVERSION_AND_ENERGY_INTEGRATION_ROUTE",
        "C13": "CHRONOLOGY_PRESERVING_ROUTE_FOR_ARBITRARY_NONMONOTONIC_INPUT_WITH_EXECUTABLE_TEST",
        "C14": "EXPLICIT_ROOT_AND_OPTIMIZER_EXHAUSTION_STATE_PROPAGATION_WITH_EXECUTABLE_TEST",
        "C15": "EXECUTABLE_TRANSFER_GRID_AND_LENGTH_PRECONDITION_GUARDS_WITH_NEGATIVE_TESTS",
    }
    incomplete = frozenset({"PARTIAL", "NOT_TESTED", "GROUND_NOT_FOUND"})
    rows: list[dict[str, Any]] = []
    for (row_id, topic, origin_path, pointer, theory_code, code_test, test_data,
         theory_data, status, owner, obligation_ids, determinant, ceiling) in specs:
        origin = value_at(documents[origin_path], pointer, "E_ROW_" + row_id)
        axes = {
            "theory_code": theory_code,
            "code_test": code_test,
            "test_data": test_data,
            "theory_data": theory_data,
        }
        supporting_origins: list[dict[str, Any]] = []
        for supporting_path, supporting_pointer in supporting_specs.get(row_id, ()):
            supporting_record = value_at(
                documents[supporting_path], supporting_pointer, "E_ROW_SUPPORT_" + row_id,
            )
            supporting_origins.append({
                "path": supporting_path,
                "pointer": supporting_pointer,
                "record_sha256": record_sha(supporting_record),
            })
        rows.append({
            "row_id": row_id,
            "topic": topic,
            "axes": axes,
            "status": status,
            "owner": owner,
            "obligation_ids": obligation_ids,
            "phase067_gate_determinant": determinant,
            "required_internal_axes": [key for key, value in axes.items()
                                       if determinant and value in incomplete],
            "acceptance_criterion": acceptance.get(
                row_id, "NO_PHASE067_CLOSURE_ACTION_REQUIRED_WITHIN_RECORDED_AUTHORITY_CEILING"),
            "not_applicable_axis_reasons": {
                key: "OUTSIDE_THE_RECORDED_EVIDENCE_CLAIM_FOR_THIS_ROW"
                for key, value in axes.items() if value == na
            },
            "external_authority_promoted": False,
            "authority_ceiling": ceiling,
            "origin": {
                "path": origin_path,
                "pointer": pointer,
                "record_sha256": record_sha(origin),
            },
            "supporting_origins": supporting_origins,
        })
    require(len(rows) == 22 and len({row["row_id"] for row in rows}) == 22,
            "E_ROW_COUNT")
    return rows


INCOMPLETE_STATUSES = frozenset({"PARTIAL", "NOT_TESTED", "GROUND_NOT_FOUND"})


def select_gate(rows: list[dict[str, Any]], hard_failures: list[str]) -> str:
    if hard_failures:
        return "FAIL_P067"
    determinant_incomplete = [
        row for row in rows if row["phase067_gate_determinant"] and
        (row["status"] in INCOMPLETE_STATUSES or
         any(value in INCOMPLETE_STATUSES for value in row["axes"].values()))
    ]
    return "CONDITIONAL_P067" if determinant_incomplete else "PASS_P067_CODE_HISTORY"


def gate_evaluation(rows: list[dict[str, Any]]) -> dict[str, Any]:
    determinants = [row["row_id"] for row in rows if row["phase067_gate_determinant"]]
    incomplete = [row["row_id"] for row in rows
                  if row["phase067_gate_determinant"] and
                  (row["status"] in INCOMPLETE_STATUSES or
                   any(value in INCOMPLETE_STATUSES for value in row["axes"].values()))]
    selected = select_gate(rows, [])
    require(selected == GATE, "E_GATE_SELECTION")
    require(determinants == ["C03", "C05", "C06", "C10", "C13", "C14", "C15"],
            "E_GATE_DETERMINANTS")
    require(incomplete == determinants, "E_GATE_INCOMPLETE")
    return {
        "selected_gate": selected,
        "exclusive_gate_enum": ["PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067"],
        "audit_hard_failures": [],
        "determinant_row_ids": determinants,
        "incomplete_determinant_row_ids": incomplete,
        "pass_eligible": False,
        "conditional_eligible": True,
        "fail_eligible": False,
        "pass_rejection": "SEVEN_REQUIRED_INTERNAL_CELLS_ARE_PARTIAL_NOT_TESTED_OR_GROUND_NOT_FOUND",
        "fail_rejection": "IDENTITY_READ_DISPOSITION_OWNER_AND_GIT_AUDIT_ARE_COMPLETE",
        "external_known_debt_is_determinant": False,
        "current_step_persistence_is_content_prerequisite": False,
    }


def gate_controls(rows: list[dict[str, Any]]) -> int:
    require(select_gate(rows, ["identity failure"]) == "FAIL_P067", "E_GATE_CONTROL_FAIL")
    closed = copy.deepcopy(rows)
    for row in closed:
        if row["phase067_gate_determinant"]:
            row["status"] = "SUPPORTED"
            row["axes"] = {key: ("SUPPORTED" if value != "NOT_APPLICABLE" else value)
                           for key, value in row["axes"].items()}
    require(select_gate(closed, []) == "PASS_P067_CODE_HISTORY", "E_GATE_CONTROL_PASS")
    require(select_gate(rows, []) == "CONDITIONAL_P067", "E_GATE_CONTROL_CONDITIONAL")
    return 3


def read_human(path: str) -> tuple[bytes, str]:
    raw = (ROOT / path).read_bytes()
    require(0 < len(raw) <= 2_000_000, "E_HUMAN_BYTES", path)
    normalized = lf_bytes(raw, "E_HUMAN_" + path)
    return raw, normalized.decode("utf-8")


def unique_prefixed_line(text: str, prefix: str, label: str) -> str:
    matches = [line for line in text.splitlines() if line.startswith(prefix)]
    require(len(matches) == 1, label, prefix)
    return matches[0]


def validate_human_documents(
        rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    common = ("Phase 067", "Step 90.2", EXPECTED_PARENT, SUBJECT, GATE,
              PRECOMMIT_STATUS, PERSISTENCE)
    specific = {
        REPORT: ("Theory–Code–Test–Data Conformance", "theory–code", "code–test",
                 "test–data", "theory–data", "22", "C03", "C15"),
        GATE_RESULT: ("PASS_P067_CODE_HISTORY", "CONDITIONAL_P067", "FAIL_P067",
                      "seven", "P0/P1/P2"),
        RESULT: ("Steps 82–90.1", "canonical-evidence reuse", "599,369",
                 "ownerless", "Step 82", "Step 90.1"),
        PARENT_LEDGER: ("Steps 82–90.1 persisted", "Step 90.2 current"),
        ACTIVE_LEDGER: ("| Phase 067 Step 90.2 |", "Steps 82–90.1 persisted"),
        HANDOVER: ("| Phase 067 Step 90.2 |", "Steps 82–90.1 persisted"),
    }
    identities: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    for path in (REPORT, GATE_RESULT, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER):
        raw, text = read_human(path)
        texts[path] = text
        for token in common + specific[path]:
            require(token in text, "E_HUMAN_TOKEN", path + ":" + token)
        identities.append(text_identity(path, raw))
    validator_raw = (ROOT / VALIDATOR).read_bytes()
    identities.insert(0, text_identity(VALIDATOR, validator_raw))
    for stale in (
            "Step 90.1 is current at `PASS_PENDING_PERSISTENCE`; Step 90.2 is blocked.",
            "Step 90.1 is current at `PASS_P067_STEP90_1_DISPOSITION` / `PASS_PENDING_PERSISTENCE`",
    ):
        require(stale not in texts[HANDOVER], "E_HANDOVER_STALE_STATE", stale)

    report_header = unique_prefixed_line(texts[REPORT], "| ID | Topic |", "E_REPORT_HEADER")
    require(report_header ==
            "| ID | Topic | theory–code | code–test | test–data | theory–data | Overall | Determinant | Owner |",
            "E_REPORT_HEADER_EXACT")
    for row in rows:
        line = unique_prefixed_line(texts[REPORT], "| " + row["row_id"] + " |",
                                    "E_REPORT_ROW")
        fields = [field.strip() for field in line.split("|")[1:-1]]
        require(len(fields) == 9, "E_REPORT_ROW_FIELDS", row["row_id"])
        expected_fields = [
            row["row_id"], row["topic"], row["axes"]["theory_code"],
            row["axes"]["code_test"], row["axes"]["test_data"],
            row["axes"]["theory_data"], row["status"],
            "YES" if row["phase067_gate_determinant"] else "NO", row["owner"],
        ]
        require(fields == expected_fields, "E_REPORT_ROW_EXACT", row["row_id"])

    for path in (GATE_RESULT, RESULT):
        selected = unique_prefixed_line(texts[path], "- Selected Gate: ", "E_SELECTED_GATE_LINE")
        require(selected == "- Selected Gate: `CONDITIONAL_P067`", "E_SELECTED_GATE_EXACT", path)

    parent_row = unique_prefixed_line(texts[PARENT_LEDGER], "| 067 |", "E_PARENT_PHASE_ROW")
    require("Steps 82–90.1 persisted; Step 90.2 current" in parent_row and
            "CONDITIONAL_PENDING_PERSISTENCE" in parent_row, "E_PARENT_PHASE_STATE")
    active_phase_row = unique_prefixed_line(texts[ACTIVE_LEDGER], "| 067 |", "E_ACTIVE_PHASE_ROW")
    require("Steps 82–90.1 persisted; Step 90.2 current" in active_phase_row and
            "CONDITIONAL_PENDING_PERSISTENCE" in active_phase_row, "E_ACTIVE_PHASE_STATE")
    active_step = unique_prefixed_line(texts[ACTIVE_LEDGER], "| Phase 067 Step 90.2 |",
                                       "E_ACTIVE_STEP_ROW")
    handover_step = unique_prefixed_line(texts[HANDOVER], "| Phase 067 Step 90.2 |",
                                         "E_HANDOVER_STEP_ROW")
    for label, line in (("active", active_step), ("handover", handover_step)):
        for token in (EXPECTED_PARENT, SUBJECT, GATE, PRECOMMIT_STATUS, PERSISTENCE):
            require(token in line, "E_STEP_ROW_TOKEN", label + ":" + token)

    result_lines = texts[RESULT].splitlines()
    result_history_lines: dict[str, tuple[int, str]] = {}
    for spec in UNIT_SPECS:
        prefix = "| " + spec["step"] + " |"
        matches = [(index + 1, line) for index, line in enumerate(result_lines)
                   if line.startswith(prefix)]
        require(len(matches) == 1, "E_HISTORY_LINE", spec["step"])
        line_number, line = matches[0]
        for token in (spec["commit"], spec["parent"], spec["subject"],
                       spec["gate"], spec["terminal"], "Python 3.12 + Python 3.14"):
            require(token in line, "E_HISTORY_TOKEN", spec["step"] + ":" + token)
        result_history_lines[spec["step"]] = (line_number, line)

    committed_ledger_raw = git_blob(EXPECTED_PARENT, ACTIVE_LEDGER)
    committed_ledger_text = lf_bytes(
        committed_ledger_raw, "E_COMMITTED_HISTORY_LEDGER",
    ).decode("utf-8")
    committed_ledger_lines = committed_ledger_text.splitlines()
    history: list[dict[str, Any]] = []
    for spec in UNIT_SPECS[:-1]:
        prefix = "| Phase 067 Step " + spec["step"] + " |"
        matches = [(index + 1, line) for index, line in enumerate(committed_ledger_lines)
                   if line.startswith(prefix)]
        require(len(matches) == 1, "E_COMMITTED_HISTORY_LINE", spec["step"])
        line_number, line = matches[0]
        for token in (spec["commit"], spec["subject"], spec["gate"], spec["terminal"],
                      "pushed", "live"):
            require(token in line, "E_COMMITTED_HISTORY_TOKEN", spec["step"] + ":" + token)
        history.append({
            "step": spec["step"],
            "commit": spec["commit"],
            "content_gate": spec["gate"],
            "recorded_persistence_terminal": spec["terminal"],
            "runtime_labels": ["Python 3.12", "Python 3.14"],
            "evidence_kind": "COMMITTED_POST_STEP_LEDGER_RECORD_NOT_RAW_STDOUT_TRANSCRIPT",
            "prior_runtime_stdout_transcript_persisted": False,
            "provenance": {
                "path": ACTIVE_LEDGER,
                "commit": EXPECTED_PARENT,
                "line": line_number,
                "line_sha256": sha256((line + "\n").encode("utf-8")),
            },
        })
    final_spec = UNIT_SPECS[-1]
    line_number, line = result_history_lines[final_spec["step"]]
    history.append({
        "step": final_spec["step"],
        "commit": final_spec["commit"],
        "content_gate": final_spec["gate"],
        "recorded_persistence_terminal": final_spec["terminal"],
        "runtime_labels": ["Python 3.12", "Python 3.14"],
        "evidence_kind": "CURRENT_RECOVERY_ASSERTION_PLUS_CURRENT_FINAL_DUAL_RUNTIME_GIT_AND_ARTIFACT_REVALIDATION",
        "prior_runtime_stdout_transcript_persisted": False,
        "provenance": {
            "path": RESULT,
            "commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "line": line_number,
            "line_sha256": sha256((line + "\n").encode("utf-8")),
        },
    })
    return identities, history


def authority_boundary() -> dict[str, Any]:
    return {
        "canonical_model": False,
        "canonical_release": False,
        "external_scientific": False,
        "held_out_validation": False,
        "historical_optimizer_state": False,
        "identifiability": False,
        "material_assignment": False,
        "phase_or_mechanism_identification": False,
        "primary_proposition": False,
        "protocol_binding": False,
        "publication_readiness": False,
        "ref7_original_full_text": "GROUND_NOT_FOUND",
        "scholarly_main_body_code_mention": False,
        "stale_pdf_release_authority": False,
        "known_external_debt_is_gate_determinant": False,
        "named_debt_owners_preserved": {
            "ref7": ["P065-OBL-0059"],
            "specimen_protocol": ["P066-OBL-0086"],
            "held_out": ["P066-OBL-0087"],
            "original_optimizer": [f"P066-OBL-{number:04d}" for number in range(89, 114)],
            "competing_external_synthesis": ["P066-OBL-0115"],
            "material_phase_species": [f"P066-OBL-{number:04d}" for number in range(116, 120)],
            "stale_pdf": ["P066-OBL-0007", "P066-OBL-0029", "P066-OBL-0030",
                          "P066-OBL-0033", "P066-OBL-0037", "P066-OBL-0038",
                          "P066-OBL-0060", "P066-OBL-0084", "P066-OBL-0085"],
        },
    }


def build_document() -> tuple[dict[str, Any], dict[str, int]]:
    units = validate_units()
    documents, inputs, nodes, depth = load_machine_inputs()
    summary = validate_machine_facts(documents)
    rows = build_conformance_rows(documents)
    gate = gate_evaluation(rows)
    human, history = validate_human_documents(rows)
    document: dict[str, Any] = {
        "schema_version": "phase067-final-conformance-v1",
        "artifact": ARTIFACT,
        "phase": 67,
        "step": "90.2",
        "generated_date": "2026-09-07",
        "branch": BRANCH,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": SUBJECT,
        "content_gate": GATE,
        "precommit_status": PRECOMMIT_STATUS,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "persistence_terminal": PERSISTENCE,
        "result_first": True,
        "json_output_last": True,
        "canonical_evidence_reuse": {
            "historical_validator_reexecution_count": 0,
            "historical_fit_reexecution_count": 0,
            "persisted_steps": [spec["step"] for spec in UNIT_SPECS],
            "prior_runtime_stdout_transcripts_persisted": False,
            "step90_1_terminal_evidence_ceiling":
                "CURRENT_RECOVERY_ASSERTION_PLUS_CURRENT_FINAL_DUAL_RUNTIME_GIT_AND_ARTIFACT_REVALIDATION",
            "policy": "VERIFY_COMMITTED_BYTES_SEMANTIC_SEALS_GIT_IDENTITY_AND_RECORDED_TERMINAL_LABELS_WITH_TRANSCRIPT_LIMITATION",
        },
        "transaction": {
            "paths": list(FINAL_PATHS),
            "status": [FINAL_STATUS[path] for path in FINAL_PATHS],
            "modes": ["100644"] * len(FINAL_PATHS),
            "nonartifact_text_identities": human,
        },
        "persisted_unit_records": units,
        "persistence_history_records": history,
        "machine_input_records": inputs,
        "coverage_summary": summary,
        "conformance_rows": rows,
        "gate_evaluation": gate,
        "authority_boundary": authority_boundary(),
        "validation": {
            "persisted_units": len(units),
            "machine_inputs": len(inputs),
            "machine_input_nodes": nodes,
            "maximum_input_depth": depth,
            "conformance_rows": len(rows),
            "conditional_determinants": len(gate["determinant_row_ids"]),
            "source_policy_negative_controls": 107,
            "git_argv_controls": 18,
            "repository_singleton_controls": 5,
            "strict_json_controls": 7,
            "semantic_controls": 47,
            "gate_controls": 3,
            "deterministic_reconstructions": 2,
        },
    }
    document["semantic_sha256"] = semantic_sha(document, "compact")
    return document, {"nodes": nodes, "depth": depth}


def nested_value(document: Any, keys: tuple[Any, ...]) -> tuple[bool, Any]:
    current = document
    for key in keys:
        if isinstance(current, dict) and isinstance(key, str) and key in current:
            current = current[key]
        elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
            current = current[key]
        else:
            return False, None
    return True, current


def singleton_diagnostics(candidate: dict[str, Any], expected: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    checks = (
        (("expected_parent",), "E_SINGLETON_WRONG_PARENT"),
        (("expected_subject",), "E_SINGLETON_WRONG_SUBJECT"),
        (("content_gate",), "E_SINGLETON_WRONG_GATE"),
        (("precommit_status",), "E_SINGLETON_PRECOMMIT_STATUS"),
        (("containing_commit",), "E_SINGLETON_CONTAINING_COMMIT"),
        (("persistence_terminal",), "E_SINGLETON_WRONG_TERMINAL"),
        (("result_first",), "E_SINGLETON_RESULT_FIRST"),
        (("json_output_last",), "E_SINGLETON_JSON_LAST"),
        (("coverage_summary", "python", "occurrences"), "E_SINGLETON_COUNT"),
        (("coverage_summary", "roles"), "E_SINGLETON_ROLE"),
        (("machine_input_records", 0, "blob_oid"), "E_SINGLETON_BLOB"),
        (("coverage_summary", "python", "unique_blob_physical_lines"), "E_SINGLETON_LINE"),
        (("coverage_summary", "python", "releases"), "E_SINGLETON_RELEASE"),
        (("canonical_evidence_reuse", "historical_validator_reexecution_count"),
         "E_SINGLETON_REPLAY_INFLATION"),
        (("coverage_summary", "carry", "multiply_owned"), "E_SINGLETON_OWNER_DUPLICATE"),
        (("authority_boundary", "ref7_original_full_text"), "E_SINGLETON_REF7_PROMOTION"),
        (("authority_boundary", "historical_optimizer_state"),
         "E_SINGLETON_OPTIMIZER_PROMOTION"),
        (("authority_boundary", "held_out_validation"), "E_SINGLETON_HELDOUT_PROMOTION"),
        (("authority_boundary", "external_scientific"), "E_SINGLETON_EXTERNAL_PROMOTION"),
        (("authority_boundary", "material_assignment"), "E_SINGLETON_MATERIAL_PROMOTION"),
        (("authority_boundary", "scholarly_main_body_code_mention"),
         "E_SINGLETON_SCHOLARLY_CODE_MENTION"),
        (("authority_boundary", "stale_pdf_release_authority"),
         "E_SINGLETON_STALE_PDF_PROMOTION"),
        (("coverage_summary", "predecessor", "selected_gate"),
         "E_SINGLETON_P066_GATE_PROMOTION"),
    )
    for keys, code in checks:
        candidate_found, candidate_value = nested_value(candidate, keys)
        expected_found, expected_value = nested_value(expected, keys)
        if candidate_found != expected_found or not typed_equal(candidate_value, expected_value):
            errors.add(code)

    candidate_units = candidate.get("persisted_unit_records")
    expected_units = expected.get("persisted_unit_records")
    if not isinstance(candidate_units, list) or not isinstance(expected_units, list) or \
            [row.get("step") for row in candidate_units if isinstance(row, dict)] != \
            [row.get("step") for row in expected_units if isinstance(row, dict)]:
        errors.add("E_SINGLETON_MISSING_STEP")
    candidate_history = candidate.get("persistence_history_records")
    expected_history = expected.get("persistence_history_records")
    if not isinstance(candidate_history, list) or not isinstance(expected_history, list) or \
            [row.get("step") for row in candidate_history if isinstance(row, dict)] != \
            [row.get("step") for row in expected_history if isinstance(row, dict)]:
        errors.add("E_SINGLETON_HISTORY_INFLATION")

    candidate_rows = candidate.get("conformance_rows")
    expected_rows = expected.get("conformance_rows")
    candidate_by_id = {row.get("row_id"): row for row in candidate_rows
                       if isinstance(row, dict)} if isinstance(candidate_rows, list) else {}
    expected_by_id = {row.get("row_id"): row for row in expected_rows
                      if isinstance(row, dict)} if isinstance(expected_rows, list) else {}
    if set(candidate_by_id) != set(expected_by_id) or any(
            candidate_by_id[row_id].get("owner") != expected_by_id[row_id].get("owner")
            for row_id in set(candidate_by_id) & set(expected_by_id)):
        errors.add("E_SINGLETON_OWNER_LOSS")
    authority_rows = (
        ("C01", "E_SINGLETON_SOURCE_AUTHORITY"),
        ("C06", "E_SINGLETON_TEST_AUTHORITY"),
        ("C07", "E_SINGLETON_DEMO_AUTHORITY"),
        ("C09", "E_SINGLETON_GUIDE_AUTHORITY"),
    )
    for row_id, code in authority_rows:
        if row_id not in candidate_by_id or row_id not in expected_by_id or \
                not typed_equal(candidate_by_id[row_id], expected_by_id[row_id]):
            errors.add(code)

    candidate_transaction = candidate.get("transaction")
    expected_transaction = expected.get("transaction")
    candidate_paths = candidate_transaction.get("paths") \
        if isinstance(candidate_transaction, dict) else None
    expected_paths = expected_transaction.get("paths") \
        if isinstance(expected_transaction, dict) else None
    if not isinstance(candidate_paths, list) or not isinstance(expected_paths, list):
        errors.update({"E_SINGLETON_EXTRA_PATH", "E_SINGLETON_RENAME_PATH",
                       "E_SINGLETON_DELETE_PATH"})
    elif len(candidate_paths) > len(expected_paths):
        errors.add("E_SINGLETON_EXTRA_PATH")
    elif len(candidate_paths) < len(expected_paths):
        errors.add("E_SINGLETON_DELETE_PATH")
    elif candidate_paths != expected_paths:
        errors.add("E_SINGLETON_RENAME_PATH")
    candidate_modes = candidate_transaction.get("modes") \
        if isinstance(candidate_transaction, dict) else None
    expected_modes = expected_transaction.get("modes") \
        if isinstance(expected_transaction, dict) else None
    if not typed_equal(candidate_modes, expected_modes):
        errors.add("E_SINGLETON_WRONG_MODE")
    return errors


def document_diagnostics(candidate: dict[str, Any], expected: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    top_sections = (
        ("schema_version", "E_DOCUMENT_SCHEMA"),
        ("expected_parent", "E_DOCUMENT_PARENT"),
        ("expected_subject", "E_DOCUMENT_SUBJECT"),
        ("content_gate", "E_DOCUMENT_GATE"),
        ("transaction", "E_DOCUMENT_TRANSACTION"),
        ("persisted_unit_records", "E_DOCUMENT_UNITS"),
        ("canonical_evidence_reuse", "E_DOCUMENT_REUSE"),
        ("persistence_history_records", "E_DOCUMENT_HISTORY"),
        ("machine_input_records", "E_DOCUMENT_INPUTS"),
        ("coverage_summary", "E_DOCUMENT_COVERAGE"),
        ("conformance_rows", "E_DOCUMENT_CONFORMANCE"),
        ("gate_evaluation", "E_DOCUMENT_EVALUATION"),
        ("authority_boundary", "E_DOCUMENT_AUTHORITY"),
    )
    if set(candidate) != set(expected):
        errors.add("E_DOCUMENT_KEYS")
    for key, code in top_sections:
        if key not in candidate or not typed_equal(candidate[key], expected[key]):
            errors.add(code)
    errors.update(singleton_diagnostics(candidate, expected))
    if not typed_equal(candidate, expected):
        errors.add("E_DOCUMENT_EXACT")
    return errors


def semantic_controls(expected: dict[str, Any]) -> int:
    cases = (
        ("schema_version", "wrong", "E_DOCUMENT_SCHEMA"),
        ("expected_parent", "0" * 40, "E_DOCUMENT_PARENT"),
        ("expected_subject", "wrong", "E_DOCUMENT_SUBJECT"),
        ("content_gate", "PASS_P067_CODE_HISTORY", "E_DOCUMENT_GATE"),
        ("transaction", {}, "E_DOCUMENT_TRANSACTION"),
        ("persisted_unit_records", [], "E_DOCUMENT_UNITS"),
        ("canonical_evidence_reuse", {}, "E_DOCUMENT_REUSE"),
        ("persistence_history_records", [], "E_DOCUMENT_HISTORY"),
        ("machine_input_records", [], "E_DOCUMENT_INPUTS"),
        ("coverage_summary", {}, "E_DOCUMENT_COVERAGE"),
        ("conformance_rows", [], "E_DOCUMENT_CONFORMANCE"),
        ("gate_evaluation", {}, "E_DOCUMENT_EVALUATION"),
        ("authority_boundary", {}, "E_DOCUMENT_AUTHORITY"),
    )
    for key, value, code in cases:
        candidate = copy.deepcopy(expected)
        candidate[key] = value
        candidate["semantic_sha256"] = semantic_sha(candidate, "compact")
        require(code in document_diagnostics(candidate, expected), "E_SEMANTIC_CONTROL", key)
    detailed_cases = (
        ("wrong_parent", "E_SINGLETON_WRONG_PARENT"),
        ("wrong_subject", "E_SINGLETON_WRONG_SUBJECT"),
        ("wrong_gate", "E_SINGLETON_WRONG_GATE"),
        ("wrong_terminal", "E_SINGLETON_WRONG_TERMINAL"),
        ("wrong_precommit", "E_SINGLETON_PRECOMMIT_STATUS"),
        ("wrong_containing", "E_SINGLETON_CONTAINING_COMMIT"),
        ("result_first", "E_SINGLETON_RESULT_FIRST"),
        ("json_last", "E_SINGLETON_JSON_LAST"),
        ("p066_gate", "E_SINGLETON_P066_GATE_PROMOTION"),
        ("scholarly_code", "E_SINGLETON_SCHOLARLY_CODE_MENTION"),
        ("count", "E_SINGLETON_COUNT"),
        ("role", "E_SINGLETON_ROLE"),
        ("blob", "E_SINGLETON_BLOB"),
        ("line", "E_SINGLETON_LINE"),
        ("release", "E_SINGLETON_RELEASE"),
        ("missing_step", "E_SINGLETON_MISSING_STEP"),
        ("replay", "E_SINGLETON_REPLAY_INFLATION"),
        ("history", "E_SINGLETON_HISTORY_INFLATION"),
        ("owner_loss", "E_SINGLETON_OWNER_LOSS"),
        ("owner_duplicate", "E_SINGLETON_OWNER_DUPLICATE"),
        ("ref7", "E_SINGLETON_REF7_PROMOTION"),
        ("optimizer", "E_SINGLETON_OPTIMIZER_PROMOTION"),
        ("heldout", "E_SINGLETON_HELDOUT_PROMOTION"),
        ("external", "E_SINGLETON_EXTERNAL_PROMOTION"),
        ("material", "E_SINGLETON_MATERIAL_PROMOTION"),
        ("stale_pdf", "E_SINGLETON_STALE_PDF_PROMOTION"),
        ("source_authority", "E_SINGLETON_SOURCE_AUTHORITY"),
        ("test_authority", "E_SINGLETON_TEST_AUTHORITY"),
        ("demo_authority", "E_SINGLETON_DEMO_AUTHORITY"),
        ("guide_authority", "E_SINGLETON_GUIDE_AUTHORITY"),
        ("extra_path", "E_SINGLETON_EXTRA_PATH"),
        ("rename_path", "E_SINGLETON_RENAME_PATH"),
        ("delete_path", "E_SINGLETON_DELETE_PATH"),
        ("wrong_mode", "E_SINGLETON_WRONG_MODE"),
    )
    for name, code in detailed_cases:
        candidate = copy.deepcopy(expected)
        if name == "wrong_parent":
            candidate["expected_parent"] = "0" * 40
        elif name == "wrong_subject":
            candidate["expected_subject"] = "wrong"
        elif name == "wrong_gate":
            candidate["content_gate"] = "PASS_P067_CODE_HISTORY"
        elif name == "wrong_terminal":
            candidate["persistence_terminal"] = "WRONG_TERMINAL"
        elif name == "wrong_precommit":
            candidate["precommit_status"] = "WRONG_PRECOMMIT"
        elif name == "wrong_containing":
            candidate["containing_commit"] = "0" * 40
        elif name == "result_first":
            candidate["result_first"] = False
        elif name == "json_last":
            candidate["json_output_last"] = False
        elif name == "p066_gate":
            candidate["coverage_summary"]["predecessor"]["selected_gate"] = \
                "PASS_P066_LINEAGE_I"
        elif name == "scholarly_code":
            candidate["authority_boundary"]["scholarly_main_body_code_mention"] = True
        elif name == "count":
            candidate["coverage_summary"]["python"]["occurrences"] += 1
        elif name == "role":
            candidate["coverage_summary"]["roles"]["code"][0] += 1
        elif name == "blob":
            candidate["machine_input_records"][0]["blob_oid"] = "0" * 40
        elif name == "line":
            candidate["coverage_summary"]["python"]["unique_blob_physical_lines"] += 1
        elif name == "release":
            candidate["coverage_summary"]["python"]["releases"] += 1
        elif name == "missing_step":
            candidate["persisted_unit_records"].pop()
        elif name == "replay":
            candidate["canonical_evidence_reuse"]["historical_validator_reexecution_count"] = 1
        elif name == "history":
            candidate["persistence_history_records"].append(
                copy.deepcopy(candidate["persistence_history_records"][-1]))
        elif name == "owner_loss":
            candidate["conformance_rows"][0]["owner"] = ""
        elif name == "owner_duplicate":
            candidate["coverage_summary"]["carry"]["multiply_owned"] = 1
        elif name == "ref7":
            candidate["authority_boundary"]["ref7_original_full_text"] = "PRESENT"
        elif name == "optimizer":
            candidate["authority_boundary"]["historical_optimizer_state"] = True
        elif name == "heldout":
            candidate["authority_boundary"]["held_out_validation"] = True
        elif name == "external":
            candidate["authority_boundary"]["external_scientific"] = True
        elif name == "material":
            candidate["authority_boundary"]["material_assignment"] = True
        elif name == "stale_pdf":
            candidate["authority_boundary"]["stale_pdf_release_authority"] = True
        elif name == "source_authority":
            candidate["conformance_rows"][0]["status"] = "WITHHELD_AS_AUTHORITY"
        elif name == "test_authority":
            candidate["conformance_rows"][5]["axes"]["code_test"] = "SUPPORTED"
        elif name == "demo_authority":
            candidate["conformance_rows"][6]["status"] = "SUPPORTED"
        elif name == "guide_authority":
            candidate["conformance_rows"][8]["status"] = "SUPPORTED"
        elif name == "extra_path":
            candidate["transaction"]["paths"].append("Codex/results/UNDECLARED")
        elif name == "rename_path":
            candidate["transaction"]["paths"][0] = "Codex/results/RENAMED"
        elif name == "delete_path":
            candidate["transaction"]["paths"].pop()
        else:
            require(name == "wrong_mode", "E_DETAILED_CONTROL_NAME", name)
            candidate["transaction"]["modes"][0] = "100755"
        candidate["semantic_sha256"] = semantic_sha(candidate, "compact")
        require(code in document_diagnostics(candidate, expected),
                "E_DETAILED_SEMANTIC_CONTROL", name)
    return len(cases) + len(detailed_cases)


def json_controls() -> int:
    fixtures = (
        b'{"a":1,"a":2}\n',
        b'{"a":NaN}\n',
        b'\xef\xbb\xbf{"a":1}\n',
        b'{"a":1}\r\n',
        b'{"a":1}',
        (b'{"a":' + b'[' * 65 + b'0' + b']' * 65 + b'}\n'),
        b'[]\n',
    )
    for index, raw in enumerate(fixtures):
        try:
            strict_load(raw, "E_JSON_CONTROL", "compact", None)
        except ValidationError:
            continue
        raise ValidationError("E_JSON_CONTROL_ACCEPTED:" + str(index))
    return len(fixtures)


def load_artifact() -> tuple[dict[str, Any], bytes, int, int]:
    path = ROOT / ARTIFACT
    require(path.is_file(), "E_ARTIFACT_MISSING")
    raw = path.read_bytes()
    document, nodes, depth = strict_load(raw, "E_ARTIFACT", "compact", "compact")
    return document, raw, nodes, depth


def validate_document(stored: dict[str, Any], expected: dict[str, Any]) -> None:
    errors = document_diagnostics(stored, expected)
    require(errors == set(), sorted(errors)[0] if errors else "E_DOCUMENT")
    require(typed_equal(stored, expected), "E_DOCUMENT_EXACT")


def live_tip(branch: str) -> str:
    output = git_text(["ls-remote", "--heads", "origin", "refs/heads/" + branch])
    fields = output.split("\t")
    require(len(fields) == 2 and fields[1] == "refs/heads/" + branch and is_oid(fields[0]),
            "E_LIVE_REMOTE", branch)
    return fields[0]


def repository_identity_diagnostics(snapshot: dict[str, Any], tip: str) -> set[str]:
    expected = {
        "branch": BRANCH,
        "origin_url": ORIGIN_URL,
        "protected_tracking": PROTECTED_TIP,
        "protected_local": PROTECTED_TIP,
        "protected_live": PROTECTED_TIP,
        "main_tracking": MAIN_TIP,
        "main_live": MAIN_TIP,
        "local_main_returncode": 1,
        "head": tip,
        "upstream": tip,
        "active_tracking": tip,
        "active_live": tip,
        "claude_diff": "",
        "outside_codex_diff": "",
    }
    codes = {
        "branch": "E_BRANCH",
        "origin_url": "E_ORIGIN_URL",
        "protected_tracking": "E_PROTECTED_TRACKING",
        "protected_local": "E_PROTECTED_LOCAL",
        "protected_live": "E_PROTECTED_LIVE",
        "main_tracking": "E_MAIN_TRACKING",
        "main_live": "E_MAIN_LIVE",
        "local_main_returncode": "E_LOCAL_MAIN",
        "head": "E_HEAD",
        "upstream": "E_UPSTREAM",
        "active_tracking": "E_ACTIVE_TRACKING",
        "active_live": "E_ACTIVE_LIVE",
        "claude_diff": "E_CLAUDE_DRIFT",
        "outside_codex_diff": "E_PRODUCTION_DRIFT",
    }
    return {codes[key] for key, value in expected.items()
            if key not in snapshot or not typed_equal(snapshot[key], value)}


def repository_negative_controls() -> int:
    tip = EXPECTED_PARENT
    snapshot = {
        "branch": BRANCH,
        "origin_url": ORIGIN_URL,
        "protected_tracking": PROTECTED_TIP,
        "protected_local": PROTECTED_TIP,
        "protected_live": PROTECTED_TIP,
        "main_tracking": MAIN_TIP,
        "main_live": MAIN_TIP,
        "local_main_returncode": 1,
        "head": tip,
        "upstream": tip,
        "active_tracking": tip,
        "active_live": tip,
        "claude_diff": "",
        "outside_codex_diff": "",
    }
    cases = (
        ("protected_tracking", "0" * 40, "E_PROTECTED_TRACKING"),
        ("main_tracking", "0" * 40, "E_MAIN_TRACKING"),
        ("claude_diff", "Claude/forbidden", "E_CLAUDE_DRIFT"),
        ("outside_codex_diff", "production/forbidden", "E_PRODUCTION_DRIFT"),
    )
    for key, value, code in cases:
        candidate = copy.deepcopy(snapshot)
        candidate[key] = value
        require(code in repository_identity_diagnostics(candidate, tip),
                "E_REPOSITORY_CONTROL", key)
    require("E_STATUS_DIRTY_EXTRA" in status_diagnostics({"outside": " M"}, {}),
            "E_REPOSITORY_CONTROL", "dirty")
    return len(cases) + 1


def parse_status(raw: bytes) -> dict[str, str]:
    result: dict[str, str] = {}
    if raw == b"":
        return result
    require(raw.endswith(b"\0"), "E_STATUS_TERMINATOR")
    records = raw[:-1].split(b"\0")
    for record in records:
        try:
            line = record.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError("E_STATUS_UTF8") from exc
        require(len(line) >= 4 and line[2] == " ", "E_STATUS_ROW", line)
        code = line[:2]
        require(code in {"??", " M", "A ", "M "}, "E_STATUS_CODE", code)
        path = line[3:]
        require(path != "" and path not in result, "E_STATUS_PATH", path)
        result[path] = code
    return result


def status_diagnostics(actual: dict[str, str], expected: dict[str, str]) -> set[str]:
    errors: set[str] = set()
    if set(actual) - set(expected):
        errors.add("E_STATUS_DIRTY_EXTRA")
    if set(expected) - set(actual):
        errors.add("E_STATUS_MISSING")
    if any(actual[path] != expected[path] for path in set(actual) & set(expected)):
        errors.add("E_STATUS_CODE")
    return errors


def require_status(actual: dict[str, str], expected: dict[str, str], label: str) -> None:
    errors = status_diagnostics(actual, expected)
    require(errors == set(), label + "_" + (sorted(errors)[0] if errors else "STATUS"))


def common_repository_guard(tip: str) -> None:
    local_main = run_git(["show-ref", "--verify", "--quiet", "refs/heads/main"], check=False)
    phase_diff = git_text(["diff", "--name-only", PROTECTED_TIP, tip, "--"]).splitlines()
    outside_codex_diff = "\n".join(
        path for path in phase_diff if not path.startswith("Codex/")
    )
    snapshot = {
        "branch": git_text(["symbolic-ref", "--quiet", "--short", "HEAD"]),
        "origin_url": git_text(["remote", "get-url", "origin"]),
        "protected_tracking": git_text([
            "rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}",
        ]),
        "protected_local": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]),
        "protected_live": live_tip(PROTECTED_BRANCH),
        "main_tracking": git_text(["rev-parse", "refs/remotes/origin/main"]),
        "main_live": live_tip("main"),
        "local_main_returncode": local_main.returncode,
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream": git_text(["rev-parse", "@{u}"]),
        "active_tracking": git_text(["rev-parse", f"refs/remotes/origin/{BRANCH}"]),
        "active_live": live_tip(BRANCH),
        "claude_diff": git_text(["diff", "--name-only", PROTECTED_TIP, tip, "--", "Claude"]),
        "outside_codex_diff": outside_codex_diff,
    }
    errors = repository_identity_diagnostics(snapshot, tip)
    require(errors == set(), sorted(errors)[0] if errors else "E_REPOSITORY")


def index_records() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    raw = git_bytes(["ls-files", "--stage", "--", *FINAL_PATHS])
    for line in raw.decode("utf-8").splitlines():
        left, path = line.split("\t", 1)
        mode, oid, stage = left.split(" ")
        require(mode == "100644" and is_oid(oid) and stage == "0", "E_INDEX_ROW", path)
        result[path] = {"mode": mode, "blob_oid": oid}
    return result


def validate_nonartifact_identities(document: dict[str, Any], source: str) -> None:
    records = document["transaction"]["nonartifact_text_identities"]
    require([row["path"] for row in records] == list(NONARTIFACT_PATHS),
            "E_TEXT_IDENTITY_PATHS")
    for row in records:
        path = row["path"]
        if source == "commit":
            raw = git_blob(git_text(["rev-parse", "HEAD"]), path)
        elif source == "index":
            raw = git_blob("", path)
        else:
            raw = (ROOT / path).read_bytes()
        actual = text_identity(path, raw)
        require(typed_equal(actual, row), "E_TEXT_IDENTITY", path)


def validate_repository(mode: str, document: dict[str, Any], commit: str | None) -> None:
    if mode == "persistence":
        require(commit is not None and is_oid(commit), "E_PERSISTENCE_COMMIT")
        tip = commit
    else:
        require(commit is None, "E_UNEXPECTED_COMMIT")
        tip = EXPECTED_PARENT
    common_repository_guard(tip)
    status = parse_status(git_bytes([
        "status", "--porcelain=v1", "-z", "--untracked-files=all",
    ]))
    if mode == "collect":
        expected = {path: ("??" if path in {VALIDATOR, REPORT, GATE_RESULT, RESULT} else " M")
                    for path in NONARTIFACT_PATHS}
        require(not (ROOT / ARTIFACT).exists(), "E_ARTIFACT_EXISTS")
        require_status(status, expected, "E_COLLECT_STATUS")
        require(git_text(["diff", "--cached", "--name-only"]) == "", "E_COLLECT_STAGED")
    elif mode == "content":
        expected = {path: ("??" if path in {VALIDATOR, ARTIFACT, REPORT, GATE_RESULT, RESULT}
                           else " M") for path in FINAL_PATHS}
        require_status(status, expected, "E_CONTENT_STATUS")
        require(git_text(["diff", "--cached", "--name-only"]) == "", "E_CONTENT_STAGED")
        validate_nonartifact_identities(document, "worktree")
    elif mode == "staged":
        expected = {path: ("A " if FINAL_STATUS[path] == "A" else "M ")
                    for path in FINAL_PATHS}
        require_status(status, expected, "E_STAGED_STATUS")
        cached = parse_name_status(git_bytes([
            "diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--",
        ]), "E_STAGED_DIFF")
        require(cached == FINAL_STATUS, "E_STAGED_PATHS")
        require(git_text(["diff", "--name-only"]) == "", "E_STAGED_UNSTAGED")
        index = index_records()
        require(set(index) == set(FINAL_PATHS), "E_STAGED_INDEX_PATHS")
        for path in FINAL_PATHS:
            index_raw = git_bytes(["show", ":" + path])
            worktree_raw = (ROOT / path).read_bytes()
            require(lf_bytes(index_raw, "E_INDEX_" + path) ==
                    lf_bytes(worktree_raw, "E_WORKTREE_" + path),
                    "E_STAGED_BYTE_DRIFT", path)
        validate_nonartifact_identities(document, "worktree")
    else:
        require(mode == "persistence", "E_MODE")
        require_status(status, {}, "E_PERSISTENCE_DIRTY")
        require(commit is not None, "E_PERSISTENCE_COMMIT")
        parent = git_text(["show", "--no-patch", "--format=%P", commit])
        subject = git_text(["show", "--no-patch", "--format=%s", commit])
        require(parent == EXPECTED_PARENT, "E_COMMIT_PARENT")
        require(subject == SUBJECT, "E_COMMIT_SUBJECT")
        diff = parse_name_status(git_bytes([
            "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames", commit, "--",
        ]), "E_COMMIT_DIFF")
        require(diff == FINAL_STATUS, "E_COMMIT_PATHS")
        tree = parse_ls_tree(git_bytes(["ls-tree", commit, "--", *FINAL_PATHS]),
                             "E_COMMIT_TREE")
        require(set(tree) == set(FINAL_PATHS), "E_COMMIT_TREE_PATHS")
        committed_artifact = git_blob(commit, ARTIFACT)
        require(committed_artifact == canonical(document), "E_COMMIT_ARTIFACT")
        validate_nonartifact_identities(document, "commit")


def atomic_collect(raw: bytes) -> None:
    path = ROOT / ARTIFACT
    require(path == ROOT / ARTIFACT, "E_OUTPUT_PATH")
    require(path.parent == ROOT / "Codex/results", "E_OUTPUT_PARENT")
    require(not path.exists(), "E_ARTIFACT_EXISTS")
    temporary = path.with_name(path.name + ".tmp")
    require(not temporary.exists(), "E_TEMP_EXISTS")
    try:
        with temporary.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def execute(mode: str, commit: str | None) -> tuple[dict[str, int], int, int, int, int]:
    if mode == "collect":
        validate_repository("collect", {"transaction": {"nonartifact_text_identities": []}}, None)
        first, measures = build_document()
        second, second_measures = build_document()
        require(typed_equal(first, second) and measures == second_measures,
                "E_DETERMINISM")
        gate_count = gate_controls(first["conformance_rows"])
        semantic_count = semantic_controls(first)
        json_count = json_controls()
        atomic_collect(canonical(first))
        stored, raw, _, _ = load_artifact()
        require(raw == canonical(first) and typed_equal(stored, first), "E_COLLECT_VERIFY")
        return measures, gate_count, semantic_count, json_count, len(first["conformance_rows"])

    stored, raw, _, _ = load_artifact()
    expected, measures = build_document()
    validate_document(stored, expected)
    require(raw == canonical(stored), "E_ARTIFACT_BYTES")
    gate_count = gate_controls(stored["conformance_rows"])
    semantic_count = semantic_controls(expected)
    json_count = json_controls()
    validate_repository(mode, stored, commit)
    return measures, gate_count, semantic_count, json_count, len(stored["conformance_rows"])


def main() -> int:
    try:
        source_controls = validate_source_policy()
        git_controls = git_argv_controls()
        repository_controls = repository_negative_controls()
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--collect", action="store_true")
        group.add_argument("--verify-content", action="store_true")
        group.add_argument("--verify-staged", action="store_true")
        group.add_argument("--verify-persistence", metavar="COMMIT")
        args = parser.parse_args()
        if args.verify_persistence is not None:
            require(is_oid(args.verify_persistence), "E_PERSISTENCE_COMMIT")
            mode = "persistence"
            commit = args.verify_persistence
        else:
            mode = "collect" if args.collect else "content" if args.verify_content else "staged"
            commit = None
        measures, gate_count, semantic_count, json_count, row_count = execute(mode, commit)
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"PASS_P067_STEP90_2_SOURCE_POLICY {source_controls}/{source_controls} "
          f"git_argv={git_controls}/{git_controls} "
          f"repository={repository_controls}/{repository_controls}")
    print(f"PASS_P067_STEP90_2_CONTROLS semantic={semantic_count}/{semantic_count} "
          f"json={json_count}/{json_count} gate={gate_count}/{gate_count} "
          f"units=9/9 inputs={len(MACHINE_SPECS)}/{len(MACHINE_SPECS)} "
          f"rows={row_count} nodes={measures['nodes']} depth={measures['depth']}")
    print(PERSISTENCE if mode == "persistence" else GATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
