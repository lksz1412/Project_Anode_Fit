# Phase 057Z — v1.0.22 R6–R9·AUD·v1.0.23 survey 관찰

정본일: 2026-07-28
세부 Step: 19.6K
범위: 16 unique documents, 2,061 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 R6 코드 구현, R7 그림 검산, R8 이월 집행, 독립 AUD,
R9 handover/index/merge-readiness, v1.0.23 수학 survey를 첫
행부터 끝 행까지 검독했다.

- `results/comp_R6/R6_REPORT.md`
- `results/comp_R7/F1_NOTE.md`
- `results/comp_R7/F2_NOTE.md`
- `results/comp_R8/R8_EXEC.md`
- `results/comp_AUD/AUD1_CH1.md`
- `results/comp_AUD/AUD2_CH2.md`
- `results/comp_AUD/AUD3_CH3.md`
- `results/comp_AUD/AUD4_CODE.md`
- `results/comp_v23/SURV1_integral_transform.md`
- `results/comp_v23/SURV2_asymptotic_pert.md`
- `results/comp_v23/SURV3_convex_inverse.md`
- `results/comp_v23/SURV4_bifurcation_stochastic.md`
- `results/comp_v23/SURV_SYNTHESIS.md`
- `results/INDEX_v1022.md`
- `results/HANDOVER_v1.0.22.md`
- `results/MERGE_READINESS.md`

## Provisional Findings

### INTENT-PROV-0183 — R6는 정해진 축약 명세를 잘 구현했지만 실험물리를 검증하지 않았다

R6와 AUD4가 확인한 구현 정합성은 실제다.

- graphite와 Si host를 같은 전위 축에서 평가한다.
- pooled charge-balance로 단일 `U_oc` 근을 푼다.
- `m_Si` wt%를 내부 `f_Si` 용량분율로 정확히 환산한다.
- `C_bg`를 한 번만 싣고 `f_Si=0`에서 graphite 경로를
  bit-exact로 회수한다.
- background-subtracted 적분으로 용량을 보존한다.

그러나 이 gate들은 동일한 가정·시연값으로 생성한 결과의 대수,
부동소수점, 연속성, 회귀를 검사한다. 공개 실험 데이터에 대한
잔차, peak 위치·높이·폭, 온도·율속 전이, held-out 예측은
검사하지 않는다.

판정:

- common-potential additive equilibrium implementation은
  `INTERNAL_VERIFICATION_PASS`.
- “실제 Si/blend 데이터 피팅 모델 완성” 또는
  `EXPERIMENTAL_VALIDATION_PASS`로 승격하지 않는다.
- 코드–문건 표면 대응표와 문건–물리 검증표를 별도 관리한다.

### INTENT-PROV-0184 — Si 계열 코드는 시연 곡선 생성기이며 생산 물질 모델이 아니다

R6가 명시한 미구현·placeholder는 다음과 같다.

- GS-1 plastic hysteresis는 `NotImplementedError`.
- GS-2 finite-rate nonadditivity와 host current partition은
  `NotImplementedError`.
- Si 열역학 반응 엔트로피가 없어 blend reversible heat가 없다.
- SiO_x 절대 평균전위와 히스테리시스는 미확보다.
- elemental Si, SiO_x, Si–C의 전이 중심·폭은 tier-C demo set이다.

특히 `SIOX_LIT['U']=0.300 V`는 elemental-Si 계열의
0.2–0.5 V 범위에서 택한 placeholder다. 경고를 붙인 것은
정직하지만, 측정 또는 유도로 정해진 값이 아니므로
“임의값이 아니다”라는 자기 설명은 받아들일 수 없다.

판정:

- demo set은 `SCHEMATIC_ONLY`; 생산 default 또는 literature
  parameter로 사용하지 않는다.
- 미확보 물리값은 경고와 함께 계산을 계속하는 것보다 명시적
  `None`/unsupported로 실패시키는 것이 사용자 원칙에 맞다.
- 실제 데이터 fit에서는 재료·조성·처리·protocol별 관측 근거로
  상태와 parameter prior를 다시 세운다.

### INTENT-PROV-0185 — common-potential 가산 모델의 유한전류 확장은 아직 닫히지 않았다

평형에서 두 host를 같은 `V_n`에 놓고 전하를 합하는 것은 유효한
zero-order baseline이다. 그러나 finite-current `dqdv`에서 두
host 진입점에 같은 전극 전류를 각각 전달하면, 실제 graphite/Si
반응전류 분배와 host별 과전압을 유도한 것이 아니다.

