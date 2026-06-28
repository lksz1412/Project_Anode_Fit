# v7-08b correction note

## Read coverage

Read in the requested order, full text:

| Order | File | Coverage |
|---:|---|---|
| 1 | `Claude/results/v7-08/v7-08.tex` | lines 1-597 |
| 2 | `Claude/results/v7-00_spine/Anode_Fit_v11_final.py` | lines 1-706 |
| 3 | `Claude/results/v7-00_spine/v11_flowchart.md` | lines 1-89 |
| 4 | `Claude/results/v7-00_spine/AUTHOR_BRIEF.md` | lines 1-75 |

`REVIEW1.md` was not opened or read.

## Corrections applied

| Item | Verdict | `v7-08b.tex` range | Note |
|---|---|---:|---|
| Correction 1 | CORRECTED | lines 573-579 | Restored the missing plus sign in the N9 cumulative equation: `C_bg + sum_j Q_j peak_shape_j`. This matches `Anode_Fit_v11_final.py` lines 431-433 and 481. |
| Correction 2 | CORRECTED | lines 296-313 | Inserted the OCV bridge `V_j(xi) -> Delta U_signed^hys = V_chg - V_dis -> |Delta U^hys| -> w_eff` immediately before the first `w_eff` derivation. |
| Correction 3 | CORRECTED | lines 379-386 | Clarified that `equilibrium()` determines `xi_eq` from hysteresis-free `V_eq`, not a hysteresis branch midpoint, and states `V_app = V_eq(xi_eq)` in the zero-current baseline. |
| Correction 4 | CORRECTED | lines 211-218, 266, 336, 379-386, 419-451, 499, 578 | Added missing algebraic intermediates for the spinodal and `L_q` derivations, plus physical motivation at major subsection starts where absent. |
| Polarity repair | CORRECTED | lines 129-134, 301-309, 635-643 | Repaired discharge polarity prose: discharge = de-lithiation = oxidation, measured `V_app > V_n`, so `eta = V_app - V_n > 0`. |

## Sign self-test

Sign-bearing passages reread after edits: `v7-08b.tex` lines 129-134, 301-309, 379-386, 635-643.

| Check | Verdict | Evidence |
|---|---|---|
| Discharge polarity: `V_n = V_app - sigma_d |I| R_n`; for discharge `V_app > V_n`, `eta > 0` | PASS | lines 129-134 and 635-643 |
| Discharge means de-lithiation and oxidation | PASS | line 134 |
| `xi_eq = logistic[sigma_d(V - U_d)/w]`; discharge `V up -> xi up` | PASS | lines 638-643 |
| Direction-invariant positive peak from `|d xi / dV|` | PASS | lines 389-394; Python self-test reports `neg=False` for discharge and charge curves |
| Hysteresis signed branch difference separated from nonnegative code gap | PASS | lines 301-309; Python self-test reports `d(dis-chg)=+86.9 mV` vs expected `+86.7 mV` |
| `chi_d = chi` for discharge and `1-chi` for charge | PASS | lines 456-465; Python self-test injectable `chi_split` check reports `differ=True` |
| `partial ln L_q / partial V < 0` retained | PASS | lines 481-487 |
| Charging tail uses reversed grid and remains nonnegative | PASS | lines 520-525; Python self-test tail direction reversal reports `neg=False` for both directions |
| N9 cumulative `dQ/dV` is baseline plus transition sum | PASS | lines 573-579 |

## Verification

Commands run from `Claude/results/v7-08`:

```text
xelatex -interaction=nonstopmode v7-08b.tex
xelatex -interaction=nonstopmode v7-08b.tex
$env:PYTHONDONTWRITEBYTECODE='1'; python '..\v7-00_spine\Anode_Fit_v11_final.py'
```

Results:

| Check | Result |
|---|---|
| `xelatex` availability | available at `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe` |
| `xelatex` pass 1 | exit code 0 |
| `xelatex` pass 2 | exit code 0 |
| Final LaTeX error count in `v7-08b.log` | 0 |
| Final warning count | 14 warnings: hyperref PDF-string warnings and font substitution warnings; no compile errors |
| PDF output | `v7-08b.pdf` generated, 10 pages |
| Python spine self-test | exit code 0, final line `>>> overall OK: True` |

