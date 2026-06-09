# Phase 1.1–1.4 — Ch1_Fable 전면 재작업(물리+해설) Result

## Summary
`graphite_ica_ch1_Fable.tex`(원본 ch1 사본) 18절 전부를 절별 루프(전문 정독→물리 손검→해설 타당성→수정→빌드→정합)로 재작업. 물리 결함 정정 7건 + 해설(교과서 접근성) 보강 12건 + 표기·정합 정정 8건. 무수정 절도 정독·검산 근거 기록(복붙-완료 금지 gate 충족).

## Step Range
1–24 (Phase 1.1 setup 1–3 · 1.2 절별 4–14 · 1.3 절별 15–21 · 1.4 게이트 22–24).

## Inputs
`Claude/docs/graphite_ica_ch1_Fable.tex` 전문(1626→1700행), 프로젝트 CLAUDE.md(P1~P5), ★메모리(절별루프·복붙금지·댕글링·단일문건·plan/result 양식).

## Files Created
본 result · `PHASE_FRR_EXECUTION_LEDGER.md`(setup 시) · `graphite_ica_ch1_Fable.tex/pdf`(setup 시 사본).

## Files Updated
`graphite_ica_ch1_Fable.tex`(18절 중 13절 수정·5절 무수정) · ledger 절별 기록.

## Read Coverage
ch1_Fable **전문**(서론 61–110 · 기호 113–172 · 전하보존 175–253 · 평형peak 256–438 · 정규용액 441–556 · 동역학 558–686 · 유효배리어 689–816 · 통계 819–897 · 분포 900–969 · 종합 972–1143 · 겹침 1146–1201 · DVA 1204–1249 · 분기 1252–1335 · 분기dQdV 1338–1362 · 분극 1365–1398 · 부분cycle 1401–1418 · master 1421–1565 · 검증 1568–1642 · bib) — 생략 구간 0.

## Execution Evidence
절 배치별 xelatex 2-pass: 전부 exit 0 · Overfull 0 · undefined 0(최종 35p). 인계 .aux 대조: dUdT 1.15·relax 1.20·eyring 1.21·Lq 1.23·affinity 1.27·bv 1.28·db 1.29·hys_dU 1.48·hys_center 1.49 — **baseline 과 전부 동일**(식 추가 0 → ch3/ch4 재매핑 불요). 규율 grep 3건=자기 장 제목(위반 0).

## Validation (주요 수정 목록)
물리: 도착점 참조순서(서론) · s 규약/관측 이중고정 해소(eqpeak) · "한 연속"→모수축+질적 경계(regsol) · V_eq 정의 인용 정정 · 물리 절 목록 "다섯→여섯"(synth, 정규용액 누락 적발) · ρ_G 독립-모형 표현 정합(dist) · S-순서 헤더 S0→S5(master).
해설(전제→단계 전개): plateau→dQ/dV 치솟음=peak 정의(서론) · Faraday 계상+서로소 분할(전하보존) · C_bg>0=단상 안정성 귀결 · plateau 발산=peak 정의 연결 · "perturbation"→임계까지(eqpeak) · z[ε]=유효 척도(Daumas–Hérold) · spinodal 닫힌꼴 본절 제시 · slowly-varying 조건 (χF/RT)L_V≈0.1 수치화(lag) · tailTC 면적보존 경유 주석 · 공통 q_a 1차근사+상관 방향(dist) · DVA 강건성 잔재 정리 · walkthrough S0 전제.
표기: σ_d 선행 안내·k^fwd 등재·r_a 상한 포화창·ρ_G 용량분율(기호표).
검산 일치 확인(무수정 근거): Stirling·logistic 역산·FWHM 3.53w·dxidV·g''·T_c·binodal 연립·w_eff·relax 항등·Lq·rsol·tail·r⁺/r⁻ 지수·χ 상쇄·LqV 감쇠인자·superpose 보존·closed 재현·S1 모멘트 직교·arrhenius 이항·hys_Veq 부호반전·hys_slope=g''/sF·ξ_s±·ΔU_hys(artanh 차·극한 (8RT/3sF)u³·54mV)·½대칭·obsgap 분해.

## Gate
**PASS** — G1.2/1.3(전 절 행범위+수정/무수정 근거, 빌드 0/0), G1.4(2-pass 0/0·인계 불변·규율 0·result 저장).

## Confirmed Non-Changes
유효배리어·통계도구·겹침·분기·분기dQdV 5절 본문 무수정(검산 전부 일치, 기존 caveat 충분 — 보강 시 중복·패딩). 원본 graphite_ica_ch1.tex/pdf 불가침(사본 작업). 라벨·식번호 변경 0.

## Open Issues / Decision Queue
없음(이번 챕터 범위). 누적 질문은 R.10 후 최종 보고에 일괄.

## Next
Phase 3.1(Ch3_Fable 사전점검 — Ch1 인계 번호 불변이라 대조만) · cumulative step 25.
