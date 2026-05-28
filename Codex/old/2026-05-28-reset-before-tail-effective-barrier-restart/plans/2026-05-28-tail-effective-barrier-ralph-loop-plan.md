# Tail Effective Barrier Ralph Wiggum Loop Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan. This is a theory-document plan. It must not create solver code or fitting code.

**Goal:** Derive a logically coherent theory for LIB graphite ICA peak-tail behavior in which temperature and present electrode potential modify an effective phase-transition barrier.

**Architecture:** Start from charge balance and internal potential only as much as needed to define the kinetic driving voltage. Then derive effective barrier lowering, transition-rate dependence, charge-coordinate relaxation length, and ICA tail shape. Peak area is explicitly out of the main line and left for later fitting.

**Tech Stack:** LaTeX source, markdown review records, PowerShell static scans.

---

## Summary

The user clarified that the current issue is not peak area. The core issue is the tail of an ICA peak: why low temperature gives a long tail, why high temperature gives a shorter tail, and how the present electrode potential lowers the effective barrier in addition to the temperature-dependent intrinsic barrier.

This plan creates a new document rather than forcing the previous broader Chapter 1 manuscript into the new shape.

## Current Ground Truth

| Item | Status |
|---|---|
| Active project | `D:\Projects\Project_Anode_Fit` |
| New output | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory.tex` |
| Main source equations | corrected ver1 lines 203-266 |
| Existing artifact status | `graphite_ica_chapter1_theory_complete.tex` is scaffold/reference, not final |
| Central phenomenon | low-temperature long tail, high-temperature short tail |
| Central mechanism | `Delta G_eff=Delta G_a(T)-chi_j A_j(V_drive,T)` |

## Phase Range

- Phase 001: scope reset and source extraction — Steps 1-35
- Phase 002: effective-barrier dependency contract — Steps 36-80
- Phase 003: new tail-barrier theory manuscript — Steps 81-155
- Phase 004: Ralph round 1, definition and dependency — Steps 156-210
- Phase 005: Ralph round 2, barrier algebra and temperature logic — Steps 211-270
- Phase 006: Ralph round 3, tail-to-ICA interpretation — Steps 271-330
- Phase 007: convergence and handover — Steps 331-380

## Non-goals

- Do not center peak area.
- Do not estimate peak area.
- Do not perform fitting.
- Do not write fitting code.
- Do not implement a solver.
- Do not claim numerical validation.
- Do not overwrite original source files.
- Do not modify Claude workspace files.

## Planned Artifacts

- `D:\Projects\Project_Anode_Fit\Codex\results\TAIL_BARRIER_SCOPE_REVIEW_2026-05-28.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\TAIL_BARRIER_DEPENDENCY_CONTRACT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\TAIL_BARRIER_RALPH_ROUND_001_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\TAIL_BARRIER_RALPH_ROUND_002_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\TAIL_BARRIER_RALPH_ROUND_003_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\TAIL_BARRIER_FINAL_HANDOVER.md`

## Phase 001 — Scope Reset And Source Extraction

- [ ] **Step 1:** Record user clarification.
- [ ] **Step 2:** Mark previous theory-complete artifact as scaffold/reference only.
- [ ] **Step 3:** Extract corrected ver1 lines 203-266.
- [ ] **Step 4:** Record voltage roles.
- [ ] **Step 5:** Record apparent voltage relation.
- [ ] **Step 6:** Record driving voltage relation.
- [ ] **Step 7:** Record affinity equation.
- [ ] **Step 8:** Record intrinsic barrier equation.
- [ ] **Step 9:** Record effective barrier equation.
- [ ] **Step 10:** Record softplus positive barrier equation.
- [ ] **Step 11:** Record rate equation.
- [ ] **Step 12:** Record state equation lines 268-286 as supporting tail dynamics.
- [ ] **Step 13:** Gate with `PASS_TAIL_SCOPE_RESET`.

## Phase 002 — Effective-Barrier Dependency Contract

- [ ] **Step 36:** Create dependency contract.
- [ ] **Step 37:** Define order: `q -> V_n -> V_app -> V_drive -> A_j -> Delta G_eff -> k_j -> dxi/dq -> tail`.
- [ ] **Step 38:** Require every barrier symbol to be defined before use.
- [ ] **Step 39:** Require intrinsic temperature barrier and potential-assisted barrier to be separated.
- [ ] **Step 40:** Require softplus or positive-part handling if barrier can become negative.
- [ ] **Step 41:** Require derivation of `ell_q=|I|/(Q_cell k_j)`.
- [ ] **Step 42:** Require substitution into `ell_q=|I|/(Q_cell nu) exp(Delta G_eff^+/(RT))`.
- [ ] **Step 43:** Require explanation of low-temperature long tail.
- [ ] **Step 44:** Require explanation of high-temperature short tail.
- [ ] **Step 45:** Require explanation of present potential lowering barrier.
- [ ] **Step 46:** Require ICA tail relation through `dxi/dV`.
- [ ] **Step 47:** Forbid peak area as main topic.
- [ ] **Step 48:** Forbid fitted-result claims.
- [ ] **Step 49:** Gate with `PASS_TAIL_BARRIER_CONTRACT`.

## Phase 003 — New Tail-Barrier Theory Manuscript

- [ ] **Step 81:** Create new LaTeX file from blank target.
- [ ] **Step 82:** Add title focused on tail and effective barrier.
- [ ] **Step 83:** State observed phenomenon.
- [ ] **Step 84:** Define ICA tail target without peak-area emphasis.
- [ ] **Step 85:** Define charge coordinate.
- [ ] **Step 86:** Define charge-balance internal potential.
- [ ] **Step 87:** Define observed/apparent/driving voltage roles.
- [ ] **Step 88:** Define thermodynamic equilibrium target.
- [ ] **Step 89:** Define intrinsic activation barrier.
- [ ] **Step 90:** Define electrode-potential affinity.
- [ ] **Step 91:** Define effective barrier lowering.
- [ ] **Step 92:** Define positive effective barrier.
- [ ] **Step 93:** Define transition rate.
- [ ] **Step 94:** Derive logarithmic sensitivity of rate to driving voltage.
- [ ] **Step 95:** Define charge-domain state equation.
- [ ] **Step 96:** Derive unrelaxed-tail decay equation.
- [ ] **Step 97:** Derive tail relaxation length.
- [ ] **Step 98:** Substitute effective barrier into relaxation length.
- [ ] **Step 99:** Interpret low temperature.
- [ ] **Step 100:** Interpret high temperature.
- [ ] **Step 101:** Interpret current electrode potential state.
- [ ] **Step 102:** Connect tail to ICA derivative.
- [ ] **Step 103:** State what future fitting may use, without fitting.
- [ ] **Step 104:** Run static scans.
- [ ] **Step 105:** Gate with `PASS_TAIL_MANUSCRIPT_INITIAL`.

## Ralph Loop Gates

| Gate | Failure Condition |
|---|---|
| G1 definition | any symbol used before definition |
| G2 dependency | `k_j` introduced before `Delta G_eff` or `V_drive` |
| G3 barrier algebra | wrong sign in `Delta G_eff=Delta G_a-chi A` or rate exponent |
| G4 temperature logic | low/high temperature tail explanation contradicts barrier expression |
| G5 potential logic | present voltage state does not lower barrier or affect rate |
| G6 ICA tail | `dxi/dq` is not connected to `dxi/dV` and ICA tail |
| G7 scope | peak area, fitted values, code, or solver becomes central |

## Test Plan

- static LaTeX scan: labels, refs, brace balance;
- forbidden scope scan: `피크 면적은 왜`, `fitting code`, `solver`, `completed fit`, `parameter values`;
- required equation scan: `Delta G_{a,j}`, `mathcal A_j`, `Delta G_{eff,j}`, `Delta G_{eff,j}^{+}`, `k_j`, `ell_{q,j}`;
- logic scan: low-T, high-T, present potential, barrier lowering, ICA tail.

## Correction History

- 2026-05-28: Created after user clarified that peak area is not the current target and effective barrier lowering by electrode potential is the core.
