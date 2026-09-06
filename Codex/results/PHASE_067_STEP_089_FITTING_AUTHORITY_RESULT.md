# Phase 067 Step 89 Fitting Evidence Authority Result

## Result

Step 89 selects `PASS_P067_STEP89_FITTING_AUTHORITY` for the bounded audit task.
The pass means that the reviewed fitting objects are identity-pinned, exclusively
classified, and prevented from acquiring unsupported optimizer, held-out, external,
material, protocol, phase, mechanism, canonical-release, or publication authority.
It does not mean that a new fit converged, that the saved A/B/C profiles are externally
validated, or that the original historical optimizer state was recovered.

Persistence remains `PASS_PENDING_PERSISTENCE` until the exact-eight child of
`7b81814017ffd4207cc2a13fabbbe68281075b00` is committed with subject
`audit(phase067): separate fitting evidence authority`, pushed, and both Python 3.12
and Python 3.14 return `PASS_P067_STEP89_PERSISTENCE` for that same child.

## Recovery and Actual Starting State

The implementer and an independent recovery auditor read the Phase 067 detailed plan,
Step 88 result, both execution ledgers, and active handover from line 1 through EOF.
Those control documents still described Step 88 as precommit because Step 88 followed
the result-first rule and its first pushed candidate later failed persistence. Direct Git
inspection supplies the missing recovery fact: the repaired Step 88 commit is
`7b81814017ffd4207cc2a13fabbbe68281075b00`, its sole parent is
`ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4`, and its exact subject is
`audit(phase067): bound numerical guard impacts`. Local HEAD, upstream, tracking ref,
and live origin were equal; the tree was clean; Python 3.12 and 3.14 both returned
`PASS_P067_STEP88_PERSISTENCE`. This Step 89 record repairs the stale control pointers
without rewriting the Step 88 result.

