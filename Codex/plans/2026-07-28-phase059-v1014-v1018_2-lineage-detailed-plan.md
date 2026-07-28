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

### 2026-07-28 — Step 34.5

- 6개 release의 golden NPZ occurrence를 file/member/array SHA,
  key order, shape, dtype, finite 값으로 전수 감사했다. 내용 기준
  unique golden은 v1.0.14 1개와 v1.0.15–18.2 공통 1개, 합계
  2개다. 각 archive는 float64 `(1000,)` 배열 13개이며 NaN/Inf는
  없다.
- 두 golden은 key/order/shape/dtype 13/13이 동일하다. `V`와
  `equilibrium_298` 2개는 exact same이고, 유한전류·온도·T(V)·
  facade 11개 배열은 전 원소가 바뀌었다. 최대 변화는
  \(3.9111\times10^{-5}\)다.
- Git commit `03dab9221d9b017501a1a9d391ce8825dd440106`에서
  v1.0.15 pointwise-memory code와 golden만 함께 변경됐고
  regression harness blob은 변경되지 않았다. commit 전 golden은
  v1.0.14 golden과 같고 commit 후 golden은 현재 v1.0.15–18.2
  golden과 같다.
- 저장된 golden delta와 현 runtime에서 직접 생성한 v1.0.14→15
  code output delta의 최대 불일치는 \(4.33\times10^{-15}\)다.
  따라서 rebaseline은 새 architecture의 의도된 내부 snapshot을
  다시 잡은 기록으로 보존한다.
- 현 runtime에서 각 version의 regenerated 13 arrays 중 bit-exact는
  1개지만 `rtol=0, atol=1e-12`는 13개 모두 통과하고 최대차는
  \(4.33\times10^{-15}\)다. bit-exact 이식성은 REJECT한다.
- v1.0.15와 v1.0.16/17/18.1/18.2의 13 legacy outputs는
  version별 exact 13/13 동일하다. 후속 additive feature가 default
  off라는 뜻이며 새 feature validation이 아니다.
- 6개 regression harness는 version/path 정규화 후 하나의 동일
  logic family다. `n_T1`, `theta_E`, LCO, direct `L_V`,
  nonmonotone/reversal/pulse, entropy/heat, SI 3600 case와
  measured/experimental token은 모두 0이다.
- NPZ는 공개 실험, optimizer state, covariance/uncertainty를
  포함하지 않는 `DERIVED_MODEL_OUTPUT_SNAPSHOT`이다. capture와
  verify가 같은 harness를 쓰므로 independent physical oracle이
  아니다.
- 46/46 source/hash/array/Git/rebaseline/coverage/determinism
  validation을 통과했다. status는
  `CONDITIONAL_P059_GOLDEN_NPZ`다.
- 근거:
  `Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json`,
  `Codex/results/PHASE_059_GOLDEN_NPZ_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_golden_npz.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_golden_npz.py`.
- gates:
  `PASS_P059_GOLDEN_NPZ_AUDIT_EXECUTION`,
  `PASS_P059_GOLDEN_NPZ`.
- Step 34 code/test/demo/golden 감사는 완료됐다. 다음은 Step 35.1
  18 PDF 492 pages를 전 페이지 render해 blank, glyph, font,
  overfull, crop, clipped equation/table/figure와 label-page 관계를
  기계·시각 검독한다.

### 2026-07-28 — Step 35.1

- 18 PDF 492 pages를 96 dpi PNG로 전수 render했고 manifest page
  count와 492/492 일치했다. invalid render, blank candidate,
  crop/media 불일치, edge-touch/near-edge candidate,
  page-boundary 밖 char/word는 모두 0이다.
- 37 contact sheets를 전부 육안 검독하고, 최고 밀도·최소 우측
  여백·NUL 집중 수식·표/그림·마지막 참고문헌을 대표하는 13쪽을
  원해상도로 재검독했다. 가시적 글리프 누락, overfull,
  equation/table/figure clipping은 찾지 못했다.
- 18/18 PDF의 모든 font는 embedded다. 그러나 전 PDF의 CMEX10과
  Chapter 1의 CMSY10 일부에 ToUnicode map이 없어 pypdf text
  extraction에서 NUL 3,117자가 발생한다. 원해상도에서는 해당
  bracket/symbol이 보이므로 display 결함이 아니라 검색·복사·
  접근성 evidence debt로 분류한다.
- 등록된 named destination은 모두 유효 page를 가리키고 본문의
  unresolved `??` marker는 0이다. 반면 각주 복귀용
  `Hfootnote.*` GoTo link 26개는 PDF name tree에 target이 없어
  `LINK_DEFECT`로 판정했다.
- v1.0.16 appendix TeX는 v1.0.15와 exact-identical이고 8개
  rendered page hash도 모두 동일하다. 표지에 `버전 1.0.15 초안`이
  남아 있으므로 v1.0.16의 새 appendix evidence로 세지 않는다.
- render audit 재실행 전후 metrics/visual/report SHA가 각각
  동일했고 validator 41/41을 통과했다.
- 근거:
  `Codex/results/PHASE_059_PDF_RENDER_METRICS.json`,
  `Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json`,
  `Codex/results/PHASE_059_ARTIFACT_RENDER_AUDIT.md`,
  `Codex/work/v1014_v1018_2_phase059/render_audit_phase059_pdfs.py`,
  `Codex/work/v1014_v1018_2_phase059/finalize_phase059_pdf_visual_review.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_pdf_render.py`.
- status:
  `CONDITIONAL_P059_PDF_RENDER_PASS_WITH_ACCESSIBILITY_AND_PROVENANCE_DEBTS`.
  이 status는 조판·link·provenance 판정이며 식의 물리 타당성,
  문헌 진실성, code conformance 또는 실험 타당성을 승인하지 않는다.
