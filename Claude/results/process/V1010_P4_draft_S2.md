# V1010 P4 코드개정 설계 드래프트 (S2)

**역할**: S2 (설계 전용 서브 세션 — .py 및 문건 수정 절대 금지)  
**작성 기준**: `Anode_Fit_v1.0.10.py` (703 L) · `V1010_P1_code-audit_RESULT.md` · `graphite_ica_ch1_v1.0.10.tex` (1933 L) · `graphite_ica_ch2_v1.0.10.tex` (751 L) 전문 정독 완료  
**인용 형식**: 코드 L# = 코드 행번호 / eq:XXX = Ch1 or Ch2 해당 식 라벨 / tab:XXX = 해당 표 라벨

---

## 0. 설계 전제 검증

### 0-1. "LCO·q_rev·dS_e 기능 부재" 확인 (P1 §2-E 인용)

P1 감사에서 `grep "LCO|q_rev|dS_e|cathode|발열"` → No matches 확정.  
코드 상 관련 심볼 0건이므로 전부 신규 추가다.

### 0-2. 흑연 경로 무섭동 전제 확인

`GraphiteAnodeDischargeDQDV` 클래스 L221–508는 독립 완결 단위다.  
`GRAPHITE_STAGING_LIT` (L531–560) 딕셔너리는 4-전이 초기값 전용이며 클래스 외부 상수다.  
신규 `LCOCathodeDQDV` 클래스와 `LCO_MSMR_LIT` 상수는 이 딕셔너리/클래스를 **공유 상속하거나 수정하지 않는다** — 독립 병존이 0-diff 가드의 물리적 기반.

### 0-3. 면적 보존 경로 확인

`_causal_lowpass` DC gain=1 (L110–128 IIR 계수 `[1-rho]` / `[1, -rho]` → DC z=1 대입 시 1/1=1).  
`use_w_eff` 제거됨(P1 §4 확인). 면적 보존 ∫Q·ξ(1−ξ)/w dV = Q 이미 성립.

---

## 1. LCO 양극 dQ/dV 클래스 설계

### 1-1. 신규 클래스 vs 일반화 base — 결정 및 근거

**결정: 독립 신규 클래스 `LCOCathodeDQDV`** (일반화 base 클래스 도입 불채택)

근거 3가지:

| 항목 | 독립 신규 클래스 | 일반화 base |
|------|----------------|------------|
| 흑연 0-diff 가드 | 기존 클래스 코드 라인 0 변경 → byte 일치 보장 | 기존 클래스의 `__init__` 시그니처 변경 불가피 → 회귀 위험 |
| LCO 전자항 | T1 전이에만 `dS_e_mol` plug-in 필요 → 조건 분기가 클래스 내부 국소화 | base에 flag 추가 시 흑연 경로에 dead branch 오염 |
| 사용자 코드 소유권 | `feedback_code_ownership_scope`: 식별자·대소문자 보존 의무 | 흑연 생성자 시그니처 변경은 보존 위반 |

`dqdv`, `curve`, `equilibrium`, `_causal_lowpass`, `func_ksi_eq` 등 **모든 모듈 수준 함수는 공유** — 이것이 MSMR 동형(eq:msmr)의 코드 측 증거이자 중복 코드 0 전략.

### 1-2. MSMR 동형 매핑표

Ch1 sec:lco-code (L1735–1760) 명시. MSMR 문헌식 eq:msmr과 Ch1 logistic eq:xieq의 1:1 대응:

| MSMR 문헌 기호 | Ch1 코드 식별자 | 의미 | 양극 적용 시 |
|---------------|----------------|------|-------------|
| `X_j` | `tr['Q']` | 용량 가중 | LCO 전이별 용량 (Q_total = 1.0 정규화) |
| `U_j^0` | `func_U_j(dH_rxn, dS_rxn, T)` (L78–79) | 평형 중심 `U_j(T)` | LCO 전이 전위 (T1≈3.90V, T2≈4.05V, T3≈4.17V) |
| `ω_j` | `func_w(T, n)` + `_width()` (L74–75, L281–284) | 봉우리 폭 `w_j = n_j RT/F` | LCO 두-상 → 현상학적 자유 피팅 폭 |
| `f` (종별 부호±1) | `σ_d` (`_direction_to_sigma`, L510–524) | 방향 인자 `f = −σ_d` | LCO 방전=리튬화(σ_d=+1), 충전=탈리튬화(σ_d=−1) |
| `exp[+f(U−U_j^0)/ω_j]` | `func_ksi_eq(V, U, w, sigma_d)` (L94–97) | logistic 점유 | 구조 동일; 파라미터만 LCO 값 |
| 불포함 (그래파이트 전용) | `func_dU_hys`, `func_U_branch` (L133–148) | 히스 분기 | LCO 1차 채용 시 `Omega=0` (히스 미적용) |
| 불포함 (흑연 전용) | `func_L_q`, `_resolve_lag_length` (L100–107, L303–347) | 동역학 지연 | LCO 1차 채용 시 `L_V=0` (평형 곡선) |

**핵심 부호 확인**: 방전(σ_d=+1, 리튬화 = ξ↑)에서 `func_ksi_eq` → `logistic[+1·(V−U)/w]` → V↑ 시 ξ↑. LCO 방전 중 V는 4.2→3.7V 방향으로 하강하므로 **LCO `curve()` 호출 시 `direction='discharge'`의 의미를 캐소드 기준으로 정의**해야 한다. 관례:

- LCO **방전(full-cell 방전) = 리튬화(Li⁺가 LCO로 삽입) = ξ: 0→1 = σ_d = +1**
- LCO **충전 = 탈리튬화 = ξ: 1→0 = σ_d = −1**

이는 Ch1 eq:msmr의 `f = −σ_d` 대응(흑연과 동일 규약)과 모순 없음.

### 1-3. MIT 전자 엔트로피 항 설계 — `ΔS_e_mol`

#### 물리 출처

Ch1 sec:lco-electronic (L928–1157)·Ch2 ssec:elec (L381–409). Sommerfeld 전자 열용량에서:

```
S_e = (π²/3) k_B² T g(E_F, x)            [eq:Se]
ΔS_{e,j}(x, T) = ∂S_e/∂x |_T
               = (π²/3) k_B² T · ∂g/∂x   [eq:dSe — 자리당, 단위: k_B²T/e_V 급]
```

몰당 환산 (코드 슬롯에 넣을 단위 = J/(mol·K)):

```
ΔS_{e,j}^mol(x, T) = N_A · (π²/3) k_B² T · ∂g/∂x   [eq:dSemolar]
```

**★단위 경고**: `g(E_F)` 를 eV⁻¹ 단위로 쓸 때 J 단위 변환은 **÷ e_V** (나눔) — 곱하면 ~4×10³⁷ 오류 (eq:gunit, Ch1 L~971 주변).

#### MIT 게이트 함수

```
g(E_F, x) ≈ g_max · [1 − σ((x − x_MIT) / Δx_MIT)]    [eq:ggate]
  σ(z) = 1/(1+exp(−z))    (logistic)
  초기값: g_max = 13 e/eV,  x_MIT ≈ 0.85,  Δx_MIT ≈ 0.05
```

닫힌 미분식:

```
∂g/∂x = −(g_max / Δx_MIT) · σ(z) · [1 − σ(z)]
         z = (x − x_MIT) / Δx_MIT
→ ΔS_{e,j}^mol < 0  (삽입 기준, 삽입 시 x↑ → g 감소)   [eq:dSegate]
```

#### x↔V 좌표 매핑 (Ch1 sec:lco-code L1724–1733)

`dqdv`는 V 격자에서 구동된다. T1 전이의 `ξ_{eq,1}(V)` = 해당 전이 구간의 정규화 조성에 대응하므로:

```python
x_coord = xi_eq_T1   # T1 전이 func_ksi_eq 출력
dSe_mol = calc_dSe_mol(x_coord, T, g_max, x_MIT, dx_MIT)
```

이를 `dS_rxn` (= `ΔS_{rxn,j}^cat`) 슬롯의 T1 전이 기여분에 합산. `func_U_j`의 `dS_rxn` 인자 경유.

#### T² 누적 (eq:U1T2, Ch1 L~971 부근)

전자항이 `∝T`이므로 U_1(T)에 T² 항이 생긴다:

```
U_1(T) = U_1(T_0) + (ΔS_0/F)(T−T_0) + (a_e/2F)(T²−T_0²)
  a_e = N_A(π²/3)k_B² · ∂g/∂x   [x_MIT 부근 대표값으로 평가]
```

1차 설계에서는 `a_e`를 별도 피팅 파라미터로 노출하거나, `dS_rxn` 키에 `T`-의존 콜러블을 허용하는 선택지가 있다. **1차 구현 권고**: `ΔS_{rxn,T1}` = `dS0_T1 + dSe_mol(x, T)` 을 `dqdv` 루프 내 T1 전이 처리 시 실시간 합산 (콜러블 불필요, 루프 내 조건 분기로 충분).

### 1-4. LCO_MSMR_LIT 상수 설계

Ch1 tab:lco-staging 기반 (3 전이, T4 ≥ 4.55V는 범위 밖):

```python
LCO_MSMR_LIT = [
    # T1: MIT 전이 (x = 0.94→0.75, ~3.90 V)
    dict(
        U=3.90,          # 피팅 출발값; ΔH_rxn/ΔS_rxn 쌍으로 대체 가능
        dH_rxn=-75000,   # J/mol  (tier C 초기값 — round-trip 검증 필요)
        dS_rxn=-5.0,     # J/(mol·K)  중심 표준값 ΔS⁰_T1 (config=0 기준; electronic 항 별도)
        Q=0.19,          # 전체 용량 비 (Li x: 0.94→0.75, ~19%)
        Omega=0,         # 히스 미적용 (1차)
        gamma=0,
        # 전자항 플래그 — T1 전용
        mit_elec=True,
        g_max=13.0,      # e/eV  (Ch1 eq:ggate 초기값)
        x_MIT=0.85,
        dx_MIT=0.05,
    ),
    # T2: 질서-무질서 전이 (~4.05–4.08 V)
    dict(
        U=4.06,
        dH_rxn=-78000,
        dS_rxn=0.47,     # Motohashi 2009 tier B
        Q=0.31,          # ~31%
        Omega=0,
        gamma=0,
        mit_elec=False,
    ),
    # T3: 질서-무질서 전이 (~4.17–4.20 V)
    dict(
        U=4.18,
        dH_rxn=-80000,
        dS_rxn=1.49,     # Motohashi 2009 tier B
        Q=0.25,          # ~25%
        Omega=0,
        gamma=0,
        mit_elec=False,
    ),
]
```

