# Phase 8 — Ch1 v7 9+9+1+1 경쟁·체리픽 최종 종합 RESULT

> plan = `Claude/plans/2026-06-29-ch1-v7-codeflow-equation-driven-9x9x1x1-plan.md`. ledger = `V7_9x9x1x1_LEDGER.md`. ★**최종 권고본 = `Claude/results/v7-11/v7-11.tex` (17p)**.

## Summary
흑연 음극 dQ/dV(ICA) Chapter 1 의 **v7 문건**을, 최종 코드 `Anode_Fit_v11_final.py`(706줄)의 클래스 계산 진행(플로우차트 N0→N9)을 척추로 삼아 **수식 주도(v5 형식)·코드 진행 어레인지(v6 방식, 대상 코드는 v11)**, 그림 전부 신규(영어 라벨)로 작성. **9종 독립 경쟁(3 Sonnet·3 Opus·3 Codex, v5만) → 방향성-만 보완 9종 → 2회 교차검토 → Opus 체리픽 v7-10(v6 합류) → adversarial 재검수 → 최종 v7-11(정식 수렴 검수).** 총 20 산출. 전 과정 Agent 도구(Workflow 미사용)·커밋 4회·★푸쉬 없음(Codex 월 한도).

## Step Range / 단계
Phase 0.1–8.1 (cumulative step 1–42). ①9(v5만) → 검토1 → ②보완9(방향성만) → 검토2 → ③체리픽 v7-10(v6 합류) → ④재검수→v7-11.

## Files Created (20 문건 + 검토 6 + plan 1 + ledger)
- 척추: `v7-00_spine/{Anode_Fit_v11_final.py, v11_flowchart.md, AUTHOR_BRIEF.md}`.
- 초본 9: `v7-01…09/v7-NN.tex`(+pdf+NOTE). 보완 9: `v7-NN/v7-NNb.tex`. 체리픽 `v7-10/v7-10.tex`. **최종 `v7-11/v7-11.tex`**.
- 검토: `PHASE2_v7_review9.md`·`PHASE4_v7_review9b.md`·`PHASE6_v7_review_v10.md`·본 문건 + 개별 `REVIEW1/REVIEW2/REVIEW_A·B/ROUND_*`.

## Execution Evidence
- **①** Claude 6 + Codex 3 전부 xelatex 0-error(14–17p Claude·9–12p Codex)·각자 자체 10R 수렴·신규 TikZ 4–6개 영어전용.
- **검토1**(9 Opus): 점수 v7-04/05=27·06=26… 09=20. ★**系統 결함 적발** — 다수 문건이 `∂lnL_q/∂V<0`+전위의존 A 를 부호체크로 내세웠으나 v11 의 A 는 전이당 상수 컷(L335). v7-04/03 만 회피.
- **②** 보완 9(방향성만·코드 X). ★분극 물리 정정: v7-05b 보완 에이전트가 *master 의 flowchart 오류*(방전 시 측정 V 방향) 적발 → 검산 후 spine 정정.
- **검토2**(9 Opus·식·부호사슬 청크): v7-06b **30/30**(자기모순 해소)·04b/05b 28. ★**보완 회귀 3건 적발**(v7-01b arrhenius 부호·03b fig:logistic 손상·09b logitsolve n²) → 이식 금지(v09b 코드 교훈 적중).
- **③ v7-10**: 베이스 v7-06b + G-usable graft(전 입력인자·기본값 표·6단계 재현 박스). v6 합류: spinodal gap·χ_d/ΔH_eff·분극 교차검증 일치, v11 컷-상수 A 가 v6 전위의존 A 보다 코드 정합 확인.
- **④ 재검수**(2 Opus, 빈통과 거부): 부호 8/8·인자표 0오류 확인 + 보완 6건(기본폭 식·L_q 분모 유도다리·logistic n·z_cut 표기·부호순). **v7-11** 작성.
- **최종 수렴**(4 갈래·가변 청크·렌즈): 부호 8/8·신규 유도 3건 수학 정확·코드 4항 재현·G-usable 닫힘·혼란 그림 0·형식 0결함. CRIT/HIGH **0**, LOW 1(U(298) 0.0855→0.0853 정정).

