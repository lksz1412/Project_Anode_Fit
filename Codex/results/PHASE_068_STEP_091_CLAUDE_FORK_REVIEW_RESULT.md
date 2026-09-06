# Phase 068 Step 91 — Claude Fork Full-Read Review Result

Date: 2026-09-07

Phase: `068`

Cumulative Step: `91`

Status: `PASS_PENDING_PERSISTENCE`

Selected Gate: `PASS_P068_STEP91_CLAUDE_FORK_READ`

Persistence terminal: `PASS_P068_STEP91_PERSISTENCE`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Current-state marker: `P068_STEP91_CLAUDE_FORK_READ_PRECOMMIT`

Expected parent: `d54d1a2b2378369cbeaef757309b3ed629491d2c`

Expected subject: `audit(phase068): read claude fork history`

Predecessor terminal: `PASS_P068_PLAN_ACTIVATION_PERSISTENCE`

Next cumulative Step: `Step 92`

## Result Boundary

Step 91 proves the frozen Claude-fork commit topology, both parent edges,
the three net modified paths, byte-zero-to-EOF coverage of every implicated
before/after text blob, and lossless extraction of the fork's claims. It does
not accept a commit message, archive note, TeX footnote, handover, prior probe,
or agreement between AI-authored records as scientific truth.

The content Gate is selected because the bounded source-read and claim-routing
work is complete. The transaction remains precommit evidence only. Step 92 is
blocked until the exact-eight transaction is committed, pushed, observed at
the live remote with a clean worktree, and both runtimes return the reserved
`PASS_P068_STEP91_PERSISTENCE` terminal.

## Exact-Eight Persistence Set

