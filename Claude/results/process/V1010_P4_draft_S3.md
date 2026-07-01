# V1010 P4 코드개정 설계 드래프트 S3

> ID: S3 | 역할: 독립 설계 드래프트 (설계 제안만, .py/문건 수정 절대 X)
> 근거 소스: Anode_Fit_v1.0.10.py (전체), V1010_P1_code-audit_RESULT.md, graphite_ica_ch1_v1.0.10.tex (sec:lco-map, sec:lco-center, sec:lco-hys, sec:lco-electronic, sec:eqpeak, sec:broadening, sec:lag), graphite_ica_ch2_v1.0.10.tex (전체)

---

## 0. 전제 확인 (compaction 방지 체크포인트)

P1 audit(V1010_P1_code-audit_RESULT.md) 에서 확정된 사실:

- 현재 코드(`Anode_Fit_v1.0.10.py`, 703줄)에 LCO·q_rev·dS_e·cathode 관련 코드 **없음** (grep 확인, P1 audit §3)
- `func_U_j_hys` (L82-91): 死코드, 0 call sites, P1 판정 = 원형 보존
- 면적보존: DC gain = 1.000000 (수치 검증 완료, P1 audit §5)
- `z_cut` docstring 부정확 (L217): minor, P4 대상 아님(P1 verdict 따름)
- 기존 경로 = `GraphiteAnodeDischargeDQDV.curve()` → `dqdv()` → `equilibrium()` + `_resolve_lag_length()` + `_causal_lowpass()`

---

## 1. LCO 양극 dQ/dV 설계

### 1-1. 구조 선택: 신규 독립 클래스 `LCOCathodeDQDV`

**선택 이유:**

기존 `GraphiteAnodeDischargeDQDV` 는 흑연 음극 전용 상수(`GRAPHITE_STAGING_LIT`)와 음극 부호 규약(`σ_d = s = +1` for discharge = delithiation)으로 정의되어 있다. LCO 양극은:

1. **부호 반전**: 방전 = 리튬화(lithiation), 즉 x↑ → 흑연 음극의 방전 방향과 반대 (Ch1 sec:lco-map L295-343)
2. **전압 범위**: ~3.9–4.2 V (흑연 ~0.085–0.210 V와 완전 분리)
3. **MIT 전자 엔트로피 항**: `ΔS_e(x,T)` — 흑연에는 없는 x-의존 추가 항 (Ch1 sec:lco-electronic)
4. **상수 집합**: `LCO_MSMR_LIT` (3 전이 T1/T2/T3, 별도 데이터셋)

합성(composition) 방식도 가능하나, 부호 규약 차이가 클래스 내부 논리 전체에 영향을 미쳐 플래그 분기가 과도하게 증가한다. 독립 클래스가 더 단순하고 흑연 회귀 0-diff를 구조적으로 보장한다.

**일반화 base 클래스 방안을 배제하는 이유:**

공통 base를 만들려면 기존 `GraphiteAnodeDischargeDQDV` 의 `__init__`·`dqdv`·`curve`를 리팩토링해야 하며, 이는 기존 code path를 건드려 흑연 회귀 가드를 위협한다. 신규 독립 클래스는 기존 클래스에 **일절 손대지 않는다**.

### 1-2. MSMR 동형 매핑표

Ch1 sec:lco-map (L295-343) 기준:

| 흑연 음극 (코드 심볼)       | LCO 양극 (Ch1 식)       | 설명                                         |
|-----------------------------|-------------------------|----------------------------------------------|
| `Q_j` (tr['Q'])             | `X_j`                   | 전이 j 용량 분율 (동일 의미)                 |
| `U` (tr['U'])               | `U_j⁰` = `U_j^d(T_ref)` | 전이 중심 전위 (기준온도에서)                |
| `w_j` (func_w 기반)         | `ω_j`                   | 전이 폭 (현상학적 피팅, 흑연과 동일 의미)   |
| `σ_d = +1` (방전=탈리튬)    | `f = −σ_d = −1`         | **★부호 반전**: LCO 방전=리튬화 → `s = -1`  |
| `θ` (Ch1 θ↔ξ)              | `ξ_j` (로지스틱 진행률) | 점유율 정의 동일, θ↔ξ 표기 동형              |
| `Omega` (tr['Omega'])       | `Ω_j`                   | 정규 용액 상호작용 파라미터                  |
| `dH_rxn` (tr['dH_rxn'])     | `ΔH_rxn,j`              | 반응 엔탈피 (삽입 기준, Li 1몰당)            |
| `dS_rxn` (tr['dS_rxn'])     | `ΔS⁰_j = ΔS_rxn,j`      | 중심 표준 반응 엔트로피 (Ch2 파생B 정의)     |
| `dH_a` (tr['dH_a'])         | `ΔH_a,j`                | 활성화 엔탈피 (동역학 tail 용)               |
| `dVdq_qa` (tr['dVdq_qa'])   | `\|dV/dq\|_a`           | 컷점 OCV 기울기                              |
| `n` (tr['n'])               | `n_j`                   | 유효 전자 수 (전이별)                        |

