# Phase 020 Handover - Claude Chapter 1 Review

## Current State

The Claude rebuilt TeX set was copied into Codex as a frozen reference:

- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01`

The primary file reviewed was:

- `graphite_ica_ch1_rebuilt.tex`
- SHA256: `2AFD3B0B4B9D66EE373240A5238673590259F8C366B6257C14F9B702D6909A07`

Review report:

- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_CH1_REBUILT_10PASS_REVIEW.md`

Plan:

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-01-chapter1-codex-rebuild-from-claude-review-plan.md`

## Important User Critique

The user's central complaint is not "some equation is wrong." It is:

- sections 7+ became unreadable;
- integrals appeared without enough physical motivation;
- variable meanings were unclear;
- the chapter did not yield a simple real-data fitting approximation;
- prior reviews likely failed because they checked correctness without chunked followability/usability review.

Any rewrite must treat readability and operational derivability as hard gates.

## Codex Judgment

Do not patch Claude Ch1 in place. Use it as source material and rewrite Codex Ch1 with a cleaner spine:

```text
observation
-> convention
-> charge conservation
-> equilibrium target
-> smooth effective mobility barrier
-> single-mode lag
-> relaxation-length spectrum
-> kernel integral
-> ICA expression
-> simplefit approximation
-> validity/falsification
```

Plan A/B and DAE/root-find content should be appendix-gated or moved later. The main Chapter 1 proof should not depend on solver machinery.

## Verification Artifacts

- `PHASE_020_CH1_CLAUDE_CHUNK_SCAN.json`
- `ch1_claude_chunk_review_scan.ps1`

Chunk sizes used:

```text
41, 53, 67, 79, 97, 113, 137, 163, 199, 251
```

## Next Recommended Action

Ask the user whether to execute the Codex rewrite plan. If approved, create a new Chapter 1 file under `Codex/results` and do not overwrite previous Codex or Claude artifacts.

