# Anode_Fit v1.0.10 P1 분석 드래프트 C3

## 0. 확인 범위

- 지시 파일: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p1_codex_C3.txt` 1-13행 전문 확인.
- 프로젝트 지침: `Codex/AGENTS.md` 전문 확인. 사용자 지시가 `Claude/results/process/V1010_P1_draft_C3.md` 출력을 명시했으므로 이 파일만 Claude 결과 폴더에 신규 작성.
- 대상 코드: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` 1-702행 전문 정독. 최초 출력 축약으로 빠진 303-369행은 좁혀 재확인.
- 다른 경쟁 드래프트 파일은 읽지 않음. 독립 작성.

## 1. 플로우차트 맵

### 1.1 전체 데이터 흐름

```text
GRAPHITE_STAGING_LIT / 사용자 transitions
  -> __init__(transitions, x, Rn, Cbg, chi, chi_split, use_dH_eff, z_cut, A_cap_RT,
              grid_pad_*, n_work_min, min_lag_grid_steps, v_span_floor, seed_*)
  -> seed_L_V = _build_seed_L_V(seed_T, seed_I, seed_Q_cell)
       -> _n_factor(tr, T)
       -> _resolve_lag_length(tr, T, I, Q_cell, n_j, sigma_d=+1)
            -> _chi_and_dH_eff -> _chi_d -> chi_split(func_chi_d 기본)
            -> func_L_q -> L_q
            -> L_V = |dVdq_qa| * L_q

equilibrium(V_n, T)
  -> Cbg baseline
  -> per transition:
       U_j = func_U_j(T, dH_rxn, dS_rxn) 또는 tr['U']
       n_j = _n_factor(tr, T)
       w = _width(tr, T) = func_w(T, n_j)
       ksi_eq = func_ksi_eq(T, V_n, U_j, n_j, s=+1 기본)
       dQ/dV += Q_j * ksi_eq * (1 - ksi_eq) / w
  -> 평형 curve

dqdv(V_app, T, I_abs, Q_cell, s)
  -> sigma_d = +1/-1
  -> V_n = V_app - sigma_d * |I| * Rn
  -> V_work padded grid, T_work interpolation 또는 scalar 확장
  -> Cbg baseline
  -> per transition:
       U_j(T_work)
       center = U_j + hys_shift
          hys_shift = func_U_branch(T_rep, 0, Omega, gamma, sigma_d, h_eta)
          func_U_branch -> func_dU_hys
       n_j, w
       ksi_eq = func_ksi_eq(T_work, V_work, center, n_j, sigma_d)
       lag_len_V = _resolve_lag_length(...)
       if lag_len_V is nonfinite/sub-grid:
           peak_shape = ksi_eq * (1 - ksi_eq) / w
       else:
           occ_lagged = _causal_lowpass(ksi_eq, grid_step, lag_len_V)
                      또는 charge 방향에서는 reverse-lowpass-reverse
           peak_shape = (ksi_eq - occ_lagged) / lag_len_V
       dqdv_work += Q_j * peak_shape
  -> np.interp(V_n, V_work, dqdv_work)
  -> dQ/dV curve

curve(V_app, direction, c_rate, Q_cell, T, I_abs)
  -> _direction_to_sigma(direction)
  -> I_use = I_abs 또는 c_rate * Q_cell
  -> dqdv(...)
```

### 1.2 함수별 물리식과 줄 근거

