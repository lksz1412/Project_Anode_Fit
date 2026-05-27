# Chapter 1 Rebuild — Master Roadmap v2

**Date**: 2026-05-28
**Charter binding**: `Claude/results/CHARTER_v2.md`
**Supersedes**: `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md` (v1 master roadmap)
**Cumulative step series**: **new series starting from 1** (DEC-6). v1 series (1~340) closed at Phase E4 v1 termination.

---

## §0. ★ 작업의 핵심 (사용자 verbatim, 본 roadmap 의 절대 기준)

> 본 §0 은 사용자가 직접 제공한 작업의 핵심 내용 verbatim. 본 roadmap 의 모든 phase·step·gate 는 본 §0 을 절대 기준으로 한다. 본 내용과 충돌하는 모든 후속 결정은 무효.

### §0.1 작업 동기 + 물리 현상 + 이론적 가설 (사용자 verbatim, 2026-05-28 statement 2)

> "LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히 피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 **피크 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐**가 달라지는것을 확인했다. 특히 **온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는** 현상이 관측되었어. 원래라면 그렇게 온도에 대해 **약간 가우시안 피크 형상**이 나타나고 더이상 진행이 안될 것으로 생각되는데 그 **온도에 의한 배리어** 외에 추가적인 **극판 자체 전위에 따른 배리어를 낮추는 효과**가 있다고 봤고 그 **유효 배리어의 논리를 확정**하고 그 것을 이용해 **피크의 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심**이야."

### §0.2 작업의 4 가지 원칙 (사용자 verbatim, 2026-05-28 statement 1)

> "1. 피팅 솔버 코드 구축X
> 2. 흑연의 ICA 즉 dQdV를 해석하는 이론적 배경을 작업
> 3. 논리 전개를 가다듬어서 가능하면 논문이나 특허로 발전시킬까 고민중
> 4. 산출물은 원본 처럼 가능하면 모든 수식 전개의 **논리적 비약이 없고**, **생략 없이** 모든 과정을 **대학교 학부생 수준의 지식**으로도 그 논리 전개 과정을 따라갈 수 있게 정리해주길 바라고 있다."

### §0.3 사용자 지시 — 본 roadmap 의 처리 방식 (2026-05-28 statement 3)

> "리뷰가 끝나면 작업 계획부터 다시 처음부터 진행하자. 그게 맞는것 같다. 하루종일 작업한게 아깝지만 처음부터 다시 계획부터 짜서 시작하는게 맞겠다. 이전까지의 작업물을 old 폴더 하나 만들어서 밀어넣고, 다시 처음부터 시작하자."

### §0.4 핵심 키워드 (본 roadmap 전체 적용)

- **ICA peak** — 피크는 상변이 신호
- **꼬리 거동** — 본 작업의 1 차 초점 (피크 면적은 피팅 영역, 본 작업 X)
- **온도 배리어** — Gibbs 활성화 자유에너지 ΔG_a(T)
- **극판 전위 보조 유효 배리어** — 전위 의존 lowering −χ·A
- **유효 배리어 = ΔG_eff = ΔG_a − χ·A** ★ spine 출발점
- **가우시안 peak** — 평형 분포의 형상 (logistic·임의 sigmoid 가 아닌 가우시안 명시)
- **저T 꼬리 길고, 고T 꼬리 짧음** — T 의존성 해석 대상
- **피팅 가능 논리식** — 본 작업의 deliverable
- **학부생 수준 전개 + 논리 비약 0 + 생략 0** — 작성 원칙
- **논문 또는 특허 수준 정밀도** — 정밀도 기준
- **피팅 솔버 코드 X** — 범위 외

### §0.5 본 roadmap 의 본 §0 정합 의무

본 roadmap 의 모든 §1-§22 + 모든 phase plan/result 는 본 §0 을 절대 기준으로 한다. 충돌 발생 시:
- 본 §0 우선.
- 본 §0 과 모순되는 모든 식·문장·spine·결정은 **즉시 invalid** 처리.
- 본 §0 외 추가 사용자 verbatim 이 들어오면 본 §0 에 immediate append.

### §0.6 Phase/Step 유연성 — 본 roadmap 의 step 은 ``최소 기준점'' (사용자 verbatim 2026-05-28)

