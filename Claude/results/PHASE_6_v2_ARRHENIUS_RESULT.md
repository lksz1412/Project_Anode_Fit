# Phase 6_v2 Result — §6 속도 상수 k_j Arrhenius

**Date**: 2026-05-28
**Cumulative steps**: 401 ~ 480
**Phase ID**: `PASS_ARRHENIUS_v2`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 930-1019)

## §1. Summary

Spine A4 (k_j = ν_j(T) exp(−ΔG_eff,j / RT)) 의 정식 유도. Transition state
theory (TST) 의 학부 수준 출발 → transition $j$ 적용 (D6) → boxed A4 식 →
온도 의존성 (O2 와의 정합) 분석.

핵심 = $k_j$ 가 두 가지 채널로 $T$ 의존:
1. Arrhenius factor 의 분모 $RT$ 가 변함
2. $\Delta G_{a,j}(T) = \Delta H_{a,j} - T \Delta S_{a,j}$ 자체가 $T$ 의존

따라서 ``저 $T$ → 작은 $k_j$ → 큰 lag → 긴 꼬리'' (O2) 의 정량적 메커니즘이
$k_j$ 의 학부 수준 분석으로 직접 도출 (Phase 10_v2 에서 정량).

## §2. 도출 블록

- **D6 (Eq. A4, BOXED)**: $k_j(T, V_{n,\app}) = \nu_j(T) \exp(-\Delta G_{\eff,j}
  /(RT))$.

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_6_v2_1` | TST 학부 수준 출발 | PASS |
| `GATE_6_v2_2` | D6 transition j 학부 수준 적용 | PASS |
| `GATE_6_v2_3` | A4 (Arrhenius) boxed 식 | PASS |
| `GATE_6_v2_4` | k_j 의 T 의존성 두 채널 (O2 정합) 명시 | PASS |
| `GATE_6_v2_5` | ν_j(T) functional form open status (DQ-v2-4) 표시 | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 0 (min(k, k_max) AP2 부재)
- Writing Precision PASS

## §5. Decision Queue

- DQ-v2-4 (ν_j(T) functional form) — Phase 6_v2 에서 ``피팅 단계 결정'' 명시.
  open 유지.

## §6. Next

Phase 7_v2 (§7 진행률 동역학 dξ_j/dt) — cumulative step 481 자동 진입.
