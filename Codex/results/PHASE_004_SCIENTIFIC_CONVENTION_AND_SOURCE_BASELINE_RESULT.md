# Phase 004 Scientific Convention and Source Baseline Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 37-54
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Read-coverage gate: `FULL_READ_SCOPE_PASS`
- Phase 003 lineage matrix used as historical context: `D:\Projects\Project_Anode_Fit\Codex\results\v1010_v1023_version_lineage.csv`
- Git commands executed: none
- Writes outside `D:\Projects\Project_Anode_Fit\Codex`: none

## Scope And Method

This phase fixed the convention and evidence baseline used by the Chapter 1-3
scientific audits. It did not edit the Claude source, TeX, code, or Git state.

The following tasks were completed:

1. Built a 34-record registry for symbols, signs, units, normalization bases,
   reference states, model class, and validity domain.
2. Built the composition-to-observable dependency graph across equilibrium
   potential, ICA/DVA, hysteresis, lag, entropy, reversible heat, mechanics,
   blending, and fitting.
3. Extracted 91 bibliography records and 268 actual citation occurrences from
   the final included Chapter 1-3 master paths. The earlier extractor result that
   included the non-included `ch1_appD_si.tex` is superseded.
4. Verified bibliographic identity for all 91 records: 81 through DOI metadata,
   nine through official publisher/library records, and one as a project-internal
   artifact.
5. Recorded 116 claim-level source assessments covering every bibliography key.
6. Screened 74 additional-source records, merged them to 68 unique works, and
   adjudicated all duplicate or conflicting recommendations.
7. Preserved access limits. Abstract-only or metadata-only access was not used to
   adopt equations, numerical coefficients, or material-specific quantitative
   conclusions.

## Canonical Artifacts

| Artifact | Rows or extent | SHA-256 |
|---|---:|---|
| `phase004_scientific_convention_registry.csv` | 34 rows | `893FA2C987D5B45A876007BD9C7A9B37D68A77CBD6B92851B08FD60BA571C3EE` |
| `phase004_model_dependency_graph.md` | complete graph and broken-edge analysis | `C185FF69E30A0392958FC1F7C1341333C1B1D145DEF4E1FE37FE9CFD229F92A0` |
| `phase004_existing_reference_claim_matrix.csv` | 91 references; 268 occurrences | `04669194C4AADEB265267166F7D91D48F6BCFA912CBD8566F63F447456490A88` |
| `phase004_existing_claim_strength_overrides_integrated.csv` | 116 claim assessments | `964973CD6AA1D23B9D11DBEFCA89FC02B1D5A015BE409981409C45384216AC97` |
| `phase004_additional_literature_source_matrix.csv` | 68 unique works | `9351C6E03A1B90FD8FA10AE049717E65FA730ACE0DE058AEC9AEE756F2815834` |
| `phase004_literature_duplicate_map.csv` | 12 duplicate-member rows | `881B3A6DD263E63E12B1BBF52DB70A14A7B724DB4EC7A6AFF0DD10E57F312FEC` |

## Convention Baseline

The registry separates the following classes, which the latest documents often
place too close together in prose:

- exact definitions and mass/charge conservation identities;
- equilibrium statistical-mechanical relations;
- near-equilibrium entropy and reversible-heat relations;
- phenomenological hysteresis, lag, broadening, and smoothing laws;
- numerical regularization and finite-difference devices;
- inverse-fitting assumptions and parameter priors;
- project-specific reductions that are not established material laws.

Four cross-chapter dependency edges are confirmed broken or underdeclared:

1. **Time unit edge:** Chapter 1 accepts C-rate in `h^-1`, while the Eyring lag
   update is seconds-based. Without division by 3600, the lag time scale changes
   by a factor of 3600 under an equivalent Ah-to-coulomb unit representation.
