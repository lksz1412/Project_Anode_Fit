# Rebuild v2 Phase 003 Failure Analysis Result

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 003 - Failure Analysis And Salvage/Reject Inventory`

Date: 2026-05-27

Gate: `PASS_REBUILD_V2_FAILURE_ANALYSIS`

## Scope

Phase 003 classified prior artifacts and major ideas into retain, rewrite, reject, and defer categories. It also confirmed that the previous draft is not a manuscript base. This phase did not create final manuscript prose.

## Draft Read Coverage

| File | Coverage | Line Count | Status |
|---|---:|---:|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex` | lines 1-375 | 375 | READ_FULL for Phase 003 reference-only classification |

## Step Execution

| Step | Planned Action | Status | Evidence |
|---:|---|---|---|
| 51 | Open previous draft as reference-only sketch. | DONE | Draft opened under reference-only boundary. |
| 52 | Read draft line 1 to end and record coverage. | DONE | Lines 1-375 read and recorded. |
| 53 | Identify technically correct reusable ideas. | DONE | Charge coordinate, root operator, voltage distinctions, self-consistent dynamics, derivatives, validation gates retained as ideas. |
| 54 | Identify skeletal draft elements. | DONE | Purpose, closure strategy, validation gates, and interfaces marked for expansion. |
| 55 | Identify scaffolding prose not to reuse. | DONE | Draft labels, process wording, and prior body prose rejected. |
| 56 | Identify old ver5 Chapter 1 ideas superseded by corrected ver1. | DONE | Old primary OCV/input logic rejected or rewritten. |
| 57 | Identify old ver5 Chapter 2 heat context. | DONE | Heat layer kept only as downstream interface. |
| 58 | Identify old ver5 Chapter 3 kinetic context. | DONE | Kinetic layer kept only as downstream interface. |
| 59 | Identify old ver5 Chapter 4 fitting context. | DONE | Fitting layer kept only as system-interface context. |
| 60 | Identify old ver5 Chapter 5 hysteresis context. | DONE | Hysteresis kept as future controlled extension. |
| 61 | Identify corrected ver1 equations to retain. | DONE | Charge balance, root operator, derived OCV, dynamics, derivative observables retained as ideas. |
| 62 | Identify corrected ver1 equations needing dependency-order rewrite. | DONE | Occupancy, root solve, dynamics, derivative expressions assigned to Phase 005-008 rewrites. |
| 63 | Identify statements risking prescribed `V_n`. | DONE | Old OCV-primary logic and any pre-root rate use rejected. |
| 64 | Identify correct voltage distinctions. | DONE | `V_n`, `V_{n,app}`, and `V_{n,drive}` distinction retained. |
| 65 | Identify correct `Q_ext` use. | DONE | `Q_ext=Q_cell q` retained as measurement coordinate. |
| 66 | Identify `Q_bg` storage requirement. | DONE | `Q_bg` must be storage term, not cosmetic baseline. |
| 67 | Identify symbol-collision risks. | DONE | `w_j`, `Q_ext`, voltage roles, `R_n`, `q`, and sign conventions listed. |
| 68 | Identify refs. 6/7 physical-overreach risks. | DONE | Molecular-pair physics and exact derivation overclaims listed. |
| 69 | Create salvage/reject inventory. | DONE | `REBUILD_V2_SALVAGE_REJECT_INVENTORY.md` created. |
| 70 | Include required inventory columns. | DONE | Columns include `Source`, `Item`, `Use As-Is?`, `Reuse As Idea?`, `Reject?`, `Reason`, `Required Rewrite`. |
| 71 | Add retain/rewrite/reject/defer categories. | DONE | `Category` column and sections added. |
| 72 | Add "must not appear" section. | DONE | Section added. |
| 73 | Add "requires user decision" section. | DONE | Section added. |
| 74 | Add "requires numerical validation" section. | DONE | Section added. |
| 75 | Add "requires full refs. 6/7 read" section. | DONE | Section added. |
| 76 | Save Phase 003 result. | DONE | This file saved. |
| 77 | Update execution ledger. | DONE | `REBUILD_V2_EXECUTION_LEDGER.md` updated after this result. |
| 78 | Gate Phase 003 with `PASS_REBUILD_V2_FAILURE_ANALYSIS`. | PASS | Every prior artifact and major idea is classified. |
| 79 | Stop if inventory uses old draft as manuscript base. | NOT TRIGGERED | Inventory explicitly rejects this. |
| 80 | Stop if old `V_OCV(q,T)` logic survives as primary dynamic input. | NOT TRIGGERED | Inventory rejects primary OCV-input logic. |
| 81 | Stop if rejected item remains planned for direct insertion. | NOT TRIGGERED | Rejected items have replacement/destination controls. |
| 82 | Stop if required rewrite has no destination phase. | NOT TRIGGERED | Rewrite/defer rows specify destination phases or conditions. |
| 83 | Proceed only if blank rewrite is feasible. | PASS | Blank rewrite is feasible after Phase 004-010 contracts. |
| 84 | Record next phase entry condition in ledger. | DONE | Ledger next step set to Phase 004 Step 85. |

