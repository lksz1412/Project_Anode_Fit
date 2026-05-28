# 비교 (2차): Claude v4 synthesis vs Codex rebuilt_v1

**Date**: 2026-05-28
**대상**:
- Claude: `Claude/docs/graphite_ica_chapter1.tex` (v4 synthesis, 623 lines)
- Codex: `Codex/results/graphite_ica_chapter1_rebuilt_v1.tex` (910 lines)
**근거**: 양쪽 본문 전문 정독 + Codex `PHASE_004_CLAUDE_CODEX_CH1_COMPARISON.md`

---

## §0. TL;DR — 수렴(convergence) 달성

1차 비교(`COMPARISON_CLAUDE_vs_CODEX_CH1.md`) 이후 \textbf{양쪽이 서로의 강점을 흡수해
거의 동일한 synthesis 로 수렴}했다. 두 산출물 모두 이제 다음 동일 골격을 갖는다:
charge conservation → implicit $V_n$ → lattice-gas equilibrium(smooth, Gaussian caution)
→ effective barrier $\Delta G_\eff=\Delta G_a-\chi\mathcal A$ (Marcus-bounded) → forward/
backward → relaxation $k=r_++r_-$ (target/mobility 구분) → single-mode exponential kernel
$L=v_Q/k$ → barrier distribution → \textbf{relaxation-length spectrum kernel integral} →
Refs 6/7 (self-consistent integral) → ICA mapping → $T/\psi$ trend → falsification +
non-unique 경고 → Ch2-5 deliverables.

★ \textbf{중요}: Codex 의 PHASE_004 자기 비교는 내 \emph{구버전 v3 (single-length, 746
lines)} 기준이었다. Codex 가 지적한 내 v3 약점 4건(single-mode 과다·barrier distribution
비중심·Refs 6/7 배치·Gaussian 대체)을 \textbf{내 v4 가 이미 독립적으로 수정}했다. 즉
Codex 의 rebuild 와 내 v4 는 \emph{같은 목표 synthesis 로 평행 수렴}했고, 결과물은 ~95%
동일하다.

---

## §1. 수렴 확인 (공통 = 사실상 동일)

| 요소 | Claude v4 | Codex rebuilt | 동일? |
|---|---|---|---|
| charge conservation → implicit $V_n$ | eq:charge_balance | eq:charge_balance | ✅ 동일 |
| lattice-gas eq.\ + logistic ideal + Gaussian caution | §equilibrium | §sec:equilibrium | ✅ 동일 |
| sign-consistent isotherm ($s_\phi$/$s_j$) | ✅ | ✅ | ✅ |
| effective barrier $\Delta G_a-\chi\mathcal A$, Marcus-bounded | eq:Geff | eq:geff | ✅ 동일 |
| forward/backward → $k=r_++r_-$, target/mobility | D5 | eq:rate_from_ratio | ✅ 동일 |
| single-mode kernel $L=v_Q/k$ | eq:single_kernel | eq:local_exponential | ✅ 동일 |
| barrier→length 지수 매핑 + Jacobian $RT/L$ | eq:L_of_G, D7 | eq:l_g, eq:jacobian | ✅ 동일 |
| relaxation-length spectrum $A_L$ | eq:spectrum | eq:a_l | ✅ 동일 |
| ★ kernel integral (중심식) | eq:kernel_integral | eq:tail_integral | ✅ 동일 |
| $T/\psi$ trend ($\partial\ln L/\partial\psi=-\chi F/RT$) | eq:psi_shift | eq:dlnl_dpsi | ✅ 동일 |
| Refs 6/7 = self-consistent integral 도구 | §closure | §self_consistent | ✅ (배치 차이 §2) |
| ICA mapping $dQ/dV_n=C_\bg/(1-\dots)$ | eq:ica | eq:ica_internal | ✅ 동일 |
| falsification + non-unique 경고 | §falsify | §falsification | ✅ 동일 |
| Ch2-5 deliverables | §summary | §deliverables | ✅ 동일 |

물리 이론은 충돌이 아니라 \textbf{동일}하다. 아래는 남은 미세 차이뿐.

---

## §2. 남은 차등 (미세, 상보적)

### Claude v4 가 가진 edge
1. \textbf{Grounding tier (Assumption Ledger)}: AL-\# in-text 인용 + 별도 ledger
   (GROUNDED/BOUNDED/FLAGGED) + grounding-audit self-check 표. Codex 는 구조적 rule
   block(C/O/M/D) + caution box 는 있으나 \emph{형식 grounding-tier ledger 부재}
   (Codex 자신이 PHASE_004 §6.2 에서 인정).
2. \textbf{Refs 6/7 closed-form 을 실제로 씀}: eq:closed (ratio-substitution 결과)을
   명시 (verification-tier flag + Fredholm/Volterra caveat). 사용자가 "PhD 방법을
   쓰라" 한 의도에 더 직접 부합 (방법을 \emph{적용}).