| 함수/메서드 | 줄 근거 | 물리식/역할 | 데이터 흐름 |
|---|---:|---|---|
| `func_w(T, n)` | 74-75 | 폭 `w = nRT/F`. | `_width`가 호출해 `ksi_eq`와 평형 피크 분모에 사용. |
| `func_U_j(T, dH_rxn, dS_rxn)` | 78-79 | 평형 중심 `U_j(T)=(-ΔH_rxn + TΔS_rxn)/F`. | `equilibrium` 359-362, `dqdv` 432-436에서 `U_j` 산출. |
| `func_U_j_hys(T, U_j, Omega, gamma, s, ...)` | 82-91 | `Ω<=2RT`면 gap 0, 아니면 `u=sqrt(1-2RT/Ω)`, `ΔU_hys=(2/F)(Ωu-2RT artanh u)`, 반환 `U_j+0.5*s*gamma*ΔU_hys`. | 클래스 본류에서는 직접 호출되지 않음. `func_dU_hys`와 `func_U_branch`가 같은 물리를 공개 헬퍼로 재구성. |
| `func_ksi_eq(T, V_n, U, n, s)` | 94-97 | `z=s(V_n-U)/w`, `ξ_eq=logistic(z)`. `z>=0`/`z<0` 분기로 overflow 완화. | `equilibrium` 365, `dqdv` 455에서 점유율 생성. |
| `func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)` | 100-107 | `I<=0`이면 `-inf`; 그 외 `T_attempt=(I/Q_cell)h/kB`, `dG_a=dH_a-TdS_a`, `ln L_q=ln(T_attempt/T)-ln(1+exp(-A/RT))+dG_a/RT-xA/RT`, `L_q=exp(ln L_q)`. | `_resolve_lag_length` 341-347에서 `x=χ_d`, `dH_a=dH_a_eff`, `L_V=|dVdq_qa|L_q`. |
| `_causal_lowpass(source_signal, grid_step, lag_length)` | 110-128 | 인과 지수기억 필터. `lag_length<=0` 또는 비유한이면 원 신호 복사. SciPy `lfilter` 우선, 실패 시 재귀식 `r_i=a r_{i-1}+(1-a)source_i`. | `dqdv` 470-473에서 동역학 꼬리 점유율 `occ_lagged` 산출. |
| `func_dU_hys(T, Omega)` | 133-140 | `Ω<=2RT`면 `0`, 아니면 `ΔU_hys=(2/F)(Ωu-2RT artanh u)`. | `func_U_branch` 148에서 히스테리시스 분기 중심 이동량에 사용. |
| `func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta)` | 143-148 | `U_j^d = U_j + 0.5 σ_d h_eta γ ΔU_hys`. | `dqdv` 444-448에서 `U_j` 배열에 상수 `hys_shift` 가산. |
| `func_dH_a_eff(dH_a, Omega, chi_d)` | 152-155 | `ΔH_a^eff = ΔH_a - χ_d Ω`. | `_chi_and_dH_eff` 297-300에서 꼬리 장벽 보정. |
| `func_chi_d(chi, sigma_d)` | 158-163 | 방향별 전달계수: 방전 `χ_d=χ`, 충전 `χ_d=1-χ`. | 생성자 기본 `chi_split` 224, `_chi_d` 287-290에서 호출. |
| `_finite`, `_finite_pos`, `_finite_nonneg` | 167-188 | 유한성, 양수, 비음수 입력 가드. | 생성자, `dqdv`, `curve`, `_resolve_lag_length`에서 분모/지수/입력 보호. |
| `__init__` | 221-259 | 전이 목록과 전역 피팅/수치 파라미터 저장, `chi=None`이면 `x`, `seed_L_V` 생성. | 모든 계산의 상태 저장. `transitions` 자체는 복사하지 않고 참조 보존. |
| `_build_seed_L_V` | 262-269 | seed 조건에서 전이별 대표 `L_V`를 방전 기준으로 계산. | 진단/초기값용 `self.seed_L_V`; 실제 `dqdv`는 호출 조건으로 재산출. |
| `_n_factor(tr, T)` | 272-278 | 폭 다중도: `'n'` 우선, 없으면 `'w'F/(RT)`, 둘 다 없으면 1. | `_width`, `_build_seed_L_V`, `equilibrium`, `dqdv`에서 사용. `GRAPHITE_STAGING_LIT`는 `'n':1.0` 보유라 `'w'`는 inert 폴백. |
| `_width(tr, T)` | 281-284 | `w=func_w(T, _n_factor(tr,T))`. | 평형 피크 분모와 logistic 폭을 동일하게 묶어 면적 보존. |
| `_chi_d(sigma_d)` | 287-290 | `chi_split(self.chi, sigma_d)`를 float로 반환. | 방향별 꼬리 장벽 계산의 입구. |
| `_chi_and_dH_eff(dH_a, Omega, sigma_d, use_dH_eff)` | 293-300 | `χ_d`와 `ΔH_a^eff`를 한 곳에서 결정. `use_dH_eff=False`면 원 `dH_a`. | `_resolve_lag_length` 337-342에서 사용. |
| `_resolve_lag_length(transition, T, I, Q_cell, n_j, sigma_d)` | 303-347 | 직접 `L_V`가 있으면 사용. 없고 `I<=0` 또는 `dH_a is None`이면 0. 그 외 `A=min(z_cut*n*RT, A_cap_RT*RT)`, `L_q=func_L_q(...)`, `L_V=|dVdq_qa|L_q`. | seed와 실 dQ/dV의 꼬리 길이를 결정. |
| `equilibrium(V_n, T)` | 350-367 | `Cbg + Σ Q_j ξ(1-ξ)/w`. 방향/히스/분극/꼬리 없음. | 평형 baseline curve. |
| `dqdv(V_app, T, I_abs, Q_cell, s)` | 370-480 | 관측 dQ/dV. `V_n=V_app-σ_d|I|R_n`, 히스 분기 중심, 평형 피크 또는 지연 꼬리, 전이 합산, 관측 grid 재보간. | 핵심 forward model. |
| `curve(...)` | 483-508 | 실험 조건 facade. 문자열 방향과 C-rate를 `dqdv` 입력으로 환산. | `direction -> σ_d`, `c_rate*Q_cell -> |I|`. |
| `_direction_to_sigma(direction)` | 510-524 | 문자열/숫자 방향을 방전 `+1`, 충전 `-1`로 환산. | `curve`에서만 호출. |
| `GRAPHITE_STAGING_LIT` | 531-560 | 흑연 staging 초기값 4개: `U/w/Q/Omega/dH_rxn/dS_rxn/n/dH_a/dS_a/dVdq_qa`. | 기본 transitions 후보. |