- 다음은 Step 35.2의 10 standalone image 원해상도 감사다.

### 2026-07-28 — Step 35.2

- Phase 059의 24 image path occurrence를 content-addressed로 묶은
  10 unique PNG를 원해상도로 전부 육안 검독했다. 10/10이 정상
  decode되고 queue 및 occurrence blob mismatch는 0이다.
- 네 image family(P4 LCO/heat, graph suite, sample test,
  dQ/dV bell shapes)는 모두 code-generated synthetic model
  output이다. 관측값, residual, uncertainty, data citation이 있는
  experimental evidence는 0/10이다.
- 두 unique P4 image의 panel (c) title이 우측 canvas에서 잘리고,
  이 결함은 6 version occurrence에 전파된다.
- `anode_fit_v1_0_14_dqdv.png`는 보이는 title과 generator가
  v1.0.16인데 filename만 v1.0.14이며, 같은 blob이 v1.0.16–
  v1.0.18.2의 4개 경로에 copy-forward됐다.
- P4/graph-suite/bell-shape의 dQ/dV 단위, graph-suite의
  entropy-parity/charge 단위, sample figure의 `|I|` 단위가
  불완전하다.
- equilibrium temperature series는 저온에서 RT/F width가 작아져
  peak가 더 높고 좁다. 저온×유한전류 joint sweep은 없으므로
  사용자가 관찰한 저온 finite-current peak suppression/broadening을
  입증하지 않는다.
- Si, graphite+Si, doped high-voltage LCO, 4.15 V 초과 구간,
  experimental overlay는 모두 없다. 자유 width로 네 peak를
  분리한 그림과 내부 항등성 그림은 phase/material identification
  또는 실험 validation으로 승격하지 않는다.
- 감사 script를 재실행해 audit JSON/report hash가 동일함을 확인했고
  validator 28/28을 통과했다.
- 근거:
  `Codex/results/PHASE_059_IMAGE_AUDIT.json`,
  `Codex/results/PHASE_059_STANDALONE_IMAGE_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_images.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_images.py`.
- status: `CONDITIONAL_P059_SYNTHETIC_IMAGE_EVIDENCE`.
  이 status는 decode·shape·metadata·provenance 검독 결과이며
  물리 mechanism, 재료 identity, parameter, 문헌 또는 실험
  타당성을 승인하지 않는다.
- 다음은 Step 35.3에서 PDF/image/golden blob을 생성 code·TeX·
  Git commit과 연결하고 isolated rerender를 수행하는 일이다.

### 2026-07-28 — Step 35.3

- PDF 18, PNG 24 occurrence/10 unique, golden NPZ 6 occurrence/
  2 unique, 총 48 artifact occurrence와 30 unique content의
  current blob, 최초 도입 commit, 마지막 변경 commit, 대응
  TeX/generator/model/test commit을 연결했다.
- PDF 18개는 byte hash로 모두 다르지만 rendered-content signature는
  17개다. v1.0.15와 v1.0.16 appendix만 TeX와 8 rendered pages가
  exact-identical하며 v1.0.16 표지의 v1.0.15 label defect와
  일치한다. PDF 뒤에 TeX가 바뀐 source-after-artifact는 0개다.
- XeLaTeX는 설치돼 있으나 shared build probe가 `kotex.sty` 부재로
  중단됐고 D2Coding도 DejaVu Sans로 fallback됐다. 18 PDF의 현재
  TeX bit-exact rebuild는 `UNTESTED_DEPENDENCY_BLOCKED`이며
  재빌드 PASS를 주장하지 않는다.
- PNG 24 occurrence 중 14개는 이전 blob의 exact copy-forward이고
  filename version token과 directory가 다른 경로는 11개다.
  v1.0.16 저장 PNG 5개는 그 뒤 production model이 바뀌었으므로
  current-source candidate로는 stale다. 후속 copy가 scientific
  output까지 같은지는 plot-data array 부재로 `UNRESOLVED`다.
- Step 34.3의 disposable rerender 24개와 저장 PNG의 byte hash는
  0/24 exact다. renderer/font/backend/metadata 영향을 분리할
  numeric plot-data hash가 없으므로 byte mismatch를 곧바로 curve
  delta로 해석하지도, curve equality로 승인하지도 않는다.
- golden은 v1.0.15 이후 4개 후속 path가 같은 blob의 exact
  copy-forward다. v1.0.14와 v1.0.16 golden은 production model이
  artifact 뒤에 바뀌었다. 현재 재계산은 전 version 13/13 arrays가
  `rtol=0, atol=5e-15`에서 맞지만 bit-exact는 1/13뿐이다.
- 계보 audit/보고서 재실행 hash가 동일했고 validator 35/35를
  통과했다.
- 근거:
  `Codex/results/PHASE_059_ARTIFACT_GENEALOGY.json`,
  `Codex/results/PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_artifact_genealogy.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_artifact_genealogy.py`.
- status:
  `CONDITIONAL_P059_ARTIFACT_GENEALOGY_WITH_PDF_DEPENDENCY_BLOCK_AND_NON_BIT_EXACT_REGENERATIONS`.
  이 status는 artifact 계보만 판정하고 과학·실험 authority를
  승인하지 않는다.
- Step 35 artifact 감사는 완료됐다. 다음은 Step 36.1에서
  v1.0.14의 textbook register, derivation restructuring,
  width budget와 theory-only 본문 경계를 v1.0.13과 exact diff로
  재판정하는 일이다.

### 2026-07-28 — Step 36.1

- v1.0.13→v1.0.14 exact source diff를 Ch1/Ch2 각각 재판정했다.
  Ch1은 2,934→3,445행(+511), Ch2는 776→794행(+18)이다.
