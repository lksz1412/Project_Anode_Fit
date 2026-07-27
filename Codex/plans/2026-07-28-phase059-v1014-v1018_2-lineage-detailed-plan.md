# Phase 059 v1.0.14–v1.0.18.2 계보 재감사 세부 계획

정본일: 2026-07-28

상위 계획:
`Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.json`

상위 Steps: 33–39

기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

선행 gate: `PASS_P058_LINEAGE_A`

## 목적

v1.0.14, v1.0.15, v1.0.16, v1.0.17, v1.0.18.1과
v1.0.18.2의 이론 source, code, test, demo, guide, handover,
PDF, image와 golden data를 전수 재감사한다. frozen source에는
독립된 `v1.0.18` directory가 없으므로 존재하지 않는 중간판을
추정하지 않는다.

핵심 질문은 다음과 같다.

1. v1.0.14의 문건 정련과 phase-separation appendix가 Phase 058의
   nonideal·two-phase blocker를 실제로 닫았는가
2. v1.0.15의 점별 연속 메모리 적분이 grid switch를 제거하면서
   보존식, \(L_V\to0\), 방향과 이력 계약을 올바르게 유지했는가
3. v1.0.16의 \(n(T)\)가 물리적 폭 모형인지 empirical fit 확장인지,
   entropy derivative와 식별 가능성이 닫혔는가
4. v1.0.17과 v1.0.18.1의 doc-only 정련이 새 물리 검증으로
   과대 계수됐는가
5. v1.0.18.2의 Einstein vibrational term이 열역학적으로 맞고
   문건·코드·시험에 같은 quantity로 구현됐는가
6. v1.0.14–v1.0.18.2가 사용자의 저온·유한전류 peak suppression/
   broadening과 local barrier 직관을 실제로 얼마나 진전시켰는가
7. graphite, Si, graphite–Si와 doped high-voltage LCO의 공개
   실험 데이터 fit이라는 최종 목표에 어떤 근거를 추가했는가

## 동결된 범위

- version paths: 117
- unique blobs: 93
- duplicate path occurrences: 24
- unique full-text blobs: 63
- unique full-text lines: 36,641
- unique PDF blobs: 18, total 492 pages
- unique image blobs: 10
- unique binary-data blobs: 2

역할별 unique blob:

| 역할 | 수 |
|---|---:|
| theory | 17 |
| code | 4 |
| test | 12 |
| demo | 18 |
| implementation guide | 3 |
| result/handover | 8 |
| supporting document | 1 |
| PDF | 18 |
| image | 10 |
| binary data | 2 |

version directory별 path 수:

| version | paths |
|---|---:|
| v1.0.14 | 19 |
| v1.0.15 | 19 |
| v1.0.16 | 20 |
| v1.0.17 | 19 |
| v1.0.18.1 | 19 |
| v1.0.18.2 | 21 |

## 선행 판정의 적용 규칙

Phase 058의 11 assets, 13 repair blockers, 5 new-scope blockers와
5 evidence debts를 입력 register로 사용한다. 그러나 후속 version이
해결했다고 미리 가정하지 않는다.

- 같은 식·code blob의 copy는 새 검증으로 세지 않는다.
- 문건 설명 수정과 executable behavior 수정을 분리한다.
- bit-exact golden, round trip과 그림 생성은 internal consistency로만
  인정한다.
- default 부재로 legacy output이 유지되는 additive capability는
  material validation으로 승격하지 않는다.
- “완결”, “물리 오류 0”, “PASS”와 외부 리뷰 수용은 actual
  source·수치·문헌·데이터 근거로 재판정한다.
- 최종 이론 본문에는 물리·화학만 두고 구현 추적은 별도 conformance
  artifact에 둔다는 사용자 경계를 적용한다.

## 산출물

- `Codex/results/PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json`
- `Codex/results/PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json`
- `Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json`
- `Codex/results/PHASE_059_CODE_BEHAVIOR_MATRIX.json`
- `Codex/results/PHASE_059_TEST_DEMO_CLAIM_MATRIX.json`
- `Codex/results/PHASE_059_ARTIFACT_RENDER_AUDIT.md`
- `Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json`
- `Codex/results/PHASE_059_V1014_V1018_2_LINEAGE_REPORT_B.md`
- `Codex/results/PHASE_059_VALIDATION.json`

