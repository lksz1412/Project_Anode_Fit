#!/usr/bin/env python3
"""Build and validate the Phase 060 Step 45.2 integrated lineage evidence.

All subordinate validators run in a disposable remote-synchronised clone.  The
active checkout may contain only the exact Step 45.2 allowlist before its atomic
commit.  Scientific truth and material validity are deliberately outside this
gate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
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
STEP45_BASELINE = "6a468ee6b9ec3b5f16d0a528c7f1766ad86af4b5"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
FINAL_SUBJECT = "audit(phase060): close v1019 lineage gate"

VALIDATOR_PATH = "Codex/work/v1019_phase060/validate_phase060_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_060_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_060_V1019_LINEAGE_REPORT_C.md"
GATE_RESULT_PATH = "Codex/results/PHASE_060_STEP_045_2_GATE_RESULT.md"
PHASE_RESULT_PATH = "Codex/results/PHASE_060_RESULT.md"
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
    "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json": "c246a05e2d13d1d33dab1682bda712611367412d241cd277694a35aaf7bcf140",
    "Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json": "36616b86f934b7c594e68e1b991c261c7b391b70e2c4c52375d452b3d69a06ad",
    "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json": "d61e514712a91b7eea89e723cf33745b00a20ee59387abcb450db778122174f7",
    "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json": "4f38d3678870c32b1910701e62506547f2bc471684ceb0578775ba29fb57e2af",
    "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json": "9fc8d1f4bd797c394effe5d72771cca0a3d4b6426e53c3a2d95d0f9f5e446bcf",
    "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json": "95c89d7536b492d21ccfdee3d6077bcd04f2054805d52bf4f067f70689864ebe",
    "Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json": "f2eb8589c3760c7567056a2890e77b9d83ea131fa4cee253c5b7c90ad9ad3468",
    "Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json": "1656e75871d33b438b48d17e861c4398debd027a5067c40108366259141afe50",
    "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json": "72848094865e0b2cad1110df92e7543dc287607af45dc2346e2040bd65812271",
}

SUBORDINATES = [
    ("validate_phase060_step40_source_topology.py", "PASS_P060_STEP40_SOURCE_TOPOLOGY 1/1"),
    ("validate_phase060_step41_process_authority.py", "PASS_P060_STEP41_PROCESS_AUTHORITY 1/1"),
    ("validate_phase060_step42_runtime_artifacts.py", "PASS_P060_STEP42_RUNTIME_ARTIFACTS 42/42"),
    ("validate_phase060_step43_doc_code_trace.py", "PASS_P060_STEP43_DOC_CODE_CONFORMANCE 11815/11815"),
    ("validate_phase060_step44_physics_validation.py", "PASS_P060_STEP44_PHYSICS_REDERIVATION"),
    ("validate_phase060_step45_dispositions.py", "PASS_P060_STEP45_DISPOSITIONS"),
]
WORK = "Codex/work/v1019_phase060"

STEP_UNITS = [
    {
        "unit": "PLAN_ACTIVATION",
        "commit": "8847493139708b3336f6947be13a3e77dda22e05",
        "subject": "docs(phase060): plan v1019 lineage reaudit",
        "paths": [
            "Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md",
            "Codex/work/v1019_phase060/validate_phase060_plan.py",
            "Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json",
            "Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md",
            PARENT_LEDGER_PATH,
            ACTIVE_LEDGER_PATH,
            HANDOVER_PATH,
        ],
    },
    {
        "unit": "STEP_40",
        "commit": "ec30b212db89656957c43b3b31109e8874f56b29",
        "subject": "audit(phase060): freeze v1019 source topology",
        "paths": [
            "Codex/work/v1019_phase060/build_phase060_step40_source_topology.py",
            "Codex/work/v1019_phase060/validate_phase060_step40_source_topology.py",
            "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json",
            "Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json",
            "Codex/results/PHASE_060_STEP_040_SOURCE_TOPOLOGY_RESULT.md",
            ACTIVE_LEDGER_PATH,
            PARENT_LEDGER_PATH,
            HANDOVER_PATH,
        ],
    },
    {
        "unit": "STEP_41",
        "commit": "0f09a8d17159cbad9764e88949cc9ce9321e958f",
        "subject": "audit(phase060): adjudicate v1019 process authority",
        "paths": [
            "Codex/work/v1019_phase060/build_phase060_step41_process_authority.py",
            "Codex/work/v1019_phase060/validate_phase060_step41_process_authority.py",
            "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json",
            "Codex/results/PHASE_060_STEP_041_PROCESS_AUTHORITY_RESULT.md",
            ACTIVE_LEDGER_PATH,
            PARENT_LEDGER_PATH,
            HANDOVER_PATH,
        ],
    },
    {
        "unit": "STEP_42",
        "commit": "229a756996bb81b4184aa2a0a4b141d002a2ceae",
        "subject": "audit(phase060): verify v1019 runtime artifacts",
        "paths": [
            "Codex/work/v1019_phase060/audit_phase060_step42_runtime_artifacts.py",
            "Codex/work/v1019_phase060/validate_phase060_step42_runtime_artifacts.py",
            "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json",
            "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json",
            "Codex/results/PHASE_060_STEP_042_RUNTIME_ARTIFACT_RESULT.md",
            HANDOVER_PATH,
            PARENT_LEDGER_PATH,
            ACTIVE_LEDGER_PATH,
        ],
    },
    {
        "unit": "STEP_43",
        "commit": "7a4c1dbea22c53abe5a8dce3c3ccf58a0915e1dc",
        "subject": "audit(phase060): trace doc-led implementation",
        "paths": [
            "Codex/work/v1019_phase060/build_phase060_step43_doc_code_trace.py",
            "Codex/work/v1019_phase060/validate_phase060_step43_doc_code_trace.py",
            "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json",
            "Codex/results/PHASE_060_STEP_043_DOC_CODE_CONFORMANCE_RESULT.md",
            HANDOVER_PATH,
            PARENT_LEDGER_PATH,
            ACTIVE_LEDGER_PATH,
        ],
    },
    {
        "unit": "STEP_44",
        "commit": "70b14fd102fca40ef17bee44e924c09dde1d9eff",
        "subject": "audit(phase060): rederive v1019 physics",
        "paths": [
            "Codex/work/v1019_phase060/build_phase060_step44_physics_validation.py",
            "Codex/work/v1019_phase060/validate_phase060_step44_physics_validation.py",
            "Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md",
            "Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json",
            "Codex/results/PHASE_060_STEP_044_PHYSICS_REDERIVATION_RESULT.md",
            HANDOVER_PATH,
            PARENT_LEDGER_PATH,
            ACTIVE_LEDGER_PATH,
        ],
    },
    {
        "unit": "STEP_45_1",
        "commit": STEP45_BASELINE,
        "subject": "audit(phase060): disposition v1019 lineage",
        "paths": [
            HANDOVER_PATH,
            PARENT_LEDGER_PATH,
            ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_060_STEP_045_1_DISPOSITION_RESULT.md",
            "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json",
            "Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json",
            "Codex/work/v1019_phase060/build_phase060_step45_dispositions.py",
            "Codex/work/v1019_phase060/validate_phase060_step45_dispositions.py",
        ],
    },
]

AUTHORITY_BOUNDARY = (
    "PASS_P060_LINEAGE_C establishes complete v1.0.19 lineage audit coverage, internal "
    "conformance routing, and independent source-model rederivation review only. It does "
    "not establish canonical-model selection, defect repair, primary-literature truth, "
    "external material or experimental validity, parameter identifiability, final LaTeX/PDF, "
    "or publication readiness."
)


class ValidationFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def exact(actual: Any, expected: Any, label: str) -> None:
    require(canonical_bytes(actual) == canonical_bytes(expected), f"exact/type mismatch: {label}")


def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValidationFailure(f"E_DUPLICATE_JSON: duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(value: str) -> None:
    raise ValidationFailure(f"E_NONFINITE_JSON: non-finite JSON constant: {value}")


def strict_bytes(data: bytes, label: str) -> Any:
    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
        )
    except ValidationFailure:
        raise
    except Exception as exc:
        raise ValidationFailure(f"E_STRICT_JSON: strict JSON parse failed for {label}: {exc}") from exc


def traversal_stats(value: Any) -> dict[str, int]:
    value_nodes = 0
    key_nodes = 0
    max_depth = 0

    def walk(node: Any, depth: int) -> None:
        nonlocal value_nodes, key_nodes, max_depth
        value_nodes += 1
        max_depth = max(max_depth, depth)
        if isinstance(node, dict):
            key_nodes += len(node)
            for child in node.values():
                walk(child, depth + 1)
        elif isinstance(node, list):
            for child in node:
                walk(child, depth + 1)

    walk(value, 0)
    return {
        "value_nodes": value_nodes,
        "key_nodes": key_nodes,
        "total_nodes": value_nodes + key_nodes,
        "max_depth": max_depth,
    }


def semantic_hash(document: dict[str, Any]) -> str:
    clone = copy.deepcopy(document)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def git(
    args: list[str],
    *,
    cwd: pathlib.Path = ROOT,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(
        ["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=False, env=env,
    )
    if check and cp.returncode:
        raise ValidationFailure(f"git {' '.join(args)} failed: {cp.stderr.decode('utf-8', 'replace')}")
    return cp


def git_text(*args: str, cwd: pathlib.Path = ROOT) -> str:
    return git(list(args), cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(path: str, ref: str = STEP45_BASELINE) -> bytes:
    require("\\" not in path and not path.startswith("/"), f"non-POSIX path: {path}")
    return git(["show", f"{ref}:{path}"]).stdout


def active_status_paths() -> list[str]:
    raw = git(["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    entries = [row for row in raw.split(b"\0") if row]
    paths: list[str] = []
    index = 0
    while index < len(entries):
        text = entries[index].decode("utf-8")
        require(len(text) >= 4, f"malformed status entry: {text!r}")
        status = text[:2]
        paths.append(pathlib.PurePosixPath(text[3:].replace("\\", "/")).as_posix())
        index += 1
        if "R" in status or "C" in status:
            require(index < len(entries), "malformed rename/copy status")
            paths.append(pathlib.PurePosixPath(entries[index].decode("utf-8").replace("\\", "/")).as_posix())
            index += 1
    return sorted(set(paths))


def live_remote_head(branch: str) -> str:
    lines = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").splitlines()
    require(len(lines) == 1, f"live remote cardinality: {branch}")
    return lines[0].split()[0]


def repository_state() -> dict[str, Any]:
    branch = git_text("rev-parse", "--abbrev-ref", "HEAD")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    remote_active = git_text("rev-parse", f"origin/{BRANCH}")
    protected = git_text("rev-parse", "origin/codex/lib-physics-endgame-v1025_2")
    main = git_text("rev-parse", "origin/main")
    live_remote = live_remote_head(BRANCH)
    live_protected = live_remote_head("codex/lib-physics-endgame-v1025_2")
    live_main = live_remote_head("main")
    require(branch == BRANCH, "active branch drift")
    require(head == upstream == remote_active == live_remote, "active local/upstream/remote divergence")
    require(protected == live_protected == PROTECTED_TIP, "protected local/live tip drift")
    require(main == live_main == MAIN_TIP, "main local/live tip drift")
    require(git(["merge-base", "--is-ancestor", STEP45_BASELINE, head], check=False).returncode == 0,
            "Step 45.1 baseline is not ancestor of active HEAD")
    status_paths = active_status_paths()
    unexpected = sorted(set(status_paths) - FINAL_PATH_SET)
    require(not unexpected, f"unexpected dirty paths outside final allowlist: {unexpected}")
    claude_diff = git(["diff", "--name-only", "origin/codex/lib-physics-endgame-v1025_2", "--", "Claude"]).stdout.decode("utf-8").splitlines()
    claude_untracked = git(["ls-files", "--others", "--exclude-standard", "--", "Claude"]).stdout.decode("utf-8").splitlines()
    require(claude_diff == [], f"Claude tracked drift: {claude_diff}")
    require(claude_untracked == [], f"Claude untracked drift: {claude_untracked}")
    return {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "origin_active": remote_active,
        "live_remote": live_remote,
        "step45_baseline": STEP45_BASELINE,
        "step45_baseline_is_ancestor": True,
        "protected": protected,
        "live_protected": live_protected,
        "main": main,
        "live_main": live_main,
        "precommit_allowlist": FINAL_PATHS,
        "only_allowlisted_status_paths": True,
        "unexpected_status_paths": unexpected,
        "claude_tracked_diff_count": 0,
        "claude_untracked_count": 0,
    }


def machine_inventory() -> tuple[dict[str, Any], dict[str, Any]]:
    objects: dict[str, Any] = {}
    records: list[dict[str, Any]] = []
    for path, expected_sha in MACHINE_ARTIFACTS.items():
        raw = git_blob(path)
        require(sha256(raw) == expected_sha, f"machine artifact SHA drift: {path}")
        current = (ROOT / path).read_bytes()
        require(current.replace(b"\r\n", b"\n") == raw, f"machine artifact worktree/Git mismatch: {path}")
        obj = strict_bytes(raw, path)
        require(type(obj) is dict, f"machine artifact top-level type: {path}")
        records.append({
            "path": path, "sha256": expected_sha, "bytes": len(raw),
            "physical_lines": len(raw.decode("utf-8").splitlines()),
            **traversal_stats(obj), "top_level_keys": sorted(obj),
        })
        objects[path] = obj
    require(len(records) == 9, "machine inventory count")
    return objects, {
        "count": 9, "records": records, "strict_duplicate_keys": True,
        "nonfinite_rejected": True,
    }


def integrated_counts(objects: dict[str, Any]) -> dict[str, Any]:
    topology = objects["Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json"]
    attestation = objects["Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json"]
    process = objects["Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json"]
    runtime = objects["Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json"]
    artifacts = objects["Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json"]
    trace = objects["Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json"]
    physics = objects["Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json"]
    dispositions = objects["Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json"]
    carry = objects["Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json"]
    counts = topology["counts"]
    expected_source = {
        "primary_paths": 77, "primary_unique_blobs": 77, "witness_occurrences": 2,
        "witness_new_unique_blobs": 1, "inspection_path_occurrences": 79,
        "inspection_unique_blobs": 78, "inspection_text_files": 61,
        "inspection_text_physical_lines": 9904, "inspection_text_nonblank_lines": 9145,
        "pdf_files": 3, "pdf_pages": 95, "image_unique_blobs": 13,
        "image_occurrences": 14, "binary_files": 1, "tex_files": 42,
        "tex_physical_lines": 5636,
    }
    exact({key: counts[key] for key in expected_source}, expected_source, "source topology counts")
    require(len(attestation["sources"]) == 42, "TeX attestation source count")
    require(all(row.get("coverage_status") == "READ_FULL" for row in attestation["sources"]), "TeX attestation incomplete")
    require(len(process["sources"]) == 17 and len(process["claims"]) == 36, "process source/claim counts")
    require(len(process["defect_correction_records"]) == 10, "process defect/correction count")
    require(len(process["contradictions"]) == 6 and len(process["unresolved_queue"]) == 11, "process obligation counts")
    for key, value in {"files": 4, "physical_lines": 1796, "definitions": 56, "call_edges": 444, "public_entries": 34, "path_semantic_records": 8, "assert_nodes": 0}.items():
        require(runtime["code_summary"][key] == value, f"runtime summary: {key}")
    require(runtime["golden_npz"]["array_count"] == 13, "NPZ array count")
    require(artifacts["pdf_summary"] == {"files": 3, "pages": 95, "rendered_pages": 95}, "PDF coverage")
    require(artifacts["image_summary"] == {"occurrences": 13, "unique_blobs": 13}, "unique image coverage")
    require(len(trace["candidate_dispositions"]) == 914 and len(trace["trace_rows"]) == 28, "trace coverage")
    require(len(trace["implementation_definitions"]) == 57 and len(trace["call_edge_index"]) == 882, "trace AST coverage")
    require(len(trace["test_gate_index"]) == 46 and len(trace["artifact_consumer_index"]) == 17, "trace gate/consumer coverage")
    require(len(physics["derivation_checks"]) == 22 and len(physics["findings"]) == 20 and len(physics["source_conflicts"]) == 10, "physics coverage")
    exact(physics["summary"]["check_results"], {"PASS": 5, "FAIL": 6, "CONDITIONAL": 9, "UNVERIFIED": 2, "NOT_APPLICABLE": 0}, "physics result distribution")
    require(len(dispositions["source_manifest"]) == len(dispositions["dispositions"]) == 173, "disposition coverage")
    exact(dispositions["gate_summary"]["primary_disposition_counts"], {"CORRECT": 71, "PRESERVE": 48, "UNVERIFIED": 38, "THEORY_ONLY": 11, "EMPIRICAL_ONLY": 5}, "disposition distribution")
    require(len(carry["inherited_items"]) == 52 and len(carry["new_blockers"]) == 5, "carry/blocker counts")
    require(carry["gate_summary"]["acceptance_satisfied_count"] == 0, "false carry acceptance")
    require(carry["gate_summary"]["resolution_status_counts"] == {"NOT_RESOLVED": 52}, "false carry resolution")
    return {
        "primary": {"paths": 77, "unique_blobs": 77, "text_files": 60, "physical_lines": 8784, "nonblank_lines": 8025},
        "witness": {"occurrences": 2, "new_blobs": 1, "text_files": 1, "physical_lines": 1120, "nonblank_lines": 1120},
        "inspection": {"occurrences": 79, "unique_blobs": 78, "text_files": 61, "physical_lines": 9904, "nonblank_lines": 9145, "pdfs": 3, "pdf_pages": 95, "image_unique": 13, "image_occurrences": 14, "binary": 1},
        "tex": {"files": 42, "physical_lines": 5636, "include_edges": 39, "expansion_records": 42},
        "process": {"sources": 17, "claims": 36, "defect_corrections": 10, "contradictions": 6, "unresolved": 11, "scientific_promotions": 0, "runtime_promotions": 0},
        "runtime": {"python_files": 4, "physical_lines": 1796, "definition_body_definitions": 56, "definition_body_calls": 444, "npz_arrays": 13, "pdfs": 3, "pdf_pages": 95, "images_unique": 13},
        "trace": {"candidates": 914, "rows": 28, "definitions": 57, "calls": 882, "public_production": 20, "support": 14, "source_gates": 46, "artifact_consumers": 17, "P0": 0, "P1": 12, "P2": 13},
        "physics": {"checks": 22, "PASS": 5, "FAIL": 6, "CONDITIONAL": 9, "UNVERIFIED": 2, "P0": 0, "P1": 12, "P2": 8, "conflicts_preserved": 10},
        "dispositions": {"sources": 173, "CORRECT": 71, "PRESERVE": 48, "UNVERIFIED": 38, "THEORY_ONLY": 11, "EMPIRICAL_ONLY": 5, "orphans": 0, "external_promotions": 0},
        "carry_forward": {"inherited": 52, "OPEN": 41, "PRESERVED_ACTIVE": 11, "touched": 33, "unchanged": 19, "resolved": 0, "new_blockers": 5},
    }


def step_commit_inventory(current_tip: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in STEP_UNITS:
        commit = spec["commit"]
        require(git(["merge-base", "--is-ancestor", commit, current_tip], check=False).returncode == 0, f"unit commit not in active ancestry: {spec['unit']}")
        require(git(["merge-base", "--is-ancestor", commit, f"origin/{BRANCH}"], check=False).returncode == 0, f"unit commit not in origin-active ancestry: {spec['unit']}")
        subject = git_text("show", "-s", "--format=%s", commit)
        require(subject == spec["subject"], f"unit subject mismatch: {spec['unit']}")
        changed = git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit]).stdout.decode("utf-8").splitlines()
        require(len(changed) == len(set(changed)), f"unit duplicate changed path: {spec['unit']}")
        require(set(changed) == set(spec["paths"]) and len(changed) == len(spec["paths"]), f"unit exact path mismatch: {spec['unit']}")
        records.append({
            "unit": spec["unit"], "commit": commit, "subject": subject,
            "path_count": len(changed), "paths": sorted(changed),
            "in_active_ancestry": True, "in_origin_active_ancestry": True,
            "result_and_machine_evidence_co_committed": True,
        })
    return records


def make_remote_clone(prefix: str) -> tuple[pathlib.Path, pathlib.Path]:
    parent = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    clone = parent / "repo"
    cp = subprocess.run(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    require(cp.returncode == 0, f"disposable clone failed: {cp.stderr.decode('utf-8', 'replace')}")
    origin_url = git_text("remote", "get-url", "origin")
    git(["remote", "set-url", "origin", origin_url], cwd=clone)
    refspecs = [
        f"+refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}",
        "+refs/heads/codex/lib-physics-endgame-v1025_2:refs/remotes/origin/codex/lib-physics-endgame-v1025_2",
        "+refs/heads/main:refs/remotes/origin/main",
    ]
    git(["fetch", "--force", "origin", *refspecs], cwd=clone)
    git(["config", "core.autocrlf", "false"], cwd=clone)
    git(["config", "core.eol", "lf"], cwd=clone)
    git(["checkout", "-B", BRANCH, f"origin/{BRANCH}"], cwd=clone)
    git(["branch", "--set-upstream-to", f"origin/{BRANCH}", BRANCH], cwd=clone)
    require(git(["status", "--porcelain=v1", "--untracked-files=all"], cwd=clone).stdout == b"", "disposable clone initially dirty")
    return parent, clone


def remove_temp_tree_strict(path: pathlib.Path) -> None:
    resolved = path.resolve()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    require(resolved.parent == temp_root, f"cleanup target outside temp root: {resolved}")
    require(resolved.name.startswith("phase060-step452-"), f"cleanup target prefix mismatch: {resolved}")

    def clear_readonly(function: Callable[[str], Any], failing_path: str, error: BaseException) -> None:
        if not isinstance(error, PermissionError):
            raise error
        os.chmod(failing_path, stat.S_IWRITE)
        function(failing_path)

    shutil.rmtree(resolved, onexc=clear_readonly)
    require(not resolved.exists(), f"temporary tree survived cleanup: {resolved}")


def run_subordinate(clone: pathlib.Path, name: str, terminal: str) -> dict[str, Any]:
    argv = [sys.executable, f"{WORK}/{name}"]
    started = time.perf_counter()
    try:
        cp = subprocess.run(argv, cwd=clone, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, timeout=600)
        timed_out = False
        exit_code, stdout, stderr = cp.returncode, cp.stdout, cp.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code, stdout, stderr = 124, exc.stdout or b"", exc.stderr or b""
    elapsed = round(time.perf_counter() - started, 6)
    text = stdout.decode("utf-8")
    stderr.decode("utf-8")
    banners = [line for line in text.splitlines() if line.startswith(("PASS", "FAIL", "BUILT", "WROTE", "COUNTS"))]
    require(exit_code == 0, f"subordinate exit nonzero: {name}: {text[-1000:]}")
    require(not timed_out and stderr == b"", f"subordinate abnormal: {name}")
    require(terminal in text.splitlines(), f"subordinate terminal missing: {name}")
    return {
        "name": name, "path": f"{WORK}/{name}", "argv": argv, "shell": False,
        "execution_location": "DISPOSABLE_REMOTE_SYNCED_CLONE", "timeout_seconds": 600,
        "exit_code": exit_code, "timed_out": timed_out, "runtime_seconds": elapsed,
        "stdout_bytes": len(stdout), "stdout_sha256": sha256(stdout),
        "stdout_lf_sha256": sha256(stdout.replace(b"\r\n", b"\n")),
        "stderr_bytes": len(stderr), "stderr_sha256": sha256(stderr),
        "terminal": terminal, "banners": banners, "traceback": False, "utf8": True,
    }


def fresh_subordinate_validation() -> dict[str, Any]:
    active_before = repository_state()
    parent, clone = make_remote_clone("phase060-step452-validators-")
    try:
        clone_head = git_text("rev-parse", "HEAD", cwd=clone)
        pre_status = git(["status", "--porcelain=v1", "--untracked-files=all"], cwd=clone).stdout
        outcomes = [run_subordinate(clone, name, terminal) for name, terminal in SUBORDINATES]
        post_status = git(["status", "--porcelain=v1", "--untracked-files=all"], cwd=clone).stdout
        require(pre_status == post_status == b"", "subordinate clone mutated")
    finally:
        remove_temp_tree_strict(parent)
    active_after = repository_state()
    exact(active_after, active_before, "active repository state before/after subordinates")
    return {
        "count": 6, "pass_count": 6, "records": outcomes, "clone_head": clone_head,
        "clone_status_before_bytes": 0, "clone_status_after_bytes": 0,
        "active_repository_unchanged": True,
    }


def require_fixture_clean(clone: pathlib.Path) -> None:
    status = git(["status", "--porcelain=v1", "--untracked-files=all"], cwd=clone).stdout
    if status:
        rows = status.decode("utf-8", "replace").splitlines()
        if any(row.startswith("?? ") for row in rows):
            raise ValidationFailure(f"E_FIXTURE_DIRTY_UNTRACKED: {rows}")
        raise ValidationFailure(f"E_FIXTURE_DIRTY_TRACKED: {rows}")


def verify_fixture_persistence() -> None:
    require(git_text("rev-parse", "HEAD^") == STEP45_BASELINE, "E_FIXTURE_PARENT: parent mismatch")
    require(git_text("show", "-s", "--format=%s", "HEAD") == FINAL_SUBJECT, "E_FIXTURE_SUBJECT: subject mismatch")
    changed = git(["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"]).stdout.decode("utf-8").splitlines()
    require(set(changed) == FINAL_PATH_SET and len(changed) == 8, "E_FIXTURE_PATH_SET: exact-eight mismatch")
    for path in FINAL_PATHS:
        raw = (ROOT / pathlib.PurePosixPath(path)).read_bytes()
        require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"E_FIXTURE_CONTENT: invalid text bytes: {path}")
    require_fixture_clean(ROOT)


def run_fixture_validator(clone: pathlib.Path, expected_exit: int, expected_line: str) -> dict[str, Any]:
    cp = subprocess.run(
        [sys.executable, VALIDATOR_PATH, "--verify-fixture"], cwd=clone,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
    )
    text = cp.stdout.decode("utf-8")
    require(cp.returncode == expected_exit, f"fixture validator exit mismatch: {text}")
    require(cp.stderr == b"", f"fixture validator stderr: {cp.stderr.decode('utf-8', 'replace')}")
    require(any(line.startswith(expected_line) for line in text.splitlines()),
            f"fixture validator diagnostic mismatch: {text}")
    return {
        "exit_code": cp.returncode, "expected_line": expected_line,
        "stdout_lf_sha256": sha256(cp.stdout.replace(b"\r\n", b"\n")),
        "stderr_bytes": len(cp.stderr),
    }


def fixture_validation() -> dict[str, Any]:
    parent = pathlib.Path(tempfile.mkdtemp(prefix="phase060-step452-fixtures-"))
    clone = parent / "repo"
    cp = subprocess.run(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    require(cp.returncode == 0, f"fixture clone failed: {cp.stderr.decode('utf-8', 'replace')}")
    try:
        git(["config", "core.autocrlf", "false"], cwd=clone)
        git(["config", "core.eol", "lf"], cwd=clone)
        git(["checkout", "--detach", STEP45_BASELINE], cwd=clone)
        for path in FINAL_PATHS:
            destination = clone / pathlib.PurePosixPath(path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = ROOT / pathlib.PurePosixPath(path)
            if source.is_file():
                shutil.copy2(source, destination)
            else:
                require(path == ARTIFACT_PATH, f"fixture missing non-artifact final path: {path}")
                destination.write_text('{"fixture_placeholder":true}\n', encoding="utf-8", newline="\n")
        git(["add", "--", *FINAL_PATHS], cwd=clone)
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": "Phase060 Fixture", "GIT_AUTHOR_EMAIL": "phase060-fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Phase060 Fixture", "GIT_COMMITTER_EMAIL": "phase060-fixture@example.invalid",
            "GIT_AUTHOR_DATE": "2026-08-26T00:00:00+09:00", "GIT_COMMITTER_DATE": "2026-08-26T00:00:00+09:00",
        })
        git(["commit", "-m", FINAL_SUBJECT], cwd=clone, env=env)
        fixture_commit = git_text("rev-parse", "HEAD", cwd=clone)
        parent_commit = git_text("rev-parse", "HEAD^", cwd=clone)
        changed = git(["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"], cwd=clone).stdout.decode("utf-8").splitlines()
        require(parent_commit == STEP45_BASELINE, "fixture parent mismatch")
        require(set(changed) == FINAL_PATH_SET and len(changed) == 8, "fixture exact-eight mismatch")
        require(git_text("show", "-s", "--format=%s", "HEAD", cwd=clone) == FINAL_SUBJECT, "fixture subject mismatch")
        clean_validation = run_fixture_validator(clone, 0, "PASS_P060_STEP45_2_FIXTURE")
        tracked_path = clone / pathlib.PurePosixPath(GATE_RESULT_PATH)
        tracked_original = tracked_path.read_bytes()
        tracked_path.write_bytes(tracked_original + b"\nDIRTY_TRACKED_FIXTURE\n")
        tracked_validation = run_fixture_validator(
            clone, 1, "FAIL_P060_LINEAGE_C: E_FIXTURE_DIRTY_TRACKED:"
        )
        tracked_path.write_bytes(tracked_original)
        require_fixture_clean(clone)
        untracked_path = clone / "Codex/results/PHASE_060_DIRTY_UNTRACKED_FIXTURE.txt"
        untracked_path.write_text("dirty\n", encoding="utf-8", newline="\n")
        untracked_validation = run_fixture_validator(
            clone, 1, "FAIL_P060_LINEAGE_C: E_FIXTURE_DIRTY_UNTRACKED:"
        )
        untracked_path.unlink()
        require_fixture_clean(clone)
        return {
            "baseline_parent": STEP45_BASELINE, "fixture_commit": fixture_commit,
            "subject": FINAL_SUBJECT, "exact_path_count": 8, "exact_paths": sorted(changed),
            "clean_descendant_pass": True, "dirty_tracked_rejected": True,
            "dirty_untracked_rejected": True,
            "clean_validator": clean_validation,
            "dirty_tracked_validator": tracked_validation,
            "dirty_untracked_validator": untracked_validation,
        }
    finally:
        remove_temp_tree_strict(parent)


def read_lf(path: str) -> tuple[bytes, str]:
    raw = (ROOT / pathlib.PurePosixPath(path)).read_bytes()
    require(raw, f"empty final output: {path}")
    text = raw.decode("utf-8")
    require("\r" not in text, f"final output is not LF-only: {path}")
    require(text.endswith("\n"), f"final output lacks terminal LF: {path}")
    return raw, text


def require_sections(text: str, sections: list[str], label: str) -> None:
    headings = {line[3:] for line in text.splitlines() if line.startswith("## ")}
    missing = [section for section in sections if section not in headings]
    require(not missing, f"missing sections in {label}: {missing}")


def final_output_inventory() -> dict[str, Any]:
    required_sections = {
        REPORT_PATH: ["Summary", "Step Range", "Inputs", "Files", "Read Coverage", "Source Topology", "Process Authority", "Runtime/Artifact Evidence", "Doc-code Conformance", "Physics Rederivation", "Dispositions", "Gate Boundary", "Non-changes", "Open Issues", "Next"],
        GATE_RESULT_PATH: ["Objective and Authority", "Cumulative Step Range", "Inputs and Actual Read Coverage", "Validation Evidence", "Exclusive Gate Decision", "Confirmed", "Unverified", "Ground Not Found", "Unresolved and Decision Queue", "Protected Non-changes", "Commit Boundary", "Next Condition"],
        PHASE_RESULT_PATH: ["Objective and Authority", "Cumulative Step Range", "Exact Inputs and Actual Read Coverage", "Files Created and Updated", "Commands and Execution Evidence", "Validation", "Exclusive Gate", "Confirmed", "Unverified", "Ground Not Found", "Unresolved and Decision Queue", "Protected Non-changes", "Exact Phase 061 Entry Condition"],
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
    combined_reports = "\n".join(texts[path] for path in [REPORT_PATH, GATE_RESULT_PATH, PHASE_RESULT_PATH])
    required_tokens = [
        "77/77", "2/2", "61/61", "9,904/9,904", "9,145/9,145", "3/3", "95/95",
        "13/13", "14/14", "1/1", "173/173", "52/52", "PASS_P060_LINEAGE_C",
        STEP45_BASELINE, "primary literature", "canonical", "final LaTeX/PDF",
        "Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md",
    ]
    for token in required_tokens:
        require(token in combined_reports, f"final reports missing required token: {token}")
    controls = texts[PARENT_LEDGER_PATH] + "\n" + texts[ACTIVE_LEDGER_PATH] + "\n" + texts[HANDOVER_PATH]
    require("pending controller" not in controls, "stale Step45.1 pending-controller pointer")
    require(STEP45_BASELINE in controls, "Step45.1 containing commit absent from controls")
    require("PASS_P060_LINEAGE_C" in controls, "final gate absent from controls")
    require("Phase 061" in controls and "detailed plan" in controls and "Step 46" in controls, "exact Phase061 entry condition absent")
    return {
        "exact_final_paths": FINAL_PATHS, "hashed_nonself_records": records,
        "hashed_nonself_count": 7, "human_required_sections": required_sections,
        "stale_step45_pending_pointer_count": 0, "phase061_plan_before_step46_required": True,
    }


def build_document() -> dict[str, Any]:
    repo = repository_state()
    objects, machine = machine_inventory()
    counts = integrated_counts(objects)
    steps = step_commit_inventory(repo["head"])
    subordinates = fresh_subordinate_validation()
    fixtures = fixture_validation()
    outputs = final_output_inventory()
    document = {
        "schema_version": "phase060-final-v1", "generated_date": "2026-08-26",
        "phase": 60, "step": "45.2", "branch": BRANCH,
        "source_commit": SOURCE_COMMIT, "step45_baseline": STEP45_BASELINE,
        "scope": "Phase 060 Step 45.2 integrated v1.0.19 lineage validation and final gate",
        "authority_boundary": AUTHORITY_BOUNDARY, "repository_state": repo,
        "machine_artifact_inventory": machine, "integrated_counts": counts,
        "step_commit_inventory": {"count": 7, "records": steps, "all_in_origin_active_ancestry": True, "all_exact_atomic": True},
        "fresh_subordinate_validation": subordinates, "repository_fixtures": fixtures,
        "final_output_contract": outputs,
        "gate": {
            "exclusive_decision": "PASS_P060_LINEAGE_C", "status": "PASS",
            "audit_requirements_complete": True, "external_scientific_truth_validated": False,
            "external_material_truth_validated": False, "experimental_validity_established": False,
            "canonical_model_selected": False, "defect_repairs_claimed": 0,
            "inherited_open_items": 52, "new_open_blockers": 5,
            "next": "Create, review, validate, atomically commit, push and remote-verify the Phase 061 detailed plan before Step 46.",
        },
        "determinism": {
            "encoding": "UTF-8", "line_endings": "LF", "json_key_order": "sorted",
            "strict_duplicate_key_parse": True, "nonfinite_rejected": True,
            "runtime_seconds_masked_in_projection": True,
            "python_executable_masked_in_projection": True,
            "raw_stdout_bytes_and_sha_masked_in_projection": True,
            "stdout_lf_sha256_retained_in_projection": True,
            "operational_commit_refs_masked_in_projection": True,
            "fresh_reconstruction_required_each_run": True,
        },
    }
    document["semantic_sha256"] = semantic_hash(document)
    return document


def deterministic_projection(document: Any, label: str) -> dict[str, Any]:
    require(type(document) is dict, f"{label}: top-level object required")
    clone = copy.deepcopy(document)
    clone.pop("semantic_sha256", None)
    records = clone.get("fresh_subordinate_validation", {}).get("records")
    require(type(records) is list, f"{label}: subordinate records list required")
    for row in records:
        runtime = row.get("runtime_seconds")
        require(type(runtime) in {int, float} and type(runtime) is not bool and runtime >= 0, f"{label}: subordinate runtime type")
        row["runtime_seconds"] = "<RUNTIME_SECONDS_MASKED>"
        require(type(row.get("argv")) is list and row["argv"], f"{label}: subordinate argv")
        row["argv"][0] = "<PYTHON_EXECUTABLE_MASKED>"
        row["stdout_bytes"] = "<RAW_STDOUT_BYTES_MASKED>"
        row["stdout_sha256"] = "<RAW_STDOUT_SHA256_MASKED>"
    clone["fresh_subordinate_validation"]["clone_head"] = "<OPERATIONAL_COMMIT_MASKED>"
    fixture = clone.get("repository_fixtures", {})
    require(type(fixture) is dict, f"{label}: fixture object required")
    require(type(fixture.get("fixture_commit")) is str and re.fullmatch(r"[0-9a-f]{40}", fixture["fixture_commit"]) is not None, f"{label}: fixture commit format")
    fixture["fixture_commit"] = "<FIXTURE_COMMIT_MASKED>"
    state = clone.get("repository_state", {})
    for key in ["head", "upstream", "origin_active", "live_remote"]:
        require(type(state.get(key)) is str and re.fullmatch(r"[0-9a-f]{40}", state[key]) is not None, f"{label}: repository {key}")
        state[key] = "<OPERATIONAL_COMMIT_MASKED>"
    return clone


def validate_diagnostic_contracts(document: dict[str, Any], expected: dict[str, Any]) -> None:
    getters: list[tuple[str, Callable[[dict[str, Any]], Any]]] = [
        ("E_PRIMARY_PATH_COUNT", lambda d: d["integrated_counts"]["primary"]["paths"]),
        ("E_WITNESS_COUNT", lambda d: d["integrated_counts"]["witness"]["occurrences"]),
        ("E_TEXT_PHYSICAL_COUNT", lambda d: d["integrated_counts"]["inspection"]["physical_lines"]),
        ("E_PDF_PAGE_COUNT", lambda d: d["integrated_counts"]["inspection"]["pdf_pages"]),
        ("E_IMAGE_OCCURRENCE_COUNT", lambda d: d["integrated_counts"]["inspection"]["image_occurrences"]),
        ("E_MACHINE_RECORD_COUNT", lambda d: len(d["machine_artifact_inventory"]["records"])),
        ("E_MACHINE_SHA", lambda d: [row["sha256"] for row in d["machine_artifact_inventory"]["records"]]),
        ("E_MACHINE_NODES", lambda d: [row["total_nodes"] for row in d["machine_artifact_inventory"]["records"]]),
        ("E_STEP_RECORD_COUNT", lambda d: len(d["step_commit_inventory"]["records"])),
        ("E_STEP_COMMIT_SHA", lambda d: [row["commit"] for row in d["step_commit_inventory"]["records"]]),
        ("E_STEP_COMMIT_PATHS", lambda d: [row["paths"] for row in d["step_commit_inventory"]["records"]]),
        ("E_STEP_REMOTE_ANCESTRY", lambda d: [row["in_origin_active_ancestry"] for row in d["step_commit_inventory"]["records"]]),
        ("E_SUBORDINATE_COUNT", lambda d: len(d["fresh_subordinate_validation"]["records"])),
        ("E_SUBORDINATE_EXIT", lambda d: [row["exit_code"] for row in d["fresh_subordinate_validation"]["records"]]),
        ("E_SUBORDINATE_TERMINAL", lambda d: [row["terminal"] for row in d["fresh_subordinate_validation"]["records"]]),
        ("E_SUBORDINATE_STDERR", lambda d: [row["stderr_bytes"] for row in d["fresh_subordinate_validation"]["records"]]),
        ("E_CLEAN_FIXTURE", lambda d: d["repository_fixtures"]["clean_descendant_pass"]),
        ("E_TRACKED_FIXTURE", lambda d: d["repository_fixtures"]["dirty_tracked_rejected"]),
        ("E_UNTRACKED_FIXTURE", lambda d: d["repository_fixtures"]["dirty_untracked_rejected"]),
        ("E_FIXTURE_PATHS", lambda d: d["repository_fixtures"]["exact_paths"]),
        ("E_FINAL_OUTPUT_HASH", lambda d: [row["sha256"] for row in d["final_output_contract"]["hashed_nonself_records"]]),
        ("E_FINAL_OUTPUT_PATHS", lambda d: d["final_output_contract"]["exact_final_paths"]),
        ("E_STALE_POINTER", lambda d: d["final_output_contract"]["stale_step45_pending_pointer_count"]),
        ("E_EXTERNAL_TRUTH", lambda d: d["gate"]["external_scientific_truth_validated"]),
        ("E_MATERIAL_TRUTH", lambda d: d["gate"]["external_material_truth_validated"]),
        ("E_CANONICAL_SELECTION", lambda d: d["gate"]["canonical_model_selected"]),
        ("E_OPEN_ITEM_PRESERVATION", lambda d: d["gate"]["inherited_open_items"]),
        ("E_EXCLUSIVE_GATE", lambda d: d["gate"]["exclusive_decision"]),
        ("E_TOP_LEVEL_SCHEMA", lambda d: sorted(d)),
        ("E_GATE_SCHEMA", lambda d: sorted(d["gate"])),
        ("E_PHASE_TYPE", lambda d: {"type": type(d["phase"]).__name__, "value": d["phase"]}),
        ("E_SOURCE_COMMIT", lambda d: d["source_commit"]),
        ("E_BASELINE_COMMIT", lambda d: d["step45_baseline"]),
        ("E_AUTHORITY_BOUNDARY", lambda d: d["authority_boundary"]),
    ]
    for code, getter in getters:
        try:
            actual_value = getter(document)
            expected_value = getter(expected)
        except (KeyError, IndexError, TypeError) as exc:
            raise ValidationFailure(f"{code}: contract path failure: {exc}") from exc
        if canonical_bytes(actual_value) != canonical_bytes(expected_value):
            raise ValidationFailure(f"{code}: contract mismatch")


def validate_document(document: Any, expected: dict[str, Any]) -> None:
    require(type(document) is dict, "artifact top-level type")
    require(type(document.get("semantic_sha256")) is str and len(document["semantic_sha256"]) == 64, "semantic SHA type")
    require(document["semantic_sha256"] == semantic_hash(document), "semantic SHA mismatch")
    validate_diagnostic_contracts(document, expected)
    exact(deterministic_projection(document, "actual"), deterministic_projection(expected, "expected"), "full deterministic projection")
    require(document["gate"]["exclusive_decision"] == "PASS_P060_LINEAGE_C", "exclusive gate decision")
    require(document["gate"]["external_scientific_truth_validated"] is False, "external truth promotion")
    require(document["gate"]["external_material_truth_validated"] is False, "material truth promotion")
    require(document["gate"]["canonical_model_selected"] is False, "canonical selection promotion")
    require(document["gate"]["inherited_open_items"] == 52 and document["gate"]["new_open_blockers"] == 5, "open-item preservation")
    require(document["machine_artifact_inventory"]["count"] == 9, "machine artifact count")
    require(document["fresh_subordinate_validation"]["count"] == document["fresh_subordinate_validation"]["pass_count"] == 6, "subordinate PASS count")
    require(document["step_commit_inventory"]["count"] == 7, "step commit count")
    require(document["repository_fixtures"]["clean_descendant_pass"] is True, "clean descendant fixture")
    require(document["repository_fixtures"]["dirty_tracked_rejected"] is True, "dirty tracked fixture")
    require(document["repository_fixtures"]["dirty_untracked_rejected"] is True, "dirty untracked fixture")


def negative_probes(document: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    probes: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = []
    def add(name: str, code: str, fn: Callable[[dict[str, Any]], None]) -> None:
        probes.append((name, code, fn))
    add("primary_path_count", "E_PRIMARY_PATH_COUNT", lambda d: d["integrated_counts"]["primary"].__setitem__("paths", 76))
    add("witness_count", "E_WITNESS_COUNT", lambda d: d["integrated_counts"]["witness"].__setitem__("occurrences", 1))
    add("text_physical_count", "E_TEXT_PHYSICAL_COUNT", lambda d: d["integrated_counts"]["inspection"].__setitem__("physical_lines", 9903))
    add("pdf_page_count", "E_PDF_PAGE_COUNT", lambda d: d["integrated_counts"]["inspection"].__setitem__("pdf_pages", 94))
    add("image_occurrence_count", "E_IMAGE_OCCURRENCE_COUNT", lambda d: d["integrated_counts"]["inspection"].__setitem__("image_occurrences", 13))
    add("drop_machine_artifact", "E_MACHINE_RECORD_COUNT", lambda d: d["machine_artifact_inventory"]["records"].pop())
    add("machine_sha", "E_MACHINE_SHA", lambda d: d["machine_artifact_inventory"]["records"][0].__setitem__("sha256", "0" * 64))
    add("machine_nodes", "E_MACHINE_NODES", lambda d: d["machine_artifact_inventory"]["records"][0].__setitem__("total_nodes", 0))
    add("drop_step_commit", "E_STEP_RECORD_COUNT", lambda d: d["step_commit_inventory"]["records"].pop())
    add("step_commit_sha", "E_STEP_COMMIT_SHA", lambda d: d["step_commit_inventory"]["records"][0].__setitem__("commit", "0" * 40))
    add("step_commit_path", "E_STEP_COMMIT_PATHS", lambda d: d["step_commit_inventory"]["records"][0]["paths"].pop())
    add("step_commit_ancestry", "E_STEP_REMOTE_ANCESTRY", lambda d: d["step_commit_inventory"]["records"][0].__setitem__("in_origin_active_ancestry", False))
    add("drop_subordinate", "E_SUBORDINATE_COUNT", lambda d: d["fresh_subordinate_validation"]["records"].pop())
    add("subordinate_exit", "E_SUBORDINATE_EXIT", lambda d: d["fresh_subordinate_validation"]["records"][0].__setitem__("exit_code", 1))
    add("subordinate_terminal", "E_SUBORDINATE_TERMINAL", lambda d: d["fresh_subordinate_validation"]["records"][0].__setitem__("terminal", "PASS_FAKE"))
    add("subordinate_stderr", "E_SUBORDINATE_STDERR", lambda d: d["fresh_subordinate_validation"]["records"][0].__setitem__("stderr_bytes", 1))
    add("clean_fixture", "E_CLEAN_FIXTURE", lambda d: d["repository_fixtures"].__setitem__("clean_descendant_pass", False))
    add("tracked_fixture", "E_TRACKED_FIXTURE", lambda d: d["repository_fixtures"].__setitem__("dirty_tracked_rejected", False))
    add("untracked_fixture", "E_UNTRACKED_FIXTURE", lambda d: d["repository_fixtures"].__setitem__("dirty_untracked_rejected", False))
    add("fixture_path", "E_FIXTURE_PATHS", lambda d: d["repository_fixtures"]["exact_paths"].pop())
    add("final_output_hash", "E_FINAL_OUTPUT_HASH", lambda d: d["final_output_contract"]["hashed_nonself_records"][0].__setitem__("sha256", "0" * 64))
    add("final_output_path", "E_FINAL_OUTPUT_PATHS", lambda d: d["final_output_contract"]["exact_final_paths"].pop())
    add("stale_pointer", "E_STALE_POINTER", lambda d: d["final_output_contract"].__setitem__("stale_step45_pending_pointer_count", 1))
    add("false_external_truth", "E_EXTERNAL_TRUTH", lambda d: d["gate"].__setitem__("external_scientific_truth_validated", True))
    add("false_material_truth", "E_MATERIAL_TRUTH", lambda d: d["gate"].__setitem__("external_material_truth_validated", True))
    add("false_canonical", "E_CANONICAL_SELECTION", lambda d: d["gate"].__setitem__("canonical_model_selected", True))
    add("false_resolution", "E_OPEN_ITEM_PRESERVATION", lambda d: d["gate"].__setitem__("inherited_open_items", 0))
    add("wrong_gate", "E_EXCLUSIVE_GATE", lambda d: d["gate"].__setitem__("exclusive_decision", "CONDITIONAL_P060"))
    add("unknown_top_key", "E_TOP_LEVEL_SCHEMA", lambda d: d.__setitem__("ESTABLISHED", True))
    add("unknown_nested_key", "E_GATE_SCHEMA", lambda d: d["gate"].__setitem__("ESTABLISHED", True))
    add("bool_int_confusion", "E_PHASE_TYPE", lambda d: d.__setitem__("phase", True))
    add("source_commit", "E_SOURCE_COMMIT", lambda d: d.__setitem__("source_commit", "0" * 40))
    add("baseline_commit", "E_BASELINE_COMMIT", lambda d: d.__setitem__("step45_baseline", "0" * 40))
    add("authority_reversal", "E_AUTHORITY_BOUNDARY", lambda d: d.__setitem__("authority_boundary", "PASS proves external truth"))
    rejected: list[str] = []
    for name, expected_code, mutation in probes:
        candidate = copy.deepcopy(document)
        mutation(candidate)
        candidate["semantic_sha256"] = semantic_hash(candidate)
        try:
            validate_document(candidate, expected)
        except ValidationFailure as exc:
            require(str(exc).startswith(f"{expected_code}:"),
                    f"E_NEGATIVE_DIAGNOSTIC: {name} expected {expected_code}, got {exc}")
            rejected.append(name)
        else:
            raise ValidationFailure(f"negative probe unexpectedly accepted: {name}")
    duplicate_raw = pretty_bytes(document).replace(b'"schema_version": "phase060-final-v1",', b'"schema_version": "phase060-final-v1",\n  "schema_version": "phase060-final-v1",', 1)
    try:
        strict_bytes(duplicate_raw, "duplicate_key_fixture")
    except ValidationFailure as exc:
        require(str(exc).startswith("E_DUPLICATE_JSON:"), f"E_NEGATIVE_DIAGNOSTIC: duplicate fixture got {exc}")
        rejected.append("duplicate_json_key")
    else:
        raise ValidationFailure("duplicate JSON key fixture accepted")
    nonfinite_raw = pretty_bytes(document).replace(b'"phase": 60', b'"phase": NaN', 1)
    try:
        strict_bytes(nonfinite_raw, "nonfinite_fixture")
    except ValidationFailure as exc:
        require(str(exc).startswith("E_NONFINITE_JSON:"), f"E_NEGATIVE_DIAGNOSTIC: nonfinite fixture got {exc}")
        rejected.append("nonfinite_json")
    else:
        raise ValidationFailure("non-finite JSON fixture accepted")
    return rejected


def verify_persistence() -> None:
    state = repository_state()
    head = state["head"]
    require(head != STEP45_BASELINE, "Step45.2 persistence commit absent")
    require(git_text("rev-parse", "HEAD^") == STEP45_BASELINE, "Step45.2 parent mismatch")
    require(git_text("show", "-s", "--format=%s", "HEAD") == FINAL_SUBJECT, "Step45.2 subject mismatch")
    changed = git(["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"]).stdout.decode("utf-8").splitlines()
    require(set(changed) == FINAL_PATH_SET and len(changed) == 8, "Step45.2 exact-eight mismatch")
    require(active_status_paths() == [], "postcommit worktree not clean")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--verify-fixture", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.verify_persistence:
            verify_persistence()
            print("PASS_P060_STEP45_2_PERSISTENCE")
            return 0
        if args.verify_fixture:
            verify_fixture_persistence()
            print("PASS_P060_STEP45_2_FIXTURE")
            return 0
        if args.collect:
            require(not ARTIFACT.exists(), "--collect refuses to overwrite existing artifact")
            expected = build_document()
            validate_document(expected, expected)
            ARTIFACT.write_bytes(pretty_bytes(expected))
            document = expected
        else:
            require(ARTIFACT.is_file(), f"missing artifact: {ARTIFACT_PATH}")
            document = strict_bytes(ARTIFACT.read_bytes(), ARTIFACT_PATH)
            expected = build_document()
            validate_document(document, expected)
        if args.determinism_check:
            second = build_document()
            exact(deterministic_projection(expected, "determinism-first"), deterministic_projection(second, "determinism-second"), "deterministic independent reconstruction 2/2")
            print("PASS determinism=2/2 runtime_seconds_masked=true")
        if args.run_negative_probes:
            rejected = negative_probes(document, expected)
            print(f"PASS negative_controls={len(rejected)}/{len(rejected)}")
        print("PASS coverage primary=77/77 witness=2/2 text=61/61 lines=9904/9904 nonblank=9145/9145")
        print("PASS artifacts pdf=3/3 pages=95/95 images_unique=13/13 occurrences=14/14 binary=1/1")
        print("PASS lineage steps=7/7 subordinates=6/6 dispositions=173/173 carry=52/52 blockers=5")
        print("PASS authority external_scientific=false external_material=false canonical=false")
        print("PASS repository clean_descendant=true dirty_tracked_rejected=true dirty_untracked_rejected=true")
        print("PASS_P060_LINEAGE_C")
        return 0
    except ValidationFailure as exc:
        print(f"FAIL_P060_LINEAGE_C: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
