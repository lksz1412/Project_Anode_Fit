# Master Roadmap v3 — 흑연 음극 ICA 꼬리 이론 (Chapter 1 from-scratch 재작성)

**Date**: 2026-05-28
**Series**: v3 (from-scratch). v2 전체는 `Claude/old/v2/` 로 아카이브 (참조 전용).
**Supersedes**: `Claude/old/v2/plans/MASTER_ROADMAP_v2.md` (closed)
**Predecessor 입력 (참조)**: `Claude/results/CROSSCHECK_v2_vs_v3_ChatGPT.md`, `Claude/results/SELF_REVIEW_v2_DELIVERABLES.md`, 문헌 grounding 리서치 (본 문서 §8 에 통합)
**상태**: **계획 (PLAN) — 사용자 GO 대기. 본 turn 에 LaTeX 본문 작성 X.**

---

## §0. 사용자 의도 (verbatim, 절대 기준)

> "LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히
> 피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 피크 꼬리의 개형이
> 늘어지느냐 빨리 떨어지느냐가 달라지는것을 확인했다. 특히 온도가 낮을때는 꼬리가
> 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는 현상이 관측되었어. 원래라면
> 그렇게 온도에 대해 약간 가우시안 피크 형상이 나타나고 더이상 진행이 안될 것으로
> 생각되는데 그 온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를
> 낮추는 효과가 있다고 봤고 그 유효 배리어의 논리를 확정하고 그 것을 이용해 피크의
> 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심이야."

**5-28 추가 표준 (사용자 명시)**: "논문을 위해 완전무결한 비약이 없는 물리적 의미를
중시하며, 사용되는 가정도 전부 논문이나 이론 베이스의 타당한 근거가 있는 것들만
반영." → 본 v3 의 **governing standard** (§2).

**사용자 4 원칙 (불변)**: P1 피팅 솔버 코드 X · P2 ICA 이론 배경 · P3 논문/특허 수준 정밀도 ·
P4 모든 수식 전개 논리적 비약 X + 생략 X + 학부생 수준.

**5-28 해석 정정 (사용자 명시)**: §0 verbatim 의 "약간 가우시안 피크 형상" 은
\*\*"뾰족하게 솟은 피크"를 가리키는 예시 표현일 뿐, 평형 분포가 가우시안(erf)이라고
확정한 것이 아니다.\*\* → 평형 isotherm 의 함수 형태는 사용자가 못 박은 제약이 아니라
\*\*grounding + 데이터로 결정\*\*할 열린 사안 (DQ-v3-1). 이 정정은 v3 가 erf 를 grounded
primary 에서 내리고 lattice-gas 를 primary 로 둔 결정(§7 pivot 1)을 직접 정당화한다.

---

## §1. Summary

본 v3 는 Chapter 1 을 **백지에서 다시** 작성한다. v2 와의 결정적 차이는 **"모든
가정이 출판 문헌 또는 확립 이론으로 grounding 되어야 하며, grounding 없는 가정은
established 로 쓰지 않고 flagged hypothesis 로만 표기"** 라는 표준을 **1급 governance**
로 격상한 것이다. 이 표준을 기계적으로 적용한 결과, v2 대비 **과학적 pivot 5 건**이
강제된다 (§7). 산출물 = grounding 된 Chapter 1 LaTeX + Assumption Ledger (가정-인용
대장) + 검증 protocol.

---

## §2. ★ Governing Standard — Assumption Grounding Protocol (AGP)

본 v3 의 모든 phase 를 지배하는 최우선 규칙.

**AGP-1 (근거 의무).** 본문에서 사용하는 모든 가정·식·관계는 다음 중 하나의 grounding
을 가져야 한다: (a) peer-reviewed 출판 문헌의 명시 인용, (b) 확립 이론(교과서 canon)
으로부터의 1st-principles 유도. 둘 다 없으면 **established 로 사용 금지**.

**AGP-2 (3-tier 상태 표기).** 각 가정은 Assumption Ledger (§8) 에서 상태를 갖는다:
- **GROUNDED** — 직접 문헌/이론 근거 있음. 본문에서 established 로 사용 가능.
- **BOUNDED** — 근거 있으나 유효 범위 제한 (예: 선형화는 평형 근처만). 본문에서 *유효
  범위를 명시*하고 사용.
- **FLAGGED (hypothesis/ansatz/novel)** — 직접 근거 없음 (analogy·경험·신규). 본문에서
  반드시 "가설/ansatz/신규 기여"로 명시하고, established 사실처럼 쓰지 않음.

