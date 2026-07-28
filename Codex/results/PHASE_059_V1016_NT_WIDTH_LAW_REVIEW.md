# Phase 059 v1.0.16 \(n(T)\) 폭 법칙 독립 판정

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1016_NT_DWDT_ALGEBRA_AND_OPT_IN_ROUNDTRIP_PASS_BUT_EMPIRICAL_STATUS_DEFAULT_BRANCH_POSITIVITY_AND_IDENTIFIABILITY_GAPS_REMAIN`

## 결론

v1.0.16의 opt-in 수학은 맞다.
\(n(T)=n_0+n_1(T-T_\mathrm{ref})\),
\(w=n(T)RT/F\)이면
\[
\frac{\partial w}{\partial T}
=\frac{R}{F}\left[n(T)+Tn_1\right]
\]
이고, 새 `_dwdT`와 entropy config 항은 이 곱미분을 정확히
구현한다. \(n_1=0.004\ \mathrm{K^{-1}}\), \(x=0.2\) 독립 probe에서
해석식–code–유한차분 오차는
5.419e-16 V/K였다.

상수 \(n\)의 equilibrium/dQdV/entropy/reversible-heat 네 경로도
v1.0.15와 bit-exact다. `w`-only의 \(T\)-동결 폭과 중심값-only
entropy 경로도 맞다.

그러나 \(n(T)\)은 미시적 다중도 법칙이 아니다. 현재 근거로는
열적 \(RT/F\) 위에 남는 폭을 국소 선형식으로 흡수하는 empirical width law다.
선형 \(n(T)\)조차 실제 폭에는
\(w(T)=(R/F)[(n_0-n_1T_\mathrm{ref})T+n_1T^2]\)의 2차식을 만든다.
상분리, 입자분포, 수송 또는 관측 폭의 어느 기작인지 식별하지
않으므로 phase mechanism으로 승격할 수 없다.

## 확인된 구현 결함

`n`과 `w`가 모두 없는 공개 기본 경로는 `_n_factor=1`이라
폭이 실제로 \(RT/F\)인데 `_dwdT`는 이를 \(T\)-동결로 취급해 0을
반환한다. \(x=0.2\) 단일 전이에서 code entropy와 실제 고정-\(x\)
유한차분은 0.119455 mV/K 어긋난다. 기본 데이터셋은
명시적 `n=1`이라 영향받지 않지만 API와 문건의 “없으면 n=1” 계약은
불일치한다.

폭 양수 guard도 평가점 fail-fast일 뿐 fitting-domain bound가 아니다.
선형 \(n(T)\)은 사용할 전체 \([T_\min,T_\max]\)에서
\[
n_0+n_1(T_\min-T_\mathrm{ref})>0,\qquad
n_0+n_1(T_\max-T_\mathrm{ref})>0
\]
두 endpoint 제약을 가져야 한다. guide와 fitting schema에는 이
제약이 없다. 실제 probe는 \(T_\mathrm{ref}\)에서 양수라 생성되지만
273.15 K에서 음수가 되어 뒤늦게 예외를 냈다.

## 상관성과 검증 권위

한 온도에서는 관측되는 것이 \(n(T_k)\) 하나라 \(n_0,n_1\)의
Jacobian rank가 1이다. 278.15/288.15/298.15 K의 한쪽 20 K 창에서
dimensionless slope \(b=T_\mathrm{ref}n_1\)를 쓴 width Jacobian도
condition number 36.60,
parameter correlation 0.760다.
따라서 \(T_\mathrm{ref}\) 중심화, slope scaling, 양쪽 온도점,
profile likelihood/uncertainty가 필요하다.

v1.0.16 실행 원장은 n(T) round-trip을 주장하지만 배포된 test/demo
파일에는 `n_T1`과 `_dwdT` occurrence가 0이다. 기존 golden은 상수-n
불변만 검사한다. 이번 독립 probe가 수학을 확인했어도 release 당시
주장의 persistent regression authority는 없다.

비등온 배열 \(T(V)\)의 entropy 결과는 scalar pointwise 호출과
exact 일치했다. 다만 Step 37.2의 lag가 local T가 아니라 sample
mean \(T\)를 쓰는 blocker와 LCO의 \(T\)-의존 \(\Delta S_e\) 미분
blocker는 별개로 남는다.

## 문건 방향

Ch1/Ch2의 새 \(n(T)\) 유도 자체는 code 이름 없이 물리식으로
서술돼 theory-only body 방향에 맞는다. 최종 정본에서는 `n`을
“다중도”라는 미시적 명칭보다 `empirical width ratio`로 고정하고,
상수-n/상수-w/n(T)를 서로 배타적인 관측모델 후보로 둬야 한다.

## 다음 단계

Step 37.5에서 다온도 rate-series가 없을 때 \(n(T)\), activation,
LCO electronic/vibrational 항을 동시에 식별할 수 있는지 structural/
practical identifiability로 판정한다.

원본 `Claude/`, `main`은 수정하지 않았다.
