# V1010 P1 분석 드래프트 S1
**대상**: `Anode_Fit_v1.0.10.py` (695줄, 흑연 음극 dQ/dV forward 모델)
**작성**: 작업 sub-agent S1 (분석·드래프트 전담, 코드 수정·commit 없음)
**날짜**: 2026-07-01

---

## 1. 플로우차트 맵

### 1.1 전체 구조 개요

```
[입력층]
  ├─ GRAPHITE_STAGING_LIT (전이 초기값 리스트, 줄 531-560)
  │    각 dict: U/dH_rxn/dS_rxn · n · Q · Omega · gamma · dH_a · dS_a · dVdq_qa
  └─ 생성자 인자 (줄 221-231)
       x=0.5 · Rn · Cbg · chi · chi_split · use_dH_eff
       z_cut · A_cap_RT · grid_pad_lo/hi · n_work_min
       min_lag_grid_steps · v_span_floor · seed_T/I/Q_cell

          ↓ __init__ (줄 221-259)
          가드(_finite/_finite_pos/_finite_nonneg) → self.* 저장
          → _build_seed_L_V() → self.seed_L_V

[평형 기준선]
  equilibrium(V_n, T) (줄 350-367)
  ├─ func_U_j(T, dH_rxn, dS_rxn)         → U_j
  ├─ _n_factor(tr, T)                      → n_j
  ├─ _width(tr, T) = func_w(T, n_j)       → w
  └─ func_ksi_eq(T, V, U_j, n_j, s=+1)   → ξ_eq
       → Σ Q_j · ξ_eq(1−ξ_eq)/w  [+ Cbg]   → dQ/dV_eq

[관측 dQ/dV]
  dqdv(V_app, T, I_abs, Q_cell, s) (줄 370-480)
  │
  ├─ [입력 가드] _finite_nonneg / _finite_pos / isfinite 검사 (줄 391-405)
  │
  ├─ [분극] V_n = V_app − σ_d · |I| · Rn  (줄 408)
  │
  ├─ [작업 격자] V_work (n_work 점, 패드 포함)  (줄 415-416)
  │
  ├─ [비등온] T_is_array → T_work interp / 등온 → T_rep 스칼라  (줄 418-426)
  │
  └─ [전이 루프] for tr in transitions:  (줄 431-477)
       │
       ├─ [U_j] func_U_j(T_work, dH_rxn, dS_rxn) 또는 tr['U']   (줄 433-436)
       │
       ├─ [히스 분기 중심] (gamma≠0 and Omega>0 시)               (줄 444-450)
       │    hys_shift = func_U_branch(T_rep, 0, Omega, gamma, σ_d, h_eta)
       │      ← func_dU_hys(T, Omega): ΔU_hys = (2/F)[Ωu − 2RT·artanh(u)]
       │    center = U_j + hys_shift
       │         (γ=0 → center = U_j)
       │
       ├─ [폭] n_j = _n_factor(tr, T_work)                        (줄 452-453)
       │        w   = _width(tr, T_work) = func_w(T_work, n_j)
       │
       ├─ [점유] ξ_eq = func_ksi_eq(T_work, V_work, center, n_j, σ_d) (줄 455)
       │
       ├─ [지연 길이 L_V] _resolve_lag_length(tr, T_rep, I_abs, Q_cell, n_rep, σ_d)
       │    (줄 303-347)
       │    ├─ 직접 'L_V' 있으면 → 반환 (동역학 우회)            (줄 313-318)
       │    ├─ I≤0 or 'dH_a' 없음 → 0 반환                       (줄 319-320)
       │    └─ 동역학 산출:
       │         A = min(z_cut·n·RT, A_cap_RT·RT)               (줄 329-331)
       │         _chi_and_dH_eff → (χ_d, ΔH_a^eff)              (줄 338-339)
       │           ← _chi_d(σ_d) = chi_split(χ, σ_d)            (줄 287-290)
       │           ← func_dH_a_eff(dH_a, Omega, chi_d): ΔH_a−χ_d·Ω (줄 152-155)
       │         func_L_q(T, I, Q_cell, dH_a_use, dS_a, chi_d, A):
       │           ln_Lq = log(I·h/(Q_cell·kB·T)) − log(1+e^{−A/RT})
       │                   + (dH_a−T·dS_a)/RT − χ_d·A/RT        (줄 104-107)
       │         L_V = |dVdq_qa| · L_q                           (줄 347)
       │
       ├─ [peak_shape 분기]                                        (줄 462-475)
       │    ① L_V < min_lag_grid_steps·grid_step:
       │       peak_shape = ξ_eq(1−ξ_eq)/w     (평형 종)
       │    ② L_V 충분:
       │       방전(σ_d≥0): occ_lagged = _causal_lowpass(ξ_eq, grid_step, L_V)
       │       충전(σ_d<0): _causal_lowpass(ξ_eq[::-1], …)[::-1]  (역방향 인과)
       │       peak_shape = (ξ_eq − occ_lagged) / L_V
       │
       └─ dqdv_work += Q_j · peak_shape                           (줄 477)

  → np.interp(V_n, V_work, dqdv_work)  → 출력 dQ/dV              (줄 479)

[편의 facade]
  curve(V_app, direction, c_rate, Q_cell, T, I_abs) (줄 483-508)
  ├─ _direction_to_sigma(direction) → σ_d                        (줄 511-524)
  ├─ I_use = c_rate · Q_cell  (또는 I_abs 직접)
  └─ → dqdv(V_app, T, I_use, Q_cell, s=σ_d)                     (위임)
```

