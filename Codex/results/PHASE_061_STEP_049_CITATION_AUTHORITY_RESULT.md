# Phase 061 Step 49 — Citation, Background and Equation-authority Audit Result

정본일: 2026-08-26

상태: `PASS_WITH_CONCERNS`

Gate: `PASS_WITH_CONCERNS_P061_STEP49_CITATION_AUTHORITY`

영속 상태: `PENDING_AT_PRECOMMIT_BY_DESIGN`

예정 commit subject: `audit(phase061): bound v1020 citation authority`

## 1. 결론

Step 49는 frozen v1.0.20 채택 원천 43개를 인용·참고문헌·표시 수식·변경 산문·출처 귀속·코드 비노출 경계로 다시 읽고, 모든 자산의 권위 상한을 내부 release text와 metadata consistency로 제한했다. 참고문헌의 존재, 인용 인접성, 수식 본문 hash, process rationale, review 합의 어느 것도 1차 문헌 진실이나 과학적 타당성으로 승격하지 않았다.

이번 gate가 확정하는 것은 다음뿐이다.

- 채택 source occurrence `43/43 = TeX 41 + Python 1 + Markdown 1`의 frozen blob·extent·Step 47 route·Step 48 delta 연결;
- 장별 bibliography/citation identity, source-text display equation, 변경 산문과 출처 귀속의 전수 inventory;
- 새 bibliography occurrence 10개 중 genuinely new source identity 8개의 Phase 071 검증 queue와 기존 identity의 장별 alias occurrence 2개;
- inherited carry 52건과 Phase 060 신규 blocker 5건의 미해결 상태 무변경;
- v1.0.20 source baseline의 code-free 본문 위반과 유도·출처 공백의 명시적 보존.

외부 논문 원문, DOI resolver, Crossref, 실험자료는 이 Step에서 조회하지 않았다. 따라서 primary literature truth, DOI metadata truth, material/experimental validity, 수식의 외부 권위는 모두 `UNVERIFIED_EXTERNAL`이다.

## 2. 입력과 회복 지점

직접 재확인한 운영 원천은 다음과 같다.

- master plan `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md` 1–665;
- Phase 061 detailed plan `Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md` 1–562, 특히 Step 49 323–344;
- Step 48 result `Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md` 1–197;
- active ledger 1–96, parent ledger 1–48, active handover 1–250;
- Step 46 topology, Step 47 authority matrix, Step 48 lineage matrix와 Phase 060 carry delta를 strict JSON으로 전건 순회했다.

Step 48 exact-eight commit은 `5cf75ba2fd4e5707c53b164d361f1526c3d31f06`이며 local HEAD, upstream, live origin이 일치했다. `PASS_P061_STEP48_PERSISTENCE`를 직접 확인한 뒤 Step 49를 시작했다. Protected Codex tip은 `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`, main tip은 `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`로 고정됐고 `Claude/**` tracked/untracked diff는 0이다.

## 3. 전문 검독 범위

### 3.1 Chapter 1

- current frozen TeX `25/25`, `3,902/3,902` physical lines, 1–EOF;
- paired v1.0.19 endpoint와 SHA-1/LF-normalized SHA-256/extent 대조;
- `SequenceMatcher(autojunk=False)` exact delta segment `56/56` 독립 재구성;
- cite command 71, ordered key reference 96, bibitem 36, source-text display 135를 전건 확인했다.

### 3.2 Chapter 2

- current frozen TeX `16/16`, `1,447/1,447` physical lines, 1–EOF;
- paired v1.0.19 `16/16`, 1,428 physical lines;
- exact delta segment `22/22`, actual text `-23/+42`를 독립 재구성;
- cite command 28, ordered key reference 34, bibitem 16, source-text display 40을 전건 확인했다.

### 3.3 Package companion

- `Anode_Fit_v1.0.20.py` 1–1,152 및 paired v1.0.19 1–1,151;
- `FITTING_GUIDE.md` 1–137 및 paired v1.0.19 1–135;
- 정형 `\cite`, `\bibitem`, DOI-like string은 0;
- `eq:` companion reference는 code 83 + guide 17 = 100 occurrence, 37 unique token이다.

두 companion은 `PACKAGE_COMPANION`이며 scholarly main body 또는 primary scientific support가 아니다.