### 1.3 `GRAPHITE_STAGING_LIT` 입력 흐름

| 전이 | 줄 근거 | 초기 중심/용량 | 코드상 실제 폭 |
|---|---:|---|---|
| stage 4->3 | 532-538 | `U=0.210`, `Q=0.10`, `Ω=6000`, `ΔH_rxn=-11700`, `ΔS_rxn=29`, `ΔH_a=48000`, `dVdq_qa=0.30` | `n=1.0` 존재로 `w=RT/F=0.025691 V @298.15K`; 줄 533의 `w=0.020`은 폴백. |
| stage 3->2L | 539-545 | `U=0.140`, `Q=0.12`, `Ω=8000`, `ΔH_rxn=-13500`, `ΔS_rxn=0`, `ΔH_a=46000` | `n=1.0`; `w=0.025691 V @298.15K`; `w=0.016` inert. |
| stage 2L->2 | 546-552 | `U=0.120`, `Q=0.25`, `Ω=10000`, `ΔH_rxn=-13100`, `ΔS_rxn=-5`, `ΔH_a=44000` | `n=1.0`; `w=0.025691 V @298.15K`; `w=0.014` inert. |
| stage 2->1 | 553-559 | `U=0.085`, `Q=0.50`, `Ω=13000`, `ΔH_rxn=-13000`, `ΔS_rxn=-16`, `ΔH_a=40000` | `n=1.0`; `w=0.025691 V @298.15K`; `w=0.012` inert. |

## 2. 조건 audit

### 2.1 BDD 음극 dQ/dV 물리수식 기반 피팅 함수 충족도

확정:

- 흑연 음극 전용 forward model이다. 클래스명 `GraphiteAnodeDischargeDQDV` 192-219, 데이터셋명 `GRAPHITE_STAGING_LIT` 527-560, 전이 주석의 stage 표기 532-553이 모두 graphite staging을 직접 가리킨다.
- 입력 전위에서 음극 내부 전위/반응 전위로 가는 분극 항은 `V_n = V_app - σ_d |I| R_n`으로 구현되어 있다. 근거: 407-408.
- 평형 피크는 logistic 점유율 미분형 `Q ξ(1-ξ)/w`다. 근거: `func_ksi_eq` 94-97, `equilibrium` 363-366, `dqdv` 462-465.
- 히스테리시스는 `Ω`, `γ`, `h_eta`, `σ_d`를 통해 분기 중심만 이동시킨다. 근거: 133-148, 438-448.
- 동역학 꼬리는 `ΔH_a`, `dS_a`, `χ_d`, `Ω`, `z_cut`, `A_cap_RT`, `dVdq_qa`, `I`, `Q_cell`, `T`를 통해 `L_q -> L_V`로 들어간다. 근거: 303-347.
- 충전/방전 신호 체인은 `curve -> _direction_to_sigma -> dqdv -> sigma_d`로 정합된다. 근거: 501-508, 510-524, 388.
- LCO 양극, reversible heat `q_rev`, 전자 엔트로피 `dS_e`는 구현 대상에 없다. `rg "LCO|q_rev|dS_e"` 기준 근거 미발견. 코드에 있는 `dS_rxn`, `dS_a`는 각각 평형 중심과 활성화 자유에너지 항이다.

