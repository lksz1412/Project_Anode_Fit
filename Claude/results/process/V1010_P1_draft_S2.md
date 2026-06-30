# V1010 P1 분석 드래프트 S2
## Anode_Fit v1.0.10 — 물리 구조 분석 (작업 sub 독립 작성)

**대상 파일**: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` (695줄, 전문 정독)
**작성일**: 2026-07-01

---

## 1. 플로우차트 맵

### 1-1. 전체 데이터 흐름 개요

```
[생성자 입력]
  transitions (List[dict])          ← GRAPHITE_STAGING_LIT 또는 사용자 정의
    ├── 열역학 : dH_rxn, dS_rxn (→ U_j) 또는 U 직접
    ├── 폭     : n 또는 w (→ w = nRT/F)
    ├── 용량   : Q
    ├── 히스   : Omega, gamma, h_eta
    ├── 동역학 : dH_a, dS_a, dVdq_qa (또는 L_V 직접)
    └── override: z_cut, A_cap_RT, use_dH_eff
  전역 스칼라: x, Rn, Cbg, chi, chi_split, use_dH_eff, z_cut, A_cap_RT
  격자 제어  : grid_pad_lo/hi, n_work_min, min_lag_grid_steps, v_span_floor
  seed 조건  : seed_T, seed_I, seed_Q_cell

        │
        ▼ __init__ (줄 221-259)
  [가드] _finite / _finite_pos / _finite_nonneg (줄 167-188) → fail-fast
        │
        ▼ _build_seed_L_V (줄 262-269)
  seed_L_V[j] = _resolve_lag_length(tr_j, seed_T, seed_I, seed_Q_cell, n_j, σ_d=+1)
  (진단·초기값용 — dqdv() 호출마다 실제 조건으로 재산출)

─────────────────────────────────────────────────────────────

[공개 메서드 호출 경로]

  ┌── curve(V_app, direction, c_rate, Q_cell, T, I_abs)  (줄 483-508)
  │     │ _direction_to_sigma (줄 510-524)
  │     │   문자열/정수 → σ_d (+1 방전 / -1 충전)
  │     │ |I| = c_rate × Q_cell  (I_abs 없을 때)
  │     └─► dqdv(V_app, T, I_abs, Q_cell, s=σ_d)
  │
  └── equilibrium(V_n, T)  (줄 350-367)
        │ [배경] Cbg(V) 또는 상수
        │ for j in transitions:
        │   U_j = func_U_j(T, dH_rxn, dS_rxn)  또는  tr['U']
        │   n_j = _n_factor(tr, T)
        │   w   = _width(tr, T) = func_w(T, n_j)
        │   ksi_eq = func_ksi_eq(T, V, U_j, n_j, s=1)
        │   dqdv += Q · ksi_eq·(1−ksi_eq) / w
        └─► dQ/dV (평형, 방향 불변)

