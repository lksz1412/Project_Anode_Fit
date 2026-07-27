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
