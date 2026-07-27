# Phase 058 — v1.0.10–v1.0.13 계보 재감사 종합 보고서

정본일: 2026-07-28

판정:
`PASS_P058_LINEAGE_A`

판정의 뜻:
v1.0.10–v1.0.13의 동결된 자료를 빠짐없이 읽고, 물리·수학·구현·시험·
산출물의 관계를 판정하여 후속 단계로 라우팅했다. 이 PASS는 어느
버전도 재료 물리의 정본이거나 공개 실험 데이터로 검증됐다는 뜻이
아니다.

## 1. 감사 경계와 완결성

- version path: 56/56
- unique blob: 45/45
- full-text blob: 27/27, 13,757행
- theory source: 6개, 9,532행
- production code: 3개, 2,610행
- test: 5개
- demo: 6개
- implementation guide: 3개
- result/handover: 4개
- PDF: 8개, 215/215 pages
- standalone image: 8/8
- golden NPZ: 13/13 arrays

동일 blob의 버전별 복제는 별도 검증으로 중복 계산하지 않았다. source,
PDF, image와 golden data는 원본을 수정하지 않고 읽기·격리 실행·독립
probe로만 조사했다.

## 2. 복원된 작성 방향과 이 보고서의 역할

이 계보에서 복원한 최종 작성 원칙은 다음과 같다.

1. 최종 이론 문건의 본문은 물리·화학 논리와 그 유도만 담는다.
2. 구현 식별자, 함수명, test 명령과 conformance 기록은 허용된 단일
   구현 경계 또는 별도 통제 문건에 둔다.
3. 코드는 문건의 변수·단위·부호·상태·극한을 전부 구현해야 한다.
4. 낮은 온도와 유한 정전류에서 관측되는 dQ/dV peak의 suppression과
   broadening을 평형 폭, 활성화된 지연, 상전이 barrier, 관측 연산자의
   분리된 인과 사슬로 설명해야 한다.
5. graphite, silicon, graphite–silicon composite와 doped
   high-voltage LCO를 공개 실험 데이터로 검증해야 한다.
6. 적합 상수는 문헌값·실험 fit·가설을 구분하고, 검증되지 않은
   material default로 승격하지 않는다.

따라서 이 보고서는 이론 원고가 아니다. 코드와 시험을 직접 언급할 수
있는 계보·정합성 통제 문건이며, 여기의 기술적 추적성이 최종 이론
본문으로 역류해서는 안 된다.

## 3. 버전별 계보 판정

### v1.0.10

가치가 있는 출발점은 이상 평형 logistic kernel, 용량 가중 합,
전극별 반응 방향을 분리하려는 구조, 완화 동역학의 축약형, entropy와
reversible heat를 연결하려는 시도다.

그러나 다음 결함 때문에 정본으로 채택할 수 없다.

- `Q_cell`을 coulomb으로 허용하면서 `I=C_rate*Q_cell`을 쓰는 경로는
  hour-to-second 변환이 빠져 3600배 단위 모호성을 만든다.
- 유한전류 지연과 평형 경로의 전환이 물리적 극한이 아니라 grid step
  기준의 수치 switch다.
- 직접 `L_V`를 주는 경로는 \(I\to0\)에서 평형으로 돌아가지 않는다.
- hysteresis는 기본값에서 꺼져 있고 영속 상태를 갖지 않는다.
- 임의 cut 위치의 affinity를 고정하여 local potential·composition
  의존 barrier를 계산하지 않는다.
- `n`, `w`, interaction과 activation enthalpy의 역할이 겹친다.
- LCO 기본값은 rate-invariant three-bell placeholder이며, doping과
  high-voltage 안정화 화학을 닫지 않는다.

과거 problem report의 국소 진단은 일부 유효하지만, integrity PASS는
기각했다. 31개 과거 claim은 confirmed 10, partial 9, rejected 12,
unresolved 0으로 재판정했다.

