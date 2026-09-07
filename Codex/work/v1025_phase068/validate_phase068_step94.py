#!/usr/bin/env python3
"""Validate the independent U13 threshold rederivation transaction."""

from __future__ import annotations

import argparse
import ast
import copy
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = "P068-STEP94-U13-INDEPENDENT-REDERIVATION-1"
BASE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
U13 = "2802395dd03e6cabe3e981bddddbba139e3963bc"
TIP = "11f90544865dd179739ca5bc5062b28c1078e504"
EXPECTED_PARENT = "0b850ea9ffa33e04356d11b83190f9a7cfbea37c"
PARENT_PARENT = "25e3120ff0f38c5fa2bf603413034920640b3e62"
EXPECTED_SUBJECT = "audit(phase068): rederive u13 threshold regularity"
CONTENT_TERMINAL = "PASS_P068_STEP94_U13_REDERIVATION"
PERSISTENCE_TERMINAL = "PASS_P068_STEP94_PERSISTENCE"
PRECOMMIT_MARKER = "P068_STEP94_U13_REDERIVATION_PRECOMMIT"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
ACTIVE_REF = "refs/heads/" + ACTIVE_BRANCH
TRACKING_REF = "refs/remotes/origin/" + ACTIVE_BRANCH
UPSTREAM = "origin/" + ACTIVE_BRANCH
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
FIXED_REFS = {
    "refs/remotes/origin/codex/lib-physics-endgame-v1025_2": (
        "refs/heads/codex/lib-physics-endgame-v1025_2", "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"),
    "refs/remotes/origin/main": ("refs/heads/main", "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"),
    "refs/remotes/origin/claude/version-1026-regsol-review-kl88j7": (
        "refs/heads/claude/version-1026-regsol-review-kl88j7", "e3e1a634f34b711aa4803fd190fe9120f1755f13"),
    "refs/remotes/origin/codex/v1025_2-physics-conformance": (
        "refs/heads/codex/v1025_2-physics-conformance", TIP),
}
BUILDER = "Codex/work/v1025_phase068/build_phase068_step94.py"
VALIDATOR = "Codex/work/v1025_phase068/validate_phase068_step94.py"
MATRIX = "Codex/results/PHASE_068_U13_REGSOL_REDERIVATION.json"
RESULT = "Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
PRIOR_MATRIX = "Codex/results/PHASE_068_PHASE044_054_REAUDIT_MATRIX.json"
PRIOR_RESULT = "Codex/results/PHASE_068_STEP_093_PHASE044_054_REAUDIT_RESULT.md"
EXACT_SEVEN = (BUILDER, VALIDATOR, MATRIX, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
PRE_JSON_SIX = (BUILDER, VALIDATOR, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
CONTROLS = (RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
EXPECTED_STATUS = dict(zip(EXACT_SEVEN, ("A", "A", "A", "A", "M", "M", "M")))
TEX = "Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex"
WIDTH_TEX = "Claude/docs/v1.0.25.2/_sections/ch1_sec05_width.tex"
PEAK_TEX = "Claude/docs/v1.0.25.2/_sections/ch1_sec06_eqpeak.tex"
P44_SCRIPT = "Codex/work/v1025_2_physics_branch/phase044_regsol_threshold_probe.py"
P54_SCRIPT = "Codex/work/v1025_2_physics_branch/phase054_regsol_crosscheck.py"
P44_JSON = "Codex/results/PHASE_044_REGSOL_THRESHOLD_PROBE.json"
P54_JSON = "Codex/results/PHASE_054_V1025_2_REGSOL_CROSSCHECK.json"
SOURCE_SPECS = (
    ("U13-BEFORE", BASE, TEX, "ea762ff015f47e03b79e99f051deae5ddef44f9c"),
    ("U13-AFTER", U13, TEX, "05f1d84713017dde303f56ca7004b61aa0496979"),
    ("P44-SCRIPT", TIP, P44_SCRIPT, "ee7ac08df3698a21500f7a0cf02ed8f814d65344"),
    ("P44-OUTPUT", TIP, P44_JSON, "aa51785f88445760d29d3ec3a5c8d219464c995a"),
    ("P54-SCRIPT", TIP, P54_SCRIPT, "853df8d32b95b96d60adee6fc842ca4307713ab1"),
    ("P54-OUTPUT", TIP, P54_JSON, "58f6b037c9d4e0d3bc9f07a2847ee4cde16fd338"),
    ("WIDTH-DEFINITION", BASE, WIDTH_TEX, "2003860215e0a721876bace4364b3b7a6a594031"),
    ("PEAK-DEFINITION", BASE, PEAK_TEX, "fe0816cf46d4ddb8cbb4b6fbb012e3b6e979a17b"),
)
READ_PATHS = {p for _, _, p, _ in SOURCE_SPECS} | set(EXACT_SEVEN) | {PRIOR_MATRIX, PRIOR_RESULT}
HEX = set("0123456789abcdef")
MAX_JSON_BYTES = 4_000_000
MAX_JSON_NODES = 250_000
MAX_JSON_DEPTH = 64
R, T, F = 8.314, 298.15, 96485.0
C = R * T / F
AUTHORITY = "MATHEMATICAL_FIXED_SMOOTH_KERNEL_MEASURE_ONLY_NOT_MATERIAL_OR_CANONICAL_AUTHORITY"

# Frozen after the human result, ledgers and handover have been written.
CONTROL_LF_SHA256: dict[str, str] = {
    RESULT: "b6fa2755be0c8c72c05eb58c5644e92a65eb9553b49ccd5410419cf3029623bc",
    PARENT_LEDGER: "d02e076cbf943d058b2c50072eee157e7a104b6e0b42c537973aa7a99f533350",
    ACTIVE_LEDGER: "b595f0ff1874e56b8e3e68d063a39c95117078a4f6f8dd619161aaa9eabd3f49",
    HANDOVER: "e1e740d573154afb15bc1e819046336b5d056d5ebe56ef5271c55fcd5d9bf526",
}


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


def fail(code: str, detail: str = "") -> None:
    raise ValidationError(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def lf_normalize(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def physical_lines(raw: bytes) -> int:
    return raw.count(b"\n") + int(bool(raw) and not raw.endswith(b"\n"))


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    return sha256(canonical_bytes({k: v for k, v in value.items() if k != "semantic_sha256"}))


def is_hex40(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 40 and set(value) <= HEX


def strict_json_loads(raw: bytes, *, label: str) -> Any:
    if len(raw) > MAX_JSON_BYTES:
        fail("E_JSON_LIMIT", label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                fail("E_JSON_DUPLICATE_KEY", label)
            result[key] = value
        return result

    def nonfinite(value: str) -> None:
        fail("E_JSON_NONFINITE", label)

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs, parse_constant=nonfinite)
    except (ValueError, RecursionError, UnicodeDecodeError):
        fail("E_JSON_PARSE", label)
    stack = [(value, 1)]
    nodes = 0
    while stack:
        item, depth = stack.pop()
        nodes += 1
        if depth > MAX_JSON_DEPTH or nodes > MAX_JSON_NODES:
            fail("E_JSON_LIMIT", label)
        if isinstance(item, dict):
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, float) and not math.isfinite(item):
            fail("E_JSON_NONFINITE", label)
    return value


def validate_git_argv(args: list[str]) -> None:
    if not args or any(not isinstance(x, str) or "\0" in x for x in args):
        fail("E_GIT_ARGV")
    cmd = args[0]
    valid = False
    if cmd == "cat-file":
        valid = len(args) == 3 and args[1] == "blob" and is_hex40(args[2])
    elif cmd == "config":
        valid = args == ["config", "--get", "remote.origin.url"]
    elif cmd == "ls-remote":
        valid = len(args) == 4 and args[1:3] == ["--refs", ORIGIN_URL] and args[3] in {ACTIVE_REF, *(x[0] for x in FIXED_REFS.values())}
    elif cmd == "ls-tree":
        valid = len(args) >= 5 and args[1] == "-l" and is_hex40(args[2]) and args[3] == "--" and set(args[4:]) <= READ_PATHS
    elif cmd == "rev-parse":
        valid = (len(args) == 2 and args[1] in {"HEAD", TRACKING_REF, "@{upstream}", *FIXED_REFS, *(c + "^{tree}" for c in (BASE, U13, TIP, EXPECTED_PARENT))}) or (len(args) == 3 and args[1] == "--abbrev-ref" and args[2] in {"HEAD", "@{upstream}"})
    elif cmd == "show":
        valid = len(args) == 4 and args[1] == "-s" and args[2] in {"--format=%P", "--format=%s"} and is_hex40(args[3])
    elif cmd == "diff":
        valid = args == ["diff", "--cached", "--name-status", "--no-renames", "-z"]
    elif cmd == "diff-tree":
        valid = len(args) == 7 and args[1:6] == ["--no-commit-id", "--name-status", "--no-renames", "-r", "-z"] and is_hex40(args[6])
    elif cmd == "ls-files":
        valid = args == ["ls-files", "--stage", "-z", "--", *EXACT_SEVEN]
    elif cmd == "status":
        valid = args == ["status", "--porcelain=v1", "-z", "--untracked-files=all"]
    if not valid:
        fail("E_GIT_ARGV", cmd)


def run_git(args: list[str]) -> bytes:
    validate_git_argv(args)
    process = subprocess.run(["git", *args], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)
    if process.returncode:
        fail("E_GIT_EXEC", f"{args[0]}:{process.returncode}:{process.stderr.decode('utf-8', 'replace').strip()}")
    return process.stdout


def git_text(args: list[str]) -> str:
    return run_git(args).decode("utf-8", "strict").strip()


def tree_entry(commit: str, path: str) -> tuple[str, int]:
    rows = git_text(["ls-tree", "-l", commit, "--", path]).splitlines()
    if len(rows) != 1:
        fail("E_TREE_ENTRY", path)
    meta, separator, actual_path = rows[0].partition("\t")
    fields = meta.split()
    if not separator or actual_path != path or len(fields) != 4 or fields[:2] != ["100644", "blob"] or not is_hex40(fields[2]) or not fields[3].isdigit():
        fail("E_TREE_ENTRY", path)
    return fields[2], int(fields[3])


def frozen_bytes(commit: str, path: str, expected_blob: str | None = None) -> bytes:
    blob, size = tree_entry(commit, path)
    raw = run_git(["cat-file", "blob", blob])
    if len(raw) != size or git_blob_oid(raw) != blob or (expected_blob is not None and blob != expected_blob):
        fail("E_SOURCE_IDENTITY", path)
    return raw


def source_records() -> list[dict[str, Any]]:
    records = []
    for source_id, commit, path, blob in SOURCE_SPECS:
        raw = frozen_bytes(commit, path, blob)
        text = raw.decode("utf-8", "strict")
        parser = "UTF8_TEXT"
        if path.endswith(".json"):
            strict_json_loads(raw, label=path)
            parser = "STRICT_JSON_FULL_RAW_READ"
        elif path.endswith(".py"):
            ast.parse(text, filename=path)
            parser = "AST_PLUS_HUMAN_FULL_READ"
        records.append({
            "id": source_id, "commit": commit, "tree": git_text(["rev-parse", commit + "^{tree}"]),
            "path": path, "blob": blob, "mode": "100644", "raw_bytes": len(raw), "raw_sha256": sha256(raw),
            "lf_bytes": len(lf_normalize(raw)), "lf_sha256": sha256(lf_normalize(raw)), "lines": physical_lines(raw),
            "read_status": "READ_FULL", "review_mode": "DIRECT_SOURCE_FULL_READ_WITH_OBJECT_IDENTITY",
            "coverage": [[1, physical_lines(raw)]], "parser": parser,
        })
    return records


def analytic_derivation() -> dict[str, Any]:
    # Reversion is checked with exact rational arithmetic, not floating fits.
    c1, c2, c3 = Fraction(3, 8), Fraction(-27, 80), Fraction(1377, 5600)
    if Fraction(8, 3) * c1 != 1 or Fraction(8, 3) * c2 + Fraction(32, 5) * c1**2 != 0 or Fraction(8, 3) * c3 + Fraction(64, 5) * c1 * c2 + Fraction(128, 7) * c1**3 != 0:
        fail("E_BINODAL_SERIES")
    assumptions = [
        "a=Omega/(R*T), epsilon=a-2, theta_a=1/2-x, y=theta-1/2, c=R*T/F",
        "R,T,F,Q,U0,width,alpha are fixed; T>0,F>0,width>0,alpha>0; Q is the transition capacity",
        "kappa is a normalized nonnegative translation-invariant kernel; kappa,kappa',kappa'' are bounded and continuous",
        "The skew logistic kappa(z)=alpha*sigma(z/width)^alpha*(1-sigma(z/width))/width obeys these assumptions for every fixed alpha>0",
        "The area statement integrates over the full real voltage line; finite windows are unnormalized observations with omitted tail mass",
        "C0,C1 are in a at each voltage and uniformly in voltage under the bounded-derivative assumptions; derivative in Omega is derivative in a divided by R*T",
        "No zero-width, varying-kernel, varying-temperature, material, mechanism, held-out-data or canonical-source conclusion is asserted",
    ]
    derivative = "D(V)=Q*c*integral_0^1 (1-2*theta)*kappa'(V-V_2(theta)) dtheta"
    propositions = [
        {"id": "U13-AREA", "analytic_status": "CONFIRMED", "statement": "integral_R B_a(V)dV=Q", "derivation": "Fubini with unit-normalized kappa: Q[(1-2 theta_a)+theta_a+theta_a]=Q; for a<=2 theta_a=1/2", "numeric_evidence": "normalization_rows"},
        {"id": "U13-SUBCRITICAL-GAP", "analytic_status": "CONFIRMED", "statement": "gap mass=0 for a<=2", "derivation": "The documented subcritical prescription theta_a=1/2 makes 1-2 theta_a identically zero", "numeric_evidence": "normalization_rows"},
        {"id": "U13-C0", "analytic_status": "CONFIRMED", "statement": "B_a(V)->B_2(V) from both sides", "derivation": "H(a,V)=Q integral_0^1 kappa(V-V_a(theta))dtheta is C2, hence C1, in a by dominated differentiation under the stated bounded C2 assumptions; B_{2+epsilon}=H(2+epsilon)+R_epsilon with R_epsilon=O(epsilon^(7/2))", "numeric_evidence": "extension_rows"},
        {"id": "U13-LEFT-DERIVATIVE", "analytic_status": "CONFIRMED", "statement": derivative, "derivation": "For a<=2 B=H; partial_a[V-V_a(theta)]=c(1-2theta). B_{2-h}=B_2-h*D+O(h^2)", "numeric_evidence": "extension_rows:left and left_Richardson"},
        {"id": "U13-RIGHT-DERIVATIVE", "analytic_status": "CONFIRMED", "statement": derivative, "derivation": "Gap replacement R_epsilon=o(epsilon), hence B_{2+epsilon}=B_2+epsilon*D+O(epsilon^2). Exact Leibniz boundary terms vanish because V_a(theta_a)=V_a(1-theta_a)=U0", "numeric_evidence": "extension_rows:right and right_Richardson"},
        {"id": "U13-C1", "analytic_status": "CONFIRMED_UNDER_DECLARED_ASSUMPTIONS", "statement": "Both one-sided derivatives exist and equal D(V); dB/da is continuous at a=2", "derivation": "Differentiate the stable integrals and gap mass: the moving-boundary terms cancel exactly. The remaining stable-domain integral of Q*c*(1-2theta)*kappa' tends by dominated convergence to D from above; H_a tends to D from below. O(epsilon) magnitude alone is not used", "numeric_evidence": "extension_rows:pointwise and norm left/right/Richardson; high_precision_rows"},
        {"id": "U13-FOOTNOTE-NORMALIZATION", "analytic_status": "SOURCE_NUMERIC_NORMALIZATION_DEFECT_CONFIRMED", "statement": "The corrected footnote defines eta=abs(Omega/(2RT)-1)=abs(epsilon)/2; its quoted 5.90 belongs to epsilon=a-2. In eta units the same limit is approximately 11.79828", "derivation": "Delta/eta=2*Delta/epsilon. This factor-of-two defect is separate from the confirmed C1 proposition", "numeric_evidence": "historical_threshold_rows and normalization_defect"},
    ]
    for row in propositions:
        row["authority_ceiling"] = AUTHORITY
    return {
        "assumptions": assumptions,
        "symbol_map": {
            "theta": {"meaning": "lithium site occupancy, complementary to xi=1-theta", "unit": "1", "source": "U13-BEFORE:L75-81"},
            "Omega": {"meaning": "regular-solution molar interaction parameter", "unit": "J/mol", "source": "U13-BEFORE:L190-208"},
            "R": {"meaning": "molar gas constant, fixed at 8.314 in the historical probes", "unit": "J/(mol*K)", "source": "P44-OUTPUT:constants"},
            "T": {"meaning": "fixed absolute temperature, 298.15 in the probes", "unit": "K", "source": "P44-OUTPUT:constants"},
            "F": {"meaning": "Faraday constant, fixed at 96485 in the probes", "unit": "C/mol", "source": "P44-OUTPUT:constants"},
            "Q": {"meaning": "transition capacity; no implicit conversion of the user's capacity unit", "unit": "[Q]", "source": "U13-BEFORE:L83-93;PEAK-DEFINITION:L20-35"},
            "U0": {"meaning": "U^circ, the fixed coexistence potential and logistic center, not generally the skew peak apex", "unit": "V", "source": "U13-BEFORE:L72-80;PEAK-DEFINITION:L51-61"},
            "rho": {"meaning": "pushforward of dtheta on (0,theta_a) union (1-theta_a,1), total mass 2*theta_a", "unit": "1/V", "source": "U13-BEFORE:L210-211"},
            "kappa": {"meaning": "normalized translation-invariant broadened logistic/skew-logistic kernel", "unit": "1/V", "source": "U13-BEFORE:L197-209;PEAK-DEFINITION:L37-50"},
            "width": {"meaning": "fixed positive w_j; w_j=n_j*R*T/F does not introduce Omega dependence", "unit": "V", "source": "WIDTH-DEFINITION:L264-275"},
            "alpha": {"meaning": "fixed positive skew exponent, not a phase or transfer coefficient", "unit": "1", "source": "PEAK-DEFINITION:L37-73"},
        },
        "binodal_equation": "ln(theta/(1-theta))+a*(1-2*theta)=0",
        "binodal_expansion": "0=2*epsilon*x-(16/3)*x^3-(64/5)*x^5-(256/7)*x^7+O(x^9)",
        "x_squared_coefficients": [str(c1), str(c2), str(c3)],
        "x_series": "x=sqrt(3*epsilon/8)*(1-9*epsilon/20+1269*epsilon^2/5600+O(epsilon^3))",
        "gap_mass": "2*x=sqrt(3*epsilon/2)*(1-9*epsilon/20+1269*epsilon^2/5600+O(epsilon^3))",
        "potential": "V_a(theta)=U0-c*[ln(theta/(1-theta))+a*(1-2theta)]",
        "full_reference_integral": "H(a,V)=Q*integral_0^1 kappa(V-V_a(theta)) dtheta",
        "central_potential_shift": "d(y)=V_{2+epsilon}(1/2+y)-U0=c*[2*epsilon*y-(16/3)*y^3-(64/5)*y^5-...], an odd function",
        "central_replacement": "R_epsilon(V)=Q*[2*x*kappa(V-U0)-integral_{-x}^{x} kappa(V-U0-d(y))dy]",
        "central_cancellation": "constant terms cancel exactly; integral d(y)dy=0 by oddness. |R|<=Q*||kappa''||inf/2*integral d(y)^2dy=O(epsilon^(7/2)); kernel symmetry is not required",
        "central_leading_term": "R_epsilon=-(32/105)*Q*c^2*(3/8)^(3/2)*kappa''(V-U0)*epsilon^(7/2)+o(epsilon^(7/2))",
        "central_second_moment": "integral_{-x}^x [2*c*epsilon*y*(1-y^2/x^2)]^2 dy=(64/105)*c^2*epsilon^2*x^3; x^2~3*epsilon/8",
        "derivative": derivative,
        "omega_derivative": "dB/dOmega=D/(R*T); units are [Q]/V per J/mol, whereas D has units [Q]/V",
        "propositions": propositions,
        "proof_basis": "BINODAL_SERIES_PLUS_EXACT_LEIBNIZ_BOUNDARY_CANCELLATION_AND_DOMINATED_CONVERGENCE",
        "c1_inferred_from_linear_norm_alone": False,
    }


@lru_cache(maxsize=5)
def gauss_legendre(order: int) -> tuple[np.ndarray, np.ndarray]:
    """Independent vector Newton roots, not either historical script's leggauss."""
    if order not in {400, 800, 1600, 3200}:
        fail("E_QUADRATURE_ORDER")
    roots = np.cos(np.pi * (np.arange(1, order + 1, dtype=float) - 0.25) / (order + 0.5))
    for _ in range(12):
        p0, p1 = np.ones(order), roots.copy()
        for degree in range(2, order + 1):
            p0, p1 = p1, ((2 * degree - 1) * roots * p1 - (degree - 1) * p0) / degree
        derivative = order * (roots * p1 - p0) / (roots * roots - 1)
        delta = p1 / derivative
        roots -= delta
        if float(np.max(np.abs(delta))) < 3e-16:
            break
    p0, p1 = np.ones(order), roots.copy()
    for degree in range(2, order + 1):
        p0, p1 = p1, ((2 * degree - 1) * roots * p1 - (degree - 1) * p0) / degree
    derivative = order * (roots * p1 - p0) / (roots * roots - 1)
    weights = 2 / ((1 - roots * roots) * derivative * derivative)
    if abs(float(np.sum(weights)) - 2) > 1e-12:
        fail("E_QUADRATURE_WEIGHT")
    return roots[::-1], weights[::-1]


def gap_halfwidth(epsilon: float) -> float:
    if epsilon <= 0:
        return 0.0
    # Solve atanh(g)/g = 1+epsilon/2 for g=2*x. A positive-term
    # series avoids cancellation against the trivial g=0 root near threshold.
    low, high = 0.0, min(1.0 - 1e-14, math.sqrt(1.5 * epsilon))
    for _ in range(90):
        g = (low + high) / 2
        if g < 0.2:
            term, total = g * g, 0.0
            for degree in range(1, 32):
                total += term / (2 * degree + 1)
                term *= g * g
            residual = total - epsilon / 2
        else:
            residual = math.atanh(g) / g - 1 - epsilon / 2
        if residual > 0:
            high = g
        else:
            low = g
    return (low + high) / 4


def kernel(delta: np.ndarray, alpha: float, width: float, *, derivative: bool = False) -> np.ndarray:
    z = delta / width
    e = np.exp(-np.abs(z))
    s = np.where(z >= 0, 1 / (1 + e), e / (1 + e))
    complement = np.where(z >= 0, e / (1 + e), 1 / (1 + e))
    k = alpha * s**alpha * complement / width
    return k * (alpha * complement - s) / width if derivative else k


def integrate_interval(a: float, voltage: np.ndarray, alpha: float, width: float, order: int, low: float, high: float, *, derivative: bool = False) -> np.ndarray:
    roots, weights = gauss_legendre(order)
    theta = low + (high - low) * (roots + 1) / 2
    weights = weights * (high - low) / 2
    potential = -C * (np.log(theta) - np.log1p(-theta) + a * (1 - 2 * theta))
    if derivative:
        weights = weights * C * (1 - 2 * theta)
    output = np.empty(len(voltage))
    for start in range(0, len(voltage), 128):
        values = kernel(voltage[start:start + 128, None] - potential[None, :], alpha, width, derivative=derivative)
        output[start:start + 128] = np.sum(values * weights[None, :], axis=1)
    return output


def curve(a: float, voltage: np.ndarray, alpha: float, width: float, order: int) -> np.ndarray:
    x = gap_halfwidth(a - 2)
    if x == 0:
        return integrate_interval(a, voltage, alpha, width, order, 0.0, 1.0)
    return (2 * x * kernel(voltage, alpha, width)
            + integrate_interval(a, voltage, alpha, width, order, 0.0, 0.5 - x)
            + integrate_interval(a, voltage, alpha, width, order, 0.5 + x, 1.0))


def matched_curve(a: float, voltage: np.ndarray, alpha: float, width: float, order: int) -> np.ndarray:
    """Same measure with a common full-domain quadrature for small differences.

    The separately evaluated central replacement preserves the measure while
    avoiding an endpoint-quadrature bias divided by an arbitrarily small step.
    """
    full = integrate_interval(a, voltage, alpha, width, order, 0, 1)
    epsilon = a-2
    if epsilon <= 0:
        return full
    x = gap_halfwidth(epsilon)
    nodes, weights = gauss_legendre(400)
    y = x*(nodes+1)/2
    shift = 2*epsilon*y
    for degree in range(1, 12):
        shift -= 2**(2*degree+2)*y**(2*degree+1)/(2*degree+1)
    shift *= C
    result = np.empty(len(voltage))
    for start in range(0,len(voltage),128):
        v = voltage[start:start+128, None]
        paired = 2*kernel(v,alpha,width)-kernel(v-shift,alpha,width)-kernel(v+shift,alpha,width)
        result[start:start+128] = np.sum(paired*weights*x/2,axis=1)
    return full+result


def norm(values: np.ndarray) -> float:
    return float(np.max(np.abs(values)))


def rounded(value: Any) -> Any:
    """Six significant decimal digits are a reporting bin, not compute precision."""
    if isinstance(value, dict):
        return {key: rounded(child) for key, child in value.items()}
    if isinstance(value, list):
        return [rounded(child) for child in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            fail("E_NUMERIC_NONFINITE")
        if abs(value) < 1e-11:
            return 0.0
        return float(format(value, ".6g"))
    return value


def historical_reproduction() -> dict[str, Any]:
    stored44 = strict_json_loads(frozen_bytes(TIP, P44_JSON), label=P44_JSON)
    stored54 = strict_json_loads(frozen_bytes(TIP, P54_JSON), label=P54_JSON)
    rows44, rows54, areas = [], [], []
    for phase, alphas, window, points, stored_rows in (
        (44, (1.0,), 0.12, 1201, stored44["rows"]),
        (54, (1.0, 4.0, 8.0), 1.0, 4001, stored54["threshold_rows"]),
    ):
        voltage = np.linspace(-window, window, points)
        for alpha in alphas:
            reference = curve(2, voltage, alpha, 0.01, 1600)
            if phase == 44:
                area = float(np.trapezoid(reference, voltage))
                if abs(area - stored44["reference_at_interaction_over_rt_2"]["finite_window_area"]) > 2e-8:
                    fail("E_HISTORICAL_AREA")
                areas.append({"phase": 44, "window": [-window, window], "points": points, "area": area, "missing_tail_mass": 1 - area, "renormalized": False})
            selected = [row for row in stored_rows if phase == 44 or row["alpha"] == alpha]
            for stored in selected:
                epsilon = stored["epsilon"]
                right = curve(2 + epsilon, voltage, alpha, 0.01, 1600) - reference
                ratio = norm(right) / epsilon
                old = stored["max_abs_difference_over_epsilon" if phase == 44 else "right_max_abs_difference_over_epsilon"]
                if abs(ratio - old) > 3e-5:
                    fail("E_HISTORICAL_THRESHOLD", f"{phase}:{alpha}:{epsilon}:{ratio}:{old}")
                item = {"phase": phase, "alpha": alpha, "epsilon": epsilon, "right_gap_weight": 2 * gap_halfwidth(epsilon), "right_max_difference_over_epsilon": ratio,
                        "right_max_difference_over_sqrt_epsilon": norm(right) / math.sqrt(epsilon), "stored_right_ratio": old,
                        "difference_from_stored": ratio - old, "absolute_tolerance": 3e-5, "grid": points, "window": [-window, window], "order": 1600}
                if phase == 44:
                    item["rms_difference_over_epsilon"] = float(np.sqrt(np.mean(right * right))) / epsilon
                    if abs(item["rms_difference_over_epsilon"] - stored["rms_difference_over_epsilon"]) > 3e-5:
                        fail("E_HISTORICAL_RMS")
                    rows44.append(item)
                else:
                    left = reference - curve(2 - epsilon, voltage, alpha, 0.01, 1600)
                    item["left_max_difference_over_epsilon"] = norm(left) / epsilon
                    item["stored_left_ratio"] = stored["left_max_abs_difference_over_epsilon"]
                    if abs(item["left_max_difference_over_epsilon"] - item["stored_left_ratio"]) > 3e-5:
                        fail("E_HISTORICAL_LEFT")
                    rows54.append(item)
    voltage = np.linspace(-1, 1, 4001)
    for stored in stored54["normalization_and_gap_rows"]:
        a, alpha = stored["interaction_over_rt"], stored["alpha"]
        numeric_area = float(np.trapezoid(curve(a, voltage, alpha, 0.01, 1600), voltage))
        gap = 2 * gap_halfwidth(a - 2)
        if abs(numeric_area - 1) > 2e-8 or abs(gap - stored["gap_weight"]) > 2e-10:
            fail("E_NORMALIZATION_REPRODUCTION", f"{a}:{alpha}")
        areas.append({"phase": 54, "a": a, "alpha": alpha, "area": numeric_area, "gap_mass": gap, "stable_mass": 1-gap, "window": [-1, 1], "points": 4001, "renormalized": False})
    return {"historical_phase044_rows": rows44, "historical_phase054_rows": rows54, "normalization_rows": areas,
            "execution_kind": "FRESH_INDEPENDENT_REIMPLEMENTATION_NOT_EXECUTION_OF_HISTORICAL_SCRIPTS",
            "constants": {"R": R, "T": T, "F": F, "Q": 1, "U0": 0, "width": 0.01},
            "historical_row_counts": {"phase044": 8, "phase054_threshold": 9, "phase054_normalization": 24}}


def extension_evidence() -> dict[str, Any]:
    rows, convergence = [], []
    configs = [(alpha, width) for alpha in (0.5, 1.0, 2.0, 4.0, 8.0) for width in (0.01,)]
    configs += [(alpha, width) for alpha in (1.0, 4.0, 8.0) for width in (0.005, 0.02)]
    voltage = np.linspace(-0.12, 0.12, 601)
    epsilons = (1e-3, 1e-4, 1e-5, 1e-6, 1e-7)
    for alpha, width in configs:
        reference = matched_curve(2, voltage, alpha, width, 1600)
        derivative = integrate_interval(2, voltage, alpha, width, 1600, 0, 1, derivative=True)
        previous = None
        for epsilon in epsilons:
            right = (matched_curve(2+epsilon, voltage, alpha, width, 1600)-reference)/epsilon
            left = (reference-matched_curve(2-epsilon, voltage, alpha, width, 1600))/epsilon
            half = epsilon / 2
            right_half = (matched_curve(2+half, voltage, alpha, width, 1600)-reference)/half
            left_half = (reference-matched_curve(2-half, voltage, alpha, width, 1600))/half
            rich_right, rich_left = 2*right_half-right, 2*left_half-left
            indices = [200, 250, 300, 350, 400]
            error = max(norm(rich_left-derivative), norm(rich_right-derivative), norm(rich_right-rich_left))
            if error > 2e-3:
                fail("E_DERIVATIVE_RICHARDSON", f"{alpha}:{width}:{epsilon}:{error}")
            row = {"alpha": alpha, "width": width, "epsilon": epsilon, "order": 1600, "grid": 601, "window": [-0.12, 0.12],
                   "left_norm": norm(left), "right_norm": norm(right), "left_error_to_D": norm(left-derivative), "right_error_to_D": norm(right-derivative),
                   "left_right_norm_difference": norm(left-right), "left_Richardson_error": norm(rich_left-derivative), "right_Richardson_error": norm(rich_right-derivative),
                   "Richardson_left_right_difference": norm(rich_left-rich_right), "absolute_tolerance": 2e-3,
                   "pointwise": [{"V": float(voltage[i]), "D": float(derivative[i]), "left": float(left[i]), "right": float(right[i]), "left_Richardson": float(rich_left[i]), "right_Richardson": float(rich_right[i])} for i in indices],
                   "linear_norm_is_not_c1_proof": True}
            if previous is not None:
                old_epsilon, old_error = previous
                row["observed_right_error_order"] = math.log(old_error/max(norm(right-derivative), 1e-16)) / math.log(old_epsilon/epsilon)
            previous = epsilon, norm(right-derivative)
            rows.append(row)
    for alpha, width in ((0.5, 0.01), (1.0, 0.005), (4.0, 0.01), (8.0, 0.02)):
        fine = integrate_interval(2, voltage, alpha, width, 3200, 0, 1, derivative=True)
        coarse = integrate_interval(2, voltage, alpha, width, 800, 0, 1, derivative=True)
        middle = integrate_interval(2, voltage, alpha, width, 1600, 0, 1, derivative=True)
        difference = norm(middle-fine)
        if difference > 3e-5:
            fail("E_QUADRATURE_CONVERGENCE", f"{alpha}:{width}:{difference}")
        convergence.append({"kind": "QUADRATURE", "alpha": alpha, "width": width, "orders": [800,1600,3200], "difference_800_3200": norm(coarse-fine), "difference_1600_3200": difference, "absolute_tolerance": 3e-5})
    for window, points in ((0.12, 601), (0.12, 1201), (0.12, 2401), (0.24, 2401), (1.0, 4001)):
        grid = np.linspace(-window, window, points)
        profile = curve(2, grid, 4, 0.01, 1600)
        derivative = integrate_interval(2, grid, 4, 0.01, 1600, 0, 1, derivative=True)
        convergence.append({"kind": "WINDOW_GRID", "alpha": 4, "width": 0.01, "window": [-window,window], "points": points, "area": float(np.trapezoid(profile,grid)), "derivative_norm": norm(derivative), "renormalized": False})
    return {"extension_rows": rows, "convergence_rows": convergence, "extension_design": "11 alpha/width cases x 5 epsilons, four 800/1600/3200 order comparisons, five window/grid cases; not a full factorial study",
            "roundoff_notice": "Binary64 curve subtraction eventually amplifies quadrature/roundoff divided by epsilon. Extension rows use full-domain H plus paired central replacement, algebraically the same measure, to avoid moving-endpoint quadrature bias. Richardson residuals and order reversal are retained, not hidden; high precision point checks are independent.",
            "sampled_norm_notice": "Every grid norm is a sampled maximum, not a continuous supremum. In particular historical alpha=4 gives about 9.69 on its grid. The independent equation review's separate bounded peak search estimates 9.69183; this module does not establish that value or a global supremum."}


def high_precision_evidence() -> list[dict[str, Any]]:
    rows = []
    for precision in (35, 55):
        with mp.workdps(precision):
            c = mp.mpf("8.314")*mp.mpf("298.15")/mp.mpf("96485")
            w = mp.mpf("0.01")
            for alpha, voltage in ((1, "0"), (4, "0"), (4, "0.02")):
                v = mp.mpf(voltage)

                def k(z: Any) -> Any:
                    s = 1/(1+mp.exp(-z/w))
                    return alpha*s**alpha*(1-s)/w

                def kp(z: Any) -> Any:
                    s = 1/(1+mp.exp(-z/w))
                    return k(z)*(alpha*(1-s)-s)/w

                def potential(theta: Any, a: Any) -> Any:
                    return -c*(mp.log(theta/(1-theta))+a*(1-2*theta))

                breaks = [0, mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("0.5"), mp.mpf("0.9"), mp.mpf("0.99"), 1]
                derivative = mp.quad(lambda th: c*(1-2*th)*kp(v-potential(th, 2)), breaks)
                sigma = 1/(1+mp.exp(-v/w))
                k_second = k(v)*((alpha-(alpha+1)*sigma)**2-(alpha+1)*sigma*(1-sigma))/w**2
                leading = -mp.mpf(32)/105*c**2*(mp.mpf(3)/8)**mp.mpf("1.5")*k_second
                for e_text in ("1e-6", "1e-10"):
                    epsilon = mp.mpf(e_text)
                    # Integrand differences avoid cancellation of whole integrals.
                    left = mp.quad(lambda th: (k(v-potential(th, 2))-k(v-potential(th, 2-epsilon)))/epsilon, breaks)
                    x = mp.findroot(lambda xx: mp.atanh(2*xx)/(2*xx)-1-epsilon/2, mp.sqrt(3*epsilon/8))
                    correction = 2*x*k(v)-mp.quad(lambda yy: k(v-potential(mp.mpf("0.5")+yy,2+epsilon)), [-x,0,x])
                    right = mp.quad(lambda th: (k(v-potential(th, 2+epsilon))-k(v-potential(th, 2)))/epsilon, breaks)+correction/epsilon
                    if max(abs(left-derivative), abs(right-derivative)) > mp.mpf("2e-5"):
                        fail("E_HIGH_PRECISION_DERIVATIVE")
                    normalized_replacement = correction/epsilon**mp.mpf("3.5")
                    replacement_tolerance = mp.mpf("2e-4") if precision == 35 else mp.mpf("1e-5")
                    if abs(normalized_replacement-leading) > replacement_tolerance:
                        fail("E_CENTRAL_REPLACEMENT_ORDER")
                    rows.append({"digits": precision, "method": "MPMATH_TANH_SINH_INDEPENDENT_OF_GAUSS_LEGENDRE", "alpha": alpha, "width": 0.01, "V": float(v), "epsilon": float(epsilon),
                                 "D": float(derivative), "left": float(left), "right": float(right), "left_error": float(abs(left-derivative)), "right_error": float(abs(right-derivative)),
                                 "central_replacement_decimal": mp.nstr(correction,16), "central_replacement_over_epsilon_7_2": float(normalized_replacement),
                                 "central_leading_coefficient": float(leading), "central_coefficient_error": float(abs(normalized_replacement-leading)),
                                 "central_coefficient_tolerance": float(replacement_tolerance),
                                 "cancellation_notice": "35-digit subtraction of gap and removed mass loses relative digits at epsilon=1e-10; 55-digit rows resolve this and are checked against the analytic 7/2 coefficient",
                                 "absolute_tolerance": 2e-5})
    for low, high in zip(rows[:6], rows[6:]):
        if max(abs(low[key]-high[key]) for key in ("D","left","right")) > 1e-11:
            fail("E_PRECISION_EXTENSION")
    return rows


def file_identity(path: str) -> dict[str, Any]:
    target = ROOT / path
    if not target.is_file() or target.is_symlink():
        fail("E_PRE_JSON_MISSING", path)
    raw = target.read_bytes()
    return {"path": path, "raw_bytes": len(raw), "raw_sha256": sha256(raw), "lf_sha256": sha256(lf_normalize(raw)), "lines": physical_lines(raw)}


@lru_cache(maxsize=1)
def numeric_evidence() -> dict[str, Any]:
    return rounded({**historical_reproduction(), **extension_evidence(), "high_precision_rows": high_precision_evidence(),
                    "calculation_precision": "IEEE754 binary64 plus independent 35 and 55 decimal digit tanh-sinh",
                    "serialization_precision": "six significant decimal digits; absolute values below 1e-11 serialized as zero; thresholds are tested on unrounded computations",
                    "source_mutations": 0, "runtime_source_kind": "THIS_FROZEN_VALIDATOR_NUMERICAL_ROUTINES_WITH_READ_ONLY_HISTORICAL_BLOBS"})


def fixed_predecessor_certificate() -> dict[str, Any]:
    if git_text(["show", "-s", "--format=%P", EXPECTED_PARENT]) != PARENT_PARENT:
        fail("E_PREDECESSOR_PARENT")
    if git_text(["show", "-s", "--format=%s", EXPECTED_PARENT]) != "audit(phase068): revalidate phase044 phase054 reviews":
        fail("E_PREDECESSOR_SUBJECT")
    raw = frozen_bytes(EXPECTED_PARENT, PRIOR_MATRIX)
    prior = strict_json_loads(raw, label=PRIOR_MATRIX)
    if not isinstance(prior, dict) or prior.get("step") != 93 or prior.get("content_terminal") != "PASS_P068_STEP93_PRIOR_REVIEW_REAUDIT" or prior.get("semantic_sha256") != semantic_sha(prior):
        fail("E_PREDECESSOR_MATRIX")
    prior_result = frozen_bytes(EXPECTED_PARENT, PRIOR_RESULT)
    if b"PASS_P068_STEP93_PERSISTENCE" not in prior_result:
        fail("E_PREDECESSOR_RESULT")
    return {"commit": EXPECTED_PARENT, "parent": PARENT_PARENT, "matrix_blob": git_blob_oid(raw), "matrix_raw_sha256": sha256(raw),
            "matrix_semantic_sha256": prior["semantic_sha256"], "result_blob": git_blob_oid(prior_result),
            "prior_content_terminal": prior["content_terminal"], "prior_persistence_terminal": "PASS_P068_STEP93_PERSISTENCE",
            "certificate_kind": "FIXED_COMMIT_OBJECTS_PLUS_CURRENT_LIVE_REF_GENEALOGY_NOT_HISTORICAL_VALIDATOR_REEXECUTION"}


def expected_matrix() -> dict[str, Any]:
    sources = source_records()
    result: dict[str, Any] = {
        "schema": SCHEMA, "phase": 68, "step": 94, "expected_parent": EXPECTED_PARENT, "required_commit_subject": EXPECTED_SUBJECT,
        "content_terminal": CONTENT_TERMINAL, "precommit_marker": PRECOMMIT_MARKER, "sources": sources,
        "source_totals": {"source_records": 8, "raw_bytes": sum(row["raw_bytes"] for row in sources), "lines": sum(row["lines"] for row in sources)},
        "predecessor_certificate": fixed_predecessor_certificate(), "pre_json_file_identities": [file_identity(p) for p in PRE_JSON_SIX],
        "analytic": analytic_derivation(), "numeric": numeric_evidence(),
        "normalization_defect": {"source": "U13-AFTER", "source_lines": [220, 225], "historical_epsilon": "Omega/(R*T)-2",
                                 "footnote_epsilon": "abs(Omega/(2*R*T)-1)", "ratio_conversion": 2,
                                 "historical_ratio_approximately": 5.89914, "footnote_units_ratio_approximately": 11.79828,
                                 "verdict": "CORRECTED_FOOTNOTE_NUMERICAL_COEFFICIENT_REQUIRES_FACTOR_TWO_REWRITE",
                                 "does_not_refute_conditional_c1": True},
        "authority": {"canonical_theory": False, "publication_ready": False, "material_mechanism_validity": False,
                      "external_scientific_truth": False, "original_optimizer_recovered": False, "whole_commit_adoptions": 0, "source_modifications": 0},
        "next_step": 95,
    }
    result["semantic_sha256"] = semantic_sha(result)
    return result


def validate_matrix_payload(value: Any, expected: dict[str, Any]) -> None:
    if not isinstance(value, dict) or set(value) != set(expected):
        fail("E_MATRIX_SCHEMA")
    if value["semantic_sha256"] != semantic_sha(value):
        fail("E_MATRIX_SEAL")
    if value["expected_parent"] != EXPECTED_PARENT or value["required_commit_subject"] != EXPECTED_SUBJECT:
        fail("E_TRANSACTION_IDENTITY")
    if value["sources"] != expected["sources"] or value["source_totals"] != expected["source_totals"]:
        fail("E_SOURCE_COVERAGE")
    analytic = value["analytic"]
    if not isinstance(analytic, dict) or set(analytic) != set(expected["analytic"]):
        fail("E_ANALYTIC_SCHEMA")
    if analytic.get("c1_inferred_from_linear_norm_alone") is not False:
        fail("E_C1_LINEAR_NORM_INFERENCE")
    if analytic.get("binodal_equation") != expected["analytic"]["binodal_equation"] or analytic.get("x_squared_coefficients") != expected["analytic"]["x_squared_coefficients"]:
        fail("E_BINODAL_SIGN_OR_SERIES")
    if analytic.get("propositions") != expected["analytic"]["propositions"]:
        fail("E_ONE_SIDED_PROPOSITIONS")
    if analytic != expected["analytic"]:
        fail("E_ANALYTIC_CONTENT")
    if value["normalization_defect"] != expected["normalization_defect"]:
        fail("E_EPSILON_NORMALIZATION")
    if value["numeric"] != expected["numeric"]:
        fail("E_NUMERIC_EVIDENCE")
    if value["authority"] != expected["authority"]:
        fail("E_AUTHORITY_PROMOTION")
    if value != expected:
        fail("E_MATRIX_CONTENT")


def validate_controls() -> None:
    if set(CONTROL_LF_SHA256) != set(CONTROLS):
        fail("E_CONTROL_HASH_CONFIG")
    for path in CONTROLS:
        raw = (ROOT / path).read_bytes()
        if sha256(lf_normalize(raw)) != CONTROL_LF_SHA256[path]:
            fail("E_CONTROL_HASH", path)
        text = raw.decode("utf-8", "strict")
        markers = [line for line in text.splitlines() if line.startswith("Current-state marker:")]
        if markers != [f"Current-state marker: `{PRECOMMIT_MARKER}`"]:
            fail("E_CONTROL_MARKER", path)
        for token in (EXPECTED_PARENT, EXPECTED_SUBJECT, CONTENT_TERMINAL, PERSISTENCE_TERMINAL,
                      "PENDING_AT_PRECOMMIT_BY_DESIGN", "PASS_P068_STEP93_PERSISTENCE"):
            if token not in text:
                fail("E_CONTROL_TOKEN", f"{path}:{token}")
        for artifact in EXACT_SEVEN[:4]:
            if artifact not in text:
                fail("E_CONTROL_ARTIFACT", f"{path}:{artifact}")
    for path, heading in ((ACTIVE_LEDGER, "## Next Exact Step"), (HANDOVER, "## Exact Next Action")):
        text = (ROOT / path).read_text(encoding="utf-8")
        if heading not in text or "Step 95" not in text.split(heading, 1)[1]:
            fail("E_CONTROL_NEXT", path)


def parse_status() -> dict[str, str]:
    raw = run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    if raw and not raw.endswith(b"\0"):
        fail("E_STATUS_PARSE")
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            fail("E_STATUS_PARSE")
        code, path = record[:2].decode("ascii"), record[3:].decode("utf-8")
        if "R" in code or "C" in code or path in result:
            fail("E_STATUS_PARSE", path)
        result[path] = code
    return result


def validate_status(paths: tuple[str, ...], *, staged: bool) -> None:
    expected = {p: EXPECTED_STATUS[p] + " " if staged else ("??" if EXPECTED_STATUS[p] == "A" else " M") for p in paths}
    actual = parse_status()
    if actual != expected:
        fail("E_TRANSACTION_STATUS", str(actual))


def live_oid(ref: str) -> str:
    fields = git_text(["ls-remote", "--refs", ORIGIN_URL, ref]).split()
    if len(fields) != 2 or fields[1] != ref or not is_hex40(fields[0]):
        fail("E_LIVE_REF", ref)
    return fields[0]


def validate_refs(expected_head: str) -> None:
    if git_text(["config", "--get", "remote.origin.url"]) != ORIGIN_URL:
        fail("E_ORIGIN_URL")
    if git_text(["rev-parse", "--abbrev-ref", "HEAD"]) != ACTIVE_BRANCH:
        fail("E_BRANCH")
    if git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]) != UPSTREAM:
        fail("E_UPSTREAM")
    for ref in ("HEAD", TRACKING_REF, "@{upstream}"):
        if git_text(["rev-parse", ref]) != expected_head:
            fail("E_TRANSACTION_REF", ref)
    if live_oid(ACTIVE_REF) != expected_head:
        fail("E_TRANSACTION_LIVE")
    for local_ref, (remote_ref, expected) in FIXED_REFS.items():
        if git_text(["rev-parse", local_ref]) != expected or live_oid(remote_ref) != expected:
            fail("E_FIXED_REF", local_ref)


def parse_name_status(raw: bytes) -> dict[str, str]:
    parts = raw.split(b"\0")
    if not parts or parts[-1] != b"" or len(parts[:-1]) % 2:
        fail("E_DIFF_PARSE")
    result = {}
    for status, path_raw in zip(parts[0:-1:2], parts[1:-1:2]):
        path = path_raw.decode("utf-8")
        code = status.decode("ascii")
        if code not in {"A", "M"} or path in result:
            fail("E_DIFF_PARSE", path)
        result[path] = code
    return result


def read_transaction_bytes(path: str) -> bytes:
    return (ROOT / path).read_bytes()


def validate_staged_index() -> None:
    if parse_name_status(run_git(["diff", "--cached", "--name-status", "--no-renames", "-z"])) != EXPECTED_STATUS:
        fail("E_STAGED_DIFF")
    raw = run_git(["ls-files", "--stage", "-z", "--", *EXACT_SEVEN])
    seen = set()
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        meta, sep, path_raw = entry.partition(b"\t")
        fields, path = meta.decode("ascii").split(), path_raw.decode("utf-8")
        if not sep or len(fields) != 3 or fields[0] != "100644" or fields[2] != "0" or path not in EXACT_SEVEN or path in seen:
            fail("E_STAGED_ENTRY", path)
        if git_blob_oid(read_transaction_bytes(path)) != fields[1]:
            fail("E_STAGED_BLOB", path)
        seen.add(path)
    if seen != set(EXACT_SEVEN):
        fail("E_STAGED_COUNT")


def validate_persistence(expected_commit: str) -> None:
    if not is_hex40(expected_commit):
        fail("E_EXPECTED_COMMIT")
    if parse_status():
        fail("E_PERSISTENCE_DIRTY")
    validate_refs(expected_commit)
    if git_text(["show", "-s", "--format=%P", expected_commit]) != EXPECTED_PARENT:
        fail("E_PERSISTENCE_PARENT")
    if git_text(["show", "-s", "--format=%s", expected_commit]) != EXPECTED_SUBJECT:
        fail("E_PERSISTENCE_SUBJECT")
    if parse_name_status(run_git(["diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r", "-z", expected_commit])) != EXPECTED_STATUS:
        fail("E_PERSISTENCE_DIFF")
    for path in EXACT_SEVEN:
        frozen = frozen_bytes(expected_commit, path)
        if frozen != read_transaction_bytes(path):
            fail("E_PERSISTENCE_BLOB", path)


def validate_source_text(path: str, source: str) -> None:
    tree = ast.parse(source, filename=path)
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    import_names = {name: name for name in ("argparse", "ast", "copy", "hashlib", "json", "math", "os", "pathlib", "subprocess", "sys", "tempfile")}
    import_names.update({"mpmath": "mp", "numpy": "np", "validate_phase068_step94": "contract"})
    imported_symbols = {"__future__": {"annotations"}, "fractions": {"Fraction"}, "functools": {"lru_cache"}, "pathlib": {"Path"}, "typing": {"Any"}}
    modules: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in import_names:
                    fail("E_SOURCE_IMPORT", path)
                binding = alias.asname or alias.name
                if binding != import_names[alias.name]:
                    fail("E_SOURCE_IMPORT_ALIAS", path)
                modules[binding] = alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module not in imported_symbols or any(alias.name not in imported_symbols[node.module] for alias in node.names):
                fail("E_SOURCE_IMPORT_SYMBOL", path)
            if any(alias.asname is not None for alias in node.names):
                fail("E_SOURCE_IMPORT_ALIAS", path)

    members = {
        "argparse": {"ArgumentParser", "Namespace"},
        "ast": {"AST", "Attribute", "Call", "Constant", "Expr", "FunctionDef", "Import", "ImportFrom", "Lambda", "List", "Load", "Name", "Starred", "Store", "dump", "iter_child_nodes", "parse", "walk"},
        "copy": {"deepcopy"}, "hashlib": {"sha256", "sha1"}, "json": {"dumps", "loads"},
        "math": {"sqrt", "atanh", "log", "isfinite"},
        "mpmath": {"workdps", "mpf", "exp", "log", "quad", "findroot", "atanh", "nstr", "sqrt"},
        "numpy": {"ndarray", "cos", "pi", "arange", "ones", "abs", "max", "sum", "exp", "where", "empty", "log", "log1p", "linspace", "sqrt", "mean", "trapezoid"},
        "pathlib": {"Path"}, "sys": {"dont_write_bytecode", "argv", "stderr"},
        "tempfile": {"TemporaryDirectory"},
        "validate_phase068_step94": {"ROOT", "MATRIX", "EXACT_SEVEN", "EXPECTED_STATUS", "ValidationError", "fail", "expect_error", "run_self_tests", "validate_source_guard", "validate_pre_json", "sha256"},
    }
    dangerous_names = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "globals", "locals", "vars", "open"}
    writers = {"open", "write", "write_bytes", "write_text", "rename", "mkdir", "rmdir", "touch", "unlink", "link", "fsync", "chmod", "lchmod", "symlink_to", "hardlink_to", "system", "popen", "tofile", "dump", "move", "move_into", "copy_into"}
    os_calls = {"open", "write", "fsync", "close", "link", "unlink"}
    # Pin the complete read-only subprocess dataflow, including argv validation,
    # to exclude argument reassignment, mutation, capture and altered options.
    git_reader_shape = ast.dump(ast.parse('''def run_git(args: list[str]) -> bytes:
    validate_git_argv(args)
    process = subprocess.run(["git", *args], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)
    if process.returncode:
        fail("E_GIT_EXEC", f"{args[0]}:{process.returncode}:{process.stderr.decode('utf-8', 'replace').strip()}")
    return process.stdout
''').body[0])

    def function_of(node: ast.AST) -> ast.FunctionDef | None:
        ancestor = parents.get(node)
        while ancestor is not None and not isinstance(ancestor, ast.FunctionDef):
            if isinstance(ancestor, ast.Lambda):
                return None
            ancestor = parents.get(ancestor)
        return ancestor

    def binary_flag_lookup(node: ast.Call) -> bool:
        return (path == BUILDER and isinstance(node.func, ast.Name) and node.func.id == "getattr"
                and len(node.args) == 3 and not node.keywords and isinstance(node.args[0], ast.Name)
                and node.args[0].id == "os" and isinstance(node.args[1], ast.Constant)
                and node.args[1].value == "O_BINARY" and isinstance(node.args[2], ast.Constant) and node.args[2].value == 0)

    for node in ast.walk(tree):
        parent = parents.get(node)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in dangerous_names and not (isinstance(parent, ast.Call) and parent.func is node and binary_flag_lookup(parent)):
                fail("E_SOURCE_CAPABILITY", path)
            if node.id.startswith("__") and node.id not in {"__name__", "__file__"}:
                fail("E_SOURCE_DUNDER", path)
            if node.id in modules and not (isinstance(parent, ast.Attribute) and parent.value is node):
                if not (isinstance(parent, ast.Call) and binary_flag_lookup(parent) and parent.args[0] is node):
                    fail("E_SOURCE_MODULE_CAPTURE", path)
        if isinstance(node, ast.Attribute) and node.attr.startswith("__") and not (node.attr == "__init__" and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "super"):
            fail("E_SOURCE_DUNDER", path)
        if not isinstance(node, ast.Attribute):
            continue
        module = modules.get(node.value.id) if isinstance(node.value, ast.Name) else None
        direct_call = isinstance(parent, ast.Call) and parent.func is node
        enclosing = function_of(node)
        if module == "os":
            if path != BUILDER or isinstance(node.ctx, ast.Store):
                fail("E_SOURCE_OS_CAPABILITY", path)
            if node.attr in os_calls:
                if not direct_call or enclosing is None or enclosing.name != "atomic_create":
                    fail("E_SOURCE_OS_CAPABILITY", path)
            elif node.attr not in {"O_WRONLY", "O_CREAT", "O_EXCL"}:
                fail("E_SOURCE_OS_CAPABILITY", path)
            continue
        if module == "subprocess":
            if node.attr == "run" and not direct_call:
                fail("E_SOURCE_SUBPROCESS_CAPTURE", path)
            if node.attr == "run":
                if path != VALIDATOR or enclosing is None or enclosing.name != "run_git":
                    fail("E_SOURCE_SUBPROCESS", path)
                if ast.dump(enclosing) != git_reader_shape:
                    fail("E_SOURCE_SUBPROCESS", path)
            elif node.attr not in {"DEVNULL", "PIPE"} or isinstance(node.ctx, ast.Store):
                fail("E_SOURCE_SUBPROCESS", path)
            continue
        if node.attr in writers and not (module == "ast" and node.attr == "dump"):
            fail("E_SOURCE_WRITER", path)
        if node.attr == "copy" and (not direct_call or parent.args or parent.keywords):
            # Existing array/dict copies have no arguments; Path.copy requires
            # a destination and captured copy methods are not permitted.
            fail("E_SOURCE_WRITER", path)
        if node.attr == "replace":
            # The only legal replace operation is byte-string newline
            # normalization with two literal byte arguments, not Path.replace.
            if not direct_call or len(parent.args) != 2 or parent.keywords or not all(isinstance(arg, ast.Constant) and isinstance(arg.value, bytes) for arg in parent.args):
                fail("E_SOURCE_WRITER", path)
        if module is not None:
            if module == "tempfile" and path != BUILDER:
                fail("E_SOURCE_WRITER", path)
            if node.attr not in members.get(module, set()):
                fail("E_SOURCE_MODULE_MEMBER", f"{path}:{module}.{node.attr}")
            if isinstance(node.ctx, ast.Store) and not (module == "sys" and node.attr == "dont_write_bytecode"):
                fail("E_SOURCE_MODULE_CAPTURE", path)
    if path == BUILDER:
        calls = [node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "os"]
        if calls.count("link") != 1 or set(calls) - {"open", "write", "fsync", "close", "link", "unlink"}:
            fail("E_BUILDER_WRITER")


def validate_source_guard() -> None:
    for path in (VALIDATOR, BUILDER):
        validate_source_text(path, (ROOT / path).read_text(encoding="utf-8"))


def expect_error(code: str, callback: Any) -> None:
    try:
        callback()
    except ValidationError as exc:
        if exc.code != code:
            fail("E_SELFTEST_WRONG_ERROR", f"{code}:{exc.code}")
        return
    fail("E_SELFTEST_ACCEPTED", code)


def run_transaction_fixture(responses: dict[tuple[str, ...], bytes], contents: dict[str, bytes], callback: Any) -> None:
    """Substitute only external readers; exercise the real validation functions."""
    global run_git, read_transaction_bytes
    saved_git, saved_read = run_git, read_transaction_bytes

    def fixture_git(args: list[str]) -> bytes:
        validate_git_argv(args)
        key = tuple(args)
        if key not in responses:
            fail("E_SELFTEST_UNDECLARED_GIT", str(key))
        return responses[key]

    def fixture_read(path: str) -> bytes:
        if path not in contents:
            fail("E_SELFTEST_UNDECLARED_PATH", path)
        return contents[path]

    try:
        run_git, read_transaction_bytes = fixture_git, fixture_read
        callback()
    finally:
        run_git, read_transaction_bytes = saved_git, saved_read


def run_transaction_self_tests() -> int:
    contents = {path: ("fixture:" + path + "\n").encode("utf-8") for path in EXACT_SEVEN}
    child, wrong = "1" * 40, "2" * 40
    status_key = ("status", "--porcelain=v1", "-z", "--untracked-files=all")
    diff_key = ("diff", "--cached", "--name-status", "--no-renames", "-z")
    index_key = ("ls-files", "--stage", "-z", "--", *EXACT_SEVEN)
    commit_diff_key = ("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r", "-z", child)
    live_key = ("ls-remote", "--refs", ORIGIN_URL, ACTIVE_REF)
    diff_rows = [(EXPECTED_STATUS[path] + "\0" + path + "\0").encode("utf-8") for path in EXACT_SEVEN]
    index_rows = [("100644 " + git_blob_oid(contents[path]) + " 0\t" + path + "\0").encode("utf-8") for path in EXACT_SEVEN]
    staged_rows = [(EXPECTED_STATUS[path] + "  " + path + "\0").encode("utf-8") for path in EXACT_SEVEN]
    unstaged_rows = [(("??" if EXPECTED_STATUS[path] == "A" else " M") + " " + path + "\0").encode("utf-8") for path in EXACT_SEVEN]
    replies = {
        status_key: b"", diff_key: b"".join(diff_rows), index_key: b"".join(index_rows),
        commit_diff_key: b"".join(diff_rows),
        ("config", "--get", "remote.origin.url"): ORIGIN_URL.encode("ascii"),
        ("rev-parse", "--abbrev-ref", "HEAD"): ACTIVE_BRANCH.encode("ascii"),
        ("rev-parse", "--abbrev-ref", "@{upstream}"): UPSTREAM.encode("ascii"),
        ("show", "-s", "--format=%P", child): EXPECTED_PARENT.encode("ascii"),
        ("show", "-s", "--format=%s", child): EXPECTED_SUBJECT.encode("ascii"),
        live_key: (child + "\t" + ACTIVE_REF + "\n").encode("ascii"),
    }
    for ref in ("HEAD", TRACKING_REF, "@{upstream}"):
        replies[("rev-parse", ref)] = child.encode("ascii")
    for local_ref, (remote_ref, oid) in FIXED_REFS.items():
        replies[("rev-parse", local_ref)] = oid.encode("ascii")
        replies[("ls-remote", "--refs", ORIGIN_URL, remote_ref)] = (oid + "\t" + remote_ref + "\n").encode("ascii")
    for path, raw in contents.items():
        oid = git_blob_oid(raw)
        replies[("ls-tree", "-l", child, "--", path)] = (f"100644 blob {oid} {len(raw)}\t{path}\n").encode("utf-8")
        replies[("cat-file", "blob", oid)] = raw
    original_replies, original_contents = replies.copy(), contents.copy()
    original_git, original_read = run_git, read_transaction_bytes

    def check(name: str, code: str | None, callback: Any, changes: dict[tuple[str, ...], bytes]) -> None:
        fixture_replies = {**replies, **changes}
        try:
            if code is None:
                run_transaction_fixture(fixture_replies, contents, callback)
            else:
                expect_error(code, lambda: run_transaction_fixture(fixture_replies, contents, callback))
        except ValidationError as exc:
            fail("E_SELFTEST_TRANSACTION", f"{name}:{exc.code}:{exc.detail}")
        finally:
            if run_git is not original_git or read_transaction_bytes is not original_read or replies != original_replies or contents != original_contents:
                fail("E_SELFTEST_FIXTURE_RESTORE", name)

    # Positive fixtures prove these replies reach the real validators before
    # any single-field mutation. They are not counted as negative controls.
    check("pre-json-six", None, lambda: validate_status(PRE_JSON_SIX, staged=False),
          {status_key: b"".join(row for path, row in zip(EXACT_SEVEN, unstaged_rows) if path != MATRIX)})
    check("unstaged-seven", None, lambda: validate_status(EXACT_SEVEN, staged=False), {status_key: b"".join(unstaged_rows)})
    check("staged-seven", None, lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: b"".join(staged_rows)})
    check("staged-index", None, validate_staged_index, {})
    check("refs", None, lambda: validate_refs(child), {})
    check("persistence", None, lambda: validate_persistence(child), {})
    cases = [
        ("status-extra-path", "E_TRANSACTION_STATUS", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: b"".join(staged_rows) + b" M Claude/undeclared.tex\0"}),
        ("status-wrong-code", "E_TRANSACTION_STATUS", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: ("M  " + BUILDER + "\0").encode() + b"".join(staged_rows[1:])}),
        ("status-missing-path", "E_TRANSACTION_STATUS", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: b"".join(staged_rows[1:])}),
        ("status-rename", "E_STATUS_PARSE", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: b"R  renamed\0original\0"}),
        ("status-delete", "E_TRANSACTION_STATUS", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: ("D  " + BUILDER + "\0").encode() + b"".join(staged_rows[1:])}),
        ("status-index-worktree-mismatch", "E_TRANSACTION_STATUS", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: b"".join(unstaged_rows)}),
        ("status-truncated", "E_STATUS_PARSE", lambda: validate_status(EXACT_SEVEN, staged=True), {status_key: b"".join(staged_rows)[:-1]}),
        ("diff-delete", "E_DIFF_PARSE", validate_staged_index, {diff_key: b"D\0deleted\0"}),
        ("diff-rename", "E_DIFF_PARSE", validate_staged_index, {diff_key: b"R100\0renamed\0"}),
        ("diff-duplicate", "E_DIFF_PARSE", validate_staged_index, {diff_key: b"".join(diff_rows) + diff_rows[0]}),
        ("staged-extra-path", "E_STAGED_DIFF", validate_staged_index, {diff_key: b"".join(diff_rows) + b"A\0Claude/undeclared.tex\0"}),
        ("staged-wrong-status", "E_STAGED_DIFF", validate_staged_index, {diff_key: ("M\0" + BUILDER + "\0").encode() + b"".join(diff_rows[1:])}),
        ("staged-missing-diff-path", "E_STAGED_DIFF", validate_staged_index, {diff_key: b"".join(diff_rows[1:])}),
        ("staged-wrong-mode", "E_STAGED_ENTRY", validate_staged_index, {index_key: b"100755" + b"".join(index_rows)[6:]}),
        ("staged-wrong-blob", "E_STAGED_BLOB", validate_staged_index, {index_key: ("100644 " + wrong + " 0\t" + BUILDER + "\0").encode() + b"".join(index_rows[1:])}),
        ("staged-conflict-stage", "E_STAGED_ENTRY", validate_staged_index, {index_key: ("100644 " + git_blob_oid(contents[BUILDER]) + " 1\t" + BUILDER + "\0").encode() + b"".join(index_rows[1:])}),
        ("staged-missing-index-path", "E_STAGED_COUNT", validate_staged_index, {index_key: b"".join(index_rows[1:])}),
        ("staged-duplicate-index-path", "E_STAGED_ENTRY", validate_staged_index, {index_key: b"".join(index_rows) + index_rows[0]}),
        ("refs-origin", "E_ORIGIN_URL", lambda: validate_refs(child), {("config", "--get", "remote.origin.url"): b"https://invalid.example/other.git"}),
        ("refs-branch", "E_BRANCH", lambda: validate_refs(child), {("rev-parse", "--abbrev-ref", "HEAD"): b"other"}),
        ("refs-upstream-name", "E_UPSTREAM", lambda: validate_refs(child), {("rev-parse", "--abbrev-ref", "@{upstream}"): b"origin/other"}),
        ("refs-live-cache-mismatch", "E_TRANSACTION_LIVE", lambda: validate_refs(child), {live_key: (wrong + "\t" + ACTIVE_REF + "\n").encode()}),
        ("refs-live-wrong-path", "E_LIVE_REF", lambda: validate_refs(child), {live_key: (child + "\trefs/heads/other\n").encode()}),
        ("persistence-invalid-oid", "E_EXPECTED_COMMIT", lambda: validate_persistence("not-an-oid"), {}),
        ("persistence-dirty", "E_PERSISTENCE_DIRTY", lambda: validate_persistence(child), {status_key: staged_rows[0]}),
        ("persistence-wrong-parent", "E_PERSISTENCE_PARENT", lambda: validate_persistence(child), {("show", "-s", "--format=%P", child): wrong.encode()}),
        ("persistence-merge-parent", "E_PERSISTENCE_PARENT", lambda: validate_persistence(child), {("show", "-s", "--format=%P", child): (EXPECTED_PARENT + " " + wrong).encode()}),
        ("persistence-wrong-subject", "E_PERSISTENCE_SUBJECT", lambda: validate_persistence(child), {("show", "-s", "--format=%s", child): b"wrong subject"}),
        ("persistence-extra-path", "E_PERSISTENCE_DIFF", lambda: validate_persistence(child), {commit_diff_key: b"".join(diff_rows) + b"A\0Claude/undeclared.tex\0"}),
        ("persistence-wrong-status", "E_PERSISTENCE_DIFF", lambda: validate_persistence(child), {commit_diff_key: ("M\0" + BUILDER + "\0").encode() + b"".join(diff_rows[1:])}),
        ("persistence-wrong-mode", "E_TREE_ENTRY", lambda: validate_persistence(child), {("ls-tree", "-l", child, "--", BUILDER): b"100755" + replies[("ls-tree", "-l", child, "--", BUILDER)][6:]}),
        ("persistence-live-cache-mismatch", "E_TRANSACTION_LIVE", lambda: validate_persistence(child), {live_key: (wrong + "\t" + ACTIVE_REF + "\n").encode()}),
    ]
    changed_blob = b"changed fixture\n"
    changed_oid = git_blob_oid(changed_blob)
    cases.append(("persistence-blob-worktree-mismatch", "E_PERSISTENCE_BLOB", lambda: validate_persistence(child), {
        ("ls-tree", "-l", child, "--", BUILDER): (f"100644 blob {changed_oid} {len(changed_blob)}\t{BUILDER}\n").encode(),
        ("cat-file", "blob", changed_oid): changed_blob}))
    for ref in ("HEAD", TRACKING_REF, "@{upstream}"):
        cases.append(("refs-local-" + ref, "E_TRANSACTION_REF", lambda: validate_refs(child), {("rev-parse", ref): wrong.encode()}))
    for local_ref, (remote_ref, _) in FIXED_REFS.items():
        cases.append(("refs-protected-local-" + local_ref, "E_FIXED_REF", lambda: validate_refs(child), {("rev-parse", local_ref): wrong.encode()}))
        cases.append(("refs-protected-live-" + remote_ref, "E_FIXED_REF", lambda: validate_refs(child), {
            ("ls-remote", "--refs", ORIGIN_URL, remote_ref): (wrong + "\t" + remote_ref + "\n").encode()}))
    if len({name for name, _, _, _ in cases}) != len(cases):
        fail("E_SELFTEST_DUPLICATE_NAME")
    for name, code, callback, changes in cases:
        check(name, code, callback, changes)
    return len(cases)


