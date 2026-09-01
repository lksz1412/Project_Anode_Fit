# Phase 066 Step 076 — Source, Process and Complete-Read Topology Result

Date: 2026-09-01

Phase: `066`

Cumulative Step: `76`

Status: `PASS_PENDING_PERSISTENCE`

Selected Gate: `PASS_P066_STEP76_SOURCE_PROCESS`

Persistence terminal: `PASS_P066_STEP76_PERSISTENCE`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Expected parent: `f9ee0599ff07d36e4b23547a835549552a51ce26`

Expected subject: `audit(phase066): freeze v1025 source process delta`

## Result Boundary

This result is the human, result-first evidence surface for the frozen
v1.0.25–v1.0.25.2 source/process topology. All three independent reader
batches reported exact coverage; the two deterministic machine artifacts are
collected only after this result and the recovery controls are updated.

The Phase 066 activation checkpoint was committed at
`f9ee0599ff07d36e4b23547a835549552a51ce26`, pushed, fetched, and matched by
local `HEAD`, upstream tracking and live origin. Python 3.12 and 3.14 both
returned `PASS_P066_PLAN_ACTIVATION_PERSISTENCE`. That terminal released Step
76; it did not pre-approve any Step 76 source, read or process claim.

## Exact-Eight Persistence Set

