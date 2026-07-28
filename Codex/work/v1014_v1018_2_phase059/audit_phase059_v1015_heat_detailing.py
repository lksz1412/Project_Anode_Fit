#!/usr/bin/env python3
"""Audit the v1.0.15 Ch2 heat detailing and theory/code quantity contract."""

from __future__ import annotations

import ast
import difflib
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CH2_14 = ROOT / "Claude/docs/v1.0.14/graphite_ica_ch2_v1.0.14.tex"
CH2_15 = ROOT / "Claude/docs/v1.0.15/graphite_ica_ch2_v1.0.15.tex"
CODE_14 = ROOT / "Claude/docs/v1.0.14/Anode_Fit_v1.0.14.py"
CODE_15 = ROOT / "Claude/docs/v1.0.15/Anode_Fit_v1.0.15.py"
HANDOVER = ROOT / "Claude/docs/v1.0.15/HANDOVER_v1.0.15.md"
CLOSING = ROOT / "Claude/docs/v1.0.15/CLOSING_v1.0.15.md"
PRIOR = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json"
OUTPUT = ROOT / "Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1015_HEAT_DETAILING_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def diff_metrics(old: Path, new: Path) -> dict[str, Any]:
    before = old.read_text(encoding="utf-8").splitlines()
    after = new.read_text(encoding="utf-8").splitlines()
    added: list[str] = []
    deleted: list[str] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        a=before, b=after, autojunk=False
    ).get_opcodes():
        if tag in {"replace", "delete"}:
            deleted.extend(before[i1:i2])
        if tag in {"replace", "insert"}:
            added.extend(after[j1:j2])
    numstat = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(old), str(new)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if numstat.returncode not in (0, 1):
        raise RuntimeError(numstat.stderr)
    fields = numstat.stdout.strip().split("\t")
    if len(fields) < 2:
        raise RuntimeError(f"unexpected numstat: {numstat.stdout!r}")
    git_added, git_deleted = int(fields[0]), int(fields[1])
    code_mentions = [
        line.strip()
        for line in added
        if any(
            token in line
            for token in ("코드", "Anode\\_Fit", "entropy\\_coefficient")
        )
    ]
    return {
        "old_line_count": len(before),
        "new_line_count": len(after),
        "added_line_count": git_added,
        "deleted_line_count": git_deleted,
        "sequence_matcher_added_line_count": len(added),
        "sequence_matcher_deleted_line_count": len(deleted),
        "added_subsection_count": sum(
            line.startswith(r"\subsection") for line in added
        ),
        "added_equation_star_count": sum(
            r"\begin{equation*}" in line for line in added
        ),
        "added_table_count": sum(r"\begin{table}" in line for line in added),
        "added_code_mention_lines": code_mentions,
        "added_body_code_mention_lines": [
            line for line in code_mentions if not line.startswith(r"\bibitem")
        ],
        "added_vibrational_caveat": any("준양자" in line for line in added),
        "added_width_model_choice_caveat": any(
            "다온도 round-trip" in line for line in added
        ),
        "added_worked_example": any("계산 예제" in line for line in added),
    }


def ast_digest(
    path: Path, function_name: str, class_name: str | None = None
) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    candidates: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    if class_name is None:
        candidates = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function_name
        ]
    else:
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                candidates = [
                    child
                    for child in node.body
                    if isinstance(
                        child, (ast.FunctionDef, ast.AsyncFunctionDef)
                    )
                    and child.name == function_name
                ]
                break
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one {class_name or '<module>'}.{function_name}"
        )
    normalized = ast.dump(candidates[0], annotate_fields=True)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def scalar(value: Any) -> float:
    return float(np.asarray(value, dtype=float).reshape(-1)[0])


def logistic(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + np.exp(-z))
    ez = np.exp(z)
    return ez / (1.0 + ez)


