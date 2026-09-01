from __future__ import annotations

import argparse
import ast
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
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_final.py"
ARTIFACT_PATH = "Codex/results/PHASE_066_VALIDATION.json"
REPORT_PATH = "Codex/results/PHASE_066_V1025_V1025_2_LINEAGE_REPORT_I.md"
GATE_PATH = "Codex/results/PHASE_066_STEP_081_2_GATE_RESULT.md"
RESULT_PATH = "Codex/results/PHASE_066_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{ACTIVE_BRANCH}"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT_COMMIT = "bdad7375d70c3734cc63265d94a61dd82afd143d"
SUBJECT = "audit(phase066): close v1025 lineage gate"
GATE = "CONDITIONAL_P066"
PERSISTENCE = "PASS_P066_STEP81_2_PERSISTENCE"
STATUS = "CONDITIONAL_PENDING_PERSISTENCE"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
DIRECT14_RAW_PATH = "Claude/results/comp_v24/sintef_data/sigr.csv"
DIRECT14_RAW_SHA256 = "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6"
DIRECT14_RAW_ROWS = 16735
DIRECT14_BINDING = "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND"
DIRECT14_BINDING_ALIASES = frozenset({DIRECT14_BINDING, "GROUND_NOT_FOUND"})

FINAL_PATHS = [
    VALIDATOR_PATH,
    ARTIFACT_PATH,
    REPORT_PATH,
    GATE_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_PATH_SET = set(FINAL_PATHS)
NONARTIFACT_PATHS = [path for path in FINAL_PATHS if path != ARTIFACT_PATH]
ARTIFACT = ROOT / ARTIFACT_PATH
FINAL_TRANSACTION = [
    ("M", HANDOVER_PATH), ("M", PARENT_LEDGER_PATH), ("M", ACTIVE_LEDGER_PATH),
    ("A", RESULT_PATH), ("A", GATE_PATH), ("A", REPORT_PATH),
    ("A", ARTIFACT_PATH), ("A", VALIDATOR_PATH),
]

ACTIVATION = "f9ee0599ff07d36e4b23547a835549552a51ce26"
STEP76 = "38e00020906e3a024e493c214c1a99a6f8ab07d2"
STEP77 = "5d26e0746864cea7a8bd37a22874093b73c1a12f"
STEP78 = "fedb2031fbfabeaba84f86427c35334526234d73"
STEP79 = "d091e7881f9f22d5dfe9511427afdf4ef22e3280"
STEP80 = "ec02d8e0017c4441d9d02c08e22ad432b8c47bc5"
STEP81_1 = PARENT_COMMIT
PROCESS_TIP = "e3e1a634f34b711aa4803fd190fe9120f1755f13"

REMOTE_HELPER_BYTES = b"""#!/bin/sh
while IFS= read -r command; do
    case "$command" in
        capabilities) printf '\\n' ;;
        list)
            git --git-dir="$PHASE066_FIXTURE_ORIGIN" for-each-ref --format='%(objectname) %(refname)' refs/heads
            printf '\\n'
            ;;
        '') exit 0 ;;
        *) printf '\\n' ;;
    esac
done
"""
STEP76_KNOWN_WARNING = b"<unknown>:5: SyntaxWarning: invalid escape sequence '\\e'\n"

ALLOWED_IMPORT_ROOTS = frozenset({
    "__future__", "argparse", "ast", "copy", "hashlib", "json", "math", "os",
    "pathlib", "re", "shutil", "stat", "subprocess", "sys", "tempfile", "typing",
})
EXPECTED_IMPORTS = (
    ("from", "__future__", ("annotations",)),
    ("import", "argparse", ()),
    ("import", "ast", ()),
    ("import", "copy", ()),
    ("import", "hashlib", ()),
    ("import", "json", ()),
    ("import", "math", ()),
    ("import", "os", ()),
    ("import", "pathlib", ()),
    ("import", "re", ()),
    ("import", "shutil", ()),
    ("import", "stat", ()),
    ("import", "subprocess", ()),
    ("import", "sys", ()),
    ("import", "tempfile", ()),
    ("from", "typing", ("Any",)),
)
FORBIDDEN_CALL_NAMES = frozenset({
    "__import__", "compile", "delattr", "eval", "exec", "getattr", "globals", "locals",
    "open", "setattr", "vars",
})
ALLOWED_CALL_FUNC_TYPES = (ast.Name, ast.Attribute)
MUTATING_CALL_ATTRIBUTES = frozenset({"chmod", "mkdir", "mkdtemp", "replace", "rmtree", "unlink", "write_bytes"})
SENSITIVE_CALL_PIN_COUNT = 125
SENSITIVE_CALL_PIN_SHA256 = {
    "3.12": "21a77c2a272c4a9bf73bc0d705f39259bb82e2134f212263ea225532ea1fa525",
    "3.14": "d9a1e772df0fb5cf679608681c1e53072805f832c3743527f61685aa0320f1db",
}
ALL_CALL_PIN_COUNT = 1246
ALL_CALL_PIN_SHA256 = {
    "3.12": "c9c7ca91bcdcf8f484ca77966e2f6e4239cd77c9bf90ddff6ffa98b406558d96",
    "3.14": "9dce013b690560481a989604ca0ab8c4e22e04142bd3dcec2546d4696e2f15da",
}

HISTORY_BANNER_ALLOWLIST = {
    "ACTIVATION": frozenset({
        "PASS_P066_PLAN_CONTROLS", "PASS_P066_PLAN_DETERMINISM",
        "PASS_P066_PLAN_ACTIVATION_STAGED", "PASS_P066_PLAN_ACTIVATION_PERSISTENCE",
    }),
    "STEP76": frozenset({
        "PASS_P066_STEP76_CONTROLS", "PASS_P066_STEP76_CONTENT",
        "PASS_P066_STEP76_SOURCE_PROCESS", "PASS_P066_STEP76_PERSISTENCE",
    }),
    "STEP77": frozenset({
        "CONDITIONAL_P066_STEP77_FIT_REPLAY_WITH_NONCONVERGED_SELECTED_TRIAL_AND_UNSEALED_PROCESS_LOGS",
        "PASS_P066_STEP77_PERSISTENCE",
    }),
    "STEP78": frozenset({
        "CONDITIONAL_P066_STEP78_VECTOR_BOUND_WITH_ORIGINAL_STATE_GROUND_NOT_FOUND",
        "PASS_P066_STEP78_PERSISTENCE",
    }),
    "STEP79": frozenset({
        "PASS_P066_STEP79_EMPIRICAL_PHYSICAL_SEPARATION", "PASS_P066_STEP79_PERSISTENCE",
    }),
    "STEP80": frozenset({"PASS_P066_STEP80_VALIDATION", "PASS_P066_STEP80_PERSISTENCE"}),
    "STEP81_1": frozenset({
        "PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS", "PASS_P066_STEP81_1_PERSISTENCE",
    }),
}


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def unit(
    name: str,
    commit: str,
    parent: str,
    subject: str,
    validator: str,
    validator_sha256: str,
    result: str,
    result_sha256: str,
    paths: list[str],
    precommit_args: list[str],
    precommit_terminal: str,
    persistence_args: list[str],
    persistence_terminal: str,
) -> dict[str, Any]:
    return {
        "unit": name,
        "commit": commit,
        "parent": parent,
        "subject": subject,
        "validator": validator,
        "validator_sha256": validator_sha256,
        "result": result,
        "result_sha256": result_sha256,
        "paths": paths,
        "precommit_args": precommit_args,
        "precommit_terminal": precommit_terminal,
        "persistence_args": persistence_args,
        "persistence_terminal": persistence_terminal,
    }


UNIT_SPECS = [
    unit(
        "ACTIVATION", ACTIVATION, "a2920fba07ab9ce75191134f0d68ed3b6ffda4e5",
        "docs(phase066): plan v1025 lineage reaudit",
        "Codex/work/v1025_phase066/validate_phase066_plan.py",
        "dd512a46c9ed69a015a8572a4a241e14809c17a5cdfabb101690c6a928c70c89",
        "Codex/results/PHASE_066_PLAN_ACTIVATION_RESULT.md",
        "866a0379e312009d052d36abc8cfecf2c70b6086ff02c462174f4be3e98c59cc",
        [
            "Codex/plans/2026-09-01-phase066-v1025-v1025_2-lineage-detailed-plan.md",
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_PLAN_ACTIVATION_RESULT.md",
            "Codex/results/PHASE_066_PLAN_ACTIVATION_VALIDATION.json",
            "Codex/work/v1025_phase066/validate_phase066_plan.py",
        ],
        ["--verify-staged"], "PASS_P066_PLAN_ACTIVATION_STAGED",
        ["--verify-persistence", "--expected-commit", ACTIVATION],
        "PASS_P066_PLAN_ACTIVATION_PERSISTENCE",
    ),
    unit(
        "STEP76", STEP76, ACTIVATION, "audit(phase066): freeze v1025 source process delta",
        "Codex/work/v1025_phase066/validate_phase066_step76.py",
        "81e49f923c76ea0ee295f13f87df0fe99788f81247321360b8192ff016f5eccb",
        "Codex/results/PHASE_066_STEP_076_SOURCE_PROCESS_RESULT.md",
        "8470965182b7d78504b03f6e992cd7f594f3b1f0874e872b05edd3cb4cf70c44",
        [
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json",
            "Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json",
            "Codex/results/PHASE_066_STEP_076_SOURCE_PROCESS_RESULT.md",
            "Codex/work/v1025_phase066/build_phase066_step76.py",
            "Codex/work/v1025_phase066/validate_phase066_step76.py",
        ],
        ["--verify-staged"], "PASS_P066_STEP76_SOURCE_PROCESS",
        ["--verify-persistence", "--expected-commit", STEP76], "PASS_P066_STEP76_PERSISTENCE",
    ),
    unit(
        "STEP77", STEP77, STEP76, "audit(phase066): reproduce skew direct14 fitting",
        "Codex/work/v1025_phase066/validate_phase066_step77.py",
        "78885534887ca840db1c6b56501f6282256570efcd202053ea2c14b628afe783",
        "Codex/results/PHASE_066_STEP_077_FIT_REPRODUCTION_RESULT.md",
        "15fc643867b3c5bdf9723139af55cbd98f8e4c3bcbee481ae3b8965f57ecf4de",
        [
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json",
            "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json",
            "Codex/results/PHASE_066_STEP_077_FIT_REPRODUCTION_RESULT.md",
            "Codex/work/v1025_phase066/build_phase066_step77.py",
            "Codex/work/v1025_phase066/validate_phase066_step77.py",
        ],
        ["--staged"], "CONDITIONAL_P066_STEP77_FIT_REPLAY_WITH_NONCONVERGED_SELECTED_TRIAL_AND_UNSEALED_PROCESS_LOGS",
        ["--persistence", STEP77], "PASS_P066_STEP77_PERSISTENCE",
    ),
    unit(
        "STEP78", STEP78, STEP77, "audit(phase066): bind optimizer state vector",
        "Codex/work/v1025_phase066/validate_phase066_step78.py",
        "d0e815fef6cbe030158feeabe2b1b8f907ea4c5372b23965eb6e9529f40e01c1",
        "Codex/results/PHASE_066_STEP_078_OPTIMIZER_VECTOR_RESULT.md",
        "118921469ddae612667923405ea843bb732555859312ac1efc013e652bdc8dbb",
        [
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json",
            "Codex/results/PHASE_066_STEP_078_OPTIMIZER_VECTOR_RESULT.md",
            "Codex/work/v1025_phase066/build_phase066_step78.py",
            "Codex/work/v1025_phase066/validate_phase066_step78.py",
        ],
        ["--staged"], "CONDITIONAL_P066_STEP78_VECTOR_BOUND_WITH_ORIGINAL_STATE_GROUND_NOT_FOUND",
        ["--persistence", STEP78], "PASS_P066_STEP78_PERSISTENCE",
    ),
    unit(
        "STEP79", STEP79, STEP78, "audit(phase066): separate fit and material authority",
        "Codex/work/v1025_phase066/validate_phase066_step79.py",
        "4fcfe02c0713b7622236adbd8debd7fc64d1199e5b1bbf87704de4d83c179e69",
        "Codex/results/PHASE_066_STEP_079_AUTHORITY_RESULT.md",
        "0a4441b588d32c24327ff9d26d99dace197dfc8ed637d93970ced3266b986fed",
        [
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json",
            "Codex/results/PHASE_066_STEP_079_AUTHORITY_RESULT.md",
            "Codex/work/v1025_phase066/build_phase066_step79.py",
            "Codex/work/v1025_phase066/validate_phase066_step79.py",
        ],
        ["--staged"], "PASS_P066_STEP79_EMPIRICAL_PHYSICAL_SEPARATION",
        ["--persistence", STEP79], "PASS_P066_STEP79_PERSISTENCE",
    ),
    unit(
        "STEP80", STEP80, STEP79, "audit(phase066): verify profile default temperature routes",
        "Codex/work/v1025_phase066/validate_phase066_step80.py",
        "c79b845b0067b45a25a59180edd061ceaab820a919a0452c735571de9553dfd5",
        "Codex/results/PHASE_066_STEP_080_PROFILE_TEMPERATURE_RESULT.md",
        "22dd0eb4104c4ff10d8055ed44e68cdf9205d71b0afe486291290acd333dea2f",
        [
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json",
            "Codex/results/PHASE_066_RUNTIME_ATTESTATION.json",
            "Codex/results/PHASE_066_STEP_080_PROFILE_TEMPERATURE_RESULT.md",
            "Codex/work/v1025_phase066/build_phase066_step80.py",
            "Codex/work/v1025_phase066/validate_phase066_step80.py",
        ],
        [], "PASS_P066_STEP80_VALIDATION",
        ["--persistence", "--expected-commit", STEP80], "PASS_P066_STEP80_PERSISTENCE",
    ),
    unit(
        "STEP81_1", STEP81_1, STEP80, "audit(phase066): disposition v1025 lineage evidence",
        "Codex/work/v1025_phase066/validate_phase066_step81_dispositions.py",
        "039e57abcb4f2ce5b8edf3bc8c6aeca86a6906c5bb0fb3521bfa40ba2419f76d",
        "Codex/results/PHASE_066_STEP_081_1_DISPOSITION_RESULT.md",
        "f81669d3fd9c0a033ea15c2f7422b997798fd0db44a328ab38519c00ea9e4b17",
        [
            HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH,
            "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json",
            "Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json",
            "Codex/results/PHASE_066_STEP_081_1_DISPOSITION_RESULT.md",
            "Codex/work/v1025_phase066/build_phase066_step81_dispositions.py",
            "Codex/work/v1025_phase066/validate_phase066_step81_dispositions.py",
        ],
        ["--staged"], "PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS",
        ["--persistence", "--expected-commit", STEP81_1], "PASS_P066_STEP81_1_PERSISTENCE",
    ),
]

MACHINE_SPECS = [
    ("Codex/results/PHASE_066_PLAN_ACTIVATION_VALIDATION.json", "00b4cc2f3f184cd17ed4b326d94194e3cd4fb7500277e5b6ca09c160a5f7e841", "d0f5d42b6a404c196541e26e6d7297ac73c5ccd20669230ff2c15e0b8e832101", ACTIVATION),
    ("Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json", "e24462702966dfb679953c6726b20b923eb7cf9591a24ba5297e7b20308f4d2b", "4df7d88cac29b09301645b4477fe30d3952a01abb27a4720a29f347b75b67a1c", STEP76),
    ("Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json", "b419291dca9849e94f1b7e4fa4a3ddc08970385e446dca45f15d469777bcfcfe", "381ae01809a56ac4aa23a786a6170033057df4e838956b535e55bb3bad7e96c3", STEP76),
    ("Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json", "ff8141e7f0d950cfb6f588f41743e7b9221c5f4cb73ecc76522b0beb45a70d80", "567c8b65886851e34fff8e913e6ad81819d8ce022001df6bf20a9b26fce6b029", STEP77),
    ("Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json", "ce8b9b8d6c2941833351f1651ec85b4e9075b96bdcfd1cc93bbc16ccb4e7a6e0", "e56db8c1eb226596d5bee98147444125d030fe969422dd542241eb64692b5a4e", STEP77),
    ("Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json", "d9dead0f766abeed899e7357b964719361054d87e31ded971fb3640b3182656e", "86842e6e53164271b70ae4b9410223b9aa40be4d85692c15f669c5c08a5b7418", STEP78),
    ("Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json", "2bb07774d5ea59b578dcfc1520a3e524ec32b42ca590a90b5cca967ae63499a1", "ccf7a972cd5a061840cf83bd3d6861bd3c840361433245d5fbf75ad3445a62ba", STEP79),
    ("Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json", "7bab3f907ab6879fec0854c94f05e7d0b42fc618d6585f2737750e2a2b1b0695", "da615e36ce8df9d16e8ca7dfb69d1a74137510c1212cf2e2fcb53e8850fc2f75", STEP80),
    ("Codex/results/PHASE_066_RUNTIME_ATTESTATION.json", "a5c909105280cf11a72ca9189070feb59c9005a824eeee4f3e161660394539d4", "3a393149d36513233e46ebbdbb0ce36f0393e28cb88e1fd3704cef5bf83fb040", STEP80),
    ("Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json", "a04e5567b9771b299742fa5f3c2313559f51f32b41ba1844d823b4e0162257de", "005bd904dc3225df1cd82906be5ff08a54e55dbe8f36521520b87a24d7a31569", STEP81_1),
    ("Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json", "847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003", "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6", STEP81_1),
]
MACHINE_SCHEMA_PINS: dict[str, dict[str, Any]] = {
    "Codex/results/PHASE_066_PLAN_ACTIVATION_VALIDATION.json": {"fingerprint_sha256": "af7939e75f5129e996467241294f3d27633957002339208e705c7b3e075940fa", "max_depth": 5, "node_type_counts": {"array": 9, "boolean": 24, "float": 0, "integer": 72, "null": 0, "object": 25, "string": 93}, "nodes": 223},
    "Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json": {"fingerprint_sha256": "dc004b83f470d4c319a5a88470866dbdaee305eb1de3bc9c145528b417e46c5a", "max_depth": 9, "node_type_counts": {"array": 897, "boolean": 344, "float": 0, "integer": 3371, "null": 994, "object": 2289, "string": 10945}, "nodes": 18840},
    "Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json": {"fingerprint_sha256": "a833187311019ede4773898b447b96d09f13fd7f34b1aead3baa958d710a15b0", "max_depth": 7, "node_type_counts": {"array": 1085, "boolean": 370, "float": 0, "integer": 2244, "null": 9, "object": 1219, "string": 4996}, "nodes": 9923},
    "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json": {"fingerprint_sha256": "64327fae3fef71fb772ba6ede9c0ad38ff0a07bab428b6ee6fb5837b70bd43da", "max_depth": 7, "node_type_counts": {"array": 56, "boolean": 48, "float": 1666, "integer": 1532, "null": 0, "object": 50, "string": 134}, "nodes": 3486},
    "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json": {"fingerprint_sha256": "a63b4f2fa6638858590697beab9df56c4941ec6c7130316774b81833c78db690", "max_depth": 5, "node_type_counts": {"array": 14, "boolean": 1, "float": 21, "integer": 33, "null": 0, "object": 21, "string": 99}, "nodes": 189},
    "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json": {"fingerprint_sha256": "5025e28b33ca8ce1fcb41d3421af16fbc233aad731addda95b2a80f168a50c81", "max_depth": 6, "node_type_counts": {"array": 58, "boolean": 13, "float": 294, "integer": 259, "null": 2, "object": 104, "string": 224}, "nodes": 954},
    "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json": {"fingerprint_sha256": "67796fe19fa71d3fc664548744e81ec4fb0aace531baeb7c688e8412742e5fd8", "max_depth": 6, "node_type_counts": {"array": 20, "boolean": 69, "float": 40, "integer": 34, "null": 0, "object": 145, "string": 571}, "nodes": 879},
    "Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json": {"fingerprint_sha256": "2f47797f6dca9185556ce69df1aa6e5943249932a30ea612e430b88d430606e2", "max_depth": 6, "node_type_counts": {"array": 33, "boolean": 202, "float": 75, "integer": 122, "null": 33, "object": 103, "string": 324}, "nodes": 892},
    "Codex/results/PHASE_066_RUNTIME_ATTESTATION.json": {"fingerprint_sha256": "40f09fe189601deb8a643e4804965a8bfe6d33e6bb955cd55815b124a35ed3ab", "max_depth": 8, "node_type_counts": {"array": 157, "boolean": 435, "float": 1244, "integer": 450, "null": 66, "object": 570, "string": 1310}, "nodes": 4232},
    "Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json": {"fingerprint_sha256": "8463be77912b0fecb16c3686de09c15b5bccfb9fb59bd143eb9268f97b9c1fab", "max_depth": 8, "node_type_counts": {"array": 1613, "boolean": 666, "float": 0, "integer": 3288, "null": 1, "object": 1505, "string": 11426}, "nodes": 18499},
    "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json": {"fingerprint_sha256": "a991e6756ac65f86112140978a3bef511891da081f3ba35ee41a976c61dfa246", "max_depth": 10, "node_type_counts": {"array": 1175, "boolean": 1239, "float": 0, "integer": 1747, "null": 189, "object": 1851, "string": 10595}, "nodes": 16796},
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, "E_DUPLICATE_JSON", key)
        output[key] = value
    return output


def reject_constant(value: str) -> None:
    raise ValidationError("E_NONFINITE_JSON", value)


def strict_load_bytes(raw: bytes, label: str) -> tuple[Any, dict[str, int]]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_constant=reject_constant)
    except ValidationError:
        raise
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError("E_STRICT_JSON", label) from error
    nodes = 0
    scalars = 0
    depth_max = 0

    def walk(item: Any, depth: int = 0) -> None:
        nonlocal nodes, scalars, depth_max
        nodes += 1
        depth_max = max(depth_max, depth)
        if isinstance(item, dict):
            for key, child in item.items():
                require(type(key) is str, "E_JSON_KEY", label)
                walk(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                walk(child, depth + 1)
        else:
            scalars += 1
            if isinstance(item, float):
                require(math.isfinite(item), "E_NONFINITE_JSON", label)

    walk(value)
    return value, {"nodes": nodes, "scalars": scalars, "depth": depth_max + 1}


def recursive_schema_topology(value: Any) -> dict[str, Any]:
    tokens: list[str] = []
    counts = {"array": 0, "boolean": 0, "float": 0, "integer": 0,
              "null": 0, "object": 0, "string": 0}
    max_depth = 0

    def escape(key: str) -> str:
        return key.replace("~", "~0").replace("/", "~1")

    def visit(item: Any, pointer: str, depth: int) -> None:
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        if isinstance(item, dict):
            counts["object"] += 1
            keys = sorted(item)
            tokens.append(pointer + "|object|" + canonical_bytes(keys).decode("utf-8"))
            for key in keys:
                visit(item[key], pointer + "/" + escape(key), depth + 1)
        elif isinstance(item, list):
            counts["array"] += 1
            tokens.append(pointer + f"|array|{len(item)}")
            for index, child in enumerate(item):
                visit(child, pointer + f"/{index}", depth + 1)
        else:
            kind = "null" if item is None else "boolean" if type(item) is bool \
                else "integer" if type(item) is int else "float" if type(item) is float else "string"
            counts[kind] += 1
            tokens.append(pointer + "|" + kind)
    visit(value, "", 0)
    return {
        "fingerprint_sha256": sha256(("\n".join(tokens) + "\n").encode("utf-8")),
        "node_type_counts": counts,
        "nodes": len(tokens),
        "max_depth": max_depth + 1,
    }


def semantic_hash(document: dict[str, Any]) -> str:
    projection = copy.deepcopy(document)
    projection.pop("semantic_sha256", None)
    return sha256(canonical_bytes(projection))


def predecessor_semantic_hash(document: dict[str, Any]) -> str:
    projection = copy.deepcopy(document)
    projection["semantic_sha256"] = ""
    return sha256(pretty_bytes(projection))


def is_fixture_location(path: pathlib.Path) -> bool:
    resolved = path.resolve()
    temp = pathlib.Path(tempfile.gettempdir()).resolve()
    return temp in resolved.parents and any(
        part.startswith(("phase066-step812-history-", "phase066-step812-migration-control-"))
        for part in resolved.parts
    )


def validate_execution_argv(argv: list[str], cwd: pathlib.Path) -> None:
    require(type(argv) is list and argv and all(type(item) is str and item for item in argv),
            "E_SOURCE_POLICY_ARGV", repr(argv))
    launcher = pathlib.Path(argv[0]).name.lower()
    if launcher in {"git", "git.exe"}:
        require(argv[0] in {"git", "git.exe"}, "E_SOURCE_POLICY_GIT_LAUNCHER", argv[0])
        args = argv[1:]
        require(args, "E_SOURCE_POLICY_GIT", "missing args")
        fixture = is_fixture_location(cwd)
        if args[0] == "--git-dir":
            require(len(args) >= 4 and args[2] == "update-ref", "E_SOURCE_POLICY_GIT", repr(args))
            git_dir = pathlib.Path(args[1]).resolve()
            require(is_fixture_location(git_dir) and fixture,
                    "E_SOURCE_POLICY_GIT_DIR", str(git_dir))
            command = "update-ref"
        else:
            command = args[0]
        require(command in {
            "branch", "checkout", "clone", "config", "diff", "diff-tree", "log", "ls-files",
            "ls-remote", "ls-tree", "remote", "rev-list", "rev-parse", "show", "status", "update-ref",
        }, "E_SOURCE_POLICY_GIT", command)
        lowered = [item.lower() for item in args]
        require(not any(item in {"-c", "--config-env", "--exec-path", "--upload-pack", "--receive-pack"}
                        or item.startswith(("alias.", "protocol.")) or "ext::" in item for item in lowered),
                "E_SOURCE_POLICY_GIT_ESCAPE", repr(args))
        write_command = command in {"checkout", "clone", "config", "update-ref"} \
            or (command == "remote" and len(args) > 1 and args[1] == "set-url")
        require(not write_command or fixture, "E_SOURCE_POLICY_ROOT_GIT_WRITE", repr(args))
        if command == "clone":
            require(len(args) == 5 and args[1:3] in (["--bare", "--shared"], ["--shared", "--no-checkout"])
                    and pathlib.Path(args[3]).resolve() == ROOT.resolve()
                    and is_fixture_location(pathlib.Path(args[4])),
                    "E_SOURCE_POLICY_GIT_CLONE", repr(args))
        elif command == "config":
            require(tuple(args) in {
                ("config", "core.autocrlf", "false"),
                ("config", "remote.origin.vcs", "phase066"),
                ("config", f"branch.{ACTIVE_BRANCH}.remote", "origin"),
                ("config", f"branch.{ACTIVE_BRANCH}.merge", f"refs/heads/{ACTIVE_BRANCH}"),
            }, "E_SOURCE_POLICY_GIT_CONFIG", repr(args))
        elif command == "remote" and len(args) > 1 and args[1] == "set-url":
            require(args == ["remote", "set-url", "origin", ORIGIN_URL],
                    "E_SOURCE_POLICY_GIT_REMOTE_WRITE", repr(args))
        elif command == "checkout":
            commits = {spec["commit"] for spec in UNIT_SPECS} | {spec["parent"] for spec in UNIT_SPECS}
            require((len(args) == 4 and args[1:3] == ["-B", ACTIVE_BRANCH] and args[3] in commits)
                    or (len(args) >= 4 and args[1] in commits and args[2] == "--"
                        and args[3:] in [spec["paths"] for spec in UNIT_SPECS]),
                    "E_SOURCE_POLICY_GIT_CHECKOUT", repr(args))
        elif command == "update-ref":
            update_args = args[3:] if args[0] == "--git-dir" else args[1:]
            require(len(update_args) == 2 and update_args[0] in {
                f"refs/remotes/origin/{ACTIVE_BRANCH}", f"refs/heads/{PROTECTED_BRANCH}",
                f"refs/remotes/origin/{PROTECTED_BRANCH}", "refs/remotes/origin/main",
                "refs/heads/phase066-fixture-process-tip", f"refs/heads/{ACTIVE_BRANCH}",
                f"refs/heads/{PROTECTED_BRANCH}", "refs/heads/main",
            } and re.fullmatch(r"[0-9a-f]{40}", update_args[1]) is not None,
                    "E_SOURCE_POLICY_GIT_UPDATE_REF", repr(args))
        return
    require(pathlib.Path(argv[0]).resolve() == pathlib.Path(sys.executable).resolve(),
            "E_SOURCE_POLICY_PYTHON", argv[0])
    scripts = [item for item in argv[1:] if item.endswith(".py")]
    require(len(scripts) == 1 and scripts[0] in {spec["validator"] for spec in UNIT_SPECS},
            "E_SOURCE_POLICY_PYTHON_SCRIPT", repr(scripts))
    require("-c" not in argv and "-m" not in argv, "E_SOURCE_POLICY_DYNAMIC_PYTHON", repr(argv))
    require(is_fixture_location(cwd), "E_SOURCE_POLICY_PYTHON_CWD", str(cwd))
    resolved = (cwd / scripts[0]).resolve()
    require(cwd.resolve() in resolved.parents, "E_SOURCE_POLICY_PYTHON_ESCAPE", str(resolved))


def run_process(
    argv: list[str], *, cwd: pathlib.Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    validate_execution_argv(argv, cwd)
    process = subprocess.run(
        argv, cwd=cwd, env=env, capture_output=True, check=False, shell=False, timeout=timeout,
    )
    if check and process.returncode != 0:
        detail = process.stderr.decode("utf-8", errors="replace")[-2000:]
        raise ValidationError("E_PROCESS", f"{argv!r}: {detail}")
    return process


def git(
    args: list[str], *, cwd: pathlib.Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, env=env, timeout=timeout, check=check)


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT, env: dict[str, str] | None = None) -> str:
    return git(args, cwd=cwd, env=env).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str, *, cwd: pathlib.Path = ROOT) -> bytes:
    return git(["show", f"{commit}:{path}"], cwd=cwd).stdout