> "phase 나 step은 계획이 저렇게 있는것이지 작업 진행하다가 추가로 더 검토가 필요하면 늘려도 된다. 저기에 무조건 맞춰야한다는게 아니고, 최소 저것은 해야한다의 기준점으로 잡으라고."

본 roadmap §2 의 17 phase × cumulative step 1-1220 은 **최소 기준점**.

- 작업 진행 중 추가 검토·증명·식 도출이 필요하면 step 늘리기 OK.
- 새로운 phase 가 필요하면 본 roadmap §2 의 phase 목록 갱신 + ledger 행 추가.
- ``계획서에 N step 으로 되어 있으니 N step 안에 끝내야 한다'' 식 압력 → 누락·간소화 트리거 → 본 roadmap §0.5 의 §0 정합 의무 위반 → **즉시 step 확장 우선**.

상세: [[feedback_step_granularity_flexibility]] (글로벌 메모리).

### §0.7 Phase Result 저장 의 컴팩션 환각 방지 + 복구 절차 (사용자 verbatim 2026-05-28)

> "내가 페이즈마다 결과물을 저장하기를 바라는 이유는 니가 작업중 컴팩션이 일어나도 훼손된 기억을 이용해서 환각 증상을 일으키지 말고, 해당되는 과거 페이즈 저장 문건을 찾아가서 보고 내용을 정확히 파악하고 제대로 작업하길 바래서다. 컴팩션 이후 해당 되는 내용이 확인이 필요한 경우 이 계획서를 보고 해당 페이즈 문건을 찾아가서 다시 확인하고 그것을 기반으로 작업하라는 의미이다."

**복구 절차 (절대 의무)**:

1. 컴팩션 후 또는 ``이전 phase 에서 어떻게 정의했더라'' 류 정보 확인 필요 시 — 추정 / 추측 / ``내가 기억하기로는'' 류 **절대 금지**.
2. 본 master roadmap (이 파일) 의 §2 phase 목록 보기 — 어느 phase 산출에 정보가 있는지 식별.
3. 해당 phase 의 result 파일 직접 Read — `Claude/results/PHASE_<N>_v2_..._RESULT.md` 또는 `.json`.
4. Read 결과를 기반으로 정확 답변·작업 — read 후 그 내용 cite 또는 직접 인용.
5. Read 안 됐거나 부재하면 ``근거 미발견'' 명시 — 추정 대체 X.

매 phase Result 저장이 본 복구 절차의 input. **Result 저장 + master roadmap/ledger 갱신 + commit 셋 모두 한 phase 의 완성 조건**.

상세: [[feedback_phase_result_anti_compaction_hallucination]] (글로벌 메모리).

### §0.8 Ralph Wiggum 검증 루프 — 논리 완성 때까지 반복 검증 (사용자 verbatim 2026-05-28)

> "논리 완성 때까지 랄프위검 루프 식의 검증 루프를 돌려서 제대로된 논리를 완성해오길 바란다."

본 roadmap 의 매 phase (특히 ★ Phase 4_v2 유효 배리어, 9_v2 Refs 6/7 closed-form, 11_v2 피팅 가능 논리식) 의 audit 단계 = Ralph Wiggum loop 적용.

**Ralph Wiggum loop 절차** (글로벌 `~/.claude/governance/06-ralph-wiggum-loop.md` + 본 작업 특화):

```
[Phase 작업물 commit]
  → [audit Pass 1 (발견)]
  → [audit Pass 2 (확정·수정)]
  → [audit Pass 3 (재검증)]
  → IF FAIL or 논리 완성 미달:
       → 추가 step 확장 (§0.6 적용)
       → 정정 commit
       → audit 재시도 (Pass 1 부터)
       → 반복 ... 최대 5 회 상한 (governance §6 정합)
  → IF 5 회에도 FAIL: stop + 사용자 보고 + DQ 등재
  → IF PASS + 논리 완성: phase 종료, 다음 phase 진입
```

**``논리 완성'' 의 판단 기준** (본 작업 특화):

