# Phase E2 — §1, §2 Writing (Purpose, Notation, Units) Phase-Level Plan

## Summary

- Status: `READY_FOR_EXECUTION` → executed in same turn as user "계속" 2026-05-27
- Parent roadmap: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
- Phase Range: cumulative Steps **141 ~ 200** (60 steps)
- Scope: Initialize `Claude/docs/graphite_ica_chapter1_v0.1.tex` with LaTeX preamble + §1 (문서의 목적과 원칙) + §2 (기호와 단위 컨벤션). This is the **first LaTeX file write** of the rebuild.
- Charter and Phase E1 spine are the foundational inputs. Every notation row in §2 must correspond 1:1 with the Phase E1 canonical variable inventory.
- TDD-like discipline: Charter Dim #11 Pass 1 is applied inline during writing, not only post hoc.

## Current Ground Truth

- Phase E1 closed PASS at commit `f585fe3`. Spine §A.3 (5 components), canonical variables §B (17 entries), derived §C (17 entries), loops §D (3), transfer §E (T1-T9), legacy mapping §F (ver5 21 + rechecked2 11 + Phase B 23).
- Charter `PHASE_E0_..._RESULT.md` §3.1 canonical namespace, §3.2 central equations, §5 smooth-limit rule, §6 audit Dim #11 procedure.
- ver5 preamble lines 1-44 (kotex + amsmath + booktabs + longtable + hyperref + fancyhdr + mdframed + amsthm + setspace).
- rechecked2 preamble lines 1-36 (mostly identical, slightly different setstretch/parskip).
- No `Claude/docs/graphite_ica_chapter1_*.tex` exists yet — this phase creates v0.1.

## Non-goals (this phase)

- Do not write §3 onwards (Phase E3+).
- Do not include any spine equation derivation beyond the §1 boxed preview — the full derivation belongs to §4 (Phase E4).
- Do not include any specific `S_R(μ; T)` or `K_n(μ, μ'; q, T)` functional form (Phase E6).
- Do not include any LaTeX bibliography (Phase E12 §20).
- Do not attempt LaTeX build (Phase F1).

## Implementation Changes

Planned new files:

- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e2-intro-notation-plan.md` (this file)
- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (★ first LaTeX file, preamble + §1 + §2)
- `Claude/results/PHASE_E2_intro_notation_RESULT.md`
- `Claude/results/PHASE_E2_intro_notation_RESULT.json`

Ledger update only (no new ledger file):
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` Phase E2 row updated to PASS.

No file in `Claude/_local_only/` or `Codex/` accessed.

## Steps (Phase E2, cumulative 141 ~ 200)

(Master roadmap Phase E2 Steps 141-200 verbatim, with execution notes.)

