#!/usr/bin/env python3
"""Build Phase 064 Step 66 ratio/transfer rederivation evidence.

The builder reads frozen Git blobs, the committed Step 65 literature evidence,
and a result-first human evidence block.  It independently reconstructs a
small deterministic Volterra/Picard benchmark.  It never imports or executes
the frozen production module, contacts the network, or modifies Claude/**.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[3]
RESULT = REPO / "Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md"
PRIOR_MATRIX = REPO / "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json"
PRIOR_ATTESTATION = REPO / "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json"
OUTPUT = REPO / "Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "5fb19384e3df7a73c96fcf26e8f599b42c331ae7"
EXPECTED_SUBJECT = "audit(phase064): rederive v1023 ratio transfer closure"
GATE = "PASS_P064_STEP66_REDERIVATION"
CEILING = "CONDITIONAL_P064_REF7_GNF_AND_FROZEN_DEFECTS_OPEN"
EVIDENCE_BEGIN = "<!-- P064_STEP66_HUMAN_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P064_STEP66_HUMAN_EVIDENCE_END -->"

EXPECTED_SOURCES: dict[str, dict[str, Any]] = {
    "Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md": {
        "blob": "ce4b17399f8d7318b4053134959ab77f9038d313", "bytes": 20203,
        "lines": 225, "sha256": "4c3aedabac00ac657f12bf2dffe6f696017654b883f2798c2d824ee70665b228",
        "read": [1, 225],
    },
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": {
        "blob": "b0e246c7bd31c63134137066d31a6032d4d190d7", "bytes": 20019,
        "lines": 212, "sha256": "26c1546fcc701d8dec6847f1ad60cbf0ea2222808fe2aaa396265a7f8641c51c",
        "read": [1, 212],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": {
        "blob": "15cd3c78f37dea9a1b942108d01df3db62101a6f", "bytes": 10884,
        "lines": 145, "sha256": "a01c5394781f3674fb167846d1acc05a49c7ec2f4c419c7480a128b1c0747723",
        "read": [1, 145],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex": {
        "blob": "490139d35601c8d83da6d567bcdcf2ac97619d1c", "bytes": 18372,
        "lines": 245, "sha256": "7fed61f947f974c21f58361519ae9cc3511ac633c3869503243a70f9cf0eef49",
        "read": [1, 245],
    },
    "Claude/docs/v1.0.23/_sections/ch1_sec10_sum.tex": {
        "blob": "10ab70e2e4a99cc72b122c75922bc178041b1923", "bytes": 15794,
        "lines": 170, "sha256": "5edccc997672641f6722cf9eae80cb93c83345f5cc9cfaa205f500a57c16de6e",
        "read": [1, 170],
    },
    "Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md": {
        "blob": "3c840b4a67b9c8b134c76c984efe34fba9271915", "bytes": 21845,
        "lines": 301, "sha256": "289b59fe109318a9d42a6daa29d30e43815a45e3729baed3366688444c767cd2",
        "read": [1, 301],
    },
    "Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py": {
        "blob": "b3b62159919fce6d4c4665b234d74456fa0fcf10", "bytes": 2866,
        "lines": 68, "sha256": "279b711ef3c33b046136f7b962c76f65ccacbaca369f571ab8f3ed50524f86dc",
        "read": [1, 68],
    },
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": {
        "blob": "cf330bfc14e0291474ea9490a5b206c2f060a319", "bytes": 6502,
        "lines": 128, "sha256": "1417277231ea795515037f470ec160e5077e04d8ab351df7e85c6467671fcef4",
        "read": [1, 128],
    },
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": {
        "blob": "554425dd566c20314357eddfcf4261517df907ee", "bytes": 97860,
        "lines": 1585, "sha256": "0298bb5fdf47ed5faf2f8301b6d84dc88fd580a69c8e616daa3942d35ceae7cf",
        "read": [[105, 210], [450, 535], [630, 710]],
        "read_kind": "TARGETED_CONTROLLER_PLUS_INDEPENDENT_EXPANSION",
    },
}

REQUIRED_SNIPPETS: dict[str, tuple[str, ...]] = {
    "Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex": (
        r"\kappa(\xi)=\kappa_0\,\exp",
        r"H(\omega)=\frac1{1+i\omega L_V}",
        r"\varepsilon\equiv",
    ),
    "Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex": (
        r"L_{q,j}=\frac{|I|}{Q_\cell\,k_j}",
        r"k_0=k_BT/h",
        r"1+e^{-\mathcal A/RT}",
    ),
    "Claude/docs/v1.0.23/_sections/ch1_sec10_sum.tex": (
        r"[1/h] 수치를 SI 로 환산하면 $\sim3600$ 배 작아지나",
    ),
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py": (
        "T_attempt = (I / Q_cell) * h / kB",
        "I_use = c * Q_cell",
        "np.fft.fftfreq",
    ),
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py": (
        "peak_H[m]-peak_frozen[m]",
        "for _ in range(60)",
    ),
}

EXPECTED_CORRECTIONS = [
    ("P064-S66-CORR-001", "P0", "Phase 064 Step 67"),
    ("P064-S66-CORR-002", "P1", "Phase 064 Step 66"),
    ("P064-S66-CORR-003", "P1", "Phase 064 Step 66"),
    ("P064-S66-CORR-004", "P1", "Phase 064 Step 66"),
    ("P064-S66-CORR-005", "P1", "Phase 064 Step 66"),
    ("P064-S66-CORR-006", "P1", "Phase 064 Step 66"),
    ("P064-S66-CORR-007", "P1", "Phase 064 Step 67"),
    ("P064-S66-CORR-008", "P1", "Phase 064 Step 66"),
    ("P064-S66-CORR-009", "P2", "Phase 064 Step 68"),
    ("P064-S66-CORR-010", "P2", "Phase 064 Step 67"),
    ("P064-S66-CORR-011", "P2", "Phase 064 Step 69.1"),
]


class BuildError(RuntimeError):
    pass


def run_git(*args: str, binary: bool = False) -> str | bytes:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        raise BuildError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout if binary else proc.stdout.decode("utf-8", "strict").strip()


def git_bytes(commit: str, path: str) -> bytes:
    raw = run_git("show", f"{commit}:{path}", binary=True)
    assert isinstance(raw, bytes)
    return raw


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def atomic_write(path: Path, raw: bytes) -> None:
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.",
            suffix=".tmp", delete=False,
        ) as handle:
            temporary = handle.name
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def strict_load_bytes(raw: bytes) -> Any:
    def pairs_hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise BuildError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise BuildError(f"non-finite JSON constant: {value}")

    value = json.loads(raw, object_pairs_hook=pairs_hook, parse_constant=reject_constant)

    def reject_overflow(node: Any) -> None:
        if isinstance(node, float) and not math.isfinite(node):
            raise BuildError("non-finite JSON numeric overflow")
        if isinstance(node, dict):
            for child in node.values():
                reject_overflow(child)
        elif isinstance(node, list):
            for child in node:
                reject_overflow(child)

    reject_overflow(value)
    return value


def strict_load(path: Path) -> Any:
    return strict_load_bytes(path.read_bytes())


def parse_human_evidence() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise BuildError("E_HUMAN_EVIDENCE_MARKERS")
    block = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise BuildError("E_HUMAN_EVIDENCE_FENCE")
    evidence = strict_load_bytes(block[8:-4].encode("utf-8"))
    if not isinstance(evidence, dict):
        raise BuildError("E_HUMAN_EVIDENCE_ROOT")
    return evidence, sha256(compact_bytes(evidence))


def verify_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, expected in EXPECTED_SOURCES.items():
        raw = git_bytes(BASELINE, path)
        blob = run_git("rev-parse", f"{BASELINE}:{path}")
        assert isinstance(blob, str)
        text = raw.decode("utf-8", "strict")
        if blob != expected["blob"]:
            raise BuildError(f"E_SOURCE_BLOB:{path}")
        if len(raw) != expected["bytes"] or sha256(raw) != expected["sha256"]:
            raise BuildError(f"E_SOURCE_BYTES:{path}")
        if len(text.splitlines()) != expected["lines"]:
            raise BuildError(f"E_SOURCE_LINES:{path}")
        for snippet in REQUIRED_SNIPPETS.get(path, ()):
            if snippet not in text:
                raise BuildError(f"E_SOURCE_ANCHOR:{path}:{snippet}")
        row = {
            "path": path, "git_blob": blob, "raw_sha256": sha256(raw),
            "bytes": len(raw), "physical_lines": len(text.splitlines()),
            "read_interval": expected["read"],
            "read_kind": expected.get("read_kind", "READ_FULL_STEP66"),
        }
        rows.append(row)
    return rows


def validate_human(evidence: dict[str, Any]) -> None:
    required = {
        "authority_ceiling", "benchmark", "contraction", "corrections",
        "evidence_date", "evidence_id", "expected_parent", "expected_subject",
        "fredholm", "gate", "ground_not_found", "readers", "reduced_volterra",
        "ref7_status", "source_mutation_count", "timebase", "transfer",
    }
    if set(evidence) != required:
        raise BuildError("E_HUMAN_ROOT_KEYS")
    if evidence["authority_ceiling"] != CEILING:
        raise BuildError("E_AUTHORITY_CEILING")
    if evidence["expected_parent"] != EXPECTED_PARENT:
        raise BuildError("E_EXPECTED_PARENT")
    if evidence["expected_subject"] != EXPECTED_SUBJECT or evidence["gate"] != GATE:
        raise BuildError("E_GATE_SUBJECT")
    if evidence["ref7_status"] != "GROUND_NOT_FOUND_NO_INFERENCE":
        raise BuildError("E_REF7_PROMOTION")
    if evidence["source_mutation_count"] != 0:
        raise BuildError("E_SOURCE_MUTATION")

    actual_corrections = [
        (row.get("id"), row.get("severity"), row.get("owner"))
        for row in evidence["corrections"]
        if isinstance(row, dict)
    ]
    if actual_corrections != EXPECTED_CORRECTIONS:
        raise BuildError("E_CORRECTION_REGISTER")
    if evidence["fredholm"] != {
        "eq32_status": "EXACT_WITHIN_EQ19_EQ20_APPROXIMATED_SYSTEM",
        "eq33_status": "EXACT_REARRANGEMENT_REQUIRES_NONZERO_W",
        "eq34_status": "REFERENCE_RATIO_APPROXIMATION",
        "eq38_angular_factor": "exp(K*sigma*mu)",
        "eq39_status": "APPROXIMATE_CLOSED_RESULT",
        "kernel_direction": "FIXED_DOMAIN_TWO_SIDED_NONCAUSAL",
        "radial_domains": [["sigma", "r"], ["r", "infinity"]],
    }:
        raise BuildError("E_FREDHOLM_CONTRACT")
    if evidence["reduced_volterra"]["model_authority"] != "REDUCED_FEEDBACK_HYPOTHESIS":
        raise BuildError("E_REDUCED_MODEL_AUTHORITY")
    if evidence["contraction"] != {
        "global_scope": "REMOTE_PAST_OR_ZERO_INITIAL_TERM",
        "global_sufficient": "q=norm_sigma_infinity*K_kappa/kappa_min^2<1",
        "global_units": "(V^-1)*(V^-1)/(V^-1)^2=1",
        "local_indicator": "epsilon_local=g*L0/(4*w)",
        "local_status": "LEADING_ORDER_HEURISTIC_NOT_GLOBAL_THEOREM",
    }:
        raise BuildError("E_CONTRACTION_CONTRACT")
    if evidence["timebase"]["legacy_overestimate_factor"] != 3600:
        raise BuildError("E_TIMEBASE_FACTOR")
    if evidence["timebase"]["required_separation"] != [
        "current_A_for_IR", "normalized_rate_s^-1_for_kinetics",
    ]:
        raise BuildError("E_TIMEBASE_SEPARATION")
    transfer = evidence["transfer"]
    if transfer["formula"] != "H=1/(1+i*omega_x*L0)" or transfer["omega_units"] != "V^-1":
        raise BuildError("E_TRANSFER_FORMULA")
    if transfer["prohibited_promotions"] != [
        "TIME_WITHOUT_SWEEP_RATE", "EIS", "INSTRUMENT_RESPONSE",
    ]:
        raise BuildError("E_TRANSFER_PROMOTION")
    benchmark = evidence["benchmark"]
    if benchmark["authority"] != "INTERNAL_SYNTHETIC_RUNTIME_OBSERVATION_ONLY":
        raise BuildError("E_BENCHMARK_AUTHORITY")
    if benchmark["comparator_conclusion"] != {
        "ratio_vs_converged_picard": "POSITIVE_WITH_APPROXIMATION_ERROR",
        "ratio_vs_first_picard": "ZERO_IDENTICAL_OUTPUT",
        "ratio_vs_frozen": "NEGATIVE_SLOWER",
    }:
        raise BuildError("E_BENCHMARK_COMPARATOR")
    if [row.get("g_eff") for row in benchmark["rows"]] != [0.5, 1.0, 2.0]:
        raise BuildError("E_BENCHMARK_ROWS")
    if not all(row.get("ratio_equals_picard1") is True for row in benchmark["rows"]):
        raise BuildError("E_BENCHMARK_PICARD1")


def logistic(x: float, center: float, width: float) -> float:
    z = (x - center) / width
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def solve_linear(xeq: list[float], step: float, lengths: list[float]) -> list[float]:
    out = [0.0] * len(xeq)
    out[0] = xeq[0]
    for index in range(1, len(xeq)):
        length = lengths[index]
        if not math.isfinite(length) or length <= 0.0:
            raise BuildError("E_NUMERIC_LENGTH")
        a = step / length
        out[index] = (out[index - 1] + a * xeq[index]) / (1.0 + a)
    return out


def max_abs(left: list[float], right: list[float]) -> float:
    return max(abs(a - b) for a, b in zip(left, right, strict=True))


def relative_l2(left: list[float], right: list[float]) -> float:
    numerator = math.fsum((a - b) ** 2 for a, b in zip(left, right, strict=True))
    denominator = math.fsum(b * b for b in right)
    return math.sqrt(numerator / denominator)


def rounded(value: float) -> float:
    return float(f"{value:.14g}")


def deterministic_benchmark() -> dict[str, Any]:
    count = 2401
    lower, upper = -0.15, 0.35
    center, width, length0 = 0.10, 0.02, 0.006
    step = (upper - lower) / (count - 1)
    xeq = [logistic(lower + index * step, center, width) for index in range(count)]
    frozen = solve_linear(xeq, step, [length0] * count)
    rows: list[dict[str, Any]] = []
    for g in (0.0, 0.5, 1.0, 2.0):
        first_lengths = [length0 * math.exp(g * (1.0 - x)) for x in frozen]
        ratio = solve_linear(xeq, step, first_lengths)
        iterate = frozen
        first_picard: list[float] | None = None
        iterations = 0
        delta = math.inf
        for iterations in range(1, 201):
            lengths = [length0 * math.exp(g * (1.0 - x)) for x in iterate]
            next_iterate = solve_linear(xeq, step, lengths)
            if iterations == 1:
                first_picard = next_iterate
            delta = max_abs(next_iterate, iterate)
            iterate = next_iterate
            if delta <= 1e-13:
                break
        else:
            raise BuildError(f"E_PICARD_NONCONVERGENCE:{g}")
        assert first_picard is not None
        if ratio != first_picard:
            raise BuildError(f"E_RATIO_NOT_PICARD1:{g}")
        kappa0 = 1.0 / length0
        kappa_min = kappa0 * math.exp(-g)
        k_kappa = g * kappa0
        sigma_max = 1.0 / (4.0 * width)
        q_sufficient = sigma_max * k_kappa / (kappa_min * kappa_min)
        rows.append({
            "g_eff": g,
            "epsilon_local": rounded(g * length0 / (4.0 * width)),
            "q_sufficient_global_bound": rounded(q_sufficient),
            "picard_iterations_to_1e-13": iterations,
            "final_sup_delta": rounded(delta),
            "ratio_equals_picard1": True,
            "frozen_relative_l2_vs_fixed_point": rounded(relative_l2(frozen, iterate)),
            "ratio_relative_l2_vs_fixed_point": rounded(relative_l2(ratio, iterate)),
            "frozen_max_abs_vs_fixed_point": rounded(max_abs(frozen, iterate)),
            "ratio_max_abs_vs_fixed_point": rounded(max_abs(ratio, iterate)),
            "workload_passes": {"frozen": 1, "ratio": 2, "converged_picard": 1 + iterations},
        })
    return {
        "authority": "DETERMINISTIC_INTERNAL_DISCRETIZATION_ONLY",
        "grid": {"N": count, "domain_V": [lower, upper], "center_V": center,
                 "w_V": width, "L0_V": length0, "scheme": "BACKWARD_EULER"},
        "reference": "CONVERGED_PICARD_FIXED_POINT_NOT_EXTERNAL_TRUTH",
        "rows": rows,
        "complexity": "ALL_ROUTES_O_N_FOR_FIXED_ITERATION_COUNT",
    }


def prior_literature_binding() -> dict[str, Any]:
    matrix = strict_load(PRIOR_MATRIX)
    attestation = strict_load(PRIOR_ATTESTATION)
    if not isinstance(matrix, dict) or not isinstance(attestation, dict):
        raise BuildError("E_PRIOR_ROOT")
    chain = matrix.get("equation_chain")
    if not isinstance(chain, list):
        raise BuildError("E_PRIOR_CHAIN")
    eq38 = next((row for row in chain if row.get("equation") == "38"), None)
    if not isinstance(eq38, dict):
        raise BuildError("E_PRIOR_EQ38")
    stale = eq38.get("semantic_projection")
    if stale != (
        "EQ38|definition=Lambda_rx|integral=4*pi*exp(U1(sigma))*"
        "integral_0_infinity[r^2*exp(-U1(r))*angular_average(exp(K*r*mu)*S_R(r,mu))dr]"
    ):
        raise BuildError("E_PRIOR_EQ38_STALE_PROJECTION_IDENTITY")
    crop_hash = eq38.get("crop_raw_pixel_sha256")
    if crop_hash != "63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978":
        raise BuildError("E_PRIOR_EQ38_CROP")
    return {
        "matrix_raw_sha256": sha256(PRIOR_MATRIX.read_bytes()),
        "attestation_raw_sha256": sha256(PRIOR_ATTESTATION.read_bytes()),
        "step65_eq38_stale_projection": stale,
        "step66_corrected_projection": (
            "EQ38|definition=Lambda_rx|integral=4*pi*exp(U1(sigma))*"
            "integral_0_infinity[r^2*exp(-U1(r))*angular_average(exp(K*sigma*mu)*S_R(r,mu))dr]"
        ),
        "eq38_pdf_crop_raw_pixel_sha256": crop_hash,
        "correction_scope": "SEMANTIC_PROJECTION_SUPERSEDED_PDF_CROP_PRESERVED",
    }


def build_payload() -> dict[str, Any]:
    evidence, evidence_sha = parse_human_evidence()
    validate_human(evidence)
    sources = verify_sources()
    payload: dict[str, Any] = {
        "schema": "phase064.step66.ratio_transfer_rederivation.v1",
        "generated_by": "build_phase064_step66_ratio_transfer_rederivation.py",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT,
        "gate": GATE,
        "status": "PASS_PENDING_PERSISTENCE_WITH_CORRECTIONS",
        "authority_ceiling": CEILING,
        "human_evidence_semantic_sha256": evidence_sha,
        "source_contracts": sources,
        "prior_literature_binding": prior_literature_binding(),
        "fredholm_rederivation": {
            "problem_class": "FREDHOLM_SECOND_KIND_FIXED_SEMI_INFINITE_DOMAIN",
            "domain": {"r": ["sigma", "infinity"], "mu": [-1, 1]},
            "boundary_conditions": ["Wbar_u(r)->1 as r->infinity", "radial_derivative_at_sigma=0"],
            "upstream_status": "EQS19_20_ORIENTATION_AVERAGING_APPROXIMATIONS",
            "eq32_domains": [["sigma", "r"], ["r", "infinity"]],
            "eq33": "EXACT_REARRANGEMENT_WITHIN_APPROXIMATED_SYSTEM_REQUIRES_W_NONZERO",
            "eq34": "REFERENCE_RATIO_APPROXIMATION",
            "eq38_angular_factor": "exp(K*sigma*mu)",
            "eq39": "APPROXIMATE_CLOSED_RESULT",
            "transferable_principle": "REFERENCE_SUBSTITUTION_DESIGN_MOTIVATION_ONLY",
            "literal_graphite_identity": False,
        },
        "volterra_rederivation": {
            "coordinate": "DIRECTED_VOLTAGE_X_INCREASES_ALONG_PROTOCOL",
            "problem_class": "NONLINEAR_CAUSAL_VOLTERRA_SECOND_KIND",
            "local_equivalent": "FIRST_ORDER_NONLINEAR_ODE",
            "initial_condition_contract": "FINITE_X0_TERM_OR_PROVED_REMOTE_PAST_DECAY",
            "selected_law": "kappa(xi)=kappa0*exp[-g*(1-xi)]",
            "selected_law_authority": "REDUCED_FEEDBACK_HYPOTHESIS",
            "frozen_reference": "r0_prime=sigma_x-kappa0*r0",
            "first_picard": "r1=T[r0]; r1_prime=sigma_x-kappa(xi0)*r1",
            "frozen_limit": "g=0 => r=r1=r0 for identical initial condition",
            "jcp_solution_ratio_identity": False,
        },
        "contraction": {
            "sufficient_bound": "q=norm_sigma_infinity*K_kappa/kappa_min^2",
            "sufficient_condition": "q<1",
            "scope": "REMOTE_PAST_OR_ZERO_INITIAL_TERM",
            "assumptions": ["kappa>=kappa_min>0", "abs(partial_kappa/partial_xi)<=K_kappa", "sigma_bounded"],
            "dimension": "DIMENSIONLESS",
            "local_indicator": "epsilon_local=g*L0/(4*w)",
            "local_authority": "LEADING_ORDER_HEURISTIC_NOT_GLOBAL_THEOREM",
        },
        "transfer": {
            "coordinate": "DIRECTED_VOLTAGE_X",
            "fourier_convention": "fhat=integral f(x)*exp(-i*omega_x*x)dx",
            "formula": "H=1/(1+i*omega_x*L0)",
            "units": {"omega_x": "V^-1", "L0": "V", "H": "1"},
            "finite_dft_caveat": "UNPADDED_DFT_IS_CIRCULAR_NOT_CAUSAL",
            "time_mapping": "REQUIRES_EXPLICIT_SWEEP_RATE_NU_AND_TAU=L0/abs(nu)",
            "external_authority": {"time_without_sweep_rate": False, "EIS": False, "instrument_response": False},
        },
        "timebase": {
            "Ah_contract": "dq/dt_s=I_A/(3600*Q_Ah)=C_h/3600",
            "coulomb_contract": "dq/dt_s=I_A/Q_C",
            "kinetic_length": "L_q=(dq/dt_s)/k_s; L_V=abs(dV/dq)*L_q",
            "legacy_overestimate_factor": 3600,
            "required_separation": ["current_A_for_IR", "normalized_rate_s^-1_for_kinetics"],
            "physical_current_regime_approved": False,
            "dimensionless_L0_over_w_tests_retained": True,
        },
        "deterministic_benchmark": deterministic_benchmark(),
        "independent_timing_observation": evidence["benchmark"],
        "correction_register": evidence["corrections"],
        "ground_not_found": evidence["ground_not_found"],
        "authority": {
            "internal_mathematical_rederivation": True,
            "internal_synthetic_numerical_behavior": True,
            "external_material_validation": False,
            "external_experimental_validation": False,
            "ref7_method_content": False,
            "canonical_model_selection": False,
            "production_repair": False,
        },
        "non_applicable_targets": [
            "ALGEBRAIC_CHARGE_BALANCE_ROOT",
            "BACKGROUND_ALGEBRAIC_SELF_CONSISTENCY",
            "LITERAL_JCP_KERNEL_VARIABLE_TRANSFER",
            "REF7_INFERRED_METHOD_CONTENT",
        ],
        "source_mutation_count": 0,
    }
    payload["semantic_sha256"] = sha256(compact_bytes(payload))
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    if not args.check_only:
        atomic_write(OUTPUT, pretty_bytes(payload))
    print(
        f"PASS_P064_STEP66_BUILD sources={len(payload['source_contracts'])} "
        f"corrections={len(payload['correction_register'])} "
        f"benchmark_cases={len(payload['deterministic_benchmark']['rows'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
