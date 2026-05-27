# Phase E3 — §3, §4 Writing (Effective Transition + 3-Way Potential Separation) Phase-Level Plan

## Summary

- Status: `READY_FOR_EXECUTION` → executed in same turn as user "고" 2026-05-28
- Parent roadmap: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
- Phase Range: cumulative Steps **201 ~ 260** (60 steps)
- Scope: Extend `Claude/docs/graphite_ica_chapter1_v0.1.tex` with §3 (흑연 staging과 연속 화학 퍼텐셜) and §4 (V_n / V_{n,app} / V_{n,drive} 3-way potential separation). These two sections together establish the continuous distribution interpretation of graphite staging and lock the three-way potential semantics that the spine relies on.
- Charter §3.1 canonical namespace + Phase E1 §B spine + Phase E2 §1+§2 notation are inputs.
- Continuous chemical potential `μ` interpretation must be made physically explicit in §3, with a one-way `continuous → discrete N_p` derivation as a backward-compatibility note (never the reverse).
- §4 lifts the rechecked2 §6.1 three-way separation verbatim in spirit, but rewires it onto the new ρ(μ) spine: V_n is the boundary value of the continuous ρ distribution, not just a single number tracked alone.

## Current Ground Truth

- Phase E2 closed PASS-with-note at commit `144d565`. `chapter1_v0.1.tex` exists with preamble + §1 + §2, 381 lines.
- Charter (`PHASE_E0_..._RESULT.md`) governs all writing.
- Phase E1 spine §A.3, §B canonical 17, §C derived 17 are the operational inventory.
- rechecked2 §6.1 (line 204-238) is the legacy three-way separation source; preserved as-is in spirit, rewritten with new ρ(μ) semantics.
- Bazant 2016 (ver5 ref [4], J.P.C. Lett.) and Rykner-Chandesris 2022 (ver5 ref [5], JPCC) are physically-grounded continuous-chemical-potential references for graphite staging.

## Non-goals (this phase)

- Do not write §5 onwards (Phase E4+).
- Do not fully detail `ρ_eq(μ; q, T)` functional form (Phase E5).
- Do not fully detail `S_R(μ; T)` or `K_n(μ, μ'; q, T)` functional form (Phase E6).
- Do not write any equation that requires Eq.49 unit reconciliation (deferred to Phase E6).
- Do not perform LaTeX build (Phase F1).
- Do not request user clarification on μ semantics (DQ-G2 → Phase F3).

## Implementation Changes

Planned new files:

- `Claude/plans/2026-05-28-anode-fit-chapter1-rebuild-phase-e3-effective-transition-plan.md` (this file)
- `Claude/results/PHASE_E3_effective_transition_potential_separation_RESULT.md`
- `Claude/results/PHASE_E3_effective_transition_potential_separation_RESULT.json`

Updated:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` — append §3 and §4 (target: +200 ~ +250 lines).
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` — Phase E3 row updated PASS.

No file in `Claude/_local_only/` or `Codex/` accessed.

## Steps (Phase E3, cumulative 201 ~ 260)

(Master roadmap Phase E3 Steps 201-260 verbatim, with execution notes.)

