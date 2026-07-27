#!/usr/bin/env python3
"""Generate the Phase 059 completion/authority/carry-forward claim audit."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
DIFF_INDEX = RESULTS / "PHASE_059_THEORY_LINEAGE_DIFF.json"
OUTPUT = RESULTS / "PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json"
SUMMARY = RESULTS / "PHASE_059_COMPLETION_AUTHORITY_REVIEW.md"

V14_HO = "Claude/docs/v1.0.14/HANDOVER_v1.0.14.md"
V15_KO = "Claude/docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md"
V15_CLOSE = "Claude/docs/v1.0.15/CLOSING_v1.0.15.md"
V15_HO = "Claude/docs/v1.0.15/HANDOVER_v1.0.15.md"
V16_GUIDE = "Claude/docs/v1.0.16/FITTING_GUIDE.md"
V16_HO = "Claude/docs/v1.0.16/HANDOVER_v1.0.16.md"
V17_HO = "Claude/docs/v1.0.17/HANDOVER_v1.0.17.md"
V181_HO = "Claude/docs/v1.0.18.1/HANDOVER_v1.0.18.1.md"
V182_GUIDE = "Claude/docs/v1.0.18.2/FITTING_GUIDE.md"
V182_HO = "Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md"
V182_ROAD = "Claude/docs/v1.0.18.2/ROADMAP_future_physics.md"

ALLOWED_CLASSES = {
    "USER_REQUIREMENT",
    "PROCESS_HISTORY",
    "THEORY_CHANGE",
    "IMPLEMENTATION_CHANGE",
    "INTERNAL_VALIDATION",
    "SCIENTIFIC_SCOPE",
    "CARRY_FORWARD",
    "EXTERNAL_REVIEW",
}
ALLOWED_DISPOSITIONS = {
    "PRESERVE_REQUIREMENT",
    "PATCH_CONFIRMED",
    "PATCH_CONFIRMED_INTERNAL_ONLY",
    "SOURCE_STATEMENT_ONLY",
    "COPY_FORWARD_NO_NEW_VALIDATION",
    "PARTIAL",
    "OVERCLAIMED",
    "CARRY_FORWARD_OPEN",
    "REVIEW_INPUT_NOT_AUTHORITY",
    "SUPERSEDED",
}


def src(path: str, line: int, needle: str) -> dict:
    return {"path": path, "line": line, "needle": needle}


def claim(
    claim_id: str,
    version: str,
    actor: str,
    claim_class: str,
    statement: str,
    sources: list[dict],
    disposition: str,
    authority_meaning: str,
    remaining_work: str,
    *,
    patch_ids: list[str] | None = None,
    contract_ids: list[str] | None = None,
    evidence_boundary: str = "SOURCE_TEXT_ONLY",
) -> dict:
    return {
        "id": claim_id,
        "version": version,
        "actor": actor,
        "claim_class": claim_class,
        "claim": statement,
        "source_specs": sources,
        "patch_ids": patch_ids or [],
        "contract_ids": contract_ids or [],
        "disposition": disposition,
        "evidence_boundary": evidence_boundary,
        "authority_meaning": authority_meaning,
        "remaining_work": remaining_work,
    }


CLAIMS = [
    claim(
        "P059-CLM-001", "v1.0.15", "USER", "USER_REQUIREMENT",
        "The manuscript must simultaneously have textbook register, review-paper depth, and equation-led exposition.",
        [src(V15_CLOSE, 9, "교과서 register")],
        "PRESERVE_REQUIREMENT",
        "Binding authorial direction recovered from a user-verbatim constitution; it is not a scientific validation result.",
        "Apply this as a final-manuscript acceptance gate.",
    ),
    claim(
        "P059-CLM-002", "v1.0.15", "USER", "USER_REQUIREMENT",
        "The theory body must not narrate version history, work phases, or implementation identifiers.",
        [src(V15_CLOSE, 13, "자기 diff"), src(V15_CLOSE, 15, "코드 함수명")],
        "PRESERVE_REQUIREMENT",
        "Binding manuscript-boundary requirement.",
        "Keep implementation traceability in separate conformance artifacts and the controlled correspondence section only.",
    ),
    claim(
        "P059-CLM-003", "v1.0.15", "USER", "USER_REQUIREMENT",
        "Derivations must expose assumptions, intermediate operations, dimensions, signs, and limits without assert-jumps.",
        [src(V15_CLOSE, 19, "완결 유도"), src(V15_CLOSE, 25, "중간식")],
        "PRESERVE_REQUIREMENT",
        "Binding exposition and derivation requirement.",
        "Use independent derivations and limiting-case checks before promoting equations into the final manuscript.",
    ),
    claim(
        "P059-CLM-004", "v1.0.15", "USER", "USER_REQUIREMENT",
        "Measured validation and internal self-consistency must be reported as different evidence classes.",
        [src(V15_CLOSE, 20, "실측 검증 vs 자기일관성 검증")],
        "PRESERVE_REQUIREMENT",
        "Binding evidence-language rule and the central authority boundary for this audit.",
        "Label every future gate as algebraic, numerical, literature, or experimental evidence.",
    ),
    claim(
        "P059-CLM-005", "v1.0.15", "USER", "PROCESS_HISTORY",
        "Past plans, handovers, ledgers, results, and current sources must be read before raising a new issue or starting a revision.",
        [src(V15_CLOSE, 39, "과거 세션"), src(V15_CLOSE, 44, "과거 이력")],
        "PRESERVE_REQUIREMENT",
        "Binding workflow requirement created after earlier history-loss failures.",
        "Continue the content-addressed lineage audit and checkpoint ledger.",
    ),
    claim(
        "P059-CLM-006", "v1.0.15", "USER", "PROCESS_HISTORY",
        "Import, grep, or sample success cannot justify completion or a golden baseline without analytic limits, convergence, and round-trip checks.",
        [src(V15_CLOSE, 59, "검증 없이"), src(V15_CLOSE, 60, "해석적 극한")],
        "PRESERVE_REQUIREMENT",
        "Binding validation standard.",
        "Re-execute each claimed gate and classify what it actually proves.",
    ),
    claim(
        "P059-CLM-007", "v1.0.15", "USER", "PROCESS_HISTORY",
        "Phase results and ledgers are recovery points against compaction loss; work should be committed frequently.",
        [src(V15_CLOSE, 105, "컴팩션 환각")],
        "PRESERVE_REQUIREMENT",
        "Binding provenance requirement; a push claim is still a repository-state fact that must be checked independently.",
        "Commit every closed substep; report local and remote state separately.",
    ),
    claim(
        "P059-CLM-008", "v1.0.14", "PAST_AGENT", "PROCESS_HISTORY",
        "v1.0.14 was described as a completed six-phase pass with about 98 corrections and a figure competition.",
        [src(V14_HO, 11, "누적 ~98건")],
        "SOURCE_STATEMENT_ONLY",
        "The source and exact diff confirm a large revision occurred, but counts and scientific completeness are narrative process claims.",
        "Do not promote this completion wording into scientific authority.",
        patch_ids=["ch1_v1013_to_v1014", "ch2_v1013_to_v1014"],
    ),
    claim(
        "P059-CLM-009", "v1.0.14", "USER", "USER_REQUIREMENT",
        "v1.0.14 established textbook/major-journal register, detailed derivation, a separate spinodal appendix, and one-way theory-to-code linkage.",
        [src(V14_HO, 6, "교과서·메이저 저널급"), src(V14_HO, 15, "별도 문건으로 유지")],
        "PRESERVE_REQUIREMENT",
        "Authorial direction is confirmed; exact patches show the appendix and controlled correspondence structure, not their scientific validity.",
        "Retain the register and separation decisions while re-deriving the physics.",
        patch_ids=["ch1_v1013_to_v1014", "ch2_v1013_to_v1014"],
    ),
    claim(
        "P059-CLM-010", "v1.0.14", "PAST_AGENT", "CARRY_FORWARD",
        "Multi-temperature T-squared behavior, LCO Omega and activation enthalpy, current-grid choices, composition mapping, and primary literature remained open.",
        [src(V14_HO, 18, "이월(실데이터 단계)")],
        "CARRY_FORWARD_OPEN",
        "Explicit unresolved scope, not a completed result.",
        "Route all surviving items into experimental, literature, code, and model-repair queues.",
        contract_ids=["P059-CON-033", "P059-CON-036", "P059-CON-038"],
    ),
    claim(
        "P059-CLM-011", "v1.0.14", "PAST_AGENT", "PROCESS_HISTORY",
        "A final code update was still judged necessary and was waiting for approval.",
        [src(V14_HO, 17, "GO 대기")],
        "SOURCE_STATEMENT_ONLY",
        "This directly prevents v1.0.14 prose completion from being read as final code conformance.",
        "Audit the subsequent implementation deltas in Step 34.",
    ),
    claim(
        "P059-CLM-012", "v1.0.15", "USER", "USER_REQUIREMENT",
        "The artificial voltage work grid had to be removed completely in favor of evaluating the actual separated electrode sample voltages.",
        [src(V15_KO, 8, "극판 성분의 전압값"), src(V15_KO, 9, "완전 퇴출")],
        "PRESERVE_REQUIREMENT",
        "Direct user architecture decision.",
        "Preserve pointwise evaluation but repair its trajectory/history contract for repeated or nonmonotone voltage.",
        contract_ids=["P059-CON-017", "P059-CON-018", "P059-CON-019"],
    ),
    claim(
        "P059-CLM-013", "v1.0.15", "PAST_AGENT", "PROCESS_HISTORY",
        "The old grid, switch, jump, and interpolation were acknowledged as implementation-derived artifacts rather than physical necessities.",
        [src(V15_KO, 16, "구현 편의")],
        "PATCH_CONFIRMED",
        "The exact Ch1 patch removes eq:vwork, eq:lowpass, and eq:branch and adds the pointwise memory derivation.",
        "Code-side deletion and runtime behavior remain Step 34 evidence.",
        patch_ids=["ch1_v1014_to_v1015"],
        evidence_boundary="THEORY_PATCH_CONFIRMED_CODE_EXECUTION_DEFERRED",
    ),
    claim(
        "P059-CLM-014", "v1.0.15", "PAST_AGENT", "THEORY_CHANGE",
        "v1.0.15 replaced the grid branch with a pointwise causal-memory formulation and an explicit L_V to zero limit.",
        [src(V15_HO, 15, "eq:memory/lag/tail-limit"), src(V15_HO, 17, "점별 재아키텍처")],
        "PATCH_CONFIRMED",
        "The exact Ch1 diff confirms the stated equation removals/additions; this proves a source change, not physical adequacy.",
        "Resolve nonmonotone traversal, finite-window initial history, and local voltage mapping.",
        patch_ids=["ch1_v1014_to_v1015"],
        contract_ids=["P059-CON-017", "P059-CON-018", "P059-CON-019"],
        evidence_boundary="THEORY_PATCH_CONFIRMED_PHYSICAL_CLOSURE_OPEN",
    ),
    claim(
        "P059-CLM-015", "v1.0.15", "PAST_AGENT", "IMPLEMENTATION_CHANGE",
        "The production code was reported to remove the work grid, reverse interpolation, low-pass recurrence, switching parameter, and dead functions.",
        [src(V15_HO, 17, "dead 삭제")],
        "SOURCE_STATEMENT_ONLY",
        "A handover reports this implementation patch, but Step 33 does not independently certify code behavior.",
        "Perform AST/exact-diff/runtime review in Step 34.",
        evidence_boundary="CODE_DIFF_AND_EXECUTION_DEFERRED_STEP_34",
    ),
    claim(
        "P059-CLM-016", "v1.0.15", "PAST_AGENT", "INTERNAL_VALIDATION",
        "Six golden gates and downstream tests were reported to pass before the pointwise golden was recaptured.",
        [src(V15_HO, 17, "골든 6종 게이트"), src(V15_HO, 23, "6종 게이트")],
        "PATCH_CONFIRMED_INTERNAL_ONLY",
        "This is, at most, internal regression/convergence evidence; it does not establish agreement with experimental data or literature.",
        "Re-execute and inspect gate logic in Steps 34.2–34.4.",
        evidence_boundary="REPORTED_INTERNAL_VALIDATION_NOT_EXTERNAL_VALIDITY",
    ),
    claim(
        "P059-CLM-017", "v1.0.15", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "The shipped defaults were already effectively equilibrium because their lag length was around 10^-8 V.",
        [src(V15_HO, 25, "L_V~1e-8")],
        "PARTIAL",
        "The source openly narrows the dynamic claim: the capability exists, but defaults do not realize visible rate-dependent broadening.",
        "Calibrate kinetics against rate-series data and impose the zero-current limit.",
        contract_ids=["P059-CON-016", "P059-CON-020", "P059-CON-021"],
    ),
    claim(
        "P059-CLM-018", "v1.0.15", "PAST_AGENT", "CARRY_FORWARD",
        "Multi-temperature curvature, two-phase width temperature dependence, LCO physical values, and literature checks remained outside v1.0.15.",
        [src(V15_HO, 27, "미완료/이월"), src(V15_HO, 28, "다온도")],
        "CARRY_FORWARD_OPEN",
        "Explicit non-completion statement.",
        "Preserve as evidence debt; do not treat pointwise completion as project completion.",
        contract_ids=["P059-CON-015", "P059-CON-024", "P059-CON-033", "P059-CON-038"],
    ),
    claim(
        "P059-CLM-019", "v1.0.15", "USER", "USER_REQUIREMENT",
        "Width-temperature inference must follow constant n, per-temperature diagnosis, constant w, then minimal n(T), with matching heat propagation.",
        [src(V15_CLOSE, 88, "n으로 fit"), src(V15_CLOSE, 90, "4단 사다리"), src(V15_CLOSE, 92, "가역열 config")],
        "PRESERVE_REQUIREMENT",
        "Binding staged-identification requirement; it does not validate the selected physical interpretation.",
        "Retain the ladder, but split homogeneous thermodynamic width from phenomenological two-phase broadening.",
        contract_ids=["P059-CON-011", "P059-CON-015", "P059-CON-022", "P059-CON-023", "P059-CON-024"],
    ),
    claim(
        "P059-CLM-020", "v1.0.15", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "Applying the thermal configurational formula to a two-phase phenomenological width was explicitly admitted to be a model choice, not a derivation.",
        [src(V15_CLOSE, 93, "물리 유도 아닌 모델 선택")],
        "CARRY_FORWARD_OPEN",
        "This is a preserved self-identified semantic boundary, not closure.",
        "Use distinct symbols and do not automatically propagate ideal configurational entropy through empirical two-phase width.",
        contract_ids=["P059-CON-010", "P059-CON-013", "P059-CON-015"],
    ),
    claim(
        "P059-CLM-021", "v1.0.16", "PAST_AGENT", "THEORY_CHANGE",
        "v1.0.16 added a linear n(T) option and the derivative d w/dT = (R/F)(n+T n').",
        [src(V16_HO, 15, "_dwdT"), src(V16_HO, 17, "eq:dwdT-nT")],
        "PATCH_CONFIRMED",
        "The exact Ch1/Ch2 patches confirm the n(T) source addition and equation label.",
        "Code default/fallback consistency and identifiability remain open.",
        patch_ids=["ch1_v1015_to_v1016", "ch2_v1015_to_v1016"],
        contract_ids=["P059-CON-022", "P059-CON-023", "P059-CON-024"],
    ),
    claim(
        "P059-CLM-022", "v1.0.16", "PAST_AGENT", "INTERNAL_VALIDATION",
        "v1.0.16 reported exact round-trip and bit-exact regression for the additive n(T) path.",
        [src(V16_HO, 15, "round-trip 정확"), src(V16_HO, 21, "bit-exact")],
        "PATCH_CONFIRMED_INTERNAL_ONLY",
        "The claim is internal implementation consistency only; it does not establish material identifiability or data agreement.",
        "Re-run code paths, including the no-n/no-w fallback that the historical suite did not expose.",
        evidence_boundary="REPORTED_INTERNAL_VALIDATION_NOT_EXTERNAL_VALIDITY",
    ),
    claim(
        "P059-CLM-023", "v1.0.16", "PAST_AGENT", "CARRY_FORWARD",
        "The four-step width ladder was not executed; real multi-temperature data were required to assign constant n, constant w, or n(T).",
        [src(V16_HO, 23, "4단 사다리는 실행 대기"), src(V16_HO, 28, "다온도 실측")],
        "CARRY_FORWARD_OPEN",
        "Explicit experimental non-completion.",
        "Execute the ladder on public multi-temperature data and quantify uncertainty/identifiability.",
        contract_ids=["P059-CON-022", "P059-CON-024"],
    ),
    claim(
        "P059-CLM-024", "v1.0.16", "PAST_AGENT", "CARRY_FORWARD",
        "The guide itself still requested implementation of temperature-dependent LCO electronic terms and fixed-point convergence checks.",
        [src(V16_GUIDE, 55, "Sommerfeld T-스케일 복원")],
        "CARRY_FORWARD_OPEN",
        "The fitting guide records an unimplemented or unclosed path, contradicting any broad code-complete reading.",
        "Derive the implicit composition/electronic coupling, chain rule, and convergence contract before implementation.",
        contract_ids=["P059-CON-036", "P059-CON-038"],
    ),
    claim(
        "P059-CLM-025", "v1.0.16", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "The guide acknowledges that visible kinetic lag requires activation enthalpy near 80 kJ/mol while shipped values produce negligible lag.",
        [src(V16_GUIDE, 54, "80 kJ/mol"), src(V16_GUIDE, 54, "L_V~10⁻⁸")],
        "PARTIAL",
        "This is an honest scale diagnosis, not validation of the barrier model or its defaults.",
        "Replace the frozen cut-affinity closure with a local electrochemical driving-force model and fit rate/temperature data.",
        contract_ids=["P059-CON-016", "P059-CON-020", "P059-CON-021"],
    ),
    claim(
        "P059-CLM-026", "v1.0.17", "PAST_AGENT", "EXTERNAL_REVIEW",
        "The title claimed complete incorporation of the external review.",
        [src(V17_HO, 1, "완전 반영")],
        "OVERCLAIMED",
        "The same handover documents that the first extraction omitted all Ch2 and appendix items; review incorporation is process evidence, never scientific authority.",
        "Retain only source-linked corrections after independent adjudication.",
        evidence_boundary="REVIEW_PROCESS_CLAIM_NOT_SCIENTIFIC_AUTHORITY",
    ),
    claim(
        "P059-CLM-027", "v1.0.17", "PAST_AGENT", "PROCESS_HISTORY",
        "The first external-review extraction omitted Ch2 and the appendix and was later repaired from source images.",
        [src(V17_HO, 11, "통째 누락")],
        "SOURCE_STATEMENT_ONLY",
        "Documented recovery from a prior extraction failure; it justifies distrust of reviewer summaries without source linkage.",
        "Keep reviewer verdicts subordinate to exact source and primary literature evidence.",
    ),
    claim(
        "P059-CLM-028", "v1.0.17", "PAST_AGENT", "THEORY_CHANGE",
        "v1.0.17 removed exposed implementation language from the theory body and strengthened references and appendix dimensions.",
        [src(V17_HO, 17, "본문 코드/구현"), src(V17_HO, 18, "DOI 2 정정"), src(V17_HO, 19, "차원정합")],
        "PATCH_CONFIRMED",
        "The exact Ch1/Ch2/appendix diffs confirm register, bibliography, and dimensional-source changes.",
        "Preserve this manuscript-boundary cleanup while independently checking the corrected references.",
        patch_ids=["ch1_v1016_to_v1017", "ch2_v1016_to_v1017", "appendix_v1016_to_v1017"],
        evidence_boundary="SOURCE_PATCH_CONFIRMED_REFERENCES_NOT_YET_PRIMARY_VERIFIED",
    ),
    claim(
        "P059-CLM-029", "v1.0.17", "PAST_AGENT", "IMPLEMENTATION_CHANGE",
        "v1.0.17 explicitly made no physical, equation, numerical, algorithmic, or production-code change beyond a matched bump.",
        [src(V17_HO, 25, "코드 무변경")],
        "COPY_FORWARD_NO_NEW_VALIDATION",
        "A copy-forward version cannot add new physical validation merely by passing the old regression.",
        "Treat v1.0.17 as a document-boundary refinement, not a new model baseline.",
    ),
    claim(
        "P059-CLM-030", "v1.0.18.1", "PAST_AGENT", "THEORY_CHANGE",
        "v1.0.18.1 was explicitly doc-only, with unchanged physics, equations, numbers, identifiers, and bit-identical code.",
        [src(V181_HO, 11, "doc-only"), src(V181_HO, 17, "물리·코드 무변경")],
        "COPY_FORWARD_NO_NEW_VALIDATION",
        "Exact source diffs confirm formatting/register work; this release provides no new scientific validation.",
        "Use it only as a presentation-lineage checkpoint.",
        patch_ids=["ch1_v1017_to_v1018_1", "ch2_v1017_to_v1018_1", "appendix_v1017_to_v1018_1"],
    ),
    claim(
        "P059-CLM-031", "v1.0.18.2", "PAST_AGENT", "THEORY_CHANGE",
        "v1.0.18.2 added an Einstein single-oscillator entropy and paired free-energy/entropy corrections.",
        [src(V182_HO, 14, "S_vib"), src(V182_HO, 23, "같은 자유에너지")],
        "PATCH_CONFIRMED",
        "The exact Ch2 patch adds eq:Svib-einstein, eq:dSvib, and eq:dUvib; this confirms internal theory-source addition.",
        "Define an insertion-reaction phonon spectrum with product/reactant modes and weights.",
        patch_ids=["ch1_v1018_1_to_v1018_2", "ch2_v1018_1_to_v1018_2"],
        contract_ids=["P059-CON-030", "P059-CON-031", "P059-CON-032"],
    ),
    claim(
        "P059-CLM-032", "v1.0.18.2", "PAST_AGENT", "INTERNAL_VALIDATION",
        "Einstein round-trip, full-path derivative, high-temperature limit, regression, demo, and sample checks were reported to pass.",
        [src(V182_HO, 14, "0.000000 µV/K")],
        "PATCH_CONFIRMED_INTERNAL_ONLY",
        "These checks establish formula/implementation self-consistency only; they do not identify a material reaction spectrum or validate experimental data.",
        "Re-execute Step 34 tests and then validate against primary thermodynamic/phonon data.",
        contract_ids=["P059-CON-031", "P059-CON-032"],
        evidence_boundary="REPORTED_INTERNAL_VALIDATION_NOT_EXTERNAL_VALIDITY",
    ),
    claim(
        "P059-CLM-033", "v1.0.18.2", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "No theta_E was assigned to the default material dataset; the Einstein term was capability-only pending multi-temperature measurements.",
        [src(V182_HO, 20, "capability + 검증만")],
        "CARRY_FORWARD_OPEN",
        "Explicitly limits the feature to an inactive capability under shipped defaults.",
        "Do not call it material physics completion until reaction-specific parameters are supported by data.",
        contract_ids=["P059-CON-030", "P059-CON-032"],
    ),
    claim(
        "P059-CLM-034", "v1.0.18.2", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "Three or more temperatures spanning the quasi-quantum window were stated as sufficient to separate vibrational and electronic terms.",
        [src(V182_HO, 22, "3온도점"), src(V182_GUIDE, 57, "3개 이상")],
        "PARTIAL",
        "Three points are a necessary design floor in the stated model, not a proof of joint identifiability with n(T), reaction entropy, and electronic terms.",
        "Require sensitivity/Fisher or profile-likelihood analysis over realistic noise and temperature windows.",
        contract_ids=["P059-CON-024", "P059-CON-032", "P059-CON-038"],
    ),
    claim(
        "P059-CLM-035", "v1.0.18.2", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "Calling v1.0.18.2 the completed physical version overstates the evidence.",
        [src(V182_HO, 4, "완결 = 물리판")],
        "OVERCLAIMED",
        "The same handover says default theta_E is absent, proposals 2–5 are open, LCO values await data, and final review may be incomplete.",
        "Classify v1.0.18.2 as an internally consistent capability branch, not scientific canon.",
        contract_ids=["P059-CON-024", "P059-CON-032", "P059-CON-033", "P059-CON-038"],
    ),
    claim(
        "P059-CLM-036", "v1.0.18.2", "EXTERNAL_REVIEWER", "EXTERNAL_REVIEW",
        "The roadmap inherits an external reviewer premise that the existing physics had zero errors.",
        [src(V182_ROAD, 3, "물리 오류 0건 전제")],
        "REVIEW_INPUT_NOT_AUTHORITY",
        "An external reviewer verdict is a review input; it is not primary literature, derivation, code execution, or experimental evidence.",
        "Adjudicate every inherited proposal and premise independently.",
    ),
    claim(
        "P059-CLM-037", "v1.0.18.2", "PAST_AGENT", "CARRY_FORWARD",
        "Composition-dependent Omega, Cahn-Hilliard-derived hysteresis, Butler-Volmer/Nernst-Planck polarization, and PSD broadening remained roadmap items.",
        [src(V182_HO, 27, "제안 2~5"), src(V182_ROAD, 11, "Ω(ξ)"), src(V182_ROAD, 14, "PSD")],
        "CARRY_FORWARD_OPEN",
        "Explicit unimplemented research scope.",
        "Re-rank after independent literature review; do not inherit the roadmap order as authority.",
        contract_ids=["P059-CON-008", "P059-CON-009", "P059-CON-010", "P059-CON-035"],
    ),
    claim(
        "P059-CLM-038", "v1.0.18.2", "PAST_AGENT", "SCIENTIFIC_SCOPE",
        "The roadmap proposes deriving voltage-lag length directly from a linear Cahn-Hilliard growth rate.",
        [src(V182_ROAD, 28, "꼬리 길이 L_V 물리 근거")],
        "OVERCLAIMED",
        "A spatial conserved-order-parameter growth rate does not by itself yield the measured voltage-domain causal kernel; the electrochemical driving protocol and observation map are missing.",
        "Derive the time/state-space model first, then map it to voltage under an explicit protocol.",
        contract_ids=["P059-CON-009", "P059-CON-017", "P059-CON-018"],
    ),
    claim(
        "P059-CLM-039", "v1.0.18.2", "PAST_AGENT", "CARRY_FORWARD",
        "Multi-temperature n diagnosis, two-phase width behavior, LCO physical values, and remaining bibliography checks were still awaiting measurements or verification.",
        [src(V182_ROAD, 45, "실측 대기"), src(V182_ROAD, 46, "per-T n"), src(V182_ROAD, 47, "LCO 실값"), src(V182_ROAD, 48, "서지 재확인")],
        "CARRY_FORWARD_OPEN",
        "Explicit unresolved evidence debt at the end of the audited range.",
        "Carry these items into literature, data, and material-validation phases without downgrading them to optional polish.",
        contract_ids=["P059-CON-015", "P059-CON-024", "P059-CON-033", "P059-CON-037", "P059-CON-038"],
    ),
    claim(
        "P059-CLM-040", "v1.0.18.2", "PAST_AGENT", "PROCESS_HISTORY",
        "The final Fable review was best-effort and could remain incomplete.",
        [src(V182_HO, 29, "미완 가능")],
        "SOURCE_STATEMENT_ONLY",
        "The historical review process explicitly did not close its own final-review gate.",
        "Do not use the presence of an external-review label as a completion certificate.",
    ),
]


def exact_anchor(spec: dict) -> dict:
    path = ROOT / spec["path"]
    lines = path.read_text(encoding="utf-8").splitlines()
    line = lines[spec["line"] - 1]
    if spec["needle"] not in line:
        raise ValueError(
            f"anchor mismatch {spec['path']}:{spec['line']}: {spec['needle']!r}"
        )
    return {
        "path": spec["path"],
        "line": spec["line"],
        "needle": spec["needle"],
        "source_line": line,
    }


def main() -> None:
    lineage = json.loads(DIFF_INDEX.read_text(encoding="utf-8"))
    patches = {entry["pair_id"]: entry for entry in lineage["comparisons"]}
    records = []
    for raw in CLAIMS:
        record = {key: value for key, value in raw.items() if key != "source_specs"}
        record["source_evidence"] = [exact_anchor(spec) for spec in raw["source_specs"]]
        record["patch_evidence"] = [
            {
                "pair_id": pair_id,
                "exact_unified_diff": patches[pair_id]["exact_unified_diff"],
                "exact_unified_diff_sha256": patches[pair_id][
                    "exact_unified_diff_sha256"
                ],
                "content_identical": patches[pair_id]["content_identical"],
            }
            for pair_id in raw["patch_ids"]
        ]
        records.append(record)

    class_counts = Counter(record["claim_class"] for record in records)
    disposition_counts = Counter(record["disposition"] for record in records)
    actor_counts = Counter(record["actor"] for record in records)
    matrix = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": lineage["baseline_commit"],
        "scope": "Phase 059 Step 33.5 guide/handover/closing/roadmap completion, authority, and carry-forward claims",
        "status": "PASS_P059_COMPLETION_AUTHORITY_ADJUDICATION",
        "authority_boundary": (
            "This audit links historical claims to exact source patches and prior "
            "contracts. It does not certify code execution, primary literature, "
            "experimental validity, or final theory canon."
        ),
        "rules": [
            "A source patch proves that text changed, not that the new physics is true.",
            "A regression or round-trip proves only the property explicitly tested.",
            "A reviewer or agent verdict is never primary scientific evidence.",
            "Copy-forward and matched version bumps do not create new validation.",
            "Open real-data and literature items remain blockers even when a version is called complete.",
        ],
        "allowed_claim_classes": sorted(ALLOWED_CLASSES),
        "allowed_dispositions": sorted(ALLOWED_DISPOSITIONS),
        "record_count": len(records),
        "claim_class_counts": dict(sorted(class_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "actor_counts": dict(sorted(actor_counts.items())),
        "records": records,
    }
    OUTPUT.write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = []
    for record in records:
        anchors = "; ".join(
            f"{Path(item['path']).name}:{item['line']}"
            for item in record["source_evidence"]
        )
        patches_text = ", ".join(record["patch_ids"]) or "—"
        rows.append(
            f"| {record['id']} | {record['version']} | {record['actor']} | "
            f"{record['claim_class']} | {record['disposition']} | {anchors} | "
            f"{patches_text} |"
        )

    summary = f"""# Phase 059 완료·권위·이월 주장 재판정

