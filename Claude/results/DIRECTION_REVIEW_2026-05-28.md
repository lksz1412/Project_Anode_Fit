# Direction Review 2026-05-28 — User Intent Clarification + Current Work Diagnosis + Restart Options

**Date**: 2026-05-28
**Trigger**: User verbatim 2026-05-28 (second statement) — explicit clarification of work objective + instruction to evaluate whether direction change is needed and to be prepared to **restart from scratch without forcing the existing work**.
**Authority**: User statement supersedes Charter / Charter Addenda 1 & 2 if direction change required.
**Output mode**: Review + Options + Recommendation. **No execution** until user GO.

---

## §1. User Intent Re-Statement (Verbatim Parsing)

### 1.1 Verbatim quote (2026-05-28)

> "피크의 면적은 어차피 추후 피팅의 영역이고, 현재는 꼬리의 거동에 대해 논리전개를 진행하면 되는데.
>
> LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히 피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 피크 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐가 달라지는것을 확인했다. 특히 온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는 현상이 관측되었어. 원래라면 그렇게 온도에 대해 약간 가우시안 피크 형상이 나타나고 더이상 진행이 안될 것으로 생각되는데 그 온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를 낮추는 효과가 있다고 봤고 그 유효 배리어의 논리를 확정하고 그 것을 이용해 피크의 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심이야."

### 1.2 Parsed intent elements

| # | Element | Verbatim phrase | Modeling implication |
|---|---|---|---|
| **I1** | **현 작업 초점 = 꼬리 거동** (피크 면적은 피팅 단계로 deferred) | "피크의 면적은 어차피 추후 피팅의 영역이고, 현재는 꼬리의 거동에 대해 논리전개를 진행하면 되는데" | Charter Addendum 2 §16.1 의 **O2 (피크 면적 온도 무관)** 는 본 phase 의 초점이 아님. **O3 (꼬리 모양 온도 의존)** 가 유일한 초점. |
| **I2** | 관측: 피크 = 상변이, 꼬리 = 늘어지느냐 빨리 떨어지느냐 변동 | "피크 부분이 상변이에 의해서 나타나는데... 피크 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐가 달라지는것을 확인" | 피크 = 상변이 신호, 꼬리 = relaxation 진행 미완성 (kinetic lag) 신호. |
| **I3** | 저온 = 꼬리 길고, 고온 = 꼬리 짧음 | "온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는" | reaction kinetics 가 T 와 함께 빨라짐 → 평형 도달 빠름 → 꼬리 짧음. Arrhenius-like T 의존성. |
| **I4** | ★ **평형 + 가우시안 peak 가 base 가정** | "원래라면 그렇게 온도에 대해 약간 가우시안 피크 형상이 나타나고 더이상 진행이 안될 것으로 생각" | 평형 분포 = **가우시안 형태** (logistic 도 erf 도 아닌 **가우시안**). 그 위에서 비평형 동역학이 추가. |
| **I5** | ★ **온도 배리어 + 전위 의존 유효 배리어 lowering** | "그 온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를 낮추는 효과가 있다고 봤고" | 활성화 자유에너지 `ΔG_eff = ΔG_a(T) - χ · A(전위)` 형태의 **2 인자 결합 배리어**. ver5 의 `eq:Geff` 가 정확히 이 구조. |
| **I6** | ★ **유효 배리어 논리 확정 + 꼬리 거동 해석 + 피팅 가능한 논리식 도출** | "그 유효 배리어의 논리를 확정하고 그 것을 이용해 피크의 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심" | **본 작업의 출발점 = 유효 배리어 식** + **본 작업의 종료점 = 꼬리 거동을 해석하는 피팅 가능한 식**. spine 의 중심이 **`ΔG_eff(T, A) → k(T, A) → dξ/dt → ξ(q) → dQ/dV 꼬리 모양`** 의 chain. |

### 1.3 User's explicit restart authorization

> "방향성이 크게 변경이 되는 경우 기존 문건을 어떻게 살려보겠다고 수정하면서 논리를 억지로 만들지 말고 다시 기초 작업부터 전부 다시할 각오를 하고 임해라"

- 억지 살리기 금지.
- 기초 재시작 허용 + 그 각오 의무.

---

## §2. Current Work Diagnosis Against User Intent

### 2.1 Inventory of current work (Phases E0~E4)

| Phase | Deliverable | Direction |
|---|---|---|
| E0 | Charter (9 sections) + Charter Addendum 1 §11 + Charter Addendum 2 §16 | governance |
| E1 | Spine redesign — `Q_ext → continuous ρ(μ; q, T) charge balance → V_n implicit → continuous reactivity Fredholm 2nd kind ρ evolution → dQ/dV` | structural |
| E2 | §1 + §2 of `chapter1_v0.1.tex` — intro + canonical 17 + derived 16 | notation |
| E3 | §3 + §4 — continuous μ + ρ(μ) interpretation + V_n / V_{n,app} / V_{n,drive} 3-way | conceptual |
| E4 | §5 — Eq.48 charge balance central equation derivation | derivation |

### 2.2 Alignment matrix (User intent I1~I6 vs Current work)

| Intent | Current work treatment | Alignment | Reason |
|---|---|---|---|
| **I1** 꼬리 거동 초점 | spine 의 final observable `dQ/dV` 이 §10 (Phase E8) 도달. 꼬리 거동 자체는 §11 (Phase E9) 의 C-rate/temperature section 이 다룰 예정 | **PARTIAL** | 꼬리가 명시적 spine 중심이 아니라 spine 의 derived 결과 |
| **I2** 피크 = 상변이, 꼬리 = lag | `ρ(μ; q, t)` 의 peak window 적분이 `ξ_j` (lag 표현 derived) | **OK** | 구조적으로 표현 가능 |
| **I3** 저T 길고 고T 짧음 | Charter Addendum 2 §16 의 O3 로 등재. Phase E6 의 `S_R(μ; T)` Arrhenius-like 가 본 현상 재현 예정 | **OK (deferred)** | Phase E6 구체화 대기 |
| **I4 ★** 평형 = 가우시안 peak | 현 spine 의 `ρ_eq(μ; q, T)` functional form 미지정. Phase E5 가 결정. **그런데 spine 자체는 가우시안 가정에 종속되지 않음** | **MISALIGNED** | 사용자는 specific 한 가우시안 모델, 나는 general continuous ρ. 추상화 수준 격차 |
| **I5 ★** 온도 배리어 + 전위 lowering 결합 = ΔG_eff | 현 spine 에 `ΔG_eff` 가 명시 X. derived 변수표 (Phase E1 §C) 에 `ΔG_{eff,j}` 가 "Phase E6 에서 `S_R(μ; T)` kernel structure 안에 embedded" 로만 등재 | **MISALIGNED** | 사용자는 ΔG_eff 가 spine 의 출발점, 나는 derived 결과로 격하 |
| **I6 ★** 유효 배리어 논리 → 꼬리 해석 → 피팅 가능한 논리식 | 본 spine 의 정밀화 단계 (`S_R` 구성 Phase E6 + Ref 6/7 적용 Phase E11) 가 결국 피팅 가능한 식 산출 예정. 그러나 **본 spine 의 출발점이 사용자 의도와 다름** | **MISALIGNED at root** | 사용자는 ΔG_eff → k → dξ/dt → dQ/dV 의 직접 chain 원함. 나는 Fredholm 2nd kind 적분식 우회 |

