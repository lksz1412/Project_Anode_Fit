# Phase 012 Recent Source Coverage Result

Date: 2026-07-20

## Scope

- Publication window: 2021-01-01 through 2026-07-20.
- Full scope: Chapter 1 graphite, Chapter 2 LCO, Chapter 3 Si/SiOx/Si-C/Si-graphite, and common inverse-method literature.
- Priority: LCO received the deepest search and direct-source review, but it was not the only material track.
- Protection boundary: no source snapshot, Claude file, TeX, Python, test, example, or Git state was modified.

## Inputs Actually Read

- Phase 011 gap matrix and result: read in full.
- Chapter 1 worker report and all 18 candidate records: read in full.
- LCO worker report, all 696 lines, and all 16 candidate records: read in full.
- Chapter 3 worker report and all 14 candidate records: read in full.
- Common-method report and all 20 original candidate records: read in full.
- The current Codex independently read the full main text of the Shojaei author preprint and the complete local Mattila-Karttunen and Chen LCO texts used during adjudication. The LCO worker additionally recorded complete reads of six direct LCO sources.

Worker full-read claims were not silently generalized. Chapter 3 and common-method papers were inspected at targeted article locations, not cover to cover. Their proposed transfers remain provisional until complete reads are performed.

## Output

- Canonical candidate matrix:
  `D:\Projects\Project_Anode_Fit\Codex\results\phase012_recent_theory_candidate_matrix.csv`
- Raw worker evidence:
  `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase012`

The integrated matrix contains 69 unique bibliographic identities. The two
additional records were found during the parent-level final completeness pass
after the first worker merge:

- Wan et al. (2026), direct Si/graphite material-health and effective-OCP
  diagnostic evidence;
- Natterer et al. (2026), SoC/temperature/aging-conditioned EIS inferential
  evidence.

| Track | Unique records |
|---|---:|
| Chapter 1 | 18 |
| LCO | 16 |
| Chapter 3 | 15 |
| Common methods | 20 |
| Total | 69 |

The original worker files contained 68 rows. Dubarry and Ansean (2022), DOI
`10.3389/fenrg.2022.1023555`, appeared in both the Chapter 1 and common-method
sets. It was deduplicated to the direct Chapter 1 identity.

## Evidence Rule

The matrix preserves both `worker_disposition` and `parent_disposition`.
Twenty-eight proposed transfers based on targeted, abstract, preview, or
otherwise incomplete reads were set to
`RETRIEVE_OR_FULL_READ_BEFORE_IMPLEMENTATION`. They may guide model direction
and retrieval priority, but they are not final equation or numerical-parameter
adoptions.

Ten source records have parent dispositions beginning with `ADOPT` on the
basis of an explicit complete read. Preprint-based adoptions retain their
preprint status and may not be cited as peer-reviewed final equations.

## Confirmed Search Results

### Chapter 1

- Recent graphite theory requires a hierarchy spanning multilayer staging
  thermodynamics, transformation dynamics, electrode transport, and the
  measurement/preprocessing operator.
- No recent battery-specific proof was found that makes an overlapping ICA
  finite-mixture decomposition structurally unique.
- No recent source makes a fitted ICA width a unique particle-size,
  diffusivity, or microstructure parameter.
- The MCMB entropy-coefficient scale near 0.28-0.30 mV K^-1 is a targeted-read
  material prior, not yet a target-graphite universal value.

### Chapter 2 LCO

- No direct recent source was found that derives the current logistic
  `g(E_F,x)` gate or `Delta x=0.05`.
- Direct finite-temperature ordering theory requires composition plus
  independent order parameters. A positive-`Omega`, x-only regular solution
  cannot distinguish ordered and disordered states at fixed composition.
- Direct recent electronic-structure work supports correlation-, magnetic-,
  structure-, and local-environment-dependent behavior, not a transferred
  scalar endpoint DOS.
- No recent direct LCO model found here simultaneously reproduces x=0.5
  ordering, the high-x metal-insulator-transition plateau, structural changes,
  branch hysteresis, and measured entropic potential.

### Chapter 3

- Recent theory strengthens the audited mass/capacity-basis correction and
  makes finite-rate host-current partition a separate dynamic closure.
- Shared electrode potential is not proof of `G_int=0`.
- General Si mechanics requires finite deformation and path/phase state; a
  thin-film stress coefficient is geometry specific.
- No reviewed recent paper supplies a calibrated nonseparable Si/graphite
  interaction free energy or an integrated SiOx/Si-C conversion-contact-SEI
  model.
- Wan et al. (2026) directly shows that the diagnosed Si-dominant state window
  and an effective Si OCP deformation evolve with degradation pathway. This is
  a strong observable/model-boundary result, not proof of a unique microscopic
  Si free energy.

### Common Methods

- ICA/DVA preprocessing belongs inside the observation model.
- Nonlinear profiles/posteriors and model discrepancy are needed beyond a local
  Jacobian check.
- Orthogonal observables and protocols are more informative than additional
  voltage data on the same manifold.
- Natterer et al. (2026) shows that EIS aging effects interact with SoC and
  temperature, so those variables cannot be treated as separable nuisance
  corrections in a degradation estimator.
- These method conclusions remain provisional for implementation because none
  of the common-method candidate papers was read cover to cover in this phase.

## Unresolved Retrievals

- LCO: Robinson 2022 full phase-field article, Liu-Fang 2023, Zhang 2025 main
  text, and exact Hu 2021 methods/locators.
- Chapter 1: Rykner-Chandesris 2022, Cordoba et al. 2026 version of record,
  Abucide-Armas 2026 supplement, and several microstructure/transport papers.
- Chapter 3: Rehm 2026, Li et al. 2022, and Wan et al. 2026 full articles and
  supplements, plus complete reads of the other targeted model papers before
  implementation.
- Common methods: complete reads before adopting likelihood, identifiability,
  discrepancy, or optimal-design equations, including the complete Natterer
  2026 inferential-statistics workflow before reusing it.

## Validation

- Structured CSV parsing: passed.
- Stable nonblank source IDs: 69/69.
- Duplicate source IDs: zero.
- Duplicate DOI/official URL identities after normalization: zero.
- All four tracks present: passed.
- Every Phase 011 gap has a candidate, controlling older source, explicit
  negative search result, or scope-boundary disposition: passed.
- Source/Claude/Git modifications: none.

## Gate

`RECENT_SOURCE_COVERAGE_PASS`

This gate means search coverage and evidence status are complete enough for
transfer adjudication. It does not mean every candidate has passed complete
source reading or is ready for equation-level implementation.
