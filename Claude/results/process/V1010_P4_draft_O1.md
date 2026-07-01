# V1.0.10 P4 — 코드개정 설계 드래프트 O1 (LCO 양극 + 가역 발열 + 흑연 0-diff)

> **드래프트 ID**: O1 (9종 경쟁 설계 중 하나). **성격**: 실편입 청사진 = 설계 제안만.
> **불가침**: `.py`·문건·코드 **1바이트도 수정 X**(단일 .py = 공유 가변상태, 실편입은 master 가 Serena 로 1회). 독립 작성(타 드래프트·통합 관여 X).
> **근거 규율**: 모든 설계 결정은 코드 줄(`Anode_Fit_v1.0.10.py`, 703줄)·Ch1(`graphite_ica_ch1_v1.0.10.tex`)·Ch2(`graphite_ica_ch2_v1.0.10.tex`)·P1 audit(`V1010_P1_code-audit_RESULT.md`) 줄근거로만. 추정은 tier 병기. 허위 attribution 금지.
> **4-tier 표기**: [확정]=코드·식 직접 줄근거 / [근거 미발견]=코드·문건으로 못 짚음 / [추정]=설계 판단(근거 명시) / [미검증]=실편입 후 self-test 로 확인 대상.

---

## §0. 목표와 갭 재확인 (설계 전 baseline) [확정]

**대상 코드 현 상태** [확정, P1 §2-E]: `Anode_Fit_v1.0.10.py` 는 **흑연 음극 staging dQ/dV forward 전용**이다. `grep "LCO|q_rev|dS_e|cathode|발열|전자엔트로피"` → No matches (P1 §2-E, C1·C2·C3 교차). 클래스 `GraphiteAnodeDischargeDQDV`(L192), 데이터셋 `GRAPHITE_STAGING_LIT`(L531, U≈0.085–0.210 V), 온도 T 는 외생 입력(등온 스칼라 or T(V) 프로파일 L402–424), 내부 열모델·발열항 없음.

**이론 확정 상태** [확정]: Ch1·Ch2 는 P2·P3 에서 확정 완료. 이제 **이론 → 1:1 코드화**(순서 = 코드→문건→코드).

**세 갭(설계 대상)**:
1. **LCO 양극 dQ/dV** — Ch1 `sec:lco-code`(L1735) 가 "같은 코드가 LCO 를 그린다"의 근거로 **MSMR 동형**(`eq:msmr` L1738)을 못박음: 곡선 클래스 구조 변경 0, 바뀌는 것은 (i) 전이 파라미터 교체 (ii) 전자 엔트로피 항 plug-in 둘뿐(L1748–1757).
2. **가역 발열 q_rev** — Ch2 `sec:revheat`(L637) `eq:qrev`(L645): `q_rev = −IT·∂U_oc/∂T = −(IT/F)ΔS(x)`. 현 코드에 없음(신규 산출 경로).
3. **흑연 회귀 0-diff** — 위 둘의 확장이 기존 `GraphiteAnodeDischargeDQDV.curve()`/`dqdv()`/`equilibrium()` 출력을 **무섭동**으로 둘 것(byte 일치).

---

## §1. LCO 양극 dQ/dV 설계 — 채택 구조 + MSMR 동형 매핑

### 1.1 채택 구조: **합성(composition) — 신규 클래스 `LCOCathodeDQDV`가 흑연 클래스를 내부 위임** [추정, 근거 아래]

세 선택지(신규 클래스 / 일반화 base / 흑연 클래스에 플래그)를 비교해 **신규 클래스 + 흑연 클래스 내부 재사용(합성)** 을 채택한다.

| 선택지 | 흑연 0-diff | LCO 고유항(전자 엔트로피) | 코드 소유권 | 판정 |
|---|---|---|---|---|
| **(a) 상속** `LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)` | 부모 메서드 override 필요 → 부모 경로 오염 위험 | override 로 주입 가능 | 부모 시그니처 계승 | △ override 표면이 넓어 회귀 리스크 |
| **(b) 일반화 base** (흑연 클래스를 base 로 리팩터) | ★기존 클래스 본체를 **수정**해야 함 → 0-diff 위반·코드 소유권 침해 | base 에 hook | 기존 심볼 대수술 | ✗ **탈락**(P1 "코드 불변" + base 프롬프트 "replace_symbol_body 최소화") |
| **(c) 합성** 신규 `LCOCathodeDQDV` 가 내부에 `GraphiteAnodeDischargeDQDV` 인스턴스 보유·위임 | ★기존 클래스 **무변경** → byte 일치 자동 | 위임 전 `ΔS` 슬롯 조립 단계에서 전자항 주입 | 기존 심볼 0-touch, 신규 심볼만 추가 | ✔ **채택** |

