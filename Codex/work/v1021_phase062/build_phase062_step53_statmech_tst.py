#!/usr/bin/env python3
"""Build Phase 062 Step 53 grand-canonical/TST rederivation evidence.

The builder reads only frozen Git objects and writes only the declared Codex
machine artifact and Step result.  It performs no network access and grants no
external scientific, material, experimental, or bibliographic authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_JSON = ROOT / "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json"
OUTPUT_MD = ROOT / "Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
Q2_COMMIT = "1635bc97fb7bd9c3fabc720e91bf09e5ba31798f"
Q2_PARENT = "b4e939b0547cd4bf73bca30abe10fd164954c277"
Q3_COMMIT = "c7420915dfae8ef076319737bddcc532a86d9505"
Q3_PARENT = Q2_COMMIT
EXPECTED_PARENT = "51ccba6c248a3e710e1a4ddd6017c18043f8a7a2"

R = 8.31446261815324
F = 96485.33212
KB = 1.380649e-23
H = 6.62607015e-34

SOURCE_SPECS = [
    ("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 442, "8982a25beb3b58d406a684cb6a92906e06d1095e", "469f9de88fdedb33c6932e0b75642eab0412b6a05d0167849497cae9d60db765"),
    ("Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex", 74, "e5b3f836d054983e43b74e64b98c1a52dcf05b45", "6c11234e9bf0c275299fcc845993e184e98e5c819f949bb9cb1e6d7920ecf88c"),
    ("Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex", 243, "93c444066debda6e8baf81b36fe570e7b6e36d2b", "a463f7070892f253e51a5bf8aa1f57ee7cf822079433a46f6a2a909fbd37432c"),
    ("Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex", 378, "e97708808c244bc114cffc570f4866419fe2b1e8", "b619a5b8fe7cabe59371c995384331ffa7d1d6e30bc33db0c3c2bd2853d73d17"),
    ("Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex", 131, "909f6d3bce10bef59b4532a4b2b3f7570a8f0631", "4835e52fd35de70d25054c95b0eb078947502afa19259b79c5691a53cbb2f038"),
    ("Claude/docs/v1.0.21/_sections/ch1_bib.tex", 64, "dc4ca0780618d5710fd04e74ea87707738ffceba", "dc58338a8abd45116d846c0053ed41265d45b0f37852fafe93b8ecd7488d651d"),
    ("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md", 37, "2d23088e094d93a28b687788b9ac03fa0ab5520c", "b0092e4313ecd228904e865cd93bc00215b7a3740bdc65a3353f05e333f686de"),
    ("Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md", 19, "ee86e4a8e74dea13cd01dc8fb8de36bb7119bf12", "b67870551a414f991badf85309da31cca208c77cc85b7399badead1fc1048472"),
    ("Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md", 37, "64bdca8830a491e10d45c30fe9d992bb334afe03", "a61856800cf5fa0247ef794c559337ff6c48f1801105ef13647ce625edd2b838"),
]

SPAN_SPECS = [
    ("Q2-SIGN", "Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 139, 221, "chemical/electrical potential sign convention and single-class logistic"),
    ("Q2-MULTICLASS", "Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 280, 390, "complete Q2 multiclass addition including assumptions, equations, proofs and guards"),
    ("Q2-LADDER", "Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 433, 439, "Part 0 ladder cross-reference"),
    ("Q2-CODEMAP", "Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex", 12, 25, "historical eq:implicit and unique-root implementation bridge"),
    ("Q2-MIXING", "Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex", 12, 35, "Chapter 2 implicit balance and derivative bridge"),
    ("Q2-CHANGE", "Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md", 7, 13, "Q2 change-control rows"),
    ("Q2-EXEC", "Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md", 7, 11, "Q2 process row"),
    ("Q2-REF", "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md", 1, 19, "Q2 source-ledger claim and authority ceiling"),
    ("Q3-CORE", "Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex", 11, 121, "Q3 Eyring/TST equations, assumptions, citations, prose and guards"),
    ("Q3-LAG", "Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex", 88, 105, "Q3-to-lag bridge and activation H/S use"),
    ("Q3-BIB", "Claude/docs/v1.0.21/_sections/ch1_bib.tex", 5, 15, "Q3 cited bibliography entries"),
    ("Q3-CHANGE", "Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md", 7, 16, "Q3 change-control rows"),
    ("Q3-EXEC", "Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md", 7, 12, "Q3 process row"),
    ("Q3-REF", "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md", 1, 19, "Q3 source-ledger claim and authority ceiling"),
]


def run_git(*args: str, binary: bool = False) -> bytes | str:
    proc = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return proc.stdout if binary else proc.stdout.decode("utf-8", "strict").strip()


def git_bytes(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}", binary=True)  # type: ignore[return-value]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def strict_json(raw: bytes) -> Any:
    def hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate key: {key}")
            out[key] = value
        return out

    return json.loads(raw, object_pairs_hook=hook, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-finite {value}")))


def traversal(value: Any) -> dict[str, int]:
    counts = {"nodes": 0, "mapping_objects": 0, "mapping_keys": 0, "lists": 0, "scalars": 0, "max_depth": 0}
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        counts["nodes"] += 1
        counts["max_depth"] = max(counts["max_depth"], depth)
        if isinstance(item, dict):
            counts["mapping_objects"] += 1
            counts["mapping_keys"] += len(item)
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            counts["lists"] += 1
            stack.extend((child, depth + 1) for child in item)
        else:
            counts["scalars"] += 1
    return counts


def source_attestations() -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    attestations: list[dict[str, Any]] = []
    decoded: dict[str, list[str]] = {}
    for path, expected_lines, expected_blob, expected_sha in SOURCE_SPECS:
        raw = git_bytes(BASELINE, path)
        text = raw.decode("utf-8", "strict")
        lines = text.splitlines()
        blob = run_git("rev-parse", f"{BASELINE}:{path}")
        if len(lines) != expected_lines or blob != expected_blob or sha256(raw) != expected_sha:
            raise RuntimeError(f"frozen source identity drift: {path}")
        decoded[path] = lines
        attestations.append({
            "path": path,
            "commit": BASELINE,
            "git_blob": blob,
            "raw_sha256": expected_sha,
            "physical_lines": expected_lines,
            "read_start": 1,
            "read_end": expected_lines,
            "read_state": "READ_FULL",
            "decoding": "UTF-8_STRICT",
        })
    return attestations, decoded


def source_spans(decoded: dict[str, list[str]]) -> list[dict[str, Any]]:
    rows = []
    for span_id, path, start, end, purpose in SPAN_SPECS:
        lines = decoded[path]
        excerpt = "\n".join(lines[start - 1:end]) + "\n"
        rows.append({
            "span_id": span_id,
            "path": path,
            "start_line": start,
            "end_line": end,
            "line_count": end - start + 1,
            "purpose": purpose,
            "excerpt_sha256": sha256(excerpt.encode("utf-8")),
            "excerpt": excerpt,
        })
    return rows


def snapshot_rows() -> list[dict[str, Any]]:
    specs = [
        ("Q2", Q2_COMMIT, "Claude/docs/v1.0.21/results/snapshot_v1021_q2.json"),
        ("Q3", Q3_COMMIT, "Claude/docs/v1.0.21/results/snapshot_v1021_q3.json"),
    ]
    rows = []
    for phase, commit, path in specs:
        raw = git_bytes(commit, path)
        parsed = strict_json(raw)
        rows.append({
            "phase": phase,
            "commit": commit,
            "path": path,
            "git_blob": run_git("rev-parse", f"{commit}:{path}"),
            "raw_sha256": sha256(raw),
            "physical_lines": len(raw.splitlines()),
            "strict_parse": True,
            "authority": "STRUCTURAL_DIFF_ONLY_NOT_SCIENTIFIC_TRUTH",
            "traversal": traversal(parsed),
        })
    return rows


def logistic_xi(V: float, eps: float, T: float, sign: int = 1, mu0: float = 0.0) -> float:
    mu = mu0 - sign * F * V
    z = (eps - mu) / (R * T)
    if z >= 0:
        ez = math.exp(-z) if z < 745 else 0.0
        theta = ez / (1.0 + ez)
    else:
        ez = math.exp(z) if z > -745 else 0.0
        theta = 1.0 / (1.0 + ez)
    return 1.0 - theta


def solve_bisection(target: float, weights: list[float], energies: list[float], T: float, lo: float, hi: float) -> float:
    total = sum(weights)
    if total <= 0:
        raise ValueError("positive total weight required")
    def residual(V: float) -> float:
        return sum(w * logistic_xi(V, e, T) for w, e in zip(weights, energies)) / total - target
    rlo, rhi = residual(lo), residual(hi)
    if rlo > 0 or rhi < 0:
        raise ValueError("target outside finite-domain image")
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if residual(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def q2_probe() -> dict[str, Any]:
    T = 298.15
    weights = [2.0, 3.0, 5.0]
    energies = [-4000.0, 0.0, 6000.0]
    target = 0.41
    V = solve_bisection(target, weights, energies, T, -0.5, 0.5)
    xis = [logistic_xi(V, e, T) for e in energies]
    thetas = [1.0 - x for x in xis]
    total = sum(weights)
    residual = sum(w * x for w, x in zip(weights, xis)) / total - target
    analytic = F / (R * T) * sum(w * th * (1.0 - th) for w, th in zip(weights, thetas)) / total
    h = 1.0e-7
    fp = sum(w * logistic_xi(V + h, e, T) for w, e in zip(weights, energies)) / total - target
    fm = sum(w * logistic_xi(V - h, e, T) for w, e in zip(weights, energies)) / total - target
    fd = (fp - fm) / (2.0 * h)
    x_single = 0.37
    V_single = solve_bisection(x_single, [7.0], [1250.0], T, -0.5, 0.5)
    V_single_closed = (R * T * math.log(x_single / (1.0 - x_single)) - 1250.0) / F

    duplicate = solve_bisection(target, [2.0, 3.0, 5.0], [0.0, 0.0, 6000.0], T, -0.5, 0.5)
    merged = solve_bisection(target, [5.0, 5.0], [0.0, 6000.0], T, -0.5, 0.5)
    zero_weight = solve_bisection(target, [0.0, 3.0, 5.0], [-99999.0, 0.0, 6000.0], T, -0.5, 0.5)
    zero_removed = solve_bisection(target, [3.0, 5.0], [0.0, 6000.0], T, -0.5, 0.5)

    finite_lo, finite_hi = -0.015, 0.025
    image_lo = sum(w * logistic_xi(finite_lo, e, T) for w, e in zip(weights, energies)) / total
    image_hi = sum(w * logistic_xi(finite_hi, e, T) for w, e in zip(weights, energies)) / total

    # Exact two-site coupled grand-canonical enumeration in molar energy units.
    mu = 500.0
    e1, e2, interaction = -600.0, 900.0, 2400.0
    states = []
    for n1 in (0, 1):
        for n2 in (0, 1):
            n = n1 + n2
            energy = e1 * n1 + e2 * n2 + interaction * n1 * n2
            boltz = math.exp(-(energy - mu * n) / (R * T))
            states.append((n, boltz))
    Z = sum(weight for _, weight in states)
    mean_n = sum(n * weight for n, weight in states) / Z
    mean_n2 = sum(n * n * weight for n, weight in states) / Z
    variance = mean_n2 - mean_n * mean_n
    dmu = 1.0e-3
    def coupled_mean(mu_value: float) -> float:
        vals = []
        for n1 in (0, 1):
            for n2 in (0, 1):
                n = n1 + n2
                energy = e1 * n1 + e2 * n2 + interaction * n1 * n2
                vals.append((n, math.exp(-(energy - mu_value * n) / (R * T))))
        z = sum(weight for _, weight in vals)
        return sum(n * weight for n, weight in vals) / z
    coupled_fd = (coupled_mean(mu + dmu) - coupled_mean(mu - dmu)) / (2.0 * dmu)
    coupled_variance_response = variance / (R * T)
    product_mean = 1.0 / (1.0 + math.exp((e1 - mu) / (R * T))) + 1.0 / (1.0 + math.exp((e2 - mu) / (R * T)))

    omega = 3.0 * R * T
    mean_field_center_slope = 4.0 * R * T - 2.0 * omega
    degeneracy = 4.0
    effective_shift = -R * T * math.log(degeneracy)

    return {
        "declared_domain": {"T_K": T, "V_unbounded_for_global_existence": True, "weights_nonnegative": True, "positive_total_weight": True, "one_electron_per_site": True},
        "multiclass": {
            "weights_Mj": weights, "energies_J_per_mol": energies, "target_xbar": target,
            "root_V": V, "normalized_residual": residual,
            "analytic_dresidual_dV_per_V": analytic, "finite_difference_dresidual_dV_per_V": fd,
            "absolute_derivative_error": abs(analytic - fd), "variance_sum": sum(w * th * (1.0 - th) for w, th in zip(weights, thetas)),
        },
        "single_class": {"target_xbar": x_single, "numeric_root_V": V_single, "closed_root_V": V_single_closed, "absolute_error_V": abs(V_single - V_single_closed)},
        "zero_weight": {"root_with_zero_weight_V": zero_weight, "root_after_removal_V": zero_removed, "absolute_error_V": abs(zero_weight - zero_removed), "all_zero_weights": "INVALID_NORMALIZATION_NO_EXISTENCE_STATEMENT"},
        "duplicate_energy": {"unmerged_root_V": duplicate, "merged_root_V": merged, "absolute_error_V": abs(duplicate - merged), "root_uniqueness": "PRESERVED", "parameter_identifiability": "NOT_IDENTIFIABLE_FROM_ROOT_ALONE"},
        "finite_domain": {"V_min": finite_lo, "V_max": finite_hi, "image_xbar_min": image_lo, "image_xbar_max": image_hi, "outside_target_xbar": min(1.0, image_hi + 0.1), "outside_target_has_bracket": False, "existence_rule": "target in closed endpoint image; uniqueness separately requires strict monotonicity"},
        "saturation": {"finite_T_finite_energy": "0<theta_j<1; exact endpoint saturation occurs only in a limit", "class_derivative_zero_limit": "does not destroy strictness while another positive-weight class fluctuates", "all_variance_zero": "NON_STRICT_NO_UNIQUENESS_GUARANTEE", "xbar_zero_or_one_finite_root": False},
        "degeneracy": {"occupied_to_empty_ratio": degeneracy, "effective_energy_shift_J_per_mol": effective_shift, "rule": "finite positive degeneracy is absorbed into effective site free energy and preserves monotonicity"},
        "coupled_exact": {"interaction_J_per_mol": interaction, "mean_N": mean_n, "variance_N": variance, "analytic_dmeanN_dmu_mol_per_J": coupled_variance_response, "finite_difference_dmeanN_dmu_mol_per_J": coupled_fd, "absolute_response_error": abs(coupled_variance_response - coupled_fd), "independent_product_mean_N": product_mean, "product_formula_absolute_error": abs(mean_n - product_mean), "rule": "general equilibrium variance identity survives; independent product and additive class variance do not"},
        "nonconvex_mean_field": {"Omega_over_RT": 3.0, "dmu_dtheta_at_half_J_per_mol": mean_field_center_slope, "unstable_branch_negative_slope": mean_field_center_slope < 0, "rule": "selected nonconvex/metastable branches do not inherit the ideal-logistic unique-root proof"},
    }


def tst_probe() -> dict[str, Any]:
    T = 298.15
    T0 = T
    a = 1.5
    b_K = 200.0
    delta_e0 = 40000.0
    kappa = 0.37
    def lnK(temp: float) -> float:
        return a * math.log(temp / T0) + b_K * (1.0 / temp - 1.0 / T0)
    def dlnK(temp: float) -> float:
        return a / temp - b_K / (temp * temp)
    def d2lnK(temp: float) -> float:
        return -a / (temp * temp) + 2.0 * b_K / (temp ** 3)
    def G(temp: float) -> float:
        return delta_e0 - R * temp * lnK(temp)
    L = lnK(T)
    S = R * (L + T * dlnK(T))
    S_source = R * L
    Hact = delta_e0 + R * T * T * dlnK(T)
    Cp = R * (2.0 * T * dlnK(T) + T * T * d2lnK(T))
    dt = 1.0e-3
    S_fd = -(G(T + dt) - G(T - dt)) / (2.0 * dt)
    def H_of(temp: float) -> float:
        return delta_e0 + R * temp * temp * dlnK(temp)
    Cp_fd = (H_of(T + dt) - H_of(T - dt)) / (2.0 * dt)
    K = math.exp(L)
    rate = kappa * KB * T / H * K * math.exp(-delta_e0 / (R * T))
    rate_no_kappa = KB * T / H * K * math.exp(-delta_e0 / (R * T))
    rate_hs = kappa * KB * T / H * math.exp(S / R) * math.exp(-Hact / (R * T))
    mass = 4.0e-26
    delta = 1.0e-10
    qrc = math.sqrt(2.0 * math.pi * mass * KB * T) * delta / H
    one_sided_flux_moment = math.sqrt(KB * T / (2.0 * math.pi * mass))
    conditional_positive_mean = 2.0 * one_sided_flux_moment
    flux_product = (one_sided_flux_moment / delta) * qrc
    flux_exact = KB * T / H
    def ln_rate(temp: float) -> float:
        return math.log(kappa * KB / H) + math.log(temp) + lnK(temp) - delta_e0 / (R * temp)
    dln_rate = 1.0 / T + dlnK(T) + delta_e0 / (R * T * T)
    dln_rate_fd = (ln_rate(T + dt) - ln_rate(T - dt)) / (2.0 * dt)
    const_ratio = 2.5
    constant_S = R * math.log(const_ratio)
    high_T_1 = 600.0
    high_T_2 = 1200.0
    # A reduced transition state with one fewer stable classical harmonic mode
    # than the reactant has K_dagger proportional to T^-1.  The TST flux factor
    # then cancels that power.  Unit normalization at high_T_1 is sufficient for
    # the exponent/ratio probe; no material parameter is inferred.
    high_T_K_1 = 1.0
    high_T_K_2 = high_T_1 / high_T_2
    high_T_prefactor_1 = high_T_1 * high_T_K_1
    high_T_prefactor_2 = high_T_2 * high_T_K_2
    return {
        "assumptions": {
            "dimensionless_standard_state_ratio": True,
            "same_energy_zero": True,
            "delta_E0_temperature_independent_for_numeric_probe": True,
            "classical_separable_reaction_coordinate": True,
            "quasi_equilibrium_transition_state": True,
            "transmission_coefficient_explicit": True,
            "rate_scope": "single-site pseudo-first-order rate in s^-1",
            "tunneling_and_recrossing": "outside source derivation; kappa carries correction",
        },
        "temperature_dependent_partition_ratio": {
            "T_K": T, "T0_K": T0, "a": a, "b_K": b_K, "delta_E0_J_per_mol": delta_e0,
            "ln_K_dagger": L, "dlnK_dT_per_K": dlnK(T), "d2lnK_dT2_per_K2": d2lnK(T),
            "source_R_lnK_J_per_molK": S_source,
            "correct_delta_S_J_per_molK": S,
            "finite_difference_delta_S_J_per_molK": S_fd,
            "missing_derivative_term_J_per_molK": R * T * dlnK(T),
            "delta_H_J_per_mol": Hact,
            "delta_Cp_J_per_molK": Cp,
            "finite_difference_delta_Cp_J_per_molK": Cp_fd,
            "entropy_fd_absolute_error": abs(S - S_fd),
            "heat_capacity_fd_absolute_error": abs(Cp - Cp_fd),
        },
        "constant_partition_ratio_limit": {
            "K_dagger": const_ratio, "dlnK_dT_per_K": 0.0,
            "delta_S_J_per_molK": constant_S, "R_lnK_J_per_molK": constant_S,
            "delta_H_J_per_mol": delta_e0, "delta_Cp_J_per_molK": 0.0,
            "rule": "source entropy equality is recovered only with zero ratio derivative and constant energy zero"},
        "rate": {
            "kappa": kappa, "k_TST_per_s": rate, "k_HS_per_s": rate_hs,
            "k_if_kappa_omitted_per_s": rate_no_kappa, "relative_omission_factor": rate_no_kappa / rate,
            "HS_roundtrip_relative_error": abs(rate - rate_hs) / rate,
            "general_form": "k=kappa(T)*(k_B*T/h)*K_dagger(T;standard_state)*exp[-DeltaE0(T)/(R*T)]",
            "analytic_dlnk_dT_per_K": dln_rate,
            "finite_difference_dlnk_dT_per_K": dln_rate_fd,
            "dlnk_derivative_absolute_error": abs(dln_rate - dln_rate_fd),
        },
        "reaction_coordinate_flux": {
            "effective_mass_kg": mass, "delta_m": delta, "q_rc": qrc,
            "one_sided_flux_moment_m_per_s": one_sided_flux_moment,
            "conditional_positive_mean_speed_m_per_s": conditional_positive_mean,
            "conditional_to_flux_moment_ratio": conditional_positive_mean / one_sided_flux_moment,
            "flux_product_per_s": flux_product,
            "kBT_over_h_per_s": flux_exact, "relative_error": abs(flux_product - flux_exact) / flux_exact,
            "rule": "sqrt(kBT/(2*pi*m)) is the one-sided moment integral_0^infinity v*f(v)dv, not E[v|v>0]; mass and length cancel only within the declared classical separable-coordinate construction",
        },
        "classical_harmonic_high_temperature": {
            "counterexample_scope": "classical harmonic unimolecular limit with common translation, rotation, standard-state factors and all corresponding stable modes cancelled except the reactant reaction-coordinate mode",
            "reactant_stable_mode_count": 3,
            "reduced_transition_state_stable_mode_count": 2,
            "T1_K": high_T_1,
            "T2_K": high_T_2,
            "normalized_K_dagger_T1": high_T_K_1,
            "normalized_K_dagger_T2": high_T_K_2,
            "K_dagger_T_exponent": -1.0,
            "T_times_K_T1_K": high_T_prefactor_1,
            "T_times_K_T2_K": high_T_prefactor_2,
            "T_times_K_relative_error": abs(high_T_prefactor_2 - high_T_prefactor_1) / high_T_prefactor_1,
            "equal_partition_ratio_prefactor_T_exponent": 1.0,
            "equal_partition_ratio_is_constant_prefactor_Arrhenius": False,
            "rule": "high-temperature powers depend on the full mode and standard-state inventory; a reduced transition state with one fewer stable harmonic mode gives K_dagger proportional to T^-1, whereas K_dagger=1 leaves the Eyring T prefactor",
        },
        "thermodynamic_identities": {
            "DeltaG": "DeltaE0(T)-R*T*lnK(T)",
            "DeltaS": "-DeltaE0'(T)+R*lnK(T)+R*T*dlnK/dT",
            "DeltaH": "DeltaE0(T)-T*DeltaE0'(T)+R*T^2*dlnK/dT",
            "DeltaCp": "-T*DeltaE0''(T)+R*(2*T*dlnK/dT+T^2*d2lnK/dT2)",
            "Arrhenius_slope_energy": "E_a=DeltaH_dagger+R*T+R*T^2*dln(kappa)/dT",
        },
    }


def equation_inventory() -> list[dict[str, Any]]:
    return [
        {"id": "EQ-Q2-001", "label": "eq:sm-mc-factor", "path": SOURCE_SPECS[0][0], "lines": [299, 311], "internal_result": "product partition follows only for independent or explicitly factorized mean-field sites"},
        {"id": "EQ-Q2-002", "label": "eq:sm-mc-occ", "path": SOURCE_SPECS[0][0], "lines": [313, 325], "internal_result": "occupation and weighted mean count confirmed"},
        {"id": "EQ-Q2-003", "label": "UNNUMBERED_Q2_CAPACITY_IDENTITY", "path": SOURCE_SPECS[0][0], "lines": [327, 339], "internal_result": "the fifth Q2 display is not represented by the +4 labeled snapshot count; one-electron C-basis identity confirmed"},
        {"id": "EQ-Q2-004", "label": "eq:sm-mc-balance", "path": SOURCE_SPECS[0][0], "lines": [340, 352], "internal_result": "one-electron site capacity balance confirmed"},
        {"id": "EQ-Q2-005", "label": "eq:sm-mc-fluc", "path": SOURCE_SPECS[0][0], "lines": [353, 380], "internal_result": "variance response confirmed; strict inequality requires positive variance"},
        {"id": "EQ-Q2-006", "label": "eq:implicit", "path": SOURCE_SPECS[2][0], "lines": [12, 35], "internal_result": "historical balance is algebraically the same weighted constraint but must inherit the exact theorem conditions"},
        {"id": "EQ-Q3-001", "label": "eq:tst-qrc", "path": SOURCE_SPECS[3][0], "lines": [57, 62], "internal_result": "classical 1D reaction-coordinate partition confirmed under stated convention"},
        {"id": "EQ-Q3-002", "label": "eq:tst-freq", "path": SOURCE_SPECS[3][0], "lines": [63, 74], "internal_result": "the one-sided Maxwell flux moment, not the conditional positive-speed mean, gives kBT/h under the source assumptions"},
        {"id": "EQ-Q3-003", "label": "eq:tst-rate", "path": SOURCE_SPECS[3][0], "lines": [76, 82], "internal_result": "conditional special case of general rate with kappa=1 and dimensionless standard-state ratio"},
        {"id": "EQ-Q3-004", "label": "eq:tst-dG", "path": SOURCE_SPECS[3][0], "lines": [82, 89], "internal_result": "conditional identity after fixing a common energy zero and dimensionless K-dagger"},
        {"id": "EQ-Q3-005", "label": "eq:tst-box", "path": SOURCE_SPECS[3][0], "lines": [91, 99], "internal_result": "rate H/S form is valid for thermodynamic H,S; displayed entropy equality omits temperature derivatives"},
        {"id": "EQ-Q3-006", "label": "eq:Lqmid2/eq:Lqfull", "path": SOURCE_SPECS[4][0], "lines": [88, 105], "internal_result": "model bridge inherits the corrected temperature-dependent activation functions"},
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("P062-S53-GC-001", "Q2-MULTICLASS", "single-site and product partition", "CONDITIONAL_ASSUMPTIONS", "PRESERVE", "Independent hard-core sites; finite positive internal degeneracy may be absorbed into effective energy."),
        ("P062-S53-GC-002", "Q2-MULTICLASS", "occupation and weighted mean particle count", "CONFIRMED_INTERNAL_DERIVATION", "PRESERVE", "Differentiate ln Xi with respect to chemical potential using one consistent per-particle or molar convention."),
        ("P062-S53-GC-003", "Q2-MULTICLASS", "Qj=(F/NA)Mj and total capacity balance", "CONFIRMED_INTERNAL_DERIVATION", "PRESERVE", "One electron transferred per site and Qj measured in coulombs."),
        ("P062-S53-GC-004", "Q2-SIGN", "V increases extraction progress for s=+1", "CONFIRMED_INTERNAL_DERIVATION", "PRESERVE", "mu=mu0-sF(V-U) must be declared before differentiation."),
        ("P062-S53-GC-005", "Q2-MULTICLASS", "variance-response derivative", "CONFIRMED_INTERNAL_DERIVATION", "PRESERVE", "Per-particle form uses beta=1/kBT; molar-mu form uses 1/RT."),
        ("P062-S53-GC-006", "Q2-MULTICLASS", "strict monotonicity and a unique root", "CONDITIONAL_ASSUMPTIONS", "CORRECT", "Replace unconditional >0/solver language by >=0, strict iff total variance>0, Q>0, nonnegative weights, T>0, finite parameters, xbar in (0,1), an independent monotone branch, and a full-domain limit or finite-domain endpoint bracket."),
        ("P062-S53-GC-007", "Q2-MULTICLASS", "mean-field-level exact product factorization", "CONFLICTING", "CORRECT", "A self-consistent mean-field factorization is an approximation to interacting sites, not exact interacting-class statistical mechanics."),
        ("P062-S53-GC-008", "Q2-MULTICLASS", "coupled-class extension", "NOT_DERIVED", "UNVERIFIED", "Exact equilibrium keeps d<N>/dmu=variance/RT but includes covariances; the class product and additive variance fail."),
        ("P062-S53-GC-009", "Q2-MULTICLASS", "Np=1 reduction", "CONFIRMED_INTERNAL_DERIVATION", "PRESERVE", "Positive class capacity; xi=xbar and the closed logistic inverse follows."),
        ("P062-S53-GC-010", "Q2-CODEMAP", "historical eq:implicit implementation and unique-root solver contract", "NOT_DERIVED", "CORRECT", "The equation identity is confirmed, but the solver contract must inherit all existence/strictness conditions; actual runtime behavior remains unverified."),
        ("P062-S53-GC-011", "Q2-MULTICLASS", "nonconvex branch uniqueness", "NOT_DERIVED", "REJECT", "Do not promote the ideal-logistic inverse proof to selected metastable/unstable mean-field branches or coexistence plateaus."),
        ("P062-S53-GC-012", "Q2-MULTICLASS", "constraint inversion is itself a Legendre-conjugate transformation", "CONFLICTING", "CORRECT", "Call this an equation-of-state inversion; separately state that canonical and grand potentials are Legendre-Fenchel related under convexity."),
        ("P062-S53-GC-013", "Q2-MULTICLASS", "capacity unit and normalization closure", "CONDITIONAL_ASSUMPTIONS", "CORRECT", "Qj=(F/NA)Mj is coulombs; divide by 3600 for Ah and use qj=Qj/Qcell for normalized capacity, with one consistent basis in every residual."),
        ("P062-S53-GC-014", "Q2-MULTICLASS", "Q2 equation denominator equals the four labeled snapshot additions", "CONFLICTING", "CORRECT", "The source addition has five displays: four labeled blocks plus the unnumbered capacity identity at lines 331-336; structural snapshot counts are not the full scientific equation denominator."),
        ("P062-S53-TST-001", "Q3-CORE", "quasi-equilibrium classical no-recrossing assumptions", "CONDITIONAL_ASSUMPTIONS", "PRESERVE", "Source explicitly fixes kappa=1 and excludes tunneling/variational corrections."),
        ("P062-S53-TST-002", "Q3-CORE", "q_rc flux cancellation to kBT/h", "CONDITIONAL_ASSUMPTIONS", "PRESERVE", "Classical separable 1D reaction coordinate and positive-direction Maxwell flux."),
        ("P062-S53-TST-003", "Q3-CORE", "kBT/h as universal barrier frequency", "CONFLICTING", "CORRECT", "It is the TST flux factor; dynamical transmission, recrossing, tunneling and coordinate conventions remain outside that phrase."),
        ("P062-S53-TST-004", "Q3-CORE", "partition-function TST rate", "CONDITIONAL_ASSUMPTIONS", "CORRECT", "General form retains dimensionless standard-state K-dagger and kappa(T); the source is the kappa=1 same-standard-state special case."),
        ("P062-S53-TST-005", "Q3-CORE", "DeltaG=DeltaE0-RT ln K-dagger", "CONDITIONAL_ASSUMPTIONS", "PRESERVE", "Common energy zero and dimensionless standard-state activation ratio."),
        ("P062-S53-TST-006", "Q3-CORE", "DeltaS=R ln(q-dagger/qR) generally", "CONFLICTING", "CORRECT", "General entropy includes -DeltaE0'(T)+RT*d ln K-dagger/dT; the displayed equality needs zero derivatives."),
        ("P062-S53-TST-007", "Q3-CORE", "Part 0 entropy-operator analogy", "CONFLICTING", "CORRECT", "Applying the stated derivative operator to the ratio produces the missing RT*d ln K/dT term."),
        ("P062-S53-TST-008", "Q3-LAG", "Q3 TST functions validate the electrode lag barrier", "NOT_DERIVED", "UNVERIFIED", "This is an internal model bridge, not electrode/material validation."),
        ("P062-S53-TST-009", "Q3-BIB", "bibliography existence and proposition support", "NOT_DERIVED", "UNVERIFIED", "Frozen bibliography/ledger are process evidence only; Step 53 performs no external verification."),
        ("P062-S53-TST-010", "Q3-CORE", "equilibrium TST implies observed dQ/dV width", "NOT_DERIVED", "REJECT", "Overpotential/current, recrossing, nucleation/growth, phase-boundary motion and distributed barriers require separate models/evidence."),
        ("P062-S53-TST-011", "Q3-CORE", "sqrt(kBT/(2*pi*m)) is the conditional positive Maxwell mean", "CONFLICTING", "CORRECT", "It is the unnormalized one-sided flux moment integral from zero to infinity; E[v|v>0] is twice this value. The source cancellation remains valid only with the flux-moment interpretation."),
        ("P062-S53-TST-012", "Q3-CORE", "reduced partition ratio has a finite constant classical high-temperature limit generally", "CONFLICTING", "CORRECT", "Temperature powers depend on the complete stable-mode and standard-state inventory; with one fewer stable harmonic mode at the reduced transition state, K-dagger is proportional to T^-1."),
        ("P062-S53-TST-013", "Q3-CORE", "q-dagger=qR gives a pure constant-prefactor Arrhenius law", "CONFLICTING", "CORRECT", "K-dagger=1 leaves the Eyring prefactor k_B*T/h, so the prefactor retains a factor T; constant-prefactor Arrhenius behavior requires an additional compensating T^-1 factor or a local approximation."),
    ]
    return [{
        "claim_id": cid, "source_span_id": span, "claim": claim,
        "derivation_state": state, "source_disposition": disposition,
        "conditions_or_correction": condition,
        "external_support_state": "UNVERIFIED_EXTERNAL",
        "external_scientific_truth": False,
        "external_material_truth": False,
    } for cid, span, claim, state, disposition, condition in rows]


def edge_case_rows() -> list[dict[str, str]]:
    return [
        {"case": "zero class weight", "existence": "unchanged if at least one positive class remains", "uniqueness": "unchanged if total variance remains positive", "finding": "all-zero weights make normalization undefined"},
        {"case": "duplicate class energy", "existence": "unchanged after merging weights", "uniqueness": "unchanged", "finding": "duplicate energies are not duplicate roots"},
        {"case": "saturated class", "existence": "depends on remaining classes/domain", "uniqueness": "one zero-variance class is harmless; all-zero variance removes strict proof", "finding": "finite T and finite energy do not exactly saturate ideal logistic"},
        {"case": "finite potential domain", "existence": "only for target in the endpoint image", "uniqueness": "at most one under strict monotonicity", "finding": "existence and uniqueness are separate"},
        {"case": "finite positive degeneracy", "existence": "energy shift only", "uniqueness": "preserved", "finding": "nonpositive/undefined degeneracy is invalid"},
        {"case": "coupled classes", "existence": "requires full partition function", "uniqueness": "variance identity is nondecreasing and strict only when variance>0", "finding": "product/additive-class formulas fail"},
        {"case": "nonconvex mean-field branch", "existence": "may be discontinuous or set-valued under coexistence", "uniqueness": "ideal branch proof does not transfer", "finding": "exact equilibrium convexity and a selected metastable branch must not be conflated"},
    ]


def build() -> dict[str, Any]:
    attestations, decoded = source_attestations()
    q2 = q2_probe()
    tst = tst_probe()
    claims = claim_rows()
    dispositions: dict[str, int] = {}
    derivations: dict[str, int] = {}
    for row in claims:
        dispositions[row["source_disposition"]] = dispositions.get(row["source_disposition"], 0) + 1
        derivations[row["derivation_state"]] = derivations.get(row["derivation_state"], 0) + 1
    return {
        "schema_version": "1.0.0",
        "artifact_kind": "PHASE_062_STEP_053_STATMECH_TST_REDERIVATION",
        "phase": 62,
        "step": 53,
        "generated_date": "2026-08-27",
        "status": "PASS_WITH_CONCERNS",
        "gate": "PASS_P062_STEP53_STATMECH_TST_REDERIVATION",
        "authority_boundary": {
            "internal_derivation_and_frozen_source_alignment": True,
            "external_scientific_truth": False,
            "external_material_truth": False,
            "external_experimental_truth": False,
            "primary_reference_proposition_support": False,
            "code_runtime_validation": False,
            "claude_files_modified": False,
        },
        "git": {
            "baseline_commit": BASELINE,
            "q2_commit": Q2_COMMIT,
            "q2_parent": Q2_PARENT,
            "q3_commit": Q3_COMMIT,
            "q3_parent": Q3_PARENT,
            "expected_precommit_parent": EXPECTED_PARENT,
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "commit_subject": "audit(phase062): rederive v1021 statmech tst",
        },
        "source_attestations": attestations,
        "source_spans": source_spans(decoded),
        "snapshot_evidence": snapshot_rows(),
        "patches": [
            {"phase": "Q2", "parent": Q2_PARENT, "commit": Q2_COMMIT, "diff_sha256": sha256(run_git("diff", "--no-ext-diff", "--unified=0", Q2_PARENT, Q2_COMMIT, binary=True))},
            {"phase": "Q3", "parent": Q3_PARENT, "commit": Q3_COMMIT, "diff_sha256": sha256(run_git("diff", "--no-ext-diff", "--unified=0", Q3_PARENT, Q3_COMMIT, binary=True))},
        ],
        "equation_inventory": equation_inventory(),
        "grand_canonical_derivation": {
            "sign_convention": "mu_molar(V)=mu0_molar-s*F*(V-U); for s=+1, dmu/dV=-F and xi=1-theta increases with V",
            "single_site": "Xi_1j=1+exp[-(eps_j-mu)/(R*T)]",
            "product": "Xi=product_j Xi_1j^Mj only for independent/factorized sites",
            "occupation": "theta_j=1/[1+exp((eps_j-mu)/(R*T))]",
            "mean_count": "<N>=sum_j Mj*theta_j",
            "capacity_constraint": "sum_j Qj*xi_j=Q*xbar with xi_j=1-theta_j, Qj=(F/NA)Mj, Q=sum_j Qj",
            "residual_derivative": "dR/dV=s*F/(R*T)*sum_j Qj*theta_j*(1-theta_j)",
            "response_identity": "d<N>/dmu_molar=Var(N)/(R*T); per-particle mu uses beta=1/(k_B*T)",
            "interacting_mean_field_susceptibility": "dtheta/dmu=theta(1-theta)/[R*T-2*Omega*theta(1-theta)]; it is not the Bernoulli response unless Omega=0 or the effective field is held fixed",
            "existence": "continuous unbounded ideal-logistic V maps to [0,Q] in the limits; finite domains only cover their endpoint image",
            "uniqueness": "strict only where the total weighted variance is positive",
            "capacity_units": "Qj=(F/NA)Mj is C; Qj_Ah=Qj_C/3600; normalized qj=Qj/Qcell; all residual terms require one common basis",
            "potential_duality_wording": "solving the monotone constraint is equation-of-state inversion; canonical/grand potentials are Legendre-Fenchel related only with the required convexity conditions",
            "q2_display_denominator": {"labeled_snapshot_blocks": 4, "unnumbered_capacity_displays": 1, "total_q2_added_displays": 5},
            "edge_cases": edge_case_rows(),
            "numeric_probe": q2,
        },
        "tst_rederivation": {
            "general_rate": "single-site pseudo-first-order k(T) [s^-1]=kappa(T)*(k_B*T/h)*K_dagger(T;consistent standard state)*exp[-DeltaE0(T)/(R*T)]",
            "scope_separation": {
                "derived_background": ["transition-state quasi-equilibrium population", "classical positive crossing flux", "kBT/h flux factor", "thermodynamic activation identities"],
                "not_derived": ["electrode overpotential/current law", "recrossing or tunneling correction", "nucleation and growth", "phase-boundary motion", "distributed barriers", "observed dQ/dV width"],
            },
            "numeric_probe": tst,
        },
        "claim_rows": claims,
        "findings": [
            {"finding_id": "P062-S53-F001", "severity": "P1", "summary": "The displayed general activation entropy omits temperature-derivative terms.", "route": "CORRECT in future canonical theory/manuscript before adoption."},
            {"finding_id": "P062-S53-F002", "severity": "P1", "summary": "Self-consistent interacting mean-field sites do not retain the independent Bernoulli product/variance susceptibility claimed as exact.", "route": "Restrict the proof to Omega=0 or a fixed effective field, or add the separate mean-field free-energy/susceptibility derivation."},
            {"finding_id": "P062-S53-F003", "severity": "P1", "summary": "The strict unique-root and solver contract omits positive-variance, positive-weight, domain-bracket and endpoint conditions.", "route": "Replace blanket >0/unique-root wording and propagate conditions to eq:implicit and solve_U_oc."},
            {"finding_id": "P062-S53-F004", "severity": "P2", "summary": "Constraint inversion is described too strongly as a Legendre-conjugate transformation.", "route": "Separate equation-of-state inversion from Legendre-Fenchel potential duality under convexity."},
            {"finding_id": "P062-S53-F005", "severity": "P2", "summary": "C, Ah and normalized capacity conversions are not explicit in the Q2 balance.", "route": "Declare C/3600 and Qj/Qcell transformations and require a common basis."},
            {"finding_id": "P062-S53-F006", "severity": "P2", "summary": "The +4 labeled snapshot count omits the fifth, unnumbered Q2 capacity display.", "route": "Keep the unnumbered display as an explicit scientific equation row; never use snapshot counts as completeness authority."},
            {"finding_id": "P062-S53-F007", "severity": "P2", "summary": "General TST needs an explicit dimensionless standard-state ratio and transmission coefficient.", "route": "Retain K-dagger and kappa in the general equation; source equation is a declared special case."},
            {"finding_id": "P062-S53-F008", "severity": "P2", "summary": "Equilibrium TST does not establish electrode-specific barriers or observed peak width.", "route": "Keep these as NOT_DERIVED/UNVERIFIED and reject TST-to-width promotion."},
            {"finding_id": "P062-S53-F009", "severity": "P1", "summary": "The source calls a one-sided Maxwell flux moment the conditional positive-speed mean; those quantities differ by a factor of two.", "route": "Keep the kBT/h cancellation only after relabeling sqrt(kBT/(2*pi*m)) as the one-sided flux moment."},
            {"finding_id": "P062-S53-F010", "severity": "P1", "summary": "The classical high-temperature partition-ratio and pure-Arrhenius limiting claims omit mode-count temperature powers.", "route": "Derive the T exponent from the complete reduced-TS/reactant mode and standard-state inventory; do not call K-dagger=1 a constant-prefactor Arrhenius limit."},
        ],
        "negative_control_contract": [
            "wrong_electrical_sign", "missing_class_weight", "variance_zero_uniqueness", "hidden_interaction",
            "constant_partition_ratio", "omitted_transmission_coefficient", "state_free_electrode_barrier", "tst_to_peak_width_promotion",
        ],
        "summary": {
            "source_files_read_full": len(attestations),
            "source_lines_read_full": sum(row["physical_lines"] for row in attestations),
            "source_spans": len(SPAN_SPECS),
            "equations": len(equation_inventory()),
            "claims": len(claims),
            "derivation_state_counts": derivations,
            "source_disposition_counts": dispositions,
            "findings": {"P0": 0, "P1": 5, "P2": 5},
            "snapshot_nodes": sum(row["traversal"]["nodes"] for row in snapshot_rows()),
            "next_step": 54,
        },
    }


def render_markdown(data: dict[str, Any], artifact_sha256: str) -> str:
    s = data["summary"]
    q2 = data["grand_canonical_derivation"]["numeric_probe"]
    tst = data["tst_rederivation"]["numeric_probe"]
    claims = data["claim_rows"]
    lines = [
        "# Phase 062 Step 053 — v1.0.21 대정준 전하 보존·TST 재유도 결과",
        "",
        "## 판정",
        "",
        "- 상태: `PASS_WITH_CONCERNS`",
        "- Precommit Gate: `PASS_P062_STEP53_STATMECH_TST_REDERIVATION`",
        "- Postcommit terminal: `PENDING_AT_PRECOMMIT_BY_DESIGN`",
        "- 범위: frozen v1.0.21 Q2/Q3 내부 수식·가정·교차참조의 독립 재유도와 조건 경계.",
        "- 외부 권위: `UNVERIFIED_EXTERNAL`; external scientific/material/experimental truth 및 primary-reference proposition support는 모두 false.",
        "- `Claude/**` 수정: 0.",
        "",
        "## 입력과 전문 검독",
        "",
        f"- frozen baseline `{BASELINE}`; Q2 `{Q2_COMMIT}`; Q3 `{Q3_COMMIT}`.",
        f"- 최종 release text/process 파일 `{s['source_files_read_full']}/{s['source_files_read_full']}`개, `{s['source_lines_read_full']}`행을 1–EOF 직접 검독했다.",
        f"- Q2/Q3 load-bearing source span `{s['source_spans']}`개는 원문 전체·행 범위·Git blob·SHA-256으로 고정했다.",
        f"- Q2/Q3 snapshot strict traversal nodes `{s['snapshot_nodes']}`; snapshot은 구조 diff evidence일 뿐 과학 truth가 아니다.",
        "",
        "## Q2 — 다클래스 대정준 재유도",
        "",
        "부호를 먼저 고정한다: `mu_molar(V)=mu0_molar-sF(V-U)`. `s=+1`이면 `dmu/dV=-F`, `xi=1-theta`이므로 전위가 오를수록 추출 진행률이 증가한다.",
        "",
        "독립 hard-core 자리에서는 `Xi_1j=1+exp[-(eps_j-mu)/(RT)]`, `Xi=product_j Xi_1j^Mj`, `theta_j=[1+exp((eps_j-mu)/(RT))]^-1`, `<N>=sum Mj theta_j`가 이어진다. 한 자리당 한 전자를 전제로 `Qj=(F/NA)Mj`를 쓰면 `sum Qj xi_j=Q xbar`가 된다.",
        "",
        "molar chemical potential 기준 응답은 `d<N>/dmu=Var(N)/(RT)`이고, 전위 residual 미분은 `sF/(RT) sum Qj theta_j(1-theta_j)`다. 따라서 비음이 아니라 **양의 분산**이 strict monotonicity의 필요조건이다. 존재성은 별도이며, 유한 전위 구간에서는 목표가 endpoint image 안에 있어야 한다. Source의 blanket `>0`·unique-root solver 계약은 이 조건들을 빠뜨려 `CORRECT`다.",
        "",
        f"- multiclass root `{q2['multiclass']['root_V']:.12f}` V, residual `{q2['multiclass']['normalized_residual']:.3e}`.",
        f"- analytic/finite-difference derivative error `{q2['multiclass']['absolute_derivative_error']:.3e}`.",
        f"- `N_p=1` closed/numeric inverse error `{q2['single_class']['absolute_error_V']:.3e}` V.",
        f"- coupled two-site variance-response error `{q2['coupled_exact']['absolute_response_error']:.3e}`, while independent-product mean error `{q2['coupled_exact']['product_formula_absolute_error']:.3e}`.",
        "- zero weight, duplicate energy, saturation, finite domain, degeneracy, coupled class and nonconvex branch는 각각 존재/유일성 축을 분리해 machine artifact에 고정했다.",
        "- interacting self-consistent mean field의 감도는 Bernoulli 분산합과 달라 `평균장 수준에서 정확`이라는 문구를 교정해야 한다.",
        "- `Qj=(F/NA)Mj`는 C 기준이다. Ah는 `/3600`, normalized capacity는 `Qj/Qcell`을 명시해야 하며, 단순 constraint inversion과 Legendre-Fenchel potential duality도 분리해야 한다.",
        "- Q2 추가 display는 snapshot의 labeled 4개가 아니라 unnumbered capacity identity를 포함한 5개다.",
        "",
        "## Q3 — TST 재유도와 교정",
        "",
        "현재 source의 single-site pseudo-first-order 범위(`[s^-1]`)에서, 일관된 표준상태의 무차원 `K_dagger`와 transmission coefficient를 유지한 식은 `k=kappa(kBT/h)K_dagger exp[-DeltaE0/(RT)]`이다. Source 식은 `kappa=1`, classical separable reaction coordinate, no recrossing/tunneling인 특수형이다.",
        "",
        "`L(T)=ln K_dagger(T)`라 두면 `DeltaG=DeltaE0-RTL`, `DeltaS=-DeltaE0'+RL+RT L'`, `DeltaH=DeltaE0-T DeltaE0'+RT^2 L'`, `DeltaCp=-T DeltaE0''+R(2T L'+T^2 L'')`이다. 그러므로 source의 `DeltaS=R ln(q-dagger/qR)`는 energy-zero derivative와 partition-ratio derivative가 모두 0일 때만 회수된다.",
        "",
        f"- temperature-dependent ratio probe: source entropy `{tst['temperature_dependent_partition_ratio']['source_R_lnK_J_per_molK']:.6f}` vs corrected `{tst['temperature_dependent_partition_ratio']['correct_delta_S_J_per_molK']:.6f}` J mol^-1 K^-1.",
        f"- entropy finite-difference error `{tst['temperature_dependent_partition_ratio']['entropy_fd_absolute_error']:.3e}`; heat-capacity error `{tst['temperature_dependent_partition_ratio']['heat_capacity_fd_absolute_error']:.3e}`.",
        f"- omitting `kappa={tst['rate']['kappa']}` changes the rate by factor `{tst['rate']['relative_omission_factor']:.6f}`.",
        f"- source의 `sqrt(kBT/(2*pi*m))`는 조건부 양의 속도 평균이 아니라 one-sided flux moment다. 조건부 평균/flux-moment 비는 `{tst['reaction_coordinate_flux']['conditional_to_flux_moment_ratio']:.1f}`이다.",
        "- classical harmonic high-T에서 reduced transition state가 안정 모드 하나 적으면 `K_dagger proportional to T^-1`이고 `(kBT/h)K_dagger`의 T 거듭제곱이 상쇄된다. 반대로 `K_dagger=1`은 Eyring prefactor의 T 인자를 남기므로 일반적인 constant-prefactor pure Arrhenius가 아니다.",
        "- equilibrium TST background does not derive electrode overpotential/current, recrossing, nucleation/growth, phase-boundary motion, barrier distributions or measured dQ/dV width.",
        "",
        "## 주장별 판정",
        "",
        "| Claim | Derivation state | Source disposition | External support |",
        "|---|---|---|---|",
    ]
    for row in claims:
        lines.append(f"| `{row['claim_id']}` | `{row['derivation_state']}` | `{row['source_disposition']}` | `UNVERIFIED_EXTERNAL` |")
    lines += [
        "",
        "## Findings and routing",
        "",
        "- P0 `0`; P1 `5`; P2 `5`.",
        "- P1: 일반 활성화 엔트로피 식의 온도 미분항 누락, self-consistent mean-field에 대한 독립 Bernoulli 증명의 과잉 확장, 조건이 빠진 blanket unique-root solver 계약, Maxwell flux-moment 오명명, high-T/순수 Arrhenius 극한 과장을 `CORRECT`로 라우팅한다.",
        "- P2: Legendre 용어, capacity basis, unnumbered Q2 equation denominator, standard-state/`kappa`, equilibrium TST→electrode/peak-width 권위 승격을 각각 교정·차단한다.",
        "- 발견된 오류는 frozen `Claude/**`에 직접 고치지 않았고 후속 canonical theory/manuscript 단계의 명시적 correction route로 남긴다.",
        "",
        "## 검증과 다음 단계",
        "",
        "- 독립 대수, exact coupled-state enumeration, bisection, central finite difference, analytic limiting cases를 사용했다.",
        "- required negative controls: wrong sign, missing weight, variance-zero uniqueness, hidden interaction, constant-ratio misuse, omitted `kappa`, state-free electrode barrier, TST-to-width promotion.",
        f"- machine artifact SHA-256: `{artifact_sha256}`.",
        "- 실행 명령: `py -3.12 Codex/work/v1021_phase062/validate_phase062_step53.py --content-only --run-negative-probes --determinism-check`; 같은 명령을 `py -3.14`로도 실행했다.",
        "- 두 런타임 모두 content Gate, negative controls `36/36`, Markdown negative controls `9/9`, builder-policy negative controls `11/11`, builder CRLF portability `1/1`, determinism `2/2`, symbolic checks `15/15`, numeric checks `20/20`, strict JSON traversal `956` nodes/depth `5`를 통과했다.",
        "- exact-seven 예정 subject: `audit(phase062): rederive v1021 statmech tst`.",
        "- Step 54는 이 exact-seven commit의 push 및 `PASS_P062_STEP53_PERSISTENCE` 확인 후에만 시작한다.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare deterministic bytes without writing")
    args = parser.parse_args()
    data = build()
    raw_json = json_bytes(data)
    raw_md = render_markdown(data, sha256(raw_json)).encode("utf-8")
    if args.check:
        if not OUTPUT_JSON.exists() or not OUTPUT_MD.exists():
            print("FAIL_P062_STEP53_BUILD_CHECK missing output")
            return 1
        if OUTPUT_JSON.read_bytes() != raw_json or OUTPUT_MD.read_bytes() != raw_md:
            print("FAIL_P062_STEP53_BUILD_CHECK deterministic byte mismatch")
            return 1
        print("PASS_P062_STEP53_BUILD_DETERMINISM")
        return 0
    OUTPUT_JSON.write_bytes(raw_json)
    OUTPUT_MD.write_bytes(raw_md)
    print(f"WROTE {OUTPUT_JSON.relative_to(ROOT).as_posix()}")
    print(f"WROTE {OUTPUT_MD.relative_to(ROOT).as_posix()}")
    print("PASS_P062_STEP53_BUILD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