**라이선스 주의**: `dH_rxn` 절대값은 Ch1 tab:lco-staging에 tier C (초기값)로 분류됨 — round-trip 피팅 필수.  
`n` 키 미지정 시 `_n_factor`가 `n=1.0` 기본값 반환 (L272–278) → `w = RT/F` (이상 고용체 폭). LCO 두-상 전이는 현상학적 `w` 필요 → `w` 키를 직접 지정하거나 `n` ≠ 1로 피팅 허용.

### 1-5. `LCOCathodeDQDV` 함수 시그니처

```python
class LCOCathodeDQDV:
    """LCO 양극 dQ/dV 전진 모델 (MSMR 동형, Ch1 sec:lco-code).

    Parameters
    ----------
    transitions : list[dict]
        전이 파라미터 리스트. 기본 = LCO_MSMR_LIT.
        키 구조: GraphiteAnodeDischargeDQDV의 transition dict와 동일 +
        mit_elec, g_max, x_MIT, dx_MIT (T1 전이 전자항).
    T : float
        온도 [K]. 기본 298.15.
    Rn : float
        분극 저항 [Ω·Ah] 또는 [V/(A/Ah)]. 기본 0.
    Cbg : float | callable
        배경 커패시턴스. 기본 0.
    chi : float
        전달 계수 [0,1]. 기본 0.5.
    chi_split : callable
        방향별 분기 함수. 기본 func_chi_d.
    grid_pad_lo, grid_pad_hi : float
        작업 격자 패딩 [V]. 기본 0.15.
    n_work_min : int
        최소 격자 점수. 기본 2048.
    min_lag_grid_steps : float
        꼬리/평형 전환 문턱. 기본 2.0.
    seed_T, seed_I, seed_Q_cell : float
        진단 seed 조건. 기본 298.15 / 0.1 / 1.0.
    """

    def __init__(
        self,
        transitions=None,
        T: float = 298.15,
        Rn: float = 0.0,
        Cbg=0.0,
        chi: float = 0.5,
        chi_split=None,
        grid_pad_lo: float = 0.15,
        grid_pad_hi: float = 0.15,
        n_work_min: int = 2048,
        min_lag_grid_steps: float = 2.0,
        seed_T: float = 298.15,
        seed_I: float = 0.1,
        seed_Q_cell: float = 1.0,
    ): ...

    def dqdv(
        self,
        V_app,          # array-like [V], 인가 전압 격자
        T: float,       # [K]
        I_abs: float,   # [A] 절대 전류
        Q_cell: float,  # [Ah]
        sigma_d: int,   # +1 방전(리튬화) / −1 충전(탈리튬화)
    ) -> np.ndarray: ...

    def curve(
        self,
        V_app,
        T: float = 298.15,
        c_rate: float = None,
        I_abs: float = None,
        Q_cell: float = 1.0,
        direction: str = "discharge",   # "discharge" = 리튬화 = σ_d=+1
    ) -> np.ndarray: ...

    def equilibrium(
        self,
        V_app,
        T: float = 298.15,
    ) -> np.ndarray: ...
```

`GraphiteAnodeDischargeDQDV`의 `curve` facade (L483–508)와 `_direction_to_sigma` (L510–524)를 **직접 호출** (import + 재사용). `dqdv` 내부의 전이 루프는 흑연과 동일 구조이되, T1 전이에서만 `mit_elec=True` 분기로 `ΔS_e_mol` 합산.

---

## 2. 가역 발열 q_rev 설계

### 2-1. q_rev 기본 방정식

Ch2 eq:qrev (L643–649):

```
Q̇_rev = −I · T · ∂U_oc/∂T = −(I·T/F) · ΔS(x)
```

부호 규약 (Ch2 L651–654):

- `ΔS = +F · ∂U_oc/∂T`
- `I > 0` = 방전
- `Q̇_rev > 0` = 발열 (셀이 주변으로 열 방출)
- `ΔS < 0` → 방전 시 발열; `ΔS > 0` → 방전 시 흡열

### 2-2. ΔS(x) 완전식 — 3성분 조립

Ch2 sec:revheat keybox (L668–685):

```
∂U_oc/∂T(x) = [Σ_j Q_j g_j(x) (ΔS⁰_j/F + (R/F)·ln(ξ_j/(1−ξ_j)))]
               / [Σ_j Q_j g_j(x)]
               
   g_j(x) = ξ_j(1−ξ_j) / w_j           # 국소 dQ/dV 비중 (= 평형 peak 모양)
   ΔS(x)  = F · ∂U_oc/∂T(x)
```

3성분 분해 (Ch2 ss:elec, Ch1 eq:lco-decomp):

