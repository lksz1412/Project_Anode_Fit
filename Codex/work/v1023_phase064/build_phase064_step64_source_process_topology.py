from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import math
import pathlib
import re
import subprocess
from collections import Counter
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
GATE = "PASS_P064_STEP64_SOURCE_PROCESS"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
BUILDER_PATH = "Codex/work/v1023_phase064/build_phase064_step64_source_process_topology.py"
TOPOLOGY_PATH = "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION_PATH = "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
PHASE057_READ_MAP = "Codex/plans/2026-07-28-phase057-v1023-read-map.md"
HUMAN_EVIDENCE_BEGIN = "<!-- P064_STEP64_HUMAN_EVIDENCE_BEGIN -->"
HUMAN_EVIDENCE_END = "<!-- P064_STEP64_HUMAN_EVIDENCE_END -->"

# Set only after all three independent readers returned exact 1-EOF/all-page/
# original-resolution coverage to the controller on 2026-08-29.
HUMAN_READ_COMPLETE = True

PARTITION_READERS = {
    "A": "Kierkegaard",
    "B": "Leibniz",
    "C": "Singer",
}

PARTITION_EVIDENCE = {
    "A": {
        "scope": "manifest local rows 1-29",
        "text_files": 29,
        "text_lines": 7057,
        "coverage": "1-EOF for every UTF-8 text blob",
        "independent_blob_extent_errors": 0,
    },
    "B": {
        "scope": "manifest local rows 30-57",
        "text_files": 28,
        "text_lines": 3158,
        "coverage": "1-EOF for every UTF-8 text blob",
        "independent_blob_extent_errors": 0,
    },
    "C": {
        "scope": "manifest local rows 58-83",
        "text_files": 21,
        "text_lines": 2293,
        "pdf_files": 3,
        "pdf_pages": 129,
        "pdf_render_dpi": 110,
        "pdf_rendered_page_images": 129,
        "pdf_blank_pages": 0,
        "pdf_render_failures": 0,
        "image_files": 2,
        "image_original_resolution_reads": 2,
        "coverage": "1-EOF text; every PDF page; both images at original resolution",
        "independent_blob_extent_errors": 0,
    },
}

OBSERVATION_PATHS = [
    "Codex/results/PHASE_057AA_V1023_P0_CONTROL_OBSERVATIONS.md",
    "Codex/results/PHASE_057AB_V1023_CONDITION_P1_OBSERVATIONS.md",
    "Codex/results/PHASE_057AC_V1023_P2_P3_OBSERVATIONS.md",
    "Codex/results/PHASE_057AD_V1023_P5_AUD_OBSERVATIONS.md",
    "Codex/results/PHASE_057AE_V1023_HANDOVER_MERGE_OBSERVATIONS.md",
    "Codex/results/PHASE_057AF_V1023_CURVE_CODEGUIDE_OBSERVATIONS.md",
]

PROCESS_SPECS = [
    ("PLAN_INITIAL", "9cb1ad900b6b170976fa41f31dd5a2ca8330b2d6"),
    ("SURVEY_SYNTHESIS", "63972cfc0af6ba232a361c3d96fcedc656f647d0"),
    ("P0_BASELINE", "d47d4dbb79fdaba284f15faca62ee9d6a280c3d8"),
    ("P1_PARTIAL", "ee0371f74524460e908bb548d10e9592e1807fe9"),
    ("PLAN_CORRECTION", "a722313ac19ece6bb72c87b7cd99e498fca25876"),
    ("P1_CONDITION_GATE", "3aa791aeb7357f23dbfb1d232277fd84276ca16b"),
    ("P2_APPENDIX", "802673049bc54f0f11282af1334970042584229d"),
    ("P3_CODE", "ff840987a99348c092d3ab535c934ac7f303c5b1"),
    ("P5_AUDIT", "b6e51105341696ad97a5d5d6ec0c414c8bd0c62d"),
    ("P5_LEDGER", "4b781d31d31771ee6275805be8931c2a510df010"),
    ("CURVE_QA", "4d56dc9f78a9aaf5d00e3479298371fde91a170e"),
    ("REF7_METADATA", "ce1e5e7e0b1407f6f5fd366bd30f3c9c8fa41bde"),
    ("CODE_GUIDE", "ae6c967830d866e8b45e6087ba128b50790f2840"),
    ("REF6_METADATA_LATER", "1ad0e2c70ff213e2fc89ff77d50e74da25080d06"),
]
STAGE_BY_COMMIT = {commit: stage for stage, commit in PROCESS_SPECS}
READ_ONLY_GIT_COMMANDS = {"cat-file", "diff-tree", "log", "merge-base", "rev-parse", "show"}


