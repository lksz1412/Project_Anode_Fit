# V1010 P2 Draft C2 — Ch1 교과서화 supplement

역할: Anode_Fit v1.0.10 P2 챕터1 경쟁 드래프트 C2(Codex).  
범위: 드래프트 supplement 작성 전용. 원본 `.tex`, 코드, 기존 process/research 문건 수정 없음.  
출력: `Claude/results/process/V1010_P2_draft_C2.md`.

## 0. 입력 정독 범위

직접 읽은 입력:

| 입력 | 실제 확인 범위 | 용도 |
|---|---:|---|
| `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` | 1--1866행 | Ch1 본문 절, 식 번호, LCO 절, broadening 절, node map 확인 |
| `Claude/results/process/V1010_P1_code-audit_RESULT.md` | 1--445행 | 코드 플로우차트, 24심볼, 12식, parameter inventory ground truth |
| `Claude/results/research/broadening_w_design.md` | 1--44행 | broadening, w 이중지위, w_eff 제거, scope guard |
| `Claude/results/research/radius/ORIGIN_VERDICT.md` | 1--79행 | delta-to-bell 원인, apparent-U/eta, size/PSD 구분, DOI 근거 |

주의: 본 supplement는 P1 audit를 코드 ground-truth anchor로 삼는다. 실제 코드 파일은 이번 P2 입력 목록에 없으므로, 코드 줄 번호와 구현 판정은 P1 result의 직접 검증 결과를 인용한다.

## 1. Ch1 ↔ 코드 1:1 coverage matrix

판정 표기:

- `covered`: 코드 step이 Ch1의 절과 식으로 교과서적으로 설명됨.
- `partial`: Ch1에 식은 있으나 코드 branch, 우선순위, guard, fitting implication이 덜 드러남.
- `code-only`: 구현 보조, guard, diagnostic, dead path라 본문 물리식의 주대상이 아님.
- `theory-only`: Ch1에는 있으나 v1.0.10 코드에는 아직 구현되지 않음. P4 구현 대상.

