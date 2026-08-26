#!/usr/bin/env python3
"""Build deterministic Phase 061 Step 46 topology and read-attestation artifacts."""

from __future__ import annotations

import argparse
import ast
import copy
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

from PIL import Image
from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[3]
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
TOPOLOGY = REPO / "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
ATTESTATION = REPO / "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json"
BUILDER = Path(__file__).resolve()
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_MANIFEST_NORMALIZED_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"

# These records are patched only after the assigned reviewer actually reports full coverage.
# They remain deterministic recovery evidence and never promote scientific authority.
REVIEW_PARTITIONS: dict[str, dict[str, Any]] = {
    "A_FINAL_RELEASE": {
        "manifest_indices": [[1, 53]],
        "expected": {"paths": 53, "text": 45, "pdf": 3, "pdf_pages": 99, "image": 5},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_scope": "final/release surfaces",
        "review_evidence": {
            "text_read_eof": "45/45",
            "physical_lines": 7209,
            "nonblank_lines": 6682,
            "pdf_pages_visual": "99/99",
            "image_occurrences_visual": "5/5",
            "path_set_sha256_manifest_order_lf": "839e684d5f9f915db5578cdbb8538ed44d2a974b131823be874501fc1a5559d5",
        },
        "review_findings": [
            "P4_lco_heat_validation.png has a right-clipped long title in subplot (c).",
            "anode_fit_v1_0_14_dqdv.png has an internal title identifying Anode Fit 1.0.16 rather than the filename's 1.0.14.",
            "The three graph_suite images use nonmonotonic lower-panel ordering V7, V9, V8 without visible clipping.",
            "All three PDFs were visually inspected page by page; no obvious page-boundary clipping was found.",
            "Release code, guide and handover identify a v1.0.19 implementation carry rather than an independently promoted v1.0.20 implementation.",
        ],
        "ground_not_found": [
            "An adoption edge integrating appendix_phase_separation.tex into either main document.",
            "An adoption edge inserting any of the five packaged PNGs into the 66-page or 25-page manuscript.",
            "Direct source authority closing LCO Omega/dH_a, broadening gamma and multi-temperature LCO electronic restoration debts.",
        ],
    },
    "B_PROCESS_SNAPSHOT": {
        "manifest_indices": [[54, 94], [221, 232]],
        "expected": {"paths": 53, "text": 53, "pdf": 0, "pdf_pages": 0, "image": 0},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_scope": "plans, core process/results, snapshots, structure tool and test gate",
        "review_evidence": {
            "text_read_eof": "53/53",
            "physical_lines": 15182,
            "nonblank_lines": 14442,
            "strict_json": "10/10",
            "strict_json_nodes": 9892,
            "path_set_sha256_manifest_order_lf": "64d4e6c586069c079c012a972db2fd4d0c3997fffe614573328e9c07ada9b81a",
            "path_blob_sha256_manifest_order_lf": "9e7abb47cbbca5a402e2c2db56bb8babfa9595db06e4666272994cfb94602206",
        },
        "review_findings": [
            "P5 and P6 snapshot paths are separate occurrences of the same frozen blob.",
            "P8 has a plan and ledger PASS claim but no dedicated RESULT_P8 or STEP_LOG_P8 in the exact v1.0.20 inventory.",
            "The master P7 window count, execution-ledger master-version pointer and reference-ledger heading counts contain stale or contradictory bookkeeping.",
            "Process/test/build/scientific claims are internal self-reports and were not promoted to runtime or scientific truth.",
        ],
        "ground_not_found": [
            "Dedicated RESULT_P8 and STEP_LOG_P8 artifacts.",
            "An explicit adjudication edge for the ashcroftmermin1976 V2-to-V1 classification change.",
        ],
    },
    "C_COMPETITIVE": {
        "manifest_indices": [[95, 220]],
        "expected": {"paths": 126, "text": 97, "pdf": 11, "pdf_pages": 31, "image": 18},
        "status": "PASS_HUMAN_FULL_REVIEW",
        "review_scope": "competitive drafts, reviews and figure candidates",
        "review_evidence": {
            "text_read_eof": "97/97",
            "physical_lines": 9162,
            "nonblank_lines": 8211,
            "pdf_pages_visual": "31/31",
            "image_occurrences_visual": "18/18",
            "strict_json": "1/1",
            "strict_json_nodes": 1757,
            "path_set_sha256_sorted_lf": "7aad75d6aedc3f10afeb4cb2e382d2ecffa1516953d5192c02609de3f7f980ea",
        },
        "review_findings": [
            "Three FF1 harness first pages are explicit dummy/zero scaffold surfaces rather than substantive figures.",
            "Eight competitive PDF families contain widespread unresolved ?? references; the same issue is visible in ten derived PNG occurrences.",
            "Two FF1 PNGs are intentional crops of a candidate page, including one partial crop rather than an independent complete page.",
            "Competitive PDF/PNG pairs are visually related but byte-distinct, and no duplicate blob occurs inside this partition.",
            "Q2 and Q3 identify themselves as v1.0.21 competing drafts and were not promoted to adopted v1.0.20 content.",
        ],
        "ground_not_found": [
            "A final authoritative adoption edge from any FF/FO, Q2 or Q3 candidate into the v1.0.20 release manuscript.",
            "A clean reference-resolved harness counterpart without unresolved ?? markers.",
            "Independent external verification of bibliography, numeric or scientific claims in the competitive review corpus.",
        ],
    },
}


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


def reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def walk_json(value: Any, path: str = "$", stats: dict[str, int] | None = None) -> dict[str, int]:
    if stats is None:
        stats = {"nodes": 0, "max_depth": 0}
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], path.count(".") + path.count("["))
    if isinstance(value, float) and not math.isfinite(value):
        raise NonFiniteNumberError(path)
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError(path)
            walk_json(child, f"{path}.{key}", stats)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_json(child, f"{path}[{index}]", stats)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise TypeError(path)
    return stats


def strict_json_bytes(data: bytes) -> tuple[Any, dict[str, int]]:
    value = json.loads(
        data.decode("utf-8"), object_pairs_hook=strict_pairs, parse_constant=reject_constant
    )
    return value, walk_json(value)


def normalize_lf(data: bytes) -> bytes:
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8", errors="strict",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return proc.stdout.strip()


def git_blob(path: str) -> tuple[str, str, bytes]:
    row = run_git("ls-tree", BASELINE, "--", path)
    if not row:
        raise FileNotFoundError(path)
    meta, actual_path = row.split("\t", 1)
    mode, object_type, blob = meta.split()
    if actual_path != path or object_type != "blob":
        raise ValueError(path)
    proc = subprocess.run(
        ["git", "cat-file", "blob", blob], cwd=REPO,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return mode, blob, proc.stdout


def authority_group(index: int) -> str:
    if 1 <= index <= 53:
        return "FINAL_RELEASE_SURFACE"
    if 54 <= index <= 63:
        return "PLAN_P0_P8"
    if 64 <= index <= 94:
        return "CORE_PROCESS_RESULT"
    if 95 <= index <= 220:
        return "COMPETITIVE_CANDIDATE_REVIEW"
    if 221 <= index <= 230:
        return "STRUCTURAL_SNAPSHOT"
    if index == 231:
        return "STRUCTURE_TOOL"
    if index == 232:
        return "TEST_GATE"
    raise ValueError(index)


def review_partition(index: int) -> str:
    if 1 <= index <= 53:
        return "A_FINAL_RELEASE"
    if 54 <= index <= 94 or 221 <= index <= 232:
        return "B_PROCESS_SNAPSHOT"
    if 95 <= index <= 220:
        return "C_COMPETITIVE"
    raise ValueError(index)


def authority_class(index: int) -> str:
    if 1 <= index <= 53:
        return "RELEASE_SURFACE_UNADJUDICATED"
    if 54 <= index <= 94:
        return "PROCESS_SELF_REPORT"
    if 95 <= index <= 220:
        return "COMPETITIVE_CANDIDATE_OR_REVIEW"
    if 221 <= index <= 230:
        return "GENERATED_STRUCTURAL_SNAPSHOT"
    return "SUPPORT_TOOL_OR_TEST"


def text_structure(path: str, text: str, extension: str) -> dict[str, Any]:
    structure: dict[str, Any] = {
        "headings": len(re.findall(r"(?m)^#{1,6}\s+", text)) if extension == "md" else 0,
        "labels": re.findall(r"\\label\{([^}]+)\}", text) if extension == "tex" else [],
        "inputs": re.findall(r"\\(?:input|include)\{([^}]+)\}", text) if extension == "tex" else [],
        "graphics": re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text) if extension == "tex" else [],
        "citation_keys": sorted({
            key.strip()
            for group in re.findall(r"\\cite\w*\{([^}]+)\}", text)
            for key in group.split(",") if key.strip()
        }) if extension == "tex" else [],
        "equation_environments": len(re.findall(r"\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}", text)) if extension == "tex" else 0,
    }
    if extension == "py":
        tree = ast.parse(text, filename=path)
        structure["python_ast"] = {
            "functions": sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree)),
            "classes": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)),
            "imports": sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)),
            "asserts": sum(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        }
    return structure


