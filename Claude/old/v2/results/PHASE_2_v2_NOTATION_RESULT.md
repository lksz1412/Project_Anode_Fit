# Phase 2_v2 Result — §2 기호와 단위 컨벤션

**Date**: 2026-05-28
**Cumulative steps**: 121 ~ 180
**Phase ID**: `PASS_NOTATION_v2`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 346-490 추가)

## §1. Summary

Chapter 1 v2 의 §2 (기호와 단위 컨벤션) 작성. 7 sub-section (기본 좌표·전하·전류·
온도 / 전위 세 가지 / 상변이 / 유효 배리어 / 속도 상수 / 관측 / Charter 적합성
점검 / 단위 컨벤션 요약) 완성. 모든 변수 정의는 §2 안에서 (Writing Precision §5
정합). longtable 환경 사용해 표 형식 정리. 핵심 = $V_n / V_{n,\app} / V_{n,\drive}$
세 가지 전위의 명시적 구분 (v1 의 ver1_rechecked2.tex §4 의 핵심 분리 보존).

## §2. 산출

- §2.1 기본 좌표 (q, T, I, F, R) — longtable
- §2.2 전위 세 가지 (V_n, V_{n,app}, V_{n,drive}) — 명시적 구분 (★ load-bearing)
- §2.3 상변이 기호 (j, N_p, ξ_j, U_j, σ_j, Q_{j,tot}) — longtable
- §2.4 유효 배리어 (ΔG_a, A_j, ΔG_eff, ΔH_a, ΔS_a, χ_j, s_φ) — longtable
- §2.5 속도 상수 (k_j, ν_j) + 동역학 (t, dξ/dt, dξ/dq)
- §2.6 관측 (Q_ext, Q_cell, dQ/dV)
- §2.7 Charter §5 적합성 자기 점검 (모든 정의 §2 내, 비약 X)
- §2.8 단위 컨벤션 (SI + V (Li/Li+) for U_j)

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_2_v2_1` | §2 의 7 sub-section 모두 작성 | PASS |
| `GATE_2_v2_2` | V_n / V_{n,app} / V_{n,drive} 명시 구분 | PASS |
| `GATE_2_v2_3` | 모든 spine A1-A12 변수 정의 §2 내 | PASS |
| `GATE_2_v2_4` | longtable 가독성 정렬 | PASS |
| `GATE_2_v2_5` | Charter §5 자기 점검 sub-section 포함 | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 류 0
- Writing Precision: §5 정합 (모든 정의 §2 내)

## §5. Next

Phase 3_v2 (§3 흑연 staging) — cumulative step 181 자동 진입.
