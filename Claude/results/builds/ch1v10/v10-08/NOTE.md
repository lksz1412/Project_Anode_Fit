# v10-08 Codex build note

- Source: `v10-08.tex` started identical to `v10-00_spine/base_v9.tex` (SHA256 match before edit).
- Added: broadening subsection near equilibrium peak, with transition split, apparent-$U=U_j+\eta$, forward-only warning, and no multi-particle/PSD convolution model.
- Updated: $w_j$ dual status. Single-phase $\Omega<2RT$ remains $nRT/F$ equilibrium width; two-phase/staging $\Omega>2RT$ is phenomenological free fitting width.
- Removed: all `w_eff` traces from text, labels, comments, input table, and node map. Final text search returned zero matches.
- Preserved: v9 graphite forward flow, LCO electronic entropy section, $\xi_\eq$ distribution framing, sign chain, figures, and existing citations except local `w_eff` removals.
- Build: `xelatex -interaction=nonstopmode v10-08.tex` run 3 times; final log has no `!`, no `LaTeX Error`, no undefined references/citations, no rerun request. Output: 31 pages.
- Self 10-pass checklist: broadening transition split, phenomenological two-phase $w$, no model extension, forward-only, radius/GITT warning, apparent-$U$, $w$ dual status, `w_eff` zero, v9 preservation, sign/G-derive/LCO preservation all checked.
- Uncertain 1: the physical literature allows PSD kinetic dispersion as an explanatory contributor, but the build prompt forbids adding a multi-particle model; this build mentions it only as absorbed into phenomenological $w_j$ and $L_V$.
