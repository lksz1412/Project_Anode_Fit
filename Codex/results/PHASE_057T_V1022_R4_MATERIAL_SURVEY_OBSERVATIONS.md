# Phase 057T — v1.0.22 R4 재료 조사·승급 관찰

정본일: 2026-07-28
세부 Step: 19.6E
범위: 11 unique documents, 1,047 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 R4 저비용 조사와 후속 승급 조사 문건을 첫 행부터 끝 행까지
검독했다.

- `comp_R4/BRIEF_R4.md`
- `comp_R4/BLEND_ALIGN.md`
- `comp_R4/L2_REGISTER_PREP.md`
- `comp_R4/L5_RESOURCE.md`
- `comp_R4/REPORT_R4_COMPLETE.md`
- `comp_R4/SI_CASES.md`
- `comp_R4/SI_ENTROPY.md`
- `comp_R4/upgraded/BLEND_UP.md`
- `comp_R4/upgraded/SIC_CASES.md`
- `comp_R4/upgraded/SIOX_CASES.md`
- `comp_R4/upgraded/SI_ENTROPY_UP.md`

## Provisional Findings

### INTENT-PROV-0125 — 저비용 검색의 0건은 네 축 모두에서 뒤집혔다

초기 R4는 SiO_x, Si–C, Si entropy, graphite–Si blend dQ/dV를
각각 0건으로 닫았다. 후속 검색은 query를 확장해 다음을 찾았다.

- SiO_x 5건.
- Si–C 3건.
- Si/Si–C entropy·열 관련 6건.
- blend 이론·실측·상용 scale 8건.

판정:

- “검색 0건 = 문헌 부재”가 아니라 search breadth 실패였다는
  `INTENT-PROV-0102`를 재확인한다.
- 최종 조사는 동의어, 측정법, 재료 상품명, composite/blend,
  entropymetry/calorimetry, citation chain을 함께 사용한다.

### INTENT-PROV-0126 — 공통 μ와 동시 반응전류가 혼동됐다

`BLEND_ALIGN.md`와 `BLEND_UP.md`는 공통-μ 골격을
“두 host가 같은 전위에서 동시에 반응”하는 가정으로 설명하고,
SoC에 따라 graphite와 Si의 우세 반응전류가 바뀌는 결과를
그 가정의 반례 또는 편차로 해석한다.

그러나 다음은 구분해야 한다.

- 평형 또는 국소 계면에서의 공통 전기화학 퍼텐셜/전극 전위.
- host별 OCV 차이.
- host별 exchange current, overpotential, diffusion,
  active area와 반응전류 분배.
- host–host 상호작용 및 전극 두께 방향 비균일.

공통 전위는 host별 전류가 같거나 항상 동시에 유의미하다는 뜻이 아니다.

판정:

- 공통 전위 아래 host별 보존식을 묶는 골격은 `PRESERVE`.
- 단순 capacity-weighted 평형곡선 합만으로 전류 분배까지 설명하는
  것은 `REJECT`.
- 최종 코드는 공통 terminal potential과 host-specific kinetics/state를
  분리하고 합계 전류·합계 Li 보존으로 결합해야 한다.

### INTENT-PROV-0127 — wt%와 capacity fraction이 다시 혼용됐다

후속 blend 조사는 실험의 Si `5–30 wt%` 범위를 확보한 뒤,
이를 마스터의 `f_Si=Q_Si/Q`와 같은 축처럼 “0–30% 전 구간 커버”로
서술했다. 그러나:

- wt%는 제조 질량분율.
- `f_Si=Q_Si/Q`는 용량분율.
- Si와 graphite의 specific capacity가 크게 달라 두 값은 같지 않다.

판정:

- 실험 입력은 mass fraction, 내부 보존 가중은 capacity fraction으로
  분리한다.
- 재료별 가역 specific capacity, ICE, cycle/state 의존을 거쳐
  명시적으로 변환한다.
- wt% 데이터를 `f_Si` 직접 초기값으로 사용하는 것은 `REJECT`.

### INTENT-PROV-0128 — 문헌 tier가 서지 확인과 정량 검증을 혼합했다

R4는 DOI, 검색 초록 또는 landing page가 확인되면 일부 항목을
tier A로 올렸다. 동시에 같은 문건은 다음을 인정한다.

- EES 2020 전문 403, 전 저자와 정량 `ΔS` 미확인.
- Reynier 2004의 특정 `0.18 k_B/atom` 및 질서상 수치 미확인.
- 일부 Crossref 문헌은 초록·정량 데이터 미확보.
- “분해 실측” 중 일부 성분은 계산/해석일 가능성을 분리하지 않음.

판정:

- bibliographic existence, method verification, qualitative result,
  exact numerical value, equation verification를 별도 evidence field로 둔다.
- DOI/abstract 확인만으로 정량 parameter를 tier A default로
  승격하는 것은 `REJECT`.

