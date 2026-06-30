# V1010_P1 분석 드래프트 S3 — Anode_Fit v1.0.10

> 대상: `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\Anode_Fit_v1.0.10.py` (695줄)
> 분석일: 2026-07-01 | 역할: 작업 sub(분석 전용 — 코드 수정·commit X)

---

## 1. 플로우차트 맵

### 1-1 전체 데이터 흐름 개요

```
[GRAPHITE_STAGING_LIT (L.531–560)]
  transitions list (4개 전이 dict)
         │
         ▼
[GraphiteAnodeDischargeDQDV.__init__ (L.221–259)]
  인자 가드(_finite/_finite_pos/_finite_nonneg)
  self.chi_split 등록 (기본 func_chi_d)
  self.seed_L_V 산출 (_build_seed_L_V)
         │
         ├──► equilibrium(V_n, T)         : |I|→0 평형 곡선
         │       └──► 반환 dqdv (평형 peak 합산)
         │
         └──► dqdv(V_app, T, I_abs, Q_cell, s)  : 관측 dQ/dV
         │       └──► curve() facade가 내부 호출
         │
         ▼
    [curve(V_app, direction, c_rate, ...)] (L.483–508)
          direction → _direction_to_sigma → σ_d
          c_rate → I_abs = c_rate × Q_cell
          → dqdv(V_app, T, I_abs, Q_cell, s=σ_d)
```

---

### 1-2 모듈 함수 (전역, 사용자 원형 보존)

| 함수 | 줄 | 물리식 | 역할 |
|------|-----|--------|------|
| `func_w(T, n)` | L.74–75 | w = nRT/F | 전이 폭 [V]. n=다중도(기본 1). |
| `func_U_j(T, dH_rxn, dS_rxn)` | L.78–79 | U_j(T) = (−ΔH_rxn + T·ΔS_rxn)/F | 온도 의존 평형 전위 [V] |
| `func_U_j_hys(T, U_j, Omega, gamma, s, …)` | L.82–91 | U_j^d = U_j + ½·σ_d·partial_hys·γ·ΔU_hys, ΔU_hys = (2/F)[Ωu − 2RT·artanh u], u=√(1−2RT/Ω) | 히스테리시스 분기 중심(partial_hys=1 하드코딩 잔존 — 보완 함수 func_U_branch로 인자화). |
| `func_ksi_eq(T, V_n, U, n, s)` | L.94–97 | ξ_eq = logistic[s(V_n−U)/w] 수치안정 분기: z≥0→1/(1+e^{−z}), z<0→e^z/(1+e^z) | 평형 점유율 ξ_eq(V). s=방향부호(충방전 분기 중심에 반영). |
| `func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)` | L.100–107 | L_q = (I/Q_cell)·h/k_B · exp[−ln(1+e^{−A/RT}) + (dH_a−T·dS_a)/(RT) − x·A/(RT)] / T. I≤0이면 −∞ 반환. | 지연 길이 L_q [단위량]. x=χ_d가 주입됨. |
| `_causal_lowpass(signal, grid_step, lag)` | L.110–128 | 인과 1차 IIR: decay=exp(−Δv/L_V), scipy lfilter 우선·fallback 루프 | 꼬리 합성곱(eq:memory). lag≤0 또는 비유한→원본 복사(pass-through). |

---

### 1-3 보완 함수 (클래스 외부, 전역)

