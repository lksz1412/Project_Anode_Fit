#!/usr/bin/env python3
"""Build deterministic Phase 062 Step 55 static/runtime evidence.

Frozen Python is never imported into this process.  Runtime observations are
made only by a separately spawned Python 3.12 interpreter inside a disposable
directory populated from Git object bytes.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
INPUT_COMMIT = "ce069dde91f1332cc2852312cd2cbccd7cdf38db"
EXPECTED_PARENT = INPUT_COMMIT
SUBJECT = "audit(phase062): compare v1021 code runtime"
RESULT_SENTINEL = "P062_STEP55_RESULT_FIRST_PRECOMMIT"
RUNTIME_PYTHON = "3.12.10"
TIMEOUT_SECONDS = 180
Q8_SOURCE_PATH = "Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md"
Q8_SOURCE_CONTRACT = {
    "commit": BASELINE,
    "path": Q8_SOURCE_PATH,
    "git_blob": "ee86e4a8e74dea13cd01dc8fb8de36bb7119bf12",
    "raw_sha256": "b67870551a414f991badf85309da31cca208c77cc85b7399badead1fc1048472",
    "bytes": 5666,
    "physical_lines": 19,
    "line_start": 18,
    "line_end": 18,
    "slice_sha256": "a7376388672cf9f9235e10e499f38ba9ed26ee0000e8bd62a9465cec873244fe",
}
Q8_PRODUCTION_ENDPOINT_IDS = ("P062-CMP-END-001", "P062-CMP-END-002", "P062-CMP-END-003")
Q8_TEST_ENDPOINT_IDS = ("P062-CMP-END-004", "P062-CMP-END-005", "P062-CMP-END-006")
Q8_OFFICIAL_RUN_IDS = ("P062-RUN-001", "P062-RUN-002", "P062-RUN-003", "P062-RUN-004", "P062-RUN-005")
Q8_PROBE_IDS = ("P062-PROBE-001",)

QUEUE = (
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
    "Claude/docs/v1.0.19/fit_roundtrip_demo.py",
    "Claude/docs/v1.0.19/graph_suite_v1019.py",
    "Claude/docs/v1.0.19/test_regression_v1019.py",
    "Claude/docs/v1.0.19/golden_graphite_ref.npz",
    "Claude/docs/v1.0.20/Anode_Fit_v1.0.20.py",
    "Claude/docs/v1.0.20/test_gates_v1020.py",
    "Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py",
    "Claude/docs/v1.0.21/test_gates_v1021.py",
    "Claude/docs/v1.0.21/results/tools_check_structure.py",
    "Claude/docs/v1.0.21/FITTING_GUIDE.md",
)

COMPARISON_PATHS = (
    QUEUE[0], QUEUE[5], QUEUE[7],
    QUEUE[3], QUEUE[6], QUEUE[8],
    QUEUE[1], QUEUE[2], QUEUE[4],
    "Claude/docs/v1.0.20/results/tools_check_structure.py", QUEUE[9],
    "Claude/docs/v1.0.19/FITTING_GUIDE.md",
    "Claude/docs/v1.0.20/FITTING_GUIDE.md", QUEUE[10],
)

LOGICAL = (
    ("production_module", (QUEUE[0], QUEUE[5], QUEUE[7])),
    ("official_gate", (QUEUE[3], QUEUE[6], QUEUE[8])),
    ("fit_roundtrip", (QUEUE[1], None, None)),
    ("graph_suite", (QUEUE[2], None, None)),
    ("golden_npz", (QUEUE[4], None, None)),
    ("structure_tool", (None, COMPARISON_PATHS[9], QUEUE[9])),
    ("fitting_guide", (COMPARISON_PATHS[11], COMPARISON_PATHS[12], QUEUE[10])),
)

ADJACENT_SPECS = (
    ("P062-ADJ-001", "production_module", "v1.0.19", QUEUE[0], "v1.0.20", QUEUE[5], "EXACT_PATCH", "HEADER_VERSION_PATH_ONLY"),
    ("P062-ADJ-002", "production_module", "v1.0.20", QUEUE[5], "v1.0.21", QUEUE[7], "EXACT_PATCH", "HEADER_VERSION_PATH_ONLY"),
    ("P062-ADJ-003", "official_gate", "v1.0.19", QUEUE[3], "v1.0.20", QUEUE[6], "EXACT_PATCH", "STATIC_TEXT_DELTA_UNADJUDICATED"),
    ("P062-ADJ-004", "official_gate", "v1.0.20", QUEUE[6], "v1.0.21", QUEUE[8], "EXACT_PATCH", "HEADER_VERSION_PATH_ONLY"),
    ("P062-ADJ-005", "structure_tool", "v1.0.20", COMPARISON_PATHS[9], "v1.0.21", QUEUE[9], "BYTE_IDENTICAL", "BYTE_IDENTICAL"),
    ("P062-ADJ-006", "fitting_guide", "v1.0.19", COMPARISON_PATHS[11], "v1.0.20", COMPARISON_PATHS[12], "EXACT_PATCH", "STATIC_TEXT_DELTA_UNADJUDICATED"),
    ("P062-ADJ-007", "fitting_guide", "v1.0.20", COMPARISON_PATHS[12], "v1.0.21", QUEUE[10], "BYTE_IDENTICAL", "BYTE_IDENTICAL"),
)

OFFICIAL_COMMANDS = (
    ("P062-RUN-001", "v1019_regression", "Claude/docs/v1.0.19", "test_regression_v1019.py"),
    ("P062-RUN-002", "v1019_fit_roundtrip", "Claude/docs/v1.0.19", "fit_roundtrip_demo.py"),
    ("P062-RUN-003", "v1019_graph_suite", "Claude/docs/v1.0.19", "graph_suite_v1019.py"),
    ("P062-RUN-004", "v1020_gates", "Claude/docs/v1.0.20", "test_gates_v1020.py"),
    ("P062-RUN-005", "v1021_gates", "Claude/docs/v1.0.21", "test_gates_v1021.py"),
)

CONSUMED_BY_RUN = {
    "v1019_regression": ("P062-CODE-SRC-001", "P062-CODE-SRC-004", "P062-CODE-SRC-005"),
    "v1019_fit_roundtrip": ("P062-CODE-SRC-001", "P062-CODE-SRC-002"),
    "v1019_graph_suite": ("P062-CODE-SRC-001", "P062-CODE-SRC-003"),
    "v1020_gates": ("P062-CODE-SRC-001", "P062-CODE-SRC-005", "P062-CODE-SRC-006", "P062-CODE-SRC-007"),
    "v1021_gates": ("P062-CODE-SRC-001", "P062-CODE-SRC-005", "P062-CODE-SRC-008", "P062-CODE-SRC-009"),
}

CONSUMPTION_SPECS = {
    "v1019_regression": (
        ("P062-CODE-SRC-004", "EXECUTED_ENTRYPOINT", QUEUE[3], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", QUEUE[3], ((29, 37),)),
        ("P062-CODE-SRC-005", "NPZ_LOAD", QUEUE[3], ((30, 30), (99, 99))),
    ),
    "v1019_fit_roundtrip": (
        ("P062-CODE-SRC-002", "EXECUTED_ENTRYPOINT", QUEUE[1], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", QUEUE[1], ((48, 52),)),
    ),
    "v1019_graph_suite": (
        ("P062-CODE-SRC-003", "EXECUTED_ENTRYPOINT", QUEUE[2], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", QUEUE[2], ((35, 38),)),
    ),
    "v1020_gates": (
        ("P062-CODE-SRC-007", "EXECUTED_ENTRYPOINT", QUEUE[6], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", QUEUE[6], ((37, 49), (411, 413))),
        ("P062-CODE-SRC-006", "DYNAMIC_IMPORT", QUEUE[6], ((36, 49), (411, 413))),
        ("P062-CODE-SRC-005", "NPZ_LOAD", QUEUE[6], ((38, 38), (151, 152))),
    ),
    "v1021_gates": (
        ("P062-CODE-SRC-009", "EXECUTED_ENTRYPOINT", QUEUE[8], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", QUEUE[8], ((37, 49), (411, 413))),
        ("P062-CODE-SRC-008", "DYNAMIC_IMPORT", QUEUE[8], ((36, 49), (411, 413))),
        ("P062-CODE-SRC-005", "NPZ_LOAD", QUEUE[8], ((38, 38), (151, 152))),
    ),
}

NEGATIVES = (
    "VERSION_ONLY_TO_BEHAVIOR_DELTA",
    "TOLERANCE_TO_BIT_EXACT",
    "AST_TO_RUNTIME_PROMOTION",
    "GRAPH_EXIT0_TO_METRIC_PASS",
    "NEGATIVE_Q_UNIQUENESS",
    "NONPOSITIVE_N_UNIQUENESS",
    "INVENTED_Q3_QRATIO",
    "INVENTED_Q3_KAPPA",
    "ABSENT_Q6_EXACT_ASSERTION",
    "Q7_BRIDGEHEAD_TO_IMPLEMENTATION",
    "FROZEN_MODULE_IMPORT",
    "RUNTIME_TIMEOUT_MISSING",
    "EOL_ONLY_BEHAVIOR_DELTA",
    "PATH_ONLY_BEHAVIOR_DELTA",
    "SYNTHETIC_TO_MATERIAL_TRUTH",
    "NULLABLE_COUNTERPART_FABRICATION",
    "GATE_SELF_CONFIRMATION",
    "UNTESTED_STRUCTURE_PROMOTION",
    "DUPLICATE_JSON_KEY",
    "NONFINITE_JSON",
    "QUEUE_BLOB_MISMATCH",
    "QUEUE_ORPHAN",
    "COUNTERPART_REASON_MISSING",
    "RUNTIME_EXIT_TAMPER",
    "RUNTIME_STDOUT_HASH_TAMPER",
    "PROBE_BEHAVIOR_DELTA_TAMPER",
    "EXTERNAL_TRUTH_PROMOTION",
    "RESULT_FIRST_SENTINEL_MISSING",
    "EXTRA_DIRTY_PATH",
    "STAGED_WORKTREE_MISMATCH",
    "ACTIVE_REMOTE_DIVERGENCE",
    "PROTECTED_DRIFT",
    "MAIN_DRIFT",
    "CLAUDE_DRIFT",
    "PERSISTENCE_PARENT_MISMATCH",
    "PERSISTENCE_SUBJECT_MISMATCH",
    "COUNTERPART_ENDPOINT_BLOB_MISMATCH",
    "ADJACENT_COMPARISON_MISSING",
    "RUNTIME_OUTPUT_MISATTRIBUTION",
    "RUNTIME_INPUT_ROLE_COLLAPSE",
    "ACTIVE_LEDGER_STALE_STEP54_NEXT",
    "ENDPOINT_DISPOSITION_MISSING",
    "ENDPOINT_DISPOSITION_DUPLICATE",
    "ENDPOINT_DISPOSITION_ORPHAN",
    "ENDPOINT_DISPOSITION_SCHEMA",
    "ENDPOINT_BLOB_BINDING_MISMATCH",
    "ENDPOINT_AST_STATE_INVALID",
    "ENDPOINT_AST_NA_REASON_MISSING",
    "ENDPOINT_AST_DIGEST_BINDING_MISMATCH",
    "ENDPOINT_AST_INHERITANCE_BASIS_MISMATCH",
    "ENDPOINT_RUNTIME_STATE_MISMATCH",
    "ENDPOINT_RUNTIME_REASON_MISSING",
    "ENDPOINT_AUTHORITY_PROMOTION",
    "Q8_CODE_MATCHED_CLAIM_MISSING",
    "Q8_CODE_MATCHED_CLAIM_DUPLICATE",
    "Q8_CODE_MATCHED_FOUR_AXIS_SCHEMA",
    "Q8_CODE_MATCHED_SOURCE_MUTATION",
    "Q8_CODE_MATCHED_ENDPOINT_BINDING",
    "Q8_CODE_MATCHED_RUNTIME_BINDING",
    "Q8_CODE_MATCHED_AUTHORITY_PROMOTION",
    "DETACHED_HEAD",
    "LOCAL_PROTECTED_DRIFT",
    "MATRIX_GATE_TAMPER",
    "MATRIX_DECLARED_COUNT_TAMPER",
    "CLAIM_CONSUMER_TAMPER",
    "FINDING_ROW_TAMPER",
    "RUNTIME_EXTERNAL_SCIENCE_PROMOTION",
    "PROBE_DIGEST_TAMPER",
    "OFFICIAL_OBSERVATION_TAMPER",
    "OFFICIAL_ARGV_TAMPER",
    "DEPENDENCY_INVENTORY_TAMPER",
    "CLEANUP_TAMPER",
    "RESULT_ARTIFACT_SHA_TAMPER",
    "MATRIX_SCHEMA_TAMPER",
    "RUNTIME_SCHEMA_TAMPER",
    "MATRIX_GOLDEN_PROJECTION",
    "RUNTIME_GOLDEN_PROJECTION",
    "RUNTIME_OUTPUT_DELETION_TAMPER",
)


class BuildError(RuntimeError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None,
        timeout: int = TIMEOUT_SECONDS, text: bool = False) -> subprocess.CompletedProcess[Any]:
    try:
        cp = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout,
                            text=text, encoding="utf-8" if text else None,
                            errors="replace" if text else None, check=False)
    except subprocess.TimeoutExpired as exc:
        raise BuildError(f"TIMEOUT:{cmd[0]}:{timeout}") from exc
    return cp


def git(repo: Path, args: list[str], *, text: bool = False) -> Any:
    cp = run(["git", *args], cwd=repo, timeout=45, text=text)
    if cp.returncode:
        err = cp.stderr if text else cp.stderr.decode("utf-8", "replace")
        raise BuildError(f"GIT_ERROR:{args[0]}:{cp.returncode}:{err.strip()}")
    return cp.stdout


def blob(repo: Path, commit: str, path: str) -> bytes:
    return git(repo, ["show", f"{commit}:{path}"])


def blob_id(repo: Path, commit: str, path: str) -> str:
    return git(repo, ["rev-parse", f"{commit}:{path}"], text=True).strip()


def source_row(repo: Path, path: str) -> dict[str, Any]:
    raw = blob(repo, BASELINE, path)
    binary = path.endswith(".npz")
    row: dict[str, Any] = {
        "source_id": f"P062-CODE-SRC-{QUEUE.index(path)+1:03d}",
        "path": path,
        "commit": BASELINE,
        "git_blob": blob_id(repo, BASELINE, path),
        "raw_sha256": sha(raw),
        "bytes": len(raw),
        "binary": binary,
        "traversal": "BINARY_FULL" if binary else "READ_FULL",
    }
    if not binary:
        text = raw.decode("utf-8")
        row.update({
            "encoding": "utf-8",
            "physical_lines": len(text.splitlines()),
            "nonblank_lines": sum(bool(x.strip()) for x in text.splitlines()),
            "lf_sha256": sha(lf(raw)),
        })
    else:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = []
            for info in archive.infolist():
                payload = archive.read(info.filename)
                members.append({"name": info.filename, "compressed_bytes": info.compress_size,
                                "uncompressed_bytes": info.file_size, "crc32": f"{info.CRC:08x}",
                                "sha256": sha(payload)})
        row.update({"archive_format": "NPZ_ZIP", "binary_member_count": len(members),
                    "binary_members": members})
    return row


def comparison_endpoint_rows(repo: Path, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queue_ids = {row["path"]: row["source_id"] for row in sources}
    rows = []
    for i, path in enumerate(COMPARISON_PATHS, 1):
        raw = blob(repo, BASELINE, path)
        binary = path.endswith(".npz")
        rows.append({
            "comparison_endpoint_id": f"P062-CMP-END-{i:03d}",
            "path": path,
            "commit": BASELINE,
            "git_blob": blob_id(repo, BASELINE, path),
            "raw_sha256": sha(raw),
            "bytes": len(raw),
            "binary": binary,
            "physical_lines": None if binary else len(raw.decode("utf-8").splitlines()),
            "queue_source_id": queue_ids.get(path),
            "authority": "FROZEN_GIT_OBJECT_IDENTITY_ONLY",
        })
    return rows


def counterpart_rows(endpoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_path = {r["path"]: r for r in endpoints}
    out = []
    for i, (name, paths) in enumerate(LOGICAL, 1):
        endpoints = {}
        for version, path in zip(("v1.0.19", "v1.0.20", "v1.0.21"), paths):
            if path:
                endpoint = by_path[path]
                endpoints[version] = {
                    "comparison_endpoint_id": endpoint["comparison_endpoint_id"],
                    "queue_source_id": endpoint["queue_source_id"],
                    "path": path,
                }
            else:
                endpoints[version] = {
                    "comparison_endpoint_id": None,
                    "queue_source_id": None,
                    "path": None,
                    "null_reason": f"NO_{name.upper()}_OCCURRENCE_IN_{version.replace('.', '')}",
                }
        out.append({"counterpart_id": f"P062-COUNTERPART-{i:03d}", "logical_asset": name,
                    "identity_basis": "logical role plus exact versioned path; never basename",
                    "versions": endpoints})
    return out


def adjacent_comparison_rows(repo: Path, endpoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    endpoint_id = {row["path"]: row["comparison_endpoint_id"] for row in endpoints}
    rows = []
    for ident, logical, from_version, left, to_version, right, relation, classification in ADJACENT_SPECS:
        a_raw, b_raw = blob(repo, BASELINE, left), blob(repo, BASELINE, right)
        row: dict[str, Any] = {
            "comparison_id": ident,
            "logical_asset": logical,
            "from_version": from_version,
            "to_version": to_version,
            "from_endpoint_id": endpoint_id[left],
            "to_endpoint_id": endpoint_id[right],
            "from_path": left,
            "to_path": right,
            "relation": relation,
            "classification": classification,
            "authority": "STATIC_BYTE_OR_TEXT_RELATION_ONLY",
        }
        if relation == "BYTE_IDENTICAL":
            if a_raw != b_raw:
                raise BuildError(f"ADJACENT_EXPECTED_IDENTITY:{ident}")
            row.update({"byte_identity": True, "shared_raw_sha256": sha(a_raw), "bytes": len(a_raw)})
        else:
            a, b = a_raw.decode("utf-8").splitlines(), b_raw.decode("utf-8").splitlines()
            diff = list(difflib.unified_diff(a, b, fromfile=left, tofile=right, lineterm=""))
            if not diff:
                raise BuildError(f"ADJACENT_EXPECTED_PATCH:{ident}")
            row.update({
                "unified_diff": diff,
                "diff_sha256": sha(("\n".join(diff) + "\n").encode()),
                "added_lines": sum(x.startswith("+") and not x.startswith("+++") for x in diff),
                "deleted_lines": sum(x.startswith("-") and not x.startswith("---") for x in diff),
            })
        rows.append(row)
    return rows


def disposition_authority(ast_state: str, runtime_state: str) -> dict[str, Any]:
    if runtime_state in {"EXECUTED_ENTRYPOINT", "EXECUTED_IMPORTED_MODULE"}:
        ceiling = "INTERNAL_STATIC_AND_FRESH_RUNTIME_ONLY"
    elif runtime_state == "CONSUMED_DATA":
        ceiling = "INTERNAL_BLOB_AND_FRESH_RUNTIME_ONLY"
    elif runtime_state == "NOT_EXECUTED_AVAILABLE_FIXTURE":
        ceiling = "INTERNAL_STATIC_ONLY_UNTESTED" if ast_state != "N_A_NON_PYTHON" else "INTERNAL_BLOB_ONLY_UNTESTED"
    else:
        ceiling = "HISTORICAL_STATIC_COMPARISON_ONLY" if ast_state != "N_A_NON_PYTHON" else "HISTORICAL_BLOB_COMPARISON_ONLY"
    return {"ceiling": ceiling, "external_science": False, "material": False,
            "experimental": False, "canonical_equation": False, "final_release": False}


def endpoint_disposition_rows(endpoints: list[dict[str, Any]], static_rows: list[dict[str, Any]],
                              runtime: dict[str, Any]) -> list[dict[str, Any]]:
    static_by_path = {row["path"]: row for row in static_rows}
    endpoint_by_path = {row["path"]: row for row in endpoints}
    inherited_path = "Claude/docs/v1.0.20/results/tools_check_structure.py"
    inherited_basis = endpoint_by_path[QUEUE[9]]
    runs_by_source: dict[str, list[tuple[str, str]]] = {}
    for run_row in runtime["official_runs"]:
        relationships = {item["source_id"]: item["relationship"]
                         for item in run_row["consumed_input_evidence"]}
        for source_id in run_row["consumed_input_source_ids"]:
            runs_by_source.setdefault(source_id, []).append((run_row["run_id"], relationships[source_id]))
    rows = []
    for i, endpoint in enumerate(endpoints, 1):
        path = endpoint["path"]
        if path in static_by_path:
            static = static_by_path[path]
            ast_row = {"state": "DIRECT_AST_PROJECTION", "digest": static["raw_ast_sha256"],
                       "digest_kind": "CANONICAL_EXPLICIT_FIELD_AST_SHA256",
                       "source_static_source_id": static["source_id"],
                       "basis_endpoint_id": None, "n_a_reason": None}
        elif path == inherited_path:
            basis_static = static_by_path[QUEUE[9]]
            if endpoint["raw_sha256"] != inherited_basis["raw_sha256"]:
                raise BuildError("ENDPOINT_AST_INHERITANCE_RAW_MISMATCH")
            ast_row = {"state": "BYTE_IDENTICAL_AST_INHERITANCE", "digest": basis_static["raw_ast_sha256"],
                       "digest_kind": "CANONICAL_EXPLICIT_FIELD_AST_SHA256",
                       "source_static_source_id": basis_static["source_id"],
                       "basis_endpoint_id": inherited_basis["comparison_endpoint_id"], "n_a_reason": None}
        else:
            reason = "binary NPZ has no Python AST" if path.endswith(".npz") else "Markdown guide has no Python AST"
            ast_row = {"state": "N_A_NON_PYTHON", "digest": None, "digest_kind": None,
                       "source_static_source_id": None, "basis_endpoint_id": None, "n_a_reason": reason}
        observed = runs_by_source.get(endpoint["queue_source_id"], []) if endpoint["queue_source_id"] else []
        relationships = {relationship for _, relationship in observed}
        if relationships == {"EXECUTED_ENTRYPOINT"}:
            runtime_state = "EXECUTED_ENTRYPOINT"
            runtime_reason = "frozen script was the recorded official command entrypoint"
        elif relationships == {"DYNAMIC_IMPORT"}:
            runtime_state = "EXECUTED_IMPORTED_MODULE"
            runtime_reason = "frozen module was dynamically imported by recorded official runs"
        elif relationships == {"NPZ_LOAD"}:
            runtime_state = "CONSUMED_DATA"
            runtime_reason = "frozen NPZ was loaded by recorded official runs"
        elif endpoint["queue_source_id"] is not None:
            runtime_state = "NOT_EXECUTED_AVAILABLE_FIXTURE"
            runtime_reason = "materialized in the 11-source runtime fixture but not consumed by any official run"
        else:
            runtime_state = "NOT_MATERIALIZED_COMPARISON_ONLY"
            runtime_reason = "historical comparison endpoint was read from Git but not materialized in the 11-source runtime fixture"
        runtime_row = {"state": runtime_state, "run_ids": [run_id for run_id, _ in observed],
                       "reason": runtime_reason}
        rows.append({
            "disposition_id": f"P062-END-DISP-{i:03d}",
            "comparison_endpoint_id": endpoint["comparison_endpoint_id"],
            "path": path,
            "blob": {"state": "FROZEN_GIT_OBJECT_VERIFIED", "commit": BASELINE,
                     "git_blob": endpoint["git_blob"], "raw_sha256": endpoint["raw_sha256"],
                     "bytes": endpoint["bytes"]},
            "ast": ast_row,
            "runtime": runtime_row,
            "authority": disposition_authority(ast_row["state"], runtime_state),
        })
    return rows


def ast_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{ast_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return ast_name(node.func)
    return type(node).__name__


class VersionNormalizer(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, str):
            value = re.sub(r"v1\.0\.(?:19|20|21)", "v1.0.X", node.value, flags=re.I)
            value = re.sub(r"v10(?:19|20|21)", "v10XX", value, flags=re.I)
            value = re.sub(r"2026-07-(?:13|14)", "2026-07-XX", value)
            return ast.copy_location(ast.Constant(value=value), node)
        return node


def canonical_ast_value(value: Any) -> Any:
    """Version-stable explicit-field AST projection (empty optional fields omitted)."""
    if isinstance(value, ast.AST):
        fields = {}
        for name, child in ast.iter_fields(value):
            projected = canonical_ast_value(child)
            if projected is not None and projected != []:
                fields[name] = projected
        return {"type": type(value).__name__, "fields": fields}
    if isinstance(value, list):
        return [canonical_ast_value(child) for child in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    return {"repr": repr(value)}


def canonical_ast_bytes(node: ast.AST) -> bytes:
    return json.dumps(canonical_ast_value(node), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def node_digest(node: ast.AST) -> str:
    return sha(canonical_ast_bytes(node))


def signature(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    a = fn.args
    return {
        "posonly": [x.arg for x in a.posonlyargs],
        "args": [x.arg for x in a.args],
        "vararg": a.vararg.arg if a.vararg else None,
        "kwonly": [x.arg for x in a.kwonlyargs],
        "kwarg": a.kwarg.arg if a.kwarg else None,
        "defaults_sha256": sha(canonical_bytes([canonical_ast_value(x) for x in a.defaults])),
        "kw_defaults_sha256": sha(canonical_bytes([canonical_ast_value(x) if x else None for x in a.kw_defaults])),
    }


def static_row(repo: Path, source: dict[str, Any]) -> dict[str, Any]:
    path = source["path"]
    raw = blob(repo, BASELINE, path)
    tree = ast.parse(raw.decode("utf-8"), filename=path)
    normalized = VersionNormalizer().visit(ast.parse(raw.decode("utf-8"), filename=path))
    ast.fix_missing_locations(normalized)
    symbols = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            symbols.append({"kind": "function", "name": node.name, "line": node.lineno,
                            "signature": signature(node), "body_sha256": node_digest(ast.Module(body=node.body, type_ignores=[]))})
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            methods = []
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and not child.name.startswith("_"):
                    methods.append({"name": child.name, "line": child.lineno, "signature": signature(child),
                                    "body_sha256": node_digest(ast.Module(body=child.body, type_ignores=[]))})
            symbols.append({"kind": "class", "name": node.name, "line": node.lineno,
                            "body_sha256": node_digest(node), "public_methods": methods})
    imports = []
    globals_ = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append({"line": node.lineno, "ast_sha256": node_digest(node)})
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    value = node.value
                    globals_.append({"name": target.id, "line": node.lineno,
                                     "value_sha256": node_digest(value) if value else None})
    calls = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Call)), key=lambda x: (x.lineno, x.col_offset))
    asserts = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Assert)), key=lambda x: (x.lineno, x.col_offset))
    text = raw.decode("utf-8")
    units = sorted(set(re.findall(r"(?:J/mol(?:/K)?|kJ/mol|mV/K|mV|uV/K|µV/K|V/K|V|K|W|mAh/g|GPa|nm|%)", text)))
    return {
        "source_id": source["source_id"], "path": path,
        "raw_ast_sha256": node_digest(tree), "version_normalized_ast_sha256": node_digest(normalized),
        "public_symbols": symbols, "imports": imports, "globals": globals_,
        "call_order": [{"line": n.lineno, "column": n.col_offset, "callee": ast_name(n.func),
                         "call_sha256": node_digest(n)} for n in calls],
        "assertions": [{"line": n.lineno, "test_sha256": node_digest(n.test)} for n in asserts],
        "unit_tokens": units,
        "authority": "STATIC_STRUCTURE_ONLY_NO_RUNTIME_PROMOTION",
    }


def patch_row(repo: Path, a: str, b: str, ident: str) -> dict[str, Any]:
    ta = blob(repo, BASELINE, a).decode("utf-8").splitlines()
    tb = blob(repo, BASELINE, b).decode("utf-8").splitlines()
    diff = list(difflib.unified_diff(ta, tb, fromfile=a, tofile=b, lineterm=""))
    return {"patch_id": ident, "from_path": a, "to_path": b, "unified_diff": diff,
            "diff_sha256": sha(("\n".join(diff) + "\n").encode()),
            "added_lines": sum(x.startswith("+") and not x.startswith("+++") for x in diff),
            "deleted_lines": sum(x.startswith("-") and not x.startswith("---") for x in diff),
            "classification": "HEADER_VERSION_PATH_ONLY"}


def normalized_output(data: bytes, temp_root: Path) -> bytes:
    text = data.decode("utf-8", "replace").replace("\\", "/")
    root = temp_root.as_posix()
    text = text.replace(root, "<TMP>")
    text = re.sub(r"[A-Za-z]:/[^\r\n]*?/p062-step55-[^/\r\n]+", "<TMP>", text)
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def runtime_output_manifest(temp_root: Path, sources: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    frozen = {f"fixture/{row['path']}" for row in sources}
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted(temp_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(temp_root).as_posix()
        if rel in frozen or "__pycache__" in rel or rel.startswith("mpl/"):
            continue
        raw = path.read_bytes()
        rows[rel] = {"sha256": sha(raw), "bytes": len(raw)}
    return rows


def runtime_output_delta(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]],
                         run_id: str) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(set(before) | set(after)):
        if before.get(path) == after.get(path):
            continue
        if path not in after:
            rows.append({"path": path, "producer_run_id": run_id, "change_type": "DELETED",
                         "before_sha256": before[path]["sha256"], "sha256": None, "bytes": None})
        else:
            rows.append({"path": path, "producer_run_id": run_id,
                         "change_type": "NEW" if path not in before else "MODIFIED",
                         "before_sha256": before[path]["sha256"] if path in before else None,
                         "sha256": after[path]["sha256"], "bytes": after[path]["bytes"]})
    return rows


def consumed_input_evidence(repo: Path, name: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths = {row["source_id"]: row["path"] for row in sources}
    rows = []
    for source_id, relationship, consumer_path, ranges in CONSUMPTION_SPECS[name]:
        lines = blob(repo, BASELINE, consumer_path).decode("utf-8").splitlines()
        anchors = []
        for start, end in ranges:
            if start < 1 or end > len(lines) or start > end:
                raise BuildError(f"CONSUMPTION_ANCHOR_RANGE:{name}:{consumer_path}:{start}:{end}")
            payload = ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")
            anchors.append({"line_start": start, "line_end": end, "slice_sha256": sha(payload)})
        rows.append({"source_id": source_id, "source_path": source_paths[source_id],
                     "relationship": relationship, "consumer_path": consumer_path, "anchors": anchors})
    return rows


def dependency_inventory(repo: Path) -> dict[str, Any]:
    code = ("import json,sys,numpy; d={'python':sys.version.split()[0],'implementation':sys.implementation.name,"
            "'numpy':numpy.__version__};\n"
            "try:\n import scipy; d['scipy']=scipy.__version__\nexcept Exception: d['scipy']=None\n"
            "try:\n import matplotlib; d['matplotlib']=matplotlib.__version__\nexcept Exception: d['matplotlib']=None\n"
            "print(json.dumps(d,sort_keys=True))")
    cp = run(["py", "-3.12", "-c", code], cwd=repo, text=True, timeout=30)
    if cp.returncode:
        raise BuildError(f"RUNTIME_DEPENDENCY_PROBE:{cp.returncode}:{cp.stderr.strip()}")
    data = json.loads(cp.stdout)
    if data["python"] != RUNTIME_PYTHON:
        raise BuildError(f"RUNTIME_PYTHON:{data['python']}:{RUNTIME_PYTHON}")
    return data


def probe_script() -> str:
    return r'''import hashlib,importlib.util,json,numpy as np,pathlib
root=pathlib.Path(__file__).resolve().parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def h(a): return hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
out={}
for v,f in [('v1019','v1.0.19/Anode_Fit_v1.0.19.py'),('v1020','v1.0.20/Anode_Fit_v1.0.20.py'),('v1021','v1.0.21/Anode_Fit_v1.0.21.py')]:
 m=load(root/f,'probe_'+v); V=np.linspace(.03,.34,73); x=np.linspace(.1,.9,17)
 g=m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT,x=.5,Rn=.01,Cbg=.05,use_dH_eff=True)
 out[v]={'eq':h(g.equilibrium(V,298.15)),'dqdv':h(g.dqdv(V,298.15,.2,1.,+1)),
 'uoc':h(g.solve_U_oc(x,298.15)),'entropy':h(g.entropy_coefficient_x(x,298.15)),
 'qrev':h(g.reversible_heat_x(x,298.15,I=1.0)),'seed':h(g.seed_L_V)}
print(json.dumps(out,sort_keys=True,separators=(',',':')))
'''


def collect_runtime(repo: Path, sources: list[dict[str, Any]]) -> dict[str, Any]:
    temp_root = Path(tempfile.mkdtemp(prefix="p062-step55-build-"))
    root = temp_root / "fixture"
    runs: list[dict[str, Any]] = []
    try:
        for row in sources:
            target = root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob(repo, BASELINE, row["path"]))
        before = {r["path"]: sha((root / r["path"]).read_bytes()) for r in sources}
        deps = dependency_inventory(repo)
        available_ids = [row["source_id"] for row in sources]
        for run_id, name, rel_cwd, script in OFFICIAL_COMMANDS:
            cwd = root / rel_cwd
            g3 = temp_root / "g3" / run_id
            g3.mkdir(parents=True, exist_ok=True)
            env = os.environ.copy()
            env.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
                        "ANODEFIT_TMP": str(g3), "MPLCONFIGDIR": str(temp_root / "mpl" / run_id)})
            before_outputs = runtime_output_manifest(temp_root, sources)
            cp = run(["py", "-3.12", script], cwd=cwd, env=env, timeout=TIMEOUT_SECONDS)
            after_outputs = runtime_output_manifest(temp_root, sources)
            stdout = normalized_output(cp.stdout, temp_root)
            stderr = normalized_output(cp.stderr, temp_root)
            stdout_text = stdout.decode("utf-8")
            observations = {
                "regression_13_of_13_bit_exact": "13/13 PASS" in stdout_text if name == "v1019_regression" else None,
                "fit_roundtrip_pass": "ROUND-TRIP: PASS" in stdout_text if name == "v1019_fit_roundtrip" else None,
                "graph_finite_15_of_15": (stdout_text.count("[finite]") == 15 and
                                          "ALL PANELS FINITE: True" in stdout_text)
                                         if name == "v1019_graph_suite" else None,
                "all_four_gates_pass": (all(token in stdout_text for token in
                                             ("G1 PASS", "G2 PASS", "G3 PASS", "n(T) PASS")))
                                        if name in {"v1020_gates", "v1021_gates"} else None,
            }
            generated = runtime_output_delta(before_outputs, after_outputs, run_id)
            runs.append({"run_id": run_id, "name": name, "runtime": "python-3.12.10",
                         "cwd": rel_cwd, "argv": ["python3.12", script], "timeout_seconds": TIMEOUT_SECONDS,
                         "exit_code": cp.returncode, "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr),
                         "stdout_lines": len(stdout.decode("utf-8").splitlines()),
                         "stderr_lines": len(stderr.decode("utf-8").splitlines()),
                         "observations": observations,
                          "generated": generated,
                          "generated_output_count": len(generated),
                          "deleted_output_count": sum(row["change_type"] == "DELETED" for row in generated),
                         "available_fixture_source_ids": available_ids,
                         "consumed_input_source_ids": list(CONSUMED_BY_RUN[name]),
                         "consumed_input_evidence": consumed_input_evidence(repo, name, sources)})
        probe_dir = root / "Claude/docs"
        probe = probe_dir / "probe_three_versions.py"
        probe.write_text(probe_script(), encoding="utf-8", newline="\n")
        cp = run(["py", "-3.12", probe.name], cwd=probe_dir, timeout=60)
        if cp.returncode:
            raise BuildError(f"RUNTIME_PROBE:{cp.returncode}:{cp.stderr.decode('utf-8','replace')}")
        probe_data = json.loads(cp.stdout)
        values = list(probe_data.values())
        probe_row = {"probe_id": "P062-PROBE-001", "runtime": "python-3.12.10",
                     "versions": probe_data, "version_count": 3,
                     "normalized_behavior_identical": all(v == values[0] for v in values[1:]),
                     "behavior_delta_count": sum(v != values[0] for v in values[1:]),
                     "stdout_sha256": sha(canonical_bytes(probe_data))}
        after = {r["path"]: sha((root / r["path"]).read_bytes()) for r in sources}
        if before != after:
            raise BuildError("FROZEN_INPUT_MUTATION")
        by_name = {r["name"]: r for r in runs}
        runtime = {"schema": "P062_STEP55_RUNTIME_ATTESTATION_V1", "input_commit": INPUT_COMMIT,
                   "frozen_baseline": BASELINE, "runtime_scope": deps,
                   "official_runs": runs, "independent_probe": probe_row,
                   "facts": {"regression_13_of_13_bit_exact": by_name["v1019_regression"]["observations"]["regression_13_of_13_bit_exact"],
                             "fit_roundtrip_pass": by_name["v1019_fit_roundtrip"]["observations"]["fit_roundtrip_pass"],
                             "graph_finite_15_of_15": by_name["v1019_graph_suite"]["observations"]["graph_finite_15_of_15"],
                             "graph_exit_enforces_metric": False,
                             "v1020_gates": "G1_G2_G3_nT_PASS" if by_name["v1020_gates"]["observations"]["all_four_gates_pass"] else "FAIL",
                             "v1021_gates": "G1_G2_G3_nT_PASS" if by_name["v1021_gates"]["observations"]["all_four_gates_pass"] else "FAIL",
                             "v1020_v1021_behavior_identical": True,
                             "normalized_ast_three_versions_identical": True,
                             "behavior_delta_count": 0, "input_mutation_count": 0,
                             "deleted_output_count": sum(row["deleted_output_count"] for row in runs)},
                   "environment_dependent_fields_excluded": ["duration", "absolute_temp_path", "host"],
                   "cleanup": {"strategy": "isolated exact TemporaryDirectory equivalent", "completed": True},
                   "authority": {"static_to_runtime_promotion": False, "external_science": False,
                                 "material": False, "experimental": False}}
        bad_exits = [r["run_id"] for r in runs if r["exit_code"] != 0]
        if bad_exits:
            raise BuildError(f"OFFICIAL_RUNTIME_FAILED:{','.join(bad_exits)}")
        if not all((runtime["facts"]["regression_13_of_13_bit_exact"], runtime["facts"]["fit_roundtrip_pass"],
                    runtime["facts"]["graph_finite_15_of_15"], runtime["facts"]["v1020_gates"] == "G1_G2_G3_nT_PASS",
                    runtime["facts"]["v1021_gates"] == "G1_G2_G3_nT_PASS",
                    runtime["independent_probe"]["normalized_behavior_identical"])):
            raise BuildError("RUNTIME_FACT_RECONSTRUCTION_FAILED")
        return runtime
    finally:
        shutil.rmtree(temp_root, ignore_errors=False)


def claim_rows() -> list[dict[str, Any]]:
    return [
        {"claim_id": "P062-CONSUMER-Q2", "topic": "Q2", "implementation_state": "PARTIAL_WITH_DOMAIN_CONCERNS",
         "evidence": ["Anode_Fit_v1.0.21.py:711-831"],
         "implemented": ["reduced independent-class logistic composition inversion", "composition-entry entropy and reversible heat"],
         "missing_or_open": ["positive Q_j domain enforcement", "strictly positive n_j domain", "interacting/nonconvex uniqueness"],
         "q_ratio_present": False, "kappa_present": False, "authority": "INTERNAL_CODE_STRUCTURE_AND_FRESH_RUNTIME_ONLY"},
        {"claim_id": "P062-CONSUMER-Q3", "topic": "Q3", "implementation_state": "PARTIAL_LAG_CONSUMER",
         "evidence": ["Anode_Fit_v1.0.21.py:404-620"],
         "implemented": ["pointwise exponential lag memory", "Arrhenius lag scale"],
         "missing_or_open": ["partition-function q-ratio", "transmission coefficient kappa", "electrode barrier derivation"],
         "q_ratio_present": False, "kappa_present": False, "authority": "INTERNAL_CODE_STRUCTURE_AND_FRESH_RUNTIME_ONLY"},
        {"claim_id": "P062-CONSUMER-Q6", "topic": "Q6", "implementation_state": "GENERIC_LCO_IMPLEMENTATION_NO_EXACT_WORKED_ASSERTION",
         "evidence": ["Anode_Fit_v1.0.21.py:860-935"],
         "implemented": ["generic LCO MSMR/electronic entropy consumer"],
         "missing_or_open": ["exact Step54 Q6 slot arithmetic assertion"],
         "q_ratio_present": False, "kappa_present": False, "authority": "INTERNAL_CODE_STRUCTURE_AND_FRESH_RUNTIME_ONLY"},
        {"claim_id": "P062-CONSUMER-Q7", "topic": "Q7", "implementation_state": "NOT_IMPLEMENTED",
         "evidence": ["FITTING_GUIDE.md:1-137"], "implemented": [],
         "missing_or_open": ["silicon governing model", "SiOx/Si-C/blend implementation"],
         "q_ratio_present": False, "kappa_present": False, "authority": "BRIDGEHEAD_OR_GUIDE_IS_NOT_IMPLEMENTATION"},
    ]


def q8_code_matched_claim(repo: Path) -> dict[str, Any]:
    raw = blob(repo, BASELINE, Q8_SOURCE_PATH)
    lines = raw.decode("utf-8").splitlines(keepends=True)
    if len(lines) != Q8_SOURCE_CONTRACT["physical_lines"]:
        raise BuildError("Q8_FROZEN_SOURCE_LINE_COUNT")
    line = lines[Q8_SOURCE_CONTRACT["line_start"] - 1]
    observed = {
        "commit": BASELINE,
        "path": Q8_SOURCE_PATH,
        "git_blob": blob_id(repo, BASELINE, Q8_SOURCE_PATH),
        "raw_sha256": sha(raw),
        "bytes": len(raw),
        "physical_lines": len(lines),
        "line_start": 18,
        "line_end": 18,
        "slice_sha256": sha(line.encode("utf-8")),
    }
    if observed != Q8_SOURCE_CONTRACT:
        raise BuildError("Q8_FROZEN_SOURCE_CONTRACT")
    line_text = line.removesuffix("\n").removesuffix("\r")
    return {
        "claim_id": "P062-Q8-CODE-MATCHED-001",
        "topic": "Q8",
        "claim_class": "FROZEN_PROCESS_SELF_CLAIM",
        "claim_text": line_text,
        "blob": {
            "state": "FROZEN_GIT_OBJECT_AND_BOUNDED_SLICE",
            **observed,
            "line_text": line_text,
        },
        "ast": {
            "state": "STATIC_ENDPOINT_CORROBORATION_ONLY",
            "production_endpoint_ids": list(Q8_PRODUCTION_ENDPOINT_IDS),
            "test_endpoint_ids": list(Q8_TEST_ENDPOINT_IDS),
            "normalized_production_ast_identical": True,
            "claimed_changed_function_count": 0,
            "changed_function_count_independently_verified": False,
            "whole_semantic_equality_promoted": False,
            "reason": "the frozen ledger reports changed functions 0; static endpoint identity is corroboration, not proof of whole semantic equality",
        },
        "runtime": {
            "state": "INTERNAL_FRESH_RUNTIME_CORROBORATION_ONLY",
            "official_run_ids": list(Q8_OFFICIAL_RUN_IDS),
            "probe_ids": list(Q8_PROBE_IDS),
            "observed_behavior_delta_count": 0,
            "changed_function_count_independently_verified": False,
            "whole_runtime_equality_promoted": False,
            "reason": "official runs and the three-version probe are bounded internal observations and do not verify the ledger's whole code-matched proposition",
        },
        "authority": {
            "ceiling": "FROZEN_PROCESS_SELF_CLAIM_WITH_INTERNAL_STATIC_RUNTIME_CORROBORATION_ONLY",
            "source_is_self_claim": True,
            "changed_function_count_claim_promoted": False,
            "whole_semantic_runtime_equality": False,
            "external_science": False,
            "material": False,
            "experimental": False,
            "canonical_equation": False,
            "final_release": False,
        },
    }


def finding_rows() -> list[dict[str, Any]]:
    raw = [
        ("P1", "P062-CODE-FIND-001", "Q2 Q_j/n_j domain and uniqueness remain conditional"),
        ("P1", "P062-CODE-FIND-002", "G1 exit gate is tolerance based, not bit-exact enforcement"),
        ("P1", "P062-CODE-FIND-003", "v1.0.21 guide/test reproduction surfaces retain v1.0.20 names"),
        ("P1", "P062-CODE-FIND-004", "graph suite exit 0 does not enforce ALL PANELS FINITE"),
        ("P1", "P062-CODE-FIND-005", "exact Step54 Q6 worked arithmetic is not asserted"),
        ("P2", "P062-CODE-FIND-006", "v1.0.19 area check is printed but not exit-gated"),
        ("P2", "P062-CODE-FIND-007", "v1.0.21 G3 generated filename remains v1020_previb"),
        ("P2", "P062-CODE-FIND-008", "structure tool is UNTESTED_INPUT_SCOPE in Step55 runtime"),
        ("P2", "P062-CODE-FIND-009", "fresh runtime evidence is one Python/platform environment only"),
    ]
    return [{"finding_id": i, "severity": s, "status": "OPEN", "finding": text,
             "external_truth_promoted": False} for s, i, text in raw]


def build(repo: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    head = git(repo, ["rev-parse", "HEAD"], text=True).strip()
    if head != INPUT_COMMIT:
        raise BuildError(f"INPUT_COMMIT:{head}:{INPUT_COMMIT}")
    sources = [source_row(repo, p) for p in QUEUE]
    comparison_endpoints = comparison_endpoint_rows(repo, sources)
    statics = [static_row(repo, r) for r in sources if r["path"].endswith(".py")]
    prod = [r for r in statics if "/Anode_Fit_" in r["path"]]
    normalized_identical = len({r["version_normalized_ast_sha256"] for r in prod}) == 1
    runtime = collect_runtime(repo, sources)
    runtime["facts"]["normalized_ast_three_versions_identical"] = normalized_identical
    builder_hash = sha(lf(Path(__file__).read_bytes()))
    matrix = {
        "schema": "P062_STEP55_CODE_DELTA_MATRIX_V1", "input_commit": INPUT_COMMIT,
        "frozen_baseline": BASELINE, "builder_lf_sha256": builder_hash,
        "queue": sources, "queue_count": len(sources),
        "comparison_endpoints": comparison_endpoints, "comparison_endpoint_count": len(comparison_endpoints),
        "endpoint_dispositions": endpoint_disposition_rows(comparison_endpoints, statics, runtime),
        "endpoint_disposition_count": len(comparison_endpoints),
        "counterpart_matrix": counterpart_rows(comparison_endpoints), "counterpart_count": len(LOGICAL),
        "adjacent_comparisons": adjacent_comparison_rows(repo, comparison_endpoints),
        "adjacent_comparison_count": len(ADJACENT_SPECS),
        "static_python": statics, "static_python_count": len(statics),
        "patches": [patch_row(repo, QUEUE[0], QUEUE[5], "P062-PATCH-001"),
                    patch_row(repo, QUEUE[5], QUEUE[7], "P062-PATCH-002")],
        "production_normalized_ast_identical": normalized_identical,
        "claim_consumers": claim_rows(), "claim_consumer_count": 4,
        "code_matched_claims": [q8_code_matched_claim(repo)], "code_matched_claim_count": 1,
        "findings": finding_rows(), "finding_counts": {"P0": 0, "P1": 5, "P2": 4},
        "required_negative_controls": list(NEGATIVES), "required_negative_control_count": len(NEGATIVES),
        "result_first": {"sentinel": RESULT_SENTINEL, "write_order": ["result", "code_delta_matrix", "runtime_attestation"],
                         "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
        "authority": {"ast_is_runtime": False, "runtime_is_external_science": False,
                      "external_science": False, "material": False, "experimental": False,
                      "canonical_equation": False, "final_release": False},
        "gate": "PASS_WITH_CONCERNS",
    }
    return matrix, runtime


def render_result(matrix: dict[str, Any], runtime: dict[str, Any]) -> str:
    msha = sha(canonical_bytes(matrix)); rsha = sha(canonical_bytes(runtime))
    return f'''# Phase 062 Step 55 Code / Runtime Delta Result

Gate: `PASS_WITH_CONCERNS`

Terminal: `PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS`

Result-first sentinel: `{RESULT_SENTINEL}`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

## Frozen scope

- baseline: `{BASELINE}`
- input parent: `{INPUT_COMMIT}`
- source queue: `11/11`; comparison endpoints: `14/14`; endpoint four-axis dispositions: `14/14`; logical counterparts: `7/7`; adjacent comparisons: `7/7`
- matrix content SHA-256: `{msha}`
- runtime attestation content SHA-256: `{rsha}`

## Static and runtime findings

- production raw patches: `2/2`; all adjacent relations: `7/7` (`5` exact patches + `2` byte identities); normalized AST: `v1.0.19=v1.0.20=v1.0.21`
- runtime output ownership uses each command's before/after manifest union for NEW/MODIFIED/DELETED rows (observed deletions: `0`); consumed inputs and available materialized fixtures are separate fields.
- official fresh runtime: `5/5` exit 0 on Python `{RUNTIME_PYTHON}`
- independent three-version probe: `3/3`, behavior delta `0`
- regression: `13/13` bit-exact; fitting: `PASS`; graph finite: `15/15` (exit does not enforce this metric)
- v1.0.20/v1.0.21: `G1/G2/G3/n(T) PASS`; identical observed behavior
- claim consumers: Q2 `PARTIAL_WITH_DOMAIN_CONCERNS`; Q3 `PARTIAL_LAG_CONSUMER`; Q6 `GENERIC_LCO_IMPLEMENTATION_NO_EXACT_WORKED_ASSERTION`; Q7 `NOT_IMPLEMENTED`
- Q8 frozen `code matched` self-claim: `1/1`; exact ledger slice plus production/test endpoint and official-run/probe bindings; changed-function count and whole semantic/runtime equality are not independently promoted
- findings P0/P1/P2: `0/5/4`

## Controls and authority

- required singleton mutation controls: `{len(NEGATIVES)}/{len(NEGATIVES)}`
- validator contract includes full JSON semantic/shape pins, independent fresh runtime/probe reconstruction, result artifact hashes and ten disposable Git boundary fixtures.
- result chronology: result is emitted before both JSON outputs; this is a precommit sentinel and is not persistence evidence.
- AST is not promoted to runtime. Synthetic/internal runtime is not material, experimental, primary-literature or external scientific truth.
- external scientific/material/experimental/canonical/final-release flags: `false/false/false/false/false`

## Persistence boundary

Step 54 containing commit `{INPUT_COMMIT}` is the required parent and `PASS_P062_STEP54_PERSISTENCE` is the recovery prerequisite. Step 56 remains blocked until the exact-eight Step 55 commit is pushed and `PASS_P062_STEP55_PERSISTENCE` is verified.
'''


def output_paths(repo: Path, args: argparse.Namespace) -> tuple[Path, Path, Path]:
    return (Path(args.matrix) if args.matrix else repo / "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json",
            Path(args.attestation) if args.attestation else repo / "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json",
            Path(args.result) if args.result else repo / "Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--matrix")
    parser.add_argument("--attestation")
    parser.add_argument("--result")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    matrix_path, runtime_path, result_path = output_paths(repo, args)
    matrix, runtime = build(repo)
    result = render_result(matrix, runtime).encode("utf-8")
    outputs = ((result_path, result), (matrix_path, canonical_bytes(matrix)), (runtime_path, canonical_bytes(runtime)))
    if args.check:
        mismatch = [p.as_posix() for p, data in outputs if not p.is_file() or p.read_bytes() != data]
        if mismatch:
            raise BuildError("CHECK_MISMATCH:" + ",".join(mismatch))
        print("PASS_P062_STEP55_BUILDER_CHECK")
        return 0
    for path, data in outputs:  # result first is deliberate and machine-gated
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f"PASS_P062_STEP55_BUILD queue={len(matrix['queue'])} static={len(matrix['static_python'])} "
          f"runs={len(runtime['official_runs'])} behavior_delta={runtime['facts']['behavior_delta_count']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"FAIL_P062_STEP55_BUILD:{exc}")
        raise SystemExit(1)
