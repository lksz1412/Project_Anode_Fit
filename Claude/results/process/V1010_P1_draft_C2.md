# V1010 P1 Draft C2 — Graphite dQ/dV Code Analysis

## 0. 작업 범위와 근거

- 지시 파일: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p1_codex_C2.txt` 전문 확인.
- 대상 코드: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` 1-702행 전문 정독. 지시문에는 695줄이라고 되어 있으나 실제 파일은 702행이다.
- 독립 작성: 같은 폴더의 다른 `V1010_P1_draft_*.md`는 읽지 않았다.
- 실행 근거:
  - `python Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` → `overall OK: True`.
  - `rg -n "LCO|q_rev|dS_e|electron|entropy|전자|양극|cathode|heat|rev"` → 코드 식별자/본문에서 양극, 발열, 전자엔트로피 계층 구현 근거 없음. 단 `entropy`는 검색어였지만 실제 출력은 tail demo 문자열 1건뿐이었다.
  - 별도 수치 검산: 평형 면적, 직접 `L_V` 꼬리 면적, `n/w` 0·음수 edge case 확인.

## 1. 플로우차트 맵

### 1.1 전체 데이터 흐름

```text
생성자 입력
  transitions / GRAPHITE_STAGING_LIT
  x, Rn, Cbg, chi, chi_split, use_dH_eff
  z_cut, A_cap_RT, grid_pad_lo/hi, n_work_min, min_lag_grid_steps, v_span_floor
  seed_T, seed_I, seed_Q_cell
    |
    v
__init__ 가드 및 저장
  _finite/_finite_pos/_finite_nonneg
  seed_L_V = _build_seed_L_V(...)
    |
    +--> equilibrium(V_n,T)
    |      Cbg(V) + Σ_j Q_j * ξ_j(1-ξ_j) / w_j
    |
    +--> dqdv(V_app,T,I_abs,Q_cell,s)
    |      V_n = V_app - σ_d |I| R_n
    |      U_j(T) 또는 U_j 상수
    |      U_j^d = U_j + 0.5 σ_d h_eta gamma ΔU_hys
    |      ξ_eq = logistic[σ_d(V_n-U_j^d)/w_j]
    |      L_V = override 또는 |dV/dq|_qa * L_q
    |      sub-grid: Q_j ξ(1-ξ)/w
    |      finite lag: Q_j(ξ - lowpass_directional(ξ))/L_V
    |      interp back to V_n
    |
    +--> curve(V_app,direction,c_rate,Q_cell,T,I_abs)
           direction -> σ_d
           I_abs 없으면 |I| = c_rate * Q_cell
           dqdv(...) 재사용
```

### 1.2 입력과 초기 데이터

- 클래스 생성자 인자는 `transitions`, `x`, `Rn`, `Cbg`, `chi`, `chi_split`, `use_dH_eff`, `z_cut`, `A_cap_RT`, 격자/seed 인자를 받는다(221-231행). 문서 문자열은 transition 키로 `U | (dH_rxn,dS_rxn)`, `w | n`, `Q`, `Omega`, `gamma`, `dH_a`, `dS_a`, `dVdq_qa`, `h_eta`, `L_V`를 명시한다(198-219행).
- 생성자는 `x`, `Rn`, `chi`, `z_cut`, `A_cap_RT`, 격자/seed 양수성을 저장·검사한다(232-259행). 단 transition 내부의 `n`, `w`, `Q`, `gamma`, `h_eta`, `dH_rxn`, `dS_rxn` 전체 유한성은 생성자에서 일괄 검증하지 않는다.
- `GRAPHITE_STAGING_LIT`는 4개 흑연 staging 전이를 제공한다(531-560행).
  - stage 4→3: `U=0.210`, `w=0.020`, `Q=0.10`, `Omega=6000`, `dH_rxn=-11700`, `dS_rxn=29.0`, `n=1.0`, `dH_a=48000`, `dVdq_qa=0.30`(532-537행).
  - stage 3→2L: `U=0.140`, `w=0.016`, `Q=0.12`, `Omega=8000`, `dH_rxn=-13500`, `dS_rxn=0.0`, `n=1.0`, `dH_a=46000`, `dVdq_qa=0.30`(539-544행).
  - stage 2L→2: `U=0.120`, `w=0.014`, `Q=0.25`, `Omega=10000`, `dH_rxn=-13100`, `dS_rxn=-5.0`, `n=1.0`, `dH_a=44000`, `dVdq_qa=0.30`(546-551행).
  - stage 2→1: `U=0.085`, `w=0.012`, `Q=0.50`, `Omega=13000`, `dH_rxn=-13000`, `dS_rxn=-16.0`, `n=1.0`, `dH_a=40000`, `dVdq_qa=0.30`(553-558행).