2. **Blend normalization edge:** Chapter 3 converts `m_Si` to `f_Si` while keeping
   graphite capacity fixed. This is a fixed-graphite-addition basis, not a
   total-active-mass weight-fraction basis.
3. **Stress-measure edge:** the Sethuraman thin-film coefficient is equi-biaxial,
   but the document inserts it as hydrostatic without the plane-stress conversion
   or a geometry-specific constitutive map.
4. **Strain-regime edge:** a small-strain scalar Larché-Cahn term is used alongside
   roughly 270-310% Si volume expansion without a finite-deformation validity
   boundary.

These edges are carried into Phases 005-009 as testable findings, not repaired in
this phase.

## Existing Reference Verification

### Coverage

- Bibliography records: 91 / 91 mapped.
- Actual citation occurrences: 268 / 268 mapped.
- Unresolved citation keys: 0.
- References with claim-level disposition: 91 / 91.
- Claim-level assessments: 116.
- Bibliographic identities: 81 DOI metadata, nine manually confirmed, one
  internal project artifact.

Claim-level support dispositions are:

| Status | Count |
|---|---:|
| `supports` | 32 |
| `partially supports` | 33 |
| `insufficient` | 21 |
| `not retrieved` | 19 |
| `contradicts` | 6 |
| `misattributed` | 5 |

The counts are claim-level, so one bibliography key can support one sentence and
fail another. This is why the canonical matrix retains combinations instead of a
single source-wide verdict.

### Confirmed High-impact Source Problems

1. `msmr_partII`: the cited source reports an entropy-coefficient scale near
   0.3 mV K^-1, while the document states approximately +3 to +4 mV K^-1. The
   document value is about one order of magnitude too large.
2. `persson2010b`: the reported migration barriers increase along the cited
   lithiation sequence (approximately 218, 283, 293 meV); the document describes
   a decreasing trend.
3. `msmr_partI`: a generic Advanced Energy Materials Part I DOI is conflated with
   the MCMB Part 1 source. The bibliographic and scientific roles must be split.
4. `bloom2005`: the source is differential-voltage analysis (`dV/dQ`), not the
   `dQ/dV` observable attributed to it.
5. `reynier2004`: approximately 0.18 `k_B/atom` is an electronic state entropy near
   metallic `x ~= 0.833`, not an O3 total partial-molar lithiation-entropy anchor.
6. `reynier2004`: the source does not establish a logistic electronic-entropy gate
   as indispensable or unique; it reports a substantial configurational role and
   a smaller electronic entropy-of-lithiation contribution over O3 outside the
   transition comparison.
7. `motohashi2009`: `g(E_F) = 13 states/eV` is inferred from susceptibility under a
   Pauli-paramagnetic assumption. It is not a direct density-of-states
   measurement.
8. `motohashi2009`: the estimate applies at `x = 0`, O1 CoO2. Its direct transfer
   to the Li-rich O3 metal-insulator window is unsupported.
9. `marianetti2004`: the Mott-transition/coexistence mechanism does not derive the
   chosen logistic kernel or its `Delta x` scale.
10. MSMR origin convention: the source convention uses `f = F/(RT) > 0`; the
    document mapping `f = +sigma_d` is contradicted by that source convention and
    must be re-derived from the project's voltage/current signs.
11. Van der Ven LCO ordering evidence is used to support a single-Omega closure,
    although the source's high-lithiation metal-insulator/two-phase behavior is a
    reason that such a reduction can fail.
12. Wojtala-type total entropy evidence is used as if it separately validates the
    configurational, vibrational, and electronic decomposition. It does not.

The citation matrix preserves exact document locations, source access level,
required correction, and confidence for each item.

## Additional Literature Baseline

### Adjudication

| Decision | Unique works | Meaning |
|---|---:|---|
| `ADOPT` | 20 | Adopt only for the role and access level recorded below. |
| `CANDIDATE` | 21 | Relevant lead requiring more source or section review before final adoption. |
| `HOLD` | 21 | Do not use for current claims; retain for retrieval or future validation. |
| `REJECT` | 6 | Material, regime, evidence, or transfer mismatch makes current adoption unsafe. |