def nul_paths(raw: bytes) -> set[str]:
    return {part.decode("utf-8") for part in raw.split(b"\0") if part}


def name_status_records(raw: bytes) -> list[dict[str, str]]:
    parts = [part.decode("utf-8") for part in raw.split(b"\0") if part]
    require(len(parts) % 2 == 0, "E_NAME_STATUS_ENCODING", repr(parts[-2:]))
    records = [
        {"status": parts[index], "path": parts[index + 1]}
        for index in range(0, len(parts), 2)
    ]
    require(all(record["status"] in {"A", "M"} for record in records),
            "E_NAME_STATUS_KIND", repr(records))
    return records


def exact_modes(commit: str, paths: list[str], *, cwd: pathlib.Path = ROOT) -> dict[str, str]:
    raw = git(["ls-tree", "-z", commit, "--", *paths], cwd=cwd).stdout
    modes: dict[str, str] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, encoded_path = item.split(b"\t", 1)
        mode, object_type, _ = metadata.decode("ascii").split()
        path = encoded_path.decode("utf-8")
        require(object_type == "blob" and path not in modes, "E_PATH_MODE_OBJECT", path)
        modes[path] = mode
    require(set(modes) == set(paths), "E_PATH_MODE_PATHS", repr(sorted(modes)))
    return modes


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT, env: dict[str, str] | None = None) -> str:
    line = git_text(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"], cwd=cwd, env=env)
    fields = line.split()
    require(len(fields) == 2 and re.fullmatch(r"[0-9a-f]{40}", fields[0]) is not None,
            "E_LIVE_REF", branch)
    return fields[0]


def validate_source_policy_text(source: str, label: str) -> int:
    try:
        tree = ast.parse(source, filename=label)
    except SyntaxError as error:
        raise ValidationError("E_SOURCE_POLICY_PARSE", label) from error
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    import_forms: list[tuple[str, str, tuple[str, ...]]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            require(isinstance(parents.get(node), ast.Module), "E_SOURCE_POLICY_IMPORT_SCOPE", label)
    for node in tree.body:
        if isinstance(node, ast.Import):
            require(len(node.names) == 1 and node.names[0].asname is None,
                    "E_SOURCE_POLICY_IMPORT_ALIAS", label)
            import_forms.append(("import", node.names[0].name, ()))
        elif isinstance(node, ast.ImportFrom):
            require(node.level == 0 and node.module is not None
                    and all(alias.asname is None and alias.name != "*" for alias in node.names),
                    "E_SOURCE_POLICY_IMPORT_ALIAS", label)
            import_forms.append(("from", node.module, tuple(alias.name for alias in node.names)))
    require(tuple(import_forms) == EXPECTED_IMPORTS, "E_SOURCE_POLICY_IMPORT_ORDER", repr(import_forms))

    def owner(node: ast.AST) -> str:
        current = node
        while current in parents:
            current = parents[current]
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return current.name
        return "<module>"

    def attribute_chain(node: ast.AST) -> tuple[str, ...] | None:
        parts: list[str] = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return tuple(reversed(parts))
        return None

    declared_calls = {
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    } | {
        "SystemExit", "all", "any", "bool", "enumerate", "frozenset", "isinstance", "len",
        "max", "print", "range", "repr", "reversed", "set", "sorted", "str", "sum",
        "super", "tuple", "type", "zip",
    }
    sensitive_observed: list[str] = []
    all_calls_observed: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            require(all(alias.name.split(".", 1)[0] in ALLOWED_IMPORT_ROOTS and alias.asname is None
                        for alias in node.names), "E_SOURCE_POLICY_IMPORT", label)
        elif isinstance(node, ast.ImportFrom):
            require(node.level == 0 and node.module is not None
                    and node.module.split(".", 1)[0] in ALLOWED_IMPORT_ROOTS
                    and all(alias.asname is None and alias.name != "*" for alias in node.names),
                    "E_SOURCE_POLICY_IMPORT_FROM", label)
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            value = node.value
            chain = attribute_chain(value) if isinstance(value, ast.Attribute) else None
            require(chain not in {("subprocess", "run"), ("os", "replace"), ("shutil", "rmtree")},
                    "E_SOURCE_POLICY_SENSITIVE_ALIAS", repr(chain))
        elif isinstance(node, ast.Attribute):
            standard_exception_init = (
                node.attr == "__init__" and owner(node) == "__init__"
                and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "super" and not node.value.args and not node.value.keywords
            )
            require(not node.attr.startswith("__") or standard_exception_init,
                    "E_SOURCE_POLICY_DUNDER", node.attr)
        elif isinstance(node, ast.Call):
            func_type = "Name" if isinstance(node.func, ast.Name) else (
                "Attribute" if isinstance(node.func, ast.Attribute) else "OTHER"
            )
            require(isinstance(node.func, ALLOWED_CALL_FUNC_TYPES),
                    "E_SOURCE_POLICY_CALL_FUNC_TYPE", func_type)
            call_signature = owner(node) + "|" + ast.dump(node, annotate_fields=True, include_attributes=False)
            all_calls_observed.append(sha256(call_signature.encode("utf-8")))
            if isinstance(node.func, ast.Name):
                require(node.func.id not in FORBIDDEN_CALL_NAMES, "E_SOURCE_POLICY_CALL", node.func.id)
                require(node.func.id in declared_calls, "E_SOURCE_POLICY_CALL_NAME", node.func.id)
            if isinstance(node.func, ast.Attribute):
                attribute = node.func.attr
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and attribute == "run":
                    require(owner(node) == "run_process", "E_SOURCE_POLICY_SUBPROCESS_OWNER", owner(node))
                    shell_values = [keyword.value for keyword in node.keywords if keyword.arg == "shell"]
                    require(len(shell_values) == 1 and isinstance(shell_values[0], ast.Constant)
                            and shell_values[0].value is False, "E_SOURCE_POLICY_SHELL", label)
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and attribute == "replace":
                    require(owner(node) in {"atomic_collect", "atomic_migrate_stored_history"},
                            "E_SOURCE_POLICY_REPLACE_OWNER", owner(node))
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "shutil" and attribute == "rmtree":
                    require(owner(node) == "remove_temp_tree", "E_SOURCE_POLICY_RMTREE_OWNER", owner(node))
                if attribute in {"chmod", "mkdir", "unlink", "write_bytes"}:
                    allowed_owner = owner(node) in {
                        "atomic_collect", "atomic_migrate_stored_history", "configure_fixture_refs",
                        "make_historical_clone", "migration_transaction_controls", "remove_temp_tree",
                    }
                    require(allowed_owner, "E_SOURCE_POLICY_MUTATION_OWNER", f"{attribute}:{owner(node)}")
                require(attribute not in {"system", "popen"}, "E_SOURCE_POLICY_SHELL", attribute)
            chain = attribute_chain(node.func) if isinstance(node.func, ast.Attribute) else None
            sensitive = (
                isinstance(node.func, ast.Name)
                and node.func.id in {"git", "git_blob", "git_text", "live_tip", "run_process"}
            ) or chain in {("subprocess", "run"), ("os", "replace"), ("shutil", "rmtree"), ("tempfile", "mkdtemp")} \
                or (isinstance(node.func, ast.Attribute) and node.func.attr in {"chmod", "mkdir", "unlink", "write_bytes"})
            if sensitive:
                signature = owner(node) + "|" + ast.dump(node, annotate_fields=True, include_attributes=False)
                digest = sha256(signature.encode("utf-8"))
                sensitive_observed.append(digest)
        elif isinstance(node, ast.Lambda):
            require(False, "E_SOURCE_POLICY_LAMBDA", label)
    runtime_key = f"{sys.version_info.major}.{sys.version_info.minor}"
    require(runtime_key in SENSITIVE_CALL_PIN_SHA256 and runtime_key in ALL_CALL_PIN_SHA256,
            "E_SOURCE_POLICY_RUNTIME", runtime_key)
    require(len(sensitive_observed) == SENSITIVE_CALL_PIN_COUNT
            and sha256(canonical_bytes(sorted(sensitive_observed))) == SENSITIVE_CALL_PIN_SHA256[runtime_key],
            "E_SOURCE_POLICY_SENSITIVE_CALL_COUNTS",
            f"count={len(sensitive_observed)} sha={sha256(canonical_bytes(sorted(sensitive_observed)))}")
    require(len(all_calls_observed) == ALL_CALL_PIN_COUNT
            and sha256(canonical_bytes(sorted(all_calls_observed))) == ALL_CALL_PIN_SHA256[runtime_key],
            "E_SOURCE_POLICY_CALL_GRAPH",
            f"count={len(all_calls_observed)} sha={sha256(canonical_bytes(sorted(all_calls_observed)))}")
    return sum(1 for _ in ast.walk(tree))


def validate_source_policy() -> int:
    source = (ROOT / VALIDATOR_PATH).read_text(encoding="utf-8")
    return validate_source_policy_text(source, VALIDATOR_PATH)


def strict_json_controls() -> tuple[int, int]:
    cases = [
        (b'{"a":1,"a":2}', "E_DUPLICATE_JSON"),
        (b'{"a":NaN}', "E_NONFINITE_JSON"),
        (b'{"a":Infinity}', "E_NONFINITE_JSON"),
        (b'{"a":-Infinity}', "E_NONFINITE_JSON"),
        (b'\xff', "E_STRICT_JSON"),
        (b'{"a":1} trailing', "E_STRICT_JSON"),
    ]
    passed = 0
    for raw, expected in cases:
        try:
            strict_load_bytes(raw, "negative")
        except ValidationError as error:
            require(error.code == expected, "E_STRICT_CONTROL_CODE", f"{error.code}!={expected}")
            passed += 1
        else:
            raise ValidationError("E_STRICT_CONTROL_ACCEPTED", expected)
    return passed, len(cases)


def source_policy_controls() -> tuple[int, int]:
    baseline = (ROOT / VALIDATOR_PATH).read_text(encoding="utf-8")
    marker = '\nif __name__ == "__main__":\n'
    require(baseline.count(marker) == 1, "E_SOURCE_POLICY_CONTROL_MARKER")
    cases = [
        ("direct_root_git_write", "\ngit(['update-ref', 'refs/heads/x', '0' * 40])\n",
         "E_SOURCE_POLICY_SENSITIVE_CALL_COUNTS"),
        ("subprocess_alias", "\nrunner = subprocess.run\nrunner(['git', 'status'])\n",
         "E_SOURCE_POLICY_SENSITIVE_ALIAS"),
        ("replace_alias", "\nmover = os.replace\nmover('a', 'b')\n",
         "E_SOURCE_POLICY_SENSITIVE_ALIAS"),
        ("indirect_callable", "\nfs = [print]\nfs[0]()\n", "E_SOURCE_POLICY_CALL_FUNC_TYPE"),
        ("nested_import", "\ndef nested_import_probe():\n    import subprocess\n",
         "E_SOURCE_POLICY_IMPORT_SCOPE"),
    ]
    passed = 0
    for name, payload, expected in cases:
        source = baseline.replace(marker, payload + marker)
        try:
            validate_source_policy_text(source, f"negative-{name}")
        except ValidationError as error:
            require(error.code == expected, "E_SOURCE_POLICY_CONTROL_CODE",
                    f"{name}:{error.code}!={expected}")
            passed += 1
        else:
            raise ValidationError("E_SOURCE_POLICY_CONTROL_ACCEPTED", name)
    return passed, len(cases)


def load_machine_artifacts() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    documents: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    total = {"nodes": 0, "scalars": 0, "depth": 0}
    for path, raw_pin, semantic_pin, owning_commit in MACHINE_SPECS:
        raw = (ROOT / path).read_bytes()
        require(sha256(raw) == raw_pin, "E_MACHINE_RAW_SHA256", path)
        value, traversal = strict_load_bytes(raw, path)
        require(type(value) is dict, "E_MACHINE_OBJECT", path)
        require(pretty_bytes(value) == raw.replace(b"\r\n", b"\n"), "E_MACHINE_CANONICAL", path)
        require(value.get("semantic_sha256") == semantic_pin
                and semantic_pin in {predecessor_semantic_hash(value), semantic_hash(value)},
                "E_MACHINE_SEMANTIC", path)
        require(git_blob(owning_commit, path) == raw, "E_MACHINE_OWNING_COMMIT_BYTES", path)
        topology = recursive_schema_topology(value)
        require(path in MACHINE_SCHEMA_PINS and topology == MACHINE_SCHEMA_PINS[path],
                "E_MACHINE_SCHEMA_TOPOLOGY", f"{path}:{topology}")
        documents[path] = value
        total["nodes"] += traversal["nodes"]
        total["scalars"] += traversal["scalars"]
        total["depth"] = max(total["depth"], traversal["depth"])
        records.append({
            "path": path,
            "owning_commit": owning_commit,
            "raw_sha256": raw_pin,
            "semantic_sha256": semantic_pin,
            "traversal": traversal,
            "recursive_schema_topology": topology,
        })
    return documents, records, total


def validate_predecessor_commits() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in UNIT_SPECS:
        commit = spec["commit"]
        parents = git_text(["rev-list", "--parents", "-n", "1", commit]).split()
        require(parents == [commit, spec["parent"]], "E_HISTORY_PARENT", spec["unit"])
        require(git_text(["show", "-s", "--format=%s", commit]) == spec["subject"],
                "E_HISTORY_SUBJECT", spec["unit"])
        changed = name_status_records(git([
            "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-r", "-z", commit,
        ]).stdout)
        expected_status = [
            {"status": "M" if path in {HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH} else "A",
             "path": path}
            for path in sorted(spec["paths"])
        ]
        require(changed == expected_status, "E_HISTORY_PATHS", f"{spec['unit']}:{changed}")
        modes = exact_modes(commit, spec["paths"])
        require(all(mode == "100644" for mode in modes.values()), "E_HISTORY_PATH_MODES", spec["unit"])
        validator_raw = git_blob(commit, spec["validator"])
        result_raw = git_blob(commit, spec["result"])
        require(sha256(validator_raw) == spec["validator_sha256"], "E_HISTORY_VALIDATOR_SHA", spec["unit"])
        require(sha256(result_raw) == spec["result_sha256"], "E_HISTORY_RESULT_SHA", spec["unit"])
        require((ROOT / spec["validator"]).read_bytes() == validator_raw,
                "E_HISTORY_VALIDATOR_CURRENT_BYTES", spec["unit"])
        require((ROOT / spec["result"]).read_bytes() == result_raw,
                "E_HISTORY_RESULT_CURRENT_BYTES", spec["unit"])
        records.append({
            "unit": spec["unit"], "commit": commit, "parent": spec["parent"],
            "subject": spec["subject"], "paths": spec["paths"], "name_status": changed,
            "modes": modes,
            "validator_path": spec["validator"], "validator_sha256": spec["validator_sha256"],
            "result_path": spec["result"], "result_sha256": spec["result_sha256"],
        })
    return records


def validate_cross_semantics(documents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source = documents["Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json"]
    read = documents["Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json"]
    fit = documents["Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"]
    provenance = documents["Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"]
    optimizer = documents["Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"]
    authority = documents["Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json"]
    profile = documents["Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"]
    runtime = documents["Codex/results/PHASE_066_RUNTIME_ATTESTATION.json"]
    disposition = documents["Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json"]
    carry = documents["Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"]

    summary = source["source_summary"]
    require((summary["occurrences"], summary["unique_blobs"], summary["unique_text_lines"],
             summary["unique_pdf_pages"]) == (433, 167, 30597, 308), "E_SOURCE_DENOMINATOR")
    require(summary["unique_review_modes"] == {"FULL_IMAGE": 3, "FULL_PDF": 6, "FULL_TEXT": 158},
            "E_SOURCE_MODES")
    require(summary["versions"] == {"v1.0.25": 143, "v1.0.25.1": 144, "v1.0.25.2": 146},
            "E_SOURCE_VERSIONS")
    require((summary["path_set_sha256"], summary["path_blob_sha256"], summary["unique_blob_sha256"]) == (
        "3c9bf954a5db4df5ce01a96ff8834f9e9284e6e35fdcecbfae0c3ae6b430b382",
        "b3620bf1a76758cad818e9ea7ece5441ea88b86f8f030bb715f48e054086655c",
        "f1982cf050f88b7145d5ea1a6afdf124316da1332afec9028ae6119730080bfa",
    ), "E_SOURCE_HASH_BINDING")
    require(source["narrative"]["expanded_documents"] == 42
            and source["narrative"]["expanded_lines"] == 9674
            and len(source["stale_pdf_pairs"]) == 3, "E_SOURCE_NARRATIVE")
    pairwise = [
        (row["from_version"], row["to_version"], row["counts"])
        for row in source["pairwise_deltas"]
    ]
    require(pairwise == [
        ("v1.0.25", "v1.0.25.1", {"added": 1, "changed": 10, "removed": 0, "same": 133, "shared": 143}),
        ("v1.0.25.1", "v1.0.25.2", {"added": 2, "changed": 11, "removed": 0, "same": 133, "shared": 144}),
        ("v1.0.25", "v1.0.25.2", {"added": 3, "changed": 16, "removed": 0, "same": 127, "shared": 143}),
    ], "E_PAIRWISE_DELTA")
    coverage = read["coverage_summary"]
    require((coverage["source_occurrences_read"], coverage["source_occurrences_total"],
             coverage["unique_blobs_read"], coverage["unique_blobs_total"],
             coverage["text_blobs"], coverage["text_lines"], coverage["pdf_blobs"],
             coverage["pdf_pages"], coverage["image_blobs"], coverage["images_visual_inspected"],
             coverage["release_commits"], coverage["routed_commits"], coverage["routing_intent_ids"])
            == (433, 433, 167, 167, 158, 30597, 6, 308, 3, 3, 17, 20, 105),
            "E_READ_COVERAGE")
    require(all(coverage[key] == 0 for key in (
        "inspection_errors", "output_truncation_unresolved", "routing_duplicate_ids",
        "source_occurrence_orphans", "unique_blobs_partial", "unique_blobs_unread",
        "unread_process_diffs",
    )), "E_READ_GAPS")

    raw_input = provenance["raw_input"]
    processed = provenance["processed_input"]
    contract = provenance["optimizer_contract"]
    require((raw_input["path"], raw_input["raw_sha256"], raw_input["data_rows"],
             raw_input["capacity_basis"], raw_input["specimen_protocol_status"]) == (
        "Claude/results/comp_v24/sintef_data/sigr.csv",
        "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6",
        16735, "absolute_mAh_not_mass_normalized",
        "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND",
    ), "E_RAW_INPUT_BINDING")
    require(len(raw_input["ground_not_found"]) == 3, "E_RAW_INPUT_GROUND_NOT_FOUND")
    require((processed["points"], processed["V_sha256"], processed["D_sha256"]) == (
        1280, "6c7ca15d7b9eaf80561d2d2d834856c9b3076f31f6d7e4e6ce304ddb266020b4",
        "713c1de666d84e29edd55fbaab5b6321bfe505fb25cfe03c0b727a88bce743ce",
    ), "E_PROCESSED_INPUT")
    require((contract["components"], len(contract["parameter_order"]), contract["max_nfev"],
             contract["seed_strategies"] * contract["restarts_per_strategy"], contract["start_matrix_sha256"])
            == (14, 5, 6000, 12, "3d5c9a7b04cfbd4a6773d9d45d64f46cb342b9adadc790960cc9264d71122ead"),
            "E_OPTIMIZER_CONTRACT")
    require(contract["parameter_order"] == ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"]
            and contract["bounds_sha256"] == {
                "lower": "56a35d64e713853ca0fb0a72dfc1c787f0ea36790b08d406a5faa0df5545e796",
                "upper": "0bea5037639ce74c22f20f45e0def0a2d57bca053467ab04cef671d839ad7517",
            } and contract["objective"] == "source_explicit_unweighted_residual=model(V)-D",
            "E_OPTIMIZER_ORDER_BOUNDS_OBJECTIVE")
    require(fit["mathematical_rederivation"]["analytic_derivative"]
            == "dxi/dV=d*(alpha/w)*sigma**alpha*(1-sigma)"
            and fit["mathematical_rederivation"]["parameter_order"] == contract["parameter_order"],
            "E_FIT_DERIVATIVE_ORDER")
    require(fit["optimizer_execution_complete"] is True and fit["runtime_success"] is False
            and fit["selected_trial_converged"] is False, "E_FIT_STATUS")
    require(fit["comparison"]["ordered_parameter_exact_reproduction"] is False
            and fit["comparison"]["runtime_curve_agreement_pass"] is True
            and fit["comparison"]["runtime_numerical_agreement_pass"] is True,
            "E_FIT_COMPARISON")
    require(fit["stored_evidence"]["original_full_precision_optimizer_state"] == "GROUND_NOT_FOUND"
            and fit["stored_evidence"]["original_optimizer_diagnostics_and_environment"] == "GROUND_NOT_FOUND",
            "E_FIT_ORIGINAL_STATE")

    require(optimizer["parameter_contract"]["count"] == 57
            and len(optimizer["original_optimizer_state_availability"]) == 25
            and all(row.get("status") == "GROUND_NOT_FOUND"
                    for row in optimizer["original_optimizer_state_availability"]),
            "E_OPTIMIZER_ORIGINAL_25")
    curve = optimizer["curve_objective_classification"]
    require((curve["ordered_parameter_vectors_vs_stored"], curve["replay_vs_stored_curve"],
             curve["python3.12_vs_python3.14_curve"], curve["original_historical_curve_and_objective"])
            == ("NOT_EQUIVALENT", "TOLERANCE_EQUIVALENT", "IDENTICAL", "GROUND_NOT_FOUND"),
            "E_OPTIMIZER_CLASSIFICATION")
    require(all(value is False for value in optimizer["authority_ceiling"].values()),
            "E_OPTIMIZER_AUTHORITY")

    require(authority["aggregate"] == {
        "empirical_pass_true": 1, "external_authority_true": 0, "held_out_not_tested": 6,
        "phase_authority_true": 0, "physical_authority_true": 0,
        "primary_text_ground_not_found": 1, "proposition_authority_true": 0, "rows": 8,
    }, "E_AUTHORITY_AGGREGATE")
    require(len(authority["claim_rows"]) == 8
            and sum(row["empirical_pass"] is True for row in authority["claim_rows"]) == 1
            and all(row[key] is False for row in authority["claim_rows"]
                    for key in ("external_authority", "phase_authority", "proposition_authority", "physical_authority")),
            "E_AUTHORITY_ROWS")
    require(all(value is False for value in authority["authority_ceiling"].values()),
            "E_AUTHORITY_CEILING")

    require(profile["aggregate"] == {
        "external_authority_true": 0, "multi_temperature_experimental_authority_true": 0,
        "profile_selection_authority_true": 0, "public_and_explicit_routes": 13,
        "route_rows": 16, "serialized_routes": 3, "temperature_dependent": 9,
        "temperature_independent": 7,
    }, "E_PROFILE_AGGREGATE")
    defaults = profile["default_adjudication"]
    require(defaults["fresh_public_default"] == "GRAPHITE_STAGING_LIT_4_PLUS_SIC_LIT_2"
            and defaults["fresh_public_default_temperature_dependent"] is True
            and defaults["skew_7_7_status"] == "EXPLICIT_OR_TOGGLE_OPT_IN_ONLY"
            and defaults["skew_7_7_temperature_dependent"] is False
            and defaults["global_order_leakage_observed"] is False
            and defaults["test_mutated_default_is_public_default"] is False,
            "E_PROFILE_DEFAULT")
    require(runtime["aggregate"]["route_runs"] == 32 and runtime["aggregate"]["order_runs"] == 4
            and runtime["aggregate"]["successful_processes"] == 36
            and runtime["aggregate"]["stderr_empty"] == 36
            and runtime["aggregate"]["order_restoration_pass"] is True,
            "E_RUNTIME_AGGREGATE")

    require(disposition["counts"] == {
        "distribution": {"CORRECT": 3, "PRESERVE": 424, "WITHHOLD": 6},
        "source_occurrences": 433, "supplemental": 2, "unique_blobs": 167,
    }, "E_DISPOSITION_COUNTS")
    process = disposition["process_commit_coverage"]
    require((process["release_commit_count"], process["routed_commit_count"],
             process["release_orphan_count"], process["routed_orphan_count"])
            == (17, 20, 0, 0), "E_DISPOSITION_PROCESS")
    gate_summary = carry["gate_summary"]
    require((gate_summary["phase057_prior"], gate_summary["phase057_new"],
             gate_summary["phase057_shared"], gate_summary["phase057_union"],
             gate_summary["step76_80_records"], gate_summary["owner_registry_records"],
             gate_summary["active_obligations"]) == (82, 95, 10, 177, 68, 355, 219),
            "E_CARRY_COUNTS")
    require(all(gate_summary[key] == 0 for key in (
        "ay_duplicate_new_obligations", "external_authority_promotions", "lost_inherited_ids",
        "multiply_owned_active_obligations", "ownerless_active_obligations",
    )), "E_CARRY_OWNER_ERRORS")
    ref7 = carry["ref7_canonical_route"]
    require((ref7["origin_identity"], ref7["canonical_owner"], ref7["status"],
             ref7["target_phase"], ref7["external_authority_promoted"]) == (
        "D74-006", "PHASE-071-PRIMARY-SOURCE-ACQUISITION", "GROUND_NOT_FOUND", 71, False,
    ), "E_REF7_ROUTE")

    integrated = {
        "source_read_process": {
            "occurrences": 433, "unique_blobs": 167, "text_blobs": 158,
            "text_lines": 30597, "pdf_blobs": 6, "pdf_pages": 308, "images": 3,
            "narrative_documents": 42, "narrative_lines": 9674,
            "release_commits": 17, "routed_commits": 20, "routing_ids": 105,
            "stale_pdf_pairs": 3,
        },
        "fit": {
            "components": 14, "parameters": 57, "starts": 12,
            "optimizer_execution_complete": True, "runtime_success": False,
            "selected_trial_converged": False,
            "raw_exact_binding": "GROUND_NOT_FOUND",
        },
        "optimizer": {
            "original_state_fields": 25, "original_state_status": "GROUND_NOT_FOUND",
            "stored_replay": "NOT_EQUIVALENT", "curve": "TOLERANCE_EQUIVALENT",
            "cross_runtime": "IDENTICAL",
        },
        "authority": authority["aggregate"],
        "profile": profile["aggregate"],
        "runtime": {"processes": 36, "successful": 36, "temperature_routes": "9/7"},
        "disposition": {
            "distribution": "424/3/6", "supplemental": 2, "phase057": "82/95/10/177",
            "step_records": 68, "owner_registry": 355, "active": 219,
            "owner_errors": "0/0/0/0/0",
        },
        "ref7": ref7,
        "positive_controls": {
            "source_path_bound": True, "source_hash_bound": True, "source_count_bound": True,
            "full_read_bound": True,
            "process_genealogy_bound": True, "pairwise_delta_bound": True,
            "manifest_supplemental_separate": True, "stale_pdf_not_promoted": True,
            "ay_duplicate_count_zero": True, "derivative_exact": True,
            "processed_data_hashes_exact": True, "parameter_order_exact": True,
            "bounds_and_start_exact": True, "synthetic_not_claimed_as_raw": True,
            "failed_fit_not_claimed_reproduced": True, "displayed8_not_full_state": True,
            "optimizer_diagnostics_not_fabricated": True, "empirical_not_material": True,
            "test_state_not_public_default": True, "profile_routes_complete": True,
            "temperature_routes_complete": True, "ref7_metadata_not_proposition_support": True,
            "owner_loss_zero": True, "owner_duplication_zero": True,
            "main_scholarly_body_unchanged": True,
            "deterministic_reconstruction": True,
            "repository_content_contract": True,
            "repository_persistence_evaluated": False,
            "repository_persistence_success": False,
        },
    }
    integrated["exclusive_gate"] = compute_gate_evaluation(integrated)
    return integrated


def compute_gate_evaluation(
    integrated: dict[str, Any], *, expected_gate: str = GATE,
) -> dict[str, Any]:
    controls = integrated["positive_controls"]
    pass_conditions = {
        "p01_source_read_complete": controls["source_path_bound"] and controls["source_hash_bound"]
        and controls["source_count_bound"] and controls["full_read_bound"],
        "p02_narrative_genealogy_complete": controls["process_genealogy_bound"],
        "p03_delta_and_stale_reproduced": controls["pairwise_delta_bound"] and controls["stale_pdf_not_promoted"],
        "p04_actual_direct14_reproduced": integrated["fit"]["optimizer_execution_complete"],
        "p05_stored_original_state_relation_grounded": integrated["optimizer"]["original_state_status"] != "GROUND_NOT_FOUND",
        "p06_profile_temperature_routes_observed": controls["profile_routes_complete"] and controls["temperature_routes_complete"],
        "p07_empirical_material_separated": controls["empirical_not_material"],
        "p08_single_canonical_owner": controls["owner_loss_zero"] and controls["owner_duplication_zero"],
        "p09_no_load_bearing_ground_not_found": integrated["fit"]["raw_exact_binding"] != "GROUND_NOT_FOUND"
        and integrated["optimizer"]["original_state_status"] != "GROUND_NOT_FOUND",
        "p10_ref7_lawful_exact_support": integrated["ref7"]["status"] != "GROUND_NOT_FOUND",
        "p11_review_clean_content": controls["deterministic_reconstruction"]
        and controls["repository_content_contract"],
        "p11_repository_persistence_mode": controls["repository_persistence_evaluated"]
        and controls["repository_persistence_success"],
    }
    conditional_conditions = {
        "c01_raw_or_preprocessing_ground_not_found": integrated["fit"]["raw_exact_binding"] == "GROUND_NOT_FOUND",
        "c02_original_optimizer_state_ground_not_found": integrated["optimizer"]["original_state_status"] == "GROUND_NOT_FOUND",
        "c03_held_out_external_material_authority_insufficient": integrated["authority"]["held_out_not_tested"] > 0
        and integrated["authority"]["external_authority_true"] == 0,
        "c04_stale_pdf_build_owner_open": integrated["source_read_process"]["stale_pdf_pairs"] > 0,
        "c05_ref7_original_full_text_ground_not_found": integrated["ref7"]["status"] == "GROUND_NOT_FOUND",
    }
    fail_conditions = {
        "f01_source_process_or_read_incomplete": not (
            controls["source_path_bound"] and controls["source_hash_bound"]
            and controls["source_count_bound"] and controls["full_read_bound"]
            and controls["process_genealogy_bound"] and controls["pairwise_delta_bound"]
        ),
        "f02_denominator_fusion": not controls["manifest_supplemental_separate"],
        "f03_fit_not_executed_but_reproduced": not controls["failed_fit_not_claimed_reproduced"],
        "f04_missing_state_or_diagnostics_fabricated": not (
            controls["synthetic_not_claimed_as_raw"] and controls["displayed8_not_full_state"]
            and controls["optimizer_diagnostics_not_fabricated"]
        ),
        "f05_test_state_reported_default": not controls["test_state_not_public_default"],
        "f06_profile_temperature_confused": not (controls["profile_routes_complete"] and controls["temperature_routes_complete"]),
        "f07_empirical_promoted_material": not controls["empirical_not_material"],
        "f08_ref7_metadata_promoted": not controls["ref7_metadata_not_proposition_support"],
        "f09_owner_loss_or_duplication": not (controls["owner_loss_zero"] and controls["owner_duplication_zero"]),
        "f10_determinism_failure": not controls["deterministic_reconstruction"],
        "f11_repository_transaction_failure_content_mode": not controls["repository_content_contract"],
    }
    selected = {
        "PASS_P066_LINEAGE_I": all(pass_conditions.values()),
        "CONDITIONAL_P066": not any(fail_conditions.values()) and any(conditional_conditions.values()),
        "FAIL_P066": any(fail_conditions.values()),
    }
    require(expected_gate in selected and sum(value is True for value in selected.values()) == 1
            and selected[expected_gate] is True,
            "E_EXCLUSIVE_GATE_PREDICATES", repr(selected))
    return {
        "selected": expected_gate, "selection": selected, "pass_conditions": pass_conditions,
        "conditional_conditions": conditional_conditions, "fail_conditions": fail_conditions,
        "repository_mode_gate": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "postcommit_persistence": {
            "evaluated": controls["repository_persistence_evaluated"],
            "success": controls["repository_persistence_success"],
            "pending": not controls["repository_persistence_evaluated"],
            "failure": controls["repository_persistence_evaluated"]
            and not controls["repository_persistence_success"],
        },
    }


def run_gate_controls(integrated: dict[str, Any]) -> tuple[int, int]:
    fields = [
        "process_genealogy_bound", "optimizer_diagnostics_not_fabricated",
        "deterministic_reconstruction", "repository_content_contract",
    ]
    passed = 0
    for field in fields:
        candidate = copy.deepcopy(integrated)
        candidate["positive_controls"][field] = False
        selection = compute_gate_evaluation(candidate, expected_gate="FAIL_P066")["selection"]
        require(selection == {
            "PASS_P066_LINEAGE_I": False, "CONDITIONAL_P066": False, "FAIL_P066": True,
        }, "E_GATE_CONTROL_SELECTION", f"{field}:{selection}")
        passed += 1
    return passed, len(fields)


def configure_fixture_refs(work: pathlib.Path, origin: pathlib.Path, active_tip: str) -> dict[str, str]:
    git(["config", "core.autocrlf", "false"], cwd=work)
    git(["remote", "set-url", "origin", ORIGIN_URL], cwd=work)
    git(["config", "remote.origin.vcs", "phase066"], cwd=work)
    git(["config", f"branch.{ACTIVE_BRANCH}.remote", "origin"], cwd=work)
    git(["config", f"branch.{ACTIVE_BRANCH}.merge", f"refs/heads/{ACTIVE_BRANCH}"], cwd=work)
    git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", active_tip], cwd=work)
    git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=work)
    git(["update-ref", "refs/heads/phase066-fixture-process-tip", PROCESS_TIP], cwd=work)
    git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=work)
    git(["update-ref", "refs/remotes/origin/main", MAIN_TIP], cwd=work)
    git(["--git-dir", str(origin), "update-ref", f"refs/heads/{ACTIVE_BRANCH}", active_tip], cwd=work)
    git(["--git-dir", str(origin), "update-ref", f"refs/heads/{PROTECTED_BRANCH}", PROTECTED_TIP], cwd=work)
    git(["--git-dir", str(origin), "update-ref", "refs/heads/main", MAIN_TIP], cwd=work)
    helper = origin.parent / "git-remote-phase066"
    helper.write_bytes(REMOTE_HELPER_BYTES)
    helper.chmod(helper.stat().st_mode | stat.S_IEXEC)
    environment = os.environ.copy()
    environment["PATH"] = str(origin.parent) + os.pathsep + environment.get("PATH", "")
    environment["PHASE066_FIXTURE_ORIGIN"] = str(origin)
    return environment


def make_historical_clone(spec: dict[str, Any], persistence: bool) -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    root = pathlib.Path(tempfile.mkdtemp(prefix="phase066-step812-history-"))
    try:
        origin = root / "origin.git"
        work = root / "work"
        git(["clone", "--bare", "--shared", str(ROOT), str(origin)], cwd=root)
        git(["clone", "--shared", "--no-checkout", str(ROOT), str(work)], cwd=root)
        git(["config", "core.autocrlf", "false"], cwd=work)
        target = spec["commit"] if persistence else spec["parent"]
        git(["checkout", "-B", ACTIVE_BRANCH, target], cwd=work)
        if not persistence:
            git(["checkout", spec["commit"], "--", *spec["paths"]], cwd=work)
        environment = configure_fixture_refs(work, origin, target)
        if spec["unit"] == "ACTIVATION":
            release_lines = git_text([
                "log", "--reverse", "--format=%H", "--all", "--",
                "Claude/docs/v1.0.25/**", "Claude/docs/v1.0.25.1/**", "Claude/docs/v1.0.25.2/**",
            ], cwd=work).splitlines()
            require(len(release_lines) == 17, "E_HISTORY_FIXTURE_PROCESS_COUNT",
                    f"count={len(release_lines)}:refs={git_text(['branch', '-a'], cwd=work)!r}")
        expected_paths = set() if persistence else set(spec["paths"])
        staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=work).stdout)
        unstaged = nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=work).stdout)
        untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=work).stdout)
        require(staged == expected_paths and not unstaged and not untracked,
                "E_HISTORY_FIXTURE_STATE",
                f"{spec['unit']}:{persistence}:staged={sorted(staged)}:unstaged={sorted(unstaged)}:untracked={sorted(untracked)}")
        return root, work, environment
    except Exception:
        remove_temp_tree(root)
        require(not root.exists(), "E_HISTORY_FIXTURE_CLEANUP_FAILURE", str(root))
        raise