- 헤더 주석에 따르면 `n`이 있으면 `w`는 fallback으로 inert이고, 기본 폭은 `RT/F ≈ 25.7 mV`이다(7-10행). 실제 `_n_factor`도 `n` 우선 → `w` 역산 → 1.0 순서다(272-278행).

### 1.3 함수별 물리식과 호출 관계

| 함수/메서드 | 코드 근거 | 물리식/동작 | 데이터 흐름 |
|---|---:|---|---|
| `func_w(T,n)` | 74-75 | `w = nRT/F` [V]. | `_width`, `func_ksi_eq`의 logistic 폭. |
| `func_U_j(T,dH_rxn,dS_rxn)` | 78-79 | `U_j(T)=(-ΔH_rxn + TΔS_rxn)/F`. | `equilibrium`, `dqdv`, self-test의 `U(298)` 확인. |
| `func_U_j_hys(T,U_j,Omega,gamma,s,last_eta,last_rest)` | 82-91 | `Ω<=2RT`이면 `ΔU_hys=0`, 아니면 `u=sqrt(1-2RT/Ω)`, `ΔU_hys=(2/F)(Ωu-2RT artanh u)`, 반환 `U_j + 0.5 s gamma ΔU_hys`. | 현재 클래스 주 호출체인은 이 함수가 아니라 `func_U_branch`를 사용한다. `last_eta`, `last_rest`는 코드에서 사용되지 않는다. |
| `func_ksi_eq(T,V_n,U,n,s)` | 94-97 | `ξ_eq = logistic[z]`, `z=s(V_n-U)/(nRT/F)`. overflow 방지를 위해 z 부호별 식을 나눈다. | `equilibrium`: `s` 기본 +1. `dqdv`: `σ_d`를 넘겨 충방전 분기 shape 생성. |
| `func_L_q(T,I,Q_cell,dH_a,dS_a,x,A)` | 100-107 | `I<=0`이면 `-inf`. 그 외 `T_attempt=(I/Q_cell)h/kB`, `ΔG_a=ΔH_a-TΔS_a`, `ln L_q=ln(T_attempt/T)-ln(1+exp(-A/RT))+ΔG_a/RT-xA/RT`, `L_q=exp(ln L_q)`. | `_resolve_lag_length`가 `x` 자리에 방향별 `χ_d`를 넣고 `L_V=|dV/dq|_qa L_q`로 환산한다. |
| `_causal_lowpass(source_signal,grid_step,lag_length)` | 110-128 | `lag_length<=0` 또는 비유한이면 원 신호 복사. 그 외 `exp(-ΔV/L_V)` 지수 기억 필터. SciPy `lfilter` 우선, 실패 시 수동 recurrence. | `dqdv`의 finite lag branch에서 방전은 정방향, 충전은 reverse-filter-reverse로 사용. |
| `func_dU_hys(T,Omega)` | 133-140 | `Ω<=2RT`이면 0. 아니면 `ΔU_hys=(2/F)(Ωu-2RT artanh u)`. | `func_U_branch`, self-test의 hysteresis gap. |
| `func_U_branch(T,U_j,Omega,gamma,sigma_d,h_eta)` | 143-148 | `U_j^d=U_j+0.5 σ_d h_eta gamma ΔU_hys`. | `dqdv`가 `U_j=0`으로 shift만 산출한 뒤 배열 `U_j(T)`에 더한다(444-448행). |
| `func_dH_a_eff(dH_a,Omega,chi_d)` | 152-155 | `ΔH_a^eff=ΔH_a-χ_dΩ`. | `_chi_and_dH_eff`에서 `use_dH_eff`가 true일 때 사용. |
| `func_chi_d(chi,sigma_d)` | 158-163 | 방전 `χ_d=χ`, 충전 `χ_d=1-χ`. | 생성자 기본 `chi_split`, `_chi_d`를 통해 `_resolve_lag_length`에 들어간다. |
| `_finite/_finite_pos/_finite_nonneg` | 167-188 | 유한성, 양수, 비음수 가드. | 생성자, `dqdv`, `_resolve_lag_length`, `curve` 입력 검사. |
| `_build_seed_L_V(T,I,Q_cell)` | 262-269 | 방전 기준 대표 조건에서 전이별 `_resolve_lag_length` 계산. | `__init__`의 `seed_L_V` 진단/초기값용. 실제 `dqdv`는 호출 조건으로 재산출한다. |
| `_n_factor(tr,T)` | 272-278 | `n` 직접값 우선, 없으면 `wF/(RT)` 역산, 없으면 1.0. | `_width`, `equilibrium`, `dqdv`, seed/lag 계산. |
| `_width(tr,T)` | 281-284 | `w=nRT/F`. `use_w_eff` 경로 제거. | peak 분모와 logistic 폭을 동일하게 맞춰 면적 보존. |
| `_chi_d(sigma_d)` | 287-290 | `self.chi_split(self.chi,sigma_d)`. | `_chi_and_dH_eff`. |
| `_chi_and_dH_eff(dH_a,Omega,sigma_d,use_dH_eff)` | 293-300 | `χ_d`와 `ΔH_a^eff`를 한 곳에서 산출. | `_resolve_lag_length`의 장벽 계산. |
| `_resolve_lag_length(transition,T,I,Q_cell,n_j,sigma_d)` | 303-347 | `L_V` 직접 지정 시 그대로. 아니면 `I<=0` 또는 `dH_a is None`이면 0. 동역학 사용 시 `A=min(z_cut|n|RT,A_cap_RT RT)`, `L_q=func_L_q(...)`, `L_V=|dVdq_qa|L_q`. | `dqdv` finite lag 여부 결정. `dVdq_qa`가 없으면 기본 0이어서 꼬리가 사라진다. |
| `equilibrium(V_n,T)` | 350-367 | `C_bg + Σ_j Q_j ξ_j(1-ξ_j)/w_j`. 히스테리시스, 분극, 동역학 꼬리 없음. | `V_n` 기준 평형 dQ/dV. |
| `dqdv(V_app,T,I_abs,Q_cell,s)` | 370-480 | `σ_d=sign(s)`, `V_n=V_app-σ_d|I|R_n`. 작업 격자에서 `U_j`, branch center, `ξ_eq`, `L_V`를 만들고 sub-grid면 equilibrium peak, 아니면 `(ξ_eq-r_bar)/L_V` 꼬리식을 쓴다. | 관측 dQ/dV 주 계산 경로. 결과는 `V_n` 위치에서 보간 반환. |
| `curve(V_app,direction,c_rate,Q_cell,T,I_abs)` | 483-508 | `direction`을 `σ_d`로 변환하고, `I_abs`가 없으면 `|I|=c_rate Q_cell`. | 사용자 facade. 물리는 추가하지 않고 `dqdv`를 재사용한다. |
| `_direction_to_sigma(direction)` | 510-524 | 문자열 `discharge/dis/d/+`는 +1, `charge/chg/c/-`는 -1, 수치형은 부호로 판정. | `curve` 입력 표준화. |