| 성분 | 기호 | 코드 슬롯 | 비고 |
|------|------|----------|------|
| Configurational | `ΔS⁰_j` + `R·ln[ξ/(1−ξ)]` | `dS_rxn` 중심값 + logistic 자동 생성 | 중심값은 `dS_rxn` 키, 분포 항은 `ξ_j` 로부터 자동 |
| Vibrational | `ΔS_j^vib` | `dS_rxn`에 합산 (중심 표준값 일부) | 별도 분리 불필요 — `ΔS⁰_j = ΔS_vib + ΔS_config_center` |
| Electronic (LCO T1만) | `ΔS_{e,j}^mol(x, T)` | T1 루프 내 `dS_rxn`에 가산 | x-의존·T-선형 → 다온도 피팅에서 분리 식별 가능 |

### 2-3. ★이중계산 직교 분리 설계

**문제 정의** (Ch2 ss:파생B, L524–537):

`ΔS⁰_j`는 봉우리 중심 `ξ_j = 1/2` (config=0)에서 정의된 표준값이다. 이 지점에서 config 항 `R·ln[ξ/(1−ξ)] = R·ln[1/1] = 0`. 따라서 `ΔS⁰_j`는 이미 vib+elec 중심을 흡수하며, **config 분포 항을 `ΔS⁰_j`에 다시 더하면 이중계산**.

**코드 내 분리 방법**:

```python
# ★ 올바른 구현 (이중계산 없음)
# dS_rxn 키 = ΔS⁰_j (봉우리 중심 표준값, config=0에서의 값)
# config 분포 항 R·ln[ξ/(1−ξ)] 는 완전식 평가 시 ξ_j로부터 별도 합산

def _dUdT_full(self, V_app, T, sigma_d):
    """∂U_oc/∂T(x) 완전식 평가 (Ch2 eq:weighted + config 분포)."""
    numerator   = 0.0
    denominator = 0.0
    for tr in self.transitions:
        U_j  = func_U_j(tr.get('dH_rxn', ...), tr.get('dS_rxn', ...), T)
        # T1: MIT 전자항 가산
        dS_total = tr.get('dS_rxn', 0.0)
        if tr.get('mit_elec', False):
            xi_T1 = func_ksi_eq(V_app, U_j, func_w(T, _n_factor(tr)), sigma_d)
            dS_total = dS_total + _calc_dSe_mol(xi_T1, T, tr)   # ΔS⁰_j + elec
        
        w_j    = func_w(T, _n_factor(tr))
        xi_j   = func_ksi_eq(V_app, U_j, w_j, sigma_d)
        g_j    = xi_j * (1.0 - xi_j) / w_j
        
        # config 분포 항: R·ln[ξ/(1−ξ)] / F — 봉우리 내부 x-의존
        # 발산 방지: clip xi away from 0/1
        xi_safe = np.clip(xi_j, 1e-12, 1.0 - 1e-12)
        config_term = (R / F) * np.log(xi_safe / (1.0 - xi_safe))
        
        dUdT_j = dS_total / F + config_term    # ΔS⁰/F + config 분포
        
        numerator   += tr['Q'] * g_j * dUdT_j
        denominator += tr['Q'] * g_j
    
    denom_safe = np.where(np.abs(denominator) < 1e-30, 1e-30, denominator)
    return numerator / denom_safe                    # ∂U_oc/∂T(x)  [V/K]

# ★ 이중계산 금지 체크리스트:
# □ dS_rxn 키에는 ΔS⁰_j (중심 표준값, config=0) 만 입력
# □ config 분포 항은 ξ_j 로부터 런타임에 자동 계산 (입력 키로 제공 X)
# □ mit_elec 슬롯에는 게이트 ΔS_e^mol(x,T) 만 (config와 직교 — Ch1 eq:lco-decomp)
```

**직교성 근거** (Ch1 eq:lco-decomp L1702–1710): config 자유도(Li 자리 점유 배열)와 전자 자유도(전도 전자 밴드 점유)는 근사적으로 독립 → `Z ≈ Z_config · Z_elec` → `S = S_config + S_elec` (교차항 ≈ 0).

### 2-4. q_rev 신규 메서드/함수 시그니처

```python
def q_rev(
    self,
    V_app,             # array-like [V]
    T: float,          # [K]
    I: float,          # [A] 부호 있음 (방전 > 0, 충전 < 0)
    Q_cell: float,     # [Ah]
    direction: str = "discharge",
) -> np.ndarray:
    """가역 발열률 [W] (Ch2 eq:qrev).

    Returns
    -------
    Q_rev : np.ndarray
        `Q̇_rev = −I·T·∂U_oc/∂T(x)` [W 또는 단위 전류 기준 W/A 등 스케일 주의]
        양수 = 발열, 음수 = 흡열.
    """
    sigma_d  = self._direction_to_sigma(direction)
    dUdT     = self._dUdT_full(V_app, T, sigma_d)      # [V/K]
    return -I * T * dUdT                                # [W]
```

히스테리시스 가역/비가역 분리 (Ch2 eq:hys_rev, L580–593):

```python
def q_rev_hys_avg(self, V_app, T, I_abs, Q_cell):
    """히스 양쪽 평균 ∂U^rev/∂T — 한 사이클 완결 시 사용 (Ch2 eq:hys_rev)."""
    dUdT_dis = self._dUdT_full(V_app, T, sigma_d=+1)
    dUdT_chg = self._dUdT_full(V_app, T, sigma_d=-1)
    dUdT_rev = 0.5 * (dUdT_dis + dUdT_chg)             # 히스 상쇄
    return -I_abs * T * dUdT_rev
```

