# V1.0.10 P4 코드개정 설계 드래프트 — O3

> **역할**: Anode_Fit v1.0.10 P4 코드개정(LCO 양극 + 발열) 9종 경쟁 **설계 드래프트 O3**.
> **성격**: ★설계 제안만 — `.py`/문건/코드 **수정 절대 X**(단일 `.py`는 공유 가변상태, 실편입은 master가 Serena로 1회 수행). 독립 작성(타 드래프트·통합 미관여). 허위 attribution 없음.
> **근거 규율**: 모든 물리식·구조 판단은 코드 줄(`Anode_Fit_v1.0.10.py`)·Ch1(`graphite_ica_ch1_v1.0.10.tex`)·Ch2(`graphite_ica_ch2_v1.0.10.tex`)·P1 audit(`V1010_P1_code-audit_RESULT.md`)의 **직접 줄 근거**로 못박는다. 추정은 `[추정]`, 근거 미발견은 `[근거 미발견]` 표기.
> **정독 커버리지**: 코드 703줄 전문 / P1 446줄 전문 / Ch1 §서론~§부호검산(L1~1875, 전영역) / Ch2 §서~맺음+bib(L1~751, 전영역). head→tail 전 구간.

---

## §0. 설계 전 사전 정합 검산 (추측 배제)

본격 설계 전, 세 문건이 요구하는 물리와 현재 코드의 실제 심볼을 대조해 "확장이 무엇을 바꾸고 무엇을 보존하는가"를 확정한다.

| 항목 | 문건 요구 (줄) | 현재 코드 실제 (줄) | 판정 |
|---|---|---|---|
| LCO logistic 동형 | MSMR `x_j=X_j/(1+e^{f(U−U_j⁰)/ω_j})` (Ch1 eq:msmr L1738-41) ↔ `ξ_eq=1/(1+e^{−σ_d(V−U^d)/w_j})` (eq:xieq L770) | `func_ksi_eq` (L94-97): `z=s(V_n−U)/func_w(T,n)`, `logistic(z)` | **[확정] 구조 동형** — `X_j↔Q_j`·`U_j⁰↔U_j^d`·`ω_j↔w_j`·`f↔−σ_d`(Ch1 L1743-46). 코드 **구조 변경 0**으로 LCO 성립 |
| LCO 평형중심 | `U_j(T)=(−ΔH_rxn+TΔS_rxn)/F`, 전극 불문 (Ch1 eq:Uj L448, eq:lco-center L465-70) | `func_U_j(T,dH_rxn,dS_rxn)` (L78-79): `(−dH_rxn+T*dS_rxn)/F` | **[확정]** 전극 가정 없음. LCO는 `(dH_rxn,dS_rxn)` 값만 교체 |
| 전자엔트로피 항 | `ΔS_e^mol=N_A·(π²/3)k_B²·T·∂g/∂x <0` (삽입 기준, 몰당; Ch1 eq:dSemolar L1018, eq:dSegate L1082) | **부재** — `grep dS_e|electronic|MIT`→No match (P1 §2-E L353-356) | **[확정] 신규 추가 필요**. 흑연=0, LCO T1만 켜짐 |
| 가역 발열 q_rev | `q_rev=−IT·∂U/∂T=−(IT/F)ΔS(x)` (Ch2 eq:qrev L645, T 한 번) | **부재** — T는 외생 입력, 열항 없음 (P1 §2-E L354) | **[확정] 신규 추가 필요** |
| 이중계산 직교 | config 슬롯 = 봉우리 중심 표준값 `ΔS⁰_j`만; 봉우리 내부 `R ln[ξ/(1−ξ)]`는 logistic w가 자동 생성 (Ch2 warnbox 파생B L293-309·L524-537) | `func_U_j`가 `dS_rxn`을 U_j(T) 통해 한 덩이로 사용. w의 T의존이 봉우리 내부 config 자동 반영 (Ch2 eq:dVdT_config L232-244) | **[확정]** config 항 재가산 금지 = 코드에서 `dS_rxn`에 중심 표준값만 넣고 config 부분몰은 코드가 이미 담음 |
| 좌표 매핑 | `ΔS_e`는 조성 x함수, `dqdv`는 V격자 → `x↔ξ_eq,1(V)` (Ch1 L1724-29 예고 (i)) | `dqdv`는 V_work 격자 위 전이 루프 (L431-477) | **[확정]** T1 전이 진행률 `ξ_eq,1(V)`로 x 좌표 연결 |

→ §0 핵심: **① LCO는 파라미터 교체 + 전자항 1개 plug-in만(MSMR 동형, 구조 변경 0)** ② 발열은 `dqdv` 밖 별도 산출(∂U/∂T가 있어야 하므로 논리적으로 dqdv와 분리) ③ 이중계산 직교는 **"config 부분몰을 코드에 손대지 말고 그대로 두는 것"**이 정답(logistic w가 이미 담음).

---

## §1. LCO 양극 dQ/dV 설계

### 1-1. 채택 구조 — 일반화 base (신규 클래스 아님) + 얇은 LCO subclass

**결정: 기존 `GraphiteAnodeDischargeDQDV`를 무변경 base로 두고, LCO는 (a) 데이터셋 상수 `LCO_STAGING_LIT` 추가 + (b) T1 전자항 plug-in을 담는 최소 subclass `LCOCathodeDQDV`로 둔다.**

