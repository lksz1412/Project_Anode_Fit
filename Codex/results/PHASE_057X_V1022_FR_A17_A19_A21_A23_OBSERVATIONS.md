# Phase 057X — v1.0.22 FR A17–A19·A21–A23 심층검토 관찰

정본일: 2026-07-28
세부 Step: 19.6I
범위: 6 unique documents, 2,894 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 FR 심층 검토 보고서를 첫 행부터 끝 행까지 검독했다.
400행을 넘는 A18·A19·A22·A23은 연속 구간으로 나누어 전량
확인했다.

- `results/comp_FR/A17_REVIEW.md`
- `results/comp_FR/A18_REVIEW.md`
- `results/comp_FR/A19_REVIEW.md`
- `results/comp_FR/A21_REVIEW.md`
- `results/comp_FR/A22_REVIEW.md`
- `results/comp_FR/A23_REVIEW.md`

이 문건들은 보고 전용 경쟁 검토이며 본문을 직접 수정하지 않았다.
따라서 아래 판정은 발견과 재계산을 회수한 잠정 감사 결과이지,
각 보고서의 제안 LaTeX를 자동 채택한 것이 아니다.

> 후속 상태 갱신(Phase 057 Step 19.6J): 아래
> `INTENT-PROV-0165`의 LCO 예제 좌표·라벨 결함은 C-048에서
> 산문·표·검산 박스가 정정됐고, `INTENT-PROV-0169`의 외부
> Si 분율 규약은 사용자 결정 C-052에서 `m_Si`(wt%)로 바뀌어
> 내부 `f_Si`(용량분율) 환산과 분리됐다. 아래 항목은 결함의
> 발견·물리적 교훈으로 보존하며, v1.0.22 최종 상태의 미수정
> 결함으로 읽지 않는다.

## Provisional Findings

### INTENT-PROV-0165 — 전극 역할·반응 방향·조성 좌표의 명시적 사상이 선행되어야 한다

A17과 A19는 같은 “충전/방전” 표기가 서로 다른 물리 방향을
가리키는 문제와 LCO 조성 좌표의 혼용을 드러냈다.

- 프로젝트의 `sigma_d=+1` 방전은 full-cell 역할을 기준으로
  흑연의 탈리튬화를 뜻한다.
- graphite half-cell cycler의 discharge는 흔히 흑연 리튬화를
  뜻한다.
- LCO 예제의 `xbar`는 탈리튬 분율인 반면 `x_MIT`의 `x`는
  `Li_xCoO2`의 Li 함량이다.

문서 자체의 사상 `x=0.94-0.19 xi_eq,1`을 적용하면
`xbar=0.50`이 MIT 게이트 중심에 가깝고 `xbar=0.85`는 금속측이다.
현 예제의 “게이트 밖/중심” 라벨은 반대로 붙었다.

판정:

- 데이터 열 이름을 그대로 반응 방향으로 사용하지 않는다.
- 각 데이터셋에 working electrode, half/full-cell, current sign,
  lithiation/delithiation, stoichiometric coordinate의 명시적
  변환표를 둔다.
- `x`, `xbar`, `theta`, `xi_j`, SOC를 서로 대입할 때 보존식과
  단조 방향을 시험하는 gate를 둔다.
- 현재 LCO worked example의 좌표 해석은 `CORRECT`.

### INTENT-PROV-0166 — LCO의 국소 MIT 물리와 현 코드의 전역 상수 전자항은 일치하지 않는다

A19의 재계산상 이론 산문은 전자 엔트로피를 조성 의존
`sigma(x)[1-sigma(x)]` 게이트로 설명한다. 그러나 당시
`_effective_dS_rxn` 구현은 각 전이의 고정 `x_center`에서 평가한
전자 엔트로피를 `xbar`와 전위에 무관한 상수로 가산한다.

그 결과 이론상 게이트 밖이라고 서술한 `xbar=0.50`에서도 전자항을
끄면 엔트로피 계수가 약 `-0.312 -> -0.035 mV/K`로 크게 바뀌며,
재중심화를 허용하면 부호까지 바뀐다. 수치 재현은 국소 MIT 게이트가
작동해서가 아니라 고정 오프셋이 모든 조성에 작동해서 얻어진다.