def solve_u(
    transitions: list[dict[str, Any]],
    temperature: float,
    xbar: float,
    gas_constant: float,
    faraday: float,
    thermal_width: bool = True,
    reference_temperature: float = 298.15,
) -> float:
    total_q = sum(float(item["Q"]) for item in transitions)

    def residual(voltage: float) -> float:
        occupied = 0.0
        for item in transitions:
            center = (
                -float(item["dH_rxn"])
                + temperature * float(item["dS_rxn"])
            ) / faraday
            width_temperature = (
                temperature if thermal_width else reference_temperature
            )
            width = (
                float(item["n"])
                * gas_constant
                * width_temperature
                / faraday
            )
            occupied += float(item["Q"]) * logistic(
                (voltage - center) / width
            )
        return occupied - total_q * xbar

    low, high = -1.0, 1.0
    for _ in range(160):
        middle = 0.5 * (low + high)
        if residual(middle) < 0.0:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def analytic_terms(
    transitions: list[dict[str, Any]],
    voltage: float,
    temperature: float,
    gas_constant: float,
    faraday: float,
) -> dict[str, Any]:
    rows = []
    for item in transitions:
        center = (
            -float(item["dH_rxn"])
            + temperature * float(item["dS_rxn"])
        ) / faraday
        width = (
            float(item["n"]) * gas_constant * temperature / faraday
        )
        xi = logistic((voltage - center) / width)
        g = xi * (1.0 - xi) / width
        qg = float(item["Q"]) * g
        center_term = float(item["dS_rxn"]) / faraday
        config_term = (
            float(item["n"])
            * gas_constant
            / faraday
            * np.log(xi / (1.0 - xi))
        )
        rows.append(
            {
                "xi": xi,
                "g_per_V": g,
                "Qg": qg,
                "center_V_per_K": center_term,
                "config_V_per_K": float(config_term),
            }
        )
    denominator = sum(row["Qg"] for row in rows)
    for row in rows:
        row["weight"] = row["Qg"] / denominator
    center_only = sum(
        row["weight"] * row["center_V_per_K"] for row in rows
    )
    config = sum(
        row["weight"] * row["config_V_per_K"] for row in rows
    )
    return {
        "rows": rows,
        "dqdv_weight_denominator_per_V": denominator,
        "center_only_V_per_K": center_only,
        "config_V_per_K": config,
        "complete_V_per_K": center_only + config,
    }


