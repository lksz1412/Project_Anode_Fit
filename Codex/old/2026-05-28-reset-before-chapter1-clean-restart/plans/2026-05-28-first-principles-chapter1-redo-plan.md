# First-Principles Chapter 1 Redo Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan inline. Do not use prior TeX equations. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a new Chapter 1 final `.tex` manuscript that derives the ICA tail/effective-barrier logic from first principles and the user's physical picture, without copying or preserving equations from prior `ver1`/`ver5` TeX sources.

**Architecture:** Prior TeX files may guide only chapter expansion order and formatting style. Equations must be created anew and tracked in an equation-origin ledger as definitions, conservation laws, thermodynamic work arguments, explicit model assumptions, or algebraic consequences. The final manuscript is a new file, not a modification of the invalidated manuscript.

**Tech Stack:** LaTeX manuscript, Markdown plan/result/ledger files, PowerShell/Python static checks.

---

## User Correction Locked As Ground Truth

- Do not repair the invalidated manuscript.
- Do not reuse equations from prior `ver1`/`ver5` TeX files.
- Existing TeX files are unreliable in their formulas from early stages.
- Existing TeX files may be used only to understand chapter expansion stages and writing/format style.
- Chapter 1 must complete the basic mathematical logic from the user's large picture:
  - graphite ICA peak tail;
  - temperature barrier;
  - present electrode-potential-assisted effective barrier;
  - tail behavior;
  - review-paper-like convention summary at the start of the chapter;
  - no fitting code;
  - no solver construction;
  - no peak-area-centered argument;
  - no logical leaps;
  - undergraduate-followable derivation.
- Chapter 2 later extends Chapter 1 to reversible heat and quantities such as `dV/dT`.
- Chapter 3 later connects Chapter 1 to electrochemical reaction-kinetic ideas.
- Chapter 4 later extends Chapter 3 with heat-generation/thermal terms.
- Chapter 5 later extends Chapter 3 toward charge/discharge hysteresis interpretation.

## Current Ground Truth

| Item | State |
|---|---|
| Active project | `D:\Projects\Project_Anode_Fit` |
| Active Codex workspace | `D:\Projects\Project_Anode_Fit\Codex` |
| Plans directory | `D:\Projects\Project_Anode_Fit\Codex\plans` |
| Results directory | `D:\Projects\Project_Anode_Fit\Codex\results` |
| Prior manuscript | invalidated; do not edit or reuse |
| Claude folder | do not modify |
| Original source folder | read-only; do not modify |

## Phase Range

| Phase | Name | Step range | Primary output | Gate |
|---|---|---:|---|---|
| Phase 015 | Redo Baseline And Equation Policy | 1-12 | `PHASE_015_FIRST_PRINCIPLES_BASELINE.md` | old equations banned, new outputs named |
| Phase 016 | First-Principles Skeleton Derivation | 13-40 | `PHASE_016_FIRST_PRINCIPLES_DERIVATION.md` | every core equation has new origin class |
| Phase 017 | Equation-Origin Logic Audit | 41-70 | `PHASE_017_EQUATION_ORIGIN_AUDIT.md` | no copied old equation class; no circular gap |
| Phase 018 | Final Chapter 1 Manuscript | 71-95 | `graphite_ica_chapter1_first_principles_final.tex` | final TeX created from audited derivation |
| Phase 019 | Final Verification And Handover | 96-112 | `PHASE_019_FIRST_PRINCIPLES_FINAL_HANDOVER.md` | static checks and recovery instructions recorded |

Phase and step counts are minimum coverage. Add repair steps if the logic fails, but do not revive the invalidated manuscript.

## Non-Goals

- Do not modify the invalidated manuscript.
- Do not copy equations from the old TeX files.
- Do not cite old TeX line numbers as formula authority.
- Do not build a solver.
- Do not write fitting code.
- Do not center the derivation on peak area.
- Do not move into Chapter 2 reversible heat, Chapter 3 electrochemical kinetics, Chapter 4 heat generation, or Chapter 5 hysteresis except as roadmap notes.

## Implementation Changes

### Create

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-first-principles-chapter1-redo-plan.md` | canonical redo plan |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_019_FIRST_PRINCIPLES_LEDGER.md` | new execution ledger, separate from invalidated chain |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_FIRST_PRINCIPLES_BASELINE.md` | restart baseline and equation policy |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_016_FIRST_PRINCIPLES_DERIVATION.md` | derivation note with equation origins |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_EQUATION_ORIGIN_AUDIT.md` | no-copy and logic audit |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex` | final Chapter 1 manuscript |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_FIRST_PRINCIPLES_FINAL_HANDOVER.md` | final handover |

### Preserve

| Path | Rule |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory_chapter1.tex` | invalidated record; do not edit |
| original source folder | read-only |
| `D:\Projects\Project_Anode_Fit\Claude` | do not modify |

## Phase 015 — Redo Baseline And Equation Policy

- [ ] Step 1: Record that prior manuscript is invalid and must not be edited.
- [ ] Step 2: Record that old TeX equations are banned as equation sources.
- [ ] Step 3: Record allowed use of old TeX: chapter structure and formatting only.
- [ ] Step 4: Create the new ledger.
- [ ] Step 5: Define equation-origin classes.
- [ ] Step 6: Define the final output filename.
- [ ] Step 7: Define Chapter 1 scope and Chapter 2-5 roadmap.
- [ ] Step 8: Create `PHASE_015_FIRST_PRINCIPLES_BASELINE.md`.
- [ ] Step 9: Gate `PASS_REDO_BASELINE`.
- [ ] Step 10: Do not modify the invalidated manuscript.
- [ ] Step 11: Do not modify source files.
- [ ] Step 12: Proceed directly to Phase 016.