| 함수 | 줄 | 물리식 | 역할 |
|------|-----|--------|------|
| `func_dU_hys(T, Omega)` | L.133–140 | ΔU_hys = (2/F)[Ωu−2RT·artanh u], u=√(1−2RT/Ω); Ω≤2RT이면 0 | gap 독립 산출(eq:hysdU). func_U_j_hys 내부와 동일식. |
| `func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta)` | L.143–148 | U_j^d = U_j + ½·σ_d·h_eta·γ·ΔU_hys | 분기 중심 인자화(h_eta 노출). func_U_j_hys의 partial_hys=1 하드코딩을 h_eta로 대체. |
| `func_dH_a_eff(dH_a, Omega, chi_d)` | L.152–155 | ΔH_a^eff = ΔH_a − χ_d·Ω | 유효 활성화 엔탈피(eq:dHeff). |
| `func_chi_d(chi, sigma_d)` | L.158–163 | χ_d = χ (방전, σ_d≥0) / 1−χ (충전, σ_d<0) | 방향별 전달계수(eq:chisum). 주입 교체 가능. |
| `_finite / _finite_pos / _finite_nonneg` | L.167–188 | — | 입력 가드 헬퍼. |

---

### 1-4 생성자 (`__init__`, L.221–259)

```
입력: transitions, x, Rn, Cbg, chi, chi_split, use_dH_eff,
      z_cut, A_cap_RT, grid_pad_lo/hi, n_work_min,
      min_lag_grid_steps, v_span_floor, seed_T/I/Q_cell

처리:
  1. 모든 스칼라 인자 → _finite/_finite_pos/_finite_nonneg 가드 (L.234–248)
  2. chi_split callable 검증 (L.238–240)
  3. self.chi = chi if not None else self.x (L.237)
  4. _build_seed_L_V(seed_T, seed_I, seed_Q_cell) → self.seed_L_V (L.256–259)
```

**GRAPHITE_STAGING_LIT 연결:**
각 전이 dict가 transitions로 주입. `'n':1.0` 보유 → `_n_factor`가 `n`키 우선 반환 → w=RT/F≈25.7mV@298K. `'w'` 폴백값(0.020 등)은 `n`이 존재하므로 비활성.

---

### 1-5 내부 메서드 (클래스)

#### `_n_factor(tr, T)` (L.272–278)
```
'n' 키 있음 → tr['n'] 반환
'w' 키 있음 → n = w·F/(RT) 역산
없으면 → 1.0
```

#### `_width(tr, T)` (L.281–284)
```
w = func_w(T, _n_factor(tr, T)) = nRT/F
```

#### `_chi_d(sigma_d)` (L.287–290)
```
chi_split(self.chi, sigma_d) 호출 → χ_d 반환
기본: 방전 χ_d=χ, 충전 χ_d=1−χ
```

#### `_chi_and_dH_eff(dH_a, Omega, sigma_d, use_dH_eff)` (L.293–300)
```
chi_d = _chi_d(sigma_d)
use_dH_eff True → dH_a_use = func_dH_a_eff(dH_a, Omega, chi_d) = ΔH_a−χ_d·Ω
use_dH_eff False → dH_a_use = dH_a
반환: (chi_d, dH_a_use)
```

#### `_build_seed_L_V(T, I, Q_cell)` (L.262–269)
```
각 전이 tr에 대해:
  n_j = _n_factor(tr, T) → scalar 추출
  _resolve_lag_length(tr, T, I, Q_cell, n_j, sigma_d=+1)
반환: List[float] (진단·초기값용)
```

#### `_resolve_lag_length(transition, T, I, Q_cell, n_j, sigma_d)` (L.303–347)
```
[A] 'L_V' 직접 지정 있음
    └── 유한+비음수 가드 → 반환

[B] I≤0 또는 'dH_a' 없음
    └── 0.0 반환 (평형 종)

[C] 동역학 산출 경로:
    n_safe = |n_j|
    z_cut = transition.get('z_cut', self.z_cut)
    A_cap = transition.get('A_cap_RT', self.A_cap_RT)
    A = min(z_cut·n_safe·RT, A_cap·RT)         ← 컷 affinity [J/mol]
    dH_a, dS_a, Omega 로드 + 가드
    (chi_d, dH_a_use) = _chi_and_dH_eff(dH_a, Omega, sigma_d)
    L_q = func_L_q(T, I, Q_cell, dH_a_use, dS_a, chi_d, A)
    L_V = |dVdq_qa| × L_q                      ← [V]
```
물리식: L_V = |dV/dq|_{qa} · L_q (eq:tail)