근거 3가지:
1. **MSMR 동형(Ch1 sec:lco-code L1735-60)이 "구조 변경 0"을 명시**한다 — `func_ksi_eq`·`func_U_j`·합산(eq:sum)은 전극 불문. 신규 병렬 클래스로 곡선식을 재작성하면 흑연 회귀 0-diff 보장이 어려워지고(코드 이중화), MSMR 동형 논지와도 어긋난다.
2. **바뀌는 것은 단 둘**(Ch1 L1748-57): ① 전이 파라미터 교체(dict 값) ② T1의 `ΔS_rxn` 평가에 전자항 몰당 식 1줄 더하기. ①은 데이터셋 상수로, ②는 subclass 훅 하나로 흡수된다.
3. **흑연 base 경로 무섭동**(§3 회귀 가드)이 가장 쉬운 구조 = base는 1바이트도 안 건드리고, 전자항만 subclass override 지점에 격리.

> **[대안 기각] 일반화 base 안에 `electronic=True` 플래그를 심는 방식**: base 시그니처·본체를 건드려 흑연 회귀 byte-diff가 발생(§3 위반). 기각. 전자항은 **subclass 훅**으로만 진입.

### 1-2. MSMR 동형 매핑표 (코드 심볼 ↔ Ch1 식)

Ch1 eq:msmr(L1738) `x_j=X_j/(1+exp[f(U−U_j⁰)/ω_j])` ↔ eq:xieq(L770) `ξ_eq,j=1/(1+exp[−σ_d(V−U_j^d)/w_j])`.

| MSMR 기호 | Ch1 코드 대응 | 코드 심볼 (줄) | 부호·의미 |
|---|---|---|---|
| `X_j` (용량 가중) | `Q_j` | `tr['Q']` (L366, L477) | 면적/높이 가중. LCO 3전이 |
| `U_j⁰` (중심) | `U_j^d` (분기중심) | `func_U_j`+`func_U_branch`→`center` (L433-450) | 양극 3.9~4.2 V. `dH_rxn`의 큰 음값이 `−ΔH_rxn` 크게 양→높은 중심 (Ch1 L467-70) |
| `ω_j` (폭) | `w_j=n_jRT/F` | `func_w`/`_width` (L74-75, L281-284) | LCO 3전이 모두 Ω>2RT 두-상 → 폭=현상학적 피팅 (Ch1 L1204-06) |
| `f` (방향 인자 ±1) | `−σ_d` | `s`/`sigma_d` (L94, L388) | **★부호 대응: f=−σ_d** (Ch1 L1744-46). MSMR 지수 `+f(U−U_j⁰)` vs Ch1 지수 `−σ_d(V−U_j^d)` 같은 자리 → `f=−σ_d` |

**결론**: MSMR 동형이 완전하므로 `func_ksi_eq`·`func_U_j`·`func_w`·`equilibrium`·`dqdv` 곡선 골격은 LCO에 **무변경 재사용**. 이것이 "같은 코드가 LCO를 그린다"(Ch1 L1735)의 코드 측 근거.

### 1-3. 양극 부호 규약 (흑연과 1:1 대칭)

- **방전(σ_d=+1) = LCO 리튬화**(Li⁺→LCO, Co⁴⁺→Co³⁺ 환원, x↑, 전위 하강) / **충전(σ_d=−1) = 탈리튬화**(x↓, 전위 상승) (Ch1 L303-08).
- **∂U_j/∂T = ΔS_rxn^cat/F** — 부호까지 흑연과 동일 관계식, 값만 전이별 `ΔS_rxn,j^cat`가 정함 (Ch1 eq:lco-dUdT L474). 코드 `func_U_j`의 `+T*dS_rxn`이 이미 이 관계 담음.
- **LCO 전이표는 충전(탈리튬화) 진행 = ξ:0→1 주 방향**을 전위 오름차순으로 적음 (Ch1 L308-09).
- **부호 코드 무손상**: `func_ksi_eq`의 `s`(=σ_d)가 방향을 담으므로, LCO도 dqdv 호출 시 `s=+1/−1`로 방·충 지정. base 부호 로직 변경 0.

### 1-4. MIT g(E_F) 급변 electronic 항 x-의존

Ch1 sec:lco-electronic(L928-1160)의 전자 엔트로피는 **T1(MIT) 전이에만** 켜지는 x-의존 항:

- **게이트 함수** (Ch1 eq:ggate L1069): `g(E_F,x) ≈ g_max·[1 − σ((x−x_MIT)/Δx_MIT)]`, 초기값 `g_max=13 e/eV·x_MIT≈0.85·Δx_MIT≈0.05`. 세 값이 피팅 대상.
- **전자 부분몰 엔트로피 몰당 닫힌식** (Ch1 eq:dSegate L1082 + 몰당 환산 eq:dSemolar L1018 + eV→J eq:gunit L1027):
  ```
  ΔS_e,j^mol(x,T) = −(π²/3)·R·(k_B·T/e_V)·(g_max/Δx_MIT)·σ(z)·[1−σ(z)]  < 0   (삽입 기준)
      z = (x − x_MIT)/Δx_MIT,   e_V = 1.602176634e−19 J/eV
  ```
  - **★단위 3중 주의**(Ch1 L1013-33·L1752-56): (i) 자리당 k_B² → 몰당 `N_A k_B² = R k_B` (N_A 누락 시 ~10²³배 과소). (ii) g가 e/eV → J로 **나눗셈**(`g_J = g_eV/e_V`), **곱하면 ~4×10³⁷배 어긋남**. (iii) 결과 부호는 환산 불변(N_A>0, e_V>0).
