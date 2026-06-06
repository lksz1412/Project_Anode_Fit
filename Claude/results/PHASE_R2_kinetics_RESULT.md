# Phase R.2 — 동역학 재유도 Result

**Date**: 2026-06-03 · **Plan**: `2026-06-03-ch1-rerevision2-foundation-first-plan.md` · **Step Range**: 15–22

## Summary
§lag eq:relax 산문 라벨을 새 규약(θ_j/ξ_j)에 정합화(C1 전파, Codex Q4 적발분) + caveat C5·C6·C7·C10·C11 반영. §barrier 는 검수 후 클린(편집 불요). Codex 적대검토에서 C6·L_q-상수 과장 2건 추가 적발 → 정직화 → closure 확인.

## Step Range
Steps 15–22 (R.2). 다음 = 23 (R.3).

## Inputs
- `graphite_ica_ch1.tex` §lag(L398~496)·§barrier(L498~592) 편집 전 정독본 + R.0/R.1 result.

## Files Updated
- `graphite_ica_ch1.tex` §lag:
  - eq:relax 도입 산문: 전향(탈리튬화, ∝1−ξ_j=θ_j=잔여 Li)/역향(∝ξ_j=빈자리) 정합 수정. 식 dξ/dt=r⁺(1−ξ)−r⁻ξ 보존.
  - C7: eq:relax 뒤 "단일 완화 모드=ansatz(핵생성·상경계 coarse-grain)" 추가.
  - C6: eq:eyring 뒤 k_0 현상론 prefactor 주(2차 정직화: 절대값은 ∝1/k_0 의존, 결론은 무관).
  - C11: 지연 r_j 정의에 "(첨자 없는 r_j=지연; 속도 r_j± 와 구별)".
  - C10: q_a 조작적 정의(dξ_eq/dq 정점 일정분율 이하 곡률 전환점).
  - C5: eq:tail 단방향 도메인 s(V_n−V_a)≥0 명시(양방향 대칭 아님).
  - verifybox: L_q 상수=국소 근사(정확해 ∫dq'/L_q(q'), slowly-varying, 급변 시 §dist 중첩) 정직화.

## Read Coverage
- §lag 편집 후 재정독 + §barrier L498–592 **전문 정독**(eq:bv/db/sseq/keff/LqV 부호 재검산).

## Execution Evidence
- 빌드: xelatex ×3(C6/Q5 수정 후 재빌드 포함) → `!`0·undefined 0·**17페이지**. 파일 821줄(정직 유도 추가로 증가).

## Validation (4-tier)
- **G-build**: PASS — `!`0·undefined 0.
- **G-local/flow/convention**: PASS — eq:relax 전향∝θ_j 재검산 정합; §barrier eq:sseq ξ_ss=ξ_eq 가 보존된 logistic 과 일치(C1 수정이 detailed balance 불파괴).
- **G-review(Codex)**: PASS — 1차 Q1·Q2·Q3 PASS, Q4(C6)·Q5(L_q 상수) 적발 → 수정 → **2차 ALL CLOSED** confirm.

## Gate
**PASS_R2_KINETICS**.

## Confirmed Non-Changes
- §barrier 전체(eq:bv·db·sseq·keff·LqV·Marcus/rate-limit boundbox): 검수 클린, 편집 불요.
- eq:relax/Lq/rsol/tail 식 구조 보존(산문·도메인·근사 라벨만 정직화).

## Open Issues / Decision Queue
- C3(eq:simplefit r_a)·superpose r_a(G)는 R.3(§synth·§dist) 범위.

## Next
R.3 (Steps 23–31): §dist eq:superpose r_a(G) 추가 → §synth eq:simplefit r_a(C3)·S3/S4 순서(C4)·C8 반쪽전지 → §overlap·§falsify 검수. 절별 5-게이트 + Codex 병행.
