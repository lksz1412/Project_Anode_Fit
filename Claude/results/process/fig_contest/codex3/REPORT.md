# codex3 figure contest report

## Scope and source check

- Required brief read: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1014_FIG_CONTEST_BRIEF.md` lines 1-19.
- Required current figure blocks read from `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.14\graphite_ica_ch1_v1.0.14.tex`:
  - `fig:spine` lines 158-191
  - `fig:staging` lines 272-305
  - `fig:hysloop` lines 1147-1173
  - `fig:barrier` lines 1255-1289
  - `fig:flux` lines 1291-1317
  - `fig:logistic` lines 1363-1385
  - `fig:widthbudget` lines 1540-1568
  - `fig:reversal` lines 1914-1946
- Edited/created scope: this `codex3` folder only.

## Per-target intent and coordinate basis

### T1_spine.tex

- Intent: Preserve the existing vertical N0-N9 spine while making the N2-N8 per-transition loop more legible. Added two side helper boxes for the equilibrium path and rate-tail path, without changing the original computation order.
- Coordinate basis: `T1_calc.py` prints the fixed node centers used in the TikZ layout.
- Conservative retouch: denser equation labels and clearer dashed loop boundary; no physical content removed.

### T2_staging.tex

- Intent: Preserve the five stage columns and gallery-fill motif, but connect the four stage transitions to the bottom initial-potential axis.
- Coordinate basis: `T2_calc.py` prints column origins, centers, nominal transition potentials, and filled-gallery indices.
- Conservative retouch: layer/galleries retained; added transition arrows and `0.210/0.140/0.120/0.085 V` peak-center correspondence.

### T3_hysloop.tex

- Intent: Preserve the single nonmonotone `V_eq(xi)` panel while separating Maxwell line, spinodal guides, and discharge/charge overshoot arrows.
- Coordinate basis: `T3_calc.py` evaluates `y = ln[xi/(1-xi)] + 4(1-2xi)` and spinodals `(1 +/- sqrt(0.5))/2`.
- Conservative retouch: same physical curve and gap; clearer path direction and gap annotation.

### T4_barrier.tex

- Intent: Preserve the two-panel equilibrium/driven barrier comparison while making the double-well landscape smoother and labeling both forward and reverse barriers.
- Coordinate basis: `T4_calc.py` evaluates a cosine-squared equilibrium barrier and a linear affinity tilt with `A=0.70`, `chi=0.50`.
- Conservative retouch: same Eyring/BV message; added `chi A` transition-state lowering and reverse-barrier rise.

### T5_flux.tex

- Intent: Preserve the forward/reverse straight-line flux construction and add affinity movement as three overlaid cases.
- Coordinate basis: `T5_calc.py` computes intersections from `xi_eq = r_plus/(r_plus+r_minus)` for `A<0`, `A=0`, and `A>0`.
- Conservative retouch: black case remains `r_plus=2r_minus`, `xi_eq=2/3`; gray cases show detailed-balance context.

### T6_logistic.tex

- Intent: Preserve the logistic plus derivative concept, but split it into stacked panels to avoid label/crossing crowding and show temperature dependence.
- Coordinate basis: `T6_calc.py` computes `w=nRT/F` for 268/298/328 K, then evaluates logistic and `xi(1-xi)/w` at fixed voltage offsets.
- Conservative retouch: same equations and center-slope meaning; added line-style distinction for temperature.

### T7_reversal.tex

- Intent: Preserve the discharge/charge mirror layout and make causal-memory direction explicit.
- Coordinate basis: `T7_calc.py` evaluates the equilibrium logistic-derivative bell and applies a one-sided exponential low-pass integral with `L_V=1.1w`; charge is the mirrored result.
- Conservative retouch: same positive peak convention; clearer arrows for high-V and low-V tails.

### T8_widthbudget.tex

- Intent: Preserve the overlay width-budget plot while separating the four narrative stages with badges and arrows.
- Coordinate basis: `T8_calc.py` evaluates the intrinsic logistic derivative, a symmetric effective-scale curve with scale `1.6w`, and a one-sided exponential convolution with `L_V=1.5w`.
- Conservative retouch: same delta -> intrinsic -> symmetric spread -> causal tail story; internal text changed to English ASCII.

## Compile result

- Command: `xelatex -interaction=nonstopmode codex3_check.tex`
- Working directory: `D:\Projects\Project_Anode_Fit\Claude\results\process\fig_contest\codex3`
- Result: exit code 0; `codex3_check.pdf` written.
- Expected non-fatal warnings: unresolved equation references from the standalone skeleton (`??` acceptable by the provided skeleton comment), font-shape substitution, and MiKTeX local logging/update environment warnings.
- Fixed during check: escaped underscores in `\code{Tn\_calc.py}` caption references after the first compile exposed LaTeX text-mode errors.