─────────────────────────────────────────────────────────────

  dqdv(V_app, T, I_abs, Q_cell, s)  (줄 370-480)
  │
  ├── [입력 가드] I_abs, Q_cell, T, V_app (줄 391-405)
  │
  ├── [분극] V_n = V_app − σ_d·|I|·Rn  (줄 408, eq:vapp)
  │
  ├── [작업 격자] V_work: [v_lo−pad_lo·span, v_hi+pad_hi·span], n_work점 (줄 415-416)
  │     grid_step = V_work[1] − V_work[0]
  │
  ├── [비등온] T_work: T 배열이면 V 기준 interp, 스칼라면 상수 배열 (줄 418-424)
  │     T_rep = mean(T_work)  (동역학 대표 온도)
  │
  ├── [배경] dqdv_work = Cbg(V_work) 또는 상수 (줄 427-429)
  │
  └── for j in transitions:  (줄 431-477)
        │
        ├── [평형 중심 U_j]
        │     dH_rxn/dS_rxn 있으면 func_U_j(T_work, …)  → 배열 (줄 434)
        │     없으면 tr['U']  → 스칼라 (줄 436)
        │
        ├── [히스테리시스 분기 이동] (줄 441-451)
        │     Omega, gamma, h_eta 추출
        │     gamma≠0 AND Omega>0 이면:
        │       hys_shift = func_U_branch(T_rep, 0.0, Omega, gamma, σ_d, h_eta)
        │                 = σ_d·½·h_eta·gamma·func_dU_hys(T_rep, Omega)
        │       center = U_j + hys_shift
        │     else: center = U_j
        │
        ├── [폭·점유]
        │     n_j = _n_factor(tr, T_work)
        │     w   = _width(tr, T_work) = func_w(T_work, n_j)  (줄 452-453)
        │     ksi_eq = func_ksi_eq(T_work, V_work, center, n_j, σ_d)  (줄 455)
        │
        ├── [지연 길이] (줄 458-460)
        │     n_rep  = _n_factor(tr, T_rep) [스칼라]
        │     lag_len_V = _resolve_lag_length(tr, T_rep, I_abs, Q_cell, n_rep, σ_d)
        │       │ L_V 직접 지정이면 즉시 반환 (줄 313-318)
        │       │ I≤0 또는 dH_a 없으면 0.0 반환 (줄 319-320)
        │       │ else: A = min(z_cut·n·R·T, A_cap·R·T) (줄 331)
        │       │       chi_d, dH_a_use = _chi_and_dH_eff(dH_a, Omega, σ_d, ...)
        │       │         ├── chi_d = chi_split(chi, σ_d)  (줄 297)
        │       │         └── dH_a_use = func_dH_a_eff(dH_a, Omega, chi_d) if use_dH_eff (줄 299)
        │       │       L_q = func_L_q(T, I, Q_cell, dH_a_use, dS_a, chi_d, A) (줄 342)
        │       └───────► lag_len_V = |dVdq_qa| × L_q (줄 347)
        │
        ├── [평형 종 (lag_len_V < min_lag_grid_steps·grid_step)] (줄 462-464)
        │     peak_shape = ksi_eq·(1−ksi_eq) / w
        │
        └── [꼬리 합성곱] (줄 466-475)
              방전 σ_d≥0: occ_lagged = _causal_lowpass(ksi_arr, grid_step, lag_len_V)
              충전 σ_d<0 : occ_lagged = _causal_lowpass(ksi_arr[::-1], …)[::-1]
                             (방향 반전 후 필터 → 되돌림; 인과 기억 방향 반전)
              peak_shape = (ksi_eq − occ_lagged) / lag_len_V
              dqdv_work += Q · peak_shape
        │
        ▼
  dqdv_out = interp(V_n, V_work, dqdv_work)  (줄 479)
  └─► 반환 (스칼라 또는 배열)
