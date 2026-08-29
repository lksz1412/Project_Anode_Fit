#!/usr/bin/env python3
"""Fail-closed validation for Phase 064 Step 69.1 disposition routing."""

from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import json
import math
import pathlib
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any, Callable


REPO = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "84b977a5333870529369d62a6dab8459a6aa551d"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
SUBJECT = "audit(phase064): disposition v1023 lineage"
GATE = "PASS_P064_STEP69_1_DISPOSITIONS"
PERSISTENCE = "PASS_P064_STEP69_1_PERSISTENCE"
SENTINEL = "P064_STEP69_1_RESULT_FIRST_PRECOMMIT"

BUILDER = "Codex/work/v1023_phase064/build_phase064_step69_dispositions.py"
VALIDATOR = "Codex/work/v1023_phase064/validate_phase064_step69_dispositions.py"
DISPOSITION = "Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json"
CARRY = "Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json"
RESULT = "Codex/results/PHASE_064_STEP_069_1_DISPOSITION_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXACT_PATHS = [BUILDER, VALIDATOR, DISPOSITION, CARRY, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER]

TOPOLOGY = "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json"
READ = "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json"
LITERATURE = "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json"
LITERATURE_READ = "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json"
RATIO = "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json"
CODE_DELTA = "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json"
RUNTIME = "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json"
AUTHORITY_MATRIX = "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json"
P63_DISPOSITION = "Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json"
P63_CARRY = "Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json"
INPUT_SHA256 = {
    TOPOLOGY: "ce0fcbda41e866d8f225255ae27ae0e0e1faba9b985c7f72194a14d085be1f99",
    READ: "5fadd789fe05ea83b294a34e0270f637a44c8359f79e63addfed60e8b62ac445",
    LITERATURE: "db67fc40d9fba6d03547325061b16d03da87ddf59e0985fd6d7b471d092d453a",
    LITERATURE_READ: "273fa6eb35000b013b48eeb63154b098bd8d0ab3dc89a8634d478d75c4106fc4",
    RATIO: "bf940a9b3707b9e90d5e82068f722a9bb0aefe632157371db969e572e6e1af7b",
    CODE_DELTA: "b360cf220e519e861080405032dfc2c5be108998901b0c130b8ab325859e5ba3",
    RUNTIME: "f3c87cf1d2f3eea271ac88a76cf516695ac0a8843984651bd591d1d8f31ea1d9",
    AUTHORITY_MATRIX: "e97e5362c8b162614c287bf2826a00bcd4b70600a67d7096e08e628a4dd59d5c",
    P63_DISPOSITION: "cb50d7f94066fe1d8238e7fc1ebe8394271dbda8d0fd03a16aba0104fa752f8b",
    P63_CARRY: "c44c4ee1366ae53969379c0b698e707862cbc290b209edf7ef80d9965a01eb46",
}
BUILDER_RAW_SHA256 = "210589f89982f0f492c72dc9a4fcd8f82de6fbe08d7680bb52efbfc3b993261e"
BUILDER_AST_SHA256 = "26e938c16c3d893404aba62d0aa7950ddc06ccb8cd0e56c0563bc1f6201e21df"

AUTHORITY = {
    "canonical_equation_promoted": False,
    "external_experimental_truth": False,
    "external_material_truth": False,
    "external_scientific_truth": False,
    "primary_literature_jcp147_method_truth": True,
    "primary_literature_ref6_method_truth": True,
    "primary_literature_ref7_method_truth": False,
    "publication_ready": False,
    "phase_ceiling": "CONDITIONAL_P064",
    "scope": "INTERNAL_V1023_LINEAGE_DISPOSITION_ONLY",
}
ALLOWED = {"CORRECT", "PRESERVE", "THEORY_ONLY", "UNVERIFIED"}
ACTIVE = {"CORRECT", "UNVERIFIED"}
CORRECT_NUMBERS = {
    1, 2, 3, 7, 9, 10, 12, 13, 15, 18, 19, 20, 22, 23, 25, 27, 28,
    31, 35, 38, 39, 41, 42, 44, 49, 50, 51, 52, 53, 54, 55, 76, 78, 82, 83,
}
UNVERIFIED_NUMBERS = {4, 6, 21, 29, 36, 37, 45, 48, 63}
THEORY_NUMBERS = {11, 14, 16, 17, 57}
CORRECT_TARGETS = {
    **{number: 83 for number in (1, 2, 3, 76, 78, 82, 83)},
    **{number: 87 for number in (7, 9, 10, 12, 13, 15, 18, 19, 20, 27, 28)},
    **{number: 78 for number in (22, 23, 25, 31, 35, 38, 39, 41, 42, 44)},
    **{number: 79 for number in (49, 50, 51, 52, 53, 54, 55)},
}
PHASE_STEPS = {
    70: "HISTORICAL_EVIDENCE_PRESERVATION", 71: "PRIMARY_SOURCE_ACQUISITION",
    73: "LITERATURE_APPLICABILITY", 74: "UNITS_TRANSFER_BOUNDARY",
    75: "BACKGROUND_ROOT_CLOSURE", 76: "INTEGRAL_RUNTIME_CLOSURE",
    78: "LCO_CANONICAL_SYNTHESIS", 79: "SILICON_CANONICAL_SYNTHESIS",
    81: "IDENTIFIABILITY_AND_INVERSE_VALIDATION", 82: "CANONICAL_EQUATION_FREEZE",
    83: "REPRODUCIBLE_IMPLEMENTATION", 86: "MATERIAL_VALIDATION",
    87: "CANONICAL_SOURCE_SYNTHESIS", 88: "FINAL_RED_TEAM", 89: "PDF_PRESERVATION",
}
TARGETS = {
    "AUTH-001": 83, "AUTH-002": 73, "AUTH-003": 76, "AUTH-004": 74,
    "AUTH-005": 76, "AUTH-006": 74, "AUTH-007": 88, "AUTH-008": 81,
    "AUTH-009": 86, "AUTH-010": 71, "AUTH-011": 75, "AUTH-012": 82,
    "AUTH-013": 83, "AUTH-014": 76,
    "RESID-015": 83, "RESID-016": 83, "RESID-017": 88, "RESID-018": 87,
}
CORRECTION_MAP = {
    "P064-S66-CORR-001": ["AUTH-006"], "P064-S66-CORR-002": ["AUTH-012"],
    "P064-S66-CORR-003": ["AUTH-003"], "P064-S66-CORR-004": ["AUTH-003"],
    "P064-S66-CORR-005": ["AUTH-002"], "P064-S66-CORR-006": ["AUTH-004"],
    "P064-S66-CORR-007": ["AUTH-005"], "P064-S66-CORR-008": ["AUTH-006"],
    "P064-S66-CORR-009": ["AUTH-001"], "P064-S66-CORR-010": ["AUTH-013"],
    "P064-S66-CORR-011": ["RESID-018"],
}
FINDING_MAP = {
    "P064-S67-F001": ["AUTH-006"], "P064-S67-F002": ["AUTH-011"],
    "P064-S67-F003": ["AUTH-005"], "P064-S67-F004": ["AUTH-003"],
    "P064-S67-F005": ["RESID-015"], "P064-S67-F006": ["AUTH-004"],
    "P064-S67-F007": ["RESID-016"], "P064-S67-F008": ["AUTH-001"],
    "P064-S67-F009": ["RESID-017"],
}
PROVISIONAL_TARGETS = {
    192: 70, 193: 70, 194: 70, 195: 76, 196: 76, 197: 74,
    198: 71, 199: 73, 200: 83, 201: 74, 202: 74, 203: 83,
    204: 73, 205: 71, 206: 88, 207: 74, 208: 73, 209: 73,
    210: 83, 211: 71, 212: 88, 213: 70, 214: 81, 215: 81,
    216: 74, 217: 71, 218: 81, 219: 86, 220: 81, 221: 81,
    222: 86, 223: 78, 224: 79, 225: 83, 226: 74, 227: 70,
}
PROVISIONAL_STATUSES = {
    192: "PRESERVED_HISTORICAL", 193: "PRESERVED_HISTORICAL", 194: "CLOSED_CONFIRMED",
    198: "PARTIALLY_RESOLVED_OPEN", 204: "PARTIALLY_RESOLVED_OPEN",
    213: "PRESERVED_HISTORICAL", 217: "PARTIALLY_RESOLVED_OPEN", 227: "PRESERVED_HISTORICAL",
}
PROVISIONAL_TO_AUTH = {
    192: ["AUTH-002"], 194: ["AUTH-002", "AUTH-003"], 195: ["AUTH-003"],
    196: ["AUTH-003"], 197: ["AUTH-006"], 198: ["AUTH-002", "AUTH-010"],
    199: ["AUTH-002", "AUTH-003"], 200: ["AUTH-003", "AUTH-007"],
    201: ["AUTH-007"], 202: ["AUTH-004"], 204: ["AUTH-009"],
    205: ["AUTH-010"], 206: ["AUTH-007"], 207: ["AUTH-006", "AUTH-007"],
    208: ["AUTH-003"], 209: ["AUTH-007"], 210: ["AUTH-007"],
    211: ["AUTH-010"], 212: ["AUTH-007"], 213: ["AUTH-007"],
    214: ["AUTH-008"], 215: ["AUTH-007", "AUTH-009"], 216: ["AUTH-006"],
    217: ["AUTH-010"], 218: ["AUTH-008"], 219: ["AUTH-006", "AUTH-009"],
    220: ["AUTH-008"], 221: ["AUTH-008"], 222: ["AUTH-009"],
    223: ["AUTH-009"], 224: ["AUTH-009"], 225: ["AUTH-013"],
    226: ["AUTH-004"], 227: ["AUTH-007"],
}