- Ch1 displayed equation은 101 unchanged, 10 changed, 5 added다.
  changed 10개 중 5개는 단일자리 대정준 분배함수, 내부 자유도
  \(q(T)\), 유효 자리 자유에너지의 실제 유도 변경이고 5개는
  code identifier를 추상 물리/연산 표기로 바꾼 경계 정리다.
  신규 5식은 \(\tilde\varepsilon\), 내부 자유도 엔트로피,
  symmetric width budget, PSD forward integral, Gibbs–Thomson
  shift다.
- Ch2는 20 equation unchanged, 2 changed, 0 added다. 두 변경은
  \(Z_1\to\Xi_1\) 대정준 표기와 Ch1의 유효 단일자리 자유에너지
  bridge 엄밀화다. 따라서 review-depth 증가는 Ch1에 집중됐고
  전체 두 장의 완결 달성을 뜻하지 않는다.
- comments와 TeX macro declaration을 제외한 rendered source에서
  구현 관련 boundary violation은 v1.0.13 두 장 합계 230행에서
  v1.0.14 24행으로 크게 줄었다. 전용 구현 부록 안에는 97행이
  모였다. 그러나 title/header/date와 본문에 `코드 진행`,
  `현재 코드`, `dict`, `self-test`, internal code artifact가
  남아 theory-only gate는 FAIL이다.
- width budget의 logistic variance
  \(\sigma_\mathrm{int}^2=\pi^2w_\mathrm{int}^2/3\), independent
  convolution variance addition, FWHM identity는 보존한다.
  반면 같은 \(w_j\)를 내재 \(n_jRT/F\)와 ensemble broadening을
  이미 흡수한 fitted effective width로 동시에 쓰면
  \(\sigma_\eta\)를 이중계산할 수 있다. 최종 문건은
  \(w_\mathrm{int}\), \(\sigma_\mathrm{ens}\), \(L_V\),
  \(w_\mathrm{obs}\)를 분리해야 한다.
- 판정 6건은 textbook asset PRESERVE, review depth PARTIAL,
  theory-only boundary FAIL, one-way theory→code PARTIAL,
  width role split CORRECT, scientific validation UNVERIFIED다.
- validator 38/38과 audit/report deterministic rerun을 통과했다.
- 근거:
  `Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json`,
  `Codex/results/PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1014_register_boundary.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1014_register_boundary.py`.
- status:
  `CONDITIONAL_P059_V1014_PEDAGOGICAL_ASSET_WITH_THEORY_BOUNDARY_AND_WIDTH_ROLE_DEBTS`.
- 다음은 Step 36.2의 regular-solution/spinodal/Cahn–Hilliard
  독립 재유도와 unit·stability·linearization·boundary-condition
  검산이다.

### 2026-07-28 — Step 36.2

- v1.0.14 `appendix_phase_separation.tex` 492행을 대상으로
  regular solution, common tangent/binodal, chemical spinodal,
  Maxwell equal-area, CNT와 Cahn–Hilliard 선형 안정성을 독립
  재유도했다.
- \(\Omega/(RT)=3\) 수치 probe에서 binodal
  0.0707202/0.9292798, spinodal 0.2113249/0.7886751,
  \(f(\xi_b)/(RT)=-0.0583413\), equal-area residual 0,
  common-tangent slope \(-6.466\times10^{-17}\)을 얻어 문건의
  정규용액 수치를 재현했다.
- 문건이 \(\kappa|\nabla\xi|^2\) convention을 택했을 때
  \(-2\kappa\nabla^2\xi\)와
  \(R=-Mk^2[f''+2\kappa k^2]\)의 factor 2는 내부적으로
  일관되며 \(k_m=k_c/\sqrt2\)도 재현됐다.
- 그러나 molar \(f\)[J/mol]를 site density 또는 molar-volume
  환산 없이 volume integral에 넣어 자유에너지 차원이 닫히지
  않는다. \(\kappa\), mobility, flux의 단위도 정의되지 않았다.
- no-flux/periodic 및 composition natural boundary가 0건이어서
  질량 보존과 자유에너지 감소를 닫을 수 없다. 최종 계약은
  \(c_s[f_m+(K/2)|\nabla\xi|^2]\), molar chemical potential,
  Onsager flux, \(M=\mathcal L/c_s\)와 두 경계조건을 함께
  정의해야 한다.
- Cahn–Hilliard(1958)와 Cahn(1961) 원 논문을 직접 대조했다.
  후자는 coherency elasticity와 composition-dependent molar
  volume이 metastability limit를 이동시킬 수 있음을 보이므로
  문건의 \(f''=0\)은 일반 고체 spinodal이 아니라
  `stress-free chemical spinodal`로 한정해야 한다.
- 정규용액/CNT/선형 안정성의 유도 자산은 조건부 보존하지만,
  dimensional closure, mobility/state closure, boundary condition은
  FAIL이고 고체 적용 범위는 CORRECT 대상으로 판정했다.
- 근거:
  `Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json`,
  `Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1014_phase_separation.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1014_phase_separation.py`.
