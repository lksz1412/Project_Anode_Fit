#!/usr/bin/env python3
"""Validate Phase 064 Step 67 evidence, Git boundary, and persistence."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any, Callable, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[3]
BUILDER = ROOT / "Codex/work/v1023_phase064/build_phase064_step67_problem_runtime_boundary.py"
CODE_PATH = ROOT / "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json"
RUNTIME_PATH = ROOT / "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json"
RESULT_PATH = ROOT / "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "0be2e45e56081e141fbd2f58be7a01b023ca16a3"
EXPECTED_SUBJECT = "audit(phase064): bound v1023 algebraic volterra runtime"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS"
PERSISTENCE = "PASS_P064_STEP67_PERSISTENCE"

EXACT_PATHS = [
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md",
    "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json",
    "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json",
    "Codex/work/v1023_phase064/build_phase064_step67_problem_runtime_boundary.py",
    "Codex/work/v1023_phase064/validate_phase064_step67.py",
]
EXACT_SET = set(EXACT_PATHS)

EXPECTED_DOC_SHA256 = {
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": "0289fc5a56577c3df380820f9911a22ec03ae0434642583d9620d85adf693264",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md": "61982f57f44015da6a73cb6afaeed94e5faf5ea89f1ef5d188cab375bd72caa5",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md": "c12d40c610d9c4b4eff54929227e8306aff6376b5820942a686b4ce111e747a5",
    "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md": "b62bb1b7d80c5da55630e4c07b96e9e3c2e0c8db62d26c1905d0933302aed5a5",
}
EXPECTED_BUILDER_GIT_BLOB = "a5de85ab9767e7396a17113d924c29d65a9dde2b"

EXPECTED_SOURCES = {
    "Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md": ("ce4b17399f8d7318b4053134959ab77f9038d313", "4c3aedabac00ac657f12bf2dffe6f696017654b883f2798c2d824ee70665b228", 20203, 225, "READ_FULL_STEP67", ((13,20),(90,113),(145,176))),
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py": ("c822c4e7ef9b8676e3a9bde675a718169ce79d5b", "a08378b555ca79f92d31bbad506e8c78551a93721cc90d705bf9390b93434783", 92292, 1500, "READ_FULL_INHERITED_STEP61_REVALIDATED_RUNTIME_STEP67", ((105,177),(481,525),(548,705))),
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": ("554425dd566c20314357eddfcf4261517df907ee", "0298bb5fdf47ed5faf2f8301b6d84dc88fd580a69c8e616daa3942d35ceae7cf", 97860, 1585, "READ_FULL_STEP67", ((99,195),(456,525),(528,545),(548,705),(796,874),(1273,1284),(1322,1365))),
    "Claude/docs/v1.0.23/test_gates_v1023.py": ("a636c6f21d97f8a1af57b61a6e4afda974b86dca", "78205fed4f6ed9ff731e11eddf14f1e871ef15759cb75344f098b8d014173832", 33361, 626, "READ_FULL_STEP67", ((1,25),(482,626))),
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": ("cf330bfc14e0291474ea9490a5b206c2f060a319", "1417277231ea795515037f470ec160e5077e04d8ab351df7e85c6467671fcef4", 6502, 128, "READ_FULL_STEP67", ((1,17),(26,128))),
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": ("b3b62159919fce6d4c4665b234d74456fa0fcf10", "279b711ef3c33b046136f7b962c76f65ccacbaca369f571ab8f3ed50524f86dc", 2866, 68, "READ_FULL_STEP67", ((1,18),(45,68))),
    "Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md": ("3c840b4a67b9c8b134c76c984efe34fba9271915", "289b59fe109318a9d42a6daa29d30e43815a45e3729baed3366688444c767cd2", 21845, 301, "READ_FULL_STEP67", ((1,25),(191,221),(269,301))),
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": ("b0e246c7bd31c63134137066d31a6032d4d190d7", "26c1546fcc701d8dec6847f1ad60cbf0ea2222808fe2aaa396265a7f8641c51c", 20019, 212, "READ_FULL_STEP67", ((19,27),(29,70),(72,135),(162,198))),
    "Claude/docs/v1.0.23/_sections/ch1_sec01_n0n1.tex": ("9648c33e724f4bb762924ff20ba775ec568d4bf0", "e040962075e33f1222128e4f86f4d474ca24e970f5285392fafa904d3c33075d", 23690, 257, "READ_FULL_STEP67", ((9,22),)),
    "Claude/docs/v1.0.23/_sections/ch1_sec02b_part0.tex": ("e9c17ce0e2b23e85843f70bfc8e6132e5154ae69", "e1d4db7c30581d70f91c38ebd72433699fc54a0e4883345ebbe55e31073e000d", 39502, 474, "READ_BOUNDED_STEP67_FULL_INHERITED_STEP64", ((320,385),)),
    "Claude/docs/v1.0.23/_sections/ch1_sec06_eqpeak.tex": ("4f96ebdd20e80601086c4aa0ddb8c3a653a9095f", "98537969a8a86f323b312489ca33c2b8c6e4549392a8ad2ea7b23456d87f0726", 7092, 89, "READ_FULL_STEP67", ((1,45),)),
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": ("15cd3c78f37dea9a1b942108d01df3db62101a6f", "a01c5394781f3674fb167846d1acc05a49c7ec2f4c419c7480a128b1c0747723", 10884, 145, "READ_FULL_STEP67", ((1,96),(107,145))),
    "Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex": ("490139d35601c8d83da6d567bcdcf2ac97619d1c", "7fed61f947f974c21f58361519ae9cc3511ac633c3869503243a70f9cf0eef49", 18372, 245, "READ_FULL_STEP67", ((1,65),(91,190),(229,245))),
    "Claude/docs/v1.0.23/_sections/ch3v22_sec03_blend.tex": ("4966fa1ffbe31364b3b87ba387cd4d439cf658a5", "231c7a2ba10c06ba2493cc812c9cc75500b3e297fa00534e5900112b7366d7a7", 29787, 278, "READ_BOUNDED_STEP67_FULL_INHERITED_STEP64", ((69,115),(229,278))),
}

EXPECTED_READ_COVERAGE = {
    "Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md": [1,225],
    "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py": [1,1500],
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": [1,1585],
    "Claude/docs/v1.0.23/test_gates_v1023.py": [1,626],
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": [1,128],
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": [1,68],
    "Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md": [1,301],
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": [1,212],
    "Claude/docs/v1.0.23/_sections/ch1_sec01_n0n1.tex": [1,257],
    "Claude/docs/v1.0.23/_sections/ch1_sec02b_part0.tex": [[188,217],[282,418]],
    "Claude/docs/v1.0.23/_sections/ch1_sec06_eqpeak.tex": [1,89],
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": [1,145],
    "Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex": [1,245],
    "Claude/docs/v1.0.23/_sections/ch3v22_sec03_blend.tex": [[1,133],[229,278]],
}
EXPECTED_FINDINGS_SHA256 = "9466dceb802190b5a3b53bdf2e78a77599b1508b9f9b309de8801de422ef8082"
EXPECTED_CLASSES_SHA256 = "8bdb94cb2525e5649045faefec553bac5ea99e04a55990f1643cd2be2c006bd5"
EXPECTED_MAPS_SHA256 = "570fe4ff3bdacccdee2bbbd15ced5d0978c6b133910f17fa12a354e0eff44290"
EXPECTED_CALL_EDGES_SHA256 = "56de5c9a12d4d788d92390e68ca1a1bc9482c2965a572900440ff47bdd055209"
EXPECTED_NON_DOUBLE_COUNT_SHA256 = "dac660a694b23929f32b141ffc6694d24ad089e2afc08fea60d8b15540d0a055"
EXPECTED_OMEGA_PARTITION_SHA256 = "c1fe08f5a65ce4acd6bda0f5995eb098d1a1ff564fa557bf253085ab6d817340"
EXPECTED_REGULAR_SOLUTION_SHA256 = "3b7ba9b7f2ca9b87e2299a88e64f4749181f982c7efd48d4b90f7c9e93ded27b"
EXPECTED_INHERITED_JOINS_SHA256 = "fa8b5e1246ce481dd339f4dcb166e14ae7ce2c61fe9d5eb0a1143a7055197a23"
EXPECTED_SOURCES_SHA256 = "b7cc3300812323e431660799dfa5dd86a3ad450b714c11e9614b4766ccde2b0c"
EXPECTED_RUNS_SHA256 = "3df5e6c979dbb7bfc285def09cba26e5a275362c688f097157cdbe086b8641c6"
EXPECTED_PROBE_PROGRAM_SHA256 = "d80a76c3949ab7215ae6ae8692bed62723336b22c49bcfd778896b24c5f34cff"
EXPECTED_PROBE_RESULTS_SHA256 = "07952eac0c8b666a7d257a33caf0ee1dd5ef53ee9c116e99e01736a44b3cccb5"
EXPECTED_RUNTIME_ROWS_SHA256 = "89d2a6cad12b94a182e4aad5e15ef10f44c5573763a7cc371195ca812655ac31"
EXPECTED_ISOLATION_SHA256 = "43871e90ee5acd1ff71fc847b313c18e022204615d55fcd0c573065d7d29d586"
EXPECTED_RUNTIME_EVIDENCE_SHA256 = "8b208d33af52d91a00806b64251c375ba7efdb928a0964bc17f25677654b7da2"
EXPECTED_CODE_TYPE_PROJECTION_SHA256 = "b488da5c54e2506d331f8673efcf0f0ca167c866f49b10f131ff2d5237511d20"
EXPECTED_RUNTIME_TYPE_PROJECTION_SHA256 = "2f7eafff45f1cb507769dc7cd68ec5ea2f3246df0d7d9ee58d0d7158efb553b5"
EXPECTED_VALIDATOR_CANONICAL_SHA256 = "bdc903d7bcb566948aa0946cf60d49db893cd912522057c63c7b24b9a7c85bb6"
EXPECTED_VALIDATOR_AST_SHA256_312 = "5e18f42b75221c994bcbd58d8fc4b52057e7dc01d2604d6eb0a928984b235edb"
EXPECTED_VALIDATOR_AST_SHA256_314 = "30587f7c93a77191d9773e18768f0f140728c03b7d8ad43209dc978f12936554"

SOURCE_ROW_KEYS = {"path","git_blob","sha256","bytes","lines","read_coverage","read_status","source_spans"}
FINDING_ROW_KEYS = {"id","priority","status","owner","finding","frozen_source_modified","external_truth_validated"}
RUN_ROW_KEYS = {"authority","command","cwd","diagnostic","encoding","exit_code","expectation_met","expected_state","external_truth","run_id","runtime","stderr_sha256","stderr_tail","stdout_sha256","stdout_tail"}
PROBE_ROW_KEYS = {"probe_sha256","results","runtime"}
ISOLATION_KEYS = {"baseline_claude_tree","branch","bytecode_disabled","claude_clean_before_after","copied_git_blobs_only","copy_manifest","disposable_cleanup_verified","disposable_external_directories","head","head_claude_tree","network_used","production_imported_by_builder","production_imported_by_validator","production_imported_only_by_child_subprocess","repository_projection_equal_before_after","repository_projection_hash_scope","repository_projection_before_sha256","repository_projection_after_sha256"}
MAP_ROW_KEYS = {"id","problem_class","source_equation","operation","domain","directionality","boundary_initial_condition","variable_map","dimension_unit","limiting_recovery","non_applicable_target","code_symbol","status","evidence"}
BOUND_SPAN_KEYS = {"path","start","end","sha256"}
RUNTIME_ROW_KEYS = {"runtime","python_version","numpy_version","launcher"}
MANIFEST_ROW_KEYS = {"path","git_blob","sha256","bytes","lines"}
RUNTIME_EVIDENCE_ROW_KEYS = {"runtime","frozen_blobs","invocation","environment","input_sha256","output_sha256","metric","tolerance","complexity_observation","repository_before_after_projection","cleanup_state","authority_ceiling"}
FROZEN_BLOB_ROW_KEYS = {"path","git_blob","sha256"}
PROBE_SECTION_KEYS = {
    "option_boundary": {"authority","experimental_truth","g_eff_zero_on_equals_off","material_truth","pass","ratio_liveness_max_abs_diff","v22_default_equals_v23_default","v23_default_equals_explicit_false"},
    "picard_identity": {"authority","claim_ceiling","experimental_truth","g_eff","material_truth","pass","ratio_vs_manual_first_picard_max_abs_diff"},
    "timebase": {"authority","captured_curve_capacity_Ah","captured_curve_current_A","experimental_truth","lag_raw_V","lag_raw_over_corrected","lag_si_corrected_V","material_truth","normalized_rate_raw_per_h_numeric","normalized_rate_si_per_s","pass","si_capacity_C","si_current_A_unchanged"},
    "transfer": {"authority","circular_wrap_first_value_abs","coordinate","experimental_truth","manual_fft_max_abs_diff","material_truth","nonuniform_grid_rejected","nonuniform_output_finite","pass"},
    "initial_condition": {"authority","experimental_truth","finite_initial_state_parameter_present","finite_window_restart_after_100_abs_gap","finite_window_restart_start_abs_gap","material_truth","pass","pointwise_first_equals_equilibrium_first","ratio_first_equals_equilibrium_first"},
}

CODE_KEYS = {
    "artifact_kind", "authority", "baseline_commit", "call_edges", "counts",
    "equation_code_map", "expected_parent", "expected_subject", "findings",
    "gate", "generated_by", "generated_date", "human_evidence",
    "human_evidence_semantic_sha256", "inherited_joins", "non_double_count",
    "omega_consumer_partition", "phase", "phase_ceiling", "problem_classes",
    "regular_solution_occupancy", "schema", "semantic_sha256", "source_contracts",
    "source_mutation_count", "status", "step",
}
RUNTIME_KEYS = {
    "artifact_kind", "authority", "baseline_commit", "counts", "expected_parent",
    "expected_subject", "gate", "generated_by", "generated_date",
    "independent_probes", "isolation", "official_and_mutation_runs", "phase",
    "phase_ceiling", "runtimes", "schema", "semantic_sha256",
    "source_mutation_count", "status", "step", "runtime_evidence_rows",
}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(f"{code}{':' + detail if detail else ''}")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def json_type_projection(value: Any) -> Any:
    value_type = type(value)
    if value_type is dict:
        return {"object": [[key, json_type_projection(value[key])] for key in sorted(value)]}
    if value_type is list:
        return {"array": [json_type_projection(child) for child in value]}
    if value_type is str:
        return "string"
    if value_type is bool:
        return "boolean"
    if value_type is int:
        return "integer"
    if value_type is float:
        return "number"
    if value is None:
        return "null"
    raise ValidationError(f"E_JSON_UNSUPPORTED_TYPE:{value_type.__name__}")


def json_type_sha256(value: Any) -> str:
    return sha256(compact_bytes(json_type_projection(value)))


def finalize_type_errors(errors: list[str], type_code: str) -> list[str]:
    unique = set(errors)
    if type_code in unique and len(unique) > 1:
        unique.remove(type_code)
    return sorted(unique)


SELF_ASSIGNMENTS = {
    "EXPECTED_VALIDATOR_CANONICAL_SHA256": "<SELF_CANONICAL_SHA256>",
    "EXPECTED_VALIDATOR_AST_SHA256_312": "<SELF_AST_SHA256_312>",
    "EXPECTED_VALIDATOR_AST_SHA256_314": "<SELF_AST_SHA256_314>",
}


def canonical_validator_source(raw: bytes) -> bytes:
    text_value = raw.decode("utf-8", "strict")
    for name, token in SELF_ASSIGNMENTS.items():
        pattern = rf'^{name} = "[0-9a-f]{{64}}"$'
        text_value, count = re.subn(pattern, f'{name} = "{token}"', text_value, count=1, flags=re.MULTILINE)
        require(count == 1, "E_VALIDATOR_SOURCE_POLICY", name)
    return text_value.encode("utf-8")


class SelfAssignmentNormalizer(ast.NodeTransformer):
    def visit_Assign(self, node: ast.Assign) -> ast.AST:
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in SELF_ASSIGNMENTS:
                node.value = ast.copy_location(ast.Constant(SELF_ASSIGNMENTS[name]), node.value)
        return self.generic_visit(node)


def canonical_validator_ast(raw: bytes) -> bytes:
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=__file__)
    normalized = SelfAssignmentNormalizer().visit(tree)
    ast.fix_missing_locations(normalized)
    return ast.dump(normalized, annotate_fields=True, include_attributes=False).encode("utf-8")


def validator_identity_errors(raw: bytes) -> list[str]:
    errors: list[str] = []
    if b"\r\n" in raw: errors.append("E_VALIDATOR_CRLF")
    try:
        if sha256(canonical_validator_source(raw)) != EXPECTED_VALIDATOR_CANONICAL_SHA256: errors.append("E_VALIDATOR_SOURCE_SHA")
        runtime_key = f"{sys.version_info.major}.{sys.version_info.minor}"
        expected_ast_sha256 = {
            "3.12": EXPECTED_VALIDATOR_AST_SHA256_312,
            "3.14": EXPECTED_VALIDATOR_AST_SHA256_314,
        }.get(runtime_key)
        if expected_ast_sha256 is None:
            errors.append("E_VALIDATOR_SOURCE_POLICY")
        elif sha256(canonical_validator_ast(raw)) != expected_ast_sha256:
            errors.append("E_VALIDATOR_AST_SHA")
    except (SyntaxError, UnicodeDecodeError, ValidationError, ValueError):
        errors.append("E_VALIDATOR_SOURCE_POLICY")
    return sorted(set(errors))


def traverse(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(1 + traverse(child) for child in value.values())
    if isinstance(value, list):
        return 1 + sum(traverse(child) for child in value)
    return 1


def strict_load_bytes(raw: bytes, source: str) -> tuple[Any, int]:
    duplicate: list[str] = []

    def hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                duplicate.append(key)
            out[key] = value
        return out

    def bad_constant(value: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{source}:{value}")

    try:
        value = json.loads(raw, object_pairs_hook=hook, parse_constant=bad_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValidationError(f"E_JSON_PARSE:{source}:{exc}") from exc
    require(not duplicate, "E_JSON_DUPLICATE", f"{source}:{duplicate}")

    def finite(node: Any) -> None:
        if isinstance(node, float) and not math.isfinite(node):
            raise ValidationError(f"E_JSON_NUMERIC_OVERFLOW:{source}")
        if isinstance(node, dict):
            for child in node.values(): finite(child)
        elif isinstance(node, list):
            for child in node: finite(child)
    finite(value)
    return value, traverse(value)


def strict_load(path: pathlib.Path) -> tuple[dict[str, Any], int, bytes]:
    raw = path.read_bytes()
    value, nodes = strict_load_bytes(raw, path.as_posix())
    require(isinstance(value, dict), "E_JSON_ROOT", path.as_posix())
    return value, nodes, raw


def git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        cp = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"E_GIT_TIMEOUT:{' '.join(args)}") from exc
    if check and cp.returncode:
        raise ValidationError(f"E_GIT_COMMAND:{' '.join(args)}:{cp.returncode}:{cp.stderr.decode('utf-8','replace').strip()}")
    return cp


def git_text(*args: str) -> str:
    return git(list(args)).stdout.decode("utf-8", "strict").strip()


def git_bytes(path: str) -> bytes:
    return git(["show", f"{BASELINE}:{path}"]).stdout


def live_tip(branch: str) -> str:
    out = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    require(bool(out), "E_LIVE_REMOTE_MISSING", branch)
    return out.split()[0]


def line_span_hash(raw: bytes, start: int, end: int) -> str:
    lines = raw.decode("utf-8", "strict").splitlines(keepends=True)
    require(1 <= start <= end <= len(lines), "E_SOURCE_SPAN_RANGE")
    return sha256("".join(lines[start-1:end]).encode("utf-8"))


def rehash(payload: dict[str, Any]) -> None:
    payload.pop("semantic_sha256", None)
    payload["semantic_sha256"] = sha256(compact_bytes(payload))


def code_errors(p: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if json_type_sha256(p) != EXPECTED_CODE_TYPE_PROJECTION_SHA256: errors.append("E_CODE_TYPES")
    if set(p) != CODE_KEYS: errors.append("E_CODE_ROOT_KEYS")
    if (p.get("artifact_kind"), p.get("schema"), p.get("phase"), p.get("step")) != ("PHASE_064_V1023_PROBLEM_CODE_DELTA",1,64,67): errors.append("E_CODE_IDENTITY")
    if (p.get("baseline_commit"),p.get("expected_parent"),p.get("expected_subject"),p.get("gate"),p.get("phase_ceiling")) != (BASELINE,EXPECTED_PARENT,EXPECTED_SUBJECT,GATE,"CONDITIONAL_P064"): errors.append("E_CONTROL_FIELDS")
    if (p.get("generated_date"),p.get("generated_by"),p.get("status")) != ("2026-08-29","build_phase064_step67_problem_runtime_boundary.py","RESULT_FIRST_PRECOMMIT_EVIDENCE"): errors.append("E_CODE_PROVENANCE")
    human = {"algebraic_problem_classes":2,"baseline_commit":BASELINE,"finding_summary":{"P0":1,"P1":5,"P2":3},"gate":GATE,"phase_ceiling":"CONDITIONAL_P064","problem_classes":3,"ratio_applicable_classes":1,"runtime_sets":2}
    if p.get("human_evidence") != human or p.get("human_evidence_semantic_sha256") != sha256(compact_bytes(human)): errors.append("E_HUMAN_EVIDENCE")
    if p.get("counts") != {"problem_classes":3,"ratio_applicable":1,"algebraic":2,"P0":1,"P1":5,"P2":3}: errors.append("E_COUNTS")
    classes = p.get("problem_classes", [])
    expected_classes = [
        ("P064-S67-CLASS-001","CHARGE_BALANCE_ALGEBRAIC_ROOT"),
        ("P064-S67-CLASS-002","BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY"),
        ("P064-S67-CLASS-003","CAUSAL_LAG_VOLTERRA_ODE"),
    ]
    if [(r.get("id"),r.get("name")) for r in classes] != expected_classes: errors.append("E_CLASS_SET")
    if len(classes) == 3 and [r.get("ratio_reference_applicable") for r in classes] != [False,False,True]: errors.append("E_CLASS_RATIO_APPLICABILITY")
    if len(classes) >= 2 and classes[1].get("solver_symbol") is not None: errors.append("E_BACKGROUND_SOLVER")
    if not any(error in {"E_CLASS_SET","E_CLASS_RATIO_APPLICABILITY","E_BACKGROUND_SOLVER"} for error in errors) and sha256(compact_bytes(classes)) != EXPECTED_CLASSES_SHA256: errors.append("E_CLASS_CONTRACT")
    non_double = p.get("non_double_count",{})
    if non_double.get("classification") != "BASELINE_PLUS_STATE_DEVIATION_NOT_DUPLICATE_TOTAL_TERM": errors.append("E_OMEGA_NON_DOUBLE_COUNT")
    elif sha256(compact_bytes(non_double)) != EXPECTED_NON_DOUBLE_COUNT_SHA256: errors.append("E_OMEGA_NON_DOUBLE_COUNT_CONTRACT")
    regular = p.get("regular_solution_occupancy",{})
    if regular.get("implicit_omega_nonzero_equilibrium_implemented") is not False: errors.append("E_REGULAR_SOLUTION_FALSE_IMPLEMENTED")
    elif sha256(compact_bytes(regular)) != EXPECTED_REGULAR_SOLUTION_SHA256: errors.append("E_REGULAR_SOLUTION_CONTRACT")
    omega = p.get("omega_consumer_partition",[])
    if len(omega) != 3 or sha256(compact_bytes(omega)) != EXPECTED_OMEGA_PARTITION_SHA256: errors.append("E_OMEGA_PARTITION")
    edges = p.get("call_edges",[])
    if len(edges) != 5 or sha256(compact_bytes(edges)) != EXPECTED_CALL_EDGES_SHA256: errors.append("E_CALL_EDGES")
    maps = {row.get("id"): row for row in p.get("equation_code_map",[])}
    if maps.get("P064-S67-MAP-007",{}).get("status") != "CONFLICT_HOUR_TO_SECOND_CONVERSION_MISSING": errors.append("E_TIMEBASE_STATIC")
    if maps.get("P064-S67-MAP-006",{}).get("status") != "VOLTAGE_COORDINATE_CIRCULAR_DFT_UNIFORMITY_UNENFORCED": errors.append("E_TRANSFER_STATIC")
    map_rows = p.get("equation_code_map",[])
    if [row.get("id") for row in map_rows] != [f"P064-S67-MAP-{i:03d}" for i in range(1,8)]: errors.append("E_MAP_SET")
    elif any(set(row) != MAP_ROW_KEYS for row in map_rows): errors.append("E_MAP_ROW_KEYS")
    elif any(not isinstance(row.get("evidence"),dict) or not {"equation_sources","code_sources"}.issubset(row["evidence"]) or not set(row["evidence"]).issubset({"equation_sources","code_sources","applicability_sources"}) or any(not isinstance(bounds,list) or not bounds or any(not isinstance(bound,dict) or set(bound) != BOUND_SPAN_KEYS for bound in bounds) for bounds in row["evidence"].values()) for row in map_rows): errors.append("E_MAP_BINDING")
    elif not any(error in {"E_TIMEBASE_STATIC","E_TRANSFER_STATIC"} for error in errors) and sha256(compact_bytes(map_rows)) != EXPECTED_MAPS_SHA256: errors.append("E_MAP_CONTRACT")
    findings = p.get("findings", [])
    if [r.get("id") for r in findings] != [f"P064-S67-F{i:03d}" for i in range(1,10)]: errors.append("E_FINDING_SET")
    elif Counter(r.get("priority") for r in findings) != Counter({"P0":1,"P1":5,"P2":3}): errors.append("E_FINDING_PRIORITY")
    elif any(set(row) != FINDING_ROW_KEYS for row in findings) or sha256(compact_bytes(findings)) != EXPECTED_FINDINGS_SHA256: errors.append("E_FINDING_CONTRACT")
    joins = p.get("inherited_joins",[])
    if len(joins) != 4 or any(row.get("duplicate_new_finding") is not False for row in joins) or sha256(compact_bytes(joins)) != EXPECTED_INHERITED_JOINS_SHA256: errors.append("E_INHERITED_JOIN")
    authority = {"static_internal_concordance":True,"runtime_internal_concordance":False,"material_truth":False,"experimental_truth":False,"external_primary_literature_truth":False,"canonical_adoption":False,"publication_readiness":False}
    if p.get("authority") != authority: errors.append("E_AUTHORITY")
    if p.get("source_mutation_count") != 0: errors.append("E_SOURCE_MUTATION")
    sources = p.get("source_contracts",[])
    if {row.get("path") for row in sources} != set(EXPECTED_SOURCES): errors.append("E_SOURCE_SET")
    else:
        for row in sources:
            path = row["path"]
            blob, digest, size, lines, status, ranges = EXPECTED_SOURCES[path]
            if set(row) != SOURCE_ROW_KEYS: errors.append("E_SOURCE_ROW_KEYS"); break
            if (row.get("git_blob"),row.get("sha256"),row.get("bytes"),row.get("lines"),row.get("read_status")) != (blob,digest,size,lines,status): errors.append("E_SOURCE_IDENTITY"); break
            if row.get("read_coverage") != EXPECTED_READ_COVERAGE[path]: errors.append("E_SOURCE_READ_COVERAGE"); break
            spans = row.get("source_spans",[])
            if any(set(x) != {"start","end","sha256"} for x in spans) or [(x.get("start"),x.get("end")) for x in spans] != list(ranges): errors.append("E_SOURCE_SPANS"); break
        if not errors or not any(error.startswith("E_SOURCE_") for error in errors):
            if sha256(compact_bytes(sources)) != EXPECTED_SOURCES_SHA256: errors.append("E_SOURCE_CONTRACT")
    if p.get("semantic_sha256") != sha256(compact_bytes({k:v for k,v in p.items() if k != "semantic_sha256"})): errors.append("E_SEMANTIC_SHA")
    return finalize_type_errors(errors, "E_CODE_TYPES")


def runtime_errors(p: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if json_type_sha256(p) != EXPECTED_RUNTIME_TYPE_PROJECTION_SHA256: errors.append("E_RUNTIME_TYPES")
    if set(p) != RUNTIME_KEYS: errors.append("E_RUNTIME_ROOT_KEYS")
    if (p.get("artifact_kind"),p.get("schema"),p.get("phase"),p.get("step")) != ("PHASE_064_V1023_RUNTIME_ATTESTATION",1,64,67): errors.append("E_RUNTIME_IDENTITY")
    if (p.get("baseline_commit"),p.get("expected_parent"),p.get("expected_subject"),p.get("gate"),p.get("phase_ceiling")) != (BASELINE,EXPECTED_PARENT,EXPECTED_SUBJECT,GATE,"CONDITIONAL_P064"): errors.append("E_CONTROL_FIELDS")
    if (p.get("generated_date"),p.get("generated_by"),p.get("status")) != ("2026-08-29","build_phase064_step67_problem_runtime_boundary.py","RESULT_FIRST_PRECOMMIT_EVIDENCE"): errors.append("E_RUNTIME_PROVENANCE")
    if p.get("counts") != {"runtimes":2,"runs":10,"run_expectations_met":10,"probe_runtime_sets":2,"probe_sections_per_runtime":5,"runtime_evidence_rows":2}: errors.append("E_RUNTIME_COUNTS")
    runtimes = p.get("runtimes",[])
    if [(r.get("runtime"),r.get("python_version"),r.get("numpy_version")) for r in runtimes] != [("3.12","3.12.10","2.3.5"),("3.14","3.14.4","2.5.0")]: errors.append("E_RUNTIME_VERSIONS")
    elif any(set(row) != RUNTIME_ROW_KEYS for row in runtimes) or sha256(compact_bytes(runtimes)) != EXPECTED_RUNTIME_ROWS_SHA256: errors.append("E_RUNTIME_ROW_CONTRACT")
    expected_runs = [f"P064-S67-{case}-{runtime}" for runtime in ("3.12","3.14") for case in ("SC-UTF8","SC-WRONG-CWD","P1-UTF8","P1-CP949","SC-VERSION-MUTATION")]
    runs = p.get("official_and_mutation_runs",[])
    if [r.get("run_id") for r in runs] != expected_runs: errors.append("E_RUN_SET")
    elif any(set(row) != RUN_ROW_KEYS for row in runs): errors.append("E_RUN_CONTRACT")
    elif any(row.get("authority") != "INTERNAL_EXECUTION_ONLY" or row.get("external_truth") is not False for row in runs): errors.append("E_RUN_AUTHORITY")
    elif any(r.get("expectation_met") is not True for r in runs): errors.append("E_RUN_MATRIX")
    else:
        matrix_bad = False
        for row in runs:
            rid = row["run_id"]
            if "WRONG-CWD" in rid and not (row.get("expected_state") == "FAIL_WRONG_CWD" and row.get("exit_code") != 0 and row.get("diagnostic") == "FILE_NOT_FOUND_CWD_RELATIVE_LOAD"): matrix_bad = True
            if "CP949" in rid and not (row.get("expected_state") == "FAIL_CP949" and row.get("exit_code") != 0 and row.get("diagnostic") == "UNICODE_ENCODE_ERROR_CP949" and row.get("encoding") == "cp949"): matrix_bad = True
            if ("SC-UTF8" in rid or "P1-UTF8" in rid or "VERSION-MUTATION" in rid) and not (row.get("expected_state") == "PASS" and row.get("exit_code") == 0 and row.get("diagnostic") is None and row.get("encoding") == "utf-8"): matrix_bad = True
        if matrix_bad: errors.append("E_RUN_MATRIX")
        elif sha256(compact_bytes(runs)) != EXPECTED_RUNS_SHA256: errors.append("E_RUN_CONTRACT")
    isolation = p.get("isolation",{})
    required_true = ("production_imported_only_by_child_subprocess","copied_git_blobs_only","disposable_external_directories","bytecode_disabled","repository_projection_equal_before_after","disposable_cleanup_verified","claude_clean_before_after")
    if set(isolation) != ISOLATION_KEYS: errors.append("E_ISOLATION_KEYS")
    elif any(isolation.get(k) is not True for k in required_true) or isolation.get("production_imported_by_builder") is not False or isolation.get("production_imported_by_validator") is not False or isolation.get("network_used") is not False: errors.append("E_ISOLATION")
    if isolation.get("head") != EXPECTED_PARENT or isolation.get("baseline_claude_tree") != isolation.get("head_claude_tree"): errors.append("E_REPO_PROJECTION")
    manifest = isolation.get("copy_manifest",[])
    expected_copy = {"Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py","Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py","Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py","Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py"}
    if {r.get("path") for r in manifest} != expected_copy: errors.append("E_RUNTIME_SOURCE_SET")
    else:
        for row in manifest:
            if set(row) != MANIFEST_ROW_KEYS: errors.append("E_RUNTIME_SOURCE_ROW_KEYS"); break
            expected = EXPECTED_SOURCES[row["path"]]
            if (row.get("git_blob"),row.get("sha256"),row.get("bytes"),row.get("lines")) != expected[:4]: errors.append("E_RUNTIME_SOURCE_IDENTITY"); break
    if not any(error.startswith(("E_ISOLATION","E_REPO_PROJECTION","E_RUNTIME_SOURCE")) for error in errors) and sha256(compact_bytes(isolation)) != EXPECTED_ISOLATION_SHA256: errors.append("E_ISOLATION_CONTRACT")
    probes = p.get("independent_probes",[])
    if [r.get("runtime") for r in probes] != ["3.12","3.14"]: errors.append("E_PROBE_SET")
    else:
        for probe in probes:
            if set(probe) != PROBE_ROW_KEYS: errors.append("E_PROBE_ROW_KEYS"); continue
            if probe.get("probe_sha256") != EXPECTED_PROBE_PROGRAM_SHA256: errors.append("E_PROBE_PROGRAM"); continue
            result = probe.get("results",{})
            if set(result) != set(PROBE_SECTION_KEYS) or any(set(result.get(name,{})) != keys for name,keys in PROBE_SECTION_KEYS.items()): errors.append("E_PROBE_SECTION_KEYS"); continue
            if any(section.get("authority") != "ISOLATED_INTERNAL_RUNTIME_ONLY" or section.get("material_truth") is not False or section.get("experimental_truth") is not False for section in result.values()): errors.append("E_PROBE_AUTHORITY"); continue
            option = result.get("option_boundary",{})
            if not all(option.get(k) is True for k in ("v22_default_equals_v23_default","v23_default_equals_explicit_false","g_eff_zero_on_equals_off","pass")) or not option.get("ratio_liveness_max_abs_diff",0)>1e-9: errors.append("E_OPTION_BOUNDARY")
            picard = result.get("picard_identity",{})
            if picard.get("claim_ceiling") != "FIRST_PICARD_ITERATE_ONLY" or not picard.get("ratio_vs_manual_first_picard_max_abs_diff",1)<1e-13 or picard.get("pass") is not True: errors.append("E_PICARD_CEILING")
            timebase = result.get("timebase",{})
            if not (math.isclose(timebase.get("lag_raw_over_corrected",0),3600.0,rel_tol=0,abs_tol=1e-8) and timebase.get("pass") is True and timebase.get("captured_curve_current_A") == 2.0 and timebase.get("si_current_A_unchanged") == 2.0 and timebase.get("captured_curve_capacity_Ah") == 2.0 and timebase.get("si_capacity_C") == 7200.0 and math.isclose(timebase.get("normalized_rate_si_per_s",0),1/3600,rel_tol=0,abs_tol=1e-18)): errors.append("E_TIMEBASE_3600")
            transfer = result.get("transfer",{})
            if not transfer.get("manual_fft_max_abs_diff",1)<1e-13: errors.append("E_TRANSFER_IDENTITY")
            if transfer.get("nonuniform_grid_rejected") is not False or transfer.get("nonuniform_output_finite") is not True: errors.append("E_UNIFORM_GRID_FALSE_ENFORCED")
            if not transfer.get("circular_wrap_first_value_abs",0)>0.0 or transfer.get("coordinate") != "VOLTAGE_ONLY" or transfer.get("pass") is not True: errors.append("E_TRANSFER_CIRCULAR")
            initial = result.get("initial_condition",{})
            if initial.get("finite_initial_state_parameter_present") is not False or not initial.get("finite_window_restart_start_abs_gap",0)>1e-3 or initial.get("pass") is not True: errors.append("E_INITIAL_CONDITION")
        if len(probes) == 2 and not any(error.startswith("E_PROBE_") or error in {"E_OPTION_BOUNDARY","E_PICARD_CEILING","E_TIMEBASE_3600","E_TRANSFER_IDENTITY","E_UNIFORM_GRID_FALSE_ENFORCED","E_TRANSFER_CIRCULAR","E_INITIAL_CONDITION"} for error in errors):
            if probes[0]["results"] != probes[1]["results"]: errors.append("E_PROBE_CROSS_RUNTIME")
            elif any(sha256(compact_bytes(probe["results"])) != EXPECTED_PROBE_RESULTS_SHA256 for probe in probes): errors.append("E_PROBE_CONTRACT")
    evidence_rows = p.get("runtime_evidence_rows",[])
    if [row.get("runtime") for row in evidence_rows] != ["3.12","3.14"]: errors.append("E_RUNTIME_EVIDENCE_SET")
    elif any(set(row) != RUNTIME_EVIDENCE_ROW_KEYS for row in evidence_rows): errors.append("E_RUNTIME_EVIDENCE_KEYS")
    else:
        expected_frozen = [{"path":row["path"],"git_blob":row["git_blob"],"sha256":row["sha256"]} for row in manifest]
        probes_by_runtime = {row["runtime"]: row for row in probes}
        runtimes_by_runtime = {row["runtime"]: row for row in runtimes}
        probe_diagnostic_present = any(error.startswith("E_PROBE_") or error in {"E_OPTION_BOUNDARY","E_PICARD_CEILING","E_TIMEBASE_3600","E_TRANSFER_IDENTITY","E_UNIFORM_GRID_FALSE_ENFORCED","E_TRANSFER_CIRCULAR","E_INITIAL_CONDITION"} for error in errors)
        runtime_source_diagnostic_present = any(error.startswith("E_RUNTIME_SOURCE") for error in errors)
        evidence_bad = False
        for row in evidence_rows:
            runtime = row["runtime"]
            invocation = ["py",f"-{runtime}","-B","-I","-X","utf8","<EXTERNAL>/step67_probe.py","<EXTERNAL>/v1.0.22/Anode_Fit_v1.0.22.py","<EXTERNAL>/v1.0.23/Anode_Fit_v1.0.23.py"]
            env = row.get("environment",{})
            projection = row.get("repository_before_after_projection",{})
            if (not runtime_source_diagnostic_present and row.get("frozen_blobs") != expected_frozen) or any(not isinstance(blob,dict) or set(blob) != FROZEN_BLOB_ROW_KEYS for blob in row.get("frozen_blobs",[])): evidence_bad = True
            if row.get("invocation") != invocation: evidence_bad = True
            if set(env) != {"python_version","numpy_version","PYTHONDONTWRITEBYTECODE","PYTHONIOENCODING","isolated_mode","network_used"}: evidence_bad = True
            elif (env.get("python_version"),env.get("numpy_version"),env.get("PYTHONDONTWRITEBYTECODE"),env.get("PYTHONIOENCODING"),env.get("isolated_mode"),env.get("network_used")) != (runtimes_by_runtime[runtime]["python_version"],runtimes_by_runtime[runtime]["numpy_version"],"1","utf-8",True,False): evidence_bad = True
            if not probe_diagnostic_present and row.get("output_sha256") != sha256(compact_bytes(probes_by_runtime[runtime]["results"])): evidence_bad = True
            if row.get("cleanup_state") != "VERIFIED_EXTERNAL_TEMP_REMOVED" or row.get("authority_ceiling") != "INTERNAL_SYNTHETIC_IMPLEMENTATION_ONLY": evidence_bad = True
            if projection != {"equal":True,"hash_scope":"HEAD_BRANCH_CLAUDE_TREE_CLAUDE_DIFF_STATUS","before_sha256":isolation.get("repository_projection_before_sha256"),"after_sha256":isolation.get("repository_projection_after_sha256"),"head":EXPECTED_PARENT,"branch":ACTIVE_BRANCH,"baseline_claude_tree":isolation.get("baseline_claude_tree"),"head_claude_tree":isolation.get("head_claude_tree"),"claude_clean_before_after":True,"full_worktree_projection_compared":True}: evidence_bad = True
        if evidence_bad: errors.append("E_RUNTIME_EVIDENCE_CONTRACT")
        elif sha256(compact_bytes(evidence_rows)) != EXPECTED_RUNTIME_EVIDENCE_SHA256: errors.append("E_RUNTIME_EVIDENCE_CONTRACT")
    authority = {"synthetic_numerical":True,"implementation_regression":True,"picard_iteration":True,"voltage_transfer_identity":True,"material_validation":False,"experimental_validation":False,"external_primary_literature_validation":False,"canonical_adoption":False,"publication_readiness":False}
    if p.get("authority") != authority: errors.append("E_RUNTIME_AUTHORITY")
    if p.get("source_mutation_count") != 0: errors.append("E_RUNTIME_SOURCE_MUTATION")
    if p.get("semantic_sha256") != sha256(compact_bytes({k:v for k,v in p.items() if k != "semantic_sha256"})): errors.append("E_SEMANTIC_SHA")
    return finalize_type_errors(errors, "E_RUNTIME_TYPES")


def guarded_errors(checker: Callable[[dict[str, Any]], list[str]], payload: dict[str, Any]) -> list[str]:
    try:
        return checker(payload)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError):
        return ["E_CODE_NESTED_SHAPE" if checker is code_errors else "E_RUNTIME_NESTED_SHAPE"]


def validate_sources(code: dict[str, Any]) -> None:
    by_path = {row["path"]: row for row in code["source_contracts"]}
    for path, expected in EXPECTED_SOURCES.items():
        raw = git_bytes(path)
        blob, digest, size, lines, _status, ranges = expected
        require(git_text("rev-parse", f"{BASELINE}:{path}") == blob, "E_GIT_SOURCE_BLOB", path)
        require((sha256(raw),len(raw),len(raw.decode("utf-8","strict").splitlines())) == (digest,size,lines), "E_GIT_SOURCE_IDENTITY", path)
        spans = by_path[path]["source_spans"]
        for row, (start,end) in zip(spans,ranges,strict=True):
            require(row["sha256"] == line_span_hash(raw,start,end), "E_GIT_SOURCE_SPAN", f"{path}:{start}-{end}")


def validate_bound_maps(code: dict[str, Any]) -> None:
    contracted = {row["path"] for row in code["source_contracts"]}
    for mapping in code["equation_code_map"]:
        for bounds in mapping["evidence"].values():
            for bound in bounds:
                path = bound["path"]
                require(path in contracted, "E_MAP_UNCONTRACTED_SOURCE", f"{mapping['id']}:{path}")
                raw = git_bytes(path)
                require(
                    bound["sha256"] == line_span_hash(raw, bound["start"], bound["end"]),
                    "E_MAP_GIT_SPAN",
                    f"{mapping['id']}:{path}:{bound['start']}-{bound['end']}",
                )


def mutation_tests(code: dict[str, Any], runtime: dict[str, Any]) -> int:
    tests: list[tuple[str, dict[str, Any], Callable[[dict[str, Any]],None], Callable[[dict[str, Any]],list[str]], list[str]]] = []
    def add(name: str, base: dict[str, Any], mutate: Callable[[dict[str, Any]],None], checker: Callable[[dict[str, Any]],list[str]], expected: str) -> None:
        tests.append((name,base,mutate,checker,[expected]))
    add("ratio_charge",code,lambda p:p["problem_classes"][0].__setitem__("ratio_reference_applicable",True),code_errors,"E_CLASS_RATIO_APPLICABILITY")
    add("ratio_background",code,lambda p:p["problem_classes"][1].__setitem__("ratio_reference_applicable",True),code_errors,"E_CLASS_RATIO_APPLICABILITY")
    add("fabricate_background",code,lambda p:p["problem_classes"][1].__setitem__("solver_symbol","solve_background"),code_errors,"E_BACKGROUND_SOLVER")
    add("class_symbols",code,lambda p:p["problem_classes"][2]["code_symbols"].pop(),code_errors,"E_CLASS_CONTRACT")
    add("class_equations",code,lambda p:p["problem_classes"][2]["source_equations"].pop(),code_errors,"E_CLASS_CONTRACT")
    add("class_mathematics",code,lambda p:p["problem_classes"][2].__setitem__("mathematical_class","ALGEBRAIC_ROOT"),code_errors,"E_CLASS_CONTRACT")
    add("regular_solution",code,lambda p:p["regular_solution_occupancy"].__setitem__("implicit_omega_nonzero_equilibrium_implemented",True),code_errors,"E_REGULAR_SOLUTION_FALSE_IMPLEMENTED")
    add("double_count",code,lambda p:p["non_double_count"].__setitem__("classification","DOUBLE_COUNT"),code_errors,"E_OMEGA_NON_DOUBLE_COUNT")
    add("timebase_static",code,lambda p:p["equation_code_map"][6].__setitem__("status","CONCORDANT"),code_errors,"E_TIMEBASE_STATIC")
    add("transfer_static",code,lambda p:p["equation_code_map"][5].__setitem__("status","INSTRUMENT_RESPONSE"),code_errors,"E_TRANSFER_STATIC")
    add("map_code",code,lambda p:p["equation_code_map"][4].__setitem__("code_symbol","fabricated_ratio"),code_errors,"E_MAP_CONTRACT")
    add("map_equation",code,lambda p:p["equation_code_map"][4].__setitem__("source_equation","eq:fabricated"),code_errors,"E_MAP_CONTRACT")
    add("map_bound_hash",code,lambda p:p["equation_code_map"][6]["evidence"]["equation_sources"][0].__setitem__("sha256","0"*64),code_errors,"E_MAP_CONTRACT")
    add("source_omit",code,lambda p:p["source_contracts"].pop(),code_errors,"E_SOURCE_SET")
    add("source_blob",code,lambda p:p["source_contracts"][0].__setitem__("git_blob","0"*40),code_errors,"E_SOURCE_IDENTITY")
    add("source_read_coverage",code,lambda p:p["source_contracts"][0].__setitem__("read_coverage",[1,1]),code_errors,"E_SOURCE_READ_COVERAGE")
    add("finding_omit",code,lambda p:p["findings"].pop(),code_errors,"E_FINDING_SET")
    add("finding_owner",code,lambda p:p["findings"][0].__setitem__("owner","Phase 999"),code_errors,"E_FINDING_CONTRACT")
    add("authority",code,lambda p:p["authority"].__setitem__("material_truth",True),code_errors,"E_AUTHORITY")
    add("source_mutation",code,lambda p:p.__setitem__("source_mutation_count",1),code_errors,"E_SOURCE_MUTATION")
    add("inherited_join",code,lambda p:p["inherited_joins"][0].__setitem__("duplicate_new_finding",True),code_errors,"E_INHERITED_JOIN")
    add("class_id",code,lambda p:p["problem_classes"][2].__setitem__("id","BAD"),code_errors,"E_CLASS_SET")
    add("call_edge",code,lambda p:p["call_edges"].pop(),code_errors,"E_CALL_EDGES")
    add("non_double_modulation",code,lambda p:p["non_double_count"].__setitem__("modulation","fabricated"),code_errors,"E_OMEGA_NON_DOUBLE_COUNT_CONTRACT")
    add("regular_status",code,lambda p:p["regular_solution_occupancy"].__setitem__("status","IMPLEMENTED"),code_errors,"E_REGULAR_SOLUTION_CONTRACT")
    add("class_scalar",code,lambda p:p.__setitem__("problem_classes",1),code_errors,"E_CODE_NESTED_SHAPE")
    add("source_scalar",code,lambda p:p.__setitem__("source_contracts",1),code_errors,"E_CODE_NESTED_SHAPE")
    add("timebase_3600",runtime,lambda p:p["independent_probes"][0]["results"]["timebase"].__setitem__("lag_raw_over_corrected",1.0),runtime_errors,"E_TIMEBASE_3600")
    add("nonuniform_claim",runtime,lambda p:p["independent_probes"][0]["results"]["transfer"].__setitem__("nonuniform_grid_rejected",True),runtime_errors,"E_UNIFORM_GRID_FALSE_ENFORCED")
    add("circular_claim",runtime,lambda p:p["independent_probes"][0]["results"]["transfer"].__setitem__("circular_wrap_first_value_abs",0.0),runtime_errors,"E_TRANSFER_CIRCULAR")
    add("initial_claim",runtime,lambda p:p["independent_probes"][0]["results"]["initial_condition"].__setitem__("finite_initial_state_parameter_present",True),runtime_errors,"E_INITIAL_CONDITION")
    add("picard_claim",runtime,lambda p:p["independent_probes"][0]["results"]["picard_identity"].__setitem__("claim_ceiling","EXACT_GENERAL"),runtime_errors,"E_PICARD_CEILING")
    add("option_claim",runtime,lambda p:p["independent_probes"][0]["results"]["option_boundary"].__setitem__("v23_default_equals_explicit_false",False),runtime_errors,"E_OPTION_BOUNDARY")
    add("run_fail",runtime,lambda p:p["official_and_mutation_runs"][4].__setitem__("exit_code",1),runtime_errors,"E_RUN_MATRIX")
    add("run_omit",runtime,lambda p:p["official_and_mutation_runs"].pop(),runtime_errors,"E_RUN_SET")
    add("run_command",runtime,lambda p:p["official_and_mutation_runs"][0]["command"].pop(),runtime_errors,"E_RUN_CONTRACT")
    add("run_cwd",runtime,lambda p:p["official_and_mutation_runs"][0].__setitem__("cwd","fabricated"),runtime_errors,"E_RUN_CONTRACT")
    add("run_stdout_hash",runtime,lambda p:p["official_and_mutation_runs"][0].__setitem__("stdout_sha256","0"*64),runtime_errors,"E_RUN_CONTRACT")
    add("run_authority",runtime,lambda p:p["official_and_mutation_runs"][0].__setitem__("external_truth",True),runtime_errors,"E_RUN_AUTHORITY")
    add("runtime_launcher",runtime,lambda p:p["runtimes"][0]["launcher"].pop(),runtime_errors,"E_RUNTIME_ROW_CONTRACT")
    add("isolation",runtime,lambda p:p["isolation"].__setitem__("disposable_cleanup_verified",False),runtime_errors,"E_ISOLATION")
    add("runtime_authority",runtime,lambda p:p["authority"].__setitem__("experimental_validation",True),runtime_errors,"E_RUNTIME_AUTHORITY")
    add("runtime_blob",runtime,lambda p:p["isolation"]["copy_manifest"][0].__setitem__("sha256","0"*64),runtime_errors,"E_RUNTIME_SOURCE_IDENTITY")
    add("runtime_source_mutation",runtime,lambda p:p.__setitem__("source_mutation_count",1),runtime_errors,"E_RUNTIME_SOURCE_MUTATION")
    add("probe_program",runtime,lambda p:p["independent_probes"][0].__setitem__("probe_sha256","0"*64),runtime_errors,"E_PROBE_PROGRAM")
    add("transfer_manual_identity",runtime,lambda p:p["independent_probes"][0]["results"]["transfer"].__setitem__("manual_fft_max_abs_diff",1.0),runtime_errors,"E_TRANSFER_IDENTITY")
    add("probe_material_truth",runtime,lambda p:p["independent_probes"][0]["results"]["transfer"].__setitem__("material_truth",True),runtime_errors,"E_PROBE_AUTHORITY")
    add("probe_cross_runtime",runtime,lambda p:p["independent_probes"][1]["results"]["option_boundary"].__setitem__("ratio_liveness_max_abs_diff",0.5),runtime_errors,"E_PROBE_CROSS_RUNTIME")
    add("timebase_current_unchanged",runtime,lambda p:p["independent_probes"][0]["results"]["timebase"].__setitem__("si_current_A_unchanged",2.0/3600.0),runtime_errors,"E_TIMEBASE_3600")
    add("runtime_evidence_output",runtime,lambda p:p["runtime_evidence_rows"][0].__setitem__("output_sha256","0"*64),runtime_errors,"E_RUNTIME_EVIDENCE_CONTRACT")
    add("runs_scalar",runtime,lambda p:p.__setitem__("official_and_mutation_runs",1),runtime_errors,"E_RUNTIME_NESTED_SHAPE")
    add("probes_scalar",runtime,lambda p:p.__setitem__("independent_probes",1),runtime_errors,"E_RUNTIME_NESTED_SHAPE")
    add("code_schema_bool",code,lambda p:p.__setitem__("schema",True),code_errors,"E_CODE_TYPES")
    add("code_phase_float",code,lambda p:p.__setitem__("phase",64.0),code_errors,"E_CODE_TYPES")
    add("code_count_bool",code,lambda p:p["counts"].__setitem__("ratio_applicable",True),code_errors,"E_CODE_TYPES")
    add("code_human_float",code,lambda p:p["human_evidence"].__setitem__("problem_classes",3.0),code_errors,"E_CODE_TYPES")
    add("code_authority_int",code,lambda p:p["authority"].__setitem__("material_truth",0),code_errors,"E_CODE_TYPES")
    add("code_source_mutation_bool",code,lambda p:p.__setitem__("source_mutation_count",False),code_errors,"E_CODE_TYPES")
    add("runtime_schema_bool",runtime,lambda p:p.__setitem__("schema",True),runtime_errors,"E_RUNTIME_TYPES")
    add("runtime_phase_float",runtime,lambda p:p.__setitem__("phase",64.0),runtime_errors,"E_RUNTIME_TYPES")
    add("runtime_count_float",runtime,lambda p:p["counts"].__setitem__("runs",10.0),runtime_errors,"E_RUNTIME_TYPES")
    add("runtime_authority_int",runtime,lambda p:p["authority"].__setitem__("experimental_validation",0),runtime_errors,"E_RUNTIME_TYPES")
    add("runtime_source_mutation_bool",runtime,lambda p:p.__setitem__("source_mutation_count",False),runtime_errors,"E_RUNTIME_TYPES")
    for name,base,mutate,checker,expected in tests:
        value = copy.deepcopy(base); mutate(value); rehash(value)
        got = guarded_errors(checker,value)
        require(got == expected, "E_NEGATIVE_DIAGNOSTIC", f"{name}:{got}!={expected}")
    return len(tests)


def strict_json_tests() -> int:
    fixtures = [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":-Infinity}',b'{"a":1e999}',b'{"a":',b'['+b'1'*5000+b']']
    for i,raw in enumerate(fixtures):
        try: strict_load_bytes(raw,f"fixture-{i}")
        except ValidationError: continue
        raise ValidationError(f"E_STRICT_JSON_ESCAPE:{i}")
    return len(fixtures)


def fixture_git(args: list[str], *, cwd: pathlib.Path | None = None, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
    if check and cp.returncode:
        raise ValidationError(f"E_GIT_FIXTURE_COMMAND:{args!r}:{cp.stderr.decode('utf-8','replace')}")
    return cp


def fixture_text(repo: pathlib.Path, *args: str) -> str:
    return fixture_git(["-C", str(repo), *args]).stdout.decode("utf-8", "strict").strip()


def fixture_control_errors(repo: pathlib.Path, bare: pathlib.Path, *, base: str, active: str,
                           active_branch: str = "active", allowed: set[str] | None = None) -> list[str]:
    allowed = {"allowed.txt"} if allowed is None else allowed
    if fixture_text(repo,"rev-parse","--abbrev-ref","HEAD") != active_branch: return ["E_FIX_BRANCH"]
    if fixture_text(repo,"rev-parse","HEAD") != active: return ["E_FIX_HEAD"]
    upstream = fixture_git(["-C",str(repo),"rev-parse","@{u}"],check=False)
    if upstream.returncode or upstream.stdout.decode("utf-8","strict").strip() != active: return ["E_FIX_UPSTREAM"]
    if fixture_text(repo,"rev-parse","--symbolic-full-name","@{u}") != "refs/remotes/origin/active": return ["E_FIX_UPSTREAM_SYMBOLIC"]
    if fixture_text(repo,"rev-parse","origin/active") != active: return ["E_FIX_TRACKING"]
    if fixture_text(bare,"rev-parse","refs/heads/active") != active: return ["E_FIX_LIVE"]
    if any(fixture_text(repo,"rev-parse",ref) != base for ref in ("protected","origin/protected")) or fixture_text(bare,"rev-parse","refs/heads/protected") != base: return ["E_FIX_PROTECTED"]
    if fixture_text(repo,"rev-parse","origin/main") != base or fixture_text(bare,"rev-parse","refs/heads/main") != base: return ["E_FIX_MAIN"]
    if fixture_text(repo,"rev-parse",f"{base}:Claude") != fixture_text(repo,"rev-parse","HEAD:Claude") or fixture_text(repo,"diff","--","Claude") or fixture_text(repo,"status","--porcelain=v1","--","Claude"): return ["E_FIX_CLAUDE"]
    staged = set(filter(None,fixture_text(repo,"diff","--cached","--name-only").splitlines()))
    if staged != allowed: return ["E_FIX_PATH"]
    if fixture_text(repo,"diff","--name-only"): return ["E_FIX_UNSTAGED"]
    if fixture_text(repo,"ls-files","--others","--exclude-standard"): return ["E_FIX_UNTRACKED"]
    if fixture_git(["-C",str(repo),"diff","--check","--cached"],check=False).returncode: return ["E_FIX_DIFF_CHECK"]
    return []


def disposable_git_fixture_tests() -> int:
    cases = [
        ("branch","E_FIX_BRANCH"),("upstream","E_FIX_UPSTREAM"),("upstream_symbolic","E_FIX_UPSTREAM_SYMBOLIC"),("head","E_FIX_HEAD"),
        ("protected","E_FIX_PROTECTED"),("main","E_FIX_MAIN"),("claude","E_FIX_CLAUDE"),
        ("path","E_FIX_PATH"),("diff_check","E_FIX_DIFF_CHECK"),("live","E_FIX_LIVE"),
    ]
    with tempfile.TemporaryDirectory(prefix="p064_s67_git_fixture_") as td:
        root = pathlib.Path(td).resolve()
        require(ROOT.resolve() not in root.parents and root != ROOT.resolve(), "E_GIT_FIXTURE_TEMP")
        bare, seed = root/"remote.git", root/"seed"
        fixture_git(["init","--bare",str(bare)],cwd=root)
        fixture_git(["init","-b","main",str(seed)],cwd=root)
        fixture_git(["-C",str(seed),"config","user.email","p064@example.invalid"])
        fixture_git(["-C",str(seed),"config","user.name","P064 Fixture"])
        (seed/"Claude").mkdir(); (seed/"Claude/frozen.txt").write_text("frozen\n",encoding="utf-8",newline="\n")
        (seed/"seed.txt").write_text("base\n",encoding="utf-8",newline="\n")
        fixture_git(["-C",str(seed),"add","Claude/frozen.txt","seed.txt"]); fixture_git(["-C",str(seed),"commit","-m","base"])
        base = fixture_text(seed,"rev-parse","HEAD")
        fixture_git(["-C",str(seed),"branch","protected",base]); fixture_git(["-C",str(seed),"switch","-c","active"])
        (seed/"active.txt").write_text("active\n",encoding="utf-8",newline="\n")
        fixture_git(["-C",str(seed),"add","active.txt"]); fixture_git(["-C",str(seed),"commit","-m","active"])
        active = fixture_text(seed,"rev-parse","HEAD")
        fixture_git(["-C",str(seed),"branch","alias",active])
        fixture_git(["-C",str(seed),"switch","-c","divergent"])
        (seed/"divergent.txt").write_text("divergent\n",encoding="utf-8",newline="\n")
        fixture_git(["-C",str(seed),"add","divergent.txt"]); fixture_git(["-C",str(seed),"commit","-m","divergent"])
        divergent = fixture_text(seed,"rev-parse","HEAD")
        fixture_git(["-C",str(seed),"remote","add","origin",str(bare)])
        fixture_git(["-C",str(seed),"push","origin","main","protected","active","alias","divergent"])
        fixture_git(["--git-dir",str(bare),"symbolic-ref","HEAD","refs/heads/main"])
        for index,(name,expected) in enumerate(cases):
            repo = root/f"case_{index}_{name}"
            fixture_git(["clone",str(bare),str(repo)],cwd=root)
            fixture_git(["-C",str(repo),"switch","--track","-c","active","origin/active"])
            fixture_git(["-C",str(repo),"branch","protected","origin/protected"])
            (repo/"allowed.txt").write_text("allowed\n",encoding="utf-8",newline="\n")
            fixture_git(["-C",str(repo),"add","allowed.txt"])
            require(fixture_control_errors(repo,bare,base=base,active=active)==[],"E_GIT_FIXTURE_BASELINE",name)
            if name == "branch": fixture_git(["-C",str(repo),"switch","main"])
            elif name == "upstream": fixture_git(["-C",str(repo),"branch","--set-upstream-to=origin/main","active"])
            elif name == "upstream_symbolic": fixture_git(["-C",str(repo),"branch","--set-upstream-to=origin/alias","active"])
            elif name == "head": fixture_git(["-C",str(repo),"update-ref","refs/heads/active",divergent])
            elif name == "protected": fixture_git(["-C",str(repo),"update-ref","refs/heads/protected",divergent])
            elif name == "main": fixture_git(["-C",str(repo),"update-ref","refs/remotes/origin/main",divergent])
            elif name == "claude": (repo/"Claude/frozen.txt").write_text("mutated\n",encoding="utf-8",newline="\n")
            elif name == "path":
                (repo/"extra.txt").write_text("extra\n",encoding="utf-8",newline="\n"); fixture_git(["-C",str(repo),"add","extra.txt"])
            elif name == "diff_check":
                (repo/"allowed.txt").write_text("trailing-space \n",encoding="utf-8",newline="\n"); fixture_git(["-C",str(repo),"add","allowed.txt"])
            elif name == "live": fixture_git(["--git-dir",str(bare),"update-ref","refs/heads/active",divergent])
            got = fixture_control_errors(repo,bare,base=base,active=active)
            require(got == [expected],"E_GIT_FIXTURE_DIAGNOSTIC",f"{name}:{got}!=[{expected}]")
    return len(cases)


def validator_self_tests() -> int:
    raw = pathlib.Path(__file__).read_bytes()
    require(validator_identity_errors(raw)==[],"E_VALIDATOR_SELF_BASELINE")
    fixtures = [
        (raw+b"\n# harmless source mutation\n",["E_VALIDATOR_SOURCE_SHA"]),
        (raw.replace(b'PERSISTENCE = "PASS_P064_STEP67_PERSISTENCE"',b'PERSISTENCE = "PASS_P064_STEP67_TAMPERED"',1),["E_VALIDATOR_AST_SHA","E_VALIDATOR_SOURCE_SHA"]),
        (raw.replace(b"\n",b"\r\n"),["E_VALIDATOR_CRLF","E_VALIDATOR_SOURCE_POLICY"]),
    ]
    for mutated,expected in fixtures:
        got = validator_identity_errors(mutated)
        require(got==expected,"E_VALIDATOR_SELF_DIAGNOSTIC",f"{got}!={expected}")
    return len(fixtures)


def builder_determinism(code_raw: bytes, runtime_raw: bytes) -> int:
    outputs: list[tuple[bytes,bytes]] = []
    with tempfile.TemporaryDirectory(prefix="p064_s67_determinism_") as td:
        base = pathlib.Path(td)
        require(ROOT.resolve() not in base.resolve().parents and base.resolve() != ROOT.resolve(), "E_DETERMINISM_TEMP")
        for i in range(2):
            out = base / str(i); out.mkdir()
            cp = subprocess.run(["py","-3.12","-B","-X","utf8",str(BUILDER),"--out-dir",str(out)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300,check=False)
            require(cp.returncode == 0, "E_BUILDER_RUN", cp.stderr.decode("utf-8","replace"))
            outputs.append(((out/CODE_PATH.name).read_bytes(),(out/RUNTIME_PATH.name).read_bytes()))
    if outputs[0] != outputs[1]:
        details: list[str] = []
        for label, left, right in (("code",outputs[0][0],outputs[1][0]),("runtime",outputs[0][1],outputs[1][1])):
            if left == right: continue
            a,b = json.loads(left),json.loads(right)
            stack: list[tuple[str,Any,Any]] = [("",a,b)]
            while stack and len(details) < 8:
                path,x,y = stack.pop()
                if type(x) is not type(y): details.append(f"{label}{path}:type"); continue
                if isinstance(x,dict):
                    for key in sorted(set(x)|set(y),reverse=True): stack.append((f"{path}/{key}",x.get(key,"<MISSING>"),y.get(key,"<MISSING>")))
                elif isinstance(x,list):
                    if len(x)!=len(y): details.append(f"{label}{path}:len {len(x)}!={len(y)}")
                    for i,(u,v) in reversed(list(enumerate(zip(x,y)))): stack.append((f"{path}/{i}",u,v))
                elif x != y: details.append(f"{label}{path}:{x!r}!={y!r}")
        raise ValidationError(f"E_BUILDER_CROSS_RUN:{details!r}")
    require(outputs[0] == (code_raw,runtime_raw), "E_BUILDER_STORED_IDENTITY")
    return 2


def validate_docs() -> None:
    validator_raw = pathlib.Path(__file__).read_bytes()
    require(validator_identity_errors(validator_raw)==[],"E_VALIDATOR_IDENTITY",repr(validator_identity_errors(validator_raw)))
    for path,digest in EXPECTED_DOC_SHA256.items():
        raw = (ROOT/path).read_bytes()
        require(b"\r\n" not in raw, "E_DOC_CRLF", path)
        require(sha256(raw) == digest, "E_DOC_SHA", path)
    builder_blob = git_text("hash-object","--path=Codex/work/v1023_phase064/build_phase064_step67_problem_runtime_boundary.py",str(BUILDER))
    require(builder_blob == EXPECTED_BUILDER_GIT_BLOB, "E_BUILDER_BLOB", builder_blob)


def validate_refs_all_modes() -> None:
    require(git_text("rev-parse","--abbrev-ref","HEAD") == ACTIVE_BRANCH, "E_BRANCH")
    head = git_text("rev-parse","HEAD")
    require(git_text("rev-parse","@{u}") == head, "E_ACTIVE_UPSTREAM")
    require(git_text("rev-parse","--symbolic-full-name","@{u}") == f"refs/remotes/origin/{ACTIVE_BRANCH}", "E_ACTIVE_UPSTREAM_SYMBOLIC")
    require(git_text("rev-parse",f"origin/{ACTIVE_BRANCH}") == head, "E_ACTIVE_TRACKING")
    require(live_tip(ACTIVE_BRANCH) == head, "E_ACTIVE_LIVE")
    require(git_text("rev-parse",PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_LOCAL")
    require(git_text("rev-parse",f"origin/{PROTECTED_BRANCH}") == PROTECTED_TIP, "E_PROTECTED_TRACKING")
    require(live_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_LIVE")
    require(git_text("rev-parse","origin/main") == MAIN_TIP, "E_MAIN_TRACKING")
    require(live_tip("main") == MAIN_TIP, "E_MAIN_LIVE")
    require(git_text("rev-parse",f"{BASELINE}:Claude") == git_text("rev-parse","HEAD:Claude"), "E_CLAUDE_TREE")


def validate_git_mode(mode: str) -> None:
    validate_refs_all_modes()
    if mode == "artifact": return
    if mode == "precommit":
        require(git_text("rev-parse","HEAD") == EXPECTED_PARENT, "E_PRECOMMIT_PARENT")
        staged = set(filter(None,git_text("diff","--cached","--name-only").splitlines()))
        require(staged == EXACT_SET, "E_STAGED_SET", repr(sorted(staged)))
        require(not git_text("diff","--name-only"), "E_UNSTAGED_TRACKED")
        untracked = set(filter(None,git_text("ls-files","--others","--exclude-standard").splitlines()))
        require(not untracked, "E_UNTRACKED", repr(sorted(untracked)))
        for path in EXACT_PATHS:
            require(git(["show",f":{path}"]).stdout == (ROOT/path).read_bytes(), "E_INDEX_WORKTREE_BYTES", path)
        require(git(["diff","--cached","--check"],check=False).returncode == 0, "E_STAGED_DIFF_CHECK")
        return
    require(mode == "persistence", "E_MODE")
    head = git_text("rev-parse","HEAD")
    require(git_text("rev-parse","HEAD^") == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(git_text("show","-s","--format=%s","HEAD") == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT")
    changed = set(filter(None,git_text("diff-tree","--no-commit-id","--name-only","-r","HEAD").splitlines()))
    require(changed == EXACT_SET, "E_COMMIT_PATHS")
    require(git_text("rev-parse","@{u}") == head, "E_UPSTREAM")
    require(git_text("rev-parse",f"origin/{ACTIVE_BRANCH}") == head, "E_TRACKING")
    require(live_tip(ACTIVE_BRANCH) == head, "E_LIVE_ACTIVE")
    require(git(["show","--check","--format=","HEAD"],check=False).returncode == 0, "E_COMMIT_DIFF_CHECK")
    require(not git_text("status","--porcelain=v1","-uall"), "E_DIRTY_PERSISTENCE")
    for path in EXACT_PATHS:
        require(git(["show",f"HEAD:{path}"]).stdout == (ROOT/path).read_bytes(), "E_COMMIT_WORKTREE_BYTES", path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",choices=("artifact","precommit","persistence"),default="artifact")
    args = parser.parse_args()
    code,n_code,code_raw = strict_load(CODE_PATH)
    runtime,n_runtime,runtime_raw = strict_load(RUNTIME_PATH)
    code_diagnostics = guarded_errors(code_errors,code)
    runtime_diagnostics = guarded_errors(runtime_errors,runtime)
    require(code_diagnostics == [], "E_CODE_CONTENT", repr(code_diagnostics))
    require(runtime_diagnostics == [], "E_RUNTIME_CONTENT", repr(runtime_diagnostics))
    validate_sources(code)
    validate_bound_maps(code)
    negative = mutation_tests(code,runtime)
    strict = strict_json_tests()
    git_fixtures = disposable_git_fixture_tests()
    self_fixtures = validator_self_tests()
    deterministic = 0 if args.mode == "persistence" else builder_determinism(code_raw,runtime_raw)
    validate_docs()
    validate_git_mode(args.mode)
    print(f"PASS_P064_STEP67_NEGATIVE {negative}/{negative} strict_json={strict}/{strict}")
    print(f"PASS_P064_STEP67_GIT_FIXTURES {git_fixtures}/{git_fixtures}")
    print(f"PASS_P064_STEP67_VALIDATOR_SELF {self_fixtures}/{self_fixtures}")
    print(f"PASS_P064_STEP67_TRAVERSAL code={n_code} runtime={n_runtime} sources={len(EXPECTED_SOURCES)}/{len(EXPECTED_SOURCES)} runs=10/10")
    if args.mode != "persistence": print(f"PASS_P064_STEP67_DETERMINISM {deterministic}/{deterministic}")
    print(PERSISTENCE if args.mode == "persistence" else GATE)


if __name__ == "__main__":
    main()
