# Phase 5_v2 Result — §5 평형 분포 ξ_eq,j = (1/2)[1 + erf]

**Date**: 2026-05-28
**Cumulative steps**: 321 ~ 400
**Phase ID**: `PASS_EQUILIBRIUM_ERF_v2`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 753-929)

## §1. Summary

Spine A5 의 정식 유도. 가우시안 분포의 학부 수준 출발 (분포 형식 동기,
중심극한정리) → ξ_{eq,j} 의 정의 (평형 누적 점유, gaussian density 의 누적 적분)
→ 변수 치환 ($u = (V_n − U_j)/(σ_j√2)$) 으로 erf 도출 → boxed A5 식 → ICA peak
형태 ($d\xi_{eq}/dV_n$ = 가우시안 PDF) 학부 수준 도출 (D5).

erf 사용 = OK-derived 분류. 사용자 verbatim ``약간 가우시안 피크 형상이 나타나고''
의 직접 표현 (AP4 에서 v2 재분류).

## §2. 도출 블록

- **D4 (Eq. A5, BOXED)**: $\xi_{\eq,j}(V_n, T) = \tfrac{1}{2}[1 + \operatorname
  {erf}((V_n - U_j(T))/(\sigma_j(T)\sqrt{2}))]$.
- **D5**: $d\xi_{\eq,j}/dV_n = (1/(\sigma_j \sqrt{2\pi})) \exp(-(V_n - U_j)^2/
  (2\sigma_j^2))$ — Gaussian PDF, ICA peak 의 평형 형태.

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_5_v2_1` | 가우시안 학부 수준 출발 (CLT 언급) | PASS |
| `GATE_5_v2_2` | ξ_eq 변수 치환 학부 수준 단계 (D4) | PASS |
| `GATE_5_v2_3` | A5 (erf) boxed 식 명시 | PASS |
| `GATE_5_v2_4` | dξ_eq/dV_n = Gaussian PDF (D5) | PASS |
| `GATE_5_v2_5` | erf = OK-derived 분류 명시 (Charter §3 AP4 재분류) | PASS |
| `GATE_5_v2_6` | 사용자 verbatim ``가우시안 피크 형상'' 정합 | PASS |
| `GATE_5_v2_7` | σ_j(T) functional form 의 open status (DQ-v2-3) 표시 | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 0
- erf 사용 인스턴스: 1 (boxed A5) — OK-derived 명시
- Writing Precision PASS

## §5. Decision Queue

- DQ-v2-3 (σ_j(T) functional form) — Phase 5_v2 안에서 ``피팅 단계 결정'' 으로
  명시. open 유지.

## §6. Next

Phase 6_v2 (§6 속도상수 Arrhenius) — cumulative step 401 자동 진입.