**채택 근거** [추정]:
- **0-diff 최강 보장** [확정 근거]: MSMR 동형(`eq:msmr` L1738)이 "곡선 클래스 구조 변경 0"(L1747)을 이미 물리로 보증한다. LCO 는 "파라미터 교체 + 항 하나"(L1748)뿐 — 그렇다면 **기존 클래스를 건드릴 이유가 없다**. 합성은 기존 `GraphiteAnodeDischargeDQDV`(L192–524)를 심볼 단위로 0-touch 로 두어, 흑연 회귀가 "구조적으로" 보장된다(테스트 이전에 코드 위상으로).
- **전자항 주입 지점의 격리** [확정 근거]: LCO 고유항 `ΔS_{e,j}`(`eq:dSemolar` L1018)는 T1 전이의 **`ΔS_rxn` 슬롯에 더해지는 한 줄**(L1752–1753, `sec:lco-code` (ii)). 이는 `func_U_j(T, dH_rxn, dS_rxn)`(L78) 이 소비하는 `dS_rxn` 값의 **조립 단계**에서 처리하면 되고, `func_U_j` 본체나 `dqdv` 루프를 바꿀 필요가 없다. 합성 클래스가 전이 dict 의 `dS_rxn` 을 "config 중심 표준값 + 전자 게이트항(V→x 매핑)"으로 조립해 흑연 인스턴스에 넘긴다.
- **코드 소유권 보존** [확정 근거, P1 Confirmed Non-Changes]: base 프롬프트 §4 "replace_symbol_body 필요한 기존 심볼이 있으면 최소화". 합성은 `replace_symbol_body` **0건**(전부 `insert_after_symbol` 신규 추가)이다.

> **★대안 경고(일반화 base 탈락 상술)** [추정]: (b) 일반화 base 는 "더 깨끗해 보이나" 기존 클래스 본체를 수정한다 — P1 이 "코드 1바이트도 수정 안 함"으로 동결한 심볼(L192–524)을 대수술하는 것이라 0-diff·코드 소유권 두 규율을 동시 위반. 효율로 보여도 실행 전 기각. (base 프롬프트 "명시 선택을 효율 판단으로 대체 금지" 정합.)

### 1.2 MSMR 동형 매핑표 (코드 심볼 ↔ Ch1 식) [확정]

Ch1 `sec:lco-code`(L1738–1746)의 MSMR 식 `x_j = X_j / (1 + exp[f(U−U_j⁰)/ω_j])`(`eq:msmr`)와 코드 transition-logistic `func_ksi_eq`(L94–97, `ξ_eq = 1/(1+exp[−σ_d(V−U_j^d)/w_j])`, `eq:xieq` L770)의 1:1 대응:

| MSMR 기호 (`eq:msmr` L1738) | Ch1/코드 대응 | 코드 심볼·줄 | 근거 |
|---|---|---|---|
| 용량 가중 `X_j` | 전이 용량 `Q_j` | `tr['Q']` (L366·L477) | L1743 `X_j ↔ Q_j` [확정] |
| 중심 `U_j⁰` | 분기 중심 `U_j^d` | `center` (L448) = `func_U_j`(L78) + `func_U_branch`(L143) shift | L1743 `U_j⁰ ↔ U_j^d` [확정] |
| 폭 `ω_j` | 전이 폭 `w_j` | `_width`→`func_w`(L74, `w=nRT/F`) | L1743 `ω_j ↔ w_j` [확정] |
| 방향 인자 `f` | `−σ_d` | `s`/`sigma_d` (L388·L455) | L1744–1746 `f ↔ −σ_d`(두 지수 `+f(U−U⁰)` vs `−σ_d(V−U^d)` 부호 비교로 `f=−σ_d`) [확정] |
| 점유↔진행률 | `θ_j = 1−ξ_j` | `ksi_eq`(L455) | Ch1 L207 [확정] |

**결론** [확정, L1747]: `func_ksi_eq`·`func_U_j`·합산식(`eq:sum`)은 **구조 변경 0** 으로 LCO 에 적용된다. 코드의 전이 dict 키 구조 동일(L1751). → **LCO 는 데이터셋 + 전자항 조립만** 신규.

### 1.3 양극 부호·MIT 전자항 x-의존 [확정]

**양극 부호(흑연과 1:1 대칭)** [확정, Ch1 `sec:lco-map` L303–309]:
- LCO 하프셀 전위 vs Li/Li⁺ ≈ 3.9–4.2 V(흑연 ~0.1 V 와 달리 **높은** 전위), 큰 음의 `ΔH_rxn`(분자 `−ΔH_rxn` 크게 양)에서 옴(L469).
- 부호 골격 동일: 방전(σ_d=+1) = LCO **리튬화**(x↑, 전위↓), 충전(σ_d=−1) = **탈리튬화**(x↑ 진행이 아니라 x↓; ξ:0→1 주 진행 = 탈리튬화, L308).
- `∂U_j/∂T = ΔS_rxn^cat/F`(`eq:lco-dUdT` L474) — **부호까지 흑연과 동일 관계식**, 값만 `ΔS_rxn,j^cat` 이 정함(L306–307). → 코드 `func_U_j`(L78) 그대로, `dS_rxn` 값만 양극 영역.
- **s(부호) 취급**: `_direction_to_sigma`(L510) 그대로 재사용. LCO 특유의 부호 반전 없음 — MSMR `f=−σ_d`(L1746)가 방향 일관성을 이미 보장.

