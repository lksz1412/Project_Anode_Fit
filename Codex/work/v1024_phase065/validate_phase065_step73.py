#!/usr/bin/env python3
"""Validate Phase 065 Step 73 content, transaction, and persistence."""

from __future__ import annotations

import argparse
import ast
import copy
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "272b8d331c55448182e96c75363a56061adf58f2"
EXPECTED_SUBJECT = "audit(phase065): separate v1024 initialization routes"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_UPSTREAM = f"origin/{BRANCH}"
MATRIX_PATH = ROOT / "Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json"
RUNTIME_PATH = ROOT / "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json"
BUILDER_PATH = ROOT / "Codex/work/v1024_phase065/build_phase065_step73.py"
STEP71_PATH = ROOT / "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"
PASS_CONTENT = "PASS_P065_STEP73_CONTENT"
PASS_PERSISTENCE = "PASS_P065_STEP73_PERSISTENCE"
EXACT_PATHS = sorted([
    "Codex/work/v1024_phase065/build_phase065_step73.py",
    "Codex/work/v1024_phase065/validate_phase065_step73.py",
    "Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json",
    "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
])
CONTROL_ROLES = {
    "Codex/work/v1024_phase065/build_phase065_step73.py": "EVIDENCE_BUILDER",
    "Codex/work/v1024_phase065/validate_phase065_step73.py": "INDEPENDENT_VALIDATOR",
    "Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md": "RESULT_FIRST_RECORD",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md": "PARENT_EXECUTION_LEDGER",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md": "CANONICAL_EXECUTION_LEDGER",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": "ACTIVE_HANDOVER",
}
RUNTIME_SOURCES = (
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
    "Claude/docs/v1.0.19/golden_graphite_ref.npz",
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.23/test_gates_v1023.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
    "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py",
    "Claude/docs/v1.0.24/test_gates_v1024.py",
    "Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py",
    "Claude/docs/v1.0.24/test_gates_v1024_reflect.py",
)
RUNTIME_IDENTITY_CODE = "import sys,numpy;print(sys.version.split()[0]);print(numpy.__version__)"
OUTCOMES = ["IMPLEMENTED_AND_OBSERVED", "ABSENT_IN_FROZEN_SOURCE", "GROUND_NOT_FOUND"]
RESULT_FIRST_CONTRACT = {
    "gate": "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS",
    "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
    "postcommit_terminal": "PENDING_AT_PRECOMMIT_BY_DESIGN",
}
EXPECTED_BUILDER_CANONICAL_AST = {
    (3, 12): "5e716543ea0eaea3059dbc96d524569f8a7465b4bb947b2e16cb3d3dbaa0998b",
    (3, 14): "c23fbd2c61d8949a96a9ad81f4ae1cfa957101f6057af8ac7048c3fd850ced7b",
}
EXPECTED_PROBE_CANONICAL_AST = {
    (3, 12): "623f4c5609893a7c13710d15764dad1740db4d197a9ee3dc0fd11d7948191850",
    (3, 14): "919463f87a4323fcfe84ec637fe6e110744875ae3fb97b80f6546de07c77498a",
}
EXPECTED_MATRIX_SCHEMA_SHA256 = "6fe09b83333e75441fc7ae6e3c0986619ede5054ce9f79f69f5535a8c4bd94aa"
EXPECTED_RUNTIME_SCHEMA_SHA256 = "4635d7082a2c4c336ceca618ea5bbd9ca202460bb31f6dc8a301093182e9904b"
EXPECTED_ROUTE_OBSERVATION_SHA256 = {
    "fresh": "a42ee02e7ee145887918968dd871458b7580df983f0e53f194bcb7cc931e8180",
    "explicit": "e22eaeba2e9f353d417bafbece7fae2628a6a9543932cbc7b91d0ce626e939d1",
    "legacy": "a2b2b40f93654925e5cf003393886bc72441b47670805c8f7dbf1b81ce52417b",
    "mutation": "d01074c4398e8c59c3134e22263da676ca031fd1f543824c8e536202f9ddb6be",
}
EXPECTED_OFFICIAL_STDOUT_SHA256 = {
    ("3.12", "v1023-main"): "615e368c8b62437c2f65e2553d633274aaf836db608e8738125cfa41cbc0d12a",
    ("3.12", "v1023-selfconsistent"): "f4a6a30568b6666bfcc895079e4b3449c4519e33fc1a6d4295323f40e5fac5b1",
    ("3.12", "v1024-main"): "7aaab130a2a0639e0567c8793281c2fcc5d934ab03afbba0908e6e8c8c87adf5",
    ("3.12", "v1024-selfconsistent"): "f4a6a30568b6666bfcc895079e4b3449c4519e33fc1a6d4295323f40e5fac5b1",
    ("3.12", "v1024-reflect"): "f755d6ae1ac2cb920a282d85c92154da6ec572fbae3609f021a6cf0288297582",
    ("3.14", "v1023-main"): "a788336181e7c964d80ae3b7d9c3e52f4e0c46743fdc52d4eac41be5897f475b",
    ("3.14", "v1023-selfconsistent"): "f4a6a30568b6666bfcc895079e4b3449c4519e33fc1a6d4295323f40e5fac5b1",
    ("3.14", "v1024-main"): "14ca65bd00caf5d60ef83cd8648997ab61d1ab5cdaed9245a35f590d03d25b48",
    ("3.14", "v1024-selfconsistent"): "f4a6a30568b6666bfcc895079e4b3449c4519e33fc1a6d4295323f40e5fac5b1",
    ("3.14", "v1024-reflect"): "f755d6ae1ac2cb920a282d85c92154da6ec572fbae3609f021a6cf0288297582",
}


class ValidationError(RuntimeError):
    pass


def fail(code: str, detail: str = "") -> None:
    raise ValidationError(code + (f": {detail}" if detail else ""))


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        fail(code, detail)


def run(args: list[str] | tuple[str, ...], *, cwd: Path = ROOT,
        timeout: int = 900, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(list(args), cwd=cwd, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, timeout=timeout, check=False)
    if check and cp.returncode != 0:
        fail("E_COMMAND", f"{args!r}\n{cp.stdout.decode('utf-8','replace')}\n{cp.stderr.decode('utf-8','replace')}")
    return cp


@lru_cache(maxsize=None)
def live_runtime_identity(runtime_id: str) -> tuple[str, str]:
    require(runtime_id in {"3.12", "3.14"}, "E_RUNTIME_IDENTITY_RUNTIME", runtime_id)
    cp = run(("py", f"-{runtime_id}", "-B", "-I", "-X", "utf8", "-c",
              RUNTIME_IDENTITY_CODE), timeout=60, check=False)
    require(cp.returncode == 0 and cp.stderr == b"", "E_RUNTIME_IDENTITY_PROBE", runtime_id)
    try:
        lines = cp.stdout.decode("utf-8", "strict").splitlines()
    except UnicodeError as exc:
        fail("E_RUNTIME_IDENTITY_PROBE", f"{runtime_id}: {exc}")
    require(len(lines) == 2 and all(lines), "E_RUNTIME_IDENTITY_PROBE", runtime_id)
    return lines[0], lines[1]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def reject_constant(value: str) -> Any:
    raise ValueError(f"non-finite JSON constant {value}")


def pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key {key}")
        out[key] = value
    return out


def strict_load_bytes(raw: bytes) -> dict[str, Any]:
    require(raw.endswith(b"\n"), "E_LF_TERMINAL")
    require(b"\r" not in raw, "E_CR_BYTE")
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_no_duplicates,
                     parse_constant=reject_constant)
    require(isinstance(obj, dict), "E_JSON_ROOT")
    return obj


def semantic_hash(obj: dict[str, Any]) -> str:
    projected = copy.deepcopy(obj)
    projected.pop("semantic_sha256", None)
    return sha256(compact(projected))


def traverse(value: Any, depth: int = 0) -> tuple[int, int]:
    count, maximum = 1, depth
    if isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str), "E_KEY_TYPE")
            c, d = traverse(item, depth + 1); count += c; maximum = max(maximum, d)
    elif isinstance(value, list):
        for item in value:
            c, d = traverse(item, depth + 1); count += c; maximum = max(maximum, d)
    elif isinstance(value, float):
        require(value == value and abs(value) != float("inf"), "E_NONFINITE")
    elif value is not None:
        require(isinstance(value, (str, int, bool)), "E_VALUE_TYPE", type(value).__name__)
    return count, maximum


def schema_shape(value: Any) -> list[Any]:
    if isinstance(value, dict):
        return ["dict", [[key, schema_shape(value[key])] for key in sorted(value)]]
    if isinstance(value, list):
        return ["list", [schema_shape(item) for item in value]]
    if value is None:
        return ["null"]
    if isinstance(value, bool):
        return ["bool"]
    if isinstance(value, int):
        return ["int"]
    if isinstance(value, float):
        return ["float"]
    if isinstance(value, str):
        return ["str"]
    fail("E_SCHEMA_VALUE_TYPE", type(value).__name__)


def check_exact_schema(matrix: dict[str, Any], runtime: dict[str, Any]) -> None:
    require(sha256(compact(schema_shape(matrix))) == EXPECTED_MATRIX_SCHEMA_SHA256,
            "E_MATRIX_SCHEMA_FINGERPRINT")
    require(sha256(compact(schema_shape(runtime))) == EXPECTED_RUNTIME_SCHEMA_SHA256,
            "E_RUNTIME_SCHEMA_FINGERPRINT")


@lru_cache(maxsize=None)
def git_bytes(revision: str, path: str) -> bytes:
    return run(("git", "cat-file", "blob", f"{revision}:{path}")).stdout


@lru_cache(maxsize=None)
def git_blob(revision: str, path: str) -> str:
    return run(("git", "rev-parse", f"{revision}:{path}")).stdout.decode().strip()


def require_upstream_name(actual: str) -> None:
    require(actual == EXPECTED_UPSTREAM, "E_UPSTREAM_NAME", actual)


def require_live_ref(ref: str, expected_hash: str, code: str) -> None:
    lines = run(("git", "ls-remote", "--heads", "origin", ref)).stdout.decode().splitlines()
    require(lines == [f"{expected_hash}\t{ref}"], code, repr(lines))


def index_worktree_raw_equal(repository: Path, path: str) -> bool:
    index_bytes = run(("git", "cat-file", "blob", f":{path}"), cwd=repository).stdout
    return index_bytes == (repository / path).read_bytes()


