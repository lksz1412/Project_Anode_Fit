# v8-09b patch note

## Read coverage before edit

| Source file | Read range | Status |
|---|---:|---|
| `Claude/results/v8-09/v8-09.tex` | 1-1189 | PASS |
| `Claude/results/v7-00_spine/Anode_Fit_v11_final.py` | 1-706 | PASS |
| `Claude/results/v7-11/v7-11.tex` | 1-889 | PASS |
| `Claude/results/v8-00_spine/AUTHOR_BRIEF_v8.md` | 1-63 | PASS |

`REVIEW1.md` was not read.

## Patch line ranges

| Patch | File/range | Status |
|---|---|---|
| Patch 1: `L_V` limit physics corrected | `v8-09b.tex` 927-940 | PASS |
| Patch 2: `w_eff` midpoint step added (`sF dV/dxi = 4Fw`) | `v8-09b.tex` 543-556 | PASS |
| Patch 3: body citations added for existing bib keys | `v8-09b.tex` 108, 367, 730 | PASS |
| Patch 4: 8 sign items checked and recorded below | `NOTEb.md` sign table | PASS |
| Patch 5: Regression self-test paragraph expanded to 5 checks | `v8-09b.tex` 1169-1192 | PASS |

## Sign table

| # | Sign item | Formula/range checked | Result |
|---:|---|---|---|
| 1 | `U_j(T)=(-Delta H+T Delta S)/F`, with `Delta G=-sFU` | `v8-09b.tex` 321-345, 1149-1150 | PASS |
| 2 | `xi_eq=logistic[sigma_d(V-U)/w]`; discharge `V up -> xi up` | `v8-09b.tex` 584-594, 605-607, 1151-1152 | PASS |
| 3 | `dxi/dV=sigma_d xi(1-xi)/w`; peak is positive and direction-invariant | `v8-09b.tex` 662-676, 679-680, 1153-1154 | PASS |
| 4 | `Delta U_hys >= 0`, `Omega <= 2RT -> 0`, branch center `+- 1/2 sigma_d` | `v8-09b.tex` 439-462, 446-447, 1155-1156 | PASS |
| 5 | `chi_d=chi` discharge, `1-chi` charge; `Delta H_a_eff=Delta H_a-chi_d Omega` | `v8-09b.tex` 766-793, 1157-1158 | PASS |
| 6 | `partial ln L_q / partial V = 0` operationally because `A` is frozen; `<0` is only motivation | `v8-09b.tex` 827-844, 1159-1162 | PASS |
| 7 | Charge tail uses grid reversal and keeps positive mirror dQ/dV | `v8-09b.tex` 947-958, 1163-1164 | PASS |
| 8 | Polarization `V_n=V_app-sigma_d |I| R_n` | `v8-09b.tex` 259-269, 1165 | PASS |

## Compiler status

`xelatex` is installed (`MiKTeX 25.12.0.0`), but compile was not run because it would write side artifacts such as `.aux`, `.log`, `.out`, `.toc`, and `.pdf`. The user constraint for this patch was to write only `v8-09b.tex` and `NOTEb.md`.

Read-only verification performed:
- Located new citations for `bazant2013`, `dreyer2010`, and `eyring1935` in body text.
- Located Patch 1, Patch 2, and Patch 5 line ranges in `v8-09b.tex`.
