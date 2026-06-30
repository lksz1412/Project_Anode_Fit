# V1010 P1 draft C1 - graphite dQ/dV code audit

## 0. 확인 범위

- 대상 파일: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`
- READ_FULL: 1-701행을 head-to-tail로 직접 확인했다. 사용자 지시문에는 695줄이라고 되어 있으나, 실제 줄 번호 출력 기준 파일은 701줄이다.
- 수행 범위: 분석 및 결과 파일 작성만 수행했다. 대상 Python 코드는 수정하지 않았다.
- 실행 확인:
  - `python Claude\docs\v1.0.10\Anode_Fit_v1.0.10.py` 실행 결과 `>>> overall OK: True`.
  - 추가 면적 검산: 기본 `GRAPHITE_STAGING_LIT`의 `sum(Q)=0.97`, 넓은 전압 구간 `[-0.20, 0.60]`에서 평형 적분 면적 `0.9699912597`.
  - 전용성 검색: `LCO`, `q_rev`, `dS_e`, `cathode`, `양극`, `발열`, `전자엔트로피` 키워드 근거 미발견.

## 1. 플로우차트 맵

### 1.1 전체 데이터 흐름

```text
GRAPHITE_STAGING_LIT / 사용자 transitions
  -> __init__(transitions, x, Rn, Cbg, chi, chi_split, use_dH_eff,
              z_cut, A_cap_RT, grid_pad_*, n_work_min, min_lag_grid_steps,
              v_span_floor, seed_T/I/Q_cell) [221-259]
  -> seed_L_V 진단값: _build_seed_L_V -> _resolve_lag_length [262-269, 303-347]

equilibrium(V_n, T) [350-367]
  -> baseline Cbg [354-357]
  -> U_j(T) = func_U_j(dH_rxn,dS_rxn) 또는 U [359-362]
  -> n_j = _n_factor, w = _width [363-364]
  -> ksi_eq = func_ksi_eq(T,V,U,n) [365]
  -> dQ/dV = Cbg + sum_j Q_j xi(1-xi)/w [366]

dqdv(V_app,T,I_abs,Q_cell,s) [370-480]
  -> sigma_d = sign(s) [388]
  -> V_n = V_app - sigma_d |I| Rn [407-408]
  -> V_work 작업 격자 + T_work 보간 [410-426]
  -> 각 transition:
       U_j(T_work) [431-437]
       hysteresis center = U_j + 0.5*sigma_d*h_eta*gamma*dU_hys(T_rep,Omega) [441-450]
       n_j, w, xi_eq = logistic[sigma_d*(V_work-center)/w] [452-455]
       lag_len_V = _resolve_lag_length(... sigma_d) [457-460]
       if lag sub-grid/0: peak = xi(1-xi)/w [462-465]
       else: causal lowpass direction by sigma_d; peak = (xi - lagged xi)/L_V [466-475]
       dqdv_work += Q_j * peak [477]
  -> interpolate back from V_n to user V_app order [479-480]

curve(V_app,direction,c_rate,Q_cell,T,I_abs) [483-508]
  -> direction string/int -> sigma_d [501, 511-524]
  -> I_abs 직접 또는 c_rate*Q_cell [502-507]
  -> dqdv(...) 재사용 [508]
