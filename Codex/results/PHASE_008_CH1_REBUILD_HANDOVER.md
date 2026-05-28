# Phase 008 — Chapter 1 Rebuild Handover

Date: 2026-05-28

## Handover Chain

| Order | Artifact | Path | Gate |
|---:|---|---|---|
| 1 | Claude/Codex comparison | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_CLAUDE_CODEX_CH1_COMPARISON.md` | comparison complete |
| 2 | Rebuild plan | `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-rebuild-claude-strengths-spectrum-plan.md` | `PASS_PLAN_SAVED` |
| 3 | Draft result | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CH1_REBUILD_DRAFT_RESULT.md` | `PASS_CH1_DRAFT_COMPLETE` |
| 4 | Logic review | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_CH1_REBUILD_LOGIC_REVIEW_10PASS.md` | `PASS_10_LOGIC_LOOPS` |
| 5 | Ledger | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_008_CH1_REBUILD_LEDGER.md` | `PASS_REBUILD_HANDOVER_READY` |

## Final Manuscript

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex`

Status:

```text
Chapter 1 rebuilt candidate after 10-pass logic review
```

This is not claimed as experimentally validated or publication-final. It is a reviewed theoretical manuscript candidate.

## What Changed Conceptually

The rewrite adopts Claude Code's strengths:

- review-paper-like convention section;
- explicit forbidden model boundary;
- lattice-gas / regular-solution equilibrium basis;
- charge conservation and implicit \(V_n\);
- measured \(V_{\app}\) bridge warning;
- effective activation barrier with bounded validity;
- self-consistent integral layer;
- falsification and non-identifiability protocol;
- bibliography scaffold.

The rewrite replaces Claude's single-tail emphasis with the corrected central tail mechanism:

```text
activation free-energy barrier distribution
-> rate constant distribution
-> relaxation-length spectrum
-> exponential kernel integral
-> observed ICA tail
```

The local single exponential remains, but only as one local kernel:

```tex
r_j(Q)\simeq r_j(Q_a)\exp[-(Q-Q_a)/L_j],
\qquad
L_j=v_Q/k_j.
```

The measured tail is:

```tex
\mathcal T_j(Q;T,\psi)
=
\int_0^\infty
A_{L,j}(L;T,\psi)
\frac{1}{L}
\exp[-(Q-Q_{a,j})/L]\,dL.
```

## Final Validation

| Check | Status |
|---|---|
| Final manuscript read start-to-end | PASS, lines 1-910 |
| 12 manuscript sections present | PASS |
| Label/ref inventory | PASS |
| Citation/bibliography inventory | PASS |
| Brace/environment counts | PASS |
| Banned adopted step-function model | PASS, not adopted |
| PDF generation | NOT RUN, no `xelatex` in PATH |

## Important Boundaries For Next Session

- Do not rely on memory alone. Reopen this handover, the ledger, and the final `.tex` before continuing.
- Do not modify Claude files unless user explicitly requests it.
- Do not treat refs 6/7 as a graphite physical model. They are a mathematical method boundary for self-consistent integral closure.
- Do not collapse the tail back into one relaxation length. Single \(L\) is only a local kernel parameter.
- Do not use a discontinuous state completion rule.
- Do not claim unique inversion from measured tail to microscopic barrier distribution.

## Open Issues

| Issue | Status |
|---|---|
| Full PDF build | unavailable in current PATH |
| DOI-level bibliography audit | not performed in this phase |
| Experimental falsification | future work |
| Fitting model implementation | future work |

## Recommended Next Step

Have the user review:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex`

After review, the next phase should be one of:

1. bibliography/DOI audit and manuscript polish, or
2. Chapter 2 derivation using \(U_j(T)\), \(\xi_{\eq,j}\), \(V_n(Q,T)\), and relaxation-spectrum variables.
