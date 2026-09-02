# Phase 067 Step 085 State, Default, Import, and Saved-Route Result

## Status

- phase/step: `067 / 85`
- selected Gate: `PASS_P067_STEP85_STATE_DEFAULT_IMPORT`
- precommit status: `PASS_PENDING_PERSISTENCE`
- expected parent: `f00bf2fa8f25c85f0c62cb901912763d98c8f070`
- expected subject: `audit(phase067): separate defaults state persistence`
- containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- postcommit terminal: `PASS_P067_STEP85_PERSISTENCE`
- exact-eight status: `A/A/A/A/A/M/M/M`
- self-audit: `P0/P1/P2=0/0/0`

This result is written before the two machine JSON outputs. It records the bounded Step 85
conclusion and does not claim staged, committed, pushed, live-remote, or persistence evidence.

## Recovery Read and Repository Boundary

The implementer directly read the following files from line 1 through EOF before Step 85 edits:

1. `Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md`, lines `1–766`.
2. `Codex/results/PHASE_067_STEP_084_PHYSICS_CALL_GRAPH_RESULT.md`, lines `1–128`.
3. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`, lines `1–164`.
4. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`, lines `1–185`.
5. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`, lines `1–438`.

The entry boundary was clean. Local `HEAD`, configured upstream, active tracking ref, and live
origin were the expected parent. Protected local/tracking/live remained
`fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`; main tracking/live remained
`4069cb36a8a52b1b88c29d68aa54dcbe915b1618`; local main was absent and the `Claude/**`
diff from the protected base was empty. Step 84 exact-seven commit
`f00bf2fa8f25c85f0c62cb901912763d98c8f070` was pushed/live/clean and Python 3.12/3.14
returned `PASS_P067_STEP84_PERSISTENCE`.

## Exact Inputs

The machine artifacts pin the committed Step 82 inventory and full-read attestation, the Step 83
state/quantity matrix, the Step 84 physics call graph, and the Phase 066 Step 80 matrix/runtime and
carry-forward delta by raw and semantic SHA-256. Frozen Git objects, not checkout-normalized bytes,
remain source authority. The complete Step 82 Python universe is preserved as `129` occurrences,
`84` unique blobs, `29,952` unique-blob physical lines, and `20` releases.

The production projection is lossless rather than endpoint-only: all `20` code occurrences and all
`15` corresponding unique Step 82 blob records are stored with their original occurrence ordinal,
manifest entry, mode, raw/LF hashes, extents, occurrence/release/role projections and genealogy.
Shared-blob bindings preserve all occurrence paths. `use_si_constants` occurs in exactly three code
occurrences (`v1.0.25`, `v1.0.25.1`, `v1.0.25.2`) over two unique blobs. The runtime focus is the
frozen v1.0.25.2 endpoint
`Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py`, baseline
`3b5fd059ed09cdcdde38668c399cb35b8afbcca9`, blob
`62b67e12724d8e1a8bbdd9f9432e4fcff864f0be`. Complete AST search over all `84/84`
unique Python blobs separates executable surfaces from comments or historical prose.

## Static Default and Surface Findings

The frozen executable module assigns:

- `DEFAULT_GRAPHITE_TRANSITIONS = GRAPHITE_STAGING_LIT`;
- `DEFAULT_SI_TRANSITIONS = None`;
- legacy `R=8.314`, `F=96485.0`, SI `R_SI=8.314462618`, `F_SI=96485.33212`, and
  `use_si_constants(True/False)` rebinding of the live module `R/F` pair;
- graphite/silicon background defaults `0.550/0.051`;
- `use_skew7_default(True)` rebinds future defaults to skew `7+7` and
  `use_skew7_default(False)` restores legacy `4+2`;
- `BlendedAnodeDQDV.__init__` reads the current module globals when explicit transitions are absent;
- `BlendedAnodeDQDV.from_wt` captured `q_gr=372.0` at function-definition time;
- graphite host transition lists preserve caller-list aliasing, while the selected silicon seed is
  copied into a new list.

The header/docstring 7-gallery-default narrative does not override these assignments. No executable
`use_legacy_4transition` definition was found. Complete `84/84` AST search returned
`SEARCHED_EXACT_NAMES_GROUND_NOT_FOUND` only for the closed vocabulary `load_profile`,
`from_profile`, `PROFILE_ALIASES`, `SAVED_PROFILES`, module `__all__`, and
`use_legacy_4transition`; this is not a claim that every arbitrarily named loader or export surface
is absent. The test's spec-loader and post-import
`use_skew7_default(False)` call are test mutation evidence, not a fresh public default.

## Bounded Isolated Runtime Contract

Exactly thirteen named cases were run independently on Python 3.12 and Python 3.14, producing
`26` isolated child processes. Every process used a repository-external disposable directory,
`-B -I -X utf8`, no network, no user site, no repository runtime current directory, and no
persistent bytecode/cache or user-state write. Each case begins with a clean production import;
only C06/C07 intentionally observe repeated import or explicit reload inside their own process.

| Case | Boundary | Grounded result |
|---|---|---|
| C01 | fresh baseline | public fresh blend is graphite `4` + silicon `2`; bound `q_gr=372.0` |
| C02 | explicit profile | explicit skew `7+7`; module globals remain fresh `4+2` |
| C03 | skew-default global rebind and silicon copy | existing object stays `4+2`; future object becomes copied `7+7` |
| C04 | in-place graphite list mutation | existing and future aliases observe graphite append |
| C05 | SI-constant `R/F` rebind and seed cache | live `R/F` and dynamic `func_w` change to exact SI values; imported scalar aliases and an existing object's `seed_L_V` remain fixed; a future seed changes; `False` restores legacy values |
| C06 | ordinary repeated import | same module object; mutated defaults persist |
| C07 | explicit reload | module dictionary resets future defaults/R/F, while the pre-reload object's transition identities, state and seed persist |
| C08 | two spec-loaded objects | distinct module objects; mutation of A does not alter fresh B |
| C09 | paired fresh process | C06 mutated total `14` and C09 fresh total `6` have distinct child PIDs per interpreter |
| C10 | bounded order A | SI then skew gives future `7+7`, SI `R/F`, and unchanged existing seed |
| C11 | bounded order B | skew then SI reaches the same future counts/seed/SI `R/F`, with unchanged existing seed |
| C12 | exact searched names | exact six absent names remain `GROUND_NOT_FOUND`; toggles and `R_SI/F_SI` remain present |
| C13 | saved config route | strict parse→canonical dump preserves semantic identity and direct constructor injection accepts `8/14/14`; kernel metadata is not dispatched and no production loader is used |

Python 3.12 and Python 3.14 observations are behavior-identical. The validator independently
reconstructs all thirteen grounded outcomes in fresh, isolated module objects rather than importing
the builder or production module in the controller.

## Saved Route and Owner Resolution

`A_regsol`, `B_gallery`, and `C_skew` parameter JSON files have transition counts `8/14/14`.
Their Git path/blob/mode, exact five-key top level, material, kernel, `N`, eight-key typed metrics,
exact transition keysets/types, finite values and canonical parse/dump hashes are preserved.
A/B/C transition keysets are respectively
`U/Omega/Q/w/Omega_over_RT/two_phase/x_binodal`, `U/w/Q`, and `U/w/Q/alpha`. The frozen
`build_two_versions.py` is writer evidence only; it is not relabeled as a production loader.
Configuration genealogy, strict parse/dump identity and bounded direct constructor injection do not
recover the original optimizer state, dispatch stored kernel metadata, invoke a production loader,
select a canonical material profile, or validate experiment/material truth.

`P066-OBL-0125` is bound directly to origin `P066-R80-14`, owner `P067-CODE-HISTORY`.
The Step 85 resolution is:

`BOUNDED_CONFIG_PARSE_CONSTRUCTOR_ACCEPTANCE_SEARCHED_EXACT_NAMES_GROUND_NOT_FOUND`.

The predecessor origin record hash, `PRESERVE`, `WITHHOLD`, both `OPEN_CARRY` states, target Phase
067, owner, and external-authority false value are exact-bound. The obligation remains
`BOUND_NOT_RESOLVED_OR_DISPATCHED`, not silently closed as recovered optimizer state. Saved JSON
parsing remains configuration evidence; only the explicitly searched names receive
`GROUND_NOT_FOUND`.

## Validation Boundary

The builder runs the bounded `26` child processes once, seals their canonical raw outputs, and proves
`2/2` deterministic reconstruction of all static evidence plus that sealed runtime projection. It
does not mislabel two independent runs with different child PIDs as byte-identical. The validator
independently checks frozen
AST identities, all-blob loader search, saved schemas, child process stdout/stderr/exit/timeout and
cleanup, cross-runtime behavior, source/control hashes, strict JSON, named semantic negatives, and
entry/terminal transaction equality. Content requires only the exact-eight worktree state. Staged
verification requires `A/A/A/A/A/M/M/M`, mode `100644`, exact index/worktree/blob equality, and no
extra or unstaged path. Persistence requires a single parent equal to the expected parent, exact
subject, paths, modes and committed bytes, local/upstream/tracking/live equality, clean tree,
protected/main invariance, local-main absence, and zero `Claude/**` drift.

Staged and persistence validation have not yet been claimed in this result. Step 86 remains blocked
until independent review is P0/P1/P2=`0/0/0`, the controller stages only the exact-eight, both
runtimes pass `--verify-staged`, and the same pushed/live/clean child passes dual
`PASS_P067_STEP85_PERSISTENCE`.

## Authority Ceiling and Open Gaps

- exact frozen source-static defaults and the named isolated runtime observations are established;
- general runtime/test correctness, scientific truth, material validity, canonical profile choice,
  original optimizer state, and publication readiness are not promoted;
- only the closed searched names listed above remain `GROUND_NOT_FOUND`; arbitrary loader/export
  absence is not promoted;
- external/held-out/material/Ref. 7/original optimizer and stale-PDF debts remain open carry and are
  not Step 85 PASS determinants;
- no `Claude/**`, production source, LaTeX, or PDF file was modified.

## Correction History

The initial working draft is not authority. It first failed on a wrong predecessor carry collection
key (`observation_records` instead of `step76_80_disposition_records`), then its validator admitted a
writer-as-loader mutation and a control-pin mutation. Those failures were repaired before the first
candidate. That candidate and its provisional PASS were then rejected by independent review: C05
did not actually exercise `use_si_constants`; production provenance was endpoint-only; saved/profile
and owner records were underbound; C09 used a self-asserted fresh-process claim; C10/C11 were the
wrong toggle orders; and nested runtime/schema valid-wrong mutations remained fail-open (the review
observed `13/14` attacks plus an observation extra-key reseal pass). The current repair preserves the
bounded C01–C13 design while adding exact `R/F` and seed-cache evidence, reload-existing-object
evidence, PID-paired C06/C09 evidence, SI↔skew order crossing, lossless `20/15` production records,
typed A/B/C schemas, exact predecessor owner binding, closed nested runtime schemas and `203/203`
named reseal-reject controls. Writer evidence remains separate from the exact searched-name
`GROUND_NOT_FOUND` boundary. Only the final JSON-last, dual-runtime validated byte set may support
the selected content Gate; every earlier candidate or provisional PASS is superseded.

The subsequent `70/70` candidate and its dual-runtime PASS were also rejected. Independent review
proved that coordinated valid-wrong mutations of both runtime observations could change C01
`ordinary_reimport_same_object` or `from_wt_q_gr_default`, C06 `same_module_object`, and C08
`distinct_objects`, then recompute observation, stdout, runtime and matrix seals while leaving
`artifact_errors=[]`. The repair exact-binds every C01–C13 case-specific scalar, Boolean, list,
identity duplicate and event projection to source/static or independently executed ground. It adds
one full-reseal negative for every one of the `52` case-specific fields plus four common fields;
with the prior controls plus exact runtime-micro and C06/C09 PID-invariant probes, the required set
is now superseded by the final `203/203` set. Each stored interpreter version is exact-compared with
a fresh independent child.
Other PIDs are positive transcript identifiers only and are not claimed reproducible; only the
stored C06/C09 pair's same-interpreter inequality supports the fresh-process boundary. The rejected
`70/70` bytes are not
authority.

The later Round 2 `128/128` candidate was rejected after coordinated full resealing showed that
Python equality admitted JSON type substitutions with equal values: `true→1`, integral
`float→int` (including `372.0→372`), and runtime version `3→3.0`. Round 3 replaces every
JSON-derived exact projection comparison with recursive type-strict equality, exact-binds source and
writer anchors, and adds equality-compatible full-reseal controls across all numeric/Boolean-bearing
case fields, common observations, runtime identity, metadata, projection, saved-route, owner,
authority, aggregate, process-pair, default and runtime-binding surfaces. The final named set is
`203/203`; the Round 2 bytes and PASS are not authority.
