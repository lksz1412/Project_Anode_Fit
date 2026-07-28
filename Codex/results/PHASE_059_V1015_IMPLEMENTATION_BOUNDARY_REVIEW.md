# Phase 059 v1.0.15 구현·상태·golden 경계 감사

상태: `CONDITIONAL_P059_V1015_MONOTONE_CURVE_KERNEL_PRESERVED_BUT_STATE_WINDOW_PROTOCOL_AND_GOLDEN_AUTHORITY_FAIL`

## 결론

v1.0.15의 pointwise kernel은 **포화 경계가 포함된 단조 전압곡선
평가기**로는 보존한다. 그러나 초기상태를 받거나 최종상태를 반환하지
않고, 배열을 시간순서가 아닌 좌표 집합으로 정렬하며, 하나의 방향
flag만 받는다. 따라서 정전류 pulse·rest·reversal을 연결하는 stateful
protocol solver는 아니다.

## Scalar와 sweep은 같은 물리 상태가 아니다

V=0에서 scalar와 singleton 출력은 각각
`12.500000000`, `12.500000000`로 평형값이다.
같은 좌표가 sweep 안에 있을 때는 `9.657353106`다.
차이 `2.842646894`는 버그라기보다
scalar가 과거 없는 stateless query임을 뜻한다. 다만 “모든 평가점에서
pointwise”라는 표현은 이 상태 의존성을 감춘다.

공개 `dqdv` 인자는 `self, V_app, T, I_abs, Q_cell, s`뿐이다. 초기 \(\xi\), 시간,
이전 state 입력과 final state 반환이 모두 없다.

## 유한창 tail과 용량

| Upper V | Area | Missing Q | Terminal density |
|---:|---:|---:|---:|
| 0.05 | 0.788311420 | 0.211688580 | 6.791505860 |
| 0.10 | 0.966264919 | 0.033735081 | 1.352108711 |
| 0.15 | 0.995851548 | 0.004148452 | 0.179783315 |
| 0.20 | 0.999545997 | 0.000454003 | 0.020430212 |
| 0.30 | 0.999995411 | 0.000004589 | 0.000214132 |
| 0.60 | 1.000000000 | 0.000000000 | 0.000000000 |

면적 부족은 수치 오차가 아니라 창 끝에서 아직 완료되지 않은 상태
변화다. 관측창 밖 잔여 상태를 반환하지 않으므로 fitting window를
바꾸면 같은 전이 Q의 관측 면적도 바뀐다.

## 방향과 이력

- 고정된 단조 charge/discharge mirror 오차는
  `0.000e+00`다.
- 같은 방향에서 입력을 오름차순/내림차순으로 주고 복구하면 차이는
  `0.000e+00`다.
- 이는 정렬된 curve 평가에는 유용하지만 측정 순서를 보존한다는
  뜻이 아니다. 한 호출 안에서 reversal/rest를 표현할 state machine도 없다.

## 비등온 경로의 sampling-density 의존

동일한 선형 280→320 K 경로를 균일 샘플링하면 평균 T는
`300.000000` K, 저전압에 점을 몰아주면
`291.673605` K다. 전이당 한 번 쓰는 lag는
`0.542553`→`1.394176` V
(2.570배)로
바뀌고, 보간 후 출력 최대 차이는
`0.684058`다.
물리 경로가 아니라 파일의 점 밀도가 kinetic parameter를 바꾸므로
mean-T closure는 기각한다.

## Golden rebaseline

commit `03dab9221d9b`에서 code와 golden은 함께
변했고 test harness는 그대로였다. 13개 중 11개 array의 architecture
delta가 현재 재계산과 최대 `4.330e-15`로
일치하므로 **의도적 출력 snapshot**이라는 계보는 보존한다.

그러나 harness는 자기 출력을 capture하고 같은 함수로 verify한다.
direct `L_V`, nonmonotone, reversal, pulse, SI-Coulomb와 실험 데이터는
전부 0 occurrence다. evidence class는
`DERIVED_MODEL_OUTPUT_SNAPSHOT`이며 독립 oracle이나 과학 검증이 아니다.

## 인수 경계

보존 범위는 “포화 경계를 포함한 단조 curve의 reduced exponential
memory”다. 실제 데이터 protocol에는 다음이 필요하다.

1. 명시적 initial/final state
2. 시간 또는 signed capacity 순서의 적분
3. reversal/rest에서 segment 상태 연속 전달
4. 관측창 밖 remaining capacity 회계
5. local T와 current를 쓰는 state rate
6. 위 항목을 고정된 외부 oracle로 검사하는 독립 시험

다음은 Step 37.3: v1.0.15 Ch2 발열 상세화가 새 물리인지 worked
explanation인지, 문건과 code가 같은 열역학 quantity를 쓰는지 판정한다.

원본 `Claude/`, `main`과 생산 이론·코드는 수정하지 않았다.