Four duplicate conflicts were adjudicated to `HOLD`, not silently merged:

- Mathiesen et al. 2019, graphite operando PXRD;
- Cui, Gao, and Qu 2012, finite-deformation stress-dependent chemical potential;
- 2021 Journal of Power Sources frequency-domain entropy inference;
- Du et al. 2016, first-principles LCO vibrational thermodynamics.

For all four, identity and prospective use are valid, but the available
abstract/preview is insufficient for equation- or number-level adoption.

### Sources Approved For Bounded Adoption

| ID and source | Exact role | Adoption boundary |
|---|---|---|
| LIT-001, McDowell et al., `10.1002/adma.201301795` | Chapter 3 Si single-host foundation and a warning against direct graphite-to-Si transfer. | Abstract-only; no host-product partition, constant partial molar volume, or coefficient adoption. |
| LIT-003, Newman and Tiedemann, `10.1002/aic.690210103` | Qualify the lumped apparent-voltage correction by naming unresolved porous-electrode gradients. | Does not validate the project's lag or tail kernel. |
| LIT-004, Van der Ven et al., `10.1002/bte2.20210017` | Install a hysteresis taxonomy and relabel the spinodal-gap expression as model-specific. | No unique mapping of graphite loops to one regular-solution `Omega`. |
| LIT-005, Huggins, `10.1007/978-0-387-76424-5` | Shared textbook-level prerequisite and definition order. | Metadata/TOC only; structural citation, not equation evidence. |
| LIT-010, Ferguson and Bazant, `10.1016/j.electacta.2014.08.083` | Replace the direct `Omega > 2RT -> observed hysteresis` implication with an equilibrium/metastability/nucleation/mosaic/transport hierarchy. | LiFePO4-centered quantitative transfer risk. |
| LIT-011, Zhang et al., `10.1016/j.ensm.2020.12.027` | Bridge graphite staging physics to the reduced observable model. | Abstract-only; does not calibrate four centers, widths, or lag. |
| LIT-019, Williford et al., `10.1016/j.jpowsour.2008.10.078` | Add material and protocol uncertainty around `dU/dT` and reversible heat. | Does not separate the document's entropy components. |
| LIT-024, Mukhopadhyay and Sheldon, `10.1016/j.pmatsci.2014.02.001` | Declare the scalar Larché-Cahn term a first-order local coupling and expose omitted finite-deformation/plasticity/geometry layers. | Does not provide Sethuraman biaxial-to-hydrostatic conversion or constant `v_bar_Li`. |
| LIT-025, Zhang et al., `10.1016/j.pmatsci.2017.04.014` | Separate chemistry, transport/contact loss, SEI, and mechanics in Chapter 3 degradation taxonomy. | Review scope; no host-current partition coefficient. |
| LIT-027, van de Walle and Ceder, `10.1016/S0378-7753(99)00237-2` | Present single-Omega LCO as a coarse reduction of cluster interactions. | Abstract-only; no single-Omega or universal hysteresis calibration. |
| LIT-028, Stuart, `10.1017/S0962492910000061` | Add a shared inverse-problem boundary and uncertainty requirement. | General method source; no battery-specific prior or likelihood. |
| LIT-030, Baek et al., `10.1021/acs.jpcc.1c10414` | Primary tutorial citation for entropic-potential definitions and measurement interpretation. | Abstract-only in this pass; cannot validate additive factorization or component magnitudes. |
| LIT-035, Bassey et al., `10.1021/jacs.2c02927` | Separate measured LCO local structure from the phenomenological electronic gate. | Spectroscopy does not calibrate the gate. |
| LIT-037, Moon et al., `10.1038/s41467-021-22662-7` | Direct evidence that finite-rate/cycled Si-graphite partition and mechanics can break an equilibrium weighted-sum description. | One formulation/protocol; no universal partition law. |
| LIT-038, Eshetu et al., `10.1038/s41467-021-25334-8` | Require material identity, mass/capacity basis, lithium inventory, and formulation domain around `f_Si`. | Practical ranges are formulation-dependent. |
| LIT-040, Zhang, `10.1038/s41524-017-0009-z` | Define the omitted chemomechanical constitutive layer beside the scalar equilibrium coupling. | Review, not a parameter source for this blend. |
| LIT-041, Lu et al., `10.1038/s41565-025-02027-7` | Strong direct boundary for host partition/degradation and omitted porosity/CBD states. | Recent single-study formulation space; no universal degradation coefficient. |
| LIT-049, Dresselhaus and Dresselhaus, `10.1080/00018730110113644` | Open Chapter 1 with graphite staging taxonomy and label the logistic sum as a reduced representation. | Abstract-only; no specific transition parameters. |
| LIT-050, Raue et al., `10.1093/bioinformatics/btp358` | Require structural/practical identifiability and profile-likelihood or equivalent correlation evidence. | Method criterion only; no present parameter is thereby shown identifiable. |
| LIT-055, Rao and Newman, `10.1149/1.1837884` | External energy-balance anchor for reversible heat; internal numerical tests remain reproducibility evidence only. | Abstract-only; project sign convention and omitted heat terms remain to be derived. |

