#!/usr/bin/env python3
"""Build and validate the Phase 061 Step 51.2 integrated lineage gate.

Subordinate validators run from disposable clones that reconstruct each Step's
historical pre-commit state. The gate establishes lineage-audit coverage and
lossless routing only; it deliberately does not promote external scientific or
material truth.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable


ROOT = pathlib.Path(__file__).resolve().parents[3]
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
STEP51_BASELINE = "fe3433e63ccb6255a75a51dda3fd6a4eb747c0a7"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
FINAL_SUBJECT = "audit(phase061): close v1020 lineage gate"

VALIDATOR_PATH = "Codex/work/v1020_phase061/validate_phase061_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_061_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_061_V1020_LINEAGE_REPORT_D.md"
GATE_RESULT_PATH = "Codex/results/PHASE_061_STEP_051_2_GATE_RESULT.md"
PHASE_RESULT_PATH = "Codex/results/PHASE_061_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
ARTIFACT = ROOT / ARTIFACT_PATH

FINAL_PATHS = [
    VALIDATOR_PATH,
    ARTIFACT_PATH,
    REPORT_PATH,
    GATE_RESULT_PATH,
    PHASE_RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_PATH_SET = set(FINAL_PATHS)

MACHINE_ARTIFACTS = {
    "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json": "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c",
    "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json": "7fcb7fb4603360976cf205ba09414f27345d0b33479750bbaf9eff8f70815cc7",
    "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json": "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403",
    "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json": "25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914",
    "Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json": "629995ab5936587840e5944c513ef86a0e82f114dd1d94860b06754fb9fdd414",
    "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json": "73004354e80635d3feb0543670c45eceee62086a1e1b6c67ff8b6e1293810ce9",
    "Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json": "22b3b0cdb06b376a97076c30c73eecc1148dbd6dca5b49f60c09a85c4cd26d7b",
    "Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json": "e204190857a60727f4d24855b03ec75683e7fdf7ed0addedaa7096dbb0309089",
    "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json": "c011ad481a325437a7d6e8b6ae37416417eb031932b1490cd9c6e8c5b39ac01e",
    "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json": "b8ed909937be07938b30ae3344d9ff60ca87a476a8c422e32d8751123bdb100e",
}

RESULT_ARTIFACTS = {
    "Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md": "c26dda8533c2fd9abbe625c4025a0a7d98815d4e15890a484799395730eaea48",
    "Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md": "4035e6c3302a856e19fb379cb8a52cb416bbe3ce001b5d499befce935adaaeb0",
    "Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md": "c899437ece2851a2ebc5c68c1f39d4174ef07a73b453d5b7d03b7021b7c9fd9e",
    "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md": "a8dab6f35b886230478d299bc3466bac22217c123a39cb2b53261a71bb066d50",
    "Codex/results/PHASE_061_STEP_050_REVIEW_ARTIFACT_RESULT.md": "385b672150044e990e53af3410b78f25e56177367d5ab65a9b3ef4847d411e58",
    "Codex/results/PHASE_061_STEP_051_1_DISPOSITION_RESULT.md": "10c328a7d15c4a3b97f774652dd32b24f9361ca4242ad01b17205bf39de632b3",
}

WORK = "Codex/work/v1020_phase061"
SUBORDINATES = [
    {"unit": "STEP_46", "commit": "4c951f390c63f11f1c5a03cc47c7e3bce32926de", "path": f"{WORK}/validate_phase061_step46.py", "sha256": "680995a23fd5365650ae245d508ff9751f821f7600fc8531903a9a9dfd377a72", "args": ["--content-only", "--run-negative-probes", "--determinism-check"], "terminal_prefix": "PASS_P061_STEP46_SOURCE_TOPOLOGY", "required": ["PASS_P061_STEP46_NEGATIVE_CONTROLS 48/48", "PASS_P061_STEP46_DETERMINISM 2/2"]},
    {"unit": "STEP_47", "commit": "46f17a9863b5a2ce0708524b09601930000e233f", "path": f"{WORK}/validate_phase061_step47.py", "sha256": "973b00b3d6a4ef321c4c55aa1b5c3ee7ba64bdf6de2be3fb773a6896e9a1ae56", "args": ["--content-only", "--run-negative-probes", "--determinism-check"], "terminal_prefix": "PASS_P061_STEP47_PROCESS_AUTHORITY", "required": ["PASS_P061_STEP47_NEGATIVE_CONTROLS 78/78", "PASS_P061_STEP47_BOUNDARY_NEGATIVE_CONTROLS 17/17", "PASS_P061_STEP47_DETERMINISM 2/2 production_imported=false"]},
    {"unit": "STEP_48", "commit": "5cf75ba2fd4e5707c53b164d361f1526c3d31f06", "path": f"{WORK}/validate_phase061_step48.py", "sha256": "3989946ac3aea915af45216469c0c9ccb096f40ac04ba0d6ed3fa95fc0a8c411", "args": ["--content-only", "--run-negative-probes", "--run-boundary-probes", "--determinism-check"], "terminal_prefix": "PASS_P061_STEP48_LINEAGE_DIFF", "required": ["PASS_P061_STEP48_NEGATIVE_CONTROLS 66/66", "PASS_P061_STEP48_STRICT_NEGATIVE_CONTROLS 2/2", "PASS_P061_STEP48_BOUNDARY_CONTROLS 29/29", "PASS_P061_STEP48_DETERMINISM 2/2"]},
    {"unit": "STEP_49", "commit": "b52435504b527d911b51470268e3879824bd6362", "path": f"{WORK}/validate_phase061_step49.py", "sha256": "a186cdf256b697ec06fc6784d9b1bc17c9a8afbd7bb6fe150ccda9171adb8acb", "args": ["--verify-staged"], "terminal_prefix": "PASS_WITH_CONCERNS_P061_STEP49_CITATION_AUTHORITY", "required": ["PASS_P061_STEP49_CONTROLS 36/36", "PASS_P061_STEP49_STRICT_JSON 2/2", "PASS_P061_STEP49_DETERMINISM 2/2", "PASS_P061_STEP49_STAGED matrix_nodes=51653 depth=6"]},
    {"unit": "STEP_50", "commit": "a90c6e8659f4fcd24945af81e50c712bbc71ef30", "path": f"{WORK}/validate_phase061_step50.py", "sha256": "9f130147b505a74f600e6cb049e520d57592d46df63ac9fd90db2c2725e26ebe", "args": ["--content-only", "--run-negative-probes", "--determinism-check"], "terminal_prefix": "PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS", "required": ["PASS_P061_STEP50_NEGATIVE_CONTROLS 16/16", "PASS_P061_STEP50_DETERMINISM 2/2"]},
    {"unit": "STEP_51_1", "commit": STEP51_BASELINE, "path": f"{WORK}/validate_phase061_step51_dispositions.py", "sha256": "b6ac6689ea4fe76db515f6a235994b08c447fa38733dee67872d2f9eea17f33a", "args": ["--mode", "artifact"], "terminal_prefix": "PASS_P061_STEP51_1_DISPOSITIONS", "required": ["PASS negative_controls=55/55", "PASS determinism=2/2 production_imported_or_executed=false"]},
]

STEP_UNITS = [
    ("PLAN_ACTIVATION", "0c18bb48401675bd5154649baa2d6a151d272d9c", "docs(phase061): plan v1020 lineage reaudit", ["Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md", HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_PLAN_ACTIVATION_RESULT.md", "Codex/results/PHASE_061_PLAN_ACTIVATION_VALIDATION.json", f"{WORK}/validate_phase061_plan.py"]),
    ("STEP_46", "4c951f390c63f11f1c5a03cc47c7e3bce32926de", "audit(phase061): freeze v1020 source topology", [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md", "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json", "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json", f"{WORK}/build_phase061_step46_source_topology.py", f"{WORK}/validate_phase061_step46.py"]),
    ("STEP_47", "46f17a9863b5a2ce0708524b09601930000e233f", "audit(phase061): adjudicate v1020 process authority", [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md", "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json", f"{WORK}/build_phase061_step47_process_authority.py", f"{WORK}/validate_phase061_step47.py"]),
    ("STEP_48", "5cf75ba2fd4e5707c53b164d361f1526c3d31f06", "audit(phase061): trace v1019-v1020 lineage delta", [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md", "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json", "Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json", f"{WORK}/build_phase061_step48_lineage_diff.py", f"{WORK}/validate_phase061_step48.py"]),
    ("STEP_49", "b52435504b527d911b51470268e3879824bd6362", "audit(phase061): bound v1020 citation authority", [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md", "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json", f"{WORK}/build_phase061_step49_citation_authority.py", f"{WORK}/validate_phase061_step49.py"]),
    ("STEP_50", "a90c6e8659f4fcd24945af81e50c712bbc71ef30", "audit(phase061): adjudicate v1020 review artifacts", [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_STEP_050_REVIEW_ARTIFACT_RESULT.md", "Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json", "Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json", f"{WORK}/audit_phase061_step50_review_artifacts.py", f"{WORK}/validate_phase061_step50.py"]),
    ("STEP_51_1", STEP51_BASELINE, "audit(phase061): disposition v1020 lineage", [HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, "Codex/results/PHASE_061_STEP_051_1_DISPOSITION_RESULT.md", "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json", "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json", f"{WORK}/build_phase061_step51_dispositions.py", f"{WORK}/validate_phase061_step51_dispositions.py"]),
]

AUTHORITY_BOUNDARY = (
    "PASS_P061_LINEAGE_D establishes complete frozen v1.0.20 lineage-audit coverage, "
    "internal authority separation, reproducible genealogy, and lossless disposition/debt "
    "routing only. It does not establish external scientific, material, experimental, or "
    "primary-literature truth; canonical model selection; defect repair; parameter "
    "identifiability; final LaTeX/PDF; or publication readiness."
)

class ValidationFailure(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ValidationFailure(code, message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def exact(actual: Any, expected: Any, code: str, label: str) -> None:
    require(canonical_bytes(actual) == canonical_bytes(expected), code, label)


def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, "E_DUPLICATE_JSON", key)
        output[key] = value
    return output


def reject_constant(value: str) -> None:
    raise ValidationFailure("E_NONFINITE_JSON", value)


def parse_finite_float(value: str) -> float:
    parsed = float(value)
    require(math.isfinite(parsed), "E_NONFINITE_JSON", value)
    return parsed


def strict_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_hook, parse_constant=reject_constant, parse_float=parse_finite_float)
    except ValidationFailure:
        raise
    except Exception as error:
        raise ValidationFailure("E_STRICT_JSON", f"{label}: {error}") from error


def traversal_stats(value: Any) -> dict[str, int]:
    value_nodes = 0
    key_nodes = 0
    maximum_depth = 0

    def walk(node: Any, depth: int) -> None:
        nonlocal value_nodes, key_nodes, maximum_depth
        value_nodes += 1
        maximum_depth = max(maximum_depth, depth)
        if isinstance(node, dict):
            key_nodes += len(node)
            for child in node.values():
                walk(child, depth + 1)
        elif isinstance(node, list):
            for child in node:
                walk(child, depth + 1)

    walk(value, 0)
    return {"value_nodes": value_nodes, "key_nodes": key_nodes, "total_nodes": value_nodes + key_nodes, "max_depth": maximum_depth}


def semantic_hash(document: dict[str, Any]) -> str:
    clone = copy.deepcopy(document)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def git(args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    try:
        process = subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, env=env, timeout=120)
    except subprocess.TimeoutExpired as error:
        raise ValidationFailure("E_GIT_TIMEOUT", str(args)) from error
    if check and process.returncode:
        raise ValidationFailure("E_GIT_COMMAND", f"{args}: {process.stderr.decode('utf-8', errors='replace').strip()}")
    return process


def git_text(*args: str, cwd: pathlib.Path = ROOT) -> str:
    return git(list(args), cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(path: str) -> bytes:
    require("\\" not in path and not path.startswith("/"), "E_GIT_PATH", path)
    return git(["show", f"{STEP51_BASELINE}:{path}"]).stdout


def nul_paths(raw: bytes) -> set[str]:
    return {item.decode("utf-8").replace("\\", "/") for item in raw.split(b"\0") if item}


def active_status_paths(cwd: pathlib.Path = ROOT) -> set[str]:
    records = [item for item in git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=cwd).stdout.split(b"\0") if item]
    paths: set[str] = set()
    index = 0
    while index < len(records):
        record = records[index]
        require(len(record) >= 4, "E_STATUS_PARSE", repr(record))
        status = record[:2].decode("ascii")
        paths.add(record[3:].decode("utf-8").replace("\\", "/"))
        index += 1
        if "R" in status or "C" in status:
            require(index < len(records), "E_STATUS_PARSE", "rename/copy")
            paths.add(records[index].decode("utf-8").replace("\\", "/"))
            index += 1
    return paths


def live_remote_head(branch: str) -> str:
    rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").splitlines()
    require(len(rows) == 1, "E_REMOTE_CARDINALITY", branch)
    return rows[0].split()[0]


def validate_protected_tips(protected: str, main: str) -> None:
    require(protected == PROTECTED_TIP, "E_PROTECTED_DRIFT", protected)
    require(main == MAIN_TIP, "E_MAIN_DRIFT", main)


def repository_state() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    origin_active = git_text("rev-parse", f"origin/{BRANCH}")
    live_active = live_remote_head(BRANCH)
    protected = git_text("rev-parse", f"origin/{PROTECTED_BRANCH}")
    main = git_text("rev-parse", "origin/main")
    validate_protected_tips(protected, main)
    require(live_remote_head(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_REMOTE_DRIFT", PROTECTED_BRANCH)
    require(live_remote_head("main") == MAIN_TIP, "E_MAIN_REMOTE_DRIFT", "main")
    require(branch == BRANCH, "E_ACTIVE_BRANCH", branch)
    require(head == upstream == origin_active == live_active, "E_ACTIVE_REMOTE", f"{head}/{upstream}/{origin_active}/{live_active}")
    require(git(["merge-base", "--is-ancestor", STEP51_BASELINE, head], check=False).returncode == 0, "E_BASELINE_ANCESTRY", head)
    unexpected = sorted(active_status_paths() - FINAL_PATH_SET)
    require(not unexpected, "E_UNEXPECTED_DIRT", str(unexpected))
    claude_tracked = git_text("diff", "--name-only", STEP51_BASELINE, "--", "Claude").splitlines()
    claude_untracked = git_text("ls-files", "--others", "--exclude-standard", "--", "Claude").splitlines()
    require(not claude_tracked and not claude_untracked, "E_CLAUDE_DRIFT", str(claude_tracked + claude_untracked))
    return {"branch": branch, "head": head, "upstream": upstream, "origin_active": origin_active, "live_remote": live_active, "step51_baseline": STEP51_BASELINE, "step51_baseline_is_ancestor": True, "protected": protected, "live_protected": PROTECTED_TIP, "main": main, "live_main": MAIN_TIP, "precommit_allowlist": FINAL_PATHS, "only_allowlisted_status_paths": True, "unexpected_status_paths": [], "claude_tracked_diff_count": 0, "claude_untracked_count": 0}


def inventory_artifacts(paths: dict[str, str], machine: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    objects: dict[str, Any] = {}
    records: list[dict[str, Any]] = []
    for path, expected_sha in paths.items():
        raw = git_blob(path)
        require(sha256(raw) == expected_sha, "E_INPUT_SHA", path)
        require((ROOT / path).read_bytes() == raw, "E_INPUT_WORKTREE", path)
        record = {"path": path, "sha256": expected_sha, "bytes": len(raw), "physical_lines": len(raw.decode("utf-8").splitlines())}
        if machine:
            obj = strict_bytes(raw, path)
            require(type(obj) is dict, "E_MACHINE_TOP_TYPE", path)
            record.update(traversal_stats(obj))
            record["top_level_keys"] = sorted(obj)
            objects[path] = obj
        records.append(record)
    return objects, records


def input_inventory() -> tuple[dict[str, Any], dict[str, Any]]:
    objects, machine_records = inventory_artifacts(MACHINE_ARTIFACTS, True)
    _, result_records = inventory_artifacts(RESULT_ARTIFACTS, False)
    require(len(machine_records) == 10 and len(result_records) == 6, "E_INPUT_COUNT", "10+6")
    return objects, {"machine_count": 10, "machine_records": machine_records, "result_count": 6, "result_records": result_records, "strict_duplicate_keys": True, "nonfinite_rejected": True, "full_recursive_traversal": True}


def integrated_counts(objects: dict[str, Any]) -> dict[str, Any]:
    topology = objects["Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"]
    reads = objects["Codex/results/PHASE_061_V1020_READ_ATTESTATION.json"]
    process = objects["Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json"]
    lineage = objects["Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json"]
    snapshot = objects["Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json"]
    citation = objects["Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json"]
    review = objects["Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json"]
    visual = objects["Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json"]
    disposition = objects["Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json"]
    carry = objects["Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json"]

    source_expected = {"paths": 232, "unique_blobs": 231, "text_files": 195, "text_physical_lines": 31553, "text_nonblank_lines": 29335, "pdf_files": 14, "pdf_pages": 130, "image_occurrences": 23, "same_relative_pairs": 47, "same_relative_identical": 18, "same_relative_changed": 29, "v1019_identical_overlap": 18, "v1019_new_blob_or_source": 214}
    exact({key: topology["counts"][key] for key in source_expected}, source_expected, "E_SOURCE_COUNTS", "topology")
    exact(reads["counts"], {"human_partitions_complete": 3, "human_partitions_total": 3, "image_occurrences": 23, "pdf_files": 14, "pdf_pages": 130, "text_files": 195, "text_nonblank_lines": 29335, "text_physical_lines": 31553}, "E_READ_COUNTS", "attestation")
    require(len(topology["sources"]) == 232 and len({row["path"] for row in topology["sources"]}) == 232, "E_SOURCE_IDENTITY", "topology paths")
    require(len({row["blob_sha1"] for row in topology["sources"]}) == 231, "E_SOURCE_BLOBS", "unique blobs")
    require(len(reads["text_records"]) == 195 and len(reads["pdf_records"]) == 14 and len(reads["image_records"]) == 23, "E_READ_RECORDS", "195/14/23")

    process_expected = {"source_routes": 232, "claims": 40, "contradictions": 10, "ground_not_found": 7, "unverified_queue": 11, "phase_rows": 9, "snapshot_machine_comparisons": 6}
    exact({key: process["counts"][key] for key in process_expected}, process_expected, "E_PROCESS_COUNTS", "process")
    require(process["counts"]["scientific_promotions_true"] == process["counts"]["external_truth_true"] == 0, "E_PROCESS_PROMOTION", "process")

    lineage_expected = {"delta_rows": 232, "v1020_occurrences": 232, "v1020_unique_blobs": 231, "v1019_occurrences": 66, "paired_occurrences": 54, "deleted_counterparts": 12, "snapshot_occurrences_linked": 10}
    exact({key: lineage["counts"][key] for key in lineage_expected}, lineage_expected, "E_LINEAGE_COUNTS", "lineage")
    exact(lineage["counts"]["comparison_classes"], {"ADDED": 178, "COPIED": 0, "MODIFIED": 29, "RENAMED": 7, "UNCHANGED": 18}, "E_LINEAGE_CLASSES", "lineage")
    exact(snapshot["counts"], {"duplicate_occurrence_groups": 1, "final_appendix_root_occurrences": 1, "p5_p6_changed_tex_paths": 3, "prefinal_occurrences": 8, "snapshot_occurrences": 10, "stage_edges": 9, "unique_snapshot_blobs": 9}, "E_SNAPSHOT_COUNTS", "snapshot")

    citation_expected = {"authority_rows": 782, "new_or_modified_assets_requiring_authority": 347, "new_or_modified_assets_with_authority": 347, "bibliography_entries": 52, "citation_occurrences": 99, "displayed_equations": 175, "source_attribution_statements": 226, "ground_not_found": 2, "genuinely_new_source_identity_debts": 8, "external_scientific_promotions": 0}
    observed_citation = {key: citation["counts"][key] if key in citation["counts"] else len(citation[key]) for key in citation_expected}
    exact(observed_citation, citation_expected, "E_CITATION_COUNTS", "citation")
    require(len(citation["unverified_external_queue"]) == 3, "E_CITATION_UNVERIFIED", "3")

    review_expected = {"topology_sources": 232, "full_read_source_union": 104, "competitive_occurrences": 126, "figure_candidates": 31, "figure_genealogy_routes": 31, "visual_images": 23, "visual_pdfs": 14, "visual_pdf_pages": 130, "external_scientific_promotions": 0, "experimental_evidence_promotions": 0}
    exact({key: review["counts"][key] for key in review_expected}, review_expected, "E_REVIEW_COUNTS", "review")
    require(len(review["review_findings"]) == 14 and len(review["ground_not_found"]) == 11 and len(review["unverified_queue"]) == 7, "E_REVIEW_DEBTS", "14/11/7")
    visual_expected = {"image_occurrences": 23, "original_resolution_inspections": 23, "unique_image_sha256": 23, "pdf_occurrences": 14, "pdf_pages": 130, "page_identity_unique": 130, "render_failures": 0, "numeric_validity_promotions": 0, "experimental_evidence_promotions": 0}
    exact({key: visual["counts"][key] for key in visual_expected}, visual_expected, "E_VISUAL_COUNTS", "visual")

    gate_summary = disposition["gate_summary"]
    exact(gate_summary["disposition_counts"], {"COMPETING_ONLY": 116, "CORRECT": 16, "PRESERVE": 92, "UNVERIFIED": 8}, "E_DISPOSITION_COUNTS", "disposition")
    require(gate_summary["source_expected"] == gate_summary["disposition_rows"] == 232, "E_DISPOSITION_COVERAGE", "232")
    for key in ("source_orphan_count", "duplicate_source_membership_count", "duplicate_disposition_id_count", "competitive_adopted_identity_overlap_count", "external_authority_promotion_count", "missing_acceptance_reason_target_status_count"):
        require(gate_summary[key] == 0, "E_DISPOSITION_INTEGRITY", key)

    carry_summary = carry["gate_summary"]
    require(len(carry["inherited_carry_items"]) == 52 and len(carry["inherited_phase060_blockers"]) == 5 and len(carry["new_blockers"]) == 5, "E_CARRY_COUNTS", "52+5+5")
    require(len(carry["debt_routing"]) == 91, "E_DEBT_COUNT", "91")
    exact(carry_summary["debt_route_state_counts"], {"OPEN": 53, "OPEN_DUPLICATE_ALIAS": 12, "OPEN_REFINEMENT": 19, "RESOLVED_INFORMATIONAL": 7}, "E_DEBT_STATES", "53/12/19/7")
    require(carry_summary["open_debt_count"] == 84 and carry_summary["orphan_open_debt_count"] == 0, "E_DEBT_OPEN", "84/0")
    require(carry_summary["acceptance_satisfied_count"] == 0 and carry_summary["resolution_status_counts"] == {"NOT_RESOLVED": 57}, "E_FALSE_RESOLUTION", "carry")
    require(carry_summary["external_authority_promotion_count"] == 0, "E_CARRY_PROMOTION", "carry")

    return {
        "source": {"paths": 232, "unique_blobs": 231, "text": 195, "physical_lines": 31553, "nonblank_lines": 29335, "pdfs": 14, "pdf_pages": 130, "images": 23},
        "process": {"routes": 232, "claims": 40, "contradictions": 10, "ground_not_found": 7, "unverified": 11, "external_promotions": 0},
        "lineage": {"rows": 232, "classes": {"ADDED": 178, "MODIFIED": 29, "UNCHANGED": 18, "RENAMED": 7, "COPIED": 0}, "paired": 54, "deleted": 12},
        "snapshot": {"occurrences": 10, "unique_blobs": 9, "edges": 9, "duplicate_groups": 1},
        "citation": {"authority_rows": 782, "required": 347, "routed": 347, "bibliography": 52, "equations": 175, "ground_not_found": 2, "unverified": 3, "new_source_debts": 8, "external_promotions": 0},
        "review": {"full_read_union": 104, "competitive": 126, "figures": 31, "images": 23, "pdfs": 14, "pages": 130, "findings": 14, "ground_not_found": 11, "unverified": 7, "external_promotions": 0},
        "dispositions": {"sources": 232, "PRESERVE": 92, "CORRECT": 16, "COMPETING_ONLY": 116, "UNVERIFIED": 8, "orphans": 0},
        "carry": {"inherited": 52, "phase060_blockers": 5, "new_blockers": 5, "canonical_debts": 91, "open_family": 84, "resolved_informational": 7, "resolved_inherited": 0},
    }


def step_commit_inventory(current_tip: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for unit, commit, subject, paths in STEP_UNITS:
        require(git(["merge-base", "--is-ancestor", commit, current_tip], check=False).returncode == 0, "E_STEP_ANCESTRY", unit)
        require(git(["merge-base", "--is-ancestor", commit, f"origin/{BRANCH}"], check=False).returncode == 0, "E_STEP_REMOTE_ANCESTRY", unit)
        require(git_text("show", "-s", "--format=%s", commit) == subject, "E_STEP_SUBJECT", unit)
        changed = git_text("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines()
        require(set(changed) == set(paths) and len(changed) == len(paths) == len(set(changed)), "E_STEP_PATHS", unit)
        records.append({"unit": unit, "commit": commit, "subject": subject, "path_count": len(paths), "paths": sorted(paths), "in_active_ancestry": True, "in_origin_active_ancestry": True, "result_and_machine_evidence_co_committed": True})
    return records


def make_remote_clone(prefix: str) -> tuple[pathlib.Path, pathlib.Path]:
    parent = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    clone = parent / "repo"
    process = subprocess.run(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, timeout=120)
    require(process.returncode == 0, "E_CLONE", process.stderr.decode("utf-8", errors="replace"))
    origin_url = git_text("remote", "get-url", "origin")
    git(["remote", "set-url", "origin", origin_url], cwd=clone)
    git(["fetch", "--force", "origin", f"+refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}", f"+refs/heads/{PROTECTED_BRANCH}:refs/remotes/origin/{PROTECTED_BRANCH}", "+refs/heads/main:refs/remotes/origin/main"], cwd=clone)
    git(["config", "core.autocrlf", "false"], cwd=clone)
    git(["config", "core.eol", "lf"], cwd=clone)
    git(["checkout", "-B", BRANCH, f"origin/{BRANCH}"], cwd=clone)
    git(["branch", "--set-upstream-to", f"origin/{BRANCH}", BRANCH], cwd=clone)
    require(git(["status", "--porcelain=v1", "--untracked-files=all"], cwd=clone).stdout == b"", "E_CLONE_DIRTY", "initial")
    return parent, clone


def remove_temp_tree_strict(path: pathlib.Path) -> None:
    resolved = path.resolve()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    require(resolved.parent == temp_root, "E_TEMP_BOUNDARY", str(resolved))
    require(resolved.name.startswith("phase061-step512-"), "E_TEMP_PREFIX", resolved.name)

    def clear_readonly(function: Callable[[str], Any], failing_path: str, error: BaseException) -> None:
        if not isinstance(error, PermissionError):
            raise error
        os.chmod(failing_path, stat.S_IWRITE)
        function(failing_path)

    shutil.rmtree(resolved, onexc=clear_readonly)
    require(not resolved.exists(), "E_TEMP_CLEANUP", str(resolved))


def resolve_subordinate_python() -> str:
    process = subprocess.run(
        ["py", "-3.12", "-c", "import PIL,sys; print(sys.executable)"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        timeout=30,
    )
    require(process.returncode == 0, "E_SUBORDINATE_RUNTIME", process.stderr.decode("utf-8", errors="replace"))
    executable = process.stdout.decode("utf-8").strip()
    require(bool(executable) and pathlib.Path(executable).is_file(), "E_SUBORDINATE_RUNTIME", executable)
    return executable


def run_subordinate(clone: pathlib.Path, spec: dict[str, Any], python_executable: str) -> dict[str, Any]:
    validator_raw = (clone / spec["path"]).read_bytes()
    require(sha256(validator_raw) == spec["sha256"], "E_SUBORDINATE_SHA", spec["unit"])
    argv = [python_executable, spec["path"], *spec["args"]]
    recorded_args = list(spec["args"])
    invocation_kind = "CLI"
    started = time.perf_counter()
    try:
        process = subprocess.run(argv, cwd=clone, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, timeout=600)
        timed_out = False
        exit_code, stdout, stderr = process.returncode, process.stdout, process.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        exit_code, stdout, stderr = 124, error.stdout or b"", error.stderr or b""
    runtime = round(time.perf_counter() - started, 6)
    text = stdout.decode("utf-8")
    stderr.decode("utf-8")
    lines = text.splitlines()
    require(exit_code == 0 and not timed_out, "E_SUBORDINATE_EXIT", f"{spec['unit']}: stdout={text[-1000:]} stderr={stderr.decode('utf-8', errors='replace')[-1000:]}")
    require(stderr == b"", "E_SUBORDINATE_STDERR", f"{spec['unit']}: {stderr.decode('utf-8', errors='replace')}")
    require(sum(line.startswith(spec["terminal_prefix"]) for line in lines) == 1, "E_SUBORDINATE_TERMINAL", spec["unit"])
    for token in spec["required"]:
        require(token in lines, "E_SUBORDINATE_REQUIRED", f"{spec['unit']}:{token}")
    return {"unit": spec["unit"], "path": spec["path"], "invocation_kind": invocation_kind, "args": recorded_args, "python_executable": python_executable, "python_runtime_policy": "PINNED_PYTHON_3_12_WITH_HISTORICAL_DEPENDENCIES", "shell": False, "execution_location": "DISPOSABLE_HISTORICAL_PRECOMMIT_CLONE", "timeout_seconds": 600, "exit_code": exit_code, "timed_out": timed_out, "runtime_seconds": runtime, "stdout_bytes": len(stdout), "stdout_sha256": sha256(stdout), "stdout_lf_sha256": sha256(stdout.replace(b"\r\n", b"\n")), "stderr_bytes": len(stderr), "stderr_sha256": sha256(stderr), "terminal_prefix": spec["terminal_prefix"], "required_lines": spec["required"], "banners": [line for line in lines if line.startswith(("PASS", "FAIL"))], "validator_sha256": sha256(validator_raw), "utf8": True}


def fresh_subordinate_validation() -> dict[str, Any]:
    active_before = repository_state()
    subordinate_python = resolve_subordinate_python()
    records: list[dict[str, Any]] = []
    unit_paths = {unit: paths for unit, _commit, _subject, paths in STEP_UNITS}
    for spec in SUBORDINATES:
        parent, clone = make_remote_clone(f"phase061-step512-{spec['unit'].lower()}-")
        try:
            clone_head = git_text("rev-parse", "HEAD", cwd=clone)
            require(git(["merge-base", "--is-ancestor", STEP51_BASELINE, clone_head], cwd=clone, check=False).returncode == 0, "E_CLONE_HEAD", clone_head)
            historical_parent = git_text("rev-parse", f"{spec['commit']}^", cwd=clone)
            paths = unit_paths[spec["unit"]]
            changed = git_text("diff-tree", "--no-commit-id", "--name-only", "-r", spec["commit"], cwd=clone).splitlines()
            require(set(changed) == set(paths) and len(changed) == len(paths), "E_SUBORDINATE_PATHS", spec["unit"])

            git(["checkout", "-B", BRANCH, historical_parent], cwd=clone)
            git(["update-ref", f"refs/remotes/origin/{BRANCH}", historical_parent], cwd=clone)
            git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=clone)
            git(["update-ref", "refs/remotes/origin/main", MAIN_TIP], cwd=clone)
            git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=clone)
            git(["update-ref", "refs/heads/main", MAIN_TIP], cwd=clone)
            git(["remote", "set-url", "origin", "."], cwd=clone)
            git(["branch", "--set-upstream-to", f"origin/{BRANCH}", BRANCH], cwd=clone)
            git(["checkout", spec["commit"], "--", *paths], cwd=clone)
            require(active_status_paths(clone) == set(paths), "E_SUBORDINATE_PRECOMMIT_PATHS", spec["unit"])

            row = run_subordinate(clone, spec, subordinate_python)
            row["historical_commit"] = spec["commit"]
            row["historical_parent"] = historical_parent
            row["precommit_path_count"] = len(paths)
            row["precommit_paths"] = sorted(paths)
            records.append(row)
            require(active_status_paths(clone) == set(paths), "E_SUBORDINATE_MUTATION", f"{spec['unit']}:after")
        finally:
            remove_temp_tree_strict(parent)
    active_after = repository_state()
    exact(active_after, active_before, "E_ACTIVE_MUTATION", "subordinate before/after")
    return {"count": 6, "pass_count": 6, "records": records, "clone_head": clone_head, "step51_baseline_is_clone_ancestor": True, "historical_precommit_reconstruction": True, "clone_status_before_bytes": 0, "clone_status_after_bytes": 0, "active_repository_unchanged": True}


def require_fixture_clean(clone: pathlib.Path) -> None:
    status = git(["status", "--porcelain=v1", "--untracked-files=all"], cwd=clone).stdout
    if status:
        rows = status.decode("utf-8", errors="replace").splitlines()
        code = "E_FIXTURE_DIRTY_UNTRACKED" if any(row.startswith("?? ") for row in rows) else "E_FIXTURE_DIRTY_TRACKED"
        raise ValidationFailure(code, str(rows))


def verify_fixture_persistence() -> None:
    require(git_text("rev-parse", "HEAD^") == STEP51_BASELINE, "E_FIXTURE_PARENT", "parent")
    require(git_text("show", "-s", "--format=%s", "HEAD") == FINAL_SUBJECT, "E_FIXTURE_SUBJECT", "subject")
    changed = set(git_text("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())
    require(changed == FINAL_PATH_SET and len(changed) == 8, "E_FIXTURE_PATH_SET", str(sorted(changed)))
    for path in FINAL_PATHS:
        raw = (ROOT / path).read_bytes()
        require(raw and b"\r" not in raw and raw.endswith(b"\n"), "E_FIXTURE_CONTENT", path)
    require_fixture_clean(ROOT)


def run_fixture_validator(clone: pathlib.Path, expected_exit: int, prefix: str) -> dict[str, Any]:
    process = subprocess.run([sys.executable, VALIDATOR_PATH, "--verify-fixture"], cwd=clone, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, timeout=120)
    text = process.stdout.decode("utf-8")
    require(process.returncode == expected_exit, "E_FIXTURE_EXIT", text)
    require(process.stderr == b"", "E_FIXTURE_STDERR", process.stderr.decode("utf-8", errors="replace"))
    require(any(line.startswith(prefix) for line in text.splitlines()), "E_FIXTURE_DIAGNOSTIC", text)
    return {"exit_code": process.returncode, "expected_prefix": prefix, "stdout_lf_sha256": sha256(process.stdout.replace(b"\r\n", b"\n")), "stderr_bytes": len(process.stderr)}


def fixture_validation() -> dict[str, Any]:
    parent = pathlib.Path(tempfile.mkdtemp(prefix="phase061-step512-fixtures-"))
    clone = parent / "repo"
    process = subprocess.run(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, timeout=120)
    require(process.returncode == 0, "E_FIXTURE_CLONE", process.stderr.decode("utf-8", errors="replace"))
    try:
        git(["config", "core.autocrlf", "false"], cwd=clone)
        git(["config", "core.eol", "lf"], cwd=clone)
        git(["checkout", "--detach", STEP51_BASELINE], cwd=clone)
        for path in FINAL_PATHS:
            destination = clone / pathlib.PurePosixPath(path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = ROOT / pathlib.PurePosixPath(path)
            if source.is_file():
                shutil.copy2(source, destination)
            else:
                require(path == ARTIFACT_PATH, "E_FIXTURE_MISSING", path)
                destination.write_text('{"fixture_placeholder":true}\n', encoding="utf-8", newline="\n")
        git(["add", "--", *FINAL_PATHS], cwd=clone)
        environment = os.environ.copy()
        environment.update({"GIT_AUTHOR_NAME": "Phase061 Fixture", "GIT_AUTHOR_EMAIL": "phase061-fixture@example.invalid", "GIT_COMMITTER_NAME": "Phase061 Fixture", "GIT_COMMITTER_EMAIL": "phase061-fixture@example.invalid", "GIT_AUTHOR_DATE": "2026-08-26T00:00:00+09:00", "GIT_COMMITTER_DATE": "2026-08-26T00:00:00+09:00"})
        git(["commit", "-m", FINAL_SUBJECT], cwd=clone, env=environment)
        fixture_commit = git_text("rev-parse", "HEAD", cwd=clone)
        clean = run_fixture_validator(clone, 0, "PASS_P061_STEP51_2_FIXTURE")
        tracked = clone / GATE_RESULT_PATH
        original = tracked.read_bytes()
        tracked.write_bytes(original + b"\nDIRTY_TRACKED_FIXTURE\n")
        dirty_tracked = run_fixture_validator(clone, 1, "FAIL_P061_LINEAGE_D: E_FIXTURE_DIRTY_TRACKED:")
        tracked.write_bytes(original)
        require_fixture_clean(clone)
        untracked = clone / "Codex/results/PHASE_061_DIRTY_UNTRACKED_FIXTURE.txt"
        untracked.write_text("dirty\n", encoding="utf-8", newline="\n")
        dirty_untracked = run_fixture_validator(clone, 1, "FAIL_P061_LINEAGE_D: E_FIXTURE_DIRTY_UNTRACKED:")
        untracked.unlink()
        require_fixture_clean(clone)
        return {"baseline_parent": STEP51_BASELINE, "fixture_commit": fixture_commit, "subject": FINAL_SUBJECT, "exact_path_count": 8, "exact_paths": sorted(FINAL_PATH_SET), "clean_descendant_pass": True, "dirty_tracked_rejected": True, "dirty_untracked_rejected": True, "clean_validator": clean, "dirty_tracked_validator": dirty_tracked, "dirty_untracked_validator": dirty_untracked}
    finally:
        remove_temp_tree_strict(parent)


def read_lf(path: str) -> tuple[bytes, str]:
    raw = (ROOT / path).read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), "E_OUTPUT_BYTES", path)
    return raw, raw.decode("utf-8")


def require_sections(text: str, sections: list[str], label: str) -> None:
    headings = {line[3:] for line in text.splitlines() if line.startswith("## ")}
    missing = [section for section in sections if section not in headings]
    require(not missing, "E_OUTPUT_SECTIONS", f"{label}:{missing}")


def final_gate_tokens(text: str) -> list[str]:
    return re.findall(r"\b(?:PASS_P061_LINEAGE_D|CONDITIONAL_P061|FAIL_P061)\b", text)


def validate_control_documents(documents: dict[str, str]) -> None:
    require(set(documents) == {PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH}, "E_HUMAN_SET", "controls")
    for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH):
        rows = [line for line in documents[path].splitlines() if line.startswith("| 061 |")]
        require(len(rows) == 1, "E_HUMAN_ROW", f"{path}:{len(rows)}")
        require("PASS" in rows[0] and "Step 51.2" in rows[0] and "PASS_P061_LINEAGE_D" in rows[0], "E_HUMAN_ROW", path)
        require(final_gate_tokens(rows[0]) == ["PASS_P061_LINEAGE_D"], "E_HUMAN_GATE", f"{path}:{final_gate_tokens(rows[0])}")
    handover_rows = [line for line in documents[HANDOVER_PATH].splitlines() if line.startswith("| Phase 061 Step 51.2 |")]
    require(len(handover_rows) == 1, "E_HUMAN_ROW", f"handover:{len(handover_rows)}")
    require(final_gate_tokens(handover_rows[0]) == ["PASS_P061_LINEAGE_D"], "E_HUMAN_GATE", f"handover:{final_gate_tokens(handover_rows[0])}")
    require("Phase 062 detailed plan" in handover_rows[0] and "Step 52" in handover_rows[0], "E_HUMAN_NEXT", "handover")


def final_output_inventory() -> dict[str, Any]:
    required_sections = {
        REPORT_PATH: ["Summary", "Step Range", "Inputs", "Files", "Read Coverage", "Source and Process Authority", "Lineage and Snapshot Genealogy", "Citation and Equation Authority", "Review and Visual Artifacts", "Dispositions and Carry-forward", "Integrated Validation", "Gate Boundary", "Non-changes", "Open Issues", "Next"],
        GATE_RESULT_PATH: ["Objective and Authority", "Cumulative Step Range", "Inputs and Actual Read Coverage", "Validation Evidence", "Exclusive Gate Decision", "Confirmed", "Unverified", "Ground Not Found", "Carry and Decision Queue", "Protected Non-changes", "Commit Boundary", "Next Condition"],
        PHASE_RESULT_PATH: ["Objective and Authority", "Cumulative Step Range", "Exact Inputs and Actual Read Coverage", "Files Created and Updated", "Commands and Execution Evidence", "Validation", "Exclusive Gate", "Confirmed", "Unverified", "Ground Not Found", "Carry and Decision Queue", "Protected Non-changes", "Exact Phase 062 Entry Condition"],
    }
    texts: dict[str, str] = {}
    records: list[dict[str, Any]] = []
    nonself = [VALIDATOR_PATH, REPORT_PATH, GATE_RESULT_PATH, PHASE_RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH]
    for path in nonself:
        raw, text = read_lf(path)
        texts[path] = text
        records.append({"path": path, "sha256": sha256(raw), "bytes": len(raw), "physical_lines": len(text.splitlines())})
    for path, sections in required_sections.items():
        require_sections(texts[path], sections, path)
    report_gates = re.findall(r"(?m)^Gate: `([^`]+)`\s*$", texts[REPORT_PATH])
    result_gates = re.findall(r"(?m)^Selected Gate: `([^`]+)`\s*$", texts[GATE_RESULT_PATH])
    phase_gates = re.findall(r"(?m)^Exclusive Gate: `([^`]+)`\s*$", texts[PHASE_RESULT_PATH])
    require(report_gates == result_gates == phase_gates == ["PASS_P061_LINEAGE_D"], "E_OUTPUT_GATE", f"{report_gates}/{result_gates}/{phase_gates}")
    combined = "\n".join(texts[path] for path in (REPORT_PATH, GATE_RESULT_PATH, PHASE_RESULT_PATH))
    required_tokens = ["232/232", "231/231", "195/195", "31,553/31,553", "29,335/29,335", "14/14", "130/130", "23/23", "10/10", "9/9", "782/782", "52+5", "91/91", "84/84", "PASS_P061_LINEAGE_D", STEP51_BASELINE, "primary literature", "canonical", "final LaTeX/PDF", "Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md", "Phase 062 detailed plan", "Step 52"]
    for token in required_tokens:
        require(token in combined, "E_OUTPUT_TOKEN", token)
    validate_control_documents({path: texts[path] for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)})
    return {"exact_final_paths": FINAL_PATHS, "hashed_nonself_records": records, "hashed_nonself_count": 7, "human_required_sections": required_sections, "exclusive_gate_headers": True, "phase062_plan_before_step52_required": True}


def build_document() -> dict[str, Any]:
    repo = repository_state()
    objects, inputs = input_inventory()
    counts = integrated_counts(objects)
    commits = step_commit_inventory(repo["head"])
    subordinates = fresh_subordinate_validation()
    fixtures = fixture_validation()
    outputs = final_output_inventory()
    document = {
        "schema_version": "phase061-final-v1", "generated_date": "2026-08-26", "phase": 61, "step": "51.2", "branch": BRANCH,
        "source_commit": SOURCE_COMMIT, "step51_baseline": STEP51_BASELINE,
        "scope": "Phase 061 Step 51.2 integrated v1.0.20 lineage validation and exclusive final gate",
        "authority_boundary": AUTHORITY_BOUNDARY, "repository_state": repo, "input_artifact_inventory": inputs, "integrated_counts": counts,
        "step_commit_inventory": {"count": 7, "records": commits, "all_in_origin_active_ancestry": True, "all_exact_atomic": True},
        "fresh_subordinate_validation": subordinates, "repository_fixtures": fixtures, "final_output_contract": outputs,
        "gate": {"exclusive_decision": "PASS_P061_LINEAGE_D", "status": "PASS", "audit_requirements_complete": True, "external_scientific_truth_validated": False, "external_material_truth_validated": False, "experimental_validity_established": False, "primary_literature_truth_validated": False, "canonical_model_selected": False, "defect_repairs_claimed": 0, "inherited_carry_items": 52, "inherited_phase060_blockers": 5, "new_phase061_blockers": 5, "canonical_debts": 91, "open_debts": 84, "resolved_informational_debts": 7, "next": "Create, review, validate, atomically commit, push and remote-verify the Phase 062 detailed plan before Step 52."},
        "determinism": {"encoding": "UTF-8", "line_endings": "LF", "json_key_order": "sorted", "strict_duplicate_key_parse": True, "nonfinite_rejected": True, "runtime_seconds_masked_in_projection": True, "python_executable_masked_in_projection": True, "raw_stdout_bytes_and_sha_masked_in_projection": True, "stdout_lf_sha256_retained_in_projection": True, "operational_commit_refs_masked_in_projection": True, "fresh_reconstruction_required_each_run": True},
    }
    document["semantic_sha256"] = semantic_hash(document)
    return document


def deterministic_projection(document: Any, label: str) -> dict[str, Any]:
    require(type(document) is dict, "E_PROJECTION_TYPE", label)
    clone = copy.deepcopy(document)
    clone.pop("semantic_sha256", None)
    records = clone.get("fresh_subordinate_validation", {}).get("records")
    require(type(records) is list and len(records) == 6, "E_PROJECTION_SUBORDINATES", label)
    for row in records:
        require(type(row.get("runtime_seconds")) in {int, float} and type(row["runtime_seconds"]) is not bool and row["runtime_seconds"] >= 0, "E_PROJECTION_RUNTIME", row.get("unit", "?"))
        row["runtime_seconds"] = "<RUNTIME_SECONDS_MASKED>"
        row["python_executable"] = "<PYTHON_EXECUTABLE_MASKED>"
        row["stdout_bytes"] = "<RAW_STDOUT_BYTES_MASKED>"
        row["stdout_sha256"] = "<RAW_STDOUT_SHA256_MASKED>"
    clone_head = clone["fresh_subordinate_validation"]["clone_head"]
    require(type(clone_head) is str and re.fullmatch(r"[0-9a-f]{40}", clone_head) is not None, "E_PROJECTION_CLONE_HEAD", label)
    require(git(["merge-base", "--is-ancestor", STEP51_BASELINE, clone_head], check=False).returncode == 0, "E_PROJECTION_CLONE_HEAD", label)
    clone["fresh_subordinate_validation"]["clone_head"] = "<OPERATIONAL_COMMIT_MASKED>"
    fixture = clone.get("repository_fixtures", {})
    require(re.fullmatch(r"[0-9a-f]{40}", fixture.get("fixture_commit", "")) is not None, "E_PROJECTION_FIXTURE", label)
    fixture["fixture_commit"] = "<FIXTURE_COMMIT_MASKED>"
    state = clone.get("repository_state", {})
    for key in ("head", "upstream", "origin_active", "live_remote"):
        require(re.fullmatch(r"[0-9a-f]{40}", state.get(key, "")) is not None, "E_PROJECTION_REPOSITORY", f"{label}:{key}")
        state[key] = "<OPERATIONAL_COMMIT_MASKED>"
    return clone


def validate_diagnostic_contracts(document: dict[str, Any], expected: dict[str, Any]) -> None:
    getters: list[tuple[str, Callable[[dict[str, Any]], Any]]] = [
        ("E_SOURCE_PATHS", lambda d: d["integrated_counts"]["source"]["paths"]), ("E_SOURCE_BLOBS", lambda d: d["integrated_counts"]["source"]["unique_blobs"]), ("E_TEXT_FILES", lambda d: d["integrated_counts"]["source"]["text"]), ("E_TEXT_LINES", lambda d: [d["integrated_counts"]["source"]["physical_lines"], d["integrated_counts"]["source"]["nonblank_lines"]]), ("E_PDF_COVERAGE", lambda d: [d["integrated_counts"]["source"]["pdfs"], d["integrated_counts"]["source"]["pdf_pages"]]), ("E_IMAGE_COVERAGE", lambda d: d["integrated_counts"]["source"]["images"]),
        ("E_PROCESS_ROUTES", lambda d: d["integrated_counts"]["process"]["routes"]), ("E_LINEAGE_ROWS", lambda d: d["integrated_counts"]["lineage"]["rows"]), ("E_SNAPSHOT_GENEALOGY", lambda d: d["integrated_counts"]["snapshot"]), ("E_AUTHORITY_ROWS", lambda d: d["integrated_counts"]["citation"]["authority_rows"]), ("E_AUTHORITY_ROUTING", lambda d: [d["integrated_counts"]["citation"]["required"], d["integrated_counts"]["citation"]["routed"]]), ("E_REVIEW_COVERAGE", lambda d: d["integrated_counts"]["review"]), ("E_DISPOSITION_COVERAGE", lambda d: d["integrated_counts"]["dispositions"]), ("E_CARRY_COVERAGE", lambda d: d["integrated_counts"]["carry"]),
        ("E_MACHINE_COUNT", lambda d: len(d["input_artifact_inventory"]["machine_records"])), ("E_MACHINE_SHA", lambda d: [row["sha256"] for row in d["input_artifact_inventory"]["machine_records"]]), ("E_MACHINE_NODES", lambda d: [row["total_nodes"] for row in d["input_artifact_inventory"]["machine_records"]]), ("E_RESULT_COUNT", lambda d: len(d["input_artifact_inventory"]["result_records"])), ("E_RESULT_SHA", lambda d: [row["sha256"] for row in d["input_artifact_inventory"]["result_records"]]),
        ("E_STEP_COUNT", lambda d: len(d["step_commit_inventory"]["records"])), ("E_STEP_COMMIT", lambda d: [row["commit"] for row in d["step_commit_inventory"]["records"]]), ("E_STEP_PATHS", lambda d: [row["paths"] for row in d["step_commit_inventory"]["records"]]), ("E_STEP_REMOTE", lambda d: [row["in_origin_active_ancestry"] for row in d["step_commit_inventory"]["records"]]),
        ("E_SUBORDINATE_COUNT", lambda d: len(d["fresh_subordinate_validation"]["records"])), ("E_SUBORDINATE_EXIT", lambda d: [row["exit_code"] for row in d["fresh_subordinate_validation"]["records"]]), ("E_SUBORDINATE_TERMINAL", lambda d: [row["terminal_prefix"] for row in d["fresh_subordinate_validation"]["records"]]), ("E_SUBORDINATE_REQUIRED", lambda d: [row["required_lines"] for row in d["fresh_subordinate_validation"]["records"]]), ("E_SUBORDINATE_STDERR", lambda d: [row["stderr_bytes"] for row in d["fresh_subordinate_validation"]["records"]]),
        ("E_CLEAN_FIXTURE", lambda d: d["repository_fixtures"]["clean_descendant_pass"]), ("E_TRACKED_FIXTURE", lambda d: d["repository_fixtures"]["dirty_tracked_rejected"]), ("E_UNTRACKED_FIXTURE", lambda d: d["repository_fixtures"]["dirty_untracked_rejected"]), ("E_FIXTURE_PATHS", lambda d: d["repository_fixtures"]["exact_paths"]), ("E_OUTPUT_HASH", lambda d: [row["sha256"] for row in d["final_output_contract"]["hashed_nonself_records"]]), ("E_OUTPUT_PATHS", lambda d: d["final_output_contract"]["exact_final_paths"]),
        ("E_EXTERNAL_TRUTH", lambda d: [d["gate"]["external_scientific_truth_validated"], d["gate"]["external_material_truth_validated"], d["gate"]["experimental_validity_established"], d["gate"]["primary_literature_truth_validated"]]), ("E_CANONICAL_SELECTION", lambda d: d["gate"]["canonical_model_selected"]), ("E_OPEN_DEBTS", lambda d: [d["gate"]["open_debts"], d["gate"]["resolved_informational_debts"]]), ("E_EXCLUSIVE_GATE", lambda d: d["gate"]["exclusive_decision"]), ("E_TOP_SCHEMA", lambda d: sorted(d)), ("E_GATE_SCHEMA", lambda d: sorted(d["gate"])), ("E_PHASE_TYPE", lambda d: {"type": type(d["phase"]).__name__, "value": d["phase"]}), ("E_SOURCE_COMMIT", lambda d: d["source_commit"]), ("E_BASELINE_COMMIT", lambda d: d["step51_baseline"]), ("E_AUTHORITY_BOUNDARY", lambda d: d["authority_boundary"]),
    ]
    for code, getter in getters:
        try:
            actual, wanted = getter(document), getter(expected)
        except (KeyError, IndexError, TypeError) as error:
            raise ValidationFailure(code, f"contract path: {error}") from error
        require(canonical_bytes(actual) == canonical_bytes(wanted), code, "contract mismatch")


def validate_document(document: Any, expected: dict[str, Any]) -> None:
    require(type(document) is dict, "E_ARTIFACT_TYPE", "top-level")
    require(type(document.get("semantic_sha256")) is str and re.fullmatch(r"[0-9a-f]{64}", document["semantic_sha256"]) is not None, "E_SEMANTIC_SHA_TYPE", "artifact")
    require(document["semantic_sha256"] == semantic_hash(document), "E_SEMANTIC_SHA", "artifact")
    validate_diagnostic_contracts(document, expected)
    exact(deterministic_projection(document, "actual"), deterministic_projection(expected, "expected"), "E_DETERMINISTIC_PROJECTION", "full projection")
    require(document["gate"]["exclusive_decision"] == "PASS_P061_LINEAGE_D", "E_EXCLUSIVE_GATE", "gate")
    require(document["gate"]["audit_requirements_complete"] is True, "E_AUDIT_COMPLETE", "gate")
    require(all(document["gate"][key] is False for key in ("external_scientific_truth_validated", "external_material_truth_validated", "experimental_validity_established", "primary_literature_truth_validated", "canonical_model_selected")), "E_AUTHORITY_PROMOTION", "gate")
    require(document["fresh_subordinate_validation"]["count"] == document["fresh_subordinate_validation"]["pass_count"] == 6, "E_SUBORDINATE_PASS", "6/6")
    require(document["step_commit_inventory"]["count"] == 7, "E_STEP_COUNT", "7")
    require(document["input_artifact_inventory"]["machine_count"] == 10 and document["input_artifact_inventory"]["result_count"] == 6, "E_INPUT_COUNT", "10+6")


def validate_precommit_path_sets(staged: set[str], unstaged: set[str], status: set[str]) -> None:
    require(staged == FINAL_PATH_SET, "E_PRECOMMIT_STAGED", str(sorted(staged)))
    require(not unstaged, "E_PRECOMMIT_UNSTAGED", str(sorted(unstaged)))
    require(status == FINAL_PATH_SET, "E_PRECOMMIT_STATUS", str(sorted(status)))


def negative_probes(document: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    probes: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = []
    def add(name: str, code: str, mutation: Callable[[dict[str, Any]], None]) -> None:
        probes.append((name, code, mutation))
    add("source_paths", "E_SOURCE_PATHS", lambda d: d["integrated_counts"]["source"].__setitem__("paths", 231)); add("source_blobs", "E_SOURCE_BLOBS", lambda d: d["integrated_counts"]["source"].__setitem__("unique_blobs", 232)); add("text_files", "E_TEXT_FILES", lambda d: d["integrated_counts"]["source"].__setitem__("text", 194)); add("text_lines", "E_TEXT_LINES", lambda d: d["integrated_counts"]["source"].__setitem__("physical_lines", 31552)); add("pdf_pages", "E_PDF_COVERAGE", lambda d: d["integrated_counts"]["source"].__setitem__("pdf_pages", 129)); add("image_coverage", "E_IMAGE_COVERAGE", lambda d: d["integrated_counts"]["source"].__setitem__("images", 22))
    add("process_routes", "E_PROCESS_ROUTES", lambda d: d["integrated_counts"]["process"].__setitem__("routes", 231)); add("lineage_rows", "E_LINEAGE_ROWS", lambda d: d["integrated_counts"]["lineage"].__setitem__("rows", 231)); add("snapshot_edge", "E_SNAPSHOT_GENEALOGY", lambda d: d["integrated_counts"]["snapshot"].__setitem__("edges", 8)); add("authority_rows", "E_AUTHORITY_ROWS", lambda d: d["integrated_counts"]["citation"].__setitem__("authority_rows", 781)); add("authority_routing", "E_AUTHORITY_ROUTING", lambda d: d["integrated_counts"]["citation"].__setitem__("routed", 346)); add("review_promotion", "E_REVIEW_COVERAGE", lambda d: d["integrated_counts"]["review"].__setitem__("external_promotions", 1)); add("disposition_drop", "E_DISPOSITION_COVERAGE", lambda d: d["integrated_counts"]["dispositions"].__setitem__("sources", 231)); add("carry_resolution", "E_CARRY_COVERAGE", lambda d: d["integrated_counts"]["carry"].__setitem__("resolved_inherited", 1))
    add("machine_drop", "E_MACHINE_COUNT", lambda d: d["input_artifact_inventory"]["machine_records"].pop()); add("machine_sha", "E_MACHINE_SHA", lambda d: d["input_artifact_inventory"]["machine_records"][0].__setitem__("sha256", "0" * 64)); add("machine_nodes", "E_MACHINE_NODES", lambda d: d["input_artifact_inventory"]["machine_records"][0].__setitem__("total_nodes", 0)); add("result_drop", "E_RESULT_COUNT", lambda d: d["input_artifact_inventory"]["result_records"].pop()); add("result_sha", "E_RESULT_SHA", lambda d: d["input_artifact_inventory"]["result_records"][0].__setitem__("sha256", "0" * 64))
    add("step_drop", "E_STEP_COUNT", lambda d: d["step_commit_inventory"]["records"].pop()); add("step_commit", "E_STEP_COMMIT", lambda d: d["step_commit_inventory"]["records"][0].__setitem__("commit", "0" * 40)); add("step_paths", "E_STEP_PATHS", lambda d: d["step_commit_inventory"]["records"][0]["paths"].pop()); add("step_remote", "E_STEP_REMOTE", lambda d: d["step_commit_inventory"]["records"][0].__setitem__("in_origin_active_ancestry", False))
    add("subordinate_drop", "E_SUBORDINATE_COUNT", lambda d: d["fresh_subordinate_validation"]["records"].pop()); add("subordinate_exit", "E_SUBORDINATE_EXIT", lambda d: d["fresh_subordinate_validation"]["records"][0].__setitem__("exit_code", 1)); add("subordinate_terminal", "E_SUBORDINATE_TERMINAL", lambda d: d["fresh_subordinate_validation"]["records"][0].__setitem__("terminal_prefix", "PASS_FAKE")); add("subordinate_required", "E_SUBORDINATE_REQUIRED", lambda d: d["fresh_subordinate_validation"]["records"][0]["required_lines"].pop()); add("subordinate_stderr", "E_SUBORDINATE_STDERR", lambda d: d["fresh_subordinate_validation"]["records"][0].__setitem__("stderr_bytes", 1))
    add("clean_fixture", "E_CLEAN_FIXTURE", lambda d: d["repository_fixtures"].__setitem__("clean_descendant_pass", False)); add("tracked_fixture", "E_TRACKED_FIXTURE", lambda d: d["repository_fixtures"].__setitem__("dirty_tracked_rejected", False)); add("untracked_fixture", "E_UNTRACKED_FIXTURE", lambda d: d["repository_fixtures"].__setitem__("dirty_untracked_rejected", False)); add("fixture_paths", "E_FIXTURE_PATHS", lambda d: d["repository_fixtures"]["exact_paths"].pop()); add("output_hash", "E_OUTPUT_HASH", lambda d: d["final_output_contract"]["hashed_nonself_records"][0].__setitem__("sha256", "0" * 64)); add("output_paths", "E_OUTPUT_PATHS", lambda d: d["final_output_contract"]["exact_final_paths"].pop())
    add("clone_head_nonhex", "E_PROJECTION_CLONE_HEAD", lambda d: d["fresh_subordinate_validation"].__setitem__("clone_head", "NOT_A_COMMIT")); add("clone_head_unrelated", "E_PROJECTION_CLONE_HEAD", lambda d: d["fresh_subordinate_validation"].__setitem__("clone_head", PROTECTED_TIP))
    add("external_truth", "E_EXTERNAL_TRUTH", lambda d: d["gate"].__setitem__("external_scientific_truth_validated", True)); add("canonical_selection", "E_CANONICAL_SELECTION", lambda d: d["gate"].__setitem__("canonical_model_selected", True)); add("open_debts", "E_OPEN_DEBTS", lambda d: d["gate"].__setitem__("open_debts", 0)); add("wrong_gate", "E_EXCLUSIVE_GATE", lambda d: d["gate"].__setitem__("exclusive_decision", "CONDITIONAL_P061")); add("unknown_top", "E_TOP_SCHEMA", lambda d: d.__setitem__("ESTABLISHED", True)); add("unknown_gate", "E_GATE_SCHEMA", lambda d: d["gate"].__setitem__("ESTABLISHED", True)); add("bool_phase", "E_PHASE_TYPE", lambda d: d.__setitem__("phase", True)); add("source_commit", "E_SOURCE_COMMIT", lambda d: d.__setitem__("source_commit", "0" * 40)); add("baseline_commit", "E_BASELINE_COMMIT", lambda d: d.__setitem__("step51_baseline", "0" * 40)); add("authority_reversal", "E_AUTHORITY_BOUNDARY", lambda d: d.__setitem__("authority_boundary", "PASS proves external truth"))
    rejected: list[str] = []
    for name, expected_code, mutation in probes:
        candidate = copy.deepcopy(document); mutation(candidate); candidate["semantic_sha256"] = semantic_hash(candidate)
        try: validate_document(candidate, expected)
        except ValidationFailure as error:
            require(error.code == expected_code, "E_NEGATIVE_DIAGNOSTIC", f"{name}:{error.code}!={expected_code}"); rejected.append(name)
        else: raise ValidationFailure("E_NEGATIVE_ACCEPTED", name)
    duplicate = pretty_bytes(document).replace(b'"schema_version": "phase061-final-v1",', b'"schema_version": "phase061-final-v1",\n  "schema_version": "phase061-final-v1",', 1)
    strict_json_probes = (
        ("duplicate_json_key", duplicate, "E_DUPLICATE_JSON"),
        ("nonfinite_json_nan", pretty_bytes(document).replace(b'"phase": 61', b'"phase": NaN', 1), "E_NONFINITE_JSON"),
        ("nonfinite_json_positive_overflow", b'{"value":1e9999}\n', "E_NONFINITE_JSON"),
        ("nonfinite_json_negative_overflow", b'{"value":-1e9999}\n', "E_NONFINITE_JSON"),
    )
    for name, raw, expected_code in strict_json_probes:
        try: strict_bytes(raw, name)
        except ValidationFailure as error:
            require(error.code == expected_code, "E_NEGATIVE_DIAGNOSTIC", f"{name}:{error.code}"); rejected.append(name)
        else: raise ValidationFailure("E_NEGATIVE_ACCEPTED", name)
    controls = {path: (ROOT / path).read_text(encoding="utf-8") for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)}
    validate_control_documents(controls)
    for path, prefix in ((PARENT_LEDGER_PATH, "| 061 |"), (ACTIVE_LEDGER_PATH, "| 061 |"), (HANDOVER_PATH, "| Phase 061 Step 51.2 |")):
        changed = dict(controls); lines = changed[path].splitlines(); hits = [index for index, line in enumerate(lines) if line.startswith(prefix)]
        require(len(hits) == 1, "E_NEGATIVE_FIXTURE", path); index = hits[0]; original = lines[index]; lines[index] = original.replace("`PASS_P061_LINEAGE_D`", "`PASS_P061_LINEAGE_D`; `FAIL_P061`", 1); require(lines[index] != original, "E_NEGATIVE_FIXTURE", path); changed[path] = "\n".join(lines) + "\n"
        try: validate_control_documents(changed)
        except ValidationFailure as error:
            require(error.code == "E_HUMAN_GATE", "E_NEGATIVE_DIAGNOSTIC", f"{path}:{error.code}"); rejected.append(f"conflicting_gate:{path}")
        else: raise ValidationFailure("E_NEGATIVE_ACCEPTED", f"conflicting_gate:{path}")
    try: validate_precommit_path_sets(FINAL_PATH_SET, set(), FINAL_PATH_SET | {"Codex/results/UNEXPECTED.txt"})
    except ValidationFailure as error:
        require(error.code == "E_PRECOMMIT_STATUS", "E_NEGATIVE_DIAGNOSTIC", f"extra dirt:{error.code}"); rejected.append("extra_dirty_path")
    else: raise ValidationFailure("E_NEGATIVE_ACCEPTED", "extra_dirty_path")
    try: validate_protected_tips("0" * 40, MAIN_TIP)
    except ValidationFailure as error:
        require(error.code == "E_PROTECTED_DRIFT", "E_NEGATIVE_DIAGNOSTIC", f"protected:{error.code}"); rejected.append("protected_drift")
    else: raise ValidationFailure("E_NEGATIVE_ACCEPTED", "protected_drift")
    return rejected


def validate_precommit() -> None:
    require(git_text("branch", "--show-current") == BRANCH, "E_ACTIVE_BRANCH", "precommit")
    require(git_text("rev-parse", "HEAD") == STEP51_BASELINE, "E_PRECOMMIT_PARENT", "HEAD")
    staged = nul_paths(git(["diff", "--cached", "--name-only", "-z"]).stdout); unstaged = nul_paths(git(["diff", "--name-only", "-z"]).stdout); status = active_status_paths()
    validate_precommit_path_sets(staged, unstaged, status)
    for path in FINAL_PATHS: require(git(["show", f":{path}"]).stdout == (ROOT / path).read_bytes(), "E_STAGED_WORKTREE_BYTES", path)
    git(["diff", "--cached", "--check"]); git(["diff", "--check"])
    validate_control_documents({path: (ROOT / path).read_text(encoding="utf-8") for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)})
    input_inventory(); repository_state()


def validate_persistence(expected_commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None, "E_EXPECTED_COMMIT", expected_commit)
    require(git_text("branch", "--show-current") == BRANCH, "E_ACTIVE_BRANCH", "persistence"); require(git_text("rev-parse", "HEAD") == expected_commit, "E_PERSISTENCE_HEAD", expected_commit); require(git_text("rev-parse", "@{upstream}") == expected_commit, "E_PERSISTENCE_UPSTREAM", expected_commit); require(live_remote_head(BRANCH) == expected_commit, "E_PERSISTENCE_REMOTE", expected_commit)
    require(git_text("show", "-s", "--format=%s", expected_commit) == FINAL_SUBJECT, "E_PERSISTENCE_SUBJECT", expected_commit); require(git_text("rev-parse", f"{expected_commit}^") == STEP51_BASELINE, "E_PERSISTENCE_PARENT", expected_commit)
    changed = set(git_text("diff-tree", "--no-commit-id", "--name-only", "-r", expected_commit).splitlines()); require(changed == FINAL_PATH_SET and len(changed) == 8, "E_PERSISTENCE_PATHS", str(sorted(changed)))
    for path in FINAL_PATHS: require(git(["show", f"{expected_commit}:{path}"]).stdout == (ROOT / path).read_bytes(), "E_COMMITTED_WORKTREE_BYTES", path)
    require(not active_status_paths(), "E_PERSISTENCE_DIRTY", "worktree")
    raw = ARTIFACT.read_bytes(); document = strict_bytes(raw, ARTIFACT_PATH); require(pretty_bytes(document) == raw, "E_ARTIFACT_CANONICAL", ARTIFACT_PATH); require(document.get("semantic_sha256") == semantic_hash(document), "E_SEMANTIC_SHA", ARTIFACT_PATH); require(document.get("gate", {}).get("exclusive_decision") == "PASS_P061_LINEAGE_D", "E_EXCLUSIVE_GATE", ARTIFACT_PATH)
    expected = build_document(); validate_document(document, expected)
    input_inventory(); validate_control_documents({path: (ROOT / path).read_text(encoding="utf-8") for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)}); validate_protected_tips(git_text("rev-parse", f"origin/{PROTECTED_BRANCH}"), git_text("rev-parse", "origin/main")); require(live_remote_head(PROTECTED_BRANCH) == PROTECTED_TIP and live_remote_head("main") == MAIN_TIP, "E_PERSISTENCE_PROTECTED_REMOTE", "protected/main"); require(not git_text("diff", "--name-only", STEP51_BASELINE, expected_commit, "--", "Claude"), "E_CLAUDE_DRIFT", expected_commit)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--collect", action="store_true"); parser.add_argument("--run-negative-probes", action="store_true"); parser.add_argument("--determinism-check", action="store_true"); parser.add_argument("--verify-precommit", action="store_true"); parser.add_argument("--verify-persistence", action="store_true"); parser.add_argument("--expected-commit"); parser.add_argument("--verify-fixture", action="store_true", help=argparse.SUPPRESS); args = parser.parse_args()
    try:
        if args.verify_fixture:
            verify_fixture_persistence(); print("PASS_P061_STEP51_2_FIXTURE"); return 0
        if args.verify_persistence:
            require(bool(args.expected_commit), "E_EXPECTED_COMMIT", "--expected-commit required"); validate_persistence(args.expected_commit); print("PASS_P061_STEP51_2_PERSISTENCE"); return 0
        if args.collect:
            require(not ARTIFACT.exists(), "E_COLLECT_OVERWRITE", ARTIFACT_PATH); expected = build_document(); validate_document(expected, expected); ARTIFACT.write_bytes(pretty_bytes(expected)); document = expected
        else:
            require(ARTIFACT.is_file(), "E_ARTIFACT_MISSING", ARTIFACT_PATH); raw = ARTIFACT.read_bytes(); document = strict_bytes(raw, ARTIFACT_PATH); require(pretty_bytes(document) == raw, "E_ARTIFACT_CANONICAL", ARTIFACT_PATH); expected = build_document(); validate_document(document, expected)
        if args.run_negative_probes:
            rejected = negative_probes(document, expected); print(f"PASS negative_controls={len(rejected)}/{len(rejected)}")
        if args.determinism_check:
            second = build_document(); exact(deterministic_projection(expected, "first"), deterministic_projection(second, "second"), "E_DETERMINISM", "2/2"); print("PASS determinism=2/2 environment_fields_masked=true")
        if args.verify_precommit:
            validate_precommit(); print("PASS_P061_STEP51_2_PRECOMMIT")
        print("PASS coverage paths=232/232 blobs=231/231 text=195/195 lines=31553/31553 nonblank=29335/29335")
        print("PASS artifacts pdf=14/14 pages=130/130 images=23/23 snapshots=10/10 unique_snapshot_blobs=9/9")
        print("PASS authority process_routes=232/232 lineage_rows=232/232 citation_rows=782/782 review_union=104/104")
        print("PASS routing dispositions=232/232 inherited=52+5 debts=91/91 open=84/84 new_blockers=5")
        print("PASS lineage_units=7/7 subordinates=6/6 external_scientific=false external_material=false canonical=false")
        print("PASS_P061_LINEAGE_D"); return 0
    except (ValidationFailure, OSError, UnicodeError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError) as error:
        print(f"FAIL_P061_LINEAGE_D: {error}"); return 1


if __name__ == "__main__":
    raise SystemExit(main())
