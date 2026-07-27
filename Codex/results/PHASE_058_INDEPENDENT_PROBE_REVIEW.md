# Phase 058 독립 물리·수치 probe 판정

정본일: 2026-07-28  
기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`  
기계 결과: `Codex/results/PHASE_058_INDEPENDENT_PROBES.json`

## 방법

v1.0.10, v1.0.12, v1.0.13 production module을 원본 수정 없이 import하고,
다음 항목을 구현과 독립된 logistic derivative, 해석 FWHM,
유한차분과 sign/unit identity로 검산했다.

- single-transition 면적·peak height·FWHM
- \(T\) 변화와 `n`/`w` 우선순위
- \(I=0\), 저율, 고율의 default와 direct-lag 경로
- C-rate–capacity 환산
- hysteresis branch gap과 호출 간 state memory
- entropy coefficient, reversible/irreversible heat
- LCO 방향 facade, electronic entropy toggle와 default kinetic scope

세 production source의 실행 전후 SHA-256은 동일했다.

## 보존할 수학 골격

### 평형 logistic derivative

세 버전 모두 single transition에서 독립식

\[
\frac{\mathrm dQ}{\mathrm dV}
=\frac{Q}{w}\frac{\exp z}{(1+\exp z)^2},
\qquad z=\frac{V-U}{w}
\]

과 최대 \(3.23\times10^{-15}\) 이내로 일치했다.
넓은 전위창 적분은 \(Q=0.5\)에 대해
\(7.8\times10^{-16}\) 이내였고, peak height \(Q/(4w)\)도 일치했다.
해석 FWHM \(4\operatorname{arcosh}\sqrt2\,w\)와 수치값도 grid 오차
범위에서 일치했다. 이 kernel의 미분·정규화 구현은 `PRESERVE`다.

### 내부 열역학·열 identity

single-transition 중심에서 `entropy_coefficient`는
\(\Delta S/F\)와 일치했고, 중심 전위의 유한차분과도
약 \(2.2\times10^{-14}\ {\rm V\,K^{-1}}\) 이내였다.
`reversible_heat`는 구현이 선언한
\(-IT(\partial U/\partial T)\) identity와 정확히 일치했다.
이것은 내부 수학 정합성으로 `PRESERVE`하되, 실험적 entropy 값의
외적 타당성으로 승격하지 않는다.

### hysteresis closed form

\(\Omega=12\ {\rm kJ\,mol^{-1}}\), \(\gamma=1\) probe에서
closed-form gap은 86.6856 mV, 수치 peak gap은 86.6900 mV였다.
branch center 구현은 자기 식과 일치한다. 다만 아래처럼 경로 기억
모델의 완결을 뜻하지 않는다.

## 교정이 필요한 핵심

### 1. 현재 default는 전류 broadening을 만들지 않는다

세 버전의 shipped graphite transition과 `Rn=0`에서
\(I=0,0.02,0.2,1.0\) A 곡선의 최대 절대차는 모두 정확히 0이었다.
1 A에서도 전이별 derived \(L_V\)는 약
\(4.9\times10^{-7}\)–\(4.7\times10^{-9}\) V라 grid switch 아래에
머물고 평형 branch로 떨어진다.

따라서 default code는 사용자가 관측한 “정전류에서 peak가 낮아지고
넓어짐”을 설명하지 않는다. `Rn`을 켜면 중심 이동은 만들 수 있으나
그 자체로 width/height 변화는 아니다.

### 2. direct `L_V` 우회는 \(I\to0\) 극한을 위반한다

`L_V=0.02` V를 직접 준 probe는 \(I=0\)과 \(I=1\) A 곡선이 정확히
동일했다. 동시에 \(I=0\) curve는 equilibrium보다 peak가
24.33에서 12.72로 낮아지고 FWHM이 18.11에서 32.74 mV로 넓었다.

이는 direct override가 current보다 먼저 반환되어 \(I\le0\) 분기를
우회하기 때문이다. fitting 편의 파라미터가 무전류 평형에서도
동역학 broadening을 남기므로 `CORRECT`다. 최소한
\(L_V(I,T,V,\text{state})\to0\) as \(I\to0\) 계약이 필요하다.

### 3. low-temperature 평형 trend만으로는 관측을 설명할 수 없다

ideal equilibrium kernel은 258.15→318.15 K에서 FWHM이
78.42→96.64 mV로 증가하고 peak는 5.62→4.56으로 감소했다.
즉 온도를 낮추면 평형 peak는 더 좁고 높아진다. 사용자의 저온
정전류 관측인 낮고 넓은 peak는 equilibrium thermal width가 아니라,
저온에서 강해지는 kinetic/transport/heterogeneity/measurement
convolution이 이를 압도해야 설명된다.

현 default kinetic path는 비활성이므로 해당 핵심 mechanism은
v1.0.10–v1.0.13에서 닫히지 않았다.

### 4. `n`과 `w`의 역할이 중복·shadowing된다

transition에 `n=1`과 `w=0.005`를 함께 주면 `w`가 없는 `n=1`
curve와 bit-identical이었다. 반면 `w`만 주면 FWHM은
258 K와 318 K에서 모두 17.62 mV로 고정됐다.

따라서 shipped dict의 `w`는 inert하고, `n`은 \(T\)-비례 폭,
`w`-only는 \(T\)-불변 empirical 폭이라는 서로 다른 observation
가정을 암묵적으로 선택한다. 둘을 한 “물리 폭”으로 설명하면 안 된다.

### 5. C-rate 단위 계약에 3600 인자가 없다

`Q_cell=3600`, `c_rate=0.2`를 넣은 `curve`는
`I_abs=720` 호출과 정확히 같았고 `I_abs=0.2`와 크게 달랐다.
`Q_cell`이 coulomb이면 올바른 환산은
\(I=C_{\rm rate}Q_{\rm cell}/3600\)이다. 반대로 `Q_cell`이 Ah이면
현재 곱셈은 맞지만, 같은 값은 `dqdv` 내부 정규화에서 “전하”로
사용되며 문건도 C와 Ah를 혼용했다.

단위를 타입/이름/API에서 분리하기 전까지 `BLOCKER_UNIT_CONTRACT`다.

### 6. hysteresis는 branch split이지 cycle memory가 아니다

방전→충전→방전을 호출한 뒤 첫 번째와 두 번째 방전 curve는
bit-identical했다. 객체에는 호출 사이에서 갱신되는 phase fraction,
turning point, rest history가 없다. 내부 causal filter는 한 voltage
array 안의 sweep 방향만 반영한다.

따라서 현 모델을 “기억” 또는 partial-cycle hysteresis 모델로 부르면
과장이다. static branch kernel로는 보존할 수 있지만 실제 memory는
state evolution과 protocol initial condition으로 새로 닫아야 한다.

### 7. irreversible heat의 \(\ge0\)는 code invariant가 아니다

`irreversible_heat(3.7,3.8,I=1)`은 \(-0.1\) W를 반환한다.
식 \(I(U_{\rm oc}-V)\)가 양수가 되려면 전류·전압·운전 방향의
일관된 sign/domain 계약이 먼저 필요하다. docstring의 “\(\ge0\)”를
무조건 보장하는 구현은 아니므로 `CORRECT_SIGN_CONTRACT`다.

## LCO 판정

- v1.0.10과 v1.0.12에서 high-level `direction="charge"`는 low-level
  \(s=-1\)과 일치했다. LCO 탈리튬화 슬롯 \(s=+1\)이라는 문건 규약과
  반대다.
- v1.0.13은 high-level charge가 \(s=+1\)과 정확히 일치해 이 facade
  오류를 고쳤다. 이 변경은 `PRESERVE`.
- 세 버전 모두 default LCO transition에 `Omega`와 `dH_a`가 없고,
  `Rn=0`에서 \(I=0\)과 1 A curve가 정확히 동일하다. 따라서 고전압
  doped LCO의 rate/temperature stability를 설명하는 모델이 아니다.
- electronic toggle은 해당 transition의 effective entropy를
  정확히 \(-45.6783\ {\rm J\,mol^{-1}\,K^{-1}}\)만큼 바꾼다.
  이는 hardcoded target의 내부 재생이며 measured composition-resolved
  partial entropy, DOS normalization 또는 \(T^2\) closure의 검증이 아니다.

## Step 27.4 결론

평형 logistic kernel, branch-gap 함수와 열 identity의 내부 구현은
보존할 수 있다. 그러나 사용자 연구의 중심인 저온·유한전류
peak suppression/broadening, 전위·상태 의존 barrier, history,
doped high-voltage LCO는 이 계보에서 구현되지 않았다.

특히 default-current invariance, direct-lag의 \(I=0\) 위반,
C-rate 단위와 heat sign은 후속 이론·코드 계약 전에 반드시 고쳐야 할
blocker다. 다음 Step 27.5에서 저장된 golden NPZ 13 array를 전수
처분하고 bitwise provenance와 physical validity를 최종 분리한다.