### v1.0.11

v1.0.10과 대응하는 text 8쌍, 3,965행은 byte-identical이다. PDF 2쌍,
48 pages도 pixel-identical rebuild다. scientific source, production
code와 test logic의 변화는 0이다.

그러므로 v1.0.11은 새 물리 검증이 아니라 version-only baseline copy다.

### v1.0.12

v1.0.10 대비 대응 file 8쌍 중 5쌍이 바뀌었고, 739행 추가·201행
삭제가 있다. LCO 단위 표기, 부호 설명, Sommerfeld endpoint와 width
설명에는 보존할 정정이 있다.

반면 production executable physics 변화는 0이다. 원고에서 추가한
composition-local electronic term과 \(T^2\) curvature가 코드에
반영되지 않았고, 공개 데이터·fit pipeline·doped high-voltage LCO
closure도 없다. 따라서 “실제 이론 정정은 있으나 실행 물리의 진전은
없다”가 판정이다.

### v1.0.13

v1.0.12 대비 text patch는 1,890행 추가·1,268행 삭제다. Chapter 1은
2,358행에서 2,934행, equation label 86개에서 111개로 늘었고 기존
label은 제거되지 않았다. 이상 partition function에서 occupancy,
chemical potential, voltage와 normalized logistic derivative로
가는 통계역학 사슬은 실제로 개선됐다.

production callable 30개 중 27개 AST는 같고 `curve`, `dqdv`,
`entropy_coefficient` 세 경로가 바뀌었다. scalar degenerate-span
tail 수정과 LCO charge→delithiation 방향 수정은 보존한다.

그러나 다음은 닫히지 않았다.

- nonideal free energy의 convexification과 two-phase topology
- common-host multi-transition partition/conservation
- empirical width와 microscopic degeneracy/cooperativity의 분리
- local-state barrier와 persistent hysteresis state
- \(I\to0\)의 연속적 평형 복귀
- ensemble·instrument 관측 연산자
- LCO interaction/barrier와 electronic term의 material validation
- Si와 graphite–Si composite
- 공개 데이터 fit, 불확도, holdout과 model discrimination

50-page Chapter 1에는 code identifier가 215회 등장한다. 구현 경계를
2,630–2,852행으로 넉넉하게 인정해도 129회, 28개 heading block이
경계 밖에 남는다. Chapter 2의 code identifier는 0회다. 따라서
v1.0.13은 실제 재구조화이지만 사용자의 theory-only 본문 원칙과
과학적 closure를 충족하지 않는다.

## 4. 핵심 물리 판정

### 4.1 좌표·보존·방향

이상 단일 전이에서 normalized logistic derivative의 면적과 FWHM
관계는 독립 검산과 일치한다. transition capacity의 합으로 총 용량을
구성하는 골격도 보존 가능하다.

반면 외부 \(Q\), 조성 \(x\), 반응 진행률과 전극별 lithiation 방향은
cycle label과 분리된 단일 계약으로 다시 써야 한다. coulomb과 Ah를
동시에 허용하려면 명시적 변환을 거친 한 단위 계약만 존재해야 한다.

### 4.2 평형 통계역학과 상전이

v1.0.13의 ideal grand-canonical 유도는 유효한 교육적·수학적
출발점이다. 다만 ideal logistic kernel의 중첩을 곧바로 graphite
staging이나 LCO phase assignment로 읽을 수 없다.

interaction parameter가 있는 비이상계는 단순 logistic width 수정이
아니라 free-energy convexification, common tangent 또는 그와 동등한
chemical-potential closure가 필요하다. 여러 전이는 독립 bell의 합이
아니라 shared host inventory와 상분율 제약을 만족해야 한다.

### 4.3 폭·관측·유한전류

현재 `n`은
\[
\lambda=\frac{wF}{RT}
\]
로 해석되는 empirical width ratio다. logistic surrogate에서
\(h=1/\lambda\)라는 등가 slope를 정의할 수는 있으나, 이를 미시적
multiplicity 또는 cooperativity의 증거로 승격할 수 없다.