201. Save Phase E3 plan as this file — **DONE by writing this file**.
202. Load Phase E0-E2 deliverables into Phase E3 context.
203. Begin §3 (흑연 staging과 연속 화학 퍼텐셜) in `chapter1_v0.1.tex`.
204. Draft §3.1 (continuous μ replacing N_p): explain that ver5 §3 decomposed graphite into N_p discrete effective transitions, but this Chapter 1 treats staging as a continuous distribution in μ-space.
205. Draft §3.2 (ρ(μ; q, T) interpretation): define `ρ(μ; q, T) dμ` as the Li content (charge density) per chemical potential window `[μ, μ + dμ]` at state `(q, T)`.
206. Draft §3.3 (physical grounding citations): cite Bazant Cahn-Hilliard (ver5 ref [4]) and Rykner-Chandesris (ver5 ref [5]) as the continuous-chemical-potential framework references for graphite intercalation.
207. Draft §3.4 (continuous → discrete one-way derivation): `ξ_j ≈ (1/N_j) ∫_{μ ∈ peak_j window} dμ · ρ(μ; q, T)` with normalization `N_j`.
208. Insert §3.4 mdframed note: this derivation is one-way (continuous → discrete), and the rebuild's central state is the continuous form. Reverse derivation (discrete → continuous) is not used.
209. Begin §4 (V_n, V_{n,app}, V_{n,drive} 3-way separation) in `chapter1_v0.1.tex`.
210. Preserve rechecked2 §6.1 three-way separation in spirit. Adapt to new ρ(μ) semantics.
211. Define §4.1 V_n as internal anode potential = implicit solution of Eq.48 charge balance (cross-ref `eq:charge_balance` to be defined in §5/Phase E4; placeholder `eq:spine_summary` (2) in §1 boxed equation).
212. Define §4.2 V_{n,app} = V_n + s_I · |I| · R_n (already given in §2.3 Eq. `Vapp_def`, restate in §4 with role-context).
213. Define §4.3 V_{n,drive} = V_{n,app} in reduced model (and footnote that reaction-resolved extension is Phase E6).
214. Add §4.4 mdframed note: roles of each potential — V_n is the model's internal state, V_{n,app} is the experimental observable, V_{n,drive} is the kernel-driving argument.
215. State §4.5 μ vs V_n distinction: μ is the distribution interior coordinate (ranges over `[μ_min, μ_max]`), V_n is a single boundary value attached to the distribution.
216. State §4.5 boundary correspondence: at equilibrium (`ρ = ρ_eq`), the boundary of the ρ_eq distribution in μ-space corresponds to V_n via the charge balance solution.
217. Draft §4.5 mdframed: this μ ↔ V_n boundary relationship is the new analogue of the legacy `V_{n,OCV}(q, T)` external function — derived from Eq.48, not assumed externally.
218. Cross-check §3 and §4 against Charter: Pass 1 keyword scan for max/min/logistic/erf/sigmoid/softplus/Heaviside/sign in §3+§4. Pass 2 classify. Pass 3 verify 0 FAIL.
219. Apply audit Pass 1+2+3 across all 11 dims.
220. Write Phase E3 Result md.
221. Write Phase E3 Result JSON.
222. Validate Result JSON parses.
223. Update ledger Phase E3 row PASS.
224. Commit pair (source `chapter1_v0.1.tex` extension + Result + JSON + ledger).
225. Push.
226. Record next-step Phase E4 (cumulative step 261).
227. End Phase E3 boundary.
228-260. Reserved for §3.1-§4.5 detailed prose, mdframed environments, and cross-references. Detailed execution embedded in body writing.

## Test Plan (this phase)

- T-E3-1: `chapter1_v0.1.tex` extended with §3 and §4 (file line count grows by +180~+250).
- T-E3-2: §3 contains 4 subsections (continuous-μ rationale, ρ interpretation, physical grounding citations, continuous→discrete derivation).
- T-E3-3: §4 contains 5 subsections (V_n implicit, V_{n,app}, V_{n,drive}, role-mdframed, μ↔V_n boundary correspondence).
- T-E3-4: §3.4 derivation is explicitly one-way (continuous→discrete only, never reverse).
- T-E3-5: §4 references rechecked2 §6.1 spirit but uses new ρ-spine semantics.
- T-E3-6: Audit Dim #11 Pass 1 scan of §3+§4: 0 FAIL in definitional contexts.
- T-E3-7: Charter compliance: no AP/FB hit in §3 or §4 definitional equations.
- T-E3-8: Result JSON parses.
- T-E3-9: Ledger Phase E3 row PASS, Gate `PASS_TRANSITION_POTENTIAL_SEPARATION`.
- T-E3-10: No file in `Claude/_local_only/` or `Codex/` accessed.

## Assumptions

- A-E3-1. μ semantics = Li/Li⁺-reference electrochemical potential (Phase E0 §3.1, DQ-G2 deferred).
- A-E3-2. `ρ_eq(μ; q, T)` functional form (Gaussian, Marcus, Bazant-CH, etc.) is Phase E5 work; §3 only defines what ρ_eq "is", not its functional shape.
- A-E3-3. The peak window for the continuous → discrete derivation (§3.4) is defined operationally (not equation-by-equation) — formal peak-window definition is Phase E5 / E10 work.
- A-E3-4. The new "μ ↔ V_n boundary" relationship in §4.5 is described conceptually (qualitative) in Phase E3; formal equation derivation belongs to §5 (Phase E4 charge balance).

## Decision Queue (this phase)

- No new DQ. DQ-G2 (μ semantics) propagated.

## Sprint Contract

- [ ] T-E3-1 ~ T-E3-10 all PASS.
- [ ] Audit 11/11 PASS, Dim #11 0 FAIL.
- [ ] Commit + push + ledger Phase E3 row PASS, Gate `PASS_TRANSITION_POTENTIAL_SEPARATION`.
- [ ] Phase E4 entry clear (next cumulative step 261).
