#!/usr/bin/env python3
"""Build Phase 067 Step 86 test/demo/golden/guide/tool evidence.

All historical inputs are read from frozen Git objects.  Executable scripts are
materialized only below repository-external temporary roots and are launched in
isolated child interpreters.  This controller never imports production code.
"""

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
import shutil
import struct
import subprocess
import tempfile
import zipfile
from io import BytesIO
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "3f2c7635aa545bd617b6cd83b5e718683d5b2b1c"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase067): adjudicate test demo golden behavior"
GATE = "PASS_P067_STEP86_TEST_DEMO_GOLDEN"
PERSISTENCE = "PASS_P067_STEP86_PERSISTENCE"
DATE = "2026-09-02"
BUILDER_SOURCE_POLICY_SHA256_LF = "031c31aa142f59950074794337d9dcfbb840f984c3e4f2504ae564e2fad89c08"

MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
MANIFEST_RAW_SHA = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
INVENTORY_RAW_SHA = "b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63"
INVENTORY_SEMANTIC_SHA = "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"
ATTESTATION_RAW_SHA = "112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174"
ATTESTATION_SEMANTIC_SHA = "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"

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
CONTROL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, RESULT_PATH, PARENT_LEDGER,
                 CANONICAL_LEDGER, HANDOVER)
PYTHON_LAUNCHERS = (("3.12", ("py", "-3.12")), ("3.14", ("py", "-3.14")))
EXPECTED = {
    "test_occurrences": 44, "test_blobs": 29, "test_lines": 6042,
    "demo_occurrences": 30, "demo_blobs": 26, "demo_lines": 3300,
    "result_occurrences": 35, "result_blobs": 14, "result_lines": 2081,
    "golden_occurrences": 8, "golden_blobs": 2,
    "guide_occurrences": 20, "guide_blobs": 8, "guide_lines": 854,
}


class BuildError(RuntimeError):
    pass


def require(ok: bool, diagnostic: str) -> None:
    if not ok:
        raise BuildError(diagnostic)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    clone = copy.deepcopy(value)
    clone.pop("semantic_sha256", None)
    return sha(canonical(clone))


def finish(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic(value)
    return value


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"E_JSON_BOM:{label}")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, f"E_JSON_DUPLICATE:{label}:{key}")
            out[key] = value
        return out
    def bad_constant(token: str) -> None:
        raise BuildError(f"E_JSON_NONFINITE:{label}:{token}")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                       parse_constant=bad_constant)
    require(isinstance(value, dict), f"E_JSON_TOP:{label}")
    return value


