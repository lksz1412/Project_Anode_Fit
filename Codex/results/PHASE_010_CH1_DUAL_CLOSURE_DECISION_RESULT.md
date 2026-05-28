# Phase 010 — Chapter 1 Dual Closure Decision Result

Date: 2026-05-28

## Summary

User decision accepted:

```text
Use two closure routes in parallel:
Plan A = Fredholm / refs 6/7 ratio-substitution closure if validated.
Plan B = conservative local ODE + relaxation-length spectrum kernel fallback if Plan A fails.
```

Implemented this decision as a new manuscript version:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v2_dual_closure.tex`

The previous v1 file remains unchanged as a historical reviewed candidate:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex`

## Inputs

| Input | Use |
|---|---|
| User decision: "그래 그렇게 가자." | approved dual-route direction |
| `PHASE_009_CLAUDE_V4_CODEX_REBUILT_CH1_COMPARISON.md` | basis for Plan A/Plan B hierarchy |
| `graphite_ica_chapter1_rebuilt_v1.tex` | copied as v2 starting point |

## Files Created

| File | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v2_dual_closure.tex` | Chapter 1 v2 with dual closure hierarchy |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_010_CH1_DUAL_CLOSURE_DECISION_RESULT.md` | this result record |

## Files Modified

None outside the new v2 manuscript and this result file.

## Main Manuscript Changes

### Abstract

Added the closure hierarchy:

```text
Fredholm / ratio-substitution route validated -> Plan A.
If not validated -> Plan B conservative formulation.
```

### Self-Consistent Integral Section

Renamed and expanded:

```text
Self-Consistent Integral Layer and Refs 6/7 Placement
```

to:

```text
Dual Closure Hierarchy for Self-Consistent Integral Layer
```

New subsections:

1. Why two closure routes are kept
2. Plan A: Refs 6/7 as candidate Fredholm / ratio-substitution closure
3. Plan B: conservative ODE plus spectrum-kernel fallback
4. Decision rule between Plan A and Plan B

### Plan A Gate

Plan A is promoted only if:

- charge-balance feedback and barrier spectrum can be recast as a fixed-domain Fredholm-type second-kind equation;
- the same unknown function class appears inside and outside the integral;
- the ratio-substitution target variable is explicitly defined;
- the single-mode limit returns the local exponential kernel;
- direct integration or an equivalent reference solution validates the closure error.

### Plan B Fallback

Plan B retains:

```tex
dr/dQ + (k/v_Q)r = dxi_eq/dQ
L(G,T,psi)=v_Q/k_0 exp[(G-W_psi)/(RT)]
T_j(Q)=int A_L(L)(1/L) exp[-(Q-Q_a)/L] dL
```

Plan B is explicitly marked as the conservative core that survives if Plan A fails.

## Validation

Static checks executed on:

`graphite_ica_chapter1_rebuilt_v2_dual_closure.tex`

| Check | Result |
|---|---|
| line count | 1009 lines |
| section inventory | PASS, 12 sections |
| begin/end count | PASS, `begin=54`, `end=54` |
| brace count | PASS, `open_braces=643`, `close_braces=643` |
| label/ref inventory | PASS, 90 labels, 19 refs, no missing refs |
| cite/bib inventory | PASS, 15 bibitems, 15 cited keys, no missing or uncited entries |
| banned adopted step-function model | PASS; only negative prose hit `threshold completion model이 아니다` |
| closure language | PASS; `Plan A`, `Plan B`, `Fredholm`, `ratio-substitution`, `fallback`, and `validated analytic closure` are present |
| PDF build | NOT RUN; `xelatex` not found in PATH |

SHA256:

```text
65711B71ED64D6646D8372AB...
```

## Confirmed Non-Changes

- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- Original downloaded source files and PDFs were not modified.
- `graphite_ica_chapter1_rebuilt_v1.tex` was not modified after being copied to v2.
- No commit, push, merge, or branch operation was performed.

## Git Status Note

`git status` required one-time `safe.directory` override because the sandbox user differs from the repo owner. The check showed:

```text
?? Codex/results/graphite_ica_chapter1_rebuilt_v2_dual_closure.tex
```

Warnings about `C:\Users\lksz1/.config/git/ignore` permission were observed and not modified.

## Gate

Gate: `PASS_DUAL_CLOSURE_DECISION_RECORDED`

Status: PASS

## Next

If continuing Chapter 1 integration, the next phase should either:

1. update Claude-style manuscript scaffold with the same dual-closure hierarchy, or
2. perform a dedicated Plan A validation phase to test whether refs 6/7 can legitimately close the graphite self-consistent integral.