**핵심 부호 규약** (Ch1 sec:lco-map L295-343 명시):

```
LCO 방전 = 리튬화 (x↑) → 흑연 방전(탈리튬, x↓)과 반대
코드 구현: s = -1 을 LCO 방전에 적용
즉, LCO dqdv() 호출 시 direction="discharge" → 내부에서 s=-1 사용
```

### 1-3. MIT 전자 엔트로피 x-의존 항

Ch1 sec:lco-electronic (L928-1160) 에서:

**eq:ggate (L1069-1075):**
```
g(E_F, x) ≈ g_max · [1 - σ((x - x_MIT) / Δx_MIT)]
g_max = 13 e/eV,  x_MIT ≈ 0.85,  Δx_MIT ≈ 0.05
σ(u) = 1 / (1 + exp(-u))  (logistic)
```

**eq:gunit (L1027-1029) — ★단위 변환 경고:**
```
g_J(E_F, x) = g_eV(E_F, x) / e_V   [states/J/atom]
★ 나누기(÷), 절대로 곱하기(×) 아님. 곱하면 10^37 오류
```

**eq:dSegate (L1082-1091):**
```
ΔS_e,j(x,T) = −(π²/3) · k_B² · T · (g_max / Δx_MIT) · σ(u) · (1 − σ(u))
```
여기서 `u = (x − x_MIT) / Δx_MIT`.
선행 마이너스 부호가 삽입 기준 음수(T1 MIT 전이에서 전자 자유도 감소)를 고정한다.

**eq:U1T2 (L1054-1061):**
```
U_1(T) = U_1(T_0) + (ΔS⁰/F)·(T-T_0) + (a_e / 2F)·(T²-T_0²)
```
T² 항의 1/2 인수는 전자 엔트로피 T 선형 적분에서 나온다.

### 1-4. LCO 전이 상수 집합 `LCO_MSMR_LIT` 초기값

Ch1 sec:lco-map (L295-343) 에서 읽은 3 전이 초기값. **이는 피팅 출발점이며 확정값 아님** (Ch1 명시).

| 전이 | 물리        | U (V vs Li/Li⁺) | Q 분율  | Omega  | dH_rxn       | dS_rxn       | n   | dH_a     | dVdq_qa |
|------|------------|-----------------|---------|--------|--------------|--------------|-----|----------|---------|
| T1   | MIT ~3.90V | 3.900           | 0.19    | 3000.0 | -22000.0     | +80.0        | 1.0 | 55000.0  | 0.50    |
| T2   | ord-dis ~4.05V | 4.050       | 0.40    | 5000.0 | -24000.0     | +50.0        | 1.0 | 50000.0  | 0.50    |
| T3   | ~4.17-4.20V | 4.185          | 0.41    | 4000.0 | -23000.0     | +30.0        | 1.0 | 48000.0  | 0.50    |

**주**: `dS_rxn` 값은 Ch1 sec:lco-center (L465-504) "대표 스케일 ΔS_rxn^cat ≈ +80 J/(mol·K)" 에서 추정. T2·T3는 그 절반 스케일로 초기화. T1은 MIT가 ΔS_e를 별도로 들고 있어 dS_rxn과 분리해야 한다(이중계산 주의 — §2에서 다룸).

### 1-5. 클래스 시그니처

