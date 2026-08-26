#!/usr/bin/env python3
"""Build deterministic Phase 062 Step 52 source/process topology evidence.

The builder reads immutable Git objects and incorporates the bounded human
full-read and visual attestations completed for this Step.  Those attestations
remain source/process/layout evidence and never promote scientific truth.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
BUILDER = Path(__file__).resolve()
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
TOPOLOGY = REPO / "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION = REPO / "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
ACTIVATION_COMMIT = "76dccbaee0efdd16a4d22c25527a1a8ab3108559"
EXPECTED_MANIFEST_NORMALIZED_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
SUPPLEMENTAL_PATH = "Claude/plans/2026-07-16-v1021-master-plan.md"
SUPPLEMENTAL_BLOB = "de26c03b53bedbe1cc4363bb07f66e9ca9da77f7"
Q1_REPORT_PATH = "Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md"
Q1_REPORT_BLOB = "3c5a20f8609b4a2cd1f9ce85d61c302b59180c50"
Q1_REPORT_ORIGIN_COMMIT = "1e6c610f11682d87a416957b1cf65b4c8df53697"
GIT_TIMEOUT = 60

IMPLEMENTATION_CHAIN = [
    ("Q0", "b4e939b0547cd4bf73bca30abe10fd164954c277"),
    ("Q2", "1635bc97fb7bd9c3fabc720e91bf09e5ba31798f"),
    ("Q3", "c7420915dfae8ef076319737bddcc532a86d9505"),
    ("Q4", "46360bd0630ee6039d595b6980ad28862b362eb7"),
    ("Q5NAV", "287d38d36415103cc28822f33c2520f734f1d6a9"),
    ("Q5", "9d208db8cec382b5d7d0dc79b4fc6a2e88cdb444"),
    ("Q5B", "7316e7915db8727f794614b61f98d4df7f803bfd"),
    ("Q6", "bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17"),
    ("Q7", "9ea5cb23754061261923bab013e279d7f6938723"),
    ("Q8", "e96147fe4d5cefcccf733702e9bee78ba0beb025"),
]
SUPPORTING_COMMITS = [
    ("MASTER_PLAN_V1", "66e3510d67162dd6bd88158557f96621cbedbbcf"),
    ("Q1_PARTIAL_REPORT_ORIGIN", Q1_REPORT_ORIGIN_COMMIT),
    ("DOWNSTREAM_Q9_Q10_CLOSURE", "5d815235de4e302ff5d7a076d525921ab417eadf"),
]
SUPPORTING_CHRONOLOGY = {
    "MASTER_PLAN_V1": "PRECURSOR_PLAN",
    "Q1_PARTIAL_REPORT_ORIGIN": "PRE_Q0_PARTIAL_REPORT",
    "DOWNSTREAM_Q9_Q10_CLOSURE": "DOWNSTREAM_AUTHORED",
}
SNAPSHOT_AUTHORED_COMMITS = {
    q_id: commit for q_id, commit in IMPLEMENTATION_CHAIN if q_id in {"Q0", "Q2", "Q3", "Q4", "Q5NAV", "Q5", "Q5B", "Q6", "Q7"}
}
PROCESS_DOCUMENT_COMMITS = {
    "CHANGE_LOG": {"created": IMPLEMENTATION_CHAIN[0][1], "last_modified": IMPLEMENTATION_CHAIN[-2][1]},
    "EXECUTION_LEDGER": {"created": IMPLEMENTATION_CHAIN[0][1], "last_modified": SUPPORTING_COMMITS[-1][1]},
    "REFERENCE_LEDGER": {"created": IMPLEMENTATION_CHAIN[0][1], "last_modified": IMPLEMENTATION_CHAIN[-2][1]},
    "HANDOVER": {"created": SUPPORTING_COMMITS[-1][1], "last_modified": SUPPORTING_COMMITS[-1][1]},
}
PROCESS_PHASES = ["Q0", "Q1", "Q2", "Q3", "Q4", "Q5NAV", "Q5", "Q5B", "Q6", "Q7", "Q8", "Q9", "Q10"]
SNAPSHOT_PATHS = {
    "Q0": "Claude/docs/v1.0.21/results/snapshot_v1021_q0.json",
    "Q1": None,
    "Q2": "Claude/docs/v1.0.21/results/snapshot_v1021_q2.json",
    "Q3": "Claude/docs/v1.0.21/results/snapshot_v1021_q3.json",
    "Q4": "Claude/docs/v1.0.21/results/snapshot_v1021_q4.json",
    "Q5NAV": "Claude/docs/v1.0.21/results/snapshot_v1021_q5nav.json",
    "Q5": "Claude/docs/v1.0.21/results/snapshot_v1021_q5.json",
    "Q5B": "Claude/docs/v1.0.21/results/snapshot_v1021_q5b.json",
    "Q6": "Claude/docs/v1.0.21/results/snapshot_v1021_q6.json",
    "Q7": "Claude/docs/v1.0.21/results/snapshot_v1021_q7.json",
    "Q8": None,
    "Q9": None,
    "Q10": None,
}
PROCESS_DOCUMENTS = [
    ("P062-PROC-DOC-001", "CHANGE_LOG", "Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md"),
    ("P062-PROC-DOC-002", "EXECUTION_LEDGER", "Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md"),
    ("P062-PROC-DOC-003", "REFERENCE_LEDGER", "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md"),
    ("P062-PROC-DOC-004", "HANDOVER", "Claude/docs/v1.0.21/HANDOVER_v1.0.21.md"),
]
PHASE057_INPUTS = [
    ("P062-NAV-001", "Codex/plans/2026-07-28-phase057-v1021-read-map.md", 85),
    ("P062-NAV-002", "Codex/results/PHASE_057J_V1021_CONTROL_DOCUMENT_INTENT_OBSERVATIONS.md", 197),
    ("P062-NAV-003", "Codex/results/PHASE_057K_V1021_Q0_BASELINE_OBSERVATIONS.md", 79),
    ("P062-NAV-004", "Codex/results/PHASE_057L_V1021_Q2_Q3_SNAPSHOT_OBSERVATIONS.md", 126),
    ("P062-NAV-005", "Codex/results/PHASE_057M_V1021_Q4_Q5NAV_SNAPSHOT_OBSERVATIONS.md", 97),
    ("P062-NAV-006", "Codex/results/PHASE_057N_V1021_Q5_Q5B_SNAPSHOT_OBSERVATIONS.md", 101),
    ("P062-NAV-007", "Codex/results/PHASE_057O_V1021_Q6_Q7_AND_VERSION_CLOSE_OBSERVATIONS.md", 134),
]
PHASE057_OBSERVATION_IDS = [f"INTENT-PROV-{index:04d}" for index in range(66, 96)]
PHASE057_OBSERVATION_RE = re.compile(r"^### (INTENT-PROV-(\d{4}))\s+—\s+(.+)$")

PROCESS_ALIASES = [
    {
        "alias_q_id": "Q5NAV",
        "parent_q_id": "Q5",
        "state": "SUBPHASE_ALIAS",
        "dedicated_plan_step_log_result_expected": False,
        "reason": "Q5NAV is an intermediate navigation snapshot label inside the Q5 implementation sequence, not an independently planned Q phase.",
    },
    {
        "alias_q_id": "Q5B",
        "parent_q_id": "Q5",
        "state": "SUBPHASE_ALIAS",
        "dedicated_plan_step_log_result_expected": False,
        "reason": "Q5B is an intermediate bibliography snapshot label inside the Q5 implementation sequence, not an independently planned Q phase.",
    },
]

HUMAN_REVIEW_PARTITIONS: dict[str, dict[str, Any]] = {
    "A_RELEASE_ROOT_AND_PDF": {
        "release_indices": [[1, 54]],
        "expected": {"paths": 54, "text": 49, "pdf": 5, "pdf_pages": 214, "snapshots": 0},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_evidence": {
            "evidence_id": "P062-REVIEW-A-RELEASE-PDF-214",
            "reviewer_ids": ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_PDF_AUDITOR", "STEP52_CONTROLLER"],
            "method": "UTF8_LINE_BY_LINE_AND_POPPLER_120_DPI_FULL_PAGE_VISUAL_REVIEW",
            "renderer": "Poppler pdftoppm 26.05.0",
            "text": "49/49 frozen UTF-8 blobs read line 1 through EOF",
            "pdf": "5/5 frozen Git blobs rendered with Poppler at 120 dpi and visually inspected page 1 through EOF",
            "pdf_page_coverage": "214/214 = 8+76+78+26+26",
            "controller_drilldown": "Ch1 base/nav pages 68-70 inspected at original detail",
        },
        "findings": [{
            "finding_id": "P062-VIS-001",
            "severity": "P1_LAYOUT",
            "state": "CONFIRMED_VISUAL_DEFECT",
            "paths": [
                "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf",
                "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf",
            ],
            "pages": [69],
            "description": "Table 8 rightmost column is clipped at the physical right page edge in both Ch1 variants.",
            "authority_ceiling": "VISUAL_LAYOUT_ONLY",
        }],
        "ground_not_found": [],
        "unverified": [
            "independent build provenance",
            "scientific, numerical, material and experimental truth",
        ],
    },
    "B_RELEASE_PROCESS_AND_SNAPSHOTS": {
        "release_indices": [[55, 68]],
        "expected": {"paths": 14, "text": 14, "pdf": 0, "pdf_pages": 0, "snapshots": 9},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_evidence": {
            "evidence_id": "P062-REVIEW-B-PROCESS-SNAPSHOT",
            "reviewer_ids": ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_CONTROLLER"],
            "method": "UTF8_LINE_BY_LINE_PLUS_STRICT_JSON_DUPLICATE_KEY_NONFINITE_REJECTION_AND_RECURSIVE_TRAVERSAL",
            "text": "14/14 frozen process, snapshot, tool and test blobs read line 1 through EOF",
            "snapshots": "9/9 strict duplicate-key/nonfinite parse and recursive traversal",
            "snapshot_extent": "12,211/12,211 physical lines; 10,425 value/container nodes plus 6,847 mapping-key nodes",
        },
        "findings": [],
        "ground_not_found": [
            "Q1 snapshot",
            "Q8 snapshot",
            "independent per-Q plan, step-log and result artifacts",
        ],
        "unverified": [
            "Q8 semantic/runtime equality beyond the frozen self-report",
            "historical build and test self-reports",
        ],
    },
    "C_SUPPLEMENTAL_PROCESS_CONTROL": {
        "release_indices": [],
        "expected": {"paths": 1, "text": 1, "pdf": 0, "pdf_pages": 0, "snapshots": 0},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_evidence": {
            "evidence_id": "P062-REVIEW-C-SUPPLEMENTAL",
            "reviewer_ids": ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_CONTROLLER"],
            "method": "UTF8_LINE_BY_LINE",
            "coverage": "Claude/plans/2026-07-16-v1021-master-plan.md lines 1-76",
            "extent": "76 physical / 59 nonblank lines / 10,664 Git bytes",
        },
        "findings": [],
        "ground_not_found": ["independently frozen first-order user transcript"],
        "unverified": ["first-order authority of D21-1 through D21-6-prime"],
    },
    "D_Q1_COMPARISON_REPORT": {
        "release_indices": [],
        "expected": {"paths": 1, "text": 1, "pdf": 0, "pdf_pages": 0, "snapshots": 0},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_evidence": {
            "evidence_id": "P062-REVIEW-D-Q1-COMPARISON",
            "reviewer_ids": ["STEP52_TEXT_PROCESS_AUDITOR", "STEP52_CONTROLLER"],
            "method": "UTF8_LINE_BY_LINE_WITH_CHRONOLOGY_CONFLICT_COMPARISON",
            "coverage": "Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md lines 1-291",
            "extent": "291 physical / 222 nonblank lines / 44,969 Git bytes",
        },
        "findings": [{
            "finding_id": "P062-PROC-CONFLICT-001",
            "state": "PARTIAL_CONFLICT",
            "description": "The report physically contains sections 1-8 and REPORT COMPLETE, while the later frozen master-plan correction history says sections 7-8 were incomplete; sections 1-6 remain partial process evidence and sections 7-8 remain a chronology-conflicted draft surface.",
        }],
        "ground_not_found": ["dedicated Q1 completion plan, step log, result and snapshot"],
        "unverified": ["report-internal WebSearch/DOI and scientific truth claims"],
    },
}

PHASE057_REPRODUCTIONS: dict[str, dict[str, Any]] = {
    "P062-NAV-001": {
        "state": "COVERAGE_MAP_REPRODUCED",
        "evidence": ["13-document/12,328-line historical queue is consistent with the nine snapshots plus four release control documents"],
    },
    "P062-NAV-002": {
        "state": "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
        "evidence": ["INTENT-PROV-0066 through 0074 internal process facts reproduced; external science, DOI, runtime and build claims remain unverified"],
    },
    "P062-NAV-003": {
        "state": "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
        "evidence": ["INTENT-PROV-0075 through 0077 reproduced; Q0 normalized payload equals v1.0.20 final while structural identity does not establish physics truth"],
    },
    "P062-NAV-004": {
        "state": "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
        "evidence": ["INTENT-PROV-0078 through 0082 reproduced; Q2 adds four registered equations, Q3 five equations and two bibliography keys, without experimental assets"],
    },
    "P062-NAV-005": {
        "state": "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
        "evidence": ["INTENT-PROV-0083 through 0086 reproduced; Q4 adds five figure labels and Q5NAV five navigation labels, with no registered equation change"],
    },
    "P062-NAV-006": {
        "state": "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
        "evidence": ["INTENT-PROV-0087 through 0090 reproduced; Q5 adds three labels outside the registered equation delta and Q5B adds two bibliography keys"],
    },
    "P062-NAV-007": {
        "state": "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
        "evidence": ["INTENT-PROV-0091 through 0094 reproduced; 0095 remains provisional advice rather than an adopted disposition"],
    },
}

PDF_SOURCE_RELATIONSHIPS: list[dict[str, Any]] = [
    {
        "relationship_id": "P062-PDF-SOURCE-001",
        "source_path": "Claude/docs/v1.0.21/appendix_phase_separation.tex",
        "pdf_path": "Claude/docs/v1.0.21/appendix_phase_separation.pdf",
        "source_relationship_state": "SOURCE_DRIVER_PRESENT",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "SOURCE_AND_DOCUMENT_IDENTITY_ONLY",
        "external_scientific_truth_validated": False,
        "external_material_truth_validated": False,
    },
    {
        "relationship_id": "P062-PDF-SOURCE-002",
        "source_path": "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex",
        "pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf",
        "source_relationship_state": "SOURCE_DRIVER_PRESENT",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "SOURCE_AND_DOCUMENT_IDENTITY_ONLY",
        "external_scientific_truth_validated": False,
        "external_material_truth_validated": False,
    },
    {
        "relationship_id": "P062-PDF-SOURCE-003",
        "source_path": "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.tex",
        "pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf",
        "source_relationship_state": "SOURCE_DRIVER_PRESENT",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "SOURCE_AND_DOCUMENT_IDENTITY_ONLY",
        "external_scientific_truth_validated": False,
        "external_material_truth_validated": False,
    },
    {
        "relationship_id": "P062-PDF-SOURCE-004",
        "source_path": "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.tex",
        "pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf",
        "source_relationship_state": "SOURCE_DRIVER_PRESENT",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "SOURCE_AND_DOCUMENT_IDENTITY_ONLY",
        "external_scientific_truth_validated": False,
        "external_material_truth_validated": False,
    },
    {
        "relationship_id": "P062-PDF-SOURCE-005",
        "source_path": "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.tex",
        "pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf",
        "source_relationship_state": "SOURCE_DRIVER_PRESENT",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "SOURCE_AND_DOCUMENT_IDENTITY_ONLY",
        "external_scientific_truth_validated": False,
        "external_material_truth_validated": False,
    },
]

PDF_VARIANT_RELATIONSHIPS: list[dict[str, Any]] = [
    {
        "relationship_id": "P062-PDF-VARIANT-CH1",
        "base_pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf",
        "navigation_pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf",
        "base_pages": 76,
        "navigation_pages": 78,
        "base_outline_nodes": 81,
        "navigation_outline_nodes": 85,
        "base_annotations": 1134,
        "navigation_annotations": 1227,
        "exact_normalized_page_text_identity_pages": 0,
        "direct_visual_difference": "navigation pages 73-74 add D.2 integrated symbol correspondence and Ch1-Ch2 relationship tables; references move from base pages 73-76 to navigation pages 75-78",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "VISUAL_AND_DOCUMENT_STRUCTURE_ONLY",
    },
    {
        "relationship_id": "P062-PDF-VARIANT-CH2",
        "base_pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf",
        "navigation_pdf_path": "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf",
        "base_pages": 26,
        "navigation_pages": 26,
        "base_outline_nodes": 39,
        "navigation_outline_nodes": 39,
        "base_annotations": 320,
        "navigation_annotations": 323,
        "same_ordinal_page_text_similarity_range": [0.9691, 0.9997],
        "exact_normalized_page_text_identity_pages": 0,
        "direct_visual_difference": "navigation title states global navigation edition and page 3 adds three links",
        "build_provenance_state": "UNVERIFIED",
        "authority_ceiling": "VISUAL_AND_DOCUMENT_STRUCTURE_ONLY",
    },
]


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


def reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def strict_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise NonFiniteNumberError(value)
    return parsed


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def walk_json(value: Any, path: str = "$", stats: dict[str, int] | None = None) -> dict[str, int]:
    if stats is None:
        stats = {"nodes": 0, "mapping_keys": 0, "objects": 0, "arrays": 0, "scalars": 0, "max_depth": 0}
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], path.count(".") + path.count("["))
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(path)
    if isinstance(value, dict):
        stats["objects"] += 1
        stats["mapping_keys"] += len(value)
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(path)
            walk_json(child, f"{path}.{key}", stats)
    elif isinstance(value, list):
        stats["arrays"] += 1
        for index, child in enumerate(value):
            walk_json(child, f"{path}[{index}]", stats)
    elif value is None or isinstance(value, (str, int, float, bool)):
        stats["scalars"] += 1
    else:
        raise TypeError(path)
    return stats


def strict_json_bytes(data: bytes) -> tuple[Any, dict[str, int]]:
    value = json.loads(
        data.decode("utf-8"), object_pairs_hook=strict_pairs,
        parse_constant=reject_constant, parse_float=strict_float,
    )
    return value, walk_json(value)


def normalize_lf(data: bytes) -> bytes:
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def strict_utf8_lf(data: bytes, path: str) -> tuple[str, list[str]]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not allowed in frozen text evidence: {path}")
    if b"\r" in data:
        raise ValueError(f"non-LF newline is not allowed in frozen text evidence: {path}")
    text = data.decode("utf-8")
    return text, text.splitlines()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def git_bytes(*args: str) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, timeout=GIT_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"git timeout: {' '.join(args)}") from exc
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip())
    return proc.stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def git_blob(commit: str, path: str) -> tuple[str, str, bytes]:
    raw = git_bytes("ls-tree", "--full-tree", "-z", commit, "--", path)
    rows = [row for row in raw.split(b"\0") if row]
    if len(rows) != 1:
        raise FileNotFoundError(f"{commit}:{path}")
    metadata, actual_path = rows[0].split(b"\t", 1)
    mode, object_type, blob = metadata.decode("ascii").split()
    if object_type != "blob" or actual_path.decode("utf-8") != path:
        raise ValueError(f"Git path identity mismatch: {path}")
    return mode, blob, git_bytes("cat-file", "blob", blob)


def commit_record(event: str, commit: str, chronology: str) -> dict[str, Any]:
    resolved = git_text("rev-parse", f"{commit}^{{commit}}")
    if resolved != commit:
        raise ValueError(f"commit mismatch: {event}")
    parents = git_text("show", "-s", "--format=%P", commit).split()
    subject = git_text("show", "-s", "--format=%s", commit)
    paths = sorted(
        row.decode("utf-8").replace("\\", "/")
        for row in git_bytes("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", commit).split(b"\0")
        if row
    )
    raw_diff_tree = git_bytes("diff-tree", "--root", "--raw", "-r", "--no-renames", "-z", commit)
    patch = git_bytes("show", "--format=", "--binary", "--full-index", "--no-ext-diff", "--no-renames", commit)
    return {
        "event": event, "commit": commit, "parents": parents, "subject": subject,
        "changed_paths": paths,
        "changed_path_set_sha256": sha256(("\n".join(paths) + "\n").encode("utf-8")),
        "raw_diff_tree_sha256": sha256(raw_diff_tree),
        "patch_sha256": sha256(patch),
        "chronology_state": chronology,
    }


def is_ancestor(older: str, newer: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=GIT_TIMEOUT, check=False,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    return completed.returncode == 0


def text_structure(path: str, text: str, extension: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "headings": [
            {"line": index, "text": line}
            for index, line in enumerate(text.splitlines(), start=1)
            if re.match(r"^#{1,6}\s+", line)
        ] if extension == "md" else [],
        "labels": re.findall(r"\\label\{([^}]+)\}", text) if extension == "tex" else [],
        "inputs": re.findall(r"\\(?:input|include)\{([^}]+)\}", text) if extension == "tex" else [],
        "graphics": re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text) if extension == "tex" else [],
        "citation_keys": sorted({
            key.strip()
            for group in re.findall(r"\\cite\w*\{([^}]+)\}", text)
            for key in group.split(",") if key.strip()
        }) if extension == "tex" else [],
    }
    if extension == "py":
        tree = ast.parse(text, filename=path)
        result["python_ast"] = {
            "functions": sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree)),
            "classes": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)),
            "imports": sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "asserts": sum(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        }
    return result


def source_authority(entry: dict[str, Any]) -> str:
    if entry["review_mode"] == "FULL_PDF":
        return "GENERATED_VISUAL_WITNESS"
    if entry["role"] == "result":
        return "PROCESS_OR_SNAPSHOT_SELF_REPORT"
    if entry["role"] == "test":
        return "INTERNAL_TEST_SURFACE"
    return "RELEASE_SURFACE_UNADJUDICATED"


def line_anchor(lines: list[str], token: str) -> dict[str, Any]:
    matches = [index for index, line in enumerate(lines, start=1) if token in line]
    return {"token": token, "line_start": matches[0] if matches else None, "line_end": matches[-1] if matches else None, "match_count": len(matches)}


def dedicated_absence_matches(sources: list[dict[str, Any]], q_id: str, kind: str) -> list[str]:
    q_token = q_id.lower()
    matches: list[str] = []
    for source in sources:
        path = source["path"]
        name = PurePosixPath(path).name.lower()
        if q_token not in name:
            continue
        if kind == "PLAN" and ("plan" in name or "/plans/" in path.lower()):
            matches.append(path)
        elif kind == "STEP_LOG" and "step" in name and "log" in name:
            matches.append(path)
        elif kind == "RESULT" and "result" in name and "snapshot" not in name:
            matches.append(path)
        elif kind == "SNAPSHOT" and "snapshot" in name:
            matches.append(path)
    return sorted(matches)


def build_phase057_observations(
    navigation_inputs: list[dict[str, Any]], navigation_lines: dict[str, list[str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for navigation in navigation_inputs:
        nav_id = navigation["navigation_id"]
        if nav_id == "P062-NAV-001":
            navigation["observation_ids"] = []
            continue
        lines = navigation_lines[nav_id]
        headings: list[tuple[int, re.Match[str]]] = []
        for line_number, line in enumerate(lines, start=1):
            match = PHASE057_OBSERVATION_RE.match(line)
            if match:
                headings.append((line_number, match))
        observation_ids: list[str] = []
        for position, (line_start, match) in enumerate(headings):
            line_end = headings[position + 1][0] - 1 if position + 1 < len(headings) else len(lines)
            observation_id = match.group(1)
            observation_ids.append(observation_id)
            section_bytes = ("\n".join(lines[line_start - 1:line_end]) + "\n").encode("utf-8")
            is_0095 = observation_id == "INTENT-PROV-0095"
            is_0086 = observation_id == "INTENT-PROV-0086"
            rows.append({
                "observation_id": observation_id,
                "source_path": navigation["path"],
                "source_blob_sha1": navigation["blob_sha1"],
                "source_sha256": navigation["sha256"],
                "line_start": line_start,
                "line_end": line_end,
                "heading": match.group(3),
                "section_sha256": sha256(section_bytes),
                "reproduction_state": "PROVISIONAL_ADVICE_NOT_ADOPTED" if is_0095 else "REPRODUCED_WITH_AUTHORITY_BOUNDARY",
                "contradiction_state": "BYTE_INVARIANCE_LIMITATION_REPRODUCED" if is_0086 else "NONE_FOUND_WITHIN_FROZEN_INTERNAL_TOPOLOGY",
                "unverified": ["external scientific, material, experimental, DOI, runtime and build truth"],
                "disposition_adoption_state": "NOT_ADOPTED" if is_0095 else "NOT_APPLICABLE",
                "authority_class": "PROVISIONAL_NAVIGATION_ONLY",
            })
        navigation["observation_ids"] = observation_ids
    if [row["observation_id"] for row in rows] != PHASE057_OBSERVATION_IDS:
        raise ValueError("Phase057 exact observation sequence mismatch")
    return rows


def build_process_artifacts(
    sources: list[dict[str, Any]], supplemental_lines: list[str], q1_record: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_by_path = {row["path"]: row for row in sources}
    rows: list[dict[str, Any]] = []
    gnf: list[dict[str, Any]] = []

    for process_id, kind, path in PROCESS_DOCUMENTS:
        source = source_by_path[path]
        commits = PROCESS_DOCUMENT_COMMITS[kind]
        created_mode, created_blob, _ = git_blob(commits["created"], path)
        last_mode, last_blob, _ = git_blob(commits["last_modified"], path)
        if created_mode != source["git_mode"] or last_mode != source["git_mode"]:
            raise ValueError(f"process document mode chronology mismatch: {path}")
        if last_blob != source["blob_sha1"]:
            raise ValueError(f"process document last-modified blob mismatch: {path}")
        chronology_state = "DOWNSTREAM_AUTHORED" if commits["last_modified"] == SUPPORTING_COMMITS[-1][1] else "CONTEMPORANEOUS"
        rows.append({
            "process_artifact_id": process_id, "q_id": "CROSS_PHASE", "artifact_kind": kind,
            "expected_by_anchor": None, "path": path, "blob_sha1": source["blob_sha1"],
            "commit": commits["last_modified"], "authored_commit": commits["last_modified"],
            "created_commit": commits["created"], "created_blob_sha1": created_blob,
            "last_modified_commit": commits["last_modified"],
            "observed_at_commit": BASELINE, "existence_state": "PRESENT",
            "chronology_state": chronology_state,
            "authority_class": "INTERNAL_SUBSTITUTE_CLOSURE" if kind in {"HANDOVER", "EXECUTION_LEDGER"} and chronology_state == "DOWNSTREAM_AUTHORED" else "PROCESS_EVIDENCE",
            "source_anchors": [], "external_scientific_truth_validated": False,
            "external_material_truth_validated": False,
        })

    q1_anchor = line_anchor(supplemental_lines, "| Q1 |")
    rows.append({
        "process_artifact_id": "P062-PROC-Q1-PARTIAL-REPORT", "q_id": "Q1",
        "artifact_kind": "PARTIAL_REPORT", "expected_by_anchor": {"path": SUPPLEMENTAL_PATH, **q1_anchor},
        "path": q1_record["path"], "blob_sha1": q1_record["blob_sha1"],
        "commit": q1_record["origin_commit"], "authored_commit": q1_record["origin_commit"],
        "observed_at_commit": BASELINE,
        "existence_state": "PARTIAL_CONFLICT", "chronology_state": "CONFLICTING",
        "authority_class": "PROCESS_EVIDENCE",
        "source_anchors": q1_record["section_anchors"],
        "external_scientific_truth_validated": False, "external_material_truth_validated": False,
    })

    for q_id in PROCESS_PHASES:
        anchor_token = f"| {q_id.replace('NAV', '').replace('B', '')} |" if q_id in {"Q5NAV", "Q5B"} else f"| {q_id} |"
        expected_anchor = {"path": SUPPLEMENTAL_PATH, **line_anchor(supplemental_lines, anchor_token)}
        for kind in ("PLAN", "STEP_LOG", "RESULT"):
            if q_id in {"Q5NAV", "Q5B"}:
                continue
            matches = dedicated_absence_matches(sources, q_id, kind)
            if matches:
                raise ValueError(f"dedicated {q_id} {kind} absence search found candidates: {matches}")
            row = {
                "process_artifact_id": f"P062-PROC-{q_id}-{kind}", "q_id": q_id,
                "artifact_kind": kind, "expected_by_anchor": expected_anchor,
                "path": None, "blob_sha1": None, "commit": None,
                "existence_state": "GROUND_NOT_FOUND", "chronology_state": "NOT_APPLICABLE",
                "authority_class": "GROUND_NOT_FOUND", "source_anchors": [],
                "external_scientific_truth_validated": False, "external_material_truth_validated": False,
            }
            rows.append(row)
            gnf.append({
                "ground_id": f"P062-GNF-{q_id}-{kind}", "kind": kind, "q_id": q_id,
                "expected_by_anchor": expected_anchor,
                "search_space": "DERIVED_EXACT_68_RELEASE_PATHS",
                "search_rule": "q-id token plus dedicated artifact-kind token; snapshots and global ledgers excluded",
                "matches": matches,
                "supplemental_checked_as_master_plan_not_dedicated": True,
            })

        snapshot_path = SNAPSHOT_PATHS[q_id]
        if snapshot_path is None:
            snapshot_matches = dedicated_absence_matches(sources, q_id, "SNAPSHOT")
            if snapshot_matches:
                raise ValueError(f"dedicated {q_id} SNAPSHOT absence search found candidates: {snapshot_matches}")
            row = {
                "process_artifact_id": f"P062-PROC-{q_id}-SNAPSHOT", "q_id": q_id,
                "artifact_kind": "SNAPSHOT", "expected_by_anchor": expected_anchor,
                "path": None, "blob_sha1": None, "commit": None,
                "existence_state": "GROUND_NOT_FOUND", "chronology_state": "NOT_APPLICABLE",
                "authority_class": "GROUND_NOT_FOUND", "source_anchors": [],
                "external_scientific_truth_validated": False, "external_material_truth_validated": False,
            }
            gnf.append({
                "ground_id": f"P062-GNF-{q_id}-SNAPSHOT", "kind": "SNAPSHOT", "q_id": q_id,
                "expected_by_anchor": expected_anchor, "search_space": "EXACT_68_RELEASE_PATHS",
                "search_rule": "q-id token plus snapshot token", "matches": snapshot_matches,
                "supplemental_checked_as_master_plan_not_dedicated": True,
            })
        else:
            source = source_by_path[snapshot_path]
            row = {
                "process_artifact_id": f"P062-PROC-{q_id}-SNAPSHOT", "q_id": q_id,
                "artifact_kind": "SNAPSHOT", "expected_by_anchor": expected_anchor,
                "path": snapshot_path, "blob_sha1": source["blob_sha1"],
                "commit": SNAPSHOT_AUTHORED_COMMITS[q_id], "authored_commit": SNAPSHOT_AUTHORED_COMMITS[q_id],
                "observed_at_commit": BASELINE,
                "existence_state": "PRESENT", "chronology_state": "CONTEMPORANEOUS",
                "authority_class": "PROCESS_EVIDENCE", "source_anchors": [],
                "external_scientific_truth_validated": False, "external_material_truth_validated": False,
            }
        rows.append(row)

    handover = source_by_path["Claude/docs/v1.0.21/HANDOVER_v1.0.21.md"]
    for q_id in ("Q9", "Q10"):
        rows.append({
            "process_artifact_id": f"P062-PROC-{q_id}-DOWNSTREAM-CLOSURE", "q_id": q_id,
            "artifact_kind": "DOWNSTREAM_CLOSURE", "expected_by_anchor": None,
            "path": handover["path"], "blob_sha1": handover["blob_sha1"],
            "commit": SUPPORTING_COMMITS[-1][1], "authored_commit": SUPPORTING_COMMITS[-1][1],
            "observed_at_commit": BASELINE, "existence_state": "PRESENT",
            "chronology_state": "DOWNSTREAM_AUTHORED", "authority_class": "INTERNAL_SUBSTITUTE_CLOSURE",
            "source_anchors": [], "external_scientific_truth_validated": False,
            "external_material_truth_validated": False,
        })
    return rows, gnf


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_bytes = normalize_lf(MANIFEST.read_bytes())
    manifest, manifest_traversal = strict_json_bytes(manifest_bytes)
    if sha256(manifest_bytes) != EXPECTED_MANIFEST_NORMALIZED_SHA256:
        raise ValueError("manifest normalized SHA mismatch")
    if manifest.get("baseline_commit") != BASELINE:
        raise ValueError("manifest baseline mismatch")
    selected = [(index, row) for index, row in enumerate(manifest["entries"], start=1) if row.get("version") == "v1.0.21"]
    if len(selected) != 68 or [index for index, _ in selected] != list(range(472, 540)):
        raise ValueError("v1.0.21 denominator mismatch")
    previous = {
        row["path"].replace("Claude/docs/v1.0.20/", "", 1): row
        for row in manifest["entries"]
        if row.get("version") == "v1.0.20" and row["path"].startswith("Claude/docs/v1.0.20/")
    }
    sources: list[dict[str, Any]] = []
    release_text_records: list[dict[str, Any]] = []
    pdf_records: list[dict[str, Any]] = []
    snapshot_records: list[dict[str, Any]] = []
    same_relative: list[dict[str, Any]] = []
    blob_paths: dict[str, list[str]] = defaultdict(list)
    partition_actual: dict[str, Counter[str]] = defaultdict(Counter)

    for release_index, (manifest_index, entry) in enumerate(selected, start=1):
        mode, blob, data = git_blob(BASELINE, entry["path"])
        if mode != entry["git_mode"] or blob != entry["blob_sha"] or len(data) != entry["size_bytes"]:
            raise ValueError(f"Git identity mismatch: {entry['path']}")
        relative = entry["path"].replace("Claude/docs/v1.0.21/", "", 1)
        old = previous.get(relative)
        pair_state = "NO_COUNTERPART" if old is None else "IDENTICAL" if old["blob_sha"] == blob else "CHANGED"
        source = {
            "source_id": f"P062-SRC-{release_index:04d}", "release_occurrence_index": release_index,
            "manifest_index": manifest_index, "path": entry["path"], "basename": PurePosixPath(entry["path"]).name,
            "blob_sha1": blob, "sha256": sha256(data), "git_mode": mode, "size_bytes": len(data),
            "extension": entry["extension"], "role": entry["role"], "review_mode": entry["review_mode"],
            "manifest_extent": entry["extent"], "dedup_group": entry["dedup_group"],
            "authority_class": source_authority(entry), "denominator": "V1021_RELEASE_68",
            "v1020_comparison": {
                "state": pair_state, "path": old["path"] if old else None,
                "blob_sha1": old["blob_sha"] if old else None,
            },
            "external_scientific_truth_validated": False, "external_material_truth_validated": False,
        }
        sources.append(source)
        blob_paths[blob].append(entry["path"])
        if old is not None:
            same_relative.append({
                "relative_path": relative, "v1020_path": old["path"], "v1020_blob_sha1": old["blob_sha"],
                "v1021_path": entry["path"], "v1021_blob_sha1": blob, "blob_relation": pair_state,
            })

        partition_id = "A_RELEASE_ROOT_AND_PDF" if release_index <= 54 else "B_RELEASE_PROCESS_AND_SNAPSHOTS"
        partition_actual[partition_id]["paths"] += 1
        if entry["review_mode"] == "FULL_TEXT":
            text, lines = strict_utf8_lf(data, entry["path"])
            if len(lines) != entry["extent"]["lines"]:
                raise ValueError(f"line extent mismatch: {entry['path']}")
            strict_stats = None
            if entry["extension"] == "json":
                _, strict_stats = strict_json_bytes(data)
            source["extent"] = {
                "lines": len(lines),
                "nonblank_lines": sum(bool(line.strip()) for line in lines),
                "pages": 0,
                "bytes": len(data),
            }
            source["read_state"] = "READ_FULL"
            human_state = "READ_FULL" if HUMAN_REVIEW_PARTITIONS[partition_id]["status"] == "PASS_HUMAN_FULL_REVIEW" else "PENDING_HUMAN_REVIEW"
            record = {
                "source_id": source["source_id"], "path": entry["path"], "blob_sha1": blob,
                "sha256": sha256(data), "bytes": len(data), "encoding": "utf-8",
                "bom": False, "newline_style": "LF",
                "physical_lines": len(lines), "nonblank_lines": sum(bool(line.strip()) for line in lines),
                "machine_read_state": "MACHINE_READ_FULL", "human_read_state": human_state,
                "review_evidence_id": HUMAN_REVIEW_PARTITIONS[partition_id]["review_evidence"]["evidence_id"],
                "strict_json_traversal": strict_stats,
                "structure": text_structure(entry["path"], text, entry["extension"]),
            }
            release_text_records.append(record)
            partition_actual[partition_id]["text"] += 1
            if strict_stats is not None:
                partition_actual[partition_id]["snapshots"] += 1
                snapshot_records.append({
                    "source_id": source["source_id"], "path": entry["path"], "blob_sha1": blob,
                    "raw_sha256": sha256(data), "physical_lines": len(lines),
                    "strict_json_traversal": strict_stats, "parse_state": "STRICT_FULL_TRAVERSAL",
                    "authority_class": "PROCESS_EVIDENCE_NOT_SCIENTIFIC_TRUTH",
                })
        elif entry["review_mode"] == "FULL_PDF":
            reader = PdfReader(io.BytesIO(data), strict=True)
            if reader.is_encrypted:
                raise ValueError(f"encrypted PDF cannot satisfy visual coverage: {entry['path']}")
            visual_state = "VISUAL_FULL" if HUMAN_REVIEW_PARTITIONS[partition_id]["status"] == "PASS_HUMAN_FULL_REVIEW" else "PENDING_VISUAL_REVIEW"
            pages = []
            for page_number, page in enumerate(reader.pages, start=1):
                pages.append({
                    "page": page_number, "width_points": float(page.mediabox.width),
                    "height_points": float(page.mediabox.height),
                    "visual_state": visual_state,
                    "review_evidence_id": "P062-REVIEW-A-RELEASE-PDF-214",
                    "source_sha256": sha256(data),
                })
            if len(pages) != entry["extent"]["pages"]:
                raise ValueError(f"PDF extent mismatch: {entry['path']}")
            source["extent"] = {
                "lines": 0,
                "nonblank_lines": 0,
                "pages": len(pages),
                "bytes": len(data),
            }
            source["read_state"] = "VISUAL_FULL"
            pdf_records.append({
                "source_id": source["source_id"], "path": entry["path"], "blob_sha1": blob,
                "sha256": sha256(data), "bytes": len(data), "pages_expected": entry["extent"]["pages"],
                "pages_observed": len(pages), "encrypted": bool(reader.is_encrypted),
                "machine_read_state": "MACHINE_METADATA_FULL", "visual_review_state": visual_state,
                "visual_review_method": "POPPLER_120_DPI_FULL_PAGE",
                "review_evidence_id": "P062-REVIEW-A-RELEASE-PDF-214",
                "pages": pages,
            })
            partition_actual[partition_id]["pdf"] += 1
            partition_actual[partition_id]["pdf_pages"] += len(pages)
        else:
            raise ValueError(f"unexpected v1.0.21 review mode: {entry['review_mode']}")

    supplemental_mode, supplemental_blob, supplemental_data = git_blob(BASELINE, SUPPLEMENTAL_PATH)
    supplemental_text, supplemental_lines = strict_utf8_lf(supplemental_data, SUPPLEMENTAL_PATH)
    if (supplemental_mode, supplemental_blob, len(supplemental_data), len(supplemental_lines)) != ("100644", SUPPLEMENTAL_BLOB, 10664, 76):
        raise ValueError("supplemental process-control identity mismatch")
    supplemental = {
        "process_id": "P062-PROC-SUP-001", "path": SUPPLEMENTAL_PATH, "manifest_member": False,
        "denominator": "SUPPLEMENTAL_PROCESS_CONTROL", "git_mode": supplemental_mode,
        "blob_sha1": supplemental_blob, "sha256": sha256(supplemental_data),
        "extent": {"bytes": len(supplemental_data), "lines": len(supplemental_lines), "nonblank_lines": sum(bool(line.strip()) for line in supplemental_lines)},
        "encoding": "utf-8", "bom": False, "newline_style": "LF",
        "authority_class": "RECORDED_SECOND_ORDER_REQUIREMENT",
        "first_order_user_transcript_state": "GROUND_NOT_FOUND",
        "machine_read_state": "MACHINE_READ_FULL", "human_read_state": "READ_FULL", "read_state": "READ_FULL",
        "review_evidence_id": "P062-REVIEW-C-SUPPLEMENTAL",
        "external_scientific_truth_validated": False, "external_material_truth_validated": False,
    }
    partition_actual["C_SUPPLEMENTAL_PROCESS_CONTROL"].update({"paths": 1, "text": 1})

    q1_mode, q1_blob, q1_data = git_blob(BASELINE, Q1_REPORT_PATH)
    origin_mode, origin_blob, origin_data = git_blob(Q1_REPORT_ORIGIN_COMMIT, Q1_REPORT_PATH)
    q1_text, q1_lines = strict_utf8_lf(q1_data, Q1_REPORT_PATH)
    if (q1_mode, q1_blob, len(q1_data), len(q1_lines)) != ("100644", Q1_REPORT_BLOB, 44969, 291):
        raise ValueError("Q1 comparison report identity mismatch")
    if (origin_mode, origin_blob, origin_data) != (q1_mode, q1_blob, q1_data):
        raise ValueError("Q1 comparison report origin mismatch")
    section_anchors = [
        {"line": index, "heading": line}
        for index, line in enumerate(q1_lines, start=1)
        if re.match(r"^## §[1-8]\.", line)
    ]
    q1_record = {
        "comparison_id": "P062-COMP-Q1-001", "path": Q1_REPORT_PATH,
        "manifest_member": False, "supplemental_member": False,
        "denominator": "Q1_COMPARISON_PROCESS_EVIDENCE", "git_mode": q1_mode,
        "blob_sha1": q1_blob, "sha256": sha256(q1_data),
        "origin_commit": Q1_REPORT_ORIGIN_COMMIT,
        "extent": {"bytes": len(q1_data), "lines": len(q1_lines), "nonblank_lines": sum(bool(line.strip()) for line in q1_lines)},
        "encoding": "utf-8", "bom": False, "newline_style": "LF",
        "section_anchors": section_anchors, "existence_state": "PARTIAL_CONFLICT",
        "chronology_state": "CONFLICTING", "authority_class": "PROCESS_EVIDENCE",
        "machine_read_state": "MACHINE_READ_FULL", "human_read_state": "READ_FULL", "read_state": "READ_FULL",
        "review_evidence_id": "P062-REVIEW-D-Q1-COMPARISON",
        "external_scientific_truth_validated": False, "external_material_truth_validated": False,
    }
    q1_record["chronology_conflict_anchors"] = {
        "report_complete": {"path": Q1_REPORT_PATH, **line_anchor(q1_lines, "## REPORT COMPLETE")},
        "master_plan_incomplete": {"path": SUPPLEMENTAL_PATH, **line_anchor(supplemental_lines, "§7~§8 미완")},
        "origin_commit": Q1_REPORT_ORIGIN_COMMIT,
    }
    if q1_record["chronology_conflict_anchors"]["report_complete"]["match_count"] != 1:
        raise ValueError("Q1 REPORT COMPLETE anchor mismatch")
    if q1_record["chronology_conflict_anchors"]["master_plan_incomplete"]["match_count"] != 1:
        raise ValueError("Q1 master-plan incomplete anchor mismatch")
    partition_actual["D_Q1_COMPARISON_REPORT"].update({"paths": 1, "text": 1})

    process_artifacts, ground_not_found = build_process_artifacts(sources, supplemental_lines, q1_record)
    implementation_history = [commit_record(q_id, commit, "CONTEMPORANEOUS") for q_id, commit in IMPLEMENTATION_CHAIN]
    support_history = [commit_record(event, commit, SUPPORTING_CHRONOLOGY[event]) for event, commit in SUPPORTING_COMMITS]
    for index in range(1, len(implementation_history)):
        if implementation_history[index - 1]["commit"] not in implementation_history[index]["parents"]:
            raise ValueError(f"implementation history chain break at {implementation_history[index]['event']}")
    q0_commit = IMPLEMENTATION_CHAIN[0][1]
    q8_commit = IMPLEMENTATION_CHAIN[-1][1]
    downstream_commit = SUPPORTING_COMMITS[-1][1]
    ancestry_relationships = [
        {"relationship_id": "P062-HIST-ANCESTRY-001", "older": SUPPORTING_COMMITS[0][1], "newer": q0_commit, "state": "ANCESTOR"},
        {"relationship_id": "P062-HIST-ANCESTRY-002", "older": Q1_REPORT_ORIGIN_COMMIT, "newer": q0_commit, "state": "ANCESTOR"},
        {"relationship_id": "P062-HIST-ANCESTRY-003", "older": q8_commit, "newer": downstream_commit, "state": "ANCESTOR"},
    ]
    for relationship in ancestry_relationships:
        if not is_ancestor(relationship["older"], relationship["newer"]):
            raise ValueError(f"supporting chronology break: {relationship['relationship_id']}")
    for event, commit in SUPPORTING_COMMITS:
        if not is_ancestor(commit, BASELINE):
            raise ValueError(f"supporting commit outside frozen baseline lineage: {event}")
    q1_origin_history = next(row for row in support_history if row["event"] == "Q1_PARTIAL_REPORT_ORIGIN")
    if Q1_REPORT_PATH not in q1_origin_history["changed_paths"]:
        raise ValueError("Q1 origin patch does not author comparison report")
    _, q1_origin_blob, _ = git_blob(Q1_REPORT_ORIGIN_COMMIT, Q1_REPORT_PATH)
    if q1_origin_blob != Q1_REPORT_BLOB:
        raise ValueError("Q1 origin authored blob mismatch")

    navigation_inputs = []
    navigation_lines: dict[str, list[str]] = {}
    for nav_id, path, expected_lines in PHASE057_INPUTS:
        mode, blob, data = git_blob(ACTIVATION_COMMIT, path)
        _, lines = strict_utf8_lf(data, path)
        if len(lines) != expected_lines:
            raise ValueError(f"Phase057 input extent mismatch: {path}")
        reproduction = PHASE057_REPRODUCTIONS[nav_id]
        navigation_lines[nav_id] = lines
        navigation_inputs.append({
            "navigation_id": nav_id, "path": path, "commit": ACTIVATION_COMMIT, "git_mode": mode,
            "blob_sha1": blob, "sha256": sha256(data), "physical_lines": len(lines),
            "nonblank_lines": sum(bool(line.strip()) for line in lines),
            "authority_class": "PROVISIONAL_NAVIGATION_ONLY", "reverification_state": reproduction["state"],
            "reverification_evidence": reproduction["evidence"],
            "unverified": ["external scientific, material, experimental, DOI, runtime and build truth"],
        })
    phase057_observations = build_phase057_observations(navigation_inputs, navigation_lines)

    partitions = []
    for partition_id, contract in HUMAN_REVIEW_PARTITIONS.items():
        actual = {
            key: partition_actual[partition_id].get(key, 0)
            for key in contract["expected"]
        }
        for key, expected in contract["expected"].items():
            if actual.get(key, 0) != expected:
                raise ValueError(f"partition mismatch {partition_id}:{key}")
        if partition_id == "A_RELEASE_ROOT_AND_PDF":
            covered = [
                {key: row[key] for key in ("source_id", "path", "blob_sha1", "sha256")}
                for row in sources if row["release_occurrence_index"] <= 54
            ]
        elif partition_id == "B_RELEASE_PROCESS_AND_SNAPSHOTS":
            covered = [
                {key: row[key] for key in ("source_id", "path", "blob_sha1", "sha256")}
                for row in sources if row["release_occurrence_index"] >= 55
            ]
        elif partition_id == "C_SUPPLEMENTAL_PROCESS_CONTROL":
            covered = [{key: supplemental[key] for key in ("path", "blob_sha1", "sha256")}]
        else:
            covered = [{key: q1_record[key] for key in ("path", "blob_sha1", "sha256")}]
        partition = {
            "partition_id": partition_id,
            **contract,
            "actual": actual,
            "covered_source_count": len(covered),
            "covered_source_set_sha256": sha256(canonical_bytes(covered)),
        }
        partition["review_contract_sha256"] = sha256(canonical_bytes(partition))
        partitions.append(partition)

    duplicates = [{"blob_sha1": blob, "paths": sorted(paths)} for blob, paths in sorted(blob_paths.items()) if len(paths) > 1]
    source_by_path = {row["path"]: row for row in sources}
    pdf_by_path = {row["path"]: row for row in pdf_records}
    pdf_source_relationships = []
    for relationship in PDF_SOURCE_RELATIONSHIPS:
        source = source_by_path[relationship["source_path"]]
        pdf = source_by_path[relationship["pdf_path"]]
        pdf_source_relationships.append({
            **relationship,
            "source_id": source["source_id"], "source_blob_sha1": source["blob_sha1"],
            "source_sha256": source["sha256"], "pdf_source_id": pdf["source_id"],
            "pdf_blob_sha1": pdf["blob_sha1"], "pdf_sha256": pdf["sha256"],
        })
    pdf_variant_relationships = []
    for relationship in PDF_VARIANT_RELATIONSHIPS:
        base = pdf_by_path[relationship["base_pdf_path"]]
        navigation = pdf_by_path[relationship["navigation_pdf_path"]]
        pdf_variant_relationships.append({
            **relationship,
            "base_source_id": base["source_id"], "base_blob_sha1": base["blob_sha1"],
            "base_sha256": base["sha256"], "navigation_source_id": navigation["source_id"],
            "navigation_blob_sha1": navigation["blob_sha1"], "navigation_sha256": navigation["sha256"],
        })
    topology = {
        "schema_version": 1, "generated_date": "2026-08-27", "phase": 62, "step": "52",
        "artifact_kind": "V1021_SOURCE_PROCESS_TOPOLOGY",
        "authority_boundary": "Source/process identity and chronology only; no scientific, material, experimental, runtime, adoption or primary-literature truth promotion.",
        "baseline_commit": BASELINE, "activation_commit": ACTIVATION_COMMIT,
        "manifest": {"path": MANIFEST.relative_to(REPO).as_posix(), "normalized_sha256": sha256(manifest_bytes), "traversal": manifest_traversal},
        "builder": {"path": BUILDER.relative_to(REPO).as_posix(), "normalized_sha256": sha256(normalize_lf(BUILDER.read_bytes()))},
        "denominator_policy": {
            "release": "V1021_RELEASE_68", "supplemental": "SUPPLEMENTAL_PROCESS_CONTROL",
            "q1_comparison": "Q1_COMPARISON_PROCESS_EVIDENCE", "fusion_allowed": False,
        },
        "counts": {
            "release_occurrences": len(sources), "release_unique_paths": len({row["path"] for row in sources}),
            "release_unique_blobs": len(blob_paths), "release_bytes": sum(row["size_bytes"] for row in sources),
            "release_text_files": len(release_text_records),
            "release_text_physical_lines": sum(row["physical_lines"] for row in release_text_records),
            "release_text_nonblank_lines": sum(row["nonblank_lines"] for row in release_text_records),
            "release_pdf_files": len(pdf_records), "release_pdf_pages": sum(row["pages_observed"] for row in pdf_records),
            "release_snapshot_files": len(snapshot_records),
            "shared_v1020_blob_identities": sum(row["v1020_comparison"]["state"] == "IDENTICAL" for row in sources),
            "same_relative_pairs": len(same_relative),
            "same_relative_identical": sum(row["blob_relation"] == "IDENTICAL" for row in same_relative),
            "same_relative_changed": sum(row["blob_relation"] == "CHANGED" for row in same_relative),
            "same_relative_no_counterpart": sum(row["v1020_comparison"]["state"] == "NO_COUNTERPART" for row in sources),
            "supplemental_occurrences": 1, "q1_comparison_occurrences": 1,
            "implementation_chain_commits": len(implementation_history), "supporting_history_commits": len(support_history),
            "process_artifact_rows": len(process_artifacts), "ground_not_found_rows": len(ground_not_found),
            "phase057_navigation_inputs": len(navigation_inputs), "phase057_navigation_lines": sum(row["physical_lines"] for row in navigation_inputs),
            "phase057_observation_rows": len(phase057_observations),
        },
        "path_set_sha256": sha256(("\n".join(sorted(row["path"] for row in sources)) + "\n").encode("utf-8")),
        "path_blob_set_sha256": sha256(("\n".join(f"{row['path']}\t{row['blob_sha1']}" for row in sorted(sources, key=lambda item: item["path"])) + "\n").encode("utf-8")),
        "review_mode_counts": dict(sorted(Counter(row["review_mode"] for row in sources).items())),
        "role_counts": dict(sorted(Counter(row["role"] for row in sources).items())),
        "extension_counts": dict(sorted(Counter(row["extension"] for row in sources).items())),
        "duplicates": duplicates, "same_relative_v1020_v1021": same_relative,
        "pdf_source_relationships": pdf_source_relationships,
        "sources": sources, "supplemental_process_control": supplemental,
        "q1_comparison_report": q1_record, "process_artifacts": process_artifacts,
        "process_aliases": PROCESS_ALIASES,
        "history": {
            "implementation_chain": implementation_history,
            "supporting_commits": support_history,
            "ancestry_relationships": ancestry_relationships,
        },
        "phase057_navigation_inputs": navigation_inputs,
        "phase057_observations": phase057_observations,
        "phase057_observation_id_sha256": sha256(("\n".join(PHASE057_OBSERVATION_IDS) + "\n").encode("utf-8")),
        "ground_not_found": ground_not_found,
        "status": "PASS_SOURCE_PROCESS_IDENTITY_TOPOLOGY",
    }

    all_human = all(row["status"] == "PASS_HUMAN_FULL_REVIEW" for row in partitions)
    attestation = {
        "schema_version": 1, "generated_date": "2026-08-27", "phase": 62, "step": "52",
        "artifact_kind": "V1021_READ_ATTESTATION",
        "authority_boundary": "Machine reads and human coverage only; snapshots, PDFs, process documents and observations do not establish scientific or material truth.",
        "baseline_commit": BASELINE, "source_topology_semantic_sha256": sha256(canonical_bytes(topology)),
        "counts": {
            "release_text_files": len(release_text_records),
            "release_text_physical_lines": sum(row["physical_lines"] for row in release_text_records),
            "release_text_nonblank_lines": sum(row["nonblank_lines"] for row in release_text_records),
            "release_pdf_files": len(pdf_records), "release_pdf_pages": sum(row["pages_observed"] for row in pdf_records),
            "snapshot_files": len(snapshot_records),
            "snapshot_nodes": sum(row["strict_json_traversal"]["nodes"] for row in snapshot_records),
            "snapshot_mapping_keys": sum(row["strict_json_traversal"]["mapping_keys"] for row in snapshot_records),
            "snapshot_traversal_items": sum(
                row["strict_json_traversal"]["nodes"] + row["strict_json_traversal"]["mapping_keys"]
                for row in snapshot_records
            ),
            "supplemental_files": 1, "supplemental_physical_lines": supplemental["extent"]["lines"],
            "q1_comparison_files": 1, "q1_comparison_physical_lines": q1_record["extent"]["lines"],
            "human_partitions_complete": sum(row["status"] == "PASS_HUMAN_FULL_REVIEW" for row in partitions),
            "human_partitions_total": len(partitions),
        },
        "partitions": partitions, "release_text_records": release_text_records,
        "pdf_records": pdf_records, "snapshot_records": snapshot_records,
        "pdf_variant_relationships": pdf_variant_relationships,
        "supplemental_text_record": supplemental, "q1_comparison_text_record": q1_record,
        "human_review_contract_sha256": sha256(canonical_bytes(partitions)),
        "status": "PASS_FULL_READ_ATTESTATION" if all_human else "PENDING_HUMAN_REVIEW",
    }
    return topology, attestation


def output_paths(output_dir: str | None) -> tuple[Path, Path]:
    if output_dir is None:
        return TOPOLOGY, ATTESTATION
    root = Path(output_dir).resolve()
    return root / TOPOLOGY.name, root / ATTESTATION.name


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    first_topology, first_attestation = build()
    if args.determinism_check:
        second_topology, second_attestation = build()
        if canonical_bytes(first_topology) != canonical_bytes(second_topology):
            print("FAIL STEP52_TOPOLOGY_NONDETERMINISTIC")
            return 1
        if canonical_bytes(first_attestation) != canonical_bytes(second_attestation):
            print("FAIL STEP52_ATTESTATION_NONDETERMINISTIC")
            return 1
    if not args.check_only:
        topology_path, attestation_path = output_paths(args.output_dir)
        topology_path.parent.mkdir(parents=True, exist_ok=True)
        topology_path.write_bytes(pretty_bytes(first_topology))
        attestation_path.write_bytes(pretty_bytes(first_attestation))
    print(
        "BUILT_P062_STEP52 "
        f"release={first_topology['counts']['release_occurrences']} "
        f"text={first_attestation['counts']['release_text_files']}/{first_attestation['counts']['release_text_physical_lines']} "
        f"pdf={first_attestation['counts']['release_pdf_files']}/{first_attestation['counts']['release_pdf_pages']} "
        f"snapshots={first_attestation['counts']['snapshot_files']}/{first_attestation['counts']['snapshot_nodes']} "
        f"human={first_attestation['counts']['human_partitions_complete']}/{first_attestation['counts']['human_partitions_total']}"
    )
    if args.determinism_check:
        print("PASS_P062_STEP52_BUILDER_DETERMINISM 2/2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
