# Phase 010 Sol Critique Summary

> Integrated adjudication note: this critic originally classified `P10-R001` as
> a new root. Full-ledger reread showed that it duplicates `P6-CH2-009`, whose
> effect already states that positive `Omega` gives demixing and literal ordering
> requires a sublattice/order parameter. The master review merges the evidence,
> upgrades `P6-CH2-009` to Critical, and does not double-count `P10-R001`.

## Scope And Verdict

- Critic scope: literature, structure/genre, version history, and document-to-code fidelity for the canonical snapshot `8ea83fc6825d2e62c360e08d7738ef26d3171914`.
- Refutation rule: every inherited conclusion was treated as a hypothesis. `AFFIRM` means the attempted refutation failed against the cited evidence; it is not proof beyond the reviewed scope.
- Overall verdict: the three-chapter architecture is defensible, but the current artifact is not an unqualified closed textbook/review volume. Chapter 1 is a conditional textbook foundation plus graphite review/application; Chapter 2 is a dependent LCO volume chapter, not a standalone review; Chapter 3 is a literature-grounded research roadmap, not a closed textbook/review chapter.
- Highest-impact independent modification: the LCO T2/T3 "ordering" construction has a model-class defect. A symmetric positive-`Omega` one-composition regular solution destabilizes `x=1/2` into composition demixing; it does not represent a Li/vacancy ordered `x=1/2` phase without an order parameter, sublattices, or a cluster-interaction model.
- Code verdict: label coverage and many reduced equations are exact, but exact transcription coexists with one public time-unit mismatch, shared invalid/incomplete equations or defaults, disclosed approximations, and explicit nonimplementations. A global `DOC_CODE_PASS` is therefore rejected.

## Exact Read Coverage

All ranges below were directly read. Long files were read in bounded consecutive ranges; the two previously truncated Chapter 1 reads were repeated as `1-130` plus `131-257`, and `1-120` plus `121-240` plus `241-336`. No unlisted file is represented here as fully read merely because it was searched, parsed, built, or compared mechanically.

### Instructions And Mandatory Canonical Records

- `D:/Projects/AGENTS.md`: lines 1-83.
- `Codex/AGENTS.md`: lines 1-180.
- `Codex/plans/2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`: lines 1-342.
- `Codex/results/PHASE_001_010_EXECUTION_LEDGER.md`: lines 1-135.
- `Codex/results/PHASE_003_V1010_V1023_LINEAGE_AUDIT_RESULT.md`: lines 1-243.
- `Codex/results/v1010_v1023_version_lineage.csv`: lines 1-301.
- `Codex/results/phase003_lineage_falsification.csv`: lines 1-89.
- `Codex/results/PHASE_004_SCIENTIFIC_CONVENTION_AND_SOURCE_BASELINE_RESULT.md`: lines 1-245.
- `Codex/results/phase004_existing_reference_claim_matrix.csv`: lines 1-94.
- `Codex/results/phase004_additional_literature_source_matrix.csv`: lines 1-69.
- `Codex/results/PHASE_005_CH1_SCIENTIFIC_AUDIT_AND_STRENGTHENING_RESULT.md`: lines 1-180.
- `Codex/results/PHASE_006_CH2_SCIENTIFIC_AUDIT_AND_STRENGTHENING_RESULT.md`: lines 1-174.
- `Codex/results/PHASE_007_CH3_SCIENTIFIC_AUDIT_AND_STRENGTHENING_RESULT.md`: lines 1-179.
- `Codex/results/PHASE_008_TEXTBOOK_REVIEW_THREE_CHAPTER_STRUCTURE_RESULT.md`: lines 1-167.
- `Codex/results/phase008_adjudicated_structure_scores.csv`: lines 1-31.
- `Codex/results/phase008_reorganization_map.csv`: lines 1-19.
- `Codex/results/PHASE_009_CH1_CH3_DOC_CODE_FIDELITY_RESULT.md`: lines 1-160.
- `Codex/results/equation_code_traceability.csv`: lines 1-64.
- `Codex/work/agent_reports/phase009/P9_code_fidelity_findings.csv`: lines 1-20.
- `Codex/results/scientific_claim_evidence_ledger.csv`: lines 1-56.

### Final v1.0.23 Masters And Chapter 1 Foundation

Root for the following snapshot paths: `Codex/work/source_snapshots/8ea83fc6825d2e62c360e08d7738ef26d3171914/Claude/docs/v1.0.23`.

