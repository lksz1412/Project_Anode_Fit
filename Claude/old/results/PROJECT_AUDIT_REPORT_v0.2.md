# Project_Anode_Fit — Phase A~D 종합 Audit 보고서 v0.2

작성일: 2026-05-27
양식: [[feedback_document_protection_addendum_pattern]] §"Supersession"

## Supersedes

- `Claude/results/PROJECT_AUDIT_REPORT.md` (v0.1, commit `a63378f`)
- 사유: v0.1 의 §3 (부족) · §4 (잘못) · §5 (해결) 가 사용자 5-27 critical 피드백 (3 항목) 을 누락. 본 v0.2 가 supersede.
- v0.1 본문은 보존 (별 supersession marker 작성). 본 v0.2 가 향후 참조 기준.

## 사용자 5-27 critical 피드백 (3 항목, 본 v0.2 추가 진단의 출발점)

1. **계획서 수준 부족** — v0.1 계획서 (436 줄, 2 phase, 17 step) 가 RO_SkillDict codex 계획서 (master roadmap 1763 줄, 16 phase, 1000+ step) 의 **약 1/5 수준**. 디테일·방향성 모두 부족.
2. **Ref 6, 7 DOI 사용자 떠넘김** — JCP DOI `10.1063/1.5000882` 따라가서 외부 검색이 내 일. 사용자에게 묻기 X. v0.1 의 DQ-E2 가 잘못된 위임.
3. **★ ver1~5 의 본질 문제 진단 실패** — 사용자 verbatim "적분을 모 아니면 도 즉 스텝펑션의 형태로 가정하여 모사 대상 시스템의 특성을 완전 무시" 가 본질 문제. 본 v0.1 의 Phase B self-consistent loop (Loop 1/2/3) 진단은 **표면 문제**. 본질은 step function 가정. 본 정독으로도 잡지 못함.

## 1. 파악한 것 (v0.1 §1 + 본질 진단 추가)

v0.1 §1.1 ~ §1.4 의 파악은 유지. **단 §1.3 (self-consistent 되먹임 정체) 의 위치 재해석** + **§1.5 신설 (step function 가정 의 본질 문제)**.

### 1.3 재해석 — Self-consistent loop = **표면 문제** (본질 아님)

v0.1 §1.3 에서 Phase B 의 Loop 1/2/3 진단을 "사용자 verbatim '되먹임이 들어간 적분식' 의 정확 매칭" 으로 결론. **이는 부분 정확 + 본질 누락**.

사용자 5-27 verbatim:
> "기존 1~5 전문건이 포함된 버전의 큰 문제점은 한계 어쩌구 하면서 적분을 모아니면 도 즉 스텝펑션의 형태로 가정하여 우리가 모사해야하는 시스템의 특성을 완전 무시한채 논리 전개를 진행하여 시작 점부터 글러 먹었었다는 문제가 있었다. 1만 있는 문건은 1~5의 잘못된 근간을 고치고자 진행된 문건인데 검토를 10번을 넘게 시켰는데 그 때마다 반복해서 문제가 계속 검출 되어 도저히 쓸수가 없는 상황이었다. 그 문제중 하나가 특정 변수를 되먹이는 수식이 나왔다길래 그것을 해결할 방법으로 내가 박사학위 하는동안 사용했던 Fredholm eq of 2nd kind의 해법을 참고하면 어떻겠는지 제시했던것이다."

**재해석**:
- **본질 문제** = ver1~5 전문건의 **step function 가정** (적분을 "모 아니면 도" 형태로 가정 → 시스템 특성 완전 무시). 시작점부터 글러먹음.
- **재작성 (ver1_rechecked2)** = ver1~5 의 잘못된 근간 (= step function 가정) 을 고치고자 진행. 10 회 넘는 검토 → 매번 문제 검출 → 도저히 쓸 수 없음.
- **그 검출된 문제 중 하나** = **특정 변수의 되먹임 (self-consistent loop)** — v0.1 의 Loop 1/2/3 진단이 이 부분에 정확 매칭.
- **사용자가 제시한 해법** = 본인 박사학위 연구 (JCP 2017 + Ref 6, 7) 의 **Fredholm equation of 2nd kind 해법** — 두 가지 동시 해결 가능성:
  - (a) self-consistent loop 의 closed-form 해 (v0.1 의 §1.4 진단)
  - (b) **step function 가정 회피** (continuous reactivity kernel `S_R(r, μ)` continuous in r — Phase D 정독 §II.C 의 long-range reaction sink 처리)

