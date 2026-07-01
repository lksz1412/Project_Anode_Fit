# P5 감사 드래프트 S2 — B조: code↔Ch2 상호 충실도

> **감사 ID**: S2 | **조**: B조(code↔Ch2 상호충실도) | **작성**: 2026-07-01
> **대상**: `docs/v1.0.10/Anode_Fit_v1.0.10.py` ↔ `docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`
> **참조 앵커**: `results/process/V1010_P4_code-revision_RESULT.md`
> **규약**: 감사 의견만 — 코드/문건 수정 절대 X. 추정 금지(코드 줄·tex 식 근거 명시).
> **4-tier**: 확정 / 근거미발견 / 추정 / 미검증

---

## 개요

B조 감사 범위: Ch2 발열 식 ↔ 코드 양방향 충실도.
검사 항목: (1) Ch2→코드: eq:qrev·eq:weighted 가중식·파생B 이중계산·비가역 lumped·warnbox 하프셀 스코프가 코드에 반영됐나. (2) 코드→Ch2: 각 발열 메서드가 Ch2 식 근거가 있나. (3) T 한 번·이중계산 직교(dqdv 무가산/q_rev 가산 비대칭)·부호·차원 재검산. (4) 갭 적발.

---

## 섹션 1. Ch2→코드 양방향 매핑

### 1-1. eq:qrev — 가역 발열 핵심 식

**Ch2 식 위치**: `\sec:revheat`, eq(2.29) 박스:
```
\dot Q_\rev = -I T \frac{\partial U_\oc}{\partial T} = -\frac{IT}{F}\Delta S(x)
```
단일 활물질 한계, $I>0$ 방전 부호 규약.

**코드 위치**: `reversible_heat` 메서드, 코드 L578-586.
```python
def reversible_heat(self, V_n, T=298.15, I=1.0):
    """가역 발열 q_rev = −I·T·∂U_oc/∂T [W] (Ch2 eq:qrev, ★T 한 번)."""
    T = _finite_pos("T", T)
    return -float(I) * T * self.entropy_coefficient(V_n, T)
```

**매핑 판정**: **확정 — 1:1 정합**.
- 코드 `−I * T * self.entropy_coefficient(...)` = Ch2 $-I T (\partial U_\oc/\partial T)$. 구조 완전 일치.
- `entropy_coefficient`가 $\partial U_\oc/\partial T$[V/K]를 반환하므로 곱 결과는 [W] = [A][K][V/K]. 차원 정합.
- T가 정확히 한 번 곱해진다(T² 금지 조건 충족): `entropy_coefficient` 내부에 추가 T 곱 없음 — L554-576 정독 확정.

---

### 1-2. eq:weighted — 겹침 가중식 (완전식)

**Ch2 식 위치**: `\sec:revheat` 핵심 박스(L670-685):
```
\frac{\partial U_\oc}{\partial T}(x) =
  \frac{\sum_j Q_j g_j(x)[\Delta S^0_j/F + (R/F)\ln(\xi_j/(1-\xi_j))]}
       {\sum_j Q_j g_j(x)},
\quad g_j = \frac{\xi_j(1-\xi_j)}{w_j}
```
두 조각: ① 중심 표준값 $\Delta S^0_j/F$ ② 봉우리 내부 config 분포 $(R/F)\ln[\xi_j/(1-\xi_j)]$.

**코드 위치**: `entropy_coefficient` 메서드, 코드 L544-576.
```python
def entropy_coefficient(self, V_n, T=298.15):
    ...
    for tr in self.transitions:
        ...
        xi = func_ksi_eq(T, V, U_j, n_j)
        g = xi * (1.0 - xi) / w                    # g_j = ξ(1-ξ)/w
        xi_c = np.clip(xi, eps, 1.0 - eps)
        config = (R / F) * np.log(xi_c / (1.0 - xi_c))  # (R/F)ln[ξ/(1-ξ)]
        Qg = tr['Q'] * g
        num = num + Qg * (dS_eff / F + config)     # 분자: Q_j g_j [ΔS/F + config]
        den = den + Qg                               # 분모: Q_j g_j
    dUdT = np.where(den > 0.0, num / np.maximum(den, eps), 0.0)
```