**AGP-3 (무비약).** v2 의 Dim #11 (정의식 anti-pattern 부재) + Writing Precision §5 +
P4 (학부 수준 무비약) 유지. 추가로 **"물리적 의미 우선"**: 모든 식은 그 물리적 의미를
prose 로 먼저 제시한 뒤 수식화.

**AGP-4 (유효 범위 명시).** BOUNDED 가정은 "어디서 성립/어디서 깨지는가"를 항상 병기
(예: BV 선형 lowering 은 Marcus 곡률에 의해 큰 |V−U| 에서 깨짐).

**AGP-5 (검증 루프).** 매 phase = 작업 commit + 검토·정정 commit 페어 (10차원×3-Pass
Ralph Wiggum). 단, v2 의 교훈 — **"내부 일관성 ≠ 과학적 완결성"** — 에 따라 검토는
*가정의 grounding 상태*까지 감사 (내부 일관성만 보지 않음).

---

## §3. Objective & Background

**Objective**: 사용자 의도 §0 의 deliverable — ICA 꼬리 거동의 온도 의존성을 설명하는
*피팅 가능한 논리식/모델* — 을 **모든 가정이 grounding 된 출판급**으로 완성.

**Background — 왜 재작성인가**:
- v2 self-review (`SELF_REVIEW_v2_DELIVERABLES.md`) 가 노출: v2 는 내부 논리는 무결하나
  **모델링 전제 3건을 근거 없이 확정**(erf primary, V_n 외부 lookup, closed-form 위상).
- cross-check (`CROSSCHECK_v2_vs_v3_ChatGPT.md`): v2·v3 코어는 동일, 차이는 grounding
  으로 판정 가능.
- 사용자 5-28 표준: grounding 을 1급 기준으로. → v2 의 미근거 확정을 그대로 둘 수 없어
  **백지 재작성** (사용자 명시).

---

## §4. Scope

**In (본 v3 Chapter 1)**: 방전(또는 단일 branch) 흑연 음극 ICA 꼬리의 평형 isotherm +
유효 배리어 + relaxation 동역학 + 전하보존 implicit V_n + 적분방정식/비율치환 +
꼬리 T-의존 신규 유도 + 경쟁 메커니즘 falsification + 피팅 모델 + 검증 protocol.

**Out (후속 chapter, v3-ch2~)**: 열 해석(가역/비가역 heat), 전기화학 Butler-Volmer
완전 전개, 충방전 hysteresis, full-cell, 수치 solver 구현 (P1). v3-ch2~ 는 Chapter 1
완료·검수 후 별도 roadmap (ChatGPT v3 의 ch2-6 구조를 grounding 표준으로 재작성).

---

## §5. Inputs (Read 대상)

- 원본 (수정 X): `Claude/docs/graphite_ica_dynamic_ver5.tex`,
  `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex`
- 외부 비교본 (수정 X): ChatGPT v3 `graphite_ica_ch1_ch6_physical_v3_rechecked.tex`
  (사용자 제공, charge-balance 6장)
- 근거 입력: `Claude/results/CROSSCHECK_v2_vs_v3_ChatGPT.md`,
  `Claude/results/SELF_REVIEW_v2_DELIVERABLES.md`
- 참조 전용 (재사용 금지, 사실 데이터만): `Claude/old/v2/**`
- 글로벌 지침·메모리: `Claude/_claude/**`

---

## §6. ★ Grounded Spine S1–S13 (v3 정식 골격)

각 항목 끝 [상태] = AGP-2 tier. 근거는 §8 Assumption Ledger 참조.

