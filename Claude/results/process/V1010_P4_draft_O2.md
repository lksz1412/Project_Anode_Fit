# V1.0.10 P4 코드개정 설계 드래프트 — **O2**

> **역할**: Anode_Fit v1.0.10 P4 코드개정(LCO 양극 + 가역 발열) 9종 경쟁 **설계 드래프트 O2**. 본 문건은 **설계 제안(청사진)** 이며 `.py`·문건·코드를 **수정하지 않는다**(단일 `.py`는 공유 가변상태 — 실편입은 master 가 Serena 로 1회). 타 드래프트·통합에 관여하지 않는 독립 작성.
> **근거 표기**: [코드 Lxxx] = `Anode_Fit_v1.0.10.py` 줄번호 / [Ch1 eq:xxx] = `graphite_ica_ch1_v1.0.10.tex` / [Ch2 eq:xxx] = `graphite_ica_ch2_v1.0.10.tex` / [P1] = `V1010_P1_code-audit_RESULT.md`. 추정은 [추정] 명시, 근거 미발견은 [근거 미발견].
> **정독 범위**: 대상 코드 703줄 전문([코드 L1-703]) · P1 result 전문 · Ch1 서론·sec:notation·sec:lco-map·sec:center·sec:lco-center·sec:hys·sec:lco-hys·sec:width·sec:lco-electronic(sec:lco-Se·sec:lco-gate)·sec:eqpeak·sec:lco-peak·sec:broadening·sec:sum·sec:lco-decomp·sec:lco-code·sec:signcheck 정독 · Ch2 서(warnbox)·ssec:elec·sec:limits·sec:revheat 정독.

---

## §0. 설계 결정 요약 (5줄 헤드라인)

| 항목 | O2 채택 | 한 줄 근거 |
|---|---|---|
| **① 확장 구조** | **합성(composition) + 서브클래스** — `_TransitionKernel` 순수함수 계층은 그대로 두고, `LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)`가 전자항 hook 하나만 override | 곡선 클래스는 MSMR 동형([Ch1 eq:msmr])으로 **구조 변경 0** → 흑연 경로 무섭동이 최우선 → 상속 + 단일 hook |
| **② q_rev** | **신규 모듈함수 `func_q_rev` + 메서드 `reversible_heat`** — `q_rev=−IT·∂U/∂T=−(IT/F)ΔS(x)`, T 한 번, ΔS(x)는 겹침가중 `∂U_oc/∂T` 조립 | [Ch2 eq:qrev]·use-this 종합식 1:1 |
| **③ 이중계산 직교** | **config 슬롯 = 중심 표준값 ΔS⁰_j 만** 넣고, 봉우리 내부 `R ln[ξ/(1−ξ)]`는 코드가 logistic 에서 **재생성**(재가산 금지) | [Ch2 eq:revheat use-this]·[Ch1 sec:lco-decomp ★이중계산 금지(B)] |
| **④ 흑연 0-diff 가드** | **기존 `dqdv`/`equilibrium`/`curve` 바디 1바이트 불변**(상속) + byte-일치 회귀 하네스(`np.array_equal`) | [P1 Confirmed Non-Changes]·[코드 L34-36 원형 보존] |
| **⑤ Serena 편입** | `insert_after_symbol` 신규 6심볼 추가 / 기존 심볼 `replace_symbol_body` **0건** | [코드 소유권·범위 보존] |

---

## §1. LCO 양극 dQ/dV 설계

### 1.1 채택 구조 — 왜 "일반화 base"가 아니라 "상속 + 단일 hook"인가

세 후보를 놓고 근거로 택한다.

| 후보 | 내용 | 판정 |
|---|---|---|
| (a) 신규 독립 클래스 `LCOCathodeDQDV(전체 재작성)` | dqdv 로직 복제 | **기각** — DRY 위반, 흑연 회귀식과 drift 필연([코드 L370-480] 복제 = 유지비 2배) |
| (b) 일반화 base `InsertionElectrodeDQDV` + 흑연/LCO 서브클래스 | 공통 base 추출, 흑연을 재배치 | **기각** — 흑연 경로가 **이동**되어 byte-일치 회귀가 깨짐(P1 "코드 불변" 위반). base 추출은 기존 심볼 body 이동을 강제 |
| **(c) 상속 + 단일 hook** ✔ | `LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)` — 흑연 클래스 무변경, **전자항 hook `_delta_S_extra(tr, T_work, xi_eq)` 한 곳만** override | **채택** — [Ch1 eq:msmr] "구조 변경 0, 바뀌는 것 단 둘(파라미터 교체 + 전자항 plug-in)" 과 1:1. 흑연 경로 무섭동(§3) |

**근거의 핵심**: [Ch1 sec:lco-code]가 "Ch1 의 곡선 클래스(`func_ksi_eq`·`func_U_j`·합산 eq:sum)는 **구조 변경 0** 으로 LCO 에 적용되며, 바뀌는 것은 단 둘 — (i) 전이 파라미터 교체 (ii) 전자 엔트로피 항 plug-in" 이라고 못박는다. MSMR 동형([Ch1 eq:msmr] $x_j=X_j/(1+\exp[f(U−U_j^0)/\omega_j])$ ↔ [Ch1 eq:xieq] $\xi_{eq,j}=1/(1+\exp[-\sigma_d(V−U_j^d)/w_j])$, 대응 $X_j\!\leftrightarrow\!Q_j$·$U_j^0\!\leftrightarrow\!U_j^d$·$\omega_j\!\leftrightarrow\!w_j$·$f\!\leftrightarrow\!-\sigma_d$)이 이 "구조 변경 0"의 이론적 보증이다.