- validator 46/46과 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1014_PHASE_SEPARATION_CORE_CORRECT_WITH_DIMENSIONAL_BOUNDARY_AND_ELASTICITY_BLOCKERS`.
- 다음은 Step 36.3에서 v1.0.14의 LCO electronic term,
  graphite/LCO sign map, heat convention과 high-voltage/doping
  scope를 독립 재유도·검산하는 일이다.

### 2026-07-28 — Step 36.3

- v1.0.14 Ch1 3,445행, Ch2 794행, production code 904행의
  LCO electronic entropy, 전위 기준, heat sign, transition map,
  doping/high-voltage 범위를 7개 1차 문헌과 독립 대조했다.
- 삽입 반응 좌표에서
  \(E=-\Delta G/F\), \(\partial E/\partial T=\Delta S/F\),
  \(\dot Q_{\mathrm{rev,gen}}=-I_{\mathrm{lith}}T\partial E/\partial T\)
  골격은 보존한다. 단 charge/discharge 문자열 대신 반응 진행과
  결합된 signed current가 필요하다.
- 문건의 가장 큰 오류는 Swiderska-Mocek 등의
  `+0.83 mV/K` intrinsic LCO single-electrode coefficient를
  `V vs Li` half-cell 기울기로 사용한 것이다. 같은 원문이 보고한
  isothermal Li|LCO half-cell 값은 `-0.25 mV/K`이므로,
  문건의 `+80.083 J/(mol K)` anchor는 실제 피팅 좌표에서
  `-24.121 J/(mol K)`로 부호까지 바뀐다.
- Sommerfeld 선도항은 검증된 금속상에서 보존하지만,
  Motohashi 원문의 `13 electrons/eV for CoO2`는 susceptibility
  차이를 Pauli 성분으로 가정해 계산한 값이다. 직접 DOS 측정이나
  `per atom` 표기가 아니며 x=0 끝점을 x≈0.85 gate에 옮기는
  tier-A 근거가 아니다.
- `dx_MIT=0.05` logistic gate는 298.15 K에서
  \(-45.678\) J/(mol K)의 중심 골을 만들지만 깊이가 \(1/dx\)에
  비례한다. 이는 선택한 폭의 model output이며 측정 anchor가
  아니다. 0.75≤x≤0.94 two-phase MIT는 phase entropy,
  coexistence composition, lever rule로 먼저 닫아야 한다.
- 문건의 \(\Delta S_e=a_eT\)로부터
  \(a_e(T^2-T_\mathrm{ref}^2)/(2F)\)를 얻는 적분 대수는 맞다.
  그러나 코드는 `x_center`와 298.15 K에서 전자항을 동결해
  composition dependence와 T² curvature를 모두 구현하지 않는다.
  268.15/298.15/328.15 K 중심 second difference는 code
  \(4.441\times10^{-16}\) V, 이론 gate 요구값
  \(-1.429\times10^{-3}\) V다.
- theory transition 3.90/4.05/4.17 V와 code
  3.93/3.88/4.049994 V가 일치하지 않으며 4.15 V 초과 code
  center는 0개다. LCO \(\Omega\), dopant variable, 실제 doped
  high-voltage profile/fit path도 없다.
- Er/Mg-doped LCO 1차 연구는 Co-site Mg가 약 4.2 V 전이를
  억제하면서 >4.45 V 산소 안정성을 악화시킬 수 있고 Li-site Er이
  산소 안정화를 담당함을 보인다. 따라서 도핑 전체를
  \(\Omega_\mathrm{pure}\to\Omega_\mathrm{dop}\) 하나로 축약하는
  일반화는 기각한다.
- `ml2024` bibliography의 실제 article/DOI는 105726이며
  v1.0.14의 105727은 오기다. 그 논문은 MIT plateau를 포착하지
  못한다고 명시하므로 electronic gate의 검증 근거도 아니다.
- 근거:
  `Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json`,
  `Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1014_lco_heat.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1014_lco_heat.py`.
- validator 52/52와 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1014_LCO_HEAT_ALGEBRA_PRESERVED_WITH_REFERENCE_DOS_GATE_CODE_AND_DOPING_BLOCKERS`.
- 다음은 Step 36.4에서 kinetics/barrier/current-broadening 사슬을
  독립 재유도하고 저온×유한전류의 peak suppression/broadening
  joint limit를 theory-code로 판정하는 일이다.

### 2026-07-28 — Step 36.4

- 실행 번호의 의미를 명시한다. 원계획 36.2의 phase-separation
  감사에서 본문 bell/transition과 appendix의 미연결까지 함께
  판정했고, LCO/heat를 실행 36.3으로 닫았다. 따라서 실행 36.4는
  사용자 출발 관측의 핵심인 kinetics/barrier/current-broadening
  joint limit 전용 단계다.
- v1.0.14 Ch1의
  \(\mathcal A\to\chi_d\to\Delta H_a^\mathrm{eff}\to
  L_q\to L_V\to\) causal tail 사슬과 production path를
  Eyring, Bazant, Fly--Chen, Gismero, Persson 2건,
  Doyle--Fuller--Newman의 7개 1차 문헌에 독립 대조했다.
- 보존 대상은
  \(\dot\xi=k(\xi_\mathrm{eq}-\xi)\),
  동일 단위계의 \(L_q=|I|/(Q_\mathrm{scale}k)\),
  국소 선형화에서 \(L_V=|dV/dq|L_q\)와 유한 \(L_V\)의
  causal suppression/broadening 정성 결과다. 이것은 reduced
  continuum limit이지 현 material closure의 검증이 아니다.
- C-rate [h\(^{-1}\)]와 Ah-style capacity를 seconds-based
  \(k_BT/h\)에 수치 그대로 결합해 \(L_q\)가 3,600배 커진다.
  298.15 K에서 동일 broadening을 맞추는 barrier gauge는
  \(RT\ln3600=20.299\) kJ/mol만큼 낮게 보인다.
  \(L_V/w=1\) 예에서 현 수치계약은 77.643 kJ/mol,
  SI 일관 계약은 97.942 kJ/mol을 요구한다.
