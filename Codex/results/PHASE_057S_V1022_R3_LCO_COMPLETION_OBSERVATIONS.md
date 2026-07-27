# Phase 057S — v1.0.22 R3 LCO completion 관찰

정본일: 2026-07-28
세부 Step: 19.6D
범위: 11 unique documents, 595 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 R3 계획·경쟁 초안·마스터 채택 기록을 첫 행부터 끝 행까지
검독했다.

- `PLAN_R3_ch2_completion.md`
- `comp_R3/BRIEF_D.md`
- `comp_R3/BRIEF_E.md`
- `comp_R3/D_seams/ADDTERM_CHECK.md`
- `comp_R3/D_seams/INTRO_NOTATION_FINAL.md`
- `comp_R3/D_seams/SEAM_PLAN_R3.md`
- `comp_R3/CHERRYPICK_R3.md`
- `comp_R3/E_bridges/BRIDGE_DRAFTS_LCO.md`
- `comp_R3/E_bridges/BRIDGE_TARGETS_LCO.md`
- `comp_R3/E_bridges/L2_TIER_CANDIDATES.md`
- `comp_R3/E_bridges/L5_CHARGEORDER_CHECK.md`

## Provisional Findings

### INTENT-PROV-0118 — R3의 LCO 설계는 “흑연 골격 + 추가 텀”이다

R3는 신 Ch2 LCO의 저작 원리를 명시적으로 다음과 같이 고정했다.

- Ch1의 전하 보존, 평형종, 히스테리시스, 폭, peak, 합산 골격을
  외부참조로 그대로 받음.
- LCO에는 방향 규약 재배선, 질서–무질서/MIT 2상역,
  configurational/vibrational/electronic entropy 분해를 추가.
- peak 식 자체는 새 항 없이 전이 집합과 파라미터만 교체.
- MSMR과 기존 logistic을 함수형 동형으로 연결.

판정:

- 재료 공통 관측·보존 골격을 재사용하는 원칙은 `PRESERVE`.
- 그러나 고전압 도핑 LCO가 graphite의 골격에 몇 항만 더한
  특수형이라는 가정은 `UNVERIFIED`.
- 산소 redox/산소 손실, Co 산화상태·전자구조, 층상구조 전이,
  표면 재구성, 입계·균열·계면, dopant site/charge compensation과
  전해액 산화까지 필요한지 최종 문헌·데이터 gate에서 다시 판정한다.

### INTENT-PROV-0119 — LCO 전자·질서 모델은 미시이론을 현상론적 gate로 축약했다

문헌 다리의 자체 설명에 따르면:

- Marianetti의 impurity-Mott/DFT 결과를
  중심 `x_MIT`와 폭 `Δx_MIT`의 logistic gate로 축약.
- Van der Ven의 다체 cluster expansion과 질서 바닥상태를
  전이별 단일 평균장 `Ω_j^cat` 정규용액으로 축약.
- 원 Hamiltonian, 정확한 판별식, ECI와 식 번호는 확인하지 못함.
- `eq:lco-mottcrit`은 Marianetti의 정량식이 아니라
  교과서적 Mott 판별식이라고 스스로 경고.

판정:

- 미시적 유일 해석이 아닌 저차원 effective model로만
  `THEORY_ONLY/EMPIRICAL_ONLY`.
- gate 중심·폭·`Ω`을 물질 상수나 dopant 메커니즘으로
  과해석하지 않는다.
- 최종 이론에는 미시 변수에서 축약식으로 내려오는 coarse-graining
  전제와 식별가능성 한계를 명시해야 한다.

### INTENT-PROV-0120 — MSMR “검증완료”도 primary-source 식 검증은 아니다

R3는 MSMR 점유식의 형태와 파라미터 정의를 PyBaMM 구현 문서와
대조해 “형태 검증완료”로 분류했다. 동시에 원 논문 내부 식 번호는
직접 대조하지 못했다고 적었다.

판정:

- 구현 문서와의 형태 대조는 독립 implementation cross-check로
  유용하므로 `PRESERVE`.
- 이를 Verbrugge/Baker–Verbrugge 원전 수식의 직접 검증으로
  간주하는 것은 `REJECT`.
- 최종 review ledger에서는 primary paper, review/implementation,
  현재 문건 식을 서로 다른 evidence tier로 분리한다.

