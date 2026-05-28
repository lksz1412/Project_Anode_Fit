# 비교 (3차): Claude canonical (dual-track) vs Codex rebuilt_v2 (dual closure)

**Date**: 2026-05-28
**대상**:
- Claude: `Claude/docs/graphite_ica_chapter1.tex` (canonical dual-track, ~705 lines)
- Codex: `Codex/results/graphite_ica_chapter1_rebuilt_v2_dual_closure.tex` (1013 lines)
**근거**: 양쪽 본문 전문 정독 (Codex §Dual Closure Hierarchy L673-826, §Falsification L873-921 포함)

---

## §0. TL;DR

물리 core 는 \textbf{계속 수렴}(거의 동일). 둘 다 closure 를 \textbf{이원화}했고, 차이는
\emph{이원화의 철학}에 있다:
- \textbf{Claude}: 1안 = \emph{구체적 closed-form (eq:closed) 작성} (사용자 PhD 방법 실제
  적용), measured $\varepsilon$ switch 로 gating; 2안 = direct \emph{numerical} reference;
  floor = single-mode. \textbf{χ\_j vs η\_ct co-linearity falsification 명시.}
- \textbf{Codex}: Plan A = \emph{abstract candidate} (operator placeholder $\mathcal C_{\mathrm{ratio}}$,
  Fredholm 재정식화 M1-M5 통과 전엔 form 미작성); Plan B = \emph{conservative reduced
  \textbf{analytic} theory} (ODE+spectrum, \emph{항상 보존되는 논리 core}); R1-R5 governance.

→ Claude 는 \textbf{사용자의 "1안 primary, 안되면 2안" 문구에 더 충실 + PhD 방법을 실제
적용}. Codex 는 \textbf{더 보수적(미검증 form 미작성) + Plan B 를 항상-core 로 + R1-R5 의
명시적 governance}. 상보적이며 병합이 명확하다.

---

## §1. 수렴 확인 (physics core 동일)
charge-balance implicit $V_n$ · lattice-gas eq(smooth, Gaussian caution) · effective barrier
$\Delta G_\eff=\Delta G_a-\chi\mathcal A$($=G-W_\psi$) · forward/backward→relaxation($k=r_++r_-$) ·
single-mode kernel $L=v_Q/k$ · barrier→length 지수 매핑+Jacobian · relaxation-length spectrum ·
kernel integral · ICA mapping · $T/\psi$ trend · non-unique 경고 — \textbf{전부 동일}. 충돌 없음.

---

## §2. ★ Dual closure 의 차등 (핵심)

| 항목 | Claude (dual-track) | Codex (Dual Closure Hierarchy) |
|---|---|---|
| 1안 / Plan A | **구체 closed-form eq:closed 작성** (eq:closed\_pre 대수 포함) | **abstract candidate** $Y_A=\mathcal C_{\mathrm{ratio}}[K,\Phi,Y^{ref}]$; 구체 form 은 Fredholm 재정식화(M1-M5) 확정 후에만 |
| 2안 / Plan B | direct **numerical** integration (computational reference/validator) | conservative **reduced analytic theory** (local ODE + $L(G)$ + spectrum kernel, 3 식) — \emph{항상 보존 core} |
| 전환/결정 | 정량 $\varepsilon\le\varepsilon_{tol}$ (measured) | 구조적 R1-R5 (Plan B 항상 core; 본문 A + appendix B + limiting-case check; A≠B 면 B 만 core) |
| Refs 6/7 실제 적용? | **YES** (concrete closed-form, 사용자 PhD 방법 적용) | NO (abstract candidate 로만, gated) |
| Volterra→Fredholm 근사 | 단계 0 명시 (frozen source + decay≪window) + ε 측정 | M1-M5 조건 + limiting-case + numerical 비교 (더 다항 조건) |
| P1(no solver) 정합 | 2안 numerical → borderline | Plan B = pure theory → **더 정합** |
| χ\_j vs η\_ct co-linearity | **명시 caveat** (단일 electrode 퇴화 → GITT 로 분리, η\_ct 분리 후만 χ\_j 귀속) | **미명시** ("polarization correction 후에도 남는지" 만 — 퇴화 자체는 안 짚음) |