**매핑 판정**: **확정 — 완전식 1:1 구현**.
- `g = xi * (1.0 - xi) / w` = $g_j = \xi_j(1-\xi_j)/w_j$. 정합.
- `dS_eff / F + config` = $\Delta S^0_j/F + (R/F)\ln[\xi_j/(1-\xi_j)]$. 두 조각 모두 반영.
- `num / den` = 가중 평균. 구조 완전 일치.
- `dS_eff`는 `_effective_dS_rxn`에서 나오므로 LCO 전자항이 seam을 통해 일관 반영됨.

---

### 1-3. 파생 B — 이중계산 금지 (dqdv 무가산/q_rev 가산 비대칭)

**Ch2 위치**: `\sec{sec:config}` warnbox(L293-309):
> config 를 $\Delta S^0_j$에 **또** 더하면 같은 물리를 두 번 세는 것. ... config항과 표준값은 결코 겹치지 않음.

**Ch2 추가 위치**: `entropy_coefficient` docstring(코드 L548-552):
> ★dqdv 곡선은 이 config 항을 넣지 않는다(폭 w가 이미 담음, Ch2 파생 B) — q_rev 경로만 명시 가산.

**코드에서 비대칭 구조 확인**:
- `dqdv` 메서드(L392-502): `ksi_eq * (1.0 - ksi_eq) / w` 평형 종 형태. $w$ 안에 배분돼 있고 config 로그 항 **미가산**. 정확 L486: `peak_shape = ksi_eq * (1.0 - ksi_eq) / w`.
- `entropy_coefficient`(L544-576): config 항 `(R/F)*log(xi/(1-xi))` **명시 가산**.

**매핑 판정**: **확정 — 파생 B 이중계산 직교 구현**.
- dqdv 경로에는 config 로그 항 없음(w가 담음). entropy_coefficient에는 명시 가산. 두 경로가 직교함.
- Ch2 warnbox의 "한 번씩만 센다" 규약과 정확히 대응.

---

### 1-4. 비가역 발열 lumped — Ch2 eq:qrev 첫 항

**Ch2 식 위치**: eq(2.29) 첫 항:
```
\dot Q_\irr = I(U_\oc - V) \ge 0
```
Ch2 warnbox/박스에 **오직 lumped 형만** boxed 제시됨. 3분해(I²R + Iη_ct + Iη_diff)는 Ch2에 boxed 식 부재.

**코드 위치**: `irreversible_heat` 메서드, L588-596.
```python
def irreversible_heat(self, U_oc, V, I):
    """비가역 발열(과전압 소산) q_irr = I·(U_oc−V) ≥ 0 [W] — lumped(Ch2 eq:qrev 첫 항).
    ★3분해(I²R_n + I·η_ct + I·η_diff)는 Ch2에 boxed 식이 없다 ... → 본 구현은 lumped만 둔다.
    """
    return np.asarray(I) * (np.asarray(U_oc) - np.asarray(V))
```

**매핑 판정**: **확정 — lumped 1:1, 3분해 미구현 Ch2 근거 있음**.
- `I*(U_oc - V)` = Ch2 $I(U_\oc - V)$. 구조 완전 일치.
- 3분해 부재는 Ch2가 boxed로 lumped만 제시한다는 근거에서 올바른 선택. 코드 docstring에 근거 명시됨.
- P4 이월 항목 "비가역 3분해: lumped만 구현"과 일치. **확정 갭 아님, 의도적 범위 제한**.

---

### 1-5. warnbox 하프셀 스코프

**Ch2 위치**: 서두 warnbox(L102-107):
> 본 장은 단일 전극(흑연 vs. Li 금속)의 하프셀 $\partial U_\oc/\partial T$와 그 가역 발열만 다룬다. 전셀 합성 $\partial U_\mathrm{cell}/\partial T = \partial U_\mathrm{cat}/\partial T - \partial U_\mathrm{an}/\partial T$는 **범위 밖**.

