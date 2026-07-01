# Anode_Fit v1.0.10 P4 코드개정 9종 경쟁 설계 드래프트 C3

## 0. 입력 정독 범위와 판정 기준

- Base prompt: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p4_draft_base.txt` 1-20행 전문 확인, `__ID__=C3` 적용.
- 대상 코드: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` 1-702행 전문 확인. Base prompt의 "614줄" 및 P1의 "703줄" 표기와 현재 파일 행수(702행)가 불일치하므로, 설계 근거는 현재 파일 1-702행 기준으로 둔다.
- P1 앵커: `Claude/results/process/V1010_P1_code-audit_RESULT.md` 1-445행 전문 확인. 흑연 전용성, 면적보존 DC gain=1, `func_U_j_hys` 死코드 보존, `w` 폴백 inert, 피팅 파라미터 인벤토리, self-test 면적 assert 부재를 설계 제약으로 채택.
- Ch1: `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` 1-1932행 전문 확인. LCO 절, 직접 전자엔트로피 `eq:Sedirect`, MSMR 동형 `eq:msmr`, LCO 분해 `eq:lco-decomp`, 코드 예고 `sec:lco-code`를 근거로 사용.
- Ch2: `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` 1-750행 전문 확인. 가역 발열 `eq:qrev`, 이중계산 금지, 겹침 가중 완전식, 히스 평균, 비가역 분리, 하프셀 범위 경고를 근거로 사용.

본 문서는 설계 제안만 작성한다. `.py`, 기존 문건, 기존 코드 수정은 하지 않는다.

## 1. LCO 양극 dQ/dV 설계

### 1.1 채택 구조: 신규 클래스 `LCOCathodeDQDV`

채택: **신규 클래스 `LCOCathodeDQDV` + append-only helper**.

일반화 base class는 이번 P4 실편입 청사진으로 부적합하다. 기존 `GraphiteAnodeDischargeDQDV`는 P1에서 24심볼, 12식, `curve()==dqdv` 경로, DC gain=1 면적보존이 이미 고정된 흑연 전용 forward 모델이다. base class로 재편하면 기존 생성자, `dqdv`, `curve`, `_direction_to_sigma`, `__main__` self-test의 호출 경로를 건드릴 가능성이 생겨 "흑연 회귀 0-diff" 요구와 충돌한다. 반대로 신규 LCO 클래스는 기존 순수 함수(`func_w`, `func_U_j`, `func_ksi_eq`, `_causal_lowpass`, `func_dU_hys`, `func_U_branch`, `func_dH_a_eff`, `func_chi_d`)만 재사용하고, Graphite 클래스 본문을 무변경으로 둔다.

설계 원칙은 "같은 물리 골격, 다른 전극 파라미터, 전자 엔트로피 plug-in"이다. Ch1의 `sec:lco-code`는 MSMR 식과 Ch1 transition-logistic 식이 동형이며 구조 변경 0으로 LCO에 적용된다고 적는다. 따라서 코드 구조는 신규 클래스로 분리하되 수식은 흑연의 N0-N9 spine을 그대로 따른다.

### 1.2 MSMR 동형 매핑표