| ID | 골격 식/관계 | 상태 |
|---|---|---|
| **S1** | 전하/site 보존 `Q_cell·q = Q_bg(V_n,T) + Σ_j Q_{j,tot} ξ_j` → V_n 암시적 결정 | GROUNDED (DFN 1993, Newman) |
| **S2** | 평형 isotherm (균질 baseline) = lattice-gas/regular-solution `μ(ξ)` → `ξ_eq(V_n,T)`; ideal 극한 = logistic | GROUNDED (McKinnon-Haering 1983, Bazant 2013) |
| **S3** | (옵션) broadening 메커니즘: 균질 상호작용(regular-solution) 또는 불균질 전이중심전위 분포 `p(U_j)`. 함수 형태(가우시안 등)는 **미확정 — 데이터로 결정**. "가우시안"은 뾰족 peak 예시일 뿐 목표 아님 | **DQ + FLAGGED** (불균질 가우시안은 Bässler GDM analogy/경험 peak-fit 뿐, 직접 근거 부재 → ansatz 로만) |
| **S4** | 활성화 자유에너지 `ΔG_a(T) = ΔH_a − T·ΔS_a` | GROUNDED (Eyring 1935, Evans-Polanyi 1935) |
| **S5** | 전위 배리어 lowering `ΔG_eff = ΔG_a − χ·F·(V_n,drive − U_j)` | BOUNDED (BV/BEP 선형; Marcus 1956 가 곡률·유효범위 한정 — 큰 |V−U| 에서 깨짐) |
| **S6** | 속도 상수 Eyring `k = (k_B T/h)·κ_j(T)·exp(−ΔG_eff/RT)` | GROUNDED (Eyring); ν=κ·k_BT/h 해석 명시 |
| **S7** | relaxation `dξ_j/dt = k_j(ξ_eq,j − ξ_j)` | BOUNDED (평형근처 선형화: De Donder/De Groot-Mazur/Onsager; 평형서 멀면 무효, k는 ξ_eq·T 의존) |
| **S8** | (옵션) 배리어 분포 `ρ_j(g)` → dispersive/stretched kinetics | BOUNDED (Plonka; 역매핑 비유일 — flag) |
| **S9** | 시간적분 → 적분방정식. ★ Fredholm(정상상태) vs Volterra(시간상한 t) **정확 구분**; 비율치환/propagator (Refs 6/7) 적용성 검증 | GROUNDED(Refs 검증) + 적용성 **DQ** |
| **S10** | ICA 관측식 `(dQ/dV)_j` = 전하보존 미분 (chain rule) | GROUNDED (DFN 미분) |
| **S11** | ★ 꼬리 T-의존 (저T 길고 고T 짧음) = kinetic lag 의 신규 유도 | **FLAGGED novel** (선행 모델 부재 — S1-S10 에서 유도, 가정 금지) |
| **S12** | ★ 경쟁 꼬리원 falsification (분극 R_n, 불균질 width, transport, 배리어분포 비유일) | 방법론 (필수) |
| **S13** | 피팅 모델 + 식별성 + 검증 protocol (저속 OCV, GITT, rate/T series) | GROUNDED (Dubarry 2022, Fly 2020; 식별성=독립 실험) |

---

## §7. ★ v2 대비 강제된 과학적 Pivot 5건 (grounding 의 직접 결과)

1. **평형 isotherm: erf primary → lattice-gas primary.** erf/Gaussian 누적은 흑연
   intercalation 에 대한 *열역학 유도가 문헌에 없다* (리서치 확인). 따라서 GROUNDED
   primary 는 lattice-gas μ(ξ) (McKinnon-Haering/Bazant). **사용자 5-28 정정으로
   "가우시안"은 함수 형태 확정이 아니라 "뾰족한 peak" 예시였음이 분명해졌다** → erf 를
   목표로 재현할 의무 없음. 평형 형태는 grounded lattice-gas 를 baseline 으로 두고,
   broadening 메커니즘·함수형태는 데이터로 결정(DQ-v3-1). 가우시안 disorder 는 *여러
   가능 broadening 중 하나의 FLAGGED 옵션*일 뿐 특권적 목표 아님.
2. **V_n: 외부 lookup → 전하보존 implicit.** DFN/Newman grounding. (v2 DQ-v2-1 종결.)
3. **배리어 lowering: 무한정 선형 → Marcus-bounded 선형.** 선형은 평형근처 leading-order;
   큰 driving force 에서 곡률(Marcus). 유효범위 명시 (AGP-4).
4. **closed-form: primary → 검증-tier 근사.** 비율치환은 Fredholm 2nd-kind 기법
   (Refs 6/7 검증). 시간의존 Volterra 적용성은 **검증 대상(DQ)**; direct 적분 대비
   오차 bound 제시 후 사용.
5. **꼬리 T-의존: 가정된 결론 → 유도된 신규 결과 + falsification.** 선행 모델 부재이므로
   S1-S10 에서 유도하고, 경쟁 꼬리원(특히 R_n 분극)을 *배제*해야 배리어 귀속 성립(S12).

---

## §8. Assumptions — ★ Assumption Ledger (grounding 대장, 본 계획의 backbone)

> 상태: GROUNDED / BOUNDED / FLAGGED. 근거는 Phase 1 에서 원문 대조로 최종 lock.