**MIT 전자항 x-의존(흑연엔 없는 고유항)** [확정, Ch1 `sec:lco-electronic` L928–1160]:
- LCO 는 x↓ 에서 절연체→금속 천이(MIT)로 `g(E_F)` 급변(L932·L944) → 전자 엔트로피 `ΔS_e(x,T)` 가 중심 표준값에 흡수 안 됨(x-의존 유지, Ch2 L406–408).
- **MIT-logistic 게이트** `eq:ggate`(L1069): `g(E_F,x) ≈ g_max[1 − σ((x−x_MIT)/Δx_MIT)]`, `g_max=13 e/eV`, `x_MIT≈0.85`, `Δx_MIT≈0.05`(초기값 3개 = 피팅 대상).
- **몰당 닫힌식** `eq:dSegate`(L1083, 유도) → `eq:dSemolar`(L1018, N_A 곱): `ΔS_{e,j}^mol = −(π²/3)·R·(k_B T/e_V)·(g_max/Δx_MIT)·σ(1−σ) < 0`(삽입 기준).
- **부호 못박음**(`eq:dSegate` leading `−`, L1088): g_max·Δx_MIT·σ(1−σ) 모두 양 → `ΔS_{e,j}<0`(삽입 기준), 탈리튬화 시 `|ΔS_e|≈0.18 k_B/atom` 방출.
- **T-의존**(다른 항과 결정적 차이): `ΔS_{e,j} ∝ T`(L1042) → `∂U/∂T|_e ∝ T`(선형), U 이동 ∝ T²(`eq:U1T2` L1055, 계수 `a_e/(2F)`, ½ 인자). 다온도 피팅에서 전자항만 이 T-의존 → config·vib 와 **분리 식별**(L1716).

### 1.4 함수 시그니처 + 신규 상수 [설계 제안]

**신규 데이터셋 상수** (원형 보존 규율 — `GRAPHITE_STAGING_LIT` L531 무변경, 병렬 신규):
```
LCO_STAGING_LIT = [   # 3-전이, vs Li metal, 초기값(피팅 override 전제) — Ch1 tab:lco-staging(L326)
  { 'U': 3.90, 'x_range': (0.94, 0.75), 'char': 'MIT',
    'dS_rxn': <config 중심 표준값 ΔS_0>,   # 전자항 제외(게이트로 별도, 이중계산 금지)
    'Omega': <>, 'Q': <>, 'dH_a': <>, 'dVdq_qa': <>,
    'electronic': True },                  # ★T1 만 전자 게이트 ON (플래그)
  { 'U': 4.05, 'char': 'order-disorder-a', 'dS_rxn': 0.47(≈J/K/mol), ... 'electronic': False },
  { 'U': 4.17, 'char': 'order-disorder-b', 'dS_rxn': 1.49(≈J/K/mol), ... 'electronic': False },
]  # (T4 O3→H1-3 ~4.55V 는 하프셀 상한 ≤4.2–4.5V 면 범위 밖, 옵션)
```
> [확정] 값 출처 = Ch1 `tab:lco-staging`(L326–336), config ΔS 초기값 Motohashi(L688–689 ≈0.47/1.49 J/K/mol). tier 병기: 신뢰값 아니라 초기값(L315·L1730).

**전자 게이트 상수** (`eq:ggate` L1069 초기값):
```
LCO_MIT_GATE = { 'g_max': 13.0,        # e/eV/atom, 완전 metal anchor(x=0), tier A 한 점(L998)
                 'x_MIT': 0.85, 'dx_MIT': 0.05 }   # 피팅 대상 3개(L1073)
E_V = 1.602176634e-19   # J/eV — eq:gunit(L1028), ★나눗셈 형만(L1032 경고)
```

