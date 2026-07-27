# Phase 058 v1.0.10–v1.0.13 계보 재감사 세부 계획

정본일: 2026-07-28  
상위 계획:
`Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`  
상위 Steps: 26–32  
기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 목적

v1.0.10–v1.0.13의 이론 source, code, tests, demos, PDF, images와
golden data를 전수 재감사한다. 과거 result의 PASS를 승계하지 않고
Phase 057 사용자 방향 헌법과 독립 물리·수학 검산으로 다음을 판정한다.

1. 최초 graphite/LCO ICA 물리 골격이 실제로 무엇을 계산했는가
2. 문건의 식, code path와 test가 같은 quantity·unit·sign을 썼는가
3. v1.0.10의 broadening·heat·finite-current 주장이 출력과 일치했는가
4. v1.0.11–v1.0.12의 철회·정정이 실제 source에 반영됐는가
5. v1.0.13의 통계역학 재작성은 무엇을 개선하고 무엇을 닫지 못했는가
6. 이후 버전에서 보존·교정·폐기해야 할 최초 자산은 무엇인가

## 동결된 범위

- version paths: 56
- unique blobs: 45
- duplicated blobs across versions: 8 groups
- unique full-text blobs: 27
- unique text lines: 13,757
- PDF blobs: 8, total 215 pages
- image blobs: 8
- NPZ blobs: 1
- generated pyc: 1, source가 있으므로 scientific evidence에서 제외

역할별 unique blob:

| 역할 | 수 |
|---|---:|
| theory | 6 |
| code | 3 |
| test | 5 |
| demo | 6 |
| implementation guide | 3 |
| result/handover | 4 |
| PDF | 8 |
| image | 8 |
| NPZ | 1 |
| generated pyc | 1 |

## 산출물

- `Codex/results/PHASE_058_V1010_V1013_AUDIT_QUEUE.json`
- `Codex/results/PHASE_058_V1010_V1013_TEXT_COVERAGE.json`
- `Codex/results/PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json`
- `Codex/results/PHASE_058_CODE_BEHAVIOR_MATRIX.json`
- `Codex/results/PHASE_058_PDF_IMAGE_RENDER_AUDIT.md`
- `Codex/results/PHASE_058_V1010_V1013_LINEAGE_REPORT_A.md`
- `Codex/results/PHASE_058_VALIDATION.json`

작업 스크립트와 렌더 중간물은
`Codex/work/v1010_v1013_phase058/` 아래에만 둔다.

## Step 26 — theory source 전수 검독

### 26.1

Phase 056 manifest에서 v1.0.10–v1.0.13의 56 path/45 blob을
content-addressed queue로 추출하고 version별 occurrence를 보존한다.

### 26.2

6개 unique theory blob의 모든 행을 연속 chunk로 읽고 coverage를
기록한다. master/section 구조가 없는 monolithic source이므로
chapter/section/equation/label index를 별도 생성한다.

### 26.3

각 식을 다음 계층으로 분류한다.

- coordinate and conservation
- equilibrium/statistical mechanics
- peak kernel and broadening
- hysteresis/kinetics
- thermal/entropy
- LCO extension
- observation and fitting

### 26.4

변수 정의, 단위, 부호, 미분 방향, 전제와 적용 범위가 처음 등장하는
위치를 추출한다. 정의 없는 symbol과 동일 symbol의 역할 충돌을 기록한다.

### 26.5

v1.0.10→11 동일 blob, v1.0.12 증축, v1.0.13 재작성의 exact diff를
식·claim 단위로 연결한다. copy-forward를 새 검증으로 세지 않는다.

## Step 27 — code·test·demo 전수 감사

### 27.1

3개 unique production code blob을 전문 검독하고 public API,
state variables, default, physical constants와 call graph를 기록한다.

### 27.2

5개 unique test와 6개 demo blob을 전문 검독해 각 assertion이
실제로 검사하는 quantity, tolerance, branch와 미검사 영역을 기록한다.

### 27.3

가능한 원래 test를 격리 실행한다. dependency 또는 API drift가 있으면
원본을 수정하지 않고 frozen environment failure와 대체 probe를 구분한다.

### 27.4

독립 probe로 최소 다음을 검산한다.

- dQ/dV area and capacity conservation
- charge/discharge sign convention
- \(T\) limit and width scaling
- \(I=0\), low-rate, high-rate paths
- hysteresis memory/lag limiting behavior
- entropy coefficient and reversible heat sign
- LCO toggle and placeholder behavior

### 27.5

golden NPZ의 모든 array를 code 재생성 결과와 대조하되,
bit-exact와 physical validity를 별도 판정한다.

## Step 28 — PDF·image 전수 감사

### 28.1