→ 즉 **v0.1 은 (a) 만 잡고 (b) 를 놓침**. (b) 가 본질.

### 1.5 신설 — Step function 가정 의 본질 진단

ver5 Chapter 1 + Chapter 2~5 + ver1_rechecked2 모두에 다음 step function 가정의 흔적:

#### 1.5.1 ver5 Ch1 §6.5 "속도 폭주 방지" 의 방법 A (line 240-245)

```latex
\Delta G_{\eff,j}^{+} = \max\left[\Delta G_{\eff,j}, 0\right]
\quad \Rightarrow \quad
k_j = \nu_j(T) \exp\left[-\Delta G_{\eff,j}^{+}/RT\right]
```

- `max(ΔG_eff, 0)` = **ReLU = step function** (음수 영역 0, 양수 영역 identity)
- ΔG_eff < 0 (강한 구동력) 영역에서 k_j 가 ν_j (상한) 로 잘림 — 모 아니면 도

#### 1.5.2 ver5 Ch1 §6.5 방법 B

```latex
k_j = \min\left[\nu_j(T) \exp(-\Delta G_{\eff,j}/RT), k_{j,\max}\right]
```

- `min(..., k_max)` = **saturation step** (k_max 이상 = k_max 로 자름)

#### 1.5.3 ver5 Ch1 의 평형 진행률 ξ_{j,eq} 의 본질

```latex
\xi_{j,\eq}(q,T) = 1 / (1 + \exp[-(V_{n,\OCV}(q,T) - U_j(T))/w_j(T)])  % Logistic, Eq. xi_eq_logistic line 188
```

- Logistic = step function 의 부드러운 버전 (sigmoid). w_j → 0 한계에서 정확히 step.
- 본질: "전위 U_j 보다 낮으면 transition X, 높으면 transition O" 의 binary state 가정
- 실제 graphite staging 은 thermodynamic phase coexistence + continuous chemical potential 변화 → step function 합으로 분해 부적합

#### 1.5.4 ver5 Ch1 의 N_p 개 discrete transition 분해 자체

- "흑연 staging 을 N_p (보통 3 ~ 4) 개의 effective transition 으로 분해" (§3 흑연 staging, line 137-150)
- 각 transition 이 독립 진행률 ξ_j 로 모델링 + 각 ξ_j 가 logistic·erf 의 합
- 실제 graphite 는 **continuous staging** + **공존 phases** + **gradient chemical potential** 시스템
- discrete N_p × logistic 합 = **piecewise step approximation** 의 부드러운 버전

#### 1.5.5 ver1_rechecked2 의 부분 개선 + 잔존 문제

rechecked2 의 step 가정 개선 시도:
- §6.2 softplus regularization `Δ G_eff^+ = ε_G·ln[1 + exp(ΔG_eff/ε_G)]` (Eq. softplus_barrier line 255) — ver5 의 `max(ΔG_eff, 0)` 를 **부드러운 step (smooth ReLU)** 으로 대체
- §8 장벽 분포 support `g ≥ 0` (Eq. rho_support line 322) + softplus — ver5 의 `-∞ ~ +∞` 보다 물리적 정합

**잔존 문제** (사용자 verbatim "10 회 넘는 검토에도 문제 계속 검출"):
- 평형 진행률 ξ_{j,eq} 는 여전히 logistic (line 188-193) — 본질적 step 합
- N_p 개 discrete transition 분해 그대로
- 즉 rechecked2 가 **수치 안정성 (softplus)** 은 개선했지만 **모델 가정의 본질 (continuous vs discrete)** 은 변경 X
- 그 결과 발생한 추가 문제 = self-consistent loop (Loop 1/2/3 — v0.1 진단)

#### 1.5.6 Ref 6, 7 / JCP 2017 의 본질적 해법 = continuous reactivity

