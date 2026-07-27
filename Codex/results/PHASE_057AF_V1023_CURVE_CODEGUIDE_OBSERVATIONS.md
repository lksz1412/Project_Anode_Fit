# Phase 057AF — v1.0.23 curve QA·code guide 관찰

정본일: 2026-07-28
세부 Step: 19.7F
범위: 2 unique documents, 234 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/qa_images/CURVE_QA_v23.md`
- `CODE_GUIDE_v23.md`

두 문건을 첫 행부터 마지막 행까지 전량 검독했다. 이 batch로
v1.0.23 intent queue 13문건 1,190행의 전문 검독을 완료한다.

## Provisional Findings

### INTENT-PROV-0219 — 기본 1C QA가 평형과 겹친다는 보고는 사용자의 출발 관찰을 재현하지 못한다

곡선 QA는 기본 흑연에서 `c=1` 동역학 곡선이 `c=0` 평형과
겹친다고 명시했다. 이유는 `L_V≈7.5e-7 V`가 미해상 guard에
걸려 평형 종으로 돌아가기 때문이다.

사용자의 연구 출발점은 무전류 대비 정전류에서, 특히 저온일수록
dQ/dV peak가 낮아지고 broadening된다는 실험 관찰이다. 따라서
기본 QA 조건은 이 핵심 현상을 보여 주지 못한다.

사용자는 실제 피팅 조건에서는 맞는다고 확인했다. 이 경험적
사실과 v1.0.23 기본 QA는 충돌하지 않는다. fitted barrier나
속도·폭 매개변수가 guard 밖의 해상 regime으로 이동했을 수
있다. 다만 그 성공은 이 문건에 데이터·파라미터·validation
split으로 기록되지 않았다.

판정:

- 기본 1C 곡선의 평형 회귀는 `MOTIVATING_PHENOMENON_FAIL`.
- 사용자가 확인한 실제 fit은 `USER_REPORTED_EMPIRICAL_SUCCESS`로
  보존하고 후속 데이터 감사에서 재현한다.
- 어떤 fitted parameter 조합이 broadening·peak suppression을
  만들었는지와 조건 외 온도·율속 예측을 분리 검증한다.

### INTENT-PROV-0220 — 전압축 매끄러움은 보였지만 parameter-to-output 미분가능성은 보이지 않았다

QA의 격자세분 검사는 선택한 전압 곡선에서 kink가 없는지를
보는 유용한 수치 검사다. 그러나 생산 경로는

`L_V * 40 > grid spacing`

이라는 해상도 기반 hard branch로 평형 종과 lag 경로를
전환한다. 테스트한 `L_V/w=0.3`은 경계에서 떨어져 있으므로
각 분기 내부가 매끄러워도, `L_V`, C-rate, 온도, barrier,
grid spacing을 바꿔 경계를 통과할 때 출력과 gradient가
불연속일 수 있다.

판정:

- 시험한 고정 조건의 voltage-domain smoothness는 `PRESERVE`.
- fitting parameter 및 조건에 대한 연속·미분가능성은
  `UNVERIFIED`.
- 최종 수치 gate는 guard 양쪽 극한, parameter Jacobian,
  grid-invariance를 직접 검사한다.

### INTENT-PROV-0221 — 세분비 약 1만으로 전 구간 C2를 증명했다고 할 수 없다

보고서는 이산 2차도함수의 세분비가 약 1이면 “전 곡선 C2”라고
판정했다. 이는 `x^2`와 `|x|` 캘리브레이션으로 지표 방향을
확인한 좋은 smoke test다.

하지만 유한 표본에서 선택한 norm 또는 최대값이 수렴하는 것은
2차도함수의 전 구간 연속성을 수학적으로 증명하지 않는다.
좁은 전환, grid-aligned branch, 높은 차수의 비매끄러움,
parameter-direction kink를 놓칠 수 있다.

판정:

- C2 smoke test는 `NUMERICAL_EVIDENCE`.
- “전건 C2 증명”은 `SUPERSEDE`.
- analytic branch regularity와 adaptive/local refinement를
  함께 사용한다.

### INTENT-PROV-0222 — 양수·peak 위치·육안 형상은 물리 정상성의 충분조건이 아니다

QA는 graphite/LCO dQ/dV가 양수이고, peak와 shoulder가
그럴듯하며, blend weight 사이 점프가 없다는 이유로
“물리 값 정상”이라 했다. 이는 명백한 부호·발산·연결 결함을
잡는 1차 점검이다.

그러나 capacity integral, 단위, 전압창, 온도·율속 추세,
전극별 독립 데이터, 불확도, charge/discharge hysteresis,
doped high-voltage LCO의 cutoff/degradation 동작을 실험값과
대조하지 않았다.

판정:

- morphology sanity check는 `PRESERVE`.
- 물리 validation 선언은 `REJECT`.
- 공개 데이터 기반의 정량 acceptance가 별도로 필요하다.

### INTENT-PROV-0223 — LCO가 흑연 코어를 거의 전부 상속하는 것은 소프트웨어 재사용이지 물리 동등성의 근거가 아니다

code guide는 LCO가 graphite class를 상속하고
`_effective_dS_rxn` 한 곳만 바꾸며, 중심전위·폭·히스·꼬리
물리를 모두 공유한다고 설명한다. 공통 수학 kernel을 재사용하는
구조는 구현상 간결하다.

그러나 graphite staging과 layered LCO의 상전이·redox·
고전압 구조변화·도핑 안정화는 같은 물리라고 자동 결론낼 수
없다. 특히 사용자가 원하는 doped high-voltage LCO에는
조성·도핑·산소/구조 안정성·전압창에 따른 별도 closure가
필요할 수 있다.

판정:

- 공통 interface/kernel 재사용은 `IMPLEMENTATION_PRESERVE`.
- LCO 물리가 graphite와 거의 같다는 서술은
  `PHYSICALLY_UNVERIFIED`.
- 최종 문헌·데이터 감사에서 공통 보편식과 재료별 free-energy/
  kinetics 항을 분리한다.

### INTENT-PROV-0224 — Si·Si-C는 additive host와 미구현 경계를 스스로 드러낸다

guide는 blend를 graphite host와 Si host의 공통 전위축
가산으로 설명하고, `plastic_hysteresis_loop`와
`nonadditive_correction`을 미구현 stub으로 표시한다.

이는 코드 범위를 숨기지 않은 좋은 기록이지만, Si의 큰
체적변화·응력–화학퍼텐셜 결합·비가역성·SEI/손실, Si-C의
전류분할과 상호작용을 완결하지 못했다는 뜻이다.

판정:

- 현재 additive equilibrium surrogate는 `EMPIRICAL_ONLY`.
- Si/Si-C의 완결 물리모델 지위는 `REJECT`.
- 공개 graphite, Si, graphite+Si 데이터를 따로 식별한 후
  비가산항이 실제로 필요한지를 model comparison으로 판정한다.

### INTENT-PROV-0225 — code guide는 별도 conformance companion의 좋은 출발점이다

6단계 구조도, N0–N9 흐름, 함수–식 사전은 코드가 어떤 식을
계산한다고 주장하는지 빠르게 추적하게 한다. 사용자의 최종
경계에서는 이런 내용이 이론 문건 안에 들어가면 안 되지만,
별도 implementation companion으로는 가치가 크다.

판정:

- guide의 구조와 식 매핑은 `PRESERVE_AND_RELOCATE`.
- 최종 이론 문건에서는 코드 식별자·플래그·guard를 제거한다.
- companion에는 equation ID, symbol, unit, code path, test,
  data gate, status를 기계 판독 가능한 표로 확장한다.

### INTENT-PROV-0226 — 전달함수 helper의 “기기응답 해석용” 표현은 근거를 넘어선다

guide는 `transfer_apparent_from_equilibrium`이 dQ/dV 본류에는
들어가지 않는 별도 FFT helper라고 명확히 밝혔다. 동시에 이를
“기기응답 해석용”이라 부른다.

전압축 exponential smoothing을 계측기 응답으로 해석하려면
실제 acquisition chain, time sampling, voltage ramp, current
control을 포함한 별도 observation model이 필요하다.

판정:

- 본류 비배선 사실은 `PRESERVE`.
- 기기응답 해석은 `UNVERIFIED`.
- 최종 observation layer에서 물리 kinetics, numerical
  smoothing, instrument response를 서로 다른 kernel로 둔다.

### INTENT-PROV-0227 — v1.0.23은 자산은 남기되 최종 물리 기준선으로 채택하지 않는다

v1.0.23 전체를 종합하면 다음은 가치가 있다.

- Fredholm과 Volterra의 문제종 구분.
- 첫 Picard 근사의 조건부 수학.
- additive parity와 식–코드 매핑.
- 재현수치 과장 교정.
- 곡선 smoothness smoke test.

반면 사용자 목표에 필요한 다음은 충족하지 못했다.

- 동기 현상의 기본 조건 재현.
- C-rate 단위 무결성.
- 재료별 LCO/Si/Si-C closure.
- 식별성 및 조건 외 데이터 검증.
- fitting parameter 방향의 미분가능성.

최종 판정:

- v1.0.23 = `NONCANONICAL_METHOD_AND_QA_ASSET`.
- 최종 정본의 직접 기준선으로 쓰지 않고, 검증된 조각만
  provenance와 함께 재합성한다.

## Coverage Status

- 이 batch의 2문건, 234행은 `READ`.
- 누적 coverage 반영 후 목표는 230문건, 48,872행이다.
- v1.0.23은 13/13문건, 1,190/1,190행 전량 `READ`.
- 전체 Phase 057 잔여 목표는 41문건, 8,923행이다.

## Next

Step 19.8:
v1.0.24–v1.0.25.2의 서술 queue를 시간순으로 전문 검독한다.
HTML guide와 machine JSON은 Step 19.9에서 별도 전량
검독·순회한다.