충족도 판단:

- `equilibrium`과 저율 `dqdv`는 BDD 음극 dQ/dV 피팅 함수로 쓸 수 있다. 피크 위치(`U_j`), 폭(`n_j`), 면적(`Q_j`), 배경(`Cbg`)이 분리되어 있고 줄 350-367에서 닫힌 형태가 명확하다.
- 유한 전류 효과도 forward model로 사용할 수 있다. 단 기본 `GRAPHITE_STAGING_LIT`의 동역학 seed `L_V`는 `4.91e-08`, `1.47e-08`, `4.37e-09`, `4.75e-10 V`로 매우 작아 일반 grid에서는 줄 462-465의 sub-grid 판정에 걸려 평형 피크로 접힌다. 실제 꼬리 피팅을 하려면 `L_V` 직접 지정 또는 `dH_a/dS_a/dVdq_qa/z_cut/A_cap_RT/chi/use_dH_eff` 재조정이 필요하다.

### 2.2 None/0 가드와 의도 흐름 차단

확정:

- `func_L_q`는 `I<=0`이면 `-inf`를 반환한다. 근거: 100-107. 그러나 정상 호출 체인에서는 `_resolve_lag_length`가 먼저 `I<=0`을 잡아 `0.0`을 반환한다. 근거: 319-320. 따라서 `func_L_q`의 `I<=0` 분기는 직접 호출 방어에 가깝고, 클래스 내부에서는 사실상 도달하지 않는다.
- `_resolve_lag_length`는 `transition.get('dH_a') is None`이면 `0.0`을 반환해 꼬리를 끈다. 근거: 319-320. `dH_a=0.0`은 None이 아니므로 막히지 않는다.
- `dVdq_qa`가 없으면 기본 `0.0`으로 처리되어 `L_V=0`이 된다. 근거: 346-347. 이는 오류 없이 꼬리를 제거한다.
- 직접 `L_V=0.0`은 합법이고, `dqdv`에서 `lag_len_V < min_lag_grid_steps*grid_step` 판정으로 평형 피크로 접힌다. 근거: 313-318, 462-465.
- `gamma=0.0` 또는 `Omega<=0.0`이면 히스테리시스 branch shift가 제거된다. 근거: 441-450.

결함/주의:

- `dH_a` 누락과 `dVdq_qa` 누락은 동역학 꼬리 비활성화를 조용히 만든다. 피팅 파이프라인에서 "꼬리를 피팅하려고 했는데 키 하나가 빠진 경우"를 오류로 잡지 못한다. 분석상 결함 후보다.
- `L_V` 직접 지정은 동역학 전체를 우회한다. 이는 테스트/피팅 핸들로 유용하지만, `dH_a`, `chi`, `Omega`, `z_cut`, `dVdq_qa`와 동시에 지정하면 후자들은 꼬리 길이에 반영되지 않는다. 근거: 313-318이 가장 먼저 return.
- `Cbg` callable 출력의 유한성 검사는 없다. 주석도 사용자 책임으로 둔다. 근거: 236, 426-429.

### 2.3 死코드/비활성 경로

확정:

- `func_U_j_hys`는 클래스 본류에서 호출되지 않는다. 동일 물리는 `func_dU_hys`와 `func_U_branch`로 활성화되어 있다. 근거: 82-91, 133-148, 444-448.
- `_build_seed_L_V`는 생성자에서 `self.seed_L_V`를 만들지만, 실제 `dqdv` 계산은 매 호출 `_resolve_lag_length`로 다시 산출한다. 근거: 256-269, 457-460. 따라서 `seed_L_V`는 진단/초기값 성격이고 forward curve에는 직접 영향이 없다.
- `func_L_q`의 `I<=0 -> -inf` 분기는 클래스 내부 정상 경로에서는 `_resolve_lag_length`의 선행 return 때문에 비활성이다. 근거: 102-103, 319-320.
- `last_eta`, `last_rest`는 `func_U_j_hys` 시그니처에만 있고 함수 내부에서 쓰이지 않는다. 근거: 82-91.

판단:

- 위 항목은 실행 오류를 만드는 死코드는 아니다. 다만 분석 문건에서 "원형 보존/호환용 비활성 함수"와 "실제 forward chain"을 분리해야 한다.

### 2.4 시그널/호출체인 정합

확정:

- `curve("discharge")`는 `+1`, `curve("charge")`는 `-1`로 변환된다. 근거: 515-520.
- 숫자 방향은 `>=0`이면 `+1`, `<0`이면 `-1`이다. 근거: 523-524. `direction=0`은 방전으로 해석된다.
- `dqdv`는 `s>=0`이면 `sigma_d=+1`, 아니면 `-1`이다. 근거: 388. 따라서 `curve`와 직접 `dqdv`의 방향 규약은 일치한다.
- 방전에서는 lowpass가 오름차순 전압 진행 방향으로 적용되고, 충전에서는 배열을 뒤집어 적용한 뒤 되돌린다. 근거: 467-473.
- 자체 실행 검증에서 `curve(dis,0.2C)`와 `dqdv(I=0.2,s=+1)`의 최대 차이는 `0.00e+00`이었다.

주의:

- `equilibrium`은 `func_ksi_eq`의 기본 `s=+1`만 사용한다. 근거: 365. 평형 피크 모양은 방향 불변이지만, `ξ` 자체의 증가 방향은 방전 convention으로 고정되어 있다.
- `dqdv`의 히스테리시스 shift는 `T_rep=mean(T_work)` 기준 상수다. 비등온 `T(V)`에서 `U_j(T_work)`는 배열이지만 `ΔU_hys`는 대표 온도로만 계산된다. 근거: 426, 444-448. 비등온 branch gap의 국소 온도 의존은 미구현이다.

### 2.5 면적 보존

검산:

- 넓은 범위 `V=-0.5..0.8`, `Cbg=0`, `T=298.15K`에서 `equilibrium` 면적은 `0.969999999913`이고 `ΣQ=0.97`, 오차 `-8.70e-11`이었다.
- 전이별 평형 면적은 각각 `0.1000000000`, `0.1200000000`, `0.2500000000`, `0.4999999999`로 각 `Q_j`와 일치했다.
- 직접 `L_V` 꼬리 단일 전이(`Q=0.5`)도 넓은 grid에서 면적이 `L_V=0.005 -> 0.499675`, `0.02 -> 0.499919`, `0.05 -> 0.499966`로 보존에 근접했다. 잔차는 finite window/interpolation 절단 성격으로 판단된다.

확정:

- 평형식은 폭 `w`가 logistic과 분모에 동일하게 쓰이므로 면적 보존 구조다. 근거: 94-97, 281-284, 363-366.
- 동역학 꼬리는 finite grid/padding에 의존한다. 무한/충분 범위에서는 `ξ_eq - lagged`의 경계 차로 면적이 보존되는 구조이나, 실제 계산은 `grid_pad_lo/hi`와 입력 전압 범위에 따라 작은 손실이 생길 수 있다. 근거: 414-416, 470-479.
- `Cbg`는 별도 배경이므로 전체 적분에는 `Cbg` 면적이 더해진다. 면적 보존 검산은 peak 성분만 분리해야 한다.

### 2.6 부호·차원·극한 적대 검산

부호:

- `V_n=V_app-σ_d|I|Rn`: 방전 `+1`에서 내부 전위가 낮아지고, 충전 `-1`에서 높아진다. 자체 실행에서 방전 `I=1.0` peak가 `0.110 V`, 충전 `I=1.0` peak가 `0.090 V`로 반대 이동했다.
- 히스테리시스 branch: `U_j^d=U_j+0.5σ_d h_eta γ ΔU_hys`. 자체 실행에서 `ΔU_hys=86.7 mV`, 방전-충전 peak 차 `+86.9 mV`로 부호가 식과 맞았다.
- `χ_d`: 방전 `χ`, 충전 `1-χ`. `χ=0.5` 기본에서는 대칭이고, custom split에서 charge `L_V`가 달라지는 검증 출력이 있었다.

차원:

- `w=nRT/F`는 J/mol divided by C/mol = V.
- `U_j=(-ΔH+TΔS)/F`도 J/mol divided by C/mol = V.
- `ΔU_hys=(2/F)(Ωu-2RT artanh u)`는 V.
- `A=z_cut*nRT`와 `A_cap_RT*RT`는 J/mol. `A/(RT)`는 무차원.
- `func_L_q`는 `T_attempt/T`의 log, `dG_a/(RT)`, `xA/(RT)`로 지수부 무차원. 반환 `L_q`는 q축 길이로 해석되고 `dVdq_qa[V] * L_q`가 `L_V[V]`가 된다.

극한:

- `Ω<=2RT`에서 히스 gap 0. 근거: 84-90, 136-140. 자체 실행도 `Omega=2RT -> 0`.
- `γ=0`이면 branch shift 없음. 근거: 441-450. 자체 실행에서 `gamma=0, |I|->0` 방전/충전 최대 차 `5.107e-15`.
- `I_abs=0` 또는 `dH_a` 누락이면 꼬리 없음. 근거: 319-320.
- `lag_len_V`가 sub-grid이면 평형 피크로 환원. 근거: 462-465.
- 온도 `T<=0`, 비유한 `T`, `Q_cell<=0`, `I_abs<0`, 비유한 `L_V`, `z_cut<=0`, 잘못된 방향 문자열은 가드된다. 자체 실행에서 guards `7/7`.

결함 후보:

- `n_safe = abs(n_j)`는 음수 `n`을 꼬리 affinity 계산에서 양수화하지만, `_width`와 `func_ksi_eq`에는 원래 `n`이 들어간다. 근거: 328, 452-455. 사용자가 음수 `n`을 주면 폭 부호와 꼬리 affinity의 해석이 갈라진다. 현재 생성자/전이 가드는 `n` 양수성을 강제하지 않는다.
- `chi` 범위 가드가 없다. `chi<0` 또는 `chi>1`도 `_finite`만 통과한다. 근거: 237, 287-300. 물리적 전달계수로는 범위 제한이 필요할 수 있으나 현재 코드는 확장 callable을 열어둔 형태다.
- `Omega`는 `_resolve_lag_length`에서는 비음수 가드가 있지만 히스테리시스 branch에서는 `Omega>0` 조건만 보고, `func_dU_hys` 직접 호출은 음수에서도 `Omega<=2RT`로 0을 반환한다. 근거: 133-140, 441-450.

## 3. 피팅 파라미터 인벤토리

권고 등급:

- 자유: 데이터에서 직접 식별 가능성이 높아 fit 후보.
- 조건부 자유: 특정 실험 조건 또는 충분한 데이터가 있을 때만 fit.
- 고정/사전값: 초벌 fit에서는 고정하고 후속 민감도 분석 대상.

