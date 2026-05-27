# Phase 4_v2 Result — ★ §4 유효 배리어 ΔG_eff,j 의 정식 유도 (Spine 출발점)

**Date**: 2026-05-28
**Cumulative steps**: 241 ~ 320
**Phase ID**: `PASS_EFFECTIVE_BARRIER_v2` (★ 핵심 phase)
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (lines 555-752 추가)

## §1. Summary — ★ 본 Chapter 의 spine 출발점

본 phase 는 사용자 의도 (Charter §00.1 verbatim ``유효 배리어의 논리를 확정'')
의 정식 유도 부. spine A1+A2+A3 의 도출 블록 D1+D2+D3 작성.

- **D1 (Eq. A1)**: $\Delta G_{a,j}(T) = \Delta H_{a,j} - T \Delta S_{a,j}$ —
  학부 화학 열역학 출발 (Gibbs 자유 에너지의 활성화 부분).
- **D2 (Eq. A2)**: $\mathcal A_j(V_{n,\app}, T) = s_{\phi,j} F (V_{n,\app} -
  U_j(T))$ — Nernst 식의 학부 수준 출발에서 전위 driving force 유도.
- **D3 (★ Eq. A3, BOXED)**: $\Delta G_{\eff,j} = \Delta G_{a,j}(T) - \chi_j
  \mathcal A_j$ — Brønsted–Evans–Polanyi (BEP) 형식 적용. **본 Chapter 의 spine
  출발점 확정.**
- $\chi_j$ (transfer coefficient) 의 의미와 범위 (0..1, 보통 ≈0.5).
- $\Delta G_{\eff,j} < 0$ 영역 처리 (step function 도입 X, spine 정의 영역
  한정 + 꼬리 영역 분석은 ΔG_eff > 0 영역 안에서).

## §2. ★ 유도 블록 D3 (BEP) 자세히

학부 화학 반응 속도론 → BEP generic → graphite transition j 적용 → 단계 1+2+3
→ 차원 점검 → 학부 수준 직관 → Charter 적합성 → spine 출발점 확정.

사용자 verbatim ``극판 자체 전위에 따른 배리어를 낮추는 효과'' 와 직접 일치.

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_4_v2_1` | D1 (Eq. A1) ΔG_a 학부 수준 유도 | PASS |
| `GATE_4_v2_2` | D2 (Eq. A2) A_j 학부 수준 유도 (Nernst→driving force) | PASS |
| `GATE_4_v2_3` | ★ D3 (Eq. A3) ΔG_eff 학부 수준 BEP 유도 (boxed) | PASS |
| `GATE_4_v2_4` | χ_j 의미와 범위 명시 | PASS |
| `GATE_4_v2_5` | ΔG_eff<0 영역 step function 처리 X | PASS |
| `GATE_4_v2_6` | spine 출발점 확정 명시 | PASS |
| `GATE_4_v2_7` | 사용자 verbatim ``배리어 lowering'' 과 직접 일치 명시 | PASS |
| `GATE_4_v2_8` | 차원 점검 inline (모든 D 블록) | PASS |

## §4. Audit

- Dim #11 Pass 1: 정의식 step function 류 0
- Anti-pattern AP1 (max(ΔG_eff, 0)) 대신 ``정의 영역 한정'' 방식 — PASS
- Writing Precision PASS
- DEC-1 (spine discrete-j) + DEC-3 (erf) + 사용자 verbatim 정합

## §5. Decision Queue

- DQ-v2-5 (χ_j 추정) — 본 phase 에서 ``피팅 단계 결정'' 으로 명시. 그대로 open.

## §6. Next

Phase 5_v2 (§5 평형 분포 ξ_eq erf) — cumulative step 321 자동 진입.
