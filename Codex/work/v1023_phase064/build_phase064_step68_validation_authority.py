#!/usr/bin/env python3
"""Build Phase 064 Step 68 validation-authority evidence.

This builder reads frozen Git objects and already committed Codex evidence.  It
does not import or execute production code.  Human result/control documents
must exist first; the authority matrix is the sole JSON output and is written
last with an atomic replace.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import tempfile
from typing import Any, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "4dec72387220e7210fc15d0323ca481a172111fd"
EXPECTED_SUBJECT = "audit(phase064): adjudicate v1023 validation authority"
GATE = "PASS_P064_STEP68_AUTHORITY"
PERSISTENCE = "PASS_P064_STEP68_PERSISTENCE"
CEILING = "CONDITIONAL_P064"
OUT = ROOT / "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json"
RESULT = ROOT / "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md"
PARENT_LEDGER = ROOT / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EVIDENCE_BEGIN = "<!-- P064_STEP68_HUMAN_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P064_STEP68_HUMAN_EVIDENCE_END -->"

AXES = (
    "synthetic_numerical",
    "implementation_regression",
    "picard_iteration_behavior",
    "transfer_identity",
    "material_validation",
    "experimental_validation",
    "external_primary_literature_validation",
)

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md": {
        "commit": EXPECTED_PARENT, "lines": 179, "spans": [[1, 28], [155, 179]],
    },
    "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md": {
        "commit": EXPECTED_PARENT, "lines": 272, "spans": [[230, 272]],
    },
    "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md": {
        "commit": EXPECTED_PARENT, "lines": 254, "spans": [[5, 28], [210, 254]],
    },
    "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md": {
        "commit": EXPECTED_PARENT, "lines": 308, "spans": [[217, 264], [296, 308]],
    },
    "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md": {
        "commit": EXPECTED_PARENT, "lines": 238, "spans": [[118, 180], [190, 238]],
    },
    "Claude/docs/v1.0.23/test_gates_v1023.py": {
        "lines": 626, "spans": [[162, 188], [196, 325], [336, 385], [389, 431],
                                   [439, 482], [485, 526], [529, 565], [568, 622]],
    },
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": {
        "lines": 128, "spans": [[26, 37], [39, 58], [60, 88], [90, 105], [107, 128]],
    },
    "Claude/docs/v1.0.23/results/PHASE_P1_RESULT.md": {
        "lines": 112, "spans": [[63, 85], [87, 95]],
    },
    "Claude/docs/v1.0.23/results/PHASE_P2_RESULT.md": {
        "lines": 114, "spans": [[76, 93]],
    },
    "Claude/docs/v1.0.23/results/PHASE_P3_RESULT.md": {
        "lines": 102, "spans": [[51, 81]],
    },
    "Claude/docs/v1.0.23/results/PHASE_P5_RESULT.md": {
        "lines": 95, "spans": [[43, 76], [85, 91]],
    },
    "Claude/docs/v1.0.23/results/comp_v23/AUD_REPORT_v23.md": {
        "lines": 65, "spans": [[1, 13], [20, 40], [52, 65]],
    },
    "Claude/docs/v1.0.23/results/MERGE_READINESS_v23.md": {
        "lines": 52, "spans": [[1, 13], [31, 52]],
    },
    "Claude/docs/v1.0.23/results/qa_images/CURVE_QA_v23.md": {
        "lines": 38, "spans": [[1, 20], [22, 38]],
    },
    "Claude/docs/v1.0.23/results/V1023_EXECUTION_LEDGER.md": {
        "lines": 12, "spans": [[1, 12]],
    },
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": {
        "lines": 68, "spans": [[1, 18], [45, 68]],
    },
    "Claude/docs/v1.0.23/results/tools_check_structure.py": {
        "lines": 170, "spans": [[95, 121], [154, 170]],
    },
    "Claude/docs/v1.0.23/results/qa_images/curve_qa.py": {
        "lines": 156, "spans": [[18, 30], [50, 106], [109, 156]],
    },
}

PRIOR_INPUTS = (
    "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json",
    "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json",
    "Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json",
    "Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json",
    "Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json",
    "Codex/results/PHASE_064_V1023_READ_ATTESTATION.json",
)


class BuildError(RuntimeError):
    pass


def run(args: Iterable[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(list(args), cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=180, check=False)
    if check and cp.returncode:
        raise BuildError(f"command failed {list(args)!r}: {cp.stderr.decode('utf-8', 'replace')}")
    return cp


def git_bytes(commit: str, path: str) -> bytes:
    return run(("git", "show", f"{commit}:{path}")).stdout


def git_text(*args: str) -> str:
    return run(("git", *args)).stdout.decode("utf-8", "strict").strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def strict_json_bytes(raw: bytes, source: str) -> Any:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise BuildError(f"strict JSON UTF-8 failure: {source}") from exc

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                raise BuildError(f"strict JSON duplicate key: {source}:{key}")
            out[key] = value
        return out

    def constant(value: str) -> Any:
        raise BuildError(f"strict JSON non-finite constant: {source}:{value}")

    def bounded_int(value: str) -> int:
        if len(value.lstrip("+-")) > 128:
            raise BuildError(f"strict JSON huge integer: {source}")
        return int(value)

    def bounded_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            raise BuildError(f"strict JSON numeric overflow: {source}")
        return parsed

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant,
                          parse_int=bounded_int, parse_float=bounded_float)
    except BuildError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise BuildError(f"strict JSON parse failure: {source}") from exc


def json_type_projection(value: Any) -> Any:
    if value is None:
        return "null"
    if type(value) is bool:
        return "bool"
    if type(value) is int:
        return "int"
    if type(value) is float:
        return "float"
    if type(value) is str:
        return "str"
    if type(value) is list:
        return [json_type_projection(item) for item in value]
    if type(value) is dict:
        return {key: json_type_projection(value[key]) for key in sorted(value)}
    raise BuildError(f"unsupported JSON type: {type(value)!r}")


def finalize(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("semantic_sha256", None)
    value.pop("json_type_projection_sha256", None)
    value["json_type_projection_sha256"] = sha256(compact_bytes(json_type_projection(value)))
    value["semantic_sha256"] = sha256(compact_bytes(value))
    return value


def atomic_write(path: pathlib.Path, raw: bytes) -> None:
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=path.parent, prefix=f".{path.name}.",
                                         suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def line_span(raw: bytes, start: int, end: int) -> dict[str, Any]:
    lines = raw.decode("utf-8", "strict").splitlines(keepends=True)
    if not (1 <= start <= end <= len(lines)):
        raise BuildError(f"invalid source span {start}-{end}/{len(lines)}")
    selected = "".join(lines[start - 1:end]).encode("utf-8")
    return {"start": start, "end": end, "sha256": sha256(selected)}


def axes(*supported: str, external: str = "NOT_ESTABLISHED") -> dict[str, str]:
    unknown = set(supported) - set(AXES[:4])
    if unknown:
        raise BuildError(f"unknown supported axes: {sorted(unknown)}")
    result = {key: "NOT_EVALUATED" for key in AXES}
    for key in supported:
        result[key] = "ESTABLISHED_BOUNDED_INTERNAL"
    result["material_validation"] = "NOT_ESTABLISHED"
    result["experimental_validation"] = "NOT_ESTABLISHED"
    result["external_primary_literature_validation"] = external
    return result


def row(identifier: str, kind: str, path: str, start: int, end: int, label: str,
        verdict: str, evidence_class: str, supported: tuple[str, ...] = (),
        *, depends_on: tuple[str, ...] = (), max_authority: str = "INTERNAL_ONLY",
        external: str = "NOT_ESTABLISHED", limitation: str,
        commit: str = BASELINE) -> dict[str, Any]:
    raw = git_bytes(commit, path)
    return {
        "id": identifier,
        "record_kind": kind,
        "source": {"path": path, "commit": commit, **line_span(raw, start, end)},
        "label": label,
        "verdict": verdict,
        "evidence_class": evidence_class,
        "axes": axes(*supported, external=external),
        "depends_on": list(depends_on),
        "max_authority": max_authority,
        "limitation": limitation,
        "counts_once_in_gate_denominator": True,
    }


def canonical_rows() -> list[dict[str, Any]]:
    main = "Claude/docs/v1.0.23/test_gates_v1023.py"
    selfc = "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py"
    p1 = "Claude/docs/v1.0.23/results/PHASE_P1_RESULT.md"
    p2 = "Claude/docs/v1.0.23/results/PHASE_P2_RESULT.md"
    p3 = "Claude/docs/v1.0.23/results/PHASE_P3_RESULT.md"
    p5 = "Claude/docs/v1.0.23/results/PHASE_P5_RESULT.md"
    rows = [
        row("EXE-G1", "EXECUTABLE_HARD", main, 162, 188, "G1 backward/golden equality", "PASS_STORED_AND_REPLAYED", "SYNTHETIC_REGRESSION", ("synthetic_numerical", "implementation_regression"), limitation="Frozen synthetic/default-path equality; not a material or experimental validation."),
        row("EXE-G2", "EXECUTABLE_HARD", main, 196, 325, "G2 analytic/reference/finite-difference round trip", "PASS_STORED_AND_REPLAYED", "SYNTHETIC_NUMERICAL_REGRESSION", ("synthetic_numerical", "implementation_regression"), limitation="Internal constructed values and numerical identities only."),
        row("EXE-G3", "EXECUTABLE_HARD", main, 336, 385, "G3 theta_E absent bit-exact and liveness", "PASS_STORED_AND_REPLAYED", "IMPLEMENTATION_REGRESSION", ("implementation_regression",), limitation="Source-mutated implementation comparison; no physical truth authority."),
        row("EXE-NT", "EXECUTABLE_HARD", main, 389, 431, "n(T) absent/zero/analytic propagation", "PASS_STORED_AND_REPLAYED", "SYNTHETIC_NUMERICAL_REGRESSION", ("synthetic_numerical", "implementation_regression"), limitation="Analytic/finite-difference implementation behavior on constructed transitions."),
        row("EXE-R6-G1", "EXECUTABLE_HARD", main, 439, 482, "blend fSi=0 bit-exact and liveness", "PASS_STORED_AND_REPLAYED", "IMPLEMENTATION_REGRESSION", ("implementation_regression",), limitation="Algebraic blend implementation behavior; not a material validation."),
        row("EXE-R6-G2", "EXECUTABLE_HARD", main, 485, 526, "synthetic wt-percent sweep continuity", "PASS_STORED_AND_REPLAYED", "SYNTHETIC_NUMERICAL", ("synthetic_numerical",), limitation="Constructed sweep continuity does not validate a real blend or protocol."),
        row("EXE-R6-G3", "EXECUTABLE_HARD", main, 529, 565, "numerical blend capacity integration identity", "PASS_STORED_AND_REPLAYED", "SYNTHETIC_NUMERICAL", ("synthetic_numerical",), limitation="Internal numerical identity; mixed capacity-basis and current-allocation debts remain outside this gate."),
        row("EXE-R6-COV", "EXECUTABLE_HARD", main, 568, 622, "Si case coverage and explicit unsupported boundaries", "PASS_STORED_AND_REPLAYED", "IMPLEMENTATION_BOUNDARY", ("implementation_regression",), limitation="Finite execution/warning/NotImplemented behavior only."),
        row("EXE-GE1", "EXECUTABLE_HARD", selfc, 26, 37, "frozen recovery g_eff=0", "PASS_STORED_AND_REPLAYED", "SYNTHETIC_PICARD_BOUNDARY", ("synthetic_numerical", "picard_iteration_behavior"), limitation="Zero-feedback identity on one constructed grid."),
        row("EXE-GE2", "EXECUTABLE_HARD", selfc, 39, 58, "dqdv bit-exact g_eff=0", "PASS_STORED_AND_REPLAYED", "IMPLEMENTATION_REGRESSION", ("implementation_regression",), limitation="Default-off/zero-feedback implementation equality only."),
        row("EXE-GE3", "EXECUTABLE_HARD", selfc, 60, 88, "self-referential Picard improvement", "PASS_STORED_AND_REPLAYED_WITH_BOUNDARY", "SYNTHETIC_PICARD", ("synthetic_numerical", "picard_iteration_behavior"), limitation="Code-defined fixed point and selected g values; not a proof of general convergence or exact physical closure."),
        row("EXE-GE4", "EXECUTABLE_HARD", selfc, 90, 105, "voltage-coordinate transfer identity", "PASS_STORED_AND_REPLAYED_WITH_BOUNDARY", "SYNTHETIC_TRANSFER", ("synthetic_numerical", "transfer_identity"), limitation="Uniform-grid voltage-coordinate comparison; implementation is unpadded circular DFT and does not establish time/EIS/instrument response."),
        row("EXE-GE5", "EXECUTABLE_HARD", selfc, 107, 128, "ratio option liveness", "PASS_STORED_AND_REPLAYED", "IMPLEMENTATION_LIVENESS", ("implementation_regression",), limitation="Selected resolved dimensionless regime only; physical C-rate label is not accepted."),
        row("DECL-P1-A", "PHASE_GATE_DECLARATION", p1, 80, 80, "P1 frozen-limit recovery", "CONDITIONAL_PASS_STORED", "ANALYTIC_SYNTHETIC", ("synthetic_numerical", "picard_iteration_behavior"), limitation="Internal identity; the cited second scratchpad implementation is not present in the frozen tree."),
        row("DECL-P1-B", "PHASE_GATE_DECLARATION", p1, 81, 81, "P1 applicability inequalities vs JCP conditions", "CONDITIONAL_PASS_REBOUNDED", "PRIMARY_METHOD_CONTEXT", (), max_authority="BOUNDED_PRIMARY_METHOD_CONTEXT_ONLY", external="ESTABLISHED_BOUNDED_JCP147_REF6_METHOD_ONLY", limitation="JCP147 and Ref6 source problems are grounded; graphite applicability and Ref7 method content are not established."),
        row("DECL-P1-C", "PHASE_GATE_DECLARATION", p1, 82, 82, "P1 master rederivation", "CONDITIONAL_PASS_REBOUNDED", "INTERNAL_DERIVATION_AND_OBSERVATION", ("synthetic_numerical", "picard_iteration_behavior"), limitation="First-iterate/order observations are internal and do not establish general convergence or material truth."),
        row("DECL-P2-01", "PHASE_GATE_DECLARATION", p2, 80, 80, "P2 chapter build", "PASS_STORED_PROCESS", "DOCUMENT_BUILD", (), limitation="Build success is document-process evidence only."),
        row("DECL-P2-02", "PHASE_GATE_DECLARATION", p2, 81, 81, "P2 boxed structure intact", "PASS_STORED_PROCESS", "DOCUMENT_STRUCTURE", (), limitation="TeX structure only."),
        row("DECL-P2-03", "PHASE_GATE_DECLARATION", p2, 82, 82, "P2 structural regression", "PASS_STORED_PROCESS", "DOCUMENT_STRUCTURE", (), limitation="Baseline-relative document structure only."),
        row("DECL-P2-04", "PHASE_GATE_DECLARATION", p2, 83, 83, "P2 body code-mention exclusion", "PASS_STORED_PROCESS", "DOCUMENT_SCOPE", (), limitation="Authorship/scope rule only."),
        row("DECL-P2-05", "PHASE_GATE_DECLARATION", p2, 84, 84, "P2 five-item subsection", "PASS_STORED_PROCESS", "DOCUMENT_CONTENT_INVENTORY", (), limitation="Presence of required headings does not validate their scientific truth."),
        row("DECL-P2-06", "PHASE_GATE_DECLARATION", p2, 85, 85, "P2 ordering convention", "PASS_STORED_PROCESS", "DOCUMENT_ORDERING", (), limitation="Pedagogical ordering only."),
        row("DECL-P2-07", "PHASE_GATE_DECLARATION", p2, 86, 86, "P2 non-applicable classes warning", "PASS_STORED_PROCESS", "DOCUMENT_SCOPE", (), limitation="Correct scope warning; no solver or physical validation is created."),
        row("DECL-P2-08", "PHASE_GATE_DECLARATION", p2, 87, 87, "P2 equation-code conformance reservation", "RESERVED_FOR_P3", "PROCESS_RESERVATION", (), limitation="Explicitly not passed in P2; later P3 declaration is separate evidence."),
        row("DECL-P3-01", "PHASE_GATE_DECLARATION", p3, 70, 70, "P3 legacy suite exit", "PASS_STORED_AGGREGATE", "AGGREGATE_REPLAY", ("synthetic_numerical", "implementation_regression"), depends_on=("EXE-G1", "EXE-G2", "EXE-G3", "EXE-NT", "EXE-R6-G1", "EXE-R6-G2", "EXE-R6-G3", "EXE-R6-COV"), limitation="Aggregate reference to eight executable gates; not an independent replication."),
        row("DECL-P3-02", "PHASE_GATE_DECLARATION", p3, 71, 71, "P3 frozen-off bit-exact", "PASS_STORED_AGGREGATE", "AGGREGATE_REGRESSION", ("implementation_regression",), depends_on=("EXE-G1", "EXE-GE2"), limitation="Aggregates two equality checks; not material validation."),
        row("DECL-P3-03", "PHASE_GATE_DECLARATION", p3, 72, 72, "P3 new-option convergence", "PASS_STORED_REBOUNDED", "AGGREGATE_PICARD", ("synthetic_numerical", "picard_iteration_behavior"), depends_on=("EXE-GE3",), limitation="Selected code-defined fixed-point improvement only; general convergence wording is rejected."),
        row("DECL-P3-04", "PHASE_GATE_DECLARATION", p3, 73, 73, "P3 transfer conformance", "PASS_STORED_REBOUNDED", "AGGREGATE_TRANSFER", ("synthetic_numerical", "transfer_identity"), depends_on=("EXE-GE4",), limitation="Voltage-coordinate uniform-grid identity only."),
        row("DECL-P3-05", "PHASE_GATE_DECLARATION", p3, 74, 74, "P3 option liveness", "PASS_STORED_AGGREGATE", "AGGREGATE_LIVENESS", ("implementation_regression",), depends_on=("EXE-GE5",), limitation="Selected numerical regime only."),
        row("DECL-P3-06", "PHASE_GATE_DECLARATION", p3, 75, 75, "P3 equation-code map", "PASS_STORED_STATIC", "STATIC_CODE_DOCUMENT_CONFORMANCE", ("implementation_regression",), limitation="Static symbol/equation mapping; not a behavioral or physical proof."),
        row("DECL-P4-SKIP", "PHASE_GATE_DECLARATION", p5, 74, 76, "P4 Fisher information geometry", "INTENTIONALLY_SKIPPED_NOT_EXECUTED", "PROCESS_DECISION", (), max_authority="PROCESS_ONLY", limitation="A deliberate decision state, neither PASS nor FAIL and not scientific evidence."),
        row("DECL-P5-01", "PHASE_GATE_DECLARATION", p5, 67, 67, "P5 zero critical findings", "PASS_STORED_ADVERSARIAL", "ADVERSARIAL_REVIEW", (), limitation="Review severity disposition only; the broad physical-all-consistent wording exceeds this authority."),
        row("DECL-P5-02", "PHASE_GATE_DECLARATION", p5, 68, 68, "P5 three-document build", "PASS_STORED_PROCESS", "DOCUMENT_BUILD", (), limitation="Stored document build evidence only."),
        row("DECL-P5-03", "PHASE_GATE_DECLARATION", p5, 69, 69, "P5 executable-suite replay", "PASS_STORED_AGGREGATE", "AGGREGATE_REPLAY", ("synthetic_numerical", "implementation_regression", "picard_iteration_behavior", "transfer_identity"), depends_on=tuple(["EXE-G1", "EXE-G2", "EXE-G3", "EXE-NT", "EXE-R6-G1", "EXE-R6-G2", "EXE-R6-G3", "EXE-R6-COV", "EXE-GE1", "EXE-GE2", "EXE-GE3", "EXE-GE4", "EXE-GE5"]), limitation="Aggregate of the thirteen executable gates; it creates no new scientific authority."),
        row("DECL-P5-04", "PHASE_GATE_DECLARATION", p5, 70, 70, "P5 code-document conformance", "PASS_STORED_ADVERSARIAL", "STATIC_AND_SELECTED_SYNTHETIC_REVIEW", ("implementation_regression",), limitation="Static mapping and selected internal recomputations only."),
        row("DECL-P5-05", "PHASE_GATE_DECLARATION", p5, 71, 71, "P5 Appendix E integrity after correction", "PASS_STORED_PROCESS", "DOCUMENT_CORRECTION", (), limitation="Correction/build integrity only."),
        row("DECL-P5-06", "PHASE_GATE_DECLARATION", p5, 72, 72, "P5 body code-mention exclusion", "PASS_STORED_PROCESS", "DOCUMENT_SCOPE", (), limitation="Authorship/scope rule only."),
    ]
    rows.extend([
        row("CUR-P064-ACT", "CURRENT_PHASE_GATE", "Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md", 155, 179, "Phase 064 plan activation", "PASS_P064_PLAN_ACTIVATION", "PROCESS_ACTIVATION", (), max_authority="PROCESS_ONLY", limitation="Plan/recovery activation only; none of the seven scientific axes is tested.", commit=EXPECTED_PARENT),
        row("CUR-P064-S64", "CURRENT_PHASE_GATE", "Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md", 230, 247, "Step 64 source/process topology", "PASS_P064_STEP64_SOURCE_PROCESS", "SOURCE_INVENTORY_READ", (), max_authority="INVENTORY_ONLY", limitation="Inventory, identity and read completeness only.", commit=EXPECTED_PARENT),
        row("CUR-P064-S65", "CURRENT_PHASE_GATE", "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md", 238, 254, "Step 65 primary literature authority", "PASS_P064_STEP65_LITERATURE_BOUNDED_GNF", "PRIMARY_LITERATURE_BOUNDARY", (), max_authority="JCP147_REF6_SOURCE_PROBLEMS_ONLY", external="ESTABLISHED_BOUNDED_JCP147_REF6_METHOD_ONLY", limitation="Ref7 method content remains GROUND_NOT_FOUND and graphite applicability is not established.", commit=EXPECTED_PARENT),
        row("CUR-P064-S66", "CURRENT_PHASE_GATE", "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md", 296, 308, "Step 66 ratio/transfer rederivation", "PASS_P064_STEP66_REDERIVATION", "INTERNAL_REDERIVATION", ("synthetic_numerical", "picard_iteration_behavior", "transfer_identity"), limitation="Reduced hypothesis, first Picard and voltage-coordinate transfer only.", commit=EXPECTED_PARENT),
        row("CUR-P064-S67", "CURRENT_PHASE_GATE", "Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md", 190, 238, "Step 67 problem/runtime boundary", "PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS", "INTERNAL_STATIC_RUNTIME", ("synthetic_numerical", "implementation_regression", "picard_iteration_behavior", "transfer_identity"), limitation="Frozen inputs and runtimes only; open P0/P1/P2 findings remain routed.", commit=EXPECTED_PARENT),
        row("HIST-P0-BASELINE", "HISTORICAL_PHASE_GATE", "Claude/docs/v1.0.23/results/V1023_EXECUTION_LEDGER.md", 8, 8, "P0 cloned baseline", "PASS_P0", "BUILD_AND_REGRESSION", ("synthetic_numerical", "implementation_regression"), limitation="Baseline reproduction only; inherited factor-3600 defect was not detected."),
        row("DECL-P1-STOP", "PHASE_GATE_DECLARATION", p1, 83, 83, "P1 stop condition", "NOT_TRIGGERED", "PROCESS_STOP_CONDITION", (), max_authority="PROCESS_ONLY", limitation="A workflow branch state, not scientific evidence."),
        row("STATIC-STRUCTURE", "STATIC_TOOL", "Claude/docs/v1.0.23/results/tools_check_structure.py", 95, 121, "structure checker terminal", "FAIL_WITH_BASELINE_EXCEPTION", "STATIC_TOOL_TERMINAL", (), max_authority="STATIC_PROCESS_ONLY", limitation="The tool terminal is FAIL because of 19 unresolved xr references; P2 separately interprets unchanged baseline as no regression."),
        row("OBS-CURVE-QA", "NON_ENFORCING_OBSERVATION", "Claude/docs/v1.0.23/results/qa_images/curve_qa.py", 50, 106, "curve QA printed pass", "PRINTED_PASS_NON_ENFORCING", "SYNTHETIC_VISUAL_OBSERVATION", ("synthetic_numerical", "implementation_regression"), limitation="No nonzero failure exit, hard-coded path, limited panels; not global C2, material or experimental proof."),
        row("OBS-P1-RATIO", "NON_ENFORCING_OBSERVATION", "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py", 36, 68, "P1 ratio order observation", "UTF8_EXIT0_NON_ENFORCING", "SYNTHETIC_OBSERVATION", ("synthetic_numerical", "picard_iteration_behavior"), limitation="No assertions or scientific failure exit; CP949 fails after calculation and cond_audit_verify.py is absent."),
    ])
    if len(rows) != 47 or len({r["id"] for r in rows}) != 47:
        raise BuildError("complete authority denominator must be exactly 47 unique records")
    return rows


def source_contracts() -> list[dict[str, Any]]:
    contracts = []
    for path, spec in SOURCE_SPECS.items():
        commit = spec.get("commit", BASELINE)
        raw = git_bytes(commit, path)
        lines = raw.decode("utf-8", "strict").splitlines()
        if len(lines) != spec["lines"]:
            raise BuildError(f"line-count drift: {path}")
        contracts.append({
            "path": path,
            "commit": commit,
            "git_blob": git_text("rev-parse", f"{commit}:{path}"),
            "sha256": sha256(raw),
            "bytes": len(raw),
            "lines": len(lines),
            "read_coverage": [1, len(lines)],
            "read_status": "READ_FULL_STEP68",
            "source_spans": [line_span(raw, a, b) for a, b in spec["spans"]],
        })
    return contracts


def prior_inputs() -> list[dict[str, Any]]:
    rows = []
    for path in PRIOR_INPUTS:
        raw = git_bytes(EXPECTED_PARENT, path)
        parsed = strict_json_bytes(raw, path)
        if type(parsed) is not dict:
            raise BuildError(f"strict JSON root is not an object: {path}")
        rows.append({
            "path": path,
            "git_blob": git_text("rev-parse", f"{EXPECTED_PARENT}:{path}"),
            "sha256": sha256(raw),
            "bytes": len(raw),
            "semantic_sha256": parsed.get("semantic_sha256"),
        })
    return rows


def high_risk_bindings() -> dict[str, Any]:
    payloads: dict[str, dict[str, Any]] = {}
    for path in PRIOR_INPUTS:
        parsed = strict_json_bytes(git_bytes(EXPECTED_PARENT, path), path)
        if type(parsed) is not dict:
            raise BuildError(f"strict JSON root is not an object: {path}")
        payloads[path] = parsed
    literature = payloads[PRIOR_INPUTS[0]]
    ratio = payloads[PRIOR_INPUTS[1]]
    problem = payloads[PRIOR_INPUTS[2]]
    topology = payloads[PRIOR_INPUTS[4]]
    read_attestation = payloads[PRIOR_INPUTS[5]]
    equation_rows = {str(row.get("equation")): row for row in literature.get("equation_chain", [])}
    required_equations = ("32", "33", "34", "37", "39")
    if set(required_equations) - set(equation_rows):
        raise BuildError("required Step 65 equation anchor missing")
    topology_sources = topology.get("sources")
    if type(topology_sources) is not list or len(topology_sources) != 83:
        raise BuildError("Step 64 topology source denominator mismatch")
    read_sources = read_attestation.get("sources")
    if type(read_sources) is not list or len(read_sources) != 83:
        raise BuildError("Step 64 read-attestation source denominator mismatch")
    manifest_path_projection = [{"occurrence_id": row.get("occurrence_id"), "manifest_index": row.get("manifest_index"), "path": row.get("path")} for row in topology_sources]
    manifest_blob_projection = [{"occurrence_id": row.get("occurrence_id"), "blob_sha1": row.get("blob_sha1"), "sha256_raw": row.get("sha256_raw")} for row in topology_sources]
    manifest_extent_projection = [{"occurrence_id": row.get("occurrence_id"), "size_bytes": row.get("size_bytes"), "extent": row.get("extent")} for row in topology_sources]
    pdf_page_projection = [{"occurrence_id": row.get("occurrence_id"), "path": row.get("path"), "extent": row.get("extent"), "page_text_records": row.get("page_text_records")} for row in topology_sources if row.get("review_mode") == "FULL_PDF"]
    text_line_projection = [{"occurrence_id": row.get("occurrence_id"), "path": row.get("path"), "extent": row.get("extent"), "physical_lines": row.get("physical_lines")} for row in topology_sources if row.get("review_mode") == "FULL_TEXT"]
    if len(pdf_page_projection) != 3 or sum(row["extent"].get("pages", 0) for row in pdf_page_projection) != 129 or len(text_line_projection) != 78:
        raise BuildError("Step 64 page/line projection denominator mismatch")
    return {
        "step64_manifest_header_sha256": sha256(compact_bytes(topology.get("manifest"))),
        "step64_manifest_path_projection_sha256": sha256(compact_bytes(manifest_path_projection)),
        "step64_manifest_blob_projection_sha256": sha256(compact_bytes(manifest_blob_projection)),
        "step64_manifest_extent_projection_sha256": sha256(compact_bytes(manifest_extent_projection)),
        "step64_pdf_page_projection_sha256": sha256(compact_bytes(pdf_page_projection)),
        "step64_text_line_projection_sha256": sha256(compact_bytes(text_line_projection)),
        "step64_read_attestation_sources_sha256": sha256(compact_bytes(read_sources)),
        "step65_equation_row_sha256": {
            equation: sha256(compact_bytes(equation_rows[equation]))
            for equation in required_equations
        },
        "step65_applicability_sha256": sha256(compact_bytes(literature.get("applicability"))),
        "step66_timebase_sha256": sha256(compact_bytes(ratio.get("timebase"))),
        "step66_benchmark_sha256": sha256(compact_bytes(ratio.get("deterministic_benchmark"))),
        "step67_problem_classes_sha256": sha256(compact_bytes(problem.get("problem_classes"))),
        "step67_non_double_count_sha256": sha256(compact_bytes(problem.get("non_double_count"))),
    }


def supplemental_evidence() -> list[dict[str, Any]]:
    return [
        {"id": "SUP-P1-OBS", "kind": "NONASSERTING_OBSERVATION", "source": {"path": "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py", "start": 45, "end": 68}, "axes": axes("synthetic_numerical", "picard_iteration_behavior"), "fresh_status": "REPLAYED_STEP67_EXIT_ZERO_BUT_ZERO_HARD_ASSERTIONS", "limitation": "Printed order observations are not a hard gate."},
        {"id": "SUP-CURVE-QA", "kind": "HISTORICAL_STORED_QA", "source": {"path": "Claude/docs/v1.0.23/results/qa_images/CURVE_QA_v23.md", "start": 1, "end": 38}, "axes": axes("synthetic_numerical", "implementation_regression"), "fresh_status": "NOT_PORTABLY_REEXECUTED_STEP61", "limitation": "Selected-panel numerical smoke and shared-path equality; not a proof of C2 parameter differentiability, material validity, or experiment."},
        {"id": "SUP-P5-AUDIT", "kind": "ADVERSARIAL_REVIEW_AGGREGATE", "source": {"path": "Claude/docs/v1.0.23/results/comp_v23/AUD_REPORT_v23.md", "start": 1, "end": 65}, "axes": axes("synthetic_numerical", "implementation_regression", "picard_iteration_behavior", "transfer_identity"), "fresh_status": "HISTORICAL_REVIEW_REBOUNDED_BY_STEPS65_TO67", "limitation": "No material/experimental truth follows from zero critical findings."},
        {"id": "SUP-MERGE-READY", "kind": "PROCESS_AGGREGATE", "source": {"path": "Claude/docs/v1.0.23/results/MERGE_READINESS_v23.md", "start": 1, "end": 52}, "axes": axes("synthetic_numerical", "implementation_regression", "picard_iteration_behavior", "transfer_identity"), "fresh_status": "HISTORICAL_MERGE_READINESS_ONLY", "limitation": "Historical integration readiness is not canonical scientific or publication readiness."},
        {"id": "SUP-STEP65-PRIMARY", "kind": "PRIMARY_LITERATURE_BOUNDARY", "source": {"path": PRIOR_INPUTS[0], "commit": EXPECTED_PARENT}, "axes": axes(external="ESTABLISHED_BOUNDED_JCP147_REF6_METHOD_ONLY"), "fresh_status": "JCP147_AND_REF6_FULL_TEXT_READ_REF7_GROUND_NOT_FOUND", "limitation": "Source-problem method authority does not validate the graphite mapping."},
        {"id": "SUP-STEP66-DERIVATION", "kind": "INTERNAL_REDERIVATION", "source": {"path": PRIOR_INPUTS[1], "commit": EXPECTED_PARENT}, "axes": axes("synthetic_numerical", "picard_iteration_behavior", "transfer_identity"), "fresh_status": "PASS_P064_STEP66_REDERIVATION", "limitation": "Reduced feedback is a hypothesis; first Picard and voltage-coordinate identity only."},
        {"id": "SUP-STEP67-RUNTIME", "kind": "ISOLATED_RUNTIME", "source": {"path": PRIOR_INPUTS[3], "commit": EXPECTED_PARENT}, "axes": axes("synthetic_numerical", "implementation_regression", "picard_iteration_behavior", "transfer_identity"), "fresh_status": "PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS", "limitation": "Executed frozen inputs/environments only; external scientific authority remains false."},
    ]


def overclaim_routes() -> list[dict[str, Any]]:
    return [
        {"id": "AUTH-001", "claim": "P1 cites absent cond_audit_verify.py and describes G1 as enforcing bit-exactness although its source predicate is tolerance <=1e-12.", "disposition": "CONFLICT_OPEN", "owner": "Phase 083", "acceptance_criterion": "Recover and replay the exact frozen script/blob or supersede its dependent attributions as GROUND_NOT_FOUND, and state G1 as tolerance-based compatibility unless the predicate itself is explicitly changed and revalidated."},
        {"id": "AUTH-002", "claim": "JCP applicability conditions validate the graphite mapping one-to-one.", "disposition": "REBOUNDED", "owner": "Phase 073", "acceptance_criterion": "Derive and independently review the JCP147/Ref6-to-graphite variable and assumption mapping without using Ref7 method content until its original is read."},
        {"id": "AUTH-003", "claim": "G-E3 establishes the true/general self-consistent solution or convergence.", "disposition": "REBOUNDED", "owner": "Phase 076", "acceptance_criterion": "Provide a stated function space, finite-window initial condition, contraction domain and independent convergence/accuracy tests beyond the code-defined fixed point."},
        {"id": "AUTH-004", "claim": "G-E4 establishes time response, EIS or instrument transfer behavior.", "disposition": "REJECTED_PROMOTION", "owner": "Phase 074", "acceptance_criterion": "Introduce and validate an explicit sweep-rate time map and instrument/electrochemical response model against a primary source and held-out data."},
        {"id": "AUTH-005", "claim": "The current transfer implementation is a general causal/nonuniform-grid identity.", "disposition": "REBOUNDED", "owner": "Phase 076", "acceptance_criterion": "Specify padding/boundary convention, enforce or handle grid uniformity, and compare against a non-circular causal reference on finite windows."},
        {"id": "AUTH-006", "claim": "Stored c_rate labels establish physical current regimes.", "disposition": "REJECTED_FACTOR_3600", "owner": "Phase 074", "acceptance_criterion": "Separate A, h^-1 and s^-1 interfaces, correct the factor 3600, and revalidate all regime claims on dimensionally consistent inputs."},
        {"id": "AUTH-007", "claim": "P5 zero-critical/adversarial PASS establishes all physics and publication readiness.", "disposition": "REJECTED_PROMOTION", "owner": "Phase 088", "acceptance_criterion": "Complete independent primary-source, material, experimental and final-manuscript validation gates; review severity alone is insufficient."},
        {"id": "AUTH-008", "claim": "Curve QA proves global C2 smoothness and parameter differentiability, and v1.0.23 inverse fitting has a fresh round-trip validation.", "disposition": "REBOUNDED", "owner": "Phase 081", "acceptance_criterion": "Run portable assertion-backed refinement, parameter-derivative, boundary and v1.0.23 inverse-fit recovery tests over declared parameter, noise and protocol domains."},
        {"id": "AUTH-009", "claim": "Curve ranges and shapes are physically/materially normal.", "disposition": "UNVERIFIED_MATERIAL", "owner": "Phase 086", "acceptance_criterion": "Compare units, basis, material identity and protocol against traceable held-out experimental data with uncertainty."},
        {"id": "AUTH-010", "claim": "Ref7 method content is available through JCP147 metadata or later summaries.", "disposition": "GROUND_NOT_FOUND", "owner": "Phase 071", "acceptance_criterion": "Lawfully acquire the Ref7 original, bind its raw hash, and read 1-EOF/all pages before method-content use."},
        {"id": "AUTH-011", "claim": "The documented background algebraic self-consistency has a frozen implementation solver.", "disposition": "GROUND_NOT_FOUND", "owner": "Phase 075", "acceptance_criterion": "Implement or explicitly remove the background algebraic root claim and verify the Q_bg/Cbg capacity basis."},
        {"id": "AUTH-012", "claim": "Step 65's Eq. 38 semantic projection K*r*mu remains authoritative after Step 66 rederived K*sigma*mu from the bound original crop.", "disposition": "SUPERSEDED_PENDING_CARRY_FORWARD_BINDING", "owner": "Step 69.1", "acceptance_criterion": "Bind the Step 65 K*r*mu record as superseded by the Step 66 K*sigma*mu correction in the 83-source disposition and carry-forward delta, with both source anchors retained."},
        {"id": "AUTH-013", "claim": "Curve QA is a fresh portable execution gate.", "disposition": "REJECTED_CURRENT_RUNTIME", "owner": "Phase 083", "acceptance_criterion": "Remove hard-coded paths, declare dependencies, run on both supported runtimes, and bind outputs to frozen inputs."},
        {"id": "AUTH-014", "claim": "The ratio route has demonstrated positive computational benefit.", "disposition": "NOT_ESTABLISHED", "owner": "Phase 076", "acceptance_criterion": "Benchmark accuracy and cost against converged Picard under identical tolerances and representative declared domains."},
    ]


def human_evidence() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise BuildError("human evidence markers missing or duplicated")
    body = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0]
    match = re.fullmatch(r"\s*```json\s*\n(.*?)\n```\s*", body, flags=re.DOTALL)
    if match is None:
        raise BuildError("human evidence block malformed")
    value = strict_json_bytes(match.group(1).encode("utf-8"), RESULT.relative_to(ROOT).as_posix())
    expected = {
        "axis_count": 7,
        "complete_authority_record_denominator": 47,
        "executable_hard_gates": 13,
        "experimental_validated_gates": 0,
        "external_comprehensive_validated_gates": 0,
        "gate": GATE,
        "material_validated_gates": 0,
        "overclaim_routes": 14,
        "phase_ceiling": CEILING,
        "planned_phase_gate_declarations": 24,
        "planned_core_gate_denominator": 37,
        "ref7_original_status": "GROUND_NOT_FOUND",
        "supplemental_evidence_records": 7,
    }
    if value != expected:
        raise BuildError(f"human evidence mismatch: {value!r}")
    return value, sha256(compact_bytes(value))


def document_contracts() -> list[dict[str, Any]]:
    checks = {
        RESULT: (GATE, "canonical gate denominator: `37/37`", EXPECTED_SUBJECT),
        PARENT_LEDGER: ("Step 68 precommit", GATE, EXPECTED_SUBJECT),
        ACTIVE_LEDGER: ("Step 68 precommit", GATE, EXPECTED_SUBJECT),
        HANDOVER: ("Step 68 precommit", GATE, EXPECTED_SUBJECT),
    }
    rows = []
    for path, snippets in checks.items():
        raw = path.read_bytes()
        text = raw.decode("utf-8", "strict")
        for snippet in snippets:
            if snippet not in text:
                raise BuildError(f"control snippet missing: {path}: {snippet}")
        rows.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(raw),
                     "bytes": len(raw), "required_snippets": list(snippets)})
    return rows


def build() -> dict[str, Any]:
    human, human_hash = human_evidence()
    canonical = canonical_rows()
    supplemental = supplemental_evidence()
    overclaims = overclaim_routes()
    material = [r["id"] for r in canonical if r["axes"]["material_validation"] not in ("NOT_ESTABLISHED", "NOT_EVALUATED")]
    experimental = [r["id"] for r in canonical if r["axes"]["experimental_validation"] not in ("NOT_ESTABLISHED", "NOT_EVALUATED")]
    comprehensive_external = [r["id"] for r in canonical if r["axes"]["external_primary_literature_validation"] == "ESTABLISHED_COMPREHENSIVE"]
    if material or experimental or comprehensive_external:
        raise BuildError("forbidden authority promotion")
    return finalize({
        "artifact_kind": "PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX",
        "schema_version": 1,
        "phase": 64,
        "step": "68",
        "generated_date": "2026-08-29",
        "generated_by": "Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "status": "PASS_WITH_CONCERNS",
        "gate": GATE,
        "phase_ceiling": CEILING,
        "authority_axes": list(AXES),
        "counts": {
            "complete_authority_records": len(canonical),
            "executable_hard_gates": sum(r["record_kind"] == "EXECUTABLE_HARD" for r in canonical),
            "planned_phase_gate_declarations": 24,
            "planned_core_gate_records": 37,
            "current_phase_gate_records": sum(r["record_kind"] == "CURRENT_PHASE_GATE" for r in canonical),
            "additional_boundary_records": 5,
            "supplemental_evidence_records": len(supplemental),
            "overclaim_routes": len(overclaims),
            "material_validated_gates": len(material),
            "experimental_validated_gates": len(experimental),
            "external_comprehensive_validated_gates": len(comprehensive_external),
        },
        "non_double_count": {
            "planned_core_denominator": "13 executable declarations + 24 P1-P5 declaration records = 37",
            "complete_authority_denominator": "37 planned core + 5 current Phase 064 gates + 5 historical/static/observational boundary records = 47",
            "repeated_pass_claims": "linked through depends_on or supplemental evidence; never added to either denominator",
            "p4_state": "one intentional-skip process declaration, not PASS and not FAIL",
            "p1_observation": "zero-hard-assertion supplemental evidence, not executable gate 14",
            "curve_qa": "historical supplemental evidence, not executable gate 14",
            "reference_ledger_vs_adopted_bibliography": "separate process and adopted-source authorities; neither substitutes for the other",
        },
        "high_risk_bindings": high_risk_bindings(),
        "authority_records": canonical,
        "supplemental_evidence": supplemental,
        "overclaim_routes": overclaims,
        "literature_boundary": {
            "jcp147_original": "FULL_TEXT_READ_PRIMARY_VOR_METHOD_CONTENT_ONLY",
            "ref6_original": "FULL_TEXT_READ_PRIMARY_VOR_METHOD_CONTENT_ONLY",
            "ref7_bibliography": "OFFICIAL_METADATA_DOI_10.1063/1.4802584",
            "ref7_original": "GROUND_NOT_FOUND",
            "jcp_ref_to_graphite_material_applicability": "NOT_ESTABLISHED",
        },
        "authority_summary": {
            "synthetic_internal_evidence": True,
            "implementation_regression_evidence": True,
            "selected_picard_iteration_evidence": True,
            "voltage_coordinate_transfer_identity_evidence": True,
            "material_validation": False,
            "experimental_validation": False,
            "comprehensive_external_primary_literature_validation": False,
            "canonical_model_selection": False,
            "publication_readiness": False,
        },
        "source_contracts": source_contracts(),
        "prior_machine_inputs": prior_inputs(),
        "document_contracts": document_contracts(),
        "human_evidence": human,
        "human_evidence_semantic_sha256": human_hash,
        "repository_boundary": {
            "exact_paths": [
                "Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py",
                "Codex/work/v1023_phase064/validate_phase064_step68.py",
                "Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json",
                "Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md",
                "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
                "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
                "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
            ],
            "claude_modified": False,
            "production_modified": False,
        },
    })


def main() -> None:
    if git_text("rev-parse", "HEAD") != EXPECTED_PARENT:
        raise BuildError("builder must run from the exact Step 67 parent")
    if not RESULT.exists():
        raise BuildError("result-first document is absent")
    payload = build()
    atomic_write(OUT, pretty_bytes(payload))
    print(f"{GATE} core={payload['counts']['planned_core_gate_records']}/37 complete={payload['counts']['complete_authority_records']}/47 supplemental=7 routes=14")


if __name__ == "__main__":
    main()