판정:

- 현재 전자항 구현을 문건 식의 1:1 구현으로 보는 주장은 `REJECT`.
- 조성 사상, 국소 전자 자유에너지, 전이별 반응 엔트로피 투영을
  먼저 물리적으로 정의한 뒤 구현한다.
- `xbar` 의존성을 구현하지 않는 축약형은 `EMPIRICAL_ONLY`로
  명명하고, 국소 MIT 해석에 사용하지 않는다.
- 문건의 예제 라벨만 고쳐 고정 오프셋 구현을 보존하는 방식은
  근본 해결이 아니다.

### INTENT-PROV-0167 — LCO의 질서·상분리·MIT를 하나의 `Omega`로 닫은 것은 축약 closure다

A18은 정규용액 대수 자체와 문헌 방향성은 상당 부분 보존할 수
있지만 물리적 귀속이 과도하게 압축됐음을 보였다.

- 전이별 order/disorder, miscibility gap, MIT가 하나의 effective
  interaction parameter로 접혀 있다.
- 본문은 pure-LCO `Omega` 초기값이 있는 것처럼 읽히지만 당시
  수치 경로에는 명시값이 없어 기본 `Omega=0`으로 귀결되는 곳이
  있다.
- Mg 등 도핑이 구조 전이만 억제하고 전자항은 보존한다는 서술은
  hole doping에 따른 MIT·전자 상태 변화 가능성을 누락한다.
- `Omega>2RT`는 mean-field regular-solution 안의 안정성 조건이지
  실제 LCO 질서상의 필요충분조건이 아니다.
- charge-order 엔트로피 `0.47/1.49 J mol^-1 K^-1`, 전자 DOS
  `g(E_F)` 최대값과 일부 조성 귀속은 1차 문헌 검증이 남아 있다.

판정:

- `Omega`를 결정 구조, 전하 질서, 전자 전이의 공통 원인으로
  승격하지 않고 reduced free-energy closure로 한정한다.
- 고전압 도핑 LCO에는 산소 redox/산소 손실, 구조전이, cation
  mixing, 전해질·표면 반응, 전자구조 변화 중 데이터가 요구하는
  기작을 분리한 상태 변수가 필요하다.
- 도핑 효과는 무도핑 파라미터의 단순 감쇠가 아니라 물질·도핑종별
  독립 가설과 문헌 prior로 검증한다.
- 명시하지 않은 `Omega=0` fallback을 물리 기본값으로 쓰지 않는다.

### INTENT-PROV-0168 — v1.0.22 Si 장은 생존 지도이지 완결 피팅 모델이 아니다

A21–A23의 가장 중요한 장점은 흑연에서 무엇을 이월할 수 있고
Si에서 무엇이 새 물리인지 분리하고, GS-1(소성 구성식)과
GS-2(블렌드 비가산성)를 정직한 공백으로 남긴 점이다. 그러나
다음 이유로 실제 데이터 피팅용 Si/SiO_x/Si–C 모델은 아직 닫히지
않았다.

- amorphous/crystalline Si와 SiO_x 케이스의 전이별
  `{U_j,w_j,Q_j}` 목록이 없다.
- 표는 평균전위·가역용량·ICE·히스테리시스 규모 같은 케이스
  집계값만 제공해 전이 리스트를 유일하게 정하지 못한다.
- 구조 carryover라는 판정 범주가 일부 표에서 정의되지 않았다.
- plastic flow, stress history, first-cycle conversion, trapped Li,
  matrix constraint, interfacial loss의 constitutive closure가 없다.

판정:

- 현 Si 장의 지도·정직 공백·공통 전위/전하보존 출발점은
  `PRESERVE`.
- 표의 집계값으로 전이 리스트를 임의 생성하는 것은 `REJECT`.
- 독립적으로 관측되지 않는 peak component를 곧바로 상 또는
  상전이로 명명하지 않는다.
- 실험 관측자와 식별가능성을 갖춘 최소 Si 상태모델을 새로 유도한
  뒤에만 생산 코드로 승격한다.