JCP 2017 §II.A `Reaction-diffusion model` (line 60-90):
- 입자 위치 r 에 대해 `recombine at a rate S_R(r)` — **continuous in r**
- §II.B (line 112-225) 의 `δ-function reaction sink` 는 special case (contact reaction)
- **§II.C (line 193-275)** 의 `long-range reaction sink functions` 가 본 paper 의 핵심 = continuous reactivity
- Ref 6, 7 의 비율 substitution 기법 = 이 continuous reactivity 의 self-consistent integral equation 의 closed-form 해

→ **graphite 적용 시 본질 해결**:
- discrete N_p transition → **continuous staging chemical potential μ(q, T)** 도입
- discrete `ξ_j` → **continuous reactivity distribution** `S_R(μ, T)`
- step (max / min / logistic) → **continuous kernel** (Marcus-like 또는 Bazant Cahn-Hilliard-like)
- self-consistent loop → ref 6, 7 의 비율 substitution 으로 closed-form

**이게 v0.1 이 놓친 본질**.

## 2. 잘된 것 (v0.1 §2 유지 + 보강 없음)

v0.1 §2 의 5 영역 (정독 / 양식 / audit / 학습 / 작업 흐름) 모두 유효. 사용자 5-27 비판은 작업 흐름·양식·audit 자체에 대한 비판 아님. **정독·audit 도구 의 정상 작동에도 불구하고, 정독 깊이 와 진단 의도 가 본질을 잡지 못함** (= §4 의 잘못 으로 분류).

## 3. 부족한 것 (v0.1 §3 + 신규 3 항목)

v0.1 §3.1 ~ §3.5 (5 항목) 유지 + **신규 3 항목**:

### 3.6 (★ 본질) Step function 가정 의 직접 진단 실패

본 정독에서 ver5 §6.5 `max(ΔG_eff, 0)` 와 §5 logistic 식 모두 정독했음에도, 이를 **사용자가 의도한 "step function 가정 = 모사 대상 시스템 특성 완전 무시"** 와 연결 못함. Phase B audit 에서 **본질적 모델 가정** 차원이 audit 9 차원 중 부재 (시그너처·데이터 흐름·컨벤션 등은 있지만 "**모델 가정 적합성**" 차원 없음).

해결: 본 v0.2 §5.1 에 audit 차원 #11 (모델 가정 적합성) 추가 권고. 향후 LaTeX 문건 작업 시 자동 적용.

### 3.7 RO_SkillDict 수준 대비 계획서 granularity 부족

v0.1 = 2 phase × 17 step. RO_SkillDict master roadmap = 16 phase × 1000+ step (각 step 단일 동작 1 줄). **약 1/5 ~ 1/60 수준** 의 granularity.

세부 비교:
- v0.1 의 "Step 20: §1 (문서의 목적과 원칙) + §2 (기호와 단위 컨벤션)" 한 줄 = **거시 명령** (실제로는 10~30 개의 단일 동작 포함)
- RO_SkillDict 의 "2282. Create a capability matrix file with columns: `Capability`, `Example Source`, ..." 한 줄 = **단일 동작** (verb + 명시적 산출물)

해결: 본 v0.2 § 7 의 마스터 로드맵 (`Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`) 이 RO_SkillDict 수준으로 작성. 17 phase × ~50-70 step = ~900-1200 step.

### 3.8 외부 검색 의 사용자 의뢰 잘못 위임

v0.1 DQ-E2 (Ref 6, 7 의 DOI 사용자 직접 제공 또는 외부 검색 의뢰) 가 잘못된 위임. JCP 본문 DOI `10.1063/1.5000882` 따라가 검색은 내 일.

**본 v0.2 작업 중 실제 외부 검색 결과** (5-27 본 세션):
- **Ref 7 검색 PASS (URL 확보)**: `pubs.aip.org/aip/jcp/article-abstract/138/16/164123/71188` — 제목 = "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity" (확정)
- **Ref 7 의 정확 DOI**: WebFetch 403 (AIP 인증 필요) + WebSearch 결과 metadata 미공개. 추정 = `10.1063/1.4XXXXXX` 패턴이나 정확 값 미확보
- **Ref 6 검색 FAIL**: 다회 search 시도 후 정확 paper 미발견. 가능성:
  - JCP 134 (12), 121102 (2011) 의 Communication 짧은 letter 라 search 결과에 잘 안 잡힘
  - 저자명 정확 매칭 (`S. Lee, C. Y. Son, J. Sung, S. Chong`) 의 paper 가 indexed 안 됨