- **부호**(Ch1 L1034-42): 삽입(x↑)으로 금속→절연체라 g(E_F) 감소 → ∂g/∂x<0 → ΔS_e<0(음의 골), 절댓값 봉우리는 탈리튬화 방출량. `ΔS_rxn` 슬롯(흑연 2→1 삽입 −16 J/mol/K)과 **부호 일관**(삽입 기준, 부호 뒤집기 없음).
- **T 의존**(Ch1 L1042-46): `ΔS_e∝T` → ∂U_1/∂T의 **기울기 자체가 T에 선형**, U_1 이동은 ∝T²(선형 아님). 식별 신호 = "∂U/∂T가 T에 선형"이지 "peak 위치가 T에 선형"이 아님. Ch2 발열로 확장 시 중요.

### 1-5. 함수 시그니처·필요 상수 (설계 제안)

**신규 모듈 함수 (base 밖, 순수 함수 — 흑연 경로 불침투):**

```python
def func_g_EF_gate(x, g_max=13.0, x_MIT=0.85, dx_MIT=0.05):
    """MIT-logistic 게이트 g(E_F,x) (Ch1 eq:ggate). 단위 e/eV/atom.
    z=(x−x_MIT)/dx_MIT; return g_max*(1 − logistic(z))."""

def func_dSe_molar(x, T, g_max=13.0, x_MIT=0.85, dx_MIT=0.05,
                   e_V=1.602176634e-19):
    """전자 부분몰 엔트로피 몰당 닫힌식 ΔS_e^mol [J/mol/K] (Ch1 eq:dSegate·dSemolar·gunit).
    z=(x−x_MIT)/dx_MIT; s=logistic(z);
    return −(pi^2/3)*R*(kB*T/e_V)*(g_max/dx_MIT)*s*(1−s).   # <0 삽입 기준
    ★eV→J는 e_V로 나눗셈(kB*T/e_V), N_A는 R이 이미 흡수(R=N_A·kB)."""
```
- `func_g_EF_gate`의 logistic은 **기존 `func_ksi_eq`의 overflow-safe 분기 형태를 재사용**(별도 로컬 logistic 헬퍼 또는 `1/(1+exp(−z))` 안전형). 새 수치 관례 도입 X.
- 필요 상수: `import math` 없이 `np.pi` 사용 가능(코드는 numpy 상주). `R`(L65)·`kB`(L67) 기존 전역 재사용. `e_V`는 함수 기본 인자로만(전역 오염 회피).

**신규 데이터셋 상수 `LCO_STAGING_LIT` (원형 보존 라벨, GRAPHITE_STAGING_LIT과 동격 배치):**

Ch1 tab:lco-staging(L319-337) 3전이 초기값:

| 전이 | U_j [V] | x 범위 | 성격 | ΔS_rxn^cat 초기값 | 전자항 |
|---|---|---|---|---|---|
| T1 (MIT) | ~3.90 | 0.94–0.75 | insulator→metal | config + ΔS_e 게이트 ON | **발현(핵심)** |
| T2 (order-disorder a) | ~4.05 | ≈0.55 | hex→monoclinic | config 주도 (≈0.47 J/K/mol) | off |
| T3 (order-disorder b) | ~4.17–4.20 | ≈0.48 | monoclinic→hex | config (≈1.49 J/K/mol) | off |

- dict 키 구조 = `GRAPHITE_STAGING_LIT`과 **동일**(`U|dH_rxn/dS_rxn·w|n·Q·Omega·gamma·dH_a·dS_a·dVdq_qa`). 값만 양극 영역.
- T1에 전자항 활성 마커(예 `'electronic': True`, `'x_range':(0.75,0.94)`) 키 **추가**만(다른 전이엔 없음 → off).
- **★출처 라벨(허위 정밀 금지)**: config 중심 표준값(Motohashi ≈0.47/1.49, Ch1 L688-689)·게이트 3값은 **초기값(round-trip 미실증)**. GRAPHITE_STAGING_LIT과 동격으로 피팅 override 전제(Ch1 L1729-33).

### 1-6. 좌표 매핑 (x ↔ ξ_eq,1(V)) — 전자항을 V격자에서 평가

Ch1 L1724-29: 전자항은 조성 x 함수인데 dqdv는 V 격자 위에서 돈다. **T1 진행률 `ξ_eq,1(V)`이 그 전이 구간 정규화 조성에 대응**하므로, 게이트 인자에 `x = x(ξ_eq,1(V))`를 대입해 V 격자 위에서 ΔS_e 평가.