- Charter v2 §5 Writing Precision Standard 의 §5.1-§5.4 모두 PASS (논리 비약 0 + 생략 0 + 학부 prose + Dim #11 0 FAIL).
- 본 §0 의 사용자 verbatim 정합 (특히 §0.1 의 ``유효 배리어 논리 확정'', §0.2 의 ``피팅 가능 논리식'' 등).
- 본 phase 의 deliverable 식 (예: Phase 4_v2 의 ΔG_eff 정의식) 이 학부 수준 reader 가 sentence-by-sentence 따라갈 수 있도록 자기 일관성.

---

## §1. Roadmap Objective

Construct `Claude/docs/graphite_ica_chapter1.tex` (final name, no v0.1 suffix — fresh start) as a journal-article-grade theoretical document explaining graphite anode ICA tail behavior (user intent I1) via:

- (A1)–(A4) Effective barrier `ΔG_eff = ΔG_a(T) − χ A(V)` Arrhenius rate (user intent I5)
- (A5) Gaussian-cumulative equilibrium distribution `ξ_eq = (1/2)[1+erf(...)]` (user intent I4)
- (A6)–(A9) Volterra-form self-consistent time integral
- **(A10)–(A11) Refs 6/7 ratio-substitution closed-form** (user PhD work, load-bearing)
- (A12) ICA observable + tail-shape T-dependence + fitting-capable logical expression (user intent I3 + I6)

---

## §2. Phase Range (v2 series, 17 phases)

| Phase | 이름 | Cumulative Steps | Goal |
|---|---|---:|---|
| **0_v2** | Charter v2 audit + Phase 0_v2 plan + spine A1-A12 lock | 1–60 | Foundation governance, no LaTeX writing |
| **1_v2** | §0 본문 머리말 + §1 작업의 동기 (O1-O3 + 사용자 의도 I1-I6 명시) | 61–120 | Setup + motivation |
| **2_v2** | §2 기호와 단위 컨벤션 (Variable inventory, units) | 121–180 | Notation |
| **3_v2** | §3 흑연 staging 과 effective transition index `j = 1..N_p` | 181–240 | Concept (discrete-j spine) |
| **4_v2** | **§4 유효 배리어 ΔG_eff = ΔG_a − χ·A 정식 유도** (★ spine 출발점) | 241–320 | User intent I5 spine 핵심 |
| **5_v2** | §5 평형 분포 ξ_eq = erf 도출 (가우시안 분포의 누적 적분) | 321–400 | User intent I4 spine |
| **6_v2** | §6 속도상수 k = ν exp(−ΔG_eff/RT) (Arrhenius + 전위 lowering 결합) | 401–480 | User intent I3 + I5 결합 |
| **7_v2** | §7 진행률 동역학 dξ/dt = k(ξ_eq − ξ) | 481–540 | Relaxation kinetics |
| **8_v2** | §8 시간 적분형 ξ(t) = Volterra equation (Refs 6/7 적용 준비) | 541–600 | Self-consistent integral form |
| **9_v2** | **§9 ★ Refs 6/7 비율 치환 closed-form ξ(t) 도출** | 601–740 | ★ User PhD work load-bearing application |
| **10_v2** | §10 ICA 관측식 + 꼬리 모양 T 의존성 정성 도출 | 741–820 | User intent I1 + I3 직접 |
| **11_v2** | §11 ★ 피팅 가능 논리식 (피팅 파라미터: ΔH_a, ΔS_a, χ, ν, U, σ) | 821–900 | ★ User intent I6 종료점 |
| **12_v2** | §12 ver5 §8 장벽 분포 평균 (advanced note 보조) + §13 ρ(μ) continuous (appendix 선택) + §14 ver.2 인계 + §15 자기 검수 + §16 참고문헌 | 901–1000 | Comprehensive close |
| **F1_v2** | LaTeX 빌드 환경 + 첫 시도 | 1001–1040 | Build |
| **F2_v2** | 빌드 에러 정정 루프 | 1041–1080 | Build fix |
| **F3_v2** | PDF 사용자 검수 (★ Decision Gate) | 1081–1120 | Review |
| **F4_v2** | 사용자 피드백 반영 + v0.2 정정 | 1121–1180 | Iterate |
| **F5_v2** | 최종 commit + 후속 계획 결정 | 1181–1220 | Close |

Total: 17 phases, cumulative steps 1–1220.

---

## §3. Non-goals (v2 series)

- 피팅 솔버 코드 작성 (사용자 명시 P1, Charter v2 §1.3)
- Chapter 2, 3, 4, 5 작성 (별 후속 roadmap)
- ρ(μ) continuous spine 의 spine primary 화 (advanced appendix 만)
- ver5 §8 장벽 분포 평균의 spine primary 화 (advanced note 만)
- v1 (Claude/old/) 의 산출 본문 직접 재사용 (사실 자료만 참조)
- Codex/ 영역 read/write (P2)
- ver5.tex / ver1_rechecked2.tex 본문 수정 (참조 only)

---

## §4. Implementation Changes

### 4.1 신규 생성 (Claude/docs/)

- `Claude/docs/graphite_ica_chapter1.tex` — 최종 본문 (no v0.1 suffix since this is the fresh start; if user later requests version suffix the file will be renamed accordingly)
- `Claude/docs/graphite_ica_chapter1.json` — companion metadata

### 4.2 신규 생성 (Claude/results/)

- `Claude/results/CHARTER_v2.md` — Charter (already written)
- `Claude/results/PHASE_0_v2_..._RESULT.md` + `.json` — Phase 0_v2 result
- `Claude/results/PHASE_<N>_v2_..._RESULT.md` + `.json` — Phase N result for N = 1..12
- `Claude/results/PHASE_F<N>_v2_..._RESULT.md` + `.json` — Phase F1-F5 result
- `Claude/results/EXECUTION_LEDGER_v2.md` — neue ledger (v2 series step 1-1220)

### 4.3 신규 생성 (Claude/plans/)

- `Claude/plans/MASTER_ROADMAP_v2.md` — this file
- `Claude/plans/PHASE_<N>_v2_..._PLAN.md` — per-phase plan (created at each phase entry)

---

## §5. Phase 0_v2 — Charter v2 audit + Spine lock

Steps (cumulative 1–60):

1. Save Charter v2 — **DONE** (`Claude/results/CHARTER_v2.md`).
2. Save Master roadmap v2 — **DONE** (this file).
3. Initialize Execution Ledger v2 (`Claude/results/EXECUTION_LEDGER_v2.md`).
4. Move v1 산출물 to `Claude/old/` — **DONE** (current turn).
5. Identify v2 spine (A1-A12) as locked per Charter v2 §2.
6. Confirm DEC-1 ~ DEC-8 are user-acknowledged (DEC-2 V_n=lookup is default; user may revise via DQ-v2-1).
7. Audit Charter v2 itself against Charter v2 §5 Writing Precision Standard.
   - 7a. Pass 1 keyword scan on CHARTER_v2.md.
   - 7b. Pass 2 classification.
   - 7c. Pass 3 verification.
8. Audit Charter v2 itself against Charter v2 §6 Audit Dim #11.
9. Audit Charter v2 itself against Charter v2 §7 (O1-O3 motivation reference).
10. Plan Phase 1_v2 entry conditions.
11–30. (Reserved for Phase 0_v2 plan/Result detailed steps.)
31–60. (Reserved.)
60. End Phase 0_v2 boundary.

Gates:
- `GATE_0_v2_1`: Charter v2 9 sections present and self-consistent. PASS criterion: 9 sections in Charter v2 visible.
- `GATE_0_v2_2`: Master roadmap v2 17 phases defined with cumulative steps. PASS criterion: this file's §2 table.
- `GATE_0_v2_3`: v1 산출 모두 `Claude/old/` 이동. PASS criterion: `Claude/docs/` 에 chapter1_v0.1.tex 부재; `Claude/plans/`, `Claude/results/` 의 chapter1 v1 관련 파일 모두 부재.
- `GATE_0_v2_4`: Cumulative step series v2 = 1부터 시작 명시. PASS criterion: ledger v2 의 Phase 0_v2 = step 1-60.
- `GATE_0_v2_5`: Charter v2 자체의 Dim #11 audit PASS (0 FAIL). 

Output: Phase 0_v2 closure with Gate `PASS_FOUNDATION_v2`.

---

## §6. Phase 1_v2 — §0 본문 머리말 + §1 작업의 동기 (cumulative 61–120)

Steps (요약, 본 phase 진입 시 별 plan 작성):

61. Save Phase 1_v2 plan.
62. Load Charter v2.
63. Begin `Claude/docs/graphite_ica_chapter1.tex` — preamble (LaTeX, kotex, amsmath, longtable, mdframed) + macros.
64. Add Charter compliance header (50-line block comment) referencing Charter v2 §3 anti-patterns + §6 audit Dim #11 + spine A1-A12.
65. Write `\title{...}` + `\author{...}` + `\date{2026-05-28}`.
66. Write `\begin{document}` + `\maketitle` + abstract + `\tableofcontents`.
67. Begin §0 (또는 §1) 본문 머리말 — 본 Chapter 의 학술적 위상 + 사용자 의도 I1-I6 verbatim 인용.
68. Draft §1.1 (배경 관측) — graphite ICA dQ/dV peak + 꼬리 + T 의존성 (O1, O2, O3 명시 + 사용자 정확 인용).
69. Draft §1.2 (이론적 가설) — 사용자 verbatim "온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를 낮추는 효과" 의 의미를 학부 수준 prose 로 설명.
70. Draft §1.3 (본 Chapter 의 deliverable) — 유효 배리어 논리식 + 꼬리 모양 의 T 의존성 closed-form + 피팅 가능 논리식.
71. Draft §1.4 (사용자 박사학위 연구 의 위치) — Refs 6, 7 의 비율 치환법이 본 spine 의 어디서 들어오는지 preview.
72. Draft §1.5 (본 Chapter 1 의 spine boxed equation) — A1-A12 의 boxed summary.
73–119. (Reserved for §1 detailed prose.)
120. End Phase 1_v2 boundary.

Gates:
- `GATE_1_v2_1`: §0 + §1 본문에 5 subsections 이상.
- `GATE_1_v2_2`: 사용자 의도 I1-I6 모두 §1 본문 내 명시 인용.
- `GATE_1_v2_3`: spine boxed equation 이 A1-A12 의 7-line form 으로 §1.5 에 포함.
- `GATE_1_v2_4`: §5 Writing Precision Standard 의 Pass 1 keyword check 0 FAIL.
- `GATE_1_v2_5`: §7 O1-O3 motivation 모두 §1 내 명시.

Output: Phase 1_v2 closure with Gate `PASS_INTRO_MOTIVATION_v2`.

---

## §7. Phase 2_v2 — §2 기호와 단위 컨벤션 (cumulative 121–180)

Steps (요약):

- Variable inventory (Charter v2 §8 의 canonical 32 + derived 6 + advanced 2 항).
- `longtable` 환경 사용.
- 단위 명시 (T K, t s, q dimensionless, etc.).
- 부호 컨벤션 (s_I, s_{φ,j}).
- §1 spine 변수 1:1 cover 확인.

Gate `PASS_NOTATION_v2`.

---

## §8. Phase 3_v2 — §3 흑연 staging 과 effective transition (cumulative 181–240)

- ver5 §3 의 N_p 개 effective transition 개념 보존 (사용자 의도 spine 의 discrete-j 정합).
- 각 transition j 의 의미 + j-index 의 의미.
- transition 의 정렬 (V_n 증가 방향, U_j(T) 정렬).
- 본 §3 은 사용자 의도 spine 의 discrete-j 가 v1 의 continuous ρ(μ) 보다 우선임을 명시.

Gate `PASS_STAGING_v2`.

---

## §9. Phase 4_v2 — ★ §4 유효 배리어 ΔG_eff = ΔG_a − χ·A 정식 유도 (cumulative 241–320)

★ 본 Chapter 의 spine 출발점. 모든 후속 §의 기초.

Steps (요약):

- §4.1 Gibbs 활성화 자유에너지 ΔG_a(T) (A1) — Gibbs 자유에너지의 정의에서 출발, ΔH - TΔS 학부 수준 도출.
- §4.2 전위 보조 구동력 A(V_n,app, T) (A2) — 전기화학 정의 (Faraday 법칙 + 화학 퍼텐셜 차이 + Nernst 식) 에서 출발, A = s_φ F (V_n,app - U) 학부 수준 도출.
- §4.3 ★ 유효 배리어 ΔG_eff = ΔG_a − χ·A (A3) — 활성화 자유에너지의 전위 의존성 (Brønsted–Evans–Polanyi 류, χ 의 학부 수준 의미) + 결합 식 도출. 사용자 verbatim 인용.
- §4.4 χ 의 학부 수준 해석 — Brønsted–Evans–Polanyi 계수, transfer coefficient, 일반화된 lever rule 의 한 사례.
- §4.5 ΔG_eff 의 T 의존성과 A 의존성의 분리 — 사용자 의도 I3 (T 의존) + I5 (전위 의존) 의 결합.
- §4.6 ΔG_eff < 0 영역 의 처리 — 단순 Arrhenius 가 폭주, ver5 §6.5 의 max(.,0) step 처리 = 본 spine 에서 폐기. **대신 (A9)~(A11) Refs 6/7 비율 치환 closed-form 에서 자연 발생적 자기 일관성 으로 처리** preview.
- §4.7 §5 진입 bridge — 평형 분포 ξ_eq 가 다음 deliverable.

Derivation blocks ≥ 10 (각 식 A1, A2, A3 의 단계별 도출 + χ 의 정량 해석 + 차원 점검).

Gate `PASS_EFFECTIVE_BARRIER_v2`.

---

## §10. Phase 5_v2 — §5 평형 분포 ξ_eq = erf 도출 (cumulative 321–400)

- §5.1 평형 진행률의 의미 — 평형 시 (k → ∞ 또는 dξ/dt = 0 한계) 에서의 ξ.
- §5.2 가우시안 분포의 통계역학적 근거 — graphite staging 의 local strain, Cahn-Hilliard mean-field 등에서 가우시안 분포가 자연 발생하는 메커니즘 (사용자 명시 "약간 가우시안 피크 형상" 의 물리 근거).
- §5.3 dξ_eq/dV = 가우시안 → ξ_eq = erf 의 누적 적분 도출 (학부 수준 미적분).
- §5.4 σ(T) 의 학부 수준 의미 — 가우시안 폭, kT 비례 가능성 (DQ-v2-3).
- §5.5 U_j(T) 의 학부 수준 의미 — 평형 전위, T 의존성 (Nernst 류).
- §5.6 logistic vs erf 비교 — 사용자 명시 가우시안 채택의 학부 수준 정당화.

Gate `PASS_EQUILIBRIUM_DIST_v2`.

---

## §11. Phase 6_v2 — §6 속도상수 k Arrhenius (cumulative 401–480)

- §6.1 Arrhenius 식의 학부 수준 도출 (transition state theory).
- §6.2 prefactor ν(T) 의 의미.
- §6.3 ΔG_eff 와의 결합 → k(T, A) 의 형태.
- §6.4 T 와 A 의 결합 효과 — 사용자 의도 I3 + I5.
- §6.5 ν_j(T) 의 functional form (DQ-v2-4).

Gate `PASS_RATE_CONSTANT_v2`.

---

## §12. Phase 7_v2 — §7 진행률 동역학 (cumulative 481–540)

- §7.1 dξ/dt = k (ξ_eq - ξ) (A6) 의 학부 수준 도출 (1차 ODE, irreversible thermodynamics).
- §7.2 정전류 q 좌표 변환 (A7).
- §7.3 초기 조건.
- §7.4 평형 한계 (k → ∞).

Gate `PASS_KINETICS_v2`.

---

## §13. Phase 8_v2 — §8 시간 적분형 (cumulative 541–600)

- §8.1 dξ/dt 의 시간 적분 → ξ(t) = ξ(0) + ∫_0^t dt' k(t') (ξ_eq(t') - ξ(t')) (A9).
- §8.2 Volterra equation form 의 인식 — integrand 의 self-reference.
- §8.3 Fredholm vs Volterra 의 학부 수준 구분.
- §8.4 k, ξ_eq 가 시간 의존 시 self-consistent 한 이유.

