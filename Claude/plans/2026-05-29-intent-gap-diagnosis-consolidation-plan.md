# 계획서 — 사용자 의도 ↔ 기존 산출물 간극 정밀 진단 + 합류(consolidation) 로드맵

**Date**: 2026-05-29 · **Author**: Claude 측 · **상태**: **계획 (PLAN) — 사용자 GO 대기. 본 turn 에 본문(LaTeX) 재작성·수정 X.**
**Series**: DIAG (진단 신규 series). 기존 `Claude/plans/MASTER_ROADMAP_v3.md` 를 supersede 하지 않고 그 위에서 **메타-진단**을 수행한다.
**관련 입력**: `MASTER_ROADMAP_v3.md`, `CHARTER_v3.md`, `CROSSCHECK_v2_vs_v3_ChatGPT.md`, `SELF_REVIEW_v2_DELIVERABLES.md`, 업로드 `graphite_ica_ch1_ch6_physical_v3_rechecked.tex` + 리뷰 지적서, GitHub `Claude/docs/graphite_ica_chapter1.tex`.

> **운영 합의 (2026-05-29 사용자 명시)**: 작업 중 선택형 보기(multiple-choice) 제시 금지. 판단이 필요한 사안은 근거와 함께 본 계획서에 **글로 명시**하고, 정말 사용자 결정이 필요한 것만 §10 결정경계에 등재한다.

---

## §0. 사용자 의도 — 두 층위 (절대 기준)

### §0.1 원천 관찰·동기 (verbatim, Charter §00 유지)
> "LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 … 피크 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐… 온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는 현상… 온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를 낮추는 효과… 그 유효 배리어의 논리를 확정하고 그것을 이용해 피크의 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심."

### §0.2 ★ 의도된 **서사 사슬** (2026-05-29 사용자 구술 — 본 진단의 두 번째 절대 기준)
사용자가 이 세션에서 명시한, 챕터를 관통하는 **하나의 인과 narrative**:

1. **관찰**: 저온 → 꼬리 길어져 **다음 피크와 겹침**, 고온 → 꼬리 빨리 떨어짐. → "이건 **열역학적 문제가 기반**"이라 판단(최초 착안점).
2. **전위 추가**: 온도뿐 아니라 극판 전위도 관여. 그런데 극판 전위는 **OCV 평형 ≠ 전류 흐를 때** → 전류 흐를 때의 극판 전위를 고려하는 시스템으로 확장.
3. **C-rate 정당화**: C-rate 따라 피크가 심하게 겹치는 건 이미 다수 확인됨 → 전류 의존 전위는 **무조건 적용 조건**.
4. **Chapter 1**: 위를 **열역학 관점 물리**로 풂 → 유효배리어 논리 확정 → **피팅 가능한 논리식**.
5. **Chapter 2**: Ch1 기반 **발열 해석의 단초**.
6. **Chapter 3**: Ch1 에 **전기화학 반응속도론** 적용해 확장.
7. **Chapter 4**: Ch3 기반 발열 해석 단초.
8. **Chapter 5(~6)**: Ch3 의 **충전 방향 확장** → 흑연 음극 **충방전 히스테리시스** 해석 가능성.

### §0.3 사용자 호소 (본 계획의 트리거)
> "기존 챕터6까지 진행된 건은 그런 내용과 거리가 있다고, 물어보는 세션마다 AI 업체마다 한결같이 말한다. 난 어떻게 해야 하는거냐?"

→ **본 계획의 목표 = (a) 그 "거리"가 구체적으로 무엇인지 객관 진단, (b) 프로젝트를 어떻게 이끌지 구체화, (c) 앞선 연구 중 버리지 않고 끌어쓸 부분(salvage) 확정.**

---

## §1. 목적 (Objective)

1. **간극 정밀 진단**: §0.2 의도 서사 사슬을, 현존하는 **두 산출물 계열**(아래 §2)에 1:1 대조하는 **Intent↔Artifact Traceability Matrix** 를 만들어, 각 사슬 고리가 "구현됨 / 부분 / 표류(drift) / 누락 / 모순" 중 무엇인지 확정한다.
2. **방향 구체화**: 두 계열을 하나의 의도-정합 spine 으로 합류시키는 로드맵을 제시한다 (확장이 아니라 **응축·합류**).
3. **Salvage map**: 기존 작업을 **KEEP / FIX / RETIRE** 로 분류하여, 앞선 연구가 버려지지 않고 어디에 재사용되는지 명시한다.

**비목표**: 본 계획 turn 에서 LaTeX 본문을 재작성·수정하지 않는다. solver 코드도 만들지 않는다(P1). 진단·로드맵·salvage map **문서**만 산출한다.

---

## §2. 배경 — 현재 두 갈래로 갈라진 산출물 (핵심 사실)

이 프로젝트에는 **서로 다른 Chapter 1 계보 2개**가 공존하며, 합쳐진 적이 없다.

