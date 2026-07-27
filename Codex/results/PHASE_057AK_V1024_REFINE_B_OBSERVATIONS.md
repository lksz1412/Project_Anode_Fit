# Phase 057AK — v1.0.24 refine-b 관찰

정본일: 2026-07-28
세부 Step: 19.8E
범위: 3 unique documents, 260 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/comp_R1/refine_b/gr_2L_b_NOTE.md`
- `results/comp_R1/refine_b/lco_omega_b_NOTE.md`
- `results/comp_R1/refine_b/si_fr_b_NOTE.md`

세 정련 노트를 첫 행부터 마지막 행까지 전량 검독했다.

## Provisional Findings

### INTENT-PROV-0259 — refine-b는 잘못된 phase 단정을 제거하고 구조 feature와 상성격을 분리했다

graphite 정련은 “두-상 4 + 고용체 1” 단정을 제거하고,
5-feature를 XRD 구조 해상도의 개수·위치 후보로만 두었다.
전이별 phase character는 별도 §7과 실험 plateau에 맡겼다.
또 기존 네 행의 라벨을 바꾸지 않고 dilute feature 하나를
더하는 `4+1` mapping으로 고쳤다.

판정:

- feature counting과 phase classification의 분리는 `PRESERVE`.
- fitted Ω만으로 최종 분류하는 잔여 문구는 후속에서 제거한다.
- 구조상과 electrochemical peak 사이 mapping은 독립 증거
  행렬로 관리한다.

### INTENT-PROV-0260 — `n_j`와 Ω의 역할을 분리한 것은 필수 교정이다

Si 정련은 기존 모순을 명시적으로 해결했다.

- regular-solution kernel의 ideal limit는 `n_j=1`,
  `w_eq=RT/F`.
- 관측된 넓은 Si 폭은 `n_j>1` gallery multiplicity 또는
  분포폭이 담당한다.
- 인력 `Omega>0`는 중심 감수율을 키워 peak를 좁힌다.
- `Omega<2RT`는 single-phase guard이지 broadening knob가 아니다.

판정:

- 이 역할 분리는 `PRESERVE`.
- “Omega→0이면 arbitrary-width logistic가 bit-exact”라는
  이전 표현은 `SUPERSEDE`; `n_j=1` 조건을 붙인다.
- 코드가 n-scaling과 Ω-kernel을 어떤 순서로 합성하는지는
  R2와 code-history에서 검증한다.

### INTENT-PROV-0261 — 두-상 kernel의 근본 문제는 산문 위임으로 해결되지 않았다

LCO 정련은 ideal width와 phenomenological observed width를
구분하고, two-phase delta의 관측폭을 `w_j` 층에 넘긴다고
설명했다. 이는 기호 충돌을 줄인다.

그러나 boxed homogeneous susceptibility kernel은 그대로
보존했다. `Omega>2RT`에서 Maxwell/common-tangent coexistence를
계산하지 않고 관측폭으로 넘기면, 공존 조성·gap capacity·
single-phase wings가 열역학에서 나오지 않는다.

판정:

- ideal/observed width 분리는 `PRESERVE`.
- two-phase thermodynamics의 현상학 width 위임은
  `EMPIRICAL_ONLY`.
- v1.0.25.2 kernel에서 miscibility-gap measure와 solid-solution
  density가 실제로 구현되는지 대조한다.

### INTENT-PROV-0262 — Ω와 configuration entropy는 별도 슬롯이지만 “차원 직교”는 정확한 표현이 아니다

LCO 정련은 Ω[J/mol]과 `Delta S_config`[J/(mol K)]가 다른
파라미터 슬롯임을 강조했다. 이 bookkeeping 의도는 타당하다.

그러나 free energy에서는 `-T Delta S_config`가 J/mol로 들어가
Ω와 같은 에너지 차원에서 phase stability와 chemical
potential에 함께 기여한다. 서로 중복하면 안 되지만 단순히
단위가 달라 물리적으로 직교한다고 할 수 없다.

판정:

- parameter/source slot의 분리는 `PRESERVE`.
- “차원 직교” 표현은 `CORRECT`.
- 최종 free-energy decomposition에서 두 항의 state dependence,
  temperature dependence, identifiability를 함께 유도한다.

### INTENT-PROV-0263 — `0.2RT` Si seed는 물리 lower bound가 아니라 선택한 초기화다

Si 정련은 `0.2RT≲Omega<2RT`를 attractive-side seed로 두되,
점값이 식별되지 않고 폭은 n_j가 담당한다고 인정한다. 이때
`0.2RT`는 fit cap/floor에서 온 값이지 물리 법칙이 정한
하한이 아니다.

판정:

- `Omega<2RT` single-phase constraint는 후보 물리 경계다.
- `Omega≥0.2RT`는 `EMPIRICAL_INITIALIZATION`.
- 최종 기본값·bound로 승격하지 않으며, Ω의 부호도 데이터와
  문헌에 맡긴다.

### INTENT-PROV-0264 — 단일 대칭종과 비대칭 envelope를 분리한 설명은 보존할 가치가 있다

Si 정련은 대칭 regular solution에서 한 종의
`theta(1-theta)` 응답은 중심 대칭이고, 관측 비대칭은 서로
다른 center/width/capacity를 가진 여러 species의 envelope에서
나온다고 정리했다.

판정:

- 대칭 free-energy 가정 아래 이 결론은 `DERIVED`.
- 실제 a-Si의 path dependence와 stress가 단일종 비대칭을
  만들 가능성까지 배제하지 않는다.
- 최종 모델은 대칭성 가정과 비대칭 관측의 출처를 명시적으로
  시험한다.

### INTENT-PROV-0265 — 산문을 정련해도 boxed 식을 불가침으로 두면 근본 오류가 남을 수 있다

세 refine 작업은 “boxed 식 byte-identical”을 회귀 강점으로
내세웠다. 표기·범위·기본값 모순을 찾는 데는 효과적이었지만,
바로 그 불가침 규칙 때문에 두-상 kernel 같은 수식 자체의
타당성을 재판정하지 않았다.

판정:

- regression-safe prose refinement는 `PRESERVE_AS_EDITING_STAGE`.
- physics audit에서는 기존 boxed 식도 authority가 아니며
  처음부터 재유도·반증 가능해야 한다.
- 최종 workflow는 physics correction 뒤에 regression
  preservation을 적용한다.

## Coverage Status

- 이 batch의 3문건, 260행은 `READ`.
- 누적 coverage 반영 후 목표는 248문건, 50,227행이다.
- 전체 Phase 057 잔여 목표는 23문건, 7,568행이다.

## Next

Step 19.8F:
v1.0.24 R1–R3 결과 3문건 141행을 전문 검독한다.