### 1.2 함수별 물리식 + 코드 줄 번호 근거

| 함수 | 물리식 | 코드 줄 | 비고 |
|------|--------|---------|------|
| `func_w(T, n)` | w = nRT/F | 74-75 | 전이 폭 [V]; n=다중도 |
| `func_U_j(T, dH_rxn, dS_rxn)` | U_j = (−ΔH_rxn + T·ΔS_rxn)/F | 78-79 | 평형 중심 [V] |
| `func_U_j_hys(T, U_j, Omega, gamma, s, last_eta, last_rest)` | U^d = U_j + ½s·partial_hys·γ·ΔU_hys | 82-91 | partial_hys=1.0 하드코딩 (후계자=func_U_branch) |
| `func_ksi_eq(T, V_n, U, n, s)` | ξ_eq = logistic[s(V_n−U)/w] (수치 안정형) | 94-97 | 방향 s: z≥0→1/(1+e^{−z}), z<0→e^z/(1+e^z) |
| `func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)` | ln L_q = ln(Ih/Q_cell kB T) − ln(1+e^{−A/RT}) + (dH_a−T·dS_a)/RT − x·A/RT | 100-107 | I≤0 → −∞(guard); x 자리에 χ_d 주입 |
| `_causal_lowpass(source, grid_step, lag_length)` | 인과 1차 지수기억 y[i] = α·y[i−1] + (1−α)·source[i], α=e^{−Δv/L_V} | 110-128 | scipy lfilter 우선, 예외 시 수동 loop |
| `func_dU_hys(T, Omega)` | ΔU_hys = (2/F)[Ω·u − 2RT·artanh(u)], u=√(1−2RT/Ω) | 133-140 | Ω≤2RT → 0; func_U_j_hys 내부와 동일식의 독립 노출 |
| `func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta)` | U^d = U_j + ½·σ_d·h_η·γ·ΔU_hys | 143-148 | h_eta: 부분 cycle 인자(func_U_j_hys의 partial_hys=1.0 인자화) |
| `func_dH_a_eff(dH_a, Omega, chi_d)` | ΔH_a^eff = ΔH_a − χ_d·Ω | 152-155 | 방향별 유효 활성화 엔탈피 |
| `func_chi_d(chi, sigma_d)` | χ_d = χ (방전, σ_d≥0) / 1−χ (충전) | 158-163 | 기본 규칙; chi_split으로 교체 가능 |
| `_finite(name, value)` | 유한성 가드 | 167-172 | NaN/±inf → ValueError |
| `_finite_pos(name, value)` | 유한 + >0 가드 | 175-180 | T·Q_cell·z_cut 등 분모 인자 |
| `_finite_nonneg(name, value)` | 유한 + ≥0 가드 | 183-188 | I_abs·Rn 등 |
| `_n_factor(tr, T)` | n 우선 → 'w' 있으면 n=wF/RT 역산 → 없으면 1 | 272-278 | 폭 다중도 산출 |
| `_width(tr, T)` | w = func_w(T, n_j) | 281-284 | use_w_eff 경로 제거됨(v1.0.10) |
| `_chi_d(sigma_d)` | χ_d = chi_split(χ, σ_d) | 287-290 | callable 위임 |
| `_chi_and_dH_eff(dH_a, Omega, sigma_d, use_dH_eff)` | (χ_d, ΔH_a^eff) 동시 산출 | 293-300 | per-tr use_dH_eff override 지원 |
| `_resolve_lag_length(tr, T, I, Q_cell, n_j, sigma_d)` | L_V = \|dVdq_qa\|·L_q | 303-347 | 직접 'L_V' 우회 → A 산출 → χ_d/ΔH_eff → func_L_q |
| `_build_seed_L_V(T, I, Q_cell)` | 전이별 L_V seed (방전 기준 대표 조건) | 262-269 | 진단/초기값 용; dqdv()는 실제 조건으로 재산출 |
| `equilibrium(V_n, T)` | dQ/dV\|_{I→0} = C_bg + Σ Q_j·ξ_eq(1−ξ_eq)/w | 350-367 | 방향 불변; func_U_j 또는 tr['U'] 양쪽 경로 |
| `dqdv(V_app, T, I_abs, Q_cell, s)` | dQ/dV = C_bg + Σ Q_j·[(ξ_eq−ξ̄)/L_V] 또는 Q_j·ξ_eq(1−ξ_eq)/w (저율) | 370-480 | 분극·히스·동역학 꼬리 통합 |
| `curve(V_app, direction, c_rate, Q_cell, T, I_abs)` | C-rate·방향 문자열 → dqdv 위임 | 483-508 | 새 물리 없음, facade |
| `_direction_to_sigma(direction)` | 문자열/정수 → σ_d=±1 | 511-524 | 정적 메서드 |