| P1 코드 step / 심볼 | P1 구현 anchor | Ch1 절·식 anchor | coverage | 갭 또는 보완 방향 |
|---|---|---|---|---|
| `curve`, `_direction_to_sigma` | N0, L483--524 | §1.1, eq:n0map; tab:nodemap N0 | covered | `curve`는 새 물리 없음. facade라는 성격을 Ch1 §facade가 설명함. |
| 입력 방향 `sigma_d`, C-rate→`I_abs` | P1 §1.1, §1.3 | eq:n0map | covered | 방향 부호의 세 작용처가 Ch1 §notation에 있음. |
| 분극 `V_n=V_app-sigma_d|I|Rn` | P1 §2-A L408 | §pol, eq:vn | covered with line drift | Ch1 tab:nodemap은 `dqdv L412`라고 쓰지만 P1 ground truth는 L408. 물리식은 일치하나 line citation은 통합 시 보정 후보. |
| 작업 격자 `V_work`, `T_work`, `n_work=max(n_work_min,2|V_n|)` | P1 §1.1, §1.3, 보완3 | §pol, eq:vwork | partial | Ch1은 격자를 설명하나, `n_work`가 `L_V<nu*grid_step` branch threshold를 데이터 점수에 종속시키는 fitting implication은 matrix/보완 초안에서 더 명시 필요. |
| `func_U_j` | L78--79 | §center, eq:Uj | covered | Gibbs→chemical potential→`U_j(T)` 사슬이 닫힘. |
| `func_U_j_hys` | L82--91, dead | Ch1 주 경로 없음. 동일 수식은 eq:dUhys/eq:Ubranch | code-only / partial | 함수 자체는 dead helper. 본문에는 live helper `func_dU_hys`, `func_U_branch`만 대응. supplement에서 dead/live 분리 필요. |
| `func_dU_hys` | L133--140 | §hys, eq:spinodal, eq:dUhys | covered | `Omega<=2RT` 극한, 차원, Taylor 극한까지 설명됨. |
| `func_U_branch` | L143--148 | §hys, eq:Ubranch, eq:center | covered | 부호 관례는 Ch1에서 방전 `+`, 충전 `-`로 설명됨. |
| `func_w`, `_width` | L74--75, L281--284 | §width, eq:wbase | covered | 식 자체는 충분. |
| `_n_factor`: `'n'` 우선, 없으면 `'w'` 역산 | L272--278 | §width 711--739; §broadening 1194--1197; tab:inputs | partial | Ch1은 `n=1`이면 `w` 폴백이 비활성임을 broadening 안에서 말하지만, code decision tree로는 덜 보임. 1:1 coverage 표에 별도 보완 필요. |
| `func_ksi_eq` logistic | L94--97 | §width, eq:bv, eq:db, eq:xieq; §dist | covered | detailed balance와 grand-canonical 분포 다리가 모두 있음. |
| `equilibrium` | L350--367 | §eqpeak, eq:eqpeak; §facade | covered / partial | 평형 peak 식은 covered. 단 P1 보완2의 `equilibrium`은 T scalar only이고 dqdv는 T array 지원이라는 API 차이는 Ch1에 짧게만 있음. |
| 평형 peak `Q_j xi(1-xi)/w` | L366, L464 | eq:eqpeak | covered | 면적=Q 해석 있음. |
| `Cbg` background | L427, L354--357 | eq:vwork, eq:sum, tab:inputs | partial | 물리 위치는 covered. callable finite 검증 부재(F4)는 Ch1보다 fitting wrapper 보완 사항. |
| `_resolve_lag_length` decision tree | L303--347 | §lag, eq:Acut--eq:LV | partial | 핵심식은 covered. 그러나 direct `L_V` override, `dH_a is None`, `dVdq_qa=0` silent-off, `z_cut/A_cap` inert 조건은 code branch 표로 더 드러내야 함. |
| cut affinity `A=min(z_cut*nRT,A_cap*RT)` | L329--331 | §lag, eq:Acut | covered | `z_cut=4.357`이 점유율 5%가 아니라 logistic derivative 5% cutoff임을 Ch1이 정확히 서술. |
| `func_chi_d` | L158--163 | §lag, eq:chid | covered | 합-1 detailed balance와 방향별 분할 설명 있음. |
| `func_dH_a_eff` | L152--155 | §lag, eq:dHeff | covered | `use_dH_eff` off 분기도 §lag에서 설명됨. |
| `func_L_q` | L100--107 | §lag, eq:Lq, eq:Lqfull | covered | attempt temperature, Arrhenius, reverse-rate denominator가 식으로 닫힘. |
| `L_V=|dVdq_qa|L_q` | L347 | §lag, eq:LV | covered / partial | 식은 covered. `dVdq_qa` 누락 시 tail silent-off는 fitting guard로 보완 필요. |
| `_causal_lowpass` | L110--128 | §tail, eq:lowpass | covered / partial | 점화식은 covered. P1의 DC gain=1과 면적보존 proof는 Ch1에서 더 짧음. supplement에 교재식 증명 추가 권고. |
| tail peak `(xi_eq-xi_lag)/L_V` | L475 | §tail, eq:peakshape | covered | `L_V→0`은 식 극한이 아니라 branch switch라는 정정도 있음. |
| branch switch `L_V<nu grid_step` | L462--475 | §tail, eq:branch | covered / partial | 불연속은 설명됨. `grid_step`이 `n_work`와 입력 V count에 연결되는 실용 영향은 보완 필요. |
| charge grid reversal | L470--473 | §tail, eq:reversal | covered | 인과 방향과 mirror sign이 설명됨. |
| summation and interpolation | L477--480 | §sum, eq:sum | covered | 배경+전이합+역보간 설명 있음. |
| `GRAPHITE_STAGING_LIT` | L531--560 | tab:staging | covered | 초기값이지 신뢰값 아님이 명시됨. |
| `seed_L_V` | L262--269 | tab:inputs only | code-only / partial | 진단·초기값 전용. Ch1 본문 물리 경로가 아니므로 supplement에서 “not model output”으로 분리. |
| finite guards `_finite*` | L167--188 | tab:inputs, 산발적 언급 | code-only | 물리 교과서 본문보다 implementation contract. fitting supplement에 guard table로 두는 것이 적절. |
| self-test | L567--703 | sign self-test §signcheck | partial | 부호 검산은 Ch1에 있음. 면적=Q assert 부재는 Ch1이 아니라 P4 test 후보. |
| LCO parameter swap | code에 없음 | §lco-map, tab:lco-staging, eq:msmr | theory-only | P2 이론 기술은 정상. 구현은 P4. |
| LCO electronic entropy plug-in | code에 없음 | §lco-electronic, eq:dSemolar, eq:ggate, eq:lco-decomp | theory-only | Ch1 이론은 있음. v1.0.10 코드에는 LCO/electronic entropy 없음. P4에서 `Delta S_e^mol` slot 구현 필요. |
| heat / reversible heat | code에 없음 | Ch1에서 Ch2 후속 언급 | out of scope | P1도 발열 부재 확정. Ch1에서는 Ch2 확장 예고만 유지. |