작업 스크립트와 렌더 중간물은
`Codex/work/v1014_v1018_2_phase059/` 아래에만 둔다.

## Step 33 — source queue·theory 전문 검독

### 33.1

Phase 056 manifest에서 여섯 version directory의 117 paths/93 unique
blobs를 content-addressed queue로 추출한다. 24 duplicate occurrence를
동일성과 version별 위치 양쪽으로 보존한다.

### 33.2

63 unique text blobs 36,641행을 연속 chunk로 전량 읽고 SHA, line
range, EOF와 read status를 기록한다. 대화 요약이나 handover만으로
전문 검독을 대체하지 않는다.

### 33.3

17 unique theory blobs의 section, equation environment, label,
definition과 bibliography index를 만든다. v1.0.13→14와 각 후속판의
exact text diff를 저장한다.

### 33.4

좌표, 상분리, 폭, memory kernel, \(n(T)\), entropy/heat,
Einstein vibration과 LCO electronic 항의 symbol·unit·sign·assumption
contract를 추출한다.

### 33.5

guide, handover, closing과 roadmap의 완료·권위·이월 claim을 source
patch와 연결한다. external reviewer와 과거 agent 판정을 과학적
근거로 자동 승계하지 않는다.

## Step 34 — code·test·demo·golden 감사

### 34.1

6개 version code path/4 unique production blob을 전문 검독한다.
public API, state, default, call graph와 AST exact diff를 만들고
v1.0.16=v1.0.17=v1.0.18.1 동일 blob을 별도 진전으로 세지 않는다.

### 34.2

test 12개와 demo 18개 unique blob을 전문 검독한다. 모든 assertion,
tolerance, printed-only check, golden path, import path와 미검사
branch를 claim matrix에 기록한다.

### 34.3

원본을 수정하지 않고 legacy test/demo를 version별 격리 실행한다.
경로·dependency 문제, 실행 PASS, report-only와 scientific gate를
서로 다른 상태로 기록한다.

### 34.4

독립 probe로 최소 다음을 검산한다.

- pointwise memory integral의 normalization과 capacity conservation
- \(L_V\to0\) equilibrium limit와 작은 \(L_V\) 연속성
- charge/discharge mirror, traversal order와 history dependence
- C-rate/Ah/C unit contract와 \(I\to0\) limit
- \(n(T)\), \(w(T)\), \(\partial w/\partial T\)와 entropy chain
- width parameter positivity, default shadowing과 identifiability
- Einstein \(S_\mathrm{vib}\), free/internal-energy relation,
  low/high-\(T\) limits와 numerical stability
- LCO electronic \(T\) dependence, interaction/barrier와 rate path

### 34.5

2 unique golden NPZ의 모든 key·shape·dtype·array를 해당 code로
재생성해 bit-exact와 tolerance match를 분리한다. v1.0.15의 deliberate
rebaseline은 이전 결함 은폐 여부와 새 architecture 검증 범위를 함께
기록한다.

## Step 35 — PDF·image·artifact 계보

### 35.1

18 PDF 492 pages를 전 페이지 render하고 blank, glyph, font,
overfull, crop, clipped equation/table/figure와 label-page 관계를
기계·시각 검독한다.

### 35.2

10 standalone image를 원해상도로 검독해 축, 단위, legend,
temperature/current, sign, peak morphology와 생성 source를 기록한다.

### 35.3

PDF/image/golden의 blob과 생성 code·TeX·Git commit을 연결한다.
copy-forward, stale artifact, version-label mismatch와 non-bit-exact
rerender를 현재 과학 증거에서 분리한다.

## Step 36 — v1.0.14 재판정

### 36.1

v1.0.14의 textbook register, derivation restructuring, width budget와
theory-only 본문 경계 개선을 v1.0.13과 exact diff로 판정한다.

### 36.2

phase-separation appendix의 regular solution, spinodal,
Cahn–Hilliard, gradient coefficient와 mobility 식을 독립 재유도한다.
단위, stability criterion, linearization과 boundary condition을
검산한다.

### 36.3

appendix의 two-phase 이론이 본문의 bell kernel, transition capacity,
hysteresis reduction factor와 production path에 실제 연결됐는지
판정한다. 별도 보류 문건은 구현된 closure로 세지 않는다.

### 36.4

