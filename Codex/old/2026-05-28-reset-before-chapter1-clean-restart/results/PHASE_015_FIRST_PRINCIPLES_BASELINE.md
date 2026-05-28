# Phase 015 — First-Principles Redo Baseline

## Summary

This phase starts a new execution chain after the invalidation of the prior manuscript. The invalidated manuscript will not be repaired or used as a base. The new Chapter 1 will be written from a first-principles derivation and saved under a new filename.

Gate result: `PASS_REDO_BASELINE`

## Locked Rules

| Rule | Status |
|---|---|
| Do not edit invalidated manuscript | locked |
| Do not copy equations from old TeX files | locked |
| Use old TeX only for chapter structure and formatting style | locked |
| Begin final manuscript with review-paper-like convention section | locked |
| Equation origin must be classified | locked |
| Chapter 1 only: no Chapter 2-5 derivation | locked |

## Equation-Origin Classes

| Class | Meaning |
|---|---|
| `definition` | introduced as a convention or variable definition |
| `calculus/conservation` | follows from calculus, incremental charge balance, or monotonic coordinate definition |
| `thermodynamic work argument` | follows from charge moved through a potential difference or activation free energy |
| `model assumption` | deliberate reduced-order modeling choice |
| `derived` | algebraic consequence of earlier equations in the new derivation |
| `standard kinetic relation` | standard Arrhenius/transition-state style relation, explicitly used as a model relation |

Forbidden class: `copied from old TeX`.

## Final Output Filename

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex`

## Chapter Scope

Chapter 1 completes the basic logic:

```text
conventions
  -> ICA tail observation
  -> minimal variables
  -> equilibrium transformed fraction
  -> finite kinetic lag
  -> potential-assisted barrier lowering
  -> rate
  -> tail length
  -> ICA observable inheritance
```

Chapter 2-5 are roadmap only:

| Chapter | Future role |
|---|---|
| Chapter 2 | reversible heat and values such as `dV/dT` |
| Chapter 3 | electrochemical reaction-kinetic extension |
| Chapter 4 | heat-generation/thermal extension of Chapter 3 |
| Chapter 5 | charge/discharge hysteresis interpretation from Chapter 3 |

## Gate

Gate: `PASS_REDO_BASELINE`

Status: PASS

Reason:

- invalidated output is excluded;
- new output path is fixed;
- review-style convention section is required;
- equation origin policy is established.

## Confirmed Non-Changes

- Invalidated manuscript was not edited in this phase.
- Original source TeX files were not modified.
- Original PDF was not modified.
- Claude folder was not modified.