- `ch1_graphite_v1.0.23.tex`: lines 1-58; `ch2_lco_v1.0.23.tex`: lines 1-31; `ch3_si_v1.0.23.tex`: lines 1-30.
- `_sections/ch1_sec00_intro.tex`: lines 1-94.
- `_sections/ch1_sec01_n0n1.tex`: lines 1-257.
- `_sections/ch1_sec02a_part0.tex`: lines 1-391.
- `_sections/ch1_sec02b_part0.tex`: lines 1-474, including a separate reread of lines 223-258 after an earlier truncation concern.
- `_sections/ch1_sec04_hys.tex`: lines 1-336.
- `_sections/ch1_sec05_width.tex`: lines 1-415.
- `_sections/ch1_sec06_eqpeak.tex`: lines 1-89.
- `_sections/ch1_sec07_broadening.tex`: lines 1-357.
- `_sections/ch1_sec08_lag.tex`: lines 1-145.
- `_sections/ch1_sec09_tail.tex`: lines 1-245.
- `_sections/ch1_sec10_sum.tex`: lines 1-170.
- `_sections/ch1_sec18_inputs.tex`: lines 1-70.
- `_sections/ch1_appB_codemap.tex`: lines 1-157.
- `_sections/ch1_appE_selfconsistent.tex`: lines 1-212.
- `_sections/ch1v22_partT_divider.tex`: lines 1-14.

### Part T And LCO Material Chapter

- `_sections/ch2_sec00_intro.tex`: lines 1-71; `ch2_sec01_partition.tex`: 1-149; `ch2_sec02_config.tex`: 1-190; `ch2_sec03_vibel.tex`: 1-118; `ch2_sec04_einstein.tex`: 1-207; `ch2_sec05_mixing.tex`: 1-245.
- `_sections/ch2_sec06_limits.tex`: lines 1-53; `ch2_sec07_revheat.tex`: 1-102; `ch2_sec08_synthesis.tex`: 1-231; `ch2_sec09_method.tex`: 1-64; `ch2_sec10_closing.tex`: 1-29.
- `_sections/ch2v22_sec00_intro.tex`: lines 1-11; `ch2v22_notation.tex`: 1-14; `ch2v22_bib.tex`: 1-21.
- `_sections/ch1_sec11_lcointro.tex`: lines 1-175; `ch1_sec12_lcocenter.tex`: 1-112; `ch1_sec13_lcohys.tex`: 1-223; `ch1_sec14_lcodecomp.tex`: 1-143; `ch1_sec15_lcoelec.tex`: 1-396; `ch1_sec16_lcopeak.tex`: 1-70; `ch1_sec17_msmr.tex`: 1-176.

### Chapter 3

- `_sections/ch3v22_sec00_intro.tex`: lines 1-12; `ch3v22_notation.tex`: 1-46.
- `_sections/ch3v22_sec01_map.tex`: lines 1-132; `ch3v22_sec02_cases.tex`: 1-162; `ch3v22_sec03_blend.tex`: 1-278; `ch3v22_sec04_mech.tex`: 1-111; `ch3v22_sec05_code.tex`: 1-70; `ch3v22_bib.tex`: 1-42.

### Operator Documents, Code Maps, Code, And Source Checks

- `Claude/docs/v1.0.23/FITTING_GUIDE.md`: lines 1-137.
- `Claude/docs/v1.0.23/CODE_GUIDE_v23.md`: lines 1-196.
- `Claude/docs/v1.0.23/_sections/ch1_appB_codemap.tex`: lines 1-157.
- `Claude/docs/v1.0.23/_sections/ch2_appB_codemap.tex`: lines 1-75.
- `Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py`: controlling ranges 90-252, 360-478, 479-705, 719-926, 945-1020, 1084-1145, and 1180-1404.
- `Codex/work/phase006/ch2_motohashi2009_full_source_check.md`: lines 1-50.
- `Codex/work/phase007/ch3_sethuraman_geometry_source_check.md`: lines 1-86.

### Version-Control And Authorship Artifacts

Snapshot root is the same SHA path stated above.