| Ch1/MSMR 물리량 | 기존 코드/흑연 심볼 | LCO 코드 제안 심볼 | 근거/주의 |
|---|---|---|---|
| 전이 용량 가중 `X_j` | `Q` / `Q_j` | `Q` / `Q_j` | MSMR `X_j <-> Q_j`, peak 면적 보존. |
| 중심 전위 `U_j^0` | `U`, `dH_rxn`, `dS_rxn`, `func_U_j` | `U`, `dH_rxn`, `dS_rxn`, optional `entropy_model` | LCO 중심은 3.90/4.05/4.17 V 영역. |
| 폭 `omega_j` | `n`, `w`, `func_w`, `_width` | `n`, `w`, `_width` | 두-상 LCO 폭은 평형 예측이 아니라 현상학적 피팅 폭. |
| MSMR 부호 `f` | `sigma_d`가 logistic exponent에 관여 | `f = -sigma_d`를 명시 보존 | Ch1 `eq:msmr`: `f <-> -sigma_d`. |
| D1 `theta` | `xi_eq` | `xi_eq` 또는 `theta=1-xi_eq` facade | LCO T1 전자항은 조성 `x`와 `xi` 매핑 필요. |
| 분극 | `V_n=V_app-sigma_d|I|Rn` | 동일 | LCO 하프셀에서도 단전극 vs Li 기준. |
| 히스 분기 | `U_j^d=U_j+1/2 sigma_d h_eta gamma DeltaU_hys` | 동일 함수 재사용 | MIT/order-disorder 2상역도 정규용액 틀 적용. |
| 꼬리 | `L_q`, `L_V`, `_causal_lowpass`, charge reversal | 동일 구조 | 방향별 인과성은 유지하되 LCO path sign 문서화. |

LCO 부호 규약은 문서에 명시해야 한다. 방전(`sigma_d=+1`)은 LCO 기준 리튬화이며 전위가 내려가고, 충전(`sigma_d=-1`)은 탈리튬화이며 전위가 올라간다. LCO 전이표는 충전/탈리튬화 진행을 전위 오름차순으로 둔다. 따라서 클래스 내부에는 `sigma_d`(실험 경로: 방전 +1, 충전 -1)와 `f_msmr=-sigma_d`(MSMR exponent 부호)를 분리한 지역 변수를 둔다. 이 분리를 하지 않으면 LCO에서 "방전=리튬화"와 MSMR 전이 진행 방향이 섞인다.

### 1.3 신규 상수와 전이 dict

신규 상수 후보:

- `eV_J = 1.602176634e-19`
- `LCO_MSMR_LIT`: LCO 하프셀 3전이 초기값. T1 MIT `~3.90 V`, T2 order-disorder `~4.05 V`, T3 order-disorder `~4.17-4.20 V`. T4 `~4.55 V`는 고전압 옵션이며 기본 off.

`LCO_MSMR_LIT` dict 키는 기존 흑연 dict 키와 최대한 맞춘다.

```python
{
    "label": "T1_MIT",
    "U": 3.90,
    "Q": ...,
    "n": 1.0,
    "Omega": ...,
    "gamma": ...,
    "dH_a": ...,
    "dS_a": 0.0,
    "dVdq_qa": ...,
    "dS0_mol": ...,
    "entropy_model": "lco_mit_electronic",
    "x_min": 0.75,
    "x_max": 0.94,
    "x_mit": 0.85,
    "dx_mit": 0.05,
    "g_ef_max_eV": 13.0,
}
```

`dS0_mol`은 봉우리 중심 표준값이다. Ch2 파생 B에 따라 중심에서 config 항은 0이며, 봉우리 내부 `R ln[xi/(1-xi)]`를 `dS0_mol`에 다시 더하면 이중계산이다. T2/T3의 Motohashi config 값도 중심 표준값으로만 읽고, 내부 config 분포항은 별도 조립 함수가 한 번만 추가한다.

### 1.4 핵심 함수 시그니처

```python
def lco_mit_g_ef_gate(x_li, g_ef_max_eV=13.0, x_mit=0.85, dx_mit=0.05):
    """Return g(E_F,x) [states/eV/atom] for LCO MIT logistic gate."""

def lco_mit_dS_e_mol(x_li, T, g_ef_max_eV=13.0, x_mit=0.85, dx_mit=0.05):
    """Return electronic entropy contribution [J/mol/K], insertion 기준 negative."""

def assemble_deltaS_mol(xi, T, tr, include_config=True, include_electronic=True):
    """Return Delta S(x,T) [J/mol/K] = center standard + config distribution + optional electronic residual."""
```