---

### 1-6 `equilibrium(V_n, T)` (L.350–367)

```
입력: V_n (전위 배열), T (온도 K)
처리:
  baseline = Cbg(V) 또는 상수 Cbg
  for tr in transitions:
    U_j = func_U_j(T, dH_rxn, dS_rxn)   ← 열역학 키 존재 시
          또는 tr['U']                    ← 직접 지정
    n_j = _n_factor(tr, T)
    w   = _width(tr, T) = nRT/F
    ξ_eq = func_ksi_eq(T, V, U_j, n_j)  ← s=1 고정(방향 인자 없음)
    dqdv += Q_j · ξ_eq(1−ξ_eq)/w        ← eq:eqpeak
  반환: dqdv 배열
```

물리식: (dQ/dV)_eq = C_bg + Σ_j Q_j · ξ_eq(1−ξ_eq) / w

**주의:** `func_ksi_eq` 호출 시 `s` 인자 기본값(=1) 사용 — 충방전 분기 중심이 반영되지 않음. 방향 불변 평형 곡선 의도에는 부합하나, 히스테리시스 분기 중심(`center`)이 `dqdv()`와 달리 적용되지 않는 차이 존재(아래 audit §2-4 참조).

---

### 1-7 `dqdv(V_app, T, I_abs, Q_cell, s)` (L.370–480)

```
[입력 가드]  (L.388–405)
  sigma_d = +1 (s≥0) / −1 (s<0)
  _finite_nonneg(I_abs), _finite_pos(Q_cell)
  V_app 유한성 검증
  T 유한 + >0 검증

[분극]  (L.407–408)
  V_n = V_app − σ_d·|I|·R_n          ← eq:vapp

[작업 격자]  (L.410–416)
  v_lo, v_hi = min/max(V_n)
  v_span = max(v_hi−v_lo, v_span_floor)
  n_work = max(n_work_min, V_n.size×2)
  V_work = linspace(v_lo − pad_lo·v_span, v_hi + pad_hi·v_span, n_work)
  grid_step = V_work[1] − V_work[0]

[온도 보간]  (L.418–424)
  T_is_array: V_n 정렬 → T(V_work) 선형 보간
  등온: T_work = T_scalar × ones(n_work)
  T_rep = mean(T_work)

[baseline]  (L.427–429)
  dqdv_work = Cbg(V_work) 또는 상수

[전이 루프]  (L.431–477)
  for tr:
    ① U_j(T_work) 열역학 또는 직접 지정
    ② 히스 분기 shift  (L.441–450)
         gamma≠0, Omega>0:
           hys_shift = func_U_branch(T_rep, 0.0, Omega, gamma, sigma_d, h_eta)
                     = ½·σ_d·h_eta·γ·ΔU_hys(T_rep, Omega)
           center = U_j + hys_shift            ← eq:hyscenter
         else: center = U_j
    ③ n_j, w 산출 (배열 T_work 기준)
    ④ ξ_eq = func_ksi_eq(T_work, V_work, center, n_j, sigma_d)  ← eq:chisum 방향
    ⑤ lag_len_V = _resolve_lag_length(tr, T_rep, I_abs, Q_cell, n_rep, sigma_d)
    ⑥ 꼬리 분기:
         lag_len_V < min_lag_grid_steps·grid_step
           → peak_shape = ξ_eq(1−ξ_eq)/w      ← 평형 종(eq:eqpeak)
         else:
           방전(σ_d≥0): occ_lagged = _causal_lowpass(ξ_eq, grid_step, lag_len_V)
           충전(σ_d<0): occ_lagged = _causal_lowpass(ξ_eq[::-1], …)[::-1]
           peak_shape = (ξ_eq − occ_lagged) / lag_len_V   ← eq:closed
    ⑦ dqdv_work += Q_j · peak_shape

[보간 출력]  (L.479–480)
  dqdv_out = interp(V_n, V_work, dqdv_work)
  스칼라/배열 반환
```

