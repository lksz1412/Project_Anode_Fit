# Anode_Fit v1.0.10 P2 Draft C1 — Ch1 코드-교과서 supplement

## 0. 범위와 입력 검독

역할: Anode_Fit v1.0.10 P2 챕터1 9종 경쟁 드래프트 C1(Codex). 본 산출물은 supplement 초안이며, 원천 문건과 코드는 수정하지 않는다. 통합은 master 단계에서 수행한다.

목표: Ch1을 "코드 플로우차트를 충실히 설명하는 물리화학 교과서"로 정련하기 위해, 코드 step과 Ch1 본문 식의 coverage를 대조하고, 식-식 사슬이 끊기는 지점에 들어갈 교재형 브리지를 제안한다. LCO 양극 이론은 현재 코드 구현이 아니라 P4 코드 구현을 예고하는 Ch1 이론 확장으로 다룬다.

직접 읽은 입력:

| 입력 | 확인 범위 | 판정 |
|---|---:|---|
| `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` | 1-1866행 | 전문 검독 완료 |
| `Claude/results/process/V1010_P1_code-audit_RESULT.md` | 1-445행 | 전문 검독 완료. 중간 축약 의심 201-285행 재확인 |
| `Claude/results/research/broadening_w_design.md` | 1-44행 | 전문 검독 완료 |
| `Claude/results/research/radius/ORIGIN_VERDICT.md` | 1-79행 | 전문 검독 완료 |

비수행: 원천 `.tex`, 코드, 기존 P1 결과, 기존 ledger는 수정하지 않았다. 외부 문헌 원문 재검색은 수행하지 않았고, DOI·문헌 판단은 입력 문건에 기록된 근거와 tier를 따른다.

---

## 1. Ch1 ↔ 코드 1:1 coverage 매트릭스

### 1.1 노드 spine coverage

