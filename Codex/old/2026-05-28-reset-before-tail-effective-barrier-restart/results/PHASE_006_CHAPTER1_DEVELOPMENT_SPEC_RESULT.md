# Phase 006 - Chapter 1 Development Specification Result

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-anode-dqdv-thermodynamic-fit-development-plan.md`

Ledger: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`

Spec: `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md`

Integration Notes: `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_to_chapter5_integration_notes.md`

Date: 2026-05-27

## Summary

Phase 006 converted the audited ver1 logic and Phase 005 method mapping into a Chapter 1 development specification.

Gate result: `PASS_CHAPTER1_SPEC`

Main finding:

- Chapter 1 should own thermodynamic charge balance and internal graphite-potential determination.
- Chapter 1 should state the self-consistent dynamics as a solver-neutral DAE/Volterra formulation.
- Heat, detailed electrochemical kinetics, integrated fitting, and hysteresis should be interfaces to Chapters 2-5 rather than solved inside Chapter 1.
- Historical `ver.1`-`ver.5` labels should be migrated to Chapter 1-5 names, with version-history language kept out of the LaTeX body.

## Step Range

| Planned Steps | Actual Steps | Status |
|---:|---:|---|
| 77-92 | 77-92 | PASS |

## Inputs

| Role | Path | Status |
|---|---|---|
| ver5 structure map | `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md` | used |
| ver1 dependency graph | `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md` | used |
| method mapping | `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md` | used |

## Files Created

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md` | Chapter 1 role, non-role, inputs, unknowns, outputs, logic order, notation rules, and gate |
| `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_to_chapter5_integration_notes.md` | Chapter naming migration and Chapter 1-5 interface contracts |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CHAPTER1_DEVELOPMENT_SPEC_RESULT.md` | This Phase 006 result |

## Chapter 1 Contract

| Contract Item | Decision |
|---|---|
| Role | thermodynamic charge balance and internal potential determination |
| Non-role | full heat, full kinetic interface, global fitting system, hysteresis memory |
| Core input | `Q_ext=Q_cell q`, `T`, `I`, model parameters |
| Core unknown | `V_n` as charge-balance root; `xi_j` as state |
| Core output | `V_n`, `V_app`, `V_OCV`, `xi_j`, rates, ICA/DVA observables, residuals |
| Mathematical class | nonlinear Volterra/DAE with algebraic root |
| Reference method | refs. 6/7-inspired closure pattern for fitting approximation |

## Non-Circular Ordering

The specification fixes the circularity by requiring this order:

```text
measured variables
-> storage/equilibrium functions
-> state variables
-> charge-balance residual
-> root-solve operator V_n = V_root(q,T,xi)
-> equilibrium OCV special case
-> apparent/drive voltage
-> kinetics and state update
-> derivative observables
-> validation gates
```

## Retain / Rewrite / Defer Decisions

| Category | Decision |
|---|---|
| retain | charge balance, implicit OCV, capacity consistency, slope floor, voltage distinctions, state dynamics, ICA/DVA definitions |
| rewrite | any statement that treats `V_n(q,T)` or `V_OCV(q,T)` as an arbitrary prescribed input for dynamic states |
| defer | heat, full BV expansion, global fitting implementation, hysteresis branch memory |

## Notation Decisions

| Notation | Decision |
|---|---|
| `V_n` | solved internal graphite potential |
| `V_OCV` | equilibrium charge-balance root only |
| `Q_ext` | external charge axis for ICA/DVA |
| `Q_bg` | storage term, not cosmetic baseline |
| `w_j` | transition width only |
| `a_j` | dimensionless capacity fraction if needed |
| superscript `ref` | reference closure path |

## Validation

| Check | Result | Evidence |
|---|---|---|
| Chapter 1 role defined | PASS | `chapter1_rewrite_spec.md` |
| Chapter 1 non-role defined | PASS | `chapter1_rewrite_spec.md` |
| input/unknown/output contract defined | PASS | `chapter1_rewrite_spec.md` |
| logic order removes variable-before-solve issue | PASS | non-circular ordering |
| retained/rewritten/deferred equations listed | PASS | `chapter1_rewrite_spec.md` |
| notation collision rules defined | PASS | `chapter1_rewrite_spec.md` |
| historical ver1-5 names mapped to chapters | PASS | `chapter1_to_chapter5_integration_notes.md` |

## Gate

Gate: `PASS_CHAPTER1_SPEC`

Gate conditions:

| Condition | Status |
|---|---|
| clear input/unknown/output contract | PASS |
| non-circular self-consistent formulation | PASS |
| Chapter 1-5 interfaces defined | PASS |
| historical version names converted conceptually to chapters | PASS |
| no body-level change history required | PASS |

## Open Issues / Decision Queue

| ID | Type | Item | Status | Next |
|---|---|---|---|---|
| C1SPEC-ISS-001 | draft | exact LaTeX wording still needs to be written | open | Phase 007 |
| C1SPEC-ISS-002 | build | LaTeX build availability unknown | open | Phase 007 |
| C1SPEC-ISS-003 | visual equation fidelity | PDF-derived equations should not be copied verbatim without visual check | open | Phase 007/manual |

## Next

Proceed to Phase 007 Step 93:

- create a standalone Codex-side Chapter 1 development draft;
- validate the draft against this specification and dependency graph;
- close ledger and handover.