**설계 (subclass 훅):**
```
LCOCathodeDQDV.dqdv 전이 루프에서, tr['electronic']==True 인 전이 j(=T1)에 대해:
  1) 그 전이의 ξ_eq,1(V_work) 계산 (base가 이미 L455에서 계산 — 재사용)
  2) x_local = x_range[0] + ξ_eq,1·(x_range[1]−x_range[0])   # ξ→x 선형 매핑
  3) dSe = func_dSe_molar(x_local, T_work, g_max, x_MIT, dx_MIT)
  4) U_j 평가 시 dS_rxn_eff = dS_rxn(중심 표준값) + dSe   # 전자항 가산 (몰당)
  5) 이 U_j로만 center·ksi_eq 재평가 (T1 전용, 다른 전이 무영향)
```
- **[추정] ξ↔x 선형 매핑**: Ch1이 "T1 전이 진행률이 정규화 조성에 대응"(L1727)이라 명시하나 정확한 함수형(선형 vs logit 역)은 문건에 없음 → 선형이 최소가정. round-trip 피팅으로 조정 가능하게 인자 노출. `[추정]`
- **이중계산 직교 준수**(§1-7): 여기서 dS_rxn에 더하는 것은 **전자항(elec 슬롯)만**. config 부분몰은 base의 logistic w가 이미 담으므로 재가산 X.

### 1-7. ★이중계산 직교 — LCO config·elec 분리 (코드에서)

Ch2 warnbox 파생B(L293-309)·Ch1 L1699-1710:

```
ΔS(x) = ΔS⁰_j (중심 표준값) + R·ln[ξ/(1−ξ)] (분포 config, w가 자동 생성) + δS_vib/e(x) (급변 시만)
```

- **config 중심 표준값 `ΔS⁰_j`만** dict의 `dS_rxn`에 넣는다(봉우리 중심 ξ=1/2에서 config=0, Ch2 L306).
- **봉우리 내부 config `R ln[ξ/(1−ξ)]`는 코드에 손대지 않는다** — logistic w의 T의존이 이미 `∂U_oc/∂T`에 이 항을 자동 생성(Ch2 eq:dVdT_config L232-244). **코드에서 이 항을 명시 추가하면 이중계산**.
- **전자항 δS_e는 T1에서만** 살린다(중심값에 흡수 안 되는 급변, Ch2 L406-408·L631-632). §1-6의 dSe가 정확히 이 δS_e 슬롯.
- **가법성 정당화**(Ch1 L1702-10): config(리튬 자리 점유)와 elec(전자 밴드 점유)는 직교 자유도 → Z=Z_config·Z_elec 인수분해 → S 가산. 이중계산 금지는 "config 슬롯=중심값만·elec 슬롯=MIT 골만"으로 각 항이 자기 자유도 몫만 채워 보장.

---

## §2. 가역 발열 q_rev 설계

### 2-1. 채택 구조 — dqdv 밖 별도 메서드 (곡선과 분리)

**결정: q_rev는 `dqdv`에 넣지 않고 별도 메서드 `reversible_heat(...)` + `entropy_coefficient(...)`로 둔다.**

근거: q_rev는 `∂U_oc/∂T`(=ΔS/F)를 요구하는데(Ch2 eq:qrev L645), 이는 dqdv가 내는 dQ/dV와 **다른 물리량**(엔트로피 계수). Ch2 종합식(use-this box L668-685)은 전하 보존 음함수 `Σ Q_j ξ_eq,j(U_oc,T)=Qx`를 풀어 U_oc(x,T)를 얻는 별도 절차. dqdv 본체에 섞으면 흑연 회귀 0-diff 위반 + 물리 혼동.

### 2-2. 함수 시그니처·핵심 식

```python
def entropy_coefficient(self, x, T):
    """∂U_oc/∂T(x) [V/K] — Ch2 종합식(use-this, L668-685).
    1) 전하보존 음함수 Σ_j Q_j·ξ_eq,j(U_oc,T)=Q·x 를 풀어 U_oc(x,T) (eq:implicit L441)
    2) 각 전이 ξ_j=ξ_eq,j(U_oc,T), g_j=ξ_j(1−ξ_j)/w_j (eq:gj L454)
    3) 완전식:
       ∂U_oc/∂T = Σ_j Q_j·g_j·[ΔS⁰_j/F + (R/F)·ln(ξ_j/(1−ξ_j))] / Σ_j Q_j·g_j
       (eq:weighted L472 중심값 + 봉우리 내부 config 분포 항)
    반환 [V/K]."""

def reversible_heat(self, x, T, I):
    """가역 발열 q_rev [W] — Ch2 eq:qrev L645.
    dUdT = self.entropy_coefficient(x, T)
    return -I * T * dUdT              # = −(IT/F)·ΔS(x), T 한 번
    부호: 방전 I>0, ΔS>0→q_rev<0 흡열 / ΔS<0→q_rev>0 발열 (Ch2 L658-661)."""
```

- **★q_rev = −IT·∂U/∂T = −(IT/F)ΔS(x), T는 한 번**(Ch2 eq:qrev L645). `entropy_coefficient`가 ∂U/∂T[V/K]를 내고, `reversible_heat`가 `−I·T·(∂U/∂T)`로 T 한 번만 곱함. **T²로 곱하는 실수 금지**(∂U/∂T가 이미 V/K, ×T×I → V·A = W).
- ΔS(x)를 별도로 만들 필요 없음 — `∂U_oc/∂T = ΔS/F`이므로 `−IT·∂U/∂T`가 곧 `−(IT/F)ΔS`. F를 다시 곱하거나 나누지 않음.