**코드 매핑**: `reversible_heat`, `entropy_coefficient` 모두 단일 전극(개별 음극 또는 양극 인스턴스)에 대해 동작. 전셀 합성 로직 없음.

**매핑 판정**: **확정 — 스코프 일치**. 코드는 전극 단독 계산만 제공하고, 전셀 합성은 사용자 레이어 몫으로 남겨 두었다. Ch2 범위 박스와 정합.

---

## 섹션 2. 코드→Ch2 역방향 점검

각 발열 메서드가 Ch2에 근거가 있는지 확인한다.

### 2-1. `entropy_coefficient` → Ch2 근거

코드 L544에 선언. 반환값 = $\partial U_\oc/\partial T$ [V/K].

**Ch2 근거**: eq(2.18) `\eqref{eq:implicit_diff}` + eq(2.19)(gj) + eq(2.20)(dxidT) → eq(2.21) 단순식 `\eqref{eq:weighted}` + config 완전식(L670-684 핵심 박스). 충분한 근거 있음.

**판정**: **확정 — Ch2에 완전 근거**.

---

### 2-2. `reversible_heat` → Ch2 근거

코드 L578.

**Ch2 근거**: eq(2.29) `\eqref{eq:qrev}` $\dot Q_\rev = -IT\partial U_\oc/\partial T$. Bernardi 에너지 수지(Ch2 \sec:revheat 도입).

**판정**: **확정 — Ch2에 직접 근거**.

---

### 2-3. `irreversible_heat` → Ch2 근거

코드 L588.

**Ch2 근거**: eq(2.29) 첫 항 $\dot Q_\irr = I(U_\oc - V)$.

**판정**: **확정 — Ch2에 직접 근거**.

---

### 2-4. `_effective_dS_rxn` seam → Ch2 근거

코드 L533: base 클래스 항등(흑연 `return tr['dS_rxn']`), L655: LCO override(`dS + func_dSe_molar(...)`).

**Ch2 근거**:
- 흑연 항등: Ch2 `\sec:vibel`에서 흑연의 vibrational·electronic이 $\Delta S^0_j$(중심 표준값)에 흡수됨으로 처리. `tr['dS_rxn']` = $\Delta S^0_j$.
- LCO override: Ch2 `\ssec:elec`(L381-408), MIT 전이가 급변 → $x$-의존 electronic 항을 따로 유지. `func_dSe_molar` 게이트가 Ch2 `\ssec:elec` 물리 구현.

**판정**: **확정 — Ch2에 물리 근거 있음**.

단, Ch2 `\ssec:elec`에서 전자항을 T-선형 Sommerfeld $S_e \propto T$(eq 2.22)로 전개했는데, 코드 LCO override(L659-670)는 `T_ref=298.15` 동결 상수 오프셋으로 근사. Ch2 `\ssec:elec`의 Sommerfeld T-스케일과 코드의 단일-기준 동결 근사 사이에 물리적 차이가 있음 → 섹션 3에서 상세 분석.

---

## 섹션 3. 핵심 물리 재검산

### 3-1. T 한 번 조건 (T² 금지)

**Ch2 규약**: eq:qrev = $-IT\partial U_\oc/\partial T$. T는 외부에서 한 번만.

**코드 경로 추적**:
1. `reversible_heat(V_n, T, I)` L586: `return -float(I) * T * self.entropy_coefficient(V_n, T)`
2. `entropy_coefficient(V_n, T)` L544: 반환값 = [V/K]. T를 분모에 갖지 않음. 내부 루프 검사:
   - L562: `dS_eff = self._effective_dS_rxn(tr, T)` — T 인자 전달되나 T가 곱해지는 연산 없음(흑연: `return tr['dS_rxn']`, 상수).
   - L563: `U_j = func_U_j(T, ...)` — T·ΔS/F 반환이나, U_j는 entropy_coefficient에서 ξ 계산에만 쓰이고 직접 ΔS에 곱해지지 않음.
   - L568: `xi = func_ksi_eq(T, V, U_j, n_j)` — T 내부에서 폭 w=nRT/F 계산에 쓰임(T 의존 ξ → g에 영향). 이 경로의 T 의존은 분포 폭에 들어가는 것으로 별도 물리.
   - L571: `config = (R/F)*log(xi_c/(1-xi_c))` — T 무관(ξ를 통한 간접 의존만).
   - L573: `num = num + Qg * (dS_eff/F + config)` — dS_eff는 상수(흑연). T가 직접 곱해지지 않음.
   - 결과 `dUdT = num/den` — [V/K].
