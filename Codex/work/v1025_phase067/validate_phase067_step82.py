from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "8975d6a6cc46686e38249b7971b5535dfa414a8b"
EXPECTED_SUBJECT = "audit(phase067): freeze complete python topology"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P067_STEP82_SOURCE_TOPOLOGY"
PERSISTENCE = "PASS_P067_STEP82_PERSISTENCE"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "39265a695fa48a74bee5d85c4a81ae6c8f6768c4f2842aa0f39ce58391ee9270"
BUILDER_SOURCE_POLICY_SHA256_LF = "d30216fc9613aa41bc4aa4feac03421a5c4bb844e40d14030824f68db0066ea3"

MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step82.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step82.py"
INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_082_SOURCE_TOPOLOGY_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
CONTROL_DOCUMENT_SHA256 = {
    RESULT_PATH: "63eb4c9de0bf3af6745f9c7347f87ce1a711b9c864c3abea62c263f6a1f4522f",
    PARENT_LEDGER_PATH: "2d7a2724b6c4e96d87a46ceaed924031eb294a29c495937c6e7d1d0f7d4a1709",
    ACTIVE_LEDGER_PATH: "69ca91c1feccce7a53c390dfe0e725a0788ea75e923d2c56909c4de902c53812",
    HANDOVER_PATH: "fbd4674569365c110215f7a48d18f9d5c0fbe36ec816f00426238acd18f5d628",
}

FINAL_PATHS = [BUILDER_PATH, VALIDATOR_PATH, INVENTORY_PATH, ATTESTATION_PATH,
               RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH]
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {path: ("A" if index < 5 else "M") for index, path in enumerate(FINAL_PATHS)}
MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
PATH_MEMBERSHIP_SHA256 = "d64fe6b430120820da6ee00a82a3fc9679b885a2c3accd4e0e9b04dced24dfe4"
PATH_BLOB_MEMBERSHIP_SHA256 = "bae10035780580c9caa629d59050f307b492e6c5e75941252aca30eadbbc981f"
BLOB_MEMBERSHIP_SHA256 = "e4e11ba47910647bcc0a0e4fd4e8918fbe2f08c75fd23fefd88fb04e8e96c066"
RELEASE_MEMBERSHIP_SHA256 = "2ccc032ffeb3d9c4b449fbce48bd66448c8324fe96d4065067d8d755127a209c"
PARTITION_MEMBERSHIP = {
    "A": "df7d7d6f4fa41a7edfb34d07cf5278352a970725858174eef773fb849a0ed812",
    "B": "2b4f335a83be768012de9575e6a49ccaca667e4bb65b671a4841d8aa85517ebd",
    "C": "16cc2650c58da37b054d5b0eaac285affce3a901a95da260848ce3f3d229dc8d",
}
PARTITION_CONTRACT = (
    {"partition": "A", "reviewer": "p067_activation_impl",
     "review_batch": "P067-S82-A-READ-FULL", "first": 1, "last": 28,
     "blobs": 28, "lines": 8862, "membership_sha256": PARTITION_MEMBERSHIP["A"],
     "review_evidence_sha256": "ab76566e1266853d0556f7f83055ac2d0a8317e014c10070c66e5e41fefbe6b3"},
    {"partition": "B", "reviewer": "p066_s76_manifest",
     "review_batch": "P067-S82-B-SUPPORT-FINAL", "first": 29, "last": 56,
     "blobs": 28, "lines": 11050, "membership_sha256": PARTITION_MEMBERSHIP["B"],
     "review_evidence_sha256": "be9c06a0894514dc30c0bc601fcc91b9939522588c544d88a5171d5431121c55"},
    {"partition": "C", "reviewer": "p066_s76_routes",
     "review_batch": "P067-S82-C-SUPPORT-FINAL", "first": 57, "last": 84,
     "blobs": 28, "lines": 10040, "membership_sha256": PARTITION_MEMBERSHIP["C"],
     "review_evidence_sha256": "341134e64337dd5e1292e5fcc2bf8dfd6535276cd5dd1662ee9b10cce16288a4"},
)
INVENTORY_VALIDATION = {"ambiguous_relations_inferred": 0, "duplicate_occurrences": 0,
                        "orphan_blobs": 0, "orphan_occurrences": 0,
                        "parser_failures": 0, "unread_blobs": 0}
ATTESTATION_VALIDATION = {"authority_promotions": 0, "blob_hash_mismatch": 0,
                          "genealogy_unbound": 0, "line_extent_mismatch": 0,
                          "occurrence_projection_orphans": 0, "partition_gap": 0,
                          "partition_overlap": 0}
RELEASE_ROOTS = tuple(f"Claude/docs/{version}" for version in (
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14", "v1.0.15",
    "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2", "v1.0.19", "v1.0.20",
    "v1.0.21", "v1.0.22", "v1.0.23", "v1.0.24", "v1.0.24.1", "v1.0.25",
    "v1.0.25.1", "v1.0.25.2"))