### 2-3. ΔS(x) 조립 (중심 ΔS⁰_j + config 분포항 + dS_e)

Ch2 use-this box(L671-674)의 완전식이 조립을 이미 규정:

```
∂U_oc/∂T = Σ_j Q_j·g_j·[ ΔS⁰_j/F + (R/F)ln(ξ_j/(1−ξ_j)) ] / Σ_j Q_j·g_j
```
세 성분 매핑:
- **중심 ΔS⁰_j** = dict `dS_rxn`(config=0 봉우리 중심 표준값). vib+elec 중심 흡수(Ch2 L297·L376-379).
- **config 분포항 `(R/F)ln(ξ_j/(1−ξ_j))`** = **코드가 명시 계산**(entropy_coefficient 완전식 안에서). 단 이건 U_oc(x,T) round-trip에서 나오는 w의 T의존과 **동일 물리** — 여기서는 발열 산출용으로 **직접** 완전식에 넣는다(dqdv의 U_j(T)와 이중계산 아님: 별도 산출 경로, 같은 값). `[확정]` Ch2 파생A 수치검증(L484-495)이 완전식=유한차분 부동소수점 일치.
- **dS_e (LCO T1만)** = §1-6의 `func_dSe_molar`. 흑연은 0(전자항 부재, Ch2 L404). LCO T1은 `ΔS⁰_j`에 이미 더해진 상태로 U_oc 계산에 반영되거나, entropy_coefficient의 중심값 슬롯에 `ΔS⁰_1 + dSe(x_local,T)`로 진입.

### 2-4. ★이중계산 직교 — 중심 ΔS⁰_j에 config 재가산 금지

Ch2 warnbox 파생B(L293-309)·L535:
- **중심 ΔS⁰_j 자리(dS_rxn)에는 봉우리 중심 표준값만** — 봉우리 내부 config `R ln[ξ/(1−ξ)]`를 여기 **또 더하면 이중계산**(같은 물리 두 번).
- **분리 방법(코드에서)**: `entropy_coefficient` 완전식은 `ΔS⁰_j/F`(중심)와 `(R/F)ln(ξ_j/(1−ξ_j))`(분포)를 **명시적으로 두 별개 항**으로 더한다. `dS_rxn` dict 값에는 결코 config 부분몰을 미리 섞지 않는다. 봉우리 중심 ξ=1/2에서 `ln(1)=0`이라 두 정의가 모순 없이 맞물림(Ch2 L306·L536-537).
- **hys 분기 처리**(Ch2 파생D L570-593): 가역 발열은 **두 분기 평균**(eq:hys_rev L582): `∂U_oc^rev/∂T = ½(∂U^ch/∂T + ∂U^dis/∂T)`. hys gap ΔU^hys 자체는 **비가역**(소산열, ∝I·ΔU^hys)이라 ∂/∂T와 별개 → q_rev에 섞지 않음. `entropy_coefficient`는 γ=0(분기 없음) 경로면 단일, γ>0이면 σ_d=±1 두 번 평가 후 평균.

### 2-5. 비가역 3분해 옵션

Ch2 eq:qrev(L643) 총 발열 = 가역 + 비가역. 비가역 3분해는 Ch1 근거로 옵션 메서드:

```python
def irreversible_heat(self, x, T, I, ...):
    """비가역 발열 3분해 (옵션). Ch2 eq:qrev 첫 항 I(U_oc−V) 소산.
    Ch1 warnbox: I²R (ohmic) + I·η_ct (charge transfer) + I·η_diff (diffusion).
    ★하프셀 범위 경고(Ch2 warnbox L102-107): 단일 전극만, 전셀 합성(∂U_cell) 범위 밖."""
```
- **[추정] 3분해 세부**: base 프롬프트가 "비가역 3분해 I²R+Iη_ct+Iη_diff"를 명시하나, Ch2 본문은 총 `I(U_oc−V)` 소산(L643)만 닫고 3분해 세 성분의 개별 닫힌식은 문건에 없음 → **옵션·저우선**. Ch1 분극 R_n(eq:vn)은 I²R_n에 대응하나 η_ct·η_diff의 코드 산출식은 근거 미발견. `[근거 미발견]` — 구현 시 문건 보강 필요, P4 필수 아님.
- **하프셀 범위 준수**(Ch2 warnbox L102-107): 단일 전극(흑연 or LCO vs Li)만. 전셀 합성 `∂U_cell/∂T=∂U_cat/∂T−∂U_an/∂T` **범위 밖**(후속) — 메서드 docstring에 명시.

---

## §3. ★흑연 회귀 0-diff 가드

### 3-1. 무섭동 구조 — 상속(합성 아닌 subclass) 채택

**결정: 상속(subclass) — `class LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)`. base는 1바이트 무변경, LCO 훅만 override.**

세 후보 비교:
| 후보 | 흑연 0-diff 보장 | 채택 |
|---|---|---|
| **상속(subclass)** | base 본체 무변경 → 흑연 인스턴스는 base 그대로 실행. LCO만 override 지점 진입 | **★채택** |
| 합성(composition) | LCO가 base 인스턴스 위임 — 가능하나 dqdv 전이루프 중간 훅 삽입이 어려움(전자항은 루프 내부 U_j 평가 시점 개입) | 차선 |
| 플래그(base에 electronic 인자) | base 시그니처·본체 수정 → **흑연 회귀 byte-diff 발생** | **기각** |