def main() -> int:
    sources = [CH2_14, CH2_15, CODE_14, CODE_15, HANDOVER, CLOSING, PRIOR]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
    module = load_module(CODE_15, "phase059_v1015_heat")
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))

    heat_functions = [
        (None, "func_U_j"),
        ("GraphiteAnodeDischargeDQDV", "_effective_dS_rxn"),
        ("GraphiteAnodeDischargeDQDV", "entropy_coefficient"),
        ("GraphiteAnodeDischargeDQDV", "reversible_heat"),
        ("GraphiteAnodeDischargeDQDV", "irreversible_heat"),
        ("LCOCathodeDQDV", "_effective_dS_rxn"),
    ]
    ast_comparison = []
    for class_name, function_name in heat_functions:
        old_hash = ast_digest(CODE_14, function_name, class_name)
        new_hash = ast_digest(CODE_15, function_name, class_name)
        ast_comparison.append(
            {
                "symbol": (
                    f"{class_name}.{function_name}"
                    if class_name
                    else function_name
                ),
                "v1014_ast_sha256": old_hash,
                "v1015_ast_sha256": new_hash,
                "executable_ast_identical": old_hash == new_hash,
            }
        )

    transitions = module.GRAPHITE_STAGING_LIT
    model = module.GraphiteAnodeDischargeDQDV(transitions)
    temperature = 298.15
    x_values = [0.10, 0.25, 0.50, 0.75, 0.90]
    numerical_rows = []
    for xbar in x_values:
        voltage = solve_u(
            transitions, temperature, xbar, module.R, module.F
        )
        analytic = analytic_terms(
            transitions, voltage, temperature, module.R, module.F
        )
        code_coefficient = scalar(
            model.entropy_coefficient(voltage, temperature)
        )
        plus = solve_u(
            transitions, temperature + 3.0, xbar, module.R, module.F
        )
        minus = solve_u(
            transitions, temperature - 3.0, xbar, module.R, module.F
        )
        finite_difference = (plus - minus) / 6.0
        fixed_plus = solve_u(
            transitions,
            temperature + 3.0,
            xbar,
            module.R,
            module.F,
            thermal_width=False,
        )
        fixed_minus = solve_u(
            transitions,
            temperature - 3.0,
            xbar,
            module.R,
            module.F,
            thermal_width=False,
        )
        fixed_width_derivative = (fixed_plus - fixed_minus) / 6.0
        heat_per_amp = scalar(
            model.reversible_heat(voltage, temperature, 1.0)
        )
        numerical_rows.append(
            {
                "xbar_delithiation_fraction": xbar,
                "U_oc_V": voltage,
                "analytic_complete_V_per_K": analytic[
                    "complete_V_per_K"
                ],
                "code_entropy_coefficient_V_per_K": code_coefficient,
                "finite_difference_thermal_width_V_per_K": finite_difference,
                "finite_difference_fixed_width_V_per_K": (
                    fixed_width_derivative
                ),
                "center_only_V_per_K": analytic["center_only_V_per_K"],
                "config_V_per_K": analytic["config_V_per_K"],
                "effective_entropy_J_per_mol_K": module.F * code_coefficient,
                "qrev_per_I_V": heat_per_amp,
                "analytic_code_abs_V_per_K": abs(
                    analytic["complete_V_per_K"] - code_coefficient
                ),
                "analytic_fd_abs_V_per_K": abs(
                    analytic["complete_V_per_K"] - finite_difference
                ),
                "fixed_width_center_abs_V_per_K": abs(
                    fixed_width_derivative
                    - analytic["center_only_V_per_K"]
                ),
            }
        )

    point = numerical_rows[1]
    point_terms = analytic_terms(
        transitions, point["U_oc_V"], temperature, module.R, module.F
    )
    ch2_diff = diff_metrics(CH2_14, CH2_15)
    code_diff = diff_metrics(CODE_14, CODE_15)

    findings = [
        {
            "id": "HD-059-01",
            "topic": "release_delta_class",
            "disposition": "WORKED_EXPLANATION_NOT_NEW_HEAT_IMPLEMENTATION",
            "finding": (
                "The main Ch2 addition is one worked example, two tables, "
                "and caveats; all six heat-path executable ASTs are unchanged."
            ),
        },
        {
            "id": "HD-059-02",
            "topic": "implicit_derivative",
            "disposition": "PRESERVE_FOR_CONSTANT_N_THERMAL_WIDTH",
            "finding": (
                "At fixed delithiation fraction, implicit differentiation "
                "gives the documented center plus configurational weighted sum."
            ),
        },
        {
            "id": "HD-059-03",
            "topic": "worked_example_numbers",
            "disposition": "PRESERVE_NUMERIC_ROUND_TRIP",
            "finding": (
                "The xbar=0.25 values and all five SOC table rows reproduce "
                "with independent bisection, analytic weighting, code output, "
                "and T±3 K finite differences."
            ),
        },
        {
            "id": "HD-059-04",
            "topic": "width_temperature_model",
            "disposition": "CONDITIONAL_MODEL_CHOICE_NOT_MATERIAL_FACT",
            "finding": (
                "The configurational term follows only when w=nRT/F with "
                "constant n. A T-frozen width produces the center-only result."
            ),
        },
        {
            "id": "HD-059-05",
            "topic": "graphite_half_cell_quantity",
            "disposition": "PRESERVE_DECLARED_HALF_CELL_REACTION_QUANTITY",
            "finding": (
                "Within the declared graphite-vs-Li half-cell, U_oc, fixed-x "
                "dU_oc/dT, DeltaS=F dU_oc/dT, and qrev=-I_lith T dU_oc/dT "
                "are mutually consistent."
            ),
        },
        {
            "id": "HD-059-06",
            "topic": "direction_label_mapping",
            "disposition": "DOCUMENTED_BUT_NOT_TYPE_SAFE",
            "finding": (
                "The text and docstring disclose that positive heat current "
                "means half-cell lithiation whereas curve discharge means "
                "graphite delithiation; the API does not encode that distinction."
            ),
        },
        {
            "id": "HD-059-07",
            "topic": "full_cell_translation",
            "disposition": "REQUIRE_CATHODE_MINUS_ANODE_ASSEMBLY",
            "finding": (
                "For full-cell discharge the graphite contribution changes "
                "sign relative to a positive lithiation-current half-cell term, "
                "and total reversible heat also requires the cathode coefficient."
            ),
        },
        {
            "id": "HD-059-08",
            "topic": "reference_electrode",
            "disposition": "PRESERVE_HALF_CELL_SCOPE_CARRY_REFERENCE_GUARD",
            "finding": (
                "The chapter declares graphite vs Li, so its fitted coefficient "
                "is a half-cell quantity. Intrinsic electrode and measured "
                "reference-inclusive coefficients must not be interchanged."
            ),
        },
        {
            "id": "HD-059-09",
            "topic": "lco_heat_inheritance",
            "disposition": "CARRY_V1014_LCO_REFERENCE_AND_T_DEPENDENCE_FAIL",
            "finding": (
                "Unchanged LCO heat AST means the v1.0.14 reference, DOS gate, "
                "composition, and T-squared-curvature blockers remain."
            ),
        },
        {
            "id": "HD-059-10",
            "topic": "calorimetry_citation_scope",
            "disposition": "REJECT_AS_SPECIFIC_GRAPHITE_SIGN_SCALE_VALIDATION",
            "finding": (
                "The cited 2024 paper validates a standardized full-cell "
                "potentiometric entropy method; it does not validate this "
                "graphite four-transition prior's +60.8 mW/A prediction."
            ),
        },
        {
            "id": "HD-059-11",
            "topic": "vibrational_caveat",
            "disposition": "PRESERVE_AS_CONCEPTUAL_CAVEAT_NOT_IMPLEMENTED_TERM",
            "finding": (
                "The classical-limit/quantum-residual sentence is a useful "
                "qualification, but no oscillator spectrum or residual T term "
                "is added to the model."
            ),
        },
        {
            "id": "HD-059-12",
            "topic": "manuscript_code_boundary",
            "disposition": "FAIL_USER_THEORY_ONLY_BODY_CONSTRAINT",
            "finding": (
                "The new worked section adds two direct production-code "
                "mentions inside the physics manuscript."
            ),
        },
        {
            "id": "HD-059-13",
            "topic": "experimental_authority",
            "disposition": "INTERNAL_SELF_CONSISTENCY_ONLY",
            "finding": (
                "The round trip validates the algebra for demonstration priors, "
                "not graphite calorimetry or multi-temperature experimental fit."
            ),
        },
    ]

    result = {
        "schema_version": 1,
        "phase": 59,
        "step": "37.3",
        "scope": (
            "v1.0.15 Ch2 heat-detailing novelty, independent numerical "
            "round trip, thermodynamic quantity/reference/sign contract, "
            "citation authority, and theory-only manuscript boundary"
        ),
        "release_delta": {
            "ch2": ch2_diff,
            "production_code": code_diff,
            "heat_path_ast": ast_comparison,
            "all_heat_path_executable_ast_identical": all(
                row["executable_ast_identical"] for row in ast_comparison
            ),
            "classification": (
                "WORKED_EXPLANATION_WITH_CONCEPTUAL_CAVEATS_NOT_NEW_HEAT_CODE"
            ),
        },
        "independent_rederivation": {
            "fixed_quantity": "total delithiation fraction xbar",
            "implicit_constraint": "sum_j Q_j xi_j(U,T)=Q_total*xbar",
            "thermal_width_assumption": "w_j=n_j*R*T/F with constant n_j",
            "derived_identity": (
                "dU/dT=sum_j alpha_j[dS_j/F+(n_j R/F)"
                "ln(xi_j/(1-xi_j))]"
            ),
            "fixed_width_limit": (
                "dw_j/dT=0 removes the configurational term"
            ),
        },
        "worked_example": {
            "temperature_K": temperature,
            "rows": numerical_rows,
            "xbar_0p25_transition_terms": point_terms,
            "maximum_analytic_code_abs_V_per_K": max(
                row["analytic_code_abs_V_per_K"]
                for row in numerical_rows
            ),
            "maximum_analytic_fd_abs_V_per_K": max(
                row["analytic_fd_abs_V_per_K"]
                for row in numerical_rows
            ),
            "maximum_fixed_width_center_abs_V_per_K": max(
                row["fixed_width_center_abs_V_per_K"]
                for row in numerical_rows
            ),
        },
        "quantity_reference_sign_contract": {
            "manuscript_scope": "graphite working electrode vs Li half-cell",
            "composition_coordinate": "xbar is delithiation fraction",
            "entropy_quantity": (
                "reaction/half-cell entropy coefficient F*dU_oc/dT "
                "at fixed xbar"
            ),
            "heat_current_coordinate": (
                "I>0 in qrev is half-cell discharge/lithiation current"
            ),
            "curve_direction_coordinate": (
                "direction=discharge maps to graphite delithiation"
            ),
            "labels_are_opposite_chemical_directions": True,
            "label_difference_disclosed_in_text_and_docstring": True,
            "api_type_enforces_reaction_coordinate": False,
            "full_cell_voltage_identity": "U_cell=U_cathode-U_anode",
            "full_cell_graphite_contribution": (
                "+I_cell*T*dU_anode/dT for discharge-positive I_cell"
            ),
            "full_cell_total_available_from_graphite_only": False,
            "reference_guard": (
                "Do not promote an intrinsic single-electrode coefficient "
                "to a measured Li-reference half-cell coefficient."
            ),
        },
        "external_source_check": {
            "citation": (
                "Hales and Bulman, J. Electrochem. Soc. 171 (2024) 050535"
            ),
            "doi": "10.1149/1945-7111/ad4918",
            "primary_repository_url": (
                "https://research-information.bris.ac.uk/en/publications/"
                "a-standardised-potentiometric-method-for-the-effective-parameteri/"
            ),
            "supported_scope": (
                "standardized potentiometric extraction of a full-cell "
                "entropy coefficient and reversible-heating parameter"
            ),
            "specific_graphite_four_transition_sign_scale_supported": False,
        },
        "inherited_v1014_blockers": {
            "prior_status": prior["status"],
            "half_cell_reference_closure_pass": prior["summary"][
                "half_cell_reference_closure_pass"
            ],
            "theory_code_electronic_conformance_pass": prior["summary"][
                "theory_code_electronic_conformance_pass"
            ],
            "doped_high_voltage_coverage_pass": prior["summary"][
                "doped_high_voltage_coverage_pass"
            ],
            "unchanged_heat_ast_means_repaired": False,
        },
        "findings": findings,
        "summary": {
            "finding_count": len(findings),
            "new_heat_implementation_pass": False,
            "worked_example_algebra_pass": True,
            "worked_example_code_match_pass": True,
            "constant_n_thermal_width_contract_pass": True,
            "fixed_width_alternative_distinguished": True,
            "graphite_half_cell_internal_quantity_pass": True,
            "reaction_coordinate_api_safety_pass": False,
            "full_cell_heat_authority_pass": False,
            "specific_calorimetry_validation_pass": False,
            "lco_heat_blockers_repaired": False,
            "theory_only_manuscript_boundary_pass": False,
            "external_material_validation_pass": False,
            "next_step": "37.4",
        },
        "status": (
            "CONDITIONAL_P059_V1015_HEAT_WORKED_EXAMPLE_NUMERICALLY_CLOSED_"
            "BUT_NO_NEW_HEAT_PHYSICS_AND_SIGN_API_BOUNDARY_REMAINS"
        ),
        "next_action": (
            "Phase 059 Step 37.4: separate v1.0.16 n(T) as an empirical "
            "width law from microscopic physics and verify dw/dT, entropy "
            "propagation, positivity, and parameter correlation."
        ),
        "source_hashes_before": before,
        "source_hashes_after": {
            str(path.relative_to(ROOT)): sha256(path) for path in sources
        },
    }
    result["source_unchanged"] = (
        result["source_hashes_before"] == result["source_hashes_after"]
    )
    OUTPUT.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    report = rf"""# Phase 059 v1.0.15 Ch2 heat 상세화 독립 판정

정본일: 2026-07-28

판정: `{result["status"]}`

## 결론

v1.0.15 Ch2의 핵심 추가분은 새 열물리 구현이 아니라 기존
상수-\(n\), \(w=nRT/F\) 식의 worked explanation이다. Ch2 exact
diff는 +{ch2_diff["added_line_count"]}/-{ch2_diff["deleted_line_count"]}
행이고, 생산 코드의 `func_U_j`, graphite/LCO entropy seam,
`entropy_coefficient`, `reversible_heat`, `irreversible_heat` 실행
AST는 v1.0.14와 전부 동일하다.

추가 예제의 대수와 수치는 보존한다. \(\bar x=0.25\),
\(T=298.15\) K에서 독립 계산은
\(U_{{oc}}={point["U_oc_V"]*1000:.3f}\) mV,
\(\partial U/\partial T={point["code_entropy_coefficient_V_per_K"]*1000:.6f}\)
mV/K, \(\Delta S={point["effective_entropy_J_per_mol_K"]:.3f}\)
J mol\(^{-1}\) K\(^{-1}\),
\(\dot Q_{{rev}}/I={point["qrev_per_I_V"]*1000:.3f}\) mV를 낸다.
해석 가중식, 생산 함수와 \(T\pm3\) K 음함수 유한차분은 최대
{result["worked_example"]["maximum_analytic_fd_abs_V_per_K"]:.3e}
V/K 안에서 일치한다.

## 새 물리와 설명의 경계

- 새로 추가된 실제 물리 내용은 진동 엔트로피의 고전극한 흡수와
  준양자 잔여 \(T\)-의존에 대한 caveat다. oscillator spectrum이나
  잔여항은 식·코드에 추가되지 않았다.
- 완전식의 config 항은 상수 \(n\)인 열적 폭 \(w=nRT/F\)를 선택한
  결과다. 폭을 \(T\)-동결하면 그 항은 사라지고 중심값 가중식으로
  돌아간다. 따라서 두-상 흑연의 물성 사실이 아니라 다온도
  round-trip으로 선택해야 할 model branch다.
- 표와 round-trip은 demonstration prior에 대한 내부 자기일관성이다.
  흑연 calorimetry 또는 다온도 실험 피팅의 외부 검증이 아니다.

## quantity·reference·sign

문건이 선언한 graphite-vs-Li 하프셀 범위 안에서는 같은 quantity를
사용한다. \(\bar x\)는 탈리튬화 분율이고,
\(F\,\partial U_{{oc}}/\partial T\)는 해당 Li-reference half-cell
반응 엔트로피이며, \(I>0\)은 하프셀 방전/graphite lithiation
전류다. 이 좌표에서는
\(\dot Q_{{rev}}=-I T\,\partial U_{{oc}}/\partial T\)가 예제와
생산 함수에서 일치한다.

그러나 curve API의 `direction="discharge"`는 graphite
delithiation을 뜻한다. 문건과 docstring이 두 discharge 라벨의 반대
화학 방향을 공개했지만 `reversible_heat(..., I)`는 이 반응 좌표를
타입이나 state로 강제하지 않는다. full-cell 방전으로 옮길 때
\(U_{{cell}}=U_{{cat}}-U_{{an}}\)이므로 graphite 몫은
\(+I_{{cell}}T\,\partial U_{{an}}/\partial T\)이고, 총열은 cathode
계수까지 있어야 한다. graphite-only 표를 full-cell 총열로 읽으면
안 된다.

v1.0.14 LCO 감사의 reference, DOS gate, 조성 의존과 \(T^2\) 곡률
blocker는 heat AST가 동일하므로 하나도 수리되지 않았다.

## 인용 권위와 본문 경계

Hales–Bulman 2024(DOI `10.1149/1945-7111/ad4918`)는 full-cell entropy
coefficient의 표준 potentiometric 추출법을 지지한다. 이 문헌은
현재 4-transition graphite prior의 \(+60.8\) mW/A 부호·규모를
실험 검증하지 않는다. 따라서 해당 문장의 “calorimetry 관측과
정합”은 구체적 외부 검증 주장으로는 기각한다.

또한 새 worked section은 생산 코드와 함수명을 직접 두 번 언급한다.
사용자의 “이론 문건 본문은 물리·화학만, 코드 언급은 통제 절에만”
제약을 통과하지 못한다. 최종 이론 정본에서는 독립 수치 검산으로
서술하고 코드명은 제거해야 한다.

## 다음 단계

Step 37.4에서 v1.0.16의 \(n(T)=n_0+n_1(T-T_{{ref}})\)를 microscopic
물리가 아닌 empirical width law와 분리하고,
\(\partial w/\partial T=(R/F)(n+Tn')\), entropy propagation,
positivity와 parameter correlation을 검산한다.

원본 `Claude/`, `main`은 수정하지 않았다.
"""
    REPORT.write_text(report, encoding="utf-8")
    print(result["status"])
    print(
        "worked xbar=0.25:",
        f"U={point['U_oc_V']:.12g}",
        f"dUdT={point['code_entropy_coefficient_V_per_K']:.12g}",
        f"q/I={point['qrev_per_I_V']:.12g}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