곧 LCO 는 (i) `LCO_STAGING_LIT` 데이터셋(파라미터 교체)과 (ii) T1 전이의 전자 엔트로피 hook 만으로 완성된다. 이 두 가지는 **기존 dqdv 바디를 건드리지 않고** 표현 가능하다 — 단, ΔS_rxn 이 배열 U_j 산출([코드 L433-436])에 들어가야 하므로 hook 삽입점 설계가 §1.4의 핵심이다.

### 1.2 MSMR 동형 매핑표 (코드 심볼 ↔ Ch1 식)

| Ch1 물리 (식) | 흑연 코드 심볼 | LCO 코드 심볼(제안) | 부호·차이 |
|---|---|---|---|
| 용량 가중 $X_j\!\leftrightarrow\!Q_j$ [eq:msmr] | `tr['Q']` [L366·L477] | `tr['Q']` 동일 | 양극 3전이 Q 재배분 |
| 중심 $U_j^0\!\leftrightarrow\!U_j^d$ [eq:msmr] | `func_U_j`/`center` [L79·L448] | 동일 함수, 값만 양극(~3.9–4.2 V) | [Ch1 sec:lco-center] 식·부호 1:1, 입력값만 다름 |
| 폭 $\omega_j\!\leftrightarrow\!w_j$ [eq:msmr] | `func_w`/`_width` [L75·L284] | 동일 $w=nRT/F$ | [Ch1 sec:lco-peak] LCO 세 전이 모두 두-상 → 현상학적 피팅 폭 |
| 방향 인자 $f\!\leftrightarrow\!-\sigma_d$ [eq:msmr] | `func_ksi_eq` 의 `s` [L96] | 동일 `s`/`sigma_d` | ★$f=-\sigma_d$ ([Ch1 sec:lco-code] 명시): 지수 $+f(U−U^0)$ vs $-\sigma_d(V−U^d)$ 자리 일치 |
| 삽입 반응 ΔS_rxn [eq:Uj] | `tr['dS_rxn']` [L78] | `tr['dS_rxn']` = **config 중심표준값 ΔS⁰_j 만** | ★이중계산 금지(§1.5) |
| MIT 전자항 ΔS_e [eq:dSegate] | (없음) | `tr['lco_electronic']` dict → hook | 흑연=0, T1 에서만 켜짐 |

**★부호 골격 동일성** [Ch1 sec:lco-map·sec:lco-center]: 방전($\sigma_d=+1$)은 LCO 입장에서 **리튬화**(Li⁺ 유입, Co⁴⁺→Co³⁺ 환원, $x$↑, 전위 하강), 충전($\sigma_d=-1$)은 **탈리튬화**($x$↓, 전위 상승). $\partial U_j/\partial T=\Delta S_{rxn,j}^{cat}/F$ [Ch1 eq:lco-dUdT]는 흑연과 **부호까지 동일한 관계식**이고 값만 전이별 $\Delta S_{rxn,j}^{cat}$ 가 정한다 → 코드 `func_U_j`([코드 L79])를 **그대로 재사용**(부호 뒤집기 없음).

### 1.3 `LCO_STAGING_LIT` 신규 상수 (초기값 데이터셋)

[Ch1 tab:lco-staging]의 3전이(하프셀 vs Li, ≤4.2–4.5 V)를 흑연 `GRAPHITE_STAGING_LIT`([코드 L531-560])와 **같은 키 구조**로 신규 상수로 추가한다. **기존 상수는 불변**(원형 보존 [코드 L527-528]). 값은 신뢰값 아닌 초기값(피팅 override 전제 [Ch1 sec:lco-map]).

```
LCO_STAGING_LIT = [
    {   # T1 (MIT)  U~3.90 V, x=0.94-0.75, insulator->metal
        'U': 3.90, 'n': 1.0, 'Q': ...,          # w=nRT/F (두-상 현상학적 폭)
        'dH_rxn': ..., 'dS_rxn': <ΔS0_config 중심표준값>,  # 전자항 별도
        'Omega': <>2RT>, 'gamma': ...,           # MIT 2상역 히스 (eq:dUhys)
        'dH_a': ..., 'dVdq_qa': ...,             # 동역학 꼬리 (흑연과 동형)
        'lco_electronic': {                      # ★T1 전용 전자항 (hook 입력)
            'g_max': 13.0,          # e/eV/atom (tier A anchor, x=0 끝점)
            'x_MIT': 0.85,          # 천이 중심 (0.75-0.94 중앙)
            'dx_MIT': 0.05,         # 게이트 폭 (2상역 폭 0.19 -> logistic ±2dx)
        },
    },
    {   # T2 (order-disorder a) U~4.05 V, x~0.55, hex->monoclinic
        'U': 4.05, 'n': 1.0, 'Q': ...,
        'dH_rxn': ..., 'dS_rxn': +0.47,          # config 주도 (Motohashi @x=1/2)
        'Omega': <>2RT>, 'gamma': ..., 'dH_a': ..., 'dVdq_qa': ...,
        # 'lco_electronic' 없음 -> 전자항 off (hook 이 0 반환)
    },
    {   # T3 (order-disorder b) U~4.17-4.20 V, x~0.48, monoclinic->hex
        'U': 4.18, 'n': 1.0, 'Q': ...,
        'dH_rxn': ..., 'dS_rxn': +1.49,          # config 주도 (Motohashi @x=2/3)
        'Omega': <>2RT>, 'gamma': ..., 'dH_a': ..., 'dVdq_qa': ...,
    },
    # (T4 O3->H1-3 ~4.55 V 는 하프셀 상한 밖 -> 옵션, 미포함)
]
```