| # | 가정 | 물리적 의미 | Grounding (문헌/이론) | 상태 | 유효범위·주의 |
|---|---|---|---|---|---|
| AL-1 | `ΔG_a=ΔH_a−TΔS_a`, Eyring `k=(k_BT/h)e^{−ΔG/RT}` | 활성화 자유에너지·천이상태 | Eyring 1935 (DOI 10.1063/1.1749604); Evans-Polanyi 1935 (10.1039/TF9353100875) | GROUNDED | prefactor 는 k_BT/h — ν 임의값 아님 |
| AL-2 | `ΔG_eff=ΔG_a−χF(V−U)` | 전위가 배리어를 선형 lowering | Butler-Volmer (Bard&Faulkner Ch.3); BEP Evans-Polanyi 1938 (10.1039/TF9383400011); Marcus 1956 (10.1063/1.1742723) | BOUNDED | 선형=leading-order. 큰 |V−U|=Marcus 곡률/역영역 → 무효. "Marcus가 선형을 전역 정당화"라 주장 금지 |
| AL-3a | 평형 isotherm = lattice-gas/regular-solution μ(ξ) (ideal→logistic) | 균질 site occupancy 열역학 | McKinnon&Haering 1983 (Mod.Asp.Electrochem.15); Bazant 2013 (10.1021/ar300145c) | GROUNDED | width w=RT/F (ideal) 또는 상호작용 보정 |
| AL-3b | erf/Gaussian 누적 isotherm (site-disorder) | 전이중심전위 불균질 분포 (broadening 의 한 옵션) | Bässler GDM 1993 (organic semic., 10.1002/pssb.2221750102) analogy; 경험 dQ/dV Gaussian-fit (Dubarry) | **FLAGGED ansatz** | 흑연 intercalation 직접 열역학 근거 **부재**. 사용자 "가우시안"은 뾰족 peak 예시일 뿐 형태 확정 아님 → 목표 아닌 옵션. "ansatz"로만 사용 |
| AL-4 | 흑연 staging (Stage 4/3/2L/2/1, LiC6/LiC12) → dQ/dV peaks | 상전이의 전압 신호 | Dahn 1991 (10.1103/PhysRevB.44.9170); Ohzuku 1993 (10.1149/1.2220849) | GROUNDED | 2L = liquid-like stage-2 (별도 stage 번호 아님) |
| AL-5 | `dξ/dt=k(ξ_eq−ξ)` | 평형으로의 1차 완화 | De Donder 1936; De Groot-Mazur 1962 Ch.X; Onsager 1931; Eigen-De Maeyer 1963 | BOUNDED | 임의 rate law 의 평형근처 Taylor 1차. 평형서 멀면 무효; k=k(ξ_eq,T) |
| AL-6 | `ρ_j(g)` 배리어분포 → stretched kinetics | 활성화에너지 분산 | Kohlrausch 1854; Williams-Watts 1970; Plonka *Dispersive Kinetics* 2001 | BOUNDED | stretched→분포 역매핑 **비유일** (retrapping도 재현). 옵션 |
| AL-7 | 비율치환/propagator (Refs 6/7) | self-consistent 적분방정식 폐형화 | Lee 2011 (10.1063/1.3565476); Son 2013 (10.1063/1.4802584, "Fredholm 2nd-kind 해법") | GROUNDED(존재·기법) + **DQ(적용성)** | Refs 는 **Fredholm**. 본 시간의존은 **Volterra** → 적용성 Phase 10 검증 |
| AL-8 | ICA 꼬리 T-의존 kinetic 모델 | 저T 작은 k 큰 lag 긴 꼬리 | **선행 출판 모델 부재** (리서치 확인) | **FLAGGED novel** | S1-S10 에서 유도. 신규 기여 = 논문 가치, 단 가정 금지·falsify 필수 |
| AL-9 | 전하보존 implicit V_n | 전위가 site/charge balance 로 결정 | Doyle-Fuller-Newman 1993 (10.1149/1.2221597); Newman&Thomas-Alyea | GROUNDED | SPM/lattice-gas μ(ξ) 극한서 외부 OCV lookup 과 등가 |
| AL-10 | ICA 진단·rate/T broadening | dQ/dV 진단 도구·rate 의존 | Dubarry-Anseán 2022 (10.3389/fenrg.2022.1023555); Fly-Chen 2020 (10.1016/j.est.2020.101329) | GROUNDED | C/6 최적; rate↑ broadening |