### 1.4 `equilibrium` 세부 흐름

```text
equilibrium(V_n,T)
  T > 0 가드(352)
  V = asarray(V_n)(353)
  baseline = Cbg(V) or constant Cbg(354-356)
  for transition:
    U_j = func_U_j(T,dH_rxn,dS_rxn) if both keys else tr['U'](358-362)
    n_j = _n_factor(tr,T)(363)
    w = _width(tr,T)(364)
    ξ_eq = func_ksi_eq(T,V,U_j,n_j)(365)
    dqdv += Q_j ξ_eq(1-ξ_eq)/w(366)
```

확정: 평형 peak 면적은 폭 `w`와 logistic 분모가 일치할 때 `Q_j[ξ(+∞)-ξ(-∞)]`가 된다. 별도 검산에서 `Cbg=0`, 넓은 격자 `[-0.30,0.70] V` 적분 면적은 `0.9699998217`, `ΣQ=0.97`로 일치했다.

### 1.5 `dqdv` 세부 흐름

```text
dqdv(V_app,T,I_abs,Q_cell,s)
  σ_d = +1 if s>=0 else -1(388)
  I_abs>=0, Q_cell>0, V_app finite/nonempty, T finite/>0 가드(390-405)
  V_n = V_app - σ_d |I| R_n(407-408)
  V_work = padded linspace(V_n min/max)(410-416)
  T_work = T(V) interpolation or scalar mean(418-426)
  dqdv_work = Cbg(V_work)(426-429)
  for transition:
    U_j(T) = func_U_j(T_work,...) or tr['U'](431-436)
    if gamma!=0 and Omega>0:
      hys_shift = func_U_branch(T_rep,0,Omega,gamma,σ_d,h_eta)(441-448)
      center = U_j + hys_shift
    else center = U_j(449-450)
    n_j,w from _n_factor/_width(452-453)
    ξ_eq = func_ksi_eq(T_work,V_work,center,n_j,σ_d)(454-455)
    L_V = _resolve_lag_length(...,T_rep,I_abs,Q_cell,n_rep,σ_d)(457-460)
    if nonfinite or L_V < min_lag_grid_steps*grid_step:
      peak_shape = ξ(1-ξ)/w(462-464)
    else:
      방전: r_bar = lowpass(ξ)
      충전: r_bar = reverse(lowpass(reverse(ξ)))(466-473)
      peak_shape = (ξ-r_bar)/L_V(474-475)
    dqdv_work += Q_j peak_shape(477)
  return interp(V_n,V_work,dqdv_work)(479-480)
```