### 1.3 데이터 흐름 화살표 요약

```
transitions[j] dict
  → [U_j] func_U_j  ──────────────────────────────────┐
  → [ΔU_hys] func_dU_hys → func_U_branch → center     │
  → [n_j] _n_factor → [w] func_w                       │
  → [ξ_eq] func_ksi_eq(center, n_j, σ_d) ─────────────┤
  → [L_q] func_L_q(χ_d via _chi_d, ΔH_a^eff) ─────────┤
    → [L_V] _resolve_lag_length                         │
      → [occ_lagged] _causal_lowpass (σ_d 방향)         │
        → peak_shape = (ξ_eq − occ_lagged)/L_V          │
          또는 ξ_eq(1−ξ_eq)/w (저율)                    │
                                               Q_j ×   │
  dqdv_work += Q_j · peak_shape ←──────────────────────┘

dqdv_work → np.interp(V_n, V_work, dqdv_work) → 출력
```

---

## 2. 조건 Audit: BDD 음극 dQ/dV 물리수식 기반 피팅 함수로서의 충족도 및 결함

### 2.1 음극 전용 범위 확인

**확정**: 이 코드는 **흑연 음극 전용** 구현이다.

- LCO 양극 관련 파라미터·식 **부재** (근거: 전체 695줄 내 LCO·cathode 키워드 없음, 전이 dict에 양극 특유 파라미터 없음)
- 발열 항 q_rev(가역 발열) **부재** (근거: 에너지 균형식 없음, 열 생성 계산 없음)
- 전자 엔트로피 dS_e **부재** (근거: 파르메티 계수·전자열 기여 없음; dS_rxn은 Li 삽입 반응 엔트로피로 열역학 U_j 온도 의존에만 사용)
- GRAPHITE_STAGING_LIT의 4개 전이 = 흑연 staging (4→3, 3→2L, 2L→2, 2→1, U값 0.085~0.210 V vs Li/Li⁺) — 흑연 음극 특성과 정합