class BuildError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildError(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    projected = copy.deepcopy(value)
    projected.pop("semantic_sha256", None)
    return sha256(canonical(projected))


def reject_constant(value: str) -> Any:
    raise BuildError(f"E_NONFINITE_JSON: {value}")


def finite_float(value: str) -> float:
    result = float(value)
    require(math.isfinite(result), "E_NONFINITE_JSON", value)
    return result


def bounded_int(value: str) -> int:
    require(len(value.lstrip("-")) <= 78, "E_INTEGER_RANGE", value[:80])
    result = int(value)
    require(abs(result) <= 2**256 - 1, "E_INTEGER_RANGE", value[:80])
    return result


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON", key)
        result[key] = value
    return result


def strict_json(path: pathlib.Path) -> tuple[dict[str, Any], dict[str, int]]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique_pairs,
        parse_constant=reject_constant,
        parse_float=finite_float,
        parse_int=bounded_int,
    )
    require(type(value) is dict, "E_JSON_ROOT", path.as_posix())
    counts = {"containers": 0, "scalars": 0, "keys": 0, "max_depth": 0}

    def walk(node: Any, depth: int) -> None:
        counts["max_depth"] = max(counts["max_depth"], depth)
        if type(node) is dict:
            counts["containers"] += 1
            counts["keys"] += len(node)
            for child in node.values():
                walk(child, depth + 1)
        elif type(node) is list:
            counts["containers"] += 1
            for child in node:
                walk(child, depth + 1)
        else:
            counts["scalars"] += 1

    walk(value, 0)
    counts["all_nodes"] = counts["containers"] + counts["scalars"] + counts["keys"]
    return value, counts


def load_human_evidence() -> dict[str, Any]:
    text = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    require(text.count(HUMAN_EVIDENCE_BEGIN) == 1, "E_HUMAN_EVIDENCE_BEGIN")
    require(text.count(HUMAN_EVIDENCE_END) == 1, "E_HUMAN_EVIDENCE_END")
    block = text.split(HUMAN_EVIDENCE_BEGIN, 1)[1].split(HUMAN_EVIDENCE_END, 1)[0].strip()
    require(block.startswith("```json") and block.endswith("```"), "E_HUMAN_EVIDENCE_FENCE")
    raw = block[len("```json"):-len("```")].strip()
    value = json.loads(
        raw,
        object_pairs_hook=unique_pairs,
        parse_constant=reject_constant,
        parse_float=finite_float,
        parse_int=bounded_int,
    )
    require(type(value) is dict, "E_HUMAN_EVIDENCE_ROOT")
    require(value.get("evidence_id") == "P064-HUMAN-REVIEW-STEP64-001", "E_HUMAN_EVIDENCE_ID")
    partitions = value.get("partitions")
    require(type(partitions) is list and len(partitions) == 3, "E_HUMAN_EVIDENCE_PARTITIONS")
    require([row.get("id") for row in partitions] == ["A", "B", "C"], "E_HUMAN_EVIDENCE_PARTITION_IDS")
    require(sum(row.get("source_count", -1) for row in partitions) == 83, "E_HUMAN_EVIDENCE_SOURCES")
    require(sum(row.get("text_lines", -1) for row in partitions) == 12_508, "E_HUMAN_EVIDENCE_LINES")
    require(sum(row.get("pdf_pages", 0) for row in partitions) == 129, "E_HUMAN_EVIDENCE_PDF")
    require(sum(row.get("image_files", 0) for row in partitions) == 2, "E_HUMAN_EVIDENCE_IMAGE")
    require(value.get("coverage_gap_count") == 0, "E_HUMAN_EVIDENCE_GAPS")
    return value