### INTENT-PROV-0169 — `f_Si` 용량분율과 실험 wt%의 혼용이 비교 범위를 왜곡한다

문건의 `f_Si in [0,0.3]`은 Si 용량분율인데 A21–A23의 여러
실험 앵커는 10–30 wt% 질량분율이다. 비용량 차이를 적용하면
`f_Si=0.3`은 대략 수 wt%에서 10여 wt%에 대응하고, 30 wt% Si
실험은 모델 창 밖에 놓일 수 있다.

판정:

- `f_Si^mass`, `f_Si^active-mass`, `f_Si^capacity`, electrode-level
  loading fraction을 별도 기호로 둔다.
- 변환에는 실제 Si 상태, graphite/Si 가용 비용량, binder/conductive
  mass, initial irreversible loss를 명시한다.
- 서로 다른 분율의 실험을 같은 x축에 둔 현재 validation 서술은
  `CORRECT`.
- 범위 밖 고-Si 실험은 비가산성의 존재 근거로는 쓸 수 있지만
  현 모델 창 안의 정량 검증으로는 쓰지 않는다.

### INTENT-PROV-0170 — common-chemical-potential 혼합은 유효한 평형 baseline일 뿐 완결 blend 모델이 아니다

A21–A23이 유도한 host partition product와 common-potential
charge-balance sum은 독립 host, 가산 용량, 평형이라는 가정 아래
내부적으로 정합한다. 하지만 합성 `dQ/dV` 식은 equilibrium peak
sum이며, 전체 모델의 finite-current lag tail과 동일한 식이 아니다.
또한 같은 전극의 graphite와 Si가 공통 `T`, `I`, polarization
mapping을 공유해야 한다는 구현 계약이 빠져 있다.

판정:

- common-potential charge conservation을 zero-order baseline으로
  `PRESERVE`.
- host interaction, shared porosity/conductivity, mechanical
  constraint, lithium inventory coupling, rate-dependent current
  partition을 독립 correction layer로 둔다.
- equilibrium blend와 finite-current observation model을 같은
  식으로 표기하지 않는다.
- 성분 가중합의 내부 consistency 통과를 실제 blend validation으로
  부르지 않는다.

### INTENT-PROV-0171 — Si의 큰 히스테리시스 배제 근거는 크기가 아니라 기작이어야 한다

`Omega=4RT`에서 regular-solution spinodal gap이 약 54.8 mV라는
재계산은 맞다. 그러나 같은 식은 `Omega`를 키우면
`Omega≈10RT`에서 약 311 mV도 낼 수 있다. 따라서 “55 mV라서
수백 mV Si 히스테리시스를 설명할 수 없다”는 명제는
`Omega`를 흑연 규모로 제한할 때만 성립한다.

Si에 별도 물리가 필요한 강한 근거는 in-situ stress evolution,
stress-potential coupling, plastic dissipation, amorphization/
crystallization path dependence다. 순수 탄성에서도 유한율 확산
응력은 경로 의존적일 수 있으므로 “탄성은 항상 단일값”이라는
표현 역시 준정적 조건이 필요하다.

판정:

- Larché–Cahn 가역 stress-potential coupling과 부호·차원 유도는
  `PRESERVE`.
- 수백 mV 크기만으로 regular solution을 배제하는 논증은 `CORRECT`.
- plasticity/damage/phase-path constitutive law가 없는 현 단계는
  `THEORY_ONLY`; 수치 파라미터로 조용히 메우지 않는다.

### INTENT-PROV-0172 — v1.0.22의 코드 요구명세도 그대로 구현할 수 없는 결함을 가진다

A23의 코드 절은 중요한 회귀 의도를 담지만 다음 계약이 불완전하다.

- `integral dQ/dV dV=Q`는 비영 background `Cbg`가 있으면 성립하지
  않으며 background-subtracted/windowed 정의가 필요하다.
- `f_Si=0` bit-exact는 `0*Si` 평가가 아니라 Si 경로 자체를
  우회하고 흑연의 기존 가산 순서를 보존해야 한다.
- `f_Si` 연속성 gate에 격자, norm, threshold, `f->0+` 접속 조건이
  없다.