| 코드 step / 식별자 | 코드 ground truth(P1) | Ch1 설명 위치 | coverage | gap / supplement 판단 |
|---|---|---|---|---|
| N0 `curve`, `_direction_to_sigma`, `sigma_d`, `I_abs` | `curve` L483-508, `_direction_to_sigma` L510-524. `|I|=c_rate Q_cell` 또는 `I_abs` | `sec:notation`, `eq:n0map`; `tab:inputs`; `tab:nodemap` N0 | 충족 | 방향 부호의 작용처 셋(분극, 분기, 꼬리)은 Ch1에 있음. 다만 facade가 "새 물리 X"라는 P1 audit 문구는 Ch1 본문에 짧은 브리지로 더 선명히 넣으면 좋다. |
| N1 분극 `V_n=V_app-sigma_d I_abs Rn` | `dqdv` L408 | `sec:pol`, `eq:vapppol`, `eq:vnmid`, `eq:vn`; `tab:nodemap` N1 | 충족, 단 줄번호 보정 필요 | Ch1 `tab:nodemap`는 코드 위치를 `dqdv L412`로 적지만 P1 audit은 L408을 ground truth로 확정했다. 본문 식은 맞고 코드 줄 인용만 supplement/통합 단계에서 L408로 맞추면 된다. |
| N1 작업 격자 `V_work`, `T_work`, 배경 초기화 | `dqdv` L410-425, 배경 L427-429 | `sec:pol`, `eq:vwork`; `sec:sum`; `tab:inputs` | 충족 | `V_app`, `V_n`, `V_work`의 지위 구분은 좋다. `Cbg` callable 유한성 미검은 Ch1에 직접 드러나지 않는다. |
| N2 `func_U_j` | L78-79, `equilibrium` L360, `dqdv` L434 | `sec:center`, `eq:gibbsdef`, `eq:mudef`, `eq:eqbalance`, `eq:eqcond`, `eq:Ujmid`, `eq:Uj` | 충족 | 반응 엔탈피/엔트로피와 활성화 엔탈피/엔트로피 구분도 기호표에 있음. LCO 전자항처럼 `Delta S`가 T 의존일 때는 `dU/dT=Delta S/F` 적분형 브리지를 추가해야 한다. |
| N3 `func_dU_hys`, `func_U_branch` | `func_dU_hys` L133-140, `func_U_branch` L143-148, 호출 L447 | `sec:hys`, `eq:mu`, `eq:gxi`, `eq:gpp`, `eq:spinodal`, `eq:Veq`, `eq:dUhys`, `eq:Ubranch`, `eq:center` | 충족 | 활성 함수 coverage는 충분하다. 그러나 P1의 `func_U_j_hys` dead-code 판정은 Ch1 본문에 거의 없다. 독자가 코드 전체를 따라가려면 "보존된 원형 dead helper와 활성 helper의 차이" 박스가 필요하다. |
| N4 `_n_factor`, `func_w`, `_width` | `func_w` L74-75, `_n_factor` L272-278, `_width` L281-284 | `sec:width`, `eq:wbase`; `sec:broadening`; `tab:inputs`; `tab:nodemap` N4 | 부분 충족 | Ch1은 `w` 이중지위를 잘 설명한다. 추가로 P1 확정인 키 우선순위, 즉 `n`이 있으면 `w` 폴백이 inert라는 코드 동작을 더 눈에 띄게 연결해야 한다. |
| N5 `func_ksi_eq` | L94-97, `dqdv` L455, `equilibrium` L365 | `sec:width`, `eq:bv`, `eq:db`, `eq:logisticsolve`, `eq:xieq`; `sec:dist`, `eq:partfn`, `eq:fermifn` | 충족 | kinetic detailed balance, grand-canonical 분포 관점, 부호 검산이 모두 있음. |
| N5+ LCO electronic entropy | 코드에는 없음(P1 `grep LCO|...` No matches) | `sec:lco-electronic`, `eq:fd`, `eq:Se`, `eq:dSe`, `eq:dSemolar`, `eq:ggate`, `eq:dSegate` | 이론만 충족 | Ch1에는 이론 plug-in으로 존재하지만 v1.0.10 코드에는 없다. supplement와 통합문은 "코드 구현=P4"를 명시해야 허위 coverage가 아니다. |
| N6 `equilibrium` 평형 peak | `equilibrium` L350-367, `dqdv` 평형 분기 L462-464 | `sec:eqpeak`, `eq:belliden`, `eq:eqpeak`; `sec:lco-peak` | 충족, 단 브리지 필요 | Ch1은 peak 식을 잘 유도한다. P1 확정인 `equilibrium`의 T 스칼라 전용, 히스/동역학 미반영, `dqdv`와의 차이를 본문 박스로 보강하면 코드 독해성이 올라간다. |
| N6 broadening / 현상학적 `w` | 모델 항 0, 설명 only | `sec:broadening`, `eq:ensavg`, `fig:broadening`; broadening design 1-44행 | 충족 | Ch1 v10은 broadening 설명을 잘 복원했다. 단 `ORIGIN_VERDICT`와 `broadening_w_design` 사이에 "크기 kinetic 분산" 포함 여부가 충돌한다. 최종 Ch1 범위는 사용자 결정 baked에 따라 size/PSD 기계장치 제외, 비-크기 apparent-U/eta 분포 설명 only가 맞다. |
| N7 `_resolve_lag_length`, `func_L_q`, `func_dH_a_eff`, `func_chi_d` | `_resolve_lag_length` L303-347, `func_L_q` L100-107, `func_dH_a_eff` L152-155, `func_chi_d` L158-163 | `sec:lag`, `eq:Lq`, `eq:kuniv`, `eq:Acut`, `eq:chid`, `eq:dHeff`, `eq:Lqfull`, `eq:LV` | 충족 | 직접 `L_V` 지정 우선, `dH_a` 없음/`I<=0`이면 off, `dVdq_qa` 누락 silent off는 Ch1의 교과서 설명보다 P1 audit에 더 선명하다. 브리지 필요. |
| N8 `_causal_lowpass`, branch, reversal | `_causal_lowpass` L110-128, dqdv L462-475 | `sec:tail`, `eq:memory`, `eq:lowpass`, `eq:peakshape`, `eq:branch`, `eq:reversal` | 충족 | Ch1은 D-PEAK 극한을 정확히 고쳤다. P1 보완 3인 `n_work=max(n_work_min,V_n.size*2)`에 따른 해상도 의존 문턱은 추가 bridge로 적는 것이 좋다. |
| N9 `dqdv_work += Q peak_shape`, `np.interp` | dqdv L477, L479-480 | `sec:sum`, `eq:sum`, `tab:staging`, `tab:inputs`, `tab:nodemap` | 충족 | 합산식은 충분하다. `Cbg` 유한성은 코드가 검증하지 않는 fitting-wrapper 책임임을 P1 audit대로 supplement에 둔다. |

### 1.2 24심볼 coverage

