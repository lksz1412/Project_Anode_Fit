# Charter Addendum 2 — Physical Phenomenon Motivation (Tail Temperature Dependence)

**Date**: 2026-05-28
**Format**: [[feedback_document_protection_addendum_pattern]] §"Addendum"
**Supersedes**: nothing (Charter body and Addendum 1 unchanged)
**Amends**: `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md` — adds §16 (Physical Phenomenon Motivation) as a normative section that anchors the Chapter 1 to a specific set of experimental observations.
**Authority**: User statement 2026-05-28 verbatim.

## Reason

User verbatim 2026-05-28 (received after Phase E4 closure):

> "혹시 몰라서 작업되어야하는 내용을 다시 간략히 제공할게.
>  LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히
>  피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 피크의 충
>  면적은 동일하겠지만 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐가 달라지는것을
>  확인했다. 특히 온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로
>  짧게 끝나는 현상이 관측되었어. 그래서 현재 그것의 뒷받침하는 논리를 구하기
>  위해서 열역학의 관점으로 해당 이슈를 검토 시키는거야. 이 부분을 염두에 두고
>  작업을 계속 해줬으면 좋겠어."

This statement provides the **experimental phenomenon that the Chapter 1 must explain**. Without it, the new spine (continuous μ, ρ, S_R, Ref 6/7 ratio-substitution) is mathematically rigorous but physically motivationless. With it, every spine element gains a target observable to reproduce.

## §16. Physical Phenomenon Motivation (New, Normative)

### 16.1 Three observed regularities (must be reproduced by the rebuilt Chapter 1)

Based on user experimental observation 2026-05-28, the rebuilt Chapter 1 must reproduce — at minimum — the following three regularities of the graphite anode ICA `dQ/dV` curve.

| # | Observation | Quantity that captures it |
|---|---|---|
| **O1** | **피크 위치** — `dQ/dV` peaks at chemical potentials corresponding to specific graphite staging transitions | center of `ρ_eq(μ; q, T)` peak windows (`U_j(T)` legacy parameter) |
| **O2** | **피크 총 면적 일정 (온도 무관)** — for a given phase transition `j`, the integrated peak area (total Li transferred per transition) is invariant under temperature change | `Q_{j,tot}` legacy parameter = `∫_{peak_j} dμ · [ρ_eq(μ; q=1, T) − ρ_eq(μ; q=0, T)] · n(μ)` must be temperature-independent (or weakly dependent only via Li-host coupling) |
| **O3** | **★ 꼬리 모양 온도 의존성** — at low temperature the peak tail (high-voltage side after the peak center) is long; at high temperature the tail is shorter | tail shape governed by reactivity-kernel `S_R(μ; T)` temperature dependence — low `T` → slow reactivity → ξ(μ) lags equilibrium → long tail in `dQ/dV`; high `T` → fast reactivity → tight following → short tail |

### 16.2 Mechanistic interpretation under the new spine

- **O1 (peak position)** is a property of `ρ_eq(μ; q, T)` and is essentially preserved between ver5, rechecked2, and the new Chapter 1.
- **O2 (peak area invariance)** is a **structural constraint** on `ρ_eq` — Phase E5 must explicitly enforce that the per-peak integrated area is temperature-independent (or document the small Li-host coupling that breaks invariance).
- **O3 (tail temperature dependence)** is **the load-bearing observable for distinguishing the rebuild from legacy ver5 step-function model**:
  - In ver5, the tail was modeled by ad hoc `max(., 0)` barrier (AP1) + logistic equilibrium (AP3) — i.e., step-function components combined to mimic a tail. This forced the tail shape to follow the step-function family rather than the underlying reaction-kinetic family.
  - In the rebuilt Chapter 1, the tail emerges naturally from the **continuous reactivity kernel `S_R(μ; T)`**'s temperature-dependent relaxation rate — Phase E6 must construct `S_R(μ; T)` such that decreasing `T` increases the relaxation time and produces a longer tail in `dQ/dV`.
  - The Fredholm 2nd kind ratio-substitution method (Refs 6, 7) then provides the closed-form analytical expression for the resulting `ρ(μ; q, t)`, from which `dQ/dV` is derived in §10 / Phase E8.

### 16.3 Thermodynamic framework consequence

The phenomenon O3 establishes the rebuild as a **thermodynamics + kinetics joint analysis** rather than a pure equilibrium thermodynamics analysis:

- Pure equilibrium thermodynamics gives `ρ_eq(μ; q, T)` with peak-position and peak-area regularities — explains O1 and O2.
- Kinetics (governed by `S_R(μ; T)` reactivity kernel + Eq. 49 Fredholm 2nd kind ρ-evolution) explains the departure `ρ − ρ_eq` and hence the tail shape — explains O3.
- O3's temperature dependence comes from the **Arrhenius-like temperature dependence of `S_R(μ; T)`** that Phase E6 must construct.

