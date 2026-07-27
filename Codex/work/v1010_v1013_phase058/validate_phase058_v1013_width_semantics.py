#!/usr/bin/env python3
"""Validate the v1.0.13 interaction/degeneracy/multiplicity separation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CH1 = ROOT / "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex"
CH2 = ROOT / "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex"
CODE = ROOT / "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py"
SAMPLE = ROOT / "Claude/docs/v1.0.13/sample_test_v1013.py"
RESULT = ROOT / "Codex/results/PHASE_058_V1013_WIDTH_SEMANTICS.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_line(path: Path, needle: str) -> int:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return number
    raise ValueError(f"Needle not found in {path}: {needle}")


def load_module():
    sys.dont_write_bytecode = True
    specification = importlib.util.spec_from_file_location(
        "phase058_v1013_width_probe", CODE
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(CODE)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def normalized_binomial_occupancy(site_count: int, fugacity: float) -> float:
    weights = [
        math.comb(site_count, occupied) * fugacity**occupied
        for occupied in range(site_count + 1)
    ]
    partition = math.fsum(weights)
    mean_occupied = math.fsum(
        occupied * weight for occupied, weight in enumerate(weights)
    ) / partition
    return mean_occupied / site_count


def main() -> int:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    numeric = data["numeric_invariants"]
    implementation = data["implementation_probe"]
    temperature = numeric["temperature_k"]
    gas_constant = numeric["gas_constant_j_per_mol_k"]
    faraday = numeric["faraday_constant_c_per_mol"]
    ideal_width = gas_constant * temperature / faraday

    checks: dict[str, bool] = {}
    checks["schema"] = data["schema_version"] == "phase058-v1013-width-semantics-v1"
    checks["boundary"] = (
        data["audit_boundary"]
        == "PHYSICAL_MEANING_SEPARATION_NOT_PARAMETER_IDENTIFICATION"
    )
    for name, path in (
        ("chapter_1", CH1),
        ("chapter_2", CH2),
        ("production_code", CODE),
        ("sample", SAMPLE),
    ):
        checks[f"{name}_hash"] = sha256(path) == data["sources"][f"{name}_sha256"]

    evidence_needles = {
        "n_named_width_multiplicity_line": (
            CH1,
            "$n_j$ (\\code{n})",
        ),
        "width_equation_line": (
            CH1,
            "w_j=\\frac{n_jRT}{F}",
        ),
        "subcritical_width_claim_line": (
            CH1,
            "단상($\\Omega_j\\le2RT$",
        ),
        "finite_rate_broadening_line": (
            CH1,
            "① 유한율속 비대칭 꼬리(동역학 몫)",
        ),
        "ensemble_integral_line": (
            CH1,
            "\\label{eq:ensavg}",
        ),
        "chapter_2_generalized_config_line": (
            CH2,
            "\\frac{n_jR}{F}\\ln",
        ),
        "chapter_2_conditional_validation_line": (
            CH2,
            "이 검증의 $w_j(T)$",
        ),
        "code_func_w_line": (
            CODE,
            "def func_w",
        ),
        "code_n_precedence_line": (
            CODE,
            "def _n_factor",
        ),
        "sample_n_0p12_line": (
            SAMPLE,
            'tr["n"] = 0.12',
        ),
    }
    for key, (path, needle) in evidence_needles.items():
        checks[f"source_line_{key}"] = (
            source_line(path, needle) == data["source_evidence"][key]
        )

    checks["ideal_width"] = math.isclose(
        ideal_width,
        numeric["ideal_one_electron_width_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    two_electron_width = ideal_width / 2.0
    current_formula_n2 = 2.0 * ideal_width
    checks["two_electron_inverse_scaling"] = math.isclose(
        two_electron_width,
        numeric["ideal_two_electron_width_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["current_n2_direct_scaling"] = math.isclose(
        current_formula_n2,
        numeric["current_formula_n_2_width_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["electron_vs_current_n_ratio"] = (
        current_formula_n2 / two_electron_width
        == numeric["current_formula_to_two_electron_width_ratio"]
        == 4.0
    )

    width_ratio = numeric["sample_lambda"]
    sample_width = width_ratio * ideal_width
    sample_fwhm = 4.0 * math.acosh(math.sqrt(2.0)) * sample_width
    checks["sample_width"] = math.isclose(
        sample_width,
        numeric["sample_lambda_width_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["sample_fwhm"] = math.isclose(
        sample_fwhm,
        numeric["sample_lambda_fwhm_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["inverse_hill"] = math.isclose(
        1.0 / width_ratio,
        numeric["sample_inverse_hill_slope"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    fugacity = numeric["site_multiplicity_probe_fugacity"]
    expected_occupancy = fugacity / (1.0 + fugacity)
    multiplicity_occupancies = [
        normalized_binomial_occupancy(site_count, fugacity)
        for site_count in numeric["site_multiplicity_probe_values"]
    ]
    checks["site_multiplicity_expected_occupancy"] = math.isclose(
        expected_occupancy,
        numeric["site_multiplicity_normalized_occupancy"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["site_count_does_not_change_fraction"] = max(
        abs(value - expected_occupancy) for value in multiplicity_occupancies
    ) < 2.0e-15

    xi = 0.8
    ideal_config = gas_constant / faraday * math.log(xi / (1.0 - xi))
    empirical_algebraic = width_ratio * ideal_config
    checks["ideal_config_term"] = math.isclose(
        ideal_config,
        numeric["ideal_config_dudt_at_xi_0p8_v_per_k"],
        rel_tol=0.0,
        abs_tol=1.0e-18,
    )
    checks["empirical_config_ratio"] = math.isclose(
        empirical_algebraic,
        numeric["lambda_0p12_algebraic_dudt_at_xi_0p8_v_per_k"],
        rel_tol=0.0,
        abs_tol=1.0e-18,
    )
    checks["empirical_is_not_ideal_config"] = math.isclose(
        empirical_algebraic / ideal_config,
        width_ratio,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    variances = numeric["illustrative_variance_components_v2"]
    equilibrium_variance = math.pi**2 * ideal_width**2 / 3.0
    total_variance = math.fsum(variances.values())
    equivalent_width = math.sqrt(3.0 * total_variance) / math.pi
    checks["logistic_variance"] = math.isclose(
        equilibrium_variance,
        variances["ideal_logistic"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["convolution_standard_deviation"] = math.isclose(
        math.sqrt(total_variance),
        numeric["illustrative_total_standard_deviation_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["variance_equivalent_width"] = math.isclose(
        equivalent_width,
        numeric["illustrative_variance_equivalent_logistic_width_v"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    activation_energy = numeric["illustrative_activation_energy_j_per_mol"]
    low_temperature = 273.15
    high_temperature = 298.15
    tau_ratio = math.exp(
        activation_energy
        / gas_constant
        * (1.0 / low_temperature - 1.0 / high_temperature)
    )
    checks["low_temperature_tau_ratio"] = math.isclose(
        tau_ratio,
        numeric["illustrative_tau_ratio_273p15k_to_298p15k"],
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )
    checks["equilibrium_temperature_ratio"] = math.isclose(
        low_temperature / high_temperature,
        numeric["equilibrium_width_ratio_273p15k_to_298p15k"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["kinetic_and_equilibrium_temperature_trends_can_compete"] = (
        tau_ratio > 1.0 and low_temperature / high_temperature < 1.0
    )

    module = load_module()
    all_defaults = list(module.GRAPHITE_STAGING_LIT) + list(module.LCO_MSMR_LIT)
    model = module.GraphiteAnodeDischargeDQDV(
        module.GRAPHITE_STAGING_LIT, Rn=0.0, Cbg=0.0
    )
    shadow_count = sum(
        "n" in transition
        and "w" in transition
        and not math.isclose(
            float(model._width(transition, temperature)),
            float(transition["w"]),
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
        for transition in all_defaults
    )
    checks["default_graphite_count"] = (
        len(module.GRAPHITE_STAGING_LIT)
        == implementation["default_graphite_transition_count"]
    )
    checks["default_lco_count"] = (
        len(module.LCO_MSMR_LIT)
        == implementation["default_lco_transition_count"]
    )
    checks["all_default_n_one"] = (
        sum(transition.get("n") == 1.0 for transition in all_defaults)
        == implementation["default_transitions_with_n_equal_one"]
        == 7
    )
    checks["all_default_w_present"] = (
        sum("w" in transition for transition in all_defaults)
        == implementation["default_transitions_with_stored_w"]
        == 7
    )
    checks["all_default_w_shadowed"] = (
        shadow_count == implementation["default_transitions_where_n_shadows_w"] == 7
    )
    checks["code_n1_width"] = math.isclose(
        float(module.func_w(temperature, 1.0)),
        implementation["code_width_v_at_298p15k_n_1"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["code_n0p12_width"] = math.isclose(
        float(module.func_w(temperature, 0.12)),
        implementation["code_width_v_at_298p15k_n_0p12"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["sample_calls_width_phenomenological"] = (
        implementation["sample_uses_n_0p12_only_as_phenomenological_fit"]
        and "phenomenological free fit width" in SAMPLE.read_text(encoding="utf-8")
    )

    taxonomy = data["symbol_taxonomy"]
    symbols = [entry["symbol"] for entry in taxonomy]
    checks["taxonomy_count"] = len(taxonomy) == 10
    checks["taxonomy_unique"] = len(symbols) == len(set(symbols))
    claims = data["claim_dispositions"]
    claim_ids = [entry["id"] for entry in claims]
    checks["claim_count"] = len(claims) == 13
    checks["claim_ids_unique"] = len(claim_ids) == len(set(claim_ids))
    checks["recommended_symbols_complete"] = set(
        data["recommended_symbol_contract"]
    ) == {
        "n_e",
        "M_j",
        "g_j",
        "Omega_j",
        "lambda_j",
        "w_eq_j",
        "rho_het_j",
        "tau_j",
        "K_obs",
        "w_reported_j",
    }

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "artifact": str(RESULT.relative_to(ROOT)),
                "check_count": len(checks),
                "failures": failures,
                "site_multiplicity_occupancies": multiplicity_occupancies,
                "two_electron_width_v": two_electron_width,
                "current_formula_n2_width_v": current_formula_n2,
                "sample_width_v": sample_width,
                "sample_inverse_hill_slope": 1.0 / width_ratio,
                "default_shadowed_w_count": shadow_count,
                "illustrative_tau_ratio": tau_ratio,
                "verdict": data["verdict"],
                "gate": (
                    "PASS_P058_V1013_WIDTH_SEMANTICS"
                    if not failures
                    else "FAIL_P058_V1013_WIDTH_SEMANTICS"
                ),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