3. \textbf{enumerated null-result 규칙 N1-N4}: 정량 기각 규칙 명시.
4. \textbf{3-potential 구분 $V_n/V_{n,\app}/V_{n,\dimedrive}$}: barrier 인수의 driving
   potential 을 별도 명시.
5. 간결 (623 lines): 핵심 chain 밀도 높음.

### Codex rebuilt 가 가진 edge
1. \textbf{더 완성된 manuscript framing}: convention/term-policy block, 더 풍부한
   pedagogical prose, deliverables D1-D4. (910 lines)
2. \textbf{더 완전한 $V_{\app}$ bridge}: $V_{\app}=V_p-V_n-IR_\Omega-\eta_{tr}-\eta_{ct}$
   (full-cell 분해). 내 v4 는 anode-scoped $V_{n,\app}=V_n+s_I|I|R_n$ (간략).
3. \textbf{Refs 6/7 의 보수적 배치}: closed-form 을 \emph{쓰지 않고} "method boundary /
   guardrail (M1-M3)" 로만 둠 — Volterra 적용성 미검증 상태에서 식을 안 쓰는 것이
   overclaiming 위험을 더 줄인다.
4. ρ_G→ρ_k→A_L 의 중간 rate-distribution 단계를 더 또렷이 언어화.

### ★ 단 하나의 진짜 fork
\textbf{Refs 6/7 closed-form: 쓸 것인가(Claude) vs flagged method-boundary 로 둘 것인가
(Codex)?}
- Claude v4: eq:closed 를 \emph{씀} + "verification-tier, direct 적분 대비 오차 검증
  필요, Fredholm vs Volterra" 명시. → 사용자 PhD 방법을 적용하되 정직하게 hedge.
- Codex: \emph{안 씀}. self-consistent integral 을 만나면 unknown 을 조용히 cancel
  하지 말고 ratio approximation 을 명시·검증하라는 \emph{guardrail} 로만. → 미검증
  Volterra closure 를 본문에 안 박아 overclaiming 위험 최소.
- 둘 다 정당. 사용자 의도("PhD 방법 사용")는 Claude 쪽, overclaiming 회피는 Codex 쪽.

---

## §3. Codex PHASE_004 가 지적한 "Claude 약점" → v4 에서 이미 해소

Codex 비교는 내 v3(746 lines) 기준이라 다음을 약점으로 들었으나, \textbf{v4 에서 해결됨}:
| Codex 지적 (v3 대상) | v4 상태 |
|---|---|
| §4.1 tail core 가 single-mode 과다 | ✅ spectrum kernel integral 을 중심식으로 격상 (eq:kernel_integral) |
| §4.2 barrier distribution 비중심 | ✅ S8/S9 로 load-bearing 화 |
| §4.3 Refs 6/7 배치 (두 integral layer 혼동) | ✅ local self-consistent vs spectrum kernel 구분 + eq:K_def |
| §4.4 Gaussian 대체 positive statement | ✅ lattice-gas baseline + heterogeneity→spectrum 으로 대체 |
→ 내 v4 와 Codex rebuild 는 사실상 \emph{동일한 처방}을 평행 구현.

---

## §4. 권고

두 산출물은 이제 \textbf{경쟁이 아니라 동일 이론의 두 표현}이다. 단일 canonical Chapter 1
로 병합 가능하며, 충돌 없이 best-of-each:
1. 물리 core (spectrum kernel + effective barrier + charge balance + falsification +
   non-unique) = \textbf{공통, 그대로}.
2. Claude 에서 가져올 것: grounding-tier Assumption Ledger, N1-N4 null rules, Refs 6/7
   closed-form (verification-tier).
3. Codex 에서 가져올 것: 더 완성된 manuscript framing(convention/deliverables), full-cell
   $V_{\app}$ bridge, Refs 6/7 의 보수적 guardrail 문장(closed-form 과 \emph{병기}).
4. fork(Refs 6/7 written vs flagged)는 \textbf{병행 수용}: closed-form 을 쓰되 Codex 의
   guardrail 문장을 붙여 "이 ratio closure 는 명시적 approximation 이고 Volterra
   적용성·오차는 검증 대상" 으로 둔다 (두 입장 모두 만족).

## §5. 한 줄 결론
- 1차 비교 시점: Codex(spectrum) vs Claude(single-length+rigor) — 상보.
- 2차(현재): \textbf{양쪽 모두 synthesis 로 수렴, 물리 동일.} 남은 차이는 framing 분량 +
  $V_{\app}$ bridge 깊이 + Refs 6/7 written/flagged 의 1개 fork 뿐.
- 다음 합리적 행보: 한 canonical 본으로 병합 (grounding-tier + spectrum core + full-cell
  bridge + Refs 6/7 written-with-guardrail), 그 후 저속 OCV tail 실측으로 spectrum
  가설 falsify.