### 2-5. 비가역 발열 3-분해 (설계 옵션)

Ch2 sec:revheat (L643–649) 명시:

```
Q̇_irr = I²R  +  I·η_ct  +  I·η_diff
          오믹   전하이동 과전압  확산 과전압
```

1차 구현에서는 `Q̇_irr = I·(U_oc − V)` (전체 비가역) 단순 형태만 제공하되, 분해 메서드는 설계 후보로 남긴다 (범위 표시 주석 + NotImplemented 플레이스홀더).

**활성화 엔트로피 혼동 방지** (Ch2 L423–427): `ΔS_{a,j}` (동역학 활성화, `_resolve_lag_length` 경로)와 `ΔS_{rxn,j}` (평형 가역열 경로)는 **완전 별개 슬롯** — 코드에서 `dS_a` 키(운동) ≠ `dS_rxn` 키(열역학).

---

## 3. 흑연 회귀 0-diff 가드 설계

### 3-1. 구조 선택 — 독립 병존 (상속/합성/플래그 불채택)

**결정: 독립 병존(Standalone coexistence)**

- `GraphiteAnodeDischargeDQDV` 클래스 (L221–508): **단 한 글자도 변경하지 않는다**
- `LCOCathodeDQDV`: 별도 클래스, 동일 모듈 수준 함수만 호출
- `LCO_MSMR_LIT`: `GRAPHITE_STAGING_LIT` (L531–560) 뒤에 추가 (기존 상수 불변)

상속을 쓰지 않는 이유: Python 상속은 `super().__init__` 경로에서 기존 `__init__` L221–259의 guard/seed_L_V 로직이 LCO 파라미터로 실행되어 예측 불가 부작용 위험. 합성도 동일 이유.

플래그를 쓰지 않는 이유: 기존 `__init__`, `dqdv`, `curve`에 `if cathode:` 분기를 삽입하면 흑연 코드 라인 수정 = 0-diff 가드 위반.

### 3-2. 회귀 하네스 설계 — byte 일치 검증

```python
# tests/test_regression_graphite.py
# 목적: LCO 코드 추가 후에도 GraphiteAnodeDischargeDQDV.curve()가
#        v1.0.10 기준값과 byte 일치함을 보장.

import numpy as np
import pytest

# 기준값 생성 방법 (1회 실행 후 저장):
# python -c "
#   from Anode_Fit_v1.0.10 import GraphiteAnodeDischargeDQDV, GRAPHITE_STAGING_LIT
#   import numpy as np
#   model = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT)
#   V = np.linspace(0.05, 0.25, 500)
#   ref = model.curve(V, T=298.15, c_rate=0.1, Q_cell=1.0, direction='discharge')
#   np.save('tests/graphite_curve_ref.npy', ref)
# "

@pytest.fixture
def graphite_model():
    from Anode_Fit_v1010 import GraphiteAnodeDischargeDQDV, GRAPHITE_STAGING_LIT
    return GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT)

@pytest.fixture
def V_grid():
    return np.linspace(0.05, 0.25, 500)

def test_graphite_curve_byte_identical(graphite_model, V_grid):
    """흑연 curve() 출력이 v1.0.10 기준값과 bit-for-bit 일치."""
    ref = np.load("tests/graphite_curve_ref.npy")
    out = graphite_model.curve(V_grid, T=298.15, c_rate=0.1, Q_cell=1.0,
                               direction="discharge")
    # np.array_equal는 NaN 위치 포함 완전 동치 확인
    assert np.array_equal(out, ref), (
        f"흑연 curve() 회귀 실패: max |Δ| = {np.max(np.abs(out - ref)):.3e}"
    )

def test_graphite_curve_charge_byte_identical(graphite_model, V_grid):
    """충전 방향도 byte 일치."""
    ref_chg = np.load("tests/graphite_curve_charge_ref.npy")
    out = graphite_model.curve(V_grid, T=298.15, c_rate=0.1, Q_cell=1.0,
                               direction="charge")
    assert np.array_equal(out, ref_chg)

def test_graphite_equilibrium_byte_identical(graphite_model, V_grid):
    """equilibrium() 도 byte 일치."""
    ref_eq = np.load("tests/graphite_eq_ref.npy")
    out = graphite_model.equilibrium(V_grid, T=298.15)
    assert np.array_equal(out, ref_eq)

def test_lco_import_does_not_affect_graphite(V_grid):
    """LCOCathodeDQDV import 후에도 흑연 curve() 불변."""
    # LCO 클래스를 먼저 import하여 모듈 수준 변수 오염 여부 확인
    from Anode_Fit_v1010 import (
        GraphiteAnodeDischargeDQDV, GRAPHITE_STAGING_LIT,
        LCOCathodeDQDV, LCO_MSMR_LIT,
    )
    _ = LCOCathodeDQDV(LCO_MSMR_LIT)    # LCO 인스턴스 생성

    model_g = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT)
    ref = np.load("tests/graphite_curve_ref.npy")
    out = model_g.curve(V_grid, T=298.15, c_rate=0.1, Q_cell=1.0,
                        direction="discharge")
    assert np.array_equal(out, ref)
```

**기준값 파일 생성 절차**:

1. LCO 코드 추가 **전** `__main__` self-test 통과 상태에서 `graphite_curve_ref.npy` 등 3종 저장
2. LCO 코드 추가 **후** `pytest tests/test_regression_graphite.py -v` 실행
3. `np.array_equal` PASS = byte 일치 (float 비교 아님 — 부동소수점 재구성 없음)

---

## 4. Serena 편입 레시피

### 4-1. 편입 대상 심볼 목록

| 심볼 유형 | 심볼 이름 | Serena 작업 | 근거 |
|---------|---------|------------|------|
| 신규 함수 | `_calc_dSe_mol` | `insert_after_symbol('_finite_nonneg')` | L188 뒤 (utility 함수 블록 끝) |
| 신규 상수 | `LCO_MSMR_LIT` | `insert_after_symbol('GRAPHITE_STAGING_LIT')` | L560 뒤 |
| 신규 클래스 | `LCOCathodeDQDV` | `insert_after_symbol('GraphiteAnodeDischargeDQDV')` | L508 뒤 (클래스 끝) |
| 신규 함수 (q_rev 전용) | `_dUdT_full_lco` | `insert_after_symbol('LCOCathodeDQDV')` 또는 메서드로 내부화 | LCO 클래스 메서드로 내부화 권고 |

**기존 심볼 `replace_symbol_body` 0건** — LCO 코드는 전부 신규 추가이며 기존 심볼 수정 없음.  
`__main__` 블록(L567–703): LCO self-test 추가 필요 시 `insert_after_symbol('__main__ block end')` 방식으로 기존 self-test 뒤 append. 기존 self-test 라인은 **단 한 글자도 수정 금지**.

### 4-2. `_calc_dSe_mol` 삽입 레시피

```
mcp__serena__insert_after_symbol(
    symbol_name = "_finite_nonneg",   # L188 기존 utility 함수
    code = """
def _calc_dSe_mol(xi_T1, T, tr):
    \"\"\"LCO T1 전이 MIT 전자 엔트로피 몰당값 [J/(mol·K)].

    Ch1 eq:dSemolar: ΔS_e^mol = N_A·(π²/3)·k_B²·T·∂g/∂x
    eq:dSegate:      ∂g/∂x = −(g_max/Δx_MIT)·σ(z)·[1−σ(z)], z=(x−x_MIT)/Δx_MIT
    eq:gunit:        g_J = g_eV / e_V  (eV⁻¹ → J⁻¹, 나눔)

    Parameters
    ----------
    xi_T1 : float or ndarray
        T1 전이 logistic 점유율 (≈ x-coordinate proxy).
    T : float
        온도 [K].
    tr : dict
        전이 dict. 키: g_max [e/eV], x_MIT, dx_MIT.

    Returns
    -------
    dSe_mol : same shape as xi_T1, [J/(mol·K)], ≤ 0 (삽입 기준).
    \"\"\"
    import math
    # 물리 상수
    pi2_3 = math.pi**2 / 3.0
    kB    = 1.380649e-23   # J/K
    NA    = 6.02214076e23
    eV    = 1.60217663e-19  # J/eV

    g_max_eV = tr.get('g_max', 13.0)     # e/eV
    x_MIT    = tr.get('x_MIT', 0.85)
    dx_MIT   = tr.get('dx_MIT', 0.05)

    # g(E_F) [eV⁻¹] → [J⁻¹]: 나눔
    g_max_J = g_max_eV / eV              # eq:gunit

    # 게이트 미분 ∂g/∂x [J⁻¹]
    z     = (xi_T1 - x_MIT) / dx_MIT
    sig   = 1.0 / (1.0 + np.exp(-z))    # logistic
    dg_dx = -(g_max_J / dx_MIT) * sig * (1.0 - sig)  # ≤ 0

    # 몰당 ΔS_e^mol = N_A · (π²/3) · k_B² · T · ∂g/∂x
    return NA * pi2_3 * kB**2 * T * dg_dx   # J/(mol·K), ≤ 0
"""
)
```

### 4-3. `LCO_MSMR_LIT` 삽입 레시피

```
mcp__serena__insert_after_symbol(
    symbol_name = "GRAPHITE_STAGING_LIT",  # L531–560
    code = """
# ============================================================
# LCO 양극 전이 파라미터 초기값 (MSMR 동형, Ch1 tab:lco-staging)
# 모든 값은 round-trip 피팅 전 tier C 출발점
# ============================================================
LCO_MSMR_LIT = [
    # T1: MIT 전이 (~3.90 V, x = 0.94→0.75)
    dict(U=3.90, dH_rxn=-75000, dS_rxn=-5.0, Q=0.19,
         Omega=0, gamma=0, mit_elec=True,
         g_max=13.0, x_MIT=0.85, dx_MIT=0.05),
    # T2: 질서-무질서 전이 (~4.06 V)
    dict(U=4.06, dH_rxn=-78000, dS_rxn=0.47, Q=0.31,
         Omega=0, gamma=0, mit_elec=False),
    # T3: 질서-무질서 전이 (~4.18 V)
    dict(U=4.18, dH_rxn=-80000, dS_rxn=1.49, Q=0.25,
         Omega=0, gamma=0, mit_elec=False),
]
"""
)
```

### 4-4. `LCOCathodeDQDV` 클래스 삽입 위치

