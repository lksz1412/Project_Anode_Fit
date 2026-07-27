# Phase 057BG 방향성 결정 계보 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Steps 22.1–22.6  
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 판정

`PASS_P057_DIRECTION_GENEALOGY`

현재 사용자 방향 17개와 전 계보 검독에서 복원한 404개 provisional
finding을 22개 canonical decision으로 통합했다. 각 decision은
주체, 현재 상태, current-direction ID, repository evidence의 path,
physical line range와 commit을 가진다.

## 상태 합계

| 상태 | 결정 수 |
|---|---:|
| `PRESERVE` | 14 |
| `CORRECT` | 5 |
| `EMPIRICAL_ONLY` | 1 |
| `THEORY_ONLY` | 1 |
| `REJECT` | 1 |
| 합계 | 22 |

주체는 current/repository-corroborated `USER_REQUIREMENT` 17개,
재감사에서 구조화한 `REVIEW_FINDING` 5개다.

## 복원된 최종 방향

### 목적과 문건

- v1.0.10–v1.0.25.2 재감사가 새 작업보다 선행한다.
- v1.0.25.2만 기준선이며 v1.0.26은 제외한다.
- 최종 원고는 대학원 교재의 유도 친절성과 review 논문의 문헌 깊이를
  동시에 갖고, 과거 버전사 없이 한 권으로 자립한다.
- theory manuscript에는 물리·화학만 남긴다. 함수명, key, gate,
  code map과 implementation history는 별도 companion으로 보낸다.
- 권위 방향은 theory → implementation contract → code다.

### 물리 구조

- 외부 누적용량, 재료 조성, 내부 전극전위, 관측 cell voltage를 분리한다.
- 전하 보존과 공통 전압 제약을 graphite/Si/blend 조립의 중심에 둔다.
- 공통 보존법칙 위에 graphite, doped LCO, Si/SiOx/Si-C별 자유에너지와
  상태변수를 둔다.
- equilibrium, kinetics/internal variables, transport,
  observation/differentiation을 연결된 계층으로 분리한다.
- 저온·유한전류의 peak lowering, shift, broadening을 하나의
  경험적 폭이나 convolution으로 몰지 않는다.
- barrier의 T·I·U 의존은 free energy, electrode potential,
  overpotential, state와 thermal activation에서 유도한다.
- entropy와 reversible heat는 승인된 free energy의 온도 미분에서만
  파생한다.

### 데이터와 식별

- graphite, Si, blend와 doped high-voltage LCO의 공개 다온도·다율속
  data를 calibration/holdout으로 분리한다.
- fit 성공은 보존하지만 phase, gallery, basis component,
  material constant의 식별로 자동 승격하지 않는다.
- skew-logistic/gallery basis는 현재 `EMPIRICAL_ONLY`다.
- regular-solution free energy는 `THEORY_ONLY` 재유도 후보이며,
  패배한 fit의 Ω로 phase를 확정하지 않는다.
- theory–code conformance, 제한극한, parameter recovery,
  uncertainty, holdout, cross-condition/material transfer를
  다른 gate로 둔다.

### 수치 원칙

- invalid-domain rejection과 명시적 실패는 필요하다.
- 값과 gradient를 몰래 바꾸는 cap, clip, clamp, fixed threshold와
  grid-dependent branch는 유도 없이는 `REJECT`다.
- 실제로 작동한 empirical fitting 자산은 삭제하지 않고
  적용 범위를 낮춰 보존하거나 명시적 heterogeneity/observation
  계층에 연결한다.

## 과거 결정을 그대로 승계하지 않은 지점

1. v1.0.25의 국소 patch 범위는 당시 범위이지 endgame의 한계가 아니다.
2. 과거의 “theory=regsol, fitting=logistic” 병치는 역사적 결정이지만
   현재 100% theory–code closure의 해법은 아니다.
3. stable legacy filename은 당시 release 운영 결정이지 새 architecture의
   과학 구조를 고정하지 않는다.
4. gallery 수를 늘린 curve resolution은 phase 수를 바꾸지 않는다.
5. code와 document가 같은 식을 쓰는 것은 conformance이며,
   그 식의 물리적 타당성은 독립 검증 대상이다.

## 기계 산출물

- generator:
  `Codex/work/v1010_v1025_2_reaudit/generate_phase057_decision_genealogy.py`
- genealogy:
  `Codex/results/PHASE_057_DECISION_GENEALOGY.json`
- decisions: 22
- repository evidence links: 72
- deterministic SHA-256:
  `ba7cb50a643dd8019390b29a04da33b51135c4c85679aca3145c568ad0a6a4a3`

모든 decision은 최소 한 개의 repository evidence를 가지며,
각 evidence는 path, line range, commit을 모두 가진다.

## 다음 단계

Phase 057 Step 23에서 cap/clip/threshold, 근거 없는 default,
평형–동역학–관측 혼동, 보류 물리와 후속 부활을 별도 폐기 계보로
분리한다. `PRESERVE` 결정 안에 과거 구현의 편의항이 섞여 들어오지
않게 하는 단계다.
