# V1010 P4 설계 드래프트 — 드래프터 S1

**드래프터 ID**: S1  
**작성일**: 2026-07-01  
**대상 파일**: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` (703줄, 수정 X)  
**출력 종류**: 설계 제안만 — `.py`·문건 수정 절대 X  

---

## 0. 정독 커버리지 선언

| 파일 | 정독 범위 | 상태 |
|------|-----------|------|
| `Anode_Fit_v1.0.10.py` | L1-703 전체 (모듈함수 14 + 클래스 11메서드 + 상수) | ✅ 완료 |
| `V1010_P1_code-audit_RESULT.md` | L1-446 전체 | ✅ 완료 |
| `graphite_ica_ch1_v1.0.10.tex` | L1-1933 전체 (L1-1666 + L1667-1933) | ✅ 완료 |
| `graphite_ica_ch2_v1.0.10.tex` | L1-751 전체 | ✅ 완료 |

---

## D1. LCO 양극 dQ/dV 설계

### D1.1 클래스 구조 채택: 단일 범용 클래스 (별도 하위 클래스 X)

**채택**: 기존 `GraphiteAnodeDischargeDQDV`를 별도 LCO 전용 하위 클래스로 분기하지 않는다.  
대신 `LCO_STAGING_LIT` dict와 전자 엔트로피 plug-in 함수를 신규 추가하는 **파라미터 교체 + 1항 추가** 방식을 채택한다.

**근거**:
- Ch1 sec:lco-code (L1735-1760) 명시: "같은 코드가 LCO를 그린다. 구조 변경 0으로 LCO에 적용되며, 바뀌는 것은 단 둘 — (i) 전이 파라미터 교체 (ii) 전자 엔트로피 항 plug-in"
- MSMR 동형 (Ch1 eq:msmr, L1739): `x_j = X_j / (1 + exp[f(U-U_j⁰)/ω_j])` 구조가 Ch1 `func_ksi_eq`와 1:1 동형 — 방향 인자 `f ↔ −σ_d` 포함
- P1 audit 확인: `func_ksi_eq`·`func_U_j`·합산 N0-N9 스파인은 전이 dict만 받으므로, 그 dict을 교체하면 클래스 코드 터치 없이 LCO 곡선이 나온다
- 하위 클래스 도입 시 `__init__`·`dqdv`·`curve` 시그니처 중복 부담 + 회귀 위험 증가 → YAGNI 원칙으로 기각

**주의**: 전자 엔트로피 항은 `func_U_j` 내부가 아니라 **전이 dict의 `dS_rxn` 값에 온도·조성 의존 함수를 반영**하거나, 별도 모듈 함수 `func_dSe_elec`를 신규 추가해 `dqdv`가 해당 전이에만 호출하는 방식으로 처리 (§D1.3 참조).

---

### D1.2 MSMR 동형 매핑 테이블 (코드 심볼 ↔ Ch1 수식)

| 개념 | MSMR (Ch1 eq:msmr, L1739) | Ch1 코드 심볼 | 비고 |
|------|---------------------------|---------------|------|
| 전이별 총 용량 가중 | $X_j$ | `Q` (dict 키) | `Q_cell` 비율 단위 |
| 평형 중심 전위 | $U_j^0$ | `U` 또는 `(dH_rxn, dS_rxn)` (dict 키) | `func_U_j(dH_rxn, dS_rxn, T)` |
| 로그 폭 | $\omega_j$ | `w` 또는 `n` (dict 키) | `func_w(n, T) = n·R·T/F` |
| 방향 인자 | $f = \pm 1$ | `−σ_d` (`s`·`σ_d` 내부 변수) | Ch1 L1745: `f ↔ −σ_d`, 지수부호 일치 |
| 점유 진행률 | $x_j / X_j$ | `ξ_eq` (`func_ksi_eq` 반환) | `θ = 1 − ξ` (Ch2 eq:logistic) |
| 반응 엔트로피 중심값 | $\Delta S_{\rm rxn,j}^0$ | `dS_rxn` (dict 키) | 봉우리 중심 표준값 (Ch2 파생 B 정의) |
| 전이별 위치 이동 | $\partial U_j / \partial T = \Delta S / F$ | `func_U_j` 내 `dS_rxn / F` 항 | L76-80 코드 |
| 방향별 분기 중심 | $U_j^d$ | `func_U_branch(...)` | L120-134 |

**LCO 음극 부호 규약** (Ch1 sec:lco-map L303-309):  
- 방전 = Li⁺ LCO에 삽입 (리튬화), Co⁴⁺ → Co³⁺, `x↑`, `V↓`  
- 흑연과 동일: 방전 `σ_d = +1`, 충전 `σ_d = −1`  
- ξ_j: 탈리튬화 진행률 (ξ→1 = Li 희박 = 충전 완료 방향)  

---

### D1.3 LCO_STAGING_LIT 상수 dict 설계

```python
# 신규 추가 심볼: LCO_STAGING_LIT
# 위치: GRAPHITE_STAGING_LIT (L531-560) 다음에 insert_after_symbol
# 키 구조: GRAPHITE_STAGING_LIT와 동일 (사용자 코드 소유권 보존)