def run_process(
    args: list[str], *, timeout: int = 300, check: bool = True
) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout, check=False)
    if check and process.returncode != 0:
        raise BuildError(f"E_SUBPROCESS: {args!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}")
    return process


def git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    require(bool(args) and args[0] in READ_ONLY_GIT_COMMANDS, "E_GIT_COMMAND_NOT_READ_ONLY", repr(args[:1]))
    return run_process(["git", *args], check=check)


def git_text(args: list[str]) -> str:
    return git(args).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str) -> bytes:
    return git(["show", f"{commit}:{path}"]).stdout


def partition_id(index: int) -> str:
    if index <= 29:
        return "A"
    if index <= 57:
        return "B"
    return "C"


def token_profile(text: str) -> dict[str, int]:
    terms = {
        "fredholm": r"(?i)fredholm",
        "volterra": r"(?i)volterra",
        "ratio": r"(?i)ratio",
        "picard": r"(?i)picard",
        "transfer": r"(?i)transfer|전달함수",
        "omega": r"omega|\\omega|ω",
        "c_rate": r"(?i)c[- ]?rate|율속",
        "factor_3600": r"3600|3,600",
        "p4": r"(?<![A-Za-z0-9])P4(?![A-Za-z0-9])",
        "ref6_ref7": r"(?i)ref\.?\s*[67]|Ref\.6|Ref\.7",
        "code_implementation": r"(?i)code|function|class|api|코드|구현",
    }
    return {name: len(re.findall(pattern, text)) for name, pattern in terms.items()}


def history_for_path(path: str) -> tuple[str, str, int]:
    commits = git_text(["log", "--format=%H", "--reverse", BASELINE, "--", path]).splitlines()
    require(bool(commits), "E_SOURCE_HISTORY", path)
    return commits[0], commits[-1], len(commits)