## 4. Machine artifact

정본 machine evidence는 `Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json`이다. Builder는 frozen Git blob과 다섯 개의 persisted Codex input(Step 46 topology, Step 47 authority, Step 48 lineage, Step 48 snapshot genealogy, Phase 060 carry delta)만 읽으며 historical production/test module을 import하거나 실행하지 않는다. 각 adopted source에는 독립 reviewer의 전문 검독 범위·source hash·evidence digest도 함께 고정했다.

Surface partition은 다음과 같다.

| Surface | Sources |
|---|---:|
| `SCHOLARLY_MAIN_BODY` | 33 |
| `DESIGNATED_IMPLEMENTATION_APPENDIX` | 2 |
| `PACKAGE_COMPANION` | 2 |
| `ROOT_WRAPPER` | 2 |
| `PREAMBLE` | 2 |
| `BIBLIOGRAPHY` | 2 |
| 합계 | 43 |

## 5. Citation and bibliography inventory

장별 identity를 `CH1::key`, `CH2::key`로 보존했다. 동일 key spelling을 한 global record로 합치지 않았다.

| 항목 | Ch1 | Ch2 | 합계 |
|---|---:|---:|---:|
| bibliography entry | 36 | 16 | 52 |
| active cite command | 71 | 28 | 99 |
| ordered citation-key occurrence | 96 | 34 | 130 |
| unique key spelling | 36 | 16 | global union 48 |
| cited-but-undefined | 0 | 0 | 0 |
| defined-but-uncited | 0 | 0 | 0 |

한 병렬 review는 multi-line `\cite{huggins2009, bazant2013}`와 Appendix B의 `\cite{numverif2026}`를 동시에 누락해 `98/128` 및 `CH2::bazant2013` unused를 보고했다. Frozen source의 exact parser와 Ch2 독립 전문 검독을 대조해 `99/130`, unused 0으로 확정했다. 이 충돌은 추론으로 메우지 않고 exact anchors `ch2_sec01_partition.tex:105`와 `ch2_appB_codemap.tex:53`으로 해소했다.

Cross-root duplicate spelling은 `bazant2013`, `dahn1991`, `ohzuku1993`, `reynier2003` 네 개다. 각 root occurrence를 유지하고 alias collapse는 0이다.

Bibliography delta는 `UNCHANGED/MODIFIED/NEW=35/7/10`이다. NEW bibliography occurrence 10개는 다음과 같다.

- Ch1: `ashcroftmermin1976`, `bakerverbrugge2018`, `dreyer2011`, `imada1998`, `marianetti2004`, `mott1968`, `msmr_origin2017`, `vanderven1998`;
- Ch2: `dahn1991`, `ohzuku1993`.

이 가운데 genuinely new source identity는 Ch1의 8개뿐이다. Ch2의 두 occurrence는 old Ch1 corpus에 이미 존재하므로 `NEW_ROOT_OCCURRENCE_EXISTING_IDENTITY` alias로 분류하며 신규 외부 검증 debt를 중복 생성하지 않는다. Identity 판정은 key와 첫 DOI만 보지 않고 v1.0.19 전체의 global key spelling, 모든 DOI token, key를 제거한 normalized metadata fingerprint를 독립 대조한다.

DOI-like occurrence는 47, normalized unique token은 40이다. Entry primary DOI가 있는 record는 44, 없는 record는 8이며 annotation cross-reference DOI는 3 occurrence다. 첫 DOI와 annotation DOI를 분리해 `ENTRY_PRIMARY_IDENTIFIER`와 `ANNOTATION_CROSS_REFERENCE`로 기록했다. 모든 token은 metadata string inventory일 뿐 검증된 DOI가 아니다.

Mixed-style key `msmr_partI`, `msmr_partII` 두 개는 보존했으며 자동 rename하지 않았다.

## 6. Equation inventory and authority

Source text의 display는 175개다.

- environment block: Ch1 128 + Ch2 32 = 160;
- bracket display `\[...\]`: Ch1 7 + Ch2 8 = 15;
- 합계: Ch1 135 + Ch2 40 = 175.

Step 48 snapshot의 equation-block denominator 160은 bracket display 15개를 포함하지 않는다. 따라서 snapshot `160`과 source-text display `175`를 같은 분모로 쓰지 않는다.

