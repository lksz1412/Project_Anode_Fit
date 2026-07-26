# Claude Rebuilt Base -> Codex Completion Master Roadmap

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:verification-before-completion` before any completion claim. This roadmap starts after the previous Codex draft line was archived. The active base is the copied Claude rebuilt TeX set.

**Goal:** Complete the Codex version by using the Claude rebuilt chapter set as the new base, then performing Codex-side review, correction, supplementation, and verification chapter by chapter.

**Architecture:** Do not restart from zero and do not patch old Codex v1--v5 files. Use the Claude rebuilt files copied into `Codex/results/PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01` as the source base. For each chapter, create a Codex working copy, run chunked deep review, repair only the identified problems, verify, and save a phase result/ledger/handover.

**Tech Stack:** LaTeX manuscript sources, PowerShell static verification, chunked line-range review, optional XeLaTeX PDF build if available, Codex `plans/results/work` phase recording.

---

## Summary

The project direction is reset as follows.

1. Previous Codex-produced chapter drafts, plans, review reports, and helper scripts have been archived to:

   `D:\Projects\Project_Anode_Fit\Codex\old\codex_pre_claude_rebase_20260601_2355`

2. The active Codex base is now the copied Claude rebuilt set:

   `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01`

3. Codex will not treat the old Codex Chapter 1/2 drafts as the manuscript base. They may be consulted only as archived comparison material if the user asks.

4. The working method is not "write a new theory from scratch." It is:

   ```text
   Claude rebuilt base
   -> Codex chunked review
   -> defect classification
   -> targeted supplement/repair
   -> Codex completed chapter candidate
   -> static/build verification
   -> phase result + ledger + handover
   ```

5. The most urgent chapter is Chapter 1 because all later chapters depend on its state variables, sign conventions, ICA tail logic, and fitting-level handoff.

## Current Ground Truth

### Active Base Reference Set

Reference directory:

`D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01`

Files:

- `graphite_ica_ch1_rebuilt.tex`
- `graphite_ica_ch2_rebuilt.tex`
- `graphite_ica_ch3_rebuilt.tex`
- `graphite_ica_ch4_rebuilt.tex`
- `graphite_ica_ch5_rebuilt.tex`
- `graphite_ica_ch6_rebuilt.tex`
- `graphite_ica_full_rebuilt.tex`
- `graphite_ica_refs_rebuilt.tex`
- `manifest.json`

### Archived Codex Line

Archive directory:

`D:\Projects\Project_Anode_Fit\Codex\old\codex_pre_claude_rebase_20260601_2355`

Archived counts:

- plans: 7
- results: 42
- work scripts: 5

### User's Active Priority

The user specifically objected that Claude Chapter 1 section 7 onward had become unreadable:

- integrals appeared abruptly;
- variable meanings and physical interpretation were unclear;
- the bridge from sections 1--6 into spectrum/kernel/fitting was weak;
- Chapter 1 alone did not provide a simple real-data fitting approximation;
- previous review likely checked formal correctness without small-chunk followability review.

This becomes the primary acceptance criterion for Chapter 1.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 021 | Rebase and base freeze | 1-10 | Archive old Codex line, freeze Claude rebuilt set as active base, write roadmap. |
| 022 | Chapter 1 review and repair plan | 11-35 | Chunked review plan and detailed correction direction for Ch1. |
| 023 | Chapter 1 Codex working copy and review execution | 36-70 | Create working copy, run 10-pass chunk review, produce defect ledger. |
| 024 | Chapter 1 targeted repair | 71-120 | Repair Ch1 section 7+ and any earlier bridge issues; preserve good material. |
| 025 | Chapter 1 verification and release candidate | 121-145 | Static checks, optional PDF build, 10-pass re-review, result/ledger/handover. |
| 026 | Chapter 2 review and repair | 146-185 | Align reversible heat chapter with repaired Ch1. |
| 027 | Chapter 3 review and repair | 186-225 | Align reaction kinetics with repaired Ch1/Ch2. |
| 028 | Chapter 4 review and repair | 226-265 | Align heat generation generalization with Ch2/Ch3. |
| 029 | Chapter 5 review and repair | 266-305 | Align hysteresis with Ch1/Ch3 conventions. |
| 030 | Chapter 6 / fitting-practice policy | 306-345 | Decide whether Ch6 remains as fitting appendix or is redistributed into chapters; repair accordingly. |
| 031 | References and integrated full manuscript | 346-390 | Rebuild refs/full, verify cross-refs/cites, save integrated result. |

## Non-goals

- Do not use old Codex drafts as the active base.
- Do not modify Claude directory.
- Do not overwrite the copied Claude reference files; create Codex working copies.
- Do not claim any chapter is complete without fresh verification.
- Do not accept Claude's "검수 완료" reports as proof.
- Do not run one whole-file review and call it deep review. Long chapters must be reviewed in small chunks with recorded line ranges.
- Do not remove Chapter 6 blindly. First classify which Ch6 content belongs inside each chapter and which content should remain as fitting/numerical appendix.
- Do not let fitting implementation dominate the theoretical chapters.
- Do not hide work history inside paper-facing LaTeX body.

## Implementation Changes

Already done:

- Move old Codex plans/results/work files into:

  `D:\Projects\Project_Anode_Fit\Codex\old\codex_pre_claude_rebase_20260601_2355`

- Keep active operating guide:

  `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`

- Keep active Claude reference set:

  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01`

