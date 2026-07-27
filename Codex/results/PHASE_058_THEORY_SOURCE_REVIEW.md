# Phase 058 v1.0.10–v1.0.13 theory source review

상태: `SOURCE_READ_COMPLETE / CODE_AND_LITERATURE_ADJUDICATION_PENDING`  
대상: 6개 unique TeX source, 9,532 lines  
판정 경계: 이 문서는 과거 문건의 감사 기록이며 새 이론 정본이 아니다.

## 전수 검독 범위

| Source | Coverage | 상태 |
|---|---:|---|
| `v1.0.10/graphite_ica_ch1_v1.0.10.tex` | 1–1937 | COMPLETE |
| `v1.0.10/graphite_ica_ch2_v1.0.10.tex` | 1–750 | COMPLETE |
| `v1.0.12/graphite_ica_ch1_v1.0.12.tex` | 1–2358 | COMPLETE |
| `v1.0.12/graphite_ica_ch2_v1.0.12.tex` | 1–777 | COMPLETE |
| `v1.0.13/graphite_ica_ch1_v1.0.13.tex` | 1–2934 | COMPLETE |
| `v1.0.13/graphite_ica_ch2_v1.0.13.tex` | 1–776 | COMPLETE |

`COMPLETE`는 원문을 빠짐없이 읽었다는 뜻일 뿐, 물리 타당성이나
문건–코드 정합성의 PASS가 아니다.

## 계보 판정

### v1.0.10

최초의 실질 골격은 다음과 같다.

1. 전이별 logistic equilibrium peak와 용량 가중 합
2. regular-solution spinodal에서 만든 대칭 hysteresis gap
3. Eyring형 시간상수에서 전압축 lag 길이를 만든 causal low-pass tail
4. 반응 엔트로피와 온도 이동, Bernardi형 reversible heat
5. 같은 슬롯을 LCO에 재사용하려는 전극 공통 facade

이 골격은 실용적 피팅 커널로서는 재사용 가치가 있다. 그러나 이론
문건이 `func_*`, dictionary key, N0–N9, gate와 기본값을 본문 전체에서
설명하므로 현재 사용자가 정한 “문건은 물리·화학만, 구현은 별도”라는
경계를 충족하지 않는다.

주요 결함은 다음과 같다.

- `|I| = c_rate Q_cell`을 쓰면서 `Q_cell`을 C로 정의한다
  (Ch1 lines 194–221). `c_rate`가 h⁻¹이면 A를 얻기 위해 Ah를 쓰거나
  C 단위 입력에 1/3600이 필요하다. 이 단위 계약은 v1.0.10에서 닫히지
  않는다.
- Li 점유율 `theta`, 여집합 진행률 `xi`, charge/discharge와
  delithiation/lithiation을 여러 문단에서 혼용한다. dQ/dV 종의 절댓값은
  여집합 교환에 불변이어서 방향 오류가 출력에서 잠복할 수 있다.
- equilibrium logistic에 sweep direction을 넣는다. 평형 상태함수와
  경로 라벨을 분리하지 못하고 branch/protocol 표현을 equilibrium으로
  부른다.
- `w=nRT/F`는 독립 단일-site lattice gas의 `n=1`에서만 직접 유도된다.
  임의 `n`과 two-phase peak의 유한 폭은 같은 유도로 정당화되지 않는다.
- spinodal extremum 차를 측정 hysteresis에 바로 연결하고 경험적
  `gamma`, `h_eta`로 축소한다. 이 수식은 phenomenological branch
  parameterization이며, 평형 상공존 자체의 유일한 결과가 아니다.
- `A=min(z_cut nRT, A_cap RT)`로 국소 affinity를 상수화하고,
  `Delta H_a_eff=Delta H_a-chi Omega`를 deep-tail 근사에서 가져온다.
  따라서 사용자가 요구한 `T`, 전류, 전극전위에 따른 국소 장벽 변화가
  실제 forward path에는 남지 않는다.
- 작은 lag에서 equilibrium kernel로 바꾸는 grid-step switch는 수치
  처방이며 물리 경계가 아니다. branch handoff는 연속성도 보장하지 않는다.