def source_identity(
    entry: dict[str, Any], index: int, data: bytes,
    duplicate_occurrence: bool, old_entry: dict[str, Any] | None,
) -> dict[str, Any]:
    if old_entry is not None and old_entry["blob_sha"] == entry["blob_sha"]:
        overlap_class = "IDENTICAL_OVERLAP"
        detailed_relation = "IDENTICAL_SAME_RELATIVE"
    elif old_entry is not None:
        overlap_class = "NEW_BLOB_OR_SOURCE"
        detailed_relation = "CHANGED_SAME_RELATIVE"
    else:
        overlap_class = "NEW_BLOB_OR_SOURCE"
        detailed_relation = "NO_SAME_RELATIVE_SOURCE"
    return {
        "source_id": f"P061-SRC-{index:04d}",
        "manifest_index_v1020": index,
        "path": entry["path"],
        "basename": PurePosixPath(entry["path"]).name,
        "blob_sha1": entry["blob_sha"],
        "sha256": sha256(data),
        "git_mode": entry["git_mode"],
        "size_bytes": len(data),
        "extension": entry["extension"],
        "manifest_role": entry["role"],
        "review_mode": entry["review_mode"],
        "manifest_extent": entry["extent"],
        "dedup_group": entry["dedup_group"],
        "derived_authority_group": authority_group(index),
        "authority_class": authority_class(index),
        "review_partition": review_partition(index),
        "duplicate_relation": "DUPLICATE_BLOB_OCCURRENCE" if duplicate_occurrence else "UNIQUE_BLOB",
        "v1019_overlap_class": overlap_class,
        "v1019_path_relation": detailed_relation,
        "v1019_same_relative_path": old_entry["path"] if old_entry is not None else None,
        "v1019_same_relative_blob_sha1": old_entry["blob_sha"] if old_entry is not None else None,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_bytes = normalize_lf(MANIFEST.read_bytes())
    manifest, manifest_traversal = strict_json_bytes(manifest_bytes)
    if sha256(manifest_bytes) != EXPECTED_MANIFEST_NORMALIZED_SHA256:
        raise ValueError("manifest normalized SHA mismatch")
    if manifest["baseline_commit"] != BASELINE:
        raise ValueError("manifest baseline mismatch")
    selected = [entry for entry in manifest["entries"] if entry["version"] == "v1.0.20"]
    previous = {
        entry["path"].replace("Claude/docs/v1.0.19/", "", 1): entry
        for entry in manifest["entries"]
        if entry["version"] == "v1.0.19" and entry["path"].startswith("Claude/docs/v1.0.19/")
    }
    if len(selected) != 232:
        raise ValueError("v1.0.20 count mismatch")
    selected_blob_counts = Counter(entry["blob_sha"] for entry in selected)

    sources: list[dict[str, Any]] = []
    text_records: list[dict[str, Any]] = []
    pdf_records: list[dict[str, Any]] = []
    image_records: list[dict[str, Any]] = []
    same_relative: list[dict[str, Any]] = []
    blob_paths: dict[str, list[str]] = defaultdict(list)
    partition_actual: dict[str, Counter[str]] = defaultdict(Counter)

    for index, entry in enumerate(selected, start=1):
        mode, blob, data = git_blob(entry["path"])
        if mode != entry["git_mode"] or blob != entry["blob_sha"] or len(data) != entry["size_bytes"]:
            raise ValueError(f"Git identity mismatch: {entry['path']}")
        relative = entry["path"].replace("Claude/docs/v1.0.20/", "", 1)
        old_entry = previous.get(relative)
        identity = source_identity(
            entry, index, data, selected_blob_counts[entry["blob_sha"]] > 1, old_entry
        )
        sources.append(identity)
        blob_paths[blob].append(entry["path"])
        partition = identity["review_partition"]
        partition_actual[partition]["paths"] += 1

        if old_entry is not None:
            old = old_entry
            same_relative.append({
                "relative_path": relative,
                "v1019_path": old["path"],
                "v1019_blob_sha1": old["blob_sha"],
                "v1020_path": entry["path"],
                "v1020_blob_sha1": blob,
                "blob_relation": "IDENTICAL" if old["blob_sha"] == blob else "CHANGED",
            })

        human_status = REVIEW_PARTITIONS[partition]["status"]
        if entry["review_mode"] == "FULL_TEXT":
            text = data.decode("utf-8")
            lines = text.splitlines()
            strict_stats = None
            if entry["extension"] == "json":
                _, strict_stats = strict_json_bytes(data)
            record = {
                "source_id": identity["source_id"],
                "path": entry["path"],
                "read_state": "MACHINE_READ_FULL",
                "human_read_state": "READ_FULL" if human_status == "PASS_HUMAN_FULL_REVIEW" else human_status,
                "physical_lines": len(lines),
                "nonblank_lines": sum(bool(line.strip()) for line in lines),
                "bytes": len(data),
                "sha256": sha256(data),
                "encoding": "utf-8",
                "strict_json_traversal": strict_stats,
                "structure": text_structure(entry["path"], text, entry["extension"]),
            }
            text_records.append(record)
            partition_actual[partition]["text"] += 1
            partition_actual[partition]["text_lines"] += len(lines)
            partition_actual[partition]["text_nonblank_lines"] += record["nonblank_lines"]
        elif entry["review_mode"] == "FULL_PDF":
            reader = PdfReader(io.BytesIO(data), strict=True)
            pages = []
            for page_index, page in enumerate(reader.pages, start=1):
                box = page.mediabox
                extracted = page.extract_text() or ""
                pages.append({
                    "page": page_index,
                    "width_points": float(box.width),
                    "height_points": float(box.height),
                    "extracted_text_chars": len(extracted),
                    "visual_state": "VISUAL_FULL" if human_status == "PASS_HUMAN_FULL_REVIEW" else human_status,
                })
            pdf_records.append({
                "source_id": identity["source_id"],
                "path": entry["path"],
                "sha256": sha256(data),
                "pages_expected": entry["extent"]["pages"],
                "pages_observed": len(reader.pages),
                "encrypted": bool(reader.is_encrypted),
                "read_state": "MACHINE_METADATA_FULL",
                "visual_review_state": "VISUAL_FULL" if human_status == "PASS_HUMAN_FULL_REVIEW" else human_status,
                "pages": pages,
            })
            partition_actual[partition]["pdf"] += 1
            partition_actual[partition]["pdf_pages"] += len(reader.pages)
        elif entry["review_mode"] == "FULL_IMAGE":
            with Image.open(io.BytesIO(data)) as image:
                image.load()
                record = {
                    "source_id": identity["source_id"],
                    "path": entry["path"],
                    "sha256": sha256(data),
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode,
                    "format": image.format,
                    "frames": getattr(image, "n_frames", 1),
                    "read_state": "MACHINE_PIXEL_METADATA_FULL",
                    "visual_review_state": "VISUAL_FULL" if human_status == "PASS_HUMAN_FULL_REVIEW" else human_status,
                }
            image_records.append(record)
            partition_actual[partition]["image"] += 1
        else:
            raise ValueError(entry["review_mode"])

    duplicates = [
        {"blob_sha1": blob, "paths": sorted(paths)}
        for blob, paths in sorted(blob_paths.items()) if len(paths) > 1
    ]
    partition_records = []
    for partition_id, contract in REVIEW_PARTITIONS.items():
        actual = dict(sorted(partition_actual[partition_id].items()))
        expected = contract["expected"]
        for key, value in expected.items():
            if actual.get(key, 0) != value:
                raise ValueError(f"partition mismatch {partition_id} {key}: {actual.get(key, 0)} != {value}")
        partition_records.append({
            "partition_id": partition_id,
            "manifest_indices": contract["manifest_indices"],
            "review_scope": contract["review_scope"],
            "status": contract["status"],
            "expected": expected,
            "actual": actual,
            "review_evidence": contract["review_evidence"],
            "review_findings": contract["review_findings"],
            "ground_not_found": contract["ground_not_found"],
        })

    topology = {
        "schema_version": 1,
        "generated_date": "2026-08-26",
        "phase": 61,
        "step": "46",
        "artifact_kind": "V1020_SOURCE_TOPOLOGY",
        "authority_boundary": "Source identity, structure and lineage only; no scientific/material/experimental or primary-literature truth promotion.",
        "baseline_commit": BASELINE,
        "manifest": {
            "path": MANIFEST.relative_to(REPO).as_posix(),
            "normalized_sha256": sha256(manifest_bytes),
            "traversal": manifest_traversal,
        },
        "builder": {
            "path": BUILDER.relative_to(REPO).as_posix(),
            "normalized_sha256": sha256(normalize_lf(BUILDER.read_bytes())),
        },
        "counts": {
            "paths": len(sources),
            "unique_blobs": len(blob_paths),
            "text_files": len(text_records),
            "text_physical_lines": sum(row["physical_lines"] for row in text_records),
            "text_nonblank_lines": sum(row["nonblank_lines"] for row in text_records),
            "pdf_files": len(pdf_records),
            "pdf_pages": sum(row["pages_observed"] for row in pdf_records),
            "image_occurrences": len(image_records),
            "same_relative_pairs": len(same_relative),
            "same_relative_identical": sum(row["blob_relation"] == "IDENTICAL" for row in same_relative),
            "same_relative_changed": sum(row["blob_relation"] == "CHANGED" for row in same_relative),
            "v1019_identical_overlap": sum(row["v1019_overlap_class"] == "IDENTICAL_OVERLAP" for row in sources),
            "v1019_new_blob_or_source": sum(row["v1019_overlap_class"] == "NEW_BLOB_OR_SOURCE" for row in sources),
        },
        "path_set_sha256": sha256(("\n".join(sorted(row["path"] for row in sources)) + "\n").encode("utf-8")),
        "path_blob_set_sha256": sha256(("\n".join(f"{row['path']}\t{row['blob_sha1']}" for row in sorted(sources, key=lambda item: item["path"])) + "\n").encode("utf-8")),
        "authority_group_counts": dict(sorted(Counter(row["derived_authority_group"] for row in sources).items())),
        "review_mode_counts": dict(sorted(Counter(row["review_mode"] for row in sources).items())),
        "role_counts": dict(sorted(Counter(row["manifest_role"] for row in sources).items())),
        "extension_counts": dict(sorted(Counter(row["extension"] for row in sources).items())),
        "duplicates": duplicates,
        "same_relative_v1019_v1020": same_relative,
        "sources": sources,
        "status": "PASS_SOURCE_IDENTITY_TOPOLOGY",
    }

    all_human_complete = all(row["status"] == "PASS_HUMAN_FULL_REVIEW" for row in partition_records)
    attestation = {
        "schema_version": 1,
        "generated_date": "2026-08-26",
        "phase": 61,
        "step": "46",
        "artifact_kind": "V1020_READ_ATTESTATION",
        "authority_boundary": "Full read and visual coverage only; structural observations do not establish scientific correctness.",
        "baseline_commit": BASELINE,
        "source_topology_semantic_sha256": sha256(canonical_bytes(topology)),
        "partitions": partition_records,
        "counts": {
            "text_files": len(text_records),
            "text_physical_lines": sum(row["physical_lines"] for row in text_records),
            "text_nonblank_lines": sum(row["nonblank_lines"] for row in text_records),
            "pdf_files": len(pdf_records),
            "pdf_pages": sum(row["pages_observed"] for row in pdf_records),
            "image_occurrences": len(image_records),
            "human_partitions_complete": sum(row["status"] == "PASS_HUMAN_FULL_REVIEW" for row in partition_records),
            "human_partitions_total": len(partition_records),
        },
        "text_records": text_records,
        "pdf_records": pdf_records,
        "image_records": image_records,
        "status": "PASS_FULL_READ_ATTESTATION" if all_human_complete else "PENDING_HUMAN_REVIEW",
    }
    return topology, attestation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    first_topology, first_attestation = build()
    if args.determinism_check:
        second_topology, second_attestation = build()
        if canonical_bytes(first_topology) != canonical_bytes(second_topology):
            print("FAIL STEP46_TOPOLOGY_NONDETERMINISTIC")
            return 1
        if canonical_bytes(first_attestation) != canonical_bytes(second_attestation):
            print("FAIL STEP46_ATTESTATION_NONDETERMINISTIC")
            return 1
    TOPOLOGY.parent.mkdir(parents=True, exist_ok=True)
    TOPOLOGY.write_bytes(pretty_bytes(first_topology))
    ATTESTATION.write_bytes(pretty_bytes(first_attestation))
    print(
        "BUILT_P061_STEP46 "
        f"paths={first_topology['counts']['paths']} "
        f"text={first_attestation['counts']['text_files']}/{first_attestation['counts']['text_physical_lines']} "
        f"pdf={first_attestation['counts']['pdf_files']}/{first_attestation['counts']['pdf_pages']} "
        f"image={first_attestation['counts']['image_occurrences']} "
        f"human={first_attestation['counts']['human_partitions_complete']}/{first_attestation['counts']['human_partitions_total']}"
    )
    if args.determinism_check:
        print("PASS_P061_STEP46_BUILDER_DETERMINISM 2/2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
