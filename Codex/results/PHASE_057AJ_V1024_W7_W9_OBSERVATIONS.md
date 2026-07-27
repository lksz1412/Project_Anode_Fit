# Phase 057AJ — v1.0.24 W7–W9 관찰

정본일: 2026-07-28
세부 Step: 19.8D
범위: 3 unique documents, 303 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/comp_R1/W7/NOTES.md`
- `results/comp_R1/W8/NOTES.md`
- `results/comp_R1/W9/NOTES.md`

세 문건을 첫 행부터 마지막 행까지 전량 검독했다.

## Provisional Findings

### INTENT-PROV-0252 — XRD 공존과 `Omega>2RT`의 연결은 model-conditional이지 보편적 동치가 아니다

W7은 고정 d-spacing 두 상의 공존을 dQ/dV 폭보다 우선하는
좋은 phase evidence로 제시했다. 그러나 이를
`XRD coexistence ⇔ Omega>2RT`로 쓰면 범위가 넓어진다.

`Omega>2RT` 문턱은 대칭 binary regular-solution free energy의
결과다. XRD는 공존상을 관측하지만, scalar fitted Ω를 직접
측정하지 않는다. 다중 sublattice, 탄성, 장거리 상호작용,
비대칭 free energy에서도 공존은 가능하다.

판정:

- XRD phase coexistence를 우선 증거로 쓰는 방향은 `PRESERVE`.
- XRD와 특정 scalar Ω의 보편적 양방향 동치는 `SUPERSEDE`.
- “선택한 regular-solution 축약 안에서의 effective Ω”라고
  명시한다.

### INTENT-PROV-0253 — 다온도 검증을 요구한 산업 방어 논리는 사용자 목표와 맞는다

W7은 stage-2L 추가가 상온 단일곡선 R²를 `-0.44%p`
악화시켰음을 숨기지 않고, 이 feature의 가치는 다온도 분리
서명과 XRD에서 검증해야 한다고 했다. LCO electronic entropy도
상온 curve가 아니라 다온도 `dU/dT`와 reversible heat로
판정하라고 했다.

판정:

- “각 항을 그 항이 예측하는 관측량으로 검증한다”는 원칙은
  `USER_DIRECTION_PRESERVE`.
- 실제 회사/공개 다온도 데이터와 split이 이 NOTES에 포함된
  것은 아니므로 결과 자체는 `VALIDATION_PENDING`.
- 최종 data matrix는 온도·전류·전위·방향을 교차해 peak
  center/height/width/area를 추적한다.

### INTENT-PROV-0254 — electronic-entropy toggle의 T_ref 동일성은 parameter gauge 변환이다

W9는

`Delta H_eff = Delta H - T_ref Delta S_e`

로 재기준해 toggle ON/OFF가 `T_ref`에서 같은 중심전위를
내도록 했다. 이는 기준온도 곡선을 보존하는 올바른 algebraic
reparameterization이다.

하지만 동일한 기준 곡선을 만드는 두 parameterization은
`Delta H`와 `Delta S_e`가 단일 온도에서 식별되지 않음을
보여 준다. 물리적 electronic entropy가 검증됐다는 뜻은 아니다.

판정:

- T_ref invariance와 재기준식은 `PRESERVE`.
- 단일온도 curve의 electronic-entropy 증거는 `REJECT`.
- 다온도 OCV/entropy/reversible-heat 자료로 gauge를 깨야 한다.

### INTENT-PROV-0255 — regular-solution 곡률 계수의 정규화가 창 사이에서 흔들린다

대부분의 초안은 대칭점 판정자를

`4RT - 2 Omega`

로 썼다. W8의 LCO 요약은

`g''(1/2)=2RT-Omega`

로 적었다. 후자가 단순히 전자의 1/2 정규화라면 문턱은 같지만,
free energy의 몰 기준·site 기준·전이좌표 정규화가 명시되지
않으면 Ω 숫자와 물리 단위의 비교가 모호해진다.

판정:

- 임계비 `Omega/(2RT)`의 형식은 후보로 보존한다.
- 재료와 식 사이 Ω의 절대값을 옮기기 전에 free-energy
  normalization과 capacity coordinate를 고정한다.
- 최종 symbol table에 basis와 units를 필수 필드로 둔다.

### INTENT-PROV-0256 — W9의 honest-limit 중심 base 선정은 적절했지만 seed 권위를 벗어나지는 못했다

W9는 세 후보 중 다음을 가장 명확히 남겼다.

- stage-2L에서는 entropy 차만 견고하고 절대 배정은 미식별.
- Si Ω는 점값이 아니라 single-phase 범위만 지지됨.
- LCO electronic term은 다온도 자료 없이 미검증.
- LCO microscopic feature label은 확정되지 않음.

이는 base로 선택할 합리적 이유다. 다만 W9도 seed의 XRD
분류와 내부 Ω vector를 “확정”으로 받아들였으므로 독립 물리
검증은 아니다.

판정:

- honest limits와 scope language는 `PRESERVE`.
- seed-derived 확정 등급은 최종 문헌·데이터 감사에서 다시
  판정한다.

### INTENT-PROV-0257 — 고전압 도핑 LCO라는 사용자 목표는 이 저작 경쟁의 범위에 없다

W7–W9의 LCO 논의는 T1/T2/T3, scalar per-peak Ω,
electronic entropy toggle에 집중한다. dopant species,
concentration, defect chemistry, oxygen stability, high-voltage
phase degradation, cutoff dependence를 모델 변수나 근거
행렬로 다루지 않는다.

판정:

- v1.0.24 LCO 소절은 일반 LCO peak surrogate 자산이다.
- 사용자가 요구한 doped high-voltage LCO 모델은
  `NOT_COVERED`.
- 최종 literature/data phase에서 별도 cathode workstream으로
  구축한다.

### INTENT-PROV-0258 — 코드·fit 수치를 이론 문건의 권위로 쓰지 않는 최신 경계를 적용한다

W7은 회사 피팅 파라미터의 산업 방어력을 목표로 삼았고,
W8/W9는 코드 toggle, kernel branch, 내부 R²를 본문 후보
서술에 포함했다. 당시 규칙에는 부합했지만 최신 사용자 지시는
이론 문건에서 코드 내용을 배제한다.

판정:

- 물리 항의 실험적 판별법은 이론 문건에 남긴다.
- 코드 플래그, bit-exact, 파일명, 내부 R² provenance는
  implementation/data companion으로 이동한다.
- 문건의 상세성은 코드 설명이 아니라 물리 유도와 재료별
  evidence depth로 채운다.

## Coverage Status

- 이 batch의 3문건, 303행은 `READ`.
- 누적 coverage 반영 후 목표는 245문건, 49,967행이다.
- 전체 Phase 057 잔여 목표는 26문건, 7,828행이다.

## Next

Step 19.8E:
graphite/LCO/Si refine-b 3문건 260행을 전문 검독한다.
