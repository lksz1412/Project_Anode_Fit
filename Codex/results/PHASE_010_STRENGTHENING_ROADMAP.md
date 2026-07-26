# Phase 010 Scientific Strengthening Roadmap

## Purpose And Boundary

This roadmap converts the v1.0.10-v1.0.23 audit into an implementation order.
It does not edit the SHA-pinned source. Every action below must preserve current
labels and user naming unless an explicitly approved correction requires a new
interface. A passing build or same-model regression is necessary but not
sufficient for scientific closure.

## Priority Order

| Priority | Meaning | Release consequence |
|---|---|---|
| P0 | Quantitative correctness or source-identity blocker | Correct before any scientific release or fitting use. |
| P1 | Model-domain, identifiability, and evidence blocker | Correct before mechanistic interpretation or review-level claims. |
| P2 | Experimental and uncertainty closure | Required before parameter validation or predictive use. |
| P3 | Structure, pedagogy, and release-surface cleanup | Perform after P0-P2 meanings are stable. |

## P0 - Immediate Corrections

### P0-1 Canonicalize the time basis

- Public `curve(c_rate)` is in `h^-1`; the Eyring chain uses seconds. Convert
  `I/Q` to `s^-1` exactly once at the public-to-kinetic interface.
- State units for `I`, `Q_cell`, `c_rate`, `L_q`, and `L_V` in the Chapter 1
  equation and code API.
- Add an invariance test showing identical curves for `1 C` represented as
  `1 h^-1` and `1/3600 s^-1`.
- Re-run the inherited Chapter 3 blend path because it delegates to the same host
  kinetics.
- Acceptance: the previous factor-3600 difference is below numerical tolerance
  and no duplicate conversion exists downstream.

### P0-2 Replace or demote the Appendix E ratio law

- Derive the local correction from the complete forward-plus-reverse affinity,
  including the local reverse-rate denominator.
- If the complete expression is not adopted, rename the existing switch as a
  forward-factor-only approximation and remove `certificate` or equivalent
  accuracy language.
- Validate against an independent nonlinear IVP/BVP solver with residual,
  convergence, grid-refinement, and perturbation-order studies. Same-update
  Picard iteration is a convergence diagnostic, not an independent oracle.
- Define the finite-window incoming-history state and FFT boundary contract.
- Acceptance: documented and implemented equations match; the error claim is
  bounded over a declared parameter domain; edge-impulse wraparound is absent or
  explicitly part of the API semantics.

### P0-3 Rebuild the LCO electronic source chain

- Correct the Reynier attribution: approximately `0.18 k_B/atom` is not an O3
  total partial-molar lithiation-entropy anchor.
- Treat Motohashi's `13 electrons/eV` as a susceptibility-derived, Pauli-
  assumption endpoint estimate for O1 `x=0`, not a direct `/atom` DOS measurement
  or an O3 `x~=0.85` gate height.
- Remove claims that the cited literature derives the logistic kernel,
  `Delta x=0.05`, electronic-only uniqueness, or the present peak amplitude.
- Either source an O3-local composition law and normalization directly or retain
  the gate as a Tier-C project ansatz whose parameters must be jointly fitted.
- Implement local composition and dynamic temperature only as a paired path:
  `Delta S_e(x,T)` and the corresponding `T^2` center integral must round-trip.
- Acceptance: source identity, phase, composition, normalization, access level,
  and model/adaptation status are adjacent to the first equation and default.

### P0-4 Fix blend normalization and capacity denominators

- Add an explicit basis selector separating fixed-total-active-mass and
  fixed-graphite-plus-added-Si experiments.
- In fixed-total-mass mode, scale graphite by `(1-m_Si)` and Si by `m_Si` before
  converting to the internal capacity fraction.
- Preserve the current additive basis under an unambiguous name because its
  mathematics is internally consistent for that experiment.
- Declare every `q_Si` denominator and cycle state: per gram of elemental Si,
  per gram of SiO compound, per gram of Si-C composite, or per total active mass.
- Remove the generic interpretation of Andersen's 3117 mAh/g as a universal
  Si-C composite capacity; it is effectively normalized to the Si content of the
  reported formulation.