- 전자항 개입 지점 = dqdv 전이 루프 내 `U_j` 평가 직후(L433-450 사이). subclass가 이 지점을 **override 가능한 protected 메서드로 추출**(base에 `_transition_dS_extra(tr, xi_eq, T)` 훅 추가, 기본 반환 0.0)해야 함.
- **★단, 이 훅 추출은 base 수정**이다 → §3-2에서 "허용되는 최소 base 수정"으로 격리·정당화.

### 3-2. base 최소 수정 vs 완전 무변경 — 트레이드오프

전자항을 subclass로 격리하려면 base dqdv 루프에 훅 1점이 필요. 두 길:

**(A) base에 훅 1줄 추가 (권장)**: dqdv 전이 루프 L436~450 사이에
```python
# base 기본: 0.0 반환(흑연 무영향). subclass override.
dS_extra = self._transition_dS_extra(tr, ...)   # 기본 0.0
# U_j 평가에 dS_extra 반영 (dS_extra=0이면 흑연과 완전 동일)
```
- **흑연 0-diff 근거**: base `_transition_dS_extra` 기본 반환 0.0 → `dS_rxn + 0.0` = 원식. 부동소수점 `x+0.0==x`(0.0은 덧셈 항등원, NaN/inf 없으면) → **byte 일치**.
- **위험**: `+0.0` 부동소수점 항등성은 유한값에서만 보장. dS_rxn이 유한(데이터셋 확정)이라 안전. 단 회귀 하네스로 실증 필수(§3-3).

**(B) base 완전 무변경 + subclass가 dqdv 전체 재정의**: 흑연 base는 절대 안전하나 LCO dqdv가 base 로직 복붙 → DRY 위반·유지보수 위험. **기각**.

→ **(A) 채택하되, `+0.0` byte 동일성을 §3-3 하네스로 반드시 실증**. 실증 실패 시 (B) 폴백.

> **[추정] byte 동일성**: `a + 0.0 == a`는 IEEE754에서 a가 유한·비-NaN이면 성립(−0.0 케이스도 `a + 0.0`은 +0.0 결과라 dqdv 출력 배열 동일). 단 `np.interp`·`linspace` 경로의 부동소수점 재현성은 하네스로 확인. `[추정→하네스로 확정]`

### 3-3. 회귀 하네스 설계 (기존 curve() 출력 byte 일치 검증)

**하네스 = P1 §4 보완4(면적=Q assert 부재 L431)를 함께 해소하는 확장 self-test.**

```python
# 회귀 가드 1: 흑연 base 경로 byte-identical
V = np.linspace(0.03, 0.34, 1000)
graphite_ref = GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05)
# 개정 후 동일 인스턴스 재실행 결과와 비교 (또는 LCO subclass가 base 흑연 데이터로 실행)
for s in (+1,-1):
    for I in (0.02, 0.2, 1.0):
        y_ref  = graphite_ref.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s)
        y_new  = <개정판 동일 호출>
        assert np.array_equal(y_ref, y_new), "흑연 회귀 byte-diff!"   # ★byte 일치
# 회귀 가드 2: 면적 보존 (P1 보완4 결함 해소)
for tr in GRAPHITE_STAGING_LIT:
    area = np.trapz(<전이 평형 peak>, V)      # ∫Q·ξ(1−ξ)/w dV
    assert abs(area − tr['Q']) < 1e-6, "면적≠Q (DC 보존 위반)"
```
- **byte 일치 = `np.array_equal`**(값 완전 동일). `allclose`(허용오차) 아님 — 0-diff는 **정확 일치** 요구.
- **저장 기준(golden)**: 개정 전 `Anode_Fit_v1.0.10.py`의 흑연 dqdv 출력을 golden 배열로 디스크 저장(예 `.npz`) → 개정 후 로드·비교. 이게 진짜 "회귀 가드"(개정 전후 대조).
- **면적보존 DC=1 유지**(P1 §0 L93·§2-D L347): `_causal_lowpass` DC gain=1, 평형 ∫=1.000000. LCO 전자항 추가가 이를 깨지 않는지도 검증(LCO 전이 면적도 Q_j 보존 assert).

### 3-4. 면적보존 DC=1 유지 확인

- **평형 peak** `Q·ξ(1−ξ)/w`의 ∫=Q (Ch1 eq:eqpeak L1193 "배경 차감 면적=Q_j"). LCO도 동일식 → 자동 보존.
- **꼬리** `(ξ_eq−ξ_lag)/L_V`의 DC 이득=1(`_causal_lowpass` 계수 `[1−ρ]/[1,−ρ]` 합=1, P1 L200). LCO 꼬리도 같은 함수 재사용 → 보존.
- **전자항이 면적 불변**: dS_e는 **U_j 위치**만 이동(∂U/∂T 통해), 면적 Q_j·폭 w는 안 건드림 → 면적 DC=1 유지. `[확정]`(전자항은 중심 이동만, Ch1 L1207-11).

---

## §4. Serena 편입 레시피