```python
class LCOCathodeDQDV:
    """LCO 양극 dQ/dV 모델 (MSMR 동형 3-전이 프레임워크).
    
    방전 = 리튬화(x↑, s=-1).
    T1 전이에만 MIT 전자 엔트로피 항 x-의존 포함.
    흑연 GraphiteAnodeDischargeDQDV 와 독립 — 상호 미영향.
    
    Args:
        transitions: LCO_MSMR_LIT 또는 사용자 제공 리스트
                     (keys: U, Q, Omega, dH_rxn, dS_rxn, n,
                            dH_a, dVdq_qa, [mit_idx=0])
        x: 초기 SOC (0=완전 방전=Li 리튬화 완료, 1=완전 충전)
        Rn: IR 저항 [Ω]
        Cbg: 배경 double-layer 커패시턴스
        chi: 전달 계수 (None = 0.5)
        chi_split: 방향별 전달 계수 분할 함수 (기본 func_chi_d 재사용)
        use_dH_eff: True = Ω 보정 유효 장벽 사용
        z_cut: 꼬리 컷 affinity 변수 (기본 4.357)
        A_cap_RT: affinity 상한 (기본 4.0)
        mit_idx: MIT 전자 엔트로피 적용 전이 인덱스 (기본 0 = T1)
        g_max_eV: g(E_F) 최대값 [e/eV] (기본 13.0)
        x_MIT: MIT 중심 SOC (기본 0.85)
        dx_MIT: MIT 폭 (기본 0.05)
    """
    def __init__(
        self,
        transitions,
        x: float = 0.5,
        Rn: float = 0.0,
        Cbg: float = 0.0,
        chi=None,
        chi_split=func_chi_d,
        use_dH_eff: bool = True,
        z_cut: float = 4.357,
        A_cap_RT: float = 4.0,
        mit_idx: int = 0,
        g_max_eV: float = 13.0,
        x_MIT: float = 0.85,
        dx_MIT: float = 0.05,
    ): ...

    def dqdv(
        self,
        V_app: np.ndarray,
        T: float,
        I_abs: float,
        Q_cell: float,
        s: int = -1,    # ★LCO 방전=리튬화 → s=-1 기본값
    ) -> np.ndarray: ...

    def curve(
        self,
        V_app: np.ndarray,
        direction: str = "discharge",
        c_rate: float = 0.0,
        Q_cell: float = 1.0,
        T: float = 298.15,
    ) -> np.ndarray: ...
```

**`s=-1` 기본값 근거**: Ch1 sec:lco-map (L295-343) 명시 — "방전 = 리튬화" → MSMR 동형에서 `f = -σ_d`, 방전(`σ_d=+1`) 시 `f=-1`, 코드 `s` 인자에 `-1` 대입.

---

## 2. 가역 발열 q_rev 설계

### 2-1. 수학 공식 (Ch2 eq:qrev, L643-649)

```
Q̇_rev = −I·T·∂U_oc/∂T = −(I·T/F)·ΔS(x)
```

여기서 I > 0 = 방전, 부호: ΔS > 0 → Q̇_rev < 0 (흡열), ΔS < 0 → Q̇_rev > 0 (발열).

**ΔS(x) 완전식** (Ch2 sec:revheat keybox L668-685):

```
∂U_oc/∂T(x) = [Σ_j Q_j·g_j(x)·(ΔS⁰_j/F + (R/F)·ln(ξ_j/(1-ξ_j)))]
              / [Σ_j Q_j·g_j(x)]
g_j = ξ_j(1-ξ_j)/w_j

→ Q̇_rev = −I·T·∂U_oc/∂T
```

LCO T1 전이에서는 `ΔS_e(x,T)` 추가:

```
ΔS_total,T1(x,T) = ΔS⁰_T1 + R·ln[ξ_T1/(1-ξ_T1)] + ΔS_e,T1(x,T)
```

### 2-2. ★이중계산 직교 (Ch2 파생 B, L524-537 명시)

**원칙**:
```
ΔS⁰_j (중심 표준값) + R·ln[ξ_j/(1-ξ_j)] (config 분포항)
두 항을 각 한 번씩만. 절대로 config 항을 ΔS⁰_j에 포함하거나 두 번 더하지 않는다.
```

**코드에서 분리 방법**:

1. `dS_rxn` (tr['dS_rxn']) = **ΔS⁰_j만** 저장 (봉우리 중심 `ξ=0.5`, config=0에서의 표준값)
2. config 항 `R·ln[ξ/(1-ξ)]`는 `q_rev()` 내부에서 `ξ_eq` 를 이용해 **별도 계산**
3. LCO T1의 `ΔS_e(x,T)`는 `dS_rxn`과 **별도 인자**로 관리 (`mit_idx` 로 전이 식별)

**구체적 검산**: Ch2 파생 B (L532-537) — "ΔS⁰_j 는 봉우리 중심(ξ=1/2, config=0)의 표준값, R·ln[ξ/(1-ξ)]/F 는 봉우리 내부의 분포 항. 이 두 항이 별개 출처임을 재확인."

### 2-3. 함수/메서드 시그니처

q_rev 는 `LCOCathodeDQDV`의 메서드 + 독립 함수 두 가지 제안:

**방안 A (권장): 독립 함수 `func_q_rev_halfcell`**

