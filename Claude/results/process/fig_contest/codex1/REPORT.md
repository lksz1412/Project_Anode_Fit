# codex1 figure contest report

## Source read coverage

- `D:\Projects\Project_Anode_Fit\Claude\results\process\V1014_FIG_CONTEST_BRIEF.md`: read all 23 lines.
- `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.14\graphite_ica_ch1_v1.0.14.tex`: read the current `tikzpicture` + caption + label blocks for:
  - `fig:spine` lines 160-190
  - `fig:staging` lines 274-304
  - `fig:hysloop` lines 1149-1172
  - `fig:barrier` lines 1257-1288
  - `fig:flux` lines 1293-1316
  - `fig:logistic` lines 1365-1384
  - `fig:widthbudget` lines 1542-1567
  - `fig:reversal` lines 1916-1945

## Candidate intent and coordinate basis

### T1_spine.tex

- Intent: Replace the flat vertical node chain with a left-to-right calculation path, a high-contrast transition loop box, and two small guide curves for equilibrium species and causal memory.
- Coordinate basis: `T1_calc.py` prints the logistic guide curve and the causal-tail guide coordinates used for the mini insets. The main node positions are layout coordinates, not fitted physical curves.

### T2_staging.tex

- Intent: Make the stage 4 -> 3 -> 2L -> 2 -> 1 gallery filling readable as a layer occupancy diagram, then tie the four transition potentials directly to a bottom `dQ/dV` peak axis.
- Coordinate basis: `T2_calc.py` maps `U=0.210/0.140/0.120/0.085 V` onto a 0.075-0.220 V axis and evaluates Gaussian peak markers around each mapped center.

### T3_hysloop.tex

- Intent: Emphasize overshoot direction, Maxwell line, spinodal extrema, and the upper hysteresis gap with stronger path contrast.
- Coordinate basis: `T3_calc.py` evaluates `y=ln[xi/(1-xi)] + 4(1-2xi)` for `Omega=4RT`, prints the plotted curve, spinodal locations `0.1464/0.8536`, extrema `+/-1.0657`, and gap `2.1314`.

### T4_barrier.tex

- Intent: Use a smoother double-well barrier with a driven tilted counterpart so `Delta G_a - chi A` and `Delta G_a + (1-chi)A` are visually separated.
- Coordinate basis: `T4_calc.py` evaluates a quartic double-well baseline and a linear-tilt driven curve with `A=0.70`, giving forward/reverse barrier examples `0.55/1.25`.

### T5_flux.tex

- Intent: Show the stationary point as a moving intersection under three affinity cases, with `A>0` / detailed-balance / `A<0` bands and line contrast.
- Coordinate basis: `T5_calc.py` evaluates `xi_eq=r+/(r++r-)` for `r+/r-=0.5, 1, 2`, giving intersections `1/3, 1/2, 2/3`.

### T6_logistic.tex

- Intent: Split the logistic species and derivative peak into two panels and make the temperature dependence of `w=nRT/F` legible.
- Coordinate basis: `T6_calc.py` evaluates the logistic and derivative curves at 268/298/328 K with `w=23.1/25.7/28.3 mV` for `n=1`.

### T7_reversal.tex

- Intent: Present discharge and charge as mirrored causal-memory panels, with explicit time/progress arrows and tail direction annotations.
- Coordinate basis: `T7_calc.py` evaluates the equilibrium logistic-derivative bell and numerically integrates a one-sided exponential low-pass kernel with `L_V=1.10w`; charge is the mirrored discharge result.

### T8_widthbudget.tex

- Intent: Turn the width budget into a four-step narrative: delta -> intrinsic species -> symmetric variance -> causal skew.
- Coordinate basis: `T8_calc.py` evaluates the intrinsic logistic derivative, the `1.6w` symmetric broadening example from `sqrt(1+1.25^2)`, and a one-sided exponential convolution with `L_V=1.5w`.

## Compile and validation result

- Calc scripts: `T1_calc.py` through `T8_calc.py` all ran successfully with Python and printed their coordinate bases.
- Build file: `_check.tex` was adapted from `fig_contest/_skeleton.tex` and inputs all eight codex1 candidates.
- Compile command: `xelatex -interaction=nonstopmode _check.tex`
- Compile result: exit code 0; `_check.pdf` generated.
- Expected unresolved references: `eq:xieq`, `eq:Veq`, `eq:Ubranch`, `eq:bv`, `eq:db`, `eq:logisticsolve`, `eq:belliden`, `eq:widthbudget` render as unresolved because the contest skeleton has no main-document labels.
- Warnings observed: overfull hbox warnings for the wide T6 and T8 figures; no TeX errors after repair.

## Boundary note

All generated, modified, and compile-output files for this task are inside:

`D:\Projects\Project_Anode_Fit\Claude\results\process\fig_contest\codex1`
