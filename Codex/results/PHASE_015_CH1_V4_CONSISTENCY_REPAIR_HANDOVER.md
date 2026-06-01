# Phase 015 Handover — Chapter 1 v4 Consistency Repair

## Handover Chain

1. Phase 014 comparison identified v3 issues:
   `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_014_CH1_V3_V2_COMPARISON.md`
2. Phase 015 repair plan:
   `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-v4-consistency-repair-plan.md`
3. Phase 015 repaired manuscript:
   `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex`
4. Phase 015 result:
   `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_CH1_V4_CONSISTENCY_REPAIR_RESULT.md`
5. Phase 015 ledger:
   `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_CH1_V4_CONSISTENCY_REPAIR_LEDGER.md`

## Current Canonical Candidate

Use:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex`

Do not overwrite v2 or v3 unless the user explicitly asks.

## Confirmed State

- v4 is generated from v3 as a new artifact.
- Coordinate convention is repaired around `q`, `L_q`, and explicit `L_Q`.
- Plan B is theoretical baseline, not code fallback.
- Plan A remains candidate analytic compression only after validation.
- AL table is embedded in the manuscript.
- `xi` remnants and implementation-colored fallback language were removed.

## Verification

- Final v4 lines: 856
- Final v4 SHA256: `615CD1F828B61C7A24E56FE7FA55F01F306768CEEBC69655D8B50BBB60A8CCC6`
- Full-read coverage: 1-856
- Static checks passed:
  - begin/end `52/52`
  - braces `749/749`
  - missing refs `0`
  - missing cites `0`
- High-risk pattern checks returned `0` for selected remnants.
- `xelatex` is not available, so no PDF was built.

## Resume Instructions

If work resumes after context compaction:

1. Read this handover.
2. Read the Phase 015 result.
3. Open the v4 `.tex` file.
4. Do not rely on memory for which issues were fixed; use the recorded verification.
5. If the user asks for another audit, start from v4 and create a new Phase 016 plan/result rather than editing history.
