# Ref. 6/7 Method Notes

Project: `D:\Projects\Project_Anode_Fit`

Phase: 004

Date: 2026-05-27

Primary PDF:
`D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`

## Read Coverage

| Source | Pages / Range | Method | Status | Notes |
|---|---:|---|---|---|
| JCP 147, 144111 (2017) PDF | 1-10 | bundled Python `pypdf` text extraction | READ_FULL_TEXT | PDF has 10 pages by `PdfReader`; all page texts were extracted and inspected |
| JCP 147, 144111 (2017) PDF equations | pages 4-5, 8-9 relevant equations | pypdf text plus equation numbering/context | PARTIAL_VISUAL_CONFIDENCE | Exact equation glyphs should be visually checked before final LaTeX transcription |
| Web metadata for ref. 6 | title / DOI / abstract-level metadata | web lookup | checked | Used because local PDF reference list lacks article titles |
| Web metadata for ref. 7 | title / DOI / abstract-level metadata | web lookup | checked | Used because local PDF reference list lacks article titles |

## Bibliographic Identification

### User Paper

| Item | Value |
|---|---|
| Title | Effects of external electric field and anisotropic long-range reactivity on charge separation probability |
| Authors | Kyusup Lee, Seonghoon Lee, Cheol Ho Choi, Sangyoub Lee |
| Journal | The Journal of Chemical Physics |
| Volume / Article | 147, 144111 |
| Year | 2017 |
| DOI | `10.1063/1.5000882` |
| Local evidence | PDF page 1 and page 2 |

### Ref. 6

| Item | Value |
|---|---|
| Local reference entry | S. Lee, C. Y. Son, J. Sung, and S. Chong, J. Chem. Phys. 134, 121102 (2011). |
| Title | Communication: Propagator for diffusive dynamics of an interacting molecular pair |
| DOI | `10.1063/1.3565476` |
| External metadata checked | Son Research Lab publication list; Digital Jiphyeonjeon metadata |
| Method relevance | Introduces a method for Fredholm integral equations of the second kind, useful when direct iterative expansion diverges |

### Ref. 7

| Item | Value |
|---|---|
| Local reference entry | C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, J. Chem. Phys. 138, 164123 (2013). |
| Title | An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity |
| DOI | `10.1063/1.4802584` |
| External metadata checked | Son Research Lab publication list; Ewha Pure metadata |
| Method relevance | Applies the Fredholm second-kind method to steady-state rate constants for diffusion-influenced bimolecular reactions with long-range reactivity |

## In-Text Uses Of Refs. 6/7 In The User Paper

| PDF Page | Context | Role |
|---:|---|---|
| 2 | Introduction | States that the paper uses the recently proposed method of refs. 6/7 for Fredholm integral equations of the second kind to handle external-field and anisotropic long-range reactivity effects |
| 5 | Theory, after Eq. (32) | Identifies the derived equation for `\bar W_u(r)` as a Fredholm integral equation of the second kind and invokes refs. 6/7 for the solution method |
| 8 | Results/discussion around long-range sink model | Uses agreement with numerical results as evidence of the utility of the refs. 6/7 solution method |

No other `6,7` or `Refs. 6 and 7` in-text citation was found by text extraction.

## Method Extracted From The User Paper

The method as used in the 2017 paper is not a direct fixed-point iteration. It has the following structure.

### Step A - Reduce The Physical Problem To A Second-Kind Integral Equation

The paper starts from a steady-state Smoluchowski survival/separation problem and reduces the long-range reaction-sink case to an equation of the schematic form:

```text
W(r) = 1 - integral_kernel[W(r1)]
```

In the paper this is Eq. (32), where the unknown `\bar W_u` appears both outside and inside integrals. This is explicitly classified as a Fredholm integral equation of the second kind.

### Step B - Rewrite Into A Formally Exact Ratio Expression

The paper rewrites Eq. (32) into a reciprocal expression, Eq. (33), whose integrands contain the ratio:

```text
W(r1) / W(r)
```

This step is important because the difficult unknown is moved from the absolute function under the integral to a relative function ratio. That changes the closure problem from "guess the whole unknown function" to "estimate a ratio."

### Step C - Close The Unknown Ratio With A Simpler Reference Problem

The unknown ratio is then approximated by a ratio from a simpler, already solved reference problem:

```text
W(r1) / W(r) ~= W_delta(r1) / W_delta(r)
```

The reference problem is the delta-function sink case with contracted reactivity matched to the long-range sink. In the paper this appears through Eqs. (34)-(38).

### Step D - Obtain A Closed Approximate Expression And Check Regime

After substituting the reference ratio, the paper obtains a closed expression for the separation probability, Eq. (39), and later compares it against finite-element numerical solutions.

The approximation is strongest when:

- the orientation dependence of the survival probability is weak enough for the mean-value / orientation-average approximation;
- the reaction zone is not too broad;
- the central isotropic potential dominates the anisotropic external-field effect;
- the inherent reactivity is not too large.

The paper records deterioration when these assumptions weaken, especially for stronger anisotropic field dominance, smaller Onsager distance, broader effective reaction zone, or larger initial separation.

## Transferable Method Kernel

For the graphite dQ/dV work, the transferable part is not the physical geminate-pair model. The transferable part is the mathematical closure pattern:

```text
1. derive an implicit/self-consistent second-kind integral form;
2. isolate the unknown self-feedback as a ratio or correction functional;
3. choose a simpler reference problem that is physically correct in a limiting case;
4. replace the unknown ratio/correction by the reference ratio/correction;
5. solve the resulting closed expression;
6. verify residual, monotonicity, and limiting behavior.
```

## Caution For Graphite Mapping

The corrected graphite ver.1 dynamics are initially more naturally a causal q-domain integral equation:

```text
xi_j(q) = xi_j(q0) + integral from q0 to q of F_j(s, xi(s), V_n[ xi(s) ]) ds
```

This is Volterra-like in the marching coordinate `q`, while refs. 6/7 are cited here for Fredholm second-kind equations. Therefore the method should be imported as a closure strategy for self-consistency, not as a one-to-one physical or equation-type identity.

The safe mapping target for Phase 005 is:

- algebraic solve: `V_n = root(q, T, xi_j)`;
- integral update: `xi_j(q)` from the ODE written in integral form;
- reference closure: use an analytically solvable or numerically stable baseline path to approximate the feedback correction;
- validation: compare against direct coupled DAE/root-solving iteration.

## Sources

Local:

- JCP 147, 144111 (2017) PDF, pages 1-10.

External metadata:

- Digital Jiphyeonjeon entry for ref. 6: `https://k-knowledge.kr/srch/read.jsp?id=276498112`
- Son Research Lab publication list: `https://songroup.github.io/sonlab-website/publications/`
- Ewha Pure metadata for ref. 7: `https://pure.ewha.ac.kr/en/publications/an-accurate-expression-for-the-rates-of-diffusion-influenced-bimo/`