(출처 링크: 리서치 보고 — Eyring/TST, Butler-Volmer, Marcus, McKinnon-Haering, Bazant,
Dahn, Lee/Son SNU·AIP, Dubarry, Fly, Plonka, De Groot-Mazur, Bässler GDM, DFN. Phase 1
에서 원문 대조 후 DOI 확정 lock.)

---

## §9. Phase 분해 (cumulative step, from-scratch 신규 series 1–1320; 최소 기준점)

| Phase | Steps | Block | Purpose | Gate (요지) |
|---|---:|---|---|---|
| **0** | 1–60 | foundation | 아카이브 확인 + Charter v3 (verbatim + AGP + grounded spine S1-S13) + 신규 ledger init | Charter v3 + AGP 5조 + spine 13 lock |
| **1** | 61–140 | ★ grounding | Assumption Ledger 원문 대조 lock (AL-1~10 DOI 확정, 3 FLAGGED 검증) | 각 AL 상태 확정 + FLAGGED 3건 근거 명시 |
| 2 | 141–200 | §1 | 머리말+동기+가설 (verbatim, O1-O2, 가설을 grounded 틀로) | 가설 각 항 → AL 매핑 |
| 3 | 201–260 | §2 | 기호·단위 + 3 전위 + 전하보존 spine(S1) | 모든 기호 §2 내 정의 |
| 4 | 261–320 | §3 | 흑연 staging (AL-4) | Dahn/Ohzuku 인용 + peak fusion 근거 |
| **5** | 321–400 | §4 | ★ 평형 isotherm: lattice-gas μ(ξ) primary(AL-3a) + 가우시안 disorder ansatz(AL-3b, FLAGGED) → erf 창발 | lattice-gas GROUNDED 유도 + erf 를 ansatz 로 명시 |
| **6** | 401–470 | §5 | ★ 유효배리어 ΔG_eff (AL-2) + Marcus 유효범위 | 선형 lowering + Marcus bound 병기 |
| 7 | 471–530 | §6 | 속도상수 Eyring (AL-1) | κ_j·k_BT/h 해석 명시 |
| 8 | 531–590 | §7 | relaxation 동역학 (AL-5) | 선형화 유효범위 명시 |
| **9** | 591–660 | §8 | ★ 전하보존 implicit V_n + DAE 구조 (AL-9) | V_n root 존재·단조성 조건 |
| **10** | 661–760 | §9 | ★ 적분방정식: Fredholm vs Volterra 정확 구분 + 비율치환 적용성 검증 (AL-7, DQ-v3-2) | Fredholm/Volterra 판정 + 적용성 결론(또는 한계 명시) |
| **11** | 761–840 | §10 | ★ ICA 관측식(S10) + 꼬리 T-의존 신규 유도 (AL-8) | 저T 긴 꼬리 = kinetic 유도 (가정 아님) |
| **12** | 841–920 | §11 | ★ 경쟁 꼬리원 falsification (S12) | R_n/width/transport 배제 절차 명시 |
| 13 | 921–1000 | §12 | 피팅 모델 + 식별성 + 검증 protocol (AL-10) | 파라미터-실험 매핑 + 식별성 표 |
| 14 | 1001–1080 | §13 | 종합 + 자기검수(grounding 감사 포함) + 참고문헌 | 모든 본문 가정 → AL 인용 0 누락 |
| F1 | 1081–1120 | build | xelatex/Overleaf 빌드 | PDF 생성 (사용자 환경) |
| F2 | 1121–1160 | build-fix | 빌드 에러 정정 | 0 error |
| **F3** | 1161–1200 | review | ★ PDF 사용자 검수 (Decision Gate) | 사용자 승인 |
| F4 | 1201–1260 | feedback | 피드백 반영 | 반영 완료 |
| F5 | 1261–1320 | closure | 최종 commit + ch2~ 후속 결정 | 종료 |

(step 수 = 최소 기준점, `feedback_step_granularity_flexibility` 에 따라 확장 OK.)

---

## §10. Gates (verifiable only, `feedback_gate_design_principle`)

- 정성 "적절해 보임" 류 gate 금지. 예: "erf 가 ansatz 로 *명시되었는가*"(확인 가능) ○ /
  "isotherm 이 맞는가"(정성) ✗ → DQ 로.
- 각 phase gate = §9 표의 verifiable 조건 + (공통) AGP-1~4 준수 + Dim #11 0-FAIL +
  Writing Precision §5 0-FAIL + 본문 사용 가정이 모두 AL 에 인용됨.