**신규 순수 함수**(모듈 레벨, `insert_after_symbol` 로 `func_chi_d`(L163) 뒤 삽입 후보):
```
def func_dS_e_molar(x, T, g_max, x_MIT, dx_MIT):
    """MIT 게이트 몰당 전자 엔트로피 ΔS_{e,j}^mol [J/mol/K] — eq:dSemolar(L1018)·eq:dSegate(L1083).
    삽입 기준 <0. ★eq:gunit(L1028) 나눗셈 형(k_B*T/E_V) — 곱하면 1/e_V² 배 어긋남(L1032)."""
    z = (x - x_MIT) / dx_MIT
    sig = 1.0 / (1.0 + np.exp(-z))          # logistic (func_ksi_eq 와 동형; overflow-safe 분기 권장)
    return -(np.pi**2 / 3.0) * R * (kB * T / E_V) * (g_max / dx_MIT) * sig * (1.0 - sig)
```
> [확정] 식 = `eq:dSegate`(L1083) 몰당형(L1031). `R`(L65)·`kB`(L67)·`np`(L62) 기존 상수·import 재사용. `sig(1−sig)` = `x_MIT` 에서 최대 ¼(L1089).

**신규 클래스 시그니처**(합성):
```
class LCOCathodeDQDV:
    """LCO 양극 dQ/dV — 흑연 GraphiteAnodeDischargeDQDV 를 내부 위임(MSMR 동형, L1747).
    흑연 경로 무변경. 차이 = (i) LCO_STAGING_LIT (ii) T1 전자항 plug-in(ΔS 슬롯)."""
    def __init__(self, transitions=LCO_STAGING_LIT, gate=LCO_MIT_GATE, **graphite_kwargs):
        # transitions 를 사본화 후 electronic=True 전이의 dS_rxn 조립은 dqdv 시점(T·V 의존)에.
        self._graphite = GraphiteAnodeDischargeDQDV(transitions, **graphite_kwargs)
        self.gate = gate
    def dqdv(self, V_app, T, I_abs, Q_cell, s=+1):
        # 전자항 T·x 의존 → 전이 dict 의 dS_rxn 을 이 호출의 (T, ξ_eq,1(V)) 로 조립 후 위임
        ...
    def curve(self, V_app, direction='discharge', c_rate=0.0, Q_cell=1.0, T=298.15, I_abs=None):
        ...  # 흑연 facade 와 동일 규약, 내부 self.dqdv 재사용
```

### 1.5 ★전자항 좌표 매핑 (x ↔ ξ_eq,1(V)) — 설계 핵심 [확정 근거 + 미검증]

**문제** [확정, Ch1 L1724–1728]: 전자항 `ΔS_e(x,T)` 는 **조성 x** 함수인데(게이트 인자 `z=(x−x_MIT)/Δx_MIT`), 코드 `dqdv` 는 **전압 격자** 위에서 돈다.

**Ch1 지정 해법** [확정, L1727–1728]: `x ↔ ξ_eq,1(V)` 매핑으로 좌표를 잇는다 — T1 전이의 진행률 `ξ_eq,1(V)` 이 그 전이 구간의 정규화 조성에 대응하므로, 게이트 인자에 `x = x(ξ_eq,1(V))` 를 대입해 V 격자 위에서 `ΔS_e` 를 평가.

**설계 구현** [추정, 근거 = L1727]:
- T1 전이의 `ξ_eq,1(V,T)` 는 `func_ksi_eq(T, V, center_1, n_1, σ_d)`(L94)로 이미 산출 가능(흑연 인스턴스 재사용).
- **정규화 조성 매핑**: T1 구간 `x∈[0.75, 0.94]`(L330). ξ_eq,1: 0→1(진행률). x 는 탈리튬화로 감소하므로 `x(ξ) = x_hi − ξ·(x_hi − x_lo)` = `0.94 − ξ·0.19` [추정, 선형 매핑; 정밀 매핑은 피팅 대상].
- 이 `x(ξ_eq,1(V))` 를 `func_dS_e_molar(x, T, ...)` 에 넣어 **V 격자 위 배열** `ΔS_e(V)` 산출.
- T1 전이의 `dS_rxn` = `ΔS_0^config(중심 표준값) + ΔS_e(V,T)`(`eq:lco-decomp` L1690) 로 조립 후 `func_U_j(T, dH_rxn, dS_rxn_array)` 에 배열로 전달(L434 이미 배열 T 대응 → 배열 dS_rxn 도 broadcast 가능 [미검증: func_U_j L79 `(−dH + T·dS)/F` 는 dS 배열이면 자동 broadcast, 확인 필요]).

> **★이중계산 직교 (여기서 결정적)** [확정, Ch1 `eq:lco-decomp` L1699·Ch2 파생 B L294]: T1 의 `dS_rxn` config 자리에는 **봉우리 중심 표준값 `ΔS_0` 만** 넣는다 — 봉우리 내부 조성 의존 `R·ln[(1−ξ)/ξ]` 는 logistic(폭 w)이 **이미 담고 있어** 재가산 금지(L1700, Ch2 L299·L535). 전자항 `ΔS_e` 는 config 와 **다른 자유도**(전자 밴드 점유)라 직교 가산(L1702–1710) — config 중심값 + 전자 게이트 골, 각 항이 자기 자유도 몫만. → §2.3 에서 q_rev 조립 시 동일 규율 재확인.

