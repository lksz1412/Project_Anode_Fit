# Phase 014 — Invalidation And First-Principles Restart

## Summary

The Phase 011 manuscript and Phase 012-013 completion framing are invalid as scientific outputs.

Reason: the user required that the Chapter 1 equations be newly derived from the corrected physical picture. Existing `ver1`/`ver5` TeX files were supposed to be used only to infer chapter expansion structure and document format. I incorrectly reused and rearranged equations from those files as if they were source-supported formulas. Because the user has now clarified that the existing formulas are flawed from early stages, this invalidates the prior manuscript as a canonical Chapter 1 deliverable.

Gate result: `INVALIDATED_PRIOR_MANUSCRIPT`

## User Correction To Preserve

The source TeX files may be used only for:

- chapter expansion order;
- document organization style;
- rough formatting conventions;
- identifying which topics were intended to belong in which chapter.

The source TeX files must not be used for:

- copying equations;
- treating old formulas as correct;
- importing old variable dependencies;
- using old algebra as proof;
- preserving old feedback-loop structure unless independently re-derived.

## Correct Chapter Roadmap

The corrected chapter architecture is:

| Chapter | Correct role |
|---|---|
| Chapter 1 | Complete the basic mathematical logic from the user’s large picture: ICA peak tail, temperature barrier, present electrode-potential-assisted effective barrier, and tail behavior. |
| Chapter 2 | Extend Chapter 1 toward reversible heat quantities such as `dV/dT` and related thermodynamic values. |
| Chapter 3 | Extend Chapter 1 by connecting electrochemical reaction-kinetic ideas. |
| Chapter 4 | Extend Chapter 3 with heat-generation/thermal terms. |
| Chapter 5 | Extend Chapter 3 toward charge/discharge hysteresis interpretation. |

## Correct Chapter 1 Starting Picture

Chapter 1 must start from the user’s stated physical target, not from old equations:

- graphite LIB ICA has phase-transition peak tails;
- low temperature gives a longer tail;
- high temperature gives a shorter tail;
- an equilibrium Gaussian-like peak is insufficient;
- thermal activation barrier alone is insufficient;
- present electrode potential state can lower an effective barrier;
- the goal is a theoretical derivation usable later for fitting;
- no solver construction;
- no fitting code;
- no peak-area-centered argument;
- no logical jump;
- undergraduate-level derivation.

## New Derivation Rule

Every equation in the next Chapter 1 attempt must be classified as one of:

| Class | Meaning |
|---|---|
| `first-principles definition` | newly introduced from basic conservation, thermodynamics, kinetics, or calculus |
| `derived in this document` | algebraically follows from earlier equations in the new attempt |
| `external standard relation` | standard physical relation that must be cited or explicitly named |
| `model assumption` | a chosen reduced-order assumption, not copied from prior TeX |

Forbidden class:

| Class | Meaning |
|---|---|
| `copied from old TeX` | not allowed |

## Immediate Status Changes

| Artifact | New status |
|---|---|
| `graphite_ica_tail_effective_barrier_theory_chapter1.tex` | INVALIDATED; header added to prevent canonical reuse |
| `PHASE_011_MANUSCRIPT_DRAFT_RESULT.md` | superseded by this invalidation |
| `PHASE_012_RALPH_WIGGUM_LOGIC_AUDIT.md` | superseded because it audited a wrongly sourced manuscript |
| `PHASE_013_FINAL_HANDOVER.md` | superseded because it packaged the invalid manuscript as current output |

## New Work Direction

The next valid step is not another edit of the invalid manuscript. The next valid step is a first-principles Chapter 1 derivation plan with a hard equation-origin ledger:

```text
physical observation
  -> minimal variables chosen from scratch
  -> conservation/coordinate definitions derived from scratch
  -> equilibrium target definition justified from thermodynamics
  -> kinetic lag model stated as new model assumption
  -> effective barrier form derived or explicitly assumed from work-lowering logic
  -> tail equation derived algebraically
  -> ICA observable relation derived from newly defined variables
  -> Ralph Wiggum audit checks every equation origin
```

## Gate

Gate: `INVALIDATED_PRIOR_MANUSCRIPT`

Status: PASS

Reason:

- the invalid manuscript is marked as non-canonical;
- the user’s corrected chapter roadmap is recorded;
- the future equation-origin rule prevents reuse of old TeX formulas as proof.

## Confirmed Non-Changes

- Original source `.tex` files were not modified.
- Original PDF was not modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.