### 2.3 Critical alignment finding (★)

내가 만든 spine 의 **출발점이 사용자 의도와 본질적으로 다름**:

- **사용자 의도 spine**:
  ```
  ΔG_eff(T, A) [유효 배리어, 온도 + 전위 의존]
    → k(T, A) = ν · exp(−ΔG_eff / RT)  [Arrhenius 의 변형]
    → dξ/dt = k · [ξ_eq − ξ]  [relaxation 동역학]
    → ξ(q)  [방전 진행에 따른 진행률]
    → dQ/dV 꼬리 모양  [관측 가능]
  ```
  이는 사실 **ver5 + ver1_rechecked2 의 spine 과 본질적으로 동일** (step function 가정 부분만 제거).

- **내 spine** (Phase E0~E4 의 결과):
  ```
  Q_ext → Q_cell·q → 전하 보존식 [continuous ρ(μ; q, T)]
    → V_n implicit → V_{n,app}
    → Fredholm 2nd kind ρ evolution [K_n × S_R × (ρ_eq − ρ)]
    → ρ(μ; q, t) → dQ/dV
  ```
  사용자의 ΔG_eff 가 `S_R(μ; T)` kernel 안에 implicit. ξ_j 가 derived. spine 의 초점이 사용자가 원한 **유효 배리어** 가 아니라 **연속 분포의 적분식**.

### 2.4 Diagnosis result

| 평가 항목 | 결과 |
|---|---|
| **사용자 의도와 정합도** | **부분 부정합 (root level misalignment)** |
| **억지 살리기 가능?** | 가능 — Phase E5 의 ρ_eq 를 가우시안으로 + Phase E6 의 S_R 을 Arrhenius·χA-coupled 로 구성하면 표면적으로 정합. 그러나 spine 의 **출발점 자체가 ΔG_eff 가 아니라 ρ 의 continuous distribution** 이라는 사실은 변경 X. 결국 사용자가 보고 싶은 ``유효 배리어 논리식'' 이 spine 의 출발점이 아닌 부수 결과로 묻힘. |
| **사용자 명시 권고** | "기존 문건을 어떻게 살려보겠다고 수정하면서 논리를 억지로 만들지 말고 다시 기초 작업부터 전부 다시할 각오를 하고 임해라" — **억지 살리기 금지 명시**. |

→ **방향 변경 필요**.

---

## §3. Restart Options (A / B / C)

### Option A — 현 ρ(μ) spine 유지 + Phase E5/E6 에서 가우시안 ρ_eq + Arrhenius S_R 구성으로 사용자 의도 표면 정합

- **수정 범위**: Phase E5 (§6 ρ_eq 작성) 에서 functional form = 가우시안 명시 + Phase E6 (§7 S_R 작성) 에서 Arrhenius + χA 결합 명시.
- **장점**: Phase E0~E4 (1203 줄 LaTeX + 5 governance/result/json 파일) 완전 보존.
- **단점**:
  - spine 의 출발점이 여전히 ``전하 보존 + 연속 적분식'' 임. 사용자가 보고 싶은 ``유효 배리어 논리'' 가 spine 출발점이 아니라 §7 의 derived 결과로 묻힘.
  - **사용자 명시 "억지 살리기 금지" 위반** 가능성 큼.
  - 논문/특허 수준 정밀도 (Charter Addendum 1 §10.3) 차원에서, spine 자체가 사용자 hypothesis 와 일치하지 않으면 학술 가치 떨어짐.
- **권장도**: ★☆☆☆☆ — 명시 금지 사항 위반 위험.

### Option B — 부분 재작성 (Spine 출발점만 ΔG_eff 로 변경, Phase E1 ~ E4 의 일부 산출 보존)

- **수정 범위**:
  - Phase E1 spine 재설계 — 출발점을 `ΔG_eff(T, A)` 로 두고 dξ/dt → dQ/dV 의 직접 chain. ρ(μ; q, T) 는 부수 표현 (필요 시 도입).
  - Phase E2 §1 + §2 부분 보존 — 단 spine 식 boxed equation 교체 + canonical 변수 inventory 변경 (ΔG_a, χ, ν 등 spine 핵심으로 승격, ρ/S_R/K_n 부수로 격하 또는 제거).
  - Phase E3 §3 + §4 일부 보존 — 단 ρ(μ) 중심 서술 폐기, ξ_j 와 그 동역학 중심 서술로 변경.
  - Phase E4 §5 charge balance 폐기 — spine 출발점이 아니므로 부수 단원으로 격하 또는 제거.
  - Phase E5 ~ E11 마스터 로드맵 일부 재설계.
- **장점**: Phase E0 Charter + Phase E2 notation 의 일부 + Phase E3 의 V_n/V_{n,app}/V_{n,drive} 3 분리 등 재사용 가능 부분 유지.
- **단점**:
  - spine 출발점 변경이 본질적이라 사실상 chapter1_v0.1.tex 의 §5 폐기 + §1 + §2 절반 교체 + §3 + §4 일부 교체. 보존 비율 ~30%.
  - 보존 부분과 신규 부분이 섞이면 **문서 일관성 위험**. 사용자 5-28 명시 "억지 살리기 금지" 우려에 부분 해당.
