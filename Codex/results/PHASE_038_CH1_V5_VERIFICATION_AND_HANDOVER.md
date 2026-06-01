# Phase 038 — Chapter 1 V5 Verification and Handover

## Canonical Candidate

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v5.tex`
- Lines: 993
- SHA256: `D5D77DC97E8FB598C39B69F339F15E048273F03D1E767A576A5816DD469A64A1`

## Build Verification

XeLaTeX was run with output directory:

- `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch1_v5`

Result:

- Pass 1 exit: 0 after repair
- Pass 2 exit: 0
- Pass 3 exit: 0
- PDF: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch1_v5\graphite_ica_ch1_codex_candidate_v5.pdf`
- PDF size: 414226 bytes

Log scan after Pass 3:

- LaTeX errors: 0
- Undefined refs: 0
- Undefined cites: 0
- Overfull: 7
- Underfull: 31
- Hyperref warnings: 13
- Font warnings: 5

MiKTeX update warning remains an environment maintenance warning, not a document compile failure.

## Downstream Interface For Chapter 2--5

Chapter 2--5 must inherit these V5 conventions:

1. `Q_bg^{eq}` is equilibrium background capacity. `C_bg` is only `partial Q_bg^{eq}/partial V_n`.
2. Rate-dependent background lag, if needed, is `Q_bg^{mathrm{lag}}` or an added dynamic mode; it is not hidden inside `C_bg`.
3. Ch1 `chi_j` is Level-A scalar mobility sensitivity, not Ch3 `beta_j`.
4. Symmetric Marcus supports `chi_j=1/2`; general `chi_j` is an empirical BEP/BV-style scalar slope.
5. Single-mode fitting is narrow-spectrum only.
6. Stretched/low-temperature tails require spectrum or Plan B forward prediction, not single-L Arrhenius extraction.
7. Eyring extraction uses `y_kappa(T)=ln[|I|/(L T)] - chi_j A_j/(RT) - ln kappa(T)`.
8. `Z_L=ln L-ln|I|` or fixed-current sweeps are required for `chi_j` extraction.

## Next

Resume with Chapter 2 planning/execution from V5. Do not use V4 as the downstream spine.