## 2. Parameter coverage matrix

### 2.1 주 파라미터 8종

| 파라미터 | 코드 지배영역(P1) | Ch1 anchor | coverage | 보완 |
|---|---|---|---|---|
| `U_j` / `dH_rxn,dS_rxn` | peak 위치 | eq:Uj, tab:staging | covered | LCO는 같은 식, 값만 양극 영역으로 교체. |
| `n_j` | 폭, `w=nRT/F` | eq:wbase, §width | partial | `n>0` fitting bound와 `'n'` 우선순위를 explicit rule로 보완. |
| `Q_j` | 면적/높이 | eq:eqpeak, eq:sum | covered | `area=Q_j` proof는 eq:eqpeak에 있음. |
| `Omega_j` | hys gap, `dH_a_eff` | eq:dUhys, eq:dHeff | covered | `Omega<=2RT` gap 0, `gamma=0 or Omega=0` branch no shift를 같이 표기. |
| `dH_a` | tail length exponential | eq:Lqfull | covered | 단일온도 과식별 경고 보완. |
| `chi` | tail charge/discharge asymmetry | eq:chid | partial | `[0,1]` bound는 Ch1보다 fitting guard 성격. |
| `L_V` direct | tail direct override | eq:LV, §lag line 1435 | partial | direct override가 `dH_a/chi/Omega/z_cut/dVdq_qa`를 우회한다는 code branch를 보완. |
| `dVdq_qa` | `L_q→L_V` voltage scale | eq:LV | partial | 누락 기본값 0이 tail silent-off를 만든다는 fitting guard 보완. |

### 2.2 보조 파라미터 10종과 수치 제어

| 파라미터 | Ch1 anchor | coverage | 보완 |
|---|---|---|---|
| `Delta H_rxn` | eq:Uj, tab:staging | covered | 단온도에서는 `U`와 중복. |
| `Delta S_rxn` | eq:Uj, eq:lco-dUdT | covered | LCO에서는 config+vib+electronic 분해. |
| `gamma` | eq:Ubranch, eq:center | covered | `gamma=0`이면 no shift. |
| `h_eta` | eq:Ubranch | covered | 부분 cycle data 없으면 fixed. |
| `dS_a` | eq:Lqfull | covered | 다온도 rate-series 전에는 과식별. |
| `z_cut` | eq:Acut | covered | derivative 5% cutoff. `n=1,z_cut>=A_cap` 조건에서 capped inert. |
| `A_cap_RT` | eq:Acut | covered | default 4.0RT cap. |
| `use_dH_eff` | eq:dHeff discussion | covered | 모델 선택 스위치. |
| `Rn` | eq:vn | covered | rate-series IR shift. |
| `Cbg` | eq:vwork, eq:sum | partial | callable finite guard는 wrapper 보완. |
| `grid_pad_lo/hi` | eq:vwork | covered | edge loss mitigation. |
| `n_work_min` | eq:vwork, eq:branch via grid step | partial | branch threshold 해상도 의존성 보완. |
| `min_lag_grid_steps` | eq:branch | covered | discontinuous mode switch 명시됨. |
| `seed_T/I/Q_cell` | tab:inputs | code-only | diagnostic only; forward `dqdv`는 호출 조건으로 재계산. |

## 3. 누락 유도·다리 보완 초안

### 3.1 code decision tree bridge: live physics vs implementation branches

Ch1 본문은 N0--N9 물리식의 교과서식 유도에 강하다. supplement에서 보강할 첫 다리는 “식 하나가 코드 branch로 어떻게 구현되는가”이다. 다음 decision tree를 Ch1 부록 또는 process supplement에 넣으면 P1의 코드 flowchart와 본문 수식이 1:1로 닫힌다.

