# Anode_Fit v1.0.10 P4 코드개정 9종 경쟁 설계 드래프트 C2

대상: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`를 흑연 음극 전용 dQ/dV forward 코드에서 LCO 양극 dQ/dV와 가역 발열까지 확장하는 구현 설계.  
작성 범위: 설계 제안만. `.py`/기존 문건/코드 수정 없음.  
직접 정독 범위: 코드 1-614행, P1 audit 1-445행, Ch1 1-1932행, Ch2 1-750행.

## 0. 채택 구조

채택: **신규 클래스 `LCOCathodeDQDV` add-only**. 일반화 base 추출은 이번 P4 편입안에서 제외한다.

근거:

1. P1이 요구한 흑연 회귀 0-diff 조건상 `GraphiteAnodeDischargeDQDV` 본체를 base class로 리팩터링하면 `curve()`/`dqdv()` byte 일치 검증 대상 경로를 직접 건드린다. 기존 클래스는 14개 모듈 함수와 11개 메서드가 이미 닫힌 호출 사슬로 검증되어 있으므로 add-only가 최저 위험이다.
2. Ch1의 MSMR 동형은 전이 logistic, 중심, 폭, 용량 가중의 수학 구조가 같다는 뜻이지, 기존 흑연 클래스의 `s` 하나를 양극에 그대로 재사용해도 된다는 뜻은 아니다. LCO는 방전이 리튬화이고, LCO 전이 좌표는 충전/탈리튬화 때 전위 오름차순으로 진행한다. 따라서 양극에서는 `sigma_current`와 `s_xi`를 분리해야 한다.
3. LCO T1에는 흑연에 없는 electronic entropy plug-in이 필요하다. 이 항은 `g(E_F,x)`의 MIT-logistic gate와 `x <-> xi_eq(V)` 매핑을 요구하므로, 기존 `func_U_j(T,dH,dS)` 단일 호출 경로에 억지로 끼우면 순환 의존과 부호 혼동이 생긴다.

따라서 기존 흑연 클래스는 그대로 두고, 새 LCO 클래스가 기존 순수 helper(`func_w`, `func_ksi_eq`, `func_dU_hys`, `func_U_branch`, `_causal_lowpass`, `_finite*`)만 재사용한다. 공통 base 추출은 P4 이후, 흑연 byte 회귀가 별도 승인된 때만 검토한다.

## 1. LCO 양극 dQ/dV 설계

### 1.1 MSMR 동형 매핑

| Ch1 / MSMR | 코드 설계 심볼 | 의미 |
|---|---|---|
| `X_j` | `Q` | 전이별 용량 가중, peak 면적 |
| `U_j^0` | `U` 또는 `dH_rxn,dS0_rxn` | LCO 전이 중심 전위 |
| `omega_j` | `w` 또는 `n` -> `w_j=nRT/F` | 전이 폭 |
| `x_j = X_j/(1+exp[f(U-U_j^0)/omega_j])` | `xi_eq = logistic[s_xi*(V-center)/w]` | 전이 진행률 |
| `f` | `-sigma_d`와 동형, 구현에서는 `s_xi`로 분리 | 지수 방향 인자 |
| `theta <-> xi` | `x_li = x_hi - xi*(x_hi-x_lo)` | LCO Li 함량과 전이 진행률 매핑 |

중요한 부호 분리:

- `sigma_current`: 전류/히스/열 부호. 방전 `+1`, 충전 `-1`. Ch2 `I>0` 방전 규약과 일치한다.
- `s_xi`: logistic 진행 좌표 부호. LCO 전이표는 충전(탈리튬화) 진행을 전위 오름차순으로 적으므로 기본 `s_xi=+1`.
- `scan_sign`: 인과 꼬리의 시간 진행 방향. 흑연은 `scan_sign=sigma_current`였지만 LCO는 방전 시 전위가 내려가므로 `scan_sign=-sigma_current`가 기본이다.

이 분리를 두지 않고 기존 graphite `s`를 그대로 쓰면, LCO charge/delithiation에서 `xi` 진행 방향과 인과 꼬리 방향이 뒤섞인다.

### 1.2 신규 상수

`LCO_MSMR_LIT`는 `GRAPHITE_STAGING_LIT`와 같은 전이 dict 목록으로 두되, 모든 수치는 **초기값/피팅 seed**로 표시한다. Ch1 근거상 확정 가능한 값만 박고, 근거가 없는 `Q`, `Omega`, `dH_a`, `dVdq_qa`는 피팅 필수 seed로 둔다.

예상 schema:

```python
LCO_MSMR_LIT = [
    {
        "name": "T1_MIT",
        "U": 3.90,
        "x_hi": 0.94,
        "x_lo": 0.75,
        "Q": None,
        "n": 1.0,
        "Omega": None,
        "gamma": 0.0,
        "dS0_rxn": None,
        "electronic": {
            "enabled": True,
            "g_max_eV": 13.0,
            "x_mit": 0.85,
            "dx_mit": 0.05,
        },
    },
    {"name": "T2_order_disorder_a", "U": 4.05, "x_center": 0.55, "dS0_rxn": 0.47, "electronic": {"enabled": False}},
    {"name": "T3_order_disorder_b", "U": 4.17, "x_center": 0.48, "dS0_rxn": 1.49, "electronic": {"enabled": False}},
]
```

`None`은 실제 코드 편입 시 그대로 계산에 넣지 말고 schema validation에서 명시 오류로 막는다. 허위 정밀 `Q`나 `Omega`를 상수처럼 박지 않는다.

### 1.3 핵심 시그니처

```python
def func_lco_x_from_xi(xi, x_hi, x_lo):
    """LCO delithiation progress xi -> Li content x_li."""