| # | 심볼 | Ch1 앵커 | 판정 |
|---:|---|---|---|
| 1 | `func_w` | `eq:wbase`, `tab:nodemap` N4 | 충족 |
| 2 | `func_U_j` | `eq:Uj` | 충족 |
| 3 | `func_U_j_hys` | 직접 앵커 약함 | 누락. 보존 dead helper라는 코드 사실을 bridge로 추가 필요 |
| 4 | `func_ksi_eq` | `eq:xieq`, `eq:fermifn` | 충족 |
| 5 | `func_L_q` | `eq:Lqfull` | 충족 |
| 6 | `_causal_lowpass` | `eq:lowpass`, `eq:reversal` | 충족 |
| 7 | `func_dU_hys` | `eq:dUhys` | 충족 |
| 8 | `func_U_branch` | `eq:Ubranch`, `eq:center` | 충족 |
| 9 | `func_dH_a_eff` | `eq:dHeff` | 충족 |
| 10 | `func_chi_d` | `eq:chid` | 충족 |
| 11 | `_finite`, `_finite_pos`, `_finite_nonneg` | 없음 | 부분 누락. 수식 교과서에는 불필요하나 코드 플로우차트 supplement에는 fail-fast guard 표가 필요 |
| 12 | `__init__` | `tab:inputs` | 부분 충족. guard, seed, transitions reference semantics는 Ch1에 없음 |
| 13 | `_build_seed_L_V` | 없음 | 누락. 진단용 seed이며 dqdv 미사용이라는 bridge 필요 |
| 14 | `_n_factor` | `eq:wbase` 주변 설명 | 부분 충족. `n` 우선으로 `w` inert 되는 코드 사실 보강 필요 |
| 15 | `_width` | `eq:wbase` | 충족 |
| 16 | `_chi_d` | `eq:chid` | 충족 |
| 17 | `_chi_and_dH_eff` | `eq:chid`, `eq:dHeff` | 부분 충족. helper 응집 구조는 Ch1에 없음 |
| 18 | `_resolve_lag_length` | `eq:Acut`-`eq:LV` | 충족, 단 우선순위/silent-off bridge 필요 |
| 19 | `equilibrium` | `eq:eqpeak` | 부분 충족. T 스칼라 전용, 히스 미반영 bridge 필요 |
| 20 | `dqdv` | N1-N9 전체 | 충족 |
| 21 | `curve` | `eq:n0map`, facade 설명 | 충족 |
| 22 | `_direction_to_sigma` | `eq:n0map` | 충족 |
| 23 | `GRAPHITE_STAGING_LIT` | `tab:staging` | 충족 |
| 24 | `__main__` self-test | `sec:signcheck` verifybox | 부분 충족. Ch1은 회귀 수치 검산을 적지만, 코드 self-test의 면적=Q assert 부재는 P1 audit에만 있음 |

### 1.3 피팅 파라미터 coverage

| 파라미터 | 코드 지배영역(P1) | Ch1 앵커 | coverage / 보강 |
|---|---|---|---|
| `U_j` 또는 `dH_rxn,dS_rxn` | peak 위치, 온도 이동 | `eq:Uj`, `tab:staging`, `tab:inputs` | 충족 |
| `n_j` / `w` | peak 폭 | `eq:wbase`, `sec:broadening` | 이중지위 충족. `n` 우선으로 `w` 폴백 inert 되는 코드 동작 보강 |
| `Q_j` | 면적/높이 | `eq:eqpeak`, `eq:sum`, `tab:staging` | 충족 |
| `Omega_j` | 히스 gap, `dH_a_eff` | `eq:dUhys`, `eq:dHeff` | 충족 |
| `gamma_j` | 히스 split | `eq:Ubranch`, `eq:center` | 충족 |
| `h_eta` | 부분 cycle 분기 | `eq:Ubranch`, `eq:center`, `tab:inputs` | 충족 |
| `dH_a,dS_a` | 꼬리 길이, T 의존 | `eq:Lqfull` | 충족 |
| `chi` / `chi_split` | 충방전 꼬리 비대칭 | `eq:chid`, `eq:dHeff` | 충족. 피팅 bound `[0,1]` 보강 |
| `L_V` 직접 | 동역학 우회 | `tab:inputs` | 부분 충족. direct override가 후속 물리 파라미터를 모두 우회함을 명시 |
| `dVdq_qa` | `L_q -> L_V` 환산 | `eq:LV` | 충족. 누락 시 silent off 보강 |
| `z_cut`, `A_cap_RT` | 컷 affinity | `eq:Acut` | 충족. z_cut docstring 부정확은 코드 docstring 문제로 별도 bridge |
| `use_dH_eff` | Ω-동역학 결합 토글 | `eq:dHeff`, `tab:inputs` | 충족 |
| `Rn` | IR shift | `eq:vn` | 충족 |
| `Cbg` | baseline | `eq:sum`, `tab:inputs` | 충족. callable 유한성 미검 보강 |
| grid controls | 수치 격자/branch | `eq:vwork`, `eq:branch`, `tab:inputs` | 충족. 해상도 의존 branch 보강 |
| seed controls | 진단용 seed | `tab:inputs` | 부분 충족. dqdv 미사용 명시 필요 |

---

## 2. 누락 유도·브리지 보완 초안

아래 문단들은 Ch1 본문에 그대로 넣을 수 있는 교재형 bridge 초안이다. 위치는 제안이며, 통합 단계에서 문체와 식 번호를 맞추면 된다.

### Bridge A — 보존 dead helper와 활성 히스 helper 분리

삽입 위치 제안: `sec:hys`의 `eq:Ubranch` 뒤 또는 `tab:nodemap` 앞.