`LCOCathodeDQDV`는 최소한 다음 public API를 갖는다.

```python
class LCOCathodeDQDV:
    def __init__(self, transitions=LCO_MSMR_LIT, x=0.5, Rn=0.0, Cbg=0.0,
                 chi=None, chi_split=func_chi_d, use_dH_eff=True,
                 z_cut=4.357, A_cap_RT=4.0, grid_pad_lo=0.15,
                 grid_pad_hi=0.15, n_work_min=2048,
                 min_lag_grid_steps=2.0, v_span_floor=1e-6):
        ...

    def dqdv(self, V_app, T, I_abs, Q_cell, direction="discharge"):
        ...

    def curve(self, V_app, direction="discharge", c_rate=0.0,
              Q_cell=1.0, T=298.15, I_abs=None):
        ...

    def reversible_heat(self, V_app, T, I_abs, Q_cell,
                        direction="discharge", include_config=True,
                        include_electronic=True, include_irreversible=False):
        ...
```

`curve()`는 Graphite와 같은 facade 명칭을 쓰되, 구현은 LCO 클래스 내부에 새로 둔다. Graphite의 `curve()`는 호출하지 않는다.

## 2. 가역 발열 `q_rev` 설계

### 2.1 채택 식과 부호

Ch2 `eq:qrev` 기준:

```text
q_rev = -I*T*(partial U_oc / partial T) = -(I*T/F)*DeltaS(x)
```

여기서 `I`는 signed current로 정의한다. 방전은 `I_signed=+I_abs`, 충전은 `I_signed=-I_abs`. 기존 `dqdv()`는 `I_abs`와 방향을 분리하므로, 발열 함수도 외부 API는 `I_abs, direction`을 받고 내부에서 signed current를 만든다. `T`는 한 번만 곱한다. `DeltaS_e`가 이미 `propto T`인 항이라고 해서 `q_rev`에서 `T`를 추가로 누락하거나 두 번 적분하지 않는다. 최종 곱은 항상 `-(I_signed*T/F)*DeltaS_total_mol`.

### 2.2 `DeltaS(x,T)` 조립

권장 조립:

```text
DeltaS_total_j(x,T)
= dS0_mol_j
  + R*ln[xi_j/(1-xi_j)]          # include_config=True일 때만
  + dS_e_mol_j(x,T)              # LCO T1 MIT에서만, include_electronic=True
  + dS_vib_residual_j(x,T)       # 기본 0, 후속 확장 슬롯
```

중요: `dS0_mol_j`는 봉우리 중심 표준값이다. Ch2 293-309행의 이중계산 금지에 따라 `dS0_mol_j`에 config 중심값을 넣고, 내부 분포항 `R ln[xi/(1-xi)]`는 별도로 한 번만 더한다. 중심 `xi=1/2`에서 `ln 1=0`이므로 두 정의가 충돌하지 않는다.

전자항은 Ch1 `eq:dSemolar`, `eq:gunit`, `eq:dSegate`를 따른다.

```text
g_J(E_F,x) = g_eV(E_F,x) / eV_J
dS_e_mol(x,T) = (pi^2/3) * R * kB * T * d[g_J(E_F,x)]/dx
```

MIT logistic gate를 쓰면 삽입 기준 `dS_e_mol < 0`이다. `eV_J`는 곱하는 것이 아니라 나눈다. 이 단위 변환을 틀리면 Ch1이 경고한 대로 전자항 크기가 터진다.

### 2.3 이중계산 직교 처리

코드 레벨에서 `DeltaS`를 세 슬롯으로 분리한다.