def remove_temp_tree(root: pathlib.Path) -> None:
    resolved = root.resolve()
    temp = pathlib.Path(tempfile.gettempdir()).resolve()
    require(temp in resolved.parents and resolved.name.startswith((
        "phase066-step812-history-", "phase066-step812-migration-control-",
    )),
            "E_TEMP_CLEANUP_SCOPE", str(resolved))
    shutil.rmtree(resolved)


def expected_history_banners(spec: dict[str, Any], persistence: bool) -> list[str]:
    terminal = spec["persistence_terminal"] if persistence else spec["precommit_terminal"]
    if spec["unit"] == "ACTIVATION":
        return ["PASS_P066_PLAN_CONTROLS", "PASS_P066_PLAN_DETERMINISM", terminal]
    if spec["unit"] == "STEP76":
        return ["PASS_P066_STEP76_CONTROLS", "PASS_P066_STEP76_CONTENT", terminal]
    return [terminal]


def run_historical_record(spec: dict[str, Any], persistence: bool) -> dict[str, Any]:
    root, work, environment = make_historical_clone(spec, persistence)
    args = spec["persistence_args"] if persistence else spec["precommit_args"]
    terminal = spec["persistence_terminal"] if persistence else spec["precommit_terminal"]
    record: dict[str, Any] | None = None
    try:
        argv = [sys.executable, "-B", "-X", "utf8", spec["validator"], *args]
        process = run_process(argv, cwd=work, env=environment, timeout=1800, check=False)
        stdout = process.stdout.replace(b"\r\n", b"\n")
        stderr = process.stderr.replace(b"\r\n", b"\n")
        stdout_text = stdout.decode("utf-8", errors="strict")
        terminal_count = sum(
            line == terminal or line.startswith(terminal + " ")
            for line in stdout_text.splitlines()
        )
        require(process.returncode == 0, "E_HISTORY_EXIT",
                f"{spec['unit']}:{persistence}:stdout={stdout[-2400:]!r}:stderr={stderr[-1200:]!r}")
        expected_stderr = STEP76_KNOWN_WARNING if spec["unit"] == "STEP76" else b""
        require(stderr == expected_stderr, "E_HISTORY_STDERR",
                f"{spec['unit']}:{persistence}:{stderr[-1200:]!r}")
        require(terminal_count == 1, "E_HISTORY_TERMINAL", f"{spec['unit']}:{persistence}:{terminal_count}")
        banner_codes = [
            line.split()[0] for line in stdout_text.splitlines()
            if line.startswith(("PASS_P066_", "CONDITIONAL_P066_"))
        ]
        require(banner_codes == expected_history_banners(spec, persistence)
                and set(banner_codes) <= HISTORY_BANNER_ALLOWLIST[spec["unit"]],
                "E_HISTORY_BANNER_SUMMARY", f"{spec['unit']}:{persistence}:{banner_codes}")
        post_staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"], cwd=work).stdout)
        post_unstaged = nul_paths(git(["diff", "--no-renames", "--name-only", "-z"], cwd=work).stdout)
        post_untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=work).stdout)
        require(post_staged == (set() if persistence else set(spec["paths"]))
                and not post_unstaged and not post_untracked,
                "E_HISTORY_POST_STATE", f"{spec['unit']}:{persistence}")
        transaction = name_status_records(git([
            "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-r", "-z", spec["commit"],
        ], cwd=work).stdout)
        expected_transaction = [
            {"status": "M" if path in {HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH} else "A",
             "path": path}
            for path in sorted(spec["paths"])
        ]
        modes = exact_modes(spec["commit"], spec["paths"], cwd=work)
        require(transaction == expected_transaction and all(mode == "100644" for mode in modes.values()),
                "E_HISTORY_TRANSACTION", spec["unit"])
        target = spec["commit"] if persistence else spec["parent"]
        refs = {
            "active_branch": git_text(["branch", "--show-current"], cwd=work),
            "head": git_text(["rev-parse", "HEAD"], cwd=work),
            "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"], cwd=work),
            "tracking_active": git_text(["rev-parse", UPSTREAM], cwd=work),
            "live_active": live_tip(ACTIVE_BRANCH, cwd=work, env=environment),
            "protected_local": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=work),
            "protected_tracking": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"], cwd=work),
            "protected_live": live_tip(PROTECTED_BRANCH, cwd=work, env=environment),
            "main_tracking": git_text(["rev-parse", "refs/remotes/origin/main"], cwd=work),
            "main_live": live_tip("main", cwd=work, env=environment),
        }
        require(refs == {
            "active_branch": ACTIVE_BRANCH, "head": target, "upstream_name": UPSTREAM,
            "tracking_active": target, "live_active": target,
            "protected_local": PROTECTED_TIP, "protected_tracking": PROTECTED_TIP,
            "protected_live": PROTECTED_TIP, "main_tracking": MAIN_TIP, "main_live": MAIN_TIP,
        }, "E_HISTORY_REFS", f"{spec['unit']}:{persistence}:{refs}")
        record = {
            "unit": spec["unit"], "commit": spec["commit"], "parent": spec["parent"],
            "subject": spec["subject"], "changed_paths": spec["paths"],
            "name_status": transaction, "modes": modes, "args": args,
            "normalized_argv": ["CURRENT_OUTER_RUNTIME", "-B", "-X", "utf8", spec["validator"], *args],
            "validator_path": spec["validator"], "validator_sha256": spec["validator_sha256"],
            "terminal": terminal, "terminal_count": terminal_count, "exit_code": process.returncode,
            "stderr_bytes": len(stderr), "stderr_lf_sha256": sha256(stderr),
            "banner_codes": banner_codes, "banner_summary_sha256": sha256(canonical_bytes(banner_codes)),
            "stdout_observation": {
                "collector_runtime": sys.version.split()[0], "lf_bytes": len(stdout),
                "lf_sha256": sha256(stdout),
                "cross_runtime_comparison": "NOT_REPLAYED_BY_DESIGN",
            },
            "python": "CURRENT_OUTER_RUNTIME", "refs": refs,
            "context": "DISPOSABLE_CLEAN_HISTORICAL_PERSISTENCE_CLONE" if persistence
            else "DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE",
            "cleanup_success": False,
        }
    finally:
        remove_temp_tree(root)
    require(not root.exists() and record is not None, "E_HISTORY_CLEANUP", str(root))
    record["cleanup_success"] = True
    return record


