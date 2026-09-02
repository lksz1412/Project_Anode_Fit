# Phase 067 Step 086 Test, Demo, Golden, Guide, and Tool Result

## Gate

`PASS_P067_STEP86_TEST_DEMO_GOLDEN`

Precommit status: `PASS_PENDING_PERSISTENCE`.

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`.

Persistence terminal after the exact child is committed, pushed, live, clean, and
verified by Python 3.12 and Python 3.14: `PASS_P067_STEP86_PERSISTENCE`.

Expected parent: `3f2c7635aa545bd617b6cd83b5e718683d5b2b1c`.

Expected subject: `audit(phase067): adjudicate test demo golden behavior`.

Step 87 is blocked until the same Step 86 child passes independent P0/P1 review,
dual staged verification, push/live/clean verification, and dual persistence.

## Inputs and Recovery Coverage

- Phase 067 detailed plan: lines 1–766 read, including Step 86 lines 430–459.
- Step 85 result: lines 1–199 read.
- parent execution ledger: lines 1–EOF read.
- canonical execution ledger: lines 1–EOF read.
- active handover: lines 1–439 read.
- frozen source manifest: strict duplicate-key parse and full recursive traversal.
- Step 82 source inventory and full-read attestation: strict duplicate-key parse,
  pinned raw/semantic identity, and lossless occurrence/blob projection.
- frozen Git blobs: test `29/29` and 6,042 unique physical lines; demo `26/26`
  and 3,300 lines; result/tool `14/14` and 2,081 lines; guide `8/8` and 854
  lines; golden `2/2` ZIP archives and all `26/26` NPY members.

The source-object baseline is `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
The persisted evidence chain is Step 82 `db167fdc941eafba0313b8476dfe7483108f13ff`
→ Step 83 `1af6c06fb5cff2918b846ed74ea213832f04f010` → Step 84
`f00bf2fa8f25c85f0c62cb901912763d98c8f070` → Step 85/current parent
`3f2c7635aa545bd617b6cd83b5e718683d5b2b1c`. The Step 82 artifact's
result-first containing-commit placeholder is not relabeled as current ownership.

## Exact Scope

| Family | Occurrences | Unique blobs | Unique physical lines |
|---|---:|---:|---:|
| tests | 44 | 29 | 6,042 |
| demos | 30 | 26 | 3,300 |
| result/tool Python | 35 | 14 | 2,081 |
| FITTING_GUIDE | 20 | 8 | 854 |
| golden_graphite_ref.npz | 8 | 2 | binary |

Manifest release order, manifest entry index, path, role, Git mode, blob OID,
Step 82 blob ordinal, size, and physical extent remain separate per occurrence.
Byte-identical occurrences are projections of one Git object, not independent
corroboration.

## Test Enforcement Adjudication

The 29 unique test blobs / 44 occurrences divide exactly as follows:

- `ASSERT_AND_EXIT`: `6/9` unique blobs/occurrences.
- `EXIT_ONLY`: `12/20`.
- `NO_EXECUTABLE_GATE`: `11/15`.

The sample/manual family and reflect family print or plot observations without an
assertion or exit gate. Printed `PASS`, finite values, or a zero process exit in
those scripts is not promoted to a gating assertion. Self-consistency and v1.0.25
gate scripts use explicit exit routes. Main gate-family scripts combine assertions
with exit behavior. These are top-level scripts rather than a pytest collection;
inventory presence, framework collectability, runtime execution, skip predicates,
observed skip, and exit outcome are distinct typed fields.

Every unique test blob is materialized under a fresh repository-external disposable
root and attempted with Python 3.12 and Python 3.14. Regression scripts receive the
explicit `verify` argument. Each record binds launcher, argv, stdout/stderr and
hashes, timeout, exit, assertion/exit counts, output mutation/residue, and one of
the closed outcomes `PASS_EXIT_GATE`, `FAIL_EXIT_GATE`, `MANUAL_OBSERVATION`,
`EXPECTED_FAILURE`, `DEPENDENCY_MISSING`, `TIMEOUT`, or `GROUND_NOT_FOUND`.
An optional-dependency or hard-coded-path diagnostic is not a skip or PASS.