```python
def func_q_rev_halfcell(
    transitions,          # list of dicts (U, Q, Omega, dH_rxn, dS_rxn, n, ...)
    V_app: np.ndarray,    # 전위 격자 [V]
    T: float,             # 온도 [K] — T 한 번만
    I: float,             # 전류 [A], I>0=방전
    Q_cell: float,        # 용량 [Ah]
    s: int = -1,          # 방향 부호
    mit_idx: int = -1,    # MIT 전이 인덱스 (-1 = 없음, LCO T1이면 0)
    g_max_eV: float = 13.0,
    x_MIT: float = 0.85,
    dx_MIT: float = 0.05,
) -> np.ndarray:
    """하프셀 가역 발열 Q̇_rev [W] per 전위 포인트.
    
    Q̇_rev = -I·T·∂U_oc/∂T = -(I·T/F)·ΔS(x)
    
    ΔS(x) = 완전식: ΔS⁰_j(중심 표준) + R·ln[ξ_j/(1-ξ_j)](config 분포)
                    + ΔS_e,j(x,T) (MIT 전이만, mit_idx≥0 시)
    
    ★이중계산 금지: dS_rxn = ΔS⁰_j (config=0 중심값만).
                    config 항은 내부에서 별도 계산, dS_rxn에 포함 X.
    
    Ch2 eq:qrev (L643-649), 파생A+B (L439-537), 범위: 하프셀 단독.
    """
    ...
```

**방안 B (보조): `LCOCathodeDQDV.q_rev()` 메서드**

```python
def q_rev(
    self,
    V_app: np.ndarray,
    T: float,
    I: float,
    Q_cell: float,
) -> np.ndarray:
    """wrapper — 내부에서 func_q_rev_halfcell 호출."""
    ...
```

**채택 이유**: 독립 함수로 두면 흑연 음극에도 `GraphiteAnodeDischargeDQDV` 와 함께 재사용 가능하다. 흑연 음극 q_rev는 `mit_idx=-1`로 호출하면 전자 엔트로피 항 없이 동일 코드를 쓴다.

### 2-4. ΔS(x) 조립 내부 알고리즘

```
1. 각 전이 j에 대해 ξ_eq,j(V,T) 계산 (func_ksi_eq 재사용)
2. g_j = ξ_eq,j · (1 - ξ_eq,j) / w_j  (w_j = func_w(T, n_j))
3. dS_center_j = tr['dS_rxn']  ← ΔS⁰_j (config=0 중심값)
4. z_j = ln(ξ_eq,j / (1 - ξ_eq,j))  (극단값 clip 필요: ξ ∈ [ε, 1-ε])
5. dS_config_j = R * z_j  ← 분포 config 항
6. dS_e_j = 0.0 if j != mit_idx else func_dS_e_lco(x_eff, T, g_max_eV, x_MIT, dx_MIT)
7. dS_j = dS_center_j + dS_config_j + dS_e_j   ← 세 항 합산 (이중계산 없음)
8. 분자 += Q_j · g_j · dS_j
9. 분모 += Q_j · g_j
10. dU_dT = (분자/분모) / F  ← ∂U_oc/∂T
11. Q_rev = -I * T * dU_dT
```

**Step 4 clip 필요 이유**: Ch2 sec:config (L419-421) — "config 는 봉우리 내부를 비선형으로 만들고 (±∞ 발산)". `ξ→0` 또는 `ξ→1` 극단에서 `ln(ξ/(1-ξ))` 발산. 안전 clip: `ξ_safe = np.clip(ξ, 1e-12, 1-1e-12)`.

### 2-5. MIT 전자 엔트로피 함수

```python
def func_dS_e_lco(
    x: float,           # SOC (0=완전 방전, 1=완전 충전)
    T: float,           # 온도 [K]
    g_max_eV: float = 13.0,   # g(E_F) 최대값 [e/eV]
    x_MIT: float = 0.85,      # MIT 중심 SOC
    dx_MIT: float = 0.05,     # MIT 폭
) -> float:
    """LCO MIT 전자 엔트로피 부분몰 항 ΔS_e,j(x,T) [J/(mol·K)].
    
    eq:ggate (Ch1 L1069-1075):
        g(E_F, x) ≈ g_max · [1 - σ((x - x_MIT) / dx_MIT)]
    eq:dSegate (Ch1 L1082-1091):
        ΔS_e,j = -(π²/3)·k_B²·T·(g_max_J/dx_MIT)·σ·(1-σ)  [J/(K·atom)]
    → 몰 환산: ΔS_e^mol = N_A · ΔS_e,j  [J/(mol·K)]
    
    eq:gunit (Ch1 L1027-1029): g_J = g_eV / e_V  (★나누기, 곱하기 X)
    """
    e_V = 1.602176634e-19        # J/eV
    N_A = 6.02214076e23          # mol^{-1}
    pi = 3.141592653589793
    
    g_max_J = g_max_eV / e_V    # states/(J·atom)  ← ÷ e_V
    u = (x - x_MIT) / dx_MIT
    sig = 1.0 / (1.0 + np.exp(-u))
    # eq:dSegate: leading minus = insertion-basis negativity locked
    dS_e_atom = -(pi**2 / 3.0) * kB**2 * T * (g_max_J / dx_MIT) * sig * (1.0 - sig)
    return N_A * dS_e_atom       # J/(mol·K)
```