def collect_historical() -> dict[str, Any]:
    before = git(["status", "--porcelain=v1", "-z"]).stdout
    precommit = [run_historical_record(spec, False) for spec in UNIT_SPECS]
    persistence = [run_historical_record(spec, True) for spec in UNIT_SPECS]
    after = git(["status", "--porcelain=v1", "-z"]).stdout
    require(before == after, "E_ACTIVE_REPOSITORY_CHANGED_BY_HISTORY")
    return {
        "unit_count": 7, "precommit_count": 7, "persistence_count": 7,
        "record_count": 14, "fresh_historical_replay": 14,
        "precommit": precommit, "persistence": persistence,
    }


def validate_reused_history(history: Any) -> dict[str, Any]:
    require(type(history) is dict and set(history) == {
        "fresh_historical_replay", "persistence", "persistence_count", "precommit",
        "precommit_count", "record_count", "unit_count",
    }, "E_HISTORY_SCHEMA")
    require((history["unit_count"], history["precommit_count"], history["persistence_count"],
             history["record_count"], history["fresh_historical_replay"]) == (7, 7, 7, 14, 14),
            "E_HISTORY_COUNTS")
    record_keys = {
        "args", "banner_codes", "banner_summary_sha256", "changed_paths", "cleanup_success",
        "commit", "context", "exit_code", "modes", "name_status", "normalized_argv", "parent",
        "python", "refs", "stderr_bytes", "stderr_lf_sha256", "stdout_observation", "subject",
        "terminal", "terminal_count", "unit", "validator_path", "validator_sha256",
    }
    for name, persistence in (("precommit", False), ("persistence", True)):
        records = history[name]
        require(type(records) is list and len(records) == 7, "E_HISTORY_RECORD_COUNT", name)
        for record, spec in zip(records, UNIT_SPECS, strict=True):
            args = spec["persistence_args"] if persistence else spec["precommit_args"]
            terminal = spec["persistence_terminal"] if persistence else spec["precommit_terminal"]
            context = "DISPOSABLE_CLEAN_HISTORICAL_PERSISTENCE_CLONE" if persistence else "DISPOSABLE_EXACT_STAGED_HISTORICAL_PRECOMMIT_CLONE"
            expected_stderr = STEP76_KNOWN_WARNING if spec["unit"] == "STEP76" else b""
            expected_transaction = [
                {"status": "M" if path in {HANDOVER_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH} else "A",
                 "path": path}
                for path in sorted(spec["paths"])
            ]
            target = spec["commit"] if persistence else spec["parent"]
            expected_refs = {
                "active_branch": ACTIVE_BRANCH, "head": target, "upstream_name": UPSTREAM,
                "tracking_active": target, "live_active": target,
                "protected_local": PROTECTED_TIP, "protected_tracking": PROTECTED_TIP,
                "protected_live": PROTECTED_TIP, "main_tracking": MAIN_TIP, "main_live": MAIN_TIP,
            }
            require(type(record) is dict and set(record) == record_keys, "E_HISTORY_RECORD_SCHEMA", spec["unit"])
            require((record["unit"], record["commit"], record["parent"], record["subject"],
                     record["changed_paths"], record["args"], record["validator_path"],
                     record["validator_sha256"], record["terminal"], record["terminal_count"],
                     record["exit_code"], record["stderr_bytes"], record["stderr_lf_sha256"],
                     record["python"], record["context"], record["cleanup_success"])
                    == (spec["unit"], spec["commit"], spec["parent"], spec["subject"],
                        spec["paths"], args, spec["validator"], spec["validator_sha256"],
                        terminal, 1, 0, len(expected_stderr), sha256(expected_stderr),
                        "CURRENT_OUTER_RUNTIME", context, True),
                    "E_HISTORY_RECORD_IDENTITY", f"{name}:{spec['unit']}")
            require(record["name_status"] == expected_transaction
                    and record["modes"] == {path: "100644" for path in spec["paths"]}
                    and record["normalized_argv"] == [
                        "CURRENT_OUTER_RUNTIME", "-B", "-X", "utf8", spec["validator"], *args,
                    ] and record["refs"] == expected_refs,
                    "E_HISTORY_RECORD_TRANSACTION", f"{name}:{spec['unit']}")
            banners = expected_history_banners(spec, persistence)
            require(record["banner_codes"] == banners
                    and record["banner_summary_sha256"] == sha256(canonical_bytes(banners)),
                    "E_HISTORY_RECORD_BANNERS", f"{name}:{spec['unit']}")
            observation = record["stdout_observation"]
            require(type(observation) is dict and set(observation) == {
                "collector_runtime", "cross_runtime_comparison", "lf_bytes", "lf_sha256",
            } and re.fullmatch(r"3\.12\.\d+", observation["collector_runtime"]) is not None
                    and observation["cross_runtime_comparison"] == "NOT_REPLAYED_BY_DESIGN"
                    and type(observation["lf_bytes"]) is int and observation["lf_bytes"] > 0
                    and re.fullmatch(r"[0-9a-f]{64}", observation["lf_sha256"]) is not None,
                    "E_HISTORY_RECORD_STDOUT", f"{name}:{spec['unit']}")
    return copy.deepcopy(history)