- Acceptance: zero-Si, pure-Si, fixed-mass, additive-mass, and 10/20/30 wt% cases
  pass against independent hand calculations.

### P0-5 Correct the Chapter 3 mechanics boundary

- Separate equi-biaxial thin-film stress from hydrostatic stress. State the
  plane-stress relation before any coefficient conversion.
- Report Sethuraman's theoretical approximately 60-62 mV/GPa and measured
  approximately 100-125 mV/GPa slopes separately; do not collapse their
  40-50% difference into one universal coefficient.
- Label the linear scalar Larché-Cahn expression as a first-order local coupling.
  Put finite deformation, composition-dependent partial molar volume,
  compliance derivative, geometry, plasticity, contact, and SEI outside its
  quantitative validity domain unless implemented.
- Keep the verified stress sign. The defect is stress measure/domain transfer,
  not the tension-positive sign chain.
- Rename the runtime input as a precomputed stress-induced voltage offset or add
  a typed stress adapter only after the constitutive map is specified.
- Acceptance: no particle/composite prediction cites a thin-film biaxial number
  as hydrostatic without derivation and uncertainty.

### P0-6 Correct width defaults and precedence

- Make the no-`n`, no-`w` path return `dw/dT = R/F`, consistent with its default
  `n=1` width.
- Resolve the API ambiguity when both `n` and `w` are present. Preserve existing
  names, but reject or warn on the inactive field and document the controlling
  parameter.
- Audit LCO presets because their displayed `w` values are currently inert when
  `n=1` is also present.
- Acceptance: analytic, automatic/finite-difference, and default-path
  temperature derivatives agree.

### P0-7 Correct the LCO ordering model class

- Stop describing a one-composition regular solution with positive `Omega` as
  an ordering model. In that state space it produces a demixing instability;
  it cannot represent an ordered phase at `x=0.5` without an order parameter,
  sublattice state, or equivalent cluster description.
- Choose one of two explicit paths: implement a source-grounded
  order-parameter/sublattice/cluster model with corresponding code and data, or
  demote the current term to a phenomenological transition fit with no literal
  microscopic-ordering claim.
- Re-audit the labels `T2`, `T3`, `order`, `ordering`, and every surrounding
  entropy interpretation after the model-class decision.
- Acceptance: no literal ordering claim is made without a state variable that
  can distinguish ordered and disordered configurations at the same overall
  composition; equations, code, defaults, and references trace to the selected
  model class.

## P1 - Chapter 1 Scientific Closure

1. Retain Part 0 in the main master and add a 2-4 page fast-route map.
2. Put a status hierarchy before hysteresis parameters: equilibrium binodal,
   metastability/spinodal, nucleation/mosaic, porous-electrode polarization,
   path memory, and project phenomenology.
3. Label the independent logistic response and the regular-solution double-well
   as two model strata unless an implicit interacting equilibrium solver is used.
4. Replace the claimed Persson barrier trend with the source's increasing-
   barrier/decreasing-diffusivity trend, or remove it as an initialization
   rationale.
5. Replace potassium-graphite as the load-bearing Li stage-class source with
   material-matched Li-graphite evidence after full-text retrieval.
6. Keep exact staging voltage anchors `미검증` until a fully read primary passage
   establishes material, temperature, protocol, and reference.
7. Split the MSMR Part I/Part II bibliography identities. Correct the MCMB
   reversible-heat scale from the document's `3-4 mV/K` to the source-supported
   order of `0.3 mV/K`: Paul et al. Part II Figure 1 reaches approximately
   `2.8e-4 V/K`, with composition-dependent sign changes. Audit all plots,
   prose, defaults, and heat calculations that inherited the factor-of-ten
   error; preserve the source's protocol and normalization limits.
8. Add explicit incoming memory state, path order, reversal handling, and
   finite-window prehistory to the API contract.
9. State that PSD, strain, disorder, instrument, and transport broadening are not
   separable from one peak width without orthogonal priors.
