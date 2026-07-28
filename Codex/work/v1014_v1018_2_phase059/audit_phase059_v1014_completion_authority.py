#!/usr/bin/env python3
"""Adjudicate v1.0.14 convergence and completion claims against Steps 36.1–36.4."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RESULT = ROOT / "Claude/results/V1014_RESULT.md"
HANDOVER = ROOT / "Claude/docs/v1.0.14/HANDOVER_v1.0.14.md"
KICKOFF = ROOT / "Claude/docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md"
LEDGER = ROOT / "Claude/results/process/V1014_EXECUTION_LEDGER.md"
PROCESS_DIR = ROOT / "Claude/results/process"

REGISTER = ROOT / "Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json"
PHASE_SEPARATION = (
    ROOT / "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json"
)
LCO_HEAT = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json"
KINETICS = ROOT / "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json"

OUTPUT = ROOT / "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_REVIEW.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def source_line(path: Path, needle: str) -> dict[str, Any]:
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if needle in line:
            return {
                "path": str(path.relative_to(ROOT)),
                "line": number,
                "needle": needle,
                "source_line": line,
            }
    raise RuntimeError(f"needle not found in {path}: {needle}")


def claim(
    claim_id: str,
    topic: str,
    historical_claim: str,
    disposition: str,
    authority_scope: str,
    evidence: list[dict[str, Any]],
    blocker_families: list[str],
    rationale: str,
) -> dict[str, Any]:
    return {
        "id": claim_id,
        "topic": topic,
        "historical_claim": historical_claim,
        "disposition": disposition,
        "authority_scope": authority_scope,
        "source_evidence": evidence,
        "blocker_families": blocker_families,
        "rationale": rationale,
    }


def main() -> int:
    review_files = sorted(PROCESS_DIR.glob("V1014_REVIEW_R*.md"))
    process_files = sorted(PROCESS_DIR.glob("V1014_*.md"))
    source_files = [RESULT, HANDOVER, KICKOFF, *process_files]
    unique_source_files = list(dict.fromkeys(source_files))
    before = {
        str(path.relative_to(ROOT)): sha256(path) for path in unique_source_files
    }

    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    phase_separation = json.loads(PHASE_SEPARATION.read_text(encoding="utf-8"))
    lco_heat = json.loads(LCO_HEAT.read_text(encoding="utf-8"))
    kinetics = json.loads(KINETICS.read_text(encoding="utf-8"))

    blocker_families = {
        "theory_boundary": {
            "source": str(REGISTER.relative_to(ROOT)),
            "status": register["status"],
            "finding_count": register["summary"]["decision_count"],
            "decisive_metrics": {
                "outside_boundary_violations": register["summary"][
                    "v1014_outside_boundary_violation_count"
                ],
                "inside_allowed_section_lines": register["summary"][
                    "v1014_inside_allowed_implementation_line_count"
                ],
                "theory_only_boundary_pass": register["summary"][
                    "theory_only_boundary_pass"
                ],
            },
        },
        "phase_separation": {
            "source": str(PHASE_SEPARATION.relative_to(ROOT)),
            "status": phase_separation["status"],
            "finding_count": phase_separation["summary"]["finding_count"],
            "decisive_metrics": {
                "dimensional_closure_pass": phase_separation["summary"][
                    "dimensional_closure_pass"
                ],
                "boundary_condition_closure_pass": phase_separation["summary"][
                    "boundary_condition_closure_pass"
                ],
                "elasticity_scope_closure_pass": phase_separation["summary"][
                    "elasticity_scope_closure_pass"
                ],
            },
        },
        "lco_heat": {
            "source": str(LCO_HEAT.relative_to(ROOT)),
            "status": lco_heat["status"],
            "finding_count": lco_heat["summary"]["finding_count"],
            "decisive_metrics": {
                "half_cell_reference_closure_pass": lco_heat["summary"][
                    "half_cell_reference_closure_pass"
                ],
                "electronic_gate_external_validation_pass": lco_heat["summary"][
                    "electronic_gate_external_validation_pass"
                ],
                "theory_code_electronic_conformance_pass": lco_heat["summary"][
                    "theory_code_electronic_conformance_pass"
                ],
                "doped_high_voltage_coverage_pass": lco_heat["summary"][
                    "doped_high_voltage_coverage_pass"
                ],
            },
        },
        "kinetics": {
            "source": str(KINETICS.relative_to(ROOT)),
            "status": kinetics["summary"]["status"],
            "finding_count": kinetics["summary"]["finding_count"],
            "decisive_metrics": {
                "constant_current_unit_contract_pass": kinetics["summary"][
                    "constant_current_unit_contract_pass"
                ],
                "closed_galvanostatic_forward_model_pass": kinetics["summary"][
                    "closed_galvanostatic_forward_model_pass"
                ],
                "local_potential_barrier_pass": kinetics["summary"][
                    "local_potential_barrier_pass"
                ],
                "default_current_broadening_pass": kinetics["summary"][
                    "default_current_broadening_pass"
                ],
                "default_lowT_finite_current_joint_limit_pass": kinetics[
                    "summary"
                ]["default_lowT_finite_current_joint_limit_pass"],
                "zero_current_limit_all_paths_pass": kinetics["summary"][
                    "zero_current_limit_all_paths_pass"
                ],
                "frozen_rate_limit_pass": kinetics["summary"][
                    "frozen_rate_limit_pass"
                ],
            },
        },
    }

    claims = [
        claim(
            "P059-V1014-AUTH-001",
            "release_workflow",
            "v1.0.14 production and review workflow was completed.",
            "PRESERVE_PROCESS_COMPLETION",
            "PROCESS_ONLY",
            [
                source_line(RESULT, "v1.0.14 완주."),
                source_line(HANDOVER, "P6.1 마감"),
            ],
            [],
            (
                "The versioned sources, review rounds, artifacts, result, and "
                "handover exist. Completion is valid as a historical workflow "
                "statement, not as a scientific certification."
            ),
        ),
        claim(
            "P059-V1014-AUTH-002",
            "build_gate",
            "The three documents built without reported TeX/reference/layout errors.",
            "PRESERVE_INTERNAL_VALIDATION",
            "BUILD_AND_LAYOUT_ONLY",
            [source_line(RESULT, "ch1 0-err/57p")],
            [],
            (
                "A successful build supports artifact integrity. It does not "
                "test dimensions, constitutive closure, literature attribution, "
                "or material validity."
            ),
        ),
        claim(
            "P059-V1014-AUTH-003",
            "regression_gate",
            "The 13/13 bit-exact regression gate passed.",
            "PRESERVE_INTERNAL_VALIDATION",
            "LEGACY_OUTPUT_IDENTITY_ONLY",
            [
                source_line(RESULT, "회귀 13/13 bit-exact"),
                source_line(HANDOVER, "회귀 = `python test_regression_graphite.py`"),
            ],
            ["kinetics"],
            (
                "The regression proves compatibility with the stored legacy "
                "baseline. The independently confirmed v1.0.10→v1.0.14 kinetic "
                "AST identity shows why it cannot establish that inherited "
                "physics is correct."
            ),
        ),
        claim(
            "P059-V1014-AUTH-004",
            "sample_demo_gate",
            "Finite graph-suite, sample, and demo checks establish the release gate.",
            "PRESERVE_INTERNAL_VALIDATION",
            "FINITE_AND_SELF_CONSISTENT_OUTPUT_ONLY",
            [source_line(RESULT, "graph_suite ALL FINITE")],
            ["lco_heat", "kinetics"],
            (
                "Finite output and agreement with an internally selected sample "
                "target are not external LCO, graphite, silicon, or full-cell "
                "validation."
            ),
        ),
        claim(
            "P059-V1014-AUTH-005",
            "textbook_register",
            "v1.0.14 materially improved pedagogy, derivation structure, and register.",
            "PRESERVE_PEDAGOGICAL_ASSET",
            "EXPOSITION_ONLY",
            [
                source_line(RESULT, "Hill 면밀 유도"),
                source_line(RESULT, "P3.1 절별 루핑"),
            ],
            ["theory_boundary"],
            (
                "The exact-diff audit confirms substantial pedagogical work. "
                "This asset remains useful even though the final theory-only "
                "boundary is not yet satisfied."
            ),
        ),
        claim(
            "P059-V1014-AUTH-006",
            "theory_code_boundary",
            "The main body contains zero code mentions after moving implementation material.",
            "NARROW_LITERAL_COUNT_ONLY_GLOBAL_CLAIM_REJECTED",
            "LITERAL_MACRO_COUNT_NOT_SEMANTIC_BOUNDARY",
            [
                source_line(RESULT, "본문 코드 언급 0"),
                source_line(RESULT, "본문 \\code 0"),
            ],
            ["theory_boundary"],
            (
                "The narrow literal-macro statement can be retained, but the "
                "semantic theory-only claim fails: 24 implementation-language "
                "violations remain outside the allowed section."
            ),
        ),
        claim(
            "P059-V1014-AUTH-007",
            "review_convergence",
            "Seven rounds converged sufficiently to close P4.1.",
            "PRESERVE_REVIEW_PROCESS_CLOSURE_ONLY",
            "DEFINED_REVIEW_LENSES_ONLY",
            [
                source_line(RESULT, "라운드 궤적: 22→13→16→8→18→13→8"),
                source_line(LEDGER, "P4.1 종결 선언"),
            ],
            [
                "theory_boundary",
                "phase_separation",
                "lco_heat",
                "kinetics",
            ],
            (
                "The declared review process ended, but the finding counts are "
                "not monotone and the stated consecutive-zero criterion was not "
                "met. Process closure cannot be promoted to open-ended scientific "
                "convergence."
            ),
        ),
        claim(
            "P059-V1014-AUTH-008",
            "zero_physics_defects",
            "There were no physical defects after review round 2.",
            "REJECT_GLOBAL_SCIENTIFIC_CLAIM",
            "NONE",
            [
                source_line(RESULT, "물리 실결함 R2 이후 0"),
                source_line(LEDGER, "물리 실결함 은 R2 이후 0"),
            ],
            [
                "phase_separation",
                "lco_heat",
                "kinetics",
            ],
            (
                "Independent dimensional, reference-electrode, electronic-gate, "
                "constant-current, local-affinity, zero-current, and frozen-rate "
                "failures directly contradict a global zero-defect statement."
            ),
        ),
        claim(
            "P059-V1014-AUTH-009",
            "corner_cases",
            "About 90 corner cases had zero failures.",
            "PRESERVE_SAMPLED_REVIEW_RESULT_ONLY",
            "ENUMERATED_ASSERTIONS_ONLY",
            [
                source_line(RESULT, "코너 케이스 ~90항 전수 FAIL 0"),
                source_line(LEDGER, "코너 케이스 90항 전수 FAIL 0"),
            ],
            ["phase_separation", "lco_heat", "kinetics"],
            (
                "This can be true for the enumerated list while remaining "
                "incomplete. The later independent audits exercised contracts "
                "outside that list and found decisive failures."
            ),
        ),
        claim(
            "P059-V1014-AUTH-010",
            "phase_separation_appendix",
            "The phase-separation appendix is a self-contained, adversarially rederived result.",
            "PARTIAL_CORE_ALGEBRA_PRESERVED_CLOSURE_REJECTED",
            "REDUCED_REGULAR_SOLUTION_CORE_ONLY",
            [source_line(RESULT, "binodal·spinodal·Maxwell")],
            ["phase_separation"],
            (
                "Regular-solution and linear Cahn–Hilliard algebra are useful, "
                "but molar/volumetric conversion, explicit boundary conditions, "
                "elasticity scope, and connection to the production peak model "
                "remain open."
            ),
        ),
        claim(
            "P059-V1014-AUTH-011",
            "reference_gate",
            "All new bibliography entries were DOI-checked and reference handling was complete.",
            "PARTIAL_BIBLIOGRAPHIC_CHECK_NOT_CLAIM_VALIDATION",
            "BIBLIOGRAPHIC_IDENTITY_ONLY",
            [
                source_line(RESULT, "전건 DOI Crossref 검증"),
                source_line(RESULT, "ml2024 tier A 원문 대조"),
            ],
            ["lco_heat"],
            (
                "DOI identity does not validate use of a value. The ml2024 "
                "article number is wrong in v1.0.14, and the source itself does "
                "not validate the MIT gate."
            ),
        ),
        claim(
            "P059-V1014-AUTH-012",
            "gmax_tier",
            "g_max=13 should remain tier A based on prior review history.",
            "REJECT_UNVERIFIED_TIER_A_PROMOTION",
            "UNVERIFIED_NUMERICAL_ANCHOR",
            [
                source_line(RESULT, "g_max=13 tier A 유지"),
                source_line(LEDGER, "g_max=13 tier A 유지"),
            ],
            ["lco_heat"],
            (
                "The historical source audit itself says the numerical value "
                "was not directly recovered from the primary paper. Prior review "
                "history is not evidence for a quantitative tier-A assignment."
            ),
        ),
        claim(
            "P059-V1014-AUTH-013",
            "lco_heat_sample",
            "The -45.68 versus -46 sample validates the LCO heat path.",
            "PRESERVE_CODE_SELF_CONSISTENCY_EXTERNAL_GATE_REJECTED",
            "INTERNAL_SYNTHETIC_SAMPLE_ONLY",
            [source_line(RESULT, "sample(-45.68@목표 −46)")],
            ["lco_heat"],
            (
                "The algebraic heat identity is preserved, but the independent "
                "audit found a reference-electrode conflation and an unvalidated "
                "electronic gate. The sample cannot serve as material validation."
            ),
        ),
        claim(
            "P059-V1014-AUTH-014",
            "lco_high_voltage_scope",
            "The LCO treatment supports the intended high-voltage material scope.",
            "REJECT_MATERIAL_SCOPE_COMPLETION",
            "NONE",
            [
                source_line(RESULT, "LCO Ω^cat/dH_a 배정"),
                source_line(HANDOVER, "LCO Ω^cat/dH_a 배정"),
            ],
            ["lco_heat"],
            (
                "The result and handover admit that LCO parameters remain open. "
                "No dopant state variable or validated doped high-voltage fitting "
                "path exists in v1.0.14."
            ),
        ),
        claim(
            "P059-V1014-AUTH-015",
            "finite_current_broadening",
            "The width budget and kinetic tail close finite-current broadening.",
            "REJECT_SHIPPED_MODEL_COMPLETION",
            "REDUCED_CAUSAL_SKELETON_ONLY",
            [source_line(RESULT, "eq:widthbudget")],
            ["kinetics"],
            (
                "The causal first-order skeleton is useful, but the hour/second "
                "factor, frozen affinity, dormant default rate shape, grid handoff, "
                "and lack of galvanostatic closure prevent the claimed physical "
                "completion."
            ),
        ),
        claim(
            "P059-V1014-AUTH-016",
            "low_temperature_finite_current_target",
            "The v1.0.14 model is physically verified for the target peak morphology.",
            "REJECT_TARGET_COMPLETION",
            "NONE",
            [source_line(RESULT, "물리·좌표는 검증 완료")],
            ["kinetics"],
            (
                "The shipped default gives identical 0.1C and 1C shapes, and "
                "low temperature makes the audited peak taller and narrower. "
                "It therefore fails the user's joint suppression/broadening target."
            ),
        ),
        claim(
            "P059-V1014-AUTH-017",
            "potential_dependent_barrier",
            "The activation-barrier construction represents the intended local potential dependence.",
            "REJECT_FROZEN_AFFINITY_CLOSURE",
            "NONE",
            [source_line(RESULT, "꼬리 문턱 수치 코드 재검산 통일")],
            ["kinetics"],
            (
                "The implemented affinity is frozen at a transition cut, making "
                "the implemented local derivative of ln L_q with voltage zero. "
                "The user's central potential-dependent-barrier hypothesis is "
                "therefore absent from the calculation."
            ),
        ),
        claim(
            "P059-V1014-AUTH-018",
            "legacy_blocker_repair",
            "v1.0.14 review rounds repaired the inherited v1.0.10 kinetic core.",
            "REJECT_REPAIR_CLAIM_COPY_FORWARD_CONFIRMED",
            "NONE",
            [source_line(RESULT, "누적 확정 정정 ~98건")],
            ["kinetics"],
            (
                "Four core kinetic functions have identical executable ASTs in "
                "v1.0.10 and v1.0.14. Review volume and documentation changes do "
                "not constitute an executable physics repair."
            ),
        ),
        claim(
            "P059-V1014-AUTH-019",
            "open_items",
            "Scientific and data-validation items remained for later work.",
            "PRESERVE_BLOCKER_ADMISSION",
            "OPEN_WORK_REGISTER",
            [
                source_line(RESULT, "v1.0.13 인계분 4건 유지"),
                source_line(HANDOVER, "이월(실데이터 단계)"),
            ],
            ["phase_separation", "lco_heat", "kinetics"],
            (
                "The open-item list is a reliable admission that multi-temperature, "
                "LCO parameter, numerical, mapping, and primary-source work was "
                "not complete."
            ),
        ),
        claim(
            "P059-V1014-AUTH-020",
            "final_authority",
            "v1.0.14 is complete in the sense required for scientific authority.",
            "REJECT_SCIENTIFIC_COMPLETION_AUTHORITY",
            "PROCESS_COMPLETE_SCIENCE_CONDITIONAL",
            [
                source_line(RESULT, "**v1.0.14 완주.**"),
                source_line(HANDOVER, "코드 업데이트: 필요 판정"),
            ],
            [
                "theory_boundary",
                "phase_separation",
                "lco_heat",
                "kinetics",
            ],
            (
                "Workflow completion is preserved, but all four independent "
                "blocker families contain unresolved failures. v1.0.14 is a "
                "valuable pedagogical and historical asset, not a scientific "
                "authority or the final theory/code basis."
            ),
        ),
    ]

    disposition_counts = dict(
        sorted(Counter(item["disposition"] for item in claims).items())
    )
    authority_scope_counts = dict(
        sorted(Counter(item["authority_scope"] for item in claims).items())
    )
    finding_total = sum(
        family["finding_count"] for family in blocker_families.values()
    )

    data = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "phase": 59,
        "step": "36.5",
        "scope": (
            "v1.0.14 review convergence, zero-physics-defect, completion, "
            "and authority claims adjudicated against Phase 059 Steps 36.1–36.4"
        ),
        "status": (
            "CONDITIONAL_P059_V1014_PROCESS_COMPLETE_BUT_SCIENTIFIC_"
            "COMPLETION_AUTHORITY_REJECTED"
        ),
        "authority_boundary": (
            "This audit preserves demonstrated workflow, build, and legacy "
            "regression facts while rejecting their promotion to scientific "
            "or material-validation authority."
        ),
        "source_contracts": {
            "process_file_count": len(process_files),
            "review_report_count": len(review_files),
            "authority_source_file_count": len(unique_source_files),
            "authority_source_line_count": sum(
                line_count(path) for path in unique_source_files
            ),
            "review_trajectory_reported": [22, 13, 16, 8, 18, 13, 8],
            "review_trajectory_monotone_nonincreasing": False,
            "declared_consecutive_zero_round_criterion_met": False,
            "result_open_item_line_present": True,
            "handover_code_update_required_line_present": True,
        },
        "adjudication_rules": [
            "Process completion is not scientific completion.",
            "A build, finite-output, regression, round-trip, or synthetic sample gate proves only its explicit internal property.",
            "Review convergence is relative to the lenses and test list used; untested contracts remain open.",
            "A source citation or DOI check does not validate numerical attribution or material applicability.",
            "An explicit carry-forward item contradicts a global completion claim for that scientific scope.",
            "Copy-forward executable physics creates no new validation authority.",
        ],
        "blocker_families": blocker_families,
        "claims": claims,
        "summary": {
            "status": (
                "CONDITIONAL_P059_V1014_PROCESS_COMPLETE_BUT_SCIENTIFIC_"
                "COMPLETION_AUTHORITY_REJECTED"
            ),
            "claim_count": len(claims),
            "disposition_counts": disposition_counts,
            "authority_scope_counts": authority_scope_counts,
            "independent_blocker_family_count": len(blocker_families),
            "independent_finding_count": finding_total,
            "process_completion_preserved": True,
            "build_and_internal_regression_preserved": True,
            "pedagogical_asset_preserved": True,
            "global_zero_physics_defect_claim_pass": False,
            "scientific_convergence_claim_pass": False,
            "scientific_completion_authority_pass": False,
            "material_validation_pass": False,
            "final_theory_code_basis_pass": False,
            "next_step": "37.1",
        },
        "source_hashes_before": before,
    }

    report_lines = [
        "# Phase 059 v1.0.14 완주·수렴·과학적 권위 재판정",
        "",
        "## 판정",
        "",
        (
            "`CONDITIONAL_P059_V1014_PROCESS_COMPLETE_BUT_SCIENTIFIC_"
            "COMPLETION_AUTHORITY_REJECTED`"
        ),
        "",
        (
            "v1.0.14는 **작업 절차와 릴리스 제작의 완료본**이다. 다만 "
            "**과학적으로 완결된 정본은 아니다**. 빌드, 회귀, 유한 출력, "
            "문서 검수와 경연 산출은 실제 내부 성과로 보존한다. 반면 "
            "“R2 이후 물리 실결함 0”, “물리·좌표 검증 완료”, “완주”를 "
            "재료 물리와 코드의 외부 타당성까지 포함하는 전역 선언으로 "
            "읽는 것은 기각한다."
        ),
        "",
        "## 왜 옛 검수가 결함을 놓쳤는가",
        "",
        (
            "옛 R1–R7은 문건 안에서 선언한 식, 그림 좌표, 정해진 코너 "
            "케이스와 레거시 출력을 매우 많이 확인했다. 그러나 검증 "
            "목록 자체의 완전성은 증명하지 않았다. 이후 독립 감사는 "
            "서로 다른 질문—단위계 경계, 기준전극, 국소 affinity, "
            "영전류·동결 극한, Cahn–Hilliard 경계조건, 도핑 재료 범위—을 "
            "물었고, 그 지점에서 실패가 드러났다."
        ),
        "",
        (
            "또한 보고된 발견 수 `22→13→16→8→18→13→8`은 수치상 "
            "단조 감소가 아니며, 실행 원장도 원래의 “연속 2라운드 "
            "0건” 기준을 충족하지 않았음을 직접 인정한다. 따라서 당시 "
            "종결은 검수 프로세스의 종료로는 유효하지만 과학적 수렴의 "
            "증거로는 부족하다."
        ),
        "",
        "## 독립 blocker 대조",
        "",
        "| Family | Findings | Decisive failure |",
        "|---|---:|---|",
        (
            f"| theory boundary | {blocker_families['theory_boundary']['finding_count']} "
            f"| 허용 절 밖 구현 언어 "
            f"{register['summary']['v1014_outside_boundary_violation_count']}건; "
            "theory-only gate FAIL |"
        ),
        (
            f"| phase separation | {blocker_families['phase_separation']['finding_count']} "
            "| 몰/부피 차원 폐쇄, 명시 경계조건, 탄성 범위 FAIL |"
        ),
        (
            f"| LCO/heat | {blocker_families['lco_heat']['finding_count']} "
            "| 기준전극·DOS gate·이론–코드·도핑 고전압 범위 FAIL |"
        ),
        (
            f"| kinetics | {blocker_families['kinetics']['finding_count']} "
            "| 3600 단위 인자, frozen affinity, 기본 rate 무효, "
            "영전류·동결 극한과 galvanostatic closure FAIL |"
        ),
        "",
        f"독립 finding은 네 계열 합계 {finding_total}건이다. 이는 옛 "
        "review 문구의 오탈자 재집계가 아니라 서로 다른 물리 계약의 "
        "독립 판정 수다.",
        "",
        "## 주장별 처분",
        "",
        "| ID | Topic | Disposition | Authority |",
        "|---|---|---|---|",
    ]
    for item in claims:
        report_lines.append(
            f"| {item['id']} | {item['topic']} | "
            f"{item['disposition']} | {item['authority_scope']} |"
        )

    report_lines.extend(
        [
            "",
            "## 보존하는 것",
            "",
            "- v1.0.14의 교재형 설명, 통계역학 전개, 그림과 편집 성과",
            "- 문서 빌드·참조·레이아웃 gate와 레거시 출력 회귀 사실",
            "- regular-solution/Cahn–Hilliard 핵심 대수와 1차 causal "
            "relaxation의 축약 골격",
            "- 이월 목록이 정직하게 기록한 미완 과제",
            "",
            "## 권위로 승격하지 않는 것",
            "",
            "- `13/13 bit-exact`, `ALL FINITE`, synthetic sample PASS를 "
            "실험·재료 검증으로 읽는 것",
            "- `\\code` 매크로 0건을 의미론적 theory-only 본문 완성으로 읽는 것",
            "- DOI 확인을 정량값·적용범위 검증으로 읽는 것",
            "- review round 종료를 “물리 오류 0” 또는 최종 이론–코드 "
            "정합으로 읽는 것",
            "",
            "## 최종 권위 위치",
            "",
            (
                "v1.0.14는 폐기할 문건이 아니다. 이후 정본에 가져갈 "
                "**교육적·대수적 자산**과 고쳐야 할 **물리 폐쇄 결함**을 "
                "동시에 가진 중간 기준선이다. 따라서 다음 버전 감사에서는 "
                "v1.0.14의 `PASS` 문구를 출발 증거로 재사용하지 않고, 각 "
                "blocker가 실제 source/code/test/data에서 닫혔는지를 "
                "개별 판정한다."
            ),
            "",
            "다음 정확한 단계는 Step 37.1: v1.0.15 pointwise "
            "continuous-memory 식의 독립 유도와 기존 grid-switch 대비다.",
            "",
            "원본 `Claude/`, `main`과 생산 이론·코드는 수정하지 않았다.",
        ]
    )

    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    after = {
        str(path.relative_to(ROOT)): sha256(path) for path in unique_source_files
    }
    data["source_hashes_after"] = after
    data["source_unchanged"] = before == after
    OUTPUT.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
