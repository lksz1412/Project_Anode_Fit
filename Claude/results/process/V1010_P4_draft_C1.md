# Anode_Fit v1.0.10 P4 코드개정 9종 설계 드래프트 C1

> 범위: 설계 제안만. `.py`/문건/코드 수정 없음.  
> 원천 직접 확인: base prompt 1-20행, `Anode_Fit_v1.0.10.py` 현재 1-702행, `V1010_P1_code-audit_RESULT.md` 현재 1-445행, `graphite_ica_ch1_v1.0.10.tex` 현재 1-1932행, `graphite_ica_ch2_v1.0.10.tex` 현재 1-750행.  
> 주의: base prompt의 코드 614줄, Ch1 1816줄 표기는 현재 파일과 다르다. 본 드래프트는 실제 읽은 현재 파일 행 번호를 근거로 한다.

## 0. 채택 구조 요약

채택안은 **기존 `GraphiteAnodeDischargeDQDV` 무변경 + 신규 `LCOCathodeDQDV` 추가 + 가역 발열 순수 함수 추가**다. 일반화 base class 리팩터링은 선택하지 않는다. 이유는 P1 audit가 흑연 경로의 물리식 12개, 24심볼 coverage, 면적보존 DC gain=1을 이미 ground truth로 확정했고, 기존 클래스의 `dqdv()` 내부 흐름은 hook 없이 직접 계산하므로 base 일반화가 `replace_symbol_body`를 요구하기 때문이다(`V1010_P1_code-audit_RESULT.md` 25-42, 48-58행; 코드 370-480행). P4의 최우선 조건인 **흑연 회귀 0-diff**에는 신규 클래스 병렬 추가가 가장 안전하다.

핵심 아이디어는 Ch1의 “같은 코드가 LCO를 그린다” 결론을 코드 구조로 옮기는 것이다. Ch1은 LCO 확장이 `GRAPHITE_STAGING_LIT -> LCO_STAGING_LIT` 파라미터 교체와 T1 전자 엔트로피 plug-in 두 가지라고 못박는다(Ch1 1735-1760행). MSMR 식은 Ch1 transition-logistic과 동형이며, 매핑은 `X_j <-> Q_j`, `U_j^0 <-> U_j^d`, `omega_j <-> w_j`, `f <-> -sigma_d`다(Ch1 1736-1747행).

## 1. LCO 양극 dQ/dV 설계

### 1.1 신규 클래스 vs 일반화 base

**선택: 신규 클래스 `LCOCathodeDQDV`.**

근거:

| 후보 | 장점 | 결함 | 판정 |
|---|---|---|---|
| `ElectrodeDQDVBase` 일반화 | 중복 감소, 장기 구조 깔끔함 | 기존 `GraphiteAnodeDischargeDQDV.dqdv()` 본문을 쪼개야 하므로 흑연 byte 회귀 위험. 현재 코드에는 중심/폭/꼬리 hook이 없다(코드 431-477행). | P4 실편입 1차안으로 부적합 |
| `GraphiteAnodeDischargeDQDV` 상속 | 표면상 코드 적음 | 전자 엔트로피를 중심 계산에 넣으려면 부모 `dqdv()`가 내부에서 `func_U_j()`를 직접 호출하므로 override 지점이 없다(코드 433-455행). 결국 부모 본문 수정 필요. | 부적합 |
| **신규 `LCOCathodeDQDV` 병렬 클래스** | 기존 흑연 class와 data를 그대로 둠. Ch1의 “파라미터 교체 + 전자항 plug-in”을 별도 경로로 구현 가능. | 일부 loop 중복 발생 | **채택** |

### 1.2 MSMR 동형 매핑표

