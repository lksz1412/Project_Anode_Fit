# Phase E1 — Spine Redesign And Core Variable Selection (Phase-Level Plan)

## Summary

- Status: `READY_FOR_EXECUTION` → executed in same turn as user GO 2026-05-27
- Parent roadmap: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
- Phase Range: cumulative Steps **81 ~ 140** (60 steps)
- Scope: Lock down the new Chapter 1 spine explicitly, classify all self-consistent loops, identify the Ref. 6/7 application target loop, and sketch the transfer-to-Chapter-2 equation set in continuous form.
- No LaTeX body writing (Phase E2 onward).
- Charter (Phase E0 §1-§9) is the foundational input — every spine equation and variable must be Charter-compliant.

## Current Ground Truth

- Phase E0 closed PASS-with-note at commit `a443682`.
- Charter `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md` §3.2 already preview-defined Eq. 48 (charge balance) and Eq. 49 (Fredholm 2nd kind ρ evolution) + apparent potential + dQ/dV. Phase E1 makes these the explicit spine with full dependency chain.
- Audit Dim #11 (`feedback_phase_audit_workflow` extension) is operational, project-local.
- Ref 6 DOI `10.1063/1.3565476` + Ref 7 DOI `10.1063/1.4802584` confirmed; no further self-search needed.

## Non-goals (this phase)

- Do not write `.tex` sections (Phase E2 onwards).
- Do not finalize the unit reconciliation of Eq. 49's `K_n × S_R` joint dimension (OI-E0-1, deferred to Phase E6).
- Do not define the specific functional form of `S_R(μ; T)` or `K_n(μ, μ'; q, T)` — Phase E6 work.
- Do not enter Phase E2 in this phase.
- Do not modify Charter; corrections go to Charter Addendum.
- Do not request user clarification mid-phase; Phase F3 is the canonical user review.

## Implementation Changes

Planned new files:

- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e1-spine-plan.md` (this file)
- `Claude/results/PHASE_E1_spine_redesign_RESULT.md` (★ spine document — 6 sections §A-§F)
- `Claude/results/PHASE_E1_spine_redesign_RESULT.json` (machine-readable spine — variable inventory, equation labels, loop classification)

Ledger update only (no new ledger file):
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` Phase E1 row updated from `(pending)` to `PASS`

No file in `Claude/docs/`, `Claude/_local_only/`, or `Codex/` accessed.

## Steps (Phase E1, cumulative 81 ~ 140)

(Master roadmap Phase E1 Steps 81-140 verbatim, with execution notes.)

81. Save Phase E1 plan as this file — **DONE by writing this file**.
82. Save companion JSON for Phase E1 plan — **DEFERRED**: consolidated into Result JSON (Step 102) per Phase E0 §"compactness" precedent.
83. Load Phase E0 Charter into Phase E1 context.
84. List ver5 Ch1 spine equation (line 66-79, Eq. main_spine) — for §A comparison.
85. List ver1_rechecked2 spine (line 51-61) — for §A comparison.
86-89. Draft spine candidates A and B, evaluate against Charter anti-pattern list, select candidate B (with explicit ICA/DVA derivation appended).
90. Write the new spine explicitly with all five components (Eq. 48, Eq. 49, V_n implicit relation, V_{n,app}, dQ/dV) — Result §A.
91. List every variable, tag canonical vs derived — Result §B + §C.
92-93. Write 1-line definitions / derivations — Result §B + §C.
94. Audit Dim #11 Pass 1 on spine equations — Result §"Validation".
95-97. Identify self-consistent loops, recognize Loop C = JCP 2017 Eq. (32) mapping, plan Ref. 6/7 application — Result §D.
98-99. Draft transfer-to-Ch2 equation form + flag Chapter 2-5 follow-up — Result §E.
100. Define legacy ↔ new variable cross-reference — Result §F (extends Charter §7).
101-102. Draft Result outline + JSON.
103-108. Gates `GATE_E1_1` ~ `GATE_E1_6` — Result §"Validation".
109-110. Stop conditions.
111-113. Confirmation rules.
114-128. Write Result + JSON + dimensional/smooth-limit checks + cross-checks against Phase A grep + Phase B variable dependency table + JCP 2017 §II.A/II.C structural correspondence.
129. Identify DQ items (μ semantics — DQ-G2 propagated, no new DQ).
130. Plan DQ items don't block Phase E2.
131. Phase E2 entry condition: this Phase E1 PASS.
132-136. Stage + commit + push + confirm.
137. Mark Phase E1 row PASS with Gate `PASS_SPINE_REDESIGN`.
138. Record next-step entry for Phase E2 (cumulative step 141).
139. Confirm no DQ-G1 blocker — user GO active.
140. End Phase E1 at documented boundary.

## Test Plan (this phase)

- T-E1-1: Spine §A contains all 5 components (Eq. 48, Eq. 49, V_n implicit, V_{n,app}, dQ/dV).
- T-E1-2: Canonical variables list ≥ 12 entries with 1-line definitions (Gate `GATE_E1_2`).
- T-E1-3: Derived variables list maps every ver5 Ch1 §2 entry (21) and rechecked2 §2 entry (11) (Gate `GATE_E1_3`).
- T-E1-4: Self-consistent loops ≥ 3 classified with explicit position in spine + Ref 6/7 target (Gate `GATE_E1_4`).
- T-E1-5: Transfer-to-Ch2 lists continuous-form quantities; ξ_j-based transfer absent (Gate `GATE_E1_5`).
- T-E1-6: Audit 11/11 dims PASS Dim #11 0 FAIL (Gate `GATE_E1_6`).
- T-E1-7: Result JSON parses (`python -m json.tool`).
- T-E1-8: Smooth-limit check: spine reduces to rechecked2 spine under `ρ → Σ_j Q_{j,tot} δ(μ - U_j)` (master roadmap T3).
- T-E1-9: Structural correspondence: spine Eq. 49 ↔ JCP 2017 Eq. (32) via the documented mapping.
- T-E1-10: No file in `Claude/docs/`, `_local_only/`, `Codex/` accessed.

## Assumptions

- A-E1-1. Charter §3.2 Eq. 48, 49 are the canonical preview; Phase E1 formalizes them as spine, no fundamental redesign.
- A-E1-2. Candidate B (with ICA/DVA derivation appended) is selected over candidate A based on completeness; this is a documentation choice, not a model choice.
- A-E1-3. Loop C (Volterra-like time-integral form) is the load-bearing target for Ref. 6/7 ratio-substitution; Loops A and B are standard DAE numerics solvable by independent methods.
- A-E1-4. `μ` interpretation as Li/Li⁺-reference electrochemical potential is inherited from Charter §3.1; subject to DQ-G2 user cross-check at Phase F3.
- A-E1-5. Unit reconciliation deferral (OI-E0-1) is acceptable since spine structure is invariant under unit choice of `K_n` and `S_R`.

## Decision Queue (this phase)

- (No new DQ items.) Existing DQ-G1 (user GO) active, DQ-G2 (μ semantics) propagated to Phase F3, OI-E0-1 (unit reconciliation) propagated to Phase E6.

## Sprint Contract

- [ ] T-E1-1 ~ T-E1-10 all PASS.
- [ ] Gates `GATE_E1_1` ~ `GATE_E1_6` all PASS.
- [ ] Commit + push + ledger Phase E1 row PASS, Gate `PASS_SPINE_REDESIGN`.
- [ ] Phase E2 entry clear (next cumulative step 141).
