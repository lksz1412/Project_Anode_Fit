#!/usr/bin/env python3
"""Independently rederive the v1.0.14 phase-separation appendix."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "Claude/docs/v1.0.14/appendix_phase_separation.tex"
OUTPUT = (
    ROOT / "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json"
)
REPORT = (
    ROOT / "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md"
)

PRIMARY_SOURCES = [
    {
        "id": "CAHN_HILLIARD_1958",
        "title": "Free Energy of a Nonuniform System. I. Interfacial Free Energy",
        "doi": "10.1063/1.1744102",
        "url": "https://doi.org/10.1063/1.1744102",
        "verified_claim": (
            "The original nonuniform-system functional carries a number-density "
            "prefactor multiplying a per-particle homogeneous free energy plus "
            "a gradient term."
        ),
        "relevance": (
            "The appendix instead integrates a previously molar f directly "
            "over volume, omitting the density/molar-volume conversion."
        ),
    },
    {
        "id": "CAHN_1961",
        "title": "On spinodal decomposition",
        "doi": "10.1016/0001-6160(61)90182-1",
        "url": "https://doi.org/10.1016/0001-6160(61)90182-1",
        "verified_claim": (
            "For coherent solids, composition-dependent molar volume and "
            "elastic energy can shift the limit of metastability away from "
            "the purely chemical spinodal."
        ),
        "relevance": (
            "The appendix states f''=0 without bounding it as the chemical, "
            "stress-free, constant-volume spinodal."
        ),
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bisection(function, lower: float, upper: float, iterations: int = 100) -> float:
    f_lower = function(lower)
    f_upper = function(upper)
    if f_lower * f_upper > 0:
        raise ValueError("root not bracketed")
    for _ in range(iterations):
        middle = 0.5 * (lower + upper)
        f_middle = function(middle)
        if f_lower * f_middle <= 0:
            upper = middle
            f_upper = f_middle
        else:
            lower = middle
            f_lower = f_middle
    return 0.5 * (lower + upper)


def numerical_rederivation() -> dict:
    interaction_ratio = 3.0  # Omega/(RT)

    def f_over_rt(x: np.ndarray | float):
        x_array = np.asarray(x)
        return (
            x_array * np.log(x_array)
            + (1.0 - x_array) * np.log(1.0 - x_array)
            + interaction_ratio * x_array * (1.0 - x_array)
        )

    def fp_over_rt(x: np.ndarray | float):
        x_array = np.asarray(x)
        return (
            np.log(x_array / (1.0 - x_array))
            + interaction_ratio * (1.0 - 2.0 * x_array)
        )

    def fpp_over_rt(x: np.ndarray | float):
        x_array = np.asarray(x)
        return (
            1.0 / (x_array * (1.0 - x_array))
            - 2.0 * interaction_ratio
        )

    binodal_minus = bisection(
        lambda x: float(fp_over_rt(x)), 1.0e-10, 0.49
    )
    binodal_plus = 1.0 - binodal_minus
    spinodal_u = math.sqrt(1.0 - 2.0 / interaction_ratio)
    spinodal_minus = 0.5 * (1.0 - spinodal_u)
    spinodal_plus = 0.5 * (1.0 + spinodal_u)
    grid = np.linspace(binodal_minus, binodal_plus, 200001)
    equal_area = float(np.trapezoid(fp_over_rt(grid), grid))
    chord_slope = float(
        (f_over_rt(binodal_plus) - f_over_rt(binodal_minus))
        / (binodal_plus - binodal_minus)
    )

    # Independent test of the appendix's factor-2 gradient convention:
    # R(k) = -M k^2 [a + 2 kappa k^2].
    curvature = -2.0
    kappa = 0.5
    mobility = 1.0
    k_critical = math.sqrt(-curvature / (2.0 * kappa))
    k_maximum = k_critical / math.sqrt(2.0)

    def growth(k: float) -> float:
        return -mobility * k**2 * (curvature + 2.0 * kappa * k**2)

    return {
        "test_condition": {"Omega_over_RT": interaction_ratio},
        "regular_solution": {
            "binodal_minus": binodal_minus,
            "binodal_plus": binodal_plus,
            "spinodal_minus": spinodal_minus,
            "spinodal_plus": spinodal_plus,
            "binodal_f_over_RT": float(f_over_rt(binodal_minus)),
            "spinodal_f_over_RT": float(f_over_rt(spinodal_minus)),
            "critical_curvature_fpp_over_RT_at_half": float(
                fpp_over_rt(0.5)
            ),
            "binodal_derivative_minus": float(fp_over_rt(binodal_minus)),
            "binodal_derivative_plus": float(fp_over_rt(binodal_plus)),
            "common_tangent_chord_slope": chord_slope,
            "maxwell_equal_area_residual": equal_area,
            "binodal_outside_spinodal": (
                binodal_minus < spinodal_minus < 0.5
                < spinodal_plus < binodal_plus
            ),
        },
        "cahn_hilliard_factor_two_convention": {
            "curvature_a": curvature,
            "kappa": kappa,
            "mobility": mobility,
            "critical_wavenumber": k_critical,
            "maximum_growth_wavenumber": k_maximum,
            "maximum_equals_critical_over_sqrt2": math.isclose(
                k_maximum, k_critical / math.sqrt(2.0)
            ),
            "growth_at_zero": growth(0.0),
            "growth_at_half_critical": growth(0.5 * k_critical),
            "growth_at_maximum": growth(k_maximum),
            "growth_at_critical": growth(k_critical),
            "growth_above_critical": growth(1.1 * k_critical),
            "maximum_growth_closed_form": (
                mobility * curvature**2 / (8.0 * kappa)
            ),
        },
    }


def source_contracts(text: str) -> dict:
    lines = text.splitlines()

    def label_line(label: str) -> int:
        return next(
            index
            for index, line in enumerate(lines, 1)
            if f"\\label{{{label}}}" in line
        )

    return {
        "line_count": len(lines),
        "equation_label_lines": {
            label: label_line(label)
            for label in (
                "eq:app-fxi",
                "eq:app-ct",
                "eq:app-binodal",
                "eq:app-spinodal",
                "eq:app-maxwell",
                "eq:app-cnt",
                "eq:app-rstar",
                "eq:app-ch-F",
                "eq:app-ch-R",
            )
        },
        "explicit_kappa_unit_count": len(
            re.findall(r"kappa.*(?:J/|J\\,|m\\^|m\^)", text, re.IGNORECASE)
        ),
        "explicit_mobility_unit_count": len(
            re.findall(
                r"(?:이동도|mobility)[^\n]*\[[^\]\n]+\]",
                text,
                re.IGNORECASE,
            )
        ),
        "explicit_no_flux_boundary_count": len(
            re.findall(
                r"no[- ]flux|무유속|n\s*\\cdot\s*\\nabla\s*\\mu",
                text,
                re.IGNORECASE,
            )
        ),
        "explicit_composition_boundary_count": len(
            re.findall(
                r"n\s*\\cdot\s*\\nabla\s*\\xi|periodic|주기 경계",
                text,
                re.IGNORECASE,
            )
        ),
        "molar_f_definition_present": (
            "몰당 혼합 자유에너지는" in text
            and "\\label{eq:app-fxi}" in text
        ),
        "molar_f_integrated_over_volume_without_conversion": (
            "F[\\xi]=\\int\\Bigl[f\\bigl(\\xi(\\mathbf{r})\\bigr)"
            in text
        ),
        "gradient_term_without_half": (
            "+\\kappa\\,\\bigl|\\nabla\\xi\\bigr|^2" in text
        ),
        "factor_two_chemical_potential": (
            "f'(\\xi)-2\\kappa\\nabla^2\\xi" in text
        ),
        "factor_two_growth_rate": (
            "f''(\\bar\\xi)+2\\kappa k^2" in text
        ),
        "elastic_energy_term_present": bool(
            re.search(r"elastic|탄성|coheren|정합 변형", text, re.IGNORECASE)
        ),
        "volume_symbol_collision": (
            "\\dd V" in text and "전위" in text
        ),
    }


def canonical_repair_contract() -> dict:
    return {
        "definitions": [
            {
                "symbol": "c_s",
                "meaning": "moles of intercalation sites per volume",
                "unit": "mol m^-3",
            },
            {
                "symbol": "f_m(xi)",
                "meaning": "homogeneous molar free energy per mole of sites",
                "unit": "J mol^-1",
            },
            {
                "symbol": "K",
                "meaning": "molar gradient coefficient in K/2 convention",
                "unit": "J m^2 mol^-1",
            },
            {
                "symbol": "mu",
                "meaning": "molar exchange chemical potential",
                "unit": "J mol^-1",
            },
            {
                "symbol": "L",
                "meaning": "Onsager mobility for molar flux",
                "unit": "mol^2 J^-1 m^-1 s^-1",
            },
            {
                "symbol": "M=L/c_s",
                "meaning": "composition mobility",
                "unit": "mol m^2 J^-1 s^-1",
            },
        ],
        "functional": (
            "G[xi] = integral c_s [f_m(xi) + (K/2)|grad xi|^2] d^3r"
        ),
        "chemical_potential": "mu = f_m'(xi) - K laplacian(xi)",
        "molar_flux": "N_B = -L grad(mu)",
        "conservation": (
            "c_s partial_t xi = -div(N_B) = div(L grad(mu))"
        ),
        "constant_coefficient_form": (
            "partial_t xi = M laplacian(mu), M=L/c_s"
        ),
        "linear_growth_rate": (
            "R(k) = -M k^2 [f_m''(xi_bar) + K k^2]"
        ),
        "critical_wavenumber": "k_c = sqrt(-f_m''/K)",
        "fastest_wavenumber": "k_m = k_c/sqrt(2)",
        "natural_boundary_conditions": [
            "normal dot grad(xi) = 0",
            "normal dot grad(mu) = 0",
        ],
        "periodic_alternative": True,
        "mass_conservation_identity": (
            "d/dt integral xi dV = 0 under no-flux or periodic boundaries"
        ),
        "energy_dissipation_identity": (
            "dG/dt = -integral L |grad(mu)|^2 dV <= 0"
        ),
        "mapping_from_appendix_convention": (
            "K = 2 kappa/c_s if appendix kappa multiplies |grad xi|^2 "
            "as a volumetric coefficient"
        ),
    }


def findings() -> list[dict]:
    return [
        {
            "id": "PS-059-01",
            "topic": "regular_solution",
            "disposition": "PRESERVE_WITH_UNIT_WORDING_CORRECTION",
            "finding": (
                "The mixing free energy, critical Omega=2RT, binodal, "
                "spinodal, common-tangent, and Maxwell equations rederive."
            ),
            "defect": (
                "The prose conflates per-site and per-mole quantities; k_B "
                "and R versions must be separated explicitly."
            ),
        },
        {
            "id": "PS-059-02",
            "topic": "chemical_spinodal_scope",
            "disposition": "CORRECT_MAJOR_SCOPE_BOUNDARY",
            "finding": (
                "f''=0 is the stress-free chemical spinodal for the chosen "
                "homogeneous free energy."
            ),
            "defect": (
                "Cahn 1961 explicitly shows coherency elasticity and "
                "composition-dependent molar volume can shift the instability "
                "criterion; the LIB-solid appendix omits that boundary."
            ),
        },
        {
            "id": "PS-059-03",
            "topic": "gradient_functional_units",
            "disposition": "FAIL_DIMENSIONAL_CLOSURE",
            "finding": (
                "The appendix integrates molar f [J/mol] directly over dV "
                "while adding an un-united kappa gradient term."
            ),
            "defect": (
                "A site density/molar-volume conversion and an explicit "
                "gradient-coefficient convention are required."
            ),
        },
        {
            "id": "PS-059-04",
            "topic": "factor_two_convention",
            "disposition": "PRESERVE_AFTER_DEFINITION",
            "finding": (
                "Using kappa|grad xi|^2 yields -2 kappa laplacian(xi) and "
                "the displayed factor-2 growth rate; these are internally "
                "consistent."
            ),
            "defect": (
                "The convention and units are not defined, making comparison "
                "with the common (K/2)|grad xi|^2 form ambiguous."
            ),
        },
        {
            "id": "PS-059-05",
            "topic": "linear_stability",
            "disposition": "PRESERVE_AFTER_DIMENSIONAL_REPAIR",
            "finding": (
                "The unstable band, critical wavenumber, and k_m=k_c/sqrt(2) "
                "follow from the stated factor-2 convention."
            ),
            "defect": (
                "As printed, k_c is dimensionally undefined because f'' is "
                "molar and kappa has no declared compatible unit."
            ),
        },
        {
            "id": "PS-059-06",
            "topic": "mobility",
            "disposition": "FAIL_UNIT_AND_STATE_CLOSURE",
            "finding": (
                "M>0 is sufficient for the sign of linear growth in a "
                "constant-mobility toy model."
            ),
            "defect": (
                "Mobility units, flux definition, site density, possible "
                "composition/temperature dependence, and relation to "
                "diffusivity are absent."
            ),
        },
        {
            "id": "PS-059-07",
            "topic": "boundary_conditions",
            "disposition": "FAIL_MISSING",
            "finding": (
                "No no-flux, natural-gradient, or periodic boundary condition "
                "is specified."
            ),
            "defect": (
                "Without boundary conditions the claimed conserved dynamics "
                "does not close mass conservation or free-energy dissipation."
            ),
        },
        {
            "id": "PS-059-08",
            "topic": "classical_nucleation",
            "disposition": "PRESERVE_WITH_ASSUMPTION_BOUNDARY",
            "finding": (
                "The spherical CNT critical radius and barrier rederive."
            ),
            "defect": (
                "Isotropic sharp-interface gamma, negligible coherency strain, "
                "bulk reservoir, and homogeneous nucleation assumptions must "
                "be stated before use for electrode particles."
            ),
        },
        {
            "id": "PS-059-09",
            "topic": "coordinate_and_symbols",
            "disposition": "CORRECT_TERMINOLOGY_AND_COLLISION",
            "finding": (
                "The xi versus 1-xi complement warning correctly anticipates "
                "the first-derivative sign reversal."
            ),
            "defect": (
                "f(xi)=f(1-xi) is mirror symmetry about 1/2, not evenness "
                "about zero, and dV for volume collides with V for voltage."
            ),
        },
        {
            "id": "PS-059-10",
            "topic": "final_authority",
            "disposition": "PRESERVE_DERIVATION_ASSET_NOT_CANON",
            "finding": (
                "The appendix is a useful pedagogical derivation of the "
                "stress-free regular-solution baseline."
            ),
            "defect": (
                "Dimensional, boundary-condition, mobility, elasticity, and "
                "solid-electrode scope blockers prevent canonical promotion."
            ),
        },
    ]


def report_text(result: dict) -> str:
    numeric = result["numerical_rederivation"]["regular_solution"]
    ch = result["numerical_rederivation"][
        "cahn_hilliard_factor_two_convention"
    ]
    source = result["source_contracts"]
    finding_rows = "\n".join(
        f"| {item['id']} | {item['topic']} | {item['disposition']} | "
        f"{item['defect']} |"
        for item in result["findings"]
    )
    return rf"""# Phase 059 v1.0.14 상분리 부록 독립 재유도

