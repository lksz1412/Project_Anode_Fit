# Phase 067 Step 087 Unit and Numerical Result

Date: 2026-09-02
Phase: 067
Step: 87
Status: `PASS_PENDING_PERSISTENCE`
Content Gate: `PASS_P067_STEP87_UNIT_NUMERICAL`
Expected parent: `4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7`
Expected subject: `audit(phase067): verify units numerical invariants`
Postcommit terminal: `PASS_P067_STEP87_PERSISTENCE`

## Result

Step 87 freezes a source-grounded, internally recomputed unit and numerical matrix for all `20`
production-code occurrences and `15` unique production blobs. The matrix has `16` ordered checks.
Each source blob is parsed from its frozen Git object and retains lossless release/path/blob/ordinal
occurrence references. Each check retains dimension exponents, basis, sign convention, formula,
typed inputs, expected and independently computed observed values, error, declared tolerance,
disposition, source features and an authority ceiling.

This is an internal software/numerical consistency result. It is not external scientific,
material, experimental, canonical-equation, or publication authority. In particular, `I_abs`
being measured in amperes is source-static convention rather than source-explicit ground, and the
generic `Q_cell` basis remains ambiguous between Ah-style and C-style use. All `20` frozen code
occurrences contain `T_attempt=(I/Q_cell)h/kB` and `I_use=c_rate*Q_cell`, but none has executable
division by `3600`. Only the three unique v1.0.24+ code blobs contain comment-only `3600`
discussion. The matrix therefore records a source non-invariance/open convention; it does not call
the comments an implemented correction.

## Inputs and Read Coverage

- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`: recovery read in bounded
  chunks, with Phase 067 routing and Step 87 transition checked.
- `Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md`: lines 1–766
  were read in bounded chunks; Step 87 lines 461–488 and the global validation/Git boundaries were
  rechecked directly.
- `Codex/results/PHASE_067_STEP_082_SOURCE_TOPOLOGY_RESULT.md` through
  `Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md`: each result was read 1–EOF.
- Step 82 inventory/full-read attestation and Step 83–86 machine artifacts: strict JSON parse,
  duplicate/nonfinite rejection and recursive traversal were performed. Step 82 and Step 83 are
  the direct topology/state-flow inputs for this matrix.
- Frozen production source: exact `20` occurrence / `15` blob projection, `18,529` unique-blob
  physical lines and `24,891` occurrence-projected lines. Relevant source features were rebuilt
  from the complete frozen Git blobs; no working-tree production source was imported or executed.
- Both execution ledgers and active handover: the current Step 82–86 chain and Step 87 boundary
  were read and reconciled.

## Numerical Checks

The `16` rows cover:

1. exact h^-1 to s^-1 factor `3600`;
2. independently recomputed finite `func_L_q` algebra for distinct Ah-style and C-style
   hypotheses: raw-hour `2.1529435464149305e-7`, normalized-second
   `5.980398740041466e-11`, ratio `3600.0000000000045`, `R*T*ln(3600)`
   `20298.27900563456 J/mol`, and compensated-second `2.152943546414923e-7`;
3. discharge voltage-shift sign;
4. charge voltage-shift sign;
5. conditional zero-current dQ/dV closure for a source-declared no-direct-`L_V`, no-`dH_a`,
   no-hysteresis, `alpha=1` fixture; direct `L_V`, hysteresis and reversed-direction skew cases
   are explicitly excluded from any universal equality claim;
6. mAh → Ah → C with `1000` and `3600` each exactly once;
7. independent V·C → J energy identity while the production integration route remains
   `GROUND_NOT_FOUND`;
8. legacy-F entropy coefficient arithmetic;
9. SI-F entropy coefficient arithmetic;
10. reversible heat for positive entropy coefficient;
11. reversible heat for negative entropy coefficient;
12. mass fraction → capacity fraction without basis conflation;
13. Si/graphite component and total capacity closure;
14. conditional irreversible heat `I(U_oc-V)` without promoting universal nonnegativity;
15. source-directed increasing-logistic finite-window positive dQ/dV area
    `+0.9999999958776927` by composite Simpson quadrature with `400001` points,
    window factor `20`, and the frozen gate's relative tolerance `1e-6`;
16. centered `T±3 K` finite difference of an independent closed-form potential against its
    analytic derivative with the frozen entropy-gate tolerance `1e-3 µV/K` (`1e-9 V/K`).

The N15 and N16 tolerances are `TOLERANCE_PRECEDENT_ONLY`: `10` exact records over `6` frozen
test blobs bind every release/path/blob/ordinal/mode/raw/LF identity, constant and gate-function
source/AST anchor. The historical blend/trapezoid and production-centered-secant gates are not the
same methods as the independent single-logistic Simpson and closed-primitive checks. Exact and
approximate checks are separate. No NaN, infinity, complex transport, bool/int numeric
coercion, or unit-label/value coordinated reseal is accepted. The source feature set includes
`T_ATTEMPT`, `I_FROM_CRATE`, direction sigma, voltage shift, entropy/F, reversible heat,
irreversible heat, positive logistic derivative, direct-`L_V` precedence, zero-current lag selection,
and v1.0.22+ mass-to-capacity/component-capacity anchors. Each feature row carries an explicit
Git-object LF hash using `CRLF_AND_LONE_CR_TO_LF` normalization.

## TDD Evidence

Before the matrix existed, the validator's content route failed exactly with:

```text
E_FILE_MISSING:Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json
```

Builder bring-up then exposed and closed exact predecessor semantic, canonical release-order and
Step 83 universe-key mismatches (`E_INPUT_SEMANTIC`, `E_RELEASE_ORDER`,
`E_STEP83_PROJECTION`). The numeric gate also rejected a wrong hand-entered capacity-fraction
oracle with `E_PROBE_TOLERANCE`; it was replaced by the directly evaluated source-grounded
fraction. These failures are not PASS evidence; the final regenerated matrix and validator gates
are the only current evidence.

The first frozen content-PASS candidate was then rejected by two independent reviewers with
`P0/P1/P2=0/6/1`. Before repair, the validator reproduced the semantic defects as
`N02_LQ_BASIS_UNDERBOUND`, `N05_ZERO_CURRENT_SCOPE_UNDERBOUND`,
`N15_LOGISTIC_SIGN_WRONG`, `TOLERANCE_PROVENANCE_MISSING`, and
`SOURCE_LF_SHA_MISSING`; bounded document fixtures additionally exposed the stale Phase 067
parent-ledger row and Step 86 handover result pointer. The repaired matrix separates unresolved
Ah/C hypotheses, binds the finite independent `func_L_q` vector and comment-only positive enthalpy
compensation, limits zero-current equality to its declared fixture, uses the positive source logistic,
reconstructs all tolerance precedents, seals explicit LF hashes, and parses the two current document
pointers structurally. The rejected PASS is retained only as correction history.

The final validator runs named coordinated full-reseal mutations for omitted/duplicated `3600` and `1000`,
`func_L_q` value/compensation/basis-hypothesis drift, Ah/C resolution promotion, energy duplicate
conversion, current/reversible-heat sign, conditional zero-current drift or universal promotion,
Faraday omission/duplication, temperature omission, mass/capacity and component/total crosswire,
irreversible-heat overclaim, area/derivative sign and tolerance drift, bool/int and int/float swaps,
NaN/Inf/complex transport, row deletion/duplication/order, source path/blob/line/LF crosswire,
tolerance-precedent path/blob/release/line/source/AST/method mutation, open-gap promotion, authority
promotion and nested/top-level extra keys. It also runs strict JSON, exact Git-argv, and bounded
current-ledger/result-pointer controls. Current final counts are recorded by the validator output rather
than inferred here.

## Step 86 Reconciliation

Step 86 is no longer pending. Exact-eight commit
`4e8769e3253e7ffc1f4550e1bee3bc2563a5cfa7`, sole parent
`3f2c7635aa545bd617b6cd83b5e718683d5b2b1c`, and subject
`audit(phase067): adjudicate test demo golden behavior` are pushed/live/clean. Python 3.12 and
Python 3.14 both returned `PASS_P067_STEP86_PERSISTENCE`. The Step 86 correction history and its
test/demo/golden/tool/guide authority ceilings remain unchanged.

## Files

Exact-seven only, all mode `100644`:

1. `Codex/work/v1025_phase067/build_phase067_step87.py` (`A`)
2. `Codex/work/v1025_phase067/validate_phase067_step87.py` (`A`)
3. `Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json` (`A`)
4. `Codex/results/PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md` (`A`)
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md` (`M`)
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md` (`M`)
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` (`M`)

No `Claude/**`, production source, LaTeX, or PDF file is changed.

## Gate Boundary and Open Items

`PASS_P067_STEP87_UNIT_NUMERICAL` means the exact frozen source identities, dimensional arithmetic,
declared numerical fixtures and tolerances, schema and authority ceilings passed the precommit
content validator. It does not mean the Step 87 commit exists and does not imply the persistence
terminal. `Q_cell` Ah/C interpretation and executable seconds normalization remain open; any
downstream impact belongs to Step 88 and the previously carried accountable owners. Ref. 7,
original optimizer state, held-out/external/material authority and stale PDFs remain open.

Step 88 is blocked until root stages only the exact-seven, both runtimes pass `--verify-staged`,
the exact subject is committed/pushed/live/clean, independent review has P0/P1/P2=`0/0/0`, and
the same child returns dual `PASS_P067_STEP87_PERSISTENCE`.