8개 PDF 215 pages를 전 페이지 render하고 대응 TeX의 label,
page count, missing glyph, overfull/blank/cropped content를 검사한다.

### 28.2

8개 image를 원해상도로 검독해 axis, unit, legend, temperature/current
condition, sign, peak morphology와 한글 glyph 상태를 기록한다.

### 28.3

PDF/image가 어떤 source commit/code state에서 생성됐는지
hash와 Git history로 연결한다. source보다 오래된 stale artifact를
현재 증거로 사용하지 않는다.

## Step 29 — v1.0.10 출발점 재구성

### 29.1

외부 \(q\), 조성, voltage와 dQ/dV 정의를 재유도한다.

### 29.2

평형 peak kernel, broadening, apparent potential,
hysteresis/finite-current 식을 독립 미분·극한 검산한다.

### 29.3

entropy coefficient, reversible/irreversible heat와 LCO extension의
부호·단위·물리 역할을 재검산한다.

### 29.4

과거 problem report와 integrity report의 상충 진단을 actual
source/output으로 재판정한다.

## Step 30 — v1.0.11–v1.0.12 정정 계보

### 30.1

v1.0.11이 v1.0.10과 content-identical인 영역과 version-only copy를
정확히 분리한다.

### 30.2

v1.0.12의 LCO 수식화, width/default, guide와 sample 변화가
물리 변화인지 설명 변화인지 patch로 판정한다.

### 30.3

R1 철회가 source, code, tests와 figure에서 실제로 일관적인지 확인한다.

## Step 31 — v1.0.13 통계역학 재작성

### 31.1

partition function, occupancy, chemical potential, Nernst/logistic,
multi-transition 합을 표준 통계역학에서 재유도한다.

### 31.2

interaction, degeneracy, multiplicity와 effective \(n\)/width의
물리적 의미를 분리한다.

### 31.3

v1.0.13에서 새로 생긴 식·문단·default와 code/test 변화를 연결한다.

### 31.4

50-page Ch1의 상세성이 실제 closure인지, 같은 가정의 장문 반복인지,
LCO와 유한전류 현상이 여전히 placeholder인지 판정한다.

## Step 32 — 종합 판정과 gate

### 32.1

모든 theory claim을 `PRESERVE`, `CORRECT`, `SUPERSEDE`,
`EMPIRICAL_ONLY`, `THEORY_ONLY`, `REJECT`, `UNVERIFIED`로 판정한다.

### 32.2

문건–code–test–PDF/image의 4축 matrix를 닫고,
각 PASS가 검사하지 않은 범위를 명시한다.

### 32.3

후속 Phase 059–069에서 사용할 carry-forward와 blocker를 분리한다.

### 32.4

queue/coverage, equation matrix, behavior matrix, render audit와
lineage report를 기계 검증한다.

### 32.5

`PASS_P058_LINEAGE_A`, `CONDITIONAL_P058`, `FAIL_P058` 중 하나를 판정한다.

## Gate

`PASS_P058_LINEAGE_A`는 다음이 모두 충족될 때만 부여한다.

- 45/45 unique blob 처분
- 27/27 text blob 전문 검독
- 8/8 PDF 전 페이지와 8/8 image 검독
- NPZ 13 arrays 전수 처분
- production code 3/3, test 5/5, demo 6/6 전문 검독
- 핵심 식의 독립 유도·단위·부호·극한 검산
- v1.0.10–13의 실제 diff와 철회·정정 계보 연결
- 미검증 external validity를 PASS에서 제외

## Stop conditions

- source와 PDF/image의 생성 관계를 확인할 수 없음
- dependency 부재를 test PASS로 오인해야 함
- 원전 문헌 확인 없이는 식의 귀속·조건을 확정할 수 없음
- code 실행이 원본 수정 또는 legacy environment 오염을 요구함

중단 시 원본을 고치지 않고 `BLOCKED`와 정확한 미완료 범위를 기록한다.

## 진행 기록

### 2026-07-28 — Steps 26.2–26.3

- 6/6 unique theory source를 1행부터 EOF까지 연속 검독했다.
- coverage: 9,532/9,532 theory lines.
- 196 section/subsection headings와 323 displayed equation environments를
  source line에 연결했다.
- 각 equation environment를 7개 계획 category로 1차 분류했다.
- 코드 식별자 표식은 Ch1에서 v1.0.10 193개, v1.0.12 195개,
  v1.0.13 217개로 확인됐다. 이는 현행 사용자 경계상 theory/source
  분리 대상이며, 과거 문건을 현 정본으로 승격하지 않는다.
- 초기 물리 검토는
  `Codex/results/PHASE_058_THEORY_SOURCE_REVIEW.md`에 저장했다.
- 아직 `PASS_P058_LINEAGE_A`가 아니다. Step 26.4의 symbol/definition
  충돌 전수화, Step 26.5 exact diff, Steps 27–32가 남았다.