| Ch1/MSMR 심볼 | 기존 코드 심볼 | LCO 설계 심볼 | 근거 |
|---|---|---|---|
| `X_j` | `tr['Q']` | `tr['Q']` 또는 `tr['X']` alias 금지, `Q` 유지 | Ch1 1739-1744행. 기존 합산도 `tr['Q']` 사용(코드 366, 477행). |
| `U_j^0` | `tr['U']` 또는 `func_U_j(T,dH_rxn,dS_rxn)` | `U_j^cat(T,x)` | Ch1 465-483행, 1750-1758행. |
| `omega_j` | `w_j = n_j RT/F` | 동일 `n`/`w` 규약 | 코드 272-284행; Ch1 711-721행. |
| `f` | `-sigma_d` 대응 | 내부 logistic 부호는 `sigma_d` 유지, MSMR 문헌 매핑만 `f=-sigma_d`로 기록 | Ch1 1742-1747행. |
| `x_j` | `xi_eq` 계열 | `xi_eq` 유지 | Ch1 770-780행. |
| LCO electronic | 없음 | T1 전이에서 `deltaS_e_mol(x,T)` 추가 | Ch1 927-1160행, 1685-1722행. |

### 1.3 양극 부호와 진행률 규약

코드의 `sigma_d` 의미는 유지한다. 단, LCO에서 방전(`sigma_d=+1`)은 **리튬화**, 충전(`sigma_d=-1`)은 **탈리튬화**다. Ch1은 LCO 하프셀에서 방전이 Li가 LCO로 들어와 `x` 증가, 전위 하강이고 충전이 `x` 감소, 전위 상승이라고 명시한다(Ch1 303-309행). 따라서 LCO 클래스 docstring에는 다음을 고정한다.

- `direction="discharge"`: LCO lithiation, `x` 증가.
- `direction="charge"`: LCO delithiation, `x` 감소.
- 내부 logistic 부호는 기존 `func_ksi_eq(T,V,center,n,sigma_d)` 규약을 그대로 쓴다. 기존 코드의 부호 사슬은 분극, 분기중심, `chi_d`, 격자 역전에 전파된다(코드 388-408, 447-475행; P1 audit 349행).

### 1.4 필요 상수와 전이 초기값

신규 상수는 기존 `GRAPHITE_STAGING_LIT`를 건드리지 않고 뒤에 추가한다.

```python
EV_J = 1.602176634e-19

LCO_MSMR_LIT = [
    {
        "label": "T1_MIT",
        "U": 3.90,
        "Q": ...,
        "n": 1.0,
        "Omega": ...,
        "gamma": ...,
        "dH_rxn": ...,
        "dS_rxn": ...,
        "dH_a": ...,
        "dS_a": 0.0,
        "dVdq_qa": ...,
        "lco_electronic": True,
        "x_mit": 0.85,
        "dx_mit": 0.05,
        "g_ef_max_eV": 13.0,
    },
    {"label": "T2_order_disorder_a", "U": 4.05, ...},
    {"label": "T3_order_disorder_b", "U": 4.17, ...},
]
```

`Q`, `Omega`, `gamma`, `dH_rxn`, `dH_a`, `dVdq_qa`의 정밀 초기값은 현재 Ch1에서 “출발점, 피팅 override”로만 제시되어 있고 신뢰값이 아니다(Ch1 311-317행, 1750-1756행). 따라서 코드 편입 시 문헌/사용자 데이터에서 채울 미확정 파라미터는 `...`가 아니라 명시적 숫자 초기값을 master가 결정해야 한다. 본 C1은 허위 정밀값을 만들지 않는다.

### 1.5 전자 엔트로피 함수 시그니처

```python
def func_lco_g_ef_gate(x_li: ScalarOrArray,
                       g_ef_max_eV: float = 13.0,
                       x_mit: float = 0.85,
                       dx_mit: float = 0.05) -> ScalarOrArray:
    ...

def func_lco_deltaS_e_mol(x_li: ScalarOrArray,
                          T: ScalarOrArray,
                          g_ef_max_eV: float = 13.0,
                          x_mit: float = 0.85,
                          dx_mit: float = 0.05) -> ScalarOrArray:
    ...
```