---

## §3. 각자 edge

### Claude canonical edge
1. \textbf{사용자 "1안 primary" 문구에 더 충실}: 사용자는 "1안 Fredholm 우선, 못 쓰면 2안
   회귀" 라 했다. Claude 는 1안을 primary 로 두고 measured switch 로 강등. Codex 는 Plan B 를
   항상-core 로 두어(A 는 후보) primary 가 보수쪽으로 기움 — 사용자 문구와 미세하게 다름.
2. \textbf{사용자 PhD 방법을 실제 적용}: eq:closed 를 구체적으로 작성(대수 포함). Codex 는
   여전히 abstract operator placeholder 라 PhD 방법이 \emph{기술}될 뿐 \emph{적용}되지 않음.
3. \textbf{χ\_j vs η\_ct co-linearity falsification}: 최대 referee 공격면을 명시 방어 (Codex
   누락). grounding-tier Assumption Ledger, N1-N4 null rules 도 유지.

### Codex v2 edge
1. \textbf{Plan B = reduced \emph{analytic} theory 를 항상-core 로}: 미검증 closed-form 에
   의존하지 않는 안정 논리 core 가 항상 남음 — 더 보수적·정직. P1(theory only)과도 더 정합
   (Claude 2안은 numerical).
2. \textbf{R1-R5 governance}: "본문 A + appendix B + limiting-case check; A≠B 면 B 만 core"
   라는 명시적 의사결정 규약 — Claude 의 단일 ε-switch 보다 publication governance 가 또렷.
3. \textbf{미검증 form 미작성}: Plan A 를 abstract 로 유지해 overclaiming 위험을 원천 차단
   (단, 사용자 PhD 방법을 적용은 안 함 — trade-off).
4. 더 완성된 manuscript 분량 (1013 lines, convention/deliverables 풍부).

---

## §4. 권고 (병합 = best of both)

두 dual 접근은 충돌이 아니라 \textbf{서로의 빈칸을 채운다}. canonical 최종:
1. \textbf{Codex Plan B (reduced analytic theory) 를 ``항상 보존 core''} 로 채택 (P1 정합 +
   안정 논리 base). → Claude 2안의 "numerical reference" 는 그 \emph{검증 수단}으로 격하.
2. \textbf{Claude eq:closed (구체 closed-form) 를 instantiated Plan A} 로 유지 (사용자 PhD
   방법 실제 적용). 단 Codex M1-M5 + Claude 정량 ε 를 \emph{둘 다} gating 조건으로.
3. \textbf{Codex R1-R5 governance 채택} (본문 A + appendix B + limiting-case check).
4. \textbf{Claude χ\_j vs η\_ct co-linearity falsification 유지} (Codex 누락분 보완).
5. grounding-tier Assumption Ledger(Claude) + 완성 manuscript framing(Codex) 병합.

→ 결과: "보수적 reduced theory 가 core(Codex) + 그 위에 검증-gated 된 구체 PhD closed-form
(Claude) + 명시 governance(Codex) + co-linearity falsification(Claude)". 사용자의 "1안
primary, 2안 fallback" 의도와 overclaiming 회피를 동시에, 최고 수준으로 만족.

## §5. 한 줄 결론
- 3차 시점: 물리 동일, dual-closure \emph{철학}만 갈림.
- Claude = \textbf{사용자 문구 충실 + PhD 적용 + co-linearity 방어}; Codex = \textbf{보수 core +
  명시 governance + P1 정합}.
- 단일 canonical 병합 추천: Codex 의 reduced-theory-core + R1-R5 위에 Claude 의 concrete
  closed-form + ε + co-linearity 를 얹는다.