- `dS0_mol`: 중심 표준값. config=0 at `xi=1/2`. vib/electronic 중심 기여를 넣을 수 있으나, 그 경우 residual electronic은 중심값을 뺀 형태로만 더한다.
- `config_distribution`: `R*logit(xi)` 단 하나. clipping은 수치 overflow 방지용으로만 쓰고 물리값을 임의 flatten하지 않는다.
- `electronic_residual`: T1 MIT gate. 기본 설계는 `dS0_mol`에 T1 electronic 중심을 넣지 않고 full gate를 이 슬롯에 둔다. 만약 fitting recipe가 `dS0_mol`에 electronic 중심까지 흡수하도록 선택하면, 구현은 `dS_e_mol(x,T) - dS_e_mol(x_center,T)`를 더해야 한다.

이 분리는 Ch1 `lco-decomp`의 "config와 electronic은 서로 다른 자유도라 가산 가능"과 Ch2의 "config를 중심값에 또 더하면 이중계산"을 동시에 만족한다. 직교성은 더해도 되는 근거이고, 무이중계산은 슬롯 분리가 보장한다.

### 2.4 비가역 3분해 옵션

`include_irreversible=False`를 기본으로 둔다. 켜면 반환 객체에 다음 component만 별도 산출한다.

```text
q_irr_ohmic = I_abs^2 * Rn
q_irr_ct    = I_signed * eta_ct
q_irr_diff  = I_signed * eta_diff
```

P4 1차 편입에서는 `eta_ct`, `eta_diff`를 실제 새 물리로 계산하지 않는다. 기존 Ch1 꼬리/분극이 비가역 소산의 원천임은 문서상 근거가 있으나, 코드에 charge-transfer overpotential과 diffusion overpotential을 분해하는 독립 상태변수가 없다. 따라서 옵션 설계는 "반환 슬롯과 future hook"까지만 두고, 기본 `q_rev`와 섞지 않는다. 히스 gap은 Ch2 파생 D에 따라 비가역열이며 `q_rev`에 포함하지 않는다.

반환 형식:

```python
{
    "q_rev": q_rev,
    "dU_dT": dU_dT,
    "DeltaS_mol": DeltaS_mol,
    "components": {
        "center": ...,
        "config": ...,
        "electronic": ...,
        "vib_residual": ...,
        "irreversible": None or {...},
    },
}
```

주의: Ch2 범위는 코인 하프셀 단독이다. 전셀 합성 `dU_cell/dT = dU_cat/dT - dU_an/dT`는 이번 P4 코드에 넣지 않는다. 필요하면 후속 `FullCellThermalDQDV`에서 별도 설계한다.

## 3. 흑연 회귀 0-diff 가드

### 3.1 무섭동 구조

Graphite 경로는 다음 심볼을 전부 무변경으로 둔다.

