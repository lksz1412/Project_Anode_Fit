#!/usr/bin/env python3
"""Independent, fail-closed validator for Phase 061 Step 48.

The validator never imports the Step 48 builder or any Claude production/test
module.  Frozen Git blobs and persisted Step 46/47 evidence are independently
projected, while disposable builder executions are used only as a second,
byte-for-byte determinism check.
"""

from __future__ import annotations

import argparse
import ast
import copy
import difflib
import hashlib
import json
import math
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


class ValidationError(RuntimeError):
    """Controlled validation failure."""


class DuplicateKeyError(ValidationError):
    """Strict JSON duplicate-key failure."""


class NonFiniteNumberError(ValidationError):
    """Strict JSON non-finite-number failure."""


REPO = Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1020_phase061/build_phase061_step48_lineage_diff.py"
VALIDATOR = Path(__file__).resolve()
LINEAGE = REPO / "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json"
SNAPSHOT = REPO / "Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json"
RESULT = REPO / "Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
TOPOLOGY = REPO / "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
PROCESS = REPO / "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json"
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
OLD_TOPOLOGY = REPO / "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "46f17a9863b5a2ce0708524b09601930000e233f"
EXPECTED_SUBJECT = "audit(phase061): trace v1019-v1020 lineage delta"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
MAIN_BRANCH = "main"
BUILDER_SHA256 = "53fa69dd440729fcedbc5ed61c3bd56ea94de288a048cc39c249cfd548aa920a"
BUILDER_AST_SHA256 = "ac95b5855951f99d2aaffb9eaba7932ac838e397014377357dd9709635f371ed"
LINEAGE_SCHEMA_SHA256 = "21f29ba6dd62faedeeec9d0a93d251930b14be9564cdf90856a53888df37b3de"
SNAPSHOT_SCHEMA_SHA256 = "d513c3ff27db4cd4d31f91ca1b927faf707c2fb339ea13301381fabfe9e79424"
INPUT_SHA256 = {
    TOPOLOGY: "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c",
    PROCESS: "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403",
    MANIFEST: "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef",
    OLD_TOPOLOGY: "c246a05e2d13d1d33dab1682bda712611367412d241cd277694a35aaf7bcf140",
}
EXACT_EIGHT = (
    "Codex/work/v1020_phase061/build_phase061_step48_lineage_diff.py",
    "Codex/work/v1020_phase061/validate_phase061_step48.py",
    "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json",
    "Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json",
    "Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
V1020_PREFIX = "Claude/docs/v1.0.20/"
V1019_PREFIX = "Claude/docs/v1.0.19/"
TEXT_EXTENSIONS = {"md", "py", "tex", "txt", "json"}
SEMANTIC_RENAME_PAIRS = {
    "Anode_Fit_v1.0.20.py": "Anode_Fit_v1.0.19.py",
    "HANDOVER_v1.0.20.md": "HANDOVER_v1.0.19.md",
    "graphite_ica_ch1_v1.0.20.pdf": "graphite_ica_ch1_v1.0.19.pdf",
    "graphite_ica_ch1_v1.0.20.tex": "graphite_ica_ch1_v1.0.19.tex",
    "graphite_ica_ch2_v1.0.20.pdf": "graphite_ica_ch2_v1.0.19.pdf",
    "graphite_ica_ch2_v1.0.20.tex": "graphite_ica_ch2_v1.0.19.tex",
    "test_gates_v1020.py": "test_regression_v1019.py",
}
SNAPSHOT_PATHS = {
    "baseline": V1020_PREFIX + "results/snapshot_v1019_baseline.json",
    "p0": V1020_PREFIX + "results/snapshot_v1020_p0.json",
    "p2": V1020_PREFIX + "results/snapshot_v1020_p2.json",
    "p3": V1020_PREFIX + "results/snapshot_v1020_p3.json",
    "p4": V1020_PREFIX + "results/snapshot_v1020_p4.json",
    "p5": V1020_PREFIX + "results/snapshot_v1020_p5.json",
    "p6": V1020_PREFIX + "results/snapshot_v1020_p6.json",
    "p7": V1020_PREFIX + "results/snapshot_v1020_p7.json",
    "p7b": V1020_PREFIX + "results/snapshot_v1020_p7b.json",
    "final": V1020_PREFIX + "results/snapshot_v1020_final.json",
}
SNAPSHOT_ORDER = tuple(SNAPSHOT_PATHS)
CLASS_COUNTS = {"ADDED": 178, "MODIFIED": 29, "UNCHANGED": 18, "RENAMED": 7, "COPIED": 0}
P5_P6_CHANGED_TEX = [
    V1020_PREFIX + "_sections/ch1_appB_codemap.tex",
    V1020_PREFIX + "_sections/ch1_sec00_intro.tex",
    V1020_PREFIX + "appendix_phase_separation.tex",
]

NEGATIVE_CONTROL_IDS = (
    "lineage-drop-source", "lineage-duplicate-source", "lineage-source-id-swap",
    "lineage-wrong-pair", "lineage-missing-old-blob", "lineage-missing-new-blob",
    "lineage-false-unchanged", "lineage-false-added", "lineage-false-renamed",
    "lineage-false-copied", "lineage-drop-deleted", "lineage-duplicate-deleted",
    "lineage-old-coverage", "lineage-new-coverage", "lineage-pair-count",
    "lineage-class-count", "lineage-path-relation", "lineage-blob-relation",
    "lineage-hunk-hash", "lineage-hunk-range", "lineage-hunk-content",
    "lineage-bib-delta", "lineage-label-delta", "lineage-equation-delta",
    "lineage-bracket-display-escape",
    "lineage-include-delta", "lineage-pdf-pages", "lineage-code-ast",
    "lineage-test-ast", "lineage-code-execution-promotion", "lineage-science-promotion",
    "snapshot-drop-occurrence", "snapshot-duplicate-occurrence", "snapshot-path-swap",
    "snapshot-blob-swap", "snapshot-sha-swap", "snapshot-root-schema",
    "snapshot-chapter-schema", "snapshot-label-duplicate", "snapshot-bib-duplicate",
    "snapshot-eqblock-schema", "snapshot-drop-edge", "snapshot-duplicate-edge",
    "snapshot-edge-order", "snapshot-edge-endpoint", "snapshot-edge-projection",
    "snapshot-p5-p6-path-collapse", "snapshot-p5-p6-blob-divergence",
    "snapshot-p5-p6-source-tree-equality", "snapshot-appendix-prefinal-promotion",
    "snapshot-appendix-final-removal", "snapshot-ch1-count", "snapshot-ch2-count",
    "snapshot-equation-hash-science-promotion", "snapshot-generated-source-inversion",
    "snapshot-structural-science-promotion", "snapshot-external-truth-promotion",
    "cross-generation-contract", "cross-input-hash", "cross-baseline-commit",
    "cross-topology-link", "cross-process-link", "cross-source-count",
    "cross-snapshot-count", "cross-authority-boundary", "cross-unverified-boundary",
)

CONTROL_DIAGNOSTIC = {
    "lineage-drop-source": "LINEAGE_SOURCE_COVERAGE",
    "lineage-duplicate-source": "LINEAGE_SOURCE_COVERAGE",
    "lineage-source-id-swap": "LINEAGE_SOURCE_IDENTITY",
    "lineage-wrong-pair": "LINEAGE_PAIRING",
    "lineage-missing-old-blob": "LINEAGE_ENDPOINT_BLOB",
    "lineage-missing-new-blob": "LINEAGE_ENDPOINT_BLOB",
    "lineage-false-unchanged": "LINEAGE_CLASSIFICATION",
    "lineage-false-added": "LINEAGE_CLASSIFICATION",
    "lineage-false-renamed": "LINEAGE_CLASSIFICATION",
    "lineage-false-copied": "LINEAGE_CLASSIFICATION",
    "lineage-drop-deleted": "LINEAGE_DELETED_COVERAGE",
    "lineage-duplicate-deleted": "LINEAGE_DELETED_COVERAGE",
    "lineage-old-coverage": "LINEAGE_DELETED_COVERAGE",
    "lineage-new-coverage": "LINEAGE_SOURCE_COVERAGE",
    "lineage-pair-count": "LINEAGE_PAIR_COUNT",
    "lineage-class-count": "LINEAGE_CLASS_COUNTS",
    "lineage-path-relation": "LINEAGE_PATH_RELATION",
    "lineage-blob-relation": "LINEAGE_BLOB_RELATION",
    "lineage-hunk-hash": "LINEAGE_TEXT_HUNKS",
    "lineage-hunk-range": "LINEAGE_TEXT_HUNKS",
    "lineage-hunk-content": "LINEAGE_TEXT_HUNKS",
    "lineage-bib-delta": "LINEAGE_LATEX_BIBLIOGRAPHY",
    "lineage-label-delta": "LINEAGE_LATEX_LABELS",
    "lineage-equation-delta": "LINEAGE_LATEX_EQUATIONS",
    "lineage-bracket-display-escape": "LINEAGE_LATEX_EQUATIONS",
    "lineage-include-delta": "LINEAGE_LATEX_INCLUDES",
    "lineage-pdf-pages": "LINEAGE_PDF_PAGES",
    "lineage-code-ast": "LINEAGE_CODE_AST",
    "lineage-test-ast": "LINEAGE_TEST_AST",
    "lineage-code-execution-promotion": "RUNTIME_PROMOTION",
    "lineage-science-promotion": "AUTHORITY_PROMOTION",
    "snapshot-drop-occurrence": "SNAPSHOT_OCCURRENCE_COVERAGE",
    "snapshot-duplicate-occurrence": "SNAPSHOT_OCCURRENCE_COVERAGE",
    "snapshot-path-swap": "SNAPSHOT_PATH_IDENTITY",
    "snapshot-blob-swap": "SNAPSHOT_BLOB_IDENTITY",
    "snapshot-sha-swap": "SNAPSHOT_BLOB_IDENTITY",
    "snapshot-root-schema": "SNAPSHOT_ROOT_PROJECTION",
    "snapshot-chapter-schema": "SNAPSHOT_CHAPTER_PROJECTION",
    "snapshot-label-duplicate": "SNAPSHOT_LABEL_SCHEMA",
    "snapshot-bib-duplicate": "SNAPSHOT_BIB_SCHEMA",
    "snapshot-eqblock-schema": "SNAPSHOT_EQBLOCK_SCHEMA",
    "snapshot-drop-edge": "SNAPSHOT_EDGE_COVERAGE",
    "snapshot-duplicate-edge": "SNAPSHOT_EDGE_COVERAGE",
    "snapshot-edge-order": "SNAPSHOT_EDGE_ORDER",
    "snapshot-edge-endpoint": "SNAPSHOT_EDGE_ENDPOINT",
    "snapshot-edge-projection": "SNAPSHOT_EDGE_PROJECTION",
    "snapshot-p5-p6-path-collapse": "P5_P6_OCCURRENCE_COLLAPSE",
    "snapshot-p5-p6-blob-divergence": "P5_P6_BLOB_DIVERGENCE",
    "snapshot-p5-p6-source-tree-equality": "P5_P6_SOURCE_EQUALITY_FALSE",
    "snapshot-appendix-prefinal-promotion": "APPENDIX_PREFINAL_HISTORY_FALSE",
    "snapshot-appendix-final-removal": "APPENDIX_FINAL_ROOT",
    "snapshot-ch1-count": "SNAPSHOT_CH1_DELTA",
    "snapshot-ch2-count": "SNAPSHOT_CH2_DELTA",
    "snapshot-equation-hash-science-promotion": "AUTHORITY_PROMOTION",
    "snapshot-generated-source-inversion": "AUTHORITY_PROMOTION",
    "snapshot-structural-science-promotion": "AUTHORITY_PROMOTION",
    "snapshot-external-truth-promotion": "AUTHORITY_PROMOTION",
    "cross-generation-contract": "CROSS_GENERATION_CONTRACT",
    "cross-input-hash": "CROSS_INPUT_HASH",
    "cross-baseline-commit": "CROSS_BASELINE_COMMIT",
    "cross-topology-link": "CROSS_TOPOLOGY_LINK",
    "cross-process-link": "CROSS_PROCESS_LINK",
    "cross-source-count": "CROSS_SOURCE_COUNT",
    "cross-snapshot-count": "CROSS_SNAPSHOT_COUNT",
    "cross-authority-boundary": "AUTHORITY_BOUNDARY",
    "cross-unverified-boundary": "UNVERIFIED_BOUNDARY",
}

DISPLAY_RE = re.compile(
    r"\\begin\{(?P<env>(?:equation|align|gather|multline|eqnarray|displaymath)\*?)\}"
    r"(?P<body>.*?)\\end\{(?P=env)\}", re.DOTALL,
)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}")
INCLUDE_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")
_UNSET = object()


def _reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def compact_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def walk_json(value: Any, depth: int = 1) -> tuple[int, int]:
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return 1, depth
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NonFiniteNumberError(str(value))
        return 1, depth
    if isinstance(value, list):
        children = [walk_json(item, depth + 1) for item in value]
    elif isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ValidationError("JSON_NONSTRING_KEY")
        children = [walk_json(item, depth + 1) for item in value.values()]
    else:
        raise ValidationError(f"JSON_TYPE:{type(value).__name__}")
    return 1 + sum(row[0] for row in children), max([depth, *(row[1] for row in children)])


def strict_load_bytes(data: bytes) -> Any:
    value = json.loads(data.decode("utf-8"), object_pairs_hook=_object_pairs, parse_constant=_reject_constant)
    walk_json(value)
    return value


def strict_load(path: Path) -> Any:
    return strict_load_bytes(path.read_bytes())


