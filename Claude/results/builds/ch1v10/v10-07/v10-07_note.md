# v10-07 short note

- Source: `v10-07.tex` started as a byte-identical copy of `v10-00_spine/base_v9.tex` before edits.
- Added broadening section near the equilibrium peak baseline: transition-by-transition split, two-phase apparent-`U = U_j + eta`, kinetic tail `L_V`, intrinsic `RT/F` floor, forward-only / ill-posed warning, and no multi-particle or PSD convolution model.
- Added `w_j` dual status: solid-solution / single-phase `w_j = n_j RT/F` is an equilibrium prediction; two-phase staging `w_j` is a phenomenological free fitting width.
- Removed all `w_eff` / effective-width narrowing traces from the TeX source.
- Preserved v9 graphite forward flow, LCO electronic entropy section, `xi_eq` distribution framing, sign chain, figures, and citations except for the targeted broadening references.
- Build: `xelatex -interaction=nonstopmode v10-07.tex` run after final edit, exit 0; PDF page count = 31.
- Self-check 10x: broadening transition split, phenomenological `w`, no multi-particle model construction, forward-only warning, radius/GITT warning, `w_eff` residual 0, v9 preservation, G-derive untouched, sign chain untouched, tier honesty checked.
- Uncertain 1 place: `rsc2021` remains a DOI-only bibliography entry because the project research note supplied the DOI/claim but not full citation metadata.