### 2.2 핵심 물리 구현 충족도

#### 2.2.1 평형 dQ/dV (equilibrium)

| 항목 | 충족 여부 | 근거 (줄) |
|------|-----------|-----------|
| Nernst-형 평형 중심 U_j(T) = (−ΔH+TΔS)/F | **충족** | 78-79, 359-361 |
| 로지스틱 점유 ξ_eq = logistic[s(V−U)/w] | **충족** | 94-97, 365 |
| dQ/dV = Q·ξ(1−ξ)/w (면적 보존 정규 종) | **충족** | 366 |
| 방향 불변 (평형) | **충족** | s=+1 고정 미반영 — equilibrium()은 n_j 전달 시 s=1 기본값 사용 (줄 365: `func_ksi_eq(T, V, U_j, n_j)` s 미전달 → 기본 s=1) |
| Cbg 배경 dQ/dV | **충족** | 354-356 |

**결함 미발견** (equilibrium에서 s 인자 미전달은 의도적 — 평형 종은 방향 불변, s=1이 올바른 기본값).

#### 2.2.2 분극 V_n (dqdv)

| 항목 | 충족 여부 | 근거 (줄) |
|------|-----------|-----------|
| V_n = V_app − σ_d·|I|·Rn | **충족** | 408 |
| 충전(σ_d=−1)→분극 방향 반전 (+Rn·I) | **충족** | σ_d=−1 → V_n = V_app + |I|·Rn |

#### 2.2.3 히스테리시스 분기 중심

| 항목 | 충족 여부 | 근거 (줄) |
|------|-----------|-----------|
| ΔU_hys = (2/F)[Ω·u−2RT·artanh(u)] | **충족** | 133-140 (func_dU_hys) |
| U^d = U_j + ½σ_d·h_η·γ·ΔU_hys | **충족** | 143-148 (func_U_branch) |
| Ω≤2RT → ΔU_hys=0 (NaN 분기 처리) | **충족** | 85-86, 136-137 |
| γ=0 또는 Ω=0 → center=U_j (평형 무히스) | **충족** | 444-450 |
| dqdv()에서 hys_shift를 T_rep (대표 온도)로 계산 | **충족·주의** | 447: `func_U_branch(T_rep, 0.0, ...)` — 배열 T일 때 T_rep=mean(T_work) 사용. 비등온 T(V) 프로파일에서 hys_shift가 스칼라. 이 근사는 물리적으로 수용 가능하나 문서화 필요. |

#### 2.2.4 동역학 꼬리 (L_V, _causal_lowpass)

| 항목 | 충족 여부 | 근거 (줄) |
|------|-----------|-----------|
| A = min(z_cut·n·RT, A_cap_RT·RT) | **충족** | 329-331 |
| func_L_q: 전이상태 이론 + Arrhenius | **충족** | 100-107 |
| L_V = |dVdq_qa|·L_q | **충족** | 347 |
| 인과 지수기억 (1차 IIR) | **충족** | 110-128 |
| 방전 σ_d≥0: 격자 오름차순 | **충족** | 470-471 |
| 충전 σ_d<0: 격자 역전 후 필터→역전 복원 | **충족** | 473 |
| L_V < min_lag_grid_steps·grid_step → 평형 종 사용 (L_V 0 처리) | **충족** | 462-464 |
| np.isfinite(L_V) 가드 | **충족** | 462 |
| χ_d 방향별 전달계수 (방전 χ / 충전 1−χ) | **충족** | 158-163, 287-290 |
| ΔH_a^eff = ΔH_a−χ_d·Ω (use_dH_eff=True) | **충족** | 152-155, 298-299 |

#### 2.2.5 면적 보존

**충족** (v1.0.10에서 use_w_eff 경로 제거 — 해당 경로는 ξ_eq의 폭과 dQ/dV 분모 w의 불일치로 면적보존이 깨지는 버그였음; 근거 줄 7, 283).