> 코드에는 히스테리시스 분기 중심을 계산하는 이름이 두 개 보인다. 첫째 `func_U_j_hys(T,U_j,Omega,gamma,s,last_eta,last_rest)`는 원형 보존용 helper이고, 현재 `dqdv` 경로에서는 호출되지 않는다. 이 함수 안의 `last_eta`, `last_rest`, 지역 `partial_hys=1.0`도 현재 forward 곡선에는 영향을 주지 않는다. 둘째 `func_U_branch(T,U_j,Omega,gamma,sigma_d,h_eta)`가 실제 활성 helper이며, `dqdv`는 이 함수를 `U_j=0`으로 호출해 방향별 shift만 구한 뒤 배열 중심 `U_j(T)`에 더한다. 따라서 본 장의 물리식은 `eq:dUhys`와 `eq:Ubranch`가 정본이고, `func_U_j_hys`는 코드 역사적 보존 항목이지 별도 물리 경로가 아니다. 외부 사용자가 `func_U_j_hys`를 직접 호출하면 기본 `s=+1` 때문에 방전 분기로 해석되므로, Ch1의 코드 flow를 재현할 때는 활성 경로 `func_U_branch`를 기준으로 삼아야 한다.

검산: dead helper를 본문 물리로 끌어오면 `h_eta` 노출, 부분 cycle, 호출자 줄 근거가 모두 어긋난다. 활성 경로만 쓰면 `U_j^d=U_j+0.5 sigma_d h_eta gamma Delta U_hys`와 self-test의 `dis-chg = gamma Delta U_hys`가 일치한다.

### Bridge B — `equilibrium`과 `dqdv`는 같은 peak 식을 공유하지만 같은 곡선이 아니다

삽입 위치 제안: `sec:eqpeak` 끝 또는 `facade 와 전체 진행 한눈에` 앞.

> `equilibrium(V_n,T)`는 `|I| -> 0` 기준선을 빠르게 그리는 보조 메서드다. 이 메서드는 `U_j(T) -> w_j -> xi_eq -> Q_j xi_eq(1-xi_eq)/w_j`만 합산한다. 히스테리시스 분기 중심 `U_j^d`, 지연 길이 `L_V`, 충전 격자 역전은 들어가지 않는다. 따라서 "방향 불변"은 평형 peak 모양에 대한 말이지, `dqdv` 전체가 방향 불변이라는 뜻이 아니다. `dqdv`는 `sigma_d`가 분극, 분기 중심, `chi_d/Delta H_a_eff`, 격자 역전 네 곳에 들어가므로 방향 의존이다. 또한 현재 `equilibrium`은 `T`를 스칼라로 검증하는 보조 경로이고, 배열 `T(V)` 비등온 보간은 `dqdv`에만 있다. 결론적으로 `equilibrium`은 `dqdv`의 작은 지연 분기에서 쓰는 평형 peak 형상과 같은 식을 공유하지만, 코드 흐름 전체의 축약판은 아니다.

식 사슬:

```text
equilibrium:
V_n, T_scalar -> U_j(T) -> w_j -> xi_eq(V_n) -> C_bg + sum Q_j xi(1-xi)/w

dqdv:
V_app, T(V), I, Q_cell, sigma_d
-> V_n -> V_work,T_work
-> U_j(T_work) -> U_j^d(T_rep,sigma_d)
-> xi_eq(V_work,U_j^d)
-> L_V(T_rep,I,Q_cell,chi_d,Delta H_a_eff)
-> branch(eq peak or causal tail)
-> C_bg + sum Q_j peak_shape
-> interp back to V_n
```

이 bridge는 P1의 정정 1을 Ch1 독자 언어로 풀어쓴 것이다.

### Bridge C — `n` 우선순위와 `w`의 이중지위

삽입 위치 제안: `sec:width`의 폭 이중지위 문단 뒤.

> 코드에서 폭은 항상 `w_j=n_jRT/F`로 평가된다. 전이 dict가 `n`을 직접 가지면 그 값이 최우선이며, `w` 키가 함께 있어도 `w`는 읽히지 않는다. `w`는 `n`이 없을 때만 `n=wF/(RT)`로 역산되는 폴백이다. 현재 `GRAPHITE_STAGING_LIT`는 네 전이 모두 `n=1.0`을 가지므로, 표에 함께 남아 있는 `w=0.020/0.016/0.014/0.012 V` 값은 출발 상태에서는 inert이다. 따라서 현재 기본 곡선의 실평가 폭은 전 전이에서 `RT/F ~= 25.7 mV`이고, 더 작은 `w` 폴백은 `n`을 제거하거나 피팅 wrapper가 `n`을 다른 값으로 명시할 때만 활성화된다.

> 이 코드 우선순위와 물리적 이중지위는 서로 다른 말이다. 코드 우선순위는 "어느 키가 계산에 쓰이는가"이고, 물리적 이중지위는 "계산된 폭을 평형 예측으로 읽을지, broadening을 흡수한 현상학적 피팅폭으로 읽을지"이다. 단상 전이는 `w=nRT/F`를 평형 등온선 폭으로 읽고, 두-상 전이는 같은 계산값을 실측 broadening의 현상학적 폭으로 읽는다.

적대 검산:

```text
T = 298.15 K, n = 1
w = RT/F = 8.314*298.15/96485 = 0.02569 V
```

이는 현재 기본 staging 출발점의 실제 코드 폭이다. 표의 `w=0.012 V`를 곧바로 코드 폭으로 읽으면 `n` 우선순위와 충돌한다.

