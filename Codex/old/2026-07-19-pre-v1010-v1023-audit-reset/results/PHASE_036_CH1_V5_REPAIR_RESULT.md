# Phase 036 — Chapter 1 V5 Repair Result

## Summary

Created and repaired `graphite_ica_ch1_codex_candidate_v5.tex` from the preserved V4 file. Claude 폴더는 수정하지 않았다.

## Files Created

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v5.tex`

## Main Repairs

1. Added notation definitions for `T`, `R`, `F`, `k_B`, `h`, `kappa(T)`, `q_a`, `C_bg`, `D`, and `eta_ct`.
2. Added AL-8 and AL-9 so the assumption ledger is continuous from AL-1 to AL-16.
3. Replaced `Q_bg` as a mixed object with `Q_bg^{eq}` and `Q_bg^{mathrm{lag}}`; `C_bg` now refers only to equilibrium background capacitance.
4. Rewrote the Marcus/BEP argument:
   - symmetric Marcus gives `chi_j=1/2`;
   - general `0 <= chi_j <= 1` is an empirical scalar mobility sensitivity, not a direct Marcus symmetric result;
   - Ch1 `chi_j` remains distinct from Ch3 `beta_j`.
5. Expanded the Volterra spectrum step by explicitly stating the two conditions that allow the `L` integral to form a kernel.
6. Expanded the Plan A denominator derivation with the intermediate `J(q)` equation.
7. Rewrote the simple fitting section as `narrow-spectrum single-mode`.
8. Added the current-prefactor-free extraction variable:
   `Z_L = ln L - ln |I|`.
9. Rewrote the Eyring extraction as:
   `y_kappa(T)=ln[|I|/(L T)] - chi_j A_j/(RT) - ln kappa(T)`.
10. Rewrote falsification so stretched-tail curvature does not incorrectly self-falsify the whole theory; it falsifies the single-mode/narrow-spectrum approximation and triggers spectrum forward prediction.

## Validation During Repair

- Static begin/end balance: 57/57.
- Duplicate labels: 0.
- Missing refs/cites by static parser: 0.
- AL IDs found: 1--16 continuous.
- Known risk scan:
  - Heaviside/support step pattern: 0.
  - amplitude-less `A_L=\delta`: 0.
  - old plus-sign Eyring double count pattern: 0.
  - placeholder/process metadata pattern: 0.
  - remaining `beta_j` mention: intended statement that Ch1 `chi_j` is not identical to Ch3 `beta_j`.

## Gate

Phase 036 repair draft is mechanically coherent enough for Phase 037 review. It is not claimed as final without Phase 037/038.
