# Phase 007 Anode dQ/dV Handover

Project: `D:\Projects\Project_Anode_Fit`

Active Codex workspace:
`D:\Projects\Project_Anode_Fit\Codex`

Date: 2026-05-27

## Recovery Start Point

Start by reading these files in order:

1. `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`
2. `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-anode-dqdv-thermodynamic-fit-development-plan.md`
3. `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_DRAFT_VALIDATION_HANDOVER_RESULT.md`
4. `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex`

## Current State

Phases 001-007 were completed with `PASS_DRAFT_HANDOVER`, with one build limitation:

- no local LaTeX engine was found (`pdflatex`, `xelatex`, `lualatex` unavailable);
- targeted LaTeX checks passed, but no PDF was built.

## Primary Created Artifacts

| Artifact | Purpose |
|---|---|
| `ver5_chapter_structure_map.md` | Chapter 1-5 structure inferred from merged ver5 |
| `ver1_charge_balance_dependency_graph.md` | corrected ver1 variable/dependency and feedback audit |
| `ref6_ref7_method_notes.md` | user's JCP paper refs. 6/7 method extraction |
| `self_consistent_variable_mapping.md` | mapping refs. 6/7 closure pattern to graphite feedback |
| `chapter1_rewrite_spec.md` | Chapter 1 development specification |
| `chapter1_to_chapter5_integration_notes.md` | Chapter stack and interface notes |
| `graphite_ica_chapter1_development_draft.tex` | standalone Chapter 1 draft |

## Core Technical Decision

The corrected Chapter 1 should be built around:

```text
Q_cell q = Q_bg(V_n,T) + sum_j Q_j,tot xi_j
```

`V_n` is solved as a root of charge balance. It is not a prescribed OCV input.

The feedback loop is:

```text
xi_j -> charge balance -> V_n -> xi_eq/k_j -> dxi_j/dq or dxi_j/dt -> xi_j
```

This is classified as a charge-balance-constrained nonlinear Volterra/DAE system.

Refs. 6/7 are used only as a mathematical closure pattern:

```text
self-consistent integral form
-> isolate feedback ratio/correction
-> close using a simpler reference solution
-> validate against direct numerical solution
```

Do not import the geminate-pair physical model into LIB graphite.

## Confirmed Source Coverage

| Source | Coverage |
|---|---|
| `graphite_ica_dynamic_ver5.tex` | READ_FULL lines 1-1974 |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | READ_FULL lines 1-495 |
| JCP 147, 144111 (2017) PDF | READ_FULL_TEXT pages 1-10 via `pypdf` |

## Open Issues

| Issue | Next Action |
|---|---|
| LaTeX build unavailable | install/provide TeX engine or build elsewhere |
| exact PDF equation glyphs not visually verified | visually inspect pages 5 and relevant equations before copying exact formulas from the paper |
| full refs. 6/7 papers not read | retrieve only if deeper derivation is needed |
| numerical solver not implemented | build direct DAE/root-solve benchmark as next technical phase |

## Guardrails

- Do not overwrite the original `.tex` sources in the source folder.
- Do not edit `D:\Projects\Project_Anode_Fit\Claude`.
- Do not put version-history/change-history notes into LaTeX body text.
- Keep `Q_ext=Q_cell q` as the ICA/DVA charge axis.
- Keep `V_n`, `V_{n,\app}`, and `V_{n,\drive}` distinct.
- Keep charge-balance residual checks active before later heat/kinetic/hysteresis fitting.