def check_header(obj: dict[str, Any], kind: str) -> None:
    require(obj["artifact_kind"] == kind, "E_KIND")
    require(obj["schema_version"] == 1 and obj["phase"] == 65 and obj["step"] == 73, "E_SCHEMA")
    require(obj["baseline_commit"] == BASELINE, "E_BASELINE")
    require(obj["expected_parent"] == EXPECTED_PARENT, "E_PARENT")
    require(obj["expected_subject"] == EXPECTED_SUBJECT, "E_SUBJECT")
    require(obj["branch"] == BRANCH, "E_BRANCH")
    require(obj["generated_date"] == "2026-08-31", "E_GENERATED_DATE")
    require(obj["gate"] == "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS", "E_GATE")
    require(obj["result_first_contract"] == RESULT_FIRST_CONTRACT, "E_RESULT_FIRST_CONTRACT")
    require(obj["semantic_sha256"] == semantic_hash(obj), "E_SEMANTIC_HASH")


def check_controls(matrix: dict[str, Any]) -> None:
    rows = matrix["control_source_bindings"]
    require(len(rows) == 6, "E_CONTROL_COUNT")
    by_path = {row["path"]: row for row in rows}
    require(set(by_path) == set(CONTROL_ROLES), "E_CONTROL_PATHS")
    for path, role in CONTROL_ROLES.items():
        raw = (ROOT / path).read_bytes()
        row = by_path[path]
        require(row["role"] == role, "E_CONTROL_ROLE", path)
        require(row["sha256"] == sha256(raw) and row["bytes"] == len(raw), "E_CONTROL_HASH", path)


def check_matrix(matrix: dict[str, Any], runtime: dict[str, Any], step71: dict[str, Any]) -> None:
    check_header(matrix, "PHASE_065_INITIALIZATION_ROUTE_MATRIX")
    require(matrix["outcome_vocabulary"] == OUTCOMES, "E_OUTCOME_VOCAB")
    consumed = matrix["consumed_step71"]
    require(consumed["path"] == "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json", "E_STEP71_PATH")
    require(consumed["sha256"] == sha256(STEP71_PATH.read_bytes()), "E_STEP71_RAW")
    require(consumed["semantic_sha256"] == step71["semantic_sha256"], "E_STEP71_SEMANTIC")
    require(consumed["gate"] == step71["gate"], "E_STEP71_GATE")
    require(consumed["route_outcomes"] == step71["route_outcomes"], "E_STEP71_ROUTES")
    require(matrix["exact_initialization_mapping"] == step71["initialization_rows"], "E_INITIALIZATION_MAP")
    require(matrix["exact_profile_mapping"] == step71["profile_surfaces"], "E_PROFILE_MAP")
    require(len(matrix["routes"]) == 3, "E_ROUTE_COUNT")
    routes = {row["route"]: row for row in matrix["routes"]}
    require(set(routes) == {"fresh_import", "explicit_profile", "legacy_restoration"}, "E_ROUTE_SET")
    require(routes["fresh_import"]["outcome"] == "IMPLEMENTED_AND_OBSERVED", "E_FRESH_OUTCOME")
    require(routes["explicit_profile"]["outcome"] == "IMPLEMENTED_AND_OBSERVED", "E_EXPLICIT_OUTCOME")
    for route_id in ("fresh_import", "explicit_profile"):
        row = routes[route_id]
        require(row["own_process"] and row["own_fixture"] and row["own_observations"], "E_ROUTE_INDEPENDENCE", route_id)
        require(len(row["process_run_ids"]) == 4 and len(set(row["process_run_ids"])) == 4, "E_ROUTE_PROCESS_IDS", route_id)
    legacy = routes["legacy_restoration"]
    require(legacy["outcome"] == "ABSENT_IN_FROZEN_SOURCE", "E_LEGACY_OUTCOME")
    require(not legacy["passing_behavior_route"] and legacy["absence_is_not_a_passing_behavior_route"], "E_LEGACY_PASS")
    require(legacy["process_run_ids"] == [] and len(legacy["absence_corroboration_run_ids"]) == 4, "E_LEGACY_RUNTIME_CLASS")
    positive = [row for row in runtime["route_runs"] if row["mutation"] == "none"]
    mutations = [row for row in runtime["route_runs"] if row["mutation"] != "none"]
    for route_id, probe_route, outcome, authority in (
        ("fresh_import", "fresh", "IMPLEMENTED_AND_OBSERVED", "ISOLATED_RUNTIME_PLUS_STEP71_STATIC"),
        ("explicit_profile", "explicit", "IMPLEMENTED_AND_OBSERVED", "ISOLATED_RUNTIME_PLUS_STEP71_STATIC"),
        ("legacy_restoration", "legacy", "ABSENT_IN_FROZEN_SOURCE", "STEP71_STATIC_CENSUS_PRIMARY_RUNTIME_CORROBORATION_ONLY"),
    ):
        implemented = outcome == "IMPLEMENTED_AND_OBSERVED"
        expected_route = {
            "route": route_id, "outcome": outcome, "authority": authority,
            "process_run_ids": ([r["run_id"] for r in positive if r["route"] == probe_route]
                                if implemented else []),
            "absence_corroboration_run_ids": ([r["run_id"] for r in positive if r["route"] == probe_route]
                                               if not implemented else []),
            "mutation_run_ids": [r["run_id"] for r in mutations if r["route"] == probe_route],
            "own_process": implemented, "own_fixture": implemented,
            "own_observations": implemented,
            "absence_corroboration_process_is_not_route_execution": not implemented,
            "changed_order_control": True, "passing_behavior_route": implemented,
            "absence_is_not_a_passing_behavior_route": not implemented,
        }
        require(routes[route_id] == expected_route, "E_ROUTE_RELATION", route_id)
    require(matrix["counts"] == {"initialization_rows": 40, "profile_surfaces": 11,
                                  "routes": 3, "implemented_routes": 2,
                                  "absent_routes": 1, "ground_not_found_routes": 0,
                                  "control_bindings": 6}, "E_MATRIX_COUNTS")
    require(len(matrix["profile_runtime_routes"]) == 11, "E_PROFILE_ROUTE_COUNT")
    require({r["profile_id"] for r in matrix["profile_runtime_routes"]} == {r["profile_id"] for r in step71["profile_surfaces"]}, "E_PROFILE_ROUTE_IDS")
    explicit_observations = [row["observations"] for row in positive if row["route"] == "explicit"]
    require(len(explicit_observations) == 4 and all(x == explicit_observations[0] for x in explicit_observations),
            "E_PROFILE_OBSERVATION_CONSENSUS")
    public_routes = {row["profile_id"]: row["public_path"]
                     for row in explicit_observations[0]["profiles"]}
    expected_profile_routes = [
        {"profile_id": row["profile_id"], "ast_sha256": row["ast_sha256"],
         "entrypoint_observed": True, "public_route": public_routes[row["profile_id"]]}
        for row in step71["profile_surfaces"]
    ]
    require(matrix["profile_runtime_routes"] == expected_profile_routes, "E_PROFILE_ROUTE_RELATION")
    owners = matrix["feature_observation_owners"]
    require(owners == {
        "default_off_and_enabled": "explicit_profile.lco_electronic_entropy",
        "old_key_absence": "ABSENT_IN_FROZEN_SOURCE; no predecessor persistence schema or restore key",
        "explicit_zero_false": "explicit_profile lco/curve observations",
        "current_saved_state_key_presence": "ABSENT_IN_FROZEN_SOURCE; no current persistence schema or restore key",
        "legacy_restoration": "ABSENT_IN_FROZEN_SOURCE",
        "seconds_hour": "explicit_profile.seconds_hour",
        "exceptions_and_unsupported": "explicit_profile.scope_boundaries",
    }, "E_FEATURE_OWNERS")
    binding = matrix["runtime_attestation_binding"]
    require(binding["path"] == "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json", "E_RUNTIME_PATH")
    require(binding["semantic_sha256"] == runtime["semantic_sha256"], "E_RUNTIME_BINDING")
    require(binding["gate"] == runtime["gate"], "E_RUNTIME_GATE_BINDING")
    require(all(matrix["negative_controls"].values()), "E_NEGATIVE_CONTROLS")
    policy = matrix["source_policy"]
    require(all(policy.values()), "E_SOURCE_POLICY")
    require(matrix["authority_boundary"] == runtime["authority_boundary"], "E_AUTHORITY_BINDING")
    require(not any(matrix["authority_boundary"][key] for key in (
        "scientific_truth", "material_truth", "experimental_truth", "proposition_support",
        "canonical_adoption", "publication_readiness")), "E_AUTHORITY")
    check_controls(matrix)


def check_command(row: dict[str, Any], manifest_hash: str) -> None:
    cmd = row["command"]
    require("-B" in cmd and "-I" in cmd and "-X" in cmd and "utf8" in cmd, "E_RUNTIME_FLAGS", row["run_id"])
    require(all("Claude/docs" not in token and str(ROOT) not in token for token in cmd), "E_CHECKOUT_IMPORT", row["run_id"])
    require(row["expectation_met"] and row["exit_code"] == row["expected_exit_code"], "E_RUN_EXIT", row["run_id"])
    require(row["source_root"] == "<TMP>" or row["source_root"].startswith("<TMP>/route_fixtures/"), "E_RUN_SOURCE_ROOT", row["run_id"])
    require(row["timed_out"] is False, "E_RUN_ISOLATION", row["run_id"])
    require(isinstance(row["interpreter"], str) and isinstance(row["numpy_version"], str), "E_RUN_VERSIONS", row["run_id"])
    require(row["observations"] is not None and row["gate"].startswith("PASS"), "E_RUN_INTERFACE", row["run_id"])
    require(set(row["mutation_probe"]) == {"enabled", "mutation_id", "detected"}, "E_MUTATION_INTERFACE", row["run_id"])
    input_obj = {"runtime": row["runtime"], "command": cmd, "cwd": row["cwd"],
                 "materialized_manifest_sha256": manifest_hash,
                 "controller_probe_sha256": sha256(extract_probe_source().encode()),
                 "fixture_id": row["fixture_id"], "source_root": row["source_root"]}
    require(row["input_sha256"] == sha256(compact(input_obj)), "E_INPUT_HASH", row["run_id"])
    require(row["stdout_sha256"] == sha256(row["stdout"].encode()), "E_STDOUT_HASH", row["run_id"])
    require(row["stderr_sha256"] == sha256(row["stderr"].encode()), "E_STDERR_HASH", row["run_id"])
    output = {"exit_code": row["exit_code"], "stdout": row["stdout"], "stderr": row["stderr"]}
    require(row["output_sha256"] == sha256(compact(output)), "E_OUTPUT_HASH", row["run_id"])
    require(row["external_scientific_truth"] is False, "E_RUN_AUTHORITY", row["run_id"])


