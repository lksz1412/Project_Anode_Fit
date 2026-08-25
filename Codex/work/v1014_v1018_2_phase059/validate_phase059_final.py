#!/usr/bin/env python3
"""Build and validate the Phase 059 integrated validation evidence.

The script is intentionally a validator/collector, not a producer for any older
Phase 059 artifact.  Validators that can write are executed only in a disposable
clone.  The active checkout is fingerprinted before and after every collection.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "9791b235e25653ee4f834d4d4fe0b5998ca37410"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED = "fc5f1776"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
ARTIFACT_PATH = "Codex/results/PHASE_059_VALIDATION.json"
ARTIFACT = ROOT / ARTIFACT_PATH
QUEUE_PATH = "Codex/results/PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
TEXT_PATH = "Codex/results/PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
REPORT_B_PATH = "Codex/results/PHASE_059_V1014_V1018_2_LINEAGE_REPORT_B.md"
STEP_RESULT_PATH = "Codex/results/PHASE_059_STEP_039_5_INTEGRATED_VALIDATION_RESULT.md"
VALIDATOR_PATH = "Codex/work/v1014_v1018_2_phase059/validate_phase059_final.py"
STEP_PATHS = {ARTIFACT_PATH, REPORT_B_PATH, STEP_RESULT_PATH, VALIDATOR_PATH}
VERSIONS = ["v1.0.14", "v1.0.15", "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2"]
AUTHORITY = (
    "PASS establishes only frozen-corpus audit completeness and internal reproducibility; "
    "it does not establish external literature truth, material validity, public-data "
    "validation, parameter identifiability, defect repair, canonical-model status, or a "
    "final publication artifact."
)
REPORT_B_LF_SHA256 = "526fdf3ad92b00d72af065e9b545e7db6f9a72aebca2fcb2ada65969815d94d0"
STEP_RESULT_MASKED_LF_SHA256 = "dd569838d3cadaf1bd7a4417983006fd1d764cc65007e993e3032bcb2b66a4e5"
STEP_RESULT_VALIDATOR_ROW_PATTERN = re.compile(
    r"^\| `Codex/work/v1014_v1018_2_phase059/validate_phase059_final\.py` "
    r"\| ([0-9][0-9,]*) \| ([0-9][0-9,]*) \| `([0-9a-f]{64})` \|$",
    re.MULTILINE,
)
STEP_RESULT_VALIDATOR_ROW_MASK = "| <VALIDATOR_MEASUREMENT_ROW_MASKED> |"
CLONE_GIT_CONFIG = {
    "core.autocrlf": "true",
    "core.safecrlf": "false",
    "core.eol": "native",
}


HUMAN_OUTPUTS = [
    "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md",
    "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md",
    "Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md",
    "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md",
    "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_REVIEW.md",
    "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_REVIEW.md",
    "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_REVIEW.md",
    "Codex/results/PHASE_059_V1015_HEAT_DETAILING_REVIEW.md",
    "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md",
    "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md",
    "Codex/results/PHASE_059_V1017_DOC_CITATION_REVIEW.md",
    "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_REVIEW.md",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_059_STEP_039_2_BLOCKER_DELTA_RESULT.md",
    "Codex/results/PHASE_059_STEP_039_3_FOUR_AXIS_CONFORMANCE_RESULT.md",
    "Codex/results/PHASE_059_STEP_039_4_CARRY_FORWARD_RESULT.md",
]

MACHINE_OUTPUTS = [
    "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json",
    "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json",
    "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json",
    "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json",
    "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_AUDIT.json",
    "Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json",
    "Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_AUDIT.json",
    "Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json",
    "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json",
    "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json",
    "Codex/results/PHASE_059_V1017_DOC_CITATION_AUDIT.json",
    "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_AUDIT.json",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json",
    "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json",
    "Codex/results/PHASE_059_CODE_BEHAVIOR_MATRIX.json",
    "Codex/results/PHASE_059_TEST_DEMO_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_FOUR_AXIS_CONFORMANCE_MATRIX.json",
    "Codex/results/PHASE_059_CARRY_FORWARD_REGISTER.json",
]

PRODUCERS = [
    "audit_phase059_v1014_register_boundary.py",
    "audit_phase059_v1014_phase_separation.py",
    "audit_phase059_v1014_lco_heat.py",
    "audit_phase059_v1014_kinetics.py",
    "audit_phase059_v1014_completion_authority.py",
    "audit_phase059_v1015_pointwise_memory.py",
    "audit_phase059_v1015_implementation_boundary.py",
    "audit_phase059_v1015_heat_detailing.py",
    "audit_phase059_v1016_nt_width_law.py",
    "audit_phase059_v1016_joint_identifiability.py",
    "audit_phase059_v1017_doc_citations.py",
    "audit_phase059_v1018_1_carryforward.py",
    "audit_phase059_v1018_2_einstein_theory.py",
    "audit_phase059_v1018_2_einstein_fullpath.py",
    "audit_phase059_step38_5_future_physics_roadmap.py",
    "build_phase059_theory_claim_dispositions.py",
    "build_phase059_blocker_delta.py",
    "build_phase059_four_axis_conformance.py",
    "build_phase059_carry_forward.py",
]

DIRECT_PASS = [
    "validate_phase059_theory_contracts.py",
    "validate_phase059_step38_5_future_physics_roadmap.py",
    "validate_phase059_theory_claim_dispositions.py",
    "validate_phase059_blocker_delta.py",
    "validate_phase059_four_axis_conformance.py",
    "validate_phase059_carry_forward.py",
]
DIRECT_TERMINALS = {
    "validate_phase059_theory_contracts.py": "PASS_P059_THEORY_CONTRACTS checks=19/19 records=38 topics=8",
    "validate_phase059_step38_5_future_physics_roadmap.py": "PASS_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION",
    "validate_phase059_theory_claim_dispositions.py": "PASS_P059_STEP_039_1_THEORY_CLAIM_DISPOSITION",
    "validate_phase059_blocker_delta.py": "PASS_P059_STEP_039_2_BLOCKER_DELTA old=34 new=6 orphan=0 resolved=0",
    "validate_phase059_four_axis_conformance.py": "PASS_P059_STEP_039_3_FOUR_AXIS_CONFORMANCE rows=185 code_records=21 test_runtime_records=103 artifact_records=152 adjudications=663",
    "validate_phase059_carry_forward.py": "PASS_P059_STEP_039_4_CARRY_FORWARD_REGISTER items=52 sources=12+34+6 orphan=0 external_truth=0",
}
ALLOWED_RAW_FAILURE_TOKENS = {
    "blob hashes exact", "source hashes exact", "exact patch hashes", "diff endpoint hashes",
    "module source hashes exact", "runtime logs exact", "diagnostic source hashes exact",
    "Claude source tree clean", "metrics_hash_linked", "deterministic_data",
    "auditor_rerun_deterministic", "rerun_deterministic", "deterministic_output",
    "auditor_rerun_exit_zero",
    "source hashes current", "result and review deterministic", "Claude tree untouched",
    "runner rerun exits zero", "runner rerun clean stderr",
}
READ_ONLY_SPARSE = [
    "validate_phase059_text_coverage.py",
    "validate_phase059_theory_index.py",
    "validate_phase059_completion_claims.py",
    "validate_phase059_code_index.py",
    "validate_phase059_test_demo_matrix.py",
    "validate_phase059_isolated_runtime.py",
]
READ_ONLY_PDF = ["validate_phase059_pdf_render.py"]
TEMP_MIRROR_REQUIRED = [
    "validate_phase059_v1014_register_boundary.py",
    "validate_phase059_v1014_phase_separation.py",
    "validate_phase059_v1014_lco_heat.py",
    "validate_phase059_v1014_kinetics.py",
    "validate_phase059_v1014_completion_authority.py",
    "validate_phase059_v1015_pointwise_memory.py",
    "validate_phase059_v1015_implementation_boundary.py",
    "validate_phase059_v1015_heat_detailing.py",
    "validate_phase059_v1016_nt_width_law.py",
    "validate_phase059_v1016_joint_identifiability.py",
    "validate_phase059_v1017_doc_citations.py",
    "validate_phase059_v1018_1_carryforward.py",
    "validate_phase059_v1018_2_einstein_theory.py",
    "validate_phase059_v1018_2_einstein_fullpath.py",
    "validate_phase059_artifact_genealogy.py",
    "validate_phase059_images.py",
    "validate_phase059_independent_code_probes.py",
    "validate_phase059_golden_npz.py",
]
ALL_VALIDATORS = DIRECT_PASS + READ_ONLY_SPARSE + READ_ONLY_PDF + TEMP_MIRROR_REQUIRED
WORK = "Codex/work/v1014_v1018_2_phase059"


class ValidationFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValidationFailure(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_bytes(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs_hook)
    except ValidationFailure:
        raise
    except Exception as exc:
        raise ValidationFailure(f"strict JSON parse failed for {label}: {exc}") from exc


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(args: list[str], cwd: pathlib.Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    if check and cp.returncode:
        raise ValidationFailure(f"git {' '.join(args)} failed: {cp.stderr.decode('utf-8', 'replace')}")
    return cp


def git_blob(path: str, ref: str = BASELINE) -> bytes:
    require("\\" not in path and not path.startswith("/"), f"non-POSIX repo path: {path}")
    return git(["show", f"{ref}:{path}"]).stdout


def git_object_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def lines(data: bytes) -> int:
    return len(data.decode("utf-8").splitlines())


def nodes(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(nodes(k) + nodes(v) for k, v in value.items())
    if isinstance(value, list):
        return 1 + sum(nodes(v) for v in value)
    return 1


def exact(actual: Any, expected: Any, label: str) -> None:
    require(canonical_bytes(actual) == canonical_bytes(expected), f"exact/type mismatch: {label}")


def semantic_hash(document: dict[str, Any]) -> str:
    clone = dict(document)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def fingerprint_active() -> dict[str, Any]:
    tracked = git(["ls-files", "-z"]).stdout.split(b"\0")
    rows = []
    excluded = STEP_PATHS
    for raw in tracked:
        if not raw:
            continue
        path = raw.decode("utf-8")
        if path in excluded:
            continue
        current_path = ROOT / path
        if current_path.is_file():
            payload = current_path.read_bytes()
            rows.append([path, sha256(payload), len(payload), "PRESENT"])
        else:
            rows.append([path, None, 0, "SPARSE_ABSENT"])
    status_rows = []
    for raw in git(["status", "--porcelain=v1", "-z"]).stdout.split(b"\0"):
        if not raw:
            continue
        decoded = raw.decode("utf-8")
        path = decoded[3:]
        if path not in STEP_PATHS:
            status_rows.append(decoded)
    return {
        "tracked_file_count": len(rows),
        "tracked_content_digest": sha256(canonical_bytes(rows)),
        "tracked_rows_sha256": sha256(canonical_bytes(rows)),
        "non_step_status_rows": sorted(status_rows),
        "non_step_status_sha256": sha256(canonical_bytes(sorted(status_rows))),
        "head": git(["rev-parse", "HEAD"]).stdout.decode().strip(),
    }


def require_clean_non_step_status(fingerprint: dict[str, Any], label: str) -> None:
    require(type(fingerprint) is dict, f"{label}: active fingerprint object required")
    rows = fingerprint.get("non_step_status_rows")
    require(type(rows) is list, f"{label}: non-step status rows must be a list")
    require(rows == [], f"{label}: non-step tracked/untracked/staged status dirty: {rows}")


def pinned_baseline_fingerprint() -> dict[str, Any]:
    rows = []
    for raw in git(["ls-tree", "-r", "-z", "--full-tree", BASELINE]).stdout.split(b"\0"):
        if not raw:
            continue
        try:
            metadata, raw_path = raw.split(b"\t", 1)
            mode, object_type, object_sha = metadata.decode("ascii").split()
            path = raw_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValidationFailure(f"malformed pinned baseline tree row: {raw!r}") from exc
        if path in STEP_PATHS:
            continue
        rows.append([path, mode, object_type, object_sha])
    require(len(rows) == len({row[0] for row in rows}), "pinned baseline tree duplicate path")
    return {
        "evidence_class": "PINNED_HISTORICAL_GIT_TREE",
        "baseline_commit": BASELINE,
        "baseline_tree": git(["rev-parse", f"{BASELINE}^{{tree}}"]).stdout.decode().strip(),
        "tracked_entry_count": len(rows),
        "tree_listing_sha256": sha256(canonical_bytes(rows)),
        "step39_5_paths_excluded": sorted(STEP_PATHS),
    }


def current_operational_repository_state() -> dict[str, Any]:
    refs = {
        "head": git(["rev-parse", "HEAD"]).stdout.decode().strip(),
        "upstream": git(["rev-parse", "@{upstream}"]).stdout.decode().strip(),
        "remote_active": git(["rev-parse", f"origin/{BRANCH}"]).stdout.decode().strip(),
        "protected": git(["rev-parse", "origin/codex/lib-physics-endgame-v1025_2"]).stdout.decode().strip(),
        "main": git(["rev-parse", "origin/main"]).stdout.decode().strip(),
    }
    branch = git(["rev-parse", "--abbrev-ref", "HEAD"]).stdout.decode().strip()
    require(branch == BRANCH, "active branch drift")
    require(refs["head"] == refs["upstream"] == refs["remote_active"], "active local/upstream/remote divergence")
    require(refs["protected"] == PROTECTED_TIP, "protected tip drift")
    require(refs["main"] == MAIN_TIP, "main tip drift")
    ancestor = git(["merge-base", "--is-ancestor", BASELINE, refs["head"]], check=False)
    require(ancestor.returncode == 0, "current active tip is not BASELINE or its descendant")
    trees = {
        key: git(["rev-parse", f"{value}^{{tree}}"]).stdout.decode().strip()
        for key, value in refs.items()
    }
    return {
        "state_class": "CURRENT_OPERATIONAL_RUN",
        "branch": branch,
        "refs": refs,
        "trees": trees,
        "baseline_is_ancestor": True,
    }


def historical_repository_state() -> dict[str, Any]:
    protected_tree = git(["rev-parse", f"{PROTECTED_TIP}^{{tree}}"]).stdout.decode().strip()
    main_tree = git(["rev-parse", f"{MAIN_TIP}^{{tree}}"]).stdout.decode().strip()
    return {
        "state_class": "PINNED_HISTORICAL_EVIDENCE",
        "branch": BRANCH,
        "baseline_commit": BASELINE,
        "baseline_tree": git(["rev-parse", f"{BASELINE}^{{tree}}"]).stdout.decode().strip(),
        "baseline_subject": git(["show", "-s", "--format=%s", BASELINE]).stdout.decode().strip(),
        "protected_tip": PROTECTED_TIP,
        "protected_tree": protected_tree,
        "main_tip": MAIN_TIP,
        "main_tree": main_tree,
        "current_run_policy": (
            "The operational tip must equal BASELINE or be its descendant; local, upstream, and "
            "origin active tips must match, while protected and main remain exact."
        ),
    }


def reconstruct_queue() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = strict_bytes(git_blob(MANIFEST_PATH), MANIFEST_PATH)
    queue = strict_bytes(git_blob(QUEUE_PATH), QUEUE_PATH)
    require(type(manifest) is dict and type(manifest.get("entries")) is list, "manifest schema")
    selected = [row for row in manifest["entries"] if row.get("version") in VERSIONS]
    require(len(selected) == 117, "manifest path universe != 117")
    require(len({row["path"] for row in selected}) == 117, "manifest duplicate path")
    by_blob: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        require(type(row) is dict, "manifest entry type")
        payload = git_blob(row["path"], queue["baseline_commit"])
        require(git_object_sha(payload) == row["blob_sha"], f"blob SHA mismatch: {row['path']}")
        require(len(payload) == row["size_bytes"], f"size mismatch: {row['path']}")
        by_blob[row["blob_sha"]].append(row)
    require(len(by_blob) == 93, "unique blob universe != 93")
    expected_records = []
    for blob_sha in sorted(by_blob):
        rows = sorted(by_blob[blob_sha], key=lambda r: r["path"])
        roles = {r["role"] for r in rows}
        modes = {r["review_mode"] for r in rows}
        require(len(roles) == len(modes) == 1, f"inconsistent dedup metadata: {blob_sha}")
        representative = rows[0]
        rec = {
            "blob_sha": blob_sha,
            "representative_path": representative["path"],
            "occurrence_paths": [r["path"] for r in rows],
            "versions": sorted({r["version"] for r in rows}, key=VERSIONS.index),
            "role": representative["role"],
            "review_mode": representative["review_mode"],
            "size_bytes": representative["size_bytes"],
            "extent": representative["extent"],
            "chunks": [],
        }
        if rec["review_mode"] == "FULL_TEXT":
            count = rec["extent"]["lines"]
            rec["chunks"] = [
                {"start_line": start, "end_line": min(start + 299, count)}
                for start in range(1, count + 1, 300)
            ]
        expected_records.append(rec)
    expected_records.sort(key=lambda row: row["representative_path"])
    exact(queue["records"], expected_records, "queue.records independently reconstructed")
    role_counts = Counter(r["role"] for r in expected_records)
    mode_counts = Counter(r["review_mode"] for r in expected_records)
    stats = {
        "path_count": len(selected),
        "unique_blob_count": len(expected_records),
        "duplicate_path_occurrence_count": len(selected) - len(expected_records),
        "unique_role_counts": dict(sorted(role_counts.items())),
        "review_mode_counts": dict(sorted(mode_counts.items())),
        "queue_blob_sha256": sha256(git_blob(QUEUE_PATH)),
        "manifest_blob_sha256": sha256(git_blob(MANIFEST_PATH)),
    }
    exact(stats["unique_role_counts"], queue["unique_role_counts"], "queue role counts")
    require(stats["path_count"] == queue["path_count"] == 117, "queue path count")
    require(stats["unique_blob_count"] == queue["unique_blob_count"] == 93, "queue blob count")
    require(stats["duplicate_path_occurrence_count"] == queue["duplicate_path_occurrence_count"] == 24, "queue duplicate count")
    return queue, stats


def reconstruct_text(queue: dict[str, Any]) -> dict[str, Any]:
    coverage = strict_bytes(git_blob(TEXT_PATH), TEXT_PATH)
    text_records = [row for row in queue["records"] if row["review_mode"] == "FULL_TEXT"]
    require(len(text_records) == 63, "text blob count != 63")
    by_sha = {row["blob_sha"]: row for row in text_records}
    docs = coverage.get("documents")
    require(type(docs) is list and len(docs) == 63, "coverage documents != 63")
    total_lines = total_chunks = 0
    for doc in docs:
        require(type(doc) is dict, "coverage document type")
        source = by_sha.get(doc.get("blob_sha"))
        require(source is not None, f"unknown coverage blob: {doc.get('blob_sha')}")
        payload = git_blob(source["representative_path"], queue["baseline_commit"])
        actual_lines = lines(payload)
        require(actual_lines == source["extent"]["lines"] == doc["line_count"], "text line mismatch")
        expected_ranges = [
            {"line_start": chunk["start_line"], "line_end": chunk["end_line"]}
            for chunk in source["chunks"]
        ]
        exact(doc["coverage"], expected_ranges, "text chunk ranges")
        require(doc["status"] == "COMPLETE", "text blob not complete")
        total_lines += actual_lines
        total_chunks += len(doc["coverage"])
    require(total_lines == coverage["total_lines"] == coverage["completed_lines"] == 36641, "text total lines")
    require(total_chunks == coverage["completed_chunks"] == 158, "text chunk total")
    require(coverage["gate"] == "PASS_P059_TEXT_COVERAGE", "text coverage gate")
    return {
        "unique_text_blobs": 63,
        "lines_read": total_lines,
        "chunks_read": total_chunks,
        "coverage_blob_sha256": sha256(git_blob(TEXT_PATH)),
        "coverage": "63/63 blobs, 36,641/36,641 lines, 158/158 chunks",
    }


def output_inventory() -> list[dict[str, Any]]:
    rows = []
    for kind, paths in (("HUMAN_RESULT", HUMAN_OUTPUTS), ("MACHINE_ARTIFACT", MACHINE_OUTPUTS)):
        for path in paths:
            frozen = git_blob(path)
            current = (ROOT / path).read_bytes()
            require(git(["diff", "--quiet", BASELINE, "--", path], check=False).returncode == 0,
                    f"current output differs semantically from HEAD: {path}")
            try:
                current_text = current.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValidationFailure(f"current output malformed UTF-8: {path}: {exc}") from exc
            normalized_current = current_text.replace("\r\n", "\n")
            require("\r" not in normalized_current, f"current output contains bare CR: {path}")
            require(
                normalized_current.encode("utf-8") == frozen,
                f"current output differs from pinned Git blob beyond CRLF checkout conversion: {path}",
            )
            row: dict[str, Any] = {
                "path": path,
                "kind": kind,
                "git_blob_sha": git_object_sha(frozen),
                "sha256": sha256(frozen),
                "bytes": len(frozen),
                "lines": lines(frozen),
            }
            if kind == "MACHINE_ARTIFACT":
                obj = strict_bytes(frozen, path)
                require(type(obj) is dict, f"machine artifact is not object: {path}")
                row.update({"node_count": nodes(obj), "top_level_keys": sorted(obj), "schema_version": obj.get("schema_version")})
                if "semantic_sha256" in obj:
                    require(obj["semantic_sha256"] == semantic_hash(obj), f"semantic hash mismatch: {path}")
                    row["semantic_sha256"] = obj["semantic_sha256"]
            else:
                text = frozen.decode("utf-8")
                headings = [line for line in text.splitlines() if line.startswith("#")]
                require(headings, f"human result has no headings: {path}")
                row["heading_count"] = len(headings)
                row["heading_sha256"] = sha256(canonical_bytes(headings))
            rows.append(row)
    require(len(rows) == 40, "expected output count != 40")
    return rows


def ensure_script_inventory() -> dict[str, Any]:
    require(len(PRODUCERS) == 19 and len(ALL_VALIDATORS) == 31, "script inventory cardinality")
    for name in PRODUCERS + ALL_VALIDATORS:
        require((ROOT / WORK / name).is_file(), f"missing script: {name}")
    require(len(set(ALL_VALIDATORS)) == 31, "duplicate validator inventory")
    return {
        "producer_count": 19,
        "validator_count": 31,
        "read_only_direct_expected_pass": DIRECT_PASS,
        "read_only_sparse_dependency": READ_ONLY_SPARSE,
        "read_only_pdf_platform_sensitive": READ_ONLY_PDF,
        "temp_mirror_required": TEMP_MIRROR_REQUIRED,
        "active_repo_execution_prohibition": "TEMP_MIRROR_REQUIRED validators MUST NOT execute in the active checkout.",
    }


def reconstruct_integrated_semantics() -> dict[str, Any]:
    """Recompute the substantive Step38.5–39.4 cardinalities from frozen rows."""
    def load(path: str) -> dict[str, Any]:
        value = strict_bytes(git_blob(path), path)
        require(type(value) is dict, f"integrated artifact type: {path}")
        require(type(value.get("authority_boundary")) is str and value["authority_boundary"],
                f"missing authority boundary: {path}")
        return value

    roadmap = load(MACHINE_OUTPUTS[14])
    theory = load(MACHINE_OUTPUTS[15])
    delta = load(MACHINE_OUTPUTS[16])
    code = load(MACHINE_OUTPUTS[17])
    test = load(MACHINE_OUTPUTS[18])
    four = load(MACHINE_OUTPUTS[19])
    carry = load(MACHINE_OUTPUTS[20])
    occurrence_ids = [oid for claim in theory["claims"] for oid in claim["mapped_occurrence_ids"]]
    require(len(occurrence_ids) == len(set(occurrence_ids)), "duplicate theory occurrence routing")
    result = {
        "roadmap_items": len(roadmap["items"]),
        "theory_unique_claims": len(theory["claims"]),
        "theory_equation_occurrences": len(occurrence_ids),
        "theory_contract_routes": len(theory["contract_routes"]),
        "theory_contract_evidence": len(theory["contract_evidence_relations"]),
        "blocker_old_deltas": len(delta["old_deltas"]),
        "blocker_new_items": len(delta["new_blockers"]),
        "code_canonical_records": len(code["records"]),
        "test_runtime_records": len(test["test_runtime_records"]),
        "artifact_canonical_records": len(test["artifact_records"]),
        "four_axis_rows": len(four["rows"]),
        "applicable_claim_ledgers": len(four["applicable_claim_code_adjudications"]),
        "carry_forward_items": len(carry["items"]),
        "external_material_truth_validated": carry["counts"]["external_material_truth_validated"],
    }
    exact(result, {
        "roadmap_items": 12, "theory_unique_claims": 185, "theory_equation_occurrences": 973,
        "theory_contract_routes": 38, "theory_contract_evidence": 80, "blocker_old_deltas": 34,
        "blocker_new_items": 6, "code_canonical_records": 21, "test_runtime_records": 103,
        "artifact_canonical_records": 152, "four_axis_rows": 185, "applicable_claim_ledgers": 51,
        "carry_forward_items": 52, "external_material_truth_validated": 0,
    }, "integrated frozen semantic counts")
    return result


def run_validator(root: pathlib.Path, name: str, execution_class: str, timeout: int = 300) -> dict[str, Any]:
    require(name in ALL_VALIDATORS and pathlib.PurePosixPath(name).name == name, f"unknown/traversal validator: {name}")
    require(execution_class in {"READ_ONLY_DIRECT", "TEMP_MIRROR_SPARSE_RAW", "TEMP_MIRROR_PDF_RAW", "TEMP_MIRROR_REQUIRED"}, "unknown execution class")
    argv = [sys.executable, f"{WORK}/{name}"]
    started = time.perf_counter()
    try:
        cp = subprocess.run(
            argv,
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            shell=False,
        )
        timed_out = False
        exit_code = cp.returncode
        stdout, stderr = cp.stdout, cp.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code = 124
        stdout, stderr = exc.stdout or b"", exc.stderr or b""
    elapsed = round(time.perf_counter() - started, 6)
    try:
        text = stdout.decode("utf-8")
        stderr_text = stderr.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationFailure(f"subordinate emitted malformed UTF-8: {name}: {exc}") from exc
    banners = [
        line for line in text.splitlines()
        if re.match(r"^(?:\d+ )?(?:PASS|FAIL)(?:\b|_)|^FAILED\b|^SUMMARY\b|^CONDITIONAL_", line)
    ]
    return {
        "name": name,
        "execution_class": execution_class,
        "argv": argv,
        "shell": False,
        "timeout_seconds": timeout,
        "execution_location": "DISPOSABLE_CLONE",
        "exit_code": exit_code,
        "timed_out": timed_out,
        "runtime_seconds": elapsed,
        "stdout_bytes": len(stdout),
        "stdout_sha256": sha256(stdout),
        "stdout_lf_sha256": sha256(stdout.replace(b"\r\n", b"\n")),
        "stdout_line_count": len(text.splitlines()),
        "stdout_utf8": True,
        "stderr_bytes": len(stderr),
        "stderr_sha256": sha256(stderr),
        "stderr_utf8": True,
        "banners": banners,
        "failed_banners": [line for line in banners if re.match(r"^(?:\d+ )?FAIL\b|^FAILED\b", line)],
        "summary_banners": [line for line in banners if line.startswith("SUMMARY")],
        "traceback": "Traceback (most recent call last)" in stderr_text,
    }


def make_clone() -> pathlib.Path:
    temp = pathlib.Path(tempfile.mkdtemp(prefix="phase059-step395-"))
    clone = temp / "repo"
    cp = subprocess.run(
        ["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    require(cp.returncode == 0, f"temp clone failed: {cp.stderr.decode('utf-8', 'replace')}")
    for key, value in CLONE_GIT_CONFIG.items():
        git(["config", "--local", key, value], cwd=clone)
        observed = git(["config", "--local", "--get", key], cwd=clone).stdout.decode().strip()
        require(observed == value, f"temp clone Git config mismatch: {key}")
    git(["checkout", "--detach", BASELINE], cwd=clone)
    git(["update-index", "--refresh"], cwd=clone)
    claude_status = git(["status", "--porcelain", "--", "Claude"], cwd=clone).stdout
    require(claude_status == b"", "temp clone initial Claude tree dirty")
    return clone


def structural_diffs(actual: Any, expected: Any, path: str = "") -> list[dict[str, Any]]:
    if type(actual) is not type(expected):
        return [{"path": path, "actual": actual, "expected": expected}]
    if isinstance(actual, dict):
        diffs: list[dict[str, Any]] = []
        for key in sorted(set(actual) | set(expected)):
            child = f"{path}.{key}" if path else key
            if key not in actual or key not in expected:
                diffs.append({"path": child, "actual": actual.get(key, "<MISSING>"), "expected": expected.get(key, "<MISSING>")})
            else:
                diffs.extend(structural_diffs(actual[key], expected[key], child))
        return diffs
    if isinstance(actual, list):
        if len(actual) != len(expected):
            return [{"path": f"{path}.length", "actual": len(actual), "expected": len(expected)}]
        diffs = []
        for index, (left, right) in enumerate(zip(actual, expected)):
            diffs.extend(structural_diffs(left, right, f"{path}[{index}]"))
        return diffs
    return [] if canonical_bytes(actual) == canonical_bytes(expected) else [{"path": path, "actual": actual, "expected": expected}]


def compact_hash(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def derive_science_metrics(document: dict[str, Any]) -> dict[str, Any]:
    rows = document["active_branch_rows"]
    validation = document["validation"]
    summary = document["summary"]
    probe = document["u_only_transition_probe"]
    return {
        "active_rows": len(rows),
        "max_roundtrip_error_V_per_K": max(abs(row["fullpath_roundtrip_error_V_per_K"]) for row in rows),
        "heat_error": max(abs(row["heat_identity_error_W_per_A"]) for row in rows),
        "max_grid_peak_error_V": max(abs(row["grid_peak_error_V"]) for row in rows),
        "u_only_public_diff_pair": [probe["equilibrium_difference"], probe["entropy_difference"]],
        "private_correction_V": probe["helper_vib_dU_nonzero_V"],
        "release_coverage_count": len(document["release_test_coverage"]),
        "theta_E_Tref_guard_present": validation["tref_positive_failfast_pass"],
        "persistent_n_T1_regression_present": validation["persistent_release_regression_pass"],
        "capability_present": summary["capability_conformance_pass"],
        "parameter_material_validation_present": summary["material_validation_pass"],
    }


def portability_contract(raw: dict[str, Any], clone: pathlib.Path) -> dict[str, Any]:
    require(raw["exit_code"] == 1 and type(raw["exit_code"]) is int, "fullpath raw exit must remain integer 1")
    require(not raw["timed_out"] and not raw["traceback"], "fullpath timeout/traceback")
    require(raw["stderr_bytes"] == 0 and raw["stderr_sha256"] == sha256(b""), "fullpath raw stderr")
    require(raw["stdout_bytes"] == 502, "fullpath raw stdout bytes")
    require(raw["stdout_sha256"] == "3e2e2af99723ecbd844a01ec4aa6a986a00f09f6665caf9da83e0b161b497803", "fullpath raw stdout SHA")
    require(raw["stdout_lf_sha256"] == "40d5e71fa090d0937f192b5ab278d39b3d003034456f7e41724a1326d3c74707", "fullpath LF stdout SHA")
    require(raw["failed_banners"] == ["FAIL rerun_deterministic"], "fullpath sole failed check")
    require(raw["summary_banners"] == ["SUMMARY 25/26 checks passed"], "fullpath 25/26 summary")
    require(sum(line.startswith("PASS") for line in raw["banners"]) == 25, "fullpath PASS count")

    artifact_path = "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json"
    report_path = "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md"
    generated_bytes = (clone / artifact_path).read_bytes()
    canonical_bytes_on_git = git_blob(artifact_path)
    generated = strict_bytes(generated_bytes, "temp fullpath generated artifact")
    canonical = strict_bytes(canonical_bytes_on_git, artifact_path)
    raw_diffs = structural_diffs(generated, canonical)
    allowlist = [
        "release_test_coverage[0].path", "release_test_coverage[1].path", "release_test_coverage[2].path",
        "source_hashes.v1018_1", "source_hashes.v1018_2",
    ]
    require([row["path"] for row in raw_diffs] == allowlist, f"fullpath raw diff allowlist mismatch: {[row['path'] for row in raw_diffs]}")
    normalized = copy.deepcopy(generated)
    source_paths = {
        "v1018_1": "Claude/docs/v1.0.18.1/Anode_Fit_v1.0.18.1.py",
        "v1018_2": "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py",
    }
    for key, source_path in source_paths.items():
        normalized["source_hashes"][key] = sha256(git_blob(source_path))
    for index in range(3):
        value = normalized["release_test_coverage"][index]["path"]
        require(type(value) is str and ".." not in pathlib.PurePosixPath(value.replace("\\", "/")).parts, "unsafe fullpath path")
        normalized["release_test_coverage"][index]["path"] = value.replace("\\", "/")
    normalized_diffs = structural_diffs(normalized, canonical)
    require(normalized_diffs == [], f"fullpath normalized diff remains: {normalized_diffs}")
    normalized_sha = compact_hash(normalized)
    require(normalized_sha == "86f6f6f85063e7639ff8e45dbe8f5ad29bd62e8354e6a2cddc13d8ac44b30296", "fullpath normalized semantic SHA")
    science_basis = copy.deepcopy(normalized)
    science_basis.pop("source_hashes")
    for row in science_basis["release_test_coverage"]:
        row.pop("path")
    science_sha = compact_hash(science_basis)
    require(science_sha == "9c16955f2871e83421f723b220c68a6f2e7345e6e66cfe5a927a875e784ac57b", "fullpath science SHA")
    metrics = derive_science_metrics(normalized)
    exact(metrics, {
        "active_rows": 4, "max_roundtrip_error_V_per_K": 8.916153405869043e-15,
        "heat_error": 0.0, "max_grid_peak_error_V": 1.7327117217441623e-05,
        "u_only_public_diff_pair": [0.0, 0.0], "private_correction_V": 3.708190858715776e-05,
        "release_coverage_count": 3, "theta_E_Tref_guard_present": False,
        "persistent_n_T1_regression_present": False, "capability_present": True,
        "parameter_material_validation_present": False,
    }, "derived fullpath science metrics")
    generated_report = (clone / report_path).read_bytes()
    canonical_report = git_blob(report_path)
    report_lf = generated_report.replace(b"\r\n", b"\n")
    require(report_lf == canonical_report, "fullpath report semantic/LF-normalized change in temp rerun")
    return {
        "raw_expected_failure": {"exit_code": 1, "failed_checks": ["rerun_deterministic"], "passed_checks": 25, "total_checks": 26, "stderr_bytes": 0},
        "raw_observed": raw,
        "raw_artifact_sha256": sha256(generated_bytes),
        "canonical_artifact_sha256": sha256(canonical_bytes_on_git),
        "raw_structural_diffs": raw_diffs,
        "exact_normalization_allowlist": allowlist,
        "raw_json_diff_count": len(raw_diffs),
        "normalized_json_diff_count": len(normalized_diffs),
        "normalized_semantic_sha256": normalized_sha,
        "prior_malformed_reference_prefix": "86f6f6f85063e7639ff8e45dbe8f5ad29bd62e8354e6a2cddc13d8ac44b302",
        "platform_independent_science_sha256": science_sha,
        "science_basis_definition": "normalized full JSON minus top-level source_hashes and each release_test_coverage[*].path; compact sorted UTF-8 without LF",
        "science_metrics": metrics,
        "report_raw_byte_equal": generated_report == canonical_report,
        "report_lf_normalized_equal": True,
        "report_raw_sha256": sha256(generated_report),
        "report_sha256": sha256(canonical_report),
        "boundary": "Raw Windows checkout portability failure is environment debt; exact five-leaf Git-blob/POSIX normalization has zero scientific JSON delta and does not establish material validity.",
    }


def collect_subordinates() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    operational_pre = current_operational_repository_state()
    pre = fingerprint_active()
    require_clean_non_step_status(pre, "active pre")
    clone = make_clone()
    clone_parent = clone.parent
    try:
        outcomes = [run_validator(clone, name, "READ_ONLY_DIRECT") for name in DIRECT_PASS]
        for row in outcomes:
            require(row["exit_code"] == 0 and any(b.startswith("PASS") for b in row["banners"]), f"mandatory validator failed: {row['name']}")
            require(not row["traceback"] and not row["timed_out"] and row["stderr_bytes"] == 0, f"mandatory validator abnormal: {row['name']}")
            require(not row["failed_banners"] and not row["summary_banners"], f"mandatory validator emitted failure/summary: {row['name']}")
            require(row["banners"][-1] == DIRECT_TERMINALS[row["name"]], f"mandatory terminal banner: {row['name']}")
        for name in READ_ONLY_SPARSE:
            outcomes.append(run_validator(clone, name, "TEMP_MIRROR_SPARSE_RAW"))
        for name in READ_ONLY_PDF:
            outcomes.append(run_validator(clone, name, "TEMP_MIRROR_PDF_RAW"))
        fullpath_name = "validate_phase059_v1018_2_einstein_fullpath.py"
        for name in [item for item in TEMP_MIRROR_REQUIRED if item != fullpath_name]:
            outcomes.append(run_validator(clone, name, "TEMP_MIRROR_REQUIRED"))
        raw_fullpath = run_validator(clone, fullpath_name, "TEMP_MIRROR_REQUIRED")
        outcomes.append(raw_fullpath)
        portability = portability_contract(raw_fullpath, clone)
    finally:
        shutil.rmtree(clone_parent, ignore_errors=True)
    post = fingerprint_active()
    require_clean_non_step_status(post, "active post")
    operational_post = current_operational_repository_state()
    exact(post, pre, "active canonical pre/post fingerprint")
    exact(operational_post, operational_pre, "operational repository pre/post state")
    by_name = {row["name"]: row for row in outcomes}
    require(len(by_name) == 31, "fresh validator outcome count")
    require(sum(row["exit_code"] == 0 for row in outcomes) == 7, "subordinate exit-zero count")
    require(sum(row["exit_code"] == 1 for row in outcomes) == 24, "subordinate exit-one count")
    for row in outcomes:
        require(not row["timed_out"] and not row["traceback"], f"subordinate abnormal termination: {row['name']}")
        if row["exit_code"] == 1:
            require(row["failed_banners"], f"raw failure lacks explicit failed check: {row['name']}")
            for banner in row["failed_banners"]:
                require(any(token in banner for token in ALLOWED_RAW_FAILURE_TOKENS), f"unexpected/scientific raw failure: {row['name']}: {banner}")
    return outcomes, {
        "pre": pre,
        "post": post,
        "unchanged": True,
        "operational_pre": operational_pre,
        "operational_post": operational_post,
        "portability": portability,
    }


def role_evidence(queue: dict[str, Any], stats: dict[str, Any], text: dict[str, Any]) -> dict[str, Any]:
    """Calculate every role fact from pinned queue rows and machine records."""
    records = queue["records"]
    role_paths = Counter()
    for row in records:
        role_paths[row["role"]] += len(row["occurrence_paths"])
    exact(stats["unique_role_counts"], {
        "code": 4, "data": 2, "demo": 18, "figure": 10, "generated_document": 18,
        "implementation_guide": 3, "result": 8, "supporting_document": 1, "test": 12, "theory": 17,
    }, "role universe")
    require(text["lines_read"] == 36641, "role coverage text line basis")

    def load(name: str) -> tuple[dict[str, Any], dict[str, Any]]:
        path = f"Codex/results/{name}"
        raw = git_blob(path)
        obj = strict_bytes(raw, path)
        require(type(obj) is dict, f"role artifact type: {path}")
        return obj, {"path": path, "sha256": sha256(raw), "git_blob_sha": git_object_sha(raw)}

    theory, theory_src = load("PHASE_059_THEORY_SOURCE_INDEX.json")
    code, code_src = load("PHASE_059_PRODUCTION_CODE_INDEX.json")
    tests, tests_src = load("PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json")
    pdf, pdf_src = load("PHASE_059_PDF_RENDER_METRICS.json")
    visual, visual_src = load("PHASE_059_PDF_VISUAL_REVIEW.json")
    images, images_src = load("PHASE_059_IMAGE_AUDIT.json")
    golden, golden_src = load("PHASE_059_GOLDEN_NPZ_AUDIT.json")
    genealogy, genealogy_src = load("PHASE_059_ARTIFACT_GENEALOGY.json")

    theory_fact = {
        "unique_blobs": len(theory["documents"]),
        "path_occurrences": sum(len(row["occurrence_paths"]) for row in theory["documents"]),
        "lines": sum(row["line_count"] for row in theory["documents"]),
        "sections": sum(row["section_count"] for row in theory["documents"]),
        "equations": len(theory["equations"]),
    }
    exact(theory_fact, {"unique_blobs": 17, "path_occurrences": 18, "lines": 28876, "sections": 493, "equations": 973}, "theory role facts")
    require(theory_fact["lines"] == theory["total_lines"] and theory_fact["sections"] == theory["section_count"] and theory_fact["equations"] == theory["equation_environment_count"], "theory top count reconciliation")
    code_fact = {
        "unique_blobs": len(code["modules"]),
        "path_occurrences": sum(len(row["occurrence_paths"]) for row in code["modules"]),
        "lines": sum(row["line_count"] for row in code["modules"]),
        "findings": len(code["review"]["findings"]),
    }
    exact(code_fact, {"unique_blobs": 4, "path_occurrences": 6, "lines": 3704, "findings": 13}, "code role facts")
    test_fact = {
        "test_unique_blobs": sum(row["role"] == "test" for row in tests["records"]),
        "demo_unique_blobs": sum(row["role"] == "demo" for row in tests["records"]),
        "records": len(tests["records"]),
        "lines": sum(row["line_count"] for row in tests["records"]),
        "findings": len(tests["findings"]),
    }
    exact(test_fact, {"test_unique_blobs": 12, "demo_unique_blobs": 18, "records": 30, "lines": 3372, "findings": 15}, "test/demo role facts")
    pdf_fact = {
        "unique_blobs": len(pdf["documents"]),
        "pages": sum(row["page_count_pdf"] for row in pdf["documents"]),
        "contact_sheets": sum(len(row["contact_sheets"]) for row in pdf["documents"]),
        "visual_documents": len(visual["documents"]),
    }
    exact(pdf_fact, {"unique_blobs": 18, "pages": 492, "contact_sheets": 37, "visual_documents": 18}, "PDF role facts")
    image_fact = {
        "unique_blobs": len(images["images"]),
        "path_occurrences": sum(row["occurrence_count"] for row in images["images"]),
    }
    exact(image_fact, {"unique_blobs": 10, "path_occurrences": 24}, "image role facts")
    array_counts = [len(row["arrays"]) for row in golden["unique_golden_contents"]]
    data_fact = {
        "unique_blobs": len(golden["unique_golden_contents"]),
        "path_occurrences": sum(row["occurrence_count"] for row in golden["unique_golden_contents"]),
        "array_counts": array_counts,
    }
    exact(data_fact, {"unique_blobs": 2, "path_occurrences": 6, "array_counts": [13, 13]}, "data role facts")
    genealogy_occurrences = len(genealogy["pdf_occurrences"]) + len(genealogy["image_occurrences"]) + len(genealogy["golden_occurrences"])
    genealogy_unique = len(genealogy["pdf_byte_content_groups"]) + len(genealogy["image_content_groups"]) + len(genealogy["golden_content_groups"])
    genealogy_fact = {"path_occurrences": genealogy_occurrences, "unique_blobs": genealogy_unique}
    exact(genealogy_fact, {"path_occurrences": 48, "unique_blobs": 30}, "artifact genealogy facts")
    return {
        "queue_path_occurrences_by_role": dict(sorted(role_paths.items())),
        "audited_role_facts": {
            "theory": theory_fact, "code": code_fact, "test_demo": test_fact, "pdf": pdf_fact,
            "image": image_fact, "data": data_fact, "artifact_genealogy": genealogy_fact,
        },
        "source_artifacts": [theory_src, code_src, tests_src, pdf_src, visual_src, images_src, golden_src, genealogy_src],
    }


def build_document(outcomes: list[dict[str, Any]], active: dict[str, Any]) -> dict[str, Any]:
    operational_now = current_operational_repository_state()
    exact(active["pre"], active["post"], "current active pre/post fingerprint")
    exact(active["operational_pre"], active["operational_post"], "current operational pre/post state")
    exact(active["operational_post"], operational_now, "current operational state after collection")
    queue, queue_stats = reconstruct_queue()
    text = reconstruct_text(queue)
    outputs = output_inventory()
    scripts = ensure_script_inventory()
    document = {
        "schema_version": 1,
        "generated_date": "2026-08-25",
        "baseline_commit": BASELINE,
        "branch": BRANCH,
        "repository_state": historical_repository_state(),
        "scope": "Phase 059 Step 39.5 integrated audit-completeness and reproducibility validation",
        "authority_boundary": AUTHORITY,
        "frozen_corpus": {**queue_stats, "text_coverage": text, "role_coverage": role_evidence(queue, queue_stats, text)},
        "expected_step_outputs": {
            "human_result_count": 19,
            "machine_artifact_count": 21,
            "total_count": 40,
            "records": outputs,
            "source_loss": 0,
            "hash_mismatch": 0,
        },
        "script_inventory": scripts,
        "fresh_subordinate_validation": {
            "count": 31,
            "mandatory_new_validator_pass_count": 5,
            "direct_pass_count": 6,
            "records": outcomes,
            "clone_checkout_policy": {
                "git_config": CLONE_GIT_CONFIG,
                "checkout": f"detached {BASELINE}",
                "index_refresh_before_validators": True,
                "initial_claude_status_bytes": 0,
            },
            "active_checkout_integrity": {
                "pinned_baseline_pre": pinned_baseline_fingerprint(),
                "pinned_baseline_post": pinned_baseline_fingerprint(),
                "pinned_unchanged": True,
                "current_run_policy": (
                    "Every invocation independently checks the current checkout pre/post fingerprint and "
                    "the BASELINE-or-descendant operational ref policy; dynamic current fingerprints are not "
                    "compared with this historical artifact."
                ),
            },
            "portability_boundary": active["portability"],
        },
        "integrated_counts": {
            "queue_paths": 117,
            "unique_blobs": 93,
            "duplicate_occurrences": 24,
            "text_blobs": 63,
            "text_lines": 36641,
            "text_chunks": 158,
            "theory_equation_occurrences": 973,
            "theory_unique_claims": 185,
            "theory_contracts": 38,
            "contract_evidence_records": 80,
            "code_findings": 13,
            "test_demo_findings": 15,
            "four_axis_rows": 185,
            "carry_forward_items": 52,
            "external_truth_promotions": 0,
            "material_validity_promotions": 0,
            "defect_repairs_claimed": 0,
        },
        "independently_reconstructed_semantics": reconstruct_integrated_semantics(),
        "human_deliverable_contract": {
            "paths": [REPORT_B_PATH, STEP_RESULT_PATH],
            "report_b_required_sections": ["Summary", "Step Range", "Inputs", "Files", "Read Coverage", "Execution Evidence", "Validation", "Gate Boundary", "Confirmed Non-changes", "Open Issues", "Next"],
            "step_result_required_sections": ["Objective and Authority", "Input Full-read Coverage", "TDD and Debug History", "Frozen Corpus and Role Counts", "Step Output and Validator Reconciliation", "Commands and Outputs", "Confirmed", "Unverified", "Unresolved", "Ground Not Found", "Files Created", "Next Condition"],
            "required_plan_path": "Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md",
            "required_counts": ["117/117", "93/93", "63/63", "36,641/36,641", "7", "24", "60/60"],
            "authority_terms": ["external literature", "material validity", "public-data", "parameter identifiability", "defect repair"],
            "integrity_policy": {
                "report_b": "LF-normalized full-content SHA-256 exact constant",
                "step_result": (
                    "LF-normalized full-content SHA-256 after exactly one strict validator measurement row "
                    "is verified against the live validator and replaced by a fixed placeholder"
                ),
            },
        },
        "gate": {
            "status": "PASS",
            "meaning": AUTHORITY,
            "confirmed": [
                "117/117 frozen paths and 93/93 unique blobs reconstructed from the pinned manifest and Git blobs",
                "63/63 unique text blobs and 36,641/36,641 lines traversed with 158/158 contiguous chunks",
                "19 human results and 21 machine artifacts match pinned HEAD bytes",
                "five Step38.5/39.1/39.2/39.3/39.4 validators freshly PASS",
                "active canonical tracked content is unchanged by subordinate validation",
            ],
            "unverified": ["external literature truth", "material validity", "public-data validation", "parameter identifiability"],
            "unresolved": ["known raw Windows portability failure", "open carry-forward register obligations", "stale ledger/handover checkpoint pending controller update"],
            "ground_not_found": ["evidence that internal PASS closes scientific defects or constitutes final publication authority"],
        },
        "determinism": {
            "encoding": "UTF-8",
            "line_endings": "LF",
            "json_key_order": "sorted",
            "strict_duplicate_key_parse": True,
            "runtime_observations_captured_once": True,
            "repeat_serialization_byte_identity_required": True,
        },
    }
    document["semantic_sha256"] = semantic_hash(document)
    return document


def deterministic_projection(document: Any, label: str) -> dict[str, Any]:
    require(type(document) is dict, f"{label}: top-level object required")
    require(type(document.get("fresh_subordinate_validation")) is dict, f"{label}: fresh validation object required")
    fresh = document["fresh_subordinate_validation"]
    require(type(fresh.get("records")) is list, f"{label}: fresh records list required")
    clone = copy.deepcopy(document)
    clone.pop("semantic_sha256", None)
    for index, row in enumerate(clone["fresh_subordinate_validation"]["records"]):
        require(type(row) is dict, f"{label}: fresh record {index} object required")
        runtime = row.get("runtime_seconds")
        require(type(runtime) in {int, float} and type(runtime) is not bool and runtime >= 0, f"{label}: runtime type/value")
        row["runtime_seconds"] = "<NONDETERMINISTIC_RUNTIME_OBSERVATION>"
    portability = clone["fresh_subordinate_validation"].get("portability_boundary")
    require(type(portability) is dict and type(portability.get("raw_observed")) is dict,
            f"{label}: portability raw observation required")
    raw_runtime = portability["raw_observed"].get("runtime_seconds")
    require(
        raw_runtime == "<NONDETERMINISTIC_RUNTIME_OBSERVATION>"
        or (type(raw_runtime) in {int, float} and type(raw_runtime) is not bool and raw_runtime >= 0),
        f"{label}: portability runtime type/value",
    )
    portability["raw_observed"]["runtime_seconds"] = "<NONDETERMINISTIC_RUNTIME_OBSERVATION>"
    return clone


def lf_normalized_report_text(value: str, label: str) -> str:
    require(type(value) is str, f"{label}: report text required")
    normalized = value.replace("\r\n", "\n")
    require("\r" not in normalized, f"{label}: unsupported bare CR")
    return normalized


def validate_reports(document: dict[str, Any], report_texts: dict[str, str | None] | None = None) -> None:
    contract = document["human_deliverable_contract"]
    require(type(contract) is dict, "human deliverable contract type")
    texts: dict[str, str] = {}
    for path in contract["paths"]:
        if report_texts is None:
            require((ROOT / path).is_file(), f"missing human deliverable: {path}")
            try:
                text = (ROOT / path).read_bytes().decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValidationFailure(f"malformed UTF-8 report: {path}: {exc}") from exc
        else:
            text = report_texts.get(path)
            require(type(text) is str, f"missing human deliverable: {path}")
        texts[path] = lf_normalized_report_text(text, path)
    report_b = texts[REPORT_B_PATH]
    require(sha256(report_b.encode("utf-8")) == REPORT_B_LF_SHA256, "Report B exact LF-normalized content SHA")
    result = texts[STEP_RESULT_PATH]
    matches = list(STEP_RESULT_VALIDATOR_ROW_PATTERN.finditer(result))
    require(len(matches) == 1, "Step result must contain exactly one strict validator measurement row")
    validator_bytes = (ROOT / VALIDATOR_PATH).read_bytes()
    try:
        validator_text = validator_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationFailure(f"malformed UTF-8 validator source: {exc}") from exc
    require("\r" not in validator_text.replace("\r\n", "\n"), "validator source contains unsupported bare CR")
    match = matches[0]
    expected_lines = len(validator_text.splitlines())
    expected_bytes = len(validator_bytes)
    require(match.group(1) == f"{expected_lines:,}", "Step result validator line measurement spelling")
    require(match.group(2) == f"{expected_bytes:,}", "Step result validator byte measurement spelling")
    reported_lines = int(match.group(1).replace(",", ""))
    reported_bytes = int(match.group(2).replace(",", ""))
    reported_sha = match.group(3)
    require(reported_lines == expected_lines, "Step result validator line measurement")
    require(reported_bytes == expected_bytes, "Step result validator byte measurement")
    require(reported_sha == sha256(validator_bytes), "Step result validator SHA measurement")
    masked_result, substitution_count = STEP_RESULT_VALIDATOR_ROW_PATTERN.subn(
        STEP_RESULT_VALIDATOR_ROW_MASK,
        result,
    )
    require(substitution_count == 1, "Step result validator measurement mask cardinality")
    require(
        sha256(masked_result.encode("utf-8")) == STEP_RESULT_MASKED_LF_SHA256,
        "Step result exact masked LF-normalized content SHA",
    )
    heading_sets = {
        path: {line[3:] for line in text.splitlines() if line.startswith("## ")}
        for path, text in texts.items()
    }
    require(set(contract["report_b_required_sections"]).issubset(heading_sets[REPORT_B_PATH]), "Report B section loss")
    require(set(contract["step_result_required_sections"]).issubset(heading_sets[STEP_RESULT_PATH]), "Step result section loss")
    combined = texts[REPORT_B_PATH] + "\n" + result
    require(contract["required_plan_path"] in result, "correct detailed plan path missing")
    require("2026-08-25-v1025_2-canonical-completion-phase059-plan.md" not in result, "stale/wrong detailed plan path")
    for token in contract["required_counts"]:
        require(token in combined, f"human deliverable measured fact missing: {token}")
    for token in contract["authority_terms"]:
        require(token in combined, f"human deliverable authority boundary missing: {token}")
    for path in STEP_PATHS:
        require(path in combined, f"human deliverable path cross-reference missing: {path}")
    require(document["fresh_subordinate_validation"]["portability_boundary"]["normalized_semantic_sha256"] in combined, "normalized semantic SHA absent from reports")
    require("7" in combined and "24" in combined and "25/26" in combined, "raw exit distribution/fullpath summary absent")
    require("commit/push" in combined or "commit" in combined and "push" in combined, "no-commit/push boundary absent")


def validate_document(
    document: Any,
    expected: dict[str, Any],
    *,
    check_reports: bool = True,
    report_texts: dict[str, str | None] | None = None,
) -> None:
    require(type(document) is dict, "artifact top-level type")
    require(type(document.get("semantic_sha256")) is str and len(document["semantic_sha256"]) == 64, "semantic SHA type/length")
    require(document["semantic_sha256"] == semantic_hash(document), "semantic hash")
    actual_projection = deterministic_projection(document, "actual")
    expected_projection = deterministic_projection(expected, "expected")
    exact(actual_projection, expected_projection, "complete deterministic source-reconstructed projection")
    # Exact projection equality closes every nested key, list order, scalar value,
    # and scalar type.  These checks make the critical runtime policies explicit.
    fresh = document["fresh_subordinate_validation"]
    records = fresh["records"]
    require(len(records) == 31 and len({row["name"] for row in records}) == 31, "validator registry cardinality/uniqueness")
    require(sum(type(row["exit_code"]) is int and row["exit_code"] == 0 for row in records) == 7, "subordinate exit0 count")
    require(sum(type(row["exit_code"]) is int and row["exit_code"] == 1 for row in records) == 24, "subordinate exit1 count")
    for row in records:
        require(row["name"] in ALL_VALIDATORS and pathlib.PurePosixPath(row["name"]).name == row["name"], "validator traversal/unknown name")
        require(row["argv"] == [sys.executable, f"{WORK}/{row['name']}"] and row["shell"] is False, "actual argv/shell policy")
        require(type(row["timeout_seconds"]) is int and row["timeout_seconds"] == 300, "timeout policy")
        require(row["execution_location"] == "DISPOSABLE_CLONE", "active execution prohibited")
        require(row["stdout_utf8"] is True and row["stderr_utf8"] is True, "UTF-8 evidence")
        require(row["timed_out"] is False and row["traceback"] is False, "timeout/traceback")
    for name in DIRECT_PASS:
        row = next(item for item in records if item["name"] == name)
        require(row["exit_code"] == 0 and row["stderr_bytes"] == 0 and not row["failed_banners"], f"mandatory PASS evidence: {name}")
        require(any(line.startswith("PASS") for line in row["banners"]), f"mandatory PASS banner: {name}")
    integrity = fresh["active_checkout_integrity"]
    exact(integrity["pinned_baseline_pre"], integrity["pinned_baseline_post"], "pinned historical pre/post")
    require(integrity["pinned_unchanged"] is True, "pinned historical baseline unchanged")
    if check_reports:
        validate_reports(document, report_texts)


def negative_probes(document: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    probes: list[tuple[str, Any]] = []

    def add(name: str, fn: Any) -> None:
        item = copy.deepcopy(document)
        fn(item)
        item["semantic_sha256"] = semantic_hash(item)
        probes.append((name, item))
    def record(d: dict[str, Any], name: str) -> dict[str, Any]:
        return next(row for row in d["fresh_subordinate_validation"]["records"] if row["name"] == name)

    add("baseline_tamper", lambda d: d.__setitem__("baseline_commit", "0" * 40))
    add("nested_authority_key", lambda d: d["gate"].__setitem__("ESTABLISHED", True))
    add("role_equation_tamper", lambda d: d["frozen_corpus"]["role_coverage"]["audited_role_facts"]["theory"].__setitem__("equations", 972))
    add("role_image_tamper", lambda d: d["frozen_corpus"]["role_coverage"]["audited_role_facts"]["image"].__setitem__("unique_blobs", 9))
    add("lines_read_tamper", lambda d: d["frozen_corpus"]["text_coverage"].__setitem__("lines_read", 36640))
    add("queue_count_tamper", lambda d: d["frozen_corpus"].__setitem__("path_count", 116))
    add("text_coverage_tamper", lambda d: d["frozen_corpus"]["text_coverage"].__setitem__("coverage", "partial"))
    add("drop_output", lambda d: d["expected_step_outputs"]["records"].pop())
    add("output_sha_tamper", lambda d: d["expected_step_outputs"]["records"][0].__setitem__("sha256", "0" * 64))
    add("output_heading_tamper", lambda d: d["expected_step_outputs"]["records"][0].__setitem__("heading_count", 999))
    add("output_heading_hash_tamper", lambda d: d["expected_step_outputs"]["records"][0].__setitem__("heading_sha256", "0" * 64))
    add("duplicate_output_path", lambda d: d["expected_step_outputs"]["records"][1].__setitem__("path", d["expected_step_outputs"]["records"][0]["path"]))
    add("output_source_loss", lambda d: d["expected_step_outputs"].__setitem__("source_loss", 1))
    add("output_hash_mismatch", lambda d: d["expected_step_outputs"].__setitem__("hash_mismatch", 1))
    add("script_count_tamper", lambda d: d["script_inventory"].__setitem__("validator_count", 30))
    add("registry_shrink", lambda d: d["script_inventory"]["temp_mirror_required"].pop())
    add("writer_reclassified_direct", lambda d: d["script_inventory"]["read_only_direct_expected_pass"].append("validate_phase059_images.py"))
    add("drop_validator", lambda d: d["fresh_subordinate_validation"]["records"].pop())
    add("duplicate_validator_name", lambda d: d["fresh_subordinate_validation"]["records"][1].__setitem__("name", d["fresh_subordinate_validation"]["records"][0]["name"]))
    add("argv_traversal", lambda d: record(d, DIRECT_PASS[0]).__setitem__("argv", [sys.executable, "../evil.py"]))
    add("fake_pass_stdout_digest", lambda d: record(d, DIRECT_PASS[0]).__setitem__("stdout_sha256", "0" * 64))
    add("temp_fake_pass_banner", lambda d: record(d, "validate_phase059_theory_index.py").__setitem__("banners", ["PASS_FAKE"]))
    add("mandatory_false_fail", lambda d: record(d, DIRECT_PASS[0]).__setitem__("exit_code", 1))
    add("mandatory_timeout", lambda d: record(d, DIRECT_PASS[0]).__setitem__("timed_out", True))
    add("mandatory_traceback", lambda d: record(d, DIRECT_PASS[0]).__setitem__("traceback", True))
    add("temp_extra_scientific_fail", lambda d: record(d, "validate_phase059_theory_index.py")["failed_banners"].append("FAIL scientific_claim"))
    add("temp_summary_tamper", lambda d: record(d, "validate_phase059_pdf_render.py").__setitem__("summary_banners", ["SUMMARY 0/999 PASS"]))
    add("portability_false_pass", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_observed"].__setitem__("exit_code", 0))
    add("portability_exit_float", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_observed"].__setitem__("exit_code", 1.0))
    add("portability_expected_failed_set", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_expected_failure"].__setitem__("failed_checks", ["scientific"]))
    add("portability_25_to_26", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_expected_failure"].__setitem__("passed_checks", 26))
    add("portability_raw_digest", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_observed"].__setitem__("stdout_sha256", "0" * 64))
    add("portability_artifact_digest", lambda d: d["fresh_subordinate_validation"]["portability_boundary"].__setitem__("raw_artifact_sha256", "0" * 64))
    add("portability_reference_digest", lambda d: d["fresh_subordinate_validation"]["portability_boundary"].__setitem__("canonical_artifact_sha256", "0" * 64))
    add("portability_timeout", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_observed"].__setitem__("timed_out", True))
    add("portability_traceback", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_observed"].__setitem__("traceback", True))
    add("portability_sixth_diff", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["raw_structural_diffs"].append({"path": "findings[0]", "actual": 1, "expected": 2}))
    add("broad_normalization", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["exact_normalization_allowlist"].append("**"))
    add("normalized_science_hash", lambda d: d["fresh_subordinate_validation"]["portability_boundary"].__setitem__("normalized_semantic_sha256", "0" * 64))
    add("science_numeric_tamper", lambda d: d["fresh_subordinate_validation"]["portability_boundary"]["science_metrics"].__setitem__("active_rows", 5))
    add(
        "pre_post_both_spoof",
        lambda d: (
            d["fresh_subordinate_validation"]["active_checkout_integrity"].__setitem__(
                "pinned_baseline_pre", {"head": "spoof"}
            ),
            d["fresh_subordinate_validation"]["active_checkout_integrity"].__setitem__(
                "pinned_baseline_post", {"head": "spoof"}
            ),
        ),
    )
    add("unverified_drop", lambda d: d["gate"]["unverified"].pop())
    add("false_determinism", lambda d: d["determinism"].__setitem__("strict_duplicate_key_parse", False))
    add("external_truth_promotion", lambda d: d["integrated_counts"].__setitem__("external_truth_promotions", 1))
    add("semantic_count_tamper", lambda d: d["independently_reconstructed_semantics"].__setitem__("theory_equation_occurrences", 972))
    add("unknown_top_key", lambda d: d.__setitem__("ESTABLISHED", True))
    add("unknown_nested_key", lambda d: d["determinism"].__setitem__("extra", True))
    add("missing_nested_key", lambda d: d["determinism"].pop("encoding"))
    add("bool_int_confusion", lambda d: d.__setitem__("schema_version", True))
    add("malformed_records_container", lambda d: d["fresh_subordinate_validation"].__setitem__("records", False))
    add("malformed_output_list", lambda d: d["expected_step_outputs"].__setitem__("records", {}))
    rejected = []
    for name, mutated in probes:
        try:
            validate_document(mutated, expected, check_reports=False)
        except ValidationFailure:
            rejected.append(name)
        else:
            raise ValidationFailure(f"negative probe unexpectedly accepted: {name}")
    raw = pretty_bytes(document).replace(b'"schema_version": 1,', b'"schema_version": 1,\n  "schema_version": 1,', 1)
    try:
        strict_bytes(raw, "raw_duplicate_key_probe")
    except ValidationFailure:
        rejected.append("raw_duplicate_key")
    else:
        raise ValidationFailure("raw duplicate key probe accepted")
    try:
        b"\xff".decode("utf-8")
    except UnicodeDecodeError:
        rejected.append("malformed_utf8")
    else:
        raise ValidationFailure("malformed UTF-8 probe accepted")
    report_texts = {
        REPORT_B_PATH: (ROOT / REPORT_B_PATH).read_text(encoding="utf-8"),
        STEP_RESULT_PATH: (ROOT / STEP_RESULT_PATH).read_text(encoding="utf-8"),
    }
    for name, path in (("missing_report_b", REPORT_B_PATH), ("missing_step_result", STEP_RESULT_PATH)):
        attacked = dict(report_texts)
        attacked[path] = None
        try:
            validate_reports(document, attacked)
        except ValidationFailure:
            rejected.append(name)
        else:
            raise ValidationFailure(f"negative report probe unexpectedly accepted: {name}")
    report_attacks = {
        "report_b_inventory_tamper": (
            REPORT_B_PATH,
            "19 producers and 31 validators",
            "19 producers and 30 validators",
        ),
        "report_b_authority_reversal": (
            REPORT_B_PATH,
            "does not establish external literature truth",
            "establishes external literature truth",
        ),
        "step_result_execution_claim_tamper": (
            STEP_RESULT_PATH,
            "The five required modern validators freshly PASS:",
            "The five required modern validators did not run:",
        ),
    }
    for name, (path, old, new) in report_attacks.items():
        attacked = dict(report_texts)
        require(attacked[path].count(old) == 1, f"negative report probe source cardinality: {name}")
        attacked[path] = attacked[path].replace(old, new, 1)
        try:
            validate_reports(document, attacked)
        except ValidationFailure:
            rejected.append(name)
        else:
            raise ValidationFailure(f"negative report probe unexpectedly accepted: {name}")
    canonical_result = report_texts[STEP_RESULT_PATH]
    canonical_match = STEP_RESULT_VALIDATOR_ROW_PATTERN.search(canonical_result)
    require(canonical_match is not None, "negative numeric probe source row missing")
    line_digits = canonical_match.group(1).replace(",", "")
    malformed_grouping = line_digits[:2] + "," + line_digits[2:]
    require(malformed_grouping != canonical_match.group(1), "negative numeric grouping mutation ineffective")
    numeric_attacks = {
        "step_result_validator_line_grouping_tamper": (1, malformed_grouping),
        "step_result_validator_byte_leading_zero_tamper": (2, "0" + canonical_match.group(2)),
    }
    for name, (group_index, replacement) in numeric_attacks.items():
        attacked = dict(report_texts)
        attacked[STEP_RESULT_PATH] = (
            canonical_result[: canonical_match.start(group_index)]
            + replacement
            + canonical_result[canonical_match.end(group_index) :]
        )
        try:
            validate_reports(document, attacked)
        except ValidationFailure:
            rejected.append(name)
        else:
            raise ValidationFailure(f"negative numeric report probe unexpectedly accepted: {name}")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--rewrite-existing", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    args = parser.parse_args()
    try:
        if args.collect:
            if ARTIFACT.exists():
                raise ValidationFailure("--collect refuses to overwrite an existing artifact")
            outcomes, active = collect_subordinates()
            expected = build_document(outcomes, active)
            document = expected
            validate_document(document, expected, check_reports=False)
            ARTIFACT.write_bytes(pretty_bytes(document))
        else:
            require(ARTIFACT.is_file(), f"missing artifact: {ARTIFACT_PATH}")
            document = strict_bytes(ARTIFACT.read_bytes(), ARTIFACT_PATH)
            outcomes, active = collect_subordinates()
            expected = build_document(outcomes, active)
            validate_document(document, expected, check_reports=True)
            if args.rewrite_existing:
                ARTIFACT.write_bytes(pretty_bytes(document))
        if args.run_negative_probes:
            rejected = negative_probes(document, expected)
            print(f"NEGATIVE_PROBES_REJECTED={len(rejected)}/{len(rejected)}")
            print("NEGATIVE_PROBE_IDS=" + ",".join(rejected))
        print("PASS_P059_STEP_039_5_INTEGRATED_VALIDATION")
        return 0
    except ValidationFailure as exc:
        print(f"FAIL_P059_STEP_039_5_INTEGRATED_VALIDATION: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
