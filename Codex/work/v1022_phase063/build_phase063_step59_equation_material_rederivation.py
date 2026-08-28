#!/usr/bin/env python3
"""Build Phase 063 Step 59 equation/material rederivation evidence.

The builder reads frozen Git objects plus previously committed Codex audit
artifacts.  It does not import or execute the frozen production module, modify
Claude/**, contact the network, or grant external scientific authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[3]
BUILDER = Path(__file__).resolve()
TOPOLOGY = REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
PHASE057 = REPO / "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json"
PRIOR_STATMECH = REPO / "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json"
PRIOR_MATERIAL = REPO / "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_059_EQUATION_MATERIAL_REDERIVATION_RESULT.md"
OUTPUT = REPO / "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "2ccee1af3a59a3a1e5c9fe7192e4f916c454521a"
GATE = "PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS"
EVIDENCE_BEGIN = "<!-- P063_STEP59_DERIVATION_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P063_STEP59_DERIVATION_EVIDENCE_END -->"
R = 8.31446261815324
F = 96485.33212
KB = 1.380649e-23
H = 6.62607015e-34

DISPLAY_ENVS = ("equation", "align", "gather", "multline", "flalign", "alignat")
RELEVANT_PHASE057_NUMERIC_IDS = (
    100, 101, 106, 111, 112, 113, 114, 115, 116,
    118, 119, 120, 121, 122, 123, 126, 127,
    130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141,
    145, 146, 147, 148, 149, 150, 151,
    156, 157, 158, 159, 160, 161,
    165, 166, 167, 168, 169, 170, 171,
    183, 184, 185, 188, 189, 191,
)


class BuildError(RuntimeError):
    pass


def run_git(*args: str, binary: bool = False) -> bytes | str:
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
    value = run_git("show", f"{commit}:{path}", binary=True)
    assert isinstance(value, bytes)
    return value


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalized_bytes(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8", "strict")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def compact_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


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

    return json.loads(raw, object_pairs_hook=pairs_hook, parse_constant=reject_constant)


def strict_load(path: Path) -> Any:
    return strict_load_bytes(path.read_bytes())


def parse_manual_evidence() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise BuildError("Step 59 result must contain one derivation evidence block")
    block = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise BuildError("Step 59 evidence block must be a fenced JSON object")
    evidence = strict_load_bytes(block[len("```json\n"):-len("\n```")].encode("utf-8"))
    if not isinstance(evidence, dict):
        raise BuildError("Step 59 evidence root must be an object")
    return evidence, sha256(compact_bytes(evidence))


def source_identity(path: str, topology_by_path: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source = topology_by_path.get(path)
    if source is None:
        raise BuildError(f"reachable source absent from topology: {path}")
    raw = git_bytes(BASELINE, path)
    blob = run_git("rev-parse", f"{BASELINE}:{path}")
    assert isinstance(blob, str)
    if blob != source["blob_sha1"] or sha256(raw) != source["sha256"]:
        raise BuildError(f"frozen source identity drift: {path}")
    lines = raw.decode("utf-8", "strict").splitlines()
    if len(lines) != source["extent"]["lines"]:
        raise BuildError(f"frozen line extent drift: {path}")
    return {
        "source_id": source["source_id"],
        "path": path,
        "git_blob": blob,
        "raw_sha256": source["sha256"],
        "physical_lines": len(lines),
        "read_interval": [1, len(lines)],
        "read_state": "READ_FULL_IN_STEP58_REUSED_WITH_PINNED_IDENTITY",
    }


def begin_environment(stripped: str) -> tuple[str, str] | None:
    for base in DISPLAY_ENVS:
        for env in (base, base + "*"):
            token = rf"\begin{{{env}}}"
            if token in stripped:
                return env, rf"\end{{{env}}}"
    return None


def extract_display_equations(
    paths: list[str], topology_by_path: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        raw = git_bytes(BASELINE, path)
        lines = raw.decode("utf-8", "strict").splitlines()
        source = topology_by_path[path]
        index = 0
        source_ordinal = 0
        while index < len(lines):
            stripped = lines[index].strip()
            begin = begin_environment(stripped)
            if begin is not None:
                env, end_token = begin
                start = index
                cursor = index
                while cursor < len(lines) and end_token not in lines[cursor]:
                    cursor += 1
                if cursor >= len(lines):
                    raise BuildError(f"unterminated {env} at {path}:{index + 1}")
                end = cursor
            elif stripped == r"\[":
                env = "bracket"
                start = index
                cursor = index + 1
                while cursor < len(lines) and lines[cursor].strip() != r"\]":
                    cursor += 1
                if cursor >= len(lines):
                    raise BuildError(f"unterminated bracket display at {path}:{index + 1}")
                end = cursor
            else:
                index += 1
                continue

            source_ordinal += 1
            body = "\n".join(lines[start:end + 1]) + "\n"
            labels = re.findall(r"\\label\{([^{}]+)\}", body)
            rows.append({
                "equation_id": f"P063-EQ-{len(rows) + 1:04d}",
                "source_id": source["source_id"],
                "path": path,
                "git_blob": source["blob_sha1"],
                "start_line": start + 1,
                "end_line": end + 1,
                "line_count": end - start + 1,
                "environment": env,
                "source_ordinal": source_ordinal,
                "labels": labels,
                "body_sha256": sha256(body.encode("utf-8")),
                "body": body,
                "authority_ceiling": "FROZEN_DISPLAY_EQUATION_TEXT_ONLY",
            })
            index = end + 1
    return rows


def stable_logistic(z: float) -> float:
    """Return 1/(1+exp(z)) without overflow."""
    if z >= 0:
        e = math.exp(-z) if z < 745 else 0.0
        return e / (1.0 + e)
    e = math.exp(z) if z > -745 else 0.0
    return 1.0 / (1.0 + e)


def bisect(func: Any, lo: float, hi: float, iterations: int = 240) -> float:
    flo, fhi = func(lo), func(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        raise BuildError(f"unbracketed bisection: f(lo)={flo}, f(hi)={fhi}")
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        fmid = func(mid)
        if flo * fmid <= 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return (lo + hi) / 2.0


def grand_canonical_probe() -> dict[str, Any]:
    temperature = 298.15
    energies = [-4200.0, 1300.0, 7100.0]
    weights = [2.0, 3.0, 5.0]
    chemical_potential = 725.0
    theta = [stable_logistic((energy - chemical_potential) / (R * temperature)) for energy in energies]
    mean_n = sum(weight * occupancy for weight, occupancy in zip(weights, theta))
    variance_n = sum(weight * occupancy * (1.0 - occupancy) for weight, occupancy in zip(weights, theta))
    dmu = 1.0e-3

    def mean(mu: float) -> float:
        return sum(
            weight * stable_logistic((energy - mu) / (R * temperature))
            for weight, energy in zip(weights, energies)
        )

    finite_difference = (mean(chemical_potential + dmu) - mean(chemical_potential - dmu)) / (2.0 * dmu)
    analytic = variance_n / (R * temperature)
    return {
        "temperature_K": temperature,
        "energies_J_per_mol": energies,
        "site_multiplicities": weights,
        "chemical_potential_J_per_mol": chemical_potential,
        "grand_partition_formula": "Xi=product_j[1+exp(-(epsilon_j-mu)/(RT))]^M_j",
        "occupancy_formula": "theta_j=[1+exp((epsilon_j-mu)/(RT))]^-1",
        "mean_N": mean_n,
        "variance_N": variance_n,
        "analytic_dmeanN_dmu_mol_per_J": analytic,
        "finite_difference_dmeanN_dmu_mol_per_J": finite_difference,
        "absolute_response_error": abs(analytic - finite_difference),
        "strictness_rule": "positive weighted variance is sufficient for strict response; existence is a separate endpoint-image condition",
        "interaction_boundary": "the general equilibrium fluctuation identity survives interactions, but the Bernoulli sum and product partition do not",
    }


def regular_solution_probe() -> dict[str, Any]:
    temperature = 298.15
    omega = 3.0 * R * temperature

    def free_energy(x: float) -> float:
        return R * temperature * (x * math.log(x) + (1.0 - x) * math.log(1.0 - x)) + omega * x * (1.0 - x)

    def chemical_potential(x: float) -> float:
        return R * temperature * math.log(x / (1.0 - x)) + omega * (1.0 - 2.0 * x)

    discriminant = 1.0 - 2.0 * R * temperature / omega
    spinodal_lo = (1.0 - math.sqrt(discriminant)) / 2.0
    spinodal_hi = 1.0 - spinodal_lo
    binodal_lo = bisect(chemical_potential, 1.0e-10, spinodal_lo)
    binodal_hi = 1.0 - binodal_lo
    tangent_slope = (free_energy(binodal_hi) - free_energy(binodal_lo)) / (binodal_hi - binodal_lo)

    # Composite midpoint integral of mu over the coexistence interval.  In the
    # symmetric model this is the Maxwell equal-area residual at mu_coex=0.
    panels = 20_000
    dx = (binodal_hi - binodal_lo) / panels
    maxwell = sum(chemical_potential(binodal_lo + (i + 0.5) * dx) * dx for i in range(panels))
    center_curvature = R * temperature / (0.5 * 0.5) - 2.0 * omega
    return {
        "temperature_K": temperature,
        "Omega_J_per_mol": omega,
        "Omega_over_RT": omega / (R * temperature),
        "free_energy_formula": "g=RT[x ln x+(1-x)ln(1-x)]+Omega x(1-x)",
        "chemical_potential_formula": "mu=RT ln[x/(1-x)]+Omega(1-2x)",
        "curvature_formula": "dmu/dx=RT/[x(1-x)]-2Omega",
        "spinodal": [spinodal_lo, spinodal_hi],
        "binodal": [binodal_lo, binodal_hi],
        "critical_rule": "Omega=2RT at x=1/2",
        "common_tangent_slope_J_per_mol": tangent_slope,
        "maxwell_integral_J_per_mol": maxwell,
        "center_curvature_J_per_mol": center_curvature,
        "center_is_unstable": center_curvature < 0,
        "separation_rule": "binodal/common tangent is equilibrium coexistence; spinodal is local-stability loss; the interval between them is metastable, not an equilibrium hysteresis width",
    }


def equilibrium_peak_probe() -> dict[str, Any]:
    temperature = 298.15
    center = 0.113
    capacity_C = 3600.0

    def xi(voltage: float) -> float:
        return 1.0 / (1.0 + math.exp(-F * (voltage - center) / (R * temperature)))

    h = 1.0e-7
    fd_center = capacity_C * (xi(center + h) - xi(center - h)) / (2.0 * h)
    analytic_center = capacity_C * F / (4.0 * R * temperature)
    fwhm = 4.0 * math.acosh(math.sqrt(2.0)) * R * temperature / F
    return {
        "temperature_K": temperature,
        "center_V": center,
        "capacity_C": capacity_C,
        "analytic_peak_C_per_V": analytic_center,
        "finite_difference_peak_C_per_V": fd_center,
        "absolute_peak_error_C_per_V": abs(analytic_center - fd_center),
        "ideal_logistic_FWHM_V": fwhm,
        "area_rule": "integral(dQ/dV dV)=Q only for the normalized equilibrium response over its full voltage domain",
        "observation_rule": "instrument convolution acts on a response after the equilibrium derivative; empirical line shapes and finite-current memory are separate operators",
        "variance_rule": "variance adds under normalized independent finite-variance convolution; FWHM-in-quadrature is not a general convolution theorem",
    }


def tst_probe() -> dict[str, Any]:
    temperature = 298.15
    reference = temperature
    e0 = 41_000.0
    e1 = 6.5
    e2 = 0.018
    a = 1.4
    b = 175.0
    kappa = 0.41

    def delta_e(temp: float) -> float:
        dt = temp - reference
        return e0 + e1 * dt + 0.5 * e2 * dt * dt

    def delta_e_prime(temp: float) -> float:
        return e1 + e2 * (temp - reference)

    def ln_ratio(temp: float) -> float:
        return a * math.log(temp / reference) + b * (1.0 / temp - 1.0 / reference)

    def ln_ratio_prime(temp: float) -> float:
        return a / temp - b / (temp * temp)

    def ln_ratio_second(temp: float) -> float:
        return -a / (temp * temp) + 2.0 * b / (temp ** 3)

    def delta_g(temp: float) -> float:
        return delta_e(temp) - R * temp * ln_ratio(temp)

    def delta_h(temp: float) -> float:
        return (
            delta_e(temp) - temp * delta_e_prime(temp)
            + R * temp * temp * ln_ratio_prime(temp)
        )

    entropy = -delta_e_prime(temperature) + R * (
        ln_ratio(temperature) + temperature * ln_ratio_prime(temperature)
    )
    enthalpy = delta_h(temperature)
    heat_capacity = -temperature * e2 + R * (
        2.0 * temperature * ln_ratio_prime(temperature)
        + temperature * temperature * ln_ratio_second(temperature)
    )
    dt = 1.0e-3
    entropy_fd = -(delta_g(temperature + dt) - delta_g(temperature - dt)) / (2.0 * dt)
    heat_capacity_fd = (delta_h(temperature + dt) - delta_h(temperature - dt)) / (2.0 * dt)
    rate = kappa * KB * temperature / H * math.exp(ln_ratio(temperature)) * math.exp(
        -delta_e(temperature) / (R * temperature)
    )
    rate_hs = kappa * KB * temperature / H * math.exp(entropy / R) * math.exp(
        -enthalpy / (R * temperature)
    )
    return {
        "temperature_K": temperature,
        "kappa": kappa,
        "rate_formula": "k=kappa(k_B T/h)K_dagger exp[-DeltaE0/(RT)]",
        "delta_S_formula": "-DeltaE0_prime+R L+RT L_prime",
        "delta_H_formula": "DeltaE0-T DeltaE0_prime+RT^2 L_prime",
        "delta_Cp_formula": "-T DeltaE0_second+R(2T L_prime+T^2 L_second)",
        "delta_S_J_per_molK": entropy,
        "delta_S_finite_difference_J_per_molK": entropy_fd,
        "entropy_absolute_error": abs(entropy - entropy_fd),
        "delta_H_J_per_mol": enthalpy,
        "delta_Cp_J_per_molK": heat_capacity,
        "delta_Cp_finite_difference_J_per_molK": heat_capacity_fd,
        "heat_capacity_absolute_error": abs(heat_capacity - heat_capacity_fd),
        "rate_partition_form_per_s": rate,
        "rate_enthalpy_entropy_form_per_s": rate_hs,
        "rate_roundtrip_relative_error": abs(rate - rate_hs) / rate,
        "scope_rule": "equilibrium TST does not by itself derive electrode overpotential, phase-boundary kinetics, empirical tail width, or current memory",
    }


def blend_probe() -> dict[str, Any]:
    temperature = 298.15
    capacities = [0.72, 0.28]
    centers = [0.105, 0.285]
    target = 0.43

    def host_xi(voltage: float, center: float) -> float:
        return 1.0 / (1.0 + math.exp(-F * (voltage - center) / (R * temperature)))

    def residual(voltage: float) -> float:
        return sum(q * host_xi(voltage, center) for q, center in zip(capacities, centers)) - target * sum(capacities)

    root = bisect(residual, -1.0, 1.0)
    occupancies = [host_xi(root, center) for center in centers]
    derivative = F / (R * temperature) * sum(
        q * value * (1.0 - value) for q, value in zip(capacities, occupancies)
    )
    h = 1.0e-7
    derivative_fd = (residual(root + h) - residual(root - h)) / (2.0 * h)

    mass_fraction_si = 0.10
    q_si_Ah_per_g = 3.20
    q_graphite_Ah_per_g = 0.350
    utilization_si = 0.82
    utilization_graphite = 0.96
    numerator = mass_fraction_si * q_si_Ah_per_g * utilization_si
    denominator = numerator + (1.0 - mass_fraction_si) * q_graphite_Ah_per_g * utilization_graphite
    capacity_fraction_si = numerator / denominator
    return {
        "temperature_K": temperature,
        "host_capacity_weights": capacities,
        "host_center_V": centers,
        "target_total_fraction": target,
        "common_potential_root_V": root,
        "charge_balance_residual": residual(root),
        "analytic_dresidual_dV_per_V": derivative,
        "finite_difference_dresidual_dV_per_V": derivative_fd,
        "absolute_derivative_error": abs(derivative - derivative_fd),
        "unique_root_sufficient_conditions": "continuous host xi_hj(V), positive aggregate derivative on the bracket, and target within endpoint image",
        "finite_current_boundary": "common equilibrium potential does not imply equal host current or synchronized local overpotential at finite rate",
        "mass_fraction_si": mass_fraction_si,
        "specific_capacity_si_Ah_per_g": q_si_Ah_per_g,
        "specific_capacity_graphite_Ah_per_g": q_graphite_Ah_per_g,
        "utilization_si": utilization_si,
        "utilization_graphite": utilization_graphite,
        "capacity_fraction_si": capacity_fraction_si,
        "capacity_fraction_formula": "f_Si=m_Si q_Si u_Si/[m_Si q_Si u_Si+(1-m_Si)q_G u_G]",
        "basis_rule": "mass fraction and capacity fraction are unequal unless specific capacity and all active/utilization/ICE bases are explicitly aligned",
    }


def finite_current_probe() -> dict[str, Any]:
    temperature = 298.15
    c_rate_per_hour = 1.0
    c_rate_per_second = c_rate_per_hour / 3600.0
    barrier = R * temperature * math.log(3600.0)
    molar_volume = 1.25e-5
    stress = 1.0e9
    shift = molar_volume * stress / F
    return {
        "temperature_K": temperature,
        "c_rate_per_hour": c_rate_per_hour,
        "c_rate_per_second": c_rate_per_second,
        "conversion_factor": 3600.0,
        "lag_if_hour_number_used_directly_over_SI_lag": 3600.0,
        "RT_ln_3600_J_per_mol": barrier,
        "barrier_direction": "correcting the direct h^-1 numerical use to s^-1 lowers inferred k by 3600 and raises an Arrhenius-inferred barrier by RT ln(3600)",
        "larche_cahn_molar_volume_m3_per_mol": molar_volume,
        "stress_Pa": stress,
        "stress_potential_shift_V": shift,
        "stress_coefficient_V_per_Pa": molar_volume / F,
        "stress_dimension_rule": "partial molar volume times stress is J/mol; division by F gives V",
        "path_rule": "a reversible single-valued stress-composition shift alone produces no closed-cycle hysteresis; plastic/damage/path-history closure is separate",
        "operator_boundary": "arbitrary cut/cap/frozen-local is an approximation operator, not full simultaneous host-specific kinetic evolution",
    }


def load_prior(path: Path, expected_gate: str) -> dict[str, Any]:
    data = strict_load(path)
    if not isinstance(data, dict) or data.get("gate") != expected_gate:
        raise BuildError(f"prior audit gate drift: {path.relative_to(REPO).as_posix()}")
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": sha256(path.read_bytes()),
        "semantic_sha256": data.get("semantic_sha256"),
        "gate": data["gate"],
        "authority_ceiling": "PRIOR_INTERNAL_AUDIT_ROUTE_ONLY",
    }


def semantic_projection(data: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(data)
    projected.pop("semantic_sha256", None)
    return projected


def build() -> dict[str, Any]:
    topology = strict_load(TOPOLOGY)
    phase057 = strict_load(PHASE057)
    evidence, evidence_sha = parse_manual_evidence()
    if topology.get("gate") != "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY":
        raise BuildError("Step 58 topology gate drift")
    if topology.get("baseline_commit") != BASELINE:
        raise BuildError("Step 58 topology baseline drift")
    topology_by_path = {row["path"]: row for row in topology["sources"]}
    reachable = sorted({
        path
        for route in topology["citation_genealogy"]["root_routes"]
        for path in route["reachable_tex_paths"]
    })
    if len(reachable) != 53:
        raise BuildError(f"reachable TeX denominator drift: {len(reachable)}")
    source_rows = [source_identity(path, topology_by_path) for path in reachable]
    equation_rows = extract_display_equations(reachable, topology_by_path)
    if len(equation_rows) != 231:
        raise BuildError(f"display equation denominator drift: {len(equation_rows)}")

    phase057_records = {row["numeric_id"]: row for row in phase057["records"]}
    selected_phase057 = []
    for numeric_id in RELEVANT_PHASE057_NUMERIC_IDS:
        row = phase057_records.get(numeric_id)
        if row is None:
            raise BuildError(f"missing Phase 057 route {numeric_id}")
        selected_phase057.append({
            **row,
            "route_state": "RETAINED_PROVISIONAL_NOT_PROMOTED",
            "external_truth_promoted": False,
            "downstream_owner": "Step 59 internal adjudication; Step 60 external authority; Phase 074+ canonical repair",
        })

    findings = evidence.get("findings")
    if not isinstance(findings, list):
        raise BuildError("manual evidence findings must be a list")
    finding_summary = dict(sorted(Counter(row["priority"] for row in findings).items()))
    data: dict[str, Any] = {
        "schema_version": 1,
        "artifact_kind": "V1022_EQUATION_MATERIAL_REDERIVATION",
        "generated_date": "2026-08-29",
        "phase": 63,
        "step": 59,
        "status": "PASS_WITH_CONCERNS",
        "gate": GATE,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "builder": {
            "path": BUILDER.relative_to(REPO).as_posix(),
            "normalized_sha256": sha256(normalized_bytes(BUILDER)),
        },
        "input_artifacts": {
            "step58_topology": {
                "path": TOPOLOGY.relative_to(REPO).as_posix(),
                "sha256": sha256(TOPOLOGY.read_bytes()),
                "semantic_sha256": sha256(compact_bytes({
                    key: value for key, value in topology.items()
                    if key != "semantic_sha256"
                })),
                "gate": topology["gate"],
            },
            "phase057_ledger": {
                "path": PHASE057.relative_to(REPO).as_posix(),
                "sha256": sha256(PHASE057.read_bytes()),
                "finding_count": phase057["finding_count"],
            },
            "prior_internal_audits": [
                load_prior(PRIOR_STATMECH, "PASS_P062_STEP53_STATMECH_TST_REDERIVATION"),
                load_prior(PRIOR_MATERIAL, "PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS"),
            ],
        },
        "result_first_contract": {
            "result_path": RESULT.relative_to(REPO).as_posix(),
            "evidence_semantic_sha256": evidence_sha,
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "persistence_claimed": False,
            "step60_blocked_until": "PASS_P063_STEP59_PERSISTENCE",
        },
        "counts": {
            "reachable_tex_sources": len(source_rows),
            "display_equations": len(equation_rows),
            "display_environment_counts": dict(sorted(Counter(row["environment"] for row in equation_rows).items())),
            "labeled_display_equations": sum(bool(row["labels"]) for row in equation_rows),
            "phase057_routes": len(selected_phase057),
            "manual_derivation_rows": len(evidence.get("derivation_rows", [])),
            "manual_sign_rows": len(evidence.get("sign_ledger", [])),
            "manual_operator_rows": len(evidence.get("operator_ledger", [])),
            "manual_material_rows": len(evidence.get("material_scope_ledger", [])),
            "findings": len(findings),
        },
        "source_inventory": source_rows,
        "display_equation_inventory": equation_rows,
        "manual_rederivation_evidence": evidence,
        "numeric_rederivation": {
            "grand_canonical": grand_canonical_probe(),
            "regular_solution": regular_solution_probe(),
            "equilibrium_peak": equilibrium_peak_probe(),
            "transition_state_theory": tst_probe(),
            "blend_and_capacity_basis": blend_probe(),
            "finite_current_mechanics": finite_current_probe(),
        },
        "phase057_provisional_routes": selected_phase057,
        "findings": findings,
        "finding_summary": finding_summary,
        "authority_boundary": {
            "frozen_source_modified": False,
            "production_module_imported_or_executed": False,
            "external_scientific_truth_validated": False,
            "external_material_truth_validated": False,
            "external_experimental_truth_validated": False,
            "primary_literature_truth_validated": False,
            "canonical_equation_accepted": False,
            "final_manuscript_ready": False,
            "scope": "frozen internal equations, assumptions, signs, dimensions, limits, material scopes and downstream correction routes",
        },
    }
    data["semantic_sha256"] = sha256(compact_bytes(semantic_projection(data)))
    return data


def output_path(output_dir: str | None) -> Path:
    if output_dir is None:
        return OUTPUT
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return directory / OUTPUT.name


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    data = build()
    path = output_path(args.output_dir)
    path.write_bytes(pretty_bytes(data))
    print(
        "PASS_P063_STEP59_BUILD "
        f"sources={data['counts']['reachable_tex_sources']} "
        f"equations={data['counts']['display_equations']} "
        f"derivations={data['counts']['manual_derivation_rows']} "
        f"findings={data['counts']['findings']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