- **키 재사용 정합** [Ch1 sec:lco-code (i)]: `(dH_rxn, dS_rxn, Q, Omega, dH_a, dVdq_qa, ...)` 전이 dict 키 구조가 흑연과 동일 → `_n_factor`/`_width`/`func_U_j`/`_resolve_lag_length` 등 기존 메서드가 **무변경**으로 소비.
- **`lco_electronic` = 유일한 신규 키**: T1 에만 존재. 없으면 hook 이 0 반환 → T2/T3 는 흑연과 완전 동형. 이 "존재/부재 = on/off" 패턴은 흑연 `dH_a is None → L_V=0`([코드 L319]) 스위치 관행과 일관.
- `dS_rxn` 슬롯의 의미 = **config 중심 표준값 ΔS⁰_j**(봉우리 내부 분포는 logistic 재생성, §1.5).

### 1.4 함수 시그니처 — 전자항 hook

**설계 원칙**: 흑연 `dqdv`([코드 L370-480])의 전이 루프에서 배열 중심 U_j 는 [코드 L433-436]에서 `func_U_j(T_work, dH_rxn, dS_rxn)` 로 산출된다. LCO 전자항은 이 **ΔS_rxn 에 x-의존 몫을 더하는** 것이므로, U_j 산출 직전에 hook 이 개입해야 한다. 그러나 흑연 `dqdv` 바디를 수정하면 회귀가 깨진다(§3). **해법 = 흑연 클래스에 "no-op hook" 를 심어두는 대신, dqdv 바디 자체를 건드리지 않는 override 지점을 만든다.**

O2 채택안 = **`func_U_j` 를 대체하지 않고, LCO 서브클래스가 전이 dict 를 "전개(pre-expand)"** 한다:

```
# 신규 모듈함수 (순수, 흑연 무관):
def func_delta_Se_molar(x, T, g_max, x_MIT, dx_MIT):
    """몰당 전자 엔트로피 ΔS_e^mol(x,T) [J/mol/K] — MIT-logistic 게이트.
    [Ch1 eq:dSegate]·[eq:dSemolar]·[eq:gunit].
    반환 <0 (삽입 기준). σ=logistic((x-x_MIT)/dx_MIT).
      = -(π²/3)·R·(kB·T/e_V)·(g_max/dx_MIT)·σ·(1-σ)
    ★e_V 나눗셈형([eq:gunit]) — 곱셈 시 1/e_V² (~4e37배) 오류."""
    # R, kB 는 코드 전역상수 [L65-68]; e_V = 1.602176634e-19 신규 상수
    ...

def func_x_of_xi(xi_eq_1, x_lo=0.75, x_hi=0.94):
    """T1 진행률 ξ_eq,1(V) -> 조성 x 매핑 [Ch1 sec:lco-decomp ★(i) 좌표 매핑].
    코드 dqdv 는 전압 격자, 게이트는 조성 x 함수 -> x=x(ξ_eq,1(V)) 로 좌표 연결.
    방전(리튬화) ξ:0->1 진행이 x 증가에 대응 (전이 구간 정규화)."""
    ...
```

```
# 신규 서브클래스:
class LCOCathodeDQDV(GraphiteAnodeDischargeDQDV):
    """LCO 양극 dQ/dV — 흑연 클래스 상속(구조 변경 0, MSMR 동형 [Ch1 eq:msmr]).
    유일한 차이 = T1 전이 ΔS_rxn 에 전자항 ΔS_e^mol(x,T) 를 더하는 것.
    dqdv/equilibrium/curve 는 부모 그대로 재사용(무변경)."""

    def _delta_S_extra(self, tr, T_work, xi_eq):
        """전자 엔트로피 몫 hook. 흑연 base 는 상수 0 반환(§3);
        LCO 는 'lco_electronic' 있는 전이(T1)에서 ΔS_e^mol 반환.
        반환 shape = T_work 배열 (V-격자 위 x-의존)."""
        elec = tr.get('lco_electronic')
        if elec is None:
            return 0.0
        x = func_x_of_xi(xi_eq)
        return func_delta_Se_molar(x, T_work, **elec)  # <0 at MIT
```

**dqdv 바디 개입 최소화 전략(핵심 설계 판단)**: 부모 `dqdv` 바디를 수정하지 않으려면 hook 을 **U_j 산출 직전**에 넣어야 하는데, 그 지점은 부모 [코드 L433-436] 안이다. O2 는 두 경로를 제시하고 **경로 B 를 권고**한다:

- **경로 A (기각)**: 부모 `dqdv` L433-436 에 `dS_rxn_eff = tr['dS_rxn'] + self._delta_S_extra(...)` 한 줄 삽입. → 부모 바디 수정 = **byte 회귀 깨짐**. 기각.
- **경로 B (채택)**: 부모 `dqdv` 에 **`_effective_dS_rxn(tr, T_work, V_work, sigma_d)` 라는 seam(이음매) 메서드를 신설**해 L434 의 `func_U_j(T_work, tr['dH_rxn'], tr['dS_rxn'])` 호출을 `func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr, T_work, V_work, sigma_d))` 로 바꾼다.
  - 흑연 base 의 `_effective_dS_rxn` = **`return tr['dS_rxn']` (항등)** → 흑연 수치 완전 불변(§3에서 byte 회귀로 실증).
  - LCO override 의 `_effective_dS_rxn` = `tr['dS_rxn'] + ΔS_e^mol` (T1 에서만 nonzero).
  - **트레이드오프 명시**: 경로 B 는 부모 `dqdv` 의 **L434 한 줄**을 `replace_symbol_body` 로 바꾼다(전체 함수 재작성 아님, 물리 불변). 흑연 회귀는 seam 이 항등이라 **수치 0-diff 보장**되나, "1바이트도 수정 X" 문언과는 L434 한 줄에서 충돌한다. → **Decision Gate (§6 리스크 R1)**: master 가 (B) seam 삽입(권고) vs (C) dqdv 전체를 LCO 에서 override-복제 중 택. O2 권고 = **(B)** — 복제(C)는 DRY·drift 비용이 seam 1줄 수정보다 크고, seam 항등성은 회귀 하네스가 반증가능하게 검증한다.