---

## §2. 가역 발열 q_rev 설계

### 2.1 채택 구조: **신규 메서드 `q_rev()`(흑연·LCO 클래스 공통 mixin 또는 각 클래스 메서드)** [추정]

Ch2 `eq:qrev`(L645): `q_rev = −IT·∂U_oc/∂T = −(IT/F)ΔS(x)`. 이는 **dQ/dV 곡선과 독립 산출물**(발열 곡선)이라, dqdv 경로를 건드리지 않는 **신규 메서드**로 추가한다(0-diff 자동). 흑연·LCO 공통 물리이므로 **모듈 순수 함수 + 각 클래스 얇은 wrapper** 로 둔다(중복 회피, DRY).

### 2.2 시그니처 + T 한 번 원칙 [설계 제안, 확정 근거]

**Ch2 use-this 종합식**(L672–674, `∂U_oc/∂T` 완전식):
```
∂U_oc/∂T (x) = [ Σ_j Q_j·g_j(x)·( ΔS_0_j/F + (R/F)·ln(ξ_j/(1−ξ_j)) ) ] / [ Σ_j Q_j·g_j(x) ],
   g_j = ξ_j(1−ξ_j)/w_j
```
`q_rev = −IT·∂U_oc/∂T`.

**신규 순수 함수**:
```
def func_dUoc_dT(xi_list, Q_list, w_list, dS0_list):
    """겹침 가중 ∂U_oc/∂T [V/K] — Ch2 use-this 완전식(L672).
    g_j = ξ_j(1−ξ_j)/w_j (=eq:gj L454). 중심 ΔS0/F + 분포 config (R/F)ln(ξ/(1−ξ)).
    ★분포 config 항은 여기서 명시 가산 — dS0 에는 넣지 않음(이중계산 금지, 파생 B L535)."""
    num = 0.0; den = 0.0
    for xi, Q, w, dS0 in zip(xi_list, Q_list, w_list, dS0_list):
        g = xi*(1.0-xi)/w
        # config 분포항: overflow 안전 위해 z_j = (V−U_j)/w_j 직접 쓰면 = ln(ξ/(1−ξ)) (eq:dxidT L459)
        config = (R/F)*np.log(xi/(1.0-xi))
        num += Q*g*(dS0/F + config); den += Q*g
    return num/den   # den>0 가드 필요(전 전이 g=0 이면 0/0)

def func_q_rev(I_signed, T, dUoc_dT):
    """가역 발열 q_rev [W] — eq:qrev(L645). q_rev = −I·T·∂U_oc/∂T.
    ★T 한 번(−I·T·∂U/∂T; −(IT/F)ΔS 로 전개해도 T 는 한 번). I 부호 = 방전 +/충전 −."""
    return -I_signed * T * dUoc_dT
```
> **★T 한 번 원칙** [확정, `eq:qrev` L645]: `q_rev = −IT·∂U/∂T`. `∂U/∂T = ΔS/F` 를 대입하면 `−(IT/F)ΔS` — T 는 여전히 **한 번**만. 전자항이 `ΔS_e ∝ T`(L1042)라도 그 T 는 ΔS 내부의 물리적 T-의존이고, q_rev 앞의 T 와 **별개 자리**다(곱셈 중복 아님). 코드에서 `func_q_rev` 는 `dUoc_dT` 를 받아 `−I·T·(그 값)` 만 하므로 T 이중곱 원천 차단.

**부호 규약** [확정, `srcbox` L651]: `ΔS = +F·∂U_oc/∂T` 로 통일. 방전(I>0): ΔS>0 → q_rev<0(흡열), ΔS<0 → q_rev>0(발열)(L658–660). 전셀 음극 몫 부호 반전은 범위 밖(하프셀 단독, `warnbox` Ch2 L102–107).

### 2.3 ΔS(x) 조립 — 중심 ΔS⁰_j + config 분포항 + dS_e [확정]

`ΔS(x) = ΔS_0_j(중심) + R·ln[ξ/(1−ξ)](분포 config) + δS_{vib/e}(x)(전이 폭 내 급변 시만)` (Ch2 `keybox` L414–418).

| 성분 | 코드 자리 | 이중계산 처리 | 근거 |
|---|---|---|---|
| **중심 ΔS_0_j** | 전이 dict `dS_rxn`(중심 표준값만) | config 재가산 X | 파생 B L297·L535 [확정] |
| **분포 config `R·ln[ξ/(1−ξ)]`** | `func_dUoc_dT` 내 명시 항 (dS0 밖) | logistic w 가 담은 것을 **q_rev 산출식에서만** 명시 (dqdv 의 dS0 슬롯엔 절대 X) | `eq:dSconfig`(L227)·L299 [확정] |
| **전자 dS_e(x,T)** | T1: `func_dS_e_molar`(§1.4) → dS0 에 **가산**(config 와 직교) | config 중심값과 다른 자유도라 직교 가산(잔차 0) | `eq:lco-decomp` L1702–1710 [확정] |