- v1.0.20: `Claude/docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` lines 1-207; `Claude/docs/v1.0.20/HANDOVER_v1.0.20.md` lines 1-74.
- v1.0.21: `Claude/plans/2026-07-16-v1021-master-plan.md` lines 1-76; `Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md` lines 1-19; `Claude/docs/v1.0.21/HANDOVER_v1.0.21.md` lines 1-24; `Claude/docs/v1.0.21/appendix_phase_separation.tex` lines 1-497.
- v1.0.22: `Claude/plans/2026-07-17-v1022-master-plan.md` lines 1-99; `Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md` lines 1-147; `Claude/docs/v1.0.22/plans/PLAN_R5_ch3_authoring.md` lines 1-45; `Claude/docs/v1.0.22/results/comp_R5/BRIEF_R5.md` lines 1-32; `Claude/docs/v1.0.22/results/comp_R5/CHERRYPICK_R5.md` lines 1-18; `Claude/docs/v1.0.22/ch2_lco_v1.0.22.tex` lines 1-31; `Claude/docs/v1.0.22/ch3_si_v1.0.22.tex` lines 1-30.
- v1.0.22 W1 under `Claude/docs/v1.0.22/results/comp_R5/W1`: `DESIGN_NOTE.md` 1-83; `notation.tex` 1-32; `s31_map.tex` 1-104; `s32_cases.tex` 1-104; `s33_blend.tex` 1-172; `s34_mech.tex` 1-116; `s35_code.tex` 1-77.
- v1.0.22 W2 under `Claude/docs/v1.0.22/results/comp_R5/W2`: `DESIGN_NOTE.md` 1-87; `notation.tex` 1-50; `s31_map.tex` 1-100; `s32_cases.tex` 1-102; `s33_blend.tex` 1-120; `s34_mech.tex` 1-75; `s35_code.tex` 1-58.
- v1.0.22 W3 under `Claude/docs/v1.0.22/results/comp_R5/W3`: `DESIGN_NOTE.md` 1-115; `notation.tex` 1-47; `s31_map.tex` 1-133; `s32_cases.tex` 1-103; `s33_blend.tex` 1-122; `s34_mech.tex` 1-81; `s35_code.tex` 1-68.
- v1.0.23: `Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md` lines 1-32; `results/HANDOVER_v23.md` 1-43; `results/qa_images/CURVE_QA_v23.md` 1-38; `appendix_phase_separation.tex` 1-497.

### Mechanical Comparisons, Not Substitutes For Full Reading

- v1.0.10 versus v1.0.11: both Python files have 851 lines and scientific assets compare byte-equal; eight process/package assets were dropped. This was a byte/inventory comparison, not a claim that every package file was read end-to-end in this phase.
- v1.0.19 versus v1.0.20: the 1151/1152-line Python files have identical abstract syntax trees. The v1.0.20 plan and handover were separately read in full as listed above.
- v1.0.22 versus v1.0.23: all 17 Chapter 2 and 8 Chapter 3 included section bodies compare byte-equal; normalized PDF scientific text is equivalent. Master roots/PDF binaries are not byte-identical because wrappers/metadata differ.
- W-stream overlap was reproduced mechanically after all W1/W2/W3 source files were read in full: final map W3 114/119, cases W2 85/153, blend W1 130/248, mechanics W1 87/94, code W3 44/62, notation W3 24/41 exact-line overlaps.

## Internet, DOI, And Official-Source Checks

Searches were performed on 2026-07-19 using exact title plus DOI, DOI resolver, and official publisher/repository domains. Full text was required for equation, coefficient, or claim-level adoption. Metadata, abstract, table-of-contents, or limited-section access was not upgraded to full-text evidence.

| Source | DOI/official URL | Access obtained | Exact endorsed role |
|---|---|---|---|
| Raue, Kreutz, Timmer | https://doi.org/10.1093/bioinformatics/btp358 | Official OUP full HTML | Common profile-likelihood/structural-practical identifiability method; no battery priors. |
| Dubarry, Anseán | https://doi.org/10.3389/fenrg.2022.1023555 | Official Frontiers 18-page full PDF | ICA acquisition, preprocessing, sign, and peak-quality guardrails; no graphite phase assignment. |
| Yao et al. | https://doi.org/10.1039/C8EE02373E | Official RSC full HTML; Argonne manuscript also available | Empirical transport-gradient confounder for Chapter 1 broadening/lag; no width/kernel calibration. |
| Kim et al. | https://doi.org/10.1039/C9EE02964H | Official RSC full HTML | LCO ordering/entropy evidence before reduction; no universal `Omega` or entropy parameters. |
| Hudak et al. | https://doi.org/10.1149/2.0071503jes | Full Sandia/OSTI author manuscript | Localized entropy-feature aging and parameter-stationarity boundary; no universal aging coefficient. |
| Otero et al. | https://doi.org/10.1038/s41598-018-33405-y | Publisher full HTML | Total-active-mass/capacity-basis equation before blend conversion and in API docs. |
| Moon et al. | https://doi.org/10.1038/s41467-021-22662-7 | Publisher full HTML | Host cross-talk/mechanical nonadditivity boundary after equilibrium blend sum. |
| Sethuraman et al. | https://doi.org/10.1149/1.3489378 | Full author manuscript | Biaxial geometry, plane-stress conversion, theory/measurement separation, finite-strain warning. |
| Zhang | https://doi.org/10.1038/s41524-017-0009-z | Publisher full HTML | Finite-strain/plastic constitutive layer omitted by GS-1. |
| Berliner et al. | https://doi.org/10.1149/1945-7111/ac26b1 | Full MIT author PDF plus DOI identity | Battery-specific nonlinear identifiability and orthogonal-data discipline; no P2D numerical transfer. |