class ValidationFailure(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationFailure(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone["semantic_sha256"] = ""
    return sha256(canonical_bytes(clone))


def membership_hash(values: list[str]) -> str:
    return sha256("".join(value + "\n" for value in values).encode("utf-8"))


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def _constant(token: str) -> None:
    raise ValidationFailure("E_JSON_NONFINITE", token)


def walk_json(value: Any, depth: int = 0) -> tuple[int, int]:
    require(depth <= 64, "E_JSON_DEPTH")
    if isinstance(value, dict):
        counts = [walk_json(nested, depth + 1) for nested in value.values()]
    elif isinstance(value, list):
        require(len(value) <= 20000, "E_JSON_ARRAY")
        counts = [walk_json(nested, depth + 1) for nested in value]
    else:
        if isinstance(value, float):
            require(math.isfinite(value), "E_JSON_NONFINITE")
        require(value is None or isinstance(value, (str, int, float, bool)), "E_JSON_TYPE")
        return 1, depth
    return 1 + sum(item[0] for item in counts), max([depth, *(item[1] for item in counts)])


def strict_load(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    require(len(raw) <= 100_000_000, "E_JSON_SIZE", label)
    require(raw == lf_bytes(raw) and raw.endswith(b"\n") and not raw.startswith(b"\xef\xbb\xbf"),
            "E_JSON_BYTES", label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationFailure("E_JSON_PARSE", f"{label}:{error}") from error
    require(isinstance(value, dict), "E_JSON_ROOT", label)
    nodes, depth = walk_json(value)
    require(canonical_bytes(value) == raw, "E_JSON_CANONICAL", label)
    require(value.get("semantic_sha256") == semantic_hash(value), "E_JSON_SEMANTIC", label)
    return value, nodes, depth


def strict_source_manifest_load(raw: bytes) -> dict[str, Any]:
    require(raw == lf_bytes(raw) and raw.endswith(b"\n") and
            not raw.startswith(b"\xef\xbb\xbf"), "E_MANIFEST_BYTES")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationFailure("E_MANIFEST_PARSE", str(error)) from error
    require(isinstance(value, dict), "E_MANIFEST_ROOT")
    walk_json(value)
    return value


def neutralized_source(raw: bytes, constant: str) -> bytes:
    pattern = re.compile(rb'(?m)^' + re.escape(constant.encode()) + rb' = "[0-9a-f]{64}"$')
    updated, count = pattern.subn(constant.encode() + b' = "' + b"0" * 64 + b'"', raw)
    require(count == 1, "E_SOURCE_POLICY_PIN", constant)
    return updated


def source_policy_errors(source: str, kind: str) -> list[str]:
    tree = ast.parse(source)
    errors: list[str] = []
    allowed_imports = {"__future__", "argparse", "ast", "collections", "copy", "hashlib",
                       "json", "math", "os", "pathlib", "re", "subprocess",
                       "types", "typing"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                if item.name.split(".", 1)[0] not in allowed_imports:
                    errors.append(f"IMPORT:{item.name}:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".", 1)[0] not in allowed_imports:
                errors.append(f"IMPORT_FROM:{node.module}:{node.lineno}")
        elif isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else (
                node.func.attr if isinstance(node.func, ast.Attribute) else "")
            identity = expression_name(node.func)
            if ((isinstance(node.func, ast.Name) and name in
                 {"eval", "exec", "compile", "__import__", "input", "open"}) or
                    identity in {"importlib.util.spec_from_file_location", "spec.loader.exec_module"}):
                errors.append(f"CALL:{name}:{node.lineno}")
            if name == "run":
                owner = next((parent.name for parent in ast.walk(tree)
                              if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                              node in set(ast.walk(parent))), "")
                if owner not in {"run_git", "git"}:
                    errors.append(f"PROCESS:{owner}:{node.lineno}")
            if name in {"write_text", "write_bytes", "unlink"} or identity == "os.replace":
                owner = next((parent.name for parent in ast.walk(tree)
                              if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                              node in set(ast.walk(parent))), "")
                if not (kind == "builder" and owner == "atomic_collect"):
                    errors.append(f"WRITE:{owner}:{name}:{node.lineno}")
        elif isinstance(node, ast.Attribute) and node.attr in {"Popen", "system", "popen", "urlopen"}:
            errors.append(f"ATTRIBUTE:{node.attr}:{node.lineno}")
    return sorted(set(errors))


def verify_source_policy() -> None:
    builder_raw = (ROOT / BUILDER_PATH).read_bytes()
    validator_raw = (ROOT / VALIDATOR_PATH).read_bytes()
    require(not source_policy_errors(builder_raw.decode("utf-8"), "builder"), "E_BUILDER_POLICY")
    require(not source_policy_errors(validator_raw.decode("utf-8"), "validator"), "E_VALIDATOR_POLICY")
    require(sha256(neutralized_source(builder_raw, "BUILDER_SOURCE_POLICY_SHA256_LF")) ==
            BUILDER_SOURCE_POLICY_SHA256_LF, "E_BUILDER_POLICY_HASH")
    require(sha256(neutralized_source(validator_raw, "VALIDATOR_SOURCE_POLICY_SHA256_LF")) ==
            VALIDATOR_SOURCE_POLICY_SHA256_LF, "E_VALIDATOR_POLICY_HASH")


def validate_git_argv(args: tuple[str, ...]) -> None:
    require(args, "E_GIT_EMPTY")
    verb = args[0]
    allowed = False
    if verb == "cat-file":
        allowed = len(args) == 3 and args[1] == "blob" and (
            re.fullmatch(r"[0-9a-f]{40}", args[2]) is not None or
            re.fullmatch(r"[0-9a-f]{40}:[^\r\n]+", args[2]) is not None)
    elif verb == "rev-parse":
        allowed = args in {("rev-parse", "HEAD"), ("rev-parse", UPSTREAM),
                           ("rev-parse", f"refs/remotes/{UPSTREAM}"),
                           ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
                           ("rev-parse", "refs/remotes/origin/main")} or (
            len(args) == 2 and re.fullmatch(r"[0-9a-f]{40}\^", args[1]) is not None) or (
            args == ("rev-parse", "--abbrev-ref", "HEAD")) or (
            args == ("rev-parse", "--abbrev-ref", "@{upstream}"))
    elif verb == "show":
        allowed = ((len(args) == 2 and (args[1].startswith(":") or
                    re.fullmatch(r"[0-9a-f]{40}:[^\r\n]+", args[1]))) or
                   (len(args) == 4 and args[1] == "-s" and
                    args[2] in {"--format=%s", "--format=%P"} and
                    re.fullmatch(r"[0-9a-f]{40}", args[3])) or
                   (len(args) == 4 and args[1:3] == ("-s", "--format=%H%x00%P%x00%T%x00%aI%x00%cI%x00%s") and
                    re.fullmatch(r"[0-9a-f]{40}", args[3])))
    elif verb == "ls-tree":
        allowed = ((len(args) == 3 and args[1] == "-r" and re.fullmatch(r"[0-9a-f]{40}", args[2])) or
                   (len(args) >= 4 and re.fullmatch(r"[0-9a-f]{40}", args[1]) and args[2] == "--" and
                    all(not path.startswith("-") and "\n" not in path and "\r" not in path for path in args[3:])))
    elif verb == "rev-list":
        prefix = ("rev-list", "--full-history", "--reverse", "--topo-order", BASELINE, "--")
        allowed = args[:len(prefix)] == prefix and args[len(prefix):] == tuple(
            f"Claude/docs/{version}" for version in (
                "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14", "v1.0.15",
                "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2", "v1.0.19", "v1.0.20",
                "v1.0.21", "v1.0.22", "v1.0.23", "v1.0.24", "v1.0.24.1", "v1.0.25",
                "v1.0.25.1", "v1.0.25.2"))
    elif verb == "status":
        allowed = args in {("status", "--porcelain=v1", "--untracked-files=all"),
                           ("status", "--porcelain")}
    elif verb == "diff":
        allowed = args in {("diff", "--name-only"), ("diff", "--cached", "--check"),
                           ("diff", "--cached", "--name-status", "--no-renames", "HEAD")} or (
            args == ("diff", "--name-only", PROTECTED_TIP, "--", "Claude"))
    elif verb == "diff-tree":
        persistence = (len(args) == 7 and args[1:5] ==
                       ("--no-commit-id", "--name-status", "--no-renames", "-r") and
                       re.fullmatch(r"[0-9a-f]{40}\^", args[5]) is not None and
                       re.fullmatch(r"[0-9a-f]{40}", args[6]) is not None)
        roots = tuple(f"Claude/docs/{version}" for version in (
            "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14", "v1.0.15",
            "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2", "v1.0.19", "v1.0.20",
            "v1.0.21", "v1.0.22", "v1.0.23", "v1.0.24", "v1.0.24.1", "v1.0.25",
            "v1.0.25.1", "v1.0.25.2"))
        common = ("-r", "--raw", "--abbrev=40", "-M", "-C", "--find-copies-harder")
        history = ((len(args) == 10 + len(roots) and args[1:7] == common and
                    re.fullmatch(r"[0-9a-f]{40}", args[7]) is not None and
                    re.fullmatch(r"[0-9a-f]{40}", args[8]) is not None and
                    args[9] == "--" and args[10:] == roots) or
                   (len(args) == 10 + len(roots) and args[1] == "--root" and
                    args[2:8] == common and re.fullmatch(r"[0-9a-f]{40}", args[8]) is not None and
                    args[9] == "--" and args[10:] == roots))
        allowed = persistence or history
    elif verb == "ls-files":
        allowed = args in {("ls-files", "--others", "--exclude-standard"), ("ls-files", "-s")}
    elif verb == "show-ref":
        allowed = args in {("show-ref", "--verify", "--hash",
                            "refs/heads/codex/lib-physics-endgame-v1025_2"),
                           ("show-ref", "--verify", "--hash", "refs/heads/main")}
    elif verb == "ls-remote":
        allowed = (args == ("ls-remote", "--get-url", "origin") or
                   (len(args) == 4 and args[1:3] == ("--heads", "origin") and
                    args[3] in {f"refs/heads/{BRANCH}",
                                "refs/heads/codex/lib-physics-endgame-v1025_2", "refs/heads/main"}))
    require(allowed, "E_GIT_ARGV", repr(args))


def git(*args: str, binary: bool = False, check: bool = True) -> bytes | str:
    validate_git_argv(tuple(args))
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False,
                            shell=False, timeout=180)
    if check:
        require(result.returncode == 0, "E_GIT", result.stderr.decode("utf-8", "replace"))
    return result.stdout if binary else result.stdout.decode("utf-8").rstrip("\r\n")


def parse_porcelain(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4, "E_PORCELAIN", line)
        result[line[3:]] = line[:2]
    return result


def parse_name_status(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        status, path = line.split("\t", 1)
        require(status in {"A", "M"} and path not in result, "E_NAME_STATUS", line)
        result[path] = status
    return result


def parse_ls_tree(text: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        require(kind == "blob" and path not in result, "E_LS_TREE", line)
        result[path] = (mode, oid)
    return result


def schema_errors(inventory: dict[str, Any], attestation: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def exact(value: Any, keys: set[str], label: str) -> bool:
        if not isinstance(value, dict) or set(value) != keys:
            errors.append(f"schema:{label}")
            return False
        return True

    common = {"artifact", "authority", "baseline_commit", "branch", "containing_commit",
              "expected_parent", "expected_subject", "gate", "generated_date", "inputs",
              "json_outputs_last", "persistence_terminal", "phase", "precommit_status",
              "result_first", "schema_version", "semantic_sha256", "step"}
    exact(inventory, common | {"blob_records", "genealogy_commit_records", "occurrence_records",
                               "universe", "validation"}, "inventory")
    exact(attestation, common | {"aggregate_ast_counts", "aggregate_definition_counts",
                                 "blob_attestations", "coverage", "inventory_semantic_sha256",
                                 "partition_contract", "validation"}, "attestation")
    input_keys = {"active_ledger", "builder", "handover", "manifest", "parent_ledger",
                  "result", "validator"}
    for label, doc in (("inventory", inventory), ("attestation", attestation)):
        inputs = doc.get("inputs")
        if exact(inputs, input_keys, f"{label}.inputs"):
            exact(inputs["manifest"], {"lf_sha256", "path", "raw_sha256"},
                  f"{label}.inputs.manifest")
            for name in input_keys - {"manifest"}:
                exact(inputs[name], {"path", "physical_lines", "sha256_lf"},
                      f"{label}.inputs.{name}")
        exact(doc.get("authority"), {"canonical_release", "external_material_authority",
              "full_read_coverage", "production_changed", "publication_ready",
              "runtime_behavior", "scientific_truth", "source_identity",
              "static_ast_topology", "test_pass"}, f"{label}.authority")
    exact(inventory.get("universe"), {"blob_membership_sha256", "occurrences",
          "path_blob_membership_sha256", "path_membership_sha256",
          "release_membership_sha256", "releases", "role_occurrence_counts",
          "role_unique_blob_counts", "unique_blob_physical_lines", "unique_blobs"},
          "inventory.universe")
    universe = inventory.get("universe", {})
    exact(universe.get("role_occurrence_counts"), {"code", "demo", "result", "test"},
          "inventory.universe.role_occurrence_counts")
    exact(universe.get("role_unique_blob_counts"), {"code", "demo", "result", "test"},
          "inventory.universe.role_unique_blob_counts")
    exact(inventory.get("validation"), set(INVENTORY_VALIDATION), "inventory.validation")
    exact(attestation.get("validation"), set(ATTESTATION_VALIDATION), "attestation.validation")
    exact(attestation.get("coverage"), {"encoding_failures", "occurrences_projected",
          "occurrences_total", "parser_failures", "releases_projected", "releases_total",
          "truncation_unresolved", "unique_blob_physical_lines_read",
          "unique_blob_physical_lines_total", "unique_blobs_read_full", "unique_blobs_total",
          "unread_lines"}, "attestation.coverage")

    occurrence_keys = {"blob_oid", "blob_ordinal", "git_mode", "manifest_entry_index",
                       "ordinal", "path", "physical_lines", "release", "role", "size_bytes"}
    for index, row in enumerate(inventory.get("occurrence_records", [])):
        exact(row, occurrence_keys, f"occurrence[{index}]")
    blob_keys = {"blob_oid", "genealogy", "git_mode", "lf_sha256", "occurrence_count",
                 "occurrence_paths", "ordinal", "physical_lines", "raw_sha256",
                 "release_projection", "role_projection", "size_bytes"}
    genealogy_keys = {"ambiguous_relation_inferred", "multiple_candidate_path_count",
                      "path_histories", "target_blob_first_introduction_candidates",
                      "target_blob_first_introduction_selection", "target_blob_later_touch_events",
                      "target_blob_touch_events"}
    path_history_keys = {"events", "exact_blob_event_count_all_history",
                         "first_exact_blob_candidates", "first_exact_selection",
                         "introduction_candidates", "introduction_event_count_all_history",
                         "introduction_selection", "path", "release",
                         "rename_copy_classification", "rename_copy_exact_same_blob",
                         "rename_copy_similarity_only", "touch_events"}
    candidate_keys = {"commit", "comparison_parent", "history_ordinal"}
    touch_keys = candidate_keys | {"status"}
    event_keys = {"author_time", "commit", "committer_time", "comparison_parent",
                  "current_tree_entry", "current_tree_matches_raw", "history_ordinal",
                  "new_blob", "new_mode", "new_path", "old_blob", "old_mode", "old_path",
                  "parent_ordinal", "parent_tree_entry", "parent_tree_matches_raw", "parents",
                  "similarity", "status", "subject", "tree_oid"}
    tree_keys = {"blob_oid", "mode", "type"}

    def event_schema(row: Any, label: str) -> None:
        if not isinstance(row, dict) or set(row) not in (event_keys, event_keys | {"path_role"}):
            errors.append(f"schema:{label}")
            return
        for entry_name in ("current_tree_entry", "parent_tree_entry"):
            entry = row[entry_name]
            if entry is not None:
                exact(entry, tree_keys, f"{label}.{entry_name}")

    for blob_index, row in enumerate(inventory.get("blob_records", [])):
        if not exact(row, blob_keys, f"blob[{blob_index}]"):
            continue
        genealogy = row["genealogy"]
        if not exact(genealogy, genealogy_keys, f"blob[{blob_index}].genealogy"):
            continue
        for name in ("target_blob_first_introduction_candidates",
                     "target_blob_later_touch_events", "target_blob_touch_events"):
            for item_index, item in enumerate(genealogy.get(name, [])):
                exact(item, candidate_keys, f"blob[{blob_index}].genealogy.{name}[{item_index}]")
        for history_index, history in enumerate(genealogy.get("path_histories", [])):
            label = f"blob[{blob_index}].genealogy.path_histories[{history_index}]"
            if not exact(history, path_history_keys, label):
                continue
            for name in ("introduction_candidates", "first_exact_blob_candidates"):
                for item_index, item in enumerate(history.get(name, [])):
                    exact(item, candidate_keys, f"{label}.{name}[{item_index}]")
            for item_index, item in enumerate(history.get("touch_events", [])):
                exact(item, touch_keys, f"{label}.touch_events[{item_index}]")
            for name in ("events", "rename_copy_exact_same_blob",
                         "rename_copy_similarity_only"):
                for item_index, item in enumerate(history.get(name, [])):
                    event_schema(item, f"{label}.{name}[{item_index}]")
    commit_keys = {"author_time", "commit", "committer_time", "history_ordinal",
                   "parent_comparisons", "parents", "subject", "tree_oid"}
    for commit_index, row in enumerate(inventory.get("genealogy_commit_records", [])):
        if exact(row, commit_keys, f"commit[{commit_index}]"):
            for parent_index, parent in enumerate(row.get("parent_comparisons", [])):
                exact(parent, {"change_count", "comparison_parent", "parent_ordinal"},
                      f"commit[{commit_index}].parent_comparisons[{parent_index}]")

    for index, row in enumerate(attestation.get("partition_contract", [])):
        exact(row, {"blobs", "first", "last", "lines", "membership_sha256", "partition",
              "review_batch", "review_evidence_sha256", "reviewer"}, f"partition[{index}]")
    attestation_keys = {"ast_parse", "blob_oid", "encoding", "genealogy_sha256",
                        "lf_sha256", "line_ranges", "occurrence_projection", "ordinal",
                        "partition", "raw_sha256", "read_status", "review_evidence_sha256",
                        "reviewer", "semantic", "truncation_unresolved", "unread_lines"}
    semantic_keys = {"ast_counts", "ast_parse", "definition_counts", "definitions", "encoding",
                     "imports", "module_behavior", "module_docstring"}
    behavior_keys = {"attribute_reads", "attribute_writes", "branches", "exceptions",
                     "fallbacks", "identifier_reads", "identifier_writes", "io_calls",
                     "lambda_count", "side_effects"}
    definition_keys = {"behavior", "decorators", "kind", "line_range", "qualified_name",
                       "signature", "source_sha256"}
    for blob_index, row in enumerate(attestation.get("blob_attestations", [])):
        label = f"attestation[{blob_index}]"
        if not exact(row, attestation_keys, label):
            continue
        exact(row["occurrence_projection"], {"paths", "releases", "roles"},
              f"{label}.occurrence_projection")
        semantic = row["semantic"]
        if not exact(semantic, semantic_keys, f"{label}.semantic"):
            continue
        if not isinstance(semantic.get("ast_counts"), dict) or not all(
                isinstance(key, str) and isinstance(value, int)
                for key, value in semantic.get("ast_counts", {}).items()):
            errors.append(f"schema:{label}.semantic.ast_counts")
        if not isinstance(semantic.get("definition_counts"), dict) or not all(
                key in {"ASYNC_FUNCTION", "CLASS", "FUNCTION"} and isinstance(value, int)
                for key, value in semantic.get("definition_counts", {}).items()):
            errors.append(f"schema:{label}.semantic.definition_counts")
        for import_index, item in enumerate(semantic.get("imports", [])):
            import_label = f"{label}.semantic.imports[{import_index}]"
            expected = ({"kind", "line", "names"} if item.get("kind") == "IMPORT" else
                        {"kind", "level", "line", "module", "names"})
            if exact(item, expected, import_label):
                for name_index, name in enumerate(item["names"]):
                    exact(name, {"alias", "name"}, f"{import_label}.names[{name_index}]")
        for definition_index, definition in enumerate(semantic.get("definitions", [])):
            definition_label = f"{label}.semantic.definitions[{definition_index}]"
            if not exact(definition, definition_keys, definition_label):
                continue
            signature = definition["signature"]
            if definition.get("kind") == "CLASS":
                if exact(signature, {"bases", "keywords"}, f"{definition_label}.signature"):
                    for keyword_index, keyword in enumerate(signature["keywords"]):
                        exact(keyword, {"name", "value"},
                              f"{definition_label}.signature.keywords[{keyword_index}]")
            elif exact(signature, {"keyword_only", "kwarg", "positional_only",
                                   "positional_or_keyword", "returns", "vararg"},
                       f"{definition_label}.signature"):
                for name in ("positional_only", "positional_or_keyword", "keyword_only"):
                    for argument_index, argument in enumerate(signature[name]):
                        exact(argument, {"annotation", "default", "name"},
                              f"{definition_label}.signature.{name}[{argument_index}]")
                for name in ("vararg", "kwarg"):
                    if signature[name] is not None:
                        exact(signature[name], {"annotation", "name"},
                              f"{definition_label}.signature.{name}")
            for behavior_name, behavior in (("behavior", definition.get("behavior")),):
                if exact(behavior, behavior_keys, f"{definition_label}.{behavior_name}"):
                    pass
        behavior_items = [(f"{label}.semantic.module_behavior", semantic.get("module_behavior"))]
        behavior_items.extend((f"{label}.semantic.definitions[{definition_index}].behavior",
                               definition.get("behavior"))
                              for definition_index, definition in enumerate(
                                  semantic.get("definitions", [])))
        for behavior_label, behavior in behavior_items:
            if not isinstance(behavior, dict) or set(behavior) != behavior_keys:
                continue
            families = (("branches", {"has_else", "kind", "line", "predicate_sha256"}),
                        ("exceptions", {"exception", "kind", "line"}),
                        ("fallbacks", {"kind", "line"}),
                        ("io_calls", {"call", "line"}),
                        ("side_effects", {"kind", "line", "target"}))
            for name, keys in families:
                for item_index, item in enumerate(behavior[name]):
                    item_label = f"{behavior_label}.{name}[{item_index}]"
                    if name == "fallbacks":
                        if not isinstance(item, dict) or set(item) not in (
                                {"kind", "line"}, {"kind", "line", "target"}):
                            errors.append(f"schema:{item_label}")
                    else:
                        exact(item, keys, item_label)
    for name in ("aggregate_ast_counts", "aggregate_definition_counts"):
        value = attestation.get(name)
        if not isinstance(value, dict) or not all(isinstance(key, str) and isinstance(count, int)
                                                  for key, count in value.items()):
            errors.append(f"schema:attestation.{name}")
    return errors


def artifact_errors(inventory: dict[str, Any], attestation: dict[str, Any]) -> list[str]:
    errors: list[str] = schema_errors(inventory, attestation)
    def check(condition: bool, label: str) -> None:
        if not condition:
            errors.append(label)
    for doc, artifact in ((inventory, "PHASE_067_PYTHON_SOURCE_INVENTORY"),
                          (attestation, "PHASE_067_PYTHON_FULL_READ_ATTESTATION")):
        check(doc.get("schema_version") == "P067-S82-1", f"schema:{artifact}")
        check(doc.get("artifact") == artifact, f"artifact:{artifact}")
        check(doc.get("phase") == 67 and doc.get("step") == 82, f"step:{artifact}")
        check(doc.get("baseline_commit") == BASELINE and doc.get("branch") == BRANCH and
              doc.get("generated_date") == "2026-09-02" and
              doc.get("result_first") is True and doc.get("json_outputs_last") is True,
              f"metadata:{artifact}")
        check(doc.get("expected_parent") == EXPECTED_PARENT and doc.get("expected_subject") == EXPECTED_SUBJECT,
              f"commit:{artifact}")
        check(doc.get("gate") == GATE and doc.get("persistence_terminal") == PERSISTENCE,
              f"gate:{artifact}")
        check(doc.get("precommit_status") == "PASS_PENDING_PERSISTENCE" and
              doc.get("containing_commit") == "PENDING_AT_PRECOMMIT_BY_DESIGN", f"boundary:{artifact}")
        check(doc.get("authority") == {"canonical_release": False, "external_material_authority": False,
              "full_read_coverage": True, "production_changed": False, "publication_ready": False,
              "runtime_behavior": False, "scientific_truth": False, "source_identity": True,
              "static_ast_topology": True, "test_pass": False}, f"authority:{artifact}")
        check(doc.get("inputs", {}).get("manifest") == {"path": MANIFEST_PATH,
              "raw_sha256": MANIFEST_SHA256, "lf_sha256": MANIFEST_SHA256},
              f"manifest-input:{artifact}")
    universe = inventory.get("universe", {})
    check((universe.get("occurrences"), universe.get("unique_blobs"),
           universe.get("unique_blob_physical_lines"), universe.get("releases")) == (129, 84, 29952, 20),
          "denominators")
    check(universe.get("role_occurrence_counts") == {"code": 20, "demo": 30, "result": 35, "test": 44},
          "role-occurrence")
    check(universe.get("role_unique_blob_counts") == {"code": 15, "demo": 26, "result": 14, "test": 29},
          "role-unique")
    check([universe.get(key) for key in ("path_membership_sha256", "path_blob_membership_sha256",
          "blob_membership_sha256", "release_membership_sha256")] == [PATH_MEMBERSHIP_SHA256,
          PATH_BLOB_MEMBERSHIP_SHA256, BLOB_MEMBERSHIP_SHA256, RELEASE_MEMBERSHIP_SHA256], "membership")
    occurrence = inventory.get("occurrence_records", [])
    blobs = inventory.get("blob_records", [])
    check(len(occurrence) == 129 and [row.get("ordinal") for row in occurrence] == list(range(1, 130)),
          "occurrence-cardinality")
    check(len(blobs) == 84 and [row.get("ordinal") for row in blobs] == list(range(1, 85)),
          "blob-cardinality")
    check(len({row.get("path") for row in occurrence}) == 129 and
          len({row.get("blob_oid") for row in blobs}) == 84, "bijection")
    blob_ordinals = {row.get("blob_oid"): row.get("ordinal") for row in blobs}
    check(all(row.get("blob_ordinal") == blob_ordinals.get(row.get("blob_oid"))
              for row in occurrence), "occurrence-blob-ordinal")
    check(sum(row.get("physical_lines", -1) for row in blobs) == 29952, "line-total")
    if len(occurrence) == 129 and len(blobs) == 84:
        by_blob: dict[str, list[dict[str, Any]]] = {row["blob_oid"]: [] for row in blobs}
        for row in occurrence:
            by_blob.setdefault(row.get("blob_oid", ""), []).append(row)
        for index, blob in enumerate(blobs, 1):
            projected = by_blob.get(blob.get("blob_oid", ""), [])
            check(blob.get("occurrence_count") == len(projected) and
                  blob.get("occurrence_paths") == [row.get("path") for row in projected] and
                  blob.get("release_projection") == sorted({row.get("release") for row in projected}) and
                  blob.get("role_projection") == sorted({row.get("role") for row in projected}),
                  f"blob-projection:{index}")
    checks = attestation.get("blob_attestations", [])
    check(len(checks) == 84 and [row.get("blob_oid") for row in checks] ==
          [row.get("blob_oid") for row in blobs], "attestation-binding")
    check(len(checks) == 84 and len(blobs) == 84 and
          all(row.get("read_status") == "READ_FULL" and
              row.get("line_ranges") == [[1, blobs[index].get("physical_lines")]] and
              row.get("unread_lines") == 0 and row.get("truncation_unresolved") == 0
              for index, row in enumerate(checks)), "full-read")
    if len(checks) == 84 and len(blobs) == 84:
        for index, (blob, row) in enumerate(zip(blobs, checks), 1):
            partition = next(item for item in PARTITION_CONTRACT
                             if item["first"] <= index <= item["last"])
            check(row.get("partition") == partition["partition"] and
                  row.get("reviewer") == partition["reviewer"] and
                  row.get("review_evidence_sha256") == partition["review_evidence_sha256"],
                  f"attestation-provenance:{index}")
            check(row.get("encoding") == "utf-8" and row.get("ast_parse") == "PASS",
                  f"attestation-parse:{index}")
            check(row.get("occurrence_projection") == {
                      "paths": blob.get("occurrence_paths"),
                      "releases": blob.get("release_projection"),
                      "roles": blob.get("role_projection")},
                  f"attestation-projection:{index}")
            check(row.get("genealogy_sha256") == sha256(canonical_bytes(blob.get("genealogy"))),
                  f"attestation-genealogy:{index}")
    partitions = attestation.get("partition_contract", [])
    check(partitions == [dict(row) for row in PARTITION_CONTRACT], "partitions")
    check(attestation.get("inventory_semantic_sha256") == inventory.get("semantic_sha256"), "pair-binding")
    check(attestation.get("coverage") == {"encoding_failures": 0, "occurrences_projected": 129,
          "occurrences_total": 129, "parser_failures": 0, "releases_projected": 20,
          "releases_total": 20, "truncation_unresolved": 0, "unique_blob_physical_lines_read": 29952,
          "unique_blob_physical_lines_total": 29952, "unique_blobs_read_full": 84,
          "unique_blobs_total": 84, "unread_lines": 0}, "coverage")
    check(inventory.get("validation") == INVENTORY_VALIDATION, "inventory-validation")
    check(attestation.get("validation") == ATTESTATION_VALIDATION, "attestation-validation")
    return errors


def source_segment(text: str, node: ast.AST) -> str:
    return ast.get_source_segment(text, node) or ""


def expression_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{expression_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Subscript):
        return f"{expression_name(node.value)}[]"
    if isinstance(node, ast.Call):
        return f"{expression_name(node.func)}()"
    return type(node).__name__


def bounded_walk(node: ast.AST) -> list[ast.AST]:
    result: list[ast.AST] = []
    stack = [node]
    first = True
    while stack:
        current = stack.pop()
        result.append(current)
        if not first and isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        first = False
        stack.extend(reversed(list(ast.iter_child_nodes(current))))
    return result


def state_projection(node: ast.AST) -> dict[str, list[str]]:
    names_read: set[str] = set()
    names_written: set[str] = set()
    attributes_read: set[str] = set()
    attributes_written: set[str] = set()
    for item in bounded_walk(node):
        if isinstance(item, ast.Name):
            (names_read if isinstance(item.ctx, ast.Load) else names_written).add(item.id)
        elif isinstance(item, (ast.Attribute, ast.Subscript)):
            target = expression_name(item)
            if isinstance(item.ctx, ast.Load):
                attributes_read.add(target)
            else:
                attributes_written.add(target)
    return {"identifier_reads": sorted(names_read), "identifier_writes": sorted(names_written),
            "attribute_reads": sorted(attributes_read), "attribute_writes": sorted(attributes_written)}


IO_NAMES = {"open", "input", "print", "read", "read_text", "read_bytes", "write", "write_text",
            "write_bytes", "load", "save", "savez", "savez_compressed", "read_csv", "to_csv",
            "savefig", "show", "run", "Popen", "system", "exit"}
MUTATION_NAMES = {"append", "extend", "insert", "pop", "remove", "clear", "update", "setdefault",
                  "sort", "reverse", "write", "write_text", "write_bytes", "save", "savez",
                  "savez_compressed", "savefig", "mkdir", "makedirs", "replace", "rename", "unlink"}


def behavior_projection(node: ast.AST, text: str) -> dict[str, Any]:
    branches: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    fallbacks: list[dict[str, Any]] = []
    io_calls: list[dict[str, Any]] = []
    side_effects: list[dict[str, Any]] = []
    lambdas = 0
    for item in bounded_walk(node):
        line = int(getattr(item, "lineno", 0))
        if isinstance(item, (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.Match)):
            test = getattr(item, "test", getattr(item, "subject", None))
            branches.append({"kind": type(item).__name__, "line": line,
                             "predicate_sha256": sha256(source_segment(text, test).encode("utf-8"))
                             if test else None, "has_else": bool(getattr(item, "orelse", []))})
            if getattr(item, "orelse", []):
                fallbacks.append({"kind": f"{type(item).__name__}_ELSE", "line": line})
        elif isinstance(item, ast.Try):
            branches.append({"kind": "Try", "line": line, "predicate_sha256": None,
                             "has_else": bool(item.orelse)})
            for handler in item.handlers:
                exceptions.append({"kind": "ExceptHandler", "line": int(getattr(handler, "lineno", line)),
                                   "exception": source_segment(text, handler.type) if handler.type else None})
                fallbacks.append({"kind": "EXCEPT_HANDLER", "line": int(getattr(handler, "lineno", line))})
        elif isinstance(item, ast.Raise):
            exceptions.append({"kind": "Raise", "line": line,
                               "exception": source_segment(text, item.exc) if item.exc else None})
        elif isinstance(item, ast.Assert):
            exceptions.append({"kind": "Assert", "line": line,
                               "exception": source_segment(text, item.test)})
        elif isinstance(item, ast.BoolOp) and isinstance(item.op, ast.Or):
            fallbacks.append({"kind": "BOOLEAN_OR", "line": line})
        elif isinstance(item, ast.Lambda):
            lambdas += 1
        if isinstance(item, ast.Call):
            identity = expression_name(item.func)
            leaf = identity.rsplit(".", 1)[-1]
            if leaf in IO_NAMES:
                io_calls.append({"call": identity, "line": line})
            if leaf in MUTATION_NAMES or identity in {"sys.exit", "os.system", "subprocess.run"}:
                side_effects.append({"kind": "CALL", "target": identity, "line": line})
            if leaf in {"get", "getattr", "setdefault"} or identity == "getattr":
                fallbacks.append({"kind": "DEFAULTING_CALL", "target": identity, "line": line})
        elif isinstance(item, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)):
            side_effects.append({"kind": type(item).__name__, "target": None, "line": line})
    return {"branches": branches, "exceptions": exceptions, "fallbacks": fallbacks,
            "io_calls": io_calls, "side_effects": side_effects, "lambda_count": lambdas,
            **state_projection(node)}


def annotation_text(text: str, node: ast.AST | None) -> str | None:
    return source_segment(text, node) if node is not None else None


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef, text: str) -> dict[str, Any]:
    arguments = node.args
    positional = [*arguments.posonlyargs, *arguments.args]
    defaults: list[str | None] = [None] * (len(positional) - len(arguments.defaults)) + [
        source_segment(text, value) for value in arguments.defaults]
    return {"positional_only": [{"name": arg.arg, "annotation": annotation_text(text, arg.annotation),
             "default": defaults[index]} for index, arg in enumerate(arguments.posonlyargs)],
            "positional_or_keyword": [{"name": arg.arg, "annotation": annotation_text(text, arg.annotation),
             "default": defaults[len(arguments.posonlyargs) + index]}
             for index, arg in enumerate(arguments.args)],
            "vararg": ({"name": arguments.vararg.arg,
                        "annotation": annotation_text(text, arguments.vararg.annotation)}
                       if arguments.vararg else None),
            "keyword_only": [{"name": arg.arg, "annotation": annotation_text(text, arg.annotation),
                              "default": annotation_text(text, default)}
                             for arg, default in zip(arguments.kwonlyargs, arguments.kw_defaults)],
            "kwarg": ({"name": arguments.kwarg.arg,
                       "annotation": annotation_text(text, arguments.kwarg.annotation)}
                      if arguments.kwarg else None), "returns": annotation_text(text, node.returns)}


def definition_records(tree: ast.Module, text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    def visit(node: ast.AST, stack: list[str]) -> None:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                records.append({"qualified_name": ".".join([*stack, node.name]),
                    "kind": "ASYNC_FUNCTION" if isinstance(node, ast.AsyncFunctionDef) else "FUNCTION",
                    "line_range": [node.lineno, node.end_lineno],
                    "source_sha256": sha256(source_segment(text, node).encode("utf-8")),
                    "signature": function_signature(node, text),
                    "decorators": [source_segment(text, item) for item in node.decorator_list],
                    "behavior": behavior_projection(node, text)})
                for statement in node.body:
                    visit(statement, [*stack, node.name])
            elif isinstance(node, ast.ClassDef):
                records.append({"qualified_name": ".".join([*stack, node.name]), "kind": "CLASS",
                    "line_range": [node.lineno, node.end_lineno],
                    "source_sha256": sha256(source_segment(text, node).encode("utf-8")),
                    "signature": {"bases": [source_segment(text, base) for base in node.bases],
                                  "keywords": [{"name": item.arg, "value": source_segment(text, item.value)}
                                               for item in node.keywords]},
                    "decorators": [source_segment(text, item) for item in node.decorator_list],
                    "behavior": behavior_projection(node, text)})
                for statement in node.body:
                    visit(statement, [*stack, node.name])
            else:
                for child in ast.iter_child_nodes(node):
                    visit(child, stack)
    visit(tree, [])
    return records


def import_records(tree: ast.Module) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            records.append({"kind": "IMPORT", "line": node.lineno,
                            "names": [{"name": item.name, "alias": item.asname} for item in node.names]})
        elif isinstance(node, ast.ImportFrom):
            records.append({"kind": "IMPORT_FROM", "line": node.lineno, "module": node.module,
                            "level": node.level,
                            "names": [{"name": item.name, "alias": item.asname} for item in node.names]})
    return sorted(records, key=lambda row: (row["line"], row["kind"], repr(row)))


def reconstruct_semantic(raw: bytes) -> dict[str, Any]:
    require(raw == lf_bytes(raw), "E_SOURCE_CR")
    text = raw.decode("utf-8")
    tree = ast.parse(text)
    definitions = definition_records(tree, text)
    counts = Counter(type(node).__name__ for node in ast.walk(tree))
    return {"encoding": "utf-8", "ast_parse": "PASS",
            "module_docstring": ast.get_docstring(tree, clean=False), "imports": import_records(tree),
            "definitions": definitions, "module_behavior": behavior_projection(tree, text),
            "ast_counts": dict(sorted(counts.items())),
            "definition_counts": dict(sorted(Counter(row["kind"] for row in definitions).items()))}


def parse_tree_dict(text: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    if not text:
        return result
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        result[path] = {"mode": mode, "type": kind, "blob_oid": oid}
    return result


def reconstruct_history(selected_paths: set[str]) -> tuple[
        list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    commit_text = git("rev-list", "--full-history", "--reverse", "--topo-order", BASELINE,
                      "--", *RELEASE_ROOTS)
    require(isinstance(commit_text, str), "E_HISTORY_REV_LIST")
    commit_oids = commit_text.splitlines()
    per_path: dict[str, list[dict[str, Any]]] = {path: [] for path in selected_paths}
    commit_records: list[dict[str, Any]] = []
    for history_ordinal, commit_oid in enumerate(commit_oids, 1):
        header = git("show", "-s", "--format=%H%x00%P%x00%T%x00%aI%x00%cI%x00%s", commit_oid)
        require(isinstance(header, str), "E_HISTORY_HEADER")
        fields = header.split("\0", 5)
        require(len(fields) == 6 and fields[0] == commit_oid, "E_HISTORY_HEADER", commit_oid)
        parents = fields[1].split()
        comparisons: list[dict[str, Any]] = []
        for parent_ordinal, parent in enumerate(parents if parents else [None], 1):
            if parent:
                raw_text = git("diff-tree", "-r", "--raw", "--abbrev=40", "-M", "-C",
                               "--find-copies-harder", parent, commit_oid, "--", *RELEASE_ROOTS)
            else:
                raw_text = git("diff-tree", "--root", "-r", "--raw", "--abbrev=40", "-M", "-C",
                               "--find-copies-harder", commit_oid, "--", *RELEASE_ROOTS)
            require(isinstance(raw_text, str), "E_HISTORY_DIFF")
            changes: list[dict[str, Any]] = []
            for line in raw_text.splitlines():
                if not line.startswith(":"):
                    continue
                cells = line.split("\t")
                meta = cells[0].split()
                require(len(meta) == 5 and len(cells) in {2, 3}, "E_HISTORY_RAW", line)
                status = meta[4]
                change = {"old_mode": meta[0][1:], "new_mode": meta[1], "old_blob": meta[2],
                          "new_blob": meta[3], "status": status[0],
                          "similarity": int(status[1:]) if len(status) > 1 else None,
                          "old_path": cells[1], "new_path": cells[-1]}
                if change["old_path"] in selected_paths or change["new_path"] in selected_paths:
                    changes.append(change)
            if not changes:
                continue
            paths = sorted({change["old_path"] for change in changes} |
                           {change["new_path"] for change in changes})
            current_tree = parse_tree_dict(str(git("ls-tree", commit_oid, "--", *paths)))
            parent_tree = parse_tree_dict(str(git("ls-tree", parent, "--", *paths))) if parent else {}
            comparisons.append({"parent_ordinal": parent_ordinal, "comparison_parent": parent,
                                "change_count": len(changes)})
            for change in changes:
                current_matches = (current_tree.get(change["new_path"], {}).get("blob_oid") == change["new_blob"]
                                   if change["new_blob"] != "0" * 40
                                   else change["new_path"] not in current_tree)
                parent_matches = (parent_tree.get(change["old_path"], {}).get("blob_oid") == change["old_blob"]
                                  if change["old_blob"] != "0" * 40
                                  else change["old_path"] not in parent_tree)
                event = {**change, "history_ordinal": history_ordinal, "parent_ordinal": parent_ordinal,
                         "commit": commit_oid, "parents": parents, "tree_oid": fields[2],
                         "author_time": fields[3], "committer_time": fields[4], "subject": fields[5],
                         "comparison_parent": parent,
                         "current_tree_entry": current_tree.get(change["new_path"]),
                         "parent_tree_entry": parent_tree.get(change["old_path"]),
                         "current_tree_matches_raw": current_matches,
                         "parent_tree_matches_raw": parent_matches}
                require(current_matches and parent_matches, "E_HISTORY_TREE_BINDING")
                if change["new_path"] in selected_paths:
                    per_path[change["new_path"]].append(event)
                if change["old_path"] in selected_paths and change["old_path"] != change["new_path"]:
                    per_path[change["old_path"]].append({**event, "path_role": "OLD_PATH"})
        if comparisons:
            commit_records.append({"history_ordinal": history_ordinal, "commit": commit_oid,
                "parents": parents, "tree_oid": fields[2], "author_time": fields[3],
                "committer_time": fields[4], "subject": fields[5], "parent_comparisons": comparisons})
    require(all(per_path.values()), "E_HISTORY_COVERAGE")
    projection = {path: [{"history_ordinal": event["history_ordinal"], "commit": event["commit"],
                          "comparison_parent": event["comparison_parent"], "status": event["status"]}
                         for event in events] for path, events in sorted(per_path.items())}
    return commit_records, projection, per_path


def reconstruct_blob_genealogy(blob: str, source_rows: list[dict[str, Any]],
                                projection: dict[str, list[dict[str, Any]]],
                                per_path: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    path_histories: list[dict[str, Any]] = []
    target_events: list[dict[str, Any]] = []
    for row in source_rows:
        events = per_path[row["path"]]
        new_events = [event for event in events if event["new_path"] == row["path"]]
        introduction_events = [event for event in new_events if event["status"] in {"A", "R", "C"}]
        exact_blob_events = [event for event in new_events if event["new_blob"] == blob]
        require(introduction_events and exact_blob_events, "E_HISTORY_CANDIDATES", row["path"])
        first_introduction_ordinal = min(event["history_ordinal"] for event in introduction_events)
        first_exact_ordinal = min(event["history_ordinal"] for event in exact_blob_events)
        introductions = [event for event in introduction_events
                         if event["history_ordinal"] == first_introduction_ordinal]
        first_exact = [event for event in exact_blob_events
                       if event["history_ordinal"] == first_exact_ordinal]
        target_events.extend(exact_blob_events)
        exact_rc = [event for event in events if event["status"] in {"R", "C"} and
                    event["old_blob"] == event["new_blob"]]
        similar_rc = [event for event in events if event["status"] in {"R", "C"} and
                      event["old_blob"] != event["new_blob"]]
        path_histories.append({"path": row["path"], "release": row["version"],
            "introduction_candidates": [{"history_ordinal": event["history_ordinal"],
                "commit": event["commit"], "comparison_parent": event["comparison_parent"]}
                for event in introductions],
            "introduction_selection": ("UNIQUE" if len(introductions) == 1 else
                "MULTIPLE_PARENT_CANDIDATES_PRESERVED_NO_RELATION_INFERRED"),
            "introduction_event_count_all_history": len(introduction_events),
            "first_exact_blob_candidates": [{"history_ordinal": event["history_ordinal"],
                "commit": event["commit"], "comparison_parent": event["comparison_parent"]}
                for event in first_exact],
            "first_exact_selection": ("UNIQUE" if len(first_exact) == 1 else
                "MULTIPLE_PARENT_CANDIDATES_PRESERVED_NO_RELATION_INFERRED"),
            "exact_blob_event_count_all_history": len(exact_blob_events),
            "touch_events": projection[row["path"]], "events": events,
            "rename_copy_exact_same_blob": exact_rc, "rename_copy_similarity_only": similar_rc,
            "rename_copy_classification": ("EXACT_SAME_BLOB" if exact_rc and not similar_rc
                else "EXACT_AND_SIMILARITY_SEPARATED" if exact_rc and similar_rc
                else "SIMILARITY_ONLY" if similar_rc else "NONE_OBSERVED_NO_RELATION_INFERRED")})
    touch_events: list[dict[str, Any]] = []
    seen: set[tuple[str, str | None]] = set()
    for event in target_events:
        identity = (event["commit"], event["comparison_parent"])
        if identity not in seen:
            seen.add(identity)
            touch_events.append({"history_ordinal": event["history_ordinal"], "commit": event["commit"],
                                 "comparison_parent": event["comparison_parent"]})
    touch_events.sort(key=lambda event: (
        event["history_ordinal"], event["commit"], event["comparison_parent"] or ""))
    first_target_ordinal = min(event["history_ordinal"] for event in touch_events)
    first_target_candidates = [event for event in touch_events
                               if event["history_ordinal"] == first_target_ordinal]
    later_target_events = [event for event in touch_events
                           if event["history_ordinal"] > first_target_ordinal]
    return {"path_histories": path_histories, "target_blob_touch_events": touch_events,
            "target_blob_first_introduction_candidates": first_target_candidates,
            "target_blob_first_introduction_selection": (
                "UNIQUE" if len(first_target_candidates) == 1 else
                "MULTIPLE_PARENT_CANDIDATES_PRESERVED_NO_RELATION_INFERRED"),
            "target_blob_later_touch_events": later_target_events,
            "multiple_candidate_path_count": sum(
                history["introduction_selection"].startswith("MULTIPLE") or
                history["first_exact_selection"].startswith("MULTIPLE") for history in path_histories),
             "ambiguous_relation_inferred": any(
                "INFERRED" in history["introduction_selection"] and
                not history["introduction_selection"].endswith("NO_RELATION_INFERRED")
                 for history in path_histories)}


def genealogy_storage_errors(inventory: dict[str, Any],
                             expected_commits: list[dict[str, Any]],
                             grouped: dict[str, list[dict[str, Any]]],
                             projection: dict[str, list[dict[str, Any]]],
                             per_path: dict[str, list[dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    if inventory.get("genealogy_commit_records") != expected_commits:
        errors.append("genealogy-commit-records")
    stored = {row.get("blob_oid"): row.get("genealogy")
              for row in inventory.get("blob_records", [])}
    for oid in sorted(grouped):
        expected = reconstruct_blob_genealogy(oid, grouped[oid], projection, per_path)
        if stored.get(oid) != expected:
            errors.append(f"genealogy-blob:{oid}")
    return errors


def genealogy_negative_controls(inventory: dict[str, Any],
                                 expected_commits: list[dict[str, Any]],
                                 grouped: dict[str, list[dict[str, Any]]],
                                 projection: dict[str, list[dict[str, Any]]],
                                 per_path: dict[str, list[dict[str, Any]]]) -> tuple[int, int]:
    mutations: list[tuple[str, Any]] = []

    dropped_commit = dict(inventory)
    dropped_commit["genealogy_commit_records"] = list(inventory["genealogy_commit_records"][:-1])
    mutations.append(("drop-genealogy-commit-record", dropped_commit))

    source_blob_index = next(index for index, row in enumerate(inventory["blob_records"])
                             if row["genealogy"]["path_histories"][0]["events"])
    dropped_event = dict(inventory)
    dropped_event["blob_records"] = list(inventory["blob_records"])
    dropped_row = dict(dropped_event["blob_records"][source_blob_index])
    dropped_row["genealogy"] = copy.deepcopy(dropped_row["genealogy"])
    dropped_row["genealogy"]["path_histories"][0]["events"].pop()
    dropped_event["blob_records"][source_blob_index] = dropped_row
    mutations.append(("drop-genealogy-event", dropped_event))

    wrong_parent = dict(inventory)
    wrong_parent["blob_records"] = list(inventory["blob_records"])
    parent_row = dict(wrong_parent["blob_records"][source_blob_index])
    parent_row["genealogy"] = copy.deepcopy(parent_row["genealogy"])
    parent_row["genealogy"]["path_histories"][0]["events"][0]["comparison_parent"] = "0" * 40
    wrong_parent["blob_records"][source_blob_index] = parent_row
    mutations.append(("wrong-comparison-parent", wrong_parent))

    nonfirst_intro = dict(inventory)
    nonfirst_intro["blob_records"] = list(inventory["blob_records"])
    intro_row = dict(nonfirst_intro["blob_records"][source_blob_index])
    intro_row["genealogy"] = copy.deepcopy(intro_row["genealogy"])
    intro_row["genealogy"]["path_histories"][0]["introduction_candidates"][0][
        "history_ordinal"] += 1
    nonfirst_intro["blob_records"][source_blob_index] = intro_row
    mutations.append(("nonfirst-introduction-candidate", nonfirst_intro))

    passed = 0
    for label, candidate in mutations:
        errors = genealogy_storage_errors(candidate, expected_commits, grouped, projection, per_path)
        require(errors, "E_GENEALOGY_NEGATIVE_ESCAPE", label)
        passed += 1
    return passed, len(mutations)


def independent_projection(inventory: dict[str, Any],
                           attestation: dict[str, Any]) -> tuple[int, int, int, int, int, int, int]:
    manifest_raw = git("cat-file", "blob", f"{EXPECTED_PARENT}:{MANIFEST_PATH}", binary=True)
    require(isinstance(manifest_raw, bytes) and sha256(manifest_raw) == MANIFEST_SHA256, "E_MANIFEST_HASH")
    manifest = strict_source_manifest_load(manifest_raw)
    indexed = [(index, row) for index, row in enumerate(manifest["entries"]) if row.get("extension") == "py"]
    rows = [row for _, row in indexed]
    blobs = sorted({row["blob_sha"] for row in rows})
    require(len(rows) == 129 and len(blobs) == 84 and len({row["version"] for row in rows}) == 20,
            "E_RECONSTRUCT_DENOMINATOR")
    require(membership_hash(sorted(row["path"] for row in rows)) == PATH_MEMBERSHIP_SHA256 and
            sha256("".join(f"{row['path']}\t{row['blob_sha']}\n" for row in sorted(rows,
                   key=lambda item: item["path"])).encode()) == PATH_BLOB_MEMBERSHIP_SHA256 and
            membership_hash(blobs) == BLOB_MEMBERSHIP_SHA256 and
            membership_hash(sorted({row["version"] for row in rows})) == RELEASE_MEMBERSHIP_SHA256,
            "E_RECONSTRUCT_MEMBERSHIP")
    for partition in PARTITION_CONTRACT:
        selected = blobs[partition["first"] - 1:partition["last"]]
        require(len(selected) == partition["blobs"] and
                membership_hash(selected) == PARTITION_MEMBERSHIP[partition["partition"]] ==
                partition["membership_sha256"], "E_RECONSTRUCT_PARTITION",
                partition["partition"])
    blob_ordinals = {oid: ordinal for ordinal, oid in enumerate(blobs, 1)}
    expected_occurrence = [(index, row["path"], row["blob_sha"], blob_ordinals[row["blob_sha"]],
                            row["version"], row["role"], row["git_mode"], row["size_bytes"],
                            row["extent"]["lines"])
                           for index, row in sorted(indexed, key=lambda item: item[1]["path"])]
    observed_occurrence = [(row["manifest_entry_index"], row["path"], row["blob_oid"],
                            row["blob_ordinal"], row["release"], row["role"], row["git_mode"],
                            row["size_bytes"], row["physical_lines"])
                           for row in inventory["occurrence_records"]]
    require(observed_occurrence == expected_occurrence, "E_RECONSTRUCT_OCCURRENCES")
    blob_records = {row["blob_oid"]: row for row in inventory["blob_records"]}
    attestations = {row["blob_oid"]: row for row in attestation["blob_attestations"]}
    aggregate = Counter()
    definitions = Counter()
    line_total = 0
    grouped: dict[str, list[dict[str, Any]]] = {oid: [] for oid in blobs}
    for row in rows:
        grouped[row["blob_sha"]].append(row)
    history_commits, history_projection, per_path = reconstruct_history({row["path"] for row in rows})
    require(not genealogy_storage_errors(inventory, history_commits, grouped,
                                          history_projection, per_path),
            "E_HISTORY_COMMIT_COMPLETENESS")
    for ordinal, oid in enumerate(blobs, 1):
        raw = git("cat-file", "blob", oid, binary=True)
        require(isinstance(raw, bytes), "E_BLOB_TYPE")
        text = raw.decode("utf-8")
        tree = ast.parse(text)
        lines = len(text.splitlines())
        line_total += lines
        aggregate.update(type(node).__name__ for node in ast.walk(tree))
        definitions.update("CLASS" if isinstance(node, ast.ClassDef) else
                           "ASYNC_FUNCTION" if isinstance(node, ast.AsyncFunctionDef) else "FUNCTION"
                           for node in ast.walk(tree)
                           if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)))
        record = blob_records[oid]
        check = attestations[oid]
        source_rows = grouped[oid]
        expected_paths = [row["path"] for row in source_rows]
        expected_releases = sorted({row["version"] for row in source_rows})
        expected_roles = sorted({row["role"] for row in source_rows})
        partition = next(row for row in PARTITION_CONTRACT
                         if row["first"] <= ordinal <= row["last"])
        require(record["ordinal"] == ordinal and record["git_mode"] == "100644" and
                record["size_bytes"] == len(raw) and record["physical_lines"] == lines and
                record["raw_sha256"] == sha256(raw) and record["lf_sha256"] == sha256(lf_bytes(raw)),
                "E_BLOB_RECONSTRUCT", oid)
        require(record["occurrence_count"] == len(source_rows) and
                record["occurrence_paths"] == expected_paths and
                record["release_projection"] == expected_releases and
                record["role_projection"] == expected_roles,
                "E_BLOB_PROJECTION", oid)
        require(check["ordinal"] == ordinal and check["raw_sha256"] == sha256(raw) and
                check["lf_sha256"] == sha256(lf_bytes(raw)) and
                check["partition"] == partition["partition"] and
                check["reviewer"] == partition["reviewer"] and
                check["review_evidence_sha256"] == partition["review_evidence_sha256"] and
                check["encoding"] == "utf-8" and check["ast_parse"] == "PASS" and
                check["occurrence_projection"] == {"paths": expected_paths,
                    "releases": expected_releases, "roles": expected_roles} and
                check["genealogy_sha256"] == sha256(canonical_bytes(record["genealogy"])) and
                check["semantic"] == reconstruct_semantic(raw),
                "E_SEMANTIC_RECONSTRUCT", oid)
        require(record["genealogy"] == reconstruct_blob_genealogy(
                oid, grouped[oid], history_projection, per_path), "E_HISTORY_EVENT_COMPLETENESS", oid)
    require(line_total == 29952, "E_RECONSTRUCT_LINES")
    require(dict(sorted(aggregate.items())) == attestation["aggregate_ast_counts"] and
            dict(sorted(definitions.items())) == attestation["aggregate_definition_counts"],
            "E_AST_AGGREGATE")
    require(definitions["FUNCTION"] + definitions["ASYNC_FUNCTION"] == 906 and
            definitions["CLASS"] == 35, "E_DEFINITION_PIN")
    require((aggregate["FunctionDef"] + aggregate["AsyncFunctionDef"], aggregate["ClassDef"],
             aggregate["Import"] + aggregate["ImportFrom"], aggregate["If"], aggregate["Try"],
             aggregate["Raise"], aggregate["With"] + aggregate["AsyncWith"], aggregate["Call"]) ==
            (906, 35, 323, 937, 83, 267, 17, 15135), "E_AST_PIN")
    genealogy_passed, genealogy_total = genealogy_negative_controls(
        inventory, history_commits, grouped, history_projection, per_path)
    return (129, 84, line_total, len(aggregate), len(history_commits),
            genealogy_passed, genealogy_total)


def control_document_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    result = texts[RESULT_PATH]
    expected_result_lines = {
        "Status: `PASS_PENDING_PERSISTENCE`",
        f"Selected Gate: `{GATE}`",
        f"Persistence terminal: `{PERSISTENCE}`",
        "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        f"Expected parent: `{EXPECTED_PARENT}`",
        f"Expected subject: `{EXPECTED_SUBJECT}`",
    }
    for line in expected_result_lines:
        if result.splitlines().count(line) != 1:
            errors.append(f"result-line:{line}")
    authority_lines = tuple(result.split("## Authority Boundary", 1)[-1].split(
        "## Files Created or Modified", 1)[0].strip().splitlines())
    expected_authority_lines = (
        "- Source identity, complete-read coverage, static AST topology and Git genealogy are true.",
        "- Runtime behavior, test pass, scientific truth, external/material authority, a canonical release and publication readiness remain false.",
        "- Ref. 7 original text, original optimizer state, held-out/external/material evidence and stale PDF debt remain open under their existing owners.",
        "- No main scholarly body, production code or `Claude/**` file is changed.",
        "- Step 83 remains blocked until the same exact-eight child is pushed/live equal,",
        "  clean and both runtimes return `PASS_P067_STEP82_PERSISTENCE`.",
    )
    if authority_lines != expected_authority_lines:
        errors.append("result-authority-boundary")
    for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH):
        rows = [line for line in texts[path].splitlines() if line.startswith("| 067 |")]
        if len(rows) != 1 or not all(token in rows[0] for token in (
                "Step 82", GATE, "PASS_PENDING_PERSISTENCE", EXPECTED_PARENT,
                EXPECTED_SUBJECT, PERSISTENCE, "129/84/29,952", "20", "READ_FULL")):
            errors.append(f"phase067-row:{path}")
    handover_rows = [line for line in texts[HANDOVER_PATH].splitlines()
                     if line.startswith("| Phase 067 Step 82 |")]
    if len(handover_rows) != 1 or not all(token in handover_rows[0] for token in (
            GATE, "PASS_PENDING_PERSISTENCE", EXPECTED_SUBJECT, PERSISTENCE,
            "129/84/29,952", "20", "READ_FULL", "Step 83")):
        errors.append("handover-step82-row")
    active = texts[ACTIVE_LEDGER_PATH]
    handover = texts[HANDOVER_PATH]
    if active.count("## Next Exact Step") != 1:
        errors.append("active-next-heading")
    if handover.count("## Exact Next Action") != 1:
        errors.append("handover-next-heading")
    active_next = active.split("## Next Exact Step", 1)[-1]
    handover_next = handover.split("## Exact Next Action", 1)[-1]
    for label, passage in (("active", active_next), ("handover", handover_next)):
        if not all(token in passage for token in ("Step 82", EXPECTED_PARENT, EXPECTED_SUBJECT,
                                                   PERSISTENCE, "Step 83")):
            errors.append(f"next-schema:{label}")
        if "Complete the Phase 067 activation-persistence-repair" in passage or \
                "Begin Step 82 only after" in passage:
            errors.append(f"stale-next:{label}")
    return errors


def verify_controls(inventory: dict[str, Any], attestation: dict[str, Any]) -> None:
    for name, path in (("builder", BUILDER_PATH), ("validator", VALIDATOR_PATH), ("result", RESULT_PATH),
                       ("parent_ledger", PARENT_LEDGER_PATH), ("active_ledger", ACTIVE_LEDGER_PATH),
                       ("handover", HANDOVER_PATH)):
        raw = (ROOT / path).read_bytes()
        if path in CONTROL_DOCUMENT_SHA256:
            require(sha256(raw) == CONTROL_DOCUMENT_SHA256[path], "E_CONTROL_DOCUMENT_HASH", path)
        for doc in (inventory, attestation):
            require(doc["inputs"][name] == {"path": path, "sha256_lf": sha256(raw),
                    "physical_lines": len(raw.decode("utf-8").splitlines())}, "E_CONTROL_BINDING", path)
    texts = {path: (ROOT / path).read_text(encoding="utf-8")
             for path in (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)}
    required = ["Step 82", GATE, "PASS_PENDING_PERSISTENCE", EXPECTED_PARENT, EXPECTED_SUBJECT, PERSISTENCE,
                "129", "84", "29,952", "20", "READ_FULL", "Step 83"]
    for path, text in texts.items():
        require(all(token in text for token in required), "E_CONTROL_TOKEN", path)
    errors = control_document_errors(texts)
    require(not errors, "E_CONTROL_STRUCTURE", repr(errors))


def control_document_negative_controls() -> tuple[int, int]:
    texts = {path: (ROOT / path).read_text(encoding="utf-8")
             for path in (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)}
    candidates: list[tuple[str, dict[str, str]]] = []
    duplicate_row = dict(texts)
    phase_row = next(line for line in texts[ACTIVE_LEDGER_PATH].splitlines()
                     if line.startswith("| 067 |"))
    duplicate_row[ACTIVE_LEDGER_PATH] += "\n" + phase_row + "\n"
    candidates.append(("duplicate-phase067-row", duplicate_row))
    stale_next = dict(texts)
    stale_next[HANDOVER_PATH] = stale_next[HANDOVER_PATH].replace(
        "Complete Step 82 JSON-last collection",
        "Complete the Phase 067 activation-persistence-repair; Begin Step 82 only after repair. "
        "Complete Step 82 JSON-last collection", 1)
    candidates.append(("stale-next-action", stale_next))
    wrong_gate = dict(texts)
    wrong_gate[RESULT_PATH] = wrong_gate[RESULT_PATH].replace(
        f"Selected Gate: `{GATE}`", "Selected Gate: `PASS_P067_CODE_HISTORY`", 1)
    candidates.append(("wrong-current-gate", wrong_gate))
    authority_overclaim = dict(texts)
    authority_overclaim[RESULT_PATH] = authority_overclaim[RESULT_PATH].replace(
        "Runtime behavior, test pass, scientific truth, external/material authority, a canonical release and publication readiness remain false.",
        "Runtime behavior, test pass, scientific truth, external/material authority, a canonical release and publication readiness are true.", 1)
    candidates.append(("step82-authority-overclaim", authority_overclaim))
    passed = 0
    for label, candidate in candidates:
        require(control_document_errors(candidate), "E_CONTROL_NEGATIVE_ESCAPE", label)
        passed += 1
    return passed, len(candidates)


def negative_controls(inventory: dict[str, Any], attestation: dict[str, Any],
                      refs: dict[str, Any], expected_tip: str) -> tuple[int, int]:
    mutations: list[tuple[str, Any]] = []
    def add(label: str, change: Any) -> None:
        mutations.append((label, change))
    add("occurrence-count", lambda a, b: a["universe"].__setitem__("occurrences", 128))
    add("blob-count", lambda a, b: a["universe"].__setitem__("unique_blobs", 83))
    add("line-count", lambda a, b: a["universe"].__setitem__("unique_blob_physical_lines", 29951))
    add("release-count", lambda a, b: a["universe"].__setitem__("releases", 19))
    add("occurrence-drop", lambda a, b: a["occurrence_records"].pop())
    add("blob-drop", lambda a, b: a["blob_records"].pop())
    add("blob-order", lambda a, b: a["blob_records"].reverse())
    add("line-inflate", lambda a, b: a["blob_records"][0].__setitem__("physical_lines", 9999))
    add("read-partial", lambda a, b: b["blob_attestations"][0].__setitem__("read_status", "PARTIAL"))
    add("partition-overlap", lambda a, b: b["partition_contract"][1].__setitem__("first", 28))
    add("review-evidence-valid-wrong", lambda a, b: b["partition_contract"][0].__setitem__(
        "review_evidence_sha256", "0" * 64))
    add("attestation-reviewer", lambda a, b: b["blob_attestations"][0].__setitem__(
        "reviewer", "wrong-reviewer"))
    add("attestation-partition", lambda a, b: b["blob_attestations"][0].__setitem__(
        "partition", "B"))
    add("attestation-projection", lambda a, b: b["blob_attestations"][0][
        "occurrence_projection"].__setitem__("paths", ["wrong/path.py"]))
    add("attestation-genealogy-hash", lambda a, b: b["blob_attestations"][0].__setitem__(
        "genealogy_sha256", "0" * 64))
    add("attestation-encoding", lambda a, b: b["blob_attestations"][0].__setitem__(
        "encoding", "ascii"))
    add("attestation-ast-parse", lambda a, b: b["blob_attestations"][0].__setitem__(
        "ast_parse", "NOT_TESTED"))
    add("blob-projection", lambda a, b: a["blob_records"][0].__setitem__(
        "release_projection", ["v0.invalid"]))
    add("inventory-validation", lambda a, b: a["validation"].__setitem__(
        "parser_failures", 1))
    add("attestation-validation", lambda a, b: b["validation"].__setitem__(
        "genealogy_unbound", 1))
    add("schema-extra-top-key", lambda a, b: a.__setitem__("unexpected", True))
    add("schema-extra-nested-key", lambda a, b: b["blob_attestations"][0].__setitem__(
        "unexpected", True))
    add("schema-missing-nested-key", lambda a, b: b["blob_attestations"][0].pop("encoding"))
    add("metadata-baseline", lambda a, b: a.__setitem__("baseline_commit", "0" * 40))
    add("metadata-branch", lambda a, b: b.__setitem__("branch", "wrong/branch"))
    add("metadata-date", lambda a, b: a.__setitem__("generated_date", "2026-09-03"))
    add("metadata-result-first", lambda a, b: b.__setitem__("result_first", False))
    add("metadata-json-last", lambda a, b: a.__setitem__("json_outputs_last", False))
    add("manifest-input-path", lambda a, b: a["inputs"]["manifest"].__setitem__(
        "path", "Codex/results/wrong.json"))
    add("manifest-input-hash", lambda a, b: b["inputs"]["manifest"].__setitem__(
        "raw_sha256", "0" * 64))
    add("occurrence-blob-ordinal", lambda a, b: a["occurrence_records"][0].__setitem__(
        "blob_ordinal", 84))
    add("pair-binding", lambda a, b: b.__setitem__("inventory_semantic_sha256", "0" * 64))
    add("authority-runtime", lambda a, b: a["authority"].__setitem__("runtime_behavior", True))
    add("authority-science", lambda a, b: a["authority"].__setitem__("scientific_truth", True))
    add("gate", lambda a, b: a.__setitem__("gate", "PASS"))
    add("parent", lambda a, b: b.__setitem__("expected_parent", BASELINE))
    passed = 0
    for label, change in mutations:
        left, right = copy.deepcopy(inventory), copy.deepcopy(attestation)
        change(left, right)
        if artifact_errors(left, right):
            passed += 1
        else:
            raise ValidationFailure("E_NEGATIVE_ESCAPE", label)
    for field in ("branch", "head", "upstream_name", "upstream_oid", "active_tracking_oid",
                  "active_live_oid", "origin", "protected_local_oid", "protected_tracking_oid",
                  "protected_live_oid", "main_local", "main_tracking_oid", "main_live_oid"):
        candidate = dict(refs)
        candidate[field] = "DRIFT"
        require(repository_ref_errors(candidate, expected_tip) == [field],
                "E_REF_NEGATIVE_ESCAPE", field)
        passed += 1
    return passed, len(mutations) + 13


def strict_json_controls() -> tuple[int, int]:
    attacks = [b'{"semantic_sha256":"","x":NaN}\n', b'{"x":1,"x":2}\n',
               b'{"semantic_sha256":""}', b'\xef\xbb\xbf{"semantic_sha256":""}\n',
               b'{"semantic_sha256":""}\r\n']
    passed = 0
    for index, raw in enumerate(attacks):
        try:
            strict_load(raw, f"negative-{index}")
        except ValidationFailure:
            passed += 1
        else:
            raise ValidationFailure("E_JSON_NEGATIVE_ESCAPE", str(index))
    return passed, len(attacks)


def policy_controls() -> tuple[int, int]:
    sources = [("import socket\n", "validator"), ("eval('1')\n", "validator"),
               ("import subprocess\nsubprocess.Popen(['x'])\n", "validator"),
               ("from pathlib import Path\nPath('x').write_text('x')\n", "validator")]
    git_attacks = [("branch", "x"), ("remote", "set-url", "origin", "x"),
                   ("diff", "--output=x", "HEAD"), ("status", "--short"),
                   ("rev-list", "--output=x", BASELINE, "--", *RELEASE_ROOTS)]
    passed = 0
    for source, kind in sources:
        require(source_policy_errors(source, kind), "E_POLICY_ESCAPE")
        passed += 1
    for attack in git_attacks:
        try:
            validate_git_argv(attack)
        except ValidationFailure:
            passed += 1
        else:
            raise ValidationFailure("E_GIT_POLICY_ESCAPE", repr(attack))
    require(persistence_parent_errors([EXPECTED_PARENT, "0" * 40]) == ["parents"],
            "E_MERGE_PARENT_NEGATIVE_ESCAPE")
    passed += 1
    return passed, len(sources) + len(git_attacks) + 1


def worktree_status() -> dict[str, str]:
    return parse_porcelain(str(git("status", "--porcelain=v1", "--untracked-files=all")))


def live_oid(ref: str) -> str:
    text = str(git("ls-remote", "--heads", "origin", ref))
    require("\t" in text, "E_LIVE_REF", ref)
    return text.split("\t", 1)[0]


def repository_refs(expected_tip: str) -> dict[str, Any]:
    record = {
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "head": git("rev-parse", "HEAD"),
        "upstream_name": git("rev-parse", "--abbrev-ref", "@{upstream}"),
        "upstream_oid": git("rev-parse", UPSTREAM),
        "active_tracking_oid": git("rev-parse", f"refs/remotes/{UPSTREAM}"),
        "active_live_oid": live_oid(f"refs/heads/{BRANCH}"),
        "origin": canonical_origin(str(git("ls-remote", "--get-url", "origin"))),
        "protected_local_oid": git("show-ref", "--verify", "--hash",
                                    "refs/heads/codex/lib-physics-endgame-v1025_2"),
        "protected_tracking_oid": git("rev-parse",
                                       "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        "protected_live_oid": live_oid("refs/heads/codex/lib-physics-endgame-v1025_2"),
        "main_local": git("show-ref", "--verify", "--hash", "refs/heads/main", check=False),
        "main_tracking_oid": git("rev-parse", "refs/remotes/origin/main"),
        "main_live_oid": live_oid("refs/heads/main"),
    }
    require(not repository_ref_errors(record, expected_tip), "E_REPOSITORY_REFS",
            repr(repository_ref_errors(record, expected_tip)))
    return record


def repository_ref_errors(record: dict[str, Any], expected_tip: str) -> list[str]:
    expected = {
        "branch": BRANCH, "head": expected_tip, "upstream_name": UPSTREAM,
        "upstream_oid": expected_tip, "active_tracking_oid": expected_tip,
        "active_live_oid": expected_tip, "origin": "github.com/lksz1412/project_anode_fit",
        "protected_local_oid": PROTECTED_TIP, "protected_tracking_oid": PROTECTED_TIP,
        "protected_live_oid": PROTECTED_TIP, "main_local": "",
        "main_tracking_oid": MAIN_TIP, "main_live_oid": MAIN_TIP,
    }
    return [key for key, value in expected.items() if record.get(key) != value]


def index_snapshot() -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in str(git("ls-files", "-s")).splitlines():
        meta, path = line.split("\t", 1)
        if path in FINAL_SET:
            mode, oid, stage = meta.split()
            require(stage == "0", "E_INDEX_STAGE")
            result[path] = (mode, oid)
    return result


def transaction_seal(expected_tip: str) -> dict[str, Any]:
    return {"repository_refs": repository_refs(expected_tip), "status": worktree_status(),
            "index": index_snapshot(),
            "path_hashes": {path: sha256((ROOT / path).read_bytes()) for path in FINAL_PATHS
                            if (ROOT / path).exists()},
            "manifest_git_blob_sha256": sha256(git("cat-file", "blob",
                f"{EXPECTED_PARENT}:{MANIFEST_PATH}", binary=True))}


def verify_content_worktree() -> None:
    status = worktree_status()
    expected = {path: ("??" if FINAL_STATUS[path] == "A" else " M") for path in FINAL_PATHS}
    require(status == expected, "E_CONTENT_PATHS", repr(status))
    require(not any(path.startswith("Claude/") for path in status), "E_CLAUDE_DIRTY")


def verify_staged() -> None:
    require(git("rev-parse", "--abbrev-ref", "HEAD") == BRANCH, "E_BRANCH")
    require(git("rev-parse", "HEAD") == EXPECTED_PARENT and git("rev-parse", UPSTREAM) == EXPECTED_PARENT,
            "E_STAGED_PARENT")
    staged = parse_name_status(str(git("diff", "--cached", "--name-status", "--no-renames", "HEAD")))
    require(staged == FINAL_STATUS, "E_STAGED_PATHS")
    require(git("diff", "--name-only") == "" and git("ls-files", "--others", "--exclude-standard") == "",
            "E_STAGED_DIRTY")
    require(git("diff", "--cached", "--check") == "", "E_DIFF_CHECK")
    index = index_snapshot()
    require(set(index) == FINAL_SET and all(mode == "100644" for mode, _ in index.values()), "E_INDEX_MODES")
    for path, (_, oid) in index.items():
        raw = (ROOT / path).read_bytes()
        require(git("show", f":{path}", binary=True) == raw and
                git("cat-file", "blob", oid, binary=True) == raw, "E_INDEX_BYTES", path)


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    return text.removesuffix(".git").strip("/")


def persistence_parent_errors(parents: list[str]) -> list[str]:
    return [] if parents == [EXPECTED_PARENT] else ["parents"]


def verify_persistence(commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "E_EXPECTED_COMMIT")
    require(git("rev-parse", "--abbrev-ref", "HEAD") == BRANCH and git("rev-parse", "HEAD") == commit,
            "E_HEAD")
    parents = str(git("show", "-s", "--format=%P", commit)).split()
    require(not persistence_parent_errors(parents), "E_COMMIT_PARENTS", repr(parents))
    require(git("rev-parse", f"{commit}^") == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(git("show", "-s", "--format=%s", commit) == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT")
    changed = parse_name_status(str(git("diff-tree", "--no-commit-id", "--name-status", "--no-renames",
                                         "-r", f"{commit}^", commit)))
    require(changed == FINAL_STATUS, "E_COMMIT_PATHS")
    tree = parse_ls_tree(str(git("ls-tree", "-r", commit)))
    require(all(tree.get(path, (None,))[0] == "100644" for path in FINAL_PATHS), "E_COMMIT_MODES")
    require(git("status", "--porcelain") == "", "E_WORKTREE_DIRTY")
    require(git("rev-parse", "--abbrev-ref", "@{upstream}") == UPSTREAM,
            "E_UPSTREAM_NAME")
    require(git("rev-parse", UPSTREAM) == commit and git("rev-parse", f"refs/remotes/{UPSTREAM}") == commit,
            "E_TRACKING")
    live = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"))
    require(live.split("\t", 1)[0] == commit, "E_LIVE_REMOTE")
    require(canonical_origin(str(git("ls-remote", "--get-url", "origin"))) ==
            "github.com/lksz1412/project_anode_fit", "E_ORIGIN")
    require(git("show-ref", "--verify", "--hash",
                "refs/heads/codex/lib-physics-endgame-v1025_2") == PROTECTED_TIP, "E_PROTECTED")
    require(git("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2") ==
            PROTECTED_TIP, "E_PROTECTED_TRACKING")
    require(str(git("ls-remote", "--heads", "origin",
                    "refs/heads/codex/lib-physics-endgame-v1025_2")).split("\t", 1)[0] == PROTECTED_TIP,
            "E_PROTECTED_LIVE")
    require(git("show-ref", "--verify", "--hash", "refs/heads/main", check=False) == "" and
            git("rev-parse", "refs/remotes/origin/main") == MAIN_TIP and
            str(git("ls-remote", "--heads", "origin", "refs/heads/main")).split("\t", 1)[0] == MAIN_TIP,
            "E_MAIN")
    require(git("diff", "--name-only", PROTECTED_TIP, "--", "Claude") == "", "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        require(git("show", f"{commit}:{path}", binary=True) == (ROOT / path).read_bytes(),
                "E_COMMITTED_BYTES", path)


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require((args.verify_persistence and args.expected_commit is not None) or
            (not args.verify_persistence and args.expected_commit is None), "E_EXPECTED_COMMIT_MODE")
    if args.verify_persistence:
        require(re.fullmatch(r"[0-9a-f]{40}", args.expected_commit or "") is not None,
                "E_EXPECTED_COMMIT")
    expected_tip = args.expected_commit if args.verify_persistence else EXPECTED_PARENT
    entry = transaction_seal(expected_tip or "")
    verify_source_policy()
    inventory, nodes_a, depth_a = strict_load((ROOT / INVENTORY_PATH).read_bytes(), INVENTORY_PATH)
    attestation, nodes_b, depth_b = strict_load((ROOT / ATTESTATION_PATH).read_bytes(), ATTESTATION_PATH)
    require(not artifact_errors(inventory, attestation), "E_ARTIFACT",
            repr(artifact_errors(inventory, attestation)[:8]))
    (occurrence_count, blob_count, line_count, ast_kinds, genealogy_commits,
     genealogy_passed, genealogy_total) = independent_projection(inventory, attestation)
    verify_controls(inventory, attestation)
    control_passed, control_total = control_document_negative_controls()
    semantic_passed, semantic_total = negative_controls(
        inventory, attestation, entry["repository_refs"], expected_tip or "")
    json_passed, json_total = strict_json_controls()
    policy_passed, policy_total = policy_controls()
    if args.content_only:
        verify_content_worktree()
    elif args.verify_staged:
        verify_staged()
    else:
        verify_persistence(args.expected_commit or "")
    terminal = transaction_seal(expected_tip or "")
    require(entry == terminal, "E_TRANSACTION_SEAL")
    print(f"PASS_P067_STEP82_CONTROLS semantic={semantic_passed}/{semantic_total} "
          f"genealogy={genealogy_passed}/{genealogy_total} strict_json={json_passed}/{json_total} "
          f"source_git={policy_passed}/{policy_total} control_docs={control_passed}/{control_total}")
    print(f"PASS_P067_STEP82_CONTENT occurrences={occurrence_count} unique={blob_count} lines={line_count} "
          f"releases=20 ast_kinds={ast_kinds} genealogy_commits={genealogy_commits} "
          f"nodes={nodes_a + nodes_b} depth={max(depth_a, depth_b)}")
    if args.content_only:
        print(f"{GATE} mode=CONTENT_ONLY exact-eight=8/8")
    elif args.verify_staged:
        print(f"{GATE} mode=STAGED exact-eight=8/8")
    else:
        print(f"{PERSISTENCE} commit={args.expected_commit} exact-eight=8/8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationFailure, KeyError, IndexError, TypeError, ValueError, OSError,
            UnicodeError, subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, ValidationFailure) else type(error).__name__
        print(f"FAIL_P067_STEP82 {code}: {error}")
        raise SystemExit(1)