## Main Findings

### What Is Good Enough To Keep As Ideas

- The corrected charge-balance root definition for `V_n`.
- The measurement-first ordering through `Q_ext=Q_cell q`.
- The distinction between internal, apparent, and driving voltages.
- The self-consistent dynamics/integral form as the formal problem class.
- The derivative observable sequence after the state/root definitions.
- The idea that refs. 6/7 motivate a reference/correction closure pattern.
- The chapter-interface direction from ver5, provided it remains downstream.

### What Is Insufficient

- The previous Chapter 1 draft is too skeletal and process-like for final manuscript use.
- The reference-closure section is schematic and cannot yet stand as a formal method.
- Validation gates are currently protocol requirements, not completed validation results.
- Later chapter interfaces are only boundaries, not developed models.
- Full refs. 6/7 original-paper readings are not yet available.

### What Is Wrong Or Must Be Prevented

- Treating `V_n` or `V_{n,OCV}(q,T)` as a prescribed primary dynamic input.
- Copying old ver5 or previous draft prose into the final manuscript.
- Collapsing `V_n`, `V_{n,app}`, and `V_{n,drive}`.
- Letting both `R_n` and kinetic prefactors freely absorb dynamic voltage shifts.
- Importing molecular-pair physical assumptions from refs. 6/7 into graphite staging.
- Claiming numerical validation or fitting performance before any solver/data phase.

### How To Resolve The Problems

- Phase 004 should lock manuscript scope and architecture.
- Phase 005 should lock notation and the equation dependency DAG.
- Phase 006 should build the Chapter 1 mathematical foundation from corrected ver1.
- Phase 007 should formalize the refs. 6/7 closure pattern with full caution about portability.
- Phase 008 should define direct solver and validation protocol.
- Phase 009 should define fitting and identifiability controls.
- Phase 010 should constrain Chapter 2-5 interfaces before any LaTeX assembly.

## Gate Check

| Gate Item | Result |
|---|---|
| Prior draft fully read for Phase 003 | PASS |
| Prior artifacts classified | PASS |
| Retain/rewrite/reject/defer categories present | PASS |
| Old draft rejected as manuscript base | PASS |
| Old primary OCV-input logic rejected | PASS |
| Symbol-collision risks recorded | PASS |
| Physical-overreach risks recorded | PASS |
| User-decision items recorded | PASS |
| Numerical-validation blockers recorded | PASS |
| Full refs. 6/7 read blockers recorded | PASS |

Gate result: `PASS_REBUILD_V2_FAILURE_ANALYSIS`

## Files Created Or Updated

| File | Action |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_SALVAGE_REJECT_INVENTORY.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_003_FAILURE_ANALYSIS_RESULT.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EXECUTION_LEDGER.md` | updated |

## Next Phase Entry Condition

Proceed to Phase 004 Step 85 only if the next work remains architecture-contract work. Manuscript drafting is still blocked until Phase 004-010 produce the required contracts.