- 남은 경로(w = nRT/F 고정): ∫ Q·ξ(1−ξ)/w dV = Q (면적 보존 수학적 충족)
- _causal_lowpass 경로: 꼬리 (ξ_eq−occ_lagged)/L_V 의 적분도 원칙적으로 면적 보존 (오프셋이 lag에 의한 이동에 불과)

#### 2.2.6 None/0 가드가 의도 흐름 차단하는 경우 검토

**검토 항목 1**: `func_L_q`의 `I <= 0 → return -np.inf` (줄 102-103)

- dqdv()에서 I_abs가 0.0일 때 _resolve_lag_length()의 줄 319 `if I <= 0` → 0.0 반환으로 먼저 차단됨
- func_L_q에 I=0이 도달하는 경로: _build_seed_L_V에서 seed_I=0.0을 사용자가 지정한 경우. 하지만 seed_I는 `_finite_nonneg("seed_I", seed_I)` 가드만 있어 0.0 허용 (줄 257)
- **잠재 결함**: seed_I=0.0 전달 시 _resolve_lag_length → I<=0 → 0.0 반환 (문제 없음). 그러나 func_L_q에 직접 I=0이 전달될 여지가 있는 다른 경로가 없는지 확인: seed_I=0.0 → _build_seed_L_V → _resolve_lag_length → I=0 → 0.0 반환 (I≤0 분기; func_L_q 미호출). **차단 없음, 흐름 정상.**

**검토 항목 2**: `_resolve_lag_length`의 `if I <= 0 or transition.get('dH_a') is None: return 0.0` (줄 319-320)

- dqdv()에서 I_abs=0.0 → L_V=0 → min_lag_grid_steps 조건 → 평형 종 선택 (줄 462-464)
- **의도 흐름 차단 없음**: 물리적으로 올바름 (I→0 = 평형)

**검토 항목 3**: `_causal_lowpass`의 `if lag_length <= 0 or not np.isfinite(lag_length): return source_signal.copy()` (줄 113-114)

- L_V=0 또는 비유한값 → 꼬리 없음(평형 복사본 반환). dqdv()의 462 줄에서 이미 걸러지므로 이중 안전.
- **차단 없음, 방어적 설계로 적절.**

**검토 항목 4**: `func_L_q` 결과 `if not np.isfinite(L_q): return 0.0` (줄 343-344)

- ΔH_a_use가 매우 커서 exp 오버플로 가능성 → np.inf → 0.0 처리
- **주의**: L_q = +inf (매우 느린 동역학) → 0으로 처리되어 꼬리 없는 평형 종으로 취급됨. 물리적으로는 매우 긴 꼬리(평형 미도달)인데 평형 종으로 처리하는 보수적 근사. **의도 흐름을 차단하지는 않으나 물리 한계 문서화 필요.**

#### 2.2.7 死코드 (Dead Code) 검토

| 후보 | 판정 | 근거 |
|------|------|------|
| `func_U_j_hys` (줄 82-91) | **사용 안 됨 (死코드)** | dqdv()·equilibrium() 어디에서도 호출 없음. func_U_branch (줄 143)가 동일 물리를 partial_hys 인자화 형태로 대체. 원형 보존 목적으로 유지. 주석 "후계자=func_U_branch" 없음 — 잠재적 혼란. |
| `last_eta`, `last_rest` 인자 (func_U_j_hys 줄 83) | **미사용 파라미터** | 함수 본체에서 사용 안 됨 (partial_hys=1.0 하드코딩). 向后호환 서명 잔존. |
| `dS_a` (func_L_q, 줄 100; GRAPHITE_STAGING_LIT dS_a=0.0) | **존재하나 실질 기여 0** | 구조적 사망은 아님(파라미터 노출 목적); 현재 초기값 전부 0.0으로 기여 없음. 자유 피팅 파라미터로 설계됨 (추정). |
| `'U'`와 `'w'` 키 in GRAPHITE_STAGING_LIT | **폴백 경로 (하위호환)** | `'n'`이 있으면 `'w'`는 _n_factor에서 무시됨 (줄 274-275). `'U'`는 dH_rxn/dS_rxn 없는 dict에서만 사용 (줄 359-361, 433-436). GRAPHITE_STAGING_LIT은 양쪽 모두 보유하므로 dH_rxn/dS_rxn 경로만 활성. |