LCO_STAGING_LIT: List[Dict[str, Any]] = [
    {
        # T1 — MIT (Metal-Insulator Transition) ~3.90 V
        # Ch1 sec:lco-gate L1063-1125: g_max=13 e/eV, x_MIT≈0.85, Δx_MIT≈0.05
        # Ch1 sec:lco-center L465-507: ∂U_j/∂T ≈ +0.83 mV/K (Swiderska-Mocek)
        #   → ΔS_rxn ≈ +80 J/(mol·K) [tier B, 스케일 참고값 — 피팅 필수]
        # 전자 엔트로피 플래그: T1만 MIT 게이트 활성
        "U":           3.90,           # V @ 298.15 K (초기값; 피팅 대상)
        "dH_rxn":      None,           # J/mol — U 직접 지정 시 None 허용
        "dS_rxn":      80.0,           # J/(mol·K) [tier B; round-trip 피팅 필수]
        "Q":           0.20,           # Q_cell 비율 (초기값)
        "Omega":       0,              # J/mol (초기값; T1은 MIT형 — 추후 피팅)
        "dH_a":        50000,          # J/mol (초기값)
        "dS_a":        0.0,
        "dVdq_qa":     0.0,
        "n":           1,
        # ★신규 키: 전자 엔트로피 활성 플래그 및 MIT 게이트 파라미터
        "elec_entropy": True,          # True → func_dSe_elec 호출
        "g_max_eV":    13.0,           # e/eV (Ch1 eq:ggate L1068-1072)
        "x_MIT":       0.85,           # 무차원 조성 (Ch1 L1071)
        "dx_MIT":      0.05,           # 전이 폭 (Ch1 L1071)
    },
    {
        # T2 — order-disorder (a) ~4.05 V
        # Ch1 tab:lco-staging: T2 전이 (ord-dis a)
        "U":           4.05,
        "dH_rxn":      None,
        "dS_rxn":      0.47,           # J/(mol·K) [Motohashi 2009, tier B]
        "Q":           0.30,
        "Omega":       0,
        "dH_a":        50000,
        "dS_a":        0.0,
        "dVdq_qa":     0.0,
        "n":           1,
        "elec_entropy": False,
        "g_max_eV":    0.0,
        "x_MIT":       0.0,
        "dx_MIT":      1.0,            # 0으로 나눔 방지
    },
    {
        # T3 — order-disorder (b) ~4.17-4.20 V
        # Ch1 tab:lco-staging: T3 전이 (ord-dis b)
        "U":           4.18,
        "dH_rxn":      None,
        "dS_rxn":      1.49,           # J/(mol·K) [Motohashi 2009, tier B]
        "Q":           0.50,
        "Omega":       0,
        "dH_a":        50000,
        "dS_a":        0.0,
        "dVdq_qa":     0.0,
        "n":           1,
        "elec_entropy": False,
        "g_max_eV":    0.0,
        "x_MIT":       0.0,
        "dx_MIT":      1.0,
    },
]
```

**키 설계 근거**:
- 기존 `GRAPHITE_STAGING_LIT` (L531-560) 키 구조 완전 보존 (사용자 코드 소유권)
- 신규 키 `elec_entropy`, `g_max_eV`, `x_MIT`, `dx_MIT`만 추가
- 흑연의 `elec_entropy` 키 부재 시 → `False`로 처리 (백워드 호환)
- `dH_rxn=None` + `U` 직접 지정: `func_U_j`가 이미 L76-80에서 `dH_rxn`으로 `U` 역산하므로, `U` 직접 입력 경로는 **기존 코드 수정 없이** `dH_rxn = -F*U + T_ref*dS_rxn` 변환으로 처리 가능 (master가 결정)

**T1 위치·ΔS_rxn 근거 (tier 명시)**:
- `U = 3.90 V`: Ch1 sec:lco-gate L1068 "MIT (~3.90 V)" [tier A, 문헌 정합]  
- `dS_rxn = 80.0`: Swiderska-Mocek 2019 "∂φ/∂T ≈ +0.83 mV/K → ΔS ≈ +80 J/(mol·K)" [tier B, 스케일만 — round-trip 피팅 전까지 신뢰값 아님]  
- T2/T3 `dS_rxn`: Motohashi 2009 초기값 [tier B]

---

### D1.4 MIT g(E_F) 전자 엔트로피 함수 설계

**신규 함수**: `func_dSe_elec`

**물리식 (Ch1 eq:dSegate L1081-1091, eq:dSemolar L1017-1022)**:
$$\Delta S_{e,j}^{\rm mol}(x, T) = \frac{\pi^2}{3} \cdot R \cdot k_B \cdot T \cdot \frac{\partial g(E_F, x)}{\partial x}$$

게이트 인자 (Ch1 eq:ggate L1068-1072):
$$g(E_F, x) = g_{\max} \left[1 - \sigma\!\left(\frac{x - x_{\rm MIT}}{\Delta x_{\rm MIT}}\right)\right]$$

$$\Rightarrow \frac{\partial g}{\partial x} = -\frac{g_{\max}}{\Delta x_{\rm MIT}} \cdot \sigma(z)(1-\sigma(z)), \quad z = \frac{x - x_{\rm MIT}}{\Delta x_{\rm MIT}}$$

닫힌식 (Ch1 eq:dSegate):
$$\Delta S_{e,j}^{\rm mol} = -\frac{\pi^2}{3} \cdot R \cdot k_B \cdot T \cdot \frac{g_{\max}}{\Delta x_{\rm MIT}} \cdot \sigma(z)(1-\sigma(z)) \quad [< 0, \text{ 삽입 기준}]$$

**단위 변환 주의** (Ch1 eq:gunit L1026-1030):
- `g_max_eV` 입력 단위: e/eV  
- J 단위로 변환: `g_max_J = g_max_eV / e_V` (**나누기**, 곱하기 아님)  
- 곱하면 오차 ≈ 4×10³⁷배 (Ch1 명시)
- `e_V = 1.602176634e-19` (J/eV)

**함수 시그니처**:
```python
def func_dSe_elec(
    xi_eq: float,
    T: float,
    g_max_eV: float,
    x_MIT: float,
    dx_MIT: float,
) -> float:
    """
    LCO T1 MIT 전자 엔트로피 부분몰 기여 (몰당, 삽입 기준).

    Parameters
    ----------
    xi_eq : float
        T1 전이의 탈리튬화 진행률 ξ_eq,1(V) — 조성 x 의 프록시.
        x = 1 − ξ_eq (삽입 기준 점유율 θ = 1 − ξ)로 내부 변환.
        Ch1 sec:lco-code L1725-1728: x ↔ ξ_eq,1(V) 좌표 매핑.
    T : float
        온도 [K].
    g_max_eV : float
        Fermi 준위 최대 상태밀도 [e/eV].
        초기값 13.0 (Ch1 eq:ggate).
    x_MIT : float
        MIT 중심 조성 (무차원, 삽입 기준).
        초기값 0.85 (Ch1 eq:ggate).
    dx_MIT : float
        MIT 전이 폭 (무차원).
        초기값 0.05 (Ch1 eq:ggate).

    Returns
    -------
    float
        ΔS_e,j^mol [J/(mol·K)], 항상 ≤ 0 (삽입으로 g(E_F) 감소).
        MIT 게이트 밖에서 ≈ 0 (σ(z)·(1−σ(z)) → 0).
    """
    ...