def git_show(revision: str, path: str) -> bytes:
    require(revision in {EXPECTED_PARENT, BASELINE}, "E_GIT_REV")
    allowed = {MANIFEST_PATH, INVENTORY_PATH, ATTESTATION_PATH, *CONTROL_PATHS}
    require(path in allowed or path.startswith("Claude/docs/"), f"E_GIT_PATH:{path}")
    proc = subprocess.run(("git", "show", f"{revision}:{path}"), cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(proc.returncode == 0, f"E_GIT_SHOW:{revision}:{path}:{proc.returncode}")
    return proc.stdout


def blob_bytes(oid: str) -> bytes:
    require(bool(re.fullmatch(r"[0-9a-f]{40}", oid)), f"E_BLOB_OID:{oid}")
    proc = subprocess.run(("git", "cat-file", "blob", oid), cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(proc.returncode == 0, f"E_BLOB_READ:{oid}")
    return proc.stdout


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest_raw = git_show(EXPECTED_PARENT, MANIFEST_PATH)
    inventory_raw = git_show(EXPECTED_PARENT, INVENTORY_PATH)
    attestation_raw = git_show(EXPECTED_PARENT, ATTESTATION_PATH)
    require(sha(manifest_raw) == MANIFEST_RAW_SHA, "E_MANIFEST_PIN")
    require(sha(inventory_raw) == INVENTORY_RAW_SHA, "E_INVENTORY_PIN")
    require(sha(attestation_raw) == ATTESTATION_RAW_SHA, "E_ATTESTATION_PIN")
    manifest = strict_json(manifest_raw, "manifest")
    inventory = strict_json(inventory_raw, "inventory")
    attestation = strict_json(attestation_raw, "attestation")
    require(inventory["semantic_sha256"] == INVENTORY_SEMANTIC_SHA, "E_INVENTORY_SEMANTIC")
    require(attestation["semantic_sha256"] == ATTESTATION_SEMANTIC_SHA, "E_ATTESTATION_SEMANTIC")
    return manifest, inventory, attestation


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


def node_anchor(node: ast.AST, source: str) -> dict[str, Any]:
    segment = ast.get_source_segment(source, node) or ""
    return {
        "ast_kind": type(node).__name__,
        "start_line": int(getattr(node, "lineno", 0)),
        "end_line": int(getattr(node, "end_lineno", getattr(node, "lineno", 0))),
        "source_sha256_lf": sha(segment.replace("\r\n", "\n").encode("utf-8")),
        "normalized_ast_sha256": sha(canonical(stable_ast(node))),
    }


def call_name(node: ast.Call) -> str:
    parts: list[str] = []
    cur: ast.AST = node.func
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    return ".".join(reversed(parts))


def python_static(blob_oid: str, role: str) -> dict[str, Any]:
    raw = blob_bytes(blob_oid)
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    calls: list[dict[str, Any]] = []
    assertions: list[dict[str, Any]] = []
    exits: list[dict[str, Any]] = []
    file_surfaces: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
        if isinstance(node, ast.Assert):
            assertions.append({"anchor": node_anchor(node, source),
                               "expression": ast.unparse(node.test),
                               "message": None if node.msg is None else ast.unparse(node.msg)})
        if isinstance(node, ast.Call):
            name = call_name(node)
            record = {"name": name, "anchor": node_anchor(node, source),
                      "literal_args": [x.value for x in node.args if isinstance(x, ast.Constant)
                                       and isinstance(x.value, (str, int, float, bool, type(None)))]}
            calls.append(record)
            if name in {"sys.exit", "exit"}:
                exits.append(record)
            if name.split(".")[-1] in {"open", "load", "save", "savez", "savez_compressed",
                                       "write_text", "write_bytes", "unlink", "remove", "replace",
                                       "rename", "mkdir", "makedirs", "rmtree", "savefig"}:
                file_surfaces.append(record)
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)):
            if any(isinstance(x, (ast.Attribute, ast.Subscript)) for x in ast.walk(node)):
                mutations.append({"anchor": node_anchor(node, source), "statement": ast.unparse(node)})
    names = [x["name"] for x in calls]
    observation = {
        "print_calls": sum(x.split(".")[-1] == "print" for x in names),
        "plot_calls": sum(x.split(".")[-1] in {"plot", "show", "savefig", "figure", "subplots"} for x in names),
        "finite_checks": sum(x.split(".")[-1] in {"isfinite", "isnan", "allclose", "array_equal"} for x in names),
        "assertions": len(assertions),
        "exit_calls": len(exits),
    }
    if role == "test":
        enforcement = ("ASSERT_AND_EXIT" if assertions and exits else
                       "EXIT_ONLY" if exits else "NO_EXECUTABLE_GATE")
    elif role == "demo":
        enforcement = "EXIT_ONLY" if exits else "NO_EXECUTABLE_GATE"
    else:
        enforcement = ("ASSERT_ONLY" if assertions and not exits else
                       "ASSERT_AND_EXIT" if assertions and exits else
                       "EXIT_ONLY" if exits else "NO_EXECUTABLE_GATE")
    return {
        "blob_oid": blob_oid, "raw_sha256": sha(raw),
        "lf_sha256": sha(raw.replace(b"\r\n", b"\n")),
        "size_bytes": len(raw), "physical_lines": len(source.splitlines()),
        "encoding": "utf-8", "ast_parse": "PASS", "role": role,
        "imports": sorted(imports), "assertions": assertions,
        "exit_calls": exits, "file_surfaces": file_surfaces,
        "mutation_surfaces": mutations, "observation_counts": observation,
        "enforcement_class": enforcement,
        "call_name_set": sorted(set(names)),
    }


