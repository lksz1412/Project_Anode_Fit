# Phase 7_v2 Result — §7 진행률 동역학 dξ_j/dt Relaxation ODE

**Date**: 2026-05-28
**Cumulative steps**: 481 ~ 540
**Phase ID**: `PASS_KINETICS_v2`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 1020-1121)

## §1. Summary

Spine A6 (dξ_j/dt = k_j (ξ_eq,j − ξ_j)) + A7 (q 좌표 변환, 정전류 한정) 정식
유도.

- **D7**: Relaxation 동역학의 학부 수준 출발 (linear restoring force 형식,
  Onsager-style linearization, fluctuation-dissipation 의 학부 수준 일관성).
  $d\xi_j/dt = k_j(\xi_{\eq,j} - \xi_j)$ boxed.
- **D8**: 정전류 한정 $q$ 좌표 변환. $t = Q_{\cell} q / |I|$ 이므로 $d\xi_j/dq
  = (Q_{\cell}/|I|) k_j (\xi_{\eq,j} - \xi_j)$. boxed.
- 초기 조건 (relaxed start: $\xi_{j,0} = \xi_{\eq,j}(V_n(0), T)$) + $k_j$ 와
  $\xi_{\eq,j}$ 의 시간 의존성 명시 → Phase 8_v2 의 시간 적분형 (Volterra) 의
  필연성.

## §2. 도출 블록

- **D7 (Eq. A6, BOXED)**: $d\xi_j/dt = k_j(T(t), V_{n,\app}(t))[\xi_{\eq,j}(t)
  - \xi_j(t)]$.
- **D8 (Eq. A7, BOXED)**: $d\xi_j/dq = (Q_{\cell}/|I|) k_j[\xi_{\eq,j} - \xi_j]$.

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_7_v2_1` | Relaxation ODE 학부 수준 출발 (D7) | PASS |
| `GATE_7_v2_2` | A6 boxed | PASS |
| `GATE_7_v2_3` | q 좌표 변환 D8 (정전류 한정) | PASS |
| `GATE_7_v2_4` | A7 boxed | PASS |
| `GATE_7_v2_5` | 초기 조건 + k_j(t) + ξ_eq(t) 시간 의존성 명시 | PASS |
| `GATE_7_v2_6` | Volterra 형식 필요성 명시 (§8 진입 bridge) | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 0
- Linear relaxation form (no clipping) PASS
- Writing Precision PASS

## §5. Next

Phase 8_v2 (§8 시간 적분형 Volterra) — cumulative step 541 자동 진입.