> **원칙**: 코드 소유권(식별자·대소문자·정수코드 보존)·지정 범위 외 임의수정 X. 신규는 `insert_after_symbol`, 기존 무변경. `replace_symbol_body`는 base 훅 1점만(최소화·근거 명시).

| # | 대상 심볼 | 연산 | 근거·최소성 |
|---|---|---|---|
| 1 | `func_chi_d` (L158-163, 모듈 함수 마지막) 뒤 | `insert_after_symbol` → `func_g_EF_gate`, `func_dSe_molar` 2개 신규 | 순수 함수, 흑연 경로 불침투. 기존 무변경 |
| 2 | `GRAPHITE_STAGING_LIT` (L531-560) 뒤 | `insert_after_symbol` → `LCO_STAGING_LIT` 신규 상수 | 데이터셋 동격 배치. 흑연 상수 무변경 |
| 3 | `GraphiteAnodeDischargeDQDV.dqdv` (L370-480) | **`replace_symbol_body` (★최소 1점)** — 전이 루프 U_j 평가부(L436-450)에 `_transition_dS_extra` 훅 1줄 삽입 | §3-2 (A). base 기본 반환 0.0 → 흑연 byte 일치. **유일한 base 본체 수정** |
| 4 | `GraphiteAnodeDischargeDQDV` 클래스 (L192, 메서드 사이) | `insert_after_symbol` → `_transition_dS_extra(self,tr,...)` 신규 메서드(기본 `return 0.0`) | base에 훅 메서드 추가(본체 아닌 신규 메서드) |
| 5 | `GraphiteAnodeDischargeDQDV` 클래스 정의 뒤 (L524 이후) | `insert_after_symbol` → `class LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)` 신규 | 상속. `_transition_dS_extra` override + `reversible_heat`·`entropy_coefficient`·`irreversible_heat` 메서드 |
| 6 | `__main__` self-test (L567-703) 끝 | `insert_after_symbol` 또는 블록 확장 | §3-3 회귀 하네스(byte 일치 + 면적 assert) + LCO 작동 검증 추가 |

