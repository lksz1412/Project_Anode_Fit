# v7-08 NOTE

## Read Coverage

All four required source files were read head to tail before writing `v7-08.tex`.

| Source | Required role | Actual read coverage |
|---|---|---|
| `D:\Projects\Project_Anode_Fit\Claude\results\v7-00_spine\AUTHOR_BRIEF.md` | authoritative spec, highest priority | lines 1-64 |
| `D:\Projects\Project_Anode_Fit\Claude\results\v7-00_spine\v11_flowchart.md` | shared N0-N9 section spine | lines 1-79 |
| `D:\Projects\Project_Anode_Fit\Claude\results\v7-00_spine\Anode_Fit_v11_final.py` | canonical identifiers, signs, equations | lines 1-706; first terminal dump truncated around 307-374, so lines 300-374 were re-read separately |
| `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_Opus_v5.tex` | v5-only format/content reference | lines 1-1883; the tail 1731-1883 was re-read separately to verify the true end marker |

No v6 source was read or used.

## 10-Round Review Log

| Round | Chunk scheme | Lens | Defects found | Fixes applied |
|---|---|---|---|---|
| R1 | whole-document outline | structure vs `v11_flowchart.md` | Rendered section counter would have produced N1-N10 although headings said N0-N9. | Added `\setcounter{section}{-1}` before the first section; verified TOC shows N0-N9. |
| R2 | LaTeX compile chunk | LaTeX syntax | Undefined `\lo` and `\hi` macros in the working-grid equations. | Replaced them with `\mathrm{lo}` and `\mathrm{hi}`. |
| R3 | N0-N1 | logic and code progression | No remaining defect. `curve -> dqdv`, `I_abs`, C-rate, `V_n`, work grid, `T_work`, and `Cbg` order match v11. | No change. |
| R4 | N2-N4 | physical correctness | No remaining defect. `U_j(T)`, `dU_hys`, `U_j^d`, `w`, `w_eff`, and dispatch rules match v11. | No change. |
| R5 | N5-N6 equations | adversarial sign check | No remaining defect. `xi_eq = logistic[sigma_d(V-U)/w]`; derivative sign is separated from positive peak shape. | No change. |
| R6 | N7 | identifier vs v11 Python | No remaining defect. `chi_d`, `dH_a_eff`, `A`, `L_q`, `L_V`, direct `L_V` override, and `dVdq_qa` are represented. | No change. |
| R7 | N8 | causal-tail and charging inversion | No remaining defect. Charging branch uses `xi[::-1]` low-pass then `[::-1]`, and peak is `(xi_eq - xi_lagged)/L_V`. | No change. |
| R8 | figures only | figure orphan and TikZ text | No remaining defect. Four figures are introduced and referenced; TikZ node/axis text is ASCII English only. | No change. |
| R9 | final formula and staging table | G-usable implementation | No remaining defect. The final equation can be translated directly into v11 `dqdv`; `GRAPHITE_STAGING_LIT` values and constructor defaults are listed. | No change. |
| R10 | full pass | convergence and section bridge check | No defects found. R9 and R10 are consecutive zero-defect rounds, so the review criterion is met. | No change. |

## Sign Identifier Checklist

Checklist run against AUTHOR_BRIEF section 8 and `Anode_Fit_v11_final.py`.

| Item | Result |
|---|---|
| `U_j(T)=(-dH_rxn+T*dS_rxn)/F` and `Delta G=-F U` | Pass. See `eq:UjT`. |
| `xi_eq = logistic[sigma_d(V_n-U)/w]` with discharge `sigma_d=+1` and `V up -> xi up` | Pass. See `eq:xieq`. |
| `dxi/dV = sigma_d*xi*(1-xi)/w`; peak is positive and direction invariant | Pass. See `eq:dxidVsig` and `eq:eqpeakshape`. |
| `Delta U_hys >= 0`, `Omega <= 2RT -> 0`, branch center `+ 1/2*sigma_d*h_eta*gamma*Delta U_hys` | Pass. See `eq:dUhys` and `eq:Ubranch`. |
| `chi_d`: discharge `chi`, charge `1-chi`; `dH_a_eff=dH_a-chi_d*Omega` | Pass. See `eq:chidHeff`. |
| `partial ln L_q / partial V < 0` in activation-dominated tail | Pass. See `eq:dlnLdV`. |
| charging lattice inversion `xi[::-1] ... [::-1]` | Pass. See `eq:chargelowpass` and `fig:causaltail`. |
| polarization `V_n=V_app-sigma_d*|I|*R_n` | Pass. See `eq:polarization` and `eq:interpout`. |
| Code identifiers preserved where used: `curve`, `dqdv`, `func_U_j`, `func_dU_hys`, `func_U_branch`, `func_w`, `func_w_eff`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass`, `GRAPHITE_STAGING_LIT` | Pass. |

## Figure Inventory

All figures are new TikZ figures. No v5/v6 figure was reused, restored, or copied.

| Label | Placement | Purpose | Orphan status |
|---|---|---|---|
| `fig:codeflow` | N0 | Maps `curve -> dqdv -> V_work -> transition loop -> sum/interp` before the equations start. | Introduced and referenced. |
| `fig:hysbranch` | N3 | Shows the symmetric branch gap and opposite discharge/charge center shift. | Introduced and referenced. |
| `fig:logisticpeak` | N5 | Shows logistic `xi_eq` and the `xi(1-xi)` peak kernel used in N6. | Introduced and referenced. |
| `fig:causaltail` | N8 | Shows why charge must reverse the lattice before the causal filter. | Introduced and referenced. |

TikZ internal text check: all node/axis labels inside `tikzpicture` environments are ASCII English only.

## Build Status

- XeLaTeX found: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`.
- Build command run from `D:\Projects\Project_Anode_Fit\Claude\results\v7-08`: `xelatex -interaction=nonstopmode -halt-on-error v7-08.tex`.
- Final build: two clean passes after the section-counter patch.
- Final exit code: 0.
- PDF produced: `D:\Projects\Project_Anode_Fit\Claude\results\v7-08\v7-08.pdf`, 9 pages.
- Log check: no `!` LaTeX error, no undefined references, no fatal error, no emergency stop. Remaining warnings are hyperref PDF-string warnings for math in section titles and a Korean italic font fallback warning; they do not block PDF generation.

## Decision Queue

- Resolved during writing: the user wording and `AUTHOR_BRIEF` both require the shared `v11_flowchart.md` spine. Therefore the rendered section order is the literal v11 flowchart order N0 through N9: experiment input, polarization, `U_j(T)`, hysteresis, width, `xi_eq`, equilibrium peak, kinetic tail, causal tail, final sum/interpolation.
- No unresolved decision blocks remain.