LCO transition 재배치, MIT anchor, Sommerfeld \(T\) dependence와
high-voltage/doping 주장의 문건–code–test–artifact 정합을 판정한다.

### 36.5

다수 review round의 “수렴”, “물리 오류 0”, “완주” claim을 actual
remaining blocker와 대조한다.

## Step 37 — v1.0.15–v1.0.16 재판정

### 37.1

v1.0.15 pointwise continuous-memory 식을 독립 유도하고 기존
grid-switch와 수치·극한 비교한다.

### 37.2

점별 구현의 방향, 초기 조건, 유한 voltage window, integration
tail, mirror branch, scalar/vector behavior와 golden rebaseline을
검산한다.

### 37.3

v1.0.15 Ch2 heat 상세화가 새 물리인지 worked explanation인지,
문건과 code quantity가 일치하는지 판정한다.

### 37.4

v1.0.16 \(n(T)=n_0+n_1(T-T_\mathrm{ref})\) 확장을 empirical
width law와 microscopic physics로 분리한다. \(\partial w/\partial T\),
entropy propagation, positivity와 parameter correlation을 검산한다.

### 37.5

다온도·rate-series 없이 \(n(T)\), activation, LCO electronic와
vibrational 항을 동시에 식별할 수 있는지 structural/practical
identifiability 관점에서 판정한다.

## Step 38 — v1.0.17–v1.0.18.2 재판정

### 38.1

v1.0.17의 doc-only claim과 citation 정정을 exact diff로 확인한다.
새로 물리적 권위에 사용된 핵심 문헌은 DOI resolver, publisher 또는
원 논문 등 primary source로 서지와 적용 범위를 확인한다.

### 38.2

v1.0.18.1이 v1.0.17의 물리 무변경 이월판인지 theory/code/test/PDF
전 축에서 판정한다. 표현·조판 정련을 새 물리 검증으로 세지 않는다.

### 38.3

v1.0.18.2 Einstein oscillator의 partition function, free energy,
internal energy와 entropy를 독립 재유도한다. reference subtraction,
low/high-\(T\) asymptote, sign과 per-mole normalization을 검산한다.

### 38.4

`theta_E` 부재 bit-exact, `theta_E` 활성 branch, derivative round
trip과 full-path coupling을 검사한다. additive capability와 graphite
material default/fit을 분리한다.

### 38.5

`ROADMAP_future_physics.md`의 interaction composition dependence,
Cahn–Hilliard hysteresis, Butler–Volmer concentration polarization,
PSD/nano와 데이터 이월을 implemented/theory-only/new-scope로
전건 분류한다.

## Step 39 — 종합 판정과 gate

### 39.1

모든 theory claim을 `PRESERVE`, `CORRECT`, `SUPERSEDE`,
`EMPIRICAL_ONLY`, `THEORY_ONLY`, `REJECT`, `UNVERIFIED`로 처분한다.

### 39.2

Phase 058의 34 register item마다 v1.0.14–v1.0.18.2의
`RESOLVED`, `PARTIAL`, `UNCHANGED`, `REGRESSED`, `NEW_EVIDENCE` delta를
부여한다. 새 발견은 별도 blocker로 추가한다.

### 39.3

문건–code–test–artifact 4축 matrix를 닫고 각 internal PASS가
external material validity에서 제외하는 범위를 기록한다.

### 39.4

후속 Phase 060–069로 넘길 carry-forward asset, repair blocker,
new-scope blocker와 evidence debt를 acceptance criterion과 함께
갱신한다.

### 39.5

queue/coverage, equation/behavior/test matrix, render audit,
blocker delta와 lineage report를 통합 기계 검증한다.

### 39.6

`PASS_P059_LINEAGE_B`, `CONDITIONAL_P059`, `FAIL_P059` 중 하나를
판정한다.

## Gate

`PASS_P059_LINEAGE_B`는 다음을 모두 충족할 때만 부여한다.

- 117/117 path와 93/93 unique blob 처분
- 63/63 text blob 36,641/36,641행 전문 검독
- theory 17/17과 code 4/4 unique blob 전문 검독
- test 12/12, demo 18/18 전문 검독
- PDF 18/18, 492/492 pages와 image 10/10 검독
- 2/2 binary data blob의 모든 array 처분
- v1.0.14–v1.0.18.2 actual copy/patch/rebaseline 계보 연결
- pointwise memory, \(n(T)\), phase separation과 Einstein term의
  독립 단위·부호·극한 검산