### 2-6. 비가역 열 3-분해 옵션 (Ch2 eq:qrev L643-649)

Ch2 eq:qrev (L643-649):
```
Q̇_irr = I·(U_oc - V)  [=I²R + I·η_ct + I·η_diff, 항상 ≥ 0]
```

`I·(U_oc - V)` 를 다음 세 항으로 분해 가능:
- `I²·R`: ohmic 손실 (IR drop)
- `I·η_ct`: charge transfer 과전압
- `I·η_diff`: diffusion 과전압

이 분해는 선택적 보조 함수로 제공:

```python
def func_q_irr_decomp(
    I: float,
    U_oc: float,
    V_terminal: float,
    Rn: float = 0.0,
) -> dict:
    """비가역 열 3-분해 (옵션, 하프셀 범위 내).
    
    반환: {'q_irr_total': float, 'q_ohmic': float, 'q_ct_diff': float}
    η_ct 와 η_diff 의 추가 분해는 Ch2 범위 밖 (명시 갭).
    """
    q_irr = I * (U_oc - V_terminal)
    q_ohmic = I**2 * Rn
    q_ct_diff = q_irr - q_ohmic
    return {'q_irr_total': q_irr, 'q_ohmic': q_ohmic, 'q_ct_diff': q_ct_diff}
```

**Ch2 범위 제한 준수**: 전셀 합성(`∂U_cell = ∂U_cat - ∂U_an`)은 Ch2 warnbox (L101-106) 명시 "범위 = 코인 하프셀 단독"에 의해 제외. 하프셀 함수로만 제공.

---

## 3. ★흑연 회귀 0-diff 가드

### 3-1. 구조 선택: 독립 클래스 = 자동 0-diff

기존 `GraphiteAnodeDischargeDQDV` 클래스에 **일절 손대지 않는다**. 신규 `LCOCathodeDQDV`를 완전히 독립 클래스로 구현하면, 흑연 코드 경로가 물리적으로 격리되어 회귀 위험이 구조적으로 제거된다.