- **권장도**: ★★★☆☆ — 가능하지만 일관성 위험.

### Option C — **기초부터 전부 재작성** (사용자 명시 권고 안)

- **수정 범위**:
  - 신규 Charter v2 작성 — ΔG_eff 중심 spine 명시.
  - 신규 master roadmap v2 작성 — 사용자 의도 정합 단계 (ΔG_eff 정의 → k 도출 → dξ/dt → dQ/dV 꼬리 모양 → 피팅식 도출).
  - 신규 `Claude/docs/graphite_ica_chapter1_v0.2.tex` 작성 — chapter1_v0.1.tex 보존 (덮어쓰기 X, supersession marker), 새 v0.2 처음부터.
  - Phase E0 ~ E12 + F1 ~ F5 의 step 재정의 (cumulative step 1221 부터 새 시리즈 시작).
- **장점**:
  - 사용자 명시 권고 정합.
  - spine 의 출발점이 사용자 hypothesis 와 일치 → 본 작업이 **사용자 박사학위 연구 (Refs 6, 7) 가 정확히 어디서 들어오는지** 명확해짐 (Refs 6, 7 는 dξ/dt = k(ξ_eq − ξ) 의 시간 적분형이 self-consistent integral equation 으로 환원될 때의 해법).
  - 논문/특허 수준 정밀도 (Charter Addendum 1 §10.3) 에 적합.
- **단점**:
  - Phase E0~E4 의 1203 줄 LaTeX + 6+ governance/result/json 파일이 모두 "이전 시도" 로 archive 됨 (보존되되 작업 baseline 에서 제거).
  - 신규 작성 분량 = chapter1_v0.2.tex 약 1500~2500 줄 + 17 phase 의 새 plan/result/json + 새 ledger.
  - 작업 시간 부담.
- **권장도**: **★★★★★** — 사용자 명시 권고 정합 + 학술 가치 정합.

---

## §4. Recommendation

### 4.1 Recommended option: **C (기초부터 전부 재작성)**

근거:
1. 사용자 verbatim 권고 정합 — "억지 살리기 금지, 기초부터 다시 할 각오".
2. spine 출발점 misalignment 가 본질적 — Option B 의 부분 재작성으로는 문서 일관성 위험.
3. 사용자의 박사학위 연구 (Refs 6, 7) 가 본 작업에서 어떤 위치를 차지하는지 명확해짐 — Option B/A 에서는 Refs 6, 7 가 ρ(μ) 적분식의 해법으로 사용되는데, 본 사용자 의도 모델 (ΔG_eff → k → dξ/dt → ξ(q)) 에서는 **시간 적분식 (Volterra-like) 의 해법으로 정확한 위치 부여** 가능 (즉 본 박사 연구 가 정확히 graphite ICA 의 꼬리 거동 해석에 들어오는 구조).
4. Charter Addendum 1 §10.3 (논문/특허 수준 정밀도) 차원에서 spine 자체가 사용자 가설과 일치해야 학술 가치.

### 4.2 Option C 의 보존 정책

- Phase E0~E4 의 모든 산출 (Charter, Addendum 1+2, master roadmap, phase plans/results/jsons, chapter1_v0.1.tex) 은 **물리적으로 보존** — 덮어쓰기 X.
- 각 파일에 supersession marker 추가 (별 marker md 파일) — 이전 시도임을 명시, 향후 참조 가능.
- 신규 작업은 별 파일 명 (예: `chapter1_v0.2.tex`, `Charter_v2`, `master_roadmap_v2`) 으로 시작.
- Cumulative step 은 1221 부터 새 시리즈 (1~1220 이 Option A spine, 1221~ 가 Option C spine — ledger 별 file).

### 4.3 Option C 의 신규 Charter v2 핵심 (preview)

- **Spine v2** (사용자 의도 정합):
  ```
  ΔG_eff(T, A) [유효 배리어, 온도 + 전위 의존]
    → k(T, A) = ν(T) · exp(−ΔG_eff / RT)  [Arrhenius]
    → dξ/dt = k · (ξ_eq − ξ)  [relaxation 동역학]
    → ξ_eq(V_n, T) = 가우시안 (또는 가우시안 적분형)  [평형 분포]
    → ξ(q, T, |I|, ξ_eq 이력)  [방전 진행]
    → dξ/dq · Q_{j,tot}  [상변이 j 의 dQ/dV 기여]
    → dQ/dV 꼬리 모양 (T 의존, |I| 의존)  [관측 가능]
    → 피팅 가능 논리식 (ΔG_a, χ, ν, ν의 T 의존, ξ_eq 의 σ 등)  [본 작업의 deliverable]
  ```

- **유효 배리어 정의**:
  ```
  ΔG_eff(T, A_j) = ΔG_{a,j}(T) − χ_j · A_j
  ΔG_{a,j}(T) = ΔH_{a,j} − T · ΔS_{a,j}  [Gibbs 자유에너지]
  A_j = F · (V_{n,app} − U_j(T))  [전위 보조 구동력, 사용자 명시: "극판 자체 전위에 따른 배리어를 낮추는 효과"]
  ```

- **꼬리 모양의 T 의존성 도출 (사용자 핵심 의도)**:
  - 평형 (ξ = ξ_eq) 시 dQ/dV 는 가우시안 형태 (사용자 명시).
  - 비평형 (ξ < ξ_eq) 시 lag = dξ/dt 가 충분히 못 따라잡음.
  - lag 의 크기 ∝ 1/k = (1/ν) · exp(ΔG_eff / RT).
  - 저 T → ΔG_eff / RT 값 큼 → k 작음 → lag 큼 → 꼬리 길게 늘어짐.
  - 고 T → ΔG_eff / RT 값 작음 → k 큼 → lag 작음 → 꼬리 빨리 떨어짐.
  - 전위 보조 χ_j · A_j 가 ΔG_eff 를 낮춤 → 같은 T 에서도 χ_j · A_j 가 크면 lag 작음.
  - 본 도출 chain 의 정량화 = 사용자 의도 핵심 deliverable.