### 2026-07-28 — Steps 26.4–26.5, 27.1

- 32개 core physical symbol에 quantity, unit, sign/role collision,
  current disposition과 source evidence를 연결했다.
- 323개 displayed equation environment의 category/source index와
  core symbol contract를 함께 사용해 Step 29–31 독립 유도의 대기열을
  닫았다. 이 단계의 `COMPLETE`는 물리 채택 판정이 아니다.
- Ch1/Ch2의 v1.0.10→12, v1.0.12→13 exact unified diff 4개와
  equation-label 변화표를 생성했다.
- v1.0.10과 v1.0.11 theory source가 동일 blob임을 확인해 새 검증으로
  중복 계상하지 않았다.
- production code 3/3 blob, 2,610/2,610행을 전문 검독하고 AST API,
  call graph, defaults와 exact code diff를 저장했다.
- text coverage는 9/27 blobs, 12,142/13,757 lines COMPLETE다.
- 아직 `PASS_P058_LINEAGE_A`가 아니다. tests 5개, demos 6개,
  guides/handover/results 4개, PDF/image/NPZ와 독립 probes가 남았다.

### 2026-07-28 — Step 27.2와 나머지 text closure

- unique test 5개와 demo 6개를 1행부터 EOF까지 전문 검독했다.
- implementation guide 3개와 result/handover 4개도 전문 검독해
  v1.0.10–v1.0.13 full-text coverage를 27/27 blobs,
  13,757/13,757행 `COMPLETE`로 닫았다.
- Python test/demo 11개에서 실제 `assert` statement는 0개였다.
  regression 2개의 실패 exit는 13개 golden array의 bit-exact 비교에만
  연결되고, `area_check`는 이름과 달리 면적 허용오차를 gate하지 않는다.
- sample test와 graph/demo suite는 그림·유한값·비율을 출력하지만
  public experiment, uncertainty 또는 holdout prediction을 검사하지 않는다.
- v1.0.13 handover의 “미완료 없음”은 같은 문장에 이월한
  LCO \(T^2\), interaction/barrier, lag rebaseline, fixed-point 때문에
  사용자 연구 목표에 대한 완료 주장으로 인정하지 않았다.
- 근거:
  `Codex/results/PHASE_058_TEST_DEMO_CLAIM_MATRIX.json`,
  `Codex/results/PHASE_058_TEST_DEMO_GUIDE_REVIEW.md`.
- 아직 `PASS_P058_LINEAGE_A`가 아니다. Step 27.3 격리 실행,
  Step 27.4 독립 probe, NPZ/PDF/image와 독립 유도·종합 판정이 남았다.

### 2026-07-28 — Step 27.3

- test/demo 11개를 대응 production module과 함께 byte-identical
  임시 복사본으로 격리 실행했다.
- 실행 전후 repository source와 v1.0.13 golden NPZ hash가 동일해
  원본 무수정을 확인했다.
- 9개 demo/report는 실행 완료, v1.0.10 regression은 repository에
  golden이 없어 `BLOCKED_MISSING_FROZEN_GOLDEN`로 처분했다.
- v1.0.13 regression은 보관 golden과 12개 array가 bit-exact
  불일치했다. 최대 절대차는 \(2.665\times10^{-15}\)였으므로
  `FAIL_BIT_EXACT_GOLDEN_FLOAT_DRIFT`로 분류했다. 수치 차이가 작다는
  사실과 `np.array_equal` gate의 실패를 동시에 보존한다.
- 11/11 case 처분과 source hash 보존은 완료됐지만, 이 결과를
  external physical validation으로 승격하지 않는다.
- 근거:
  `Codex/results/PHASE_058_LEGACY_ISOLATED_EXECUTION.json`,
  `Codex/results/PHASE_058_LEGACY_EXECUTION_REVIEW.md`.
- 다음은 Step 27.4 독립 conservation/sign/limit/current/temperature
  probe다.

### 2026-07-28 — Step 27.4

- v1.0.10, v1.0.12, v1.0.13에 independent logistic derivative,
  analytic FWHM, finite difference와 sign/unit identity probe를 실행했다.
- equilibrium kernel의 면적·peak·FWHM, entropy center,
  reversible-heat identity와 hysteresis closed-form branch gap은
  독립 계산과 일치했다.
- 세 version의 default graphite는 `Rn=0`에서 0–1 A curve가
  정확히 동일했다. 사용자 핵심인 finite-current broadening이
  default에서 비활성임을 확인했다.
- direct `L_V`는 0 A와 1 A curve가 동일하고 0 A에서도
  equilibrium보다 넓어 \(I\to0\) limit를 위반했다.