```

### 1.2 함수별 물리식과 줄 근거

| 함수/메서드 | 줄 | 물리식/역할 | 호출·데이터 흐름 근거 |
|---|---:|---|---|
| `func_w` | 74-75 | 전이 폭 `w = nRT/F`. | `_width`가 `func_w(T, _n_factor(...))`로 호출한다 [281-284]. |
| `func_U_j` | 78-79 | 평형 중심 `U_j(T)=(-dH_rxn + T*dS_rxn)/F`. | `equilibrium` [359-360], `dqdv` [433-434], self-test U(298) 출력 [582-584]. |
| `func_U_j_hys` | 82-91 | `Omega > 2RT`이면 `u=sqrt(1-2RT/Omega)`, `dU_hys=(2/F)(Omega*u-2RT*artanh(u))`, 반환 `U_j + 0.5*s*gamma*dU_hys`. | 클래스 내부 호출 근거 미발견. legacy/public 함수로 남아 있고, 실제 dqdv는 `func_U_branch`를 쓴다 [447]. `last_eta`, `last_rest`는 미사용 [82-91]. |
| `func_ksi_eq` | 94-97 | 안정 logistic: `xi = 1/(1+exp(-z))`, `z=s*(V_n-U)/func_w(T,n)`. | `equilibrium` [365], `dqdv` [455]. |
| `func_L_q` | 100-107 | `I<=0`이면 `-inf`; 그 외 `T_attempt=(I/Q_cell)h/kB`, `dG_a=dH_a-T*dS_a`, `ln L_q=log(T_attempt/T)-log(1+exp(-A/RT))+dG_a/RT-xA/RT`. | `_resolve_lag_length`에서 `x=chi_d`, `dH_a_use`를 넣어 호출 [341-342]. |
| `_causal_lowpass` | 110-128 | lag length가 양수·유한이면 지수 메모리 `r_i=a*r_{i-1}+(1-a)*source_i`, `a=exp(-grid_step/L)`. SciPy `lfilter`가 있으면 사용, 실패 시 루프 fallback. | `dqdv`에서 방전은 정방향, 충전은 reverse-filter-reverse로 호출 [470-473]. |
| `func_dU_hys` | 133-140 | `Omega<=2RT`이면 gap 0, 아니면 `func_U_j_hys`와 같은 `dU_hys` 식. | `func_U_branch` [148], self-test spinodal limit [657-660]. |
| `func_U_branch` | 143-148 | 분기 중심 `U_j^d=U_j+0.5*sigma_d*h_eta*gamma*dU_hys`. | `dqdv`에서 `U_j=0` shift를 계산한 뒤 배열 `U_j`에 더한다 [444-448]. |
| `func_dH_a_eff` | 152-155 | 유효 활성화 엔탈피 `dH_a_eff=dH_a-chi_d*Omega`. | `_chi_and_dH_eff`가 `use_dH_eff`일 때 호출 [297-299]. |
| `func_chi_d` | 158-163 | 방향별 전달계수: 방전 `chi`, 충전 `1-chi`. | 생성자 기본 `chi_split` [221-225], `_chi_d` 호출 [287-290], self-test custom split [622-635]. |
| `_finite`, `_finite_pos`, `_finite_nonneg` | 167-188 | 입력 유한성, 양수, 비음수 가드. | 생성자 스칼라 [234-248], `dqdv` 입력 [391-405], lag dict 일부 [328-347]. |
| `__init__` | 221-259 | transitions와 전역 파라미터 저장, `chi` 기본값은 `x`, seed 조건으로 `seed_L_V` 생성. | `self.transitions` 보존 [232], `seed_L_V` 생성 [256-259]. |
| `_build_seed_L_V` | 262-269 | 전이별 대표 조건 방전 기준 `L_V` seed 계산. | 생성자에서만 호출 [256-259]. `dqdv` 본 계산에는 쓰이지 않으므로 진단/초기값 성격이다 [254-255]. |
| `_n_factor` | 272-278 | 우선순위: `n`이 `None` 아니면 `n`; 아니면 `w*F/(RT)`; 없으면 1. | `_width`, `equilibrium`, `dqdv`, `_build_seed_L_V`가 사용 [266, 363, 452, 458]. |
| `_width` | 281-284 | `w=nRT/F`; `use_w_eff` 경로 제거. | peak 분모와 logistic 폭을 같은 `w`로 유지 [364-366, 452-455]. |
| `_chi_d` | 287-290 | `chi_split(self.chi, sigma_d)`를 float화. | `_chi_and_dH_eff`가 사용 [297]. |
| `_chi_and_dH_eff` | 293-300 | `chi_d`와 `dH_a_eff`를 한 곳에서 산출. `use_dH_eff=False`면 원래 `dH_a`. | `_resolve_lag_length` [337-339]. |
| `_resolve_lag_length` | 303-347 | `L_V` 직접 지정 우선. 없으면 `A=min(z_cut*|n|RT, A_cap_RT*RT)`, `L_q=func_L_q(...)`, `L_V=|dVdq_qa|*L_q`. | `seed_L_V` [267-268], `dqdv` [459-460], self-test override isolation [686-698]. |
| `equilibrium` | 350-367 | 방향·전류·히스 없는 평형 `Cbg + sum Q*xi(1-xi)/w`. | callable/scalar Cbg 모두 처리 [354-356]. |
| `dqdv` | 370-480 | 관측 곡선: 분극, 히스 분기, 동역학 꼬리, 충방전 방향을 결합. | `curve`가 재사용 [508]. |
| `curve` | 483-508 | 실험 조건 facade. 새 물리 없이 direction/C-rate/I_abs를 정규화해 `dqdv` 호출. | direction helper [501], current 결정 [503-507]. |
| `_direction_to_sigma` | 511-524 | 문자열/수치 방향을 `+1/-1`로 변환. | `curve` [501], bad direction self-test [675]. |

### 1.3 `GRAPHITE_STAGING_LIT` 입력 맵

| 전이 | 줄 | 초기 중심/용량 | 열역학 | 폭 | 동역학 | 상호작용 |
|---|---:|---|---|---|---|---|
| stage 4->3 | 532-538 | `U=0.210`, `Q=0.10` | `dH_rxn=-11700`, `dS_rxn=+29` | `w=0.020`, `n=1.0` | `dH_a=48000`, `dS_a=0`, `dVdq_qa=0.30` | `Omega=6000` |
| stage 3->2L | 539-545 | `U=0.140`, `Q=0.12` | `dH_rxn=-13500`, `dS_rxn=0` | `w=0.016`, `n=1.0` | `dH_a=46000`, `dS_a=0`, `dVdq_qa=0.30` | `Omega=8000` |
| stage 2L->2 | 546-552 | `U=0.120`, `Q=0.25` | `dH_rxn=-13100`, `dS_rxn=-5` | `w=0.014`, `n=1.0` | `dH_a=44000`, `dS_a=0`, `dVdq_qa=0.30` | `Omega=10000` |
| stage 2->1 | 553-559 | `U=0.085`, `Q=0.50` | `dH_rxn=-13000`, `dS_rxn=-16` | `w=0.012`, `n=1.0` | `dH_a=40000`, `dS_a=0`, `dVdq_qa=0.30` | `Omega=13000` |

주의: `_n_factor` 우선순위 때문에 `n=1.0`이 있는 기본 데이터에서는 `w` 값이 폭에 쓰이지 않는다 [272-278]. 실제 폭은 298.15 K에서 `RT/F=0.025691238 V`이고, `w=0.012-0.020`은 `n` 제거 시에만 역산 경로로 활성화된다. 코드 헤더도 이 점을 명시한다 [7-10].

## 2. 조건 audit

### 2.1 충족 판단

| 항목 | 판단 | 증거 |
|---|---|---|
| BDD 음극 dQ/dV 물리수식 기반 피팅 함수 | 대체로 충족 | 입력 파라미터가 `transitions`와 생성자/호출 인자로 노출되어 있고 [198-218, 221-231], 평형 logistic peak [350-367], 분극 [407-408], 히스 분기 [441-455], 동역학 꼬리 [457-475]가 한 호출 체인에 들어간다. |
| 흑연 음극 전용 | 확정 | 파일 헤더·클래스가 흑연 음극으로 명시 [3-7, 192-193], 데이터셋은 graphite staging [527-560]. `LCO`, `q_rev`, `dS_e`, 양극, 발열, 전자엔트로피 관련 코드 근거 미발견. |
| equilibrium 기준선 | 충족 | `equilibrium`은 방향과 전류 없이 `Q*xi(1-xi)/w`를 합산한다 [350-367]. 넓은 구간 적분 `0.969991`로 `sum(Q)=0.97`에 근접. |
| dqdv 호출 체인 | 충족 | `curve -> dqdv` [501-508], `dqdv -> func_U_j/func_U_branch/func_ksi_eq/_resolve_lag_length/_causal_lowpass` [431-475]. |
| 면적 보존 | 조건부 충족 | 평형과 sub-grid lag는 `xi(1-xi)/w`라 면적 보존이 좋다 [462-465]. 직접 `L_V` lag 검산도 `L=0.02`에서 단일 `Q=0.5` 대비 방전 0.499674, 충전 0.499667로 근접. 단, 긴 꼬리와 유한 작업 격자에서는 경계 손실이 생긴다(`L=0.08`, 충전 0.489003). |
| 부호 정합 | 대체로 충족 | 분극은 `V_n=V_app-sigma_d|I|Rn` [407-408]. self-test에서 방전 전류 증가 시 peak 전위가 0.100->0.110, 충전은 0.100->0.090으로 반대 이동. 히스 분기는 `sigma_d` 부호로 반대 shift [447-448]. |
| 차원 정합 | 대체로 충족 | `w=nRT/F`는 V [74-75], `U=(-dH+TdS)/F`는 V [78-79], `dU_hys`는 J/mol divided by F로 V [133-140], `A`는 J/mol [331], `L_V=|dVdq_qa|*L_q` [346-347]. 단 `dVdq_qa` 주석은 `[V]`라고 쓰지만 실제 의미는 `|dV/dq|`라 q가 무차원일 때 V로 볼 수 있다 [207, 346-347]. |
| 극한 | 부분 충족 | `Omega<=2RT -> dU_hys=0` [137-140], self-test 확인 [657-660]. `I<=0` 또는 `dH_a is None -> L_V=0` [319-320]라 평형 종으로 환원. `gamma=0, |I|->0` self-test에서 충방전 차이 `5.107e-15`. |

### 2.2 결함·위험 audit

| 등급 | 항목 | 증거 | 영향 | 권고 |
|---|---|---|---|---|
| 결함 | `n=0` 또는 음수 폭 가드 부재 | `_n_factor`는 `n`을 그대로 반환 [272-278], `_width`도 양수 확인 없이 `func_w` 호출 [281-284]. 추가 검산에서 `n=0`은 `nan`, `n=-1`은 음수 dQ/dV를 생성. | 피팅 중 optimizer가 0/음수 `n`을 탐색하면 NaN 또는 음수 peak가 생겨 BDD 물리 곡선을 깨뜨린다. | `n`/`w`는 양수 제약으로 fitting bounds를 두는 것이 필수. 코드 수정 범위 밖이므로 여기서는 보고만 한다. |
| 결함 | `chi`/`x` 범위 가드 부재 | 생성자는 유한성만 검사한다 [234, 237]. `func_chi_d`는 그대로 `chi` 또는 `1-chi` 반환 [158-163]. | `chi<0` 또는 `chi>1`이면 전이상태 분율/장벽 분배가 물리 범위를 벗어나며 `dH_a_eff`가 과도하게 변한다. | 피팅 자유변수는 `[0,1]` bound 권고. |
| 위험 | 기본 데이터의 `w`가 inert | `n` 우선 [274-275], `w`는 `n`이 없을 때만 사용 [276-277]. 기본 전이는 모두 `n=1.0` [534, 541, 548, 555]. | 표의 `w=0.012-0.020`을 피팅 초기 폭으로 기대하면 실제 곡선 폭은 전부 25.69 mV로 같아진다. | 폭 fitting은 `n`을 조정하거나, `n` key를 제거하고 `w`를 직접 쓰는 정책 중 하나로 고정해야 한다. |
| 위험 | `dVdq_qa` 누락 시 꼬리 자동 소거 | `_resolve_lag_length`는 `transition.get('dVdq_qa',0.0)`에 `abs`를 곱한다 [346-347]. | `dH_a`가 있어도 `dVdq_qa` 누락이면 `L_V=0`이 되어 동역학 꼬리가 사라진다. 의도적 평형 전이와 누락 실수가 구분되지 않는다. | fitting schema에서 동역학 전이는 `dVdq_qa>0` 필수로 관리. |
| 위험 | `dH_a is None`은 꼬리 off 스위치 | `I<=0 or transition.get('dH_a') is None`이면 0 반환 [319-320]. | 명시적 `None`은 의도 흐름 차단이다. 다만 `dH_a=0`은 허용된다. | 평형-only 전이는 `dH_a` 생략/None으로 명시 가능하나, fitting 입력 검증에서 누락과 의도를 구분해야 한다. |
| 위험 | `func_U_j_hys`는 현재 호출 체인 밖 | 함수 정의 [82-91], 클래스는 `func_U_branch`를 호출 [447]. | legacy API로는 존재하지만 실제 dqdv flow에는 들어가지 않는다. 또한 `last_eta`, `last_rest`는 미사용이고 `partial_hys=1.0` 하드코딩 [82-91]. | 문서에는 legacy helper로 분류. 실제 branch 근거는 `func_U_branch`로 잡아야 한다. |
| 위험 | `seed_L_V`는 진단값이지 실제 초기화 주입 아님 | 생성자에서 계산 [256-259], 주석도 실제 dqdv가 재산출한다고 명시 [254-255]. | seed를 fitting initial guess로 사용할 수는 있지만, curve 계산에 seed가 직접 반영된다고 해석하면 안 된다. | 인벤토리에서 `seed_*`는 계산 조건으로만 분류. |
| 위험 | `Cbg` callable 출력 유한성 미검사 | 생성자 주석이 사용자 책임이라고 명시 [236], `equilibrium/dqdv`는 출력 검사 없이 더한다 [354-357, 427-429]. | 배경 함수가 NaN/inf를 내면 곡선 전체가 오염된다. | fitting wrapper에서 `Cbg(V)` 유한성 검증 권고. |
| 위험 | `Omega`/`gamma`의 dqdv branch 가드는 느슨함 | dqdv에서는 `float(tr.get(...))`만 수행 [441-443], `gamma != 0 and Omega > 0`일 때만 branch [444]. | `Omega=nan`이면 비교가 false가 되어 히스가 조용히 비활성화될 수 있다. `_resolve_lag_length`에서는 `Omega` 유한·비음수 가드가 있다 [335]. | 히스 fitting 입력은 별도 schema 검증이 필요. |
| 결함 아님 | `func_L_q(I<=0)->-inf` | 직접 함수는 `-inf` 반환 [102-103], resolver는 그 전에 `I<=0`을 `L_V=0`으로 처리 [319-320]. | 클래스 경로에서는 평형 환원으로 안전하다. 직접 API 사용자는 `-inf`를 받을 수 있다. | public helper 사용 문서에 명시. |
| 결함 아님 | 직접 `L_V=0` | override는 0 이상이면 허용 [314-318], dqdv에서 sub-grid면 평형 peak로 간다 [462-465]. | `L_V=0`은 꼬리 off로 자연스럽다. | 유지 가능. |

### 2.3 적대 검산 요약

- 부호: `sigma_d=+1` 방전은 분극으로 `V_n=V_app-|I|Rn`, 같은 `V_n` 중심을 맞추려면 관측 peak가 높은 `V_app`로 이동한다 [407-408]. 실행 결과 방전 peak는 I 증가에 따라 `0.100 -> 0.102 -> 0.110`, 충전은 `0.100 -> 0.098 -> 0.090`.
- 히스 극한: `Omega<=2RT`일 때 `func_dU_hys=0` [137-140], 실행 결과 `0.000e+00`. `gamma=0`이면 branch shift가 꺼진다 [444-450].
- 동역학 꼬리 방향: 방전은 정방향 lowpass, 충전은 reverse-filter-reverse [470-473]. self-test에서 직접 `L_V=0.02`일 때 방전 peak `0.134`, 충전 peak `0.106`으로 반대쪽 꼬리 [648-655].
- 면적: logistic 평형 종은 넓은 구간에서 `sum(Q)` 보존. lag 종은 finite grid/padding에서 긴 꼬리 손실 가능성이 있다. 이는 수치 도메인 손실이지 수식 자체의 즉시 결함은 아니지만, 큰 `L_V` fitting에서는 전압 창과 `grid_pad_lo/hi`가 같이 식별된다.
- 차원: `A=min(z_cut*nRT, A_cap_RT*RT)` [328-331]에서 `z_cut`/`A_cap_RT`는 무차원, `A`는 J/mol이다. `func_L_q`의 exp 항은 모두 무차원 [104-107].

## 3. 피팅 파라미터 인벤토리

| 파라미터 | 코드 위치/초기값 | 역할 | 지배 곡선 영역 | 자유/고정 초벌 권고 |
|---|---|---|---|---|
| `Q` | 전이별 0.10, 0.12, 0.25, 0.50 [533, 540, 547, 554] | 전이 peak 면적/가중치. `dqdv += Q*shape` [477], equilibrium도 `Q*xi(1-xi)/w` [366]. | peak 면적과 높이. 폭 고정 시 높이에도 직접 영향. | 자유. 단 전체 용량 정규화가 있으면 `sum(Q)` 제약 권고. |
| `U` | 0.210, 0.140, 0.120, 0.085 [533, 540, 547, 554] | `dH_rxn/dS_rxn` 없을 때 중심 전위 fallback [361-362, 435-436]. | peak 위치. | 기본 데이터에서는 열역학 키가 있어 fallback이다. 직접 fitting 시 `U` 또는 `dH_rxn/dS_rxn` 중 하나만 주 핸들로 선택. |
| `dH_rxn` | -11700, -13500, -13100, -13000 J/mol [534, 541, 548, 555] | `U_j(T)=(-dH+T*dS)/F`의 enthalpy 항 [78-79]. | 온도별 peak 위치 intercept. | 다온도 데이터가 있으면 자유, 단 `U(298)`와 강하게 결합. 단일 온도면 `U`로 환산해 고정/축소 권고. |
| `dS_rxn` | +29, 0, -5, -16 J/mol/K [534, 541, 548, 555] | `U_j(T)` 온도 기울기 [78-79]. | 온도 변화에 따른 peak 위치 이동. | 다온도 데이터 없으면 고정 권고. |
| `n_j` / `n` | 기본 모두 1.0 [534, 541, 548, 555] | 폭 `w=nRT/F` [74-75, 281-284]. | peak 폭, 폭을 통한 peak 높이(면적 보존 시 `height~Q/(4w)`). | 자유 가능하지만 `n>0` bound 필수. 기본 데이터에서는 `w`보다 우선한다. |
| `w` | 0.020, 0.016, 0.014, 0.012 [533, 540, 547, 554] | `n`이 없을 때 `n=wF/RT`로 역산 [276-277]. | peak 폭/높이. | 현재 기본에서는 inert. `w`를 쓸 거면 `n` 제거 또는 schema 정책 필요. |
| `Omega` | 6000, 8000, 10000, 13000 J/mol [533, 540, 547, 554] | 히스 gap `dU_hys` [133-140], 유효장벽 `dH_a_eff=dH_a-chi_d*Omega` [152-155]. | 히스 분기 간격, 꼬리 길이(장벽 감소) 양쪽. | 데이터가 충분하면 자유. 아니면 히스와 꼬리가 동시에 움직이므로 고정/단계 fitting 권고. |
| `gamma` | 기본 데이터에는 없음, default 0 [441-442] | 히스 분기 축소 인자: shift `0.5*sigma*h_eta*gamma*dU_hys` [143-148, 447-448]. | 충방전 peak 분리. | 충방전 loop 데이터가 있으면 자유 `[0,1]` 권고. 단방향 데이터면 고정 0. |
| `h_eta` | default 1.0 [443] | partial cycle branch scale [143-148]. | 히스 분기 shift 크기. | partial-cycle 실험 메타가 없으면 고정 1.0. |
| `dH_a` | 48000, 46000, 44000, 40000 J/mol [536, 543, 550, 557] | `func_L_q`의 Arrhenius barrier, 선택적으로 `Omega` 보정 후 사용 [333-342]. | 꼬리 길이, rate-dependence, peak 비대칭. | rate series가 있으면 자유. 단 `L_V` 직접 fitting과 동시 자유는 과식별 위험. |
| `dS_a` | 기본 모두 0 [536, 543, 550, 557] | `dG_a=dH_a-T*dS_a` [105]. | 꼬리의 온도 의존성. | 다온도·다율 데이터 없으면 고정 0. |
| `chi` / `x` | 생성자 `x=0.5`, `chi=None -> x` [221-237] | 방향별 장벽 분배 `chi_d`의 기준 [287-300]. | 방전/충전 꼬리 비대칭, `dH_a_eff`. | `[0,1]` bound로 자유 가능. 충방전 rate data 없으면 0.5 고정. |
| `chi_split` | default `func_chi_d` [221-225, 158-163] | 방전 `chi`, 충전 `1-chi` 규칙 또는 사용자 규칙. | 방향별 꼬리 비대칭. | 일반 fitting에서는 고정. 모델 구조 비교 때만 교체. |
| `use_dH_eff` | default True [225, 241] | `dH_a_eff` 적용 여부 [297-299]. 전이별 override 가능 [338-339]. | 꼬리 길이와 `Omega`-kinetics coupling. | 모델 선택 스위치. 한 번 정하면 고정. |
| `L_V` | transition optional [209, 313-318] | 지연 길이 직접 지정, 동역학 산출 우회. | 꼬리 길이와 peak 비대칭. | 초기 fitting에서는 직접 `L_V` 자유가 안정적. 물리 해석 단계에서는 `dH_a/dS_a/dVdq_qa` 산출 경로로 전환. |
| `dVdq_qa` | 기본 모두 0.30 [536, 543, 550, 557] | `L_q -> L_V` 환산 기울기 [346-347]. | 꼬리 전압 길이 스케일. | `L_V` 직접 fitting 시 고정. 물리 경로 fitting 시 양수 bound로 자유 가능. |
| `z_cut` | 생성자 default 4.357 [226, 242], 전이 override [329] | 컷 affinity `A=z_cut*nRT`의 하한 후보 [328-331]. | 꼬리 시작/길이 산출 민감도. | 일반 fitting에서는 고정. 전이별 override는 민감도 검토용. |
| `A_cap_RT` | default 4.0 [226, 243], 전이 override [330] | `A <= A_cap_RT*RT` 상한 [329-331]. | 꼬리 길이 산출 상한. | 고정 권고. |
| `Rn` | 생성자 default 0.0 [221-235] | ohmic polarization `V_n=V_app-sigma|I|Rn` [407-408]. | rate별 전체 peak 위치 이동. | rate series가 있으면 자유, 단 전이별 `U` shift와 분리 필요. |
| `Cbg` | default 0.0 [221-236] | 상수/callable background [354-357, 427-429]. | 전체 baseline, valley offset. | 실험 baseline이 있으면 낮은 차수 함수/상수로 자유. callable 출력 유한성은 wrapper에서 검사. |
| `grid_pad_lo`, `grid_pad_hi` | default 0.15 [227, 244-245] | 꼬리 계산 작업 격자 padding [410-416]. | 긴 꼬리 면적 손실/경계 효과. | fitting 물리 파라미터로 보지 말고 수치 설정으로 고정. 큰 `L_V`면 확대 검토. |
| `n_work_min` | default 2048 [228, 246] | 작업 격자 해상도 [412]. | 수치 smoothness, peak interpolation. | 고정. |
| `min_lag_grid_steps` | default 2.0 [228, 247] | lag가 grid step 대비 너무 짧으면 평형 peak로 환원 [462-465]. | 저율/짧은 꼬리에서 평형 처리 threshold. | 수치 설정으로 고정. |
| `v_span_floor` | default 1e-6 [229, 248] | 입력 전압 span이 작을 때 작업 격자 최소 span [410-411]. | scalar/좁은 V 입력 안정성. | 고정. |
| `T` | 호출 default 298.15 [350, 488] | 모든 열역학/폭/동역학 식에 들어감 [352, 402-426]. | peak 위치, 폭, 꼬리 온도 의존성. | 실험 조건으로 고정 입력. |
| `I_abs`, `c_rate`, `Q_cell` | `dqdv` [370-375], `curve` [483-508] | rate/current와 `L_q`, 분극 결정 [391-392, 503-508]. | rate별 shift와 꼬리. | 실험 조건으로 고정 입력. |

## 4. 결론

- 이 코드는 흑연 음극 dQ/dV forward model로서 equilibrium peak, ohmic polarization, hysteresis branch, kinetic tail을 한 호출 체인에 연결한다.
- 코드 기준 충족도는 높지만, fitting 함수로 쓰려면 `n/w/chi/Omega/gamma/dVdq_qa`의 bounds와 schema 검증이 별도 필요하다.
- 가장 큰 즉시 위험은 `n=0/음수`가 막히지 않아 NaN/음수 peak가 가능한 점, 그리고 기본 데이터에서 `w`가 `n=1.0`에 의해 비활성이라는 점이다.
- 면적 보존은 평형 및 짧은/중간 lag에서 양호하지만, 큰 `L_V`에서는 유한 작업 격자 padding에 따른 꼬리 면적 손실이 관측된다.
- LCO 양극, reversible heat `q_rev`, electron entropy `dS_e`는 코드 근거가 없으며 흑연 음극 전용으로 확정한다.
