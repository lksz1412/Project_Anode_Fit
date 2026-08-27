#!/usr/bin/env python3
"""Independent fail-closed validator for Phase 062 Step 55."""
from __future__ import annotations

import argparse
import ast
import copy
import difflib
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Callable

REPO = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "ce069dde91f1332cc2852312cd2cbccd7cdf38db"
SUBJECT = "audit(phase062): compare v1021 code runtime"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = "origin/codex/anode-fit-v1025_2-canonical-completion"
PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
SENTINEL = "P062_STEP55_RESULT_FIRST_PRECOMMIT"
RUNTIME_PYTHON = "3.12.10"
RUNTIME_LABEL = "python-3.12.10"
BUILDER_LF_SHA256 = "1fdee23ac4d1a2d1d87a2ece28de07014f04c7bdf5d320ce0fae1b7463acdc1d"
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
CLAIM_CONSUMERS_SHA256 = "abed5a0e968e9f0459afb6473d0fd316c75b2993d36cf039e9accb78d3006173"
FINDINGS_SHA256 = "3ab7d74402979f218434f5cdccaef0e3182803a7ae59fe555843db6a0f462064"
MATRIX_GOLDEN_SHA256 = "ba0e6f7eee956294f0b38c2497c9f90b3976321718d262406e57d77853c058d4"
RUNTIME_GOLDEN_SHA256 = "7c6d8486ddf66749527cb4171932bbe737405e1d640657884859b1330e6edf77"
MATRIX_SHAPE_SHA256 = "8a4137f4ffc5c1b5a8655fb94e483d1b9ed7f192863b0a282f7810e0ac17ec9c"
RUNTIME_SHAPE_SHA256 = "2dad01ba41222112cbd61a38bc92a5c60fd39721a062c8cf2dfab6c6b4b7148c"
PROBE_STDOUT_SHA256 = "452b9b1969987e3e4befc59883047cd4884afcf38bfa65b1e767b4d1afd8726d"
RUNTIME_SCOPE_EXPECTED = {"implementation": "cpython", "matplotlib": "3.10.8", "numpy": "2.3.5",
                          "python": "3.12.10", "scipy": "1.17.1"}
MATRIX_TOP_KEYS = {"schema", "input_commit", "frozen_baseline", "builder_lf_sha256", "queue", "queue_count",
                   "comparison_endpoints", "comparison_endpoint_count", "endpoint_dispositions",
                   "endpoint_disposition_count", "counterpart_matrix", "counterpart_count", "adjacent_comparisons",
                   "adjacent_comparison_count", "static_python", "static_python_count", "patches",
                   "production_normalized_ast_identical", "claim_consumers", "claim_consumer_count",
                   "code_matched_claims", "code_matched_claim_count", "findings", "finding_counts",
                   "required_negative_controls", "required_negative_control_count", "result_first", "authority", "gate"}
RUNTIME_TOP_KEYS = {"schema", "input_commit", "frozen_baseline", "runtime_scope", "official_runs",
                    "independent_probe", "facts", "environment_dependent_fields_excluded", "cleanup", "authority"}
RUN_KEYS = {"run_id", "name", "runtime", "cwd", "argv", "timeout_seconds", "exit_code", "stdout_sha256",
            "stderr_sha256", "stdout_lines", "stderr_lines", "observations", "generated", "generated_output_count",
            "deleted_output_count", "available_fixture_source_ids", "consumed_input_source_ids", "consumed_input_evidence"}
OFFICIAL_RUN_META = (
    ("P062-RUN-001", "v1019_regression", "Claude/docs/v1.0.19", "test_regression_v1019.py"),
    ("P062-RUN-002", "v1019_fit_roundtrip", "Claude/docs/v1.0.19", "fit_roundtrip_demo.py"),
    ("P062-RUN-003", "v1019_graph_suite", "Claude/docs/v1.0.19", "graph_suite_v1019.py"),
    ("P062-RUN-004", "v1020_gates", "Claude/docs/v1.0.20", "test_gates_v1020.py"),
    ("P062-RUN-005", "v1021_gates", "Claude/docs/v1.0.21", "test_gates_v1021.py"),
)
EXPECTED_OBSERVATIONS = {
    "v1019_regression": {"regression_13_of_13_bit_exact": True, "fit_roundtrip_pass": None,
                          "graph_finite_15_of_15": None, "all_four_gates_pass": None},
    "v1019_fit_roundtrip": {"regression_13_of_13_bit_exact": None, "fit_roundtrip_pass": True,
                             "graph_finite_15_of_15": None, "all_four_gates_pass": None},
    "v1019_graph_suite": {"regression_13_of_13_bit_exact": None, "fit_roundtrip_pass": None,
                           "graph_finite_15_of_15": True, "all_four_gates_pass": None},
    "v1020_gates": {"regression_13_of_13_bit_exact": None, "fit_roundtrip_pass": None,
                     "graph_finite_15_of_15": None, "all_four_gates_pass": True},
    "v1021_gates": {"regression_13_of_13_bit_exact": None, "fit_roundtrip_pass": None,
                     "graph_finite_15_of_15": None, "all_four_gates_pass": True},
}

BUILDER = "Codex/work/v1021_phase062/build_phase062_step55_code_runtime_delta.py"
VALIDATOR = "Codex/work/v1021_phase062/validate_phase062_step55.py"
MATRIX = "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json"
ATTESTATION = "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json"
RESULT = "Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXACT_EIGHT = (BUILDER, VALIDATOR, MATRIX, ATTESTATION, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)

SOURCE_EXPECTED = (
    ("Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py", "115b2e60e79ef8e26f20960b8841b37cef55c415", "7de32d7bcd276687b2350b150559e00c1181dca953aba116760828b0bdff5193", 68896, 1151),
    ("Claude/docs/v1.0.19/fit_roundtrip_demo.py", "dd49eda5108c6cfb8cfb5a9f49a4cfdfbe8e8252", "20d10cd37f466b7a8b88ee84375cf80e515f7a12a0a9fe66648230696794293f", 19290, 368),
    ("Claude/docs/v1.0.19/graph_suite_v1019.py", "6344fb400d789715cf4cd80090802d21a9194659", "d688ddcf63973866c9bc6e8c73f9b49ae63eec4adb6d9e18a9b41d2ad5af546d", 8631, 150),
    ("Claude/docs/v1.0.19/test_regression_v1019.py", "c7eb9c4a742440ee5a45881e788b4e891eaf3bee", "8d1cbe5c15ec5b0813a6f15a82a7b2b40d3bea6bdcad0f0e7da66f210f1c5b3d", 5851, 127),
    ("Claude/docs/v1.0.19/golden_graphite_ref.npz", "8932d9dbfc165eeb39ec5cab23337d4582ba0ae8", "61b7f59b809417f46618039d1eecf5cc1aca9ed2d0202fcda7d909386c00d0c2", 107324, None),
    ("Claude/docs/v1.0.20/Anode_Fit_v1.0.20.py", "fce94465d04966df02d844d328c0b422081f80e9", "415bde6197d825685bac044aec9435eaa3b9148e0bab37c1eefe9b82430a635b", 69332, 1152),
    ("Claude/docs/v1.0.20/test_gates_v1020.py", "82155e9b0664b4dc50369326679e348727b2c906", "ecdee4458754d4de9f4820222c9a71ecf41f2bc5a59fa33741fab77d019d648a", 22050, 427),
    ("Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py", "7588fe782a027511c2407d9b7caea6ef0ca6c3bd", "d50612413f9f956486594ddafde37776f9592b75e2c8a2266927eaaa23267eaf", 69343, 1152),
    ("Claude/docs/v1.0.21/test_gates_v1021.py", "742506b061d872afdd094781ea2157faae800943", "a8de4944ea304b0106a7cfe0c495f2d7939f9cda74c2eae131fba55dd7e67d36", 22050, 427),
    ("Claude/docs/v1.0.21/results/tools_check_structure.py", "c929b7502f67e8799843744da729e15ee391a473", "7389bfce4c204e1d57801d84d43bb464c5bc918a9e9ad678f353f7880cd670b3", 8313, 165),
    ("Claude/docs/v1.0.21/FITTING_GUIDE.md", "f097793b69237d6f63705cc07708f8a1adbe7192", "f7ca9038e163cfba6313f85e0cd4f3095ac2890a9ff9eb6f8aa4a8cdf12409e1", 24415, 137),
)

COMPARISON_EXTRA_EXPECTED = (
    ("Claude/docs/v1.0.19/FITTING_GUIDE.md", "3a404573f6dc9eb296a7ef343421a450eac49232", "2f43e15747594403f54030d800a0179e7039384847a206a40d37a9f199b410be", 24026, 135),
    ("Claude/docs/v1.0.20/FITTING_GUIDE.md", "f097793b69237d6f63705cc07708f8a1adbe7192", "f7ca9038e163cfba6313f85e0cd4f3095ac2890a9ff9eb6f8aa4a8cdf12409e1", 24415, 137),
    ("Claude/docs/v1.0.20/results/tools_check_structure.py", "c929b7502f67e8799843744da729e15ee391a473", "7389bfce4c204e1d57801d84d43bb464c5bc918a9e9ad678f353f7880cd670b3", 8313, 165),
)

COMPARISON_PATHS = (
    SOURCE_EXPECTED[0][0], SOURCE_EXPECTED[5][0], SOURCE_EXPECTED[7][0],
    SOURCE_EXPECTED[3][0], SOURCE_EXPECTED[6][0], SOURCE_EXPECTED[8][0],
    SOURCE_EXPECTED[1][0], SOURCE_EXPECTED[2][0], SOURCE_EXPECTED[4][0],
    COMPARISON_EXTRA_EXPECTED[2][0], SOURCE_EXPECTED[9][0],
    COMPARISON_EXTRA_EXPECTED[0][0], COMPARISON_EXTRA_EXPECTED[1][0], SOURCE_EXPECTED[10][0],
)

LOGICAL_EXPECTED = (
    ("production_module", (SOURCE_EXPECTED[0][0], SOURCE_EXPECTED[5][0], SOURCE_EXPECTED[7][0])),
    ("official_gate", (SOURCE_EXPECTED[3][0], SOURCE_EXPECTED[6][0], SOURCE_EXPECTED[8][0])),
    ("fit_roundtrip", (SOURCE_EXPECTED[1][0], None, None)),
    ("graph_suite", (SOURCE_EXPECTED[2][0], None, None)),
    ("golden_npz", (SOURCE_EXPECTED[4][0], None, None)),
    ("structure_tool", (None, COMPARISON_EXTRA_EXPECTED[2][0], SOURCE_EXPECTED[9][0])),
    ("fitting_guide", (COMPARISON_EXTRA_EXPECTED[0][0], COMPARISON_EXTRA_EXPECTED[1][0], SOURCE_EXPECTED[10][0])),
)

ADJACENT_EXPECTED = (
    ("P062-ADJ-001", "production_module", "v1.0.19", SOURCE_EXPECTED[0][0], "v1.0.20", SOURCE_EXPECTED[5][0], "EXACT_PATCH", "HEADER_VERSION_PATH_ONLY"),
    ("P062-ADJ-002", "production_module", "v1.0.20", SOURCE_EXPECTED[5][0], "v1.0.21", SOURCE_EXPECTED[7][0], "EXACT_PATCH", "HEADER_VERSION_PATH_ONLY"),
    ("P062-ADJ-003", "official_gate", "v1.0.19", SOURCE_EXPECTED[3][0], "v1.0.20", SOURCE_EXPECTED[6][0], "EXACT_PATCH", "STATIC_TEXT_DELTA_UNADJUDICATED"),
    ("P062-ADJ-004", "official_gate", "v1.0.20", SOURCE_EXPECTED[6][0], "v1.0.21", SOURCE_EXPECTED[8][0], "EXACT_PATCH", "HEADER_VERSION_PATH_ONLY"),
    ("P062-ADJ-005", "structure_tool", "v1.0.20", COMPARISON_EXTRA_EXPECTED[2][0], "v1.0.21", SOURCE_EXPECTED[9][0], "BYTE_IDENTICAL", "BYTE_IDENTICAL"),
    ("P062-ADJ-006", "fitting_guide", "v1.0.19", COMPARISON_EXTRA_EXPECTED[0][0], "v1.0.20", COMPARISON_EXTRA_EXPECTED[1][0], "EXACT_PATCH", "STATIC_TEXT_DELTA_UNADJUDICATED"),
    ("P062-ADJ-007", "fitting_guide", "v1.0.20", COMPARISON_EXTRA_EXPECTED[1][0], "v1.0.21", SOURCE_EXPECTED[10][0], "BYTE_IDENTICAL", "BYTE_IDENTICAL"),
)

CONSUMED_EXPECTED = {
    "v1019_regression": ("P062-CODE-SRC-001", "P062-CODE-SRC-004", "P062-CODE-SRC-005"),
    "v1019_fit_roundtrip": ("P062-CODE-SRC-001", "P062-CODE-SRC-002"),
    "v1019_graph_suite": ("P062-CODE-SRC-001", "P062-CODE-SRC-003"),
    "v1020_gates": ("P062-CODE-SRC-001", "P062-CODE-SRC-005", "P062-CODE-SRC-006", "P062-CODE-SRC-007"),
    "v1021_gates": ("P062-CODE-SRC-001", "P062-CODE-SRC-005", "P062-CODE-SRC-008", "P062-CODE-SRC-009"),
}