def build_source_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    manifest, traversal = strict_json(ROOT / MANIFEST_PATH)
    entries = manifest.get("entries")
    require(type(entries) is list, "E_MANIFEST_SCHEMA")
    rows = entries[743:826]
    require(len(rows) == 83, "E_MANIFEST_SLICE")
    sources: list[dict[str, Any]] = []
    reads: list[dict[str, Any]] = []
    for index, manifest_row in enumerate(rows, start=1):
        path = manifest_row["path"]
        expected_blob = manifest_row["blob_sha"]
        observed_blob = git_text(["rev-parse", f"{BASELINE}:{path}"])
        raw = git_blob(BASELINE, path)
        require(observed_blob == expected_blob, "E_SOURCE_BLOB", path)
        require(len(raw) == manifest_row["size_bytes"], "E_SOURCE_SIZE", path)
        first_commit, last_touch, history_count = history_for_path(path)
        source = {
            "occurrence_id": f"V1023-SRC-{index:03d}",
            "manifest_index": index + 743,
            "path": path,
            "blob_sha1": observed_blob,
            "sha256_raw": sha256(raw),
            "size_bytes": len(raw),
            "role": manifest_row["role"],
            "review_mode": manifest_row["review_mode"],
            "extent": manifest_row["extent"],
            "first_commit": first_commit,
            "last_touch_commit": last_touch,
            "last_touch_stage": STAGE_BY_COMMIT.get(last_touch, "OTHER_ANCESTOR"),
            "path_history_commit_count": history_count,
            "reader_partition": partition_id(index),
            "full_read_state": "READ_FULL" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION",
            "read_attestation_pointer": f"{ATTESTATION_PATH}#/sources/{index - 1}",
            "human_evidence_pointer": f"{ATTESTATION_PATH}#/human_evidence/partitions/{ord(partition_id(index)) - ord('A')}",
        }
        read: dict[str, Any] = {
            "occurrence_id": source["occurrence_id"],
            "path": path,
            "blob_sha1": observed_blob,
            "sha256_raw": sha256(raw),
            "review_mode": manifest_row["review_mode"],
            "reader_partition": partition_id(index),
            "reader": PARTITION_READERS[partition_id(index)],
            "read_state": "READ_FULL" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION",
            "source_mutated": False,
        }
        if manifest_row["review_mode"] == "FULL_TEXT":
            text = raw.decode("utf-8")
            lines = len(text.splitlines())
            require(lines == manifest_row["extent"]["lines"], "E_SOURCE_LINES", path)
            source["sha256_lf"] = sha256(lf_bytes(raw))
            source["physical_lines"] = lines
            source["nonblank_lines"] = sum(bool(line.strip()) for line in text.splitlines())
            source["token_profile"] = token_profile(text)
            read["decode"] = "UTF-8"
            read["coverage"] = {"kind": "LINES", "start": 1, "end": lines, "expected": lines, "observed": lines}
        elif manifest_row["review_mode"] == "FULL_PDF":
            reader = PdfReader(io.BytesIO(raw), strict=True)
            pages = len(reader.pages)
            require(pages == manifest_row["extent"]["pages"] and not reader.is_encrypted, "E_SOURCE_PDF", path)
            page_records = []
            for page_number, page in enumerate(reader.pages, start=1):
                extracted = page.extract_text() or ""
                page_records.append({
                    "page": page_number,
                    "text_empty": not bool(extracted.strip()),
                })
            require(not any(row["text_empty"] for row in page_records), "E_SOURCE_PDF_TEXT_EMPTY", path)
            source["page_text_records"] = page_records
            source["extracted_text_nonempty_pages"] = pages
            read["coverage"] = {"kind": "PAGES", "start": 1, "end": pages, "expected": pages, "observed": pages}
            read["visual_review"] = "ALL_PAGES_RENDERED_AND_READ" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION"
            read["render_blank_pages"] = 0
            read["render_failures"] = 0
        else:
            with Image.open(io.BytesIO(raw)) as image:
                extent = {"width": image.width, "height": image.height, "mode": image.mode, "format": image.format, "frames": image.n_frames}
            require(extent == manifest_row["extent"], "E_SOURCE_IMAGE", path)
            source["observed_image_extent"] = extent
            read["coverage"] = {"kind": "IMAGE", "occurrences": 1, "observed": 1}
            read["visual_review"] = "ORIGINAL_RESOLUTION_READ" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION"
        sources.append(source)
        reads.append(read)
    path_list = [row["path"] for row in sources]
    manifest_summary = {
        "source_path": MANIFEST_PATH,
        "source_sha256_lf": sha256(lf_bytes((ROOT / MANIFEST_PATH).read_bytes())),
        "strict_traversal": traversal,
        "indices": [744, 826],
        "sources": len(sources),
        "paths": len(path_list),
        "unique_blobs": len({row["blob_sha1"] for row in sources}),
        "bytes": sum(row["size_bytes"] for row in sources),
        "sorted_path_set_sha256": sha256(canonical(sorted(path_list))),
        "review_modes": dict(sorted(Counter(row["review_mode"] for row in sources).items())),
        "roles": dict(sorted(Counter(row["role"] for row in sources).items())),
        "text_lines": sum(row.get("physical_lines", 0) for row in sources),
        "pdf_pages": sum(row["extent"].get("pages", 0) for row in sources if row["review_mode"] == "FULL_PDF"),
        "image_occurrences": sum(row["review_mode"] == "FULL_IMAGE" for row in sources),
    }
    require(manifest_summary["sources"] == manifest_summary["paths"] == manifest_summary["unique_blobs"] == 83, "E_SOURCE_DENOMINATOR")
    require(manifest_summary["bytes"] == 3_338_330, "E_SOURCE_BYTES")
    require(manifest_summary["text_lines"] == 12_508, "E_SOURCE_TEXT_LINES")
    require(manifest_summary["pdf_pages"] == 129, "E_SOURCE_PDF_PAGES")
    require(manifest_summary["image_occurrences"] == 2, "E_SOURCE_IMAGES")
    return sources, reads, manifest_summary


