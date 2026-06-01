# PHASE 039 — Chapter 2 V5 Spine Plan And Source Review

## Purpose

Chapter 1 V5의 convention spine을 기준으로 Chapter 2를 이어 작성/보수하기 위한 입력 검토와 작업 기준을 기록한다. 이 phase는 본문 변경 이력 문건이며 TeX 본문에는 phase/작업 이력을 넣지 않는다.

## Input Files

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v5.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_038_CH1_V5_VERIFICATION_AND_HANDOVER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch2_rebuilt.tex`
- Working candidate: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch2_codex_candidate_v1.tex`

## Chapter 1 V5 Downstream Interface Applied

- Use `Q_\bg^{\eq}` for equilibrium background capacity; do not reintroduce unsplit `Q_\bg` into the fitting denominator.
- Keep `V_n`, `V_{n,\app}`, `V_{n,\drive}`, and `V_{n,\OCV}` distinct.
- Treat `\chi_j` as Chapter 1 Level-A scalar mobility sensitivity.
- Do not identify `\beta_j` with `\chi_j`; Chapter 3 introduces `\beta_j` separately.
- Keep reversible heat tied to equilibrium entropy coefficient / reaction entropy.
- Keep irreversible heat tied to overpotential, flux-force, and entropy production.
- Do not implement solver/fitting code in this chapter.

## Actual Read Coverage

- Chapter 2 candidate full read by range:
  - lines 1--180
  - lines 181--360
  - lines 361--540
  - lines 541--720
  - lines 721--854
- Source line count after edits: 854 content lines plus trailing newline accounting in parser.

## Findings Before Repair

- TeX top comments contained worker-facing reconstruction metadata and `Codex V5-aligned candidate`.
- PDF metadata contained `candidate`.
- The body contained a `Chapter 2 자체 검수표`, which belongs in result records rather than manuscript body.
- Multiple body lines referred to solver implementation as `Chapter 6`, while current requested scope is Chapters 1--5 theory only.
- One text-font Greek sigma in the AL table produced a missing-character warning.

## Repair Plan

1. Remove worker-facing top metadata and leave only a neutral scientific chapter comment.
2. Remove `candidate` from PDF metadata.
3. Remove the manuscript-body self-check table.
4. Replace `Chapter 6` / solver implementation wording with theory-scope statements and separate numerical implementation wording.
5. Replace text `σ` in the AL table with math-mode `$\sigma$`.
6. Run static label/ref/cite/risk checks.
7. Run XeLaTeX build and record warnings without overstating cleanliness.

## Gate

Proceed to Phase 040 only if Chapter 2 compiles without LaTeX errors and without undefined references/citations. Layout warnings are recorded separately.