```text
per transition j:
  n_j:
    if 'n' in transition:        n_j = transition['n']
    elif 'w' in transition:      n_j = w F/(RT)
    else:                       n_j = 1

  U_j(T):
    if dH_rxn,dS_rxn present:    U_j=(-dH_rxn+T dS_rxn)/F
    else:                       U_j=transition['U']

  branch center:
    if gamma != 0 and Omega > 0: center=U_j+0.5 sigma_d h_eta gamma Delta U_hys
    else:                       center=U_j

  lag length:
    if 'L_V' present:            L_V = explicit override
    elif I<=0 or dH_a missing:   L_V = 0
    else:
      A=min(z_cut |n_j| RT, A_cap RT)
      chi_d=chi if discharge else 1-chi
      dH_a_use=dH_a-chi_d Omega if use_dH_eff else dH_a
      L_q=(T*/T) exp[(dH_a_use-T dS_a)/RT] exp[-chi_d A/RT]/(1+exp[-A/RT])
      L_V=|dVdq_qa| L_q

  peak_shape:
    if L_V < min_lag_grid_steps grid_step or nonfinite: xi_eq(1-xi_eq)/w
    else if discharge:                                  (xi_eq-lowpass(xi_eq))/L_V
    else charge:                                       (xi_eq-lowpass(reverse(xi_eq)) reversed)/L_V
```

여기서 중요한 교과서적 메시지는 “모든 branch가 새 물리를 뜻하지 않는다”이다. `L_V` 직접 지정은 물리식을 우회하는 fitting shortcut이고, `dH_a` 누락 또는 `dVdq_qa=0`은 tail off 상태다. `seed_L_V`는 diagnostic seed라 forward curve의 실제 `L_V`가 아니다.

### 3.2 `n` vs `w` bridge

현재 Ch1은 폭의 이중지위는 잘 설명하지만, 코드의 key priority는 한 문장으로는 부족하다. 보완 문단 초안:

> 코드의 폭 입력은 `w`가 아니라 최종적으로 `n_j`이다. 전이 dict에 `n`이 있으면 `w`는 읽히지 않고, `w`는 `n`이 없을 때만 `n=wF/(RT)`로 역산되는 fallback이다. 따라서 `GRAPHITE_STAGING_LIT`처럼 모든 전이에 `n=1`과 `w=...`가 같이 들어 있으면 실제 폭은 `w=RT/F`이고, 표의 `w=0.020/0.016/0.014/0.012 V`는 비활성 초기 메모다. 피팅에서 두-상 폭을 현상학적으로 줄이거나 늘리려면 `n`을 직접 움직이거나 `n`을 제거하고 `w` fallback을 활성화해야 한다. 물리적 bound는 `n>0`; `n<=0`은 logistic 폭의 차원은 맞아도 확률분포와 positive dQ/dV를 깨뜨린다.

### 3.3 lowpass DC gain and area bridge

P1은 `_causal_lowpass`의 DC gain=1과 면적보존을 중요한 확정 사항으로 둔다. Ch1 §tail은 점화식을 제공하므로 다음 4줄 증명을 붙이면 area bridge가 닫힌다.

저역통과 점화식

```math
y_i=\rho y_{i-1}+(1-\rho)x_i,\qquad 0<\rho<1
```

의 z-transform은

```math
H(z)=\frac{Y(z)}{X(z)}=\frac{1-\rho}{1-\rho z^{-1}}.
```

DC gain은 `z=1`에서

```math
H(1)=\frac{1-\rho}{1-\rho}=1.
```

따라서 충분히 넓은 전압창에서 `xi_lag`는 `xi_eq`와 같은 총 step height를 갖고, `(\xi_eq-\xi_lag)/L_V`로 만든 tail kernel의 전체 전하 면적은 경계 절단을 제외하면 보존된다. 면적 손실이 생기면 물리식이 아니라 finite voltage window / padding 문제로 분리해 검산해야 한다.

### 3.4 branch discontinuity and grid-resolution bridge