> **자기완결 주석(타 전공 석박사용)**: "seam" = 부모 함수의 한 계산 단계를 이름 붙인 메서드로 빼내, 서브클래스가 그 단계만 갈아끼우게 하는 리팩토링. 부모 기본 구현이 원래 값을 그대로 반환하면(항등), 부모 동작은 정의상 불변이다. 여기서 갈아끼우는 단계 = "이 전이의 유효 반응 엔트로피는 얼마인가"이며, LCO 만 전자항을 더한다.

### 1.5 ★이중계산 직교 — LCO dQ/dV 에서의 처리

[Ch1 sec:lco-decomp ★이중계산 금지(B)]·[Ch2 eq:revheat use-this]가 못박는 규칙:

> $\Delta S_{rxn,j}^{cat}(x,T) = \underbrace{\Delta S_j^{config}}_{\text{logistic } w=RT/F \text{ 가 담음}} + \underbrace{\Delta S_j^{vib}}_{\text{음 baseline}} + \underbrace{\Delta S_{e,j}^{mol}(x,T)}_{\text{MIT 게이트}}$ [Ch1 eq:lco-decomp]

- **config 슬롯 = 봉우리 중심 표준값 ΔS⁰_j 만**. 봉우리 내부 조성 의존 $R\ln[(1-\xi)/\xi]$ 는 격자기체 점유 분포([Ch1 sec:dist])에서 **logistic 이 자동 생성**하므로, `dS_rxn` 에 재가산하면 **두 번 셈**([Ch1 sec:lco-decomp]·[Ch2 sec:limits keybox]: 중심 $\xi=\tfrac12$ 에서 config$=0$ 이라 표준값 정확 회수).
- **코드 분리 방법**: `tr['dS_rxn']` = 중심 표준값 ΔS⁰_j (상수). 봉우리 내부 항은 코드가 `func_ksi_eq`([코드 L94-97])로 산출하는 $\xi_{eq}$ 에서 dQ/dV 곡선상 이미 반영됨 → **`dS_rxn` 에 절대 `R ln[ξ/(1−ξ)]` 를 더하지 않는다**. 이것이 dQ/dV 경로에서의 직교 처리다.
- **전자항의 직교(가법성 정당화)** [Ch1 sec:lco-decomp ★가법성]: config(리튬 자리 점유 배열)와 ΔS_e(전도 전자 밴드 점유)는 서로 다른 자유도라 통계역학적으로 **근사 직교** ($Z=Z_{config}\cdot Z_{elec}$ 인수분해 → $S=S_{config}+S_{elec}$, 교차항 선도차수 0). 따라서 전자항을 **더하는 것 자체는 정당**하고, 무이중계산은 각 슬롯에 자기 자유도 몫만 넣는 §1.5 규칙이 보장한다.

---

## §2. 가역 발열 q_rev 설계

### 2.1 신규 심볼 시그니처

[Ch2 eq:qrev]의 boxed 식을 1:1 코드화. **T 는 한 번만 곱한다**(식 자체가 $-IT\cdot\partial U/\partial T$, T 중복 금지).

```
# 신규 모듈함수 (순수):
def func_q_rev(I, T, dUoc_dT):
    """가역 발열 q_rev [W] = -I·T·∂U_oc/∂T  [Ch2 eq:qrev].
    I>0 방전. 부호: ∂U/∂T>0(ΔS>0) -> q_rev<0 흡열 / <0 -> 발열.
    ★T 한 번만(식이 이미 -IT·∂U/∂T). ΔS 경유 원하면 func_q_rev_from_dS 사용."""
    return -I * T * dUoc_dT

def func_q_rev_from_dS(I, T, dS):
    """등가형 q_rev = -(I·T/F)·ΔS(x)  [Ch2 eq:qrev 우변].
    ΔS = +F·∂U_oc/∂T ([Ch2 srcbox] 규약). F = 코드 전역상수 [L66].
    ★직교: ΔS 는 config 중심표준값 + 분포 + dS_e 조립 (§2.3), 재가산 금지."""
    return -(I * T / F) * dS
```

```
# 신규 메서드 (GraphiteAnodeDischargeDQDV 에 추가; LCO 상속):
def reversible_heat(self, V_app, T, I_abs, Q_cell, s=+1, x_grid=None):
    """가역 발열 곡선 q_rev(V 또는 x) [Ch2 eq:qrev + use-this 종합식].
    ★새 물리는 여기서만. dqdv 경로 무개입(별도 메서드, §3 회귀 무관).
    반환 = q_rev 배열 (V_app 격자 위).
    절차: (1) ∂U_oc/∂T(x) 겹침가중 조립 (_dUoc_dT_weighted)
          (2) I=σ_d·|I_abs| 부호화 후 func_q_rev.
    입력 가드: _finite_nonneg('I_abs')·_finite_pos('T'/'Q_cell') 재사용 [L167-188]."""
    ...

def _dUoc_dT_weighted(self, U_oc, T, V_work=None):
    """겹침가중 ∂U_oc/∂T(x) [Ch2 eq:revheat use-this 종합식].
      ∂U_oc/∂T = Σ_j Q_j·g_j·[ΔS0_j/F + (R/F)ln(ξ_j/(1-ξ_j))] / Σ_j Q_j·g_j
      g_j = ξ_j(1-ξ_j)/w_j   (= 평형 peak 모양, [Ch1 eq:eqpeak]·[코드 L366])
    ★config 봉우리내부항 (R/F)ln(ξ/(1-ξ)) 은 여기서 명시 조립(dQ/dV 와 별 경로).
    ★LCO: T1 에서 _delta_S_extra 로 ΔS_e^mol 을 ΔS0_j 에 가산(직교, §2.3)."""
    ...
```