- **JCP 2017 본문 fetch FAIL** (HTTP 403)

해결 안:
- WebFetch 우회: AIP 인증 우회 가능한 mirror (예: ResearchGate, arXiv) 시도 → 본 검색에서 ResearchGate URL 1 건 발견 (Sung-Chong-Lee 의 다른 paper) — 정확 매칭 아님
- 사용자에게 묻는 대신: **본 v0.2 계획서 §"Phase D Addendum 2"** 로 정확 DOI 확보 phase 별 신설. master roadmap Phase E0 의 Step 부터 진행.

## 4. 잘못된 것 (v0.1 §4 + 신규 B4 + 신규 L4)

v0.1 §4.1 ~ §4.3 (이미 정정 3 + 행위적 잘못 3 + 방법론 한계 3) 유지 + **신규 B4 + L4**.

### B4 (행위적 잘못 — 사용자 critical 피드백) — 계획서 수준 부족 + 외부 검색 위임 + 본질 진단 실패

| # | 항목 | 원인 | 영구 해결 |
|---|---|---|---|
| **B4** | 계획서 v0.1 의 수준 부족 (RO_SkillDict 대비 ~1/5) | 양식 (G2 메모리) 은 갖췄으나, **각 step 의 granularity 표준** 부재. 신규 작업 시 step granularity 표 절대 기준 없음 | **신규 메모리 후보**: `feedback_plan_step_granularity_standard.md` — "각 step 은 단일 동작 verb-noun. 거시 명령 (예: '§1+§2 작성') 분할 의무. RO_SkillDict 마스터 로드맵 패턴 기준." 사용자 결정 받은 후 메모리화 (★ 본 v0.2 가 사용자 검수 통과하면 신설) |
| **B5** | 외부 검색 위임 → 사용자 묻기 (DQ-E2) | "외부 정보 = 사용자 의뢰" 의 잘못된 default. 실제 external resource 의 접근 권한 + 도구 (WebSearch, WebFetch) 이미 보유 | **신규 메모리 후보**: `feedback_external_lookup_first_self.md` — "외부 정보 (DOI · 학술 검색 · 공개 데이터) 는 사용자 묻기 전 self-search 의무. 실패 후에만 사용자 의뢰." |
| **B6** | 본질 진단 실패 — Phase B 에서 self-consistent loop 만 잡고 step function 가정 (사용자 의도) 못 잡음 | Audit 9 차원 중 **"모델 가정 적합성"** 차원 부재. 정독 도중 "이 식이 모사 대상 시스템 특성을 정확히 표현하는가?" 질문 누락 | **메모리 확장**: [[feedback_phase_audit_workflow]] 의 10 차원에 **신규 차원 #11 "모델 가정 적합성 (system-fidelity)"** 추가. 향후 LaTeX·수식 작업 시 자동 적용 |

### L4 (방법론 한계) — Phase D 의 ref 6, 7 정독 깊이 부족

v0.1 §4.3 의 L1 (5 요소 매핑 정성 수준) 확장.

본 정독 (Phase D Step 14-18) 에서 JCP 본문 의 핵심 = §II.C 의 **long-range reaction sink** (continuous reactivity) 였으나, 본 v0.1 의 5 요소 매핑이 이 본질 (continuous vs discrete / step) 을 명시 못함. v0.1 §5 매핑 표 의 "Fredholm vs Volterra" 등 4 가지 차이만 정성 진단.

해결: 본 v0.2 §5.10 에서 신규 5 가지 차이 (이전 4 + **step function vs continuous reactivity**) + 정량 변환 수식 명시.

## 5. 해결안 (v0.1 §5 + 보강 + 신규 §5.11)

v0.1 §5.1 ~ §5.10 유지 + 본질 진단 (§5.11 신설) + audit 차원 확장 (§5.12 신설).