- **Refs 6, 7 (사용자 박사 연구) 의 정확한 위치**:
  - dξ/dt = k · (ξ_eq − ξ) 를 시간 적분하면:
    `ξ(t) = ξ(0) + ∫_0^t dt' k(t') · [ξ_eq(t') − ξ(t')]`.
  - integrand 안에 `ξ(t')` 자기 등장 → **self-consistent integral equation**.
  - 일반적으로 ξ_eq, k 가 시간에 따라 변하면 정확 해는 numerical 만 가능.
  - 단, 특정 영역 (저 |I| + ξ_eq 의 slow variation) 에서는 Refs 6, 7 의 **비율 substitution** 으로 closed-form 해석해 도출 가능.
  - 이 closed-form 이 곧 사용자 의도의 **피팅 가능 논리식**.

### 4.4 Option C 의 작업 분량 추정

| 단계 | 분량 |
|---|---|
| Charter v2 (신규) | ~300 줄 |
| Master roadmap v2 (17~20 phase, 신규) | ~800~1200 줄 |
| chapter1_v0.2.tex (신규 본문) | ~1500~2500 줄 |
| Phase plan/result/json (각 phase) | 평균 ~500 줄 × 17 = ~8500 줄 |
| Supersession markers (Phase E0~E4 archive) | ~200 줄 |
| 합 | **~12,000 줄 신규** |

Option C 는 시간 부담 크지만 사용자 명시 권고 정합.

---

## §5. Decision Required (사용자 GO 사인 대기 항목)

### DQ-DIR-1 — 방향 변경 옵션 선택

| 선택지 | 의미 |
|---|---|
| **"Option A"** | 현 spine 유지, Phase E5/E6 에서 가우시안 ρ_eq + Arrhenius S_R 로 표면 정합 (★☆☆☆☆ — 명시 금지 위반 위험) |
| **"Option B"** | spine 출발점만 ΔG_eff 로 변경, 일부 재작성 (★★★☆☆ — 일관성 위험) |
| **"Option C"** | 기초부터 전부 재작성, chapter1_v0.2.tex 신규 (★★★★★ — 사용자 명시 권고 정합) |
| **"Option B + 구체화"** | B 안의 보존 비율 / 폐기 비율 사용자 직접 지정 |
| **"Option C 진행"** | 즉시 Charter v2 작성 시작 |

### DQ-DIR-2 — Option C 채택 시 Refs 6, 7 의 위치

내가 §4.3 에서 추정한 Refs 6, 7 의 위치 (시간 적분 self-consistent equation 의 비율 substitution closed-form) 가 사용자 의도와 정합하는지?

| 선택지 | 의미 |
|---|---|
| **"정확"** | 내 추정 정합 — 그대로 진행 |
| **"수정: ..."** | 다른 위치 또는 다른 해법 의도 |

### DQ-DIR-3 — Phase E0~E4 산출의 archive 방법

| 선택지 | 의미 |
|---|---|
| **"보존 marker"** | 각 파일에 SUPERSEDED marker 추가, 파일 보존 |
| **"별 폴더 archive"** | `Claude/archive/option_A_attempt/` 폴더에 일괄 이동 |
| **"git 만 보존"** | 파일 삭제, git 이력만 보존 |

### DQ-DIR-4 — Cumulative step 시리즈 처리

| 선택지 | 의미 |
|---|---|
| **"이어가기"** | Option C 의 신규 phase 가 cumulative step 1221 부터 |
| **"리셋"** | 새 시리즈 1 부터 (Option A 시리즈 1~1220 은 종료) |

---

## §6. 메타

- 본 검토 보고서는 [[feedback_planning_vs_execution]] 정합 — 사용자가 "검수 + 검토 + 방향 변경 결정" 요청. **작업 실행은 사용자 GO 사인 후**.
- 본 보고서가 명시한 모든 Option 의 산출물 분량 추정은 보수적 — 실제 더 줄어들 가능성 있음.
- [[feedback_document_protection_addendum_pattern]] 정합 — 기존 Charter, Addendum 1+2, master roadmap, phase results 모두 보존. supersession 시 새 marker 별 파일.
- **★ 본 보고서 자체는 ``작업 산출'' 이 아니라 ``방향 검토'' 산출** — Phase E5 진입 deferral 상태에서 작성.
- 사용자 GO 사인 받기 전까지 chapter1_v0.1.tex 및 모든 Phase E0~E4 산출은 **그대로 동결**.

---

## §7. ver5.tex 사용자 의도 기준 재검토

사용자 의도 (I4: 가우시안 peak + I5: 유효 배리어 = ΔG_a − χA + I6: 꼬리 거동 해석 피팅식) 안경으로 ver5.tex `Claude/docs/graphite_ica_dynamic_ver5.tex` Chapter 1 (line 46-526) 의 핵심 영역 재평가.

### 7.1 ver5 §6 (유효 장벽과 상변이 속도상수, line 203-250) — ★ 사용자 의도 spine 의 직접 구성 단원

| ver5 § | line | 식 | 사용자 의도 정합? |
|---|---:|---|---|
| §6.1 고유 활성화 자유에너지 | 204-211 | `Ga_def`: $\Delta G_{a,j}(T) = \Delta H_{a,j} - T \Delta S_{a,j}$ | **★ 직접 정합** (I5 의 ``온도에 의한 배리어''. Gibbs 자유에너지 표준 정의) |
| §6.2 전위 보조 구동력 | 212-219 | `A_simple`: $\mathcal A_j = s_{\phi,j} F [V_{n,\app} - U_j(T)]$ | **★ 직접 정합** (I5 의 ``극판 자체 전위에 따른 배리어 lowering'' 의 driving force 표현) |
| §6.3 유효 장벽 | 220-227 | `Geff`: $\Delta G_{\eff,j} = \Delta G_{a,j} - \chi_j \mathcal A_j$ | **★★★ 사용자 의도의 정수** (I5 verbatim ``유효 배리어'') |
| §6.4 속도상수 | 228-235 | `k_basic`: $k_j = \nu_j(T) \exp[-\Delta G_{\eff,j} / RT]$ | **★ 직접 정합** (Arrhenius, I6 ``꼬리 거동'' 의 동역학 핵심) |
| §6.5 속도 폭주 방지 | 236-250 | 방법 A: `max(ΔG_eff, 0)` [AP1] / 방법 B: `min(k_j, k_max)` [AP2] | **★ 부정합** (사용자 의도 = 부드러운 처리, ver5 의 step 처리 = anti-pattern) |