- LCO 도핑 효과를 주로 `Omega` 감소와 중심 `U` 이동으로 접는다.
  고전압 doped LCO의 산소 안정성, 상질서, 결함화학, 전자구조와 수송을
  설명하기에는 부족하다.

### v1.0.11

queue와 blob 계보상 v1.0.10의 핵심 source가 그대로 재사용된다. 버전
라벨이나 handover의 “정정”만으로 새 물리 검증으로 세지 않는다.
실제 diff와 claim의 효력은 Step 30에서 commit patch로 다시 연결한다.

### v1.0.12

개선:

- Bragg–Williams/Nernst 부호를 바로잡는다.
- two-phase logistic 폭을 엄밀 평형 예측이 아니라 현상학적 폭으로
  명시한다.
- hysteresis branch 평균은 작은-gap 선형화라는 한계를 적는다.
- low-pass의 작은-lag 극한이 스스로 equilibrium bell로 환원되지 않고
  별도 switch에 의존함을 인정한다.
- 내부 finite-difference 검증과 외부 실측 검증을 일부 구분한다.

미해결 또는 새 위험:

- Ch1 lines 199–227에서 `Q_cell`은 여전히 C인데
  `|I|=c_rate Q_cell`이다.
- two-phase 폭은 자유 피팅이라고 하면서 모든 `n` 전이에
  `w(T)=nRT/F`를 강제하고, 그 강제된 온도 미분을 configurational
  entropy의 증거로 다시 사용한다. 이는 구현 내부 미분 일치이지
  two-phase 폭의 열역학적 검증이 아니다.
- `A_cap_RT=4`와 `z_cut=4.357`, 통상 `n≈1`이면 `min`의 cap이 항상
  선택된다. 이름은 affinity지만 실질적으로 임의 `4RT` 상수가 kinetics를
  지배한다.
- `Delta H_a_eff`는 전위 함수가 아니라 전이당 동결 상수다.
  문건이 서술하는 `∂ln Lq/∂V<0`는 실제 계산 경로에서 0이다.
- LCO 세 전이를 모두 같은 scalar regular-solution coordinate로
  표현하고, `Omega>2RT`를 아직 값도 없는 “후보”로 둔다. 다중
  sublattice/order parameter 또는 phase-specific free energy가 없다.
- 전자 엔트로피는 현 구현에서 `T_ref`, `x_center`에 동결되어 이론의
  `T²` 이동과 조성 국소성을 구현하지 않는다.

### v1.0.13

개선:

- Part 0을 추가해 ensemble, partition function, occupancy와 entropy를
  교재형으로 자세히 설명한다.
- `theta`를 Li occupancy, `xi=1-theta`를 delithiation progress로
  명시해 이전의 여집합 혼동을 상당 부분 고친다
  (Ch2 lines 143–176).
- C-rate 단위 설명에 Ah 사용과 시간단위 정합 주의를 추가한다
  (Ch1 lines 203–233).
- theory-only 식과 현행 동결 구현의 차이를 일부 자진 명시한다.

그러나 “설명이 길어진 것”과 “물리가 폐쇄된 것”은 다르다.

- 같은 `Q_cell`을 C 또는 Ah로 허용하면서 정규화와 전류 환산에 공용한다.
  API에서 단위를 타입/별도 변수로 분리하지 않으면 여전히 모호하다.
- Fermi–Dirac의 energy-level occupancy와 composition-dependent MIT
  activation curve가 모두 logistic이라는 이유만으로 후자를
  “물리적으로 정당화”한다 (Ch1 lines 2347–2447). 함수형 동형은
  microscopic derivation이 아니다.
- `g(E_F,x)` 연속곡선이 문헌에 없다고 인정하면서
  `g_max=13`, `x_MIT=0.85`, `dx=0.05`의 logistic derivative를 넣어
  중심에서 약 `-46 J mol^-1 K^-1`을 만든다
  (Ch1 lines 2449–2476). 이는 같은 문건이 인용한 총 부분몰 값
  약 `0.18 kB/atom ≈ 1.5 J mol^-1 K^-1`과 정의·정규화·상분율을
  포함해 반드시 직접 대조해야 한다. “서로 다른 척도”라는 선언은
  검산을 대체하지 못한다.