10. Add a finite-mixture inverse section with sensitivities, correlations,
    profile likelihood or equivalent, non-uniqueness examples, and multi-rate/
    multi-temperature data requirements.

## P1 - Chapter 2 Scientific Closure

1. Label Chapter 2 as a dependent volume chapter and add a compact inherited-
   equation/state recap instead of duplicating Chapter 1.
2. Put measured LCO phase/order/entropy evidence before the effective reduction.
   Separate direct observation, calculation, project factorization, frozen
   approximation, and Tier-C ansatz.
3. Present cluster-expansion/order evidence as a reason that a single symmetric
   `Omega` may fail, not as proof of equivalence.
4. Put the electronic-gate source/status warning before first use and expose the
   non-identifiable ratio `g_max/Delta x`.
5. Make gate-off ablation reference preserving: refit or consistently reset the
   reference enthalpy/center instead of counting a calibration shift as the
   electronic contribution.
6. Do not interpret fitted two-phase width as equilibrium configurational
   entropy without material- and protocol-specific evidence.
7. Do not average charge/discharge entropy slopes into a reversible equilibrium
   quantity unless antisymmetry, common center, path independence, and
   temperature behavior are demonstrated.
8. Treat the one-mode Einstein term as a reduced residual basis, not a measured
   phonon reaction spectrum.
9. Add local inverse/identifiability, validity/UQ, fitting, and reproducibility
   closures. Separate single-electrode, Li-reference, and full-cell heat signs.

## P1 - Chapter 3 Scientific Closure

1. Keep the survival map first, preceded only by a concise material, cycle,
   history, reference-state, geometry, and normalization orientation.
2. Qualify the common-chemical-potential balance: it is exact at equilibrium;
   the host-product factorization and additive pure-host observables require an
   independent-host closure.
3. Label component curves as latent reduced-model terms unless independently
   measured. Do not infer host current partition from the additive curve.
4. Add cycle index, cutoff, crystallinity/amorphization, and phase-path state to
   the case contract before generalizing first-cycle/subsequent-cycle behavior.
5. Do not attribute approximately 40% SiOx lithium consumption to silicate/Li2O
   from initial Coulombic efficiency alone; separate SEI, trapped Li, conversion
   products, and inactive material.
6. Describe Andersen's 1200-cycle result as capacity-limited and resistance-
   increasing, not as unconditional stability.
7. Add explicit output exclusions for fracture/LAM, SEI/lithium inventory,
   porosity/CBD, contact, and finite-rate host switching.
8. Demonstrate exact non-identifiability of center/stress offset and of
   `m_Si`/`q_Si`; require orthogonal mechanical, compositional, operando, and
   inventory data before mechanistic interpretation.
9. Move API signatures and detailed gate procedures to a same-master appendix;
   retain compact G1-G3 and GS-1/GS-2 scientific meanings in the body.

## P2 - Validation And Uncertainty Program

### Common experimental matrix

- At least three temperatures spanning the intended operating window, with
  equilibrated potentiometry and a documented reference-electrode convention.
- Multiple low rates plus current interrupts to separate quasi-equilibrium,
  polarization, lag, and memory.
- Replicates and reported measurement uncertainty; raw sampling and smoothing
  settings for ICA/DVA.
- Train/holdout split by rate, temperature, and cell/electrode batch.
- Competing-model comparison, model-discrepancy term, and posterior/profile
  uncertainty rather than one optimum and a same-model round trip.

### Chapter-specific data

- Chapter 1: operando Li-graphite staging/heterogeneity, independently measured
  particle/structural priors, and reversal/cropped-window protocols.
- Chapter 2: composition-resolved single-electrode `dU/dT`, phase/ordering
  observables, electronic/phonon comparators, and full-cell sign validation kept
  separate from half-cell inference.
- Chapter 3: formulation-resolved mass/capacity inventory, host-resolved operando
  signals, thickness/porosity/CBD evolution, stress under defined geometry,
  cycle/cutoff history, and Si/SiOx/Si-C material identity.

### Acceptance metrics

- Structural and practical identifiability reported for every interpreted
  parameter or combination.
