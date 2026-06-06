# Phase A.0 — 전제·인벤토리·설계 Result

**Date**: 2026-06-06 · **Plan**: `2026-06-06-ch1-sec6-statmech-accessibility-plan.md` · **Step Range**: 1–4

## Summary
Ch1 완료본의 §5끝~§6(dist)~§7(synth) 재정독으로 §6 통계역학 진입 장벽을 진단하고, §5·§6 사이 신규 "통계의 도구" 절(5 도구) 설계 확정. eq#29=eq:superpose(.aux 검증)·overflow 목록 확정.

## Step Range
Steps 1–4 (A.0). 다음 = 5 (A.1).

## Inputs / Read Coverage
- `graphite_ica_ch1.tex` **L513~706 재정독**(§barrier 끝 L617~623, §dist L625~682 전문, §synth 도입 L684~705). 현재 상태(L641 L_q(G)≃·eq:superpose 1줄·rigorbox·boundbox) 정확 확인.
- `.aux`·`.log` 대조: eq 번호·overflow.

## 확정 사실
- **eq#29 = eq:superpose** (.aux: 26 sseq,27 keff,28 LqV,**29 superpose**,30 closed,31 simplefit,32 arrhenius).
- **Overflow**: L653 eq:superpose **85.9pt**(사용자 식, 최대) · L490–495 **53.6pt**(verifybox 인라인 적분 $r_j=r_j(q_a)\exp[-\!\int\!\dd q'/L_q(q')]$) · L158/162 표 행(7.8/1.5pt) · L763 7.7pt(arrhenius 유도).
- **§5→§6 전이**: §barrier 끝(L622~623) "남은 물리=입자가 동일하지 않다" → §dist(L626) 즉시 ρ_G 분포·eq:superpose 가중적분·분산전파·rigorbox 변수변환으로 \*전제 없이\* 진입(통계역학 도구 점프).

## 신규 절 설계 (§5·§6 사이 삽입, \label{sec:stattools})
제목(안): "통계의 도구: 분포·가중 평균·퍼짐 — 통계역학을 안 배워도". 1~2학년 수학(미적분·기초확률)만. 박스 건너뛰어도 줄기 유지. 5 도구, 각 \*동기→직관(쉬운 예)→식→물리 연결\*:
1. **분포·밀도 ρ(G)**: 입자가 제각각 → 한 값 아닌 \*퍼짐\*. 히스토그램→연속 밀도(G와 G+dG 사이 비율=ρ(G)dG), 정규화 ∫ρdG=1, "용량 가중"(신호 기여 몫만큼 무게).
2. **가중 평균(앙상블)**: 반평균=Σ(점수×비율) → 연속 ∫(값)(밀도)dG. 관측=각 집단 곡선을 비율로 더함=∫ρ_G f dG(=eq:superpose 구조). 기댓값.
3. **퍼짐(분산)·지수 증폭**: 평균±σ. Var(aX)=a²Var X. L_q∝e^{G/RT} → ln L=const+G/RT → σ_{lnL}=σ_G/RT. 저온(RT↓)→퍼짐↑→꼬리↑(분산 전파 직관).
4. **변수 변환(밀도 보존)**: 비율은 좌표(G↔L) 무관 보존 → ρ_G dG=A_L dL → 자코비안 A_L=ρ_G|dG/dL|. (rigorbox 1~2학년화; 심화는 박스.)
5. **연속 지수합→stretched**: 빠른 집단 먼저 끝·느린 집단 길게 끔 → 여러 e^{−x/L} 혼합=단일지수 아닌 늘어진 꼬리. 인용 lindsey/johnston/svare.
→ 이후 §dist(→§7)는 (a)~(d)·eq:superpose·분산·rigorbox 를 이 도구 \*인용\*해 경량 재서술(수식 보존, 직관 보강).

## Validation
- 정독 커버리지 PASS(L513~706). eq#29·overflow .aux/log 확정. 설계 5도구 확정.
- Decision 권고값 확정(신규 절·eq#29 분할·경량/본격·G-undergrad).

## Gate
**PASS_A0_DESIGN**.

## Confirmed Non-Changes
- §1~5 본문(경량 확인만). 핵심 결과식 값.

## Open Issues / Next
- A.1: eq:superpose aligned 2줄 분할 + L490–495·표 overflow + 빌드. (S5–7)