- C-rate에 coulomb capacity를 넣을 때 3600 환산 누락,
  호출 간 hysteresis state 부재, irreversible heat 음수 반환 가능성을
  확인했다.
- LCO facade 방향은 v1.0.13에서 고쳐졌으나, 세 version 모두
  default LCO에 `Omega`/`dH_a`가 없고 rate-invariant였다.
- 근거:
  `Codex/results/PHASE_058_INDEPENDENT_PROBES.json`,
  `Codex/results/PHASE_058_INDEPENDENT_PROBE_REVIEW.md`.
- 다음은 Step 27.5 golden NPZ 13 arrays 전수 처분이다.

### 2026-07-28 — Step 27.5

- v1.0.13 golden NPZ의 13/13 array를 key, shape, dtype, finite,
  byte hash, bit equality, tolerance와 최대 오차로 전수 처분했다.
- `V` 1개만 bit-exact였고 12개 model output은
  `np.array_equal`에 실패했다. 전체 최대 절대차는
  \(2.665\times10^{-15}\)였으며 13개 모두
  `rtol=atol=1e-12`에서 allclose였다.
- NPZ는 raw experiment, optimizer state, parameter covariance,
  protocol metadata 또는 runtime provenance를 담지 않는
  `DERIVED_MODEL_OUTPUT_SNAPSHOT`으로 분류했다.
- v1.0.10 regression golden은 repository 밖 temporary path에만 있어
  재현 불가능하다는 Step 27.3 blocker를 유지했다.
- 근거:
  `Codex/results/PHASE_058_GOLDEN_NPZ_AUDIT.json`,
  `Codex/results/PHASE_058_GOLDEN_NPZ_REVIEW.md`.
- Step 27은 완료됐다. 다음은 Step 28.1 PDF 8개 215 pages
  전 페이지 render와 source 대응 감사다.

### 2026-07-28 — Step 28.1

- PDF skill 절차로 8개 PDF 215 pages를 96 dpi PNG로 전 페이지
  render하고 17개 contact sheet를 모두 시각 검독했다.
- page count 215/215, blank 0, replacement character 0,
  media/crop mismatch 0, font는 전부 embedded였다.
- full-resolution edge 후보 검독에서 clipping 4쪽을 확인했다:
  v1.0.10 Ch2 p.10, v1.0.11 Ch2 p.10, v1.0.12 Ch1 p.37,
  v1.0.12 Ch2 p.11.
- v1.0.10과 v1.0.11은 Ch1 35/35, Ch2 13/13 pages가
  pixel-identical해 v1.0.11을 새 PDF 검증으로 세지 않았다.
- v1.0.10 Ch1 PDF 뒤 TeX 1행 변경은 source comment뿐이라 visible
  stale artifact는 아니지만 build genealogy에는 기록했다.
- 근거:
  `Codex/results/PHASE_058_PDF_RENDER_METRICS.json`,
  `Codex/results/PHASE_058_PDF_VISUAL_REVIEW.json`,
  `Codex/results/PHASE_058_PDF_IMAGE_RENDER_AUDIT.md`.
- 판정: `LAYOUT_PASS_WITH_4_RECORDED_DEFECTS`.
- 다음은 Step 28.2 standalone image 8개 원해상도 검독이다.

### 2026-07-28 — Step 28.2

- standalone PNG 8/8을 저장 원해상도로 열어 axis, unit, legend,
  condition, sign/direction, peak morphology와 glyph를 검독했다.
- 8개 image와 대응 generator의 SHA-256, 크기, mode, content bounds와
  pairwise pixel 관계를 기계 기록했다. 8개는 모두 서로 다른 nonblank
  blob이고 generator가 존재한다.
- v1.0.10 P5의 한글 tofu glyph와 v1.0.13 P4 panel (c) 제목
  truncation을 확인했다.
- LCO rate curve는 거의 겹치고, 저온 plot은 높고 좁은 평형 peak를
  보였다. 따라서 저장 그림은 사용자의 finite-current·low-temperature
  peak 저하와 broadening을 검증하지 않는다.
- v1.0.13 일부 그림은 LCO 방향을 고쳤지만 sample image에는
  `discharge`가 남아 같은 버전 내부에서도 direction label이
  일관되지 않다.
- 8개 모두 model-generated output이며 public experimental overlay,
  uncertainty, residual 또는 holdout prediction이 없다.
- 근거:
  `Codex/results/PHASE_058_STANDALONE_IMAGE_AUDIT.json`,
  `Codex/results/PHASE_058_STANDALONE_IMAGE_REVIEW.md`.
- 판정: `VISUAL_COMPLETE_SCIENTIFIC_VALIDATION_ABSENT`.
- 다음은 Step 28.3 artifact–generator Git genealogy와 isolated
  regeneration hash 대조다.

### 2026-07-28 — Step 28.3