## Validation (v7-11 게이트)
- 빌드 **xelatex 3-pass 0-error**·ref/cite undefined 0·17p.
- 척추 N0→N9 절 1:1·노드맵 표·식별자 코드 1:1.
- ★부호 사슬 8항 PASS(코드 대조)·verifybox 4 수치 회귀(86.7mV·u=0.766·Ω=2RT→0·|I|→0 환원).
- 신규 유도 다리(기본폭·L_q 분모 정·역 합·logistic n) 수학 정확·func_w/ksi_eq/L_q 4항 재현.
- 그림 5개 신규 TikZ·**렌더 영어 ASCII 전용**·orphan 0·식 좌표 정합(혼란 그림 0).
- G-usable: 6단계 재현 박스+tab:inputs(전 인자·기본값 0오류)+tab:staging+tab:nodemap 으로 곡선 재현 닫힘.

## Gate = PASS (20/20 산출, v7-11 최종 권고본)

## Confirmed Non-Changes
원본 v3/v4/v5/v6/메인 tex·`Anode_Fit_v11_final.py`·Codex/ 무수정. 기존 그림 재사용 0(전부 신규). Optuna·피팅 절차·고정/피팅 스코프 미결정(사용자 후속). ※spine flowchart 의 분극 서술 1줄은 *내 작성물*이라 정정(원본 아님).

## Open Issues / 정직 고지
- v7-11 잔존 = advisory LOW(eq:weff 가 n_j 미포함 — 옵션 경로·코드 func_w_eff 설계대로, 비차단). 차단 결함 0.
- 분량: v7-11 17p — v5/v6(36–50p) 대비 짧다. v7 는 *곡선에 필요한 식만*(11 노드)으로 의도적 축소(전 통계역학 유도는 결과식 인용만). 사용자 의도("실제 표현에 필요한 수식만") 정합.
- Codex 3종(07/08/09)은 Claude 대비 짧고(9–12p) 유도 빈약 경향 — 보완으로 개선됐으나 체리픽 베이스엔 안 듦.

## ★ 메타평가 — 경쟁·체리픽이 *문건*에도 통했는가 (테스트 베드 본 목적)
**결론: 통했다 — 코드보다 오히려 더 가치 있었다.**
1. **단일 문건이면 출하했을 결함을 다양성이 표면화** — (a) 系統 A-상수 vs ∂lnL_q/∂V 모순(v5/v6 계승, 4/9 문건 보유)은 v7-04/03 이 회피한 *대조*가 있어 드러났다. (b) 더 결정적으로, **내(master)가 쓴 spine flowchart 의 분극 부호 오류를 보완 에이전트가 독립 검산으로 적발** — 단일 권위로는 못 잡았을 자기 오류.
2. **보완 단계 회귀를 교차검토가 차단** — 검토2가 보완-유입 회귀 3건을 잡아 체리픽서 배제(코드판 v09b 교훈이 문건에서도 재현·적중).
3. **30/30 베이스에도 adversarial 신선 검수가 실질 결함 적발** — Phase6 가 L_q 분모 유도 누락·기본폭 참조 함정을 잡았다(좋은 단일 저자도 출하한 유도 다리 공백).
4. **최종본 > 임의 단일 문건** — v7-11 = 최고 베이스(v7-06b) + G-usable graft + 6 유도/참조 보완. 어느 단일 산출보다 완결(부호 8/8·G-usable 닫힘·유도 다리 메움).
5. **비용** — 문건 작성 ~20 + 검수 ~24 에이전트(+Codex 6). 토큰 큼(사용자 사전 수용). 문건 결함은 빌드로 안 걸리는 *물리 서술·유도·그림* 류라 기계 검증이 약함 → **다양·적대 다세션이 코드보다 더 결정적**.
6. **스킬화 권고** — 高가치 레퍼런스/배포 문건에 적합. 단 (a) 토큰 비용 큰 작업에 한정 (b) Codex 는 분량·유도서 Claude 대비 약함(역할 한정 권장) (c) 系統 결함 적발이 핵심 가치이므로 *동일 브리프·독립 무통신* 유지가 관건. → 스킬화 시 "경쟁 N + 방향성-보완 + 교차검토 2회 + 체리픽 + adversarial 최종" 골격 권장.

## Next
- 사용자: v7-11 의 tab:inputs(전 인자·기본값) + 6단계 재현 박스로 v11 곡선을 BDD 백엔드에서 재현·Optuna 피팅. 고정/피팅 스코프 직접 결정.
- 스킬화 진행 여부 결정(메타평가 6 참조).