Gate `PASS_VOLTERRA_v2`.

---

## §14. Phase 9_v2 — ★ §9 Refs 6/7 비율 치환 closed-form 도출 (cumulative 601–740)

★ 본 Chapter 의 load-bearing phase. 사용자 박사학위 연구의 정확한 응용.

- §9.1 Refs 6, 7 의 배경 — Lee/Son/Sung/Chong (2011) + Son/Kim/Kim/Kim/Lee (2013) + JCP 2017 의 핵심 기법.
- §9.2 Fredholm 적분 방정식 제2종의 학부 수준 정의.
- §9.3 단순 case 의 closed-form ξ^{simple}(t) = 1 - exp(-k t)(ξ_eq - ξ(0)) 도출 (k, ξ_eq 시간 무관).
- §9.4 ★ 비율 치환 ξ(t)/ξ(t') ≈ ξ^{simple}(t)/ξ^{simple}(t') 의 학부 수준 정당화.
- §9.5 비율 치환 적용 → ξ(t) closed-form (A11) 도출 의 단계별 algebra.
- §9.6 closed-form 의 차원 점검 + 한계 점검 + 정확도 영역 (저 |I|, 큰 χ A, etc.).

Derivation blocks ≥ 15 (Refs 6/7 의 (33)→(34)→(39) 패턴 단계별 적용).