- PDF 8개와 PNG 8개의 마지막 저장 commit을 각각 TeX,
  figure generator와 production model의 마지막 commit에 연결했다.
- v1.0.10 Ch1 PDF는 TeX comment-only 정정이 PDF 뒤에 있으나
  렌더 본문은 current로 판정했다. 나머지 PDF 7개는 source와 같은
  commit이거나 source 뒤에 저장됐다.
- v1.0.10 P4 LCO/heat PNG는 factor-2 정정과 model 변경 전,
  v1.0.10 dQ/dV overview는 최종 model 변경 전 저장돼 stale provenance
  artifact 2개로 판정했다.
- 8개 image generator의 격리 재실행은 모두 PNG를 생성했지만
  저장 PNG와 bit-exact한 것은 0/8이었다. render hash의 환경 민감성과
  scientific plot-data 검증을 분리했다.
- partial clone에서 일부 과거 blob 본문이 unavailable하므로 과거
  pixel-level curve delta는 `UNRESOLVED`로 남기고, 확인 가능한 commit
  graph와 현재 source 근거 이상을 주장하지 않았다.
- 근거:
  `Codex/results/PHASE_058_ARTIFACT_GENEALOGY.json`,
  `Codex/results/PHASE_058_ARTIFACT_GENEALOGY_REVIEW.md`.
- 판정:
  `PROVENANCE_COMPLETE_WITH_2_STALE_IMAGES_AND_HISTORICAL_BLOB_LIMIT`.
- Step 28은 완료됐다. 다음은 Step 29.1 v1.0.10 외부 \(q\), 조성,
  voltage와 dQ/dV 정의의 독립 재유도다.

### 2026-07-28 — Step 29.1

- circuit passed charge, reaction-state charge, normalized progress,
  Li stoichiometry를 분리하고
  \(Q_{\rm rxn}=Q_{\rm bg}+\sum_jQ_j\xi_j\)를 전위로 미분했다.
- logistic derivative의 unit area, peak \(Q_j/(4w_j)\),
  FWHM \(=4w_j\operatorname{arcosh}\sqrt2\)를 독립 유도·수치 검산했다.
- \(Q_{\rm cell}\)을 C로 선언하면서
  \(I=r_CQ_{\rm cell}\), \(r_C[{\rm h^{-1}}]\)를 쓴 문건·facade는
  factor-3600 unit error임을 재확인했다.
- default \(Q_j\) 합 graphite 0.97, LCO 1.00과 demo의
  \(Q_{\rm cell}=1\)은 실제 C보다 normalized capacity weight 계약에
  가깝다. 이론 표의 C 단위와 code default가 일치하지 않는다.
- delithiation/lithiation이라는 reaction direction과
  half-cell/full-cell charge/discharge protocol label을 분리했다.
  v1.0.10의 electrode-independent \(\sigma_d\) 주장은 기각했다.
- constant \(IR\) correction은 peak shift만 만들며 current broadening
  physics가 아니다. state-dependent overpotential에는 별도 Jacobian이
  필요하다.
- 근거:
  `Codex/results/PHASE_058_V1010_COORDINATE_CONSERVATION_DERIVATION.md`,
  `Codex/results/PHASE_058_V1010_COORDINATE_CONSERVATION_VALIDATION.json`.
- 판정:
  `CORE_CONSERVATION_PRESERVED_COORDINATE_CONTRACT_REJECTED`.
- 다음은 Step 29.2 평형 kernel, broadening, apparent potential,
  hysteresis/finite-current 식의 독립 미분·극한 검산이다.

### 2026-07-28 — Step 29.2

- ideal logistic, interacting regular solution과 two-phase branch를
  독립 재유도했다. \(\Omega\ne0\) free energy를 선언하면서
  equilibrium peak는 ideal logistic로 유지한 legacy 조합은
  thermodynamically inconsistent하다.
- first-order relaxation
  \(d\xi/dV=(\xi_{\rm eq}-\xi)/L_V\)은 \(L_V/w\) 증가에 따라
  peak 저하·FWHM 증가·causal shift·면적 보존을 보여 reduced model
  골격으로 보존했다.
- continuum \(L_V\to0\)은 평형 derivative로 매끄럽게 수렴하지만,
  legacy의 \(2\Delta V_{\rm grid}\) mode switch는 대표 격자에서
  peak를 22.9% jump시켰다.
- 258.15 K, numeric \(I=1,Q_{\rm cell}=1\)에서도 default 최대
  \(L_V\)가 switch threshold의 0.0233에 불과해 네 graphite 전이가
  모두 equilibrium branch를 사용함을 확인했다.
- direct \(L_V=0.04\) V는 \(I=0\)에서도 peak를 평형의 0.772로 낮추고
  FWHM을 1.288배 넓혀 \(I\to0\) limit를 위반했다.
