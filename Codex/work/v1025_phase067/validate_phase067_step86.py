#!/usr/bin/env python3
"""Validate Phase 067 Step 86 evidence and Git transaction boundaries."""

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
import struct
import subprocess
import sys
import tempfile
import zipfile
from io import BytesIO
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "3f2c7635aa545bd617b6cd83b5e718683d5b2b1c"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = "origin/codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
SUBJECT = "audit(phase067): adjudicate test demo golden behavior"
GATE = "PASS_P067_STEP86_TEST_DEMO_GOLDEN"
PERSISTENCE = "PASS_P067_STEP86_PERSISTENCE"
DATE = "2026-09-02"
BUILDER_SOURCE_POLICY_SHA256_LF = "031c31aa142f59950074794337d9dcfbb840f984c3e4f2504ae564e2fad89c08"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "93f1c8df556c67b2db3a8451c5f6614e8be50c36d701aa7e218c495b3609601a"

MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
MANIFEST_RAW_SHA = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
INVENTORY_RAW_SHA = "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63"
INVENTORY_SEMANTIC_SHA = "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"
ATTESTATION_RAW_SHA = "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174"
ATTESTATION_SEMANTIC_SHA = "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"
EXPECTED_RUNTIME_RECORDS_SHA256 = "45673d528eaa826d4f1876ef67d09d8c0ec41d7e757f357b263b48a8cfd0a267"

BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step86.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step86.py"
MATRIX_PATH = "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json"
CONFORMANCE_PATH = "Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, CONFORMANCE_PATH,
               RESULT_PATH, PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if i < 5 else "M") for i, path in enumerate(FINAL_PATHS)}
CONTROL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, RESULT_PATH, PARENT_LEDGER,
                 CANONICAL_LEDGER, HANDOVER)
CONTROL_SHA256 = {
    RESULT_PATH: "d8750f51bd12162d6fb4099bba9deaf8b31b8ea6c11431b94b07eafb09b6aa5c",
    PARENT_LEDGER: "ac8d0a3a696e4305e3f9935fddb8157027b6b070087b163f86b26307b31f47d9",
    CANONICAL_LEDGER: "e0b7d2c1aecb5b0ab0560786df8480c278663df30b22c9e2b343129419291078",
    HANDOVER: "236ae90e927e739e0f427f974c1a5e679fa231d3e3ab53402ef682214cd80b3f",
}
EXPECTED = {
    "test_occurrences": 44, "test_blobs": 29, "test_lines": 6042,
    "demo_occurrences": 30, "demo_blobs": 26, "demo_lines": 3300,
    "result_occurrences": 35, "result_blobs": 14, "result_lines": 2081,
    "golden_occurrences": 8, "golden_blobs": 2,
    "guide_occurrences": 20, "guide_blobs": 8, "guide_lines": 854,
}
EXPECTED_RUNTIME_CONTRACT = {
    "representative_unique_blob_execution": True,
    "occurrence_projection_is_not_independent_corroboration": True,
    "network_allowed": False,
    "repository_external_disposable_roots": True,
    "runtime_authority": "OBSERVED_ISOLATED_PROCESS_ONLY",
    "runtime_records_sha256": EXPECTED_RUNTIME_RECORDS_SHA256,
}
EXPECTED_GOLDEN_CONTRACT = {
    "two_blobs_must_remain_distinct": True,
    "capture_overwrite_by_release": "v1.0.13-v1.0.18.2 np.savez overwrite-capable; v1.0.19 refuses existing with exit 3",
    "later_test_gate_load_is_not_current_release_golden_provenance": True,
}
EXPECTED_GUIDE_CONTRACT = {
    "guide_prose_is_self_report_until_exact_source_assertion_and_runtime_bound": True,
    "manifest_entry_index_base": 0,
    "stale_claims_preserved": True,
    "mirror_occurrences_not_corroboration": True,
}
EXPECTED_TOOL_CONTRACT = {
    "hardcoded_paths_are_portability_evidence_not_skip": True,
    "optional_dependency_failure_is_not_pass": True,
    "writer_and_check_modes_are_distinct": True,
    "stdout_pass_without_assert_or_exit_is_not_gate": True,
}


class ValidationError(RuntimeError):
    pass


def require(ok: bool, diagnostic: str, detail: str = "") -> None:
    if not ok:
        raise ValidationError(diagnostic + ((":" + detail) if detail else ""))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


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


