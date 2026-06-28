# NOTEb — v7-09b augmentation log

## Read coverage

- `Claude/results/v7-09/v7-09.tex`: READ_FULL, lines 1-554.
- `Claude/results/v7-00_spine/Anode_Fit_v11_final.py`: READ_FULL, lines 1-706.
- `Claude/results/v7-00_spine/v11_flowchart.md`: READ_FULL, lines 1-89.
- `Claude/results/v7-00_spine/AUTHOR_BRIEF.md`: READ_FULL, lines 1-75.
- `Claude/results/v7-09/REVIEW1.md`: not read, per instruction.

## Augmentation locations in `v7-09b.tex`

- (A) G-usable additions:
  - Constructor defaults table: lines 157-183.
  - Expanded staging table with `dH_a`, `dVdq_qa`, `dS_a`: lines 232-246.
- (B) Added derivations:
  - Logistic `xi_eq` from chemical-potential equality and Fermi-Dirac analogy: lines 252-267.
  - Spinodal `delta_U_hys` from regular-solution double-well: lines 353-379.
  - Physical `L_q` motivation with integral memory kernel: lines 429-452.
- (C) `fig:spine` node labels now include section numbers: lines 89-98.
- (D) Explicit `q=Q/Q_cell` definition and propagation into `L_q`: lines 130-136 and 429-446.
- (E) v11 `A` / `L_q` plateau clarification: lines 500-507.
- (F) Discharge polarization sign convention strengthened: line 193.

## Compile status

- `xelatex` found on PATH: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`.
- Ran from `Claude/results/v7-09`.
- Required 2-pass compile completed with exit code 0.
- One extra stabilization pass was run because pass 2 reported changed labels.
- Final pass: no LaTeX errors, no undefined-reference warning, PDF produced in temp output directory `C:\Users\lksz1\AppData\Local\Temp\codex_v7_09b_xelatex\v7-09b.pdf` with 11 pages.
- Non-blocking warnings remained: hyperref removed math tokens from a PDF bookmark; font italic shapes fell back to upright for `UnBatang`/`D2Coding`; MiKTeX printed local log/update/security warnings.

## Sign-convention self-test

All requested sign checks passed against `Anode_Fit_v11_final.py`.

- `eta` sign: discharge `eta=+0.002000`; charge `eta=-0.002000`.
- `delta_U_hys` sign: `func_dU_hys(298.15, 12000)=+0.086685635`; `Omega=2RT` gives `0.000000000e+00`.
- Graphite OCV `dU/dq` sign for lithiation-coordinate staging sequence: `U=[0.210, 0.140, 0.120, 0.085]`, steps `[-0.070, -0.020, -0.035]`, so `dU/dq<0`.
- Butler-Volmer exponent sign: with `chi=0.5`, `A=4RT`, the barrier term is `-2.000000`.
- `xi_eq` endpoint convention:
  - discharge `sigma_d=+1`: `(V<<U, V>>U) = (0.009277, 0.999095)`;
  - charge `sigma_d=-1`: endpoints reverse to `(0.990723, 0.000905)`.

## Scope check

- Intended output files: `v7-09b.tex`, `NOTEb.md`.
- `v7-09.tex` was not modified.