### Bridge D — 지연 길이 resolver의 우선순위와 silent-off 조건

삽입 위치 제안: `sec:lag`의 codebox 뒤.

> `L_V`는 물리식 한 줄만으로 결정되는 값이 아니라 resolver의 우선순위를 따른다. 첫째, 전이 dict에 `L_V`가 직접 지정되어 있으면 코드가 그 값을 즉시 반환한다. 이 경우 `dH_a`, `dS_a`, `Omega`, `chi`, `z_cut`, `A_cap_RT`, `dVdq_qa`는 꼬리 길이 계산에 반영되지 않는다. 직접 `L_V`는 초벌 피팅에는 안정적이지만, 물리 파라미터 fit으로 넘어갈 때 제거해야 한다. 둘째, `I<=0`이거나 `dH_a`가 없으면 `L_V=0`으로 떨어져 평형 peak 분기가 쓰인다. 셋째, 동역학 경로가 켜졌더라도 `dVdq_qa`가 없으면 기본 `0`이 곱해져 `L_V=0`이 된다. 이 경우 `dH_a`가 있어도 꼬리가 조용히 사라지므로, fitting schema에서는 동역학 전이에 `dVdq_qa>0`을 필수로 두어야 한다.

교재형 flow:

```text
if 'L_V' in transition:
    L_V = transition['L_V']              # direct kinetic length, physics chain bypass
elif I <= 0 or 'dH_a' not in transition:
    L_V = 0                              # equilibrium branch
else:
    A = min(z_cut*abs(n_j)*RT, A_cap_RT*RT)
    chi_d = chi_split(chi, sigma_d)
    Delta H_a_use = Delta H_a - chi_d Omega  # only if use_dH_eff
    L_q = func_L_q(T, I, Q_cell, Delta H_a_use, Delta S_a, chi_d, A)
    L_V = abs(dVdq_qa) * L_q
```

부호·차원:

```text
A: J/mol
Delta H_a_use - T Delta S_a: J/mol
L_q: dimensionless capacity-coordinate length
abs(dVdq_qa): V
L_V: V
```

극한:

```text
I -> 0  => T_* = I h/(Q_cell k_B) -> 0 => L_q -> 0 => L_V -> 0
L_V < min_lag_grid_steps * Delta_grid => equilibrium branch
```

### Bridge E — branch threshold의 해상도 의존성

삽입 위치 제안: `sec:tail`, `eq:branch` 설명 뒤.

> `eq:branch`의 문턱은 물리 상수만으로 정해지지 않고, 작업 격자 해상도에 의존한다. 코드는 `n_work=max(n_work_min, 2*len(V_n))`로 작업 격자 점 수를 정하고, `Delta_grid=(V_work[1]-V_work[0])`를 얻은 뒤 `L_V < min_lag_grid_steps * Delta_grid`이면 평형 peak로 접는다. 따라서 같은 물리 `L_V`라도 사용자가 넣은 `V_app` 점 수와 전압 span이 바뀌면 `Delta_grid`가 바뀌고, 꼬리 분기와 평형 분기의 경계가 이동한다. 이것은 물리 모델의 새 효과가 아니라 sub-grid 지연을 꼬리식으로 나누어 생기는 `0/0` 불안정을 피하기 위한 수치적 mode switch다.

검산 문장:

```text
V point 수 증가 -> n_work 증가 -> Delta_grid 감소
=> 같은 L_V가 더 쉽게 L_V >= 2 Delta_grid 조건을 만족
=> 꼬리 branch가 켜질 수 있음
```

피팅 문건에는 같은 데이터셋을 비교할 때 `V_app` resampling과 `n_work_min`을 고정해야 한다는 운영 가드를 붙이는 것이 좋다.

### Bridge F — 입력 guard와 fitting wrapper 책임

삽입 위치 제안: `tab:inputs` 뒤.

> Ch1의 수식은 물리량의 정의역을 전제로 하지만, optimizer는 그 정의역 밖도 탐색한다. 코드 내부 guard는 일부만 막는다. `T`, `Q_cell`, 생성자 스칼라는 유한성/양수성을 검사하지만, 전이별 `n`은 양수 bound가 없고, `chi`는 유한성만 보며 `[0,1]` 범위는 강제하지 않고, callable `Cbg(V)`의 반환값 유한성도 검사하지 않는다. 따라서 피팅 wrapper의 최소 bound는 `n>0`, `0<=chi<=1`, 동역학 전이의 `dVdq_qa>0`, `Cbg(V)` 유한성이다. 이는 물리식을 바꾸는 방어 로직이 아니라, 식의 정의역을 optimizer에 전달하는 schema 조건이다.

수식 근거:

```text
n <= 0     -> w=nRT/F <= 0; logistic 폭과 Q xi(1-xi)/w가 무의미
chi<0 or >1 -> barrier split이 transition-state fraction 해석을 잃음
dVdq_qa=0 -> L_V=0; dH_a가 있어도 tail silent off
Cbg=NaN/inf -> sum 전체 오염
```