### 2.2 ΔS(x) 조립 — 중심 ΔS⁰_j + config 분포항 + dS_e

[Ch2 eq:revheat use-this]의 완전식을 그대로 조립한다:

$$\frac{\partial U_{oc}}{\partial T}(x)=\frac{\sum_j Q_j\,g_j(x)\,[\Delta S^0_j/F+(R/F)\ln(\xi_j/(1-\xi_j))]}{\sum_j Q_j\,g_j(x)},\quad g_j=\frac{\xi_j(1-\xi_j)}{w_j}$$

- **입력 재사용**: $\{\Delta S^0_j, Q_j, U_j, w_j\}$ 는 전이 dict 에서, $\xi_j(V,T)$ 는 `func_ksi_eq`([코드 L94-97])로. $g_j$ 는 [Ch1 eq:eqpeak] 평형 peak 모양([코드 L366]의 `ksi_eq*(1-ksi_eq)/w`)과 **동일 함수** → 재사용.
- **$U_{oc}(x,T)$ 역산**: [Ch2 eq:implicit] $\sum_j Q_j\xi_{eq,j}(U_{oc},T)=Qx$ 음함수를 풀어 SOC $x$ 에서 $U_{oc}$ 를 얻고 되먹임. dqdv 는 V 격자 위이므로, `reversible_heat` 도 **V_app 격자 위**에서 직접 평가하면 음함수 역산 없이 각 V 에서 $\xi_j(V)$ 로 조립 가능(V→x 는 진단용).
- **부호 검산** [Ch2 sec:revheat]: 방전($I>0$)에서 $\Delta S>0$→$q_{rev}<0$ 흡열, $\Delta S<0$→$q_{rev}>0$ 발열. stage 2→1($x\approx0.5$, 흑연 $\Delta S_{rxn}=-16$ J/mol/K [코드 L555])의 큰 음 ΔS → 방전 시 발열 봉우리 = calorimetry 정합.

### 2.3 ★이중계산 직교 — 코드에서의 분리 방법 (q_rev)

**가장 위험한 결함 클래스** — 명시적으로 분리 규칙을 코딩한다.

1. **config 중심 ΔS⁰_j 는 `tr['dS_rxn']` 에서 한 번만**. use-this 식의 `ΔS0_j/F` 항이 이 몫이다.
2. **봉우리 내부 config 분포항 `(R/F)ln(ξ/(1-ξ))` 는 use-this 식이 명시적으로 더하되, `tr['dS_rxn']` 에는 절대 재가산하지 않는다**. [Ch2 sec:limits keybox]·[Ch1 sec:lco-decomp]: 중심 $\xi=\tfrac12$ 에서 이 항 = $R\ln 1=0$ 이라 표준값이 정확히 회수됨 → 두 항이 서로 다른 자리를 채운다(중심값 + 중심으로부터의 편차).
   - **코드 가드**: `_dUoc_dT_weighted` 는 `ΔS0_j = tr['dS_rxn']` (raw dict 값) 만 읽고, 분포항은 런타임에 `(R/F)*np.log(xi/(1-xi))` 로 **재계산**. dict 를 오염시키지 않으므로 재가산 물리적 불가능.
3. **전자항 ΔS_e^mol 은 ΔS⁰_j 에 가산(직교)**, 봉우리 내부 항과는 다른 자유도라 중복 아님. `_delta_S_extra` hook([§1.4])이 T1 에서만 nonzero → `ΔS0_j_eff = tr['dS_rxn'] + _delta_S_extra(...)`.
   - **★단위 가드** [Ch1 sec:lco-code (ii)·eq:dSemolar]: 전자항은 **몰당**($N_A$ 곱한 [Ch1 eq:dSemolar], J/mol/K)을 써야 함. 자리당 [Ch1 eq:dSe]($k_B^2$ 차원) 직접 사용 시 $\sim10^{23}$배 과소. `func_delta_Se_molar` 가 몰당형으로 반환(§1.4)해 이 슬롯 단위 일치.
   - **★eV→J 가드** [Ch1 eq:gunit]: $g_J=g_{eV}/e_V$ **나눗셈**. 곱셈 시 $1/e_V^2\approx4\times10^{37}$배 오류 → 함수 내부 나눗셈형 고정, 상수 `e_V=1.602176634e-19` 신규.

> **직교 = "더해도 되나(가법성)"와 "과대계상 없나(무초과)"의 분리** [Ch1 sec:lco-decomp]. 가법성은 config·elec 자유도 근사 직교($Z$ 인수분해)가, 무초과는 각 슬롯에 자기 몫만 넣는 §2.3-1~3 규칙이 보장.

### 2.4 비가역 3분해 옵션

[Ch2 eq:qrev]의 전체 발열은 $\dot Q = \dot Q_{irr} + \dot Q_{rev}$, $\dot Q_{irr}=I(U_{oc}-V)\ge0$ (과전압 소산, 2법칙상 항상 발열 [Ch2 L648]).