- 모듈 함수: `func_w`, `func_U_j`, `func_U_j_hys`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass`, `func_dU_hys`, `func_U_branch`, `func_dH_a_eff`, `func_chi_d`, `_finite*`
- 클래스: `GraphiteAnodeDischargeDQDV` 전체
- 데이터: `GRAPHITE_STAGING_LIT`
- self-test `if __name__ == "__main__":` 본문

신규 LCO와 q_rev는 기존 Graphite 클래스의 상속 부모를 바꾸지 않고, Graphite 클래스에 flag를 추가하지 않고, Graphite `curve()`에 electrode 분기를 넣지 않는다. 상속이나 flag는 코드량이 줄어 보이지만 기존 경로의 dispatch와 default 값을 흔드는 순간 0-diff를 보장하기 어렵다.

### 3.2 회귀 하네스

회귀 하네스는 편입 전후 같은 Python/NumPy 환경에서 다음을 비교한다.

1. 같은 입력으로 `GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True).curve(...)` 산출.
2. `direction=("discharge","charge")`, `c_rate=(0.0,0.02,0.2,1.0)`, `T=(258.15,298.15,318.15)`, scalar T와 `T(V)` 배열 모두 포함.
3. `np.array_equal(y_before, y_after)` 및 `y_before.tobytes()==y_after.tobytes()` 확인.
4. `equilibrium()`도 별도 비교한다. q_rev/LCO 추가가 전역 상수나 helper를 바꾸지 않았다는 증거다.
5. 면적보존 DC=1: 평형 peak `trapz(Q*xi*(1-xi)/w,V)`가 전이별 `Q_j`와 일치하는지 assert를 추가 테스트로 둔다. P1에서 self-test 본문에는 면적 assert가 없다고 판정했으므로, 이 회귀는 별도 harness 파일/CI에서 수행하고 Graphite 본문은 수정하지 않는다.

P1의 `func_U_j_hys` 死코드 판정은 그대로 따른다. 삭제하지 않고, LCO도 이 함수를 호출하지 않는다. 분기 중심은 기존 활성 helper `func_U_branch` 또는 LCO 내부 동형 helper만 사용한다.

## 4. Serena 편입 레시피

### 4.1 신규 추가 심볼

권장 insert 순서:

1. `insert_after_symbol("GRAPHITE_STAGING_LIT")`
   - `eV_J`
   - `LCO_MSMR_LIT`
   - `lco_mit_g_ef_gate`
   - `lco_mit_dS_e_mol`
   - `assemble_deltaS_mol`
   - `LCOCathodeDQDV`

`GRAPHITE_STAGING_LIT` 뒤, `__main__` self-test 앞에 넣으면 import 시 심볼이 정상 공개되고, Graphite 클래스 본문은 변경하지 않는다. 기존 `__main__` self-test가 실행될 때 LCO class 정의가 먼저 끝난다는 장점도 있다.

2. 새 self-test가 필요하면 기존 `__main__`에 섞지 말고 `def _selftest_lco_smoke():`를 신규 심볼로 추가한다. 실행 여부는 master가 별도 결정한다. 기존 `__main__` 본문을 건드리면 0-diff 판단이 어려워진다.

### 4.2 replace_symbol_body 필요 여부

필수 `replace_symbol_body`: **없음**.

기존 함수 재사용만으로 LCO dQ/dV의 MSMR 동형, q_rev 조립, 회귀 harness 설계가 가능하다. 기존 함수 본문 교체가 필요한 듯 보이는 경우는 대부분 일반화 base class 욕심에서 온다. 이번 범위에서는 모두 append-only로 처리한다.

예외 후보:

- `__all__`가 향후 추가된다면 신규 심볼 export 반영이 필요할 수 있다. 현재 대상 코드에는 `__all__`이 없다.
- 문서용 docstring 정정(`z_cut` docstring 부정확)은 P1의 P4 후보이나, 이번 설계의 핵심 요구가 LCO+발열+흑연 0-diff이므로 실편입 시에도 별도 topic으로 분리하는 편이 안전하다.

### 4.3 코드 소유권/식별자 보존

기존 식별자, 대소문자, 문자열 direction alias, 정수 부호 `+1/-1`, `GRAPHITE_STAGING_LIT` dict key는 바꾸지 않는다. LCO 신규 key도 기존 key와 충돌하지 않게 추가한다. `Q`, `U`, `n`, `w`, `Omega`, `gamma`, `dH_a`, `dS_a`, `dVdq_qa`, `L_V`는 같은 의미로 유지한다. 전자항 관련 key만 신규 namespace를 붙인다(`x_mit`, `dx_mit`, `g_ef_max_eV`, `entropy_model`).

## 5. 그래프 검증 계획

### 5.1 흑연 dQ/dV

- 기존 `GRAPHITE_STAGING_LIT`로 `V=linspace(0.03,0.34,1000)` 산출.
- 방전/충전, 0.02C/0.2C/1.0C, 258/298/318 K 비교.
- 기대: 기존 peak 위치와 `curve()==dqdv` byte 일치, 히스 `gamma>0` 별도 demo에서 dis-chg split 유지, 면적 `sum Q` 보존.

### 5.2 LCO dQ/dV

- `V=linspace(3.75,4.25,1200)` 기본. 옵션 T4를 켤 때만 4.6 V까지 확장.
- 기대 peak: T1 MIT `~3.90 V`, T2 `~4.05 V`, T3 `~4.17-4.20 V`.
- `direction="charge"`에서는 탈리튬화 진행의 전위 오름차순 peak를 확인하고, `direction="discharge"`에서는 path sign과 memory reversal이 반대 방향 꼬리를 내는지 본다.
- `Q_j` 면적 보존: 배경 차감 후 각 전이 peak 적분이 dict `Q`와 일치해야 한다.
- MIT electronic gate on/off 비교: 단일 298 K dQ/dV에서는 중심 calibration 때문에 큰 shape 차이가 없어야 하며, 다온도에서는 T1의 `dU/dT` 이동률이 `T` 선형 성분을 보여야 한다.

### 5.3 가역 발열 곡선

- 흑연: `DeltaS_total = dS0 + R logit(xi)`로 `q_rev` 산출. 기대: `DeltaS>0` 영역에서 방전 `q_rev<0`(흡열), `DeltaS<0` 영역에서 방전 `q_rev>0`(발열).
- LCO: T1 MIT gate를 켜고 끈 곡선을 비교한다. 기대: T1 조성 구간에서 전자항이 국소 음의 `DeltaS_e` 골을 만들고, 방전 q_rev 부호는 `-(I*T/F)*DeltaS`에 따라 결정된다.
- 하프셀 경고: 그래프 제목/축 라벨에는 "half-cell vs Li"를 명시한다. 전셀 발열처럼 보이는 합성 그래프는 이번 P4 검증에서 만들지 않는다.

## 6. 리스크와 보류

- LCO 전자항은 `x` 함수이고 dQ/dV 코어는 `V` 격자 함수다. Ch1 1724-1729행의 예고대로 T1 `xi_eq(V)`를 통해 `x <-> xi`를 매핑해야 한다. 이 매핑이 가장 큰 구현 리스크다. 첫 편입은 one-pass mapping으로 두고, 필요할 때 fixed-point 반복을 추가한다.
- `dS_e_mol(x,T)`가 `propto T`라 `U(T)` 이동은 `T^2` 항을 가진다. 기존 `func_U_j`는 선형 `(-dH+T*dS)/F`만 지원한다. LCO 클래스는 기존 `func_U_j`를 그대로 두고, LCO 내부 `center_potential()`에서 기준온도 `T_ref`와 전자항 적분을 별도 처리해야 한다.
- `q_rev`의 완전식은 하프셀 OCV의 `x` 좌표가 필요하다. 현재 dQ/dV code path는 forward curve generator이지 `U_oc(x)` solver가 아니다. 전압 격자 위 근사 q_rev는 가능하지만, Ch2 668-684행의 엄밀한 SOC 완전식은 전하보존 음함수 solver가 필요하다. P4 1차 구현은 voltage-grid diagnostic과 SOC solver를 분리하는 편이 안전하다.
- 비가역 3분해는 반환 슬롯만 두고 기본 off로 유지한다. 실제 `eta_ct`, `eta_diff` 식별은 현재 코드 상태변수만으로는 근거 부족이다.

## 7. C3 결론

`LCOCathodeDQDV` 신규 클래스 append-only가 최선이다. LCO dQ/dV는 MSMR 동형으로 기존 logistic/꼬리/히스 spine을 재사용하고, T1 MIT 전자 엔트로피만 `DeltaS` 조립 함수로 plug-in한다. q_rev는 `q_rev=-(I*T/F)*DeltaS(x)`를 단일 출구로 두며, config 분포항과 중심 표준값을 분리해 이중계산을 차단한다. Graphite 경로는 상속/flag/base 일반화 없이 무변경으로 두고, `curve()` 출력 byte 일치와 면적보존 DC=1을 별도 회귀 harness로 잠근다.