### 16.4 Affected Charter sections and downstream phases

This Addendum binds the following Charter/master-roadmap sections:

- **Charter §1 (Objective)** — augmented with "must reproduce O1, O2, O3 observations" (implicit; this Addendum makes it explicit).
- **Master roadmap Phase E5 (§6 ρ_eq writing)** — must enforce O1 (peak position) and O2 (peak area invariance) explicitly in `ρ_eq(μ; q, T)` parameterization.
- **Master roadmap Phase E6 (§7 S_R + K_n)** — must construct `S_R(μ; T)` to produce O3 (low-T long tail, high-T short tail) via temperature-dependent relaxation rate. Arrhenius-like form (`exp(−ΔG_a / RT)` skeleton) is a natural starting point; explicit derivation in Phase E6.
- **Master roadmap Phase E8 (§10 ICA/DVA derivation)** — must derive `dQ/dV` from `ρ(μ; q, t)` and explicitly demonstrate O1, O2, O3 reproduction in qualitative terms.
- **Master roadmap Phase E9 (§11 C-rate, temperature, EMG)** — temperature section must explicitly cite O3 as the motivating observable and derive the tail-length temperature dependence.
- **Master roadmap Phase E11 (§17 Ref 6/7 application)** — closed-form `ρ(μ; q, t)` from ratio substitution must yield a `dQ/dV` shape whose tail behavior follows O3.

### 16.5 New audit hook (Dim #11 extension)

Add a new check to Charter §6 Audit Dim #11 Pass 1 — applicable from Phase E5 onward:

| Check | Pass criterion |
|---|---|
| Section claims to model `dQ/dV` peak/tail behavior without referencing O1/O2/O3 | WARN — add explicit cross-reference to Addendum 2 §16.1 |
| Section introduces temperature dependence without addressing O3 | WARN — clarify whether the new T-dependence explains, contradicts, or is orthogonal to O3 |
| `ρ_eq` parameterization breaks O2 (peak area invariance) without disclosure | FAIL — either fix or document deviation |
| `S_R(μ; T)` construction does not produce O3 (low-T long tail) in qualitative limit | FAIL (Phase E6 specific) |

### 16.6 Decision Queue update

| ID | Item | Status before Addendum 2 | Status after |
|---|---|---|---|
| DQ-G3 (originally DQ1) | ChatGPT 의 "큰 논리 오류" 정체 | 사용자 결정 대기 | **부분 해소** — ChatGPT 가 step function 가정 (AP1 + AP3 등) 으로 O3 의 tail 온도 의존성을 표현하려다 발생한 misalignment 가 본질일 가능성 강해짐. 완전 확정은 사용자 cross-check 후. |
| DQ-G2 | μ as Li/Li⁺ electrochemical potential | 사용자 결정 대기 | unchanged (Phase F3) |

### 16.7 Backward application note

- Phases E0–E4 deliverables are NOT retroactively re-audited under §16. Their content (governance + charge balance derivation) does not depend on O1/O2/O3 directly.
- Phase E5 onward is bound by §16.1–§16.5.
- Phase E2 §1 (문서의 목적과 원칙) may receive a forward-reference update to §16 in a future Chapter 1 revision (v0.2 or later), but no in-place edit is performed under [[feedback_document_protection_addendum_pattern]].

## §17. Effect On Master Roadmap

- Master roadmap `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md` is not modified.
- Phase E5–E11 detailed plans (which are written at phase entry per RO_SkillDict pattern) must each include a §"§16 motivation cross-reference" clause.
- Test Plan T-E5 onward in each phase plan must include items verifying O1/O2/O3 reproduction.

## §18. Re-validation

- Phases E0–E4 PASS status remains valid; their scope is governance + charge balance, not directly tied to O1/O2/O3.
- Charter Addendum 1 §11 (Writing Precision Standard) remains in force; §16 is additive, not conflicting.
- Chapter 1 v0.1 source file §1–§5 content is preserved; §6 onward will be written under both Addendum 1 §11 and Addendum 2 §16.

## §19. Ledger Update

Add a row to `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` Updates table:

| 2026-05-28 | Charter Addendum 2 | 사용자 5-28 실험 현상 정보 (피크 면적 온도 무관 + 꼬리 모양 온도 의존: 저온 길고 고온 짧음, 열역학 관점 검토 요청) 영구 반영. Charter §16 (Physical Phenomenon Motivation O1-O3) 신설. Phase E5 부터 ρ_eq + S_R 구성이 O1/O2/O3 재현 필수. DQ-G3 (ChatGPT 큰 논리 오류) 부분 해소 — step function 가정으로 O3 tail 온도 의존성 표현 시 misalignment 발생이 본질일 가능성. |