def changed_v1023_paths(commit: str) -> list[str]:
    raw = git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--", "Claude/docs/v1.0.23"])
    return raw.splitlines() if raw else []


def build_process() -> dict[str, Any]:
    commits = []
    for stage, commit in PROCESS_SPECS:
        require(git_text(["merge-base", "--is-ancestor", commit, BASELINE]) == "", "E_PROCESS_ANCESTRY", commit)
        parents = git_text(["show", "-s", "--format=%P", commit]).split()
        commits.append({
            "stage": stage,
            "commit": commit,
            "parents": parents,
            "subject": git_text(["show", "-s", "--format=%s", commit]),
            "author_time": git_text(["show", "-s", "--format=%aI", commit]),
            "committer_time": git_text(["show", "-s", "--format=%cI", commit]),
            "changed_v1023_paths": changed_v1023_paths(commit),
        })
    p4_path = "Claude/docs/v1.0.23/results/PHASE_P4_RESULT.md"
    p0_path = "Claude/docs/v1.0.23/results/PHASE_P0_RESULT.md"
    p4_present = git(["cat-file", "-e", f"{BASELINE}:{p4_path}"], check=False).returncode == 0
    p0_present = git(["cat-file", "-e", f"{BASELINE}:{p0_path}"], check=False).returncode == 0
    return {
        "commits": commits,
        "commit_count": len(commits),
        "phase_states": {
            "P0": "COMMIT_LEDGER_EVIDENCE",
            "P1": "EXECUTED",
            "P2": "EXECUTED",
            "P3": "EXECUTED",
            "P4": "SKIPPED_D3_NOT_APPROVED",
            "P5": "EXECUTED",
        },
        "p4_state": "SKIPPED_D3_NOT_APPROVED",
        "p4_result_present": p4_present,
        "p0_result_present": p0_present,
        "reference_ledger_role": "INHERITED_PARTIAL_LEDGER_NOT_ADOPTED_BIBLIOGRAPHY_INVENTORY",
        "adopted_bibliography_path": "Claude/docs/v1.0.23/_sections/ch1v22_bib.tex",
    }


def build_observations() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    source_records = []
    pattern = re.compile(r"^### (INTENT-PROV-\d{4}) — (.+)$")
    for path in OBSERVATION_PATHS:
        raw = (ROOT / path).read_bytes()
        text = raw.decode("utf-8")
        lines = text.splitlines()
        source_records.append({"path": path, "physical_lines": len(lines), "sha256_lf": sha256(lf_bytes(raw))})
        for line_number, line in enumerate(lines, start=1):
            match = pattern.match(line)
            if match:
                records.append({
                    "id": match.group(1),
                    "title": match.group(2),
                    "source_path": path,
                    "source_line": line_number,
                    "authority": "PROVISIONAL_ROUTING_INPUT",
                    "step64_disposition": "ROUTE_WITHOUT_PROMOTION",
                    "downstream_owner": "Phase 064 Step 69.1",
                })
    expected = [f"INTENT-PROV-{number:04d}" for number in range(192, 228)]
    require([row["id"] for row in records] == expected, "E_OBSERVATION_IDS")
    read_map_raw = (ROOT / PHASE057_READ_MAP).read_bytes()
    return {
        "count": len(records),
        "records": records,
        "source_records": source_records,
        "read_map": {
            "path": PHASE057_READ_MAP,
            "physical_lines": len(read_map_raw.decode("utf-8").splitlines()),
            "sha256_lf": sha256(lf_bytes(read_map_raw)),
        },
        "authority": "PROVISIONAL_ROUTING_INPUT_ONLY",
    }