분극 검산: 코드 자체 실행에서 `Rn=0.01`, 방전 peak는 `I=0.02→0.2→1.0`일 때 `0.100→0.102→0.110 V`로 증가했고, 충전 peak는 `0.100→0.098→0.090 V`로 감소했다. 이는 `V_n=V_app-σ_d|I|R_n` 부호와 정합한다(407-408행, 실행 출력).

히스테리시스 검산: `Ω=12000`, `gamma=1` self-test에서 `ΔU_hys=86.7 mV`, 방전/충전 peak split은 `+86.9 mV`였다(637-646행 실행 출력). `func_dU_hys`와 `func_U_branch` 부호가 self-test 범위에서는 정합한다.

동역학 꼬리 검산: 직접 `L_V=0.02`인 단일 전이에서 넓은 격자 면적은 방전 `0.9994275`, 충전 `0.9994142`로 `Q=1`에 가깝다. `L_V=0.10`에서는 같은 finite span에서 방전 `0.9748906`, 충전 `0.9543438`로 더 손실된다. 이는 무한 영역 물리식의 면적 문제가 아니라 현재 finite work grid/padding의 boundary loss로 보는 것이 타당하다.

### 1.6 `curve` facade 흐름

```text
curve(...)
  direction -> _direction_to_sigma(501)
  Q_cell > 0(502)
  I_abs is None:
    c_rate >= 0
    I_use = c_rate * Q_cell(503-505)
  else:
    I_use = I_abs >= 0(506-507)
  return dqdv(V_app,T,I_use,Q_cell,sigma_d)(508)
```

실행 검산: `curve(discharge,0.2C)`와 직접 `dqdv(I_abs=0.2,s=+1)`의 최대 차이는 `0.00e+00`이었다(608-615행 실행 출력).

## 2. 조건 Audit

### 2.1 BDD 음극 dQ/dV 물리수식 기반 피팅 함수 충족도

확정:

- 평형 중심 `U_j(T)`는 `ΔH_rxn`, `ΔS_rxn` 또는 직접 `U`로 결정된다(358-362, 431-436행).
- 폭은 `w=nRT/F`로 logistic 폭과 peak 분모가 일치한다(74-75, 281-284, 365-366행). 넓은 격자 적분에서 `ΣQ=0.97`과 면적 `0.9699998217`이 일치했다.
- 분극은 `V_n=V_app-σ_d|I|R_n`으로 dQ/dV 관측 축을 이동한다(407-408행).
- 히스테리시스 branch는 `Ω`, `gamma`, `h_eta`, `σ_d`로 중심을 이동한다(133-148, 441-448행).
- 동역학 꼬리는 `L_V` 직접 지정 또는 `dH_a`, `dS_a`, `χ_d`, `Ω`, `z_cut`, `A_cap_RT`, `dVdq_qa`를 통한 계산으로 들어간다(303-347행).
- `curve`는 실험 입력인 방향, C-rate, 용량, 온도를 `dqdv` 호출로 환산한다(483-508행).

판정: 알파 수준의 피팅 함수 골격은 충족한다. 다만 optimizer가 자유롭게 탐색하는 피팅 함수로 쓰기에는 transition 내부 파라미터 가드가 아직 불완전하다.

### 2.2 None/0 가드와 의도 흐름 차단

확정:

- `_resolve_lag_length`는 `L_V` override가 있으면 동역학 계산을 우회한다(313-318행). 이는 의도된 empirical tail override다.
- `I<=0` 또는 `dH_a is None`이면 `L_V=0`을 반환한다(319-320행). 이 경우 `dqdv`는 sub-grid 평형 peak를 사용한다(462-464행). 무전류/동역학 키 부재를 평형 종으로 환원하는 의도는 명확하다.
- `dVdq_qa`는 없으면 `0.0`으로 들어가 `L_V=0`이 된다(346-347행). 이때 오류 없이 꼬리가 꺼진다.

결함/위험:

- `dH_a` 누락과 `dVdq_qa` 누락/0은 동역학 꼬리를 silent-off 한다. 사용자가 동역학 피팅을 의도했는데 키를 빠뜨린 경우에도 호출체인은 정상 종료하므로 결함을 발견하기 어렵다(319-320, 346-347행).
- `func_L_q` 자체는 `I<=0`에서 `-inf`를 반환하지만(100-103행), `_resolve_lag_length`가 먼저 `I<=0`을 0으로 처리하므로 일반 call-chain에서는 `func_L_q`의 `I<=0` branch는 사실상 방어용 중복이다.
- `n` 또는 `w`가 0/음수인 transition은 생성자에서 차단되지 않는다. 별도 edge 검산 결과 `n=0` 또는 `w=0`은 `nan`, `n=-1`은 음수 dQ/dV 값을 만들었다. 근거는 `_n_factor`와 `_width`에 양수 가드가 없고(272-284행), `func_ksi_eq`와 peak 분모가 그대로 나눗셈을 수행하기 때문이다(94-97, 365-366행).

### 2.3 死코드와 중복 경로

확정:

- `func_U_j_hys`는 모듈 함수로 존재하지만 현재 클래스의 `dqdv`는 `func_U_branch`를 사용한다(82-91, 143-148, 444-448행). 따라서 현재 핵심 호출체인 기준으로 `func_U_j_hys`는 legacy helper 또는 비교식이지 활성 경로가 아니다.
- `func_U_j_hys`의 `last_eta`, `last_rest` 인자는 사용되지 않으며, 내부 `partial_hys=1.0`이 고정이다(82-91행). 부분 cycle 인자는 활성 경로에서는 `func_U_branch(..., h_eta)`로 구현된다(143-148, 441-448행).
- `_build_seed_L_V`가 만든 `seed_L_V`는 생성자에서 저장되지만(256-269행), `dqdv` 계산에는 사용되지 않는다. 코드 주석도 진단·초기값용이라고 설명한다(250-255행). 실행 출력에서 4자리 표시로 모두 `0.0000`이었지만 실제 값은 약 `4.91e-08`, `1.47e-08`, `4.37e-09`, `4.75e-10` V였다.

판정: 치명적 dead code는 아니지만, `func_U_j_hys`와 seed 경로는 “물리 주 호출체인”으로 오해하면 안 된다.

### 2.4 시그널/호출체인 정합

확정:

- `curve → dqdv`는 수치적으로 동일하다. 실행 self-test에서 `max_diff=0.00e+00`(608-615행).
- `direction → σ_d` 변환은 discharge 계열 문자열을 +1, charge 계열 문자열을 -1로 보낸다(510-524행).
- `dqdv`는 스칼라 입력이면 스칼라 float를, 배열 입력이면 배열을 반환한다(394-396, 479-480행).
- 비등온 `T(V)`는 `V_n` 정렬 후 `V_work`로 보간한다(418-424행). 단 branch shift는 `T_rep=mean(T_work)`로 한 번 계산한다(426, 444-448행).

위험/추정:

- 비등온 상황에서 `U_j(T)`와 `w(T)`는 배열 온도를 쓰지만(431-455행), hysteresis shift `ΔU_hys(T)`는 평균 온도 `T_rep`를 쓴다(426, 447행). 온도 구배가 크면 branch center의 국소 온도 의존성을 근사 처리한다. 이 근사가 의도인지, 단순 구현 편의인지는 코드 근거만으로는 확정할 수 없다.
- `chi`와 `x`는 물리적으로 0-1 범위가 자연스럽지만 생성자에서는 유한성만 검사한다(234, 237행). `func_chi_d`도 범위 검사를 하지 않는다(158-163행). optimizer가 범위 밖 값을 넣으면 물리적으로 해석하기 어려운 `χ_d`, `ΔH_a^eff`가 가능하다.

### 2.5 면적 보존

확정:

- 평형식의 면적 보존은 코드 구조상 성립한다. `ξ(1-ξ)/w`는 logistic derivative 크기이고, `Q_j`를 곱해 전이 면적을 정한다(94-97, 365-366행).
- 수치 검산: `Cbg=0`, 넓은 격자 `[-0.30,0.70] V`, `GRAPHITE_STAGING_LIT`의 평형 면적 `0.9699998217`, `ΣQ=0.97`.
- direct lag branch는 finite domain에서 padding과 lag length에 의존한다. `L_V=0.005`와 `0.02`에서는 `Q=1` 면적에 매우 근접했지만, `L_V=0.10`에서는 방전 `0.9749`, 충전 `0.9543`으로 손실이 커졌다. 현재 기본 `grid_pad_lo/hi=0.15`와 finite interpolation 영역이 긴 꼬리를 완전히 담지 못할 수 있다(414-416, 479행).

판정: 평형 면적 보존은 충족. finite lag 꼬리는 실험 window와 padding을 포함한 수치 설정의 영향을 받으므로, 큰 `L_V` 피팅에서는 면적 보존 gate를 별도로 두어야 한다.

### 2.6 흑연 음극 전용성

확정:

- 코드 상단과 클래스명, 데이터셋은 흑연 음극 staging 전이를 대상으로 한다(3-11, 192-219, 527-560행).
- `GRAPHITE_STAGING_LIT`는 stage 4→3, 3→2L, 2L→2, 2→1의 4개 흑연 전이를 둔다(531-560행).
- 검색 결과 `LCO`, `q_rev`, `dS_e`, `cathode`, `전자`, `양극`, `heat` 구현 식별자는 발견되지 않았다. `dS_rxn`, `dS_a`는 각각 반응/활성화 엔트로피로 쓰일 뿐 전자엔트로피 `dS_e`나 reversible heat `q_rev` 계층이 아니다(78-79, 100-106, 533-558행).

판정: 흑연 음극 dQ/dV forward model로 확정. LCO 양극, 발열 `q_rev`, 전자엔트로피 `dS_e`는 부재.

### 2.7 부호·차원·극한 적대 검산

부호:

- 분극 부호: `V_n=V_app-σ_d|I|R_n`(407-408행). 실행 self-test에서 방전 전류 증가 시 관측 peak가 높은 `V_app` 쪽으로, 충전 전류 증가 시 낮은 `V_app` 쪽으로 이동했다.
- 히스테리시스 부호: `U_j^d=U_j+0.5σ_d h_eta gamma ΔU_hys`(143-148행). 실행 self-test에서 `ΔU_hys=86.7 mV`, 방전-충전 peak 차 `+86.9 mV`.
- 꼬리 방향: 방전은 증가 전위 방향 lowpass, 충전은 reverse-lowpass-reverse(470-473행). direct `L_V=0.02` demo에서 양 방향 모두 음수 peak가 발생하지 않았다.

차원:

- `w=nRT/F`는 J/mol divided by C/mol = V(74-75행).
- `U=(-ΔH+TΔS)/F`도 J/mol divided by C/mol = V(78-79행).
- `ΔU_hys=(2/F)(Ωu-2RT artanh u)`는 J/mol divided by C/mol = V(133-140행).
- `A=z_cut n RT` 또는 `A_cap_RT RT`는 J/mol(328-331행).
- `func_L_q`의 `T_attempt/T`는 `(I/Q_cell)*(h/kB)/T`로 무차원, 지수항도 모두 무차원이다(104-107행). `dVdq_qa * L_q`는 V 단위 lag length로 쓰인다(346-347행).

극한:

- `Ω<=2RT`이면 hysteresis gap 0(133-140행). 실행 self-test도 `Omega=2RT -> dU_hys=0.000e+00`(657-660행).
- `I_abs=0`이면 `_resolve_lag_length`가 `L_V=0`을 반환하고 평형 peak branch로 간다(319-320, 462-464행).
- `T<=0`, `Q_cell<=0`, `I_abs<0`, `T=NaN`, bad direction, `z_cut<=0`, `L_V=inf`는 self-test에서 모두 예외 처리됐다(667-684행).
- `n=0`, `w=0`, `n<0`은 self-test에 없고 현재 코드에서 차단되지 않는다. 별도 edge 검산에서 NaN 또는 음수 dQ/dV가 발생했다.

## 3. 피팅 파라미터 인벤토리