1. `Codex/work/v1025_phase068/build_phase068_step91.py`
2. `Codex/work/v1025_phase068/validate_phase068_step91.py`
3. `Codex/results/PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json`
4. `Codex/results/PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json`
5. `Codex/results/PHASE_068_STEP_091_CLAUDE_FORK_REVIEW_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required precommit status is exactly `A/A/A/A/A/M/M/M`; every mode must be
`100644`. No `Claude/**`, production source, protected branch, frozen fork ref,
or `main` path belongs to this transaction.

## Result-First and JSON-Last Boundary

- The builder, validator, this result, both ledgers, and active handover are
  frozen before either new JSON artifact is written.
- The validator was executed while the inventory JSON was absent and returned
  the required `E_OUTPUT_MISSING` RED state on Python 3.12 and Python 3.14.
- `Codex/results/PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json` and
  `Codex/results/PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json` are generated
  only after these six non-JSON records are fixed.
- A passing content run, deterministic pair, staged run, commit, push, or
  persistence run is not pre-claimed by this result.

## Frozen Git Topology

| Object | Exact identity | Directly established |
|---|---|---|
| common base | `3b5fd059ed09cdcdde38668c399cb35b8afbcca9` | merge base and first parent |
| Claude commit 1 | `2802395dd03e6cabe3e981bddddbba139e3963bc` | sole parent is the common base |
| Claude commit 2 / tip | `e3e1a634f34b711aa4803fd190fe9120f1755f13` | sole parent is commit 1 |

The base-to-tip set contains exactly two commits in that topological order.
The two parent-edge path counts are exactly `2/1`, totaling three edge events.
The base-to-tip net tree contains exactly `net 3` modified paths, all mode
`100644`:

| Edge | Path | Old blob | New blob | Status |
|---|---|---|---|:---:|
| base → `2802395d...` | `Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md` | `537d2a25326116067a079a978dcd1f272a75ed7b` | `6b2cdd9e16ca99d26b0879d28a30b3322d43015e` | M |
| base → `2802395d...` | `Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex` | `ea762ff015f47e03b79e99f051deae5ddef44f9c` | `05f1d84713017dde303f56ca7004b61aa0496979` | M |
| `2802395d...` → `e3e1a634...` | `Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md` | `7aa93a497eb660d40fbfea43f47960aed750c661` | `b763605ab233303e93d25cf0843851b4c96beef7` | M |

The exact commit subjects are:

1. `fix(v1.0.25.2): 문턱 근방 스케일링 각주 오류 정정 — Codex 교차검증 수용 (U13)`
2. `docs(v1.0.25.2): 핸드오버 갱신 — Codex 11f9054 대조 상태 + U13 오류 기록`

## Complete Read Coverage

Both commit messages and all `6` unique before/after blobs were read from byte
0 through EOF. No unread interval, output truncation, decode failure, binary,
or PDF object exists in this Step 91 source set.

| Path state | Blob | Raw bytes | Physical lines | Coverage |
|---|---|---:|---:|---|
| archive before | `537d2a25326116067a079a978dcd1f272a75ed7b` | 30,245 | 381 | `1–EOF`, no gap |
| archive after | `6b2cdd9e16ca99d26b0879d28a30b3322d43015e` | 32,409 | 406 | `1–EOF`, no gap |
| TeX before | `ea762ff015f47e03b79e99f051deae5ddef44f9c` | 26,835 | 253 | `1–EOF`, no gap |
| TeX after | `05f1d84713017dde303f56ca7004b61aa0496979` | 27,406 | 258 | `1–EOF`, no gap |
| handover before | `7aa93a497eb660d40fbfea43f47960aed750c661` | 10,087 | 175 | `1–EOF`, no gap |
| handover after | `b763605ab233303e93d25cf0843851b4c96beef7` | 14,150 | 219 | `1–EOF`, no gap |

The machine attestation stores raw and normalized-LF SHA-256 separately and
maps each unique blob to every edge occurrence. Checkout CRLF bytes and
absolute workspace paths are not treated as canonical object identity.

## Atomic Claim Register

The `C91-01..C91-98` register contains 98 atomic propositions and 222 exact
claimant-surface pointers. Each machine row carries the normalized proposition,
domain, assumptions, quantity/unit/sign/basis field, claimant surfaces,
self-report status, truth status, supporting/refuting evidence IDs, authority
ceiling, owner, route, and `scientific_truth_promoted=false`. “Verified text”
means only that the exact historical text exists at the stated object; it does
not make its scientific content true.

| Claim | Atomic proposition | Pointer count | Truth status / owner |
|---|---|---:|---|
| `C91-01` | fixed first commit, parent, and subject | 2 | repository object verified; Step 91 |
| `C91-02` | fixed second commit, parent, and subject | 2 | repository object verified; Step 91 |
| `C91-03` | fixed archive path/mode/blob edge | 1 | tree edge verified; Step 91 |
| `C91-04` | fixed TeX path/mode/blob edge | 1 | tree edge verified; Step 91 |
| `C91-05` | fixed handover path/mode/blob edge | 1 | tree edge verified; Step 91 |
| `C91-06` | exactly three fixed base-to-tip net paths | 1 | tree topology verified; Step 91 |
| `C91-07` | old TeX asserted value continuity | 1 | historical text only; Step 94 |
| `C91-08` | old TeX asserted derivative divergence and slope discontinuity | 1 | historical text reported as error; Step 94 |
| `C91-09` | `theta_a` square-root opening | 3 | unverified scientific proposition; Step 94 |
| `C91-10` | gap-weight square-root closure | 5 | unverified scientific proposition; Step 94 |
| `C91-11` | equal weight loss of the two solid-solution terms | 4 | unverified scientific proposition; Step 94 |
| `C91-12` | cancellation of the leading square-root order | 5 | unverified scientific proposition; Step 94 |
| `C91-13` | reported invariant ratio `5.90` over `1e-3..1e-5` | 6 | unverified numerical self-report; Step 94 |
| `C91-14` | response difference is `O(epsilon)` | 9 | unverified scientific proposition; Step 94 |
| `C91-15` | finite threshold derivative with respect to Omega | 5 | unverified scientific proposition; Step 94 |
| `C91-16` | C1 and equal one-sided slopes | 5 | undecided pending limits and both derivatives; Step 94 |
| `C91-17` | area error `7.8e-16`, rounded to `8e-16` | 6 | unverified numerical self-report; Step 94 |
| `C91-18` | exactly zero subcritical gap weight | 6 | unverified numerical self-report; Step 94 |
| `C91-19` | U9 raw differences `5.764e-2/5.698e-3/5.488e-4` | 2 | unverified numerical self-report; Step 94 |
| `C91-20` | U9 normalized ratios `57.6/57.0/54.9` | 3 | unverified numerical self-report; Step 94 |
| `C91-21` | square-root gap scaling was transferred to the full curve | 7 | unverified causal self-report; Step 94 |
| `C91-22` | numbers were generated but not read through | 4 | unverified workflow retrospective; Step 91 record |
| `C91-23` | Codex `11f9054` reportedly merged Claude `3b5fd05` | 5 | unverified pending Step 92 topology |
| `C91-24` | Phase 054 script reportedly recalculated the equation independently | 3 | unverified pending Step 92/94 |
| `C91-25` | source authors identified the threshold derivative-divergence footnote as wrong | 10 | correction statement verified, science unverified; Step 94 |
| `C91-26` | Claude recorded full acceptance of the Codex finding | 4 | acceptance text verified; Step 91 |
| `C91-27` | first commit says the TeX footnote was corrected | 7 | path change verified, meaning unadjudicated; Step 91/94 |
| `C91-28` | first commit says archive U13 was added | 3 | record exists, content unadjudicated; Step 91/94 |
| `C91-29` | first commit reports `STRUCTURE_CHECK PASS` | 1 | unverified build self-report; Step 96 |
| `C91-30` | handover history labels `3b5fd05` as final rewrite | 1 | unverified history row; Step 92 |
| `C91-31` | handover history labels `2802395` as U13 correction | 1 | row exists, science unadjudicated; Step 91/94 |
| `C91-32` | Codex reportedly produced four documents and three probes | 2 | unverified pending Step 92 |
| `C91-33` | only the regular-solution crosscheck was reportedly reviewed | 2 | unverified review status; Step 92 |
| `C91-34` | that crosscheck reportedly triggered U13 | 1 | unverified causal self-report; Step 92/94 |
| `C91-35` | Phase 054 addendum was marked unreviewed | 1 | unverified review status; Step 92 |
| `C91-36` | alignment matrix was marked unreviewed | 1 | unverified review status; Step 92 |
| `C91-37` | alignment matrix may answer gallery-to-staging P1 | 3 | unverified hypothesis; Step 92 |
| `C91-38` | correction handover was marked unreviewed | 1 | unverified review status; Step 92 |
| `C91-39` | ledger, probes, and manifest were marked unreviewed | 1 | unverified review status; Step 92 |
| `C91-40` | package, manuscript, and PDF totaling 26,385 lines were marked unreviewed | 1 | unverified review status; Step 92 |
| `C91-41` | defective-baseline concern was reported resolved | 2 | unverified issue status; Step 92 |
| `C91-42` | handover mismatch was reported resolved | 2 | unverified issue status; Step 92 |
| `C91-43` | missing equation crosscheck was reported resolved | 2 | unverified issue status; Step 92/94 |
| `C91-44` | conformance name was assessed as hiding work scale and unresolved | 2 | unverified governance assessment; Step 95 |
| `C91-45` | workflow rule requires an explicit scaling-ratio table | 2 | rule text verified; Steps 94–97 |
| `C91-46` | all listed legacy gates were reported GREEN | 1 | unverified build self-report; Step 96 |
| `C91-47` | handover reports `STRUCTURE_CHECK PASS` | 1 | unverified build self-report; Step 96 |
| `C91-48` | handover reports three of three numerical checks | 1 | unverified numerical self-report; Step 94 |
| `C91-49` | handover reports temperature-dependence magnitude `0.5252` | 1 | unverified numerical self-report; Step 93 |
| `C91-50` | handover reports zero NaN/Inf | 1 | unverified build self-report; Step 96 |
| `C91-51` | XeLaTeX three-pass build was not run | 1 | open build requirement; Step 96 |
| `C91-52` | handover contains a six-position next-work queue | 1 | queue text exists but is not current authority |
| `C91-53` | handover locates current Codex branch at `11f9054` | 1 | unverified pending Step 92 |
| `C91-54` | handover scopes the older Codex scientific audit to v1.0.10–23 and locates its branch | 1 | unverified scope/location; Step 95 |
| `C91-55` | second commit says the queue was reordered with P0 first | 3 | path changed; content routed |
| `C91-56` | header still routes only U1–U12 while U13 exists | 2 | verified textual routing mismatch; Step 97 |
| `C91-57` | corrected equation remains theory-layer, not adopted post-v1.0.25 | 1 | status text exists; Step 95 |
| `C91-58` | Codex-output review was classified P0/highest/blocking | 2 | priority text exists but current plan supersedes it |
| `C91-59` | P1 lost its former highest-priority label after P0 insertion | 3 | textual priority change verified; current plan supersedes it |
| `C91-60` | the lengthened U13 footnote requires layout recheck | 1 | open build requirement; Step 96 |

The seven rows `C91-46..C91-51` and `C91-57` are explicitly retained as
unchanged context needed to interpret the changed handover/TeX claims; they are
not counted as independent evidence that the two-commit delta newly established
those facts.

| Claim | Atomic proposition | Pointer count | Truth status / owner |
|---|---|---:|---|
| `C91-61` | prior area self-check reported `1e-4` on a finite-window/coarse-grid basis | 4 | unverified numerical self-report; Step 94 |
| `C91-62` | authors called `7.8e-16` stricter/higher precision than `1e-4` | 4 | unverified numerical comparison; Step 94 |
| `C91-63` | unread numbers and failure to verify were said to share one root | 4 | unverified workflow retrospective; Step 91 record |
| `C91-64` | workflow rule requires counting all cancellation pairs together | 3 | rule text verified; Steps 94–97 |
| `C91-65` | workflow rule requires reading produced outputs through to the end | 2 | rule text verified; Steps 94–97 |
| `C91-66` | Phase 054 addendum was reported as 372 lines | 1 | unverified inventory self-report; Step 92 |
| `C91-67` | four prior findings were said to use baseline `2abf019` | 1 | unverified baseline self-report; Step 92 |
| `C91-68` | area conservation was said to be re-confirmed at higher precision | 2 | unverified numerical self-report; Step 94 |
| `C91-69` | window-integrated area was reported equal to `Q` | 2 | unverified numerical self-report; Step 94 |
| `C91-70` | authors said U9 ratios already displayed linear scaling | 4 | unverified retrospective interpretation; Step 94 |
| `C91-71` | comparison tip `11f9054` was dated `2026-07-27` | 1 | unverified date self-report; Step 92 |
| `C91-72` | baseline `3b5fd05` was said to include U11 and U12 | 2 | unverified baseline self-report; Step 92 |
| `C91-73` | second commit created a P4 correction-history record | 2 | record exists, content unadjudicated; Step 91/94 |
| `C91-74` | branch work was characterized as a parallel physics rewrite with separate manuscript/PDF | 1 | unverified scope assessment; Steps 93/95 |
| `C91-75` | parallel work was said to create an additional hidden lineage | 1 | unverified lineage assessment; Step 95 |
| `C91-76` | lineage disposition was assigned to the user | 1 | pending user decision; Step 95 |
| `C91-77` | P1 thermodynamic-input issue remained labeled unresolved | 2 | textual status comparison verified; current plan supersedes queue |
| `C91-78` | alignment-matrix review was named the next session's first work | 1 | queue text only; current plan supersedes it |
| `C91-79` | queue position 1 requires review of Codex `11f9054` outputs | 1 | queue text only; current plan supersedes it |
| `C91-80` | alignment matrix is first within queue position 1 | 1 | queue text only; current plan supersedes it |
| `C91-81` | Phase 054 addendum follows the matrix | 1 | queue text only; current plan supersedes it |
| `C91-82` | `conformance_model` follows the addendum | 1 | queue text only; current plan supersedes it |
| `C91-83` | queue position 2 requires three-pass XeLaTeX and three PDFs | 1 | queue text only; current plan supersedes it |
| `C91-84` | queue position 3 requires user confirmation of gallery-to-staging assignment | 1 | queue text only; current plan supersedes it |
| `C91-85` | confirmed assignment is followed by populating `dH_rxn`, `dS_rxn`, and `n` | 1 | queue text only; current plan supersedes it |
| `C91-86` | default is then to be restored to 7-skew | 1 | queue text only; current plan supersedes it |
| `C91-87` | a default-path temperature-dependence gate is then to be added | 1 | queue text only; current plan supersedes it |
| `C91-88` | queue position 4 puts P0-4 blend normalization first | 1 | queue text only; current plan supersedes it |
| `C91-89` | P0-2, P0-3, and P0-5 follow P0-4 | 1 | queue text only; current plan supersedes it |
| `C91-90` | queue position 5 requests one Omega model-family qualifier | 1 | queue text only; current plan supersedes it |
| `C91-91` | residual queue includes N7 skew-regular-solution `N=7` | 1 | queue text only; current plan supersedes it |
| `C91-92` | residual queue includes N8 equilibrium-data GITT/pOCV plus hold | 1 | queue text only; current plan supersedes it |
| `C91-93` | residual queue includes N9 bootstrap confidence intervals | 1 | queue text only; current plan supersedes it |
| `C91-94` | residual queue includes C-4 source-journal to M4 resolution | 1 | queue text only; current plan supersedes it |
| `C91-95` | residual queue includes D trap record in Chapter 2 Appendix A | 1 | queue text only; current plan supersedes it |
| `C91-96` | second commit reports appending two history rows | 3 | changed-path action claim; Step 91 closed |
| `C91-97` | second commit reports adding the comparison branch to the location map | 3 | changed-path action claim; Step 92 |
| `C91-98` | zero subcritical gap was said to be re-confirmed at higher precision | 2 | unverified numerical self-report; Step 94 |

Eight supplemental source units preserve the complete claim-bearing ranges of
the second commit message and new handover. Each unit maps back to its atomic
claim IDs and carries no independent truth promotion.

The validator catalog executes `131` individually named, data-only negative
controls: strict JSON `12`, Git argv/index ordering `16`, source policy `64`,
human-control structure `10`, and payload/authority contract `29`. Every payload mutation starts from a deep
copy, requires its exact predicate-specific failure, and leaves the pristine
canonical pair byte-identical after the complete suite.

## U13 Disposition

The existence of the old divergence wording and its replacement is verified.
Whether the broadened response is actually (C^1) at
\(\Omega=2RT\), whether both one-sided derivatives exist and agree, and how
the two reported ratio scales map to one normalization are not decided here.
The exact machine disposition is `UNDECIDED_ROUTE_STEP94`.

The distinction is mandatory: an observed finite sampled quotient may refute
one naive divergence interpretation, but does not by itself derive the limit
or prove equality of both one-sided derivatives. Step 94 must independently
derive the expansion and reproduce the numerical normalization before any
scholarly adoption.

## Findings and Ground Not Found

These are source-content findings, not validator-release findings:

| Finding | Severity | Disposition |
|---|:---:|---|
| `F91-P1-01` | P1 | finite sampled difference quotients alone do not establish C1; analytic and numerical Step 94 rederivation required |
| `F91-P1-02` | P1 | the reported `5.90` and `57.x` ratios lack a demonstrated definition/normalization bridge; do not equate them before Step 94 |
| `F91-P2-01` | P2 | handover header still routes `ARCHIVE_NOTE` only through U12 although U13 exists; preserve as stale-pointer evidence |
| `F91-P2-02` | P2 | `STRUCTURE_CHECK PASS` and three-of-three checks lack an execution transcript in the two reviewed commits; retain as self-report |

The handover's counts and assertions that three prior issues are resolved are
ground not found within this Claude-only fork read. Step 92 must inspect the
Codex branch objects before Step 96 adjudicates those statements. The area
values `7.8e-16` and `8e-16` may be rounding-compatible, but the provenance and
calculation remain Step 94 work.

Independent source-read review found no missing commit, edge, blob interval,
or claim-family coverage. Its review of the coverage work was P0/P1=`0/0`.
The P1/P2 entries above remain deliberately open because Step 91 is an audit
record, not a source-repair or scientific-approval step.

## Authority Ceiling

- Git object identity, path/mode/blob topology, exact textual presence, and
  complete-read coverage are established.
- U13 mathematics, numerical precision, material interpretation, primary-
  source authority, implementation correctness, canonical release status,
  and publication readiness are not established.
- scientific truth promotions: 0
- No whole commit is approved for cherry-pick or adoption.
- No `Claude/**`, production source, manuscript, test, PDF, protected ref, or
  `main` object was modified.

## Executed and Deferred Verification

Executed before JSON creation:

1. direct Git merge-base, commit-parent-subject, raw parent-edge, net-tree,
   mode/blob and object-size reconstruction;
2. byte-zero-to-EOF UTF-8 reads of both commit messages and six blobs;
3. dual-runtime in-memory compilation and self-tests for the evidence tools
   (validator `133`, builder `138`, including all `131` named negatives);
4. dual-runtime RED validation with the required JSON missing; and
5. independent read-coverage and claim-routing review.

Deferred until the six non-JSON records are frozen:

1. atomic creation of the two JSON artifacts;
2. dual-runtime content validation and deterministic bytes `2/2`;
3. current-byte independent code/specification review at P0/P1/P2=`0/0/0`;
4. exact-eight staging and dual staged validation;
5. exact-subject commit, push, live-remote equality and clean-tree proof; and
6. dual-runtime persistence validation on the exact child.

## Decision and Next Condition

The selected content decision is bounded to complete Claude-fork reading and
claim extraction. Step 91 remains `PASS_PENDING_PERSISTENCE` with containing
commit `PENDING_AT_PRECOMMIT_BY_DESIGN`. After JSON-last generation, content
and deterministic validation, independent release review, exact staging,
commit and push, both runtimes must return `PASS_P068_STEP91_PERSISTENCE`.
Only then may `Step 92` begin the 5-commit/6-edge/135-event Codex-fork read.

PASS_P068_STEP91_CLAUDE_FORK_READ
