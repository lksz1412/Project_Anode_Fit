# Phase 10_v2 Result — §10 ICA 관측식 + 꼬리 모양의 온도 의존성 (O2 정량)

**Date**: 2026-05-28
**Cumulative steps**: 741 ~ 820
**Phase ID**: `PASS_ICA_TAIL_v2`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 1384-1489)

## §1. Summary — 사용자 관측 O2 의 정량 메커니즘

본 phase 는 사용자 verbatim ``특히 온도가 낮을 때는 꼬리가 길고, 온도가 높으면
그 꼬리가 상대적으로 짧게 끝나는 현상이 관측되었어'' (O2) 의 \emph{정량
메커니즘} 을 spine A12 + closed-form (A11) 로 직접 도출.

- **D12 (Eq. A12, BOXED)**: $(dQ/dV)_j \approx Q_{j,\tot}(d\xi_j/dq)/(dV_{n,\app}
  /dq)$ — 각 transition $j$ 의 ICA 기여 (chain rule + 분리).
- **D13**: 꼬리 영역 정량 — $d\xi_j/dq = (Q_{\cell}/|I|) k_j (\xi_{\eq,j} - \xi_j)$.
  꼬리 = $V_{n,\app}$ 가 peak 중심 $U_j(T)$ 를 지나 진행 했지만 $\xi_j$ 가
  $\xi_{\eq,j}$ 를 완전히 못 따라잡은 영역. 꼬리 길이 $\propto |I|/(Q_{\cell} k_j)$.
- **D14 (★ O2 정량 도출)**: $k_j$ 의 $T$ 의존 (Arrhenius) → 저 $T$ 작은 $k_j$
  큰 lag 긴 꼬리, 고 $T$ 큰 $k_j$ 작은 lag 짧은 꼬리. 사용자 관측 O2 의 \emph
  {정량 메커니즘 확정}.
- 꼬리의 분석적 형태: 비율 치환 closed-form $\xi_j(t)$ (식 A11) 를 $q$ 미분 + 식
  A12 대입 → 꼬리 영역의 명시적 함수 형태 (Phase 11_v2 의 fitting expression
  으로 직접 연결).

## §2. ★ O2 정량 메커니즘

| $T$ | $\Delta G_{\eff,j}$ | $k_j$ | lag $(\xi_{\eq,j} - \xi_j)$ | 꼬리 길이 |
|---|---|---|---|---|
| 낮음 | (큼, $\Delta H - T\Delta S$, $T$ 작음) | 작음 | 큼 | \textbf{길게 늘어짐} |
| 높음 | (작음, $\Delta H - T\Delta S$, $T$ 큼) | 큼 | 작음 | \textbf{짧게 끝남} |

또한 Arrhenius factor 의 $RT$ 분모 효과까지 결합: $T$ 의 $k_j$ 의존이 \emph{double-
channel} (분자 $\Delta G_a(T)$ + 분모 $RT$).

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_10_v2_1` | D12 ICA chain rule 학부 수준 유도 | PASS |
| `GATE_10_v2_2` | A12 (j-번째 ICA 기여) boxed | PASS |
| `GATE_10_v2_3` | D13 꼬리 영역 분석 | PASS |
| `GATE_10_v2_4` | D14 (★ O2 정량 도출) | PASS |
| `GATE_10_v2_5` | 사용자 관측 O2 와 정량 일치 명시 | PASS |
| `GATE_10_v2_6` | T 의존 double-channel 명시 | PASS |
| `GATE_10_v2_7` | Phase 11_v2 진입 bridge | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 0
- Writing Precision PASS

## §5. Next

★ Phase 11_v2 (피팅 가능 논리식) — cumulative step 821 자동 진입.
