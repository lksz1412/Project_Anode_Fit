# Phase A.3–A.5 — 신규 통계 도구 절 + §dist 연결 + 전영역 검증 Result

**Date**: 2026-06-06 · **Plan**: `2026-06-06-ch1-sec6-statmech-accessibility-plan.md` · **Step Range**: 12–30

## Summary
§5(barrier)·§6(dist) 사이에 신규 §6 `통계의 도구`(sec:stattools, 5 도구) 삽입 — 통계역학 미수강 학부 1~2학년이 §7(dist)의 분포·중첩·분산전파·변수변환을 따라가게 바닥부터 깔았다. §7 dist 가 그 도구를 \eqref 로 인용·의존. Codex 교차모델 + Claude 전원 DOCUMENT CLEAN.

## Step Range
Steps 12–30 (A.3 12–18 신규 절 / A.4 19–25 dist 연결 / A.5 26–30 검증). 챕터 A 완료.

## Files Updated (`graphite_ica_ch1.tex`)
- **신규 §6 sec:stattools**(§5·§6 사이): 도구1 분포/밀도 ρ_G(eq:density·eq:norm ∫ρdG=1, 용량가중) · 도구2 가중평균/앙상블 ⟨f⟩=∫fρ_G dG(eq:wavg) · 도구3 분산·지수증폭 Var(aG)=a²σ², L_q∝e^{G/RT}(같은 T·I·구동력서 G만 차이)→σ_{lnL_q}=σ_G/RT(eq:varprop) · 도구4 변수변환 A_L=ρ_G|dG/dL|(eq:jacobian) · 도구5 연속지수합→stretched · keybox. 각 "동기→직관(히스토그램·반평균·두 반·키 로그)→식→물리 연결".
- **§7 dist 연결**: (b)분포→도구1(eq:norm) · (d)중첩→도구2(eq:wavg) · 분산전파 문단→도구3(eq:varprop, L_V∝L_q) · rigorbox→도구4(eq:jacobian).
- **마감 clarity**: 서 로드맵 (5)에 "통계 도구는 §6서 먼저" 명시 · §synth "위 다섯 \emph{물리} 절(통계 도구절 제외)"로 모호 제거.
- (A.1 줄나눔 별도 result.)

## Read Coverage
- A.0서 §barrier 끝~§dist~§synth 도입 재정독. 신규 절 작성 후 자체 재정독(도구1~5 수학·직관). §dist 편집부 재정독.

## Execution Evidence
- 빌드: xelatex → `!`0·undefined 0·**21p·971줄**·11 sections·17 bibitems·\end. Overfull: L163 표 셀 1.51pt(비가시)만 — 디스플레이 식 0.
- 번호(.aux): 신규 §6 sec:stattools, dist→§7. 신규식 eq:density29·norm30·wavg31·varprop32·jacobian33, eq:superpose=34.

## Validation (4-tier) — Claude + Codex 교차모델
- **확정(완료)**: 
  - **Claude 자체**(신규 절): 도구1~5 수학 재검산 정확(정규화·⟨f⟩=∫fρ·Var(aG)=a²σ²·σ_{lnL}=σ_G/RT·자코비안·stretched). G-undergrad 직관 1~2학년 접근 가능.
  - **Codex 신규 절 적대**: CLEAN(4렌즈 — math·G-undergrad·G-flow·정합). 가장 약한 1곳(L_q∝ 조건 생략)→보강.
  - **Codex 전영역 최종**: **DOCUMENT CLEAN — 전 절 확정결함 0**. §6↔§7 도구 인용 4건 정합, §5→§6→§7→§8 비약 0, §1~5 회귀 0, 참조 139·라벨 48 undefined/중복 0, 서지 17 일치. 의심 2건(로드맵·"다섯 절")→clarity 보강.
- **추정/근거미발견/미검증**: 없음.

## Gate
**PASS_A3-A5_STATMECH** — Claude + Codex 동시 DOCUMENT CLEAN. 사용자 두 요청 충족: eq#29 줄나눔(A.1) + §6 통계역학 학부 초년생 접근성(신규 절).

## Confirmed Non-Changes
- §7 dist 핵심 수식(eq:superpose 적분·분산전파·rigorbox·boundbox) 값 보존 — 도구 인용·연결만 추가. §1~5 내용(레이아웃만). 핵심 결과식 값.

## Next
챕터 A 완료. 사용자 검토. 후속: 충전 branch·Ch2~5(별도), 피팅 부록.