- Phase 058 blocker 전건 delta routing
- 핵심 신규 문헌 claim의 primary-source 확인
- 미검증 external validity를 PASS 의미에서 제외
- `Claude/` 원본 무변경

## Stop conditions

- source가 없는 `v1.0.18` 중간판을 추정해야 함
- 원래 test 실행을 위해 legacy source 수정이 필요함
- golden rebaseline의 이전·이후 생성 관계를 확인할 수 없음
- primary source 없이 재료 parameter 또는 문헌 귀속을 확정해야 함
- appendix의 이론 존재를 production implementation으로 오인해야 함
- additive capability를 public-data material validation으로
  오인해야 함

## 실행 기록

### 2026-07-28 — Step 33.1

- Phase 056 frozen manifest에서 여섯 version directory를 추출해
  117 paths/93 unique blobs의 content-addressed queue를 생성했다.
- duplicate path occurrence 24개를 unique blob과 version별 occurrence
  양쪽으로 보존했다.
- 전문 검독 대상은 63 unique text blobs/36,641행/158 chunks다.
- unique 역할 수는 theory 17, code 4, test 12, demo 18,
  guide 3, result 8, supporting document 1, PDF 18, image 10,
  data 2로 동결했다.
- 독립 `v1.0.18` directory가 frozen manifest에 없음을 검증하고,
  v1.0.18.1과 v1.0.18.2만 scope에 포함했다.
- 9개 frozen-scope validation이 모두 통과했다.
- 근거:
  `Codex/results/PHASE_059_AUDIT_QUEUE_RESULT.md`,
  `Codex/results/PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json`,
  `Codex/results/PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json`.
- gate:
  `PASS_P059_AUDIT_QUEUE`.
- 다음은 Step 33.2 63개 text blob 36,641행을 연속 chunk로 전문
  검독하고 coverage를 닫는다.

### 2026-07-28 — Step 33.2

- 63/63 unique text blob, 36,641/36,641행과 queue-defined
  158/158 contiguous chunk를 SHA·UTF-8·byte size·line count·EOF
  기준으로 전문 검독했다.
- 역할별로 theory 17, production code 4, test 12, demo 18,
  fitting guide 3, result/handover/closing 8, supporting roadmap 1을
  모두 `COMPLETE`로 닫았다.
- v1.0.14 신규 source 전문과 v1.0.15–v1.0.18.2의 exact
  copy/patch diff를 함께 읽어 copy-forward를 새 물리 진전으로
  세지 않았다.
- `CLOSING_v1.0.15.md`에서 교과서 register, 논문 깊이,
  수식 주도, theory-only 본문 경계, theory-first,
  전문 정독과 자주 저장하는 작업 규율을 복구했다.
- 후속 matrix 입력 후보로 two-phase 현상론적 폭과 Ch2
  configurational entropy의 의미 충돌, local barrier의 affinity
  동결, direct `L_V`의 \(I\to0\) 위반, LCO theory/code 불일치,
  \(n(T)\) default derivative 불일치와 Einstein reaction-spectrum
  미정의를 기록했다.
- test/demo는 v1.0.14 이후 계산·assertion 로직 변화 없이
  version/import/output 문자열만 바뀌어 pointwise memory,
  \(n(T)\)와 Einstein term을 새로 검증하지 않음을 확인했다.
- 15/15 read-only coverage validation을 통과했다.
- 근거:
  `Codex/results/PHASE_059_TEXT_SOURCE_REVIEW.md`,
  `Codex/results/PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json`,
  `Codex/work/v1014_v1018_2_phase059/mark_phase059_text_coverage.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_text_coverage.py`.
- gate:
  `PASS_P059_TEXT_COVERAGE`.
- 이 PASS는 source 전문 검독 완료만 뜻하며 물리 타당성, 공개
  데이터 fit, PDF/image/golden 또는 최종 lineage 승인을 뜻하지
  않는다.
- 다음은 Step 33.3 theory 17 blob의 structure/equation/label/
  definition/bibliography index와 exact source diff를 생성한다.

### 2026-07-28 — Step 33.3

- 17/17 unique theory blob, 28,876행을 content-addressed source
  index에 연결했다.