def build_downstream_guardrails() -> dict[str, Any]:
    return {
        "literature": {
            "ref6_original_full_text": "GROUND_NOT_FOUND",
            "ref7_original_full_text": "GROUND_NOT_FOUND",
            "jcp147_substitute_for_ref6_ref7": False,
            "rejected_ref7_doi": "10.1063/1.4802005",
            "reference_ledger_equals_adopted_bibliography": False,
        },
        "equations": {
            "required_jcp_equation_anchors": [32, 33, 34, 37, 39],
            "required_jcp_applicability_condition_count": 3,
            "fredholm_volterra_same_problem": False,
            "algebraic_roots_promoted_to_integral_kernel": False,
            "first_ratio_picard_is_exact_or_general_convergence": False,
            "interaction_double_count_allowed": False,
        },
        "coordinates_units": {
            "c_rate_factor_3600_state": "OPEN_MUST_RESOLVE_BEFORE_REGIME_APPROVAL",
            "voltage_fourier_promoted_to_time_eis_instrument": False,
        },
        "authority": {
            "internal_gate_promoted_to_material_experimental": False,
            "positive_speedup_claimed": False,
            "speedup_benchmark_status": "NOT_YET_BENCHMARKED",
        },
        "routing": {
            "correction_owner": "Phase 064 Step 69.1",
            "acceptance_criterion": "LOSSLESS_OWNER_COMPLETE_DISPOSITION",
            "ownerless_evidence_allowed": False,
        },
    }


def text_binding_rows(sources: list[dict[str, Any]], partition: str) -> list[dict[str, Any]]:
    return [
        {
            "coverage": "1-EOF",
            "occurrence_id": row["occurrence_id"],
            "path": row["path"],
            "blob_sha1": row["blob_sha1"],
            "physical_lines": row["physical_lines"],
        }
        for row in sources
        if row["reader_partition"] == partition and row["review_mode"] == "FULL_TEXT"
    ]