Identity-only or limited-access searches were also performed for LIT-027, LIT-030, LIT-049, LIT-055, LIT-061, and LIT-067. They remain retrieval/data candidates. LIT-001, LIT-003, LIT-005, LIT-011, and LIT-028 were rejected for claim-level transfer under their abstract/metadata/TOC access. LIT-064 was rejected as a system-topology mismatch. Exact DOI URLs and access consequences are in rows `P10-A011` through `P10-A022`.

## Mechanical Counts

The CSV contains 108 data rows and 109 physical lines including its header.

### By Domain

| Domain | Count |
|---|---:|
| CITATION_PLACEMENT | 1 |
| CODE_FIDELITY | 15 |
| GENRE | 4 |
| LITERATURE_ADDITIONAL | 22 |
| LITERATURE_EXISTING | 38 |
| SCIENTIFIC_MODEL_ROOT | 1 |
| STRUCTURE | 18 |
| VERSION_HISTORY | 9 |

### By Chapter Or Version

| Chapter/version | Count | Chapter/version | Count |
|---|---:|---|---:|
| Ch1 | 24 | Ch1 Appendix E | 1 |
| Ch1 Appendix E/v1.0.23 | 1 | Ch1-Ch3/v1.0.23 | 2 |
| Ch1/Ch2 | 1 | Ch1/Ch2/Ch3 | 2 |
| Ch1/Part T | 5 | Ch1/v1.0.23 | 3 |
| Ch2 | 16 | Ch2/Ch3 | 1 |
| Ch2/v1.0.23 | 2 | Ch3 | 28 |
| Ch3/v1.0.23 | 4 | Part T | 2 |
| Part T/v1.0.23 | 1 | v1.0.10-v1.0.11 | 1 |
| v1.0.19-v1.0.20 | 1 | v1.0.20-v1.0.23 | 1 |
| v1.0.21 | 1 | v1.0.22 | 1 |
| v1.0.22-v1.0.23 | 1 | v1.0.23 | 3 |
| v1.0.23 guides | 2 | Volume | 4 |

### By Severity, Evidence Status, And Disposition

| Severity | Count | Evidence status | Count | Disposition | Count |
|---|---:|---|---:|---|---:|
| Critical | 17 | 확정 | 90 | AFFIRM | 66 |
| High | 64 | 미결 | 4 | MODIFY | 26 |
| Medium | 20 | 근거 미발견 | 1 | REJECT | 8 |
| Low | 3 | 미검증 | 13 | UNRESOLVED | 8 |
| Info | 4 | 추정 | 0 | - | 0 |

## Version History And Attribution

| Record | Disposition | Final judgment |
|---|---|---|
| Release control 1 | MODIFY | v1.0.22-v1.0.23 Chapter 2/3 included section bodies are byte-identical and normalized science is equivalent; whole roots/PDFs are not byte-identical. |
| Release control 2 | AFFIRM | v1.0.23 reference ledger is stale and misses `lee2017jcp`, `lee2011jcp`, and `son2013jcp`. |
| Release control 3 | MODIFY | `appendix_phase_separation.pdf` is absent while TeX remains; packaging blocker, not a demonstrated science regression. |
| Release control 4 | AFFIRM | v1.0.11 is a scientific no-op relative to v1.0.10 but not a literal package clone because eight process/package assets disappeared. |
| Release control 5 | AFFIRM | v1.0.23 handover QA state, fitting guide, and Chapter 3 future-tense implementation prose are stale. |
| v1.0.20 role | AFFIRM | Bounded quality/documentation edition; Python AST is unchanged from v1.0.19. |
| v1.0.21 Fable role | MODIFY | Fable was solo integrator for Q2-Q7 and authored a preliminary Chapter 3 appendix; Q9/Q10 were superseded by v1.0.22. |
| v1.0.22 Fable/Opus role | MODIFY | Opus produced the primary W-stream drafts; Fable selected and integrated them. Exact final-stream overlaps are reported above. |
| Model identity | AFFIRM | Provenance only. It supplies no authority or scientific-quality presumption. |