```
mcp__serena__insert_after_symbol(
    symbol_name = "GraphiteAnodeDischargeDQDV",  # L221–508 클래스 끝
    code = """
class LCOCathodeDQDV:
    # ... (§1-5 시그니처 그대로)
    # 내부에서 func_ksi_eq, func_U_j, func_w 등 모듈 수준 함수 공유
    # _calc_dSe_mol 호출 (T1 mit_elec=True 분기)
    # _causal_lowpass 공유 (미래 꼬리 확장 시)
"""
)
```

### 4-5. 코드 소유권 보존 체크리스트

`feedback_code_ownership_scope` 적용:

- [ ] `GraphiteAnodeDischargeDQDV` 클래스 내 식별자 대소문자·정수코드 0 변경
- [ ] `GRAPHITE_STAGING_LIT` dict 키 철자 0 변경 (`dH_rxn`, `dS_rxn`, `Omega` 등)
- [ ] `func_U_j`, `func_ksi_eq`, `func_w`, `_causal_lowpass` 시그니처 0 변경
- [ ] 신규 심볼은 `LCO_` 또는 `lco_` 접두사로 명확 구분
- [ ] 기존 `__main__` self-test 라인 수정 금지 (LCO test는 append)

---

## 5. 그래프 검증 계획

### 5-1. 흑연 회귀 그래프

**목적**: LCO 코드 추가 후 흑연 곡선 형태 불변 시각 확인

```python
# 4-패널 figure:
# (a) 방전 dQ/dV (T=298K, C/10)   — 기준값 vs 현행값 오버레이
# (b) 충전 dQ/dV (T=298K, C/10)
# (c) 잔차 (현행 − 기준): 전 구간에서 0 (기계 엡실론 급)
# (d) 전이별 peak 위치: 4전이 표시 (0.085, 0.120, 0.140, 0.210 V)
```

합격 기준: 잔차 `max(|Δ|) < 1e-12 mAh/V` (부동소수점 재현성)

### 5-2. LCO dQ/dV 개형 확인

**목적**: 3 전이 (T1/T2/T3)의 위치·형태·면적이 문헌과 정합하는지 확인

```python
# 2-패널 figure:
# (a) V 범위 3.7–4.3V, 방전(리튬화) dQ/dV
#     T1≈3.90V, T2≈4.06V, T3≈4.18V 각각 표시
#     각 peak 면적 비 = Q_1:Q_2:Q_3 ≈ 0.19:0.31:0.25 확인
# (b) 온도 효과: T=278/298/318K 오버레이
#     T1 peak의 V 이동 ΔV/ΔT ≈ ΔS_rxn/F 방향 확인 (음의 ΔS → 온도↑ 시 V↓)
```

### 5-3. ∂U_oc/∂T(x) 곡선 개형

**목적**: 연속 블렌드와 이중계산 분리 검증

```python
# 유한차분 검증 (Ch2 파생A 수치 검증):
T1, T2 = 292.15, 298.15
V = np.linspace(0.05, 0.25, 500)  # 흑연 범위
dUdT_fd   = (model_g.equilibrium(V, T2) - model_g.equilibrium(V, T1)) / (T2 - T1)
dUdT_full = model_g._dUdT_full(V, 298.15, sigma_d=+1)

# 합격 기준: max|FD − 완전식| < 1e-7 V/K (부동소수점 정밀도)
# 불합격 시: config 분포 항 누락 또는 이중계산 진단
```

### 5-4. q_rev 부호·개형 확인

**목적**: 흡/발열 부호와 SOC 의존 패턴 검증

```python
# 흑연 반전지, 방전(I > 0), T=298K, C/10
# 기대 개형 (Ch2 sec:revheat L659–666):
#   저x (ξ→1): config 발산 → ΔS > 0 → Q̇_rev = −I·T·ΔS < 0 (흡열)
#   고x (stage 2→1, x≈0.5): 큰 음의 ΔS → Q̇_rev > 0 (발열)
# 부호 역전점: ΔS = 0 크로싱 SOC 위치 기록

# LCO 반전지, 방전, T=298K
# T1 구간 (x≈0.75–0.94): ΔS_e < 0 → Q̇_rev 추가 발열 기여
# T2/T3 구간: ΔS > 0 (Motohashi 2009) → Q̇_rev 흡열 경향
```

### 5-5. 검증 통과 기준 요약

| 검증 항목 | 합격 기준 |
|---------|---------|
| 흑연 회귀 byte 일치 | `np.array_equal` PASS (잔차 < 기계 엡실론) |
| LCO T1/T2/T3 peak 위치 | 문헌 ±0.02V 이내 (초기값; 피팅 전) |
| LCO 면적 보존 | `∫dQ/dV dV ≈ Σ Q_j` (상대오차 < 1e-4) |
| ∂U/∂T 유한차분 일치 | max|FD − 완전식| < 1e-7 V/K |
| q_rev 부호 | 저x=흡열, 고x=발열 방전 패턴 확인 |
| T1 mit_elec 기여 | T1 구간 ΔS_e < 0 (음수 확인) |

---

## 6. 설계 간 정합성 매트릭스