- default \(n=1\)에서는
  \(\min(4.357nRT,4RT)=4RT\)가 항상 선택되고, 이 지점은
  peak derivative의 5%가 아니라 7.065%다. affinity가 전이당
  상수로 동결되어 구현의
  \(\partial\ln L_q/\partial V=0\)이고, local 식이라면 같은
  조건에서 \(-18.761\ {\rm V^{-1}}\)다. 사용자의
  potential-dependent barrier 가설은 실제 계산에서 사라진다.
- \(\Delta H_a^\mathrm{eff}=\Delta H_a-\chi\Omega\)는 속도만
  바꾸고 forward/reverse ratio에 regular-solution local
  chemical affinity를 복원하지 않는다. bulk Li migration
  barrier와 \(k_BT/h\)를 electrode-scale phase-fraction
  relaxation으로 승격하려면 active area, site density,
  nucleation, phase-boundary mobility, geometry와 transport의
  coarse graining이 필요하다.
- 대표 single-transition default는 258.15/298.15/318.15 K
  모두 0.1C와 1C shape가 exact-identical했다. 저온/상온
  peak-height ratio는 1.154949, FWHM ratio는 0.865839라
  저온에서 더 높고 좁다. shipped default는 사용자의
  저온×유한전류 suppression/broadening을 재현하지 않는다.
- 차원 일관 SI와 별도 mesoscopic Arrhenius rate를 둔 독립
  existence probe는 저온/상온 peak-height 0.646834,
  FWHM 1.456489를 얻어 target을 정성 재현했다. 이는 1차
  causal skeleton을 보존할 근거일 뿐 v1.0.14의 prefactor,
  barrier, frozen affinity 또는 material parameter를 승인하지 않는다.
- direct \(L_V\)는 \(I=0\)과 \(I=1\) 출력이 exact-identical하고
  \(I=0\)에서도 equilibrium과 최대 10.3291만큼 달라
  zero-current limit를 위반한다. two-grid-step branch는
  kinetic impulse area 0.770747에서 equilibrium 1로
  22.925% 불연속 점프한다.
- 더 큰 장벽/더 낮은 온도에서 \(L_q=+\infty\)가 되면 code는
  nonfinite를 \(L_V=0\)으로 바꿔 frozen-state limit를 equilibrium
  limit로 역전한다. 비등온 path도 mean \(T\)에서 lag를 한 번만
  평가하며 voltage sorting은 revisit/rest/reversal chronology를
  보존하지 않는다.
- docstring을 제외한 executable AST 대조에서 `func_L_q`,
  `_causal_lowpass`, `func_dH_a_eff`,
  `_resolve_lag_length` 4개 모두 v1.0.10과 v1.0.14가 동일하다.
  scalar-input guard와 설명 개선은 인정하되 core kinetic blocker는
  copy-forward로 판정한다.
- 근거:
  `Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json`,
  `Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1014_kinetics.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1014_kinetics.py`.
- validator 78/78과 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1014_KINETIC_SKELETON_PRESERVED_BUT_CONSTANT_CURRENT_LOCAL_BARRIER_AND_JOINT_LIMIT_FAIL`.
- 다음은 Step 36.5에서 v1.0.14의 다수 review round가 선언한
  수렴·완주·물리 오류 0 주장을 독립 blocker와 대조해 v1.0.14
  최종 권위 판정을 닫는 일이다.

### 2026-07-28 — Step 36.5

- v1.0.14 `RESULT`, handover 2개와 `V1014_*` process 문건
  32개를 권위 corpus로 다시 고정했다. 중복 제거 후 35개
  source/3,412행이며, R1--R7 review 보고서는 20개다.
- “완주”, “R2 이후 물리 실결함 0”, “코너 케이스 약 90항
  FAIL 0”, “물리·좌표 검증 완료”, build/regression/sample PASS,
  `g_max=13` tier A 유지와 이월 선언을 20개 claim으로 분해했다.
- 절차적 사실과 과학적 권위를 분리했다. v1.0.14 source·artifact
  제작, build/layout, legacy regression, review process 종료와
  교재형 자산은 보존한다. 이들은 각각 process/internal/pedagogical
  evidence일 뿐 external material validation은 아니다.
- review 발견 수 `22→13→16→8→18→13→8`은 단조 감소가 아니고,
  execution ledger는 원래의 연속 2라운드 0건 criterion을 충족하지
  않은 채 대체 근거로 종결했음을 직접 기록한다. 따라서 review
  종료는 보존하되 open-ended scientific convergence로 승격하지 않는다.
- Steps 36.1--36.4의 네 독립 blocker family를 대조했다:
  theory boundary 6 findings, phase separation 10, LCO/heat 16,
  kinetics 20으로 합계 52다.
- 좁은 `\code` macro 0건은 보존하지만 허용 절 밖 의미론적
  구현 언어 24건 때문에 theory-only 본문 완성 주장은 기각한다.
- phase-separation의 regular-solution/Cahn--Hilliard 핵심 대수와
  1차 causal relaxation 골격은 보존한다. 차원·경계조건·탄성 범위,
  기준전극·DOS gate·도핑 고전압, 3,600 단위계·frozen affinity·
  영전류/동결 극한·galvanostatic closure는 미폐쇄다.
- `13/13 bit-exact`, `ALL FINITE`, synthetic sample은 각 내부
  속성만 증명한다. v1.0.10→v1.0.14 core kinetic AST 4개가
  동일하므로 legacy regression은 inherited physics repair의
  증거가 아니다.
- v1.0.14가 직접 이월한 다온도, LCO parameter, 수치·mapping,
  primary-source 항목과 handover의 “코드 업데이트 필요” 선언은
  전역 scientific completion과 양립하지 않는다.
- 근거:
  `Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_AUDIT.json`,
  `Codex/results/PHASE_059_V1014_COMPLETION_AUTHORITY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1014_completion_authority.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1014_completion_authority.py`.
- validator 53/53과 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1014_PROCESS_COMPLETE_BUT_SCIENTIFIC_COMPLETION_AUTHORITY_REJECTED`.
- v1.0.14의 최종 위치는 폐기본이 아니라 교육적·대수적 자산과
  물리 폐쇄 결함을 함께 가진 중간 기준선이다. 이후 version의
  `PASS`는 source/code/test/data에서 blocker가 실제 닫혔을 때만
  새 권위를 얻는다.