## Existing-Reference Defects And Consequences

All 38 material Phase 004 records were challenged. Their exact row-level evidence and actions are `P10-E001` through `P10-E038`.

| Record | Defect that survived refutation | Exact consequence |
|---|---|---|
| REF-001 | Dahn page/figure not retrieved for staging and 0.085/0.210 V anchors. | Anchors remain unverified/sample-dependent; initialization and validation targets may be wrong. |
| REF-002 | Ohzuku access does not carry all stage/0.120/0.125 V claims. | Retrieve exact figure or downgrade values and full-map language. |
| REF-012/013 | Dreyer sources support conceptual metastability, not the exact chapter gap equation. | Identify the formula as a local construction or add an exact derivation source. |
| REF-014 | Bloom is DVA (`dV/dQ`), not a primary ICA (`dQ/dV`) source. | Observable, interpretation, and units must be separated. |
| REF-020 | K-graphite paper is used for Li-graphite. | Replace the load-bearing claim with direct Li evidence. |
| REF-021 | Fly primary text was not retrieved. | Exact `L_V`, exponential kernel, and zero-current claims remain model hypotheses. |
| REF-025/026 | Persson does not support, and the second record contradicts, the decreasing 48-to-40 kJ/mol trend. | Remove source-derived trend claim; re-derive or label values unsupported priors. |
| REF-035 | Two MSMR records share one key. | Split `ad1d27` framework from `ad7d1c` MCMB Part 1. |
| REF-036 | `+3` to `+4 mV/K` should be about `+0.3 mV/K`. | Factor-of-ten error directly scales temperature shifts and reversible heat. |
| REF-037 | Protocol paper does not establish stage-specific entropy magnitude or `+60.8 mV`. | Keep protocol role and add graphite primary numerical evidence. |
| REF-038 | Temperature-path paper does not establish graphite branch averaging. | Branch-average reversible entropy remains a disclosed approximation, not sourced equilibrium entropy. |
| REF-039 | Internal `numverif2026` is in external bibliography. | Move to hashed reproducibility evidence; it cannot supply scientific authority. |
| REF-041 | Lee identity/mapping is unresolved. | Correct DOI and call the local method Picard/lagged-coefficient iteration until mapping is demonstrated. |
| REF-043 | Reimers diffraction anchors phases, not a unique single-`Omega` model. | Treat equations as phenomenological reduction requiring calibration. |
| REF-044 | Multi-ECI ordering is equated to one `Omega`; high-x MIT transfer is unsupported. | Remove equivalence; this exposes the new wrong-model-class root. |
| REF-050 | Motohashi estimate is susceptibility-derived O1 `x=0`, not direct per-atom O3 `x=0.85` DOS. | Current defaults create an unsupported `-45.68 J mol^-1 K^-1` well. |
| REF-052 | State electronic entropy is used as total partial-molar entropy and logistic proof. | Quantity/derivative scale and gate shape must be rebuilt. |
| REF-054 | MSMR source does not derive the chapter's direction sign/hysteresis slot. | Keep equilibrium width; label sign/branch as local convention/extension. |
| REF-057 | Configurational model cannot exclude the omitted electronic term. | Keep the MIT electronic channel open in decomposition/inverse analysis. |
| REF-059 | Limthongkul numerical/loss claims are not fully retrieved and mix capacity bases. | Retrieve tables and require a commensurate reversible basis. |
| REF-060 | Li-Dahn is structural evolution, not sharp moving-boundary imaging. | Add spatially resolved evidence before imposing a sharp boundary. |
| REF-063 | About 310% expansion does not validate constant partial molar volume. | Require finite-strain, composition-dependent, geometry-consistent mechanics. |
| REF-064 | Constrained biaxial film result is generalized to universal/dominant mechanics. | Preserve geometry; mechanical dissipation is comparable to polarization under that protocol. |
| REF-068 | Single Li-Si precedent is called proof of two-host common-`mu` additivity. | Derive/validate the blend extension independently; exact source mapping remains unresolved. |
| REF-070 | Original Larché-Cahn derivation was not retrieved and small-strain transfer is unstated. | No direct verification of the high-strain hydrostatic coefficient. |
| REF-072/073 | First-lithiation evidence is extended to subsequent-cycle switching. | Split cycle-history claims and source later-cycle behavior directly. |
| REF-075 | Miyachi XPS assignments/priority were not retrieved. | Phase, irreversibility, and buffer-role claims remain unresolved. |
| REF-078 | Total first-cycle inefficiency is allocated to phases without Li balance. | Report total efficiency only unless phase-resolved balance is supplied. |
| REF-079 | Andersen `3117 mAh/g-Si` first-charge basis is conflated with long-cycle operation. | Do not use it as a generic reversible blend default. |
| REF-080 | Component voltage-axis comparison is called common-`mu` validation. | Relabel as comparison; independently validate inversion/additivity. |
| REF-083 | Calorimetry is called mechanics corroboration. | Retain only protocol-specific thermal observation. |
| REF-085 | Full-cell entropy interpretation is called component-separated measurement. | Label host attribution and Si-aging conclusions as interpreted/hypothesized. |
| REF-086 | Internal G2 and one formulation are used as continuity/basis proof. | G2 is numerical only; implement or relabel the absolute mass basis. |
| REF-088 | One 30 wt% datum is used for continuous interpolation. | Use only as a discrete comparison. |
| REF-089 | Cited total-active-mass equation contradicts fixed-graphite absolute-Q implementation. | At 10/20/30 wt%, absolute-Q inflation is 1.111/1.25/1.429. |