식:

\[
g(E_F,x)=g_{\max}\left[1-\sigma\left(\frac{x-x_{\mathrm{MIT}}}{\Delta x_{\mathrm{MIT}}}\right)\right]
\]

\[
\Delta S_{e}^{mol}(x,T)
=-\frac{\pi^2}{3}R\left(\frac{k_B T}{e_V}\right)
\frac{g_{\max}}{\Delta x_{\mathrm{MIT}}}\sigma(1-\sigma)
\]

부호는 삽입 기준 음수다. Ch1은 `g_eV/e_V` 나눗셈 환산을 명시하고, `e_V`를 곱하면 `1/e_V^2` 배 오류가 난다고 경고한다(Ch1 1023-1034행). T1 MIT에서 `Delta S_e < 0`, 탈리튬화 방출은 절댓값 양수라는 부호 규약도 명시되어 있다(Ch1 1034-1047행, 1081-1091행).

### 1.6 `LCOCathodeDQDV` 핵심 시그니처

```python
class LCOCathodeDQDV:
    def __init__(self,
                 transitions: List[Dict[str, Any]],
                 x: float = 0.5,
                 Rn: float = 0.0,
                 Cbg: Union[float, Callable] = 0.0,
                 chi: Optional[float] = None,
                 chi_split: Callable[[float, int], float] = func_chi_d,
                 use_dH_eff: bool = True,
                 z_cut: float = 4.357,
                 A_cap_RT: float = 4.0,
                 grid_pad_lo: float = 0.15,
                 grid_pad_hi: float = 0.15,
                 n_work_min: int = 2048,
                 min_lag_grid_steps: float = 2.0,
                 v_span_floor: float = 1e-6,
                 x_li_map: Optional[Callable[[np.ndarray, Dict[str, Any]], np.ndarray]] = None):
        ...

    def dqdv(self, V_app, T, I_abs, Q_cell, s=+1):
        ...

    def curve(self, V_app, direction="discharge", c_rate=0.0,
              Q_cell=1.0, T=298.15, I_abs=None):
        ...
```

`x_li_map`은 전자항 평가용 조성 좌표를 제공한다. 기본값은 T1 전이의 `xi_eq`를 `x_start -> x_end`로 선형 매핑하는 내부 함수로 둔다. Ch1은 전자항이 조성 `x` 함수이지만 `dqdv()`는 전압 격자에서 돌기 때문에 `x <-> xi_eq(V)` 매핑이 필요하다고 예고한다(Ch1 1724-1729행).

## 2. 가역 발열 `q_rev` 설계

### 2.1 함수/메서드 시그니처

발열은 클래스에 종속시키기보다 먼저 순수 함수로 추가한다. 기존 흑연 경로와 LCO 경로가 같은 출구식을 공유할 수 있고, 기존 class 수정 없이 import 가능한 함수만 추가하면 회귀 위험이 낮다.

```python
def func_q_rev(I: ScalarOrArray,
               T: ScalarOrArray,
               deltaS_mol: ScalarOrArray) -> ScalarOrArray:
    """q_rev = -(I*T/F)*DeltaS(x), DeltaS in J/(mol K)."""
    return -(np.asarray(I) * np.asarray(T) / F) * np.asarray(deltaS_mol)
```

Ch2의 출구식은 `q_rev = -I T * partial U_oc/partial T = -(I T/F) Delta S(x)`이고, `T`는 한 번만 곱한다(Ch2 83-85행, 642-646행). 코드에서도 `T * deltaS_mol / F`만 쓰며 `deltaS_mol`이 이미 `T`를 포함한 전자항일 때 추가 `T`를 또 넣지 않는다.

### 2.2 `Delta S(x)` 조립

기본 조립식:

\[
\Delta S(x)=\Delta S^0_j + R\ln\frac{\xi_j}{1-\xi_j}+\delta S_{vib/e}(x)
\]

겹침 영역에서는 Ch2의 완전식을 쓴다.

\[
\frac{\partial U_{oc}}{\partial T}
=
\frac{\sum_j Q_j g_j(x)\left[\Delta S^0_j/F+(R/F)\ln(\xi_j/(1-\xi_j))\right]}
{\sum_j Q_j g_j(x)}, \quad
g_j=\xi_j(1-\xi_j)/w_j
\]

근거는 Ch2 668-684행이다. LCO T1에서는 `deltaS_e_mol(x,T)`를 `delta S_vib/e(x)`의 급변 항으로 추가한다. Ch2는 electronic 급변이 중심값에 흡수되지 못하는 예외라고 설명한다(Ch2 381-408행, 627-633행).

### 2.3 이중계산 직교 규칙

구현 규칙:

1. `tr['dS_rxn']` 또는 `tr['dS0_rxn']`는 **봉우리 중심 표준값**만 담는다.
2. `R ln[xi/(1-xi)]` config 분포항은 `deltaS_profile()` 함수에서 계산한다.
3. `dS_rxn`에 이미 config 항을 누적한 값을 넣는 입력 모드는 금지하거나, 명시 플래그 없이 허용하지 않는다.
4. electronic은 T1 MIT 자유도에만 더하고, config와 같은 Li 자리 배열 엔트로피로 취급하지 않는다.

근거:

- Ch2는 중심 표준값 `Delta S^0_j`와 config 분포항을 서로 다른 출처로 분리하고, config를 `Delta S^0_j`에 또 더하면 이중계산이라고 경고한다(Ch2 293-309행, 524-537행).
- Ch1은 LCO에서 config와 electronic이 근사적으로 직교 자유도이며, 직교성은 “더해도 되는가”를, 중심값/골 분리 규칙은 “과대 계상 없는가”를 보장한다고 정리한다(Ch1 1685-1722행).

### 2.4 비가역 3분해 옵션

P4 범위에서 `q_rev`는 가역열만 기본 구현한다. 다만 옵션 구조는 다음 이름으로 열어 둔다.

```python
def func_q_irr_components(I_abs, R_ohm=0.0, eta_ct=0.0, eta_diff=0.0):
    return {
        "ohmic": I_abs * I_abs * R_ohm,
        "charge_transfer": I_abs * eta_ct,
        "diffusion": I_abs * eta_diff,
    }
```

Ch2는 Bernardi 식에서 비가역항을 `I(U_oc - V)`로 분리하고, Ch1 동역학 꼬리와 분극이 entropy production을 만든다고 한다(Ch2 639-649행). base prompt는 비가역 3분해 옵션을 요구하므로 `I²R + I eta_ct + I eta_diff`를 별도 옵션으로 제안하되, 가역열 `q_rev`와 혼합하지 않는다. 히스 gap도 비가역 소산으로 분리해야 하며 가역열에 섞지 않는다(Ch2 570-593행).

## 3. 흑연 회귀 0-diff 가드

### 3.1 무섭동 구조

흑연 클래스와 상수는 그대로 둔다.

무변경 대상:

- `func_w`, `func_U_j`, `func_U_j_hys`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass` 원형 보존 구역(코드 73-128행).
- `GraphiteAnodeDischargeDQDV` 전체(코드 192-524행).
- `GRAPHITE_STAGING_LIT` 전체(코드 527-560행).
- `__main__` self-test(코드 567-702행).

추가 대상은 모두 신규 심볼이다. 신규 함수가 기존 이름과 충돌하지 않아야 하며, 기존 `curve()`나 `dqdv()` 호출 경로에서 참조되지 않아야 한다.

### 3.2 회귀 하네스

편입 직후 master가 돌릴 최소 회귀:

```python
V = np.linspace(0.03, 0.34, 1000)
before = baseline_model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15)
after = patched_model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15)
assert before.dtype == after.dtype
assert before.shape == after.shape
assert before.tobytes() == after.tobytes()
```

추가 matrix:

- `direction`: `"discharge"`, `"charge"`, `+1`, `-1`
- `I_abs`: `0.0`, `1e-6`, `0.02`, `0.2`, `1.0`
- `T`: scalar `298.15`, array `np.linspace(288.15,308.15,V.size)`
- `transitions`: `GRAPHITE_STAGING_LIT`, one-transition direct `L_V`

P1 audit는 `curve()`가 `dqdv()` 재사용이고 `curve(dis,0.2C)==dqdv(...)` self-test가 이미 존재한다고 확인한다(코드 483-508, 608-615행; P1 audit 31-36행). P4 회귀는 “근사 0”이 아니라 **byte 일치**를 gate로 둔다.

### 3.3 면적보존 DC=1 유지

면적보존은 `_causal_lowpass`의 DC gain=1과 `Q_j xi(1-xi)/w` 적분에서 온다(코드 110-128, 366, 464-477행; P1 audit 33행, 347행). 신규 LCO 클래스에서도 동일한 두 원칙을 유지한다.

- 평형 peak: `Q_j * xi_eq * (1 - xi_eq) / w`
- 꼬리 peak: `Q_j * (xi_eq - occ_lagged) / L_V`
- 새 전자 엔트로피는 `U_j(T,x)` 또는 `DeltaS(x)`에만 작용하고 `Q_j` 면적 가중을 임의 변경하지 않는다.

## 4. Serena 편입 레시피

### 4.1 신규 추가 심볼

`insert_after_symbol` 기준 제안:

| 순서 | 심볼 | Serena 작업 | 위치 |
|---|---|---|---|
| 1 | `EV_J` | `insert_after_symbol` | `h` 상수 뒤 또는 `ScalarOrArray` 뒤 |
| 2 | `func_lco_g_ef_gate` | `insert_after_symbol` | `_finite_nonneg` 뒤 |
| 3 | `func_lco_deltaS_e_mol` | `insert_after_symbol` | `func_lco_g_ef_gate` 뒤 |
| 4 | `func_q_rev` | `insert_after_symbol` | `func_lco_deltaS_e_mol` 뒤 |
| 5 | `func_q_irr_components` | `insert_after_symbol` | `func_q_rev` 뒤 |
| 6 | `LCOCathodeDQDV` | `insert_after_symbol` | `GraphiteAnodeDischargeDQDV` class 뒤, `GRAPHITE_STAGING_LIT` 앞 또는 뒤 |
| 7 | `LCO_MSMR_LIT` | `insert_after_symbol` | `GRAPHITE_STAGING_LIT` 뒤 |

`replace_symbol_body`는 원칙적으로 **0개**다. 필요한 기존 심볼 교체가 있다면 본 C1 설계에서는 근거 미발견이다. 기존 import에는 이미 `Dict, Any, List, Union, Callable, Optional, Tuple`과 `np`가 있어 신규 함수 타입에 충분하다(코드 61-70행). 신규 타입이 더 필요하지 않게 설계한다.

### 4.2 보존 규칙

- 기존 식별자 대소문자 보존: `GraphiteAnodeDischargeDQDV`, `GRAPHITE_STAGING_LIT`, `func_U_j_hys` 등 변경 금지.
- `func_U_j_hys`는 P1 판정대로 死코드이지만 보존한다(P1 audit 50, 57, 182-183, 344행).
- `w` 폴백 inert, `z_cut` docstring 부정확, 면적 self-test 부재 같은 P1 이슈는 P4 LCO/발열 편입 중 임의 정리하지 않는다(P1 audit 54-58, 337-347행).

## 5. 그래프 검증 계획

### 5.1 흑연 dQ/dV

1. 기존 `GRAPHITE_STAGING_LIT`로 `curve()` 출력 baseline과 patched 출력 byte 비교.
2. `np.trapz(y - Cbg, V)`가 기존 baseline과 동일한지 확인.
3. 방전/충전 peak 위치와 꼬리 방향이 기존 self-test와 동일한지 확인(코드 586-656행).

### 5.2 LCO dQ/dV

1. `LCO_MSMR_LIT`로 3개 양극 peak가 약 `3.90`, `4.05`, `4.17-4.20 V` 근방에 나타나는지 확인한다(Ch1 319-337, 1199-1211행).
2. T1 MIT 전자항 on/off 비교:
   - off: 기존 MSMR/logistic peak.
   - on: T1의 `U_1(T)` 이동률에 `Delta S_e ∝ T` 곡률이 반영되어야 한다(Ch1 1042-1061, 1207-1211행).
3. `direction="discharge"`와 `"charge"`에서 LCO 부호 설명과 peak 진행 방향이 맞는지 확인한다(Ch1 303-309행).

### 5.3 발열 곡선

1. `Delta S(x)>0`이면 방전 `I>0`에서 `q_rev<0` 흡열, `Delta S(x)<0`이면 `q_rev>0` 발열인지 확인한다(Ch2 656-666행).
2. `T` 배수는 한 번만 들어가는지 단위 검산한다.
3. config 이중계산 방지: `Delta S0 + R ln[xi/(1-xi)]`와 `Delta S0` 단독의 차이가 Ch2가 말한 config 항 범위와 부호를 갖는지 확인한다(Ch2 484-494, 524-537행).
4. 비가역 옵션은 `q_rev`와 별도 plot layer로 표시한다. 총열은 `q_total = q_rev + q_irr_ohmic + q_irr_ct + q_irr_diff`로만 합산한다.

## 6. 리스크와 미확정

| 항목 | 상태 | 이유 | 처리 |
|---|---|---|---|
| LCO 전이별 numeric `Q/Omega/gamma/dH_a/dVdq_qa` | 미확정 | Ch1은 초기값 철학과 전위/성격 중심을 주지만 모든 피팅 숫자를 확정하지 않는다. | master가 문헌/사용자 데이터로 초기값 확정 |
| `x_li_map` | 설계 확정, 구현 세부 미정 | Ch1이 `x <-> xi_eq(V)` 매핑 필요만 예고한다. | T1 `x_start/x_end` 선형 매핑을 기본, callable override 허용 |
| LCO electronic 크기 | 함수형 확정, 곡선은 모델 가정 | Ch1은 함수형/anchor는 tier A, MIT 연속 곡선은 모델 가정이라고 분리한다(Ch1 993-1002행). | 피팅 파라미터로 노출 |
| 전셀 발열 | 범위 밖 | Ch2 warnbox가 하프셀 단독, 전셀 합성 범위 밖을 명시한다(Ch2 102-107행). | P4에 넣지 않음 |

## 7. 5줄 요약

1. 채택 구조: `GraphiteAnodeDischargeDQDV` 무변경, 신규 `LCOCathodeDQDV`와 순수 발열 함수 병렬 추가.
2. 핵심 시그니처: `func_lco_deltaS_e_mol(x_li,T,...)`, `func_q_rev(I,T,deltaS_mol)`, `LCOCathodeDQDV.curve/dqdv(...)`.
3. 회귀 가드: 기존 흑연 `curve()` matrix 출력은 shape/dtype/`tobytes()` byte 일치로 0-diff 검증.
4. 이중계산 처리: `Delta S0`는 중심 표준값만, `R ln[xi/(1-xi)]` config 분포항과 T1 electronic MIT 항은 별도 조립.
5. 리스크: LCO 전이별 수치 초기값과 `x_li_map` 세부는 데이터/문헌 기반 master 결정 필요.