- 다음은 Step 37.1에서 v1.0.15 pointwise continuous-memory 식을
  독립 유도하고 v1.0.14 grid-switch와 수치·극한 비교하는 일이다.

### 2026-07-28 — Step 37.1

- v1.0.15 Ch1 3,512행과 production code 895행의 pointwise-memory
  theory/code를 v1.0.14 code와 독립 비교했다.
- 진행 좌표 \(s\)의
  \(\mathrm d\xi/\mathrm ds=(\xi_\mathrm{eq}-\xi)/L\)에서
  유한 초기점 해, \(-\infty\) 자연경계 convolution,
  peak shape와 \(L\to0\) derivative limit를 다시 유도했다.
- 정규화된 지수 커널과 resolved linear-segment recurrence는
  보존한다. 불규칙 7점의 상수·선형 source 오차는 floating-point
  noise였고, 넓은 [-0.6,0.6] V 창의 지연 면적은
  0.999999999997로 Q=1을 보존했다.
- v1.0.15는 v1.0.14의 hidden `V_work`, 역보간과 22.925%
  two-grid-step handoff를 제거했다. 이는 실질적 개선이다.
- 다만 `a<1e-4` branch는 exact linear integral이 아니라
  1차 trapezoidal asymptote다. 오차는 작지만 “구간 exact”의
  전역 문구는 정정해야 한다.
- 이론은 \(-\infty\) prehistory를 적분하지만 code는 첫 점을
  `xi_lag(V0)=xi_eq(V0)`로 둔다. 동일 [-0.05,0.2] V crop을
  독립 호출하면 첫 peak 0, 넓은 과거를 유지하면 1.847424이며,
  면적은 0.923653 대 0.960601로 Q 대비 -3.6948% 편향이다.
  명시 초기 state 또는 prehistory가 필요하다.
- hidden work grid는 제거됐지만 sampling independence는 아니다.
  0.01 V와 0.0001 V 입력을 같은 좌표에서 비교하면 최대
  0.079297 차이가 난다.
- `_LAG_RESOLVE_DECAY_CAP=40`은 여전히 sampling-dependent
  branch다. 0.01 V 간격에서 경계 \(L_V=0.00025\) V를 넘을 때
  최대 1.194267, equilibrium peak의 9.554% jump가 발생했다.
  “불연속 없는 수치 가드” 주장은 기각한다.
- 단조 고정 방향의 charge/discharge mirror는 exact했다. 그러나
  code가 voltage를 정렬하므로 shuffled input을 복원한 출력은
  sorted output과 exact-identical이고, 실제 입력 순서 recurrence와
  최대 21.3296 차이다. pulse/rest/loop/reversal chronology를
  표현하지 못한다.
- derived lag path의 \(I=0\) 평형 branch는 보존한다. direct
  `L_V`는 \(I=0\)에서도 활성이고, nonfinite derived lag는
  다시 \(L_V=0\) 평형으로 뒤집힌다.
- `func_L_q`와 lag resolver executable AST는 v1.0.14와 동일하다.
  3,600 시간 단위, frozen cut affinity와 electrode-scale
  coarse-graining blocker는 수정되지 않았다.
- golden rebaseline은 새 architecture의 11개 output snapshot으로
  보존하지만 direct `L_V`, nonmonotone, reversal, pulse와
  3,600-unit contract를 검사하지 않는다.
- 근거:
  `Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_AUDIT.json`,
  `Codex/results/PHASE_059_V1015_POINTWISE_MEMORY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1015_pointwise_memory.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1015_pointwise_memory.py`.
