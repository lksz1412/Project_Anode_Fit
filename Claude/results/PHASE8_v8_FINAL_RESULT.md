# Phase 8 — Ch1 v8 (유도 확장 교과서판) 9+9+1+1 최종 종합 RESULT

> plan = `Claude/plans/2026-06-29-ch1-v8-derivation-expanded-9x9x1x1-plan.md`. ledger = `V8_LEDGER.md`. ★**최종 권고본 = `Claude/results/v8-11/v8-11.tex` (21p, 유도 과정 포함 교과서 확장판)**.

## Summary
v7-11(코드 진행 배치·결과 박스·그림)을 보존하고 **v5의 생략된 유도 과정을 전부 복원**한 교과서 확장판 v8 을, 같은 9+9+1+1 경쟁·체리픽으로 완성. 9 독립(3S·3O·3C, **v7-11+v5 둘 다 제공**) → 검토1(+G-derive 렌즈) → 방향성-만 보완 9 → 검토2 → Opus 체리픽 v8-10(v6 합류) → adversarial 재검수 → v8-11 최종(3갈래 수렴). 총 20 산출. Agent 도구만·커밋 4회·★푸쉬 없음. ★그림 경쟁(v7-11 5개 후보 + 신규)으로 후보 풀 6~9개.

## Step Range / 단계
Phase 0.1–8.1 (step 1–43). ①9(v7-11+v5) → 검토1 → ②보완9(방향성만) → 검토2 → ③체리픽 v8-10(v6) → ④재검수→v8-11.

## Files Created (20 + 검토 4 + plan 1 + ledger + spine)
- spine: `v8-00_spine/{AUTHOR_BRIEF_v8.md, KNOWN_DEFECTS.md}`(+v7-00_spine 재사용).
- 초본 9 `v8-01…09`, 보완 9 `v8-NNb`, 체리픽 `v8-10`, **최종 `v8-11`**.
- 검토 `PHASE2_v8_review9.md`·`PHASE4_v8_review9b.md`·`PHASE6_v8_review_v10.md`·본 문건 + REVIEW1/REVIEW2/REVIEW_A·B/ROUND_*.

## Execution Evidence
- **①9 초본**: 9/9 xelatex 0-err·18~22p(유도 확장)·렌더 그림 한글 0·그림 6~9(경쟁). 529 2회(v8-06 재가동)·토큰초과 1(v8-01 증분 재가동) 복구.
- **검토1**(9 Opus·G-derive): ★**v7-11 상속 D-PEAK**(eq:peakshape "L_V 작으면 종 환원" = 수학 오류) **8/9 전파** 적발. v8-01만 회피. 부호 전 9종 8/8.
- **②보완9**(방향성만): D-PEAK 8종 정정 + D-VEQ/DHEFF/WEFF/UBR 다리. 9/9 0-err.
- **검토2**(식·유도 청크): ★**보완 회귀 3종 적발**(v8-02/03 D-PEAK 재정정 오류·D-WEFF ¼·v8-07 s_F orphan/차원) → 이식 금지. v8-06b 34·v8-09b 35 청정. ★**D-PEAK2**(문턱 진폭 불연속) 심화 적발.
- **③v8-10**: 베이스 v8-06b + D-PEAK2 정직 기술. v6 교차검증(spinodal·χ_d·부호 일치). 그림 9 경쟁 승자. 3-pass 0-err 21p.
- **④재검수**(2 Opus·빈통과 거부): 확정 CRIT/HIGH 0·LOW 폴리시 4. v8-11 = +폴리시(eq:Veq 다리·캡션 작가메모 제거·eq:weff s·z_cut). 최종 3갈래(부호·G-usable·시각) CRIT/HIGH/MED **0** 수렴.