평형 이질성, 동역학과 관측을
\[
\left(K_{\rm obs} * K_{\rm kin} * \rho_{\rm het} * p_{\rm eq}\right)(V)
\]
처럼 분리해야 한다. 이 식은 후속 이론의 구조 원칙이지 현재 재료에
검증된 kernel 선택을 뜻하지 않는다.

이상 평형 폭은 298.15 K에서 273.15 K로 낮추면 약 0.916배가 된다.
한편 \(E_a=40\) kJ/mol의 예시 Arrhenius relaxation time은 약
4.379배 증가한다. 따라서 저온에서 평형 peak는 좁아지더라도
finite-current lag·분포·관측 convolution이 더 강해져 measured
peak suppression과 broadening을 만들 수 있다. 이는 사용자의 관측과
방향이 맞는 기작 가설이며, 아직 재료 parameter의 검증은 아니다.

### 4.4 barrier와 hysteresis

barrier는 전극 전위·조성·상분율·온도와 전류 이력에 따른 local
free-energy landscape에서 정의돼야 한다. interaction energy를 곧바로
activation enthalpy에서 빼는 방식이나 임의 cut affinity는 이 역할을
대체하지 못한다.

평형 branch 선택과 kinetic memory를 구분해야 한다. hysteresis를
설명하려면 최소한 상태 변수, 진화 법칙, 초기 조건, detailed-balance
또는 비평형 정당화와 \(I\to0\) 극한이 필요하다.

### 4.5 entropy와 heat

이상 \(n=1\) 경로의 entropy coefficient와 reversible heat identity는
주어진 부호 규약 아래 내부 정합성을 갖는다. 임의 `n`과 `w`에 동일
configurational entropy 의미를 부여하는 것은 기각한다. `n` 입력은
\(w\propto T\), `w`-only 입력은 \(w=\mathrm{constant}\)라는 서로 다른
온도 모형을 선택하므로 alias가 아니다.

LCO electronic gate의 적분은 설정된 endpoint와 내부적으로 맞지만,
composition locality, \(T^2\) voltage curvature와 독립 electronic
structure 근거가 구현·검증되지 않았다. 내부 합 규칙의 일치는 재료
귀속의 증명이 아니다.

### 4.6 재료 범위

이 계보에는 공개 experimental dataset 0, fit result 0, optimizer state
0, Si theory/code path 0이다. doped high-voltage LCO는 interaction
감소와 center shift라는 서술 수준이며, dopant chemistry, oxygen
stability, electronic/structural transition과 degradation boundary를
식과 데이터로 닫지 않는다.

따라서 graphite/LCO/Si 수치 상수를 material default로 승격할 근거가
없다. 이 계보의 default는 검증된 물성값이 아니라 legacy configuration
또는 Tier-C placeholder로만 취급해야 한다.

## 5. 문건–코드–시험–산출물 4축 판정

26개 핵심 계약의 종합 상태는 다음과 같다.

| 상태 | 수 | 의미 |
|---|---:|---|
| `ALIGNED` | 6 | 네 축 또는 필요한 축의 내부 관계가 맞음 |
| `PARTIAL` | 6 | 일부 축만 존재하거나 gate가 불완전함 |
| `MISALIGNED` | 8 | 같은 물리량·단위·극한을 구현하지 않음 |
| `ABSENT` | 5 | 요구된 물리 또는 검증 경로가 없음 |
| `UNVERIFIED` | 1 | 구현은 있으나 재료 귀속 근거가 없음 |

내부 정합으로 확인된 여섯 항목도 external material validity를
확정하지 않는다. test/demo 11개에는 Python `assert`가 0개다.
격리 실행 11건은 report-only 9, frozen golden 부재로 blocked 1,
bit-exact drift 1이다.