### 5.11 (★ 본질) Step function 가정 회피 + Continuous chemical potential 모델 도입

**A. 신 Chapter 1 의 spine 재설계**:
- ver5 spine `Δ G_eff,j → k_j → dξ_j/dt → ξ_j(q) → dξ_j/dq → dQ/dV` (discrete N_p)
- rechecked2 spine `Q_ext = Q_cell·q → 전하 보존식 → V_n → V_{n,app} → dQ/dV` (V_n implicit, discrete N_p 유지)
- **신 spine** (v0.2 master roadmap Phase E1 결과):
  ```
  Q_ext = Q_cell·q
    → 전하 보존식 [continuous μ(q, T) 또는 분포 ρ(μ; q, T)]
    → V_n = chemical potential μ 의 boundary 또는 적분 결과
    → ref 6, 7 의 비율 substitution closed-form [continuous reactivity S_R(μ) kernel]
    → V_{n,app}
    → dQ/dV (closed-form analytic + 수치 보강)
  ```
- 핵심: discrete `ξ_j` 변수 폐기 또는 보조 변수로 강등. 중심 변수 = **continuous chemical potential μ** 또는 **continuous distribution ρ(μ)**

**B. ref 6, 7 의 비율 substitution 의 graphite 적용**:
- JCP 2017 의 W̄_u(r) ↔ graphite 의 ρ(μ; q, T) 또는 ξ(μ; q, t) (continuous distribution)
- continuous reactivity kernel S_R(μ) — Marcus theory 또는 Cahn-Hilliard 의 chemical potential dependence
- 비율 substitution: `ρ(μ_1)/ρ(μ_0) ≈ ρ^δ(μ_1)/ρ^δ(μ_0)` (단순 case 의 알려진 해 의 비율)

**C. 본 신 spine 의 핵심 검증**:
- ξ_j (discrete) 가 신 spine 에서 어떻게 emerge 하는가? (예: continuous ρ(μ) 의 N_p 개 peak 의 envelope)
- step function 가정 완전 회피 — softplus·logistic·erf·max·min 모두 본질 변수 정의에 사용 X (수치 안정성 보조 항으로만 한정)

**D. Master roadmap Phase E0 ~ E12 에서 단계적 구현**.

### 5.12 (★) Audit 차원 #11 (모델 가정 적합성 = system-fidelity) 신설

[[feedback_phase_audit_workflow]] 확장 — 차원 #11 추가:

> **#11. 모델 가정 적합성 (system-fidelity)** — 본문에 등장하는 모든 가정 (분포 형태, 변수 정의 범위, 경계 조건, 수치 regularization) 이 **모사 대상 시스템의 물리적 특성을 정확히 표현** 하는가? 단순화 (예: step function, discrete N_p) 가 본질 시스템 특성 (예: continuous chemical potential) 을 무시하지 않는가?
>
> Pass 1 의심 항목: max/min/clip/saturation/threshold/step/piecewise/heaviside/sign function 의 사용 위치 + logistic·erf·softplus 가 본질 변수 정의에 사용되는지 (수치 보조 X)
>
> Pass 2: 발견된 항목 중 본질 변수 정의에 사용된 것 → 사용자 시스템 특성 (graphite 의 continuous staging) 과 충돌 진단 → 정정 또는 OI 기록
>
> Pass 3: 정정 후 새 변수 정의가 본질 시스템 특성 정합 + 수치 안정성도 보존

본 차원이 향후 LaTeX·수식·물리 모델 작업 시 자동 적용.

## 6. 종합 평가 (v0.2 재산정)

