# Phase 001 — Clean-Slate Baseline Result

## Summary

The user instructed:

> 이전의 작업물은 old로 넘기고 챕터 1 다시 처음부터 시작한다.

Action taken:

- Previous active Chapter 1 plans/results were moved into an archive folder under `Codex\old`.
- Active `plans` now retains the operations guide and the new clean-slate plan.
- Active `results` now starts a new Phase 001-008 chain.

Gate result:

`PASS_CLEAN_SLATE_BASELINE`

## Step Range

Steps 1-18.

## Inputs

| Input | Use |
|---|---|
| User instruction | Restart Chapter 1 from scratch |
| `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` | Project operating rules |
| `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md` | Plan/result/ledger format |

## Files Created

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-clean-slate-plan.md` | New Chapter 1 clean-slate plan |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_008_CHAPTER1_CLEAN_SLATE_LEDGER.md` | New execution ledger |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_CLEAN_SLATE_BASELINE_RESULT.md` | This baseline result |

## Files Moved To Old

Archive path:

`D:\Projects\Project_Anode_Fit\Codex\old\2026-05-28-reset-before-chapter1-clean-restart`

| Category | Count |
|---|---:|
| Plans moved | 4 |
| Results moved | 26 |

## Current Active Folder State

| Folder | State |
|---|---|
| `Codex\plans` | Contains `phase_planning_operations_guide.md` and the new clean-slate plan |
| `Codex\results` | Contains only new clean-slate Phase 001 artifacts |
| `Codex\old` | Contains archived previous work |

## Locked Clean-Slate Rules

- Archived drafts are non-canonical.
- Archived equations are not equation authority.
- The new Chapter 1 must be derived from the user observation, defensible theory, and explicitly labeled reduced assumptions.
- Barrier handling must not use `max`, clipping, softplus, cap, bounded transform, or step-function-like treatment as core physics.
- If the reduced active barrier is exhausted, the active-barrier regime ends; the text must not silently clip the barrier.
- Physical limits must be discussed as physical bottlenecks or later-chapter extensions, not mathematical repair devices.

## User Physical Target

Chapter 1 must explain, without logical leaps:

- graphite negative-electrode ICA peak tail after phase-transition peak;
- low-temperature long tail;
- high-temperature shorter tail;
- temperature-dependent activation barrier;
- present electrode-potential-assisted effective barrier lowering;
- finite kinetic lag as the mechanism behind post-peak residual tail;
- capacity-axis and voltage-axis tail distinction;
- no peak-area-centered argument.

## Execution Evidence

Move operation result:

```text
Moved plan files: 4
Moved result files: 26
Archive: D:\Projects\Project_Anode_Fit\Codex\old\2026-05-28-reset-before-chapter1-clean-restart
```

## Validation

| Check | Result |
|---|---|
| Archive path exists | PASS |
| Previous active results moved out | PASS |
| Active `plans` keeps operations guide | PASS |
| New clean-slate plan created | PASS |
| New execution ledger created | PASS |
| Banned shortcuts recorded | PASS |
| Previous TeX not marked canonical | PASS |

## Gate

Gate:

`PASS_CLEAN_SLATE_BASELINE`

Status:

PASS

## Confirmed Non-Changes

- `D:\Projects\Project_Anode_Fit\Claude` was not modified by this phase.
- Original source/download files were not modified by this phase.
- `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` was not modified by this phase.
- `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md` was not modified by this phase.

## Open Issues / Decision Queue

No user decision is required before Phase 002.

Phase 002 must not treat archived drafts as equation authority.

## Next

Proceed to Phase 002: Evidence And Source Inventory.