### Bridge G — broadening은 설명이고 코드 차원 증가는 아니다

삽입 위치 제안: `sec:broadening` 끝 keybox 또는 `tab:nodemap` N6 보강행.

> `eq:ensavg`는 현재 v1.0.10 코드가 새 적분층을 가진다는 뜻이 아니다. 현재 코드는 단일 유효 입자 응답에 `w_j`와 `L_V`를 주어 곡선을 만든다. `eq:ensavg`는 두-상 전이의 실측 폭을 해석하는 forward 통계 평균 설명이며, 그 폭의 효과는 현상학적 `w_j`에 흡수된다. 측정 dQ/dV에서 `rho(U_app)`를 역산하지 않고, PSD 또는 입자 반경 분포 convolution도 만들지 않는다. 따라서 coverage 표의 N6 보강행은 "모델 항 0, 설명 only"로 읽어야 한다.

`broadening_w_design.md` 기준 최종 scope:

```text
복원: 델타 vs 실측 종, w=현상학적 피팅 폭 설명
유지: forward-only ensemble average 설명
금지: radius/PSD 기계장치, dQ/dV -> rho 역산, w_eff
```

`ORIGIN_VERDICT.md`에는 크기 kinetic 분산이 강한 지지로 정리되어 있으나, P2 Ch1 v10 통합 명세는 사용자 결정 baked에 의해 사이즈/PSD 모델을 제외한다. 그러므로 supplement에서는 크기 kinetic 분산을 "물리적으로 가능한 후속 확장 후보"로만 분리하고, 현 Ch1 본문에는 비-크기 `eta` heterogeneity와 현상학적 `w` 흡수로 제한해야 한다.

---

## 3. LCO 이론 정련안

### 3.1 현 상태 판정

확정:

1. v1.0.10 코드 ground truth는 흑연 음극 전용이다. P1 audit의 grep 결과에서 `LCO`, `q_rev`, `dS_e`, `cathode`, `발열`, `전자엔트로피`가 코드에 없다고 확정했다.
2. Ch1 문건은 LCO를 이론 확장으로 이미 포함한다. 핵심 앵커는 `tab:lco-staging`, `eq:lco-dUdT`, `sec:lco-electronic`, `eq:Se`, `eq:dSe`, `eq:dSemolar`, `eq:ggate`, `eq:dSegate`, `eq:lco-decomp`, `eq:msmr`이다.
3. 따라서 "Ch1 이론 정련"과 "코드 구현"은 분리해야 한다. P2는 교과서 이론 기술이고, LCO 코드 구현은 P4 예고로 명기한다.

근거 미발견:

1. 입력 파일만 기준으로는 LCO `g(E_F,x)` 연속 곡선의 1차 문헌 실측값이 없다. Ch1도 이를 갭 G2로 두고 MIT-logistic gate를 모델 가정으로 둔다.
2. 도핑에 따른 `x_MIT`, `Delta x_MIT`, `g_max` shift 정량식은 입력 파일 기준 근거 미발견이다. 피팅 대상 초기값으로만 둔다.

### 3.2 LCO dQ/dV 교재형 사슬

LCO 하프셀 dQ/dV도 Ch1 spine과 같은 수학 구조를 쓴다. 전극이 바뀌어도 "전이별 logistic + 용량 가중 합산"은 유지되고, 값과 엔트로피 분해만 바뀐다.

교재형 사슬:

```text
LCO transition list:
T1 MIT around 3.90 V
T2 order-disorder around 4.05 V
T3 order-disorder around 4.17-4.20 V

For each transition j:
U_j(T) is determined by reaction Gibbs free energy.
dU_j/dT = Delta S_rxn,j^cat / F.
xi_eq,j = 1 / (1 + exp[-sigma_d(V-U_j^d)/w_j]).
(dQ/dV)_j = Q_j xi_eq,j(1-xi_eq,j)/w_j, or tail branch if finite-rate lag is active.
dQ/dV = C_bg + sum_j Q_j peak_shape_j.
```

LCO 특수성:

```text
Delta S_rxn,j^cat = Delta S_config,j + Delta S_vib,j + Delta S_e,j^mol(x,T)
```

흑연과 같은 항:

```text
Delta S_config: Li/vacancy arrangement
Delta S_vib: lattice vibration baseline
Omega/gamma: order-disorder or MIT two-phase hysteresis
w_j: two-phase broadening phenomenological fitting width
```

LCO에만 켜지는 항:

```text
Delta S_e: electronic entropy from insulator-metal transition near T1
```

### 3.3 Sommerfeld 전자 엔트로피 정련

Ch1의 `eq:Se`는 표준 금속 전자기체의 저온 Sommerfeld 결과다.

자리당 상태밀도 `g(E_F,x)`를 쓰면:

```text
f(E) = 1 / (1 + exp[(E-E_F)/(k_B T)])
S_e(T,x) = (pi^2/3) k_B^2 T g(E_F,x)
```