```

**내부 계산 로직**:
```
x = 1.0 - xi_eq           # ξ → θ = 1-ξ → x (삽입 기준 조성)
z = (x - x_MIT) / dx_MIT  # 게이트 인자
sigma_z = 1.0 / (1.0 + exp(-z))   # logistic (기존 func_ksi_eq 패턴)
g_max_J = g_max_eV / e_V  # 단위 변환: e/eV → J⁻¹  [÷ e_V, NOT ×]
# ΔS_e^mol = −(π²/3)·R·kB·T·(g_max_J/dx_MIT)·σ(z)·(1−σ(z))
dSe = -(pi**2 / 3.0) * R * kB * T * (g_max_J / dx_MIT) * sigma_z * (1.0 - sigma_z)
return dSe
```

**T² 위치 이동** (Ch1 eq:U1T2 L1054-1057):
$$U_1(T) = U_1(T_0) + \frac{\Delta S_0}{F}(T-T_0) + \frac{a_e}{2F}(T^2 - T_0^2)$$
여기서 $a_e = -\frac{\pi^2}{3} R \frac{k_B}{e_V} \frac{g_{\max}}{\Delta x_{\rm MIT}} \sigma(z)(1-\sigma(z))$.  
이 T² 보정은 `dS_rxn` 슬롯의 `dSe`가 온도 의존이므로 `func_U_j` 내에서 `T`를 1회만 사용하는 한 이 T 선형·T²효과가 자동 누적된다 — 추가 함수 불필요.

---

## D2. 가역열 q_rev 설계

### D2.1 물리식 (Ch2 eq:qrev L644-645)

$$\dot{Q}_{\rm rev} = -I \cdot T \cdot \frac{\partial U_{\rm oc}}{\partial T} = -\frac{I \cdot T}{F} \cdot \Delta S(x)$$

**∂U_oc/∂T 완전식** (Ch2 sec:revheat keybox L672-684):
$$\frac{\partial U_{\rm oc}}{\partial T}(x) = \frac{\displaystyle\sum_j Q_j \, g_j(x) \left[\frac{\Delta S_j^0}{F} + \frac{R}{F}\ln\frac{\xi_j}{1-\xi_j}\right]}{\displaystyle\sum_j Q_j \, g_j(x)}, \quad g_j = \frac{\xi_j(1-\xi_j)}{w_j}$$

**비가역 3-분해** (Ch2 eq:qrev L643):
$$\dot{Q} = \underbrace{I(U_{\rm oc} - V)}_{\dot{Q}_{\rm irr} \geq 0} - \underbrace{I \cdot T \cdot \frac{\partial U_{\rm oc}}{\partial T}}_{\dot{Q}_{\rm rev}}$$
- `Q_irr = I * (U_oc - V)` ≥ 0 (과전압 소산, Chapter 1의 동역학 꼬리가 만드는 entropy production)
- `Q_rev = -I*T*(∂U_oc/∂T)` (부호 양방향: ΔS > 0 이면 방전 시 흡열)

---

### D2.2 함수 시그니처 설계

**신규 함수**: `func_dUdT_rev`

```python
def func_dUdT_rev(
    xi_eq_arr: np.ndarray,
    dS_rxn_arr: np.ndarray,
    Q_arr: np.ndarray,
    w_arr: np.ndarray,
) -> float:
    """
    평형 전위의 온도 계수 ∂U_oc/∂T — 겹침 가중 완전식.

    Ch2 sec:revheat keybox 의 완전식 (겹침 가중 중심값 + 봉우리 내부 config).

    Parameters
    ----------
    xi_eq_arr : np.ndarray, shape (n_transitions,)
        전이별 평형 탈리튬화 진행률 ξ_eq,j 배열.
    dS_rxn_arr : np.ndarray, shape (n_transitions,)
        전이별 중심 표준 반응 엔트로피 ΔS⁰_j [J/(mol·K)].
        정의: 봉우리 중심 ξ_j=0.5 에서의 값 (Ch2 파생 B).
        ★이중계산 금지: config 항 R·ln[ξ/(1-ξ)] 는 내부에서 추가하므로
          이 입력에 config 를 포함시키면 이중계산임.
    Q_arr : np.ndarray, shape (n_transitions,)
        전이별 용량 가중 Q_j.
    w_arr : np.ndarray, shape (n_transitions,)
        전이별 logistic 폭 w_j [V].

    Returns
    -------
    float
        ∂U_oc/∂T [V/K].
        가역열 = -I*T*(반환값) [W].

    Notes
    -----
    봉우리 내부 config 항 (R/F)·ln[ξ/(1-ξ)] 는 내부에서 계산 (Ch2 L298-308).
    히스테리시스 분기 평균은 호출 측에서 처리 (Ch2 eq:hys_rev L582-584).
    """
    ...
