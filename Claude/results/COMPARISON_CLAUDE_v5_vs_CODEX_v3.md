# 비교 (4차): Claude v5 merged canonical vs Codex rebuilt_v3 canonical_merge

**Date**: 2026-05-28
**대상**:
- Claude: `Claude/docs/graphite_ica_chapter1.tex` (v5 merged canonical, 737 lines)
- Codex: `Codex/results/graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex` (748 lines)
**근거**: 양쪽 본문 정독 (Codex §closure L398-532, §falsify L590-630 포함)

---

## §0. TL;DR — \textbf{거의 완전 수렴 (~98%)}. 남은 substantive fork 는 단 1개.

Codex v3 는 \textbf{내 v5 구조를 거의 그대로 채택}했다: 동일 section/label/notation, Plan A/
Plan B + R1-R5 + I1/I2 + M1-M5 closure hierarchy, 그리고 \textbf{§falsification 은 내가 추가한
$\chi_j$ vs $\eta_{\mathrm{ct}}$ co-linearity caveat + N1-N4 + competing-source 표까지
사실상 verbatim 흡수}. 양쪽 physics·falsification·grounding 이 동일하다.

\textbf{남은 단 하나의 substantive 차이}: Plan A 의 구체화 수준.
- \textbf{Claude v5}: Plan A = \emph{concrete} closed-form `eq:closed` (ratio-substitution
  결과를 명시 작성, 대수 eq:closed\_pre 포함) — 사용자 PhD 방법을 \emph{실제 적용}한 usable
  fitting 식. M1-M5(정량 $\varepsilon$ 포함) gated.
- \textbf{Codex v3}: Plan A = \emph{abstract} operator placeholder `eq:plan_a_closure`
  $Y_A=\mathcal C_{\mathrm{ratio}}[K,\Phi,Y^{ref}]$ — "detailed form 은 integral equation
  class·variable mapping 확정 후에만 본문식으로 승격". concrete식 \emph{미작성}.

---

## §1. 수렴 확인 (동일)
section 구조·label(sec:verbatim/hypothesis/spine/closure/tailT/falsify…)·notation·spine
S1-S14·charge-balance $V_n$·lattice-gas eq·effective barrier·rate·spectrum·kernel integral·
ICA mapping·$T/\psi$ trend·Plan A/B+R1-R5·\textbf{falsification(χ/η\_ct caveat, N1-N4,
non-unique) — Codex 가 내 판을 흡수해 동일}.

---

## §2. 단일 fork: Plan A concrete (Claude) vs abstract (Codex)

| | Claude v5 | Codex v3 |
|---|---|---|
| Plan A 본문식 | **concrete eq:closed** (PhD 방법 실제 적용; usable) | **abstract operator** $\mathcal C_{\mathrm{ratio}}$; 미작성 (confirm 후 승격) |
| M5 (gate) | **정량 $\varepsilon=\lVert\Theta_A-\Theta_B\rVert/\lVert\Theta_B\rVert\le\varepsilon_{tol}$** | "Plan B local ODE limit 과 같은 limiting behavior" (정성/한계거동) |
| R5 framing | (R1-R4 + governance) | + "dual hierarchy 는 coding route 아닌 \emph{논리적 책임 분리}" (P1 강조 깔끔) |
| §phd 제목 | "= kernel integral 의 closure" | "= candidate analytic closure" (abstract 일관) |

### 평가
- \textbf{Claude edge}: 사용자 "1안(Fredholm) 우선 사용" + "PhD 방법 사용" 의도에 더 충실 —
  abstract operator 는 \emph{사용}할 수 없고, concrete eq:closed 는 (gated 하에) 바로 쓰는
  fitting 식. M5 가 정량($\varepsilon$)이라 더 testable.
- \textbf{Codex edge}: 더 보수적 — Fredholm 재정식화·variable mapping 확정 전엔 특정 form 을
  본문에 안 박아 overclaiming 위험 최소. R5 "coding route 아님" 한 줄은 P1 정합을 더 또렷이.
- \textbf{공통}: 둘 다 Plan B 를 항상-core 로 보존, R1-R5 governance, exact 주장 X.

---

## §3. 권고
두 판은 이제 \textbf{동일 canonical 의 두 표현}이며, 단일 fork 만 결정하면 완전 통합된다.

\textbf{권고: Claude v5 의 concrete Plan A 유지} — 이유: (a) 사용자가 명시한 "option 1 을
실제 사용 + PhD 방법 적용" 에 부합, (b) Chapter 의 deliverable(피팅 식)이 실재해야 함, (c)
이미 M1-M5 + 정량 $\varepsilon$ + "candidate, exact 주장 X" 로 충분히 honest-gated. abstract
로 두면 deliverable 이 비어버림.

\textbf{Codex 에서 흡수할 미세 2건}:
1. R5 의 "dual hierarchy 는 coding route 가 아니라 논리적 책임 분리" 문장 (P1 정합 강조) →
   내 R-governance 에 1줄 추가.
2. M-조건에 "limiting behavior consistency" 를 \emph{명시 항목}으로 (내 M4 single-mode limit
   이 이미 포함하나, Codex 처럼 'Plan B local-ODE limit 일치' 를 별도 문구로 강화).

이 2건만 반영하면 Claude v5 = 두 판의 superset (concrete deliverable + 보수 governance +
P1 강조 + 정량·정성 gate 둘 다).

## §4. 한 줄 결론
- 4차 시점: \textbf{~98% 동일}. Codex 가 내 falsification·구조를 흡수, 나는 Codex Plan-B-core/
  governance 를 흡수 → 수렴 완료 단계.
- 유일 fork = Plan A \emph{concrete(Claude) vs abstract(Codex)}. 사용자 의도상 \textbf{concrete
  유지} 권고 + Codex R5/M-limiting 문구 2건 흡수 → 단일 정본 확정 가능.
- 다음: 이 2건 미세 반영 후 단일 canonical 확정 → 저속 OCV tail 실측(falsification) / Chapter 2.