3. 최종: `reversible_heat = -I * T * dUdT` — T 정확히 한 번.

**판정**: **확정 — T 한 번 조건 충족**. T² 경로 없음.

---

### 3-2. 부호 규약

**Ch2 eq:qrev 부호 박스**(L645):
```
\dot Q_\rev = -IT\frac{\partial U_\oc}{\partial T}
```
srcbox(L651-654): ΔS = +F·∂U_oc/∂T 규약. 방전(I>0)·ΔS>0 → q_rev<0(흡열). 방전·ΔS<0 → q_rev>0(발열).

**코드 부호**(L582-586):
```python
"""...방전 I>0: ΔS>0(∂U/∂T>0) → q_rev<0 흡열 / ΔS<0(∂U/∂T<0) → 발열(Ch2 부호규약)."""
return -float(I) * T * self.entropy_coefficient(V_n, T)
```

**판정**: **확정 — 부호 정합**. 코드 docstring이 Ch2 srcbox와 동일한 부호 해석을 명시. 기호 구조도 일치.

---

### 3-3. 차원 검산

| 양 | Ch2 표기 | 코드 단위 | 정합? |
|---|---|---|---|
| $\partial U_\oc/\partial T$ | [V/K] | `entropy_coefficient` 반환 [V/K] (분자: [J/mol/K]/F=[V/K], 분모: [1/V]·[1]) | 확정 O |
| $\dot Q_\rev$ | [W]=[A][V] | `reversible_heat` = [A][K][V/K] = [W] | 확정 O |
| $g_j = \xi(1-\xi)/w$ | [1/V] | `xi*(1-xi)/w`, w=[V] → [1/V] | 확정 O |
| config = $(R/F)\ln[...]$ | [V/K] × (1/T)·T = [V/K]·가중됨 | `(R/F)*log(...)` = [J/(mol·K)] / [C/mol] = [V/K] | 확정 O |

---

### 3-4. 이중계산 직교 검산 (파생 B 핵심)

**Ch2 규약** (L296-308 warnbox):
- $\Delta S^0_j$: 중심 표준값, config 항을 포함 **안 함** (중심에서 config=0).
- config: $(R/F)\ln[\xi/(1-\xi)]$, 봉우리 내부 분포 항.
- 둘을 더하면 이중계산.

**코드 경로 검사**:
- `dqdv` 내부: `peak_shape = ksi_eq * (1.0 - ksi_eq) / w` (L486) — $\xi(1-\xi)/w$, logistic 종. logistic 폭 $w$ 안에 `nRT/F`가 들어 있어 T 의존이 내포되나, 이것은 종의 형태를 만드는 것이지 $\partial U/\partial T$의 config 항을 별도 가산하는 게 아님.
- `entropy_coefficient` 내부: `config = (R/F)*log(xi/(1-xi))`를 **명시 가산**.

**두 경로가 동일 ξ를 쓰지만 목적이 다름**:
- `dqdv`: ξ·(1-ξ)/w → **dQ/dV 봉우리 형태**.
- `entropy_coefficient`: ξ → **발열 가중 계산**, config 로그 항 별도 가산.

**판정**: **확정 — 이중계산 없음**. dqdv 경로는 config 로그 항 가산 없음; entropy_coefficient 경로만 가산. 직교 관계 유지.

---

## 섹션 4. 갭 적발

### 갭 G1: LCO 전자항 T-스케일 — Ch2 Sommerfeld vs. 코드 단일-기준 동결 근사

**위치 (Ch2)**: `\ssec:elec`, eq(2.22)(L391-394):
```
S_e = \frac{\pi^2}{3} k_B^2 T g(E_F)
```
Sommerfeld 전자 엔트로피는 **T에 선형**. 즉 $\Delta S_e \propto T$ 의존.