| 설계 항목 | Ch1 근거 | Ch2 근거 | P1 감사 근거 | 코드 라인 |
|---------|---------|---------|------------|---------|
| MSMR 동형 | sec:lco-code L1735–1760, eq:msmr | — | §2-E (LCO 부재 확인) | L221–508 (재사용) |
| MIT 게이트 g(E_F) | sec:lco-electronic, eq:ggate | ssec:elec L381–409 | §2-E | 신규 `_calc_dSe_mol` |
| 단위 변환 (÷ e_V) | eq:gunit | — | — | `_calc_dSe_mol` 내부 |
| 이중계산 금지 | eq:lco-decomp L1699–1701 | ss:파생B L524–537 | — | `_dUdT_full` 슬롯 분리 |
| 완전식 (config 분포) | — | eq:weighted, keybox L668–685 | — | `_dUdT_full` config_term |
| q_rev 기본식 | — | eq:qrev L643–649 | — | `q_rev()` |
| 히스 평균 | — | eq:hys_rev L580–593 | — | `q_rev_hys_avg()` |
| 회귀 0-diff | — | — | §1 (흑연 경로 확인) | `test_graphite_curve_byte_identical` |
| 면적 보존 | — | — | §3 (DC gain=1) | `_causal_lowpass` 공유 (불변) |
| 활성화 ≠ 반응 엔트로피 | eq:Lqfull | L423–427 | — | `dS_a` ≠ `dS_rxn` 키 분리 |

---

## 7. 미결 항목 및 P4 구현 주의사항

1. **`dH_rxn` LCO 초기값 검증**: Ch1 tab:lco-staging의 절대값은 tier C (초기값). 코인 반전지 round-trip 피팅 후 tier 승격 필요 (Ch1 L1729–1733 예고).

2. **x↔V 매핑 상세**: `ξ_{eq,T1}(V)`는 T1 전이의 단일 logistic이므로 x ∈ [0,1]이 아닌 [0, Q_T1] 범위. 조성 x(ξ)를 전체 LCO 조성으로 정규화할 때 `Σ Q_j · ξ_{eq,j}(V)`를 역산하는 음함수 루프가 필요할 수 있음 → 1차에서는 `ξ_{eq,T1}` 직접 proxy로 사용하고, 정확한 x↔V 음함수는 round-trip 피팅 단계에서 구현.

3. **`func_U_j_hys` 사문(dead code)**: L82–91 보존 (P1 결정). `_calc_dSe_mol` 삽입 후에도 이 함수 위치(L82–91) 변경 없음.

4. **LCO `_direction_to_sigma` 재사용**: Ch1 eq:msmr `f = −σ_d` 대응에서 방전(σ_d=+1) = 리튬화. `LCOCathodeDQDV`는 `GraphiteAnodeDischargeDQDV._direction_to_sigma` static method를 **import** 또는 복사 없이 모듈 수준에서 `_direction_to_sigma` 함수로 공유.

5. **`n_work_min` vs LCO 전압 범위**: LCO 작업 격자는 3.7–4.3V (흑연 0.05–0.25V 대비 넓음). `grid_pad` 기본값 0.15V 유지 시 격자 점 수 충분한지 `_build_seed_L_V` 동등 진단 함수로 사전 확인 권고.

6. **`ΔS_rxn` 부호 확인**: LCO `dS_rxn` 키 = `ΔS⁰_j^cat` = 삽입 기준 부호. T1의 음의 `dS_rxn=-5.0`과 전자항 `ΔS_e_mol<0`이 모두 음 → 삽입 시 엔트로피 감소 (Co 격자 정렬). 부호가 틀리면 `∂U/∂T > 0` (온도↑ 시 V↑)가 나오는데 LCO T1에서 기대 방향 확인 필요.

---

**5줄 요약**

1. `LCOCathodeDQDV` 신규 독립 클래스 채택 — 기존 `GraphiteAnodeDischargeDQDV` 단 한 라인도 변경 않고 모듈 수준 함수(`func_ksi_eq`·`func_U_j` 등)만 공유 (MSMR 동형, Ch1 eq:msmr).
2. MIT 전자 엔트로피는 `_calc_dSe_mol` 신규 함수로 T1 전이 루프 내 `dS_rxn` 슬롯에 가산 — eV⁻¹→J⁻¹ 변환은 ÷ e_V (eq:gunit), 몰당 × N_A (eq:dSemolar); 흑연에서는 이 함수 호출 0.
3. ΔS(x) 이중계산 방지: `dS_rxn` 키 = ΔS⁰_j (ξ=1/2, config=0 중심값) 만, config 분포 항 R·ln[ξ/(1−ξ)] / F 는 `_dUdT_full` 내 런타임 자동 계산 (Ch2 eq:weighted + 파생 B).
4. 회귀 0-diff 가드: `np.array_equal` byte 일치 4종 자동화 테스트 (`test_regression_graphite.py`) — LCO import·인스턴스 생성 후에도 흑연 곡선 기준값과 bit-for-bit 동일 요구.
5. 모든 신규 심볼은 `insert_after_symbol` 전용 (기존 심볼 `replace_symbol_body` 0건) — `LCO_MSMR_LIT`는 `GRAPHITE_STAGING_LIT` 뒤, `LCOCathodeDQDV`는 `GraphiteAnodeDischargeDQDV` 뒤, `_calc_dSe_mol`은 `_finite_nonneg` 뒤 삽입.
