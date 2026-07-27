# Phase 057U — v1.0.22 R5·RV·SM2 관찰

정본일: 2026-07-28
세부 Step: 19.6F
범위: 11 unique documents, 1,072 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 R5 Ch3 저작, 장별·교차 검토, 통계역학 보강 후보 문건을
첫 행부터 끝 행까지 검독했다.

- `plans/PLAN_R5_ch3_authoring.md`
- `results/comp_R5/BRIEF_R5.md`
- `results/comp_R5/W1/DESIGN_NOTE.md`
- `results/comp_R5/W2/DESIGN_NOTE.md`
- `results/comp_R5/W3/DESIGN_NOTE.md`
- `results/comp_R5/CHERRYPICK_R5.md`
- `results/comp_RV/RV1_CH1_REPORT.md`
- `results/comp_RV/RV2_CH2_REPORT.md`
- `results/comp_RV/RV3_CROSS_REPORT.md`
- `results/comp_SM2/SM2_SURVEY.md`
- `results/comp_SM2/SM2_REMOVAL.md`

## Provisional Findings

### INTENT-PROV-0134 — R5는 Si·blend의 첫 실질 이론화지만 완결본은 아니다

R5는 Ch3를 5쪽에서 16쪽으로 늘리며 다음을 실제 본문 골격으로
채택했다.

- graphite와 Si host의 전하·Li 보존 합.
- `f_Si -> 0`에서 graphite-only 식으로 돌아가는 극한.
- host별 `dQ/dV`의 합산.
- Larché–Cahn 계열 응력 화학퍼텐셜 이동.
- 후속 구현 계약.

이는 단순 문헌 목록보다 진전된 첫 실질 Ch3 이론화다. 다만
host별 동역학, 응력 이력, SiO_x formation, irreversible inventory,
실험 식별성이 닫히지 않았다.

판정:

- 보존식과 host 분해 골격은 `PRESERVE`.
- R5 자체를 Si·blend의 완결 이론으로 보는 것은 `REJECT`.
- 최종 문건에서는 평형, 동역학, 역학, formation/cycle-state를
  서로 다른 closure로 명시한다.

### INTENT-PROV-0135 — 공통 전위는 동일한 host 전류를 뜻하지 않는다

R5는 공통 화학퍼텐셜 아래 두 host의 반응이 완전 동시적이고
가산적이어야 한다는 식으로 논리를 밀고, SoC별 우세 host 전류의
전환을 그 가정과 충돌하는 현상처럼 다룬다.

그러나 공통 terminal potential 아래에서도 각 host는 서로 다른
OCV, exchange current, overpotential, diffusion length, active area,
state와 history를 가질 수 있다. 따라서 host 전류는 달라지고
SoC·온도·전류에 따라 우세 host가 바뀔 수 있다.

판정:

- 공통 전위와 전체 전류·Li 보존은 `PRESERVE`.
- 공통 전위에서 host별 전류가 같거나 항상 유의미하다는 해석은
  `REJECT`.
- 최종 코드에서는 공통 terminal constraint와 host-specific
  current allocation을 분리해 푼다.

### INTENT-PROV-0136 — R5의 `f_Si` 범위는 질량분율과 용량분율을 혼용한다

R5는 `f_Si=Q_Si/Q`를 capacity fraction으로 정의하면서 R4에서
찾은 `0–30 wt%` 실험 범위를 같은 `0–0.3` 축처럼 사용한다.
Si와 graphite의 specific capacity, ICE, utilization이 다르므로
두 분율은 수치적으로 같지 않다.

판정:

- 제조 입력 mass fraction과 모델 내부 reversible capacity fraction을
  별도 변수로 둔다.
- 변환에는 material-specific capacity, active fraction, ICE,
  cycle/state-dependent utilization을 명시한다.
- `wt% = f_Si` 대입은 `REJECT`.

### INTENT-PROV-0137 — Larché–Cahn 이동은 유용하지만 Si 히스테리시스를 닫지 않는다

R5의 `mu = mu_chem + partial_molar_volume * sigma_h` 계열 결합은
응력에 의한 가역 전위 이동의 보존할 출발점이다. 그러나
응력의 부호 convention과 hydrostatic definition은 다시 유도해야
하며, 무엇보다 `sigma_h(state, history)`를 주는 탄소성 구성식이 없다.

고정된 응력 offset은 전위를 옮길 뿐 경로 의존 히스테리시스를
만들지 못한다. 히스테리시스에는 적어도 팽창–수축, yield,
plastic flow, morphology/constraint 및 history state가 필요하다.

판정:

- 화학–역학 coupling은 `PRESERVE`.
- 상수 응력 이동을 Si 히스테리시스 완결식으로 읽는 것은 `REJECT`.
- 부호·단위·경로 의존성을 독립 유도하고 실험으로 식별한다.

### INTENT-PROV-0138 — “scope 밖” 선언은 예측 closure의 공백을 없애지 않는다

R5는 소성 응력 구성식을 범위 밖으로 선언한 뒤 “논리 공백 0”으로
평가한다. 문서 범위를 정하는 것과 대상 실험을 예측할 물리식이
닫히는 것은 다르다.

판정:

- 범위 선언은 문서 관리상 유효하다.
- 그 선언으로 Si의 voltage hysteresis와 `dQ/dV` 조건 의존성이
  설명 완료됐다고 보는 것은 `REJECT`.