Ch1 eq:branch는 “작은 `L_V`는 식의 극한이 아니라 branch switch로 평형종에 떨어진다”고 정확히 쓴다. 여기에 P1 보완3을 연결하는 문단:

> switch threshold는 `L_V < nu Delta_grid`이고, `Delta_grid`는 `V_work` span과 `n_work=max(n_work_min, 2|V_n|)`로 정해진다. 그러므로 같은 물리 파라미터가 만든 같은 `L_V`라도 사용자가 넣은 전압점 수와 전압 span에 따라 `tail branch`와 `equilibrium branch`가 갈릴 수 있다. 이 의존성은 물리 파라미터가 아니라 수치해상도 의존성이다. rate-tail 피팅에서는 `n_work_min`, `min_lag_grid_steps`, voltage span을 고정하거나, branch boundary 근처의 parameter set을 별도 표시해야 한다.

### 3.5 dead helper bridge

`func_U_j_hys`는 원형 보존 dead helper이고, live path는 `func_dU_hys` + `func_U_branch`이다. Ch1 본문은 live path 중심이라 적절하다. 다만 1:1 coverage를 요구하면 다음 주석이 필요하다.

> 코드에는 `func_U_j_hys(T,U_j,Omega,gamma,s,last_eta,last_rest)`가 남아 있으나, 클래스 forward path와 self-test에서는 호출되지 않는다. 같은 gap 수식은 `func_dU_hys`가 계산하고, 실제 branch center는 `func_U_branch`가 만든다. 따라서 교과서 본문은 `func_U_j_hys`를 독립 물리식으로 다시 유도하지 않고, “동일 수식을 담은 미호출 원형 helper”로만 표기한다. `last_eta`, `last_rest`, 내부 `partial_hys=1.0`은 live model parameter가 아니다.

### 3.6 fitting guard bridge

본문 수식은 물리식을 닫지만 optimizer가 자유 탐색할 때의 guard는 별도 계층이다. supplement 표:

| guard | 이유 | 적용 위치 |
|---|---|---|
| `n_j>0` | `w=nRT/F`가 양수여야 logistic derivative가 positive peak | fitting bounds |
| `0<=chi<=1` | transition-state splitting fraction | fitting bounds |
| dynamic transition이면 `dVdq_qa>0` | `dVdq_qa=0`은 tail silent-off | schema validation |
| callable `Cbg(V)` finite | NaN/inf baseline이 전체 곡선 오염 | wrapper output check |
| direct `L_V`와 physical tail params 동시 자유화 금지 | `L_V` override가 `dH_a,chi,Omega,z_cut,dVdq_qa` 우회 | parameterization choice |
| `Omega`와 `gamma` 동시 자유화 제한 | branch split은 주로 product-like sensitivity | staged fitting |

## 4. LCO 이론 정련안

### 4.1 현재 Ch1 LCO 절의 타당성

확정:

1. Ch1은 LCO를 현재 v1.0.10 코드 구현으로 주장하지 않는다. Ch1은 흑연 forward 골격을 LCO half-cell에 이론적으로 거는 구조이며, P1은 코드에 LCO·발열·전자엔트로피가 없음을 확정했다.
2. LCO의 기본 logistic transition skeleton은 흑연과 동형이다. `U_j(T)`, `w_j`, `xi_eq`, `Q_j xi(1-xi)/w`, hys branch, summation은 전극 종류에 의존하지 않는 삽입형 전극 골격이다.
3. LCO의 고유 보강은 T1 MIT 구간의 electronic entropy plug-in이다. Ch1은 Sommerfeld 함수형, MIT logistic gate, molar conversion, config+vib+electronic decomposition을 이미 가진다.
4. 코드 구현은 P4로 예고해야 한다. P2에서 LCO code path가 있는 것처럼 쓰면 P1 ground truth와 충돌한다.

미검증 또는 주의:

- LCO `g(E_F,x)`의 연속 곡선은 1차 문헌 anchor 한 점과 MIT 구간 정성 추세를 바탕으로 둔 model assumption이다. 함수형과 anchor, transition shape의 신뢰등급을 분리해야 한다.
- `Delta S_e`의 단위는 자리당 식과 몰당 forward slot을 반드시 분리해야 한다. P4 구현에서 `N_A` 및 eV→J conversion 누락은 치명적이다.
- LCO broadening에 흑연 turbostratic 비-크기 heterogeneity 근거를 그대로 이식하면 안 된다. Ch1도 LCO에는 일반 eta 분포로만 둔다.

