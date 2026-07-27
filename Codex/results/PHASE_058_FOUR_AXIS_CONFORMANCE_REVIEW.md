# Phase 058 문건–코드–시험–산출물 4축 정합 판정

정본일: 2026-07-28  
대상: Phase 058 Step 32.2  
기계 matrix:
`Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_MATRIX.json`  
검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_four_axis_matrix.py`

## 결론

핵심 계약 26개를 theory, production code, test gate,
PDF/image/data artifact 네 축으로 분리했다.

| 종합 상태 | 수 |
|---|---:|
| `ALIGNED` | 6 |
| `PARTIAL` | 6 |
| `MISALIGNED` | 8 |
| `ABSENT` | 5 |
| `UNVERIFIED` | 1 |

최종 판정은

`NO_SINGLE_AXIS_PASS_IS_A_PHYSICAL_CLOSURE;_SIX_TOPICS_ALIGN_INTERNALLY_BUT_NONE_ESTABLISHES_MATERIAL_EXTERNAL_VALIDITY`

이다.

내부 정합 6건도 외부 재료 유효성을 증명하지 않는다. 반대로
artifact에 결함이 있어도 그 artifact가 그린 수학식까지 자동으로
틀린 것은 아니다. 네 축을 분리한 이유가 이것이다.

## 1. 내부 정합이 확인된 여섯 항목

### Ohmic polarization sign

좌표와 전극 방향을 명시하면 theory와 code가 맞고 독립 probe도
부호를 재현한다. 다만 \(R_n\)의 재료 값은 검증하지 않는다.

### Ideal logistic peak

이상계의 면적, 높이, FWHM과 온도 scaling은 theory–code–독립
formula가 맞는다. Golden·sample은 model output일 뿐 실험이 아니다.

### Graphite direction mapping

graphite half-cell 방향 mapping은 구현과 독립 probe가 맞는다.
일부 stored image label은 별도 artifact 결함으로 남는다.

### LCO charge → delithiation

v1.0.13 facade는 LCO charge를 cathode delithiation에 연결한다.
이 변경은 맞지만 regression harness는 이 경로를 gate하지 않는다.

### Ideal \(n=1\) entropy coefficient

이상 정규화에서 식, code, finite-difference identity가 맞는다.
이는 fitted \(\Delta S_j\)가 실제 재료 값이라는 검증이 아니다.

### Reversible heat identity

명시한 current/electrode sign 아래
\(\dot Q_\mathrm{rev}=-IT\,\partial U/\partial T\)가 맞는다.
Calorimetry와 전체 heat source closure는 별도다.

## 2. 부분 정합 여섯 항목

### Multi-transition sum

용량 가중 peak 합은 구현되지만 common-host phase topology는
증명되지 않았다. Test는 주로 면적·출력 report다.

### Finite-current relaxation

Causal reduced model은 구현됐지만 shipped default가 rate response를
보이지 않는다. 실험 조건 matrix도 없다.

### Zero-current limit

Arrhenius path는 \(I\to0\)을 지향하지만 direct `L_V`가 이를
우회한다. Legacy test가 아니라 독립 probe가 발견했다.

### LCO electronic entropy

Sommerfeld 이론 일부와 frozen implementation이 있으나, 유도한
\(T^2\) 신호와 조성 feedback은 구현·시험·data가 없다.

### Graphite golden regression

13개 array 비교는 유용한 software regression이다. 그러나
scalar, entropy, LCO, physical validity와 portability를 gate하지
않는다. 현재 환경 bit-exact는 1/13이고 \(10^{-12}\) allclose는
13/13이다.

### PDF layout

8 PDFs/215 pages가 모두 render됐지만 4쪽 clipping defect가 있다.
전 페이지 render 성공은 조판 완전성이나 과학 타당성 PASS가 아니다.

## 3. 불일치 여덟 항목

- C-rate–capacity 단위: factor 3600 mismatch
- nonideal regular solution: implicit isotherm과 closed logistic 혼용
- \(n/w\) width: theory의 multiplicity와 code의 empirical width 혼동
- local barrier: local \(U,\xi,\eta\)가 아니라 cut scalar에 동결
- persistent hysteresis: static branch와 within-curve filter뿐
- arbitrary-\(n\) configurational entropy: 대수 미분을 미시 entropy로 승격
- image provenance: stale 2개, isolated rerender bit-exact 0/8
- theory-only 문건 구조: Ch1 code identifier 215회

이 항목들은 “설명이 많다”거나 “curve가 그려진다”는 이유로
승계하지 않는다.

## 4. 부재 다섯 항목

- convexified equilibrium/binodal closure
- 실행 가능한 ensemble heterogeneity observation layer
- doped high-voltage LCO stability chemistry
- public-data fit·uncertainty·holdout
- silicon 및 graphite–silicon composite

부재는 실패한 구현과 다르다. 후속 계획에서 신규 설계해야 하며
기존 식을 조금 고쳐 완료 처리할 수 없다.

## 5. 미검증 한 항목

LCO transition default와 phase assignment는 theory의 Tier C,
code의 three-peak initial, model-output plot까지만 있다. Test와
공개 실험 fit이 없으므로 `UNVERIFIED`다.

## 6. 각 PASS의 한계

### Theory PASS가 뜻하지 않는 것

- code implementation
- material parameter validity
- identifiability
- experimental support

### Code execution PASS가 뜻하지 않는 것

- 같은 물리량·단위·부호
- correct limiting behavior
- default activation
- data explanatory power

### Test PASS가 뜻하지 않는 것

- 미검사 branch의 정합
- printed diagnostic의 failure gate
- golden output의 물리 타당성

### Artifact PASS가 뜻하지 않는 것

- current source에서 생성됨
- axis/legend/scientific claim 정확성
- public experimental evidence

## 7. 기초 증거

- theory source 6개, equation occurrence 323
- production code blob 3개, 2,610행
- test/demo 11개, Python assert 0
- legacy execution 11건 중 report-only success 9
- golden 13 arrays: bit-exact 1, allclose \(10^{-12}\) 13
- PDF 8개/215쪽, clipping 4
- standalone image 8개, stale 2
- public experimental dataset 0

44/44 machine checks가 통과했다.

## 8. 다음 단계

Step 32.3에서는 후속 Phase 059–069로 넘길 항목을

- carry-forward asset
- repair blocker
- new-scope blocker
- evidence debt

로 분리한다. 특히 기존 v1.0.14 이후 version을 읽을 때
“이미 v1.0.13에서 해결됐다”는 선언을 그대로 승계하지 않도록
이 matrix를 비교 기준으로 사용한다.