#### 2.2.8 시그널·호출체인 정합

| 체인 | 정합 여부 |
|------|-----------|
| curve() → dqdv() 위임 (새 물리 없음) | **정합** (줄 508) |
| dqdv() → _resolve_lag_length() → _chi_and_dH_eff() → _chi_d() → chi_split() | **정합** (줄 338, 293-300, 287-290) |
| dqdv() → func_U_branch() (T_rep 스칼라) → func_dU_hys() | **정합**, T_rep 근사 주의사항 있음 |
| equilibrium() → func_ksi_eq() s=1 기본 (방향 불변) | **정합** |
| _build_seed_L_V() → _resolve_lag_length() sigma_d=+1 | **정합** (방전 기준 seed) |
| func_ksi_eq에서 s 인자: dqdv()는 sigma_d 전달 (줄 455), equilibrium()은 미전달 (기본 s=1) | **정합** (평형=방향 불변) |

#### 2.2.9 요약: 주요 결함 및 주의사항

1. **func_U_j_hys 死코드 + 미사용 인자** (줄 82-91): 호출처 없음. 혼란 방지 주석 없음. 원형 보존 의도이나 문서화 필요.
2. **비등온 T(V) 시 hys_shift 스칼라 근사** (줄 447): T_rep=mean(T_work)으로 hys_shift 단일값 계산. 배열 T 환경에서 ΔU_hys 위치 의존성 미반영. 실용적 근사이나 추정.
3. **L_q=∞ → 0.0 처리** (줄 343-344): 매우 높은 ΔH_a 에서 L_q 오버플로 → 꼬리 없음으로 silent fallback. 물리 한계 명시 필요.
4. **dS_a 전부 0.0** (GRAPHITE_STAGING_LIT 줄 537, 543, 551, 557): 활성화 엔트로피 기여 없음. 자유 피팅 인자로 의도됐으나 초기값=0의 의미 혼동 가능.
5. **func_U_j_hys vs func_U_branch 중복**: 동일 물리의 두 구현이 공존. func_U_j_hys (원형), func_U_branch (인자화 후계자). 실제 경로는 func_U_branch만.

---

## 3. 피팅 파라미터 인벤토리

### 3.1 전이별 파라미터 (transitions[j] dict)

