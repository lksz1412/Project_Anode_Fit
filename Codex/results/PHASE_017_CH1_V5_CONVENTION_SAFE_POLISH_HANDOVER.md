# Phase 017 Handover — Chapter 1 v5 Convention-Safe Polish

## Handover Chain

1. Phase 015: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_CH1_V4_CONSISTENCY_REPAIR_RESULT.md`
   - Produced v4 consistency-repaired candidate.
2. Phase 016: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_016_CH1_V4_V3_COMPARISON.md`
   - Compared v4 against v3 and recommended v4 as current candidate.
3. Phase 017: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_RESULT.md`
   - Produced v5 convention-safe polish candidate.

## Current Canonical Candidate

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex`

SHA256:

`9E5DCCE75CB650251FAAA7741591B1D23B89632545BAFF157EB5798E53E690F1`

## What Changed in v5

- `DQ-v3-1/2` labels were replaced with `VG-1/2`.
- `K_\lambda` schematic shorthand was replaced with the explicit exponential kernel integral.
- `Grounding 감사 (AGP self-check)` was rewritten as `Assumption and validation status`.
- `Codex`, `AGP`, `2026-05-28`, audit-style `통과`, and standalone `DQ` status markers were removed from the manuscript body.

## What Must Be Preserved

- Korean prose with English academic terms.
- Activation barrier remains part of the theory.
- No step-function / `0 -> 1` jump.
- Electrode potential lowers the effective barrier smoothly.
- `q` remains the primary coordinate.
- `L_q` remains the normalized relaxation-length coordinate.
- `L_Q` is only dimensional conversion.
- Plan B remains the conservative theoretical baseline.
- Plan A remains a gated candidate analytic compression until Refs 6/7 audit and Fredholm/Volterra mapping are confirmed.

## Verified

- v5 lines 1-858 were read in chunks after generation.
- Static LaTeX counts passed:
  - `\begin`/`\end`: `52/52`
  - braces: `750/750`
  - missing refs: 0
  - missing cites: 0
- Targeted high-risk patterns all returned count 0:
  - `\xi`
  - `L=v_Q/k`
  - `$L(G)$`
  - `large-$L$`
  - `short-$L$`
  - `\frac{\dd r_j}{\dd Q}`
  - `Q_{a,j}`
  - `\Theta(Q)`
  - core `dQ/dV_n`
  - `solver`
  - `fallback`
  - `회귀`
  - `K_\lambda`
  - `DQ-v3`
  - standalone `DQ` status
  - `Codex`
  - `AGP`
  - `2026-05-28`
  - `Grounding 감사` / `self-check`
  - audit-style `통과`

## Not Verified

- PDF compile: `xelatex` was not found.
- External source audit for Refs 6/7 was not re-run in Phase 017.

## Resume Instructions

If context compaction occurs, do not rely on memory. Open in order:

1. This handover.
2. Phase 017 result.
3. Phase 017 ledger.
4. v5 TeX candidate.
5. Phase 016 comparison if another v4/v5 comparison is requested.

Before making further manuscript changes, preserve v5 and write a new plan/result pair for the next phase.