Gate `PASS_REF67_CLOSED_FORM_v2`.

---

## §15. Phase 10_v2 — §10 ICA 관측식 + 꼬리 모양 T 의존성 (cumulative 741–820)

- §10.1 (dQ/dV)_j = Q_{j,tot} dξ_j/dq / (dV_n,app/dq) (A12) 의 학부 수준 도출.
- §10.2 평형 한계 (ξ → ξ_eq) 에서 dQ/dV ∝ Q_{j,tot} dξ_eq/dV = 가우시안 → 평형 시 peak 가우시안 형상 (사용자 I4 정합).
- §10.3 비평형 (lag) 시 dξ/dq 의 꼬리 형성 메커니즘 — (A11) closed-form 으로 정량.
- §10.4 ★ 저T 의 꼬리 길이 정량 (사용자 I3 직접) — k 작음 → lag 큼 → dξ/dq 가 더 멀리 까지 0 으로 천천히 수렴.
- §10.5 고T 의 꼬리 짧음 정량.
- §10.6 χ A 가 꼬리 길이에 미치는 효과.

Gate `PASS_ICA_TAIL_v2`.

---

## §16. Phase 11_v2 — ★ §11 피팅 가능 논리식 (cumulative 821–900)

★ 본 Chapter 의 종료점. 사용자 의도 I6.