**위치 (코드)**: `LCOCathodeDQDV._effective_dS_rxn`(L655-671):
```python
T_ref = 298.15
dS = dS + func_dSe_molar(tr['x_center'], T_ref, ...)  # T_ref 동결 상수 오프셋
return dS  # T-무관 상수
```
`T` 인자를 받지만 `T_ref=298.15`로 고정. 결과 `dS_eff`가 T-무관 상수.

**갭 내용**: Ch2 eq(2.22)의 $S_e \propto T$에서 파생되는 부분몰 전자 엔트로피는 T-선형이어야 하지만, 코드는 `T_ref=298.15` 동결로 T-무관 상수로 근사.

**근거**: 코드 docstring L659-665에 근사 이유와 한계 명시:
> "전자항은 기준온도 T_ref에서 동결한 상수 오프셋으로 더한다(단일-기준 근사). → dS_eff가 T-무관이 되어 ... Sommerfeld T-스케일(∝T)과 eq:U1T2의 center-T_ref 별도적분(½=a_e/2F 인자)은 다온도 round-trip 피팅 단계의 과제로 분리한다(P4 미구현, 라벨)."

**4-tier 분류**: **확정 갭 — 의도적 근사이나 Ch2 Sommerfeld(T-선형)와 코드(T-상수)의 물리적 차이가 존재함**.

- 단일 온도(T=298.15K)에서: 근사가 정확함(동결 온도와 실제 T 일치).
- 다온도 계산(T ≠ 298.15K)에서: `entropy_coefficient(V_n, T)` 내부의 `func_dSe_molar(..., T_ref, ...)` 호출이 T_ref=298.15로 고정되어, 실제 T와 무관하게 동일 ΔS_e 사용. Ch2의 $S_e \propto T$와 불일치.

**master 정정용 정보**:
- 위치: `LCOCathodeDQDV._effective_dS_rxn` (코드 L659), `T_ref = 298.15` 하드코딩.
- 무엇이: `func_dSe_molar(tr['x_center'], T_ref, ...)` → `func_dSe_molar(tr['x_center'], T, ...)`로 변경 시 T-선형 근사.
- 맞는 형태: 다온도 round-trip 피팅 단계에서 T 인자 전달로 Sommerfeld T-스케일 반영(P4 이월 항목 "다온도 T² 곡률"과 연결). 단, 이 변경이 흑연 0-diff 회귀 영향 없음(흑연 base는 LCO override 미사용).

**P4 이월 연계**: P4_RESULT §11 이월항 "다온도 T² 곡률: Sommerfeld T-스케일·eq:U1T2 center-T_ref 별도적분(½=a_e/2F) 미구현" — 본 갭과 동일 사안. **이미 라벨됨**.

---

### 갭 G2: x_MIT=0.50 — Ch2와 코드 내 LCO 시연값의 물리적 타당성

**위치 (코드)**: `LCO_MSMR_LIT` 두 번째 전이(L626-634):
```python
{   # order-disorder(≈3.880 V) — x≈0.5, MIT 창 포함
    ...
    'x_center': 0.50,
    'g_max_eV': 13.0, 'x_MIT': 0.50, 'dx_MIT': 0.05,
}
```

**위치 (Ch2)**: Ch2 `\ssec:elec`(L406-408)에서 LCO MIT를 사례로 언급:
> "LCO 하프셀(사례): Li_xCoO_2는 x에 따라 금속-절연체 전이(MIT)를 겪어 g(E_F)가 급변한다."
Ch2는 MIT의 구체적 x_MIT 값을 명시하지 않음.

**위치 (Ch1)**: P4_RESULT §11 이월항:
> "x_MIT=0.50 tier-C placeholder: Ch1 eq:ggate anchor x_MIT≈0.85·플래토 x≈0.75-0.94와 불일치(내부 정합이나 문서). round-trip 피팅 단계서 물리값 정정·문서 정합."

