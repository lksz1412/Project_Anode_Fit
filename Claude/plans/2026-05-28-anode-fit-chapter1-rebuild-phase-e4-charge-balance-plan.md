# Phase E4 — §5 Writing (Charge Balance Central Equation, Continuous Reformulation) Phase-Level Plan

## Summary

- Status: `READY_FOR_EXECUTION` → executed in same turn as user "다음 단계 ㄱㄱ" 2026-05-28
- Parent roadmap: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
- Phase-level scope: cumulative Steps **261 ~ 340** (80 steps), §5 of new Chapter 1
- **★ This is the first phase under Charter Addendum 1 §11 Writing Precision Standard.** Every equation derivation must follow §11.1–§11.4 rules: no logical jump, no omission, undergraduate-level prose, with §11.5 reporting in this phase Result.
- Spine component (2) from §1 Eq. `spine_summary` is the target: derive `Q_cell · q = Q_bg(V_n, T) + ∫_{μ_min}^{μ_max} dμ · ρ(μ; q, T) · n(μ)` step-by-step from conservation of charge.

## Current Ground Truth

- Phase E3 closed PASS at commit `0972d9c`. `chapter1_v0.1.tex` is 663 lines (preamble + §1 + §2 + §3 + §4).
- Charter Addendum 1 added §10 (Session Purpose), §11 (Writing Precision Standard), and §6 audit Dim #11 extension.
- §3 established ρ(μ; q, T) as continuous distribution and ξ_j as one-way derived.
- §4 established V_n as implicit solution of the charge balance equation, with three-way potential separation.
- §5 derives the very equation that §4.1 referenced. Forward references in §3 and §4 resolve here.

## Non-goals (this phase)

- Do not write §6 onwards.
- Do not define functional form of `ρ_eq(μ; q, T)` (Phase E5).
- Do not define `S_R(μ; T)` or `K_n(μ, μ'; q, T)` (Phase E6).
- Do not implement numerical solver code (Charter Addendum 1 §10.1).
- Do not perform LaTeX build (Phase F1).
- Do not derive Eq. 49 (Fredholm 2nd kind ρ evolution) — Phase E6/E7.

## Implementation Changes

Planned new files:

- `Claude/plans/2026-05-28-anode-fit-chapter1-rebuild-phase-e4-charge-balance-plan.md` (this file)
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.md`
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.json`

Updated:

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` — append §5 (target +250 ~ +350 lines).
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` — Phase E4 row PASS.

## §5 Content Plan (Under §11 Writing Precision Standard)

§5 will contain the following derivation blocks, each fully expanded per §11.1–§11.3:

### §5.1 Setup: external vs internal charge

