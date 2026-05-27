# Anode Fit — Chapter 1 Rebuild Master Roadmap

## Summary

- Status: `READY_FOR_USER_REVIEW`
- Date: `2026-05-27`
- Active project: `D:\Projects\Project_Anode_Fit`
- Supersedes: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan.md` (v0.1)
- Driver document: `Claude/results/PROJECT_AUDIT_REPORT_v0.2.md`
- This roadmap rebuilds Chapter 1 of the graphite anode ICA/DVA dynamics document **from scratch**, treating ver5 (`Claude/docs/graphite_ica_dynamic_ver5.tex`) and ver1_rechecked2 (`Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex`) as reference only, never modified.
- The next direction is not "improve rechecked2 by absorbing ver5 sections". The next direction is **redesign the modelling foundation to avoid the step function assumption** that the user identified as the root defect of ver1~5 (`적분을 모 아니면 도 즉 스텝펑션의 형태로 가정`).
- The user's PhD-level Fredholm integral equation (2nd kind) ratio-substitution method (JCP 2017 + Refs. 6, 7) is the load-bearing technique. Its long-range continuous reactivity kernel directly enables both (a) self-consistent loop closed-form solution and (b) step-function-assumption avoidance.
- No body writing, no LaTeX build, no user-facing PDF should start before the spine redesign and continuous-chemical-potential model are validated against the user's intent.

## Current Ground Truth

- Project root: `D:\Projects\Project_Anode_Fit`
- Active Claude workspace: `D:\Projects\Project_Anode_Fit\Claude`
- ver5 master (reference only): `Claude/docs/graphite_ica_dynamic_ver5.tex` — 1974 lines, 5 chapters (Ch1 = lines 46-526, 19§/21subsec)
- ver1_rechecked2 (reference only): `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` — 495 lines, 14§/14subsec
- User's own paper (local only): `Claude/_local_only/JCP_147(14)_144111_(2017)...pdf` — 10 pages, DOI `10.1063/1.5000882`, first author Kyusup Lee (= user)
- pdftotext extract: `Claude/_local_only/jcp_extract.txt` — 724 lines, gitignored
- Phase A result: `Claude/results/PHASE_A_ver5_master_structure_RESULT.md` (Gate `PASS_VER5_MASTER_STRUCTURE`)
- Phase B result: `Claude/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` + Addendum 1 (Gate `PASS_VER1_RECHECKED_DIAGNOSIS`)
- Phase C result: `Claude/results/PHASE_C_chapter1_mapping_and_feedback_note_RESULT.md` (Gate `PASS_CHAPTER1_MAPPING_TABLE`, GATE_C4 deferred)
- Phase D result: `Claude/results/PHASE_D_jcp_ref6_7_methodology_RESULT.md` (Gate `PASS_JCP_REF6_7_METHODOLOGY`)
- Phase A~D ledger: `Claude/results/PHASE_A_D_EXECUTION_LEDGER.md` — all 4 phases PASS, cumulative steps 1-18 closed
- Audit report v0.2: `Claude/results/PROJECT_AUDIT_REPORT_v0.2.md` — supersedes v0.1, identifies B4/B5/B6 + L4 + 3.6/3.7/3.8 gaps
- Ref 6 (user paper grouped citation): S. Lee, C. Y. Son, J. Sung, S. Chong, J. Chem. Phys. **134**, 121102 (2011) — DOI not found by 2026-05-27 external search (multiple attempts, AIP HTTP 403)
- Ref 7 (user paper grouped citation): C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, J. Chem. Phys. **138**, 164123 (2013) — title "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity", URL `pubs.aip.org/aip/jcp/article-abstract/138/16/164123/71188`, DOI not directly extractable
- User 5-27 verbatim diagnosis preserved in audit v0.2 §1.3
- Codex parallel workspace: `D:\Projects\Project_Anode_Fit\Codex` — never read/modified (P2)

## Core Principle (Charter)

- Build the new Chapter 1 with **continuous chemical potential** semantics first.
- Treat ver5 and ver1_rechecked2 as evidence sources and as anti-pattern references (where step function assumptions live).
- Treat the user's Fredholm 2nd kind ratio-substitution method as the canonical method for handling self-consistent integral equations that arise from the new model.
- Prefer a long phase path that prevents the rework that caused ver1_rechecked2's 10+ failed reviews over a fast path that produces premature LaTeX body.
- Do not introduce any `max(., 0)`, `min(., k_max)`, `step(.)`, `Heaviside(.)`, `sign(.)`, or analogous piecewise constructions in **definitional** equations. They may appear only as **numerical regularization auxiliaries** with explicit `ε → 0` smooth-limit consistency.
- Do not collapse continuous staging chemical potential into N_p discrete transitions in **definitional** equations. N_p decomposition may appear only as a **derived basis expansion** after the continuous form is established.
- Do not use logistic / erf / sigmoid as the definitional shape of equilibrium quantities. They may appear as approximations to a continuous distribution `ρ(μ; q, T)` with explicit error bound.
- Unknown facts (e.g., Ref. 6 DOI) must be resolved via local DB / external search / explicit `근거 미발견` mark — never silent assumption, never user-delegated as a default.

## Phase Range

- Phase E0: Foundation reset and rebuild charter — Steps `19-80` (62 steps)
- Phase E1: Spine redesign and core variable selection — Steps `81-140` (60 steps)
- Phase E2: §1, §2 writing (purpose, notation, units) — Steps `141-200` (60 steps)
- Phase E3: §3, §4 writing (effective transition concept, V_n / V_{n,app} / V_{n,drive} 3-way separation) — Steps `201-260` (60 steps)
- Phase E4: §5 writing (charge balance — central equation, continuous reformulation) — Steps `261-340` (80 steps)
- Phase E5: §6 writing (continuous chemical potential distribution ρ(μ)) — Steps `341-420` (80 steps)
- Phase E6: §7 writing (continuous reactivity kernel S_R(μ) — replaces discrete k_j) — Steps `421-500` (80 steps)
- Phase E7: §8, §9 writing (progress and barrier distribution in continuous form) — Steps `501-580` (80 steps)
- Phase E8: §10 writing (ICA · DVA derivation from continuous ρ(μ)) — Steps `581-640` (60 steps)
- Phase E9: §11, §12 writing (C-rate, temperature, empirical comparison) — Steps `641-700` (60 steps)
- Phase E10: §13, §14, §15, §16 writing (fitting procedure, identifiability, model levels) — Steps `701-780` (80 steps)
- Phase E11: ★ §17 writing — Ref. 6, 7 ratio-substitution applied to graphite continuous reactivity self-consistent integral equation — Steps `781-900` (120 steps)
- Phase E12: §18, §19, §20 writing (transfer to Ch2, self-audit checklist, references) and global consistency pass — Steps `901-980` (80 steps)
- Phase F1: LaTeX build environment setup and first build attempt — Steps `981-1020` (40 steps)
- Phase F2: Build error correction loop (max 3 rounds) — Steps `1021-1060` (40 steps)
- Phase F3: PDF user review request (★ Decision Gate `GATE_F3`) — Steps `1061-1100` (40 steps)
- Phase F4: User feedback application and v0.2 file creation — Steps `1101-1180` (80 steps)
- Phase F5: Final commit, Phase A~F ledger closure, follow-up plan decision — Steps `1181-1220` (40 steps)

Total: 17 phases, cumulative steps 19 - 1220 (≈ 1200 steps).

Chapter 2~5 rebuild is out of scope. Each will get its own master roadmap after Chapter 1 closes.

## Non-goals

- Do not modify `Claude/docs/graphite_ica_dynamic_ver5.tex`.
- Do not modify `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex`.
- Do not modify any file in `Claude/_local_only/`.
- Do not read or modify `Codex/` artifacts (P2). Codex run dictates and operational docs already absorbed in earlier Audit phases.
- Do not write Chapter 2, 3, 4, 5 in this roadmap.
- Do not implement numerical solvers in this roadmap. Numerical implementation is a separate Phase G plan.
- Do not perform empirical fitting against experimental ICA data in this roadmap. Empirical validation is a separate Phase H plan.
- Do not adopt ver5 §6.5 `max(ΔG_eff, 0)` form in any definitional equation.
- Do not adopt ver1_rechecked2 §6.2 softplus form in any definitional equation. Softplus may appear only as an explicit smooth limit of `max(., 0)`, never as the canonical functional form.
- Do not adopt ver5 §5.1 logistic / §5.2 erf as the definitional shape of any continuous distribution.
- Do not decompose graphite staging into N_p discrete `ξ_j` as the primary state variable. N_p discretization may appear only as a derived basis after a continuous distribution is established.
- Do not adopt ver5's "5 chapter `ver.N` adapter chain" pattern wholesale. New Chapter 1's transfer to Ch2 must be rewritten on top of the continuous form, not on top of the discrete `ξ_j` chain.
- Do not enable PDF output for user review before §17 (Ref. 6, 7 application) is structurally complete.
- Do not delegate external resource lookup to user as a default. Lookup must be attempted by Claude via WebSearch / WebFetch / local DB before any user query.

## Implementation Changes

Planned new files (Claude/docs/):

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` — new Chapter 1 LaTeX body
- `Claude/docs/graphite_ica_chapter1_v0.1.json` — companion metadata (variable inventory, equation labels, audit dim coverage)