**4-tier 분류**: **확정 갭(이미 P4 이월 항목)**. Ch2에는 구체적 x_MIT 값 없으므로 Ch2↔코드 직접 불일치는 아님. 그러나 Ch2 §4 시연 검산에 쓰이는 LCO 파라미터(x_MIT=0.50)가 Ch1의 물리값 기대와 어긋나는 사안이 이월됨. **B조 확정 갭이라기보다는 Ch1↔코드 갭(A조 영역)**이나, 발열 seam을 통해 entropy_coefficient에도 영향.

---

### 갭 G3: 파생 D(히스테리시스 분기 ∂U/∂T) — Ch2 제시, 코드 미구현

**위치 (Ch2)**: `\ssec:hys`(L570-593), eq(2.26), eq(2.27):
```
\frac{\partial U_\oc^{(d)}}{\partial T} = \frac{1}{F} \frac{\sum_j Q_j g_j^{(d)} \Delta S_{\rxn,j}}{\sum_j Q_j g_j^{(d)}}
```
```
\frac{\partial U_\oc^\rev}{\partial T} = \frac{1}{2}\left(\frac{\partial U_\oc^\mathrm{ch}}{\partial T} + \frac{\partial U_\oc^\mathrm{dis}}{\partial T}\right)
```
히스 분기별 $\partial U/\partial T$와 가역/비가역 분리.

**위치 (코드)**: `entropy_coefficient`(L544) — `s` (방향) 인자 없음. 단일 평균 ξ 기준. 히스 분기 분리 미구현.

**갭 내용**: Ch2 파생 D는 방전/충전 분기별로 각각 $g_j^{(d)}$를 계산해 $\partial U^{(d)}/\partial T$를 구하고, 그 평균으로 $\partial U^\rev/\partial T$를 산출하는 흐름을 제시. 코드 `entropy_coefficient`는 방향 인자가 없어 항상 방향-무관 ξ_eq(평형 기준)만 사용.

**4-tier 분류**: **확정 갭**. Ch2에 파생 D 명시, 코드에 대응 구현 없음.

**master 정정용 정보**:
- 위치: `entropy_coefficient` 메서드 시그니처.
- 무엇이: `s` (σ_d, 방향) 인자 부재. 히스테리시스 분기 가중 없음.
- 맞는 형태: `entropy_coefficient(self, V_n, T, s=0)` 형태로 방향 인자 추가 후, `s!=0`이면 히스 분기 중심 `center = U_j + hys_shift`로 ξ 계산(현재 `dqdv` 내 방식 재용). `s=0`은 평균(현재 동작 유지). Ch2 eq(2.27) 평균 처리를 사용자가 두 방향 호출 후 평균내는 방식 또는 내부 처리로 구현.
- 리스크: `reversible_heat`가 `entropy_coefficient`를 호출하므로 시그니처 변경 시 연쇄 영향.

**주의**: Ch2 한계·갭 항목(L693-694)에서 "히스테리시스 하 경로의존 $\partial U_\oc/\partial T$ 측정 불확실도 정량화는 본 장 범위 밖이며, 파생 D는 가역/비가역 분리의 틀만 제시"라고 명시. 즉 파생 D는 **틀**만 제시이고, 완전 구현은 범위 밖으로 인정됨. 따라서 "미구현 = 오류"라기보다 **의도적 스코프 제한의 갭**임.

---

### 갭 G4: Ch2 eq:weighted 단순식 vs. 완전식 — 코드는 완전식만 구현

**위치 (Ch2)**: eq(2.21) `\eqref{eq:weighted}` 단순식(중심 표준값만)과, L670-684 핵심 박스 완전식(+config).

**위치 (코드)**: `entropy_coefficient`(L544-576) — config 항을 항상 포함 = 완전식 전용.

**갭 내용**: Ch2 수치 검증(L485-494 srcbox)에서 "단순식의 절대오차 최대 0.18 mV/K"라고 언급. 코드는 단순식(중심 근사) 인터페이스를 제공하지 않음. Ch2 내 단순식은 비교용 개념이지만, 사용자가 단순식 산출을 원할 경우 코드에서 config 항을 끄는 옵션이 없음.