### INTENT-PROV-0129 — charge-order 0.47/1.49 값의 재소싱은 성공하지 않았다

`L5_RESOURCE.md`는 Reynier 2004와 EES 2020을 “부분 성공” 대안으로
제시했지만 두 원전에서 `0.47/1.49 J mol⁻¹ K⁻¹` 자체를 확인하지 못했다.
또 `x=2/3→5/6` 변경을 제안했으나 이는 서로 다른 질서상을 기존 T3에
재배정하는 새 해석이며, 원 값과 슬롯의 대응을 입증하지 않는다.

판정:

- 기존 두 수치의 재소싱은 `FAIL/UNVERIFIED`.
- Motohashi 귀속 제거 후보는 유지하되 다른 문헌에 수치를
  재귀속하지 않는다.
- 정확 값이 필요하면 각 원문의 `ΔS(x)` 정의·정규화·조성·전압과
  현재 전이 슬롯의 mapping을 새로 구축한다.

### INTENT-PROV-0130 — 원소 Si 자료에도 즉시 재검증할 수치 오류가 있다

`SI_CASES.md`는 `Li15Si4` 이론용량을 약 `4200 mAh g⁻¹`로 적었다.
이는 통상 `Li15Si4` 조성에서 계산되는 약 `3579 mAh g⁻¹`과
일치하지 않으며, 약 4200은 더 높은 Li/Si 비의 역사적 최대용량
표현과 섞였을 가능성이 있다.

판정:

- 이 값은 Phase 063/문헌 원문에서 직접 재계산·재검증하기 전
  `UNVERIFIED`.
- 최종 수치 원장은 화학식으로부터 Faraday-law 재계산한 값과
  원전 보고값을 나란히 보관한다.
- “17건 검증 완료”라는 묶음 선언으로 개별 수치까지 승인하지 않는다.

### INTENT-PROV-0131 — SiO_x의 ICE는 평형 dQ/dV species parameter가 아니다

승급 조사는 SiO_x의 실리케이트/Li2O 형성, 낮은 ICE,
비정질 Li_xSi 경로와 용량을 유용하게 수집했다. 그러나 ICE와
1차 비가역 Li 소비는 다음에 속한다.

- cycle-0/formation state.
- irreversible inventory loss.
- SEI/비활성 silicate formation.
- 이후 가역 host response와 다른 observation/state layer.

판정:

- SiO_x case의 물리적 핵심으로 `PRESERVE`.
- ICE를 평형 OCV/dQdV 전이의 용량 가중치에 곧바로 넣지 않는다.
- formation/cycle-state model과 reversible host model을 분리한다.

### INTENT-PROV-0132 — Si entropy 문헌은 열 검증축을 열었지만 일반 상수는 주지 않는다

후속 조사는 Si–C entropy coefficient, Si microcalorimetry,
Gr–SiO_x full-cell entropy profiling, MSMR 열 분해,
저온 열거동, lithium-silicide 열용량 문헌을 확보했다.

이들은 서로 다른 양과 시료를 측정한다.

- electrode `dU/dT`.
- total/reversible/parasitic heat.
- full-cell composite entropy signature.
- reaction-wise inferred entropy.
- crystalline compound `C_p/S°`.

판정:

- entropic potential, calorimetry, full-cell 분해를 독립 검증축으로
  쓰는 방향은 `PRESERVE`.
- Si–C의 `−40~−105 μV K⁻¹`를 순수 Si, SiO_x, 모든 cycle/state의
  기본 상수로 승격하는 것은 `REJECT`.
- 재료·조성·SoC·cycle·temperature와 측정법을 보존한 함수/데이터로
  취급한다.

### INTENT-PROV-0133 — 문헌 case 수치는 기본값보다 dataset seed다

R4 문건은 특정 논문의 다음 값을 코드 case parameter로
“직접 사용 가능”하다고 제안했다.

- 특정 Si–C 조성 `60:15:10:15`.
- 평균 delithiation potential `0.4 V`.
- SiO_x capacity `1710 mAh g⁻¹`, ICE.
- blend wt%별 용량·유지율.

판정:

- 논문별 case fixture/validation dataset seed로는 유효하다.
- chemistry-agnostic production default로 승격하지 않는다.
- 최종 코드는 문헌 fixture와 사용자 fit parameter를 분리하고,
  출처 없는 재료 상수를 기본값에 두지 않는다.

## Coverage Status

- 이 batch의 11문건, 1,047행은 `READ`.
- 누적 coverage 반영 후 목표는 158문건, 35,148행이다.
- v1.0.22 잔여 목표는 59문건, 12,534행이다.

## Next

Step 19.6F:
R5 Ch3 저작, RV 교차 검토, SM2 11문건 1,072행을 전문 검독해
조사 결과가 실제 이론·코드 계약으로 어떻게 변환됐는지 확인한다.
