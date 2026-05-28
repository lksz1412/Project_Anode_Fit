# Charter v3 — Graphite Anode ICA Tail Theory (Chapter 1 from-scratch)

**Date**: 2026-05-28 · **Supersedes**: `Claude/old/v2/results/CHARTER_v2.md`
**Plan**: `Claude/plans/MASTER_ROADMAP_v3.md` · **Assumption Ledger**: `Claude/results/ASSUMPTION_LEDGER_v3.md`

---

## §00. 사용자 의도 (verbatim — 절대 기준)

> "LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히
> 피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 피크 꼬리의 개형이
> 늘어지느냐 빨리 떨어지느냐가 달라지는것을 확인했다. 특히 온도가 낮을때는 꼬리가
> 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는 현상이 관측되었어. 원래라면
> 그렇게 온도에 대해 약간 가우시안 피크 형상이 나타나고 더이상 진행이 안될 것으로
> 생각되는데 그 온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를
> 낮추는 효과가 있다고 봤고 그 유효 배리어의 논리를 확정하고 그 것을 이용해 피크의
> 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심이야."

### §00.1 사용자 정정 (2026-05-28, 절대 반영)
- **"가우시안"은 sharp peak 를 가리키는 예시 표현일 뿐, equilibrium distribution 이
  Gaussian(erf) 이라는 형태 확정이 아니다.** → isotherm 형태는 grounding + data 로 결정.
- **Activation energy barrier 는 맞다 (유지).** 사용자가 "쓸모없다"고 한 것은 ChatGPT 의
  실수 — "특정 지점을 넘으면 0→1 로 갑자기 점프"하는 **step-function 식 비약**을 지칭.
  → activation barrier spine 유지, **discontinuous step jump 는 금지**.

### §00.2 사용자 4 원칙
P1 피팅 solver 코드 X · P2 ICA(dQ/dV) theoretical background · P3 paper/patent 수준
정밀도 · P4 모든 derivation 의 logical leap X + omission X + 학부 수준.

### §00.3 작성 규칙
- **Korean prose + English academic terms** (`feedback_korean_prose_english_terms`).
- **Commit 시 Codex/ 동반** (`feedback_commit_includes_codex`).

---

## §1. Governing Standard — Assumption Grounding Protocol (AGP)

(상세: MASTER_ROADMAP_v3 §2.) 모든 assumption 은 GROUNDED / BOUNDED / FLAGGED 상태를
갖고, FLAGGED 는 established 로 사용 금지. 모든 본문 assumption 은 Assumption Ledger
인용. step-function·0→1 급점프·max·min·Heaviside·hard-switch 정의식 금지 (smooth only).

---

## §2. Grounded Spine S1–S13

(상세: MASTER_ROADMAP_v3 §6, Assumption Ledger AL-1~10.)

- S1 charge/site conservation → implicit `V_n` [AL-9]
- S2 equilibrium isotherm = lattice-gas `μ(ξ)` (smooth) [AL-3a]; broadening option [AL-3b FLAGGED]
- S4 activation free energy `ΔG_a(T)` [AL-1]
- S5 ★ effective barrier `ΔG_eff = ΔG_a − χ·F·(V−U)` [AL-2, Marcus-bounded] — 유지
- S6 rate constant Eyring [AL-1]
- S7 relaxation `dξ/dt=k(ξ_eq−ξ)` [AL-5, near-eq linear]
- S8 (옵션) barrier distribution [AL-6]
- S9 integral equation + ratio substitution [AL-7, Fredholm vs Volterra]
- S10 ICA observable `(dQ/dV)_j`
- S11 ★ tail T-dependence = kinetic lag [AL-8 novel]
- S12 ★ falsification of competing tail sources [AL-10]
- S13 fitting model + identifiability + validation protocol [AL-10]

---

## §3. Decision Queue
DQ-v3-1 (isotherm/broadening 형태 — data) · DQ-v3-2 (ratio-substitution Volterra 적용성) ·
DQ-v3-3 (χ_j / Marcus regime) · DQ-v3-4 (tail source 판별) · DQ-v3-5 (ν_j(T) 형태).