- regular-solution spinodal gap 닫힌형은 독립 계산과 일치하지만,
  measured hysteresis가 아니라 homogeneous metastability upper
  scale로 한정했다. default gamma는 전부 0이고 cross-call history가
  없어 branch memory는 닫히지 않았다.
- default affinity는 \(A=4RT\)로 전이당 동결돼 local voltage
  dependence가 0이다. \(\Delta H_a-\chi\Omega\)는 equilibrium
  interaction을 underived activation correction으로 중복 사용한다.
- thermodynamic heterogeneity와 kinetic overpotential을 모두
  apparent-\(U\)의 \(\eta\)로 묶고, \(w\)와 \(L_V\)에 finite-rate
  broadening을 동시에 흡수한 설명은 분리·교정 대상으로 판정했다.
- 근거:
  `Codex/results/PHASE_058_V1010_EQUILIBRIUM_KINETICS_DERIVATION.md`,
  `Codex/results/PHASE_058_V1010_KINETICS_VALIDATION.json`.
- 판정:
  `REDUCED_RELAXATION_PROMISING_LEGACY_CLOSURE_REJECTED`.
- 다음은 Step 29.3 entropy coefficient, reversible/irreversible heat와
  LCO extension의 부호·단위·물리 역할 재검산이다.

### 2026-07-28 — Step 29.3

- \(\partial U/\partial T=\Delta S/F\), implicit entropy weighting과
  \(\dot Q_{\rm rev}=-IT\,\partial U/\partial T\)를 reaction/current/
  heat sign을 명시하는 조건으로 보존했다.
- entropy code의 \((R/F)\logit\xi\) 항은 ideal \(n=1\)에서만
  독립 미분과 일치했다. \(n=2\)와 constant empirical \(w\)에서는
  각각 \(1.1946\times10^{-4}\) V/K 오차가 생겨 width–entropy
  contract가 불일치했다.
- irreversible heat helper는 입력에 따라 \(-1\) W도 반환해
  docstring의 \(\ge0\) invariant를 보장하지 않는다.
- Sommerfeld functional form은 조건부 보존했지만 composition
  logistic DOS gate는 empirical assumption으로 낮췄다.
- gate center \(-45.678\) J/(mol K)는 수학적으로 재현됐으나 조성
  적분이 \(-9.135\) J/(mol K) \(=-1.099R\)라 문건의
  \(0.18k_B\) anchor보다 6.10배 컸다. derivative sum rule 때문에
  두 수치를 독립 척도로 분리한 정당화를 기각했다.
- 문건의 electronic \(T^2\) 식은 맞지만 code가 298.15 K offset으로
  동결해 곡률 0이다. 328.15 K에서 이론 적분과 0.7145 mV 차이가 났다.
- default LCO는 center 3.93/3.88/4.05 V의 rate-invariant three-bell
  placeholder다. \(\Omega,\gamma,\Delta H_a\), dopant/oxygen/surface
  state와 4.5 V 이상 closure가 전부 없다.
- 근거:
  `Codex/results/PHASE_058_V1010_HEAT_LCO_DERIVATION.md`,
  `Codex/results/PHASE_058_V1010_HEAT_LCO_VALIDATION.json`.
- 판정:
  `HEAT_IDENTITY_PRESERVED_ENTROPY_AND_LCO_CLOSURE_REJECTED`.
- 다음은 Step 29.4 과거 problem/integrity report의 상충 진단을
  actual source/output으로 재판정한다.

### 2026-07-28 — Step 29.4

- 과거 problem report와 integrity report의 31개 claim을 actual
  manuscript, production source, isolated execution, independent
  probe, PDF/image와 Step 29.1–29.3 재유도에 다시 연결했다.
- 판정은 `CONFIRMED` 10, `PARTIAL` 9, `REJECTED` 12,
  `UNRESOLVED` 0이며 source hash, claim ID uniqueness, status와
  evidence existence 25개 gate가 모두 통과했다.
- 최초 R1의 “분리 peak 생성 불가”는 실행으로 기각했다. 그러나 이를
  철회한 뒤 “폭 물리가 온전하다”고 확대한 integrity 결론도 기각했다.
  peak representability는 thermodynamic provenance가 아니다.
- near-delta+convolution을 무조건 강제하는 옛 처방은 채택하지 않는다.
  equilibrium phase response, kinetic state, ensemble heterogeneity,
  observation kernel을 forward hierarchy로 분리하고 식별 가능성을
  검사하는 방향으로 정리했다.
- default kinetic-off, tail 방향 모순, 전역 \(\Omega>2RT\) constraint
  충돌, heat sign, report-only area gate와 stale provenance/layout
  진단은 보존했다.