def parse_npy(raw: bytes) -> dict[str, Any]:
    require(raw.startswith(b"\x93NUMPY"), "E_NPY_MAGIC")
    major, minor = raw[6], raw[7]
    require((major, minor) in {(1, 0), (2, 0), (3, 0)}, "E_NPY_VERSION")
    if major == 1:
        header_len = struct.unpack("<H", raw[8:10])[0]
        pos = 10
    else:
        header_len = struct.unpack("<I", raw[8:12])[0]
        pos = 12
    header_raw = raw[pos:pos + header_len]
    header = ast.literal_eval(header_raw.decode("latin1").strip())
    require(set(header) == {"descr", "fortran_order", "shape"}, "E_NPY_HEADER")
    require(header["descr"] == "<f8" and header["fortran_order"] is False,
            "E_NPY_LAYOUT")
    shape = list(header["shape"])
    require(shape == [1000], "E_NPY_SHAPE")
    data = raw[pos + header_len:]
    require(len(data) == 8000, "E_NPY_DATA_SIZE")
    values = struct.unpack("<1000d", data)
    require(all(math.isfinite(x) for x in values), "E_NPY_NONFINITE")
    return {"dtype": "float64", "shape": shape, "size": 1000,
            "finite_count": 1000, "finite_min": min(values), "finite_max": max(values),
            "member_sha256": sha(raw), "value_bytes_sha256": sha(data),
            "npy_header_sha256": sha(header_raw)}


def golden_record(entry: dict[str, Any]) -> dict[str, Any]:
    raw = blob_bytes(entry["blob_sha"])
    members: list[dict[str, Any]] = []
    with zipfile.ZipFile(BytesIO(raw), "r") as archive:
        for info in archive.infolist():
            require(info.filename.endswith(".npy"), "E_GOLD_MEMBER_NAME")
            payload = archive.read(info.filename)
            members.append({"key": info.filename[:-4], "zip_member": info.filename,
                            "crc32": info.CRC, "compress_type": info.compress_type,
                            "compressed_size": info.compress_size,
                            "uncompressed_size": info.file_size, **parse_npy(payload)})
    require(len(members) == 13 and len({x["key"] for x in members}) == 13,
            "E_GOLD_MEMBER_COUNT")
    return {"blob_oid": entry["blob_sha"], "raw_sha256": sha(raw),
            "size_bytes": len(raw), "member_count": 13,
            "member_order": [x["key"] for x in members], "members": members,
            "value_projection_sha256": sha(canonical([
                {"key": x["key"], "value_bytes_sha256": x["value_bytes_sha256"]} for x in members]))}


def occurrence_rows(inventory: dict[str, Any], role: str) -> list[dict[str, Any]]:
    rows = [copy.deepcopy(x) for x in inventory["occurrence_records"] if x["role"] == role]
    return rows


def release_assets(manifest: dict[str, Any], inventory: dict[str, Any]) -> dict[str, bytes]:
    wanted = {x["path"]: x["blob_oid"] for x in inventory["occurrence_records"]}
    for entry in manifest["entries"]:
        if entry["path"].endswith("/golden_graphite_ref.npz"):
            wanted[entry["path"]] = entry["blob_sha"]
    return {path: blob_bytes(oid) for path, oid in sorted(wanted.items())}


def normalized_output(raw: bytes, temp_root: Path) -> str:
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    variants = {str(temp_root), str(temp_root).replace("\\", "/"),
                str(temp_root).replace("\\", "\\\\")}
    for item in sorted(variants, key=len, reverse=True):
        text = text.replace(item, "<DISPOSABLE_ROOT>")
    return text


def assert_output_normalization_regression() -> None:
    fixture = Path(r"C:\Temp\p067_s86_fixture")
    raw = ("FileNotFoundError: 'C:\\\\Temp\\\\p067_s86_fixture\\\\_sections'\n").encode()
    normalized = normalized_output(raw, fixture)
    require(normalized == "FileNotFoundError: '<DISPOSABLE_ROOT>\\\\_sections'\n",
            "E_ESCAPED_TEMP_NORMALIZATION_REGRESSION")
    control = b"FileNotFoundError: 'C:\\\\external\\\\_sections'\n"
    require(normalized_output(control, fixture) == control.decode(),
            "E_NONTEMP_OUTPUT_NORMALIZATION_REGRESSION")


def file_manifest(root: Path) -> dict[str, tuple[int, str]]:
    out: dict[str, tuple[int, str]] = {}
    for path in sorted(x for x in root.rglob("*") if x.is_file()):
        rel = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        out[rel] = (len(raw), sha(raw))
    return out


def normalized_change(path: str, kind: str, before: tuple[int, str] | None,
                      after: tuple[int, str] | None) -> dict[str, Any]:
    ephemeral_font_cache = bool(re.fullmatch(r"home/\.matplotlib/fontlist-v[0-9]+\.json", path))
    def side(value: tuple[int, str] | None) -> dict[str, Any] | None:
        if value is None:
            return None
        return {"size": value[0],
                "sha256": ("WITHHELD_NONDETERMINISTIC_THIRD_PARTY_CACHE"
                           if ephemeral_font_cache else value[1])}
    return {"path": path, "change": kind, "before": side(before), "after": side(after),
            "content_hash_class": ("NONDETERMINISTIC_THIRD_PARTY_CACHE"
                                   if ephemeral_font_cache else "EXACT"),
            "content_hash_authority": not ephemeral_font_cache}


