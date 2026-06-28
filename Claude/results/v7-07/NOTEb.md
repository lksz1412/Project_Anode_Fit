# NOTEb -- v7-07b

## Read Coverage

- READ_FULL: `Claude/results/v7-07/v7-07.tex` lines 1-703.
- READ_FULL: `Claude/results/v7-00_spine/Anode_Fit_v11_final.py` lines 1-706.
- READ_FULL: `Claude/results/v7-00_spine/v11_flowchart.md` lines 1-89.
- READ_FULL: `Claude/results/v7-00_spine/AUTHOR_BRIEF.md` lines 1-75.
- `Claude/results/v7-07/REVIEW1.md` was not read, per instruction.

## Change List

- C1 restored the missing `+` in `V_{\eq,j}(\xi)` before the interaction term and expanded the spinodal endpoint evaluation through `V_{\eq,j}(\xi_-)-V_{\eq,j}(\xi_+) = \Delta U_j^\hys`.
- C2 reserved `A_j` for the v11 per-transition cut affinity `min(z_cut*n*RT, A_cap_RT*RT)` and renamed voltage dependence to driving force `\Phi_j(V)`.
- C3 replaced direct formula transcription with stepwise derivations for `\Delta U^\hys`, `L_q`, and the causal lowpass recursion; also restored the missing `+` in the memory integral.
- Added final sign-regression self-test conditions in the TeX body.

## AUTHOR_BRIEF Section 8 Sign Audit

- 1 PASS: `U_j(T)=(-Delta H+T Delta S)/F` preserved.
- 2 PASS: `xi_eq=logistic[sigma_d(V_n-U)/w]`; discharge `sigma_d=+1` gives `V` up -> delithiation up.
- 3 PASS: `d xi/dV=sigma_d xi(1-xi)/w`; peak magnitude remains positive.
- 4 PASS: `Delta U_hys >= 0`, `Omega<=2RT -> 0`, branch centers split by `+/- 1/2 sigma_d h_eta gamma Delta U_hys`.
- 5 PASS: `chi_d=chi` for discharge and `1-chi` for charge; `Delta H_a_eff=Delta H_a-chi_d Omega`.
- 6 PASS: voltage dependence is driving force only; along progress direction the barrier term shortens `L_q`.
- 7 PASS: charge lowpass uses reversed grid and returns positive mirror-type peak.
- 8 PASS: `V_n=V_app-sigma_d|I|R_n`; discharge is delithiation/oxidation and has `V_app > V_n`.

## Sign Regression Self-Test

- Command: inline Python import of `Anode_Fit_v11_final.py`.
- Results: `POLARIZATION_OK=True`, `HYSTERESIS_OK=True`, `ACUT_DIRECTION_INDEPENDENT_OK=True`, `FACADE_CORE_OK=True`, `OVERALL_SIGN_REGRESSION_OK=True`.

## Build State

- BUILD: pass.
- Ran `xelatex -interaction=nonstopmode v7-07b.tex` twice as requested, one extra pass because pass 2 still reported changed labels, and one final verification pass.
- Final output: `v7-07b.pdf`, 13 pages, 234100 bytes.
- Final log check: no fatal/error/undefined-reference/changing-label patterns. Remaining non-fatal messages are font substitutions, hyperref PDF-string cleanup, underfull boxes, and MiKTeX local log/update notices.