반응 엔트로피 슬롯에 넣어야 하는 것은 전자 엔트로피 자체가 아니라 삽입 반응 1몰당 변화량이다. 삽입 기준에서:

```text
Delta S_e,j(x,T) = (partial S_e / partial x)_T
                 = (pi^2/3) k_B^2 T (partial g(E_F,x)/partial x)
```

몰당 환산:

```text
Delta S_e,j^mol(x,T)
  = N_A Delta S_e,j(x,T)
  = (pi^2/3) R k_B T (partial g(E_F,x)/partial x)
```

단위 주의:

```text
if g is in states/eV/atom:
    partial g / partial x has unit 1/eV/atom
    convert eV to J before inserting into J/(mol K)
```

부호:

```text
LCO delithiation: x decreases, insulator -> metal, g(E_F) increases.
Insertion direction: x increases, metal -> insulator, g(E_F) decreases.
Therefore partial g/partial x < 0 near MIT, so Delta S_e^mol < 0 in insertion convention.
```

이 부호는 Ch1의 `Delta S_rxn` 슬롯과 일관된다. 탈리튬화 관측에서는 전자 엔트로피 방출량의 절댓값이 양의 bump로 보이지만, forward 반응 엔트로피 슬롯에는 삽입 기준 음수로 들어간다.

### 3.4 MIT-logistic gate의 지위

Ch1의 `eq:ggate`는 1차 문헌에서 연속 `g(E_F,x)` 곡선이 없다는 갭을 메우는 모델 가정이다.

```text
g(E_F,x) ~= g_max [1 - sigma((x-x_MIT)/Delta x_MIT)]
```

초기값:

```text
g_max ~= 13 e/eV/atom
x_MIT ~= 0.85
Delta x_MIT ~= 0.05
```

식별 지위:

| 구성요소 | 지위 |
|---|---|
| Sommerfeld 함수형 `S_e=(pi^2/3)k_B^2 T g(E_F)` | 교과서 표준 함수형. Ch1 tier A |
| `g_max` anchor | 입력 문건 기준 Motohashi 단일점 anchor. 그 점에서만 강함 |
| `g(E_F,x)` 연속 곡선 | 1차 문헌 근거 미발견. logistic gate는 fitting model assumption |
| `x_MIT`, `Delta x_MIT` | 초기값. 실제 시료/도핑에서 피팅 대상 |

LCO supplement에 필요한 명시 문장:

> MIT-logistic gate는 "전자항이 반드시 logistic이어야 한다"는 문헌 확정이 아니라, 절연체에서 금속으로 전자 상태밀도가 유한 폭으로 켜진다는 물리와 Ch1의 logistic 언어를 결합한 최소 smooth parameterization이다. 함수형은 데이터 fitting 전의 초기 모델이며, P4 구현에서는 이 세 값을 노출해야 한다.

### 3.5 `Delta S(T)`가 T 의존일 때의 열역학 bridge

Ch1의 기본식:

```text
U_j(T)=(-Delta H_rxn + T Delta S_rxn)/F
```

은 `Delta H_rxn`, `Delta S_rxn`을 해당 온도 창에서 상수로 둘 때의 닫힌형이다. LCO 전자항은 `Delta S_e^mol(x,T) proportional T`이므로, 엄밀한 교재형 설명에서는 미분형을 먼저 둔다.

```text
dU_j/dT = Delta S_rxn,j(T) / F
```

따라서 기준온도 `T0`에서의 중심 `U_j(T0)`를 anchor로 잡으면:

```text
U_j(T) = U_j(T0) + (1/F) int_{T0}^{T} Delta S_rxn,j(T') dT'
```

config와 vib를 상수 `Delta S_0`로 두고, electronic을 `Delta S_e(T)=aT`로 두면:

```text
U_j(T) = U_j(T0)
       + (Delta S_0/F)(T-T0)
       + (a/(2F))(T^2-T0^2)
```

이 bridge가 없으면 "전자항은 `Delta S_e proportional T`"와 "U는 `T Delta S`"를 단순 곱으로 섞어 `T^2` 계수의 1/2를 잃을 위험이 있다. Ch1은 이미 "전자 기여의 `partial U/partial T`가 T에 선형이고 U 이동은 `propto T^2`"라고 적고 있으므로, 통합본에는 위 적분형을 박스로 추가하는 것이 안정적이다.

### 3.6 P4 구현 예고

P4에서 필요한 최소 구현 경계:

1. `LCO_STAGING_LIT` 또는 전이 dict를 별도 제공한다. 키 구조는 graphite와 동일하게 둔다.
2. T1 전이에만 electronic entropy plug-in을 켠다.
3. `dS_rxn`을 상수 스칼라로만 읽는 현재 `func_U_j(T,dH_rxn,dS_rxn)` 경로와, `Delta S_rxn(T,x)` callable 또는 precomputed array 경로를 분리한다.
4. 몰당 환산과 eV-to-J 변환을 강제한다.
5. `x` 또는 SOC mapping이 필요하다. 현재 dQ/dV 호출은 전압 격자 기반이므로, LCO electronic gate의 `x`를 어떻게 얻을지 별도 상태 변수 또는 전이 진행률 mapping을 설계해야 한다.
6. P4 전까지 Ch1은 이론 plug-in과 구현 예고만 적고, v1.0.10 코드 coverage로 보고하지 않는다.