| 파라미터 | 코드 위치/초기값 | 역할 | 지배 영역 | 자유/고정 초벌 권고 |
|---|---|---|---|---|
| `U_j` 직접값 | `GRAPHITE_STAGING_LIT`: 0.210, 0.140, 0.120, 0.085 V(532-555행) | 전이 중심 전위 fallback. `dH_rxn,dS_rxn`이 있으면 `equilibrium/dqdv`에서는 열역학식이 우선이다(358-362, 431-436행). | peak 위치. | 단일 온도 피팅에서는 `U_j` 또는 `dH_rxn` 중 하나만 자유화. 현재 데이터는 `dH_rxn,dS_rxn` 우선이므로 `U`는 하위호환 라벨로 고정 또는 제거 후보. |
| `dH_rxn`, `dS_rxn` | `[-11700,29]`, `[-13500,0]`, `[-13100,-5]`, `[-13000,-16]`(533-558행) | `U_j(T)=(-ΔH+TΔS)/F`. | peak 위치의 온도 의존성. | 다온도 데이터가 있으면 자유. 단일 온도에서는 강한 상관이 있으므로 `dS_rxn` 고정, `dH_rxn` 또는 `U_j(298)`만 자유 권고. |
| `Q_j` | 0.10, 0.12, 0.25, 0.50, 합 0.97(533-558행) | 전이 면적 가중. | peak 면적, peak 높이. | 자유. 양수 제약과 총량/normalization 제약 권고. |
| `n_j` | 모두 `n=1.0`(534, 541, 548, 555행) | `w=nRT/F` 폭 다중도. `n` 존재 시 `w` fallback은 inert(272-284행). | peak 폭, peak 높이, overlap. | 자유 후보 1순위. 반드시 `n>0` 제약 필요. 현재 코드는 0/음수를 차단하지 않는다. |
| `w` fallback | 0.020, 0.016, 0.014, 0.012 V(533-554행) | `n`이 없을 때만 `n=wF/RT`로 역산(272-278행). | peak 폭. | 현재 `n`이 있으므로 실제 초기 피팅에는 영향 없음. `w`를 직접 핸들로 쓸 경우 `n` 키를 제거하고 `w>0` 제약 필요. |
| `Omega` | 6000, 8000, 10000, 13000 J/mol(533-554행) | hysteresis gap `ΔU_hys`, effective barrier `ΔH_a^eff=ΔH_a-χ_dΩ`. | charge/discharge peak split, tail 길이. | 충방전 쌍 데이터가 있으면 자유. 방전 또는 충전 단독이면 식별성 약하므로 고정/저차원 prior 권고. |
| `gamma` | 데이터셋에는 없음, 기본 0 via `tr.get('gamma',0.0)`(441-448행) | hysteresis gap 축소/확대. | 방전-충전 branch 중심 분리. | hysteresis 데이터가 있을 때만 자유. 없으면 0 고정. |
| `h_eta` | 데이터셋에는 없음, 기본 1.0(441-448행) | 부분 cycle branch scale. | hysteresis split 크기. | partial cycle 실험 설계가 없으면 1.0 고정. |
| `dH_a` | 48000, 46000, 44000, 40000 J/mol(536-558행) | Arrhenius tail length. `use_dH_eff` true면 `Ω`와 `χ_d`로 보정. | 동역학 꼬리 길이, rate/T dependence, peak 비대칭. | 다 C-rate/다온도 데이터에서 자유. 단일 곡선에서는 `L_V` 직접 피팅이 더 안정적일 수 있음. |
| `dS_a` | 모두 0.0 default/명시(536-558행) | activation entropy. `ΔG_a=ΔH_a-TΔS_a`. | tail의 온도 의존성. | 온도 sweep 없으면 0 고정. 다온도 rate 데이터가 있을 때만 자유. |
| `chi` / `x` | 생성자 `x=0.5`, `chi=None`이면 `chi=x`(221-237행) | 전이상태 위치/전달계수. 방향별 `χ_d=χ` 또는 `1-χ`. | charge/discharge tail 비대칭, `ΔH_a^eff`. | 0-1 범위 제약을 걸고 자유화. 초기 0.5. 현재 코드는 범위 제약이 없으므로 fitter 쪽 제약 필요. |
| `chi_split` | 기본 `func_chi_d`(221-225, 158-163행) | 방향별 barrier split 규칙 교체. | 충방전 tail 비대칭. | 모델 구조 선택 항목. 기본 고정. 비대칭 분배 가설을 검정할 때만 교체. |
| `L_V` | transition key 선택값(208-210, 313-318행) | 직접 lag length. 있으면 `dH_a/dS_a/dVdq_qa` 동역학 계산 우회. | 꼬리 길이, peak 뒤끌림, finite-window 면적. | 경험적 1차 피팅에서는 자유 후보. 물리 기반 피팅에서는 제거하고 `dH_a,dS_a,dVdq_qa` 사용. |
| `dVdq_qa` | 모두 0.30 V(536-558행) | `L_q -> L_V` 환산 scale. | tail 길이. | `dH_a`와 강하게 상관. 둘 중 하나를 고정하거나 stage 공통 scale로 묶는 권고. 누락 시 silent `L_V=0` 위험. |
| `z_cut` | 생성자 default 4.357, per-transition override 가능(226, 328-331행) | tail affinity cutoff. | derived `L_V` 크기. | numerical/definition parameter로 고정 권고. sensitivity audit만 수행. |
| `A_cap_RT` | 생성자 default 4.0, per-transition override 가능(226, 328-331행) | `A <= A_cap_RT RT` 상한. | derived `L_V` 상한/꼬리. | 고정 권고. 자유화하면 `z_cut`, `dH_a`, `dVdq_qa`와 식별성 충돌. |
| `use_dH_eff` | 생성자 default true, transition override 가능(225, 293-300, 337-340행) | `ΔH_a^eff` 보강 on/off. | `Ω`, `χ_d`가 꼬리에 미치는 영향. | 모델 선택 플래그로 고정. 비교 실험에서 true/false 별도 fit. |
| `Rn` | 생성자 default 0.0, self-test 0.01(221-235, 407-408행) | ohmic polarization. | C-rate에 따른 전체 peak 위치 이동. | EIS/전압 IR 정보가 있으면 고정. 없으면 C-rate series에서 자유. |
| `Cbg` | 생성자 default 0.0, scalar/callable(221-236, 354-356, 426-429행) | background dQ/dV. | baseline, 낮은 곡률 영역, apparent area. | 상수 또는 낮은 차수 smooth background로 자유. callable 출력 유한성은 사용자 책임. |
| `Q_cell` | `dqdv/curve` 호출 인자(370-381, 483-508행) | C-rate→current, `I/Q_cell` rate scale. | 동역학 tail scale. | 실험 입력으로 고정. 피팅 파라미터로 두면 `I_abs`, `dH_a`, `dVdq_qa`와 혼동. |
| `I_abs`, `c_rate`, `T`, `direction` | 호출 인자(370-389, 483-508행) | 실험 조건. | 분극, tail, 온도별 peak 위치/폭. | 데이터 메타데이터로 고정. |
| `grid_pad_lo/hi`, `n_work_min`, `min_lag_grid_steps`, `v_span_floor` | 생성자 default 0.15/0.15/2048/2.0/1e-6(226-229행) | 수치 격자와 lag branch threshold. | 큰 `L_V`의 꼬리 면적, interpolation 안정성. | 피팅 물리 파라미터가 아니라 numerical controls. 큰 tail 데이터에서는 padding 검증 후 고정. |