| | **(A) Kernel-integral 계열** | **(B) 전하보존 6장 계열** |
|---|---|---|
| 대표 파일 | `Claude/docs/graphite_ica_chapter1.tex` (v5 merged canonical) + `Codex/results/..._rebuilt_v3_canonical_merge.tex` | 업로드 `graphite_ica_ch1_ch6_physical_v3_rechecked.tex` (ChatGPT origin) |
| 범위 | **Chapter 1 단독** (Ch2~ 명시 연기, Roadmap §4 "Out") | **Ch1~Ch6** (발열·BV·히스테리시스 포함) |
| tail 메커니즘 | barrier→**relaxation-length spectrum**→kernel integral; Refs 6/7 closure(Plan A/B) | `k_phys = k_act ⊕ k_lim` 직렬, ξ 동역학, ρ(g) 분포 |
| 진행 기호 | θ | ξ |
| 의도 사슬과의 정합 | **깊이는 깊으나 §0.2 의 1챕터에만 해당; framing 이 분산 동역학으로 pivot** | **폭(Ch1~6)은 §0.2 사슬과 외형 일치하나 "거리 있다" 평가 받음** |

**핵심 인식 1 — 두 계열은 경쟁자가 아니라 같은 코어의 좁은/넓은 버전.** `CROSSCHECK_v2_vs_v3_ChatGPT.md` 가 이미 식별식 1:1 대조로 **SAME 8 / RECONCILABLE 3 / CONTRADICTORY 1(erf vs logistic) / superset 3** 을 확정했다. 즉 배리어→Arrhenius→relaxation→비율치환 **핵심 사슬은 동일**하다.

**핵심 인식 2 — 그런데 프로젝트는 "합집합 산출물"을 만든 적이 없다.** (A)의 깊이(kernel tail engine)를 (B)의 폭(Ch1~6 서사) 안에 끼워 끝까지 관통시킨 **단일 문서가 부재**하다. 이것이 "거리 있다"의 구조적 뿌리로 의심된다.

**핵심 인식 3 — 의도 사슬과 정확히 맞는 트렁크는 (B)다.** §0.2 의 Ch1(열역학)→Ch3(반응속도론)→Ch5(히스테리시스) 구조는 (B)의 장 구성과 직접 대응한다. (A)는 그 Ch1 자리에 들어갈 **tail-shape 엔진**으로서 가치가 크다.

---

## §3. 범위 (Scope)

**In**
- §0.2 의도 사슬 8고리 ↔ (A)·(B) 산출물 traceability 대조.
- thermo vs kinetic framing 재정합(§6.2), χ𝒜 keystone 진단(§6.3).
- Salvage map (KEEP/FIX/RETIRE) + 합류 spine 제안.
- 산출 문서: 진단 result + salvage ledger + 갱신 로드맵(합류판).

**Out (후속·별도 GO)**
- 합류 spine 에 따른 **실제 LaTeX 본문 재작성** (= 다음 단계, 별도 GO).
- fitting solver 구현(P1 불변).
- erf/logistic 최종 확정(DQ-v3-1, 데이터 대기 — 본 진단에선 미결로 유지).

---

## §4. 입력 (Read 대상) 과 접근 규칙

**전문 검독 (full read)**
- (B) 업로드 `graphite_ica_ch1_ch6_physical_v3_rechecked.tex` — **Ch2~Ch6 전문** (현재 Ch1·Ch2 일부 + 리뷰요약만 봄 → Phase A 에서 완독 필수).
- (A) `Claude/docs/graphite_ica_chapter1.tex` — 완독 완료(본 세션).
- 리뷰 지적서 `graphite_ica_v3_review_notes.tex` — 완독 완료.

**부분 확인 / 사실 데이터만**
- `CROSSCHECK_v2_vs_v3_ChatGPT.md`, `SELF_REVIEW_v2_DELIVERABLES.md`, `CHARTER_v3.md`, `MASTER_ROADMAP_v3.md` — 완독 완료.
- `Claude/results/COMPARISON_*` (Claude 측 비교 문서) — Codex 측 내용은 **이 비교문서를 통해서만 간접 참조**.
- 원본(수정 X): `graphite_ica_dynamic_ver5.tex`, `graphite_ica_charge_balance_ver1_rechecked2.tex`.

**접근 금지 (CLAUDE.md P2 준수)**
- **`Codex/results/*.tex` (Codex 산출물 본문) read 금지** — 양 모델 독립 산출물 비교 무결성 보존. Codex 측은 Claude 비교문서로만 간접 인용. (Codex 운용지침 `Codex/AGENTS.md` 류는 필요 시 read 가능.)
- `_local_only/` 원천 PDF·사진은 사용자 명시 시에만.

---

## §5. 가정·제약 (작업 규칙)

