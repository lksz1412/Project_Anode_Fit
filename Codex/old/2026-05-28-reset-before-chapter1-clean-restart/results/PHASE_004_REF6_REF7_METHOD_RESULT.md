# Phase 004 — PDF Ref. 6/7 Method Extraction Result

## Summary

The PDF text is extractable without OCR. The user's paper cites refs. 6 and 7 as the source of an efficient solution method for Fredholm integral equations of the second kind. In the paper itself, that method is used after deriving an integral equation for the ultimate charge separation probability. The method rewrites the self-referential integral equation into a formally exact reciprocal expression involving ratios of the unknown function, then closes the expression by approximating those ratios with a truncated series or physically motivated estimates.

For the graphite ICA Chapter 1 restart, this method is verified but should not be imported as a main derivation step yet. The corrected Chapter 1 core can be closed by charge balance plus a relaxation equation. Ref. 6/7 methodology is useful as a future or appendix-level tool if the barrier-distribution or implicit feedback formulation is later recast as a Fredholm-type integral equation.

Gate result: `PASS_REF_METHOD_VERIFIED`

Transfer decision: `METHOD_VERIFIED_BUT_NOT_IMPORTED_TO_CHAPTER1_CORE`

## Step Range

Planned steps: 43-58

Actual steps completed: 43-58

## Input

| Input | Path |
|---|---|
| User paper PDF | `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` |

PDF metadata observed in extracted text:

| Item | Value |
|---|---|
| Title | Effects of external electric field and anisotropic long-range reactivity on charge separation probability |
| Citation | The Journal of Chemical Physics 147, 144111 (2017) |
| DOI in PDF | `10.1063/1.5000882` |
| Page count by `pypdf` | 10 |

## Extraction Method

| Check | Result |
|---|---|
| `pdftotext` availability | not available in current shell |
| bundled Python available | yes |
| `pypdf` import | yes |
| PDF text extraction | successful |
| OCR needed | no |

No OCR correction was applied. Therefore no OCR uncertainty flag is needed for the extracted text used in this phase.

## Bibliography Entries For Ref. 6 And Ref. 7

Extracted from the PDF reference list on PDF page 10 / article page `144111-9`:

| Ref. | Bibliography entry as available in PDF | Verification state |
|---:|---|---|
| 6 | S. Lee, C. Y. Son, J. Sung, and S. Chong, J. Chem. Phys. 134, 121102 (2011). | exact title and DOI not present in the PDF reference list; do not invent them |
| 7 | C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, J. Chem. Phys. 138, 164123 (2013). | title/DOI externally cross-checked as an auxiliary note: “An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity”, DOI `10.1063/1.4802005`, source: `https://pure.ewha.ac.kr/en/publications/an-accurate-expression-for-the-rates-of-diffusion-influenced-bimo` |

The method context is established from the user's PDF itself, so the Chapter 1 decision does not depend on having the full text of refs. 6 and 7 in this phase.

## Citation Context In The User Paper

| Location | Context | Meaning |
|---|---|---|
| PDF page 2 / article opening | The paper states that it employs a recently proposed method from refs. 6 and 7 for Fredholm integral equations of the second kind. | Ref. 6/7 are cited as a mathematical method source, not as a battery-specific physical model. |
| PDF page 5 / article page `144111-4` | After deriving an integral equation for the charge separation probability, the paper identifies it as a Fredholm integral equation of the second kind and cites refs. 6 and 7 for the solution method. | This is the main method-import point. |
| PDF page 8 / article page `144111-7` | The paper describes agreement with numerical results as demonstrating the utility of the Fredholm-equation solution method. | The method is an analytic approximation strategy validated against numerical solutions in that problem class. |

## Mathematical Problem Class

The method applies to a Fredholm integral equation of the second kind, i.e. a structure where the unknown function appears both outside and inside an integral:

```tex
f(x)=g(x)+\int K(x,y) f(y)\,dy
```

The user's PDF derives a more specialized version for charge separation probability. In simplified notation, the paper's Eq. (32) has the same self-referential structure:

```tex
\bar W_u(r)
=1-\int_{\sigma}^{r} K_1(r,r_1)\bar W_u(r_1)\,dr_1
  -\int_{r}^{\infty}K_2(r,r_1)\bar W_u(r_1)\,dr_1 .
```

The paper then rewrites this into a formally exact expression whose correction terms contain ratios such as:

```tex
\frac{\bar W_u(r_1)}{\bar W_u(r)} .
```

Those unknown ratios are then approximated, for example by truncated series solutions or physically reasonable estimates. The conceptual move is therefore:

```text
self-referential integral equation
  -> formally exact ratio expression
  -> approximate the unknown ratio
  -> closed analytic estimate
  -> compare against numerical solution
```

## Candidate Mapping To Graphite ICA

| Ref. 6/7 method object | Graphite ICA analogue | Transfer status |
|---|---|---|
| Unknown function `\bar W_u(r)` | phase progress or residual lag as a function of coordinate, e.g. `xi_j(q)` or `u_j(q)` | possible only if a Fredholm-type integral form is derived |
| Integral kernel `K(r,r_1)` | distribution/interaction kernel over charge coordinate, barrier coordinate, or potential state | not yet derived in Chapter 1 |
| Unknown ratio `\bar W_u(r_1)/\bar W_u(r)` | possible ratio `u_j(s)/u_j(q)` or `xi_j(g,s)/xi_j(g,q)` | future method candidate, not current core |
| Closed analytic estimate | approximate tail expression | Chapter 1 already has a simpler local ODE route for the first tail scale |

## What Transfers Safely

The following can be used as a methodological principle later:

- If the graphite problem is reformulated as a Fredholm second-kind equation, do not solve it by circular assertion.
- Recast the implicit integral equation into a form where the self-dependence is explicit.
- Close the expression only after stating the approximation used for unknown ratios or kernels.
- Validate the approximation against the limiting cases of the physical problem.

## What Does Not Transfer Directly

The following must not be imported into Chapter 1 as-is:

- the geminate charge-pair diffusion model;
- the specific spatial coordinate `r`, contact distance `sigma`, or central potential `U(r)`;
- the external-field anisotropic recombination sink as a battery phase-transition rate;
- numerical finite-element validation as a required Chapter 1 step;
- a solver-first workflow.

## Decision For Chapter 1

The ref. 6/7 method is verified but not needed in the core Chapter 1 derivation at this stage.

Reason:

1. The corrected graphite source already closes the primary feedback through charge balance:

```tex
Q_{\cell}q=Q_{\bg}(V_n,T)+\sum_j Q_{j,\tot}\xi_j.
```

2. The tail can be derived from the local relaxation equation:

```tex
\frac{d\xi_j}{dq}
=\frac{Q_{\cell}}{|I|}k_j\left[\xi_{j,\mathrm{eq}}-\xi_j\right].
```

3. A Fredholm-method import would be premature unless Phase 010 or later derives an actual Fredholm-type integral equation for a barrier-distribution tail or another implicit kernel.

Therefore the new manuscript should mention this only, if needed, as:

```text
Implicit integral formulations can be handled by a ratio-closure method for Fredholm equations,
but the present Chapter 1 first derives the single-barrier local tail scale from the ODE form.
```

## Validation

| Check | Result | Evidence |
|---|---|---|
| PDF text extractable without OCR | PASS | `pypdf` extracted page text |
| PDF page count established | PASS | 10 pages |
| Ref. 6 bibliography entry extracted | PASS | PDF page 10 / article page `144111-9` |
| Ref. 7 bibliography entry extracted | PASS | PDF page 10 / article page `144111-9` |
| Ref. 6/7 citation location found | PASS | PDF page 2 and PDF page 5 |
| Method problem class identified | PASS | Fredholm integral equation of the second kind |
| Exact method structure identified | PASS | self-referential integral equation -> unknown-function ratio expression -> ratio approximation |
| Transfer limits marked | PASS | battery variables not assumed equivalent to diffusion recombination variables |
| Chapter 1 import decision recorded | PASS | `METHOD_VERIFIED_BUT_NOT_IMPORTED_TO_CHAPTER1_CORE` |

## Gate

Gate: `PASS_REF_METHOD_VERIFIED`

Status: PASS

Reason:

- bibliography entries for refs. 6 and 7 were extracted from the user's PDF;
- citation locations and mathematical method context were found in the user's PDF;
- the method was classified as Fredholm second-kind integral-equation ratio closure;
- the method was not imported into Chapter 1 core because no Fredholm-type graphite ICA integral equation has yet been derived.

## Confirmed Non-Changes

- The original PDF was not modified.
- No source `.tex` file was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| Exact title/DOI for ref. 6 was not present in the PDF reference list | open but not blocking |
| Whether a Fredholm-type derivation is useful for the barrier-distribution extension | pending Phase 010 |
| Whether to cite refs. 6/7 in the final Chapter 1 manuscript body or reserve them for an appendix/future methods section | pending after Phases 008-010 |

No user decision is required before Phase 005.

## Next

Proceed directly to Phase 005 — Problem Definition And Scope Contract.
