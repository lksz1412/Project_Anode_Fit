# codex2 Figure Contest Report

## Scope

- Target brief read: `V1014_FIG_CONTEST_BRIEF.md`, 19 lines.
- Source figure blocks read from `graphite_ica_ch1_v1.0.14.tex`:
  - T1 `fig:spine`: lines 158--191.
  - T2 `fig:staging`: lines 272--305.
  - T3 `fig:hysloop`: lines 1147--1173.
  - T4 `fig:barrier`: lines 1255--1289.
  - T5 `fig:flux`: lines 1291--1317.
  - T6 `fig:logistic`: lines 1363--1385.
  - T8 `fig:widthbudget`: lines 1540--1568.
  - T7 `fig:reversal`: lines 1914--1946.
- Edited/created files are confined to this `codex2` folder.

## Design Line

codex2 uses an engineering-drawing style: fixed axes, light construction grids, explicit baselines, dimension arrows, and grayscale-safe line hierarchy. Internal figure text is English ASCII; captions keep the Korean document terminology and existing labels.

## Per-Target Notes

### T1_spine.tex

- Intent: replace the vertical node list with a measured process drawing. N0/N1 are separated as global pre-processing, N2--N8 are enclosed as the per-transition loop, and N9/output are placed as the terminal aggregation block.
- Coordinate basis: `T1_calc.py` records fixed node centers and a small inset comparing a logistic equilibrium bell with a causal-tail shape. The inset points are numeric evaluations of `logistic(z)(1-logistic(z))` and a tail reference curve.

### T2_staging.tex

- Intent: make gallery filling and voltage mapping simultaneous. The upper drawing keeps stage 4, 3, 2L, 2, 1 gallery occupancy; the lower drawing adds a voltage axis and peak centers.
- Coordinate basis: `T2_calc.py` maps `U=0.210/0.140/0.120/0.085 V` onto a common `0.060--0.230 V` axis and evaluates small logistic-derivative peak markers.

### T3_hysloop.tex

- Intent: make the spinodal extrema, Maxwell line, overshoot directions, and full gap dimension visible at once.
- Coordinate basis: `T3_calc.py` evaluates `ln[xi/(1-xi)] + 4(1-2xi)` for `Omega/RT=4`. Spinodal points are `xi_s^-=0.1464`, `xi_s^+=0.8536`, with scaled extrema `+/-1.0657`.

### T4_barrier.tex

- Intent: improve the barrier landscape from a schematic curve to a smooth double-well engineering diagram with explicit forward/reverse barrier dimensions.
- Coordinate basis: `T4_calc.py` evaluates `G0(x)=0.10+0.90(x-1)^2(x-5)^2/16` and the driven tilt `G(x)=G0(x)-A(x-1)/4` with `A=0.35`, `chi=1/2`.

### T5_flux.tex

- Intent: keep the forward/reverse flux-line derivation while adding multiple affinity cases so the fixed point motion is visible.
- Coordinate basis: `T5_calc.py` evaluates `xi_eq=r+/(r++r-)` for `r+/r-=1,2,3` plus a negative-affinity reference. The plotted emphasized intersections are `1/2`, `2/3`, and `3/4`.

### T6_logistic.tex

- Intent: split logistic and derivative into two aligned panels so `w=nRT/F`, center slope, and temperature broadening are readable.
- Coordinate basis: `T6_calc.py` evaluates `xi_eq=1/(1+exp(-(V-U)/w))` and `xi(1-xi)/w` for `T=268/298/328 K` with `n=1`.

### T7_reversal.tex

- Intent: show discharge and charge as mirror-causal low-pass results, with explicit time/progress arrows and tail directions.
- Coordinate basis: `T7_calc.py` evaluates the equilibrium bell and a first-order low-pass recurrence with `L_V/w=0.85`, `Delta V/w=0.1`, then mirrors the result for charge after grid reversal.

### T8_widthbudget.tex

- Intent: keep all four width-budget stages but make the scale budget explicit with construction lines and dimension arrows.
- Coordinate basis: `T8_calc.py` evaluates the intrinsic logistic derivative, the broadened `1.6w_j` logistic-derivative approximation, and a one-sided exponential convolution with `L_V=1.5w_j` by trapezoidal numerical integration.

## Compile Check

Command run inside this folder:

```powershell
xelatex -interaction=nonstopmode codex2_check.tex
```

Result:

- Exit code: 0.
- Log error scan: no lines beginning with `!`.
- Output: `codex2_check.pdf`, 3 pages.
- Expected warnings: unresolved `\eqref` references from the skeleton context, and a Korean font italic substitution warning. These do not block the requested 0-error compile check.
