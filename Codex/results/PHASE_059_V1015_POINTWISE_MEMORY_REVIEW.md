# Phase 059 v1.0.15 점별 연속 메모리 독립 재유도

상태: `CONDITIONAL_P059_V1015_POINTWISE_MEMORY_CORE_PRESERVED_BUT_FINITE_WINDOW_RESOLUTION_SWITCH_AND_CHRONOLOGY_FAIL`

## 결론

v1.0.15는 v1.0.14의 숨은 `V_work`·역보간과 두-grid-step 전환을 제거한 **실질적 개선**이다. 정규화된 지수 기억 커널, 선형 구간 적분, 넓은 전압창의 용량 보존과 고정 방향 충·방전 거울은 보존한다.

그러나 “모든 평가점에서 연속이며 격자와 무관하다”는 강한 해석은 성립하지 않는다. 유한창 첫 상태가 이론의 무한 과거 경계와 다르고, `char_h/L_V=40`에서 여전히 샘플링 의존 전환이 있으며, 전압 정렬이 실제 protocol chronology를 지운다.

## 독립 유도

진행 좌표를 \(s\)라 하면 \(\mathrm d\xi/\mathrm ds=(\xi_\mathrm{eq}-\xi)/L\)이고, 유한 초기점 해는

\[\xi(s)=e^{-(s-s_0)/L}\xi(s_0)+\frac1L\int_{s_0}^{s}e^{-(s-u)/L}\xi_\mathrm{eq}(u)\,\mathrm du.\]

\(s_0\to-\infty\)의 정규화 convolution은 초기항이 소멸할 만큼 충분한 prehistory가 있을 때만 이 해와 같다. 또한 \((\xi_\mathrm{eq}-\xi)/L=\mathrm d\xi/\mathrm ds\)이므로 면적은 시작과 끝의 실제 상태 차이다. 따라서 유한 창에서는 초기 상태를 생략할 수 없다.

## 보존되는 수학과 개선

- 불규칙 7점에서 상수·선형 source recurrence 오차는 각각 `0.000e+00`, `0.000e+00`다.
- 넓은 창의 평형/지연 면적은 `1.000000000000`, `0.999999999997`로 Q=1을 보존한다.
- direct \(L_V=0.02\)에서 peak는 `12.500000`→`10.810830`로 낮아진다.
- 대칭 단일 전이의 충·방전 거울 최대 오차는 `0.000e+00`다.
- v1.0.14의 22.925% 두-grid-step handoff를 제거했고, 입력 좌표로 직접 반환한다.

## 새로 확인한 결함

### 1. 유한 전압창 초기조건

이론은 \(-\infty\)부터의 과거를 적분하지만 코드는 첫 점에서 `xi_lag=xi_eq`로 둔다. [-0.05, 0.2] V만 독립 호출하면 첫 peak는 `0.000000`, 넓은 창의 실제 과거를 유지하면 `1.847424`다. 같은 crop에서 최대 차이는 `1.847424`, 면적은 `0.923653` 대 `0.960601`다.

### 2. 해상도 cap은 여전히 유한 전환이다

입력 간격 `0.01` V에서 cap 경계는 `L_V=0.00025` V다. 경계 아래는 평형 종, 경계 위는 cell-average memory 종이 되며 최대 jump는 `1.194267` (9.554% of equilibrium peak)다. 따라서 “물리 분기가 아니며 불연속이 없다”는 주장은 기각한다.

### 3. 숨은 격자 제거와 sampling independence는 다르다

작업격자와 역보간은 사라졌지만 logistic source를 구간별 선형으로 근사하므로 supplied sampling에 따라 수렴한다. 0.01 V와 0.0001 V 입력을 같은 좌표에서 비교한 최대 차이는 `0.079297`다.

### 4. 실제 시간 이력을 계산하지 않는다

전압 좌표를 섞은 뒤 원위치로 복구해도 출력 차이는 `0.000e+00`다. 반면 입력 순서를 실제로 따라간 recurrence와는 기존 독립 probe에서 `21.329615` 차이가 났다. pulse·rest·loop·reversal의 시간 이력 모델로 사용할 수 없다.

### 5. 기존 동역학 blocker는 고쳐지지 않았다

`func_L_q`와 lag resolver의 executable AST는 v1.0.14와 동일하다. 따라서 3,600 시간단위 인자, 컷점에 동결된 affinity, 전극-scale coarse graining 부재는 그대로다. direct `L_V`는 I=0에서도 활성이고, derived overflow는 다시 L_V=0 평형으로 뒤집힌다.

## 최종 처분

점별 지수 커널은 monotone sweep의 **축약 수학 모형**으로 보존한다. 실제 정전류 protocol에는 전압 정렬이 아니라 부호 있는 시간/용량 상태 적분, 명시 초기 상태, current conservation과 terminal-voltage closure가 필요하다. 평형 극한은 sampling threshold 없이 연속적인 수치식으로 구현해야 한다.

다음은 Step 37.2: 방향, 초기조건, 유한창, tail, mirror, scalar/vector와 golden rebaseline의 구현 경계 종합 판정이다.

원본 `Claude/`, `main`과 생산 이론·코드는 수정하지 않았다.