def run_self_tests(expected: dict[str, Any] | None = None) -> int:
    cases = [
        ("E_JSON_DUPLICATE_KEY", lambda: strict_json_loads(b'{"x":1,"x":2}', label="negative")),
        ("E_JSON_NONFINITE", lambda: strict_json_loads(b'{"x":NaN}', label="negative")),
        ("E_JSON_NONFINITE", lambda: strict_json_loads(b'{"x":1e999}', label="negative")),
        ("E_JSON_LIMIT", lambda: strict_json_loads(b"["*70+b"0"+b"]"*70, label="negative")),
        ("E_GIT_ARGV", lambda: validate_git_argv(["push", "origin", ACTIVE_BRANCH])),
        ("E_GIT_ARGV", lambda: validate_git_argv(["config", "--global", "user.name"])),
        ("E_GIT_ARGV", lambda: validate_git_argv(["ls-remote", "--refs", ORIGIN_URL, "refs/heads/undeclared"])),
        ("E_GIT_ARGV", lambda: validate_git_argv(["show", "--output=probe", TIP])),
        ("E_SOURCE_SUBPROCESS", lambda: validate_source_text(VALIDATOR, "import subprocess\nsubprocess.run(['git','push'])\n")),
        ("E_SOURCE_CAPABILITY", lambda: validate_source_text(VALIDATOR, "eval('1')\n")),
        ("E_SOURCE_DUNDER", lambda: validate_source_text(VALIDATOR, "x.__class__\n")),
        ("E_SOURCE_OS_CAPABILITY", lambda: validate_source_text(VALIDATOR, "import os\nos.system('PAYLOAD_NOT_EXECUTED')\n")),
        ("E_SOURCE_OS_CAPABILITY", lambda: validate_source_text(VALIDATOR, "import os\nos.write(1,b'PAYLOAD_NOT_EXECUTED')\n")),
        ("E_SOURCE_IMPORT_ALIAS", lambda: validate_source_text(VALIDATOR, "import subprocess as sp\nsp.run(['PAYLOAD_NOT_EXECUTED'])\n")),
        ("E_SOURCE_IMPORT_ALIAS", lambda: validate_source_text(VALIDATOR, "import os as alternate\nalternate.system('PAYLOAD_NOT_EXECUTED')\n")),
        ("E_SOURCE_IMPORT_ALIAS", lambda: validate_source_text(VALIDATOR, "from pathlib import Path as Alternate\nAlternate('unused').open('w')\n")),
        ("E_SOURCE_IMPORT_SYMBOL", lambda: validate_source_text(VALIDATOR, "from subprocess import run\nrun(['PAYLOAD_NOT_EXECUTED'])\n")),
        ("E_SOURCE_SUBPROCESS_CAPTURE", lambda: validate_source_text(VALIDATOR, "import subprocess\nrunner=subprocess.run\nrunner(['PAYLOAD_NOT_EXECUTED'])\n")),
        ("E_SOURCE_MODULE_CAPTURE", lambda: validate_source_text(VALIDATOR, "import subprocess\nsp=subprocess\nsp.run(['PAYLOAD_NOT_EXECUTED'])\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "from pathlib import Path\nPath('unused').open('w')\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "from pathlib import Path\nwriter=Path('unused').write_bytes\nwriter(b'PAYLOAD_NOT_EXECUTED')\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "from pathlib import Path\nwriter=Path('unused').open\nwriter('w')\n")),
        ("E_SOURCE_CAPABILITY", lambda: validate_source_text(VALIDATOR, "opener=open\nopener('unused','w')\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "import numpy as np\nnp.ones(1).tofile('unused')\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "import numpy as np\nnp.ones(1).dump('unused')\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "from pathlib import Path\nPath('unused').move('unused2')\n")),
        ("E_SOURCE_WRITER", lambda: validate_source_text(VALIDATOR, "from pathlib import Path\nPath('unused').copy('unused2')\n")),
        ("E_SOURCE_SUBPROCESS", lambda: validate_source_text(VALIDATOR, "import subprocess\ndef run_git(args):\n validate_git_argv(args)\n args=['push','origin','unused']\n subprocess.run(['git',*args],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,check=False)\n")),
    ]
    for code, callback in cases:
        expect_error(code, callback)
    if gap_halfwidth(-0.001) != 0 or gap_halfwidth(0) != 0:
        fail("E_SELFTEST_SUBCRITICAL")
    if abs(2*gap_halfwidth(0.001)-0.0387124138091) > 1e-10:
        fail("E_SELFTEST_BINODAL")
    analytic_derivation()
    tests = len(cases) + run_transaction_self_tests()
    if expected is not None:
        mutations = [
            ("E_MATRIX_SCHEMA", lambda x: x.update({"unknown": 1})),
            ("E_TRANSACTION_IDENTITY", lambda x: x.update({"expected_parent": BASE})),
            ("E_TRANSACTION_IDENTITY", lambda x: x.update({"required_commit_subject": "wrong"})),
            ("E_SOURCE_COVERAGE", lambda x: x["sources"].pop()),
            ("E_SOURCE_COVERAGE", lambda x: x["sources"][0].update({"mode": "100755"})),
            ("E_SOURCE_COVERAGE", lambda x: x["sources"][0].update({"coverage": [[2,253]]})),
            ("E_C1_LINEAR_NORM_INFERENCE", lambda x: x["analytic"].update({"c1_inferred_from_linear_norm_alone": True})),
            ("E_BINODAL_SIGN_OR_SERIES", lambda x: x["analytic"].update({"binodal_equation": "ln(theta/(1-theta))-a*(1-2*theta)=0"})),
            ("E_ONE_SIDED_PROPOSITIONS", lambda x: x["analytic"]["propositions"].pop(3)),
            ("E_EPSILON_NORMALIZATION", lambda x: x["normalization_defect"].update({"ratio_conversion": 1})),
            ("E_NUMERIC_EVIDENCE", lambda x: x["numeric"]["extension_rows"].pop()),
            ("E_NUMERIC_EVIDENCE", lambda x: x["numeric"]["normalization_rows"][0].update({"renormalized": True})),
            ("E_NUMERIC_EVIDENCE", lambda x: x["numeric"]["convergence_rows"].pop()),
            ("E_AUTHORITY_PROMOTION", lambda x: x["authority"].update({"canonical_theory": True})),
        ]
        before = canonical_bytes(expected)
        for code, mutation in mutations:
            modified = copy.deepcopy(expected)
            mutation(modified)
            modified["semantic_sha256"] = semantic_sha(modified)
            expect_error(code, lambda: validate_matrix_payload(modified, expected))
        if canonical_bytes(expected) != before:
            fail("E_SELFTEST_MUTATION_RESTORE")
        tests += len(mutations)
    return tests


def validate_pre_json() -> bytes:
    if (ROOT / MATRIX).exists():
        fail("E_MATRIX_EXISTS", MATRIX)
    validate_refs(EXPECTED_PARENT)
    validate_status(PRE_JSON_SIX, staged=False)
    validate_source_guard()
    validate_controls()
    expected = expected_matrix()
    run_self_tests(expected)
    raw = canonical_bytes(expected)
    validate_controls()
    if [file_identity(p) for p in PRE_JSON_SIX] != expected["pre_json_file_identities"]:
        fail("E_PRE_JSON_INPUT_CHANGED")
    validate_status(PRE_JSON_SIX, staged=False)
    validate_refs(EXPECTED_PARENT)
    return raw


def load_and_validate_matrix() -> tuple[dict[str, Any], bytes, int]:
    path = ROOT / MATRIX
    if not path.is_file():
        fail("E_MATRIX_MISSING", MATRIX)
    raw = path.read_bytes()
    value = strict_json_loads(raw, label=MATRIX)
    if canonical_bytes(value) != raw:
        fail("E_MATRIX_CANONICAL")
    expected = expected_matrix()
    validate_matrix_payload(value, expected)
    tests = run_self_tests(expected)
    return value, raw, tests


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    for mode in ("collect", "content-only", "verify-staged", "verify-persistence"):
        modes.add_argument("--"+mode, action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args(argv)
    if args.verify_persistence:
        if not is_hex40(args.expected_commit):
            parser.error("--verify-persistence requires --expected-commit <lowercase40>")
    elif args.expected_commit is not None:
        parser.error("--expected-commit is permitted only with --verify-persistence")
    return args


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
        if args.collect:
            raw = validate_pre_json()
            print(f"PASS_P068_STEP94_COLLECT bytes={len(raw)} sha256={sha256(raw)}")
            return 0
        if not (ROOT / MATRIX).is_file():
            fail("E_MATRIX_MISSING", MATRIX)
        if args.verify_persistence:
            validate_persistence(args.expected_commit)
        else:
            validate_refs(EXPECTED_PARENT)
            validate_status(EXACT_SEVEN, staged=args.verify_staged)
        validate_source_guard()
        validate_controls()
        value, raw, tests = load_and_validate_matrix()
        validate_controls()
        if args.verify_persistence:
            if parse_status():
                fail("E_PERSISTENCE_DIRTY_FINAL")
            validate_refs(args.expected_commit)
            terminal = PERSISTENCE_TERMINAL
        else:
            validate_status(EXACT_SEVEN, staged=args.verify_staged)
            if args.verify_staged:
                validate_staged_index()
            validate_refs(EXPECTED_PARENT)
            terminal = CONTENT_TERMINAL
        print(f"{terminal} sources={len(value['sources'])} propositions={len(value['analytic']['propositions'])} bytes={len(raw)} sha256={sha256(raw)} negative_controls={tests}")
        return 0
    except (ValidationError, OSError, ValueError, SyntaxError) as exc:
        code = exc.code if isinstance(exc, ValidationError) else "E_VALIDATION_IO_OR_PARSE"
        detail = exc.detail if isinstance(exc, ValidationError) else str(exc)
        print(f"FAIL_P068_STEP94 {code} {detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