- validator 76/76과 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1015_POINTWISE_MEMORY_CORE_PRESERVED_BUT_FINITE_WINDOW_RESOLUTION_SWITCH_AND_CHRONOLOGY_FAIL`.
- repair 방향은 normalized kernel을 monotone reduced limit로
  보존하되, 실제 protocol에는 명시 초기 state와 signed
  time/capacity integration, current/terminal-voltage closure를
  사용하고 sampling threshold 없이 평형 극한을 닫는 것이다.
- 다음은 Step 37.2에서 방향·초기조건·유한창·tail·mirror·
  scalar/vector behavior와 golden rebaseline의 구현 경계를
  종합 판정하는 일이다.

### 2026-07-28 — Step 37.2

- v1.0.15 pointwise kernel의 scalar/vector, state, finite-window
  tail, 방향, nonisothermal sampling과 golden rebaseline 경계를
  Step 37.1의 수학 판정 위에서 종합했다.
- direct \(L_V=0.02\) 단일 전이의 V=0에서 scalar와 singleton은
  평형값 12.5를 반환하지만 같은 좌표의 sweep 값은 9.657353이다.
  scalar는 과거 없는 stateless query로만 허용하며 sweep과 같은
  물리 상태라는 해석은 기각한다.
- public `dqdv`에는 initial state나 time 입력, final state 반환이
  없다. 호출마다 첫 state를 재초기화하므로 잘린 창과 연속 protocol
  사이에 상태를 전달할 수 없다.
- [-0.6,V_end] 적분 면적은 V_end=0.05/0.10/0.15/0.20/0.30/0.60 V에서
  0.788311/0.966265/0.995852/0.999546/0.999995/1.000000으로
  tail completion에 따라 달라진다. 창 밖 remaining state 회계가
  없으므로 fitting window가 전이 Q의 관측 면적을 바꾼다.
- 고정 단조 charge/discharge mirror와 같은 방향의 ascending/
  descending coordinate 복구는 exact했다. 이는 unordered curve
  mode의 자산이지 acquisition chronology가 아니다. 한 호출 내
  reversal/rest state machine은 없다.
- 같은 선형 280→320 K path도 균일 sampling은 mean T=300 K,
  저전압 집중 sampling은 291.674 K가 된다. 전이당 한 번 계산한
  lag는 0.542553→1.394176 V(2.570배), 보간 출력 최대 차이는
  0.684058이다. sample arithmetic mean T를 path kinetics로 쓰는
  closure를 기각한다.
- rebaseline commit에서 code와 golden 11/13 arrays는 함께 바뀌고
  test harness는 불변이었다. architecture output snapshot의
  traceability는 보존하고 independent oracle 권위는 기각한다.
- harness에는 direct `L_V`, nonmonotone, reversal, pulse,
  SI-Coulomb와 experimental observation이 없다. critical state,
  protocol, unit coverage는 FAIL이다.
- 최종 구현 권위는 saturated boundary를 포함한 fixed monotone
  curve의 reduced kernel로 제한한다. stateful galvanostatic
  protocol solver 권위는 없다.
- repair contract는 initial/final state, signed time/capacity,
  reversal/rest segment continuity, remaining-tail capacity,
  local T/current rate와 독립 oracle이다.
- 근거:
  `Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_AUDIT.json`,
  `Codex/results/PHASE_059_V1015_IMPLEMENTATION_BOUNDARY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1015_implementation_boundary.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1015_implementation_boundary.py`.
- validator 63/63과 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1015_MONOTONE_CURVE_KERNEL_PRESERVED_BUT_STATE_WINDOW_PROTOCOL_AND_GOLDEN_AUTHORITY_FAIL`.
- 다음은 Step 37.3에서 v1.0.15 Ch2 heat 상세화가 새 물리인지
  worked explanation인지, 문건과 code가 같은 열역학 quantity를
  쓰는지 판정하는 일이다.

### 2026-07-28 — Step 37.3

- v1.0.14→v1.0.15 Ch2 exact diff(+99/-7)를 분류하고
  `func_U_j`, graphite/LCO entropy seam, `entropy_coefficient`,
  `reversible_heat`, `irreversible_heat`의 실행 AST를 대조했다.
  여섯 heat-path AST가 모두 동일하므로 주된 추가분은 새 열물리
  구현이 아니라 worked explanation이다.
- 상수 \(n\), \(w=nRT/F\)에서 전하보존 음함수를 독립 미분했다.
  고정 탈리튬화 분율에서 중심 엔트로피와 config 항의
  \(Q_jg_j\) 가중식이 복원되고, \(T\)-동결 폭에서는 config 항이
  사라져 중심값 가중식으로 환원된다.
- \(\bar x=0.25\), 298.15 K에서 독립 bisection은
  \(U_{\rm oc}=74.351141\) mV,
  \(\partial U/\partial T=-0.203946\) mV/K,
  \(\Delta S=-19.6777\) J mol\(^{-1}\) K\(^{-1}\),
  \(\dot Q_{\rm rev}/I=+60.8065\) mV를 냈다.
  다섯 SOC 행 전체가 해석식·production 함수·\(T\pm3\) K
  유한차분에서 일치했다.
- 문건이 선언한 graphite-vs-Li half-cell 좌표 안에서는
  \(F\partial U_{\rm oc}/\partial T\)와 lithiation-positive
  \(q_{\rm rev}=-IT\partial U_{\rm oc}/\partial T\)가 내부
  정합한다. 그러나 curve discharge는 graphite delithiation이고
  heat의 \(I>0\)은 half-cell lithiation이라 같은 단어가 반대
  반응을 가리킨다. 이 차이는 문건에 공개됐지만 API가 반응좌표를
  강제하지 않는다.
- full-cell에서는 \(U_{\rm cell}=U_{\rm cat}-U_{\rm an}\)이므로
  graphite 몫의 부호가 바뀌고 cathode coefficient도 필요하다.
  graphite-only 표에는 full-cell 총열 권위가 없다.
- Hales–Bulman 2024는 full-cell entropy coefficient 추출법을
  지지하지만 이 4-transition graphite prior의 \(+60.8\) mW/A를
  검증하지 않는다. 해당 calorimetry 정합 주장은 구체적 외부
  검증으로는 기각했다.
- v1.0.14 LCO reference/DOS/composition/\(T^2\)-curvature
  blocker는 heat AST가 동일하므로 미수리다.
- 새 worked section은 생산 코드명을 본문에 두 번 직접 적어
  사용자의 theory-only manuscript 제약을 통과하지 못했다.
- 근거:
  `Codex/results/PHASE_059_V1015_HEAT_DETAILING_AUDIT.json`,
  `Codex/results/PHASE_059_V1015_HEAT_DETAILING_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1015_heat_detailing.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1015_heat_detailing.py`.