---

## 4. 부호·차원·극한 적대 검산

| 항목 | 검산 | 판정 |
|---|---|---|
| 분극 | 방전 `sigma_d=+1`: `V_n=V_app-|I|Rn < V_app`; 충전 반대 | PASS |
| `U_j` | `(-Delta H + T Delta S)/F`: J/mol divided by C/mol = V | PASS |
| logistic | `(V-U)/w` 무차원, `xi in (0,1)` | PASS |
| peak | `Q xi(1-xi)/w`: C/V | PASS |
| hys gap | `Omega`, `RT`는 J/mol, `/F`로 V; `Omega<=2RT -> 0` | PASS |
| branch | `U_dis-U_chg = gamma h_eta Delta U_hys > 0` | PASS |
| `Acut` | `z_cut nRT`, `A_cap RT` 모두 J/mol; 방향 부호 미포함 | PASS |
| `L_q` | `T_*/T`, exponent terms 무차원; `L_q` dimensionless | PASS |
| `L_V` | `abs(dVdq_qa)` V times `L_q` dimensionless = V | PASS |
| tail branch | `L_V<nu Delta_grid`는 V<V 비교 | PASS |
| LCO `Delta S_e^mol` | `R k_B T (partial g/partial x)` with eV-to-J conversion -> J/(mol K) | 조건부 PASS. 구현 시 단위 변환 guard 필요 |
| LCO T dependence | `dU/dT=Delta S(T)/F`; `Delta S_e=aT`이면 `U` 이동은 `a(T^2-T0^2)/(2F)` | PASS, Ch1 bridge 권고 |

---

## 5. 추가 후보

실제 수정하지 않았다. 통합 master가 선택할 후보만 남긴다.

| 후보 | 위치 | 이유 | 변경 종류 |
|---|---|---|---|
| `tab:nodemap` N1 코드 줄 `L412` -> `L408` | Ch1 `tab:nodemap` | P1 audit ground truth와 줄 번호 불일치 | 문서 줄근거 갱신 |
| dead helper bridge 추가 | `sec:hys` | 24심볼 coverage에서 `func_U_j_hys` 누락 | 문서 보강 |
| `equilibrium` vs `dqdv` bridge 추가 | `sec:eqpeak` 또는 facade 절 | 방향 불변·히스 잔존·T 스칼라 전용 혼동 방지 | 문서 보강 |
| `n` 우선 / `w` inert bridge 추가 | `sec:width` | 현재 기본 폭이 `RT/F`임을 코드와 직접 연결 | 문서 보강 |
| lag resolver priority bridge 추가 | `sec:lag` | direct `L_V`, silent off, fitting schema를 코드 flowchart로 연결 | 문서 보강 |
| branch 해상도 의존 bridge 추가 | `sec:tail` | 입력 V 점수에 따라 branch 문턱이 바뀌는 코드 동작 설명 | 문서 보강 |
| fitting wrapper bounds 박스 추가 | `tab:inputs` 뒤 | `n>0`, `chi in [0,1]`, `dVdq_qa>0`, `Cbg` finite | 문서 보강 |
| LCO T-dependent entropy 적분형 추가 | `sec:lco-electronic` 또는 `sec:lco-decomp` | `Delta S_e proportional T`와 `U(T)` 이동의 `1/2` 계수 명확화 | 문서 보강 |
| P4 구현 경계 문장 추가 | LCO 코드 일반화 절 | 현재 코드에는 LCO가 없으므로 허위 coverage 방지 | 문서 보강 |

---

## 6. 결론

확정: Ch1 v1.0.10은 N0-N9 spine의 주요 물리식 대부분을 코드와 1:1로 설명한다. 특히 `eq:vn`, `eq:Uj`, `eq:dUhys`, `eq:Ubranch`, `eq:wbase`, `eq:xieq`, `eq:eqpeak`, `eq:Acut`-`eq:LV`, `eq:peakshape`, `eq:reversal`, `eq:sum`은 P1 audit의 12 closed-form 식과 대응한다.

미결: 코드 전체를 교과서처럼 따라가려면 활성 물리식 바깥의 코드 운영부, 즉 dead helper, guard, key priority, direct `L_V` override, silent-off, branch 해상도 의존, fitting wrapper 책임을 bridge로 보강해야 한다.

근거 미발견: LCO `g(E_F,x)`의 연속 실측 곡선, 도핑별 MIT gate 정량식, 현재 v1.0.10 코드의 LCO 구현 근거는 입력 파일 기준 없다.

권고: master 통합본은 Ch1 본문을 크게 갈아엎기보다, 위 Bridge A-G와 LCO T-dependent entropy 적분형을 삽입해 "코드 flowchart를 충실히 설명하는 교과서" 성격을 완성하는 편이 안전하다.