### 4.2 교재급 LCO 전자 엔트로피 식 사슬

Fermi--Dirac 분포:

```math
f(E)=\frac{1}{1+\exp[(E-E_F)/(k_BT)]}.
```

축퇴 금속에서 `g(E)`를 Fermi 준위 근방 열폭 `~kBT` 안에서 `g(E_F,x)`로 동결하면 Sommerfeld 전개로

```math
C_e(T,x)=\frac{\pi^2}{3}k_B^2Tg(E_F,x),
```

이고

```math
S_e(T,x)=\int_0^T \frac{C_e(T',x)}{T'}\,dT'
=\frac{\pi^2}{3}k_B^2Tg(E_F,x).
```

이 식의 `g(E_F,x)`가 `J^{-1}` per site 단위일 때 `S_e`는 site당 `J/K`이다. 문헌값이 `e/eV/atom`이면

```math
g_J(E_F,x)=\frac{g_{\mathrm{eV}}(E_F,x)}{1.602176634\times10^{-19}}\quad[J^{-1}\ \mathrm{site}^{-1}]
```

로 변환한 뒤 써야 한다.

forward slot은 삽입 반응 엔트로피의 몰당 값이므로

```math
\Delta S_{e}^{\mathrm{mol}}(x,T)
=N_A\frac{\partial S_e}{\partial x}\Big|_T
=\frac{\pi^2}{3}Rk_BT\frac{\partial g_J(E_F,x)}{\partial x}.
```

MIT logistic gate를

```math
g_J(E_F,x)=g_{J,\max}\left[1-\sigma\left(\frac{x-x_{\mathrm{MIT}}}{\Delta x_{\mathrm{MIT}}}\right)\right],
\qquad
\sigma(z)=\frac{1}{1+e^{-z}}
```

로 두면

```math
\frac{\partial g_J}{\partial x}
=-\frac{g_{J,\max}}{\Delta x_{\mathrm{MIT}}}\sigma(1-\sigma),
```

따라서 삽입 기준 electronic entropy는

```math
\Delta S_e^{\mathrm{mol}}(x,T)
=-\frac{\pi^2}{3}Rk_BT
\frac{g_{J,\max}}{\Delta x_{\mathrm{MIT}}}
\sigma\left(\frac{x-x_{\mathrm{MIT}}}{\Delta x_{\mathrm{MIT}}}\right)
\left[1-\sigma\left(\frac{x-x_{\mathrm{MIT}}}{\Delta x_{\mathrm{MIT}}}\right)\right] < 0.
```

부호 해석:

- 삽입 기준 `x↑`: MIT metal→insulator 방향이므로 `g(E_F)`가 감소하고 `∂g/∂x<0`, 따라서 `Delta S_e<0`.
- 탈리튬화 기준 `x↓`: electronic entropy가 방출되는 양의 bump는 `-Delta S_e>0`.
- forward `Delta S_rxn` slot은 삽입 기준이므로 부호를 뒤집지 않는다.

온도 의존:

```math
\frac{\partial U_1}{\partial T}\Big|_e
=\frac{\Delta S_e^{\mathrm{mol}}(x,T)}{F}
\propto T.
```

따라서 기준온도 `T0`에서의 electronic contribution 위치 이동은

```math
\Delta U_{1,e}(T)-\Delta U_{1,e}(T_0)
=-\frac{\pi^2}{6F}Rk_B
\frac{g_{J,\max}}{\Delta x_{\mathrm{MIT}}}
\sigma(1-\sigma)\,(T^2-T_0^2),
```

로 `T^2`형이다. 관측 식별 신호는 “peak 위치가 단순 선형”이 아니라 “`partial U/partial T`가 T에 선형”이다.

### 4.3 LCO P4 구현 예고

P4 구현은 다음 최소 구조여야 한다.

