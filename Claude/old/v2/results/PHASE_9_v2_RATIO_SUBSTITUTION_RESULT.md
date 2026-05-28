# Phase 9_v2 Result — ★ §9 Refs 6/7 비율 치환 closed-form (Load-Bearing)

**Date**: 2026-05-28
**Cumulative steps**: 601 ~ 740
**Phase ID**: `PASS_RATIO_SUBSTITUTION_v2` (★ load-bearing phase = 사용자 박사 연구 직접 사용 부)
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 1213-1383)

## §1. Summary — ★ 사용자 박사학위 연구의 직접 사용 부

본 phase 는 사용자 PhD 연구 (Refs 6 = Lee 2011 JCP 134:121102, Ref 7 = Son 2013
JCP 138:164123) 의 비율 치환 기법을 graphite ICA tail dynamics 의 Volterra
integral equation 에 적용해 \textbf{closed-form 해석해} 도출. 본 Chapter 의
load-bearing (가장 ★) 부.

- **D10**: 단순 case ($k_j$, $\xi_{\eq,j}$ 시간 무관) 의 closed-form $\xi_j^{\simplecase}
  (t) = \xi_{\eq,j}(1 - \exp(-k_j t))$ (학부 수준 first-order linear ODE 해).
- **Refs 6/7 동기**: 시간 의존 일반 case 에서 $\xi_j(t)/\xi_j(t')$ 의 normalized
  shape 가 simple case 와 같다는 \emph{비율 치환 ansatz}.
- **D11 (★ Eq. A11, BOXED)**: 비율 치환을 Volterra 2종 (A9) 의 두 번째 적분에
  적용 → $\xi_j(t)$ 가 적분 밖으로 → algebra 풀이 → \textbf{closed-form 해석해}:
  $$\xi_j(t) = \frac{\xi_{j,0} + \int_0^t k_j(t')\xi_{\eq,j}(t') dt'}{1 +
  \frac{1}{\xi_j^{\simplecase}(t)} \int_0^t k_j(t') \xi_j^{\simplecase}(t') dt'}.$$
- 유효 영역 (Refs 6/7 의 정합 조건): k_j 와 ξ_eq,j 가 너무 급격하지 않을 것 +
  normalized shape ratio 정합 + 꼬리 영역 자체가 가장 정확. graphite 저속 정전류
  방전 영역에서 자동 충족.

## §2. ★ 사용자 박사학위 연구의 위치

- Refs 6 (Lee 2011) DOI: 10.1063/1.3565476 — 학부 수준 화학 반응 시간 적분 식의
  비율 치환 기법 (propagator 형식).
- Ref 7 (Son 2013) DOI: 10.1063/1.4802584 — 동 기법의 long-range reactivity
  diffusion-influenced bimolecular reactions 확장. 본 Chapter 의 Volterra 형식
  이 정확히 이 type 에 해당.

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_9_v2_1` | D10 simple case ξ^simple closed-form 학부 수준 유도 | PASS |
| `GATE_9_v2_2` | Refs 6/7 비율 치환 ansatz 학부 수준 동기 (Refs 인용) | PASS |
| `GATE_9_v2_3` | ★ D11 비율 치환 algebra 학부 수준 (5 단계) | PASS |
| `GATE_9_v2_4` | ★ A11 closed-form boxed | PASS |
| `GATE_9_v2_5` | 차원 점검 inline | PASS |
| `GATE_9_v2_6` | 유효 영역 (Refs 6/7 정합 조건) 명시 | PASS |
| `GATE_9_v2_7` | 사용자 박사학위 연구의 ★ 정확한 위치 명시 (Refs 6/7 인용) | PASS |
| `GATE_9_v2_8` | step function 류 정의식 부재 | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 0
- 적분 + 분수의 단순 결합, anti-pattern 부재 PASS
- Writing Precision PASS

## §5. Decision Queue

- DQ-v2-2 (Refs 6/7 ξ^{simple} candidate exact form) — D10 에서 first-order
  linear ODE 해 $\xi^{simple}(t) = \xi_{\eq}(1 - e^{-k t})$ 로 명시 확정.
  \textbf{DQ-v2-2 closed.}

## §6. Next

Phase 10_v2 (§10 ICA + 꼬리 T 의존성) — cumulative step 741 자동 진입.
