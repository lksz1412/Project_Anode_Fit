# Phase 057V — v1.0.22 FR A01–A08·A20 심층검토 관찰

정본일: 2026-07-28
세부 Step: 19.6G
범위: 10 unique documents, 3,579 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 FR 공통 brief와 A01–A08·A20 심층 검토 보고서를 첫 행부터
끝 행까지 검독했다. 400행을 넘는 보고서는 연속 구간으로 나누어
읽었으며, 출력이 잘린 A03은 더 작은 구간으로 다시 전량 확인했다.

- `results/comp_FR/BRIEF_FR_A.md`
- `results/comp_FR/A01_REVIEW.md`
- `results/comp_FR/A02_REVIEW.md`
- `results/comp_FR/A03_REVIEW.md`
- `results/comp_FR/A04_REVIEW.md`
- `results/comp_FR/A05_REVIEW.md`
- `results/comp_FR/A06_REVIEW.md`
- `results/comp_FR/A07_REVIEW.md`
- `results/comp_FR/A08_REVIEW.md`
- `results/comp_FR/A20_REVIEW.md`

## Provisional Findings

### INTENT-PROV-0144 — FR은 실제 재계산을 수행했지만 전부 “보고 전용 제안”이다

FR 공통 brief는 각 절의 전문 정독, 수식 재유도, 그림 좌표 재계산,
교차참조 대조, H/M/L 분류를 요구했다. A01–A08·A20은 이를 상당히
충실히 수행했다. 특히 다음은 단순 문체 검수가 아니다.

- 상수항·부호·극한의 독립 재유도.
- logistic 높이·FWHM·면적과 그림 좌표 수치 검산.
- TST 고온극한의 모드 수 대조.
- 평균장 응답과 독립자리 분산의 조건 분리.
- 문건 식과 당시 코드 경로 대조.

그러나 모든 창은 소스 무수정의 `report-only`였고 제시한 LaTeX는
후보일 뿐이다.

판정:

- 결함 후보와 재계산 로그는 `PRESERVE`.
- “FR에서 제안했다 = 마스터에 반영됐다”는 해석은 `REJECT`.
- 후속 batch에서 각 제안의 실제 채택·수정·철회 여부를 별도 추적한다.

### INTENT-PROV-0145 — 다클래스 독립자리 식과 `Omega` 자기무모순 평균장이 충돌한다

A03은 Part 0의 산문이 class 내부 `Omega_j`를 자기무모순 평균장으로
넣는다고 말하면서, 전시된 `Xi`, 점유율, 분산 식은
composition-independent site energy를 쓴 독립자리 식임을 찾았다.

두 모델은 같은 식이 아니다.

- 독립자리: explicit logistic, 응답 `beta theta(1-theta)`.
- 평균장 상호작용: `theta`가 자기 지수에 되먹임되는 implicit
  isotherm.
- `0 < Omega < 2RT`에서도 응답에는
  interaction denominator가 생긴다.
- `Omega > 2RT`에서는 비단조성과 상공존 처리가 필요하다.

판정:

- 이 충돌은 v1.0.22의 핵심 미해결 결함으로 `CORRECT`.
- 최종 문건은 ideal independent-site, single-phase regular solution,
  two-phase coexistence를 서로 다른 해로 분리한다.
- 최종 코드는 선택한 물리 층과 같은 Jacobian·susceptibility를
  계산해야 하며, 산문은 평균장인데 코드는 explicit logistic인
  혼합을 허용하지 않는다.

### INTENT-PROV-0146 — TST 활성화 엔트로피의 고온극한 검산은 성립하지 않는다

A06은 표준 Eyring mode counting에서 transition state가 reaction
coordinate 한 모드를 잃으므로, 고온에서
`q^ddagger/q_R` 자체는 일반적으로 `1/T`로 간다는 점을 재유도했다.
유한한 고전 시도빈도로 가는 것은 그 비에 `k_BT/h`를 곱한
prefactor다.

또한 다음 두 정의가 섞였다.

- `Delta S_a = R ln(q^ddagger/q_R)`라는 식별.
- `-partial Delta G_a/partial T`라는 열역학 미분 정의.

분배함수 비가 온도 의존하면 둘 사이에 미분항이 추가된다.

판정:

- 현 TST verifybox는 `CORRECT`.
- 활성화 엔탈피·엔트로피의 표준상태, 모드, 온도 의존을
  partition function부터 다시 유도한다.
- 상수 `Delta H_a`, `Delta S_a`는 제한된 온도창의 effective fit인지
  미시 계산값인지 구분한다.

### INTENT-PROV-0147 — 요동–응답 항등과 logistic 종을 같은 조건으로 묶으면 안 된다

A07은 평형 감수율 항등의 정확 조건을 `n_j=1`로 둔 것이 잘못임을
찾았다.