## Phase 016 — First-Principles Skeleton Derivation

- [ ] Step 13: Define the observation and required explanatory target.
- [ ] Step 14: Write the beginning convention block: electrode-potential convention, current/scan direction, ICA/DVA definitions, negative-electrode vs full-cell scope, tail direction, sign of barrier-lowering work, and units.
- [ ] Step 15: Choose minimal variables from scratch.
- [ ] Step 16: Define a one-dimensional scan coordinate `x` independent of old notation.
- [ ] Step 17: Define ICA observable from calculus: `I_ICA=dQ/dV`.
- [ ] Step 18: Define a smooth equilibrium transformed fraction `theta_eq(phi,T)` as a thermodynamic state function, not a copied formula.
- [ ] Step 19: Define actual transformed fraction `theta(x)`.
- [ ] Step 20: State lag as `r=theta_eq-theta`.
- [ ] Step 21: Introduce finite relaxation as a first-order minimal model assumption.
- [ ] Step 22: Convert relaxation from time to scan coordinate using a scan speed.
- [ ] Step 23: Derive residual equation with forcing from moving equilibrium target.
- [ ] Step 24: Derive post-peak tail approximation when the equilibrium target stops moving strongly.
- [ ] Step 25: Derive local tail length as scan speed divided by rate.
- [ ] Step 26: Introduce intrinsic activation free energy from thermodynamics.
- [ ] Step 27: Derive potential work term from charge moved through potential difference.
- [ ] Step 28: Define effective barrier as intrinsic barrier minus assisting work fraction.
- [ ] Step 29: Define bounded positive barrier as a model regularization.
- [ ] Step 30: Define rate from activation barrier as a model assumption.
- [ ] Step 31: Substitute rate into tail length.
- [ ] Step 32: Derive low-T long-tail condition.
- [ ] Step 33: Derive high-T short-tail condition.
- [ ] Step 34: Derive present-potential tail-shortening condition.
- [ ] Step 35: Define how the phase fraction changes stored charge and potential slope.
- [ ] Step 36: Derive ICA tail inheritance through `dQ/dV`.
- [ ] Step 37: List assumptions and validity limits.
- [ ] Step 38: Build equation-origin table.
- [ ] Step 39: Create `PHASE_016_FIRST_PRINCIPLES_DERIVATION.md`.
- [ ] Step 40: Gate `PASS_FIRST_PRINCIPLES_DERIVATION`.
- [ ] Step 40a: Proceed directly to Phase 017.

## Phase 017 — Equation-Origin Logic Audit

- [ ] Step 41: Check every equation has an origin class.
- [ ] Step 42: Check no origin class is copied old TeX.
- [ ] Step 43: Check units for potential work and barrier.
- [ ] Step 44: Check sign of assisting potential.
- [ ] Step 45: Check residual-tail algebra.
- [ ] Step 46: Check low-T/high-T claims are conditional on rate.
- [ ] Step 47: Check present-potential effect does not double-count equilibrium location.
- [ ] Step 48: Check ICA mapping does not require peak-area argument.
- [ ] Step 49: Check no solver/fitting implementation entered.
- [ ] Step 50: If a gap exists, repair derivation note before manuscript.
- [ ] Step 51: Create `PHASE_017_EQUATION_ORIGIN_AUDIT.md`.
- [ ] Step 52: Gate `PASS_EQUATION_ORIGIN_AUDIT`.
- [ ] Step 53: Do not edit invalid manuscript.
- [ ] Step 54: Proceed to Phase 018.

## Phase 018 — Final Chapter 1 Manuscript

- [ ] Step 71: Write a new `.tex` file with no reference to invalidated manuscript.
- [ ] Step 72: Include title, abstract, and a review-paper-like convention section before the main derivation.
- [ ] Step 73: Keep equation-origin labels out of final manuscript body unless needed as explanatory prose.
- [ ] Step 74: Include Chapter 2-5 roadmap only as final scope note.
- [ ] Step 75: Keep all work-history terms out of manuscript body.
- [ ] Step 76: Run static checks for braces, labels, and equation references.
- [ ] Step 77: Search for forbidden phrases and copied-old-equation markers.
- [ ] Step 78: Record hash and line count.
- [ ] Step 79: Gate `PASS_FINAL_TEX_CREATED`.

## Phase 019 — Final Verification And Handover

- [ ] Step 96: Re-run static checks.
- [ ] Step 97: Check TeX engine availability.
- [ ] Step 98: Record inability to compile PDF if engines are unavailable.
- [ ] Step 99: Record all created files.
- [ ] Step 100: Record no source/Claude modifications.
- [ ] Step 101: Create final handover.
- [ ] Step 102: Update ledger.
- [ ] Step 103: Gate `PASS_FIRST_PRINCIPLES_FINAL_HANDOVER`.

## Test Plan

- Static TeX brace balance via Python.
- Label/ref consistency via Python regex.
- Forbidden manuscript hygiene search via `rg`.
- Equation-origin audit table with no copied-old class.
- Git status with safe-directory override.
- TeX engine availability check.

## Assumptions

- A first-order relaxation law is a deliberately chosen minimal kinetic model, not copied from old TeX.
- A potential work term proportional to charge times potential difference is a basic electrostatic work argument.
- The exact microscopic reaction coordinate is not solved in Chapter 1; Chapter 1 builds the reduced theoretical background for later fitting.

## Correction History

- This plan supersedes the invalidated Phase 011-013 chain.
