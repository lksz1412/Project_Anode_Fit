#!/usr/bin/env python3
"""Validate the Phase 060 Step 40 source-topology artifact.

The validator derives its expected inventory, hashes, text extents, root include
edges, and expansion order from frozen Git objects.  The artifact path can be
overridden for one-condition negative fixtures with ``--artifact``.  This file
does not build or repair the artifact it validates.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import posixpath
import re
import subprocess
import sys
from bisect import bisect_right
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import numpy as np
from PIL import Image
from pypdf import PdfReader


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


REPO = Path(__file__).resolve().parents[3]
DEFAULT_ARTIFACT = REPO / "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
READ_ATTESTATION_PATH = "Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json"
READ_ATTESTATION = REPO / READ_ATTESTATION_PATH

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROTECTED_REF = "origin/codex/lib-physics-endgame-v1025_2"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_REF = "origin/main"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

ARTIFACT_KIND = "P060_V1019_SOURCE_TOPOLOGY"
AUTHORITY_BOUNDARY = (
    "Step 40 source inventory and TeX read topology only; external scientific "
    "truth is not established"
)

SUPPLEMENTARY_PATHS = [
    "Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md",
    "Claude/results/process/V1019_ASSET_CHECKLIST.md",
    "Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md",
    "Claude/results/process/V1019_CH2_FABLE_BRIEF.md",
    "Claude/results/process/V1019_CH2_UNION_DEFECTS.md",
    "Claude/results/process/V1019_CODE_FABLE_BRIEF.md",
    "Claude/results/process/V1019_CONTINUITY_JUDGMENT.md",
    "Claude/results/process/V1019_EXECUTION_LEDGER.md",
    "Claude/results/process/V1019_FABLE_BRIEF.md",
    "Claude/results/process/V1019_FINAL_REVIEW_UNION.md",
    "Claude/results/process/V1019_UNION_DEFECTS.md",
]

WITNESS_PATHS = [
    "Claude/docs/v1.0.20/figs/graph_suite_v1019.png",
    "Claude/docs/v1.0.20/results/snapshot_v1019_baseline.json",
]

ROOT_GROUPS = [
    ("CH1", "Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.tex"),
    ("CH2", "Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex"),
    ("STANDALONE", "Claude/docs/v1.0.19/appendix_phase_separation.tex"),
]

PREDECESSOR_ROOTS = [
    (
        "CH1",
        "Claude/docs/v1.0.18.2/graphite_ica_ch1_v1.0.18.2.tex",
        "Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.tex",
    ),
    (
        "CH2",
        "Claude/docs/v1.0.18.2/graphite_ica_ch2_v1.0.18.2.tex",
        "Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex",
    ),
    (
        "STANDALONE",
        "Claude/docs/v1.0.18.2/appendix_phase_separation.tex",
        "Claude/docs/v1.0.19/appendix_phase_separation.tex",
    ),
]

PREDECESSOR_EVIDENCE_PATH = (
    "Codex/results/PHASE_059_THEORY_SOURCE_STRUCTURE_INDEX.md"
)

LEXICAL_AUTHORITY = "LEXICAL_SOURCE_ANCHOR_ONLY_NOT_SCIENTIFIC_TRUTH"
CANDIDATE_CUE_AUTHORITY = (
    "CANDIDATE_CUE_ONLY_REQUIRES_LATER_ADJUDICATION_NOT_SCIENTIFIC_TRUTH"
)

TOP_LEVEL_KEYS = {
    "schema_version",
    "generated_date",
    "phase",
    "step",
    "artifact_kind",
    "baseline_commit",
    "authority_boundary",
    "counts",
    "sources",
    "read_attestation",
    "include_topology",
    "content_index",
    "predecessor_comparison",
    "diagnostics",
    "protection",
}

READ_ATTESTATION_SUMMARY_KEYS = {
    "path",
    "sha256",
    "source_records",
    "reader_tasks",
    "authority_boundary",
}

READ_ATTESTATION_SOURCE_KEYS = {
    "path",
    "git_blob_sha1",
    "physical_lines",
    "actual_coverage",
    "coverage_status",
    "reader_task",
}

SOURCE_KEYS = {
    "path",
    "owner",
    "version",
    "occurrence_kind",
    "git_mode",
    "git_blob_sha1",
    "sha256",
    "size_bytes",
    "role",
    "authority_class",
    "review_mode",
    "expected_extent",
    "text_metrics",
    "tex_group",
    "actual_coverage",
    "coverage_status",
    "evidence",
    "authority_boundary",
}

ROOT_RECORD_KEYS = {
    "document_group",
    "root_path",
    "git_blob_sha1",
    "sha256",
    "physical_lines",
    "include_edge_count",
}

EDGE_KEYS = {
    "edge_id",
    "document_group",
    "parent_path",
    "parent_line",
    "command",
    "raw_target",
    "resolved_path",
    "child_git_blob_sha1",
    "expansion_ordinal",
    "resolution_status",
}

EXPANSION_KEYS = {
    "global_ordinal",
    "document_group",
    "group_ordinal",
    "expansion_kind",
    "path",
    "git_blob_sha1",
    "include_edge_id",
}

CONTENT_INDEX_KEYS = {
    "lexical_rules_version",
    "authority_boundary",
    "kind_counts",
    "document_statistics",
    "records",
}

DOCUMENT_STATISTIC_KEYS = {
    "document_group",
    "citation_command_occurrences",
    "citation_key_occurrences",
    "unique_citation_keys",
    "bibliography_key_occurrences",
    "unique_bibliography_keys",
    "label_occurrences",
    "unique_label_keys",
    "reference_key_occurrences",
    "unique_reference_keys",
    "external_document_occurrences",
    "external_link_occurrences",
}

CONTENT_RECORD_KEYS = {
    "anchor_id",
    "path",
    "line_start",
    "line_end",
    "kind",
    "token",
    "key",
    "text_sha256",
    "authority",
}

PREDECESSOR_COMPARISON_KEYS = {
    "predecessor_version",
    "evidence_record",
    "root_comparisons",
    "authority_boundary",
}

PREDECESSOR_EVIDENCE_KEYS = {
    "path",
    "git_blob_sha1",
    "sha256",
    "physical_lines",
    "relevant_line_ranges",
    "gate",
    "authority_boundary",
}

PREDECESSOR_ROOT_COMPARISON_KEYS = {
    "document_group",
    "predecessor_path",
    "predecessor_git_blob_sha1",
    "predecessor_sha256",
    "predecessor_physical_lines",
    "predecessor_include_edge_count",
    "current_path",
    "current_git_blob_sha1",
    "current_sha256",
    "current_physical_lines",
    "current_include_edge_count",
    "topology_relation",
    "copied_content_status",
    "comparison_status",
}

DIAGNOSTIC_KEYS = {
    "missing_source_paths",
    "unexpected_source_paths",
    "duplicate_source_paths",
    "duplicate_primary_blob_sha1",
    "blob_sha1_mismatches",
    "sha256_mismatches",
    "size_mismatches",
    "extent_mismatches",
    "coverage_gaps",
    "coverage_overlaps",
    "coverage_out_of_bounds",
    "missing_include_edges",
    "unexpected_include_edges",
    "unresolved_include_edges",
    "duplicate_include_edges",
    "unreachable_tex_sources",
    "circular_include_dependencies",
    "external_reference_dependencies",
    "expansion_ordinal_errors",
    "content_index_mismatches",
    "duplicate_label_keys",
    "unresolved_citation_keys",
    "unresolved_reference_candidates",
    "forward_reference_keys",
    "predecessor_comparison_mismatches",
    "protected_drift",
    "main_drift",
    "claude_diff_paths",
}

PROTECTION_KEYS = {
    "protected_ref",
    "expected_protected_tip",
    "actual_protected_tip",
    "main_ref",
    "expected_main_tip",
    "actual_main_tip",
    "claude_diff_paths",
    "untracked_claude_paths",
    "active_branch",
    "upstream_ref",
    "origin_active_ref",
    "active_refs_equal",
    "allowed_step_paths",
    "unexpected_worktree_paths",
}

ALLOWED_STEP_PATHS = {
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_060_STEP_040_SOURCE_TOPOLOGY_RESULT.md",
    "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json",
    "Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json",
    "Codex/work/v1019_phase060/build_phase060_step40_source_topology.py",
    "Codex/work/v1019_phase060/validate_phase060_step40_source_topology.py",
}

INCLUDE_RE = re.compile(r"\\(input|include)\s*\{([^}]+)\}")
DISPLAY_ENV_RE = re.compile(
    r"\\(begin|end)\{(equation\*?|align\*?|gather\*?|multline\*?|"
    r"flalign\*?|eqnarray\*?)\}"
)
DISPLAY_BRACKET_RE = re.compile(r"(?<!\\)\\\[|(?<!\\)\\\]")
LABEL_RE = re.compile(r"\\label\s*\{([^}]+)\}")
CITE_RE = re.compile(r"\\(cite[a-zA-Z*]*)\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}")
REF_RE = re.compile(r"\\(eqref|ref|autoref|pageref)\s*\{([^}]+)\}")
EXTERNAL_DOCUMENT_RE = re.compile(
    r"\\externaldocument\s*(?:\[[^\]]*\]\s*)?\{([^}]+)\}"
)
EXTERNAL_LINK_RE = re.compile(r"\\(href|url)\s*\{([^}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem\s*(?:\[[^\]]*\]\s*)?\{([^}]+)\}")

CUE_PATTERNS = {
    "DEFINITION_CANDIDATE": re.compile(
        r"(?i)(\bdefine(?:d|s)?\b|\bdefinition\b|\bdenote(?:d|s)?\b|"
        r"\blet\b|정의|정한다|뜻한다|라\s*하|로\s*둔다)"
    ),
    "ASSUMPTION_CANDIDATE": re.compile(
        r"(?i)(\bassum(?:e|ed|es|ing|ption|ptions)\b|\bsuppose(?:d|s)?\b|"
        r"가정|전제)"
    ),
    "SIGN_UNIT_DECLARATION_CANDIDATE": re.compile(
        r"(?i)(\bsign(?:ed)?\b|\bpositive\b|\bnegative\b|\bunits?\b|"
        r"\bdimension(?:al|less)?\b|부호|양의|음의|단위|차원)"
    ),
    "CODE_MENTION_CANDIDATE": re.compile(
        r"(?i)(\bcode\b|\bimplementation\b|\bpython\b|\bfunction\b|"
        r"\bclass\b|\bAPI\b|\broutine\b|\bmodule\b|코드|구현|함수|클래스)"
    ),
    "FORWARD_REFERENCE_CANDIDATE": re.compile(
        r"(?i)(\bbelow\b|\blater\b|\bnext\s+section\b|\bfollowing\b|"
        r"후술|뒤에서|다음\s*절|향후|앞으로|후속)"
    ),
}


class DuplicateKeyError(ValueError):
    """Raised when strict JSON parsing finds a repeated object key."""


class InvalidJsonConstantError(ValueError):
    """Raised for non-standard JSON constants such as NaN or Infinity."""


class GroundTruthError(RuntimeError):
    """Raised when the frozen control inputs do not match their contract."""


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_json_bytes(data: bytes, label: str) -> Any:
    def reject_constant(value: str) -> None:
        raise InvalidJsonConstantError(value)

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GroundTruthError(f"JSON control is not UTF-8: {label}") from exc
    return json.loads(
        text, object_pairs_hook=strict_pairs, parse_constant=reject_constant
    )


def strict_json(path: Path) -> Any:
    return strict_json_bytes(path.read_bytes(), str(path))


def run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise GroundTruthError(
            f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def git_blob_at(treeish: str, path: str) -> tuple[str, str, bytes]:
    row = run_git("ls-tree", treeish, "--", path)
    if not row:
        raise GroundTruthError(f"missing baseline path: {path}")
    try:
        metadata, tree_path = row.split("\t", 1)
        mode, object_type, blob_sha1 = metadata.split()
    except ValueError as exc:
        raise GroundTruthError(f"malformed ls-tree row for {path}: {row!r}") from exc
    if tree_path != path or object_type != "blob":
        raise GroundTruthError(
            f"unexpected ls-tree identity for {path}: type={object_type}, path={tree_path}"
        )
    proc = subprocess.run(
        ["git", "cat-file", "blob", blob_sha1],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise GroundTruthError(
            f"git cat-file blob {blob_sha1} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return mode, blob_sha1, proc.stdout


def git_blob(path: str) -> tuple[str, str, bytes]:
    return git_blob_at(BASELINE, path)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_metrics(data: bytes, path: str) -> dict[str, Any]:
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise GroundTruthError(f"baseline text is not UTF-8: {path}") from exc
    return {
        "encoding": "utf-8",
        "physical_lines": len(lines),
        "nonblank_lines": sum(bool(line.strip()) for line in lines),
    }


def derived_binary_extent(review_mode: str, data: bytes, path: str) -> Any:
    try:
        if review_mode == "FULL_PDF":
            reader = PdfReader(io.BytesIO(data))
            return {"pages": len(reader.pages), "encrypted": reader.is_encrypted}
        if review_mode == "FULL_IMAGE":
            with Image.open(io.BytesIO(data)) as image:
                image.load()
                return {
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode,
                    "format": image.format,
                    "frames": getattr(image, "n_frames", 1),
                }
        if review_mode == "BINARY_INTROSPECTION":
            arrays: list[dict[str, Any]] = []
            with np.load(io.BytesIO(data), allow_pickle=False) as archive:
                for key in archive.files:
                    array = archive[key]
                    finite = np.isfinite(array)
                    finite_values = array[finite]
                    arrays.append(
                        {
                            "key": key,
                            "dtype": str(array.dtype),
                            "shape": list(array.shape),
                            "size": int(array.size),
                            "finite_count": int(finite.sum()),
                            "finite_min": (
                                float(finite_values.min())
                                if finite_values.size
                                else None
                            ),
                            "finite_max": (
                                float(finite_values.max())
                                if finite_values.size
                                else None
                            ),
                        }
                    )
            arrays.sort(key=lambda item: item["key"])
            return {"arrays": arrays}
    except Exception as exc:
        raise GroundTruthError(
            f"cannot introspect frozen {review_mode} bytes for {path}: {exc}"
        ) from exc
    return None


def tex_group(path: str) -> str:
    if "/_sections/ch1_" in path:
        return "CH1_SECTION"
    if "/_sections/ch2_" in path:
        return "CH2_SECTION"
    if path in {root_path for _, root_path in ROOT_GROUPS}:
        return "ROOT_TEX"
    return "NOT_TEX"


def authority_class(path: str, role: str) -> str:
    if not path.endswith(".tex"):
        return f"NON_TEX_{role.upper()}"
    name = PurePosixPath(path).name
    if path.endswith("appendix_phase_separation.tex"):
        return "STANDALONE_PHASE_SEPARATION"
    if name.endswith("_bib.tex"):
        return "BIBLIOGRAPHY"
    if name == "ch1_appA_signcheck.tex":
        return "SIGN_CHECK_APPENDIX"
    if name.endswith("_appB_codemap.tex"):
        return "CODE_MAP_APPENDIX"
    if name == "ch2_appA_traps.tex":
        return "SCIENTIFIC_TRAPS_APPENDIX"
    if name.endswith("_preamble.tex"):
        return "DOCUMENT_PREAMBLE"
    if path in {root_path for _, root_path in ROOT_GROUPS}:
        return "DOCUMENT_ROOT"
    return "SCIENTIFIC_BODY"


def document_group_for_path(path: str) -> str:
    if "/_sections/ch1_" in path or path.endswith(
        "graphite_ica_ch1_v1.0.19.tex"
    ):
        return "CH1"
    if "/_sections/ch2_" in path or path.endswith(
        "graphite_ica_ch2_v1.0.19.tex"
    ):
        return "CH2"
    if path.endswith("appendix_phase_separation.tex"):
        return "STANDALONE"
    raise GroundTruthError(f"TeX source is outside the three frozen document groups: {path}")


def expected_source_record(
    *,
    path: str,
    owner: str,
    version: str,
    occurrence_kind: str,
    role: str,
    review_mode: str,
    expected_extent: Any,
    expected_git_mode: str | None = None,
    expected_blob_sha1: str | None = None,
    expected_size_bytes: int | None = None,
) -> dict[str, Any]:
    git_mode, blob_sha1, data = git_blob(path)
    if expected_git_mode is not None and git_mode != expected_git_mode:
        raise GroundTruthError(
            f"manifest git mode mismatch for {path}: {expected_git_mode} != {git_mode}"
        )
    if expected_blob_sha1 is not None and blob_sha1 != expected_blob_sha1:
        raise GroundTruthError(
            f"manifest blob mismatch for {path}: {expected_blob_sha1} != {blob_sha1}"
        )
    if expected_size_bytes is not None and len(data) != expected_size_bytes:
        raise GroundTruthError(
            f"manifest size mismatch for {path}: {expected_size_bytes} != {len(data)}"
        )
    metrics = text_metrics(data, path) if review_mode == "FULL_TEXT" else None
    if metrics is not None and expected_extent.get("lines") != metrics["physical_lines"]:
        raise GroundTruthError(
            f"manifest line mismatch for {path}: "
            f"{expected_extent.get('lines')} != {metrics['physical_lines']}"
        )
    if review_mode in {"FULL_PDF", "FULL_IMAGE", "BINARY_INTROSPECTION"}:
        actual_extent = derived_binary_extent(review_mode, data, path)
        if not same_json_value(actual_extent, expected_extent):
            raise GroundTruthError(
                f"manifest binary extent mismatch for {path}: expected "
                f"{canonical_json(expected_extent)}, actual "
                f"{canonical_json(actual_extent)}"
            )
    return {
        "path": path,
        "owner": owner,
        "version": version,
        "occurrence_kind": occurrence_kind,
        "git_mode": git_mode,
        "git_blob_sha1": blob_sha1,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
        "role": role,
        "authority_class": authority_class(path, role),
        "review_mode": review_mode,
        "expected_extent": expected_extent,
        "text_metrics": metrics,
        "tex_group": tex_group(path),
    }


def load_expected_sources() -> list[dict[str, Any]]:
    _, _, manifest_data = git_blob_at(EXPECTED_PROTECTED, MANIFEST_PATH)
    manifest = strict_json_bytes(
        manifest_data, f"{EXPECTED_PROTECTED}:{MANIFEST_PATH}"
    )
    if not isinstance(manifest, dict):
        raise GroundTruthError("manifest root is not an object")
    if manifest.get("baseline_commit") != BASELINE:
        raise GroundTruthError(
            f"manifest baseline mismatch: {manifest.get('baseline_commit')} != {BASELINE}"
        )
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise GroundTruthError("manifest entries is not an array")

    release = [entry for entry in entries if entry.get("version") == "v1.0.19"]
    if len(release) != 66:
        raise GroundTruthError(f"release entry count mismatch: {len(release)} != 66")
    release_paths = [entry.get("path") for entry in release]
    if any(not isinstance(path, str) for path in release_paths):
        raise GroundTruthError("release entry has a non-string path")
    if len(set(release_paths)) != 66:
        raise GroundTruthError("release manifest contains duplicate paths")

    witness_entries = {
        entry.get("path"): entry for entry in entries if entry.get("path") in WITNESS_PATHS
    }
    if set(witness_entries) != set(WITNESS_PATHS):
        raise GroundTruthError("manifest does not contain the exact two witness paths")

    expected: list[dict[str, Any]] = []
    for entry in release:
        required = {
            "path",
            "version",
            "git_mode",
            "blob_sha",
            "size_bytes",
            "role",
            "review_mode",
            "extent",
        }
        if not required.issubset(entry):
            raise GroundTruthError(
                f"release manifest entry lacks keys {sorted(required - set(entry))}: "
                f"{entry.get('path')}"
            )
        expected.append(
            expected_source_record(
                path=entry["path"],
                owner="P060_PRIMARY_RELEASE",
                version=entry["version"],
                occurrence_kind="PRIMARY_RELEASE",
                role=entry["role"],
                review_mode=entry["review_mode"],
                expected_extent=entry["extent"],
                expected_git_mode=entry["git_mode"],
                expected_blob_sha1=entry["blob_sha"],
                expected_size_bytes=entry["size_bytes"],
            )
        )

    for path in SUPPLEMENTARY_PATHS:
        git_mode, _, data = git_blob(path)
        metrics = text_metrics(data, path)
        expected.append(
            expected_source_record(
                path=path,
                owner="P060_PRIMARY_PROCESS",
                version="v1.0.19",
                occurrence_kind="PRIMARY_PROCESS",
                role="process_evidence",
                review_mode="FULL_TEXT",
                expected_extent={
                    "encoding_check": "utf-8",
                    "lines": metrics["physical_lines"],
                },
                expected_git_mode=git_mode,
                expected_size_bytes=len(data),
            )
        )

    for path in WITNESS_PATHS:
        entry = witness_entries[path]
        expected.append(
            expected_source_record(
                path=path,
                owner="P060_CROSS_VERSION_WITNESS",
                version=entry["version"],
                occurrence_kind="CROSS_VERSION_WITNESS",
                role=entry["role"],
                review_mode=entry["review_mode"],
                expected_extent=entry["extent"],
                expected_git_mode=entry["git_mode"],
                expected_blob_sha1=entry["blob_sha"],
                expected_size_bytes=entry["size_bytes"],
            )
        )

    expected.sort(key=lambda item: item["path"])
    if len(expected) != 79 or len({item["path"] for item in expected}) != 79:
        raise GroundTruthError("expected inspection inventory is not 79 unique path occurrences")
    return expected


def load_read_attestation(
    expected_sources: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    attestation_bytes = READ_ATTESTATION.read_bytes()
    attestation = strict_json_bytes(attestation_bytes, READ_ATTESTATION_PATH)
    required_root_keys = {
        "schema_version",
        "generated_date",
        "phase",
        "step",
        "artifact_kind",
        "baseline_commit",
        "authority_boundary",
        "review_runs",
        "sources",
        "controller_reconciliation",
    }
    if not isinstance(attestation, dict) or set(attestation) != required_root_keys:
        raise GroundTruthError("read attestation root schema mismatch")
    scalar_expectations = {
        "schema_version": 1,
        "generated_date": "2026-08-26",
        "phase": 60,
        "step": 40,
        "artifact_kind": "P060_V1019_TEX_READ_ATTESTATION",
        "baseline_commit": BASELINE,
        "authority_boundary": (
            "Human-agent full-read provenance for frozen TeX source only; not "
            "scientific truth, build success, implementation conformance or external validity"
        ),
    }
    for key, value in scalar_expectations.items():
        if not same_json_value(attestation.get(key), value):
            raise GroundTruthError(f"read attestation scalar mismatch: {key}")
    review_runs = attestation.get("review_runs")
    if not isinstance(review_runs, list) or len(review_runs) != 2:
        raise GroundTruthError("read attestation must preserve the two actual review runs")
    run_by_reader = {
        run.get("reader_task"): run for run in review_runs if isinstance(run, dict)
    }
    expected_readers = {
        "/root/step396_implementer": (["CH1"], "25 files / 3711 physical lines"),
        "/root/step396_spec_review": (
            ["CH2", "STANDALONE"],
            "17 files / 1925 physical lines",
        ),
    }
    if set(run_by_reader) != set(expected_readers):
        raise GroundTruthError("read attestation reviewer identities mismatch")
    for reader, (groups, coverage_prefix) in expected_readers.items():
        run = run_by_reader[reader]
        if run.get("status") != "READ_FULL" or run.get("document_groups") != groups:
            raise GroundTruthError(f"read attestation run mismatch: {reader}")
        if not str(run.get("actual_coverage", "")).startswith(coverage_prefix):
            raise GroundTruthError(f"read attestation run coverage mismatch: {reader}")

    source_records = attestation.get("sources")
    if not isinstance(source_records, list) or len(source_records) != 42:
        raise GroundTruthError("read attestation source count is not 42")
    by_path: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(source_records):
        if not isinstance(record, dict) or set(record) != READ_ATTESTATION_SOURCE_KEYS:
            raise GroundTruthError(
                f"read attestation source schema mismatch at index {index}"
            )
        path = record.get("path")
        if not isinstance(path, str) or path in by_path:
            raise GroundTruthError(f"read attestation duplicate/invalid path: {path!r}")
        by_path[path] = record
    expected_tex = {
        source["path"]: source
        for source in expected_sources
        if source["owner"] == "P060_PRIMARY_RELEASE"
        and source["path"].endswith(".tex")
    }
    if set(by_path) != set(expected_tex):
        raise GroundTruthError("read attestation paths do not equal frozen 42-TeX set")
    for path, source in expected_tex.items():
        record = by_path[path]
        lines = source["text_metrics"]["physical_lines"]
        expected_reader = (
            "/root/step396_implementer"
            if document_group_for_path(path) == "CH1"
            else "/root/step396_spec_review"
        )
        expected_record = {
            "path": path,
            "git_blob_sha1": source["git_blob_sha1"],
            "physical_lines": lines,
            "actual_coverage": [{"start": 1, "end": lines}],
            "coverage_status": "READ_FULL",
            "reader_task": expected_reader,
        }
        if not same_json_value(record, expected_record):
            raise GroundTruthError(f"read attestation source mismatch: {path}")
    summary = {
        "path": READ_ATTESTATION_PATH,
        "sha256": sha256_bytes(attestation_bytes),
        "source_records": len(source_records),
        "reader_tasks": sorted(expected_readers),
        "authority_boundary": scalar_expectations["authority_boundary"],
    }
    return summary, by_path


def strip_tex_comment(line: str) -> str:
    for index, character in enumerate(line):
        if character != "%":
            continue
        preceding_backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            preceding_backslashes += 1
            cursor -= 1
        if preceding_backslashes % 2 == 0:
            return line[:index]
    return line


def resolve_tex_target(parent_path: str, raw_target: str) -> str:
    target = raw_target.strip()
    if not target or "\\" in target or PurePosixPath(target).is_absolute():
        raise GroundTruthError(
            f"invalid TeX include target in {parent_path}: {raw_target!r}"
        )
    if not PurePosixPath(target).suffix:
        target += ".tex"
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(parent_path), target))
    if resolved == ".." or resolved.startswith("../") or resolved.startswith("/"):
        raise GroundTruthError(
            f"TeX include escapes the repository in {parent_path}: {raw_target!r}"
        )
    return resolved


def build_expected_topology(
    sources: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    source_by_path = {item["path"]: item for item in sources}
    frozen_tex_paths = {
        item["path"]
        for item in sources
        if item["owner"] == "P060_PRIMARY_RELEASE"
        and item["path"].endswith(".tex")
    }
    root_records: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for document_group, root_path in ROOT_GROUPS:
        root = source_by_path.get(root_path)
        if root is None:
            raise GroundTruthError(f"missing root source record: {root_path}")
        _, _, data = git_blob(root_path)
        lines = data.decode("utf-8").splitlines()
        group_edges: list[dict[str, Any]] = []
        for parent_line, line in enumerate(lines, start=1):
            body = strip_tex_comment(line)
            for match in INCLUDE_RE.finditer(body):
                command, raw_target = match.groups()
                resolved_path = resolve_tex_target(root_path, raw_target)
                child = source_by_path.get(resolved_path)
                if resolved_path not in frozen_tex_paths or child is None:
                    raise GroundTruthError(
                        f"unresolved frozen TeX edge {root_path}:{parent_line} -> "
                        f"{resolved_path}"
                    )
                ordinal = len(group_edges) + 1
                group_edges.append(
                    {
                        "edge_id": f"P060-EDGE-{document_group}-{ordinal:03d}",
                        "document_group": document_group,
                        "parent_path": root_path,
                        "parent_line": parent_line,
                        "command": command,
                        "raw_target": raw_target,
                        "resolved_path": resolved_path,
                        "child_git_blob_sha1": child["git_blob_sha1"],
                        "expansion_ordinal": ordinal,
                        "resolution_status": "RESOLVED_FROZEN_SOURCE",
                    }
                )
        root_records.append(
            {
                "document_group": document_group,
                "root_path": root_path,
                "git_blob_sha1": root["git_blob_sha1"],
                "sha256": root["sha256"],
                "physical_lines": root["text_metrics"]["physical_lines"],
                "include_edge_count": len(group_edges),
            }
        )
        edges.extend(group_edges)

    if [record["include_edge_count"] for record in root_records] != [24, 15, 0]:
        raise GroundTruthError(
            "root include-edge counts differ from the frozen 24/15/0 contract"
        )
    if len(edges) != 39 or len({edge["resolved_path"] for edge in edges}) != 39:
        raise GroundTruthError("frozen include topology is not 39 unique section edges")

    edges_by_group: dict[str, list[dict[str, Any]]] = {
        group: [edge for edge in edges if edge["document_group"] == group]
        for group, _ in ROOT_GROUPS
    }
    expansion_sequence: list[dict[str, Any]] = []
    global_ordinal = 0
    for document_group, root_path in ROOT_GROUPS:
        global_ordinal += 1
        root = source_by_path[root_path]
        expansion_sequence.append(
            {
                "global_ordinal": global_ordinal,
                "document_group": document_group,
                "group_ordinal": 1,
                "expansion_kind": "ROOT",
                "path": root_path,
                "git_blob_sha1": root["git_blob_sha1"],
                "include_edge_id": None,
            }
        )
        for edge in edges_by_group[document_group]:
            global_ordinal += 1
            child = source_by_path[edge["resolved_path"]]
            expansion_sequence.append(
                {
                    "global_ordinal": global_ordinal,
                    "document_group": document_group,
                    "group_ordinal": edge["expansion_ordinal"] + 1,
                    "expansion_kind": "INCLUDED_SECTION",
                    "path": edge["resolved_path"],
                    "git_blob_sha1": child["git_blob_sha1"],
                    "include_edge_id": edge["edge_id"],
                }
            )
    if len(expansion_sequence) != 42:
        raise GroundTruthError("frozen TeX expansion sequence is not 42 records")
    return {
        "root_records": root_records,
        "edges": edges,
        "expansion_sequence": expansion_sequence,
    }


def anchor_text_sha256(lines: list[str], line_start: int, line_end: int) -> str:
    normalized = "\n".join(lines[line_start - 1 : line_end]).encode("utf-8")
    return sha256_bytes(normalized)


def build_expected_content_index(
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    citation_command_counts: Counter[str] = Counter()
    tex_sources = [
        item
        for item in sources
        if item["owner"] == "P060_PRIMARY_RELEASE"
        and item["path"].endswith(".tex")
    ]

    def add_record(
        *,
        path: str,
        lines: list[str],
        line_start: int,
        line_end: int,
        kind: str,
        token: str,
        key: str | None,
        authority: str,
    ) -> None:
        records.append(
            {
                "path": path,
                "line_start": line_start,
                "line_end": line_end,
                "kind": kind,
                "token": token,
                "key": key,
                "text_sha256": anchor_text_sha256(lines, line_start, line_end),
                "authority": authority,
            }
        )

    for source in sorted(tex_sources, key=lambda item: item["path"]):
        path = source["path"]
        _, _, data = git_blob(path)
        lines = data.decode("utf-8").splitlines()
        clean_lines = [strip_tex_comment(line) for line in lines]
        clean_text = "\n".join(clean_lines)
        document_group = document_group_for_path(path)
        citation_command_counts[document_group] += sum(
            1 for _ in CITE_RE.finditer(clean_text)
        )
        line_starts = [0]
        line_starts.extend(
            index + 1 for index, character in enumerate(clean_text) if character == "\n"
        )

        def match_line_span(match: re.Match[str]) -> tuple[int, int]:
            line_start = bisect_right(line_starts, match.start())
            line_end = bisect_right(line_starts, max(match.start(), match.end() - 1))
            return line_start, line_end

        environment_stack: list[tuple[str, int]] = []
        bracket_stack: list[int] = []
        for line_number, body in enumerate(clean_lines, start=1):
            for match in DISPLAY_ENV_RE.finditer(body):
                action, environment = match.groups()
                if action == "begin":
                    environment_stack.append((environment, line_number))
                    continue
                matching_index = next(
                    (
                        index
                        for index in range(len(environment_stack) - 1, -1, -1)
                        if environment_stack[index][0] == environment
                    ),
                    None,
                )
                if matching_index is None:
                    raise GroundTruthError(
                        f"unmatched display environment end in {path}:{line_number}: "
                        f"{environment}"
                    )
                _, line_start = environment_stack.pop(matching_index)
                add_record(
                    path=path,
                    lines=lines,
                    line_start=line_start,
                    line_end=line_number,
                    kind="DISPLAYED_EQUATION",
                    token=f"environment:{environment}",
                    key=environment,
                    authority=LEXICAL_AUTHORITY,
                )
            for match in DISPLAY_BRACKET_RE.finditer(body):
                token = match.group(0)
                if token == "\\[":
                    bracket_stack.append(line_number)
                elif not bracket_stack:
                    raise GroundTruthError(
                        f"unmatched display bracket end in {path}:{line_number}"
                    )
                else:
                    line_start = bracket_stack.pop()
                    add_record(
                        path=path,
                        lines=lines,
                        line_start=line_start,
                        line_end=line_number,
                        kind="DISPLAYED_EQUATION",
                        token="bracket-display",
                        key=None,
                        authority=LEXICAL_AUTHORITY,
                    )

            for kind, pattern in CUE_PATTERNS.items():
                matches = [match.group(0) for match in pattern.finditer(body)]
                if not matches:
                    continue
                cue_token = "|".join(
                    sorted(dict.fromkeys(matches), key=lambda item: item.casefold())
                )
                add_record(
                    path=path,
                    lines=lines,
                    line_start=line_number,
                    line_end=line_number,
                    kind=kind,
                    token=cue_token,
                    key=None,
                    authority=CANDIDATE_CUE_AUTHORITY,
                )
        if environment_stack:
            raise GroundTruthError(
                f"unclosed display environments in {path}: {environment_stack}"
            )
        if bracket_stack:
            raise GroundTruthError(
                f"unclosed display brackets in {path}: {bracket_stack}"
            )

        for match in LABEL_RE.finditer(clean_text):
            line_start, line_end = match_line_span(match)
            add_record(
                path=path,
                lines=lines,
                line_start=line_start,
                line_end=line_end,
                kind="LABEL_KEY",
                token="label",
                key=match.group(1).strip(),
                authority=LEXICAL_AUTHORITY,
            )
        for match in CITE_RE.finditer(clean_text):
            line_start, line_end = match_line_span(match)
            command, raw_keys = match.groups()
            for key in (item.strip() for item in raw_keys.split(",")):
                if key:
                    add_record(
                        path=path,
                        lines=lines,
                        line_start=line_start,
                        line_end=line_end,
                        kind="CITATION_KEY",
                        token=command,
                        key=key,
                        authority=LEXICAL_AUTHORITY,
                    )
        for match in BIBITEM_RE.finditer(clean_text):
            line_start, line_end = match_line_span(match)
            add_record(
                path=path,
                lines=lines,
                line_start=line_start,
                line_end=line_end,
                kind="BIBLIOGRAPHY_KEY",
                token="bibitem",
                key=match.group(1).strip(),
                authority=LEXICAL_AUTHORITY,
            )
        for match in REF_RE.finditer(clean_text):
            line_start, line_end = match_line_span(match)
            command, key = match.groups()
            add_record(
                path=path,
                lines=lines,
                line_start=line_start,
                line_end=line_end,
                kind="REFERENCE_KEY",
                token=command,
                key=key.strip(),
                authority=LEXICAL_AUTHORITY,
            )
        for match in EXTERNAL_DOCUMENT_RE.finditer(clean_text):
            line_start, line_end = match_line_span(match)
            add_record(
                path=path,
                lines=lines,
                line_start=line_start,
                line_end=line_end,
                kind="EXTERNAL_DOCUMENT",
                token="externaldocument",
                key=match.group(1).strip(),
                authority=LEXICAL_AUTHORITY,
            )
        for match in EXTERNAL_LINK_RE.finditer(clean_text):
            line_start, line_end = match_line_span(match)
            command, target = match.groups()
            add_record(
                path=path,
                lines=lines,
                line_start=line_start,
                line_end=line_end,
                kind="EXTERNAL_LINK",
                token=command,
                key=target.strip(),
                authority=LEXICAL_AUTHORITY,
            )

    records.sort(
        key=lambda item: (
            item["path"],
            item["line_start"],
            item["line_end"],
            item["kind"],
            item["token"],
            "" if item["key"] is None else item["key"],
        )
    )
    for index, record in enumerate(records, start=1):
        record["anchor_id"] = f"P060-LEX-{index:06d}"
    ordered_records = [
        {
            "anchor_id": record["anchor_id"],
            "path": record["path"],
            "line_start": record["line_start"],
            "line_end": record["line_end"],
            "kind": record["kind"],
            "token": record["token"],
            "key": record["key"],
            "text_sha256": record["text_sha256"],
            "authority": record["authority"],
        }
        for record in records
    ]
    kind_counts = dict(sorted(Counter(record["kind"] for record in records).items()))
    document_statistics: list[dict[str, Any]] = []
    for document_group in ("CH1", "CH2", "STANDALONE"):
        group_records = [
            record
            for record in records
            if document_group_for_path(record["path"]) == document_group
        ]
        citations = [
            record["key"]
            for record in group_records
            if record["kind"] == "CITATION_KEY"
        ]
        bibliography = [
            record["key"]
            for record in group_records
            if record["kind"] == "BIBLIOGRAPHY_KEY"
        ]
        labels = [
            record["key"]
            for record in group_records
            if record["kind"] == "LABEL_KEY"
        ]
        references = [
            record["key"]
            for record in group_records
            if record["kind"] == "REFERENCE_KEY"
        ]
        document_statistics.append(
            {
                "document_group": document_group,
                "citation_command_occurrences": citation_command_counts[
                    document_group
                ],
                "citation_key_occurrences": len(citations),
                "unique_citation_keys": len(set(citations)),
                "bibliography_key_occurrences": len(bibliography),
                "unique_bibliography_keys": len(set(bibliography)),
                "label_occurrences": len(labels),
                "unique_label_keys": len(set(labels)),
                "reference_key_occurrences": len(references),
                "unique_reference_keys": len(set(references)),
                "external_document_occurrences": sum(
                    record["kind"] == "EXTERNAL_DOCUMENT"
                    for record in group_records
                ),
                "external_link_occurrences": sum(
                    record["kind"] == "EXTERNAL_LINK" for record in group_records
                ),
            }
        )
    return {
        "lexical_rules_version": 2,
        "authority_boundary": (
            "Mechanical TeX lexical anchors only. Definition, assumption, sign/unit, "
            "code-mention and forward-reference matches are candidate cues requiring "
            "later adjudication; no record establishes scientific truth."
        ),
        "kind_counts": kind_counts,
        "document_statistics": document_statistics,
        "records": ordered_records,
    }


def build_expected_diagnostics(
    sources: list[dict[str, Any]],
    topology: dict[str, list[dict[str, Any]]],
    content_index: dict[str, Any],
) -> dict[str, list[Any]]:
    diagnostics: dict[str, list[Any]] = {
        key: [] for key in sorted(DIAGNOSTIC_KEYS)
    }
    tex_paths = {
        source["path"]
        for source in sources
        if source["owner"] == "P060_PRIMARY_RELEASE"
        and source["path"].endswith(".tex")
    }
    parsed_edges: list[dict[str, Any]] = []
    for parent_path in sorted(tex_paths):
        _, _, data = git_blob(parent_path)
        lines = data.decode("utf-8").splitlines()
        clean_text = "\n".join(strip_tex_comment(line) for line in lines)
        line_starts = [0]
        line_starts.extend(
            index + 1 for index, character in enumerate(clean_text) if character == "\n"
        )
        for match in INCLUDE_RE.finditer(clean_text):
            command, raw_target = match.groups()
            resolved_path = resolve_tex_target(parent_path, raw_target)
            record = {
                "parent_path": parent_path,
                "parent_line": bisect_right(line_starts, match.start()),
                "command": command,
                "raw_target": raw_target,
                "resolved_path": resolved_path,
            }
            parsed_edges.append(record)
            if resolved_path not in tex_paths:
                diagnostics["unresolved_include_edges"].append(record)

    parsed_identity_counts = Counter(
        (edge["parent_path"], edge["resolved_path"]) for edge in parsed_edges
    )
    diagnostics["duplicate_include_edges"] = [
        {
            "parent_path": parent_path,
            "resolved_path": resolved_path,
            "occurrences": count,
        }
        for (parent_path, resolved_path), count in sorted(parsed_identity_counts.items())
        if count > 1
    ]
    expected_root_edges = {
        (edge["parent_path"], edge["resolved_path"], edge["parent_line"])
        for edge in topology["edges"]
    }
    parsed_root_edges = {
        (edge["parent_path"], edge["resolved_path"], edge["parent_line"])
        for edge in parsed_edges
        if edge["parent_path"] in {path for _, path in ROOT_GROUPS}
    }
    diagnostics["missing_include_edges"] = [
        {"parent_path": parent, "resolved_path": child, "parent_line": line}
        for parent, child, line in sorted(expected_root_edges - parsed_root_edges)
    ]
    diagnostics["unexpected_include_edges"] = [
        edge
        for edge in parsed_edges
        if (
            edge["parent_path"],
            edge["resolved_path"],
            edge["parent_line"],
        )
        not in expected_root_edges
    ]

    adjacency: dict[str, list[str]] = {path: [] for path in tex_paths}
    for edge in parsed_edges:
        if edge["resolved_path"] in tex_paths:
            adjacency[edge["parent_path"]].append(edge["resolved_path"])
    reachable: set[str] = set()

    def mark_reachable(path: str) -> None:
        if path in reachable:
            return
        reachable.add(path)
        for child in adjacency[path]:
            mark_reachable(child)

    for _, root_path in ROOT_GROUPS:
        mark_reachable(root_path)
    diagnostics["unreachable_tex_sources"] = sorted(tex_paths - reachable)

    state: dict[str, int] = {path: 0 for path in tex_paths}
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def visit(path: str) -> None:
        state[path] = 1
        stack.append(path)
        for child in adjacency[path]:
            if state[child] == 0:
                visit(child)
            elif state[child] == 1:
                start = stack.index(child)
                cycles.add(tuple(stack[start:] + [child]))
        stack.pop()
        state[path] = 2

    for path in sorted(tex_paths):
        if state[path] == 0:
            visit(path)
    diagnostics["circular_include_dependencies"] = [
        list(cycle) for cycle in sorted(cycles)
    ]

    records = content_index["records"]
    diagnostics["external_reference_dependencies"] = [
        {
            "path": record["path"],
            "line_start": record["line_start"],
            "line_end": record["line_end"],
            "target": record["key"],
        }
        for record in records
        if record["kind"] == "EXTERNAL_DOCUMENT"
    ]
    expansion_order = {
        record["path"]: (record["document_group"], record["group_ordinal"])
        for record in topology["expansion_sequence"]
    }
    for document_group in ("CH1", "CH2", "STANDALONE"):
        group_records = [
            record
            for record in records
            if document_group_for_path(record["path"]) == document_group
        ]
        labels = [record for record in group_records if record["kind"] == "LABEL_KEY"]
        citations = [
            record for record in group_records if record["kind"] == "CITATION_KEY"
        ]
        bibliography = [
            record for record in group_records if record["kind"] == "BIBLIOGRAPHY_KEY"
        ]
        references = [
            record for record in group_records if record["kind"] == "REFERENCE_KEY"
        ]
        labels_by_key: dict[str, list[dict[str, Any]]] = {}
        for record in labels:
            labels_by_key.setdefault(record["key"], []).append(record)
        bibliography_keys = {record["key"] for record in bibliography}
        for key, occurrences in sorted(labels_by_key.items()):
            if len(occurrences) > 1:
                diagnostics["duplicate_label_keys"].append(
                    {
                        "document_group": document_group,
                        "key": key,
                        "anchors": [
                            {
                                "path": record["path"],
                                "line_start": record["line_start"],
                                "line_end": record["line_end"],
                            }
                            for record in occurrences
                        ],
                    }
                )
        for record in citations:
            if record["key"] not in bibliography_keys:
                diagnostics["unresolved_citation_keys"].append(
                    {
                        "document_group": document_group,
                        "key": record["key"],
                        "path": record["path"],
                        "line_start": record["line_start"],
                        "line_end": record["line_end"],
                    }
                )
        for record in references:
            targets = labels_by_key.get(record["key"], [])
            if not targets:
                diagnostics["unresolved_reference_candidates"].append(
                    {
                        "document_group": document_group,
                        "key": record["key"],
                        "path": record["path"],
                        "line_start": record["line_start"],
                        "line_end": record["line_end"],
                        "status": (
                            "PACKAGE_GENERATED_LABEL_CANDIDATE_UNVERIFIED_WITHOUT_LATEX_BUILD"
                            if record["key"] == "LastPage"
                            else "UNRESOLVED_IN_FROZEN_TEX_SOURCE"
                        ),
                    }
                )
                continue
            target = targets[0]
            reference_position = (
                expansion_order[record["path"]][1],
                record["line_start"],
            )
            target_position = (
                expansion_order[target["path"]][1],
                target["line_start"],
            )
            if target_position > reference_position:
                diagnostics["forward_reference_keys"].append(
                    {
                        "document_group": document_group,
                        "key": record["key"],
                        "reference_path": record["path"],
                        "reference_line_start": record["line_start"],
                        "reference_line_end": record["line_end"],
                        "target_path": target["path"],
                        "target_line_start": target["line_start"],
                        "target_line_end": target["line_end"],
                    }
                )
    return diagnostics


def independent_git_bytes(treeish: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{treeish}:{path}"],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise GroundTruthError(
            f"independent git show failed for {treeish}:{path}: "
            + proc.stderr.decode("utf-8", errors="replace")
        )
    return proc.stdout


def independent_git_blob_sha1(treeish: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", f"{treeish}:{path}"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise GroundTruthError(
            f"independent git rev-parse failed for {treeish}:{path}: "
            + proc.stderr.strip()
        )
    return proc.stdout.strip()


def independent_clean_tex(data: bytes, path: str) -> tuple[list[str], str]:
    try:
        source_lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise GroundTruthError(f"independent TeX decode failed: {path}") from exc
    clean_lines: list[str] = []
    for source_line in source_lines:
        cut = len(source_line)
        for index, character in enumerate(source_line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and source_line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        clean_lines.append(source_line[:cut])
    return source_lines, "\n".join(clean_lines)


def independent_tex_commands(data: bytes, path: str) -> list[dict[str, Any]]:
    _, clean_text = independent_clean_tex(data, path)
    line_starts = [0]
    line_starts.extend(
        index + 1 for index, character in enumerate(clean_text) if character == "\n"
    )
    commands: list[dict[str, Any]] = []
    index = 0
    while index < len(clean_text):
        if clean_text[index] != "\\" or index + 1 >= len(clean_text):
            index += 1
            continue
        command_start = index
        index += 1
        if clean_text[index] in "[]":
            commands.append(
                {
                    "command": clean_text[index],
                    "argument": None,
                    "line_start": bisect_right(line_starts, command_start),
                    "line_end": bisect_right(line_starts, index),
                }
            )
            index += 1
            continue
        name_start = index
        while index < len(clean_text) and clean_text[index].isalpha():
            index += 1
        if index == name_start:
            index += 1
            continue
        command = clean_text[name_start:index]
        if index < len(clean_text) and clean_text[index] == "*":
            command += "*"
            index += 1
        cursor = index
        while cursor < len(clean_text) and clean_text[cursor].isspace():
            cursor += 1
        while cursor < len(clean_text) and clean_text[cursor] == "[":
            depth = 1
            cursor += 1
            while cursor < len(clean_text) and depth:
                if clean_text[cursor] == "[":
                    depth += 1
                elif clean_text[cursor] == "]":
                    depth -= 1
                cursor += 1
            while cursor < len(clean_text) and clean_text[cursor].isspace():
                cursor += 1
        if cursor >= len(clean_text) or clean_text[cursor] != "{":
            commands.append(
                {
                    "command": command,
                    "argument": None,
                    "line_start": bisect_right(line_starts, command_start),
                    "line_end": bisect_right(line_starts, max(command_start, index - 1)),
                }
            )
            continue
        argument_start = cursor + 1
        depth = 1
        cursor += 1
        while cursor < len(clean_text) and depth:
            if clean_text[cursor] == "{" and clean_text[cursor - 1] != "\\":
                depth += 1
            elif clean_text[cursor] == "}" and clean_text[cursor - 1] != "\\":
                depth -= 1
            cursor += 1
        if depth:
            raise GroundTruthError(
                f"independent command scanner found unclosed argument in {path}:"
                f"{bisect_right(line_starts, command_start)}"
            )
        commands.append(
            {
                "command": command,
                "argument": clean_text[argument_start : cursor - 1],
                "line_start": bisect_right(line_starts, command_start),
                "line_end": bisect_right(line_starts, cursor - 1),
            }
        )
        # Continue inside the argument so nested citation/reference commands are
        # independently discovered instead of being hidden by an outer macro.
        index = argument_start
    return commands


def validate_independent_source_crosscheck(
    artifact: dict[str, Any], errors: list[str]
) -> None:
    try:
        manifest = json.loads(
            independent_git_bytes(EXPECTED_PROTECTED, MANIFEST_PATH).decode("utf-8")
        )
        release_entries = [
            entry for entry in manifest["entries"] if entry.get("version") == "v1.0.19"
        ]
        witness_entries = {
            entry["path"]: entry
            for entry in manifest["entries"]
            if entry.get("path") in WITNESS_PATHS
        }
        inventory_paths = [entry["path"] for entry in release_entries]
        inventory_paths.extend(SUPPLEMENTARY_PATHS)
        inventory_paths.extend(WITNESS_PATHS)
        if len(inventory_paths) != 79 or len(set(inventory_paths)) != 79:
            raise GroundTruthError("independent inventory is not 79 unique paths")
        actual_sources = artifact.get("sources")
        if not isinstance(actual_sources, list):
            errors.append("independent_crosscheck: artifact sources are not an array")
            return
        actual_by_path = {
            record.get("path"): record
            for record in actual_sources
            if isinstance(record, dict) and isinstance(record.get("path"), str)
        }
        if set(actual_by_path) != set(inventory_paths):
            errors.append("independent_crosscheck: 79-path source inventory mismatch")
            return
        release_by_path = {entry["path"]: entry for entry in release_entries}
        for path in inventory_paths:
            data = independent_git_bytes(BASELINE, path)
            record = actual_by_path[path]
            if record.get("git_blob_sha1") != independent_git_blob_sha1(BASELINE, path):
                errors.append(f"independent_crosscheck: blob mismatch {path}")
            if record.get("sha256") != hashlib.sha256(data).hexdigest():
                errors.append(f"independent_crosscheck: SHA-256 mismatch {path}")
            if record.get("size_bytes") != len(data):
                errors.append(f"independent_crosscheck: byte-size mismatch {path}")
            entry = release_by_path.get(path) or witness_entries.get(path)
            review_mode = (
                entry.get("review_mode") if entry is not None else "FULL_TEXT"
            )
            if review_mode == "FULL_TEXT":
                lines = data.decode("utf-8").splitlines()
                metrics = record.get("text_metrics")
                if not isinstance(metrics, dict) or metrics.get("physical_lines") != len(lines):
                    errors.append(f"independent_crosscheck: line extent mismatch {path}")

        tex_paths = sorted(
            entry["path"] for entry in release_entries if entry["path"].endswith(".tex")
        )
        if len(tex_paths) != 42:
            raise GroundTruthError("independent TeX inventory is not 42")
        commands_by_path = {
            path: independent_tex_commands(independent_git_bytes(BASELINE, path), path)
            for path in tex_paths
        }
        group_paths: dict[str, list[str]] = {}
        all_include_edges: list[tuple[str, int, str]] = []
        for group, root_path in ROOT_GROUPS:
            included: list[str] = []
            for command in commands_by_path[root_path]:
                if command["command"] not in {"input", "include"}:
                    continue
                argument = str(command["argument"]).strip()
                if not PurePosixPath(argument).suffix:
                    argument += ".tex"
                resolved = posixpath.normpath(
                    posixpath.join(posixpath.dirname(root_path), argument)
                )
                included.append(resolved)
                all_include_edges.append(
                    (root_path, command["line_start"], resolved)
                )
            group_paths[group] = [root_path, *included]
        nested_edges = [
            (path, command)
            for path in tex_paths
            if path not in {root for _, root in ROOT_GROUPS}
            for command in commands_by_path[path]
            if command["command"] in {"input", "include"}
        ]
        if len(all_include_edges) != 39 or nested_edges:
            errors.append("independent_crosscheck: include topology is not root-only 39")
        if set(path for paths in group_paths.values() for path in paths) != set(tex_paths):
            errors.append("independent_crosscheck: unreachable or duplicate TeX source")

        display_environments = {
            "equation",
            "equation*",
            "align",
            "align*",
            "gather",
            "gather*",
            "multline",
            "multline*",
            "flalign",
            "flalign*",
            "eqnarray",
            "eqnarray*",
        }
        derived_stats: list[dict[str, Any]] = []
        forward_records: list[dict[str, Any]] = []
        unresolved_reference_candidates: list[dict[str, Any]] = []
        displayed_equations = 0
        for group in ("CH1", "CH2", "STANDALONE"):
            paths = group_paths[group]
            path_order = {path: index for index, path in enumerate(paths, start=1)}
            labels: list[tuple[str, int, int, str]] = []
            references: list[tuple[str, int, int, str]] = []
            citation_commands: list[dict[str, Any]] = []
            citation_keys: list[str] = []
            bibliography_keys: list[str] = []
            external_documents = 0
            external_links = 0
            for path in paths:
                for command in commands_by_path[path]:
                    name = command["command"]
                    argument = command["argument"]
                    if name == "begin" and argument in display_environments:
                        displayed_equations += 1
                    elif name == "[":
                        displayed_equations += 1
                    elif name == "label" and isinstance(argument, str):
                        labels.append(
                            (path, command["line_start"], command["line_end"], argument.strip())
                        )
                    elif name in {"eqref", "ref", "autoref", "pageref"} and isinstance(argument, str):
                        references.append(
                            (path, command["line_start"], command["line_end"], argument.strip())
                        )
                    elif name.startswith("cite") and isinstance(argument, str):
                        citation_commands.append(command)
                        citation_keys.extend(
                            key.strip() for key in argument.split(",") if key.strip()
                        )
                    elif name == "bibitem" and isinstance(argument, str):
                        bibliography_keys.append(argument.strip())
                    elif name == "externaldocument":
                        external_documents += 1
                    elif name in {"href", "url"}:
                        external_links += 1
            label_by_key: dict[str, tuple[str, int, int, str]] = {}
            duplicate_labels: set[str] = set()
            for label in labels:
                if label[3] in label_by_key:
                    duplicate_labels.add(label[3])
                else:
                    label_by_key[label[3]] = label
            if duplicate_labels:
                errors.append(
                    f"independent_crosscheck: duplicate labels in {group}: "
                    + ",".join(sorted(duplicate_labels))
                )
            unresolved_citations = set(citation_keys) - set(bibliography_keys)
            if unresolved_citations:
                errors.append(
                    f"independent_crosscheck: unresolved citations in {group}: "
                    + ",".join(sorted(unresolved_citations))
                )
            for path, line_start, line_end, key in references:
                target = label_by_key.get(key)
                if target is None:
                    unresolved_reference_candidates.append(
                        {
                            "document_group": group,
                            "key": key,
                            "path": path,
                            "line_start": line_start,
                            "line_end": line_end,
                            "status": (
                                "PACKAGE_GENERATED_LABEL_CANDIDATE_UNVERIFIED_WITHOUT_LATEX_BUILD"
                                if key == "LastPage"
                                else "UNRESOLVED_IN_FROZEN_TEX_SOURCE"
                            ),
                        }
                    )
                    continue
                target_path, target_start, target_end, _ = target
                if (path_order[target_path], target_start) > (
                    path_order[path],
                    line_start,
                ):
                    forward_records.append(
                        {
                            "document_group": group,
                            "key": key,
                            "reference_path": path,
                            "reference_line_start": line_start,
                            "reference_line_end": line_end,
                            "target_path": target_path,
                            "target_line_start": target_start,
                            "target_line_end": target_end,
                        }
                    )
            derived_stats.append(
                {
                    "document_group": group,
                    "citation_command_occurrences": len(citation_commands),
                    "citation_key_occurrences": len(citation_keys),
                    "unique_citation_keys": len(set(citation_keys)),
                    "bibliography_key_occurrences": len(bibliography_keys),
                    "unique_bibliography_keys": len(set(bibliography_keys)),
                    "label_occurrences": len(labels),
                    "unique_label_keys": len(set(label[3] for label in labels)),
                    "reference_key_occurrences": len(references),
                    "unique_reference_keys": len(set(reference[3] for reference in references)),
                    "external_document_occurrences": external_documents,
                    "external_link_occurrences": external_links,
                }
            )
        forward_records.sort(
            key=lambda row: (
                row["document_group"],
                row["reference_path"],
                row["reference_line_start"],
                row["reference_line_end"],
                row["key"],
                row["target_path"],
                row["target_line_start"],
            )
        )
        unresolved_reference_candidates.sort(
            key=lambda row: (
                row["document_group"],
                row["path"],
                row["line_start"],
                row["line_end"],
                row["key"],
            )
        )
        content_index = artifact.get("content_index")
        if not isinstance(content_index, dict):
            errors.append("independent_crosscheck: content_index is not an object")
            return
        if not same_json_value(
            content_index.get("document_statistics"), derived_stats
        ):
            errors.append(
                "independent_crosscheck: balanced scanner document statistics mismatch"
            )
        expected_kind_counts = {
            "ASSUMPTION_CANDIDATE": 51,
            "BIBLIOGRAPHY_KEY": 42,
            "CITATION_KEY": 82,
            "CODE_MENTION_CANDIDATE": 255,
            "DEFINITION_CANDIDATE": 89,
            "DISPLAYED_EQUATION": 188,
            "FORWARD_REFERENCE_CANDIDATE": 102,
            "LABEL_KEY": 318,
            "REFERENCE_KEY": 949,
            "SIGN_UNIT_DECLARATION_CANDIDATE": 229,
        }
        if content_index.get("kind_counts") != expected_kind_counts:
            errors.append("independent_crosscheck: frozen lexical kind counts mismatch")
        if displayed_equations != 188:
            errors.append(
                f"independent_crosscheck: displayed equations {displayed_equations} != 188"
            )
        diagnostics = artifact.get("diagnostics")
        if not isinstance(diagnostics, dict):
            errors.append("independent_crosscheck: diagnostics is not an object")
            return
        if not same_json_value(
            diagnostics.get("forward_reference_keys"), forward_records
        ):
            actual_forward = diagnostics.get("forward_reference_keys")
            mismatch_index = None
            if isinstance(actual_forward, list):
                for index, (actual_row, expected_row) in enumerate(
                    zip(actual_forward, forward_records)
                ):
                    if not same_json_value(actual_row, expected_row):
                        mismatch_index = index
                        break
            errors.append(
                "independent_crosscheck: forward-reference records mismatch "
                f"actual_count={len(actual_forward) if isinstance(actual_forward, list) else 'NA'} "
                f"expected_count={len(forward_records)} first_mismatch={mismatch_index} "
                f"actual_row={canonical_json(actual_forward[mismatch_index]) if isinstance(actual_forward, list) and mismatch_index is not None else 'NA'} "
                f"expected_row={canonical_json(forward_records[mismatch_index]) if mismatch_index is not None else 'NA'}"
            )
        if not same_json_value(
            diagnostics.get("unresolved_reference_candidates"),
            unresolved_reference_candidates,
        ):
            errors.append(
                "independent_crosscheck: unresolved-reference candidates mismatch"
            )
        artifact_edges = artifact.get("include_topology", {}).get("edges", [])
        edge_projection = [
            (edge.get("parent_path"), edge.get("parent_line"), edge.get("resolved_path"))
            for edge in artifact_edges
            if isinstance(edge, dict)
        ]
        if edge_projection != all_include_edges:
            errors.append("independent_crosscheck: include-edge sequence mismatch")
        records = content_index.get("records")
        if not isinstance(records, list) or len(records) != 2305:
            errors.append("independent_crosscheck: lexical record count is not 2305")
        else:
            source_lines = {
                path: independent_git_bytes(BASELINE, path).decode("utf-8").splitlines()
                for path in tex_paths
            }
            for record in records:
                path = record.get("path")
                start = record.get("line_start")
                end = record.get("line_end")
                if (
                    path not in source_lines
                    or type(start) is not int
                    or type(end) is not int
                    or start < 1
                    or end < start
                    or end > len(source_lines[path])
                ):
                    errors.append("independent_crosscheck: invalid lexical anchor range")
                    break
                digest = hashlib.sha256(
                    "\n".join(source_lines[path][start - 1 : end]).encode("utf-8")
                ).hexdigest()
                if record.get("text_sha256") != digest:
                    errors.append(
                        f"independent_crosscheck: lexical anchor hash mismatch {record.get('anchor_id')}"
                    )
                    break
    except (KeyError, TypeError, ValueError, UnicodeDecodeError) as exc:
        errors.append(f"independent_crosscheck: exception {type(exc).__name__}: {exc}")


def count_include_commands(path: str) -> int:
    _, _, data = git_blob(path)
    return sum(
        len(INCLUDE_RE.findall(strip_tex_comment(line)))
        for line in data.decode("utf-8").splitlines()
    )


def build_expected_predecessor_comparison(
    sources: list[dict[str, Any]],
    topology: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    evidence_mode, evidence_blob, evidence_data = git_blob_at(
        EXPECTED_PROTECTED, PREDECESSOR_EVIDENCE_PATH
    )
    if evidence_mode != "100644":
        raise GroundTruthError(
            f"unexpected predecessor evidence git mode: {evidence_mode}"
        )
    evidence_lines = evidence_data.decode("utf-8").splitlines()
    if len(evidence_lines) != 35 or evidence_lines[34] != "Gate: `PASS_P059_THEORY_SOURCE_INDEX`.":
        raise GroundTruthError("Phase 059 predecessor structure-index anchor drift")
    evidence_record = {
        "path": PREDECESSOR_EVIDENCE_PATH,
        "git_blob_sha1": evidence_blob,
        "sha256": sha256_bytes(evidence_data),
        "physical_lines": len(evidence_lines),
        "relevant_line_ranges": [
            {"start": 3, "end": 4, "purpose": "mechanical-authority boundary"},
            {"start": 22, "end": 24, "purpose": "v1.0.18.2 source-index rows"},
            {"start": 31, "end": 35, "purpose": "stored-index pointer and gate"},
        ],
        "gate": "PASS_P059_THEORY_SOURCE_INDEX",
        "authority_boundary": (
            "Phase 059 mechanical predecessor index only; not physical or "
            "bibliography validity"
        ),
    }
    source_by_path = {source["path"]: source for source in sources}
    current_roots = {
        record["root_path"]: record for record in topology["root_records"]
    }
    root_comparisons: list[dict[str, Any]] = []
    for document_group, predecessor_path, current_path in PREDECESSOR_ROOTS:
        _, predecessor_blob, predecessor_data = git_blob(predecessor_path)
        predecessor_lines = predecessor_data.decode("utf-8").splitlines()
        predecessor_edge_count = count_include_commands(predecessor_path)
        current_source = source_by_path[current_path]
        current_root = current_roots[current_path]
        if predecessor_edge_count == 0 and current_root["include_edge_count"] > 0:
            topology_relation = "MONOLITHIC_TO_MODULAR_ROOT"
        elif predecessor_edge_count == 0 and current_root["include_edge_count"] == 0:
            topology_relation = "STANDALONE_ROOT_CHANGED"
        else:
            topology_relation = "TOPOLOGY_CHANGED"
        root_comparisons.append(
            {
                "document_group": document_group,
                "predecessor_path": predecessor_path,
                "predecessor_git_blob_sha1": predecessor_blob,
                "predecessor_sha256": sha256_bytes(predecessor_data),
                "predecessor_physical_lines": len(predecessor_lines),
                "predecessor_include_edge_count": predecessor_edge_count,
                "current_path": current_path,
                "current_git_blob_sha1": current_source["git_blob_sha1"],
                "current_sha256": current_source["sha256"],
                "current_physical_lines": current_source["text_metrics"][
                    "physical_lines"
                ],
                "current_include_edge_count": current_root["include_edge_count"],
                "topology_relation": topology_relation,
                "copied_content_status": "NOT_INFERRED_FROM_TOPOLOGY_OR_BLOB_DIFFERENCE",
                "comparison_status": "MECHANICAL_TOPOLOGY_COMPARISON_ONLY",
            }
        )
    return {
        "predecessor_version": "v1.0.18.2",
        "evidence_record": evidence_record,
        "root_comparisons": root_comparisons,
        "authority_boundary": (
            "Topology and source-identity comparison only. Copied or changed text is "
            "not newly scientifically validated by this comparison."
        ),
    }


def sum_text(sources: list[dict[str, Any]]) -> tuple[int, int, int]:
    text_sources = [item for item in sources if item["review_mode"] == "FULL_TEXT"]
    return (
        len(text_sources),
        sum(item["text_metrics"]["physical_lines"] for item in text_sources),
        sum(item["text_metrics"]["nonblank_lines"] for item in text_sources),
    )


def build_expected_counts(
    sources: list[dict[str, Any]],
    topology: dict[str, list[dict[str, Any]]],
    content_index: dict[str, Any],
    predecessor_comparison: dict[str, Any],
) -> dict[str, int]:
    release = [item for item in sources if item["owner"] == "P060_PRIMARY_RELEASE"]
    process = [item for item in sources if item["owner"] == "P060_PRIMARY_PROCESS"]
    primary = release + process
    witness = [
        item for item in sources if item["owner"] == "P060_CROSS_VERSION_WITNESS"
    ]
    release_text = sum_text(release)
    process_text = sum_text(process)
    primary_text = sum_text(primary)
    witness_text = sum_text(witness)
    inspection_text = sum_text(sources)
    tex = [item for item in release if item["path"].endswith(".tex")]
    ch1 = [item for item in tex if item["tex_group"] == "CH1_SECTION"]
    ch2 = [item for item in tex if item["tex_group"] == "CH2_SECTION"]
    roots = [item for item in tex if item["tex_group"] == "ROOT_TEX"]
    pdfs = [item for item in release if item["review_mode"] == "FULL_PDF"]
    images = [item for item in sources if item["review_mode"] == "FULL_IMAGE"]
    binaries = [
        item for item in primary if item["review_mode"] == "BINARY_INTROSPECTION"
    ]
    primary_blobs = {item["git_blob_sha1"] for item in primary}
    witness_blobs = {item["git_blob_sha1"] for item in witness}
    binary_arrays = sum(
        len(item["expected_extent"].get("arrays", [])) for item in binaries
    )
    counts = {
        "release_paths": len(release),
        "release_unique_blobs": len({item["git_blob_sha1"] for item in release}),
        "process_paths": len(process),
        "process_unique_blobs": len({item["git_blob_sha1"] for item in process}),
        "primary_paths": len(primary),
        "primary_unique_blobs": len(primary_blobs),
        "witness_occurrences": len(witness),
        "witness_new_unique_blobs": len(witness_blobs - primary_blobs),
        "inspection_path_occurrences": len(sources),
        "inspection_unique_blobs": len(primary_blobs | witness_blobs),
        "release_text_files": release_text[0],
        "release_text_physical_lines": release_text[1],
        "release_text_nonblank_lines": release_text[2],
        "process_text_files": process_text[0],
        "process_text_physical_lines": process_text[1],
        "process_text_nonblank_lines": process_text[2],
        "primary_text_files": primary_text[0],
        "primary_text_physical_lines": primary_text[1],
        "primary_text_nonblank_lines": primary_text[2],
        "witness_text_files": witness_text[0],
        "witness_text_physical_lines": witness_text[1],
        "witness_text_nonblank_lines": witness_text[2],
        "inspection_text_files": inspection_text[0],
        "inspection_text_physical_lines": inspection_text[1],
        "inspection_text_nonblank_lines": inspection_text[2],
        "tex_files": len(tex),
        "tex_physical_lines": sum(item["text_metrics"]["physical_lines"] for item in tex),
        "ch1_section_files": len(ch1),
        "ch1_section_physical_lines": sum(
            item["text_metrics"]["physical_lines"] for item in ch1
        ),
        "ch2_section_files": len(ch2),
        "ch2_section_physical_lines": sum(
            item["text_metrics"]["physical_lines"] for item in ch2
        ),
        "root_tex_files": len(roots),
        "root_tex_physical_lines": sum(
            item["text_metrics"]["physical_lines"] for item in roots
        ),
        "pdf_files": len(pdfs),
        "pdf_pages": sum(item["expected_extent"]["pages"] for item in pdfs),
        "image_occurrences": len(images),
        "image_unique_blobs": len({item["git_blob_sha1"] for item in images}),
        "binary_files": len(binaries),
        "binary_arrays": binary_arrays,
        "include_edges": len(topology["edges"]),
        "expansion_records": len(topology["expansion_sequence"]),
        "content_index_records": len(content_index["records"]),
        "predecessor_root_comparisons": len(
            predecessor_comparison["root_comparisons"]
        ),
    }
    required_values = {
        "release_paths": 66,
        "release_unique_blobs": 66,
        "process_paths": 11,
        "process_unique_blobs": 11,
        "primary_paths": 77,
        "primary_unique_blobs": 77,
        "witness_occurrences": 2,
        "witness_new_unique_blobs": 1,
        "inspection_path_occurrences": 79,
        "inspection_unique_blobs": 78,
        "primary_text_files": 60,
        "primary_text_physical_lines": 8784,
        "primary_text_nonblank_lines": 8025,
        "witness_text_files": 1,
        "witness_text_physical_lines": 1120,
        "witness_text_nonblank_lines": 1120,
        "tex_files": 42,
        "tex_physical_lines": 5636,
        "ch1_section_files": 24,
        "ch1_section_physical_lines": 3668,
        "ch2_section_files": 15,
        "ch2_section_physical_lines": 1391,
        "root_tex_files": 3,
        "root_tex_physical_lines": 577,
        "pdf_files": 3,
        "pdf_pages": 95,
        "image_occurrences": 14,
        "image_unique_blobs": 13,
        "binary_files": 1,
        "binary_arrays": 13,
        "include_edges": 39,
        "expansion_records": 42,
        "predecessor_root_comparisons": 3,
    }
    mismatches = {
        key: {"expected": value, "actual": counts.get(key)}
        for key, value in required_values.items()
        if counts.get(key) != value
    }
    if mismatches:
        raise GroundTruthError(
            "derived frozen count mismatch: "
            + json.dumps(mismatches, ensure_ascii=False, sort_keys=True)
        )
    return counts


def is_exact_int(value: Any) -> bool:
    return type(value) is int


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def same_json_value(actual: Any, expected: Any) -> bool:
    """Compare JSON values without Python's bool/int or int/float coercion."""

    return canonical_json(actual) == canonical_json(expected)