def parse_direct14_raw_claim(text: str, label: str) -> tuple[str, str, int, str]:
    blocks = re.findall(r"(?m)^(?:-|\d+\.) .*(?:\n {2,}.*)*", text)
    matches = [block for block in blocks if f"`{DIRECT14_RAW_PATH}`" in block]
    require(text.count(f"`{DIRECT14_RAW_PATH}`") == 1 and len(matches) == 1,
            "E_DOCUMENT_DIRECT14_CLAIM_CARDINALITY", label)
    tokens = re.findall(r"`([^`\r\n]+)`", matches[0])
    paths = [token for token in tokens if token.endswith(".csv")]
    hashes = [token for token in tokens if re.fullmatch(r"[0-9a-f]{64}", token) is not None]
    rows = [token for token in tokens if token.replace(",", "") == str(DIRECT14_RAW_ROWS)]
    bindings = [token for token in tokens if "GROUND_NOT_FOUND" in token]
    require(paths == [DIRECT14_RAW_PATH], "E_DOCUMENT_DIRECT14_PATH", f"{label}:{paths}")
    require(hashes == [DIRECT14_RAW_SHA256], "E_DOCUMENT_DIRECT14_RAW_SHA", f"{label}:{hashes}")
    require(rows == [f"{DIRECT14_RAW_ROWS:,}"], "E_DOCUMENT_DIRECT14_ROWS", f"{label}:{rows}")
    require(bindings and set(bindings) <= DIRECT14_BINDING_ALIASES,
            "E_DOCUMENT_DIRECT14_BINDING", f"{label}:{bindings}")
    return DIRECT14_RAW_PATH, DIRECT14_RAW_SHA256, DIRECT14_RAW_ROWS, DIRECT14_BINDING


