# Phase 057AB — v1.0.23 조건감사·P1 관찰

정본일: 2026-07-28
세부 Step: 19.7B
범위: 2 unique documents, 413 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/comp_v23/COND_AUDIT.md`
- `results/PHASE_P1_RESULT.md`

`COND_AUDIT.md`는 1–200, 201–301의 연속 구간으로 나누어
전량 읽었고, P1 결과도 첫 행부터 끝 행까지 검독했다.

## Provisional Findings

### INTENT-PROV-0194 — P1은 Fredholm 원문과 lag 문제의 종이 다름을 정확히 발견했다

조건감사는 사용자 논문의 문제가 고정구간 전역
Fredholm 2종인 반면, 문건 lag는 가변상한·인과·Markov인
Volterra 2종이며 1계 전진 ODE와 동등함을 명시했다.

따라서 사용자 논문의 방법을 문자 그대로 이식할 수 없고,
“미지 비를 가해 기준 비로 치환한다”는 철학만 옮겼다.
또한 원 문제가 이미 O(N) 전진해라 ratio가 계산량을 줄인다는
초기 셀링포인트를 철회했다.

판정:

- 종의 차이와 계산절감 철회는 `PRESERVE`.
- 이 접목은 새로운 필수 solver가 아니라 선택적 1차
  perturbative approximation이다.
- “Fredholm 방법이 graphite lag를 해결했다”는 요약은 `REJECT`.

### INTENT-PROV-0195 — 1차 ratio 보정은 선택한 surrogate 안에서는 Picard 1회와 같다

P1이 쓴 참 문제는

`dr/dV = sigma(V) - r kappa(xi)`,
`xi=xi_eq-r`

이고, 0차 동결 궤적 `xi_0`에서 `kappa(xi_0)`를 평가해 한 번
전진한 것이 1차 ratio 보정이다. 즉 수학적으로는 동결 기준의
첫 Picard iterate 또는 기준궤적 선형화다. 상태 의존성이 작으면
0차 오차의 선형항을 제거해 2차 오차가 되는 결과는 예상되는
섭동 구조이며 내부 수치도 이를 재현한다.

판정:

- 이 수학적 해석은 `PRESERVE`.
- “ratio” 명칭만으로 일반적인 수렴·물리 정확성이 보증되지는
  않는다.
- 정확 비선형 ODE, 0차 동결, 1차 Picard를 같은 synthetic
  constitutive law에서 비교한 것은 근사 차수 검산이지
  실험 검증이 아니다.

### INTENT-PROV-0196 — P1의 상태의존 lag law와 유효성 부등식은 가정된 closure다

검산은

`L_V(xi)=L_0 exp[2 chi_d (Omega/RT)(1-xi)]`

라는 상태 의존성을 참값으로 놓았다. 그러나 이는 물질별 전이
장벽·prefactor·affinity로부터 독립 검증된 law가 아니라,
기존 effective-barrier 해석을 격리한 surrogate다.

`epsilon = 2 chi_d (Omega/RT) Delta xi_supp`,
`Delta xi_supp ≈ L_V/(4w)`

도 logistic 최대 기울기와 kernel support의 국소 규모 추정이다.
유용한 작은-파라미터 진단이지만 전역 rigorous bound나
실험적으로 식별된 물질 기준은 아니다.

판정:

- `epsilon`은 `LOCAL_PERTURBATION_DIAGNOSTIC`.
- 보편 물리 상수 또는 automatic acceptance threshold로 쓰지
  않는다.
- 재료·온도·율속별 실제 `L_V(xi)`가 데이터와 독립 관측으로
  지지되기 전 ratio 효과를 상전이 장벽의 검증으로 해석하지 않는다.

### INTENT-PROV-0197 — “기본상태 lag 휴면” 결론은 C-rate 단위 재감사 전 무효다

P1은 `L_V/w≈10^-8`을 기본상태로 두고 ratio가
`0.1≲L_V/w≲0.6`에서만 유용하다고 결론냈다. 그러나 v1.0.22
재감사에서 C-rate 숫자를 `h^-1`에서 `s^-1`처럼 사용한
3,600배 시간 단위 문제가 발견됐다.

이 오류는 `L_q=|I|/(Q_cell k)`와 `L_V`를 직접 바꾸며
barrier에 `RT ln 3600` 규모로 흡수될 수 있다.

판정:

- 기존 `L_V/w` 수치와 “휴면 regime”은 `UNVERIFIED`.
- SI 시간 단위 교정과 barrier 재식별 후 전부 재계산한다.
- 차원 없는 synthetic sweep에서 얻은 유효성 창은 형식 결과로만
  보존한다.

### INTENT-PROV-0198 — 문헌 grounding은 부분적이며 방법론 권위의 완결 검증이 아니다

P1은 JCP147 추출 텍스트에서 Ref.6·7 서지와 Fredholm/ratio
문구를 확인했지만, 사용자 논문의 PDF page/paragraph와 Ref.6·7
원문은 확보하지 못했다고 명시했다. 그럼에도 후속 부록 저작을
허용했다.

판정:

- 사용자 논문 서지와 자기 인용 계보는 `PARTIALLY_VERIFIED`.
- 원 방법의 가정, 오차, 변수 의미를 Ref.6·7 원문에서 확인하기
  전 “충실한 이식”을 확정하지 않는다.
- 최종 문헌 조사는 DOI 존재뿐 아니라 원문 식·가정·적용 범위를
  직접 대조한다.

## Coverage Status

- 이 batch의 2문건, 413행은 `READ`.
- 누적 coverage 반영 후 목표는 221문건, 48,124행이다.
- v1.0.23 잔여 목표는 9문건, 748행이다.

## Next

Step 19.7C:
P2 부록 E와 P3 코드 적용 결과 2문건 216행을 전문 검독한다.
