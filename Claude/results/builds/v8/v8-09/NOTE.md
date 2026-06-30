# v8-09 NOTE

## Read Coverage

All required sources were read directly in this session before writing `v8-09.tex`.

| Source | Required role | Direct read coverage |
|---|---|---|
| `Claude/results/v8-00_spine/AUTHOR_BRIEF_v8.md` | authoritative spec | lines 1-63, full |
| `Claude/results/v7-11/v7-11.tex` | preserve layout/order/boxes/signs/tables | lines 1-889, full |
| `Claude/docs/graphite_ica_ch1_Opus_v5.tex` | derivation source | lines 1-1883, full |
| `Claude/results/v7-00_spine/Anode_Fit_v11_final.py` | Python 1:1 ground truth | lines 1-706, full |
| `Claude/results/v7-00_spine/v11_flowchart.md` | N0-N9 spine | lines 1-89, full |

Project root `AGENTS.md` was checked first and was not present. The global instructions supplied in the user message were used.

## Output Files

| File | Status |
|---|---|
| `Claude/results/v8-09/v8-09.tex` | self-contained XeLaTeX source |
| `Claude/results/v8-09/v8-09.pdf` | built by XeLaTeX |
| `Claude/results/v8-09/NOTE.md` | this record |

Auxiliary build files (`.aux`, `.log`, `.out`, `.toc`) were generated only inside `Claude/results/v8-09/`.

## Derivation Map

| Required stage | v8-09 location | Restored derivation chain |
|---|---|---|
| 1. `U_j(T)` | `sec:center`, `eq:gmu_bridge`-`eq:Uj` | `G=H-TS`, `mu=dG/dn`, electrochemical equilibrium, `Delta G=-sFU`, `Delta G=Delta H-TDelta S`, algebra to box |
| 2. `w_j` | `sec:width`, `eq:w_depart`-`eq:wbase` | ideal lattice-gas logit, multiplicity `n_j`, comparison to logistic denominator, `w_j=n_jRT/F` |
| 3. `xi_eq` logistic | `sec:width`, `eq:xieq_rates`-`eq:xieq` | forward/reverse rates, detailed-balance ratio, stationary condition, logit solve, logistic box |
| 4. equilibrium peak | `sec:eqpeak`, `eq:charge_v809`-`eq:eqpeak` | conservation law, trajectory derivative, logistic derivative identity, chain rule, positive peak box |
| 5. `Delta U_hys` | `sec:hys`, `eq:gprime_v809`-`eq:dUhys` | regular-solution `g`, first/second derivatives, quadratic roots, spinodal endpoint substitution, log/artanh reduction, box |
| 6. branch center | `sec:hys`, `eq:hyssym_v809`-`eq:Ubranch` | spinodal endpoint average, cancellation of log and interaction terms, symmetric one-DOF branch center, box |
| 7. `L_q`/`L_V` | `sec:lag`, `eq:Lq`-`eq:LV` | lag ODE, integrating factor, general memory solution, rate sum, Eyring substitution, log terms, voltage-axis conversion |
| 8. cut affinity `A` | `sec:lag`, `eq:zcut_source`-`eq:Acut` | logistic derivative 5% cutoff, `z_cut=2 arcosh sqrt(20)`, cap rule, operational constant distinction |
| 9. `Delta H_a^eff` | `sec:lag`, `eq:A_with_Omega_v809`-`eq:dHeff` | interaction term split from affinity, deep-tail limit, direction-specific `chi_d`, enthalpy absorption, box |
| 10. `L_V` causal tail | `sec:tail`, `eq:lag_ode_v809`-`eq:reversal` | continuous low-pass ODE, one-step solution, discrete recurrence, peak shape from ODE, charge grid reversal |
| 11. final sum | `sec:sum`, `eq:sum_depart_v809`-`eq:sum` | conservation law, derivative, branch-selected `peak_shape`, linear weighted sum, interpolation note |

No result expression from v11 was intentionally changed. One inherited v7-11 staging figure label that made discharge progress decrease was corrected to discharge `xi_j:0->1` to satisfy the AUTHOR_BRIEF sign convention.

## Sign Audit