물리식(합산): dQ/dV = C_bg + Σ_j Q_j [ξ_eq(1−ξ_eq)/w − (ξ_eq−ξ̄)/L_V] (eq:closed/hysmaster)

---

### 1-8 `curve(V_app, direction, c_rate, Q_cell, T, I_abs)` (L.483–508) — facade

```
direction → _direction_to_sigma → sigma_d
I_abs 직접 지정: _finite_nonneg 가드 → I_use = I_abs
I_abs None: I_use = c_rate × Q_cell
→ dqdv(V_app, T, I_use, Q_cell, s=sigma_d) 위임
```

---

## 2. 조건 Audit: 흑연 음극 dQ/dV 물리수식 피팅 함수 충족도

### 2-1 충족 항목 (확정)

| 항목 | 근거 줄 | 비고 |
|------|---------|------|
| Fermi-Dirac 형 점유율 ξ_eq = logistic[s(V_n−U)/w] | L.94–97 | 수치안정 2-분기 구현 |
| 평형 peak Q·ξ_eq(1−ξ_eq)/w (방향 불변) | L.366, L.464 | eq:eqpeak |
| 분극 V_n = V_app − σ_d·|I|·R_n | L.408 | eq:vapp. σ_d 부호 정확 |
| 히스테리시스 분기 중심 U^d = U_j + ½·σ_d·h_eta·γ·ΔU_hys | L.447–448 | func_U_branch 활성화(L.447) |
| 히스 gap ΔU_hys = (2/F)[Ωu−2RT·artanh u], Ω≤2RT→0 | L.133–140 | spinodal 기준 |
| 전달계수 χ_d: 방전=χ, 충전=1−χ | L.158–163 | 주입 교체 가능 |
| 유효 활성화 엔탈피 ΔH_a^eff = ΔH_a − χ_d·Ω | L.152–155 | use_dH_eff 플래그로 on/off |
| 컷 affinity A = min(z_cut·n·RT, A_cap·RT) | L.331 | per-tr override 가능 |
| L_q = (I/Q_cell)·(h/kB)·exp[…]/T 변환 | L.104–107 | eq:lnLq. I≤0→−∞ 처리 |
| L_V = \|dVdq_qa\| · L_q | L.347 | eq:tail |
| 인과 꼬리 합성곱: 방전=오름차순 IIR, 충전=뒤집어 IIR 후 되돌림 | L.470–473 | eq:memory. 방향 반전 정확 |
| peak_shape = (ξ_eq−ξ̄)/L_V (꼬리 차분 미분 이산형) | L.475 | eq:closed |
| 저율/lag 미달 시 자동 평형 종 폴백 | L.462–464 | min_lag_grid_steps 기준 |
| 비등온 T(V) 지원: V_n 정렬 후 선형 보간 | L.418–424 | T_is_array 경로 |
| 배경 C_bg: 상수 또는 callable(V) | L.427–429 | |
| facade curve(): C-rate·방향문자열→내부 dqdv 재사용 | L.483–508 | 새 물리 없음 |
| chi_split 주입 교체 가능 | L.224, L.287–290 | callable 검증 포함 |
| per-transition z_cut·A_cap_RT·use_dH_eff override | L.329–330, L.339 | 전이별 격리 |
| fail-fast 입력 가드 (T·I·Q_cell·dict 값·z_cut·L_V 등) | L.167–188, L.234–248, L.391–405 | ValueError/TypeError |
| 면적 보존: w=nRT/F 일관 (use_w_eff 제거) | L.7, L.283 | v1.0.10 핵심 변경 |

---

### 2-2 결함 / 주의 항목