### INTENT-PROV-0121 — LCO 문헌 다리 4개도 핵심 식·수치 검증이 남았다

R3가 채택한 4개 다리의 실제 상태는 다음과 같다.

- Marianetti 2004:
  기작·조성 경계만 확인, 원 모델 Hamiltonian 미확인.
- Van der Ven 1998:
  방법·`x=1/2` 질서 결과만 확인, ECI 식·값 미확인.
- MSMR 계보:
  PyBaMM로 형태 확인, 원전 직접 대조 미완.
- Reynier 2004:
  측정 원리·3기여 분해는 초록 수준 확인,
  본문 `0.18 k_B/atom` 값은 미확인.

판정:

- R3의 4개 다리 채택은 교육적 연결 채택이지 문헌 검증 종료가 아니다.
- load-bearing 식과 수치는 원문 본문·표·보충자료까지 다시 확인한다.

### INTENT-PROV-0122 — 0.47/1.49 J mol⁻¹ K⁻¹ charge-order 값은 권위 상실 상태다

`L5_CHARGEORDER_CHECK.md`는 T2/T3 config 슬롯에 쓰인
`0.47/1.49 J mol⁻¹ K⁻¹ @ x=1/2, 2/3`에 대해 다음을 기록한다.

- Motohashi 2009는 자화율과 NMR/NQR 기반 자기·전자 상도표 논문.
- 해당 값이 논문에 실제 존재하는지 직접 확인하지 못함.
- configurational charge-order entropy가 아니라 magnetic/spin
  entropy일 가능성이 있어 물리 범주 오류 가능.
- 검증된 Reynier 초록의 질서 조성은 `x=1/2, 5/6`로,
  기존 `x=2/3` 배정과도 불일치.
- 당시 보고 자체가 값의 tier A 주장 강등을 검토하라고 권고.

판정:

- 두 값과 Motohashi 귀속은 `UNVERIFIED`.
- primary source에서 양의 종류·정의·조성·정규화 basis를
  확인하기 전 기본값, 검산값, dopant 해석에 사용하지 않는다.
- 확인 실패 시 삭제 또는 명시적 empirical placeholder로 격리한다.

### INTENT-PROV-0123 — L2 후보는 방향만 유효하고 정량 승급은 미완료다

R3는 Reynier 2004, Ménétrier 1999, EES entropymetry 2020을
LCO 실측 후보로 올렸다. 그러나:

- 일부는 abstract/landing/search snippet만 확인.
- EES 2020의 정량 `ΔS`는 확보하지 못함.
- 표 갱신과 원장 등재는 R4로 이월.
- Ni doping이 order를 완화한다는 정성 결과는 있었지만
  dopant-specific 방정식이나 매개변수 지도는 없음.

판정:

- 실측 OCV/entropic coefficient/order signature로 LCO 모델을
  검증하려는 방향은 `PRESERVE`.
- tier-A 정량값·도핑 메커니즘 확보 완료로 읽는 것은 `REJECT`.
- 최종 조사에서 pristine과 doped high-voltage LCO를 분리하고,
  dopant 종류·농도·site·전압창·열처리·cycling 상태를 함께 기록한다.

### INTENT-PROV-0124 — R3 PASS는 편집 복구와 build 성공까지다

R3 집행에서는 실제로 다음 사고가 있었다.

- 6열 전환표를 5열로 오파싱해 4곳이 일시 축약된 뒤 복구.
- `\textbf` 인자 내부에 다리를 삽입해 LaTeX 명령을 절단한 뒤 복구.

마스터는 이를 같은 턴에 검출하고 재빌드·재스윕으로 복구했다.

판정:

- 작업 이력을 숨기지 않고 복구를 기록한 점은 `PRESERVE`.
- 최종 자동화는 table schema 검증과 syntax-aware 삽입을 요구한다.
- 복구 후 build PASS도 물리·실험 검증을 뜻하지 않는다.

## Coverage Status

- 이 batch의 11문건, 595행은 `READ`.
- 누적 coverage 반영 후 목표는 147문건, 34,101행이다.
- v1.0.22 잔여 목표는 70문건, 13,581행이다.

## Next

Step 19.6E:
R4 Si/SiO_x/Si–C/blend/LCO 조사·승급 11문건 1,047행을
전문 검독해 실제 데이터·재료별 근거와 placeholder 경계를 확인한다.
