# Phase 061 Step 48 Lineage Delta and Snapshot Genealogy Result

정본일: 2026-08-26

Gate: `PASS_P061_STEP48_LINEAGE_DIFF`

Status: `PASS_WITH_CONCERNS`

## Objective and Authority Boundary

Step 48은 frozen v1.0.19 release 66 occurrence와 frozen v1.0.20 corpus 232 occurrence를 role·chapter·section·artifact identity로 대조하고, 모든 v1.0.20 occurrence를 정확히 한 번 분류했다. 또한 v1.0.20 structural snapshot 10 occurrence의 stage genealogy와 adopted-release source delta를 Git object에서 재구성했다.

이 gate가 확정하는 범위는 frozen source bytes, occurrence pairing, exact text delta, LaTeX equation·label·bibliography·include projection, Python abstract syntax tree (AST) projection, PDF page extent, snapshot occurrence와 Git genealogy다. Primary-paper 진실성, DOI support, material law, equation·derivation validity, runtime behavior, figure/PDF 수치 타당성, 실험적 권위 또는 standalone appendix의 adopted-release 지위는 확정하지 않는다.

## Recovery and Actual Read Coverage

복구 경계에서 다음 정본을 1행부터 EOF까지 다시 읽었다.

- master plan: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`, 1–665;
- active Phase 061 plan: `Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md`, 1–562;
- previous result: `Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md`, 1–186;
- active ledger 1–95, parent ledger 1–48, active handover 1–244 pre-edit;
- Step 46 topology, Step 47 authority matrix, Phase 060 v1.0.19 topology와 complete manifest를 strict parse하고 pairing input 전건을 순회했다;
- v1.0.19 release 66 occurrence와 v1.0.20 232 occurrence의 frozen Git blobs를 comparison endpoint로 사용했다;
- snapshot 10 occurrence와 9 stage edge, P5/P6 commit boundary, final appendix-root projection을 Git object에서 독립 재구성했다.

Step 47의 process claim은 navigation과 authority ceiling에만 사용했다. Step 48의 pairing, source delta, snapshot content 또는 Python AST 결과를 Step 47 self-report에서 복사해 진실로 승격하지 않았다.

## Validator-first RED

Step 48 validator skeleton을 artifact 작성 전에 실행했을 때 다음 네 named diagnostic만 반환했다.

```text
STEP48_BUILDER_MISSING
STEP48_LINEAGE_MATRIX_MISSING
STEP48_RESULT_MISSING
STEP48_SNAPSHOT_GENEALOGY_MISSING
```

이 RED는 Step 48 신규 산출물 부재를 명시적으로 검출했다. 이후 builder와 두 machine artifact를 생성하고 result/control 문건을 이 exact-eight 경계에 추가했다.

## Endpoint Coverage and Pairing

| Field | Exact value |
|---|---:|
| v1.0.20 occurrences / unique blobs | 232 / 231 |
| v1.0.19 release occurrences | 66 |
| paired v1.0.20 occurrences | 54 |
| separate v1.0.19-only counterparts | 12 |
| v1.0.19 source reuse | 0 |
| `ADDED / MODIFIED / UNCHANGED / RENAMED / COPIED` | `178 / 29 / 18 / 7 / 0` |
| paired text hunks | 117 |
| changed old / new lines over all paired text | 233 / 782 |

Primary pairing은 full version-relative path의 version-neutral identity다. Basename-only pairing은 금지했고, Python module·handover·Ch1/Ch2 roots와 PDFs·test의 7개 semantic rename만 명시적 old/new identity로 저장했다. `P061-DELTA-0001..0232`는 manifest index 1–232와 일대일이며, paired old 54개와 old-only 12개의 합집합은 v1.0.19 release 66개와 exact하다.

Old-only 12개는 roundtrip demo, golden NPZ, graph suite, sample continuity text 1개와 PNG 8개다. 삭제 또는 패키지 제외의 process rationale은 발견했다고 만들지 않고 `P061-STEP48-UNV-006`으로 route했다.

## Adopted Release Delta

Step 47 결과의 “Adopted TeX source 43” 표현은 부정확하다. 현재 exact matrix의 adopted source 43개는 TeX 41, Python 1, Markdown 1이며 role은 theory 40, result 1, code 1, implementation guide 1이다. 이미 commit된 Step 47 결과를 재작성하지 않고 이 result에서 정정 경계를 고정한다.

| Field | Exact value |
|---|---:|
| adopted sources | 43 |
| comparison `MODIFIED / UNCHANGED / RENAMED` | `27 / 13 / 3` |
| old / new physical lines | `6,425 / 6,638` |
| changed old / new lines | `106 / 319` |
| exact opcode segments | 84 |
| final release surface occurrences | 53 |
| final release `MODIFIED / UNCHANGED / RENAMED` | `29 / 18 / 6` |

Ch1 adopted TeX 25개는 3,711→3,902행, exact changed line `-76/+267`이다. Ch2 adopted TeX 16개는 1,428→1,447행, `-23/+42`다. 따라서 Ch2를 source-text 차원에서 “bibliography-only”라고 부를 수 없다. 아래 bibliography-only 경계는 snapshot equation-body projection에만 적용된다.

v1.0.20에서만 존재하는 TeX 63개에는 모두 경쟁 draft surface inventory를 저장했다. 이 inventory는 adopted source나 scientific authority를 만들지 않는다.

## Equation, Bibliography and Include Findings

Baseline→final snapshot projection에서 Ch1은 label `219→225`, displayed-equation block `122→128`, bibliography `28→36`이다. 새 label과 equation block은 각각 6개이고 bibliography key는 8개 추가됐다. 기존 `eq:lco-slots`의 substantive hash는 `33b9f996b18e`에서 `228a215741f1`로 바뀌었다.

Ch2는 label `69→69`, equation block `32→32`, substantive projection SHA-256 `93cc152ed77eea330da56f57cc55df77de239df836a1b0f88b6f3fff77df286f`로 전후가 같다. 네 unlabeled equation key는 source insertion에 따라 줄 위치만 이동했고 body hash는 유지됐다. Bibliography는 14→16이며 `dahn1991`, `ohzuku1993`가 추가됐다.

LaTeX bracket-display parser의 최초 후보는 행간격 명령 `\\[4pt]`를 `\[` 수식 시작으로 오인했다. 독립 QUALITY 검수에서 이 P1을 발견했고, 연속 backslash parity를 판정하는 lexer로 교체했다. 회귀 후 `ch1_sec13_lcohys.tex`의 실제 결과는 changed 0, moved 4이며 escaped bracket control을 required negative set에 추가했다.

Ordered include topology는 Ch1 24, Ch2 15, 합계 39 edge다. Added, removed, moved edge는 모두 0이며 root placeholder와 주석 내부 pseudo-include는 edge로 세지 않았다. Standalone appendix는 이 39개 adopted Ch1/Ch2 include edge에 없다.

## PDF and Image Lineage

Paired PDF는 3개로 95→99 pages다: standalone appendix 8→8, Ch1 62→66, Ch2 25→25. 새 PDF 11개·31 pages를 합친 v1.0.20 전체는 14개·130 pages다.

Image occurrence는 v1.0.20 23개이며 unchanged paired 5, added 18, v1.0.19-only counterpart 8이다. Byte/page equality와 occurrence presence에서 visual equivalence, numerical correctness, scientific correctness 또는 experimental authority를 추론하지 않았다.

## Python and Test Source Comparison

Production module은 nonempty-field canonical JSON AST projection에서 old/new SHA-256이 모두 `bd253ce91c2409fb423968d73d68825281ba76e76976824c9d7f56acd684bdf8`로 같고, 41개 definition은 added/removed/changed 0이다. 이는 frozen source structure equality이며 runtime behavior equality가 아니다.

Test source는 127→427 physical lines이며 AST projection이 다르다. Added definition 8, removed 3, changed 2를 보존했다. Production과 test module을 import하거나 실행하지 않았고 fresh G1/G2/G3/n(T) 실행과 behavioral equivalence는 Phase 067 queue로 남겼다.

## Snapshot Genealogy

| Field | Exact value |
|---|---:|
| snapshot occurrences | 10 |
| unique blobs | 9 |
| stage edges | 9 |
| duplicate occurrence groups | 1 |
| pre-final occurrences | 8 |
| final appendix-root occurrences | 1 |

Chronology는 baseline→P0→P2→P3→P4→P5→P6→P7→P7b→final이다. P1 structural snapshot은 찾지 못했다. 모든 occurrence에는 full captured document projection을 포함하고 9개 stage edge를 양 endpoint blob과 연결했다.

P5와 P6는 distinct path/occurrence지만 blob과 captured projection이 byte-identical하다. P6 commit은 P5 commit의 direct child이나, 두 commit 사이 실제 source tree에는 TeX 3개를 포함한 변경 path 11개가 있다. 따라서 snapshot identity는 source-tree identity가 아니다. P6 snapshot을 재생성했는지 P5 bytes를 복사했는지는 근거 미발견이다.

Standalone appendix root는 pre-final 8 occurrence에 0, final snapshot에 1회 나타난다. Snapshot enumeration만으로 adopted Ch1/Ch2 include edge를 만들지 않았고 Phase 062에서 adoption authority를 판정한다.

## Ground Not Found

| ID | Object | Next owner |
|---|---|---|
| `P061-STEP48-GNF-001` | P1 structural snapshot | Phase 061 boundary |
| `P061-STEP48-GNF-002` | snapshot generation command/cwd/runtime/environment | Phase 067 |
| `P061-STEP48-GNF-003` | P6 regeneration versus P5-byte copy evidence | Phase 061 boundary |
| `P061-STEP48-GNF-004` | historical snapshot-embedded source blob provenance | Phase 061 boundary |
| `P061-STEP48-GNF-005` | adopted Ch1/Ch2 root의 standalone appendix include edge | Phase 062 |

## Unverified Queue

8개 queue를 해결로 승격하지 않았다.

- Phase 067: fresh test execution, runtime equivalence, generated PDF numerical/scientific correctness, old-only 12개 rationale, historical snapshot collision/truncated-hash risk;
- Phase 071: primary DOI/bibliography claim support, equation·derivation·material-law scientific validity;
- Phase 062: standalone appendix adoption authority.

## Builder and Machine Artifacts

| Artifact | Physical lines | Bytes | UTF-8 LF SHA-256 |
|---|---:|---:|---|
| `build_phase061_step48_lineage_diff.py` | 1,286 | 62,808 | `53fa69dd440729fcedbc5ed61c3bd56ea94de288a048cc39c249cfd548aa920a` |
| `PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json` | 23,511 | 976,227 | `25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914` |
| `PHASE_061_V1020_SNAPSHOT_GENEALOGY.json` | 27,979 | 888,081 | `629995ab5936587840e5944c513ef86a0e82f114dd1d94860b06754fb9fdd414` |
| `validate_phase061_step48.py` | 2,008 | 107,679 | `3989946ac3aea915af45216469c0c9ccb096f40ac04ba0d6ed3fa95fc0a8c411` |

두 JSON은 strict duplicate-key/nonfinite parse와 full recursive traversal을 적용했다. Lineage matrix는 20,442 nodes, snapshot genealogy는 24,339 nodes를 전건 순회했다. Builder는 frozen Git blobs를 읽을 뿐 production/test module을 import·execute하지 않으며 generated output을 source-of-record로 승격하지 않는다.

## Validation

| Field | Exact value |
|---|---|
| content | `PASS_P061_STEP48_LINEAGE_DIFF` |
| matrix negative controls | `PASS_P061_STEP48_NEGATIVE_CONTROLS 66/66` |
| strict JSON negative controls | `PASS_P061_STEP48_STRICT_NEGATIVE_CONTROLS 2/2` |
| boundary negative controls | `PASS_P061_STEP48_BOUNDARY_CONTROLS 29/29` |
| determinism | `PASS_P061_STEP48_DETERMINISM 2/2` |
| Python 3.12 / 3.14 rebuild | `2/2` byte-identical for both artifacts |
| final SPEC / QUALITY | `PASS / PASS`; `P0/P1/P2=0/0/0` |

각 66개 content mutation은 full unfiltered diagnostic set에서 의도한 singleton diagnostic 하나로 격리됐다. Boundary 29건은 result·두 ledger·handover의 current-state contradiction, exact-eight dirt/staging, active/protected/main/Claude 상태를 포함한다. Disposable builder rebuild 2회와 Python 3.12/3.14 교차 재생성은 두 persisted JSON과 byte-identical했다. External scientific authority promotion: 0.

실행한 핵심 검증은 다음과 같다.

```powershell
python -m py_compile Codex/work/v1020_phase061/validate_phase061_step48.py
python Codex/work/v1020_phase061/validate_phase061_step48.py --content-only --run-negative-probes --run-boundary-probes --determinism-check
python Codex/work/v1020_phase061/validate_phase061_step48.py
git diff --check
git status --short --branch
```

Final independent QUALITY review는 builder 1–1,286, lineage JSON 1–23,511, snapshot JSON 1–27,979를 전문 또는 strict full traversal하고 최초 bracket-display P1 수정 후 `PASS`, `P0/P1/P2=0/0/0`으로 닫혔다. Validator contract review도 1–2,008행 전문과 combined suite PASS를 확인했다.

## Files in the Atomic Step Boundary

1. `Codex/work/v1020_phase061/build_phase061_step48_lineage_diff.py`
2. `Codex/work/v1020_phase061/validate_phase061_step48.py`
3. `Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json`
4. `Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json`
5. `Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## Protected Non-changes

- `Claude/**` source and artifacts were read-only; tracked/untracked modification is 0.
- protected Codex branch and `main` were not modified.
- source LaTeX/PDF/PNG/Python/test/snapshot, credentials and global configuration were not modified.
- no merge, rebase, pull request or source repair was performed.

## Persistence

| Field | Exact value |
|---|---|
| parent | `46f17a9863b5a2ce0708524b09601930000e233f` |
| subject | `audit(phase061): trace v1019-v1020 lineage delta` |
| state | `PENDING_AT_PRECOMMIT_BY_DESIGN` |

Step 49 remains pending until exact-eight commit/push/remote verification establishes the persistence gate `PASS_P061_STEP48_PERSISTENCE`.