- 493 sections, 973 displayed equation environments, 1,481 label
  occurrences, 635 definition cues, 252 bibliography-item occurrences와
  40 unique bibliography keys의 위치·section ownership·source
  excerpt·normalized hash를 생성했다.
- v1.0.13→v1.0.14 Ch1/Ch2, Phase 059 각 연속판 Ch1/Ch2와
  appendix의 17 exact text diff를 저장했다.
- 각 diff에 endpoint Git blob SHA, exact patch SHA-256,
  line opcode count, section add/remove와 labeled-equation
  unchanged/changed/add/remove를 기록했다.
- v1.0.15→v1.0.16 appendix가 byte-identical임을 별도
  copy-forward로 검출했다. version occurrence는 보존하지만 새
  물리 검증으로 세지 않는다.
- 두 번 연속 생성한 source index, structure summary와 lineage
  diff의 SHA-256이 같아 deterministic generation을 확인했다.
- 17/17 read-only index/diff validation을 통과했다.
- 근거:
  `Codex/results/PHASE_059_THEORY_SOURCE_INDEX.json`,
  `Codex/results/PHASE_059_THEORY_SOURCE_STRUCTURE_INDEX.md`,
  `Codex/results/PHASE_059_THEORY_LINEAGE_DIFF.json`,
  `Codex/work/v1014_v1018_2_phase059/theory_diffs/`,
  `Codex/work/v1014_v1018_2_phase059/generate_phase059_theory_index.py`,
  `Codex/work/v1014_v1018_2_phase059/generate_phase059_theory_diff.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_theory_index.py`.
- gates:
  `PASS_P059_THEORY_SOURCE_INDEX`,
  `PASS_P059_THEORY_EXACT_DIFF`,
  `PASS_P059_THEORY_INDEX_AND_DIFF`.
- 이 PASS들은 source structure와 exact lineage만 뜻한다.
  equation의 물리 타당성, 참고문헌 실재·귀속과 code conformance는
  아직 부여하지 않는다.
- 다음은 Step 33.4 coordinate, phase separation, width, memory,
  \(n(T)\), entropy/heat, Einstein vibration과 LCO electronic
  symbol·unit·sign·assumption contract를 추출한다.

### 2026-07-28 — Step 33.4

- coordinates 5, phase separation 5, width 5, pointwise memory 6,
  \(n(T)\) 3, entropy/heat 5, Einstein vibration 3,
  LCO electronic/high-voltage 6의 8 topic/38 source-linked
  contract를 생성했다.
- 각 contract에 symbol, intended quantity, unit,
  sign/orientation, assumptions, source claim, provisional
  disposition, closure state, required action과 exact source
  anchor를 기록했다.
- disposition은 PRESERVE 13, CORRECT 13, EMPIRICAL_ONLY 9,
  THEORY_ONLY 1, REJECT 1, UNVERIFIED 1이다.
- 다음 highest-impact blocker를 명시적으로 보존했다:
  C-rate/Q-cell 단위, protocol sign의 equilibrium 오염,
  two-phase phenomenological width와 ideal config entropy 충돌,
  local affinity 동결, direct \(L_V\) zero-current limit,
  다온도 항 식별 가능성, Einstein reaction-spectrum 정의,
  doped high-voltage LCO 범위.
- `P059-CON-020`의 전이당 동결 affinity는 사용자의 local
  voltage-dependent barrier 출발점과 양립하지 않으므로
  `REJECT`로 판정했다.
- 19/19 source-anchor/field/blocker validation을 통과했다.
- 근거:
  `Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json`,
  `Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/generate_phase059_theory_contracts.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_theory_contracts.py`.
- gates:
  `PASS_P059_THEORY_CONTRACT_EXTRACTION`,
  `PASS_P059_THEORY_CONTRACTS`.
- 이 contract는 최종 theory canon이 아니라 후속 독립 유도,
  code conformance, 1차 문헌과 공개 데이터 검증을 위한 audit
  입력이다.
- 다음은 Step 33.5 guide, handover, closing과 roadmap의
  완료·권위·이월 claim을 actual source patch에 연결한다.

### 2026-07-28 — Step 33.5

- guide, handover, closing과 roadmap의 완료·검증·불변·이월 표현을
  40개 source-linked claim으로 분해했다.