1. `Codex/work/v1025_phase066/build_phase066_step76.py`
2. `Codex/work/v1025_phase066/validate_phase066_step76.py`
3. `Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json`
4. `Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json`
5. `Codex/results/PHASE_066_STEP_076_SOURCE_PROCESS_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected precommit status in that order is `A/A/A/A/A/M/M/M`. No production,
`Claude/**`, protected-branch or `main` path belongs to this checkpoint.

## Frozen Source Denominators

| Measure | Exact value | Current state |
|---|---:|---|
| manifest slice, zero-based | `1087–1519` | machine-reconstructed |
| source path occurrences | `433` | machine-reconstructed |
| per-version occurrences | `143 / 144 / 146` | machine-reconstructed |
| unique Git blobs | `167` | machine-reconstructed |
| occurrence bytes | `26,391,541` | machine-reconstructed |
| unique-blob bytes | `12,483,701` | machine-reconstructed |
| unique UTF-8 text blobs / physical lines | `158 / 30,597` | byte-complete; `157` human `READ_FULL`, one declared generated-runtime exception |
| unique PDFs / pages | `6 / 308` | all pages rendered and visually reviewed |
| unique images | `3` | original-resolution visual review complete |

The authoritative manifest Git blob is LF and its raw/LF SHA-256 is
`60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef`.
A Windows checkout may expose CRLF bytes and a different checkout-only hash;
that checkout transformation is not frozen-source identity and is not used by
the machine artifact.

The occurrence path-set, path-plus-blob and unique-blob SHA-256 values are,
respectively:

- `3c9bf954a5db4df5ce01a96ff8834f9e9284e6e35fdcecbfae0c3ae6b430b382`;
- `b3620bf1a76758cad818e9ea7ece5441ea88b86f8f030bb715f48e054086655c`;
- `f1982cf050f88b7145d5ea1a6afdf124316da1332afec9028ae6119730080bfa`.

Occurrence and unique-blob denominators remain separate. They are never added
and described as a larger source count.

## Pairwise Delta Contract

| Comparison | Shared | Same | Changed | Added | Removed |
|---|---:|---:|---:|---:|---:|
| v1.0.25 → v1.0.25.1 | `143` | `133` | `10` | `1` | `0` |
| v1.0.25.1 → v1.0.25.2 | `144` | `133` | `11` | `2` | `0` |
| v1.0.25 → v1.0.25.2 | `143` | `127` | `16` | `3` | `0` |

Each changed or added occurrence must retain both path-introduction and
first-exact-blob-at-path events. The two events differ for 10 affected
occurrences; a first-ADD shortcut is therefore forbidden.

The three added relative paths are:

- `results/V1025_1_TOUCHUP_NOTE.md`;
- `results/HANDOVER_v1025_2.md`;
- `results/KERNEL_COMPARISON_REPORT_v1025_2.html`.

## Stale PDF Boundary

The following v1.0.25.1/v1.0.25.2 PDF pairs have equal PDF blobs while their
candidate TeX blobs differ:

| PDF | Blob | Pages | v1.0.25.2 build evidence |
|---|---|---:|---|
| `ch1_graphite_v1.0.24.pdf` | `3b5fb27293c95b85436813350db1dcc44d0a695a` | `102` | false |
| `ch2_lco_v1.0.24.pdf` | `ec61067fccd1ebbb677affd449183d68a44af529` | `30` | false |
| `ch3_si_v1.0.24.pdf` | `8a96945c674ae58d83c939edddfb5832dd0543aa` | `22` | false |

Their existence and readability establish inventory and historical rendering
coverage only. They do not prove a v1.0.25.2 build, scientific correctness or
publication readiness.

## Narrative and Routing Denominators

| Surface | Documents | Physical lines | Denominator rule |
|---|---:|---:|---|
| manifest-backed narrative queue | `40` | `9,019` | excludes one 1-line machine-evidence JSON |
| root supplemental controls | `2` | `655` | outside the manifest occurrence set |
| expanded narrative/control surface | `42` | `9,674` | human read required |
| AO–AW/AY routing observations | `10` | `1,919` | separate observation-document denominator |
| underlying documents described by observations | `15` | `3,031` | separate source-document denominator |

AO–AW route exactly `INTENT-PROV-0293–0387` (`95` identities). AY routes
exactly `INTENT-PROV-0395–0404` (`10` identities). The `0388–0394` AX range is
outside this scope. AY is a shared Phase 065 reference: eight identities remain
`OPEN_CARRY`, two remain `BOUNDED_HISTORICAL`, and the number of new Phase 066
AY obligations is zero.

AO–AW canonical owners are not invented at Step 76. Their workflow custodian is
`P066_STEP76`, while the downstream canonical owner remains
`PENDING_STEP81_1` until the disposition unit.

## Process Genealogy

| Partition | Commits | First | Last | Digest |
|---|---:|---|---|---|
| release | `17` | `edbc4a2c68cda0dd21662cb6dd68ba8bed699a76` | `e3e1a634f34b711aa4803fd190fe9120f1755f13` | `f09417ef085ee7139fa11869f6f123937d6492dcc53d1f0b51e71a2c8a124860` |
| routed | `20` | `edbc4a2c68cda0dd21662cb6dd68ba8bed699a76` | `e3e1a634f34b711aa4803fd190fe9120f1755f13` | `57062f623809de1f3fb66b8241117363a0ec18626bc58a40f4f0e41cbed93418` |

The routed-only commits are `db19c8747d24c19bb2fac1a5c7a5a0d0d597f908`,
`878cb16b7c190245f2242f03875ab806dfe8bd93`, and
`ce417e79698487065056d6b71b9f6dd6530f4581`. A contiguous ancestry count is
not the process denominator because it also contains an out-of-scope v1.0.26
A/B commit.

## Human Reader Assignments

### Unique text blobs

| Batch | Reviewer | Blobs | Lines | Membership SHA-256 | Status |
|---|---|---:|---:|---|---|
| `TEXT-1` | `p066_s76_routes` | `50` | `10,203` | `5f5ad117e367d6be18d1f45d7db55de1fe3fc15ff94b3b6fb443bba92662883a` | `COMPLETE_WITH_DECLARED_MACHINE_SEGMENT` |
| `TEXT-2` | `p066_s76_scaffold` | `54` | `10,198` | `aa99071f2ff0fe10e7bc71d56e1c3ddc7d3f49a5bd5a22ec8cf012038ec2ccdc` | `READ_FULL` |
| `TEXT-3` | `p066_s76_manifest` | `54` | `10,196` | `30aead4089fbfdbf4ff1b99c3e8c1fda46fd1b2fb6fe1ecbe8113fbb244899e2` | `READ_FULL` |

The membership rule is deterministic greedy balancing over
`(-physical_lines, blob_sha1)`, assigning each blob to the current minimum
line-sum batch with lower-index tie-break.

### PDF and image review

| Reviewer | PDF pages | Image blobs | Status |
|---|---:|---:|---|
| `p066_s76_routes` | `52` | `1` | `READ_FULL` |
| `p066_s76_scaffold` | `124` | `1` | `READ_FULL` |
| `p066_s76_manifest` | `132` | `1` | `READ_FULL` |

### Process patch review

| Batch | Reviewer | Routed ordinals | Status |
|---|---|---|---|
| `PROCESS-1` | `p066_s76_routes` | `1–7` | `COMPLETE_BY_TRANSITIVE_CONTENT_BINDING` |
| `PROCESS-2` | `p066_s76_scaffold` | `8–14` | `COMPLETE_BY_TRANSITIVE_CONTENT_BINDING` |
| `PROCESS-3` | `p066_s76_manifest` | `15–20` | `READ_FULL` |

`CODE_GUIDE_v24.html` lines 220–3807 are a 3,565,102-byte vendored/minified
Mermaid runtime. It was byte-covered with strict UTF-8, SHA-256, Node syntax
and unsafe-API scans; only lines 1–219 and 3808–3812 were human semantic-read.
The attestation therefore records
`MACHINE_COMPLETE_HUMAN_AUTHORED_READ`, explicitly false for human semantic
reading of the generated segment, rather than overstating `READ_FULL`.

Process batches 1–2 contain copied release trees, binary boundaries and a
vendored minified Mermaid runtime. Coverage is therefore recorded without
pretending that duplicate binary/textconv output was a second human semantic
reading: direct no-textconv semantic patches are combined with the complete
content-addressed source/PDF/image union, and the minified runtime is covered
by strict bytes, hash, syntax and unsafe-API scans. Batch 3 additionally
strict-decodes and visually inspects all embedded PNG payloads. The builder
refuses JSON collection if any declared component is pending, partial, unread,
truncated or has an unresolved inspection error.

## Observed Defects and Non-Promoted Findings

- The v1.0.25 Chapter 1 PDF has one confirmed layout defect: page 50's bottom
  long equation is clipped at the right page boundary. It is historical input,
  not a release PDF, and is routed to the later LaTeX/PDF repair owner.
- `KERNEL_COMPARISON_REPORT_v1025_2.html` contains nine valid embedded PNGs,
  but all nine raster plots show missing Korean title/legend glyphs as square
  placeholders. The surrounding HTML UTF-8 text is intact.
- Blob `d46e5c2d147c8c16b7c1fdde132fc41c71d6a1b1` has a `.json` path but is
  actually the one-line text pointer `snapshot -> ch1_graphite_v1.0.24.tex`.
  The machine record classifies it as `TEXT_POINTER`, not JSON.
- The historical surfaces retain unresolved or superseded statements about
  graphite two-phase counts, regular-solution kernels, dataset protocols and
  default transition sets. Step 76 records them as inputs; it does not promote
  them to scientific or release authority.

## Authority Boundary

- This unit establishes source identity, machine extent, complete-read coverage,
  pairwise delta and process genealogy only.
- It does not reproduce the Direct14 fit; that is Step 77.
- It does not recover original full-precision optimizer state; that is Step 78
  and may remain `GROUND_NOT_FOUND`.
- It does not turn empirical fit components into material phase, gallery or
  species evidence.
- It does not establish external scientific truth, a canonical release, a
  fresh v1.0.25.2 build or publication readiness.
- Ref. 7 original full text remains `GROUND_NOT_FOUND` under
  `PHASE-071-PRIMARY-SOURCE-ACQUISITION`.
- No production or Claude source is modified.

## RED/GREEN Execution Record

The initial validator RED was executed before the builder or machine artifacts
existed:

```text
py -3.12 Codex/work/v1025_phase066/validate_phase066_step76.py --content-only
FAIL_P066_STEP76 E_ARTIFACT_MISSING
exit 1
```

This was the expected missing-artifact failure. After all reader reports were
received, deterministic preview and JSON-last collection completed. The first
dual-runtime content candidate passed but was superseded after independent
review found source-policy, rollback and source-binding weaknesses. It is not
the final precommit evidence.

```text
superseded: semantic=15/15 strict_json=6/6 source_git=25/25
```

The repaired hardening rejects `32/32` source/Git attacks, rejects `6/6`
validator and `6/6` builder JSON attacks, rolls back both outputs after an
injected second-rename failure, binds all 52 provenance records back to Git,
and verifies protected/main live refs. Fresh dual-runtime content and staged
outputs must be taken from the validator execution itself; this result does not
pre-claim an execution that depends on its own staged bytes.

## Files Created or Modified

Created for Step 76:

- `Codex/work/v1025_phase066/build_phase066_step76.py`;
- `Codex/work/v1025_phase066/validate_phase066_step76.py`;
- this result document.

JSON-last artifacts:

- `Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json`;
- `Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json`.

Result-first control updates:

- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`;
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`;
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`.

## Confirmed Decisions

- Frozen source baseline and later process tip remain distinct.
- Manifest raw and LF-normalized identities remain distinct.
- Machine extent and human read coverage remain distinct.
- Filename extension never overrides observed bytes.
- Path introduction and first exact blob at path remain distinct provenance
  events.
- Stale PDFs cannot supply v1.0.25.2 build evidence.
- AO–AW pending ownership is not filled by inference; AY prior ownership is
  reused without creating new obligations.

## Unresolved and Next Condition

Reader coverage is complete and the content Gate is selected. Repaired
dual-runtime content/staged validation, independent P0/P1/P2=`0/0/0`,
exact-eight commit/push and persistence are the remaining checkpoint
operations. Step 77 remains blocked until both runtimes return
`PASS_P066_STEP76_PERSISTENCE`.