def func_lco_g_eF_gate(x_li, g_max_eV=13.0, x_mit=0.85, dx_mit=0.05):
    """MIT logistic gate g(E_F,x), e/eV/atom."""

def func_lco_dS_e_mol(x_li, T, g_max_eV=13.0, x_mit=0.85, dx_mit=0.05):
    """Insert 기준 electronic entropy, J/(mol K), negative at MIT."""

class LCOCathodeDQDV:
    def __init__(self, transitions, Rn=0.0, Cbg=0.0, ...):
        ...

    def dqdv(self, V_app, T, I_abs, Q_cell, direction="discharge"):
        ...

    def curve(self, V_app, direction="discharge", c_rate=0.0, Q_cell=1.0, T=298.15, I_abs=None):
        ...
```

전자항 단위 규칙:

- Ch1 `S_e=(pi^2/3) k_B^2 T g(E_F)`는 자리당 값이다.
- forward 슬롯은 J/(mol K)이므로 `N_A` 환산이 필요하다.
- `g_eV`는 states/eV/atom이므로 `g_J = g_eV / eV_J`를 쓴다. 곱셈이 아니라 나눗셈이다.
- MIT gate 미분은 삽입 기준 `dS_e_mol < 0`가 되도록 leading minus를 둔다.

## 2. 가역 발열 `q_rev` 설계

### 2.1 반응 엔트로피 조립

Ch2의 계산용 완전식은 다음 조립으로 코드화한다.

```python
DeltaS_total(xi, T) =
    dS0_rxn
    + R * log(xi / (1 - xi))
    + dS_e_mol(x_li, T)
```

의미:

- `dS0_rxn`: 봉우리 중심 표준값. 중심 `xi=1/2`에서 configurational 항이 0이므로 이 슬롯은 config=0 기준이다.
- `R*ln[xi/(1-xi)]`: logistic 폭 `w=RT/F`가 이미 만든 봉우리 내부 configurational 분포항.
- `dS_e_mol`: LCO T1 MIT electronic 항. T1에서만 on, T2/T3는 off. 흑연은 0.

**이중계산 직교 규칙**:

1. `dS0_rxn`에 봉우리 내부 config 항을 넣지 않는다.
2. `R ln[xi/(1-xi)]`는 `DeltaS_total()`에서 한 번만 더한다.
3. `dS_e_mol`은 전도 전자 밴드 점유 자유도이므로 config와 가산 가능하지만, T1 MIT gate의 골만 넣는다. 중심값이 이미 `dS0_rxn`에 들어간 electronic baseline은 다시 넣지 않는다.
4. 코드 이름도 이를 강제하도록 `dS0_rxn`와 `include_config_distribution`를 분리한다. `dS_rxn`이라는 모호한 이름 하나에 중심값과 분포항을 섞지 않는다.

### 2.2 q_rev 시그니처

```python
def func_q_rev(I_signed, T, delta_S_mol):
    """
    q_rev = -I*T*dU/dT = -(I*T/F)*DeltaS.
    I_signed > 0: discharge, I_signed < 0: charge.
    """
    return -(I_signed * T / F) * delta_S_mol
