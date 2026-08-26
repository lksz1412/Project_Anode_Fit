#!/usr/bin/env python3
"""Build deterministic Phase 061 Step 48 lineage and snapshot evidence.

The builder reads only frozen Git objects plus already-persisted Codex evidence.  It
does not import or execute historical production or test modules.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


class BuildError(RuntimeError):
    """Controlled build failure."""


class DuplicateKeyError(BuildError):
    """Strict JSON duplicate-key failure."""


class NonFiniteNumberError(BuildError):
    """Strict JSON non-finite-number failure."""


REPO = Path(__file__).resolve().parents[3]
BASELINE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
INPUT_COMMIT = "46f17a9863b5a2ce0708524b09601930000e233f"
GENERATED_DATE = "2026-08-26"

TOPOLOGY_PATH = Path("Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json")
PROCESS_PATH = Path("Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json")
MANIFEST_PATH = Path("Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json")
V1019_TOPOLOGY_PATH = Path("Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json")
DEFAULT_LINEAGE = Path("Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json")
DEFAULT_SNAPSHOT = Path("Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json")

EXPECTED_INPUT_SHA256 = {
    TOPOLOGY_PATH.as_posix(): "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c",
    PROCESS_PATH.as_posix(): "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403",
    MANIFEST_PATH.as_posix(): "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef",
    V1019_TOPOLOGY_PATH.as_posix(): "c246a05e2d13d1d33dab1682bda712611367412d241cd277694a35aaf7bcf140",
}

V1020_PREFIX = "Claude/docs/v1.0.20/"
V1019_PREFIX = "Claude/docs/v1.0.19/"
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

TEXT_EXTENSIONS = {"md", "py", "tex", "txt", "json"}
DISPLAY_ENVIRONMENTS = "equation|align|gather|multline|eqnarray|displaymath"
DISPLAY_RE = re.compile(
    rf"\\begin\{{(?P<env>(?:{DISPLAY_ENVIRONMENTS})\*?)\}}"
    rf"(?P<body>.*?)\\end\{{(?P=env)\}}",
    re.DOTALL,
)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}")
INCLUDE_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")

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


def _reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_load_bytes(data: bytes) -> Any:
    return json.loads(
        data.decode("utf-8"), object_pairs_hook=_object_pairs, parse_constant=_reject_constant
    )


def walk_finite(value: Any) -> tuple[int, int]:
    nodes = 1
    depth = 1
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return nodes, depth
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NonFiniteNumberError(str(value))
        return nodes, depth
    if isinstance(value, list):
        child = [walk_finite(item) for item in value]
    elif isinstance(value, dict):
        child = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise BuildError("JSON_NONSTRING_KEY")
            child.append(walk_finite(item))
    else:
        raise BuildError(f"JSON_TYPE:{type(value).__name__}")
    if child:
        nodes += sum(item[0] for item in child)
        depth += max(item[1] for item in child)
    return nodes, depth


def lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def run_git(args: list[str], diagnostic: str, timeout: int = 60) -> bytes:
    completed = subprocess.run(
        ["git", *args], cwd=REPO, check=False, capture_output=True, timeout=timeout
    )
    if completed.returncode != 0:
        raise BuildError(f"{diagnostic}:{completed.returncode}")
    return completed.stdout


def git_blob_batch(shas: list[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(shas))
    completed = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input=("\n".join(ordered) + "\n").encode("ascii"),
        check=False, capture_output=True, timeout=120,
    )
    if completed.returncode != 0:
        raise BuildError(f"GIT_CAT_FILE_BATCH:{completed.returncode}")
    stream = memoryview(completed.stdout)
    offset = 0
    result: dict[str, bytes] = {}
    for expected in ordered:
        newline = completed.stdout.find(b"\n", offset)
        if newline < 0:
            raise BuildError("GIT_CAT_FILE_HEADER_EOF")
        header = bytes(stream[offset:newline]).decode("ascii", errors="strict")
        offset = newline + 1
        parts = header.split()
        if len(parts) != 3 or parts[0] != expected or parts[1] != "blob":
            raise BuildError(f"GIT_CAT_FILE_HEADER:{expected}:{header}")
        size = int(parts[2])
        data = bytes(stream[offset:offset + size])
        offset += size
        if bytes(stream[offset:offset + 1]) != b"\n":
            raise BuildError(f"GIT_CAT_FILE_SEPARATOR:{expected}")
        offset += 1
        if git_blob_sha1(data) != expected:
            raise BuildError(f"GIT_BLOB_IDENTITY:{expected}")
        result[expected] = data
    if bytes(stream[offset:]):
        raise BuildError("GIT_CAT_FILE_TRAILING_DATA")
    return result


def load_input(path: Path) -> tuple[Any, dict[str, Any]]:
    data = (REPO / path).read_bytes()
    normalized = lf_bytes(data)
    actual = sha256(normalized)
    expected = EXPECTED_INPUT_SHA256[path.as_posix()]
    if actual != expected:
        raise BuildError(f"INPUT_HASH:{path.as_posix()}:{actual}")
    parsed = strict_load_bytes(data)
    nodes, depth = walk_finite(parsed)
    return parsed, {
        "path": path.as_posix(), "sha256_lf_normalized": actual,
        "physical_lines": len(normalized.splitlines()), "nodes": nodes, "maximum_depth": depth,
    }


def suffix(path: str, prefix: str) -> str:
    if not path.startswith(prefix):
        raise BuildError(f"PATH_PREFIX:{path}")
    return path[len(prefix):]


def normalized_identity(relative_path: str, role: str) -> dict[str, Any]:
    version_neutral = relative_path
    for new_name, old_name in SEMANTIC_RENAME_PAIRS.items():
        if relative_path in {new_name, old_name}:
            version_neutral = new_name
            break
    parts = Path(version_neutral).parts
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
        artifact_form = "LATEX_SOURCE"
    elif filename.endswith(".pdf"):
        artifact_form = "GENERATED_PDF"
    elif filename.endswith(".py"):
        artifact_form = "PYTHON_SOURCE"
    elif filename.endswith(".png"):
        artifact_form = "RASTER_IMAGE"
    else:
        artifact_form = "TEXT_OR_STRUCTURED_RECORD"
    family = "/".join(parts[:-1]) or "ROOT"
    return {
        "role": role, "document_family": family, "chapter": chapter,
        "section_or_artifact": filename, "artifact_form": artifact_form,
        "version_neutral_key": f"{role}|{family}|{chapter}|{filename}|{artifact_form}",
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
    old_lf, new_lf = lf_bytes(old), lf_bytes(new)
    old_lines = old_lf.decode("utf-8").splitlines()
    new_lines = new_lf.decode("utf-8").splitlines()
    segments: list[dict[str, Any]] = []
    for tag, old_start, old_end, new_start, new_end in difflib.SequenceMatcher(
        None, old_lines, new_lines, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            continue
        old_slice = old_lines[old_start:old_end]
        new_slice = new_lines[new_start:new_end]
        segment = {
            "tag": tag,
            "old_line_start": old_start + 1,
            "old_line_end": old_end,
            "new_line_start": new_start + 1,
            "new_line_end": new_end,
            "old_lines": old_slice,
            "new_lines": new_slice,
        }
        segment["segment_sha256"] = sha256(canonical_json_bytes(segment))
        segments.append(segment)
    return {
        "old": text_record(old), "new": text_record(new),
        "segments": segments,
        "segment_count": len(segments),
        "changed_old_lines": sum(len(item["old_lines"]) for item in segments),
        "changed_new_lines": sum(len(item["new_lines"]) for item in segments),
        "exact_reconstruction_boundary": "CHANGED_SEGMENTS_PLUS_ENDPOINT_BLOBS",
    }


def bracket_display_spans(text: str) -> list[tuple[int, str]]:
    commands: list[tuple[int, str]] = []
    for index, char in enumerate(text):
        if char not in "[]":
            continue
        preceding_backslashes = 0
        cursor = index - 1
        while cursor >= 0 and text[cursor] == "\\":
            preceding_backslashes += 1
            cursor -= 1
        if preceding_backslashes % 2 == 1:
            commands.append((index - 1, char))

    spans: list[tuple[int, str]] = []
    open_start: int | None = None
    for command_start, bracket in commands:
        if bracket == "[":
            if open_start is None:
                open_start = command_start
        elif open_start is not None:
            spans.append((open_start, text[open_start:command_start + 2]))
            open_start = None
    return spans


def latex_equations(text: str) -> list[dict[str, Any]]:
    text = latex_without_comments(text)
    matches: list[tuple[int, str, str]] = []
    for match in DISPLAY_RE.finditer(text):
        matches.append((match.start(), match.group("env"), match.group(0)))
    for start, raw in bracket_display_spans(text):
        matches.append((start, "bracket_display", raw))
    provisional: list[dict[str, Any]] = []
    for index, (start, environment, raw) in enumerate(sorted(matches), start=1):
        labels = LABEL_RE.findall(raw)
        line_start = text.count("\n", 0, start) + 1
        substantive = re.sub(r"\s+", " ", raw).strip()
        body_hash = sha256(substantive.encode("utf-8"))
        base_identity = (
            "LABEL:" + "|".join(labels)
            if labels else "UNLABELED_HASH:" + body_hash
        )
        provisional.append({
            "ordinal": index, "environment": environment, "line_start": line_start,
            "labels": labels, "sha256_lf_normalized": sha256(lf_bytes(raw.encode("utf-8"))),
            "substantive_sha256": body_hash, "base_identity": base_identity,
        })
    totals: dict[str, int] = {}
    for row in provisional:
        totals[row["base_identity"]] = totals.get(row["base_identity"], 0) + 1
    seen: dict[str, int] = {}
    records: list[dict[str, Any]] = []
    for row in provisional:
        base = row.pop("base_identity")
        seen[base] = seen.get(base, 0) + 1
        row["semantic_identity"] = (
            base if totals[base] == 1 else f"{base}#OCCURRENCE-{seen[base]:03d}"
        )
        records.append(row)
    return records


def bibliography_records(text: str) -> dict[str, dict[str, Any]]:
    matches = list(BIBITEM_RE.finditer(text))
    records: dict[str, dict[str, Any]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        key = match.group(1)
        if key in records:
            raise BuildError(f"DUPLICATE_BIBITEM:{key}")
        raw = text[match.start():end].rstrip()
        records[key] = {
            "line_start": text.count("\n", 0, match.start()) + 1,
            "sha256_lf_normalized": sha256(lf_bytes(raw.encode("utf-8"))),
        }
    return records


def latex_without_comments(text: str) -> str:
    return "\n".join(re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines())


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


def equation_semantic_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    shared = sorted(set(before) & set(after))
    substantive_fields = ("environment", "labels", "sha256_lf_normalized", "substantive_sha256")
    changed = []
    moved = []
    unchanged = []
    for key in shared:
        if any(before[key][field] != after[key][field] for field in substantive_fields):
            changed.append({"key": key, "before": before[key], "after": after[key]})
        elif (
            before[key]["ordinal"] != after[key]["ordinal"]
            or before[key]["line_start"] != after[key]["line_start"]
        ):
            moved.append({"key": key, "before": before[key], "after": after[key]})
        else:
            unchanged.append(key)
    return {
        "added": [{"key": key, "after": after[key]} for key in sorted(set(after) - set(before))],
        "removed": [{"key": key, "before": before[key]} for key in sorted(set(before) - set(after))],
        "changed": changed, "moved": moved,
        "unchanged_count": len(unchanged),
        "unchanged_projection_sha256": sha256(canonical_json_bytes(unchanged)),
    }


def latex_delta(old: bytes, new: bytes) -> dict[str, Any]:
    old_text, new_text = lf_bytes(old).decode("utf-8"), lf_bytes(new).decode("utf-8")
    old_clean, new_clean = latex_without_comments(old_text), latex_without_comments(new_text)
    old_eq = {row["semantic_identity"]: row for row in latex_equations(old_clean)}
    new_eq = {row["semantic_identity"]: row for row in latex_equations(new_clean)}
    if len(old_eq) != len(latex_equations(old_clean)) or len(new_eq) != len(latex_equations(new_clean)):
        raise BuildError("LATEX_EQUATION_IDENTITY_COLLISION")
    old_labels, new_labels = set(LABEL_RE.findall(old_clean)), set(LABEL_RE.findall(new_clean))
    old_includes = INCLUDE_RE.findall(old_clean)
    new_includes = INCLUDE_RE.findall(new_clean)
    return {
        "labels": {
            "before": len(old_labels), "after": len(new_labels),
            "added": sorted(new_labels - old_labels), "removed": sorted(old_labels - new_labels),
        },
        "equation_blocks_by_semantic_identity": equation_semantic_delta(old_eq, new_eq),
        "bibliography": keyed_delta(bibliography_records(old_clean), bibliography_records(new_clean)),
        "include_topology": {
            "before": old_includes, "after": new_includes,
            "added": sorted(set(new_includes) - set(old_includes)),
            "removed": sorted(set(old_includes) - set(new_includes)),
        },
    }


def latex_inventory(data: bytes) -> dict[str, Any]:
    text = latex_without_comments(lf_bytes(data).decode("utf-8"))
    equations = latex_equations(text)
    bibliography = bibliography_records(text)
    includes = INCLUDE_RE.findall(text)
    return {
        "labels": sorted(set(LABEL_RE.findall(text))),
        "equation_blocks": equations,
        "bibliography": bibliography,
        "ordered_includes": includes,
        "authority_ceiling": "SOURCE_STRUCTURE_ONLY",
    }


def stable_ast_projection(value: Any) -> Any:
    if isinstance(value, ast.AST):
        result: dict[str, Any] = {"_type": type(value).__name__}
        for field in value._fields:
            item = getattr(value, field, None)
            if item is None or item == []:
                continue
            result[field] = stable_ast_projection(item)
        return result
    if isinstance(value, (list, tuple)):
        return [stable_ast_projection(item) for item in value]
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if value is Ellipsis:
        return {"_ellipsis": True}
    if isinstance(value, complex):
        return {"_complex_repr": repr(value)}
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(str(value))
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    raise BuildError(f"AST_PROJECTION_TYPE:{type(value).__name__}")


def stable_ast_sha(node: ast.AST) -> str:
    return sha256(canonical_json_bytes(stable_ast_projection(node)))


class DefinitionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.stack: list[str] = []
        self.records: dict[str, str] = {}

    def _visit_definition(self, node: ast.AST, name: str) -> None:
        qualified = ".".join((*self.stack, name))
        self.records[qualified] = stable_ast_sha(node)
        self.stack.append(name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_definition(node, node.name)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_definition(node, node.name)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_definition(node, node.name)


def python_structure_delta(old: bytes, new: bytes) -> dict[str, Any]:
    old_tree = ast.parse(old.decode("utf-8"))
    new_tree = ast.parse(new.decode("utf-8"))
    old_visitor, new_visitor = DefinitionVisitor(), DefinitionVisitor()
    old_visitor.visit(old_tree)
    new_visitor.visit(new_tree)
    old_defs, new_defs = old_visitor.records, new_visitor.records
    old_ast = stable_ast_sha(old_tree)
    new_ast = stable_ast_sha(new_tree)
    def module_stats(tree: ast.AST) -> dict[str, Any]:
        nodes = list(ast.walk(tree))
        imports = sorted(
            alias.name
            for node in nodes if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        )
        calls = sum(isinstance(node, ast.Call) for node in nodes)
        executable_literals = sum(
            isinstance(node, ast.Constant) and not isinstance(node.value, (type(None), bool))
            for node in nodes
        )
        return {
            "ast_nodes": len(nodes), "imports": imports,
            "calls": calls, "executable_literals": executable_literals,
        }
    old_stats, new_stats = module_stats(old_tree), module_stats(new_tree)
    return {
        "old_module_ast_sha256": old_ast, "new_module_ast_sha256": new_ast,
        "ast_projection_contract": "NONEMPTY_FIELDS_CANONICAL_JSON_V1",
        "module_ast_identical": old_ast == new_ast,
        "definitions_before": len(old_defs), "definitions_after": len(new_defs),
        "added_definitions": sorted(set(new_defs) - set(old_defs)),
        "removed_definitions": sorted(set(old_defs) - set(new_defs)),
        "changed_definitions": sorted(
            key for key in set(old_defs) & set(new_defs) if old_defs[key] != new_defs[key]
        ),
        "unchanged_definitions": sorted(
            key for key in set(old_defs) & set(new_defs) if old_defs[key] == new_defs[key]
        ),
        "old_structure_stats": old_stats, "new_structure_stats": new_stats,
        "execution_performed": False,
        "behavioral_change_state": "UNVERIFIED_NO_RUNTIME_EXECUTION",
        "authority_ceiling": "FROZEN_SOURCE_STRUCTURE_ONLY_NOT_RUNTIME_BEHAVIOR",
    }


def snapshot_chapter(snapshot: dict[str, Any], chapter_number: int) -> dict[str, Any]:
    marker = f"_ch{chapter_number}_"
    matches = [value for key, value in snapshot.items() if marker in key]
    if len(matches) != 1:
        raise BuildError(f"SNAPSHOT_CHAPTER_CARDINALITY:{chapter_number}:{len(matches)}")
    return matches[0]


def validate_snapshot(snapshot: Any, alias: str) -> dict[str, Any]:
    if not isinstance(snapshot, dict) or len(snapshot) not in {2, 3}:
        raise BuildError(f"SNAPSHOT_ROOT_SCHEMA:{alias}")
    for root, chapter in snapshot.items():
        if not isinstance(root, str) or not isinstance(chapter, dict):
            raise BuildError(f"SNAPSHOT_ROOT_TYPE:{alias}")
        if set(chapter) != {"labels", "eqblocks", "asset_unique", "bibitems"}:
            raise BuildError(f"SNAPSHOT_CHAPTER_FIELDS:{alias}:{root}")
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
            raise BuildError(f"SNAPSHOT_CHAPTER_TYPE:{alias}:{root}")
        for identifier, block in chapter["eqblocks"].items():
            if (
                not isinstance(identifier, str) or not isinstance(block, dict)
                or set(block) != {"hash", "boxed", "file"}
                or not isinstance(block["hash"], str)
                or not isinstance(block["boxed"], bool)
                or not isinstance(block["file"], str)
            ):
                raise BuildError(f"SNAPSHOT_EQBLOCK_SCHEMA:{alias}:{root}:{identifier}")
    return snapshot


def chapter_projection(chapter: dict[str, Any]) -> dict[str, Any]:
    return {
        "labels": sorted(chapter["labels"]),
        "eqblocks": [
            {"identifier": key, **value} for key, value in sorted(chapter["eqblocks"].items())
        ],
        "asset_unique": chapter["asset_unique"],
        "bibitems": sorted(chapter["bibitems"]),
    }


def normalized_snapshot_root(root_name: str) -> str:
    return root_name.replace("v1.0.19", "VERSION").replace("v1.0.20", "VERSION")


def document_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    all_roots = [
        {
            "raw_root_name": root_name,
            "normalized_root_name": normalized_snapshot_root(root_name),
            "content": chapter_projection(chapter),
        }
        for root_name, chapter in sorted(snapshot.items())
    ]
    return {
        "raw_roots": sorted(snapshot),
        "normalized_roots": sorted(normalized_snapshot_root(root) for root in snapshot),
        "all_root_projections": all_roots,
        "ch1": chapter_projection(snapshot_chapter(snapshot, 1)),
        "ch2": chapter_projection(snapshot_chapter(snapshot, 2)),
    }


def set_delta(before: list[str], after: list[str]) -> dict[str, Any]:
    return {
        "count_before": len(before), "count_after": len(after),
        "count_delta": len(after) - len(before),
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
    }


def snapshot_eq_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_map = {row["identifier"]: {k: row[k] for k in ("hash", "boxed", "file")} for row in before["eqblocks"]}
    after_map = {row["identifier"]: {k: row[k] for k in ("hash", "boxed", "file")} for row in after["eqblocks"]}
    substantive_before = sorted(
        before_map.values(), key=lambda row: (row["hash"], row["boxed"], row["file"])
    )
    substantive_after = sorted(
        after_map.values(), key=lambda row: (row["hash"], row["boxed"], row["file"])
    )
    return {
        "count_before": len(before_map), "count_after": len(after_map),
        "added": [{"identifier": key, **after_map[key]} for key in sorted(set(after_map) - set(before_map))],
        "removed": [{"identifier": key, **before_map[key]} for key in sorted(set(before_map) - set(after_map))],
        "changed": [
            {"identifier": key, "before": before_map[key], "after": after_map[key]}
            for key in sorted(set(before_map) & set(after_map)) if before_map[key] != after_map[key]
        ],
        "substantive_projection_equal": substantive_before == substantive_after,
        "substantive_before_sha256": sha256(canonical_json_bytes(substantive_before)),
        "substantive_after_sha256": sha256(canonical_json_bytes(substantive_after)),
    }


def snapshot_edge(before_alias: str, after_alias: str, projections: dict[str, dict[str, Any]]) -> dict[str, Any]:
    before, after = projections[before_alias], projections[after_alias]
    chapters: dict[str, Any] = {}
    for chapter in ("ch1", "ch2"):
        chapters[chapter] = {
            "labels": set_delta(before[chapter]["labels"], after[chapter]["labels"]),
            "eqblocks": snapshot_eq_delta(before[chapter], after[chapter]),
            "bibitems": set_delta(before[chapter]["bibitems"], after[chapter]["bibitems"]),
            "asset_unique_before": before[chapter]["asset_unique"],
            "asset_unique_after": after[chapter]["asset_unique"],
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
        "before_projection_sha256": sha256(canonical_json_bytes(before)),
        "after_projection_sha256": sha256(canonical_json_bytes(after)),
        "document_projection_equal": normalized_before == normalized_after,
        "raw_root_delta": set_delta(before["raw_roots"], after["raw_roots"]),
        "normalized_root_delta": set_delta(before["normalized_roots"], after["normalized_roots"]),
        "chapters": chapters,
        "authority_ceiling": "CAPTURED_STRUCTURE_ONLY",
        "external_scientific_truth": False,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    topology, topology_input = load_input(TOPOLOGY_PATH)
    process, process_input = load_input(PROCESS_PATH)
    manifest, manifest_input = load_input(MANIFEST_PATH)
    v1019_topology, v1019_topology_input = load_input(V1019_TOPOLOGY_PATH)
    inputs = [topology_input, process_input, manifest_input, v1019_topology_input]

    if topology.get("baseline_commit") != BASELINE_COMMIT or process.get("baseline_commit") != BASELINE_COMMIT:
        raise BuildError("BASELINE_COMMIT")
    if manifest.get("baseline_commit") != BASELINE_COMMIT:
        raise BuildError("MANIFEST_BASELINE")
    if v1019_topology.get("baseline_commit") != BASELINE_COMMIT:
        raise BuildError("V1019_TOPOLOGY_BASELINE")
    sources = topology.get("sources")
    routes = process.get("source_routes")
    entries = manifest.get("entries")
    if not isinstance(sources, list) or len(sources) != 232:
        raise BuildError("TOPOLOGY_SOURCE_COUNT")
    if not isinstance(routes, list) or len(routes) != 232:
        raise BuildError("PROCESS_ROUTE_COUNT")
    if not isinstance(entries, list):
        raise BuildError("MANIFEST_ENTRIES")
    route_by_id = {row["source_id"]: row for row in routes}
    if len(route_by_id) != 232:
        raise BuildError("PROCESS_ROUTE_IDS")
    for source in sources:
        route = route_by_id.get(source["source_id"])
        if route is None or route["path"] != source["path"] or route["blob_sha1"] != source["blob_sha1"]:
            raise BuildError(f"TOPOLOGY_PROCESS_LINK:{source['source_id']}")

    old_entries = [row for row in entries if row.get("version") == "v1.0.19"]
    new_entries = [row for row in entries if row.get("version") == "v1.0.20"]
    if len(old_entries) != 66 or len(new_entries) != 232:
        raise BuildError(f"MANIFEST_VERSION_COUNTS:{len(old_entries)}:{len(new_entries)}")
    old_topology_primary = [
        row for row in v1019_topology.get("sources", [])
        if row.get("occurrence_kind") == "PRIMARY_RELEASE"
    ]
    if len(old_topology_primary) != 66:
        raise BuildError(f"V1019_TOPOLOGY_PRIMARY_COUNT:{len(old_topology_primary)}")
    old_topology_by_path = {row["path"]: row for row in old_topology_primary}
    if len(old_topology_by_path) != 66:
        raise BuildError("V1019_TOPOLOGY_PRIMARY_DUPLICATE")
    for old_row in old_entries:
        topology_row = old_topology_by_path.get(old_row["path"])
        if topology_row is None or topology_row["git_blob_sha1"] != old_row["blob_sha"]:
            raise BuildError(f"V1019_TOPOLOGY_MANIFEST_LINK:{old_row['path']}")
    old_by_relative = {suffix(row["path"], V1019_PREFIX): row for row in old_entries}
    new_manifest_by_path = {row["path"]: row for row in new_entries}
    if len(old_by_relative) != 66 or len(new_manifest_by_path) != 232:
        raise BuildError("MANIFEST_PATH_DUPLICATE")

    all_shas = [row["blob_sha"] for row in old_entries] + [row["blob_sha1"] for row in sources]
    blobs = git_blob_batch(all_shas)
    used_old_paths: set[str] = set()
    delta_rows: list[dict[str, Any]] = []
    class_counts = {key: 0 for key in ("ADDED", "MODIFIED", "UNCHANGED", "RENAMED", "COPIED")}
    paired_text_hunks = 0
    changed_old_lines = 0
    changed_new_lines = 0
    python_pairs: list[dict[str, Any]] = []

    for source in sources:
        path = source["path"]
        relative = suffix(path, V1020_PREFIX)
        route = route_by_id[source["source_id"]]
        manifest_row = new_manifest_by_path.get(path)
        if manifest_row is None or manifest_row["blob_sha"] != source["blob_sha1"]:
            raise BuildError(f"NEW_MANIFEST_LINK:{source['source_id']}")
        old_relative: str | None
        pair_basis: str
        if relative in old_by_relative:
            old_relative, pair_basis = relative, "FULL_VERSION_RELATIVE_PATH"
        elif relative in SEMANTIC_RENAME_PAIRS:
            old_relative, pair_basis = SEMANTIC_RENAME_PAIRS[relative], "VERSIONED_ROLE_CHAPTER_SECTION_IDENTITY"
        else:
            old_relative, pair_basis = None, "NO_V1019_COUNTERPART"
        old_row = old_by_relative.get(old_relative) if old_relative is not None else None
        new_identity = normalized_identity(relative, source["manifest_role"])
        old_identity = None if old_row is None else normalized_identity(
            suffix(old_row["path"], V1019_PREFIX), old_row["role"]
        )
        if old_identity is not None and old_identity["version_neutral_key"] != new_identity["version_neutral_key"]:
            raise BuildError(f"NORMALIZED_IDENTITY_MISMATCH:{source['source_id']}")
        new_data = blobs[source["blob_sha1"]]
        if sha256(new_data) != source["sha256"] or len(new_data) != source["size_bytes"]:
            raise BuildError(f"NEW_BLOB_EXTENT:{source['source_id']}")
        if old_row is None:
            comparison_class, path_relation, blob_relation = "ADDED", "ADDED", "NO_OLD_BLOB"
        else:
            if old_row["path"] in used_old_paths:
                raise BuildError(f"OLD_PAIR_REUSE:{old_row['path']}")
            used_old_paths.add(old_row["path"])
            if old_relative != relative:
                comparison_class, path_relation = "RENAMED", "RENAMED_VERSIONED_IDENTITY"
            elif old_row["blob_sha"] == source["blob_sha1"]:
                comparison_class, path_relation = "UNCHANGED", "SAME_RELATIVE_PATH"
            else:
                comparison_class, path_relation = "MODIFIED", "SAME_RELATIVE_PATH"
            blob_relation = "IDENTICAL" if old_row["blob_sha"] == source["blob_sha1"] else "CHANGED"
        class_counts[comparison_class] += 1
        row: dict[str, Any] = {
            "delta_id": f"P061-DELTA-{int(source['source_id'].rsplit('-', 1)[1]):04d}",
            "v1020_source_id": source["source_id"],
            "manifest_index_v1020": source["manifest_index_v1020"],
            "comparison_class": comparison_class,
            "pair_basis": pair_basis,
            "normalized_identity": new_identity,
            "old_normalized_identity": old_identity,
            "candidate_count": 0 if old_row is None else 1,
            "selected_reason": "NO_NORMALIZED_IDENTITY_CANDIDATE" if old_row is None else pair_basis,
            "path_relation": path_relation,
            "blob_relation": blob_relation,
            "v1019": None if old_row is None else {
                "path": old_row["path"], "blob_sha1": old_row["blob_sha"],
                "size_bytes": old_row["size_bytes"], "role": old_row["role"],
                "review_mode": old_row["review_mode"], "extent": old_row["extent"],
                "sha256": sha256(blobs[old_row["blob_sha"]]),
                "sha256_lf_normalized": (
                    sha256(lf_bytes(blobs[old_row["blob_sha"]]))
                    if old_row["extension"] in TEXT_EXTENSIONS else None
                ),
            },
            "v1020": {
                "path": path, "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
                "size_bytes": source["size_bytes"], "role": source["manifest_role"],
                "review_mode": source["review_mode"], "extent": source["manifest_extent"],
                "sha256_lf_normalized": (
                    sha256(lf_bytes(new_data)) if source["extension"] in TEXT_EXTENSIONS else None
                ),
            },
            "step47_authority": {
                "source_authority_class": route["source_authority_class"],
                "authority_ceiling": route["authority_ceiling"],
                "evidence_route": route["evidence_route"],
                "adoption_topology": route["adoption_topology"],
                "scientific_authority_promoted": route["scientific_authority_promoted"],
                "external_scientific_truth": route["external_scientific_truth"],
            },
            "surface_layer": route["source_authority_class"],
            "semantic_delta": "WHOLE_BLOB_ADDITION" if old_row is None else (
                "BYTE_IDENTICAL" if blob_relation == "IDENTICAL" else "EXACT_ENDPOINT_AND_TEXT_OR_BINARY_DELTA"
            ),
            "authority_limit": "LINEAGE_ONLY",
            "external_scientific_truth": False,
            "generated_output_is_source_of_record": False,
        }
        if old_row is not None:
            old_data = blobs[old_row["blob_sha"]]
            if old_row["extension"] in TEXT_EXTENSIONS and source["extension"] in TEXT_EXTENSIONS:
                row["text_delta"] = exact_text_delta(old_data, new_data)
                paired_text_hunks += row["text_delta"]["segment_count"]
                changed_old_lines += row["text_delta"]["changed_old_lines"]
                changed_new_lines += row["text_delta"]["changed_new_lines"]
            else:
                row["text_delta"] = None
            if old_row["extension"] == "tex" and source["extension"] == "tex":
                row["latex_delta"] = latex_delta(old_data, new_data)
            else:
                row["latex_delta"] = None
            if old_row["extension"] == "pdf" and source["extension"] == "pdf":
                row["pdf_delta"] = {
                    "pages_before": old_row["extent"]["pages"],
                    "pages_after": source["manifest_extent"]["pages"],
                    "page_delta": source["manifest_extent"]["pages"] - old_row["extent"]["pages"],
                    "visual_or_scientific_equivalence_inferred": False,
                }
            else:
                row["pdf_delta"] = None
            if old_row["extension"] == "py" and source["extension"] == "py":
                structure = python_structure_delta(old_data, new_data)
                row["python_structure_delta"] = structure
                python_pairs.append({
                    "v1020_source_id": source["source_id"], "old_path": old_row["path"],
                    "new_path": path, "role_pair": f"{old_row['role']}->{source['manifest_role']}",
                    **structure,
                })
            else:
                row["python_structure_delta"] = None
        else:
            row.update({
                "text_delta": None, "latex_delta": None, "pdf_delta": None,
                "python_structure_delta": None,
                "added_latex_inventory": latex_inventory(new_data) if source["extension"] == "tex" else None,
            })
        if old_row is not None:
            row["added_latex_inventory"] = None
        delta_rows.append(row)

    deleted = []
    for old_row in old_entries:
        if old_row["path"] in used_old_paths:
            continue
        deleted.append({
            "deleted_id": f"P061-OLDONLY-{len(deleted) + 1:03d}",
            "comparison_class": "DELETED_COUNTERPART",
            "v1019_path": old_row["path"], "v1019_blob_sha1": old_row["blob_sha"],
            "v1019_sha256": sha256(blobs[old_row["blob_sha"]]),
            "size_bytes": old_row["size_bytes"], "role": old_row["role"],
            "review_mode": old_row["review_mode"], "extent": old_row["extent"],
            "normalized_identity": normalized_identity(
                suffix(old_row["path"], V1019_PREFIX), old_row["role"]
            ),
            "phase060_topology_authority_class": old_topology_by_path[old_row["path"]]["authority_class"],
            "phase060_occurrence_kind": old_topology_by_path[old_row["path"]]["occurrence_kind"],
            "v1020_counterpart": None, "authority_limit": "LINEAGE_ONLY",
            "absence_is_not_behavioral_or_scientific_rejection": True,
        })

    if class_counts != {"ADDED": 178, "MODIFIED": 29, "UNCHANGED": 18, "RENAMED": 7, "COPIED": 0}:
        raise BuildError(f"CLASS_COUNTS:{class_counts}")
    if len(used_old_paths) != 54 or len(deleted) != 12:
        raise BuildError(f"PAIR_DELETE_COUNTS:{len(used_old_paths)}:{len(deleted)}")
    if len({row["v1020_source_id"] for row in delta_rows}) != 232:
        raise BuildError("DELTA_SOURCE_COVERAGE")

    snapshot_sources = {row["path"]: row for row in sources if row["path"] in SNAPSHOT_PATHS.values()}
    if len(snapshot_sources) != 10:
        raise BuildError(f"SNAPSHOT_SOURCE_COUNT:{len(snapshot_sources)}")
    snapshots: dict[str, dict[str, Any]] = {}
    projections: dict[str, dict[str, Any]] = {}
    occurrence_rows: list[dict[str, Any]] = []
    for alias, path in SNAPSHOT_PATHS.items():
        source = snapshot_sources[path]
        data = blobs[source["blob_sha1"]]
        parsed = validate_snapshot(strict_load_bytes(data), alias)
        walk_finite(parsed)
        projection = document_projection(parsed)
        snapshots[alias], projections[alias] = parsed, projection
        history = run_git(["log", "--format=%H", BASELINE_COMMIT, "--", path], f"SNAPSHOT_LOG:{alias}").decode("ascii").splitlines()
        occurrence_rows.append({
            "snapshot_id": f"P061-SNAPSHOT-{len(occurrence_rows) + 1:02d}",
            "alias": alias, "source_id": source["source_id"], "path": path,
            "blob_sha1": source["blob_sha1"], "sha256": source["sha256"],
            "physical_lines": len(lf_bytes(data).splitlines()),
            "root_names": sorted(parsed), "normalized_root_names": projection["normalized_roots"],
            "root_count": len(parsed), "stage_ordinal": len(occurrence_rows),
            "projection": projection,
            "projection_sha256": sha256(canonical_json_bytes(projection)),
            "strict_traversal": {
                "nodes": walk_finite(parsed)[0], "maximum_depth": walk_finite(parsed)[1],
            },
            "history_commits_newest_first": history,
            "history_commit_count": len(history),
            "authority_class": "STRUCTURAL_WITNESS",
            "authority_ceiling": "CAPTURED_STRUCTURE_ONLY",
            "external_scientific_truth": False,
        })
    edges = [snapshot_edge(before, after, projections) for before, after in zip(SNAPSHOT_ORDER, SNAPSHOT_ORDER[1:])]

    baseline_projection, final_projection = projections["baseline"], projections["final"]
    baseline_final = {
        "ch1": {
            "labels": set_delta(baseline_projection["ch1"]["labels"], final_projection["ch1"]["labels"]),
            "eqblocks": snapshot_eq_delta(baseline_projection["ch1"], final_projection["ch1"]),
            "bibitems": set_delta(baseline_projection["ch1"]["bibitems"], final_projection["ch1"]["bibitems"]),
        },
        "ch2": {
            "labels": set_delta(baseline_projection["ch2"]["labels"], final_projection["ch2"]["labels"]),
            "eqblocks": snapshot_eq_delta(baseline_projection["ch2"], final_projection["ch2"]),
            "bibitems": set_delta(baseline_projection["ch2"]["bibitems"], final_projection["ch2"]["bibitems"]),
        },
    }
    provisional_verified = (
        baseline_final["ch1"]["labels"]["count_delta"] == 6
        and baseline_final["ch1"]["eqblocks"]["count_after"] - baseline_final["ch1"]["eqblocks"]["count_before"] == 6
        and baseline_final["ch1"]["bibitems"]["count_delta"] == 8
        and baseline_final["ch2"]["labels"]["count_delta"] == 0
        and baseline_final["ch2"]["eqblocks"]["substantive_projection_equal"]
        and baseline_final["ch2"]["bibitems"]["count_delta"] == 2
    )
    if not provisional_verified:
        raise BuildError("PROVISIONAL_DELTA_MISMATCH")

    p5 = next(row for row in occurrence_rows if row["alias"] == "p5")
    p6 = next(row for row in occurrence_rows if row["alias"] == "p6")
    process_boundary = process.get("boundaries", {}).get("p5_p6")
    if not isinstance(process_boundary, dict):
        raise BuildError("PROCESS_P5_P6_BOUNDARY")
    if p5["history_commit_count"] != 1 or p6["history_commit_count"] != 1:
        raise BuildError("P5_P6_SNAPSHOT_HISTORY_CARDINALITY")
    p5_commit = p5["history_commits_newest_first"][0]
    p6_commit = p6["history_commits_newest_first"][0]
    p6_parent = run_git(["rev-parse", f"{p6_commit}^"], "P6_PARENT").decode("ascii").strip()
    changed_paths = sorted(
        line for line in run_git(
            ["diff-tree", "--no-commit-id", "--name-only", "-r", p5_commit, p6_commit, "--", V1020_PREFIX],
            "P5_P6_DIFF_TREE",
        ).decode("utf-8").splitlines() if line
    )
    changed_tex = sorted(path for path in changed_paths if path.endswith(".tex"))
    expected_changed_tex = [
        V1020_PREFIX + "_sections/ch1_appB_codemap.tex",
        V1020_PREFIX + "_sections/ch1_sec00_intro.tex",
        V1020_PREFIX + "appendix_phase_separation.tex",
    ]
    if (
        p5["blob_sha1"] != p6["blob_sha1"]
        or p5["path"] == p6["path"]
        or p6_parent != p5_commit
        or changed_tex != expected_changed_tex
        or process_boundary.get("p5_commit") != p5_commit
        or process_boundary.get("p6_commit") != p6_commit
        or process_boundary.get("changed_tex_paths") != changed_tex
        or process_boundary.get("actual_source_tree_identical") is not False
    ):
        raise BuildError("P5_P6_BOUNDARY")

    generation_contract_id = "P061-STEP48-V1019-V1020-LINEAGE-SNAPSHOT-V1"
    common_boundary = {
        "generation_contract_id": generation_contract_id,
        "baseline_commit": BASELINE_COMMIT,
        "input_commit": INPUT_COMMIT,
        "inputs": inputs,
        "production_or_test_modules_imported_or_executed": False,
        "external_scientific_truth_promoted": False,
        "snapshot_or_pdf_equality_certifies_scientific_correctness": False,
        "generated_output_is_source_of_record": False,
        "authority_ceiling": "FROZEN_LINEAGE_AND_CAPTURED_STRUCTURE_ONLY",
    }

    adopted_rows = [
        row for row in delta_rows
        if row["step47_authority"]["source_authority_class"] == "ADOPTED_RELEASE_SOURCE"
    ]
    final_surface_rows = [
        row for row in delta_rows
        if next(source for source in sources if source["source_id"] == row["v1020_source_id"])["derived_authority_group"]
        == "FINAL_RELEASE_SURFACE"
    ]
    def comparison_distribution(rows: list[dict[str, Any]]) -> dict[str, int]:
        return {
            key: sum(row["comparison_class"] == key for row in rows)
            for key in ("ADDED", "MODIFIED", "UNCHANGED", "RENAMED", "COPIED")
        }
    def text_extent_summary(rows: list[dict[str, Any]]) -> dict[str, int]:
        paired = [row for row in rows if row["v1019"] is not None and row["v1020"]["review_mode"] == "FULL_TEXT"]
        return {
            "paired_text_sources": len(paired),
            "old_physical_lines": sum(row["v1019"]["extent"]["lines"] for row in paired),
            "new_physical_lines": sum(row["v1020"]["extent"]["lines"] for row in paired),
            "old_bytes": sum(row["v1019"]["size_bytes"] for row in paired),
            "new_bytes": sum(row["v1020"]["size_bytes"] for row in paired),
            "changed_old_lines": sum(row["text_delta"]["changed_old_lines"] for row in paired),
            "changed_new_lines": sum(row["text_delta"]["changed_new_lines"] for row in paired),
            "exact_opcode_segments": sum(row["text_delta"]["segment_count"] for row in paired),
        }
    root_rows = {
        row["normalized_identity"]["chapter"]: row
        for row in delta_rows
        if row["normalized_identity"]["section_or_artifact"] in {
            "graphite_ica_ch1_v1.0.20.tex", "graphite_ica_ch2_v1.0.20.tex"
        }
    }
    include_summary: dict[str, Any] = {}
    for chapter, expected_count in (("CH1", 24), ("CH2", 15)):
        root_row = root_rows.get(chapter)
        if root_row is None or root_row["latex_delta"] is None:
            raise BuildError(f"ROOT_INCLUDE_ROW:{chapter}")
        include_delta = root_row["latex_delta"]["include_topology"]
        if (
            len(include_delta["before"]) != expected_count
            or len(include_delta["after"]) != expected_count
            or include_delta["before"] != include_delta["after"]
        ):
            raise BuildError(f"ROOT_INCLUDE_TOPOLOGY:{chapter}")
        include_summary[chapter] = {
            "edge_count": expected_count, "ordered_targets": include_delta["after"],
            "ordered_targets_sha256": sha256(canonical_json_bytes(include_delta["after"])),
            "added": [], "removed": [], "moved": [],
        }
    ground_not_found = [
        {"ground_id": "P061-STEP48-GNF-001", "object": "P1 structural snapshot", "status": "GROUND_NOT_FOUND", "target_phase": 61},
        {"ground_id": "P061-STEP48-GNF-002", "object": "snapshot-generation command, cwd, runtime and tool environment", "status": "GROUND_NOT_FOUND", "target_phase": 67},
        {"ground_id": "P061-STEP48-GNF-003", "object": "evidence distinguishing P6 snapshot regeneration from copying P5 bytes", "status": "GROUND_NOT_FOUND", "target_phase": 61},
        {"ground_id": "P061-STEP48-GNF-004", "object": "source blob provenance embedded inside each historical snapshot", "status": "GROUND_NOT_FOUND", "target_phase": 61},
        {"ground_id": "P061-STEP48-GNF-005", "object": "standalone appendix include edge from adopted Ch1 or Ch2 roots", "status": "GROUND_NOT_FOUND", "target_phase": 62},
    ]
    unverified_queue = [
        {"queue_id": "P061-STEP48-UNV-001", "object": "fresh v1.0.20 G1/G2/G3/n(T) test execution", "status": "UNVERIFIED", "target_phase": 67},
        {"queue_id": "P061-STEP48-UNV-002", "object": "runtime equivalence beyond identical production-module AST", "status": "UNVERIFIED", "target_phase": 67},
        {"queue_id": "P061-STEP48-UNV-003", "object": "primary DOI and bibliography claim support", "status": "UNVERIFIED", "target_phase": 71},
        {"queue_id": "P061-STEP48-UNV-004", "object": "equation, derivation and material-law scientific validity", "status": "UNVERIFIED", "target_phase": 71},
        {"queue_id": "P061-STEP48-UNV-005", "object": "generated PDF numerical and scientific correctness", "status": "UNVERIFIED", "target_phase": 67},
        {"queue_id": "P061-STEP48-UNV-006", "object": "process rationale for twelve v1.0.19-only package paths", "status": "UNVERIFIED", "target_phase": 67},
        {"queue_id": "P061-STEP48-UNV-007", "object": "snapshot tool collision and truncated-hash risk in historical generation", "status": "UNVERIFIED", "target_phase": 67},
        {"queue_id": "P061-STEP48-UNV-008", "object": "standalone appendix adoption authority despite final structural enumeration", "status": "UNVERIFIED", "target_phase": 62},
    ]
    pdf_rows = [row for row in delta_rows if row["v1020"]["review_mode"] == "FULL_PDF"]
    image_rows = [row for row in delta_rows if row["v1020"]["review_mode"] == "FULL_IMAGE"]
    paired_pdf_rows = [row for row in pdf_rows if row["v1019"] is not None]
    added_pdf_rows = [row for row in pdf_rows if row["comparison_class"] == "ADDED"]

    lineage = {
        "schema_version": "1.0",
        "artifact_kind": "PHASE_061_V1020_LINEAGE_DIFF_MATRIX",
        "generated_date": GENERATED_DATE, "phase": 61, "step": 48,
        "status": "COMPLETE", "gate": "PASS_P061_STEP48_LINEAGE_DIFF",
        "authority_boundary": common_boundary,
        "pairing_policy": {
            "primary": "FULL_VERSION_RELATIVE_PATH",
            "semantic_renames": SEMANTIC_RENAME_PAIRS,
            "basename_only_pairing_allowed": False,
            "one_v1019_source_reused": False,
            "v1020_occurrence_exactly_once": True,
            "deleted_counterparts_separate_from_v1020_denominator": True,
        },
        "counts": {
            "v1020_occurrences": 232, "v1020_unique_blobs": 231,
            "v1019_occurrences": 66, "paired_occurrences": 54,
            "deleted_counterparts": 12, "delta_rows": len(delta_rows),
            "comparison_classes": class_counts,
            "paired_text_hunks": paired_text_hunks,
            "changed_old_lines": changed_old_lines, "changed_new_lines": changed_new_lines,
            "python_test_pairs": len(python_pairs), "snapshot_occurrences_linked": 10,
        },
        "release_delta_summary": {
            "v1020_final_release_surface_occurrences": sum(
                source["derived_authority_group"] == "FINAL_RELEASE_SURFACE" for source in sources
            ),
            "v1020_final_release_surface_all_paired": all(
                next(row for row in delta_rows if row["v1020_source_id"] == source["source_id"])["v1019"] is not None
                for source in sources if source["derived_authority_group"] == "FINAL_RELEASE_SURFACE"
            ),
            "provisional_ch1_ch2_claim_independently_verified": provisional_verified,
            "baseline_to_final_snapshot_delta": baseline_final,
            "generated_pdf_page_pairs": [
                {
                    "v1020_source_id": row["v1020_source_id"],
                    "old_path": row["v1019"]["path"], "new_path": row["v1020"]["path"],
                    **row["pdf_delta"],
                }
                for row in delta_rows if row["pdf_delta"] is not None
            ],
            "authority_ceiling": "RELEASE_LINEAGE_AND_STRUCTURE_ONLY",
            "final_release_surface_comparison_classes": comparison_distribution(final_surface_rows),
            "adopted_release_source_count": len(adopted_rows),
            "adopted_release_source_roles": {
                role: sum(row["v1020"]["role"] == role for row in adopted_rows)
                for role in sorted({row["v1020"]["role"] for row in adopted_rows})
            },
            "adopted_release_source_extensions": {
                extension: sum(
                    next(source for source in sources if source["source_id"] == row["v1020_source_id"])["extension"] == extension
                    for row in adopted_rows
                )
                for extension in sorted({
                    next(source for source in sources if source["source_id"] == row["v1020_source_id"])["extension"]
                    for row in adopted_rows
                })
            },
            "adopted_release_comparison_classes": comparison_distribution(adopted_rows),
            "adopted_release_text_extents": text_extent_summary(adopted_rows),
            "ordered_include_topology": include_summary,
            "pdf_lineage": {
                "paired_files": len(paired_pdf_rows),
                "paired_pages_before": sum(row["v1019"]["extent"]["pages"] for row in paired_pdf_rows),
                "paired_pages_after": sum(row["v1020"]["extent"]["pages"] for row in paired_pdf_rows),
                "added_files": len(added_pdf_rows),
                "added_pages": sum(row["v1020"]["extent"]["pages"] for row in added_pdf_rows),
                "v1020_total_files": len(pdf_rows),
                "v1020_total_pages": sum(row["v1020"]["extent"]["pages"] for row in pdf_rows),
                "scientific_correctness_inferred": False,
            },
            "image_lineage": {
                "unchanged_paired_occurrences": sum(row["comparison_class"] == "UNCHANGED" for row in image_rows),
                "added_occurrences": sum(row["comparison_class"] == "ADDED" for row in image_rows),
                "v1020_total_occurrences": len(image_rows),
                "old_only_image_counterparts": sum(row["review_mode"] == "FULL_IMAGE" for row in deleted),
                "experimental_authority_inferred": False,
            },
        },
        "python_test_source_comparisons": python_pairs,
        "delta_rows": delta_rows,
        "deleted_counterparts": deleted,
        "ground_not_found": ground_not_found,
        "unverified_queue": unverified_queue,
        "snapshot_genealogy_link": {
            "artifact_kind": "PHASE_061_V1020_SNAPSHOT_GENEALOGY",
            "generation_contract_id": generation_contract_id,
            "occurrences": 10, "edges": 9,
        },
        "required_negative_controls": list(NEGATIVE_CONTROL_IDS),
    }

    snapshot_genealogy = {
        "schema_version": "1.0",
        "artifact_kind": "PHASE_061_V1020_SNAPSHOT_GENEALOGY",
        "generated_date": GENERATED_DATE, "phase": 61, "step": 48,
        "status": "COMPLETE", "gate": "PASS_P061_STEP48_LINEAGE_DIFF",
        "authority_boundary": common_boundary,
        "counts": {
            "snapshot_occurrences": len(occurrence_rows), "unique_snapshot_blobs": len({row["blob_sha1"] for row in occurrence_rows}),
            "stage_edges": len(edges), "duplicate_occurrence_groups": 1,
            "prefinal_occurrences": 8, "final_appendix_root_occurrences": 1,
            "p5_p6_changed_tex_paths": len(changed_tex),
        },
        "snapshot_order": list(SNAPSHOT_ORDER),
        "snapshot_occurrences": occurrence_rows,
        "stage_edges": edges,
        "duplicate_occurrence_groups": [{
            "duplicate_id": "P061-SNAPSHOT-DUP-001", "aliases": ["p5", "p6"],
            "paths": [p5["path"], p6["path"]], "blob_sha1": p5["blob_sha1"],
            "sha256": p5["sha256"], "occurrences_distinct": True,
            "blob_identical": True, "captured_document_projection_identical": projections["p5"] == projections["p6"],
            "actual_source_tree_identical": False, "changed_tex_paths": changed_tex,
            "all_changed_paths": changed_paths,
            "p5_commit": p5_commit, "p6_commit": p6_commit,
            "p6_parent": p6_parent, "direct_parent": p6_parent == p5_commit,
            "independently_reconstructed_from_git": True,
            "step47_boundary_exactly_corroborates": True,
            "authority_ceiling": "CAPTURED_STRUCTURE_ONLY",
        }],
        "appendix_root_genealogy": {
            "prefinal_aliases": ["p0", "p2", "p3", "p4", "p5", "p6", "p7", "p7b"],
            "prefinal_root_occurrences": 0, "final_root_name": "appendix_phase_separation.tex",
            "final_root_occurrences": sum(
                root == "appendix_phase_separation.tex" for root in projections["final"]["raw_roots"]
            ),
            "baseline_root_occurrences": 0,
            "adopted_release_edge_inferred_from_snapshot": False,
            "target_phase_for_adoption_authority": 62,
        },
        "baseline_to_final": baseline_final,
        "provisional_claim_independently_verified": provisional_verified,
        "lineage_matrix_link": {
            "artifact_kind": "PHASE_061_V1020_LINEAGE_DIFF_MATRIX",
            "generation_contract_id": generation_contract_id,
            "v1020_occurrences": 232, "paired_occurrences": 54,
        },
        "ground_not_found": [row for row in ground_not_found if "snapshot" in row["object"].lower() or "P6" in row["object"] or "appendix" in row["object"]],
        "unverified_queue": [row for row in unverified_queue if row["target_phase"] in {62, 67}],
        "required_negative_controls": list(NEGATIVE_CONTROL_IDS),
    }
    walk_finite(lineage)
    walk_finite(snapshot_genealogy)
    return lineage, snapshot_genealogy


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-output", type=Path, default=DEFAULT_LINEAGE)
    parser.add_argument("--snapshot-output", type=Path, default=DEFAULT_SNAPSHOT)
    args = parser.parse_args()
    try:
        lineage, snapshot = build()
        lineage_path = args.lineage_output if args.lineage_output.is_absolute() else REPO / args.lineage_output
        snapshot_path = args.snapshot_output if args.snapshot_output.is_absolute() else REPO / args.snapshot_output
        lineage_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        lineage_path.write_bytes(canonical_json_bytes(lineage))
        snapshot_path.write_bytes(canonical_json_bytes(snapshot))
        print(
            "PASS_P061_STEP48_BUILDER "
            f"delta_rows={len(lineage['delta_rows'])} paired={lineage['counts']['paired_occurrences']} "
            f"deleted={lineage['counts']['deleted_counterparts']} snapshots={snapshot['counts']['snapshot_occurrences']} "
            f"edges={snapshot['counts']['stage_edges']} production_imported=false"
        )
        return 0
    except (BuildError, DuplicateKeyError, NonFiniteNumberError, UnicodeError, json.JSONDecodeError, SyntaxError) as exc:
        print(f"FAIL STEP48_BUILDER_ERROR {type(exc).__name__}:{exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