- §11.1 피팅 파라미터 정리 — ΔH_a,j, ΔS_a,j, χ_j, ν_j(T), U_j(T), σ_j(T) (DQ-v2-3, DQ-v2-4 결정 적용).
- §11.2 closed-form (A11) 의 파라미터 의존성 명시.
- §11.3 피팅 가능한 실험 관측 — 다중 T 의 dQ/dV 꼬리 길이 (정량).
- §11.4 식별성 분석 — 파라미터의 상관성, 일반화된 모델 vs 줄어든 모델.
- §11.5 본 spine 의 피팅 가능 논리식 = 사용자 의도 I6 deliverable.

Gate `PASS_FITTING_EXPR_v2`.

---

## §17. Phase 12_v2 — §12-§16 종합 (cumulative 901–1000)

- §12 ver5 §8 장벽 분포 평균 (advanced note 보조 단원, DEC-7).
- §13 ρ(μ; q, T) continuous 일반화 (appendix 선택, DEC-8).
- §14 ver.2 (Chapter 2 발열) 로 전달되는 식 (continuous-form transfer placeholder).
- §15 자기 검수 체크리스트 (≥ 20 항).
- §16 참고문헌 (ver5 5 ref + JCP 2017 + Ref 6 DOI + Ref 7 DOI + 추가).