def assert_change_normalization_regression() -> None:
    a = normalized_change("home/.matplotlib/fontlist-v390.json", "ADDED", None, (84056, "a" * 64))
    b = normalized_change("home/.matplotlib/fontlist-v390.json", "ADDED", None, (84056, "b" * 64))
    require(a == b and a["after"]["sha256"] == "WITHHELD_NONDETERMINISTIC_THIRD_PARTY_CACHE"
            and a["after"]["size"] == 84056 and a["content_hash_authority"] is False,
            "E_FONT_CACHE_NORMALIZATION_REGRESSION")
    c = normalized_change("output.png", "ADDED", None, (10, "a" * 64))
    d = normalized_change("output.png", "ADDED", None, (10, "b" * 64))
    require(c != d and c["after"]["sha256"] == "a" * 64,
            "E_NONCACHE_HASH_AUTHORITY_REGRESSION")


def runtime_one(label: str, launcher: tuple[str, ...], row: dict[str, Any],
                assets: dict[str, bytes], static: dict[str, Any],
                timeout_seconds: int = 50) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="p067_s86_") as td:
        root = Path(td).resolve()
        require(ROOT.resolve() not in root.parents and root != ROOT.resolve(), "E_TEMP_INSIDE_REPO")
        for rel, raw in assets.items():
            dest = root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
        before = file_manifest(root)
        target = root / row["path"]
        env = os.environ.copy()
        env.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1",
                    "PYTHONDONTWRITEBYTECODE": "1", "MPLBACKEND": "Agg",
                    "ANODEFIT_TMP": str(root / "runtime_tmp"), "HOME": str(root / "home"),
                    "USERPROFILE": str(root / "home"), "TMP": str(root / "tmp"),
                    "TEMP": str(root / "tmp")})
        (root / "runtime_tmp").mkdir()
        (root / "home").mkdir()
        (root / "tmp").mkdir()
        script_args = ["verify"] if "regression" in target.name else []
        argv = (*launcher, "-B", "-I", "-X", "utf8", target.name, *script_args)
        try:
            proc = subprocess.run(argv, cwd=target.parent, env=env, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, check=False, timeout=timeout_seconds)
            timed_out = False
            exit_code: int | None = proc.returncode
            stdout = normalized_output(proc.stdout, root)
            stderr = normalized_output(proc.stderr, root)
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            exit_code = None
            stdout = normalized_output(exc.stdout or b"", root)
            stderr = normalized_output(exc.stderr or b"", root)
        after = file_manifest(root)
        all_paths = sorted(set(before) | set(after))
        changes = []
        for path in all_paths:
            if before.get(path) != after.get(path):
                kind = "ADDED" if path not in before else "DELETED" if path not in after else "MODIFIED"
                changes.append(normalized_change(path, kind, before.get(path), after.get(path)))
        if timed_out:
            outcome = "TIMEOUT"
        elif exit_code == 0 and static["enforcement_class"] != "NO_EXECUTABLE_GATE":
            outcome = "PASS_EXIT_GATE"
        elif exit_code == 0:
            outcome = "MANUAL_OBSERVATION"
        elif "ModuleNotFoundError" in stderr or "ImportError" in stderr:
            outcome = "DEPENDENCY_MISSING"
        elif static["enforcement_class"] != "NO_EXECUTABLE_GATE":
            outcome = "FAIL_EXIT_GATE"
        else:
            outcome = "EXPECTED_FAILURE"
        return {"runtime": label, "launcher": list(launcher),
                "argv_tail": ["-B", "-I", "-X", "utf8", target.name, *script_args],
                "blob_oid": row["blob_oid"], "representative_path": row["path"],
                "representative_release": row["release"], "exit_code": exit_code,
                "timed_out": timed_out, "stdout": stdout, "stderr": stderr,
                "stdout_sha256": sha(stdout.encode("utf-8")),
                "stderr_sha256": sha(stderr.encode("utf-8")), "filesystem_changes": changes,
                "inventory_present": True, "framework_kind": "TOP_LEVEL_SCRIPT",
                "runtime_collection_status": "NOT_COLLECTABLE",
                "runtime_execution_status": ("ERROR" if timed_out else "PASS" if exit_code == 0 else "FAIL"),
                "static_skip_predicates": [x for x in static["call_name_set"]
                                           if x.split(".")[-1] in {"skip", "skipif", "xfail"}],
                "observed_skip": bool(re.search(r"(?im)^\s*(?:skip|skipped)\b", stdout + "\n" + stderr)),
                "outcome": outcome, "enforcement_class": static["enforcement_class"],
                "assertion_count": static["observation_counts"]["assertions"],
                "exit_call_count": static["observation_counts"]["exit_calls"],
                "authority": "ISOLATED_REPRESENTATIVE_OCCURRENCE_ONLY"}


