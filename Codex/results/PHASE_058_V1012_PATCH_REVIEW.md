# Phase 058 v1.0.12 patch 재판정

정본일: 2026-07-28

대상: Phase 058 Step 30.2

기계 matrix:
`Codex/results/PHASE_058_V1012_PATCH_ADJUDICATION.json`

## 결론

v1.0.12에는 보존할 실제 이론 정정이 있다. 그러나 production code의
실행 AST와 대표 출력은 v1.0.11과 동일하다.

최종 판정:

`V1012_CONTAINS_REAL_THEORY_CORRECTIONS_BUT_NO_EXECUTABLE_PHYSICS_ADVANCE`

## patch 크기

대응 파일 8개 중 5개가 바뀌고 3개는 byte-identical이다. 총 diff는
739행 추가, 201행 삭제다.

| 역할 | + | − | 분류 |
|---|---:|---:|---|
| production code | 16 | 7 | header/comment/docstring |
| fitting guide | 67 | 15 | workflow 문서 |
| LCO/heat demo | 0 | 0 | byte-identical |
| Chapter 1 | 533 | 112 | 이론·설명 확장 |
| Chapter 2 | 41 | 14 | 부호·적용한계 정정 |
| dQ/dV plot | 0 | 0 | byte-identical |
| sample test | 82 | 53 | report/figure 재작성 |
| regression | 0 | 0 | byte-identical |

Chapter 1은 labeled equation 60개에서 86개로 늘었다. 26개가 새
LCO label이고 기존 식 2개가 바뀌었다. Chapter 2는 equation 수가
22개로 같고 Bragg–Williams 전위와 기울기 2개가 바뀌었다.

## 실제로 보존할 이론 정정

### Bragg–Williams 부호

점유율 \(\theta\) convention에서

\[
 U_{\rm eq}
 =U_j-\frac{RT}{F}\ln\frac{\theta}{1-\theta}
 -\frac{\Omega}{F}(1-2\theta)
\]

로 고친 것은 맞다. \(\Omega=0\)에서 기존 occupancy/Nernst 식과
일치하고, 중심 기울기의 부호를 함께 고쳐
\(\Omega=2RT\) 임계조건은 보존된다.

### MSMR pairing

MSMR의 Li 점유율은 Li 점유율과, 탈리튬화 진행률은 탈리튬화 진행률과
대응시켜야 한다. 이때 재모수화된 방향 표기는
\(f=+\sigma_d\)가 된다. v1.0.12의 이 교정은 보존한다.

다만 logistic derivative의 절댓값은 여집합 교환에 불변이라
이 정정만으로 dQ/dV curve가 달라지지 않는다. 실제 LCO high-level
`charge` mapping은 v1.0.12에서도 고치지 않았다.

### 설명의 적용한계

다음 정정도 보존한다.

- finite-rate causal tail과 symmetric width를 분리
- grid switch의 기본 약 23% jump를 정직하게 공개
- branch-average reversible entropy를 small-gap 선형화로 제한
- Sommerfeld 식을 degenerate regime로 제한
- LCO \(\Omega,\Delta H_a\)가 미배정임을 명시

이는 과거 overclaim을 줄이는 실질 개선이다.

## 새 식과 새 물리가 같은 것은 아니다

새 LCO equation 26개는 주로 graphite 식에
`cat`, T1/T2/T3 label을 붙여 전개한 것이다. 식의 추적성은 좋아졌지만
다음은 생기지 않았다.

- LCO phase별 자유에너지 또는 order parameter
- dopant/oxygen vacancy/surface reconstruction state
- 4.5 V 이상 oxygen/redox/structural stability closure
- LCO \(\Omega,\gamma,\Delta H_a,L_V\) parameter
- composition-resolved public data calibration

도핑에 따른 \(\Omega\to2RT^+\)만으로 static gap이 작아진다는
asymptotic은 맞아도, 고전압 도핑 LCO의 화학적 안정성을 설명하는
모델은 아니다.

## 이론–코드 불일치가 남은 항목

### production은 실행상 동일

comment/docstring을 제거한 AST hash는 두 버전에서 동일하다. graphite
curve, graphite entropy, LCO curve, LCO entropy 네 대표 array도
모두 bit-identical이고 최대 차이는 0이다.

따라서 v1.0.10의 다음 결함은 v1.0.12에 그대로 남는다.

- factor-3600 capacity/current 계약
- default current broadening 비활성
- direct \(L_V\)의 \(I\to0\) 위반
- grid-dependent branch switch
- frozen \(A=4RT\)와 underived barrier correction
- stateless hysteresis
- heat sign API 충돌

### entropy-width

v1.0.12는 insertion convention의
\(+R\ln[\xi/(1-\xi)]\) 부호를 고쳤다. ideal \(n=1\)에는 맞지만,
일반 `n`이면 \(nR\)가 필요하고 constant empirical `w`이면 그
온도미분 항은 0이다. 따라서 “`w=nRT/F`가 자동 생성”이라는 설명은
전체 width API와 아직 맞지 않는다.

### electronic \(T^2\)

원고는 composition-dependent entropy를 적분한 \(U_1(V,T)\)를
제시하지만 code는 `x_center`, 298.15 K에서 값을 동결한다.
따라서 조성 국소성과 \(T^2\) 곡률은 theory-only다.

## guide와 sample의 효력

S0–S5, GITT/AIC, staged fitting, residual diagnosis와 holdout 원칙은
후속 설계 자산으로 보존할 가치가 있다. 그러나 v1.0.12에는 data ingest,
objective, optimizer, covariance/uncertainty, AIC와 holdout 실행
pipeline이 없다.

sample은 그림과 console report를 개선했지만 physics assertion은 없다.
또 guide가 LCO charge를 positive delithiation slot에 넣으라고 경고한
반면 sample은 여전히 `direction="discharge"` facade를 사용한다.
저장 PNG는 public experiment, residual과 uncertainty가 없는 model
output이다.

## release PASS의 한계

historical ledger의 build와 source-consistency PASS는 provenance
기록으로 보존한다. 그러나 scientific PASS로 승격하지 않는다.
전페이지 PDF 검독에서 v1.0.12 Ch1 p.37과 Ch2 p.11의 right-edge
clipping이 확인됐고, regression은 public-data validation이 아니다.

다음 Step 30.3에서는 R1 철회가 v1.0.12 source, code, tests와 figure
전체에서 실제로 일관되게 반영됐는지 별도로 판정한다.