> **★이중계산 직교 분리 방법(코드 명시)** [확정]:
> 1. **dqdv 경로**(§1): 전이 `dS_rxn` = 중심 ΔS_0 (+ LCO T1 전자항). config 분포항은 **넣지 않음** — `func_ksi_eq` 의 폭 w(=RT/F, `func_w` L74)가 이미 담음(Ch2 L242–244 "w=RT/F 가 부분몰 config 를 담고 있었다").
> 2. **q_rev 경로**(§2): `func_dUoc_dT` 가 config 분포항 `R·ln[ξ/(1−ξ)]` 를 **명시 가산**(중심 ΔS_0 밖에서). 이는 dqdv 의 w 가 담은 것과 **다른 산출**(q_rev 는 ∂U/∂T 직접 평가라 분포항이 명시적으로 필요). 두 경로가 같은 물리를 두 번 세지 않음 — dqdv 는 곡선 모양에, q_rev 는 발열에.
> 3. **전자항**: config·vib 중심값은 ΔS_0 에 흡수, MIT 급변만 `func_dS_e_molar` 로 분리(Ch2 L307·L407). config 슬롯에 전자항 재가산 절대 금지(직교 = 가산 가능, 이중계산 금지 = 중심/골 분리; L1710).

### 2.4 비가역 항 옵션 [추정 + 근거 미발견 병기]

base 프롬프트는 "비가역 3분해 옵션(I²R + Iη_ct + Iη_diff)"을 언급하나, **Ch2 tex 는 비가역열을 단일 lumped 항 `I(U_oc−V)`(`eq:qrev` L643, `Q̇_irr≥0`)로만 제시**한다 [확정, grep 결과 L643 유일]. 명시적 3-way η 분해(charge-transfer η_ct / diffusion η_diff)는 **Ch2 본문에 없음** [근거 미발견].

**설계 판단** [추정]:
- **채택**: lumped `q_irr = I·(U_oc − V) = I·(σ_d·|I|·R_n + 동역학 과전압)` — 코드의 기존 분극 `Rn`(L408, `V_n=V_app−σ_d|I|Rn`)과 꼬리 `L_V`(L459)가 이미 IR·과전압 소산을 담으므로, `q_irr` 은 **기존 machinery 재사용**으로 산출 가능(신규 물리 0).
- **3-way 분해는 옵션/후속**: I²R(=|I|²Rn) 은 코드 Rn 에서 직접, 나머지 η_ct/η_diff 는 Ch2 에 닫힌식 없음 → **구현 안 함**(허위 정밀 금지). 신규 함수 `func_q_irr(I, U_oc, V)` 얇은 lumped 형만 제공, 3분해는 docstring 에 "Ch2 미제공, 후속" 명기.
> [미검증] `U_oc`(평형)와 `V`(단자)의 코드 내 산출 = `V_n`(내부)과 `V_app`(측정) 차로 근사 가능하나, Ch2 의 `U_oc−V` 정의와 정확 대응하는지는 실편입 후 확인 대상.

---

## §3. ★흑연 회귀 0-diff 가드

### 3.1 구조 (합성 → 무섭동) [확정 근거]

§1.1 합성 채택으로 **기존 `GraphiteAnodeDischargeDQDV`(L192–524)·`GRAPHITE_STAGING_LIT`(L531)·모듈 순수 함수(L74–188) 전부 심볼 단위 0-touch**. LCO·q_rev 는 전부 **신규 심볼**(insert_after_symbol). 따라서 흑연 경로는 **코드 위상으로** 무섭동 — 테스트 이전에 구조로 보장.

**유일 주의점** [미검증]: `func_dS_e_molar`·`LCOCathodeDQDV`·`func_q_rev` 등 신규 심볼을 흑연 함수 **뒤**에 삽입할 것(orphan 0, 앞 도입·뒤 사용). 기존 `if __name__=="__main__"` self-test(L567–703)는 무변경, 신규 self-test 는 그 뒤에 append.

### 3.2 회귀 하네스 설계 (기존 curve() 출력 byte 일치) [설계 제안]

**목적**: 확장 전후 흑연 `curve()`/`dqdv()`/`equilibrium()` 출력이 **정확히 동일**함을 증명.