## Additional Literature Disposition

### Adopt Now

| Source | Exact placement | Integration role |
|---|---|---|
| Raue | Chapter 1 after kinetics/synthesis and before validity/UQ; Chapter 2/3 local inverse sections | Profile likelihood, structural/practical identifiability, confidence intervals. |
| Dubarry-Anseán | Chapter 1 immediately after `eq:eqpeak` and before broadening; Part T method/acquisition table | ICA acquisition, preprocessing, sign, noise, and peak guardrails. |
| Yao | Chapter 1 Sec. 1.07 broadening sources and Sec. 1.08 lag validity | 1C porous-electrode concentration-gradient confounder, not fit-parameter calibration. |
| Kim | Chapter 2 pre-model evidence/status subsection and configurational validation boundary | Direct ordering/entropy evidence with material/protocol limits. |
| Hudak | Chapter 2 decomposition/peak-validity and validation requirements | Localized cycling change and stationarity uncertainty. |
| Otero | Chapter 3 Sec. 3.3 before wt conversion; Sec. 3.5 API basis | Fixed-total-active-mass capacity equation and explicit basis distinction. |
| Moon | Immediately after equilibrium common-`mu` sum/GS-2; mechanics coupling | Finite-rate/cycled host cross-talk and mechanical nonadditivity boundary. |
| Sethuraman | Chapter 3 mechanics before scalar coupling | Biaxial geometry, plane-stress conversion, theory/measurement separation, finite-strain warning. |
| Zhang | Chapter 3 mechanics validity envelope and GS-1 | Constitutive finite-strain/plastic layer that is not implemented. |
| Berliner | Chapter 2/3 inverse/UQ after the common Raue method | Battery-specific nonlinear identifiability and orthogonal data; no numerical P2D transfer. |

### Retrieval Or Data Required

- `LIT-027` van de Walle/Ceder: retrieve full text before using it to delimit cluster-interaction-to-single-`Omega` reduction.
- `LIT-030` Baek et al.: retrieve full text before importing entropic-potential definitions or validity equations.
- `LIT-049` Dresselhaus/Dresselhaus: retrieve exact staging pages before detailed Chapter 1 taxonomy use.
- `LIT-055` Rao/Newman: retrieve equation-level text before replacing internal heat-balance authority.
- `LIT-061` Lian/Bazant: retrieve full body only if fast-charge/plating scope is added.
- `LIT-067` Park et al.: full-source recheck required before retaining broad width-origin claims.

### Rejected Transfers

- `LIT-064`: parallel-cell DVA does not directly support this single-cell method.
- `LIT-001`, `LIT-003`, `LIT-005`, `LIT-011`, and `LIT-028`: abstract/metadata/TOC access cannot support equations, coefficients, or claim-level adoption. They may be revisited only for a named need after retrieval. Fully accessed Raue/Berliner already cover the immediate inverse-method gap, so Stuart is not needed as citation padding.

## Structure And Genre Adjudication

### All 18 Reorganization Proposals