#### (결함 1) `equilibrium()`의 히스테리시스 분기 미반영 (확정)
- **줄:** L.365 — `func_ksi_eq(T, V, U_j, n_j)` (s 인자 기본값=1, center 아닌 U_j 사용)
- **현상:** `dqdv()`는 gamma≠0일 때 `center = U_j + hys_shift`를 사용하나(L.448), `equilibrium()`은 U_j를 그대로 사용하고 s=1 고정.
- **영향:** `equilibrium()`이 엄밀히는 "히스테리시스 분기 중심의 평균 평형"이 아닌 "미분기 평형". gamma=0이면 영향 없음. 고 C-rate 피팅 비교 시 참조선 오차 가능.
- **판단:** 의도적 설계(방향 불변 평형 기준선)일 수 있으나 docstring에 명시 없음.

#### (결함 2) `func_U_j_hys()` partial_hys 하드코딩 잔존 (확정)
- **줄:** L.90 — `partial_hys = 1.0` (인자로 받은 `last_eta`, `last_rest`가 미사용)
- **현상:** 인자 시그니처에 `last_eta: float = 1.0, last_rest: int = 600`가 있으나 함수 내부에서 사용되지 않음. `func_U_branch()`가 `h_eta`를 인자화해 이 역할을 대체하므로, `func_U_j_hys()`는 사실상 dead parameter 보유.
- **판단:** `func_U_j_hys()`는 "사용자 원형 보존(1바이트도 변조 X)" 대상(L.36)이므로 의도적 동결. 실제 호출은 `dqdv()` 루프 안에서 `func_U_branch()`로 대체됨(L.447). `func_U_j_hys()` 자체는 `dqdv()`·`equilibrium()` 어디에서도 직접 호출되지 않음 → 死코드(외부 접근용 보존 원형).

#### (결함 3) `func_L_q()` I≤0 처리 일관성 (주의)
- **줄:** L.102–103 — `if I <= 0: return -np.inf`
- **현상:** `_resolve_lag_length()`에서 `I <= 0` 분기(L.319)가 먼저 걸려 `func_L_q()`까지 도달하지 않으므로 실질 사고 없음. 단, `func_L_q()`를 직접 호출 시 −∞ 반환.
- **판단:** 이중 가드 구조. 외부 직접 호출 시 −∞→`isfinite` 검사(L.343)→0 반환 경로이므로 안전.

#### (결함 4) `_resolve_lag_length()` dS_a 기본값 0.0 조용한 폴백 (주의)
- **줄:** L.334 — `dS_a = _finite("dS_a", transition.get('dS_a', 0.0))`
- **현상:** dict에 `dS_a`가 없으면 0으로 대체. GRAPHITE_STAGING_LIT 모든 전이에서 `'dS_a': 0.0` 명시(L.537, 543, 551, 557)이므로 현재 데이터셋에선 문제없음.
- **판단:** 설계 의도로 보이나, 외부 dict 작성 시 묵시적 0 폴백 주의.

#### (결함 5) `dqdv_work` 초기값 배열 재사용 (주의)
- **줄:** L.427–429, L.477 — baseline 배열을 `dqdv_work`로 초기화 후 `dqdv_work = dqdv_work + tr['Q'] * peak_shape`로 합산.
- **판단:** 불변 연산(`+` 신규 배열 생성)이므로 별도 copy() 없어도 원본 배열 변조 없음. 정상.

---

### 2-3 시그널 체인 검증

```
GRAPHITE_STAGING_LIT['n':1.0]
  → _n_factor(): 'n' 키 우선(L.274) → n_j=1.0
  → _width(): func_w(T, 1.0) = RT/F ≈ 0.02569 V @298K
  (※ 'w':0.020 등 dict 폴백값은 n이 존재하므로 미사용 — 확정)

dqdv() 전이 루프 내:
  U_j(T_work) 배열 → func_U_j 매 원소 → center = U_j + hys_shift
  ξ_eq = func_ksi_eq(T_work, V_work, center, n_j, sigma_d)
    → s=sigma_d가 logistic 부호 제어 → 충방전 분기 중심 반영 ✓
  lag_len_V = _resolve_lag_length(T_rep, I_abs, Q_cell, n_rep, sigma_d)
    → chi_d → dH_a_use → func_L_q → × dVdq_qa ✓
  peak_shape = (ξ_eq − occ_lagged) / lag_len_V ✓
  dqdv_work += Q_j · peak_shape ✓

dqdv_out = interp(V_n, V_work, dqdv_work)
  ← V_n = V_app − σ_d·I·Rn (분극 반영된 전위) ✓
```