```

**신규 함수**: `func_qrev`

```python
def func_qrev(
    I: float,
    T: float,
    dUdT: float,
) -> float:
    """
    가역(엔트로피) 발열 q_rev [W/Q_cell].

    Ch2 eq:qrev: q_rev = -I·T·(∂U_oc/∂T).
    T는 1회만 곱함 (Ch2 L644: "-I·T·∂U_oc/∂T").

    Parameters
    ----------
    I : float
        전류 [A/Q_cell] (방전 I > 0).
    T : float
        온도 [K] — 1회만 곱힘.
    dUdT : float
        ∂U_oc/∂T [V/K] (func_dUdT_rev 반환값).

    Returns
    -------
    float
        q_rev [W/Q_cell].
        ΔS > 0 이면 방전 시 흡열 (q_rev < 0).
        ΔS < 0 이면 방전 시 발열 (q_rev > 0).
    """
    return -I * T * dUdT
```

---

### D2.3 ★이중계산 직교성 — 코드 분리 방법 (최중요)

**원칙** (Ch2 warnbox L294-308, Ch2 파생 B L524-537):

`ΔS(x) = ΔS⁰_j` (중심 표준값) `+ R·ln[ξ/(1-ξ)]` (분포 config, logistic 폭이 담음) `+ δS_vib/e(x)` (MIT 급변 시만)

**코드 분리 설계**:

```
                    ┌───────────────────────────────────────────┐
                    │ dS_rxn 슬롯 (전이 dict 키)               │
                    │ = ΔS⁰_j (중심 표준값, config=0)          │
                    │ ★ config 항 포함하면 이중계산           │
                    └─────────────────┬─────────────────────────┘
                                      │
                    ┌─────────────────▼─────────────────────────┐
                    │ func_dUdT_rev 내부                        │
                    │ 자동 추가: (R/F)·ln[ξ_j/(1-ξ_j)]        │
                    │ (봉우리 내부 config 분포 항)              │
                    │ Ch2 eq:single_config L527-530             │
                    └───────────────────────────────────────────┘
