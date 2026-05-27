# Phase 11_v2 Result — ★ §11 피팅 가능 논리식 (사용자 deliverable 종료점)

**Date**: 2026-05-28
**Cumulative steps**: 821 ~ 900
**Phase ID**: `PASS_FITTING_EXPRESSION_v2` (★ Chapter 1 종료점)
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 1490-1577)

## §1. Summary — ★ 사용자 의도 deliverable

본 phase 는 사용자 verbatim (Charter §00.1) ``피크 의 거동 을 해석 하는 피팅
하는데 쓸 수 있는 논리 식 을 구하 는게 이 작업의 핵심이야'' 의 \textbf{정식
deliverable} 출력. Phase 1-10 의 spine A1-A12 + closed-form 종합 →
\textbf{boxed 피팅 가능 closed-form} (`eq:fitting_logical_form`).

## §2. ★ 피팅 가능 closed-form 식 (식 fitting_logical_form)

$$
(dQ/dV)_j(V_{n,\app}, T, |I|) = \frac{Q_{j,\tot}(d\xi_j/dq)}{dV_{n,\app}/dq}
$$
with
- $\xi_j(t)$ = closed-form (Eq. A11, biased numerator + denominator integral)
- $\xi_{\eq,j}(V_n, T) = (1/2)[1 + \operatorname{erf}((V_n-U_j(T))/(σ_j(T)√2))]$
- $\xi_j^{\simplecase}(t) = \xi_{\eq,j}(1 - \exp(-k_j t))$
- $k_j(T, V_{n,\app}) = ν_j(T) \exp[-(\Delta H_{a,j} - T\Delta S_{a,j} - χ_j s_{φ,j}
  F(V_{n,\app} - U_j(T)))/(RT)]$
- $\xi_{j,0} = \xi_{\eq,j}(V_n(0), T)$ (relaxed start)

## §3. 피팅 파라미터 8 종 (longtable)

| 파라미터 | 단위 | 결정 방법 |
|---|---|---|
| $\Delta H_{a,j}$ | J/mol | 다중 T Arrhenius plot |
| $\Delta S_{a,j}$ | J/(mol K) | 같은 Arrhenius plot |
| $\chi_j$ | 무차원 | 다중 $|I|$ 의 $V_{n,\app}$ shift (BEP 계수) |
| $\nu_j(T)$ | 1/s | Arrhenius prefactor (DQ-v2-4 functional form) |
| $U_j(T)$ | V (Li/Li+) | 저속 OCV peak 위치 |
| $\sigma_j(T)$ | V | 저속 OCV peak FWHM (DQ-v2-3 functional form) |
| $Q_{j,\tot}$ | C | 저속 OCV peak 적분 |
| $s_{\phi,j}$ | ±1 | 방향 부호 (보통 +1) |

## §4. 본 식의 사용법 (피팅 단계 — 본 Chapter 범위 외, P1 정합)

1. 다중 $T$ 저속 OCV 에서 평형 파라미터 추정
2. 다중 $T$ + 다중 $|I|$ 정전류 $dQ/dV$ 데이터에서 동역학 파라미터 fitting (솔버
   구현 X, 본 Chapter 범위 외 = 사용자 P1 정합)
3. 결과의 학부 수준 직관 정합 검증 (활성화 에너지 10~100 kJ/mol, χ ≈ 0.5)

## §5. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_11_v2_1` | 피팅 파라미터 8 종 정리 (longtable) | PASS |
| `GATE_11_v2_2` | ★ closed-form 피팅 식 boxed (eq:fitting_logical_form) | PASS |
| `GATE_11_v2_3` | 5 sub-equations 모두 (ξ_j, ξ_eq, ξ^simple, k_j, ξ_0) | PASS |
| `GATE_11_v2_4` | 사용자 verbatim ``피팅 하는데 쓸 수 있는 논리 식'' 직접 명시 | PASS |
| `GATE_11_v2_5` | 사용법 단계 (P1 정합 = 솔버 구현 X) | PASS |
| `GATE_11_v2_6` | 학부 수준 검증 가이드 | PASS |

## §6. Audit

- Dim #11 Pass 1: 정의식 step function 0 (전체 closed-form 형식 안에서)
- erf 1 instance (A5 인용) OK-derived
- Writing Precision PASS
- 사용자 verbatim ``유효 배리어'' (A3) + ``피팅 식'' (eq:fitting_logical_form)
  연결 PASS

## §7. Next

Phase 12_v2 (종합 + 검수 + 인계 + 참고문헌) — cumulative step 901 자동 진입.