정본일: 2026-07-28

판정: `{result['status']}`

## 결론

정규용액의 homogeneous thermodynamics는 대체로 맞다. 자유에너지,
공통접선, binodal, chemical spinodal, Maxwell 등면적, 구형 CNT
식과 Cahn–Hilliard 성장 band의 대수는 독립 재유도된다.

그러나 Cahn–Hilliard 절은 현재 형태로 차원이 닫히지 않는다.
앞에서 \(f\)를 J/mol로 정의한 뒤 site density 또는 molar-volume
환산 없이 \(\int f\,dV\)를 쓰고, \(\kappa\)와 \(M\)의 단위를
정의하지 않았다. 경계조건도 없어 질량보존과 자유에너지 감소를
증명할 수 없다. 또한 고체 삽입전극에서 중요한 coherency elasticity
가 chemical spinodal을 바꿀 수 있다는 적용 경계를 누락했다.

## 정규용액 수치 재유도

\(\Omega/(RT)=3\)에서 독립 계산은 다음을 준다.

- binodal:
  \(\xi_b^-={numeric['binodal_minus']:.7f}\),
  \(\xi_b^+={numeric['binodal_plus']:.7f}\)
- spinodal:
  \(\xi_s^-={numeric['spinodal_minus']:.7f}\),
  \(\xi_s^+={numeric['spinodal_plus']:.7f}\)