**4-tier 분류**: **근거미발견**. 단순식 인터페이스가 없다는 것이 불일치인지는 Ch2가 명시적으로 코드에 요구하지 않음. 수치 검증 근거 문건이 내부 자료(`\cite{numverif2026}`)이므로 코드 공개 요건인지 미확인.

---

### 갭 G5: Ch2 한계·갭 §6 항목 — 코드 내 라벨 대응 점검

**Ch2 한계 항목**(L687-697):
1. 완전식이 FD와 부동소수점 정밀도로 일치 — 코드 `entropy_coefficient` 구현됨(확정 O).
2. 히스 경로의존 측정 불확실도 — 범위 밖(갭 G3과 연결).
3. 상호작용 Ω 온도 의존(2차 항) — 코드 미구현, Ch2 범위 밖으로 명시.
4. electronic 항 절대값(흑연 소수 취급) — 코드 흑연 base에 electronic 항 없음(항등 seam). Ch2와 정합.
5. 전셀 합성 범위 밖 — 코드도 단일 전극 기준(갭 없음).

**4-tier 분류**: **확정**. 코드와 Ch2 한계 항목이 대체로 정합. Ω 온도 의존(항목3)은 Ch2가 범위 밖으로 명시하고 코드에도 없음 — **의도적 일치**.

---

## 섹션 5. 3대 무결 최종 확인

### 5-1. 물리 배경 정확

B조 범위(Ch2 발열):

| 식 | 정확성 | 근거 |
|---|---|---|
| eq:qrev: $-IT\partial U/\partial T$ | 확정 정확 | Bernardi 에너지 수지, Ch2 eq(2.29) |
| eq:weighted 완전식 | 확정 정확 | 음함수 미분 유도, Ch2 L468-482 |
| 파생 B 이중계산 분리 | 확정 정확 | config=0 @중심 → 정의 자기일관 |
| 부호 규약 (방전 I>0) | 확정 정확 | Ch2 srcbox L651-654 |
| T 한 번 (T² 금지) | 확정 정확 | reversible_heat 구조 검사 |
| 파생 D 히스 분기 | **틀만 Ch2 제시, 코드 미구현** | Ch2 §6 "범위 밖" 인정 |
| LCO Sommerfeld T-스케일 | **의도적 근사(T_ref 동결)** | P4 이월, 다온도 단계 과제 |

### 5-2. 코드 정확

- `reversible_heat`, `entropy_coefficient`, `irreversible_heat` 모두 Ch2 식에 1:1 근거.
- 이중계산 직교 구현 확정.
- T 한 번 조건 충족.
- 파생 D 미구현 = 의도적 범위 제한.

### 5-3. 사용자 의도 반영

- P4 RESULT §8 "Adversarial 항목7(factor-2) 마감 해소" 확인 → entropy_coefficient 3경로 일관 동작.
- P4 이월 항목(x_MIT, 다온도 T² 곡률, LCO 파라미터, 비가역 3분해) 중 비가역 3분해·x_MIT·다온도 T² 곡률은 모두 **라벨됨** — 미구현 상태이나 사용자 의도 반영으로 분류.

---

## 섹션 6. P4 이월 항목 Ch2 정합·라벨 확인

| P4 이월 항목 | Ch2 대응 | 코드 상태 | 라벨 확인 |
|---|---|---|---|
| x_MIT=0.50 tier-C placeholder | Ch2 x_MIT 값 미명시 | LCO_MSMR_LIT x_MIT=0.50 | 코드 docstring L619에 "tier-C 시연 기본값, round-trip 피팅 前 placeholder" 라벨 확정 O |
| 다온도 T² 곡률 (Sommerfeld T-스케일) | Ch2 eq(2.22) S_e∝T | T_ref=298.15 동결 근사 | 코드 L663 "Sommerfeld T-스케일·eq:U1T2 ...미구현...라벨" 확정 O |
| LCO 시연 파라미터 tier-C | Ch2는 파라미터 신뢰도 언급 없음 | LCO_MSMR_LIT 내 주석 "tier-C" | L619 "출처 라벨" 확정 O |
| 비가역 3분해 | Ch2 lumped만 boxed | irreversible_heat lumped | L592 "3분해...Ch2에 boxed 식이 없다...lumped만 둔다" 확정 O |