**진단**: ver5 의 §6.1-§6.4 는 사용자 의도와 완벽히 정합. **§6.5 만 step function 처리** 가 문제.

### 7.2 ver5 §5 (평형 진행률 ξ_{j,eq}, line 176-202)

| ver5 § | line | 식 | 사용자 의도 정합? |
|---|---:|---|---|
| §5.1 Logistic 표현 | 186-192 | `xi_eq_logistic`: $\xi_{j,\eq} = 1 / (1 + \exp[-(V_{n,\OCV} - U_j) / w_j])$ | **부정합** (logistic, 사용자 명시 = 가우시안) |
| §5.2 Erf 표현 | 193-199 | `xi_eq_erf`: $\xi_{j,\eq} = (1/2)[1 + \operatorname{erf}((V_{n,\OCV} - U_j) / (\sqrt{2} w_j))]$ | **★ 잠재적 정합** (erf 는 가우시안의 누적 적분 ⇒ $d\xi_{j,\eq}/dV = $ **가우시안 형태**. 사용자 명시 ``가우시안 피크 형상'' 의 직접적 표현) |

**진단**: ver5 의 **§5.2 erf 표현은 사실 사용자 의도와 정합**. dξ_eq/dV = 가우시안 이므로 평형 dQ/dV 가 가우시안 peak 가 됨 (사용자 명시).

→ **재해석**: Charter Addendum 1 §11.4 의 AP3 (logistic) 는 anti-pattern 정확하지만, AP4 (erf) 는 **사용자가 가우시안 분포를 직접 명시했으므로 OK-derived (물리 가정 기반)** 로 재분류 필요.

### 7.3 ver5 §7 (상변이 진행률 동역학, line 252-285)

| ver5 § | line | 식 | 사용자 의도 정합? |
|---|---:|---|---|
| §7.1 시간 영역 | 253-262 | `xi_ode_t`: $d\xi_j/dt = k_j \cdot (\xi_{j,\eq} - \xi_j)$ | **★ 직접 정합** (I6 의 relaxation 동역학) |
| §7.2 q 좌표 | 263-275 | `xi_ode_q`: $d\xi_j/dq = (Q_{\cell}/|I|) \cdot k_j \cdot (\xi_{j,\eq} - \xi_j)$ | **★ 직접 정합** (정전류 좌표 변환) |
| §7.3 해석 | 277-285 | C-rate 효과 2 경로 + 온도 효과 | **★ 직접 정합** (꼬리 거동의 정성 설명) |

### 7.4 ver5 §8 (장벽 분포 평균 동역학, line 286-324)

ver5 의 시도: 단일 k_j 가 꼬리를 충분히 만들지 못하면 **장벽 분포 $\rho_j(g)$ 평균** 으로 꼬리 길이 조정.

- 의도: 다양한 활성화 장벽 g 를 가진 sub-domain 들이 각각 k_j(g) 로 진행 → 평균.
- **사용자 의도와의 관계**: 가능한 confluence point — 단 사용자 명시는 "전위 의존 배리어 lowering" 이 1 차 메커니즘. 장벽 분포 평균은 보조적 (단일 k 가 부족할 때).

### 7.5 ver5 §9 (ICA 와 DVA 유도, line 325-366)

- dξ/dq → dQ_n/dq → dQ_n/dV_n,app (parameterized derivative).
- **★ 직접 정합** (피팅 가능 논리식 산출 단원).

### 7.6 ver5 Chapter 1 종합 평가

| 사용자 의도 element | ver5 Chapter 1 의 정합도 |
|---|---|
| I4 가우시안 peak | **§5.2 erf** = 가우시안 누적, 정합. §5.1 logistic 부정합. |
| I5 유효 배리어 (ΔG_a − χA) | **§6.1-§6.4** = 완벽 정합. §6.5 step 처리만 부정합. |
| I6 꼬리 거동 + 피팅 가능 논리식 | **§7 + §8 + §9** = 직접 정합. |

**ver5 Chapter 1 의 사용자 의도 정합도 = ★★★★☆** (5 중 4). **§5.1 logistic 폐기 + §6.5 step 처리 폐기** 만 하면 사용자 의도 spine 의 직접 구성이 가능. 나머지는 모두 살릴 가치.

### 7.7 ★ 본 사실의 의미

**내 Phase E0~E4 의 ρ(μ) continuous spine 은 ver5 Chapter 1 의 잘된 부분 (§6.1-§6.4 + §7 + §9) 을 우회한 것이다.** 사용자가 ``기존 1~5 전문건의 큰 문제점은 ... 적분을 모 아니면 도 즉 스텝펑션 형태로 가정'' 이라고 한 것은 **§5.1 logistic + §6.5 step 처리** 한정 비판이지, **§6.1-§6.4 의 유효 배리어 spine 자체 비판이 아니다**.

내가 잘못 일반화 했다.

---

## §8. ver1_rechecked2.tex 사용자 의도 기준 재검토

### 8.1 ver1_rechecked2 §6 (상변이 속도식, line 203-266)

| ver1_rechecked2 § | line | 식 | 사용자 의도 정합? |
|---|---:|---|---|
| §6.1 구동 전위와 apparent 전위의 구분 | 204-238 | V_n / V_{n,app} / V_{n,drive} 3 종 분리 | **★★★ 잘 정합** (사용자 의도 spine 의 명확화) |
| §6.2 유효 장벽 + 속도상수 + softplus | 240-266 | `Geff` (= ver5 §6.3 보존) + softplus `softplus_barrier` 정규화 | **★★★ 부분 정합** — Geff 는 정합, softplus 는 step 의 부드러운 버전이라 부정합 (smooth-step) |

### 8.2 ver1_rechecked2 §5 (평형 진행률, line 184-201)

| § | line | 식 | 정합? |
|---|---:|---|---|
| §5 본문 | 188-201 | `xi_eq_logistic`: logistic 식 직접 사용 | **부정합** (logistic, 사용자 명시 = 가우시안) |

### 8.3 ver1_rechecked2 §7 (진행률 동역학, line 268-318)

| § | 정합? |
|---|---|
| §7.1 시간 영역 | **★ 직접 정합** (relaxation 동역학) |
| §7.2 q 좌표 (정전류 한정) | **★ 직접 정합** + 휴지 처리 추가 |
| §7.3 초기 조건 + 전하 보존식 정합 | **★ 정합** (부수적, 전하 보존식의 일관성 확인) |