**하네스 A — 신규 self-test 블록**(기존 self-test 뒤 append, 기존 무변경):
```
# ---- GRAPHITE REGRESSION 0-diff GUARD (P4 확장 후) ----
V = np.linspace(0.03, 0.34, 1000)
m = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
# 확장 전 golden 값을 코드에 하드코딩(또는 .npy) 후 대조:
for s, I in [(+1,0.02),(+1,0.2),(+1,1.0),(-1,0.2)]:
    y = m.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s)
    assert np.array_equal(y, GOLDEN[(s,I)])   # ★byte 일치 (allclose 아님, exact)
yeq = m.equilibrium(V, T=298.15); assert np.array_equal(yeq, GOLDEN_EQ)
```
> **golden 확보 절차** [설계]: 실편입 **직전**(확장 코드 삽입 전) 원본으로 `dqdv`/`equilibrium` 출력을 `.npy` 저장 → 확장 후 `np.array_equal`(bit 단위)로 대조. `allclose`(tol 허용) 아니라 **exact array_equal** — 신규 심볼이 흑연 경로에 손대지 않았으면 부동소수점까지 동일해야 함.

**하네스 B — 면적보존 회귀**(P1 §4 보완4 = self-test 면적 assert 부재 지적 [확정]):
- P1 이 "면적=Q assert 부재"(L57·§4-4)를 결함으로 지적. **P4 에서 신규 추가**(코드 개정 후보로 P1 이 명시):
```
for tr in GRAPHITE_STAGING_LIT:
    m1 = GraphiteAnodeDischargeDQDV([tr], Cbg=0.0)
    yeq = m1.equilibrium(V, T=298.15)
    area = np.trapz(yeq, V)
    assert abs(area - tr['Q']) < 1e-3   # ∫Q·ξ(1−ξ)/w dV = Q (P1 §0 = 1.000000)
```
> [확정, P1 §0 L93] 독립 면적적분 = 1.000000. 이 assert 는 흑연 회귀 + 면적보존 이중 가드. (base 프롬프트 3 "면적보존 DC=1 유지" 정합.)

**하네스 C — LCO/q_rev 신규 경로 sanity**(회귀 아니라 신규 검증):
- LCO dqdv 유한성·3-peak 위치(§5), q_rev 부호 교대(ΔS 부호 따라 흡/발열, L661).

---

## §4. Serena 편입 레시피

### 4.1 심볼별 작업 (insert_after / 무변경) [설계]

| 순서 | Serena 작업 | 대상 | 내용 | replace 여부 |
|---|---|---|---|---|
| 1 | `insert_after_symbol` | `func_chi_d`(L163) 뒤 | `func_dS_e_molar` | 신규(0 replace) |
| 2 | `insert_after_symbol` | (1) 뒤 | `func_dUoc_dT`·`func_q_rev`·`func_q_irr` | 신규 |
| 3 | `insert_after_symbol` | `_finite_nonneg`(L188) 뒤 or 클래스 뒤 | 상수 `LCO_MIT_GATE`·`E_V` | 신규 |
| 4 | `insert_after_symbol` | `GraphiteAnodeDischargeDQDV`(L524) 뒤 | `class LCOCathodeDQDV` | 신규 |
| 5 | `insert_after_symbol` | `GRAPHITE_STAGING_LIT`(L560) 뒤 | `LCO_STAGING_LIT` | 신규 |
| 6 | `insert_after_symbol` | self-test 끝(L703) 앞 or 뒤 | 회귀 하네스 A/B/C | 신규(기존 self-test 무변경) |
| — | **무변경** | L74–188·L192–524·L531–560·L567–703 | 흑연 전 심볼 | 0-touch |

**replace_symbol_body 필요 심볼** [설계]: **0건 목표**. 예외 가능성 [미검증]:
- `func_U_j`(L79)가 `dS_rxn` 배열을 broadcast 하는지 확인 필요(§1.5). broadcast 되면 replace 0. 안 되면 **신규 wrapper 함수**로 우회(기존 `func_U_j` 무변경, LCO 클래스가 배열 dS 를 자체 처리) — **원형 보존 우선, replace 회피**.

### 4.2 코드 소유권 규율 [확정, 준수 사항]
- **식별자·대소문자·정수코드 보존**: 기존 심볼명·시그니처 1바이트 무변경. 신규 심볼만 추가.
- **지정 범위 외 임의수정 X**: P1 이 보고만 한 결함(死코드 `func_U_j_hys` L82–91, z_cut docstring 부정확 L217)은 **P4 개정 후보이나 본 드래프트 범위 밖 처리** — 死코드 `func_U_j_hys` 는 **P1 판정(보존) 따름**(base 프롬프트 품질 항). z_cut docstring 은 별도 결정(이 확장과 무관, 건드리지 않음).
- **원형 불가침(L34–36)**: `func_w`·`func_U_j`·`func_U_j_hys`·`func_ksi_eq`·`func_L_q`·`_causal_lowpass`·`GRAPHITE_STAGING_LIT` 동결 유지.

---

## §5. 그래프 검증 계획