def identity_token(value: Any) -> str:
    """Return a hashable diagnostic token for any strict-JSON identity value."""

    return value if isinstance(value, str) else f"<non-string>:{canonical_json(value)}"


def is_posix_repo_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    pure = PurePosixPath(value)
    return (
        not pure.is_absolute()
        and ".." not in pure.parts
        and pure.as_posix() == value
    )


def exact_keys(
    value: Any, expected: set[str], location: str, errors: list[str]
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{location}: expected object, got {type(value).__name__}")
        return False
    actual = set(value)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        errors.append(
            f"{location}: schema keys mismatch; missing={missing}, unexpected={unexpected}"
        )
        return False
    return True


def compare_record_lists(
    location: str,
    actual: Any,
    expected: list[dict[str, Any]],
    keys: set[str],
    identity_key: str,
    errors: list[str],
) -> None:
    if not isinstance(actual, list):
        errors.append(f"{location}: expected array, got {type(actual).__name__}")
        return
    for index, record in enumerate(actual):
        exact_keys(record, keys, f"{location}[{index}]", errors)
    actual_ids = [
        identity_token(record.get(identity_key) if isinstance(record, dict) else None)
        for record in actual
    ]
    expected_ids = [record[identity_key] for record in expected]
    duplicate_ids = sorted(
        str(identity)
        for identity, count in Counter(actual_ids).items()
        if count > 1
    )
    if duplicate_ids:
        errors.append(f"{location}: duplicate {identity_key} values={duplicate_ids}")
    missing = sorted(set(expected_ids) - set(actual_ids))
    unexpected = sorted(str(value) for value in set(actual_ids) - set(expected_ids))
    if missing or unexpected:
        errors.append(
            f"{location}: identity mismatch; missing={missing}, unexpected={unexpected}"
        )
    if not same_json_value(actual, expected):
        first_mismatch = next(
            (
                index
                for index, (actual_item, expected_item) in enumerate(
                    zip(actual, expected, strict=False)
                )
                if not same_json_value(actual_item, expected_item)
            ),
            min(len(actual), len(expected)),
        )
        errors.append(
            f"{location}: ordered records differ from frozen expectation; "
            f"first_mismatch_index={first_mismatch}, "
            f"actual_count={len(actual)}, expected_count={len(expected)}"
        )


def validate_coverage(
    record: dict[str, Any], expected: dict[str, Any], index: int, errors: list[str]
) -> None:
    location = f"sources[{index}]"
    coverage = record.get("actual_coverage")
    status = record.get("coverage_status")
    is_tex = expected["path"].endswith(".tex")
    if not is_tex:
        if coverage != []:
            errors.append(f"{location}.actual_coverage: non-TeX source must be [] in Step 40")
        if status != "INVENTORIED_ONLY":
            errors.append(
                f"{location}.coverage_status: expected INVENTORIED_ONLY, got {status!r}"
            )
        return
    if status != "READ_FULL":
        errors.append(f"{location}.coverage_status: expected READ_FULL, got {status!r}")
    if not isinstance(coverage, list) or not coverage:
        errors.append(f"{location}.actual_coverage: TeX coverage must be a non-empty array")
        return
    intervals: list[tuple[int, int]] = []
    for interval_index, interval in enumerate(coverage):
        interval_location = f"{location}.actual_coverage[{interval_index}]"
        if not exact_keys(interval, {"start", "end"}, interval_location, errors):
            continue
        start = interval.get("start")
        end = interval.get("end")
        if not is_exact_int(start) or not is_exact_int(end):
            errors.append(f"{interval_location}: start/end must be integers")
            continue
        intervals.append((start, end))
    if len(intervals) != len(coverage):
        return
    expected_end = expected["text_metrics"]["physical_lines"]
    cursor = 1
    for interval_index, (start, end) in enumerate(intervals):
        if start < 1 or end < start or end > expected_end:
            errors.append(
                f"{location}.actual_coverage[{interval_index}]: out of bounds "
                f"{start}..{end} for 1..{expected_end}"
            )
            continue
        if start < cursor:
            errors.append(
                f"{location}.actual_coverage[{interval_index}]: overlap at {start}..{end}; "
                f"next expected line was {cursor}"
            )
        elif start > cursor:
            errors.append(
                f"{location}.actual_coverage[{interval_index}]: gap {cursor}..{start - 1}"
            )
        cursor = max(cursor, end + 1)
    if cursor != expected_end + 1:
        errors.append(
            f"{location}.actual_coverage: trailing gap {cursor}..{expected_end}"
        )


def validate_sources(
    actual: Any,
    expected: list[dict[str, Any]],
    attestation_summary: dict[str, Any],
    attestation_by_path: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    if not isinstance(actual, list):
        errors.append(f"sources: expected array, got {type(actual).__name__}")
        return
    for index, record in enumerate(actual):
        exact_keys(record, SOURCE_KEYS, f"sources[{index}]", errors)
    actual_paths = [
        identity_token(record.get("path") if isinstance(record, dict) else None)
        for record in actual
    ]
    expected_paths = [record["path"] for record in expected]
    duplicates = sorted(
        str(path) for path, count in Counter(actual_paths).items() if count > 1
    )
    missing = sorted(set(expected_paths) - set(actual_paths))
    unexpected = sorted(str(path) for path in set(actual_paths) - set(expected_paths))
    if duplicates:
        errors.append(f"sources: duplicate path identities={duplicates}")
    if missing or unexpected:
        errors.append(f"sources: path mismatch; missing={missing}, unexpected={unexpected}")
    if actual_paths != expected_paths:
        errors.append("sources: records are not in exact canonical POSIX path order")

    expected_by_path = {record["path"]: record for record in expected}
    fixed_keys = SOURCE_KEYS - {
        "actual_coverage",
        "coverage_status",
        "evidence",
        "authority_boundary",
    }
    for index, record in enumerate(actual):
        if not isinstance(record, dict):
            continue
        path = record.get("path")
        if not is_posix_repo_path(path):
            errors.append(f"sources[{index}].path: not a canonical POSIX repo path: {path!r}")
        expected_record = expected_by_path.get(path) if isinstance(path, str) else None
        if expected_record is None:
            continue
        for key in sorted(fixed_keys):
            if not same_json_value(record.get(key), expected_record[key]):
                errors.append(
                    f"sources[{index}].{key}: expected "
                    f"{json.dumps(expected_record[key], ensure_ascii=False, sort_keys=True)}, "
                    f"got {json.dumps(record.get(key), ensure_ascii=False, sort_keys=True)}"
                )
        evidence = record.get("evidence")
        if (
            not isinstance(evidence, list)
            or not evidence
            or any(not isinstance(item, str) or not item for item in evidence)
            or len(evidence) != len(set(evidence))
        ):
            errors.append(
                f"sources[{index}].evidence: require a non-empty unique string array"
            )
        elif path.endswith(".tex"):
            if path.endswith("appendix_phase_separation.tex"):
                group_read_token = "P060-STEP40-READ-FULL-STANDALONE-1-FILE-497-LINES"
            elif "/_sections/ch1_" in path or path.endswith(
                "graphite_ica_ch1_v1.0.19.tex"
            ):
                group_read_token = "P060-STEP40-READ-FULL-CH1-25-FILES-3711-LINES"
            else:
                group_read_token = "P060-STEP40-READ-FULL-CH2-16-FILES-1428-LINES"
            expected_read_token = (
                f"P060-STEP40-READ-FULL-PATH:{path}:1-"
                f"{expected_record['text_metrics']['physical_lines']}"
            )
            expected_evidence = [
                group_read_token,
                "P060-STEP40-READ-ATTESTATION-SHA256:"
                + attestation_summary["sha256"],
                expected_read_token,
                "P060-STEP40-LEXICAL-CONTENT-INDEX",
            ]
            if evidence != expected_evidence:
                errors.append(
                    f"sources[{index}].evidence: expected exact review claim "
                    f"{expected_evidence!r}, got {evidence!r}"
                )
            attested_record = attestation_by_path[path]
            if not same_json_value(
                record.get("actual_coverage"), attested_record["actual_coverage"]
            ) or record.get("coverage_status") != attested_record["coverage_status"]:
                errors.append(
                    f"sources[{index}]: coverage/status differs from read attestation"
                )
        elif evidence != ["P060-STEP40-GIT-BLOB-INVENTORY-ONLY"]:
            errors.append(
                f"sources[{index}].evidence: non-TeX Step 40 source must remain "
                "inventory-only"
            )
        authority = record.get("authority_boundary")
        expected_authority = (
            "Full source-content and lexical-topology evidence only; scientific "
            "truth, build success and implementation conformance remain unverified"
            if path.endswith(".tex")
            else "Git-blob identity and extent inventory only; content review belongs "
            "to its scheduled later Step"
        )
        if authority != expected_authority:
            errors.append(
                f"sources[{index}].authority_boundary: expected {expected_authority!r}, "
                f"got {authority!r}"
            )
        validate_coverage(record, expected_record, index, errors)

    primary_paths = {
        record["path"]
        for record in expected
        if record["owner"] in {"P060_PRIMARY_RELEASE", "P060_PRIMARY_PROCESS"}
    }
    primary_blob_values = [
        identity_token(record.get("git_blob_sha1"))
        for record in actual
        if isinstance(record, dict)
        and isinstance(record.get("path"), str)
        and record.get("path") in primary_paths
    ]
    duplicate_primary_blobs = sorted(
        str(blob)
        for blob, count in Counter(primary_blob_values).items()
        if count > 1
    )
    if duplicate_primary_blobs:
        errors.append(
            f"sources: duplicate primary blob identities={duplicate_primary_blobs}"
        )


def validate_topology(
    actual: Any,
    expected: dict[str, list[dict[str, Any]]],
    errors: list[str],
) -> None:
    if not exact_keys(
        actual, {"root_records", "edges", "expansion_sequence"}, "include_topology", errors
    ):
        return
    compare_record_lists(
        "include_topology.root_records",
        actual["root_records"],
        expected["root_records"],
        ROOT_RECORD_KEYS,
        "root_path",
        errors,
    )
    compare_record_lists(
        "include_topology.edges",
        actual["edges"],
        expected["edges"],
        EDGE_KEYS,
        "edge_id",
        errors,
    )
    compare_record_lists(
        "include_topology.expansion_sequence",
        actual["expansion_sequence"],
        expected["expansion_sequence"],
        EXPANSION_KEYS,
        "path",
        errors,
    )
    for index, edge in enumerate(actual.get("edges", [])):
        if not isinstance(edge, dict):
            continue
        for key in ("parent_path", "resolved_path"):
            if not is_posix_repo_path(edge.get(key)):
                errors.append(
                    f"include_topology.edges[{index}].{key}: not a canonical POSIX repo path"
                )
    for index, row in enumerate(actual.get("expansion_sequence", [])):
        if isinstance(row, dict) and not is_posix_repo_path(row.get("path")):
            errors.append(
                f"include_topology.expansion_sequence[{index}].path: "
                "not a canonical POSIX repo path"
            )


def validate_content_index(
    actual: Any, expected: dict[str, Any], errors: list[str]
) -> None:
    if not exact_keys(actual, CONTENT_INDEX_KEYS, "content_index", errors):
        return
    if not same_json_value(
        actual.get("lexical_rules_version"), expected["lexical_rules_version"]
    ):
        errors.append("content_index.lexical_rules_version: exact value mismatch")
    if actual.get("authority_boundary") != expected["authority_boundary"]:
        errors.append("content_index.authority_boundary: exact value mismatch")
    if not same_json_value(actual.get("kind_counts"), expected["kind_counts"]):
        errors.append(
            "content_index.kind_counts: exact lexical-kind counts mismatch; expected="
            + canonical_json(expected["kind_counts"])
            + ", got="
            + canonical_json(actual.get("kind_counts"))
        )
    compare_record_lists(
        "content_index.document_statistics",
        actual.get("document_statistics"),
        expected["document_statistics"],
        DOCUMENT_STATISTIC_KEYS,
        "document_group",
        errors,
    )
    compare_record_lists(
        "content_index.records",
        actual.get("records"),
        expected["records"],
        CONTENT_RECORD_KEYS,
        "anchor_id",
        errors,
    )
    records = actual.get("records")
    if not isinstance(records, list):
        return
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        if not is_posix_repo_path(record.get("path")):
            errors.append(
                f"content_index.records[{index}].path: not a canonical POSIX repo path"
            )
        if not is_exact_int(record.get("line_start")) or not is_exact_int(
            record.get("line_end")
        ):
            errors.append(
                f"content_index.records[{index}]: line_start/line_end must be integers"
            )
        elif record["line_start"] < 1 or record["line_end"] < record["line_start"]:
            errors.append(f"content_index.records[{index}]: invalid line range")
        expected_authority = (
            CANDIDATE_CUE_AUTHORITY
            if isinstance(record.get("kind"), str)
            and record["kind"].endswith("_CANDIDATE")
            else LEXICAL_AUTHORITY
        )
        if record.get("authority") != expected_authority:
            errors.append(
                f"content_index.records[{index}].authority: expected "
                f"{expected_authority!r}"
            )


def validate_predecessor_comparison(
    actual: Any, expected: dict[str, Any], errors: list[str]
) -> None:
    if not exact_keys(
        actual,
        PREDECESSOR_COMPARISON_KEYS,
        "predecessor_comparison",
        errors,
    ):
        return
    evidence = actual.get("evidence_record")
    exact_keys(
        evidence,
        PREDECESSOR_EVIDENCE_KEYS,
        "predecessor_comparison.evidence_record",
        errors,
    )
    compare_record_lists(
        "predecessor_comparison.root_comparisons",
        actual.get("root_comparisons"),
        expected["root_comparisons"],
        PREDECESSOR_ROOT_COMPARISON_KEYS,
        "document_group",
        errors,
    )
    if not same_json_value(actual, expected):
        errors.append(
            "predecessor_comparison: exact mechanical predecessor comparison mismatch"
        )
    if isinstance(evidence, dict) and not is_posix_repo_path(evidence.get("path")):
        errors.append(
            "predecessor_comparison.evidence_record.path: not a canonical POSIX repo path"
        )
    comparisons = actual.get("root_comparisons")
    if isinstance(comparisons, list):
        for index, record in enumerate(comparisons):
            if not isinstance(record, dict):
                continue
            for key in ("predecessor_path", "current_path"):
                if not is_posix_repo_path(record.get(key)):
                    errors.append(
                        f"predecessor_comparison.root_comparisons[{index}].{key}: "
                        "not a canonical POSIX repo path"
                    )
            if record.get("copied_content_status") != (
                "NOT_INFERRED_FROM_TOPOLOGY_OR_BLOB_DIFFERENCE"
            ):
                errors.append(
                    f"predecessor_comparison.root_comparisons[{index}]: copied content "
                    "must not be inferred from topology or blob identity"
                )


def validate_diagnostics(
    actual: Any, expected: dict[str, list[Any]], errors: list[str]
) -> None:
    if not exact_keys(actual, DIAGNOSTIC_KEYS, "diagnostics", errors):
        return
    for key in sorted(DIAGNOSTIC_KEYS):
        value = actual[key]
        if not isinstance(value, list):
            errors.append(f"diagnostics.{key}: expected array")
    if not same_json_value(actual, expected):
        errors.append(
            "diagnostics: exact frozen diagnostic/candidate mismatch; expected="
            + canonical_json(expected)
            + ", got="
            + canonical_json(actual)
        )


def expected_protection() -> dict[str, Any]:
    protected_tip = run_git("rev-parse", PROTECTED_REF)
    main_tip = run_git("rev-parse", MAIN_REF)
    claude_diff = run_git("diff", "--name-only", PROTECTED_REF, "--", "Claude")
    claude_diff_paths = claude_diff.splitlines() if claude_diff else []
    untracked_claude = run_git(
        "ls-files", "--others", "--exclude-standard", "--", "Claude"
    )
    untracked_claude_paths = untracked_claude.splitlines() if untracked_claude else []
    active_branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
    upstream_ref = run_git(
        "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"
    )
    local_tip = run_git("rev-parse", "HEAD")
    upstream_tip = run_git("rev-parse", "@{upstream}")
    origin_active_ref = f"refs/heads/{active_branch}"
    remote_proc = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", origin_active_ref],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if remote_proc.returncode != 0 or not remote_proc.stdout.strip():
        raise GroundTruthError(
            "cannot resolve origin active tip: " + remote_proc.stderr.strip()
        )
    origin_active_tip = remote_proc.stdout.split()[0]
    active_refs_equal = local_tip == upstream_tip == origin_active_tip
    status_proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status_proc.returncode != 0:
        raise GroundTruthError("git status failed: " + status_proc.stderr.strip())
    worktree_paths = []
    status_entries = [entry for entry in status_proc.stdout.split("\0") if entry]
    index = 0
    while index < len(status_entries):
        entry = status_entries[index]
        if len(entry) < 4:
            raise GroundTruthError(f"invalid porcelain status entry: {entry!r}")
        status_code = entry[:2]
        path = entry[3:]
        worktree_paths.append(PurePosixPath(path).as_posix())
        if "R" in status_code or "C" in status_code:
            index += 1
            if index >= len(status_entries):
                raise GroundTruthError("porcelain rename/copy entry lacks source path")
            worktree_paths.append(PurePosixPath(status_entries[index]).as_posix())
        index += 1
    unexpected_worktree_paths = sorted(set(worktree_paths) - ALLOWED_STEP_PATHS)
    if protected_tip != EXPECTED_PROTECTED:
        raise GroundTruthError(
            f"protected drift: {protected_tip} != {EXPECTED_PROTECTED}"
        )
    if main_tip != EXPECTED_MAIN:
        raise GroundTruthError(f"main drift: {main_tip} != {EXPECTED_MAIN}")
    if claude_diff_paths:
        raise GroundTruthError(
            "Claude drift relative to protected: " + json.dumps(claude_diff_paths)
        )
    if untracked_claude_paths:
        raise GroundTruthError(
            "untracked Claude paths: " + json.dumps(untracked_claude_paths)
        )
    if active_branch != "codex/anode-fit-v1025_2-canonical-completion":
        raise GroundTruthError(f"unexpected active branch: {active_branch}")
    if upstream_ref != f"origin/{active_branch}":
        raise GroundTruthError(f"unexpected upstream ref: {upstream_ref}")
    if not active_refs_equal:
        raise GroundTruthError(
            "active ref divergence: "
            f"local={local_tip}, upstream={upstream_tip}, origin={origin_active_tip}"
        )
    if unexpected_worktree_paths:
        raise GroundTruthError(
            "unexpected worktree paths outside Step 40 allowlist: "
            + json.dumps(unexpected_worktree_paths)
        )
    return {
        "protected_ref": PROTECTED_REF,
        "expected_protected_tip": EXPECTED_PROTECTED,
        "actual_protected_tip": protected_tip,
        "main_ref": MAIN_REF,
        "expected_main_tip": EXPECTED_MAIN,
        "actual_main_tip": main_tip,
        "claude_diff_paths": claude_diff_paths,
        "untracked_claude_paths": untracked_claude_paths,
        "active_branch": active_branch,
        "upstream_ref": upstream_ref,
        "origin_active_ref": origin_active_ref,
        "active_refs_equal": active_refs_equal,
        "allowed_step_paths": sorted(ALLOWED_STEP_PATHS),
        "unexpected_worktree_paths": unexpected_worktree_paths,
    }


def validate_artifact(artifact: Any) -> list[str]:
    errors: list[str] = []
    if not exact_keys(artifact, TOP_LEVEL_KEYS, "artifact", errors):
        return errors

    scalar_expectations = {
        "schema_version": 1,
        "generated_date": "2026-08-26",
        "phase": 60,
        "step": 40,
        "artifact_kind": ARTIFACT_KIND,
        "baseline_commit": BASELINE,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    for key, expected_value in scalar_expectations.items():
        if not same_json_value(artifact.get(key), expected_value):
            errors.append(
                f"artifact.{key}: expected {expected_value!r}, got {artifact.get(key)!r}"
            )

    expected_sources = load_expected_sources()
    expected_attestation, attestation_by_path = load_read_attestation(expected_sources)
    expected_topology = build_expected_topology(expected_sources)
    expected_content_index = build_expected_content_index(expected_sources)
    expected_predecessor_comparison = build_expected_predecessor_comparison(
        expected_sources, expected_topology
    )
    expected_diagnostics = build_expected_diagnostics(
        expected_sources, expected_topology, expected_content_index
    )
    expected_counts = build_expected_counts(
        expected_sources,
        expected_topology,
        expected_content_index,
        expected_predecessor_comparison,
    )
    counts = artifact.get("counts")
    if isinstance(counts, dict):
        if set(counts) != set(expected_counts):
            errors.append(
                "artifact.counts: schema keys mismatch; missing="
                f"{sorted(set(expected_counts) - set(counts))}, unexpected="
                f"{sorted(set(counts) - set(expected_counts))}"
            )
        for key, value in counts.items():
            if type(value) is not int:
                errors.append(
                    f"artifact.counts.{key}: expected integer, got {type(value).__name__}"
                )
    else:
        errors.append(f"artifact.counts: expected object, got {type(counts).__name__}")
    if not same_json_value(counts, expected_counts):
        errors.append(
            "artifact.counts: exact count schema/value mismatch; expected="
            + json.dumps(expected_counts, ensure_ascii=False, sort_keys=True)
            + ", got="
            + json.dumps(artifact.get("counts"), ensure_ascii=False, sort_keys=True)
        )
    if not exact_keys(
        artifact.get("read_attestation"),
        READ_ATTESTATION_SUMMARY_KEYS,
        "read_attestation",
        errors,
    ) or not same_json_value(
        artifact.get("read_attestation"), expected_attestation
    ):
        errors.append("read_attestation: exact provenance summary mismatch")
    validate_sources(
        artifact.get("sources"),
        expected_sources,
        expected_attestation,
        attestation_by_path,
        errors,
    )
    validate_topology(artifact.get("include_topology"), expected_topology, errors)
    validate_content_index(
        artifact.get("content_index"), expected_content_index, errors
    )
    validate_predecessor_comparison(
        artifact.get("predecessor_comparison"),
        expected_predecessor_comparison,
        errors,
    )
    validate_diagnostics(artifact.get("diagnostics"), expected_diagnostics, errors)

    live_protection = expected_protection()
    if not exact_keys(artifact.get("protection"), PROTECTION_KEYS, "protection", errors):
        return errors
    if not same_json_value(artifact["protection"], live_protection):
        errors.append(
            "protection: exact live/frozen state mismatch; expected="
            + json.dumps(live_protection, ensure_ascii=False, sort_keys=True)
            + ", got="
            + json.dumps(artifact["protection"], ensure_ascii=False, sort_keys=True)
        )
    validate_independent_source_crosscheck(artifact, errors)
    return errors


def display_artifact_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the Phase 060 Step 40 frozen source-topology artifact."
    )
    parser.add_argument(
        "--artifact",
        default=str(DEFAULT_ARTIFACT),
        help=(
            "Topology JSON to validate. Relative paths resolve from the repository root; "
            "absolute paths support disposable negative fixtures."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    artifact_path = Path(args.artifact)
    if not artifact_path.is_absolute():
        artifact_path = REPO / artifact_path
    artifact_label = display_artifact_path(artifact_path)

    if not artifact_path.is_file():
        print(f"FAIL missing_artifact: {artifact_label}")
        print("FAIL_P060_STEP40_SOURCE_TOPOLOGY 0/1")
        return 2

    try:
        artifact = strict_json(artifact_path)
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        DuplicateKeyError,
        InvalidJsonConstantError,
    ) as exc:
        print(f"FAIL invalid_artifact_json: {artifact_label}: {exc}")
        print("FAIL_P060_STEP40_SOURCE_TOPOLOGY 0/1")
        return 1

    try:
        errors = validate_artifact(artifact)
    except (
        GroundTruthError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        DuplicateKeyError,
        InvalidJsonConstantError,
    ) as exc:
        print(f"FAIL frozen_ground_truth: {exc}")
        print("FAIL_P060_STEP40_SOURCE_TOPOLOGY 0/1")
        return 3

    if errors:
        for error in errors:
            print(f"FAIL artifact_contract: {error}")
        print(f"FAIL_P060_STEP40_SOURCE_TOPOLOGY 0/{len(errors)}")
        return 1

    print("PASS_P060_STEP40_SOURCE_TOPOLOGY 1/1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