---

## §11. Test Plan + Decision Queue + Sprint Contract + 위험

### Test Plan
- T-v3-1: 본문 모든 가정이 AL 에 인용 (0 누락).
- T-v3-2: FLAGGED 3건(AL-3b, AL-7 적용성, AL-8)이 본문서 "established"로 안 쓰임.
- T-v3-3: BOUNDED 가정(AL-2,5,6)에 유효범위 병기.
- T-v3-4: spine S1-S13 차원 점검 0-FAIL.
- T-v3-5: Ralph Wiggum Pass3 (grounding 감사 포함) 0-FAIL.

### Decision Queue (사용자/데이터 대기)
- **DQ-v3-1**: 평형 isotherm/broadening 의 **함수 형태 자체가 미확정** (사용자 "가우시안"은
  형태 확정 아님). lattice-gas 균질 vs 불균질 disorder(가우시안 등) 지배, 그리고 꼬리
  감쇠가 지수형/가우시안형/멱급수형 중 무엇인지 → **저속 OCV peak near-peak 감쇠 형상**
  실측으로 결정 (`log dQ/dV` vs `(V−U)` → 지수 / vs `(V−U)²` → 가우시안 / log-log → 멱급수).
  사용자 데이터 필요. 데이터 전까지 lattice-gas baseline + 형태 dual/multi-track 병기.
- **DQ-v3-2**: 비율치환(Fredholm 기법)의 시간의존 Volterra 적용성 → Phase 10 검증.
- **DQ-v3-3**: χ_j 크기 / Marcus 영역 진입 여부.
- **DQ-v3-4**: 꼬리 경쟁원 판별 결과 (Phase 12).
- **DQ-v3-5**: ν_j(T) 형태 (Eyring linear-T 기본).

### Sprint Contract
- [ ] Phase 0-14 + F1-F5 (또는 확장) 완료.
- [ ] AL 0 누락 + FLAGGED 미오용 + BOUNDED 유효범위 병기.
- [ ] 매 phase commit 페어 (작업+검토).
- [ ] F3 사용자 검수 통과.

### 위험
- R1: FLAGGED 3건이 본문서 슬그머니 established 화 → AGP-2 감사로 차단.
- R2: erf/lattice-gas 미결(DQ-v3-1)로 §4 정체 → **양 형태 병기(dual-track)**로 진행,
  데이터 시 확정. 정지 사유 아님.
- R3: 비율치환 Volterra 적용 실패 시 → direct 적분 reference 로 fallback (closed-form
  은 가속·검증 tier).

---

## §12. Correction History

| 일자 | 변경 |
|---|---|
| 2026-05-28 | v3 신설. 사용자 "챕터1 처음부터 재작성 + v2 old 로 + 계획서부터" 수신. v2 전체 `Claude/old/v2/` 아카이브. 문헌 grounding 리서치 통합 → Assumption Ledger §8. AGP(가정 grounding 표준) 1급 격상. v2 대비 과학적 pivot 5건 명시(§7). cross-check·self-review 를 근거 입력으로 유지. **계획 상태 — GO 대기, 본문 작성 X.** |
| 2026-05-28 | 사용자 정정 "가우시안 관측은 뾰족한 피크 예시일 뿐 가우시안 확정 아님" 반영. §0·§6 S3·§7 pivot 1·§8 AL-3b·§11 DQ-v3-1·§13 갱신: 평형 isotherm 함수 형태를 사용자 제약이 아닌 grounding+데이터 결정 사안으로 명확화. erf 는 목표 아닌 FLAGGED 옵션. v3 의 erf→lattice-gas pivot 이 이 정정으로 강화됨. |

---

## §13. 진입 조건

- 본 계획 **사용자 GO** 시 Phase 0 진입. GO 후엔 정지 4조건(Decision Gate / 새 의존성 /
  FAIL gate / 사용자 stop) 외 마지막 phase 까지 자동 진행 (`feedback_plan_continuation_until_done`).
- DQ-v3-1(평형 isotherm 함수 형태)은 데이터 대기지만 **lattice-gas baseline +
  형태 multi-track 으로 진행 가능** — 정지 사유 아님.
- **확인 요청**: (a) 본 grounded spine·pivot 5건 방향 승인? (b) Chapter 1 단독 우선
  (ch2~ 후속) 승인? (c) 평형 형태는 grounded lattice-gas baseline 위에서 형태
  미확정 채로 진행(데이터 시 확정) 승인?