- **계획-실행 분리**: 본 문서는 PLAN. GO 전 본문 미수정.
- **문서 보호**: 기존 (A)(B) 및 결과 문서 **덮어쓰기 금지**. 진단은 신규 파일로만.
- **명명 보존 (P5, P3-7)**: `ver.1~ver.5`(역사 명칭) ↔ `Chapter 1~5`(새 구조) 혼동 금지. 보고 시 둘 다 쓰면 매핑 명시. 기존 변수·라벨·절 제목 임의 변경 X.
- **전위 기호 일관 (P3-1)**: `V_n / V_{n,app} / V_{n,drive} / V_{n,OCV}` 구분 유지.
- **무비약·grounding (AGP)**: GROUNDED/BOUNDED/FLAGGED tier 유지. FLAGGED 를 established 로 쓰지 않음.
- **한글 prose + 영어 학술용어**.
- **추가 개선 후보는 실제 수정하지 말고 `추가 후보`로만 보고** (P5).

---

## §6. ★ 예비 진단 (현 시점 근거로 도출 — Phase A 에서 완독 후 확정)

> 아래는 (A) 완독 + (B) Ch1·Ch2 + 리뷰지적서 + 기존 Claude 결과문서에 근거한 **예비** 진단이다. Ph A 의 (B) Ch3~6 완독으로 G1·G4·G5 를 확정/수정한다.

### §6.0 진단의 grounding anchor (물리 주장은 AL 인용 동반 — AGP-1)
본 §6 의 모든 물리 주장은 `ASSUMPTION_LEDGER_v3.md` 의 AL-# 에 anchor 한다 (신규 가정 도입 X, 기존 grounding 재사용).

| 주장 | anchor | 문헌 (DOI) | tier |
|---|---|---|---|
| `ΔG_a=ΔH_a−TΔS_a`, Eyring `k=(k_BT/h)e^{−ΔG/RT}` | AL-1 | Eyring 1935 (10.1063/1.1749604); Evans-Polanyi 1935 | GROUNDED |
| `ΔG_eff=ΔG_a−χF(V−U)` 선형 lowering + 한계 | AL-2 | BV(Bard&Faulkner Ch.3); BEP Evans-Polanyi 1938 (10.1039/TF9383400011); Marcus 1956 (10.1063/1.1742723) | BOUNDED |
| 평형 lattice-gas `μ(ξ)`, ideal width `w=RT/F` | AL-3a | McKinnon-Haering 1983; Bazant 2013 (10.1021/ar300145c) | GROUNDED |
| 1차 완화 `dξ/dt=k(ξ_eq−ξ)`, detailed balance | AL-5 | Onsager 1931; De Groot-Mazur 1962 Ch.X | BOUNDED (평형근처) |
| 꼬리 T-의존 = kinetic lag (저T 큰 lag 긴 꼬리) | AL-8 | 선행 모델 부재 → S1-S10 유도 | FLAGGED novel |
| 비율치환/propagator closure | AL-7 | Lee 2011 (10.1063/1.3565476); Son 2013 (10.1063/1.4802584) | GROUNDED(기법)+DQ(적용성) |

### §6.1 간극 5축 (G1~G5)

- **G1 — 서사 단절 (가장 큰 간극, 추정).** §0.2 는 *하나의 인과 narrative*(관찰→유효배리어→피팅식→발열→히스테리시스)인데, 산출물은 (A) 깊게 판 한 챕터(framing pivot) 또는 (B) 병렬적 형식 장들로 읽힌다. "각 챕터가 왜 존재하며 저온-긴-꼬리 관찰로 어떻게 환원되는지"의 끈이 문서 표면에서 안 보인다. → 매 세션이 "거리 있다"고 하는 1순위 원인으로 추정.
- **G2 — 열역학 vs 동역학 정체성(framing).** §6.2 상술. 관찰의 온도 방향 자체가 *동역학적 지문*인데 라벨은 "열역학". 과학은 이미 사용자 편이나 framing 이 미정합.
- **G3 — keystone 미해결 (χ𝒜 의 역할).** §6.3 상술. 사용자가 가장 중시하는 "전위가 배리어를 낮춘다"의 수학적 역할이 (A)(B) **양쪽 다 미확정**. Ch2~6 이 이 미해결 위에 적층됨.
- **G4 — deliverable 지연 (scope 폭발, 추정).** "피팅에 쓸 수 있는 논리식 1개"가 closure governance·non-uniqueness·P1 밖으로 밀려 표면에서 사라짐. Ph A 에서 (B) 가 실제로 피팅식을 제시하는지 확인.
- **G5 — 두 계열 미합류.** §2 핵심인식 2·3. 깊이(A)와 폭(B)이 합쳐진 단일 문서 부재.

### §6.2 ★ 열역학 vs 동역학 — 재정합 (이미 내부적으로 해소된 사안)

`SELF_REVIEW_v2_DELIVERABLES.md §3` 가 이미 도출한 결론을 본 진단의 1급 명제로 격상한다:

- 평형 lattice-gas 폭 `w = RT/F` 는 **저온서 좁아진다** (25°C 0.0257V → −15°C 0.0222V). 즉 **순수 평형 열역학은 "저온 → 더 sharp"** 를 예측 → 관찰(저온 긴 꼬리)과 **반대**.
- 저온 긴 꼬리는 `k = k_0 exp(−ΔG_a/RT)` 감소 → lag 증가 → relaxation length `L=|I|/(Q_cell k)` 증가의 **동역학 신호**. 관찰과 **일치**.
- ∴ **열역학 = 무대**(`V_n` charge-balance, `θ_eq` 평형 target), **관찰된 꼬리 거동 = 동역학(주역)**. 사용자의 "전위가 배리어를 낮춘다"도 이미 **activation-barrier(동역학)** 개념.

→ **정정된 framing**: "열역학적 *기반* 위에서 전개되는 동역학적 꼬리 현상." 이 한 문장을 합류 문서의 머리에 못박으면 G2 가 닫힌다. (사용자 최초 직관은 틀린 게 아니라 — 열역학이 무대를 깐다 — 다만 *주역이 동역학*임을 명시 안 했을 뿐.)

### §6.3 ★ Keystone — χ𝒜 의 역할 (Level A vs Level B), 그리고 의도 사슬이 주는 해답

리뷰 지적서 #1 + 본 세션 (A) 검토에서 확인된 핵심 모순:
- (A) `D3`: χ 를 **BEP/BV transfer coefficient**(방향성)로 grounding. 그러나 `D5`+`eq:rate`: χ𝒜 가 **총 mobility `k=r_++r_-`** 에 대칭 삽입 → ratio `r_+/r_- = θ_eq/(1−θ_eq)` 가 χ𝒜 와 무관 → 실제로는 **방향성 없는 Level A(mobility scale)**. 이름·grounding(Level B)과 사용(Level A)이 불일치.
- (B) 도 동형 (`ΔG_eff=ΔG_a−χ𝒜` → `k_act` → relaxation). v3 는 Ch3 에서 명시적 forward/backward(Level B)를 따로 도입해 Ch1(Level A)과 **장 간 충돌** (리뷰 지적서 핵심).

**★ 의도 사슬이 곧 해답을 준다 (본 진단의 핵심 통찰):**
§0.2 에서 사용자는 **Ch1 = 열역학, Ch3 = 전기화학 반응속도론 확장**으로 이미 분리했다. 이 분리에 χ𝒜 역할을 그대로 얹으면 자연스럽게 정합한다:
- **Ch1 (열역학 무대 + 1차 완화)**: χ𝒜 를 **mobility 가속 인자(Level A)** 로 재명명. ratio 는 thermodynamic `θ_eq` 가 전담. "effective barrier" 라는 방향성 함의 용어를 Ch1 기본형에서 떼어냄. → 리뷰 권장 (A안)과 일치, (A)의 spectrum-shift 메커니즘(이미 Level A)과도 일치.
- **Ch3 (반응속도론)**: forward/backward 비대칭 split(`r_+ ∝ exp[−(ΔG^‡−β𝒜)/RT]`, `r_- ∝ exp[−(ΔG^‡+(1−β)𝒜)/RT]`)으로 **방향성 barrier lowering = Level B** 를 도입. detailed balance `r_+/r_- = exp(𝒜/RT)` 가 `θ_eq` 와 정합.
- **Ch5 (히스테리시스)**: branch 의존은 Ch3 Level B 구조 위에서만 의미 → keystone 이 Ch3 에서 확정돼야 Ch5 가 성립.

→ 즉 **"barrier lowering = ratio 변경 = Level B" 를 Ch3 한 곳에만 두고, Ch1 은 mobility 가속 + 열역학 무대로 명료화** 하면, χ𝒜 모순이 해소되며 동시에 §0.2 의도 사슬과 정확히 정렬된다. 이것이 본 계획이 제시하는 keystone 해결 **후보**다 (최종 채택은 §10 D2 사용자 결정).

### §6.4 Salvage map (예비 — 앞선 연구를 버리지 않는다)