- 최종 완결성 원장은 각 현상별로 `closed`, `empirical closure`,
  `unresolved`를 분리한다.

### INTENT-PROV-0139 — R5의 코드 사양은 사용자가 원하는 이론 문건 경계를 넘는다

R5 계획과 §3.5는 실제 class 이름, 구현 분기, bit-exact 회귀,
`GraphiteAnodeDischargeDQDV`와 `_LIT` 같은 식별자를 이론 장에
직접 넣는다.

사용자가 요구한 정본 원칙은 다음과 같다.

- 이론 문건에는 물리·화학 논리만 둔다.
- 코드 언급은 지정된 제한 구역에서만 허용한다.
- 코드는 별도 추적 문건을 통해 이론을 100% 반영한다.

판정:

- 물리식과 구현의 추적 가능성 자체는 `PRESERVE`.
- 생산 class 이름과 bit-exact 계약을 물리 장 본문에 두는 것은
  `CORRECT`.
- 최종 구조는 physics manuscript, implementation concordance,
  verification ledger를 분리한다.

### INTENT-PROV-0140 — RV의 `H=0`·PASS는 자체 지적과 양립하지 않는다

RV1–RV3은 여러 실제 결함을 찾으면서도 높은 수준의 PASS 또는
`H=0`으로 닫았다.

- Dreyer의 common-mu framework와 문건이 추가한 eta 분포의
  귀속 경계가 불명확하다.
- McKinnon의 `x`와 문건의 `xi=1-x` 사이 부호 mapping이
  “역할 대응”이라는 말로 가려졌다.
- charge-order 수치와 entropy scale의 정량 원전 검증이 남았다.
- MIT logistic gate의 endpoint tail이 0이 아니다.
- Ch1이 뒤 장에만 정의된 tier legend에 의존한다.
- Part/Chapter 명명, `u_j` 기호 scope, appendix letter가 취약하다.
- RV3 수행 중 Ch3가 편집 중이어서 안정된 Ch3 교차감사를 하지 못했다.

판정:

- RV 보고서는 결함 후보 원장으로 `PRESERVE`.
- 그 보고서의 총괄 PASS를 과학적 검증 완료로 승격하는 것은 `REJECT`.
- 각 지적은 후속 채택본과 원전·수식·실험 gate에서 재판정한다.

### INTENT-PROV-0141 — SM2의 세 bridge는 유망하지만 독립 재유도가 필요하다

SM2는 다음 세 교육적 bridge를 제안했다.

- ideal independent-site width와 점유수 fluctuation/susceptibility.
- finite ensemble에서 상대 fluctuation의 크기 감소.
- 전압 응답 `dQ/dV`와 온도 응답 reversible heat를 하나의
  free-energy surface에서 해석.

이 방향은 대학원 교재형 설명에 매우 유용하다. 그러나 현재 제안식은
입자/몰 정의, `N_A`·`F` 계수, 전압·화학퍼텐셜 부호, 미분할 때
고정하는 변수, implicit composition dependence를 다시 확인해야 한다.
특히 equilibrium fluctuation 관계를 finite-current broadening의
직접 원인으로 확장하면 안 된다.

판정:

- 세 bridge의 설명 목적은 `PRESERVE`.
- 현재 제안식을 검산 없이 정본에 삽입하는 것은 `UNVERIFIED`.
- partition function부터 단위·부호를 재유도하고, 평형 width와
  비평형 broadening을 명시적으로 분리한다.

### INTENT-PROV-0142 — 장 구조가 뒤쪽 정의를 앞 장이 빌리는 순환 의존을 만들었다

RV3은 Ch1이 self-contained를 표방하면서 tier A/B/C 정의를
Ch2에서만 제공하고, 역사적 “Part II”와 현재 Ch2 명칭이 충돌하며,
Part T의 “본 장/본 파트”와 `u_j` guard가 실제 scope를 명확히 하지
못함을 확인했다.

판정:

- 전체 공통 convention과 evidence tier는 front matter에서 정의한다.
- 각 장의 로컬 기호는 section-local scope와 완전한 정의를 둔다.
- 하드코딩한 appendix letter와 역사적 Part 명칭은 제거한다.

### INTENT-PROV-0143 — R5의 서지 정정은 DOI 존재와 물리 검증의 차이를 보여준다

R5 cherry-pick은 R4의 Arnot article number를 `110536`에서
`110509`로 고쳤다. 이는 Crossref 검색과 문헌 수 집계가 있어도
개별 metadata와 정량 주장에 오류가 남을 수 있음을 직접 보여준다.

판정:

- 문헌 존재, metadata, 원문 방법, 수식, 수치, 현재 모델과의
  mapping을 별도 필드로 검증한다.
- “19개 key 확보” 같은 수량 집계를 물리 수치 검증으로 읽지 않는다.
- 논문별 case 값은 validation fixture 후보이며 production default가
  아니다.

## Coverage Status

- 이 batch의 11문건, 1,072행은 `READ`.
- 누적 coverage 반영 후 목표는 169문건, 36,220행이다.
- v1.0.22 잔여 목표는 48문건, 11,462행이다.

## Next

Step 19.6G:
FR A01–A08 및 A20 심층 review 10문건 3,579행을 전문 검독해
각 review의 물리·수학 검산 깊이와 후속 채택 여부를 판정한다.