전류 분배는 exchange current, active area, transport, stress,
local SOC, interfacial impedance에 따라 달라질 수 있다. 현재
R6의 “같은 전위 배열에서 host 곡선을 더함”은 이 동역학을
해결하지 않는다. 문건 스스로 GS-2로 남긴 이유도 이것이다.

판정:

- additive blend는 equilibrium/low-rate baseline으로만
  `PRESERVE`.
- finite-current peak suppression·broadening을 설명하는
  생산 모델로 사용할 때는 host current partition과 terminal
  voltage observation map을 새로 유도해야 한다.
- GS-2를 단순 correction 함수 한 개로 미리 규정하지 않는다.

### INTENT-PROV-0186 — R7 그림은 코드 시연의 시각 검산이지 실험 증거가 아니다

F1·F2 좌표는 코드 출력과 정확히 일치하고 면적·환산·bit-exact
검산도 통과한다. 그러나 그림이 보여주는 peak 축소와 Si 기여
성장은 총용량 정규화와 선형 가산의 직접 귀결이다. F2의
SiO_x 가로 위치는 placeholder이며, 세 케이스 형상도 tier-C
전이 리스트에서 생성된다.

판정:

- 이 그림들은 `MODEL_SCHEMATIC` 또는 `INTERNAL_REGRESSION`으로
  표기할 수 있다.
- 실험 그림, 문헌 재현, 물질별 예측으로 부르면 안 된다.
- 최종 문건에는 공개 raw data, protocol, uncertainty와 대조한
  그림을 별도로 만들고, placeholder 좌표는 정량 패널에서
  제외한다.

### INTENT-PROV-0187 — AUD의 “치명 0”은 제한된 acceptance boundary 안에서만 참이다

AUD1–AUD4는 앞선 수정의 산술·문면·코드 정합을 독립 재계산했고,
여러 잔여 오류도 찾았다. 이 검수는 가치가 높다. 동시에 질문은
대체로 “기존 명세를 정확히 고쳤는가”, “게이트 뒤에 숨은
correctness bug가 있는가”였다.

따라서 다음 둘은 동시에 참이다.

1. 해당 수정과 R6 구현은 지정 명세 안에서 치명 결함이 없다.
2. 명세 자체에는 물질 closure와 실험 validation이 크게 비어 있다.

판정:

- `NO_FATAL_WITHIN_DECLARED_SCOPE`를 전체 과학적 타당성으로
  확대하지 않는다.
- 최종 gate는 algebra, implementation, literature, experiment,
  transferability를 각각 판정한다.

### INTENT-PROV-0188 — v1.0.23 수학 survey에는 유용한 도구와 물리적 과해석이 섞여 있다

보존 가치가 큰 후보는 다음이다.

- Legendre–Fenchel 관점으로 요동양성, 볼록성, 유일근,
  공통접선을 연결.
- Fisher information으로 온도점 설계·공선형·sloppy direction을
  정량화.
- causal exponential kernel의 Watson 전개로 shift, variance,
  skewness를 분리.
- inverse problem을 forward physics와 분리.

반면 그대로 채택하면 안 되는 항목도 있다.

- `H(k_V)=1/(1+i k_V L_V)`는 전위 좌표 합성곱의 Fourier
  전달함수다. 이를 곧바로 측정기 instrument response 또는
  평형 동적 감수율로 부르면 범주 오류다. 시간 응답으로 읽으려면
  명시적 ramp `V(t)`와 `k_t` 변환이 필요하다.
- survey가 “기본 `L_V/w`가 10^-8 수준이라 휴면”이라고 한
  결론은 앞서 발견한 C-rate hour/second 3,600배 문제에
  의존할 수 있어 재계산 전 신뢰할 수 없다.
- SURV2는 3/2 지수를 mean-field spinodal 결과로 한정하고
  실계 임계 rounding을 경고하지만, SURV4는 이를
  “평균장 특유가 아닌 보편 지수”라고 쓴다. 둘은 그대로는
  양립하지 않는다.
- 사용자 논문의 Fredholm ratio를 “확정 본체”로 부르면서도
  ref.6·7 원문은 미확인이라고 기록했다. 원문·변수 사상 확인
  전에는 후보일 뿐이다.

판정:

- 수학 명칭 추가보다 물리 적용 조건과 차원·좌표를 먼저 검증한다.
- `H`는 우선 voltage-domain smoothing operator로만 둔다.
- C-rate 단위 교정 뒤 Watson/transfer-function 규모를 재평가한다.
- cusp/critical exponent 문구는 원 자유에너지와 fluctuation
  universality class를 구분해 다시 유도한다.
- 미확인 사용자 논문 방법을 권위로 선취하지 않는다.

### INTENT-PROV-0189 — 식별성과 역문제는 필수지만 물리 본문과 분리해야 한다

SURV3가 제안한 Fisher information, Cramér–Rao bound,
Bayesian posterior, multi-start/비볼록성 진단은 실제 피팅
완결에 필요하다. 특히 “fit이 된다”와 “파라미터가 식별된다”를
가르는 핵심 도구다.

그러나 이는 자유에너지·전기화학·동역학의 물리 유도와 같은
본문 층이 아니다.

판정:

- physics-only manuscript에는 실험설계와 식별성의 물리적
  필요조건만 간결히 둔다.
- objective, optimizer, priors, FIM, uncertainty, held-out
  protocol은 별도 fitting/validation companion에 둔다.
- forward 모델과 inverse inference가 서로의 가정을 숨기지
  않도록 equation/parameter provenance ID로 연결한다.

### INTENT-PROV-0190 — R9 상태 문건은 말기 수정 전후가 섞여 단독 정본이 될 수 없다

동일 v1.0.22의 상태 문건 사이에 직접 충돌이 있다.

- `HANDOVER_v1.0.22.md`는 Part II 제목과 Moyassari 등재가
  C-055로 완료됐다고 적는다.
- `MERGE_READINESS.md`는 같은 두 항목을 아직 사용자 결정
  대기라고 적는다.
- handover의 다음 버전 후보에도 이미 완료된 Moyassari
  등재 조건이 다시 남아 있다.
- 장 요약의 “f_Si 0–30%” 표현은 후속 `m_Si` wt% 규약보다
  오래된 표기다.

이는 문서 생성 시점과 후속 patch 전파가 달랐기 때문이다.

판정:

- handover/index/merge readiness의 자기 보고를 그대로 최신
  상태로 믿지 않는다.
- 실제 source, change log의 시간순 commit, tests를 함께 대조한다.
- 새 작업에서는 모든 상태 문건에 `as_of_commit`과 superseded
  marker를 넣고, 완료된 decision의 stale 재등장을 gate로 막는다.

### INTENT-PROV-0191 — v1.0.22의 최종 평가는 “강한 내부 정합성, 미완의 물질·실험 모델”이다

v1.0.22는 다음을 크게 진전시켰다.

- thermodynamic/statistical-mechanical derivation의 교육적 구조.
- graphite/LCO/Si 장 분리와 cross-reference.
- 많은 대수·부호·단위·조판 오류의 검출·수선.
- additive equilibrium blend의 명세–코드 일치.
- 기록·gate·handover 문화.

그러나 사용자가 원하는 최종 목적에는 아직 못 미친다.

- doped high-voltage LCO의 degradation/oxygen/structure/electronic
  coupling이 물질별로 닫히지 않았다.
- Si/SiO_x/Si–C의 plasticity, first-cycle chemistry, interphase,
  rate-dependent host coupling이 없다.
- finite-current peak lowering/broadening과 temperature dependence가
  public data로 검증되지 않았다.
- 다수 파라미터는 demo·tier-C·placeholder이며 식별성 검증이 없다.
- physics manuscript와 code specification이 섞였다.

판정:

- v1.0.22는 `VALUABLE_INTERMEDIATE_BASELINE`.
- 최종 이론·코드의 과학적 권위로는 `NOT_YET_ACCEPTED`.
- 다음 버전의 고등수학 증축보다 먼저 material closure,
  observables, data/protocol validation을 우선한다.

## Coverage Status

- 이 batch의 16문건, 2,061행은 `READ`.
- 누적 coverage 반영 후 목표는 217문건, 47,682행이다.
- v1.0.22는 101/101문건, 16,855/16,855행 전량 `READ`가 된다.
- Phase 057 전체 잔여는 54문건, 10,113행이다.

## Next

Step 19.7:
v1.0.23 intent queue의 전 문건을 고유 blob 기준으로 편성하고
사용자/Fable 진행, Fredholm·전달함수 채택, 후속 철회와
v1.0.24로 이월된 결함을 전문 검독한다.