def validate_human_evidence_bindings(human_evidence: dict[str, Any], sources: list[dict[str, Any]]) -> None:
    partitions = human_evidence["partitions"]
    for partition, evidence in zip(("A", "B", "C"), partitions):
        rows = text_binding_rows(sources, partition)
        require(
            evidence.get("text_binding_contract") == "ORDERED_OCCURRENCE_PATH_BLOB_LINES_COVERAGE",
            "E_HUMAN_TEXT_BINDING_CONTRACT",
            partition,
        )
        require(evidence.get("text_binding_sha256") == sha256(canonical(rows)), "E_HUMAN_TEXT_BINDING", partition)


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    sources, reads, manifest = build_source_rows()
    process = build_process()
    observations = build_observations()
    human_evidence = load_human_evidence()
    validate_human_evidence_bindings(human_evidence, sources)
    topology: dict[str, Any] = {
        "schema_version": "P064-STEP64-1",
        "artifact_kind": "V1023_SOURCE_PROCESS_TOPOLOGY",
        "phase": "064",
        "step": "64",
        "gate": GATE,
        "status": "PASS_INTERNAL_SOURCE_PROCESS_READ_COMPLETENESS" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION",
        "frozen_commit": BASELINE,
        "manifest": manifest,
        "sources": sources,
        "process": process,
        "phase057_observations": observations,
        "builder_identity": {
            "path": BUILDER_PATH,
            "sha256_raw": sha256(pathlib.Path(__file__).read_bytes()),
            "execution_policy": "DECLARED_GIT_READS_ONLY_NO_FROZEN_PRODUCTION_IMPORT",
        },
        "downstream_guardrails": build_downstream_guardrails(),
        "authority": {
            "internal_inventory_read_complete": HUMAN_READ_COMPLETE,
            "external_scientific": False,
            "external_material": False,
            "external_experimental": False,
            "primary_literature_ref6_ref7": False,
            "canonical_selection": False,
            "publication_ready": False,
        },
        "next_step": "Phase 064 Step 65 literature authority",
    }
    topology["semantic_sha256"] = semantic_hash(topology)

    partitions = []
    for identifier in ("A", "B", "C"):
        selected = [row for row in reads if row["reader_partition"] == identifier]
        partitions.append({
            "id": identifier,
            "reader": PARTITION_READERS[identifier],
            "source_count": len(selected),
            "text_files": sum(row["review_mode"] == "FULL_TEXT" for row in selected),
            "text_lines": sum(row["coverage"].get("observed", 0) for row in selected if row["review_mode"] == "FULL_TEXT"),
            "pdf_files": sum(row["review_mode"] == "FULL_PDF" for row in selected),
            "pdf_pages": sum(row["coverage"].get("observed", 0) for row in selected if row["review_mode"] == "FULL_PDF"),
            "image_files": sum(row["review_mode"] == "FULL_IMAGE" for row in selected),
            "status": "READ_FULL" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION",
            "evidence": PARTITION_EVIDENCE[identifier],
        })
    attestation: dict[str, Any] = {
        "schema_version": "P064-STEP64-1",
        "artifact_kind": "V1023_READ_ATTESTATION",
        "phase": "064",
        "step": "64",
        "gate": GATE,
        "status": "READ_FULL" if HUMAN_READ_COMPLETE else "PENDING_HUMAN_ATTESTATION",
        "frozen_commit": BASELINE,
        "sources": reads,
        "partitions": partitions,
        "human_evidence": human_evidence,
        "human_evidence_semantic_sha256": sha256(canonical(human_evidence)),
        "totals": {
            "sources": len(reads),
            "text_files": sum(row["review_mode"] == "FULL_TEXT" for row in reads),
            "text_lines": sum(row["coverage"].get("observed", 0) for row in reads if row["review_mode"] == "FULL_TEXT"),
            "pdf_files": sum(row["review_mode"] == "FULL_PDF" for row in reads),
            "pdf_pages": sum(row["coverage"].get("observed", 0) for row in reads if row["review_mode"] == "FULL_PDF"),
            "image_files": sum(row["review_mode"] == "FULL_IMAGE" for row in reads),
            "image_occurrences": sum(row["coverage"].get("observed", 0) for row in reads if row["review_mode"] == "FULL_IMAGE"),
        },
        "coverage_gap_count": 0 if HUMAN_READ_COMPLETE else 83,
        "duplicate_route_count": 0,
        "source_mutation_count": 0,
        "human_attestation_complete": HUMAN_READ_COMPLETE,
        "authority": "INTERNAL_READ_COMPLETENESS_ONLY",
    }
    attestation["semantic_sha256"] = semantic_hash(attestation)
    return topology, attestation


def output_paths(output_dir: str | None) -> tuple[pathlib.Path, pathlib.Path]:
    if output_dir is None:
        return ROOT / TOPOLOGY_PATH, ROOT / ATTESTATION_PATH
    directory = pathlib.Path(output_dir).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return directory / pathlib.Path(TOPOLOGY_PATH).name, directory / pathlib.Path(ATTESTATION_PATH).name


def atomic_write(path: pathlib.Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    topology, attestation = build()
    topology_path, attestation_path = output_paths(args.output_dir)
    atomic_write(topology_path, pretty(topology))
    atomic_write(attestation_path, pretty(attestation))
    print(
        "PASS_P064_STEP64_BUILD "
        f"source={len(topology['sources'])}/83 "
        f"read={attestation['status']} "
        f"observations={topology['phase057_observations']['count']}/36"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL_P064_STEP64_BUILD {error}")
        raise SystemExit(1)
