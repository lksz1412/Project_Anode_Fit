# Phase 4.1–4.3 — Ch4_Fable(반응속도론) 전면 재작업 Result

## Summary
`graphite_ica_ch4_Fable.tex` 8절 전부 전문 정독. 전 유도 손 재검산 — **확정 결함 0, 본문 무수정**(복붙-완료가 아니라 검산 증거 기반 무수정 판정).

## Step Range
39–49.

## Inputs
ch4_Fable 전문(323행) · ch1_Fable.aux 인계 스냅샷.

## Files Created / Updated
Created: 본 result. 본문 무수정(원본·사본 동일 유지).

## Read Coverage
ch4_Fable **전문**(서론 56–69 · 기호 75–95 · flux-force 98–151 · BV 154–198 · R_ct 201–221 · i0 224–246 · 정상상태 249–283 · 전류분배 286–311 · bib) — 생략 0.

## Execution Evidence
재검산: eq:nch2_Anet(=A−RT logit) · 평형검산(logit=A/RT→A_net=0) · De Donder 부호 · V_eq 국소(logistic 역) · Fη_j=A_net 일치 · BV 선형화(상수 상쇄·합1→α 무관) · R_ct=RT/Fi₀ 차원 Ω·m² · i₀ 유도(e^{χA/RT}=[ξ/(1−ξ)]^χ → ξ^χ(1−ξ)^{1−χ}) · g_j 극대 ξ=α_j(d ln g/dξ=0) · ξ_ss 두 경우(C_j 흡수) · 전류분배(시간미분·차원·부호) — 전부 일치. 인계 인용 (1.1)(1.2)(1.3)(1.11)(1.20)(1.27)(1.28)(1.29) — ch1_Fable .aux 전수 일치. 빌드(baseline) 6p 0/0.

## Validation / Gate
**PASS** — 무수정 사유 = 위 전 항목 검산 일치 + 규율(인계 inline 인용만, recap/transmit 절 0) 충족 + 해설 비약 없음(flux를 따로 보는 이유·net 친화도의 두 항 해석·BV 도입이 전제→단계 전개로 이미 충실).

## Confirmed Non-Changes
전체 본문. 원본 ch4.tex/pdf 불가침.

## Open Issues / Decision Queue
없음.

## Next
Phase R.1(재검토 라운드 1) · step 50.
