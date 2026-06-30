# Corrections Applied

- D-PEAK (v8-07b.tex lines 907-915): Replaced the incorrect small-$L_V$ explanation with the recurrence limit $\rho=\exp(-\Delta_\mathrm{grid}/L_V)$. The new text states that $L_V\to0$ gives $\rho\to0$, $\xi_\mathrm{lag}\to\xi_\eq$, and peak suppression unless the code branch selects the equilibrium bell, while $L_V\gg\Delta_\mathrm{grid}$ is the smooth-lag limit that recovers the derivative reduction.
- D-UBR (v8-07b.tex lines 459-460): Added that eq:Ubranch is a phenomenological parameterization, not a first-principles derivation. The sentence ties the ansatz to observed voltage-branch behavior and the $h_{\eta,j}\gamma_j$ shrinkage of the spinodal upper-bound gap.
- D-WEFF (v8-07b.tex lines 545-560): Inserted the missing algebra bridge from the HWHM-style effective-width discussion to $s_F(\dd V/\dd\xi)_{1/2}=4Fw$. The inserted display derives $\dd q/\dd\xi|_{1/2}=s_F/4$ and then connects the charge-axis slope to the voltage-axis width.

# Sign-Convention Self-Test

| item | status(OK/FIXED/WARN) | note |
|---|---|---|
| $U_j(T)=(-\Delta H+T\Delta S)/F$, $\Delta G=-FU$ | OK | Present at eq:Uj and sign-check S1; exothermic $\Delta H_\rxn<0$ raises $U_j$. |
| $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$, discharge $V\uparrow\Rightarrow\xi\uparrow$ | OK | Present in notation, eq:xieq, and S2; direction sign remains unchanged by edits. |
| $d\xi/dV=\sigma_d\xi(1-\xi)/w$, peak positive and direction-invariant | OK | Present at eq:eqpeak and S3; peak uses magnitude $\xi(1-\xi)/w$. |
| $\Delta U_\hys\ge0$, $\Omega\le2RT\to0$, branch center $\pm\tfrac12\sigma_d$ | OK | Present at eq:dUhys, eq:Ubranch, and S4; D-UBR adds ansatz caveat without changing signs. |
| $\chi_d$: discharge $\chi$, charge $1-\chi$; $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | OK | Present at eq:chid, eq:dHeff, and S5; code mapping unchanged. |
| $\partial\ln L_q/\partial V$ operationally $0$ because cut affinity is constant | OK | Present in N7 discussion and S6; inequality is still framed only as physical motivation. |
| Tail: charge grid reversal; charge $\dd Q/\dd V$ is discharge mirror and positive | OK | Present at eq:reversal and S7; D-PEAK edit does not alter reversal logic. |
| Polarization $V_n=V_\app-\sigma_d|I|R_n$ | OK | Present at eq:vn and S8; discharge measured voltage remains above internal voltage. |

# Regression Check

| category | result | note |
|---|---|---|
| Read coverage | PASS | Read full files: v8-07.tex lines 1-1157, Anode_Fit_v11_final.py lines 1-706, v7-11.tex lines 1-889, AUTHOR_BRIEF_v8.md lines 1-63. REVIEW1.md was not read. |
| Target-only output scope | PASS | Wrote only in Claude/results/v8-07: v8-07b.tex, NOTEb.md, and xelatex build artifacts/PDF. Original v8-07.tex was copied from and left untouched. |
| Cross-references | PASS | PowerShell check: 79 labels, 111 refs, 0 duplicate labels, 0 missing refs. Final log scan found no undefined-reference, citation, or rerun warnings. |
| Equation environments | PASS | PowerShell begin/end balance check found 0 environment imbalances. xelatex completed without LaTeX errors. |
| D-PEAK regression | PASS | Deleted the wrong "one-cell lag / small L_V derivative recovery" sentence; literal search found 0 hits for the removed wrong phrasing. |
| Edited-region contradictions | PASS | Near D-PEAK, the text now separates $L_V\to0$ branch recovery from the $L_V\gg\Delta_\mathrm{grid}$ smooth reduction. D-UBR and D-WEFF additions do not change code identifiers or branch signs. |
| Compile warnings | WARN | Nonfatal existing-style warnings remain: font substitutions, underfull/overfull hboxes, hyperref PDF-string token removals, MiKTeX log/update/security notices, and an "Infinite glue shrinkage" ignored warning. |

# Compile

- xelatex found: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`
- Pass 1 command: `xelatex -interaction=nonstopmode -halt-on-error v8-07b.tex`; exit code 0; PDF produced with first-pass unresolved refs.
- Pass 2 command: `xelatex -interaction=nonstopmode -halt-on-error v8-07b.tex`; exit code 0; PDF produced; rerun warning remained.
- Stabilization pass: same command; exit code 0; final log has no unresolved-reference or rerun warnings.
- PDF: `D:\Projects\Project_Anode_Fit\Claude\results\v8-07\v8-07b.pdf` (362808 bytes, 20 pages).
