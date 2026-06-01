# Phase 015 — Chapter 1 v4 Consistency Repair Result

Date: 2026-05-28

## Scope

User request: fix the problems found in the latest Chapter 1 comparison.

Primary target:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex`

This phase does not overwrite v2 or v3. It creates a new v4 candidate from v3 and records the repair evidence.

## Input Files Actually Used

| Role | File | Coverage |
|---|---|---|
| Project rules | `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` | Read relevant sections for project boundary, phase record, verification rules |
| Prior comparison | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_014_CH1_V3_V2_COMPARISON.md` | Read issue list and repair targets |
| Source manuscript | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex` | Read targeted sections before transformation |
| Generated manuscript | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex` | Final full read lines 1-856 in chunks 1-220, 221-440, 441-660, 661-856 |

## Created / Updated Files

| File | Status |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-v4-consistency-repair-plan.md` | Created |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex` | Created / regenerated |
| `D:\Projects\Project_Anode_Fit\Codex\work\create_ch1_v4_consistency_repaired.ps1` | Created / retained as reproducibility script |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_CH1_V4_CONSISTENCY_REPAIR_RESULT.md` | Created |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_CH1_V4_CONSISTENCY_REPAIR_LEDGER.md` | Created |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_CH1_V4_CONSISTENCY_REPAIR_HANDOVER.md` | Created |

## Main Repairs

1. Coordinate convention repaired.
   - Primary coordinate is now normalized `q=Q_ext/Q_cell`.
   - Primary relaxation length is now `L_q=v_q/k=|I|/(Q_cell k)`.
   - Dimensional length is explicitly separated as `L_Q=v_Q/k=Q_cell L_q`.
   - Plan B residual, kernel, ICA mapping, voltage-axis tail scale, and summary use this convention.

2. State symbol drift repaired.
   - Stray `xi` / `xi_j` notation was removed from Plan A and Plan B.
   - The manuscript consistently uses `theta_j`, `theta_eq,j`, and `Theta`.

3. Derivation granularity restored.
   - Added displayed regular-solution chemical potential.
   - Added electrochemical equilibrium condition.
   - Added ideal logistic target derivation and derivative / width argument.
   - Added differential charge-balance derivation.
   - Expanded forward/backward rate derivation into first-order relaxation.

4. Assumption Ledger added inside the `.tex`.
   - Added compact AL-1 through AL-10 table so AL tags are not external-only.

5. Plan A / Plan B wording repaired.
   - Plan B is described as the always-preserved theoretical baseline.
   - Plan A is described only as candidate analytic compression after M1-M5 and limiting-case checks.
   - Implementation-colored remnants such as `solver`, `code route`, `coding route`, and `fallback` were removed from the manuscript body.

6. Remaining `L` notation cleanup.
   - Special-case spectrum expression now uses `A_L(lambda)=delta(lambda-L_{q,0})`.
   - Core chain now uses `int A_L(lambda) K_lambda d lambda`.

## Verification Evidence

Generated v4 file:

| Property | Value |
|---|---|
| Lines | 856 |
| SHA256 | `615CD1F828B61C7A24E56FE7FA55F01F306768CEEBC69655D8B50BBB60A8CCC6` |

Static checks:

| Check | Result |
|---|---|
| `\begin{}` / `\end{}` count | `52 / 52` |
| brace count | `749 / 749` |
| labels / refs | labels `55`, refs `25`, missing refs `0` |
| bibitems / cites | bibitems `20`, cites `20`, missing cites `0` |

Targeted high-risk pattern check:

All of the following returned count `0`: `\xi`, `L=v_Q/k`, `$L(G)$`, `large-$L$`, `short-$L$`, `\frac{\dd r_j}{\dd Q}`, `Q_{a,j}`, `\Theta(Q)`, `\xi_j`, `dQ/dV_n`, `fallback`, `회귀`, `solver`, `code route`, `code procedure`, `coding route`, `closed-form`, `closed analytic shortcut`, `switch criterion`, `single-mode floor`, `\,dL`, `K_L`, `delta(L-L_0)`.

Expected / intentional dimensional conversion remains:

- `dTheta/dQ_ext=(1/Q_cell)dTheta/dq`
- `dG/dL_q`

These are not drift errors; they are explicit conversion / Jacobian statements.

PDF status:

- `xelatex NOT_FOUND`
- PDF was not generated in this phase.

## Gate Result

Gate status: PASS for the requested consistency repair.

Residual risk:

- Scientific novelty and final publication-level validity still require future literature grounding and user review.
- Plan A / Refs 6/7 closure remains gated, not established.
- This phase did not install TeX or build PDF.

## Next Step

Use v4 as the next Codex Chapter 1 candidate for user review or for a later deeper scientific audit loop.
