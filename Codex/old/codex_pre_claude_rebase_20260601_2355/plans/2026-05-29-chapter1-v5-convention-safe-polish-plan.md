# Chapter 1 v5 Convention-Safe Polish Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:verification-before-completion` before any completion claim. This plan is a narrow manuscript-polish phase, not a new theoretical rewrite.

**Goal:** Upgrade Chapter 1 from v4 to v5 by absorbing the good points from the v4-v3 comparison while preventing new convention drift or logical drift.

**Architecture:** Treat `graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex` as the current canonical candidate. Apply only tightly scoped paper-facing cleanup: remove version/process labels, expand shorthand kernel notation, and rewrite internal audit wording as manuscript-style validation status. Preserve the core chain `charge conservation -> theta_eq -> Delta G_eff -> k -> L_q -> A_L -> spectrum kernel integral -> dQ_ext/dV_n`.

**Tech Stack:** LaTeX manuscript source, PowerShell 7 UTF-8 file operations, static LaTeX/convention checks.

---

## Summary

This phase responds to the user's instruction:

- 좋은 점은 흡수한다.
- 흡수 과정에서 convention 문제를 새로 만들지 않는다.
- 흡수 과정에서 논리 문제를 새로 만들지 않는다.
- Chapter 1 remains a theory/logic manuscript, not solver/fitting implementation.

The physical target remains:

- LIB graphite anode ICA (`dQ/dV`) peak-tail behavior.
- Low temperature: longer post-peak tail.
- High temperature: shorter post-peak tail.
- Activation barrier is retained as a real thermodynamic/kinetic mechanism.
- Step-function style `0 -> 1` transition is forbidden.
- Electrode-potential assistance lowers an effective barrier smoothly.
- Chapter 1 must explain the tail behavior with undergraduate-followable derivation and no hidden logical jumps.

## Current Ground Truth

Source files already established by Phase 016:

- Previous candidate: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex`
- Current candidate: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex`
- Comparison report: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_016_CH1_V4_V3_COMPARISON.md`

Phase 016 verdict:

- v4 is materially better than v3.
- v4 should remain the base for the next candidate.
- Core mathematical chain in v4 has no blocking inconsistency found in Phase 016.

Known v4 repair candidates:

- `DQ-v3-*` labels remain in the manuscript body.
- `K_\lambda` appears as a schematic shorthand without a local definition.
- `Grounding 감사 (AGP self-check)` reads like process metadata rather than paper-facing validation prose.
- External Refs 6/7 audit was not re-performed, so Plan A remains gated.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 017 | Convention-safe v5 polish | 1-10 | Apply small manuscript-facing repairs and verify no convention/logic regression. |

## Non-goals

- Do not rewrite the Chapter 1 theory from scratch in this phase.
- Do not promote Plan A to established theory.
- Do not create solver, fitting code, or numerical implementation.
- Do not modify Claude workspace or original source PDFs.
- Do not overwrite v3, v4, Phase 015, or Phase 016 artifacts.
- Do not introduce new symbols for the core coordinate system.
- Do not change `q` to dimensional `Q` except where v4 already uses `Q_ext`, `Q_cell`, or `L_Q` for explicit dimensional conversion.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_HANDOVER.md`
- `D:\Projects\Project_Anode_Fit\Codex\work\create_ch1_v5_convention_safe_polish.ps1`

Modify:

- No existing project artifact is modified in place.

## Phase 017 - Convention-Safe v5 Polish

- [ ] **Step 1: Save this plan before manuscript edits.**

  Expected: plan exists in `Codex\plans`.

- [ ] **Step 2: Reconfirm Phase 016 repair list from file.**

  Expected: the v5 edits trace to actual Phase 016 findings or direct manuscript-convention risk found during inspection.

- [ ] **Step 3: Copy v4 to v5 as a new file.**

  Expected: v4 remains untouched.

- [ ] **Step 4: Replace version-specific validation tags.**

  Exact intent:

  - `DQ-v3-1` -> `VG-1`
  - `DQ-v3-2` -> `VG-2`

  Expected: no `DQ-v3` remains.

- [ ] **Step 5: Remove process-history language from manuscript body.**

  Exact intent:

  - Replace date/user correction heading with neutral manuscript wording.
  - Replace `AGP` with `Validation rule` where it appears as process label.
  - Remove `Codex 산출물과의 대조` from the central equation explanation.

  Expected: no `Codex`, `AGP`, or `2026-05-28` process marker remains in v5 body.

- [ ] **Step 6: Expand the schematic `K_\lambda` chain.**

  Replace the shorthand closure arrow with an explicit kernel integral using the already defined normalized length variable:

  ```latex
  \int_0^\infty A_L(\lambda;T,\psi)\lambda^{-1}
  \exp[-(q-q_a)/\lambda]\,d\lambda
  ```

  Expected: no undefined `K_\lambda` remains.

- [ ] **Step 7: Rewrite the internal audit table as paper-facing validation status.**

  Expected: section/subsection title and table statuses read as assumption/validation status, not work-process self-check.

- [ ] **Step 8: Run static LaTeX checks.**

  Required checks:

  - `\begin` and `\end` counts match.
  - Brace counts match.
  - All `\ref{...}` targets exist.
  - All `\cite{...}` keys exist in `\bibitem{...}`.

- [ ] **Step 9: Run targeted convention and logic-drift checks.**

  Must remain absent:

  - `\xi`
  - `L=v_Q/k`
  - generic `$L(G)$`
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
  - `Codex`
  - `AGP`
  - `2026-05-28`

- [ ] **Step 10: Save result, ledger, and handover.**

  Expected: Phase 017 artifacts state actual read coverage, commands, verification evidence, confirmed repairs, and remaining gates.

## Test Plan

Static verification commands will be run after v5 generation:

- Read v5 line count.
- Compute SHA256.
- Count LaTeX `begin/end`, braces, labels, refs, cites, bibitems.
- Check missing refs and missing citations.
- Search all targeted high-risk patterns.
- Full-read v5 in line chunks and record the coverage in Phase 017 result.

PDF build is optional only if a TeX engine is available. If `xelatex` is missing, report it as not run, not as success.

## Assumptions

- v4 remains the mathematical base because Phase 016 found no blocking inconsistency in the core chain.
- This phase is a polish/repair phase, not a new theory derivation phase.
- Plan A remains candidate analytic compression until Refs 6/7 are source-audited again.
- Plan B remains the conservative theoretical baseline.

## Correction History

- Phase 017 starts from Phase 016 comparison findings and adds one direct manuscript-convention cleanup found during inspection: removing process-history markers such as `Codex`, `AGP`, and `2026-05-28` from the LaTeX body.