| 파라미터 | 줄 근거 | 초기값/기본값 | 역할 | 지배 영역 | 초벌 권고 |
|---|---:|---|---|---|---|
| `Q_j` | 204, 533, 540, 547, 554 | `0.10, 0.12, 0.25, 0.50` | 전이별 면적 가중치. | peak 면적, 높이. 폭 고정 시 높이에도 직접 영향. | 자유. 단 `ΣQ`를 전극 용량 또는 정규화 조건에 묶는 제약 권고. |
| `U` | 202, 436, 533, 540, 547, 554 | `0.210, 0.140, 0.120, 0.085 V` | `dH_rxn/dS_rxn`이 없을 때 중심 전위. | peak 위치. | `dH_rxn/dS_rxn`을 쓰지 않는 초벌에서는 자유. 둘을 쓰면 중복이므로 고정/비사용. |
| `dH_rxn` | 202, 433-435, 534, 541, 548, 555 | `-11700, -13500, -13100, -13000 J/mol` | `U_j(T)`의 절편 성격. | 온도별 peak 위치. | 단일 온도 fit에서는 `U_j`와 식별성 중복이 커서 고정. 다온도 데이터에서 조건부 자유. |
| `dS_rxn` | 202, 433-435, 534, 541, 548, 555 | `29, 0, -5, -16 J/mol/K` | `U_j(T)`의 온도 기울기. | 온도 변화에 따른 peak 위치 이동. | 다온도 데이터 전에는 고정. 다온도 peak shift가 충분하면 조건부 자유. |
| `n_j` | 203, 272-284, 534, 541, 548, 555 | 전 전이 `1.0` | `w=nRT/F` 폭 다중도. | peak 폭, peak 높이, 꼬리 affinity `A=z_cut*nRT`에도 영향. | 자유. 양수 제약 필요. |
| `w` | 203, 276-277, 533, 540, 547, 554 | `0.020, 0.016, 0.014, 0.012 V` | `n`이 없을 때만 폭으로 역산되는 폴백. | peak 폭/높이. | 현재 데이터셋에서는 `n` 때문에 inert. 초벌에서는 `n` 또는 `w` 중 하나만 선택. |
| `Omega` | 205, 133-148, 335, 533, 540, 547, 554 | `6000, 8000, 10000, 13000 J/mol` | 히스 gap과 `ΔH_a^eff=ΔH_a-χ_dΩ`에 들어감. | 충/방전 peak split, 꼬리 길이. | 초기에는 고정 또는 조건부 자유. 히스 데이터와 rate 데이터가 모두 있어야 식별 가능. |
| `gamma` | 205, 441-448 | 기본 `0.0`; lit dict에는 없음 | 히스 gap 축소 계수. | 충/방전 peak 위치 분리. | 충방전 pair 데이터가 있으면 자유. 단 `Omega`와 강하게 결합되므로 하나를 고정하고 시작. |
| `h_eta` | 208, 443-448 | 기본 `1.0` | 부분 cycle 히스테리시스 축소. | 히스 분기 위치. | 초벌 고정. 부분 cycle 실험이 있으면 조건부 자유. |
| `dH_a` | 206, 333, 536, 543, 550, 557 | `48000, 46000, 44000, 40000 J/mol` | 꼬리 길이의 Arrhenius 장벽. | rate 의존 꼬리 길이, peak 비대칭/완만한 tail. | rate-series가 있으면 조건부 자유. 단 기본값은 꼬리가 sub-grid라 민감도 확인 필요. |
| `dS_a` | 206, 334, 536, 543, 550, 557 | 전 전이 `0.0` | 활성화 자유에너지 `dG_a=dH_a-TdS_a`. | 온도별 꼬리 길이. | 초벌 고정. 다온도 rate 데이터 전에는 자유화 금지 권고. |
| `chi` / `x` | 210, 213, 234, 237, 287-300 | `x=0.5`, `chi=None -> x` | 방향별 전달계수의 기준값. | 충/방전 꼬리 비대칭, `ΔH_a^eff`. | 초벌 고정 `0.5`. 충/방전 rate tail 비대칭이 뚜렷하면 조건부 자유. 범위 제약 필요. |
| `chi_split` | 214, 224, 238-240, 287-290 | 기본 `func_chi_d` | `χ_d` 규칙 자체를 교체. | 충/방전 꼬리 비대칭 구조. | 초벌 고정. 모델 비교 단계에서만 교체. |
| `use_dH_eff` | 216, 241, 297-300, 338-339 | 기본 `True` | `ΔH_a-χ_dΩ` 보강 on/off. | 꼬리 길이와 `Omega`-동역학 결합. | 모델 선택 스위치로 고정. fit 파라미터처럼 연속 최적화하지 않음. |
| `L_V` | 209, 313-318 | transition별 선택값 없음 | 직접 꼬리 길이 지정. 있으면 동역학 산출 우회. | tail 길이, peak 비대칭. | 초벌 rate-tail fit에서는 `L_V` 직접 자유가 가장 안정적. 물리 파라미터 fit 단계에서는 제거해야 중복 회피. |
| `z_cut` | 217, 242, 329-331 | 전역 `4.357`; per-transition override 가능 | 컷 affinity `A=z_cut*nRT`. | 꼬리 길이 산출, rate tail. | 고정. 데이터로 직접 식별하기 어렵고 `dH_a`, `dVdq_qa`와 결합. |
| `A_cap_RT` | 218, 243, 330-331 | 전역 `4.0`; per-transition override 가능 | affinity 상한 `A<=A_cap_RT RT`. | 꼬리 길이 상한 효과. | 고정. 초벌 자유화 비권고. |
| `dVdq_qa` | 207, 346-347, 536, 543, 550, 557 | 전 전이 `0.30 V` | `L_q`를 `L_V`로 변환하는 컷점 OCV 기울기. | tail 길이. | `L_V` 직접 fit을 쓰지 않는 경우 조건부 자유. `dH_a`와 곱/지수 결합이 강해 단독 식별성 약함. |
| `Rn` | 211, 235, 407-408 | 기본 `0.0`; self-test `0.01` | ohmic 분극. | 전체 peak 위치의 전류 방향별 rigid shift. | rate-series에서 자유. 단 전이별 tail과 분리하려면 고전류/저전류 비교 필요. |
| `Cbg` | 212, 236, 354-356, 426-429 | 기본 `0.0`; self-test `0.05` | 상수 또는 callable 배경 dQ/dV. | baseline, 전체 area offset. | 자유. 상수부터 시작하고 필요 시 smooth callable/저차 basis. |
| `grid_pad_lo`, `grid_pad_hi` | 227, 244-245, 414-416 | `0.15`, `0.15` | 작업 grid padding. | finite tail 면적 손실/경계 artifact. | 수치 파라미터로 고정. 긴 꼬리 fit에서는 검증용 증가. |
| `n_work_min` | 228, 246, 412 | `2048` | 작업 grid 최소 해상도. | sub-grid tail 판정, peak smoothness. | 수치 파라미터로 고정. 해상도 수렴성 검증 대상. |
| `min_lag_grid_steps` | 228, 247, 462 | `2.0` | 너무 짧은 `L_V`를 평형 피크로 접는 threshold. | tail 활성/비활성 경계. | 고정. 아주 짧은 tail 연구 시 민감도 점검. |
| `v_span_floor` | 229, 248, 410-412 | `1e-6` | 전압 span 0 방지. | scalar/좁은 grid 안정성. | 고정. |
| `seed_T`, `seed_I`, `seed_Q_cell` | 230-231, 256-259 | `298.15`, `0.1`, `1.0` | `seed_L_V` 진단 조건. | 실제 curve에는 직접 영향 없음. | 고정 또는 진단용만 조정. |
| `direction`, `c_rate`, `I_abs`, `Q_cell`, `T` | 483-508, 370-405 | 호출 조건 | 실험 조건. | 분극, 꼬리 길이, 온도별 위치/폭. | fit 파라미터가 아니라 실험 메타데이터로 고정. |