Textual delta는 `UNCHANGED/MODIFIED/NEW=168/1/6`이다. 신규/변경 식은 다음과 같다.

| Identity | Text delta | Authority class | Derivation state |
|---|---|---|---|
| `eq:sm-baresum` | NEW | newly introduced background relation | self-contained bounded derivation; external support unverified |
| `eq:sm-baremid` | NEW | newly introduced background relation | self-contained bounded derivation |
| `eq:sm-bare` | NEW | algebraic restatement | preceding numerator/denominator reduction |
| `eq:sm-exch` | NEW | newly introduced background relation | assumptions stated; external support unverified |
| `eq:sm-fdbe` | NEW | newly introduced background relation | BE convergence condition stated; external support unverified |
| `eq:lco-mottcrit` | NEW | newly introduced background relation | `W≈2zt` derivation/model scope `GROUND_NOT_FOUND` |
| `eq:lco-slots` | MODIFIED text | unchanged source model | mathematical content unchanged; explanatory cross-reference only |

새 governing relation로 승격한 식은 0이다. `eq:lco-mottcrit` 뒤의 citation adjacency는 특정 계수 관계를 증명하지 않는다. 모든 equation row에서 `hash_is_scientific_validity=false`다.

## 7. Background claims and source attribution

Exact v1.0.19→v1.0.20 changed-line segments에서 237 prose candidate를 추출했다.

- `BACKGROUND_CLAIM=230`;
- designated Appendix B의 `IMPLEMENTATION_ONLY=6`;
- `NON_CLAIM=1`.

보수적으로 분류한 230개 background candidate 각각에 authority row를 만들었다. Source-attribution statement는 226개이며 delta는 `UNCHANGED/NEW/MODIFIED=168/43/15`다. NEW/MODIFIED statement 58개 모두 old anchor 또는 exact delta segment, statement identity와 독립 authority row를 가진다. 한 문장에 cite key나 내부 source 표현이 있어도 proposition-level support는 `UNVERIFIED_EXTERNAL`이다.

주요 bounded gap은 다음과 같다.

- Ch1 `eq:lco-mottcrit`의 `W≈2zt` heuristic은 lattice/dispersion/model 조건과 유도가 없다;
- Ch1 config/electronic coupling residual의 gate/width 흡수는 명시적 leading-order 가정이나 독립 근거는 없다;
- Ch2의 새 `약 0.3 mV` rounded-center discrepancy는 citation, 계산 절편, standalone machine provenance가 없다;
- LCO optical phonon 50–80 meV, graphite `ΔS_e≈0`, LCO MIT/`g(E_F)` 변화, reversible branch-average 식, two-phase `w_j(T)` law의 primary anchor는 여전히 `GROUND_NOT_FOUND` 또는 `UNVERIFIED_EXTERNAL`이다;
- `numverif2026`은 internal self-report이며 외부 문헌도 독립 machine provenance도 아니다.

## 8. Code-free main-body audit

허용된 TeX surface는 exact full path `Claude/docs/v1.0.20/_sections/ch1_appB_codemap.tex`, `Claude/docs/v1.0.20/_sections/ch2_appB_codemap.tex` 두 개뿐이다. Comments와 preamble definition, `\code{eq:...}` equation-label 표기는 code leakage로 세지 않았다.

그 결과 허용 부록 밖 rendered source에서 14개 confirmed policy violation anchor를 기록했다.

- Ch1 10개: intro 19; n0n1 38; center 68; lag 125; sum 18/47; LCO center 105; inputs 29/36/66;
- Ch2 4개: App A 8; bibliography 20; Einstein 96; synthesis 95.

따라서 v1.0.20 source baseline의 code-free 상태는 `NONCOMPLIANT_V1020_SOURCE_BASELINE`이다. 이번 audit는 `Claude/**`를 수정하지 않으며, canonical manuscript 작성 시 Phase 072 경계에서 본문 표현을 제거하고 designated implementation appendix/companion으로만 이동해야 한다.

Ch2 root comment의 “구현 개정 완료”와 Appendix B의 “이후 개정 요구”는 process-state contradiction이다. Comment는 rendered scholarly claim이 아니지만 완료 근거로 사용할 수 없다.

