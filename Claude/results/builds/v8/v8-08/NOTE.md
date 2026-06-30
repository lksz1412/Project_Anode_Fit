# v8-08 Note

## Full-read confirmation

Before creating or editing any v8-08 output, I read the requested source items in full:

- `Claude/results/v8-00_spine/AUTHOR_BRIEF_v8.md`: lines 1-63.
- `Claude/results/v7-11/v7-11.tex`: lines 1-889.
- `Claude/docs/graphite_ica_ch1_Opus_v5.tex`: lines 1-1883.
- `Claude/results/v7-00_spine/Anode_Fit_v11_final.py`: lines 1-706.
- `Claude/results/v7-00_spine/v11_flowchart.md`: lines 1-89.

The user listed four source items; item 4 contains two physical files, so five physical files were read.

## 10 self-review rounds

1. Source-priority pass, chunked by requested file: confirmed `AUTHOR_BRIEF_v8.md` is highest priority and v7-11 is the preservation target.
2. v7-11 section-order pass, chunked by LaTeX `\section`: v8-08 has the same 10 sections in the same order.
3. Result-box pass, chunked by `eq:` labels: v7-11 and v8-08 both have 25 unique equation labels; missing `[]`, extra `[]`.
4. Boxed-result pass, chunked by `\boxed`: v7-11 and v8-08 both have 10 boxed results.
5. Figure pass, chunked by figure environment: all 5 v7-11 candidate figures were retained, one v8-08 figure was added, all 6 figures have origin tags and body citations.
6. Forbidden-content pass, chunked by keyword scan: no `v6`, no TODO/TBD, no Korean one-line-jump trigger phrases, and no malformed `\\quad` remained.
7. Derivation pass, chunked by AUTHOR_BRIEF section 3 chains: all 11 required derivation chains are visible with starting relation, algebra, at least one intermediate step, and boxed/result equation.
8. Sign pass, chunked by the 8 sign-audit items: the v11 sign conventions and the v7-11 sign-audit structure were preserved.
9. LaTeX environment pass, chunked by environment type: `document`, `figure`, `table`, `longtable`, `equation`, `derivebox`, `keybox`, `codebox`, `signbox`, `verifybox`, and `align` environments are balanced.
10. Build/log pass, chunked by XeLaTeX error class: fixed hard errors found during compile attempts, reran until XeLaTeX exited 0 with no fatal error, undefined reference, or rerun request.

Findings fixed during review: malformed display math near the `U_j(T)` derivation, malformed `\\quad`, undefined math shorthands such as `\cut`, `\cap`, `\grid`, `\lag`, and a missing explicit N6 equilibrium-peak derivation block.

## Derivation restoration account

The v8-08 draft restores the AUTHOR_BRIEF section 3 derivation chains while preserving v7-11 result identifiers and boxed equations:

1. `U_j(T)`: Gibbs free energy -> electrochemical equilibrium -> `Delta G = -F U` -> boxed `U_j(T)=(-Delta H+T Delta S)/F`.
2. `w_j`: ideal lattice-gas chemical potential -> linearized voltage scale -> boxed `w_j=n_j RT/F` plus effective-width branch.
3. `xi_eq` logistic: detailed balance rate ratio -> occupancy odds -> logistic denominator -> boxed direction-aware logistic.
4. Equilibrium peak: logistic derivative -> chain rule -> positive ICA peak -> boxed `Q_j xi_eq(1-xi_eq)/w_j`.
5. `Delta U_hys`: regular-solution free energy -> spinodal condition -> two spinodal points -> boxed hysteresis gap.
6. Branch center: spinodal gap -> half-gap split -> gamma and partial-cycle factors -> boxed branch center.
7. `L_q`: relaxation ODE in q -> linear relaxation rate -> detailed-balance rate sum -> boxed q-axis lag length.
8. Cut affinity `A`: logistic derivative cutoff -> `cosh^2` cutoff equation -> `z_cut` -> boxed min-capped affinity.
9. `Delta H_a_eff`: regular-solution affinity -> barrier term -> direction-dependent transfer coefficient -> boxed effective activation enthalpy.
10. `L_V` and causal tail: q-lag to voltage-lag conversion -> causal lowpass solution -> peak-shape result -> charge-grid reversal.
11. Final sum: transition-wise peak shape -> positive capacity contribution -> background addition -> boxed full `dQ/dV` sum.

## Sign audit

- `U_j(T)=(-Delta H+T Delta S)/F` and `Delta G=-F U`: preserved.
- Logistic sign: discharge uses `sigma_d=+1`, so increasing voltage increases `xi_eq`.
- Peak sign: `d xi/dV = sigma_d xi(1-xi)/w`; plotted ICA peak uses the positive magnitude.
- Hysteresis sign: `Delta U_hys >= 0`, collapses at `Omega <= 2RT`, branch center uses `+/- 1/2 sigma_d`.
- Transfer coefficient: discharge uses `chi`, charge uses `1-chi`; `Delta H_a_eff = Delta H_a - chi_d Omega`.
- Lag monotonicity: `partial ln L_q / partial V < 0` is retained as physical motivation; code-level cut affinity is frozen per transition, so its operational derivative is 0.
- Tail direction: charge reverses the grid before and after the causal lowpass, preserving a positive mirrored peak shape.
- Polarization: `V_n=V_app-sigma_d |I| R_n`; for discharge the measured voltage is above the internal voltage.

## Figure list

- `fig:spine`: [Origin: v7-11 candidate], retained and cited in the introduction.
- `fig:staging`: [Origin: v7-11 candidate], retained and cited in notation/staging discussion.
- `fig:hysloop`: [Origin: v7-11 candidate], retained and cited in the hysteresis section.
- `fig:logistic`: [Origin: v7-11 candidate], retained and cited in the width/logistic section.
- `fig:reversal`: [Origin: v7-11 candidate], retained and cited in the tail/reversal section.
- `fig:derivechain`: [Origin: v8-08 new], new figure with English ASCII internal labels, cited in the introduction.

## Build result

`xelatex` was available at `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`.

I ran XeLaTeX repeatedly while fixing hard errors, then completed a final rerun:

```text
Output written on v8-08.pdf (21 pages).
```

Final log scan found no fatal `!` errors, no `Undefined control sequence`, no undefined references, and no cross-reference rerun request. Remaining nonfatal warnings are font substitutions, hyperref PDF-string warnings for math in bookmarks, underfull/overfull boxes, and MiKTeX local log/update/security notices.

Generated outputs inside this directory include `v8-08.tex`, `v8-08.pdf`, LaTeX auxiliary files, and this `NOTE.md`.