| 파라미터 | 단위 | 역할 | dQ/dV 지배 영역 | GRAPHITE_STAGING_LIT 초기값 | 자유/고정 초벌 권고 |
|----------|------|------|-----------------|------------------------------|---------------------|
| `dH_rxn` | J/mol | 평형 중심 U_j = (−ΔH+TΔS)/F의 온도 독립 항 | **peak 위치**: 온도 불변 기여. ΔH=-13~-11 kJ/mol → U≈0.085~0.210 V | stage별: −11700, −13500, −13100, −13000 | **자유** (온도 의존 실험 있으면 ΔS_rxn과 커플링) |
| `dS_rxn` | J/mol/K | 평형 중심 U_j의 온도 의존 기울기 dU/dT = ΔS/F | **peak 위치 온도 이동** (dU/dT·ΔT). 실온 단일 온도면 U에 흡수됨 | stage별: +29.0, 0.0, −5.0, −16.0 | **자유** (다온도 피팅 시); 단온도 피팅엔 **고정 또는 0** 권고 |
| `U` | V | 직접 평형 중심 (dH_rxn/dS_rxn 미지정 시 폴백) | peak 위치 | 0.210, 0.140, 0.120, 0.085 | **폴백용**, dH_rxn/dS_rxn 사용 시 불활성 |
| `n` | 무차원 | 폭 다중도 w=nRT/F. 현상학적 전이 날카로움 | **peak 폭**: n↑ → 폭↑ → peak 낮고 넓음. n=1 → w≈25.7mV@298K | 전부 1.0 | **자유** (가장 중요한 형상 파라미터); n>1 넓은 peak, n<1 날카로운 peak |
| `w` | V | 폭 직접 지정 폴백 ('n' 없을 때) | peak 폭 ('n'과 동일 역할) | 0.012~0.020 (폴백, 'n'=1.0 있어 불활성) | **폴백용** ('n' 사용 시 불활성) |
| `Q` | 전하 (a.u.) | 전이 용량 가중: dQ/dV peak 높이 비례 | **peak 높이·면적**: Q↑ → peak 높고 넓음. 면적 = Q | stage별: 0.10, 0.12, 0.25, 0.50 | **자유** (합이 전체 용량과 정합 필요) |
| `Omega` | J/mol | 정규용액 상호작용 상수. 히스테리시스 gap ΔU_hys에 진입 | **히스 gap**: Ω↑ → ΔU_hys↑ → 충방전 peak 분리↑. Ω≤2RT(≈4.96 kJ/mol@298K) → gap 0 | 6000~13000 (stage IV→I 증가 경향) | **자유** (gamma≠0 시); gamma=0이면 곡선에 기여 없음 |
| `gamma` | 무차원 | 히스 분기 축소 인자. γ∈[0,1] | **히스 분기 크기**: γ=0 → 히스 없음. γ=1 → 최대 분기 | GRAPHITE_STAGING_LIT에 미정의(→ 기본 0.0) | **자유** (히스테리시스 fitting); 초기 γ=0 (히스 없음) 추천 후 필요 시 해제 |
| `h_eta` | 무차원 | 부분 cycle 인자. partial_hys 비율 | **히스 분기 스케일**: h_eta<1 → 부분 cycle 히스 감소 | GRAPHITE_STAGING_LIT에 미정의(→ 기본 1.0) | 완전 cycle은 **고정 1.0**; 부분 cycle 실험 시 **자유** |
| `dH_a` | J/mol | 활성화 엔탈피. L_q의 Arrhenius 인자 | **꼬리 길이·C-rate 의존**: dH_a↑ → L_q↑ → 꼬리 길어짐, C-rate 의존 강함 | 40000~48000 (만충→저SOC 감소) | **자유** (C-rate/온도 의존 실험 있을 때); 단율 단온도 피팅엔 L_V 직접 지정 대안 |
| `dS_a` | J/mol/K | 활성화 엔트로피. dG_a=dH_a−T·dS_a | **꼬리 온도 의존 미세조정** (dH_a 대비 보조 역할) | 전부 0.0 | **고정 0.0** 초벌 권고 (기여 약하고 dH_a와 상관 높음) |
| `dVdq_qa` | V | 컷점 OCV 기울기 |dV/dq| at affinity 컷점 | **꼬리 크기 스케일**: dVdq_qa↑ → L_V↑ → 꼬리 길어짐. L_q·dVdq_qa = L_V | 전부 0.30 | **자유** (C-rate 의존 실험 있을 때); dH_a와 함께 L_V 스케일 결정 |
| `z_cut` | 무차원 | 꼬리 컷점 A/(nRT). A=z_cut·n·RT (상한 A_cap_RT·RT) | **A 컷점 위치 → L_q 기저값 결정**: z_cut↑ → A↑ → L_q↑. ξ_eq~5% 컷 (z_cut≈4.357) | 전역 기본 4.357 (per-tr override 가능) | **고정 4.357** 권고 (물리적 정의점); 탐색적 피팅 시 자유 |
| `A_cap_RT` | 무차원 | A 상한 = A_cap_RT·RT | **A 포화 방지**: 고n·저T에서 A 발산 억제 | 전역 기본 4.0 | **고정 4.0** 권고 초벌 |
| `use_dH_eff` | bool | per-tr ΔH_a^eff 보강 on/off | **ΔH_a^eff=ΔH_a−χ_d·Ω 경로 제어** | 전역 기본 True | **고정 True** (물리 정합); False는 디버그용 |
| `L_V` | V | 지연 길이 직접 지정 (동역학 우회) | **꼬리 길이 직접 제어**: dH_a/dVdq_qa 산출 우회 | 미정의 (동역학 산출 사용) | **자유** (단율 fit·테스트 시 대안); 정의 시 dH_a/dVdq_qa 불활성 |