```

**구현 근거**:
- Ch2 수치 검증 (L486-494): 완전식(config 포함)은 유한차분과 부동소수점 정밀도 일치; 단순식(config 없음)은 최대 0.18 mV/K 체계적 오차
- config 항 R·ln[ξ/(1-ξ)]은 `func_ksi_eq`가 이미 계산한 `xi_eq`에서 즉시 평가 가능
- **★핵심**: `ξ_j → 0` 또는 `ξ_j → 1` 에서 `ln` 발산 — 수치 안전가드 필요
  - 제안: `xi_clipped = np.clip(xi_j, 1e-10, 1.0 - 1e-10)` 후 `np.log(xi_clipped / (1.0 - xi_clipped))`
  - 발산은 물리적 (Ch2 L248-255) — 실제 데이터에서 희박·만충 극한은 보통 범위 밖

**LCO 전자 엔트로피 직교성** (Ch1 sec:lco-decomp L1703-1710):
- config(Li 배열) vs 전자 엔트로피(밴드 점유): 서로 다른 자유도 → 근사적 직교
- 가산성: `Z ≈ Z_config · Z_elec` → `S = S_config + S_elec`
- 무이중계산: config 슬롯 = 중심값만, elec 슬롯 = MIT 게이트만 → 겹침 없음

---

## D3. ★흑연 회귀 0-diff 가드 설계

### D3.1 구조 채택: 플래그(Flag) 방식

**채택**: 상속(Inheritance) 또는 합성(Composition) 대신 **전이 dict 키 기반 조건 분기** 방식.  
`GraphiteAnodeDischargeDQDV.dqdv` 경로는 **완전 무수정**.

**근거**:
- P1 audit (CONFIRMED): `_causal_lowpass` DC gain=1, 넓이 보존 ∫=1.000000 → 기존 경로 변경 시 검증 필요
- 기존 `dqdv` 경로의 변경은 회귀 위험 최대화 — 현재 코드 703줄 전체가 흑연 검증 완료 상태
- `elec_entropy` 플래그 (D1.3 설계)를 전이 dict에 추가하면, 흑연 전이 dict에는 해당 키 부재 → 코드가 `False`로 처리 → 흑연 경로 완전 무수정
- 플래그 결여 시 기본값 `False` 처리는 **기존 코드 호출 측 수정 없음** 원칙과 일치

**흑연 경로 비교 기준점 (byte-match 회귀 하네스)**:

```python
# 회귀 하네스 설계 (신규 추가, __main__ self-test 블록 확장)
# 위치: L567- __main__ 블록 (L703 이후 insert_after_symbol 활용)
# 기존 self-test 가 curve() 호출 결과를 저장 → 확장 후 결과와 비교

