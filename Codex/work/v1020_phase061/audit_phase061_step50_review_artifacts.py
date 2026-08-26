#!/usr/bin/env python3
"""Build Phase 061 Step 50 review/artifact and visual-read evidence.

The builder reads only frozen Git blobs and persisted Codex audit inputs.  It
does not import or execute the historical production, test, renderer, or TeX
sources.  Human visual observations are deliberately bounded to appearance;
they never imply numerical, material, experimental, or literature validity.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any


REPO = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
DATE = "2026-08-26"

TOPOLOGY_PATH = REPO / "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
READ_PATH = REPO / "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json"
PROCESS_PATH = REPO / "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json"
LINEAGE_PATH = REPO / "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json"
CITATION_PATH = REPO / "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json"
MATRIX_PATH = REPO / "Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json"
VISUAL_PATH = REPO / "Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json"

PROCESS_REVIEW_INDICES = (3, 54, 62, 68, 77, 85, 86)

FIGURE_FORWARD_SELECTIONS: dict[str, dict[str, str]] = {
    "FF1-1": {"cluster": "C-B", "role": "BASE", "grade": "A"},
    "FF1-2": {"cluster": "C-F", "role": "ALTERNATE", "grade": "B"},
    "FF1-3": {"cluster": "C-A", "role": "ALTERNATE", "grade": "A"},
    "FF1-4": {"cluster": "C-J", "role": "BASE", "grade": "B"},
    "FF1-5": {"cluster": "C-K", "role": "BASE", "grade": "B"},
    "FF1-6": {"cluster": "C-D", "role": "GRAFT", "grade": "A"},
    "FF1-7": {"cluster": "C-H", "role": "OPTIONAL_GRAFT", "grade": "B"},
    "FF2-1": {"cluster": "C-A", "role": "BASE", "grade": "A"},
    "FF2-2": {"cluster": "C-B", "role": "GRAFT", "grade": "A"},
    "FF2-3": {"cluster": "C-G", "role": "BASE", "grade": "B"},
    "FF2-4": {"cluster": "C-I", "role": "BASE", "grade": "B"},
    "FF2-5": {"cluster": "C-D", "role": "BASE", "grade": "A"},
    "FF3-1": {"cluster": "C-A", "role": "GRAFT", "grade": "A"},
    "FF3-2": {"cluster": "C-F", "role": "BASE", "grade": "B"},
    "FF3-3": {"cluster": "C-E", "role": "BASE", "grade": "A"},
    "FF3-4": {"cluster": "C-H", "role": "BASE", "grade": "B"},
    "FF3-5": {"cluster": "C-B", "role": "ALTERNATE", "grade": "A"},
    "FF3-6": {"cluster": "C-D", "role": "ALTERNATE", "grade": "A"},
    "FF3-7": {"cluster": "C-K", "role": "ALTERNATE", "grade": "B"},
    "FO1-1": {"cluster": "C-C", "role": "ALTERNATE", "grade": "A"},
    "FO1-2": {"cluster": "C-G", "role": "ALTERNATE", "grade": "B"},
    "FO1-3": {"cluster": "C-A", "role": "ALTERNATE", "grade": "A"},
    "FO1-4": {"cluster": "C-D", "role": "ALTERNATE", "grade": "A"},
    "FO2-1": {"cluster": "C-A", "role": "GRAFT", "grade": "A"},
    "FO2-2": {"cluster": "C-C", "role": "GRAFT", "grade": "A"},
    "FO2-3": {"cluster": "C-D", "role": "ALTERNATE", "grade": "A"},
    "FO2-4": {"cluster": "C-D", "role": "GRAFT", "grade": "A"},
    "FO3-1": {"cluster": "C-E", "role": "GRAFT", "grade": "A"},
    "FO3-2": {"cluster": "C-A", "role": "ALTERNATE", "grade": "A"},
    "FO3-3": {"cluster": "C-L", "role": "BASE_OPTIONAL", "grade": "C"},
    "FO3-4": {"cluster": "C-C", "role": "BASE", "grade": "A"},
}

# Candidate-specific provenance adjudication.  Family-level files are never
# promoted to a direct candidate edge merely because they share a directory.
FIGURE_PROVENANCE_STATES: dict[str, dict[str, str]] = {
    **{
        f"FF1-{number}": {"data": "UNVERIFIED", "generation": "UNVERIFIED", "route": "P061-STEP50-GNF-007"}
        for number in range(1, 8)
    },
    **{
        f"FF2-{number}": {"data": "GNF", "generation": "UNVERIFIED", "route": "P061-STEP50-GNF-005"}
        for number in range(1, 6)
    },
    **{
        f"FF3-{number}": {"data": "UNVERIFIED", "generation": "UNVERIFIED", "route": "P061-STEP50-GNF-007"}
        for number in range(1, 8)
    },
    **{
        f"FO1-{number}": {"data": "GNF", "generation": "GNF", "route": "P061-STEP50-GNF-007"}
        for number in range(1, 5)
    },
    **{
        f"FO2-{number}": {"data": "GNF", "generation": "GNF", "route": "P061-STEP50-GNF-007"}
        for number in range(1, 5)
    },
    **{
        f"FO3-{number}": {"data": "PARTIAL", "generation": "PARTIAL", "route": "P061-STEP50-GNF-007"}
        for number in range(1, 5)
    },
}
FIGURE_PROVENANCE_STATES["FF1-2"] = {
    "data": "PARTIAL", "generation": "PARTIAL", "route": "P061-STEP50-GNF-003",
}
FIGURE_PROVENANCE_STATES["FF3-2"] = {
    "data": "PARTIAL", "generation": "PARTIAL", "route": "P061-STEP50-GNF-006",
}
FIGURE_PROVENANCE_STATES["FF3-7"] = {
    "data": "CONTRADICTED", "generation": "CONTRADICTED", "route": "P061-STEP50-GNF-007",
}

CONTENT_ADOPTION_SPECS = (
    ("P2-F1", 97, 96, 10, "BASE"),
    ("P2-O1", 98, 96, 10, "GRAFT"),
    ("P2-O2", 99, 96, 10, "GRAFT"),
    ("P2-O3", 100, 96, 10, "GRAFT"),
    ("P4-F1", 103, 102, 24, "GRAFT"),
    ("P4-F3", 104, 102, 24, "BASE"),
    ("P4-O3", 107, 102, 24, "GRAFT"),
)

TRIAGE_TARGETS = {
    "T-01": (10, "254"), "T-02": (10, "149"),
    "T-03": (14, "196"), "T-04": (14, "106"),
    "T-05": (16, "51-54"), "T-06": (23, "70-73"),
    "T-07": (24, "240-241"), "T-08": (25, "57"),
    "T-09": (23, "47,54; plus P061-SRC-0005:100"),
    "T-10": (32, "20-22"), "T-11": (34, "129-131"),
    "T-12": (35, "16-17"), "T-13": (35, "90"),
    "T-14": (36, "61-62"),
    "T-15": (40, "46-47; plus P061-SRC-0029:B.4"),
    "T-16": (44, "398"), "T-17": (44, "3"),
    "T-18": (86, "C-019"),
}

# Page 1 of each FF1 harness is an explicit dummy scaffold.  The later
# competitive harness families visibly retain unresolved cross references.
FF1_DUMMY_PDFS = {
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF1/harness_app.pdf",
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF1/harness_ch1.pdf",
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF1/harness_ch2.pdf",
}
UNRESOLVED_REF_PDF_PREFIXES = (
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF2/",
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF3/",
    "Claude/docs/v1.0.20/results/comp_P7_figs/FO1/",
    "Claude/docs/v1.0.20/results/comp_P7_figs/FO2/",
    "Claude/docs/v1.0.20/results/comp_P7_figs/FO3/",
)
FF2_UNRESOLVED_MARKER_COUNTS = {
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF2/harness_ff2_ch1.pdf": {1: 5, 2: 10},
    "Claude/docs/v1.0.20/results/comp_P7_figs/FF2/harness_ff2_ch2.pdf": {1: 11, 2: 4},
}


class AuditError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise AuditError(f"nonfinite JSON constant: {value}")


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise AuditError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_pairs,
        parse_constant=reject_constant,
    )


def canonical_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def semantic_sha(obj: Any) -> str:
    return sha256_bytes(canonical_bytes(obj))


def write_json(path: Path, obj: Any) -> None:
    path.write_bytes(canonical_bytes(obj))


def git_cat_file_batch(paths: list[str]) -> dict[str, tuple[str, bytes]]:
    request = b"".join(f"{BASELINE}:{path}\n".encode("utf-8") for path in paths)
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=request,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if proc.returncode != 0:
        raise AuditError(proc.stderr.decode("utf-8", "replace"))
    out = proc.stdout
    pos = 0
    records: dict[str, tuple[str, bytes]] = {}
    for path in paths:
        end = out.find(b"\n", pos)
        if end < 0:
            raise AuditError(f"missing cat-file header for {path}")
        header = out[pos:end].decode("ascii", "strict")
        pos = end + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise AuditError(f"invalid cat-file header for {path}: {header}")
        size = int(parts[2])
        data = out[pos:pos + size]
        pos += size
        if out[pos:pos + 1] != b"\n":
            raise AuditError(f"missing cat-file terminator for {path}")
        pos += 1
        records[path] = (parts[0], data)
    if pos != len(out):
        raise AuditError("unexpected trailing cat-file output")
    return records


def text_extent(data: bytes) -> tuple[int, int]:
    text = data.decode("utf-8")
    lines = text.splitlines()
    return len(lines), sum(bool(line.strip()) for line in lines)


def source_family(path: str) -> str:
    for token in ("comp_P2_part0", "comp_P4_mitbg", "comp_P7_review", "comp_Q2_gcbalance", "comp_Q3_tst"):
        if f"/{token}/" in path:
            return token
    match = re.search(r"/comp_P7_figs/(FF[123]|FO[123])/", path)
    return match.group(1) if match else "PROCESS_OR_RELEASE"


def artifact_role(path: str, review_mode: str) -> str:
    name = PurePosixPath(path).name
    if review_mode == "FULL_PDF":
        return "RENDERED_PDF"
    if review_mode == "FULL_IMAGE":
        return "PIXEL_IMAGE"
    if name.startswith("FRAMING_") or name == "AUTHOR_BRIEF.md":
        return "COMPETITION_SPECIFICATION"
    if name in {"PICK_JUDGMENT.md", "FIGS_PICK_JUDGMENT.md"}:
        return "CONSOLIDATED_JUDGMENT"
    if name == "TRIAGE_P7.md":
        return "CONSOLIDATED_TRIAGE"
    if name.startswith("REVIEW_"):
        return "REVIEW_RECORD_OCCURRENCE"
    if name.startswith("NOTE_"):
        return "CANDIDATE_NOTE"
    if re.match(r"(?:draft_|fig_).+\.tex$", name):
        return "CANDIDATE_TEX"
    if "harness" in name.lower() and name.endswith(".tex"):
        return "RENDER_HARNESS"
    if name.endswith(".py"):
        return "GENERATION_OR_COORDINATE_RECORD"
    if name.endswith((".json", ".txt")):
        return "COORDINATE_OR_DATA_RECORD"
    if name.startswith(("PLAN_", "RESULT_", "STEP_LOG_")):
        return "PROCESS_RECORD"
    if name == "HANDOVER_v1.0.20.md":
        return "FINAL_HANDOVER_REFERENCE"
    return "TEXT_RECORD"


def figure_candidate_id(path: str) -> str | None:
    family_match = re.search(r"/comp_P7_figs/(FF[123]|FO[123])/", path)
    number_match = re.search(r"/fig_(?:ff|fo)[123]_([1-9])_", path.lower())
    if not family_match or not number_match:
        return None
    return f"{family_match.group(1)}-{number_match.group(1)}"


def source_ref(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": row["source_id"],
        "manifest_index": row["manifest_index_v1020"],
        "path": row["path"],
        "blob_sha1": row["blob_sha1"],
        "sha256": row["sha256"],
    }


def adopted_target_ref(row: dict[str, Any], anchor: str) -> dict[str, Any]:
    ref = source_ref(row)
    ref["anchor"] = anchor
    ref["authority_ceiling"] = "RELEASE_CONTENT_PRESENCE_ONLY"
    return ref


def parse_harness_inputs(text: str) -> list[str]:
    return [match.strip() for match in re.findall(r"\\input\{([^}]+)\}", text)]


def manual_image_observation(path: str) -> dict[str, Any]:
    defects: list[dict[str, str]] = []
    axes = "MIXED_OR_NOT_APPLICABLE"
    legends = "MIXED_OR_NOT_APPLICABLE"
    labels = "PRESENT"
    relation = "STANDALONE_GENERATED_ASSET_NO_ADOPTED_TEX_INCLUDE_EDGE"
    if path.endswith("P4_lco_heat_validation.png"):
        defects.append({"id": "VIS-P2-001", "finding": "subplot (c) long title is clipped at the right image boundary"})
        axes, legends = "PRESENT", "PRESENT"
    elif path.endswith("anode_fit_v1_0_14_dqdv.png"):
        defects.append({"id": "VIS-P2-002", "finding": "filename says v1.0.14 while the internal title says Anode Fit 1.0.16"})
        axes, legends = "PRESENT", "PRESENT"
    elif "/FF1/" in path:
        relation = "RASTER_RENDER_OR_CROP_OF_FF1_HARNESS_PAGE"
        axes, legends = "PRESENT_OR_PANEL_DEPENDENT", "PRESENT_OR_PANEL_DEPENDENT"
        if path.endswith("v_ch1_4crop.png"):
            defects.append({"id": "VIS-P2-003", "finding": "partial crop; not an independent complete candidate page"})
        if path.endswith("v_ch1_4top.png"):
            defects.append({"id": "VIS-P2-004", "finding": "intentional top crop; not an independent complete candidate page"})
    elif "/FF3/" in path or "/FO1/" in path:
        relation = "RASTER_RENDER_OF_COMPETITIVE_HARNESS_PAGE"
        axes, legends = "PRESENT_OR_PANEL_DEPENDENT", "PRESENT_OR_PANEL_DEPENDENT"
        defects.append({"id": "VIS-P2-005", "finding": "visible unresolved cross-reference marker(s) inherited from competitive harness"})
    elif "graph_suite_" in path:
        axes, legends = "PRESENT", "PRESENT"
        relation = "PACKAGE_VALIDATION_ASSET_NO_ADOPTED_TEX_INCLUDE_EDGE"
        defects.append({
            "id": "VIS-P2-008",
            "finding": "near-duplicate graph-suite occurrence; do not count version-label pixel changes as independent visual evidence",
        })
    return {
        "labels": labels,
        "axes": axes,
        "legends": legends,
        "caption_source_relationship": relation,
        "visible_defects": defects,
        "aesthetic_readability_state": "VISUALLY_REVIEWED_BOUNDED",
        "numeric_reproduction_state": "UNVERIFIED_BY_VISUAL_REVIEW",
        "material_validation_state": "UNVERIFIED",
        "experimental_evidence_state": "NOT_EVIDENCE",
    }


def manual_pdf_page_observation(path: str, page: int) -> dict[str, Any]:
    defects: list[dict[str, str]] = []
    page_role = "SCHOLARLY_RELEASE_PAGE" if "/results/comp_P7_figs/" not in path else "COMPETITIVE_HARNESS_PAGE"
    if path in FF1_DUMMY_PDFS and page == 1:
        defects.append({"id": "VIS-P2-006", "finding": "dummy scaffold page with zero/dummy placeholder content"})
        page_role = "DUMMY_SCAFFOLD_PAGE"
    if path.startswith(UNRESOLVED_REF_PDF_PREFIXES):
        defects.append({"id": "VIS-P2-007", "finding": "visible unresolved cross-reference marker(s)"})
    if path.endswith("FO1/_harness.pdf") and page == 2:
        defects.append({"id": "VIS-P2-009", "finding": "figure 4 electronic line and label slightly overlap but remain readable"})
    if path.endswith("FO3/_harness.pdf") and page == 1:
        defects.append({"id": "VIS-P2-010", "finding": "float ordering places the document title after a figure caption"})
    return {
        "page_role": page_role,
        "labels": "PRESENT_OR_NOT_APPLICABLE",
        "axes": "PRESENT_OR_NOT_APPLICABLE",
        "legends": "PRESENT_OR_NOT_APPLICABLE",
        "caption_source_relationship": (
            "ROOT_AND_SECTION_TEX_TO_GENERATED_RELEASE_PDF"
            if page_role == "SCHOLARLY_RELEASE_PAGE"
            else "HARNESS_INPUT_CANDIDATE_TO_COMPETITIVE_PDF_PAGE"
        ),
        "visible_defects": defects,
        "visible_unresolved_reference_markers": FF2_UNRESOLVED_MARKER_COUNTS.get(path, {}).get(page),
        "blank_page": False,
        "render_failure": False,
        "aesthetic_readability_state": "VISUALLY_REVIEWED_BOUNDED",
        "numeric_reproduction_state": "UNVERIFIED_BY_VISUAL_REVIEW",
        "material_validation_state": "UNVERIFIED",
        "experimental_evidence_state": "NOT_EVIDENCE",
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    topology = load_json(TOPOLOGY_PATH)
    read_att = load_json(READ_PATH)
    process = load_json(PROCESS_PATH)
    lineage = load_json(LINEAGE_PATH)
    citation = load_json(CITATION_PATH)
    baseline_by_input = {
        "topology": topology.get("baseline_commit"),
        "read": read_att.get("baseline_commit"),
        "process": process.get("baseline_commit"),
        "lineage": lineage.get("authority_boundary", {}).get("baseline_commit"),
        "citation": citation.get("baseline_commit"),
    }
    for name, value in baseline_by_input.items():
        if value != BASELINE:
            raise AuditError(f"{name} baseline mismatch")

    sources = topology["sources"]
    if len(sources) != 232:
        raise AuditError("topology source count mismatch")
    by_index = {row["manifest_index_v1020"]: row for row in sources}
    by_path = {row["path"]: row for row in sources}
    if len(by_index) != 232 or len(by_path) != 232:
        raise AuditError("source identity collision")

    competitive = [row for row in sources if 95 <= row["manifest_index_v1020"] <= 220]
    competitive_text = [row for row in competitive if row["review_mode"] == "FULL_TEXT"]
    process_review = [by_index[index] for index in PROCESS_REVIEW_INDICES]
    adopted = citation["source_coverage"]
    adopted_ids = {row["source_id"] for row in adopted}
    if len(adopted) != 43 or len(adopted_ids) != 43:
        raise AuditError("adopted source coverage mismatch")

    text_read_rows = sorted(
        {row["path"]: row for row in competitive_text + process_review}.values(),
        key=lambda row: row["manifest_index_v1020"],
    )
    prior_text_by_path = {row["path"]: row for row in read_att["text_records"]}
    visual_prior_rows = read_att["image_records"] + read_att["pdf_records"]
    blobs = git_cat_file_batch([row["path"] for row in text_read_rows + visual_prior_rows])
    full_read_records: list[dict[str, Any]] = []
    text_by_path: dict[str, str] = {}
    for row in text_read_rows:
        blob_sha1, data = blobs[row["path"]]
        if blob_sha1 != row["blob_sha1"] or sha256_bytes(data) != row["sha256"]:
            raise AuditError(f"frozen text identity mismatch: {row['path']}")
        physical, nonblank = text_extent(data)
        expected = row["manifest_extent"]
        prior_text = prior_text_by_path[row["path"]]
        if physical != expected["lines"] or physical != prior_text["physical_lines"] or nonblank != prior_text["nonblank_lines"]:
            raise AuditError(f"frozen text extent mismatch: {row['path']}")
        text = data.decode("utf-8")
        text_by_path[row["path"]] = text
        full_read_records.append({
            **source_ref(row),
            "reviewed_range": f"1-{physical}",
            "physical_lines": physical,
            "nonblank_lines": nonblank,
            "family": source_family(row["path"]),
            "artifact_role": artifact_role(row["path"], row["review_mode"]),
            "full_read_state": "FULL_TEXT_1_TO_EOF",
            "authority_ceiling": "FROZEN_INTERNAL_SOURCE_ONLY",
        })

    competitive_records: list[dict[str, Any]] = []
    for row in competitive:
        family = source_family(row["path"])
        role = artifact_role(row["path"], row["review_mode"])
        cid = figure_candidate_id(row["path"])
        adoption_state = "NOT_ADOPTED_V1020"
        if row["manifest_index_v1020"] in {97, 98, 99, 100, 103, 104, 107}:
            adoption_state = "CONTENT_PARTIALLY_ADOPTED_V1020_EXPLICIT_EDGE"
        elif family == "comp_P7_review":
            adoption_state = "INTERNAL_REVIEW_INPUT_OR_TRIAGE"
        elif family in {"comp_Q2_gcbalance", "comp_Q3_tst"}:
            adoption_state = "FORWARD_CANDIDATE_V1021_NOT_V1020"
        elif cid is not None:
            adoption_state = "FORWARD_SELECTED_OR_COMPETING_V1021_NOT_V1020"
        competitive_records.append({
            **source_ref(row),
            "family": family,
            "artifact_role": role,
            "figure_candidate_id": cid,
            "v1020_adoption_state": adoption_state,
            "external_scientific_truth": False,
            "experimental_evidence": False,
        })

    content_adoption_edges: list[dict[str, Any]] = []
    for edge_id, candidate_index, judgment_index, target_index, role in CONTENT_ADOPTION_SPECS:
        content_adoption_edges.append({
            "edge_id": f"P061-STEP50-CONTENT-{edge_id}",
            "edge_type": "COMPETING_TEXT_CONTENT_TO_ADOPTED_V1020_SOURCE",
            "candidate": source_ref(by_index[candidate_index]),
            "judgment": source_ref(by_index[judgment_index]),
            "target": adopted_target_ref(by_index[target_index], "bounded section replacement recorded by judgment"),
            "integration_role": role,
            "authority_ceiling": "CONTENT_ADOPTION_ONLY_NOT_SCIENTIFIC_VALIDITY",
            "external_scientific_truth": False,
        })

    review_triage_rows: list[dict[str, Any]] = []
    triage_row = by_path["Claude/docs/v1.0.20/results/comp_P7_review/TRIAGE_P7.md"]
    triage_text = text_by_path[triage_row["path"]]
    for triage_id in [f"T-{number:02d}" for number in range(1, 19)]:
        if f"| {triage_id} |" not in triage_text:
            raise AuditError(f"missing triage row {triage_id}")
        target_index, anchor = TRIAGE_TARGETS[triage_id]
        target_row = by_index[target_index]
        review_triage_rows.append({
            "triage_id": triage_id,
            "triage_source": source_ref(triage_row),
            "target": adopted_target_ref(target_row, anchor),
            "disposition": "ADOPTED_INTERNAL_EDIT",
            "authority_ceiling": (
                "PROCESS_RECORD_ONLY" if target_index == 86 else
                "RELEASE_SURFACE_EDIT_ONLY" if target_index == 44 else
                "ADOPTED_RELEASE_CONTENT_ONLY"
            ),
            "external_scientific_truth": False,
        })

    harness_rows = [row for row in competitive_text if artifact_role(row["path"], row["review_mode"]) == "RENDER_HARNESS"]
    candidate_rows = [row for row in competitive_text if figure_candidate_id(row["path"]) is not None]
    candidate_names = [PurePosixPath(row["path"]).name.lower() for row in candidate_rows]
    if len(candidate_names) != len(set(candidate_names)):
        raise AuditError("candidate basename collision")
    candidates_by_name = {PurePosixPath(row["path"]).name.lower(): row for row in candidate_rows}
    family_pdfs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in competitive:
        if row["review_mode"] == "FULL_PDF":
            family_pdfs[source_family(row["path"])].append(row)
    harness_edges: list[dict[str, Any]] = []
    candidate_to_harness: dict[str, list[str]] = defaultdict(list)
    for harness in harness_rows:
        inputs = parse_harness_inputs(text_by_path[harness["path"]])
        for input_name in inputs:
            basename = PurePosixPath(input_name).name
            if not basename.lower().endswith(".tex"):
                basename += ".tex"
            candidate = candidates_by_name.get(basename.lower())
            if candidate is None:
                raise AuditError(f"unresolved harness input {input_name} in {harness['path']}")
            family = source_family(harness["path"])
            pdf_targets = family_pdfs[family]
            harness_stem = PurePosixPath(harness["path"]).stem.lower()
            narrowed = [pdf for pdf in pdf_targets if PurePosixPath(pdf["path"]).stem.lower() == harness_stem]
            if len(narrowed) != 1:
                raise AuditError(f"harness PDF target ambiguity: {harness['path']}")
            cid = figure_candidate_id(candidate["path"])
            assert cid is not None
            candidate_to_harness[cid].append(harness["source_id"])
            harness_edges.append({
                "edge_id": f"P061-STEP50-RENDER-{len(harness_edges)+1:03d}",
                "edge_type": "CANDIDATE_TEX_TO_HARNESS_TO_RENDERED_PDF",
                "candidate": source_ref(candidate),
                "harness": source_ref(harness),
                "rendered_pdf": source_ref(narrowed[0]),
                "renderer_execution_state": "HISTORICAL_SELF_REPORT_NOT_FRESHLY_EXECUTED",
                "authority_ceiling": "SOURCE_AND_RENDER_GENEALOGY_ONLY",
            })
    if len(harness_edges) != 31:
        raise AuditError(f"expected 31 harness edges, got {len(harness_edges)}")

    figure_candidates: list[dict[str, Any]] = []
    for row in sorted(candidate_rows, key=lambda item: figure_candidate_id(item["path"]) or ""):
        cid = figure_candidate_id(row["path"])
        assert cid is not None
        selection = FIGURE_FORWARD_SELECTIONS[cid]
        figure_candidates.append({
            "candidate_id": cid,
            "candidate_source": source_ref(row),
            "harness_source_ids": sorted(candidate_to_harness[cid]),
            "judgment_source_id": by_index[68]["source_id"],
            "judgment_cluster": selection["cluster"],
            "forward_selection_role": selection["role"],
            "forward_grade": selection["grade"],
            "v1020_adopted_figure": False,
            "v1020_tex_include_edge": None,
            "v1020_generated_release_pdf_page_edge": None,
            "forward_target": "V1.0.21_Q4_PHASE062_ADOPTION_ADJUDICATION",
            "numeric_reproduction_state": "INTERNAL_SELF_REPORT_UNVERIFIED",
            "material_validation_state": "UNVERIFIED",
            "experimental_evidence_state": "NOT_EVIDENCE",
        })

    figure_genealogy_routes: list[dict[str, Any]] = []
    family_source_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in competitive_text:
        family_source_rows[source_family(row["path"])].append(row)
    render_by_candidate = {
        row["candidate"]["source_id"]: row for row in harness_edges
    }
    for candidate in figure_candidates:
        candidate_source = candidate["candidate_source"]
        candidate_id = candidate["candidate_id"]
        family = candidate_id.split("-")[0]
        provenance_state = FIGURE_PROVENANCE_STATES[candidate_id]
        family_rows = family_source_rows[family]
        model_rows = [
            {
                "record": source_ref(row),
                "relation_scope": "FAMILY_COMPETITION_CONTEXT_NOT_NUMERIC_PROVENANCE",
                "candidate_link_state": "CONFIRMED",
                "evidence_anchor": "FULL_TEXT_1_TO_EOF_AND_CANDIDATE_LIST_CONTEXT",
            }
            for row in family_rows
            if artifact_role(row["path"], row["review_mode"]) == "COMPETITION_SPECIFICATION"
        ]
        data_rows = [
            {
                "record": source_ref(row),
                "relation_scope": "FAMILY_DATA_CONTEXT_CANDIDATE_LINK_ADJUDICATED_SEPARATELY",
                "candidate_link_state": provenance_state["data"],
                "evidence_anchor": "FULL_TEXT_1_TO_EOF_CROSS_READ_WITH_CANDIDATE",
                "route": provenance_state["route"],
            }
            for row in family_rows
            if artifact_role(row["path"], row["review_mode"]) == "COORDINATE_OR_DATA_RECORD"
        ]
        generator_rows = [
            {
                "record": source_ref(row),
                "relation_scope": "FAMILY_GENERATION_CONTEXT_CANDIDATE_LINK_ADJUDICATED_SEPARATELY",
                "candidate_link_state": provenance_state["generation"],
                "evidence_anchor": "FULL_TEXT_1_TO_EOF_CROSS_READ_WITH_CANDIDATE",
                "route": provenance_state["route"],
            }
            for row in family_rows
            if artifact_role(row["path"], row["review_mode"]) == "GENERATION_OR_COORDINATE_RECORD"
        ]
        render = render_by_candidate[candidate_source["source_id"]]
        missing_edges = [
            {
                "edge": "candidate_to_individual_reviewer_vote",
                "state": "GROUND_NOT_FOUND",
                "route": "P061-STEP50-GNF-011",
            },
            {
                "edge": "v1020_adopted_figure_to_tex_include_to_release_pdf_page",
                "state": "GROUND_NOT_FOUND_VERSION_BOUNDARY_V1021_FORWARD_ONLY",
                "route": "P061-STEP50-GNF-001",
            },
        ]
        if not data_rows:
            missing_edges.append({
                "edge": "persisted_source_data_to_candidate",
                "state": provenance_state["data"],
                "route": provenance_state["route"],
            })
        if not generator_rows:
            missing_edges.append({
                "edge": "generator_to_candidate",
                "state": provenance_state["generation"],
                "route": provenance_state["route"],
            })
        if data_rows and provenance_state["data"] != "CONFIRMED":
            missing_edges.append({
                "edge": "candidate_specific_data_to_candidate",
                "state": provenance_state["data"],
                "route": provenance_state["route"],
            })
        if generator_rows and provenance_state["generation"] != "CONFIRMED":
            missing_edges.append({
                "edge": "candidate_specific_generator_to_candidate",
                "state": provenance_state["generation"],
                "route": provenance_state["route"],
            })
        figure_genealogy_routes.append({
            "route_id": f"P061-STEP50-FIG-GENEALOGY-{len(figure_genealogy_routes)+1:03d}",
            "candidate_id": candidate_id,
            "source_model_or_claim_records": model_rows,
            "source_data_records": data_rows,
            "generation_records": generator_rows,
            "candidate_specific_data_link_state": provenance_state["data"],
            "candidate_specific_generation_link_state": provenance_state["generation"],
            "candidate": candidate_source,
            "renderer_harness": render["harness"],
            "competitive_rendered_pdf": render["rendered_pdf"],
            "review_vote_records": [],
            "consolidated_judgment": source_ref(by_index[68]),
            "forward_selection": {
                "cluster": candidate["judgment_cluster"],
                "role": candidate["forward_selection_role"],
                "grade": candidate["forward_grade"],
                "target": candidate["forward_target"],
            },
            "v1020_adopted_figure": None,
            "v1020_tex_include": None,
            "v1020_release_pdf_page": None,
            "missing_edges": missing_edges,
            "authority_ceiling": "FROZEN_INTERNAL_GENEALOGY_ONLY",
        })

    images = read_att["image_records"]
    pdfs = read_att["pdf_records"]
    if len(images) != 23 or len(pdfs) != 14:
        raise AuditError("visual source count mismatch")
    visual_images: list[dict[str, Any]] = []
    for prior in images:
        source = by_path[prior["path"]]
        frozen_blob_sha1, frozen_data = blobs[prior["path"]]
        if frozen_blob_sha1 != source["blob_sha1"] or sha256_bytes(frozen_data) != source["sha256"]:
            raise AuditError(f"frozen image identity mismatch: {prior['path']}")
        observation = manual_image_observation(prior["path"])
        visual_images.append({
            **source_ref(source),
            "pixel_identity": f"sha256:{source['sha256']}",
            "width": prior["width"],
            "height": prior["height"],
            "mode": prior["mode"],
            "format": prior["format"],
            "frames": prior["frames"],
            "original_resolution_inspected": True,
            "review_state": "HUMAN_ORIGINAL_RESOLUTION_FULL",
            **observation,
        })

    visual_pdfs: list[dict[str, Any]] = []
    flat_pages: list[dict[str, Any]] = []
    for prior in pdfs:
        source = by_path[prior["path"]]
        frozen_blob_sha1, frozen_data = blobs[prior["path"]]
        if frozen_blob_sha1 != source["blob_sha1"] or sha256_bytes(frozen_data) != source["sha256"]:
            raise AuditError(f"frozen PDF identity mismatch: {prior['path']}")
        pages: list[dict[str, Any]] = []
        for page in prior["pages"]:
            observation = manual_pdf_page_observation(prior["path"], page["page"])
            record = {
                "page_identity": f"{source['source_id']}#page-{page['page']:04d}",
                "pdf_sha256": source["sha256"],
                "page": page["page"],
                "width_points": page["width_points"],
                "height_points": page["height_points"],
                "extracted_text_chars_prior_attestation": page["extracted_text_chars"],
                "render_review": "HUMAN_FULL_PAGE_RENDER_PARTITION_150_TO_200_DPI",
                **observation,
            }
            pages.append(record)
            flat_pages.append({"source_id": source["source_id"], **record})
        visual_pdfs.append({
            **source_ref(source),
            "pages_expected": prior["pages_expected"],
            "pages_observed": len(pages),
            "encrypted": prior["encrypted"],
            "review_state": "HUMAN_ALL_PAGES_FULL",
            "pages": pages,
        })
    if len(flat_pages) != 130:
        raise AuditError("visual page count mismatch")

    visual = {
        "schema_version": "phase061-step50-visual-attestation-v1",
        "artifact_kind": "VISUAL_READ_ATTESTATION",
        "generated_date": DATE,
        "phase": 61,
        "step": 50,
        "baseline_commit": BASELINE,
        "status": "PASS_WITH_CONCERNS",
        "authority_boundary": {
            "visual_appearance_only": True,
            "numerical_validity": False,
            "material_validity": False,
            "experimental_evidence": False,
            "primary_literature_authority": False,
        },
        "method": {
            "images": "23/23 original-resolution occurrence review; byte SHA is the pixel-file identity",
            "pdfs": "14/14 PDFs and 130/130 pages rendered and visually reviewed by bounded partitions at 150 to 200 dpi",
            "page_identity": "source occurrence ID plus one-based page number and frozen PDF SHA-256",
            "prior_machine_extent_input": READ_PATH.relative_to(REPO).as_posix(),
        },
        "image_occurrences": visual_images,
        "pdf_occurrences": visual_pdfs,
        "counts": {
            "image_occurrences": len(visual_images),
            "unique_image_sha256": len({row["sha256"] for row in visual_images}),
            "original_resolution_inspections": sum(row["original_resolution_inspected"] for row in visual_images),
            "pdf_occurrences": len(visual_pdfs),
            "pdf_pages": len(flat_pages),
            "page_identity_unique": len({row["page_identity"] for row in flat_pages}),
            "dummy_scaffold_pages": sum(row["page_role"] == "DUMMY_SCAFFOLD_PAGE" for row in flat_pages),
            "pages_with_visible_defects": sum(bool(row["visible_defects"]) for row in flat_pages),
            "images_with_visible_defects": sum(bool(row["visible_defects"]) for row in visual_images),
            "blank_pages": sum(row["blank_page"] for row in flat_pages),
            "render_failures": sum(row["render_failure"] for row in flat_pages),
            "numeric_validity_promotions": 0,
            "experimental_evidence_promotions": 0,
        },
    }

    source_role_counts = Counter(row["artifact_role"] for row in competitive_records)
    family_counts = Counter(row["family"] for row in competitive_records)
    review_count_claims = [
        {"claim": "PLAN_P7 initial review windows", "values": [4], "source_id": by_index[62]["source_id"], "state": "HISTORICAL_INITIAL_PLAN"},
        {
            "claim": "STEP_LOG/RESULT review-source union",
            "values": [11],
            "source_id": by_index[85]["source_id"],
            "state": "P7_UNION_SOURCE_TAXONOMY_NOT_11_INDEPENDENT_COMPLETED_REVIEWERS",
            "breakdown": {
                "chapter1_O_windows": 3,
                "chapter2_O_and_F_windows": 6,
                "partial_prior_F1": 1,
                "stream3_interchapter_report": 1,
            },
            "separate_final_fable_pass": 1,
        },
        {"claim": "figure competition windows", "values": [6], "source_id": by_index[68]["source_id"], "state": "FIGURE_COMPETITION_TAXONOMY"},
        {"claim": "topology REVIEW_/TRIAGE Markdown record occurrences", "values": [12], "source_id": triage_row["source_id"], "state": "FILE_OCCURRENCE_TAXONOMY_NOT_REVIEWER_COUNT"},
    ]

    review_findings = [
        {
            "id": "P061-STEP50-P1-001", "priority": "P1",
            "object": "P7 review-count semantics",
            "finding": "The historical 11-source union is 3 chapter-1 O windows + 6 chapter-2 O/F windows + 1 partial prior F1 + 1 stream-3 report; FINAL_FABLE is a separate pass, so 11 must not be promoted to 11 independent completed reviewers.",
            "authority": "FROZEN_PROCESS_RECORD_AND_FULL_READ_REVIEW",
        },
        {
            "id": "P061-STEP50-P1-002", "priority": "P1",
            "object": "FF1 coordinate persistence claim",
            "finding": "FRAMING_FF1.md:133 claims every curve has persisted coordinates, but the lag-map TeX stages (48k,6k), (46k,8k), (44k,10k), and (40k,13k) while coords/generator persist only a generic 40/48/60/80k schedule with default Omega=13k; only (40k,13k) is directly recoverable.",
            "authority": "INTERNAL_PROVENANCE_CONSISTENCY_ONLY",
        },
        {
            "id": "P061-STEP50-P1-003", "priority": "P1",
            "object": "FF3 nucleation formula-to-render consistency",
            "finding": "The declared/generated/coordinate formula 3x^2-2x^3 disagrees with plotted TikZ coordinates in fig_ff3_7_nucleation.tex; at x=1.5/1.6/1.63 the formula gives 0/-0.512/-0.690794 while the plot gives -0.28/-1.012/-1.269 (maximum observed absolute discrepancy 0.578206).",
            "authority": "INTERNAL_NUMERICAL_CONSISTENCY_NOT_EXTERNAL_SCIENTIFIC_TRUTH",
        },
        {
            "id": "P061-STEP50-P2-001", "priority": "P2",
            "object": "P4 competition-count drift",
            "finding": "AUTHOR_BRIEF states N=4, while PICK_JUDGMENT records six launched, five finished, and F2 timeout after an earlier failed round.",
            "authority": "FROZEN_PROCESS_RECORD",
        },
        {
            "id": "P061-STEP50-P2-002", "priority": "P2",
            "object": "FF2 unresolved references",
            "finding": "All four FF2 PDF pages visibly retain unresolved references: chapter 1 pages contain 5 and 10 markers; chapter 2 pages contain 11 and 4 markers (30 total).",
            "authority": "HUMAN_FULL_PAGE_VISUAL_REVIEW",
        },
        {
            "id": "P061-STEP50-P2-003", "priority": "P2",
            "object": "FF2 coordinate artifact genealogy",
            "finding": "A generator exists, but no persisted stdout/coordinate artifact was found for exact recovery of the rendered numbers.",
            "authority": "GROUND_NOT_FOUND_IN_FROZEN_TOPOLOGY",
        },
        {
            "id": "P061-STEP50-P2-004", "priority": "P2",
            "object": "FF3 latent-variable coordinate route",
            "finding": "coords_ff3 records temperature-specific w(T)=69.4/77.6/86.0, while the figure intentionally uses fixed w(298.15 K)=69.6/77.6/85.7; the caption explains the choice, but the plotted triple is not directly recoverable from the persisted coordinate artifact.",
            "authority": "INTERNAL_PROVENANCE_CONSISTENCY_ONLY",
        },
        {
            "id": "P061-STEP50-P2-005", "priority": "P2",
            "object": "FF3/FO1/FO2/FO3 unresolved references",
            "finding": "All 17 pages in these four competitive families contain visible unresolved-reference markers; a human partition counted 65 in aggregate, but the per-page distribution was not persisted. No blank page or obvious clipping was observed.",
            "authority": "HUMAN_FULL_PAGE_VISUAL_REVIEW",
            "aggregate_count": 65,
            "machine_reconstructability": "AGGREGATE_HUMAN_COUNT_ONLY_PER_PAGE_DISTRIBUTION_NOT_PERSISTED",
        },
        {
            "id": "P061-STEP50-P2-006", "priority": "P2",
            "object": "FO3 page-1 float ordering",
            "finding": "The document title appears after a figure caption on page 1.",
            "authority": "HUMAN_FULL_PAGE_VISUAL_REVIEW",
        },
        {
            "id": "P061-STEP50-P2-007", "priority": "P2",
            "object": "FO1 figure-4 label placement",
            "finding": "The electronic line and label slightly overlap on page 2 but remain readable.",
            "authority": "HUMAN_FULL_PAGE_VISUAL_REVIEW",
        },
        {
            "id": "P061-STEP50-P2-008", "priority": "P2",
            "object": "P4 validation PNG title clipping",
            "finding": "P4_lco_heat_validation.png clips the right side of the panel (c) title.",
            "authority": "HUMAN_ORIGINAL_RESOLUTION_VISUAL_REVIEW",
        },
        {
            "id": "P061-STEP50-P2-009", "priority": "P2",
            "object": "dQ/dV PNG version identity",
            "finding": "anode_fit_v1_0_14_dqdv.png has v1.0.14 in the filename but Anode Fit 1.0.16 in the internal title.",
            "authority": "HUMAN_ORIGINAL_RESOLUTION_VISUAL_REVIEW",
        },
        {
            "id": "P061-STEP50-P2-010", "priority": "P2",
            "object": "graph-suite PNG evidence independence",
            "finding": "v1015, v1016, and v1019 graph-suite PNGs are nearly identical apart from sparse version-legend pixels and must not be counted as three independent scientific witnesses.",
            "authority": "HUMAN_ORIGINAL_RESOLUTION_VISUAL_REVIEW_NOT_SCIENTIFIC_VALIDATION",
        },
        {
            "id": "P061-STEP50-P2-011", "priority": "P2",
            "object": "Q3 candidate-claim conflict",
            "finding": "q3f1 describes reaction-coordinate curvature as zero/free translation, whereas q3f3/f4 describe an unstable mode.",
            "authority": "INTERNAL_CANDIDATE_CONSISTENCY_ONLY_UNVERIFIED_EXTERNAL",
        },
    ]

    ground_not_found = [
        {"id": "P061-STEP50-GNF-001", "object": "v1.0.20 adopted TeX include edge for any of the 31 P7 figure candidates", "target_phase": 62},
        {"id": "P061-STEP50-GNF-002", "object": "v1.0.20 adopted TeX include edge for any of the five packaged release PNG occurrences", "target_phase": 62},
        {"id": "P061-STEP50-GNF-003", "object": "persisted FF1 coordinate rows for three of four staged lag-map parameter pairs", "target_phase": 67},
        {"id": "P061-STEP50-GNF-004", "object": "persisted crop command and exact pixel-subarray edge for FF1 crop PNGs", "target_phase": 67},
        {"id": "P061-STEP50-GNF-005", "object": "persisted FF2 stdout/coordinate artifact recovering rendered numbers", "target_phase": 67},
        {"id": "P061-STEP50-GNF-006", "object": "persisted FF3 coordinate row matching the plotted fixed-temperature latent-variable triple", "target_phase": 67},
        {"id": "P061-STEP50-GNF-007", "object": "source-data or renderer command/environment proving every other hard-coded competitive coordinate", "target_phase": 67},
        {"id": "P061-STEP50-GNF-008", "object": "fresh clean competitive harness counterpart with all unresolved references removed", "target_phase": 62},
        {"id": "P061-STEP50-GNF-009", "object": "v1.0.20 adoption edge for Q2/Q3 v1.0.21 draft content", "target_phase": 62},
        {"id": "P061-STEP50-GNF-010", "object": "experimental dataset lineage for generated figure curves", "target_phase": 72},
        {"id": "P061-STEP50-GNF-011", "object": "candidate-level individual reviewer vote edge for each of the 31 figure candidates", "target_phase": 62},
    ]
    unverified = [
        {"id": "P061-STEP50-UNV-001", "object": "all figure numeric reproduction self-reports", "target_phase": 67},
        {"id": "P061-STEP50-UNV-002", "object": "material and experimental validity of all curves", "target_phase": 72},
        {"id": "P061-STEP50-UNV-003", "object": "review claims of literature/web confirmation", "target_phase": 71},
        {"id": "P061-STEP50-UNV-004", "object": "final v1.0.21 placement, density, labels, and complete build of forward-selected figures", "target_phase": 62},
        {"id": "P061-STEP50-UNV-005", "object": "Q2/Q3 DOI, derivations, and numerical/material/experimental truth", "target_phase": 71},
        {"id": "P061-STEP50-UNV-006", "object": "two-phase-width thermal-form assumption and heat-sign claim near xbar=0.75", "target_phase": 72},
        {"id": "P061-STEP50-UNV-007", "object": "MCMB +3-4 mV/K claim marked unverified in the frozen source", "target_phase": 71},
    ]

    matrix = {
        "schema_version": "phase061-step50-review-artifact-v1",
        "artifact_kind": "REVIEW_ARTIFACT_AUTHORITY_MATRIX",
        "generated_date": DATE,
        "phase": 61,
        "step": 50,
        "baseline_commit": BASELINE,
        "status": "PASS_WITH_CONCERNS",
        "gate": "PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS",
        "authority_boundary": {
            "frozen_source_genealogy": True,
            "internal_review_and_selection": True,
            "visual_appearance": True,
            "numerical_reproduction": False,
            "material_or_experimental_validity": False,
            "primary_literature_truth": False,
        },
        "input_artifacts": [
            {"path": path.relative_to(REPO).as_posix(), "sha256": sha256_bytes(path.read_bytes())}
            for path in (TOPOLOGY_PATH, READ_PATH, PROCESS_PATH, LINEAGE_PATH, CITATION_PATH)
        ],
        "full_read_records": full_read_records,
        "adopted_source_references": adopted,
        "competitive_source_records": competitive_records,
        "content_adoption_edges": content_adoption_edges,
        "p7_review_triage": review_triage_rows,
        "figure_candidates": figure_candidates,
        "candidate_render_edges": harness_edges,
        "figure_genealogy_routes": figure_genealogy_routes,
        "review_count_claims": review_count_claims,
        "review_findings": review_findings,
        "visual_attestation": {
            "path": VISUAL_PATH.relative_to(REPO).as_posix(),
            "semantic_sha256": semantic_sha(visual),
            "image_occurrences": len(visual_images),
            "pdf_occurrences": len(visual_pdfs),
            "pdf_pages": len(flat_pages),
        },
        "ground_not_found": ground_not_found,
        "unverified_queue": unverified,
        "counts": {
            "topology_sources": len(sources),
            "competitive_occurrences": len(competitive),
            "competitive_text_sources": len(competitive_text),
            "process_or_adoption_reference_sources": len(process_review),
            "full_read_source_union": len(full_read_records),
            "adopted_source_references": len(adopted),
            "competitive_family_counts": dict(sorted(family_counts.items())),
            "competitive_artifact_role_counts": dict(sorted(source_role_counts.items())),
            "p2_candidate_tex": sum(row["family"] == "comp_P2_part0" and row["artifact_role"] == "CANDIDATE_TEX" for row in competitive_records),
            "p4_candidate_tex": sum(row["family"] == "comp_P4_mitbg" and row["artifact_role"] == "CANDIDATE_TEX" for row in competitive_records),
            "p7_review_documents": sum(row["family"] == "comp_P7_review" for row in competitive_records),
            "q2_occurrences": sum(row["family"] == "comp_Q2_gcbalance" for row in competitive_records),
            "q3_occurrences": sum(row["family"] == "comp_Q3_tst" for row in competitive_records),
            "figure_candidates": len(figure_candidates),
            "figure_windows": len({cid.split("-")[0] for cid in FIGURE_FORWARD_SELECTIONS}),
            "candidate_render_edges": len(harness_edges),
            "figure_genealogy_routes": len(figure_genealogy_routes),
            "content_adoption_edges": len(content_adoption_edges),
            "p7_adopted_triage_rows": len(review_triage_rows),
            "v1020_adopted_figure_candidates": sum(row["v1020_adopted_figure"] for row in figure_candidates),
            "v1020_packaged_png_include_edges": 0,
            "visual_images": len(visual_images),
            "visual_pdfs": len(visual_pdfs),
            "visual_pdf_pages": len(flat_pages),
            "external_scientific_promotions": 0,
            "experimental_evidence_promotions": 0,
        },
        "required_negative_controls": [
            "SKIPPED_IMAGE_OCCURRENCE", "MISSING_PDF_PAGE", "FALSE_V1020_FIGURE_ADOPTION",
            "REVIEW_COUNT_INFLATION", "GENERATED_AS_EXPERIMENT", "VISUAL_PASS_AS_NUMERIC_VALIDITY",
            "DROPPED_COMPETITIVE_SOURCE", "FIGURE_CANDIDATE_COUNT", "CANDIDATE_RENDER_COUNT",
            "BROKEN_GENEALOGY_ROUTE", "Q2_Q3_FALSE_ADOPTION", "CONTENT_ADOPTION_WITHOUT_JUDGMENT",
            "PACKAGED_PNG_FALSE_INCLUDE",
            "GROUND_NOT_FOUND_REMOVED", "UNVERIFIED_REMOVED", "EXTERNAL_PROMOTION",
            "STRICT_JSON_DUPLICATE_KEY", "STRICT_JSON_NONFINITE", "PERSISTED_REBUILD_MISMATCH",
            "TWO_RUN_MISMATCH",
        ],
    }
    matrix["builder"] = {
        "path": Path(__file__).relative_to(REPO).as_posix(),
        "sha256_lf": sha256_bytes(Path(__file__).read_bytes().replace(b"\r\n", b"\n")),
        "historical_production_imported": False,
        "historical_renderer_executed": False,
        "git_subprocess_contract": "single git cat-file --batch invocation for selected frozen text, image, and PDF blobs",
    }
    return matrix, visual


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-out", type=Path, default=MATRIX_PATH)
    parser.add_argument("--visual-out", type=Path, default=VISUAL_PATH)
    args = parser.parse_args(argv)
    try:
        matrix, visual = build()
        matrix["visual_attestation"]["path"] = VISUAL_PATH.relative_to(REPO).as_posix()
        write_json(args.visual_out, visual)
        write_json(args.matrix_out, matrix)
    except (AuditError, OSError, UnicodeError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL_P061_STEP50_BUILDER {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(
        "PASS_P061_STEP50_BUILD "
        f"competitive={matrix['counts']['competitive_occurrences']} "
        f"figures={matrix['counts']['figure_candidates']} "
        f"images={visual['counts']['image_occurrences']} "
        f"pdf={visual['counts']['pdf_occurrences']}/{visual['counts']['pdf_pages']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