## 4. 결론

확정:

- 이 코드는 흑연 음극 staging 기반 dQ/dV forward model이다. 평형 peak, 분극, hysteresis branch, 동역학 꼬리, facade 호출체인이 모두 코드상 연결되어 있다.
- LCO 양극, 발열 `q_rev`, 전자엔트로피 `dS_e` 구현은 없다.
- 평형 면적 보존은 구조와 수치 검산 모두에서 성립한다.
- `curve → dqdv` 호출체인, 분극 부호, hysteresis branch 부호, 기본 가드 self-test는 실행상 통과했다.

결함/주의:

- transition 내부 `n/w` 양수 가드가 없어 0/음수 폭에서 NaN 또는 음수 dQ/dV가 발생한다.
- `dH_a` 누락, `dVdq_qa` 누락/0은 동역학 꼬리를 silent-off 하므로 피팅 입력 검증이 필요하다.
- `func_U_j_hys`는 현재 주 호출체인에서 쓰이지 않으며, `last_eta/last_rest`도 미사용이다.
- 큰 `L_V` 꼬리는 finite work grid/padding에 따라 면적 손실이 생길 수 있다.
- `chi/x` 범위 제약과 callable `Cbg` 출력 유한성은 코드 내부에서 완전히 보장하지 않는다.