# ① 확장 전 기준값 생성
ref_discharge = model_graphite.curve(V_arr, direction="discharge", c_rate=0.1)
ref_charge    = model_graphite.curve(V_arr, direction="charge",    c_rate=0.1)

# ② LCO 관련 코드 추가 후 동일 모델로 재실행
# ③ 차이가 머신 엡실론 이내인지 확인
assert np.allclose(new_discharge, ref_discharge, atol=0, rtol=0), "REGRESSION: graphite dqdv changed"
assert np.allclose(new_charge,    ref_charge,    atol=0, rtol=0), "REGRESSION: graphite dqdv changed"
```

**넓이 보존 DC=1 보존** (P1 audit 확인):
- `_causal_lowpass`의 DC gain=1 성질 (L168-188): 수정하지 않으므로 자동 보존
- 평형 peak ∫ = Q_j (P1 audit): 흑연 경로 무수정이므로 자동 보존
- LCO 신규 경로에서도 동일 `_causal_lowpass` 재사용 → 넓이 보존 상속

---

### D3.2 회귀 하네스 설계 (상세)

```
목표: GraphiteAnodeDischargeDQDV.curve() 반환값의 byte-match 보장

단계:
1. [빌드 전] 기존 v1.0.10 코드에서 대표 조건 curve() 실행 → 기준 배열 npz 저장
   - 조건: T=298.15K, c_rate=0.1, direction=discharge/charge
   - 저장: Claude/results/process/V1010_P4_graphite_regression_ref.npz

2. [코드 확장 후] 동일 조건 재실행 → 기준 배열과 비교
   - 허용 오차: atol=0, rtol=0 (완전 bit-identical)
   - 실패 시: 즉시 STOP, 흑연 경로 수정 없음 원칙 위반 보고