141. Save Phase E2 plan as this file — **DONE by writing this file**.
142. Save companion JSON for Phase E2 plan — **DEFERRED**: consolidated into Result JSON.
143. Load Phase E0 charter and Phase E1 spine into Phase E2 context.
144. Start `Claude/docs/graphite_ica_chapter1_v0.1.tex` with LaTeX preamble derived from ver5 preamble (lines 1-44) + rechecked2 preamble (lines 1-36).
145. Add `\usepackage{kotex}` for Korean if available (xelatex/lualatex compatible).
146. Define LaTeX command macros for new variables: `\rhomu` (continuous distribution), `\Sreact` (reactivity kernel), `\Kncross` (cross-kernel), `\mucont` (continuous chemical potential), `\rhoeq` (equilibrium distribution); preserve `\dd`, `\OCV`, `\app`, `\drive`, `\eq`, `\eff`, `\bg`, `\cell`, `\tot` from ver5/rechecked2.
147. Add `% CHARTER COMPLIANCE` header comment at top, listing Charter §2 anti-pattern + §4 forbidden-pattern + §5 smooth-limit rule + §6 audit Dim #11 reference.
148. Write `\title{...}`, `\author{Claude (Project_Anode_Fit Claude 측)}`, `\date{2026-05-27}`.
149. Write `\maketitle` and `\tableofcontents`.
150. Begin §1.
151. Draft §1 paragraph 1 (목적): 1 sentence on continuous μ + continuous reactivity + Ref 6/7 ratio-substitution.
152. Draft §1 paragraph 2 (원칙): 4 numbered principles per Charter §3.
153. Draft §1 paragraph 3 (적용 범위): low-rate to finite C-rate, OCV vs 0.2C, isothermal default with extension paths.
154. Draft §1 paragraph 4 (ver5/rechecked2 와의 관계): explicit from-scratch rebuild note.
155. Insert boxed spine equation summary (Phase E1 §A.3 5 components abbreviated).
156. Add `\begin{mdframed}` note: "본 문서는 ξ_j 를 primary state 로 사용하지 않는다. ξ_j 는 ρ(μ; q, T) 로부터 derive 되는 양이다."
157. Begin §2.
158. Begin §2.1 (기호 정의) as `longtable`.
159-161. Add canonical (17), derived (17), parameter rows.
162. Verify every spine variable appears in §2.1.
163. Verify §2.1 row count matches Phase E1 inventory.
164. Begin §2.2 (단위 컨벤션).
165-175. State units for Q_cell (C), μ (V), ρ (C/V), S_R (1/s pending), K_n (1/(V·s) pending), R_n (Ω), I (A), T (K), t (s), q (dimensionless).
176. Begin §2.3 (전류·전위 부호).
177-179. s_I, s_{φ,j} sign conventions, discharge direction default, charge-branch deferred to Ch5.
180. Closing §2 with 1-line summary connecting back to §1 spine.
181-183. Audit Pass 1+2+3 on §1 + §2: enumerate every functional form; check no AP/FB hit.
184-185. Cross-check §2 variable definitions against Phase E1 spine; dimensional consistency.
186. Record any unit-conflict.
187. Confirm `chapter1_v0.1.tex` line count bounded (target ≤ 250 lines after Phase E2).
188-189. Write Phase E2 Result md + JSON.
190. Validate Result JSON parses.
191. Update ledger Phase E2 row PASS.
192. Audit Pass 1+2+3 with all 11 dims on Phase E2 deliverable.
193. Commit pair: `chapter1_v0.1.tex` (source) + `PHASE_E2_RESULT.md` + ledger.
194-195. Push + confirm.
196. Mark Phase E2 row PASS, Gate `PASS_INTRO_NOTATION`.
197. Record next-step Phase E3 (step 201).
198. Stop if §2 var count ≠ Phase E1 inventory.
199. Stop if §1 or §2 sentence implies discrete N_p as primary state.
200. End Phase E2 at documented boundary.

## Test Plan (this phase)

- T-E2-1: `chapter1_v0.1.tex` file exists with valid LaTeX preamble.
- T-E2-2: §1 contains 4 numbered principles per Charter §3.
- T-E2-3: §1 boxed spine equation summary present.
- T-E2-4: §2.1 longtable contains all 17 canonical variables from Phase E1 §B.
- T-E2-5: §2.1 includes legacy-derived rows with explicit "derived from continuous form" tag.
- T-E2-6: §2.2 units match Phase E1 inventory (Eq.49-related units may be marked "pending Phase E6").
- T-E2-7: §2.3 sign conventions consistent with rechecked2 §6.1.
- T-E2-8: Audit Dim #11 Pass 1 scan of §1+§2: 0 FAIL (no `max`, `min`, logistic, erf, softplus, sigmoid, Heaviside, sign in definitional contexts).
- T-E2-9: Result JSON parses.
- T-E2-10: Total `.tex` line count ≤ 250.

## Assumptions

- A-E2-1. xelatex (with kotex) is the assumed build engine. Build verification deferred to Phase F1.
- A-E2-2. `n(μ) = 1` default per Phase E1 §B canonical entry 17; appears in §2.1 with this default note.
- A-E2-3. Eq.49 unit reconciliation (OI-E0-1) is deferred to Phase E6; §2.2 marks S_R and K_n units as "pending Phase E6 detailed kernel construction".
- A-E2-4. Section numbering follows Charter §3 / Phase E1 §A spine order; §1 = purpose, §2 = notation; §3 onwards in subsequent phases.

## Decision Queue (this phase)

- No new DQ. OI-E0-1, OI-E1-1/2/3 propagated. DQ-G2 (μ semantics) propagated to Phase F3.

## Sprint Contract

- [ ] T-E2-1 ~ T-E2-10 all PASS.
- [ ] Audit 11/11 PASS, Dim #11 0 FAIL.
- [ ] Commit + push + ledger Phase E2 row PASS, Gate `PASS_INTRO_NOTATION`.
- [ ] Phase E3 entry clear (next cumulative step 201).