| 분류 | 항목 | 출처 | 재사용 위치 |
|---|---|---|---|
| **KEEP (코어, 양 계열 합의)** | `ΔG_eff=ΔG_a−χ𝒜` spine; barrier→Arrhenius→relaxation→q변환; charge-balance implicit `V_n` | (A)(B) 공통, CROSSCHECK SAME 8 | 합류 Ch1 골격 |
| **KEEP (결정적 통찰)** | 저온-긴-꼬리 = kinetic 신호 (T-방향 논증) | SELF_REVIEW §3 | 합류 Ch1 framing 머리 (§6.2) |
| **KEEP (깊이 엔진)** | relaxation-length **spectrum kernel integral**; Refs 6/7 closure(validator-tier); Marcus bound; non-uniqueness/forward-only; χ-vs-η_ct discriminator | (A) | 합류 Ch1 tail-shape 엔진 + falsification |
| **KEEP (폭 구조)** | charge-balance 해존재·단조성; Ch3 detailed balance `r_+/r_-`; Ch4 entropy-production heat; Ch5 hysteresis flux-force | (B), 리뷰 "확인된 정합 항목" | 합류 Ch2~Ch5 |
| **FIX (재사용 전 수정)** | χ𝒜 Level A/B 확정(§6.3); flux→rate clamp(리뷰 #2); 검수표 항목 추가(리뷰 #3) | (A)(B) | keystone 확정 후 전파 |
| **DQ (데이터 대기)** | erf vs logistic 평형 형태 | CROSSCHECK §2.B | 저속 OCV near-peak plot 까지 dual-track |
| **RETIRE/강등** | 관찰→배리어→피팅 사슬에서 떠 있는 형식 절; closed-form "primary" 과대위상(이미 v5 강등); "열역학 only" 인식 | (A)(B) | 합류 시 제거/각주화 |

### §6.5 ★ Intent↔Artifact Traceability — 예비 skeleton (Phase B 에서 식·줄 근거로 확정)
§0.2 의 8고리 × 두 계열. 판정: ✅구현 / ◑부분 / ⚠표류(drift) / ✗누락 / ✖모순. (※ (B) Ch3~6 미완독분은 *잠정* 표기 — Phase A 후 확정.)

| # | 의도 고리 (§0.2) | (A) Kernel 계열 | (B) 전하보존 6장 | 예비 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | 저온 긴 꼬리/고온 짧음 = 열역학 기반 관찰 | ✅ (O2, abstract) | ✅ (Ch1 §온도 tail 분해) | **◑** | 양쪽 "관찰"은 적되 framing이 열역학/동역학 미정합(G2) |
| 2 | 전위 효과 (OCV 평형 ≠ 전류 시) | ✅ (`V_drive`, `eq:psi_shift`) | ✅ (`V_n/V_app/V_drive`, `eq:Vapp`) | ✅ | 양 계열 전위 3분 명확(P3-1 양호) |
| 3 | C-rate 무조건 적용 (전류 의존 전위) | ◑ (`L∝|I|` 언급) | ✅ (Ch1 §C-rate, 0.2C 기준식) | **◑** | (A)는 C-rate 절 미약 |
| 4 | Ch1: 열역학 → 유효배리어 → **피팅식** | ◑ (kernel+closure, 식은 P1밖 연기) | ◑ (EMG 비교용·물리식, 피팅식 표면 약) | **◑→G4** | 피팅식 deliverable 표면화 필요 |
| 5 | Ch2: Ch1 기반 발열 단초 | ✗ (Ch1 단독) | 잠정✅ (Ch2 평형 온도계수·heat) | **(A)✗ / (B)잠정◑** | Phase A 확정 |
| 6 | Ch3: 전기화학 반응속도론 확장 | ✗ | 잠정✅ (Ch3 BV forward/backward) | **(A)✗ / (B)잠정◑** | ★ keystone(§6.3) 충돌 지점 — 리뷰 #1 |
| 7 | Ch4: Ch3 기반 발열 | ✗ | 잠정✅ (Ch4 entropy production) | **(A)✗ / (B)잠정◑** | 리뷰 "정합" 항목 다수 |
| 8 | Ch5(~6): 충전방향 → 히스테리시스 | ✗ | 잠정✅ (Ch5 hysteresis flux-force) | **(A)✗ / (B)잠정◑** | Ch3 Level B 확정에 종속 |

→ 예비 결론: **(B)가 §0.2 폭을 거의 덮고(고리 5~8), (A)는 고리 1~4의 깊이를 가진다.** 합류 시 **(A)의 깊이(고리 4 tail/피팅)를 (B) 트렁크에 이식**하는 그림이 traceability 상으로도 지지된다(§2 핵심인식 3 정량 확인).

### §6.6 ★ Self-consistent loop — 예비 dependency + 4-분류 (P3-3 / P3-4)
순환 의존이 **어느 식·변수**에서 생기고, `정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌` 중 무엇인지:

```
charge balance:  Q_cell·q = Q_bg(V_n,T) + Σ_j Q_{j,tot}·ξ_j      …(C)
dynamics:        dξ_j/dt = k_j(V_drive)·[ξ_eq,j(V_n,T) − ξ_j]    …(K)
target:          ξ_eq,j = ξ_eq,j(V_n,T)                          …(E)
driving/rate:    A_j = s_φF(V_drive−U_j),  V_drive = V_n         …(D)
observable:      dQ/dV, dV/dQ  ← d/dq of (C)                     …(O)

loop:  V_n ──(E)──▶ ξ_eq ──(K)──▶ ξ_j ──(C)──▶ V_n   (메인 폐루프)
       V_n ──(D)──▶ A_j ──▶ k_j ──(K)──▶ ξ_j ↑
       Q_bg(V_n) (C)의 RHS·해(V_n) 양쪽 등장 (implicit root)
```

| loop edge | 순환 출처 | 4-분류 | 처리 |
|---|---|---|---|
| `V_n` ↔ `Q_bg(V_n)` in (C) | implicit root | **정의상 implicit formulation** | 단조성 floor `∂Q_bg/∂V_n≥ε_Q` → unique smooth root (well-posed) |
| `V_n` ↔ `ξ_j` (C+K+E) | 상태 결합 DAE | **수치해법 필요** | 시간적분; Plan A 비율치환은 closed-form 시도(검증 tier) |
| kernel `Θ` 적분 안팎 (Volterra) | self-consistent integral | **수치해법 필요** | Plan B direct numerical = reference |
| `χA` 가 `k`(mobility)에 — Level A/B | grounding↔사용 불일치 | **★ 물리 가정 충돌** | §6.3 keystone — Ch1 Level A / Ch3 Level B 분리로 해소(D2) |
| `ρ_G → A_L` 역매핑 | 비유일 inverse | **논리 공백 (회피됨)** | forward-only discipline (역산 금지, Plonka 비유일) |

→ 4-분류 중 **실제 위험은 단 1건(χA Level A/B = 물리 가정 충돌)** 이며 나머지는 well-posed implicit 또는 수치해법으로 닫힌다. 즉 keystone(§6.3) 하나가 loop 상 유일한 미해결 충돌이다.

### §6.7 ★ 합류 시 강제되는 구조 변경 (MASTER_ROADMAP_v3 §7 pivot 열거와 동격)
salvage(KEEP) 를 보존하면서 합류하려면 다음 구조 변경이 **강제**된다 (각각 §10 결정·Phase 와 연결):

1. **χA 역할 분리** — Ch1=mobility 가속(Level A) / Ch3=forward·backward barrier lowering(Level B). (§6.3, D2, Phase C)
2. **기호 통일** — (A) `θ` ↔ (B) `ξ`. 트렁크 (B) 채택 시 `ξ` 로 통일하되 (A) `θ` 는 역사 명칭으로 매핑표 보존(P3-7). (DQ-DIAG-3)
3. **tail 엔진 이식** — (A) relaxation-length spectrum kernel integral 을 (B) Ch1 §완화/§tail 자리에 삽입 (단일 relaxation → spectrum 격상). (Phase E)
4. **framing 머리 못박기** — "열역학 무대 + 동역학 주역"(§6.2)을 합류 Ch1 서두에. (G2 종결)
5. **flux→rate clamp** — 리뷰 #2: 발산·부호 없는 clamp 형태로. (FIX)
6. **피팅식 표면화** — deliverable 논리식을 본문 결과로 노출(solver 코드는 여전히 P1 밖). (G4)
7. **명명 매핑표** — `ver.1~5` ↔ `Chapter 1~5` 매핑을 합류 문서 머리에(P3-7).

---

## §7. Phase 분해 (cumulative step: DIAG series D1–D260; 최소 기준점)

> 직전 Claude 측 ledger = `REVIEW_LEDGER_v4_CANONICAL_CH1.md`. 본 진단은 신규 DIAG series 로 시작하며, GO 시 `Claude/results/PHASE_DIAG_EXECUTION_LEDGER.md` 를 init 한다.

| Phase | Steps | Block | Purpose | Gate (verifiable) |
|---|---:|---|---|---|
| **A** | 1–60 | 완독 | (B) Ch2~Ch6 전문 정독 + (A) 재확인. 각 장 핵심식·역할 추출 | (B) 6개 장 각각 "핵심식 목록 + 역할 1문장" 표 완성 (누락 0) |
| **B** | 61–130 | ★ Traceability | §0.2 8고리 × {(A),(B)} → "구현/부분/표류/누락/모순" 판정 매트릭스 | 8고리 전부 양 계열에 대해 셀이 채워지고 각 판정에 파일·식·줄 근거 1개 이상 |
| **C** | 131–170 | ★ Keystone | χ𝒜 Level A/B 를 §6.3 후보로 정밀 진단 (Ch1 Level A / Ch3 Level B 정합성 수식 검증) | Ch1↔Ch3↔Ch5 전달 정합(P3-6) 확인 + detailed balance 정합식 명시 |
| **D** | 171–220 | Salvage | §6.4 표를 (B) 완독 근거로 확정: KEEP/FIX/RETIRE + 재사용 위치 | 모든 기존 장·핵심식이 정확히 한 분류에 배정 (미분류 0) |
| **E** | 221–260 | 합류 로드맵 | (B) 트렁크 + (A) Ch1 엔진 이식한 **단일 spine Ch1~6** 제안 + 피팅식이 표면화되는 위치 명시 | spine 각 장이 §0.2 고리에 매핑 + 피팅식 등장 절 지정 + Ch1 기준식↔Ch2-5 전달 무충돌(P3-6) |
| F | 261– | 산출·검수 | 진단 result + salvage ledger + 갱신 로드맵 commit; self-check(P3 7항목) | §8 gate 전 항목 통과 후 사용자 검수(Decision Gate) |

(step 수 = 최소 기준점, 확장 가능.)

---

## §8. Gate — 본 프로젝트 검수 7항목 (P3) 의 본 진단판

각 Phase gate 는 §7 조건 + 아래 P3 매핑을 만족해야 한다 ([[feedback_gate_design_principle]] 확인가능 조건):

1. (P3-1) `V_n/V_{n,app}/V_{n,drive}/V_{n,OCV}` 구분이 진단·매트릭스 전체에서 일관.
2. (P3-2) 전하 보존식이 **내부 전위 결정 중심식**으로 유지되는지 양 계열에서 확인 (OCV 읽기로 회귀 X).
3. (P3-3) `ξ/θ, Q_bg, dQ/dV, dV/dQ` 의 self-consistent loop 가 **어느 식·변수**에서 생기는지 dependency graph/표로 표시.
4. (P3-4) 그 순환을 `정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌` 4분류로 분리 진단.
5. (P3-5) Refs 6/7 도입부에 {서지·사용자논문 내 위치·원 수학구조·변수매핑·물리가정 차이} 5항목이 기록되는지 확인 (Phase C).
6. (P3-6) 합류 spine 의 Ch1 기준식이 Ch2~5 전달식과 무충돌.
7. (P3-7) `ver.N` ↔ `Chapter N` 명칭 혼동 0, 보고 시 매핑 명시.
+ 공통: 본문 가정 모두 AL 인용, FLAGGED 미오용, BOUNDED 유효범위 병기, Codex tex 미열람 준수.

---

## §9. 산출물 · 저장 위치

- `Claude/results/PHASE_DIAG_INTENT_GAP_RESULT.md` — 진단 본문 (G1~G5 확정 + Traceability Matrix + §6.2/§6.3 결론).
- `Claude/results/PHASE_DIAG_SALVAGE_LEDGER.md` — KEEP/FIX/RETIRE 분류표 + 재사용 위치.
- `Claude/results/PHASE_DIAG_EXECUTION_LEDGER.md` — 12컬럼 실행 ledger.
- `Claude/plans/2026-05-29-consolidation-roadmap.md` (Phase E 산출) — 합류 spine Ch1~6 로드맵 (= 차기 재작성 GO 의 입력).
- commit: 작업+검토 페어, push `claude/chapter-1-physics-logic-WD1R5` (사용자 push 지시 시).

---

## §10. 리스크 · 중단조건 · ★ 사용자 결정경계

### 리스크
- R1: (B) Ch3~6 완독 결과가 §6 예비진단을 뒤집을 수 있음 → Phase A 후 G1·G4·G5 재확정(정지 사유 아님, 갱신).
- R2: keystone(χ𝒜) 해결이 (A) tail 메커니즘에 영향 → Phase C 에서 spectrum-shift 가 Level A 와 정합함을 우선 검증(이미 정합 — §6.3).
- R3: erf/logistic 미결로 합류 spine 정체 → dual-track 유지로 진행(정지 사유 아님).

### 중단조건
Decision Gate 도달 / 새 외부 의존성 / FAIL gate / 사용자 stop — 그 외엔 마지막 Phase 까지 자동 진행.

### ★ 사용자 결정경계 (선택형 보기 없이, 글로 명시 — 자유 회신으로 알려주시면 됩니다)
- **D1 (트렁크)**: 합류의 **서사 트렁크를 (B) 전하보존 6장**으로 두고 (A) kernel-integral 을 **Ch1 의 tail-shape 엔진으로 이식**하는 방향 — 이것이 §0.2 의도 사슬과 직접 정합하므로 **본 계획의 권고**. 다른 선호(예: (A)를 트렁크로) 있으면 알려주세요.
- **D2 (keystone)**: χ𝒜 = **Ch1 mobility 가속(Level A) + Ch3 forward/backward(Level B)** 분리(§6.3) — **권고**. 동의 여부.
- **D3 (erf/logistic)**: 데이터 전까지 **dual-track 유지(미결)** — 권고. 변경 원하면 알려주세요.
- **D4 (범위)**: 본 단계를 **진단·로드맵까지만**(권고) 할지, 진단 직후 **합류 본문 재작성까지 연속** 진행할지.

> 위 D1~D4 는 GO 시점에 한 번에 글로 답해주시면 됩니다. 무응답 시 본 계획은 **권고값(D1=B트렁크+A엔진, D2=분리, D3=dual-track, D4=진단까지)** 으로 Phase A 진입하도록 설계되어 있습니다.

---

## §11. Test Plan · Decision Queue · Sprint Contract

### Test Plan (verifiable, 통과기준 명시)
- **T-DIAG-1**: §0.2 8고리 × {(A),(B)} traceability 매트릭스 셀 **누락 0** (16셀 전부 판정).
- **T-DIAG-2**: 모든 ⚠표류/✗누락/✖모순 판정에 파일·식·줄 근거 **≥1**.
- **T-DIAG-3**: self-consistent loop 모든 edge 가 4-분류(P3-4) 중 정확히 하나에 배정 (미분류 0).
- **T-DIAG-4**: 기존 모든 장·핵심식이 salvage 분류(KEEP/FIX/RETIRE) 정확히 1개에 배정 (미분류 0).
- **T-DIAG-5**: 합류 spine 각 장 → §0.2 고리 매핑 + Ch1 기준식 ↔ Ch2-5 전달 무충돌(P3-6) 0-FAIL.
- **T-DIAG-6**: §6 의 모든 물리 주장이 §6.0 AL anchor 인용 동반 (무인용 0); FLAGGED(AL-8 등) established 미사용.
- **T-DIAG-7**: Codex `*.tex` 본문 미열람 준수 (git/대화 로그상 read 0).

### Decision Queue (기존 DQ 연계 + 신규)
*데이터 대기 / phase 내 해소 / 사용자 결정* 으로 분리:
- **DQ-v3-1** (erf vs logistic 평형형태) — *데이터 대기*. 본 진단서 **dual-track 유지**, 미결로 보존(저속 OCV near-peak plot 까지).
- **DQ-v3-2** (Volterra↔Fredholm 비율치환 적용성) — *Phase C 내 해소* (기존 Plan A M1 검증과 합치).
- **DQ-DIAG-1** (트렁크 = (B)+A엔진) — *사용자 결정* (§10 D1). 무응답 시 권고값.
- **DQ-DIAG-2** (keystone Level A/B 분리) — *사용자 결정 + Phase C 수식 검증* (§10 D2).
- **DQ-DIAG-3** (기호 `θ`↔`ξ` 통일) — *합류 시 결정*. 권고: 트렁크 (B) 의 `ξ` 채택 + (A) `θ` 매핑표 보존(P3-7).
- **DQ-DIAG-4** (범위 = 진단까지 / 재작성 연속) — *사용자 결정* (§10 D4).

### Sprint Contract
- [ ] Phase A~F 완료 (또는 확장).
- [ ] Traceability 매트릭스 8×2 무누락 + 근거 첨부 (T-DIAG-1,2).
- [ ] self-consistent loop 4-분류 완료 (T-DIAG-3).
- [ ] salvage 미분류 0 (T-DIAG-4).
- [ ] 합류 로드맵 산출 + §0.2 매핑 + P3-6 무충돌 (T-DIAG-5).
- [ ] §6 물리주장 AL 인용 0 누락 (T-DIAG-6).
- [ ] 매 phase commit 페어 (작업+검토), Codex tex 미열람.
- [ ] P3 7항목 self-check + 사용자 검수(Decision Gate) 통과.

---

## §12. 진입조건 · 순서 (P4 체크리스트 확인)

- [x] 활성 작업 폴더 = `Claude/` 계열.
- [x] 원천 파일 목록 확정 (§4).
- [x] 전문 검독(=(B) Ch2~6) vs 부분확인 분리 (§4).
- [x] 기존 계획서(MASTER_ROADMAP_v3)/ledger(REVIEW_LEDGER_v4)/handover 확인 완료.
- [x] cumulative step 시작점 = DIAG D1 (직전 v4 canonical 이후 신규 series).
- [x] 중단조건 + 사용자 결정경계 명시 (§10).
- [x] 검증 gate 실제 수행 가능하게 기술 (§7~§8).
- [x] 결과·ledger 저장 위치 확정 (§9).

**진입**: 본 계획 **사용자 GO** 시 Phase A 진입. (§10 D1~D4 회신은 GO 와 함께, 또는 무응답 시 권고값 적용.)

---

## §13. Correction History
| 일자 | 변경 |
|---|---|
| 2026-05-29 | 신설. 사용자 호소(§0.3) + 의도 서사 사슬(§0.2) 수신 → 간극 진단 + 합류 로드맵 + salvage map 계획화. 두 산출물 계열(A kernel / B 전하보존 6장) 갈라짐을 핵심 사실로 식별. thermo/kinetic 재정합(§6.2)·χ𝒜 keystone 해결 후보(§6.3)·salvage map(§6.4) 예비 제시. 선택형 보기 금지 합의 반영. **계획 상태 — GO 대기.** |
| 2026-05-29 | 심도 보완 (사용자 "기존 계획서와 유사 심도 확인·보완"): §6.0 grounding anchor(AL+DOI), §6.5 Intent↔Artifact 예비 traceability skeleton(8×2), §6.6 self-consistent loop dependency + P3-4 4-분류, §6.7 합류 강제 구조변경 7건(roadmap §7 pivot 동격), §11 Test Plan(T-DIAG-1~7)·Decision Queue(기존 DQ-v3 연계)·Sprint Contract 추가. 진입조건→§12, History→§13 재번호. |
