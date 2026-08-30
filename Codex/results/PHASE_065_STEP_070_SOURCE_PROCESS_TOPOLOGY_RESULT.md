# Phase 065 Step 70 Source and Process Topology Result

Date: 2026-08-30
Status: `PASS_PENDING_PERSISTENCE`
Phase plan: `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`
Expected parent: `83323ebfff1c468e4ada5e695ced10c69e24fb32`
Expected subject: `audit(phase065): freeze v1024 source process topology`

## 1. Purpose and Authority Boundary

This result freezes the source, read, process, and derived-artifact topology of
the v1.0.24/v1.0.24.1 lineage before any static, scientific, runtime, or
conformance adjudication. It is an internal provenance and complete-read gate.
It does not establish external scientific, material, experimental, or
publication authority, and it does not treat v1.0.24.1 as independent
corroboration of v1.0.24.

This result was intentionally created before its two machine artifacts. All
human/agent read partitions, deterministic reconstruction, dual-runtime
hardening, and independent pre-collection reviews are now complete. The two
machine artifacts are collected from this final human evidence state under the
JSON-last rule; only commit, push, fetch, and live-remote persistence remain
outside the precommit gate.

## 2. Recovery State

- Active branch: `codex/anode-fit-v1025_2-canonical-completion`.
- Phase 065 activation commit:
  `83323ebfff1c468e4ada5e695ced10c69e24fb32`.
- Activation persistence terminal:
  `PASS_P065_PLAN_ACTIVATION_PERSISTENCE`.
- Frozen Claude baseline:
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- Protected branch pin:
  `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- Main tracking/live pin:
  `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- `Claude/**`, the protected branch, and `main` remain read-only.

The controller directly reread the Phase 065 plan and activation evidence and
recovered both execution ledgers and the active handover. Assigned reviewers
must report exact full-read ranges and unreviewed intervals; their summaries
cannot substitute for the frozen Git objects.