golden 13 arrays는 \(10^{-12}\) allclose 13개지만 bit-exact는 1개다.
이는 float 재현성과 frozen-output 관계를 보여줄 뿐 물리 검증이 아니다.

PDF 8개 215 pages는 전 페이지 검독했다. blank/glyph/font 문제는 없지만
right-edge clipping 4건이 확인됐다. standalone image 8개 중 2개는
stale provenance이며, 재생성 8개가 모두 bit-exact가 아니므로 그림을
현재 source의 독립 증거로 사용하지 않는다.

## 6. claim 처분과 후속 라우팅

theory equation occurrence 323/323을 다음과 같이 처분했다.

| 결정 | 수 |
|---|---:|
| `PRESERVE` | 145 |
| `CORRECT` | 35 |
| `SUPERSEDE` | 29 |
| `EMPIRICAL_ONLY` | 29 |
| `THEORY_ONLY` | 66 |
| `REJECT` | 6 |
| `UNVERIFIED` | 13 |

후속 Phase 059–069에는 34개 register item을 넘긴다.

- carry-forward asset: 11
- repair blocker: 13
- new-scope blocker: 5
- evidence debt: 5

자산으로 넘기는 것은 ideal kernel, 보존식, 방향 계약, reduced causal
start, entropy/heat identity, Sommerfeld endpoint, evidence tiering,
scalar guard와 감사 infrastructure다.

repair blocker는 unit, convexification, multi-transition topology,
width/entropy, local barrier, \(I\to0\), numerical handoff, hysteresis
state, LCO electronic/default, observation, executable test와
theory–code separation이다.

new scope는 public-data fit, Si/composite, doped high-voltage LCO,
uncertainty/holdout/ablation과 systematic literature review다. 이들은
옛 식을 조금 고치는 것으로 해결됐다고 표시할 수 없다.

## 7. 이 구간에서 선택 가능한 “최선”과 그 한계

v1.0.10–v1.0.13 안에서 단일 최종 버전을 고르면 v1.0.13이 ideal
통계역학 설명, scalar guard와 LCO 방향 수정 면에서 가장 나은 국소
출발점이다. 그러나 다음 작업의 정본으로 그대로 채택할 수는 없다.

- empirical width와 nonideal phase physics가 섞여 있다.
- finite-current와 hysteresis closure가 없다.
- LCO는 material-validated model이 아니다.
- Si/composite와 public-data fit이 없다.
- theory-only 본문 경계를 위반한다.

따라서 현 단계의 올바른 결론은 “v1.0.13을 정본으로 승격”이 아니라
“검증된 부분 자산만 후속 버전 계보와 비교할 후보로 보존”이다.
v1.0.10–v1.0.25.2 전체에서 어떤 조합을 최종 기반으로 삼을지는
Phase 059–063을 동일 기준으로 재감사한 뒤 결정한다.

## 8. 최종 gate

다음 조건을 모두 충족하여 `PASS_P058_LINEAGE_A`를 부여한다.

- 45/45 unique blob 처분
- 27/27 text blob 전문 검독
- production code 3/3, test 5/5, demo 6/6 전문 검독
- PDF 8/8, 215/215 pages와 image 8/8 검독
- golden 13/13 arrays 처분
- 좌표·평형·폭·동역학·열·LCO의 독립 단위·부호·극한 검산
- v1.0.10→v1.0.13의 copy, patch, 철회와 정정 계보 연결
- theory claim 323/323 처분
- 4축 row 26/26 판정과 후속 register 34개 라우팅
- external validity를 PASS 의미에서 명시적으로 제외
- `Claude/` 원본 무변경

다음 단계는 v1.0.14–v1.0.18.2를 다루는 Phase 059다. Phase 058의
결론은 후속 계보의 설명을 선점하지 않으며, 더 최신 source가 이전
결함을 고쳤는지 실제 diff와 독립 probe로 다시 판정한다.