class ValidationError(RuntimeError):
    """Fail-closed Step 69.1 error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def run_git(*args: str, text: bool = True, cwd: pathlib.Path = REPO) -> str | bytes:
    process = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=text,
        encoding="utf-8" if text else None, errors="strict" if text else None,
        timeout=120, check=True,
    )
    return process.stdout


@functools.lru_cache(maxsize=None)
def git_bytes(revision: str, path: str) -> bytes:
    return run_git("show", f"{revision}:{path}", text=False)  # type: ignore[return-value]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def record_sha(value: Any) -> str:
    return sha256(compact(value))


def strict_load_bytes(raw: bytes, *, require_object: bool = False) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            require(key not in result, f"E_JSON_DUPLICATE_KEY:{key}")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{value}")

    def finite(value: str) -> float:
        parsed = float(value)
        require(math.isfinite(parsed), f"E_JSON_NONFINITE:{value}")
        return parsed

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant, parse_float=finite)
    except UnicodeDecodeError as exc:
        raise ValidationError(f"E_JSON_UTF8:{exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"E_JSON_SYNTAX:{exc.msg}") from exc
    if require_object:
        require(type(value) is dict, "E_JSON_ROOT_TYPE")
    return value


def strict_load(path: pathlib.Path) -> Any:
    return strict_load_bytes(path.read_bytes(), require_object=True)


def traversal_count(value: Any) -> int:
    if type(value) is dict:
        return 1 + len(value) + sum(traversal_count(child) for child in value.values())
    if type(value) is list:
        return 1 + sum(traversal_count(child) for child in value)
    if type(value) is float:
        require(math.isfinite(value), "E_TRAVERSAL_NONFINITE")
    return 1


def pointer_value(document: Any, pointer: str) -> Any:
    value = document
    for token in pointer.lstrip("/").split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if type(value) is list else value[token]
    return value


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    objects: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for path, expected_sha in INPUT_SHA256.items():
        raw = git_bytes(PARENT, path)
        require(sha256(raw) == expected_sha, f"E_INPUT_SHA:{path}")
        require((REPO / path).read_bytes() == raw, f"E_INPUT_WORKTREE:{path}")
        objects[path] = strict_load_bytes(raw, require_object=True)
        metadata.append({
            "path": path, "commit": PARENT,
            "git_blob": str(run_git("rev-parse", f"{PARENT}:{path}")).strip(),
            "sha256": expected_sha, "bytes": len(raw), "parse_mode": "STRICT_JSON_FULL_TRAVERSAL",
        })
    return objects, metadata


def portable_ast_value(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"node": type(value).__name__, "fields": {name: portable_ast_value(child) for name, child in ast.iter_fields(value) if name != "type_params"}}
    if isinstance(value, list):
        return [portable_ast_value(child) for child in value]
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    return value


def portable_ast_sha(raw: bytes) -> str:
    packed = json.dumps(portable_ast_value(ast.parse(raw.decode("utf-8"), filename=BUILDER)), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(packed)


def validate_builder_policy(candidate: bytes | None = None, *, raw_pin: bool = True, ast_pin: bool = True) -> None:
    raw = (REPO / BUILDER).read_bytes() if candidate is None else candidate
    if raw_pin:
        require(sha256(raw) == BUILDER_RAW_SHA256, "E_BUILDER_RAW_SHA256")
    tree = ast.parse(raw.decode("utf-8"), filename=BUILDER)
    if ast_pin:
        require(portable_ast_sha(raw) == BUILDER_AST_SHA256, "E_BUILDER_AST_SHA256")
    allowed = {"__future__", "argparse", "hashlib", "json", "math", "pathlib", "subprocess", "collections", "typing"}
    imports: set[str] = set()
    subprocess_calls: list[ast.Call] = []
    git_node: ast.AST | None = None
    forbidden: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
            forbidden.append(node.func.id)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
            subprocess_calls.append(node)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "git_bytes":
            require(git_node is None, "E_BUILDER_GIT_FUNCTION_DUPLICATE")
            git_node = node
    require(imports <= allowed, f"E_BUILDER_IMPORT_POLICY:{sorted(imports - allowed)}")
    require(not forbidden, f"E_BUILDER_DYNAMIC_EXEC:{forbidden}")
    require(git_node is not None, "E_BUILDER_GIT_FUNCTION_MISSING")
    require(len(subprocess_calls) == 1, f"E_BUILDER_SUBPROCESS_POLICY:{len(subprocess_calls)}")
    call = subprocess_calls[0]
    require(call in set(ast.walk(git_node)), "E_BUILDER_SUBPROCESS_SCOPE")
    require(bool(call.args) and isinstance(call.args[0], ast.List), "E_BUILDER_SUBPROCESS_ARGV")
    values = call.args[0].elts
    require(len(values) == 2 and isinstance(values[0], ast.Constant) and values[0].value == "git" and isinstance(values[1], ast.Starred), "E_BUILDER_SUBPROCESS_ARGV")


def expected_projection() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    with tempfile.TemporaryDirectory(prefix="p064-step69-1-projection-") as tmp:
        root = pathlib.Path(tmp)
        disposition = root / "disposition.json"
        carry = root / "carry.json"
        result = root / "result.md"
        subprocess.run(
            [sys.executable, "-B", str(REPO / BUILDER), "--repo", str(REPO), "--disposition", str(disposition), "--carry", str(carry), "--result", str(result)],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=300, check=True,
        )
        return strict_load(disposition), strict_load(carry), result.read_bytes()


def structure_equal(actual: Any, expected: Any, pointer: str = "") -> None:
    require(type(actual) is type(expected), f"E_STRUCTURE:{pointer}:type")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"E_STRUCTURE:{pointer}:keys")
        for key in expected:
            structure_equal(actual[key], expected[key], f"{pointer}/{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"E_STRUCTURE:{pointer}:length")
        for index, (left, right) in enumerate(zip(actual, expected)):
            structure_equal(left, right, f"{pointer}/{index}")


def validate_evidence(route: dict[str, Any], inputs: dict[str, Any]) -> Any:
    require(route["artifact_path"] in inputs, f"E_EVIDENCE_PATH:{route['artifact_path']}")
    try:
        record = pointer_value(inputs[route["artifact_path"]], route["json_pointer"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ValidationError(f"E_EVIDENCE_POINTER:{route['artifact_path']}:{route['json_pointer']}") from exc
    require(record_sha(record) == route["record_sha256"], "E_EVIDENCE_HASH")
    return record


def expected_disposition(number: int) -> str:
    if number in CORRECT_NUMBERS:
        return "CORRECT"
    if number in UNVERIFIED_NUMBERS:
        return "UNVERIFIED"
    if number in THEORY_NUMBERS:
        return "THEORY_ONLY"
    return "PRESERVE"


def expected_target(source: dict[str, Any], disposition: str) -> int:
    number = int(source["occurrence_id"].rsplit("-", 1)[1])
    path = source["path"].lower()
    if disposition == "CORRECT": return CORRECT_TARGETS[number]
    if disposition == "UNVERIFIED": return 71
    if disposition == "THEORY_ONLY": return 82
    if source["role"] in {"generated_document", "figure"}: return 89
    if source["role"] == "result": return 70
    if "/ch2" in path: return 78
    if "/ch3" in path: return 79
    return 87


def expected_source_authority_links(source: dict[str, Any]) -> list[str]:
    lower = source["path"].lower()
    profile = source.get("token_profile", {})
    links: set[str] = set()
    if profile.get("c_rate", 0) or profile.get("factor_3600", 0): links.add("AUTH-006")
    if profile.get("fredholm", 0) or profile.get("ref6_ref7", 0): links.add("AUTH-002")
    if profile.get("picard", 0) or profile.get("ratio", 0) or profile.get("volterra", 0): links.update(("AUTH-003", "AUTH-014"))
    if profile.get("transfer", 0) or profile.get("omega", 0): links.update(("AUTH-004", "AUTH-005"))
    if source["role"] in {"code", "test", "implementation_guide", "supporting_document"}: links.add("AUTH-013")
    if any(token in lower for token in ("phase_p5", "merge_readiness", "aud_report", "execution_ledger")): links.update(("AUTH-007", "RESID-017"))
    if any(token in lower for token in ("curve_qa", "qa_v102")): links.update(("AUTH-008", "AUTH-009", "AUTH-013"))
    if "ch1v22_bib" in lower: links.update(("AUTH-002", "AUTH-010", "AUTH-012"))
    if any(token in lower for token in ("appe_selfconsistent", "cond_audit", "p1_ratio_check")): links.add("AUTH-001")
    if "test_gates_v1023_selfconsistent" in lower: links.add("RESID-015")
    if "p1_ratio_check" in lower: links.add("RESID-016")
    if "ch1_sec09_tail" in lower: links.add("RESID-018")
    if source["role"] == "code": links.add("AUTH-011")
    return sorted(links)


def expected_v1022_counterpart(source: dict[str, Any], prior_rows: list[dict[str, Any]]) -> tuple[int, dict[str, Any]] | None:
    candidate = source["path"].replace("/v1.0.23/", "/v1.0.22/").replace("v1.0.23", "v1.0.22").replace("v1023", "v1022")
    matches = [(index, row) for index, row in enumerate(prior_rows) if row["source_identity"]["path"] == candidate]
    require(len(matches) <= 1, "E_V1022_COUNTERPART_DUPLICATE")
    return matches[0] if matches else None


def validate_observation(route: dict[str, Any], record: dict[str, Any], path: str, pointer: str, target: int, links: list[str], status: str) -> None:
    require(route["origin_path"] == path and route["origin_pointer"] == pointer and route["origin_record_sha256"] == record_sha(record), "E_OBSERVATION_ORIGIN")
    require(route["prior_record"] == record, "E_OBSERVATION_RECORD")
    require(route["status_after"] == status, "E_OBSERVATION_STATUS")
    require(route["primary_target"] == {"phase": target, "step": PHASE_STEPS[target]}, "E_OBSERVATION_TARGET")
    require(route["current_owner_id"] == f"PHASE-{target:03d}-CANONICAL-WORK-QUEUE", "E_OBSERVATION_OWNER")
    require(route["corroborating_authority_route_ids"] == links, "E_OBSERVATION_LINKS")
    require(route["downstream_target_phases"] == list(range(target + 1, 91)), "E_OBSERVATION_DOWNSTREAM")
    require(route["blocker_identity_created"] is False and route["authority_flags"] == {"external_truth": False, "canonical_adoption": False}, "E_OBSERVATION_AUTHORITY")


def validate_semantics(disposition: dict[str, Any], carry: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]], projection: tuple[dict[str, Any], dict[str, Any], bytes]) -> None:
    require(set(disposition) == {"artifact_kind", "authority_boundary", "baseline_commit", "counts", "gate", "input_commit", "inputs", "phase", "result_first", "schema_version", "source_contract", "source_dispositions", "step", "supplemental_dispositions"}, "E_DISPOSITION_SCHEMA")
    require(set(carry) == {"artifact_kind", "authority_boundary", "baseline_commit", "canonical_owner_duplicate_check_universe", "equation38_supersession_binding", "gate", "gate_summary", "inherited_phase063_snapshot", "input_commit", "inputs", "new_phase064_blockers", "phase", "phase057_provisional_routes", "phase066_correction_observations", "phase067_finding_observations", "phase068_authority_routes", "residual_topical_routes", "result_first", "schema_version", "source_disposition_links", "step", "supplemental_disposition_links"}, "E_CARRY_SCHEMA")
    structure_equal(disposition, projection[0], "/disposition")
    structure_equal(carry, projection[1], "/carry")
    require(disposition["schema_version"] == "P064_STEP69_1_DISPOSITION_V1" and carry["schema_version"] == "P064_STEP69_1_CARRY_FORWARD_V1", "E_SCHEMA_VERSION")
    require(disposition["phase"] == carry["phase"] == 64 and disposition["step"] == carry["step"] == "69.1", "E_PHASE_STEP")
    require(disposition["baseline_commit"] == carry["baseline_commit"] == BASELINE and disposition["input_commit"] == carry["input_commit"] == PARENT, "E_INPUT_IDENTITY")
    require(disposition["inputs"] == carry["inputs"] == metadata, "E_INPUT_METADATA")
    require(disposition["result_first"] == carry["result_first"] == {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"}, "E_RESULT_FIRST")
    require(disposition["gate"] == carry["gate"] == GATE, "E_GATE")
    require(disposition["authority_boundary"] == carry["authority_boundary"] == AUTHORITY, "E_AUTHORITY")
    require(disposition["source_contract"] == {"manifest_occurrences": 83, "supplemental_occurrences": 6, "supplemental_by_denominator": {"literature": 4, "plan": 1, "process": 1}, "identity_rule": "ONE_DISPOSITION_PER_OCCURRENCE_ID; NO_MANIFEST_SUPPLEMENTAL_OR_AUTHORITY_FUSION"}, "E_SOURCE_CONTRACT")

    sources = inputs[TOPOLOGY]["sources"]
    reads = inputs[READ]["sources"]
    rows = disposition["source_dispositions"]
    require(len(sources) == len(reads) == len(rows) == 83, "E_SOURCE_COUNT")
    require(len({row["source_id"] for row in rows}) == len({row["disposition_id"] for row in rows}) == 83, "E_SOURCE_DUPLICATE")
    evidence_ids: list[str] = []
    prior_rows = inputs[P63_DISPOSITION]["source_dispositions"]
    counterpart_count = 0
    for index, (source, read, row) in enumerate(zip(sources, reads, rows), 1):
        require(row["source_id"] == source["occurrence_id"] and row["disposition_id"] == f"P064-DISP-{index:04d}", "E_SOURCE_ORDER")
        require(row["source_identity"] == source and row["source_record_sha256"] == record_sha(source), "E_SOURCE_IDENTITY")
        expected = expected_disposition(index)
        require(row["disposition"] in ALLOWED and row["disposition"] == expected, "E_SOURCE_DISPOSITION")
        status = "OPEN_UNVERIFIED" if expected == "UNVERIFIED" else "OPEN_CORRECTION" if expected == "CORRECT" else "BOUNDED_PRESERVE"
        require(row["status"] == status, "E_SOURCE_STATUS")
        target = expected_target(source, expected)
        require(row["primary_target"] == {"phase": target, "step": PHASE_STEPS[target]} and row["downstream_target_phases"] == list(range(target + 1, 91)), "E_SOURCE_TARGET")
        require(row["current_owner_id"] == f"PHASE-{target:03d}-{PHASE_STEPS[target]}", "E_SOURCE_OWNER")
        require(bool(row["reason"].strip()) and bool(row["acceptance_criterion"].strip()) and bool(row["non_double_count_basis"].strip()), "E_SOURCE_RECOVERY_FIELDS")
        require(row["authority_flags"] == {"canonical_equation": False, "external_experimental": False, "external_material": False, "external_scientific": False, "publication_ready": False}, "E_SOURCE_AUTHORITY")
        require(row["evidence_ids"] == [route["evidence_id"] for route in row["evidence_routes"]], "E_SOURCE_EVIDENCE_IDS")
        require(row["evidence_routes"][0]["artifact_path"] == TOPOLOGY and row["evidence_routes"][0]["json_pointer"] == f"/sources/{index - 1}", "E_SOURCE_TOPOLOGY_ROUTE")
        require(row["evidence_routes"][1]["artifact_path"] == READ and row["evidence_routes"][1]["json_pointer"] == f"/sources/{index - 1}" and record_sha(read) == row["evidence_routes"][1]["record_sha256"], "E_SOURCE_READ_ROUTE")
        expected_links = expected_source_authority_links(source)
        require(row["corroborating_authority_route_ids"] == expected_links and row["carry_forward_links"] == [f"P064-SOURCE-ROUTE-{index:04d}", *expected_links], "E_SOURCE_AUTHORITY_LINKS")
        counterpart = expected_v1022_counterpart(source, prior_rows)
        counterpart_routes = [route for route in row["evidence_routes"] if route["route_role"] == "V1022_LINEAGE_COUNTERPART"]
        if counterpart is None:
            require(counterpart_routes == [] and row["inherited_owner_id"] is None, "E_V1022_COUNTERPART")
        else:
            prior_index, prior_row = counterpart
            require(len(counterpart_routes) == 1 and counterpart_routes[0]["artifact_path"] == P63_DISPOSITION and counterpart_routes[0]["json_pointer"] == f"/source_dispositions/{prior_index}" and counterpart_routes[0]["record_sha256"] == record_sha(prior_row) and row["inherited_owner_id"] == prior_row["canonical_owner_id"], "E_V1022_COUNTERPART")
            counterpart_count += 1
        for route in row["evidence_routes"]:
            validate_evidence(route, inputs)
            evidence_ids.append(route["evidence_id"])
    require(counterpart_count == 63, "E_V1022_COUNTERPART_COUNT")
    require(len(evidence_ids) == len(set(evidence_ids)), "E_SOURCE_EVIDENCE_DUPLICATE")
    distribution = dict(sorted(Counter(row["disposition"] for row in rows).items()))
    status_distribution = dict(sorted(Counter(row["status"] for row in rows).items()))
    require(distribution == {"CORRECT": 35, "PRESERVE": 34, "THEORY_ONLY": 5, "UNVERIFIED": 9}, "E_SOURCE_DISTRIBUTION")
    require(status_distribution == {"BOUNDED_PRESERVE": 39, "OPEN_CORRECTION": 35, "OPEN_UNVERIFIED": 9}, "E_SOURCE_STATUS_DISTRIBUTION")
    require(disposition["counts"] == {"duplicate_source_membership": 0, "external_authority_promotions": 0, "open_source_dispositions": 44, "open_supplemental_dispositions": 1, "source_disposition_distribution": distribution, "source_dispositions": 83, "source_orphans": 0, "source_status_distribution": status_distribution, "supplemental_dispositions": 6}, "E_DISPOSITION_COUNTS")

    supplemental = disposition["supplemental_dispositions"]
    plan_candidates = [(index, row) for index, row in enumerate(inputs[RATIO]["source_contracts"]) if row["path"].startswith("Claude/plans/")]
    require(len(plan_candidates) == 1, "E_SUPPLEMENTAL_PLAN")
    plan_index, plan = plan_candidates[0]
    literature_sources = {row["source_id"]: (index, row) for index, row in enumerate(inputs[LITERATURE]["sources"])}
    require(set(literature_sources) == {"JCP147", "REF6", "REF7"}, "E_SUPPLEMENTAL_LITERATURE_SET")
    extract = inputs[LITERATURE]["bibliography_boundaries"]["printed_reference_list"]
    process_anchor = {
        "p4_state": inputs[TOPOLOGY]["process"]["p4_state"],
        "p4_result_present": inputs[TOPOLOGY]["process"]["p4_result_present"],
        "phase_state": inputs[TOPOLOGY]["process"]["phase_states"]["P4"],
    }
    supplemental_specs = [
        ("P064-SUP-PLAN-001", "PLAN", plan, "PRESERVE", "BOUNDED_PROCESS_EVIDENCE", None, 87, RATIO, f"/source_contracts/{plan_index}"),
        ("P064-SUP-LIT-001", "LITERATURE_ORIGINAL", literature_sources["JCP147"][1], "THEORY_ONLY", "FULL_TEXT_READ_BOUNDED_METHOD", None, 73, LITERATURE, f"/sources/{literature_sources['JCP147'][0]}"),
        ("P064-SUP-LIT-002", "LITERATURE_ORIGINAL", literature_sources["REF6"][1], "THEORY_ONLY", "FULL_TEXT_READ_BOUNDED_METHOD", None, 73, LITERATURE, f"/sources/{literature_sources['REF6'][0]}"),
        ("P064-SUP-LIT-003", "LITERATURE_METADATA_AND_GNF", literature_sources["REF7"][1], "UNVERIFIED", "OPEN_GROUND_NOT_FOUND", "PHASE-071-PRIMARY-SOURCE-ACQUISITION", 71, LITERATURE, f"/sources/{literature_sources['REF7'][0]}"),
        ("P064-SUP-LIT-004", "LITERATURE_EXTRACT", extract, "PRESERVE", "BOUNDED_DERIVED_TEXT", None, 73, LITERATURE, "/bibliography_boundaries/printed_reference_list"),
        ("P064-SUP-PROC-001", "PROCESS_DECISION", process_anchor, "PRESERVE", "INTENTIONAL_SKIP_PRESERVED", "PHASE-081-IDENTIFIABILITY-AUTHORIZATION", 81, TOPOLOGY, "/process"),
    ]
    require(len(supplemental) == len(supplemental_specs) == 6, "E_SUPPLEMENTAL_DENOMINATOR")
    require([row["supplemental_id"] for row in supplemental] == [spec[0] for spec in supplemental_specs] and all(row["manifest_member"] is False for row in supplemental), "E_SUPPLEMENTAL_DENOMINATOR")
    by_id = {row["supplemental_id"]: row for row in supplemental}
    ref6 = by_id["P064-SUP-LIT-002"]["source_anchor"]
    require(ref6["authority"]["original_full_text_status"] == "FULL_TEXT_READ" and ref6["authority"]["pages_read"] == 4 and ref6["authority"]["raw_sha256"] == "c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460", "E_REF6_CLOSURE")
    ref7_row = by_id["P064-SUP-LIT-003"]
    require(ref7_row["source_anchor"]["bibliographic_identity"]["doi"] == "10.1063/1.4802584" and ref7_row["source_anchor"]["authority"]["original_full_text_status"] == "GROUND_NOT_FOUND" and ref7_row["status"] == "OPEN_GROUND_NOT_FOUND" and ref7_row["current_owner_id"] == "PHASE-071-PRIMARY-SOURCE-ACQUISITION", "E_REF7_GNF")
    conflict = inputs[LITERATURE]["conflicts"][0]
    require(conflict["candidate_ref7_doi"] == "10.1063/1.4802005" and conflict["disposition"] == "REJECT_AS_REF7_DOI", "E_REF7_WRONG_DOI")
    process_row = by_id["P064-SUP-PROC-001"]
    require(process_row["source_anchor"] == {"p4_state": "SKIPPED_D3_NOT_APPROVED", "p4_result_present": False, "phase_state": "SKIPPED_D3_NOT_APPROVED"} and process_row["status"] == "INTENTIONAL_SKIP_PRESERVED" and process_row["current_owner_id"] == "PHASE-081-IDENTIFIABILITY-AUTHORIZATION", "E_P4_SKIP")
    for index, (row, (item_id, denominator, anchor, expected, status, owner, target, path, pointer)) in enumerate(zip(supplemental, supplemental_specs), 1):
        require(row["supplemental_id"] == item_id and row["denominator"] == denominator and row["manifest_member"] is False and row["source_anchor"] == anchor and row["source_record_sha256"] == record_sha(anchor), "E_SUPPLEMENTAL_IDENTITY")
        require(row["disposition"] == expected and row["status"] == status and row["inherited_owner_id"] == ("PHASE-064-STEP65-LITERATURE-ACQUISITION" if item_id == "P064-SUP-LIT-003" else None), "E_SUPPLEMENTAL_CONTRACT")
        require(row["current_owner_id"] == owner and row["primary_target"] == {"phase": target, "step": PHASE_STEPS[target]} and row["downstream_target_phases"] == list(range(target + 1, 91)), "E_SUPPLEMENTAL_TARGET")
        evidence_record = pointer_value(inputs[path], pointer)
        expected_route = {"evidence_id": f"P064-SUP-EVID-{index:03d}", "artifact_path": path, "json_pointer": pointer, "record_sha256": record_sha(evidence_record), "route_role": denominator}
        require(row["evidence_routes"] == [expected_route] and bool(row["acceptance_criterion"]), "E_SUPPLEMENTAL_EVIDENCE")
        validate_evidence(row["evidence_routes"][0], inputs)
        require(row["authority_flags"] == {"external_experimental": False, "external_material": False, "publication_ready": False, "ref7_method_content": False}, "E_SUPPLEMENTAL_AUTHORITY")

    source_links = carry["source_disposition_links"]
    require(len(source_links) == 83, "E_SOURCE_LINK_COUNT")
    for row, link in zip(rows, source_links):
        require(link == {"source_id": row["source_id"], "disposition_id": row["disposition_id"], "status": row["status"], "current_owner_id": row["current_owner_id"], "primary_target": row["primary_target"], "carry_forward_links": row["carry_forward_links"]}, "E_SOURCE_LINK_PROJECTION")
    expected_supplemental_links = [{"supplemental_id": row["supplemental_id"], "denominator": row["denominator"], "status": row["status"], "current_owner_id": row["current_owner_id"], "primary_target": row["primary_target"]} for row in supplemental]
    require(carry["supplemental_disposition_links"] == expected_supplemental_links, "E_SUPPLEMENTAL_LINK_PROJECTION")

    provisional_records = inputs[TOPOLOGY]["phase057_observations"]["records"]
    provisional_routes = carry["phase057_provisional_routes"]
    require(len(provisional_records) == len(provisional_routes) == 36, "E_PHASE057_COUNT")
    for index, (record, route) in enumerate(zip(provisional_records, provisional_routes)):
        numeric = int(record["id"].rsplit("-", 1)[1])
        require(route["route_id"] == f"P064-P057-ROUTE-{index + 1:04d}", "E_PHASE057_ORDER")
        validate_observation(route, record, TOPOLOGY, f"/phase057_observations/records/{index}", PROVISIONAL_TARGETS[numeric], PROVISIONAL_TO_AUTH.get(numeric, []), PROVISIONAL_STATUSES.get(numeric, "OPEN_CARRY_OBSERVATION"))

    for section, path, records, mapping, prefix in (
        (carry["phase066_correction_observations"], RATIO, inputs[RATIO]["correction_register"], CORRECTION_MAP, "P064-S66-OBS"),
        (carry["phase067_finding_observations"], CODE_DELTA, inputs[CODE_DELTA]["findings"], FINDING_MAP, "P064-S67-OBS"),
    ):
        require(len(section) == len(records), "E_CURRENT_OBSERVATION_COUNT")
        key = "correction_register" if path == RATIO else "findings"
        for index, (record, route) in enumerate(zip(records, section)):
            links = mapping[record["id"]]
            target = min(TARGETS[item] for item in links)
            require(route["route_id"] == f"{prefix}-{index + 1:04d}", "E_CURRENT_OBSERVATION_ORDER")
            validate_observation(route, record, path, f"/{key}/{index}", target, links, "OPEN_CARRY_OBSERVATION")

    authority_originals = inputs[AUTHORITY_MATRIX]["overclaim_routes"]
    authority_routes = carry["phase068_authority_routes"]
    require(len(authority_originals) == len(authority_routes) == 14 and [row["route_id"] for row in authority_routes] == [f"AUTH-{i:03d}" for i in range(1, 15)], "E_AUTH_ROUTE_COUNT")
    for index, (record, route) in enumerate(zip(authority_originals, authority_routes)):
        route_id = record["id"]
        require(route["origin_path"] == AUTHORITY_MATRIX and route["origin_pointer"] == f"/overclaim_routes/{index}" and route["origin_record_sha256"] == record_sha(record) and route["prior_record"] == record, "E_AUTH_ROUTE_ORIGIN")
        require(route["inherited_owner_id"] == record["owner"] and route["acceptance_criterion"] == record["acceptance_criterion"], "E_AUTH_ROUTE_CONTENT")
        target = TARGETS[route_id]
        if route_id == "AUTH-012":
            require(route["status_after"] == "CLOSED_BOUND_IN_STEP69_1" and route["closure_owner_id"] == "STEP-069-1-EQ38-SUPERSESSION-BINDING" and route["current_owner_id"] == "PHASE-082-CANONICAL-EQUATION-FREEZE" and route["primary_target"] == {"phase": 82, "step": "CANONICAL_EQUATION_FREEZE"}, "E_AUTH12_CLOSURE")
        else:
            require(route["status_after"] == "OPEN_CARRY" and route["closure_owner_id"] is None and route["current_owner_id"] == f"PHASE-{target:03d}-AUTHORITY-{route_id}" and route["primary_target"] == {"phase": target, "step": "AUTHORITY_CLOSURE"}, "E_AUTH_ROUTE_OWNER")
        require(route["downstream_target_phases"] == list(range(route["primary_target"]["phase"] + 1, 91)) and route["authority_flags"] == {"external_truth": False, "canonical_adoption": False, "publication_ready": False}, "E_AUTH_ROUTE_AUTHORITY")

    residual = carry["residual_topical_routes"]
    residual_specs = [("RESID-015", CODE_DELTA, "/findings/4", 83), ("RESID-016", CODE_DELTA, "/findings/6", 83), ("RESID-017", CODE_DELTA, "/findings/8", 88), ("RESID-018", RATIO, "/correction_register/10", 87)]
    require(len(residual) == 4 and [row["route_id"] for row in residual] == [row[0] for row in residual_specs], "E_RESIDUAL_COUNT")
    for route, (route_id, path, pointer, target) in zip(residual, residual_specs):
        record = pointer_value(inputs[path], pointer)
        require(route["origin_path"] == path and route["origin_pointer"] == pointer and route["origin_record_sha256"] == record_sha(record) and route["prior_record"] == record, "E_RESIDUAL_ORIGIN")
        require(route["status_after"] == "OPEN_CARRY" and route["current_owner_id"] == f"PHASE-{target:03d}-RESIDUAL-{route_id}" and route["primary_target"] == {"phase": target, "step": "RESIDUAL_AUTHORITY_CLOSURE"}, "E_RESIDUAL_OWNER")
        require("NOT_SUBSUMED" in route["non_double_count_basis"] and route["authority_flags"] == {"external_truth": False, "canonical_adoption": False, "publication_ready": False}, "E_RESIDUAL_NON_DOUBLE_COUNT")

    binding = carry["equation38_supersession_binding"]
    require(binding["binding_id"] == "P064-EQ38-SUPERSESSION-001" and binding["authority_route_id"] == "AUTH-012" and binding["status"] == "CLOSED_BOUND_IN_STEP69_1", "E_EQ38_BINDING")
    require("K*r*mu" in binding["superseded_projection"] and "K*sigma*mu" in binding["superseding_projection"] and binding["retained_crop_raw_pixel_sha256"] == "63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978", "E_EQ38_SEMANTICS")
    require(binding["closure_owner_id"] == "STEP-069-1-EQ38-SUPERSESSION-BINDING" and binding["next_owner_id"] == "PHASE-082-CANONICAL-EQUATION-FREEZE", "E_EQ38_OWNER")
    for route in binding["evidence_routes"]: validate_evidence(route, inputs)

    inherited = carry["inherited_phase063_snapshot"]
    require(inherited["origin_path"] == P63_CARRY and inherited["origin_pointer"] == "" and inherited["prior_record"] == inputs[P63_CARRY] and inherited["prior_record_sha256"] == record_sha(inputs[P63_CARRY]), "E_INHERITED_PHASE063")
    require(inherited["status_after"] == "CARRIED_FORWARD_LOSSLESS", "E_INHERITED_STATUS")
    prior_owners = inputs[P63_CARRY]["canonical_owner_duplicate_check_universe"]["records"]
    universe = carry["canonical_owner_duplicate_check_universe"]
    require(universe["schema_version"] == "P064_CANONICAL_OWNER_UNIVERSE_V1" and universe["record_count"] == len(universe["records"]) == 326, "E_OWNER_UNIVERSE_COUNT")
    require(len({row["registry_id"] for row in universe["records"]}) == 326 and universe["records_sha256"] == record_sha(universe["records"]), "E_OWNER_UNIVERSE_HASH")
    for prior, row in zip(prior_owners, universe["records"][:308]):
        require(row == {"registry_id": f"P064-INHERITED-{prior['registry_id']}", "denominator_section": "INHERITED_PHASE063_OWNER_UNIVERSE", "origin_identity": prior["origin_identity"], "owner_id": prior["owner_id"], "target_phase": prior["target_phase"], "origin_record_sha256": record_sha(prior), "active_current_authority_route": False}, "E_OWNER_UNIVERSE_INHERITED")
    topical = [*authority_routes, *residual]
    for route, row in zip(topical, universe["records"][308:]):
        require(row["origin_identity"] == route["route_id"] and row["owner_id"] == route["current_owner_id"] and row["target_phase"] == route["primary_target"]["phase"] and row["active_current_authority_route"] == (route["status_after"] == "OPEN_CARRY"), "E_OWNER_UNIVERSE_CURRENT")
    require(carry["new_phase064_blockers"] == [], "E_NEW_BLOCKER")
    expected_summary = {"canonical_owner_duplicate_check_records": 326, "closed_topical_routes": 1, "equation38_supersession_bindings": 1, "external_authority_promotions": 0, "inherited_phase063_owner_records": 308, "multiply_owned_open_routes": 0, "new_phase064_blockers": 0, "open_source_dispositions": 44, "open_supplemental_acquisition_routes": 1, "open_topical_routes": 17, "ownerless_open_routes": 0, "phase057_provisional_routes": 36, "phase066_correction_observations": 11, "phase067_finding_observations": 9, "phase068_authority_routes": 14, "phase_ceiling": "CONDITIONAL_P064", "ref6_original_full_text": "FULL_TEXT_READ_4_OF_4", "ref7_original_full_text": "GROUND_NOT_FOUND", "residual_topical_routes": 4, "source_disposition_links": 83, "status": "PASS_WITH_CONCERNS", "supplemental_disposition_links": 6, "topical_routes": 18}
    require(carry["gate_summary"] == expected_summary, "E_GATE_SUMMARY")
    require(canonical(disposition) == canonical(projection[0]) and canonical(carry) == canonical(projection[1]), "E_EXACT_PROJECTION")


def validate_recovery_texts(result: str, parent_ledger: str, active_ledger: str, handover: str, disposition_sha: str, carry_sha: str) -> None:
    lines = result.splitlines()
    require([line for line in lines if line.startswith("Gate:")] == [f"Gate: `{GATE}`"], "E_RESULT_GATE")
    require([line for line in lines if line.startswith("Terminal:")] == [f"Terminal: `{GATE}`"], "E_RESULT_TERMINAL")
    require([line for line in lines if line.startswith("Result-first sentinel:")] == [f"Result-first sentinel: `{SENTINEL}`"], "E_RESULT_SENTINEL")
    require([line for line in lines if line.startswith("Containing commit:")] == ["Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`"], "E_RESULT_COMMIT")
    require(not any(token in result for token in ("Gate: `FAIL", "Terminal: `FAIL", "Overall status: FAIL")), "E_RESULT_CONTRADICTION")
    require(all(token in result for token in (PARENT, disposition_sha, carry_sha, "83/83", "14` plus non-subsumed", "18` topical", "Ref. 6", "Ref. 7", "CONDITIONAL_P064")), "E_RESULT_RECOVERY")
    parent_rows = [line for line in parent_ledger.splitlines() if line.startswith("| 064 | 64–69 |")]
    active_rows = [line for line in active_ledger.splitlines() if line.startswith("| 064 | 64–69 |")]
    step_rows = [line for line in active_ledger.splitlines() if line.startswith("| Step 69.1 |")]
    handover_rows = [line for line in handover.splitlines() if line.startswith("| Phase 064 Step 69.1 |")]
    require(len(parent_rows) == len(active_rows) == len(step_rows) == len(handover_rows) == 1, "E_RECOVERY_ROW_COUNT")
    required = (GATE, PARENT, SUBJECT, SENTINEL, disposition_sha, carry_sha, "PENDING_AT_PRECOMMIT_BY_DESIGN")
    for row in (*parent_rows, *active_rows, *step_rows, *handover_rows):
        require(all(row.count(token) == 1 for token in required), "E_RECOVERY_ROW_CONTENT")
        require("FAIL" not in row and "CONDITIONAL" not in row, "E_RECOVERY_ROW_CONTRADICTION")
    for text in (parent_ledger, active_ledger, handover):
        require("84b977a5333870529369d62a6dab8459a6aa551d" in text and "PASS_P064_STEP68_PERSISTENCE" in text, "E_STEP68_RECONCILIATION")
    require(f"16. 현재 result: `{RESULT}`" in handover and "Step 69.2" in handover and "PASS_P064_STEP69_1_PERSISTENCE" in handover, "E_HANDOVER_CURRENT")


def validate_result_and_recovery() -> None:
    process = subprocess.run([sys.executable, "-B", str(REPO / BUILDER), "--repo", str(REPO), "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=300, check=True)
    require("PASS_P064_STEP69_1_BUILDER_CHECK" in process.stdout, "E_BUILDER_CHECK")
    validate_recovery_texts(
        (REPO / RESULT).read_text(encoding="utf-8"),
        (REPO / PARENT_LEDGER).read_text(encoding="utf-8"),
        (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8"),
        (REPO / HANDOVER).read_text(encoding="utf-8"),
        sha256((REPO / DISPOSITION).read_bytes()), sha256((REPO / CARRY).read_bytes()),
    )


def run_negative_probes(disposition: dict[str, Any], carry: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]], projection: tuple[dict[str, Any], dict[str, Any], bytes]) -> tuple[int, int, int, int, int]:
    probes: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], None], str]] = []
    def add(name: str, mutate: Callable[[dict[str, Any], dict[str, Any]], None], diagnostic: str) -> None: probes.append((name, mutate, diagnostic))
    def swap_source_ids(d: dict[str, Any], _c: dict[str, Any]) -> None:
        rows = d["source_dispositions"]
        rows[0]["source_id"], rows[1]["source_id"] = rows[1]["source_id"], rows[0]["source_id"]
    def edit_supplemental_anchor(d: dict[str, Any], index: int, mutate: Callable[[dict[str, Any]], None]) -> None:
        row = d["supplemental_dispositions"][index]
        mutate(row["source_anchor"])
        row["source_record_sha256"] = record_sha(row["source_anchor"])
    def edit_current_owner(_d: dict[str, Any], c: dict[str, Any]) -> None:
        universe = c["canonical_owner_duplicate_check_universe"]
        universe["records"][308]["owner_id"] = "generic"
        universe["records_sha256"] = record_sha(universe["records"])
    def edit_source_authority_link(d: dict[str, Any], c: dict[str, Any]) -> None:
        index = next(i for i, row in enumerate(d["source_dispositions"]) if row["corroborating_authority_route_ids"])
        row = d["source_dispositions"][index]
        row["corroborating_authority_route_ids"][0] = "AUTH-999"
        row["carry_forward_links"][1] = "AUTH-999"
        c["source_disposition_links"][index]["carry_forward_links"][1] = "AUTH-999"
    def break_v1022_counterpart(d: dict[str, Any], _c: dict[str, Any]) -> None:
        route = next(route for row in d["source_dispositions"] for route in row["evidence_routes"] if route["route_role"] == "V1022_LINEAGE_COUNTERPART")
        route["route_role"] = "BROKEN_COUNTERPART"
    add("disposition_schema", lambda d, c: d.__setitem__("invented", True), "E_DISPOSITION_SCHEMA")
    add("carry_schema", lambda d, c: c.__setitem__("invented", True), "E_CARRY_SCHEMA")
    add("nested_type", lambda d, c: d["source_dispositions"][0].__setitem__("status", 1), "E_STRUCTURE")
    add("phase", lambda d, c: d.__setitem__("phase", 65), "E_PHASE_STEP")
    add("input", lambda d, c: c.__setitem__("input_commit", "0" * 40), "E_INPUT_IDENTITY")
    add("result_first", lambda d, c: d["result_first"].__setitem__("containing_commit", "invented"), "E_RESULT_FIRST")
    add("gate", lambda d, c: c.__setitem__("gate", "PASS"), "E_GATE")
    add("source_loss", lambda d, c: d["source_dispositions"].pop(), "E_STRUCTURE")
    add("source_reorder", swap_source_ids, "E_SOURCE_ORDER")
    add("source_identity", lambda d, c: d["source_dispositions"][0]["source_identity"].__setitem__("blob_sha1", "0" * 40), "E_SOURCE_IDENTITY")
    add("source_disposition", lambda d, c: d["source_dispositions"][0].__setitem__("disposition", "PRESERVE"), "E_SOURCE_DISPOSITION")
    add("source_status", lambda d, c: d["source_dispositions"][0].__setitem__("status", "BOUNDED_PRESERVE"), "E_SOURCE_STATUS")
    add("source_target", lambda d, c: d["source_dispositions"][0]["primary_target"].__setitem__("phase", 82), "E_SOURCE_TARGET")
    add("source_owner", lambda d, c: d["source_dispositions"][0].__setitem__("current_owner_id", "generic"), "E_SOURCE_OWNER")
    add("source_authority", lambda d, c: d["source_dispositions"][0]["authority_flags"].__setitem__("external_scientific", True), "E_SOURCE_AUTHORITY")
    add("source_authority_link", edit_source_authority_link, "E_SOURCE_AUTHORITY_LINKS")
    add("v1022_counterpart", break_v1022_counterpart, "E_V1022_COUNTERPART")
    add("source_pointer", lambda d, c: d["source_dispositions"][0]["evidence_routes"][0].__setitem__("json_pointer", "/sources/99"), "E_SOURCE_TOPOLOGY_ROUTE")
    add("source_evidence_hash", lambda d, c: d["source_dispositions"][0]["evidence_routes"][0].__setitem__("record_sha256", "0" * 64), "E_EVIDENCE_HASH")
    add("source_link", lambda d, c: d["source_dispositions"][0]["carry_forward_links"].pop(), "E_STRUCTURE")
    add("source_projection", lambda d, c: c["source_disposition_links"][0].__setitem__("status", "wrong"), "E_SOURCE_LINK_PROJECTION")
    add("supplemental_fusion", lambda d, c: d["supplemental_dispositions"][0].__setitem__("manifest_member", True), "E_SUPPLEMENTAL_DENOMINATOR")
    add("supplemental_status", lambda d, c: d["supplemental_dispositions"][0].__setitem__("status", "OPEN_GROUND_NOT_FOUND"), "E_SUPPLEMENTAL_CONTRACT")
    add("supplemental_projection", lambda d, c: c["supplemental_disposition_links"][0].__setitem__("status", "wrong"), "E_SUPPLEMENTAL_LINK_PROJECTION")
    add("ref6_false_open", lambda d, c: edit_supplemental_anchor(d, 2, lambda anchor: anchor["authority"].__setitem__("original_full_text_status", "GROUND_NOT_FOUND")), "E_REF6_CLOSURE")
    add("ref7_false_present", lambda d, c: edit_supplemental_anchor(d, 3, lambda anchor: anchor["authority"].__setitem__("original_full_text_status", "FULL_TEXT_READ")), "E_REF7_GNF")
    add("ref7_wrong_doi", lambda d, c: edit_supplemental_anchor(d, 3, lambda anchor: anchor["bibliographic_identity"].__setitem__("doi", "10.1063/1.4802005")), "E_REF7_GNF")
    add("p4_fabricated", lambda d, c: edit_supplemental_anchor(d, 5, lambda anchor: anchor.__setitem__("p4_result_present", True)), "E_P4_SKIP")
    add("p4_failure", lambda d, c: edit_supplemental_anchor(d, 5, lambda anchor: anchor.__setitem__("p4_state", "FAILED")), "E_P4_SKIP")
    add("phase057_loss", lambda d, c: c["phase057_provisional_routes"].pop(), "E_STRUCTURE")
    add("phase057_target", lambda d, c: c["phase057_provisional_routes"][0]["primary_target"].__setitem__("phase", 71), "E_OBSERVATION_TARGET")
    add("phase057_status", lambda d, c: c["phase057_provisional_routes"][2].__setitem__("status_after", "OPEN_CARRY_OBSERVATION"), "E_OBSERVATION_STATUS")
    add("phase057_link", lambda d, c: c["phase057_provisional_routes"][0].__setitem__("corroborating_authority_route_ids", ["AUTH-999"]), "E_OBSERVATION_LINKS")
    add("phase057_owner", lambda d, c: c["phase057_provisional_routes"][0].__setitem__("current_owner_id", None), "E_STRUCTURE")
    add("correction_loss", lambda d, c: c["phase066_correction_observations"].pop(), "E_STRUCTURE")
    add("correction_mapping", lambda d, c: c["phase066_correction_observations"][10].__setitem__("corroborating_authority_route_ids", ["AUTH-009"]), "E_OBSERVATION_LINKS")
    add("finding_loss", lambda d, c: c["phase067_finding_observations"].pop(), "E_STRUCTURE")
    add("finding_subsumption", lambda d, c: c["phase067_finding_observations"][4].__setitem__("corroborating_authority_route_ids", ["AUTH-013"]), "E_OBSERVATION_LINKS")
    add("auth_loss", lambda d, c: c["phase068_authority_routes"].pop(), "E_STRUCTURE")
    add("auth_owner", lambda d, c: c["phase068_authority_routes"][0].__setitem__("current_owner_id", "generic"), "E_AUTH_ROUTE_OWNER")
    add("auth_promotion", lambda d, c: c["phase068_authority_routes"][0]["authority_flags"].__setitem__("external_truth", True), "E_AUTH_ROUTE_AUTHORITY")
    add("auth12_open", lambda d, c: c["phase068_authority_routes"][11].__setitem__("status_after", "OPEN_CARRY"), "E_AUTH12_CLOSURE")
    add("residual_loss", lambda d, c: c["residual_topical_routes"].pop(), "E_STRUCTURE")
    add("residual_owner", lambda d, c: c["residual_topical_routes"][0].__setitem__("current_owner_id", "generic"), "E_RESIDUAL_OWNER")
    add("residual_subsume", lambda d, c: c["residual_topical_routes"][0].__setitem__("non_double_count_basis", "SUBSUMED"), "E_RESIDUAL_NON_DOUBLE_COUNT")
    add("eq38_stale", lambda d, c: c["equation38_supersession_binding"].__setitem__("superseded_projection", "K*sigma*mu"), "E_EQ38_SEMANTICS")
    add("eq38_correct", lambda d, c: c["equation38_supersession_binding"].__setitem__("superseding_projection", "K*r*mu"), "E_EQ38_SEMANTICS")
    add("eq38_crop", lambda d, c: c["equation38_supersession_binding"].__setitem__("retained_crop_raw_pixel_sha256", "0" * 64), "E_EQ38_SEMANTICS")
    add("eq38_owner", lambda d, c: c["equation38_supersession_binding"].__setitem__("next_owner_id", "generic"), "E_EQ38_OWNER")
    add("inherited_mutation", lambda d, c: c["inherited_phase063_snapshot"]["prior_record"].__setitem__("invented", True), "E_STRUCTURE")
    add("inherited_hash", lambda d, c: c["inherited_phase063_snapshot"].__setitem__("prior_record_sha256", "0" * 64), "E_INHERITED_PHASE063")
    add("owner_loss", lambda d, c: c["canonical_owner_duplicate_check_universe"]["records"].pop(), "E_STRUCTURE")
    add("owner_hash", lambda d, c: c["canonical_owner_duplicate_check_universe"].__setitem__("records_sha256", "0" * 64), "E_OWNER_UNIVERSE_HASH")
    add("owner_current", edit_current_owner, "E_OWNER_UNIVERSE_CURRENT")
    add("new_blocker", lambda d, c: c["new_phase064_blockers"].append({"id": "invented"}), "E_STRUCTURE")
    add("summary_ownerless", lambda d, c: c["gate_summary"].__setitem__("ownerless_open_routes", 1), "E_GATE_SUMMARY")
    add("authority_boundary", lambda d, c: c["authority_boundary"].__setitem__("primary_literature_ref7_method_truth", True), "E_AUTHORITY")
    add("projection", lambda d, c: d["source_dispositions"][0].__setitem__("reason", "invented"), "E_EXACT_PROJECTION")
    passed = 0
    for name, mutate, diagnostic in probes:
        d = copy.deepcopy(disposition); c = copy.deepcopy(carry); mutate(d, c)
        try: validate_semantics(d, c, inputs, metadata, projection)
        except ValidationError as exc:
            require(str(exc).split(":", 1)[0] == diagnostic, f"E_NEGATIVE_DIAGNOSTIC:{name}:{exc}!={diagnostic}"); passed += 1
        else: raise ValidationError(f"E_NEGATIVE_ESCAPED:{name}")

    strict_fixtures = [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":-Infinity}', b'{"a":', b'{"a":1} x', b'{"a":1e9999}', b'\xff', b'[1,2]']
    strict_passed = 0
    for raw in strict_fixtures:
        try: strict_load_bytes(raw, require_object=True)
        except ValidationError: strict_passed += 1
        else: raise ValidationError("E_STRICT_JSON_ESCAPED")

    disposition_sha = sha256((REPO / DISPOSITION).read_bytes()); carry_sha = sha256((REPO / CARRY).read_bytes())
    docs = [(REPO / RESULT).read_text(encoding="utf-8"), (REPO / PARENT_LEDGER).read_text(encoding="utf-8"), (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8"), (REPO / HANDOVER).read_text(encoding="utf-8")]
    current_rows = [
        next(line for line in docs[1].splitlines() if line.startswith("| 064 | 64–69 |")),
        next(line for line in docs[2].splitlines() if line.startswith("| 064 | 64–69 |")),
        next(line for line in docs[2].splitlines() if line.startswith("| Step 69.1 |")),
        next(line for line in docs[3].splitlines() if line.startswith("| Phase 064 Step 69.1 |")),
    ]
    recovery = [
        ("result_fail", 0, lambda text: text + "\nOverall status: FAIL\n", "E_RESULT_CONTRADICTION"),
        ("result_gate", 0, lambda text: text.replace(f"Gate: `{GATE}`", "Gate: `PASS`", 1), "E_RESULT_GATE"),
        ("parent_hash", 1, lambda text: text.replace(current_rows[0], current_rows[0].replace(disposition_sha, "0" * 64, 1), 1), "E_RECOVERY_ROW_CONTENT"),
        ("active_duplicate", 2, lambda text: text + "\n" + current_rows[1] + "\n", "E_RECOVERY_ROW_COUNT"),
        ("step_subject", 2, lambda text: text.replace(current_rows[2], current_rows[2].replace(SUBJECT, "wrong", 1), 1), "E_RECOVERY_ROW_CONTENT"),
        ("handover_commit", 3, lambda text: text.replace(current_rows[3], current_rows[3].replace("PENDING_AT_PRECOMMIT_BY_DESIGN", "invented", 1), 1), "E_RECOVERY_ROW_CONTENT"),
        ("handover_fail", 3, lambda text: text.replace(current_rows[3], current_rows[3] + " FAIL", 1), "E_RECOVERY_ROW_CONTRADICTION"),
        ("step68_loss", 3, lambda text: text.replace("PASS_P064_STEP68_PERSISTENCE", "missing"), "E_STEP68_RECONCILIATION"),
        ("handover_result", 3, lambda text: text.replace(f"16. 현재 result: `{RESULT}`", "16. 현재 result: `wrong`", 1), "E_HANDOVER_CURRENT"),
        ("result_sha", 0, lambda text: text.replace(disposition_sha, "0" * 64, 1), "E_RESULT_RECOVERY"),
    ]
    recovery_passed = 0
    for name, index, mutate, diagnostic in recovery:
        mutated = list(docs); mutated[index] = mutate(mutated[index])
        try: validate_recovery_texts(*mutated, disposition_sha, carry_sha)
        except ValidationError as exc:
            require(str(exc).split(":", 1)[0] == diagnostic, f"E_RECOVERY_DIAGNOSTIC:{name}:{exc}!={diagnostic}"); recovery_passed += 1
        else: raise ValidationError(f"E_RECOVERY_ESCAPED:{name}")

    builder_raw = (REPO / BUILDER).read_bytes(); text = builder_raw.decode("utf-8")
    policies = [
        (builder_raw + b"\n# mutate\n", True, True, "E_BUILDER_RAW_SHA256"),
        (text.replace("timeout=120", "timeout=121", 1).encode(), False, True, "E_BUILDER_AST_SHA256"),
        (text.replace("    process = subprocess.run(", "    subprocess.run(['git', '--version'])\n    process = subprocess.run(", 1).encode(), False, False, "E_BUILDER_SUBPROCESS_POLICY"),
        (text.replace('["git", *args]', '["cmd", *args]', 1).encode(), False, False, "E_BUILDER_SUBPROCESS_ARGV"),
    ]
    policy_passed = 0
    for raw, raw_pin, ast_pin, diagnostic in policies:
        try: validate_builder_policy(raw, raw_pin=raw_pin, ast_pin=ast_pin)
        except ValidationError as exc:
            require(str(exc).split(":", 1)[0] == diagnostic, f"E_POLICY_DIAGNOSTIC:{exc}"); policy_passed += 1
        else: raise ValidationError("E_POLICY_ESCAPED")
    return passed, len(probes), strict_passed, recovery_passed, policy_passed


def determinism_check() -> None:
    with tempfile.TemporaryDirectory(prefix="p064-step69-1-determinism-") as tmp:
        root = pathlib.Path(tmp); outputs: list[tuple[bytes, bytes, bytes]] = []
        for run in (1, 2):
            d = root / f"d-{run}.json"; c = root / f"c-{run}.json"; r = root / f"r-{run}.md"
            subprocess.run([sys.executable, "-B", str(REPO / BUILDER), "--repo", str(REPO), "--disposition", str(d), "--carry", str(c), "--result", str(r)], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=300, check=True)
            outputs.append((d.read_bytes(), c.read_bytes(), r.read_bytes()))
        require(outputs[0] == outputs[1], "E_DETERMINISM_2X")
        require(outputs[0] == ((REPO / DISPOSITION).read_bytes(), (REPO / CARRY).read_bytes(), (REPO / RESULT).read_bytes()), "E_DETERMINISM_STORED")
    print("PASS_P064_STEP69_1_DETERMINISM 2/2")


def live_ref(ref: str) -> str:
    output = str(run_git("ls-remote", "origin", ref)).strip()
    require(bool(output), f"E_LIVE_REF:{ref}")
    return output.split()[0]


def safe_index_equal(path: str) -> bool:
    try: return run_git("show", f":{path}", text=False) == (REPO / path).read_bytes()
    except (OSError, subprocess.CalledProcessError): return False


def safe_commit_equal(commit: str, path: str) -> bool:
    try: return git_bytes(commit, path) == (REPO / path).read_bytes()
    except (OSError, subprocess.CalledProcessError): return False


def validate_staged_snapshot(snapshot: dict[str, Any], *, parent: str, branch: str, upstream: str, protected: str, main: str, paths: list[str]) -> None:
    require(snapshot["head"] == parent, "E_STAGED_PARENT")
    require(snapshot["branch"] == branch, "E_STAGED_BRANCH")
    require(snapshot["upstream"] == upstream and snapshot["upstream_commit"] == parent, "E_STAGED_UPSTREAM")
    require(snapshot["active_tracking"] == snapshot["active_live"] == parent, "E_STAGED_ACTIVE_REMOTE")
    require(snapshot["protected_local"] == snapshot["protected_tracking"] == snapshot["protected_live"] == protected, "E_STAGED_PROTECTED")
    require(snapshot["main_tracking"] == snapshot["main_live"] == main, "E_STAGED_MAIN")
    require(snapshot["staged"] == sorted(paths), "E_STAGED_PATHS")
    require(snapshot["claude_status"] == [] and not any(path.startswith("Claude/") for path in snapshot["staged"]), "E_STAGED_CLAUDE")
    require(snapshot["unstaged"] == [] and snapshot["untracked"] == [] and snapshot["diff_check"], f"E_STAGED_DIRTY:{snapshot['unstaged']}:{snapshot['untracked']}:{snapshot['diff_check']}")
    require(snapshot["equal"] == {path: True for path in paths}, "E_STAGED_INDEX_WORKTREE")


def validate_persistence_snapshot(snapshot: dict[str, Any], *, commit: str, parent: str, subject: str, branch: str, upstream: str, protected: str, main: str, paths: list[str]) -> None:
    require(snapshot["head"] == commit and len(commit) == 40, "E_PERSIST_HEAD")
    require(snapshot["parent"] == parent, "E_PERSIST_PARENT")
    require(snapshot["subject"] == subject, "E_PERSIST_SUBJECT")
    require(snapshot["committed"] == sorted(paths), "E_PERSIST_PATHS")
    require(snapshot["branch"] == branch and snapshot["upstream"] == upstream, "E_PERSIST_BRANCH")
    require(snapshot["upstream_commit"] == snapshot["active_tracking"] == snapshot["active_live"] == commit, "E_PERSIST_ACTIVE_REMOTE")
    require(snapshot["protected_local"] == snapshot["protected_tracking"] == snapshot["protected_live"] == protected, "E_PERSIST_PROTECTED")
    require(snapshot["main_tracking"] == snapshot["main_live"] == main, "E_PERSIST_MAIN")
    require(snapshot["status"] == [] and snapshot["claude_diff"] == snapshot["claude_status"] == [], "E_PERSIST_DIRTY")
    require(snapshot["equal"] == {path: True for path in paths}, "E_PERSIST_COMMIT_WORKTREE")


def production_staged_snapshot() -> dict[str, Any]:
    status = str(run_git("status", "--porcelain=v1", "--untracked-files=all")).splitlines()
    return {
        "head": str(run_git("rev-parse", "HEAD")).strip(), "branch": str(run_git("branch", "--show-current")).strip(),
        "upstream": str(run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")).strip(), "upstream_commit": str(run_git("rev-parse", "@{u}")).strip(),
        "active_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip(), "active_live": live_ref(f"refs/heads/{BRANCH}"),
        "protected_local": str(run_git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}")).strip(), "protected_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip(), "protected_live": live_ref(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_tracking": str(run_git("rev-parse", "refs/remotes/origin/main")).strip(), "main_live": live_ref("refs/heads/main"),
        "staged": str(run_git("diff", "--cached", "--name-only")).splitlines(), "unstaged": str(run_git("diff", "--name-only")).splitlines(),
        "untracked": [line[3:] for line in status if line.startswith("?? ")], "diff_check": subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, timeout=60).returncode == 0,
        "claude_status": str(run_git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")).splitlines(), "equal": {path: safe_index_equal(path) for path in EXACT_PATHS},
    }


def production_persistence_snapshot(commit: str) -> dict[str, Any]:
    return {
        "head": str(run_git("rev-parse", "HEAD")).strip(), "parent": str(run_git("rev-parse", f"{commit}^")).strip(), "subject": str(run_git("show", "-s", "--format=%s", commit)).rstrip("\r\n"),
        "committed": sorted(str(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", commit)).splitlines()), "branch": str(run_git("branch", "--show-current")).strip(),
        "upstream": str(run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")).strip(), "upstream_commit": str(run_git("rev-parse", "@{u}")).strip(),
        "active_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip(), "active_live": live_ref(f"refs/heads/{BRANCH}"),
        "protected_local": str(run_git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}")).strip(), "protected_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip(), "protected_live": live_ref(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_tracking": str(run_git("rev-parse", "refs/remotes/origin/main")).strip(), "main_live": live_ref("refs/heads/main"),
        "status": str(run_git("status", "--porcelain=v1", "--untracked-files=all")).splitlines(), "claude_diff": str(run_git("diff", "--name-only", PARENT, commit, "--", "Claude")).splitlines(),
        "claude_status": str(run_git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")).splitlines(), "equal": {path: safe_commit_equal(commit, path) for path in EXACT_PATHS},
    }


def git_fixture() -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="p064-step69-1-git-") as tmp:
        root = pathlib.Path(tmp); work = root / "work"; bare = root / "origin.git"; work.mkdir()
        def g(cwd: pathlib.Path, *args: str) -> str: return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=60, check=True).stdout.strip()
        def gb(cwd: pathlib.Path, *args: str) -> bytes: return subprocess.run(["git", *args], cwd=cwd, capture_output=True, timeout=60, check=True).stdout
        g(work, "init", "--initial-branch=main"); g(work, "config", "user.email", "step69@example.invalid"); g(work, "config", "user.name", "Step69 Fixture"); g(work, "config", "core.autocrlf", "false"); g(work, "config", "core.whitespace", "cr-at-eol")
        (work / "base.txt").write_text("base\n", encoding="utf-8"); (work / "victim.txt").write_text("must survive\n", encoding="utf-8"); (work / "Claude").mkdir(); (work / "Claude" / "keep.txt").write_text("protected\n", encoding="utf-8")
        g(work, "add", "."); g(work, "commit", "-m", "base"); base = g(work, "rev-parse", "HEAD")
        g(work, "branch", "protected", base); g(work, "branch", "active", base); g(work, "switch", "-c", "drift", base); g(work, "commit", "--allow-empty", "-m", "drift"); drift = g(work, "rev-parse", "HEAD"); g(work, "switch", "active")
        g(root, "init", "--bare", str(bare)); g(work, "remote", "add", "origin", str(bare)); g(work, "push", "origin", "main", "protected", "drift:fixture-drift"); g(work, "push", "-u", "origin", "active")
        paths = [f"evidence-{i}.txt" for i in range(8)]
        for path in paths: (work / path).write_text(path + "\n", encoding="utf-8")
        g(work, "add", *paths)
        def live(ref: str) -> str: return g(root, "--git-dir", str(bare), "rev-parse", ref)
        def staged_snapshot() -> dict[str, Any]:
            status = g(work, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
            equal = {}
            for path in paths:
                try: equal[path] = gb(work, "show", f":{path}") == (work / path).read_bytes()
                except (OSError, subprocess.CalledProcessError): equal[path] = False
            return {"head": g(work, "rev-parse", "HEAD"), "branch": g(work, "branch", "--show-current"), "upstream": g(work, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"), "upstream_commit": g(work, "rev-parse", "@{u}"), "active_tracking": g(work, "rev-parse", "refs/remotes/origin/active"), "active_live": live("refs/heads/active"), "protected_local": g(work, "rev-parse", "refs/heads/protected"), "protected_tracking": g(work, "rev-parse", "refs/remotes/origin/protected"), "protected_live": live("refs/heads/protected"), "main_tracking": g(work, "rev-parse", "refs/remotes/origin/main"), "main_live": live("refs/heads/main"), "staged": g(work, "diff", "--cached", "--name-only").splitlines(), "unstaged": g(work, "diff", "--name-only").splitlines(), "untracked": [line[3:] for line in status if line.startswith("?? ")], "diff_check": subprocess.run(["git", "diff", "--cached", "--check"], cwd=work, capture_output=True).returncode == 0, "claude_status": g(work, "status", "--porcelain=v1", "--untracked-files=all", "--", "Claude").splitlines(), "equal": equal}
        passed = 0
        def expect(name: str, diagnostic: str, action: Callable[[], None]) -> None:
            nonlocal passed
            action()
            try: validate_staged_snapshot(staged_snapshot(), parent=base, branch="active", upstream="origin/active", protected=base, main=base, paths=paths)
            except ValidationError as exc: require(str(exc).split(":", 1)[0] == diagnostic, f"E_GIT_DIAGNOSTIC:{name}:{exc}!={diagnostic}"); passed += 1
            else: raise ValidationError(f"E_GIT_ESCAPED:{name}")
        validate_staged_snapshot(staged_snapshot(), parent=base, branch="active", upstream="origin/active", protected=base, main=base, paths=paths)
        extra = work / "extra.txt"; expect("extra", "E_STAGED_PATHS", lambda: (extra.write_text("x\n"), g(work, "add", "extra.txt"))); g(work, "restore", "--staged", "extra.txt"); extra.unlink()
        victim = work / "victim.txt"; victim.unlink(); g(work, "add", "-u", "--", "victim.txt"); expect("deletion", "E_STAGED_PATHS", lambda: None); g(work, "restore", "--staged", "--", "victim.txt"); g(work, "restore", "--worktree", "--", "victim.txt")
        expect("missing", "E_STAGED_PATHS", lambda: g(work, "restore", "--staged", paths[-1])); g(work, "add", paths[-1])
        original = (work / paths[0]).read_bytes(); expect("index_worktree", "E_STAGED_INDEX_WORKTREE", lambda: ((work / paths[0]).write_text("changed\n"), g(work, "update-index", "--assume-unchanged", paths[0]))); (work / paths[0]).write_bytes(original); g(work, "update-index", "--no-assume-unchanged", paths[0])
        expect("branch", "E_STAGED_BRANCH", lambda: (g(work, "switch", "-c", "wrong"), g(work, "config", "branch.wrong.remote", "origin"), g(work, "config", "branch.wrong.merge", "refs/heads/active"))); g(work, "switch", "active")
        expect("upstream", "E_STAGED_UPSTREAM", lambda: g(work, "branch", "--set-upstream-to", "origin/main", "active")); g(work, "branch", "--set-upstream-to", "origin/active", "active")
        expect("active_live", "E_STAGED_ACTIVE_REMOTE", lambda: g(root, "--git-dir", str(bare), "update-ref", "refs/heads/active", drift)); g(root, "--git-dir", str(bare), "update-ref", "refs/heads/active", base)
        expect("protected_local", "E_STAGED_PROTECTED", lambda: g(work, "branch", "-f", "protected", drift)); g(work, "branch", "-f", "protected", base)
        expect("protected_live", "E_STAGED_PROTECTED", lambda: g(root, "--git-dir", str(bare), "update-ref", "refs/heads/protected", drift)); g(root, "--git-dir", str(bare), "update-ref", "refs/heads/protected", base)
        expect("main_live", "E_STAGED_MAIN", lambda: g(root, "--git-dir", str(bare), "update-ref", "refs/heads/main", drift)); g(root, "--git-dir", str(bare), "update-ref", "refs/heads/main", base)
        claude = work / "Claude" / "drift.txt"; expect("claude", "E_STAGED_CLAUDE", lambda: claude.write_text("x\n")); claude.unlink()
        dirty = work / "dirty.txt"; expect("untracked", "E_STAGED_DIRTY", lambda: dirty.write_text("x\n")); dirty.unlink()
        (work / paths[1]).write_text("bad \n", encoding="utf-8"); g(work, "add", paths[1]); expect("diff_check", "E_STAGED_DIRTY", lambda: None); (work / paths[1]).write_text(paths[1] + "\n", encoding="utf-8"); g(work, "add", paths[1])
        g(work, "commit", "-m", "wrong subject"); wrong = g(work, "rev-parse", "HEAD")
        def persisted(commit: str) -> dict[str, Any]:
            equal = {path: gb(work, "show", f"{commit}:{path}") == (work / path).read_bytes() for path in paths}
            return {"head": g(work, "rev-parse", "HEAD"), "parent": g(work, "rev-parse", f"{commit}^"), "subject": g(work, "show", "-s", "--format=%s", commit), "committed": sorted(g(work, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines()), "branch": g(work, "branch", "--show-current"), "upstream": g(work, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"), "upstream_commit": g(work, "rev-parse", "@{u}"), "active_tracking": g(work, "rev-parse", "refs/remotes/origin/active"), "active_live": live("refs/heads/active"), "protected_local": g(work, "rev-parse", "refs/heads/protected"), "protected_tracking": g(work, "rev-parse", "refs/remotes/origin/protected"), "protected_live": live("refs/heads/protected"), "main_tracking": g(work, "rev-parse", "refs/remotes/origin/main"), "main_live": live("refs/heads/main"), "status": g(work, "status", "--porcelain=v1", "--untracked-files=all").splitlines(), "claude_diff": g(work, "diff", "--name-only", base, commit, "--", "Claude").splitlines(), "claude_status": g(work, "status", "--porcelain=v1", "--untracked-files=all", "--", "Claude").splitlines(), "equal": equal}
        def pexpect(name: str, diagnostic: str, snapshot: Callable[[], dict[str, Any]]) -> None:
            nonlocal passed
            try: validate_persistence_snapshot(snapshot(), commit=g(work, "rev-parse", "HEAD"), parent=base, subject=SUBJECT, branch="active", upstream="origin/active", protected=base, main=base, paths=paths)
            except ValidationError as exc: require(str(exc).split(":", 1)[0] == diagnostic, f"E_GIT_PERSIST_DIAGNOSTIC:{name}:{exc}!={diagnostic}"); passed += 1
            else: raise ValidationError(f"E_GIT_PERSIST_ESCAPED:{name}")
        pexpect("subject", "E_PERSIST_SUBJECT", lambda: persisted(wrong))
        g(work, "commit", "--amend", "-m", SUBJECT); committed = g(work, "rev-parse", "HEAD"); g(work, "push", "origin", "active")
        validate_persistence_snapshot(persisted(committed), commit=committed, parent=base, subject=SUBJECT, branch="active", upstream="origin/active", protected=base, main=base, paths=paths)
        (work / paths[0]).write_text("dirty\n", encoding="utf-8"); pexpect("dirty", "E_PERSIST_DIRTY", lambda: persisted(committed)); (work / paths[0]).write_bytes(gb(work, "show", f"{committed}:{paths[0]}") )
        g(work, "switch", "drift");
        for path in paths: (work / path).write_text(path + "\n", encoding="utf-8")
        g(work, "add", *paths); g(work, "commit", "-m", SUBJECT); wrong_parent = g(work, "rev-parse", "HEAD"); g(work, "branch", "-f", "active", wrong_parent); g(work, "switch", "active")
        pexpect("parent", "E_PERSIST_PARENT", lambda: persisted(wrong_parent))
        g(work, "reset", "--hard", committed)
        # committed-path and commit/worktree mutations are evaluated against synthetic snapshots to keep the fixture recoverable.
        snap = persisted(committed); snap["committed"] = snap["committed"][:-1]
        try: validate_persistence_snapshot(snap, commit=committed, parent=base, subject=SUBJECT, branch="active", upstream="origin/active", protected=base, main=base, paths=paths)
        except ValidationError as exc: require(str(exc).split(":", 1)[0] == "E_PERSIST_PATHS", "E_GIT_PATH_DIAGNOSTIC"); passed += 1
        else: raise ValidationError("E_GIT_PATH_ESCAPED")
        snap = persisted(committed); snap["equal"][paths[0]] = False
        try: validate_persistence_snapshot(snap, commit=committed, parent=base, subject=SUBJECT, branch="active", upstream="origin/active", protected=base, main=base, paths=paths)
        except ValidationError as exc: require(str(exc).split(":", 1)[0] == "E_PERSIST_COMMIT_WORKTREE", "E_GIT_EQUAL_DIAGNOSTIC"); passed += 1
        else: raise ValidationError("E_GIT_EQUAL_ESCAPED")
        return passed, 18


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    try:
        require(not (args.verify_staged and args.verify_persistence), "E_MODE_CONFLICT")
        validate_builder_policy()
        inputs, metadata = load_inputs()
        disposition = strict_load(REPO / DISPOSITION); carry = strict_load(REPO / CARRY)
        projection = expected_projection()
        validate_semantics(disposition, carry, inputs, metadata, projection)
        validate_result_and_recovery()
        nodes = sum(traversal_count(value) for value in [*inputs.values(), disposition, carry])
        strong = args.verify_staged or args.verify_persistence
        if args.run_negative_probes or strong:
            semantic, semantic_total, strict_count, recovery_count, policy_count = run_negative_probes(disposition, carry, inputs, metadata, projection)
            git_count, git_total = git_fixture()
            require(semantic == semantic_total == 58 and strict_count == 9 and recovery_count == 10 and policy_count == 4 and git_count == git_total == 18, "E_NEGATIVE_TOTAL")
            print(f"PASS_P064_STEP69_1_NEGATIVE semantic={semantic}/{semantic_total} strict_json=9/9 recovery=10/10 builder_policy=4/4 git_boundary=18/18")
        if args.determinism_check or strong: determinism_check()
        if args.verify_staged:
            validate_staged_snapshot(production_staged_snapshot(), parent=PARENT, branch=BRANCH, upstream=f"origin/{BRANCH}", protected=PROTECTED_TIP, main=MAIN_TIP, paths=EXACT_PATHS)
            print("PASS_P064_STEP69_1_STAGED exact-eight")
        elif args.verify_persistence:
            require(bool(args.expected_commit), "E_EXPECTED_COMMIT_REQUIRED")
            validate_persistence_snapshot(production_persistence_snapshot(str(args.expected_commit)), commit=str(args.expected_commit), parent=PARENT, subject=SUBJECT, branch=BRANCH, upstream=f"origin/{BRANCH}", protected=PROTECTED_TIP, main=MAIN_TIP, paths=EXACT_PATHS)
            print(PERSISTENCE)
        else:
            print(f"{GATE} strict_traversal={nodes}")
        return 0
    except (KeyError, IndexError, OSError, subprocess.CalledProcessError, SyntaxError, TypeError, ValidationError, ValueError) as exc:
        print(f"FAIL_P064_STEP69_1: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
