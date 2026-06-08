# PHASE 1.1–1.9 (Ch1) — 연결고리 + 최종 피팅식 개정 Result

## Summary
Ch1(`graphite_ica_ch1.tex`)을 절 단위 루프로 개정: 전반부→후반부 대동맥 연결(S1–S4), 최종식 도착점 thread, 신규 §최종 종합식 절(sec:master), 확정 결함(C2-1·C2-2·C2-4·C2-5·부록) 시정. 정확성 확인된 유도는 보존, surgical 개정만.

## Step Range
Steps 1–31 (Phase 1.1–1.9).

## Inputs
- `Claude/docs/graphite_ica_ch1.tex`(개정 전 953줄, 전문 정독본).
- 검토 결과 `Claude/results/REVIEW_CH1_CH2_6LENS_section-by-section_2026-06-08.md`(9f06579).
- 계획 `Claude/plans/2026-06-08-ch1-ch2-connective-masterequation-revision-plan.md`.

## Files Created
- `Claude/results/PHASE_CM_ch1_RESULT.md`(본 문건).
- `Claude/docs/graphite_ica_ch1.pdf`(빌드 산출, 21p).

## Files Updated
- `graphite_ica_ch1.tex`:
  - 서론: 최종식 도착점 thread(\S\ref{sec:master} 예고, 각 절=한 항) [1.1]
  - §eqpeak: (a)dξ_eq(1.13)→dQdV(1.4) 대입 loop-closure 문장 (b){U_j,w_j,Q_j}→최종식 평형항 thread (c)8.314×258 표기 [1.2]
  - §lag: 단일지수=근사·실측 stretched·분포(§dist) 예고 = 전반부→후반부 동기(S2 출발); 꼬리=최종식 동역학항 thread [1.3]
  - §barrier: §6 도구막간 예고 다리(S1); k_0 disclaimer 중복 1곳 제거; eq:keff 조건 𝒜≳RT→𝒜≳3RT(본문 5%@3RT 정합) [1.4]
  - §stattools: "도구 정비 막간" reframe + §lag stretched 연결; **C2-1 길이식 e^{(G−χ𝒜)/RT}로 정합 + χ𝒜 집단공통=상수=분산무관 명시** [1.5]
  - §dist: §lag 예고 stretched의 payoff 명시(단일지수=좁은 분포 극한) [1.6]
  - §synth: 단일지수 vs stretched 선택 명시(분포는 버린 우회 아님, S2 마감); 메타문장(297)·"무근거 단정"(790) 제거; "부록" 2곳→S1/피팅 장 [1.7]
  - **신규 §종합 모델식과 피팅·예측(sec:master, eq:master)**: master 식 boxed + 파라미터 표(전이당 {U_j,w_j,Q_j,ΔH_a}+공통{χ,R_n,C_bg}+선택 ρ_G) + 데이터→파라미터 S1–S4 + 예측 keybox [1.8]

## Read Coverage
- ch1.tex 1–953 전문 정독(직전 세션). 본 phase 개정 구간 재확인: 서론·§eqpeak·§lag·§barrier·§stattools·§dist·§synth·신규 절.

## Execution Evidence
- 빌드: `xelatex` 2-pass, pass1 exit=0, pass2 exit=0. `Output written on graphite_ica_ch1.pdf (21 pages)`.
- undefined ref/citation: grep 결과 **0건**(신규 \label{sec:master}·eq:master 포함 전 ref 해소).

## Validation (4-tier)
- **확정 PASS** — G1.1~G1.8 본문 편집 모두 반영(grep/diff add-only), 빌드 0 undefined(G1.9 빌드분).
- **확정 PASS** — eq:master 손검: 평형 상승부=eq:dxidV(s=+1), 꼬리 길이=eq:Lq·eq:keff, 𝒜=eq:affinity, V_n=eq:vapp 일치. I→0서 꼬리→0(L_q→0… 실제 I→0이면 L_q→0이라 꼬리 소멸)·평형 peak 복귀.
- **미검증** — Codex 교차 적대검수(연결 비약·신규식): Ch2까지 마친 뒤 일괄 foreground 1회 예정(G1.9 Codex분 보류).

## Gate
**CONDITIONAL PASS** — 빌드·손검·편집 PASS. Codex 교차검수만 말미 일괄(미검증 1).

## Confirmed Non-Changes
- 정확성 확인된 유도(logistic·eqcond·db·spinodal 없음(Ch1)·dxidV·dUdT) 본체 불변. eq 라벨·식 번호 불변(신규만 add). §falsify·3×3 표·S1–S4 골자 불변.

## Open Issues / Decision Queue
- 없음(파라미터 집합 IF-1대로, 사용자 이의 시 조정).

## Next
- Step 32, Phase 2.1(Ch2 §1 γ_j 정의역·서론 thread). Codex는 Phase 2.8 일괄.