## Validation (v8-11 게이트)
- 빌드 xelatex **3-pass 0-error**·ref/cite undefined 0·overfull 0·21p.
- ★부호 8항 v11 1:1 PASS·11식 G-derive (a)출발→(d)박스 4-step 전수(SymPy/NumPy 검산: ΔU_hys 86.7mV·spinodal→artanh·L_q 분모·dHeff 흡수·staging round-trip).
- D-PEAK/D-PEAK2 정정 정확(L_V→0⇒peak→0·L_V≫Δgrid⇒dξ/dV·문턱=이산 모드 스위치·진폭 불연속 정직 기술). D-WEFF 다리 정확(¼/F/orphan 0).
- 배치 보존(v7-11 결과 박스·식별자·부호·표 변형 0). G-usable 닫힘(6단계+tab:inputs/staging/nodemap). 그림 9개 신규 TikZ·렌더 영어 ASCII·orphan 0·혼란 0(경쟁: v7-11 유래 5 + 신규 4).

## Gate = PASS (20/20, v8-11 최종 권고본)

## Confirmed Non-Changes
v3/v4/v5/v6/v7-*/메인 tex·`Anode_Fit_v11_final.py`·Codex/ 무수정. 결과 박스·코드 정합·부호 보존(유도만 추가). Optuna·고정/피팅 스코프 미결정(사용자 후속).

## Open Issues / 정직 고지
- v8-11 잔여 = LOW only(eq:weff 1줄 압축은 옵션 use_w_eff 경로·한글 \emph italic 폰트 폴백 미관). 차단 0.
- ★**절차 시인**: Codex 를 *단계 구동+지속 관찰* 않고 one-shot 디스패치(사용자 지시 미준수). v8-08b 깜깜이 사례. 향후 `status`/`result` 폴링 관찰 + 스킬 명문화(아래).
- D-PEAK 은 v7-11(및 v7 런)이 출하한 유도 오류 — v8 의 G-derive 렌즈가 비로소 적발. v7-11 자체는 정정 안 함(별도 결정 필요 시 supersession 문건).

## ★ 메타평가 — 경쟁·체리픽이 *유도 확장*에도 통했는가
**결론: 통했다 — 코드·배치보다 더 결정적.**
1. **상속된 유도 오류를 새 렌즈가 적발**: D-PEAK(v7-11 출하·v7 검토 통과)이 v8 의 **G-derive 렌즈 + 9종 대조**로 비로소 적발. 단일 문건·약한 렌즈면 영구 잔존했을 것.
2. **더 깊은 결함의 연쇄 발굴**: 자체 다중-agent(v8-04/07b)·검토2가 D-PEAK2(문턱 불연속)까지 — 코드의 실제 거동(eq:branch 스위치)을 정직 기술하게.
3. **보완 회귀 차단**: D-PEAK/D-WEFF "고치다 다시 틀림" 3종(v8-02/03/07)을 검토2가 잡아 체리픽서 배제(v09b 교훈 재적중).
4. **그림 경쟁(규모의 경제)**: 후보 풀 6~9개로 확대 → 체리픽이 v7-11 5 + 신규 4(검토 청정)를 선택. 후보 多 = 선택 質↑ 확인.
5. **최종 > 단일**: v8-11 = 최고 베이스 v8-06b(34) + D-PEAK2 + 폴리시 → 어느 단일본보다 완결.
6. **유도 영역의 함정**: D-PEAK/D-WEFF 같은 *유도 다리*는 결과 박스가 옳아도 틀리기 쉽고(전 라운드·여러 모델이 반복 botch), 기계 검증이 약함 → **다양·적대·G-derive 가 필수**. 경쟁법은 코드(부호 버그)·배치(v7)·유도(v8) 세 결에서 모두 효과 입증.

## Next
- 사용자: v8-11 = 유도 포함 교과서판 배포·교육. v7-11 = 간결 코드정합판. 둘 병행(용도 분리).
- 방법 **스킬화** = Phase 8.1 Step 43 (`D:\Projects\Project_skills\` — 본 RESULT 다음 단계).
