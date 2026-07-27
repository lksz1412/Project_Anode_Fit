# Phase 057AI — v1.0.24 W4–W6 관찰

정본일: 2026-07-28
세부 Step: 19.8C
범위: 3 unique documents, 247 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/comp_R1/W4/NOTES.md`
- `results/comp_R1/W5/NOTES.md`
- `results/comp_R1/W6/NOTES.md`

세 문건을 첫 행부터 마지막 행까지 전량 검독했다.

## Provisional Findings

### INTENT-PROV-0245 — homogeneous Frumkin 감수율을 `Omega>2RT` 두-상 peak에 그대로 쓰면 안 된다

세 초안은

`dQ/dV = QF / |RT/[theta(1-theta)] - 2 Omega|`

를 Si 단상뿐 아니라 graphite와 LCO의 per-peak Ω까지 통일하는
방향을 제안했다. 이 식은 균일상 chemical-potential branch의
국소 감수율이다.

`Omega>2RT`에서는 자유에너지가 비볼록하고 miscibility gap이
생긴다. 평형은 불안정 branch를 절댓값으로 통과하는 것이 아니라
common tangent/Maxwell construction과 두 공존 조성으로
대체된다. 전압 plateau의 dQ/dV에는 공존구간의 singular
contribution과 단상 날개를 별도로 다뤄야 한다.

판정:

- `Omega<2RT` 단상 감수율 kernel은 `THEORY_CANDIDATE`.
- 동일 식의 절댓값을 `Omega>2RT` 두-상 peak에 적용하는 것은
  `REJECT`.
- v1.0.25.2의 kernel 수정 계보에서 closed-form two-phase
  처리와 연속 임계를 따로 검토한다.

### INTENT-PROV-0246 — `w_eff`는 임계점 중심의 국소 곡률 폭이지 전 peak의 FWHM이 아니다

W4/W5는

`w_eff=(RT/F)(1-Omega/(2RT))`

를 regular-solution 판정자와 기존 logistic 폭 사이의 다리로
사용했다. 이는 `theta=1/2`에서 chemical potential을
선형화한 중심 기울기에 해당한다.

판정:

- 중심 근방 local width scale로는 `DERIVED`.
- 비대칭 전이, multi-gallery envelope, 임계 근처, two-phase
  공존의 전체 FWHM으로 쓰는 것은 `UNVERIFIED`.
- 최종 문건은 local curvature, observed FWHM, heterogeneity
  broadening, kinetic broadening을 다른 기호로 둔다.

### INTENT-PROV-0247 — 창마다 같은 논문의 검증 상태가 달라 서지 tier가 안정되지 않았다

`schmitt2022`에 대해 W5는 웹 검색으로 43℃와 0℃의 구체적
결과가 확인됐다고 썼지만, W6는 원문 전문을 받지 못해 정량
findings가 미검증이라고 썼다. `artrith2018`도 어떤 창은
a-Si 단일상을 직접 지지한다고 단정하고, 다른 창은 서지
존재만 확인했다.

판정:

- DOI/제목 확인은 `BIBLIOGRAPHIC_EVIDENCE`.
- figure·온도·phase conclusion을 원문에서 대조하지 않은
  내용은 `CONTENT_UNVERIFIED`.
- 최종 review matrix는 창별 tier가 아니라 원문 page/equation/
  figure에 연결된 단일 canonical tier를 사용한다.

### INTENT-PROV-0248 — Tu blend 논문의 article number와 직접 인용은 재검증이 필요하다

W5/W6는 같은 DOI에 대해 article number `050520`과 `050539`가
충돌한다고 기록했고, “clearly a superposition”이라는 문구를
blend 가산성의 근거로 사용했다.

판정:

- DOI·article metadata를 1차 출판사에서 다시 확인한다.
- 문구의 실제 문맥이 equilibrium voltage, differential
  capacity, composite electrode response 중 무엇인지 원문에서
  대조한다.
- 단일 인용문만으로 finite-rate current partition과
  nonadditivity가 사라진다고 해석하지 않는다.

### INTENT-PROV-0249 — 공통 regular-solution 골격은 유용하지만 세 재료의 미시 물리를 통일하지 않는다

W6의 목표는 graphite, Si, LCO를 한 Ω 판정자로 묶는 것이다.
혼합 자유에너지의 convexity라는 공통 수학은 비교에 유용하다.

그러나 각 재료의 order parameter와 상공간은 다르다.

- graphite: stage와 sublattice ordering.
- a-Si: amorphous network, stress, path dependence.
- LCO: Li/vacancy ordering, redox, layered structural transition,
  high-voltage degradation and dopant effects.

판정:

- 공통 thermodynamic template는 `PRESERVE`.
- 하나의 scalar Ω와 동일 peak kernel로 미시 물리를 대체하는
  것은 `REJECT`.
- 최종 문건은 공통 변분 구조와 재료별 free-energy functional/
  kinetics를 계층적으로 구분한다.

### INTENT-PROV-0250 — “무근거 수치 0”은 tier 표기가 있다는 뜻이지 물리 검증 완료가 아니다

W4–W6는 수치마다 seed 또는 내부 artifact를 연결해 출처 없는
숫자를 피했다. 동시에 다음을 스스로 미검증·tier-C로 남겼다.

- stage-2L 개별 entropy 배정.
- Si Ω와 gallery 수.
- LCO per-peak Ω와 electronic-entropy 다온도 영향.
- LCO feature label과 전압 anchor.
- graphite regular-solution vector의 transition ordering.

판정:

- provenance 표시는 `PRESERVE`.
- “무근거 수치 0”을 “외부 검증 수치만 사용”으로 읽지 않는다.
- 최종 parameter table은 source, inference method, uncertainty,
  calibration set, transferability를 모두 기록한다.

### INTENT-PROV-0251 — 초안들이 발견한 모순 목록은 정본보다 중요한 감사 자산이다

W4–W6는 다음을 반복해서 플래그했다.

- graphite §7 분류와 seed의 직접 충돌.
- `tab:staging` entropy와 새 stage-2L seed의 충돌.
- LCO O2/O3와 T1/T2/T3의 충돌.
- blend 논문 metadata 불일치.
- `Omega→0` 폴백과 electronic toggle의 bit-exact 전제.

판정:

- 이 honest gaps를 후속 문구로 덮지 않고 결함 ledger에
  유지한다.
- 최종 합성 전 각 항목은 `resolved by source`,
  `resolved by data`, `model choice`, `still unknown` 중 하나로
  닫혀야 한다.

## Coverage Status

- 이 batch의 3문건, 247행은 `READ`.
- 누적 coverage 반영 후 목표는 242문건, 49,664행이다.
- 전체 Phase 057 잔여 목표는 29문건, 8,131행이다.

## Next

Step 19.8D:
W7–W9 NOTES 3문건 303행을 전문 검독한다.