def parse_machine_evidence_table(text: str) -> list[tuple[str, str, str, str]]:
    marker = "### Machine evidence cross-bind"
    require(text.count(marker) == 1, "E_DOCUMENT_MACHINE_TABLE_MARKER")
    section = text.split(marker, 1)[1].lstrip("\r\n")
    lines = section.splitlines()
    table_lines: list[str] = []
    for line in lines:
        if line.startswith("|"):
            table_lines.append(line)
        elif table_lines:
            break
    require(len(table_lines) == 13, "E_DOCUMENT_MACHINE_TABLE_ROWS", str(len(table_lines)))
    require(table_lines[0] == "| Machine artifact | Owning commit | Raw SHA-256 | Semantic SHA-256 | Bound status/count |"
            and table_lines[1] == "|---|---|---|---|---|", "E_DOCUMENT_MACHINE_TABLE_HEADER")
    records: list[tuple[str, str, str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        require(len(cells) == 5, "E_DOCUMENT_MACHINE_TABLE_CELL_COUNT", line)
        values: list[str] = []
        for cell in cells[:4]:
            require(len(cell) >= 2 and cell.startswith("`") and cell.endswith("`")
                    and "`" not in cell[1:-1], "E_DOCUMENT_MACHINE_TABLE_CELL", cell)
            values.append(cell[1:-1])
        records.append((values[0], values[1], values[2], values[3]))
    expected = [
        (path, owning_commit, raw_pin, semantic_pin)
        for path, raw_pin, semantic_pin, owning_commit in MACHINE_SPECS
    ]
    require(records == expected, "E_DOCUMENT_MACHINE_TABLE_TUPLES", repr(records))
    return records


def human_document_controls() -> tuple[int, int]:
    wrong_sha = "0" * 64
    gate_text = (ROOT / GATE_PATH).read_text(encoding="utf-8")
    appended = gate_text + (
        f"\n- Adversarial duplicate `{DIRECT14_RAW_PATH}` raw SHA `{wrong_sha}`; "
        f"correct token elsewhere `{DIRECT14_RAW_SHA256}`, rows `{DIRECT14_RAW_ROWS:,}`, "
        f"binding `{DIRECT14_BINDING}`.\n"
    )
    report_text = (ROOT / REPORT_PATH).read_text(encoding="utf-8")
    first = MACHINE_SPECS[0]
    swapped = report_text.replace(
        f"| `{first[1]}` | `{first[2]}` |", f"| `{first[2]}` | `{first[1]}` |", 1,
    )
    passed = 0
    try:
        parse_direct14_raw_claim(appended, GATE_PATH)
    except ValidationError as error:
        require(error.code == "E_DOCUMENT_DIRECT14_CLAIM_CARDINALITY", "E_HUMAN_CONTROL_CODE",
                f"direct14_adjacent_wrong_and_correct:{error.code}")
        passed += 1
    else:
        raise ValidationError("E_HUMAN_CONTROL_ACCEPTED", "direct14_adjacent_wrong_and_correct")
    try:
        parse_machine_evidence_table(swapped)
    except ValidationError as error:
        require(error.code == "E_DOCUMENT_MACHINE_TABLE_TUPLES", "E_HUMAN_CONTROL_CODE",
                f"machine_raw_semantic_swap:{error.code}")
        passed += 1
    else:
        raise ValidationError("E_HUMAN_CONTROL_ACCEPTED", "machine_raw_semantic_swap")
    return passed, 2


def validate_human_documents() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    required: dict[str, list[str]] = {
        REPORT_PATH: [
            "Selected phase gate: `CONDITIONAL_P066`",
            "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
            "Postcommit persistence terminal: `PASS_P066_STEP81_2_PERSISTENCE`",
            "Canonical-history denominator: precommit `7` + persistence `7` = `14`",
            "`PASS_P066_LINEAGE_I` is rejected",
            "Phase 067 detailed plan",
            "Claude/results/comp_v24/sintef_data/sigr.csv",
            "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6",
            "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND",
        ],
        GATE_PATH: [
            "Selected gate: `CONDITIONAL_P066`", "Rejected promotion: `PASS_P066_LINEAGE_I`",
            "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
            "Postcommit persistence terminal: `PASS_P066_STEP81_2_PERSISTENCE`",
            "fresh_historical_replay=0/14", "claim staged PASS because Step 81.2 has not been staged",
            "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6",
        ],
        RESULT_PATH: [
            "Selected gate: `CONDITIONAL_P066`", "Status: `CONDITIONAL_PENDING_PERSISTENCE`",
            "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
            "Postcommit persistence terminal: `PASS_P066_STEP81_2_PERSISTENCE`",
            "Stored records: precommit `7/7`, persistence `7/7`, total `14/14`",
            "`PASS_P066_LINEAGE_I` is not selected",
            "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6",
        ],
        PARENT_LEDGER_PATH: [
            "Steps 76–81.2 complete; final persistence pending", "`CONDITIONAL_P066`",
            PARENT_COMMIT, "`PENDING_AT_PRECOMMIT_BY_DESIGN`", SUBJECT,
        ],
        ACTIVE_LEDGER_PATH: [
            "Steps 76–81.2 complete; final persistence pending", "Phase 066 Step 81.2",
            PARENT_COMMIT, "canonical history `14/14`", SUBJECT,
        ],
        HANDOVER_PATH: [
            "Phase 066 Step 81.2 selected `CONDITIONAL_P066`", "canonical history `14/14`",
            PARENT_COMMIT, "`PENDING_AT_PRECOMMIT_BY_DESIGN`", SUBJECT,
        ],
    }
    document_texts: dict[str, str] = {}
    for path, tokens in required.items():
        raw = (ROOT / path).read_bytes()
        text = raw.decode("utf-8")
        document_texts[path] = text
        for token in tokens:
            require(token in text, "E_DOCUMENT_TOKEN", f"{path}:{token}")
        require("Step 81.1 starts only after" not in text
                and "Step 81.2 starts only after Python 3.12/3.14 return `PASS_P066_STEP81_1_PERSISTENCE`" not in text,
                "E_DOCUMENT_STALE_NEXT", path)
        records.append({"path": path, "bytes": len(raw), "raw_sha256": sha256(raw)})
    for path in (REPORT_PATH, GATE_PATH, RESULT_PATH):
        require(parse_direct14_raw_claim(document_texts[path], path) == (
            DIRECT14_RAW_PATH, DIRECT14_RAW_SHA256, DIRECT14_RAW_ROWS, DIRECT14_BINDING,
        ), "E_DOCUMENT_DIRECT14_TUPLE", path)
    report = document_texts[REPORT_PATH]
    parse_machine_evidence_table(report)
    require("e571a971" not in report, "E_DOCUMENT_STALE_RAW_SHA")
    for path, raw_pin, semantic_pin, owning_commit in MACHINE_SPECS:
        for token in (path, raw_pin, semantic_pin, owning_commit):
            require(token in report, "E_DOCUMENT_MACHINE_CROSS_BIND", f"{path}:{token}")
    validator_raw = (ROOT / VALIDATOR_PATH).read_bytes()
    records.append({"path": VALIDATOR_PATH, "bytes": len(validator_raw), "raw_sha256": sha256(validator_raw)})
    return records


def build_document(history: dict[str, Any]) -> dict[str, Any]:
    machines, machine_records, traversal = load_machine_artifacts()
    commits = validate_predecessor_commits()
    integrated = validate_cross_semantics(machines)
    outputs = validate_human_documents()
    document: dict[str, Any] = {
        "schema_version": "phase066-step81.2-final-validation-v1",
        "phase": 66,
        "step": "81.2",
        "generated_date": "2026-09-01",
        "gate": GATE,
        "status": STATUS,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "expected_parent": PARENT_COMMIT,
        "expected_subject": SUBJECT,
        "persistence_terminal": PERSISTENCE,
        "repository_contract": {
            "active_branch": ACTIVE_BRANCH, "upstream": UPSTREAM,
            "protected_branch": PROTECTED_BRANCH, "protected_tip": PROTECTED_TIP,
            "main_tip": MAIN_TIP, "origin_url": ORIGIN_URL,
            "exact_paths": FINAL_PATHS, "exact_path_count": 8,
            "result_first": True, "json_last": True,
            "production_source_changed": False, "claude_changed": False,
        },
        "historical_execution": validate_reused_history(history),
        "canonical_history_contract": {
            "units": [spec["unit"] for spec in UNIT_SPECS],
            "precommit": 7, "persistence": 7, "total": 14,
            "ordinary_fresh_historical_replay": 0,
            "collector_only_fresh_historical_replay": 14,
        },
        "predecessor_commits": commits,
        "machine_evidence": machine_records,
        "machine_full_traversal": traversal,
        "integrated_assertions": integrated,
        "output_evidence": outputs,
        "authority_ceiling": {
            "ref7_original_full_text": "GROUND_NOT_FOUND",
            "original_full_precision_optimizer_state": "GROUND_NOT_FOUND",
            "raw_exact_binding": "GROUND_NOT_FOUND",
            "held_out_authority": False, "external_authority": False,
            "material_authority": False, "stale_pdf_build_closed": False,
            "main_scholarly_body_modified": False,
        },
        "next_phase_boundary": {
            "step81_2_persistence_required": True,
            "phase067_plan_activation_required": True,
            "step82_released": False,
        },
        "negative_control_contract": {
            "semantic_cases": 35, "strict_json_cases": 6,
            "source_policy_cases": 5, "repository_boundary_cases": 18,
            "human_document_cases": 2, "gate_truth_table_cases": 4,
            "migration_transaction_cases": 3,
        },
        "determinism": {"reconstructions": 2, "equal": True},
    }
    document["semantic_sha256"] = semantic_hash(document)
    return document


def document_diagnostics(candidate: dict[str, Any], expected: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    if candidate != expected:
        errors.add("E_DOCUMENT_RECONSTRUCTION")
    if candidate.get("gate") != GATE or candidate.get("gate") == "PASS_P066_LINEAGE_I":
        errors.add("E_GATE_EXCLUSIVE")
    if candidate.get("status") != STATUS:
        errors.add("E_STATUS")
    if candidate.get("containing_commit") != "PENDING_AT_PRECOMMIT_BY_DESIGN":
        errors.add("E_CONTAINING_COMMIT")
    if candidate.get("expected_parent") != PARENT_COMMIT or candidate.get("expected_subject") != SUBJECT:
        errors.add("E_COMMIT_CONTRACT")
    if candidate.get("persistence_terminal") != PERSISTENCE:
        errors.add("E_PERSISTENCE_TERMINAL")
    history = candidate.get("historical_execution", {})
    if not isinstance(history, dict) or (
        history.get("unit_count"), history.get("precommit_count"), history.get("persistence_count"),
        history.get("record_count"), history.get("fresh_historical_replay"),
    ) != (7, 7, 7, 14, 14):
        errors.add("E_HISTORY_COUNTS")
    elif len(history.get("precommit", [])) != 7 or len(history.get("persistence", [])) != 7:
        errors.add("E_HISTORY_RECORD_COUNT")
    repository = candidate.get("repository_contract", {})
    if not isinstance(repository, dict) or repository.get("exact_paths") != FINAL_PATHS \
            or repository.get("exact_path_count") != 8:
        errors.add("E_EXACT_EIGHT")
    if not isinstance(repository, dict) or repository.get("result_first") is not True \
            or repository.get("json_last") is not True:
        errors.add("E_RESULT_JSON_ORDER")
    if not isinstance(repository, dict) or repository.get("protected_tip") != PROTECTED_TIP:
        errors.add("E_PROTECTED_MUTATION")
    if not isinstance(repository, dict) or repository.get("main_tip") != MAIN_TIP:
        errors.add("E_MAIN_MUTATION")
    if not isinstance(repository, dict) or repository.get("claude_changed") is not False:
        errors.add("E_CLAUDE_MUTATION")
    integrated = candidate.get("integrated_assertions", {})
    if not isinstance(integrated, dict) or integrated.get("fit", {}).get("runtime_success") is not False \
            or integrated.get("fit", {}).get("selected_trial_converged") is not False:
        errors.add("E_FIT_CEILING")
    if not isinstance(integrated, dict) or integrated.get("optimizer", {}).get("original_state_fields") != 25 \
            or integrated.get("optimizer", {}).get("original_state_status") != "GROUND_NOT_FOUND":
        errors.add("E_OPTIMIZER_STATE_CEILING")
    if not isinstance(integrated, dict) or integrated.get("authority", {}).get("external_authority_true") != 0 \
            or integrated.get("authority", {}).get("physical_authority_true") != 0:
        errors.add("E_AUTHORITY_CEILING")
    if not isinstance(integrated, dict) or integrated.get("profile", {}).get("route_rows") != 16 \
            or integrated.get("runtime", {}).get("processes") != 36:
        errors.add("E_PROFILE_RUNTIME")
    if not isinstance(integrated, dict) or integrated.get("ref7", {}).get("status") != "GROUND_NOT_FOUND" \
            or integrated.get("ref7", {}).get("canonical_owner") != "PHASE-071-PRIMARY-SOURCE-ACQUISITION":
        errors.add("E_REF7_CEILING")
    positive_codes = {
        "source_path_bound": "E_MUTATION_PATH", "source_hash_bound": "E_MUTATION_HASH",
        "source_count_bound": "E_MUTATION_COUNT", "full_read_bound": "E_MUTATION_READ",
        "process_genealogy_bound": "E_MUTATION_PROCESS", "pairwise_delta_bound": "E_MUTATION_DELTA",
        "manifest_supplemental_separate": "E_DENOMINATOR_FUSION",
        "stale_pdf_not_promoted": "E_STALE_PDF_PROMOTION",
        "ay_duplicate_count_zero": "E_AY_DUPLICATION", "derivative_exact": "E_DERIVATIVE_MUTATION",
        "processed_data_hashes_exact": "E_DATA_MUTATION", "parameter_order_exact": "E_ORDER_MUTATION",
        "bounds_and_start_exact": "E_BOUNDS_MUTATION", "synthetic_not_claimed_as_raw": "E_SYNTHETIC_AS_RAW",
        "failed_fit_not_claimed_reproduced": "E_FAILED_FIT_AS_REPRODUCED",
        "displayed8_not_full_state": "E_DISPLAYED8_AS_FULL_STATE",
        "optimizer_diagnostics_not_fabricated": "E_FABRICATED_DIAGNOSTICS",
        "empirical_not_material": "E_EMPIRICAL_TO_MATERIAL",
        "test_state_not_public_default": "E_TEST_STATE_AS_DEFAULT",
        "profile_routes_complete": "E_OMITTED_PROFILE_ROUTE",
        "temperature_routes_complete": "E_OMITTED_TEMPERATURE_ROUTE",
        "ref7_metadata_not_proposition_support": "E_REF7_METADATA_PROMOTION",
        "owner_loss_zero": "E_OWNER_LOSS", "owner_duplication_zero": "E_OWNER_DUPLICATION",
        "main_scholarly_body_unchanged": "E_SCHOLARLY_CODE_MENTION",
        "deterministic_reconstruction": "E_DETERMINISM_MUTATION",
        "repository_content_contract": "E_REPOSITORY_CONTENT_MUTATION",
    }
    positive = integrated.get("positive_controls", {}) if isinstance(integrated, dict) else {}
    expected_positive = expected.get("integrated_assertions", {}).get("positive_controls", {})
    for name, code in positive_codes.items():
        if positive.get(name) != expected_positive.get(name) or positive.get(name) is not True:
            errors.add(code)
    gate_evaluation = integrated.get("exclusive_gate", {}) if isinstance(integrated, dict) else {}
    if gate_evaluation != expected.get("integrated_assertions", {}).get("exclusive_gate", {}) \
            or gate_evaluation.get("selection") != {
                "PASS_P066_LINEAGE_I": False, "CONDITIONAL_P066": True, "FAIL_P066": False,
            }:
        errors.add("E_GATE_CONDITIONS")
    ceiling = candidate.get("authority_ceiling", {})
    if not isinstance(ceiling, dict) or ceiling.get("stale_pdf_build_closed") is not False \
            or ceiling.get("held_out_authority") is not False or ceiling.get("material_authority") is not False:
        errors.add("E_OPEN_AUTHORITY_CEILING")
    boundary = candidate.get("next_phase_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("step81_2_persistence_required") is not True \
            or boundary.get("phase067_plan_activation_required") is not True \
            or boundary.get("step82_released") is not False:
        errors.add("E_NEXT_PHASE_BOUNDARY")
    stored_seal = candidate.get("semantic_sha256")
    if not isinstance(stored_seal, str) or stored_seal != semantic_hash(candidate):
        errors.add("E_SEMANTIC_SEAL")
    return errors


def run_semantic_controls(baseline: dict[str, Any]) -> tuple[int, int]:
    positive = "integrated_assertions.positive_controls."
    cases: list[tuple[str, str, Any, str]] = [
        ("path_mutation", positive + "source_path_bound", False, "E_MUTATION_PATH"),
        ("hash_mutation", positive + "source_hash_bound", False, "E_MUTATION_HASH"),
        ("count_mutation", positive + "source_count_bound", False, "E_MUTATION_COUNT"),
        ("read_mutation", positive + "full_read_bound", False, "E_MUTATION_READ"),
        ("process_mutation", positive + "process_genealogy_bound", False, "E_MUTATION_PROCESS"),
        ("delta_mutation", positive + "pairwise_delta_bound", False, "E_MUTATION_DELTA"),
        ("denominator_fusion", positive + "manifest_supplemental_separate", False, "E_DENOMINATOR_FUSION"),
        ("stale_pdf_promotion", positive + "stale_pdf_not_promoted", False, "E_STALE_PDF_PROMOTION"),
        ("ay_duplication", positive + "ay_duplicate_count_zero", False, "E_AY_DUPLICATION"),
        ("derivative_mutation", positive + "derivative_exact", False, "E_DERIVATIVE_MUTATION"),
        ("data_mutation", positive + "processed_data_hashes_exact", False, "E_DATA_MUTATION"),
        ("order_mutation", positive + "parameter_order_exact", False, "E_ORDER_MUTATION"),
        ("bounds_mutation", positive + "bounds_and_start_exact", False, "E_BOUNDS_MUTATION"),
        ("synthetic_as_raw", positive + "synthetic_not_claimed_as_raw", False, "E_SYNTHETIC_AS_RAW"),
        ("failed_fit_as_reproduced", positive + "failed_fit_not_claimed_reproduced", False, "E_FAILED_FIT_AS_REPRODUCED"),
        ("displayed8_as_full_state", positive + "displayed8_not_full_state", False, "E_DISPLAYED8_AS_FULL_STATE"),
        ("fabricated_diagnostics", positive + "optimizer_diagnostics_not_fabricated", False, "E_FABRICATED_DIAGNOSTICS"),
        ("empirical_to_material", positive + "empirical_not_material", False, "E_EMPIRICAL_TO_MATERIAL"),
        ("test_state_as_default", positive + "test_state_not_public_default", False, "E_TEST_STATE_AS_DEFAULT"),
        ("omitted_profile_route", positive + "profile_routes_complete", False, "E_OMITTED_PROFILE_ROUTE"),
        ("omitted_temperature_route", positive + "temperature_routes_complete", False, "E_OMITTED_TEMPERATURE_ROUTE"),
        ("ref7_metadata_promotion", positive + "ref7_metadata_not_proposition_support", False, "E_REF7_METADATA_PROMOTION"),
        ("owner_loss", positive + "owner_loss_zero", False, "E_OWNER_LOSS"),
        ("owner_duplication", positive + "owner_duplication_zero", False, "E_OWNER_DUPLICATION"),
        ("scholarly_code_mention", positive + "main_scholarly_body_unchanged", False, "E_SCHOLARLY_CODE_MENTION"),
        ("determinism_failure", positive + "deterministic_reconstruction", False, "E_DETERMINISM_MUTATION"),
        ("repository_content_failure", positive + "repository_content_contract", False, "E_REPOSITORY_CONTENT_MUTATION"),
        ("wrong_gate", "gate", "PASS_P066_LINEAGE_I", "E_GATE_EXCLUSIVE"),
        ("wrong_parent", "expected_parent", STEP80, "E_COMMIT_CONTRACT"),
        ("wrong_subject", "expected_subject", "wrong subject", "E_COMMIT_CONTRACT"),
        ("wrong_terminal", "persistence_terminal", "PASS_P066_LINEAGE_I", "E_PERSISTENCE_TERMINAL"),
        ("extra_path", "repository_contract.exact_paths", FINAL_PATHS + ["extra"], "E_EXACT_EIGHT"),
        ("protected_change", "repository_contract.protected_tip", STEP80, "E_PROTECTED_MUTATION"),
        ("main_change", "repository_contract.main_tip", STEP80, "E_MAIN_MUTATION"),
        ("claude_change", "repository_contract.claude_changed", True, "E_CLAUDE_MUTATION"),
    ]
    passed = 0
    for name, dotted, value, expected_code in cases:
        candidate = copy.deepcopy(baseline)
        target: dict[str, Any] = candidate
        parts = dotted.split(".")
        for part in parts[:-1]:
            target = target[part]
        target[parts[-1]] = value
        candidate["semantic_sha256"] = semantic_hash(candidate)
        diagnostics = document_diagnostics(candidate, baseline)
        require(expected_code in diagnostics, "E_SEMANTIC_CONTROL_CODE",
                f"{name}:{sorted(diagnostics)} expected={expected_code}")
        passed += 1
    return passed, len(cases)


def repository_snapshot() -> dict[str, Any]:
    staged = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"]).stdout)
    unstaged = nul_paths(git(["diff", "--no-renames", "--name-only", "-z"]).stdout)
    untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout)
    head = git_text(["rev-parse", "HEAD"])
    return {
        "branch": git_text(["branch", "--show-current"]),
        "head": head,
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]),
        "tracking": git_text(["rev-parse", UPSTREAM]),
        "live_active": live_tip(ACTIVE_BRANCH),
        "protected_local": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]),
        "protected_tracking": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"]),
        "protected_live": live_tip(PROTECTED_BRANCH),
        "main_tracking": git_text(["rev-parse", "refs/remotes/origin/main"]),
        "main_live": live_tip("main"),
        "origin": git_text(["remote", "get-url", "origin"]),
        "staged": staged, "unstaged": unstaged, "untracked": untracked,
        "index_worktree_equal": all(
            git(["show", f":{path}"], check=False).returncode != 0
            or git(["show", f":{path}"], check=False).stdout == (ROOT / path).read_bytes()
            for path in FINAL_PATHS
        ),
        "diff_check": git(["diff", "--check"], check=False).returncode == 0
        and git(["diff", "--cached", "--check"], check=False).returncode == 0,
        "claude_changed": bool(git_text(["diff", "--name-only", BASELINE, "--", "Claude"])),
        "production_changed": any(
            not path.startswith("Codex/results/") and not path.startswith("Codex/work/")
            for path in staged | unstaged | untracked
        ),
    }