### 8.4 ver1_rechecked2 §4 (전하 보존식, line 118-182)

| § | 정합? |
|---|---|
| §4 전체 | **부수적** — 사용자 의도 spine 의 직접 구성 단원 아님. V_n 의 구체 결정 방식 (전하 보존식 implicit) 만 제공. 사용자 의도의 꼬리 거동 해석에는 보조적. |

### 8.5 ver1_rechecked2 종합 평가

| 사용자 의도 element | ver1_rechecked2 정합도 |
|---|---|
| I4 가우시안 peak | **부정합** (logistic 만 사용) |
| I5 유효 배리어 (ΔG_a − χA) | **★★★ 정합** (§6.2 보존 + softplus 만 부정합) |
| I6 꼬리 거동 + 피팅 가능 논리식 | **★★★ 정합** (§7 보존) |
| 추가 가치 | V_n / V_{n,app} / V_{n,drive} 3 분리 (사용자 의도 명확화) |

**ver1_rechecked2 의 사용자 의도 정합도 = ★★★☆☆** (5 중 3). ver5 보다 logistic 만 사용해 평형 분포가 더 부정합. 단 V_n 3 분리는 추가 가치.

### 8.6 두 ver 의 self-consistent loop (내 Phase B 진단) 의 위치

내가 Phase B 에서 진단한 Loop 1/2/3 (V_n implicit + DAE + Volterra-like) 는:

- ver5 에는 **없음** — V_n,OCV 가 외부 lookup 함수라 self-consistent loop 발생 X.
- ver1_rechecked2 에는 **있음** — V_n 을 전하 보존식 implicit 으로 격상한 결과 발생.

**중요**: 사용자가 ChatGPT 와의 검토 과정에서 발견한 ``특정 변수가 되먹이는 수식'' 은 **ver1_rechecked2 가 도입한 V_n implicit 의 결과 일 가능성** 이 큼. ver5 의 원래 spine (V_n,OCV 외부 lookup) 에서는 본 loop 가 발생 X.

→ **사용자가 Refs 6/7 의 비율 substitution 적용을 제안한 것은 ver1_rechecked2 의 V_n implicit 격상의 부작용을 해결하기 위한 것** 일 가능성.

또는 사용자가 의도한 spine 은 ver5 의 dξ/dt = k·(ξ_eq - ξ) 의 **시간 적분형 (Volterra-like)** 의 self-consistent integral equation 으로, V_n implicit 과는 별 관계일 수도.

이는 다음 §10 에서 정밀화.

---

## §9. 종합 정합도 표 (3 spine 후보 vs 사용자 의도)

| 사용자 의도 element | ver5 spine | ver1_rechecked2 spine | 내 Phase E0~E4 ρ(μ) spine |
|---|:---:|:---:|:---:|
| I4 가우시안 peak | ★ (§5.2 erf 사용 가능) | ✗ (logistic 만) | △ (functional form Phase E5 미정) |
| I5 유효 배리어 (ΔG_a − χA) | ★★★ (§6.1-§6.4) | ★★★ (§6.2 보존) | △ (S_R kernel 안에 implicit, spine 출발점 아님) |
| I6 꼬리 거동 + 피팅 식 | ★★★ (§7 + §8 + §9) | ★★★ (§7 보존) | △ (Phase E11 Ref 6/7 closed-form 후 도출 예정) |
| step function 회피 | ✗ (§5.1 + §6.5) | △ (§6.2 softplus) | ★★★ |
| 자기참조 적분식 적절 해법 | n/a (loop 없음) | n/a (loop 있음, 해법 명시 X) | ★★★ (Refs 6/7 적용) |
| spine 출발점이 사용자 의도와 일치 | ★★★ | ★★ | ✗ |
| 추상화 수준이 사용자 수준과 일치 | ★★★ | ★★ | ✗ (너무 추상) |

**결론**:
- ver5 spine 이 사용자 의도와 가장 정합 (특히 §6.1-§6.4 + §7 + §9).
- ver1_rechecked2 는 V_n 3 분리 + softplus 추가 가치 있으나 logistic 평형 + self-consistent loop 도입으로 복잡화.
- 내 ρ(μ) spine 은 step function 회피는 잘 했지만 사용자 의도 spine 출발점과 misalignment.

---

## §10. ★ 신 spine v2 제안 (사용자 의도 직접 정합)

### 10.1 신 spine v2 구조

```
[기초 정의 — ver5 §6.1-§6.4 보존, §6.5 폐기]

(A1) ΔG_a,j(T) = ΔH_a,j − T ΔS_a,j               [Gibbs 활성화 자유에너지, ver5 §6.1]
(A2) A_j = s_{φ,j} F (V_{n,app} − U_j(T))         [전위 보조 구동력, ver5 §6.2]
(A3) ΔG_eff,j(T, A_j) = ΔG_a,j(T) − χ_j A_j      [★ 유효 배리어, ver5 §6.3 = 사용자 의도 핵심]
(A4) k_j(T, A_j) = ν_j(T) exp(−ΔG_eff,j / RT)    [Arrhenius, ver5 §6.4]

[평형 분포 — ver5 §5.2 erf 보존, §5.1 logistic 폐기]

(A5) ξ_eq,j(V_n, T) = (1/2)[1 + erf((V_n − U_j(T))/(σ_j(T) √2))]
                                                   [erf 가 가우시안 누적 적분, dξ_eq/dV = 가우시안 ← 사용자 명시]

[동역학 — ver5 §7 보존]

(A6) dξ_j/dt = k_j · (ξ_eq,j − ξ_j)               [relaxation, ver5 §7.1]
(A7) dξ_j/dq = (Q_cell/|I|) · k_j · (ξ_eq,j − ξ_j) [정전류 q 좌표, ver5 §7.2]

[V_n 결정 — ver1_rechecked2 §6.1 의 V_n / V_{n,app} / V_{n,drive} 분리 보존]
[★ V_n 의 결정: 사용자 의도 검토 후 선택]
     선택 1: V_n,OCV(q, T) 외부 lookup (ver5 방식, self-consistent loop 없음)
     선택 2: 전하 보존식 implicit (rechecked2 방식, loop 1 발생 → Refs 6/7 적용 가능)

[꼬리 거동 도출 (사용자 의도 핵심)]

(A8) ξ_j(t) = ξ_j(0) + ∫_0^t dt' k_j(t') · (ξ_eq,j(t') − ξ_j(t'))   [(A6) 시간 적분형]
        → Volterra integral equation of 2nd kind (k 와 ξ_eq 가 시간 의존 시 self-consistent)

[Refs 6/7 (사용자 박사 연구) 의 정확한 적용 위치]

(A9) 비율 substitution: ξ(t)/ξ(t') ≈ ξ^simple(t)/ξ^simple(t')
       ξ^simple = k, ξ_eq 가 상수일 때의 closed-form (= 단순 exponential)
       → (A8) 의 closed-form 해석해 도출

[관측]

(A10) Q_n(q) = Q_bg(q) + Σ_j Q_{j,tot} ξ_j(q)     [용량식, ver5 §9.1]
(A11) dQ/dV_{n,app} = (dQ_n/dq) / (dV_{n,app}/dq) [ICA, ver5 §9]
(A12) dQ/dV 꼬리 모양 = (A9) closed-form 에서 T, χA 의존성 직접 도출
       → ★ 본 작업의 종료점 = 피팅 가능 논리식
```

