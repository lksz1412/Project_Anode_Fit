# Chapter 1 V4 Full Rebuild and 10-Pass Review Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This project stores plans in `D:\Projects\Project_Anode_Fit\Codex\plans` and deliverables/results in `D:\Projects\Project_Anode_Fit\Codex\results`.

**Goal:** Produce a final Chapter 1 candidate that is self-contained enough to derive and use a first-pass ICA tail fitting approximation for graphite anode dQ/dV, with no physical leaps, no undefined variables, consistent convention, and ten full-document review passes using different chunk granularities.

**Architecture:** Use Codex v3 as the safer convention spine and Claude final Chapter 1 as the detailed explanatory scaffold. The final v4 must not copy Claude's convention conflicts: `chi_j` remains Level-A scalar relaxation-barrier sensitivity, not the Chapter 3 transfer coefficient; amplitude-bearing spectra must carry their amplitude; support limits are domain conditions, not artificial step functions.

**Tech Stack:** LaTeX with kotex, amsmath, longtable, theorem boxes; verification by static text checks, label/ref/cite parsing, and XeLaTeX 2-pass build.

---

## Summary

The user requested overnight uninterrupted execution. Do not ask intermediate questions. Complete the Chapter 1 rebuild, run ten review passes with varied chunk lengths, repair every issue found, and leave all evidence in `Codex\results`.

## Current Ground Truth

- Codex v3 is mechanically valid and safer in convention, but too compressed for the user's target.
- Claude final is fuller and more usable, but has convention and notation issues:
  - `chi_j` is incorrectly described as identical to Chapter 3 transfer coefficient `beta_j` in the notation table.
  - Single-mode `A_L=delta(L-L*)` loses amplitude if `A_L` is an amplitude spectrum.
  - `H(L-L_min)` is mathematically a support indicator but visually resembles a step-function model; prefer lower-limit domain language.
  - Process metadata remains in scientific document body/preamble.
  - Some bibliography entries remain placeholder-like.
  - C-rate conclusion is too one-directional unless current prefactor, potential-assisted rate, and apparent-axis polarization are separated.

## Phase Range

- Phase 027: Source freeze and v4 drafting.
- Phase 028: Ten-pass full review with varied chunk lengths.
- Phase 029: Repair loop and final verification.
- Phase 030: Result report, change history, handover, ledger update.

## Non-goals

- Do not implement fitting code or numerical solvers.
- Do not modify Claude-side files.
- Do not delete or overwrite earlier result files.
- Do not write phase/change history inside the LaTeX scientific body.
- Do not claim Plan A quantitative validity without Plan B validation.

## Implementation Changes

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex`
- Create: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_028_CH1_V4_10PASS_REVIEW.md`
- Create: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_029_CH1_V4_VERIFICATION_RESULT.md`
- Create: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_030_CH1_V4_CHANGE_HISTORY_AND_HANDOVER.md`
- Update if present: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_031_CLAUDE_BASE_COMPLETION_LEDGER.md`

## Phase 027 — Source Freeze and V4 Drafting

### Task 1: Freeze source state

**Files:**
- Read: Codex v3, Claude final, Phase 026 comparison report.
- Create result metadata in Phase 028/029 reports.

- [ ] Step 1: Record line counts and SHA256 for Codex v3 and Claude final.
- [ ] Step 2: Confirm no Claude-side file will be edited.

### Task 2: Build v4 from safe convention spine plus detailed scaffold

**Files:**
- Create: `graphite_ica_ch1_codex_candidate_v4.tex`

- [ ] Step 3: Remove process metadata from scientific TeX body.
- [ ] Step 4: Insert early convention/assumption section: branch convention, barrier convention, ICA fitting convention, assumption ledger summary.
- [ ] Step 5: Preserve Claude's detailed derivations where they improve G-follow.
- [ ] Step 6: Correct `chi_j` so it is not identical to `beta_j` in Chapter 1.
- [ ] Step 7: Correct amplitude spectrum and single-mode delta notation.
- [ ] Step 8: Replace visible Heaviside support expression with lower-limit domain statements.
- [ ] Step 9: Make C-rate discussion explicitly competitive, not one-directional.
- [ ] Step 10: Replace placeholder bibliography with complete entries from Codex v3 and verified source notes.

**Gate:** v4 must contain all major sections from Claude final, while preserving Codex's safer convention choices.

## Phase 028 — Ten-Pass Full Review With Varied Chunk Lengths

Each pass must cover the whole v4 file. Chunk lengths differ by pass. Every pass must record actual coverage and findings.

- [ ] Step 11: Pass 1, section-level chunks: macro/structure/metadata/convention.
- [ ] Step 12: Pass 2, 70-line chunks: variable introduction and meaning.
- [ ] Step 13: Pass 3, 90-line chunks offset by 35 lines: equation continuity and no skipped derivation.
- [ ] Step 14: Pass 4, 120-line chunks: physical assumptions and citation/grounding.
- [ ] Step 15: Pass 5, 55-line chunks: units, dimensions, sign conventions.
- [ ] Step 16: Pass 6, logical dependency chunks: charge balance -> equilibrium -> rate -> dynamics -> spectrum -> kernel -> self-consistency -> fitting.
- [ ] Step 17: Pass 7, reverse-order chunks: catch forward-reference and late-definition issues.
- [ ] Step 18: Pass 8, fitting-usability chunks: can a reader extract `Y_tail`, `L`, `chi_j`, and effective enthalpy without circularity?
- [ ] Step 19: Pass 9, adversarial physics chunks: transport/charge-transfer degeneracy, barrier-only disorder, Plan A limits.
- [ ] Step 20: Pass 10, final full sweep: consistency with user requirements and no remaining high/critical defects.

**Gate:** Every line must be covered in every pass, and unresolved findings must be classified as fixed, bounded/accepted with reason, or remaining risk.

## Phase 029 — Repair Loop and Verification

- [ ] Step 21: Apply repairs found in review passes.
- [ ] Step 22: Run static label/ref/cite checks.
- [ ] Step 23: Run risk-pattern checks: process metadata, `chi_j` identity, amplitude-less delta, Heaviside/step-function, placeholder bibliography, C-rate one-direction overclaim.
- [ ] Step 24: Run XeLaTeX 2-pass build.
- [ ] Step 25: If verification fails, repair and repeat until no LaTeX errors, no undefined refs/cites, no duplicate labels.

## Phase 030 — Result Report and Handover

- [ ] Step 26: Save 10-pass review report.
- [ ] Step 27: Save verification result.
- [ ] Step 28: Save change history and handover.
- [ ] Step 29: Update ledger with v4 status.

## Test Plan

- Static parse: line count, SHA256, begin/end balance, brace balance, labels, refs, cites, duplicate labels.
- Risk-pattern scan: `step-function`, `Heaviside`, `H(`, `동일물`, `beta_j`, `placeholder`, `...`, process metadata.
- Build: XeLaTeX two passes with output PDF.
- Content gates: G-follow, G-usable, G-noleap, convention consistency, assumption grounding, fitting non-circularity, falsifiability.

## Assumptions

- Claude final file is treated as a reference source, not as an editable target.
- v4 is allowed to be longer than Codex v3 because the user's priority is no skipped logic and undergraduate-level followability.
- The final output is TeX; PDF is verification artifact only.

## Correction History

- This plan supersedes the weaker Phase 025/026 conclusion that only identified issues. It explicitly requires repair, ten full review passes, and final v4 creation.