## Demo Adjudication

All 26 unique demo blobs have zero AST `Assert`. Exactly `1/1` unique
blob/occurrence (`fit_roundtrip_demo.py`) has an exit gate; `25/29` have no
executable gate. Plot, print, and finite-value observations remain manual software
observations. Matplotlib runs use the noninteractive Agg backend in disposable
roots. No demo observation is material, scientific, or canonical-release proof.

## Disposable Cache Correction

The first full deterministic replay candidate was rejected. The first differing
pointer was `runtime_records[0].filesystem_changes[0].after.sha256` for blob
`088e5c8887ed5a2ef6847de74725fff4fd211041`, script
`Claude/docs/v1.0.18.2/graph_suite_v1018_2.py`, and disposable file
`home/.matplotlib/fontlist-v390.json`. Two repeats had identical target stdout and
stderr but different font-cache bytes. The repair preserves exact path, creation,
size, count, cleanup boundary, and class `NONDETERMINISTIC_THIRD_PARTY_CACHE`, while
withholding only that allowlisted third-party cache content hash. A regression
fixture proves the same rule does not hide a non-cache output hash, path, size, or
count change. No other output or transcript is normalized.

The next frozen replay candidate was also rejected at
`runtime_records[108].stderr`: the same expected v1.0.25.1
`test_gates_v1025.py` `FileNotFoundError` carried the random disposable root in
Python's doubled-backslash exception representation. The exception type, missing
`_sections` suffix, exit, and all non-root text were identical. The repair adds
only the exact doubled-backslash spelling of the already-authorized disposable
root to path normalization. Raw-backslash and POSIX forms remain covered, and a
negative fixture proves a non-temp traceback/path is unchanged. No general
backslash regex or diagnostic suppression was introduced.

## Independent Review Repair

The first frozen content-PASS candidate was rejected after independent review.
It used one-based `manifest_entry_index` values although the Phase 056/Step 82
manifest enumeration is zero-based; it also failed open on valid-resealed guide
blob/line provenance fields and the four runtime/golden/guide/tool contract maps.
A coordinated forged runtime transcript and filesystem projection could likewise
pass after its local hashes and artifact semantics were resealed, and the Step 82
full-read attestation was named in `inputs` without an independent raw/semantic
load. The repaired candidate uses the original zero-based manifest indices,
reconstructs every guide blob and all 854 typed line records from frozen Git
objects, exact-binds the four contract maps, pins the deterministic 110-record
runtime section, and independently strict-loads and verifies the attestation.
Named full-reseal controls cover each rejected class. Final content controls are
`54/54` semantic and `7/7` strict-loader controls on both Python runtimes.

A later final review rejected that candidate because the persistence `diff-tree`
allowlist applied its hexadecimal predicate to the terminal empty argument, making
the validator's own call unreachable. An initial suggestion to allow `""` was
also rejected after an independent real Git probe returned exit 128 for the empty
revision/path argument. The final call and allowlist require the literal `--`
revision/path separator. One reachable known Step 85 exact-eight comparison and
nine malformed/empty/swapped/path/option/extra-argument cases pass `10/10` without
executing rejected payloads.

An independent reviewer then rejected the frozen candidate because the authoritative
parent-ledger Step 85 paragraph still combined the already persisted commit with
`PASS_PENDING_PERSISTENCE`, `expected parent`, and malformed containing-commit wording.
The bounded Step 85 paragraph now states the actual commit `3f2c7635aa545bd617b6cd83b5e718683d5b2b1c`,
its sole Git parent `f00bf2fa8f25c85f0c62cb901912763d98c8f070`, exact subject,
pushed/live/clean state, and dual `PASS_P067_STEP85_PERSISTENCE`. A proposed
`919af57fa44dd9ecc15d4096f2178c178a200a68` parent value was discarded after direct
Git `%P` verification. The stale fixture is rejected and the repaired bounded paragraph
passes the named document controls `2/2`; historical pending wording outside that paragraph
is not globally prohibited.

## Golden Adjudication

The two golden blobs remain distinct:

- `fc5a0189abc7c9d180236d2d431e63ad7838e495`, v1.0.13–v1.0.14,
  raw SHA-256 `21fb6f9c9dc7bd3158b51268bd9f883dfdec562474e0c4804700ce3ced125fd6`.