- **Ch2 본문은 $\dot Q_{irr}$ 를 lumped 단일항** $I\eta$ ($\eta=U_{oc}-V$)로 둔다 [Ch2 eq:qrev L643]. 기저 3분해 $I^2R + I\eta_{ct} + I\eta_{diff}$ (ohmic + 전하전달 + 확산 과전압)는 $\eta = IR_n + \eta_{ct} + \eta_{diff}$ 의 표준 전개이나, **Ch2 는 이를 명시 박스로 두지 않음** → [근거 미발견](Ch2 는 lumped $I(U_{oc}-V)$ 만 boxed).
- **설계 제안(옵션)**: `func_q_irr(I, U_oc, V)` = `I*(U_oc - V)` (lumped, [Ch2 eq:qrev] 직접) 를 기본 제공. 3분해 `func_q_irr_split(I, R_n, eta_ct, eta_diff)` = `I*I*R_n + I*eta_ct + I*eta_diff` 는 **옵션 helper**로만 제공하고, 그 근거가 Ch2 boxed 식이 아니라 표준 전개임을 docstring 에 [추정]·[Ch2 범위 밖] 라벨로 명시. `R_n` 은 기존 분극 저항([코드 L235·L408])과 동일 심볼 재사용. **기본 경로는 lumped** (Ch2 정합).
- **활성화 엔트로피 혼동 금지 가드** [Ch2 ssec:elec 반응 vs 활성화]: q_rev 에 들어가는 것은 **반응(평형) 엔트로피 ΔS(x)** 뿐. 동역학 꼬리의 활성화 엔트로피 `tr['dS_a']`([코드 L100·L334])는 **비가역**이라 q_rev 에 절대 넣지 않는다. `reversible_heat` 는 `dS_a` 를 읽지 않는다(코드 상 분리 보장).

---

## §3. ★흑연 회귀 0-diff 가드

### 3.1 무섭동 구조 (상속 채택)

[P1 Confirmed Non-Changes]·[코드 L34-36 "1바이트도 변조 X"]가 최우선 제약. 상속(§1.1 (c)) 구조에서 흑연 경로 무섭동을 보장하는 방식:

| 요소 | 흑연 경로 상태 | 보장 방식 |
|---|---|---|
| `GraphiteAnodeDischargeDQDV.equilibrium` [L350-367] | **완전 불변** | 신규 코드 미접촉. LCO 는 상속만 |
| `GraphiteAnodeDischargeDQDV.curve` [L483-508] | **완전 불변** | 상속, 부모 dqdv 재사용 |
| 순수함수 `func_w`/`func_U_j`/`func_ksi_eq`/`func_L_q`/`_causal_lowpass` [L74-128] | **완전 불변** | LCO 는 재사용만, 신규 함수는 별도 모듈함수 |
| `GRAPHITE_STAGING_LIT` [L531-560] | **완전 불변** | `LCO_STAGING_LIT` 별도 상수 신설 |
| 死코드 `func_U_j_hys` [L82-91] | **불변(보존)** | [P1] 판정 따름 — 개정 X |
| `dqdv` [L370-480] | **seam 1줄만**(경로 B, §1.4) — L434 `dS_rxn` → `_effective_dS_rxn(...)` | 흑연 base seam = 항등(`return tr['dS_rxn']`) → **수치 0-diff** |

**seam 항등성 = 0-diff 의 논리적 근거**: 흑연 base 의 `_effective_dS_rxn(tr,...)` 가 `tr['dS_rxn']` 를 그대로 반환하면, `func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr,...))` 는 원래 `func_U_j(T_work, tr['dH_rxn'], tr['dS_rxn'])`([코드 L434])와 **인자가 완전 동일** → 출력 배열 byte 일치. 이는 회귀 하네스로 반증가능하게 검증(§3.2).

### 3.2 회귀 하네스 설계 (byte-일치 검증법)

`GRAPHITE_STAGING_LIT` 로 개정 전/후 `curve()`·`dqdv()`·`equilibrium()` 출력이 **byte 일치**함을 검증한다.

```
# 회귀 하네스 (신규 self-test 또는 별도 tests/test_graphite_regression.py):
def test_graphite_curve_byte_identical():
    """개정 후 흑연 곡선이 개정 전과 byte 일치 (seam 항등성 실증).
    골든 = 개정 전 커밋에서 저장한 .npy (또는 고정 seed 재산출)."""
    model = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05)
    V = np.linspace(0.03, 0.34, 1000)   # [코드 L568] self-test 격자
    for s, I in [(+1,0.02),(+1,0.2),(+1,1.0),(-1,0.02),(-1,0.2),(-1,1.0)]:
        y_new = model.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s)
        y_gold = np.load(f"golden/graphite_dqdv_s{s}_I{I}.npy")
        assert np.array_equal(y_new, y_gold), f"byte diff at s={s},I={I}"
    # equilibrium·curve·비등온 T(V)·히스 split 도 동일 검증
```

- **검증법 3계층**:
  1. **byte 일치** `np.array_equal(y_new, y_gold)` — bit-exact(부동소수점 동일 연산순서 → 동일 bit). seam 항등이면 통과.
  2. **면적 보존** [P1 §4 보완4·§2-D]: 개정 전 self-test 에 부재했던 **면적=Q assert 추가**(∫Q·ξ(1−ξ)/w dV = Q, [P1] "면적 회귀 가드 결함" 해소). 이는 P4 개정 기회에 흑연 회귀 하네스를 강화하는 부수 이득.
  3. **DC gain=1 보존** [P1 §2-D]: `_causal_lowpass` 미접촉 → DC 이득 1 자동 보존, 면적 보존 유지.
- **골든 생성**: 개정 착수 전 master 가 현 코드로 골든 `.npy` 저장(HEAD 커밋 기준). 이것이 회귀 baseline.
- **면적보존 DC=1 유지** [P1]: LCO 추가·q_rev 추가가 `_causal_lowpass`([L110-128])·평형 peak([L366])를 건드리지 않으므로 흑연 면적 보존(∫=1.000000 [P1 Execution Evidence])은 정의상 불변.

### 3.3 LCO 자체 검증 (round-trip 가드)