- `var(N)=k_BT partial<N>/partial mu`는 평형 대정준 응답 관계다.
- `var(N)=sum M_j theta_j(1-theta_j)`는 독립자리 분해다.
- 폭 `RT/F`의 logistic 종은 ideal independent-site
  (`Omega=0`) 특수형이다.
- `n_j`는 선택된 peak scale의 재모수화이지 상호작용 부재 조건이
  아니다.

문건 기본값 자체가 `n_j=1`과 `Omega_j>2RT`를 동시에 두므로
기존 가드는 자기 반례를 갖는다.

판정:

- 일반 fluctuation–response identity는 `PRESERVE`.
- 이를 임의의 현상학 logistic peak와 동일시하는 것은 `REJECT`.
- equilibrium susceptibility, observation convolution,
  empirical line shape를 서로 다른 식과 검증 gate로 둔다.

### INTENT-PROV-0148 — spinodal gap은 평형 히스테리시스가 아니다

A05는 regular-solution spinodal 식과 gap 대수를 정밀하게
재검산했지만, 문건의 더 큰 개념 혼합은 남았다.

- 엄밀한 평형 전환은 Maxwell/binodal 조건에서 가역 plateau를 준다.
- spinodal은 균일 준안정 가지가 더 버틸 수 없는 한계다.
- 실제 zero-current 또는 ultra-low-rate hysteresis는 nucleation,
  elastic coherency, defects, finite size, path history와 관측시간에
  의해 Maxwell과 spinodal 사이 어디에서 전환하는지 결정된다.
- `gamma_j`와 `h_eta,j`로 spinodal gap을 축소하는 식은 이 전환을
  기술하는 phenomenological closure이며 equilibrium state function이
  아니다.

판정:

- regular-solution free energy와 spinodal 계산은 `PRESERVE`.
- 이를 “열역학적 평형 히스테리시스”로 부르는 것은 `CORRECT`.
- 최종 구조는 reversible equilibrium, metastable branch,
  nucleation/kinetic switching, partial-cycle memory를 분리한다.

### INTENT-PROV-0149 — broadening 예산은 내부 모순을 찾았지만 “평형 잔여 폭”도 재검증해야 한다

A08은 keybox가 세 출처를 자유폭 `w_j` 하나에 흡수한다고 쓰면서
본문은 비대칭 current tail을 `L_V,j`로 따로 두고 중복계산을
금지한 자기모순을 찾았다.

보존할 구분은 다음과 같다.

- symmetric equilibrium/heterogeneity response.
- asymmetric finite-rate memory tail.
- mean shift와 variance.
- particle-count weighting과 capacity weighting.

다만 A08이 유지한 “plateau delta + binodal single-phase tails를
한 봉우리로 읽으면 `RT/F` 평형 잔여 폭”이라는 설명도 아직
정본으로 승인할 수 없다. 거시 평형 two-phase capacity는 Maxwell
전위의 singular contribution이고, 양끝 solid-solution response와
실험 resolution/heterogeneity를 어떤 관측 커널로 묶는지에 따라
겉보기 폭이 달라진다.

판정:

- `w_j`와 `L_V,j`의 중복 금지는 `PRESERVE`.
- two-phase peak에 보편적인 intrinsic `RT/F` 폭을 부여하는 것은
  `UNVERIFIED`.
- 최종 observation model에서 delta/finite-size/heterogeneity/
  instrument/differentiation kernel을 명시적으로 합성한다.

### INTENT-PROV-0150 — 전위·화학퍼텐셜·분극 회계 경계가 아직 닫히지 않았다

A01, A03, A04, A08은 서로 다른 위치에서 같은 구조 문제를 찾았다.

- 측정 전위와 Galvani potential difference의 무조건 등치.
- 무전류 평형에서만 가능한 electrolyte electrochemical-potential
  cancellation.
- `V_app`, internal `V_n`, equilibrium `V`의 표기 전환.
- lumped `R_n`, host lag `L_V`, particle-local overpotential
  distribution의 중복계산 경계.

일부 FR 제안은 “곡선 모양이 다르므로 중복이 아니다”라고
정리하지만, 출력 모양의 차이는 두 항이 물리적으로 독립임을
증명하지 않는다.

판정:

- terminal voltage에서 local interfacial driving force까지의
  potential ladder를 보존식으로 다시 세운다.
- electrolyte, electronic, charge-transfer, solid diffusion,
  contact heterogeneity의 상태·저항·과전압을 분리한다.
- 같은 물리량을 서로 다른 line shape로 두 번 세지 않았다는 것은
  limiting experiment와 parameter identifiability로 검증한다.

### INTENT-PROV-0151 — `n_j`는 증명 전까지 “물리적 다중도”가 아니라 scale parameter다

