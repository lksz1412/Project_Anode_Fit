#!/usr/bin/env python3
"""Build Phase 065 Step 70 source/process topology and read attestation."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "83323ebfff1c468e4ada5e695ced10c69e24fb32"
PHASE057_SOURCE_REF = EXPECTED_PARENT
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_SUBJECT = "audit(phase065): freeze v1024 source process topology"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
RESULT_PATH = "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
TOPOLOGY_PATH = "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION_PATH = "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json"
MANIFEST_START = 826
MANIFEST_STOP = 1087

PATH_SET_SHA256 = "815f37a830da3e5d6539d53bf6dc24c35dec012f39241818b070154b7b729aa7"
PATH_BLOB_SHA256 = "35c224df31807c02ab7d0f8ace3aad7edb36369b6d4d2dd97895589dd5624c0d"
BLOB_SET_SHA256 = "0cc9e04e676dd9c5024842eeaf57180b515bbe2bb7d068dc7aa8eb10c83c8cdd"
RELEASE_SHA256 = "5ab99355b7221e324e022051bb9d9a6d90e8df63907c487b3782257a39954b18"
ROUTED_SHA256 = "3579de45ef774036ae3e74ce2cba2c753c37d43721880a8d5316339c54a95bd4"

AUTHORITY_CEILING = {
    "internal_source_process_topology": True,
    "external_scientific": False,
    "external_material": False,
    "external_experimental": False,
    "external_primary_literature": False,
    "publication_ready": False,
    "canonical_model_selected": False,
    "runtime_behavior_validated": False,
    "defect_repaired": False,
    "v1024_1_independent_corroboration": False,
    "generated_artifact_independent_support": False,
    "source_self_report_is_external_authority": False,
}

MANDATORY_EVIDENCE_GROUPS = (
    "release_scientific_document_text",
    "release_code_test_text",
    "release_pdf",
    "release_image",
    "supplemental_process_text",
    "narrative_history",
    "comp_v24_python",
    "comp_v24_json",
    "comp_v24_csv",
    "comp_v24_txt",
    "comp_v24_png",
    "release_process_all_038",
    "routed_process_ordinals_001_033",
    "routed_process_ordinals_034_066",
    "routed_process_ordinals_067_098",
)

ALLOWED_STATUS_BY_KIND = {
    "FULL_PDF_EXTRACT_RENDER_VISUAL": {"AGENT_FULL_READ"},
    "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL": {"AGENT_FULL_READ"},
    "FULL_TEXT": {"DIRECT_READ", "AGENT_FULL_READ"},
    "FULL_TEXT_AST_NO_IMPORT": {"DIRECT_READ", "AGENT_FULL_READ"},
    "FULL_TEXT_STRICT_JSON": {"DIRECT_READ", "AGENT_FULL_READ"},
    "FULL_TEXT_NUMERIC_DATA": {"DIRECT_READ", "AGENT_FULL_READ"},
    "FULL_PATCH": {"DIRECT_READ", "AGENT_FULL_READ"},
}

FINDING_ROUTE_SCHEMA = {
    "id",
    "severity",
    "status",
    "summary",
    "owner",
    "target_steps",
    "authority_promoted",
}
READER_REPORT_SCHEMA = {
    "reader_id",
    "assignments",
    "report_path",
    "report_section",
    "report_binding_sha256",
    "finding_ids",
    "unreviewed_intervals",
    "output_truncation_unresolved",
}
REQUIRED_FINDING_ROUTE_IDS = {f"P065-S70-F{index:02d}" for index in range(6, 45)}
RESERVED_FINDING_IDS = {f"P065-S70-F{index:02d}" for index in range(1, 6)}

PROCESS_PARTITIONS = {
    "routed_process_ordinals_001_033": {
        "ordinals": [1, 33],
        "commits": 33,
        "patch_bytes": 455844,
        "patch_lines": 7878,
        "canonical_row_binding_sha256": "5e22f38eddbfafa1a19a0a293c2b36780b8b59fc285dc0ce1ddc824878348076",
    },
    "routed_process_ordinals_034_066": {
        "ordinals": [34, 66],
        "commits": 33,
        "patch_bytes": 2655327,
        "patch_lines": 66770,
        "canonical_row_binding_sha256": "a06de2b79da8acdcd8ca1cfb017e1f4e8177706f7f2a90cbd7747debd4ac748e",
    },
    "routed_process_ordinals_067_098": {
        "ordinals": [67, 98],
        "commits": 32,
        "patch_bytes": 9394733,
        "patch_lines": 32153,
        "canonical_row_binding_sha256": "e080af1a80e9907bf53872f5595a61266b0ffc6d7ff557fe51178dfe3f5869ca",
    },
}
ROUTED_PROCESS_CANONICAL_ROW_BINDING_SHA256 = "5c8ff3bc6f9f3570c024c603d363a7663210335ff950f5f279cf4e2fc5240ac2"
READ_ONLY_GIT_SUBCOMMANDS = {"cat-file", "rev-parse", "ls-tree", "log", "diff-tree", "show"}
SEMANTIC_DEFERRED_PATCH_INTERVALS = {70: (226, 3813), 98: (2012, 5599)}

EVIDENCE_BEGIN = "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON"
EVIDENCE_END = "END_P065_STEP70_HUMAN_EVIDENCE_JSON"

RELEASE_PATHS = (
    "Claude/docs/v1.0.24/**",
    "Claude/docs/v1.0.24.1/**",
)
PLAN_PATHS = (
    "Claude/plans/2026-07-18-v1024-completeness-validation-plan.md",
    "Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md",
    "Claude/plans/2026-07-22-v1024-feedback-revision-plan.md",
)
ROOT_ANCHORS = (
    "Claude/results/V1024_EXECUTION_LEDGER.md",
    "Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md",
    "Claude/results/V1024_PROGRESS_SUMMARY.md",
)
ROUTED_PATHS = (*RELEASE_PATHS, *PLAN_PATHS, *ROOT_ANCHORS, "Claude/results/comp_v24/**")
PHASE057_PATHS = (
    "Codex/plans/2026-07-28-phase057-v1024-v1025_2-read-map.md",
    "Codex/results/PHASE_057AG_V1024_R0_SEED_OBSERVATIONS.md",
    "Codex/results/PHASE_057AH_V1024_BRIEF_W1_W3_OBSERVATIONS.md",
    "Codex/results/PHASE_057AI_V1024_W4_W6_OBSERVATIONS.md",
    "Codex/results/PHASE_057AJ_V1024_W7_W9_OBSERVATIONS.md",
    "Codex/results/PHASE_057AK_V1024_REFINE_B_OBSERVATIONS.md",
    "Codex/results/PHASE_057AL_V1024_R1_R3_OBSERVATIONS.md",
    "Codex/results/PHASE_057AM_V1024_HANDOVER_MERGE_OBSERVATIONS.md",
    "Codex/results/PHASE_057AN_V1024_CODE_GUIDE_OBSERVATIONS.md",
    "Codex/results/PHASE_057AX_V1024_HTML_GUIDE_OBSERVATIONS.md",
    "Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md",
)
SUPPLEMENTAL_PATHS = (*PLAN_PATHS, *ROOT_ANCHORS)
MASTERS = {
    "graphite": "Claude/docs/v1.0.24/ch1_graphite_v1.0.24.tex",
    "lco": "Claude/docs/v1.0.24/ch2_lco_v1.0.24.tex",
    "si_blend": "Claude/docs/v1.0.24/ch3_si_v1.0.24.tex",
}

PROCESS_CLASS_ORDINALS = {
    "proposal": {1, 2, 37, 38, 78, 80, 82},
    "competition": {41, 42, 51, 52},
    "review": {4, 5, 6, 7, 8, 9, 12, 13, 15, 16, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 54, 56, 57, 63, 79, 81, 95},
    "patch": {10, 22, 32, 35, 40, 44, 45, 46, 47, 49, 53, 58, 59, 60, 61, 62, 64, 65, 66, 68, 69},
    "build": {34, 36, 39, 50, 55, 70},
    "feedback_revision": {71, 72, 73, 74, 75, 76, 77, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 96, 97},
    "archive": {98},
    "status": {3, 11, 14, 18, 43, 48, 67},
}

OBSERVATION_ROUTES = {
    "P065_STEP70": {228, 235, 243, 251, 272, 282, 292, 388, 389, 390, 391, 395, 396, 404},
    "P065_STEP71": {229, 230, 234, 266, 267, 268, 269, 276, 278, 280, 284, 285, 286, 287, 288, 290, 392, 393},
    "P065_STEP72": {231, 232, 237, 238, 239, 240, 241, 242, 245, 246, 247, 248, 249, 250, 252, 254, 255, 256, 257, 259, 260, 261, 262, 263, 264, 265, 273, 274, 275, 279, 283, 289, 397, 398, 399, 400, 401, 402, 403},
    "P065_STEP73": {230, 234, 266, 267, 268, 269, 270, 271, 275, 276, 277, 278, 279, 280, 284, 285, 286, 287, 288, 289, 396, 397, 398, 399, 400},
    "P065_STEP74": {233, 244, 258, 277, 281, 291, 390, 394, 404},
}


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(f"{code}: {detail}")


def git_read_only_shape(args: tuple[str, ...]) -> bool:
    if not args:
        return False
    command = args[0]
    if command == "cat-file":
        return len(args) == 3 and args[1] == "blob"
    if command == "rev-parse":
        return len(args) == 2
    if command == "ls-tree":
        return len(args) == 6 and args[1:4] == ("-r", "--name-only", BASELINE) and args[4] == "--"
    if command == "log":
        return len(args) >= 6 and args[1:4] == ("--reverse", "--format=%H", BASELINE) and args[4] == "--"
    if command == "diff-tree":
        prefix = ("diff-tree", "--root", "--no-commit-id", "--raw", "--abbrev=40", "--no-renames", "-r")
        return len(args) >= 8 and args[:7] == prefix
    if command == "show":
        if len(args) == 4 and args[1] == "-s" and args[2] in {"--format=%P", "--format=%s"}:
            return True
        prefix = ("show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv", "--find-renames", "--find-copies")
        return len(args) >= 10 and args[:7] == prefix and args[8] == "--"
    return False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def line_count(data: bytes) -> int:
    return len(lf_bytes(data).decode("utf-8").splitlines())


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(value))
    clone.pop("semantic_sha256", None)
    return sha256_bytes(canonical_bytes(clone))


def _reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE_KEY", key)
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise BuildFailure(f"E_JSON_NONFINITE: {token}")


def _walk_json(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        require(abs(value) <= 2**63 - 1, "E_JSON_INTEGER_RANGE", path)
        return
    if isinstance(value, float):
        require(math.isfinite(value), "E_JSON_NONFINITE", path)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _walk_json(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _walk_json(item, f"{path}.{key}")
        return
    raise BuildFailure(f"E_JSON_TYPE: {path}")


def strict_json(data: bytes) -> Any:
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_reject_pairs, parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BuildFailure(f"E_JSON_PARSE: {exc}") from exc
    _walk_json(value)
    return value


def run_process(root: Path, argv: list[str]) -> subprocess.CompletedProcess[bytes]:
    require(bool(argv) and argv[0] == "git", "E_PROCESS_NOT_GIT", repr(argv))
    return subprocess.run(
        argv,
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def run_git(root: Path, *args: str) -> bytes:
    require(bool(args) and all(isinstance(arg, str) for arg in args), "E_GIT_ARGV")
    require(not args[0].startswith("-"), "E_GIT_SUBCOMMAND", args[0])
    require(args[0] in READ_ONLY_GIT_SUBCOMMANDS, "E_GIT_NOT_READ_ONLY", args[0])
    require(git_read_only_shape(tuple(args)), "E_GIT_ARGV_SHAPE", repr(args))
    dangerous = ("-c", "--config-env", "--upload-pack", "--receive-pack", "--exec-path", "--ext-diff", "--textconv")
    dangerous_prefixes = ("--config=", "--config-env=", "--upload-pack=", "--receive-pack=", "--exec-path=")
    require(not any(arg in dangerous or arg.startswith(dangerous_prefixes) or arg.startswith("alias.") or arg.startswith("protocol.") for arg in args), "E_GIT_OPTION")
    require(not any(arg == "-o" or arg.startswith(("--output", "--config=", "--git-dir", "--work-tree")) for arg in args), "E_GIT_WRITE_OPTION")
    require(not any(arg.startswith("ext::") or arg.startswith("file://") for arg in args), "E_GIT_PROTOCOL")
    proc = run_process(root, ["git", *args])
    require(proc.returncode == 0, "E_GIT", f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout


def git_text(root: Path, *args: str) -> str:
    return run_git(root, *args).decode("utf-8").strip()


def git_ref_blob(root: Path, source_ref: str, path: str) -> bytes:
    return run_git(root, "cat-file", "blob", f"{source_ref}:{path}")


def git_blob(root: Path, path: str) -> bytes:
    return git_ref_blob(root, BASELINE, path)


def git_ref_blob_id(root: Path, source_ref: str, path: str) -> str:
    return git_text(root, "rev-parse", f"{source_ref}:{path}")


def git_blob_id(root: Path, path: str) -> str:
    return git_ref_blob_id(root, BASELINE, path)


def git_paths(root: Path, prefix: str) -> list[str]:
    raw = run_git(root, "ls-tree", "-r", "--name-only", BASELINE, "--", prefix)
    return [line for line in raw.decode("utf-8").splitlines() if line]


def hash_rows(rows: Any) -> str:
    return sha256_bytes(canonical_bytes(rows))


def parse_human_evidence(root: Path) -> tuple[dict[str, Any], str]:
    result = (root / RESULT_PATH).read_text(encoding="utf-8")
    require(EVIDENCE_BEGIN in result and EVIDENCE_END in result, "E_HUMAN_EVIDENCE_MARKERS")
    before, tail = result.split(EVIDENCE_BEGIN, 1)
    payload, after = tail.split(EVIDENCE_END, 1)
    require(EVIDENCE_BEGIN not in before + after and EVIDENCE_END not in before + after, "E_HUMAN_EVIDENCE_DUPLICATE_MARKER")
    payload = payload.strip()
    require(payload.startswith("```json") and payload.endswith("```"), "E_HUMAN_EVIDENCE_FENCE")
    body = payload[len("```json"): -len("```")].strip().encode("utf-8")
    evidence = strict_json(body)
    require(isinstance(evidence, dict), "E_HUMAN_EVIDENCE_OBJECT")
    return evidence, sha256_bytes(canonical_bytes(evidence))


def manifest_topology(root: Path) -> dict[str, Any]:
    manifest = strict_json((root / MANIFEST_PATH).read_bytes())
    require(manifest.get("baseline_commit") == BASELINE, "E_MANIFEST_BASELINE")
    source_rows = manifest.get("entries")
    require(isinstance(source_rows, list) and len(source_rows) >= MANIFEST_STOP, "E_MANIFEST_ROWS")
    rows = source_rows[MANIFEST_START:MANIFEST_STOP]
    require(len(rows) == 261, "E_MANIFEST_SLICE")

    paths = [row["path"] for row in rows]
    blobs = [row["blob_sha"] for row in rows]
    require(len(set(paths)) == 261, "E_PATH_UNIQUENESS")
    path_set_hash = sha256_bytes(("\n".join(sorted(paths)) + "\n").encode("utf-8"))
    path_blob_hash = sha256_bytes(("\n".join(f"{row['path']}\0{row['blob_sha']}" for row in sorted(rows, key=lambda item: item["path"])) + "\n").encode("utf-8"))
    blob_set_hash = sha256_bytes(("\n".join(sorted(set(blobs))) + "\n").encode("ascii"))
    require(path_set_hash == PATH_SET_SHA256, "E_PATH_SET_HASH")
    require(path_blob_hash == PATH_BLOB_SHA256, "E_PATH_BLOB_HASH")
    require(blob_set_hash == BLOB_SET_SHA256, "E_BLOB_SET_HASH")

    paths_by_blob: dict[str, list[str]] = defaultdict(list)
    source_by_blob: dict[str, dict[str, Any]] = {}
    for row in rows:
        paths_by_blob[row["blob_sha"]].append(row["path"])
        source_by_blob.setdefault(row["blob_sha"], row)

    unique_sources: list[dict[str, Any]] = []
    for blob in sorted(paths_by_blob):
        row = source_by_blob[blob]
        raw = git_blob(root, sorted(paths_by_blob[blob])[0])
        require(len(raw) == row["size_bytes"], "E_BLOB_SIZE", blob)
        record: dict[str, Any] = {
            "blob": blob,
            "paths": sorted(paths_by_blob[blob]),
            "representative_path": sorted(paths_by_blob[blob], key=lambda path: ("v1.0.24.1" in path, path))[0],
            "role": row["role"],
            "review_mode": row["review_mode"],
            "extent": row["extent"],
            "size_bytes": len(raw),
            "sha256_raw": sha256_bytes(raw),
            "sha256_lf": sha256_bytes(lf_bytes(raw)) if row["review_mode"] == "FULL_TEXT" else None,
            "read_status": "MACHINE_RECONSTRUCTED",
            "read_ranges": [],
            "machine_extent_ranges": [],
        }
        if row["review_mode"] == "FULL_TEXT":
            actual_lines = line_count(raw)
            require(actual_lines == row["extent"]["lines"], "E_TEXT_EXTENT", record["representative_path"])
            record["machine_extent_ranges"] = [[1, actual_lines]] if actual_lines else []
        elif row["review_mode"] == "FULL_PDF":
            pages = len(PdfReader(io.BytesIO(raw)).pages)
            require(pages == row["extent"]["pages"], "E_PDF_EXTENT", record["representative_path"])
            record["machine_extent_ranges"] = [[1, pages]]
        elif row["review_mode"] == "FULL_IMAGE":
            with Image.open(io.BytesIO(raw)) as image:
                width, height = image.size
                mode = image.mode
            record["image"] = {"width": width, "height": height, "mode": mode}
            record["machine_extent_ranges"] = [[1, 1]]
        unique_sources.append(record)

    prefix24 = "Claude/docs/v1.0.24/"
    prefix241 = "Claude/docs/v1.0.24.1/"
    by24 = {row["path"][len(prefix24):]: row for row in rows if row["path"].startswith(prefix24)}
    by241 = {row["path"][len(prefix241):]: row for row in rows if row["path"].startswith(prefix241)}
    common = sorted(set(by24) & set(by241))
    require(len(common) == 130, "E_MIRROR_COMMON")
    require(all(by24[path]["blob_sha"] == by241[path]["blob_sha"] for path in common), "E_MIRROR_BLOBS")
    require(sorted(set(by241) - set(by24)) == ["ARCHIVE_NOTE.md"], "E_ARCHIVE_DELTA")
    require(not (set(by24) - set(by241)), "E_REVERSE_ARCHIVE_DELTA")

    occurrence_rows: list[dict[str, Any]] = []
    root_process_paths = set(root_process_rule(root))
    comp_paths = set(git_paths(root, "Claude/results/comp_v24"))
    for index, row in enumerate(rows, MANIFEST_START):
        relative = row["path"].removeprefix(prefix24).removeprefix(prefix241)
        mirror_path = None
        if relative in common:
            mirror_path = (prefix241 if row["path"].startswith(prefix24) else prefix24) + relative
        routes = ["P065_STEP70_UNIQUE_SOURCE"]
        if row["path"] in root_process_paths:
            routes.append("P065_STEP70_NARRATIVE")
        if row["path"] in comp_paths:
            routes.append("P065_COMP_V24")
        if row["role"] in {"code", "test"}:
            routes.append("P065_STEP71_STATIC")
        if row["extension"] == "tex":
            routes.append("P065_STEP72_SCIENCE")
        occurrence_rows.append({
            "occurrence_index": index,
            "ordinal": index + 1,
            "version": row["version"],
            "path": row["path"],
            "blob": row["blob_sha"],
            "dedup_group": row["dedup_group"],
            "git_mode": row["git_mode"],
            "role": row["role"],
            "review_mode": row["review_mode"],
            "extent": row["extent"],
            "size_bytes": row["size_bytes"],
            "read_status": "MACHINE_RECONSTRUCTED",
            "read_ranges": [],
            "machine_extent_ranges": next(item["machine_extent_ranges"] for item in unique_sources if item["blob"] == row["blob_sha"]),
            "mirror_counterpart": mirror_path,
            "process_routes": routes,
        })

    unique_text = [row for row in unique_sources if row["review_mode"] == "FULL_TEXT"]
    text_lines = sum(row["extent"]["lines"] for row in unique_text)
    pdf_sources = [row for row in unique_sources if row["review_mode"] == "FULL_PDF"]
    image_sources = [row for row in unique_sources if row["review_mode"] == "FULL_IMAGE"]
    manifest_summary = {
        "zero_based_indices": [826, 1086],
        "one_based_ordinals": [827, 1087],
        "occurrences": len(rows),
        "unique_paths": len(set(paths)),
        "versions": dict(sorted(Counter(row["version"] for row in rows).items())),
        "unique_blobs": len(unique_sources),
        "unique_text_blobs": len(unique_text),
        "unique_text_lines": text_lines,
        "unique_pdfs": len(pdf_sources),
        "unique_pdf_pages": sum(row["extent"]["pages"] for row in pdf_sources),
        "unique_images": len(image_sources),
        "unique_bytes": sum(row["size_bytes"] for row in unique_sources),
        "occurrence_bytes": sum(row["size_bytes"] for row in rows),
        "shared_pairs": len(common),
        "path_set_sha256": path_set_hash,
        "path_blob_sha256": path_blob_hash,
        "unique_blob_sha256": blob_set_hash,
        "occurrence_roles": dict(sorted(Counter(row["role"] for row in rows).items())),
        "unique_roles": dict(sorted(Counter(row["role"] for row in source_by_blob.values()).items())),
        "occurrence_review_modes": dict(sorted(Counter(row["review_mode"] for row in rows).items())),
        "unique_review_modes": dict(sorted(Counter(row["review_mode"] for row in unique_sources).items())),
    }
    require(manifest_summary["unique_text_lines"] == 21618, "E_TEXT_TOTAL")
    require(manifest_summary["unique_pdf_pages"] == 148, "E_PDF_TOTAL")
    require(manifest_summary["unique_bytes"] == 7812647, "E_UNIQUE_BYTES")
    require(manifest_summary["occurrence_bytes"] == 15622368, "E_OCCURRENCE_BYTES")
    return {
        "manifest": manifest_summary,
        "occurrences": occurrence_rows,
        "unique_sources": unique_sources,
        "mirror": {
            "shared_relative_paths": len(common),
            "byte_identical_pairs": len(common),
            "pairs": [{"relative_path": path, "v1024_blob": by24[path]["blob_sha"], "v1024_1_blob": by241[path]["blob_sha"]} for path in common],
            "v1024_1_only": ["ARCHIVE_NOTE.md"],
            "independent_corroboration": False,
        },
    }


def record_for_path(root: Path, path: str, source_ref: str) -> dict[str, Any]:
    raw = git_ref_blob(root, source_ref, path)
    blob = git_ref_blob_id(root, source_ref, path)
    return {
        "path": path,
        "source": "git_blob",
        "source_ref": source_ref,
        "blob": blob,
        "lines": line_count(raw),
        "bytes": len(raw),
        "sha256_raw": sha256_bytes(raw),
        "sha256_lf": sha256_bytes(lf_bytes(raw)),
        "read_status": "MACHINE_RECONSTRUCTED",
        "read_ranges": [],
        "machine_extent_ranges": [[1, line_count(raw)]] if line_count(raw) else [],
    }


def root_process_rule(root: Path) -> list[str]:
    release_results = [path for path in git_paths(root, "Claude/docs/v1.0.24/results") if path.endswith(".md")]
    require(len(release_results) == 23, "E_RELEASE_RESULT_MD_COUNT")
    paths = sorted(release_results) + [
        "Claude/docs/v1.0.24/CODE_GUIDE_v24.md",
        "Claude/docs/v1.0.24/FITTING_GUIDE.md",
        "Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md",
        *ROOT_ANCHORS,
    ]
    require(len(paths) == 29 and len(set(paths)) == 29, "E_ROOT_PROCESS_PATHS")
    return paths


def narrative_topology(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    plans = [record_for_path(root, path, BASELINE) for path in PLAN_PATHS]
    root_process = [record_for_path(root, path, BASELINE) for path in root_process_rule(root)]
    comp_md_paths = [path for path in git_paths(root, "Claude/results/comp_v24") if path.endswith(".md")]
    comp_md = [record_for_path(root, path, BASELINE) for path in sorted(comp_md_paths)]
    phase057 = [record_for_path(root, path, PHASE057_SOURCE_REF) for path in PHASE057_PATHS]
    require((len(plans), sum(row["lines"] for row in plans)) == (3, 639), "E_PLAN_NARRATIVE")
    require((len(root_process), sum(row["lines"] for row in root_process)) == (29, 2306), "E_ROOT_PROCESS_NARRATIVE")
    require((len(comp_md), sum(row["lines"] for row in comp_md)) == (31, 2635), "E_COMP_MD_NARRATIVE")
    require((len(phase057), sum(row["lines"] for row in phase057)) == (11, 1890), "E_PHASE057_NARRATIVE")
    records: list[dict[str, Any]] = []
    for partition, rows in (("plans", plans), ("root_process", root_process), ("comp_v24_markdown", comp_md), ("phase057_routing", phase057)):
        for row in rows:
            row["partition"] = partition
            records.append(row)
    require(len(records) == 74 and sum(row["lines"] for row in records) == 7470, "E_NARRATIVE_TOTAL")
    return {
        "copied_activation_claim": {"documents": 29, "lines": 2068},
        "corrected_root_process": {"documents": 29, "lines": 2306},
        "corrected_total": {"documents": 74, "lines": 7470},
        "correction_delta_lines": 238,
        "partition_counts": {
            "plans": {"documents": 3, "lines": 639},
            "root_process": {"documents": 29, "lines": 2306},
            "comp_v24_markdown": {"documents": 31, "lines": 2635},
            "phase057_routing": {"documents": 11, "lines": 1890},
        },
        "records": records,
        "binding_sha256": hash_rows([{"path": row["path"], "lines": row["lines"], "sha256_lf": row["sha256_lf"]} for row in records]),
    }, records


def supplemental_topology(root: Path) -> dict[str, Any]:
    records = [record_for_path(root, path, BASELINE) for path in SUPPLEMENTAL_PATHS]
    require(len(records) == 6 and sum(row["lines"] for row in records) == 728, "E_SUPPLEMENTAL_TOTAL")
    return {
        "documents": 6,
        "lines": 728,
        "records": records,
        "binding_sha256": hash_rows([{"path": row["path"], "blob": row["blob"], "lines": row["lines"], "sha256_lf": row["sha256_lf"]} for row in records]),
    }


def comp_v24_topology(root: Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path in sorted(git_paths(root, "Claude/results/comp_v24")):
        raw = git_blob(root, path)
        extension = PurePosixPath(path).suffix.lower().lstrip(".")
        record: dict[str, Any] = {
            "path": path,
            "blob": git_blob_id(root, path),
            "extension": extension,
            "bytes": len(raw),
            "sha256_raw": sha256_bytes(raw),
            "read_status": "MACHINE_RECONSTRUCTED",
            "read_ranges": [],
        }
        if extension == "png":
            with Image.open(io.BytesIO(raw)) as image:
                record["image"] = {"width": image.width, "height": image.height, "mode": image.mode}
            record["machine_extent_ranges"] = [[1, 1]]
            record["route"] = "P065_STEP72_VISUAL_FIT_EVIDENCE"
        else:
            record["lines"] = line_count(raw)
            record["sha256_lf"] = sha256_bytes(lf_bytes(raw))
            record["machine_extent_ranges"] = [[1, record["lines"]]] if record["lines"] else []
            record["route"] = "P065_STEP70_NARRATIVE" if extension == "md" else "P065_STEP71_STATIC" if extension == "py" else "P065_STEP72_FIT_EVIDENCE"
        records.append(record)
    counts = dict(sorted(Counter(row["extension"] for row in records).items()))
    line_counts = {extension: sum(row.get("lines", 0) for row in records if row["extension"] == extension) for extension in sorted(counts) if extension != "png"}
    expected_counts = {"csv": 10, "json": 16, "md": 31, "png": 33, "py": 29, "txt": 7}
    expected_lines = {"csv": 45203, "json": 1650, "md": 2635, "py": 2932, "txt": 171}
    require(counts == expected_counts, "E_COMP_EXTENSION_COUNTS", repr(counts))
    require(line_counts == expected_lines, "E_COMP_LINE_COUNTS", repr(line_counts))
    return {"extension_counts": counts, "text_line_counts": line_counts, "records": records}


def classify_commit(subject: str, changed_paths: list[dict[str, Any]]) -> str:
    lower = subject.lower()
    joined = " ".join(row["path"].lower() for row in changed_paths)
    if "archive" in lower or "아카이브" in lower:
        return "archive"
    if re.search(r"\bfb[0-9]+\b", lower) or "feedback" in lower or "피드백" in lower:
        return "feedback_revision"
    if "review" in lower or "검토" in lower or "readiness" in joined:
        return "review"
    if "comp" in lower or re.search(r"\bw[1-9]\b", lower) or "competition" in lower or "/comp_r1/" in joined:
        return "competition"
    if "build" in lower or "pdf" in lower or "html" in lower or "render" in lower:
        return "build"
    if any(token in lower for token in ("patch", "fix", "revise", "revision", "correct", "수정", "보강", "추가")):
        return "patch"
    if any(token in lower for token in ("result", "ledger", "status", "summary", "progress", "handover", "결과", "요약", "인계")):
        return "status"
    return "proposal"


def changed_statuses(root: Path, commit: str, pathspecs: tuple[str, ...] | None = None) -> list[dict[str, Any]]:
    args = ["diff-tree", "--root", "--no-commit-id", "--raw", "--abbrev=40", "--no-renames", "-r", commit]
    if pathspecs:
        args.extend(["--", *pathspecs])
    raw = run_git(root, *args)
    rows: list[dict[str, Any]] = []
    for line in raw.decode("utf-8").splitlines():
        if not line:
            continue
        metadata, path = line.split("\t", 1)
        fields = metadata.split()
        require(len(fields) == 5 and fields[0].startswith(":"), "E_PROCESS_RAW_STATUS", f"{commit}:{line}")
        old_mode, new_mode, old_blob, new_blob, status = fields[0][1:], fields[1], fields[2], fields[3], fields[4]
        require(not status.startswith(("R", "C")), "E_PROCESS_RENAME", f"{commit}:{line}")
        rows.append({
            "status": status,
            "path": path,
            "old_mode": old_mode,
            "new_mode": new_mode,
            "old_blob": None if set(old_blob) == {"0"} else old_blob,
            "new_blob": None if set(new_blob) == {"0"} else new_blob,
        })
    return rows


def historical_blob_metadata(root: Path, blob: str | None, path: str) -> dict[str, Any] | None:
    if blob is None:
        return None
    raw = run_git(root, "cat-file", "blob", blob)
    metadata: dict[str, Any] = {
        "git_blob": blob,
        "bytes": len(raw),
        "sha256_raw": sha256_bytes(raw),
    }
    extension = PurePosixPath(path).suffix.lower()
    if extension == ".png":
        with Image.open(io.BytesIO(raw)) as image:
            metadata["image"] = {"width": image.width, "height": image.height, "mode": image.mode}
    elif extension == ".pdf":
        metadata["pdf"] = {"pages": len(PdfReader(io.BytesIO(raw)).pages)}
    return metadata


def process_classification_note(label: str) -> str:
    notes = {
        "proposal": "Planning or proposed-state routing label; no adoption or behavior authority.",
        "competition": "Competing candidate routing label; no final-adoption or scientific authority.",
        "review": "Internal review/survey routing label; self-report does not establish correctness.",
        "patch": "Source-change routing label; changed bytes do not establish runtime or scientific validity.",
        "build": "Build/generated-artifact routing label; artifact existence is not independent support.",
        "feedback_revision": "Editorial/feedback revision routing label; later wording is not back-projected.",
        "archive": "Archive identity routing label; the mirror is not independent corroboration.",
        "status": "Status/self-report routing label; internal completion wording is not external authority.",
    }
    return notes[label]


def process_binding_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "commit": row["commit"],
        "parents": row["parents"],
        "full_commit_changed_paths": row["full_commit_changed_paths"],
        "routed_changed_paths": row["routed_changed_paths"],
        "historical_binary": row["historical_binary"],
        "parent_patches": [{
            "parent": patch["parent"],
            "sha256_raw": patch["sha256_raw"],
            "bytes": patch["bytes"],
            "lines": patch["lines"],
        } for patch in row["parent_patches"]],
    } for row in rows]


def process_rows(
    root: Path,
    pathspecs: tuple[str, ...],
    expected_count: int,
    expected_hash: str,
    cache: dict[tuple[str, tuple[str, ...]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    process_query_argv = ["git", "log", "--reverse", "--format=%H", BASELINE, "--", *pathspecs]
    raw = run_git(root, *process_query_argv[1:])
    commits = [line for line in raw.decode("ascii").splitlines() if line]
    require(len(commits) == expected_count, "E_PROCESS_COUNT", str(expected_count))
    require(sha256_bytes(lf_bytes(raw)) == expected_hash, "E_PROCESS_ORDER_HASH", str(expected_count))
    selected = set(commits)
    rows: list[dict[str, Any]] = []
    class_by_ordinal = {ordinal: label for label, ordinals in PROCESS_CLASS_ORDINALS.items() for ordinal in ordinals}
    require(set(class_by_ordinal) == set(range(1, 99)), "E_PROCESS_CLASS_COVERAGE")
    for ordinal, commit in enumerate(commits, 1):
        cache_key = (commit, pathspecs)
        if cache is not None and cache_key in cache:
            base_record = json.loads(json.dumps(cache[cache_key]))
        else:
            parents = git_text(root, "show", "-s", "--format=%P", commit).split()
            subject = git_text(root, "show", "-s", "--format=%s", commit)
            full_changes = changed_statuses(root, commit)
            routed_changes = changed_statuses(root, commit, pathspecs)
            patches: list[dict[str, Any]] = []
            if parents:
                for parent in parents:
                    patch = run_git(
                        root,
                        "show",
                        "--format=",
                        "--no-color",
                        "--no-ext-diff",
                        "--no-textconv",
                        "--find-renames",
                        "--find-copies",
                        commit,
                        "--",
                        *pathspecs,
                    )
                    patches.append({
                        "parent": parent,
                        "sha256_raw": sha256_bytes(patch),
                        "bytes": len(patch),
                        "lines": len(lf_bytes(patch).splitlines()),
                        "read_status": "MACHINE_RECONSTRUCTED",
                    })
            else:
                patch = run_git(
                    root,
                    "show",
                    "--format=",
                    "--no-color",
                    "--no-ext-diff",
                    "--no-textconv",
                    "--find-renames",
                    "--find-copies",
                    commit,
                    "--",
                    *pathspecs,
                )
                patches.append({
                    "parent": None,
                    "sha256_raw": sha256_bytes(patch),
                    "bytes": len(patch),
                    "lines": len(lf_bytes(patch).splitlines()),
                    "read_status": "MACHINE_RECONSTRUCTED",
                })
            state_class = class_by_ordinal[ordinal] if expected_count == 98 else classify_commit(subject, routed_changes)
            historical_binary = []
            for change in routed_changes:
                if PurePosixPath(change["path"]).suffix.lower() not in {".pdf", ".png"}:
                    continue
                historical_binary.append({
                    "path": change["path"],
                    "status": change["status"],
                    "old": historical_blob_metadata(root, change["old_blob"], change["path"]),
                    "new": historical_blob_metadata(root, change["new_blob"], change["path"]),
                })
            base_record = {
                "commit": commit,
                "parents": parents,
                "subject": subject,
                "full_commit_changed_paths": full_changes,
                "routed_changed_paths": routed_changes,
                "historical_binary": historical_binary,
                "parent_patches": patches,
                "complete_diff_read": False,
                "state_class": state_class,
                "adoption_authority": "PROCESS_EVIDENCE_ONLY",
                "classification_basis": "PROVISIONAL_ORDINAL_ROUTING_AWAITING_HUMAN_EVIDENCE" if expected_count == 98 else "SUBJECT_AND_ROUTED_PATH_HEURISTIC",
                "classification_notes": process_classification_note(state_class),
                "patch_scope": list(pathspecs),
            }
            if cache is not None:
                cache[cache_key] = json.loads(json.dumps(base_record))
        base_record["ordinal"] = ordinal
        base_record["predecessors"] = [parent for parent in base_record["parents"] if parent in selected]
        base_record["successors"] = []
        rows.append(base_record)
    by_commit = {row["commit"]: row for row in rows}
    for row in rows:
        for predecessor in row["predecessors"]:
            by_commit[predecessor]["successors"].append(row["commit"])
    binding = process_binding_records(rows)
    canonical_patch_rows = [{
        "ordinal": row["ordinal"],
        "commit": row["commit"],
        "parents": row["parents"],
        "sha256_raw": row["parent_patches"][0]["sha256_raw"],
        "bytes": row["parent_patches"][0]["bytes"],
        "lines": row["parent_patches"][0]["lines"],
    } for row in rows]
    require(all(len(row["parent_patches"]) == 1 for row in rows), "E_PROCESS_CANONICAL_SINGLE_PATCH")
    canonical_row_binding = hash_rows(canonical_patch_rows)
    if expected_count == 98:
        require(sum(row["bytes"] for row in canonical_patch_rows) == 12505904, "E_ROUTED_CANONICAL_BYTES")
        require(sum(row["lines"] for row in canonical_patch_rows) == 106801, "E_ROUTED_CANONICAL_LINES")
        require(canonical_row_binding == ROUTED_PROCESS_CANONICAL_ROW_BINDING_SHA256, "E_ROUTED_CANONICAL_ROW_BINDING", canonical_row_binding)
        for group_id, partition in PROCESS_PARTITIONS.items():
            first, last = partition["ordinals"]
            subset = canonical_patch_rows[first - 1:last]
            require(len(subset) == partition["commits"], "E_PROCESS_PARTITION_COUNT", group_id)
            require(sum(row["bytes"] for row in subset) == partition["patch_bytes"], "E_PROCESS_PARTITION_BYTES", group_id)
            require(sum(row["lines"] for row in subset) == partition["patch_lines"], "E_PROCESS_PARTITION_LINES", group_id)
            require(hash_rows(subset) == partition["canonical_row_binding_sha256"], "E_PROCESS_PARTITION_BINDING", group_id)
    return {
        "query": list(pathspecs),
        "process_query_argv": process_query_argv,
        "count": len(rows),
        "merge_commits": sum(len(row["parents"]) > 1 for row in rows),
        "patch_bytes": sum(patch["bytes"] for row in rows for patch in row["parent_patches"]),
        "patch_lines": sum(patch["lines"] for row in rows for patch in row["parent_patches"]),
        "ordered_sha256": expected_hash,
        "first": commits[0],
        "last": commits[-1],
        "commits": rows,
        "patch_binding_sha256": hash_rows(binding),
        "patch_binding_schema": "machine-process-projection-v1",
        "canonical_patch_rows": canonical_patch_rows,
        "canonical_patch_row_schema": ["ordinal", "commit", "parents", "sha256_raw", "bytes", "lines"],
        "canonical_patch_row_binding_sha256": canonical_row_binding,
    }


def reconcile_process_classifications(release: dict[str, Any], routed: dict[str, Any]) -> None:
    routed_by_commit = {row["commit"]: row for row in routed["commits"]}
    for routed_row in routed["commits"]:
        routed_row["classification_basis"] = "CANONICAL_ROUTED_ORDINAL_WITH_SUBJECT_PATHS_BINARY_PATCH_CONTEXT"
    for release_row in release["commits"]:
        canonical = routed_by_commit.get(release_row["commit"])
        require(canonical is not None, "E_RELEASE_NOT_ROUTED", release_row["commit"])
        for field in ("state_class", "classification_basis", "classification_notes"):
            release_row[field] = canonical[field]


def require_process_projection_consistency(release: dict[str, Any], routed: dict[str, Any]) -> None:
    routed_by_commit = {row["commit"]: row for row in routed["commits"]}
    for release_row in release["commits"]:
        routed_row = routed_by_commit.get(release_row["commit"])
        require(routed_row is not None, "E_RELEASE_NOT_ROUTED", release_row["commit"])
        require(
            all(release_row[field] == routed_row[field] for field in ("state_class", "classification_basis", "classification_notes")),
            "E_PROCESS_CLASSIFICATION_PROJECTION_DRIFT",
            release_row["commit"],
        )


def reviewed_process_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "ordinal": row["ordinal"],
        "commit": row["commit"],
        "subject": row["subject"],
        "state_class": row["state_class"],
        "classification_basis": row["classification_basis"],
        "classification_notes": row["classification_notes"],
        "full_commit_changed_paths": row["full_commit_changed_paths"],
        "routed_changed_paths": row["routed_changed_paths"],
        "historical_binary": row["historical_binary"],
        "parent_patches": [{
            "parent": patch["parent"],
            "sha256_raw": patch["sha256_raw"],
            "bytes": patch["bytes"],
            "lines": patch["lines"],
        } for patch in row["parent_patches"]],
        "patch_scope": row["patch_scope"],
    } for row in rows]


def strip_tex_comments(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        output: list[str] = []
        index = 0
        while index < len(line):
            if line[index] == "%" and (index == 0 or line[index - 1] != "\\"):
                break
            output.append(line[index])
            index += 1
        cleaned.append("".join(output))
    return "\n".join(cleaned)


def resolve_tex_target(source_path: str, target: str, known: set[str]) -> str:
    target = target.strip()
    if not target.endswith(".tex"):
        target += ".tex"
    candidate = str(PurePosixPath(source_path).parent / target)
    normalized = str(PurePosixPath(candidate))
    require(normalized in known, "E_TEX_INCLUDE_UNRESOLVED", f"{source_path}->{target}")
    return normalized


def tex_topology(root: Path, unique_sources: list[dict[str, Any]]) -> dict[str, Any]:
    tex_sources = [row for row in unique_sources if row["representative_path"].endswith(".tex")]
    require(len(tex_sources) == 90, "E_TEX_COUNT")
    tex_by_path = {row["representative_path"]: row for row in tex_sources}
    known = set(tex_by_path)
    include_edges: list[dict[str, str]] = []
    xref_edges: list[dict[str, str]] = []
    include_pattern = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
    xref_pattern = re.compile(r"\\externaldocument(?:\[[^\]]*\])?\s*\{([^}]+)\}")
    for path in sorted(known):
        text = strip_tex_comments(git_blob(root, path).decode("utf-8"))
        for match in include_pattern.finditer(text):
            include_edges.append({"source": path, "target": resolve_tex_target(path, match.group(1), known), "kind": "include"})
        for match in xref_pattern.finditer(text):
            target = match.group(1).strip()
            if not target.endswith(".tex"):
                target += ".tex"
            target_path = str(PurePosixPath(path).parent / target)
            xref_edges.append({"source": path, "target": str(PurePosixPath(target_path)), "kind": "externaldocument"})
    require(len(include_edges) == 55, "E_TEX_INCLUDE_COUNT", str(len(include_edges)))
    require(len(xref_edges) == 4, "E_TEX_XREF_COUNT", str(len(xref_edges)))
    children: dict[str, list[str]] = defaultdict(list)
    for edge in include_edges:
        children[edge["source"]].append(edge["target"])

    closures: dict[str, dict[str, Any]] = {}
    adopted: set[str] = set()
    expected = {"graphite": (34, 5625), "lco": (13, 1618), "si_blend": (11, 1143)}
    for name, master in MASTERS.items():
        seen: set[str] = set()
        stack = [master]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(children[current])
        lines = sum(tex_by_path[path]["extent"]["lines"] for path in seen)
        require((len(seen), lines) == expected[name], "E_TEX_CLOSURE", name)
        adopted.update(seen)
        closures[name] = {
            "master": master,
            "files": len(seen),
            "lines": lines,
            "paths": sorted(seen),
            "path_set_sha256": sha256_bytes(("\n".join(sorted(seen)) + "\n").encode("utf-8")),
        }
    adopted_lines = sum(tex_by_path[path]["extent"]["lines"] for path in adopted)
    non_master = sorted(known - adopted)
    non_master_lines = sum(tex_by_path[path]["extent"]["lines"] for path in non_master)
    require((len(adopted), adopted_lines) == (56, 8218), "E_TEX_ADOPTED_UNION")
    require((len(non_master), non_master_lines) == (34, 4489), "E_TEX_NONMASTER")
    return {
        "unique_tex": {"files": 90, "lines": sum(row["extent"]["lines"] for row in tex_sources)},
        "include_edges": sorted(include_edges, key=lambda row: (row["source"], row["target"])),
        "cross_reference_edges": sorted(xref_edges, key=lambda row: (row["source"], row["target"])),
        "adopted_closures": closures,
        "adopted_union": {"files": len(adopted), "lines": adopted_lines},
        "non_master": {"files": len(non_master), "lines": non_master_lines},
        "non_master_paths": non_master,
        "non_master_path_set_sha256": sha256_bytes(("\n".join(non_master) + "\n").encode("utf-8")),
    }


def derived_topology(root: Path, unique_sources: list[dict[str, Any]], tex: dict[str, Any]) -> list[dict[str, Any]]:
    by_suffix = {PurePosixPath(row["representative_path"]).name: row for row in unique_sources}
    pdf_specs = (
        ("ch1_graphite_v1.0.24.pdf", MASTERS["graphite"], "graphite"),
        ("ch2_lco_v1.0.24.pdf", MASTERS["lco"], "lco"),
        ("ch3_si_v1.0.24.pdf", MASTERS["si_blend"], "si_blend"),
    )
    records: list[dict[str, Any]] = []
    for name, source, closure in pdf_specs:
        artifact = by_suffix[name]
        records.append({
            "artifact_path": artifact["representative_path"],
            "artifact_blob": artifact["blob"],
            "kind": "PDF",
            "source": source,
            "source_closure": tex["adopted_closures"][closure]["paths"],
            "producer": "XeLaTeX/dvipdfmx according to source comments and PDF metadata",
            "producer_state": "COMMAND_GROUND_NOT_FOUND",
            "first_final_commit": "b109707fbacf7a3e2b64bdc2d69aae3ada761ece",
            "independent_support": False,
        })
    html = by_suffix["CODE_GUIDE_v24.html"]
    records.append({
        "artifact_path": html["representative_path"],
        "artifact_blob": html["blob"],
        "kind": "HTML",
        "source": "Claude/docs/v1.0.24/CODE_GUIDE_v24.md",
        "producer": None,
        "producer_state": "GROUND_NOT_FOUND",
        "evidence": "HTML line 219 source declaration; MD/HTML co-change at 1ee23c53fec14c41a1f5372a19e6b2f70adb0de0",
        "independent_support": False,
    })
    image_specs = (
        ("final_sample_core.png", "Claude/docs/v1.0.24/results/v1024_final_sample.py", "lines 9-12 and 68"),
        ("final_sample_reflect.png", "Claude/docs/v1.0.24/results/v1024_final_sample.py", "lines 9-12 and 102"),
        ("reflect_curves.png", "Claude/docs/v1.0.24/results/v1024_reflect_curves.py", "lines 7, 9, and 40"),
    )
    for name, source, anchors in image_specs:
        artifact = by_suffix[name]
        records.append({
            "artifact_path": artifact["representative_path"],
            "artifact_blob": artifact["blob"],
            "kind": "PNG",
            "source": source,
            "producer": source,
            "producer_state": "STATIC_SOURCE_BOUND_NONPORTABLE_NOT_EXECUTED",
            "evidence": anchors,
            "absolute_historical_path_present": True,
            "independent_support": False,
        })
    require(len(records) == 7, "E_DERIVED_COUNT")
    return records


def observation_topology(root: Path) -> dict[str, Any]:
    found: dict[int, dict[str, Any]] = {}
    source_documents = [record_for_path(root, path, PHASE057_SOURCE_REF) for path in PHASE057_PATHS]
    source_by_path = {row["path"]: row for row in source_documents}
    pattern = re.compile(r"^###\s+INTENT-PROV-(\d{4})\s+—\s+(.+)$")
    for path in PHASE057_PATHS:
        lines = git_ref_blob(root, PHASE057_SOURCE_REF, path).decode("utf-8").splitlines()
        for line_number, line in enumerate(lines, 1):
            match = pattern.match(line)
            if not match:
                continue
            numeric = int(match.group(1))
            require(numeric not in found, "E_OBSERVATION_DUPLICATE", str(numeric))
            found[numeric] = {
                "id": f"INTENT-PROV-{numeric:04d}",
                "numeric_id": numeric,
                "title": match.group(2),
                "source_path": path,
                "source_ref": PHASE057_SOURCE_REF,
                "source_blob": source_by_path[path]["blob"],
                "heading_line": line_number,
            }
    expected = set(range(228, 293)) | set(range(388, 405))
    require(set(found) == expected and len(found) == 82, "E_OBSERVATION_DENOMINATOR")
    downstream = {
        234: ["d7d894"],
        244: ["9f713d"],
        269: ["d7d894"],
        278: ["3821b5"],
        279: ["e4c3cf"],
        281: ["9f713d"],
    }
    open_ids = {230, 266, 267, 284, 285, 286, 390, 392, 393, 395, 397, 398, 399, 400, 401, 402, 403}
    records: list[dict[str, Any]] = []
    for numeric in sorted(found):
        routes = [step for step, ids in OBSERVATION_ROUTES.items() if numeric in ids]
        routes.append("P065_STEP75_DISPOSITION")
        row = found[numeric]
        row["routes"] = routes
        row["downstream_correction_commits"] = downstream.get(numeric, [])
        row["back_projection_forbidden"] = bool(row["downstream_correction_commits"])
        row["open_in_v1024_mirror"] = numeric in open_ids
        records.append(row)
    require(all(row["routes"] for row in records), "E_OBSERVATION_ROUTE")
    return {
        "count": 82,
        "ranges": ["INTENT-PROV-0228–0292", "INTENT-PROV-0388–0404"],
        "records": records,
        "source_documents": source_documents,
        "source_document_binding_sha256": hash_rows(source_documents),
        "binding_sha256": hash_rows(records),
        "later_corrections_are_original_evidence": False,
    }


def make_evidence_binding(
    group_id: str,
    kind: str,
    records: list[dict[str, Any]],
    summary: dict[str, Any],
) -> dict[str, Any]:
    identities: list[str] = []
    for record in records:
        if "path" in record:
            identities.append(f"path:{record['path']}")
        elif "blob" in record:
            identities.append(f"blob:{record['blob']}")
        elif "ordinal" in record:
            identities.append(f"ordinal:{record['ordinal']}")
        else:
            raise BuildFailure(f"E_EVIDENCE_RECORD_IDENTITY: {group_id}")
    require(len(identities) == len(set(identities)), "E_EVIDENCE_RECORD_DUPLICATE", group_id)
    manifest_sha256 = hash_rows(records)
    value = {
        "group_id": group_id,
        "kind": kind,
        "record_count": len(records),
        "record_manifest_sha256": manifest_sha256,
        "summary": summary,
    }
    value["binding_sha256"] = hash_rows({"binding": value, "records": records})
    return value


def lf_interval(raw: bytes, first: int, last: int) -> tuple[bytes, int]:
    lines = lf_bytes(raw).splitlines(keepends=True)
    require(1 <= first <= last <= len(lines), "E_SEMANTIC_INTERVAL_RANGE", f"{first}-{last}/{len(lines)}")
    return b"".join(lines[first - 1:last]), len(lines)


def semantic_deferred_intervals(root: Path, core: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    html_path = "Claude/docs/v1.0.24/CODE_GUIDE_v24.html"
    html_raw = git_ref_blob(root, BASELINE, html_path)
    html_slice, html_lines = lf_interval(html_raw, 220, 3807)
    html_record = {
        "interval_id": "release-code-guide-html-mermaid-lines-220-3807",
        "group_id": "release_scientific_document_text",
        "subject_type": "GIT_BLOB_TEXT_INTERVAL",
        "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
        "source_ref": BASELINE,
        "path": html_path,
        "blob": git_ref_blob_id(root, BASELINE, html_path),
        "full_bytes": len(html_raw),
        "full_lines": html_lines,
        "full_sha256_raw": sha256_bytes(html_raw),
        "full_sha256_lf": sha256_bytes(lf_bytes(html_raw)),
        "line_range": [220, 3807],
        "interval_bytes_lf": len(html_slice),
        "interval_lines": 3588,
        "interval_sha256_lf": sha256_bytes(html_slice),
    }
    routed_rows = {row["ordinal"]: row for row in core["process"]["routed"]["commits"]}
    process_records: list[dict[str, Any]] = []
    for ordinal, (first, last) in SEMANTIC_DEFERRED_PATCH_INTERVALS.items():
        row = routed_rows[ordinal]
        patch = run_git(
            root, "show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv",
            "--find-renames", "--find-copies", row["commit"], "--", *ROUTED_PATHS,
        )
        interval, patch_lines = lf_interval(patch, first, last)
        require(row["parent_patches"][0]["sha256_raw"] == sha256_bytes(patch), "E_SEMANTIC_PATCH_IDENTITY", str(ordinal))
        process_records.append({
            "interval_id": f"routed-process-ordinal-{ordinal:03d}-minified-lines-{first}-{last}",
            "group_id": "routed_process_ordinals_067_098",
            "subject_type": "GIT_PATCH_TEXT_INTERVAL",
            "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
            "source_ref": BASELINE,
            "ordinal": ordinal,
            "commit": row["commit"],
            "parent": row["parent_patches"][0]["parent"],
            "patch_sha256_raw": sha256_bytes(patch),
            "patch_bytes": len(patch),
            "patch_lines": patch_lines,
            "line_range": [first, last],
            "interval_bytes_lf": len(interval),
            "interval_lines": last - first + 1,
            "interval_sha256_lf": sha256_bytes(interval),
        })
    return {
        "release_scientific_document_text": [html_record],
        "routed_process_ordinals_067_098": process_records,
    }


def evidence_bindings(root: Path, core: dict[str, Any]) -> dict[str, Any]:
    unique = core["unique_sources"]
    code_tests = [row for row in unique if row["review_mode"] == "FULL_TEXT" and row["representative_path"].endswith(".py")]
    code_test_blobs = {row["blob"] for row in code_tests}
    document_text = [row for row in unique if row["review_mode"] == "FULL_TEXT" and row["blob"] not in code_test_blobs]
    pdfs = [row for row in unique if row["review_mode"] == "FULL_PDF"]
    images = [row for row in unique if row["review_mode"] == "FULL_IMAGE"]

    def source_text_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{
            "blob": row["blob"],
            "source_ref": BASELINE,
            "paths": row["paths"],
            "bytes": row["size_bytes"],
            "lines": row["extent"]["lines"],
            "line_ranges": row["machine_extent_ranges"],
            "sha256_raw": row["sha256_raw"],
            "sha256_lf": row["sha256_lf"],
        } for row in sorted(rows, key=lambda item: item["blob"])]

    def path_text_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{
            "path": row["path"],
            "source_ref": row.get("source_ref", BASELINE),
            "blob": row["blob"],
            "bytes": row["bytes"],
            "lines": row["lines"],
            "line_ranges": row["machine_extent_ranges"],
            "sha256_raw": row["sha256_raw"],
            "sha256_lf": row["sha256_lf"],
        } for row in sorted(rows, key=lambda item: item["path"])]

    deferred = semantic_deferred_intervals(root, core)
    bindings: dict[str, Any] = {}
    records = source_text_records(document_text)
    bindings["release_scientific_document_text"] = make_evidence_binding(
        "release_scientific_document_text", "FULL_TEXT", records,
        {"blobs": len(records), "lines": sum(row["extent"]["lines"] for row in document_text), "semantic_deferred_intervals": deferred["release_scientific_document_text"]},
    )
    records = source_text_records(code_tests)
    bindings["release_code_test_text"] = make_evidence_binding(
        "release_code_test_text", "FULL_TEXT_AST_NO_IMPORT", records,
        {"blobs": len(records), "lines": sum(row["extent"]["lines"] for row in code_tests)},
    )
    records = [{
        "blob": row["blob"],
        "paths": row["paths"],
        "bytes": row["size_bytes"],
        "page_ranges": row["machine_extent_ranges"],
        "pages": row["extent"]["pages"],
        "sha256_raw": row["sha256_raw"],
    } for row in sorted(pdfs, key=lambda item: item["blob"])]
    bindings["release_pdf"] = make_evidence_binding(
        "release_pdf", "FULL_PDF_EXTRACT_RENDER_VISUAL", records,
        {"documents": len(records), "pages": sum(row["extent"]["pages"] for row in pdfs)},
    )
    records = [{
        "blob": row["blob"],
        "paths": row["paths"],
        "bytes": row["size_bytes"],
        "image_ranges": row["machine_extent_ranges"],
        "image": row["image"],
        "sha256_raw": row["sha256_raw"],
    } for row in sorted(images, key=lambda item: item["blob"])]
    bindings["release_image"] = make_evidence_binding(
        "release_image", "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL", records,
        {"images": len(records)},
    )
    records = path_text_records(core["supplemental"]["records"])
    bindings["supplemental_process_text"] = make_evidence_binding(
        "supplemental_process_text", "FULL_TEXT", records,
        {"documents": len(records), "lines": sum(row["lines"] for row in core["supplemental"]["records"])},
    )
    records = path_text_records(core["narrative"]["records"])
    bindings["narrative_history"] = make_evidence_binding(
        "narrative_history", "FULL_TEXT", records,
        {"documents": len(records), "lines": sum(row["lines"] for row in core["narrative"]["records"])},
    )

    for extension, group_id, kind in (
        ("py", "comp_v24_python", "FULL_TEXT_AST_NO_IMPORT"),
        ("json", "comp_v24_json", "FULL_TEXT_STRICT_JSON"),
        ("csv", "comp_v24_csv", "FULL_TEXT_NUMERIC_DATA"),
        ("txt", "comp_v24_txt", "FULL_TEXT"),
        ("png", "comp_v24_png", "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL"),
    ):
        comp_rows = [row for row in core["comp_v24"]["records"] if row["extension"] == extension]
        if extension == "png":
            records = [{
                "path": row["path"],
                "blob": row["blob"],
                "bytes": row["bytes"],
                "image_ranges": row["machine_extent_ranges"],
                "image": row["image"],
                "sha256_raw": row["sha256_raw"],
            } for row in sorted(comp_rows, key=lambda item: item["path"])]
            summary = {"files": len(records), "images": len(records)}
        else:
            records = path_text_records(comp_rows)
            summary = {"files": len(records), "lines": sum(row["lines"] for row in comp_rows)}
        bindings[group_id] = make_evidence_binding(group_id, kind, records, summary)

    release_rows = reviewed_process_records(core["process"]["release"]["commits"])
    bindings["release_process_all_038"] = make_evidence_binding(
        "release_process_all_038", "FULL_PATCH", release_rows,
        {
            "commits": 38,
            "patch_bytes": sum(row["bytes"] for row in core["process"]["release"]["canonical_patch_rows"]),
            "patch_lines": sum(row["lines"] for row in core["process"]["release"]["canonical_patch_rows"]),
            "canonical_row_binding_sha256": core["process"]["release"]["canonical_patch_row_binding_sha256"],
            "reviewed_record_schema": "subject-paths-binary-classification-patch-v1",
        },
    )
    routed_rows = reviewed_process_records(core["process"]["routed"]["commits"])
    for group_id, partition in PROCESS_PARTITIONS.items():
        first, last = partition["ordinals"]
        records = routed_rows[first - 1:last]
        canonical_records = core["process"]["routed"]["canonical_patch_rows"][first - 1:last]
        bindings[group_id] = make_evidence_binding(
            group_id, "FULL_PATCH", records,
            {
                "ordinals": [first, last],
                "commits": len(records),
                "patch_bytes": sum(row["bytes"] for row in canonical_records),
                "patch_lines": sum(row["lines"] for row in canonical_records),
                "canonical_row_binding_sha256": PROCESS_PARTITIONS[group_id]["canonical_row_binding_sha256"],
                "all_98_canonical_row_binding_sha256": core["process"]["routed"]["canonical_patch_row_binding_sha256"],
                "reviewed_record_schema": "subject-paths-binary-classification-patch-v1",
                "semantic_deferred_intervals": deferred.get(group_id, []),
            },
        )
    require(tuple(bindings) == MANDATORY_EVIDENCE_GROUPS, "E_EVIDENCE_GROUP_ORDER", repr(tuple(bindings)))
    return bindings


def build_core(root: Path) -> dict[str, Any]:
    source = manifest_topology(root)
    narrative, _ = narrative_topology(root)
    supplemental = supplemental_topology(root)
    comp = comp_v24_topology(root)
    process_cache: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}
    routed = process_rows(root, ROUTED_PATHS, 98, ROUTED_SHA256, process_cache)
    release = process_rows(root, RELEASE_PATHS, 38, RELEASE_SHA256, process_cache)
    reconcile_process_classifications(release, routed)
    require_process_projection_consistency(release, routed)
    tex = tex_topology(root, source["unique_sources"])
    derived = derived_topology(root, source["unique_sources"], tex)
    observations = observation_topology(root)
    return {
        **source,
        "narrative": narrative,
        "supplemental": supplemental,
        "comp_v24": comp,
        "process": {"release": release, "routed": routed},
        "tex": tex,
        "derived_artifacts": derived,
        "phase057_observations": observations,
    }


def validate_evidence(evidence: dict[str, Any], bindings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    require(evidence.get("schema_version") == "P065-S70-HUMAN-EVIDENCE-1", "E_EVIDENCE_SCHEMA")
    require(evidence.get("baseline_commit") == BASELINE, "E_EVIDENCE_BASELINE")
    require(evidence.get("bindings") == bindings, "E_EVIDENCE_BINDINGS")
    require(evidence.get("unreviewed_intervals") == [], "E_EVIDENCE_UNREVIEWED")
    require(evidence.get("output_truncation_unresolved") == [], "E_EVIDENCE_TRUNCATION")
    require(evidence.get("authority") == AUTHORITY_CEILING, "E_EVIDENCE_AUTHORITY")
    readers = evidence.get("readers")
    require(isinstance(readers, list) and len(readers) >= 3, "E_EVIDENCE_READERS")
    reader_ids = [reader.get("reader_id") for reader in readers]
    require(all(isinstance(reader_id, str) and reader_id for reader_id in reader_ids), "E_EVIDENCE_READER_IDS")
    require(len(reader_ids) == len(set(reader_ids)), "E_EVIDENCE_READER_ID_DUPLICATE")
    require(all(reader.get("unreviewed_intervals") == [] for reader in readers), "E_EVIDENCE_READER_INTERVALS")
    require(all(reader.get("output_truncation_unresolved") == [] for reader in readers), "E_EVIDENCE_READER_TRUNCATION")

    assignments: dict[str, dict[str, Any]] = {}
    reader_finding_ids: list[str] = []
    for reader in readers:
        require(set(reader) == READER_REPORT_SCHEMA, "E_EVIDENCE_READER_REPORT_SCHEMA", str(reader.get("reader_id")))
        require(reader.get("report_path") == RESULT_PATH, "E_EVIDENCE_READER_REPORT_PATH", str(reader.get("reader_id")))
        require(reader.get("report_section") == EVIDENCE_BEGIN, "E_EVIDENCE_READER_REPORT_SECTION", str(reader.get("reader_id")))
        report_payload = {key: value for key, value in reader.items() if key != "report_binding_sha256"}
        require(reader.get("report_binding_sha256") == sha256_bytes(canonical_bytes(report_payload)), "E_EVIDENCE_READER_REPORT_BINDING", str(reader.get("reader_id")))
        finding_ids_for_reader = reader.get("finding_ids")
        require(isinstance(finding_ids_for_reader, list), "E_EVIDENCE_READER_FINDING_IDS", str(reader.get("reader_id")))
        require(len(finding_ids_for_reader) == len(set(finding_ids_for_reader)), "E_EVIDENCE_READER_FINDING_DUPLICATE", str(reader.get("reader_id")))
        require(set(finding_ids_for_reader) <= REQUIRED_FINDING_ROUTE_IDS, "E_EVIDENCE_READER_FINDING_UNKNOWN", str(reader.get("reader_id")))
        reader_finding_ids.extend(finding_ids_for_reader)
        reader_assignments = reader.get("assignments")
        require(isinstance(reader_assignments, list) and reader_assignments, "E_EVIDENCE_READER_ASSIGNMENTS", str(reader.get("reader_id")))
        for assignment in reader_assignments:
            require(set(assignment) == {"group_id", "record_count", "record_manifest_sha256", "binding_sha256", "status"}, "E_EVIDENCE_ASSIGNMENT_SCHEMA", repr(assignment))
            group_id = assignment["group_id"]
            require(group_id in bindings, "E_EVIDENCE_ASSIGNMENT_EXTRA", str(group_id))
            require(group_id not in assignments, "E_EVIDENCE_ASSIGNMENT_DUPLICATE", str(group_id))
            expected = bindings[group_id]
            require(assignment["record_count"] == expected["record_count"], "E_EVIDENCE_ASSIGNMENT_COUNT", group_id)
            require(assignment["record_manifest_sha256"] == expected["record_manifest_sha256"], "E_EVIDENCE_ASSIGNMENT_MANIFEST", group_id)
            require(assignment["binding_sha256"] == expected["binding_sha256"], "E_EVIDENCE_ASSIGNMENT_BINDING", group_id)
            allowed_status = ALLOWED_STATUS_BY_KIND.get(expected["kind"])
            require(allowed_status is not None, "E_EVIDENCE_BINDING_KIND", expected["kind"])
            require(assignment["status"] in allowed_status, "E_EVIDENCE_ASSIGNMENT_STATUS", group_id)
            assignments[group_id] = {**assignment, "reader_id": reader["reader_id"]}
    require(set(assignments) == set(MANDATORY_EVIDENCE_GROUPS), "E_EVIDENCE_ASSIGNMENT_COVERAGE", repr(sorted(set(MANDATORY_EVIDENCE_GROUPS) - set(assignments))))
    require(len(reader_finding_ids) == len(set(reader_finding_ids)), "E_EVIDENCE_READER_FINDING_CROSS_DUPLICATE")
    require(set(reader_finding_ids) == REQUIRED_FINDING_ROUTE_IDS, "E_EVIDENCE_READER_FINDING_COVERAGE")

    expected_deferred = sorted(
        (
            interval
            for binding in bindings.values()
            for interval in binding["summary"].get("semantic_deferred_intervals", [])
        ),
        key=lambda row: row["interval_id"],
    )
    provided_deferred = evidence.get("semantic_deferred_intervals")
    require(provided_deferred == expected_deferred, "E_EVIDENCE_SEMANTIC_DEFERRED")

    require(evidence.get("pdf_visual", {}).get("pages_extracted") == 148, "E_EVIDENCE_PDF_EXTRACTED")
    require(evidence.get("pdf_visual", {}).get("pages_rendered") == 148, "E_EVIDENCE_PDF_RENDERED")
    require(evidence.get("pdf_visual", {}).get("pages_visual") == 148, "E_EVIDENCE_PDF_VISUAL")
    require(evidence.get("image_visual", {}).get("original_resolution_visual") == 3, "E_EVIDENCE_IMAGE_VISUAL")
    require(evidence.get("process_patch_read", {}).get("release") == 38, "E_EVIDENCE_RELEASE_PATCH")
    require(evidence.get("process_patch_read", {}).get("routed") == 98, "E_EVIDENCE_ROUTED_PATCH")
    require(evidence.get("narrative_correction_acknowledged") == {"copied_lines": 2068, "reconstructed_lines": 2306, "delta": 238}, "E_EVIDENCE_CORRECTION")
    finding_routes = evidence.get("finding_routes")
    require(isinstance(finding_routes, list) and len(finding_routes) == len(REQUIRED_FINDING_ROUTE_IDS), "E_EVIDENCE_FINDINGS")
    require(all(isinstance(row, dict) and set(row) == FINDING_ROUTE_SCHEMA for row in finding_routes), "E_EVIDENCE_FINDING_SCHEMA")
    finding_ids = [row.get("id") for row in finding_routes]
    require(len(finding_ids) == len(set(finding_ids)), "E_EVIDENCE_FINDING_IDS")
    require(not RESERVED_FINDING_IDS.intersection(finding_ids), "E_EVIDENCE_FINDING_RESERVED")
    require(set(finding_ids) == REQUIRED_FINDING_ROUTE_IDS, "E_EVIDENCE_FINDING_COVERAGE")
    require(all(isinstance(finding_id, str) and re.fullmatch(r"P065-S70-F(?:0[6-9]|[1-9][0-9]+)", finding_id) for finding_id in finding_ids), "E_EVIDENCE_FINDING_ID_FORMAT")
    require(all(row["severity"] in {"P0", "P1", "P2"} for row in finding_routes), "E_EVIDENCE_FINDING_SEVERITY")
    require(all(isinstance(row["status"], str) and row["status"] for row in finding_routes), "E_EVIDENCE_FINDING_STATUS")
    require(all(isinstance(row["summary"], str) and row["summary"] for row in finding_routes), "E_EVIDENCE_FINDING_SUMMARY")
    require(all(isinstance(row["owner"], str) and row["owner"] for row in finding_routes), "E_EVIDENCE_FINDING_OWNER")
    require(all(isinstance(row["target_steps"], list) and row["target_steps"] and all(isinstance(step, str) and step for step in row["target_steps"]) for row in finding_routes), "E_EVIDENCE_FINDING_TARGETS")
    require(all(row["authority_promoted"] is False for row in finding_routes), "E_EVIDENCE_FINDING_AUTHORITY")
    return assignments


def apply_human_evidence(core: dict[str, Any], assignments: dict[str, dict[str, Any]]) -> None:
    def stamp(record: dict[str, Any], group_id: str) -> None:
        assignment = assignments[group_id]
        record["read_status"] = assignment["status"]
        record["read_ranges"] = record["machine_extent_ranges"]
        record["human_review"] = {
            "group_id": group_id,
            "reader_id": assignment["reader_id"],
            "binding_sha256": assignment["binding_sha256"],
        }

    source_group_by_blob: dict[str, str] = {}
    for row in core["unique_sources"]:
        if row["review_mode"] == "FULL_PDF":
            group_id = "release_pdf"
        elif row["review_mode"] == "FULL_IMAGE":
            group_id = "release_image"
        elif row["representative_path"].endswith(".py"):
            group_id = "release_code_test_text"
        else:
            group_id = "release_scientific_document_text"
        stamp(row, group_id)
        source_group_by_blob[row["blob"]] = group_id
    source_by_blob = {row["blob"]: row for row in core["unique_sources"]}
    for row in core["occurrences"]:
        source = source_by_blob[row["blob"]]
        row["read_status"] = source["read_status"]
        row["read_ranges"] = source["read_ranges"]
        row["human_review"] = source["human_review"]

    for row in core["supplemental"]["records"]:
        stamp(row, "supplemental_process_text")
    for row in core["narrative"]["records"]:
        stamp(row, "narrative_history")
    comp_group = {
        "py": "comp_v24_python",
        "json": "comp_v24_json",
        "csv": "comp_v24_csv",
        "txt": "comp_v24_txt",
        "png": "comp_v24_png",
        "md": "narrative_history",
    }
    narrative_review = assignments["narrative_history"]
    for row in core["comp_v24"]["records"]:
        group_id = comp_group[row["extension"]]
        if group_id == "narrative_history":
            row["read_status"] = narrative_review["status"]
            row["read_ranges"] = row["machine_extent_ranges"]
            row["human_review"] = {
                "group_id": group_id,
                "reader_id": narrative_review["reader_id"],
                "binding_sha256": narrative_review["binding_sha256"],
            }
        else:
            stamp(row, group_id)

    for row in core["process"]["release"]["commits"]:
        assignment = assignments["release_process_all_038"]
        row["complete_diff_read"] = True
        row["classification_review"] = "HUMAN_REVIEWED_SUBJECT_PATHS_BINARY_PATCH_AND_CANONICAL_ROUTING"
        row["human_review"] = {"group_id": "release_process_all_038", "reader_id": assignment["reader_id"], "binding_sha256": assignment["binding_sha256"]}
        for patch in row["parent_patches"]:
            patch["read_status"] = assignment["status"]
            patch["read_ranges"] = [[1, patch["lines"]]] if patch["lines"] else []
            patch["human_review"] = {"group_id": "release_process_all_038", "reader_id": assignment["reader_id"], "binding_sha256": assignment["binding_sha256"]}
    for row in core["process"]["routed"]["commits"]:
        group_id = next(group for group, spec in PROCESS_PARTITIONS.items() if spec["ordinals"][0] <= row["ordinal"] <= spec["ordinals"][1])
        assignment = assignments[group_id]
        row["complete_diff_read"] = True
        row["classification_review"] = "HUMAN_REVIEWED_SUBJECT_PATHS_BINARY_PATCH_AND_CANONICAL_ROUTING"
        row["human_review"] = {"group_id": group_id, "reader_id": assignment["reader_id"], "binding_sha256": assignment["binding_sha256"]}
        for patch in row["parent_patches"]:
            patch["read_status"] = assignment["status"]
            patch["read_ranges"] = [[1, patch["lines"]]] if patch["lines"] else []
            patch["human_review"] = {"group_id": group_id, "reader_id": assignment["reader_id"], "binding_sha256": assignment["binding_sha256"]}
    require_process_projection_consistency(core["process"]["release"], core["process"]["routed"])


def build_artifacts(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    core = build_core(root)
    bindings = evidence_bindings(root, core)
    evidence, evidence_hash = parse_human_evidence(root)
    assignments = validate_evidence(evidence, bindings)
    apply_human_evidence(core, assignments)
    topology: dict[str, Any] = {
        "schema_version": "P065-S70-TOPOLOGY-1",
        "generated_date": "2026-08-30",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "branch": BRANCH,
        "manifest": core["manifest"],
        "occurrences": core["occurrences"],
        "unique_sources": core["unique_sources"],
        "mirror": core["mirror"],
        "supplemental": core["supplemental"],
        "narrative": core["narrative"],
        "comp_v24": core["comp_v24"],
        "process": core["process"],
        "tex": core["tex"],
        "derived_artifacts": core["derived_artifacts"],
        "phase057_observations": core["phase057_observations"],
        "findings": [
            {"id": "P065-S70-F01", "status": "CONFIRMED", "finding": "v1.0.24.1 is a 130-blob mirror plus one archive note and is not independent corroboration."},
            {"id": "P065-S70-F02", "status": "CONFIRMED", "finding": "The JSON-suffixed snapshot is a 37-byte plain-text pointer."},
            {"id": "P065-S70-F03", "status": "CORRECTED", "finding": "The exact 29-path process partition is 2,306 lines; copied 2,068 is stale."},
            {"id": "P065-S70-F04", "status": "CONFIRMED", "finding": "The 38 release commits are a strict subset of the 98 routed commits."},
            {"id": "P065-S70-F05", "status": "BOUND", "finding": "Derived artifacts do not provide independent scientific authority."},
            *evidence["finding_routes"],
        ],
        "authority": AUTHORITY_CEILING,
        "human_evidence_sha256": evidence_hash,
    }
    topology["semantic_sha256"] = semantic_hash(topology)
    attestation: dict[str, Any] = {
        "schema_version": "P065-S70-ATTESTATION-1",
        "generated_date": "2026-08-30",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "result_path": RESULT_PATH,
        "result_sha256_lf": sha256_bytes(lf_bytes((root / RESULT_PATH).read_bytes())),
        "human_evidence_sha256": evidence_hash,
        "topology_semantic_sha256": topology["semantic_sha256"],
        "coverage": {
            "unique_sources": {"read": 131, "required": 131},
            "text": {"blobs": 125, "lines": 21618},
            "pdf": {"documents": 3, "pages_extracted": 148, "pages_rendered": 148, "pages_visual": 148},
            "image": {"images": 3, "original_resolution_visual": 3},
            "supplemental": {"documents": 6, "lines": 728},
            "narrative": {"documents": 74, "lines": 7470},
            "comp_v24": {
                "python": {"files": 29, "lines": 2932},
                "json": {"files": 16, "lines": 1650},
                "csv": {"files": 10, "lines": 45203},
                "txt": {"files": 7, "lines": 171},
                "png": {"files": 33, "original_resolution_visual": 33},
            },
            "release_commits": {"commits": 38, "complete_patches": 38},
            "routed_commits": {"commits": 98, "complete_patches": 98, "patch_bytes": 12505904, "patch_lines": 106801},
            "routed_partitions": PROCESS_PARTITIONS,
        },
        "bindings": bindings,
        "readers": evidence["readers"],
        "pdf_visual": evidence["pdf_visual"],
        "image_visual": evidence["image_visual"],
        "process_patch_read": evidence["process_patch_read"],
        "semantic_deferred_intervals": evidence.get("semantic_deferred_intervals", []),
        "output_truncation_rechecks": evidence.get("output_truncation_rechecks", []),
        "output_truncation_unresolved": evidence["output_truncation_unresolved"],
        "unreviewed_intervals": evidence["unreviewed_intervals"],
        "authority": AUTHORITY_CEILING,
        "gate": "PASS_P065_STEP70_PRECOMMIT",
    }
    attestation["semantic_sha256"] = semantic_hash(attestation)
    return topology, attestation


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    allowed = {(ROOT / TOPOLOGY_PATH).resolve(), (ROOT / ATTESTATION_PATH).resolve()}
    require(path.resolve() in allowed, "E_WRITE_TARGET", str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(canonical_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--print-bindings", action="store_true")
    args = parser.parse_args()
    try:
        if args.print_bindings:
            core = build_core(ROOT)
            print(json.dumps(evidence_bindings(ROOT, core), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        topology, attestation = build_artifacts(ROOT)
        if args.collect:
            output_dir = ROOT / "Codex" / "results"
            write_json_atomic(output_dir / Path(TOPOLOGY_PATH).name, topology)
            write_json_atomic(output_dir / Path(ATTESTATION_PATH).name, attestation)
        else:
            print(json.dumps({"topology_semantic_sha256": topology["semantic_sha256"], "attestation_semantic_sha256": attestation["semantic_sha256"]}, sort_keys=True))
    except (BuildFailure, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL_P065_STEP70_BUILD {exc}")
        return 1
    print("PASS_P065_STEP70_BUILD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