| Item | v8-09 status |
|---|---|
| `U_j(T)=(-Delta H+TDelta S)/F`, `Delta G=-FU` | explicit in `eq:Uj`; signbox S1 retained |
| `xi_eq=logistic[sigma_d(V-U)/w]`, discharge `V up -> xi up` | explicit in `eq:xieq`; signbox S2 retained |
| `dxi/dV` peak positive/direction invariant | explicit in `eq:eqpeak`; signbox S3 retained |
| `Delta U_hys>=0`, `Omega<=2RT -> 0`, branch `+-1/2 sigma_d` | explicit in `eq:dUhys`, `eq:Ubranch`; signbox S4 retained |
| `chi_d` discharge `chi`, charge `1-chi`; `Delta H_a^eff=Delta H_a-chi_d Omega` | explicit in `eq:chid`, `eq:dHeff`; signbox S5 retained |
| `partial ln L_q / partial V`: operational `0`, `<0` only physical motivation | explicit in N7 prose and signbox S6 |
| tail charge grid reversal, charge dQ/dV mirror positive | explicit in `eq:reversal`; signbox S7 retained |
| polarization `V_n=V_app-sigma_d |I| R_n`, discharge measured above internal | explicit in `eq:vn`; signbox S8 retained |

## Figure Inventory

| Label | Origin | Status |
|---|---|---|
| `fig:spine` | v7-11 derived | retained |
| `fig:staging` | v7-11 derived, one sign label corrected | retained/improved |
| `fig:hysloop` | v7-11 derived | retained |
| `fig:logistic` | v7-11 derived | retained |
| `fig:memorykernel` | v8-09 new | added for lag ODE/general solution |
| `fig:reversal` | v7-11 derived | retained |

Figure audit: all six figure labels have in-text `\ref{...}` references. A TikZ-body scan found no Hangul inside figure drawing text; captions remain Korean where useful.

## 10-Round Self-Review Log

| Round | Lens | Result |
|---|---|---|
| R1 | Source coverage | Clean: all five requested files read fully; project `AGENTS.md` absent |
| R2 | Layout/order | Clean: section sequence remains `N0 -> N9` plus sign audit; v7-11 tables retained |
| R3 | G-derive | Defect found: inherited v7 logistic/w/spinodal/Lq jumps were too compressed; expanded with intermediate equations |
| R4 | Sign convention | Defect found: staging figure made discharge progress decrease; corrected to `xi_j:0->1` |
| R5 | Identifier/code 1:1 | Clean: v11 identifiers `func_U_j`, `func_dU_hys`, `func_U_branch`, `func_ksi_eq`, `func_L_q`, `_resolve_lag_length`, `_causal_lowpass`, `dqdv_work`, `np.interp` retained |
| R6 | Figure/orphan | Defect found: new memory figure needed explicit body reference; added prose reference before the figure |
| R7 | Scope/source restriction | Defect found: inherited header comments mentioned a forbidden prior-version source; removed from `v8-09.tex` |
| R8 | Completeness/11 stages | Clean: all 11 AUTHOR_BRIEF stages mapped to visible equations and final results |
| R9 | Build/log | Clean for fatal errors: XeLaTeX exit 0; settled PDF generated. Remaining warnings are font substitutions, hyperref PDF-string removals, and inherited minor overfull/underfull boxes |
| R10 | Final mixed lens | Clean: no forbidden prior-version mentions in `v8-09.tex`, no unreferenced figures, no unresolved references after stabilizing pass, sign audit 8/8 present |

Convergence: R9 and R10 were consecutive clean rounds for required gates.

## Build Instructions

From `D:\Projects\Project_Anode_Fit\Claude\results\v8-09`:

```powershell
xelatex -interaction=nonstopmode v8-09.tex
xelatex -interaction=nonstopmode v8-09.tex
```

In this session, XeLaTeX was available at:

```text
C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe
```

Build record: two requested passes plus one stabilizing pass were run. Final pass exit code was 0 and produced `v8-09.pdf` (20 pages). The log contains non-fatal font/hyperref box warnings and MiKTeX local logging/update notices, but no LaTeX fatal errors or unresolved-reference rerun warnings after the final pass.

## Decision Queue

None blocking. The only substantive editorial correction made beyond derivation expansion was the discharge progress label in `fig:staging`, required by the AUTHOR_BRIEF sign convention.
