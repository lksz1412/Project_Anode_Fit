#!/usr/bin/env python3
"""Validate Phase 064 Step 66 evidence, exact Git boundary, and persistence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[3]
BUILDER_PATH = REPO / "Codex/work/v1023_phase064/build_phase064_step66_ratio_transfer_rederivation.py"
ARTIFACT_PATH = REPO / "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json"
RESULT_PATH = REPO / "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_PARENT = "5fb19384e3df7a73c96fcf26e8f599b42c331ae7"
EXPECTED_SUBJECT = "audit(phase064): rederive v1023 ratio transfer closure"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P064_STEP66_REDERIVATION"
PERSISTENCE = "PASS_P064_STEP66_PERSISTENCE"

EXACT_PATHS = [
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md",
    "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json",
    "Codex/work/v1023_phase064/build_phase064_step66_ratio_transfer_rederivation.py",
    "Codex/work/v1023_phase064/validate_phase064_step66.py",
]
EXACT_SET = set(EXACT_PATHS)

EXPECTED_DOC_SHA256 = {
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": "64917808663fdbbe0fa1c7232333e06073a8dd4dcc430af7bceb60f4b0d604dc",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md": "f3029ddc4a92e4386bd80c61e16539754c93b1f6a6341f9e662df48f5b8dfa77",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md": "88cd691e3e9b4e16b694d7ea1be3be41ffe4b9629a38456ea31cbddf00c0dda4",
    "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md": "1f5f85c51f9aa78eae0f04cb48ee9aac6c6c4cbe85884919148a8b6072378ae6",
}

EXPECTED_BUILDER_GIT_BLOB = "6d3cc941dce8afe49087c65bc93a3604cbaee59e"
EXPECTED_SOURCE_CONTRACTS_SHA256 = "cb1e6e39e670418c9220d52932238b4df0c456f08dedc0da2a6704005714b527"
EXPECTED_CORRECTIONS_SHA256 = "39754f8cb8eafe17375130ffcd0ecb08dca9832cea0302aa98e10719abdf37f2"
EXPECTED_TIMING_SHA256 = "830490acc3ee83e4776ac7fb076ab8516b985529bb2f1f2e85711b3bb1e609db"

EXPECTED_ROOT_KEYS = {
    "authority", "authority_ceiling", "baseline_commit", "contraction",
    "correction_register", "deterministic_benchmark", "expected_parent",
    "expected_subject", "fredholm_rederivation", "gate", "generated_by",
    "ground_not_found", "human_evidence_semantic_sha256",
    "independent_timing_observation", "non_applicable_targets",
    "prior_literature_binding", "schema", "semantic_sha256",
    "source_contracts", "source_mutation_count", "status", "timebase",
    "transfer", "volterra_rederivation",
}
EXPECTED_CORRECTIONS = [
    ("P064-S66-CORR-001", "P0", "Phase 064 Step 67", "CORRECT_DERIVATION_AND_ROUTE_RUNTIME"),
    ("P064-S66-CORR-002", "P1", "Phase 064 Step 66", "SUPERSEDE_SEMANTIC_PROJECTION_KEEP_PDF_CROP"),
    ("P064-S66-CORR-003", "P1", "Phase 064 Step 66", "DEMOTE_TO_REDUCED_FEEDBACK_HYPOTHESIS"),
    ("P064-S66-CORR-004", "P1", "Phase 064 Step 66", "REPLACE_WITH_GLOBAL_SUFFICIENT_BOUND_AND_LOCAL_HEURISTIC"),
    ("P064-S66-CORR-005", "P1", "Phase 064 Step 66", "DEMOTE_TO_INTERNAL_ANALOGY"),
    ("P064-S66-CORR-006", "P1", "Phase 064 Step 66", "BOUND_TO_DIRECTED_VOLTAGE_COORDINATE"),
    ("P064-S66-CORR-007", "P1", "Phase 064 Step 67", "ROUTE_CODE_RUNTIME_BOUNDARY"),
    ("P064-S66-CORR-008", "P1", "Phase 064 Step 66", "RETAIN_DIMENSIONLESS_REJECT_CURRENT_LABEL"),
    ("P064-S66-CORR-009", "P2", "Phase 064 Step 68", "GROUND_NOT_FOUND_ROUTE_VALIDATION_AUTHORITY"),
    ("P064-S66-CORR-010", "P2", "Phase 064 Step 67", "REQUIRE_UTF8_INVOCATION"),
    ("P064-S66-CORR-011", "P2", "Phase 064 Step 69.1", "ROUTE_SOURCE_DISPOSITION"),
]
NON_APPLICABLE = [
    "ALGEBRAIC_CHARGE_BALANCE_ROOT",
    "BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY",
    "LITERAL_JCP_KERNEL_VARIABLE_TRANSFER",
    "REF7_INFERRED_METHOD_CONTENT",
]

EXPECTED_SOURCE_IDENTITIES = {
    "Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md": ("ce4b17399f8d7318b4053134959ab77f9038d313", "4c3aedabac00ac657f12bf2dffe6f696017654b883f2798c2d824ee70665b228", 20203, 225, [1, 225], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": ("b0e246c7bd31c63134137066d31a6032d4d190d7", "26c1546fcc701d8dec6847f1ad60cbf0ea2222808fe2aaa396265a7f8641c51c", 20019, 212, [1, 212], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": ("15cd3c78f37dea9a1b942108d01df3db62101a6f", "a01c5394781f3674fb167846d1acc05a49c7ec2f4c419c7480a128b1c0747723", 10884, 145, [1, 145], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex": ("490139d35601c8d83da6d567bcdcf2ac97619d1c", "7fed61f947f974c21f58361519ae9cc3511ac633c3869503243a70f9cf0eef49", 18372, 245, [1, 245], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/_sections/ch1_sec10_sum.tex": ("10ab70e2e4a99cc72b122c75922bc178041b1923", "5edccc997672641f6722cf9eae80cb93c83345f5cc9cfaa205f500a57c16de6e", 15794, 170, [1, 170], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md": ("3c840b4a67b9c8b134c76c984efe34fba9271915", "289b59fe109318a9d42a6daa29d30e43815a45e3729baed3366688444c767cd2", 21845, 301, [1, 301], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": ("b3b62159919fce6d4c4665b234d74456fa0fcf10", "279b711ef3c33b046136f7b962c76f65ccacbaca369f571ab8f3ed50524f86dc", 2866, 68, [1, 68], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": ("cf330bfc14e0291474ea9490a5b206c2f060a319", "1417277231ea795515037f470ec160e5077e04d8ab351df7e85c6467671fcef4", 6502, 128, [1, 128], "READ_FULL_STEP66"),
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": ("554425dd566c20314357eddfcf4261517df907ee", "0298bb5fdf47ed5faf2f8301b6d84dc88fd580a69c8e616daa3942d35ceae7cf", 97860, 1585, [[105, 210], [450, 535], [630, 710]], "TARGETED_CONTROLLER_PLUS_INDEPENDENT_EXPANSION"),
}

TIMING_ROW_KEYS = (
    "g_eff", "frozen_ms", "ratio_ms", "picard_ms", "picard_iterations",
    "ratio_over_frozen", "picard_over_ratio", "lag_relative_l2_frozen",
    "lag_relative_l2_ratio", "peak_relative_l2_frozen",
    "peak_relative_l2_ratio", "ratio_equals_picard1",
)
EXPECTED_TIMING_ROWS = [
    (0.5, 4.0579, 8.9484, 50.3639, 10, 2.205, 5.628, 0.0118446, 0.000462266, 0.0502759, 0.00263474, True),
    (1.0, 4.0579, 8.7944, 59.6905, 12, 2.167, 6.787, 0.0290647, 0.00292961, 0.124001, 0.0169777, True),
    (2.0, 4.0579, 8.6916, 87.6683, 18, 2.142, 10.087, 0.0918681, 0.0282658, 0.379598, 0.162313, True),
]


class ValidationError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(f"{code}{':' + detail if detail else ''}")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def strict_load_bytes(raw: bytes, source: str) -> tuple[Any, int]:
    duplicate: list[str] = []

    def pairs_hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                duplicate.append(key)
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{source}:{value}")

    try:
        value = json.loads(
            raw, object_pairs_hook=pairs_hook, parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"E_JSON_PARSE:{source}:{exc}") from exc
    require(not duplicate, "E_JSON_DUPLICATE", f"{source}:{duplicate}")

    def reject_overflow(node: Any) -> None:
        if isinstance(node, float) and not math.isfinite(node):
            raise ValidationError(f"E_JSON_NUMERIC_OVERFLOW:{source}")
        if isinstance(node, dict):
            for child in node.values():
                reject_overflow(child)
        elif isinstance(node, list):
            for child in node:
                reject_overflow(child)

    reject_overflow(value)
    return value, traverse(value)


def strict_load(path: Path) -> tuple[dict[str, Any], int, bytes]:
    raw = path.read_bytes()
    value, nodes = strict_load_bytes(raw, path.as_posix())
    require(isinstance(value, dict), "E_JSON_ROOT", path.as_posix())
    return value, nodes, raw


def traverse(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(1 + traverse(child) for child in value.values())
    if isinstance(value, list):
        return 1 + sum(traverse(child) for child in value)
    return 1


def git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        process = subprocess.run(
            ["git", *args], cwd=REPO, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False, timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"E_GIT_TIMEOUT:{' '.join(args)}") from exc
    if check and process.returncode:
        detail = process.stderr.decode("utf-8", "replace").strip()
        raise ValidationError(f"E_GIT_COMMAND:{' '.join(args)}:{process.returncode}:{detail}")
    return process


def git_text(args: list[str]) -> str:
    return git(args).stdout.decode("utf-8", "strict").strip()


def live_tip(branch: str) -> str:
    output = git_text(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"])
    require(bool(output), "E_LIVE_REMOTE_MISSING", branch)
    return output.split()[0]


def load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("p064_step66_builder", BUILDER_PATH)
    require(spec is not None and spec.loader is not None, "E_BUILDER_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rehash(payload: dict[str, Any]) -> None:
    payload.pop("semantic_sha256", None)
    payload["semantic_sha256"] = sha256(compact_bytes(payload))


def payload_errors(payload: dict[str, Any]) -> list[str]:
    if not isinstance(payload, dict):
        return ["E_ROOT_TYPE"]
    errors: list[str] = []

    def add(condition: bool, code: str) -> None:
        if condition:
            errors.append(code)

    def mapping(value: Any, code: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            errors.append(code)
            return {}
        return value

    def sequence(value: Any, code: str) -> list[Any]:
        if not isinstance(value, list):
            errors.append(code)
            return []
        return value

    def is_number(value: Any) -> bool:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and (not isinstance(value, float) or math.isfinite(value))
        )

    dictionary_contracts = [
        ("prior_literature_binding", "E_PRIOR_BINDING_TYPE"),
        ("fredholm_rederivation", "E_FREDHOLM_TYPE"),
        ("volterra_rederivation", "E_VOLTERRA_TYPE"),
        ("contraction", "E_CONTRACTION_TYPE"),
        ("transfer", "E_TRANSFER_TYPE"),
        ("timebase", "E_TIMEBASE_TYPE"),
        ("deterministic_benchmark", "E_BENCHMARK_TYPE"),
        ("independent_timing_observation", "E_TIMING_TYPE"),
        ("authority", "E_AUTHORITY_TYPE"),
    ]
    for key, code in dictionary_contracts:
        if not isinstance(payload.get(key), dict):
            return [code]
    for key, code in (
        ("source_contracts", "E_SOURCE_TYPE"),
        ("correction_register", "E_CORRECTIONS_TYPE"),
        ("non_applicable_targets", "E_NON_APPLICABLE_TYPE"),
        ("ground_not_found", "E_GROUND_NOT_FOUND_TYPE"),
    ):
        if not isinstance(payload.get(key), list):
            return [code]
    if not isinstance(payload["transfer"].get("units"), dict):
        return ["E_TRANSFER_UNITS_TYPE"]
    if not isinstance(payload["transfer"].get("external_authority"), dict):
        return ["E_TRANSFER_AUTHORITY_TYPE"]
    if not isinstance(payload["deterministic_benchmark"].get("grid"), dict):
        return ["E_BENCHMARK_GRID_TYPE"]
    if not isinstance(payload["deterministic_benchmark"].get("rows"), list):
        return ["E_BENCHMARK_ROWS_TYPE"]
    if any(not isinstance(row, dict) for row in payload["deterministic_benchmark"]["rows"]):
        return ["E_BENCHMARK_ROW_TYPE"]
    if any(not isinstance(row.get("workload_passes"), dict) for row in payload["deterministic_benchmark"]["rows"]):
        return ["E_WORKLOAD_TYPE"]
    benchmark_numeric_keys = (
        "g_eff", "epsilon_local", "q_sufficient_global_bound", "final_sup_delta",
        "frozen_relative_l2_vs_fixed_point", "ratio_relative_l2_vs_fixed_point",
        "frozen_max_abs_vs_fixed_point", "ratio_max_abs_vs_fixed_point",
    )
    for row in payload["deterministic_benchmark"]["rows"]:
        if any(not is_number(row.get(key)) for key in benchmark_numeric_keys):
            return ["E_BENCHMARK_NUMERIC_TYPE"]
        if not isinstance(row.get("picard_iterations_to_1e-13"), int) or isinstance(row.get("picard_iterations_to_1e-13"), bool):
            return ["E_BENCHMARK_ITERATION_TYPE"]
        if not isinstance(row.get("ratio_equals_picard1"), bool):
            return ["E_BENCHMARK_BOOLEAN_TYPE"]
        if any(not isinstance(row["workload_passes"].get(key), int) or isinstance(row["workload_passes"].get(key), bool) for key in ("frozen", "ratio", "converged_picard")):
            return ["E_WORKLOAD_VALUE_TYPE"]
    timing_preflight = payload["independent_timing_observation"]
    for key, code in (
        ("comparator_conclusion", "E_TIMING_COMPARATOR_TYPE"),
        ("environment", "E_TIMING_ENVIRONMENT_TYPE"),
        ("input", "E_TIMING_INPUT_TYPE"),
    ):
        if not isinstance(timing_preflight.get(key), dict):
            return [code]
    if not isinstance(timing_preflight.get("rows"), list):
        return ["E_TIMING_ROWS_TYPE"]
    if any(not isinstance(row, dict) for row in timing_preflight["rows"]):
        return ["E_TIMING_ROW_TYPE"]
    for row in timing_preflight["rows"]:
        timing_numeric = [row.get(key) for key in TIMING_ROW_KEYS if key not in ("picard_iterations", "ratio_equals_picard1")]
        if any(not is_number(value) for value in timing_numeric):
            return ["E_TIMING_NUMERIC_TYPE"]
        if not isinstance(row.get("picard_iterations"), int) or isinstance(row.get("picard_iterations"), bool):
            return ["E_TIMING_ITERATION_TYPE"]
        if not isinstance(row.get("ratio_equals_picard1"), bool):
            return ["E_TIMING_BOOLEAN_TYPE"]
    if any(not isinstance(row, dict) for row in payload["source_contracts"]):
        return ["E_SOURCE_ROW_TYPE"]
    if any(not isinstance(row.get("bytes"), int) or isinstance(row.get("bytes"), bool) or not isinstance(row.get("physical_lines"), int) or isinstance(row.get("physical_lines"), bool) for row in payload["source_contracts"]):
        return ["E_SOURCE_EXTENT_TYPE"]
    if any(not isinstance(row, dict) for row in payload["correction_register"]):
        return ["E_CORRECTIONS_ROW_TYPE"]

    add(set(payload) != EXPECTED_ROOT_KEYS, "E_ROOT_KEYS")
    add(payload.get("schema") != "phase064.step66.ratio_transfer_rederivation.v1", "E_SCHEMA")
    add(payload.get("generated_by") != "build_phase064_step66_ratio_transfer_rederivation.py", "E_GENERATOR")
    add(payload.get("baseline_commit") != "3b5fd059ed09cdcdde38668c399cb35b8afbcca9", "E_BASELINE")
    add(payload.get("human_evidence_semantic_sha256") != "3468a3706862525b625949fedae0e86b696d8f288799addab2b8dadcb197abbc", "E_HUMAN_EVIDENCE_HASH")
    add(payload.get("expected_parent") != EXPECTED_PARENT, "E_EXPECTED_PARENT")
    add(payload.get("expected_subject") != EXPECTED_SUBJECT, "E_EXPECTED_SUBJECT")
    add(payload.get("gate") != GATE, "E_GATE")
    add(payload.get("status") != "PASS_PENDING_PERSISTENCE_WITH_CORRECTIONS", "E_STATUS")
    add(payload.get("authority_ceiling") != "CONDITIONAL_P064_REF7_GNF_AND_FROZEN_DEFECTS_OPEN", "E_CEILING")
    add(payload.get("source_mutation_count") != 0, "E_SOURCE_MUTATION")
    source_rows = sequence(payload.get("source_contracts"), "E_SOURCE_TYPE")
    add(len(source_rows) != 9, "E_SOURCE_COUNT")
    actual_sources: dict[str, tuple[Any, ...]] = {}
    for raw_row in source_rows:
        row = mapping(raw_row, "E_SOURCE_ROW_TYPE")
        path = row.get("path")
        if not isinstance(path, str):
            errors.append("E_SOURCE_PATH")
            continue
        actual_sources[path] = (
            row.get("git_blob"), row.get("raw_sha256"), row.get("bytes"),
            row.get("physical_lines"), row.get("read_interval"), row.get("read_kind"),
        )
    add(actual_sources != EXPECTED_SOURCE_IDENTITIES, "E_SOURCE_IDENTITY")
    add(sha256(compact_bytes(source_rows)) != EXPECTED_SOURCE_CONTRACTS_SHA256, "E_SOURCE_IDENTITY")

    semantic = payload.get("semantic_sha256")
    unsigned = copy.deepcopy(payload)
    unsigned.pop("semantic_sha256", None)
    add(semantic != sha256(compact_bytes(unsigned)), "E_SEMANTIC_HASH")

    binding = mapping(payload.get("prior_literature_binding"), "E_PRIOR_BINDING_TYPE")
    add(binding.get("matrix_raw_sha256") != "db67fc40d9fba6d03547325061b16d03da87ddf59e0985fd6d7b471d092d453a", "E_PRIOR_MATRIX_HASH")
    add(binding.get("attestation_raw_sha256") != "273fa6eb35000b013b48eeb63154b098bd8d0ab3dc89a8634d478d75c4106fc4", "E_PRIOR_ATTESTATION_HASH")
    add(binding.get("step65_eq38_stale_projection") != "EQ38|definition=Lambda_rx|integral=4*pi*exp(U1(sigma))*integral_0_infinity[r^2*exp(-U1(r))*angular_average(exp(K*r*mu)*S_R(r,mu))dr]", "E_EQ38_STALE_BINDING")
    add(binding.get("step66_corrected_projection") != "EQ38|definition=Lambda_rx|integral=4*pi*exp(U1(sigma))*integral_0_infinity[r^2*exp(-U1(r))*angular_average(exp(K*sigma*mu)*S_R(r,mu))dr]", "E_EQ38_CORRECTION")
    add(binding.get("eq38_pdf_crop_raw_pixel_sha256") != "63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978", "E_EQ38_CROP")
    add(binding.get("correction_scope") != "SEMANTIC_PROJECTION_SUPERSEDED_PDF_CROP_PRESERVED", "E_EQ38_CORRECTION_SCOPE")

    fredholm = mapping(payload.get("fredholm_rederivation"), "E_FREDHOLM_TYPE")
    add(fredholm.get("problem_class") != "FREDHOLM_SECOND_KIND_FIXED_SEMI_INFINITE_DOMAIN", "E_FREDHOLM_CLASS")
    add(fredholm.get("boundary_conditions") != ["Wbar_u(r)->1 as r->infinity", "radial_derivative_at_sigma=0"], "E_FREDHOLM_BOUNDARY")
    add(fredholm.get("upstream_status") != "EQS19_20_ORIENTATION_AVERAGING_APPROXIMATIONS", "E_UPSTREAM_APPROXIMATION")
    add(fredholm.get("eq32_domains") != [["sigma", "r"], ["r", "infinity"]], "E_EQ32_DOMAINS")
    add(fredholm.get("eq33") != "EXACT_REARRANGEMENT_WITHIN_APPROXIMATED_SYSTEM_REQUIRES_W_NONZERO", "E_EQ33_DENOMINATOR")
    add(fredholm.get("eq34") != "REFERENCE_RATIO_APPROXIMATION", "E_EQ34_APPROXIMATION")
    add(fredholm.get("eq38_angular_factor") != "exp(K*sigma*mu)", "E_EQ38_CORRECTION")
    add(fredholm.get("eq39") != "APPROXIMATE_CLOSED_RESULT", "E_EQ39_APPROXIMATION")
    add(fredholm.get("transferable_principle") != "REFERENCE_SUBSTITUTION_DESIGN_MOTIVATION_ONLY", "E_TRANSFERABLE_PRINCIPLE")
    add(fredholm.get("literal_graphite_identity") is not False, "E_CLASS_BOUNDARY")

    volterra = mapping(payload.get("volterra_rederivation"), "E_VOLTERRA_TYPE")
    add(volterra.get("coordinate") != "DIRECTED_VOLTAGE_X_INCREASES_ALONG_PROTOCOL", "E_VOLTERRA_COORDINATE")
    add(volterra.get("problem_class") != "NONLINEAR_CAUSAL_VOLTERRA_SECOND_KIND", "E_PROBLEM_CLASS")
    add(volterra.get("initial_condition_contract") != "FINITE_X0_TERM_OR_PROVED_REMOTE_PAST_DECAY", "E_INITIAL_BOUNDARY")
    add(volterra.get("selected_law_authority") != "REDUCED_FEEDBACK_HYPOTHESIS", "E_REDUCED_AUTHORITY")
    add(volterra.get("selected_law") != "kappa(xi)=kappa0*exp[-g*(1-xi)]", "E_SELECTED_LAW")
    add(volterra.get("frozen_reference") != "r0_prime=sigma_x-kappa0*r0", "E_FROZEN_ODE_SIGN")
    add(volterra.get("first_picard") != "r1=T[r0]; r1_prime=sigma_x-kappa(xi0)*r1", "E_PICARD_ODE_SIGN")
    add(volterra.get("local_equivalent") != "FIRST_ORDER_NONLINEAR_ODE", "E_LOCAL_EQUIVALENT")
    add(volterra.get("frozen_limit") != "g=0 => r=r1=r0 for identical initial condition", "E_FROZEN_LIMIT")
    add(volterra.get("jcp_solution_ratio_identity") is not False, "E_JCP_IDENTITY")

    contraction = mapping(payload.get("contraction"), "E_CONTRACTION_TYPE")
    add(contraction.get("sufficient_bound") != "q=norm_sigma_infinity*K_kappa/kappa_min^2", "E_CONTRACTION_BOUND")
    add(contraction.get("sufficient_condition") != "q<1", "E_CONTRACTION_CONDITION")
    add(contraction.get("assumptions") != ["kappa>=kappa_min>0", "abs(partial_kappa/partial_xi)<=K_kappa", "sigma_bounded"], "E_CONTRACTION_ASSUMPTIONS")
    add(contraction.get("scope") != "REMOTE_PAST_OR_ZERO_INITIAL_TERM", "E_CONTRACTION_SCOPE")
    add(contraction.get("dimension") != "DIMENSIONLESS", "E_CONTRACTION_UNITS")
    add(contraction.get("local_authority") != "LEADING_ORDER_HEURISTIC_NOT_GLOBAL_THEOREM", "E_CONTRACTION_AUTHORITY")

    transfer = mapping(payload.get("transfer"), "E_TRANSFER_TYPE")
    add(transfer.get("coordinate") != "DIRECTED_VOLTAGE_X", "E_TRANSFER_COORDINATE")
    add(transfer.get("fourier_convention") != "fhat=integral f(x)*exp(-i*omega_x*x)dx", "E_TRANSFER_CONVENTION")
    add(transfer.get("formula") != "H=1/(1+i*omega_x*L0)", "E_TRANSFER_FORMULA")
    add(transfer.get("units") != {"omega_x": "V^-1", "L0": "V", "H": "1"}, "E_TRANSFER_UNITS")
    add(transfer.get("finite_dft_caveat") != "UNPADDED_DFT_IS_CIRCULAR_NOT_CAUSAL", "E_DFT_BOUNDARY")
    add(transfer.get("time_mapping") != "REQUIRES_EXPLICIT_SWEEP_RATE_NU_AND_TAU=L0/abs(nu)", "E_TIME_MAPPING")
    add(transfer.get("external_authority") != {"time_without_sweep_rate": False, "EIS": False, "instrument_response": False}, "E_TRANSFER_PROMOTION")

    timebase = mapping(payload.get("timebase"), "E_TIMEBASE_TYPE")
    add(timebase.get("Ah_contract") != "dq/dt_s=I_A/(3600*Q_Ah)=C_h/3600", "E_TIMEBASE_AH")
    add(timebase.get("coulomb_contract") != "dq/dt_s=I_A/Q_C", "E_TIMEBASE_COULOMB")
    add(timebase.get("kinetic_length") != "L_q=(dq/dt_s)/k_s; L_V=abs(dV/dq)*L_q", "E_KINETIC_LENGTH")
    add(timebase.get("legacy_overestimate_factor") != 3600, "E_TIMEBASE")
    add(timebase.get("required_separation") != ["current_A_for_IR", "normalized_rate_s^-1_for_kinetics"], "E_CURRENT_RATE_SEPARATION")
    add(timebase.get("physical_current_regime_approved") is not False, "E_CURRENT_REGIME")
    add(timebase.get("dimensionless_L0_over_w_tests_retained") is not True, "E_DIMENSIONLESS_RETENTION")

    benchmark = mapping(payload.get("deterministic_benchmark"), "E_BENCHMARK_TYPE")
    rows = sequence(benchmark.get("rows"), "E_BENCHMARK_ROWS_TYPE")
    add(benchmark.get("authority") != "DETERMINISTIC_INTERNAL_DISCRETIZATION_ONLY", "E_BENCHMARK_AUTHORITY_INTERNAL")
    add(benchmark.get("grid") != {"N": 2401, "domain_V": [-0.15, 0.35], "center_V": 0.1, "w_V": 0.02, "L0_V": 0.006, "scheme": "BACKWARD_EULER"}, "E_BENCHMARK_GRID")
    add(benchmark.get("reference") != "CONVERGED_PICARD_FIXED_POINT_NOT_EXTERNAL_TRUTH", "E_BENCHMARK_REFERENCE")
    add([row.get("g_eff") for row in rows if isinstance(row, dict)] != [0.0, 0.5, 1.0, 2.0], "E_BENCHMARK_CASES")
    for row in rows:
        if not isinstance(row, dict):
            errors.append("E_BENCHMARK_ROW")
            continue
        g = row.get("g_eff")
        add(row.get("ratio_equals_picard1") is not True, "E_BENCHMARK_IDENTITY")
        workload = mapping(row.get("workload_passes"), "E_WORKLOAD_TYPE")
        add(workload.get("ratio") != 2, "E_WORKLOAD_PASSES")
        add(workload.get("frozen") != 1, "E_WORKLOAD_PASSES")
        add(workload.get("converged_picard") != 1 + row.get("picard_iterations_to_1e-13", -1), "E_WORKLOAD_PASSES")
        if isinstance(g, (int, float)):
            expected_epsilon = g * 0.006 / (4.0 * 0.02)
            expected_q = 12.5 * (g / 0.006) / (((1.0 / 0.006) * math.exp(-g)) ** 2)
            add(not math.isclose(row.get("epsilon_local", math.nan), expected_epsilon, rel_tol=0.0, abs_tol=5e-14), "E_LOCAL_INDICATOR")
            add(not math.isclose(row.get("q_sufficient_global_bound", math.nan), expected_q, rel_tol=0.0, abs_tol=5e-13), "E_GLOBAL_BOUND_NUMERIC")
        add(row.get("ratio_relative_l2_vs_fixed_point", math.inf) > row.get("frozen_relative_l2_vs_fixed_point", -math.inf) + 1e-15, "E_BENCHMARK_ACCURACY")
    if rows:
        zero = rows[0]
        add(any(zero.get(key) != 0.0 for key in (
            "frozen_relative_l2_vs_fixed_point", "ratio_relative_l2_vs_fixed_point",
            "frozen_max_abs_vs_fixed_point", "ratio_max_abs_vs_fixed_point",
        )), "E_G0_EXACT_LIMIT")
        add(rows[-1].get("q_sufficient_global_bound", 0.0) <= 1.0, "E_BOUND_NOT_UNIVERSAL")

    timing = mapping(payload.get("independent_timing_observation"), "E_TIMING_TYPE")
    add(timing.get("authority") != "INTERNAL_SYNTHETIC_RUNTIME_OBSERVATION_ONLY", "E_BENCHMARK_AUTHORITY")
    add(timing.get("comparator_conclusion") != {
        "ratio_vs_converged_picard": "POSITIVE_WITH_APPROXIMATION_ERROR",
        "ratio_vs_first_picard": "ZERO_IDENTICAL_OUTPUT",
        "ratio_vs_frozen": "NEGATIVE_SLOWER",
    }, "E_BENCHMARK_COMPARATOR")
    add(timing.get("environment") != {"architecture": "AMD64", "numpy": "2.5.0", "os": "Windows 11 build 26200", "python": "3.14.4"}, "E_TIMING_ENVIRONMENT")
    add(timing.get("input") != {"L0_V": 0.006, "N": 8000, "center_V": 0.1, "convergence_sup_delta": 1e-13, "domain_V": [-0.15, 0.35], "w_V": 0.02}, "E_TIMING_INPUT")
    timing_rows = sequence(timing.get("rows"), "E_TIMING_ROWS_TYPE")
    actual_timing_rows = []
    for raw_row in timing_rows:
        row = mapping(raw_row, "E_TIMING_ROW_TYPE")
        actual_timing_rows.append(tuple(row.get(key) for key in TIMING_ROW_KEYS))
    add(actual_timing_rows != EXPECTED_TIMING_ROWS, "E_TIMING_ROWS")
    add(sha256(compact_bytes(timing)) != EXPECTED_TIMING_SHA256, "E_TIMING_IDENTITY")

    corrections = sequence(payload.get("correction_register"), "E_CORRECTIONS_TYPE")
    actual_corrections = [
        (row.get("id"), row.get("severity"), row.get("owner"), row.get("disposition"))
        for row in corrections if isinstance(row, dict)
    ]
    add(len(actual_corrections) != len(corrections), "E_CORRECTIONS_ROW_TYPE")
    add(actual_corrections != EXPECTED_CORRECTIONS, "E_CORRECTIONS")
    add(sha256(compact_bytes(corrections)) != EXPECTED_CORRECTIONS_SHA256, "E_CORRECTIONS")
    add(payload.get("non_applicable_targets") != NON_APPLICABLE, "E_NON_APPLICABLE")
    add(payload.get("ground_not_found") != [
        "Ref7 original full text and equation chain",
        "scratchpad/cond_audit_verify.py",
        "primary-source proof of JCP-to-graphite variable mapping",
    ], "E_REF7")
    authority = mapping(payload.get("authority"), "E_AUTHORITY_TYPE")
    add(authority.get("ref7_method_content") is not False, "E_REF7")
    add(authority != {
        "internal_mathematical_rederivation": True,
        "internal_synthetic_numerical_behavior": True,
        "external_material_validation": False,
        "external_experimental_validation": False,
        "ref7_method_content": False,
        "canonical_model_selection": False,
        "production_repair": False,
    }, "E_AUTHORITY_PROMOTION")
    return sorted(set(errors))


def strict_json_probes() -> int:
    value, _ = strict_load_bytes(b'{"a":1,"b":[true,null]}', "valid")
    require(value == {"a": 1, "b": [True, None]}, "E_JSON_VALID_PROBE")
    probes = [
        (b'{"a":1,"a":2}', "E_JSON_DUPLICATE"),
        (b'{"a":NaN}', "E_JSON_NONFINITE"),
        (b'{"a":Infinity}', "E_JSON_NONFINITE"),
        (b'{"a":1e999}', "E_JSON_NUMERIC_OVERFLOW"),
        (b'{"a":-1e999}', "E_JSON_NUMERIC_OVERFLOW"),
        (b'{"a":1', "E_JSON_PARSE"),
    ]
    for raw, expected in probes:
        try:
            strict_load_bytes(raw, "probe")
        except ValidationError as exc:
            require(str(exc).startswith(expected), "E_JSON_WRONG_REJECTION", str(exc))
        else:
            raise ValidationError(f"E_JSON_PROBE_ACCEPTED:{expected}")
    return 7


def negative_probes(payload: dict[str, Any]) -> int:
    probes: list[tuple[set[str], Any]] = [
        ({"E_BASELINE"}, lambda p: p.__setitem__("baseline_commit", "0" * 40)),
        ({"E_GENERATOR"}, lambda p: p.__setitem__("generated_by", "wrong.py")),
        ({"E_HUMAN_EVIDENCE_HASH"}, lambda p: p.__setitem__("human_evidence_semantic_sha256", "0" * 64)),
        ({"E_EQ38_CORRECTION"}, lambda p: p["fredholm_rederivation"].__setitem__("eq38_angular_factor", "exp(K*r*mu)")),
        ({"E_CLASS_BOUNDARY"}, lambda p: p["fredholm_rederivation"].__setitem__("literal_graphite_identity", True)),
        ({"E_EQ33_DENOMINATOR"}, lambda p: p["fredholm_rederivation"].__setitem__("eq33", "EXACT_REARRANGEMENT")),
        ({"E_INITIAL_BOUNDARY"}, lambda p: p["volterra_rederivation"].__setitem__("initial_condition_contract", "REMOTE_PAST_ASSUMED")),
        ({"E_REDUCED_AUTHORITY"}, lambda p: p["volterra_rederivation"].__setitem__("selected_law_authority", "TRUE_FULL_KINETICS")),
        ({"E_FROZEN_ODE_SIGN"}, lambda p: p["volterra_rederivation"].__setitem__("frozen_reference", "r0_prime=sigma_x+kappa0*r0")),
        ({"E_PICARD_ODE_SIGN"}, lambda p: p["volterra_rederivation"].__setitem__("first_picard", "r1=T[r0]; r1_prime=sigma_x+kappa(xi0)*r1")),
        ({"E_CONTRACTION_BOUND"}, lambda p: p["contraction"].__setitem__("sufficient_bound", "q=norm_sigma_infinity*K_kappa/kappa_min")),
        ({"E_CONTRACTION_CONDITION"}, lambda p: p["contraction"].__setitem__("sufficient_condition", "q>1")),
        ({"E_CONTRACTION_AUTHORITY"}, lambda p: p["contraction"].__setitem__("local_authority", "GLOBAL_SAFETY_THEOREM")),
        ({"E_TRANSFER_PROMOTION"}, lambda p: p["transfer"]["external_authority"].__setitem__("EIS", True)),
        ({"E_TRANSFER_UNITS"}, lambda p: p["transfer"]["units"].__setitem__("omega_x", "s^-1")),
        ({"E_DFT_BOUNDARY"}, lambda p: p["transfer"].__setitem__("finite_dft_caveat", "CAUSAL_BY_DEFAULT")),
        ({"E_TIME_MAPPING"}, lambda p: p["transfer"].__setitem__("time_mapping", "TAU=L0")),
        ({"E_TIMEBASE"}, lambda p: p["timebase"].__setitem__("legacy_overestimate_factor", 1)),
        ({"E_TIMEBASE_AH"}, lambda p: p["timebase"].__setitem__("Ah_contract", "dq/dt_s=I_A/Q_Ah=C_h")),
        ({"E_CURRENT_REGIME"}, lambda p: p["timebase"].__setitem__("physical_current_regime_approved", True)),
        ({"E_BENCHMARK_IDENTITY"}, lambda p: p["deterministic_benchmark"]["rows"][1].__setitem__("ratio_equals_picard1", False)),
        ({"E_WORKLOAD_PASSES"}, lambda p: p["deterministic_benchmark"]["rows"][1]["workload_passes"].__setitem__("ratio", 1)),
        ({"E_BENCHMARK_NUMERIC_TYPE"}, lambda p: p["deterministic_benchmark"]["rows"][1].__setitem__("epsilon_local", "wrong-type")),
        ({"E_BENCHMARK_NUMERIC_TYPE"}, lambda p: p["deterministic_benchmark"]["rows"][1].__setitem__("ratio_relative_l2_vs_fixed_point", "wrong-type")),
        ({"E_BENCHMARK_ITERATION_TYPE"}, lambda p: p["deterministic_benchmark"]["rows"][1].__setitem__("picard_iterations_to_1e-13", "wrong-type")),
        ({"E_BENCHMARK_NUMERIC_TYPE"}, lambda p: p["deterministic_benchmark"]["rows"][0].__setitem__("epsilon_local", False)),
        ({"E_BENCHMARK_COMPARATOR", "E_TIMING_IDENTITY"}, lambda p: p["independent_timing_observation"]["comparator_conclusion"].__setitem__("ratio_vs_frozen", "POSITIVE")),
        ({"E_TIMING_IDENTITY", "E_TIMING_ROWS"}, lambda p: p["independent_timing_observation"]["rows"][0].__setitem__("frozen_ms", 999999.0)),
        ({"E_SOURCE_IDENTITY"}, lambda p: p["source_contracts"][0].__setitem__("raw_sha256", "0" * 64)),
        ({"E_CORRECTIONS"}, lambda p: p["correction_register"].pop()),
        ({"E_CORRECTIONS"}, lambda p: p["correction_register"][0].__setitem__("disposition", "IGNORE")),
        ({"E_NON_APPLICABLE"}, lambda p: p["non_applicable_targets"].pop()),
        ({"E_REF7", "E_AUTHORITY_PROMOTION"}, lambda p: p["authority"].__setitem__("ref7_method_content", True)),
        ({"E_SOURCE_MUTATION"}, lambda p: p.__setitem__("source_mutation_count", 1)),
        ({"E_AUTHORITY_PROMOTION"}, lambda p: p["authority"].__setitem__("external_material_validation", True)),
        ({"E_VOLTERRA_TYPE"}, lambda p: p.__setitem__("volterra_rederivation", "wrong-type")),
    ]
    for expected, mutate in probes:
        candidate = copy.deepcopy(payload)
        mutate(candidate)
        rehash(candidate)
        errors = set(payload_errors(candidate))
        require(errors == expected, "E_NEGATIVE_PROBE_DIAGNOSTIC_SET", f"expected={sorted(expected)}:actual={sorted(errors)}")
    return len(probes)


def validate_documents() -> None:
    required_tokens = {
        "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md": [
            GATE, EXPECTED_PARENT, EXPECTED_SUBJECT, "exp(K*sigma*mu)",
            "REDUCED_FEEDBACK_HYPOTHESIS", "dq/dt_s = C_h/3600",
            "GROUND_NOT_FOUND", PERSISTENCE,
        ],
        "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md": [
            "Step 66 precommit", "5fb19384e3df7a73c96fcf26e8f599b42c331ae7",
            GATE, PERSISTENCE,
        ],
        "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md": [
            "| Step 66 |", "Step 66 seven declared paths", EXPECTED_SUBJECT,
            GATE, PERSISTENCE,
        ],
        "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": [
            "Current checkpoint: Step 66", "Phase 064 Step 66",
            "Step 66 seven declared paths", EXPECTED_SUBJECT, GATE, PERSISTENCE,
        ],
    }
    for path, tokens in required_tokens.items():
        raw = (REPO / path).read_bytes()
        require(b"\r\n" not in raw, "E_DOCUMENT_NOT_LF", path)
        require(EXPECTED_DOC_SHA256[path] != "TO_BE_FINALIZED", "E_DOCUMENT_HASH_UNFINALIZED", path)
        require(sha256(raw) == EXPECTED_DOC_SHA256[path], "E_DOCUMENT_HASH", path)
        text = raw.decode("utf-8", "strict")
        for token in tokens:
            require(token in text, "E_DOCUMENT_TOKEN", f"{path}:{token}")


def validate_artifacts() -> tuple[dict[str, Any], int]:
    artifact, nodes, raw = strict_load(ARTIFACT_PATH)
    require(raw.endswith(b"\n"), "E_ARTIFACT_FINAL_NEWLINE")
    require(
        git_text(["hash-object", "--path=Codex/work/v1023_phase064/build_phase064_step66_ratio_transfer_rederivation.py", str(BUILDER_PATH)])
        == EXPECTED_BUILDER_GIT_BLOB,
        "E_BUILDER_IDENTITY",
    )
    errors = payload_errors(artifact)
    require(not errors, "E_PAYLOAD", ",".join(errors))
    builder = load_builder()
    rebuilt_a = builder.build_payload()
    rebuilt_b = builder.build_payload()
    require(rebuilt_a == rebuilt_b, "E_BUILDER_NONDETERMINISTIC")
    require(artifact == rebuilt_a, "E_ARTIFACT_RECONSTRUCTION")
    validate_documents()
    return artifact, nodes


def status_paths() -> set[str]:
    output = git(["status", "--porcelain=v1", "--untracked-files=all"]).stdout.decode("utf-8", "strict")
    if not output:
        return set()
    result: set[str] = set()
    for line in output.splitlines():
        require(len(line) >= 4, "E_STATUS_PARSE", line)
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        result.add(path.replace("\\", "/"))
    return result


def validate_common_git() -> None:
    require(git_text(["branch", "--show-current"]) == ACTIVE_BRANCH, "E_ACTIVE_BRANCH")
    head = git_text(["rev-parse", "HEAD"])
    require(git_text(["rev-parse", "@{upstream}"]) == head, "E_ACTIVE_UPSTREAM_TIP")
    require(git_text(["rev-parse", "--symbolic-full-name", "@{upstream}"]) == f"refs/remotes/origin/{ACTIVE_BRANCH}", "E_ACTIVE_UPSTREAM_NAME")
    require(git_text(["rev-parse", f"origin/{ACTIVE_BRANCH}"]) == head, "E_ACTIVE_TRACKING_TIP")
    require(live_tip(ACTIVE_BRANCH) == head, "E_ACTIVE_LIVE_TIP")
    require(git_text(["rev-parse", PROTECTED_BRANCH]) == PROTECTED_TIP, "E_PROTECTED_TIP")
    require(git_text(["rev-parse", f"origin/{PROTECTED_BRANCH}"]) == PROTECTED_TIP, "E_PROTECTED_TRACKING_TIP")
    require(git_text(["rev-parse", "origin/main"]) == MAIN_TIP, "E_MAIN_TRACKING_TIP")
    require(live_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_LIVE_TIP")
    require(live_tip("main") == MAIN_TIP, "E_MAIN_LIVE_TIP")
    require(not git_text(["diff", "--name-only", f"{PROTECTED_TIP}..HEAD", "--", "Claude"]), "E_CLAUDE_TRACKED_DIFF")
    require(not any(path == "Claude" or path.startswith("Claude/") for path in status_paths()), "E_CLAUDE_STATUS")


def validate_artifact_git() -> None:
    require(git_text(["rev-parse", "HEAD"]) == EXPECTED_PARENT, "E_ARTIFACT_HEAD")
    require(status_paths() == EXACT_SET, "E_ARTIFACT_EXACT_SEVEN", str(sorted(status_paths())))


def validate_precommit_git() -> None:
    require(git_text(["rev-parse", "HEAD"]) == EXPECTED_PARENT, "E_PRECOMMIT_HEAD")
    staged = set(filter(None, git_text(["diff", "--cached", "--name-only"]).splitlines()))
    require(staged == EXACT_SET, "E_PRECOMMIT_EXACT_SEVEN", str(sorted(staged)))
    require(not git_text(["diff", "--name-only"]), "E_PRECOMMIT_UNSTAGED_TRACKED")
    untracked = set(filter(None, git_text(["ls-files", "--others", "--exclude-standard"]).splitlines()))
    require(not untracked, "E_PRECOMMIT_UNTRACKED", str(sorted(untracked)))
    require(not git_text(["diff", "--cached", "--check"]), "E_PRECOMMIT_DIFF_CHECK")
    require(status_paths() == EXACT_SET, "E_PRECOMMIT_STATUS")


def commit_paths(commit: str) -> set[str]:
    return set(filter(None, git_text([
        "diff-tree", "--no-commit-id", "--name-only", "-r", commit,
    ]).splitlines()))


def validate_persistence_git(expected_commit: str) -> None:
    head = git_text(["rev-parse", "HEAD"])
    require(head == expected_commit, "E_PERSISTENCE_EXPECTED_COMMIT")
    require(git_text(["rev-parse", "HEAD^"]) == EXPECTED_PARENT, "E_PERSISTENCE_PARENT")
    require(git_text(["show", "-s", "--format=%s", "HEAD"]) == EXPECTED_SUBJECT, "E_PERSISTENCE_SUBJECT")
    require(git_text(["rev-parse", "@{upstream}"]) == head, "E_PERSISTENCE_UPSTREAM")
    require(git_text(["rev-parse", "--symbolic-full-name", "@{upstream}"]) == f"refs/remotes/origin/{ACTIVE_BRANCH}", "E_PERSISTENCE_UPSTREAM_NAME")
    require(git_text(["rev-parse", f"origin/{ACTIVE_BRANCH}"]) == head, "E_PERSISTENCE_TRACKING")
    require(live_tip(ACTIVE_BRANCH) == head, "E_PERSISTENCE_LIVE")
    require(commit_paths(head) == EXACT_SET, "E_PERSISTENCE_EXACT_SEVEN", str(sorted(commit_paths(head))))
    require(not git_text(["status", "--porcelain"]), "E_PERSISTENCE_DIRTY")
    for path in EXACT_PATHS:
        require(
            git_text(["rev-parse", f"HEAD:{path}"])
            == git_text(["hash-object", f"--path={path}", path]),
            "E_PERSISTENCE_BYTES", path,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="precommit")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.mode == "persistence":
        require(bool(args.expected_commit), "E_EXPECTED_COMMIT_REQUIRED")

    artifact, nodes = validate_artifacts()
    strict_count = strict_json_probes()
    negative_count = negative_probes(artifact)
    validate_common_git()
    if args.mode == "artifact":
        validate_artifact_git()
    elif args.mode == "precommit":
        validate_precommit_git()
    else:
        validate_persistence_git(args.expected_commit)

    print(f"PASS_P064_STEP66_NEGATIVE {negative_count}/{negative_count} strict_json={strict_count}/{strict_count}")
    print(f"PASS_P064_STEP66_TRAVERSAL artifact={nodes} sources={len(artifact['source_contracts'])}/9 corrections={len(artifact['correction_register'])}/11")
    print("PASS_P064_STEP66_DETERMINISM 2/2")
    print(PERSISTENCE if args.mode == "persistence" else GATE)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"FAIL_P064_STEP66:{exc}", file=sys.stderr)
        raise SystemExit(1)