| Proposal | Disposition | Required bounded action |
|---|---|---|
| P8-REORG-001 | MODIFY | Keep Part 0 in Chapter 1; add a fast route/dependency map and move only optional excursions. |
| P8-REORG-002 | AFFIRM | Put the hysteresis mechanism/status hierarchy before branch interpretation. |
| P8-REORG-003 | MODIFY | One canonical width/status table plus a minimal self-contained Part T recap. |
| P8-REORG-004 | MODIFY | Add early observable orientation; retain the existing prerequisite derivation order. |
| P8-REORG-005 | AFFIRM | Add common inverse/identifiability closure after kinetics/synthesis. |
| P8-REORG-006 | MODIFY | Add validity/UQ/reproducibility dividers; keep Appendix E optional and unverified. |
| P8-REORG-007 | REJECT | Do not delete non-rendered provenance comments. |
| P8-REORG-008 | AFFIRM | Label Chapter 2 a dependent volume chapter and add a compact recap. |
| P8-REORG-009 | MODIFY | Put LCO evidence/status before reduction and correct the order-parameter/model-class defect. |
| P8-REORG-010 | AFFIRM | Put component/status/MSMR non-identity guards before the electronic gate. |
| P8-REORG-011 | AFFIRM | Add Chapter 2-local inverse, validity/UQ, and reproducibility closure. |
| P8-REORG-012 | MODIFY | Move LCO-only workflow rows; retain one canonical shared code map. |
| P8-REORG-013 | MODIFY | Add a concise orientation, then keep the survival map first. |
| P8-REORG-014 | AFFIRM | Add an observed-versus-latent host table before blend addition. |
| P8-REORG-015 | AFFIRM | Put the mechanics validity envelope before the first coupling equation. |
| P8-REORG-016 | MODIFY | Move API details to a same-master appendix; retain scientific gates/exclusions in main text. |
| P8-REORG-017 | AFFIRM | Add Chapter 3 inverse/UQ/validation and bounded fitting closure. |
| P8-REORG-018 | MODIFY | Use common checkpoints with chapter-specific dependency order, not one rigid sequence. |

### Chapter And Volume Verdicts

- Chapter 1: retain Part 0. It is the strongest textbook foundation and supplies downstream premises. The chapter is not textbook-ready until reference defects, inverse/identifiability, validity/UQ, and reproducibility close.
- Chapter 2: appropriate only as a linked/dependent volume chapter. It must say so, add a local recap and local closure, and stop claiming literal order-disorder physics from the current positive-`Omega` reduction.
- Chapter 3: keep orientation then survival map, cases, blend, mechanics boundary, inverse/UQ/validation, and same-master API appendix. Its honest genre is a research roadmap.
- Volume: the architecture can support a mixed textbook/review-volume contract, but the current state is `CONDITIONAL/NOT-YET`, not an unqualified pass.
- Citation placement: place each primary citation and access/status guard adjacent to the exact equation, coefficient, stage assignment, or transfer claim. Abstract/metadata-only access cannot support equations or numerical adoption.

## Document-To-Code Fidelity

### Category Separation

| Category | Records | Verdict and consequence |
|---|---|---|
| Transcription/API mismatch | P9-F001; P9-F004 | `c_rate` hour/second path is 3600x wrong when lag resolves; FFT helper silently implements circular boundary behavior. |
| Shared invalid/incomplete science | P9-F002; P9-F006; P9-F007 | Document and code agree on an incomplete local-affinity correction, unsupported LCO defaults, and fixed-graphite wt% semantics. Agreement does not make them valid. |
| Document science defect with bounded code input | P9-F008 | Stress geometry/coefficient is invalidly transferred; code only consumes a caller-precomputed scalar offset and therefore does not implement mechanics. |
| Disclosed approximation | P9-F005; equilibrium logistic reductions | Frozen LCO electronic temperature path is correctly disclosed but cannot support dynamic multi-temperature claims. |
| Explicit nonimplementation | P9-F009; P9-F010; P9-F017 | Plastic mechanics, finite-rate host nonadditivity, and PSD inversion are absent or explicitly raise/stop. They are not hidden transcription mismatches. |
| Exact reduced mapping | equation-label parse; P9-F019 | 190/190 labels are covered and both `eq:qrev` terms map exactly under reduced assumptions. Coverage is navigation/internal fidelity only. |
| Operator/validation debt | P9-F013; P9-F014; P9-F015; CODE_GUIDE contract | Official tests miss adversarial invariances; synthetic inverse is same-model only; fitting guide is stale; exact-implementation language needs categories. |

### Five High Phase 009 Findings

1. Hour/second API (`P10-K001`): affirmed as a true document/code unit mismatch; measured factor `3599.999999999991`.
2. Incomplete affinity (`P10-K002`): affirmed as a shared scientific defect. At `A_cut=4RT`, the reverse denominator factor is `1.018315638889`; at local `A=0`, the correct denominator is `2`, giving an optional-L ratio `0.509157819444` before the interaction factor.
3. LCO provenance defaults (`P10-K003`): affirmed; `g_max=13`, `x_center=0.85`, `dx=0.05` produce about `-45.68 J mol^-1 K^-1` without source support.
4. Blend basis (`P10-K004`): affirmed as document/code-consistent but semantically wrong for fixed-total-mass wt%; inflation factors `1.111111`, `1.25`, `1.428571` at 10/20/30 wt%.
5. Stress (`P10-K005`): affirmed as a document science/geometry defect; runtime accepts a precomputed offset and contains no constitutive mechanics.