- validator 64/64와 audit/report deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1015_HEAT_WORKED_EXAMPLE_NUMERICALLY_CLOSED_BUT_NO_NEW_HEAT_PHYSICS_AND_SIGN_API_BOUNDARY_REMAINS`.
- 다음은 Step 37.4에서 v1.0.16 \(n(T)\)를 empirical width law와
  microscopic physics로 분리하고 \(\partial w/\partial T\),
  entropy propagation, positivity와 parameter correlation을
  검산하는 일이다.

### 2026-07-28 — Step 37.4

- v1.0.15→v1.0.16 exact patch를 code +55/-20, Ch1 +11/-8,
  Ch2 +18/-6, fitting guide +23/-7, regression harness +2/-2로
  고정하고 `_n_factor`, `_width`, 신설 `_dwdT`,
  `entropy_coefficient`, `reversible_heat` AST 변화를 분리했다.
- \(n(T)=n_0+n_1(T-T_{\rm ref})\),
  \(w=n(T)RT/F\)에서
  \(\partial w/\partial T=(R/F)[n(T)+Tn_1]\)를 독립 유도했다.
  \(n_1=0.004\ {\rm K}^{-1}\), \(x=0.2\) probe의 해석식–code–
  유한차분 오차는 \(5.42\times10^{-16}\) V/K였다.
- 상수 \(n\)의 equilibrium/dQdV/entropy/reversible-heat 네
  경로는 v1.0.15와 bit-exact였고 `w`-only \(T\)-동결 경로도
  중심값-only entropy에 맞았다.
- `n`과 `w`가 모두 없는 공개 기본 경로는 `_n_factor=1`이라
  실제 폭이 \(RT/F\)인데 `_dwdT=0`으로 처리된다. \(x=0.2\)에서
  고정-\(x\) entropy 미분 오차가 0.119455 mV/K라 default-branch
  theory/code conformance를 FAIL로 판정했다.
- 평가점의 \(w>0\) fail-fast는 있으나 전체 fitting 온도창의
  \(n(T)>0\) 제약은 없다. 선형식은 \(T_{\min},T_{\max}\) 두
  endpoint에서 양수를 강제해야 한다.
- 한 온도에서는 \(n_0,n_1\) Jacobian rank가 1이다.
  278.15/288.15/298.15 K 한쪽 창에서 scaled slope
  \(b=T_{\rm ref}n_1\) width Jacobian condition number는 36.60,
  parameter correlation은 0.760이었다.
- 선형 \(n(T)\)은 실제로 \(w(T)\)에 \(T^2\) 항을 넣는 국소
  empirical width law다. microscopic multiplicity 또는
  phase-separation mechanism 권위는 기각했다.
- 실행 원장은 n(T) round-trip을 주장하지만 배포 test/demo의
  `n_T1`과 `_dwdT` occurrence는 모두 0이다. persistent regression
  authority는 FAIL이다.
- 배열 \(T(V)\) entropy는 scalar pointwise와 exact했지만
  Step 37.2 sample-mean-T lag와 LCO \(T\)-dependent entropy
  derivative blocker는 미수리다.
- 근거:
  `Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json`,
  `Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1016_nt_width_law.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1016_nt_width_law.py`.
- validator 68/68과 deterministic rerun을 통과했다.
- status:
  `CONDITIONAL_P059_V1016_NT_DWDT_ALGEBRA_AND_OPT_IN_ROUNDTRIP_PASS_BUT_EMPIRICAL_STATUS_DEFAULT_BRANCH_POSITIVITY_AND_IDENTIFIABILITY_GAPS_REMAIN`.
- 다음은 Step 37.5에서 다온도 rate-series 없이 \(n(T)\),
  activation, LCO electronic/vibrational 항을 동시에 식별 가능한지
  structural/practical identifiability로 판정하는 일이다.

### 2026-07-28 — Step 37.5

- 관측식의 Jacobian을 직접 구성해 \(n(T)\), activation,
  LCO electronic gate, vibrational 잔여항의 구조적 rank를
  각각 판정했다.
- 단일 온도의 \(n_0,n_1\)은 voltage point 수와 무관하게 rank
  1/2이며, \(T_{\rm ref}\) 양쪽 다온도 자료에서만 rank 2/2가 된다.
- activation의
  \((\Delta H_a,\Delta S_a,\log|dV/dq|)\)는 단일 온도 여러 rate에서
  rank 1/3, 세 온도 여러 rate에서도 rank 2/3이다. rate는 알려진
  \(\log I\) offset만 바꾸며 \(\Delta S_a\)와 prefactor/\(dV/dq\)
  사이의 정확한 null direction은 제거하지 못한다.
- 현 LCO electronic gate는 \(x_{\rm center},T_{\rm ref}\)에서 한
  상수로 동결되어
  \((\Delta S_{\rm base},g_{\max},x_{\rm MIT},\Delta x)\) rank가
  1/4다. composition-resolved \(x(V,T)\)와 독립 reference/DOS
  prior 없이는 분해할 수 없다.
- vibrational 잔여항은 생산 forward parameter가 없어 rank 0이다.
  phonon/heat-capacity prior와 명시 식을 추가하기 전에는 electronic
  \(T^2\) 항과 분리할 수 없다.
- synthetic round-trip은 numerical self-consistency일 뿐 noise,
  covariance, model discrepancy 아래 statistical identifiability
  증거가 아니다.
- guide의 상수-n → per-T width → n(T) 단계화는 방향만 보존한다.
  실제 graphite/LCO/Si, 특히 doped high-voltage LCO 피팅 권위는
  아직 없다.
- 근거:
  `Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json`,
  `Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md`,
  `Codex/work/v1014_v1018_2_phase059/audit_phase059_v1016_joint_identifiability.py`,
  `Codex/work/v1014_v1018_2_phase059/validate_phase059_v1016_joint_identifiability.py`.
- validator 45/45와 deterministic rerun을 통과했다.
- status:
  `FAIL_P059_V1016_JOINT_IDENTIFIABILITY_WITHOUT_MULTI_TEMPERATURE_RATE_SERIES_AND_INDEPENDENT_ELECTRONIC_VIBRATIONAL_PRIORS`.
- 다음은 Step 38.1에서 v1.0.17의 doc-only·citation 정정을 exact
  diff와 1차 출처로 판정하는 일이다.