**최소화 근거(replace_symbol_body를 #3 1점으로 한정)**:
- 전자항 개입은 dqdv 전이 루프 내부라 훅 없이는 subclass가 dqdv 전체를 복붙해야 함(DRY 위반, 회귀 위험 ↑). 훅 1점이 **가장 작은 침습**.
- 훅 기본값 0.0 → 흑연 경로 무섭동(§3-2). #3 외 모든 신규는 insert(기존 무변경).
- **死코드 `func_U_j_hys`(L82-91)는 P1 판정(보존, L50·L182) 따름** — 건드리지 않음.

**코드 소유권 보존 체크**:
- 기존 식별자·대소문자·`GRAPHITE_STAGING_LIT` 정수/문자열 인코딩 절대 보존.
- 신규 심볼 명명은 기존 관례 따름(`func_*` 모듈함수, `_*` protected, PascalCase 클래스).
- `chi_split` 주입 관례(L214-224)·per-tr override 관례 계승(LCO 전자항도 tr dict 키로 노출, 하드코딩 X).

---

## §5. 그래프 검증 계획

> **목표**: 흑연+LCO dQ/dV·발열 곡선 개형이 문건 물리와 정합함을 시각·수치로 확인.

### 5-1. dQ/dV 개형 (흑연 회귀 + LCO 신규)

| 검증 | 방법 | 기대 개형 (문건 근거) |
|---|---|---|
| **흑연 회귀** | 개정 전후 dqdv 오버레이 (동일 축) | **완전 중첩**(byte 일치, §3-3). 4 peak @0.085~0.210 V (Ch1 tab:staging L1673-76) |
| **LCO 3 peak** | `LCOCathodeDQDV.curve` @298K, 방·충 | T1~3.90·T2~4.05·T3~4.17 V 3봉우리 (Ch1 L1202-03). T2·T3 좁은 한 쌍(큰 Ω order-disorder, Ch1 L1206) |
| **LCO 히스 분기** | γ>0 dis/chg peak 분리 | dis peak > chg peak, 간격=γ·ΔU_hys (Ch1 eq:Ubranch L634-35) |
| **면적=Q** | 각 전이 ∫dQ/dV dV | =Q_j (§3-4, DC 보존) |
| **방향 부호** | 방전 V↑→탈리튬화 진행 | ξ_eq↑ (Ch1 signbox L846-51) |

### 5-2. 발열 곡선 개형

| 검증 | 방법 | 기대 개형 (문건 근거) |
|---|---|---|
| **엔트로피 계수 ∂U/∂T(x)** | `entropy_coefficient` x-스윕 | 저-x 양(config 발산 +∞ 방향)·고-x 음(vib baseline), 비선형 (Ch2 L77·tab:limits L610-611) |
| **연속 블렌드(계단 아님)** | 전이 경계에서 ∂U/∂T 연속 | ΔS⁰_j→ΔS⁰_{j+1} 연속 이동, 계단 X (Ch2 파생A fig:blend L520) |
| **유한차분 대조(round-trip)** | 완전식 vs `[U_oc(x,T₂)−U_oc(x,T₁)]/ΔT` (T₁=292.15,T₂=298.15) | 부동소수점 일치(절대오차≈0), 단순식만 config 항만큼(최대 0.18 mV/K) 빗나감 (Ch2 파생A L488-491) |
| **q_rev 부호** | `reversible_heat` 방전 x-스윕 | 저-x ΔS>0→q_rev<0 흡열 / 고-x ΔS<0→q_rev>0 발열. stage 2→1(x≈0.5) 큰 음 ΔS→발열 신호 (Ch2 L658-664) |
| **LCO T1 전자항 T-선형 신호** | 다온도 ∂U_1/∂T | **∂U/∂T 기울기가 T에 선형**(위치 이동은 ∝T², Ch1 L1042-46·L1208-11). config·vib와 분리 식별 |
| **전자항 골 깊이 검산** | T1 중심 dSe | ≈−46 J/mol/K (σ(1−σ)=1/4, g_max=13, Δx_MIT=0.05, T=300K; Ch1 L1123) |

### 5-3. 검증 산출물

- **figs 저장**: 흑연 회귀 오버레이·LCO dQ/dV·∂U/∂T(x)·q_rev(x)·다온도 T1 이동 5종 → `Claude/docs/v1.0.10/figs/` 또는 `results/code/figs/`(P1 관례 L9).
- **수치 assert(self-test 편입)**: byte 일치·면적=Q·유한차분 부동소수점 일치·q_rev 부호 교대·전자항 골 깊이 ≈−46. §3-3 하네스에 통합.

---

## §6. 리스크·미검증 (4-tier)

- **[확정]** MSMR 동형 → 곡선 골격 무변경 재사용 / config 이중계산 = "logistic w가 이미 담음, 코드 재가산 X" / q_rev=−IT·∂U/∂T (T 한 번) / dS_e 몰당 단위(N_A→R·eV 나눗셈, 부호 삽입<0) / 死코드 func_U_j_hys 보존.
- **[근거 미발견]** 비가역 3분해(I²R+Iη_ct+Iη_diff) 개별 닫힌식 — Ch2는 총 소산 `I(U_oc−V)`만 닫음. 옵션·저우선, 구현 시 문건 보강 필요.
- **[추정]** ξ_eq,1↔x 선형 매핑(문건은 "대응"만 명시, 함수형 미규정 — 선형 최소가정, 피팅 인자 노출) / `+0.0` byte 동일성(IEEE754 유한값 성립 예상, 하네스로 확정).
- **[미검증]** LCO config 중심 표준값(0.47/1.49)·게이트 3값(g_max·x_MIT·Δx_MIT) round-trip 미실증 초기값 — 흑연 ΔS_rxn=−16 동격으로 self-test round-trip 후 승격(Ch1 L1729-33).

**핵심 리스크 3**:
1. **base 훅 1점(replace_symbol_body #3)의 byte 동일성** — `+0.0` 부동소수점 항등성이 np.interp 경로에서 정확 재현되는지 golden 배열 대조 필수. 실패 시 subclass dqdv 전체 재정의(B) 폴백.
2. **좌표 매핑 ξ↔x** — 선형 가정이 T1 물리와 어긋나면 전자항 위치 오차. 피팅 인자로 노출해 흡수.
3. **이중계산 경계** — entropy_coefficient 완전식의 config 항이 dqdv의 w(T)와 "같은 물리 별도 산출"임을 명확히(같은 값·다른 경로, 이중계산 아님). 코드 주석·docstring으로 못박아 후속 혼동 차단.

---

## 5줄 요약

1. **채택 구조**: 기존 `GraphiteAnodeDischargeDQDV`를 무변경 base로, LCO는 얇은 subclass `LCOCathodeDQDV`(상속) — MSMR 동형(Ch1 eq:msmr)이 "곡선 골격 구조 변경 0"을 보장, 바뀌는 건 데이터셋 교체 + T1 전자항 plug-in 둘뿐.
2. **핵심 시그니처**: `func_g_EF_gate`·`func_dSe_molar`(전자 부분몰 몰당, N_A→R·eV 나눗셈·부호<0) 신규 모듈함수 / subclass `entropy_coefficient`(∂U/∂T 완전식)·`reversible_heat`(q_rev=−IT·∂U/∂T, **T 한 번**) / base 훅 `_transition_dS_extra`(기본 0.0).
3. **회귀 가드**: 상속으로 base 무섭동, base 수정은 dqdv 훅 1점(`replace_symbol_body` 유일)뿐이며 기본 반환 0.0 → 흑연 `np.array_equal` byte 일치. golden 배열 대조 + 면적=Q assert(P1 보완4 결함 동시 해소) + DC=1 유지.
4. **이중계산 처리**: config 슬롯(`dS_rxn`)에는 봉우리 중심 표준값 `ΔS⁰_j`만 — 봉우리 내부 config `R ln[ξ/(1−ξ)]`는 logistic w가 자동 생성하므로 **코드 재가산 금지**(Ch2 파생B). elec 슬롯(dS_e)은 T1만, hys는 분기 평균으로 가역만 추출(비가역 gap 분리).
5. **리스크**: base 훅 `+0.0` byte 동일성(하네스로 확정, 실패 시 subclass dqdv 재정의 폴백)·ξ↔x 선형 매핑([추정], 피팅 인자 노출)·비가역 3분해 개별식 [근거 미발견](옵션 저우선). Serena 편입 6단계 = 신규 5 insert + base 훅 1 replace, 死코드 func_U_j_hys 보존.