- `S_e(x,T)`의 조성미분을 반응 전자엔트로피로 쓰려면 DOS의 기준,
  formula-unit/Co/atom normalization, chemical potential 유지조건,
  two-phase lever rule와 상분율을 명시해야 한다. 현재 logistic
  interpolation은 검증 대기 가설이다.
- `U_1(V,T)`가 `xi_eq`, 다시 `U_1`을 참조하는 고정점 문제를 1회 갱신
  또는 기준점 동결로 넘긴다. 수렴성·유일성·thermodynamic consistency가
  증명되지 않았다.
- LCO order–disorder와 MIT를 단일 host-neutral regular solution의
  `Omega_j`만 교체해 표현한다. 고전압 doped LCO 목표에는 명백히
  불충분하고, 문건 자체도 4.5 V 이상을 범위 밖으로 둔다.
- Ch2의 overlap entropy 완전식은 강제한 `w(T)=nRT/F`를 유한차분한
  결과와 일치한다. 이는 좋은 analytic/code identity test지만 실험적
  물리 검증은 아니다 (Ch2 lines 498–520, 717–720).
- reversible heat를 charge/discharge branch의 단순 평균으로 두는 것은
  작은-gap/동일-shape 선형화에서만 가능하다 (Ch2 lines 597–619).
  비평형 branch 자료에서 equilibrium entropy를 복원하는 일반식이 아니다.
- Ch1/Ch2 모두 코드 식별자, 구현 상태, gate와 self-test를 광범위하게
  포함하므로 현재 최종 문건 형식 제약을 충족하지 않는다.

## 현재 보존 후보

다음은 후속 독립 유도와 문헌 확인을 통과하면 보존할 수 있는 자산이다.

- 전하보존에서 dQ/dV 면적을 전이 용량과 연결하는 구조
- 독립-site lattice gas의 occupancy와 ideal logistic 관계
- regular-solution 곡률과 `Omega=2RT` mean-field critical condition
- equilibrium, kinetic lag, ohmic polarization, observation kernel을
  분리하려는 계층화
- entropy coefficient와 reversible heat의 부호를 명시적 reaction
  convention으로 연결해야 한다는 문제의식
- simulation self-consistency와 experimental validation을 구분하려는
  v1.0.12–13의 정정

## 현재 교정·폐기 후보

- 평형 logistic에 방향 부호를 넣는 서술
- graphite/LCO/Si를 전이 dictionary 교체만으로 같은 물리라 부르는 주장
- arbitrary cap, grid threshold, one-step update를 물리 법칙으로 읽는 것
- `Omega`를 equilibrium, hysteresis, activation barrier와 doping
  smear에 중복 사용하면서 자유에너지에서 일관되게 유도하지 않는 구조
- function-name/code-key/node-map을 이론 본문에 두는 구성
- internal derivative PASS를 외부 물리 타당성 PASS로 승격하는 관행

## 다음 검증 질문

Step 27에서 다음을 코드와 직접 대조한다.

1. `Q_cell`, `c_rate`, `I_abs`의 실제 단위와 3600 배 경로
2. facade direction이 graphite와 LCO에서 실제 어떤 `sigma`를 만드는지
3. `Omega`, `gamma`, `h_eta`, `A_cap_RT`, `use_dH_eff`의 default와
   실제 활성 경로
4. Eyring prefactor/activation energy가 만드는 lag의 실제 크기
5. branch switch의 면적·연속성·grid dependence
6. electronic entropy의 eV→J, Avogadro, sign, `T`/composition 동결
7. tests가 default path와 theory-only path 중 무엇을 검사하는지

문헌 검증 전에는 LCO MIT/DOS, dopant 효과, graphite phase assignment와
수치 anchor를 `PRESERVE`로 승격하지 않는다.