### Literature-gap Taxonomy

The Chapter 1-3 strengthening work must address these gaps:

- microscopic phase/staging evidence versus reduced logistic components;
- equilibrium hysteresis, metastability, nucleation, memory, and transport;
- broadening-source separability and inverse identifiability;
- LCO configuration/electronic/vibrational coupling near transitions;
- single-electrode versus full-cell entropy-coefficient inference;
- reversible-heat sign and complete energy balance;
- Si phase/amorphization path dependence and finite deformation;
- Si/graphite mass, capacity, lithium-inventory, and host-current bases;
- degradation, porosity, conductive-binder-domain, SEI, and contact-loss states;
- real-data validation and uncertainty, which synthetic tests cannot close.

## Analytic Limits And Later Tests

The baseline requires later audits to test, at minimum:

- zero interaction, zero current, zero lag, zero broadening, and one-component limits;
- separated, overlapping, and identical-center transition limits;
- complete-affinity forward/reverse normalization;
- hours-to-seconds invariance of the lag law;
- entropy derivative and reversible-heat sign under the fixed current convention;
- electronic-gate-off comparison with all non-electronic parameters refit or held
  under a declared counterfactual;
- zero-Si, pure-Si, fixed-total-mass, and fixed-graphite-addition blend limits;
- plane-stress biaxial-to-hydrostatic conversion and finite-strain applicability;
- structural and practical identifiability under initialization and noise changes.

## Access Limits And Unverified Items

- Nineteen existing-source claim assessments remain `not retrieved`; their
  bibliography and claim locations are known, but no scientific support is
  inferred from identity alone.
- Several adopted review/textbook sources were available only as abstract,
  metadata, TOC, or targeted sections. Their adoption is deliberately structural
  or classificatory.
- Paywalled full text is marked by access state in the matrices. It is not treated
  as silently verified.
- No company experimental dataset was available in this phase. Real-data model
  validity and parameter identifiability remain open.
- The source baseline does not itself prove that any document equation or code
  implementation is correct; that burden belongs to Phases 005-009.

## Gate

`SOURCE_BASELINE_PASS`

Reason: every existing bibliography record and actual citation occurrence has a
bibliographic and claim-level disposition; every additional source has an exact
role, target, access state, transfer risk, and adoption decision; unresolved
access is explicitly marked rather than promoted to evidence. This gate closes
traceability and convention setup only. It does not close chapter correctness,
structure quality, or document-code fidelity.