- actor는 USER 10, PAST_AGENT 29, EXTERNAL_REVIEWER 1이고,
  class는 USER_REQUIREMENT 7, PROCESS_HISTORY 8, THEORY_CHANGE 5,
  IMPLEMENTATION_CHANGE 2, INTERNAL_VALIDATION 3,
  SCIENTIFIC_SCOPE 7, CARRY_FORWARD 6, EXTERNAL_REVIEW 2다.
- exact theory patch로 v1.0.15 pointwise memory, v1.0.16 \(n(T)\),
  v1.0.17 theory-body 경계 정련과 v1.0.18.2 Einstein 식 추가를
  확인했다. patch 확인은 물리 타당성·code conformance·실험
  검증을 뜻하지 않는다.
- disposition은 PRESERVE_REQUIREMENT 10, PATCH_CONFIRMED 5,
  PATCH_CONFIRMED_INTERNAL_ONLY 3, SOURCE_STATEMENT_ONLY 5,
  COPY_FORWARD_NO_NEW_VALIDATION 2, PARTIAL 3, OVERCLAIMED 3,
  CARRY_FORWARD_OPEN 8, REVIEW_INPUT_NOT_AUTHORITY 1이다.
- v1.0.18.2의 “물리판 완결”, v1.0.17의 외부 리뷰 “완전 반영”,
  Cahn--Hilliard 성장률에서 voltage-domain \(L_V\)를 직접
  근거화한다는 주장을 과장으로 판정했다.
- 외부 리뷰의 “물리 오류 0건”은 review input으로만 보존하고
  scientific authority로 승계하지 않았다.
- v1.0.17과 v1.0.18.1은 copy-forward/no-new-validation으로
  분리했고, golden·bit-exact·round-trip은 internal evidence로
  한정했다.
- 40/40 claim의 source line, frozen coverage, exact patch SHA,
  contract link와 disposition을 확인했고 26/26 validation을
  통과했다. 두 번 생성한 JSON/summary SHA-256도 동일했다.
- 근거:
  `Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json`,
  `Codex/results/PHASE_059_COMPLETION_AUTHORITY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/generate_phase059_completion_claims.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_completion_claims.py`.
- gates:
  `PASS_P059_COMPLETION_AUTHORITY_ADJUDICATION`,
  `PASS_P059_COMPLETION_CLAIMS`.
- 다음은 Step 34.1 production code 4 unique blob의 AST/public
  API/default/call graph와 exact diff를 감사한다.

### 2026-07-28 — Step 34.1

- production code 4 unique blob/6 occurrence path/3,704행을 AST로
  인덱싱했다. module constants, classes, function/method signature,
  public API, call set, transition-key access와 literal dataset을
  source hash와 함께 저장했다.
- v1.0.14→15, v1.0.15→16, v1.0.16→18.2의 3 exact code diff를
  endpoint Git blob SHA와 patch SHA-256으로 고정했다.
- v1.0.16, v1.0.17, v1.0.18.1이 하나의 동일 production-code
  blob임을 copy-forward로 분리했다.
- v1.0.15 grid removal/pointwise helper, v1.0.16 `_dwdT`,
  v1.0.18.2 Einstein helper 4개의 함수 계보를 AST/source hash로
  확인했다. 세 비교에서 graphite/LCO literal dataset hash는
  변하지 않았다.
- 정적 finding 13건을 기록했다. CRITICAL 5건은 input voltage
  sorting에 의한 chronology 소실, direct `L_V` zero-current 위반,
  cutoff affinity 동결, C-rate/Q-cell unit ambiguity,
  doped high-voltage LCO scope 부재다.
- HIGH/MEDIUM finding에는 finite-window 평형 초기화,
  default width와 `_dwdT` fallback 불일치, 비등온 kinetics의
  mean-\(T\) 축약, Einstein reference temperature 양수 guard 부재,
  LCO electronic entropy의 298.15 K 동결과 dormant Einstein
  capability가 포함된다.
- 31/31 source/AST/queue/diff/dataset/copy-lineage/finding validation을
  통과했고 두 번 생성한 모든 JSON, summary와 patch SHA-256이
  동일했다.
- 근거:
  `Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json`,
  `Codex/results/PHASE_059_PRODUCTION_CODE_DIFF.json`,
  `Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/code_diffs/`,
  `Codex/work/v1014_v1018_2_phase059/generate_phase059_code_index.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_code_index.py`.