Planned new files (Claude/results/):

- `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md`
- `Claude/results/PHASE_E1_spine_redesign_RESULT.md`
- `Claude/results/PHASE_E2_intro_notation_RESULT.md`
- `Claude/results/PHASE_E3_effective_transition_potential_separation_RESULT.md`
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.md`
- `Claude/results/PHASE_E5_continuous_distribution_RESULT.md`
- `Claude/results/PHASE_E6_continuous_reactivity_kernel_RESULT.md`
- `Claude/results/PHASE_E7_progress_barrier_distribution_RESULT.md`
- `Claude/results/PHASE_E8_ica_dva_derivation_RESULT.md`
- `Claude/results/PHASE_E9_crate_temperature_emg_RESULT.md`
- `Claude/results/PHASE_E10_fitting_identifiability_model_levels_RESULT.md`
- `Claude/results/PHASE_E11_ref6_7_ratio_substitution_RESULT.md`
- `Claude/results/PHASE_E12_transfer_audit_references_RESULT.md`
- `Claude/results/PHASE_F1_build_first_attempt_RESULT.md`
- `Claude/results/PHASE_F2_build_correction_RESULT.md`
- `Claude/results/PHASE_F3_user_review_RESULT.md` (Decision Gate)
- `Claude/results/PHASE_F4_feedback_application_RESULT.md`
- `Claude/results/PHASE_F5_closure_RESULT.md`
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` (cumulative steps 19-1220, 17 phase rows)

Planned new phase-level plans (Claude/plans/, one per phase as RO_SkillDict pattern):

- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md`
- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e1-spine-plan.md`
- ... (one per phase, created right before each phase begins per `feedback_phase_execution_loop` Step 1 `plan saved`)

Planned new memory candidates (Claude/_claude/memory/ + global):

- `feedback_plan_step_granularity_standard.md` — each step = single verb-noun action, no compound commands; RO_SkillDict master roadmap as reference
- `feedback_external_lookup_first_self.md` — external info (DOI, citation, public API) must be self-searched before user delegation
- Extension of `feedback_phase_audit_workflow.md` — add Dim #11 "model assumption fidelity (system-fidelity)"

All three contingent on user approval of audit v0.2.

## Phase E0 — Foundation Reset And Rebuild Charter

Steps:

19. Save Phase E0 plan as `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md`.
20. Save companion JSON for Phase E0 plan.
21. Load `Claude/results/PROJECT_AUDIT_REPORT_v0.2.md` §1.5 (step function assumption diagnosis) into Phase E0 context.
22. Load `Claude/results/PROJECT_AUDIT_REPORT_v0.2.md` §5.11 (continuous chemical potential rebuild direction) into Phase E0 context.
23. Load `Claude/results/PHASE_D_jcp_ref6_7_methodology_RESULT.md` §"original methodology" into Phase E0 context.
24. Load `Claude/_local_only/jcp_extract.txt` §II.C "Solution to Eq. (6) for long-range reaction sink functions" (lines 193-275) into Phase E0 context.
25. Identify and record the exact ver5 line numbers that contain the step function assumption (e.g., line 240-245 §6.5 method A `max(ΔG_eff,0)`, line 247-249 method B `min(., k_max)`, line 188 §5.1 logistic, line 137-150 §3 discrete N_p decomposition).
26. Identify and record the exact ver1_rechecked2 line numbers with residual step function or discrete N_p assumptions (e.g., line 188-193 §5 logistic still present, line 110 §3 effective transition N_p still discrete).
27. Identify and record the JCP 2017 line numbers that demonstrate continuous reactivity (e.g., lines 60-90 §II.A `S_R(r)` continuous in r, lines 193-275 §II.C long-range sink).
28. Write a charter document listing: rebuild objective, anti-pattern list, allowed-pattern list, forbidden-pattern list, smooth-limit consistency rule.
29. Declare rebuild objective: "Construct a Chapter 1 that models graphite anode ICA/DVA via continuous chemical potential distribution and continuous reactivity kernel, with the user's Fredholm 2nd kind ratio-substitution method as the canonical solver for the resulting self-consistent integral equation."
30. Declare anti-pattern: `max(ΔG, 0)`, `min(., k_max)`, sigmoid as definitional, discrete N_p decomposition as primary state.
31. Declare allowed-pattern: continuous distribution `ρ(μ; q, T)`, continuous kernel `S_R(μ)`, integral over continuous `μ`-space, Fredholm 2nd kind self-consistent integral equations, ratio-substitution method.
32. Declare forbidden-pattern: any new step function or Heaviside in definitional equations; any discretization of `μ` without explicit basis derivation from a continuous form.
33. Declare smooth-limit consistency rule: every regularization term `ε > 0` (e.g., softplus, ε_Q in ∂Q_bg/∂V_n ≥ ε_Q) must have an explicit `ε → 0` limit that recovers a continuous-form expression, documented at the point of use.
34. Define audit Dimension #11 "model assumption fidelity": at every section boundary, list every assumption used and tag it with `system-fidelity-OK`, `system-fidelity-WARN`, or `system-fidelity-FAIL`.
35. Define audit Pass 1 procedure for Dim #11: enumerate all `max`, `min`, `clip`, `Heaviside`, `sign`, `step`, `logistic`, `sigmoid`, `erf`, `softplus`, `tanh`, `relu` uses in the candidate text; flag for review.
36. Define audit Pass 2 procedure for Dim #11: classify each flagged use as definitional (FAIL), regularization-with-smooth-limit (WARN), or empirical-approximation-with-error-bound (OK).
37. Define audit Pass 3 procedure for Dim #11: verify that flagged-FAIL uses have been removed or reclassified with explicit justification.
38. Confirm Claude does not have web access to AIP pay-walled content. WebFetch returns HTTP 403 for `pubs.aip.org` direct URLs.
39. Record alternative external resource paths: arXiv preprint, ResearchGate mirror, Google Scholar abstract, university repository.
40. Attempt WebSearch with arXiv keyword combinations for Ref. 6 (`S. Lee Son Sung Chong JCP 121102 Fredholm integral 2011`).
41. Attempt WebSearch with arXiv keyword combinations for Ref. 7 (`Son Kim Kim Kim Lee JCP 164123 long-range diffusion 2013`).
42. Record any new DOI / preprint URL discovered; if none, mark `Ref 6 DOI: 근거 미발견 (multiple external search attempts on 2026-05-27)`.
43. Record `Ref 7 DOI: 근거 미발견 (AIP HTTP 403, no arXiv mirror found by 2026-05-27)` if no DOI confirmed.
44. Plan a Decision Queue entry asking user for Ref. 6, 7 PDF directly (user-as-author option, not user-as-search-fallback).
45. Define new variable namespace for the rebuild: `μ` (continuous chemical potential coordinate), `ρ(μ; q, T)` (continuous distribution density at chemical potential μ), `S_R(μ; T)` (continuous reactivity kernel at μ), `K_n(μ, μ'; q, T)` (cross-kernel), `Q_bg(V_n, T)` (preserved from rechecked2 as residual chemical capacitance, semantics unchanged), `V_n` (internal potential, implicit solution of new charge balance with continuous ρ), `V_{n,app}` (apparent potential, preserved), `V_{n,drive}` (driving potential, preserved).
46. Define legacy variable migration: `ξ_j` → derived from `ρ(μ; q, T)` by integration over μ-peak window; `k_j` → derived from `S_R(μ)` by μ-peak averaging; `U_j` → derived as `μ-peak center`; `w_j` → derived as `μ-peak FWHM`.
47. Define the legacy ↔ new variable mapping table to be included verbatim in new Chapter 1 §3.
48. Define the rebuild's central equation (will be detailed in Phase E4): `Q_cell · q = Q_bg(V_n, T) + ∫ dμ · ρ(μ; q, T) · n(μ)` where `n(μ)` is the per-unit-chemical-potential Li occupation count (continuous analog of ξ_j sums).
49. Define the rebuild's progress kinetics equation (will be detailed in Phase E6-E7): `∂ρ(μ; q, t)/∂t = ∫ dμ' · K_n(μ, μ'; q, T) · S_R(μ'; T) · [ρ_eq(μ'; q, T) - ρ(μ'; q, t)]` where `K_n` is the continuous transport kernel and `S_R` is the continuous reactivity kernel.
50. Recognize that Equation 49 is precisely a Fredholm-2nd-kind self-consistent integral equation in `ρ` — and is the exact target of Ref. 6, 7 ratio-substitution.
51. Record that this central equation form does not contain any `max`, `min`, logistic, or N_p sum — Charter compliant.
52. Define dependency graph for the rebuild: `q` (input) → `ρ(μ; q, T)` (continuous state) → `V_n` (implicit from charge balance) → `V_{n,app}`, `V_{n,drive}` → `S_R(μ)`, `K_n` → `dρ/dt` → `dQ/dV`, `dV/dQ` via Eq. 48 differentiation.
53. Identify the new self-consistent loop in this dependency graph: `ρ(μ; q, t) ↔ V_n(q, t)` via charge balance Eq. 48 + reactivity Eq. 49.
54. Plan Ref. 6, 7 application: ratio-substitution `ρ(μ_1)/ρ(μ_0) ≈ ρ^{simple}(μ_1)/ρ^{simple}(μ_0)` where `ρ^{simple}` is the known closed-form solution for a simplified kernel (analog of δ-function sink in JCP 2017 §II.B).
55. Identify `ρ^{simple}` candidate: continuous distribution under fixed `V_n = V_{n,OCV}(q, T)` (legacy ver5 assumption treated as known closed-form for ratio reference, not as canonical model).
56. Define Phase E0 deliverable: charter document `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md` with 9 sections (Charter Objective, Anti-pattern list, Allowed-pattern list, Forbidden-pattern list, Smooth-limit rule, Audit Dim #11 procedure, Legacy↔New variable mapping, Central equations preview, Ref. 6, 7 application sketch).
57. Define Phase E0 companion JSON: machine-readable charter, anti-pattern enumeration, audit dim spec, variable mapping table.
58. Gate `GATE_E0_1`: charter document contains all 9 sections, no section empty.
59. Gate `GATE_E0_2`: anti-pattern list cites at least 5 specific ver5 + rechecked2 line numbers as evidence.
60. Gate `GATE_E0_3`: allowed-pattern list defines new variable namespace and central equation form.
61. Gate `GATE_E0_4`: smooth-limit consistency rule has at least 2 worked examples (e.g., `max(x,0)` vs `ε·ln(1+exp(x/ε))` as ε → 0; logistic vs continuous distribution moment-matching).
62. Gate `GATE_E0_5`: audit Dim #11 procedure has Pass 1/2/3 each defined.
63. Gate `GATE_E0_6`: legacy ↔ new variable mapping covers all variables in ver5 Ch1 §2 (21 entries) and rechecked2 §2 (11 entries).
64. Gate `GATE_E0_7`: central equations 48 and 49 are written in valid LaTeX-renderable form and pass smooth-limit check.
65. Gate `GATE_E0_8`: Ref. 6, 7 application sketch identifies `ρ^{simple}` candidate explicitly.
66. Stop condition: if user has not approved audit v0.2 by the start of Phase E0 execution, do not enter Phase E0.
67. Stop condition: if WebSearch for Ref. 6, 7 DOIs returns no new lead, mark `근거 미발견` and proceed (do not loop).
68. Confirm no file modification in `Claude/docs/` during Phase E0 (charter is in Claude/results/ only).
69. Confirm no file in `Claude/_local_only/` is read except `jcp_extract.txt`.
70. Confirm `Codex/` is not read.
71. Write Phase E0 Result markdown.
72. Write Phase E0 Result companion JSON.
73. Validate Phase E0 Result JSON parses.
74. Update `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` Phase E0 row with PASS status.
75. Apply audit Pass 1+2+3 on Phase E0 deliverables (Dim #2 verbatim, Dim #3 read coverage, Dim #6 convention, Dim #7 silent miss, Dim #10 format, Dim α boundary, Dim β handover, Dim γ tree, Dim δ 4-tier, Dim #11 system-fidelity).
76. Record any Dim #11 finding in Phase E0 even on the charter itself (e.g., charter must not implicitly assume step function avoidance in only one section).
77. Commit Phase E0 Result + ledger + plan file as a pair commit per `feedback_phase_audit_workflow`.
78. Push commit.
79. Proceed to Phase E1 automatically per `feedback_plan_continuation_until_done` (do not request user re-GO unless Phase E0 audit produces user-decision-required item).
80. End Phase E0 at documented boundary.

Outputs:

- `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md`
- `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.json`
- ledger row Phase E0 PASS
- charter loaded into all subsequent phases

## Phase E1 — Spine Redesign And Core Variable Selection

Steps:

81. Save Phase E1 plan as `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e1-spine-plan.md`.
82. Save companion JSON for Phase E1 plan.
83. Load Phase E0 charter into Phase E1 context.
84. List ver5 Ch1 spine equation (line 66-79, Eq. main_spine): `ΔG_eff,j → k_j → dξ_j/dt → ξ_j(q) → dξ_j/dq → dQ/dV, dV/dQ`.
85. List ver1_rechecked2 spine (line 51-61): `Q_ext = Q_cell·q → 전하 보존식 → V_n → V_{n,app} → dQ/dV`.
86. Draft new spine candidate A: charter Eq. 48 + Eq. 49 with `ρ(μ; q, T)` as central state.
87. Draft new spine candidate B: same as A but with the explicit ICA/DVA derivation step `dQ/dV = (∂Q_ext/∂q) / (∂V_{n,app}/∂q)` appended.
88. Evaluate candidate A vs B against Charter anti-pattern list (no step, no discrete N_p in spine).
89. Select candidate B as the new spine.
90. Write the new spine explicitly:
   - `Q_ext = Q_cell · q` (external charge accumulation, preserved from rechecked2)
   - `Q_cell · q = Q_bg(V_n, T) + ∫ dμ · ρ(μ; q, T) · n(μ)` (charge balance with continuous ρ — Eq. 48)
   - `V_n` is the implicit solution of charge balance for given `q, T, ρ(μ; q, T)`
   - `ρ(μ; q, t)` evolves per Fredholm 2nd kind integral equation (Eq. 49) with continuous `S_R(μ)` and `K_n(μ, μ'; q, T)`
   - `V_{n,app} = V_n + s_I · |I| · R_n(q, T, |I|)` (preserved from rechecked2 §6.1)
   - `V_{n,drive}` defined per Phase E3 (preserved from rechecked2 as third potential)
   - `dQ/dV = Q_cell / (∂V_{n,app}/∂q)` (preserved structure from rechecked2 §9, with `V_n` and `V_{n,app}` from continuous form)
91. List every variable appearing in the new spine and tag canonical vs derived: `μ`, `ρ`, `S_R`, `K_n`, `Q_bg`, `V_n`, `V_{n,app}`, `V_{n,drive}`, `R_n`, `Q_cell`, `q`, `I`, `T`, `t` = canonical; `ξ_j`, `k_j`, `U_j`, `w_j`, `dξ_j/dq` = derived (from Phase E0 legacy mapping).
92. For each canonical variable, write a 1-line definition draft (will be expanded in Phase E2-E3).
93. For each derived variable, write the integral or limit defining it from canonical variables.
94. Verify all spine equations Charter-compliant by running audit Dim #11 Pass 1 manually.
95. Identify the new self-consistent loops in the spine: (i) Eq. 48 implicit in V_n (per-timestep root-find), (ii) Eq. 49 + Eq. 48 coupled (DAE in continuous μ-space), (iii) Eq. 49 in integral form = direct Fredholm 2nd kind in ρ (target of Ref. 6, 7).
96. Recognize that loop (iii) is structurally identical to JCP 2017 Eq. (32) with `W̄_u(r) ↔ ρ(μ; q, t)` mapping.
97. Plan that Ref. 6, 7 application in Phase E11 will provide closed-form for loop (iii), and loops (i), (ii) become standard DAE numerics built on top.
98. Draft the new transfer-to-Ch2 equation form (replaces ver5 §17 `ver.2 로 전달되는 기준식`): pass `ρ(μ; q, T)`, `V_n(q, t)`, `S_R(μ; T)`, `K_n(μ, μ'; q, T)`, `Q_bg(V_n, T)`, `R_n(q, T, |I|)` to Chapter 2 (thermal) instead of `dξ_j/dq`.
99. Note: Chapter 2~5 will need to be rewritten consistently with the continuous form. That work is out of scope here but flagged for follow-up roadmaps.
100. Define the legacy ↔ new variable cross-reference table for Phase E1 deliverable.
101. Draft Phase E1 Result document outline: §A spine choice rationale, §B canonical variable list, §C derived variable list, §D self-consistent loop classification, §E transfer-to-Ch2 sketch, §F legacy↔new cross-reference.
102. Draft a Phase E1 JSON companion: variable inventory, equation labels, loop classification.
103. Gate `GATE_E1_1`: new spine is explicitly written, Charter-compliant, no step function in definitional equations.
104. Gate `GATE_E1_2`: canonical variable list ≥ 12 entries, each with 1-line definition.
105. Gate `GATE_E1_3`: derived variable list maps every ver5 Ch1 §2 entry and every rechecked2 §2 entry to either a canonical variable or to a derivation from canonical variables.
106. Gate `GATE_E1_4`: self-consistent loop classification identifies ≥ 3 loops with clear position in the spine and labels which one Ref. 6, 7 will solve closed-form.
107. Gate `GATE_E1_5`: transfer-to-Ch2 sketch lists what Ch2 will receive in continuous form, and notes the legacy `dξ_j/dq`-based transfer is deprecated.
108. Gate `GATE_E1_6`: audit Pass 1+2+3 on the spine equations confirms Dim #11 OK (no FAIL flags, only WARN-with-justification allowed for any auxiliary regularization).
109. Stop condition: if a candidate spine introduces a step function that cannot be moved to regularization-only role, return to Step 86 and redraft.
110. Stop condition: if `μ`-space integration appears infeasible for any spine equation, document the obstacle, do not silently approximate.
111. Confirm no `Claude/docs/` write during Phase E1.
112. Confirm no `Codex/` read.
113. Confirm Phase E0 charter is the only foundational input; do not silently import ver5 or rechecked2 spine elements without explicit justification.
114. Write Phase E1 Result markdown.
115. Write Phase E1 Result companion JSON.
116. Validate Phase E1 Result JSON parses.
117. Update ledger Phase E1 row with PASS status.
118. Apply audit Pass 1+2+3 on Phase E1 deliverables (all 11 dims).
119. Document any Dim #11 finding on the spine.
120. Record decision queue items if a spine equation requires user clarification (e.g., μ choice = electrochemical chemical potential or thermodynamic phase chemical potential — likely user-cross-check).
121. List the legacy `ξ_j`-centered approach in Phase E1 result as an explicit `superseded` artifact reference, not a fallback option.
122. Cross-check Phase E1 spine against JCP 2017 §II.A (line 60-90) `S_R(r)` continuous-in-r model — confirm structural correspondence.
123. Cross-check Phase E1 spine against JCP 2017 §II.C (line 193-275) long-range reaction sink derivation — confirm Eq. 49 is correctly Fredholm-2nd-kind-shaped.
124. Cross-check Phase E1 spine variable count vs Phase A grep result (ver5 Ch1 §2 = 21 entries) — confirm derivation covers all 21.
125. Cross-check Phase E1 spine variable count vs Phase B variable dependency table (rechecked2 = 23 entries) — confirm derivation covers all 23.
126. Run the smooth-limit consistency rule on every regularization in the spine (e.g., `ε_Q` in `∂Q_bg/∂V_n ≥ ε_Q`) — record limit ε → 0 behavior.
127. Confirm the spine produces the same ICA/DVA at low rate as the legacy ver5 spine in the appropriate limit (small `|I|`, large rc analog, continuous ρ approximating discrete ξ_j peaks).
128. Record this limit-consistency verification as a Phase E1 Test Plan item to be executed numerically in Phase G (future).
129. Identify any Phase E1 result item that depends on user cross-check and record in Decision Queue (e.g., chemical potential μ semantics).
130. Plan that Decision Queue items do not block Phase E2 entry unless they are explicit Decision Gates (per `feedback_plan_continuation_until_done`).
131. Plan Phase E2 entry condition: Phase E1 PASS + spine accepted as draft baseline.
132. Define Phase E1 commit message: `phase(E1): chapter 1 spine redesign — continuous ρ(μ; q, T) replaces discrete ξ_j, Charter Dim #11 compliant`.
133. Stage Phase E1 deliverables for commit.
134. Commit Phase E1 with audit pass note.
135. Push commit.
136. Confirm push success on GitHub.
137. Mark Phase E1 row in ledger as PASS with Gate ID `PASS_SPINE_REDESIGN`.
138. Record Phase E1 next-step entry for Phase E2 (cumulative step 141).
139. Confirm no DQ-G1 (user audit v0.2 approval) blocker — if blocker, stop here and wait.
140. End Phase E1 at documented boundary.

Outputs:

- `Claude/results/PHASE_E1_spine_redesign_RESULT.md`
- `Claude/results/PHASE_E1_spine_redesign_RESULT.json`
- new spine equations 48, 49, and supporting equations registered in variable inventory
- ledger row Phase E1 PASS, Gate `PASS_SPINE_REDESIGN`

## Phase E2 — §1, §2 Writing (Purpose, Notation, Units)

Steps:

141. Save Phase E2 plan as a new file.
142. Save companion JSON for Phase E2 plan.
143. Load Phase E0 charter and Phase E1 spine into Phase E2 context.
144. Start `Claude/docs/graphite_ica_chapter1_v0.1.tex` with LaTeX preamble derived from ver5 preamble (lines 1-44) and rechecked2 preamble (lines 1-36).
145. Add `\usepackage{kotex}` for Korean if user environment supports xelatex or lualatex (will be checked in Phase F1).
146. Define LaTeX command macros for new variables: `\rhomu`, `\Sreact`, `\Kncross`, `\mucont`, plus preserved `\dd`, `\OCV`, `\app`, `\drive`, `\bg`, `\cell`, `\eff`.
147. Add a `% CHARTER COMPLIANCE` header comment at the top of the file, listing the anti-pattern, allowed-pattern, forbidden-pattern lists from Phase E0.
148. Write `\title{...}` and `\author{...}` and `\date{2026-05-27}`.
149. Write `\maketitle` and `\tableofcontents`.
150. Begin §1 (문서의 목적과 원칙).
151. Draft §1 paragraph 1 (목적): 1 sentence stating the document models graphite anode ICA/DVA via continuous chemical potential distribution and continuous reactivity kernel.
152. Draft §1 paragraph 2 (원칙): 4 numbered principles — (a) continuous μ over discrete N_p, (b) self-consistent loop closed-form via Ref. 6, 7 ratio-substitution, (c) charge balance is the central equation, (d) no step function in definitional equations.
153. Draft §1 paragraph 3 (적용 범위): low-rate to finite C-rate, OCV vs 0.2C reference, isothermal default with explicit temperature extension paths.
154. Draft §1 paragraph 4 (이전 ver5/rechecked2 와의 관계): explicit note that this Chapter 1 is a from-scratch rebuild, not a revision of ver5 Ch1 or rechecked2. Reference both as evidence sources.
155. Insert spine equation from Phase E1 (Eq. 48-49 + V_{n,app} + dQ/dV) as boxed display equation at end of §1.
156. Add `\begin{mdframed} ... \end{mdframed}` note: "본 문서는 진행률 변수 ξ_j 를 상태로 사용하지 않는다. ξ_j 는 ρ(μ; q, T) 의 N_p 개 peak window 적분으로부터 derive 되는 양이다."
157. Begin §2 (기호와 단위 컨벤션).
158. Begin §2.1 (기호 정의) as a `longtable`.
159. Add canonical variable rows: `μ`, `ρ(μ; q, T)`, `S_R(μ; T)`, `K_n(μ, μ'; q, T)`, `Q_bg(V_n, T)`, `V_n`, `V_{n,app}`, `V_{n,drive}`, `R_n(q, T, |I|)`, `Q_cell`, `q`, `I`, `T`, `t`, `s_I`, `s_{φ,j}` (for derived branch index).
160. Add derived variable rows with explicit "derived from continuous form" tag: `ξ_j`, `k_j`, `U_j`, `w_j`, `dξ_j/dq`.
161. Add parameter rows: `ν_j` (replaced or interpreted via `S_R(μ)` evaluated at μ-peak), `χ_j` (replaced via `S_R(μ)` derivative or moment), `ΔH_a`, `ΔS_a`, `ΔG_a` (kept as Marcus theory parameters of `S_R(μ)`).
162. Verify every variable used in the Phase E1 spine appears in §2.1.
163. Verify §2.1 row count matches Phase E1 variable inventory count.
164. Begin §2.2 (단위 컨벤션).
165. State `Q_cell` in coulombs explicitly (preserved from rechecked2 §2.2 lines 88-92).
166. State `Ah → C` conversion: `Q_cell[C] = 3600 · Q_cell[Ah]`.
167. State `μ` in volts (Li/Li⁺ reference) — preserved chemical potential semantics.
168. State `ρ(μ)` in (Coulombs per volt) so that `∫ dμ · ρ(μ; q, T) · n(μ)` is in coulombs.
169. State `S_R(μ)` in 1/seconds (reactivity rate at chemical potential μ).
170. State `K_n(μ, μ')` in 1/(volts · seconds) for dimensional consistency.
171. State `R_n` in ohms.
172. State `I` in amperes.
173. State `T` in kelvin.
174. State `t` in seconds.
175. State `q` dimensionless (= `Q_ext / Q_cell`).
176. Begin §2.3 (전류·전위 부호).
177. Define `s_I` per ver1_rechecked2 §6.1 convention.
178. Define discharge direction default: `s_I = +1` increases `V_{n,app}` above `V_n` during discharge.
179. Note that charge branch handling is deferred to Chapter 5 (history) but anticipated by `s_I` and `s_{φ,j}` sign declarations.
180. Begin closing §2 with a 1-line summary connecting notation back to §1 spine.
181. Audit Pass 1 on §1 and §2: enumerate every functional form used; check no `max`, `min`, logistic, erf, step in definitional rows.
182. Audit Pass 2: confirm every flag is regularization-only or empirical-approximation-with-justification.
183. Audit Pass 3: confirm no residual FAIL.
184. Cross-check §2 variable definitions against Phase E1 spine: every spine variable defined in §2 with consistent units.
185. Cross-check §2 unit consistency: every spine equation dimensional check passes.
186. Record any unit-conflict found.
187. Confirm `Claude/docs/graphite_ica_chapter1_v0.1.tex` line count is bounded (target ≤ 200 lines after Phase E2).
188. Write Phase E2 Result markdown summarizing §1 and §2 content and audit.
189. Write Phase E2 Result companion JSON with section line ranges and variable inventory.
190. Validate Phase E2 Result JSON parses.
191. Update ledger Phase E2 row with PASS status.
192. Apply audit Pass 1+2+3 with all 11 dims on Phase E2 deliverable.
193. Commit Phase E2 deliverables as a pair: source `chapter1_v0.1.tex` + `PHASE_E2_RESULT.md` + ledger.
194. Push commit.
195. Confirm push success.
196. Mark Phase E2 row in ledger PASS with Gate `PASS_INTRO_NOTATION`.
197. Record Phase E2 next-step entry for Phase E3 (cumulative step 201).
198. Stop condition: if §2 variable count is ≠ Phase E1 inventory count, return to Step 162 and reconcile.
199. Stop condition: if any §1 or §2 sentence implies discrete N_p as primary state, redraft.
200. End Phase E2 at documented boundary.

Outputs:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (partial, §1 + §2 only after Phase E2)
- `Claude/results/PHASE_E2_intro_notation_RESULT.md`
- `Claude/results/PHASE_E2_intro_notation_RESULT.json`
- ledger row Phase E2 PASS, Gate `PASS_INTRO_NOTATION`

## Phase E3 — §3, §4 Writing (Effective Transition Concept, Three-Way Potential Separation)

Steps:

201. Save Phase E3 plan.
202. Load Phase E0-E2 deliverables.
203. Begin §3 (흑연 staging 과 연속 chemical potential).
204. Draft §3 paragraph 1: explain that ver5 §3 decomposed graphite into N_p discrete effective transitions, but this Chapter 1 treats staging as a continuous distribution in μ-space.
205. Draft §3 paragraph 2: define `ρ(μ; q, T) dμ` as the Li content (or equivalent fractional occupation) contributed per chemical potential window `[μ, μ + dμ]` at state `(q, T)`.
206. Draft §3 paragraph 3: cite Bazant Cahn-Hilliard reaction model (ver5 ref [4] = J.P.C. Lett. 2016) as physically grounded continuous chemical potential framework for graphite intercalation.
207. Insert a `note` explaining the relationship between continuous `ρ(μ)` and the legacy `N_p`-peak picture: `ξ_j ≈ ∫_{μ ∈ peak_j window} dμ · ρ(μ; q, T) / N_j` where `N_j` is normalization.
208. State explicitly: this derivation is one-way (continuous → discrete), and the rebuild's central state is the continuous form.
209. Begin §4 (음극 내부 전위 V_n, apparent 전위 V_{n,app}, 구동 전위 V_{n,drive} 의 3 종 구분).
210. Preserve the rechecked2 §6.1 three-way separation explicitly.
211. Define `V_n` as the internal anode potential, determined as the implicit solution of the (new continuous) charge balance equation for given `(q, T, ρ)`.
212. Define `V_{n,app} = V_n + s_I · |I| · R_n(q, T, |I|)` as the experimentally observable apparent potential.
213. Define `V_{n,drive}` as the driving potential for reactivity, given by `V_{n,app}` in the reduced-model case or by explicit overpotential in the reaction-resolved case.
214. Add a `note` explaining the role of each potential in the spine.
215. State that `μ` (continuous chemical potential coordinate) is conceptually distinct from `V_n` (internal potential at the electrode boundary): `V_n` is a single boundary value, `μ` ranges over the distribution interior.
216. State the boundary correspondence: the maximum-occupied `μ` at given `(q, T, ρ)` corresponds to `V_n` (after sign convention).
217. Draft a `mdframed` clarifying that this μ ↔ V_n boundary relationship is the new analogue of the legacy `V_{n,OCV}(q, T)` external function — and it is now derived from charge balance, not assumed.
218. Cross-check §3 and §4 against Charter: no step function, no discrete N_p as primary, continuous μ everywhere.
219. Audit Pass 1+2+3.
220. Write Phase E3 Result markdown.
221. Write Phase E3 Result JSON.
222. Validate Phase E3 Result JSON parses.
223. Update ledger Phase E3 row PASS, Gate `PASS_TRANSITION_POTENTIAL_SEPARATION`.
224. Commit Phase E3 deliverables.
225. Push.
226. Record next step entry for Phase E4 (cumulative step 261).
227. End Phase E3 at documented boundary.

(Steps 228-260 reserved for fine-grain content of §3 and §4: figure placeholders, cross-reference to legacy ver5 lines, explicit mapping table of N_p ↔ ρ(μ) peak windows, dimensional consistency check, mdframed warnings. Detailed step list to be expanded in the Phase E3 phase-level plan when Phase E3 is entered.)

Outputs:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (extended with §3 + §4)
- `Claude/results/PHASE_E3_effective_transition_potential_separation_RESULT.md`
- `Claude/results/PHASE_E3_effective_transition_potential_separation_RESULT.json`
- ledger row Phase E3 PASS

## Phase E4 — §5 Writing (Charge Balance — Central Equation)

Steps:

261. Save Phase E4 plan.
262. Load Phase E0-E3.
263. Begin §5 (전하 보존식 — 중심식).
264. State that §5 is the central equation of the Chapter 1 rebuild.
265. Write Eq. 48 explicitly: `Q_cell · q = Q_bg(V_n, T) + ∫_{μ_min}^{μ_max} dμ · ρ(μ; q, T) · n(μ)`.
266. Define `n(μ)` (per-μ Li occupation count): for a unit slab of chemical potential, the equivalent Li count per coulomb. In simplest form `n(μ) = 1` (dimensionless), so `ρ(μ)` carries the dimension `[charge / potential]`.
267. State integration limits: `μ_min` = lowest accessible chemical potential at full-discharge state, `μ_max` = highest at full-charge state. Both are problem-defined boundary parameters.
268. Add a sub-section §5.1 (해 존재 조건).
269. State that for given `(q, T, ρ)`, Eq. 48 may not have a solution in `V_n` if `Q_bg(V_n, T) + ∫ ρ` cannot reach the required `Q_cell · q` — explicit range condition.
270. Add a sub-section §5.2 (Q_bg 의 잔류 chemical capacitance 역할 — preserved from rechecked2 §4.1 lines 129).
271. State that `Q_bg(V_n, T)` carries the residual Li that is not captured by discrete staging peaks in the legacy picture, and in the new picture it carries the Li at chemical potentials outside the dominant `ρ(μ)` support.
272. Add a sub-section §5.3 (총용량 정합 조건 — preserved from rechecked2 §4.3).
273. Restate the capacity-consistency identity in continuous form: `Q_cell = Q_bg(V_{n,1}, T) - Q_bg(V_{n,0}, T) + ∫ dμ · [ρ(μ; q=1, T) - ρ(μ; q=0, T)] · n(μ)`.
274. Add a sub-section §5.4 (배경 용량 함수의 수치 안정성 — preserved from rechecked2 §4.4).
275. Restate `∂Q_bg/∂V_n ≥ ε_Q > 0` as a numerical regularization with smooth-limit-consistency proof in `ε_Q → 0`.
276. Note: this is the only regularization in §5 that uses a strictly positive bound. Charter compliance: explicitly classified `system-fidelity-WARN with smooth-limit-OK`.
277. Add a sub-section §5.5 (이전 ver5 / rechecked2 와의 비교).
278. Note that rechecked2's Eq. charge_balance (line 121-126) is `Q_cell·q = Q_bg(V_n,T) + Σ_j Q_{j,tot} ξ_j` — the discrete sum analogue. Show how it reduces to a coarse-grained limit of the new Eq. 48 by `ρ(μ) → Σ_j Q_{j,tot} δ(μ - U_j)` (Dirac comb).
279. Note that the new Eq. 48 contains the discrete rechecked2 form as a special case but supports continuous staging where rechecked2 cannot.
280. Audit Pass 1+2+3 on §5 with explicit Dim #11.
281. Run dimensional consistency: every term in Eq. 48 must have units of coulombs.
282. Cross-check §5 against Phase E1 spine (Eq. 48 same form).
283. Cross-check §5 against ver5 Ch1 §"전하 보존식": ver5 has no such section (this is the rechecked2-and-new central equation).
284. Cross-check §5 against rechecked2 §4 (lines 118-182): structural correspondence + continuous extension.
285. Write Phase E4 Result markdown with §5 content summary and cross-check.
286. Write Phase E4 Result JSON.
287. Validate JSON parses.
288. Update ledger Phase E4 row PASS, Gate `PASS_CHARGE_BALANCE_CENTRAL`.
289. Commit and push.
290. Record next step Phase E5 (cumulative step 341).
291. End Phase E4 at documented boundary.

(Steps 292-340 reserved for §5 detailed content: example with toy `ρ(μ)`, dimensional table, smooth-limit worked example, validation against rechecked2 limit.)

Outputs:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (extended with §5)
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.md`
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.json`
- ledger row Phase E4 PASS

## Phase E5 ~ Phase E10 — Section Writing (Continuous Distribution, Reactivity Kernel, Progress, ICA/DVA, C-rate/Temperature, Fitting Procedure)

(Detailed step lists to be expanded in each phase-level plan when entered. Each phase carries 60-80 cumulative steps with the same structural pattern: Save plan → Load inputs → Define section content → Draft LaTeX → Audit Pass 1+2+3 (Dim #11 mandatory) → Cross-check vs ver5/rechecked2 → Write Result → Update ledger → Commit pair → Push.)

### Phase E5 — §6 Writing (Continuous Distribution ρ(μ; q, T))
- Steps 341-420 (80 steps)
- Output: `Claude/results/PHASE_E5_continuous_distribution_RESULT.md`, Gate `PASS_CONTINUOUS_DISTRIBUTION`

### Phase E6 — §7 Writing (Continuous Reactivity Kernel S_R(μ) — Replaces Discrete k_j)
- Steps 421-500 (80 steps)
- Output: `Claude/results/PHASE_E6_continuous_reactivity_kernel_RESULT.md`, Gate `PASS_CONTINUOUS_REACTIVITY`

### Phase E7 — §8, §9 Writing (Progress And Barrier Distribution In Continuous Form)
- Steps 501-580 (80 steps)
- Output: `Claude/results/PHASE_E7_progress_barrier_distribution_RESULT.md`, Gate `PASS_PROGRESS_BARRIER`

### Phase E8 — §10 Writing (ICA · DVA Derivation From Continuous ρ(μ))
- Steps 581-640 (60 steps)
- Output: `Claude/results/PHASE_E8_ica_dva_derivation_RESULT.md`, Gate `PASS_ICA_DVA_DERIVATION`

### Phase E9 — §11, §12 Writing (C-rate, Temperature, Empirical Comparison)
- Steps 641-700 (60 steps)
- Output: `Claude/results/PHASE_E9_crate_temperature_emg_RESULT.md`, Gate `PASS_CRATE_TEMP_EMG`

### Phase E10 — §13, §14, §15, §16 Writing (Fitting Procedure, Identifiability, Model Levels)
- Steps 701-780 (80 steps)
- Output: `Claude/results/PHASE_E10_fitting_identifiability_model_levels_RESULT.md`, Gate `PASS_FITTING_IDENT_LEVELS`

## Phase E11 — ★ §17 Writing — Ref. 6, 7 Ratio-Substitution Applied To Graphite

This is the load-bearing phase of the entire rebuild. The user's PhD-level Fredholm 2nd kind ratio-substitution method (Refs. 6, 7 + JCP 2017) is applied here to provide closed-form solutions for the self-consistent integral equation that arises from the continuous reactivity model.

Steps:

781. Save Phase E11 plan as `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e11-ref6-7-application-plan.md`.
782. Load Phase E0 charter (especially §"Ref. 6, 7 application sketch").
783. Load Phase E5 continuous distribution definitions.
784. Load Phase E6 continuous reactivity kernel definitions.
785. Load Phase D `PHASE_D_jcp_ref6_7_methodology_RESULT.md` §"original methodology".
786. Load `Claude/_local_only/jcp_extract.txt` lines 280-389 (§II.C "Solution to Eq. (6) for long-range reaction sink functions") for direct equation reference.
787. Begin §17 (Ref. 6, 7 의 비율 substitution 기법을 graphite 의 연속 reactivity self-consistent integral equation 에 적용).
788. Begin §17.1 (motivation): explain why the Phase E5-E7 continuous form produces a Fredholm 2nd kind self-consistent integral equation in `ρ(μ; q, t)`.
789. Write the new graphite Fredholm 2nd kind equation explicitly from the Phase E6 reactivity kernel: `ρ(μ; q, t) = ρ_0(μ; q, t) + ∫ dμ' · K_n(μ, μ'; q, T) · S_R(μ'; T) · [ρ_eq(μ'; q, T) - ρ(μ'; q, t)]`.
790. Verify structural correspondence to JCP 2017 Eq. (32): `W̄_u(r) ↔ ρ(μ; q, t)`, `r ↔ μ`, `σ ↔ μ_min`, `D ↔ K_n`, `S_R(r)/e^{U₁(r)} ↔ S_R(μ') · ρ_eq(μ')`, `[σ, ∞] ↔ [μ_min, μ_max]`.
791. Note: JCP 2017 integration range `[σ, ∞]` is unbounded, graphite range `[μ_min, μ_max]` is bounded. State that the ratio-substitution method extends to bounded range without loss of generality (justify by referencing JCP 2017 §II.B step + §II.C extension).
792. Note: JCP 2017 time variable absent (steady-state ultimate probability), graphite has explicit `t` evolution. State that the ratio-substitution applies at each `t` slice, with `t` as parameter. This is a generalization of JCP, not a violation.
793. Begin §17.2 (Step 1 of ratio-substitution — formal rearrangement).
794. Write the graphite analogue of JCP 2017 Eq. (33): separate `ρ(μ'; q, t) = (ρ(μ'; q, t) / ρ(μ; q, t)) · ρ(μ; q, t)`, move `ρ(μ; q, t)` outside the integral.
795. Begin §17.3 (Step 2 — ratio-substitution approximation).
796. Identify the simple-case reference distribution `ρ^{simple}(μ; q, T)`: per Phase E0 Step 55, take this as the equilibrium distribution under fixed `V_n = V_{n,OCV}(q, T)` (legacy assumption used as reference, not as canonical model).
797. Write the graphite analogue of JCP 2017 Eq. (34): `ρ(μ'; q, t) / ρ(μ; q, t) ≈ ρ^{simple}(μ'; q, T) / ρ^{simple}(μ; q, T)`.
798. State the validity conditions for this approximation (graphite analogues of JCP 2017 §III conditions): low C-rate (analog of small K), large characteristic chemical potential scale relative to perturbation (analog of large rc), small reactivity (analog of small σ³φ/D).
799. Begin §17.4 (Step 3 — closed-form analytic expression).
800. Write the graphite closed-form analogue of JCP 2017 Eq. (39): `ρ(μ; q, t) = [denominator with ρ^{simple} ratios] / [numerator with K_n integral]`. (Detailed form to be expanded in phase-level plan.)
801. Verify closed-form is dimensionally consistent and Charter-compliant.
802. Begin §17.5 (validity domain and limitation).
803. State quantitative validity boundaries deferred to Phase G (numerical implementation + experimental cross-check), but document the analytic limits.
804. State that outside the validity domain, the closed-form is an approximation; a higher-order ratio-substitution can be applied per JCP 2017 §II.C (line 320-336 truncation order discussion).
805. Begin §17.6 (algorithm pseudocode).
806. Write pseudocode in LaTeX `\begin{algorithm}` or `\begin{verbatim}` environment showing the numerical evaluation of the closed-form for given `(q, T, t)`.
807. Begin §17.7 (한계와 적용 영역).
808. Note the 5 differences from JCP 2017 (Fredholm/Volterra-like time evolution, bounded vs unbounded range, isotropic vs anisotropic, low-rate validity, step-function-vs-continuous-reactivity — this last is the **new** difference identified in audit v0.2 that v0.1 missed).
809. Note that the step-function-vs-continuous difference is precisely the foundation of this Chapter 1 rebuild and is recovered automatically by adopting the continuous reactivity kernel from Phase E6.
810. Note Ref. 6 DOI status: `근거 미발견 (2026-05-27 external search FAIL)`. Cite as plain `J. Chem. Phys. 134, 121102 (2011)` in references.
811. Note Ref. 7 status: title confirmed via WebSearch, URL `pubs.aip.org/aip/jcp/article-abstract/138/16/164123/71188`. DOI not directly confirmed; cite as plain `J. Chem. Phys. 138, 164123 (2013)` in references, with title.
812. Audit Pass 1+2+3 on §17 with explicit Dim #11.
813. Confirm no step function in §17 definitional equations.
814. Confirm closed-form is a continuous expression in `μ`.
815. Cross-check §17 against JCP 2017 §II.C line-by-line.
816. Cross-check §17 against Phase E0 Charter Ref. 6, 7 application sketch (Steps 54-55).
817. Write Phase E11 Result markdown with §17 content summary, cross-check, audit.
818. Write Phase E11 Result JSON.
819. Validate JSON parses.
820. Update ledger Phase E11 row PASS, Gate `PASS_REF6_7_GRAPHITE_APPLICATION`.

(Steps 821-900 reserved for §17 detailed expansion in Phase E11 phase-level plan, including: figure for ρ(μ) shape evolution under reactivity, side-by-side comparison of JCP Eq. and graphite Eq., explicit smooth-limit check of `ρ → δ-comb` recovering rechecked2.)

Outputs:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (extended with §17 — load-bearing section)
- `Claude/results/PHASE_E11_ref6_7_ratio_substitution_RESULT.md`
- `Claude/results/PHASE_E11_ref6_7_ratio_substitution_RESULT.json`
- ledger row Phase E11 PASS, Gate `PASS_REF6_7_GRAPHITE_APPLICATION`

## Phase E12 — §18, §19, §20 Writing And Global Consistency Pass

Steps:

901. Save Phase E12 plan.
902. Begin §18 (ver.2 로 전달되는 기준식).
903. Write the new transfer equations per Phase E1 Step 98: pass continuous `ρ(μ; q, T)`, `V_n(q, t)`, `S_R(μ; T)`, `K_n(μ, μ'; q, T)`, `Q_bg(V_n, T)`, `R_n(q, T, |I|)` to Chapter 2.
904. Note: Chapter 2 must be rewritten consistently. Flag for follow-up roadmap.
905. Begin §19 (자기 검수 체크리스트).
906. List 20+ self-audit items including: every definitional equation is continuous, no step function in primary definitions, every regularization has smooth-limit proof, charge balance is the central equation, Ref. 6, 7 application closes the self-consistent loop, every variable in §2 used at least once, every spine variable referenced in transfer-to-Ch2.
907. Begin §20 (참고문헌).
908. List ver5 Ch1 §19 references (5 entries) verbatim.
909. Add JCP 2017 (user's own paper) with full citation including DOI 10.1063/1.5000882.
910. Add Ref. 6 citation as found in JCP 2017 body (line 711-712), with note `(DOI: 근거 미발견 by 2026-05-27 external search)`.
911. Add Ref. 7 citation as found in JCP 2017 body (line 713-714) + title "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity" (from WebSearch).
912. Add Bazant 2016 / Rykner-Chandesris 2022 from ver5 Ch1 ref list as direct relevance to continuous chemical potential framework.
913. Run global consistency pass on `Claude/docs/graphite_ica_chapter1_v0.1.tex`: every `\ref`, `\eqref` defined; every variable used appears in §2; every section has at least one cross-reference to spine; no orphan equations.
914. Audit Pass 1+2+3 with all 11 dims including Dim #11 across the whole file.
915. Write Phase E12 Result markdown.
916. Write Phase E12 Result JSON.
917. Validate JSON parses.
918. Update ledger Phase E12 row PASS, Gate `PASS_TRANSFER_AUDIT_REFS`.

(Steps 919-980 reserved for global consistency detailed steps.)

Outputs:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (complete)
- `Claude/results/PHASE_E12_transfer_audit_references_RESULT.md`
- ledger row Phase E12 PASS

## Phase F1 — LaTeX Build Environment Setup And First Build Attempt

Steps:

981. Save Phase F1 plan.
982. Run `which pdflatex xelatex lualatex` to detect available engines.
983. Run `which kotex` or `kpsewhich kotex.sty` for Korean LaTeX availability.
984. Choose engine per priority: xelatex if kotex available; else lualatex; else pdflatex (likely fails for Korean).
985. Document engine choice in Phase F1 Result.
986. Run first build: `<engine> -interaction=nonstopmode graphite_ica_chapter1_v0.1.tex`.
987. Capture build log to `Claude/results/PHASE_F1_build_first_attempt_log.txt`.
988. Capture PDF output if any.
989. Classify build outcome: PASS (no errors), WARN (warnings only), FAIL (errors).
990. If PASS: confirm PDF page count is reasonable and ≥ section count.
991. Write Phase F1 Result markdown.
992. Update ledger Phase F1 row.

(Steps 993-1020 reserved for build environment edge cases.)

## Phase F2 — Build Error Correction Loop

Steps 1021-1060: Up to 3 rounds of error correction. Each round: read error log → identify cause → fix in `.tex` → rebuild → audit pass on changes.

## Phase F3 — PDF User Review Request (★ Decision Gate)

Steps:

1061. Save Phase F3 plan.
1062. Stage `Claude/docs/graphite_ica_chapter1_v0.1.pdf` for user review.
1063. Write a review request note listing: spine intent check, Phase E11 §17 ref.6,7 application math check (user as author), Charter compliance check on Dim #11, GATE_C4 mapping label adequacy (from Phase C deferred), DQ-G1-G5 of audit v0.2.
1064. Submit to user (commit + push, then notify in conversation).
1065. Decision Gate `GATE_F3`: wait for user GO or correction instruction.
1066. If user GO: proceed to Phase F4.
1067. If user correction instruction: write correction items to Decision Queue and enter Phase F4.

(Steps 1068-1100 reserved.)

## Phase F4 — User Feedback Application And v0.2 File Creation

Steps 1101-1180: per correction item, decide minor (in-place edit + commit) or major (new file `chapter1_v0.2.tex` + supersession marker per addendum pattern).

## Phase F5 — Final Commit, Ledger Closure, Follow-up Plan Decision

Steps:

1181. Save Phase F5 plan.
1182. Confirm all Phase E0-F4 rows in ledger PASS.
1183. Compose final commit message summarizing rebuild outcome.
1184. Commit final state.
1185. Push.
1186. Write `Claude/results/PHASE_F5_closure_RESULT.md` summarizing: how the rebuild addressed v0.1 Audit's gap list, how Charter Dim #11 was enforced, how user verbatim "step function 가정" was avoided.
1187. Plan that Chapter 2 (thermal) rebuild requires its own master roadmap referencing new Ch1 §18 transfer equations.
1188. Plan that numerical implementation (Phase G) requires its own master roadmap.
1189. Plan that empirical validation (Phase H) requires its own master roadmap.
1190. Write Decision Queue summary for user.

(Steps 1191-1220 reserved.)

Outputs:

- `Claude/results/PHASE_F5_closure_RESULT.md`
- final ledger row Phase F5 PASS
- follow-up roadmap stubs (Chapter 2 / Phase G / Phase H placeholders)

## Implementation Interfaces

### Charter File Schema

```markdown
# Chapter 1 Rebuild Charter

## Objective
[1 sentence]

## Anti-Pattern List
- [pattern]: [ver5/rechecked2 line evidence]
...

## Allowed-Pattern List
- [pattern]: [intended use]
...

## Forbidden-Pattern List
- [pattern]: [reason]
...

## Smooth-Limit Consistency Rule
- [regularization]: [smooth-limit expression] [ε → 0 recovered form]
...

## Audit Dimension #11 Procedure
- Pass 1: [enumerate]
- Pass 2: [classify]
- Pass 3: [verify]

## Legacy ↔ New Variable Mapping
| Legacy | New | Derivation |
|...|...|...|

## Central Equation Preview
- Eq. 48: [LaTeX]
- Eq. 49: [LaTeX]

## Ref. 6, 7 Application Sketch
- ρ^{simple} candidate: [definition]
- Ratio substitution: [equation]
- Validity domain: [conditions]
```

### Variable Inventory JSON Schema

```json
{
  "canonical_variables": [
    {"symbol": "mu", "latex": "\\mu", "unit": "V", "description": "...", "first_used_section": "§3"}
  ],
  "derived_variables": [
    {"symbol": "xi_j", "latex": "\\xi_j", "derivation": "\\int_{peak_j} d\\mu \\rho(\\mu; q, T) / N_j", "first_used_section": "§3"}
  ],
  "parameters": [
    {"symbol": "Q_cell", "unit": "C", "constant": true}
  ]
}
```

### Ledger Row Format

(Per `feedback_phase_execution_loop` §3 12-column schema.)

### Audit Dim #11 Result Format

```markdown
| Phase | Pass 1 flags | Pass 2 classify | Pass 3 verify | FAIL count |
|...|...|...|...|...|
```

## Test Plan

| # | Item | Method | Pass Criterion |
|---|---|---|---|
| T1 | Charter Dim #11 enforced | grep new Chapter 1 for `max(`, `min(`, `\\step`, `\\Heaviside`, `\\sign`, `logistic`, `sigmoid`, `erf`, `softplus`, `tanh`, `ReLU` | every occurrence classified WARN-with-smooth-limit or OK-with-error-bound, 0 FAIL |
| T2 | Spine equations dimensional consistency | manual dimensional check on Eq. 48, 49, V_{n,app}, dQ/dV | every term consistent |
| T3 | Continuous distribution recovers discrete limit | substitute `\rho(\mu) = \sum_j Q_{j,tot} \delta(\mu - U_j)` in Eq. 48 | recover rechecked2 Eq. charge_balance form |
| T4 | Ref. 6, 7 application closed-form recovers JCP 2017 in 3-D radial limit | manual structural check | structural correspondence verified |
| T5 | LaTeX build PASS | run engine on `chapter1_v0.1.tex` | exit 0, PDF generated |
| T6 | Variable inventory completeness | every variable in spine appears in §2 | 100% coverage |
| T7 | Section spine cross-reference | every § references at least one spine equation | 0 orphans |
| T8 | Ref. 6 DOI external search log | record all attempts | log present, fallback `근거 미발견` acceptable |
| T9 | Phase audit Pass 1+2+3 every phase Dim #11 | inspect Phase E0-F5 result files | 0 FAIL, all phases logged |
| T10 | User review Decision Gate `GATE_F3` | user response in conversation | explicit GO or explicit correction list |
| T11 | Audit v0.2 user approval (Decision Gate `DQ-G1`) | user response | explicit GO before Phase E0 entry |
| T12 | Charter compliance global | grep entire `chapter1_v0.1.tex` for anti-pattern keywords | 0 anti-pattern hits in definitional sections |
| T13 | Smooth-limit consistency every regularization | inspect each ε-regularized expression | every regularization has explicit smooth-limit |
| T14 | Self-audit checklist §19 has ≥ 20 items | count items | ≥ 20 |
| T15 | Transfer-to-Ch2 §18 lists continuous-form quantities | inspect | ρ, V_n, S_R, K_n, Q_bg, R_n all listed; ξ_j-based transfer absent |
| T16 | All Phase E0-F5 ledger rows PASS or BLOCKED with reason | inspect ledger | 0 silent FAIL |
| T17 | No `Claude/docs/` write during charter phases (E0-E1) | git log | confirmed |
| T18 | No `Codex/` read across entire rebuild | git/file access log | confirmed |
| T19 | Ref. 6 / Ref. 7 self-search log present in Phase E0 | inspect Phase E0 Result | log present |
| T20 | Audit Dim #11 added to global memory after audit v0.2 approval | inspect `~/.claude/projects/d--Projects/memory/` | new memory file present (if DQ-G5 approved) |

## Assumptions

- A1. User approves Audit Report v0.2 (DQ-G1) before Phase E0 enters. Until approval, this roadmap is in `READY_FOR_USER_REVIEW` state.
- A2. User has not yet confirmed or denied the new spine (DQ-G2). Phase E1 will enter under assumption that the spine draft is acceptable; user may correct via Phase F3 Decision Gate.
- A3. User has not provided DQ1 answer (ChatGPT 의 큰 논리 오류 정체). Phase E2 §1 will note this anti-pattern reference is incomplete and may be revised in Phase F4 if user provides.
- A4. Ref. 6 DOI remains `근거 미발견` if external search after multiple attempts (Phase E0 Steps 40-44) does not surface it. User may optionally provide (DQ-G4).
- A5. Ref. 7 DOI similar to A4.
- A6. LaTeX engine xelatex + kotex is available in user environment (DQ-E3 from v0.1, deferred to Phase F1).
- A7. New audit Dim #11 memory + memory candidates B4/B5/B6 (DQ-G5) are pending user approval. Until approved, Dim #11 is project-local for Chapter 1 rebuild only.
- A8. Continuous chemical potential interpretation `μ` as Li/Li⁺ reference electrochemical potential is the user's intended semantics. If user clarifies differently (DQ-G2), revise.
- A9. JCP 2017 §II.C ratio-substitution applies to bounded-range Fredholm 2nd kind without loss. If user disputes this generalization, revise Phase E11 Step 791.
- A10. Cumulative step numbering continues from Phase A~D (1-18). Phase E0 starts at step 19. Phase F5 ends at step 1220. No re-numbering of legacy Phase A~D.
- A11. ver5 and ver1_rechecked2 are never modified throughout the rebuild. Their roles are evidence + anti-pattern reference + cross-check baseline only.
- A12. Phase E0-F5 commit pairs follow `feedback_phase_audit_workflow` standard. Phase F3 user review is a single-commit decision gate, not a pair.
- A13. The continuous-form spine reduces correctly to the rechecked2 spine in the discrete `ρ → Σ_j δ(μ - U_j)` limit (T3 above). If this limit check fails, return to Phase E1 and redesign.
- A14. The continuous reactivity kernel `S_R(μ)` can be chosen as a Marcus-theory-derived form (Gaussian in μ) or a Cahn-Hilliard-derived form (chemical-potential-difference dependent) — choice is Phase E6 deliverable.
- A15. Chapter 2~5 rebuild after Chapter 1 will require parallel roadmaps. This roadmap does not block on them.

## Correction History

- v0.1 (`...-from-scratch-plan.md`, 436 lines, 2 phase, 17 step): superseded by this v0.2 master roadmap. v0.1 lacked RO_SkillDict-level granularity, lacked the Charter / Dim #11 / continuous-chemical-potential foundation, and contained the now-rejected DQ-E2 (Ref. 6, 7 DOI user-delegation).
- v0.2 (this file): rewritten from scratch. Step granularity per RO_SkillDict pattern. Charter + Dim #11 explicit. Continuous chemical potential as the foundational shift addressing the user's verbatim "step function 가정 = 모사 대상 시스템 특성 완전 무시" diagnosis.

## Success Criteria (Sprint Contract)

- [ ] Phase E0: Charter document with all 9 sections, Gates 1-8 PASS, audit Dim #11 procedure operational.
- [ ] Phase E1: New spine explicitly written, Charter-compliant, ≥ 3 self-consistent loops classified, Ref. 6, 7 application target identified.
- [ ] Phase E2-E12: `Claude/docs/graphite_ica_chapter1_v0.1.tex` complete with §1-§20, all sections audit PASS Dim #11, variable inventory complete.
- [ ] Phase E11 (load-bearing): §17 Ref. 6, 7 ratio-substitution applied to graphite Fredholm 2nd kind, closed-form recovered, validity domain documented.
- [ ] Phase F1: LaTeX build PASS, PDF generated.
- [ ] Phase F3: User Decision Gate satisfied (GO or explicit correction list).
- [ ] Phase F5: Final ledger closure, Chapter 2 / Phase G / Phase H roadmap stubs created.
- [ ] T1-T20: all test plan items PASS or documented BLOCKED with reason.
- [ ] DQ-G1-G5 of audit v0.2: each resolved (user approval, user cross-check, optional user info, or fallback documented).

## QA Tier (Sprint Contract)

- [ ] Quick (Critical / High only)
- [x] **Standard (+ Medium)** ← default + appropriate for rebuild scope
- [ ] Exhaustive (everything, including cosmetic)

Rationale: rebuild scope is large but Cosmetic-level LaTeX polish is Phase F-only. Exhaustive across all 17 phases would balloon scope. Standard captures Medium per phase audit Dim #11 findings and Decision Queue resolution.

## Decision Queue

| ID | Item | Priority | Action |
|---|---|:---:|---|
| **DQ-G1** | User approval of audit report v0.2 | ★ blocking | wait for explicit GO before Phase E0 |
| **DQ-G2** | User cross-check of continuous chemical potential `μ` semantics + new spine acceptability | high | Phase E1 enters under assumption; Phase F3 explicit review |
| **DQ-G3** | DQ1 (ChatGPT 의 큰 논리 오류 정체) — for Phase E2 §1 anti-pattern note | medium | optional, Phase F4 revision available |
| **DQ-G4** | Ref. 6 DOI (and Ref. 7 DOI confirmation) — user-as-author option, not user-as-search-fallback | medium | Phase E0 self-search first; ask user only if author-side provides easier |
| **DQ-G5** | Audit Dim #11 + B4/B5/B6 memory candidates global adoption | medium | Phase E0 uses Dim #11 project-locally until approved |
| **DQ-G6** | Chapter 2 rebuild master roadmap timing (immediately after Phase F5 vs. delay) | low | Phase F5 closure decision |
| **DQ-G7** | Phase G (numerical implementation) decision: solver language (Python `scipy.integrate.solve_bvp` for Fredholm + DAE; or Julia DifferentialEquations.jl) | low | post-Chapter 1 |
| **DQ-G8** | Phase H (empirical validation) data source: user has graphite ICA experimental data? if yes, format? | low | post-Chapter 1 |

## Meta

- This roadmap follows `feedback_plan_template_11sections` (with Sprint Contract + Decision Queue extensions).
- This roadmap follows `feedback_plan_continuation_until_done` for inter-phase auto-progression — user GO at DQ-G1 covers Phase E0 through F2. Phase F3 is a Decision Gate by design (PDF user review). Phase F4 onward auto-proceeds from F3 GO.
- Per `feedback_document_protection_addendum_pattern`, ver5 and ver1_rechecked2 are never modified; v0.1 plan is superseded by this v0.2 (marker file).
- Per `feedback_external_lookup_first_self` (candidate memory), Ref. 6, 7 DOI is self-searched first.
- Per audit Dim #11 (Charter §"Audit Dim #11 Procedure"), every phase's audit includes the system-fidelity pass.
- All phase-level plans (e.g., `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md`) will be created at the start of each phase per RO_SkillDict pattern. This master roadmap is the canonical reference for cumulative step numbering and Phase Range.
