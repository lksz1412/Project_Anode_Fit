# Chapter 1 v3 Canonical Merge Plan

## Summary

사용자 결정에 따라 최신 Claude Chapter 1의 manuscript shell과 최신 Codex Chapter 1의 logic-only dual closure를 병합한다. 목표는 기존 파일을 덮어쓰지 않고 `Codex\results`에 새 canonical merge version을 생성하는 것이다.

## Current Ground Truth

- Active project: `D:\Projects\Project_Anode_Fit`.
- Codex workspace: `D:\Projects\Project_Anode_Fit\Codex`.
- Claude file is reference only and must not be modified.
- Latest comparison report: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_012_LATEST_CLAUDE_CODEX_DUAL_CLOSURE_COMPARISON.md`.
- Canonical direction: Claude publishable structure + Codex no-overclaim logic.
- Current Chapter 1 is theory/logic only. It must not become a solver, fitting workflow, direct numerical fallback, validator workflow, or code design document.

## Phase Range

| Phase | Name | Step Range | Output | Gate |
|---|---|---:|---|---|
| Phase 013 | Chapter 1 v3 canonical merge | 1-12 | `graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex` | `PASS_V3_CANONICAL_MERGE_REVIEWED` |

## Non-goals

- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not overwrite Codex v1 or v2 result files.
- Do not implement fitting code or a numerical solver.
- Do not make refs 6/7 load-bearing unless the Fredholm/variable mapping is verified.
- Do not describe Plan B as code fallback.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_013_CH1_V3_CANONICAL_MERGE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_013_CH1_V3_CANONICAL_MERGE_LEDGER.md`

Read without modification:

- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_chapter1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v2_dual_closure.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_012_LATEST_CLAUDE_CODEX_DUAL_CLOSURE_COMPARISON.md`

## Phase 013 — Chapter 1 v3 canonical merge

- [ ] Step 1: Confirm latest source file paths and read coverage.
- [ ] Step 2: Use Claude file as structural shell only.
- [ ] Step 3: Replace abstract closure claim with logic-only Plan A/Plan B hierarchy.
- [ ] Step 4: Replace Refs 6/7 load-bearing wording with candidate analytic closure wording.
- [ ] Step 5: Replace S10 spine item with Plan A candidate + Plan B conservative theoretical formulation.
- [ ] Step 6: Replace self-consistent integral closure section with Codex logic-only closure section.
- [ ] Step 7: Preserve Claude strengths: user verbatim, H1-H6, S1-S14, AL tags, graphite staging, voltage bridge, falsification, DOI-rich bibliography.
- [ ] Step 8: Preserve Codex strengths: Plan B as theoretical base, not code fallback; refs 6/7 as method candidate; state/target/rate separation.
- [ ] Step 9: Remove direct-numerical/fallback/validator/switch/floor language from the manuscript body.
- [ ] Step 10: Run static TeX checks.
- [ ] Step 11: Run banned-term and missing-reference checks.
- [ ] Step 12: Save result and ledger.

## Test Plan

- Check file existence.
- Check begin/end count.
- Check brace count.
- Check labels/refs.
- Check cites/bibitems.
- Search for implementation-colored terms: `direct numerical`, `fallback`, `validator`, `switch criterion`, `single-mode floor`.
- Confirm Claude file unchanged by path policy.

## Assumptions

- This phase is a manuscript-level canonical merge, not final literature validation.
- Refs 6/7 remain candidate closure methods until exact equation-class and variable mapping are verified.
- PDF build is optional because xelatex may not be installed in the current environment.

## Correction History

- Supersedes Phase 012 comparison decision by implementing the recommended canonical merge.
