# v8-07 NOTE

## Read Coverage

All requested sources were read head to tail before LaTeX writing.

| Source | Lines read | Status |
|---|---:|---|
| `Claude/results/v8-00_spine/AUTHOR_BRIEF_v8.md` | 63 | READ_FULL |
| `Claude/results/v7-11/v7-11.tex` | 889 | READ_FULL; prompt said 879, current file has 889 |
| `Claude/docs/graphite_ica_ch1_Opus_v5.tex` | 1883 | READ_FULL |
| `Claude/results/v7-00_spine/Anode_Fit_v11_final.py` | 706 | READ_FULL |
| `Claude/results/v7-00_spine/v11_flowchart.md` | 89 | READ_FULL |
| `Codex/AGENTS.md` | full file | Project instruction layer read |

## Steps Restored

The v7-11 section order, result boxes, equation identifiers, tables, and five figures were preserved. The derivation expansion was added around the existing results, using v5 as derivation source and v11 as symbol/sign authority.

| Brief step | Restored numbered chain in `v8-07.tex` |
|---|---|
| 1. `U_j(T)` | `eq:UjderiveA` -> `eq:UjderiveB` -> `eq:eqcond` -> `eq:UjderiveC` -> `eq:Uj` |
| 2. `w_j` | `eq:wderiveA` -> `eq:wderiveB` -> `eq:wbase`; `eq:weff` retained |
| 3. `xi_eq logistic` | `eq:xieqderiveA` -> `eq:xieqderiveB` -> `eq:xieqderiveC` -> `eq:xieqderiveD` -> `eq:xieq` |
| 4. Equilibrium peak | `eq:eqpeakderiveA` -> `eq:eqpeakderiveB` -> `eq:eqpeakderiveC` -> `eq:eqpeak` |
| 5. `Delta U_hys` | `eq:gxi` -> `eq:gprime_v8` -> `eq:gpp_v8` -> `eq:spinodalquad` -> `eq:spinodal` -> `eq:hyssub_v8` -> `eq:dUhysderive` -> `eq:dUhys` |
| 6. Branch center | `eq:Ubranchderive` -> `eq:Ubranch`; `eq:center` retained |
| 7. `L_q` | `eq:LqderiveA` -> `eq:LqderiveB` -> `eq:Lq`; `eq:LqfullderiveA` -> `eq:LqfullderiveB` -> `eq:Lqfull` |
| 8. Cut affinity `A` | `eq:AcutderiveA` -> `eq:AcutderiveB` -> `eq:Acut` |
| 9. `Delta H_a^eff` | `eq:chidderive` -> `eq:chid` -> `eq:dHeffderiveA` -> `eq:dHeffderiveB` -> `eq:dHeff` |
| 10. `L_V` and causal tail | `eq:LVderive` -> `eq:LV`; `eq:lowpassderiveA` -> `eq:lowpassderiveB` -> `eq:lowpass`; `eq:peakshapederiveA` -> `eq:peakshapederiveB` -> `eq:peakshape`; `eq:reversal` retained |
| 11. Summation | `eq:sumderiveA` -> `eq:sumderiveB` -> `eq:sum` |

## 8 Sign Conventions

1. `U_j(T)=(-Delta H+T Delta S)/F`, with `Delta G=-F U` in the discharge convention.
2. `xi_eq=logistic[sigma_d(V-U)/w]`; discharge has `sigma_d=+1`, so increasing `V` increases delithiation progress.
3. `d xi/dV` changes sign with direction, but the peak shape uses the positive magnitude `xi(1-xi)/w`.
4. `Delta U_hys >= 0`; if `Omega <= 2RT`, the hysteresis gap is zero; branch center uses `+/- 1/2 sigma_d`.
5. `chi_d=chi` for discharge and `chi_d=1-chi` for charge; `Delta H_a^eff=Delta H_a-chi_d Omega`.
6. `partial ln L_q / partial V < 0` is a physical motivation for the cut rule; operational derivative is zero after cut-affinity freezing.
7. Charge tail uses grid reversal `xi[::-1]... [::-1]`; charge `dQ/dV` remains the positive mirror.
8. Polarization is `V_n=V_app-sigma_d |I| R_n`; discharge measured `V_app` is above thermodynamic `V_n`.

## Figure Origin

| Figure | Origin | Status |
|---|---|---|
| `fig:spine` | v7-11 lineage | retained |
| `fig:staging` | v7-11 lineage | retained |
| `fig:hysloop` | v7-11 lineage | retained |
| `fig:logistic` | v7-11 lineage | retained |
| `fig:reversal` | v7-11 lineage | retained |

No additional v8-only figure was added. The user instruction allowed new figures only if useful; the five retained figures already cover the code spine, staging, spinodal overrun, logistic derivative, and causal reversal without introducing orphan risk. Automated check: all five `fig:*` labels are referenced once; no Korean text appears inside TikZ picture bodies.

## Self-Review Log

| Round | Lens | Result |
|---|---|---|
| R1 | Structure | 1 defect found and fixed: copied header comments referenced forbidden prior version context. Removed those comments; section order N0-N9, sign-check section, tables, and boxes preserved. |
| R2 | Algebra / G-derive | 0 open defects after checking `G -> mu -> Delta G -> U`, spinodal quadratic, `artanh`, integrating-factor, and `L_q` chains. |
| R3 | Symbol | 0 defects: symbols match v11 identifiers (`sigma_d`, `V_n`, `U_j`, `w_j`, `xi_eq`, `A`, `chi_d`, `dH_a_eff`, `L_q`, `L_V`, `peak_shape`). |
| R4 | Sign | 0 defects: all eight sign conventions listed above are represented in text and sign-check section. |
| R5 | Completeness | 0 defects: all 11 AUTHOR_BRIEF Section 3 chains have numbered equations and converge to the preserved v7-11 result expressions. |
| R6 | Orphan | 0 defects: all five figure labels are referenced; no new orphan figure introduced; no `input/include`. |
| R7 | Box-link | 0 defects: every preserved boxed result has preceding starting equation plus intermediate equations; result labels retained. |
| R8 | Notation | 0 defects: `mathcal A` cut is separated from local derivative motivation; `sigma_d` and `s` roles remain distinct where needed. |
| R9 | Box fidelity | 0 defects: boxed results remain v7-11/v11-compatible; no result formula changed. |
| R10 | Overall | 0 defects: final scan shows 10 boxed results, 5 figures, 4 tables, 0 forbidden prior-version tokens, 0 `input/include`, 0 Korean text inside TikZ internals. |

Convergence criterion met: R9 and R10 were two consecutive zero-defect rounds.

## Build Result

Fresh command run with output redirected outside the project:

```powershell
xelatex -interaction=nonstopmode -halt-on-error -output-directory=<temp-build-dir> v8-07.tex
```

Executed three passes because labels changed after the first pass. Final result: exit codes `0,0,0`, PDF produced in temp at `C:\Users\lksz1\AppData\Local\Temp\codex_v8_07_xelatex_fresh_66c5bd86823d4b2488320afe37cdb266\v8-07.pdf` (20 pages). No PDF or auxiliary build files were left in `Claude/results/v8-07` because the requested project outputs were `v8-07.tex` and `NOTE.md`.

Final log check: no LaTeX errors, no undefined references, no undefined citations, no rerun request. Remaining warnings are font-shape substitutions and minor overfull boxes inherited from dense tables/inline code.
