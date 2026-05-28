# Phase 8_v2 Result — §8 시간 적분형 ξ_j(t) Volterra Integral Equation

**Date**: 2026-05-28
**Cumulative steps**: 541 ~ 600
**Phase ID**: `PASS_VOLTERRA_v2`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 1122-1212)

## §1. Summary

Spine A9 의 정식 유도. Phase 7_v2 의 ODE (A6) 시간 적분 (D9, 양변 0→t 적분 +
부분 적분) → Volterra integral equation of the 2nd kind 형식 식별 → Fredholm vs
Volterra 학부 수준 정의 → 식 \eqref{eq:volterra_form} 가 Volterra 형식임을 학부
수준 정합 → self-consistent 의 의미 명시 → 닫힌 형식 해석해 가 일반 케이스
에서는 존재 X 의 학부 수준 설명 → Phase 9_v2 의 Refs 6/7 비율 치환 기법 필요성
명시.

## §2. 도출 블록

- **D9 (Eq. A9, BOXED)**: $\xi_j(t) = \xi_{j,0} + \int_0^t k_j(t')[\xi_{\eq,j}(t')
  - \xi_j(t')] dt'$.
- Fredholm (kernel 상수 적분 한계) vs Volterra (상한 = t) 학부 수준 구분.
- 본 식이 Volterra 2종 (linear in unknown $\xi_j$) 임을 명시.
- self-consistent 의 의미 (양변의 $\xi_j$ 가 같은 함수): 일반 closed-form 부재의
  근거.

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_8_v2_1` | ODE → 시간 적분 D9 학부 수준 유도 | PASS |
| `GATE_8_v2_2` | A9 boxed | PASS |
| `GATE_8_v2_3` | Volterra vs Fredholm 정의 학부 수준 | PASS |
| `GATE_8_v2_4` | 본 식이 Volterra 2종 분류 명시 | PASS |
| `GATE_8_v2_5` | self-consistent 의미 명시 | PASS |
| `GATE_8_v2_6` | Phase 9_v2 (★ Refs 6/7) 진입 bridge | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 0
- Volterra 형식 = OK (수학적 정의 식별, anti-pattern 무관)
- Writing Precision PASS

## §5. Next

★ Phase 9_v2 (Refs 6/7 비율 치환 closed-form) — cumulative step 601 자동 진입.