- 공통 함수(`func_w`, `func_U_j`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass`, `func_chi_d`, `func_dH_a_eff`)는 양측에서 읽기 전용으로 재사용한다 (기존 함수 본체 수정 없음)
- `func_U_j_hys`(L82-91): P1 판정(원형 보존) 그대로 유지, P4에서 건드리지 않음

### 3-2. 회귀 하네스 설계

**byte 일치 검증 전략**:

```python
# tests/test_graphite_regression.py (신규 파일, .py 추가이므로 허용)

import hashlib
import numpy as np
from Anode_Fit_v1_0_10 import GraphiteAnodeDischargeDQDV, GRAPHITE_STAGING_LIT

GRAPHITE_CURVE_HASH = "<<P4 편입 전 실행하여 저장>>"

def test_graphite_curve_byte_match():
    """P4 편입 후 GraphiteAnodeDischargeDQDV.curve() 출력이
    편입 전 해시와 byte-level 일치하는지 검증.
    
    면적보존 DC=1 (P1 §5 확인값) 포함 자동 검증.
    """
    model = GraphiteAnodeDischargeDQDV(
        transitions=GRAPHITE_STAGING_LIT,
        x=0.5, Rn=0.0, Cbg=0.0,
    )
    V_app = np.linspace(0.05, 0.30, 1000)
    result = model.curve(V_app, direction="discharge", c_rate=0.0, Q_cell=1.0, T=298.15)
    
    # byte-level hash
    result_bytes = result.tobytes()
    digest = hashlib.sha256(result_bytes).hexdigest()
    assert digest == GRAPHITE_CURVE_HASH, (
        f"흑연 회귀 실패! hash={digest}, expected={GRAPHITE_CURVE_HASH}"
    )
    
    # 면적보존 검증 (DC gain = 1, P1 audit §5)
    dV = V_app[1] - V_app[0]
    area = np.trapz(result, dx=dV)
    assert abs(area - 1.0) < 1e-4, f"면적보존 실패: area={area:.6f}"
```

**하네스 실행 절차**:
1. P4 편입 **전**: 위 테스트를 실행해 `GRAPHITE_CURVE_HASH` 값 확보
2. 상수를 테스트 파일에 하드코딩
3. P4 편입 **후**: 동일 테스트 재실행 → PASS = 회귀 없음, FAIL = 즉시 정지

### 3-3. 면적보존 DC=1 유지 검증

`_causal_lowpass` 는 P1 audit 에서 DC gain = 1.000000 수치 확인됨. LCO 클래스도 동일 함수를 재사용하므로, 신규 LCO 클래스의 면적 보존도 같은 방식으로 검증 가능:

```python
def test_lco_area_preserving():
    from Anode_Fit_v1_0_10 import LCOCathodeDQDV, LCO_MSMR_LIT
    model = LCOCathodeDQDV(transitions=LCO_MSMR_LIT, x=0.5)
    V_app = np.linspace(3.80, 4.25, 2000)
    result = model.curve(V_app, direction="discharge", c_rate=0.0, Q_cell=1.0, T=298.15)
    dV = V_app[1] - V_app[0]
    area = np.trapz(result, dx=dV)
    assert abs(area - 1.0) < 1e-3
```

---

## 4. Serena 편입 레시피

### 4-1. 심볼별 신규 추가 (`insert_after_symbol`)

P4에서 추가되는 신규 심볼들은 모두 `insert_after_symbol` 을 사용한다. 삽입 순서와 기준점:

| 작업                        | Serena 도구                     | 기준 심볼                        | 근거                           |
|-----------------------------|----------------------------------|----------------------------------|-------------------------------|
| `LCO_MSMR_LIT` 상수 추가   | `insert_after_symbol`           | `GRAPHITE_STAGING_LIT`          | 상수 집합 뒤 자연 위치         |
| `MIT_PARAMS_DEFAULT` 상수   | `insert_after_symbol`           | `LCO_MSMR_LIT`                  | MIT 파라미터 상수              |
| `func_dS_e_lco` 추가        | `insert_after_symbol`           | `func_dH_a_eff`                 | 보조 함수 블록 뒤              |
| `LCOCathodeDQDV` 클래스 추가 | `insert_after_symbol`          | `GraphiteAnodeDischargeDQDV`    | 클래스 블록 직후               |
| `func_q_rev_halfcell` 추가  | `insert_after_symbol`           | `LCOCathodeDQDV`                | 클래스 이후 독립 함수          |
| `func_q_irr_decomp` 추가    | `insert_after_symbol`           | `func_q_rev_halfcell`           | 비가역 보조 함수               |

### 4-2. 기존 심볼 수정 없음

기존 심볼 수정은 **제로**. `replace_symbol_body` 사용 없음.

- `GraphiteAnodeDischargeDQDV`: 건드리지 않음 (독립 클래스 전략)
- `GRAPHITE_STAGING_LIT`: 읽기만, 수정 없음
- `func_w`, `func_U_j`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass`, `func_chi_d`, `func_dH_a_eff`: 재사용만 (수정 없음)
- `func_U_j_hys` (L82-91): P1 원형 보존 판정, 절대 건드리지 않음

### 4-3. 코드 소유권 준수 사항

- 기존 식별자 대소문자 그대로 유지 (`func_ksi_eq`, `GraphiteAnodeDischargeDQDV`, `GRAPHITE_STAGING_LIT` 등)
- 정수/문자열 코드 인코딩 보존 (`s=+1` 방전 규약, `sigma_d` 표기)
- LCO 신규 심볼은 LCO 도메인 명시 (`LCO`, `lco`, `cathode`) — 흑연 네임스페이스와 혼합 금지

### 4-4. 공통 함수 재사용 확인 (`find_symbol` 사전 확인)

편입 전 Serena `find_symbol`로 다음 심볼의 현재 시그니처 확인 필요:

```
func_w(T, n=1.0)
func_U_j(T, dH_rxn, dS_rxn)
func_ksi_eq(T, V_n, U, n=1.0, s=1)
func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)
_causal_lowpass(source_signal, grid_step, lag_length)
func_chi_d(chi, sigma_d)
func_dH_a_eff(dH_a, Omega, chi_d)
```

**이유**: 이들을 LCO 클래스가 내부 호출하므로, 시그니처가 현재 코드와 일치하는지 사전 검증 필요. 변경 없이 그대로 호출한다.

---

## 5. 그래프 검증 계획

### 5-1. 흑연 음극 dQ/dV 회귀 확인

```python
# 기존 curve() 와 완전 동일한 출력 확인
V_an = np.linspace(0.05, 0.30, 2000)
model_an = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT)
dqdv_an = model_an.curve(V_an, direction="discharge", c_rate=0.0, Q_cell=1.0, T=298.15)
```

**기대 개형**: 0.085V, 0.120V, 0.140V, 0.210V 부근 4개 봉우리 (GRAPHITE_STAGING_LIT U값 대응).

### 5-2. LCO 양극 dQ/dV

```python
V_cat = np.linspace(3.80, 4.25, 2000)
model_cat = LCOCathodeDQDV(LCO_MSMR_LIT, mit_idx=0)
dqdv_cat = model_cat.curve(V_cat, direction="discharge", c_rate=0.0, Q_cell=1.0, T=298.15)
```

**기대 개형**:
- T1 (~3.90V): MIT 관련 넓은 봉우리 (Ω > 2RT 가능성, x≈0.75–0.94 범위)
- T2 (~4.05V): order-disorder 봉우리
- T3 (~4.17–4.20V): 세 번째 봉우리
- 전체 면적 ≈ 1.0 (면적보존)
- 양극 방전이므로 V 증가 방향으로 계산 (s=-1, V_cat 오름차순)

**부호 확인**: `s=-1` 사용 시 로지스틱 점유 `ξ = 1/(1 + exp(-s·(V-U)/w))` → V > U에서 ξ 감소 방향 → 리튬화 진행과 일치.

### 5-3. 가역 발열 q_rev 곡선

```python
# 흑연 음극 하프셀
q_rev_an = func_q_rev_halfcell(
    GRAPHITE_STAGING_LIT, V_an, T=298.15, I=0.01, Q_cell=1.0, s=+1, mit_idx=-1
)
# LCO 양극 하프셀
q_rev_cat = func_q_rev_halfcell(
    LCO_MSMR_LIT, V_cat, T=298.15, I=0.01, Q_cell=1.0, s=-1, mit_idx=0
)
```

**기대 개형 (흑연)**:
- Ch2 sec:revheat (L658-666): stage 2→1 (x≈0.5, ~0.085V) 에서 큰 음의 ΔS → 방전 시 발열 (q_rev > 0)
- 저-x 구간 (만충, ~0.210V 근처): ΔS > 0 → 방전 시 흡열 (q_rev < 0)

**기대 개형 (LCO)**:
- T1 (MIT ~3.90V): ΔS_e < 0 (전자 자유도 감소, eq:dSegate 선행 마이너스) → MIT 전이 구간에서 발열 기여
- 전반적 ΔS > 0 (Ch1 sec:lco-center "ΔS_rxn^cat ≈ +80 > 0") → 방전(I>0) 시 주요 구간 흡열

### 5-4. 검증 플롯 체크리스트

```
[ ] 흑연 dQ/dV: 4봉우리 위치·상대 높이 P1 audit 값과 일치
[ ] LCO dQ/dV: 3봉우리 위치 Ch1 sec:lco-map 값과 일치
[ ] 흑연 면적 = 1.0 ± 0.001 (회귀 하네스 pass)
[ ] LCO 면적 = 1.0 ± 0.001
[ ] q_rev 흑연: stage 2→1 구간 발열(+), 저-x 흡열(-) 부호 일치
[ ] q_rev LCO T1: MIT 구간에서 ΔS_e 기여로 발열 증가
[ ] func_dS_e_lco: x=0.85에서 최대 절대값, x≪0.85 또는 x≫0.85에서 ≈0 확인
[ ] ΔS_e 부호: 항상 ≤ 0 (eq:dSegate 선행 마이너스, 삽입 기준)
[ ] 이중계산 확인: q_rev 계산에서 dS_rxn + config (두 번째 config 항 없음)
```

---

## 6. 리스크 분석

### 리스크 R1: LCO 부호 규약 혼동 ★

**내용**: LCO 방전 = 리튬화(s=-1). 흑연 방전(s=+1)과 반대. `curve(direction="discharge")` 내부에서 s=-1을 올바르게 전달해야 한다.

**완화**: `LCOCathodeDQDV.dqdv()` 의 `s` 인자 기본값을 `-1`로 고정, `curve()` 에서 `direction="discharge"` → `s=-1` 매핑을 명시적으로 구현.

### 리스크 R2: eV→J 단위 변환 방향 ★★

**내용**: `g_J = g_eV / e_V` (나누기). 곱하면 10^37 오류. Ch1 eq:gunit (L1027-1029) 명시.

**완화**: `func_dS_e_lco` 내부에서 `g_max_J = g_max_eV / e_V` 한 줄을 명시하고 주석에 eq:gunit 인용. 단위 검증: `g_max_J ≈ 13 / 1.6e-19 ≈ 8.1e19 states/(J·atom)` 의 크기 확인.

### 리스크 R3: config 항 ±∞ 발산

**내용**: `ln(ξ/(1-ξ))` → ξ→0 또는 ξ→1 에서 발산. Ch2 sec:config L419-421 확인.

**완화**: `ξ_safe = np.clip(ξ, 1e-12, 1-1e-12)` 적용. 극단값에서는 q_rev 의 기여가 가중 분자 `Q_j·g_j` 에서 `g_j→0` 으로 자연히 억제됨 (단, 수치 nan 방지용 clip 여전히 필요).

### 리스크 R4: MIT T1 이중계산 복잡성

**내용**: T1 전이의 `dS_rxn` 이 이미 MIT 중심 온도 이동 `ΔS_e` 의 중심값을 흡수했는지 여부. Ch2 파생B 기준으로 `dS_rxn = ΔS⁰_T1` 은 "config=0에서의 표준값"이고 MIT `ΔS_e(x,T)` 는 추가 x-의존 항이다.

**완화**: LCO 피팅 시 `dS_rxn`(T1)과 `func_dS_e_lco` 의 기여를 그래프에서 분리 확인. `dS_rxn=0`으로 두고 MIT 항만 보는 단위 테스트 추가.

### 리스크 R5: 흑연 회귀 하네스 hash 타이밍

**내용**: P4 편입 전 hash를 캡처해야 하는데, hash 캡처를 편입 후에 하면 무의미.

**완화**: 편입 전 master가 hash 캡처 단계를 plan에 명시적 step으로 포함. Serena 편입 작업 전에 반드시 실행.

### 리스크 R6: LCO_MSMR_LIT 초기값 불확실성

**내용**: §1-4의 초기값은 Ch1 "대표 스케일" 에서 추정한 tier-C 수준. 피팅 없이 그래프 개형 검증 목적으로만 사용.

**완화**: 문서에 "초기값 — 피팅 대상" 명시. 실데이터 round-trip 피팅으로 확정 (Ch2 procedurebox L700-716 절차).

---

## 7. 설계 드래프트 완결성 자가 검수

### 기반 소스 근거 확인

| 설계 항목                    | 근거 소스                                | 근거 위치           |
|------------------------------|------------------------------------------|---------------------|
| LCO 독립 클래스 선택         | P1 audit + Ch1 sec:lco-map               | P1 §1, Ch1 L295     |
| MSMR 동형 매핑표             | Ch1 sec:lco-map                          | L295-343            |
| LCO 방전 s=-1                | Ch1 sec:lco-map                          | L295-343            |
| MIT g(E_F) logistic          | Ch1 eq:ggate                             | L1069-1075          |
| eV→J 나누기                  | Ch1 eq:gunit                             | L1027-1029          |
| ΔS_e,j 음수 부호             | Ch1 eq:dSegate                           | L1082-1091          |
| q_rev = -IT·∂U/∂T            | Ch2 eq:qrev                              | L643-649            |
| ΔS 완전식 (중심+config)      | Ch2 파생A keybox                         | L670-685            |
| 이중계산 분리                 | Ch2 파생B                                | L524-537            |
| config ±∞ 발산               | Ch2 sec:config                           | L419-421            |
| func_U_j_hys 원형 보존       | P1 audit §4 死코드 판정                  | P1 §4               |
| 면적보존 DC=1                 | P1 audit §5 수치 검증                    | P1 §5               |
| 하프셀 범위 제한             | Ch2 warnbox                              | L101-106            |

---

## 8. 5줄 요약

1. **채택 구조**: `LCOCathodeDQDV` 독립 신규 클래스 (공통 함수 재사용, `GraphiteAnodeDischargeDQDV` 무수정) + 독립 함수 `func_q_rev_halfcell`·`func_dS_e_lco`·`func_q_irr_decomp`.

2. **핵심 시그니처**: `LCOCathodeDQDV.__init__(transitions, ..., mit_idx=0, g_max_eV=13.0, x_MIT=0.85, dx_MIT=0.05)`, `dqdv(V_app, T, I_abs, Q_cell, s=-1)`, `func_q_rev_halfcell(transitions, V_app, T, I, Q_cell, s=-1, mit_idx=-1, ...)`

3. **회귀 가드**: 독립 클래스 구조로 흑연 코드 경로 물리적 격리 + `SHA-256` hash 하네스(`test_graphite_curve_byte_match`) + 면적보존 DC=1 자동 검증 — 편입 전 hash 캡처 후 편입 후 PASS 확인.

4. **이중계산 처리**: `tr['dS_rxn']` = ΔS⁰_j (봉우리 중심 config=0 표준값만), config 항 `R·ln[ξ/(1-ξ)]`은 `func_q_rev_halfcell` 내부 Step 5에서 별도 계산, MIT `ΔS_e`는 `func_dS_e_lco`로 분리 — 세 항을 각 한 번씩 합산.

5. **리스크**: R2(eV÷e_V 나누기, 10^37 오류) ★★ / R1(LCO s=-1 부호 규약) ★ / R4(T1 dS_rxn과 MIT ΔS_e의 이중계산 경계 확인) — 편입 시 `func_dS_e_lco` 단위 테스트와 부호 검증 필수.