- `8932d9dbfc165eeb39ec5cab23337d4582ba0ae8`, v1.0.15–v1.0.19,
  raw SHA-256 `61b7f59b809417f46618039d1eecf5cc1aca9ed2d0202fcda7d909386c00d0c2`.

Each has 13 ordered uncompressed `<f8` arrays of shape `[1000]`, all finite. ZIP
member, CRC, compression, NPY header, member byte, value byte, dtype, shape,
first-order statistics, and outer blob hashes are bound. `V` and
`equilibrium_298` are byte-identical between the two blobs; the other eleven arrays
are not flattened. v1.0.13–v1.0.18.2 explicit capture uses overwrite-capable
`np.savez` only on a disposable copy. v1.0.19 refuses an existing golden with exit
3. Later test-gate loading of the v1.0.19 golden is auxiliary comparison evidence,
not provenance for a current-release golden.

## Result and Tool Adjudication

The 14 unique result/tool blobs / 35 occurrences divide into `ASSERT_ONLY=1/1`,
`EXIT_ONLY=5/18`, and `NO_EXECUTABLE_GATE=8/16`. Only `gen_coords_ff3.py` has
assertions, seven in total. `tools_check_structure.py` check, snapshot-writer, and
diff modes remain separate. Plot/coordinate emitters and stdout are not enforcement
unless an exact assertion or exit branch exists. Hard-coded Windows paths,
optional imports, file inputs, outputs, mutation surfaces, and cleanup surfaces are
recorded rather than translated into a generic skip.

## FITTING_GUIDE Conformance

The exact suffix `/FITTING_GUIDE.md`, manifest role `implementation_guide`,
extension `md`, and review mode `FULL_TEXT` select exactly 20 occurrences / eight
blobs. Every one of the 854 unique physical lines belongs to one and only one
closed line kind and keeps exact line text/body hash and occurrence references.
Headings and title spelling remain separate from release occurrence labels. Shared
stale titles are preserved, including v1.0.16 title text projected into v1.0.17,
v1.0.18.1, and v1.0.18.2, and v1.0.20 title text projected through v1.0.25.2.

Guide statements about Phase-E holdout, PASS, 확정, 실증, regression, or fitting
remain instruction/self-report unless an exact source assertion and isolated
runtime record bind the stated software behavior. Even a referenced exit-zero
script is not proposition, science, or material proof. Known unimplemented/GNF
caveats remain open; no guide prose is used to fill an absent source edge.

## Authority Boundary

This Step establishes frozen source identity, static enforcement structure,
isolated software-process observations, golden file structure/value identity, and
guide/tool conformance routing only. It does not establish external scientific
truth, material/experimental validity, held-out performance, original optimizer
state, canonical release selection, final manuscript readiness, or publication
authority. No production source, Claude artifact, LaTeX, or PDF was changed.

## Outputs

1. `Codex/work/v1025_phase067/build_phase067_step86.py` (`A`)
2. `Codex/work/v1025_phase067/validate_phase067_step86.py` (`A`)
3. `Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json` (`A`)
4. `Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json` (`A`)
5. `Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md` (`A`)
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md` (`M`)
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md` (`M`)
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` (`M`)

Exact status must be `A/A/A/A/A/M/M/M`, mode `100644`, with no rename/delete or
extra path.

## Validation Boundary

The validator independently reconstructs occurrence/blob/line denominators,
source AST anchors and enforcement, guide full-line partition, golden ZIP/NPY
members and values, runtime transcript consistency, and authority ceilings. It
uses strict duplicate-key/nonfinite JSON, recursive type-strict equality, full-
reseal semantic negatives, exact content/staged/persistence transaction seals,
single-parent `%P`, exact subject/path/mode/blob bytes, local/upstream/tracking/live
origin, protected/main, and Claude non-change.

No staged or persistence PASS is claimed in this precommit result. Step 87 remains
blocked until the controller completes independent P0/P1/P2=`0/0/0`, dual staged,
commit/push/live/clean, and dual `PASS_P067_STEP86_PERSISTENCE` for the same child.