Create next:

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-01-claude-rebuilt-base-codex-completion-roadmap.md`
- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-01-chapter1-claude-base-review-repair-plan.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_CODEX_REBASE_TO_CLAUDE_BASE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_031_CLAUDE_BASE_COMPLETION_LEDGER.md`

Future working copies:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_rebuilt_codex_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch2_rebuilt_codex_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch3_rebuilt_codex_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch4_rebuilt_codex_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch5_rebuilt_codex_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch6_rebuilt_codex_v1.tex` or a redistributed appendix plan, depending on Phase 030.

## Chapter-Level Strategy

### Chapter 1 - ICA tail foundation

Role:

- Defines core state variables, charge conservation, internal potential, equilibrium target, kinetic lag, effective barrier, relaxation-length spectrum, kernel integral, ICA/DVA expression, and a simple fitting approximation.

Main current risk:

- Section 7 onward may still be too machinery-heavy and unclear even after Claude's repair.
- Solver/Plan A/B/fitting content may be overcentralized in Chapter 1.

Codex target:

- Keep Claude's useful physical ingredients.
- Repair followability and usability.
- Ensure Chapter 1 alone gives a simple one-mode/small-tail fitting expression.
- Push full solver/validator content into appendix or Ch6 unless necessary for the theory proof.

### Chapter 2 - reversible heat / entropy coefficient

Role:

- Extends Ch1 equilibrium potential and transition inventory to reversible heat, entropy coefficient, apparent vs equilibrium \(dV/dT\), and heat separation.

Main current risk:

- If Ch1 convention or simplefit handoff changes, Ch2 may inherit stale notation.

Codex target:

- Re-check Ch2 only after Ch1 is repaired.
- Ensure reversible heat uses equilibrium coefficient, not dynamic tail response.

### Chapter 3 - reaction kinetics

Role:

- Expands Chapter 1 reduced mobility model into forward/backward kinetics, detailed balance, and Butler--Volmer-like structure.

Main current risk:

- Chapter 1 Level A common-mode mobility and Chapter 3 directional kinetics can be confused.

Codex target:

- Make the Level A -> Level B boundary explicit.

### Chapter 4 - heat generation with kinetics

Role:

- Connects Ch2 heat terms and Ch3 reaction kinetics into heat generation and entropy production.

Main current risk:

- Double counting reversible heat, kinetic-lag heat, and polarization heat.

Codex target:

- Verify energy-balance signs, units, and term separation.

### Chapter 5 - hysteresis

Role:

- Uses Ch1/Ch3 dynamic lag and directional kinetics to interpret charge/discharge hysteresis.

Main current risk:

- Charge/discharge sign convention and equilibrium/dynamic separation can drift.

Codex target:

- Verify branch definitions and hysteresis decomposition.

### Chapter 6 - fitting practice / numerical appendix

Role:

- Should not be the source of Chapter 1 logic.
- May remain as fitting/numerical practice, or be partially redistributed into chapter appendices.

Main current risk:

- If Ch6 is retained, earlier chapters may lazily defer needed usable formulas to Ch6.

Codex target:

- Ensure every chapter is self-contained for its own theoretical deliverable.
- Keep Ch6 as implementation/fitting workflow only.

### References and full manuscript

Role:

- Provide canonical bibliography and integrated manuscript.

Main current risk:

- Source references may compile but still contain incomplete "citation role" or placeholder annotations.

Codex target:

- Verify cite/bib consistency, DOI presence, and no placeholder bibliographic text in paper-facing final files.

## Review Method Standard

For every chapter review:

1. Read the full chapter in chunks.
2. Run 10 passes with different chunk sizes.
3. Each pass has a different lens.
4. Each pass records line coverage.
5. Findings must be categorized as:

   - `잘못된 부분`
   - `부족한 부분`
   - `개선할 부분`
   - `좋은 점/흡수할 부분`
   - `추가 검증 필요`

6. A finding cannot be marked resolved until the repaired file is re-read in the relevant chunk and static checks pass.

## Test Plan

Static checks for each `.tex` candidate:

- line count;
- SHA256;
- begin/end balance;
- brace balance;
- duplicate labels;
- missing refs;
- missing cites;
- high-risk string search:

  ```text
  Date:
  Author:
  RB 재구성본
  audit
  phase
  unresolved
  TBD
  TODO
  step-function
  0 -> 1
  근거 미발견
  ```

Build:

- If XeLaTeX exists, run 2-pass build.
- If not, report `xelatex NOT_FOUND`, do not claim PDF success.

Manual review gates:

- followability: can an undergraduate reader follow each derivation?
- physical meaning: does every variable/integral state what it measures?
- no hidden solver dependency: does the chapter's theory stand without numerical implementation?
- usability: does the chapter deliver the formula it promises?
- convention continuity: do later chapters receive stable variables?

## Assumptions

- The Claude rebuilt set is now the active base because the user explicitly requested that direction.
- The old Codex work is archived, not deleted, so it can be consulted later if the user asks.
- Chapter 1 must be stabilized before repairing Chapter 2--6.
- The user prefers detailed plans and phase records over short summaries.

## Correction History

- 2026-06-01: Roadmap created after user corrected Codex direction: use Claude rebuilt set as base, archive old Codex drafts, then supplement/repair into Codex completed version.

