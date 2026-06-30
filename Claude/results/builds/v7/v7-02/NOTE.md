# NOTE.md — v7-02 (경쟁 구현 02)

## 1. Read Coverage

| File | Lines | Read Method | Coverage |
|------|-------|-------------|----------|
| AUTHOR_BRIEF.md | 1–76 (full) | Sequential head→tail | 100% |
| v11_flowchart.md | 1–90 (full) | Sequential head→tail | 100% |
| Anode_Fit_v11_final.py | 1–706 (full) | 4 batches, head→tail | 100% |
| graphite_ica_ch1_Opus_v5.tex | 1–1882 (full) | 4 batches (limit 450), head→tail | 100% |

## 2. Self-Check 10-Round Log

| Round | Chunk scheme | Lens | Defects found | Action |
|-------|-------------|------|---------------|--------|
| R1 | Full document sequential | Structural: TOC / section order / bridges | 0 | PASS |
| R2 | Equation block-by-block (25 eq.) | Physics: derivation chain, unit | 0 | PASS |
| R3 | Code-ID / line-number pairs | Code: identifier, line ref 1:1 with v11 | 0 | PASS |
| R4 | 8-item sign checklist (per AUTHOR_BRIEF §8) | Sign correctness | 0 | PASS |
| R5 | Figure-by-figure (5 TikZ figures) | English ASCII only inside TikZ | 5 | FIXED (Korean→English in nodes) |
| R6 | Label/ref orphan scan; command inventory | Completeness: orphans | 2 | INFO (\dis, \chg defined but unused — not an error) |
| R7 | N-node by N-node (N0–N9) | Completeness: every node has verifybox | 0 | PASS |
| R8 | Domain physics (spinodal, hys gap) | Accuracy: independent numerical check | 0 | PASS |
| R9 | Practical usability: fitting section | G-usable: code reproducibility | 0 | PASS |
| R10 | Line-level scan (format, style, v6 absence) | Style / v5 preamble / no v6 | 0 | PASS |

Convergence: R9 and R10 consecutive 0-defect rounds → converged. Rounds 9–10 = 0 each.

## 3. Sign Checklist (AUTHOR_BRIEF §8)

All 8 items verified against both v7-02.tex and v11_final.py:

| # | Item | Equation label | v11 code ref | Status |
|---|------|---------------|--------------|--------|
| 1 | U_j(T) = (−ΔH_rxn + T·ΔS_rxn) / F | eq:Uj | func_U_j L68 | PASS |
| 2 | ξ_eq = logistic[σ_d(V_n−U)/w]; discharge σ_d=+1: V↑→ξ↑ | eq:xieq | func_ksi_eq L84 | PASS |
| 3 | dξ/dV = σ_d·ξ(1−ξ)/w → peak positive (direction invariant) | eq:dxidV | L468 | PASS |
| 4 | ΔU_hys≥0, Ω≤2RT→0; branch center +½σ_d·h_η·γ·ΔU_hys | eq:hysdU, eq:hyscenter | func_dU_hys L123, func_U_branch L133 | PASS |
| 5 | χ_d: discharge χ / charge 1−χ; ΔH_a^eff = ΔH_a − χ_d·Ω | eq:chid, eq:dHeff | func_chi_d L155, func_dH_a_eff L149 | PASS |
| 6 | ∂lnL_q/∂V < 0 (V↑→A↑→barrier↓→tail shorter) | eq:lnLq (verifybox) | func_L_q L90 | PASS |
| 7 | Charging lattice reversal ξ[::-1]…[::-1]; dQ/dV positive | eq:reverse | L474–477 | PASS |
| 8 | Polarization: V_n = V_app − σ_d·|I|·R_n | eq:vn | dqdv L412 | PASS |

## 4. Figure List

| Label | Section / Node | Content (English summary) | New TikZ? |
|-------|---------------|--------------------------|-----------|
| fig:polar | §2 / N1 | IR-drop block diagram: V_app → V_n | Yes (new) |
| fig:vdwloop | §4 / N3 | Non-monotone isotherm (Ω=3RT), discharge/charge overshoot paths, ΔU_hys gap | Yes (new) |
| fig:eqpeak | §6 / N6 | Equilibrium bell-shaped dQ/dV peak, peak height Q_j/(4w_j), area Q_j | Yes (new) |
| fig:tail | §8 / N8 | Kinetic tail: equilibrium (dotted) vs lagged (solid), tail length L_{V,j} | Yes (new) |
| fig:flowchart | §9 / N9 | N0→N9 calculation flow, node-to-section mapping | Yes (new) |

All 5 figures: new TikZ, figure-internal text English ASCII only (Korean removed in R5 fix).
No figures reused from v5 or v6. Orphan rule satisfied: each figure is referenced in its section or caption is self-descriptive.

## 5. Decision Queue

| ID | Node | Issue | Decision taken |
|----|------|-------|----------------|
| DQ-01 | N5 | func_ksi_eq L84: code uses `s` parameter (not `sigma_d`) as input. Did not change identifier in text — described as `sigma_d` conceptually per v11_flowchart.md naming. | Use sigma_d in text (physics convention); note code uses `s` as argument name |
| DQ-02 | N7 | lnLq formula: code L90 uses `x` for chi_d and `A` for affinity. Text uses χ_d and A. No identifier conflict since text is exposition, not code listing. | Use physics symbols in equations; cite code arg names in parenthetical |
| DQ-03 | N8 | eq:reverse uses Python slice notation `[::-1]` directly in LaTeX math. Could be ambiguous to non-Python readers. | Retained for direct code traceability; L474-477 citation makes it clear |
| DQ-04 | N6 | ∂ξ/∂V derivation: σ_d factor in eq:dxidV makes peak positive for both directions. Text explicitly states "direction invariant" but the σ_d factor is still present. v5 convention: peak always positive. | Verified: σ_d cancels because equilibrium (ξ_eq) is monotone in σ_d(V−U)/w direction — peak_shape=(ξ_eq−ξ_lagged)/L_V is always ≥0. Stated explicitly. |
| DQ-05 | Build | \sstat not defined in preamble (discovered during build R1). | Added \newcommand{\sstat}{\mathrm{ss}} to preamble. |

## 6. Build Results

| Pass | Command | Output | Fatal errors (^!) | Warnings |
|------|---------|--------|-------------------|----------|
| Pass 1 (initial) | xelatex -interaction=nonstopmode v7-02.tex | 13 pages PDF | 1 (Undefined \sstat) | LastPage undef, rerun |
| Pass 2 (after \sstat fix) | xelatex -interaction=nonstopmode v7-02.tex | 14 pages PDF | 0 | Label changed, rerun |
| Pass 3 (stabilize) | xelatex -interaction=nonstopmode v7-02.tex | 14 pages PDF | 0 | Font substitution (cosmetic) |
| Pass 4 (after figure English fix) | xelatex -interaction=nonstopmode v7-02.tex | 14 pages PDF | 0 | Font substitution (cosmetic) |
| Pass 5 (final stabilize) | xelatex -interaction=nonstopmode v7-02.tex | 14 pages PDF | 0 | Font substitution (cosmetic) |

**Final status: 0 fatal errors, 14-page PDF generated.**
Remaining warnings: "Some font shapes were not available, defaults substituted" — MiKTeX font fallback for some math shapes; does not affect PDF output. "major issue: So far, you have not checked for MiKTeX updates" — MiKTeX system-level advisory, not a document error.