The two governing master plans were also directly read from first line through
EOF during recovery: `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
lines `1–520`, and
`Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md` lines
`1–665`. These ranges are recovery evidence for plan scope only; they do not
substitute for Step 70 corpus evidence.

## 3. Frozen Release Denominator

The Phase 056 manifest indices `826–1086` (zero based), or ordinals
`827–1087` (one based), contain 261 path occurrences. Independent
reconstruction must close the following denominator:

| Measure | Required value |
|---|---:|
| occurrences / unique paths | `261 / 261` |
| v1.0.24 / v1.0.24.1 occurrences | `130 / 131` |
| unique Git blobs | `131` |
| unique text blobs / physical lines | `125 / 21,618` |
| unique PDFs / pages | `3 / 148` |
| unique images | `3` |
| unique / occurrence bytes | `7,812,647 / 15,622,368` |
| shared relative paths with identical blobs | `130 / 130` |
| v1.0.24.1-only paths | `1` (`ARCHIVE_NOTE.md`) |

The frozen path-set SHA-256 is
`815f37a830da3e5d6539d53bf6dc24c35dec012f39241818b070154b7b729aa7`,
the path-plus-blob SHA-256 is
`35c224df31807c02ab7d0f8ace3aad7edb36369b6d4d2dd97895589dd5624c0d`,
and the unique-blob-set SHA-256 is
`0cc9e04e676dd9c5024842eeaf57180b515bbe2bb7d068dc7aa8eb10c83c8cdd`.

## 4. Activation-Denominator Correction

The activation plan copied a provisional narrative partition of
`29 documents / 2,068 lines` and a corresponding narrative total of
`74 / 7,232`. Step 70 cannot reproduce the line count from the frozen
baseline and therefore does not attest it.

The exact reproducible 29-document path rule is:

1. all 23 Markdown records below `Claude/docs/v1.0.24/results/**`;
2. `Claude/docs/v1.0.24/CODE_GUIDE_v24.md`;
3. `Claude/docs/v1.0.24/FITTING_GUIDE.md`;
4. `Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md`;
5. the three named root V1024 ledger/summary anchors.

Those exact frozen objects contain `2,306` physical lines, not `2,068`.
Accordingly the reproducible narrative universe is `74 documents / 7,470
lines`: three plans (`639`), the corrected 29-document release/root process
partition (`2,306`), 31 `comp_v24` Markdown records (`2,635`), and 11 Phase
057 routing records (`1,890`). The count is unchanged; only the stale line
extent is corrected by `+238`. The machine artifacts must preserve both the
copied claim and the independently reconstructed value so downstream work
cannot silently reuse the stale denominator.

## 5. Complete-Read Partitions

### 5.1 Unique release blobs

The 125 text blobs were partitioned by observed file type. Independent reader
reports cover 118 scientific/document blobs/18,737 physical lines and seven
Python blobs/2,881 lines from baseline Git objects. Those reports do not become
`AGENT_FULL_READ` topology state merely because the builder can reconstruct the
same byte extents. The final evidence block now binds each exact
blob/range/hash group to one reader, and the controller accepts the union with
no missing or duplicate assignments; those groups therefore carry
`AGENT_FULL_READ` state in the collected topology.

The 3,812-line HTML guide received a byte-complete structural review. Authored
content is lines 1–219 and 3808–3812; the minified third-party Mermaid payload
is lines 220–3807. Only that exact interval is recorded as
`SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL`, not as a whole-group read status and
not as a claim that every vendor token was semantically interpreted. The
scientific/document group itself still requires `DIRECT_READ` or
`AGENT_FULL_READ`. This interval is routed to Step 74 and is not an unbound byte
interval. The `.json`-suffixed snapshot was read as its actual one-line
plain-text pointer.

All mirror occurrences reuse the verified unique-blob read while retaining
both occurrence identities. No mirror occurrence is counted as a second read
or a second authority source.

### 5.2 Supplemental process records

All six named baseline records were read from line 1 through the final line:
three plans/639 lines and three ledger/summary anchors/89 lines, total
`6 / 728`. They remain a process-evidence denominator separate from the 261
release occurrences even where the narrative topology references them.

### 5.3 Narrative and `comp_v24` evidence

The corrected narrative denominator is machine-reconstructed as three
plans/639, 29 release/root process records/2,306, 31 `comp_v24` Markdown
records/2,635, and 11 Phase 057 routing records/1,890: `74 / 7,470`.
Reader coverage is bound in the final evidence block, and the exact group union
contains no gaps or duplicate assignments.

The narrative auditor identified a reproducibility defect in the draft
controller: all 11 Phase 057 plan/observation documents were being read from
the mutable checkout. The builder now reads them only as Git blobs at the
frozen expected parent
`83323ebfff1c468e4ada5e695ced10c69e24fb32`, persists source ref, blob ID,
raw/LF hashes, byte and line extents, and exact ranges, and uses the same frozen
bytes for observation-heading extraction. The validator independently
recomputes those records from the expected-parent objects and contains named
CRLF-checkout substitution, byte-mutation, and source-ref mutation probes.

The remaining `comp_v24` evidence is not deferred out of Step 70. Python
`29 / 2,932`, JSON `16 / 1,650`, CSV `10 / 45,203`, TXT `7 / 171`, and PNG
`33` form five mandatory Step 70 evidence groups. Their exact paths, blobs,
ranges, raw/LF hashes, byte extents, and original-resolution image metadata are
machine-derived from the baseline. Independent full-read/visual reports are
integrated in the final evidence block, including exact report hashes and the
five mandatory group assignments.

### 5.4 PDF and image inspection

All three unique PDFs were materialized from exact Git blobs, inspected with
PDF metadata, extracted page by page, rendered with Poppler, and visually
reviewed page by page: graphite `97`, LCO `30`, and Si/blend `21`, total
`148/148`. No blank page, cutoff, overflow, missing figure, or unreadable layout
was observed. The Si PDF's page 7 text extraction contains two replacement
glyphs where the rendered common-chemical-potential symbol is visually intact;
this is recorded as an extraction limitation, not a missing visible equation.

All three unique PNGs were inspected at original pixels: `2070×1150 RGBA`,
`2160×624 RGBA`, and `2040×600 RGBA`. The first two were additionally inspected
as unscaled crops to avoid preview downscaling. No clipping, legend collision,
or unreadable panel was observed. Visual inspection establishes presentation
coverage only; it does not validate fitted physics or material identity.

## 6. Process Topology

Git reproduces both denominators:

- 38 commits touching the two release trees, from
  `04ebc0cf8b36d34f776ddbc2b356ca0246983fe8` through
  `2147abfac3fb6c82279aefb2b21c749a521112dc`;
- 98 commits in the routed release/plan/root-anchor/`comp_v24` union.

All 98 routed commits are single-parent commits. Machine reconstruction of their
routed-scope parent patches totals `12,505,904` bytes and `106,801`
LF-normalized lines. The canonical human-review partitions are ordinals
`1–33` (`455,844 / 7,878`), `34–66` (`2,655,327 / 66,770`), and `67–98`
(`9,394,733 / 32,153`) in bytes/lines. Their canonical row bindings are,
respectively, `5e22f38eddbfafa1a19a0a293c2b36780b8b59fc285dc0ce1ddc824878348076`,
`a06de2b79da8acdcd8ca1cfb017e1f4e8177706f7f2a90cbd7747debd4ac748e`,
and `e080af1a80e9907bf53872f5595a61266b0ffc6d7ff557fe51178dfe3f5869ca`;
the all-98 binding is
`5c8ff3bc6f9f3570c024c603d363a7663210335ff950f5f279cf4e2fc5240ac2`.
These use canonical JSON rows with `ordinal`, `commit`, `parents`,
`sha256_raw`, `bytes`, and `lines`. Earlier reviewer-local manifest hashes used
different schemas and are not interchangeable with these bindings.

The topology schema separates full-commit changed paths from routed changed
paths and supplements every routed PDF/PNG change with exact old/new Git blob
identity, byte length, raw SHA-256, and page count or image dimensions. Encoded
binary payload is not treated as human-readable patch prose. Human patch-read
status and per-ordinal classification acceptance are integrated in the final
evidence block: all 98 ordinals are reviewed, with no unread or failed row.

Only the exact minified patch intervals at routed ordinal 70 lines `226–3813`
and ordinal 98 lines `2012–5599` may carry
`SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL`. Their commit, parent, full patch
identity, line range, interval byte extent, and LF SHA-256 are machine-derived
and validator-recomputed. No process partition as a whole may use a structural
status in place of human review.

For every selected commit, Step 70 records parents, subject, full-commit
no-rename changed-path status with old/new blob identity, and the complete
routed-scope parent-patch hash/extent. The 38-release-commit subset has its own
two-release-directory patch projection (`10,872,687` bytes/`50,787` lines) and
cannot inherit the routed totals by subtraction.

The routed provisional classes partition all 98 commits exactly once:
proposal 7, competition 4, review 31, patch 21, build 6, feedback revision 21,
archive 1, and status/self-report 7. These are provenance-routing labels only.
They do not prove adoption, runtime behavior, or scientific correctness.

## 7. TeX and Derived-Artifact Topology

The comment-aware parse covers 90 unique TeX blobs/12,707 lines, 55 resolved
`input`/`include`/`subfile` edges, zero unresolved include edges, and four
separate `externaldocument` cross-reference edges. The cross-reference edges
form a build-order dependency and are not counted as source-inclusion edges.

The adopted closures are graphite `34 files / 5,625 lines`, LCO
`13 / 1,618`, and Si/blend `11 / 1,143`; their union is
`56 unique TeX files / 8,218 lines`. The remaining `34 / 4,489` are competition
drafts, refine-b drafts, the phase-separation appendix, the orphan Si appendix,
and legacy preambles.

The three PDFs bind to their three masters and closures. Source comments and
PDF metadata support a XeLaTeX/dvipdfmx route, but no exact build command was
found. The HTML declares its Markdown source and co-changed with it, while the
exact generator/helper remains `GROUND_NOT_FOUND`. The three PNGs bind to the
two historical helper scripts and exact save locations; their absolute source
paths make the producers nonportable, and no frozen helper was executed.

## 8. Preliminary Findings

- `P065-S70-F01`: v1.0.24.1 is a 130-blob mirror plus one archive note; it is
  not a second scientific corpus.
- `P065-S70-F02`: the `.json`-suffixed snapshot is a 37-byte plain-text pointer
  and must be classified from bytes, not extension.
- `P065-S70-F03`: the activation narrative line total is stale. The frozen
  exact 29-path rule yields 2,306 lines and the full 74-record narrative set
  yields 7,470 lines.
- `P065-S70-F04`: 38 release-tree commits are a strict subset of the
  98-commit routed process universe; neither count may substitute for the
  other.
- `P065-S70-F05`: generated PDF/HTML/image existence is derived-artifact
  evidence only and cannot overrule source, runtime, or primary literature.
- `P065-S70-F06` (`P1`, routed Steps 72/74/75): the Si text combines a width
  law `w=n_jRT/F` with an Ω-dependent regular-solution peak, but the boxed
  direct kernel retains the `n=1` entropy coefficient. It does not derive the
  generalized denominator or corresponding critical threshold.
- `P065-S70-F07` (`P1`, routed Steps 72/75): internally fitted finite Si widths
  are called direct single-phase evidence. Width alone cannot exclude kinetics,
  heterogeneity, overlap, or instrumental convolution, so the claim ceiling is
  internal diagnostic pending independent phase authority.
- `P065-S70-F08` (`P1`, routed Steps 71/72/74): the reflect seed table says the
  regular-solution branch applies in equilibrium and derivative paths, while
  the final code guide says derivative/entropy/solver paths ignore it. Step 70
  preserves the contradiction; prose cannot decide runtime behavior.
- `P065-S70-F09` (`P1`, preserved open authority): the seed table calls Refs. 6
  and 7 complete, but the source itself requests an original comparison and
  Phase 064 has Ref. 7 original `GROUND_NOT_FOUND`. The completion self-claim
  is rejected as authority.
- `P065-S70-F10` (`P2`, routed Step 74): generated HTML table rows at physical
  lines 142, 166, and 214 have extra cells because literal `|I|` was parsed as
  delimiters. The readable Markdown source is not modified here.
- `P065-S70-F11` (`P2`): the exact HTML generator command is
  `GROUND_NOT_FOUND`; co-change and source declaration do not justify inventing
  a command.
- `P065-S70-F12` (`P1`, routed Steps 72/73/75): the advertised 2 mA-to-5 mA
  transfer validation independently fits `(R_n,k)` at both currents. It is not
  a held-out cross-rate prediction and cannot support transfer predictivity.
- `P065-S70-F13` (`P1`, routed Steps 72/75): the claim that fitted
  `Omega>2RT` independently confirms two-phase behavior is constrained by an
  optimizer lower bound of `2.02RT`; one result lies exactly on that bound.
  This is a constraint-induced/tautological result, not independent phase
  evidence. Moreover `Omega=2RT` is the regular-solution critical point, not a
  finite miscibility gap; the latter requires the strict supercritical regime.
- `P065-S70-F14` (`P1`, routed Steps 72/74/75): early summary/synthesis records
  call an analytic Marquis/Doyle-Garcia curve the first real LCO fit, while the
  same lineage later admits that no LCO-specific measured raw data were
  available. The later correction cannot be back-projected, and the stale
  headline cannot remain current ground truth.
- `P065-S70-F15` (`P1`, routed Steps 72/75): the anode ablation reuses the same
  cell's fitted baseline positions as supposed physical anchors, so zero loss
  is in-sample reuse. A lower in-sample fit under simultaneously changed seeds,
  bounds, and model is also insufficient to diagnose overfitting, which
  requires held-out degradation.
- `P065-S70-F16` (`P1`, routed Steps 72/75): a width-only Si solid-solution
  decision contradicts the same lineage's explicit statement that derivative
  peak width alone cannot distinguish solid solution from two-phase behavior
  without structural evidence such as X-ray diffraction.
- `P065-S70-F17` (`P1`, routed Steps 72/75): the conclusion that low fit quality
  is proven to be a data-quality problem compares different chemistries and
  acquisition routes without matched downsampling/noise injection, a
  measurement-error model, or held-out analysis. The residual cause is
  confounded.
- `P065-S70-F18` (`P2`, routed Steps 72/75): a shared in-sample fit on two cells
  of one material is a two-cell consistency demonstration, not industrial
  generality or no-refit production usability; independently resampled
  derivative residuals also ignore correlation.
- `P065-S70-F19` (`P1`, routed Steps 71/72/75): the temperature-split example inserts
  the literature entropy slope, merger temperature, and width and then
  reproduces those targets. It is a calibrated physical-seed demonstration,
  not an independent prediction. The fit uses cell 1 only, converts non-finite
  values with `nan_to_num(..., nan=0)`, and reports no cell-2 prediction or
  held-out score.
- `P065-S70-F20` (`P2`, routed Step 72): two cited DOI identities have conflicting
  article numbers within the archive. Primary metadata resolution is required
  before citation export.
- `P065-S70-F21` (`P2`, process boundary): routed ordinal 32 adds only a test
  script and no result, JSON, or status artifact. Script existence is not
  experiment completion.
- `P065-S70-F22` (`P2`, routed Steps 71/73/75): the lineage acknowledges the
  seconds/hour mismatch and an approximately 20 kJ/mol shift in interpreted
  activation enthalpy but calls silent bugs zero because curve shape can absorb
  it. Absorbability does not preserve physical parameter interpretation; this
  remains a unit/interpretation defect.
- `P065-S70-F23` (`P1`, routed Steps 72/75): commit `ad2061` introduces six
  numerical seeds without a closed bibliography/DOI/table-or-page route. They
  remain internal inputs, not literature-established material constants.
- `P065-S70-F24` (`P1`, preserved authority blocker): a later internal record
  promotes Ref. 7 to complete authority despite the direct Phase 064
  `GROUND_NOT_FOUND` state. The promotion is rejected; acquisition remains the
  Phase 071 owner.
- `P065-S70-F25` (`P1`, routed Steps 71/72/73): the reflect check accepts
  `npk>=1` while reporting a “single peak” result and does not test the
  `Omega -> 0` equivalence of the regular-solution and logistic routes. The
  printed pass is therefore weaker than its wording.
- `P065-S70-F26` (`P2`, process authority): internal labels such as `BUG0` and
  `MERGE-READY` are status/self-report evidence only and cannot establish
  external correctness, adoption, or scientific validity.
- `P065-S70-F27` (`P1`, routed Steps 72/73/75): the G-E3 “truth” comparison uses
  a fixed-point result produced by the same implementation family. It is an
  internal self-consistency oracle, not independent physics truth.
- `P065-S70-F28` (`P1`, routed Steps 72/75): the `consistency2` route selects
  the nearest fitted peak within a ±20 mV window around the expected target.
  That target-conditioned selection is circular and cannot independently
  validate the peak assignment.
- `P065-S70-F29` (`P1`, routed Steps 72/75): an in-sample O2-LCO fit is used to
  support an O3 model and an absence-cause claim. Neither the polymorph change
  nor the causal absence statement is established by that reused fit.
- `P065-S70-F30` (`P1`, routed Steps 72/75): the denoising comparison changes
  the target while comparing scores, and the reported delta-R² does not support
  the stated improvement. It is not held-out evidence for denoising quality.
- `P065-S70-F31` (`P1`, routed Steps 72/75): the differential-voltage curve is
  obtained by taking the reciprocal of the same fitted derivative curve. It is
  a deterministic re-expression, not independent validation.
- `P065-S70-F32` (`P1`, routed Steps 72/75): free/blend peaks are assigned to a
  material component without an identified component model or a closed
  mass-capacity basis. Peak flexibility alone does not establish material
  identity or fraction.
- `P065-S70-F33` (`P1`, routed Steps 71/72/75): the rate-broadening script fits
  peak position versus rate, not full width at half maximum versus current.
  Its output therefore cannot support the advertised broadening law.
- `P065-S70-F34` (`P1`, routed Steps 71/73/74/75): the LCO R3 toggle is described
  as default OFF in one release surface while the corresponding source defaults
  it to true. Static and runtime adjudication must resolve the conflict.
- `P065-S70-F35` (`P2`, routed Steps 71/72/74): the graphite first-look path
  labels capacity as mAh and later multiplies it by 1,000 while retaining that
  label. The displayed capacity unit is not closed.
- `P065-S70-F36` (`P2`, routed Steps 71/72/74): one report emits Ω divided by a
  current expressed in mA without a coherent derived unit. That output must not
  be interpreted as a material parameter.
- `P065-S70-F37` (`P2`, routed Steps 71/73/75): optional smoothing/filter paths
  can silently fall back or replace failed/non-finite output. The fallback state
  is not surfaced as an explicit result classification.
- `P065-S70-F38` (`P2`, routed Steps 71/72/75): the asymmetric-peak form is not
  normalized and its precise Zhu source route is unresolved. Area/capacity
  interpretations remain unverified.
- `P065-S70-F39` (`P2`, routed Steps 71/73/74): historical helper scripts contain
  hard-coded absolute paths. They are provenance evidence, not portable
  reproduction commands.
- `P065-S70-F40` (`P2`, routed Steps 71/73/75): LCO composition grids contain
  duplicate/reversed coordinates, so code that assumes strict monotonicity is
  unsafe without an explicit normalization rule.
- `P065-S70-F41` (`P2`, routed Steps 72/74): original-resolution review found
  missing-glyph boxes in 17 `comp_v24` PNGs. The affected filenames are bound in
  the visual audit and require regeneration with a verified font stack.
- `P065-S70-F42` (`P2`, routed Steps 72/74): `gr_dva_Mremoval.png` clips curves,
  `lco_phase.png` exposes a NumPy scalar representation in its legend, and
  `param_distributions.png`/`quality_vs_r2.png` contain label overlap.
- `P065-S70-F43` (`P2`, routed Steps 74/75): the shared fitting guide still
  identifies itself as v1.0.20 inside the v1.0.24 release surface. It is stale
  release metadata, not a current-version authority statement.
- `P065-S70-F44` (`P2`, routed Step 74): two Markdown records lack a final LF.
  This does not alter scientific content but remains an exact-output
  conformance defect.

An early patch-screening hypothesis that a `seed=None` line made a synthetic
check nondeterministic was withdrawn after the complete patch showed that the
perturbation uses a deterministic modular sequence and performs no random
draw. It is not retained as a finding.

## 9. Human Full-Read Evidence

The assigned readers returned complete path/blob/range/page reports. The
controller reconciled all 15 mandatory evidence groups with no duplicate
assignment, unreviewed interval, or unresolved output truncation. The following
strict JSON block is the human-evidence authority surface consumed by the
builder:

BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON
```json
{
  "schema_version": "P065-S70-HUMAN-EVIDENCE-1",
  "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
  "bindings": {
    "comp_v24_csv": {
      "binding_sha256": "e03ed796997d371b96047ae1bc2c98dc3cbbd6a10f2b089181790ae2a1fa2ec7",
      "group_id": "comp_v24_csv",
      "kind": "FULL_TEXT_NUMERIC_DATA",
      "record_count": 10,
      "record_manifest_sha256": "ecede214d5dc119999d0acfd972a6a4db76d3d4eb5ca8565bb26fa24806f6064",
      "summary": {
        "files": 10,
        "lines": 45203
      }
    },
    "comp_v24_json": {
      "binding_sha256": "ce6466235a412b1c6e65c583f56da3a72e93595b7ed8ddfbcf0b9488cc4705fc",
      "group_id": "comp_v24_json",
      "kind": "FULL_TEXT_STRICT_JSON",
      "record_count": 16,
      "record_manifest_sha256": "896fdb65d1527a289e1aa553961f85bb93ec7de3f592559a901cc6d31568ba53",
      "summary": {
        "files": 16,
        "lines": 1650
      }
    },
    "comp_v24_png": {
      "binding_sha256": "27137436c03b370f698dcc65822f4eae273bc06aca482247e0edc517689c1435",
      "group_id": "comp_v24_png",
      "kind": "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL",
      "record_count": 33,
      "record_manifest_sha256": "863cdcbc7d460c572f057ef9f27ec70a30ad0ba78b22a8d417c16a4042ba85bd",
      "summary": {
        "files": 33,
        "images": 33
      }
    },
    "comp_v24_python": {
      "binding_sha256": "46bbdb55eeb6a2f03cb20d8b469c0eb8368083c0b80ddce22c5e2c1f659d572a",
      "group_id": "comp_v24_python",
      "kind": "FULL_TEXT_AST_NO_IMPORT",
      "record_count": 29,
      "record_manifest_sha256": "204a68df82fe7303cf3b52a016dd15ddad9e96528bca0dd6ede318dcad096215",
      "summary": {
        "files": 29,
        "lines": 2932
      }
    },
    "comp_v24_txt": {
      "binding_sha256": "16c1c04f9cff49dabb0c009f0f6adeb1f154000e6fededbef5897854320daac2",
      "group_id": "comp_v24_txt",
      "kind": "FULL_TEXT",
      "record_count": 7,
      "record_manifest_sha256": "178d629595481e2cf4936591f9fcba890b41eae36409be28a08f50ceeb1d23fc",
      "summary": {
        "files": 7,
        "lines": 171
      }
    },
    "narrative_history": {
      "binding_sha256": "6e52620222da97ea8a793ecdf757f6e9018a85ced1d9cbec89af2826c721db5a",
      "group_id": "narrative_history",
      "kind": "FULL_TEXT",
      "record_count": 74,
      "record_manifest_sha256": "8072fd05fed9548aa539c56092140943222743e6bc858f4a1d23500f37f3eb6e",
      "summary": {
        "documents": 74,
        "lines": 7470
      }
    },
    "release_code_test_text": {
      "binding_sha256": "1c85b6dcabc12122dda239761d94033617607e3f3e0fd42cfeee53be5dcc25e1",
      "group_id": "release_code_test_text",
      "kind": "FULL_TEXT_AST_NO_IMPORT",
      "record_count": 7,
      "record_manifest_sha256": "a63bc0c6c286eb7d25fe3769c16fc7fd9e120c9f2e8b2fd2857fa4b10c230acf",
      "summary": {
        "blobs": 7,
        "lines": 2881
      }
    },
    "release_image": {
      "binding_sha256": "9d33018bbcf6eaaa80047f8a7d7633a56e681b8913d2e4079567ab36f34e8eb9",
      "group_id": "release_image",
      "kind": "FULL_IMAGE_ORIGINAL_RESOLUTION_VISUAL",
      "record_count": 3,
      "record_manifest_sha256": "ce1b44c3abca0e227bf3c0ea0cb2217c205ed644fe7b801e6410178281d2c9ea",
      "summary": {
        "images": 3
      }
    },
    "release_pdf": {
      "binding_sha256": "746756744e7df1671f4eb72a75464628ff2a3144849db86c2be12561d3838cde",
      "group_id": "release_pdf",
      "kind": "FULL_PDF_EXTRACT_RENDER_VISUAL",
      "record_count": 3,
      "record_manifest_sha256": "b216aa128227d9c74cf5d76307cde3825341849ba809afbfe10451b99ab1206c",
      "summary": {
        "documents": 3,
        "pages": 148
      }
    },
    "release_process_all_038": {
      "binding_sha256": "ae5e548e382fb14b1e8cbdb04c241b19955e07dbd312fd810ad5258560d1fb3d",
      "group_id": "release_process_all_038",
      "kind": "FULL_PATCH",
      "record_count": 38,
      "record_manifest_sha256": "d9a3726b18a708896d728a088fb16e9f44fe873819ea337fca3318d0fc2d477b",
      "summary": {
        "canonical_row_binding_sha256": "50a8ab7df16e06b39ef67cfa8d83876ea7effa12ff81c4bda8369830ab8324ba",
        "commits": 38,
        "patch_bytes": 10872687,
        "patch_lines": 50787,
        "reviewed_record_schema": "subject-paths-binary-classification-patch-v1"
      }
    },
    "release_scientific_document_text": {
      "binding_sha256": "e85898e4d6425581e738934a3fba19aca265e17ebeadaa8271949eda6b341a98",
      "group_id": "release_scientific_document_text",
      "kind": "FULL_TEXT",
      "record_count": 118,
      "record_manifest_sha256": "69520a33892446b0c5a5038b71535cd2849575d4b12284452726f9229c5de1ab",
      "summary": {
        "blobs": 118,
        "lines": 18737,
        "semantic_deferred_intervals": [
          {
            "blob": "3fa2ea6ea6889e0d0d095dcc6c1ee3b9500dee6a",
            "full_bytes": 3594138,
            "full_lines": 3812,
            "full_sha256_lf": "c795a947a44b31eb4d0039e67d067a96d51d807e9a3de9fda799534180908aa1",
            "full_sha256_raw": "c795a947a44b31eb4d0039e67d067a96d51d807e9a3de9fda799534180908aa1",
            "group_id": "release_scientific_document_text",
            "interval_bytes_lf": 3565120,
            "interval_id": "release-code-guide-html-mermaid-lines-220-3807",
            "interval_lines": 3588,
            "interval_sha256_lf": "ed349941137ddb8155918d9a975c3a0f316d6080fad27652a7e8a2de8de31238",
            "line_range": [
              220,
              3807
            ],
            "path": "Claude/docs/v1.0.24/CODE_GUIDE_v24.html",
            "source_ref": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
            "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
            "subject_type": "GIT_BLOB_TEXT_INTERVAL"
          }
        ]
      }
    },
    "routed_process_ordinals_001_033": {
      "binding_sha256": "6c228cc9e1f0c7babdd847d4b22ad4cef027749b6df038ef3db4e3cded29a2f9",
      "group_id": "routed_process_ordinals_001_033",
      "kind": "FULL_PATCH",
      "record_count": 33,
      "record_manifest_sha256": "662905ea4b1068d525900ad909ed6ea18e912b427d9083e0251683f7635c3648",
      "summary": {
        "all_98_canonical_row_binding_sha256": "5c8ff3bc6f9f3570c024c603d363a7663210335ff950f5f279cf4e2fc5240ac2",
        "canonical_row_binding_sha256": "5e22f38eddbfafa1a19a0a293c2b36780b8b59fc285dc0ce1ddc824878348076",
        "commits": 33,
        "ordinals": [
          1,
          33
        ],
        "patch_bytes": 455844,
        "patch_lines": 7878,
        "reviewed_record_schema": "subject-paths-binary-classification-patch-v1",
        "semantic_deferred_intervals": []
      }
    },
    "routed_process_ordinals_034_066": {
      "binding_sha256": "87ffa75d74131868900657dcaeb5d16e75c5e0da637180e67228e3e7356c0640",
      "group_id": "routed_process_ordinals_034_066",
      "kind": "FULL_PATCH",
      "record_count": 33,
      "record_manifest_sha256": "df62b8210b15c82faf5cfa9475f7ff909242f6f31ae50131558c4efea1713ef6",
      "summary": {
        "all_98_canonical_row_binding_sha256": "5c8ff3bc6f9f3570c024c603d363a7663210335ff950f5f279cf4e2fc5240ac2",
        "canonical_row_binding_sha256": "a06de2b79da8acdcd8ca1cfb017e1f4e8177706f7f2a90cbd7747debd4ac748e",
        "commits": 33,
        "ordinals": [
          34,
          66
        ],
        "patch_bytes": 2655327,
        "patch_lines": 66770,
        "reviewed_record_schema": "subject-paths-binary-classification-patch-v1",
        "semantic_deferred_intervals": []
      }
    },
    "routed_process_ordinals_067_098": {
      "binding_sha256": "0a2af66967d7d51d800e40d05e2507dd526d71837f2131a0eb8e231dc838a74d",
      "group_id": "routed_process_ordinals_067_098",
      "kind": "FULL_PATCH",
      "record_count": 32,
      "record_manifest_sha256": "43e59f101eb2ec352277049b62e46b8a02917af637d57a38ba1b98417ebacbb4",
      "summary": {
        "all_98_canonical_row_binding_sha256": "5c8ff3bc6f9f3570c024c603d363a7663210335ff950f5f279cf4e2fc5240ac2",
        "canonical_row_binding_sha256": "e080af1a80e9907bf53872f5595a61266b0ffc6d7ff557fe51178dfe3f5869ca",
        "commits": 32,
        "ordinals": [
          67,
          98
        ],
        "patch_bytes": 9394733,
        "patch_lines": 32153,
        "reviewed_record_schema": "subject-paths-binary-classification-patch-v1",
        "semantic_deferred_intervals": [
          {
            "commit": "1ee23c53fec14c41a1f5372a19e6b2f70adb0de0",
            "group_id": "routed_process_ordinals_067_098",
            "interval_bytes_lf": 3568708,
            "interval_id": "routed-process-ordinal-070-minified-lines-226-3813",
            "interval_lines": 3588,
            "interval_sha256_lf": "ad876d11d7f34252c672254b1fe4f8549b5fe1d3f28e8a37268798abe13286d5",
            "line_range": [
              226,
              3813
            ],
            "ordinal": 70,
            "parent": "e5ea8472071b842445a8a4c3763ec7878aabbebd",
            "patch_bytes": 3599773,
            "patch_lines": 3844,
            "patch_sha256_raw": "00672e2353527f90890f15dba203cf05b5f76e1b3a3aae9e3ffb6fe6dba36cbd",
            "source_ref": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
            "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
            "subject_type": "GIT_PATCH_TEXT_INTERVAL"
          },
          {
            "commit": "2147abfac3fb6c82279aefb2b21c749a521112dc",
            "group_id": "routed_process_ordinals_067_098",
            "interval_bytes_lf": 3568708,
            "interval_id": "routed-process-ordinal-098-minified-lines-2012-5599",
            "interval_lines": 3588,
            "interval_sha256_lf": "ad876d11d7f34252c672254b1fe4f8549b5fe1d3f28e8a37268798abe13286d5",
            "line_range": [
              2012,
              5599
            ],
            "ordinal": 98,
            "parent": "b109707fbacf7a3e2b64bdc2d69aae3ada761ece",
            "patch_bytes": 5178479,
            "patch_lines": 22393,
            "patch_sha256_raw": "0d1585d2f206efd3b1e4ca1bb5697f01f843f7952718c5b4ec5efa86a8749ebc",
            "source_ref": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
            "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
            "subject_type": "GIT_PATCH_TEXT_INTERVAL"
          }
        ]
      }
    },
    "supplemental_process_text": {
      "binding_sha256": "289b8ca30d47675be9ce1407b53247a8dbea60e743ca3794f56a9837c0835ee2",
      "group_id": "supplemental_process_text",
      "kind": "FULL_TEXT",
      "record_count": 6,
      "record_manifest_sha256": "4f46236399bea189c64d2b9871199a647d25328341575545cd852f59178d3fb7",
      "summary": {
        "documents": 6,
        "lines": 728
      }
    }
  },
  "readers": [
    {
      "reader_id": "step692_final_science",
      "assignments": [
        {
          "group_id": "release_scientific_document_text",
          "record_count": 118,
          "record_manifest_sha256": "69520a33892446b0c5a5038b71535cd2849575d4b12284452726f9229c5de1ab",
          "binding_sha256": "e85898e4d6425581e738934a3fba19aca265e17ebeadaa8271949eda6b341a98",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "release_code_test_text",
          "record_count": 7,
          "record_manifest_sha256": "a63bc0c6c286eb7d25fe3769c16fc7fd9e120c9f2e8b2fd2857fa4b10c230acf",
          "binding_sha256": "1c85b6dcabc12122dda239761d94033617607e3f3e0fd42cfeee53be5dcc25e1",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "release_pdf",
          "record_count": 3,
          "record_manifest_sha256": "b216aa128227d9c74cf5d76307cde3825341849ba809afbfe10451b99ab1206c",
          "binding_sha256": "746756744e7df1671f4eb72a75464628ff2a3144849db86c2be12561d3838cde",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "release_image",
          "record_count": 3,
          "record_manifest_sha256": "ce1b44c3abca0e227bf3c0ea0cb2217c205ed644fe7b801e6410178281d2c9ea",
          "binding_sha256": "9d33018bbcf6eaaa80047f8a7d7633a56e681b8913d2e4079567ab36f34e8eb9",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "supplemental_process_text",
          "record_count": 6,
          "record_manifest_sha256": "4f46236399bea189c64d2b9871199a647d25328341575545cd852f59178d3fb7",
          "binding_sha256": "289b8ca30d47675be9ce1407b53247a8dbea60e743ca3794f56a9837c0835ee2",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "routed_process_ordinals_067_098",
          "record_count": 32,
          "record_manifest_sha256": "43e59f101eb2ec352277049b62e46b8a02917af637d57a38ba1b98417ebacbb4",
          "binding_sha256": "0a2af66967d7d51d800e40d05e2507dd526d71837f2131a0eb8e231dc838a74d",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [
        "P065-S70-F06",
        "P065-S70-F07",
        "P065-S70-F08",
        "P065-S70-F09",
        "P065-S70-F10",
        "P065-S70-F11",
        "P065-S70-F12",
        "P065-S70-F13",
        "P065-S70-F14",
        "P065-S70-F15",
        "P065-S70-F16",
        "P065-S70-F17",
        "P065-S70-F18",
        "P065-S70-F19",
        "P065-S70-F20",
        "P065-S70-F21",
        "P065-S70-F22",
        "P065-S70-F23",
        "P065-S70-F24",
        "P065-S70-F25",
        "P065-S70-F26",
        "P065-S70-F27"
      ],
      "report_binding_sha256": "49478924bdd1380c8adec1d20b04502f9030bba0a5a06f9f5afdea78a2899b10"
    },
    {
      "reader_id": "step692_final_records",
      "assignments": [
        {
          "group_id": "routed_process_ordinals_001_033",
          "record_count": 33,
          "record_manifest_sha256": "662905ea4b1068d525900ad909ed6ea18e912b427d9083e0251683f7635c3648",
          "binding_sha256": "6c228cc9e1f0c7babdd847d4b22ad4cef027749b6df038ef3db4e3cded29a2f9",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [],
      "report_binding_sha256": "93add8f2c780e7309266a91f257ddc93a2e5402166c4a3b74ace5691f921efcb"
    },
    {
      "reader_id": "step692_final_validator",
      "assignments": [
        {
          "group_id": "routed_process_ordinals_034_066",
          "record_count": 33,
          "record_manifest_sha256": "df62b8210b15c82faf5cfa9475f7ff909242f6f31ae50131558c4efea1713ef6",
          "binding_sha256": "87ffa75d74131868900657dcaeb5d16e75c5e0da637180e67228e3e7356c0640",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [],
      "report_binding_sha256": "46efd73483e590ec28bf4c8e2825fd0c10d5279fffc8f395e15491a11314f288"
    },
    {
      "reader_id": "step70_comp_text_audit",
      "assignments": [
        {
          "group_id": "comp_v24_python",
          "record_count": 29,
          "record_manifest_sha256": "204a68df82fe7303cf3b52a016dd15ddad9e96528bca0dd6ede318dcad096215",
          "binding_sha256": "46bbdb55eeb6a2f03cb20d8b469c0eb8368083c0b80ddce22c5e2c1f659d572a",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "comp_v24_json",
          "record_count": 16,
          "record_manifest_sha256": "896fdb65d1527a289e1aa553961f85bb93ec7de3f592559a901cc6d31568ba53",
          "binding_sha256": "ce6466235a412b1c6e65c583f56da3a72e93595b7ed8ddfbcf0b9488cc4705fc",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "comp_v24_txt",
          "record_count": 7,
          "record_manifest_sha256": "178d629595481e2cf4936591f9fcba890b41eae36409be28a08f50ceeb1d23fc",
          "binding_sha256": "16c1c04f9cff49dabb0c009f0f6adeb1f154000e6fededbef5897854320daac2",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [
        "P065-S70-F28",
        "P065-S70-F29",
        "P065-S70-F30",
        "P065-S70-F31",
        "P065-S70-F32",
        "P065-S70-F33",
        "P065-S70-F34",
        "P065-S70-F35",
        "P065-S70-F36",
        "P065-S70-F37",
        "P065-S70-F38",
        "P065-S70-F39",
        "P065-S70-F40"
      ],
      "report_binding_sha256": "c54e5fafd5c992099076ca14c264cfc1a514726ffd9216edad56182f8bc3a48a"
    },
    {
      "reader_id": "step70_comp_data_visual_audit",
      "assignments": [
        {
          "group_id": "comp_v24_csv",
          "record_count": 10,
          "record_manifest_sha256": "ecede214d5dc119999d0acfd972a6a4db76d3d4eb5ca8565bb26fa24806f6064",
          "binding_sha256": "e03ed796997d371b96047ae1bc2c98dc3cbbd6a10f2b089181790ae2a1fa2ec7",
          "status": "AGENT_FULL_READ"
        },
        {
          "group_id": "comp_v24_png",
          "record_count": 33,
          "record_manifest_sha256": "863cdcbc7d460c572f057ef9f27ec70a30ad0ba78b22a8d417c16a4042ba85bd",
          "binding_sha256": "27137436c03b370f698dcc65822f4eae273bc06aca482247e0edc517689c1435",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [
        "P065-S70-F41",
        "P065-S70-F42"
      ],
      "report_binding_sha256": "6e720658fa9604d849238058378e9396a72923f5c834d664f69cb39980a1f8a7"
    },
    {
      "reader_id": "step70_narrative_audit",
      "assignments": [
        {
          "group_id": "narrative_history",
          "record_count": 74,
          "record_manifest_sha256": "8072fd05fed9548aa539c56092140943222743e6bc858f4a1d23500f37f3eb6e",
          "binding_sha256": "6e52620222da97ea8a793ecdf757f6e9018a85ced1d9cbec89af2826c721db5a",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [
        "P065-S70-F43",
        "P065-S70-F44"
      ],
      "report_binding_sha256": "73d0853895e629baa06565ea226b4385ebefe7b2c10278e65fce92d5282367a2"
    },
    {
      "reader_id": "step70_release_patch_audit",
      "assignments": [
        {
          "group_id": "release_process_all_038",
          "record_count": 38,
          "record_manifest_sha256": "d9a3726b18a708896d728a088fb16e9f44fe873819ea337fca3318d0fc2d477b",
          "binding_sha256": "ae5e548e382fb14b1e8cbdb04c241b19955e07dbd312fd810ad5258560d1fb3d",
          "status": "AGENT_FULL_READ"
        }
      ],
      "unreviewed_intervals": [],
      "output_truncation_unresolved": [],
      "report_path": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
      "report_section": "BEGIN_P065_STEP70_HUMAN_EVIDENCE_JSON",
      "finding_ids": [],
      "report_binding_sha256": "06b5017ebb8774f83d75467e4d4d7deec1ca2b73ab645c2d270307601decf183"
    }
  ],
  "unreviewed_intervals": [],
  "output_truncation_unresolved": [],
  "authority": {
    "internal_source_process_topology": true,
    "external_scientific": false,
    "external_material": false,
    "external_experimental": false,
    "external_primary_literature": false,
    "publication_ready": false,
    "canonical_model_selected": false,
    "runtime_behavior_validated": false,
    "defect_repaired": false,
    "v1024_1_independent_corroboration": false,
    "generated_artifact_independent_support": false,
    "source_self_report_is_external_authority": false
  },
  "pdf_visual": {
    "pages_extracted": 148,
    "pages_rendered": 148,
    "pages_visual": 148
  },
  "image_visual": {
    "original_resolution_visual": 3
  },
  "process_patch_read": {
    "release": 38,
    "routed": 98
  },
  "narrative_correction_acknowledged": {
    "copied_lines": 2068,
    "reconstructed_lines": 2306,
    "delta": 238
  },
  "semantic_deferred_intervals": [
    {
      "blob": "3fa2ea6ea6889e0d0d095dcc6c1ee3b9500dee6a",
      "full_bytes": 3594138,
      "full_lines": 3812,
      "full_sha256_lf": "c795a947a44b31eb4d0039e67d067a96d51d807e9a3de9fda799534180908aa1",
      "full_sha256_raw": "c795a947a44b31eb4d0039e67d067a96d51d807e9a3de9fda799534180908aa1",
      "group_id": "release_scientific_document_text",
      "interval_bytes_lf": 3565120,
      "interval_id": "release-code-guide-html-mermaid-lines-220-3807",
      "interval_lines": 3588,
      "interval_sha256_lf": "ed349941137ddb8155918d9a975c3a0f316d6080fad27652a7e8a2de8de31238",
      "line_range": [
        220,
        3807
      ],
      "path": "Claude/docs/v1.0.24/CODE_GUIDE_v24.html",
      "source_ref": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
      "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
      "subject_type": "GIT_BLOB_TEXT_INTERVAL"
    },
    {
      "commit": "1ee23c53fec14c41a1f5372a19e6b2f70adb0de0",
      "group_id": "routed_process_ordinals_067_098",
      "interval_bytes_lf": 3568708,
      "interval_id": "routed-process-ordinal-070-minified-lines-226-3813",
      "interval_lines": 3588,
      "interval_sha256_lf": "ad876d11d7f34252c672254b1fe4f8549b5fe1d3f28e8a37268798abe13286d5",
      "line_range": [
        226,
        3813
      ],
      "ordinal": 70,
      "parent": "e5ea8472071b842445a8a4c3763ec7878aabbebd",
      "patch_bytes": 3599773,
      "patch_lines": 3844,
      "patch_sha256_raw": "00672e2353527f90890f15dba203cf05b5f76e1b3a3aae9e3ffb6fe6dba36cbd",
      "source_ref": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
      "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
      "subject_type": "GIT_PATCH_TEXT_INTERVAL"
    },
    {
      "commit": "2147abfac3fb6c82279aefb2b21c749a521112dc",
      "group_id": "routed_process_ordinals_067_098",
      "interval_bytes_lf": 3568708,
      "interval_id": "routed-process-ordinal-098-minified-lines-2012-5599",
      "interval_lines": 3588,
      "interval_sha256_lf": "ad876d11d7f34252c672254b1fe4f8549b5fe1d3f28e8a37268798abe13286d5",
      "line_range": [
        2012,
        5599
      ],
      "ordinal": 98,
      "parent": "b109707fbacf7a3e2b64bdc2d69aae3ada761ece",
      "patch_bytes": 5178479,
      "patch_lines": 22393,
      "patch_sha256_raw": "0d1585d2f206efd3b1e4ca1bb5697f01f843f7952718c5b4ec5efa86a8749ebc",
      "source_ref": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
      "status": "SEMANTIC_DEFERRED_STRUCTURAL_INTERVAL",
      "subject_type": "GIT_PATCH_TEXT_INTERVAL"
    }
  ],
  "finding_routes": [
    {
      "id": "P065-S70-F06",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The generalized silicon regular-solution denominator and critical threshold are not derived.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 74",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F07",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Finite fitted width is not independent single-phase evidence.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F08",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Regular-solution applicability conflicts across seed, derivative, entropy, solver, and guide surfaces.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F09",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Ref. 7 completion is a rejected self-claim while the original remains unavailable.",
      "owner": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
      "target_steps": [
        "Step 71"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F10",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Generated HTML table rows contain delimiter-induced extra cells.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F11",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "The exact HTML generator command was not found.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F12",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The cross-rate example independently refits both currents and is not held out.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 72",
        "Step 73",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F13",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The reported two-phase confirmation is constrained by the optimizer lower bound and misstates the critical point.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F14",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "An analytic LCO curve is mislabeled as a real-data fit despite absent LCO-specific raw data.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 72",
        "Step 74",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F15",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The anode ablation reuses in-sample anchors and cannot diagnose overfitting.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F16",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "A width-only silicon phase assignment lacks structural evidence and conflicts with the lineage.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F17",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The claimed data-quality cause is confounded across chemistry and acquisition route.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F18",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Two-cell in-sample consistency does not establish industrial generality or no-refit usability.",
      "owner": "PHASE-075-AUTHORITY-DISPOSITION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F19",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The temperature example reproduces inserted calibration targets and provides no held-out prediction.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F20",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Two DOI identities conflict on article numbers and require primary metadata resolution.",
      "owner": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
      "target_steps": [
        "Step 72"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F21",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "A test-only process commit does not establish experiment completion.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 73"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F22",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Absorption of the seconds/hour factor does not preserve physical parameter interpretation.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 73",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F23",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Six numerical seeds lack a closed primary-source route.",
      "owner": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F24",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Ref. 7 authority promotion is rejected pending original-source acquisition.",
      "owner": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
      "target_steps": [
        "Step 71"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F25",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The reflect check neither proves a single peak nor tests the regular-solution limit.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 73"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F26",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Internal status labels do not establish external correctness or adoption.",
      "owner": "PHASE-075-AUTHORITY-DISPOSITION",
      "target_steps": [
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F27",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The G-E3 comparison uses a same-family fixed-point result rather than independent truth.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 72",
        "Step 73",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F28",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Target-window peak selection is circular and cannot validate the assignment independently.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F29",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "An in-sample O2 fit cannot establish the O3 model or an absence cause.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F30",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The denoising comparison changes its target and lacks held-out support.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F31",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Reciprocal transformation of the same fitted derivative is not independent validation.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F32",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "Flexible blend peaks do not establish component identity or fraction without a material model and capacity basis.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F33",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The rate script fits position rather than full width at half maximum and cannot support the broadening claim.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F34",
      "severity": "P1",
      "status": "OPEN_ROUTED",
      "summary": "The LCO R3 default conflicts between release documentation and source.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 73",
        "Step 74",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F35",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "The graphite first-look capacity label conflicts with a factor-1000 conversion.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F36",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Resistance divided by current in mA is reported without a coherent derived unit.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F37",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Optional filtering can silently fall back or replace invalid output without explicit status.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 73",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F38",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "The asymmetric peak is unnormalized and its precise source route remains unresolved.",
      "owner": "PHASE-072-SCIENTIFIC-REDERIVATION",
      "target_steps": [
        "Step 71",
        "Step 72",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F39",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Historical absolute paths are provenance, not portable reproduction commands.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 73",
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F40",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Duplicate and reversed LCO composition coordinates require an explicit normalization rule.",
      "owner": "PHASE-073-RUNTIME-BOUNDARY",
      "target_steps": [
        "Step 71",
        "Step 73",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F41",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Seventeen PNGs contain missing-glyph boxes and require verified-font regeneration.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 72",
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F42",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Four visual artifacts contain clipping, scalar-representation, or label-overlap defects.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 72",
        "Step 74"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F43",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "The fitting guide carries stale v1.0.20 metadata in the v1.0.24 surface.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 74",
        "Step 75"
      ],
      "authority_promoted": false
    },
    {
      "id": "P065-S70-F44",
      "severity": "P2",
      "status": "OPEN_ROUTED",
      "summary": "Two Markdown records lack a final line feed.",
      "owner": "PHASE-074-DOCUMENT-REPAIR",
      "target_steps": [
        "Step 74"
      ],
      "authority_promoted": false
    }
  ]
}
```
END_P065_STEP70_HUMAN_EVIDENCE_JSON

The evidence schema requires exactly 15 mandatory groups: release
scientific/document text, release code/test text, release PDFs, release images,
supplemental process text, narrative history, five non-Markdown `comp_v24`
groups, the 38-commit release projection, and the three routed-process ordinal
partitions. Each group must be assigned to exactly one reader with the
machine-recomputed record count, record-manifest hash, and binding hash. Missing,
extra, or duplicate group assignments are rejected.

Each reader report is durably located at this result's evidence marker and has
its own canonical report-binding hash over the reader identity, exact group
assignments, finding IDs, and empty gap/truncation declarations. The 39 routed
finding IDs are partitioned exactly once across those reports. The resulting
topology carries every text/page/image machine extent as its human read range;
each process parent patch likewise carries the exact `1–lines` read interval
plus the same reader/group/binding identity used by its partition assignment.

## 10. Machine Artifacts and Validation

The initial validator-first RED run, executed after the result and validator
existed but before either machine artifact existed, terminated as required:

```text
FAIL_P065_STEP70_CONTENT E_ARTIFACT_MISSING: ...PHASE_065_SOURCE_PROCESS_TOPOLOGY.json
EXIT=1
```

The hardening TDD RED run was then executed before production-policy changes:

```text
py -3.12 -B Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
FAIL_P065_STEP70_HARDENING_SELFTEST E_HARDENING_SELFTEST: accepted_source_policy=['importlib-dynamic-import', 'filesystem-write-text', 'filesystem-write-bytes', 'filesystem-touch', 'builtin-open-write', 'builtin-open-append', 'builtin-open-create', 'builtin-open-update', 'tempfile-outside-atomic-writer', 'git-wrapper-non-git-literal', 'git-alias-execution', 'git-protocol-override', 'git-ext-protocol']; unmet_contracts=['validator-defers-builder-import', 'neutral-machine-status', 'mandatory-evidence-groups', 'exact-authority-ceiling', 'canonical-process-partitions', 'full-commit-path-separation', 'routed-path-separation', 'historical-binary-metadata']
EXIT=1
```

A second test-first expansion for callable aliases and `Path`/`io` open routes
also failed before its implementation:

```text
py -3.12 -B Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
FAIL_P065_STEP70_HARDENING_SELFTEST E_HARDENING_SELFTEST: accepted_source_policy=['builtin-open-alias', 'path-open-write', 'io-open-write', 'tempfile-callable-alias', 'git-wrapper-callable-alias']; unmet_contracts=[]
EXIT=1
```

After the bounded hardening implementation, the complete named policy,
evidence-contract, and exact-current-state suite is green without creating
either machine artifact:

```text
py -3.12 -B Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
PASS_P065_STEP70_HARDENING_SELFTEST cases=59
EXIT=0
py -3.14 -B Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
PASS_P065_STEP70_HARDENING_SELFTEST cases=59
EXIT=0
```

The later SPEC review was applied as a separate test-first hardening cycle. Its
first named-probe run failed before the production fixes:

```text
py -3.12 Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
FAIL_P065_STEP70_HARDENING_SELFTEST E_HARDENING_SELFTEST: accepted_source_policy=['subprocess-tuple-alias', 'subprocess-subscript-alias', 'filesystem-os-remove', 'filesystem-shutil-rmtree', 'git-run-process-callable-alias', 'git-run-process-tuple-alias', 'git-run-process-subscript-alias', 'git-dynamic-protocol-value']; unmet_contracts=['frozen-phase057-source-ref', 'unique-run-process-boundary', 'frozen-process-query-argv', 'kind-specific-read-status', 'reviewed-process-record-binding', 'cross-projection-classification', 'finding-route-schema']
EXIT=1
```

A second test-first projection contract failed because the required consistency
API did not yet exist:

```text
py -3.12 Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
AttributeError: module 'build_phase065_step70' has no attribute 'require_process_projection_consistency'
EXIT=1
```

After implementing the bounded SPEC fixes, both supported runtimes pass the
expanded 96-case selftest while the JSON-last artifacts remain absent:

```text
py -3.12 Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
PASS_P065_STEP70_HARDENING_SELFTEST cases=96
EXIT=0
py -3.14 Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
PASS_P065_STEP70_HARDENING_SELFTEST cases=96
EXIT=0
```

Independent SPEC/quality review then found that the 96-case policy still
accepted indirect callable dispatch, writer-owner abuse, mutable Git commands,
dynamic write modes, and unpinned upstream/origin identity. Named RED cycles
reproduced those failures before each implementation. The widest source-policy
RED contained 23 accepted attacks, including inline list/dict/lambda dispatch,
`vars`/`partial`, `shutil` moves/copies, `**mode` writes, arbitrary writer-owner
unlink, and `clean`/`reset`/`push` inside an otherwise allowlisted Git owner.
Later RED cycles separately exposed Git output/work-tree/textconv options,
14 OS/filesystem/callback and dynamic branch/ref mutations, `Path.replace` and
`os.environ` mutation, removal/substitution of the atomic target guard, and the
mutable process-binding schema.

The final bounded policy uses an exact import-symbol allowlist, rejects indirect
callable shapes and sensitive references, permits only the two exact
`subprocess.run` wrappers, gives each Git subcommand an exact read-only argv
grammar, pins the symbolic upstream and normalized GitHub origin identity,
pins the complete atomic-writer AST and its two output callsites, and constrains
runtime writes to the topology and attestation paths. It also independently
binds the correct ordinal-98 Mermaid interval `2012–5599`; the previous
`2036–5623` controller interval was rejected because it omitted 24 vendor lines
and deferred 24 authored/footer lines. Process machine bindings now exclude the
later-mutated read status and are validator-recomputed as
`machine-process-projection-v1`.

A final test-first namespace cycle then reproduced environment, module-cache,
import-path, import-hook, namespace-alias, print-alias, and function-default
alias attempts. The first run rejected all but `sys.meta_path.insert(...)` and
a sensitive namespace captured in a function default. The bounded fix pins the
only permitted `sys.path` access to the exact builder loader, pins the only
permitted `sys.stdout` operation to the validator entry point, rejects every
other `sys.*` attribute access, checks positional and keyword-only defaults for
sensitive callable capture, and adds complete atomic-writer-definition removal
to the negative controls.

The final independent source review exposed three additional P1 contract gaps:
F28–F44 were documented but not mandatory, module-level rebinding could replace
validated functions after their definitions, and the `__builtins__` namespace
could bypass direct-name restrictions. Test-first repairs require the exact
F01–F44 artifact order and exact F06–F44 evidence set, independently exercise
missing/duplicate/extra/schema mutations, reject decorators and every
module-level rebinding of a declared function, and ban `__builtins__` plus
`breakpoint`. The builder loader now evicts the same-name module cache entry and
checks the imported module's resolved source identity. Reader-report hashes and
exact process-patch read ranges close the two accompanying evidence-strength
concerns.

The first real-evidence preflight then failed all seven reader hashes because a
manual calculation omitted the canonical serializer's terminal LF. The hashes
were recomputed with the same canonical byte function used by builder and
validator. Hardening now parses the current result evidence itself and checks
the exact marker lines, strict JSON, 15-group union, seven reader-report hashes,
39 finding routes, and zero unresolved gaps before collection can begin; a
synthetic fixture alone can no longer mask drift in the live result.

The next source review reproduced six further RED cases: three structural
pattern bindings that replace a top-level function name, two transitive
`subprocess` namespace paths, and a two-stage `argparse.FileType('w')` write.
The final policy treats `MatchAs`, `MatchStar`, and mapping-rest names as
module-level binders and constrains every attribute chain rooted in an allowed
module to the exact chain set used by the frozen builder and validator. A
direct-import allowlist therefore cannot be widened through a re-exported
module or callable factory.

A final targeted cycle reproduced assignment, deletion, and import replacement
of a module function through a nested function's `global` declaration. The
policy now rejects every `ast.Global` name that intersects the declared
top-level function set; all three named variants are retained as negative
controls.

The last loader-integrity cycle reproduced an `async def` duplicate of a
critical function plus missing, assignment-replaced, and class-replaced loader
definitions. Synchronous and asynchronous top-level definitions now share one
duplicate-name inventory, and any validator surface containing
`source_policy_errors` must contain exactly one synchronous `load_builder`
whose complete AST equals the frozen loader contract.

The required-function cycle then removed and assignment-replaced pre-evidence,
actual-evidence, source-policy, staged, persistence, and builder-evidence gates.
The validator now supplies the expected source kind explicitly and requires the
exact ordered synchronous top-level function inventory for both builder and
validator. It also distinguishes a true module-level owner from a nested
function with the same name, so a nested writer or Git-wrapper name cannot
inherit a privileged write/process boundary. Six inventory mutations and two
nested-owner variants remain in the hardening suite.

The final process/write boundary cycle then replaced each `run_git` wrapper's
actual `run_process` argv and aliased both class-level and instance-level
`Path.open`. The only permitted wrapper calls are now the exact
`run_process(root, ['git', *args])` forms used by builder and validator, and an
`open` attribute is treated as a sensitive callable with direct-call allowance
only for `Image.open`. All four substitutions are retained as RED-before-GREEN
regressions.

As a fail-closed completion of that boundary, the full ASTs of both supported
`run_process` implementations and both `run_git` implementations are pinned.
Named tests that reassign the checked `args`/`argv` before execution prove that
read-only validation and the subprocess call cannot be separated by an
unreviewed mutation inside either wrapper.

The pre-collection historical hardening gate was:

```text
py -3.12 -B Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
PASS_P065_STEP70_HARDENING_SELFTEST cases=247
EXIT=0
py -3.14 -B Codex/work/v1024_phase065/validate_phase065_step70.py --hardening-selftest
PASS_P065_STEP70_HARDENING_SELFTEST cases=247
EXIT=0
```

That self-test intentionally asserts the result-first state and is not the
post-collection reproduction command. After evidence integration, the current
reproducible precommit gates are `--content-only` and `--staged`; both returned
`PASS_P065_STEP70_CONTENT` and `PASS_P065_STEP70_STAGED` on Python 3.12 and
3.14 with determinism `2/2`, semantic cases `25`, source-policy cases `149`,
and strict-JSON cases `6`.

The following artifacts are collected from the completed human evidence block
under the JSON-last rule:

- `Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json`;
- `Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json`.

The validator must fail while either artifact is absent. Final validation must
pass on Python 3.12 and 3.14, include deterministic double generation, strict
JSON rejection probes, source-policy attacks, exact-eight status control, and
post-push live-remote persistence verification.

## 11. Gate State

Current Step 70 gate: `PASS_P065_STEP70_PRECOMMIT`; commit/push persistence is pending.

The only passing persistence terminal is `PASS_P065_STEP70_PERSISTENCE`.
Step 71 is not released until that terminal is observed on both supported
Python runtimes after push and fetch.

## 12. Exact Commit Contract

The Step 70 commit may contain exactly these eight paths:

1. `Codex/work/v1024_phase065/build_phase065_step70.py`
2. `Codex/work/v1024_phase065/validate_phase065_step70.py`
3. `Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json`
4. `Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json`
5. `Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Renames are forbidden. The expected parent is
`83323ebfff1c468e4ada5e695ced10c69e24fb32` and the exact subject is
`audit(phase065): freeze v1024 source process topology`.