체인 단절 없음. 모든 방향 의존(σ_d)이 분극·분기·꼬리 세 곳에 일관 전달 확정.

---

### 2-4 面적 보존 (Spectral Weight Conservation) 검증

- `w = nRT/F` (`_width()`, L.284) — ξ_eq 분모와 동일 w로 일관.
- `func_ksi_eq()` 분모 `func_w(T, n)` (L.96) = `_width()` 반환값과 동일 식.
- `use_w_eff` 경로(폭 보정 버그) 제거됨(L.7, L.283 주석) → v1.0.10의 핵심 정정.
- 평형 peak 적분 = Q_j (logistic 면적 = 1·w) → 면적 보존 성립 확정.

---

### 2-5 흑연 전용성 (LCO·발열·전자엔트로피 부재) 확인

| 항목 | 상태 | 근거 |
|------|------|------|
| 흑연 staging 전이(4→3, 3→2L, 2L→2, 2→1) | 존재 | GRAPHITE_STAGING_LIT L.531–560 |
| LCO 전이 | 부재 확정 | GRAPHITE_STAGING_LIT에 없음 |
| 발열 항(dQ/self-heating 커플링) | 부재 확정 | 온도 T는 입력 파라미터. 자기발열 피드백 없음 |
| 전자 엔트로피 항(Sommerfeld) | 부재 확정 | ΔS_rxn은 리튬화 반응 엔트로피 — 전자 엔트로피 별도 없음 |
| 비등온 T(V) | 지원 | L.418–424. 단, T(V) 프로파일은 사용자 입력(계산 아님) |

---

## 3. 피팅 파라미터 인벤토리

### 3-1 전이별 파라미터 (transitions dict 키)