- “모든 잔여는 minor”, electronic entropy 완전 검증,
  Chapter 2 thermodynamic integrity, redesign 금지와 LCO placeholder
  강등 주장은 현 사용자 목표와 독립 검산에 따라 기각했다.
- 근거:
  `Codex/results/PHASE_058_V1010_PRIOR_REPORT_ADJUDICATION.md`,
  `Codex/results/PHASE_058_V1010_PRIOR_REPORT_ADJUDICATION.json`.
- 기계 gate:
  `PASS_P058_V1010_PRIOR_REPORT_ADJUDICATION`.
- Step 29는 완료됐다. 다음은 Step 30.1 v1.0.11이 v1.0.10과
  content-identical인 영역과 version-only copy를 정확히 분리한다.

### 2026-07-28 — Step 30.1

- commit `d86e00849a019463b6535df8322d6e8afc07b93a`에서 생성된
  v1.0.11 대응 text 8개 3,965행을 v1.0.10과 대조했고
  8/8이 byte-identical이었다.
- production code, Chapter 1/2와 sample은 파일명만 v1.0.11로
  바뀐 동일 blob이고, guide/demo/plot/regression은 동일 파일명의
  byte-identical copy다.
- PDF 2개는 CreationDate 때문에 file hash가 다르지만 기존 전페이지
  render evidence에서 48/48 pages가 pixel-identical, 최대 channel
  차이 0이었다. v1.0.10 Ch2 p.10 clipping도 그대로 복사됐다.
- docs 밖에 새로 생긴 execution ledger는 Phase 0.1 baseline copy만
  완료하고 LCO 수식화 등 Phase 1.1 이후를 미완으로 기록한다.
- 따라서 scientific source, production path, defaults, test logic와
  experimental validation 변화는 모두 0이다.
- 근거:
  `Codex/results/PHASE_058_V1011_COPY_LINEAGE_REVIEW.md`,
  `Codex/results/PHASE_058_V1011_COPY_LINEAGE_MATRIX.json`.
- 기계 gate:
  `PASS_P058_V1011_COPY_LINEAGE` (64 checks).
- 판정:
  `V1011_IS_A_BYTE_IDENTICAL_TEXT_BASELINE_COPY_AND_RENDER_IDENTICAL_PDF_REBUILD`.
- 다음은 Step 30.2 v1.0.12의 LCO 수식화, width/default, guide와
  sample 변화가 물리 변화인지 설명 변화인지 patch로 판정한다.

### 2026-07-28 — Step 30.2

- v1.0.11→v1.0.12 대응 8개 파일의 exact patch는 739행 추가,
  201행 삭제였다. 5개가 변경됐고 demo/plot/regression 3개는
  byte-identical이다.
- Ch1은 labeled equation 60→86개(26 추가, 2 변경), Ch2는
  22개 유지(2 변경)다.
- 점유 convention의 Bragg–Williams 전위/기울기 부호,
  MSMR same-quantity pairing의 \(f=+\sigma_d\), finite-rate tail과
  symmetric width 분리, branch-average small-gap 한정,
  Sommerfeld 적용범위와 LCO parameter 미배정 표시는 보존했다.
- production diff 16+/7−는 header/comment/docstring뿐이다.
  docstring-stripped executable AST hash는 두 version이 같고,
  graphite/LCO curve와 entropy 대표 4 case가 전부 bit-identical,
  최대 차이 0이었다.
- 새 LCO equation은 추적성을 높였지만 같은 scalar
  regular-solution/logistic 식의 label 치환이며 phase-specific
  free energy, dopant/oxygen/surface/high-voltage state를 만들지 않았다.
- entropy-width 일반화, electronic composition/\(T^2\),
  LCO direction facade, \(I\to0\), grid handoff와 barrier closure는
  theory-only 또는 미해결이다.
- S0–S5/GITT/AIC/holdout은 유용한 계획이지만 data/fitting/
  uncertainty pipeline은 추가되지 않았다. sample은 report-only이며
  public experiment가 없다.
- 근거:
  `Codex/results/PHASE_058_V1012_PATCH_REVIEW.md`,
  `Codex/results/PHASE_058_V1012_PATCH_ADJUDICATION.json`.
- 기계 gate:
  `PASS_P058_V1012_PATCH_ADJUDICATION` (40 checks).
- 판정:
  `V1012_CONTAINS_REAL_THEORY_CORRECTIONS_BUT_NO_EXECUTABLE_PHYSICS_ADVANCE`.
- 다음은 Step 30.3 R1 철회가 source, code, tests와 figure에서 실제로
  일관적인지 확인한다.

### 2026-07-28 — Step 30.3

- R1 철회의 historical claim, v1.0.12 theory, code, sample/test와
  stored figure를 12개 facet으로 교차 판정했다.