[Ch1 sec:lco-decomp ★(ii) round-trip 가드]: LCO config 중심표준값(Motohashi ~0.47/1.49)은 초기값(신뢰값 아님)이므로, 흑연 $\Delta S_{rxn}=-16$ round-trip 과 **동격 절차**로 T1 위치 $U_1(298)\approx3.90$ V 와 $\partial U_1/\partial T$ 부호·기울기를 self-test 로 맞춘 뒤 승격.

- **전자항 식별 신호** [Ch1 sec:lco-Se·eq:U1T2]: $\Delta S_{e,1}\propto T$ 라 $\partial U_1/\partial T$ 가 **T 에 선형**(config·vib 는 상수). U 이동은 $\propto T^2$ ([Ch1 eq:U1T2] $U_1(T)=U_1(T_0)+\frac{\Delta S_0}{F}(T-T_0)+\frac{a_e}{2F}(T^2-T_0^2)$, ★$\tfrac12$ 인자 = 적분 $\int a_e T'dT'$). self-test 는 "$\partial U/\partial T$ 가 T-선형"을 확인(위치가 T-선형이 아님에 주의).
- **골 깊이 검산** [Ch1 sec:lco-gate]: 천이 중심 $\sigma(1-\sigma)=\tfrac14$, $g_{max}=13$, $\Delta x_{MIT}=0.05$, $T=300$K 에서 $\Delta S_{e,1}^{mol}\approx-46$ J/mol/K. self-test assert 로 이 스케일 확인(허위 정밀 금지, tier 병기).

---

## §4. Serena 편입 레시피

**원칙**: 신규 심볼은 `insert_after_symbol` 로 추가, 기존 심볼 `replace_symbol_body` 는 **최소화**. 코드 소유권(식별자·대소문자·정수코드 보존) 준수, 지정 범위 외 임의수정 X.

| # | 편입 대상 | Serena 연산 | 삽입 지점 | 기존 심볼 영향 |
|---|---|---|---|---|
| 1 | `e_V` 상수 (1.602176634e-19) | `insert_after_symbol` | `h` 전역상수 뒤 [L68] | 없음(추가만) |
| 2 | `func_delta_Se_molar` | `insert_after_symbol` | `func_chi_d` 뒤 [L163] (순수함수 계층 말미) | 없음 |
| 3 | `func_x_of_xi` | `insert_after_symbol` | #2 뒤 | 없음 |
| 4 | `func_q_rev` / `func_q_rev_from_dS` / `func_q_irr`(옵션) | `insert_after_symbol` | #3 뒤 | 없음 |
| 5 | `_effective_dS_rxn` (base 항등 메서드) | `insert_after_symbol` | `GraphiteAnodeDischargeDQDV.equilibrium` 앞 또는 `_resolve_lag_length` 뒤 [L347] | 없음(신규 메서드) |
| 6 | `_delta_S_extra` (base no-op) + `reversible_heat` + `_dUoc_dT_weighted` | `insert_after_symbol` | `curve` 뒤 [L508] (클래스 말미) | 없음 |
| 7 | `LCO_STAGING_LIT` 상수 | `insert_after_symbol` | `GRAPHITE_STAGING_LIT` 뒤 [L560] | 없음 |
| 8 | `LCOCathodeDQDV` 클래스 | `insert_after_symbol` | `GRAPHITE_STAGING_LIT` 뒤 (클래스 정의 영역) | 없음 |

**★유일한 `replace_symbol_body` (경로 B seam, §1.4)**:

| 대상 | 연산 | 변경 내용 | 근거·최소성 |
|---|---|---|---|
| `GraphiteAnodeDischargeDQDV.dqdv` [L370-480] | `replace_symbol_body` (1줄) | L434 `func_U_j(T_work, tr['dH_rxn'], tr['dS_rxn'])` → `func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr, T_work, V_work, sigma_d))` | 물리 불변(seam 항등), 흑연 0-diff. **나머지 L370-480 전부 원형 보존**. ★Decision Gate: master 승인 필요(§6 R1) |

- **replace 최소성 근거**: 전체 함수 재작성이 아니라 **호출 인자 1개**를 항등 seam 으로 감싸는 것. `_effective_dS_rxn` base 구현이 `tr['dS_rxn']` 반환이므로 흑연 수치 불변(§3.2 byte 회귀로 실증). 이 1줄이 없으면 LCO 전자항이 dqdv 에 들어갈 seam 이 없어 dqdv 전체 override-복제(DRY 위반)가 강제됨 → 1줄 seam 이 최소 개입.
- **정수코드·대소문자 보존**: 기존 심볼명(`func_U_j`·`dqdv`·`GRAPHITE_STAGING_LIT` 등) 일절 rename 없음. 신규 심볼만 추가.
- **死코드 `func_U_j_hys` 미접촉** [P1 Open Issues]: P4 개정 후보(死코드 정리·z_cut docstring·면적 assert)는 **본 LCO/발열 개정과 분리** — 본 드래프트는 LCO·q_rev 확장에 한정, 死코드 정리는 별도 개정 트랙(단, §3.2 면적 assert 추가는 회귀 하네스 강화로 포함 권고).

---

## §5. 그래프 검증 계획

흑연+LCO dQ/dV·발열 곡선 개형 확인. `plot_*.py` 계열(흑연 기존 `plot_dqdv.py` [코드 L11 언급])와 동형.

### 5.1 흑연 회귀 그래프 (0-diff 시각 실증)
- 개정 전/후 `dqdv` 곡선 overlay → **완전 겹침**(byte 일치의 시각 확인). residual 패널 = 0 직선.
- 검증: `max|y_new − y_gold| == 0.0` 텍스트 병기.