- gates:
  `PASS_P059_PRODUCTION_CODE_INDEX`,
  `PASS_P059_PRODUCTION_CODE_EXACT_DIFF`,
  `PASS_P059_PRODUCTION_CODE_INDEX_AND_DIFF`.
- 이 gate는 static code lineage를 닫을 뿐 runtime, test adequacy,
  theory conformance나 experimental validity를 부여하지 않는다.
- 다음은 Step 34.2 test 12개/demo 18개 unique blob의 assertion,
  tolerance, printed-only check, import/golden path와 미검사 branch를
  claim matrix에 기록한다.

### 2026-07-28 — Step 34.2

- test 12개와 demo 18개, 합계 30 unique blobs/3,372행의
  assertion, comparison, exit, golden read/write, figure output,
  dynamic import path, model call과 feature token을 AST로
  인덱싱했다.
- Python `assert`는 0개다. 실패를 명시적으로 강제하는 표준
  검사는 regression verify의 current-output별 `np.array_equal`
  6건과 final exit뿐이다.
- regression의 area check는 출력만 하고 `all_ok`에 포함되지
  않는다. capture는 golden을 직접 덮어쓰며, CODE만 environment
  override가 있고 GOLD는 absolute Windows path로 고정돼 있다.
- sample test, LCO heat demo, graph suite와 plot의 finite,
  parity, area, shape와 expected-value 결과는 모두 print/figure
  전용이다. false verdict가 process failure를 만들지 않는다.
- version/path 문자열을 정규화하면 30 blobs는 sample,
  regression, graph suite, LCO heat demo, plot의 5 logic family
  × 6 releases다. 새 release별 test logic 진전은 없다.
- 전체 corpus에서 `n_T1`, `theta_E`, direct `L_V`,
  nonmonotone/reversal/pulse와 measured/experimental data token은
  0회다. Step 34.1 critical branch와 두 headline feature를
  표준 harness가 검사하지 않는다.
- finding 15건과 exact source anchor를 저장하고 34/34 validation을
  통과했다. 두 번 생성한 JSON/summary SHA-256도 동일했다.
- 근거:
  `Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json`,
  `Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/generate_phase059_test_demo_matrix.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_test_demo_matrix.py`.
- gates:
  `PASS_P059_TEST_DEMO_ASSERTION_INVENTORY`,
  `PASS_P059_TEST_DEMO_ASSERTIONS`.
- 이 gate는 test evidence가 실제로 강제하는 범위를 닫을 뿐
  runtime PASS나 물리·실험 타당성을 부여하지 않는다.
- 다음은 Step 34.3 capture를 금지한 격리 환경에서 version별
  production self-check, regression verify, sample/demo/graph/plot을
  실행하고 결과·exit·output hash를 저장한다.

### 2026-07-28 — Step 34.3

- disposable temporary directory에서 6 versions × production
  self-check/regression verify/sample/LCO demo/graph suite/plot의
  36개 process를 실행했다. `capture`는 호출하지 않았고 source
  tree와 NPZ mutation은 0이다.
- production self-check와 24 print/figure 계열 실행은 30/30
  exit 0이었다. regression verify 6개는 모두 exit 1이며
  PASS banner는 0개다.
- 각 version의 current 13 arrays와 저장 golden의 key/shape/dtype을
  별도 진단했다. exact `array_equal`은 1/13, `rtol=0`,
  `atol=1e-12`에서는 13/13이고 최대 절대차는
  \(4.33\times10^{-15}\)이다. strict bit gate의 runtime/library
  비이식성을 확인했다.
- regression이 출력하는 finite-window area ratio는 모든 version에서
  0.9363078774로 guide의 0.95 하한보다 작지만 `all_ok`와 exit에
  포함되지 않는다. 이는 무한영역 capacity identity 자체의 반증이
  아니라 현 harness window/gate의 결함이다.
- 24 generated image의 hash를 temporary directory 안에서 수집한 뒤
  폐기했다. stdout/stderr 72개를 temporary path 치환 후 저장했다.
- 결과/summary/log aggregate SHA-256은 반복 실행 전후 동일했다.
- 29/29 runtime-result/log/source/golden/no-mutation validation을
  통과했지만 strict regression 실패 때문에 status는
  `CONDITIONAL_P059_ISOLATED_RUNTIME`이다.