def strict_load(raw: bytes, label: str, generated_artifact: bool = True) -> tuple[dict[str, Any], int, int]:
    require(not raw.startswith(b"\xef\xbb\xbf"), "E_JSON_BOM", label)
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, "E_JSON_DUPLICATE", f"{label}:{key}")
            out[key] = value
        return out
    def bad(token: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{label}:{token}")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad)
    require(isinstance(value, dict), "E_JSON_TOP", label)
    nodes, depth_max = 0, 0
    stack = [(value, 1)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        depth_max = max(depth_max, depth)
        require(nodes <= 2_000_000 and depth <= 24, "E_JSON_BOUNDS", label)
        if isinstance(current, dict):
            stack.extend((x, depth + 1) for x in current.values())
        elif isinstance(current, list):
            stack.extend((x, depth + 1) for x in current)
        elif isinstance(current, float):
            require(math.isfinite(current), "E_JSON_NONFINITE", label)
    if generated_artifact:
        require(raw == canonical(value), "E_JSON_CANONICAL", label)
        require(value.get("semantic_sha256") == semantic(value), "E_JSON_SEMANTIC", label)
    return value, nodes, depth_max


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    allowed = False
    if args in {
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
    }:
        allowed = True
    elif len(args) == 2 and args[0] == "show" and ":" in args[1]:
        rev, path = args[1].split(":", 1)
        allowed = rev in {EXPECTED_PARENT, BASELINE, ""} or bool(re.fullmatch(r"[0-9a-f]{40}", rev))
        allowed = allowed and (path in {MANIFEST_PATH, INVENTORY_PATH, ATTESTATION_PATH, *FINAL_PATHS}
                               or path.startswith("Claude/docs/"))
    elif len(args) == 3 and args[:2] == ("cat-file", "blob"):
        allowed = bool(re.fullmatch(r"[0-9a-f]{40}", args[2]))
    elif len(args) == 3 and args[:2] == ("show", "-s") and args[2].startswith("--format="):
        allowed = False
    elif len(args) == 4 and args[:2] == ("show", "-s") and args[2] in {"--format=%P", "--format=%s"}:
        allowed = bool(re.fullmatch(r"[0-9a-f]{40}", args[3]))
    elif len(args) == 2 and args[0] == "rev-parse" and args[1].endswith("^"):
        allowed = bool(re.fullmatch(r"[0-9a-f]{40}\^", args[1]))
    elif len(args) == 8 and args[:5] == ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r"):
        allowed = (bool(re.fullmatch(r"[0-9a-f]{40}\^", args[5]))
                   and bool(re.fullmatch(r"[0-9a-f]{40}", args[6]))
                   and args[7] == "--")
    elif len(args) == 4 and args[:2] == ("ls-tree", "-r"):
        allowed = bool(re.fullmatch(r"[0-9a-f]{40}", args[2])) and args[3] == ""
    return allowed


def git(args: tuple[str, ...], allow_failure: bool = False) -> bytes:
    require(git_argv_allowed(args), "E_GIT_ARGV", repr(args))
    proc = subprocess.run(("git", *args), cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    require(allow_failure or proc.returncode == 0, "E_GIT_EXIT", f"{args}:{proc.returncode}")
    return proc.stdout


def gtext(args: tuple[str, ...], allow_failure: bool = False) -> str:
    return git(args, allow_failure).decode("utf-8").rstrip("\r\n")


def commit_bytes(path: str) -> bytes:
    return git(("show", f"{EXPECTED_PARENT}:{path}"))


def input_documents() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_raw = commit_bytes(MANIFEST_PATH)
    inventory_raw = commit_bytes(INVENTORY_PATH)
    attestation_raw = commit_bytes(ATTESTATION_PATH)
    require(sha(manifest_raw) == MANIFEST_RAW_SHA, "E_MANIFEST_PIN")
    require(sha(inventory_raw) == INVENTORY_RAW_SHA, "E_INVENTORY_PIN")
    require(sha(attestation_raw) == ATTESTATION_RAW_SHA, "E_ATTESTATION_PIN")
    manifest, _, _ = strict_load(manifest_raw, MANIFEST_PATH, False)
    inventory, _, _ = strict_load(inventory_raw, INVENTORY_PATH, False)
    attestation, _, _ = strict_load(attestation_raw, ATTESTATION_PATH, False)
    require(inventory["semantic_sha256"] == INVENTORY_SEMANTIC_SHA, "E_INVENTORY_SEMANTIC")
    require(attestation.get("semantic_sha256") == ATTESTATION_SEMANTIC_SHA
            and predecessor_semantic(attestation) == ATTESTATION_SEMANTIC_SHA,
            "E_ATTESTATION_SEMANTIC")
    return manifest, inventory


def blob(oid: str) -> bytes:
    return git(("cat-file", "blob", oid))


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__,
                **{field: stable_ast(getattr(value, field, None)) for field in value._fields}}
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if isinstance(value, complex):
        return {"_complex": [value.real, value.imag]}
    if value is Ellipsis:
        return {"_ellipsis": True}
    return value


def call_name(node: ast.Call) -> str:
    names: list[str] = []
    current: ast.AST = node.func
    while isinstance(current, ast.Attribute):
        names.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        names.append(current.id)
    return ".".join(reversed(names))


def independent_static(oid: str, role: str) -> dict[str, Any]:
    raw = blob(oid)
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    names, imports, assertions, exits, files, mutations = [], [], [], [], [], []
    def anchor(node: ast.AST) -> dict[str, Any]:
        segment = ast.get_source_segment(source, node) or ""
        return {"ast_kind": type(node).__name__, "start_line": int(getattr(node, "lineno", 0)),
                "end_line": int(getattr(node, "end_lineno", getattr(node, "lineno", 0))),
                "source_sha256_lf": sha(segment.replace("\r\n", "\n").encode()),
                "normalized_ast_sha256": sha(canonical(stable_ast(node)))}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
        if isinstance(node, ast.Assert):
            assertions.append({"anchor": anchor(node), "expression": ast.unparse(node.test),
                               "message": None if node.msg is None else ast.unparse(node.msg)})
        if isinstance(node, ast.Call):
            name = call_name(node)
            rec = {"name": name, "anchor": anchor(node),
                   "literal_args": [x.value for x in node.args if isinstance(x, ast.Constant)
                                    and isinstance(x.value, (str, int, float, bool, type(None)))]}
            names.append(name)
            if name in {"sys.exit", "exit"}: exits.append(rec)
            if name.split(".")[-1] in {"open", "load", "save", "savez", "savez_compressed",
                                       "write_text", "write_bytes", "unlink", "remove", "replace",
                                       "rename", "mkdir", "makedirs", "rmtree", "savefig"}: files.append(rec)
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)) and any(
                isinstance(x, (ast.Attribute, ast.Subscript)) for x in ast.walk(node)):
            mutations.append({"anchor": anchor(node), "statement": ast.unparse(node)})
    obs = {"print_calls": sum(x.split(".")[-1] == "print" for x in names),
           "plot_calls": sum(x.split(".")[-1] in {"plot", "show", "savefig", "figure", "subplots"} for x in names),
           "finite_checks": sum(x.split(".")[-1] in {"isfinite", "isnan", "allclose", "array_equal"} for x in names),
           "assertions": len(assertions), "exit_calls": len(exits)}
    enforcement = (("ASSERT_AND_EXIT" if assertions and exits else "EXIT_ONLY" if exits else "NO_EXECUTABLE_GATE")
                   if role == "test" else ("EXIT_ONLY" if exits else "NO_EXECUTABLE_GATE")
                   if role == "demo" else ("ASSERT_ONLY" if assertions and not exits else
                                            "ASSERT_AND_EXIT" if assertions and exits else
                                            "EXIT_ONLY" if exits else "NO_EXECUTABLE_GATE"))
    return {"blob_oid": oid, "raw_sha256": sha(raw), "lf_sha256": sha(raw.replace(b"\r\n", b"\n")),
            "size_bytes": len(raw), "physical_lines": len(source.splitlines()), "encoding": "utf-8",
            "ast_parse": "PASS", "role": role, "imports": sorted(imports), "assertions": assertions,
            "exit_calls": exits, "file_surfaces": files, "mutation_surfaces": mutations,
            "observation_counts": obs, "enforcement_class": enforcement,
            "call_name_set": sorted(set(names))}