def repository_diagnostics(snapshot: dict[str, Any], *, precommit: bool) -> set[str]:
    errors: set[str] = set()
    if snapshot.get("branch") != ACTIVE_BRANCH:
        errors.add("E_REPOSITORY_BRANCH")
    if snapshot.get("head") != PARENT_COMMIT:
        errors.add("E_REPOSITORY_HEAD")
    if snapshot.get("upstream_name") != UPSTREAM:
        errors.add("E_REPOSITORY_UPSTREAM_NAME")
    if snapshot.get("tracking") != PARENT_COMMIT:
        errors.add("E_REPOSITORY_TRACKING")
    if snapshot.get("live_active") != PARENT_COMMIT:
        errors.add("E_REPOSITORY_LIVE_ACTIVE")
    if snapshot.get("protected_local") != PROTECTED_TIP:
        errors.add("E_REPOSITORY_PROTECTED_LOCAL")
    if snapshot.get("protected_tracking") != PROTECTED_TIP:
        errors.add("E_REPOSITORY_PROTECTED_TRACKING")
    if snapshot.get("protected_live") != PROTECTED_TIP:
        errors.add("E_REPOSITORY_PROTECTED_LIVE")
    if snapshot.get("main_tracking") != MAIN_TIP:
        errors.add("E_REPOSITORY_MAIN_TRACKING")
    if snapshot.get("main_live") != MAIN_TIP:
        errors.add("E_REPOSITORY_MAIN_LIVE")
    if snapshot.get("origin") != ORIGIN_URL:
        errors.add("E_REPOSITORY_ORIGIN")
    if snapshot.get("claude_changed") is not False:
        errors.add("E_REPOSITORY_CLAUDE")
    if snapshot.get("production_changed") is not False:
        errors.add("E_REPOSITORY_PRODUCTION")
    if precommit:
        if snapshot.get("staged") != FINAL_PATH_SET:
            errors.add("E_REPOSITORY_STAGED")
        if snapshot.get("unstaged"):
            errors.add("E_REPOSITORY_UNSTAGED")
        if snapshot.get("untracked"):
            errors.add("E_REPOSITORY_UNTRACKED")
        if snapshot.get("index_worktree_equal") is not True:
            errors.add("E_REPOSITORY_INDEX_BYTES")
        if snapshot.get("diff_check") is not True:
            errors.add("E_REPOSITORY_DIFF_CHECK")
    return errors


def repository_boundary_controls() -> tuple[int, int]:
    baseline = {
        "branch": ACTIVE_BRANCH, "head": PARENT_COMMIT, "upstream_name": UPSTREAM,
        "tracking": PARENT_COMMIT, "live_active": PARENT_COMMIT,
        "protected_local": PROTECTED_TIP, "protected_tracking": PROTECTED_TIP,
        "protected_live": PROTECTED_TIP, "main_tracking": MAIN_TIP, "main_live": MAIN_TIP,
        "origin": ORIGIN_URL, "staged": FINAL_PATH_SET, "unstaged": set(), "untracked": set(),
        "index_worktree_equal": True, "diff_check": True, "claude_changed": False,
        "production_changed": False,
    }
    cases = [
        ("branch", "wrong"), ("head", STEP80), ("upstream_name", "wrong"),
        ("tracking", STEP80), ("live_active", STEP80), ("protected_local", STEP80),
        ("protected_tracking", STEP80), ("protected_live", STEP80),
        ("main_tracking", STEP80), ("main_live", STEP80), ("origin", "wrong"),
        ("staged", set()), ("unstaged", {REPORT_PATH}), ("untracked", {REPORT_PATH}),
        ("index_worktree_equal", False), ("diff_check", False),
        ("claude_changed", True), ("production_changed", True),
    ]
    passed = 0
    require(not repository_diagnostics(baseline, precommit=True), "E_REPOSITORY_CONTROL_BASELINE")
    for field, value in cases:
        candidate = copy.deepcopy(baseline)
        candidate[field] = value
        require(repository_diagnostics(candidate, precommit=True), "E_REPOSITORY_CONTROL_ACCEPTED", field)
        passed += 1
    return passed, len(cases)


def validate_repository_artifact_state() -> None:
    snapshot = repository_snapshot()
    require(not repository_diagnostics(snapshot, precommit=False),
            "E_REPOSITORY_BASE", repr(sorted(repository_diagnostics(snapshot, precommit=False))))
    require(snapshot["staged"] | snapshot["unstaged"] | snapshot["untracked"] == FINAL_PATH_SET,
            "E_ARTIFACT_EXACT_DIRT", repr(sorted(snapshot["staged"] | snapshot["unstaged"] | snapshot["untracked"])))
    require(snapshot["diff_check"] is True, "E_ARTIFACT_DIFF_CHECK")


def validate_precommit() -> None:
    snapshot = repository_snapshot()
    errors = repository_diagnostics(snapshot, precommit=True)
    require(not errors, "E_PRECOMMIT_REPOSITORY", repr(sorted(errors)))
    transaction = name_status_records(git([
        "diff", "--cached", "--no-renames", "--name-status", "-z",
    ]).stdout)
    require(transaction == [
        {"status": status, "path": path} for status, path in FINAL_TRANSACTION
    ] and sum(record["status"] == "A" for record in transaction) == 5
            and sum(record["status"] == "M" for record in transaction) == 3,
            "E_PRECOMMIT_NAME_STATUS", repr(transaction))
    index_modes: dict[str, str] = {}
    for path in FINAL_PATHS:
        fields = git_text(["ls-files", "--stage", "--", path]).split()
        require(len(fields) >= 4 and fields[2] == "0", "E_PRECOMMIT_INDEX_ENTRY", path)
        index_modes[path] = fields[0]
    require(all(mode == "100644" for mode in index_modes.values()),
            "E_PRECOMMIT_MODES", repr(index_modes))
    for path in FINAL_PATHS:
        require(git(["show", f":{path}"]).stdout == (ROOT / path).read_bytes(),
                "E_PRECOMMIT_EXACT_BYTES", path)


def validate_persistence(expected_commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
            "E_EXPECTED_COMMIT_FORMAT", expected_commit)
    require(git_text(["branch", "--show-current"]) == ACTIVE_BRANCH, "E_PERSISTENCE_BRANCH")
    require(git_text(["rev-parse", "HEAD"]) == expected_commit, "E_PERSISTENCE_HEAD")
    require(git_text(["rev-list", "--parents", "-n", "1", expected_commit]).split()
            == [expected_commit, PARENT_COMMIT], "E_PERSISTENCE_PARENT")
    require(git_text(["show", "-s", "--format=%s", expected_commit]) == SUBJECT,
            "E_PERSISTENCE_SUBJECT")
    require(git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]) == UPSTREAM,
            "E_PERSISTENCE_UPSTREAM_NAME")
    require(git_text(["rev-parse", UPSTREAM]) == expected_commit, "E_PERSISTENCE_TRACKING")
    require(live_tip(ACTIVE_BRANCH) == expected_commit, "E_PERSISTENCE_LIVE_ACTIVE")
    require(git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]) == PROTECTED_TIP
            and git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"]) == PROTECTED_TIP
            and live_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PERSISTENCE_PROTECTED")
    require(git_text(["rev-parse", "refs/remotes/origin/main"]) == MAIN_TIP
            and live_tip("main") == MAIN_TIP, "E_PERSISTENCE_MAIN")
    require(git_text(["remote", "get-url", "origin"]) == ORIGIN_URL, "E_PERSISTENCE_ORIGIN")
    transaction = name_status_records(git([
        "diff-tree", "--no-commit-id", "--no-renames", "--name-status", "-r", "-z", expected_commit,
    ]).stdout)
    require(transaction == [
        {"status": status, "path": path} for status, path in FINAL_TRANSACTION
    ] and sum(record["status"] == "A" for record in transaction) == 5
            and sum(record["status"] == "M" for record in transaction) == 3,
            "E_PERSISTENCE_NAME_STATUS", repr(transaction))
    changed = {record["path"] for record in transaction}
    require(changed == FINAL_PATH_SET, "E_PERSISTENCE_PATHS", repr(sorted(changed)))
    require(all(mode == "100644" for mode in exact_modes(expected_commit, FINAL_PATHS).values()),
            "E_PERSISTENCE_MODES")
    require(not any(path.startswith("Claude/") or not path.startswith("Codex/") for path in changed),
            "E_PERSISTENCE_SCOPE")
    require(git(["status", "--porcelain=v1", "-z"]).stdout == b"", "E_PERSISTENCE_DIRTY")
    for path in FINAL_PATHS:
        require(git_blob(expected_commit, path) == (ROOT / path).read_bytes(),
                "E_PERSISTENCE_EXACT_BYTES", path)


