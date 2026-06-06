# Phase R.1 — 무대·열역학 재유도 Result

**Date**: 2026-06-03 · **Plan**: `2026-06-03-ch1-rerevision2-foundation-first-plan.md` · **Step Range**: 6–14

## Summary
§notation·§stage·§eqpeak 의 lattice-gas 유도를 점유율 θ_j 기반으로 정직화(C1) + ΔS_j 방향 라벨(C2). 최종 logistic·peak 식은 글자 단위 보존, 유도 사슬의 hidden flip 만 제거.

## Step Range
Steps 6–14 (R.1). 다음 = 15 (R.2).

## Inputs
- `graphite_ica_ch1.tex` L124–390(notation·stage·eqpeak) 편집 전 정독본 + R.0 result 의 잠근 유도.

## Files Updated
- `graphite_ica_ch1.tex`:
  - L129 전이 인덱스 규약: θ_j 도입, ξ_j=1−θ_j 명시.
  - 기호표: θ_j 행 추가, ξ_j 행에 =1−θ_j, ΔS_j 행 "삽입(리튬화) 반응" 라벨+∂U_j/∂T 식.
  - L183 §stage 전하균형: ξ_j=1−θ_j(점유율 θ_j 감소) 병기.
  - L245–248 "왜 이 양인가": 점유율 θ_j 기준·진행률 옮김 명시.
  - eq:smix·eq:mumix·eq:muint·eq:mu(L258–286): θ_j 로. eq:mu→μ_Li(θ_j).
  - (iii) eqcond(L288–305): 점유율 균형 정직 유도. eq:eqcond=μ_Li(θ_eq)=μ⁰−sF(V_n−U_j), U_j=U_j⁰−μ⁰/(sF). "부호의 정직성" 문단.
  - (iv) solve(L307–323): θ_eq=1−ξ_eq 치환 부호 반전 명시 → logistic(보존).
  - flagbox(L329): Ω 항 θ 기준(ξ 환산 병기).
  - eq:dUdT 텍스트(L375–388): 삽입 반응 ΔG_j·ΔS_j 방향 라벨, 탈리튬화 환산 동치 명시.

## Read Coverage
- 편집 후 L243–337 **재정독**(자체 검수). 기호표 L124–172, dUdT L370–390 확인.

## Execution Evidence
- 빌드: xelatex ×3 패스 → `!` 오류 **0**, undefined ref/citation **0**, **17페이지**(분량 회귀 없음). `graphite_ica_ch1.pdf` 352932 B.
- (Font shape UnBatang italic 경고·hyperref PDF-string 경고 = pre-existing 무해.)

## Validation (R.1 gate, 4-tier)
- **G-build**: PASS(확정) — `!`0·undefined 0·17p.
- **G-local**: PASS(확정) — eq:mu→eqcond→solve 차원·부호·무비약 자체 재검산.
- **G-flow**: PASS(확정) — logistic 박스 이전과 동일, downstream(dxidV·eqpeak·온도) 불변. §stage 정합.
- **G-convention**: PASS(확정) — θ_j/ξ_j 일관(R.1 범위 내).
- **G-review(Codex --resume)**: PASS — Q1(eqcond/U_j 정합)·Q2(부호반전→logistic)·Q3(ΔS 라벨) 전부 PASS. "L245–323 열역학 블록 정합" confirm.

## Gate
**PASS_R1_THERMO**.

## Confirmed Non-Changes
- eq:logistic·eq:dxidV·eq:eqpeak·온도식·U_j 정의: 최종 결과 보존(불변).
- 사용자 기호 s·s_I·U_j·w_j·Q_j·라벨·식번호 P5 보존.

## Open Issues / Decision Queue
- **eq:relax 산문 라벨(L405–408)**: "1−ξ_j=빈자리, ξ_j=점유 분율" 이 새 규약과 역전(C1 전파). Codex Q4 적발. **§lag(R.2) 범위** — R.2 첫 작업으로 교정(식 구조 dξ/dt=r⁺(1−ξ)−r⁻ξ 는 보존, 산문만). R.0서 이미 식별·배정한 항목(R.1 신규 오류 아님).

## Next
R.2 (Steps 15–22): §lag eq:relax 라벨 교정(C11 포함) → eq:relax ansatz(C7) → eyring k_0 현상론(C6) → eq:tail 도메인(C5) → q_a 정의(C10). 절별 5-게이트 + Codex 병행.