Gate `PASS_COMPREHENSIVE_v2`.

---

## §18. Phase F1_v2 ~ F5_v2 (cumulative 1001–1220)

- F1: LaTeX 빌드 환경 + 첫 시도 (xelatex + kotex).
- F2: 빌드 에러 정정 루프 (최대 3 회).
- F3: PDF 사용자 검수 (★ Decision Gate `GATE_F3_v2`).
- F4: 사용자 피드백 반영.
- F5: 최종 commit + Chapter 2 후속 roadmap 결정.

---

## §19. Test Plan (v2 series)

| # | Item | Method | Pass Criterion |
|---|---|---|---|
| T-v2-1 | spine A1-A12 모두 §4-§11 본문 내 명시 | 본문 scan | 12 식 모두 본문에 |
| T-v2-2 | 사용자 의도 I1-I6 모두 §1 내 명시 | 본문 scan | 6 의도 모두 |
| T-v2-3 | Charter v2 §3 anti-pattern 위반 0 | Dim #11 Pass 1+2+3 | 0 FAIL |
| T-v2-4 | Charter v2 §5 Writing Precision Standard 준수 | 매 phase result audit | 0 FAIL, WARN 처리 |
| T-v2-5 | Refs 6/7 적용 (§9_v2) closed-form ξ(t) 도출 완성 | §9_v2 본문 | A11 명시 |
| T-v2-6 | 꼬리 모양 T 의존성 정량 도출 (§10_v2) | §10.4 + §10.5 | 정량 표현 명시 |
| T-v2-7 | 피팅 가능 논리식 (§11_v2) closed-form 의 피팅 파라미터 명시 | §11.5 | 6 파라미터 list |
| T-v2-8 | ver5 §6.1-§6.4 의 활용 정합 + §6.5 step 처리 폐기 명시 | §4_v2 본문 | 인용 정합 |
| T-v2-9 | ver5 §5.2 erf 의 활용 + §5.1 logistic 폐기 명시 | §5_v2 본문 | 인용 정합 |
| T-v2-10 | LaTeX 빌드 PASS | F1_v2 빌드 | exit 0 |
| T-v2-11 | 사용자 PDF 검수 통과 | F3_v2 | user GO |

