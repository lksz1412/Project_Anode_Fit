#!/usr/bin/env python3
"""Validate Phase 068 Step 93 Phase 044/054 claim-level reaudit.

The validator binds the 21 declared historical inputs to frozen Git blobs and
to the already-persisted Step 92 full-read attestation.  It then validates one
closed judgment matrix that keeps historical statements, successor evidence,
fresh replay observations, and authority ceilings separate.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
SCHEMA = "P068-STEP93-PHASE044-054-READJUDICATION-2"
TIP = "11f90544865dd179739ca5bc5062b28c1078e504"
TIP_TREE = "34cc6332317a96b53891da6c970bbe0dfb81698e"
EXPECTED_PARENT = "25e3120ff0f38c5fa2bf603413034920640b3e62"
EXPECTED_SUBJECT = "audit(phase068): revalidate phase044 phase054 reviews"
CONTENT_TERMINAL = "PASS_P068_STEP93_PRIOR_REVIEW_REAUDIT"
PERSISTENCE_TERMINAL = "PASS_P068_STEP93_PERSISTENCE"
PRECOMMIT_MARKER = "P068_STEP93_PRIOR_REVIEW_REAUDIT_PRECOMMIT"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
ACTIVE_REF = "refs/heads/" + ACTIVE_BRANCH
TRACKING_REF = "refs/remotes/origin/" + ACTIVE_BRANCH
LIVE_ACTIVE_REF = "refs/heads/" + ACTIVE_BRANCH
UPSTREAM = "origin/" + ACTIVE_BRANCH
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"

FIXED_REFS = {
    "refs/remotes/origin/codex/lib-physics-endgame-v1025_2": (
        "refs/heads/codex/lib-physics-endgame-v1025_2",
        "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71",
    ),
    "refs/remotes/origin/main": (
        "refs/heads/main",
        "f0c381bd6dc315ac75cbffa93dd86ce83a37949b",
    ),
    "refs/remotes/origin/claude/version-1026-regsol-review-kl88j7": (
        "refs/heads/claude/version-1026-regsol-review-kl88j7",
        "e3e1a634f34b711aa4803fd190fe9120f1755f13",
    ),
    "refs/remotes/origin/codex/v1025_2-physics-conformance": (
        "refs/heads/codex/v1025_2-physics-conformance",
        TIP,
    ),
}

BUILDER = "Codex/work/v1025_phase068/build_phase068_step93.py"
VALIDATOR = "Codex/work/v1025_phase068/validate_phase068_step93.py"
MATRIX = "Codex/results/PHASE_068_PHASE044_054_REAUDIT_MATRIX.json"
RESULT = "Codex/results/PHASE_068_STEP_093_PHASE044_054_REAUDIT_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
STEP92_INVENTORY = "Codex/results/PHASE_068_CODEX_FORK_DIFF_INVENTORY.json"
STEP92_ATTESTATION = "Codex/results/PHASE_068_CODEX_FORK_FULL_READ_ATTESTATION.json"

EXACT_SEVEN = (BUILDER, VALIDATOR, MATRIX, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
PRE_JSON_SIX = (BUILDER, VALIDATOR, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
EXPECTED_STATUS = {path: ("M" if path in {PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER} else "A") for path in EXACT_SEVEN}

SOURCE_PATHS = (
    "Codex/plans/2026-07-27-v1025_2-physics-conformance-branch-plan.md",
    "Codex/plans/2026-07-27-v1025_2-latest-lineage-review-addendum-plan.md",
    "Codex/results/PHASE_044_053_V1025_2_CONFORMANCE_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_044_CURRENT_SOURCE_PROBES.json",
    "Codex/results/PHASE_044_LINEAGE_DIFF.json",
    "Codex/results/PHASE_044_REGSOL_THRESHOLD_PROBE.json",
    "Codex/results/PHASE_044_SOURCE_FREEZE_MANIFEST.json",
    "Codex/results/PHASE_044_V1010_V1025_2_LINEAGE_REVIEW.md",
    "Codex/results/PHASE_044_V1025_2_SOURCE_FREEZE_AND_COMPARISON_RESULT.md",
    "Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md",
    "Codex/results/PHASE_054_V1025_2_LATEST_REVIEW_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_FREEZE_MANIFEST.json",
    "Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_PROBES.json",
    "Codex/results/PHASE_054_V1025_2_REGSOL_CROSSCHECK.json",
    "Codex/work/v1025_2_physics_branch/phase044_current_source_probes.py",
    "Codex/work/v1025_2_physics_branch/phase044_lineage_diff.py",
    "Codex/work/v1025_2_physics_branch/phase044_regsol_threshold_probe.py",
    "Codex/work/v1025_2_physics_branch/phase044_source_manifest.py",
    "Codex/work/v1025_2_physics_branch/phase054_latest_source_manifest.py",
    "Codex/work/v1025_2_physics_branch/phase054_latest_source_probes.py",
    "Codex/work/v1025_2_physics_branch/phase054_regsol_crosscheck.py",
)

P44_HUMAN = {
    SOURCE_PATHS[0], SOURCE_PATHS[2], SOURCE_PATHS[7], SOURCE_PATHS[8],
}
P44_MACHINE = {
    SOURCE_PATHS[3], SOURCE_PATHS[4], SOURCE_PATHS[5], SOURCE_PATHS[6],
    SOURCE_PATHS[14], SOURCE_PATHS[15], SOURCE_PATHS[16], SOURCE_PATHS[17],
}

POINTER_PATHS = {
    "P": SOURCE_PATHS[0],
    "A": SOURCE_PATHS[1],
    "L": SOURCE_PATHS[2],
    "S": SOURCE_PATHS[8],
    "R": SOURCE_PATHS[7],
    "M": SOURCE_PATHS[9],
    "ML": SOURCE_PATHS[10],
    "J54": SOURCE_PATHS[12],
    "C67": "Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md",
}

ALLOWED_RELATIONS = {"CONFIRMS", "CORRECTS", "SUPERSEDES", "UNCHANGED_OPEN"}
PHASE67_DISPOSITIONS = {
    "BOUNDED_CORROBORATION", "CONFLICT", "OVERCLAIM",
    "SCOPE_MISMATCH", "STILL_OPEN_AUTHORITY",
}
HEX = set("0123456789abcdef")
MAX_JSON_BYTES = 4_000_000
MAX_JSON_NODES = 250_000
MAX_JSON_DEPTH = 64

# Filled only after all four control documents are final.  LF-normalized exact
# hashes prevent a token-only replacement from being accepted and resealed.
CONTROL_LF_SHA256 = {
    RESULT: "fbd7845d78f992690c525fbc8169428142cde138860a059adba65d2d046d943d",
    PARENT_LEDGER: "dbc53729d156137b5cc4d18f9408e891ac113b219e42ed0ff145563c09ad8d0d",
    ACTIVE_LEDGER: "3e98d29ca8e9bf19afdc57ca1a9e2993bb142fe06ec7aa3bf9127314000e134c",
    HANDOVER: "c09e8d2c0c499798395ce88034a3f178f5f5fd8d684be431de85d1023489cba5",
}


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str = "") -> None:
    raise ValidationError(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def physical_lines(raw: bytes) -> int:
    return 0 if not raw else raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def lf_normalize(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def is_hex40(value: str) -> bool:
    return len(value) == 40 and all(char in HEX for char in value)


def validate_expected_commit(value: str) -> None:
    if not is_hex40(value):
        fail("E_EXPECTED_COMMIT", value)


def validate_git_argv(args: list[str]) -> None:
    if not args or any(not isinstance(item, str) or "\0" in item for item in args):
        fail("E_GIT_ARGV", "shape")
    command = args[0]
    valid = False
    if command == "cat-file":
        valid = len(args) == 3 and args[1] == "blob" and is_hex40(args[2])
    elif command == "config":
        valid = args == ["config", "--get", "remote.origin.url"]
    elif command == "diff":
        valid = args == ["diff", "--cached", "--name-status", "--no-renames", "-z"]
    elif command == "diff-tree":
        valid = len(args) == 7 and args[1:6] == ["--no-commit-id", "--name-status", "--no-renames", "-r", "-z"] and is_hex40(args[6])
    elif command == "log":
        valid = len(args) == 4 and args[1:3] == ["-1", "--format=%s"] and is_hex40(args[3])
    elif command == "ls-files":
        valid = args == ["ls-files", "--stage", "-z", "--", *EXACT_SEVEN]
    elif command == "ls-remote":
        valid = len(args) == 4 and args[1:3] == ["--refs", ORIGIN_URL] and args[3].startswith("refs/heads/")
    elif command == "ls-tree":
        valid = (
            len(args) >= 5 and args[1] == "-l" and is_hex40(args[2])
            and args[3] == "--" and all(path in EXACT_SEVEN or path in SOURCE_PATHS for path in args[4:])
        )
    elif command == "rev-parse":
        valid = (
            len(args) == 2 and args[1] in {"HEAD", TRACKING_REF, "@{upstream}", f"{TIP}^{{tree}}", *FIXED_REFS}
        ) or (
            len(args) == 3 and args[1] == "--abbrev-ref" and args[2] in {"HEAD", "@{upstream}"}
        )
    elif command == "show":
        valid = (
            len(args) == 2 and ":" in args[1]
            and is_hex40(args[1].split(":", 1)[0])
            and args[1].split(":", 1)[1] in set(SOURCE_PATHS) | {STEP92_INVENTORY, STEP92_ATTESTATION, POINTER_PATHS["C67"]}
        ) or (
            len(args) == 4 and args[1:3] == ["-s", "--format=%P"] and is_hex40(args[3])
        )
    elif command == "status":
        valid = args == ["status", "--porcelain=v1", "-z", "--untracked-files=all"]
    if not valid:
        fail("E_GIT_ARGV", command)


def run_git(args: list[str], *, allow_exit: Iterable[int] = (0,)) -> bytes:
    validate_git_argv(args)
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False,
    )
    if proc.returncode not in set(allow_exit):
        detail = proc.stderr.decode("utf-8", "replace").strip()
        fail("E_GIT_EXEC", f"{args[0]}:{proc.returncode}:{detail}")
    return proc.stdout


def git_text(args: list[str]) -> str:
    try:
        return run_git(args).decode("utf-8", "strict").strip()
    except UnicodeDecodeError:
        fail("E_GIT_UTF8", args[0])


def strict_json_loads(raw: bytes, *, label: str) -> tuple[Any, int, int, int]:
    if len(raw) > MAX_JSON_BYTES:
        fail("E_JSON_LIMIT", label)
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        fail("E_JSON_UTF8", label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                fail("E_JSON_DUPLICATE_KEY", f"{label}:{key}")
            out[key] = value
        return out

    def nonfinite(token: str) -> Any:
        fail("E_JSON_NONFINITE", f"{label}:{token}")

    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=nonfinite)
    except ValidationError:
        raise
    except (json.JSONDecodeError, RecursionError, ValueError) as exc:
        fail("E_JSON_PARSE", f"{label}:{getattr(exc, 'msg', str(exc))}")

    nodes = leaves = max_depth = 0

    def walk(item: Any, depth: int) -> None:
        nonlocal nodes, leaves, max_depth
        nodes += 1
        max_depth = max(max_depth, depth)
        if nodes > MAX_JSON_NODES or depth > MAX_JSON_DEPTH:
            fail("E_JSON_LIMIT", label)
        if isinstance(item, dict):
            for child in item.values():
                walk(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                walk(child, depth + 1)
        else:
            if isinstance(item, float) and not math.isfinite(item):
                fail("E_JSON_NONFINITE", label)
            leaves += 1

    try:
        walk(value, 1)
    except RecursionError:
        fail("E_JSON_LIMIT", label)
    return value, nodes, leaves, max_depth


def parent_json(path: str) -> dict[str, Any]:
    raw = run_git(["show", f"{EXPECTED_PARENT}:{path}"])
    value, _, _, _ = strict_json_loads(raw, label=path)
    if not isinstance(value, dict):
        fail("E_PARENT_JSON", path)
    return value


def parse_ls_tree(path: str) -> tuple[str, str, int]:
    text = git_text(["ls-tree", "-l", TIP, "--", path])
    if not text or "\t" not in text:
        fail("E_SOURCE_TREE", path)
    meta, actual_path = text.split("\t", 1)
    parts = meta.split()
    if actual_path != path or len(parts) != 4 or parts[0] != "100644" or parts[1] != "blob":
        fail("E_SOURCE_TREE", path)
    if not is_hex40(parts[2]) or not parts[3].isdigit():
        fail("E_SOURCE_TREE", path)
    return parts[0], parts[2], int(parts[3])


def review_partition(path: str) -> str:
    if path in P44_HUMAN:
        return "DELEGATED_PHASE044_HUMAN_FULL_READ"
    if path in P44_MACHINE:
        return "DELEGATED_PHASE044_MACHINE_FULL_READ"
    return "ROOT_PHASE054_FULL_READ"


def build_source_records() -> tuple[list[dict[str, Any]], dict[str, int]]:
    attestation = parent_json(STEP92_ATTESTATION)
    inventory = parent_json(STEP92_INVENTORY)
    if attestation.get("tip") != TIP or inventory.get("tip") != TIP:
        fail("E_STEP92_TIP")
    if attestation.get("content_terminal") != "PASS_P068_STEP92_CODEX_FORK_READ":
        fail("E_STEP92_TERMINAL")
    if attestation.get("coverage_gaps") or attestation.get("decode_failures") or attestation.get("parser_failures"):
        fail("E_STEP92_GAPS")
    rows = attestation.get("full_read_rows")
    if not isinstance(rows, list):
        fail("E_STEP92_ROWS")

    records: list[dict[str, Any]] = []
    total_attested = total_bytes = total_lines = json_nodes = json_leaves = python_ast_nodes = 0
    max_json_depth = 0
    media = Counter()
    for path in SOURCE_PATHS:
        mode, blob, size = parse_ls_tree(path)
        raw = run_git(["cat-file", "blob", blob])
        if len(raw) != size or git_blob_oid(raw) != blob:
            fail("E_SOURCE_BLOB", path)
        try:
            text = raw.decode("utf-8", "strict")
        except UnicodeDecodeError:
            fail("E_SOURCE_UTF8", path)
        lines = physical_lines(raw)
        matches = [
            row for row in rows
            if isinstance(row, dict) and row.get("commit") == TIP and row.get("path") == path and row.get("blob") == blob
        ]
        if not matches:
            fail("E_STEP92_ATTESTATION", path)
        for row in matches:
            coverage = row.get("coverage", {}).get("bytes", {})
            if coverage != {"byte_end": size, "byte_start": 0, "status": "READ_FULL"}:
                fail("E_STEP92_COVERAGE", path)
            if row.get("raw_bytes") != size or row.get("raw_sha256") != sha256(raw) or row.get("lines") != lines:
                fail("E_STEP92_IDENTITY", path)
        selected = matches[0]
        parser = selected.get("parser")
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            media_role = "json"
            _, nodes, leaves, depth = strict_json_loads(raw, label=path)
            if parser != {"leaves": leaves, "max_depth": depth, "nodes": nodes, "strict_parse": True}:
                fail("E_SOURCE_JSON_ATTESTATION", path)
            json_nodes += nodes
            json_leaves += leaves
            max_json_depth = max(max_json_depth, depth)
        elif suffix == ".py":
            media_role = "python"
            try:
                tree = ast.parse(text, filename=path)
            except SyntaxError:
                fail("E_SOURCE_PYTHON_AST", path)
            ast_nodes = sum(1 for _ in ast.walk(tree))
            if parser != {"ast_node_count": ast_nodes, "ast_parse": True}:
                fail("E_SOURCE_PYTHON_ATTESTATION", path)
            python_ast_nodes += ast_nodes
        else:
            media_role = "markdown"
            if parser != {"utf8_decode": True}:
                fail("E_SOURCE_MARKDOWN_PARSER", path)
        media[media_role] += 1
        total_attested += len(matches)
        total_bytes += size
        total_lines += lines
        records.append({
            "attestation_occurrence_ids": sorted(str(row["occurrence_id"]) for row in matches),
            "blob": blob,
            "lines": lines,
            "media_role": media_role,
            "mode": mode,
            "path": path,
            "raw_bytes": size,
            "raw_sha256": sha256(raw),
            "review_partition": review_partition(path),
            "step92_attestation_count": len(matches),
            "step93_coverage": {"byte_end": size, "byte_start": 0, "line_end": lines, "line_start": 1, "status": "READ_FULL"},
        })
    totals = {
        "attestation_occurrences": total_attested,
        "json_leaves": json_leaves,
        "json_max_depth": max_json_depth,
        "json_nodes": json_nodes,
        "markdown_files": media["markdown"],
        "python_ast_nodes": python_ast_nodes,
        "python_files": media["python"],
        "json_files": media["json"],
        "raw_bytes": total_bytes,
        "source_files": len(records),
        "text_lines": total_lines,
    }
    expected = {
        "attestation_occurrences": 22,
        "json_files": 7,
        "json_leaves": 10171,
        "json_max_depth": 6,
        "json_nodes": 13699,
        "markdown_files": 7,
        "python_ast_nodes": 7703,
        "python_files": 7,
        "raw_bytes": 712453,
        "source_files": 21,
        "text_lines": 20997,
    }
    if totals != expected:
        fail("E_SOURCE_TOTALS", f"{totals}")
    return records, totals


def line_bounds(token: str) -> tuple[int, int]:
    if not token.startswith("L"):
        fail("E_POINTER", token)
    parts = token[1:].split("-")
    if len(parts) not in {1, 2} or any(not part.isdigit() for part in parts):
        fail("E_POINTER", token)
    start = int(parts[0])
    end = int(parts[-1])
    if start < 1 or end < start:
        fail("E_POINTER", token)
    return start, end


def ptr(code: str) -> str:
    parts = code.split(":")
    if len(parts) < 2 or parts[0] not in POINTER_PATHS or any(not part for part in parts):
        fail("E_POINTER", code)
    alias, lines, *anchors = parts
    line_bounds(lines)
    commit = EXPECTED_PARENT if alias == "C67" else TIP
    suffix = ":" + ":".join(anchors) if anchors else ""
    return f"{commit}:{POINTER_PATHS[alias]}:{lines}{suffix}"


def row_specs() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    def add(group: str, data: list[tuple[str, str, str]]) -> None:
        rows.extend((item_id, group, judgment, pointer) for item_id, judgment, pointer in data)

    add("governance", [
        ("H44-GOV-001", "Phase 044 baseline was ab196b on the conformance branch and v1.0.25.2 was the target release.", "P:L16-24;S:L37-46;L:L31-41"),
        ("H44-GOV-002", "v1.0.26A/B were excluded and comp_v26_data was limited to adopted v1.0.25.2 fit provenance.", "S:L42-51;R:L28-35"),
        ("H44-GOV-003", "The dirty v1.0.24.1 code-guide HTML was preserved but excluded.", "P:L22-24;S:L45-46;R:L61-64"),
        ("H44-GOV-004", "The two comparison lineages were the five Codex chapters and the v1.0.25.2 release/code/test/fit surfaces.", "P:L5-12"),
        ("H44-GOV-005", "Curve-fit success and physical-parameter identification require separate judgments.", "P:L51-57;S:L28-33"),
        ("H44-GOV-006", "Regular-solution, empirical-skew, causal, thermal, kinetic and hysteretic extensions do not share evidence status automatically.", "P:L53-55"),
        ("H44-GOV-007", "The manuscript must not be distorted to match code; implementation is downstream of the physics specification.", "P:L56-57;S:L756-760"),
        ("H44-GOV-008", "The earlier audit was locator-only; its verdicts, counts, scientific conclusions and priorities were not inherited.", "P:L59-76;S:L53-76;R:L46-54"),
        ("H44-GOV-009", "Used locator claims were said to be rechecked, but no exhaustive claim crosswalk was performed.", "P:L71-76;S:L73-76;L:L20"),
        ("H44-GOV-010", "The designated text inventory reported 1386 paths, 777 unique contents and 609 duplicate instances.", "S:L80-89"),
        ("H44-GOV-011", "The inventory covered seven text suffixes and excluded binary and visual artifacts.", "S:L90-95"),
        ("H44-GOV-012", "Manifest membership or byte difference is not full reading or scientific validation.", "S:L92-95;R:L56-60"),
        ("H44-GOV-013", "Five candidate chapters totaling 4320 lines were declared fully read.", "S:L121-132"),
        ("H44-GOV-014", "The current TeX graph was declared 56 files, 55 edges and zero unresolved includes.", "S:L134-145"),
        ("H44-GOV-015", "Other full-read declarations lacked exact file denominators for several governance, release and fit-dependency sets.", "S:L123-166"),
        ("H44-GOV-016", "Raw worker and review drafts were explicitly not all rejudged sentence by sentence.", "R:L48-54"),
        ("H44-GOV-017", "Changed Phase 038/040 bytes made old hash-bound evidence inapplicable to current bytes.", "S:L115-117"),
        ("H44-GOV-018", "The nominal Phase 044 range was Steps 861-900, but only 861-874 were defined and completed.", "P:L80-82;P:L121-139;L:L19-20"),
        ("H44-GOV-019", "The defined denominator was fourteen steps: four freeze plus ten comparison steps.", "P:L123-139;L:L19-20"),
        ("H44-GOV-020", "Steps 875-900 had no definition, status or omission rationale.", "P:L121-139;L:L19-20"),
        ("H44-GOV-021", "The gate required no missing declared sources/includes, exact pointers, no draft overcount and no inherited prior verdicts.", "P:L141-146"),
        ("H44-GOV-022", "The result labelled current-source and lineage comparison complete.", "S:L3-5"),
        ("H44-GOV-023", "v1.0.25.2 was frozen as a physics-conformance candidate rather than release truth.", "R:L18-24"),
        ("H44-GOV-024", "Existing source and Claude surfaces were preserved while new branch artifacts were created.", "P:L93-119;S:L805-810"),
        ("H44-GOV-025", "An earlier unexecuted integrated-reference/full-manuscript phase was said to be absorbed into Phases 044-050.", "P:L331-335"),
        ("H44-GOV-026", "The later ledger labelled Phase 044A/B complete and passing.", "L:L19-20"),
        ("H44-GOV-027", "The later ledger blanket-labelled Phases 044-053 closed.", "L:L43-48"),
        ("H44-GOV-028", "No claim-level supersession map connected the historical gate to the later closure wording.", "S:L793-810;L:L43-48"),
    ])
    add("fit_provenance", [
        ("H44-FIT-001", "sigr.csv was only blend-labelled and its experimental protocol remained unknown.", "S:L7-10;R:L118-119"),
        ("H44-FIT-002", "Active preprocessing used finite filtering, capacity sort/dedup, isotonic V(Q), 0.5 mV rebinning, longest-positive-run selection and Savitzky-Golay ensemble smoothing.", "S:L194-202"),
        ("H44-FIT-003", "The driver header's dMSMCD/wavelet description did not match the active body.", "S:L203-204"),
        ("H44-FIT-004", "The recorded reconstruction environment was Python 3.12.13, NumPy 2.3.5, pandas 2.2.3 and SciPy 1.17.0.", "S:L175-184"),
        ("H44-FIT-005", "The fit denominator was 1280 points, 14 transitions, 57 free parameters and baseline 0.5169124 mAh/V.", "S:L206-213"),
        ("H44-FIT-006", "Stored-8dp reconstruction reported R2 0.99964941790404 and BIC -4760.653827485789.", "S:L214-217;R:L118-128"),
        ("H44-FIT-007", "The release static path and independent formula differed by about 1.42e-14 mAh/V.", "S:L218-225;R:L130-132"),
        ("H44-FIT-008", "Stored-8dp and presentation-6dp curves differed by at most 0.0069744215 mAh/V; an acceptance tolerance was not fixed.", "S:L218-225"),
        ("H44-FIT-009", "The builder calculated from transient full precision, stored eight decimals and omitted prediction while emitting six-decimal transitions.", "S:L231-240;R:L148-155"),
        ("H44-FIT-010", "Original optimizer environment, full precision, success, termination, Jacobian and evaluation count were unavailable.", "S:L182-184;S:L226-241"),
        ("H44-FIT-011", "Original convergence, global optimality and exact optimizer replay were not established.", "S:L226-241"),
        ("H44-FIT-012", "Direct14 fit quality did not identify host/phase allocation or thermal/kinetic parameters.", "S:L226-229;R:L205-214"),
        ("H44-FIT-013", "BIC was only a same-objective working statistic for smoothed correlated residuals.", "S:L243-245;R:L126-128"),
        ("H44-FIT-014", "Five float64 hashes were declared for voltage, observation, vector, prediction and residual.", "S:L247-255"),
    ])
    add("scientific_finding", [
        ("H44-F001", "RT/(Fw) is broadening rather than electron stoichiometry; separate z and rederive the reduced entropy-production expression.", "S:L259-285;R:L205-209"),
        ("H44-F002", "Reversible-heat sign prose conflicted with the formula; retain -IT dU/dT under stated convention while control-volume allocation stays open.", "S:L287-311"),
        ("H44-F003", "Charging reverses signed trajectory, not state orientation; signed storage, metastability and the heat proof require rederivation.", "S:L313-337"),
        ("H44-F004", "The small-tail coefficient and dimensions were wrong; chemical and observation baselines and inadmissible denominators must be separated.", "S:L339-371"),
        ("H44-F005", "Fixed-state OCV differentiation includes w-prime logit(xi); a canonical entropy basis or rederivation is required.", "S:L373-399"),
        ("H44-F006", "Preserve raw network entropy production with capacity/rate/heat conditions and rebuild Chapter 4 as integrated EOS/DAE.", "S:L401-429"),
        ("H44-F007", "The alpha-skew observation map must remain empirical and isolated from signed storage, physical occupancy, heat and direction claims.", "S:L431-478"),
        ("H44-F008", "Normalized kernel measure and amplitude-bearing residual spectrum must be separated into a(L), Theta, K and b(L).", "S:L480-502"),
        ("H44-F009", "The thermal mirror mixed power and q-derivative; only a qualitative exp(-2dq/L) flag survived pending rederivation.", "S:L504-511"),
        ("H44-F010", "The shipped host preset was not the accepted generic Direct14 fit; model identity and objective differences forbid equating them.", "S:L513-556;R:L116-146"),
        ("H44-F011", "The threshold derivative-divergence claim omitted leading-mass cancellation; area/continuity survive while divergence wording is removed and theory-only status remains.", "S:L558-583;R:L180-194"),
    ])
    add("code_finding", [
        ("H44-C061", "Keyless width uses RT/F while dwdT and reported entropy are zero.", "S:L587-598"),
        ("H44-C062-A", "Hour-based C-rate and SI-second Eyring prefactor create an approximately 3600-fold lag-scale mismatch.", "S:L600-604;R:L165-178"),
        ("H44-C062-B", "The multi-temperature correction is -R ln(3600) in entropy/intercept; 20.298 kJ/mol is only a 298.15 K apparent offset.", "S:L606-621"),
        ("H44-C063", "Eager np.where logistic evaluation emitted two overflow and one invalid-divide warning despite finite output.", "S:L623-627"),
        ("H44-C064", "Voltage sorting destroys nonmonotonic acquisition history and needs a separate time-ordered trajectory route.", "S:L629-633;R:L196-204"),
        ("H44-C065", "Variable temperature is only partly pointwise because branch shift and lag use mean temperature.", "S:L635-639;R:L201-202"),
        ("H44-C066", "Finite 5L padding leaves exp(-5) residual and duplicate initial voltage can yield zero padding points.", "S:L641-645;R:L196-200"),
        ("H44-C067", "Default Si transitions could bypass invalid si_case validation.", "S:L647-650"),
        ("H44-C068-A", "The transition toggle changes future-instance global defaults but did not prove a stale mismatch inside existing instances.", "S:L652-660"),
        ("H44-C068-B", "Global R/F rebinding changes existing-object calculations while cached seed state remains stale.", "S:L661-664"),
        ("H44-C068-C", "Constants and transition choices should become explicit immutable profiles.", "S:L666"),
        ("H44-C069-A", "Inline documentation reversed default/opt-in and alpha-presence status.", "S:L668-673"),
        ("H44-C069-B", "The claimed five exact alpha upper-bound hits conflicted with stored maximum 7.99623012; active-set status remained unknown.", "S:L673-680"),
        ("H44-C0610-A", "Terminal I(Uoc-V) heat exists, so a blanket not-implemented statement was false.", "S:L682-689"),
        ("H44-C0610-B", "That heat path remained partial without sign/domain/control-volume or double-count guards.", "S:L691-694"),
        ("H44-C-EXTRA-001", "The lineage also recorded nonfinite lag falling back silently to equilibrium.", "R:L196-204"),
    ])
    add("preserved_concept", [
        ("H44-PRES-001", "Preserve skew-logistic derivative and empirical cumulative full-window area.", "S:L700-712"),
        ("H44-PRES-002", "Preserve the stored-8dp fourteen-peak empirical fit.", "S:L701-712"),
        ("H44-PRES-003", "Preserve first-order common-potential graphite/Si equilibrium architecture.", "S:L702-712"),
        ("H44-PRES-004", "Preserve the fSi-to-zero graphite recovery limit.", "S:L703-712"),
        ("H44-PRES-005", "Preserve the fixed-q implicit OCV derivative concept.", "S:L704-712"),
        ("H44-PRES-006", "Preserve reaction-entropy versus activation-entropy separation.", "S:L705-712"),
        ("H44-PRES-007", "Preserve the forward/backward mass-action skeleton.", "S:L706-712"),
        ("H44-PRES-008", "Preserve the nonnegative network entropy-production structure.", "S:L707-712"),
        ("H44-PRES-009", "Preserve the reversible/irreversible heat distinction.", "S:L708-712"),
        ("H44-PRES-010", "Preserve the electrical-Rn versus thermal-resistance distinction.", "S:L709-712"),
        ("H44-PRES-011", "Preserve the identifiability/falsification hierarchy.", "S:L710-712"),
        ("H44-PRES-012", "No preserved item may be copied without its Phase 044 correction and validity domain.", "S:L712"),
    ])
    add("architecture", [
        ("H44-ARCH-001", "Chapter 1: graphite equilibrium, observation map and charge balance.", "S:L718"),
        ("H44-ARCH-002", "Chapter 2: thermodynamics and heat.", "S:L719"),
        ("H44-ARCH-003", "Chapter 3: kinetics with fixed reaction stoichiometry.", "S:L720"),
        ("H44-ARCH-004", "Chapter 4: integrated EOS/DAE.", "S:L721"),
        ("H44-ARCH-005", "Chapter 5: hysteresis with fixed state orientation.", "S:L722"),
        ("H44-ARCH-006", "Material applications: graphite, LCO and Si/blend.", "S:L723"),
        ("H44-ARCH-007", "Empirical product: immutable fourteen-skew profile.", "S:L724"),
        ("H44-ARCH-008", "Implementation conformance belongs in an appendix or ledger.", "S:L725"),
        ("H44-ARCH-009", "Do not delete LCO/Si-blend chapters; relocate useful Chapter 2/4 content.", "S:L727-729"),
    ])
    add("product_split", [
        ("H44-PROD-001", "The empirical product owns preprocessing/vector/hash/metric, not physical interpretation.", "R:L227-236"),
        ("H44-PROD-002", "The physical-host product owns common potential, normalization, backgrounds and finite-rate contracts, not Direct14 validation claims.", "R:L238-248"),
        ("H44-PROD-003", "Legacy behavior belongs in immutable named compatibility profiles, not process-global toggles.", "R:L250-254"),
    ])
    add("purity", [
        ("H44-PURE-001", "The scholarly body allows nine physics/assumption/derivation/conservation/identifiability/closure/admissibility/boundary categories.", "S:L735-745"),
        ("H44-PURE-002", "Six code/history/solver/default/test/build categories are restricted to implementation sections or ledgers.", "S:L747-754"),
        ("H44-PURE-003", "Move code-level language out, retain mathematical existence/admissibility/branch selection, and never change physics to match code.", "S:L756-760"),
    ])
    add("test_run", [
        ("H44-TEST-RUN-001", "test_gates_v1025.py was reported 9/9 PASS.", "S:L764-766"),
        ("H44-TEST-RUN-002", "test_gates_v1024.py was reported PASS without a case denominator.", "S:L767"),
        ("H44-TEST-RUN-003", "The current-source probe was reported as a deterministic JSON match without a repeat denominator.", "S:L768"),
    ])
    add("test_proved_domain", [
        ("H44-TEST-P-001", "Tests were said to prove alpha=1 compatibility.", "S:L770-773"),
        ("H44-TEST-P-002", "Tests were said to prove skew area and smoothness.", "S:L772-774"),
        ("H44-TEST-P-003", "Tests were said to prove selected causal-window behavior.", "S:L774"),
        ("H44-TEST-P-004", "Tests were said to prove legacy regression.", "S:L775"),
        ("H44-TEST-P-005", "Tests were said to prove selected blend invariants only with explicit transitions.", "S:L776"),
    ])
    add("test_unproved_domain", [
        ("H44-TEST-N-001", "Tests did not prove the claimed production default7+7.", "S:L778-780"),
        ("H44-TEST-N-002", "Tests did not prove default-background consumption.", "S:L781"),
        ("H44-TEST-N-003", "Tests did not prove an accepted stored-8dp blend entry point.", "S:L782"),
        ("H44-TEST-N-004", "Tests did not prove invalid-si_case handling.", "S:L783"),
        ("H44-TEST-N-005", "Tests did not prove warnings-as-errors logistic stability.", "S:L784"),
        ("H44-TEST-N-006", "Tests did not prove keyless width-temperature round trip.", "S:L785"),
        ("H44-TEST-N-007", "Tests did not prove the SI rate/time contract.", "S:L786"),
        ("H44-TEST-N-008", "Tests did not prove nonmonotonic trajectory preservation.", "S:L787"),
        ("H44-TEST-N-009", "Tests did not prove scientific validity of candidate Chapters 1-5.", "S:L788"),
    ])
    add("test_scope_limit", [
        ("H44-TEST-LIM-001", "The v1.0.24 gate forced legacy4 and could not validate the then-claimed default7+7.", "S:L790-791"),
    ])
    add("phase_gate", [
        ("H44-GATE-001", "Current-source comparison was marked PASS.", "S:L795-797"),
        ("H44-GATE-002", "Stored-8dp reconstruction was marked PASS.", "S:L798"),
        ("H44-GATE-003", "Original optimizer reproduction was NOT AVAILABLE.", "S:L799"),
        ("H44-GATE-004", "Prior-audit independence was marked PASS despite the crosswalk gap.", "S:L800"),
        ("H44-GATE-005", "v1.0.10-v1.0.25.2 lineage review was marked PASS.", "S:L801"),
        ("H44-GATE-006", "Manuscript scientific promotion was BLOCKED.", "S:L802"),
        ("H44-GATE-007", "Implementation modification was NOT STARTED.", "S:L803"),
    ])
    versions = [
        ("1010", "historical skeleton with placeholders", "L93"), ("1011", "incomplete copy, not authority", "L94"),
        ("1012", "manuscript corrections only after revalidation", "L95"), ("1013", "first reliable implementation-correction spine", "L96"),
        ("1014", "theory/reference, not a solver release", "L97"), ("1015", "replace sequential-memory API and reject strong pointwise claims", "L98"),
        ("1016", "preserve keyed math under assumptions; reject keyless interpretation", "L99"), ("1017", "documentation release only", "L100"),
        ("10181", "documentation release without distinct code step", "L101"), ("10182", "Einstein correction as opt-in closure only", "L102"),
        ("1019", "strong common-core baseline with state/data caveats", "L103"), ("1020", "documentation expansion to fold into corrected manuscript", "L104"),
        ("1021", "salvage bounded derivations only", "L105"), ("1022", "keep equilibrium blend and gate finite-rate claims", "L106"),
        ("1023", "optional diagnostic without physical-validation claim", "L107"), ("1024", "preserve provenance lessons and discard production regsol path", "L108"),
        ("10241", "editorial snapshot, not model release", "L109"), ("1025", "preserve skew/honesty correction and rewrite defaults/memory claims", "L110"),
        ("10251", "authoritative editorial correction without new fit", "L111"), ("10252", "conformance candidate preserving Direct14 and corrected theory pieces", "L112"),
    ]
    add("version_disposition", [(f"H44-V-{code}", text, f"R:{line}") for code, text, line in versions])
    add("repair_order", [
        ("H44-REPAIR-001", "Ordered repair queue: freeze scope; crosswalk; preserve fit/provenance loss; repair physics blockers; split products; remove globals; test new defaults; then validate common protocols and holdouts.", "R:L256-275"),
    ])
    return rows


RELATION_OVERRIDES: dict[str, tuple[str, tuple[str, ...]]] = {
    "H44-GOV-001": ("SUPERSEDES", ("M:L12-21", "M:L49-56")),
    "H44-GOV-005": ("CONFIRMS", ("M:L44-47",)),
    "H44-GOV-007": ("CONFIRMS", ("M:L163-187",)),
    "H44-GOV-022": ("CORRECTS", ("M:L12-47", "M:L274-283")),
    "H44-GOV-023": ("CONFIRMS", ("M:L58-91",)),
    "H44-GOV-024": ("CONFIRMS", ("M:L18-21", "M:L93-107")),
    "H44-GOV-026": ("CORRECTS", ("M:L147-199", "M:L249-272")),
    "H44-GOV-027": ("CORRECTS", ("M:L147-199", "M:L249-272")),
    "H44-FIT-005": ("CONFIRMS", ("M:L114-126", "J54:L192-206:accepted_direct14_profile:points:parameter_count:stored_8dp_background")),
    "H44-FIT-006": ("CONFIRMS", ("M:L30-32",)),
    "H44-FIT-007": ("CONFIRMS", ("J54:L212:stored_8dp_release_kernel_vs_direct_max_abs",)),
    "H44-FIT-012": ("CONFIRMS", ("M:L30-47", "M:L123-126")),
    "H44-F010": ("CONFIRMS", ("M:L23-32", "M:L123-126")),
    "H44-C061": ("CONFIRMS", ("M:L249-261",)),
    "H44-C062-A": ("CONFIRMS", ("M:L249-261",)),
    "H44-C063": ("CONFIRMS", ("M:L249-261",)),
    "H44-C064": ("UNCHANGED_OPEN", ("M:L263-272",)),
    "H44-C065": ("UNCHANGED_OPEN", ("M:L263-272",)),
    "H44-C066": ("CONFIRMS", ("M:L249-269",)),
    "H44-C067": ("CORRECTS", ("M:L109-145",)),
    "H44-C069-B": ("CONFIRMS", ("M:L189-199",)),
    "H44-PRES-002": ("CONFIRMS", ("M:L30-32", "M:L114-126")),
    "H44-TEST-N-001": ("SUPERSEDES", ("M:L23-29", "M:L109-145")),
    "H44-TEST-N-004": ("CORRECTS", ("M:L120-145",)),
    "H44-TEST-LIM-001": ("CONFIRMS", ("M:L297-298",)),
    "H44-GATE-001": ("SUPERSEDES", ("M:L12-47", "M:L274-283")),
    "H44-GATE-002": ("CONFIRMS", ("M:L30-32",)),
    "H44-GATE-003": ("CONFIRMS", ("M:L189-199",)),
    "H44-GATE-006": ("CONFIRMS", ("M:L58-91",)),
    "H44-V-10252": ("CONFIRMS", ("M:L49-91",)),
}


def phase67_rows(item_id: str) -> tuple[str, ...]:
    rows: list[str] = []
    if item_id.startswith("H44-FIT-") or item_id in {"H44-F010", "H44-PRES-002"}:
        rows.extend(("C67:L63:C16", "C67:L64:C17"))
    if item_id in {"H44-FIT-010", "H44-FIT-011", "H44-GATE-003"}:
        rows.extend(("C67:L61:C14", "C67:L65:C18"))
    if item_id == "H44-FIT-001":
        rows.append("C67:L66:C19")
    if item_id in {"H44-FIT-001", "H44-FIT-012", "H44-TEST-N-009", "H44-GATE-006"}:
        rows.append("C67:L68:C21")
    if item_id.startswith("H44-C068") or item_id in {"H44-GOV-006", "H44-PROD-003"}:
        rows.extend(("C67:L51:C04", "C67:L52:C05"))
    if item_id in {"H44-C067", "H44-TEST-N-001", "H44-TEST-LIM-001"}:
        rows.append("C67:L51:C04")
    if item_id.startswith("H44-C062") or item_id == "H44-TEST-N-007":
        rows.append("C67:L57:C10")
    if item_id in {"H44-C063", "H44-TEST-N-005"}:
        rows.append("C67:L59:C12")
    if item_id in {"H44-C064", "H44-TEST-N-008"}:
        rows.append("C67:L60:C13")
    if item_id.startswith("H44-TEST-") or item_id == "H44-GATE-001":
        rows.append("C67:L53:C06")
    if item_id == "H44-GATE-002":
        rows.extend(("C67:L64:C17", "C67:L65:C18"))
    return tuple(dict.fromkeys(rows))


PHASE67_OVERALL = {
    "C04": "SUPPORTED_BOUNDED", "C05": "GROUND_NOT_FOUND",
    "C06": "PARTIAL", "C10": "PARTIAL", "C12": "SUPPORTED_BOUNDED",
    "C13": "PARTIAL", "C14": "PARTIAL", "C16": "SUPPORTED_BOUNDED",
    "C17": "SUPPORTED_BOUNDED", "C18": "GROUND_NOT_FOUND",
    "C19": "GROUND_NOT_FOUND", "C21": "GROUND_NOT_FOUND",
}

PHASE67_SCOPE_MISMATCH_IDS = {
    "H44-GOV-006",
    "H44-FIT-002", "H44-FIT-003", "H44-FIT-004", "H44-FIT-005",
    "H44-FIT-006", "H44-FIT-007", "H44-FIT-008", "H44-FIT-009",
    "H44-FIT-010", "H44-FIT-011", "H44-FIT-013", "H44-FIT-014",
    "H44-TEST-RUN-001", "H44-TEST-RUN-002", "H44-TEST-RUN-003",
    "H44-TEST-P-001", "H44-TEST-P-002", "H44-TEST-P-003",
    "H44-TEST-P-004", "H44-TEST-P-005", "H44-TEST-LIM-001",
    "H44-GATE-001",
}
PHASE67_OVERCLAIM_IDS = {
    "H44-TEST-P-001", "H44-TEST-P-002", "H44-TEST-P-003",
    "H44-TEST-P-004", "H44-TEST-P-005", "H44-GATE-001",
}
PHASE67_CONFLICT_IDS = {"H44-C067", "H44-TEST-N-001", "H44-TEST-LIM-001"}
PHASE67_BOUNDED_PARTIAL_IDS = {
    "H44-C062-A", "H44-C062-B", "H44-C064",
    "H44-TEST-N-002", "H44-TEST-N-003", "H44-TEST-N-004",
    "H44-TEST-N-005", "H44-TEST-N-006", "H44-TEST-N-007",
    "H44-TEST-N-008", "H44-TEST-N-009", "H44-GATE-003", "H44-GATE-006",
}


def phase67_comparison(item_id: str, codes: tuple[str, ...]) -> dict[str, Any]:
    if not codes:
        return {
            "dispositions": [],
            "row_statuses": [],
            "status": "NO_COMPARABLE_ROW",
        }
    row_ids = [code.rsplit(":", 1)[1] for code in codes]
    if any(row_id not in PHASE67_OVERALL for row_id in row_ids):
        fail("E_PHASE67_ROW", item_id)
    dispositions: set[str] = set()
    if any(PHASE67_OVERALL[row_id] == "SUPPORTED_BOUNDED" for row_id in row_ids) or item_id in PHASE67_BOUNDED_PARTIAL_IDS:
        dispositions.add("BOUNDED_CORROBORATION")
    if any(PHASE67_OVERALL[row_id] in {"PARTIAL", "GROUND_NOT_FOUND"} for row_id in row_ids):
        dispositions.add("STILL_OPEN_AUTHORITY")
    if item_id in PHASE67_SCOPE_MISMATCH_IDS:
        dispositions.add("SCOPE_MISMATCH")
    if item_id in PHASE67_OVERCLAIM_IDS:
        dispositions.add("OVERCLAIM")
    if item_id in PHASE67_CONFLICT_IDS:
        dispositions.add("CONFLICT")
    if not dispositions:
        fail("E_PHASE67_DISPOSITION", item_id)
    if not dispositions.issubset(PHASE67_DISPOSITIONS):
        fail("E_PHASE67_DISPOSITION", item_id)
    return {
        "dispositions": sorted(dispositions),
        "row_statuses": [
            {"id": row_id, "overall": PHASE67_OVERALL[row_id]}
            for row_id in row_ids
        ],
        "status": "COMPARABLE_ROWS_CLASSIFIED",
    }


def downstream_owner(item_id: str, group: str) -> str:
    if item_id == "H44-F011":
        return "PHASE068_STEP94"
    if group in {"code_finding", "test_run", "test_proved_domain", "test_unproved_domain", "test_scope_limit"}:
        return "PHASE068_STEP95_AND_LATER_IMPLEMENTATION"
    if group in {"governance", "phase_gate", "version_disposition", "repair_order"}:
        return "PHASE068_STEP96_TO_STEP98"
    if group == "fit_provenance":
        return "PHASE069_AND_PHASE072_083"
    return "PHASE069_AND_CANONICAL_REWRITE_PHASES"


def build_judgments() -> list[dict[str, Any]]:
    judgments: list[dict[str, Any]] = []
    for item_id, group, judgment, pointer_text in row_specs():
        relation, phase54_codes = RELATION_OVERRIDES.get(item_id, ("UNCHANGED_OPEN", ()))
        if relation not in ALLOWED_RELATIONS:
            fail("E_RELATION", item_id)
        if relation in {"CONFIRMS", "CORRECTS", "SUPERSEDES"} and not phase54_codes:
            fail("E_SUCCESSOR_EVIDENCE", item_id)
        phase44_pointers = [ptr(code) for code in pointer_text.split(";")]
        phase54_pointers = [ptr(code) for code in phase54_codes]
        p67_codes = phase67_rows(item_id)
        phase67_pointers = [ptr(code.rsplit(":", 1)[0]) + ":" + code.rsplit(":", 1)[1] for code in p67_codes]
        p67_comparison = phase67_comparison(item_id, p67_codes)
        current = {
            "CONFIRMS": "CONFIRMED_BOUNDED",
            "CORRECTS": "CORRECTED_CURRENT",
            "SUPERSEDES": "SUPERSEDED_CURRENT_USE_HISTORICAL_RECORD_RETAINED",
            "UNCHANGED_OPEN": "UNCHANGED_OPEN",
        }[relation]
        judgments.append({
            "authority_ceiling": "INTERNAL_FROZEN_SOURCE_AND_BOUNDED_REPLAY_ONLY",
            "current_adjudication": current,
            "downstream_owner": downstream_owner(item_id, group),
            "group": group,
            "id": item_id,
            "judgment": judgment,
            "phase044_pointers": phase44_pointers,
            "phase054_evidence_status": "DIRECT_SUCCESSOR_POINTER" if phase54_pointers else "CLAIM_SPECIFIC_SUCCESSOR_GROUND_NOT_FOUND",
            "phase054_pointers": phase54_pointers,
            "phase054_relation": relation,
            "phase067_comparison": p67_comparison,
            "phase067_pointers": phase67_pointers,
        })
    ids = [row["id"] for row in judgments]
    if len(ids) != len(set(ids)):
        fail("E_JUDGMENT_DUPLICATE")
    return judgments


def validate_judgment_pointers(judgments: list[dict[str, Any]]) -> dict[str, Any]:
    expected_targets = {
        POINTER_PATHS["P"]: TIP,
        POINTER_PATHS["L"]: TIP,
        POINTER_PATHS["S"]: TIP,
        POINTER_PATHS["R"]: TIP,
        POINTER_PATHS["M"]: TIP,
        POINTER_PATHS["J54"]: TIP,
        POINTER_PATHS["C67"]: EXPECTED_PARENT,
    }
    cache: dict[tuple[str, str], list[str]] = {}
    seen: set[str] = set()
    occurrences = anchored = tip_occurrences = parent_occurrences = 0
    for row in judgments:
        for field in ("phase044_pointers", "phase054_pointers", "phase067_pointers"):
            for pointer in row[field]:
                parts = pointer.split(":")
                if len(parts) < 3:
                    fail("E_POINTER_TARGET", pointer)
                commit, path, line_token = parts[:3]
                anchors = parts[3:]
                if expected_targets.get(path) != commit:
                    fail("E_POINTER_COMMIT", pointer)
                key = (commit, path)
                if key not in cache:
                    raw = run_git(["show", f"{commit}:{path}"])
                    try:
                        cache[key] = raw.decode("utf-8", "strict").splitlines()
                    except UnicodeDecodeError:
                        fail("E_POINTER_UTF8", pointer)
                start, end = line_bounds(line_token)
                lines = cache[key]
                if end > len(lines):
                    fail("E_POINTER_BOUNDS", pointer)
                selected = "\n".join(lines[start - 1:end])
                if any(anchor not in selected for anchor in anchors):
                    fail("E_POINTER_ANCHOR", pointer)
                occurrences += 1
                anchored += len(anchors)
                tip_occurrences += int(commit == TIP)
                parent_occurrences += int(commit == EXPECTED_PARENT)
                seen.add(pointer)
    if set(cache) != {(commit, path) for path, commit in expected_targets.items()}:
        fail("E_POINTER_COVERAGE")
    return {
        "anchored_occurrences": anchored,
        "expected_parent_occurrences": parent_occurrences,
        "occurrences": occurrences,
        "target_files": len(cache),
        "tip_occurrences": tip_occurrences,
        "unique_pointers": len(seen),
    }


GROUP_COUNTS = {
    "architecture": 9,
    "code_finding": 16,
    "fit_provenance": 14,
    "governance": 28,
    "phase_gate": 7,
    "preserved_concept": 12,
    "product_split": 3,
    "purity": 3,
    "repair_order": 1,
    "scientific_finding": 11,
    "test_proved_domain": 5,
    "test_run": 3,
    "test_scope_limit": 1,
    "test_unproved_domain": 9,
    "version_disposition": 20,
}


def coverage_register(judgments: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["group"] for row in judgments)
    if dict(sorted(counts.items())) != GROUP_COUNTS:
        fail("E_JUDGMENT_GROUP_COUNTS", str(dict(counts)))
    science = [f"H44-F{i:03d}" for i in range(1, 12)]
    present = {row["id"] for row in judgments}
    if not set(science).issubset(present):
        fail("E_SCIENCE_COVERAGE")
    code_sections = {
        "6.1": ["H44-C061"],
        "6.2": ["H44-C062-A", "H44-C062-B"],
        "6.3": ["H44-C063"],
        "6.4": ["H44-C064"],
        "6.5": ["H44-C065"],
        "6.6": ["H44-C066"],
        "6.7": ["H44-C067"],
        "6.8": ["H44-C068-A", "H44-C068-B", "H44-C068-C"],
        "6.9": ["H44-C069-A", "H44-C069-B"],
        "6.10": ["H44-C0610-A", "H44-C0610-B"],
    }
    if any(not set(ids).issubset(present) for ids in code_sections.values()):
        fail("E_CODE_COVERAGE")
    relations = Counter(row["phase054_relation"] for row in judgments)
    comparable = [row for row in judgments if row["phase067_comparison"]["status"] == "COMPARABLE_ROWS_CLASSIFIED"]
    phase67_dispositions = Counter(
        disposition
        for row in comparable
        for disposition in row["phase067_comparison"]["dispositions"]
    )
    if set(phase67_dispositions) != PHASE67_DISPOSITIONS:
        fail("E_PHASE67_DISPOSITION_COVERAGE", str(dict(phase67_dispositions)))
    return {
        "code_named_sections": code_sections,
        "group_counts": dict(sorted(counts.items())),
        "judgment_rows": len(judgments),
        "phase054_relation_counts": dict(sorted(relations.items())),
        "phase067_comparable_rows": len(comparable),
        "phase067_disposition_counts": dict(sorted(phase67_dispositions.items())),
        "phase067_no_comparable_rows": len(judgments) - len(comparable),
        "register_granularity": "NAMED_TOPIC_LEVEL_WITH_COMPOUND_CLAUSES_NOT_ATOMIC_PROPOSITION_DENOMINATOR",
        "scientific_finding_ids": science,
        "scientific_findings": len(science),
        "scientific_severity_denominator": {"BLOCKER": 4, "MAJOR": 7},
        "unique_ids": len(present),
    }


MANIFEST_CHANGES = (
    ("Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md", 23279, 284, "08b02ccb097a8872008ec0d0f9e62e129e206a5e7560071c3fa7fb370f3ea11a", 30245, 381, "00c89fb5a3078ff5b53a797e061fd5a80c9ef305d123aa1d77acd151b816d35d"),
    ("Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py", 129709, 2004, "eaa019f6a2f73d9274fbeea6211fa645d1e734ae98e490efbd473196f4a12746", 131823, 2024, "c28101568b1b57f7dcb1e20c19fcdaa997fb5022d6230f839657216e1872ae44"),
    ("Claude/docs/v1.0.25.2/_sections/ch1_sec05b_gr2L.tex", 28168, 274, "192b126463432940995892f835cbc0a37f3ed6baa5891d5a1d4e262b8565bbf5", 28508, 277, "b7e3d1217073b095ec6c9a88388e7e885738216a6bb883584a4222ca724ce777"),
    ("Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex", 10701, 126, "08d704a380330a58fcfad158ff92833ac604a48a206afb78a22e8bbc6832b62b", 10727, 126, "ea807c55b8fb5bacc9af91836142034937af410abc78dc3e6d8c088d54557c59"),
    ("Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md", 7173, 132, "881f8c0b6d8934513b6e4e329c345d444854d63bb86ec09526e987e8ab5e1aa1", 10087, 175, "76f6565912f7fdbadb501c665f0e8969948e28c257af6b7ac9bd116a6015ee49"),
    ("Claude/docs/v1.0.25.2/test_gates_v1024.py", 34274, 637, "ac5a893f49755c7dde0053ece82a7b7c84fc5fe683173d0cb8e154f1677e942c", 34214, 637, "8817607e36e65f83b80df9dada5538a19d359f3fdd6908b9028f831a4bbea83e"),
)


def manifest_changes() -> list[dict[str, Any]]:
    return [{
        "frozen_tip": {"bytes": new_b, "lines": new_l, "sha256": new_h},
        "path": path,
        "stored_baseline": {"bytes": old_b, "lines": old_l, "sha256": old_h},
    } for path, old_b, old_l, old_h, new_b, new_l, new_h in MANIFEST_CHANGES]


def replay_records(source_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = [
        {"id": "R93-01", "artifact": "PHASE_044_SOURCE_FREEZE_MANIFEST", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 459104, "sha256": "19a5933954c1c92415cb66beea229ecfce9826af202c5e778602d1e9a7541d10"}, "fresh": {"bytes": 473900, "sha256": "6154be57788fd5c582f2f7f76aa5aad1f68dd13ad045393d37351d3949a4c653"}, "result": "COUNT_STABLE_RECORD_STALE", "details": {"counts": "1386/777/609/231/56/55", "changed_file_records": 6, "fresh_cross_runtime": "RAW_IDENTICAL"}, "ceiling": "FIXED_MANIFEST_SCOPE_ONLY"},
        {"id": "R93-02", "artifact": "PHASE_044_LINEAGE_DIFF", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 59244, "sha256": "85647ea3c87910f679ab2d43ff4dc82aa4a071734a20e134483f64613aaddb79"}, "fresh": {"bytes": 60741, "sha256": "3967b21feb8991770b7474940b0ae3c2afc3ee50dbc5f64a7f9d1dbcfe192475"}, "result": "SEMANTIC_IDENTICAL_RAW_CRLF_DRIFT", "details": {"aggregate": "20/545/417/199/599", "raw_delta_bytes": 1497}, "ceiling": "BYTE_DIFF_IS_NEWLINE_ONLY"},
        {"id": "R93-03", "artifact": "PHASE_044_CURRENT_SOURCE_PROBES", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 5525, "sha256": "2de5211ba1394de5ef84f9a0671d51c1150f906fafe5bfd5e9e26103a36de752"}, "fresh": {"bytes": 5756, "sha256": "8b724bd1e343d91418383ab1e07ebc3c570fa8fa2d1520e6b8540bf7a2d61d11"}, "result": "MATERIAL_CURRENT_SOURCE_DRIFT", "details": {"leaf_differences": 25, "default": "7+7_TO_4+2", "invalid_si_case": "ACCEPTED_TO_REJECTED", "direct14": "NEAR_PRESERVED", "python314": "DEPENDENCY_MISSING_PANDAS"}, "ceiling": "SOURCE_ENVIRONMENT_PATH_AND_ARRAY_DRIFT_CONFOUNDED"},
        {"id": "R93-04", "artifact": "PHASE_044_REGSOL_THRESHOLD_PROBE", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 3290, "sha256": "e1be03de00ed1ce35f2a27a67d104c43491685b98cc5122367d6a0fcf47bbd12"}, "fresh": {"bytes": 3368, "sha256": "c3211bd8055cd51a13b59d4e1d137fa74630d017e98e680f16ecf983f486b0da"}, "result": "QUALITATIVE_TREND_PRESERVED_NUMERIC_DRIFT", "details": {"numeric_leaf_differences": 33, "max_abs_drift": "1.1842384850524468e-09", "max_rel_drift": "2.0074797143116978e-10"}, "ceiling": "FINITE_GRID_NUMERICAL_NOT_ANALYTIC_PROOF"},
        {"id": "R93-05", "artifact": "PHASE_054_V1025_2_LATEST_SOURCE_FREEZE_MANIFEST", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 3028, "sha256": "91f445aac02c448e2d0cc09dcbb438f3f927b87ea0c944e76c4ab93fab4d9279"}, "fresh": {"bytes": 3028, "sha256": "91f445aac02c448e2d0cc09dcbb438f3f927b87ea0c944e76c4ab93fab4d9279"}, "result": "RAW_AND_SEMANTIC_IDENTICAL", "details": {}, "ceiling": "TEN_FILE_DECLARED_SCOPE_ONLY"},
        {"id": "R93-06", "artifact": "PHASE_054_V1025_2_LATEST_SOURCE_PROBES", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 9280, "sha256": "3c6d039f7b35d5cb1dacdfc5cd678ad554c857e55647ffc1821d3a792a22b8b8"}, "fresh": {"bytes": 9572, "sha256": "9235155e30aeadb13f1455d82a36d95c3830862151bb448104e5afe9eefab1d9"}, "result": "SEMANTIC_NEAR_REPLAY_WITH_PATH_ARRAY_AND_LAST_DIGIT_DRIFT", "details": {"leaf_differences": 15, "current_default_r2": "0.07507231361482658_TO_0.07507231361482647", "max_reported_parameter_drift": "1.461259446777774e-09", "python314": "DEPENDENCY_MISSING_SCIPY"}, "ceiling": "NO_ORIGINAL_OPTIMIZER_OR_EXTERNAL_AUTHORITY"},
        {"id": "R93-07", "artifact": "PHASE_054_V1025_2_REGSOL_CROSSCHECK", "runtimes": ["3.12.10", "3.14.4"], "stored": {"bytes": 11893, "sha256": "de29023d4ea021900b60b0271787dc1e36bfcc463f12935d2db2e8afe7e02923"}, "fresh": {"bytes": 12225, "sha256": "5d388655c67b1a66ebae1ee6ecaee3a11ec67157a537913f5b9cc8f5bfb3111d"}, "result": "QUALITATIVE_RESULT_PRESERVED_NUMERIC_DRIFT", "details": {"numeric_leaf_differences": 4, "max_abs_drift": "3.552713678800501e-12", "max_rel_drift": "3.6645755563035957e-13"}, "ceiling": "STEP94_INDEPENDENT_DERIVATION_REQUIRED"},
    ]
    scripts = {
        "R93-01": SOURCE_PATHS[17], "R93-02": SOURCE_PATHS[15],
        "R93-03": SOURCE_PATHS[14], "R93-04": SOURCE_PATHS[16],
        "R93-05": SOURCE_PATHS[18], "R93-06": SOURCE_PATHS[19],
        "R93-07": SOURCE_PATHS[20],
    }
    outputs = {
        "R93-01": SOURCE_PATHS[6], "R93-02": SOURCE_PATHS[4],
        "R93-03": SOURCE_PATHS[3], "R93-04": SOURCE_PATHS[5],
        "R93-05": SOURCE_PATHS[11], "R93-06": SOURCE_PATHS[12],
        "R93-07": SOURCE_PATHS[13],
    }
    captures = {"R93-01": "NAMED_FILE", "R93-02": "NAMED_FILE"}
    fixed_parameters = {
        "R93-01": "script literals: 20 version names, seven text suffixes, three release masters, declared governance/support lists; no CLI parameters",
        "R93-02": "script literals: 20 ordered versions, seven text suffixes, one excluded path; no CLI parameters",
        "R93-03": "script literals: active source/fit/data paths, Savitzky-Golay ratios 0.01/0.02/0.03, voltage 0.060..0.700 V at 0.0005 V; no CLI parameters",
        "R93-04": "R=8.314, T=298.15 K, F=96485, U0=0, width=0.010 V, voltage=-0.12..0.12 V/1201, eight epsilons, quadrature=1600; no CLI parameters",
        "R93-05": "script literal ten-input manifest and four lineage identifiers; no CLI parameters",
        "R93-06": "T=288.15/308.15 K, voltage=0.03..0.34 V/1000 plus source-embedded fit bounds and stored profile; no CLI parameters",
        "R93-07": "R=8.314, T=298.15 K, F=96485, U0=0, width=0.010 V, voltage=-1..1 V/4001, interaction ratios 0/1/1.999/2/2.001/3/4/8, alpha=1/4/8, epsilon=1e-3/1e-4/1e-5, quadrature=1600; no CLI parameters",
    }
    output_fields = {
        "R93-01": ["path/content/duplicate/TeX totals", "per-file identity changes"],
        "R93-02": ["20 version rows", "added/removed/changed totals", "semantic JSON"],
        "R93-03": ["default composition", "invalid si_case", "Direct14 metrics", "typed leaf diff"],
        "R93-04": ["epsilon derivative ratios", "area", "typed numeric leaf diff"],
        "R93-05": ["ten source identities", "lineage", "scope"],
        "R93-06": ["default/opt-in wiring", "Direct14", "implementation probes", "typed leaf diff"],
        "R93-07": ["area", "gap weight", "continuity", "derivative ratios", "typed numeric leaf diff"],
    }
    comparison_policy = {
        "R93-01": "exact integer totals; exact typed file-record comparison; no numeric tolerance",
        "R93-02": "exact parsed-JSON equality; raw CRLF-only difference reported separately",
        "R93-03": "exact typed-leaf comparison; numerical differences reported, not accepted as identity",
        "R93-04": "exact typed-leaf comparison; max absolute/relative drift reported without analytic-promotion tolerance",
        "R93-05": "exact raw-byte and parsed-JSON equality",
        "R93-06": "exact typed-leaf comparison; numerical/path/hash drift reported, not accepted as identity",
        "R93-07": "exact typed-leaf comparison; max absolute/relative drift reported without analytic-promotion tolerance",
    }
    successful_runtimes = {
        "R93-01": ("3.12.10", "3.14.4"), "R93-02": ("3.12.10", "3.14.4"),
        "R93-03": ("3.12.10",), "R93-04": ("3.12.10", "3.14.4"),
        "R93-05": ("3.12.10", "3.14.4"), "R93-06": ("3.12.10",),
        "R93-07": ("3.12.10", "3.14.4"),
    }
    dependency_failures = {"R93-03": ("3.14.4", "pandas"), "R93-06": ("3.14.4", "SciPy")}
    by_path = {row["path"]: row for row in source_records}

    def frozen_identity(path: str) -> dict[str, Any]:
        row = by_path[path]
        return {
            "blob": row["blob"], "bytes": row["raw_bytes"], "commit": TIP,
            "path": path, "sha256": row["raw_sha256"],
        }

    for record in records:
        record_id = record["id"]
        script = scripts[record_id]
        attempts = [{
            "argv": ["py", f"-{runtime[:4]}", script],
            "exit_code": 0,
            "output_bytes": record["fresh"]["bytes"],
            "output_sha256": record["fresh"]["sha256"],
            "runtime": runtime,
            "status": "SUCCESS",
        } for runtime in successful_runtimes[record_id]]
        if record_id in dependency_failures:
            runtime, dependency = dependency_failures[record_id]
            attempts.append({
                "argv": ["py", f"-{runtime[:4]}", script],
                "dependency": dependency,
                "exit_code": None,
                "exit_code_status": "NONZERO_VALUE_NOT_RETAINED",
                "runtime": runtime,
                "status": "DEPENDENCY_MISSING",
            })
        record["protocol"] = {
            "capture": captures.get(record_id, "STDOUT_JSON"),
            "comparison_policy": comparison_policy[record_id],
            "fixed_parameters": fixed_parameters[record_id],
            "input_object_contract": {
                "commit": TIP, "tree": TIP_TREE,
                "materialization": "external disposable exact-tip tree with LF object verification",
            },
            "output_fields_compared": output_fields[record_id],
            "reproducible_argv_template": ["py", "-<3.12|3.14>", script],
            "script_source": frozen_identity(script),
            "stored_output_source": frozen_identity(outputs[record_id]),
            "working_directory": "EXTERNAL_DISPOSABLE_EXACT_TIP_TREE_ROOT",
        }
        record["runtime_attempts"] = attempts
        record["transcript_evidence"] = {
            "derived_output_digests_retained": True,
            "raw_stdout_stderr_retained": False,
            "status": "BOUNDED_ROOT_SESSION_ATTESTATION_NOT_MACHINE_REEXECUTED_BY_STEP93_VALIDATOR",
        }
        del record["runtimes"]
    return records


def file_identity(path: str) -> dict[str, Any]:
    raw = (ROOT / path).read_bytes()
    normalized = lf_normalize(raw)
    return {
        "lf_bytes": len(normalized), "lf_sha256": sha256(normalized),
        "lines": physical_lines(raw), "path": path,
        "raw_bytes": len(raw), "raw_sha256": sha256(raw),
    }


def pre_json_identities() -> list[dict[str, Any]]:
    for path in PRE_JSON_SIX:
        if not (ROOT / path).is_file():
            fail("E_PRE_JSON_MISSING", path)
    return [file_identity(path) for path in PRE_JSON_SIX]


def expected_matrix() -> dict[str, Any]:
    source_records, totals = build_source_records()
    judgments = build_judgments()
    pointer_validation = validate_judgment_pointers(judgments)
    coverage = coverage_register(judgments)
    payload: dict[str, Any] = {
        "authority": {
            "canonical_theory": False,
            "external_scientific_truth": False,
            "material_or_mechanism_validity": False,
            "original_optimizer_recovered": False,
            "publication_readiness": False,
            "scientific_truth_promotions": 0,
            "whole_commit_adoptions": 0,
        },
        "content_terminal": CONTENT_TERMINAL,
        "coverage_register": coverage,
        "expected_parent": EXPECTED_PARENT,
        "fixed_tip": TIP,
        "fixed_tip_tree": TIP_TREE,
        "judgments": judgments,
        "judgment_register_contract": {
            "atomic_proposition_denominator_claimed": False,
            "compound_clause_recovery": "USE_EACH_ROW_PHASE044_POINTERS_AND_FROZEN_SOURCE_BLOBS",
            "granularity": "NAMED_TOPIC_LEVEL",
            "preservation_copy_rule": {
                "judgment": "No preserved item may be copied without its Phase 044 correction and validity domain.",
                "pointer": ptr("S:L712"),
            },
        },
        "manifest_record_changes": manifest_changes(),
        "phase": 68,
        "pointer_validation": pointer_validation,
        "pre_json_file_identities": pre_json_identities(),
        "precommit_marker": PRECOMMIT_MARKER,
        "replay_environment": {
            "external_tree_cleanup": {"bytes": 195717850, "deleted": True, "files": 3261, "pycache_directories": 4},
            "python312": {"numpy": "2.3.5", "pandas": "3.0.2", "python": "3.12.10", "scipy": "1.17.1"},
            "python314": {"numpy": "2.5.0", "pandas": "DEPENDENCY_MISSING", "python": "3.14.4", "scipy": "DEPENDENCY_MISSING"},
            "retained_raw_transcripts": False,
        },
        "replay_records": replay_records(source_records),
        "required_commit_subject": EXPECTED_SUBJECT,
        "schema": SCHEMA,
        "source_totals": totals,
        "sources": source_records,
        "step": 93,
        "supersession_rule": "A SUPERSEDES row replaces current-form use only; the historical Phase 044 record remains addressable.",
    }
    payload["semantic_sha256"] = semantic_sha(payload)
    return payload


def result_text(path: str) -> str:
    raw = (ROOT / path).read_bytes()
    try:
        return raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        fail("E_CONTROL_UTF8", path)


def validate_controls() -> None:
    paths = (RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
    for path in paths:
        expected_hash = CONTROL_LF_SHA256.get(path, "")
        raw = (ROOT / path).read_bytes()
        if len(expected_hash) != 64 or any(char not in HEX for char in expected_hash):
            fail("E_CONTROL_HASH_CONFIG", path)
        if sha256(lf_normalize(raw)) != expected_hash:
            fail("E_CONTROL_HASH", path)
        text = result_text(path)
        markers = [line for line in text.splitlines() if line.startswith("Current-state marker:")]
        if markers != [f"Current-state marker: `{PRECOMMIT_MARKER}`"]:
            fail("E_CONTROL_MARKER", path)
        for token in (EXPECTED_PARENT, EXPECTED_SUBJECT, CONTENT_TERMINAL, PERSISTENCE_TERMINAL, "PENDING_AT_PRECOMMIT_BY_DESIGN"):
            if token not in text:
                fail("E_CONTROL_TOKEN", f"{path}:{token}")
        if "25e3120ff0f38c5fa2bf603413034920640b3e62" not in text or "PASS_P068_STEP92_PERSISTENCE" not in text:
            fail("E_PREDECESSOR_TOKEN", path)
    result = result_text(RESULT)
    for token in ("source records: `21/21`", "Step 92 attestation occurrences: `22/22`", "judgment rows: `142/142`", "scientific truth promotions: `0`"):
        if token not in result:
            fail("E_RESULT_TOKEN", token)
    active = result_text(ACTIVE_LEDGER)
    handover = result_text(HANDOVER)
    if "## Next Exact Step" not in active or "Step 94" not in active.split("## Next Exact Step", 1)[1]:
        fail("E_CONTROL_NEXT", ACTIVE_LEDGER)
    if "## Exact Next Action" not in handover or "Step 94" not in handover.split("## Exact Next Action", 1)[1]:
        fail("E_CONTROL_NEXT", HANDOVER)


def parse_status() -> dict[str, str]:
    raw = run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    records = raw.split(b"\0")
    if records[-1] != b"":
        fail("E_STATUS_PARSE")
    out: dict[str, str] = {}
    for record in records[:-1]:
        if len(record) < 4 or record[2:3] != b" ":
            fail("E_STATUS_PARSE")
        code = record[:2].decode("ascii", "strict")
        path = record[3:].decode("utf-8", "strict").replace("\\", "/")
        if path in out or code[0] in "RC" or code[1] in "RC":
            fail("E_STATUS_PARSE", path)
        out[path] = code
    return out


def expected_porcelain(paths: tuple[str, ...], *, staged: bool) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        status = EXPECTED_STATUS[path]
        result[path] = (status + " ") if staged else ("??" if status == "A" else " M")
    return result


def validate_status(paths: tuple[str, ...], *, staged: bool, code: str) -> None:
    actual = parse_status()
    expected = expected_porcelain(paths, staged=staged)
    if actual != expected:
        fail(code, f"actual={actual}")


def live_oid(ref: str) -> str:
    text = git_text(["ls-remote", "--refs", ORIGIN_URL, ref])
    parts = text.split()
    if len(parts) != 2 or parts[1] != ref or not is_hex40(parts[0]):
        fail("E_LIVE_REF", ref)
    return parts[0]


def validate_origin_and_tip_tree() -> None:
    if git_text(["config", "--get", "remote.origin.url"]) != ORIGIN_URL:
        fail("E_ORIGIN_URL")
    if git_text(["rev-parse", f"{TIP}^{{tree}}"]) != TIP_TREE:
        fail("E_TIP_TREE")


def validate_fixed_refs() -> None:
    for local_ref, (remote_ref, expected) in FIXED_REFS.items():
        if git_text(["rev-parse", local_ref]) != expected:
            fail("E_FIXED_REF", local_ref)
        if live_oid(remote_ref) != expected:
            fail("E_FIXED_LIVE_REF", remote_ref)


def validate_precommit_boundary() -> None:
    validate_origin_and_tip_tree()
    if git_text(["rev-parse", "--abbrev-ref", "HEAD"]) != ACTIVE_BRANCH:
        fail("E_BRANCH")
    if git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]) != UPSTREAM:
        fail("E_UPSTREAM")
    for ref in ("HEAD", TRACKING_REF, "@{upstream}"):
        if git_text(["rev-parse", ref]) != EXPECTED_PARENT:
            fail("E_PRECOMMIT_BOUNDARY", ref)
    if live_oid(LIVE_ACTIVE_REF) != EXPECTED_PARENT:
        fail("E_PRECOMMIT_LIVE")
    validate_fixed_refs()


def validate_source_text(path: str, source: str) -> None:
    """Validate the loaded source shape; this is not a pre-execution sandbox."""
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError:
        fail("E_SOURCE_AST", path)
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

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
            allowed = {"argparse", "ast", "collections", "hashlib", "json", "math", "os", "pathlib", "subprocess", "sys", "tempfile", "typing", "validate_phase068_step93"}
            if any(name not in allowed for name in names):
                fail("E_SOURCE_IMPORT", f"{path}:{names}")
        if isinstance(node, ast.ImportFrom):
            names = [(node.module or "").split(".")[0]]
            allowed = {"__future__", "collections", "pathlib", "typing"}
            if any(name not in allowed for name in names):
                fail("E_SOURCE_IMPORT", f"{path}:{names}")
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__", "open"}:
            fail("E_SOURCE_CAPABILITY", f"{path}:{node.func.id}")
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in {"write_bytes", "write_text", "unlink", "rename", "replace", "mkdir", "rmdir", "touch"}:
                if path == VALIDATOR and node.func.attr != "replace":
                    fail("E_VALIDATOR_WRITER", node.func.attr)
                if path == BUILDER and node.func.attr in {"write_bytes", "write_text", "rename", "replace", "mkdir", "rmdir", "touch"}:
                    fail("E_BUILDER_PATH_WRITER", node.func.attr)
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                if path != VALIDATOR or node.func.attr != "run" or enclosing_function(node) != "run_git":
                    fail("E_SOURCE_SUBPROCESS", f"{path}:{node.func.attr}")

    if path == BUILDER:
        calls = [
            node.func.attr for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name) and node.func.value.id == "os"
        ]
        allowed = {"close", "fsync", "link", "open", "unlink", "write"}
        if calls.count("link") != 1 or any(name not in allowed for name in calls):
            fail("E_BUILDER_WRITER", str(calls))


def validate_source_guard() -> None:
    for path in (VALIDATOR, BUILDER):
        validate_source_text(path, result_text(path))


def matrix_bytes_expected() -> bytes:
    first = canonical_bytes(expected_matrix())
    second = canonical_bytes(expected_matrix())
    if first != second:
        fail("E_DETERMINISM")
    return first


def validate_pre_json() -> bytes:
    if (ROOT / MATRIX).exists():
        fail("E_MATRIX_EXISTS", MATRIX)
    validate_precommit_boundary()
    validate_source_guard()
    validate_controls()
    validate_status(PRE_JSON_SIX, staged=False, code="E_PRE_JSON_STATUS")
    raw = matrix_bytes_expected()
    validate_status(PRE_JSON_SIX, staged=False, code="E_PRE_JSON_STATUS_FINAL")
    return raw


def load_and_validate_matrix() -> tuple[dict[str, Any], bytes]:
    path = ROOT / MATRIX
    if not path.is_file():
        fail("E_MATRIX_MISSING", MATRIX)
    raw = path.read_bytes()
    value, _, _, _ = strict_json_loads(raw, label=MATRIX)
    if not isinstance(value, dict):
        fail("E_MATRIX_SHAPE")
    if raw != canonical_bytes(value):
        fail("E_MATRIX_CANONICAL")
    if value.get("semantic_sha256") != semantic_sha(value):
        fail("E_MATRIX_SEAL")
    expected = expected_matrix()
    if value != expected:
        fail("E_MATRIX_CONTENT")
    return value, raw


def validate_content_common(*, staged: bool) -> tuple[dict[str, Any], bytes, int]:
    if not (ROOT / MATRIX).is_file():
        fail("E_MATRIX_MISSING", MATRIX)
    validate_precommit_boundary()
    validate_status(EXACT_SEVEN, staged=staged, code="E_CONTENT_STATUS_INITIAL")
    validate_source_guard()
    validate_controls()
    matrix, raw = load_and_validate_matrix()
    tests = run_self_tests()
    validate_status(EXACT_SEVEN, staged=staged, code="E_CONTENT_STATUS_FINAL")
    return matrix, raw, tests


def parse_name_status(raw: bytes) -> dict[str, str]:
    parts = raw.split(b"\0")
    if parts[-1] != b"":
        fail("E_DIFF_PARSE")
    parts = parts[:-1]
    out: dict[str, str] = {}
    index = 0
    while index < len(parts):
        token = parts[index]
        if b"\t" in token:
            status_raw, path_raw = token.split(b"\t", 1)
            index += 1
        else:
            if index + 1 >= len(parts):
                fail("E_DIFF_PARSE")
            status_raw, path_raw = token, parts[index + 1]
            index += 2
        status = status_raw.decode("ascii", "strict")
        path = path_raw.decode("utf-8", "strict").replace("\\", "/")
        if status not in {"A", "M"} or path in out:
            fail("E_DIFF_PARSE", path)
        out[path] = status
    return out


def validate_staged_index() -> None:
    changes = parse_name_status(run_git(["diff", "--cached", "--name-status", "--no-renames", "-z"]))
    if changes != EXPECTED_STATUS:
        fail("E_STAGED_DIFF", str(changes))
    raw = run_git(["ls-files", "--stage", "-z", "--", *EXACT_SEVEN])
    entries = [item for item in raw.split(b"\0") if item]
    if len(entries) != len(EXACT_SEVEN):
        fail("E_STAGED_COUNT")
    seen: set[str] = set()
    for entry in entries:
        meta, sep, path_raw = entry.partition(b"\t")
        parts = meta.decode("ascii", "strict").split()
        path = path_raw.decode("utf-8", "strict").replace("\\", "/")
        if not sep or len(parts) != 3 or parts[0] != "100644" or parts[2] != "0" or path not in EXACT_SEVEN or path in seen:
            fail("E_STAGED_ENTRY", path)
        raw_file = (ROOT / path).read_bytes()
        if git_blob_oid(raw_file) != parts[1]:
            fail("E_STAGED_BLOB", path)
        seen.add(path)
    if seen != set(EXACT_SEVEN):
        fail("E_STAGED_ENTRY", "coverage")


def validate_commit_entries(expected_commit: str) -> None:
    raw = run_git(["ls-tree", "-l", expected_commit, "--", *EXACT_SEVEN])
    lines = raw.decode("utf-8", "strict").splitlines()
    if len(lines) != len(EXACT_SEVEN):
        fail("E_PERSISTENCE_TREE_COUNT", str(len(lines)))
    seen: set[str] = set()
    for line in lines:
        meta, sep, path = line.partition("\t")
        parts = meta.split()
        if (
            not sep or len(parts) != 4 or parts[0] != "100644"
            or parts[1] != "blob" or not is_hex40(parts[2])
            or not parts[3].isdigit() or path not in EXACT_SEVEN or path in seen
        ):
            fail("E_PERSISTENCE_TREE_ENTRY", path)
        seen.add(path)
    if seen != set(EXACT_SEVEN):
        fail("E_PERSISTENCE_TREE_ENTRY", "coverage")


def validate_persistence_boundary(expected_commit: str) -> None:
    validate_expected_commit(expected_commit)
    validate_origin_and_tip_tree()
    if parse_status():
        fail("E_PERSISTENCE_DIRTY_INITIAL")
    if git_text(["rev-parse", "--abbrev-ref", "HEAD"]) != ACTIVE_BRANCH:
        fail("E_BRANCH")
    if git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]) != UPSTREAM:
        fail("E_UPSTREAM")
    for ref in ("HEAD", TRACKING_REF, "@{upstream}"):
        if git_text(["rev-parse", ref]) != expected_commit:
            fail("E_PERSISTENCE_BOUNDARY", ref)
    if live_oid(LIVE_ACTIVE_REF) != expected_commit:
        fail("E_PERSISTENCE_LIVE")
    parents = git_text(["show", "-s", "--format=%P", expected_commit]).split()
    if parents != [EXPECTED_PARENT]:
        fail("E_PERSISTENCE_PARENT")
    if git_text(["log", "-1", "--format=%s", expected_commit]) != EXPECTED_SUBJECT:
        fail("E_PERSISTENCE_SUBJECT")
    changes = parse_name_status(run_git(["diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r", "-z", expected_commit]))
    if changes != EXPECTED_STATUS:
        fail("E_PERSISTENCE_DIFF", str(changes))
    validate_commit_entries(expected_commit)
    validate_fixed_refs()
    if parse_status():
        fail("E_PERSISTENCE_DIRTY_FINAL")


def expect_error(code: str, callback: Any) -> None:
    try:
        callback()
    except ValidationError as exc:
        if exc.code != code:
            fail("E_SELFTEST_WRONG_ERROR", f"{code}:{exc.code}")
        return
    fail("E_SELFTEST_ACCEPTED", code)


def expect_error_one_of(codes: set[str], callback: Any) -> None:
    try:
        callback()
    except ValidationError as exc:
        if exc.code not in codes:
            fail("E_SELFTEST_WRONG_ERROR", f"{sorted(codes)}:{exc.code}")
        return
    fail("E_SELFTEST_ACCEPTED", str(sorted(codes)))


def run_self_tests() -> int:
    tests = 0
    expect_error("E_JSON_DUPLICATE_KEY", lambda: strict_json_loads(b'{"a":1,"a":2}', label="self")); tests += 1
    expect_error("E_JSON_NONFINITE", lambda: strict_json_loads(b'{"a":NaN}', label="self")); tests += 1
    expect_error_one_of({"E_JSON_LIMIT", "E_JSON_PARSE"}, lambda: strict_json_loads(b"[" * 10_000 + b"0" + b"]" * 10_000, label="deep")); tests += 1
    expect_error("E_JSON_PARSE", lambda: strict_json_loads(b"1" * 10_000, label="integer")); tests += 1
    expect_error("E_EXPECTED_COMMIT", lambda: validate_expected_commit("--help")); tests += 1
    expect_error("E_GIT_ARGV", lambda: validate_git_argv(["push", "origin"])); tests += 1
    expect_error("E_GIT_ARGV", lambda: validate_git_argv(["config", "--global", "user.name"])); tests += 1
    expect_error("E_GIT_ARGV", lambda: validate_git_argv(["diff", "--output=probe"])); tests += 1
    expect_error("E_GIT_ARGV", lambda: validate_git_argv(["show", "--output=probe", TIP])); tests += 1
    expect_error("E_POINTER", lambda: ptr("S:259-285")); tests += 1
    expect_error("E_POINTER", lambda: ptr("S:L285-259")); tests += 1
    if not ptr("C67:L63").startswith(EXPECTED_PARENT + ":"):
        fail("E_SELFTEST_POINTER_COMMIT")
    tests += 1
    altered = {"schema": SCHEMA, "step": 93}
    altered["semantic_sha256"] = semantic_sha(altered)
    altered["step"] = 94
    if altered["semantic_sha256"] == semantic_sha(altered):
        fail("E_SELFTEST_SEAL")
    tests += 1
    expect_error(
        "E_SOURCE_SUBPROCESS",
        lambda: validate_source_text(VALIDATOR, "import subprocess\nsubprocess.run(['git', 'push'])\n"),
    ); tests += 1
    expect_error(
        "E_SOURCE_CAPABILITY",
        lambda: validate_source_text(BUILDER, "open('probe', 'w')\n"),
    ); tests += 1
    if len(SOURCE_PATHS) != 21 or len(SOURCE_PATHS) != len(set(SOURCE_PATHS)):
        fail("E_SELFTEST_SOURCE_DENOMINATOR")
    tests += 1
    judgments = build_judgments()
    if len(judgments) != 142:
        fail("E_SELFTEST_JUDGMENT_DENOMINATOR", str(len(judgments)))
    tests += 1
    coverage = coverage_register(judgments)
    if coverage["scientific_findings"] != 11 or len(coverage["code_named_sections"]) != 10:
        fail("E_SELFTEST_COVERAGE")
    tests += 1
    if coverage["phase054_relation_counts"] != {"CONFIRMS": 20, "CORRECTS": 5, "SUPERSEDES": 3, "UNCHANGED_OPEN": 114}:
        fail("E_SELFTEST_RELATIONS")
    tests += 1
    by_id = {row["id"]: row for row in judgments}
    required_phase67 = {
        "H44-C064": "C13", "H44-FIT-010": "C14",
        "H44-FIT-011": "C14", "H44-FIT-001": "C19",
    }
    for item_id, anchor in required_phase67.items():
        if not any(pointer.endswith(":" + anchor) for pointer in by_id[item_id]["phase067_pointers"]):
            fail("E_SELFTEST_PHASE67_MAPPING", item_id)
    tests += 1
    if set(coverage["phase067_disposition_counts"]) != PHASE67_DISPOSITIONS:
        fail("E_SELFTEST_PHASE67_DISPOSITIONS")
    tests += 1
    if any(row["phase054_relation"] == "SUPERSEDES" and not row["phase054_pointers"] for row in judgments):
        fail("E_SELFTEST_SUCCESSOR")
    tests += 1
    if len(EXACT_SEVEN) != 7 or [EXPECTED_STATUS[p] for p in EXACT_SEVEN] != ["A", "A", "A", "A", "M", "M", "M"]:
        fail("E_SELFTEST_ALLOWLIST")
    tests += 1
    if any(len(value) != 64 or any(char not in HEX for char in value) for value in CONTROL_LF_SHA256.values()):
        fail("E_SELFTEST_CONTROL_HASH_CONFIG")
    tests += 1
    return tests


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--collect", action="store_true")
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args(argv)
    if args.verify_persistence:
        if args.expected_commit is None:
            parser.error("--expected-commit is required with --verify-persistence")
        validate_expected_commit(args.expected_commit)
    elif args.expected_commit is not None:
        parser.error("--expected-commit is only valid with --verify-persistence")
    return args


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
        if args.collect:
            raw = validate_pre_json()
            print(f"PASS_P068_STEP93_COLLECT bytes={len(raw)} sha256={sha256(raw)} self_tests={run_self_tests()}")
            return 0
        if args.content_only:
            matrix, raw, tests = validate_content_common(staged=False)
            print(f"{CONTENT_TERMINAL} sources={matrix['source_totals']['source_files']} attestations={matrix['source_totals']['attestation_occurrences']} judgments={matrix['coverage_register']['judgment_rows']} bytes={len(raw)} sha256={sha256(raw)} self_tests={tests}")
            return 0
        if args.verify_staged:
            matrix, raw, tests = validate_content_common(staged=True)
            validate_staged_index()
            validate_status(EXACT_SEVEN, staged=True, code="E_STAGED_STATUS_FINAL")
            print(f"{CONTENT_TERMINAL} staged=7 judgments={matrix['coverage_register']['judgment_rows']} bytes={len(raw)} sha256={sha256(raw)} self_tests={tests}")
            return 0
        assert args.expected_commit is not None
        validate_persistence_boundary(args.expected_commit)
        validate_source_guard()
        validate_controls()
        matrix, raw = load_and_validate_matrix()
        tests = run_self_tests()
        if parse_status():
            fail("E_PERSISTENCE_DIRTY_POST_CONTENT")
        print(f"{PERSISTENCE_TERMINAL} commit={args.expected_commit} judgments={matrix['coverage_register']['judgment_rows']} bytes={len(raw)} sha256={sha256(raw)} self_tests={tests}")
        return 0
    except ValidationError as exc:
        print(f"FAIL_P068_STEP93 {exc.code} {exc.detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