def stdout_json(row: dict[str, Any]) -> dict[str, Any]:
    try:
        value = json.loads(row["stdout"], object_pairs_hook=pairs_no_duplicates,
                           parse_constant=reject_constant)
    except (UnicodeError, ValueError, TypeError) as exc:
        fail("E_ROUTE_STDOUT_JSON", f"{row['run_id']}: {exc}")
    require(isinstance(value, dict), "E_ROUTE_STDOUT_JSON", row["run_id"])
    return value


def check_runtime(runtime: dict[str, Any]) -> None:
    check_header(runtime, "PHASE_065_RUNTIME_ATTESTATION")
    iso = runtime["isolation"]
    for key in ("exact_git_blobs_materialized", "disposable_external_directory",
                "materialized_path_containment_verified", "bytecode_disabled",
                "isolated_mode", "utf8_mode"):
        require(iso[key] is True, "E_ISOLATION", key)
    require(iso["working_checkout_source_imported"] is False and iso["network_requested"] is False, "E_ISOLATION_NEGATIVE")
    require(iso["probe_program_sha256"] == sha256(extract_probe_source().encode()), "E_PROBE_HASH")
    manifest = iso["materialized_manifest"]
    require([x["source_path"] for x in manifest] == list(RUNTIME_SOURCES), "E_MANIFEST_PATHS")
    expected_base_relative_paths = [
        PurePosixPath(source).relative_to("Claude/docs").as_posix()
        for source in RUNTIME_SOURCES
    ]
    require([x["materialized_relative_path"] for x in manifest] == expected_base_relative_paths,
            "E_MANIFEST_RELATIVE_PATHS")
    require(iso["materialized_manifest_sha256"] == sha256(compact(manifest)), "E_MANIFEST_HASH")
    for row in manifest:
        raw = git_bytes(BASELINE, row["source_path"])
        require(row["git_blob"] == git_blob(BASELINE, row["source_path"]), "E_MANIFEST_BLOB")
        require(row["sha256"] == sha256(raw) and row["bytes"] == len(raw), "E_MANIFEST_RAW")
    after = iso["materialized_manifest_after"]
    require([x["source_path"] for x in after] == list(RUNTIME_SOURCES), "E_MANIFEST_AFTER_PATHS")
    require(all(x["unchanged"] for x in after) and iso["source_blobs_unchanged"], "E_SOURCE_MUTATION")
    before_by_path = {x["source_path"]: x for x in manifest}
    for row in after:
        before = before_by_path[row["source_path"]]
        require(row["sha256"] == before["sha256"] and row["bytes"] == before["bytes"], "E_SOURCE_AFTER_HASH", row["source_path"])
    require(iso["probe_program_unchanged"] and iso["cleanup_verified_after_context"], "E_FIXTURE_CLEANUP")
    require(iso["base_fixture_scan_excluded_top_level"] == ["route_fixtures"], "E_FIXTURE_SCAN_SCOPE")
    expected_base_files = sorted(row["materialized_relative_path"] for row in manifest)
    require(iso["fixture_files_before"] == expected_base_files
            and iso["fixture_files_after"] == expected_base_files,
            "E_FIXTURE_FILE_SET_EXACT")
    require(iso["fixture_files_before"] == iso["fixture_files_after"] and iso["unexpected_fixture_files"] == [], "E_FIXTURE_FILE_SET")
    require(len(runtime["runtime_environments"]) == 2, "E_RUNTIME_ENV_COUNT")
    require({x["runtime"] for x in runtime["runtime_environments"]} == {"3.12", "3.14"}, "E_RUNTIME_SET")
    expected_environment_topology = [
        (runtime_id, f"P065-RUNTIME-{runtime_id.replace('.', '')}",
         f"environment-{runtime_id}", "<TMP>", ".",
         tuple(("py", f"-{runtime_id}", "-B", "-I", "-X", "utf8", "-c", RUNTIME_IDENTITY_CODE)))
        for runtime_id in ("3.12", "3.14")
    ]
    actual_environment_topology = [
        (row["runtime"], row["run_id"], row["fixture_id"], row["source_root"],
         row["cwd"], tuple(row["command"]))
        for row in runtime["runtime_environments"]
    ]
    require(actual_environment_topology == expected_environment_topology, "E_ENV_TOPOLOGY")
    for row in runtime["runtime_environments"]:
        check_command(row, iso["materialized_manifest_sha256"])
        require(row["exit_code"] == row["expected_exit_code"] == 0,
                "E_ENV_EXIT_ZERO", row["run_id"])
        require(row["gate"] == "PASS_RUNTIME_ENVIRONMENT", "E_ENV_GATE", row["run_id"])
        lines = row["stdout"].splitlines()
        require(len(lines) == 2, "E_ENV_STDOUT", row["run_id"])
        expected_observations = {"python_version": lines[0], "numpy_version": lines[1]}
        require(row["observations"] == expected_observations
                and row["python_version"] == lines[0]
                and row["interpreter"] == lines[0]
                and row["numpy_version"] == lines[1], "E_ENV_OBSERVATION", row["run_id"])
        live_python, live_numpy = live_runtime_identity(row["runtime"])
        require((lines[0], lines[1]) == (live_python, live_numpy)
                and row["stdout"] == f"{live_python}\n{live_numpy}\n"
                and row["stderr"] == "",
                "E_ENV_LIVE_IDENTITY", row["run_id"])
        require(row["authority"] == "RUNTIME_ENVIRONMENT_ONLY", "E_ENV_AUTHORITY", row["run_id"])
        require(row["mutation_probe"] == {"enabled": False, "mutation_id": None, "detected": None},
                "E_NONMUTATION_PROBE", row["run_id"])
    environment_by_runtime = {row["runtime"]: row for row in runtime["runtime_environments"]}
    require(len(runtime["official_runs"]) == 10, "E_OFFICIAL_COUNT")
    official_specs = (
        ("v1023-main", "v1.0.23", "test_gates_v1023.py"),
        ("v1023-selfconsistent", "v1.0.23", "test_gates_v1023_selfconsistent.py"),
        ("v1024-main", "v1.0.24", "test_gates_v1024.py"),
        ("v1024-selfconsistent", "v1.0.24", "test_gates_v1024_selfconsistent.py"),
        ("v1024-reflect", "v1.0.24", "test_gates_v1024_reflect.py"),
    )
    expected_official_topology = []
    for runtime_id in ("3.12", "3.14"):
        suffix = runtime_id.replace(".", "")
        for label, cwd, script in official_specs:
            expected_official_topology.append(
                (runtime_id, label, f"P065-OFFICIAL-{label.upper()}-{suffix}",
                 f"official-shared-{runtime_id}", "<TMP>", cwd,
                 ("py", f"-{runtime_id}", "-B", "-I", "-X", "utf8", script)))
    actual_official_topology = [
        (row["runtime"], row["observations"]["official_gate"], row["run_id"],
         row["fixture_id"], row["source_root"], row["cwd"], tuple(row["command"]))
        for row in runtime["official_runs"]
    ]
    require(actual_official_topology == expected_official_topology, "E_OFFICIAL_TOPOLOGY")
    for row in runtime["official_runs"]:
        check_command(row, iso["materialized_manifest_sha256"])
        require(row["exit_code"] == row["expected_exit_code"] == 0,
                "E_OFFICIAL_EXIT_ZERO", row["run_id"])
        require(row["gate"] == "PASS_OFFICIAL_GATE", "E_OFFICIAL_GATE", row["run_id"])
        script_to_label = {
            "test_gates_v1023.py": "v1023-main",
            "test_gates_v1023_selfconsistent.py": "v1023-selfconsistent",
            "test_gates_v1024.py": "v1024-main",
            "test_gates_v1024_selfconsistent.py": "v1024-selfconsistent",
            "test_gates_v1024_reflect.py": "v1024-reflect",
        }
        require(row["command"][-1] in script_to_label, "E_OFFICIAL_COMMAND", row["run_id"])
        require(row["observations"] == {"official_gate": script_to_label[row["command"][-1]],
                                         "exit_zero": True},
                "E_OFFICIAL_OBSERVATION", row["run_id"])
        official_key = (row["runtime"], row["observations"]["official_gate"])
        require(row["stderr"] == ""
                and row["stdout_sha256"] == EXPECTED_OFFICIAL_STDOUT_SHA256[official_key],
                "E_OFFICIAL_OUTPUT_PIN", row["run_id"])
        environment = environment_by_runtime[row["runtime"]]
        require(row["interpreter"] == environment["python_version"]
                and row["numpy_version"] == environment["numpy_version"],
                "E_RUN_ENV_BINDING", row["run_id"])
        require(row["authority"] == "EXACT_COPIED_OFFICIAL_GATE_ONLY",
                "E_OFFICIAL_AUTHORITY", row["run_id"])
        require(row["mutation_probe"] == {"enabled": False, "mutation_id": None, "detected": None},
                "E_NONMUTATION_PROBE", row["run_id"])
    runs = runtime["route_runs"]
    require(len(runs) == 18, "E_ROUTE_RUN_COUNT")
    ids = [r["run_id"] for r in runs]
    require(len(set(ids)) == len(ids), "E_RUN_ID_UNIQUE")
    all_ids = ([row["run_id"] for row in runtime["runtime_environments"]]
               + [row["run_id"] for row in runtime["official_runs"]] + ids)
    require(len(set(all_ids)) == len(all_ids), "E_ALL_RUN_ID_UNIQUE")
    fixture_ids = [row["fixture_id"] for row in runs]
    require(len(set(fixture_ids)) == len(fixture_ids), "E_FIXTURE_ID_UNIQUE")
    require(iso["route_fixture_count"] == len(runs) and iso["route_fixture_ids_unique"] and iso["each_route_run_has_own_fixture"], "E_OWN_FIXTURE")
    for row in runs:
        route_manifest = row["fixture_manifest"]
        require([x["source_path"] for x in route_manifest] == [
            "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
            "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py"], "E_ROUTE_MANIFEST_PATHS")
        require([x["materialized_relative_path"] for x in route_manifest] == [
            "v1.0.23/Anode_Fit_v1.0.23.py",
            "v1.0.24/Anode_Fit_v1.0.24.py"], "E_ROUTE_MANIFEST_RELATIVE_PATHS")
        for source_row in route_manifest:
            raw = git_bytes(BASELINE, source_row["source_path"])
            require(source_row["git_blob"] == git_blob(BASELINE, source_row["source_path"]), "E_ROUTE_MANIFEST_BLOB")
            require(source_row["sha256"] == sha256(raw) and source_row["bytes"] == len(raw), "E_ROUTE_MANIFEST_RAW")
        route_input = {"sources": route_manifest, "probe_program_sha256": sha256(extract_probe_source().encode())}
        route_hash = sha256(compact(route_input))
        require(row["fixture_input_manifest_sha256"] == route_hash, "E_ROUTE_INPUT_MANIFEST")
        require(row["source_before_sha256"] == route_hash and row["source_after_sha256"] == route_hash and row["source_unchanged"], "E_ROUTE_SOURCE_IMMUTABLE")
        expected_route_files = sorted([*(source_row["materialized_relative_path"]
                                        for source_row in route_manifest),
                                       "step73_route_probe.py"])
        require(row["fixture_files_before"] == expected_route_files
                and row["fixture_files_after"] == expected_route_files,
                "E_ROUTE_FIXTURE_FILES_EXACT", row["run_id"])
        require(row["fixture_files_before"] == row["fixture_files_after"], "E_ROUTE_FIXTURE_FILES")
        check_command(row, route_hash)
        expected_gate = ("PASS_MUTATION_REJECTED" if row["mutation"] != "none" else
                         "PASS_ABSENCE_CORROBORATION" if row["route"] == "legacy" else
                         "PASS_IMPLEMENTED_ROUTE")
        require(row["gate"] == expected_gate, "E_ROUTE_GATE", row["run_id"])
        environment = environment_by_runtime[row["runtime"]]
        require(row["interpreter"] == environment["python_version"]
                and row["numpy_version"] == environment["numpy_version"],
                "E_RUN_ENV_BINDING", row["run_id"])
        if row["mutation"] == "none":
            require(sha256(compact(row["observations"])) ==
                    EXPECTED_ROUTE_OBSERVATION_SHA256[row["route"]],
                    "E_ROUTE_OBSERVATION_PIN", row["run_id"])
            require(row["authority"] == "ISOLATED_INTERNAL_RUNTIME_ONLY",
                    "E_ROUTE_AUTHORITY", row["run_id"])
            require(row["mutation_probe"] == {"enabled": False, "mutation_id": None, "detected": None},
                    "E_NONMUTATION_PROBE", row["run_id"])
            require(stdout_json(row) == {"route": row["route"], "mutation": "none",
                                         "result": row["observations"]},
                    "E_ROUTE_STDOUT_BINDING", row["run_id"])
        else:
            require(sha256(compact(row["observations"])) ==
                    EXPECTED_ROUTE_OBSERVATION_SHA256["mutation"],
                    "E_ROUTE_OBSERVATION_PIN", row["run_id"])
            require(row["authority"] == "ROUTE_MUTATION_NEGATIVE_CONTROL",
                    "E_MUTATION_AUTHORITY", row["run_id"])
            require(row["mutation_probe"] == {"enabled": True, "mutation_id": row["route"],
                                               "detected": True},
                    "E_MUTATION_PROBE", row["run_id"])
            expected_stderr = {
                "fresh": "AssertionError: fresh required symbols missing:GRAPHITE_STAGING_XRD_v1024,GRAPHITE_STAGING_MSMR6_LIT\n",
                "explicit": "AssertionError: profile redirect detected:GRAPHITE_STAGING_XRD_v1024\n",
                "legacy": "AssertionError: false implemented-restoration claim rejected\n",
            }
            require(row["stdout"] == "" and row["stderr"] == expected_stderr[row["route"]],
                    "E_MUTATION_OUTPUT", row["run_id"])
            require(row["observations"] == {"expected_failure_exit": 7, "actual_exit": 7,
                                             "mutation_detected": True},
                    "E_MUTATION_OBSERVATION", row["run_id"])
    normal = [r for r in runs if r["mutation"] == "none"]
    mutations = [r for r in runs if r["mutation"] != "none"]
    require(len(normal) == 12 and len(mutations) == 6, "E_RUN_CLASS_COUNTS")
    require(all(r["exit_code"] == 0 and r["observations"] is not None for r in normal), "E_NORMAL_RUNS")
    require(all(r["exit_code"] == 7 and r["mutation_detected"] for r in mutations), "E_MUTATION_RUNS")
    expected_normal_topology = []
    expected_mutation_topology = []
    order_routes = {"A": (("fresh", 1), ("explicit", 2), ("legacy", 3)),
                    "B": (("legacy", 1), ("explicit", 2), ("fresh", 3))}
    for runtime_id in ("3.12", "3.14"):
        suffix = runtime_id.replace(".", "")
        for order, route_positions in order_routes.items():
            for route, position in route_positions:
                run_id = f"P065-ROUTE-{route.upper()}-{order}-{suffix}"
                expected_normal_topology.append(
                    (runtime_id, route, order, position, "none", run_id, run_id.lower()))
        for route in ("fresh", "explicit", "legacy"):
            run_id = f"P065-MUTATION-{route.upper()}-{suffix}"
            expected_mutation_topology.append(
                (runtime_id, route, "MUTATION", None, route, run_id, run_id.lower()))
    topology = lambda row: (row["runtime"], row["route"], row["order_id"], row["position"],
                            row["mutation"], row["run_id"], row["fixture_id"])
    require([topology(row) for row in normal] == expected_normal_topology, "E_NORMAL_TOPOLOGY")
    require([topology(row) for row in mutations] == expected_mutation_topology, "E_MUTATION_TOPOLOGY")
    for row in runs:
        fixture_root = f"<TMP>/route_fixtures/{row['fixture_id']}"
        normalized_command = [token.replace("\\", "/") for token in row["command"]]
        expected_v24 = "v1.0.23/Anode_Fit_v1.0.23.py" if row["mutation"] == "fresh" else "v1.0.24/Anode_Fit_v1.0.24.py"
        require(row["cwd"].replace("\\", "/") == f"route_fixtures/{row['fixture_id']}"
                and row["source_root"] == fixture_root
                and normalized_command == [
                    "py", f"-{row['runtime']}", "-B", "-I", "-X", "utf8",
                    f"{fixture_root}/step73_route_probe.py",
                    f"{fixture_root}/v1.0.23/Anode_Fit_v1.0.23.py",
                    f"{fixture_root}/{expected_v24}", row["route"], row["mutation"],
                ], "E_ROUTE_COMMAND_TOPOLOGY", row["run_id"])
    expected_order_controls = []
    for runtime_id in ("3.12", "3.14"):
        for route in ("fresh", "explicit", "legacy"):
            a = next(row for row in normal if row["runtime"] == runtime_id and row["route"] == route and row["order_id"] == "A")
            b = next(row for row in normal if row["runtime"] == runtime_id and row["route"] == route and row["order_id"] == "B")
            expected_order_controls.append({
                "runtime": runtime_id, "route": route,
                "order_A_output_sha256": sha256(compact(a["observations"])),
                "order_B_output_sha256": sha256(compact(b["observations"])),
                "normalized_observations_equal": a["observations"] == b["observations"],
            })
    require(runtime["changed_order_controls"] == expected_order_controls
            and all(row["normalized_observations_equal"] for row in expected_order_controls),
            "E_ORDER_RELATION")
    fresh = [r["observations"] for r in normal if r["route"] == "fresh"]
    require(all(x["pass"] and x["constructor"] == "BlendedAnodeDQDV(0.0)" for x in fresh), "E_FRESH_PASS")
    require(all(x["graphite_constructor_requires_transitions"] and x["lco_constructor_requires_transitions"] for x in fresh), "E_FRESH_REQUIRED")
    explicit = [r["observations"] for r in normal if r["route"] == "explicit"]
    require(all(x["pass"] and len(x["profiles"]) == 11 and all(x["checks"].values()) for x in explicit), "E_EXPLICIT_PASS")
    require(all(x["seconds_hour"]["None_I_abs_capture"] == 2.0 and x["seconds_hour"]["explicit_zero_capture"] == 0.0 for x in explicit), "E_SECONDS_HOUR")
    legacy = [r["observations"] for r in normal if r["route"] == "legacy"]
    require(all(x["actual_restoration_path"] == "ABSENT_IN_FROZEN_SOURCE" and x["predecessor_schema_fixture"] == "ABSENT_IN_FROZEN_SOURCE" for x in legacy), "E_LEGACY_ABSENCE")
    expected_counts = {"runtimes": 2, "official_runs": 10, "official_expectations_met": 10,
        "implemented_behavior_route_runs": 8, "implemented_behavior_route_expectations_met": 8,
        "absence_corroboration_runs": 4, "absence_corroboration_expectations_met": 4,
        "mutation_runs": 6, "mutations_detected": 6,
        "changed_order_checks": 6, "changed_order_equal": 6}
    require(runtime["counts"] == expected_counts, "E_RUNTIME_COUNTS", repr(runtime["counts"]))
    require(runtime["authority_boundary"]["internal_runtime_behavior"] is True, "E_INTERNAL_AUTHORITY")
    require(not any(runtime["authority_boundary"][key] for key in (
        "scientific_truth", "material_truth", "experimental_truth", "proposition_support",
        "canonical_adoption", "publication_readiness")), "E_RUNTIME_AUTHORITY")


