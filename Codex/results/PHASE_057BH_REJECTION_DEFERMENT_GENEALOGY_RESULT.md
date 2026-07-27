# Phase 057BH 금지·철회·보류 계보 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Steps 23.1–23.5  
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 판정

`PASS_P057_REJECTION_DEFERMENT_GENEALOGY`

방향성 결정 22개와 별도로, 과거 구현의 편의항·혼동·데이터 없는 default,
철회된 default 및 아직 수행되지 않은 필수 물리를 20개 계보 항목으로
분리했다. “폐기”는 모두 삭제한다는 뜻이 아니다. `REJECT`,
`CORRECT`, `EMPIRICAL_ONLY`, `THEORY_ONLY`, `DEFERRED_REQUIRED`,
`WITHDRAWN`의 역할을 구분한다.

## 즉시 승계하지 않는 항목

### 물리로 위장될 수 있는 수치 편의

- hard cap, clip, clamp, fixed truncation
- grid spacing에 따라 equilibrium으로 조용히 돌아가는 branch
- 측정 모델 없이 instrument/kinetic response로 불린 smoothing
- C-rate 3,600배 단위 오류로 형성된 old barrier gauge

invalid input rejection과 NaN 방지는 필요하지만, 값을 몰래 바꾸는
수치 장치를 물리로 승격하지 않는다.

### 좌표·회계 혼동

- Si wt%, capacity fraction, blend capacity denominator 혼용
- equilibrium에서 삭제된 Ω와 barrier/hysteresis/phase 서술의 Ω 단절
- equilibrium, hysteresis, polarization, transport, observation을
  하나의 width 또는 lag에 압축
- pOCV, pOCV-hold, 서로 다른 specimen과 미확정 protocol의 혼용

### 경험식을 물리 상수로 승격한 사례

- skew α를 susceptibility·entropy·reversible heat에 직접 사용
- gallery/basis component를 phase로 판정
- 패배한 regsol fit Ω를 흑연 상 증거로 이전
- literature case 또는 fit seed를 재료 default로 승격
- in-sample R²/BIC를 mechanism validation으로 사용

## 보존하되 지위를 낮춘 자산

- skew-logistic/gallery basis:
  `EMPIRICAL_ONLY`
- voltage-domain transfer/smoothing:
  `EMPIRICAL_ONLY`
- regular-solution free energy:
  `THEORY_ONLY_PENDING_INDEPENDENT_PHASE_EVIDENCE`
- 비상수 background 관찰:
  `UNVERIFIED`
- 기존 legacy 회귀:
  별도 `LEGACY_GATE`로 보존

따라서 실제 fitting 성능을 없애지 않는다. 대신 thermodynamic state와
동일시하지 않고, 후속 heterogeneity/observation 계층에 연결될 수 있는
후보 자산으로 보존한다.

## 철회와 부활

- 7-gallery skew default는 `77ae0d9`에서 도입되고 `7b342dd`에서
  철회됐다. 현재는 empirical opt-in만 유효하다.
- 이론 본문 코드 금지 원칙은 반복적으로 선언됐지만 code map, function,
  gate가 후속 문건에서 다시 들어왔다. 최종 원고에서는 companion으로 이동한다.
- bit-exact legacy 보호가 SI default와 새 default 검증을 막은 사례가
  반복됐다. 앞으로 legacy regression과 physics acceptance를 분리한다.
- “완결” 선언 뒤에도 C-rate 단위, blend normalization, alpha
  thermodynamics, default temperature dependence 결함이 다시 발견됐다.
  완료 표현은 Phase별 명시 범위로만 유효하다.

## 보류가 아니라 필수인 후속 물리

다음은 “나중에 해도 되는 장식”이 아니라 사용자 목표를 닫기 위한
`DEFERRED_REQUIRED`다.

1. doped high-voltage LCO의 defect chemistry, oxygen stability,
   phase degradation와 cutoff dependence
2. Si chemo-mechanics, stress-coupled chemical potential,
   hysteresis, SiOx/Si-C host effect
3. graphite/Si/blend/LCO의 multi-temperature, multi-rate,
   rest/equilibrium, independent-cell public data
4. equilibrium–kinetics–transport–observation 계층 분리
5. protocol/cell/preprocessing provenance와 holdout validation

## 기계 기록

`Codex/results/PHASE_057_REJECTION_DEFERMENT_GENEALOGY.json`에
20개 항목과 118개의 provisional finding 참조(96개 고유 ID)를 저장했다.
각 항목은 category, item, evidence claim ID와 현재 disposition을 가진다.

## 다음 단계

Phase 057 Step 24에서 22개 보존·교정 결정과 20개 금지·철회·보류
항목의 충돌을 시간순으로 해소한다. 그 결과를 현재 사용자 방향 헌법으로
작성하되, 아직 새 이론의 식·목차·코드 구조를 확정하지 않는다.