초벌 피팅 순서 권고:

1. 저율/평형 데이터: `Cbg`, `Q_j`, `U_j` 또는 `dH_rxn/dS_rxn` 환산 중심, `n_j`만 자유화한다. 현재 lit dict는 `n=1.0` 때문에 `w` 초기값이 작동하지 않으므로 `n`을 명시적으로 다룬다.
2. 충/방전 pair: `Rn`, `gamma`를 추가한다. `Omega`는 고정하고 `gamma`를 먼저 fit하거나, 반대로 `gamma=1` 가정 후 `Omega`만 움직여 식별성 붕괴를 피한다.
3. rate-series tail: 먼저 `L_V` 직접 fit으로 전이별 꼬리 길이의 관측 가능성을 확인한다. 이후 `L_V`를 제거하고 `dH_a`, `dVdq_qa`, `chi`, `z_cut` 물리 파라미터로 환산한다.
4. 다온도 rate-series: `dS_rxn`, `dS_a`, `use_dH_eff/Omega` 결합을 검토한다. 단일 온도에서는 이들을 자유화하면 과적합 가능성이 크다.

## 4. 실행 검증 기록

- `python Claude\docs\v1.0.10\Anode_Fit_v1.0.10.py`: `overall OK: True`, guards `7/7`, `curve(dis,0.2C) == dqdv(...)` max diff `0.00e+00`, 히스 split `86.9 mV` vs expected `86.7 mV`.
- 면적 검산 1차는 `np.trapz`가 NumPy 2.x에서 제거되어 실패했다. 같은 계산을 `np.trapezoid`로 재실행해 성공.
- `np.trapezoid` 검산: `ΣQ=0.97`, 평형 면적 `0.969999999913`, 오차 `-8.70e-11`.
- `rg "LCO|q_rev|dS_e"`: 근거 미발견.

## 5. 결론

확정:

- 이 코드는 흑연 음극 staging dQ/dV forward model이며, LCO 양극, `q_rev`, `dS_e` 발열/전자엔트로피 모델은 포함하지 않는다.
- 평형 dQ/dV는 면적 보존 구조로 구현되어 있고 수치 검산도 `ΣQ`와 일치한다.
- 충/방전 방향, 분극, 히스테리시스 branch, 동역학 꼬리 호출체인은 코드상 연결되어 있다.
- 기본 lit 초기값에서는 `n=1.0`이 `w`보다 우선하므로 주석의 `w` 값들은 현재 폭 피팅 초기값으로 작동하지 않는다.

추정/주의:

- 기본 동역학 파라미터의 `L_V`는 매우 작아 실사용 grid에서 꼬리가 거의 평형 피크로 환원된다. rate tail 피팅을 목표로 하면 `L_V` 직접 fit 또는 동역학 파라미터 재스케일이 필요하다는 판단은 검산에 근거한 추정이다.
- `dH_a` 누락, `dVdq_qa` 누락, `L_V=0`은 오류가 아니라 조용한 꼬리 비활성화로 이어진다. 자동 피팅 파이프라인에서는 결함 후보로 취급하는 것이 안전하다.
