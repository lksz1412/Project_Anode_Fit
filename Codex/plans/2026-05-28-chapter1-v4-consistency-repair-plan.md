# Chapter 1 v4 Consistency Repair Plan

Date: 2026-05-28

## Summary

This repair plan fixes the problems found in Phase 014 without overwriting prior artifacts. The target artifact is a new Chapter 1 candidate:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex`

The repair keeps the manuscript-facing structure of v3, but restores the derivation consistency and explicit logic required by the user:

- LIB graphite anode ICA peak tail is the target phenomenon.
- Low temperature gives a longer post-peak tail; high temperature gives a shorter tail.
- Activation free-energy barrier is retained as a rate-determining quantity.
- A step-function or sudden `0 -> 1` completion model is forbidden.
- Electrode potential assistance smoothly lowers the effective barrier and shifts the relaxation-length spectrum.
- The manuscript remains theory/logic only, not a solver or fitting implementation.
- Korean prose is used, but academic terms remain in English.
- Undergraduate-followable derivation blocks must be present where logical gaps would otherwise occur.

## Current Ground Truth

- v3 is the active manuscript shell.
- Phase 014 found coordinate drift (`q` versus `Q`), state symbol drift (`theta` versus `xi`), derivation compression, external-only AL tags, and a later fitting section that leaned too strongly toward Plan A.
- The repair chooses normalized charge coordinate `q` as the primary coordinate.
- Dimensional charge coordinate `Q_ext` is retained only through explicit conversion:
  `L_Q = v_Q/k = Q_cell L_q`, `L_q = v_q/k = |I|/(Q_cell k)`.

## Phase Range

## Phase 015 — v4 consistency repair

Steps:

1. Create a new v4 artifact from v3 without overwriting v2 or v3.
2. Repair notation and coordinate consistency: `theta`, `q`, `L_q` are primary; `L_Q` is conversion-only.
3. Reinsert compact derivation blocks for lattice-gas target, charge-balance differential form, and forward/back rate relaxation.
4. Add a compact Assumption Ledger inside the `.tex` body.
5. Reframe Plan B as the always-available theoretical baseline and Plan A as a candidate analytic compression only after validation.
6. Run static LaTeX consistency checks and targeted content checks.
7. Save Phase 015 result/ledger/handover records.

## Non-goals

- Do not build a numerical solver.
- Do not implement fitting code.
- Do not claim Plan A/Fredholm closure is established before validation.
- Do not overwrite v2, v3, Claude outputs, original downloaded `.tex`, or user PDF files.
- Do not put phase history or audit metadata inside the manuscript body.

## Test Plan

- Check `\begin`/`\end` balance.
- Check brace balance.
- Check missing `\ref` labels and missing `\cite` bibitems.
- Search for forbidden or risky remnants: `\xi`, ambiguous `L=v_Q/k`, dimensional Plan B tail in `Q`, and implementation-colored fallback wording.
- Full-read the generated v4 file in recorded chunks before reporting.

## Assumptions

- `xelatex` is not available on PATH; PDF generation is outside this phase unless a TeX distribution is installed later.
- The repair is a consistency repair of v3, not a new scientific literature expansion.

## Correction History

- Supersedes neither v2 nor v3. v4 is a new candidate artifact created because Phase 014 identified repairable consistency defects in v3.