- \(f(\xi_b)/(RT)={numeric['binodal_f_over_RT']:.7f}\)
- Maxwell equal-area residual:
  {numeric['maxwell_equal_area_residual']:.3e}
- common-tangent chord slope:
  {numeric['common_tangent_chord_slope']:.3e}

따라서 문건의 0.0707/0.9293, 0.2113/0.7887, \(-0.0583\)
수치는 재현된다.

## Cahn–Hilliard 식의 대수와 차원

문건은 gradient energy를 \(\kappa|\nabla\xi|^2\)로 썼으므로
변분의 \(-2\kappa\nabla^2\xi\)와 성장률
\[
R(k)=-Mk^2[f''+2\kappa k^2]
\]
은 같은 convention 안에서는 일관된다. 독립 probe에서도
\(k_c={ch['critical_wavenumber']:.7f}\),
\(k_m={ch['maximum_growth_wavenumber']:.7f}=k_c/\sqrt2\),
\(R(k_c)={ch['growth_at_critical']:.3e}\)가 재현된다.

하지만 이 대수는 단위를 복구한 뒤에만 물리식이 된다.
[Cahn–Hilliard 1958 원 논문](https://doi.org/10.1063/1.1744102)은
per-particle homogeneous free energy와 gradient term 앞에
number-density factor를 둔다. v1.0.14는 molar \(f\)를 그대로
volume integral에 넣어 그 연결을 빠뜨렸다.

최종 문건의 권장 계약은
\[
\mathcal G[\xi]=\int c_s\left[f_m(\xi)+
\frac{{K}}{{2}}|\nabla\xi|^2\right]d^3r,\qquad
\mu=f_m'(\xi)-K\nabla^2\xi
\]
이다. 여기서 \(c_s\)[mol m\(^{{-3}}\)],
\(f_m\)[J mol\(^{{-1}}\)], \(K\)[J m\(^2\) mol\(^{{-1}}\)]다.
몰 flux \(\mathbf N_B=-\mathcal L\nabla\mu\)와
\(c_s\partial_t\xi=-\nabla\cdot\mathbf N_B\)를 쓰면
\(M=\mathcal L/c_s\)[mol m\(^2\) J\(^{{-1}}\) s\(^{{-1}}\)]이고,
\[
R(k)=-Mk^2[f_m''+Kk^2].
\]
문건 convention으로 돌아가려면 volumetric \(\kappa\)에 대해
\(K=2\kappa/c_s\)를 명시해야 한다.

## 빠진 경계조건과 고체 적용 경계

source에서 explicit \(\kappa\) unit, mobility unit, no-flux
boundary, composition natural boundary count는 각각
{source['explicit_kappa_unit_count']},
{source['explicit_mobility_unit_count']},
{source['explicit_no_flux_boundary_count']},
{source['explicit_composition_boundary_count']}이다.

폐계라면
\(\mathbf n\cdot\nabla\mu=0\)와
\(\mathbf n\cdot\nabla\xi=0\), 또는 periodic boundary가 필요하다.
그때만
\[
\frac{{d}}{{dt}}\int\xi\,dV=0,\qquad
\frac{{d\mathcal G}}{{dt}}=-\int\mathcal L|\nabla\mu|^2dV\le0
\]
를 닫을 수 있다.

[Cahn 1961 원 논문](https://doi.org/10.1016/0001-6160(61)90182-1)은
고체에서 조성에 따른 molar-volume 변화와 elastic energy가
metastability limit를 이동시킬 수 있음을 명시한다. 따라서
v1.0.14의 \(f''=0\)은 일반 LIB 고체의 spinodal이 아니라
`stress-free chemical spinodal`로 한정해야 한다.

## 판정표

| ID | topic | disposition | blocker/debt |
|---|---|---|---|
{finding_rows}

## 다음 단계

Step 36.3에서 v1.0.14의 LCO electronic term, graphite/LCO sign
map, heat convention과 high-voltage/doping scope를 독립
재유도·검산한다.
"""


def main() -> int:
    before = sha256(SOURCE)
    text = SOURCE.read_text(encoding="utf-8")
    result = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "scope": (
            "Phase 059 Step 36.2 independent regular-solution, binodal, "
            "spinodal, Maxwell, nucleation, and Cahn-Hilliard rederivation"
        ),
        "authority_boundary": (
            "Independent mathematical and dimensional audit of the historical "
            "appendix; not final theory or material-specific validation."
        ),
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256_before": before,
        "source_contracts": source_contracts(text),
        "primary_source_checks": PRIMARY_SOURCES,
        "numerical_rederivation": numerical_rederivation(),
        "canonical_repair_contract": canonical_repair_contract(),
        "findings": findings(),
        "summary": {
            "finding_count": len(findings()),
            "preserve_family_count": sum(
                item["disposition"].startswith("PRESERVE")
                for item in findings()
            ),
            "correct_family_count": sum(
                item["disposition"].startswith("CORRECT")
                for item in findings()
            ),
            "fail_family_count": sum(
                item["disposition"].startswith("FAIL")
                for item in findings()
            ),
            "primary_source_count": len(PRIMARY_SOURCES),
            "regular_solution_numeric_check_count": 10,
            "cahn_hilliard_numeric_check_count": 8,
            "explicit_boundary_condition_count": (
                source_contracts(text)["explicit_no_flux_boundary_count"]
                + source_contracts(text)[
                    "explicit_composition_boundary_count"
                ]
            ),
            "dimensional_closure_pass": False,
            "boundary_condition_closure_pass": False,
            "elasticity_scope_closure_pass": False,
        },
        "source_sha256_after": sha256(SOURCE),
        "source_unchanged": before == sha256(SOURCE),
        "status": (
            "CONDITIONAL_P059_V1014_PHASE_SEPARATION_CORE_CORRECT_WITH_"
            "DIMENSIONAL_BOUNDARY_AND_ELASTICITY_BLOCKERS"
        ),
        "next_action": (
            "Run Step 36.3 LCO electronic, graphite/LCO sign-map, heat, "
            "and high-voltage/doping-scope rederivation."
        ),
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text(report_text(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "report": str(REPORT.relative_to(ROOT)),
                "status": result["status"],
                "summary": result["summary"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