### 10.2 신 spine v2 의 사용자 의도 정합도

| 사용자 의도 element | 신 spine v2 정합도 |
|---|:---:|
| I1 꼬리 거동 초점 | ★★★★★ (A12 = 종료점) |
| I2 피크 + 꼬리 = lag | ★★★★★ (A6 lag 표현) |
| I3 저 T 길고 고 T 짧음 | ★★★★★ (A4 의 T 의존 + A6 의 lag) |
| I4 가우시안 peak | ★★★★★ (A5 erf = 가우시안 누적) |
| I5 유효 배리어 (ΔG_a − χA) | ★★★★★ (A3 spine 출발점) |
| I6 꼬리 거동 → 피팅 가능 논리식 | ★★★★★ (A9 closed-form → A12) |
| step function 회피 | ★★★★☆ (§6.5 폐기, A5 erf 는 사용자 명시이므로 OK-derived) |
| Refs 6/7 의 정확한 위치 | ★★★★★ (A9, 시간 적분식 의 비율 substitution) |
| 추상화 수준이 사용자와 일치 | ★★★★★ (학부 전기화학 + 미적분 수준) |

**전체 = ★★★★★** (5/5). 사용자 의도와 본질적 정합.

### 10.3 신 spine v2 vs ver5 spine 의 차이

신 spine v2 는 사실 **ver5 spine 의 정제 버전**:
- ver5 §6.1-§6.4 그대로 보존 (A1-A4)
- ver5 §5.2 erf 채택 (A5) — §5.1 logistic 폐기
- ver5 §7 그대로 보존 (A6-A7)
- ver5 §6.5 step 처리 폐기 — 대신 ΔG_eff < 0 영역 의 처리는 사용자 박사 연구의 비율 substitution (A9) 로 우회
- ver5 §9 그대로 보존 (A10-A11)
- ★ ver5 에 없는 신규 = **(A8) 시간 적분형 명시 + (A9) Refs 6/7 비율 substitution closed-form**
- ★ ver1_rechecked2 의 V_n / V_{n,app} / V_{n,drive} 3 분리 보존 (선택 1 또는 2)

즉 **ver5 의 spine 을 보존하면서 step function 부분만 사용자 박사 연구로 대체** 하는 구조.

### 10.4 신 spine v2 와 ρ(μ) continuous spine 의 관계

내 Phase E0~E4 의 ρ(μ) continuous spine 은 신 spine v2 의 **연속 일반화** 로 위치할 수 있음:
- 각 transition j 의 ξ_j 가 분포 ρ_j(μ) 의 peak window 적분 → ρ(μ) = Σ_j ρ_j(μ) (composition).
- ρ_j(μ) 자체가 가우시안 (사용자 명시) — 즉 dξ_eq,j/dV_n 의 가우시안 형태에 대응.
- 그러나 **연속 일반화가 본 사용자 작업의 필수 요소가 아님**. 신 spine v2 의 discrete-j 표현이 사용자 의도와 직접 정합.

→ **결론**: ρ(μ) continuous spine 은 **선택적 일반화** 로 위치 (Chapter 1 의 advanced note 또는 appendix). spine 의 primary 표현은 discrete-j ξ_j 기반 (신 spine v2).

---

## §11. Option C 의 구체 진행 안 (사용자 GO 시)

### 11.1 archive 전략

| Phase E0~E4 산출 | archive 방법 |
|---|---|
| `Claude/docs/graphite_ica_chapter1_v0.1.tex` (1203 줄) | 보존 + supersession marker `chapter1_v0.1_SUPERSEDED.md` |
| Charter + Addendum 1 + Addendum 2 | 보존 + supersession marker — 단 Addendum 1 §11 (Writing Precision Standard) + Addendum 2 §16 (O1-O3 motivation) 은 신 Charter v2 에 흡수 |
| Master roadmap (master_roadmap.md) | 보존 + supersession marker — 신 master_roadmap_v2.md 작성 |
| Phase E0~E4 results / json / phase plans | 보존 그대로 (이전 시도의 사실 기록) |
| `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` | 보존 + 후속 ledger 는 별 파일 `PHASE_E_F_EXECUTION_LEDGER_v2.md` |

### 11.2 신 Charter v2 핵심

신 Charter v2 (`PHASE_E0_v2_..._RESULT.md`) 는 다음을 포함:

1. **Objective**: 사용자 의도 I1-I6 verbatim 명시 + 신 spine v2 (A1-A12) 그대로 채택.
2. **Anti-pattern list**: ver5 §5.1 logistic + ver5 §6.5 step 처리 + ver1_rechecked2 §5 logistic. 단 erf (가우시안 누적) 는 OK-derived (사용자 명시 가우시안 분포의 직접 표현).
3. **Allowed-pattern**: 신 spine v2 의 A1-A12 전체. ver5 §6.1-§6.4 + §7 + §9 의 보존 + Refs 6/7 의 시간 적분식 적용.
4. **Smooth-limit rule**: 잔존 (Phase E0 §5 동일).
5. **Writing Precision Standard**: Charter Addendum 1 §11 그대로 흡수.
6. **Physical Phenomenon Motivation**: Charter Addendum 2 §16 그대로 흡수 + I1 (꼬리 거동 초점) 우선순위 명시.
7. **Audit Dim #11**: 잔존 + AP4 (erf) 재분류 (가우시안 누적 = OK-derived).