| 파라미터 | 역할 | 곡선 지배 영역 | GRAPHITE_STAGING_LIT 초기값 | 자유/고정 |
|----------|------|----------------|----------------------------|-----------|
| `n_j` (`'n'` 키) | 전이 폭 다중도. w = n·RT/F. | 각 peak 폭(전 전이). n↑→peak 넓어짐 | 전이 1–4 모두 n=1.0 | 자유(fit). 현재 GRAPHITE_STAGING_LIT은 n=1.0 고정값이나 피팅 override 전제 |
| `U_j` (`'U'` 키) | 전이 평형 전위 직접 지정 [V] | 각 peak 중심 위치 | 0.210, 0.140, 0.120, 0.085 V (폴백; 열역학 키 존재 시 비활성) | 자유(열역학 우선 시 dH_rxn/dS_rxn으로 대체) |
| `dH_rxn` | 리튬화 반응 엔탈피 [J/mol]. U_j(T) = (−ΔH+TΔS)/F | peak 중심의 온도 의존성 | −11700, −13500, −13100, −13000 J/mol | 자유(열역학 피팅) |
| `dS_rxn` | 리튬화 반응 엔트로피 [J/mol/K] | peak 중심의 온도 계수 dU/dT = ΔS/F | +29.0, 0.0, −5.0, −16.0 J/mol/K | 자유(열역학 피팅) |
| `Omega` (Ω_j) | 정규용액 상호작용 파라미터 [J/mol]. 히스테리시스 gap·유효장벽에 관여 | 히스 분기 폭(gap)·꼬리 깊이(ΔH_a^eff). Ω↑→히스 gap↑, 꼬리↑ | 6000, 8000, 10000, 13000 J/mol | 자유(히스 존재 시 핵심 피팅) |
| `gamma` (γ) | 히스테리시스 분기 축소 인자(0~1). ΔU_hys에 곱해져 실효 분기 폭 제어 | 히스 peak 분리 정도. γ=0→히스 없음 | 미지정(0.0 기본) | 자유. GRAPHITE_STAGING_LIT에 미포함(0 처리) |
| `dH_a` | 활성화 엔탈피 [J/mol]. L_q 지수항 지배 | 꼬리 길이의 온도·C-rate 의존성. dH_a↑→꼬리 김 | 48000, 46000, 44000, 40000 J/mol | 자유(동역학 피팅) |
| `dS_a` | 활성화 엔트로피 [J/mol/K] | L_q의 온도 계수(dG_a = dH_a − T·dS_a) | 0.0 (전 전이, 명시) | 자유(기본 0 고정; 고온 피팅 시 자유화 가능) |
| `dVdq_qa` | 컷점 OCV 기울기 |dV/dq| [V] | L_V = |dVdq_qa| × L_q 환산. 꼬리 길이 [V]의 스케일 팩터 | 0.30 V (전 전이) | 자유(OCV 곡선 기울기 fit) |
| `Q` | 전이 용량 가중 (충전·전하 단위). peak 높이와 면적 지배 | 전체 곡선 각 peak 높이/면적. Q↑→peak↑ | 0.10, 0.12, 0.25, 0.50 | 자유(용량 배분 피팅) |
| `h_eta` | 부분 cycle 히스테리시스 인자(기본 1.0). ΔU_hys에 곱해짐 | 부분 충방전 시 히스 분기 감쇠. 1.0=완전 cycle | 미지정(1.0 기본) | 조건부 자유(부분 cycle 데이터 있을 때) |
| `L_V` | 꼬리 지연 길이 직접 지정 [V] (선택). 있으면 동역학 경로 우회 | 꼬리 길이 고정(동역학 우회, 테스트/간편 피팅용) | 미지정 | 조건부(지정 시 dH_a/dVdq_qa 무시) |
| `z_cut` | per-tr 컷 affinity z=A/(nRT) override (선택) | 꼬리 컷 점 위치(전이별 조정) | 미지정(전역 4.357 사용) | 조건부 자유 |
| `A_cap_RT` | per-tr 컷 affinity 상한 A_cap·RT override (선택) | 꼬리 상한 조정(전이별) | 미지정(전역 4.0 사용) | 조건부 자유 |
| `use_dH_eff` | per-tr ΔH_a^eff 보강 on/off override (bool, 선택) | 꼬리의 상호작용 보강 여부 (전이별) | 미지정(전역 True 사용) | 조건부 |

---

### 3-2 전역 생성자 파라미터