def atomic_collect(raw: bytes) -> None:
    require(not ARTIFACT.exists(), "E_COLLECT_REFUSES_OVERWRITE", ARTIFACT_PATH)
    require(all((ROOT / path).is_file() for path in NONARTIFACT_PATHS),
            "E_RESULT_FIRST", "seven non-artifact paths")
    current = nul_paths(git(["diff", "--cached", "--no-renames", "--name-only", "-z"]).stdout) \
        | nul_paths(git(["diff", "--no-renames", "--name-only", "-z"]).stdout) \
        | nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout)
    require(current == set(NONARTIFACT_PATHS), "E_JSON_LAST", repr(sorted(current)))
    temp_path = ARTIFACT.with_name(ARTIFACT.name + ".tmp-step812")
    require(not temp_path.exists(), "E_COLLECT_TEMP_EXISTS", str(temp_path))
    try:
        temp_path.write_bytes(raw)
        value, _ = strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        require(pretty_bytes(value) == raw, "E_COLLECT_CANONICAL")
        os.replace(temp_path, ARTIFACT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(ARTIFACT.read_bytes() == raw, "E_COLLECT_WRITE")


def atomic_migrate_stored_history(
    raw: bytes, prior_raw: bytes, expected_document: dict[str, Any], *,
    artifact_path: pathlib.Path = ARTIFACT, inject_postwrite_failure: bool = False,
) -> None:
    target = artifact_path.resolve()
    production_target = target == ARTIFACT.resolve()
    fixture_target = (
        target.name == ARTIFACT.name and is_fixture_location(target)
        and target.parent.name.startswith("phase066-step812-migration-control-")
    )
    require(production_target or fixture_target, "E_MIGRATE_TARGET_SCOPE", str(target))
    if production_target:
        require(all((ROOT / path).is_file() for path in NONARTIFACT_PATHS),
                "E_RESULT_FIRST", "seven non-artifact paths")

    temp_path = target.with_name(target.name + ".tmp-step812-migrate")
    backup_path = target.with_name(target.name + ".bak-step812-migrate")
    target_document: dict[str, Any] | None = None
    target_raw: bytes | None = None
    if target.is_file():
        try:
            target_document, target_raw = read_stored(target)
        except ValidationError:
            target_document, target_raw = None, None

    if backup_path.exists():
        backup_document: dict[str, Any] | None = None
        backup_raw: bytes | None = None
        try:
            backup_document, backup_raw = read_stored(backup_path)
        except ValidationError:
            backup_document, backup_raw = None, None
        candidate_complete = (
            target_document is not None and target_raw == raw and target_document == expected_document
            and not document_diagnostics(target_document, expected_document)
        )
        if backup_document is not None and target_document is not None \
                and backup_raw != target_raw and not candidate_complete:
            raise ValidationError("E_MIGRATE_STALE_AMBIGUOUS", str(backup_path))
        if candidate_complete:
            if temp_path.exists():
                temp_path.unlink()
            backup_path.unlink()
            require(not temp_path.exists() and not backup_path.exists(),
                    "E_MIGRATE_RESIDUE_CLEANUP")
            if production_target:
                validate_repository_artifact_state()
            return
        if backup_document is not None and backup_raw == prior_raw:
            if temp_path.exists():
                temp_path.unlink()
            os.replace(backup_path, target)
            restored_document, restored_raw = read_stored(target)
            require(restored_raw == prior_raw and restored_document == backup_document,
                    "E_MIGRATE_STALE_RESTORE")
            target_document, target_raw = restored_document, restored_raw
        else:
            raise ValidationError("E_MIGRATE_STALE_AMBIGUOUS", str(backup_path))
    elif temp_path.exists():
        candidate_complete = (
            target_document is not None and target_raw == raw
            and not document_diagnostics(target_document, expected_document)
        )
        require(candidate_complete, "E_MIGRATE_TEMP_AMBIGUOUS", str(temp_path))
        temp_path.unlink()
        if production_target:
            validate_repository_artifact_state()
        return

    if production_target:
        validate_repository_artifact_state()
    require(target.is_file() and target.read_bytes() == prior_raw,
            "E_MIGRATE_PRIOR_BYTES")
    preserve_pre_replace = False
    guarded_target_raw: bytes | None = None
    guarded_backup_raw: bytes | None = None
    try:
        backup_path.write_bytes(prior_raw)
        backup_document, backup_raw = read_stored(backup_path)
        require(backup_raw == prior_raw and backup_path.read_bytes() == prior_raw,
                "E_MIGRATE_BACKUP_BYTES")
        temp_path.write_bytes(raw)
        value, candidate_raw = read_stored(temp_path)
        require(candidate_raw == raw and value == expected_document
                and not document_diagnostics(value, expected_document),
                "E_MIGRATE_CANDIDATE")
        guarded_target_raw = target.read_bytes() if target.is_file() else None
        guarded_backup_raw = backup_path.read_bytes() if backup_path.is_file() else None
        try:
            current_target_document, current_target_raw = read_stored(target)
            current_backup_document, current_backup_raw = read_stored(backup_path)
        except ValidationError as error:
            preserve_pre_replace = True
            raise ValidationError("E_MIGRATE_PRIOR_CHANGED", str(target)) from error
        current_candidate_complete = (
            current_target_raw == raw and current_target_document == expected_document
            and not document_diagnostics(current_target_document, expected_document)
        )
        if current_target_raw != current_backup_raw:
            if current_candidate_complete:
                temp_path.unlink()
                backup_path.unlink()
                require(not temp_path.exists() and not backup_path.exists(),
                        "E_MIGRATE_RESIDUE_CLEANUP")
                if production_target:
                    validate_repository_artifact_state()
                return
            preserve_pre_replace = True
            raise ValidationError("E_MIGRATE_STALE_AMBIGUOUS", str(backup_path))
        if current_target_raw != prior_raw or current_backup_raw != prior_raw:
            preserve_pre_replace = True
            raise ValidationError("E_MIGRATE_PRIOR_CHANGED", str(target))
        os.replace(temp_path, target)
        migrated, migrated_raw = read_stored(target)
        if inject_postwrite_failure:
            raise ValidationError("E_MIGRATE_INJECTED_POSTWRITE_FAILURE")
        require(migrated_raw == raw and migrated == expected_document
                and not document_diagnostics(migrated, expected_document),
                "E_MIGRATE_POSTWRITE")
        backup_path.unlink()
        require(not temp_path.exists() and not backup_path.exists(),
                "E_MIGRATE_RESIDUE_CLEANUP")
    except Exception:
        if preserve_pre_replace:
            if temp_path.exists():
                temp_path.unlink()
            require((target.read_bytes() if target.is_file() else None) == guarded_target_raw
                    and (backup_path.read_bytes() if backup_path.is_file() else None) == guarded_backup_raw,
                    "E_MIGRATE_CONCURRENT_BYTES_CHANGED")
            raise
        backup_usable = False
        if backup_path.is_file():
            try:
                _, rollback_raw = read_stored(backup_path)
                backup_usable = rollback_raw == prior_raw
            except ValidationError:
                backup_usable = False
        if temp_path.exists():
            temp_path.unlink()
        if backup_usable:
            os.replace(backup_path, target)
        else:
            temp_path.write_bytes(prior_raw)
            restored_candidate, restored_candidate_raw = read_stored(temp_path)
            require(restored_candidate_raw == prior_raw and type(restored_candidate) is dict,
                    "E_MIGRATE_ROLLBACK_SOURCE")
            os.replace(temp_path, target)
        restored, restored_raw = read_stored(target)
        require(restored_raw == prior_raw and type(restored) is dict,
                "E_MIGRATE_ROLLBACK_BYTES")
        if backup_path.exists():
            backup_path.unlink()
        if temp_path.exists():
            temp_path.unlink()
        require(not backup_path.exists() and not temp_path.exists(),
                "E_MIGRATE_ROLLBACK_RESIDUE")
        raise


def migration_transaction_controls(expected_document: dict[str, Any]) -> tuple[int, int]:
    root = pathlib.Path(tempfile.mkdtemp(prefix="phase066-step812-migration-control-"))
    fixture = root / ARTIFACT.name
    temp_path = fixture.with_name(fixture.name + ".tmp-step812-migrate")
    backup_path = fixture.with_name(fixture.name + ".bak-step812-migrate")
    prior_document = copy.deepcopy(expected_document)
    prior_document["generated_date"] = "2026-08-31"
    prior_document["semantic_sha256"] = semantic_hash(prior_document)
    prior_raw = pretty_bytes(prior_document)
    expected_raw = pretty_bytes(expected_document)
    passed = 0
    try:
        fixture.write_bytes(prior_raw)
        try:
            atomic_migrate_stored_history(
                expected_raw, prior_raw, expected_document, artifact_path=fixture,
                inject_postwrite_failure=True,
            )
        except ValidationError as error:
            require(error.code == "E_MIGRATE_INJECTED_POSTWRITE_FAILURE",
                    "E_MIGRATE_CONTROL_CODE", error.code)
        else:
            raise ValidationError("E_MIGRATE_CONTROL_ACCEPTED")
        restored, restored_raw = read_stored(fixture)
        require(restored_raw == prior_raw and restored == prior_document,
                "E_MIGRATE_CONTROL_ROLLBACK_BYTES")
        require(not temp_path.exists() and not backup_path.exists(),
                "E_MIGRATE_CONTROL_RESIDUE")
        passed += 1

        divergent_document = copy.deepcopy(prior_document)
        divergent_document["generated_date"] = "2026-08-30"
        divergent_document["semantic_sha256"] = semantic_hash(divergent_document)
        divergent_raw = pretty_bytes(divergent_document)
        fixture.write_bytes(prior_raw)
        backup_path.write_bytes(divergent_raw)
        require(expected_raw not in {prior_raw, divergent_raw},
                "E_MIGRATE_DIVERGENT_CONTROL_DISTINCT")
        try:
            read_migration_source(fixture)
        except ValidationError as error:
            require(error.code == "E_MIGRATE_STALE_AMBIGUOUS",
                    "E_MIGRATE_DIVERGENT_CONTROL_CODE", error.code)
        else:
            raise ValidationError("E_MIGRATE_DIVERGENT_CONTROL_ACCEPTED")
        require(fixture.read_bytes() == prior_raw and backup_path.read_bytes() == divergent_raw,
                "E_MIGRATE_DIVERGENT_CONTROL_BYTES")
        require(not temp_path.exists(), "E_MIGRATE_DIVERGENT_CONTROL_TEMP")
        passed += 1

        fixture.unlink()
        source_document, source_raw, _, proposed_document, proposed_raw = read_migration_source(fixture)
        require(source_document == divergent_document and source_raw == divergent_raw
                and proposed_raw == expected_raw and proposed_document == expected_document,
                "E_MIGRATE_TOCTOU_CONTROL_SOURCE")
        fixture.write_bytes(prior_raw)
        try:
            atomic_migrate_stored_history(
                proposed_raw, source_raw, proposed_document, artifact_path=fixture,
            )
        except ValidationError as error:
            require(error.code == "E_MIGRATE_STALE_AMBIGUOUS",
                    "E_MIGRATE_TOCTOU_CONTROL_CODE", error.code)
        else:
            raise ValidationError("E_MIGRATE_TOCTOU_CONTROL_ACCEPTED")
        require(fixture.read_bytes() == prior_raw and backup_path.read_bytes() == divergent_raw,
                "E_MIGRATE_TOCTOU_CONTROL_BYTES")
        require(not temp_path.exists(), "E_MIGRATE_TOCTOU_CONTROL_TEMP")
        passed += 1
    finally:
        remove_temp_tree(root)
    require(not root.exists(), "E_MIGRATE_CONTROL_FIXTURE_CLEANUP", str(root))
    return passed, 3


def reconstruct_migration_candidate(
    document: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], bytes]:
    history = validate_reused_history(document.get("historical_execution"))
    expected = build_document(history)
    expected_raw = pretty_bytes(expected)
    require(expected_raw == pretty_bytes(build_document(copy.deepcopy(history))),
            "E_DETERMINISM", "2/2")
    return history, expected, expected_raw


def read_migration_source(
    artifact_path: pathlib.Path = ARTIFACT,
) -> tuple[dict[str, Any], bytes, dict[str, Any], dict[str, Any], bytes]:
    target = artifact_path.resolve()
    production_target = target == ARTIFACT.resolve()
    fixture_target = (
        target.name == ARTIFACT.name and is_fixture_location(target)
        and target.parent.name.startswith("phase066-step812-migration-control-")
    )
    require(production_target or fixture_target, "E_MIGRATE_TARGET_SCOPE", str(target))
    backup_path = target.with_name(target.name + ".bak-step812-migrate")
    temp_path = target.with_name(target.name + ".tmp-step812-migrate")
    target_state: tuple[dict[str, Any], bytes] | None = None
    backup_state: tuple[dict[str, Any], bytes] | None = None
    if target.is_file():
        try:
            target_state = read_stored(target)
        except ValidationError:
            target_state = None
    if backup_path.is_file():
        try:
            backup_state = read_stored(backup_path)
        except ValidationError:
            backup_state = None

    if target_state is not None and backup_state is not None:
        target_document, target_raw = target_state
        backup_document, backup_raw = backup_state
        try:
            target_history = validate_reused_history(target_document.get("historical_execution"))
            backup_history = validate_reused_history(backup_document.get("historical_execution"))
        except ValidationError as error:
            raise ValidationError("E_MIGRATE_STALE_AMBIGUOUS", str(backup_path)) from error
        require(target_history == backup_history, "E_MIGRATE_STALE_AMBIGUOUS", str(backup_path))
        history, expected, expected_raw = reconstruct_migration_candidate(target_document)
        if target_raw == backup_raw:
            return target_document, target_raw, history, expected, expected_raw
        target_complete = (
            target_raw == expected_raw and target_document == expected
            and not document_diagnostics(target_document, expected)
        )
        require(target_complete, "E_MIGRATE_STALE_AMBIGUOUS", str(backup_path))
        return target_document, target_raw, history, expected, expected_raw

    if backup_state is not None:
        backup_document, backup_raw = backup_state
        history, expected, expected_raw = reconstruct_migration_candidate(backup_document)
        return backup_document, backup_raw, history, expected, expected_raw

    if target_state is not None:
        target_document, target_raw = target_state
        history, expected, expected_raw = reconstruct_migration_candidate(target_document)
        target_complete = (
            target_raw == expected_raw and target_document == expected
            and not document_diagnostics(target_document, expected)
        )
        require(target_complete or (not backup_path.exists() and not temp_path.exists()),
                "E_MIGRATE_STALE_AMBIGUOUS" if backup_path.exists() else "E_MIGRATE_TEMP_AMBIGUOUS",
                str(backup_path if backup_path.exists() else temp_path))
        return target_document, target_raw, history, expected, expected_raw

    raise ValidationError("E_MIGRATE_SOURCE_UNRECOVERABLE")


def read_stored(artifact_path: pathlib.Path = ARTIFACT) -> tuple[dict[str, Any], bytes]:
    require(artifact_path.is_file(), "E_VALIDATION_ARTIFACT_MISSING", str(artifact_path))
    raw = artifact_path.read_bytes()
    value, _ = strict_load_bytes(raw, str(artifact_path))
    require(type(value) is dict and pretty_bytes(value) == raw.replace(b"\r\n", b"\n"),
            "E_VALIDATION_ARTIFACT_CANONICAL")
    require(value.get("semantic_sha256") == semantic_hash(value), "E_VALIDATION_ARTIFACT_SEMANTIC")
    return value, raw


def validate_cli(
    collect: bool, migrate_stored_history: bool, mode: str, expected_commit: str | None,
) -> None:
    require(not (collect and migrate_stored_history), "E_CLI_MODE", "collect and migrate")
    require(not ((collect or migrate_stored_history) and mode != "artifact"),
            "E_CLI_MODE", "collector repository mode")
    if mode == "persistence":
        require(expected_commit is not None and re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
                "E_EXPECTED_COMMIT_FORMAT", str(expected_commit))
    else:
        require(expected_commit is None, "E_UNEXPECTED_COMMIT", str(expected_commit))


def execute(
    *, collect: bool, migrate_stored_history: bool, mode: str, expected_commit: str | None,
) -> int:
    source_nodes = validate_source_policy()
    strict_passed, strict_total = strict_json_controls()
    policy_passed, policy_total = source_policy_controls()
    human_passed, human_total = human_document_controls()
    if collect:
        require(not ARTIFACT.exists(), "E_COLLECT_REFUSES_OVERWRITE", ARTIFACT_PATH)
        require(git_text(["rev-parse", "HEAD"]) == PARENT_COMMIT, "E_COLLECT_PARENT")
        preflight_machines, _, _ = load_machine_artifacts()
        validate_cross_semantics(preflight_machines)
        validate_predecessor_commits()
        validate_human_documents()
        history = collect_historical()
        first = build_document(history)
        second = build_document(copy.deepcopy(history))
        first_raw = pretty_bytes(first)
        require(first_raw == pretty_bytes(second), "E_DETERMINISM", "2/2")
        semantic_passed, semantic_total = run_semantic_controls(first)
        gate_passed, gate_total = run_gate_controls(first["integrated_assertions"])
        repository_passed, repository_total = repository_boundary_controls()
        migration_passed, migration_total = migration_transaction_controls(first)
        atomic_collect(first_raw)
        stored, stored_raw = read_stored()
        require(stored_raw == first_raw and not document_diagnostics(stored, first),
                "E_COLLECT_POSTWRITE")
        print(f"PASS_P066_STEP81_2_NEGATIVE semantic={semantic_passed}/{semantic_total} "
              f"strict_json={strict_passed}/{strict_total} source_policy={policy_passed}/{policy_total} "
              f"human={human_passed}/{human_total} gate={gate_passed}/{gate_total} "
              f"repository_boundary={repository_passed}/{repository_total} "
              f"migration={migration_passed}/{migration_total} ast_nodes={source_nodes}")
        print("PASS_P066_STEP81_2_DETERMINISM 2/2")
        print("CONDITIONAL_P066 collect=JSON_LAST result_first=true historical=14/14 "
              "fresh_historical_replay=14/14 pass_lineage_i=false")
        return 0

    if migrate_stored_history:
        stored, prior_raw, history, first, first_raw = read_migration_source()
        second = build_document(copy.deepcopy(history))
        require(first_raw == pretty_bytes(second), "E_DETERMINISM", "2/2")
        semantic_passed, semantic_total = run_semantic_controls(first)
        gate_passed, gate_total = run_gate_controls(first["integrated_assertions"])
        repository_passed, repository_total = repository_boundary_controls()
        migration_passed, migration_total = migration_transaction_controls(first)
        atomic_migrate_stored_history(first_raw, prior_raw, first)
        migrated, migrated_raw = read_stored()
        require(migrated_raw == first_raw and not document_diagnostics(migrated, first),
                "E_MIGRATE_POSTWRITE")
        print(f"PASS_P066_STEP81_2_NEGATIVE semantic={semantic_passed}/{semantic_total} "
              f"strict_json={strict_passed}/{strict_total} source_policy={policy_passed}/{policy_total} "
              f"human={human_passed}/{human_total} gate={gate_passed}/{gate_total} "
              f"repository_boundary={repository_passed}/{repository_total} "
              f"migration={migration_passed}/{migration_total} ast_nodes={source_nodes}")
        print("PASS_P066_STEP81_2_DETERMINISM 2/2")
        print("CONDITIONAL_P066 migrate_stored_history=true json_last=true "
              "historical=CANONICAL_REUSED_14/14 fresh_historical_replay=0/14 pass_lineage_i=false")
        return 0

    stored, stored_raw = read_stored()
    history = validate_reused_history(stored.get("historical_execution"))
    expected = build_document(history)
    expected_raw = pretty_bytes(expected)
    errors = document_diagnostics(stored, expected)
    require(not errors, "E_STORED_DOCUMENT", repr(sorted(errors)))
    require(stored_raw == expected_raw, "E_STORED_BYTE_RECONSTRUCTION")
    second = build_document(copy.deepcopy(history))
    require(expected_raw == pretty_bytes(second), "E_DETERMINISM", "2/2")
    semantic_passed, semantic_total = run_semantic_controls(stored)
    gate_passed, gate_total = run_gate_controls(stored["integrated_assertions"])
    repository_passed, repository_total = repository_boundary_controls()
    migration_passed, migration_total = migration_transaction_controls(expected)
    print(f"PASS_P066_STEP81_2_NEGATIVE semantic={semantic_passed}/{semantic_total} "
          f"strict_json={strict_passed}/{strict_total} source_policy={policy_passed}/{policy_total} "
          f"human={human_passed}/{human_total} gate={gate_passed}/{gate_total} "
          f"repository_boundary={repository_passed}/{repository_total} "
          f"migration={migration_passed}/{migration_total} ast_nodes={source_nodes}")
    print("PASS_P066_STEP81_2_DETERMINISM 2/2")
    if mode == "precommit":
        validate_precommit()
        print("PASS_P066_STEP81_2_STAGED exact-eight=8/8 historical=CANONICAL_REUSED_14/14 "
              "fresh_historical_replay=0/14")
    elif mode == "persistence":
        require(expected_commit is not None, "E_EXPECTED_COMMIT")
        validate_persistence(expected_commit)
        print(f"{PERSISTENCE} commit={expected_commit} exact-eight=8/8 "
              "historical=CANONICAL_REUSED_14/14 fresh_historical_replay=0/14")
    else:
        validate_repository_artifact_state()
        print("CONDITIONAL_P066 artifact=true historical=CANONICAL_REUSED_14/14 "
              "fresh_historical_replay=0/14 pass_lineage_i=false")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--migrate-stored-history", action="store_true")
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="artifact")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    validate_cli(args.collect, args.migrate_stored_history, args.mode, args.expected_commit)
    return execute(collect=args.collect, migrate_stored_history=args.migrate_stored_history,
                   mode=args.mode, expected_commit=args.expected_commit)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError,
        json.JSONDecodeError, subprocess.TimeoutExpired,
    ) as error:
        code = error.code if isinstance(error, ValidationError) else "UNEXPECTED_VALIDATION_ERROR"
        print(f"FAIL_P066_STEP81_2 {code}: {error}")
        raise SystemExit(1)