- G2가 가리키는 일부 문헌 이름은 실제 bibliography/해당 절에
  없거나 다른 절의 인용이다.
- 케이스 집계표에서 전이별 초기값을 만들라는 요구는 구현자에게
  임의 물리값 생성을 위임한다.

판정:

- bit-exact legacy preservation, background accounting, charge
  conservation, endpoint limit의 취지는 `PRESERVE`.
- 수치 gate와 API/identifier/default는 물리 본문이 아니라 별도의
  implementation-conformance 정본에 둔다.
- 현재 사용자의 더 엄격한 지시대로 최종 물리 문건에는 코드 절을
  두지 않고, 식별 가능한 물리 계약만 남긴다.
- 빈 물리 파라미터는 `None`/명시적 미지원 상태로 실패하게 하며
  임의 fallback을 두지 않는다.

### INTENT-PROV-0173 — 심층 review의 자체 검산은 강하지만 독립 문헌·실험 검증과 구분해야 한다

A17–A23은 식 재유도, 코드 실명 대조, DOI/Crossref 확인, build,
수치 round-trip을 수행해 실제 결함을 다수 발견했다. 특히 LCO
좌표 역전과 전자항 동결, Si 분율 단위 충돌, ghost reference,
background 적분 오류는 회수 가치가 높다.

반면 일부 정량은 초록 또는 2차 자료 수준이며, 제안 문구에는
기존 closure를 더 잘 설명하는 것과 closure 자체를 검증하는 것이
섞여 있다. 문건 내부의 동일 식·동일 코드로 얻은 round-trip은
공개 실험 데이터에 대한 예측 검증이 아니다.

판정:

- 결함 위치·재계산·출처 상태는 `PRESERVE`.
- 각 보고서의 수정문은 `UNVERIFIED` 후보로 유지한다.
- 1차 문헌 전문, 공개 raw data, protocol metadata, held-out
  temperature/rate/composition, calorimetry/stress cross-modal
  evidence를 거쳐야 물리 정본으로 승격한다.

### INTENT-PROV-0174 — 사용자가 요구한 끝판 방향은 물질별 자유에너지–동역학–관측자의 분리다

이번 묶음을 사용자의 현재 지시와 함께 읽으면 최종 방향은
“한 보편식에 모든 물질 효과를 밀어 넣기”가 아니다.

1. 물리 문건은 thermodynamic state, free-energy contribution,
   kinetic barrier, dissipative internal variable, electrode/cell
   observation map을 순서대로 유도한다.
2. graphite staging, doped high-voltage LCO, Si/SiO_x/Si–C는 공통
   보존 법칙만 공유하고 물질별 상태 변수와 closure를 분리한다.
3. 유한전류에서 peak 감소·broadening, 저온 강화, 전위·상태 의존
   장벽을 하나의 임의 convolution/cap으로 설명하지 않고 경쟁
   메커니즘과 식별가능성을 시험한다.
4. 코드는 이론 문건의 식·가정·적용범위를 추적하는 별도
   concordance 정본으로 관리하며, 물리 본문에는 구현 명칭을
   넣지 않는다.
5. 실제 fit 성공은 필요조건일 뿐이며, 단위 불변성, 제한극한,
   parameter recovery, held-out 예측, material/protocol transfer를
   통과해야 한다.

이 방향은 새 이론·코드 작업을 즉시 시작한다는 뜻이 아니다.
v1.0.10–v1.0.25.2의 나머지 이력과 후속 철회를 모두 읽은 뒤
Phase 069 종합 gate에서만 정본 설계를 확정한다.

## Coverage Status

- 이 batch의 6문건, 2,894행은 `READ`.
- 누적 coverage 반영 후 목표는 193문건, 45,337행이다.
- v1.0.22 누적 목표는 77/101문건, 14,510/16,855행이다.
- v1.0.22 잔여 목표는 24문건, 2,345행이다.

## Next

Step 19.6J:
FR 운영 계획·resume·triage·M1–M4 8문건 284행을 전문 검독해
심층 검토의 운영 규율, 마스터 판정 절차, 실제 채택·보류 이력을
복원한다.