def independent_guide(manifest: dict[str, Any], runtime_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entries = [entry for entry in manifest["entries"]
               if entry["path"].endswith("/FITTING_GUIDE.md")
               and entry["role"] == "implementation_guide" and entry["extension"] == "md"
               and entry["review_mode"] == "FULL_TEXT"]
    occurrences = [{"ordinal": ordinal, "manifest_entry_index": manifest["entries"].index(entry),
                    "release": entry["version"], "path": entry["path"],
                    "blob_oid": entry["blob_sha"], "git_mode": entry["git_mode"],
                    "size_bytes": entry["size_bytes"], "physical_lines": entry["extent"]["lines"]}
                   for ordinal, entry in enumerate(entries, 1)]
    by_blob: dict[str, list[dict[str, Any]]] = {}
    for row in occurrences:
        by_blob.setdefault(row["blob_oid"], []).append(row)
    runtime_names = sorted({Path(row["representative_path"]).name for row in runtime_rows})
    runtime_zero = {Path(row["representative_path"]).name for row in runtime_rows
                    if row["exit_code"] == 0 and not row["timed_out"]}
    records = []
    for oid in sorted(by_blob):
        raw = blob(oid)
        lines = raw.decode("utf-8").splitlines()
        line_records = []
        for number, line in enumerate(lines, 1):
            stripped = line.strip()
            mentions = [name for name in runtime_names if name in line]
            if stripped == "":
                kind = "BLANK"
            elif stripped.startswith("#"):
                kind = "HEADING"
            elif stripped.startswith("```"):
                kind = "FENCE"
            elif re.fullmatch(r"\|?(?:\s*:?-+:?\s*\|)+", stripped):
                kind = "TABLE_RULE"
            elif stripped.startswith("|"):
                kind = "TABLE_HEADER" if number == 1 or (number < len(lines) and re.fullmatch(
                    r"\|?(?:\s*:?-+:?\s*\|)+", lines[number].strip())) else "CLAIM"
            elif stripped.startswith("<!--"):
                kind = "COMMENT"
            elif stripped.startswith((">", "-", "*", "+")) or re.match(r"^\d+[.)]\s", stripped):
                kind = "CLAIM"
            elif stripped.startswith(("$", "python ", "py ", "pytest ")):
                kind = "CODE_OR_COMMAND"
            else:
                kind = "CLAIM"
            claim_like = kind == "CLAIM"
            bound = [name for name in mentions if name in runtime_zero]
            disposition = ("STRUCTURAL_OR_BLANK" if not claim_like else
                           "RUNTIME_EXIT_ZERO_REFERENCE_NOT_PROPOSITION_PROOF" if bound else
                           "SOURCE_NAME_BOUND_SELF_REPORT" if mentions else
                           "SELF_REPORT_UNBOUND_OR_STALE")
            line_records.append({"line": number, "raw_sha256": sha(line.encode("utf-8")),
                                 "text": line, "mentioned_script_names": mentions,
                                 "line_kind": kind, "claim_like": claim_like,
                                 "disposition": disposition})
        titles = [row["text"].lstrip("#").strip() for row in line_records
                  if row["line_kind"] == "HEADING"]
        records.append({"blob_oid": oid, "raw_sha256": sha(raw),
                        "lf_sha256": sha(raw.replace(b"\r\n", b"\n")),
                        "size_bytes": len(raw), "physical_lines": len(lines),
                        "occurrence_paths": [row["path"] for row in by_blob[oid]],
                        "release_projection": [row["release"] for row in by_blob[oid]],
                        "title_spelling": titles[0] if titles else "GROUND_NOT_FOUND",
                        "coverage": {"first_line": 1, "last_line": len(lines),
                                     "covered_lines": len(line_records), "gaps": 0, "overlaps": 0},
                        "line_records": line_records})
    return occurrences, records


def parse_npy(raw: bytes) -> dict[str, Any]:
    require(raw.startswith(b"\x93NUMPY"), "E_NPY_MAGIC")
    major, minor = raw[6], raw[7]
    require((major, minor) in {(1, 0), (2, 0), (3, 0)}, "E_NPY_VERSION")
    if major == 1:
        count, start = struct.unpack("<H", raw[8:10])[0], 10
    else:
        count, start = struct.unpack("<I", raw[8:12])[0], 12
    header_raw = raw[start:start + count]
    header = ast.literal_eval(header_raw.decode("latin1").strip())
    require(header == {"descr": "<f8", "fortran_order": False, "shape": (1000,)}, "E_NPY_HEADER")
    data = raw[start + count:]
    require(len(data) == 8000, "E_NPY_DATA")
    values = struct.unpack("<1000d", data)
    return {"dtype": "float64", "shape": [1000], "size": 1000, "finite_count": 1000,
            "finite_min": min(values), "finite_max": max(values), "member_sha256": sha(raw),
            "value_bytes_sha256": sha(data), "npy_header_sha256": sha(header_raw)}


def independent_golden(entry: dict[str, Any]) -> dict[str, Any]:
    raw = blob(entry["blob_sha"])
    members = []
    with zipfile.ZipFile(BytesIO(raw)) as zf:
        for info in zf.infolist():
            payload = zf.read(info.filename)
            members.append({"key": info.filename[:-4], "zip_member": info.filename,
                            "crc32": info.CRC, "compress_type": info.compress_type,
                            "compressed_size": info.compress_size, "uncompressed_size": info.file_size,
                            **parse_npy(payload)})
    return {"blob_oid": entry["blob_sha"], "raw_sha256": sha(raw), "size_bytes": len(raw),
            "member_count": 13, "member_order": [x["key"] for x in members], "members": members,
            "value_projection_sha256": sha(canonical([
                {"key": x["key"], "value_bytes_sha256": x["value_bytes_sha256"]} for x in members]))}


HEADER_KEYS = {"schema_version", "artifact", "phase", "step", "generated_date", "baseline_commit",
               "expected_parent", "branch", "expected_subject", "gate", "precommit_status",
               "containing_commit", "persistence_terminal", "result_first", "json_outputs_last",
               "semantic_sha256"}
MATRIX_KEYS = HEADER_KEYS | {"inputs", "universe", "occurrence_projection", "python_blob_static_records",
                            "enforcement_summary",
                            "runtime_contract", "runtime_records", "golden_blob_records", "golden_contract",
                            "golden_route_records", "validation", "authority"}
CONFORMANCE_KEYS = HEADER_KEYS | {"inputs", "matrix_semantic_sha256", "guide_occurrence_projection",
                                 "guide_blob_records", "tool_occurrence_projection", "tool_blob_records",
                                 "guide_contract", "tool_contract", "validation", "authority"}


def expected_occurrences(manifest: dict[str, Any], inventory: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    roles = {name: [copy.deepcopy(x) for x in inventory["occurrence_records"] if x["role"] == role]
             for name, role in (("test", "test"), ("demo", "demo"), ("result_tool", "result"))}
    gold = [x for x in manifest["entries"] if x["path"].endswith("/golden_graphite_ref.npz")]
    roles["golden"] = [{"ordinal": i, "release": x["version"], "path": x["path"],
                        "blob_oid": x["blob_sha"], "git_mode": x["git_mode"], "size_bytes": x["size_bytes"]}
                       for i, x in enumerate(gold, 1)]
    return roles


def expected_enforcement(occurrences: dict[str, list[dict[str, Any]]],
                         static_records: list[dict[str, Any]]) -> dict[str, Any]:
    by_oid = {x["blob_oid"]: x for x in static_records}
    result: dict[str, Any] = {}
    for name in ("test", "demo", "result_tool"):
        blobs: dict[str, int] = {}
        occ: dict[str, int] = {}
        for oid in sorted({x["blob_oid"] for x in occurrences[name]}):
            key = by_oid[oid]["enforcement_class"]
            blobs[key] = blobs.get(key, 0) + 1
        for row in occurrences[name]:
            key = by_oid[row["blob_oid"]]["enforcement_class"]
            occ[key] = occ.get(key, 0) + 1
        result[name] = {"unique_blob_counts": dict(sorted(blobs.items())),
                        "occurrence_counts": dict(sorted(occ.items()))}
    return result


def expected_golden_routes(test_rows: list[dict[str, Any]],
                           static_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_oid = {x["blob_oid"]: x for x in static_records}
    out = []
    overwrite = {"v1.0.13", "v1.0.14", "v1.0.15", "v1.0.16", "v1.0.17",
                 "v1.0.18.1", "v1.0.18.2"}
    later = {"v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23", "v1.0.24", "v1.0.24.1",
             "v1.0.25", "v1.0.25.1", "v1.0.25.2"}
    for row in test_rows:
        names = by_oid[row["blob_oid"]]["call_name_set"]
        if not any(x.split(".")[-1] in {"load", "savez", "savez_compressed"} for x in names):
            continue
        release = row["release"]
        cls = ("EXPLICIT_CAPTURE_OVERWRITES_DISPOSABLE_EXISTING_GOLDEN" if release in overwrite else
               "EXPLICIT_CAPTURE_REFUSES_EXISTING_EXIT_3" if release == "v1.0.19" else
               "AUXILIARY_V1_0_19_GOLDEN_LOAD_ONLY_NO_CURRENT_RELEASE_GOLDEN_PROVENANCE" if release in later else
               "UNRELATED_OR_EXTERNAL_GOLDEN_ROUTE")
        out.append({"release": release, "path": row["path"], "blob_oid": row["blob_oid"],
                    "capture_overwrite_class": cls, "source_static_only": True,
                    "repository_golden_mutated": False})
    return out


def artifact_errors(matrix: dict[str, Any], conformance: dict[str, Any],
                    manifest: dict[str, Any], inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    def check(ok: bool, name: str) -> None:
        if not ok: errors.append(name)
    check(set(matrix) == MATRIX_KEYS, "matrix_keys")
    check(set(conformance) == CONFORMANCE_KEYS, "conformance_keys")
    check(typed_equal(matrix.get("runtime_contract"), EXPECTED_RUNTIME_CONTRACT), "runtime_contract")
    check(typed_equal(matrix.get("golden_contract"), EXPECTED_GOLDEN_CONTRACT), "golden_contract")
    check(typed_equal(conformance.get("guide_contract"), EXPECTED_GUIDE_CONTRACT), "guide_contract")
    check(typed_equal(conformance.get("tool_contract"), EXPECTED_TOOL_CONTRACT), "tool_contract")
    for value, artifact in ((matrix, "PHASE_067_TEST_DEMO_GOLDEN_MATRIX"),
                            (conformance, "PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX")):
        expected_meta = {"schema_version": "P067-S86-1", "artifact": artifact, "phase": 67, "step": 86,
                         "generated_date": DATE, "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
                         "branch": BRANCH, "expected_subject": SUBJECT, "gate": GATE,
                         "precommit_status": "PASS_PENDING_PERSISTENCE",
                         "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
                         "persistence_terminal": PERSISTENCE, "result_first": True, "json_outputs_last": True}
        check(all(typed_equal(value.get(k), v) for k, v in expected_meta.items()), artifact + ":metadata")
        check(typed_equal(value.get("universe", EXPECTED), EXPECTED), artifact + ":universe")
        expected_inputs = {"manifest": {"path": MANIFEST_PATH, "raw_sha256": MANIFEST_RAW_SHA},
                           "inventory": {"path": INVENTORY_PATH, "raw_sha256": INVENTORY_RAW_SHA,
                                         "semantic_sha256": INVENTORY_SEMANTIC_SHA},
                           "attestation": {"path": ATTESTATION_PATH, "raw_sha256": ATTESTATION_RAW_SHA,
                                           "semantic_sha256": ATTESTATION_SEMANTIC_SHA},
                           "persisted_chain": {"step82": "db167fdc941eafba0313b8476dfe7483108f13ff",
                                               "step83": "1af6c06fb5cff2918b846ed74ea213832f04f010",
                                               "step84": "f00bf2fa8f25c85f0c62cb901912763d98c8f070",
                                               "step85_current_parent": EXPECTED_PARENT,
                                               "inventory_containing_commit_is_owner": False},
                           "controls": {path: {"raw_sha256": sha((ROOT / path).read_bytes()),
                                               "lf_sha256": sha((ROOT / path).read_bytes().replace(b"\r\n", b"\n"))}
                                        for path in CONTROL_PATHS}}
        check(typed_equal(value.get("inputs"), expected_inputs), artifact + ":inputs")
    expected_occ = expected_occurrences(manifest, inventory)
    check(typed_equal(matrix.get("occurrence_projection"), expected_occ), "occurrence_projection")
    stored_static = matrix.get("python_blob_static_records", [])
    check(isinstance(stored_static, list), "static_type")
    if isinstance(stored_static, list):
        expected_static = []
        for role in ("test", "demo", "result"):
            for oid in sorted({x["blob_oid"] for x in inventory["occurrence_records"] if x["role"] == role}):
                expected_static.append(independent_static(oid, role))
        expected_static.sort(key=lambda x: x["blob_oid"])
        check(typed_equal(stored_static, expected_static), "static_projection")
        check(typed_equal(matrix.get("enforcement_summary"), expected_enforcement(expected_occ, expected_static)),
              "enforcement_summary")
        check(typed_equal(matrix.get("golden_route_records"),
                          expected_golden_routes(expected_occ["test"], expected_static)),
              "golden_routes")
    gold_entries = [x for x in manifest["entries"] if x["path"].endswith("/golden_graphite_ref.npz")]
    expected_gold = [independent_golden(next(x for x in gold_entries if x["blob_sha"] == oid))
                     for oid in sorted({x["blob_sha"] for x in gold_entries})]
    check(typed_equal(matrix.get("golden_blob_records"), expected_gold), "golden_projection")
    guide_entries = [entry for entry in manifest["entries"]
                     if entry["path"].endswith("/FITTING_GUIDE.md")
                     and entry["role"] == "implementation_guide" and entry["extension"] == "md"
                     and entry["review_mode"] == "FULL_TEXT"]
    guide_occ, expected_guide_rows = independent_guide(manifest, matrix.get("runtime_records", []))
    check(typed_equal(conformance.get("guide_occurrence_projection"), guide_occ), "guide_occurrences")
    tool_occ = [copy.deepcopy(x) for x in inventory["occurrence_records"] if x["role"] == "result"]
    check(typed_equal(conformance.get("tool_occurrence_projection"), tool_occ), "tool_occurrences")
    expected_tool = [independent_static(oid, "result") for oid in sorted({x["blob_oid"] for x in tool_occ})]
    check(typed_equal(conformance.get("tool_blob_records"), expected_tool), "tool_projection")
    guide_rows = conformance.get("guide_blob_records", [])
    check(isinstance(guide_rows, list) and len(guide_rows) == 8, "guide_blobs")
    check(typed_equal(guide_rows, expected_guide_rows), "guide_projection")
    if isinstance(guide_rows, list):
        runtime_names = sorted({Path(x.get("representative_path", "")).name for x in matrix.get("runtime_records", [])
                                if isinstance(x, dict)})
        runtime_zero = {Path(x.get("representative_path", "")).name for x in matrix.get("runtime_records", [])
                        if isinstance(x, dict) and x.get("exit_code") == 0 and not x.get("timed_out")}
        by_oid = {x["blob_sha"]: [] for x in guide_entries}
        for i, entry in enumerate(guide_entries, 1):
            by_oid[entry["blob_sha"]].append(guide_occ[i - 1])
        for record in guide_rows:
            oid = record.get("blob_oid", "")
            if oid not in by_oid:
                errors.append("guide_oid"); continue
            raw = blob(oid); lines = raw.decode("utf-8").splitlines()
            check(record.get("raw_sha256") == sha(raw), "guide_raw")
            check(record.get("physical_lines") == len(lines), "guide_lines")
            check(record.get("occurrence_paths") == [x["path"] for x in by_oid[oid]], "guide_paths")
            titles = [line.lstrip("#").strip() for line in lines if line.strip().startswith("#")]
            check(record.get("title_spelling") == (titles[0] if titles else "GROUND_NOT_FOUND"), "guide_title")
            check(record.get("coverage") == {"first_line": 1, "last_line": len(lines),
                                               "covered_lines": len(lines), "gaps": 0, "overlaps": 0},
                  "guide_coverage")
            lr = record.get("line_records", [])
            check(len(lr) == len(lines), "guide_line_records")
            for index, line in enumerate(lines, 1):
                if index <= len(lr):
                    stripped = line.strip()
                    if stripped == "": expected_kind = "BLANK"
                    elif stripped.startswith("#"): expected_kind = "HEADING"
                    elif stripped.startswith("```"): expected_kind = "FENCE"
                    elif re.fullmatch(r"\|?(?:\s*:?-+:?\s*\|)+", stripped): expected_kind = "TABLE_RULE"
                    elif stripped.startswith("|"):
                        expected_kind = "TABLE_HEADER" if index == 1 or (index < len(lines) and re.fullmatch(r"\|?(?:\s*:?-+:?\s*\|)+", lines[index].strip())) else "CLAIM"
                    elif stripped.startswith("<!--"): expected_kind = "COMMENT"
                    elif stripped.startswith((">", "-", "*", "+")) or re.match(r"^\d+[.)]\s", stripped): expected_kind = "CLAIM"
                    elif stripped.startswith(("$", "python ", "py ", "pytest ")): expected_kind = "CODE_OR_COMMAND"
                    else: expected_kind = "CLAIM"
                    mentions = [name for name in runtime_names if name in line]
                    claim_like = expected_kind == "CLAIM"
                    bound = [x for x in mentions if x in runtime_zero]
                    expected_disposition = ("STRUCTURAL_OR_BLANK" if not claim_like else
                                            "RUNTIME_EXIT_ZERO_REFERENCE_NOT_PROPOSITION_PROOF" if bound else
                                            "SOURCE_NAME_BOUND_SELF_REPORT" if mentions else
                                            "SELF_REPORT_UNBOUND_OR_STALE")
                    check(lr[index - 1].get("line") == index and lr[index - 1].get("text") == line
                          and lr[index - 1].get("raw_sha256") == sha(line.encode()), "guide_line_exact")
                    check(lr[index - 1].get("line_kind") == expected_kind
                          and lr[index - 1].get("claim_like") is claim_like
                          and lr[index - 1].get("mentioned_script_names") == mentions
                          and lr[index - 1].get("disposition") == expected_disposition,
                          "guide_line_semantic")
    check(matrix.get("validation") == {"denominator_mismatch": 0, "ast_parse_failure": 0,
                                        "golden_member_failure": 0, "source_read_failure": 0,
                                        "runtime_assumption_promotions": 0}, "matrix_validation")
    check(conformance.get("validation") == {"guide_line_mismatch": 0, "tool_blob_orphan": 0,
                                             "stale_claim_promotion": 0, "authority_promotion": 0},
          "conformance_validation")
    check(matrix.get("authority") == {"source_static": True, "isolated_runtime_observation": True,
                                       "test_pass_global": False, "demo_assertion_authority": False,
                                       "scientific_truth": False, "material_validity": False,
                                       "canonical_release": False, "publication_ready": False}, "matrix_authority")
    check(conformance.get("authority") == {"source_static": True, "guide_claim_truth": False,
                                            "result_tool_output_validity": False, "scientific_truth": False,
                                            "material_validity": False, "canonical_release": False,
                                            "publication_ready": False}, "conformance_authority")
    check(conformance.get("matrix_semantic_sha256") == matrix.get("semantic_sha256"), "matrix_binding")
    runtime_keys = {"runtime", "launcher", "argv_tail", "blob_oid", "representative_path",
                    "representative_release", "exit_code", "timed_out", "stdout", "stderr",
                    "stdout_sha256", "stderr_sha256", "filesystem_changes", "inventory_present",
                    "framework_kind", "runtime_collection_status", "runtime_execution_status",
                    "static_skip_predicates", "observed_skip", "outcome", "enforcement_class",
                    "assertion_count", "exit_call_count", "authority"}
    runtime_rows = matrix.get("runtime_records", [])
    check(isinstance(runtime_rows, list) and len(runtime_rows) == 110, "runtime_count")
    check(isinstance(runtime_rows, list)
          and sha(canonical(runtime_rows)) == EXPECTED_RUNTIME_RECORDS_SHA256,
          "runtime_records_pin")
    if isinstance(runtime_rows, list) and isinstance(stored_static, list):
        by_static = {x["blob_oid"]: x for x in stored_static}
        source_rows = expected_occ["test"] + expected_occ["demo"]
        reps: dict[str, dict[str, Any]] = {}
        for row in source_rows:
            reps.setdefault(row["blob_oid"], row)
        expected_pairs = {(oid, runtime) for oid in reps for runtime in ("3.12", "3.14")}
        seen: set[tuple[str, str]] = set()
        allowed_outcome = {"PASS_EXIT_GATE", "FAIL_EXIT_GATE", "MANUAL_OBSERVATION",
                           "EXPECTED_FAILURE", "DEPENDENCY_MISSING", "TIMEOUT", "GROUND_NOT_FOUND"}
        for row in runtime_rows:
            check(isinstance(row, dict) and set(row) == runtime_keys, "runtime_keys")
            if not isinstance(row, dict):
                continue
            oid, runtime = row.get("blob_oid"), row.get("runtime")
            pair = (oid, runtime)
            check(pair in expected_pairs and pair not in seen, "runtime_pair")
            seen.add(pair)
            if oid not in reps or oid not in by_static:
                continue
            rep, static = reps[oid], by_static[oid]
            check(row.get("representative_path") == rep["path"] and
                  row.get("representative_release") == rep["release"], "runtime_representative")
            check(row.get("launcher") == ["py", f"-{runtime}"], "runtime_launcher")
            expected_tail = ["-B", "-I", "-X", "utf8", Path(rep["path"]).name]
            if "regression" in Path(rep["path"]).name:
                expected_tail.append("verify")
            check(row.get("argv_tail") == expected_tail, "runtime_argv")
            check(row.get("inventory_present") is True and row.get("framework_kind") == "TOP_LEVEL_SCRIPT",
                  "runtime_inventory")
            check(row.get("runtime_collection_status") == "NOT_COLLECTABLE", "runtime_collection")
            check(row.get("runtime_execution_status") in {"PASS", "FAIL", "SKIP", "ERROR"}, "runtime_execution")
            check(row.get("outcome") in allowed_outcome, "runtime_outcome")
            check(row.get("authority") == "ISOLATED_REPRESENTATIVE_OCCURRENCE_ONLY", "runtime_authority")
            check(row.get("enforcement_class") == static["enforcement_class"], "runtime_enforcement")
            check(row.get("assertion_count") == static["observation_counts"]["assertions"] and
                  row.get("exit_call_count") == static["observation_counts"]["exit_calls"], "runtime_gate_counts")
            check(row.get("static_skip_predicates") == [x for x in static["call_name_set"]
                                                         if x.split(".")[-1] in {"skip", "skipif", "xfail"}],
                  "runtime_skip_static")
            check(type(row.get("observed_skip")) is bool and type(row.get("timed_out")) is bool,
                  "runtime_bool_types")
            check(type(row.get("stdout")) is str and type(row.get("stderr")) is str and
                  row.get("stdout_sha256") == sha(row.get("stdout", "").encode()) and
                  row.get("stderr_sha256") == sha(row.get("stderr", "").encode()), "runtime_transcript")
            check("p067_s86_" not in row.get("stdout", "") + row.get("stderr", ""), "runtime_temp_leak")
            changes = row.get("filesystem_changes")
            check(isinstance(changes, list), "runtime_changes_type")
            if isinstance(changes, list):
                for change in changes:
                    check(isinstance(change, dict) and set(change) == {"path", "change", "before", "after",
                                                                      "content_hash_class", "content_hash_authority"},
                          "runtime_change_keys")
                    if isinstance(change, dict):
                        check(type(change.get("path")) is str and not Path(change["path"]).is_absolute()
                              and ".." not in Path(change["path"]).parts, "runtime_change_path")
                        check("__pycache__" not in change["path"] and not change["path"].endswith(".pyc"),
                              "runtime_cache_residue")
                        font_cache = bool(re.fullmatch(r"home/\.matplotlib/fontlist-v[0-9]+\.json",
                                                       change["path"]))
                        check(change.get("content_hash_class") == ("NONDETERMINISTIC_THIRD_PARTY_CACHE"
                                                                   if font_cache else "EXACT")
                              and change.get("content_hash_authority") is (not font_cache),
                              "runtime_change_authority")
                        for side in (change.get("before"), change.get("after")):
                            if side is not None:
                                check(isinstance(side, dict) and set(side) == {"size", "sha256"}
                                      and type(side["size"]) is int, "runtime_change_side")
                                check(side["sha256"] == ("WITHHELD_NONDETERMINISTIC_THIRD_PARTY_CACHE"
                                                         if font_cache else side["sha256"])
                                      and (font_cache or bool(re.fullmatch(r"[0-9a-f]{64}", side["sha256"]))),
                                      "runtime_change_hash")
            exit_code, timed = row.get("exit_code"), row.get("timed_out")
            check(exit_code is None if timed else type(exit_code) is int, "runtime_exit_type")
            expected_exec = "ERROR" if timed else "PASS" if exit_code == 0 else "FAIL"
            check(row.get("runtime_execution_status") == expected_exec, "runtime_execution_match")
            if timed:
                expected_outcome = "TIMEOUT"
            elif exit_code == 0 and static["enforcement_class"] != "NO_EXECUTABLE_GATE":
                expected_outcome = "PASS_EXIT_GATE"
            elif exit_code == 0:
                expected_outcome = "MANUAL_OBSERVATION"
            elif "ModuleNotFoundError" in row["stderr"] or "ImportError" in row["stderr"]:
                expected_outcome = "DEPENDENCY_MISSING"
            elif static["enforcement_class"] != "NO_EXECUTABLE_GATE":
                expected_outcome = "FAIL_EXIT_GATE"
            else:
                expected_outcome = "EXPECTED_FAILURE"
            check(row.get("outcome") == expected_outcome, "runtime_outcome_match")
        check(seen == expected_pairs, "runtime_complete")
    return errors


def reseal(value: dict[str, Any]) -> None:
    value["semantic_sha256"] = semantic(value)


def loader_contract_controls() -> tuple[int, int]:
    pretty = b'{\n  "a": 1\n}\n'
    value, _, _ = strict_load(pretty, "historical_pretty_fixture", False)
    require(value == {"a": 1}, "E_HISTORICAL_PRETTY_REJECTED")
    pinned = sha(pretty)
    require(sha(pretty) == pinned and sha(pretty + b" ") != pinned,
            "E_HISTORICAL_RAW_PIN_FIXTURE")
    rejected_generated = False
    try:
        strict_load(pretty, "generated_noncanonical_fixture", True)
    except ValidationError as exc:
        rejected_generated = str(exc).startswith("E_JSON_CANONICAL")
    require(rejected_generated, "E_GENERATED_NONCANONICAL_FALSE_PASS")
    duplicate_rejected = False
    try:
        strict_load(b'{"a":1,"a":2}\n', "historical_duplicate_fixture", False)
    except ValidationError as exc:
        duplicate_rejected = str(exc).startswith("E_JSON_DUPLICATE")
    require(duplicate_rejected, "E_HISTORICAL_DUPLICATE_FALSE_PASS")
    nonfinite_rejected = False
    try:
        strict_load(b'{"a":NaN}\n', "historical_nonfinite_fixture", False)
    except ValidationError as exc:
        nonfinite_rejected = str(exc).startswith("E_JSON_NONFINITE")
    require(nonfinite_rejected, "E_HISTORICAL_NONFINITE_FALSE_PASS")
    require(typed_equal({"a": 1, "b": True}, {"b": True, "a": 1})
            and not typed_equal([1, 2], [2, 1]) and not typed_equal({"a": True}, {"a": 1}),
            "E_TYPED_OBJECT_ORDER_REGRESSION")
    attestation_raw = commit_bytes(ATTESTATION_PATH)
    attestation, _, _ = strict_load(attestation_raw, "attestation_loader_fixture", False)
    require(sha(attestation_raw) == ATTESTATION_RAW_SHA
            and attestation.get("semantic_sha256") == ATTESTATION_SEMANTIC_SHA
            and predecessor_semantic(attestation) == ATTESTATION_SEMANTIC_SHA,
            "E_ATTESTATION_LOADER_BINDING")
    forged_attestation = copy.deepcopy(attestation)
    forged_attestation["semantic_sha256"] = "0" * 64
    require(not (forged_attestation.get("semantic_sha256") == ATTESTATION_SEMANTIC_SHA
                 and predecessor_semantic(forged_attestation) == ATTESTATION_SEMANTIC_SHA),
            "E_ATTESTATION_MUTATION_FALSE_PASS")
    return 7, 7


def negative_controls(matrix: dict[str, Any], conformance: dict[str, Any],
                      manifest: dict[str, Any], inventory: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    def add(name: str, mutate: Any) -> None:
        m, c = copy.deepcopy(matrix), copy.deepcopy(conformance)
        mutate(m, c)
        require(not (typed_equal(m, matrix) and typed_equal(c, conformance)),
                "E_NEGATIVE_NOOP", name)
        reseal(m); c["matrix_semantic_sha256"] = m["semantic_sha256"]; reseal(c)
        cases.append((name, m, c))
    def mutate_first_claim_to_blank(_matrix: dict[str, Any], target: dict[str, Any]) -> None:
        row = next(item for item in target["guide_blob_records"][0]["line_records"]
                   if item["line_kind"] == "CLAIM")
        require(row["line_kind"] == "CLAIM", "E_NEGATIVE_PRECONDITION", "line_to_blank")
        row["line_kind"] = "BLANK"
    def mutate_runtime_transcript(target: dict[str, Any], _conformance: dict[str, Any]) -> None:
        row = target["runtime_records"][0]
        row["stdout"] = "FORGED OBSERVATION\n"
        row["stdout_sha256"] = sha(row["stdout"].encode("utf-8"))
    def mutate_filesystem_value(target: dict[str, Any], _conformance: dict[str, Any]) -> None:
        row = next(item for item in target["runtime_records"] if item["filesystem_changes"])
        change = row["filesystem_changes"][0]
        change["change"] = "MODIFIED" if change["change"] != "MODIFIED" else "CREATED"
    def mutate_filesystem_order(target: dict[str, Any], _conformance: dict[str, Any]) -> None:
        row = next(item for item in target["runtime_records"] if len(item["filesystem_changes"]) > 1)
        row["filesystem_changes"].reverse()
    add("release_drop", lambda m, c: m["occurrence_projection"]["test"].pop())
    add("release_order", lambda m, c: m["occurrence_projection"]["test"].reverse())
    add("path_crosswire", lambda m, c: m["occurrence_projection"]["demo"][0].__setitem__("path", "x.py"))
    add("blob_crosswire", lambda m, c: m["occurrence_projection"]["test"][0].__setitem__("blob_oid", "0" * 40))
    add("blob_ordinal_type", lambda m, c: m["occurrence_projection"]["test"][0].__setitem__("blob_ordinal", float(m["occurrence_projection"]["test"][0]["blob_ordinal"])))
    add("static_assertion", lambda m, c: m["python_blob_static_records"][0]["observation_counts"].__setitem__("assertions", 999))
    add("enforcement_promotion", lambda m, c: m["python_blob_static_records"][0].__setitem__("enforcement_class", "PASS"))
    add("source_anchor", lambda m, c: m["python_blob_static_records"][0]["call_name_set"].append("false.edge"))
    add("golden_flatten", lambda m, c: m["golden_blob_records"][1].__setitem__("value_projection_sha256", m["golden_blob_records"][0]["value_projection_sha256"]))
    add("golden_member_value", lambda m, c: m["golden_blob_records"][0]["members"][0].__setitem__("value_bytes_sha256", "f" * 64))
    add("golden_member_type", lambda m, c: m["golden_blob_records"][0]["members"][0].__setitem__("size", 1000.0))
    add("guide_manifest_index_base", lambda m, c: c["guide_occurrence_projection"][0].__setitem__(
        "manifest_entry_index", c["guide_occurrence_projection"][0]["manifest_entry_index"] + 1))
    add("guide_blob_extra", lambda m, c: c["guide_blob_records"][0].__setitem__("extra", 0))
    add("guide_line_extra", lambda m, c: c["guide_blob_records"][0]["line_records"][0].__setitem__("extra", 0))
    add("guide_lf_sha", lambda m, c: c["guide_blob_records"][0].__setitem__("lf_sha256", "0" * 64))
    add("guide_size", lambda m, c: c["guide_blob_records"][0].__setitem__("size_bytes", 0))
    add("guide_release_projection", lambda m, c: c["guide_blob_records"][0].__setitem__("release_projection", []))
    add("guide_line", lambda m, c: c["guide_blob_records"][0]["line_records"][0].__setitem__("text", "PASS"))
    add("guide_stale_promotion", lambda m, c: c["guide_blob_records"][0]["line_records"][1].__setitem__("disposition", "VERIFIED"))
    add("tool_crosswire", lambda m, c: c["tool_blob_records"][0].__setitem__("blob_oid", c["tool_blob_records"][1]["blob_oid"]))
    add("stdout_pass_promotion", lambda m, c: m["authority"].__setitem__("test_pass_global", True))
    add("demo_assertion_promotion", lambda m, c: m["authority"].__setitem__("demo_assertion_authority", True))
    add("science_promotion", lambda m, c: m["authority"].__setitem__("scientific_truth", True))
    add("material_promotion", lambda m, c: c["authority"].__setitem__("material_validity", True))
    add("canonical_promotion", lambda m, c: m["authority"].__setitem__("canonical_release", True))
    add("publication_promotion", lambda m, c: c["authority"].__setitem__("publication_ready", True))
    add("runtime_contract_network", lambda m, c: m["runtime_contract"].__setitem__("network_allowed", True))
    add("golden_contract_distinct", lambda m, c: m["golden_contract"].__setitem__(
        "two_blobs_must_remain_distinct", False))
    add("guide_contract_stale", lambda m, c: c["guide_contract"].__setitem__("stale_claims_preserved", False))
    add("tool_contract_optional_dependency", lambda m, c: c["tool_contract"].__setitem__(
        "optional_dependency_failure_is_not_pass", False))
    add("validation_drift", lambda m, c: m["validation"].__setitem__("ast_parse_failure", 1))
    add("nested_extra", lambda m, c: m["golden_blob_records"][0]["members"][0].__setitem__("extra", 0))
    add("top_extra", lambda m, c: m.__setitem__("extra", 0))
    add("runtime_exit", lambda m, c: m["runtime_records"][0].__setitem__("exit_code", 99))
    add("runtime_stdout", lambda m, c: m["runtime_records"][0].__setitem__("stdout", "PASS\n"))
    add("runtime_outcome", lambda m, c: m["runtime_records"][0].__setitem__("outcome", "GROUND_NOT_FOUND"))
    add("runtime_collection", lambda m, c: m["runtime_records"][0].__setitem__("runtime_collection_status", "COLLECTED"))
    add("runtime_skip", lambda m, c: m["runtime_records"][0].__setitem__("observed_skip", 1))
    add("runtime_extra", lambda m, c: m["runtime_records"][0].__setitem__("extra", False))
    add("runtime_argv", lambda m, c: m["runtime_records"][0]["argv_tail"].append("capture"))
    add("runtime_blob", lambda m, c: m["runtime_records"][0].__setitem__("blob_oid", "f" * 40))
    add("runtime_transcript_full_reseal", mutate_runtime_transcript)
    add("runtime_filesystem_value_full_reseal", mutate_filesystem_value)
    add("runtime_filesystem_order_full_reseal", mutate_filesystem_order)
    add("line_to_blank", mutate_first_claim_to_blank)
    add("claim_delete", lambda m, c: c["guide_blob_records"][0]["line_records"].pop())
    add("claim_duplicate", lambda m, c: c["guide_blob_records"][0]["line_records"].append(copy.deepcopy(c["guide_blob_records"][0]["line_records"][-1])))
    add("line_crosswire", lambda m, c: c["guide_blob_records"][0]["line_records"][0].__setitem__("line", 2))
    add("placeholder_owner", lambda m, c: m["inputs"]["persisted_chain"].__setitem__("step85_current_parent", "PENDING_AT_PRECOMMIT_BY_DESIGN"))
    add("parent", lambda m, c: m.__setitem__("expected_parent", "0" * 40))
    add("subject", lambda m, c: c.__setitem__("expected_subject", "wrong"))
    passed = 0
    for name, m, c in cases:
        if artifact_errors(m, c, manifest, inventory): passed += 1
        else: raise ValidationError(f"E_NEGATIVE_FALSE_PASS:{name}")
    # explicit Python JSON equality traps
    require(not typed_equal(True, 1) and not typed_equal(1, 1.0)
            and not typed_equal([1], [1.0]), "E_TYPED_EQUAL")
    return passed + 3, len(cases) + 3


def source_policy() -> None:
    for path, pin in ((BUILDER_PATH, BUILDER_SOURCE_POLICY_SHA256_LF),
                      (VALIDATOR_PATH, VALIDATOR_SOURCE_POLICY_SHA256_LF)):
        raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        text = raw.decode("utf-8")
        neutral = re.sub(rf'^{"BUILDER" if path == BUILDER_PATH else "VALIDATOR"}_SOURCE_POLICY_SHA256_LF = "[^"]+"$',
                         f'{"BUILDER" if path == BUILDER_PATH else "VALIDATOR"}_SOURCE_POLICY_SHA256_LF = "<SELF>"',
                         text, count=1, flags=re.MULTILINE)
        require(sha(neutral.encode()) == pin, "E_SOURCE_POLICY_PIN", path)
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                module = (node.module or "") if isinstance(node, ast.ImportFrom) else ""
                names = [x.name for x in node.names]
                require(not any(x.split(".")[0] in {"socket", "requests", "urllib", "http", "ftplib"}
                                for x in [module, *names]), "E_SOURCE_NETWORK", path)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                require(node.func.id not in {"eval", "exec", "compile", "__import__"},
                        "E_SOURCE_DYNAMIC", path)


def control_documents() -> None:
    for path, expected in CONTROL_SHA256.items():
        require(sha((ROOT / path).read_bytes()) == expected, "E_CONTROL_HASH", path)
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    parent = (ROOT / PARENT_LEDGER).read_text(encoding="utf-8")
    canonical_doc = (ROOT / CANONICAL_LEDGER).read_text(encoding="utf-8")
    handover = (ROOT / HANDOVER).read_text(encoding="utf-8")
    for label, text in (("result", result), ("parent", parent), ("canonical", canonical_doc), ("handover", handover)):
        require(GATE in text and SUBJECT in text and PERSISTENCE in text, "E_CONTROL_TOKENS", label)
        require("Step 87" in text and "blocked" in text.lower(), "E_STEP87_BLOCKED", label)
    require(canonical_doc.count("| 067 |") == 1, "E_CANONICAL_ROW")
    require(f"현재 result: `{RESULT_PATH}`" in handover, "E_HANDOVER_RESULT")
    require(f"현재 machine evidence: `{MATRIX_PATH}` + `{CONFORMANCE_PATH}`" in handover,
            "E_HANDOVER_MACHINE")


def step85_persisted_paragraph_errors(text: str) -> list[str]:
    start_marker = "Step 85 losslessly binds"
    end_marker = "Step 86 fixes"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        return ["E_STEP85_PARAGRAPH_BOUNDARY"]
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    paragraph = " ".join(text[start:end].split())
    required = (
        "PASS_P067_STEP85_STATE_DEFAULT_IMPORT",
        "3f2c7635aa545bd617b6cd83b5e718683d5b2b1c",
        "f00bf2fa8f25c85f0c62cb901912763d98c8f070",
        "audit(phase067): separate defaults state persistence",
        "pushed/live/clean",
        "Python 3.12/3.14 both returned `PASS_P067_STEP85_PERSISTENCE`",
    )
    forbidden = (
        "PASS_PENDING_PERSISTENCE",
        "expected parent",
        "containing commit",
        "PENDING_AT_PRECOMMIT_BY_DESIGN",
    )
    errors = [f"E_STEP85_PERSISTED_REQUIRED:{token}" for token in required if token not in paragraph]
    errors.extend(f"E_STEP85_PERSISTED_STALE:{token}" for token in forbidden if token in paragraph)
    return errors


def step85_persisted_paragraph_controls() -> tuple[int, int]:
    parent = (ROOT / PARENT_LEDGER).read_text(encoding="utf-8")
    errors = step85_persisted_paragraph_errors(parent)
    require(not errors, "E_STEP85_PERSISTED_PARAGRAPH", repr(errors))
    start = parent.index("Step 85 losslessly binds")
    end = parent.index("Step 86 fixes", start)
    good = parent[start:end]
    stale = good.replace(
        "is persisted under",
        "is `PASS_PENDING_PERSISTENCE` under expected parent",
        1,
    )
    require(stale != good, "E_STEP85_PERSISTED_CONTROL_NOOP")
    require(step85_persisted_paragraph_errors(stale), "E_STEP85_PERSISTED_CONTROL_FALSE_PASS")
    require(not step85_persisted_paragraph_errors(parent), "E_STEP85_PERSISTED_CONTROL_GOOD_FAIL")
    return 2, 2


def parse_porcelain(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4 and line[2] == " ", "E_STATUS_LINE")
        status, path = line[:2], line[3:].replace("\\", "/")
        require(" -> " not in path and path not in out, "E_STATUS_RENAME")
        out[path] = status
    return out


def parse_name_status(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        status, path = line.split("\t", 1)
        require(status in {"A", "M"} and path not in out, "E_NAME_STATUS")
        out[path] = status
    return out


def git_argv_controls() -> tuple[int, int]:
    prefix = ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r")
    child = EXPECTED_PARENT
    accepted = (*prefix, f"{child}^", child, "--")
    require(git_argv_allowed(accepted), "E_GIT_ARGV_POSITIVE_UNREACHABLE")
    rejected = {
        "empty_separator": (*prefix, f"{child}^", child, ""),
        "malformed_parent": (*prefix, f"{'g' * 40}^", child, "--"),
        "missing_caret": (*prefix, child, child, "--"),
        "uppercase_parent": (*prefix, f"{child.upper()}^", child, "--"),
        "nonhex_child": (*prefix, f"{child}^", "z" * 40, "--"),
        "swapped_order": (*prefix, child, f"{child}^", "--"),
        "nonempty_path": (*prefix, f"{child}^", child, "Claude"),
        "option_injection": (*prefix, f"{child}^", child, "--output=x"),
        "extra_argument": (*prefix, f"{child}^", child, "--", "extra"),
    }
    for name, argv in rejected.items():
        require(not git_argv_allowed(argv), "E_GIT_ARGV_CONTROL_FALSE_PASS", name)
    observed = parse_name_status(gtext(accepted))
    expected = {
        "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": "M",
        "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md": "M",
        "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md": "M",
        "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json": "A",
        "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json": "A",
        "Codex/results/PHASE_067_STEP_085_STATE_DEFAULT_IMPORT_RESULT.md": "A",
        "Codex/work/v1025_phase067/build_phase067_step85.py": "A",
        "Codex/work/v1025_phase067/validate_phase067_step85.py": "A",
    }
    require(observed == expected, "E_GIT_ARGV_PERSISTED_FIXTURE")
    return 10, 10


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    return text.removesuffix(".git").strip("/")


def live(ref: str) -> str:
    text = gtext(("ls-remote", "--heads", "origin", ref))
    require("\t" in text, "E_LIVE_REF", ref)
    return text.split("\t", 1)[0]


def repository_refs(tip: str) -> dict[str, str]:
    record = {"branch": gtext(("rev-parse", "--abbrev-ref", "HEAD")),
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
                "origin": "github.com/lksz1412/project_anode_fit",
                "protected_local": PROTECTED_TIP, "protected_tracking": PROTECTED_TIP,
                "protected_live": PROTECTED_TIP, "main_local": "",
                "main_tracking": MAIN_TIP, "main_live": MAIN_TIP}
    require(record == expected, "E_REPOSITORY_REFS", repr(record))
    return record


def status() -> dict[str, str]:
    return parse_porcelain(gtext(("status", "--porcelain=v1", "--untracked-files=all")))


def index_snapshot() -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for line in gtext(("ls-files", "-s")).splitlines():
        meta, path = line.split("\t", 1)
        if path in FINAL_SET:
            mode, oid, stage = meta.split()
            require(stage == "0", "E_INDEX_STAGE")
            out[path] = (mode, oid)
    return out


def seal(tip: str) -> dict[str, Any]:
    return {"refs": repository_refs(tip), "status": status(), "index": index_snapshot(),
            "path_hashes": {p: sha((ROOT / p).read_bytes()) for p in FINAL_PATHS if (ROOT / p).exists()},
            "input_hashes": {p: sha(commit_bytes(p)) for p in (MANIFEST_PATH, INVENTORY_PATH, ATTESTATION_PATH)}}


def verify_content() -> None:
    expected = {p: ("??" if FINAL_STATUS[p] == "A" else " M") for p in FINAL_PATHS}
    require(status() == expected, "E_CONTENT_PATHS", repr(status()))
    require(not set(index_snapshot()).intersection(FINAL_SET - {PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER}),
            "E_CONTENT_STAGED_ADD")


def verify_staged() -> None:
    require(gtext(("rev-parse", "HEAD")) == EXPECTED_PARENT, "E_STAGED_PARENT")
    require(parse_name_status(gtext(("diff", "--cached", "--name-status", "--no-renames", "HEAD")))
            == FINAL_STATUS, "E_STAGED_PATHS")
    require(gtext(("diff", "--name-only")) == "" and
            gtext(("ls-files", "--others", "--exclude-standard")) == "", "E_STAGED_DIRTY")
    require(gtext(("diff", "--cached", "--check")) == "", "E_DIFF_CHECK")
    idx = index_snapshot()
    require(set(idx) == FINAL_SET and all(mode == "100644" for mode, _ in idx.values()), "E_INDEX_MODES")
    for path, (_, oid) in idx.items():
        raw = (ROOT / path).read_bytes()
        require(git(("show", f":{path}")) == raw and blob(oid) == raw, "E_INDEX_BYTES", path)


def verify_persistence(commit: str) -> None:
    parents = gtext(("show", "-s", "--format=%P", commit)).split()
    require(parents == [EXPECTED_PARENT], "E_COMMIT_PARENTS", repr(parents))
    require(gtext(("rev-parse", f"{commit}^")) == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(gtext(("show", "-s", "--format=%s", commit)) == SUBJECT, "E_COMMIT_SUBJECT")
    changed = parse_name_status(gtext(("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r", f"{commit}^", commit, "--")))
    require(changed == FINAL_STATUS, "E_COMMIT_PATHS")
    require(gtext(("status", "--porcelain")) == "", "E_WORKTREE_DIRTY")
    require(gtext(("diff", "--name-only", PROTECTED_TIP, "--", "Claude")) == "", "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        require(git(("show", f"{commit}:{path}")) == (ROOT / path).read_bytes(), "E_COMMITTED_BYTES", path)


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require((args.verify_persistence and args.expected_commit is not None) or
            (not args.verify_persistence and args.expected_commit is None), "E_EXPECTED_COMMIT_MODE")
    if args.verify_persistence:
        require(bool(re.fullmatch(r"[0-9a-f]{40}", args.expected_commit or "")), "E_EXPECTED_COMMIT")
    tip = args.expected_commit if args.verify_persistence else EXPECTED_PARENT
    entry = seal(tip or "")
    source_policy(); control_documents()
    manifest, inventory = input_documents()
    matrix, n1, d1 = strict_load((ROOT / MATRIX_PATH).read_bytes(), MATRIX_PATH)
    conformance, n2, d2 = strict_load((ROOT / CONFORMANCE_PATH).read_bytes(), CONFORMANCE_PATH)
    errors = artifact_errors(matrix, conformance, manifest, inventory)
    require(not errors, "E_ARTIFACT", ",".join(errors[:8]))
    negatives = negative_controls(matrix, conformance, manifest, inventory)
    loader_controls = loader_contract_controls()
    argv_controls = git_argv_controls()
    document_controls = step85_persisted_paragraph_controls()
    if args.content_only: verify_content()
    elif args.verify_staged: verify_staged()
    else: verify_persistence(args.expected_commit or "")
    terminal = seal(tip or "")
    require(entry == terminal, "E_TRANSACTION_SEAL")
    print(f"PASS_P067_STEP86_CONTROLS semantic={negatives[0]}/{negatives[1]} "
          f"json={loader_controls[0]}/{loader_controls[1]} "
          f"git_argv={argv_controls[0]}/{argv_controls[1]} "
          f"documents={document_controls[0]}/{document_controls[1]} "
          f"nodes={n1+n2} depth={max(d1,d2)}")
    print(f"{PERSISTENCE if args.verify_persistence else GATE} test=44/29 demo=30/26 "
          f"golden=8/2 result=35/14 guide=20/8 determinism=2/2")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(str(exc))
        raise SystemExit(1)