def extract_probe_source() -> str:
    tree = ast.parse(BUILDER_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PROBE_SOURCE" for t in node.targets):
            require(isinstance(node.value, ast.Constant) and isinstance(node.value.value, str), "E_PROBE_LITERAL")
            return node.value.value
    fail("E_PROBE_MISSING")


def source_policy_errors(builder_source: str, probe_source: str) -> list[str]:
    errors: list[str] = []
    try:
        builder_tree = ast.parse(builder_source)
        probe_tree = ast.parse(probe_source)
    except SyntaxError as exc:
        return [f"syntax:{exc}"]

    runtime_key = sys.version_info[:2]
    if runtime_key not in EXPECTED_BUILDER_CANONICAL_AST:
        errors.append(f"unsupported-validator-runtime:{runtime_key}")
    else:
        builder_ast_sha = sha256(ast.dump(builder_tree, annotate_fields=True,
                                          include_attributes=False).encode())
        probe_ast_sha = sha256(ast.dump(probe_tree, annotate_fields=True,
                                        include_attributes=False).encode())
        if builder_ast_sha != EXPECTED_BUILDER_CANONICAL_AST[runtime_key]:
            errors.append(f"builder-canonical-ast:{builder_ast_sha}")
        if probe_ast_sha != EXPECTED_PROBE_CANONICAL_AST[runtime_key]:
            errors.append(f"probe-canonical-ast:{probe_ast_sha}")

    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(builder_tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    def owner(node: ast.AST) -> str:
        cur = node
        while cur in parents:
            cur = parents[cur]
            if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return cur.name
        return "<module>"

    forbidden_imports = {"socket", "requests", "urllib", "http", "ftplib", "paramiko", "multiprocessing"}
    subprocess_imports = 0
    imports: list[str] = []
    for node in ast.walk(builder_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                imports.append(f"import:{alias.name}:{alias.asname or ''}")
                if root in forbidden_imports:
                    errors.append(f"forbidden-import:{root}")
                if root == "subprocess":
                    subprocess_imports += 1
                    if alias.name != "subprocess" or alias.asname is not None:
                        errors.append("aliased-subprocess-import")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            for alias in node.names:
                imports.append(f"from:{node.module or ''}:{alias.name}:{alias.asname or ''}")
            if root in forbidden_imports or root in {"subprocess", "os"}:
                errors.append(f"forbidden-from-import:{root}")
    expected_imports = [
        "from:__future__:annotations:",
        "import:argparse:", "import:copy:", "import:hashlib:", "import:json:",
        "import:os:", "import:subprocess:", "import:sys:", "import:tempfile:",
        "from:pathlib:Path:", "from:pathlib:PurePosixPath:", "from:typing:Any:",
    ]
    if sorted(imports) != sorted(expected_imports):
        errors.append(f"import-set:{sorted(imports)}")
    if subprocess_imports != 1:
        errors.append(f"subprocess-import-count:{subprocess_imports}")

    subprocess_calls: list[str] = []
    choke_callers: list[str] = []
    runtime_callers: list[str] = []
    git_callers: list[str] = []
    path_mutations: list[tuple[str, str]] = []
    suspicious_names = {"Popen", "call", "check_call", "check_output", "getoutput",
                        "getstatusoutput", "system", "popen", "spawn", "execv", "execve"}
    mutation_attributes = {"write_text", "write_bytes", "write", "writelines", "truncate",
                           "open", "unlink", "remove", "rename", "renames", "replace",
                           "rmdir", "removedirs", "touch", "chmod", "lchmod", "link_to",
                           "symlink_to", "hardlink_to", "mkdir", "makedirs"}
    sensitive_bound_attributes = suspicious_names | mutation_attributes | {"run"}
    dynamic_names = {"__import__", "eval", "exec", "compile", "globals", "locals", "vars"}
    module_attributes = {
        "subprocess": {"CompletedProcess", "PIPE", "run"},
        "os": {"environ", "replace"},
        "sys": {"exit"},
    }
    for node in ast.walk(builder_tree):
        if isinstance(node, ast.Attribute) and node.attr in sensitive_bound_attributes:
            parent = parents.get(node)
            if not (isinstance(parent, ast.Call) and parent.func is node):
                errors.append(f"bound-sensitive-attribute:{node.attr}@{owner(node)}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in {
            "_run_subprocess", "run_runtime", "run_git"
        }:
            parent = parents.get(node)
            if not (isinstance(parent, ast.Call) and parent.func is node):
                errors.append(f"bound-choke-reference:{node.id}@{owner(node)}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in module_attributes:
            parent = parents.get(node)
            if not (isinstance(parent, ast.Attribute) and parent.value is node
                    and parent.attr in module_attributes[node.id]):
                errors.append(f"module-alias-or-attribute:{node.id}@{owner(node)}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in dynamic_names | {
            "getattr", "setattr", "delattr", "open", "__builtins__"
        }:
            errors.append(f"dynamic-reference:{node.id}@{owner(node)}")
        if not isinstance(node, ast.Call):
            continue
        call_owner = owner(node)
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            receiver, attr = node.func.value.id, node.func.attr
            if receiver == "subprocess":
                subprocess_calls.append(f"{attr}@{call_owner}")
                if attr != "run" or call_owner != "_run_subprocess":
                    errors.append(f"subprocess-call:{attr}@{call_owner}")
                if attr == "run":
                    keywords = {kw.arg: kw.value for kw in node.keywords if kw.arg is not None}
                    shell = keywords.get("shell")
                    check = keywords.get("check")
                    if not (isinstance(shell, ast.Constant) and shell.value is False):
                        errors.append("subprocess-shell-not-false")
                    if not (isinstance(check, ast.Constant) and check.value is False):
                        errors.append("subprocess-check-not-false")
                    if any(kw.arg is None for kw in node.keywords):
                        errors.append("subprocess-dynamic-keywords")
            if receiver == "os" and attr in suspicious_names:
                errors.append(f"os-execution:{attr}@{call_owner}")
        if isinstance(node.func, ast.Attribute) and node.func.attr in suspicious_names:
            errors.append(f"suspicious-attribute-call:{node.func.attr}@{call_owner}")
        if isinstance(node.func, ast.Attribute) and node.func.attr == "run":
            if not (isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"):
                errors.append(f"nonliteral-run-receiver@{call_owner}")
        if isinstance(node.func, ast.Name):
            if node.func.id in suspicious_names:
                errors.append(f"suspicious-call:{node.func.id}@{call_owner}")
            if node.func.id in dynamic_names:
                errors.append(f"dynamic-call:{node.func.id}@{call_owner}")
            if node.func.id == "_run_subprocess":
                choke_callers.append(call_owner)
            elif node.func.id == "run_runtime":
                runtime_callers.append(call_owner)
            elif node.func.id == "run_git":
                git_callers.append(call_owner)
        if isinstance(node.func, ast.Attribute) and node.func.attr in mutation_attributes:
            path_mutations.append((node.func.attr, call_owner))
        if isinstance(node.func, ast.Name) and node.func.id in {"getattr", "setattr", "delattr"}:
            errors.append(f"dynamic-attribute-access:{node.func.id}@{call_owner}")

    if subprocess_calls != ["run@_run_subprocess"]:
        errors.append(f"subprocess-choke:{subprocess_calls}")
    if sorted(choke_callers) != ["run_git", "run_runtime"]:
        errors.append(f"choke-callers:{sorted(choke_callers)}")
    if runtime_callers != ["run_record"]:
        errors.append(f"runtime-callers:{runtime_callers}")
    if not git_callers or set(git_callers) - {"git_bytes", "git_blob", "guard_json_last"}:
        errors.append(f"git-callers:{git_callers}")

    expected_mutations = [
        ("mkdir", "atomic_json"), ("write", "atomic_json"),
        ("replace", "atomic_json"), ("unlink", "atomic_json"),
        ("mkdir", "materialize"), ("write_bytes", "materialize"),
        ("write_text", "create_route_fixture"),
        ("replace", "normalized_text"), ("replace", "normalized_text"),
        ("replace", "normalized_text"),
        ("replace", "run_record"), ("replace", "run_record"),
        ("replace", "run_record"),
        ("replace", "collect_runtime"), ("replace", "collect_runtime"),
        ("replace", "collect_runtime"), ("replace", "collect_runtime"),
    ]
    if sorted(path_mutations) != sorted(expected_mutations):
        errors.append(f"filesystem-mutations:{sorted(path_mutations)}")

    probe_imports = set()
    for node in ast.walk(probe_tree):
        if isinstance(node, ast.Import):
            probe_imports.update(x.name.split(".")[0] for x in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            probe_imports.add(node.module.split(".")[0])
    allowed_probe_imports = {"__future__", "hashlib", "importlib", "json", "pathlib", "sys", "numpy"}
    if probe_imports - allowed_probe_imports:
        errors.append(f"probe-imports:{sorted(probe_imports - allowed_probe_imports)}")
    for node in ast.walk(probe_tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {
            "write_text", "write_bytes", "unlink", "mkdir", "rename", "replace", "rmdir", "touch"
        }:
            errors.append(f"probe-write:{node.func.attr}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"open", "exec", "eval", "compile", "__import__"}:
            errors.append(f"probe-dynamic:{node.func.id}")
    return errors


def check_source_policy() -> int:
    builder_source = BUILDER_PATH.read_text(encoding="utf-8")
    validator_source = Path(__file__).read_text(encoding="utf-8")
    probe_source = extract_probe_source()
    errors = source_policy_errors(builder_source, probe_source)
    require(not errors, "E_SOURCE_POLICY_AST", repr(errors))
    negative_sources = [
        builder_source + "\nfrom subprocess import run as alias_run\nalias_run(['x'])\n",
        builder_source + "\nsubprocess.Popen(['x'])\n",
        builder_source + "\nos.system('x')\n",
        builder_source + "\nPath('escape').write_text('x')\n",
        builder_source + "\nfrom os import system as harmless\nharmless('x')\n",
        builder_source + "\nwriter=Path('escape').write_text\nwriter('x')\n",
        builder_source + "\nrunner=__import__('subprocess').run\nrunner(['x'])\n",
        builder_source + "\nimport os as harmless\nharmless.system('x')\n",
        builder_source + "\nsys.modules['subprocess'].run(['x'])\n",
        builder_source + "\nimport importlib\nimportlib.import_module('subprocess').run(['x'])\n",
        builder_source + "\nalias=subprocess\nalias.run(['x'])\n",
        builder_source + "\nimp=__import__\nimp('subprocess').run(['x'])\n",
        builder_source + "\nga=getattr\nga(subprocess,'run')(['x'])\n",
        builder_source + "\nPath('a').replace('b')\n",
        builder_source + "\nopen('x','w').write('x')\n",
        builder_source.replace('"cat-file", "blob"', '"clean", "-fd"', 1),
        builder_source + "\ndef rogue():\n    return _run_subprocess(('x',),cwd=ROOT,timeout=1,env=None,check=False)\n",
        builder_source.replace("shell=False", "shell=True", 1),
    ]
    for index, mutated in enumerate(negative_sources, 1):
        require(bool(source_policy_errors(mutated, probe_source)), "E_SOURCE_POLICY_NEGATIVE", str(index))
    bad_probe = probe_source + "\npathlib.Path('escape').write_text('x')\n"
    require(bool(source_policy_errors(builder_source, bad_probe)), "E_PROBE_POLICY_NEGATIVE")
    return (len(list(ast.walk(ast.parse(builder_source))))
            + len(list(ast.walk(ast.parse(validator_source))))
            + len(list(ast.walk(ast.parse(probe_source)))))


def check_documents() -> None:
    result = (ROOT / "Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md").read_text(encoding="utf-8")
    parent = (ROOT / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md").read_text(encoding="utf-8")
    canonical = (ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md").read_text(encoding="utf-8")
    handover = (ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md").read_text(encoding="utf-8")
    for token in ("PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS", "ABSENT_IN_FROZEN_SOURCE",
                  "IMPLEMENTED_AND_OBSERVED", "PENDING_AT_PRECOMMIT_BY_DESIGN", "Step 73"):
        require(token in result, "E_RESULT_TOKEN", token)
    require("Step 72" in result and "272b8d331c55448182e96c75363a56061adf58f2" in result, "E_RESULT_PARENT")
    for label, text in (("parent", parent), ("canonical", canonical), ("handover", handover)):
        require("Step 73" in text and "Step 74" in text and "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS" in text, "E_LEDGER_TOKEN", label)
        require("272b8d331c55448182e96c75363a56061adf58f2" in text, "E_STEP72_COMMIT", label)
    require("PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md" in handover, "E_HANDOVER_RESULT")


def check_output_boundary() -> int:
    forbidden = ROOT / "Codex/work/v1024_phase065" / f"__step73_forbidden_output_{sys.version_info.major}_{sys.version_info.minor}__"
    require(not forbidden.exists(), "E_OUTPUT_BOUNDARY_PREEXISTING", str(forbidden))
    before = (MATRIX_PATH.read_bytes(), RUNTIME_PATH.read_bytes())
    cp = run((sys.executable, "-B", "-I", "-X", "utf8", str(BUILDER_PATH),
              "--output-dir", str(forbidden)), timeout=60, check=False)
    require(cp.returncode != 0, "E_OUTPUT_BOUNDARY_ACCEPTED")
    require(b"explicit output directory must remain outside repository" in cp.stderr,
            "E_OUTPUT_BOUNDARY_SIGNAL")
    require(not forbidden.exists(), "E_OUTPUT_BOUNDARY_WROTE")
    require(before == (MATRIX_PATH.read_bytes(), RUNTIME_PATH.read_bytes()),
            "E_OUTPUT_BOUNDARY_CHANGED_ARTIFACT")
    return 1


def check_temporary_link_boundary() -> int:
    repository_before = (MATRIX_PATH.read_bytes(), RUNTIME_PATH.read_bytes())
    with tempfile.TemporaryDirectory(prefix="p065_step73_output_link_") as td:
        root = Path(td)
        approved = root / "approved"
        approved.mkdir()
        sentinel = root / "outside-approved-sentinel.bin"
        sentinel_payload = b"P065_STEP73_SENTINEL\n"
        sentinel.write_bytes(sentinel_payload)
        trap = approved / f"{RUNTIME_PATH.name}.tmp"
        try:
            trap.symlink_to(sentinel)
        except OSError:
            os.link(sentinel, trap)
        require(trap.exists() or trap.is_symlink(), "E_TEMP_LINK_SETUP")
        cp = run((sys.executable, "-B", "-I", "-X", "utf8", str(BUILDER_PATH),
                  "--output-dir", str(approved)), timeout=60, check=False)
        require(cp.returncode != 0, "E_TEMP_LINK_BOUNDARY_ACCEPTED")
        require(b"pre-existing temporary output path is forbidden" in cp.stderr,
                "E_TEMP_LINK_BOUNDARY_SIGNAL")
        require(sentinel.read_bytes() == sentinel_payload, "E_TEMP_LINK_SENTINEL_CHANGED")
        require(not (approved / RUNTIME_PATH.name).exists()
                and not (approved / MATRIX_PATH.name).exists(), "E_TEMP_LINK_OUTPUT_WRITTEN")
    require(repository_before == (MATRIX_PATH.read_bytes(), RUNTIME_PATH.read_bytes()),
            "E_TEMP_LINK_REPOSITORY_CHANGED")
    return 1


def transaction_negatives() -> int:
    try:
        require_upstream_name("origin/wrong-same-commit-branch")
    except ValidationError as exc:
        require("E_UPSTREAM_NAME" in str(exc), "E_TRANSACTION_NEGATIVE_UPSTREAM")
    else:
        fail("E_TRANSACTION_NEGATIVE_UPSTREAM_ACCEPTED")
    with tempfile.TemporaryDirectory(prefix="p065_step73_git_raw_") as td:
        repository = Path(td)
        run(("git", "init", "-q"), cwd=repository)
        (repository / ".gitattributes").write_text("sample.txt text eol=lf\n",
                                                   encoding="utf-8", newline="\n")
        sample = repository / "sample.txt"
        sample.write_bytes(b"alpha\n")
        run(("git", "add", "--", ".gitattributes", "sample.txt"), cwd=repository)
        sample.write_bytes(b"alpha\r\n")
        require(not run(("git", "diff", "--name-only", "--", "sample.txt"),
                        cwd=repository).stdout.splitlines(), "E_TRANSACTION_FIXTURE_NOT_NORMALIZED_CLEAN")
        require(not index_worktree_raw_equal(repository, "sample.txt"),
                "E_TRANSACTION_RAW_MISMATCH_NOT_DETECTED")
    return 2


def core(matrix: dict[str, Any], runtime: dict[str, Any], step71: dict[str, Any]) -> dict[str, int]:
    n1, d1 = traverse(matrix); n2, d2 = traverse(runtime)
    check_exact_schema(matrix, runtime)
    check_runtime(runtime)
    check_matrix(matrix, runtime, step71)
    check_documents()
    ast_nodes = check_source_policy()
    output_boundary = check_output_boundary()
    temporary_link_boundary = check_temporary_link_boundary()
    transaction_cases = transaction_negatives()
    return {"json_nodes": n1 + n2, "max_depth": max(d1, d2),
            "ast_nodes": ast_nodes, "output_boundary": output_boundary,
            "temporary_link_boundary": temporary_link_boundary,
            "transaction_cases": transaction_cases}


def schema_negatives(matrix: dict[str, Any], runtime: dict[str, Any]) -> int:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
        ("matrix", lambda x: x.__setitem__("unexpected", False), "E_MATRIX_SCHEMA_FINGERPRINT"),
        ("matrix", lambda x: x["routes"][0].__setitem__("unexpected", False), "E_MATRIX_SCHEMA_FINGERPRINT"),
        ("runtime", lambda x: x["official_runs"][0].__setitem__("unexpected", False), "E_RUNTIME_SCHEMA_FINGERPRINT"),
        ("runtime", lambda x: x["route_runs"][0]["observations"].__setitem__("unexpected", False), "E_RUNTIME_SCHEMA_FINGERPRINT"),
    ]
    for target, mutation, code in cases:
        candidate_matrix, candidate_runtime = copy.deepcopy(matrix), copy.deepcopy(runtime)
        mutation(candidate_matrix if target == "matrix" else candidate_runtime)
        try:
            check_exact_schema(candidate_matrix, candidate_runtime)
        except ValidationError as exc:
            require(code in str(exc), "E_SCHEMA_NEGATIVE_WRONG_FAILURE", f"expected {code}, got {exc}")
            continue
        fail("E_SCHEMA_NEGATIVE_ACCEPTED", code)
    return len(cases)


def expect_failure(base_matrix: dict[str, Any], base_runtime: dict[str, Any], step71: dict[str, Any],
                   target: str, mutate: Callable[[dict[str, Any]], None], code: str) -> None:
    matrix, runtime = copy.deepcopy(base_matrix), copy.deepcopy(base_runtime)
    obj = matrix if target == "matrix" else runtime
    mutate(obj)
    obj["semantic_sha256"] = semantic_hash(obj)
    try:
        check_runtime(runtime); check_matrix(matrix, runtime, step71)
    except ValidationError as exc:
        require(code in str(exc), "E_NEGATIVE_WRONG_FAILURE", f"expected {code}, got {exc}")
        return
    fail("E_NEGATIVE_ACCEPTED", code)


def rehash_run_input(row: dict[str, Any], manifest_hash: str) -> None:
    input_obj = {"runtime": row["runtime"], "command": row["command"], "cwd": row["cwd"],
                 "materialized_manifest_sha256": manifest_hash,
                 "controller_probe_sha256": sha256(extract_probe_source().encode()),
                 "fixture_id": row["fixture_id"], "source_root": row["source_root"]}
    row["input_sha256"] = sha256(compact(input_obj))


def mutate_base_relative_path(runtime: dict[str, Any]) -> None:
    isolation = runtime["isolation"]
    isolation["materialized_manifest"][0]["materialized_relative_path"] = "FAKE_BASE_SOURCE.py"
    manifest_hash = sha256(compact(isolation["materialized_manifest"]))
    isolation["materialized_manifest_sha256"] = manifest_hash
    expected_files = sorted(row["materialized_relative_path"]
                            for row in isolation["materialized_manifest"])
    isolation["fixture_files_before"] = expected_files
    isolation["fixture_files_after"] = copy.deepcopy(expected_files)
    for row in runtime["runtime_environments"] + runtime["official_runs"]:
        rehash_run_input(row, manifest_hash)


def mutate_route_relative_path(runtime: dict[str, Any]) -> None:
    row = runtime["route_runs"][0]
    row["fixture_manifest"][0]["materialized_relative_path"] = "FAKE_ROUTE_SOURCE.py"
    route_input = {"sources": row["fixture_manifest"],
                   "probe_program_sha256": sha256(extract_probe_source().encode())}
    route_hash = sha256(compact(route_input))
    row["fixture_input_manifest_sha256"] = route_hash
    row["source_before_sha256"] = route_hash
    row["source_after_sha256"] = route_hash
    expected_files = sorted([*(source["materialized_relative_path"]
                               for source in row["fixture_manifest"]),
                             "step73_route_probe.py"])
    row["fixture_files_before"] = expected_files
    row["fixture_files_after"] = copy.deepcopy(expected_files)
    rehash_run_input(row, route_hash)


def mutate_environment_source_root(runtime: dict[str, Any]) -> None:
    row = runtime["runtime_environments"][0]
    row["source_root"] = "<TMP>/route_fixtures/FAKE"
    rehash_run_input(row, runtime["isolation"]["materialized_manifest_sha256"])


def mutate_official_source_root(runtime: dict[str, Any]) -> None:
    row = runtime["official_runs"][0]
    row["source_root"] = "<TMP>/route_fixtures/FAKE"
    rehash_run_input(row, runtime["isolation"]["materialized_manifest_sha256"])


def rehash_run_output(row: dict[str, Any]) -> None:
    row["stdout_sha256"] = sha256(row["stdout"].encode())
    row["stderr_sha256"] = sha256(row["stderr"].encode())
    output = {"exit_code": row["exit_code"], "stdout": row["stdout"],
              "stderr": row["stderr"]}
    row["output_sha256"] = sha256(compact(output))


def mutate_environment_exit(runtime: dict[str, Any]) -> None:
    row = runtime["runtime_environments"][0]
    row["exit_code"] = row["expected_exit_code"] = 9
    rehash_run_output(row)


def mutate_official_exit(runtime: dict[str, Any]) -> None:
    row = runtime["official_runs"][0]
    row["exit_code"] = row["expected_exit_code"] = 9
    rehash_run_output(row)


def mutate_runtime_identity(runtime: dict[str, Any], *, python: str | None = None,
                            numpy: str | None = None) -> None:
    runtime_id = "3.12"
    environment = next(row for row in runtime["runtime_environments"]
                       if row["runtime"] == runtime_id)
    python_value = python if python is not None else environment["python_version"]
    numpy_value = numpy if numpy is not None else environment["numpy_version"]
    environment["python_version"] = python_value
    environment["interpreter"] = python_value
    environment["numpy_version"] = numpy_value
    environment["observations"] = {"python_version": python_value,
                                   "numpy_version": numpy_value}
    environment["stdout"] = f"{python_value}\n{numpy_value}\n"
    rehash_run_output(environment)
    for row in runtime["official_runs"] + runtime["route_runs"]:
        if row["runtime"] == runtime_id:
            row["interpreter"] = python_value
            row["numpy_version"] = numpy_value


def mutate_route_claim(runtime: dict[str, Any], route: str,
                       mutate: Callable[[dict[str, Any]], None]) -> None:
    rows = [row for row in runtime["route_runs"]
            if row["mutation"] == "none" and row["route"] == route]
    for row in rows:
        mutate(row["observations"])
        payload = {"route": route, "mutation": "none", "result": row["observations"]}
        row["stdout"] = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":"), allow_nan=False) + "\n"
        rehash_run_output(row)
    by_runtime = {runtime_id: sha256(compact(next(
        row["observations"] for row in rows if row["runtime"] == runtime_id)))
        for runtime_id in ("3.12", "3.14")}
    for control in runtime["changed_order_controls"]:
        if control["route"] == route:
            value = by_runtime[control["runtime"]]
            control["order_A_output_sha256"] = value
            control["order_B_output_sha256"] = value


def mutate_official_output(runtime: dict[str, Any]) -> None:
    row = runtime["official_runs"][0]
    row["stdout"] = "FORGED OFFICIAL PASS\n"
    rehash_run_output(row)


def semantic_negatives(matrix: dict[str, Any], runtime: dict[str, Any], step71: dict[str, Any]) -> int:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
        ("matrix", lambda x: x["routes"].pop(), "E_ROUTE_COUNT"),
        ("matrix", lambda x: x["routes"].append(copy.deepcopy(x["routes"][0])), "E_ROUTE_COUNT"),
        ("matrix", lambda x: x["routes"][0].__setitem__("own_fixture", False), "E_ROUTE_INDEPENDENCE"),
        ("matrix", lambda x: x["routes"][0].__setitem__("outcome", "GROUND_NOT_FOUND"), "E_FRESH_OUTCOME"),
        ("matrix", lambda x: x["routes"][2].__setitem__("outcome", "IMPLEMENTED_AND_OBSERVED"), "E_LEGACY_OUTCOME"),
        ("matrix", lambda x: x["routes"][2].__setitem__("passing_behavior_route", True), "E_LEGACY_PASS"),
        ("matrix", lambda x: x["routes"][0].__setitem__("process_run_ids", ["FAKE-A", "FAKE-B", "FAKE-C", "FAKE-D"]), "E_ROUTE_RELATION"),
        ("matrix", lambda x: x["routes"][2].__setitem__("absence_corroboration_run_ids", ["FAKE-A", "FAKE-B", "FAKE-C", "FAKE-D"]), "E_ROUTE_RELATION"),
        ("matrix", lambda x: x["routes"][1].__setitem__("mutation_run_ids", ["FAKE-A", "FAKE-B"]), "E_ROUTE_RELATION"),
        ("matrix", lambda x: x["exact_initialization_mapping"][0].__setitem__("restore_key", "state"), "E_INITIALIZATION_MAP"),
        ("matrix", lambda x: x["exact_profile_mapping"][0].__setitem__("profile_id", "FAKE"), "E_PROFILE_MAP"),
        ("matrix", lambda x: x["profile_runtime_routes"].pop(), "E_PROFILE_ROUTE_COUNT"),
        ("matrix", lambda x: x["profile_runtime_routes"][0].__setitem__("ast_sha256", "0" * 64), "E_PROFILE_ROUTE_RELATION"),
        ("matrix", lambda x: x["profile_runtime_routes"][0].__setitem__("public_route", "FAKE"), "E_PROFILE_ROUTE_RELATION"),
        ("matrix", lambda x: x["runtime_attestation_binding"].__setitem__("semantic_sha256", "0" * 64), "E_RUNTIME_BINDING"),
        ("matrix", lambda x: x["runtime_attestation_binding"].__setitem__("gate", "FAKE"), "E_RUNTIME_GATE_BINDING"),
        ("matrix", lambda x: x["consumed_step71"].__setitem__("gate", "FAKE"), "E_STEP71_GATE"),
        ("matrix", lambda x: x["result_first_contract"].__setitem__("containing_commit", "FAKE_PERSISTED"), "E_RESULT_FIRST_CONTRACT"),
        ("matrix", lambda x: x["source_policy"].__setitem__("invented_restoration_loader_forbidden", False), "E_SOURCE_POLICY"),
        ("matrix", lambda x: x["feature_observation_owners"].__setitem__("current_saved_state_key_presence", "kernel"), "E_FEATURE_OWNERS"),
        ("matrix", lambda x: x["feature_observation_owners"].__setitem__("seconds_hour", "FAKE"), "E_FEATURE_OWNERS"),
        ("matrix", lambda x: x.__setitem__("generated_date", "1900-01-01"), "E_GENERATED_DATE"),
        ("matrix", lambda x: x["authority_boundary"].__setitem__("scientific_truth", True), "E_AUTHORITY"),
        ("matrix", lambda x: x["authority_boundary"].__setitem__("internal_runtime_behavior", False), "E_AUTHORITY_BINDING"),
        ("runtime", lambda x: x["isolation"].__setitem__("working_checkout_source_imported", True), "E_ISOLATION_NEGATIVE"),
        ("runtime", lambda x: x["isolation"].__setitem__("network_requested", True), "E_ISOLATION_NEGATIVE"),
        ("runtime", lambda x: x.__setitem__("generated_date", "1900-01-01"), "E_GENERATED_DATE"),
        ("runtime", lambda x: x["result_first_contract"].__setitem__("containing_commit", "FAKE_PERSISTED"), "E_RESULT_FIRST_CONTRACT"),
        ("runtime", lambda x: x["runtime_environments"][1].__setitem__("run_id", "FAKE"), "E_ENV_TOPOLOGY"),
        ("runtime", mutate_environment_source_root, "E_ENV_TOPOLOGY"),
        ("runtime", mutate_environment_exit, "E_ENV_EXIT_ZERO"),
        ("runtime", lambda x: mutate_runtime_identity(x, python="9.99.0"), "E_ENV_LIVE_IDENTITY"),
        ("runtime", lambda x: mutate_runtime_identity(x, numpy="NOT_NUMPY"), "E_ENV_LIVE_IDENTITY"),
        ("runtime", lambda x: x["official_runs"].__setitem__(slice(None), [copy.deepcopy(x["official_runs"][0]) for _ in range(10)]), "E_OFFICIAL_TOPOLOGY"),
        ("runtime", mutate_official_source_root, "E_OFFICIAL_TOPOLOGY"),
        ("runtime", mutate_official_exit, "E_OFFICIAL_EXIT_ZERO"),
        ("runtime", mutate_official_output, "E_OFFICIAL_OUTPUT_PIN"),
        ("runtime", lambda x: x["route_runs"].pop(), "E_ROUTE_RUN_COUNT"),
        ("runtime", mutate_base_relative_path, "E_MANIFEST_RELATIVE_PATHS"),
        ("runtime", mutate_route_relative_path, "E_ROUTE_MANIFEST_RELATIVE_PATHS"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("exit_code", 3), "E_RUN_EXIT"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("stdout", "tampered"), "E_STDOUT_HASH"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("input_sha256", "0" * 64), "E_INPUT_HASH"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("command", ["python"]), "E_RUNTIME_FLAGS"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("interpreter", "FAKE"), "E_RUN_ENV_BINDING"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("authority", "EXTERNAL_SCIENTIFIC_TRUTH"), "E_ROUTE_AUTHORITY"),
        ("runtime", lambda x: x["runtime_environments"][0].__setitem__("authority", "EXTERNAL_SCIENTIFIC_TRUTH"), "E_ENV_AUTHORITY"),
        ("runtime", lambda x: x["official_runs"][0].__setitem__("interpreter", "FAKE"), "E_RUN_ENV_BINDING"),
        ("runtime", lambda x: x["changed_order_controls"][0].__setitem__("normalized_observations_equal", False), "E_ORDER_RELATION"),
        ("runtime", lambda x: x["changed_order_controls"][0].__setitem__("runtime", "FAKE"), "E_ORDER_RELATION"),
        ("runtime", lambda x: (x["route_runs"][0].__setitem__("position", 2), x["route_runs"][1].__setitem__("position", 1)), "E_NORMAL_TOPOLOGY"),
        ("runtime", lambda x: next(r for r in x["route_runs"] if r["mutation"] != "none").__setitem__("order_id", "A"), "E_MUTATION_TOPOLOGY"),
        ("runtime", lambda x: x["route_runs"][0]["observations"].__setitem__("pass", False), "E_ROUTE_OBSERVATION_PIN"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("source_unchanged", False), "E_ROUTE_SOURCE_IMMUTABLE"),
        ("runtime", lambda x: (x["isolation"]["fixture_files_before"].__setitem__(0, "FAKE"), x["isolation"]["fixture_files_after"].__setitem__(0, "FAKE")), "E_FIXTURE_FILE_SET_EXACT"),
        ("runtime", lambda x: (x["route_runs"][0]["fixture_files_before"].__setitem__(0, "FAKE"), x["route_runs"][0]["fixture_files_after"].__setitem__(0, "FAKE")), "E_ROUTE_FIXTURE_FILES_EXACT"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("fixture_id", x["route_runs"][1]["fixture_id"]), "E_FIXTURE_ID_UNIQUE"),
        ("runtime", lambda x: x["route_runs"][0].__setitem__("gate", "PASS_ABSENCE_CORROBORATION"), "E_ROUTE_GATE"),
        ("runtime", lambda x: mutate_route_claim(x, "fresh", lambda o: o.__setitem__("Q_Si", 999.0)), "E_ROUTE_OBSERVATION_PIN"),
        ("runtime", lambda x: mutate_route_claim(x, "explicit", lambda o: o["kernel"].__setitem__("named_profiles_select_regsol", True)), "E_ROUTE_OBSERVATION_PIN"),
        ("runtime", lambda x: mutate_route_claim(x, "legacy", lambda o: o.__setitem__("actual_restoration_path", "FORGED_IMPLEMENTED")), "E_ROUTE_OBSERVATION_PIN"),
        ("runtime", lambda x: x["route_runs"][0]["fixture_files_after"].append("escape"), "E_ROUTE_FIXTURE_FILES"),
        ("runtime", lambda x: x["runtime_environments"][0]["observations"].__setitem__("python_version", "FAKE"), "E_ENV_OBSERVATION"),
        ("runtime", lambda x: x["official_runs"][0]["observations"].__setitem__("exit_zero", False), "E_OFFICIAL_OBSERVATION"),
        ("runtime", lambda x: next(r for r in x["route_runs"] if r["mutation"] != "none")["observations"].__setitem__("actual_exit", 8), "E_ROUTE_OBSERVATION_PIN"),
        ("runtime", lambda x: next(r for r in x["route_runs"] if r["mutation"] != "none").__setitem__("mutation_probe", {"enabled": False, "mutation_id": "FAKE", "detected": False}), "E_MUTATION_PROBE"),
        ("runtime", lambda x: x["isolation"].__setitem__("unexpected_fixture_files", ["escape"]), "E_FIXTURE_FILE_SET"),
        ("runtime", lambda x: x["counts"].__setitem__("mutations_detected", 5), "E_RUNTIME_COUNTS"),
        ("runtime", lambda x: x["authority_boundary"].__setitem__("publication_readiness", True), "E_RUNTIME_AUTHORITY"),
    ]
    for target, mutation, code in cases:
        expect_failure(matrix, runtime, step71, target, mutation, code)
    return len(cases)


def determinism() -> tuple[str, str]:
    outputs = []
    with tempfile.TemporaryDirectory(prefix="p065_step73_validate_a_") as a, tempfile.TemporaryDirectory(prefix="p065_step73_validate_b_") as b:
        for directory in (a, b):
            cp = run((sys.executable, "-B", "-I", "-X", "utf8", str(BUILDER_PATH), "--output-dir", directory), timeout=900)
            require(b"PASS_P065_STEP73_BUILD" in cp.stdout, "E_BUILD_TERMINAL")
            outputs.append((Path(directory) / MATRIX_PATH.name).read_bytes())
            outputs.append((Path(directory) / RUNTIME_PATH.name).read_bytes())
    require(outputs[0] == outputs[2] and outputs[1] == outputs[3], "E_DETERMINISM")
    require(outputs[0] == MATRIX_PATH.read_bytes(), "E_DETERMINISM_STAGED_MATRIX")
    require(outputs[1] == RUNTIME_PATH.read_bytes(), "E_DETERMINISM_STAGED_RUNTIME")
    return sha256(outputs[0]), sha256(outputs[1])


def git_controls(mode: str, expected_commit: str | None) -> None:
    branch = run(("git", "branch", "--show-current")).stdout.decode().strip()
    require(branch == BRANCH, "E_GIT_BRANCH", branch)
    upstream_name = run(("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name",
                         "@{upstream}")).stdout.decode().strip()
    require_upstream_name(upstream_name)
    protected = run(("git", "rev-parse", "codex/lib-physics-endgame-v1025_2")).stdout.decode().strip()
    protected_remote = run(("git", "rev-parse", "origin/codex/lib-physics-endgame-v1025_2")).stdout.decode().strip()
    main = run(("git", "rev-parse", "origin/main")).stdout.decode().strip()
    require(protected == "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71", "E_PROTECTED_PIN")
    require(protected_remote == protected, "E_PROTECTED_REMOTE_PIN")
    require(main == "4069cb36a8a52b1b88c29d68aa54dcbe915b1618", "E_MAIN_PIN")
    require_live_ref("refs/heads/codex/lib-physics-endgame-v1025_2", protected,
                     "E_PROTECTED_LIVE")
    require_live_ref("refs/heads/main", main, "E_MAIN_LIVE")
    if mode == "staged":
        head = run(("git", "rev-parse", "HEAD")).stdout.decode().strip()
        require(head == EXPECTED_PARENT, "E_STAGED_PARENT", head)
        staged = sorted(run(("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR")).stdout.decode().splitlines())
        require(staged == EXACT_PATHS, "E_STAGED_PATHS", repr(staged))
        require(not run(("git", "diff", "--name-only")).stdout.decode().splitlines(), "E_UNSTAGED_REPOSITORY")
        status = run(("git", "status", "--porcelain=v1", "--untracked-files=all")).stdout.decode().splitlines()
        require(len(status) == len(EXACT_PATHS) and all(len(row) >= 4 and row[0] in {"A", "M"} and row[1] == " " for row in status), "E_STAGED_STATUS", repr(status))
        require(sorted(row[3:] for row in status) == EXACT_PATHS, "E_STAGED_STATUS_PATHS")
        require(run(("git", "diff", "--cached", "--check"), check=False).returncode == 0, "E_STAGED_DIFF_CHECK")
        for path in EXACT_PATHS:
            require(index_worktree_raw_equal(ROOT, path), "E_STAGED_RAW_BYTES", path)
        upstream = run(("git", "rev-parse", "@{upstream}")).stdout.decode().strip()
        require(upstream == EXPECTED_PARENT, "E_STAGED_UPSTREAM")
        require_live_ref(f"refs/heads/{BRANCH}", EXPECTED_PARENT,
                         "E_STAGED_LIVE_BRANCH")
        require(not run(("git", "diff", "--name-only", protected, head, "--", "Claude")).stdout.decode().splitlines(), "E_CLAUDE_DRIFT")
        return
    require(expected_commit is not None, "E_EXPECTED_COMMIT")
    head = run(("git", "rev-parse", "HEAD")).stdout.decode().strip()
    require(head == expected_commit, "E_PERSIST_HEAD")
    require(run(("git", "rev-parse", f"{head}^")).stdout.decode().strip() == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(run(("git", "show", "-s", "--format=%s", head)).stdout.decode().strip() == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT")
    changed = sorted(run(("git", "diff-tree", "--no-commit-id", "--name-only", "-r", head)).stdout.decode().splitlines())
    require(changed == EXACT_PATHS, "E_COMMIT_PATHS")
    upstream = run(("git", "rev-parse", "@{upstream}")).stdout.decode().strip()
    require(upstream == head, "E_UPSTREAM")
    require_live_ref(f"refs/heads/{BRANCH}", head, "E_LIVE_REMOTE")
    require(not run(("git", "status", "--porcelain")).stdout.decode().splitlines(), "E_DIRTY")
    require(not run(("git", "diff", "--name-only", protected, head, "--", "Claude")).stdout.decode().splitlines(), "E_CLAUDE_DRIFT")
    for path in EXACT_PATHS:
        require(git_bytes(head, path) == (ROOT / path).read_bytes(), "E_PERSIST_BYTES", path)


def main() -> int:
    ap = argparse.ArgumentParser()
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--staged", action="store_true")
    modes.add_argument("--persistence", action="store_true")
    ap.add_argument("--expected-commit")
    args = ap.parse_args()
    mode = "persistence" if args.persistence else "staged" if args.staged else "content"
    matrix = strict_load_bytes(MATRIX_PATH.read_bytes())
    runtime = strict_load_bytes(RUNTIME_PATH.read_bytes())
    step71 = strict_load_bytes(STEP71_PATH.read_bytes())
    metrics = core(matrix, runtime, step71)
    schema_cases = schema_negatives(matrix, runtime)
    negatives = semantic_negatives(matrix, runtime, step71)
    matrix_raw, runtime_raw = determinism()
    if mode != "content": git_controls(mode, args.expected_commit)
    terminal = PASS_PERSISTENCE if mode == "persistence" else PASS_CONTENT
    print(f"{terminal} mode={mode} json_nodes={metrics['json_nodes']} depth={metrics['max_depth']} "
          f"ast_nodes={metrics['ast_nodes']} schema_cases={schema_cases} semantic_cases={negatives} "
          f"output_boundary={metrics['output_boundary']}/1 "
          f"temporary_link_boundary={metrics['temporary_link_boundary']}/1 "
          f"transaction_cases={metrics['transaction_cases']} determinism=2/2 "
          f"matrix_raw={matrix_raw} runtime_raw={runtime_raw}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValidationError as exc:
        print(f"FAIL_P065_STEP73 {exc}", file=sys.stderr)
        sys.exit(1)