| 파라미터 | 역할 | 곡선 지배 영역 | 기본값 | 자유/고정 |
|----------|------|----------------|--------|-----------|
| `x` (= `chi` 미지정 시) | 전이상태 분율 위치 χ(방전 기준). L_q의 x 인자. | 꼬리 길이의 방향 비대칭(χ_d 분배) | 0.5 | 자유. χ=0.5이면 충방전 꼬리 대칭 |
| `chi` | χ 직접 지정(없으면 x 사용) | 상동 | None (x 사용) | 자유(x와 동의어, 직접 지정 우선) |
| `Rn` | 직렬 저항 [Ω]. 분극 V_n = V_app − σ_d·I·Rn | 전체 곡선 전위 축 이동. 방전 우 이동·충전 좌 이동 | 0.0 Ω | 자유(저율이면 영향 미미, 고율에서 중요) |
| `Cbg` | 배경 dQ/dV (상수 또는 V함수) | 전체 구간 베이스라인 | 0.0 | 자유(상수 또는 callable) |
| `z_cut` | 꼬리 컷점 affinity z=A/(nRT) (전역) | L_V 산출의 A 결정. z_cut↑→A↑→꼬리↑ | 4.357 (ξ_eq≈5% 해당) | 고정 권장(물리 기준); 필요 시 per-tr override |
| `A_cap_RT` | 컷 affinity 상한 A ≤ A_cap_RT·RT (전역) | A의 상한. 고온/고율 꼬리 발산 억제 | 4.0 | 고정 권장 |
| `use_dH_eff` | ΔH_a^eff = ΔH_a−χ_d·Ω 보강 전역 on/off | 꼬리의 상호작용 보강 전역 제어 | True | 전역 제어. per-tr override 가능 |
| `chi_split` | (chi, σ_d)→χ_d callable | 방향별 χ_d 분배 규칙 전체 교체 | `func_chi_d` | 고급 확장(기본값이면 고정으로 봄) |
| `grid_pad_lo/hi` | 작업 격자 하/상단 패딩(v_span의 배율) | 꼬리 truncation 방지 | 0.15 | 고정 권장(사용자 전위 범위 맞춤 조정 가능) |
| `n_work_min` | 작업 격자 최소 점수 | 내삽 해상도 | 2048 | 고정(정밀도 확보) |
| `min_lag_grid_steps` | 꼬리 폴백 threshold (lag < steps×grid_step) | 평형 종/꼬리 종 전환 경계 | 2.0 | 고정 권장 |
| `v_span_floor` | V_span 하한 (스칼라 V 시) | 단일점 호출 시 격자 축소 방지 | 1e-6 V | 고정 |
| `seed_T/I/Q_cell` | seed_L_V 산출용 대표 조건 | 진단값 seed에만 영향(실 호출과 무관) | 298.15 K / 0.1 / 1.0 | 진단용 고정 |

---

### 3-3 파라미터 곡선 지배 영역 요약

```
전위 축 이동       : Rn(분극) + U_j / dH_rxn+dS_rxn(온도·열역학)
peak 위치·간격     : U_j (또는 dH_rxn+dS_rxn) — 각 전이별 독립
peak 폭           : n_j (또는 w) — nRT/F. 온도 의존. 면적 보존 조건
peak 높이·면적     : Q_j (용량 가중)
히스 분기 폭       : Omega·gamma — gamma=0이면 히스 없음
꼬리 길이 [V]      : dH_a (지배) + chi/x (방향 비대칭) + dVdq_qa (스케일)
                     + Omega (ΔH_a^eff 보강, use_dH_eff=True 시)
꼬리 온도 의존      : dH_a - T·dS_a 항 (dS_a=0이면 Arrhenius)
베이스라인         : Cbg
```

---

## 부록: GRAPHITE_STAGING_LIT 전이 대응표

| 전이 | stage | SOC 구간 | U(폴백)[V] | n | Q | Omega[J/mol] | dH_rxn[J/mol] | dS_rxn[J/mol/K] | dH_a[J/mol] | dVdq_qa[V] | 줄 |
|------|-------|----------|-----------|---|---|-------------|--------------|----------------|------------|------------|-----|
| 1 | 4→3 | x=0.08–0.16 | 0.210 | 1.0 | 0.10 | 6000 | −11700 | +29.0 | 48000 | 0.30 | L.532–538 |
| 2 | 3→2L | x=0.16–0.25 | 0.140 | 1.0 | 0.12 | 8000 | −13500 | 0.0 | 46000 | 0.30 | L.539–545 |
| 3 | 2L→2 | x=0.25–0.50 | 0.120 | 1.0 | 0.25 | 10000 | −13100 | −5.0 | 44000 | 0.30 | L.546–552 |
| 4 | 2→1 | x=0.50–1.00 | 0.085 | 1.0 | 0.50 | 13000 | −13000 | −16.0 | 40000 | 0.30 | L.553–559 |

> 모든 전이: dS_a=0.0 명시, gamma 미지정(=0), h_eta 미지정(=1.0), L_V 미지정(동역학 산출 경로).

---

*작성: 2026-07-01 | S3 작업 sub | 파일: V1010_P1_draft_S3.md*