- 298.15 K에서 shipped \(n=1\), \(w=25.691\) mV는 local maximum
  1개, fitted \(n=0.12\), \(w=3.083\) mV는 4개를 만들었다.
  따라서 “분리 peak 생성 불가”는 좁은 의미에서 기각했다.
- shipped transition은 네 개 모두 \(n=1\)이고 stored `w` fallback은
  shadowed다. default는 여전히 merged이며 \(R_n=0\)에서
  \(I=0\)과 1 A shape 차이는 정확히 0이다.
- 원고는 near-delta equilibrium과 \(\rho(U_\app)\) forward
  broadening을 개념적으로 분리했지만 production에는 explicit
  ensemble integral이 없다.
- 같은 theory 절에서 finite-current ①은 \(w\)가 아니라 \(L_V\)라고
  한 뒤 keybox는 ①·②·③을 모두 \(w\)가 흡수한다고 적어 내부 모순도
  남는다.
- v1.0.12 sample source와 PNG는 same-commit current artifact이고
  default/fitted를 정직하게 표시한다. 그러나 sample과 regression의
  Python assert는 각각 0개다.
- copied regression은 v1.0.12에서도 v1.0.10 module path를 hardcode해
  v1.0.12나 R1을 gate하지 않는다.
- 근거:
  `Codex/results/PHASE_058_R1_WITHDRAWAL_CONSISTENCY_REVIEW.md`,
  `Codex/results/PHASE_058_R1_WITHDRAWAL_CONSISTENCY_MATRIX.json`.
- 기계 gate:
  `PASS_P058_R1_CROSS_ARTIFACT_ADJUDICATION` (24 checks).
- 판정:
  `R1_WITHDRAWAL_IS_CONSISTENT_ONLY_FOR_NUMERICAL_FLEXIBILITY_NOT_FOR_PHYSICAL_CLOSURE`.
- Step 30은 완료됐다. 다음은 Step 31.1 v1.0.13 partition function,
  occupancy, chemical potential, Nernst/logistic와 multi-transition
  합을 표준 통계역학에서 재유도한다.

### 2026-07-28 — Step 31.1

- 단일자리 grand partition에 빈/점유 상태 축퇴도까지 포함해
  점유율, chemical potential, Li/Li\(^+\) 기준 전위,
  Nernst/logistic과 이상 dQ/dV 종을 독립 재유도했다.
- 298.15 K에서 이상 \(w=25.692579\) mV,
  FWHM \(=90.579042\) mV, peak \(=9.730436\) V\(^{-1}\),
  면적 1을 확인했다. 분배함수 점유와 직접 logistic의 최대 차이는
  \(1.67\times10^{-16}\)이다.
- 축퇴도 \(g_1/g_0=3\)은 중심을 28.226 mV 옮기지만 FWHM은
  바꾸지 않으므로 폭 다중도 \(n_j\)의 유도가 될 수 없다고 판정했다.
- 독립 자리/반응군이면
  \(\Xi_{\rm total}=\prod_j\Xi_j^{M_j}\)에서 용량 합이 나오지만,
  동일 host의 연속 staging 상태에는 상호배타 multi-state partition
  또는 명시적 reaction extent가 필요함을 분리했다.
- v1.0.13은 \(\Omega\ne0\)이면 닫힌 logistic이 아니라고 올바르게
  쓰면서도, 다른 절에서는 모든 단상 \(\Omega\le2RT\)의 폭을
  \(n_jRT/F\) 평형 예측으로 확장해 내부 충돌한다.
- \(\Omega=RT,\xi=0.8\)에서 정규용액 전위가 이상 Nernst보다
  15.416 mV 낮고, 중심 기울기 등가 폭도 \(RT/(2F)\)임을 검산했다.
- \(\Omega=3RT\)의 binodal은
  \(\theta=0.070720/0.929280\)이고 spinodal
  \(0.211325/0.788675\)와 다르다. 비볼록 loop는 convexification
  전 homogeneous/metastable branch이며 그 자체가 평형 plateau나
  측정 hysteresis memory가 아니라고 판정했다.
- 고정 \(s=+1\)의 평형 유도는 보존하지만, 후반의
  \(\sigma_d\) 재도입은 물리적 평형 방향이 아니라 좌표 여집합
  relabel 또는 별도 kinetic path로만 허용한다.
- 13개 claim을 처분했고 기계 검산 35/35가 통과했다.
- 근거:
  `Codex/results/PHASE_058_V1013_STATMECH_DERIVATION.md`,
  `Codex/results/PHASE_058_V1013_STATMECH_VALIDATION.json`.
- 기계 gate:
  `PASS_P058_V1013_STATMECH_REDERIVATION`.
- 다음은 Step 31.2 interaction, degeneracy, multiplicity와
  effective \(n\)/width의 물리적 의미를 분리한다.