| 영역 | v0.1 점수 | v0.2 재산정 | 비고 |
|---|---|---|---|
| 정독 의무 | ★★★★★ | ★★★★★ | 변경 없음 |
| 양식 정합 | ★★★★★ | ★★★★★ | 변경 없음 |
| Audit 효과 | ★★★★ | ★★★ | **하향** — 9 차원 중 "모델 가정 적합성" 부재로 본질 문제 못 잡음 (B6). v0.2 §5.12 로 #11 차원 신설 후 회복 예정 |
| 자기 학습 | ★★★★★ | ★★★★★ | 변경 없음 |
| 사용자 의사 반영 | ★★★★ | ★★★ | **하향** — B4 + B5 + B6 동시 발생. v0.2 신규 메모리 3 개 (granularity / external lookup / system-fidelity) 신설 후 회복 |
| 수식 정밀도 | ★★ | ★★ | 변경 없음 |
| 외부 cross-check | ★★ | ★★★ | **상향** — 본 v0.2 작업 중 Ref 7 URL 확보 + Ref 6 다회 search 시도 (FAIL 인정). 사용자 떠넘김 X |
| **계획서 granularity** | (미평가) | ★★ | **신규 평가** — v0.1 가 RO_SkillDict 대비 1/5 수준 |
| **본질 진단 (system-fidelity)** | (미평가) | ★★ | **신규 평가** — Phase B 가 표면 (self-consistent loop) 만 잡고 본질 (step function 가정) 못 잡음 |

**총평**: v0.1 의 "정독·양식·학습 강건, 수식·외부 cross-check 약함" → v0.2 의 "정독·양식·학습 강건, **본질 진단 + granularity 약함 (사용자 critical 피드백)**, 외부 cross-check 부분 회복".

## 7. 새 계획서 (v0.2 — 마스터 로드맵 형식)

본 v0.2 보고서가 입력 → 다음 산출물:

- **`Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`** (마스터 로드맵, RO_SkillDict 수준)
  - 17 phase (E0 ~ E12 + F1 ~ F5) × 평균 50-70 step = ~ 900-1200 step
  - 각 step = 단일 동작 verb-noun 1 줄
  - 각 phase = Save plan + Load inputs + Define + Produce + Gate + Confirm + Result + Ledger 의 일정 구조
  - Phase E0 (Foundation reset and rebuild charter, Steps 19-80) 부터 시작 — step function 가정 회피 charter 선언
  - Phase E1 (Spine redesign, Steps 81-140) — 신 spine 의 continuous chemical potential 도입
  - ... (이하 마스터 로드맵 본문 참조)
- **`Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan-SUPERSEDED.md`** (v0.1 supersession marker)

v0.1 계획서 본문은 보존 (덮어쓰기 X, [[feedback_document_protection_addendum_pattern]] 정합). 향후 참조 기준 = 본 v0.2 보고서 + 마스터 로드맵.

## 8. 메타 (사용자 의뢰 항목 정리)

본 v0.2 가 v0.1 의 DQ-E2 (사용자 의뢰) 를 폐기 — 외부 검색이 내 일. 다만 다음 항목은 여전히 사용자 결정 영역 (자동 처리 X):

| ID | 항목 | 사유 |
|---|---|---|
| **DQ-G1** | 본 v0.2 보고서 + 마스터 로드맵 사용자 검수 | 새 계획서 진입 GO 사인 |
| **DQ-G2** | 신 Chapter 1 의 spine 재설계 안 (continuous chemical potential 도입) 의 사용자 cross-check | 사용자 본인 박사 연구 영역 — 정확 적용 가능성 검증 |
| **DQ-G3** | DQ1 (ChatGPT 의 "큰 논리 오류" 정체) — 본 v0.2 §1.3 재해석 (10 회 검토 도중 발견된 self-consistent loop 등) 이 사용자 의도 정합? | 본질 진단 정확성 cross-check |
| **DQ-G4** | Ref 6 의 정확 DOI / 제목 — 본 v0.2 외부 검색 다회 FAIL. 사용자가 본인 그룹 paper 정보 보유 시 제공 요청 (의뢰 아니라 옵션) | 외부 자원 한계, 사용자 보유 시 제공이 효율적 |
| **DQ-G5** | Audit 차원 #11 (system-fidelity) 신설 + B4·B5·B6 의 신규 메모리 3 개 신설 영구 반영 결정 | 글로벌 메모리 정책 영향 |

DQ-G4 는 "묻기" 가 아니라 "사용자 보유 시 제공 옵션" — 정보 보유자가 사용자 한정인 경우 (본인 그룹 paper) 의 자연스러운 협력. v0.1 의 DQ-E2 같은 무책임 위임 아님.
