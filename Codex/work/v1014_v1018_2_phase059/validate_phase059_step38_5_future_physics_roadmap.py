#!/usr/bin/env python3
"""Validate the Phase 059 Step 38.5 future-physics roadmap disposition."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_PATH = ROOT / "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json"
ROADMAP_PATH = "Claude/docs/v1.0.18.2/ROADMAP_future_physics.md"
EXPECTED_BASELINE_COMMIT = "1cf955ba347218676a73bdae0a9eb8add8e1581a"
EXPECTED_ROADMAP_SHA256 = "fedde051b920af1550e0408b744ca8daf98a01d058aab5341a930d9a9abdc39e"
EXPECTED_INPUT_LINES = 15623
EXPECTED_SEMANTIC_SHA256 = "1deeee80c3f0a439b0cd2cd24c8484bfa8fc60c25619977357d192af5f3a1794"
EXPECTED_INPUT_PATHS = [
    ROADMAP_PATH,
    "Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md",
    "Claude/docs/v1.0.18.2/FITTING_GUIDE.md",
    "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py",
    "Claude/docs/v1.0.18.2/test_regression_graphite.py",
    "Claude/docs/v1.0.18.2/sample_test_v1018_2.py",
    "Claude/docs/v1.0.18.2/graph_suite_v1018_2.py",
    "Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md",
    "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md",
    "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json",
    "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md",
    "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json",
    "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md",
    "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json",
    "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md",
    "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json",
    "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md",
    "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md",
    "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json",
    "Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md",
]
TOPIC_ENUM = {"interaction", "phase_field", "kinetics", "transport", "particle_size", "data", "other"}
EXPECTED_ITEM_CONTRACTS = {
    "P059-RM-001": {"source_lines": "3, 10", "topic": "other", "atomic_topic": "einstein_vibration", "primary_classification": "IMPLEMENTED"},
    "P059-RM-002": {"source_lines": "18-23", "topic": "interaction", "atomic_topic": "interaction_composition", "primary_classification": "NEW_SCOPE"},
    "P059-RM-003": {"source_lines": "25-29", "topic": "phase_field", "atomic_topic": "phase_field_hysteresis", "primary_classification": "THEORY_ONLY"},
    "P059-RM-004": {"source_lines": "31-35", "topic": "transport", "atomic_topic": "kinetics_transport", "primary_classification": "NEW_SCOPE"},
    "P059-RM-005": {"source_lines": "37-41", "topic": "particle_size", "atomic_topic": "particle_size", "primary_classification": "NEW_SCOPE"},
    "P059-RM-006": {"source_lines": "46", "topic": "data", "atomic_topic": "n_of_T_diagnostic", "primary_classification": "NEW_SCOPE"},
    "P059-RM-007": {"source_lines": "46", "topic": "data", "atomic_topic": "two_phase_width_temperature", "primary_classification": "NEW_SCOPE"},
    "P059-RM-008": {"source_lines": "47", "topic": "data", "atomic_topic": "lco_omega_dha", "primary_classification": "NEW_SCOPE"},
    "P059-RM-009": {"source_lines": "47", "topic": "data", "atomic_topic": "lco_electronic_temperature", "primary_classification": "NEW_SCOPE"},
    "P059-RM-010": {"source_lines": "47", "topic": "data", "atomic_topic": "lco_composition_gate", "primary_classification": "NEW_SCOPE"},
    "P059-RM-011": {"source_lines": "48", "topic": "other", "atomic_topic": "bibliography", "primary_classification": "NEW_SCOPE"},
    "P059-RM-012": {"source_lines": "49", "topic": "data", "atomic_topic": "joint_identifiability", "primary_classification": "NEW_SCOPE"},
}
EXPECTED_ITEM_IDS = list(EXPECTED_ITEM_CONTRACTS)
PRIMARY_CLASSIFICATIONS = {"IMPLEMENTED", "THEORY_ONLY", "NEW_SCOPE"}
REQUIRED_ITEM_FIELDS = {
    "item_id",
    "source_path",
    "source_lines",
    "source_text",
    "topic",
    "atomic_topic",
    "primary_classification",
    "secondary_status",
    "theory_evidence",
    "code_evidence",
    "test_evidence",
    "artifact_evidence",
    "data_prerequisites",
    "literature_prerequisites",
    "acceptance_criterion",
    "authority_boundary",
}
EVIDENCE_FIELDS = ("theory_evidence", "code_evidence", "test_evidence", "artifact_evidence")


class ValidationFailure(Exception):
    """Raised when a validation invariant is not satisfied."""


def git_blob_bytes(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise ValidationFailure(
            f"cannot read Git blob for {path}: {completed.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return completed.stdout


def source_lines(path: str) -> list[str]:
    return git_blob_bytes(path).decode("utf-8").splitlines()


def selected_source_text(lines: list[str], specification: str) -> str:
    selected: list[str] = []
    for segment in [part.strip() for part in specification.split(",")]:
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", segment)
        if not match:
            raise ValidationFailure(f"invalid source_lines specification: {specification!r}")
        start = int(match.group(1))
        end = int(match.group(2) or start)
        if start < 1 or end < start or end > len(lines):
            raise ValidationFailure(
                f"source_lines {specification!r} falls outside 1-{len(lines)}"
            )
        selected.extend(lines[start - 1 : end])
    return "\n".join(selected)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def validate_evidence(item_id: str, field: str, entries: Any) -> None:
    require(isinstance(entries, list) and entries, f"{item_id}.{field} must be a non-empty list")
    for index, entry in enumerate(entries):
        require(isinstance(entry, dict), f"{item_id}.{field}[{index}] must be an object")
        path = entry.get("path")
        require(isinstance(path, str) and path.strip(), f"{item_id}.{field}[{index}] missing path")
        require("\\" not in path, f"{item_id}.{field}[{index}] path is not POSIX: {path}")
        require((ROOT / path).exists(), f"{item_id}.{field}[{index}] path does not exist: {path}")
        require(
            isinstance(entry.get("anchor"), str) and entry["anchor"].strip(),
            f"{item_id}.{field}[{index}] missing exact anchor",
        )
        require(
            isinstance(entry.get("finding"), str) and entry["finding"].strip(),
            f"{item_id}.{field}[{index}] missing finding",
        )


def validate() -> None:
    require(ARTIFACT_PATH.exists(), f"missing artifact: {ARTIFACT_PATH.relative_to(ROOT).as_posix()}")
    try:
        artifact = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"artifact is not valid UTF-8 JSON: {exc}") from exc

    require(artifact.get("schema_version") == 1, "schema_version must be 1")
    require(artifact.get("step") == "38.5", "step must be 38.5")
    require(artifact.get("baseline_commit") == EXPECTED_BASELINE_COMMIT, "baseline_commit mismatch")
    require(
        artifact.get("status") == "PASS_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION",
        "unexpected status banner",
    )
    require(isinstance(artifact.get("rules_and_definitions"), dict), "rules_and_definitions missing")
    require(isinstance(artifact.get("unresolved_items"), list), "unresolved_items must be a list")
    require(isinstance(artifact.get("validator_summary"), dict), "validator_summary missing")

    coverage = artifact.get("input_coverage")
    require(isinstance(coverage, list) and coverage, "input_coverage must be a non-empty list")
    coverage_paths: list[str] = []
    for entry in coverage:
        require(isinstance(entry, dict), "each input_coverage entry must be an object")
        path = entry.get("path")
        require(isinstance(path, str) and path, "input coverage path missing")
        require("\\" not in path, f"input coverage path is not POSIX: {path}")
        require(path not in coverage_paths, f"duplicate input coverage path: {path}")
        coverage_paths.append(path)
        blob = git_blob_bytes(path)
        lines = blob.decode("utf-8").splitlines()
        require(entry.get("line_count") == len(lines), f"line count mismatch for {path}")
        require(entry.get("read_range") == f"1-{len(lines)}", f"read range mismatch for {path}")
        require(entry.get("full_read") is True, f"full_read must be true for {path}")
        require(entry.get("hash_basis") == "Git blob bytes at HEAD", f"hash_basis mismatch for {path}")
        require(
            entry.get("git_blob_sha256") == hashlib.sha256(blob).hexdigest(),
            f"Git blob SHA-256 mismatch for {path}",
        )

    require(coverage_paths == EXPECTED_INPUT_PATHS, "input coverage ordered path contract mismatch")
    roadmap = source_lines(ROADMAP_PATH)
    require(len(roadmap) == 49, f"roadmap must contain 49 Git-blob lines, got {len(roadmap)}")
    roadmap_coverage = coverage[0]
    require(roadmap_coverage["git_blob_sha256"] == EXPECTED_ROADMAP_SHA256, "roadmap frozen SHA-256 mismatch")

    items = artifact.get("items")
    require(isinstance(items, list), "items must be a list")
    require(len(items) == len(EXPECTED_ITEM_IDS), f"expected 12 items, got {len(items)}")
    require([item.get("item_id") for item in items] == EXPECTED_ITEM_IDS, "item IDs/order mismatch")

    for item in items:
        item_id = item.get("item_id", "<unknown>")
        missing = REQUIRED_ITEM_FIELDS.difference(item)
        require(not missing, f"{item_id} missing fields: {sorted(missing)}")
        require(item["source_path"] == ROADMAP_PATH, f"{item_id} source_path mismatch")
        contract = EXPECTED_ITEM_CONTRACTS[item_id]
        require(item["source_lines"] == contract["source_lines"], f"{item_id} source_lines contract mismatch")
        require(item["topic"] in TOPIC_ENUM, f"{item_id} topic is outside plan enum")
        require(item["topic"] == contract["topic"], f"{item_id} topic contract mismatch")
        require(item["atomic_topic"] == contract["atomic_topic"], f"{item_id} atomic_topic contract mismatch")
        require(item["primary_classification"] in PRIMARY_CLASSIFICATIONS, f"{item_id} invalid primary classification")
        require(item["primary_classification"] == contract["primary_classification"], f"{item_id} primary classification contract mismatch")
        require(isinstance(item["secondary_status"], list) and item["secondary_status"], f"{item_id} secondary_status must be non-empty")
        for field in ("secondary_status", "data_prerequisites", "literature_prerequisites"):
            require(
                isinstance(item[field], list) and item[field],
                f"{item_id}.{field} must be a non-empty list",
            )
            require(
                all(isinstance(value, str) and value.strip() for value in item[field]),
                f"{item_id}.{field} must contain only nonblank strings",
            )
        expected_text = selected_source_text(roadmap, item["source_lines"])
        require(item["source_text"] == expected_text, f"{item_id} source text mismatch")
        for field in EVIDENCE_FIELDS:
            validate_evidence(item_id, field, item[field])
        require(
            isinstance(item["acceptance_criterion"], str) and item["acceptance_criterion"].strip(),
            f"{item_id} acceptance criterion missing",
        )
        require(
            isinstance(item["authority_boundary"], str) and item["authority_boundary"].strip(),
            f"{item_id} authority boundary missing",
        )

    counts = artifact.get("counts")
    require(isinstance(counts, dict), "counts missing")
    require(counts.get("total_items") == 12, "counts.total_items mismatch")
    require(counts.get("input_files") == 26, "counts.input_files mismatch")
    require(counts.get("input_lines") == EXPECTED_INPUT_LINES, "counts.input_lines mismatch")
    require(sum(entry["line_count"] for entry in coverage) == EXPECTED_INPUT_LINES, "recomputed input line total mismatch")
    observed = {name: 0 for name in sorted(PRIMARY_CLASSIFICATIONS)}
    for item in items:
        observed[item["primary_classification"]] += 1
    require(counts.get("primary_classifications") == observed, "primary classification counts mismatch")

    semantic_hash = artifact.get("determinism", {}).get("semantic_sha256")
    require(isinstance(semantic_hash, str) and re.fullmatch(r"[0-9a-f]{64}", semantic_hash) is not None,
            "determinism.semantic_sha256 must be a lowercase SHA-256")
    semantic_copy = json.loads(json.dumps(artifact))
    semantic_copy["determinism"]["semantic_sha256"] = ""
    canonical = json.dumps(semantic_copy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(canonical).hexdigest() == semantic_hash, "semantic SHA-256 mismatch")
    require(semantic_hash == EXPECTED_SEMANTIC_SHA256, "canonical semantic SHA-256 lock mismatch")


def main() -> int:
    try:
        validate()
    except ValidationFailure as exc:
        print(f"FAIL_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION: {exc}", file=sys.stderr)
        return 1
    print("PASS_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