The external main ref is pinned at `f0c381bd6dc315ac75cbffa93dd86ce83a37949b`.
The protected audit ref is pinned at `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
The active branch has zero `Claude/**` drift from that protected ref.

## Read and Verification Scope

The following recovery/control documents were read 1–EOF:

- `Codex/AGENTS.md`, 180 lines.
- `Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md`,
  766 lines.
- `Codex/results/PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md`, 263 lines.
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`, 274 lines.
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`, 283 lines.
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`, 498 lines.

The Phase 066 fit-provenance, reproduction, optimizer-state, empirical-authority and
carry-forward JSON objects, plus the Phase 065 skew/material authority origin, were
strict-parsed with duplicate-key and non-finite rejection and traversed completely.
The four supplemental Python files were read 1–EOF and AST parsed without import or
execution. The source statement and four saved JSON objects were read 1–EOF. The
`sigr.csv` header and all 16,735 rows were parsed as two finite numeric cells per row.

## Exact Supplemental Object Set

All ten paths exist as mode `100644` blobs at supplemental commit
`e3e1a634f34b711aa4803fd190fe9120f1755f13`; all ten are byte-identical to their
objects at baseline `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`. No sparse-checkout
path or directory name was used as identity evidence.

| Bounded object | Bytes | Git blob | Raw SHA-256 |
|---|---:|---|---|
| `Claude/results/comp_v24/sintef_data/sigr.csv` | 286,471 | `4b06fefa1bb81de842386c95fbba5bdd431602d4` | `e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6` |
| `Claude/results/comp_v24/sintef_data/SOURCES.md` | 1,581 | `876e4a675812557dcacbac416ed74ff3c2ad858d` | `4fa8bc00535d31fe90cd066af895285341c69938c2e259eaa7609950de2a6649` |
| `Claude/results/comp_v26_data/build_two_versions.py` | 10,662 | `d14f98564d1f4723bfcd32c921a3dc9c69149ac9` | `70c50cadfe4c8b170612e275fccfbf7714cef42d9889588cf8316629f9db16ab` |
| `Claude/results/comp_v26_data/test_skew_regsol_v2.py` | 14,621 | `c064a11241c07195a11ad12878fa7a3914c1f15b` | `90ee96c2717d4b12bc94647da58b715c3974c2336bf03907b77c693adebb0c0c` |
| `Claude/results/comp_v26_data/bdd_dqdv.py` | 7,539 | `c4fc6b997bad2a15617f1c7255708bf736b9e37a` | `d3441b15b276ac87c4925c77146a24cdb2e16f1184057f9a17d9d6952daebf2c` |
| `Claude/results/comp_v26_data/test_gallery_vs_regsol.py` | 12,145 | `2a826e4b27ddcde3584daaf1e6a8c557011c773a` | `3ee4e41b8e6881529e36f4fddeb9d0130605f55955f8ef268ee578f3dd54a574` |
| `Claude/results/comp_v26_data/out_versions/summary_versions.json` | 17,754 | `c0a475352abe2f2df145442d8ed722d132ab5d03` | `edcafd90b91b6515ca12dca3743678055bc021a52cff3a86a2355467afe8dedc` |
| `Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json` | 1,709 | `f40c5d3b4019378c02453189717c19a27cbfac88` | `32cddfd8d148407090e117c8e4fdc386c15ac36b8612254fba75c658ab5b0206` |
| `Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json` | 1,321 | `7292f367c4bb03819efec316f01db0df64427d5e` | `89befa143dca8d4051ba4627f224608ff3e6fb0500a06fbca2d77409c3d7788f` |
| `Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json` | 1,669 | `c327a56b22a0f2c2c2910b90283088fb7f2c8f13` | `c4ba2e46d515eddbbdc4c5d8f3310a9ab90fc8b777e0def0177a22ad127f125e` |

## Exclusive Provenance Classification

The twelve present evidence records have exactly one class each:

| Class | Count | Bounded interpretation |
|---|---:|---|
| `REAL_DATA` | 1 | repository-derived `sigr.csv`; not the original parquet and not specimen/protocol-cryptographically bound |
| `RECONSTRUCTED` | 6 | four static reconstruction recipes/helpers and two sealed Phase 066 replay records |
| `SYNTHETIC` | 0 | no positive synthetic fitting record in the exact reviewed inventory |
| `DEMO` | 0 | no positive demo fitting record in the exact reviewed inventory |
| `SAVED_ONLY` | 5 | source declaration, A/B/C rounded profiles, and rounded summary |

The zero `SYNTHETIC` and `DEMO` counts are reviewed-inventory absences, not project-wide
absence claims. In particular, the `test_` filename prefix does not convert a real-CSV
reconstruction route into demo evidence. Missing original optimizer evidence is recorded
as `GROUND_NOT_FOUND`; a nonexistent object is not assigned one of the five classes.

## Data, Preprocessing, and Weighting Contract

The real-data object has columns `V_vs_Li,Q_mAh`, units V versus Li/Li+ and mAh, and an
`absolute_mAh_not_mass_normalized` capacity basis. All 16,735 rows are finite and Q is
monotonic nondecreasing. The observed ranges are 0.0461118–1.0 V and 0–3.82018 mAh;
there are 2,819 decreasing-voltage adjacent pairs and 114 equal-voltage adjacent pairs.

`SOURCES.md` declares SINTEF/EU IntelLiGent Zenodo record 20086298, CC-BY-4.0,
graphite+Si blend half-cell, pOCV, C/50 and approximately 25 °C. Those are source
declarations. The exact original parquet key/checksum, specimen UUID/composition binding,
and extraction-script-to-parquet cryptographic binding remain `GROUND_NOT_FOUND`.

The Phase 066 Direct14 path fixes finite filtering, stable Q sort, first-V retention for
unique Q, increasing isotonic V(Q), right-continuous cumulative Q on a uniform V grid,
forward difference, positive finite bins, longest contiguous interval, and absolute
direct/reciprocal Savitzky–Golay ensemble. The window is 0.06–0.70 V at 0.5 mV, retaining
1,280 points. Weighting is one unit per retained grid point and the objective is
`model(V)-D`.

The `test_skew_regsol_v2.py` docstring says BDD/dMSMCD, wavelet, and Savitzky–Golay are
combined, but its executed Direct14 preprocessing route calls the Savitzky–Golay ensemble
without BDD/dMSMCD or wavelet. Phase 066 independently seals
`wavelet_or_bdd_dmsmcd_used=false`; executable call flow and the sealed record control
over the descriptive sentence.

## Optimizer Contract and Historical Boundary

Direct14 uses skew-logistic components with flat order
`U[14],w[14],Q[14],alpha[14],bg`, 57 implicitly free box-bounded parameters, RNG seed 23,
three seed strategies, four restarts per strategy, and unweighted residuals. The solver is
`scipy.optimize.least_squares`; only `bounds` and `max_nfev=6000` are source-explicit.
Historical resolved method, loss, Jacobian scheme, tolerances, Python/NumPy/SciPy versions,
full-precision parameter/prediction, diagnostics and process streams remain
`GROUND_NOT_FOUND`.

The A/B/C comparison reconstruction source fixes:

- A blend: regsol, N=8, order `U,Omega,Q,w,bg`, 33 parameters.
- B blend: logistic, N=14, order `U,w,Q,bg`, 43 parameters.
- C blend: skew-logistic, N=14, order `U,w,Q,alpha,bg`, 57 parameters.
- Shared recipe: RNG seed 23, three seed strategies, four restarts, width 0.004 initial,
  Q=area/N initial, 0.75–1.25 restart perturbation, `least_squares`, unweighted
  residual and `max_nfev=6000`. The three seed sets and per-kernel bounds/initial
  vectors are supplied by `test_gallery_vs_regsol.seed_sets` and
  `test_gallery_vs_regsol.bounds_and_seed`, respectively.

The source chooses minimum cost even when the returned result is nonconverged. The
historical A/B/C initial vectors, trial records, convergence status, resolved method/loss/
tolerances, environment and full-precision optimizer state were not retained. A/B/C saved
metrics and U-sorted transitions agree with the saved summary, but the flat summary vectors
are rounded to eight decimal places and transition files are sorted/rounded views, not
original optimizer-state evidence.

The two other static fitting routes have separate contracts and are not silently assigned
the A/B/C settings. `test_skew_regsol_v2.py` uses RNG seed 7, four restarts, perturbation
multiplier 0.7–1.3 and `max_nfev=4000`; its configured transition positions receive clipped
U-bands. Its exact graphite, silicon, and blend CSV names, fit/zoom windows, grid steps,
transition lists, U-bands, and common 0.0001–0.10 V width bounds are sealed in the matrix.
`test_gallery_vs_regsol.py` uses the exact graphite `gr.csv`, 0.060–0.300 V, 0.25 mV
route, RNG seed 11, three seed strategies, three restarts
per strategy, perturbation multiplier 0.75–1.25 and `max_nfev=4000`; its U values are free
over the data window and it sweeps kernel-specific transition counts. Both use unweighted
`model(V)-D`, box bounds and `scipy.optimize.least_squares`; resolved method, loss, Jacobian
scheme and tolerances remain `GROUND_NOT_FOUND`. Neither route was executed in Step 89.

## Reused Runtime Evidence

Step 89 executed zero historical fits and made zero optimizer calls. It statically parsed
the four supplemental Python objects without import, `runpy`, `exec`, pytest collection,
or module-body execution. Importing those modules was prohibited because module bodies can
create directories and truncate logs.

The only optimizer runtime evidence is reused from the sealed Phase 066 replay. Python
3.12 and 3.14 select trial 11 with identical replay vector hash, cost
`11.287055224907945`, `success=false`, `status=0`, `nfev=6000`, `njev=5656`, and
optimality `0.11459771897658692`. Stored-to-replay ordered parameters are
`NOT_EQUIVALENT` with maximum absolute difference `1.2482043497025828`; the curve/
objective agreement is only tolerance-equivalent. All 25 original historical optimizer
state fields remain `GROUND_NOT_FOUND`.

## Evaluation and Authority Separation

All retained R², BIC, peak/valley RMSE, area and cost observations are training/in-sample
or saved in-sample reports. No held-out cell, rate, temperature or external dataset was
tested. A whole-blend curve fit cannot identify graphite/Si fractions, phase/gallery
species, a transferable mechanism, host independence, finite-rate current partition, or
nonadditive blend behavior. Every evidence row therefore keeps held-out, external,
specimen/protocol-binding, material, phase/mechanism, identifiability, original optimizer,
canonical-release and publication authority false.

## Owner Bindings

`P065-OBL-0054/P065-S72-F04` is explicitly bounded: blend additivity lacks one
consistently declared denominator and finite-rate current-partition evidence.
`P066-OBL-0120/P066-P79-07` is explicitly bounded: an in-sample whole-curve fit does not
test \(I=I_\mathrm{graphite}+I_\mathrm{Si}\), host independence, current partition or
nonadditive finite-rate behavior. Both remain owned by `P067-CODE-HISTORY` in the inherited
record and receive Step 89 disposition `EXPLICITLY_BOUNDED_NOT_RESOLVED`; Step 90.1 must
perform their lossless final disposition. No external authority is promoted.

## TDD, Validation, and Scope

The Step 89 validator was written first and returned the intended RED terminal
`E_MATRIX_MISSING`. The builder preview then completed on Python 3.12 and Python 3.14
without writing artifacts. This human result is saved before the two canonical JSON
objects. Final collection must rebuild both JSON objects deterministically, pass strict
duplicate/non-finite/depth/node limits, named semantic mutations, source policy, exact
object identities, exact-eight content/staged checks, and independent review before commit.

Only the Step 89 builder, validator, two JSON artifacts, this result, both ledgers and the
active handover may change. `Claude/**`, production Python, LaTeX, bibliography, figures,
PDFs and data are untouched. No defect repair, refactor, new API/model/default, parameter
reselection, historical-output overwrite, synthetic substitution, manuscript change,
stale-PDF rebuild, or Phase 068 work is authorized.

## Gate and Next Condition

Content gate: `PASS_P067_STEP89_FITTING_AUTHORITY`.

Persistence gate: `PASS_P067_STEP89_PERSISTENCE` after exact-eight commit, push,
live-remote equality, clean tree, protected/main pins, zero `Claude/**` drift and dual
Python verification. Only then may Step 90.1 begin.
