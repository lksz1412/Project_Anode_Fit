#!/usr/bin/env python3
"""Validate Phase 065 Step 70 source/process topology artifacts."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_PARENT = "83323ebfff1c468e4ada5e695ced10c69e24fb32"
EXPECTED_SUBJECT = "audit(phase065): freeze v1024 source process topology"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EXPECTED_UPSTREAM = f"origin/{BRANCH}"
EXPECTED_ORIGIN_IDENTITY = "github.com/lksz1412/project_anode_fit"

TOPOLOGY = "Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION = "Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json"
RESULT = "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
BUILDER = "Codex/work/v1024_phase065/build_phase065_step70.py"
VALIDATOR = "Codex/work/v1024_phase065/validate_phase065_step70.py"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
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

EXACT_PATHS = (
    BUILDER,
    VALIDATOR,
    TOPOLOGY,
    ATTESTATION,
    RESULT,
    PARENT_LEDGER,
    CANONICAL_LEDGER,
    HANDOVER,
)
EXPECTED_STATUS = {
    BUILDER: "A",
    VALIDATOR: "A",
    TOPOLOGY: "A",
    ATTESTATION: "A",
    RESULT: "A",
    PARENT_LEDGER: "M",
    CANONICAL_LEDGER: "M",
    HANDOVER: "M",
}
EXPECTED_PRE_EVIDENCE_STATUS = {
    BUILDER: "??",
    VALIDATOR: "??",
    RESULT: "??",
    PARENT_LEDGER: " M",
    CANONICAL_LEDGER: " M",
    HANDOVER: " M",
}

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
PROCESS_PARTITIONS = {
    "routed_process_ordinals_001_033": {"ordinals": [1, 33], "commits": 33, "patch_bytes": 455844, "patch_lines": 7878, "canonical_row_binding_sha256": "5e22f38eddbfafa1a19a0a293c2b36780b8b59fc285dc0ce1ddc824878348076"},
    "routed_process_ordinals_034_066": {"ordinals": [34, 66], "commits": 33, "patch_bytes": 2655327, "patch_lines": 66770, "canonical_row_binding_sha256": "a06de2b79da8acdcd8ca1cfb017e1f4e8177706f7f2a90cbd7747debd4ac748e"},
    "routed_process_ordinals_067_098": {"ordinals": [67, 98], "commits": 32, "patch_bytes": 9394733, "patch_lines": 32153, "canonical_row_binding_sha256": "e080af1a80e9907bf53872f5595a61266b0ffc6d7ff557fe51178dfe3f5869ca"},
}
ROUTED_PROCESS_CANONICAL_ROW_BINDING_SHA256 = "5c8ff3bc6f9f3570c024c603d363a7663210335ff950f5f279cf4e2fc5240ac2"
HUMAN_READ_STATUSES = {"DIRECT_READ", "AGENT_FULL_READ"}
EXPECTED_BASE_FINDING_IDS = tuple(f"P065-S70-F{index:02d}" for index in range(1, 6))
EXPECTED_ROUTED_FINDING_IDS = tuple(f"P065-S70-F{index:02d}" for index in range(6, 45))
EXPECTED_FINDING_IDS = (*EXPECTED_BASE_FINDING_IDS, *EXPECTED_ROUTED_FINDING_IDS)
BASE_FINDING_SCHEMA = {"id", "status", "finding"}
ROUTED_FINDING_SCHEMA = {"id", "severity", "status", "summary", "owner", "target_steps", "authority_promoted"}
READER_REPORT_SCHEMA = {
    "reader_id", "assignments", "report_path", "report_section",
    "report_binding_sha256", "finding_ids", "unreviewed_intervals",
    "output_truncation_unresolved",
}
ASSIGNMENT_SCHEMA = {"group_id", "record_count", "record_manifest_sha256", "binding_sha256", "status"}
READ_ONLY_GIT_SUBCOMMANDS = {
    "branch", "cat-file", "diff", "diff-tree", "log", "ls-files", "ls-remote",
    "ls-tree", "rev-parse", "show", "show-ref", "status",
}
EXPECTED_SEMANTIC_DEFERRED_PATCH_INTERVALS = {70: (226, 3813), 98: (2012, 5599)}
ALLOWED_DIRECT_IMPORTS = {
    "argparse", "ast", "copy", "hashlib", "io", "json", "math", "os", "re",
    "subprocess", "sys", "tempfile",
}
ALLOWED_FROM_IMPORTS = {
    "__future__": {"annotations"},
    "collections": {"Counter", "defaultdict"},
    "pathlib": {"Path", "PurePosixPath"},
    "PIL": {"Image"},
    "pypdf": {"PdfReader"},
    "typing": {"Any"},
}
SENSITIVE_MODULE_NAMES = ALLOWED_DIRECT_IMPORTS | {"Image"}
ALLOWED_MODULE_ATTRIBUTE_CHAINS = {
    "Image.open",
    "argparse.ArgumentParser",
    "ast.AST", "ast.AnnAssign", "ast.Assign", "ast.AsyncFunctionDef", "ast.Attribute",
    "ast.Call", "ast.ClassDef", "ast.Constant", "ast.Del", "ast.ExceptHandler",
    "ast.FunctionDef", "ast.Global", "ast.Import", "ast.ImportFrom", "ast.List", "ast.Load",
    "ast.MatchAs", "ast.MatchMapping", "ast.MatchStar", "ast.Module", "ast.Name",
    "ast.NamedExpr", "ast.Starred", "ast.Store", "ast.Tuple", "ast.dump",
    "ast.iter_child_nodes", "ast.parse", "ast.unparse", "ast.walk",
    "copy.deepcopy",
    "hashlib.sha256",
    "io.BytesIO",
    "json.JSONDecodeError", "json.dumps", "json.loads",
    "math.isfinite",
    "os.fsync", "os.replace",
    "re.compile", "re.fullmatch", "re.search",
    "subprocess.CompletedProcess", "subprocess.PIPE", "subprocess.run",
    "sys.modules", "sys.modules.pop", "sys.path", "sys.path.insert",
    "sys.stdout", "sys.stdout.reconfigure",
    "tempfile.NamedTemporaryFile",
}
EXPECTED_BUILDER_FUNCTION_SEQUENCE = (
    "require", "git_read_only_shape", "sha256_bytes", "lf_bytes", "line_count",
    "canonical_bytes", "semantic_hash", "_reject_pairs", "_reject_constant",
    "_walk_json", "strict_json", "run_process", "run_git", "git_text",
    "git_ref_blob", "git_blob", "git_ref_blob_id", "git_blob_id", "git_paths",
    "hash_rows", "parse_human_evidence", "manifest_topology", "record_for_path",
    "root_process_rule", "narrative_topology", "supplemental_topology",
    "comp_v24_topology", "classify_commit", "changed_statuses",
    "historical_blob_metadata", "process_classification_note",
    "process_binding_records", "process_rows", "reconcile_process_classifications",
    "require_process_projection_consistency", "reviewed_process_records",
    "strip_tex_comments", "resolve_tex_target", "tex_topology", "derived_topology",
    "observation_topology", "make_evidence_binding", "lf_interval",
    "semantic_deferred_intervals", "evidence_bindings", "build_core",
    "validate_evidence", "apply_human_evidence", "build_artifacts",
    "write_json_atomic", "main",
)
EXPECTED_VALIDATOR_FUNCTION_SEQUENCE = (
    "fail", "repo_root", "sha256_bytes", "canonical_bytes", "_reject_pairs",
    "_reject_constant", "_walk_json", "strict_loads", "read_json", "semantic_hash",
    "require", "git_read_only_shape", "reviewed_process_record",
    "machine_process_binding_records", "machine_evidence_records",
    "finding_rows_errors", "reader_report_errors", "artifact_errors", "load_builder",
    "source_policy_errors", "run_source_policy_negative_controls",
    "run_atomic_writer_contract_negative_controls",
    "run_required_function_inventory_negative_controls", "run_hardening_contract_probes",
    "run_evidence_contract_negative_controls", "run_finding_artifact_negative_controls",
    "run_process_projection_negative_controls", "markdown_table_row",
    "verify_in_progress_controls", "verify_in_progress_evidence_contract",
    "run_strict_json_negative_controls", "run_semantic_negative_controls",
    "run_process", "run_git", "parse_name_status", "frozen_source_record_errors",
    "verify_phase057_frozen_sources", "verified_lf_interval",
    "verify_semantic_deferred_sources", "run_semantic_boundary_contract",
    "run_phase057_frozen_source_negative_controls", "parse_porcelain",
    "live_remote_tip", "canonical_origin_identity", "require_repository_identity",
    "run_repository_identity_negative_controls", "verify_protection",
    "verify_pre_evidence_git_state", "verify_staged", "verify_persistence",
    "verify_result_and_controls", "validate", "main",
)
EXPECTED_ATOMIC_WRITER_SOURCE = """def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    allowed = {(ROOT / TOPOLOGY_PATH).resolve(), (ROOT / ATTESTATION_PATH).resolve()}
    require(path.resolve() in allowed, 'E_WRITE_TARGET', str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(mode='wb', dir=path.parent, prefix=f'.{path.name}.', suffix='.tmp', delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(canonical_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()"""
EXPECTED_ATOMIC_WRITER_CALLS = {
    "write_json_atomic(output_dir / Path(TOPOLOGY_PATH).name, topology)",
    "write_json_atomic(output_dir / Path(ATTESTATION_PATH).name, attestation)",
}
EXPECTED_LOAD_BUILDER_SOURCE = """def load_builder(root: Path):
    path = root / BUILDER
    if not path.is_file():
        fail('E_BUILDER_MISSING', str(path))
    module_dir = str(path.parent)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    sys.modules.pop('build_phase065_step70', None)
    import build_phase065_step70 as loaded_builder
    require(Path(loaded_builder.__file__).resolve() == path.resolve(), 'E_BUILDER_MODULE_IDENTITY', str(loaded_builder.__file__))
    return loaded_builder"""
EXPECTED_RUN_PROCESS_SOURCES = {
    """def run_process(root: Path, argv: list[str]) -> subprocess.CompletedProcess[bytes]:
    require(bool(argv) and argv[0] == 'git', 'E_PROCESS_NOT_GIT', repr(argv))
    return subprocess.run(argv, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)""",
    """def run_process(root: Path, argv: list[str], binary: bool=False) -> subprocess.CompletedProcess[Any]:
    require(bool(argv) and argv[0] == 'git', 'E_PROCESS_NOT_GIT', repr(argv))
    return subprocess.run(argv, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary, encoding=None if binary else 'utf-8', errors=None if binary else 'strict')""",
}
EXPECTED_RUN_GIT_SOURCES = {
    """def run_git(root: Path, *args: str) -> bytes:
    require(bool(args) and all((isinstance(arg, str) for arg in args)), 'E_GIT_ARGV')
    require(not args[0].startswith('-'), 'E_GIT_SUBCOMMAND', args[0])
    require(args[0] in READ_ONLY_GIT_SUBCOMMANDS, 'E_GIT_NOT_READ_ONLY', args[0])
    require(git_read_only_shape(tuple(args)), 'E_GIT_ARGV_SHAPE', repr(args))
    dangerous = ('-c', '--config-env', '--upload-pack', '--receive-pack', '--exec-path', '--ext-diff', '--textconv')
    dangerous_prefixes = ('--config=', '--config-env=', '--upload-pack=', '--receive-pack=', '--exec-path=')
    require(not any((arg in dangerous or arg.startswith(dangerous_prefixes) or arg.startswith('alias.') or arg.startswith('protocol.') for arg in args)), 'E_GIT_OPTION')
    require(not any((arg == '-o' or arg.startswith(('--output', '--config=', '--git-dir', '--work-tree')) for arg in args)), 'E_GIT_WRITE_OPTION')
    require(not any((arg.startswith('ext::') or arg.startswith('file://') for arg in args)), 'E_GIT_PROTOCOL')
    proc = run_process(root, ['git', *args])
    require(proc.returncode == 0, 'E_GIT', f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout""",
    """def run_git(root: Path, *args: str, check: bool=True, binary: bool=False) -> Any:
    require(bool(args) and all((isinstance(arg, str) for arg in args)), 'E_GIT_ARGV', repr(args))
    require(not args[0].startswith('-'), 'E_GIT_SUBCOMMAND', args[0])
    require(args[0] in READ_ONLY_GIT_SUBCOMMANDS, 'E_GIT_NOT_READ_ONLY', args[0])
    require(git_read_only_shape(tuple(args)), 'E_GIT_ARGV_SHAPE', repr(args))
    dangerous = ('-c', '--config-env', '--upload-pack', '--receive-pack', '--exec-path', '--ext-diff', '--textconv')
    dangerous_prefixes = ('--config=', '--config-env=', '--upload-pack=', '--receive-pack=', '--exec-path=')
    require(not any((arg in dangerous or arg.startswith(dangerous_prefixes) or arg.startswith('alias.') or arg.startswith('protocol.') for arg in args)), 'E_GIT_OPTION', repr(args))
    require(not any((arg == '-o' or arg.startswith(('--output', '--config=', '--git-dir', '--work-tree')) for arg in args)), 'E_GIT_WRITE_OPTION', repr(args))
    require(not any((arg.startswith('ext::') or arg.startswith('file://') for arg in args)), 'E_GIT_PROTOCOL', repr(args))
    proc = run_process(root, ['git', *args], binary=binary)
    if check and proc.returncode != 0:
        stderr = proc.stderr.decode('utf-8', 'replace') if binary else proc.stderr
        fail('E_GIT', f"git {' '.join(args)}: {stderr.strip()}")
    return proc.stdout""",
}


class ValidationFailure(RuntimeError):
    pass


def fail(code: str, detail: str) -> None:
    raise ValidationFailure(f"{code}: {detail}")


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists() or (parent / "Codex").is_dir():
            if (parent / "Codex" / "results").is_dir():
                return parent
    fail("E_REPO_ROOT", str(here))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            fail("E_JSON_DUPLICATE_KEY", key)
        out[key] = value
    return out


def _reject_constant(token: str) -> None:
    fail("E_JSON_NONFINITE", token)


def _walk_json(value: Any, path: str = "$") -> int:
    if value is None or isinstance(value, (str, bool)):
        return 1
    if isinstance(value, int):
        if abs(value) > 2**63 - 1:
            fail("E_JSON_INTEGER_RANGE", path)
        return 1
    if isinstance(value, float):
        if not math.isfinite(value):
            fail("E_JSON_NONFINITE", path)
        return 1
    if isinstance(value, list):
        return 1 + sum(_walk_json(item, f"{path}[{index}]") for index, item in enumerate(value))
    if isinstance(value, dict):
        return 1 + sum(_walk_json(item, f"{path}.{key}") for key, item in value.items())
    fail("E_JSON_TYPE", f"{path}: {type(value)}")


def strict_loads(data: bytes) -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail("E_JSON_UTF8", str(exc))
    try:
        value = json.loads(text, object_pairs_hook=_reject_pairs, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        fail("E_JSON_PARSE", str(exc))
    _walk_json(value)
    return value


def read_json(path: Path) -> Any:
    if not path.is_file():
        fail("E_ARTIFACT_MISSING", str(path))
    value = strict_loads(path.read_bytes())
    if path.read_bytes() != canonical_bytes(value):
        fail("E_JSON_NOT_CANONICAL", str(path))
    return value


def semantic_hash(value: dict[str, Any]) -> str:
    clone = copy.deepcopy(value)
    clone.pop("semantic_sha256", None)
    return sha256_bytes(canonical_bytes(clone))


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        fail(code, detail)


def git_read_only_shape(args: tuple[str, ...]) -> bool:
    if not args:
        return False
    command = args[0]
    if command == "cat-file":
        return len(args) == 3 and args[1] == "blob"
    if command == "rev-parse":
        return len(args) == 2 or args == ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if command == "ls-tree":
        return len(args) == 6 and args[1:4] == ("-r", "--name-only", BASELINE) and args[4] == "--"
    if command == "log":
        return len(args) >= 6 and args[1:4] == ("--reverse", "--format=%H", BASELINE) and args[4] == "--"
    if command == "diff-tree":
        raw_prefix = ("diff-tree", "--root", "--no-commit-id", "--raw", "--abbrev=40", "--no-renames", "-r")
        status_prefix = ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r")
        return (len(args) >= 8 and args[:7] == raw_prefix) or (len(args) == 7 and args[:5] == status_prefix)
    if command == "show":
        if len(args) == 4 and args[1] == "-s" and args[2] in {"--format=%P", "--format=%s"}:
            return True
        patch_prefix = ("show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv", "--find-renames", "--find-copies")
        return len(args) >= 10 and args[:7] == patch_prefix and args[8] == "--"
    if command == "ls-remote":
        return args == ("ls-remote", "--get-url", "origin") or (
            len(args) == 4 and args[1:3] == ("--heads", "origin") and args[3].startswith("refs/heads/")
        )
    if command == "branch":
        return args == ("branch", "--show-current")
    if command == "show-ref":
        return args == ("show-ref", "--verify", "--hash", "refs/heads/main")
    if command == "diff":
        return args in {
            ("diff", "--name-only"),
            ("diff", "--cached", "--check"),
            ("diff", "--cached", "--name-status", "--no-renames", "HEAD"),
            ("diff", "--name-only", BASELINE, "--", "Claude"),
        }
    if command == "status":
        return args in {
            ("status", "--porcelain"),
            ("status", "--porcelain=v1", "--untracked-files=all"),
            ("status", "--porcelain=v1", "--", "Claude"),
        }
    if command == "ls-files":
        return args == ("ls-files", "--others", "--exclude-standard")
    return False


def reviewed_process_record(row: dict[str, Any]) -> dict[str, Any]:
    return {
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
    }


def machine_process_binding_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
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


def machine_evidence_records(topology: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    unique = topology.get("unique_sources", [])
    code = [row for row in unique if row.get("review_mode") == "FULL_TEXT" and row.get("representative_path", "").endswith(".py")]
    code_blobs = {row["blob"] for row in code}
    documents = [row for row in unique if row.get("review_mode") == "FULL_TEXT" and row.get("blob") not in code_blobs]
    pdfs = [row for row in unique if row.get("review_mode") == "FULL_PDF"]
    images = [row for row in unique if row.get("review_mode") == "FULL_IMAGE"]

    def source_text(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{
            "blob": row["blob"], "source_ref": BASELINE, "paths": row["paths"],
            "bytes": row["size_bytes"], "lines": row["extent"]["lines"],
            "line_ranges": row["machine_extent_ranges"], "sha256_raw": row["sha256_raw"],
            "sha256_lf": row["sha256_lf"],
        } for row in sorted(rows, key=lambda item: item["blob"])]

    def path_text(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{
            "path": row["path"], "source_ref": row.get("source_ref", BASELINE), "blob": row["blob"],
            "bytes": row["bytes"], "lines": row["lines"], "line_ranges": row["machine_extent_ranges"],
            "sha256_raw": row["sha256_raw"], "sha256_lf": row["sha256_lf"],
        } for row in sorted(rows, key=lambda item: item["path"])]

    result = {
        "release_scientific_document_text": source_text(documents),
        "release_code_test_text": source_text(code),
        "release_pdf": [{
            "blob": row["blob"], "paths": row["paths"], "bytes": row["size_bytes"],
            "page_ranges": row["machine_extent_ranges"], "pages": row["extent"]["pages"],
            "sha256_raw": row["sha256_raw"],
        } for row in sorted(pdfs, key=lambda item: item["blob"])],
        "release_image": [{
            "blob": row["blob"], "paths": row["paths"], "bytes": row["size_bytes"],
            "image_ranges": row["machine_extent_ranges"], "image": row["image"], "sha256_raw": row["sha256_raw"],
        } for row in sorted(images, key=lambda item: item["blob"])],
        "supplemental_process_text": path_text(topology.get("supplemental", {}).get("records", [])),
        "narrative_history": path_text(topology.get("narrative", {}).get("records", [])),
    }
    comp = topology.get("comp_v24", {}).get("records", [])
    for extension, group_id in (("py", "comp_v24_python"), ("json", "comp_v24_json"), ("csv", "comp_v24_csv"), ("txt", "comp_v24_txt")):
        result[group_id] = path_text([row for row in comp if row.get("extension") == extension])
    result["comp_v24_png"] = [{
        "path": row["path"], "blob": row["blob"], "bytes": row["bytes"],
        "image_ranges": row["machine_extent_ranges"], "image": row["image"], "sha256_raw": row["sha256_raw"],
    } for row in sorted((row for row in comp if row.get("extension") == "png"), key=lambda item: item["path"])]
    release_rows = topology.get("process", {}).get("release", {}).get("commits", [])
    routed_rows = topology.get("process", {}).get("routed", {}).get("commits", [])
    result["release_process_all_038"] = [reviewed_process_record(row) for row in release_rows]
    for group_id, partition in PROCESS_PARTITIONS.items():
        first, last = partition["ordinals"]
        result[group_id] = [reviewed_process_record(row) for row in routed_rows[first - 1:last]]
    return result


def finding_rows_errors(rows: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(rows, list):
        return ["Step70 findings list"]
    identifiers = [row.get("id") if isinstance(row, dict) else None for row in rows]
    if identifiers != list(EXPECTED_FINDING_IDS):
        errors.append("Step70 finding exact ordered coverage")
    if len(identifiers) != len(set(identifiers)):
        errors.append("Step70 finding unique IDs")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"Step70 finding object {index + 1}")
            continue
        expected_schema = BASE_FINDING_SCHEMA if index < len(EXPECTED_BASE_FINDING_IDS) else ROUTED_FINDING_SCHEMA
        if set(row) != expected_schema:
            errors.append(f"Step70 finding schema {index + 1}")
        if index >= len(EXPECTED_BASE_FINDING_IDS):
            if row.get("severity") not in {"P0", "P1", "P2"}:
                errors.append(f"Step70 finding severity {index + 1}")
            if not isinstance(row.get("target_steps"), list) or not row.get("target_steps"):
                errors.append(f"Step70 finding targets {index + 1}")
            if row.get("authority_promoted") is not False:
                errors.append(f"Step70 finding authority {index + 1}")
    return errors


def reader_report_errors(readers: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(readers, list) or len(readers) < 3:
        return ["reader report list"]
    reader_ids: list[Any] = []
    finding_ids: list[Any] = []
    for index, reader in enumerate(readers):
        if not isinstance(reader, dict):
            errors.append(f"reader report object {index + 1}")
            continue
        if set(reader) != READER_REPORT_SCHEMA:
            errors.append(f"reader report schema {index + 1}")
        reader_ids.append(reader.get("reader_id"))
        if not isinstance(reader.get("reader_id"), str) or not reader.get("reader_id"):
            errors.append(f"reader report id {index + 1}")
        if reader.get("report_path") != RESULT or reader.get("report_section") != "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON":
            errors.append(f"reader report location {index + 1}")
        report_payload = {key: value for key, value in reader.items() if key != "report_binding_sha256"}
        if reader.get("report_binding_sha256") != sha256_bytes(canonical_bytes(report_payload)):
            errors.append(f"reader report binding {index + 1}")
        assignments = reader.get("assignments")
        if not isinstance(assignments, list) or not assignments or not all(isinstance(row, dict) and set(row) == ASSIGNMENT_SCHEMA for row in assignments):
            errors.append(f"reader report assignments {index + 1}")
        if reader.get("unreviewed_intervals") != [] or reader.get("output_truncation_unresolved") != []:
            errors.append(f"reader report incomplete {index + 1}")
        reported_findings = reader.get("finding_ids")
        if not isinstance(reported_findings, list) or len(reported_findings) != len(set(reported_findings)):
            errors.append(f"reader report finding IDs {index + 1}")
        else:
            finding_ids.extend(reported_findings)
    if len(reader_ids) != len(set(reader_ids)):
        errors.append("reader report duplicate ID")
    if len(finding_ids) != len(set(finding_ids)) or set(finding_ids) != set(EXPECTED_ROUTED_FINDING_IDS):
        errors.append("reader report exact finding coverage")
    return errors


def artifact_errors(topology: dict[str, Any], attestation: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def check(condition: bool, name: str) -> None:
        if not condition:
            errors.append(name)

    check(topology.get("schema_version") == "P065-S70-TOPOLOGY-1", "topology schema")
    check(attestation.get("schema_version") == "P065-S70-ATTESTATION-1", "attestation schema")
    check(topology.get("baseline_commit") == BASELINE, "topology baseline")
    check(attestation.get("baseline_commit") == BASELINE, "attestation baseline")
    check(topology.get("semantic_sha256") == semantic_hash(topology), "topology semantic hash")
    check(attestation.get("semantic_sha256") == semantic_hash(attestation), "attestation semantic hash")

    manifest = topology.get("manifest", {})
    expected_manifest = {
        "occurrences": 261,
        "unique_paths": 261,
        "unique_blobs": 131,
        "unique_text_blobs": 125,
        "unique_text_lines": 21618,
        "unique_pdfs": 3,
        "unique_pdf_pages": 148,
        "unique_images": 3,
        "unique_bytes": 7812647,
        "occurrence_bytes": 15622368,
        "shared_pairs": 130,
    }
    for key, expected in expected_manifest.items():
        check(manifest.get(key) == expected, f"manifest {key}")
    check(manifest.get("path_set_sha256") == PATH_SET_SHA256, "path set hash")
    check(manifest.get("path_blob_sha256") == PATH_BLOB_SHA256, "path/blob hash")
    check(manifest.get("unique_blob_sha256") == BLOB_SET_SHA256, "blob set hash")
    check(len(topology.get("occurrences", [])) == 261, "occurrence rows")
    check(len(topology.get("unique_sources", [])) == 131, "unique source rows")
    check(len({row.get("path") for row in topology.get("occurrences", [])}) == 261, "occurrence path uniqueness")
    check(len({row.get("blob") for row in topology.get("unique_sources", [])}) == 131, "unique blob uniqueness")
    check(all(row.get("read_status") in HUMAN_READ_STATUSES for row in topology.get("unique_sources", [])), "unique source human read status")
    check(all(row.get("read_ranges") == row.get("machine_extent_ranges") for row in topology.get("unique_sources", [])), "unique source exact ranges")
    check(all(set(row.get("human_review", {})) == {"group_id", "reader_id", "binding_sha256"} for row in topology.get("unique_sources", [])), "unique source human review binding")

    mirror = topology.get("mirror", {})
    check(mirror.get("shared_relative_paths") == 130, "mirror relative count")
    check(mirror.get("byte_identical_pairs") == 130, "mirror identical count")
    check(mirror.get("v1024_1_only") == ["ARCHIVE_NOTE.md"], "archive-only path")
    check(mirror.get("independent_corroboration") is False, "mirror authority")

    narrative = topology.get("narrative", {})
    check(narrative.get("copied_activation_claim") == {"documents": 29, "lines": 2068}, "copied narrative claim")
    check(narrative.get("corrected_root_process") == {"documents": 29, "lines": 2306}, "corrected root process")
    check(narrative.get("corrected_total") == {"documents": 74, "lines": 7470}, "corrected narrative total")
    check(narrative.get("correction_delta_lines") == 238, "narrative correction delta")
    check(len(narrative.get("records", [])) == 74, "narrative records")
    check(sum(row.get("lines", -10**9) for row in narrative.get("records", [])) == 7470, "narrative line sum")
    check(all(row.get("read_status") in HUMAN_READ_STATUSES for row in narrative.get("records", [])), "narrative full read")
    check(all(row.get("read_ranges") == row.get("machine_extent_ranges") for row in narrative.get("records", [])), "narrative exact ranges")

    comp = topology.get("comp_v24", {})
    check(comp.get("extension_counts") == {"csv": 10, "json": 16, "md": 31, "png": 33, "py": 29, "txt": 7}, "comp extension counts")
    check(comp.get("text_line_counts") == {"csv": 45203, "json": 1650, "md": 2635, "py": 2932, "txt": 171}, "comp line counts")
    check(len(comp.get("records", [])) == 126, "comp record rows")
    check(all(row.get("read_status") in HUMAN_READ_STATUSES for row in comp.get("records", [])), "comp full read")
    check(all(row.get("read_ranges") == row.get("machine_extent_ranges") for row in comp.get("records", [])), "comp exact ranges")
    check(len({row.get("path") for row in comp.get("records", [])}) == 126, "comp path uniqueness")

    process = topology.get("process", {})
    release = process.get("release", {})
    routed = process.get("routed", {})
    check(release.get("count") == 38, "release commit count")
    check(release.get("ordered_sha256") == RELEASE_SHA256, "release commit hash")
    check(release.get("process_query_argv") == ["git", "log", "--reverse", "--format=%H", BASELINE, "--", *RELEASE_PATHS], "release frozen process argv")
    check(routed.get("count") == 98, "routed commit count")
    check(routed.get("ordered_sha256") == ROUTED_SHA256, "routed commit hash")
    check(routed.get("process_query_argv") == ["git", "log", "--reverse", "--format=%H", BASELINE, "--", *ROUTED_PATHS], "routed frozen process argv")
    check(routed.get("merge_commits") == 0, "routed merge count")
    check(routed.get("patch_bytes") == 12505904, "routed patch bytes")
    check(routed.get("patch_lines") == 106801, "routed patch lines")
    check(routed.get("canonical_patch_row_binding_sha256") == ROUTED_PROCESS_CANONICAL_ROW_BINDING_SHA256, "routed canonical row binding")
    check(routed.get("canonical_patch_row_schema") == ["ordinal", "commit", "parents", "sha256_raw", "bytes", "lines"], "routed canonical row schema")
    canonical_rows = routed.get("canonical_patch_rows", [])
    check(len(canonical_rows) == 98, "routed canonical patch rows")
    check(sha256_bytes(canonical_bytes(canonical_rows)) == ROUTED_PROCESS_CANONICAL_ROW_BINDING_SHA256, "routed canonical rows recomputed")
    for group_id, partition in PROCESS_PARTITIONS.items():
        first, last = partition["ordinals"]
        rows = canonical_rows[first - 1:last]
        check(len(rows) == partition["commits"], f"{group_id} count")
        check(sum(row.get("bytes", -10**9) for row in rows) == partition["patch_bytes"], f"{group_id} bytes")
        check(sum(row.get("lines", -10**9) for row in rows) == partition["patch_lines"], f"{group_id} lines")
        check(sha256_bytes(canonical_bytes(rows)) == partition["canonical_row_binding_sha256"], f"{group_id} binding")
    check(len(release.get("commits", [])) == 38, "release commit rows")
    check(len(routed.get("commits", [])) == 98, "routed commit rows")
    for label, projection in (("release", release), ("routed", routed)):
        check(projection.get("patch_binding_schema") == "machine-process-projection-v1", f"{label} machine process binding schema")
        check(
            projection.get("patch_binding_sha256") == sha256_bytes(canonical_bytes(machine_process_binding_records(projection.get("commits", [])))),
            f"{label} machine process binding",
        )
    check(all(row.get("complete_diff_read") is True for row in release.get("commits", [])), "release complete patches")
    check(all(row.get("complete_diff_read") is True for row in routed.get("commits", [])), "routed complete patches")
    for label, projection in (("release", release), ("routed", routed)):
        for row in projection.get("commits", []):
            review = row.get("human_review", {})
            check(set(review) == {"group_id", "reader_id", "binding_sha256"}, f"{label} process human review {row.get('ordinal')}")
            for patch in row.get("parent_patches", []):
                check(patch.get("read_status") in HUMAN_READ_STATUSES, f"{label} patch read status {row.get('ordinal')}")
                expected_ranges = [[1, patch.get("lines")]] if patch.get("lines") else []
                check(patch.get("read_ranges") == expected_ranges, f"{label} patch exact read ranges {row.get('ordinal')}")
                check(patch.get("human_review") == review, f"{label} patch human review binding {row.get('ordinal')}")
    check(all(row.get("state_class") in {"proposal", "competition", "review", "patch", "build", "feedback_revision", "archive", "status"} for row in routed.get("commits", [])), "process state classes")
    process_classes: dict[str, int] = {}
    for row in routed.get("commits", []):
        label = row.get("state_class")
        process_classes[label] = process_classes.get(label, 0) + 1
    check(process_classes == {"archive": 1, "build": 6, "competition": 4, "feedback_revision": 21, "patch": 21, "proposal": 7, "review": 31, "status": 7}, "process class partition")
    check(all(row.get("classification_basis") == "CANONICAL_ROUTED_ORDINAL_WITH_SUBJECT_PATHS_BINARY_PATCH_CONTEXT" for row in routed.get("commits", [])), "process classification basis")
    check(all(row.get("classification_review") == "HUMAN_REVIEWED_SUBJECT_PATHS_BINARY_PATCH_AND_CANONICAL_ROUTING" for row in routed.get("commits", [])), "process classification review scope")
    check(all(isinstance(row.get("classification_notes"), str) and row.get("classification_notes") for row in routed.get("commits", [])), "process classification notes")
    check(all(set(row.get("human_review", {})) == {"group_id", "reader_id", "binding_sha256"} for row in routed.get("commits", [])), "process per-ordinal human review")
    routed_by_commit = {row.get("commit"): row for row in routed.get("commits", [])}
    for row in release.get("commits", []):
        canonical = routed_by_commit.get(row.get("commit"), {})
        check(
            all(row.get(field) == canonical.get(field) for field in ("state_class", "classification_basis", "classification_notes", "classification_review")),
            f"process cross-projection classification {row.get('commit')}",
        )
    check(all(all(change.get("old_blob") or change.get("new_blob") for change in row.get("full_commit_changed_paths", [])) for row in routed.get("commits", [])), "full process blob identities")
    check(all(all(change.get("old_blob") or change.get("new_blob") for change in row.get("routed_changed_paths", [])) for row in routed.get("commits", [])), "routed process blob identities")
    for row in routed.get("commits", []):
        full_by_path = {change.get("path"): change for change in row.get("full_commit_changed_paths", [])}
        check(all(full_by_path.get(change.get("path")) == change for change in row.get("routed_changed_paths", [])), f"routed path subset ordinal {row.get('ordinal')}")
        binary_by_path = {entry.get("path"): entry for entry in row.get("historical_binary", [])}
        expected_binary_paths = {change.get("path") for change in row.get("routed_changed_paths", []) if Path(str(change.get("path"))).suffix.lower() in {".pdf", ".png"}}
        check(set(binary_by_path) == expected_binary_paths, f"historical binary coverage ordinal {row.get('ordinal')}")
        for path, entry in binary_by_path.items():
            change = next(item for item in row.get("routed_changed_paths", []) if item.get("path") == path)
            for side in ("old", "new"):
                metadata = entry.get(side)
                blob = change.get(f"{side}_blob")
                if blob is None:
                    check(metadata is None, f"historical binary null {side} {path}")
                else:
                    check(isinstance(metadata, dict) and metadata.get("git_blob") == blob, f"historical binary blob {side} {path}")
                    check(isinstance(metadata.get("bytes"), int) and metadata.get("bytes") >= 0, f"historical binary bytes {side} {path}")
                    check(isinstance(metadata.get("sha256_raw"), str) and len(metadata.get("sha256_raw")) == 64, f"historical binary sha {side} {path}")
                    if Path(path).suffix.lower() == ".png":
                        check(set(metadata.get("image", {})) == {"width", "height", "mode"}, f"historical PNG dimensions {side} {path}")
                    else:
                        check(set(metadata.get("pdf", {})) == {"pages"}, f"historical PDF pages {side} {path}")

    tex = topology.get("tex", {})
    closures = tex.get("adopted_closures", {})
    check(closures.get("graphite", {}).get("files") == 34 and closures.get("graphite", {}).get("lines") == 5625, "graphite closure")
    check(closures.get("lco", {}).get("files") == 13 and closures.get("lco", {}).get("lines") == 1618, "lco closure")
    check(closures.get("si_blend", {}).get("files") == 11 and closures.get("si_blend", {}).get("lines") == 1143, "si closure")
    check(tex.get("adopted_union") == {"files": 56, "lines": 8218}, "tex adopted union")
    check(tex.get("non_master") == {"files": 34, "lines": 4489}, "tex non-master")

    observations = topology.get("phase057_observations", {})
    observation_rows = observations.get("records", [])
    expected_observations = {f"INTENT-PROV-{value:04d}" for value in (*range(228, 293), *range(388, 405))}
    check(observations.get("count") == 82, "Phase057 observation count")
    check(len(observation_rows) == 82, "Phase057 observation rows")
    check({row.get("id") for row in observation_rows} == expected_observations, "Phase057 observation IDs")
    check(all("P065_STEP75_DISPOSITION" in row.get("routes", []) for row in observation_rows), "Phase057 disposition routes")
    check(observations.get("later_corrections_are_original_evidence") is False, "Phase057 back-projection boundary")

    errors.extend(finding_rows_errors(topology.get("findings")))

    coverage = attestation.get("coverage", {})
    check(coverage.get("unique_sources") == {"read": 131, "required": 131}, "unique source coverage")
    check(coverage.get("text") == {"blobs": 125, "lines": 21618}, "text coverage")
    check(coverage.get("pdf") == {"documents": 3, "pages_extracted": 148, "pages_rendered": 148, "pages_visual": 148}, "PDF coverage")
    check(coverage.get("image") == {"images": 3, "original_resolution_visual": 3}, "image coverage")
    check(coverage.get("supplemental") == {"documents": 6, "lines": 728}, "supplemental coverage")
    check(coverage.get("narrative") == {"documents": 74, "lines": 7470}, "narrative coverage")
    check(coverage.get("comp_v24") == {"python": {"files": 29, "lines": 2932}, "json": {"files": 16, "lines": 1650}, "csv": {"files": 10, "lines": 45203}, "txt": {"files": 7, "lines": 171}, "png": {"files": 33, "original_resolution_visual": 33}}, "comp coverage")
    check(coverage.get("release_commits") == {"commits": 38, "complete_patches": 38}, "release patch coverage")
    check(coverage.get("routed_commits") == {"commits": 98, "complete_patches": 98, "patch_bytes": 12505904, "patch_lines": 106801}, "routed patch coverage")
    check(coverage.get("routed_partitions") == PROCESS_PARTITIONS, "routed partition coverage")
    check(attestation.get("unreviewed_intervals") == [], "unreviewed intervals")
    check(attestation.get("output_truncation_unresolved") == [], "truncation unresolved")
    check(topology.get("authority") == AUTHORITY_CEILING, "topology exact authority ceiling")
    check(attestation.get("authority") == AUTHORITY_CEILING, "attestation exact authority ceiling")
    bindings = attestation.get("bindings", {})
    check(set(bindings) == set(MANDATORY_EVIDENCE_GROUPS) and len(bindings) == len(MANDATORY_EVIDENCE_GROUPS), "mandatory evidence groups")
    check(all(group_id == binding.get("group_id") for group_id, binding in bindings.items()), "evidence group identity")
    check(all(set(binding) == {"group_id", "kind", "record_count", "record_manifest_sha256", "summary", "binding_sha256"} for binding in bindings.values()), "evidence binding schema")
    machine_records = machine_evidence_records(topology)
    check(set(machine_records) == set(MANDATORY_EVIDENCE_GROUPS), "machine evidence group coverage")
    for group_id, records in machine_records.items():
        binding = bindings.get(group_id, {})
        manifest_sha256 = sha256_bytes(canonical_bytes(records))
        expected_without_hash = {
            "group_id": group_id,
            "kind": binding.get("kind"),
            "record_count": len(records),
            "record_manifest_sha256": manifest_sha256,
            "summary": binding.get("summary"),
        }
        check(binding.get("record_count") == len(records), f"machine evidence count {group_id}")
        check(binding.get("record_manifest_sha256") == manifest_sha256, f"machine evidence manifest {group_id}")
        check(binding.get("binding_sha256") == sha256_bytes(canonical_bytes({"binding": expected_without_hash, "records": records})), f"machine evidence binding {group_id}")
    errors.extend(reader_report_errors(attestation.get("readers")))
    assignments = [assignment for reader in attestation.get("readers", []) if isinstance(reader, dict) for assignment in reader.get("assignments", [])]
    check(len(assignments) == len(MANDATORY_EVIDENCE_GROUPS), "evidence assignment count")
    check({assignment.get("group_id") for assignment in assignments} == set(MANDATORY_EVIDENCE_GROUPS), "evidence assignment coverage")
    check(len({assignment.get("group_id") for assignment in assignments}) == len(assignments), "evidence assignment duplicate")
    for assignment in assignments:
        binding = bindings.get(assignment.get("group_id"), {})
        check(assignment.get("record_count") == binding.get("record_count"), f"evidence assignment count {assignment.get('group_id')}")
        check(assignment.get("record_manifest_sha256") == binding.get("record_manifest_sha256"), f"evidence assignment manifest {assignment.get('group_id')}")
        check(assignment.get("binding_sha256") == binding.get("binding_sha256"), f"evidence assignment binding {assignment.get('group_id')}")
        visual = binding.get("kind") in {"FULL_PDF_EXTRACT_RENDER_VISUAL", "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL"}
        expected_statuses = {"AGENT_FULL_READ"} if visual else HUMAN_READ_STATUSES
        check(assignment.get("status") in expected_statuses, f"evidence assignment status {assignment.get('group_id')}")
    expected_deferred = sorted(
        [interval for binding in bindings.values() for interval in binding.get("summary", {}).get("semantic_deferred_intervals", [])],
        key=lambda row: row.get("interval_id", ""),
    )
    check(attestation.get("semantic_deferred_intervals") == expected_deferred, "semantic deferred interval binding")
    check(attestation.get("gate") == "PASS_P065_STEP70_PRECOMMIT", "attestation gate")
    check(attestation.get("topology_semantic_sha256") == topology.get("semantic_sha256"), "cross-artifact binding")
    return errors


def load_builder(root: Path):
    path = root / BUILDER
    if not path.is_file():
        fail("E_BUILDER_MISSING", str(path))
    module_dir = str(path.parent)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    sys.modules.pop("build_phase065_step70", None)
    import build_phase065_step70 as loaded_builder
    require(Path(loaded_builder.__file__).resolve() == path.resolve(), "E_BUILDER_MODULE_IDENTITY", str(loaded_builder.__file__))
    return loaded_builder


def source_policy_errors(source: str, expected_kind: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"syntax:{exc}"]
    parent: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node

    function_name_sequence = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    function_names = set(function_name_sequence)
    if len(function_name_sequence) != len(function_names):
        errors.append("duplicate-top-level-function")
    if expected_kind == "builder" and tuple(function_name_sequence) != EXPECTED_BUILDER_FUNCTION_SEQUENCE:
        errors.append("builder-function-inventory-contract")
    if expected_kind == "validator" and tuple(function_name_sequence) != EXPECTED_VALIDATOR_FUNCTION_SEQUENCE:
        errors.append("validator-function-inventory-contract")
    if expected_kind in {"builder", "validator"} and any(isinstance(node, ast.AsyncFunctionDef) for node in tree.body):
        errors.append(f"{expected_kind}-async-top-level-function")
    is_builder_source = {"build_artifacts", "process_rows", "write_json_atomic"}.intersection(function_names)
    writers = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "write_json_atomic"]
    if is_builder_source and len(writers) != 1:
        errors.append("atomic-writer-required")
    if writers:
        if len(writers) != 1 or ast.unparse(writers[0]) != EXPECTED_ATOMIC_WRITER_SOURCE:
            errors.append("atomic-writer-definition-contract")
        writer_calls = {
            ast.unparse(node)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "write_json_atomic"
        }
        if writer_calls != EXPECTED_ATOMIC_WRITER_CALLS:
            errors.append("atomic-writer-callsite-contract")
        module_literals = {
            target.id: node.value.value
            for node in tree.body
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)
            for target in node.targets
            if isinstance(target, ast.Name) and target.id in {"TOPOLOGY_PATH", "ATTESTATION_PATH"}
        }
        if module_literals != {"TOPOLOGY_PATH": TOPOLOGY, "ATTESTATION_PATH": ATTESTATION}:
            errors.append("atomic-writer-output-constant-contract")
    loaders = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "load_builder"]
    if "source_policy_errors" in function_names and len(loaders) != 1:
        errors.append("load-builder-required")
    if loaders and (len(loaders) != 1 or not isinstance(loaders[0], ast.FunctionDef) or ast.unparse(loaders[0]) != EXPECTED_LOAD_BUILDER_SOURCE):
        errors.append("load-builder-definition-contract")
    process_wrappers = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "run_process"]
    if process_wrappers and (len(process_wrappers) != 1 or not isinstance(process_wrappers[0], ast.FunctionDef) or ast.unparse(process_wrappers[0]) not in EXPECTED_RUN_PROCESS_SOURCES):
        errors.append("run-process-definition-contract")
    git_wrappers = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "run_git"]
    if git_wrappers and (len(git_wrappers) != 1 or not isinstance(git_wrappers[0], ast.FunctionDef) or ast.unparse(git_wrappers[0]) not in EXPECTED_RUN_GIT_SOURCES):
        errors.append("run-git-definition-contract")

    def owner(node: ast.AST) -> str:
        cur = node
        while cur in parent:
            cur = parent[cur]
            if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return cur.name if isinstance(parent.get(cur), ast.Module) else f"<nested:{cur.name}>"
        return "<module>"

    forbidden_names = {
        "eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr",
        "globals", "locals", "vars", "breakpoint",
    }
    forbidden_attrs = {
        "system", "popen", "Popen", "call", "check_call", "check_output", "run_path",
        "run_module", "exec_module", "import_module", "remove", "rmtree", "move",
        "copyfile", "copy2", "copytree", "makedirs", "hardlink_to", "symlink_to",
        "FileIO", "partial", "getoutput", "getstatusoutput", "create_subprocess_exec",
        "create_subprocess_shell", "Process", "writelines", "truncate", "ftruncate",
        "chmod", "fchmod", "lchmod", "chown", "fchown", "lchown", "utime", "mknod",
        "mkfifo", "putenv", "unsetenv", "chdir", "save", "write_stream",
    }
    sensitive_callable_attrs = forbidden_attrs | {
        "run", "NamedTemporaryFile", "TemporaryFile", "mkstemp", "mkdtemp", "mkdir",
        "unlink", "write", "write_text", "write_bytes", "touch", "rename", "rmdir", "removedirs",
        "symlink", "link", "open",
    }
    mutator_owners = {
        "mkdir": {"write_json_atomic"},
        "replace": {"write_json_atomic"},
        "unlink": {"write_json_atomic"},
        "write_text": set(),
        "write_bytes": set(),
        "touch": set(),
        "rename": set(),
        "rmdir": set(),
        "removedirs": set(),
        "remove": set(),
        "rmtree": set(),
        "makedirs": set(),
        "hardlink_to": set(),
        "symlink_to": set(),
        "move": set(),
        "copyfile": set(),
        "copy2": set(),
        "copytree": set(),
        "symlink": set(),
        "link": set(),
    }
    allowed_atomic_calls = {
        "path.parent.mkdir(parents=True, exist_ok=True)",
        "tempfile.NamedTemporaryFile(mode='wb', dir=path.parent, prefix=f'.{path.name}.', suffix='.tmp', delete=False)",
        "handle.write(canonical_bytes(value))",
        "os.replace(temporary, path)",
        "temporary.unlink()",
    }
    allowed_lf_replace_calls = {
        "data.replace(b'\\r\\n', b'\\n')",
        "data.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')",
        "raw.replace(b'\\r\\n', b'\\n')",
        "raw.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')",
        "html_raw.replace(b'\\r\\n', b'\\n')",
        "html_raw.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')",
        "patch.replace(b'\\r\\n', b'\\n')",
        "patch.replace(b'\\r\\n', b'\\n').replace(b'\\r', b'\\n')",
    }
    dangerous_git_literals = {
        "-c",
        "--config-env",
        "--upload-pack",
        "--receive-pack",
        "--exec-path",
        "--ext-diff",
        "--textconv",
    }
    dangerous_git_prefixes = (
        "--config=", "--config-env=", "--upload-pack=", "--receive-pack=",
        "--exec-path=", "--output", "--git-dir", "--work-tree",
    )
    allowed_run_git_owners = {
        "git_text", "git_ref_blob", "git_paths", "changed_statuses", "historical_blob_metadata",
        "process_rows", "semantic_deferred_intervals", "live_remote_tip", "verify_protection",
        "verify_staged", "verify_persistence", "verify_pre_evidence_git_state",
        "verify_phase057_frozen_sources", "verify_semantic_deferred_sources",
        "run_semantic_boundary_contract",
    }

    def sensitive_callable_expression(value: ast.AST) -> bool:
        if isinstance(value, ast.Call):
            return False
        for item in ast.walk(value):
            cursor = item
            inside_call = False
            while cursor is not value and cursor in parent:
                cursor = parent[cursor]
                if isinstance(cursor, ast.Call):
                    inside_call = True
                    break
            if inside_call:
                continue
            if isinstance(parent.get(item), ast.Call) and parent[item].func is item:
                continue
            if isinstance(item, ast.Name) and item.id in {"open", "run_git", "run_process", "print"} | SENSITIVE_MODULE_NAMES:
                return True
            if isinstance(item, ast.Attribute) and item.attr in forbidden_attrs | {"run", "NamedTemporaryFile", "TemporaryFile", "mkstemp", "mkdtemp"} | set(mutator_owners):
                return True
        return False

    def literal_strings(call: ast.Call) -> list[str]:
        return [argument.value for argument in call.args if isinstance(argument, ast.Constant) and isinstance(argument.value, str)]

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.decorator_list:
                errors.append(f"function-decorator:{node.name}@{owner(node)}")
            if owner(node) == "<module>" and not isinstance(parent.get(node), ast.Module):
                errors.append(f"conditional-top-level-function:{node.name}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id == "__builtins__":
            errors.append(f"builtins-namespace-reference@{owner(node)}")
        if owner(node) == "<module>" and isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and node.id in function_names:
            errors.append(f"top-level-function-rebinding:{node.id}")
        if owner(node) == "<module>" and isinstance(node, ast.ClassDef) and node.name in function_names:
            errors.append(f"top-level-function-class-rebinding:{node.name}")
        if owner(node) == "<module>" and isinstance(node, ast.ExceptHandler) and node.name in function_names:
            errors.append(f"top-level-function-exception-rebinding:{node.name}")
        if owner(node) == "<module>" and isinstance(node, (ast.MatchAs, ast.MatchStar, ast.MatchMapping)):
            pattern_names = [node.name] if isinstance(node, (ast.MatchAs, ast.MatchStar)) else [node.rest]
            for pattern_name in pattern_names:
                if pattern_name in function_names:
                    errors.append(f"top-level-function-pattern-rebinding:{pattern_name}")
        if isinstance(node, ast.Global):
            for global_name in node.names:
                if global_name in function_names:
                    errors.append(f"global-function-rebinding:{global_name}@{owner(node)}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in SENSITIVE_MODULE_NAMES:
            if not isinstance(parent.get(node), ast.Attribute) or parent[node].value is not node:
                errors.append(f"sensitive-namespace-reference:{node.id}@{owner(node)}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id == "print":
            if not isinstance(parent.get(node), ast.Call) or parent[node].func is not node:
                errors.append(f"sensitive-name-reference:print@{owner(node)}")
        if isinstance(node, ast.Attribute):
            rendered_attribute = ast.unparse(node)
            attribute_root: ast.AST = node
            while isinstance(attribute_root, ast.Attribute):
                attribute_root = attribute_root.value
            if isinstance(attribute_root, ast.Name) and attribute_root.id in SENSITIVE_MODULE_NAMES and rendered_attribute not in ALLOWED_MODULE_ATTRIBUTE_CHAINS:
                errors.append(f"module-attribute-chain:{rendered_attribute}@{owner(node)}")
            if rendered_attribute.startswith("os.environ"):
                errors.append(f"os-environ-reference@{owner(node)}")
            if rendered_attribute.startswith("sys."):
                allowed_sys_attribute = (
                    owner(node) == "load_builder" and rendered_attribute in {"sys.path", "sys.path.insert", "sys.modules", "sys.modules.pop"}
                ) or (
                    owner(node) == "main" and rendered_attribute in {"sys.stdout", "sys.stdout.reconfigure"}
                )
                if not allowed_sys_attribute:
                    errors.append(f"sys-namespace-reference:{rendered_attribute}@{owner(node)}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in {"open", "run_git", "run_process"}:
            direct = isinstance(parent.get(node), ast.Call) and parent[node].func is node
            if not direct:
                errors.append(f"sensitive-name-reference:{node.id}@{owner(node)}")
        if isinstance(node, ast.Attribute) and node.attr in sensitive_callable_attrs:
            direct_call = isinstance(parent.get(node), ast.Call) and parent[node].func is node
            allowed_direct = direct_call and (
                (node.attr == "run" and owner(parent[node]) == "run_process" and ast.unparse(node) == "subprocess.run")
                or (owner(parent[node]) == "write_json_atomic" and ast.unparse(parent[node]) in allowed_atomic_calls)
                or (node.attr == "open" and ast.unparse(node) == "Image.open")
            )
            if not allowed_direct:
                errors.append(f"sensitive-attribute-reference:{node.attr}@{owner(node)}")
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            if owner(node) == "<module>":
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(not isinstance(target, (ast.Name, ast.Tuple)) for target in targets):
                    errors.append("module-level-mutation-target")
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(ast.unparse(target).startswith("os.environ[") for target in targets):
                errors.append("os-environ-mutation")
            value = node.value
            if sensitive_callable_expression(value):
                errors.append(f"sensitive-callable-alias@{owner(node)}")
            if isinstance(value, ast.Name) and value.id in forbidden_names:
                errors.append(f"forbidden-builtin-alias:{value.id}@{owner(node)}")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defaults = [*node.args.defaults, *(item for item in node.args.kw_defaults if item is not None)]
            if any(sensitive_callable_expression(value) for value in defaults):
                errors.append(f"sensitive-callable-default@{node.name}")
        if isinstance(node, ast.Import):
            if len(node.names) != 1:
                errors.append(f"multi-import@{owner(node)}")
            for alias in node.names:
                bound_name = alias.asname or alias.name.split(".", 1)[0]
                if owner(node) == "<module>" and bound_name in function_names:
                    errors.append(f"top-level-function-import-rebinding:{bound_name}")
                exact_builder_import = owner(node) == "load_builder" and alias.name == "build_phase065_step70" and alias.asname == "loaded_builder"
                if alias.name not in ALLOWED_DIRECT_IMPORTS and not exact_builder_import:
                    errors.append(f"unexpected-import:{alias.name}@{owner(node)}")
                if alias.asname is not None and not exact_builder_import:
                    errors.append(f"sensitive-namespace-alias:{alias.name}@{owner(node)}")
        if isinstance(node, ast.ImportFrom):
            imported_names = {alias.name for alias in node.names}
            if node.module not in ALLOWED_FROM_IMPORTS or not imported_names <= ALLOWED_FROM_IMPORTS.get(node.module, set()):
                errors.append(f"unexpected-from-import:{node.module}@{owner(node)}")
            if node.module in {"subprocess", "os", "runpy", "importlib", "tempfile", "shutil", "functools"}:
                errors.append(f"sensitive-from-import:{node.module}@{owner(node)}")
            if any(alias.asname is not None for alias in node.names):
                errors.append(f"from-import-alias:{node.module}@{owner(node)}")
            for alias in node.names:
                bound_name = alias.asname or alias.name
                if owner(node) == "<module>" and bound_name in function_names:
                    errors.append(f"top-level-function-import-rebinding:{bound_name}")
        if isinstance(node, ast.Call):
            call_owner = owner(node)
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                errors.append(f"indirect-call-shape:{ast.dump(node.func, include_attributes=False).partition('(')[0]}@{call_owner}")
            if isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
                errors.append(f"forbidden-call:{node.func.id}@{call_owner}")
            if isinstance(node.func, ast.Name) and node.func.id == "print" and any(keyword.arg == "file" for keyword in node.keywords):
                errors.append(f"print-file-write@{call_owner}")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                module_name = node.func.value.id
                module_call = f"{module_name}.{node.func.attr}"
                if module_name == "subprocess" and ast.unparse(node) not in {
                    "subprocess.run(argv, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)",
                    "subprocess.run(argv, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary, encoding=None if binary else 'utf-8', errors=None if binary else 'strict')",
                }:
                    errors.append(f"subprocess-call-contract:{module_call}@{call_owner}")
                if module_name == "os" and ast.unparse(node) not in {
                    "os.fsync(handle.fileno())", "os.replace(temporary, path)"
                }:
                    errors.append(f"os-call-contract:{module_call}@{call_owner}")
                if module_name == "tempfile" and ast.unparse(node) not in allowed_atomic_calls:
                    errors.append(f"tempfile-call-contract:{module_call}@{call_owner}")
                if module_name == "io" and node.func.attr != "BytesIO":
                    errors.append(f"io-call-contract:{module_call}@{call_owner}")
                if module_name == "json" and node.func.attr not in {"loads", "dumps"}:
                    errors.append(f"json-call-contract:{module_call}@{call_owner}")
                if module_name == "Image" and node.func.attr != "open":
                    errors.append(f"image-call-contract:{module_call}@{call_owner}")
            if ast.unparse(node.func) == "sys.stdout.reconfigure" and ast.unparse(node) != "sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')":
                errors.append(f"sys-stdout-call-contract@{call_owner}")
            is_name_open = isinstance(node.func, ast.Name) and node.func.id == "open"
            is_attribute_open = (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "open"
                and not (isinstance(node.func.value, ast.Name) and node.func.value.id == "Image")
            )
            if is_name_open or is_attribute_open:
                if any(keyword.arg is None for keyword in node.keywords):
                    errors.append(f"dynamic-open-keywords@{call_owner}")
                if is_attribute_open and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    errors.append(f"filesystem-os-open@{call_owner}")
                if is_name_open or (is_attribute_open and isinstance(node.func.value, ast.Name) and node.func.value.id == "io"):
                    mode_node: ast.AST | None = node.args[1] if len(node.args) >= 2 else None
                else:
                    mode_node = node.args[0] if node.args else None
                for keyword in node.keywords:
                    if keyword.arg == "mode":
                        mode_node = keyword.value
                if mode_node is not None:
                    if not isinstance(mode_node, ast.Constant) or not isinstance(mode_node.value, str):
                        errors.append(f"dynamic-open-mode@{call_owner}")
                    elif any(token in mode_node.value for token in "wax+"):
                        errors.append(f"filesystem-open-write:{mode_node.value}@{call_owner}")
            if isinstance(node.func, ast.Name) and node.func.id == "run_git":
                if call_owner not in allowed_run_git_owners:
                    errors.append(f"run-git-outside-allowlist@{call_owner}")
                strings = literal_strings(node)
                allowed_dynamic_git_calls = {
                    "run_git(root, *args)",
                    "run_git(root, *process_query_argv[1:])",
                }
                if len(node.args) < 2:
                    errors.append(f"git-missing-subcommand@{call_owner}")
                elif isinstance(node.args[1], ast.Starred):
                    if ast.unparse(node) not in allowed_dynamic_git_calls:
                        errors.append(f"git-dynamic-argv-shape@{call_owner}")
                elif not isinstance(node.args[1], ast.Constant) or not isinstance(node.args[1].value, str):
                    errors.append(f"git-dynamic-subcommand@{call_owner}")
                elif node.args[1].value in {"branch", "show-ref", "ls-remote"} and any(isinstance(argument, ast.Starred) for argument in node.args[2:]):
                    errors.append(f"git-starred-options@{call_owner}")
                literal_argv = tuple(
                    argument.value
                    for argument in node.args[1:]
                    if isinstance(argument, ast.Constant) and isinstance(argument.value, str)
                )
                all_literal_argv = len(literal_argv) == len(node.args) - 1 and not any(isinstance(argument, ast.Starred) for argument in node.args[1:])
                if all_literal_argv and not git_read_only_shape(literal_argv):
                    errors.append(f"git-argv-shape@{call_owner}")
                if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str):
                    if node.args[1].value not in READ_ONLY_GIT_SUBCOMMANDS:
                        errors.append(f"git-non-read-only-subcommand:{node.args[1].value}@{call_owner}")
                if any(value in dangerous_git_literals or value == "-o" or value.startswith(dangerous_git_prefixes) for value in strings):
                    errors.append(f"unsafe-git-option@{call_owner}")
                if any(value.startswith("alias.") or value.startswith("protocol.") or value.startswith("ext::") or value.startswith("file://") for value in strings):
                    errors.append(f"unsafe-git-protocol-or-alias@{call_owner}")
            if isinstance(node.func, ast.Name) and node.func.id == "run_process":
                if call_owner != "run_git":
                    errors.append(f"run-process-outside-git-wrapper@{call_owner}")
                if ast.unparse(node) not in {
                    "run_process(root, ['git', *args])",
                    "run_process(root, ['git', *args], binary=binary)",
                }:
                    errors.append(f"run-process-call-contract@{call_owner}")
                argv = node.args[1] if len(node.args) >= 2 else None
                safe_git_argv = (
                    isinstance(argv, ast.List)
                    and bool(argv.elts)
                    and isinstance(argv.elts[0], ast.Constant)
                    and argv.elts[0].value == "git"
                )
                if not safe_git_argv:
                    errors.append(f"run-process-non-git-literal@{call_owner}")
            if isinstance(node.func, ast.Attribute):
                attr = node.func.attr
                if attr in forbidden_attrs:
                    errors.append(f"forbidden-attribute:{attr}@{call_owner}")
                if attr == "run":
                    if call_owner != "run_process":
                        errors.append(f"subprocess-run-outside-wrapper@{call_owner}")
                if attr in {"NamedTemporaryFile", "TemporaryFile", "mkstemp", "mkdtemp"} and call_owner != "write_json_atomic":
                    errors.append(f"tempfile-creation:{attr}@{call_owner}")
                if attr in {"NamedTemporaryFile", "write", "mkdir", "unlink"} and call_owner == "write_json_atomic":
                    if ast.unparse(node) not in allowed_atomic_calls:
                        errors.append(f"atomic-writer-call-shape:{attr}@{call_owner}")
                if attr == "replace":
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                        if call_owner not in mutator_owners[attr] or ast.unparse(node) not in allowed_atomic_calls:
                            errors.append(f"filesystem-mutator:{attr}@{call_owner}")
                    elif not (
                        ast.unparse(node) in allowed_lf_replace_calls
                        or (call_owner == "run_atomic_writer_contract_negative_controls" and ast.unparse(node).startswith("source.replace("))
                    ):
                        errors.append(f"filesystem-or-unapproved-replace@{call_owner}")
                elif attr in mutator_owners and call_owner not in mutator_owners[attr]:
                    errors.append(f"filesystem-mutator:{attr}@{call_owner}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__") and not (
            owner(node) == "load_builder" and ast.unparse(node) == "loaded_builder.__file__"
        ):
            errors.append(f"dunder-attribute:{node.attr}@{owner(node)}")
    return errors


SOURCE_POLICY_ATTACKS = {
    "builtin-eval": "eval('1')",
    "builtin-exec": "exec('x=1')",
    "builtin-compile": "compile('1','','exec')",
    "builtin-breakpoint": "breakpoint()",
    "builtin-dynamic-import": "__import__('os')",
    "importlib-dynamic-import": "import importlib\nimportlib.import_module('os')",
    "os-system": "import os\nos.system('echo bad')",
    "subprocess-popen": "import subprocess\nsubprocess.Popen(['x'])",
    "subprocess-run-outside-wrapper": "import subprocess\ndef x(): subprocess.run(['x'])",
    "subprocess-callable-alias": "import subprocess\nr = subprocess.run\nr(['x'])",
    "subprocess-tuple-alias": "import subprocess\nr, = (subprocess.run,)\nr(['x'])",
    "subprocess-subscript-alias": "import subprocess\nr = [subprocess.run][0]\nr(['x'])",
    "subprocess-inline-list-dispatch": "import subprocess\n[subprocess.run][0](['x'])",
    "subprocess-inline-dict-dispatch": "import subprocess\n{'r': subprocess.run}['r'](['x'])",
    "subprocess-inline-lambda-dispatch": "import subprocess\n(lambda f: f)(subprocess.run)(['x'])",
    "subprocess-returned-callable-dispatch": "import subprocess\ndef pick(): return subprocess.run\npick()(['x'])",
    "subprocess-vars-dispatch": "import subprocess\nvars(subprocess)['run'](['x'])",
    "subprocess-partial-dispatch": "import subprocess, functools\nfunctools.partial(subprocess.run, ['x'])()",
    "subprocess-getoutput": "import subprocess\nsubprocess.getoutput('x')",
    "asyncio-subprocess-shell": "import asyncio\nasyncio.create_subprocess_shell('x')",
    "multiprocessing-process": "import multiprocessing\nmultiprocessing.Process(target=print)",
    "subprocess-default-callback": "import subprocess\ndef x(callback=subprocess.run): pass",
    "subprocess-map-callback": "import subprocess\nmap(subprocess.run, [['x']])",
    "subprocess-from-import": "import subprocess\nfrom subprocess import run\nrun(['x'])",
    "dynamic-attribute-execution": "def x(o): return getattr(o, 'run')(['x'])",
    "runpy-execution": "import runpy\nrunpy.run_path('x.py')",
    "dunder-reflection": "def x(o): return o.__class__",
    "filesystem-unlink": "from pathlib import Path\ndef x(): Path('x').unlink()",
    "filesystem-mkdir-outside-writer": "from pathlib import Path\ndef x(): Path('x').mkdir()",
    "filesystem-rename": "import os\ndef x(): os.rename('a','b')",
    "filesystem-replace-alias": "import os\nr = os.replace\nr('a','b')",
    "filesystem-os-remove": "import os\ndef x(): os.remove('x')",
    "filesystem-shutil-rmtree": "import shutil\ndef x(): shutil.rmtree('x')",
    "filesystem-shutil-from-import-rmtree": "from shutil import rmtree\ndef x(): rmtree('x')",
    "filesystem-shutil-move": "import shutil\ndef x(): shutil.move('a', 'b')",
    "filesystem-shutil-copyfile": "import shutil\ndef x(): shutil.copyfile('a', 'b')",
    "filesystem-os-makedirs": "import os\ndef x(): os.makedirs('x')",
    "filesystem-os-open": "import os\ndef x(): os.open('x', os.O_WRONLY | os.O_CREAT)",
    "execution-os-execv": "import os\ndef x(): os.execv('x', ['x'])",
    "execution-os-spawnv": "import os\ndef x(): os.spawnv(os.P_WAIT, 'x', ['x'])",
    "execution-os-startfile": "import os\ndef x(): os.startfile('x')",
    "filesystem-os-chmod": "import os\ndef x(): os.chmod('x', 0o600)",
    "filesystem-os-utime": "import os\ndef x(): os.utime('x')",
    "filesystem-os-truncate": "import os\ndef x(): os.truncate('x', 0)",
    "filesystem-os-chown": "import os\ndef x(): os.chown('x', 0, 0)",
    "filesystem-os-mknod": "import os\ndef x(): os.mknod('x')",
    "filesystem-path-hardlink": "from pathlib import Path\ndef x(): Path('a').hardlink_to('b')",
    "filesystem-path-symlink": "from pathlib import Path\ndef x(): Path('a').symlink_to('b')",
    "filesystem-path-replace": "from pathlib import Path\ndef x(): Path('a').replace('b')",
    "filesystem-symlink": "import os\ndef x(): os.symlink('a','b')",
    "filesystem-write-text": "from pathlib import Path\ndef x(): Path('x').write_text('bad')",
    "filesystem-write-bytes": "from pathlib import Path\ndef x(): Path('x').write_bytes(b'bad')",
    "filesystem-touch": "from pathlib import Path\ndef x(): Path('x').touch()",
    "builtin-open-write": "def x(): open('x', 'w').write('bad')",
    "builtin-open-append": "def x(): open('x', 'a').write('bad')",
    "builtin-open-create": "def x(): open('x', 'x').write('bad')",
    "builtin-open-update": "def x(): open('x', 'r+').write('bad')",
    "builtin-open-alias": "def x():\n    writer = open\n    writer('x', 'w')",
    "path-open-write": "from pathlib import Path\ndef x(): Path('x').open('w')",
    "builtin-open-starstar-write": "def x(): open('x', **{'mode': 'w'})",
    "path-open-starstar-write": "from pathlib import Path\ndef x(): Path('x').open(**{'mode': 'w'})",
    "io-open-write": "import io\ndef x(): io.open('x', 'w')",
    "io-fileio-write": "import io\ndef x(): io.FileIO('x', 'w')",
    "filehandle-writelines": "def x(handle): handle.writelines(['bad'])",
    "filehandle-truncate": "def x(handle): handle.truncate(0)",
    "json-dump-write": "import json\ndef x(handle): json.dump({}, handle)",
    "print-file-write": "def x(handle): print('bad', file=handle)",
    "tempfile-outside-atomic-writer": "import tempfile\ndef x(): tempfile.NamedTemporaryFile()",
    "tempfile-callable-alias": "import tempfile\ndef x():\n    maker = tempfile.NamedTemporaryFile\n    maker()",
    "git-wrapper-non-git-literal": "import subprocess\ndef run_git(root, *args): subprocess.run(['python', *args])",
    "git-wrapper-callable-alias": "def x(root):\n    runner = run_git\n    runner(root, 'status')",
    "git-run-process-callable-alias": "def x(root):\n    runner = run_process\n    runner(root, ['git', 'status'])",
    "git-run-process-tuple-alias": "def x(root):\n    runner, = (run_process,)\n    runner(root, ['git', 'status'])",
    "git-run-process-subscript-alias": "def x(root):\n    runner = [run_process][0]\n    runner(root, ['git', 'status'])",
    "git-run-process-inline-list": "def x(root): [run_process][0](root, ['git', 'status'])",
    "git-run-git-inline-list": "def x(root): [run_git][0](root, 'status')",
    "filesystem-path-write-inline-list": "from pathlib import Path\ndef x(): [Path('x').write_text][0]('bad')",
    "filesystem-open-inline-list": "def x(): [open][0]('x', 'w')",
    "tempfile-inline-list": "import tempfile\ndef x(): [tempfile.NamedTemporaryFile][0]()",
    "tempfile-temporary-directory": "import tempfile\ndef x(): tempfile.TemporaryDirectory()",
    "pil-image-save": "from PIL import Image\ndef x(): Image.new('RGB', (1, 1)).save('victim.png')",
    "json-from-import-dump": "from json import dump\ndef x(handle): dump({}, handle)",
    "pypdf-writer": "from pypdf import PdfWriter\ndef x(handle): PdfWriter().write_stream(handle)",
    "os-environ-write": "import os\ndef x(): os.environ['GIT_EXTERNAL_DIFF'] = 'bad'",
    "os-environ-update": "import os\ndef x(): os.environ.update({'GIT_DIR': 'C:/evil/.git'})",
    "os-environ-setdefault": "import os\ndef x(): os.environ.setdefault('GIT_DIR', 'C:/evil/.git')",
    "os-environ-ior": "import os\ndef x():\n    os.environ |= {'GIT_DIR': 'C:/evil/.git'}",
    "os-environ-delete": "import os\ndef x(): del os.environ['GIT_DIR']",
    "sys-path-insert": "import sys\ndef x(): sys.path.insert(0, 'C:/evil')",
    "sys-path-append": "import sys\ndef x(): sys.path.append('C:/evil')",
    "sys-modules-delete": "import sys\ndef x(): del sys.modules['build_phase065_step70']",
    "sys-meta-path-insert": "import sys\ndef x(hook): sys.meta_path.insert(0, hook)",
    "namespace-os-alias": "import os\ndef x():\n    other = os\n    other.execv('x', ['x'])",
    "namespace-json-alias": "import json\ndef x(handle):\n    other = json\n    other.dump({}, handle)",
    "builtin-print-alias": "def x(handle):\n    output = print\n    output('bad', file=handle)",
    "namespace-default-alias": "import os\ndef x(other=os.path): other.exists('x')",
    "builtins-namespace-exec": "def x(): __builtins__.exec('value = 1')",
    "builtins-namespace-open": "def x(): __builtins__.open('victim.txt', 'w')",
    "module-function-rebind": "def validate(): return True\nvalidate = lambda: False",
    "module-function-delete": "def validate(): return True\ndel validate",
    "module-function-class-rebind": "def validate(): return True\nclass validate: pass",
    "module-function-decorator-rebind": "@lambda function: (lambda: False)\ndef validate(): return True",
    "module-function-conditional-rebind": "if True:\n    def validate(): return False",
    "module-function-exception-rebind": "def validate(): return True\ntry:\n    raise RuntimeError()\nexcept RuntimeError as validate:\n    pass",
    "module-function-match-as-rebind": "def validate(): return True\nmatch (lambda: False):\n    case validate:\n        pass",
    "module-function-match-star-rebind": "def validate(): return True\nmatch [lambda: False]:\n    case [*validate]:\n        pass",
    "module-function-match-mapping-rebind": "def validate(): return True\nmatch {'x': 1}:\n    case {'x': _, **validate}:\n        pass",
    "transitive-subprocess-os-execv": "import subprocess\ndef x(): subprocess.os.execv('x', ['x'])",
    "transitive-subprocess-builtins-exec": "import subprocess\ndef x(): subprocess.sys.modules['builtins'].exec('value = 1')",
    "argparse-filetype-two-stage-write": "import argparse\ndef x():\n    factory = argparse.FileType('w')\n    factory('victim.txt')",
    "call-result-subprocess-alias": "import copy\nimport subprocess\ndef x():\n    runner = copy.deepcopy(subprocess.run)\n    runner(['x'])",
    "nested-call-result-subprocess-alias": "import subprocess\ndef x():\n    runner = next(iter([subprocess.run]))\n    runner(['x'])",
    "call-result-path-writer-alias": "import copy\nfrom pathlib import Path\ndef x():\n    writer = copy.deepcopy(Path.write_text)\n    writer(Path('victim.txt'), 'bad')",
    "function-global-rebind": "def validate(): return True\ndef mutate():\n    global validate\n    validate = lambda: False\nmutate()",
    "function-global-delete": "def validate(): return True\ndef mutate():\n    global validate\n    del validate\nmutate()",
    "function-global-import-rebind": "def Path(): return None\ndef mutate():\n    global Path\n    from pathlib import Path\nmutate()",
    "async-function-rebind": "def validate(): return True\nasync def validate(): return False",
    "validator-loader-missing": "def source_policy_errors(source): return []",
    "validator-loader-assignment": "def source_policy_errors(source): return []\nload_builder = lambda root: None",
    "validator-loader-class": "def source_policy_errors(source): return []\nclass load_builder: pass",
    "nested-writer-owner-spoof": "from pathlib import Path\ndef x():\n    def write_json_atomic():\n        temporary = Path('C:/victim')\n        temporary.unlink()\n    write_json_atomic()",
    "nested-git-owner-spoof": "import subprocess\ndef x(root):\n    def git_text(root):\n        def run_process(root, argv, binary=False):\n            return subprocess.run(argv, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n        def run_git(root, *args):\n            return run_process(root, ['git', 'clean', '-fdx'])\n        return run_git(root, 'status')\n    return git_text(root)",
    "run-git-process-argv-substitution": "def run_git(root, *args):\n    return run_process(root, ['git', 'clean', '-fdx'])",
    "run-git-process-binary-argv-substitution": "def run_git(root, *args, binary=False):\n    return run_process(root, ['git', 'clean', '-fdx'], binary=binary)",
    "path-open-class-callable-alias": "from pathlib import Path\ndef x():\n    writer = Path.open\n    writer(Path('victim.txt'), 'w')",
    "path-open-instance-callable-alias": "from pathlib import Path\ndef x():\n    writer = Path('victim.txt').open\n    writer('w')",
    "run-process-argv-reassignment": "import subprocess\ndef run_process(root, argv):\n    argv = ['git', 'clean', '-fdx']\n    return subprocess.run(argv, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)",
    "run-git-args-reassignment": "def run_git(root, *args):\n    args = ('clean', '-fdx')\n    return run_process(root, ['git', *args])",
    "load-builder-cache-reuse": "def load_builder(root):\n    path = root / BUILDER\n    if not path.is_file():\n        fail('E_BUILDER_MISSING', str(path))\n    module_dir = str(path.parent)\n    if module_dir not in sys.path:\n        sys.path.insert(0, module_dir)\n    import build_phase065_step70 as loaded_builder\n    return loaded_builder",
    "filesystem-writer-owner-unlink": "from pathlib import Path\ndef write_json_atomic(): Path('Claude/victim').unlink()",
    "git-reader-owner-clean": "def git_text(root): run_git(root, 'clean', '-fdx')",
    "git-reader-owner-reset": "def git_text(root): run_git(root, 'reset', '--hard')",
    "git-reader-owner-push": "def git_text(root): run_git(root, 'push', 'origin', 'main')",
    "git-reader-output-option": "def git_text(root): run_git(root, 'log', '--output=x')",
    "git-reader-work-tree-option": "def git_text(root): run_git(root, 'status', '--work-tree=/tmp')",
    "git-reader-textconv-option": "def git_text(root): run_git(root, 'show', '--textconv', 'HEAD')",
    "git-reader-branch-delete": "def verify_protection(root): run_git(root, 'branch', '-D', 'main')",
    "git-reader-show-ref-delete": "def verify_protection(root): run_git(root, 'show-ref', '--delete', 'refs/heads/main')",
    "git-reader-cat-file-filter": "def git_text(root): run_git(root, 'cat-file', '--filters', 'HEAD:x')",
    "git-reader-branch-move": "def verify_protection(root): run_git(root, 'branch', '-m', 'main')",
    "git-reader-upstream-change": "def verify_protection(root): run_git(root, 'branch', '--set-upstream-to=origin/main')",
    "git-reader-dynamic-branch-delete": "def verify_protection(root):\n    command='branch'\n    options=['-D','main']\n    run_git(root, command, *options)",
    "git-reader-dynamic-show-ref-delete": "def verify_protection(root):\n    command='show-ref'\n    options=['--delete','refs/heads/main']\n    run_git(root, command, *options)",
    "git-alias-execution": "def x(root): run_git(root, '-c', 'alias.pwn=!sh -c bad', 'pwn')",
    "git-protocol-override": "def x(root): run_git(root, '-c', 'protocol.file.allow=always', 'clone', 'file:///x')",
    "git-ext-protocol": "def x(root): run_git(root, 'clone', 'ext::sh -c bad')",
    "git-dynamic-config-option": "def x(root):\n    option = '-c'\n    run_git(root, option, 'alias.pwn=!sh -c bad', 'pwn')",
    "git-dynamic-options-starred": "def x(root):\n    options = ['-c', 'protocol.file.allow=always']\n    run_git(root, *options, 'clone', 'file:///x')",
    "git-dynamic-protocol-value": "def x(root):\n    value = 'ext::sh -c bad'\n    run_git(root, 'clone', value)",
}


def run_source_policy_negative_controls() -> int:
    accepted = [name for name, attack in SOURCE_POLICY_ATTACKS.items() if not source_policy_errors(attack)]
    if accepted:
        fail("E_SOURCE_POLICY_NEGATIVE", f"accepted={accepted}")
    return len(SOURCE_POLICY_ATTACKS)


def run_atomic_writer_contract_negative_controls(root: Path) -> int:
    source = (root / BUILDER).read_text(encoding="utf-8")
    guard = "    require(path.resolve() in allowed, \"E_WRITE_TARGET\", str(path))\n"
    require(guard in source, "E_ATOMIC_WRITER_GUARD_FIXTURE", "guard")
    no_guard = source.replace(guard, "", 1)
    victim_allowed = source.replace(
        "    allowed = {(ROOT / TOPOLOGY_PATH).resolve(), (ROOT / ATTESTATION_PATH).resolve()}\n",
        "    allowed = {Path('C:/victim.json').resolve()}\n",
        1,
    ).replace(
        "            write_json_atomic(output_dir / Path(TOPOLOGY_PATH).name, topology)\n",
        "            write_json_atomic(Path('C:/victim.json'), topology)\n",
        1,
    )
    writer_start = source.index("\ndef write_json_atomic")
    writer_stop = source.index("\ndef main", writer_start)
    no_writer = source[:writer_start] + source[writer_stop:]
    rebound_writer = source[:writer_stop] + "\nwrite_json_atomic = lambda path, value: None\n" + source[writer_stop:]
    attacks = {
        "removed-target-guard": no_guard,
        "substituted-target-and-callsite": victim_allowed,
        "removed-writer-definition": no_writer,
        "rebound-writer-definition": rebound_writer,
    }
    for name, attack in attacks.items():
        if source_policy_errors(attack, "builder"):
            continue
        fail("E_ATOMIC_WRITER_CONTRACT_NEGATIVE", name)
    return len(attacks)


def run_required_function_inventory_negative_controls(root: Path) -> int:
    cases = (
        (VALIDATOR, "verify_pre_evidence_git_state", "verify_pre_evidence_git_state = lambda root: None"),
        (VALIDATOR, "verify_in_progress_evidence_contract", "verify_in_progress_evidence_contract = lambda root: 0"),
        (VALIDATOR, "run_source_policy_negative_controls", "run_source_policy_negative_controls = lambda: 0"),
        (VALIDATOR, "verify_staged", "verify_staged = lambda root: None"),
        (VALIDATOR, "verify_persistence", "verify_persistence = lambda root, commit: None"),
        (BUILDER, "validate_evidence", "validate_evidence = lambda evidence, bindings: {}"),
    )
    for path, target_name, replacement in cases:
        source = (root / path).read_text(encoding="utf-8")
        tree = ast.parse(source)
        target = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == target_name
        )
        lines = source.splitlines()
        mutated = "\n".join([*lines[:target.lineno - 1], replacement, *lines[target.end_lineno:]]) + "\n"
        expected_kind = "builder" if path == BUILDER else "validator"
        if source_policy_errors(mutated, expected_kind):
            continue
        fail("E_REQUIRED_FUNCTION_INVENTORY_NEGATIVE", f"{path}:{target_name}")
    return len(cases)


def run_hardening_contract_probes(root: Path) -> int:
    validator_source = (root / VALIDATOR).read_text(encoding="utf-8")
    builder_source = (root / BUILDER).read_text(encoding="utf-8")
    validator_tree = ast.parse(validator_source)
    top_level_builder_import = any(
        isinstance(node, ast.Import)
        and any(alias.name == "build_phase065_step70" for alias in node.names)
        for node in validator_tree.body
    )
    top_level_functions = {node.name for node in validator_tree.body if isinstance(node, ast.FunctionDef)}
    top_level_assignments = {
        target.id
        for node in validator_tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    unmet: list[str] = []
    contracts = {
        "validator-defers-builder-import": not top_level_builder_import,
        "neutral-machine-status": "MACHINE_RECONSTRUCTED" in builder_source,
        "mandatory-evidence-groups": "MANDATORY_EVIDENCE_GROUPS" in builder_source,
        "exact-authority-ceiling": "AUTHORITY_CEILING" in builder_source,
        "canonical-process-partitions": "PROCESS_PARTITIONS" in builder_source,
        "full-commit-path-separation": '"full_commit_changed_paths"' in builder_source,
        "routed-path-separation": '"routed_changed_paths"' in builder_source,
        "historical-binary-metadata": "historical_binary" in builder_source,
        "frozen-phase057-source-ref": "PHASE057_SOURCE_REF" in builder_source and "source_ref" in builder_source,
        "phase057-independent-ref-check": "verify_phase057_frozen_sources" in validator_source,
        "unique-run-process-boundary": "def run_process" in builder_source and "def run_process" in validator_source,
        "frozen-process-query-argv": "process_query_argv" in builder_source,
        "kind-specific-read-status": "ALLOWED_STATUS_BY_KIND" in builder_source,
        "semantic-deferred-intervals": "semantic_deferred_intervals" in builder_source,
        "reviewed-process-record-binding": "reviewed_process_records" in builder_source,
        "cross-projection-classification": "reconcile_process_classifications" in builder_source,
        "finding-route-schema": "FINDING_ROUTE_SCHEMA" in builder_source,
        "exact-current-state": "verify_pre_evidence_git_state" in validator_source,
        "immutable-process-binding-schema": "machine-process-projection-v1" in builder_source and "process_binding_records" in builder_source,
        "finding-artifact-global-contract": "finding_rows_errors" in top_level_functions and "EXPECTED_FINDING_IDS" in top_level_assignments,
    }
    unmet.extend(name for name, passed in contracts.items() if not passed)
    accepted = [name for name, attack in SOURCE_POLICY_ATTACKS.items() if not source_policy_errors(attack)]
    if accepted or unmet:
        fail("E_HARDENING_SELFTEST", f"accepted_source_policy={accepted}; unmet_contracts={unmet}")
    return len(SOURCE_POLICY_ATTACKS) + len(contracts)


def run_evidence_contract_negative_controls(builder: Any) -> int:
    bindings = {
        group_id: {
            "group_id": group_id,
            "kind": (
                "FULL_PDF_EXTRACT_RENDER_VISUAL" if group_id == "release_pdf"
                else "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL" if group_id in {"release_image", "comp_v24_png"}
                else "FULL_PATCH" if group_id.startswith("release_process_") or group_id.startswith("routed_process_")
                else "FULL_TEXT"
            ),
            "record_count": 1,
            "record_manifest_sha256": sha256_bytes(group_id.encode("utf-8")),
            "summary": {"records": 1},
            "binding_sha256": sha256_bytes(f"binding:{group_id}".encode("utf-8")),
        }
        for group_id in MANDATORY_EVIDENCE_GROUPS
    }

    def assignment(group_id: str) -> dict[str, Any]:
        binding = bindings[group_id]
        return {
            "group_id": group_id,
            "record_count": binding["record_count"],
            "record_manifest_sha256": binding["record_manifest_sha256"],
            "binding_sha256": binding["binding_sha256"],
            "status": "AGENT_FULL_READ",
        }

    groups = list(MANDATORY_EVIDENCE_GROUPS)
    synthetic_interval = {
        "interval_id": "release-code-guide-html-mermaid-lines-220-3807",
        "group_id": "release_scientific_document_text",
        "subject_type": "GIT_BLOB_TEXT_INTERVAL",
        "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
        "source_ref": BASELINE,
        "path": "Claude/docs/v1.0.24/CODE_GUIDE_v24.html",
        "blob": "2" * 40,
        "full_bytes": 4000,
        "full_lines": 4000,
        "full_sha256_raw": "3" * 64,
        "full_sha256_lf": "4" * 64,
        "line_range": [220, 3807],
        "interval_bytes_lf": 3588,
        "interval_lines": 3588,
        "interval_sha256_lf": "5" * 64,
    }
    bindings["release_scientific_document_text"]["summary"]["semantic_deferred_intervals"] = [synthetic_interval]
    evidence: dict[str, Any] = {
        "schema_version": "P065-S70-HUMAN-EVIDENCE-1",
        "baseline_commit": BASELINE,
        "bindings": bindings,
        "readers": [
            {"reader_id": "contract-reader-a", "assignments": [assignment(group) for group in groups[:5]], "unreviewed_intervals": [], "output_truncation_unresolved": []},
            {"reader_id": "contract-reader-b", "assignments": [assignment(group) for group in groups[5:10]], "unreviewed_intervals": [], "output_truncation_unresolved": []},
            {"reader_id": "contract-reader-c", "assignments": [assignment(group) for group in groups[10:]], "unreviewed_intervals": [], "output_truncation_unresolved": []},
        ],
        "unreviewed_intervals": [],
        "output_truncation_unresolved": [],
        "authority": AUTHORITY_CEILING,
        "pdf_visual": {"pages_extracted": 148, "pages_rendered": 148, "pages_visual": 148},
        "image_visual": {"original_resolution_visual": 3},
        "process_patch_read": {"release": 38, "routed": 98},
        "narrative_correction_acknowledged": {"copied_lines": 2068, "reconstructed_lines": 2306, "delta": 238},
        "semantic_deferred_intervals": [synthetic_interval],
        "finding_routes": [{
            "id": f"P065-S70-F{index:02d}",
            "severity": "P1" if index <= 22 else "P2",
            "status": "OPEN_ROUTED",
            "summary": f"synthetic finding {index}",
            "owner": "Step 70 controller",
            "target_steps": ["Step 71"],
            "authority_promoted": False,
        } for index in range(6, 45)],
    }
    for index, reader in enumerate(evidence["readers"]):
        reader["report_path"] = RESULT
        reader["report_section"] = "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON"
        reader["finding_ids"] = list(EXPECTED_ROUTED_FINDING_IDS) if index == 0 else []
        reader["report_binding_sha256"] = sha256_bytes(canonical_bytes({
            key: value for key, value in reader.items() if key != "report_binding_sha256"
        }))
    builder.validate_evidence(copy.deepcopy(evidence), bindings)

    attacks: dict[str, Any] = {}
    missing = copy.deepcopy(evidence)
    missing["readers"][2]["assignments"].pop()
    attacks["missing-group"] = missing
    duplicate = copy.deepcopy(evidence)
    duplicate["readers"][1]["assignments"].append(copy.deepcopy(duplicate["readers"][0]["assignments"][0]))
    attacks["duplicate-group"] = duplicate
    extra = copy.deepcopy(evidence)
    extra["readers"][0]["assignments"][0]["group_id"] = "extra-group"
    attacks["extra-group"] = extra
    wrong_binding = copy.deepcopy(evidence)
    wrong_binding["readers"][0]["assignments"][0]["binding_sha256"] = "0" * 64
    attacks["binding-mismatch"] = wrong_binding
    incomplete_authority = copy.deepcopy(evidence)
    incomplete_authority["authority"].pop("external_material")
    attacks["authority-incomplete"] = incomplete_authority
    promoted_authority = copy.deepcopy(evidence)
    promoted_authority["authority"]["external_scientific"] = True
    attacks["authority-promoted"] = promoted_authority
    unread = copy.deepcopy(evidence)
    unread["unreviewed_intervals"] = ["synthetic-gap"]
    attacks["unreviewed-interval"] = unread
    duplicate_reader = copy.deepcopy(evidence)
    duplicate_reader["readers"][1]["reader_id"] = duplicate_reader["readers"][0]["reader_id"]
    attacks["duplicate-reader"] = duplicate_reader
    text_structural = copy.deepcopy(evidence)
    text_structural["readers"][0]["assignments"][0]["status"] = "FULL_BYTE_STRUCTURAL"
    attacks["text-group-fake-structural"] = text_structural
    pdf_structural = copy.deepcopy(evidence)
    pdf_assignment = next(
        assignment
        for reader in pdf_structural["readers"]
        for assignment in reader["assignments"]
        if assignment["group_id"] == "release_pdf"
    )
    pdf_assignment["status"] = "FULL_BYTE_STRUCTURAL"
    attacks["pdf-group-fake-structural"] = pdf_structural
    image_direct = copy.deepcopy(evidence)
    image_assignment = next(
        assignment
        for reader in image_direct["readers"]
        for assignment in reader["assignments"]
        if assignment["group_id"] == "release_image"
    )
    image_assignment["status"] = "DIRECT_READ"
    attacks["image-group-nonvisual-status"] = image_direct
    unexpected_deferred = copy.deepcopy(evidence)
    unexpected_deferred["semantic_deferred_intervals"] = [{"interval_id": "invented"}]
    attacks["semantic-deferred-extra"] = unexpected_deferred
    missing_deferred = copy.deepcopy(evidence)
    missing_deferred["semantic_deferred_intervals"] = []
    attacks["semantic-deferred-missing-known"] = missing_deferred
    wrong_deferred_hash = copy.deepcopy(evidence)
    wrong_deferred_hash["semantic_deferred_intervals"][0]["interval_sha256_lf"] = "0" * 64
    attacks["semantic-deferred-wrong-hash"] = wrong_deferred_hash
    id_only = copy.deepcopy(evidence)
    id_only["finding_routes"][0] = {"id": "P065-S70-F06"}
    attacks["finding-id-only"] = id_only
    reserved = copy.deepcopy(evidence)
    reserved["finding_routes"][0]["id"] = "P065-S70-F05"
    attacks["finding-reserved-id"] = reserved
    authority_route = copy.deepcopy(evidence)
    authority_route["finding_routes"][0]["authority_promoted"] = True
    attacks["finding-authority-promotion"] = authority_route
    collision = copy.deepcopy(evidence)
    collision["finding_routes"][1]["id"] = collision["finding_routes"][0]["id"]
    attacks["finding-id-collision"] = collision
    missing_high = copy.deepcopy(evidence)
    missing_high["finding_routes"] = [row for row in missing_high["finding_routes"] if row["id"] != "P065-S70-F44"]
    attacks["finding-high-id-missing"] = missing_high
    missing_reader_report = copy.deepcopy(evidence)
    missing_reader_report["readers"][0].pop("report_binding_sha256")
    attacks["reader-report-binding-missing"] = missing_reader_report
    wrong_reader_report = copy.deepcopy(evidence)
    wrong_reader_report["readers"][0]["report_binding_sha256"] = "0" * 64
    attacks["reader-report-binding-wrong"] = wrong_reader_report
    wrong_reader_path = copy.deepcopy(evidence)
    wrong_reader_path["readers"][0]["report_path"] = "Codex/results/UNBOUND_REPORT.md"
    wrong_reader_path["readers"][0]["report_binding_sha256"] = sha256_bytes(canonical_bytes({
        key: value for key, value in wrong_reader_path["readers"][0].items() if key != "report_binding_sha256"
    }))
    attacks["reader-report-path-wrong"] = wrong_reader_path
    unknown_reader_finding = copy.deepcopy(evidence)
    unknown_reader_finding["readers"][0]["finding_ids"].append("P065-S70-F45")
    unknown_reader_finding["readers"][0]["report_binding_sha256"] = sha256_bytes(canonical_bytes({
        key: value for key, value in unknown_reader_finding["readers"][0].items() if key != "report_binding_sha256"
    }))
    attacks["reader-report-finding-unknown"] = unknown_reader_finding

    for name, attack in attacks.items():
        try:
            builder.validate_evidence(attack, bindings)
        except builder.BuildFailure:
            continue
        fail("E_EVIDENCE_CONTRACT_NEGATIVE", name)
    require(reader_report_errors(evidence["readers"]) == [], "E_READER_REPORT_ARTIFACT_FIXTURE", repr(reader_report_errors(evidence["readers"])))
    reader_attacks = {
        "binding-missing": missing_reader_report["readers"],
        "binding-wrong": wrong_reader_report["readers"],
        "path-wrong": wrong_reader_path["readers"],
        "finding-unknown": unknown_reader_finding["readers"],
    }
    for name, attack in reader_attacks.items():
        if reader_report_errors(attack):
            continue
        fail("E_READER_REPORT_ARTIFACT_NEGATIVE", name)
    return len(attacks) + len(reader_attacks)


def run_finding_artifact_negative_controls() -> int:
    valid = [
        {"id": finding_id, "status": "CONFIRMED", "finding": "synthetic base finding"}
        for finding_id in EXPECTED_BASE_FINDING_IDS
    ] + [
        {
            "id": finding_id,
            "severity": "P1",
            "status": "OPEN_ROUTED",
            "summary": "synthetic routed finding",
            "owner": "synthetic owner",
            "target_steps": ["Step 71"],
            "authority_promoted": False,
        }
        for finding_id in EXPECTED_ROUTED_FINDING_IDS
    ]
    require(finding_rows_errors(valid) == [], "E_FINDING_ARTIFACT_FIXTURE", repr(finding_rows_errors(valid)))
    attacks: dict[str, list[dict[str, Any]]] = {}
    attacks["missing-high-id"] = copy.deepcopy(valid[:-1])
    duplicate = copy.deepcopy(valid)
    duplicate[-1]["id"] = duplicate[-2]["id"]
    attacks["duplicate-high-id"] = duplicate
    extra = copy.deepcopy(valid)
    extra.append({"id": "P065-S70-F45", "status": "CONFIRMED", "finding": "extra"})
    attacks["extra-id"] = extra
    wrong_schema = copy.deepcopy(valid)
    wrong_schema[-1].pop("owner")
    attacks["routed-schema-missing"] = wrong_schema
    promoted = copy.deepcopy(valid)
    promoted[-1]["authority_promoted"] = True
    attacks["routed-authority-promoted"] = promoted
    for name, attack in attacks.items():
        if finding_rows_errors(attack):
            continue
        fail("E_FINDING_ARTIFACT_NEGATIVE", name)
    return len(attacks)


def run_process_projection_negative_controls(builder: Any) -> int:
    canonical = {
        "commit": "a" * 40,
        "state_class": "review",
        "classification_basis": "CANONICAL_ROUTED_ORDINAL_WITH_SUBJECT_PATHS_BINARY_PATCH_CONTEXT",
        "classification_notes": "internal review only",
    }
    release = {"commits": [copy.deepcopy(canonical)]}
    routed = {"commits": [copy.deepcopy(canonical)]}
    builder.require_process_projection_consistency(release, routed)
    attacks = {
        "process-state-class-drift": ("state_class", "patch"),
        "process-classification-basis-drift": ("classification_basis", "patch-only"),
        "process-classification-notes-drift": ("classification_notes", "unsupported authority"),
    }
    for name, (field, value) in attacks.items():
        mutated = copy.deepcopy(release)
        mutated["commits"][0][field] = value
        try:
            builder.require_process_projection_consistency(mutated, routed)
        except builder.BuildFailure:
            continue
        fail("E_PROCESS_PROJECTION_NEGATIVE", name)
    return len(attacks)


def markdown_table_row(text: str, first_cell: str) -> list[str]:
    matches = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] == first_cell:
            matches.append(cells)
    require(len(matches) == 1, "E_CONTROL_ROW", f"{first_cell}: {len(matches)}")
    return matches[0]


def verify_in_progress_controls(root: Path) -> None:
    result_lines = (root / RESULT).read_text(encoding="utf-8").splitlines()
    require(result_lines[3] == "Status: `IN_PROGRESS_RESULT_FIRST`", "E_RESULT_IN_PROGRESS_STATUS", result_lines[3])
    require("Current Step 70 gate: `IN_PROGRESS_RESULT_FIRST`." in result_lines, "E_RESULT_IN_PROGRESS_GATE", RESULT)
    require(not (root / TOPOLOGY).exists() and not (root / ATTESTATION).exists(), "E_JSON_LAST_PREMATURE_ARTIFACT", "Step 70 JSON exists")

    parent = markdown_table_row((root / PARENT_LEDGER).read_text(encoding="utf-8"), "065")
    require(len(parent) == 12, "E_PARENT_LEDGER_SCHEMA", repr(parent))
    require(parent[2] == "detailed-plan activation persisted; Step 70 result-first evidence collection and validator hardening in progress; Steps 71–75 pending", "E_PARENT_LEDGER_ACTUAL", parent[2])
    require(parent[5] == "IN_PROGRESS", "E_PARENT_LEDGER_STATUS", parent[5])
    require(parent[10] == "`IN_PROGRESS_RESULT_FIRST`; evidence pending", "E_PARENT_LEDGER_GATE", parent[10])
    require(parent[11] == "finish complete-read/visual evidence, then JSON-last collection and dual-runtime validation", "E_PARENT_LEDGER_NEXT", parent[11])

    canonical = markdown_table_row((root / CANONICAL_LEDGER).read_text(encoding="utf-8"), "065")
    require(len(canonical) == 11, "E_CANONICAL_LEDGER_SCHEMA", repr(canonical))
    require(canonical[2] == "detailed-plan activation persisted; Step 70 result-first evidence collection and validator hardening in progress; Steps 71–75 pending", "E_CANONICAL_LEDGER_ACTUAL", canonical[2])
    require(canonical[4] == "IN_PROGRESS", "E_CANONICAL_LEDGER_STATUS", canonical[4])
    require(canonical[9] == "`IN_PROGRESS_RESULT_FIRST`; no Step 70 PASS selected", "E_CANONICAL_LEDGER_GATE", canonical[9])
    require(canonical[10] == "finish complete-read/visual evidence, collect JSONs last, then dual-runtime staged validation", "E_CANONICAL_LEDGER_NEXT", canonical[10])

    handover_lines = (root / HANDOVER).read_text(encoding="utf-8").splitlines()
    require("17. 현재 Phase 상태: Phase 065 `IN_PROGRESS`, Current checkpoint: Step 70 `IN_PROGRESS_RESULT_FIRST`" in handover_lines, "E_HANDOVER_CURRENT", HANDOVER)
    handover_row = markdown_table_row("\n".join(handover_lines), "Phase 065 Step 70")
    require(len(handover_row) == 4, "E_HANDOVER_ROW_SCHEMA", repr(handover_row))
    require(handover_row[3] == "integrate complete-read/visual evidence, collect JSONs last, validate and persist before Step 71", "E_HANDOVER_NEXT", handover_row[3])


def verify_in_progress_evidence_contract(root: Path) -> int:
    text = (root / RESULT).read_text(encoding="utf-8")
    begin = "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON"
    end = "END_P065_STEP70_HUMAN_EVIDENCE_JSON"
    lines = text.splitlines()
    begin_rows = [index for index, line in enumerate(lines) if line == begin]
    end_rows = [index for index, line in enumerate(lines) if line == end]
    require(len(begin_rows) == 1 and len(end_rows) == 1 and begin_rows[0] < end_rows[0], "E_IN_PROGRESS_EVIDENCE_MARKERS", RESULT)
    payload = "\n".join(lines[begin_rows[0] + 1:end_rows[0]]).strip()
    require(payload.startswith("```json") and payload.endswith("```"), "E_IN_PROGRESS_EVIDENCE_FENCE", RESULT)
    evidence = strict_loads(payload[len("```json"): -len("```")].strip().encode("utf-8"))
    require(isinstance(evidence, dict), "E_IN_PROGRESS_EVIDENCE_OBJECT", RESULT)
    require(evidence.get("schema_version") == "P065-S70-HUMAN-EVIDENCE-1", "E_IN_PROGRESS_EVIDENCE_SCHEMA", RESULT)
    require(evidence.get("baseline_commit") == BASELINE, "E_IN_PROGRESS_EVIDENCE_BASELINE", RESULT)
    bindings = evidence.get("bindings")
    require(isinstance(bindings, dict) and set(bindings) == set(MANDATORY_EVIDENCE_GROUPS), "E_IN_PROGRESS_EVIDENCE_BINDINGS", RESULT)
    report_errors = reader_report_errors(evidence.get("readers"))
    require(report_errors == [], "E_IN_PROGRESS_READER_REPORTS", "; ".join(report_errors))
    routed_findings = evidence.get("finding_routes")
    require(isinstance(routed_findings, list), "E_IN_PROGRESS_FINDING_LIST", RESULT)
    require([row.get("id") if isinstance(row, dict) else None for row in routed_findings] == list(EXPECTED_ROUTED_FINDING_IDS), "E_IN_PROGRESS_FINDING_COVERAGE", RESULT)
    require(all(isinstance(row, dict) and set(row) == ROUTED_FINDING_SCHEMA and row.get("authority_promoted") is False for row in routed_findings), "E_IN_PROGRESS_FINDING_SCHEMA", RESULT)
    assignments = [assignment for reader in evidence["readers"] for assignment in reader["assignments"]]
    require(len(assignments) == len(MANDATORY_EVIDENCE_GROUPS) and {row.get("group_id") for row in assignments} == set(MANDATORY_EVIDENCE_GROUPS), "E_IN_PROGRESS_ASSIGNMENT_COVERAGE", RESULT)
    require(evidence.get("unreviewed_intervals") == [] and evidence.get("output_truncation_unresolved") == [], "E_IN_PROGRESS_EVIDENCE_GAPS", RESULT)
    return len(evidence["readers"]) + 7


def run_strict_json_negative_controls() -> int:
    attacks = [
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":9223372036854775808}',
        b'{"a":1',
        b'\xff',
    ]
    for index, attack in enumerate(attacks, 1):
        try:
            strict_loads(attack)
        except ValidationFailure:
            continue
        fail("E_STRICT_JSON_NEGATIVE", f"attack {index} accepted")
    return len(attacks)


def run_semantic_negative_controls(topology: dict[str, Any], attestation: dict[str, Any]) -> int:
    mutations: list[tuple[str, str, Any]] = [
        ("top", "manifest.occurrences", 260),
        ("top", "manifest.unique_blobs", 130),
        ("top", "manifest.unique_text_lines", 21617),
        ("top", "manifest.unique_pdf_pages", 147),
        ("top", "manifest.path_set_sha256", "0" * 64),
        ("top", "mirror.byte_identical_pairs", 129),
        ("top", "narrative.corrected_root_process.lines", 2068),
        ("top", "narrative.corrected_total.lines", 7232),
        ("top", "process.release.count", 37),
        ("top", "process.routed.count", 97),
        ("top", "process.routed.canonical_patch_row_binding_sha256", "0" * 64),
        ("top", "tex.adopted_union.lines", 8217),
        ("top", "authority.external_material", True),
        ("att", "coverage.text.lines", 21617),
        ("att", "coverage.pdf.pages_visual", 147),
        ("att", "coverage.image.original_resolution_visual", 2),
        ("att", "coverage.supplemental.lines", 727),
        ("att", "coverage.narrative.lines", 7232),
        ("att", "coverage.comp_v24.csv.lines", 45202),
        ("att", "coverage.routed_commits.complete_patches", 97),
        ("att", "coverage.routed_partitions.routed_process_ordinals_067_098.patch_bytes", 9394732),
        ("att", "unreviewed_intervals", ["x"]),
        ("att", "authority.external_scientific", True),
        ("att", "authority.publication_ready", True),
        ("att", "gate", "PASS_P065_STEP70_PERSISTENCE"),
    ]

    def assign(obj: dict[str, Any], dotted: str, value: Any) -> None:
        parts = dotted.split(".")
        cur: Any = obj
        for part in parts[:-1]:
            cur = cur[part]
        cur[parts[-1]] = value

    for label, dotted, value in mutations:
        top_copy = copy.deepcopy(topology)
        att_copy = copy.deepcopy(attestation)
        target = top_copy if label == "top" else att_copy
        assign(target, dotted, value)
        target["semantic_sha256"] = semantic_hash(target)
        if not artifact_errors(top_copy, att_copy):
            fail("E_SEMANTIC_NEGATIVE", dotted)
    return len(mutations)


def run_process(root: Path, argv: list[str], binary: bool = False) -> subprocess.CompletedProcess[Any]:
    require(bool(argv) and argv[0] == "git", "E_PROCESS_NOT_GIT", repr(argv))
    return subprocess.run(
        argv,
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "strict",
    )


def run_git(root: Path, *args: str, check: bool = True, binary: bool = False) -> Any:
    require(bool(args) and all(isinstance(arg, str) for arg in args), "E_GIT_ARGV", repr(args))
    require(not args[0].startswith("-"), "E_GIT_SUBCOMMAND", args[0])
    require(args[0] in READ_ONLY_GIT_SUBCOMMANDS, "E_GIT_NOT_READ_ONLY", args[0])
    require(git_read_only_shape(tuple(args)), "E_GIT_ARGV_SHAPE", repr(args))
    dangerous = ("-c", "--config-env", "--upload-pack", "--receive-pack", "--exec-path", "--ext-diff", "--textconv")
    dangerous_prefixes = ("--config=", "--config-env=", "--upload-pack=", "--receive-pack=", "--exec-path=")
    require(not any(arg in dangerous or arg.startswith(dangerous_prefixes) or arg.startswith("alias.") or arg.startswith("protocol.") for arg in args), "E_GIT_OPTION", repr(args))
    require(not any(arg == "-o" or arg.startswith(("--output", "--config=", "--git-dir", "--work-tree")) for arg in args), "E_GIT_WRITE_OPTION", repr(args))
    require(not any(arg.startswith("ext::") or arg.startswith("file://") for arg in args), "E_GIT_PROTOCOL", repr(args))
    proc = run_process(root, ["git", *args], binary=binary)
    if check and proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", "replace") if binary else proc.stderr
        fail("E_GIT", f"git {' '.join(args)}: {stderr.strip()}")
    return proc.stdout


def parse_name_status(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for raw in text.splitlines():
        if not raw:
            continue
        parts = raw.split("\t")
        status = parts[0]
        if status.startswith("R") or status.startswith("C") or len(parts) != 2:
            fail("E_RENAME_OR_STATUS", raw)
        if parts[1] in rows:
            fail("E_DUPLICATE_PATH_STATUS", parts[1])
        rows[parts[1]] = status
    return rows


def frozen_source_record_errors(record: dict[str, Any], path: str, source_ref: str, blob: str, raw: bytes) -> list[str]:
    lf = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    lines = len(lf.decode("utf-8").splitlines())
    expected = {
        "path": path,
        "source": "git_blob",
        "source_ref": source_ref,
        "blob": blob,
        "lines": lines,
        "bytes": len(raw),
        "sha256_raw": sha256_bytes(raw),
        "sha256_lf": sha256_bytes(lf),
        "machine_extent_ranges": [[1, lines]] if lines else [],
    }
    return [field for field, value in expected.items() if record.get(field) != value]


def verify_phase057_frozen_sources(root: Path, topology: dict[str, Any]) -> None:
    narrative_rows = {
        row["path"]: row
        for row in topology.get("narrative", {}).get("records", [])
        if row.get("partition") == "phase057_routing"
    }
    source_rows = {
        row["path"]: row
        for row in topology.get("phase057_observations", {}).get("source_documents", [])
    }
    require(set(narrative_rows) == set(PHASE057_PATHS), "E_PHASE057_NARRATIVE_PATHS", repr(sorted(narrative_rows)))
    require(set(source_rows) == set(PHASE057_PATHS), "E_PHASE057_OBSERVATION_SOURCE_PATHS", repr(sorted(source_rows)))
    blob_by_path: dict[str, str] = {}
    for path in PHASE057_PATHS:
        raw = run_git(root, "cat-file", "blob", f"{EXPECTED_PARENT}:{path}", binary=True)
        blob = run_git(root, "rev-parse", f"{EXPECTED_PARENT}:{path}").strip()
        blob_by_path[path] = blob
        for label, record in (("narrative", narrative_rows[path]), ("observation", source_rows[path])):
            errors = frozen_source_record_errors(record, path, EXPECTED_PARENT, blob, raw)
            require(not errors, "E_PHASE057_FROZEN_RECORD", f"{label}:{path}:{errors}")
    for row in topology.get("phase057_observations", {}).get("records", []):
        path = row.get("source_path")
        require(path in blob_by_path, "E_PHASE057_OBSERVATION_PATH", str(path))
        require(row.get("source_ref") == EXPECTED_PARENT, "E_PHASE057_OBSERVATION_REF", str(path))
        require(row.get("source_blob") == blob_by_path[path], "E_PHASE057_OBSERVATION_BLOB", str(path))


def verified_lf_interval(raw: bytes, first: int, last: int) -> tuple[bytes, int]:
    lf = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    lines = lf.splitlines(keepends=True)
    require(1 <= first <= last <= len(lines), "E_SEMANTIC_INTERVAL_RANGE", f"{first}-{last}/{len(lines)}")
    return b"".join(lines[first - 1:last]), len(lines)


def verify_semantic_deferred_sources(root: Path, topology: dict[str, Any], attestation: dict[str, Any]) -> None:
    actual = attestation.get("semantic_deferred_intervals")
    require(isinstance(actual, list), "E_SEMANTIC_INTERVALS", repr(actual))
    html_path = "Claude/docs/v1.0.24/CODE_GUIDE_v24.html"
    html_raw = run_git(root, "cat-file", "blob", f"{BASELINE}:{html_path}", binary=True)
    html_slice, html_lines = verified_lf_interval(html_raw, 220, 3807)
    expected = [{
        "interval_id": "release-code-guide-html-mermaid-lines-220-3807",
        "group_id": "release_scientific_document_text",
        "subject_type": "GIT_BLOB_TEXT_INTERVAL",
        "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
        "source_ref": BASELINE,
        "path": html_path,
        "blob": run_git(root, "rev-parse", f"{BASELINE}:{html_path}").strip(),
        "full_bytes": len(html_raw),
        "full_lines": html_lines,
        "full_sha256_raw": sha256_bytes(html_raw),
        "full_sha256_lf": sha256_bytes(html_raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")),
        "line_range": [220, 3807],
        "interval_bytes_lf": len(html_slice),
        "interval_lines": 3588,
        "interval_sha256_lf": sha256_bytes(html_slice),
    }]
    routed = {row.get("ordinal"): row for row in topology.get("process", {}).get("routed", {}).get("commits", [])}
    for ordinal, (first, last) in EXPECTED_SEMANTIC_DEFERRED_PATCH_INTERVALS.items():
        row = routed.get(ordinal)
        require(isinstance(row, dict), "E_SEMANTIC_PROCESS_ORDINAL", str(ordinal))
        patch = run_git(
            root, "show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv",
            "--find-renames", "--find-copies", row["commit"], "--", *ROUTED_PATHS, binary=True,
        )
        interval, patch_lines = verified_lf_interval(patch, first, last)
        expected.append({
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
    require(actual == sorted(expected, key=lambda row: row["interval_id"]), "E_SEMANTIC_INTERVAL_BINDING", "exact known intervals")


def run_semantic_boundary_contract(root: Path, builder: Any) -> int:
    require(
        builder.SEMANTIC_DEFERRED_PATCH_INTERVALS == EXPECTED_SEMANTIC_DEFERRED_PATCH_INTERVALS,
        "E_SEMANTIC_BOUNDARY_CONSTANT",
        repr(builder.SEMANTIC_DEFERRED_PATCH_INTERVALS),
    )
    commits = {
        70: "1ee23c53fec14c41a1f5372a19e6b2f70adb0de0",
        98: "2147abfac3fb6c82279aefb2b21c749a521112dc",
    }
    expected_interval_sha256 = "ad876d11d7f34252c672254b1fe4f8549b5fe1d3f28e8a37268798abe13286d5"
    for ordinal, (first, last) in EXPECTED_SEMANTIC_DEFERRED_PATCH_INTERVALS.items():
        patch = run_git(
            root, "show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv",
            "--find-renames", "--find-copies", commits[ordinal], "--", *ROUTED_PATHS, binary=True,
        )
        lines = patch.replace(b"\r\n", b"\n").replace(b"\r", b"\n").splitlines(keepends=True)
        interval = b"".join(lines[first - 1:last])
        require(lines[first - 1].startswith(b'+<script>"use strict";'), "E_SEMANTIC_BOUNDARY_START", str(ordinal))
        require(lines[last - 1].rstrip(b"\n") == b"+</script>", "E_SEMANTIC_BOUNDARY_END", str(ordinal))
        require(lines[last].rstrip(b"\n") == b"+<script>", "E_SEMANTIC_BOUNDARY_FOOTER", str(ordinal))
        require(sha256_bytes(interval) == expected_interval_sha256, "E_SEMANTIC_BOUNDARY_HASH", str(ordinal))
    return len(commits)


def run_phase057_frozen_source_negative_controls() -> int:
    path = PHASE057_PATHS[0]
    source_ref = EXPECTED_PARENT
    raw = b"alpha\nbeta\n"
    blob = "1" * 40
    record = {
        "path": path,
        "source": "git_blob",
        "source_ref": source_ref,
        "blob": blob,
        "lines": 2,
        "bytes": len(raw),
        "sha256_raw": sha256_bytes(raw),
        "sha256_lf": sha256_bytes(raw),
        "read_status": "MACHINE_RECONSTRUCTED",
        "read_ranges": [],
        "machine_extent_ranges": [[1, 2]],
    }
    attacks = {
        "phase057-crlf-checkout-substitution": b"alpha\r\nbeta\r\n",
        "phase057-content-mutation": b"alpha\ngamma\n",
    }
    for name, attack_raw in attacks.items():
        if not frozen_source_record_errors(record, path, source_ref, blob, attack_raw):
            fail("E_PHASE057_FROZEN_NEGATIVE", name)
    wrong_ref = copy.deepcopy(record)
    wrong_ref["source_ref"] = BASELINE
    if not frozen_source_record_errors(wrong_ref, path, source_ref, blob, raw):
        fail("E_PHASE057_FROZEN_NEGATIVE", "phase057-source-ref-mutation")
    return 3


def parse_porcelain(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4, "E_PORCELAIN_ROW", line)
        status, path = line[:2], line[3:]
        require(" -> " not in path and path not in rows, "E_PORCELAIN_PATH", path)
        rows[path] = status
    return rows


def live_remote_tip(root: Path, branch: str) -> str:
    output = run_git(root, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    rows = [line.split()[0] for line in output.splitlines() if line.strip()]
    require(len(rows) == 1, "E_LIVE_REMOTE", f"{branch}: {rows}")
    return rows[0]


def canonical_origin_identity(value: str) -> str:
    candidate = value.strip().rstrip("/")
    lowered = candidate.lower()
    if lowered.startswith("https://github.com/"):
        tail = candidate[len("https://github.com/"):]
    elif lowered.startswith("git@github.com:"):
        tail = candidate[len("git@github.com:"):]
    else:
        return ""
    if tail.lower().endswith(".git"):
        tail = tail[:-4]
    return f"github.com/{tail}".lower()


def require_repository_identity(upstream: str, origin_url: str) -> None:
    require(upstream == EXPECTED_UPSTREAM, "E_UPSTREAM_IDENTITY", upstream)
    require(canonical_origin_identity(origin_url) == EXPECTED_ORIGIN_IDENTITY, "E_ORIGIN_IDENTITY", origin_url)


def run_repository_identity_negative_controls() -> int:
    require_repository_identity(EXPECTED_UPSTREAM, "https://github.com/lksz1412/Project_Anode_Fit.git")
    attacks = (
        ("origin/main", "https://github.com/lksz1412/Project_Anode_Fit.git"),
        (BRANCH, "https://github.com/lksz1412/Project_Anode_Fit.git"),
        (EXPECTED_UPSTREAM, "https://github.com/lksz1412/Other.git"),
        (EXPECTED_UPSTREAM, "file:///tmp/Project_Anode_Fit.git"),
        (EXPECTED_UPSTREAM, "https://github.com/other/Project_Anode_Fit.git"),
    )
    for upstream, origin_url in attacks:
        try:
            require_repository_identity(upstream, origin_url)
        except ValidationFailure:
            continue
        fail("E_REPOSITORY_IDENTITY_NEGATIVE", f"{upstream}|{origin_url}")
    return len(attacks)


def verify_protection(root: Path) -> None:
    upstream = run_git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}").strip()
    origin_url = run_git(root, "ls-remote", "--get-url", "origin").strip()
    require_repository_identity(upstream, origin_url)
    require(run_git(root, "rev-parse", f"refs/heads/{PROTECTED_BRANCH}").strip() == PROTECTED_TIP, "E_PROTECTED_LOCAL", PROTECTED_BRANCH)
    require(run_git(root, "rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}").strip() == PROTECTED_TIP, "E_PROTECTED_TRACKING", PROTECTED_BRANCH)
    require(live_remote_tip(root, PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_LIVE", PROTECTED_BRANCH)
    local_main = run_git(root, "show-ref", "--verify", "--hash", "refs/heads/main", check=False).strip()
    require(local_main == "", "E_LOCAL_MAIN_PRESENT", local_main)
    require(run_git(root, "rev-parse", "refs/remotes/origin/main").strip() == MAIN_TIP, "E_MAIN_TRACKING", "origin/main")
    require(live_remote_tip(root, "main") == MAIN_TIP, "E_MAIN_LIVE", "main")
    require(run_git(root, "diff", "--name-only", BASELINE, "--", "Claude").strip() == "", "E_CLAUDE_DRIFT", "Claude/**")


def verify_pre_evidence_git_state(root: Path) -> None:
    require(run_git(root, "branch", "--show-current").strip() == BRANCH, "E_BRANCH", BRANCH)
    require(run_git(root, "rev-parse", "HEAD").strip() == EXPECTED_PARENT, "E_PARENT", EXPECTED_PARENT)
    require(run_git(root, "rev-parse", "@{upstream}").strip() == EXPECTED_PARENT, "E_UPSTREAM_PARENT", EXPECTED_PARENT)
    require(run_git(root, "rev-parse", f"refs/remotes/origin/{BRANCH}").strip() == EXPECTED_PARENT, "E_TRACKING_PARENT", BRANCH)
    require(live_remote_tip(root, BRANCH) == EXPECTED_PARENT, "E_LIVE_PARENT", BRANCH)
    status = parse_porcelain(run_git(root, "status", "--porcelain=v1", "--untracked-files=all"))
    require(status == EXPECTED_PRE_EVIDENCE_STATUS, "E_PRE_EVIDENCE_EXACT_SIX", repr(status))
    require(not (root / TOPOLOGY).exists() and not (root / ATTESTATION).exists(), "E_JSON_LAST_PREMATURE_ARTIFACT", "Step 70 JSON exists")
    require(run_git(root, "status", "--porcelain=v1", "--", "Claude").strip() == "", "E_CLAUDE_WORKTREE_DRIFT", "Claude/**")
    verify_protection(root)


def verify_staged(root: Path) -> None:
    require(run_git(root, "branch", "--show-current").strip() == BRANCH, "E_BRANCH", BRANCH)
    require(run_git(root, "rev-parse", "HEAD").strip() == EXPECTED_PARENT, "E_PARENT", EXPECTED_PARENT)
    status = parse_name_status(run_git(root, "diff", "--cached", "--name-status", "--no-renames", "HEAD"))
    require(status == EXPECTED_STATUS, "E_EXACT_EIGHT", repr(status))
    require(run_git(root, "diff", "--name-only").strip() == "", "E_UNSTAGED", "tracked unstaged change")
    require(run_git(root, "ls-files", "--others", "--exclude-standard").strip() == "", "E_UNTRACKED", "untracked path")
    require(run_git(root, "diff", "--cached", "--check").strip() == "", "E_DIFF_CHECK", "staged diff")
    upstream = run_git(root, "rev-parse", "@{upstream}").strip()
    require(upstream == EXPECTED_PARENT, "E_UPSTREAM_PARENT", upstream)
    require(live_remote_tip(root, BRANCH) == EXPECTED_PARENT, "E_LIVE_PARENT", BRANCH)
    verify_protection(root)


def verify_persistence(root: Path, commit: str) -> None:
    require(run_git(root, "branch", "--show-current").strip() == BRANCH, "E_BRANCH", BRANCH)
    require(run_git(root, "rev-parse", "HEAD").strip() == commit, "E_HEAD_COMMIT", commit)
    require(run_git(root, "rev-parse", f"{commit}^").strip() == EXPECTED_PARENT, "E_COMMIT_PARENT", EXPECTED_PARENT)
    require(run_git(root, "show", "-s", "--format=%s", commit).strip() == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT", EXPECTED_SUBJECT)
    status = parse_name_status(run_git(root, "diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r", f"{commit}^", commit))
    require(status == EXPECTED_STATUS, "E_COMMIT_EXACT_EIGHT", repr(status))
    require(run_git(root, "status", "--porcelain").strip() == "", "E_WORKTREE_DIRTY", "postcommit")
    require(run_git(root, "rev-parse", "@{upstream}").strip() == commit, "E_UPSTREAM_COMMIT", commit)
    require(run_git(root, "rev-parse", f"refs/remotes/origin/{BRANCH}").strip() == commit, "E_TRACKING_COMMIT", commit)
    require(live_remote_tip(root, BRANCH) == commit, "E_LIVE_COMMIT", commit)
    verify_protection(root)


def verify_result_and_controls(root: Path) -> None:
    text = (root / RESULT).read_text(encoding="utf-8")
    lines = text.splitlines()
    require(lines[3] == "Status: `PASS_PENDING_PERSISTENCE`", "E_RESULT_STATUS", lines[3])
    require("Current Step 70 gate: `PASS_P065_STEP70_PRECOMMIT`; commit/push persistence is pending." in lines, "E_RESULT_GATE", RESULT)
    require(sum(line == "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON" for line in lines) == 1, "E_RESULT_EVIDENCE_BEGIN", RESULT)
    require(sum(line == "END_P065_STEP70_HUMAN_EVIDENCE_JSON" for line in lines) == 1, "E_RESULT_EVIDENCE_END", RESULT)
    require("Those exact frozen objects contain `2,306` physical lines, not `2,068`." in lines, "E_RESULT_CORRECTED_ROOT", RESULT)
    require(any(line.startswith("Accordingly the reproducible narrative universe is `74 documents / 7,470") for line in lines), "E_RESULT_CORRECTED_TOTAL", RESULT)

    parent = markdown_table_row((root / PARENT_LEDGER).read_text(encoding="utf-8"), "065")
    require(len(parent) == 12, "E_PARENT_LEDGER_SCHEMA", repr(parent))
    require(parent[2] == "detailed-plan activation persisted; Step 70 precommit validation complete; Steps 71–75 pending", "E_PARENT_LEDGER_ACTUAL", parent[2])
    require(parent[5] == "IN_PROGRESS", "E_PARENT_LEDGER_STATUS", parent[5])
    require(parent[10] == "`PASS_P065_STEP70_PRECOMMIT`; `PASS_PENDING_PERSISTENCE`", "E_PARENT_LEDGER_GATE", parent[10])
    require(parent[11] == "exact-eight Step 70 commit/push/persistence, then Step 71", "E_PARENT_LEDGER_NEXT", parent[11])

    canonical = markdown_table_row((root / CANONICAL_LEDGER).read_text(encoding="utf-8"), "065")
    require(len(canonical) == 11, "E_CANONICAL_LEDGER_SCHEMA", repr(canonical))
    require(canonical[2] == "detailed-plan activation persisted; Step 70 precommit validation complete; Steps 71–75 pending", "E_CANONICAL_LEDGER_ACTUAL", canonical[2])
    require(canonical[4] == "IN_PROGRESS", "E_CANONICAL_LEDGER_STATUS", canonical[4])
    require(canonical[9] == "`PASS_P065_STEP70_PRECOMMIT`; `PASS_PENDING_PERSISTENCE`", "E_CANONICAL_LEDGER_GATE", canonical[9])
    require(canonical[10] == "exact-eight Step 70 commit/push/persistence, then Step 71", "E_CANONICAL_LEDGER_NEXT", canonical[10])

    handover_lines = (root / HANDOVER).read_text(encoding="utf-8").splitlines()
    require("17. 현재 Phase 상태: Phase 065 `IN_PROGRESS`, Current checkpoint: Step 70 `PASS_PENDING_PERSISTENCE`" in handover_lines, "E_HANDOVER_CURRENT", HANDOVER)
    handover_row = markdown_table_row("\n".join(handover_lines), "Phase 065 Step 70")
    require(len(handover_row) == 4, "E_HANDOVER_ROW_SCHEMA", repr(handover_row))
    require(handover_row[3] == "after persistence execute Step 71", "E_HANDOVER_NEXT", handover_row[3])


def validate(mode: str, expected_commit: str | None) -> dict[str, Any]:
    root = repo_root()
    for source_path, expected_kind in ((BUILDER, "builder"), (VALIDATOR, "validator")):
        policy = source_policy_errors((root / source_path).read_text(encoding="utf-8"), expected_kind)
        if policy:
            fail("E_SOURCE_POLICY", f"{source_path}: {'; '.join(policy)}")
    source_policy_cases = run_source_policy_negative_controls()

    topology = read_json(root / TOPOLOGY)
    attestation = read_json(root / ATTESTATION)
    errors = artifact_errors(topology, attestation)
    if errors:
        fail("E_ARTIFACT_SEMANTICS", "; ".join(errors))
    verify_phase057_frozen_sources(root, topology)
    verify_semantic_deferred_sources(root, topology, attestation)
    verify_result_and_controls(root)

    strict_json_cases = run_strict_json_negative_controls()
    semantic_cases = run_semantic_negative_controls(topology, attestation)

    builder = load_builder(root)
    built1 = builder.build_artifacts(root)
    built2 = builder.build_artifacts(root)
    require(canonical_bytes(built1[0]) == canonical_bytes(built2[0]), "E_DETERMINISM_TOPOLOGY", "2/2")
    require(canonical_bytes(built1[1]) == canonical_bytes(built2[1]), "E_DETERMINISM_ATTESTATION", "2/2")
    require(canonical_bytes(built1[0]) == (root / TOPOLOGY).read_bytes(), "E_TOPOLOGY_RECONSTRUCTION", TOPOLOGY)
    require(canonical_bytes(built1[1]) == (root / ATTESTATION).read_bytes(), "E_ATTESTATION_RECONSTRUCTION", ATTESTATION)

    if mode == "staged":
        verify_staged(root)
    elif mode == "persistence":
        if not expected_commit:
            fail("E_EXPECTED_COMMIT_REQUIRED", "--expected-commit")
        verify_persistence(root, expected_commit)

    return {
        "semantic_cases": semantic_cases,
        "source_policy_cases": source_policy_cases,
        "strict_json_cases": strict_json_cases,
        "determinism": "2/2",
        "mode": mode,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--staged", action="store_true")
    modes.add_argument("--persistence", action="store_true")
    modes.add_argument("--hardening-selftest", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.hardening_selftest:
        try:
            root = repo_root()
            for source_path, expected_kind in ((BUILDER, "builder"), (VALIDATOR, "validator")):
                policy = source_policy_errors((root / source_path).read_text(encoding="utf-8"), expected_kind)
                if policy:
                    fail("E_SOURCE_POLICY", f"{source_path}: {'; '.join(policy)}")
            cases = run_hardening_contract_probes(root)
            cases += run_atomic_writer_contract_negative_controls(root)
            cases += run_required_function_inventory_negative_controls(root)
            verify_in_progress_controls(root)
            cases += verify_in_progress_evidence_contract(root)
            verify_pre_evidence_git_state(root)
            cases += 9
            cases += run_phase057_frozen_source_negative_controls()
            builder = load_builder(root)
            cases += run_evidence_contract_negative_controls(builder)
            cases += run_finding_artifact_negative_controls()
            cases += run_process_projection_negative_controls(builder)
            cases += run_semantic_boundary_contract(root, builder)
            cases += run_repository_identity_negative_controls()
        except (ValidationFailure, OSError, KeyError, TypeError, ValueError) as exc:
            print(f"FAIL_P065_STEP70_HARDENING_SELFTEST {exc}")
            return 1
        print(f"PASS_P065_STEP70_HARDENING_SELFTEST cases={cases}")
        return 0
    mode = "persistence" if args.persistence else "staged" if args.staged else "content"
    try:
        summary = validate(mode, args.expected_commit)
    except (ValidationFailure, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL_P065_STEP70_{mode.upper()} {exc}")
        return 1
    terminal = "PASS_P065_STEP70_PERSISTENCE" if mode == "persistence" else "PASS_P065_STEP70_STAGED" if mode == "staged" else "PASS_P065_STEP70_CONTENT"
    print(f"{terminal} {json.dumps(summary, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