Additional operator conclusions:

- `FITTING_GUIDE.md` is stale and incorrectly describes the unresolved-tail threshold/fallback relative to current lines 612-653.
- Recursive parsing of the three final masters found 53 includes and 190 labels; traceability has zero missing and zero extra labels.
- `CODE_GUIDE_v23.md` must classify mappings as `EXACT`, `APPROXIMATION`, `SHARED_DEFECT`, or `NOT_IMPLEMENTED`; its blanket exactness language is false, and `irreversible_heat` must be added under `eq:qrev`.
- The unpadded FFT helper requires a circular/periodic contract or linear-convolution padding and edge tests.
- Official tests and same-model synthetic recovery establish internal consistency only, not physical validity, model completeness, uniqueness, or parameter identifiability.

## New Root Cause

`P10-R001` is the only genuinely new root introduced by this critic. In `_sections/ch1_sec13_lcohys.tex:9-25`, the same one-coordinate symmetric regular-solution free energy is declared literally applicable to LCO T2/T3 order-disorder. Its positive interaction term creates a concave central region and two composition wells; it is a demixing model. An ordered half-filled phase requires at least a separate order parameter/sublattice occupancy or a cluster-interaction description. Therefore the canonical issue is deeper than missing `Omega` calibration or an ECI-to-`Omega` citation: the literal microscopic interpretation is invalid. The bounded alternatives are:

1. Add a true ordering model with its own state variable(s), phase evidence, and code mapping.
2. Retain the current equations only as phenomenological two-state/two-phase peak/gap fits, deleting claims of literal Li/vacancy order-parameter authorship.

## Explicit Unresolved And Limited-Access Items

- Existing-reference unresolved/limited records: REF-001, REF-002, REF-021, REF-041, REF-059, REF-068, REF-070, and REF-075. Their status is not upgraded by DOI identity.
- Additional-literature retrieval candidates: LIT-027, LIT-030, LIT-049, LIT-055, LIT-061, and LIT-067.
- Metadata/abstract/TOC-only rejected transfers: LIT-001, LIT-003, LIT-005, LIT-011, and LIT-028. LIT-064 is rejected for topology mismatch.
- No primary source was found in this scope that validates the complete-affinity optional correction, a universal O3 LCO logistic electronic gate, fixed-graphite addition as a fixed-total-mass wt% sweep, or direct biaxial-to-particle/hydrostatic stress transfer.
- The branch-averaged reversible-entropy formula is disclosed but not established by the cited temperature-path source as equilibrium entropy.

## Mechanical Validation

Final validation was rerun after summary construction and canonical self-hash insertion; the results below are from that fresh full pass.

- Exact CSV header: PASS for both raw first line and parsed property order.
- CSV parse: PASS, 108 data rows, 109 physical lines.
- Unique `critic_id`: PASS, 108 unique IDs, zero duplicates.
- Allowed enums: PASS, zero invalid severity, evidence-status, or disposition values.
- Nonblank cells: PASS, zero blank cells across 15 columns.
- Local citations: PASS, 133 parsed `file:line` references; all files exist and all cited lines/ranges are within file bounds.
- Literature URLs: PASS, 60 literature rows checked; 60 syntactically valid URL occurrences, with REF-039 intentionally documented as having no DOI/official publication.
- Coverage counts: PASS - five lineage release-control rows, 38 material existing-reference rows, 18 reorganization rows, all five High Phase 009 findings, ten endorsed sources, six retrieval candidates, six rejected transfers, and one new root.
- CSV full-file SHA-256: `57b3c65694b532258d2a6a8aa9a8879729dc07a3b9571d582988c30d6a7cf3d3`.
- Summary canonical self-hash scheme: UTF-8 file bytes after replacing the 64 hexadecimal characters on the next line with 64 ASCII zeroes.
- Summary canonical SHA-256: `89faa4603c97097d540cc4ce3fa6988bfdd6e58fe38db3cfb29bdd79205a040a`.

No Git command was run. No snapshot, source/code, Claude file, existing Codex result/plan, configuration, or repository metadata was changed. The only writes are the two required files in `Codex/work/agent_reports/phase010`.