이 문건은 v1.0.14–v1.0.18.2의 guide, handover, closing, roadmap에
쓰인 “완료·검증·불변·이월” 표현을 실제 소스 패치와 연결한 감사
결과다. 이론 정본, 코드 실행 인증, 1차 문헌 검증 또는 실험 검증이
아니다.

## 핵심 판정

1. 사용자 헌법은 명확하다. 최종 문건은 교재 register, 리뷰 논문
   깊이, 수식 주도 전개를 동시에 충족하고, 이론 본문은 코드와
   작업이력을 서술하지 않는다.
2. v1.0.15의 격자 퇴출, v1.0.16의 `n(T)`, v1.0.17의 theory-body
   경계 정련, v1.0.18.2의 Einstein 식 추가는 exact theory patch로
   확인된다. “패치 확인”은 과학적 타당성이나 코드 정합을 뜻하지
   않는다.
3. golden, bit-exact, round-trip, demo PASS는 내부 검증이다.
   실데이터 적합성, parameter identifiability, 문헌 타당성은
   별도 증거가 필요하다.
4. v1.0.17과 v1.0.18.1은 명시적으로 물리·코드 copy-forward다.
   문체·서지·조판 개선은 보존하지만 새로운 물리 검증으로 세지
   않는다.
5. v1.0.18.2의 Einstein 항은 기본 데이터셋에서 비활성이고,
   reaction-specific phonon spectrum과 joint identifiability가
   없다. 따라서 “물리판 완결”은 과장이다.
6. 외부 리뷰의 “물리 오류 0건”과 “완전 반영”은 검토 입력일 뿐
   과학적 권위가 아니다. 같은 이력 안에 추출 누락과 최종검수
   미완 가능성이 기록돼 있다.
7. 다온도 폭, LCO 물성·고전압 도핑, 전자항 결합, 문헌 재확인,
   제안 2–5는 v1.0.18.2 끝에서도 열려 있다.

## 주장별 근거표

| ID | Version | Actor | Class | Disposition | Source anchors | Exact theory patches |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## 집계

- records: {len(records)}
- classes: {json.dumps(dict(sorted(class_counts.items())), ensure_ascii=False)}
- dispositions: {json.dumps(dict(sorted(disposition_counts.items())), ensure_ascii=False)}
- actors: {json.dumps(dict(sorted(actor_counts.items())), ensure_ascii=False)}

Gate: `PASS_P059_COMPLETION_AUTHORITY_ADJUDICATION`.
"""
    SUMMARY.write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