### 3.2 전역 생성자 파라미터

| 파라미터 | 단위 | 역할 | dQ/dV 지배 영역 | 초기값 | 자유/고정 초벌 권고 |
|----------|------|------|-----------------|--------|---------------------|
| `x` (chi 미지정 시 → chi) | 무차원 [0,1] | 전이상태 분율 위치 χ. 방향별 χ_d 기반 | **꼬리 비대칭·방향 의존**: χ↑(→1) → 방전 꼬리 길고 충전 꼬리 짧음 | 0.5 (대칭) | **자유** (충방전 비대칭 피팅 시) |
| `chi` | 무차원 [0,1] | χ 직접 지정 (x 우선순위 재정의) | (x와 동일) | None → x 사용 | **자유** (x 대신 명시 지정 시) |
| `Rn` | Ω | 직렬 저항. V_n=V_app−σ_d|I|Rn | **peak 위치 C-rate 이동**: Rn↑ → 분극↑ → 방전 peak 저V, 충전 peak 고V 이동 | 0.0 | **자유** (분극 fitting 필요 시) |
| `Cbg` | dQ/dV 단위 또는 callable | 배경 dQ/dV 상수 또는 V 함수 | **기저 레벨** (모든 V에 균등 기여) | 0.0 | **자유** (기저 오프셋 필요 시) |
| `chi_split` | callable (chi, σ_d)→χ_d | 방향별 χ_d 분배 규칙 | **꼬리 방향 의존 전체 제어** | func_chi_d (방전 χ/충전 1−χ) | **고정 기본** (물리 기본); 비대칭 분배 실험 시 자유 |
| `use_dH_eff` | bool | 전역 ΔH_a^eff 보강 on/off | 꼬리 길이 전역 보정 | True | **고정 True** |

### 3.3 파라미터 지배 영역 요약 다이어그램

```
V축 (dQ/dV 곡선) ← 낮은 V (만충) ─── 높은 V (방전 말) →

peak 위치 ──────── dH_rxn / dS_rxn (온도 이동) / Rn (분극 이동)
peak 폭   ──────── n (또는 w 폴백)
peak 높이 ──────── Q / n (Q 고정·n 커지면 낮아짐, 면적=Q 불변)
히스 분기 ──────── Omega + gamma (+ h_eta 부분 cycle)
꼬리 길이 ──────── dH_a + dVdq_qa → L_V (또는 L_V 직접)
꼬리 비대칭 ──────── x(chi) [방전 vs 충전 꼬리 길이 비]
꼬리 방향 ──────── sigma_d (방전: V증가 방향 / 충전: V감소 방향)
기저 레벨 ──────── Cbg
분극 오프셋 ──────── Rn × I_abs
```

### 3.4 피팅 초벌 우선순위 권고

**1단계 (평형 형상, 단율·단온도):**
- 자유: `dH_rxn` × 4 (peak 위치), `n` × 4 (peak 폭), `Q` × 4 (peak 높이)
- 고정: dS_rxn=문헌, gamma=0, dH_a=문헌, Rn=0, Cbg=0 또는 소값

**2단계 (C-rate 의존, 동역학):**
- 추가 자유: `dH_a` × 4, `dVdq_qa` × 4, `Rn` (또는 `L_V` 직접)
- 대안: `L_V` × 4 직접 지정(동역학 우회, 개수 절반)

**3단계 (히스테리시스, 충방전 분기):**
- 추가 자유: `Omega` × 4, `gamma` × 4 (또는 전이별)
- 선택: `chi` (비대칭 꼬리), `dS_rxn` × 4 (다온도)

---

*이하 불확실 표기 규약: "추정" = 코드 근거 있으나 설계 의도 명시 없음; "근거 미발견" = 코드에서 직접 확인 불가*