- Define what is "external charge" `Q_ext` (charge that crossed the external circuit).
- Define what is "internal charge state" (Li atoms residing in the graphite host frame at given (q, T, ρ)).
- State the conservation principle: external charge supplied = internal charge stored (per Faraday's law).
- Derivation block B1: Q_ext as time integral of current — `Q_ext(t) = ∫_0^t |I(t')| dt'`.
- Derivation block B2: constant-current and capacity normalization — `Q_ext = Q_cell · q` when `q = Q_ext / Q_cell`.

### §5.2 Internal charge decomposition: background + distribution

- State that internal Li occupation has two components: (a) a "background" component absorbed in `Q_bg(V_n, T)`, and (b) a distributed component over chemical potential coordinate μ.
- Physical interpretation of `Q_bg`: residual chemical capacitance, including any Li occupation that does not show up as a localized peak in the μ-distribution.
- Physical interpretation of `∫ dμ ρ(μ; q, T) n(μ)`: Li occupation distributed across μ-space, captured by `ρ` density.
- Derivation block B3: total internal Li charge = `Q_bg + ∫ ρ · n dμ`.

### §5.3 The central equation (Eq. 48)

- State the central equation:
  ```
  Q_cell · q = Q_bg(V_n, T) + ∫_{μ_min}^{μ_max} dμ · ρ(μ; q, T) · n(μ)
  ```
- Derivation block B4: from §5.1 (external) and §5.2 (internal), apply conservation → Eq. 48.
- Dimensional check: every term in [C].
- Identify which variable is implicit: V_n appears inside `Q_bg(V_n, T)` argument; ρ is the distribution. Given (q, T, ρ), V_n is solved from this equation.

### §5.4 Existence of V_n solution

- Question: does Eq. 48 always have a V_n solution?
- Answer: depends on the range of `Q_bg(·, T)` and the value of `Q_cell · q − ∫ ρ · n dμ`.
- Derivation block B5: solution existence condition `Q_{bg,min}(T) ≤ Q_cell·q − ∫ ρ · n dμ ≤ Q_{bg,max}(T)`.
- Discuss what happens when the condition fails (no V_n exists — parameter set rejected during fitting).

### §5.5 Numerical stability: Q_bg slope floor regularization

- Question: when V_n exists, is the root-find numerically stable?
- Answer: requires `∂Q_bg/∂V_n` to be bounded below by a positive number ε_Q for robust root-find convergence.
- Derivation block B6: regularization condition `∂Q_bg/∂V_n ≥ ε_Q > 0`.
- Smooth-limit analysis: ε_Q → 0 recovers the relaxed condition `∂Q_bg/∂V_n ≥ 0` (monotonic), which is the physically required condition.
- Charter §5 smooth-limit consistency: ε_Q is a solver-side regularization with explicit ε → 0 form (per Charter Addendum 1 §11.4 reporting).

### §5.6 Total capacity consistency

- Derivation block B7: at q = 0 (start of discharge) and q = 1 (end of discharge), V_n takes boundary values V_{n,0} and V_{n,1}. Subtract Eq. 48 at q=1 from Eq. 48 at q=0:
  ```
  Q_cell = Q_bg(V_{n,1}, T) − Q_bg(V_{n,0}, T) + ∫ dμ [ρ(μ; 1, T) − ρ(μ; 0, T)] · n(μ)
  ```
- Physical interpretation: Q_bg drift over the discharge window + total Li transferred through the ρ distribution = total cell capacity.

### §5.7 Monotonicity constraint

- Question: when is dV_n/dq ≥ 0 for an isothermal discharge?
- Derivation block B8: differentiate Eq. 48 with respect to q at fixed T (isothermal) → obtain dV_n/dq expression as a ratio.
- Sign analysis: under monotonicity assumption ∂Q_bg/∂V_n > 0 (§5.5), the sign of dV_n/dq depends on the numerator.
- Derivation block B9: monotonicity constraint
  ```
  ∫ dμ · ∂ρ/∂q · n(μ) ≤ Q_cell
  ```
  (so that the numerator stays non-negative, hence dV_n/dq ≥ 0).
- This is the continuous analogue of the rechecked2 §9 monotonicity constraint `Σ_j Q_{j,tot} dξ_j/dq ≤ Q_cell` — recover this by Dirac-comb limit (§5.8).

### §5.8 Comparison with ver5 and rechecked2

- §5.8.1: rechecked2 Eq. charge_balance (line 121-126) form recovery — set `ρ(μ; q, T) = Σ_j Q_{j,tot} δ(μ − U_j(T))` (Dirac comb), integrate, recover `Q_cell · q = Q_bg(V_n, T) + Σ_j Q_{j,tot} ξ_j`.
- §5.8.2: ver5 explicitly had no central charge balance equation; ver5 §3-§9 treat V_{n,OCV} as external lookup. Show that ver5's structure is a degenerate case where the ρ distribution is replaced by a discrete spectrum but the central conservation is implicit.
- §5.8.3: the new continuous formulation strictly generalizes both: it contains rechecked2 as a Dirac-comb limit and extends ver5 by giving V_n an explicit derivation source.

### §5.9 §6 진입 bridge

- §5 produced Eq. 48 (central equation), V_n existence + stability, capacity consistency, monotonicity.
- §6 will define ρ_eq(μ; q, T) (equilibrium distribution) which is the relaxation target of the Fredholm-2nd-kind ρ-evolution equation (Eq. 49, derived in Phase E7).
- §7 (Phase E6) will define S_R(μ; T) and K_n(μ, μ'; q, T) — the continuous reactivity kernels.

## §11.5 Reporting Plan (this phase)

Phase E4 Result will include §"Writing precision audit" with:

- 9 derivation blocks B1-B9 itemized.
- For each block: starting equation/definition, ending equation, count of intermediate steps shown, count of dimensional checks, count of advanced-concept footnotes.
- §11.4 FAIL/WARN occurrences (target: 0 FAIL, ≤ 2 WARN with resolution).

## Steps (Phase E4, cumulative 261 ~ 340)

(Master roadmap Phase E4 Steps 261-340. Detailed list embedded in body writing.)

261. Save Phase E4 plan as this file — **DONE**.
262. Save companion JSON — **DEFERRED** to Result JSON.
263-340. §5 body writing under §11 standard + audit + commit + push + ledger.

## Test Plan (this phase)

- T-E4-1: `chapter1_v0.1.tex` extended with §5 (9 subsections, +250 ~ +350 lines).
- T-E4-2: 9 derivation blocks B1-B9 all present with full intermediate steps.
- T-E4-3: Dimensional check at start and end of each derivation block (target ≥ 9 each).
- T-E4-4: Smooth-limit analysis for ε_Q included (§5.5).
- T-E4-5: Dirac-comb limit recovery of rechecked2 charge balance form (§5.8.1).
- T-E4-6: §11.4 FAIL = 0, WARN ≤ 2 with resolution noted.
- T-E4-7: Charter §6 Dim #11 Pass 1: 0 FAIL in definitional contexts.
- T-E4-8: Forward references in §3.2, §3.4, §4.1, §4.6 to "§5" or `eq:charge_balance` all resolve to actual §5 content.
- T-E4-9: Result JSON parses.
- T-E4-10: No file in `Claude/_local_only/` or `Codex/` accessed.

## Assumptions

- A-E4-1. Charter Addendum 1 §11 is the binding writing standard from this phase.
- A-E4-2. Eq. 48 is derived from charge conservation (Faraday's law) and decomposition of internal Li occupation into Q_bg + ∫ρ·n dμ — both undergraduate-accessible.
- A-E4-3. Q_bg(V_n, T) functional form is left unspecified in §5; only its monotonicity in V_n and bounded range matter for the §5 derivations.
- A-E4-4. ρ(μ; q, T) functional form is left unspecified in §5; only the integration property matters.
- A-E4-5. n(μ) = 1 default (Charter §3.1) applied throughout §5 derivations; generalization to n(μ) ≠ 1 footnoted.
- A-E4-6. Isothermal default is applied in §5.7 monotonicity analysis; non-isothermal extension footnoted with reference to §11 (Phase E9 C-rate/temperature section).

## Sprint Contract

- [ ] T-E4-1 ~ T-E4-10 all PASS.
- [ ] Audit 11/11 PASS, Dim #11 0 FAIL.
- [ ] §11.4 FAIL = 0, WARN ≤ 2 resolved.
- [ ] Commit + push + ledger Phase E4 row PASS, Gate `PASS_CHARGE_BALANCE_CENTRAL`.
- [ ] Phase E5 entry clear (next cumulative step 341).