- Profile likelihood, posterior correlation, or equivalent nonlinearity-aware
  interval; Fisher/Hessian results alone require stated local assumptions.
- Residual structure and holdout error by rate, temperature, direction, and
  material batch.
- Conservation, unit invariance, reference-state round trip, zero limits, and
  independent-oracle tests separated from empirical validation.

## Literature Integration - Adopt Now Within Recorded Bounds

| Source | Exact placement and purpose | Must not be used for |
|---|---|---|
| [Raue et al. 2009](https://doi.org/10.1093/bioinformatics/btp358) | Common inverse-method section; profile likelihood and structural/practical identifiability. | Evidence that the present battery parameters are identifiable. |
| [Dubarry and Ansean 2022](https://doi.org/10.3389/fenrg.2022.1023555) | Ch1 after the ICA/DVA peak equation and in the method table; acquisition, preprocessing, sign, noise, and peak-quality guardrails. | Graphite phase assignment or calibration of the project kernel. |
| [Yao et al. 2019](https://doi.org/10.1039/C8EE02373E) | Ch1 broadening/lag validity; porous-electrode concentration-gradient confounding. | Width or lag-parameter calibration. |
| [Kim et al. 2020](https://doi.org/10.1039/C9EE02964H) | Ch2 pre-model evidence; LCO ordering and entropy constraints before reduction. | A universal `Omega`, gate, or numerical entropy parameter. |
| [Hudak et al. 2015](https://doi.org/10.1149/2.0071503jes) | Ch2 decomposition and validation; localized entropy-feature aging and parameter-stationarity limits. | A universal aging coefficient. |
| [Otero et al. 2018](https://doi.org/10.1038/s41598-018-33405-y) | Ch3 before wt% conversion and in the API basis; fixed-total-active-mass capacity accounting. | Universal transfer to other formulations or additive-mass normalization. |
| [Moon et al. 2021](https://doi.org/10.1038/s41467-021-22662-7) | Ch3 blend/GS-2 boundary; host crosstalk and mechanical degradation. | A universal host-partition law. |
| [Sethuraman et al. 2010](https://doi.org/10.1149/1.3489378) | Ch3 mechanics before scalar coupling; biaxial geometry, plane stress, and theory/measurement separation. | Direct hydrostatic or particle/composite transfer. |
| [Zhang 2017](https://doi.org/10.1038/s41524-017-0009-z) | Ch3 GS-1 validity envelope; omitted finite-strain/plastic constitutive layer. | Validation of the present linear scalar coupling. |
| [Berliner et al. 2021](https://doi.org/10.1149/1945-7111/ac26b1) | Ch2/3 inverse/UQ sections; battery-specific nonlinear identifiability and orthogonal-data discipline. | Numerical P2D parameter transfer. |
| [Lu et al. 2025](https://doi.org/10.1038/s41565-025-02027-7) | Ch3 strongest current porosity/CBD/heterogeneous-utilization boundary. | A universal degradation coefficient outside the tested formulations. |

This list is narrower than the provisional Phase 004 `ADOPT` set. Immediate
claim-level adoption requires full text actually read in this audit and remains
limited to the role stated above; it is not blanket approval of the paper.

## Literature Integration - Retrieve Or Validate Before Adoption

| Source/need | Next action | Target |
|---|---|---|
| van de Walle and Ceder 1999, `10.1016/S0378-7753(99)00237-2` | Retrieve full text before delimiting cluster-interaction-to-single-`Omega` reduction. | Ch2 LCO model class. |
| Baek et al. 2022, `10.1021/acs.jpcc.1c10414` | Retrieve full text before importing entropic-potential definitions or validity equations. | Ch2 entropy interpretation. |
| Dresselhaus and Dresselhaus 2002, `10.1080/00018730110113644` | Retrieve exact staging passages before detailed taxonomy use. | Ch1 staging. |
| Rao and Newman 1997, `10.1149/1.1837884` | Retrieve equation-level text before replacing the internal heat-balance authority. | Ch2 reversible heat. |
| Lian and Bazant 2024, `10.1149/1945-7111/ad1e3d` | Retrieve the full body only if fast-charge/plating scope is added. | Ch1 competing mechanisms. |
| Park et al. 2021, `10.3390/ma14164683` | Re-read the full source before retaining broad width-origin claims. | Ch1 diffusion/broadening. |
| Mathiesen et al. 2019, `10.1016/j.carbon.2019.06.103` | Retrieve and read full methods/results before using detailed Li-graphite phase assignments. | Ch1 staging and broadening. |
| Smith, Khoo, and Bazant 2017, `10.1021/acs.jpcc.7b00185` | Read full graphite model and define which stage/kinetic assumptions transfer. | Ch1 reduced thermodynamics/kinetics. |
| Viswanathan et al. 2010, `10.1016/j.jpowsour.2009.11.103` | Use the fully read paper to build a half-cell/full-cell sign and reference validation hierarchy. | Ch2 reversible heat. |
| Reimers and Dahn 1992, `10.1149/1.2221184` | Retrieve full text; use structure/topology only unless a separate fit identifies `Omega`. | Ch2 phase evidence. |
| Bower et al. 2011, `10.1016/j.jmps.2011.01.003` | Complete end-to-end derivation review before implementing finite-strain/plasticity terms. | Ch3 GS-1 escalation. |
| Laue et al. 2021, `10.1007/s10800-021-01579-5`; Galuppini et al. 2023, `10.1016/j.jpowsour.2023.233009` | Adapt only as experiment-design/identifiability precedent, not parameter evidence. | Chapter-local inverse sections. |

## Literature Integration - Rejected Direct Transfers Under Current Access

- McDowell et al. (`LIT-001`), Newman and Tiedemann (`LIT-003`), Huggins
  (`LIT-005`), the Zhang graphite review (`LIT-011`), and Stuart (`LIT-028`)
  were available only as abstract, metadata, or table of contents in this audit.
  They cannot support equations, coefficients, or load-bearing claims without
  retrieval. Raue and Berliner already cover the immediate inverse-method need.
- Wong et al. (`LIT-064`) concerns parallel-cell DVA. Its system topology does
  not directly support the present single-cell method and it is rejected for
  that transfer, independently of access quality.

## P3 - Structure And Release Surfaces

- Keep Chapter 1 Part 0; add fast navigation and a canonical width/status table.
- Declare Chapter 2's dependent-volume genre and move LCO-only inputs local.
- Declare Chapter 3 a literature-grounded research roadmap with bounded textbook
  derivations, not a closed standalone review.
- Give every load-bearing claim a local class: identity, equilibrium relation,
  reduced model, phenomenology, numerical device, hypothesis, or future work.
- Put inverse/identifiability, validity/UQ, and reproducibility checkpoints in all
  three chapters, ordered according to each chapter's dependency graph.
- Update the v1.0.23 reference ledger, fitting guide, handover QA state, and
  Chapter 3 future-tense implementation prose.
- Decide whether `appendix_phase_separation.pdf` is restored or explicitly
  excluded. Preserve the TeX and audit history.
- After any authorized move, rebuild all masters, resolve cross-document labels,
  inspect every rendered page, and rerun equation/code traceability.

## Completion Gates

1. `P0_CORRECTNESS_PASS`: all seven P0 families corrected and independently tested.
2. `SOURCE_CLAIM_PASS`: every changed load-bearing source has full access state,
   exact passage, role, and transfer boundary.
3. `IDENTIFIABILITY_PASS`: interpreted parameter combinations have structural and
   practical identifiability evidence or are explicitly reported as latent.
4. `EMPIRICAL_VALIDATION_PASS`: held-out material/rate/temperature data and
   uncertainty/model discrepancy are reported.
5. `DOC_CODE_PASS`: all load-bearing equations and public APIs agree after the
   science is corrected; disclosed approximations and nonimplementations remain
   visible.
6. `STRUCTURE_PASS`: the 18-row Phase 008 map is implemented without broken labels
   or changed scientific meaning.

Until gates 1-5 close, the chapters are suitable as a sophisticated research
derivation and roadmap, not as a validated fitting reference or publication-
ready textbook/review authority.