## 9. Authority rows and carry-forward

Authority row는 총 782개다.

| Asset type | Rows |
|---|---:|
| `BIB_ENTRY` | 52 |
| `CITATION_OCCURRENCE` | 99 |
| `EQUATION` | 175 |
| `BACKGROUND_CLAIM` | 230 |
| `SOURCE_ATTRIBUTION_STATEMENT` | 226 |

New/modified 자산 347개는 authority row `347/347`를 갖는다. 여기에는 원래 집계 289개와 NEW/MODIFIED source-attribution statement 58개가 포함된다. Orphan authority row, duplicate asset ID, unsupported scientific promotion은 0이다.

Phase 060 carry delta에서 inherited 52건과 신규 blocker 5건을 source-record digest와 함께 projection했다. `status`, `target`, `acceptance`, `resolution`, external truth flag는 하나도 바꾸지 않았다. 52건은 모두 `NOT_RESOLVED`, acceptance satisfied 0이며 5 blockers는 모두 `OPEN`이다.

Step 49의 신규 Phase 071 debt는 v1.0.20에서 genuinely new인 bibliography identity 8개에 대해서만 만들었다. Ch2의 new root occurrence 2개는 old Ch1 corpus에 이미 존재하는 alias이므로 별도 debt를 만들지 않았다. 기존 source identity에서 새로 발견한 gap은 finding/GNF로 연결했지만 별도 carry blocker로 중복 생성하지 않았다.

## 10. Validation

TDD RED는 builder/matrix/result 부재를 `FAIL_P061_STEP49_CITATION_AUTHORITY`로 먼저 확인했다. Builder 생성 뒤 byte check를 반복해 stored matrix와 재생성 bytes가 일치함을 확인했다.

최종 validator가 강제하는 범위는 다음과 같다.

- strict duplicate-key/nonfinite JSON rejection 및 full recursive traversal;
- frozen Git blob에서 bibliography/citation/equation inventory 독립 재구성;
- chapter-scoped identity, multi-line citation, primary/annotation DOI 역할, source/snapshot equation denominator 분리;
- 782 authority row 및 new/modified 347/347 coverage;
- inherited 52 + 5 exact-state preservation, genuinely new identity debt 8개와 existing-identity alias 2개;
- 외부 권위·review·rationale·hash promotion 금지;
- code-free confirmed violation 14개와 designated allowlist 2개;
- frozen blob에서 bibliography/citation/equation/prose/attribution/code/companion semantic projection 독립 재구성, 782 authority row와 원천 자산의 exact bijection;
- 모든 nested JSON keyset/type의 schema fingerprint, builder LF-normalized SHA, Python 3.12/3.14 공통 canonical AST pin과 `git cat-file --batch` 단일 read-only subprocess 계약;
- singleton diagnostic을 강제하는 required negative controls 36개와 deterministic rebuild 2개;
- exact-seven staging, parent/subject/path, push/remote persistence, protected/main/Claude non-change.

Final precommit validator 결과는 Python 3.12와 system-default Python 3.14 양쪽에서 required singleton-diagnostic negative controls `36/36`, strict duplicate-key/nonfinite controls `2/2`, deterministic rebuild/stored equality `2/2`, matrix full traversal `51,653` nodes / maximum depth 6으로 PASS다. 두 runtime의 canonical builder AST SHA도 동일하다. `git diff --check`도 통과했다. 이 문서 작성 시점의 containing commit hash는 자기 commit 전이므로 `PENDING_AT_PRECOMMIT_BY_DESIGN`이다.

## 11. Exact-seven checkpoint

Step 49 exact-seven은 다음 파일만 포함한다.

1. `Codex/work/v1020_phase061/build_phase061_step49_citation_authority.py`
2. `Codex/work/v1020_phase061/validate_phase061_step49.py`
3. `Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json`
4. `Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md`
5. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Subject는 정확히 `audit(phase061): bound v1020 citation authority`다. Exact-seven commit·push·live-origin 검증과 `PASS_P061_STEP49_PERSISTENCE`가 끝나기 전 Step 50은 시작하지 않는다.

## 12. Next

Step 50은 figure competition, multi-review와 artifact audit를 소유한다. Step 49 persistence 전에는 `Step 50 blocked until persistence`다.