### 11.3 신 master_roadmap_v2 핵심

phase 구조 (cumulative step 1221 부터 또는 새 시리즈 1 부터, DQ-DIR-4):

| Phase v2 | 이름 | 사용자 의도 element |
|---|---|---|
| E0_v2 | Foundation reset v2 + Charter v2 + 신 spine v2 lock | I1-I6 |
| E1_v2 | Spine redesign v2 (A1-A12 명시) | I5 (spine 출발점) |
| E2_v2 | §1+§2 (목적, 기호, 단위) — 사용자 의도 그대로 명시 | I1 |
| E3_v2 | §3 흑연 staging (discrete-j ξ_j 기반) + §4 V_n 결정 방식 선택 | (보조) |
| E4_v2 | §5 유효 배리어 ΔG_eff 정의 (A1-A3 정식 유도) | **I5 spine 핵심** |
| E5_v2 | §6 평형 분포 ξ_eq = erf (A5 도출) | **I4 가우시안 peak** |
| E6_v2 | §7 속도상수 k = Arrhenius (A4 + ΔG_eff 결합) | **I3 + I5 결합** |
| E7_v2 | §8 진행률 동역학 dξ/dt (A6-A7) | I6 동역학 |
| E8_v2 | §9 시간 적분형 (A8) + Volterra integral 형식 명시 | **★ Refs 6/7 적용 준비** |
| E9_v2 | §10 ★ Refs 6/7 비율 substitution closed-form 도출 (A9) | **★ 사용자 박사 연구 정확 적용** |
| E10_v2 | §11 ICA/DVA 관측식 + 꼬리 거동 해석 (A10-A12) | **★ I1 + I6 종료점** |
| E11_v2 | §12 피팅 가능 논리식 + 식별성 | I6 종료점 |
| E12_v2 | §13 ver.2 인계 + 자기 검수 + 참고문헌 | 종합 |
| F1_v2 ~ F5_v2 | 빌드 + 검수 + 정정 + 종료 | n/a |

**Phase 수 = 17 (E0_v2 ~ E12_v2 + F1_v2 ~ F5_v2)**, master roadmap 과 동일 구조이나 phase 내용이 신 spine v2 정합.

### 11.4 신 chapter1_v0.2.tex 핵심 차이

| chapter1_v0.1.tex (현재) | chapter1_v0.2.tex (Option C) |
|---|---|
| spine = `Q_ext → ρ(μ) charge balance → V_n implicit → Fredholm 2nd kind ρ evolution → dQ/dV` | spine = `ΔG_eff(T, A) → k(T, A) → dξ/dt → ξ(q) → dQ/dV 꼬리 모양 → 피팅식` |
| primary state = ρ(μ; q, T) continuous | primary state = ξ_j(q, T) discrete (ver5 보존) |
| §3 = 연속 μ 도입, §4 = V_n 3 분리, §5 = 전하 보존식 | §3 = 흑연 staging (discrete-j), §4 = 유효 배리어 ΔG_eff (★ 출발점), §5 = 가우시안 평형 분포 + erf, §6 = 속도상수 Arrhenius, §7 = 진행률 동역학, §8 = 시간 적분 + Volterra, §9 = Refs 6/7 적용 (★ 사용자 박사 연구), §10 = ICA/DVA + 꼬리 거동 해석 + 피팅식 |
| Refs 6/7 = ρ(μ) 적분식의 해법 | Refs 6/7 = **ξ_j 시간 적분식 (Volterra) 의 비율 substitution closed-form** ← 사용자 의도 정확 정합 |

---

## §12. 갱신된 Decision Required

### DQ-DIR-1 갱신: Option C 진행 결정

신 spine v2 (§10) 채택 + chapter1_v0.2.tex 신규 작성 진행?

| 선택지 | 의미 |
|---|---|
| **"Option C, 신 spine v2 채택"** | 즉시 Charter v2 + master roadmap v2 + chapter1_v0.2.tex 신규 시작 |
| **"신 spine v2 의 정정: ..."** | spine v2 의 A1-A12 중 어느 부분 수정 |
| **"V_n 결정 = 선택 1 (외부 lookup)"** | (§10.1) V_n,OCV 외부 lookup 채택, self-consistent loop 회피 |
| **"V_n 결정 = 선택 2 (전하 보존식 implicit)"** | (§10.1) ver1_rechecked2 방식 채택, loop 1 발생 → Refs 6/7 V_n 에도 적용 |

### DQ-DIR-2 갱신: Phase E0~E4 산출의 archive

§11.1 의 archive 전략 (supersession marker + 보존) 채택?

### DQ-DIR-3 갱신: cumulative step 시리즈

| 선택지 | 의미 |
|---|---|
| **"신 시리즈 1 부터"** | E0_v2 = step 1, E1_v2 = step 81, ... (1~1220 시리즈는 종료) |
| **"이어가기 1221 부터"** | E0_v2 = step 1221, ... |

### DQ-DIR-4: ver5 §8 (장벽 분포) 처리

신 spine v2 에서 ver5 §8 (장벽 분포 평균) 는?

| 선택지 | 의미 |
|---|---|
| **"폐기"** | 단일 k_j relaxation 으로 충분 가정, 장벽 분포 평균 미사용 |
| **"보조 단원으로 유지"** | chapter1_v0.2.tex 의 advanced note 또는 appendix 로 보존 |
| **"신 spine v2 의 일반화로 포함"** | 신 spine v2 의 A8 시간 적분형이 장벽 분포 평균을 자연 포함하는 형태로 일반화 |

### DQ-DIR-5: 추상화 수준

신 spine v2 의 ρ(μ) continuous 일반화는?

| 선택지 | 의미 |
|---|---|
| **"필요시만"** | discrete-j ξ_j 가 primary, 연속 일반화는 Chapter 1 의 advanced note (선택적) |
| **"Chapter 1 본문에서 동시 제공"** | discrete-j + continuous 양자 표기, 사용자 선택 |
| **"폐기"** | 연속 일반화 미사용 (Chapter 1 에서 ρ(μ) 미등장) |

