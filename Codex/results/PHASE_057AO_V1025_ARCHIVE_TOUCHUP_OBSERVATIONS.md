# Phase 057AO — v1.0.25·v1.0.25.1 archive·touchup 관찰

정본일: 2026-07-28
세부 Step: 19.8I
범위: 3 unique documents, 288 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25/ARCHIVE_NOTE.md`
- `Claude/docs/v1.0.25.1/ARCHIVE_NOTE.md`
- `Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md`

각 문건을 첫 행부터 마지막 행까지 전량 검독했다. 이 batch는
v1.0.25의 regular-solution 철회, v1.0.25.1 문건 touchup,
검증 시점의 차이를 구분한다.

## Provisional Findings

### INTENT-PROV-0293 — regular-solution 철회는 데이터 provenance 문제를 인정한 정정이다

v1.0.25는 `_REGSOL_XG`, `_regsol_binodal_xa`,
`_regsol_dqdv`와 equilibrium kernel branch를 제거했다.
배경 addendum은 혼합 protocol, 독립 cell 재현성 부족,
`p-ocvhold` 선호를 기록하고 @3 regular-solution 판정을
철회한다.

판정:

- 잘못된 물질 상수나 성공 주장을 고집하지 않은 점은
  `PRESERVE_AS_CORRECTION`.
- v1.0.24의 공개 pOCV fit은 calibration 증거로는 남기되,
  독립 조건 validation이나 상 정체성 확인으로 승격하지 않는다.
- 철회 자체를 모델 완결의 실패로 간주하지 않는다. 오히려
  provenance gate를 새 정본 설계에 포함한다.

### INTENT-PROV-0294 — 채택 모델과 이론 기록의 지위가 분리되어 있지만 경계가 충분히 강하지 않다

생산 코드는 regular-solution 평형 kernel을 삭제하고 logistic
gallery만 남겼다. 반면 문건은 Frumkin/regular-solution 식을
boxed equation과 label로 보존하고, touchup에서 이를
“analytic record”라고 설명한다.

판정:

- 비채택 후보 이론을 리뷰 문건에서 논하는 것은 허용된다.
- 그러나 canonical physical model, 검토 후보, 기각된 closure를
  독자가 즉시 구별할 수 있어야 한다.
- 최종 이론 문건에는 코드 이름을 쓰지 않고 model status를
  물리 용어로 표시한다. 별도 conformance companion에서만
  채택 식과 구현 경로를 1:1 연결한다.

### INTENT-PROV-0295 — v1.0.24의 양성 fitting 증거는 보존하되 검증 범위를 축소해야 한다

v1.0.25 addendum은 v1.0.24에서 보고한 공개 SINTEF pOCV fit의
프로토콜 혼합과 독립-cell 검증 공백을 명시한다.

판정:

- 공개 데이터에 대한 수치 적합 가능성은 `PRESERVE`.
- 물질 상, 고유 파라미터, 다른 cell·온도·전류 조건의 예측성은
  `UNVERIFIED`.
- 이후 평가는 calibration/validation split, cell hierarchy,
  protocol metadata를 필수로 한다.

### INTENT-PROV-0296 — skew `alpha`는 정규화된 형상 자유도지만 아직 물질 물리 파라미터가 아니다

v1.0.25는 `func_dxi_eq`에 opt-in skew `alpha`를 추가했고,
`alpha` 부재 시 1로 두어 기존 경로를 bit-exact 보존한다.
touchup은 peak shift, peak height, area invariance를 유도한다.

판정:

- 수학적 정규화와 opt-in 호환성은 `PRESERVE`.
- 비대칭의 원인을 입자 분포, 상전이 경로, 이질성, kinetic lag
  가운데 어느 것으로 식별하는지는 근거가 없다.
- 출처와 식별성 검증 전에는 `EMPIRICAL_ONLY`이며, kinetics나
  heterogeneity를 대신 흡수하지 않는지 교차검증해야 한다.

### INTENT-PROV-0297 — width scale과 FWHM의 혼동은 v1.0.25.1에서 명시적으로 교정됐다

touchup은 v1.0.24의 “width=`lambda` continuity” 표현을
잘못으로 판정하고, 비대칭 kernel의 FWHM 보정이
`(16/3)(RT/F) lambda^(3/2)`임을 기록한다. 또한 유효 width를
center-height scale로 한정한다.

판정:

- 이 정정과 `lambda^(3/2)` 의존은 `PRESERVE_FOR_REDERIVATION`.
- 최종 정본에서는 scale parameter, local curvature,
  variance, FWHM을 서로 바꿔 쓰지 않는다.
- 차원, limit, 수치 kernel과의 일치를 새로 유도·시험한다.

### INTENT-PROV-0298 — graphite 상 개수는 v1.0.25.1에서도 해결되지 않았다

N4는 Dahn abstract에서 읽은 two-phase count 4와 §7 authority의
2가 충돌한다고 남긴다. 초록만으로 stage/transition/gallery
분류를 확정하지 못했다.

판정:

- gallery 수를 thermodynamic phase 수로 읽지 않는다.
- 원문 전문과 독립 구조·전기화학 문헌을 확인하기 전까지
  물질별 phase count는 `UNVERIFIED`.

### INTENT-PROV-0299 — v1.0.25와 v1.0.25.1의 빌드 검증 시점은 다르다

v1.0.25 archive 시점에는 TeX 도구가 없어 구조 검사만 수행했다.
v1.0.25.1은 이후 XeLaTeX build와 gate를 성공했다고 보고한다.

판정:

- v1.0.25 당시의 “문건 완료”와 v1.0.25.1의 실제 build
  verification을 같은 시점의 증거로 합치지 않는다.
- 최종 이력표에는 작성, 수식 검토, build, physics validation,
  data validation을 별도 열로 둔다.

### INTENT-PROV-0300 — v1.0.25.1은 정직한 touchup이지만 endgame은 아니다

F1은 logistic이 regular-solution보다 “가정이 적다”는 표현을
철회하고, F3는 Frumkin 식을 비채택 analytic record로 낮췄다.
또한 background와 대칭성 조건을 좁혀 썼다. 그러나 N4와
다중-cell 재현성, 데이터 보존·재현 script 항목은 열린 상태다.

판정:

- 자기 교정과 한계 공개는 `PRESERVE`.
- 문건–코드–자유에너지 일관성, 재료별 closure, 독립 데이터
  validation이 닫히지 않았으므로 `NOT_ENDGAME`.

### INTENT-PROV-0301 — SI 상수 opt-in과 `Omega` 역할 분리는 직접 코드 감사가 필요하다

v1.0.25는 `R_SI`, `F_SI`, `use_si_constants()`와 SI gallery
preset을 opt-in으로 추가한다. 동시에 regular-solution
equilibrium은 삭제하면서 `Omega`는 hysteresis, barrier,
phase classification에 남긴다.

판정:

- legacy와 SI 경로의 단위·수치 차이를 Phase 067에서 직접
  대조한다.
- 동일 `Omega`가 equilibrium chemical potential과 끊긴 채
  kinetic/barrier 의미만 갖는지 확인한다.
- 한 기호가 서로 다른 물리량을 겸하면 분리하거나 명시적
  constitutive relation을 요구한다.

## Direction Recovered

이 세 문건에서 확인되는 사용자 방향은 다음과 같다.

1. 그럴듯한 fit보다 provenance와 재현성의 정직한 경계를 우선한다.
2. 이론 후보를 삭제해 숨기지 않되, 채택·비채택 지위를 선명하게
   분리한다.
3. 이론 본문은 물리·화학 논리만 담고, 구현 대응은 별도 companion에
   격리한다.
4. fitting 자유도는 물리적 원인을 가장한 기본값으로 승격하지 않는다.
5. 문건의 모든 채택 식은 생산 구현과 단위·미분·limit까지 일치해야 한다.

## Coverage Status

- 이 batch의 3문건, 288행은 `READ`.
- 누적 coverage 반영 후 목표는 258문건, 51,240행이다.
- 전체 Phase 057 잔여 목표는 13문건, 6,555행이다.

## Next

Step 19.8J:
`V1025_DATA_ADDENDUM.md` 1문건 291행을 전문 검독한다.
