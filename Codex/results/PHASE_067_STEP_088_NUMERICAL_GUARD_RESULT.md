# Phase 067 Step 88 Numerical Guard Impact Result

## Status

- Gate: `PASS_P067_STEP88_NUMERICAL_GUARD`.
- Persistence state: `PASS_PENDING_PERSISTENCE`.
- Expected parent: `ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4`.
- Expected subject: `audit(phase067): bound numerical guard impacts`.
- Postcommit terminal: `PASS_P067_STEP88_PERSISTENCE`.
- Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`.
- external scientific/material/experimental/canonical/publication authority: false.

This Gate closes the frozen-source identity, internal software behavior, and bounded
numerical-impact inventory for Step 88. It does not certify a physical model,
material parameter, experiment, canonical equation, optimizer convergence, or
publication readiness.

## Recovery and Inputs

The implementer read the Phase 067 detailed plan, Step 87 result, both execution
ledgers, and active handover from line 1 through EOF before edits. The clean entry
boundary was observed directly: local HEAD, configured upstream, active tracking ref,
and live origin were all `ba331b7ad7eb66a2e16ab494d890a15c3b5e8bd4`;
protected local/tracking/live remained `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`;
main tracking/live remained `4069cb36a8a52b1b88c29d68aa54dcbe915b1618` at that entry boundary;
local main was absent; the worktree was clean; and the Step 87 commit changed no
`Claude/**` path. Python 3.12 and 3.14 independently returned
`PASS_P067_STEP87_PERSISTENCE` for the same child.

On the 2026-09-06 recovery check, live `main` had independently advanced by seven
commits to `f0c381bd6dc315ac75cbffa93dd86ce83a37949b`. Its merge base with the
Step 88 expected parent remains the former main tip
`4069cb36a8a52b1b88c29d68aa54dcbe915b1618`; all 25 paths changed by that
parallel advance are under `Claude/**`, and zero are under `Codex/**`. The
updated `origin/main` tracking ref is pinned to the same live tip. This parallel
history is neither merged into the active branch nor used as Step 88 scientific,
material, canonical, or publication authority, and it changes no numerical
matrix input or conclusion.

Pinned committed inputs are the Step 82 source inventory and full-read attestation;
Step 83 state-flow; Step 84 call graph; both Step 85 state/default/import and saved-route
runtime matrices; both Step 86 test/demo/golden and guide/tool matrices; Step 87
unit/numerical evidence; and Phase 066 Direct14 fit reproduction. All are strict-parsed,
content-addressed and semantically used or explicitly bounded. Frozen Git blobs, not
prose, remain source authority.

## Scope and Coverage

- production projection: `20/20` occurrences, `15/15` unique blobs, canonical release order;
- nonproduction projection: `109` total, exactly `1` selected supplemental optimizer
  occurrence and `108` excluded occurrences;
- candidate disposition: all `84/84` Python blobs, with broad lexical discovery
  explicitly non-authoritative;
- supplemental optimizer source: v1.0.19 `fit_roundtrip_demo.py`, one occurrence/blob;
- guard records: `24/24`;
- quantitative/static impact probes: `27/27`;
- closed numerical-default records: `8/8`;
- optimizer route records: `3/3`, separating backend selection from termination/convergence.

The source projection stores each shared production blob once and preserves every
release/path/blob/blob-ordinal/manifest-entry occurrence. Ordered anchor lists preserve
repeated sites and carry qualified owner, AST kind, line extent, exact LF-normalized
source hash, stable AST hash, and expression. Every selected source row is cross-bound
to its Step 82 inventory record and `READ_FULL` attestation, including raw/LF hashes,
extents and occurrence projection.

## Guard Findings

### Overflow, clip, and denominator boundaries

The frozen logistic `np.where` returns finite values at the fixed extreme vector but
both branches evaluate: the isolated NumPy observation records three overflow and one
invalid-divide warnings. This is finite returned state with warnings, not warning-free
numerical success.

The entropy `xi` clip at `eps=1e-12` bounds the logit to
`±27.63102111592755`. Area, center, sign, continuity and monotonicity are explicitly
`NOT_APPLICABLE` to this state clip; no returned-`dQ/dV` proxy is invented. The
denominator guard separately maps `den<=0` to zero and floors small positive
denominators. The v24/v24.1 regular-solution `z` clip at `±350` is a separate,
removed-after-v24.1 helper boundary. Its bounded `V∈[-20,20]` before/after area,
center, sign, monotonicity and exact clip-boundary continuity are calculated; the
globally nonzero clipped tail is recorded as divergent, not a finite global area.

Dual isolated NumPy observations of fixed-vector `func_L_q` arithmetic distinguish
underflow, finite output, and overflow without guessed exponent thresholds. The finite
path applies `abs(dVdq)*L_q`; the resolver maps a nonfinite result to `L_V=0`. The
ratio path separately records local exponential overflow/underflow: infinite local
length freezes the state and zeroes the peak, while zero local length raises uncaught
`ZeroDivisionError`. Neither boundary is successful kinetics.

### Sorting, interpolation, padding, and causality

Releases v1.0.10–v1.0.14 sort voltage, interpolate temperature to a work grid, and
interpolate the result back. A no-tie fixture exact-binds sort and endpoint constant
clamping. Duplicate-voltage ordering was not executed and is not claimed; there is no
portable tie contract. Nonmonotonic chronological order is discarded. Releases
v1.0.15 onward stable-sort by voltage and inverse-restore output positions, which
preserves sample correspondence but not arbitrary within-call chronology. For charge,
full reversal after stable ascending sort reverses equal-voltage tie order.

The v25 family padding extends five lag lengths with nominal step at most `L/20`, but
caps at 4000 points. Executable deterministic arrays prove the five-lag span, original
sample suffix, direction and extended-grid content reevaluation while exposing
coarsening. A zero first interval returns `npad=0` even when a later interval is nonzero.
The strict resolution predicate preserves the memory path at `lag*40 == char_h` and
selects equilibrium at the next-lower representable lag. For the pre-v25 no-pad helper,
the returned peak-shape and state deltas are stored; the fixture is not generalized to
the v25+ path that pads before pointwise memory. The strict `a<1e-4` boundary also stores
its one-ULP branch-output jump.
These are implementation boundaries, not external causal/physical validation.

### Root and optimizer outcomes

Invalid root domain/capacity/bracket cases fail with `ValueError`. In contrast,
`max_iter=0` and insufficient iteration silently return a midpoint with no convergence
flag; both are recorded `FAIL_NONCONVERGED_SILENT_RETURN`. Eight closed default records
bind entropy epsilon, resolution cap, pad span/divisor/cap, regular-solution floor/clip,
legacy work-grid settings, root tolerance/iterations, and both optimizer backends'
stopping/budget values. These are software choices, not physical constants.

Optimizer backend selection and convergence are separate. The v1.0.19 demo prints
whether SciPy or pure-NumPy Nelder-Mead was selected. That disclosure does not prove
convergence. SciPy `sol.x` is consumed without `sol.success`; pure Nelder-Mead sorts
and returns its best simplex point after its loop even on budget exhaustion. The
persisted Direct14 selected trial 11 is bound as `status=0`, `success=false`,
`nfev=6000`, `njev=5656`; its finite returned vector remains nonconverged.

Missing kinetics (`I<=0` or absent `dH_a`) is an explicit intended equilibrium/no-tail
contract. A direct finite `L_V` override and the `Omega<=2RT` zero-gap branch are also
intended model behavior. They are not conflated with nonfinite kinetics, underresolved
memory, or iteration-exhaustion fallbacks. Transfer-helper uniform-grid/length checks
remain `GROUND_NOT_FOUND_EXECUTABLE_GUARD`: prose preconditions are not executable
validation.

## TDD and Negative Controls

The initial RED validator failed `E_MATRIX_MISSING` before builder output existed.
GREEN implements strict canonical JSON, duplicate/nonfinite rejection, recursive typed
equality, exact metadata and section seals, independent Git-blob identity/anchor
reconstruction, and named full-reseal mutations. The controls reject root midpoint or
optimizer result promotion, backend-print/`sol.x`/Nelder exhaustion promotion,
fallback-to-intended crosswires, clip/default/operator mutations, before/after metric
swaps, source occurrence/blob/raw/LF/anchor crosswires, delete/duplicate/order changes,
extra keys, authority promotion, and bool/int or int/float substitutions. The final
semantic mutation suite is `64/64`; strict JSON fixtures are `7/7` and bounded control-
document mutations are `2/2`. Source policy exact-binds imports and function sites,
process and Git call inventories, the sole atomic JSON writer, filesystem mutation
sites, dynamic import/dunder restrictions, and module/callable transport. Twenty-nine
named AST-only attack payloads are rejected `29/29` without executing a payload.
Every JSON is rejected before parsing above `8,000,000` bytes or lexical nesting depth
`64`; iterative traversal then rejects more than `600,000` nodes.

Independent reviews rejected the intermediate 21-guard/25-probe design because it
kept only earliest anchors, omitted required input/default/scope provenance, underbound
runtime processes, and conflated optimizer selection with termination. The repaired
24-guard/27-probe design preserves repeated anchors, full-read cross-bindings, dual
runtime transcripts, actual pad arrays, bounded clipping deltas, strict resolution and
small-`a` deltas, direct-override behavior, and ratio local-exponential propagation.

## Open Boundaries

- `Q_cell` Ah-versus-C basis and absent executable `/3600` remain with the existing
  Phase 066/Step 87 owners.
- arbitrary nonmonotonic chronology is not represented by voltage sorting;
- root and optimizer results do not carry convergence status on every exhaustion path;
- transfer-helper executable precondition checks are ground-not-found;
- external physical accuracy and original optimizer state are ground-not-found.

## Exact-Seven Boundary

Only the Step 88 builder, validator, matrix, this result, two ledgers, and active
handover are in scope, with status `A/A/A/A/M/M/M`. No production or `Claude/**` file
was edited. This result is written before the canonical JSON. Step 89 is blocked until
the controller stages only the exact seven, obtains dual staged validation, commits
with the exact subject, pushes, verifies live/clean refs, and both runtimes return
`PASS_P067_STEP88_PERSISTENCE` for the same child.

## Correction History

- The first combinatorial idea was not used; the final design stores unique source
  objects once and preserves occurrence references.
- The first 14-guard/16-probe preview was expanded before JSON collection after
  independent pre-audit identified seven underrepresented boundaries: entropy
  denominator, v24 regular-solution clipping, charge equal-voltage tie reversal,
  first-step-zero padding, strict resolution equality, transfer guard GNF, and
  persisted optimizer nonconvergence. The superseded preview is not a Gate.
- The subsequent 21-guard/25-probe preview and its PASS output were rejected at
  `P0/P1/P2=0/7/1`, then residual `0/3/1`. The fabricated entropy shape proxy,
  incomplete regular-solution metrics, guessed exponent thresholds, unexecuted
  fallback claims and underbound source/default/runtime provenance are all superseded
  by the repaired 24/27/8 projection. Rejected previews are not persistence evidence.
- A later builder review rejected an overbroad I21 returned-path claim and inconsistent
  observation labels. The repaired I21 is explicitly pre-v25/no-pad; duplicate-voltage
  interpolation remains not executed/not claimed; root failure and direct-LV evidence
  are labeled source-static unless a sealed runtime transcript exists.
- The next exact-seven independent review returned two P1 findings. The validator's
  former source scan did not close callable/module aliases, shell-enabled process calls,
  arbitrary Git argv, or filesystem writers, and the result text incorrectly called an
  unexecuted duplicate-voltage case a runtime observation. The repaired policy uses
  exact structural inventories plus `20/20` nonexecuted attack probes; the result now
  states that only the no-tie fixture ran and duplicate-voltage behavior is unexecuted
  and unclaimed. The rejected review state is not persistence evidence.
- Re-review rejected that intermediate `20/20` policy because a mutation-capable bound
  method could be transported through an approved name or higher-order keyword, and a
  UNC `Path.read_text()` could initiate undeclared network I/O. The final policy forbids
  approved-name/function rebinding, rejects sensitive attribute transport, and exact-
  binds every `Path` constructor and filesystem-read site. Five new AST-only probes bind
  both writer transports, function-name rebinding, and direct/transported UNC reads;
  current controls are `25/25`. No injected payload is executed.
- A third review rejected global allowance of nested helper names: `pairs = main;
  pairs()` could transport and call the builder entry point. The builder's local probe
  constructor was renamed from collision-prone `row` to `probe_row`; nested calls are
  now owner-scoped, all declared function bindings are protected, and declared
  callables cannot be transported except the exact strict-JSON `pairs` hook. Two added
  probes reject nested-name and higher-order declared-callable transport, bringing the
  current nonexecuted source-policy suite to `27/27`. The `25/25` state is superseded.
- A final pre-freeze red-team pass found that `argparse.FileType` could be transported
  through an approved higher-order call and that `ArgumentParser(fromfile_prefix_chars=...)`
  could activate undeclared file or UNC input. The source policy now protects the
  `argparse` module binding, exact-binds its sole module attribute and constructor call,
  and adds two AST-only negative probes. The current suite is `29/29`; the `27/27`
  state is superseded, and neither attack payload is executed.
- Final gate review rejected an impossible staged-state predicate and an unbounded JSON
  parser. Staged validation now requires an exact-seven index diff against the fixed
  parent, permits only in-scope staged `A `/`M ` porcelain rows, and requires an empty
  index-to-worktree diff; this also supports a bounded amend without hiding companions.
  The amend route accepts only the named rejected candidate, rechecks its direct parent
  and subject with `--no-patch`, and rejects every other staged `HEAD`.
  JSON validation now
  enforces pre-parse byte/depth limits and an iterative node limit, with three new
  controls raising the strict suite from `4/4` to `7/7`. The rejected state is not
  persistence evidence.
- The first JSON-last content candidate was rejected by `E_GIT_ARGV_CONTROL`: its
  negative fixture exposed that the allowlist accepted mismatched `commit^` and commit
  OIDs. An interim uppercase-only fixture correction was rejected on independent review.
  The final predicate requires `args[5] == args[6] + '^'`, retains the mismatched-child
  negative, and the bounded control passes `7/7`.
- That repaired candidate next exposed `E_CONTENT_STAGED`: content mode had treated the
  three baseline-tracked control documents returned by `index_snapshot()` as staged
  deltas. The final gate tests the parsed cached diff for emptiness; staged mode retains
  the exact-seven index snapshot contract.
- The next candidate reached the final content checks but a redundant all-tree
  `git diff --name-only` rejected Git's exact CRLF-conversion warnings despite return
  code zero and correct stdout. Exact content status already proves the seven-path
  delta, so the warning-sensitive duplicate check was removed; Claude drift remains
  separately sealed.
- A 2026-09-06 recovery rerun correctly failed `E_REPOSITORY_REFS` after the
  separately maintained `main` branch advanced from `4069cb36...` to
  `f0c381bd...`. GitHub comparison and fetched object genealogy show exactly seven
  descendant commits and 25 changed paths, all under `Claude/**`, with the former
  main tip as the exact merge base against the Step 88 parent. The validator now
  pins both tips, the merge base, commit count, path count, and zero non-Claude
  paths; three new malformed-argv controls raised the then-current Git allowlist gate
  from `7/7` to `10/10`. This is an external parallel-history correction, not a Step 88
  source, matrix, or authority change.
- The first pushed candidate `6ee61ea9e5636a66e0aa217e4929e60897d8b073`
  correctly failed dual persistence with `E_COMMIT_PARENT`: its metadata query used
  `git show --format=...`, whose stdout also contained the patch. Both subject and
  parent queries now require `--no-patch`; the old forms are rejected, and four added
  good/bad shape checks raise the Git allowlist suite from `10/10` to `14/14`. The
  failed candidate is not persistence evidence; only an amended child that passes
  persistence can replace it.