A07·A08은 `n_j<1`을 “유효 다중도”로 읽고 폭 폴백을
`n_j≈0.47–0.55`로 환산한다. 그러나 실제 microscopic degeneracy나
독립 전이 수는 일반적으로 1보다 작은 연속 fit parameter가 아니다.

판정:

- `w_j=n_jRT/F`는 편리한 scale 재모수화로 `PRESERVE`.
- `n_j`를 microscopic multiplicity로 부르는 것은 별도 통계역학
  유도와 실험 근거 전 `REJECT`.
- 최종 문건은 dimensionless scale factor, site degeneracy,
  ensemble heterogeneity를 서로 다른 기호로 둔다.

### INTENT-PROV-0152 — FR의 서지 확인은 수식·정량 주장 검증과 동일하지 않다

FR 보고서들은 Crossref/DOI metadata 확인, landing page,
서브에이전트 보고, 기존 V1 원장 승계를 폭넓게 사용했다. 동시에
각 보고서는 여러 핵심 내용을 원문 전문에서 확인하지 못했다고
명시한다.

예:

- MSMR 원문의 식번호·기호 mapping.
- 흑연·LCO peak 정량값과 figure.
- TST·hysteresis 후보 논문의 구체 조건.
- 일부 GITT·단입자·entropy 주장.

판정:

- bibliographic metadata 검증은 `PRESERVE`.
- 그것만으로 방법·수식·수치까지 tier A로 읽는 것은 `REJECT`.
- 최종 문헌 원장은 `metadata`, `full-text method`, `equation`,
  `quantity`, `sample/condition`, `model mapping`을 별도 판정한다.

### INTENT-PROV-0153 — FR의 강점은 내부정합, 약점은 실험 식별성과 외부타당성이다

이 batch의 검증은 부호, 단위, 극한, 그림 좌표, 참조, 당시 코드와의
일치를 매우 잘 다뤘다. 반면 다음은 거의 수행하지 않았다.

- 실제 multi-temperature/multi-rate dQ/dV 동시 적합.
- relaxation/interruption으로 reversible·metastable·kinetic 분해.
- reference-electrode/half-cell로 full-cell contribution 분리.
- calorimetry/entropic coefficient와 peak shift의 교차검증.
- out-of-sample chemistry·protocol prediction.
- competing closures의 식별가능성 비교.

판정:

- FR PASS를 `INTERNAL_CONSISTENCY_REVIEW`로 보존한다.
- 과학적 완결성은 별도 literature, experiment, identifiability,
  validation gate를 통과해야 한다.

### INTENT-PROV-0154 — FR 수정문도 기계 적용하지 않고 독립 판정한다

FR 제안에는 정확한 교정과 함께 아직 승인할 수 없는 해석도 섞였다.

- 평균장 오차를 “피팅된 Omega가 흡수”한다는 주장.
- 서로 다른 모양이면 중복계산이 아니라는 주장.
- two-phase peak의 보편적 `RT/F` 잔여폭.
- spinodal gap을 열역학적 hysteresis 상한으로 직접 사용.
- 문헌 metadata 확인을 정량 anchor로 확장하는 경향.

판정:

- H/M/L 등급은 우선순위 정보일 뿐 채택 판정이 아니다.
- 각 후보는 `PRESERVE/CORRECT/SUPERSEDE/EMPIRICAL_ONLY/
  THEORY_ONLY/REJECT/UNVERIFIED`로 다시 판정한다.
- 제안 LaTeX를 자동 cherry-pick하지 않는다.

### INTENT-PROV-0155 — 이론·코드·검증 문건의 역할 분리가 필요하다

FR은 당시 코드와의 일치 검산을 수행하고 구현 이름·기본값·가드까지
물리 절의 수정안에 끌어오는 경우가 있다. 추적 가능성에는 유용하지만
사용자가 원하는 정본 이론 문건의 경계와는 다르다.

판정:

- 최종 physics manuscript에는 물리·화학 논리와 실험적 판별법만 둔다.
- 구현 이름, API, default, bit-exact contract는 implementation
  concordance로 옮긴다.
- test 결과와 데이터 적합성은 verification ledger로 분리한다.
- 세 문건 사이에는 식 ID·가정 ID·시험 ID의 traceability를 둔다.

## Coverage Status

- 이 batch의 10문건, 3,579행은 `READ`.
- 누적 coverage 반영 후 목표는 179문건, 39,799행이다.
- v1.0.22 잔여 목표는 38문건, 7,883행이다.

## Next

Step 19.6H:
FR A09–A16 심층 review 8문건 2,644행을 전문 검독해 동역학 꼬리,
관측식, LCO/열 장과 구현 경계의 후속 결함을 판정한다.
