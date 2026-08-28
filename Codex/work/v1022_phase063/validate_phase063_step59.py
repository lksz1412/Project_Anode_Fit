#!/usr/bin/env python3
"""Validate Phase 063 Step 59 equation/material rederivation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1022_phase063/build_phase063_step59_equation_material_rederivation.py"
ARTIFACT = REPO / "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_059_EQUATION_MATERIAL_REDERIVATION_RESULT.md"
TOPOLOGY = REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
PHASE057 = REPO / "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "2ccee1af3a59a3a1e5c9fe7192e4f916c454521a"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase063): rederive v1022 equation material"
GATE = "PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
EVIDENCE_BEGIN = "<!-- P063_STEP59_DERIVATION_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P063_STEP59_DERIVATION_EVIDENCE_END -->"
TIMEOUT = 300

EXACT_SEVEN = (
    "Codex/work/v1022_phase063/build_phase063_step59_equation_material_rederivation.py",
    "Codex/work/v1022_phase063/validate_phase063_step59.py",
    "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json",
    "Codex/results/PHASE_063_STEP_059_EQUATION_MATERIAL_REDERIVATION_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_SEVEN_SET = set(EXACT_SEVEN)

# Finalized after all four recovery documents reach their precommit form.  The
# validator is excluded to avoid a self-referential digest.
CONTROL_SHA256: dict[str, str] = {
    "result": "6d7cb13ca9fd3c820900bfd00a8d1071272ae7c6e10ffa804554291753f815e1",
    "active_ledger": "fe9afd486f045ad55ce628cfdc95ac11d716e6cacd31078bc1daadb3bee2cecf",
    "parent_ledger": "df42c4106f999b6a8b8f88e247dc5677a30335ab801b9188894ca8241dd5e223",
    "handover": "9e8ea812ecc6435635d9b3f124f5fa638555df192d7f94486b45ee042df9c0e2",
}

REQUIRED_GUARDS = {
    "independent_site_not_mean_field",
    "spinodal_not_binodal",
    "equilibrium_not_observation",
    "common_potential_not_equal_current",
    "mass_fraction_not_capacity_fraction",
    "larche_cahn_reversible_not_hysteresis_closure",
    "lco_global_offset_not_local_closure",
    "c_rate_requires_divide_3600",
    "tst_temperature_derivatives_retained",
    "reversible_heat_not_hysteretic_dissipation",
}
REQUIRED_SIGN_IDS = {f"P063-SIGN-{number:03d}" for number in range(1, 7)}
REQUIRED_OPERATOR_IDS = {f"P063-OP-{number:03d}" for number in range(1, 7)}
REQUIRED_MATERIAL_IDS = {f"P063-MAT-{number:03d}" for number in range(1, 7)}
REQUIRED_DERIVATION_IDS = {f"P063-DER-{number:03d}" for number in range(1, 26)}
REQUIRED_FINDING_IDS = {f"P063-S59-F{number:03d}" for number in range(1, 21)}
REQUIRED_PHASE057_NUMERIC_IDS = {
    100, 101, 106, 111, 112, 113, 114, 115, 116,
    118, 119, 120, 121, 122, 123, 126, 127,
    130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141,
    145, 146, 147, 148, 149, 150, 151,
    156, 157, 158, 159, 160, 161,
    165, 166, 167, 168, 169, 170, 171,
    183, 184, 185, 188, 189, 191,
}


class ValidationError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def strict_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"non-finite JSON number: {value}")
    return number


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def traverse(value: Any) -> int:
    if value is None or isinstance(value, (str, bool, int)):
        return 1
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite JSON number")
        return 1
    if isinstance(value, list):
        return 1 + sum(traverse(item) for item in value)
    if isinstance(value, dict):
        return 1 + sum(1 + traverse(item) for item in value.values())
    raise ValueError(f"unsupported JSON node: {type(value).__name__}")


def strict_load_text(text: str) -> tuple[Any, int]:
    value = json.loads(
        text, object_pairs_hook=strict_pairs, parse_constant=reject_constant,
        parse_float=strict_float,
    )
    return value, traverse(value)


def strict_load(path: Path) -> tuple[Any, int]:
    return strict_load_text(path.read_text(encoding="utf-8"))


def normalized_bytes(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8", "strict")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def evidence_block() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise ValidationError("result evidence marker cardinality")
    block = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise ValidationError("result evidence fence")
    value, _ = strict_load_text(block[len("```json\n"):-len("\n```")])
    if not isinstance(value, dict):
        raise ValidationError("result evidence root")
    return value, digest(compact(value))


def run(args: list[str], timeout: int = TIMEOUT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=timeout, check=False,
    )


def git_bytes(*args: str, check: bool = True) -> bytes:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise ValidationError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def git_text(*args: str, check: bool = True) -> str:
    return git_bytes(*args, check=check).decode("utf-8", "strict").strip()


def git_paths(*args: str) -> set[str]:
    return {
        item.decode("utf-8", "strict").replace("\\", "/")
        for item in git_bytes(*args).split(b"\0") if item
    }


def ref_hash(ref: str) -> str | None:
    value = git_text("show-ref", "--verify", "--hash", ref, check=False)
    return value or None


def remote_head(branch: str) -> str:
    ref = f"refs/heads/{branch}"
    rows = [line.split() for line in git_text("ls-remote", "--heads", "origin", ref).splitlines() if line.strip()]
    if len(rows) != 1 or rows[0][1] != ref:
        raise ValidationError(f"remote head cardinality: {branch}: {rows}")
    return rows[0][0]


def add(errors: set[str], condition: bool, code: str) -> None:
    if condition:
        errors.add(code)


def unique_ids(rows: Any, key: str) -> bool:
    return (
        isinstance(rows, list)
        and all(isinstance(row, dict) and isinstance(row.get(key), str) for row in rows)
        and len({row[key] for row in rows}) == len(rows)
    )


def verify_source_anchor(anchor: dict[str, Any], source_map: dict[str, dict[str, Any]]) -> bool:
    source = source_map.get(anchor.get("path"))
    if source is None:
        return False
    if anchor.get("source_id") != source.get("source_id") or anchor.get("git_blob") != source.get("git_blob"):
        return False
    intervals = anchor.get("line_intervals")
    extent = source.get("physical_lines")
    return (
        isinstance(intervals, list) and bool(intervals)
        and all(
            isinstance(interval, list) and len(interval) == 2
            and all(isinstance(number, int) for number in interval)
            and 1 <= interval[0] <= interval[1] <= extent
            for interval in intervals
        )
    )


def artifact_diagnostics(
    data: dict[str, Any], evidence_reference: dict[str, Any] | None = None,
) -> set[str]:
    errors: set[str] = set()
    add(errors, data.get("schema_version") != 1, "SCHEMA")
    add(errors, data.get("artifact_kind") != "V1022_EQUATION_MATERIAL_REDERIVATION", "KIND")
    add(errors, data.get("phase") != 63 or data.get("step") != 59, "PHASE_STEP")
    add(errors, data.get("status") != "PASS_WITH_CONCERNS", "STATUS")
    add(errors, data.get("gate") != GATE, "GATE")
    add(errors, data.get("baseline_commit") != BASELINE, "BASELINE")
    add(errors, data.get("expected_parent") != EXPECTED_PARENT, "PARENT")

    builder = data.get("builder", {})
    add(errors, builder.get("path") != EXACT_SEVEN[0], "BUILDER_PATH")
    add(errors, builder.get("normalized_sha256") != digest(normalized_bytes(BUILDER)), "BUILDER_SHA")
    contract = data.get("result_first_contract", {})
    add(errors, contract.get("result_path") != EXACT_SEVEN[3], "RESULT_PATH")
    add(errors, contract.get("containing_commit") != "PENDING_AT_PRECOMMIT_BY_DESIGN", "RESULT_PENDING")
    add(errors, contract.get("persistence_claimed") is not False, "FALSE_PERSISTENCE")
    add(errors, contract.get("step60_blocked_until") != "PASS_P063_STEP59_PERSISTENCE", "NEXT_GATE")
    live_evidence: dict[str, Any] | None = None
    try:
        live_evidence, evidence_sha = evidence_block()
        add(errors, contract.get("evidence_semantic_sha256") != evidence_sha, "EVIDENCE_SHA")
    except (OSError, ValueError, ValidationError):
        errors.add("EVIDENCE_BLOCK")

    counts = data.get("counts", {})
    add(errors, counts.get("reachable_tex_sources") != 53, "SOURCE_COUNT")
    add(errors, counts.get("display_equations") != 231, "EQUATION_COUNT")
    add(errors, counts.get("phase057_routes") != 55, "PHASE057_COUNT")
    add(errors, counts.get("manual_derivation_rows") != 25, "DERIVATION_COUNT")
    add(errors, counts.get("manual_sign_rows") != 6, "SIGN_COUNT")
    add(errors, counts.get("manual_operator_rows") != 6, "OPERATOR_COUNT")
    add(errors, counts.get("manual_material_rows") != 6, "MATERIAL_COUNT")
    add(errors, counts.get("findings") != 20, "FINDING_COUNT")

    sources = data.get("source_inventory")
    add(errors, not unique_ids(sources, "source_id"), "SOURCE_IDS")
    if isinstance(sources, list):
        add(errors, len(sources) != 53 or len({row.get("path") for row in sources}) != 53, "SOURCE_ROWS")
        add(errors, any(row.get("read_interval") != [1, row.get("physical_lines")] for row in sources), "SOURCE_READ")
    source_map = {row["path"]: row for row in sources} if isinstance(sources, list) else {}

    equations = data.get("display_equation_inventory")
    equation_ids_valid = unique_ids(equations, "equation_id")
    add(errors, not equation_ids_valid, "EQUATION_IDS")
    if isinstance(equations, list):
        if equation_ids_valid:
            add(
                errors,
                len(equations) != 231
                or [row.get("equation_id") for row in equations]
                != [f"P063-EQ-{i:04d}" for i in range(1, 232)],
                "EQUATION_ROWS",
            )
        for row in equations:
            source = source_map.get(row.get("path"))
            if source is None or row.get("source_id") != source.get("source_id") or row.get("git_blob") != source.get("git_blob"):
                errors.add("EQUATION_SOURCE")
                break
            start, end = row.get("start_line"), row.get("end_line")
            if not isinstance(start, int) or not isinstance(end, int) or not 1 <= start <= end <= source["physical_lines"]:
                errors.add("EQUATION_INTERVAL")
                break
            body = row.get("body")
            if not isinstance(body, str) or digest(body.encode("utf-8")) != row.get("body_sha256"):
                errors.add("EQUATION_BODY")
                break
            if row.get("line_count") != end - start + 1 or len(body.splitlines()) != row.get("line_count"):
                errors.add("EQUATION_EXTENT")
                break

    evidence = data.get("manual_rederivation_evidence", {})
    if evidence_reference is None:
        evidence_reference = live_evidence
    add(errors, evidence_reference is None or evidence != evidence_reference, "EVIDENCE_PARITY")
    add(errors, evidence.get("evidence_id") != "P063-STEP59-INDEPENDENT-REDERIVATION", "EVIDENCE_ID")
    add(errors, evidence.get("external_truth_state") != "UNVERIFIED_EXTERNAL", "EXTERNAL_STATE")
    guards = evidence.get("negative_claim_guards", {})
    add(errors, set(guards) != REQUIRED_GUARDS or not all(value is True for value in guards.values()), "CLAIM_GUARDS")
    derivations = evidence.get("derivation_rows")
    derivation_ids_valid = unique_ids(derivations, "derivation_id")
    add(errors, not derivation_ids_valid, "DERIVATION_IDS")
    if isinstance(derivations, list):
        add(errors, len(derivations) != 25, "DERIVATION_ROWS")
        if len(derivations) == 25 and derivation_ids_valid:
            add(errors, {row.get("derivation_id") for row in derivations} != REQUIRED_DERIVATION_IDS, "DERIVATION_ID_SET")
        add(errors, any(row.get("external_support") not in {"UNVERIFIED_EXTERNAL", "GROUND_NOT_FOUND"} for row in derivations), "DERIVATION_EXTERNAL")
        add(errors, any(row.get("disposition") not in {"PRESERVE", "PRESERVE_CONDITIONAL", "CORRECT", "REJECT", "UNRESOLVED"} for row in derivations), "DERIVATION_DISPOSITION")
        add(errors, any(not row.get("source_evidence") or not all(verify_source_anchor(anchor, source_map) for anchor in row["source_evidence"]) for row in derivations), "DERIVATION_ANCHOR")

    sign_rows = evidence.get("sign_ledger")
    add(errors, not unique_ids(sign_rows, "sign_id"), "SIGN_IDS")
    if isinstance(sign_rows, list):
        add(errors, {row["sign_id"] for row in sign_rows} != REQUIRED_SIGN_IDS, "SIGN_COVERAGE")
        add(errors, any(row.get("adjudicated") is not True for row in sign_rows), "SIGN_ADJUDICATION")
    operator_rows = evidence.get("operator_ledger")
    add(errors, not unique_ids(operator_rows, "operator_id"), "OPERATOR_IDS")
    if isinstance(operator_rows, list):
        add(errors, {row["operator_id"] for row in operator_rows} != REQUIRED_OPERATOR_IDS, "OPERATOR_COVERAGE")
        add(errors, any(row.get("collapsed_with") != [] for row in operator_rows), "OPERATOR_COLLAPSE")
    material_rows = evidence.get("material_scope_ledger")
    add(errors, not unique_ids(material_rows, "material_id"), "MATERIAL_IDS")
    if isinstance(material_rows, list):
        add(errors, {row["material_id"] for row in material_rows} != REQUIRED_MATERIAL_IDS, "MATERIAL_COVERAGE")
        add(errors, any(row.get("scope_state") not in {"DERIVED_INTERNAL", "CONDITIONAL", "UNVERIFIED_EXTERNAL", "GROUND_NOT_FOUND"} for row in material_rows), "MATERIAL_STATE")

    numeric = data.get("numeric_rederivation", {})
    gc = numeric.get("grand_canonical", {})
    add(errors, gc.get("absolute_response_error", math.inf) >= 1.0e-10, "GC_FD")
    add(errors, gc.get("variance_N", 0.0) <= 0.0, "GC_VARIANCE")
    add(errors, "existence is a separate" not in gc.get("strictness_rule", ""), "GC_EXISTENCE")
    regular = numeric.get("regular_solution", {})
    add(errors, regular.get("Omega_over_RT") != 3.0, "REGULAR_OMEGA")
    add(errors, regular.get("center_is_unstable") is not True, "REGULAR_STABILITY")
    add(errors, abs(regular.get("maxwell_integral_J_per_mol", math.inf)) >= 1.0e-8, "REGULAR_MAXWELL")
    add(errors, abs(regular.get("common_tangent_slope_J_per_mol", math.inf)) >= 1.0e-10, "REGULAR_TANGENT")
    add(errors, regular.get("spinodal") == regular.get("binodal"), "REGULAR_COLLAPSE")
    peak = numeric.get("equilibrium_peak", {})
    add(errors, peak.get("absolute_peak_error_C_per_V", math.inf) >= 1.0e-2, "PEAK_FD")
    add(errors, "not a general" not in peak.get("variance_rule", ""), "PEAK_CONVOLUTION")
    tst = numeric.get("transition_state_theory", {})
    add(errors, tst.get("entropy_absolute_error", math.inf) >= 1.0e-6, "TST_ENTROPY_FD")
    add(errors, tst.get("heat_capacity_absolute_error", math.inf) >= 1.0e-6, "TST_CP_FD")
    add(errors, tst.get("rate_roundtrip_relative_error", math.inf) >= 1.0e-12, "TST_ROUNDTRIP")
    add(errors, "DeltaE0_prime" not in tst.get("delta_S_formula", "") or "L_prime" not in tst.get("delta_S_formula", ""), "TST_DERIVATIVES")
    blend = numeric.get("blend_and_capacity_basis", {})
    add(errors, abs(blend.get("charge_balance_residual", math.inf)) >= 1.0e-12, "BLEND_ROOT")
    add(errors, blend.get("absolute_derivative_error", math.inf) >= 1.0e-8, "BLEND_FD")
    add(errors, blend.get("capacity_fraction_si") == blend.get("mass_fraction_si"), "BLEND_BASIS")
    add(errors, "does not imply equal host current" not in blend.get("finite_current_boundary", ""), "BLEND_CURRENT")
    finite = numeric.get("finite_current_mechanics", {})
    add(errors, not math.isclose(finite.get("c_rate_per_second", math.inf), 1.0 / 3600.0, rel_tol=0.0, abs_tol=1.0e-18), "CRATE_CONVERSION")
    add(errors, not math.isclose(finite.get("lag_if_hour_number_used_directly_over_SI_lag", 0.0), 3600.0), "CRATE_LAG")
    add(errors, not math.isclose(finite.get("RT_ln_3600_J_per_mol", 0.0), 20_299.4232, rel_tol=2.0e-6), "CRATE_BARRIER")
    add(errors, "raises" not in finite.get("barrier_direction", ""), "BARRIER_DIRECTION")
    add(errors, "J/mol" not in finite.get("stress_dimension_rule", "") or "V" not in finite.get("stress_dimension_rule", ""), "LARCHE_DIMENSION")
    add(errors, "no closed-cycle hysteresis" not in finite.get("path_rule", ""), "LARCHE_HISTORY")

    routes = data.get("phase057_provisional_routes")
    add(errors, not isinstance(routes, list) or len(routes) != 55, "PHASE057_ROWS")
    if isinstance(routes, list):
        add(errors, len({row.get("numeric_id") for row in routes}) != 55, "PHASE057_IDS")
        add(errors, {row.get("numeric_id") for row in routes} != REQUIRED_PHASE057_NUMERIC_IDS, "PHASE057_ID_SET")
        add(errors, any(row.get("route_state") != "RETAINED_PROVISIONAL_NOT_PROMOTED" for row in routes), "PHASE057_STATE")
        add(errors, any(row.get("external_truth_promoted") is not False for row in routes), "PHASE057_PROMOTION")

    findings = data.get("findings")
    add(errors, not unique_ids(findings, "finding_id"), "FINDING_IDS")
    add(errors, findings != evidence.get("findings"), "FINDING_PARITY")
    if isinstance(findings, list):
        add(errors, len(findings) != 20, "FINDING_ROWS")
        add(errors, {row.get("finding_id") for row in findings} != REQUIRED_FINDING_IDS, "FINDING_ID_SET")
        finding_priorities_valid = all(row.get("priority") in {"P0", "P1", "P2"} for row in findings)
        add(errors, not finding_priorities_valid, "FINDING_PRIORITY")
        add(errors, any(row.get("status") != "OPEN_ROUTED" for row in findings), "FINDING_STATUS")
        add(errors, any(row.get("external_truth_validated") is not False for row in findings), "FINDING_EXTERNAL")
        if finding_priorities_valid:
            observed_summary = dict(sorted(Counter(row["priority"] for row in findings).items()))
            add(
                errors,
                observed_summary != data.get("finding_summary")
                or observed_summary != {"P0": 4, "P1": 8, "P2": 8},
                "FINDING_SUMMARY",
            )

    authority = data.get("authority_boundary", {})
    false_keys = (
        "frozen_source_modified", "production_module_imported_or_executed",
        "external_scientific_truth_validated", "external_material_truth_validated",
        "external_experimental_truth_validated", "primary_literature_truth_validated",
        "canonical_equation_accepted", "final_manuscript_ready",
    )
    add(errors, any(authority.get(key) is not False for key in false_keys), "AUTHORITY_PROMOTION")
    projection = copy.deepcopy(data)
    stored_semantic = projection.pop("semantic_sha256", None)
    add(errors, stored_semantic != digest(compact(projection)), "SEMANTIC_SHA")
    return errors


def run_builder_once(directory: str) -> tuple[dict[str, Any], bytes, int]:
    proc = run([sys.executable, str(BUILDER), "--output-dir", directory])
    if proc.returncode:
        raise ValidationError(
            f"builder failed ({proc.returncode}): "
            f"{proc.stdout.decode('utf-8', errors='replace')} "
            f"{proc.stderr.decode('utf-8', errors='replace')}"
        )
    path = Path(directory) / ARTIFACT.name
    value, nodes = strict_load(path)
    if not isinstance(value, dict):
        raise ValidationError("builder output root")
    return value, path.read_bytes(), nodes


def validate_frozen_identity(data: dict[str, Any]) -> None:
    topology, _ = strict_load(TOPOLOGY)
    by_path = {row["path"]: row for row in topology["sources"]}
    for source in data["source_inventory"]:
        raw = git_bytes("show", f"{BASELINE}:{source['path']}")
        if digest(raw) != source["raw_sha256"]:
            raise ValidationError(f"frozen source raw drift: {source['path']}")
        blob = git_text("rev-parse", f"{BASELINE}:{source['path']}")
        if blob != source["git_blob"] or blob != by_path[source["path"]]["blob_sha1"]:
            raise ValidationError(f"frozen source blob drift: {source['path']}")
        if len(raw.decode("utf-8", "strict").splitlines()) != source["physical_lines"]:
            raise ValidationError(f"frozen source line drift: {source['path']}")
    for equation in data["display_equation_inventory"]:
        raw = git_bytes("show", f"{BASELINE}:{equation['path']}")
        lines = raw.decode("utf-8", "strict").splitlines()
        body = "\n".join(lines[equation["start_line"] - 1:equation["end_line"]]) + "\n"
        if body != equation["body"] or digest(body.encode("utf-8")) != equation["body_sha256"]:
            raise ValidationError(f"equation replay drift: {equation['equation_id']}")


def validate_phase057_identity(data: dict[str, Any]) -> None:
    ledger, _ = strict_load(PHASE057)
    records = {row["numeric_id"]: row for row in ledger["records"]}
    for routed in data["phase057_provisional_routes"]:
        original = records.get(routed["numeric_id"])
        projection = {
            key: value for key, value in routed.items()
            if key not in {"route_state", "external_truth_promoted", "downstream_owner"}
        }
        if original is None or projection != original:
            raise ValidationError(f"Phase057 record identity drift: {routed['numeric_id']}")


def control_document_checks() -> None:
    mapping = {
        "result": RESULT, "active_ledger": ACTIVE_LEDGER,
        "parent_ledger": PARENT_LEDGER, "handover": HANDOVER,
    }
    if any(value == "PENDING" for value in CONTROL_SHA256.values()):
        raise ValidationError("control SHA constants not finalized")
    for key, path in mapping.items():
        actual = digest(normalized_bytes(path))
        if actual != CONTROL_SHA256[key]:
            raise ValidationError(f"control document drift: {key}: {actual}")
    result_text = RESULT.read_text(encoding="utf-8")
    required = (
        "상태: `PASS_WITH_CONCERNS`", f"Precommit Gate: `{GATE}`",
        "Postcommit terminal: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "external scientific/material/experimental truth", "Claude/**",
    )
    if any(token not in result_text for token in required):
        raise ValidationError("result recovery token drift")


def run_negative_probes(data: dict[str, Any]) -> tuple[int, int]:
    probes: list[tuple[str, Any, str]] = []
    def probe(name: str, mutate: Any, expected: str) -> None:
        probes.append((name, mutate, expected))

    probe("gate", lambda d: d.__setitem__("gate", "PASS"), "GATE")
    probe("baseline", lambda d: d.__setitem__("baseline_commit", "0" * 40), "BASELINE")
    probe("source_drop", lambda d: d["source_inventory"].pop(), "SOURCE_ROWS")
    probe("equation_source_blob", lambda d: d["display_equation_inventory"][0].__setitem__("git_blob", "0" * 40), "EQUATION_SOURCE")
    probe("equation_drop", lambda d: d["display_equation_inventory"].pop(), "EQUATION_ROWS")
    probe("equation_duplicate", lambda d: d["display_equation_inventory"][1].__setitem__("equation_id", "P063-EQ-0001"), "EQUATION_IDS")
    probe("equation_interval", lambda d: d["display_equation_inventory"][0].__setitem__("start_line", 0), "EQUATION_INTERVAL")
    probe("equation_body", lambda d: d["display_equation_inventory"][0].__setitem__("body_sha256", "0" * 64), "EQUATION_BODY")
    probe("evidence_sha", lambda d: d["result_first_contract"].__setitem__("evidence_semantic_sha256", "0" * 64), "EVIDENCE_SHA")
    probe("derivation_drop", lambda d: d["manual_rederivation_evidence"]["derivation_rows"].pop(), "DERIVATION_ROWS")
    probe("derivation_id_set", lambda d: d["manual_rederivation_evidence"]["derivation_rows"][0].__setitem__("derivation_id", "P063-DER-999"), "DERIVATION_ID_SET")
    probe("manual_formula_parity", lambda d: d["manual_rederivation_evidence"]["derivation_rows"][0].__setitem__("formula", "false formula"), "EVIDENCE_PARITY")
    probe("manual_anchor_parity", lambda d: d["manual_rederivation_evidence"]["derivation_rows"][0]["source_evidence"][0].__setitem__("line_intervals", [[1, 1]]), "EVIDENCE_PARITY")
    probe("finding_parity", lambda d: d["manual_rederivation_evidence"]["findings"].pop(), "FINDING_PARITY")
    guard_expectations = (
        ("independent_meanfield", "independent_site_not_mean_field"),
        ("spinodal_binodal", "spinodal_not_binodal"),
        ("equilibrium_observation", "equilibrium_not_observation"),
        ("common_potential_equal_current", "common_potential_not_equal_current"),
        ("mass_capacity", "mass_fraction_not_capacity_fraction"),
        ("larche_history", "larche_cahn_reversible_not_hysteresis_closure"),
        ("lco_local_global", "lco_global_offset_not_local_closure"),
        ("c_rate_3600", "c_rate_requires_divide_3600"),
        ("tst_derivative", "tst_temperature_derivatives_retained"),
        ("reversible_hysteretic", "reversible_heat_not_hysteretic_dissipation"),
    )
    for name, key in guard_expectations:
        probe(name, lambda d, k=key: d["manual_rederivation_evidence"]["negative_claim_guards"].__setitem__(k, False), "CLAIM_GUARDS")
    probe("sign", lambda d: d["manual_rederivation_evidence"]["sign_ledger"][0].__setitem__("adjudicated", False), "SIGN_ADJUDICATION")
    probe("operator", lambda d: d["manual_rederivation_evidence"]["operator_ledger"][0].__setitem__("collapsed_with", ["P063-OP-002"]), "OPERATOR_COLLAPSE")
    probe("material", lambda d: d["manual_rederivation_evidence"]["material_scope_ledger"][0].__setitem__("scope_state", "VALIDATED_EXTERNAL"), "MATERIAL_STATE")
    probe("phase057_promote", lambda d: d["phase057_provisional_routes"][0].__setitem__("external_truth_promoted", True), "PHASE057_PROMOTION")
    probe("phase057_id_set", lambda d: d["phase057_provisional_routes"][0].__setitem__("numeric_id", 1), "PHASE057_ID_SET")
    probe(
        "finding_priority",
        lambda d: (
            d["findings"][0].__setitem__("priority", "P3"),
            d["manual_rederivation_evidence"]["findings"][0].__setitem__("priority", "P3"),
        ),
        "FINDING_PRIORITY",
    )
    probe(
        "finding_id_set",
        lambda d: (
            d["findings"][0].__setitem__("finding_id", "P063-S59-F999"),
            d["manual_rederivation_evidence"]["findings"][0].__setitem__("finding_id", "P063-S59-F999"),
        ),
        "FINDING_ID_SET",
    )
    probe(
        "p0_downgrade",
        lambda d: (
            d["findings"][0].__setitem__("priority", "P1"),
            d["manual_rederivation_evidence"]["findings"][0].__setitem__("priority", "P1"),
            d.__setitem__("finding_summary", {"P0": 3, "P1": 9, "P2": 8}),
        ),
        "FINDING_SUMMARY",
    )
    probe(
        "finding_external",
        lambda d: (
            d["findings"][0].__setitem__("external_truth_validated", True),
            d["manual_rederivation_evidence"]["findings"][0].__setitem__("external_truth_validated", True),
        ),
        "FINDING_EXTERNAL",
    )
    probe("external_promote", lambda d: d["authority_boundary"].__setitem__("external_scientific_truth_validated", True), "AUTHORITY_PROMOTION")
    probe("canonical_promote", lambda d: d["authority_boundary"].__setitem__("canonical_equation_accepted", True), "AUTHORITY_PROMOTION")
    probe("gc_variance", lambda d: d["numeric_rederivation"]["grand_canonical"].__setitem__("variance_N", 0.0), "GC_VARIANCE")
    probe("regular_collapse", lambda d: d["numeric_rederivation"]["regular_solution"].__setitem__("binodal", d["numeric_rederivation"]["regular_solution"]["spinodal"]), "REGULAR_COLLAPSE")
    probe("peak_convolution", lambda d: d["numeric_rederivation"]["equilibrium_peak"].__setitem__("variance_rule", "FWHM quadrature always"), "PEAK_CONVOLUTION")
    probe("tst_formula", lambda d: d["numeric_rederivation"]["transition_state_theory"].__setitem__("delta_S_formula", "R L"), "TST_DERIVATIVES")
    probe("blend_current", lambda d: d["numeric_rederivation"]["blend_and_capacity_basis"].__setitem__("finite_current_boundary", "equal host current"), "BLEND_CURRENT")
    probe("crate", lambda d: d["numeric_rederivation"]["finite_current_mechanics"].__setitem__("c_rate_per_second", 1.0), "CRATE_CONVERSION")
    probe("barrier_direction", lambda d: d["numeric_rederivation"]["finite_current_mechanics"].__setitem__("barrier_direction", "lowers"), "BARRIER_DIRECTION")
    probe("larche_dimension", lambda d: d["numeric_rederivation"]["finite_current_mechanics"].__setitem__("stress_dimension_rule", "unknown"), "LARCHE_DIMENSION")
    probe("semantic", lambda d: None, "SEMANTIC_SHA")

    passed = 0
    for name, mutate, expected in probes:
        fixture = copy.deepcopy(data)
        mutate(fixture)
        projection = copy.deepcopy(fixture)
        projection.pop("semantic_sha256", None)
        fixture["semantic_sha256"] = digest(compact(projection))
        if name == "semantic":
            fixture["semantic_sha256"] = "0" * 64
        diagnostics = artifact_diagnostics(
            fixture,
            None if name in {"manual_formula_parity", "manual_anchor_parity"}
            else fixture["manual_rederivation_evidence"],
        )
        if diagnostics != {expected}:
            raise ValidationError(f"negative {name}: expected {[expected]}, got {sorted(diagnostics)}")
        passed += 1
    return passed, len(probes)


def strict_json_negative_probes() -> tuple[int, int]:
    fixtures = ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}', '[1,2,')
    passed = 0
    for fixture in fixtures:
        try:
            strict_load_text(fixture)
        except (ValueError, json.JSONDecodeError):
            passed += 1
        else:
            raise ValidationError(f"strict JSON accepted invalid fixture: {fixture}")
    return passed, len(fixtures)


def verify_branch_guards() -> None:
    errors = []
    if ref_hash(f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("protected local")
    if ref_hash(f"refs/remotes/origin/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("protected tracking")
    if remote_head(PROTECTED_BRANCH) != PROTECTED_TIP:
        errors.append("protected live")
    if ref_hash("refs/heads/main") is not None:
        errors.append("unexpected local main")
    if ref_hash("refs/remotes/origin/main") != MAIN_TIP or remote_head("main") != MAIN_TIP:
        errors.append("main drift")
    if git_paths("diff", "--name-only", "-z", BASELINE, "HEAD", "--", "Claude"):
        errors.append("Claude committed diff")
    if git_paths("diff", "--name-only", "-z", "--", "Claude"):
        errors.append("Claude worktree diff")
    if git_paths("diff", "--cached", "--name-only", "-z", "--", "Claude"):
        errors.append("Claude staged diff")
    if errors:
        raise ValidationError("branch guard drift: " + ", ".join(errors))


def verify_staged() -> str:
    if git_text("branch", "--show-current") != BRANCH:
        raise ValidationError("wrong branch")
    if git_text("rev-parse", "HEAD") != EXPECTED_PARENT:
        raise ValidationError("wrong precommit parent")
    if git_text("rev-parse", "@{upstream}") != EXPECTED_PARENT or remote_head(BRANCH) != EXPECTED_PARENT:
        raise ValidationError("upstream/live not at parent")
    staged = git_paths("diff", "--cached", "--name-only", "-z", "HEAD")
    if staged != EXACT_SEVEN_SET:
        raise ValidationError(f"staged path mismatch: {sorted(staged ^ EXACT_SEVEN_SET)}")
    unstaged = git_paths("diff", "--name-only", "-z")
    untracked = git_paths("ls-files", "--others", "--exclude-standard", "-z")
    if unstaged or untracked:
        raise ValidationError(f"unstaged/untracked paths remain: {sorted(unstaged | untracked)}")
    for path in EXACT_SEVEN:
        if git_bytes("show", f":{path}") != (REPO / path).read_bytes():
            raise ValidationError(f"staged/worktree byte mismatch: {path}")
    worktree_check = run(["git", "diff", "--check"])
    cached_check = run(["git", "diff", "--cached", "--check"])
    if worktree_check.returncode or cached_check.returncode:
        detail = (worktree_check.stdout + worktree_check.stderr + cached_check.stdout + cached_check.stderr).decode(
            "utf-8", errors="replace"
        ).strip()
        raise ValidationError(f"staged whitespace check failed: {detail}")
    verify_branch_guards()
    return EXPECTED_PARENT


def verify_persistence(expected_commit: str | None) -> str:
    if not expected_commit or len(expected_commit) != 40:
        raise ValidationError("--expected-commit full hash required")
    if git_text("branch", "--show-current") != BRANCH:
        raise ValidationError("wrong branch")
    head = git_text("rev-parse", "HEAD")
    if head != expected_commit or git_text("rev-parse", "HEAD^") != EXPECTED_PARENT:
        raise ValidationError("local HEAD/parent mismatch")
    if git_text("show", "-s", "--format=%s", "HEAD") != SUBJECT:
        raise ValidationError("commit subject mismatch")
    if git_text("rev-parse", "@{upstream}") != head or remote_head(BRANCH) != head:
        raise ValidationError("upstream/live mismatch")
    changed = git_paths("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD")
    if changed != EXACT_SEVEN_SET:
        raise ValidationError(f"commit path mismatch: {sorted(changed ^ EXACT_SEVEN_SET)}")
    if git_paths("status", "--porcelain=v1", "-z") or git_paths("diff", "--cached", "--name-only", "-z"):
        raise ValidationError("worktree/index not clean")
    commit_check = run(["git", "diff", "--check", "HEAD^", "HEAD"])
    if commit_check.returncode:
        detail = (commit_check.stdout + commit_check.stderr).decode("utf-8", errors="replace").strip()
        raise ValidationError(f"commit whitespace check failed: {detail}")
    verify_branch_guards()
    return head


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if sum((args.content_only, args.verify_staged, args.verify_persistence)) != 1:
        print("select exactly one primary mode", file=sys.stderr)
        return 2
    try:
        if not ARTIFACT.is_file():
            raise ValidationError(f"E_ARTIFACT_MISSING: {ARTIFACT.relative_to(REPO).as_posix()}")
        data, nodes = strict_load(ARTIFACT)
        if not isinstance(data, dict):
            raise ValidationError("artifact root not object")
        diagnostics = artifact_diagnostics(data)
        if diagnostics:
            raise ValidationError("artifact diagnostics: " + ", ".join(sorted(diagnostics)))
        validate_frozen_identity(data)
        validate_phase057_identity(data)
        control_document_checks()
        mandatory_terminal_controls = args.verify_staged or args.verify_persistence
        run_negative = args.run_negative_probes or mandatory_terminal_controls
        run_determinism = args.determinism_check or mandatory_terminal_controls
        negative = run_negative_probes(data) if run_negative else (0, 0)
        strict_negative = strict_json_negative_probes() if run_negative else (0, 0)
        determinism = (0, 0)
        if run_determinism:
            with tempfile.TemporaryDirectory(prefix="p063-step59-a-") as first, tempfile.TemporaryDirectory(prefix="p063-step59-b-") as second:
                first_data, first_raw, _ = run_builder_once(first)
                second_data, second_raw, _ = run_builder_once(second)
                if first_raw != second_raw or first_raw != ARTIFACT.read_bytes() or first_data != data or second_data != data:
                    raise ValidationError("builder determinism drift")
                determinism = (2, 2)
        suffix = (
            f"negative={negative[0]}/{negative[1]} strict={strict_negative[0]}/{strict_negative[1]} "
            f"determinism={determinism[0]}/{determinism[1]} nodes={nodes}"
        )
        if args.verify_staged:
            print(f"PASS_P063_STEP59_STAGED parent={verify_staged()} paths=7/7 {suffix}")
        elif args.verify_persistence:
            print(f"PASS_P063_STEP59_PERSISTENCE head={verify_persistence(args.expected_commit)} paths=7/7 {suffix}")
        else:
            print(f"PASS_P063_STEP59_CONTENT sources=53 equations=231 {suffix}")
        return 0
    except (OSError, UnicodeError, ValueError, ValidationError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL_P063_STEP59: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
