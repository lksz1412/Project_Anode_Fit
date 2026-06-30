# v10-09 short note

- Source: `v10-09.tex` started byte-identical to `v10-00_spine/base_v9.tex` (1644 lines) before edits.
- Added broadening section near N6: transition-by-transition split, two-phase delta-to-measured-bell explanation, `U_j^app = U_j + eta`, `L_V` tail + `RT/F` floor, forward-only scope warning.
- Added `w_j` dual-status text: single-phase `Omega < 2RT` = equilibrium `nRT/F`; two-phase `Omega > 2RT` = phenomenological free fitting width. Current four graphite staging fit entries are explicitly read as phenomenological because their table `Omega` values exceed `2RT`.
- Removed `w_eff` trail from text, symbols, input table, and node map. Keyword gate found no `w_eff`/`use_w_eff`/`func_w_eff`/`eq:weff` remnants.
- Preserved v9 graphite forward, LCO electronic entropy, `xi_eq` distribution framing, sign chain, tables, and figures except for required `w_eff` edits and added broadening/bibliography text.
- Build: `xelatex -interaction=nonstopmode v10-09.tex` run 3 times; final pass exit 0, PDF 31 pages.
- Self 10-round checklist: broadening split, phenomenological `w`, no distribution inversion, no multi-particle/PSD convolution model, forward-only warning, `w_eff` zero, G-derive untouched, sign chain untouched, LCO electronic entropy untouched, tier/honesty note checked.
- Uncertain 1: new Levi/Fly/Park bibliography entries are DOI-grounded but abbreviated descriptively rather than full-title verified in this session.