def schema_sha(value: Any) -> str:
    rows: set[tuple[str, str, tuple[str, ...] | None]] = set()
    stack = [("$", value)]
    while stack:
        path, item = stack.pop()
        if item is None:
            kind = "null"
        elif isinstance(item, bool):
            kind = "bool"
        elif isinstance(item, int):
            kind = "int"
        elif isinstance(item, float):
            kind = "float"
        elif isinstance(item, str):
            kind = "str"
        elif isinstance(item, list):
            kind = "list"
        elif isinstance(item, dict):
            kind = "dict"
        else:
            raise ValidationError("SCHEMA_TYPE")
        rows.add((path, kind, tuple(sorted(item)) if isinstance(item, dict) else None))
        if isinstance(item, dict):
            stack.extend((path + "." + key, child) for key, child in item.items())
        elif isinstance(item, list):
            stack.extend((path + "[]", child) for child in item)
    return sha256(json.dumps(sorted(rows), ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def canonical_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {
            "_type": type(value).__name__,
            **{
                field: canonical_ast(getattr(value, field))
                for field in value._fields
                if getattr(value, field, None) not in (None, [])
            },
        }
    if isinstance(value, (list, tuple)):
        return [canonical_ast(item) for item in value]
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if value is Ellipsis:
        return {"_ellipsis": True}
    if isinstance(value, complex):
        return {"_complex_repr": repr(value)}
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(str(value))
    return value


def builder_security_diagnostics(data: bytes) -> set[str]:
    try:
        tree = ast.parse(lf_bytes(data).decode("utf-8"))
        projection = sha256(compact_bytes(canonical_ast(tree)))
    except (SyntaxError, UnicodeError, ValidationError):
        return {"BUILDER_AST_POLICY"}
    if projection != BUILDER_AST_SHA256:
        return {"BUILDER_AST_POLICY"}
    expected_imports = {
        "__future__", "argparse", "ast", "difflib", "hashlib", "json", "math", "re",
        "subprocess", "sys", "pathlib", "typing",
    }
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").split(".")[0])
    if imports != expected_imports:
        return {"BUILDER_AST_POLICY"}
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    subprocess_calls = [
        node for node in calls
        if isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess" and node.func.attr == "run"
    ]
    if len(subprocess_calls) != 2:
        return {"BUILDER_AST_POLICY"}
    forbidden_names = {"exec", "eval", "compile", "__import__", "globals", "locals"}
    if any(isinstance(node, ast.Name) and node.id in forbidden_names for node in ast.walk(tree)):
        return {"BUILDER_AST_POLICY"}
    text = lf_bytes(data).decode("utf-8")
    if any(token in text for token in ("shell=True", "executable=", "git clean", "git reset", "git checkout")):
        return {"BUILDER_AST_POLICY"}
    if sha256(lf_bytes(data)) != BUILDER_SHA256:
        return {"BUILDER_FIXED_HASH_MISMATCH"}
    return set()


def run_git_bytes(args: list[str], code: str, timeout: int = 60) -> bytes:
    try:
        completed = subprocess.run(
            ["git", *args], cwd=REPO, check=False, capture_output=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"{code}_TIMEOUT") from exc
    if completed.returncode != 0:
        raise ValidationError(f"{code}:{completed.returncode}")
    return completed.stdout


def run_git_text(args: list[str], code: str, timeout: int = 60) -> str:
    return run_git_bytes(args, code, timeout).decode("utf-8").strip()


def git_blobs(shas: list[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(shas))
    try:
        completed = subprocess.run(
            ["git", "cat-file", "--batch"], cwd=REPO,
            input=("\n".join(ordered) + "\n").encode("ascii"),
            check=False, capture_output=True, timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError("GIT_CAT_FILE_TIMEOUT") from exc
    if completed.returncode != 0:
        raise ValidationError("GIT_CAT_FILE")
    offset = 0
    result: dict[str, bytes] = {}
    for expected in ordered:
        newline = completed.stdout.find(b"\n", offset)
        if newline < 0:
            raise ValidationError("GIT_CAT_FILE_HEADER")
        header = completed.stdout[offset:newline].decode("ascii")
        offset = newline + 1
        parts = header.split()
        if len(parts) != 3 or parts[0] != expected or parts[1] != "blob":
            raise ValidationError("GIT_CAT_FILE_HEADER")
        size = int(parts[2])
        data = completed.stdout[offset:offset + size]
        offset += size
        if completed.stdout[offset:offset + 1] != b"\n" or blob_sha1(data) != expected:
            raise ValidationError("GIT_BLOB_IDENTITY")
        offset += 1
        result[expected] = data
    if completed.stdout[offset:]:
        raise ValidationError("GIT_CAT_FILE_TRAILING")
    return result


def suffix(path: str, prefix: str) -> str:
    if not path.startswith(prefix):
        raise ValidationError("PATH_PREFIX")
    return path[len(prefix):]


def normalized_identity(relative: str, role: str) -> dict[str, Any]:
    neutral = relative
    for new_name, old_name in SEMANTIC_RENAME_PAIRS.items():
        if relative in {new_name, old_name}:
            neutral = new_name
            break
    parts = Path(neutral).parts
    filename = parts[-1]
    if filename.startswith("ch1_") or "_ch1_" in filename or filename.startswith("graphite_ica_ch1_"):
        chapter = "CH1"
    elif filename.startswith("ch2_") or "_ch2_" in filename or filename.startswith("graphite_ica_ch2_"):
        chapter = "CH2"
    elif filename.startswith("appendix_phase_separation"):
        chapter = "STANDALONE_APPENDIX"
    else:
        chapter = "NON_CHAPTER"
    if filename.endswith(".tex"):
        form = "LATEX_SOURCE"
    elif filename.endswith(".pdf"):
        form = "GENERATED_PDF"
    elif filename.endswith(".py"):
        form = "PYTHON_SOURCE"
    elif filename.endswith(".png"):
        form = "RASTER_IMAGE"
    else:
        form = "TEXT_OR_STRUCTURED_RECORD"
    family = "/".join(parts[:-1]) or "ROOT"
    return {
        "role": role, "document_family": family, "chapter": chapter,
        "section_or_artifact": filename, "artifact_form": form,
        "version_neutral_key": f"{role}|{family}|{chapter}|{filename}|{form}",
        "basename_only": False,
    }


def text_record(data: bytes) -> dict[str, Any]:
    normalized = lf_bytes(data)
    text = normalized.decode("utf-8")
    return {
        "sha256_lf_normalized": sha256(normalized),
        "physical_lines": len(normalized.splitlines()),
        "nonblank_lines": sum(bool(line.strip()) for line in text.splitlines()),
        "trailing_newline": normalized.endswith(b"\n"),
    }


def exact_text_delta(old: bytes, new: bytes) -> dict[str, Any]:
    old_lines = lf_bytes(old).decode("utf-8").splitlines()
    new_lines = lf_bytes(new).decode("utf-8").splitlines()
    segments: list[dict[str, Any]] = []
    for tag, old_start, old_end, new_start, new_end in difflib.SequenceMatcher(
        None, old_lines, new_lines, autojunk=False,
    ).get_opcodes():
        if tag == "equal":
            continue
        segment = {
            "tag": tag, "old_line_start": old_start + 1, "old_line_end": old_end,
            "new_line_start": new_start + 1, "new_line_end": new_end,
            "old_lines": old_lines[old_start:old_end], "new_lines": new_lines[new_start:new_end],
        }
        segment["segment_sha256"] = sha256(pretty_bytes(segment))
        segments.append(segment)
    return {
        "old": text_record(old), "new": text_record(new), "segments": segments,
        "segment_count": len(segments),
        "changed_old_lines": sum(len(row["old_lines"]) for row in segments),
        "changed_new_lines": sum(len(row["new_lines"]) for row in segments),
        "exact_reconstruction_boundary": "CHANGED_SEGMENTS_PLUS_ENDPOINT_BLOBS",
    }


def latex_without_comments(text: str) -> str:
    return "\n".join(re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines())


def bracket_display_spans(text: str) -> list[tuple[int, str]]:
    commands: list[tuple[int, str]] = []
    for index, char in enumerate(text):
        if char not in "[]":
            continue
        preceding = 0
        cursor = index - 1
        while cursor >= 0 and text[cursor] == "\\":
            preceding += 1
            cursor -= 1
        if preceding % 2 == 1:
            commands.append((index - 1, char))
    spans: list[tuple[int, str]] = []
    start: int | None = None
    for command_start, bracket in commands:
        if bracket == "[" and start is None:
            start = command_start
        elif bracket == "]" and start is not None:
            spans.append((start, text[start:command_start + 2]))
            start = None
    return spans


def latex_equations(text: str) -> list[dict[str, Any]]:
    text = latex_without_comments(text)
    matches: list[tuple[int, str, str]] = []
    for match in DISPLAY_RE.finditer(text):
        matches.append((match.start(), match.group("env"), match.group(0)))
    for start, raw in bracket_display_spans(text):
        matches.append((start, "bracket_display", raw))
    provisional: list[dict[str, Any]] = []
    for ordinal, (start, environment, raw) in enumerate(sorted(matches), start=1):
        labels = LABEL_RE.findall(raw)
        substantive = re.sub(r"\s+", " ", raw).strip()
        body_hash = sha256(substantive.encode("utf-8"))
        base = "LABEL:" + "|".join(labels) if labels else "UNLABELED_HASH:" + body_hash
        provisional.append({
            "ordinal": ordinal, "environment": environment,
            "line_start": text.count("\n", 0, start) + 1, "labels": labels,
            "sha256_lf_normalized": sha256(lf_bytes(raw.encode("utf-8"))),
            "substantive_sha256": body_hash, "base_identity": base,
        })
    totals = Counter(row["base_identity"] for row in provisional)
    seen: Counter[str] = Counter()
    result = []
    for row in provisional:
        base = row.pop("base_identity")
        seen[base] += 1
        row["semantic_identity"] = base if totals[base] == 1 else f"{base}#OCCURRENCE-{seen[base]:03d}"
        result.append(row)
    return result


def bibliography_records(text: str) -> dict[str, dict[str, Any]]:
    matches = list(BIBITEM_RE.finditer(text))
    result: dict[str, dict[str, Any]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        key = match.group(1)
        if key in result:
            raise ValidationError("LATEX_DUPLICATE_BIBITEM")
        raw = text[match.start():end].rstrip()
        result[key] = {
            "line_start": text.count("\n", 0, match.start()) + 1,
            "sha256_lf_normalized": sha256(lf_bytes(raw.encode("utf-8"))),
        }
    return result


def keyed_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        "added": [{"key": key, "after": after[key]} for key in sorted(set(after) - set(before))],
        "removed": [{"key": key, "before": before[key]} for key in sorted(set(before) - set(after))],
        "changed": [
            {"key": key, "before": before[key], "after": after[key]}
            for key in sorted(set(before) & set(after)) if before[key] != after[key]
        ],
        "unchanged_count": sum(before[key] == after[key] for key in set(before) & set(after)),
    }


def equation_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    shared = sorted(set(before) & set(after))
    fields = ("environment", "labels", "sha256_lf_normalized", "substantive_sha256")
    changed, moved, unchanged = [], [], []
    for key in shared:
        if any(before[key][field] != after[key][field] for field in fields):
            changed.append({"key": key, "before": before[key], "after": after[key]})
        elif before[key]["ordinal"] != after[key]["ordinal"] or before[key]["line_start"] != after[key]["line_start"]:
            moved.append({"key": key, "before": before[key], "after": after[key]})
        else:
            unchanged.append(key)
    return {
        "added": [{"key": key, "after": after[key]} for key in sorted(set(after) - set(before))],
        "removed": [{"key": key, "before": before[key]} for key in sorted(set(before) - set(after))],
        "changed": changed, "moved": moved, "unchanged_count": len(unchanged),
        "unchanged_projection_sha256": sha256(pretty_bytes(unchanged)),
    }


def latex_delta(old: bytes, new: bytes) -> dict[str, Any]:
    old_text = latex_without_comments(lf_bytes(old).decode("utf-8"))
    new_text = latex_without_comments(lf_bytes(new).decode("utf-8"))
    old_rows, new_rows = latex_equations(old_text), latex_equations(new_text)
    old_eq = {row["semantic_identity"]: row for row in old_rows}
    new_eq = {row["semantic_identity"]: row for row in new_rows}
    if len(old_eq) != len(old_rows) or len(new_eq) != len(new_rows):
        raise ValidationError("LATEX_EQUATION_IDENTITY")
    old_labels, new_labels = set(LABEL_RE.findall(old_text)), set(LABEL_RE.findall(new_text))
    old_includes, new_includes = INCLUDE_RE.findall(old_text), INCLUDE_RE.findall(new_text)
    return {
        "labels": {"before": len(old_labels), "after": len(new_labels),
                   "added": sorted(new_labels - old_labels), "removed": sorted(old_labels - new_labels)},
        "equation_blocks_by_semantic_identity": equation_delta(old_eq, new_eq),
        "bibliography": keyed_delta(bibliography_records(old_text), bibliography_records(new_text)),
        "include_topology": {"before": old_includes, "after": new_includes,
                             "added": sorted(set(new_includes) - set(old_includes)),
                             "removed": sorted(set(old_includes) - set(new_includes))},
    }


def stable_ast_projection(value: Any) -> Any:
    return canonical_ast(value)


def stable_ast_sha(node: ast.AST) -> str:
    return sha256(pretty_bytes(stable_ast_projection(node)))


class DefinitionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.stack: list[str] = []
        self.records: dict[str, str] = {}

    def _visit(self, node: ast.AST, name: str) -> None:
        qualified = ".".join((*self.stack, name))
        self.records[qualified] = stable_ast_sha(node)
        self.stack.append(name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit(node, node.name)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit(node, node.name)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit(node, node.name)


def python_structure_delta(old: bytes, new: bytes) -> dict[str, Any]:
    old_tree, new_tree = ast.parse(old.decode("utf-8")), ast.parse(new.decode("utf-8"))
    old_visitor, new_visitor = DefinitionVisitor(), DefinitionVisitor()
    old_visitor.visit(old_tree)
    new_visitor.visit(new_tree)
    old_defs, new_defs = old_visitor.records, new_visitor.records

    def stats(tree: ast.AST) -> dict[str, Any]:
        nodes = list(ast.walk(tree))
        imports = sorted(
            alias.name for node in nodes if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        )
        return {
            "ast_nodes": len(nodes), "imports": imports,
            "calls": sum(isinstance(node, ast.Call) for node in nodes),
            "executable_literals": sum(
                isinstance(node, ast.Constant) and not isinstance(node.value, (type(None), bool))
                for node in nodes
            ),
        }

    old_ast, new_ast = stable_ast_sha(old_tree), stable_ast_sha(new_tree)
    return {
        "old_module_ast_sha256": old_ast, "new_module_ast_sha256": new_ast,
        "ast_projection_contract": "NONEMPTY_FIELDS_CANONICAL_JSON_V1",
        "module_ast_identical": old_ast == new_ast,
        "definitions_before": len(old_defs), "definitions_after": len(new_defs),
        "added_definitions": sorted(set(new_defs) - set(old_defs)),
        "removed_definitions": sorted(set(old_defs) - set(new_defs)),
        "changed_definitions": sorted(key for key in set(old_defs) & set(new_defs) if old_defs[key] != new_defs[key]),
        "unchanged_definitions": sorted(key for key in set(old_defs) & set(new_defs) if old_defs[key] == new_defs[key]),
        "old_structure_stats": stats(old_tree), "new_structure_stats": stats(new_tree),
        "execution_performed": False,
        "behavioral_change_state": "UNVERIFIED_NO_RUNTIME_EXECUTION",
        "authority_ceiling": "FROZEN_SOURCE_STRUCTURE_ONLY_NOT_RUNTIME_BEHAVIOR",
    }


def validate_snapshot_source(value: Any, alias: str) -> dict[str, Any]:
    if not isinstance(value, dict) or len(value) not in {2, 3}:
        raise ValidationError(f"SNAPSHOT_SOURCE_ROOT:{alias}")
    for root, chapter in value.items():
        if not isinstance(root, str) or not isinstance(chapter, dict):
            raise ValidationError(f"SNAPSHOT_SOURCE_ROOT_TYPE:{alias}")
        if set(chapter) != {"labels", "eqblocks", "asset_unique", "bibitems"}:
            raise ValidationError(f"SNAPSHOT_SOURCE_CHAPTER_FIELDS:{alias}")
        if (
            not isinstance(chapter["labels"], list)
            or any(not isinstance(item, str) for item in chapter["labels"])
            or len(chapter["labels"]) != len(set(chapter["labels"]))
            or not isinstance(chapter["bibitems"], list)
            or any(not isinstance(item, str) for item in chapter["bibitems"])
            or len(chapter["bibitems"]) != len(set(chapter["bibitems"]))
            or not isinstance(chapter["asset_unique"], int)
            or isinstance(chapter["asset_unique"], bool)
            or not isinstance(chapter["eqblocks"], dict)
        ):
            raise ValidationError(f"SNAPSHOT_SOURCE_CHAPTER_TYPE:{alias}")
        for key, block in chapter["eqblocks"].items():
            if (
                not isinstance(key, str) or not isinstance(block, dict)
                or set(block) != {"hash", "boxed", "file"}
                or not isinstance(block["hash"], str)
                or not isinstance(block["boxed"], bool)
                or not isinstance(block["file"], str)
            ):
                raise ValidationError(f"SNAPSHOT_SOURCE_EQBLOCK:{alias}")
    return value


def snapshot_chapter(value: dict[str, Any], chapter: int) -> dict[str, Any]:
    matches = [row for key, row in value.items() if f"_ch{chapter}_" in key]
    if len(matches) != 1:
        raise ValidationError(f"SNAPSHOT_CHAPTER_CARDINALITY:{chapter}")
    return matches[0]


def chapter_projection(chapter: dict[str, Any]) -> dict[str, Any]:
    return {
        "labels": sorted(chapter["labels"]),
        "eqblocks": [{"identifier": key, **value} for key, value in sorted(chapter["eqblocks"].items())],
        "asset_unique": chapter["asset_unique"],
        "bibitems": sorted(chapter["bibitems"]),
    }


def normalized_snapshot_root(root: str) -> str:
    return root.replace("v1.0.19", "VERSION").replace("v1.0.20", "VERSION")


def document_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    roots = [
        {
            "raw_root_name": root,
            "normalized_root_name": normalized_snapshot_root(root),
            "content": chapter_projection(chapter),
        }
        for root, chapter in sorted(snapshot.items())
    ]
    return {
        "raw_roots": sorted(snapshot),
        "normalized_roots": sorted(normalized_snapshot_root(root) for root in snapshot),
        "all_root_projections": roots,
        "ch1": chapter_projection(snapshot_chapter(snapshot, 1)),
        "ch2": chapter_projection(snapshot_chapter(snapshot, 2)),
    }


def set_delta(before: list[str], after: list[str]) -> dict[str, Any]:
    return {
        "count_before": len(before), "count_after": len(after),
        "count_delta": len(after) - len(before),
        "added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
    }


def snapshot_eq_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    old = {row["identifier"]: {key: row[key] for key in ("hash", "boxed", "file")} for row in before["eqblocks"]}
    new = {row["identifier"]: {key: row[key] for key in ("hash", "boxed", "file")} for row in after["eqblocks"]}
    substantive_old = sorted(old.values(), key=lambda row: (row["hash"], row["boxed"], row["file"]))
    substantive_new = sorted(new.values(), key=lambda row: (row["hash"], row["boxed"], row["file"]))
    return {
        "count_before": len(old), "count_after": len(new),
        "added": [{"identifier": key, **new[key]} for key in sorted(set(new) - set(old))],
        "removed": [{"identifier": key, **old[key]} for key in sorted(set(old) - set(new))],
        "changed": [
            {"identifier": key, "before": old[key], "after": new[key]}
            for key in sorted(set(old) & set(new)) if old[key] != new[key]
        ],
        "substantive_projection_equal": substantive_old == substantive_new,
        "substantive_before_sha256": sha256(pretty_bytes(substantive_old)),
        "substantive_after_sha256": sha256(pretty_bytes(substantive_new)),
    }


def snapshot_edge(before_alias: str, after_alias: str, projections: dict[str, dict[str, Any]]) -> dict[str, Any]:
    before, after = projections[before_alias], projections[after_alias]
    chapters = {
        chapter: {
            "labels": set_delta(before[chapter]["labels"], after[chapter]["labels"]),
            "eqblocks": snapshot_eq_delta(before[chapter], after[chapter]),
            "bibitems": set_delta(before[chapter]["bibitems"], after[chapter]["bibitems"]),
            "asset_unique_before": before[chapter]["asset_unique"],
            "asset_unique_after": after[chapter]["asset_unique"],
        }
        for chapter in ("ch1", "ch2")
    }
    normalized_before = {
        "normalized_roots": before["normalized_roots"], "ch1": before["ch1"], "ch2": before["ch2"],
        "extra_roots": [
            row for row in before["all_root_projections"]
            if row["normalized_root_name"] not in {"graphite_ica_ch1_VERSION.tex", "graphite_ica_ch2_VERSION.tex"}
        ],
    }
    normalized_after = {
        "normalized_roots": after["normalized_roots"], "ch1": after["ch1"], "ch2": after["ch2"],
        "extra_roots": [
            row for row in after["all_root_projections"]
            if row["normalized_root_name"] not in {"graphite_ica_ch1_VERSION.tex", "graphite_ica_ch2_VERSION.tex"}
        ],
    }
    return {
        "edge_id": f"P061-SNAP-EDGE-{SNAPSHOT_ORDER.index(before_alias) + 1:02d}",
        "before_alias": before_alias, "after_alias": after_alias,
        "before_projection_sha256": sha256(pretty_bytes(before)),
        "after_projection_sha256": sha256(pretty_bytes(after)),
        "document_projection_equal": normalized_before == normalized_after,
        "raw_root_delta": set_delta(before["raw_roots"], after["raw_roots"]),
        "normalized_root_delta": set_delta(before["normalized_roots"], after["normalized_roots"]),
        "chapters": chapters, "authority_ceiling": "CAPTURED_STRUCTURE_ONLY",
        "external_scientific_truth": False,
    }


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    parsed = []
    for path, expected_hash in INPUT_SHA256.items():
        data = path.read_bytes()
        if sha256(lf_bytes(data)) != expected_hash:
            raise ValidationError(f"INPUT_FIXED_HASH:{path.name}")
        parsed.append(strict_load_bytes(data))
    return tuple(parsed)  # type: ignore[return-value]


def independent_expected() -> dict[str, Any]:
    topology, process, manifest, old_topology = load_inputs()
    if topology.get("baseline_commit") != BASELINE or process.get("baseline_commit") != BASELINE:
        raise ValidationError("INPUT_BASELINE")
    sources = topology.get("sources")
    routes = process.get("source_routes")
    entries = manifest.get("entries")
    if not isinstance(sources, list) or len(sources) != 232:
        raise ValidationError("INPUT_SOURCE_COUNT")
    if not isinstance(routes, list) or len(routes) != 232 or not isinstance(entries, list):
        raise ValidationError("INPUT_ROUTE_MANIFEST")
    route_by_id = {row["source_id"]: row for row in routes}
    if len(route_by_id) != 232:
        raise ValidationError("INPUT_ROUTE_DUPLICATE")
    old_entries = [row for row in entries if row.get("version") == "v1.0.19"]
    new_entries = [row for row in entries if row.get("version") == "v1.0.20"]
    if len(old_entries) != 66 or len(new_entries) != 232:
        raise ValidationError("INPUT_MANIFEST_COUNTS")
    old_primary = [row for row in old_topology.get("sources", []) if row.get("occurrence_kind") == "PRIMARY_RELEASE"]
    if len(old_primary) != 66:
        raise ValidationError("INPUT_OLD_TOPOLOGY_COUNT")
    old_topology_by_path = {row["path"]: row for row in old_primary}
    old_by_relative = {suffix(row["path"], V1019_PREFIX): row for row in old_entries}
    new_manifest_by_path = {row["path"]: row for row in new_entries}
    if len(old_topology_by_path) != 66 or len(old_by_relative) != 66 or len(new_manifest_by_path) != 232:
        raise ValidationError("INPUT_PATH_DUPLICATE")
    for source in sources:
        route = route_by_id.get(source["source_id"])
        manifest_row = new_manifest_by_path.get(source["path"])
        if (
            route is None or route["path"] != source["path"] or route["blob_sha1"] != source["blob_sha1"]
            or manifest_row is None or manifest_row["blob_sha"] != source["blob_sha1"]
        ):
            raise ValidationError("INPUT_CROSS_LINK")
    for row in old_entries:
        topology_row = old_topology_by_path.get(row["path"])
        if topology_row is None or topology_row["git_blob_sha1"] != row["blob_sha"]:
            raise ValidationError("INPUT_OLD_CROSS_LINK")

    blobs = git_blobs([row["blob_sha"] for row in old_entries] + [row["blob_sha1"] for row in sources])
    used_old: set[str] = set()
    expected_rows: list[dict[str, Any]] = []
    class_counts: Counter[str] = Counter()
    python_pairs: list[dict[str, Any]] = []
    for source in sources:
        relative = suffix(source["path"], V1020_PREFIX)
        if relative in old_by_relative:
            old_relative, basis = relative, "FULL_VERSION_RELATIVE_PATH"
        elif relative in SEMANTIC_RENAME_PAIRS:
            old_relative, basis = SEMANTIC_RENAME_PAIRS[relative], "VERSIONED_ROLE_CHAPTER_SECTION_IDENTITY"
        else:
            old_relative, basis = None, "NO_V1019_COUNTERPART"
        old = old_by_relative.get(old_relative) if old_relative is not None else None
        new_data = blobs[source["blob_sha1"]]
        if blob_sha1(new_data) != source["blob_sha1"] or sha256(new_data) != source["sha256"] or len(new_data) != source["size_bytes"]:
            raise ValidationError("INPUT_NEW_BLOB")
        new_identity = normalized_identity(relative, source["manifest_role"])
        old_identity = None if old is None else normalized_identity(suffix(old["path"], V1019_PREFIX), old["role"])
        if old_identity is not None and old_identity["version_neutral_key"] != new_identity["version_neutral_key"]:
            raise ValidationError("INPUT_NORMALIZED_IDENTITY")
        if old is None:
            comparison, path_relation, blob_relation = "ADDED", "ADDED", "NO_OLD_BLOB"
        else:
            if old["path"] in used_old:
                raise ValidationError("INPUT_PAIR_REUSE")
            used_old.add(old["path"])
            if old_relative != relative:
                comparison, path_relation = "RENAMED", "RENAMED_VERSIONED_IDENTITY"
            elif old["blob_sha"] == source["blob_sha1"]:
                comparison, path_relation = "UNCHANGED", "SAME_RELATIVE_PATH"
            else:
                comparison, path_relation = "MODIFIED", "SAME_RELATIVE_PATH"
            blob_relation = "IDENTICAL" if old["blob_sha"] == source["blob_sha1"] else "CHANGED"
        class_counts[comparison] += 1
        old_data = None if old is None else blobs[old["blob_sha"]]
        extension = source["extension"]
        row = {
            "delta_id": f"P061-DELTA-{int(source['source_id'].rsplit('-', 1)[1]):04d}",
            "v1020_source_id": source["source_id"], "manifest_index_v1020": source["manifest_index_v1020"],
            "comparison_class": comparison, "pair_basis": basis,
            "normalized_identity": new_identity, "old_normalized_identity": old_identity,
            "candidate_count": 0 if old is None else 1,
            "selected_reason": "NO_NORMALIZED_IDENTITY_CANDIDATE" if old is None else basis,
            "path_relation": path_relation, "blob_relation": blob_relation,
            "v1019": None if old is None else {
                "path": old["path"], "blob_sha1": old["blob_sha"], "size_bytes": old["size_bytes"],
                "role": old["role"], "review_mode": old["review_mode"], "extent": old["extent"],
                "sha256": sha256(old_data),
                "sha256_lf_normalized": sha256(lf_bytes(old_data)) if old["extension"] in TEXT_EXTENSIONS else None,
            },
            "v1020": {
                "path": source["path"], "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
                "size_bytes": source["size_bytes"], "role": source["manifest_role"],
                "review_mode": source["review_mode"], "extent": source["manifest_extent"],
                "sha256_lf_normalized": sha256(lf_bytes(new_data)) if extension in TEXT_EXTENSIONS else None,
            },
            "step47_authority": {
                "source_authority_class": route_by_id[source["source_id"]]["source_authority_class"],
                "authority_ceiling": route_by_id[source["source_id"]]["authority_ceiling"],
                "evidence_route": route_by_id[source["source_id"]]["evidence_route"],
                "adoption_topology": route_by_id[source["source_id"]]["adoption_topology"],
                "scientific_authority_promoted": route_by_id[source["source_id"]]["scientific_authority_promoted"],
                "external_scientific_truth": route_by_id[source["source_id"]]["external_scientific_truth"],
            },
            "surface_layer": route_by_id[source["source_id"]]["source_authority_class"],
            "semantic_delta": "WHOLE_BLOB_ADDITION" if old is None else (
                "BYTE_IDENTICAL" if blob_relation == "IDENTICAL" else "EXACT_ENDPOINT_AND_TEXT_OR_BINARY_DELTA"
            ),
            "authority_limit": "LINEAGE_ONLY", "external_scientific_truth": False,
            "generated_output_is_source_of_record": False,
        }
        if old is None:
            row.update({"text_delta": None, "latex_delta": None, "pdf_delta": None,
                        "python_structure_delta": None})
        else:
            row["text_delta"] = exact_text_delta(old_data, new_data) if old["extension"] in TEXT_EXTENSIONS and extension in TEXT_EXTENSIONS else None
            row["latex_delta"] = latex_delta(old_data, new_data) if old["extension"] == extension == "tex" else None
            row["pdf_delta"] = {
                "pages_before": old["extent"]["pages"], "pages_after": source["manifest_extent"]["pages"],
                "page_delta": source["manifest_extent"]["pages"] - old["extent"]["pages"],
                "visual_or_scientific_equivalence_inferred": False,
            } if old["extension"] == extension == "pdf" else None
            row["python_structure_delta"] = python_structure_delta(old_data, new_data) if old["extension"] == extension == "py" else None
            if row["python_structure_delta"] is not None:
                python_pairs.append({
                    "v1020_source_id": source["source_id"], "old_path": old["path"], "new_path": source["path"],
                    "role_pair": f"{old['role']}->{source['manifest_role']}", **row["python_structure_delta"],
                })
        expected_rows.append(row)

    deleted = [
        {
            "deleted_id": f"P061-OLDONLY-{index:03d}", "comparison_class": "DELETED_COUNTERPART",
            "v1019_path": old["path"], "v1019_blob_sha1": old["blob_sha"],
            "v1019_sha256": sha256(blobs[old["blob_sha"]]), "size_bytes": old["size_bytes"],
            "role": old["role"], "review_mode": old["review_mode"], "extent": old["extent"],
            "normalized_identity": normalized_identity(suffix(old["path"], V1019_PREFIX), old["role"]),
            "phase060_topology_authority_class": old_topology_by_path[old["path"]]["authority_class"],
            "phase060_occurrence_kind": old_topology_by_path[old["path"]]["occurrence_kind"],
            "v1020_counterpart": None, "authority_limit": "LINEAGE_ONLY",
            "absence_is_not_behavioral_or_scientific_rejection": True,
        }
        for index, old in enumerate((row for row in old_entries if row["path"] not in used_old), start=1)
    ]
    if {key: class_counts[key] for key in CLASS_COUNTS} != CLASS_COUNTS or len(used_old) != 54 or len(deleted) != 12:
        raise ValidationError("INDEPENDENT_COUNTS")

    source_by_path = {row["path"]: row for row in sources}
    occurrences, projections = [], {}
    for ordinal, (alias, path) in enumerate(SNAPSHOT_PATHS.items()):
        source = source_by_path[path]
        data = blobs[source["blob_sha1"]]
        parsed = validate_snapshot_source(strict_load_bytes(data), alias)
        projection = document_projection(parsed)
        projections[alias] = projection
        history = run_git_text(["log", "--format=%H", BASELINE, "--", path], f"SNAPSHOT_HISTORY_{alias}").splitlines()
        nodes, depth = walk_json(parsed)
        occurrences.append({
            "snapshot_id": f"P061-SNAPSHOT-{ordinal + 1:02d}", "alias": alias,
            "source_id": source["source_id"], "path": path, "blob_sha1": source["blob_sha1"],
            "sha256": source["sha256"], "physical_lines": len(lf_bytes(data).splitlines()),
            "root_names": sorted(parsed), "normalized_root_names": projection["normalized_roots"],
            "root_count": len(parsed), "stage_ordinal": ordinal, "projection": projection,
            "projection_sha256": sha256(pretty_bytes(projection)),
            "strict_traversal": {"nodes": nodes, "maximum_depth": depth},
            "history_commits_newest_first": history, "history_commit_count": len(history),
            "authority_class": "STRUCTURAL_WITNESS", "authority_ceiling": "CAPTURED_STRUCTURE_ONLY",
            "external_scientific_truth": False,
        })
    edges = [snapshot_edge(before, after, projections) for before, after in zip(SNAPSHOT_ORDER, SNAPSHOT_ORDER[1:])]
    baseline_final = {
        chapter: {
            "labels": set_delta(projections["baseline"][chapter]["labels"], projections["final"][chapter]["labels"]),
            "eqblocks": snapshot_eq_delta(projections["baseline"][chapter], projections["final"][chapter]),
            "bibitems": set_delta(projections["baseline"][chapter]["bibitems"], projections["final"][chapter]["bibitems"]),
        }
        for chapter in ("ch1", "ch2")
    }
    p5 = next(row for row in occurrences if row["alias"] == "p5")
    p6 = next(row for row in occurrences if row["alias"] == "p6")
    p6_parent = run_git_text(["rev-parse", f"{p6['history_commits_newest_first'][0]}^"], "P6_PARENT")
    changed_paths = sorted(
        line for line in run_git_text([
            "diff-tree", "--no-commit-id", "--name-only", "-r",
            p5["history_commits_newest_first"][0], p6["history_commits_newest_first"][0], "--", V1020_PREFIX,
        ], "P5_P6_DIFF").splitlines() if line
    )
    changed_tex = sorted(path for path in changed_paths if path.endswith(".tex"))
    return {
        "sources": sources, "routes": route_by_id, "rows": expected_rows, "deleted": deleted,
        "class_counts": CLASS_COUNTS, "python_pairs": python_pairs,
        "occurrences": occurrences, "projections": projections, "edges": edges,
        "baseline_final": baseline_final, "p5": p5, "p6": p6, "p6_parent": p6_parent,
        "changed_paths": changed_paths, "changed_tex": changed_tex,
    }


def add_if(diagnostics: set[str], condition: bool, code: str) -> None:
    if condition:
        diagnostics.add(code)


def input_boundary_map(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    boundary = artifact.get("authority_boundary")
    if not isinstance(boundary, dict) or not isinstance(boundary.get("inputs"), list):
        return {}
    rows = boundary["inputs"]
    return {row.get("path"): row for row in rows if isinstance(row, dict) and isinstance(row.get("path"), str)}


def authority_promoted(value: Any) -> bool:
    science_true = {
        "external_scientific_truth", "external_scientific_truth_promoted",
        "scientific_authority_promoted", "snapshot_or_pdf_equality_certifies_scientific_correctness",
        "generated_output_is_source_of_record", "scientific_correctness_inferred",
        "experimental_authority_inferred", "visual_or_scientific_equivalence_inferred",
    }
    if isinstance(value, dict):
        for key, child in value.items():
            if key in science_true and child is not False:
                return True
            if key == "authority_ceiling" and child in {"SCIENTIFIC_TRUTH", "EXTERNAL_SCIENTIFIC_AUTHORITY"}:
                return True
            if authority_promoted(child):
                return True
    elif isinstance(value, list):
        return any(authority_promoted(child) for child in value)
    return False


def content_diagnostics(lineage: Any, snapshot: Any, expected: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    if not isinstance(lineage, dict):
        return {"LINEAGE_EXACT_SCHEMA"}
    if not isinstance(snapshot, dict):
        return {"SNAPSHOT_EXACT_SCHEMA"}
    if schema_sha(lineage) != LINEAGE_SCHEMA_SHA256:
        diagnostics.add("LINEAGE_EXACT_SCHEMA")
    if schema_sha(snapshot) != SNAPSHOT_SCHEMA_SHA256:
        diagnostics.add("SNAPSHOT_EXACT_SCHEMA")
    if diagnostics:
        return diagnostics

    expected_contract = "P061-STEP48-V1019-V1020-LINEAGE-SNAPSHOT-V1"
    for artifact in (lineage, snapshot):
        add_if(diagnostics, artifact.get("schema_version") != "1.0", "CROSS_GENERATION_CONTRACT")
        add_if(diagnostics, artifact.get("phase") != 61 or artifact.get("step") != 48, "CROSS_GENERATION_CONTRACT")
        add_if(diagnostics, artifact.get("status") != "COMPLETE", "CROSS_GENERATION_CONTRACT")
        add_if(diagnostics, artifact.get("gate") != "PASS_P061_STEP48_LINEAGE_DIFF", "CROSS_GENERATION_CONTRACT")
        boundary = artifact.get("authority_boundary", {})
        add_if(diagnostics, boundary.get("generation_contract_id") != expected_contract, "CROSS_GENERATION_CONTRACT")
        add_if(diagnostics, boundary.get("baseline_commit") != BASELINE, "CROSS_BASELINE_COMMIT")
        add_if(diagnostics, boundary.get("input_commit") != EXPECTED_PARENT, "CROSS_BASELINE_COMMIT")
        if (
            boundary.get("production_or_test_modules_imported_or_executed") is not False
            or boundary.get("snapshot_or_pdf_equality_certifies_scientific_correctness") is not False
            or boundary.get("generated_output_is_source_of_record") is not False
            or boundary.get("external_scientific_truth_promoted") is not False
            or boundary.get("authority_ceiling") != "FROZEN_LINEAGE_AND_CAPTURED_STRUCTURE_ONLY"
        ):
            diagnostics.add("AUTHORITY_BOUNDARY")

    line_inputs, snap_inputs = input_boundary_map(lineage), input_boundary_map(snapshot)
    if set(line_inputs) != {path.relative_to(REPO).as_posix() for path in INPUT_SHA256} or set(snap_inputs) != set(line_inputs):
        diagnostics.add("CROSS_INPUT_HASH")
    else:
        for path, expected_hash in INPUT_SHA256.items():
            relative = path.relative_to(REPO).as_posix()
            line_row, snap_row = line_inputs[relative], snap_inputs[relative]
            if relative == TOPOLOGY.relative_to(REPO).as_posix():
                code = "CROSS_TOPOLOGY_LINK"
            elif relative == PROCESS.relative_to(REPO).as_posix():
                code = "CROSS_PROCESS_LINK"
            else:
                code = "CROSS_INPUT_HASH"
            add_if(diagnostics, line_row != snap_row or line_row.get("sha256_lf_normalized") != expected_hash, code)

    add_if(diagnostics, lineage.get("required_negative_controls") != list(NEGATIVE_CONTROL_IDS), "NEGATIVE_CONTROL_CONTRACT")
    add_if(diagnostics, snapshot.get("required_negative_controls") != list(NEGATIVE_CONTROL_IDS), "NEGATIVE_CONTROL_CONTRACT")
    counts = lineage.get("counts", {})
    add_if(diagnostics, counts.get("v1020_occurrences") != 232 or counts.get("delta_rows") != 232, "CROSS_SOURCE_COUNT")
    add_if(diagnostics, counts.get("v1019_occurrences") != 66, "LINEAGE_DELETED_COVERAGE")
    add_if(diagnostics, counts.get("paired_occurrences") != 54, "LINEAGE_PAIR_COUNT")
    add_if(diagnostics, counts.get("deleted_counterparts") != 12, "LINEAGE_DELETED_COVERAGE")
    add_if(diagnostics, counts.get("comparison_classes") != CLASS_COUNTS, "LINEAGE_CLASS_COUNTS")
    add_if(diagnostics, counts.get("snapshot_occurrences_linked") != 10, "CROSS_SNAPSHOT_COUNT")
    add_if(diagnostics, counts.get("python_test_pairs") != 2, "LINEAGE_PYTHON_SUMMARY")

    rows = lineage.get("delta_rows")
    if not isinstance(rows, list):
        return diagnostics | {"LINEAGE_SOURCE_COVERAGE"}
    expected_rows = expected["rows"]
    expected_ids = [row["v1020_source_id"] for row in expected_rows]
    ids = [row.get("v1020_source_id") for row in rows if isinstance(row, dict)]
    coverage_bad = len(rows) != 232 or len(ids) != 232 or len(set(ids)) != 232 or set(ids) != set(expected_ids)
    if coverage_bad:
        diagnostics.add("LINEAGE_SOURCE_COVERAGE")
    elif ids != expected_ids:
        diagnostics.add("LINEAGE_SOURCE_IDENTITY")
    else:
        class_bad = False
        same_relative = Counter()
        for actual, wanted in zip(rows, expected_rows):
            if actual.get("comparison_class") != wanted["comparison_class"]:
                diagnostics.add("LINEAGE_CLASSIFICATION")
                class_bad = True
            if actual.get("pair_basis") != wanted["pair_basis"] or actual.get("candidate_count") != wanted["candidate_count"]:
                diagnostics.add("LINEAGE_PAIRING")
            if (
                actual.get("normalized_identity") != wanted["normalized_identity"]
                or actual.get("old_normalized_identity") != wanted["old_normalized_identity"]
                or actual.get("selected_reason") != wanted["selected_reason"]
            ):
                diagnostics.add("LINEAGE_PAIRING")
            if actual.get("path_relation") != wanted["path_relation"]:
                diagnostics.add("LINEAGE_PATH_RELATION")
            if actual.get("blob_relation") != wanted["blob_relation"]:
                diagnostics.add("LINEAGE_BLOB_RELATION")
            old_actual, old_wanted = actual.get("v1019"), wanted["v1019"]
            new_actual, new_wanted = actual.get("v1020"), wanted["v1020"]
            if old_wanted is None:
                if old_actual is not None:
                    diagnostics.add("LINEAGE_PAIRING")
            elif not isinstance(old_actual, dict):
                diagnostics.add("LINEAGE_ENDPOINT_BLOB")
            else:
                endpoint_keys = ("blob_sha1", "size_bytes", "role", "review_mode", "extent", "sha256", "sha256_lf_normalized")
                if any(old_actual.get(key) != old_wanted[key] for key in endpoint_keys):
                    diagnostics.add("LINEAGE_ENDPOINT_BLOB")
                if old_actual.get("path") != old_wanted["path"]:
                    diagnostics.add("LINEAGE_PAIRING")
            if not isinstance(new_actual, dict) or any(new_actual.get(key) != new_wanted[key] for key in new_wanted):
                diagnostics.add("LINEAGE_ENDPOINT_BLOB")
            if actual.get("step47_authority") != wanted["step47_authority"] or actual.get("surface_layer") != wanted["surface_layer"]:
                diagnostics.add("STEP47_AUTHORITY_ROUTE")
            if (
                actual.get("authority_limit") != "LINEAGE_ONLY"
                or actual.get("external_scientific_truth") is not False
                or actual.get("generated_output_is_source_of_record") is not False
            ):
                diagnostics.add("AUTHORITY_PROMOTION")
            if actual.get("text_delta") != wanted.get("text_delta"):
                diagnostics.add("LINEAGE_TEXT_HUNKS")
            actual_latex, wanted_latex = actual.get("latex_delta"), wanted.get("latex_delta")
            if isinstance(wanted_latex, dict):
                if not isinstance(actual_latex, dict):
                    diagnostics.update({"LINEAGE_LATEX_LABELS", "LINEAGE_LATEX_EQUATIONS", "LINEAGE_LATEX_BIBLIOGRAPHY", "LINEAGE_LATEX_INCLUDES"})
                else:
                    add_if(diagnostics, actual_latex.get("labels") != wanted_latex["labels"], "LINEAGE_LATEX_LABELS")
                    add_if(diagnostics, actual_latex.get("equation_blocks_by_semantic_identity") != wanted_latex["equation_blocks_by_semantic_identity"], "LINEAGE_LATEX_EQUATIONS")
                    add_if(diagnostics, actual_latex.get("bibliography") != wanted_latex["bibliography"], "LINEAGE_LATEX_BIBLIOGRAPHY")
                    add_if(diagnostics, actual_latex.get("include_topology") != wanted_latex["include_topology"], "LINEAGE_LATEX_INCLUDES")
            elif actual_latex is not None:
                diagnostics.add("LINEAGE_LATEX_EQUATIONS")
            add_if(diagnostics, actual.get("pdf_delta") != wanted.get("pdf_delta"), "LINEAGE_PDF_PAGES")
            actual_python, wanted_python = actual.get("python_structure_delta"), wanted.get("python_structure_delta")
            if wanted_python is not None:
                filename = wanted["v1020"]["path"].rsplit("/", 1)[-1]
                code = "LINEAGE_TEST_AST" if filename.startswith("test_") else "LINEAGE_CODE_AST"
                if isinstance(actual_python, dict):
                    runtime_keys = {"execution_performed", "behavioral_change_state", "authority_ceiling"}
                    actual_structure = {key: value for key, value in actual_python.items() if key not in runtime_keys}
                    wanted_structure = {key: value for key, value in wanted_python.items() if key not in runtime_keys}
                    add_if(diagnostics, actual_structure != wanted_structure, code)
                    if (
                        actual_python.get("execution_performed") is not False
                        or actual_python.get("behavioral_change_state") != "UNVERIFIED_NO_RUNTIME_EXECUTION"
                        or actual_python.get("authority_ceiling") != "FROZEN_SOURCE_STRUCTURE_ONLY_NOT_RUNTIME_BEHAVIOR"
                    ):
                        diagnostics.add("RUNTIME_PROMOTION")
                else:
                    diagnostics.add(code)
            elif actual_python is not None:
                diagnostics.add("LINEAGE_CODE_AST")
            if wanted["pair_basis"] == "FULL_VERSION_RELATIVE_PATH":
                same_relative[wanted["comparison_class"]] += 1
        if not class_bad:
            observed_classes = Counter(row.get("comparison_class") for row in rows)
            add_if(diagnostics, {key: observed_classes[key] for key in CLASS_COUNTS} != CLASS_COUNTS, "LINEAGE_CLASS_COUNTS")
            add_if(diagnostics, sum(same_relative.values()) != 47 or same_relative != Counter({"MODIFIED": 29, "UNCHANGED": 18}), "LINEAGE_SAME_RELATIVE_SUBSET")

    deleted = lineage.get("deleted_counterparts")
    if not isinstance(deleted, list) or deleted != expected["deleted"]:
        diagnostics.add("LINEAGE_DELETED_COVERAGE")

    actual_python_pairs = lineage.get("python_test_source_comparisons")
    if not isinstance(actual_python_pairs, list) or len(actual_python_pairs) != 2:
        diagnostics.add("LINEAGE_PYTHON_SUMMARY")
    else:
        for actual, wanted in zip(actual_python_pairs, expected["python_pairs"]):
            runtime_keys = {"execution_performed", "behavioral_change_state", "authority_ceiling"}
            if {k: v for k, v in actual.items() if k not in runtime_keys} != {k: v for k, v in wanted.items() if k not in runtime_keys}:
                diagnostics.add("LINEAGE_PYTHON_SUMMARY")
            if actual.get("execution_performed") is not False or actual.get("behavioral_change_state") != "UNVERIFIED_NO_RUNTIME_EXECUTION":
                diagnostics.add("RUNTIME_PROMOTION")

    snapshot_counts = snapshot.get("counts", {})
    add_if(diagnostics, snapshot_counts.get("snapshot_occurrences") != 10, "CROSS_SNAPSHOT_COUNT")
    add_if(diagnostics, snapshot_counts.get("unique_snapshot_blobs") != 9, "SNAPSHOT_BLOB_IDENTITY")
    add_if(diagnostics, snapshot_counts.get("stage_edges") != 9, "SNAPSHOT_EDGE_COVERAGE")
    add_if(diagnostics, snapshot_counts.get("duplicate_occurrence_groups") != 1, "P5_P6_BLOB_DIVERGENCE")
    add_if(diagnostics, snapshot.get("snapshot_order") != list(SNAPSHOT_ORDER), "SNAPSHOT_EDGE_ORDER")
    occurrences = snapshot.get("snapshot_occurrences")
    occurrence_ok = isinstance(occurrences, list) and len(occurrences) == 10
    aliases = [row.get("alias") for row in occurrences] if occurrence_ok else []
    if not occurrence_ok or len(set(aliases)) != 10 or set(aliases) != set(SNAPSHOT_ORDER):
        diagnostics.add("SNAPSHOT_OCCURRENCE_COVERAGE")
    elif aliases != list(SNAPSHOT_ORDER):
        diagnostics.add("SNAPSHOT_PATH_IDENTITY")
    else:
        for actual, wanted in zip(occurrences, expected["occurrences"]):
            add_if(diagnostics, actual.get("snapshot_id") != wanted["snapshot_id"] or actual.get("path") != wanted["path"] or actual.get("source_id") != wanted["source_id"] or actual.get("stage_ordinal") != wanted["stage_ordinal"], "SNAPSHOT_PATH_IDENTITY")
            add_if(diagnostics, actual.get("blob_sha1") != wanted["blob_sha1"] or actual.get("sha256") != wanted["sha256"] or actual.get("physical_lines") != wanted["physical_lines"], "SNAPSHOT_BLOB_IDENTITY")
            add_if(diagnostics, actual.get("root_names") != wanted["root_names"] or actual.get("normalized_root_names") != wanted["normalized_root_names"] or actual.get("root_count") != wanted["root_count"], "SNAPSHOT_ROOT_PROJECTION")
            projection = actual.get("projection")
            wanted_projection = wanted["projection"]
            projection_codes: set[str] = set()
            if not isinstance(projection, dict):
                projection_codes.add("SNAPSHOT_CHAPTER_PROJECTION")
            else:
                for chapter in ("ch1", "ch2"):
                    actual_chapter = projection.get(chapter)
                    wanted_chapter = wanted_projection[chapter]
                    if not isinstance(actual_chapter, dict):
                        projection_codes.add("SNAPSHOT_CHAPTER_PROJECTION")
                        continue
                    labels = actual_chapter.get("labels")
                    bibitems = actual_chapter.get("bibitems")
                    eqblocks = actual_chapter.get("eqblocks")
                    if not isinstance(labels, list) or len(labels) != len(set(labels)):
                        projection_codes.add("SNAPSHOT_LABEL_SCHEMA")
                    elif labels != wanted_chapter["labels"]:
                        projection_codes.add("SNAPSHOT_CHAPTER_PROJECTION")
                    if not isinstance(bibitems, list) or len(bibitems) != len(set(bibitems)):
                        projection_codes.add("SNAPSHOT_BIB_SCHEMA")
                    elif bibitems != wanted_chapter["bibitems"]:
                        projection_codes.add("SNAPSHOT_CHAPTER_PROJECTION")
                    if not isinstance(eqblocks, list) or len({row.get("identifier") for row in eqblocks if isinstance(row, dict)}) != len(eqblocks):
                        projection_codes.add("SNAPSHOT_EQBLOCK_SCHEMA")
                    elif eqblocks != wanted_chapter["eqblocks"]:
                        projection_codes.add("SNAPSHOT_CHAPTER_PROJECTION")
                    if actual_chapter.get("asset_unique") != wanted_chapter["asset_unique"]:
                        projection_codes.add("SNAPSHOT_CHAPTER_PROJECTION")
                if projection.get("raw_roots") != wanted_projection["raw_roots"] or projection.get("normalized_roots") != wanted_projection["normalized_roots"] or projection.get("all_root_projections") != wanted_projection["all_root_projections"]:
                    projection_codes.add("SNAPSHOT_ROOT_PROJECTION")
            diagnostics.update(projection_codes)
            if not projection_codes:
                add_if(diagnostics, actual.get("projection_sha256") != wanted["projection_sha256"], "SNAPSHOT_CHAPTER_PROJECTION")
            add_if(diagnostics, actual.get("strict_traversal") != wanted["strict_traversal"], "SNAPSHOT_CHAPTER_PROJECTION")
            add_if(diagnostics, actual.get("history_commits_newest_first") != wanted["history_commits_newest_first"] or actual.get("history_commit_count") != wanted["history_commit_count"], "SNAPSHOT_PATH_IDENTITY")
            if actual.get("authority_class") != "STRUCTURAL_WITNESS" or actual.get("authority_ceiling") != "CAPTURED_STRUCTURE_ONLY" or actual.get("external_scientific_truth") is not False:
                diagnostics.add("AUTHORITY_PROMOTION")

    edges = snapshot.get("stage_edges")
    edge_coverage = isinstance(edges, list) and len(edges) == 9 and len({row.get("edge_id") for row in edges if isinstance(row, dict)}) == 9
    if not edge_coverage:
        diagnostics.add("SNAPSHOT_EDGE_COVERAGE")
    else:
        order_bad = [(row.get("before_alias"), row.get("after_alias")) for row in edges] != list(zip(SNAPSHOT_ORDER, SNAPSHOT_ORDER[1:]))
        if order_bad:
            diagnostics.add("SNAPSHOT_EDGE_ORDER")
        else:
            for actual, wanted in zip(edges, expected["edges"]):
                add_if(diagnostics, actual.get("edge_id") != wanted["edge_id"] or actual.get("before_alias") != wanted["before_alias"] or actual.get("after_alias") != wanted["after_alias"], "SNAPSHOT_EDGE_ENDPOINT")
                if {key: value for key, value in actual.items() if key not in {"edge_id", "before_alias", "after_alias"}} != {key: value for key, value in wanted.items() if key not in {"edge_id", "before_alias", "after_alias"}}:
                    diagnostics.add("SNAPSHOT_EDGE_PROJECTION")

    duplicates = snapshot.get("duplicate_occurrence_groups")
    if not isinstance(duplicates, list) or len(duplicates) != 1 or not isinstance(duplicates[0], dict):
        diagnostics.add("P5_P6_BLOB_DIVERGENCE")
    else:
        duplicate = duplicates[0]
        add_if(diagnostics, duplicate.get("aliases") != ["p5", "p6"] or duplicate.get("paths") != [expected["p5"]["path"], expected["p6"]["path"]] or duplicate.get("occurrences_distinct") is not True, "P5_P6_OCCURRENCE_COLLAPSE")
        add_if(diagnostics, duplicate.get("blob_sha1") != expected["p5"]["blob_sha1"] or duplicate.get("sha256") != expected["p5"]["sha256"] or duplicate.get("blob_identical") is not True or duplicate.get("captured_document_projection_identical") is not True, "P5_P6_BLOB_DIVERGENCE")
        add_if(diagnostics, duplicate.get("actual_source_tree_identical") is not False or duplicate.get("changed_tex_paths") != P5_P6_CHANGED_TEX or duplicate.get("all_changed_paths") != expected["changed_paths"] or duplicate.get("independently_reconstructed_from_git") is not True, "P5_P6_SOURCE_EQUALITY_FALSE")
        add_if(diagnostics, duplicate.get("p5_commit") != expected["p5"]["history_commits_newest_first"][0] or duplicate.get("p6_commit") != expected["p6"]["history_commits_newest_first"][0] or duplicate.get("p6_parent") != expected["p6_parent"] or duplicate.get("direct_parent") is not True or duplicate.get("step47_boundary_exactly_corroborates") is not True, "P5_P6_SOURCE_EQUALITY_FALSE")

    appendix = snapshot.get("appendix_root_genealogy", {})
    add_if(diagnostics, appendix.get("prefinal_aliases") != ["p0", "p2", "p3", "p4", "p5", "p6", "p7", "p7b"] or appendix.get("prefinal_root_occurrences") != 0 or appendix.get("baseline_root_occurrences") != 0, "APPENDIX_PREFINAL_HISTORY_FALSE")
    add_if(diagnostics, appendix.get("final_root_name") != "appendix_phase_separation.tex" or appendix.get("final_root_occurrences") != 1, "APPENDIX_FINAL_ROOT")
    add_if(diagnostics, appendix.get("adopted_release_edge_inferred_from_snapshot") is not False or appendix.get("target_phase_for_adoption_authority") != 62, "AUTHORITY_PROMOTION")

    baseline_final = snapshot.get("baseline_to_final", {})
    if baseline_final.get("ch1") != expected["baseline_final"]["ch1"]:
        diagnostics.add("SNAPSHOT_CH1_DELTA")
    if baseline_final.get("ch2") != expected["baseline_final"]["ch2"]:
        diagnostics.add("SNAPSHOT_CH2_DELTA")
    if lineage.get("release_delta_summary", {}).get("baseline_to_final_snapshot_delta") != baseline_final:
        diagnostics.add("LINEAGE_RELEASE_SNAPSHOT_LINK")
    expected_ch1, expected_ch2 = expected["baseline_final"]["ch1"], expected["baseline_final"]["ch2"]
    if not (
        expected_ch1["labels"]["count_delta"] == 6
        and expected_ch1["eqblocks"]["count_after"] - expected_ch1["eqblocks"]["count_before"] == 6
        and expected_ch1["bibitems"]["count_delta"] == 8
        and any(row["identifier"] == "eq:lco-slots" for row in expected_ch1["eqblocks"]["changed"])
    ):
        diagnostics.add("SNAPSHOT_CH1_DELTA")
    if not (
        expected_ch2["labels"]["count_delta"] == 0
        and expected_ch2["eqblocks"]["substantive_projection_equal"]
        and expected_ch2["bibitems"]["count_delta"] == 2
    ):
        diagnostics.add("SNAPSHOT_CH2_DELTA")
    if expected["projections"]["baseline"]["normalized_roots"] != expected["projections"]["p0"]["normalized_roots"] or expected["projections"]["baseline"]["ch1"] != expected["projections"]["p0"]["ch1"] or expected["projections"]["baseline"]["ch2"] != expected["projections"]["p0"]["ch2"]:
        diagnostics.add("SNAPSHOT_BASELINE_P0")

    if authority_promoted(lineage) or authority_promoted(snapshot):
        diagnostics.add("AUTHORITY_PROMOTION")
    if not all(row.get("status") == "UNVERIFIED" for row in lineage.get("unverified_queue", [])):
        diagnostics.add("UNVERIFIED_BOUNDARY")
    if not all(row.get("status") == "UNVERIFIED" for row in snapshot.get("unverified_queue", [])):
        diagnostics.add("UNVERIFIED_BOUNDARY")
    return diagnostics


def first_row(rows: list[dict[str, Any]], predicate: Any) -> dict[str, Any]:
    return next(row for row in rows if predicate(row))


def mutate_for_control(control: str, lineage: dict[str, Any], snapshot: dict[str, Any]) -> None:
    rows = lineage["delta_rows"]
    paired = first_row(rows, lambda row: row["v1019"] is not None)
    added = first_row(rows, lambda row: row["comparison_class"] == "ADDED")
    modified = first_row(rows, lambda row: row["comparison_class"] == "MODIFIED")
    unchanged = first_row(rows, lambda row: row["comparison_class"] == "UNCHANGED")
    renamed = first_row(rows, lambda row: row["comparison_class"] == "RENAMED")
    text = first_row(rows, lambda row: isinstance(row["text_delta"], dict) and row["text_delta"]["segments"])
    latex = first_row(rows, lambda row: isinstance(row["latex_delta"], dict))
    latex_bib = first_row(rows, lambda row: isinstance(row["latex_delta"], dict) and (
        row["latex_delta"]["bibliography"]["added"] or row["latex_delta"]["bibliography"]["removed"]
        or row["latex_delta"]["bibliography"]["changed"]
    ))
    latex_label = first_row(rows, lambda row: isinstance(row["latex_delta"], dict) and (
        row["latex_delta"]["labels"]["added"] or row["latex_delta"]["labels"]["removed"]
    ))
    latex_eq = first_row(rows, lambda row: isinstance(row["latex_delta"], dict) and (
        row["latex_delta"]["equation_blocks_by_semantic_identity"]["added"]
        or row["latex_delta"]["equation_blocks_by_semantic_identity"]["removed"]
        or row["latex_delta"]["equation_blocks_by_semantic_identity"]["changed"]
        or row["latex_delta"]["equation_blocks_by_semantic_identity"]["moved"]
    ))
    latex_include = first_row(rows, lambda row: isinstance(row["latex_delta"], dict) and row["latex_delta"]["include_topology"]["before"])
    pdf = first_row(rows, lambda row: isinstance(row["pdf_delta"], dict))
    code = first_row(rows, lambda row: isinstance(row["python_structure_delta"], dict) and not row["v1020"]["path"].rsplit("/", 1)[-1].startswith("test_"))
    test = first_row(rows, lambda row: isinstance(row["python_structure_delta"], dict) and row["v1020"]["path"].rsplit("/", 1)[-1].startswith("test_"))
    occurrences = snapshot["snapshot_occurrences"]
    edges = snapshot["stage_edges"]
    duplicate = snapshot["duplicate_occurrence_groups"][0]

    if control == "lineage-drop-source":
        rows.pop(1)
    elif control == "lineage-duplicate-source":
        rows[-1]["v1020_source_id"] = rows[0]["v1020_source_id"]
    elif control == "lineage-source-id-swap":
        rows[0]["v1020_source_id"], rows[1]["v1020_source_id"] = rows[1]["v1020_source_id"], rows[0]["v1020_source_id"]
    elif control == "lineage-wrong-pair":
        paired["v1019"]["path"] = "Claude/docs/v1.0.19/WRONG"
    elif control == "lineage-missing-old-blob":
        paired["v1019"]["blob_sha1"] = "0" * 40
    elif control == "lineage-missing-new-blob":
        rows[0]["v1020"]["blob_sha1"] = "0" * 40
    elif control == "lineage-false-unchanged":
        modified["comparison_class"] = "UNCHANGED"
    elif control == "lineage-false-added":
        added["comparison_class"] = "MODIFIED"
    elif control == "lineage-false-renamed":
        renamed["comparison_class"] = "MODIFIED"
    elif control == "lineage-false-copied":
        added["comparison_class"] = "COPIED"
    elif control == "lineage-drop-deleted":
        lineage["deleted_counterparts"].pop()
    elif control == "lineage-duplicate-deleted":
        lineage["deleted_counterparts"][-1] = copy.deepcopy(lineage["deleted_counterparts"][0])
    elif control == "lineage-old-coverage":
        lineage["counts"]["v1019_occurrences"] -= 1
    elif control == "lineage-new-coverage":
        rows[-1]["v1020_source_id"] = "P061-V1020-SOURCE-0000"
    elif control == "lineage-pair-count":
        lineage["counts"]["paired_occurrences"] -= 1
    elif control == "lineage-class-count":
        lineage["counts"]["comparison_classes"]["MODIFIED"] -= 1
    elif control == "lineage-path-relation":
        paired["path_relation"] = "ADDED"
    elif control == "lineage-blob-relation":
        paired["blob_relation"] = "NO_OLD_BLOB"
    elif control == "lineage-hunk-hash":
        text["text_delta"]["segments"][0]["segment_sha256"] = "0" * 64
    elif control == "lineage-hunk-range":
        text["text_delta"]["segments"][0]["new_line_start"] += 1
    elif control == "lineage-hunk-content":
        text["text_delta"]["segments"][0]["new_lines"][0] += " MUTATED"
    elif control == "lineage-bib-delta":
        latex_bib["latex_delta"]["bibliography"]["unchanged_count"] += 1
    elif control == "lineage-label-delta":
        latex_label["latex_delta"]["labels"]["after"] += 1
    elif control in {"lineage-equation-delta", "lineage-bracket-display-escape"}:
        latex_eq["latex_delta"]["equation_blocks_by_semantic_identity"]["unchanged_count"] += 1
    elif control == "lineage-include-delta":
        latex_include["latex_delta"]["include_topology"]["before"].reverse()
    elif control == "lineage-pdf-pages":
        pdf["pdf_delta"]["pages_after"] += 1
    elif control == "lineage-code-ast":
        code["python_structure_delta"]["new_module_ast_sha256"] = "0" * 64
    elif control == "lineage-test-ast":
        test["python_structure_delta"]["new_module_ast_sha256"] = "0" * 64
    elif control == "lineage-code-execution-promotion":
        code["python_structure_delta"]["execution_performed"] = True
    elif control == "lineage-science-promotion":
        rows[0]["external_scientific_truth"] = True
    elif control == "snapshot-drop-occurrence":
        occurrences.pop()
    elif control == "snapshot-duplicate-occurrence":
        occurrences[-1] = copy.deepcopy(occurrences[0])
    elif control == "snapshot-path-swap":
        occurrences[0]["path"], occurrences[1]["path"] = occurrences[1]["path"], occurrences[0]["path"]
    elif control == "snapshot-blob-swap":
        occurrences[0]["blob_sha1"], occurrences[1]["blob_sha1"] = occurrences[1]["blob_sha1"], occurrences[0]["blob_sha1"]
    elif control == "snapshot-sha-swap":
        occurrences[0]["sha256"], occurrences[1]["sha256"] = occurrences[1]["sha256"], occurrences[0]["sha256"]
    elif control == "snapshot-root-schema":
        occurrences[0]["root_count"] += 1
    elif control == "snapshot-chapter-schema":
        occurrences[0]["projection"]["ch1"]["asset_unique"] += 1
    elif control == "snapshot-label-duplicate":
        labels = occurrences[0]["projection"]["ch1"]["labels"]
        labels.append(labels[0])
    elif control == "snapshot-bib-duplicate":
        bibitems = occurrences[0]["projection"]["ch1"]["bibitems"]
        bibitems.append(bibitems[0])
    elif control == "snapshot-eqblock-schema":
        eqblocks = occurrences[0]["projection"]["ch1"]["eqblocks"]
        eqblocks.append(copy.deepcopy(eqblocks[0]))
    elif control == "snapshot-drop-edge":
        edges.pop(1)
    elif control == "snapshot-duplicate-edge":
        edges[-1]["edge_id"] = edges[0]["edge_id"]
    elif control == "snapshot-edge-order":
        edges[0], edges[1] = edges[1], edges[0]
    elif control == "snapshot-edge-endpoint":
        edges[0]["edge_id"] = "P061-SNAP-EDGE-99"
    elif control == "snapshot-edge-projection":
        edges[0]["document_projection_equal"] = not edges[0]["document_projection_equal"]
    elif control == "snapshot-p5-p6-path-collapse":
        duplicate["paths"][1] = duplicate["paths"][0]
        duplicate["occurrences_distinct"] = False
    elif control == "snapshot-p5-p6-blob-divergence":
        duplicate["blob_sha1"] = "0" * 40
        duplicate["blob_identical"] = False
    elif control == "snapshot-p5-p6-source-tree-equality":
        duplicate["actual_source_tree_identical"] = True
    elif control == "snapshot-appendix-prefinal-promotion":
        snapshot["appendix_root_genealogy"]["prefinal_root_occurrences"] = 1
    elif control == "snapshot-appendix-final-removal":
        snapshot["appendix_root_genealogy"]["final_root_occurrences"] = 0
    elif control == "snapshot-ch1-count":
        snapshot["baseline_to_final"]["ch1"]["labels"]["count_delta"] += 1
        lineage["release_delta_summary"]["baseline_to_final_snapshot_delta"]["ch1"]["labels"]["count_delta"] += 1
    elif control == "snapshot-ch2-count":
        snapshot["baseline_to_final"]["ch2"]["bibitems"]["count_delta"] += 1
        lineage["release_delta_summary"]["baseline_to_final_snapshot_delta"]["ch2"]["bibitems"]["count_delta"] += 1
    elif control in {
        "snapshot-equation-hash-science-promotion", "snapshot-generated-source-inversion",
        "snapshot-structural-science-promotion", "snapshot-external-truth-promotion",
    }:
        occurrences[0]["external_scientific_truth"] = True
    elif control == "cross-generation-contract":
        lineage["authority_boundary"]["generation_contract_id"] += "-MUTATED"
    elif control == "cross-input-hash":
        input_boundary_map(lineage)[MANIFEST.relative_to(REPO).as_posix()]["sha256_lf_normalized"] = "0" * 64
    elif control == "cross-baseline-commit":
        lineage["authority_boundary"]["baseline_commit"] = "0" * 40
    elif control == "cross-topology-link":
        input_boundary_map(lineage)[TOPOLOGY.relative_to(REPO).as_posix()]["sha256_lf_normalized"] = "0" * 64
    elif control == "cross-process-link":
        input_boundary_map(lineage)[PROCESS.relative_to(REPO).as_posix()]["sha256_lf_normalized"] = "0" * 64
    elif control == "cross-source-count":
        lineage["counts"]["v1020_occurrences"] -= 1
    elif control == "cross-snapshot-count":
        snapshot["counts"]["snapshot_occurrences"] -= 1
    elif control == "cross-authority-boundary":
        lineage["authority_boundary"]["production_or_test_modules_imported_or_executed"] = True
    elif control == "cross-unverified-boundary":
        lineage["unverified_queue"][0]["status"] = "VERIFIED"
    else:
        raise ValidationError(f"NEGATIVE_CONTROL_UNIMPLEMENTED:{control}")


def strict_json_negative_controls() -> tuple[int, int]:
    probes = [b'{"x":1,"x":2}', b'{"x":NaN}']
    passed = 0
    for data in probes:
        try:
            strict_load_bytes(data)
        except (DuplicateKeyError, NonFiniteNumberError):
            passed += 1
    return passed, len(probes)


def run_negative_controls(lineage: dict[str, Any], snapshot: dict[str, Any], expected: dict[str, Any]) -> tuple[int, int]:
    if content_diagnostics(lineage, snapshot, expected):
        raise ValidationError("NEGATIVE_BASELINE_NOT_CLEAN")
    if len(NEGATIVE_CONTROL_IDS) != len(set(NEGATIVE_CONTROL_IDS)) or set(NEGATIVE_CONTROL_IDS) != set(CONTROL_DIAGNOSTIC):
        raise ValidationError("NEGATIVE_ID_CONTRACT")
    passed = 0
    for control in NEGATIVE_CONTROL_IDS:
        mutated_lineage, mutated_snapshot = copy.deepcopy(lineage), copy.deepcopy(snapshot)
        mutate_for_control(control, mutated_lineage, mutated_snapshot)
        observed = content_diagnostics(mutated_lineage, mutated_snapshot, expected)
        wanted = {CONTROL_DIAGNOSTIC[control]}
        if observed != wanted:
            print(f"FAIL NEGATIVE_{control} expected={sorted(wanted)} observed={sorted(observed)}")
        else:
            passed += 1
    return passed, len(NEGATIVE_CONTROL_IDS)


def run_builder_once(directory: Path) -> tuple[bytes, bytes, str]:
    lineage_path, snapshot_path = directory / "lineage.json", directory / "snapshot.json"
    try:
        completed = subprocess.run(
            [sys.executable, str(BUILDER), "--lineage-output", str(lineage_path), "--snapshot-output", str(snapshot_path)],
            cwd=REPO, check=False, capture_output=True, text=True, timeout=180,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError("BUILDER_TIMEOUT") from exc
    if completed.returncode != 0:
        raise ValidationError("BUILDER_EXECUTION:" + completed.stdout.strip())
    if not lineage_path.is_file() or not snapshot_path.is_file():
        raise ValidationError("BUILDER_OUTPUT_MISSING")
    line_bytes, snap_bytes = lineage_path.read_bytes(), snapshot_path.read_bytes()
    strict_load_bytes(line_bytes)
    strict_load_bytes(snap_bytes)
    return line_bytes, snap_bytes, completed.stdout.strip()


def determinism_check(stored_lineage: bytes, stored_snapshot: bytes) -> tuple[int, int]:
    outputs = []
    for _ in range(2):
        with tempfile.TemporaryDirectory(prefix="p061_step48_validate_") as name:
            outputs.append(run_builder_once(Path(name))[:2])
    passed = sum(
        line == stored_lineage and snap == stored_snapshot and line == outputs[0][0] and snap == outputs[0][1]
        for line, snap in outputs
    )
    return passed, 2


def bracket_escape_fixture() -> bool:
    false_display = r"\\[4pt] ordinary row break"
    true_display = r"\[x+y\]"
    return latex_equations(false_display) == [] and len(latex_equations(true_display)) == 1


def current_contradiction(text: str, target: str) -> bool:
    """Reject explicit FAIL-like state only in current Step 48 context."""
    in_fence = False
    headings: list[tuple[int, str]] = []
    lines = lf_bytes(text.encode("utf-8")).decode("utf-8").splitlines()
    for index, raw in enumerate(lines):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        quote_free = re.sub(r"^(?:>\s*)+", "", stripped)
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*$", quote_free)
        if heading:
            level, title = len(heading.group(1)), heading.group(2)
            headings = [row for row in headings if row[0] < level]
            headings.append((level, title))
            continue
        if index + 1 < len(lines) and re.match(r"^\s*(?:=+|-+)\s*$", lines[index + 1]):
            level = 1 if "=" in lines[index + 1] else 2
            headings = [row for row in headings if row[0] < level]
            headings.append((level, quote_free))
        context = " / ".join(title for _, title in headings)
        explicit_target = target.lower() in quote_free.lower()
        step_headings = [title for _, title in headings if re.search(r"Step\s*\d+", title, re.I)]
        if step_headings:
            heading_current = target.lower() in step_headings[-1].lower()
        else:
            heading_current = target.lower() in context.lower()
        current = explicit_target or heading_current or (
            "phase 061" in (context + " " + quote_free).lower() and "current" in (context + " " + quote_free).lower()
        )
        state = re.search(r"(?:^|[|:=`\s])(FAIL(?:ED)?|CONDITIONAL|BLOCKED)(?:$|[|`\s])", quote_free, re.I)
        if current and state:
            if state.group(1).upper() == "BLOCKED" and re.search(r"Step\s*49", quote_free, re.I) and not re.search(r"Step\s*48", quote_free, re.I):
                continue
            return True
    return False


def result_diagnostics(text: str | None) -> set[str]:
    if text is None:
        return {"STEP48_RESULT_MISSING"}
    required = (
        "Phase 061 Step 48", "PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json",
        "PHASE_061_V1020_SNAPSHOT_GENEALOGY.json", "PASS_P061_STEP48_LINEAGE_DIFF",
        "PASS_WITH_CONCERNS", "232", "66", "54", "12", "178", "29", "18", "7", "0",
        "PENDING_AT_PRECOMMIT_BY_DESIGN", EXPECTED_SUBJECT, "Step 49", "persistence",
        BUILDER_SHA256, "25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914",
        "629995ab5936587840e5944c513ef86a0e82f114dd1d94860b06754fb9fdd414",
    )
    if any(token not in text for token in required):
        return {"STEP48_RESULT_BAD"}
    if current_contradiction(text, "Step 48"):
        return {"STEP48_RESULT_BAD"}
    if not re.search(r"(?:external scientific|scientific/external|외부 과학|과학.*권위).{0,80}(?:0|not promoted|승격.*없)", text, re.I | re.S):
        return {"STEP48_RESULT_BAD"}
    return set()


def ledger_diagnostics(text: str | None, parent: bool = False) -> set[str]:
    code = "STEP48_PARENT_LEDGER_BAD" if parent else "STEP48_ACTIVE_LEDGER_BAD"
    if text is None:
        return {code}
    phase_rows = [line for line in text.splitlines() if re.match(r"^\|\s*061\s*\|", line)]
    if len(phase_rows) != 1:
        return {code}
    row = phase_rows[0]
    required = (
        "46–48", "PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md",
        "PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json", "PHASE_061_V1020_SNAPSHOT_GENEALOGY.json",
        "PASS_P061_STEP48_LINEAGE_DIFF", "PASS_WITH_CONCERNS", "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "Step 49", "persistence",
    )
    if any(token not in row for token in required):
        return {code}
    if not parent:
        step47 = [line for line in text.splitlines() if re.match(r"^\|\s*Step 47\s*\|", line)]
        step48 = [line for line in text.splitlines() if re.match(r"^\|\s*Step 48\s*\|", line)]
        if (
            len(step47) != 1 or EXPECTED_PARENT not in step47[0] or "PASS_P061_STEP47_PERSISTENCE" not in step47[0]
            or len(step48) != 1 or "PENDING_AT_PRECOMMIT_BY_DESIGN" not in step48[0]
        ):
            return {code}
    if current_contradiction(text, "Step 48"):
        return {code}
    return set()


def handover_diagnostics(text: str | None) -> set[str]:
    if text is None:
        return {"STEP48_HANDOVER_BAD"}
    required = (
        "Phase 061", "Step 48", "PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md",
        "PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json", "PHASE_061_V1020_SNAPSHOT_GENEALOGY.json",
        EXPECTED_PARENT, "PASS_P061_STEP47_PERSISTENCE", "PASS_P061_STEP48_LINEAGE_DIFF",
        "PASS_WITH_CONCERNS", "PENDING_AT_PRECOMMIT_BY_DESIGN", "Step 49", "persistence",
    )
    if any(token not in text for token in required):
        return {"STEP48_HANDOVER_BAD"}
    if current_contradiction(text, "Step 48"):
        return {"STEP48_HANDOVER_BAD"}
    return set()


def read_optional(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def control_diagnostics(
    result: str | None | object = _UNSET,
    active: str | None | object = _UNSET,
    parent: str | None | object = _UNSET,
    handover: str | None | object = _UNSET,
) -> set[str]:
    values = {
        "result": read_optional(RESULT) if result is _UNSET else result,
        "active": read_optional(ACTIVE_LEDGER) if active is _UNSET else active,
        "parent": read_optional(PARENT_LEDGER) if parent is _UNSET else parent,
        "handover": read_optional(HANDOVER) if handover is _UNSET else handover,
    }
    diagnostics = result_diagnostics(values["result"] if isinstance(values["result"], str) else None)
    diagnostics |= ledger_diagnostics(values["active"] if isinstance(values["active"], str) else None)
    diagnostics |= ledger_diagnostics(values["parent"] if isinstance(values["parent"], str) else None, parent=True)
    diagnostics |= handover_diagnostics(values["handover"] if isinstance(values["handover"], str) else None)
    return diagnostics


def clean_control_templates() -> tuple[str, str, str, str]:
    result = f"""# Phase 061 Step 48 Lineage Diff Result

Gate: PASS_P061_STEP48_LINEAGE_DIFF
Overall: PASS_WITH_CONCERNS
Artifacts: PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json PHASE_061_V1020_SNAPSHOT_GENEALOGY.json
Counts: 232/66; paired 54; deleted 12; classes 178/29/18/7/0.
Hashes: builder {BUILDER_SHA256}; lineage 25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914; snapshot 629995ab5936587840e5944c513ef86a0e82f114dd1d94860b06754fb9fdd414.
External scientific authority promotion: 0.
Containing commit: PENDING_AT_PRECOMMIT_BY_DESIGN.
Subject: {EXPECTED_SUBJECT}
Next: Step 49 is blocked until persistence.
"""
    phase = (
        "| 061 | 46–48 | Steps 46–48 | IN_PROGRESS | PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md | "
        "PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json; PHASE_061_V1020_SNAPSHOT_GENEALOGY.json | "
        "PASS_P061_STEP48_LINEAGE_DIFF; PASS_WITH_CONCERNS; PENDING_AT_PRECOMMIT_BY_DESIGN | "
        "Step 49 blocked until persistence |"
    )
    active = "# Ledger\n" + phase + (
        f"\n| Step 47 | result | {EXPECTED_PARENT} | PASS_P061_STEP47_PERSISTENCE |"
        "\n| Step 48 | result | PENDING_AT_PRECOMMIT_BY_DESIGN |"
    )
    parent = "# Parent Ledger\n" + phase
    handover = f"""# Active handover

Current Phase 061 Step 48
Current result PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md
Artifacts PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json PHASE_061_V1020_SNAPSHOT_GENEALOGY.json
Step 47 {EXPECTED_PARENT} PASS_P061_STEP47_PERSISTENCE
Step 48 PASS_P061_STEP48_LINEAGE_DIFF PASS_WITH_CONCERNS PENDING_AT_PRECOMMIT_BY_DESIGN
Next Step 49 blocked until persistence.
"""
    return result, active, parent, handover


def run_control_boundary_probes() -> tuple[int, int]:
    result, active, parent, handover = clean_control_templates()
    cases: list[tuple[set[str], dict[str, Any]]] = [
        (set(), {"result": result, "active": active, "parent": parent, "handover": handover}),
        ({"STEP48_RESULT_MISSING"}, {"result": None, "active": active, "parent": parent, "handover": handover}),
        ({"STEP48_ACTIVE_LEDGER_BAD"}, {"result": result, "active": None, "parent": parent, "handover": handover}),
        ({"STEP48_PARENT_LEDGER_BAD"}, {"result": result, "active": active, "parent": None, "handover": handover}),
        ({"STEP48_HANDOVER_BAD"}, {"result": result, "active": active, "parent": parent, "handover": None}),
        ({"STEP48_RESULT_BAD"}, {"result": result.replace("PASS_WITH_CONCERNS", "PASS"), "active": active, "parent": parent, "handover": handover}),
        ({"STEP48_ACTIVE_LEDGER_BAD"}, {"result": result, "active": active.replace("46–48", "46–47"), "parent": parent, "handover": handover}),
        ({"STEP48_PARENT_LEDGER_BAD"}, {"result": result, "active": active, "parent": parent.replace("Step 49", "Step 50"), "handover": handover}),
        ({"STEP48_HANDOVER_BAD"}, {"result": result, "active": active, "parent": parent, "handover": handover.replace(EXPECTED_PARENT, "0" * 40)}),
        ({"STEP48_RESULT_BAD"}, {"result": result + "\n## Step 48\nStatus: FAIL\n", "active": active, "parent": parent, "handover": handover}),
        ({"STEP48_ACTIVE_LEDGER_BAD"}, {"result": result, "active": active + "\n## Step 48\nGate: CONDITIONAL\n", "parent": parent, "handover": handover}),
        ({"STEP48_PARENT_LEDGER_BAD"}, {"result": result, "active": active, "parent": parent + "\nStep 48\n------\nFAIL\n", "handover": handover}),
        ({"STEP48_HANDOVER_BAD"}, {"result": result, "active": active, "parent": parent, "handover": handover + "\n> ## Step 48\n> BLOCKED\n"}),
        (set(), {"result": result + "\n## Historical Step 40\nStatus: FAIL\n", "active": active, "parent": parent, "handover": handover}),
        (set(), {"result": result, "active": active + "\n## Historical Step 40\nFAIL\n", "parent": parent, "handover": handover}),
        (set(), {"result": result, "active": active, "parent": parent + "\n## Historical Step 40\nCONDITIONAL\n", "handover": handover}),
        (set(), {"result": result, "active": active, "parent": parent, "handover": handover + "\n## Historical Step 40\nBLOCKED\n"}),
    ]
    passed = 0
    for wanted, kwargs in cases:
        observed = control_diagnostics(**kwargs)
        if observed == wanted:
            passed += 1
        else:
            print(f"FAIL CONTROL_BOUNDARY expected={sorted(wanted)} observed={sorted(observed)}")
    return passed, len(cases)


def parse_porcelain_z(data: bytes) -> dict[str, str]:
    result: dict[str, str] = {}
    fields = data.split(b"\0")
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        text = field.decode("utf-8")
        status, path = text[:2], text[3:].replace("\\", "/")
        if status[0] in {"R", "C"}:
            if index >= len(fields):
                raise ValidationError("PORCELAIN_RENAME")
            index += 1
        result[path] = status
    return result


def remote_tip(branch: str) -> str:
    output = run_git_text(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"], "LS_REMOTE")
    parts = output.split()
    if len(parts) != 2 or parts[1] != f"refs/heads/{branch}":
        raise ValidationError("LS_REMOTE_SHAPE")
    return parts[0]


def live_repository_evidence() -> dict[str, Any]:
    dirty = parse_porcelain_z(run_git_bytes(["status", "--porcelain=v1", "-z", "--untracked-files=all"], "STATUS"))
    staged = set(run_git_text(["diff", "--cached", "--name-only"], "STAGED").splitlines())
    unstaged = set(run_git_text(["diff", "--name-only"], "UNSTAGED").splitlines())
    return {
        "branch": run_git_text(["branch", "--show-current"], "BRANCH"),
        "head": run_git_text(["rev-parse", "HEAD"], "HEAD"),
        "dirty": set(dirty), "staged": staged, "unstaged": unstaged,
        "active_remote": remote_tip(ACTIVE_BRANCH),
        "protected_local": run_git_text(["rev-parse", f"origin/{PROTECTED_BRANCH}"], "PROTECTED_LOCAL"),
        "protected_live": remote_tip(PROTECTED_BRANCH),
        "main_local": run_git_text(["rev-parse", "origin/main"], "MAIN_LOCAL"),
        "main_live": remote_tip(MAIN_BRANCH),
        "claude_diff": set(run_git_text(["diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude"], "CLAUDE_DIFF").splitlines()),
    }


def repository_diagnostics(evidence: dict[str, Any], verify_staged: bool = False) -> set[str]:
    diagnostics: set[str] = set()
    add_if(diagnostics, evidence.get("branch") != ACTIVE_BRANCH, "REPOSITORY_ACTIVE_BRANCH")
    add_if(diagnostics, evidence.get("head") != EXPECTED_PARENT, "REPOSITORY_PARENT")
    add_if(diagnostics, set(evidence.get("dirty", set())) != set(EXACT_EIGHT), "REPOSITORY_EXACT_EIGHT_DIRT")
    add_if(diagnostics, evidence.get("active_remote") != EXPECTED_PARENT, "REPOSITORY_ACTIVE_REMOTE")
    add_if(diagnostics, evidence.get("protected_local") != "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71" or evidence.get("protected_live") != "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71", "REPOSITORY_PROTECTED_STATE")
    add_if(diagnostics, evidence.get("main_local") != "4069cb36a8a52b1b88c29d68aa54dcbe915b1618" or evidence.get("main_live") != "4069cb36a8a52b1b88c29d68aa54dcbe915b1618", "REPOSITORY_MAIN_STATE")
    add_if(diagnostics, bool(evidence.get("claude_diff")), "REPOSITORY_CLAUDE_DRIFT")
    if verify_staged:
        add_if(diagnostics, set(evidence.get("staged", set())) != set(EXACT_EIGHT), "STAGING_EXACT_EIGHT")
        add_if(diagnostics, bool(evidence.get("unstaged")), "STAGING_UNSTAGED_CHANGES")
    return diagnostics


def run_repository_boundary_probes() -> tuple[int, int]:
    base = {
        "branch": ACTIVE_BRANCH, "head": EXPECTED_PARENT, "dirty": set(EXACT_EIGHT),
        "staged": set(EXACT_EIGHT), "unstaged": set(), "active_remote": EXPECTED_PARENT,
        "protected_local": "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71",
        "protected_live": "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71",
        "main_local": "4069cb36a8a52b1b88c29d68aa54dcbe915b1618",
        "main_live": "4069cb36a8a52b1b88c29d68aa54dcbe915b1618", "claude_diff": set(),
    }
    cases = [
        (set(), {}),
        ({"REPOSITORY_ACTIVE_BRANCH"}, {"branch": "main"}),
        ({"REPOSITORY_PARENT"}, {"head": "0" * 40}),
        ({"REPOSITORY_EXACT_EIGHT_DIRT"}, {"dirty": set(EXACT_EIGHT) - {EXACT_EIGHT[-1]}}),
        ({"REPOSITORY_EXACT_EIGHT_DIRT"}, {"dirty": set(EXACT_EIGHT) | {"unexpected"}}),
        ({"REPOSITORY_ACTIVE_REMOTE"}, {"active_remote": "0" * 40}),
        ({"REPOSITORY_PROTECTED_STATE"}, {"protected_live": "0" * 40}),
        ({"REPOSITORY_MAIN_STATE"}, {"main_live": "0" * 40}),
        ({"REPOSITORY_CLAUDE_DRIFT"}, {"claude_diff": {"Claude/x"}}),
        ({"STAGING_EXACT_EIGHT"}, {"staged": set(EXACT_EIGHT) - {EXACT_EIGHT[-1]}}),
        ({"STAGING_EXACT_EIGHT"}, {"staged": set(EXACT_EIGHT) | {"unexpected"}}),
        ({"STAGING_UNSTAGED_CHANGES"}, {"unstaged": {EXACT_EIGHT[0]}}),
    ]
    passed = 0
    for wanted, changes in cases:
        fixture = copy.deepcopy(base)
        fixture.update(changes)
        observed = repository_diagnostics(fixture, verify_staged=True)
        if observed == wanted:
            passed += 1
        else:
            print(f"FAIL REPOSITORY_BOUNDARY expected={sorted(wanted)} observed={sorted(observed)}")
    return passed, len(cases)


def persistence_diagnostics(evidence: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    head = evidence.get("head")
    add_if(diagnostics, evidence.get("branch") != ACTIVE_BRANCH, "PERSISTENCE_BRANCH")
    add_if(diagnostics, not isinstance(head, str) or head == EXPECTED_PARENT, "PERSISTENCE_CONTAINING_COMMIT")
    if isinstance(head, str) and head != EXPECTED_PARENT:
        parent = run_git_text(["rev-parse", f"{head}^"], "PERSISTENCE_PARENT")
        subject = run_git_text(["show", "-s", "--format=%s", head], "PERSISTENCE_SUBJECT")
        files = set(run_git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", head], "PERSISTENCE_FILES").splitlines())
        add_if(diagnostics, parent != EXPECTED_PARENT, "PERSISTENCE_PARENT")
        add_if(diagnostics, subject != EXPECTED_SUBJECT, "PERSISTENCE_SUBJECT")
        add_if(diagnostics, files != set(EXACT_EIGHT), "PERSISTENCE_EXACT_EIGHT")
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASELINE, head], cwd=REPO,
            check=False, capture_output=True, timeout=30,
        )
        add_if(diagnostics, ancestry.returncode != 0, "PERSISTENCE_ANCESTRY")
    add_if(diagnostics, evidence.get("active_remote") != head, "PERSISTENCE_ACTIVE_REMOTE")
    add_if(diagnostics, bool(evidence.get("dirty")), "PERSISTENCE_DIRTY")
    add_if(diagnostics, evidence.get("protected_local") != "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71" or evidence.get("protected_live") != "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71", "PERSISTENCE_PROTECTED")
    add_if(diagnostics, evidence.get("main_local") != "4069cb36a8a52b1b88c29d68aa54dcbe915b1618" or evidence.get("main_live") != "4069cb36a8a52b1b88c29d68aa54dcbe915b1618", "PERSISTENCE_MAIN")
    add_if(diagnostics, bool(evidence.get("claude_diff")), "PERSISTENCE_CLAUDE")
    return diagnostics


def validate(
    *, content_only: bool, run_negative: bool, run_boundary: bool,
    run_determinism: bool, verify_staged: bool, verify_persistence: bool,
) -> tuple[set[str], dict[str, tuple[int, int]]]:
    diagnostics: set[str] = set()
    metrics: dict[str, tuple[int, int]] = {}
    for path, code in (
        (BUILDER, "STEP48_BUILDER_MISSING"),
        (LINEAGE, "STEP48_LINEAGE_MATRIX_MISSING"),
        (SNAPSHOT, "STEP48_SNAPSHOT_GENEALOGY_MISSING"),
    ):
        if not path.is_file():
            diagnostics.add(code)
    if diagnostics:
        return diagnostics, metrics

    builder_bytes = BUILDER.read_bytes()
    diagnostics |= builder_security_diagnostics(builder_bytes)
    try:
        lineage_bytes, snapshot_bytes = LINEAGE.read_bytes(), SNAPSHOT.read_bytes()
        lineage, snapshot = strict_load_bytes(lineage_bytes), strict_load_bytes(snapshot_bytes)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as exc:
        return diagnostics | {f"STRICT_JSON:{type(exc).__name__}"}, metrics
    add_if(diagnostics, lineage_bytes != pretty_bytes(lineage), "LINEAGE_CANONICAL_BYTES")
    add_if(diagnostics, snapshot_bytes != pretty_bytes(snapshot), "SNAPSHOT_CANONICAL_BYTES")
    expected = independent_expected()
    diagnostics |= content_diagnostics(lineage, snapshot, expected)

    with tempfile.TemporaryDirectory(prefix="p061_step48_rebuild_") as name:
        rebuilt_lineage, rebuilt_snapshot, _ = run_builder_once(Path(name))
    add_if(diagnostics, rebuilt_lineage != lineage_bytes or rebuilt_snapshot != snapshot_bytes, "BUILDER_STORED_RECONSTRUCTION")

    if not bracket_escape_fixture():
        diagnostics.add("LINEAGE_BRACKET_DISPLAY_ESCAPE")
    if run_negative:
        passed, total = run_negative_controls(lineage, snapshot, expected)
        metrics["negative"] = (passed, total)
        add_if(diagnostics, passed != total, "NEGATIVE_CONTROLS")
        strict_passed, strict_total = strict_json_negative_controls()
        metrics["strict_negative"] = (strict_passed, strict_total)
        add_if(diagnostics, strict_passed != strict_total, "STRICT_JSON_NEGATIVE_CONTROLS")
    if run_boundary:
        control_passed, control_total = run_control_boundary_probes()
        repo_passed, repo_total = run_repository_boundary_probes()
        metrics["boundary"] = (control_passed + repo_passed, control_total + repo_total)
        add_if(diagnostics, control_passed != control_total or repo_passed != repo_total, "BOUNDARY_CONTROLS")
    if run_determinism:
        passed, total = determinism_check(lineage_bytes, snapshot_bytes)
        metrics["determinism"] = (passed, total)
        add_if(diagnostics, passed != total, "DETERMINISM")

    if not content_only:
        diagnostics |= control_diagnostics()
        evidence = live_repository_evidence()
        if verify_persistence:
            diagnostics |= persistence_diagnostics(evidence)
        else:
            diagnostics |= repository_diagnostics(evidence, verify_staged=verify_staged)
    return diagnostics, metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--run-boundary-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    args = parser.parse_args()
    try:
        diagnostics, metrics = validate(
            content_only=args.content_only,
            run_negative=args.run_negative_probes,
            run_boundary=args.run_boundary_probes,
            run_determinism=args.determinism_check,
            verify_staged=args.verify_staged,
            verify_persistence=args.verify_persistence,
        )
    except (
        ValidationError, DuplicateKeyError, NonFiniteNumberError, UnicodeError,
        json.JSONDecodeError, SyntaxError, OSError, subprocess.SubprocessError,
    ) as exc:
        print(f"FAIL STEP48_VALIDATOR_ERROR {type(exc).__name__}:{exc}")
        return 1
    for name, (passed, total) in metrics.items():
        label = name.upper()
        print(f"PASS_P061_STEP48_{label}_CONTROLS {passed}/{total}" if name != "determinism" else f"PASS_P061_STEP48_DETERMINISM {passed}/{total}")
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        print(f"FAIL_P061_STEP48_LINEAGE_DIFF diagnostics={len(diagnostics)}")
        return 1
    print(
        "PASS_P061_STEP48_LINEAGE_DIFF "
        "v1020=232 old_release=66 paired=54 deleted=12 "
        "classes=178/29/18/7/0 snapshots=10/9 edges=9 external_science_promoted=0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