```

T는 **한 번만** 곱한다. `dS_e_mol` 자체가 `propto T`이므로, `q_rev`에서 추가로 곱해지는 T와 합쳐 전자항 가역열은 `propto T^2`가 된다. 그러나 `DeltaS_total` 조립 단계에서 `T*dS_e`를 만들면 안 된다.

LCO/흑연 공통 계산용 method:

```python
def reversible_heat(self, V_app, T, I_signed, Q_cell=1.0, direction=None):
    """Return q_rev(V), DeltaS_total(V), xi_j(V) diagnostic bundle."""
```

반환은 최소 `q_rev`만이 아니라 검증을 위해 `DeltaS_total`, 전이별 `xi`, 전이별 contribution을 함께 반환하는 diagnostic option이 필요하다. 그래프 검증에서 이 분해가 있어야 config와 electronic 이중계산을 잡을 수 있다.

### 2.3 비가역 3분해 옵션

가역열과 비가역열을 같은 함수 안에서 섞지 않는다. 별도 옵션 함수로 둔다.

```python
def irreversible_heat_terms(I_abs, R_ohmic=0.0, eta_ct=0.0, eta_diff=0.0):
    return {
        "ohmic": I_abs * I_abs * R_ohmic,
        "charge_transfer": I_abs * eta_ct,
        "diffusion": I_abs * eta_diff,
    }
```

`I^2R + I eta_ct + I eta_diff`는 Ch2의 비가역 3분해로만 둔다. 히스 gap, IR 분극, kinetic tail의 entropy production은 `q_rev`에 절대 합산하지 않는다.

## 3. 흑연 회귀 0-diff 가드

### 3.1 구조 가드

- `GraphiteAnodeDischargeDQDV` symbol body: 무변경.
- `GRAPHITE_STAGING_LIT`: 무변경.
- 기존 순수 함수의 시그니처: 무변경.
- 기존 `curve()`와 `dqdv()`의 direction mapping: 무변경.
- 신규 LCO 클래스는 기존 graphite 클래스의 부모가 되지 않는다. 기존 class hierarchy를 건드리지 않는다.

### 3.2 byte 일치 회귀 하네스

기존 파일을 baseline으로 보존한 뒤, 편입본에서 같은 입력을 넣어 다음을 비교한다.

```python
V = np.linspace(0.03, 0.34, 1000)
model = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)