def runtime_records(inventory: dict[str, Any], manifest: dict[str, Any], execute: bool) -> list[dict[str, Any]]:
    rows = occurrence_rows(inventory, "test") + occurrence_rows(inventory, "demo")
    representative: dict[str, dict[str, Any]] = {}
    for row in rows:
        representative.setdefault(row["blob_oid"], row)
    if not execute:
        return []
    assets = release_assets(manifest, inventory)
    records: list[dict[str, Any]] = []
    for oid in sorted(representative):
        row = representative[oid]
        for label, launcher in PYTHON_LAUNCHERS:
            records.append(runtime_one(label, launcher, row, assets,
                                       python_static(oid, "test" if row["role"] == "test" else "demo")))
    return records


def guide_records(manifest: dict[str, Any], static_by_blob: dict[str, dict[str, Any]],
                  runtime: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entries = [x for x in manifest["entries"]
               if x["path"].endswith("/FITTING_GUIDE.md")
               and x["role"] == "implementation_guide" and x["extension"] == "md"
               and x["review_mode"] == "FULL_TEXT"]
    occurrences = [{"ordinal": i, "manifest_entry_index": manifest["entries"].index(x),
                    "release": x["version"], "path": x["path"],
                    "blob_oid": x["blob_sha"], "git_mode": x["git_mode"],
                    "size_bytes": x["size_bytes"], "physical_lines": x["extent"]["lines"]}
                   for i, x in enumerate(entries, 1)]
    by_blob: dict[str, list[dict[str, Any]]] = {}
    for row in occurrences:
        by_blob.setdefault(row["blob_oid"], []).append(row)
    known_names = sorted({Path(x["representative_path"]).name for x in runtime})
    runtime_zero = {Path(x["representative_path"]).name for x in runtime
                    if x["exit_code"] == 0 and not x["timed_out"]}
    records = []
    for oid in sorted(by_blob):
        raw = blob_bytes(oid)
        text = raw.decode("utf-8")
        lines = text.splitlines()
        line_records = []
        for number, line in enumerate(lines, 1):
            stripped = line.strip()
            mentions = [name for name in known_names if name in line]
            if stripped == "":
                line_kind = "BLANK"
            elif stripped.startswith("#"):
                line_kind = "HEADING"
            elif stripped.startswith("```"):
                line_kind = "FENCE"
            elif re.fullmatch(r"\|?(?:\s*:?-+:?\s*\|)+", stripped):
                line_kind = "TABLE_RULE"
            elif stripped.startswith("|"):
                line_kind = "TABLE_HEADER" if number == 1 or (number < len(lines) and re.fullmatch(r"\|?(?:\s*:?-+:?\s*\|)+", lines[number].strip())) else "CLAIM"
            elif stripped.startswith("<!--"):
                line_kind = "COMMENT"
            elif stripped.startswith((">", "-", "*", "+")) or re.match(r"^\d+[.)]\s", stripped):
                line_kind = "CLAIM"
            elif stripped.startswith(("$", "python ", "py ", "pytest ")):
                line_kind = "CODE_OR_COMMAND"
            else:
                line_kind = "CLAIM"
            claim_like = line_kind == "CLAIM"
            assertion_bound = [x for x in mentions if x in runtime_zero]
            if not claim_like:
                disposition = "STRUCTURAL_OR_BLANK"
            elif assertion_bound:
                disposition = "RUNTIME_EXIT_ZERO_REFERENCE_NOT_PROPOSITION_PROOF"
            elif mentions:
                disposition = "SOURCE_NAME_BOUND_SELF_REPORT"
            else:
                disposition = "SELF_REPORT_UNBOUND_OR_STALE"
            line_records.append({"line": number, "raw_sha256": sha(line.encode("utf-8")),
                                 "text": line, "mentioned_script_names": mentions,
                                 "line_kind": line_kind, "claim_like": claim_like,
                                 "disposition": disposition})
        titles = [x["text"].lstrip("#").strip() for x in line_records if x["line_kind"] == "HEADING"]
        records.append({"blob_oid": oid, "raw_sha256": sha(raw), "lf_sha256": sha(raw.replace(b"\r\n", b"\n")),
                        "size_bytes": len(raw), "physical_lines": len(lines),
                        "occurrence_paths": [x["path"] for x in by_blob[oid]],
                        "release_projection": [x["release"] for x in by_blob[oid]],
                        "title_spelling": titles[0] if titles else "GROUND_NOT_FOUND",
                        "coverage": {"first_line": 1, "last_line": len(lines),
                                     "covered_lines": len(line_records), "gaps": 0, "overlaps": 0},
                        "line_records": line_records})
    return occurrences, records


def common_header(artifact: str) -> dict[str, Any]:
    return {"schema_version": "P067-S86-1", "artifact": artifact, "phase": 67, "step": 86,
            "generated_date": DATE, "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
            "branch": BRANCH, "expected_subject": SUBJECT, "gate": GATE,
            "precommit_status": "PASS_PENDING_PERSISTENCE",
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "persistence_terminal": PERSISTENCE, "result_first": True, "json_outputs_last": True}


def enforcement_summary(rows: list[dict[str, Any]], static_by_blob: dict[str, dict[str, Any]]) -> dict[str, Any]:
    blob_counts: dict[str, int] = {}
    occurrence_counts: dict[str, int] = {}
    for oid in sorted({x["blob_oid"] for x in rows}):
        key = static_by_blob[oid]["enforcement_class"]
        blob_counts[key] = blob_counts.get(key, 0) + 1
    for row in rows:
        key = static_by_blob[row["blob_oid"]]["enforcement_class"]
        occurrence_counts[key] = occurrence_counts.get(key, 0) + 1
    return {"unique_blob_counts": dict(sorted(blob_counts.items())),
            "occurrence_counts": dict(sorted(occurrence_counts.items()))}


def golden_route_records(test_rows: list[dict[str, Any]],
                         static_by_blob: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for row in test_rows:
        names = static_by_blob[row["blob_oid"]]["call_name_set"]
        if not any(x.split(".")[-1] in {"load", "savez", "savez_compressed"} for x in names):
            continue
        release = row["release"]
        if release in {"v1.0.13", "v1.0.14", "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2"}:
            capture = "EXPLICIT_CAPTURE_OVERWRITES_DISPOSABLE_EXISTING_GOLDEN"
        elif release == "v1.0.19":
            capture = "EXPLICIT_CAPTURE_REFUSES_EXISTING_EXIT_3"
        elif release in {"v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23", "v1.0.24", "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2"}:
            capture = "AUXILIARY_V1_0_19_GOLDEN_LOAD_ONLY_NO_CURRENT_RELEASE_GOLDEN_PROVENANCE"
        else:
            capture = "UNRELATED_OR_EXTERNAL_GOLDEN_ROUTE"
        records.append({"release": release, "path": row["path"], "blob_oid": row["blob_oid"],
                        "capture_overwrite_class": capture,
                        "source_static_only": True, "repository_golden_mutated": False})
    return records


def build(execute_runtime: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    assert_change_normalization_regression()
    assert_output_normalization_regression()
    manifest, inventory, attestation = load_inputs()
    roles = {r: occurrence_rows(inventory, r) for r in ("test", "demo", "result")}
    for role, occ_key, blob_key, line_key in (
        ("test", "test_occurrences", "test_blobs", "test_lines"),
        ("demo", "demo_occurrences", "demo_blobs", "demo_lines"),
        ("result", "result_occurrences", "result_blobs", "result_lines")):
        rows = roles[role]
        oids = sorted({x["blob_oid"] for x in rows})
        line_total = sum(next(x["physical_lines"] for x in inventory["blob_records"] if x["blob_oid"] == oid) for oid in oids)
        require((len(rows), len(oids), line_total) == (EXPECTED[occ_key], EXPECTED[blob_key], EXPECTED[line_key]),
                f"E_ROLE_DENOMINATOR:{role}")
    static_by_blob: dict[str, dict[str, Any]] = {}
    for role in ("test", "demo", "result"):
        for oid in sorted({x["blob_oid"] for x in roles[role]}):
            static_by_blob[oid] = python_static(oid, role)
    enforcement = {name: enforcement_summary(roles[role], static_by_blob)
                   for name, role in (("test", "test"), ("demo", "demo"), ("result_tool", "result"))}
    require(enforcement["test"] == {"unique_blob_counts": {"ASSERT_AND_EXIT": 6, "EXIT_ONLY": 12, "NO_EXECUTABLE_GATE": 11},
                                     "occurrence_counts": {"ASSERT_AND_EXIT": 9, "EXIT_ONLY": 20, "NO_EXECUTABLE_GATE": 15}},
            "E_TEST_ENFORCEMENT")
    require(enforcement["demo"] == {"unique_blob_counts": {"EXIT_ONLY": 1, "NO_EXECUTABLE_GATE": 25},
                                     "occurrence_counts": {"EXIT_ONLY": 1, "NO_EXECUTABLE_GATE": 29}},
            "E_DEMO_ENFORCEMENT")
    require(enforcement["result_tool"] == {"unique_blob_counts": {"ASSERT_ONLY": 1, "EXIT_ONLY": 5, "NO_EXECUTABLE_GATE": 8},
                                            "occurrence_counts": {"ASSERT_ONLY": 1, "EXIT_ONLY": 18, "NO_EXECUTABLE_GATE": 16}},
            "E_TOOL_ENFORCEMENT")
    runtime = runtime_records(inventory, manifest, execute_runtime)
    golden_entries = [x for x in manifest["entries"] if x["path"].endswith("/golden_graphite_ref.npz")]
    require(len(golden_entries) == 8 and len({x["blob_sha"] for x in golden_entries}) == 2, "E_GOLD_DENOMINATOR")
    golden_occ = [{"ordinal": i, "release": x["version"], "path": x["path"],
                   "blob_oid": x["blob_sha"], "git_mode": x["git_mode"],
                   "size_bytes": x["size_bytes"]} for i, x in enumerate(golden_entries, 1)]
    gold_by_oid = {x["blob_sha"]: golden_record(x) for x in golden_entries}
    guide_occ, guide_blobs = guide_records(manifest, static_by_blob, runtime)
    require((len(guide_occ), len(guide_blobs), sum(x["physical_lines"] for x in guide_blobs)) == (20, 8, 854),
            "E_GUIDE_DENOMINATOR")
    controls = {path: {"raw_sha256": sha((ROOT / path).read_bytes()),
                       "lf_sha256": sha((ROOT / path).read_bytes().replace(b"\r\n", b"\n"))}
                for path in CONTROL_PATHS if (ROOT / path).exists()}
    inputs = {"manifest": {"path": MANIFEST_PATH, "raw_sha256": MANIFEST_RAW_SHA},
              "inventory": {"path": INVENTORY_PATH, "raw_sha256": INVENTORY_RAW_SHA,
                            "semantic_sha256": INVENTORY_SEMANTIC_SHA},
              "attestation": {"path": ATTESTATION_PATH, "raw_sha256": ATTESTATION_RAW_SHA,
                              "semantic_sha256": ATTESTATION_SEMANTIC_SHA},
              "persisted_chain": {"step82": "db167fdc941eafba0313b8476dfe7483108f13ff",
                                    "step83": "1af6c06fb5cff2918b846ed74ea213832f04f010",
                                    "step84": "f00bf2fa8f25c85f0c62cb901912763d98c8f070",
                                    "step85_current_parent": EXPECTED_PARENT,
                                    "inventory_containing_commit_is_owner": False},
              "controls": controls}
    matrix = common_header("PHASE_067_TEST_DEMO_GOLDEN_MATRIX")
    matrix.update({"inputs": inputs, "universe": EXPECTED,
                   "occurrence_projection": {"test": roles["test"], "demo": roles["demo"],
                                             "result_tool": roles["result"], "golden": golden_occ},
                   "python_blob_static_records": [static_by_blob[x] for x in sorted(static_by_blob)],
                   "enforcement_summary": enforcement,
                   "runtime_contract": {"representative_unique_blob_execution": True,
                                        "occurrence_projection_is_not_independent_corroboration": True,
                                        "network_allowed": False, "repository_external_disposable_roots": True,
                                        "runtime_authority": "OBSERVED_ISOLATED_PROCESS_ONLY",
                                        "runtime_records_sha256": sha(canonical(runtime))},
                   "runtime_records": runtime,
                   "golden_blob_records": [gold_by_oid[x] for x in sorted(gold_by_oid)],
                   "golden_route_records": golden_route_records(roles["test"], static_by_blob),
                   "golden_contract": {"two_blobs_must_remain_distinct": True,
                                       "capture_overwrite_by_release": "v1.0.13-v1.0.18.2 np.savez overwrite-capable; v1.0.19 refuses existing with exit 3",
                                       "later_test_gate_load_is_not_current_release_golden_provenance": True},
                   "validation": {"denominator_mismatch": 0, "ast_parse_failure": 0,
                                  "golden_member_failure": 0, "source_read_failure": 0,
                                  "runtime_assumption_promotions": 0},
                   "authority": {"source_static": True, "isolated_runtime_observation": bool(runtime),
                                 "test_pass_global": False, "demo_assertion_authority": False,
                                 "scientific_truth": False, "material_validity": False,
                                 "canonical_release": False, "publication_ready": False}})
    matrix = finish(matrix)
    conformance = common_header("PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX")
    conformance.update({"inputs": inputs, "matrix_semantic_sha256": matrix["semantic_sha256"],
                        "guide_occurrence_projection": guide_occ, "guide_blob_records": guide_blobs,
                        "tool_occurrence_projection": roles["result"],
                        "tool_blob_records": [static_by_blob[x] for x in sorted({r["blob_oid"] for r in roles["result"]})],
                        "guide_contract": {"guide_prose_is_self_report_until_exact_source_assertion_and_runtime_bound": True,
                                           "manifest_entry_index_base": 0,
                                           "stale_claims_preserved": True, "mirror_occurrences_not_corroboration": True},
                        "tool_contract": {"hardcoded_paths_are_portability_evidence_not_skip": True,
                                          "optional_dependency_failure_is_not_pass": True,
                                          "writer_and_check_modes_are_distinct": True,
                                          "stdout_pass_without_assert_or_exit_is_not_gate": True},
                        "validation": {"guide_line_mismatch": 0, "tool_blob_orphan": 0,
                                       "stale_claim_promotion": 0, "authority_promotion": 0},
                        "authority": {"source_static": True, "guide_claim_truth": False,
                                      "result_tool_output_validity": False, "scientific_truth": False,
                                      "material_validity": False, "canonical_release": False,
                                      "publication_ready": False}})
    return matrix, finish(conformance)


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    except Exception:
        try:
            os.unlink(name)
        except OSError:
            pass
        raise


def first_difference(left: Any, right: Any, path: str = "$") -> str:
    if type(left) is not type(right):
        return f"{path}:type:{type(left).__name__}!={type(right).__name__}"
    if isinstance(left, dict):
        if list(left) != list(right):
            return f"{path}:keys"
        for key in left:
            found = first_difference(left[key], right[key], f"{path}.{key}")
            if found:
                return found
        return ""
    if isinstance(left, list):
        if len(left) != len(right):
            return f"{path}:len:{len(left)}!={len(right)}"
        for index, (a, b) in enumerate(zip(left, right)):
            found = first_difference(a, b, f"{path}[{index}]")
            if found:
                return found
        return ""
    return "" if left == right else f"{path}:{left!r}!={right!r}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--no-runtime", action="store_true")
    args = parser.parse_args()
    require(args.collect ^ args.preview, "E_MODE")
    matrix, conformance = build(execute_runtime=not args.no_runtime)
    if args.collect:
        for rel, value in ((MATRIX_PATH, matrix), (CONFORMANCE_PATH, conformance)):
            target = ROOT / rel
            require(not target.exists(), f"E_REFUSE_OVERWRITE:{rel}")
            atomic_write(target, canonical(value))
        print(f"{GATE} collect test={EXPECTED['test_occurrences']}/{EXPECTED['test_blobs']} "
              f"demo={EXPECTED['demo_occurrences']}/{EXPECTED['demo_blobs']} runtime={len(matrix['runtime_records'])}")
    else:
        matrix2, conformance2 = build(execute_runtime=False if args.no_runtime else True)
        require(canonical(matrix) == canonical(matrix2),
                "E_PREVIEW_MATRIX_NONDETERMINISTIC:" + first_difference(matrix, matrix2))
        require(canonical(conformance) == canonical(conformance2),
                "E_PREVIEW_CONFORMANCE_NONDETERMINISTIC:" + first_difference(conformance, conformance2))
        print(f"{GATE} preview determinism=2/2 runtime={len(matrix['runtime_records'])}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(str(exc))
        raise SystemExit(1)