1. `LCO_STAGING_LIT`를 별도 전이 dict로 둔다. 키 구조는 graphite와 동일하되 `U`, `dH_rxn`, `dS_rxn`, `Q`, `Omega`, `dH_a`, `dS_a`, `dVdq_qa` 값을 LCO half-cell 초기값으로 둔다.
2. T1 MIT 전이에만 `electronic_entropy` option을 둔다. 기본 off 또는 명시적 model flag가 필요하다.
3. electronic entropy 계산은 반드시 molar slot으로 반환한다: `DeltaS_e_mol = (pi^2/3)*R*kB*T*dg_dE_F_dx_J`.
4. `g_max` 입력 단위가 `e/eV/atom`이면 내부에서 `J^-1 site^-1`로 변환한다.
5. `x` coordinate와 direction convention을 test로 고정한다: insertion 기준 `DeltaS_e<0`, delithiation release `-DeltaS_e>0`.
6. Ch1의 `config+vib+electronic` 가법성은 parameter decomposition이고, config 내부 logistic 조성 의존을 다시 `DeltaS_config(x)`로 중복 구현하지 않는다.

## 5. 부호·차원·극한 adversarial check

| 항목 | 검산 | 판정 |
|---|---|---|
| `w=nRT/F` | `[J/mol]/[C/mol]=V`; `n` dimensionless | pass |
| `U=(-DeltaH+TDeltaS)/F` | `[J/mol]/[C/mol]=V`; `partial U/partial T=DeltaS/F` | pass |
| `xi_eq` | exponent `(V-U)/w` dimensionless, `0<xi<1` | pass |
| equilibrium peak | `Q xi(1-xi)/w` = `C/V` | pass |
| `DeltaU_hys` | `(2/F)[J/mol]` = V; `Omega<=2RT -> 0` | pass |
| `L_q` | `T*/T`, exponent terms dimensionless | pass |
| `L_V` | `|dV/dq| L_q`; if `q` normalized, unit V | pass |
| lowpass DC | `(1-rho)/(1-rho)=1` | pass |
| `z_cut` | cutoff is derivative fraction, not `xi_eq` fraction | pass |
| LCO `DeltaS_e_mol` | `R kB T g_J` = `J/(mol K)` after `g_J[J^-1]` | pass if eV→J conversion applied |
| LCO electronic sign | insertion `x↑` makes `g` decrease, `dg/dx<0`, `DeltaS_e<0` | pass |
| LCO code status | current v1.0.10 has no LCO/electronic entropy implementation | theory-only, P4 |

## 6. 통합 권고

Ch1 본문은 이미 물리식 사슬의 대부분을 교과서식으로 닫고 있다. P2 supplement에서 통합할 보강은 본문 전체 재작성보다 다음 다리 삽입이 적절하다.

1. `N0--N9 code decision tree`를 Ch1 끝 또는 supplement에 추가한다.
2. `n` 우선, `w` fallback, `n>0` bound를 width 절에 명시한다.
3. dead helper `func_U_j_hys`와 live helper `func_dU_hys/func_U_branch`를 분리한다.
4. `_causal_lowpass` DC gain=1과 면적보존 proof를 tail 절에 추가한다.
5. `L_V` direct override, `dH_a missing`, `dVdq_qa=0` silent-off를 fitting guard 표로 둔다.
6. branch threshold의 `grid_step` 의존성을 rate-tail fitting 주의로 추가한다.
7. LCO 절에는 “current code에는 없음, P4 구현 예정”을 명시한다.
8. LCO electronic entropy는 molar conversion과 eV→J conversion을 별도 boxed rule로 둔다.

## 7. 결론

확정: Ch1은 P1의 12개 closed-form 물리식 대부분을 절·식 번호로 설명한다. 핵심 누락은 “식”이 아니라 code branch contract와 fitting guard다.  
확정: LCO 이론은 현재 Ch1에 존재하지만 v1.0.10 코드에는 없다. P2에서 이론 기술은 정상이며, 구현은 P4로 넘겨야 한다.  
확정: broadening은 `U_j` 분포가 아니라 `U_app=U_j+eta` 분포로 정리되어 있고, 입자 size/PSD 역산은 범위 밖이다.  
추정: LCO `g(E_F,x)`의 MIT logistic shape는 1차 문헌 연속곡선 부재를 메우는 model assumption이며 피팅 대상이다.  
추가 후보: Ch1 tab:nodemap의 polarization line citation은 P1 ground truth(L408)와 다르므로 통합 시 line-only 보정 후보로 남긴다.
