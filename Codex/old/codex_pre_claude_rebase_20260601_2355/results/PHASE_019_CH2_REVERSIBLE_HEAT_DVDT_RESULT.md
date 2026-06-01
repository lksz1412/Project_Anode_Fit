# Phase 019 Result - Chapter 2 Reversible Heat and dV/dT

## Summary

Chapter 2 was planned, written from zero-base, and reviewed through 10 logic passes.

Core result:

- The manuscript derives equilibrium `dV/dT` from fixed-`q` charge conservation.
- It defines `h_n^eq = (partial V_n,eq / partial T)_q` as the equilibrium entropy coefficient.
- It separates `h_n^eq` from finite-current `h_n^dyn` and apparent `h_n^app`.
- It connects Chapter 1 tail kernels to dynamic thermal response without treating tail features as reversible heat.
- It separates reversible heat from irreversible heat and leaves kinetic heat law details for Chapter 3/4.

## Created Files

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-29-chapter2-reversible-heat-dvdt-plan.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVIEW_10PASS.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVERSIBLE_HEAT_DVDT_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVERSIBLE_HEAT_DVDT_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVERSIBLE_HEAT_DVDT_HANDOVER.md`
- `D:\Projects\Project_Anode_Fit\Codex\work\verify_ch2_reversible_heat_dvdt_v1.ps1`

## Input Files and Read Coverage

Read or inspected in this phase:

- `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md`
- `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`
- `D:\Projects\Project_Anode_Fit\README.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_018_CH1_V5_V4_COMPARISON.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_dynamic_ver5.tex`

Coverage notes:

- Chapter 1 v5 was used as canonical equation/convention input.
- Old merged `ver.2` material was used only as a structure hint, not as equation authority.
- Chapter 2 staged manuscript was read in line chunks covering its full content before copying to the project results path. The copied final file was verified by SHA256.

## Main Equations Produced

Equilibrium charge balance:

```latex
Q_{\cell}q
=
Q_{\bg}(V_{n,\eqs},T)
+Q_p\Theta_{\eqs}(V_{n,\eqs},T)
```

Equilibrium entropy coefficient:

```latex
h_n^{\eqs}(q,T)
=
\left(\frac{\partial V_{n,\eqs}}{\partial T}\right)_q
=
-\frac{
\left(\partial Q_{\bg}/\partial T\right)_V
+Q_p\left(\partial\Theta_{\eqs}/\partial T\right)_V}
{C_{\bg}(V_{n,\eqs},T)
+Q_p\left(\partial\Theta_{\eqs}/\partial V\right)_T}
```

Reversible heat:

```latex
\dot Q_{\rev,n}=-I_sT h_n^{\eqs}
```

Dynamic apparent derivative:

```latex
h_n^{\app}
=
h_n^{\dyn}
+
\left(\partial\eta_n/\partial T\right)_{q,\calH}
```

Tail-kernel temperature derivative:

- Peak-aligned derivative uses `s=q-q_a`.
- Fixed absolute `q` derivative includes the extra `q_a(T,psi)` chain-rule term.

## Verification Commands

Static verifier:

```powershell
& 'D:\Projects\Project_Anode_Fit\Codex\work\verify_ch2_reversible_heat_dvdt_v1.ps1' `
  -TexPath 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex' |
  ConvertTo-Json -Depth 5
```

High-risk string search:

```powershell
Select-String -Path 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex' `
  -Pattern 'PHASE|Phase|Codex|audit|Ralph|fallback|solver|\\xi|0 -> 1|step-function|회귀' `
  -CaseSensitive
```

## Verification Evidence

Final static result:

```text
Lines: 932
SHA256: 21BF4933DE5D332B9EF61BC5F10645F11254BF11811C68855496FA5A2C5B6F63
BeginCount: 61
EndCount: 61
OpenBraceCount: 740
CloseBraceCount: 740
LabelCount: 76
RefCount: 21
MissingRefs: []
CiteCount: 3
BibitemCount: 5
MissingCites: []
Xelatex: NOT_FOUND
```

High-risk search:

```text
No matches for PHASE, Phase, Codex, audit, Ralph, fallback, solver, \xi, ASCII 0 -> 1, step-function, or 회귀.
```

## Repairs Made During Review

- Removed old-coordinate contamination from a convention sentence.
- Removed process-version wording from the manuscript body.
- Added a free-energy/entropy sign derivation with `sigma_V` and `sigma_I`.
- Added missing tail-kernel temperature derivative branch for fixed absolute `q` when `q_a(T,psi)` shifts.

## External Source Verification

Used web lookup only to verify citation metadata:

- Bernardi, Pawlikowski, and Newman, `A General Energy Balance for Battery Systems`, DOI `10.1149/1.2113792`.
- Thomas and Newman, `Thermal Modeling of Porous Insertion Electrodes`, DOI `10.1149/1.1531194`.

## Remaining Items

- PDF was not generated because `xelatex` is not installed or not on PATH.
- No fitting or solver implementation was attempted, by scope.
- Chapter 3 can now start from the Chapter 2 handoff equations.

## Gate Result

PASS for the requested Chapter 2 plan, manuscript, and 10-pass logic review.

