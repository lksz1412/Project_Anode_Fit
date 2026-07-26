# PHASE 041 — Chapter 3 Candidate V1 10-Pass Review And Verification

## Target

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch3_codex_candidate_v1.tex`

## Source Status

- Final SHA256: `7C91C7F7A6AB595AD1ED4C51C285D8701669AA618D5E1C0B6A337FBAC786FE9F`
- Final line count: 787 source lines, parser reported 788 including trailing split artifact.

## Critical Repairs Applied

- Replaced Claude lineage `\chi_j\equiv\beta_j` with the Chapter 1 V5 convention:
  - `\chi_j` = Level-A scalar mobility sensitivity.
  - `\beta_j` = Chapter 3 Level-B directional transfer coefficient.
  - They are not identical.
- Added the Level-B to Level-A projection formula:
  - `\chi_{j,\mathrm{proj}} = RT\,\partial \ln(r_j^++r_j^-)/\partial\mathcal A_j`.
  - This is the proper comparison object for Chapter 1 `\chi_j`.
- Removed worker-facing RB/CHARTER metadata, author/date metadata, Chapter 3 self-check table, Ch6/solver references, and direct `Q_\bg` inheritance.
- Replaced Ch3 current-balance background terms with `Q_\bg^{\eq}` to match Chapter 1 V5 and Chapter 2 V1.
- Preserved the physical forward/backward Eyring and BV structure while correcting the parameter hierarchy.

## 10-Pass Review Summary

All passes covered the full Chapter 3 candidate either by direct full-file chunks or whole-file static parsing.

| Pass | Chunking / Lens | Result |
|---|---|---|
| P1 | section-level convention scan | RB/CHARTER/author/date/self-check/process markers removed. |
| P2 | 1--180 / inherited variables and notation | Chapter 1 V5 and Chapter 2 V1 interface preserved; `Q_\bg^{\eq}` inherited. |
| P3 | 181--360 / potential hierarchy and detailed balance | `V_n`, `V_{n,\app}`, `V_{n,\drive}`, `\eta_n`, `\eta_j`, and `\mathcal A_j` remain separated. |
| P4 | 361--540 / Level-B directional kinetics | `\beta_j` no longer equals `\chi_j`; `\chi_{j,\mathrm{proj}}` introduced for Level-B to Level-A comparison. |
| P5 | 541--787 / current, identifiability, AL, conclusion | Current conservation uses `Q_\bg^{\eq}`; identifiability chain includes both `\chi_j` and `\beta_j` as distinct correlated quantities. |
| P6 | risk-pattern scan | No `RB`, `CHARTER`, `P3-`, `Ch6`, `Chapter 6`, `solver`, self-check table, direct `Q_\bg`, or explicit `\chi=\beta` pattern remains. |
| P7 | static integrity parse | begin/end 52/52, labels 48, duplicate labels 0, refs 116 with missing refs 0, cites 13 / bibitems 10 with missing cites 0 and unused bibs 0. |
| P8 | physics consistency | Level A target recovery is kept as detailed-balance stationary-target limit, not unconditional parameter identity. |
| P9 | fitting/usability boundary | Ch3 does not implement solver code; it supplies theory variables and boundaries for Ch4/Ch5. |
| P10 | downstream handoff | Ch4 receives `r_j^\pm`, `n_j^{\eff}`, `I_j`, `\eta_j`, `R_\ct`, and distinct `\beta_j`; Ch5 receives `\xi_{\sstat,j}` branch/hysteresis structure. |

## Verification Commands And Results

Static parser:

- `begin=52`, `end=52`
- `labels=48`, `duplicateLabels=0`
- `refs=116`, `missingRefs=0`
- `cites=13`, `bibitems=10`, `missingCites=0`, `unusedBibs=0`

Risk scan:

- No remaining `RB`, `CHARTER`, `P3-`, `재구성본`, `Author`, `Date`, `Ch.6`, `Ch6`, `Chapter 6`, `solver`, `자체 검수`, `검수표`, direct unsplit `Q_\bg`, `Heaviside`, or explicit `\chi_j=\beta_j` / `\chi_j\equiv\beta_j`.
- Remaining `clip/cap/softplus/step` occurrences are prohibition statements, not model definitions.

XeLaTeX:

- Engine: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`
- Output PDF: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch3_v1\graphite_ica_ch3_codex_candidate_v1.pdf`
- PDF size: 354838 bytes
- Final log:
  - LaTeX errors: 0
  - Undefined references/citations: 0
  - Missing character warnings: 0
  - Rerun warnings counted: 1
  - Overfull hbox warnings: 0
  - Underfull hbox warnings: 1
  - Font warnings: 5
  - Hyperref PDF-string warnings: 31
- MiKTeX update warning is environmental, not a TeX source failure.

## Gate Result

Chapter 3 candidate V1 is ready as the current Codex theory candidate. Proceed to Chapter 4 with these constraints:

- Chapter 4 must use `\beta_j` as a Ch3 directional kinetic parameter, not as Ch1 `\chi_j`.
- Chapter 4 must use `n_j^{\eff}` and transition current `I_j` from Ch3 to build irreversible heat.
- Chapter 4 must preserve Chapter 2's reversible/irreversible split and avoid double counting relaxation heat.