- 근거:
  `Codex/results/PHASE_059_ISOLATED_RUNTIME_RESULTS.json`,
  `Codex/results/PHASE_059_ISOLATED_RUNTIME_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/runtime_logs/`,
  `Codex/work/v1014_v1018_2_phase059/run_phase059_isolated_runtime.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_isolated_runtime.py`.
- 다음은 Step 34.4 독립 probe로 memory, conservation, order/history,
  current/unit, width/entropy, Einstein과 LCO electronic/barrier
  contract를 직접 검산한다.

### 2026-07-28 — Step 34.4

- frozen v1.0.14/15/16/18.2 production module을 read-only import하고
  기존 release test/demo를 호출하지 않은 독립 물리·수치 probe
  22건을 실행했다. source SHA는 실행 전후 동일하고 `Claude/`
  working tree는 clean이다.
- v1.0.15 pointwise recurrence는 불규칙 격자 상수·선형 source를
  \(5.56\times10^{-17}\), \(2.78\times10^{-17}\) 최대오차로
  재현했다. 넓은 전압창에서 평형/지연 면적은 모두 \(Q=1\)을
  \(3\times10^{-12}\) 이내로 보존했고, 지연 peak suppression과
  FWHM broadening 및 resolved \(L_V\to0\) 단조 수렴을 확인했다.
- 대칭 단일전이 charge/discharge mirror는 0 오차로 일치했다.
  반면 입력 전압을 임의 순열해도 원위치 복구 출력은 0 오차로
  동일하고, 실제 입력 순서를 따라 memory를 전개한 결과와는
  최대 21.33 차이가 났다. production `dqdv`의 voltage sorting이
  pulse/reversal/rest chronology를 제거한다.
- derived kinetics는 \(I=0\)에서 평형으로 환원되지만 direct
  `L_V`는 \(I=0\)과 \(I=1\) 출력이 같고 평형과 최대 3.903
  차이가 났다. \(Q_\mathrm{cell}=3600\) C, 1C 환산은
  SI-consistent 1 A에 비해 `func_L_q`가 정확히 3600배다.
- explicit constant \(n\), \(n(T)\), `w`-only의
  \(\partial w/\partial T\)와 entropy chain은 finite difference와
  일치했다. 그러나 `n`/`w` 부재 시 observable은 \(w=RT/F\)인데
  `_dwdT`는 0을 반환해 \(R/F=8.6169\times10^{-5}\) V/K가
  누락된다. `n`과 `w`를 함께 주면 `w`는 exact inert다.
- v1.0.18.2 Einstein pair는
  \(\partial\Delta U_\mathrm{vib}/\partial T
  =\Delta S_\mathrm{vib}/F\), \(U=F+TS\), low/high-\(T\)
  asymptote를 만족했다. 하지만 `theta_E_Tref<=0`은 fail-fast
  되지 않고 NaN으로 진행하며, shipped graphite/LCO 7개 기본
  전이에 `theta_E`는 하나도 없다.
- LCO electronic entropy는 240–360 K에서 완전히 동결되고,
  기본 LCO는 \(R_n=0\)에서 \(I=0\)과 \(I=1\) 곡선이 exact
  identical이다. 최대 중심은 4.05 V이고 dopant/oxygen-loss/
  surface state가 없다. lag resolver에도 local voltage/affinity
  인자가 없고 U를 0.08→0.28 V로 바꿔도 lag가 동일하다.
- verdict는 PASS identity 10, PASS guard 1, blocker confirmed 8,
  scope absent 2, identifiability caution 1이다. 45/45 validation과
  반복 생성 hash 동일성을 통과했다.
- 근거:
  `Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json`,
  `Codex/results/PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/run_phase059_independent_code_probes.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_independent_code_probes.py`.
- gate:
  `PASS_P059_INDEPENDENT_CODE_PROBE_EXECUTION`,
  `PASS_P059_INDEPENDENT_CODE_PROBES`.
- 위 PASS는 probe 실행·evidence validation만 뜻한다. release
  물리 정합 상태는 `CONDITIONAL_P059_CODE_CONFORMANCE`이며,
  blocker나 실험 타당성을 PASS로 승격하지 않는다.
- 다음은 Step 34.5 두 golden NPZ의 모든 key/shape/dtype/array를
  재생성해 bit-exact와 tolerance match를 분리하고 v1.0.15
  rebaseline의 검증 범위와 결함 은폐 가능성을 판정한다.