```

---

### 1-2. 함수별 물리식 + 줄 번호 근거

#### 모듈 수준 독립 함수 (사용자 원형 보존 영역, 줄 73-129)

**`func_w(T, n)` [줄 74-75]**
- 물리식: $w = nRT/F$
- 역할: 전이 폭 [V]. n = 다중도(폭 파라미터).
- 호출자: `_width` (줄 284), `func_ksi_eq` 내부 (줄 96)

**`func_U_j(T, dH_rxn, dS_rxn)` [줄 78-79]**
- 물리식: $U_j(T) = (-\Delta H_\text{rxn} + T\Delta S_\text{rxn})/F$
- 역할: 전이 평형 중심 전위 [V]. 깁스-헬름홀츠 관계.
- 호출자: `equilibrium` (줄 360), `dqdv` (줄 434), `__main__` 검증 (줄 583)

**`func_U_j_hys(T, U_j, Omega, gamma, s, last_eta, last_rest)` [줄 82-91]**
- 물리식:
  - $u = \sqrt{1 - 2RT/\Omega}$ (줄 88, Ω > 2RT 조건)
  - $\Delta U_\text{hys} = (2/F)[\Omega u - 2RT\cdot\text{artanh}(u)]$ (줄 89)
  - $U_j^d = U_j + \tfrac{1}{2}s \cdot \text{partial\_hys} \cdot \gamma \cdot \Delta U_\text{hys}$ (줄 91)
- partial_hys = 1.0 **하드코딩** (줄 90). 이 함수는 `dqdv`에서 직접 호출되지 않음 — `func_U_branch` + `func_dU_hys`로 대체(줄 447).
- 주의: `last_eta`, `last_rest` 인자를 받지만 본체에서 사용 안 함 (死인자, 줄 83).

**`func_ksi_eq(T, V_n, U, n, s)` [줄 94-97]**
- 물리식: $z = s(V_n - U)/w$, $\xi_\text{eq} = \sigma(z)$ (수치 안정 logistic)
- 역할: 평형 점유율 ξ_eq.
- 수치 안정: z≥0 이면 1/(1+exp(-z)), z<0 이면 exp(z)/(1+exp(z)) (줄 97)
- 호출자: `equilibrium` (줄 365), `dqdv` (줄 455)

**`func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)` [줄 100-107]**
- 물리식:
  - $T_\text{att} = (I/Q_\text{cell})\cdot h/k_B$ (줄 104)
  - $\Delta G_a = \Delta H_a - T\Delta S_a$ (줄 105)
  - $\ln L_q = \ln(T_\text{att}/T) - \ln(1 + e^{-A/RT}) + \Delta G_a/(RT) - xA/(RT)$ (줄 106)
  - $L_q = \exp(\ln L_q)$ (줄 107)
- I≤0이면 -inf 반환 (줄 103)
- x 인자 자리에 호출 시 χ_d(방향별 전달계수)가 주입됨 (줄 342)

**`_causal_lowpass(source_signal, grid_step, lag_length)` [줄 110-128]**
- 물리식: 1차 IIR 지수기억 필터 = 인과 합성곱 (eq:memory)
  - $\alpha = \exp(-\Delta V / L_V)$ (줄 115)
  - scipy.signal.lfilter([1-α],[1,-α], signal) (줄 119-121)
  - fallback: 순환 루프 (줄 124-128)
- lag_length ≤ 0 또는 비유한이면 source_signal.copy() 그대로 반환 (줄 113-114)

#### 보완 영역 독립 함수 (줄 132-188)

**`func_dU_hys(T, Omega)` [줄 133-140]**
- 물리식: spinodal 분기 gap $\Delta U_\text{hys} = (2/F)[\Omega u - 2RT\cdot\text{artanh}(u)]$, $u=\sqrt{1-2RT/\Omega}$
- Ω ≤ 2RT이면 0.0 (줄 137-138)
- `func_U_j_hys` 내부 식의 추출·공개본. `func_U_branch`가 호출.

**`func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta)` [줄 143-148]**
- 물리식: $U_j^d = U_j + \tfrac{1}{2}\sigma_d\cdot h_\eta\cdot\gamma\cdot\Delta U_\text{hys}$ (eq:hyscenter)
- `func_U_j_hys`의 partial_hys 하드코딩을 h_eta로 인자화한 버전.
- 호출자: `dqdv` 내 히스 분기 shift 계산 (줄 447)

**`func_dH_a_eff(dH_a, Omega, chi_d)` [줄 152-155]**
- 물리식: $\Delta H_a^\text{eff} = \Delta H_a - \chi_d\cdot\Omega$ (eq:dHeff)
- 호출자: `_chi_and_dH_eff` (줄 299)

**`func_chi_d(chi, sigma_d)` [줄 158-163]**
- 물리식: $\chi_d = \chi$ (방전 σ_d≥0) / $\chi_d = 1-\chi$ (충전 σ_d<0) (eq:chisum)
- 기본 chi_split callable. 생성자에 다른 callable 주입 가능 (줄 224, 239-240).

**가드 함수 `_finite`, `_finite_pos`, `_finite_nonneg` [줄 167-188]**
- 물리식 없음. 입력 유한성·부호 검증 → ValueError.

#### 클래스 메서드 (GraphiteAnodeDischargeDQDV, 줄 192-)

**`_n_factor(tr, T)` [줄 272-278]**
- 폭 다중도 n 결정 우선순위: tr['n'] → tr['w']·F/(RT) 역산 → 1.0
- GRAPHITE_STAGING_LIT는 'n':1.0 보유 → 항상 첫 번째 분기 (줄 274)
- 'w' 값(0.020 등)은 'n'이 있을 때 inert (줄 533-559 확인)

**`_width(tr, T)` [줄 281-284]**
- $w = \text{func\_w}(T, n_j) = n_j RT/F$
- use_w_eff 경로 제거됨 (줄 283 주석: v12에서 제거 — 실제로는 v1.0.10에서 이미 제거)

**`_chi_d(sigma_d)` [줄 287-290]**
- `self.chi_split(self.chi, sigma_d)` 위임. 주입된 callable 사용.

**`_chi_and_dH_eff(dH_a, Omega, sigma_d, use_dH_eff)` [줄 293-300]**
- χ_d와 ΔH_a^eff를 한 곳에서 산출. per-transition override 지원 (use_dH_eff=None→전역 사용).

**`_resolve_lag_length(transition, T, I, Q_cell, n_j, sigma_d)` [줄 303-347]**
- 지연 길이 L_V [V] 계산:
  1. tr['L_V'] 직접 지정 → 반환 (줄 313-318)
  2. I≤0 또는 dH_a 없음 → 0.0 (줄 319-320)
  3. 동역학 산출:
     - n_safe = |n_j|, z_cut = tr.get('z_cut', self.z_cut) (줄 328-329)
     - $A = \min(z_\text{cut}\cdot n\cdot RT,\; A_\text{cap}\cdot RT)$ (줄 331)
     - (χ_d, ΔH_a_use) = _chi_and_dH_eff (줄 338-339)
     - L_q = func_L_q(T, I, Q_cell, dH_a_use, dS_a, chi_d, A) (줄 342)
     - L_V = |dVdq_qa| × L_q (줄 347)

**`equilibrium(V_n, T)` [줄 350-367]**
- 평형 dQ/dV = Cbg + Σ_j Q_j·ξ_eq·(1−ξ_eq)/w (eq:eqpeak)
- 방향 불변 (s=1 고정으로 func_ksi_eq 호출, 줄 365)

**`dqdv(V_app, T, I_abs, Q_cell, s)` [줄 370-480]**
- 관측 dQ/dV 전체 계산. 핵심 메서드. 상세는 1-1 플로우차트 참조.

**`curve(V_app, direction, c_rate, Q_cell, T, I_abs)` [줄 483-508]**
- 편의 facade. 새 물리 없음. c_rate→|I| 환산 후 `dqdv` 위임.

**`_direction_to_sigma(direction)` [줄 510-524]**
- 문자열/정수 방향 → σ_d (+1/-1) 변환.

---

## 2. 조건 Audit: 'BDD 음극 dQ/dV 물리수식 피팅 함수' 충족도·결함

### 2-1. 음극 전용 여부 확인

**확정**: 흑연 음극 전용.
- GRAPHITE_STAGING_LIT 4개 전이: stage 4→3, 3→2L, 2L→2, 2→1 (줄 532-559) → 흑연 스테이징 전이.
- U 범위: 0.085~0.210 V vs. Li/Li+ → 음극 전위 영역.
- LCO(양극) 물리, 발열 모델, 전자 엔트로피 항 **부재** — 코드 어디에도 없음 (전문 정독 근거).
- 부호 규약: 충전 σ_d=−1, 방전 σ_d=+1 → 음극 기준 (양극이면 부호 반대).

### 2-2. 물리수식 충족도

| 항목 | 충족 | 근거 줄 |
|------|------|---------|
| 평형 U_j(T) 열역학 | ✓ | 78-79, 360, 434 |
| 폭 w = nRT/F | ✓ | 74-75, 284 |
| 평형 점유 ξ_eq(logistic) | ✓ | 94-97, 455 |
| 평형 peak Q·ξ(1−ξ)/w | ✓ | 366, 464 |
| 분극 V_n = V_app − σ_d|I|Rn | ✓ | 408 |
| 히스 gap ΔU_hys (eq:hysdU) | ✓ | 133-140 |
| 분기 중심 U^d (eq:hyscenter) | ✓ | 143-148, 447 |
| 전달계수 χ_d (eq:chisum) | ✓ | 158-163, 287-290 |
| 유효 활성화 ΔH_a^eff (eq:dHeff) | ✓ | 152-155, 299 |
| 지연 길이 L_q (eq:lnLq) | ✓ | 100-107, 342 |
| L_V = |dVdq_qa|·L_q (eq:tail) | ✓ | 347 |
| 인과 지수기억 합성곱 (eq:memory) | ✓ | 110-128, 471-473 |
| dQ/dV = Cbg + Σ Q·(평형−꼬리)/L_V | ✓ | 475-477 |
| 충전 방향 반전 합성곱 | ✓ | 472-473 |

### 2-3. 결함 및 주의 사항

#### (A) 死인자 (dead parameter)

**`func_U_j_hys`의 `last_eta`, `last_rest` (줄 83)**
- 함수 시그니처에 있으나 본체(줄 84-91) 어디에도 사용되지 않음.
- 또한 이 함수 자체가 `dqdv` 내에서 직접 호출되지 않음 — `func_U_branch` + `func_dU_hys`가 대체.
- 결함 유형: dead parameter + 사실상 dead code (외부에서 호출 시에만 유효, 내부 경로에서는 우회됨).
- `__main__` 검증 블록에서도 `func_U_j_hys` 직접 호출 없음 (확정).

#### (B) partial_hys 하드코딩 vs. h_eta 인자화 불일치

- `func_U_j_hys` 내 `partial_hys = 1.0` 하드코딩 (줄 90).
- `func_U_branch`는 `h_eta` 인자로 이를 노출 (줄 144, 148).
- `dqdv`는 `func_U_branch` 사용 → h_eta 반영됨. `func_U_j_hys` 직접 호출 경로는 partial_hys=1.0 고정.
- 이 불일치는 `dqdv` 경로에는 영향 없으나, 사용자가 `func_U_j_hys`를 직접 사용하면 h_eta를 무시함 — 혼동 위험.

#### (C) 면적 보존 관련

- use_w_eff 경로 제거 (줄 7, 283) → 현재 w = nRT/F만 사용 → 면적 보존 성립.
- 평형 종: $\int Q\cdot\xi(1-\xi)/w\,dV = Q\cdot[\xi]_{-\infty}^{+\infty} = Q$ (해석적으로 성립).
- 꼬리 종: peak_shape = (ξ_eq − ξ_lag)/L_V. 인과 필터에서 ξ_lag의 적분 = ξ_eq의 적분 (수렴 후), 따라서 $\int \text{peak\_shape}\,dV \to 0$ (꼬리는 면적 이동이지 추가가 아님). **주의**: 격자 범위가 꼬리를 충분히 커버하지 않으면 면적 손실 가능 (grid_pad_lo/hi로 완화).

#### (D) 가드 차단 경로 확인

- I≤0 시 `func_L_q`가 -inf 반환 (줄 103), `_resolve_lag_length`에서 isfinite 가드 (줄 343-344) → 0.0 반환 → 평형 종 경로 진입 (줄 462-464). **정상 동작**.
- dqdv에서 I_abs=0 입력: `_finite_nonneg` 통과 (≥0 허용) → `_resolve_lag_length(I=0)` → 0.0 → 평형 종. **정상**.
- L_V=inf 직접 지정 시: `_resolve_lag_length` 줄 316에서 ValueError 발생. **가드 정상** (`__main__` 줄 677-678 검증 확인).

#### (E) 시그널/호출 체인 확인

- `func_ksi_eq`의 s(부호) 인자: `equilibrium`에서 s=1 고정 (줄 365), `dqdv`에서 sigma_d 전달 (줄 455). **정상**.
- `func_L_q`의 x 인자 자리: `_resolve_lag_length`에서 chi_d 주입 (줄 342). **정합**.
- `func_U_branch`의 U_j=0.0 입력 (줄 447): shift만 산출 후 배열 U_j에 가산 (줄 448). T_rep 사용 (스칼라). **설계상 정상**.
- `_build_seed_L_V`에서 `_n_factor` 반환값 `.reshape(-1)[0]` 처리 (줄 266): T_work가 배열일 때 n_j가 배열이 될 수 있으므로 스칼라 추출. `dqdv`에서도 동일 패턴 (줄 458). **정상**.

#### (F) `dqdv_work` 누적 시작값

- 줄 427-429: `dqdv_work = Cbg(V_work) 또는 상수`. 배경부터 시작 후 for 루프에서 += 누적. **정상**.

#### (G) 충전 합성곱 방향

- 줄 472-473: `ksi_arr[::-1]`로 뒤집어 `_causal_lowpass` 후 `[::-1]` 복원. 충전 진행 방향(V 감소)을 격자 오름차순으로 처리. **물리적으로 정합**.

### 2-4. 전체 충족도 요약

- BDD 음극 dQ/dV 물리수식: **충족** (전이 식 전체 구현됨).
- 결함: `func_U_j_hys`의 死인자 (last_eta, last_rest) — dqdv 경로에는 영향 없음.
- 히스 partial_hys 불일치: dqdv 경로(func_U_branch 사용) 무관, 원형 보존 목적 함수 직접 사용 시 혼동 위험.
- 면적 보존: w=nRT/F 유지 조건에서 성립. 격자 여백 부족 시 꼬리 면적 손실 가능 (설계 주의 사항).

---

## 3. 피팅 파라미터 인벤토리

### 3-1. 전이별(per-transition) 파라미터

| 파라미터 | 코드 키 | 역할 | 곡선 지배 영역 | GRAPHITE_STAGING_LIT 초기값 | 자유/고정 권고 |
|----------|---------|------|---------------|---------------------------|--------------|
| 평형 중심 전위 | `U` (또는 dH_rxn, dS_rxn) | 각 전이 peak의 V축 위치 | **peak 위치** | 0.210, 0.140, 0.120, 0.085 V | **자유** (핵심 피팅 대상) |
| 폭 다중도 | `n` (또는 `w` 역산) | peak 폭 = nRT/F [V] | **peak 폭** | 1.0 (4전이 공통) — 'w' 폴백 있으나 'n' 존재 시 inert | **자유** (n 또는 w 중 택일) |
| 전이 용량 가중 | `Q` | peak 높이 스케일 | **peak 높이** | 0.10, 0.12, 0.25, 0.50 | **자유** (단, Σ Q = 전체 용량 제약 가능) |
| 정규용액 상호작용 | `Omega` (Ω) | 히스 gap 크기·평형 종 분기 유무 | **히스 분기 크기** (Ω>2RT 시 활성) | 6000, 8000, 10000, 13000 J/mol | **자유** (히스 피팅 시); Ω≤2RT이면 히스=0 |
| 히스 축소 인자 | `gamma` (γ) | 분기 이동량 스케일 γ·ΔU_hys | **히스 분기 폭 조절** | GRAPHITE_STAGING_LIT에 없음 (기본 0.0 = 히스 off) | **자유** (히스 off=0, 단순 피팅 시 고정=0) |
| 부분 cycle 인자 | `h_eta` | 부분 cycle 시 히스 감소 | 히스 분기 크기 | GRAPHITE_STAGING_LIT에 없음 (기본 1.0) | 단순 피팅 시 **고정=1.0** |
| 활성화 엔탈피 | `dH_a` | 꼬리 길이(동역학 속도 장벽) | **꼬리 길이** | 48000, 46000, 44000, 40000 J/mol | **자유** (동역학 포함 피팅 시) |
| 활성화 엔트로피 | `dS_a` | 꼬리 온도 의존성 | 꼬리 온도 민감도 | 0.0 (4전이 공통) | 단순 피팅 시 **고정=0** |
| 컷점 OCV 기울기 | `dVdq_qa` | L_V 환산 인자 (L_q→L_V) | **꼬리 스케일** | 0.30 V (4전이 공통) | **자유** (또는 실험 OCV 곡선에서 고정) |
| 지연 길이 직접 지정 | `L_V` | 동역학 우회, L_V 직접 제어 | 꼬리 길이 전체 | 없음 (선택 override) | **자유** (동역학 식 우회 시 택일) |
| 컷 affinity | `z_cut` | 꼬리 시작점 (ξ_eq~5%) | 꼬리 시작 위치 | 4.357 (전역 기본, per-tr override 가능) | 단순 피팅 시 **고정=4.357** |
| affinity 상한 | `A_cap_RT` | 컷 affinity 상한 배수 | 꼬리 포화 제한 | 4.0 (전역 기본) | 단순 피팅 시 **고정=4.0** |
| ΔH_eff 보강 사용 | `use_dH_eff` | ΔH_a^eff = ΔH_a − χ_d·Ω on/off | 꼬리 χ_d 보강 | 전역 True (per-tr override 가능) | 단순 피팅 시 **고정=True** |

### 3-2. 전역(모델 수준) 파라미터

| 파라미터 | 생성자 인자 | 역할 | 곡선 지배 영역 | 기본값 | 자유/고정 권고 |
|----------|-----------|------|---------------|-------|--------------|
| 전이상태 위치 | `x` (chi 없을 때) | χ 기본값 (방향별 전달계수 계산) | 꼬리 충전/방전 비대칭 | 0.5 | 단순 피팅 **고정=0.5** |
| 전달계수 직접 지정 | `chi` | χ_d=χ(방전)/1-χ(충전) | 꼬리 충전/방전 비대칭 | x 값 사용 | **자유** (비대칭 꼬리 피팅 시) |
| 직렬 저항 | `Rn` | 분극 ΔV = σ_d|I|Rn → peak 이동 | **peak 위치 C-rate 의존성** | 0.0 Ω | **자유** (C-rate 의존 피팅 시) |
| 배경 dQ/dV | `Cbg` | 전체 곡선의 바닥 오프셋 | 전 영역 오프셋 | 0.0 | **자유** (상수 또는 V 함수) |

### 3-3. 파라미터 역할 요약 (곡선 지배 구조)

```
곡선 형상 요소          지배 파라미터
─────────────────────────────────────────────────────
peak V축 위치          U_j (또는 dH_rxn, dS_rxn) + Rn·|I|·σ_d (분극 이동)
peak 폭                n (또는 w = nRT/F) — T에 비례
peak 높이              Q (용량 가중)
히스 분기 이동         Omega·gamma (Ω>2RT 조건 하에서 분기 gap 활성)
부분 cycle 히스        h_eta (0~1)
꼬리 길이              dH_a + dS_a + chi/x (→ ΔH_a^eff → L_q → L_V)
꼬리 스케일            dVdq_qa × L_q
꼬리 충방전 비대칭     chi (→ χ_d = χ vs. 1-χ)
배경                   Cbg
```

---

## 메타 정보

- 정독 범위: 줄 1-703 전체 (전문 정독 완료)
- 불확실 처리: '추정' 표기 없음 — 모든 항목 줄 근거로 확정
- 근거 미발견: `func_U_j_hys`의 last_eta/last_rest 물리적 의도 불명 (코드 본체 미사용, 추정 금지)
- 허위 attribution 없음 — 독립 작성

**경로**: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1010_P1_draft_S2.md`