3. 회귀 자동화: __main__ self-test에 포함 (L567+ 블록)
```

---

## D4. Serena 통합 레시피

### D4.1 심볼-by-심볼 추가 순서

Serena `insert_after_symbol` 기준 추가 순서 (master가 실행):

| 순서 | 작업 | Serena 동작 | 앵커 심볼 | 비고 |
|------|------|-------------|-----------|------|
| 1 | `e_V` 상수 추가 | `insert_after_symbol` | `kB` (L65) | `e_V = 1.602176634e-19` [J/eV] |
| 2 | `func_dSe_elec` 추가 | `insert_after_symbol` | `func_dH_a_eff` (L155) | 전자 엔트로피 모듈 함수 |
| 3 | `func_dUdT_rev` 추가 | `insert_after_symbol` | `func_dSe_elec` | 가역열 온도 계수 함수 |
| 4 | `func_qrev` 추가 | `insert_after_symbol` | `func_dUdT_rev` | 가역열 출력 함수 |
| 5 | `LCO_STAGING_LIT` 추가 | `insert_after_symbol` | `GRAPHITE_STAGING_LIT` (L531) | 파라미터 dict |
| 6 | self-test 회귀 블록 확장 | `insert_after_symbol` | `__main__` 마지막 assert | 기준값 저장 + 비교 |

**`replace_symbol_body` 최소화 원칙**:
- **수정 필요한 심볼**: 없음 (흑연 경로 무수정)
- 유일 예외: `dqdv` 메서드 내 전자 엔트로피 플래그 분기 추가 — **이것이 유일한 기존 심볼 수정**
  - 수정 범위: `dqdv` 내부에서 전이별로 `dS_rxn` 값을 참조할 때, `elec_entropy=True` 전이에 대해 `func_dSe_elec(xi_eq_j, T, ...)` 결과를 더하는 1-2줄 추가
  - 추가 후 흑연 전이 dict에 `elec_entropy` 키 부재 → `False` → 기존 경로 완전 유지
  - **사용자 코드 소유권 보존**: 식별자 `dS_rxn`, `xi_eq`, `T`, `I_abs` 등 원본 이름 완전 보존

**사용자 코드 소유권 보존** (feedback_code_ownership_scope):
- `GraphiteAnodeDischargeDQDV` 클래스명 변경 X
- `func_ksi_eq`, `func_U_j`, `func_w`, `_causal_lowpass` 등 모든 기존 심볼명 변경 X
- 정수/문자열 코드: `GRAPHITE_STAGING_LIT` 키 이름 변경 X
- `dqdv` 메서드 시그니처 변경 X

---

### D4.2 MCP 오버헤드 절감 지침

- **Serena 사용 대상**: 심볼 추가/삽입(insert_after_symbol) 6건 — 다파일 아니고 단일 703줄 파일이나, 삽입 위치 정밀도가 중요해 Serena 활용 타당
- **Serena 미사용**: 상수 값 조회, dict 키 확인, 단순 grep — Read/Grep 직접 사용
- `replace_symbol_body` 사용은 `dqdv` 메서드 1건으로 최소화 (정당화: 전자 엔트로피 분기가 dqdv 내부 전이 루프와 불가분)

---

## D5. 그래프 검증 계획

### D5.1 흑연 + LCO dQ/dV 곡선 형태 확인

**흑연 dQ/dV** (회귀 확인):
- T=298.15K, c_rate=0.1, direction=discharge
- 기대: 4개 봉우리 (~0.085, 0.120, 0.140, 0.210 V vs Li/Li⁺)
- 비교: 코드 확장 전후 완전 일치 (byte-match)

**LCO dQ/dV** (신규 검증):
- T=298.15K, c_rate=0.1, direction=discharge
- `LCO_STAGING_LIT` 3 전이 → 봉우리 위치 기대:
  - T1 ~3.90 V (MIT, 온도 의존 T² 이동 존재)
  - T2 ~4.05 V (order-disorder a)
  - T3 ~4.17-4.20 V (order-disorder b)
- 면적 합 = ΣQ_j = 1.00 (Q_cell 기준) 확인
- `_causal_lowpass` DC=1 → 각 봉우리 넓이 = Q_j (자동)

**MIT T² 온도 이동 확인** (Ch1 eq:U1T2):
- T1 봉우리 위치를 T=268.15K, 298.15K, 328.15K에서 비교
- 기대: T1만 비선형 (T²) 이동, T2·T3는 선형 이동 또는 소폭 이동
- 흑연 봉우리: 선형 ΔS_rxn 온도 이동만 (T² 항 없음)

**전자 엔트로피 게이트 확인**:
- T1 전이에서 `func_dSe_elec` 반환값 플롯 vs 조성 x
- 기대: x ≈ 0.85 (x_MIT) 근방에서 음의 피크, 피크 반폭 ≈ 0.05 (dx_MIT)
- ΔS_e^mol의 최대 크기 추정: Ch1 eq:dSegate → `(π²/3)·R·kB·T·(13/e_V)/0.05·0.25`
  - = `(3.29)·(8.314)·(1.381e-23)·298·(13/1.602e-19)/0.05·0.25`
  - ≈ `3.29 × 8.314 × 1.381e-23 × 298 × 81.15e18 × 5` ≈ 검산 필요 (master 수치 확인)

### D5.2 가역열 q_rev 곡선 형태 확인

**흑연 q_rev 곡선** (T=298.15K, I=0.1):
- Ch2 L660-665: 저-x에서 ΔS > 0 → 방전 시 흡열 (q_rev < 0)
- 고-x (stage 2→1, x≈0.5)에서 ΔS < 0 → 방전 시 발열 (q_rev > 0)
- 기대 부호 반전: x ≈ 0.2 SOC 근방 (Ch2 L313-318, Allart 2018)

**완전식 vs 단순식 비교** (Ch2 파생 A 수치 검증):
- 단순식 (중심값만): 최대 0.18 mV/K 체계적 오차 (Ch2 L489-490)
- 완전식 (config 포함): 유한차분과 부동소수점 정밀도 일치
- 검증: 동일 조건 유한차분 `ΔU_oc/ΔT` (T1=292.15K, T2=298.15K)와 `func_dUdT_rev` 비교

---

## 5줄 요약

1. **채택 구조**: 기존 `GraphiteAnodeDischargeDQDV` 단일 클래스 유지; `LCO_STAGING_LIT` dict (3 전이, 신규 키 `elec_entropy`/`g_max_eV`/`x_MIT`/`dx_MIT`) + `func_dSe_elec`·`func_dUdT_rev`·`func_qrev` 신규 함수 추가; `dqdv` 내부 1행 플래그 분기 추가가 유일한 기존 코드 수정.
2. **핵심 시그니처**: `func_dSe_elec(xi_eq, T, g_max_eV, x_MIT, dx_MIT) → float`; `func_dUdT_rev(xi_eq_arr, dS_rxn_arr, Q_arr, w_arr) → float`; `func_qrev(I, T, dUdT) → float`; 기존 `curve`·`dqdv` 시그니처 무수정.
3. **회귀 가드**: `GraphiteAnodeDischargeDQDV.curve()` byte-match 회귀 하네스 (npz 기준값 vs 확장 후); `elec_entropy` 키 부재 시 `False` 기본값으로 흑연 경로 완전 무수정; `_causal_lowpass` DC=1 자동 보존.
4. **이중계산 처리**: `dS_rxn` 슬롯 = 중심 표준값 `ΔS⁰_j` (config=0 지점); config 항 `(R/F)·ln[ξ/(1-ξ)]`는 `func_dUdT_rev` 내부에서만 추가; 전자 엔트로피 `ΔS_e^mol`은 T1 전이 dict의 `elec_entropy=True` 시에만 `dqdv` 루프에서 호출 — 세 항 각 1회만 계상.
5. **리스크**: ① `g_max_eV` → J 단위 변환 `÷e_V` (곱으면 4×10³⁷배 오차); ② `func_dUdT_rev` 내 `ln(ξ/(1-ξ))` 양 끝 발산 → `clip(1e-10, 1-1e-10)` 필수; ③ T2/T3·T1 `dS_rxn` 초기값이 tier B — round-trip 실측 피팅 전까지 신뢰값 아님; ④ `func_U_j` 수정 없이 `dS_rxn`에 `dSe` 더할 경우 T² 이동이 자동 누적되나, `dSe`가 T 의존이라 `func_U_j` 호출 시 T 인자가 1회만 들어가는지 확인 필요.

---

*정독 완료 후 설계 제안만 기술 — `.py`·문건 수정 없음.*