cases = [
    ("eq", model.equilibrium(V, T=298.15)),
    ("dis_0p2", model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15)),
    ("chg_0p2", model.curve(V, direction="charge", c_rate=0.2, Q_cell=1.0, T=298.15)),
    ("T_profile", model.curve(V, direction="discharge", I_abs=0.2, Q_cell=1.0, T=np.linspace(288.15, 308.15, V.size))),
]
```

검증은 `np.allclose`가 아니라 `array.tobytes()` 동일성으로 한다. scalar 반환도 `np.asarray(value, dtype=np.float64).tobytes()`로 비교한다. 이 byte gate가 실패하면 P4 편입 중단이다.

### 3.3 면적보존 DC=1 유지

추가 회귀:

- 평형 peak: 전이별 `trapz(Q_j*xi*(1-xi)/w, V)`가 `Q_j`에 수렴해야 한다.
- lowpass: `_causal_lowpass` 계수 `[1-rho]/[1,-rho]`의 DC gain=1을 수치 step signal로 확인한다.
- 꼬리 branch: `L_V < min_lag_grid_steps*grid_step`에서는 기존 평형종으로 떨어져야 한다.

LCO 클래스에도 같은 면적 gate를 적용하되, LCO의 `Q`가 확정 seed가 아니면 `sum(Q_j)` 정규화 전후를 분리해서 보고한다.

## 4. Serena 편입 레시피

add-only 원칙:

1. `insert_after_symbol("func_chi_d")`
   - `func_lco_x_from_xi`
   - `func_lco_g_eF_gate`
   - `func_lco_dS_e_mol`
   - `func_reaction_entropy_mol`
   - `func_q_rev`
   - `irreversible_heat_terms`

2. `insert_after_symbol("GRAPHITE_STAGING_LIT")`
   - `LCO_MSMR_LIT`

3. `insert_after_symbol("GraphiteAnodeDischargeDQDV")`
   - `class LCOCathodeDQDV`

4. `replace_symbol_body`
   - 기본값: 없음.
   - 필요한 기존 심볼 없음. 기존 graphite 경로를 건드리는 replace가 발생하면 편입 중단 후 별도 승인 필요.

소유권 보존:

- 기존 식별자, 대소문자, 정수/문자열 코드, 한글 주석/문구 변경 금지.
- `func_U_j_hys`는 P1 판정대로 死코드 보존. 삭제나 시그니처 정리는 하지 않는다.
- `z_cut` docstring 부정확, `n<=0` guard 등 P1 후보는 이번 LCO/q_rev 편입과 직접 연동되지 않으면 수정하지 않는다. 추가 후보로만 남긴다.

## 5. 그래프 검증 계획

### 5.1 흑연

- 기존 self-test 조건과 같은 전압창 `0.03-0.34 V`.
- `equilibrium`, discharge 0.2C, charge 0.2C, T(V) profile을 baseline과 byte 비교.
- 별도 그래프는 기존 결과와 overlay해서 완전 중첩되어야 한다. 눈검증보다 byte gate가 우선이다.

### 5.2 LCO dQ/dV

- 전압창: `3.75-4.25 V` 기본, T4 옵션을 켜면 `4.6 V`까지 확장.
- 기대 개형: T1 MIT peak `~3.90 V`, T2 `~4.05 V`, T3 `~4.17-4.20 V`.
- `direction="charge"`에서는 delithiation 진행이 전위 오름차순이고, `direction="discharge"`에서는 인과 꼬리가 전위 내림차순 진행을 따라야 한다.
- T1 electronic gate on/off 비교: on일 때 다온도에서 T1의 `dU/dT` 이동률이 T 의존 곡률을 가진다. T2/T3는 config/vib 중심값 위주다.

### 5.3 q_rev

- `DeltaS_total(V)`와 `q_rev(V)`를 함께 plot한다.
- 방전 `I>0`에서 `DeltaS>0`이면 `q_rev<0` 흡열, `DeltaS<0`이면 `q_rev>0` 발열이어야 한다.
- T1에서 `dS_e_mol`만 별도 plot해 삽입 기준 음의 골, 탈리튬화 기준 방출 봉우리가 MIT 중심 `x_mit~0.85`에 국소하는지 확인한다.
- `q_rev`와 `q_irr`는 같은 plot에 합산하지 않고 stacked diagnostics로만 보여준다.

## 6. 리스크와 중단 조건

- **양극 부호 리스크**: `sigma_current`, `s_xi`, `scan_sign` 중 하나라도 기존 graphite `s`로 뭉개지면 LCO charge/discharge 꼬리 방향이 틀어진다. LCO 클래스 설계의 핵심 gate다.
- **전자항 단위 리스크**: `g_eV`를 `eV_J`로 나누지 않거나 `N_A` 환산을 누락하면 `dS_e`가 각각 극대/극소로 틀어진다.
- **이중계산 리스크**: `dS0_rxn`에 config 분포를 포함해 놓고 `R ln[xi/(1-xi)]`를 또 더하면 Ch2 파생 B 위반이다.
- **흑연 회귀 리스크**: 기존 클래스 body replace가 발생하면 0-diff 보장이 사라진다. add-only가 깨지는 순간 편입을 멈춘다.
- **문헌 seed 리스크**: LCO `Q`, `Omega`, `dH_a`, `dVdq_qa`는 현재 문건에서 신뢰값으로 확정되지 않았다. 코드 상수에 허위 정밀값을 박지 말고 schema에서 피팅 필수로 표시한다.

## 7. 완료 후 5줄 요약

1. 채택 구조: 기존 `GraphiteAnodeDischargeDQDV` 무변경, 신규 `LCOCathodeDQDV` add-only.
2. 핵심 시그니처: `func_lco_dS_e_mol`, `func_reaction_entropy_mol`, `func_q_rev`, `LCOCathodeDQDV.curve/dqdv/reversible_heat`.
3. 회귀 가드: graphite `curve()`/`dqdv()`/`equilibrium()`은 baseline 대비 `tobytes()` byte 일치, 면적보존 DC=1 별도 확인.
4. 이중계산 처리: `dS0_rxn`은 config=0 중심값, `R ln[xi/(1-xi)]`는 한 번만, T1 `dS_e_mol`은 MIT electronic 골만 추가.
5. 리스크: LCO 부호 3분리, eV->J 나눗셈과 `N_A` 환산, 미확정 LCO seed 허위 정밀값 금지.
