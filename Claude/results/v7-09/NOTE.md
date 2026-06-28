# v7-09 NOTE

## Read Coverage
- `Claude/results/v7-00_spine/AUTHOR_BRIEF.md`: READ_FULL lines 1-75.
- `Claude/results/v7-00_spine/v11_flowchart.md`: READ_FULL lines 1-89.
- `Claude/results/v7-00_spine/Anode_Fit_v11_final.py`: READ_FULL lines 1-706.
- `Claude/docs/graphite_ica_ch1_Opus_v5.tex`: READ_FULL lines 1-1883.

## 10R Review Log
- R1 structure/build chunk: found missing `\abs`, `\lo`, `\hi` macros; fixed before continuing.
- R2 macro/equation chunk: found missing v5-style `\eq` macro used in subscripts; fixed.
- R3 section-spine chunk: found LaTeX counter rendered N1-N10 instead of N0-N9; fixed with pre-section counter reset.
- R4 layout/equation chunk: found overfull boxed `L_q/L_V` equations; split equations and rebuilt.
- R5 generated-TOC chunk: PASS, `v7-09.toc` shows N0 through N9 in order.
- R6 sign-chain chunk: PASS, polarization, logistic, derivative, hysteresis, `chi_d`, `dH_a_eff`, low-pass reversal, and interpolation signs match v11.
- R7 identifier chunk: PASS, code-facing names `func_U_j`, `func_dU_hys`, `func_U_branch`, `func_L_q`, `func_chi_d`, `func_dH_a_eff`, `_causal_lowpass`, `dqdv_work`, `peak_shape`, `occ_lagged`, `grid_step`, and `min_lag_grid_steps` are traceable.
- R8 figure chunk: PASS, six new TikZ figures, all labelled and captioned, zero Korean characters inside `tikzpicture`.
- R9 scope/forbidden chunk: PASS, no v6 reference, no external `\input` or `\include`, source files untouched.
- R10 final-build chunk: PASS, two-pass `xelatex -interaction=nonstopmode -halt-on-error v7-09.tex` completed with exit code 0 and generated `v7-09.pdf`.

## Sign Checklist
- PASS `U_j(T)=(-dH_rxn+T dS_rxn)/F`: equation `eq:Uj`, matches `func_U_j`.
- PASS `ksi_eq=logistic[sigma_d(V-center)/w]`: equation `eq:ksieq`, discharge increases with `V`, charge mirrors by `sigma_d=-1`.
- PASS `dksi/dV=sigma_d ksi(1-ksi)/w` and positive peak: equations `eq:dxidv` and `eq:absdxidv`.
- PASS `dU_hys>=0`, `Omega<=2RT -> 0`, branch center `+ 1/2 sigma_d h_eta gamma dU_hys`: equations `eq:dUhys`, `eq:Ubranch`, `eq:center`.
- PASS `chi_d`: discharge `chi`, charge `1-chi`: equation `eq:chid`.
- PASS `dH_a_eff=dH_a-chi_d Omega`: equation `eq:dHeff`.
- PASS `partial ln L_q / partial V < 0`: equation `eq:lnLq` has `-chi_d A/(RT)`, with larger cutoff affinity shortening `L_q`.
- PASS causal tail charge reversal: equations `eq:dislowpass`, `eq:chglowpass`, `eq:tailpeak`; charge uses `[::-1]` then `[::-1]`.
- PASS polarization `V_n=V_app-sigma_d |I| R_n`: equation `eq:polar`.

## Figures
- `fig:spine`: v11 node order and calculation flow.
- `fig:polar`: polarization sign convention.
- `fig:logistic`: logistic state and bell factor.
- `fig:hys`: hysteresis branch-center split.
- `fig:lowpass`: causal low-pass and charge grid reversal.
- `fig:sum`: transition summation into total dQ/dV.

## Build Result
- `xelatex` was available at `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`.
- Final two-pass build command: `xelatex -interaction=nonstopmode -halt-on-error v7-09.tex`.
- Result: PASS, exit code 0, `v7-09.pdf` generated with 9 pages.
- Nonfatal warnings remaining: hyperref PDF-string warnings for math in section titles and font italic substitution warnings; no LaTeX errors, no undefined references, no rerun request, no overfull boxes in the final log.

## Decision Queue
- None.