### 5.1 흑연 (회귀 = 무변화 확인) [설계]
- 확장 전후 `plot_dqdv.py`(헤더 L11 참조) 출력 **완전 동일**(§3.2 하네스 A 의 시각 확인). 4-전이 peak @V≈0.085/0.120/0.140/0.210 위치·높이 불변.

### 5.2 LCO dQ/dV (신규 개형) [설계, 확정 근거]
- **3-peak 확인** [확정, Ch1 `sec:lco-peak` L1203]: T1 ~3.90 V(MIT plateau, 넓은 종), T2 ~4.05 V·T3 ~4.17 V(한 쌍 좁은 order-disorder 봉우리). V 격자 = `np.linspace(3.7, 4.3, N)`.
- **전자항 발현 확인**: T1 peak 에서 `ΔS_e` 게이트 ON 이 위치·T-의존에 미치는 효과 — 다온도(258/298/318 K)에서 T1 위치 이동이 **∝T²**(`eq:U1T2` L1055) 곡률을 보이는지(config·vib 는 선형). 이것이 전자항 식별 신호(L1060).
- **부호 검산**: 양극 영역 dQ/dV>0(면적=Q), 유한성(`np.all(np.isfinite)`).

### 5.3 가역 발열 q_rev (신규 곡선) [설계, 확정 근거]
- **흑연 q_rev(x)** [확정, Ch2 L661–664]: 저-x 흡열(ΔS>0, 방전 q_rev<0) → 고-x 발열(ΔS<0), stage 2→1(x≈0.5) 큰 음의 ΔS 에서 방전 발열 두드러진 신호. x-축 q_rev 곡선이 부호 교대 재현하는지.
- **수치 검증 앵커** [확정, Ch2 파생 A `srcbox` L484–489]: 유한차분 `∂U_oc/∂T|_x^FD = [U_oc(x,T2)−U_oc(x,T1)]/ΔT`(T1=292.15, T2=298.15 K)와 `func_dUoc_dT` 완전식 대조 — 175 점 전 범위 절대오차 ≈0(부동소수점 정밀도)이어야 함(완전식 = FD 일치). **이 FD 대조가 q_rev 회귀 하네스의 정량 gate**.
- **LCO q_rev**: T1 전자항 `∝T` 가 q_rev 에 들어가 다온도 거동 차이 확인(config·vib 대비).

---

## 5줄 요약

1. **채택 구조**: **합성(신규 `LCOCathodeDQDV` 가 흑연 `GraphiteAnodeDischargeDQDV` 를 내부 위임)** — 기존 흑연 심볼(L74–524·L531) **0-touch**, MSMR 동형(Ch1 L1747 "구조 변경 0")이 물리로 보증. LCO = 데이터셋 `LCO_STAGING_LIT`(3-전이) + 전자항 plug-in 둘뿐.
2. **핵심 시그니처**: `func_dS_e_molar(x,T,g_max,x_MIT,dx_MIT)`(MIT 게이트 몰당 전자 엔트로피, `eq:dSegate` L1083, **eq:gunit 나눗셈 형** L1032) · `func_dUoc_dT(...)` + `func_q_rev(I,T,dUoc_dT)`(`eq:qrev` L645) · 전자항 좌표는 `x=x(ξ_eq,1(V))` 매핑(Ch1 L1727).
3. **회귀 가드**: 합성으로 흑연 경로 **코드 위상 무섭동** + 신규 self-test 하네스 A(`np.array_equal` byte 일치, allclose 아님) + B(면적=Q assert, P1 §4 결함 해소) + q_rev 는 FD 175점 절대오차≈0 정량 gate(Ch2 `srcbox` L484).
4. **이중계산 처리**: dqdv 경로 = 전이 `dS_rxn` 에 **중심 ΔS_0 만**(config 분포항 `R·ln[ξ/(1−ξ)]` 는 폭 w 가 이미 담음, 재가산 금지 — 파생 B L535); q_rev 경로 = `func_dUoc_dT` 가 config 분포항 **명시 가산**(다른 산출); 전자항은 config 와 **직교 가산**(중심/골 분리, L1710). q_rev 의 T 는 `−IT·∂U/∂T` **한 번**(전자항 ΔS∝T 와 별개 자리).
5. **리스크**: (a) `func_U_j`(L79)의 `dS_rxn` 배열 broadcast 미확인 → 안 되면 신규 wrapper 로 우회(replace 0 유지) [미검증]. (b) 비가역 3분해(I²R+Iη_ct+Iη_diff)는 **Ch2 미제공**(lumped `I(U_oc−V)` L643 만) → lumped 형만 구현, 3분해는 후속 명기(허위 정밀 금지) [근거 미발견]. (c) x↔ξ 선형 매핑은 초기값(정밀 매핑 피팅 대상) [추정]. 死코드 `func_U_j_hys` 는 P1 판정(보존) 따름.