CONSUMPTION_SPECS = {
    "v1019_regression": (
        ("P062-CODE-SRC-004", "EXECUTED_ENTRYPOINT", SOURCE_EXPECTED[3][0], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", SOURCE_EXPECTED[3][0], ((29, 37),)),
        ("P062-CODE-SRC-005", "NPZ_LOAD", SOURCE_EXPECTED[3][0], ((30, 30), (99, 99))),
    ),
    "v1019_fit_roundtrip": (
        ("P062-CODE-SRC-002", "EXECUTED_ENTRYPOINT", SOURCE_EXPECTED[1][0], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", SOURCE_EXPECTED[1][0], ((48, 52),)),
    ),
    "v1019_graph_suite": (
        ("P062-CODE-SRC-003", "EXECUTED_ENTRYPOINT", SOURCE_EXPECTED[2][0], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", SOURCE_EXPECTED[2][0], ((35, 38),)),
    ),
    "v1020_gates": (
        ("P062-CODE-SRC-007", "EXECUTED_ENTRYPOINT", SOURCE_EXPECTED[6][0], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", SOURCE_EXPECTED[6][0], ((37, 49), (411, 413))),
        ("P062-CODE-SRC-006", "DYNAMIC_IMPORT", SOURCE_EXPECTED[6][0], ((36, 49), (411, 413))),
        ("P062-CODE-SRC-005", "NPZ_LOAD", SOURCE_EXPECTED[6][0], ((38, 38), (151, 152))),
    ),
    "v1021_gates": (
        ("P062-CODE-SRC-009", "EXECUTED_ENTRYPOINT", SOURCE_EXPECTED[8][0], ((1, 1),)),
        ("P062-CODE-SRC-001", "DYNAMIC_IMPORT", SOURCE_EXPECTED[8][0], ((37, 49), (411, 413))),
        ("P062-CODE-SRC-008", "DYNAMIC_IMPORT", SOURCE_EXPECTED[8][0], ((36, 49), (411, 413))),
        ("P062-CODE-SRC-005", "NPZ_LOAD", SOURCE_EXPECTED[8][0], ((38, 38), (151, 152))),
    ),
}

ENDPOINT_RUNTIME_EXPECTED = {
    SOURCE_EXPECTED[0][0]: ("EXECUTED_IMPORTED_MODULE", ("P062-RUN-001", "P062-RUN-002", "P062-RUN-003", "P062-RUN-004", "P062-RUN-005"), "frozen module was dynamically imported by recorded official runs"),
    SOURCE_EXPECTED[5][0]: ("EXECUTED_IMPORTED_MODULE", ("P062-RUN-004",), "frozen module was dynamically imported by recorded official runs"),
    SOURCE_EXPECTED[7][0]: ("EXECUTED_IMPORTED_MODULE", ("P062-RUN-005",), "frozen module was dynamically imported by recorded official runs"),
    SOURCE_EXPECTED[3][0]: ("EXECUTED_ENTRYPOINT", ("P062-RUN-001",), "frozen script was the recorded official command entrypoint"),
    SOURCE_EXPECTED[6][0]: ("EXECUTED_ENTRYPOINT", ("P062-RUN-004",), "frozen script was the recorded official command entrypoint"),
    SOURCE_EXPECTED[8][0]: ("EXECUTED_ENTRYPOINT", ("P062-RUN-005",), "frozen script was the recorded official command entrypoint"),
    SOURCE_EXPECTED[1][0]: ("EXECUTED_ENTRYPOINT", ("P062-RUN-002",), "frozen script was the recorded official command entrypoint"),
    SOURCE_EXPECTED[2][0]: ("EXECUTED_ENTRYPOINT", ("P062-RUN-003",), "frozen script was the recorded official command entrypoint"),
    SOURCE_EXPECTED[4][0]: ("CONSUMED_DATA", ("P062-RUN-001", "P062-RUN-004", "P062-RUN-005"), "frozen NPZ was loaded by recorded official runs"),
    COMPARISON_EXTRA_EXPECTED[2][0]: ("NOT_MATERIALIZED_COMPARISON_ONLY", (), "historical comparison endpoint was read from Git but not materialized in the 11-source runtime fixture"),
    SOURCE_EXPECTED[9][0]: ("NOT_EXECUTED_AVAILABLE_FIXTURE", (), "materialized in the 11-source runtime fixture but not consumed by any official run"),
    COMPARISON_EXTRA_EXPECTED[0][0]: ("NOT_MATERIALIZED_COMPARISON_ONLY", (), "historical comparison endpoint was read from Git but not materialized in the 11-source runtime fixture"),
    COMPARISON_EXTRA_EXPECTED[1][0]: ("NOT_MATERIALIZED_COMPARISON_ONLY", (), "historical comparison endpoint was read from Git but not materialized in the 11-source runtime fixture"),
    SOURCE_EXPECTED[10][0]: ("NOT_EXECUTED_AVAILABLE_FIXTURE", (), "materialized in the 11-source runtime fixture but not consumed by any official run"),
}

AST_STATES = {"DIRECT_AST_PROJECTION", "BYTE_IDENTICAL_AST_INHERITANCE", "N_A_NON_PYTHON"}
RUNTIME_STATES = {"EXECUTED_ENTRYPOINT", "EXECUTED_IMPORTED_MODULE", "CONSUMED_DATA",
                  "NOT_EXECUTED_AVAILABLE_FIXTURE", "NOT_MATERIALIZED_COMPARISON_ONLY"}

NEGATIVES = (
    "VERSION_ONLY_TO_BEHAVIOR_DELTA", "TOLERANCE_TO_BIT_EXACT", "AST_TO_RUNTIME_PROMOTION",
    "GRAPH_EXIT0_TO_METRIC_PASS", "NEGATIVE_Q_UNIQUENESS", "NONPOSITIVE_N_UNIQUENESS",
    "INVENTED_Q3_QRATIO", "INVENTED_Q3_KAPPA", "ABSENT_Q6_EXACT_ASSERTION",
    "Q7_BRIDGEHEAD_TO_IMPLEMENTATION", "FROZEN_MODULE_IMPORT", "RUNTIME_TIMEOUT_MISSING",
    "EOL_ONLY_BEHAVIOR_DELTA", "PATH_ONLY_BEHAVIOR_DELTA", "SYNTHETIC_TO_MATERIAL_TRUTH",
    "NULLABLE_COUNTERPART_FABRICATION", "GATE_SELF_CONFIRMATION", "UNTESTED_STRUCTURE_PROMOTION",
    "DUPLICATE_JSON_KEY", "NONFINITE_JSON", "QUEUE_BLOB_MISMATCH", "QUEUE_ORPHAN",
    "COUNTERPART_REASON_MISSING", "RUNTIME_EXIT_TAMPER", "RUNTIME_STDOUT_HASH_TAMPER",
    "PROBE_BEHAVIOR_DELTA_TAMPER", "EXTERNAL_TRUTH_PROMOTION", "RESULT_FIRST_SENTINEL_MISSING",
    "EXTRA_DIRTY_PATH", "STAGED_WORKTREE_MISMATCH", "ACTIVE_REMOTE_DIVERGENCE",
    "PROTECTED_DRIFT", "MAIN_DRIFT", "CLAUDE_DRIFT", "PERSISTENCE_PARENT_MISMATCH",
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


class ValidationError(RuntimeError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def schema_shape(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: schema_shape(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [schema_shape(item) for item in value]
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    return type(value).__name__


def semantic_sha(value: Any) -> str:
    return sha(canonical(value))


def shape_sha(value: Any) -> str:
    return semantic_sha(schema_shape(value))


def strict_load_bytes(data: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                raise ValidationError("DUPLICATE_JSON_KEY")
            out[key] = value
        return out
    def reject(value: str) -> None:
        raise ValidationError(f"NONFINITE_JSON:{value}")
    def finite_float(value: str) -> float:
        result = float(value)
        if not math.isfinite(result):
            raise ValidationError("NONFINITE_JSON:overflow")
        return result
    try:
        result = json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                            parse_constant=reject, parse_float=finite_float)
    except UnicodeDecodeError as exc:
        raise ValidationError("JSON_NOT_UTF8") from exc
    stack = [result]
    while stack:
        value = stack.pop()
        if isinstance(value, float) and not math.isfinite(value):
            raise ValidationError("NONFINITE_JSON:recursive")
        if isinstance(value, dict):
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    return result


def strict_load(path: str) -> Any:
    target = REPO / path
    if not target.is_file():
        raise ValidationError(f"MISSING:{path}")
    return strict_load_bytes(target.read_bytes())


def proc(cmd: list[str], *, cwd: Path = REPO, timeout: int = 60,
         env: dict[str, str] | None = None, text: bool = False) -> subprocess.CompletedProcess[Any]:
    try:
        return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, check=False, timeout=timeout,
                              text=text, encoding="utf-8" if text else None,
                              errors="replace" if text else None)
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"SUBPROCESS_TIMEOUT:{cmd[0]}:{timeout}") from exc


def git(args: list[str], *, text: bool = True, timeout: int = 45) -> Any:
    return git_at(REPO, args, text=text, timeout=timeout)


def git_at(repo: Path, args: list[str], *, text: bool = True, timeout: int = 45,
           check: bool = True) -> Any:
    cp = proc(["git", *args], cwd=repo, timeout=timeout, text=text)
    if cp.returncode:
        err = cp.stderr if text else cp.stderr.decode("utf-8", "replace")
        if not check:
            return cp
        raise ValidationError(f"GIT_ERROR:{args[0]}:{cp.returncode}:{err.strip()}")
    return cp.stdout


def blob(path: str) -> bytes:
    return git(["show", f"{BASELINE}:{path}"], text=False)


def blob_id(path: str) -> str:
    return git(["rev-parse", f"{BASELINE}:{path}"]).strip()


class VersionNormalizer(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, str):
            value = re.sub(r"v1\.0\.(?:19|20|21)", "v1.0.X", node.value, flags=re.I)
            value = re.sub(r"v10(?:19|20|21)", "v10XX", value, flags=re.I)
            value = re.sub(r"2026-07-(?:13|14)", "2026-07-XX", value)
            return ast.copy_location(ast.Constant(value=value), node)
        return node


def canonical_ast_value(value: Any) -> Any:
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


def ast_digest(node: ast.AST) -> str:
    return sha(json.dumps(canonical_ast_value(node), ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8"))


def independent_source_rows() -> list[dict[str, Any]]:
    rows = []
    for i, (path, expected_blob, expected_sha, expected_bytes, expected_lines) in enumerate(SOURCE_EXPECTED, 1):
        raw = blob(path)
        if (blob_id(path), sha(raw), len(raw)) != (expected_blob, expected_sha, expected_bytes):
            raise ValidationError(f"FROZEN_SOURCE_IDENTITY:{path}")
        binary = path.endswith(".npz")
        row: dict[str, Any] = {"source_id": f"P062-CODE-SRC-{i:03d}", "path": path,
            "commit": BASELINE, "git_blob": expected_blob, "raw_sha256": expected_sha,
            "bytes": expected_bytes, "binary": binary,
            "traversal": "BINARY_FULL" if binary else "READ_FULL"}
        if not binary:
            text = raw.decode("utf-8")
            if len(text.splitlines()) != expected_lines:
                raise ValidationError(f"FROZEN_LINE_COUNT:{path}")
            row.update({"encoding": "utf-8", "physical_lines": expected_lines,
                        "nonblank_lines": sum(bool(x.strip()) for x in text.splitlines()),
                        "lf_sha256": sha(lf(raw))})
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
        rows.append(row)
    return rows


def comparison_endpoint_contract() -> list[dict[str, Any]]:
    expected = {row[0]: row for row in SOURCE_EXPECTED + COMPARISON_EXTRA_EXPECTED}
    queue_ids = {row[0]: f"P062-CODE-SRC-{i:03d}" for i, row in enumerate(SOURCE_EXPECTED, 1)}
    rows = []
    for i, path in enumerate(COMPARISON_PATHS, 1):
        _, expected_blob, expected_sha, expected_bytes, expected_lines = expected[path]
        binary = path.endswith(".npz")
        rows.append({
            "comparison_endpoint_id": f"P062-CMP-END-{i:03d}",
            "path": path,
            "commit": BASELINE,
            "git_blob": expected_blob,
            "raw_sha256": expected_sha,
            "bytes": expected_bytes,
            "binary": binary,
            "physical_lines": expected_lines,
            "queue_source_id": queue_ids.get(path),
            "authority": "FROZEN_GIT_OBJECT_IDENTITY_ONLY",
        })
    return rows


def independent_comparison_endpoints() -> list[dict[str, Any]]:
    rows = comparison_endpoint_contract()
    for row in rows:
        path = row["path"]
        raw = blob(path)
        if (blob_id(path), sha(raw), len(raw)) != (row["git_blob"], row["raw_sha256"], row["bytes"]):
            raise ValidationError(f"COMPARISON_ENDPOINT_IDENTITY:{path}")
        if not row["binary"] and len(raw.decode("utf-8").splitlines()) != row["physical_lines"]:
            raise ValidationError(f"COMPARISON_ENDPOINT_LINES:{path}")
    return rows


def independent_counterparts(endpoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_path = {row["path"]: row for row in endpoints}
    rows = []
    for i, (logical_asset, paths) in enumerate(LOGICAL_EXPECTED, 1):
        versions = {}
        for version, path in zip(("v1.0.19", "v1.0.20", "v1.0.21"), paths):
            if path is None:
                versions[version] = {
                    "comparison_endpoint_id": None,
                    "queue_source_id": None,
                    "path": None,
                    "null_reason": f"NO_{logical_asset.upper()}_OCCURRENCE_IN_{version.replace('.', '')}",
                }
            else:
                endpoint = by_path[path]
                versions[version] = {
                    "comparison_endpoint_id": endpoint["comparison_endpoint_id"],
                    "queue_source_id": endpoint["queue_source_id"],
                    "path": path,
                }
        rows.append({
            "counterpart_id": f"P062-COUNTERPART-{i:03d}",
            "logical_asset": logical_asset,
            "identity_basis": "logical role plus exact versioned path; never basename",
            "versions": versions,
        })
    return rows


def independent_adjacent_comparisons(endpoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    endpoint_id = {row["path"]: row["comparison_endpoint_id"] for row in endpoints}
    rows = []
    for ident, logical, from_version, left, to_version, right, relation, classification in ADJACENT_EXPECTED:
        a_raw, b_raw = blob(left), blob(right)
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
                raise ValidationError(f"ADJACENT_EXPECTED_IDENTITY:{ident}")
            row.update({"byte_identity": True, "shared_raw_sha256": sha(a_raw), "bytes": len(a_raw)})
        else:
            a, b = a_raw.decode("utf-8").splitlines(), b_raw.decode("utf-8").splitlines()
            diff = list(difflib.unified_diff(a, b, fromfile=left, tofile=right, lineterm=""))
            if not diff:
                raise ValidationError(f"ADJACENT_EXPECTED_PATCH:{ident}")
            row.update({
                "unified_diff": diff,
                "diff_sha256": sha(("\n".join(diff) + "\n").encode()),
                "added_lines": sum(x.startswith("+") and not x.startswith("+++") for x in diff),
                "deleted_lines": sum(x.startswith("-") and not x.startswith("---") for x in diff),
            })
        rows.append(row)
    return rows


def ast_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{ast_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return ast_name(node.func)
    return type(node).__name__


def signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    args = node.args
    return {
        "posonly": [x.arg for x in args.posonlyargs], "args": [x.arg for x in args.args],
        "vararg": args.vararg.arg if args.vararg else None,
        "kwonly": [x.arg for x in args.kwonlyargs], "kwarg": args.kwarg.arg if args.kwarg else None,
        "defaults_sha256": sha(canonical([canonical_ast_value(x) for x in args.defaults])),
        "kw_defaults_sha256": sha(canonical([canonical_ast_value(x) if x else None for x in args.kw_defaults])),
    }


def independent_static_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for source in sources:
        path = source["path"]
        if not path.endswith(".py"):
            continue
        raw = blob(path)
        tree = ast.parse(raw.decode("utf-8"), filename=path)
        normalized = VersionNormalizer().visit(ast.parse(raw.decode("utf-8"), filename=path))
        ast.fix_missing_locations(normalized)
        symbols = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                symbols.append({"kind": "function", "name": node.name, "line": node.lineno,
                                "signature": signature(node),
                                "body_sha256": ast_digest(ast.Module(body=node.body, type_ignores=[]))})
            elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                methods = []
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and not child.name.startswith("_"):
                        methods.append({"name": child.name, "line": child.lineno, "signature": signature(child),
                                        "body_sha256": ast_digest(ast.Module(body=child.body, type_ignores=[]))})
                symbols.append({"kind": "class", "name": node.name, "line": node.lineno,
                                "body_sha256": ast_digest(node), "public_methods": methods})
        imports, globals_ = [], []
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append({"line": node.lineno, "ast_sha256": ast_digest(node)})
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        globals_.append({"name": target.id, "line": node.lineno,
                                         "value_sha256": ast_digest(node.value) if node.value else None})
        calls = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Call)),
                       key=lambda x: (x.lineno, x.col_offset))
        assertions = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Assert)),
                            key=lambda x: (x.lineno, x.col_offset))
        text = raw.decode("utf-8")
        units = sorted(set(re.findall(r"(?:J/mol(?:/K)?|kJ/mol|mV/K|mV|uV/K|µV/K|V/K|V|K|W|mAh/g|GPa|nm|%)", text)))
        rows.append({"source_id": source["source_id"], "path": path,
                     "raw_ast_sha256": ast_digest(tree),
                     "version_normalized_ast_sha256": ast_digest(normalized),
                     "public_symbols": symbols, "imports": imports, "globals": globals_,
                     "call_order": [{"line": n.lineno, "column": n.col_offset, "callee": ast_name(n.func),
                                    "call_sha256": ast_digest(n)} for n in calls],
                     "assertions": [{"line": n.lineno, "test_sha256": ast_digest(n.test)} for n in assertions],
                     "unit_tokens": units, "authority": "STATIC_STRUCTURE_ONLY_NO_RUNTIME_PROMOTION"})
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


def expected_endpoint_dispositions(endpoints: list[dict[str, Any]],
                                   static_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    static_by_path = {row["path"]: row for row in static_rows}
    endpoint_by_path = {row["path"]: row for row in endpoints}
    inherited_path = COMPARISON_EXTRA_EXPECTED[2][0]
    inherited_basis = endpoint_by_path[SOURCE_EXPECTED[9][0]]
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
            basis_static = static_by_path[SOURCE_EXPECTED[9][0]]
            if endpoint["raw_sha256"] != inherited_basis["raw_sha256"]:
                raise ValidationError("ENDPOINT_AST_INHERITANCE_RAW_MISMATCH")
            ast_row = {"state": "BYTE_IDENTICAL_AST_INHERITANCE", "digest": basis_static["raw_ast_sha256"],
                       "digest_kind": "CANONICAL_EXPLICIT_FIELD_AST_SHA256",
                       "source_static_source_id": basis_static["source_id"],
                       "basis_endpoint_id": inherited_basis["comparison_endpoint_id"], "n_a_reason": None}
        else:
            reason = "binary NPZ has no Python AST" if path.endswith(".npz") else "Markdown guide has no Python AST"
            ast_row = {"state": "N_A_NON_PYTHON", "digest": None, "digest_kind": None,
                       "source_static_source_id": None, "basis_endpoint_id": None, "n_a_reason": reason}
        runtime_state, run_ids, reason = ENDPOINT_RUNTIME_EXPECTED[path]
        runtime_row = {"state": runtime_state, "run_ids": list(run_ids), "reason": reason}
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


def independent_patches() -> list[dict[str, Any]]:
    pairs = ((SOURCE_EXPECTED[0][0], SOURCE_EXPECTED[5][0], "P062-PATCH-001"),
             (SOURCE_EXPECTED[5][0], SOURCE_EXPECTED[7][0], "P062-PATCH-002"))
    rows = []
    for left, right, ident in pairs:
        a, b = blob(left).decode("utf-8").splitlines(), blob(right).decode("utf-8").splitlines()
        diff = list(difflib.unified_diff(a, b, fromfile=left, tofile=right, lineterm=""))
        rows.append({"patch_id": ident, "from_path": left, "to_path": right, "unified_diff": diff,
                     "diff_sha256": sha(("\n".join(diff) + "\n").encode()),
                     "added_lines": sum(x.startswith("+") and not x.startswith("+++") for x in diff),
                     "deleted_lines": sum(x.startswith("-") and not x.startswith("---") for x in diff),
                     "classification": "HEADER_VERSION_PATH_ONLY"})
    return rows


def builder_ast_policy() -> list[str]:
    raw = (REPO / BUILDER).read_bytes()
    if sha(lf(raw)) != BUILDER_LF_SHA256:
        return ["BUILDER_HASH"]
    tree = ast.parse(raw.decode("utf-8"))
    codes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            codes.append("BUILDER_AST_POLICY")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if any(alias.name.startswith(("Claude", "importlib")) for alias in node.names):
                codes.append("BUILDER_AST_POLICY")
        if isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
            if name in {"eval", "exec", "compile", "__import__", "getoutput", "getstatusoutput"}:
                codes.append("BUILDER_AST_POLICY")
    return sorted(set(codes))


def claim_map(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x.get("claim_id", ""): x for x in matrix.get("claim_consumers", [])}


def independent_q8_code_matched_claim() -> dict[str, Any]:
    raw = blob(Q8_SOURCE_PATH)
    lines = raw.decode("utf-8").splitlines(keepends=True)
    if len(lines) != Q8_SOURCE_CONTRACT["physical_lines"]:
        raise ValidationError("Q8_FROZEN_SOURCE_LINE_COUNT")
    line = lines[Q8_SOURCE_CONTRACT["line_start"] - 1]
    observed = {
        "commit": BASELINE,
        "path": Q8_SOURCE_PATH,
        "git_blob": blob_id(Q8_SOURCE_PATH),
        "raw_sha256": sha(raw),
        "bytes": len(raw),
        "physical_lines": len(lines),
        "line_start": 18,
        "line_end": 18,
        "slice_sha256": sha(line.encode("utf-8")),
    }
    if observed != Q8_SOURCE_CONTRACT:
        raise ValidationError("Q8_FROZEN_SOURCE_CONTRACT")
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


def q8_code_matched_diagnostics(matrix: dict[str, Any], runtime: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    rows = matrix.get("code_matched_claims", [])
    if not isinstance(rows, list) or not rows:
        return {"Q8_CODE_MATCHED_CLAIM_MISSING"}
    if len(rows) != 1:
        return {"Q8_CODE_MATCHED_CLAIM_DUPLICATE"}
    if matrix.get("code_matched_claim_count") != 1:
        return {"Q8_CODE_MATCHED_CLAIM_MISSING"}
    row = rows[0]
    expected = independent_q8_code_matched_claim()
    row_keys = {"claim_id", "topic", "claim_class", "claim_text", "blob", "ast", "runtime", "authority"}
    blob_keys = {"state", "commit", "path", "git_blob", "raw_sha256", "bytes", "physical_lines",
                 "line_start", "line_end", "slice_sha256", "line_text"}
    ast_keys = {"state", "production_endpoint_ids", "test_endpoint_ids", "normalized_production_ast_identical",
                "claimed_changed_function_count", "changed_function_count_independently_verified",
                "whole_semantic_equality_promoted", "reason"}
    runtime_keys = {"state", "official_run_ids", "probe_ids", "observed_behavior_delta_count",
                    "changed_function_count_independently_verified", "whole_runtime_equality_promoted", "reason"}
    authority_keys = {"ceiling", "source_is_self_claim", "changed_function_count_claim_promoted",
                      "whole_semantic_runtime_equality", "external_science", "material", "experimental",
                      "canonical_equation", "final_release"}
    if not isinstance(row, dict) or set(row) != row_keys or not isinstance(row.get("blob"), dict) or \
            set(row["blob"]) != blob_keys or not isinstance(row.get("ast"), dict) or set(row["ast"]) != ast_keys or \
            not isinstance(row.get("runtime"), dict) or set(row["runtime"]) != runtime_keys or \
            not isinstance(row.get("authority"), dict) or set(row["authority"]) != authority_keys:
        return {"Q8_CODE_MATCHED_FOUR_AXIS_SCHEMA"}
    if any(row.get(key) != expected[key] for key in ("claim_id", "topic", "claim_class")):
        out.add("Q8_CODE_MATCHED_FOUR_AXIS_SCHEMA")
    if row.get("claim_text") != expected["claim_text"] or row["blob"] != expected["blob"]:
        out.add("Q8_CODE_MATCHED_SOURCE_MUTATION")
    ast_other = {key: value for key, value in row["ast"].items()
                 if key not in {"production_endpoint_ids", "test_endpoint_ids"}}
    expected_ast_other = {key: value for key, value in expected["ast"].items()
                          if key not in {"production_endpoint_ids", "test_endpoint_ids"}}
    endpoint_ids = {item.get("comparison_endpoint_id") for item in matrix.get("comparison_endpoints", [])}
    if row["ast"].get("production_endpoint_ids") != list(Q8_PRODUCTION_ENDPOINT_IDS) or \
            row["ast"].get("test_endpoint_ids") != list(Q8_TEST_ENDPOINT_IDS) or \
            not set(Q8_PRODUCTION_ENDPOINT_IDS + Q8_TEST_ENDPOINT_IDS).issubset(endpoint_ids):
        out.add("Q8_CODE_MATCHED_ENDPOINT_BINDING")
    if ast_other != expected_ast_other:
        out.add("Q8_CODE_MATCHED_FOUR_AXIS_SCHEMA")
    runtime_other = {key: value for key, value in row["runtime"].items()
                     if key not in {"official_run_ids", "probe_ids"}}
    expected_runtime_other = {key: value for key, value in expected["runtime"].items()
                              if key not in {"official_run_ids", "probe_ids"}}
    run_ids = {item.get("run_id") for item in runtime.get("official_runs", [])}
    probe_id = runtime.get("independent_probe", {}).get("probe_id")
    if row["runtime"].get("official_run_ids") != list(Q8_OFFICIAL_RUN_IDS) or \
            row["runtime"].get("probe_ids") != list(Q8_PROBE_IDS) or \
            not set(Q8_OFFICIAL_RUN_IDS).issubset(run_ids) or probe_id not in Q8_PROBE_IDS:
        out.add("Q8_CODE_MATCHED_RUNTIME_BINDING")
    if runtime_other != expected_runtime_other:
        out.add("Q8_CODE_MATCHED_FOUR_AXIS_SCHEMA")
    if row["authority"] != expected["authority"]:
        out.add("Q8_CODE_MATCHED_AUTHORITY_PROMOTION")
    return out


def independent_consumed_input_evidence(name: str) -> list[dict[str, Any]]:
    source_paths = {f"P062-CODE-SRC-{i:03d}": row[0] for i, row in enumerate(SOURCE_EXPECTED, 1)}
    rows = []
    for source_id, relationship, consumer_path, ranges in CONSUMPTION_SPECS[name]:
        lines = blob(consumer_path).decode("utf-8").splitlines()
        anchors = []
        for start, end in ranges:
            if start < 1 or end > len(lines) or start > end:
                raise ValidationError(f"CONSUMPTION_ANCHOR_RANGE:{name}:{consumer_path}:{start}:{end}")
            payload = ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")
            anchors.append({"line_start": start, "line_end": end, "slice_sha256": sha(payload)})
        rows.append({"source_id": source_id, "source_path": source_paths[source_id],
                     "relationship": relationship, "consumer_path": consumer_path, "anchors": anchors})
    return rows


def endpoint_disposition_diagnostics(matrix: dict[str, Any], runtime: dict[str, Any], *, deep: bool) -> set[str]:
    out: set[str] = set()
    endpoints = matrix.get("comparison_endpoints", [])
    static_rows = matrix.get("static_python", [])
    rows = matrix.get("endpoint_dispositions", [])
    if matrix.get("endpoint_disposition_count") != 14:
        out.add("ENDPOINT_DISPOSITION_MISSING")
    endpoint_ids = [row.get("comparison_endpoint_id") for row in endpoints]
    actual_ids = [row.get("comparison_endpoint_id") for row in rows]
    missing = set(endpoint_ids) - set(actual_ids)
    duplicates = {item for item in actual_ids if actual_ids.count(item) > 1}
    orphans = set(actual_ids) - set(endpoint_ids)
    if missing:
        out.add("ENDPOINT_DISPOSITION_MISSING")
    if duplicates:
        out.add("ENDPOINT_DISPOSITION_DUPLICATE")
    if orphans:
        out.add("ENDPOINT_DISPOSITION_ORPHAN")
    if missing or duplicates:
        return out
    expected_rows = expected_endpoint_dispositions(endpoints, static_rows)
    expected_by_id = {row["comparison_endpoint_id"]: row for row in expected_rows}
    actual_by_id = {row["comparison_endpoint_id"]: row for row in rows if row.get("comparison_endpoint_id") in expected_by_id}
    row_keys = {"disposition_id", "comparison_endpoint_id", "path", "blob", "ast", "runtime", "authority"}
    blob_keys = {"state", "commit", "git_blob", "raw_sha256", "bytes"}
    ast_keys = {"state", "digest", "digest_kind", "source_static_source_id", "basis_endpoint_id", "n_a_reason"}
    runtime_keys = {"state", "run_ids", "reason"}
    authority_keys = {"ceiling", "external_science", "material", "experimental", "canonical_equation", "final_release"}
    for endpoint_id, expected in expected_by_id.items():
        row = actual_by_id.get(endpoint_id)
        if row is None:
            continue
        if set(row) != row_keys or not isinstance(row.get("blob"), dict) or set(row["blob"]) != blob_keys or \
                not isinstance(row.get("ast"), dict) or set(row["ast"]) != ast_keys or \
                not isinstance(row.get("runtime"), dict) or set(row["runtime"]) != runtime_keys or \
                not isinstance(row.get("authority"), dict) or set(row["authority"]) != authority_keys or \
                row.get("disposition_id") != expected["disposition_id"] or row.get("path") != expected["path"]:
            out.add("ENDPOINT_DISPOSITION_SCHEMA")
            continue
        if row["blob"] != expected["blob"]:
            out.add("ENDPOINT_BLOB_BINDING_MISMATCH")
        ast_row, expected_ast = row["ast"], expected["ast"]
        if ast_row.get("state") not in AST_STATES:
            out.add("ENDPOINT_AST_STATE_INVALID")
        elif ast_row["state"] == "N_A_NON_PYTHON":
            if ast_row.get("n_a_reason") != expected_ast["n_a_reason"] or not ast_row.get("n_a_reason"):
                out.add("ENDPOINT_AST_NA_REASON_MISSING")
            if any(ast_row.get(key) is not None for key in
                   ("digest", "digest_kind", "source_static_source_id", "basis_endpoint_id")):
                out.add("ENDPOINT_AST_DIGEST_BINDING_MISMATCH")
        else:
            if any(ast_row.get(key) != expected_ast[key] for key in
                   ("digest", "digest_kind", "source_static_source_id", "n_a_reason")):
                out.add("ENDPOINT_AST_DIGEST_BINDING_MISMATCH")
            if ast_row.get("basis_endpoint_id") != expected_ast["basis_endpoint_id"]:
                out.add("ENDPOINT_AST_INHERITANCE_BASIS_MISMATCH")
        runtime_row, expected_runtime = row["runtime"], expected["runtime"]
        if runtime_row.get("state") not in RUNTIME_STATES or runtime_row.get("state") != expected_runtime["state"] or \
                runtime_row.get("run_ids") != expected_runtime["run_ids"]:
            out.add("ENDPOINT_RUNTIME_STATE_MISMATCH")
        elif runtime_row.get("reason") != expected_runtime["reason"] or not runtime_row.get("reason"):
            out.add("ENDPOINT_RUNTIME_REASON_MISSING")
        if row["authority"] != expected["authority"]:
            out.add("ENDPOINT_AUTHORITY_PROMOTION")
    if deep and not (missing or duplicates or orphans):
        independent_endpoints = independent_comparison_endpoints()
        independent_static = independent_static_rows(independent_source_rows())
        if rows != expected_endpoint_dispositions(independent_endpoints, independent_static):
            # Field-specific diagnostics above are authoritative; this guards an unclassified projection drift.
            if not out:
                out.add("ENDPOINT_DISPOSITION_SCHEMA")
        runs_by_source: dict[str, list[tuple[str, str]]] = {}
        for run in runtime.get("official_runs", []):
            evidence = {item["source_id"]: item["relationship"] for item in run.get("consumed_input_evidence", [])}
            for source_id in run.get("consumed_input_source_ids", []):
                runs_by_source.setdefault(source_id, []).append((run["run_id"], evidence.get(source_id, "")))
        for endpoint, expected in zip(independent_endpoints, expected_rows):
            source_id = endpoint["queue_source_id"]
            observed = runs_by_source.get(source_id, []) if source_id else []
            expected_runtime = expected["runtime"]
            if [run_id for run_id, _ in observed] != expected_runtime["run_ids"]:
                out.add("ENDPOINT_RUNTIME_STATE_MISMATCH")
            relationships = {relationship for _, relationship in observed}
            state = expected_runtime["state"]
            relation_state = {"EXECUTED_ENTRYPOINT": {"EXECUTED_ENTRYPOINT"},
                              "EXECUTED_IMPORTED_MODULE": {"DYNAMIC_IMPORT"},
                              "CONSUMED_DATA": {"NPZ_LOAD"}}
            if state in relation_state and relationships != relation_state[state]:
                out.add("ENDPOINT_RUNTIME_STATE_MISMATCH")
            if state.startswith("NOT_") and observed:
                out.add("ENDPOINT_RUNTIME_STATE_MISMATCH")
    return out


def content_diagnostics(matrix: dict[str, Any], runtime: dict[str, Any], *, deep: bool) -> set[str]:
    out: set[str] = set()
    matrix_schema_mismatch = set(matrix) != MATRIX_TOP_KEYS
    runtime_schema_mismatch = set(runtime) != RUNTIME_TOP_KEYS
    declared_count_mismatch = any((
        matrix.get("queue_count") != 11,
        matrix.get("comparison_endpoint_count") != 14,
        matrix.get("endpoint_disposition_count") != 14,
        matrix.get("counterpart_count") != 7,
        matrix.get("adjacent_comparison_count") != 7,
        matrix.get("static_python_count") != 9,
        matrix.get("claim_consumer_count") != 4,
        matrix.get("code_matched_claim_count") != 1,
        matrix.get("required_negative_control_count") != len(NEGATIVES),
    ))
    claim_projection_mismatch = semantic_sha(matrix.get("claim_consumers")) != CLAIM_CONSUMERS_SHA256
    finding_projection_mismatch = semantic_sha(matrix.get("findings")) != FINDINGS_SHA256
    if matrix.get("schema") != "P062_STEP55_CODE_DELTA_MATRIX_V1" or matrix.get("input_commit") != PARENT or matrix.get("frozen_baseline") != BASELINE:
        out.add("MATRIX_HEADER")
    if runtime.get("schema") != "P062_STEP55_RUNTIME_ATTESTATION_V1" or runtime.get("input_commit") != PARENT or runtime.get("frozen_baseline") != BASELINE:
        out.add("RUNTIME_HEADER")
    if matrix.get("builder_lf_sha256") != BUILDER_LF_SHA256:
        out.add("BUILDER_HASH")
    if matrix.get("gate") != "PASS_WITH_CONCERNS":
        out.add("MATRIX_GATE_TAMPER")
    queue = matrix.get("queue", [])
    if len(queue) != 11 or matrix.get("queue_count") != 11:
        out.add("QUEUE_ORPHAN")
    else:
        for row, expected in zip(queue, SOURCE_EXPECTED):
            path, expected_blob, expected_sha, expected_bytes, _ = expected
            if (row.get("path"), row.get("git_blob"), row.get("raw_sha256"), row.get("bytes")) != (
                    path, expected_blob, expected_sha, expected_bytes):
                out.add("QUEUE_BLOB_MISMATCH")
        if deep and queue != independent_source_rows():
            out.add("QUEUE_BLOB_MISMATCH")
    cps = matrix.get("counterpart_matrix", [])
    if len(cps) != 7 or matrix.get("counterpart_count") != 7:
        out.add("COUNTERPART_REASON_MISSING")
    else:
        for row in cps:
            if row.get("identity_basis") != "logical role plus exact versioned path; never basename":
                out.add("NULLABLE_COUNTERPART_FABRICATION")
            for endpoint in row.get("versions", {}).values():
                if endpoint.get("path") is None and not endpoint.get("null_reason"):
                    out.add("COUNTERPART_REASON_MISSING")
                if endpoint.get("path") is None and any(endpoint.get(key) is not None for key in
                                                         ("source_id", "queue_source_id", "comparison_endpoint_id")):
                    out.add("NULLABLE_COUNTERPART_FABRICATION")
        if deep and cps != independent_counterparts(independent_comparison_endpoints()):
            out.add("COUNTERPART_ENDPOINT_BLOB_MISMATCH")
    comparison_endpoints = matrix.get("comparison_endpoints", [])
    if len(comparison_endpoints) != 14 or matrix.get("comparison_endpoint_count") != 14 or \
            comparison_endpoints != comparison_endpoint_contract():
        out.add("COUNTERPART_ENDPOINT_BLOB_MISMATCH")
    elif deep and comparison_endpoints != independent_comparison_endpoints():
        out.add("COUNTERPART_ENDPOINT_BLOB_MISMATCH")
    adjacent = matrix.get("adjacent_comparisons", [])
    if len(adjacent) != 7 or matrix.get("adjacent_comparison_count") != 7:
        out.add("ADJACENT_COMPARISON_MISSING")
    elif deep and adjacent != independent_adjacent_comparisons(independent_comparison_endpoints()):
        out.add("ADJACENT_COMPARISON_MISSING")
    patches = matrix.get("patches", [])
    for row in patches:
        cls = row.get("classification")
        if cls == "BEHAVIOR_DELTA": out.add("VERSION_ONLY_TO_BEHAVIOR_DELTA")
        elif cls == "EOL_BEHAVIOR_DELTA": out.add("EOL_ONLY_BEHAVIOR_DELTA")
        elif cls == "PATH_BEHAVIOR_DELTA": out.add("PATH_ONLY_BEHAVIOR_DELTA")
        elif cls != "HEADER_VERSION_PATH_ONLY": out.add("VERSION_ONLY_TO_BEHAVIOR_DELTA")
    if len(patches) != 2 or matrix.get("production_normalized_ast_identical") is not True:
        out.add("VERSION_ONLY_TO_BEHAVIOR_DELTA")
    static = matrix.get("static_python", [])
    if len(static) != 9 or matrix.get("static_python_count") != 9:
        out.add("FROZEN_MODULE_IMPORT")
    for row in static:
        if row.get("authority") == "FROZEN_IMPORTED": out.add("FROZEN_MODULE_IMPORT")
        if row.get("path", "").endswith("tools_check_structure.py") and row.get("authority") != "STATIC_STRUCTURE_ONLY_NO_RUNTIME_PROMOTION":
            out.add("UNTESTED_STRUCTURE_PROMOTION")
    if comparison_endpoints == comparison_endpoint_contract() and len(static) == 9:
        out.update(endpoint_disposition_diagnostics(matrix, runtime, deep=deep))
    auth = matrix.get("authority", {})
    if auth.get("ast_is_runtime") is not False: out.add("AST_TO_RUNTIME_PROMOTION")
    if auth.get("runtime_is_external_science") is not False: out.add("RUNTIME_EXTERNAL_SCIENCE_PROMOTION")
    if auth.get("material") is not False: out.add("SYNTHETIC_TO_MATERIAL_TRUTH")
    if any(auth.get(k) is not False for k in ("external_science", "experimental", "canonical_equation", "final_release")):
        out.add("EXTERNAL_TRUTH_PROMOTION")
    claims = claim_map(matrix)
    q2, q3, q6, q7 = (claims.get(f"P062-CONSUMER-{q}", {}) for q in ("Q2", "Q3", "Q6", "Q7"))
    if "positive Q_j domain enforcement" not in q2.get("missing_or_open", []): out.add("NEGATIVE_Q_UNIQUENESS")
    if "strictly positive n_j domain" not in q2.get("missing_or_open", []): out.add("NONPOSITIVE_N_UNIQUENESS")
    if q3.get("q_ratio_present") is not False: out.add("INVENTED_Q3_QRATIO")
    if q3.get("kappa_present") is not False: out.add("INVENTED_Q3_KAPPA")
    if q6.get("implementation_state") != "GENERIC_LCO_IMPLEMENTATION_NO_EXACT_WORKED_ASSERTION": out.add("ABSENT_Q6_EXACT_ASSERTION")
    if q7.get("implementation_state") != "NOT_IMPLEMENTED": out.add("Q7_BRIDGEHEAD_TO_IMPLEMENTATION")
    out.update(q8_code_matched_diagnostics(matrix, runtime))
    facts = runtime.get("facts", {})
    if facts.get("graph_exit_enforces_metric") is not False: out.add("GRAPH_EXIT0_TO_METRIC_PASS")
    if facts.get("regression_13_of_13_bit_exact") is not True: out.add("TOLERANCE_TO_BIT_EXACT")
    if facts.get("v1020_gates") == "SELF_CONFIRMED" or facts.get("v1021_gates") == "SELF_CONFIRMED": out.add("GATE_SELF_CONFIRMATION")
    expected_facts = {"fit_roundtrip_pass": True, "graph_finite_15_of_15": True,
        "v1020_gates": "G1_G2_G3_nT_PASS", "v1021_gates": "G1_G2_G3_nT_PASS",
        "v1020_v1021_behavior_identical": True, "normalized_ast_three_versions_identical": True,
        "behavior_delta_count": 0, "input_mutation_count": 0, "deleted_output_count": 0}
    if any(facts.get(k) != v for k, v in expected_facts.items()):
        if facts.get("behavior_delta_count") != 0: out.add("PROBE_BEHAVIOR_DELTA_TAMPER")
        elif facts.get("v1020_gates") != "G1_G2_G3_nT_PASS" or facts.get("v1021_gates") != "G1_G2_G3_nT_PASS": out.add("GATE_SELF_CONFIRMATION")
        else: out.add("RUNTIME_EXIT_TAMPER")
    runs = runtime.get("official_runs", [])
    if len(runs) != 5: out.add("RUNTIME_EXIT_TAMPER")
    meta_by_id = {run_id: (name, cwd, script) for run_id, name, cwd, script in OFFICIAL_RUN_META}
    available_expected = [f"P062-CODE-SRC-{i:03d}" for i in range(1, 12)]
    for row in runs:
        if set(row) != RUN_KEYS:
            runtime_schema_mismatch = True
        expected_meta = meta_by_id.get(row.get("run_id"))
        if expected_meta is None or (row.get("name"), row.get("cwd"), row.get("argv"), row.get("runtime")) != (
                expected_meta[0], expected_meta[1], ["python3.12", expected_meta[2]], RUNTIME_LABEL):
            out.add("OFFICIAL_ARGV_TAMPER")
        if row.get("observations") != EXPECTED_OBSERVATIONS.get(row.get("name")):
            out.add("OFFICIAL_OBSERVATION_TAMPER")
        if row.get("timeout_seconds") != 180: out.add("RUNTIME_TIMEOUT_MISSING")
        if row.get("exit_code") != 0: out.add("RUNTIME_EXIT_TAMPER")
        if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("stdout_sha256"))): out.add("RUNTIME_STDOUT_HASH_TAMPER")
        if row.get("available_fixture_source_ids") != available_expected or \
                tuple(row.get("consumed_input_source_ids", [])) != CONSUMED_EXPECTED.get(row.get("name")) or \
                "input_source_ids" in row:
            out.add("RUNTIME_INPUT_ROLE_COLLAPSE")
        if deep and row.get("consumed_input_evidence") != independent_consumed_input_evidence(row.get("name")):
            out.add("RUNTIME_INPUT_ROLE_COLLAPSE")
        generated = row.get("generated", [])
        if row.get("generated_output_count") != len(generated) or \
                len({x.get("path") for x in generated}) != len(generated):
            out.add("RUNTIME_OUTPUT_MISATTRIBUTION")
        if row.get("deleted_output_count") != sum(x.get("change_type") == "DELETED" for x in generated):
            out.add("RUNTIME_OUTPUT_DELETION_TAMPER")
        for output in generated:
            keys = set(output)
            if output.get("producer_run_id") != row.get("run_id") or output.get("change_type") not in {"NEW", "MODIFIED", "DELETED"}:
                out.add("RUNTIME_OUTPUT_MISATTRIBUTION")
            if output.get("change_type") == "NEW" and output.get("before_sha256") is not None:
                out.add("RUNTIME_OUTPUT_MISATTRIBUTION")
            if output.get("change_type") == "MODIFIED" and (not re.fullmatch(r"[0-9a-f]{64}", str(output.get("before_sha256"))) or
                    output.get("before_sha256") == output.get("sha256")):
                out.add("RUNTIME_OUTPUT_MISATTRIBUTION")
            if output.get("change_type") == "DELETED" and (not re.fullmatch(r"[0-9a-f]{64}", str(output.get("before_sha256"))) or
                    output.get("sha256") is not None or output.get("bytes") is not None):
                out.add("RUNTIME_OUTPUT_DELETION_TAMPER")
            if keys != {"path", "producer_run_id", "change_type", "before_sha256", "sha256", "bytes"}:
                out.add("RUNTIME_OUTPUT_MISATTRIBUTION")
    probe = runtime.get("independent_probe", {})
    if probe.get("version_count") != 3 or probe.get("normalized_behavior_identical") is not True or probe.get("behavior_delta_count") != 0:
        out.add("PROBE_BEHAVIOR_DELTA_TAMPER")
    if probe.get("stdout_sha256") != PROBE_STDOUT_SHA256:
        out.add("PROBE_DIGEST_TAMPER")
    if runtime.get("runtime_scope") != RUNTIME_SCOPE_EXPECTED:
        out.add("DEPENDENCY_INVENTORY_TAMPER")
    if runtime.get("cleanup") != {"strategy": "isolated exact TemporaryDirectory equivalent", "completed": True}:
        out.add("CLEANUP_TAMPER")
    rauth = runtime.get("authority", {})
    if any(rauth.get(k) is not False for k in ("static_to_runtime_promotion", "external_science", "material", "experimental")):
        out.add("EXTERNAL_TRUTH_PROMOTION")
    rf = matrix.get("result_first", {})
    if rf.get("sentinel") != SENTINEL or rf.get("write_order") != ["result", "code_delta_matrix", "runtime_attestation"]:
        out.add("RESULT_FIRST_SENTINEL_MISSING")
    if matrix.get("finding_counts") != {"P0": 0, "P1": 5, "P2": 4} or len(matrix.get("findings", [])) != 9:
        out.add("FINDINGS")
    if matrix.get("required_negative_controls") != list(NEGATIVES) or matrix.get("required_negative_control_count") != len(NEGATIVES):
        out.add("NEGATIVE_MANIFEST")
    if not out and declared_count_mismatch:
        out.add("MATRIX_DECLARED_COUNT_TAMPER")
    if not out and claim_projection_mismatch:
        out.add("CLAIM_CONSUMER_TAMPER")
    if not out and finding_projection_mismatch:
        out.add("FINDING_ROW_TAMPER")
    if not out and (matrix_schema_mismatch or shape_sha(matrix) != MATRIX_SHAPE_SHA256):
        out.add("MATRIX_SCHEMA_TAMPER")
    if not out and (runtime_schema_mismatch or shape_sha(runtime) != RUNTIME_SHAPE_SHA256):
        out.add("RUNTIME_SCHEMA_TAMPER")
    if not out and semantic_sha(matrix) != MATRIX_GOLDEN_SHA256:
        out.add("MATRIX_GOLDEN_PROJECTION")
    if not out and semantic_sha(runtime) != RUNTIME_GOLDEN_SHA256:
        out.add("RUNTIME_GOLDEN_PROJECTION")
    return out


def normalized_output(data: bytes, temp_root: Path) -> bytes:
    text = data.decode("utf-8", "replace").replace("\\", "/")
    text = text.replace(temp_root.as_posix(), "<TMP>")
    text = re.sub(r"[A-Za-z]:/[^\r\n]*?/p062-step55-[^/\r\n]+", "<TMP>", text)
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def runtime_output_manifest(temp_root: Path) -> dict[str, dict[str, Any]]:
    frozen = {f"fixture/{path}" for path, *_ in SOURCE_EXPECTED}
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


def independent_dependency_inventory() -> dict[str, Any]:
    code = ("import json,sys,numpy; d={'python':sys.version.split()[0],'implementation':sys.implementation.name,"
            "'numpy':numpy.__version__};\n"
            "try:\n import scipy; d['scipy']=scipy.__version__\nexcept Exception: d['scipy']=None\n"
            "try:\n import matplotlib; d['matplotlib']=matplotlib.__version__\nexcept Exception: d['matplotlib']=None\n"
            "print(json.dumps(d,sort_keys=True))")
    cp = proc(["py", "-3.12", "-c", code], timeout=30, text=True)
    if cp.returncode:
        raise ValidationError(f"FRESH_DEPENDENCY_INVENTORY:{cp.returncode}:{cp.stderr.strip()}")
    return strict_load_bytes(cp.stdout.encode("utf-8"))


def independent_probe_script() -> str:
    return r'''import hashlib,importlib.util,json,numpy as np,pathlib
root=pathlib.Path(__file__).resolve().parent
def load(rel,name):
 spec=importlib.util.spec_from_file_location(name,root/rel); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def digest(value): return hashlib.sha256(np.asarray(value).tobytes()).hexdigest()
result={}
for version,rel in [('v1019','v1.0.19/Anode_Fit_v1.0.19.py'),('v1020','v1.0.20/Anode_Fit_v1.0.20.py'),('v1021','v1.0.21/Anode_Fit_v1.0.21.py')]:
 module=load(rel,'validator_'+version); voltage=np.linspace(.03,.34,73); composition=np.linspace(.1,.9,17)
 model=module.GraphiteAnodeDischargeDQDV(module.GRAPHITE_STAGING_LIT,x=.5,Rn=.01,Cbg=.05,use_dH_eff=True)
 result[version]={'eq':digest(model.equilibrium(voltage,298.15)),'dqdv':digest(model.dqdv(voltage,298.15,.2,1.,+1)),
 'uoc':digest(model.solve_U_oc(composition,298.15)),'entropy':digest(model.entropy_coefficient_x(composition,298.15)),
 'qrev':digest(model.reversible_heat_x(composition,298.15,I=1.0)),'seed':digest(model.seed_L_V)}
print(json.dumps(result,sort_keys=True,separators=(',',':')))
'''


def fresh_runtime_compare(stored: dict[str, Any]) -> None:
    temp = Path(tempfile.mkdtemp(prefix="p062-step55-validator-"))
    root = temp / "fixture"
    fresh_runs: list[dict[str, Any]] = []
    try:
        for path, *_ in SOURCE_EXPECTED:
            dest = root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob(path))
        frozen_before = {path: sha((root / path).read_bytes()) for path, *_ in SOURCE_EXPECTED}
        dependencies = independent_dependency_inventory()
        available_ids = [f"P062-CODE-SRC-{i:03d}" for i in range(1, 12)]
        for run_id, name, rel, script in OFFICIAL_RUN_META:
            env = os.environ.copy()
            env.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
                        "ANODEFIT_TMP": str(temp / "g3" / run_id), "MPLCONFIGDIR": str(temp / "mpl" / run_id)})
            Path(env["ANODEFIT_TMP"]).mkdir(parents=True, exist_ok=True)
            before_outputs = runtime_output_manifest(temp)
            cp = proc(["py", "-3.12", script], cwd=root / rel, env=env, timeout=180)
            after_outputs = runtime_output_manifest(temp)
            stdout = normalized_output(cp.stdout, temp)
            stderr = normalized_output(cp.stderr, temp)
            stdout_text = stdout.decode("utf-8")
            observations = {
                "regression_13_of_13_bit_exact": "13/13 PASS" in stdout_text if name == "v1019_regression" else None,
                "fit_roundtrip_pass": "ROUND-TRIP: PASS" in stdout_text if name == "v1019_fit_roundtrip" else None,
                "graph_finite_15_of_15": (stdout_text.count("[finite]") == 15 and
                                           "ALL PANELS FINITE: True" in stdout_text)
                                          if name == "v1019_graph_suite" else None,
                "all_four_gates_pass": all(token in stdout_text for token in
                                             ("G1 PASS", "G2 PASS", "G3 PASS", "n(T) PASS"))
                                       if name in {"v1020_gates", "v1021_gates"} else None,
            }
            if cp.returncode != 0 or observations != EXPECTED_OBSERVATIONS[name]:
                raise ValidationError(f"FRESH_RUNTIME:{name}:{cp.returncode}")
            generated = runtime_output_delta(before_outputs, after_outputs, run_id)
            fresh_runs.append({"run_id": run_id, "name": name, "runtime": RUNTIME_LABEL,
                               "cwd": rel, "argv": ["python3.12", script], "timeout_seconds": 180,
                               "exit_code": cp.returncode, "stdout_sha256": sha(stdout),
                               "stderr_sha256": sha(stderr), "stdout_lines": len(stdout_text.splitlines()),
                               "stderr_lines": len(stderr.decode("utf-8").splitlines()),
                               "observations": observations, "generated": generated,
                               "generated_output_count": len(generated),
                               "deleted_output_count": sum(row["change_type"] == "DELETED" for row in generated),
                               "available_fixture_source_ids": available_ids,
                               "consumed_input_source_ids": list(CONSUMED_EXPECTED[name]),
                               "consumed_input_evidence": independent_consumed_input_evidence(name)})
        probe_dir = root / "Claude/docs"
        probe_path = probe_dir / "validator_probe_three_versions.py"
        probe_path.write_text(independent_probe_script(), encoding="utf-8", newline="\n")
        cp = proc(["py", "-3.12", probe_path.name], cwd=probe_dir, timeout=60)
        if cp.returncode:
            raise ValidationError(f"FRESH_PROBE:{cp.returncode}:{cp.stderr.decode('utf-8','replace')}")
        probe_data = strict_load_bytes(cp.stdout)
        values = list(probe_data.values())
        probe_row = {"probe_id": "P062-PROBE-001", "runtime": RUNTIME_LABEL, "versions": probe_data,
                     "version_count": 3, "normalized_behavior_identical": all(v == values[0] for v in values[1:]),
                     "behavior_delta_count": sum(v != values[0] for v in values[1:]),
                     "stdout_sha256": sha(canonical(probe_data))}
        frozen_after = {path: sha((root / path).read_bytes()) for path, *_ in SOURCE_EXPECTED}
        if frozen_before != frozen_after:
            raise ValidationError("FRESH_INPUT_MUTATION")
        by_name = {row["name"]: row for row in fresh_runs}
        expected_runtime = {
            "schema": "P062_STEP55_RUNTIME_ATTESTATION_V1", "input_commit": PARENT,
            "frozen_baseline": BASELINE, "runtime_scope": dependencies, "official_runs": fresh_runs,
            "independent_probe": probe_row,
            "facts": {"regression_13_of_13_bit_exact": by_name["v1019_regression"]["observations"]["regression_13_of_13_bit_exact"],
                      "fit_roundtrip_pass": by_name["v1019_fit_roundtrip"]["observations"]["fit_roundtrip_pass"],
                      "graph_finite_15_of_15": by_name["v1019_graph_suite"]["observations"]["graph_finite_15_of_15"],
                      "graph_exit_enforces_metric": False, "v1020_gates": "G1_G2_G3_nT_PASS",
                      "v1021_gates": "G1_G2_G3_nT_PASS", "v1020_v1021_behavior_identical": True,
                      "normalized_ast_three_versions_identical": True, "behavior_delta_count": 0,
                      "input_mutation_count": 0,
                      "deleted_output_count": sum(row["deleted_output_count"] for row in fresh_runs)},
            "environment_dependent_fields_excluded": ["duration", "absolute_temp_path", "host"],
            "cleanup": {"strategy": "isolated exact TemporaryDirectory equivalent", "completed": True},
            "authority": {"static_to_runtime_promotion": False, "external_science": False,
                          "material": False, "experimental": False},
        }
        if stored != expected_runtime:
            raise ValidationError("FRESH_RUNTIME_FULL_ARTIFACT_MISMATCH")
    finally:
        shutil.rmtree(temp, ignore_errors=False)
        if temp.exists():
            raise ValidationError("TEMP_CLEANUP")


def validate_content(*, fresh_runtime: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    matrix, runtime = strict_load(MATRIX), strict_load(ATTESTATION)
    policy = builder_ast_policy()
    if policy:
        raise ValidationError(";".join(policy))
    codes = content_diagnostics(matrix, runtime, deep=True)
    if codes:
        raise ValidationError("CONTENT:" + ",".join(sorted(codes)))
    source_rows = independent_source_rows()
    if matrix["static_python"] != independent_static_rows(source_rows):
        raise ValidationError("INDEPENDENT_STATIC_MISMATCH")
    if matrix["patches"] != independent_patches():
        raise ValidationError("INDEPENDENT_PATCH_MISMATCH")
    comparison_endpoints = independent_comparison_endpoints()
    if matrix["comparison_endpoints"] != comparison_endpoints:
        raise ValidationError("INDEPENDENT_COMPARISON_ENDPOINTS")
    if matrix["counterpart_matrix"] != independent_counterparts(comparison_endpoints):
        raise ValidationError("INDEPENDENT_COUNTERPART_MATRIX")
    if matrix["adjacent_comparisons"] != independent_adjacent_comparisons(comparison_endpoints):
        raise ValidationError("INDEPENDENT_ADJACENT_COMPARISONS")
    endpoint_ids = [v["queue_source_id"] for row in matrix["counterpart_matrix"]
                    for v in row["versions"].values() if v["queue_source_id"] is not None]
    if sorted(endpoint_ids) != sorted(x["source_id"] for x in source_rows):
        raise ValidationError("INDEPENDENT_COUNTERPART_COVERAGE")
    norm = []
    for path, *_ in SOURCE_EXPECTED:
        if "/Anode_Fit_" in path:
            tree = VersionNormalizer().visit(ast.parse(blob(path).decode("utf-8")))
            ast.fix_missing_locations(tree)
            norm.append(ast_digest(tree))
    if len(set(norm)) != 1:
        raise ValidationError("INDEPENDENT_NORMALIZED_AST")
    if fresh_runtime:
        fresh_runtime_compare(runtime)
    return matrix, runtime


BOUNDARY = {"EXTRA_DIRTY_PATH", "STAGED_WORKTREE_MISMATCH", "ACTIVE_REMOTE_DIVERGENCE",
            "PROTECTED_DRIFT", "MAIN_DRIFT", "CLAUDE_DRIFT", "DETACHED_HEAD",
            "LOCAL_PROTECTED_DRIFT", "PERSISTENCE_PARENT_MISMATCH", "PERSISTENCE_SUBJECT_MISMATCH"}


def fixture_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def boundary_negative_fixture(name: str) -> set[str]:
    if name not in BOUNDARY:
        raise ValidationError(f"UNKNOWN_BOUNDARY_FIXTURE:{name}")
    temp_path: Path | None = None
    with tempfile.TemporaryDirectory(prefix="p062-step55-git-boundary-") as td:
        temp_path = Path(td)
        origin = temp_path / "origin.git"
        work = temp_path / "work"
        origin.mkdir()
        work.mkdir()
        git_at(origin, ["init", "--bare"])
        git_at(work, ["init", "-b", "active"])
        for key, value in (("user.name", "Step55 Fixture"), ("user.email", "step55@example.invalid"),
                           ("core.autocrlf", "false")):
            git_at(work, ["config", key, value])
        fixture_write(work / "seed.txt", "seed\n")
        fixture_write(work / "Claude/base.txt", "protected baseline\n")
        git_at(work, ["add", "--", "seed.txt", "Claude/base.txt"])
        git_at(work, ["commit", "-m", "fixture base"])
        base = git_at(work, ["rev-parse", "HEAD"]).strip()
        git_at(work, ["branch", "protected", base])
        git_at(work, ["branch", "main", base])
        git_at(work, ["remote", "add", "origin", str(origin)])
        git_at(work, ["push", "-u", "origin", "active", "protected", "main"])
        if name in {"EXTRA_DIRTY_PATH", "STAGED_WORKTREE_MISMATCH"}:
            for i, path in enumerate(EXACT_EIGHT, 1):
                fixture_write(work / path, f"fixture {i}\n")
            if name == "EXTRA_DIRTY_PATH":
                fixture_write(work / "Codex/results/EXTRA.txt", "extra\n")
                observed = precommit_diagnostics(
                    work, False, branch="active", parent=base, protected_branch="protected",
                    protected_tip=base, exact_paths=EXACT_EIGHT)
            else:
                git_at(work, ["add", "--", *EXACT_EIGHT])
                fixture_write(work / EXACT_EIGHT[0], "fixture 1\nunstaged mutation\n")
                observed = precommit_diagnostics(
                    work, True, branch="active", parent=base, protected_branch="protected",
                    protected_tip=base, exact_paths=EXACT_EIGHT)
        else:
            parent_expected = base
            if name == "CLAUDE_DRIFT":
                fixture_write(work / "Claude/drift.txt", "drift\n")
                git_at(work, ["add", "--", "Claude/drift.txt"])
                git_at(work, ["commit", "-m", "fixture parent with Claude drift"])
                parent_expected = git_at(work, ["rev-parse", "HEAD"]).strip()
            elif name == "PERSISTENCE_PARENT_MISMATCH":
                fixture_write(work / "parent-extra.txt", "different parent\n")
                git_at(work, ["add", "--", "parent-extra.txt"])
                git_at(work, ["commit", "-m", "fixture different parent"])
            for i, path in enumerate(EXACT_EIGHT, 1):
                fixture_write(work / path, f"fixture committed {i}\n")
            git_at(work, ["add", "--", *EXACT_EIGHT])
            subject = "wrong subject" if name == "PERSISTENCE_SUBJECT_MISMATCH" else SUBJECT
            git_at(work, ["commit", "-m", subject])
            child = git_at(work, ["rev-parse", "HEAD"]).strip()
            git_at(work, ["push", "origin", "active"])
            if name == "ACTIVE_REMOTE_DIVERGENCE":
                git_at(origin, ["update-ref", "refs/heads/active", parent_expected])
            elif name == "PROTECTED_DRIFT":
                git_at(origin, ["update-ref", "refs/heads/protected", child])
            elif name == "MAIN_DRIFT":
                git_at(origin, ["update-ref", "refs/heads/main", child])
            elif name == "LOCAL_PROTECTED_DRIFT":
                git_at(work, ["branch", "-f", "protected", child])
            elif name == "DETACHED_HEAD":
                git_at(work, ["checkout", "--detach", child])
            observed = persistence_diagnostics(
                work, branch="active", upstream="origin/active", parent_expected=parent_expected,
                subject_expected=SUBJECT, protected_branch="protected", protected_tip=base,
                main_tip=base, exact_paths=EXACT_EIGHT)
    if temp_path is not None and temp_path.exists():
        raise ValidationError(f"BOUNDARY_FIXTURE_CLEANUP:{name}")
    return observed


def run_negative_controls(matrix: dict[str, Any], runtime: dict[str, Any]) -> None:
    baseline = content_diagnostics(matrix, runtime, deep=False)
    if baseline:
        raise ValidationError("NEGATIVE_BASELINE:" + ",".join(sorted(baseline)))
    deletion_fixture = runtime_output_delta({"gone.bin": {"sha256": "a" * 64, "bytes": 1}}, {}, "P062-RUN-FIXTURE")
    if deletion_fixture != [{"path": "gone.bin", "producer_run_id": "P062-RUN-FIXTURE",
                             "change_type": "DELETED", "before_sha256": "a" * 64,
                             "sha256": None, "bytes": None}]:
        raise ValidationError("NEGATIVE_BASELINE:RUNTIME_OUTPUT_DELETION_TAMPER")
    cases: dict[str, Callable[[dict[str, Any], dict[str, Any]], None]] = {}
    def reg(name: str, fn: Callable[[dict[str, Any], dict[str, Any]], None]) -> None:
        cases[name] = fn
    reg("VERSION_ONLY_TO_BEHAVIOR_DELTA", lambda m, r: m["patches"][0].__setitem__("classification", "BEHAVIOR_DELTA"))
    reg("TOLERANCE_TO_BIT_EXACT", lambda m, r: r["facts"].__setitem__("regression_13_of_13_bit_exact", False))
    reg("AST_TO_RUNTIME_PROMOTION", lambda m, r: m["authority"].__setitem__("ast_is_runtime", True))
    reg("GRAPH_EXIT0_TO_METRIC_PASS", lambda m, r: r["facts"].__setitem__("graph_exit_enforces_metric", True))
    reg("NEGATIVE_Q_UNIQUENESS", lambda m, r: m["claim_consumers"][0]["missing_or_open"].remove("positive Q_j domain enforcement"))
    reg("NONPOSITIVE_N_UNIQUENESS", lambda m, r: m["claim_consumers"][0]["missing_or_open"].remove("strictly positive n_j domain"))
    reg("INVENTED_Q3_QRATIO", lambda m, r: m["claim_consumers"][1].__setitem__("q_ratio_present", True))
    reg("INVENTED_Q3_KAPPA", lambda m, r: m["claim_consumers"][1].__setitem__("kappa_present", True))
    reg("ABSENT_Q6_EXACT_ASSERTION", lambda m, r: m["claim_consumers"][2].__setitem__("implementation_state", "EXACT_ASSERTED"))
    reg("Q7_BRIDGEHEAD_TO_IMPLEMENTATION", lambda m, r: m["claim_consumers"][3].__setitem__("implementation_state", "IMPLEMENTED"))
    reg("FROZEN_MODULE_IMPORT", lambda m, r: m["static_python"][0].__setitem__("authority", "FROZEN_IMPORTED"))
    reg("RUNTIME_TIMEOUT_MISSING", lambda m, r: r["official_runs"][0].__setitem__("timeout_seconds", None))
    reg("EOL_ONLY_BEHAVIOR_DELTA", lambda m, r: m["patches"][0].__setitem__("classification", "EOL_BEHAVIOR_DELTA"))
    reg("PATH_ONLY_BEHAVIOR_DELTA", lambda m, r: m["patches"][0].__setitem__("classification", "PATH_BEHAVIOR_DELTA"))
    reg("SYNTHETIC_TO_MATERIAL_TRUTH", lambda m, r: m["authority"].__setitem__("material", True))
    reg("NULLABLE_COUNTERPART_FABRICATION", lambda m, r: m["counterpart_matrix"][2]["versions"]["v1.0.20"].__setitem__("source_id", "FAKE"))
    reg("GATE_SELF_CONFIRMATION", lambda m, r: r["facts"].__setitem__("v1020_gates", "SELF_CONFIRMED"))
    reg("UNTESTED_STRUCTURE_PROMOTION", lambda m, r: next(x for x in m["static_python"] if x["path"].endswith("tools_check_structure.py")).__setitem__("authority", "RUNTIME_PROMOTED"))
    reg("QUEUE_BLOB_MISMATCH", lambda m, r: m["queue"][0].__setitem__("raw_sha256", "0" * 64))
    reg("QUEUE_ORPHAN", lambda m, r: (m["queue"].pop(), m.__setitem__("queue_count", 10)))
    reg("COUNTERPART_REASON_MISSING", lambda m, r: m["counterpart_matrix"][2]["versions"]["v1.0.20"].__setitem__("null_reason", ""))
    reg("RUNTIME_EXIT_TAMPER", lambda m, r: r["official_runs"][0].__setitem__("exit_code", 1))
    reg("RUNTIME_STDOUT_HASH_TAMPER", lambda m, r: r["official_runs"][0].__setitem__("stdout_sha256", "bad"))
    reg("PROBE_BEHAVIOR_DELTA_TAMPER", lambda m, r: r["independent_probe"].__setitem__("behavior_delta_count", 1))
    reg("EXTERNAL_TRUTH_PROMOTION", lambda m, r: m["authority"].__setitem__("external_science", True))
    reg("RESULT_FIRST_SENTINEL_MISSING", lambda m, r: m["result_first"].__setitem__("sentinel", "MISSING"))
    reg("COUNTERPART_ENDPOINT_BLOB_MISMATCH", lambda m, r: m["comparison_endpoints"][0].__setitem__("raw_sha256", "0" * 64))
    reg("ADJACENT_COMPARISON_MISSING", lambda m, r: (m["adjacent_comparisons"].pop(),
                                                       m.__setitem__("adjacent_comparison_count", 6)))
    def misattribute(m: dict[str, Any], r: dict[str, Any]) -> None:
        owner = next(row for row in r["official_runs"] if row["generated"])
        owner["generated"][0]["producer_run_id"] = "P062-RUN-999"
    reg("RUNTIME_OUTPUT_MISATTRIBUTION", misattribute)
    reg("RUNTIME_INPUT_ROLE_COLLAPSE", lambda m, r: r["official_runs"][0].__setitem__(
        "consumed_input_source_ids", list(r["official_runs"][0]["available_fixture_source_ids"])))
    reg("ENDPOINT_DISPOSITION_MISSING", lambda m, r: (m["endpoint_dispositions"].pop(),
                                                        m.__setitem__("endpoint_disposition_count", 13)))
    reg("ENDPOINT_DISPOSITION_DUPLICATE", lambda m, r: m["endpoint_dispositions"].append(
        copy.deepcopy(m["endpoint_dispositions"][0])))
    def orphan_disposition(m: dict[str, Any], r: dict[str, Any]) -> None:
        row = copy.deepcopy(m["endpoint_dispositions"][0])
        row["disposition_id"] = "P062-END-DISP-999"
        row["comparison_endpoint_id"] = "P062-CMP-END-999"
        row["path"] = "orphan"
        m["endpoint_dispositions"].append(row)
    reg("ENDPOINT_DISPOSITION_ORPHAN", orphan_disposition)
    reg("ENDPOINT_DISPOSITION_SCHEMA", lambda m, r: m["endpoint_dispositions"][0].__setitem__("unexpected", True))
    reg("ENDPOINT_BLOB_BINDING_MISMATCH", lambda m, r: m["endpoint_dispositions"][0]["blob"].__setitem__("raw_sha256", "0" * 64))
    reg("ENDPOINT_AST_STATE_INVALID", lambda m, r: m["endpoint_dispositions"][0]["ast"].__setitem__("state", "INVALID"))
    reg("ENDPOINT_AST_NA_REASON_MISSING", lambda m, r: next(
        row for row in m["endpoint_dispositions"] if row["ast"]["state"] == "N_A_NON_PYTHON")["ast"].__setitem__("n_a_reason", ""))
    reg("ENDPOINT_AST_DIGEST_BINDING_MISMATCH", lambda m, r: next(
        row for row in m["endpoint_dispositions"] if row["ast"]["state"] == "DIRECT_AST_PROJECTION")["ast"].__setitem__("digest", "0" * 64))
    reg("ENDPOINT_AST_INHERITANCE_BASIS_MISMATCH", lambda m, r: next(
        row for row in m["endpoint_dispositions"] if row["ast"]["state"] == "BYTE_IDENTICAL_AST_INHERITANCE")["ast"].__setitem__("basis_endpoint_id", "P062-CMP-END-999"))
    reg("ENDPOINT_RUNTIME_STATE_MISMATCH", lambda m, r: m["endpoint_dispositions"][0]["runtime"].__setitem__("state", "INVALID"))
    reg("ENDPOINT_RUNTIME_REASON_MISSING", lambda m, r: m["endpoint_dispositions"][0]["runtime"].__setitem__("reason", ""))
    reg("ENDPOINT_AUTHORITY_PROMOTION", lambda m, r: m["endpoint_dispositions"][0]["authority"].__setitem__("external_science", True))
    reg("Q8_CODE_MATCHED_CLAIM_MISSING", lambda m, r: (m["code_matched_claims"].pop(),
                                                          m.__setitem__("code_matched_claim_count", 0)))
    reg("Q8_CODE_MATCHED_CLAIM_DUPLICATE", lambda m, r: (
        m["code_matched_claims"].append(copy.deepcopy(m["code_matched_claims"][0])),
        m.__setitem__("code_matched_claim_count", 2)))
    reg("Q8_CODE_MATCHED_FOUR_AXIS_SCHEMA", lambda m, r: m["code_matched_claims"][0]["blob"].pop("state"))
    reg("Q8_CODE_MATCHED_SOURCE_MUTATION", lambda m, r: m["code_matched_claims"][0]["blob"].__setitem__(
        "slice_sha256", "0" * 64))
    reg("Q8_CODE_MATCHED_ENDPOINT_BINDING", lambda m, r: m["code_matched_claims"][0]["ast"].__setitem__(
        "production_endpoint_ids", ["P062-CMP-END-001", "P062-CMP-END-002"]))
    reg("Q8_CODE_MATCHED_RUNTIME_BINDING", lambda m, r: m["code_matched_claims"][0]["runtime"].__setitem__(
        "official_run_ids", ["P062-RUN-001", "P062-RUN-002", "P062-RUN-003", "P062-RUN-004"]))
    reg("Q8_CODE_MATCHED_AUTHORITY_PROMOTION", lambda m, r: m["code_matched_claims"][0]["authority"].__setitem__(
        "whole_semantic_runtime_equality", True))
    reg("MATRIX_GATE_TAMPER", lambda m, r: m.__setitem__("gate", "PASS"))
    reg("MATRIX_DECLARED_COUNT_TAMPER", lambda m, r: m.__setitem__("claim_consumer_count", 5))
    reg("CLAIM_CONSUMER_TAMPER", lambda m, r: m["claim_consumers"][0].__setitem__("evidence", ["fake:1"]))
    reg("FINDING_ROW_TAMPER", lambda m, r: m["findings"][0].__setitem__("finding", "tampered"))
    reg("RUNTIME_EXTERNAL_SCIENCE_PROMOTION", lambda m, r: m["authority"].__setitem__(
        "runtime_is_external_science", True))
    reg("PROBE_DIGEST_TAMPER", lambda m, r: r["independent_probe"].__setitem__("stdout_sha256", "0" * 64))
    reg("OFFICIAL_OBSERVATION_TAMPER", lambda m, r: r["official_runs"][0]["observations"].__setitem__(
        "regression_13_of_13_bit_exact", False))
    reg("OFFICIAL_ARGV_TAMPER", lambda m, r: r["official_runs"][0].__setitem__(
        "argv", ["python3.12", "evil.py"]))
    reg("DEPENDENCY_INVENTORY_TAMPER", lambda m, r: r["runtime_scope"].__setitem__("python", "0.0.0"))
    reg("CLEANUP_TAMPER", lambda m, r: r["cleanup"].__setitem__("completed", False))
    reg("MATRIX_SCHEMA_TAMPER", lambda m, r: m.__setitem__("unexpected", True))
    reg("RUNTIME_SCHEMA_TAMPER", lambda m, r: r.__setitem__("unexpected", True))
    reg("MATRIX_GOLDEN_PROJECTION", lambda m, r: m["result_first"].__setitem__("containing_commit", "OTHER_PENDING"))
    reg("RUNTIME_GOLDEN_PROJECTION", lambda m, r: r.__setitem__(
        "environment_dependent_fields_excluded", ["duration", "absolute_temp_path", "platform"]))
    reg("RUNTIME_OUTPUT_DELETION_TAMPER", lambda m, r: r["official_runs"][0].__setitem__(
        "deleted_output_count", 1))
    passed = 0
    for name in NEGATIVES:
        if name == "DUPLICATE_JSON_KEY":
            try:
                strict_load_bytes(b'{"x":1,"x":2}')
            except ValidationError as exc:
                observed = {"DUPLICATE_JSON_KEY"} if str(exc).startswith("DUPLICATE_JSON_KEY") else {str(exc)}
            else:
                observed = set()
        elif name == "NONFINITE_JSON":
            try:
                strict_load_bytes(b'{"x":NaN}')
            except ValidationError as exc:
                observed = {"NONFINITE_JSON"} if str(exc).startswith("NONFINITE_JSON") else {str(exc)}
            else:
                observed = set()
        elif name == "ACTIVE_LEDGER_STALE_STEP54_NEXT":
            parent_text = (REPO / PARENT_LEDGER).read_text(encoding="utf-8")
            active_text = (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8")
            handover_text = (REPO / HANDOVER).read_text(encoding="utf-8")
            mutated = active_text.replace("Controller performs final Step 55 exact-eight validation",
                                          "Controller performs final Step 54 exact-seven validation", 1)
            observed = current_control_diagnostics(parent_text, mutated, handover_text)
        elif name == "RESULT_ARTIFACT_SHA_TAMPER":
            result_text = (REPO / RESULT).read_text(encoding="utf-8")
            matrix_bytes = (REPO / MATRIX).read_bytes()
            runtime_bytes = (REPO / ATTESTATION).read_bytes()
            mutated = result_text.replace(sha(matrix_bytes), "0" * 64, 1)
            observed = result_artifact_sha_diagnostics(mutated, matrix_bytes, runtime_bytes)
        elif name in BOUNDARY:
            observed = boundary_negative_fixture(name)
        elif name in cases:
            m, r = copy.deepcopy(matrix), copy.deepcopy(runtime)
            cases[name](m, r)
            observed = content_diagnostics(m, r, deep=False) - baseline
        else:
            observed = set()
        if observed != {name}:
            raise ValidationError(f"NEGATIVE_NOT_SINGLETON:{name}:{sorted(observed)}")
        passed += 1
    print(f"PASS_P062_STEP55_NEGATIVE_CONTROLS {passed}/{len(NEGATIVES)} isolated={passed} nonisolated=0")


def builder_determinism() -> None:
    with tempfile.TemporaryDirectory(prefix="p062-step55-det-") as td:
        root = Path(td)
        outputs = []
        for i in range(2):
            paths = [root / f"m{i}.json", root / f"a{i}.json", root / f"r{i}.md"]
            cp = proc(["py", "-3.12", str(REPO / BUILDER), "--repo", str(REPO),
                       "--matrix", str(paths[0]), "--attestation", str(paths[1]), "--result", str(paths[2])],
                      timeout=240, text=True)
            if cp.returncode:
                raise ValidationError(f"BUILDER_RERUN:{i}:{cp.stdout}:{cp.stderr}")
            outputs.append(tuple(p.read_bytes() for p in paths))
        if outputs[0] != outputs[1]:
            raise ValidationError("BUILDER_NONDETERMINISTIC")
        stored = ((REPO / MATRIX).read_bytes(), (REPO / ATTESTATION).read_bytes(), (REPO / RESULT).read_bytes())
        if outputs[0] != stored:
            raise ValidationError("BUILDER_STORED_MISMATCH")
    print("PASS_P062_STEP55_DETERMINISM 2/2")


def parse_status_paths(repo: Path = REPO) -> set[str]:
    raw = git_at(repo, ["status", "--porcelain=v1", "-z"], text=False)
    parts, paths, i = raw.split(b"\0"), set(), 0
    while i < len(parts) and parts[i]:
        entry = parts[i]
        status = entry[:2].decode("ascii", "replace")
        paths.add(entry[3:].decode("utf-8").replace("\\", "/"))
        i += 1
        if "R" in status or "C" in status:
            if i < len(parts) and parts[i]:
                paths.add(parts[i].decode("utf-8").replace("\\", "/"))
                i += 1
    return paths


def markdown_table_rows(text: str) -> list[list[str]]:
    return [[cell.strip() for cell in line.strip()[1:-1].split("|")]
            for line in text.splitlines()
            if line.strip().startswith("|") and line.strip().endswith("|")]


def current_control_diagnostics(parent_text: str, active_text: str, handover_text: str) -> set[str]:
    code = "ACTIVE_LEDGER_STALE_STEP54_NEXT"
    parent_rows = markdown_table_rows(parent_text)
    active_rows = markdown_table_rows(active_text)
    handover_rows = markdown_table_rows(handover_text)
    parent_phase = [row for row in parent_rows if row and row[0] == "062"]
    active_phase = [row for row in active_rows if row and row[0] == "062"]
    active_54 = [row for row in active_rows if row and row[0] == "Step 54"]
    active_55 = [row for row in active_rows if row and row[0] == "Step 55"]
    handover_54 = [row for row in handover_rows if row and row[0] == "Phase 062 Step 54"]
    handover_55 = [row for row in handover_rows if row and row[0] == "Phase 062 Step 55"]
    groups = (parent_phase, active_phase, active_54, active_55, handover_54, handover_55)
    if any(len(group) != 1 for group in groups):
        return {code}
    required_rows = (
        (parent_phase[0], ("ce069dde91f1332cc2852312cd2cbccd7cdf38db", "PASS_P062_STEP54_PERSISTENCE",
                           "PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS", "78/78", "Q8", "1/1",
                           "PENDING_AT_PRECOMMIT_BY_DESIGN", "PASS_P062_STEP55_PERSISTENCE")),
        (active_phase[0], ("ce069dde91f1332cc2852312cd2cbccd7cdf38db", "PASS_P062_STEP54_PERSISTENCE",
                          "PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS", "78/78", "Q8", "1/1",
                          "PENDING_AT_PRECOMMIT_BY_DESIGN", "PASS_P062_STEP55_PERSISTENCE")),
        (active_54[0], ("ce069dde91f1332cc2852312cd2cbccd7cdf38db", "pushed", "yes",
                       "PASS_P062_STEP54_PERSISTENCE")),
        (active_55[0], ("PENDING_AT_PRECOMMIT_BY_DESIGN", "exact-eight checkpoint prepared",
                       "verify after atomic commit", "PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS",
                         "78/78", "Q8", "1/1", "PASS_P062_STEP55_PERSISTENCE")),
        (handover_54[0], ("ce069dde91f1332cc2852312cd2cbccd7cdf38db", "PASS_P062_STEP54_PERSISTENCE")),
        (handover_55[0], ("PENDING_AT_PRECOMMIT_BY_DESIGN", "PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS",
                           "78/78", "Q8", "1/1", "PASS_P062_STEP55_PERSISTENCE")),
    )
    if any(any(token not in " | ".join(row) for token in tokens) for row, tokens in required_rows):
        return {code}
    active_next = active_text.split("## Next Exact Step", 1)
    handover_next = handover_text.split("## Exact Next Action", 1)
    if len(active_next) != 2 or len(handover_next) != 2:
        return {code}
    exact_tokens = ("Step 55 exact-eight", SUBJECT, PARENT, "PASS_P062_STEP55_PERSISTENCE", "Step 56")
    if any(token not in active_next[1] for token in exact_tokens) or any(token not in handover_next[1] for token in exact_tokens):
        return {code}
    stale = ("final Step 54 exact-seven validation", "may Step 55 begin", "Step 55 blocked until Step 54 persistence")
    if any(token in active_next[1] for token in stale) or any(token in handover_next[1] for token in stale):
        return {code}
    return set()


def result_artifact_sha_diagnostics(result_text: str, matrix_bytes: bytes, runtime_bytes: bytes) -> set[str]:
    matrix_matches = re.findall(r"^- matrix content SHA-256: `([0-9a-f]{64})`$", result_text, re.MULTILINE)
    runtime_matches = re.findall(r"^- runtime attestation content SHA-256: `([0-9a-f]{64})`$", result_text, re.MULTILINE)
    if len(matrix_matches) != 1 or len(runtime_matches) != 1 or \
            matrix_matches[0] != sha(matrix_bytes) or runtime_matches[0] != sha(runtime_bytes):
        return {"RESULT_ARTIFACT_SHA_TAMPER"}
    return set()


def markdown_gate() -> None:
    result_bytes = (REPO / RESULT).read_bytes()
    result = result_bytes.decode("utf-8")
    required = ("# Phase 062 Step 55 Code / Runtime Delta Result", "Gate: `PASS_WITH_CONCERNS`",
        "Terminal: `PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS`",
        f"Result-first sentinel: `{SENTINEL}`", "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "required singleton mutation controls: `78/78`", "Q8 frozen `code matched` self-claim: `1/1`",
        "findings P0/P1/P2: `0/5/4`",
        "PASS_P062_STEP55_PERSISTENCE")
    missing = [x for x in required if x not in result]
    if missing:
        raise ValidationError("RESULT_CONTRACT:" + repr(missing))
    sha_codes = result_artifact_sha_diagnostics(
        result, (REPO / MATRIX).read_bytes(), (REPO / ATTESTATION).read_bytes())
    if sha_codes:
        raise ValidationError(",".join(sorted(sha_codes)))
    texts = [(PARENT_LEDGER, (REPO / PARENT_LEDGER).read_text(encoding="utf-8")),
             (ACTIVE_LEDGER, (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8")),
             (HANDOVER, (REPO / HANDOVER).read_text(encoding="utf-8"))]
    tokens = ("Step 54 exact-seven `ce069dde91f1332cc2852312cd2cbccd7cdf38db`",
              "PASS_P062_STEP54_PERSISTENCE", "Step 55",
              "PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS", SENTINEL,
                "78/78", "Q8", "1/1", "0/5/4", "PASS_P062_STEP55_PERSISTENCE")
    for path, text in texts:
        missing = [x for x in tokens if x not in text]
        if missing:
            raise ValidationError(f"CONTROL_CONTRACT:{path}:{missing}")
    codes = current_control_diagnostics(texts[0][1], texts[1][1], texts[2][1])
    if codes:
        raise ValidationError("CONTROL_STATE:" + ",".join(sorted(codes)))


def symbolic_branch(repo: Path) -> str | None:
    cp = proc(["git", "symbolic-ref", "--quiet", "--short", "HEAD"], cwd=repo, timeout=45, text=True)
    if cp.returncode == 1:
        return None
    if cp.returncode:
        raise ValidationError(f"GIT_SYMBOLIC_REF:{cp.returncode}:{cp.stderr.strip()}")
    return cp.stdout.strip()


def precommit_diagnostics(repo: Path, staged: bool, *, branch: str, parent: str,
                          protected_branch: str, protected_tip: str,
                          exact_paths: tuple[str, ...]) -> set[str]:
    current = symbolic_branch(repo)
    if current is None:
        return {"DETACHED_HEAD"}
    head = git_at(repo, ["rev-parse", "HEAD"]).strip()
    if current != branch or head != parent:
        return {"PRECOMMIT_HEAD"}
    local_protected = git_at(repo, ["rev-parse", f"refs/heads/{protected_branch}"], check=False)
    if not isinstance(local_protected, str) or local_protected.strip() != protected_tip:
        return {"LOCAL_PROTECTED_DRIFT"}
    if git_at(repo, ["diff", "--name-only", f"{protected_tip}..HEAD", "--", "Claude"]).strip():
        return {"CLAUDE_DRIFT"}
    expected = set(exact_paths)
    if staged:
        cached = set(filter(None, git_at(repo, ["diff", "--cached", "--name-only"]).splitlines()))
        unstaged = set(filter(None, git_at(repo, ["diff", "--name-only"]).splitlines()))
        untracked = parse_status_paths(repo) - cached - unstaged
        if cached != expected:
            return {"STAGED_EXACT_EIGHT"}
        if unstaged or untracked:
            return {"STAGED_WORKTREE_MISMATCH"}
    else:
        actual = parse_status_paths(repo)
        if actual - expected:
            return {"EXTRA_DIRTY_PATH"}
        if actual != expected:
            return {"WORKTREE_EXACT_EIGHT"}
    return set()


def precommit_gate(staged: bool) -> None:
    codes = precommit_diagnostics(REPO, staged, branch=BRANCH, parent=PARENT,
                                  protected_branch=PROTECTED_BRANCH, protected_tip=PROTECTED,
                                  exact_paths=EXACT_EIGHT)
    if codes:
        raise ValidationError(",".join(sorted(codes)))


def live_ref_at(repo: Path, ref: str) -> str:
    cp = proc(["git", "ls-remote", "origin", ref], cwd=repo, timeout=45, text=True)
    fields = cp.stdout.strip().split() if cp.returncode == 0 else []
    if len(fields) != 2:
        raise ValidationError(f"LS_REMOTE:{ref}:{cp.returncode}")
    return fields[0]


def persistence_diagnostics(repo: Path, *, branch: str, upstream: str, parent_expected: str,
                            subject_expected: str, protected_branch: str, protected_tip: str,
                            main_tip: str, exact_paths: tuple[str, ...]) -> set[str]:
    if parse_status_paths(repo):
        return {"PERSISTENCE_DIRTY"}
    current = symbolic_branch(repo)
    if current is None:
        return {"DETACHED_HEAD"}
    if current != branch:
        return {"PERSISTENCE_BRANCH"}
    local_protected = git_at(repo, ["rev-parse", f"refs/heads/{protected_branch}"], check=False)
    if not isinstance(local_protected, str) or local_protected.strip() != protected_tip:
        return {"LOCAL_PROTECTED_DRIFT"}
    head = git_at(repo, ["rev-parse", "HEAD"]).strip()
    parent = git_at(repo, ["rev-parse", "HEAD^"]).strip()
    subject = git_at(repo, ["show", "-s", "--format=%s", "HEAD"]).strip()
    paths = set(filter(None, git_at(repo, ["show", "--format=", "--name-only", "HEAD"]).splitlines()))
    if parent != parent_expected:
        return {"PERSISTENCE_PARENT_MISMATCH"}
    if subject != subject_expected:
        return {"PERSISTENCE_SUBJECT_MISMATCH"}
    if paths != set(exact_paths):
        return {"PERSISTENCE_EXACT_EIGHT"}
    upstream_tip = git_at(repo, ["rev-parse", upstream], check=False)
    if not isinstance(upstream_tip, str) or not (head == upstream_tip.strip() == live_ref_at(repo, f"refs/heads/{branch}")):
        return {"ACTIVE_REMOTE_DIVERGENCE"}
    if live_ref_at(repo, f"refs/heads/{protected_branch}") != protected_tip:
        return {"PROTECTED_DRIFT"}
    if live_ref_at(repo, "refs/heads/main") != main_tip:
        return {"MAIN_DRIFT"}
    if git_at(repo, ["diff", "--name-only", f"{protected_tip}..HEAD", "--", "Claude"]).strip():
        return {"CLAUDE_DRIFT"}
    return set()


def persistence_gate() -> None:
    codes = persistence_diagnostics(REPO, branch=BRANCH, upstream=UPSTREAM, parent_expected=PARENT,
                                    subject_expected=SUBJECT, protected_branch=PROTECTED_BRANCH,
                                    protected_tip=PROTECTED, main_tip=MAIN, exact_paths=EXACT_EIGHT)
    if codes:
        raise ValidationError(",".join(sorted(codes)))
    print("PASS_P062_STEP55_PERSISTENCE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--no-fresh-runtime", action="store_true")
    args = parser.parse_args()
    matrix, runtime = validate_content(fresh_runtime=not args.no_fresh_runtime)
    print("PASS schema queue=11/11 comparison_endpoints=14/14 dispositions=14/14 counterparts=7/7 adjacent=7/7 static=9/9 consumers=4/4 q8_code_matched=1/1 findings=0/5/4 runtime=5/5")
    if args.run_negative_probes:
        run_negative_controls(matrix, runtime)
    if args.determinism_check:
        builder_determinism()
    if args.content_only:
        print("PASS_P062_STEP55_CONTENT")
        return 0
    markdown_gate()
    if args.verify_persistence:
        persistence_gate()
    else:
        precommit_gate(args.verify_staged)
    print("PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"FAIL_P062_STEP55:{exc}")
        raise SystemExit(1)