---

## §20. Assumptions

- A-v2-1. Charter v2 DEC-1~DEC-8 user-acknowledged (DEC-2 V_n=lookup 기본, DQ-v2-1 검토 가능).
- A-v2-2. Phase 9_v2 의 Refs 6/7 비율 치환 적용에 ξ^{simple} = 1 − exp(−kt)(ξ_eq − ξ(0)) 채택 (DQ-v2-2, Phase 9_v2 진입 시 검증).
- A-v2-3. σ_j(T), ν_j(T) functional forms (DQ-v2-3, DQ-v2-4) 는 Phase 5_v2, 6_v2 진입 시 결정.
- A-v2-4. χ_j 추정 (DQ-v2-5) 는 Phase 4_v2 §4.3 본문에서 처리.
- A-v2-5. Cumulative step v2 = 1 부터 (DEC-6).
- A-v2-6. v1 산출물 (Claude/old/) 의 LaTeX 본문 미사용; v1 의 ``파악된 사실'' (ver5/rechecked2 의 §·식 위치, JCP DOI) 만 input 사실로 재참조.

---

## §21. Decision Queue

| ID | 항목 | Resolution timing |
|---|---|---|
| DQ-v2-1 | V_n 결정 = 외부 lookup (DEC-2 기본) — user clarification 시 implicit 으로 변경 | 사용자 직접 또는 Phase 검수 |
| DQ-v2-2 | Refs 6/7 의 ξ^{simple} 후보 (A-v2-2) | Phase 9_v2 진입 시 |
| DQ-v2-3 | σ_j(T) functional form | Phase 5_v2 |
| DQ-v2-4 | ν_j(T) functional form | Phase 6_v2 |
| DQ-v2-5 | χ_j 추정 | Phase 4_v2 |

---

## §22. Meta

- 본 master roadmap v2 는 Charter v2 의 governance 하에서 v2 series 작업의 가이드.
- v1 (Claude/old/) 의 master roadmap 은 본 v2 가 supersede; v1 의 어떤 본문 내용도 본 v2 의 작업에 영향 X.
- 각 phase 진입 시 별 phase plan 작성 (RO_SkillDict pattern).
- Phase 0_v2 (현재) → Phase 1_v2 (다음 turn) 자동 진입 (per `feedback_plan_continuation_until_done`).