모든 P4 이월 항목이 코드 내 inline 라벨 또는 docstring으로 명시됨. **라벨 확인 PASS**.

---

## 섹션 7. 요약 — 확정 갭 목록 및 리스크

### 확정 갭 (master 정정 대상)

| 갭 ID | 위치(코드줄·tex식) | 무엇이 | 맞는 형태 | 리스크 |
|---|---|---|---|---|
| **G1** | 코드 L659, Ch2 eq(2.22) | LCO 전자항이 T_ref=298.15 동결 → T-무관 상수. Ch2 Sommerfeld S_e∝T와 다온도 불일치 | 다온도 round-trip 피팅 단계에서 `func_dSe_molar(..., T, ...)` T 인자 전달로 T-선형 복원 | 중(단일T에서는 정확, 다온도 피팅 시 체계적 오차 가능) |
| **G3** | 코드 `entropy_coefficient` 시그니처, Ch2 eq(2.26-27) | 히스 분기별 $\partial U^{(d)}/\partial T$ 미구현. Ch2 파생 D 틀 제시 | `s` 인자 추가 후 분기별 ξ 계산 옵션 | 저(Ch2가 "틀만 제시, 완전 구현 범위 밖" 명시) |

### 근거미발견

| 항목 | 내용 |
|---|---|
| G4(단순식 인터페이스) | Ch2가 코드에 단순식 옵션을 요구하는지 명시 없음. 완전식 전용 구현이 불일치인지 미확인 |

### 의도적 근사·범위 제한 (갭 아님)

| 항목 | 내용 |
|---|---|
| G1 현재 상태 | P4 이월 "다온도 T² 곡률" 라벨됨. 단일T 정합 확인됨. 오류 아님 |
| G3 현재 상태 | Ch2 §6 "범위 밖" 명시. 미구현이 오류 아님 |
| 비가역 3분해 | Ch2 boxed 부재, lumped 근거 있음 |
| Ω 온도 의존 2차항 | Ch2 범위 밖 명시, 코드 미구현 일치 |

### 최중대 갭

**G1** — LCO 전자항 T-선형 Sommerfeld vs. T_ref 동결: 다온도 round-trip 피팅 단계에서 체계적 오차 원천. P4 이월 항목이지만 Ch2 eq(2.22)과 코드 사이 물리적 차이가 명확히 존재함.

---

## 부록: 충실도 매핑 요약표

| Ch2 항목 | 코드 심볼 | 1:1 매핑 | 비고 |
|---|---|---|---|
| eq:qrev $\dot Q_\rev = -IT\partial U/\partial T$ | `reversible_heat` L578 | **확정 O** | T 한 번 확인 |
| eq:weighted 완전식(+config) | `entropy_coefficient` L544 | **확정 O** | 두 조각 모두 |
| $g_j = \xi(1-\xi)/w_j$ | `g = xi*(1-xi)/w` L569 | **확정 O** | |
| config $(R/F)\ln[\xi/(1-\xi)]$ | `config = (R/F)*log(xi_c/(1-xi_c))` L571 | **확정 O** | |
| 파생 B 이중계산 직교 | dqdv 무가산 / entropy_coeff 가산 | **확정 O** | |
| 부호: 방전I>0·ΔS>0→흡열 | `return -float(I)*T*...` | **확정 O** | |
| $\dot Q_\irr = I(U_\oc-V)$ | `irreversible_heat` L588 | **확정 O** | lumped |
| seam(_effective_dS_rxn) | base: 항등, LCO: dSe 가산 | **확정 O** | |
| 하프셀 스코프(단일전극) | 전극 단독 계산 | **확정 O** | |
| 파생 D 히스 분기 | 미구현 | **갭 G3** | Ch2 "틀만" |
| Sommerfeld S_e∝T | T_ref 동결 근사 | **갭 G1** | P4 이월 |

---

*감사 드래프트 S2 완료. 코드/문건 수정 없음. master 정정 대상: G1(다온도 단계 과제), G3(파생 D 히스 분기, 옵션). 허위적발 없음.*