### 5.2 LCO dQ/dV 개형 (양극 세 봉우리)
- `LCOCathodeDQDV(LCO_STAGING_LIT)` 로 V∈[3.7, 4.3] V 격자 dQ/dV → **세 봉우리** T1(~3.90)·T2(~4.05)·T3(~4.17–4.20 V) [Ch1 sec:lco-peak].
- 검증 개형: (a) 봉우리 위치 = 중심 $U_j^d$, (b) T2·T3 는 큰 Ω order-disorder 로 흑연보다 날카로운 좁은 한 쌍 [Ch1 sec:lco-hys], (c) 면적 = Q_j 보존, (d) 전 구간 유한·비음수(평형종).
- **다온도 오버레이**: T=258/298/318 K 에서 T1 봉우리 위치의 **온도 이동**. 전자항 식별 신호 = $\partial U_1/\partial T$ 가 T 에 선형(U 이동 $\propto T^2$ [Ch1 eq:U1T2]) → 등간격 온도에서 이동폭이 고온측에서 커지는(곡률) 개형 확인.

### 5.3 가역 발열 곡선 개형
- **흑연 q_rev(V)**: `reversible_heat(V, ...)` → SOC 따라 부호 교대 [Ch2 sec:revheat]. 저-$x$(고 V, 희박) 흡열($q_{rev}<0$, ΔS>0)·고-$x$(저 V, 만충) 발열($q_{rev}>0$, ΔS<0). stage 2→1 큰 음 ΔS 에서 발열 봉우리.
- **LCO q_rev(V)**: T1 MIT 전자항이 만드는 $q_{rev}$ 특징(전자 골). config-only 대비 전자항 on/off overlay 로 MIT 게이트 기여 시각화([Ch1 fig:lco-electronic] 파선 개형과 대조).
- **부호 검산 그래프**: $q_{rev}$ 와 $-\Delta S(x)$ 부호 일치([Ch2 eq:qrev]) 패널 병기.
- **직교 검증 그래프**: `dS_rxn`(중심)만 vs 중심+분포항 vs 중심+분포+전자 세 곡선 overlay → 각 항이 서로 다른 자리를 채움을 시각 확인(재가산 시 봉우리 2배로 튀는 것과 대조).

---

## §6. 리스크·Decision Gate

| ID | 리스크 | 영향 | 대응 |
|---|---|---|---|
| **R1** ★ | **dqdv seam(경로 B) = L434 1줄 `replace_symbol_body`** — "1바이트 X" 문언과 충돌 | 흑연 회귀는 seam 항등으로 0-diff(반증가능 검증)이나 문언 위반 소지 | **Decision Gate(master)**: (B) seam 1줄(O2 권고) vs (C) dqdv override-복제. B 는 DRY·최소개입, C 는 원형 완전보존이나 복제 drift. master 판단 |
| R2 | 전자항 단위(자리당 vs 몰당)·eV→J | $10^{23}$/$4\times10^{37}$배 오류 | `func_delta_Se_molar` 내부 몰당·나눗셈 고정 + self-test 골 깊이(~−46 J/mol/K) assert [Ch1 sec:lco-gate] |
| R3 | 이중계산(config 봉우리내부 재가산) | q_rev·U_j(T) 봉우리 2배 오류 | `dS_rxn`=중심표준값만, 분포항 런타임 재계산(dict 미오염, §2.3) |
| R4 | x↔ξ_eq,1 좌표 매핑 [Ch1 sec:lco-decomp (i)] | 전자항 위치 어긋남 | `func_x_of_xi` 로 T1 진행률→조성 매핑, self-test 로 x_MIT 정렬 확인 |
| R5 | 死코드/z_cut docstring/면적 assert [P1 Open Issues] | 본 트랙 범위 밖 | 별도 개정 트랙. 면적 assert 만 회귀 하네스 강화로 포함 권고 |
| R6 | 흑연 dS_a(활성화)를 q_rev 에 혼입 | 가역/비가역 혼동 [Ch2 ssec:elec] | `reversible_heat` 는 `dS_a` 미참조(코드상 분리) |

---

## §7. 완료 요약 (5줄)

1. **채택 구조**: `LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)` 상속 + 전자항 hook 단일 override — MSMR 동형([Ch1 eq:msmr]) "구조 변경 0, 파라미터 교체 + 전자항 plug-in" 1:1. base 는 `LCO_STAGING_LIT`·전자항 순수함수만 추가.
2. **핵심 시그니처**: `func_q_rev(I,T,dUoc_dT)=−I·T·∂U/∂T`([Ch2 eq:qrev], T 한 번) · `reversible_heat`(겹침가중 use-this 종합식) · `func_delta_Se_molar`(MIT-logistic 게이트, 몰당·eV나눗셈) · seam `_effective_dS_rxn`.
3. **회귀 가드**: 흑연 `dqdv`/`equilibrium`/`curve` 무섭동(seam 항등 → byte 일치 `np.array_equal`), 골든 `.npy` 회귀 하네스 + 면적=Q assert 신설(P1 결함 해소), `_causal_lowpass` DC=1·면적보존 정의상 유지.
4. **이중계산 처리**: config 중심 ΔS⁰_j 만 `dS_rxn` 슬롯 → 봉우리 내부 `R ln[ξ/(1−ξ)]`는 logistic 재생성(재가산 금지, 중심 ξ=½서 0 회수) → 전자항은 직교 자유도라 가산(단위 몰당·eV나눗셈 가드). dict 미오염으로 재가산 물리적 불가능.
5. **리스크(최우선)**: dqdv seam 1줄 `replace_symbol_body`(경로 B)가 "1바이트 X" 문언과 충돌 → **Decision Gate(master)**: seam 최소개입(권고) vs dqdv override-복제. 그 외 전자항 단위·좌표매핑·활성화엔트로피 혼입은 self-test·코드분리로 통제.
