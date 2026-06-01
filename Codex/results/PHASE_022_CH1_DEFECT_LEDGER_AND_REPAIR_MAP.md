# PHASE 022C - Chapter 1 Defect Ledger and Repair Map

## Repair Map

| Defect | Severity | Repair in Codex candidate |
|---|---|---|
| Process metadata in paper-facing body | High | Removed visible RB/date/author/process history from candidate body. |
| English prose dominance | High | Rebuilt v3 with Korean explanatory prose and English technical terms. |
| Branch convention ambiguity | Critical | Added branch-local discharge/delithiation convention and separated lithiation literature order. |
| `chi_j` vs `beta_j` conflation | Critical | Defined `chi_j` as Level-A scalar relaxation-barrier sensitivity; directional kinetics moved to Ch3. |
| BV/Marcus common-mode conflict | Critical | Recast potential assistance as bounded scalar relaxation-barrier approximation, not microscopic forward barrier split. |
| `A_L` overload | Critical | Split `p_L(L)` probability spectrum and `A_L(L)` amplitude spectrum. |
| Single-mode amplitude omission | Critical | Replaced `A_L=delta` with `A_L(L)=Theta_0 delta(L-L_*)`. |
| C-rate unconditional claim | Critical | Replaced with competition of `|I|` prefactor, potential-assisted `k`, and apparent-axis polarization. |
| ICA exponential overclaim | High | Added small-tail/local-baseline condition before `Y_tail approx B exp[-x/L]`. |
| Arrhenius overclaim | High | Added prefactor/entropy/fixed-drive conditions. |
| Plan A/B solver dominance | Medium | Demoted to optional self-consistency correction and reference evaluation. |
| Placeholder refs 6/7/user paper | High | Corrected titles, authors, article numbers, and DOI entries. |

## Output Candidate

- Main repaired file: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v3.tex`
- Intermediate candidate kept for traceability: `graphite_ica_ch1_codex_candidate_v2.tex`

## Gate Status

- Followability gate: PASS for current candidate structure; still needs human scientific review.
- Usability gate: PASS, first-pass fitting formula present as `Y_tail(q) approx B exp[-(q-q_a)/L]`.
- Scope gate: PASS, Plan A/B no longer dominates main proof.
- Citation placeholder gate: PASS for checked user paper/ref.6/ref.7 metadata.
