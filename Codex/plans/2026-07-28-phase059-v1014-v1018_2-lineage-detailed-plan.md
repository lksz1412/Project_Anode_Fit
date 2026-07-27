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
