# 계획서 — Chapter 1 완전 백지 재작성: clean-spine 서사 우선 (BP-series)

**Date**: 2026-06-03 · **Author**: Claude(메인) · **상태**: 사용자 방향 GO 수령(완전 백지 메인 + 부록 B 서브에이전트 보조). 본 계획 확정 후 즉시 실행.
**양식**: 표준 11-section(`feedback_plan_template_11sections`) + cumulative step(BP-1~) + Phase 5-stage 루프(`feedback_phase_execution_loop`).
**선행 진단**: 본 세션 §6→§7 단절·L/Θ 무근거 등장 정밀 진단(본문 L422/L514/L453 증거). 표준(GS-1·N-1·방향-1)은 옳았으나 게이트가 *국소 정당화*만 검사, no-leap 압력이 *과잉 단서*를 유발해 줄기를 묻음.

---

## Summary

기존 `graphite_ica_ch1_rebuilt.tex`(1629줄, 부록 B 670줄 흡수)를 **버리고**, 서(序)의 5단계 인과 사슬과 RB 6원칙/GS-1~4/N-1~5 *기획의도만 계승*해 Chapter 1 을 **완전 백지에서 재유도**한다. 실패의 근본(줄기 실종)을 잡기 위해, 기존에 없던 **clean-spine 게이트군**(G-spine/G-motive/G-interpret/G-nofwd/G-bridge/G-reader)을 no-leap·grounding 게이트와 *긴장-균형*시켜 새로 도입한다. 핵심 규칙 = **엄밀성(BOUNDED/FLAGGED/별개 단서·측도론 형식)은 박스로, 본문 줄기는 깨끗하게.** 부록 B(피팅 워크플로/수치, 구 Ch6)는 Ch1 에서 **분리**해 별도 보조 문서로 두고 서브에이전트가 같은 표준으로 병행 재작성한다. 산출 = `graphite_ica_ch1_clean.tex`(메인, 신규) + `graphite_ica_ch1_appendixB_fitting.tex`(보조, 서브에이전트). 기존 `_rebuilt` 전부 보존(덮어쓰기 금지).

## Current Ground Truth

**확정 사실**
- 현 `graphite_ica_ch1_rebuilt.tex`: 서(L81-110) + 14 절 + 부록 B(L893-1563, 구 Ch6). 빌드 GREEN. **물리 식 자체는 대체로 건전**(Eyring 부호·bib·χ_j 한정·기호표 상수 등 직전 세션에 교정 완료).
- 실패는 *서술*: ① L 이 §6 L422 에서 유도 중 치환으로 등장(동기 부재) ② Θ 가 §7 L514 에서 쓰이나 정의는 §12(forward ref) ③ §6→§7 이 단일 ODE→측도론 spectrum 으로 기계 도약 ④ BOUNDED/FLAGGED/별개/이중계상 단서가 본문 줄기를 끊음.
- 선행 계획(2026-05-30 undergrad, 2026-05-29 intent-gap)이 학부 가독·단일 서사를 이미 규정했으나, 게이트가 국소(각 step 정당성·agent 의 boxed 식 재현)만 검사해 전역 서사를 못 잡음. **no-leap 게이트가 과잉 단서를 미덕화**한 것이 역설적 원인.

**계승 대상(사용자 "기획의도만 가져와서")**
- 서의 5단계 인과 사슬(저온 긴 꼬리 관찰 → 평형열역학 무대 + 동역학 주역 → 전하보존이 V_n 결정 → relaxation-length spectrum → 피팅 닫힌식). 표현은 다듬되 골자 유지.
- RB 6원칙 / GS-1~4 / N-1~5 intent. 단 Ch1 = **최대한 심플**(2026-05-30 plan §128 사용자 명시).

**미확인**
- 새 Ch1 의 정확한 절 수·길이(아래 골격은 최소 기준점, `feedback_step_granularity_flexibility`).
- 부록 B 보조 문서의 Ch1 식 cross-ref 는 새 Ch1 확정 후 재동기(서브에이전트는 1차안 + 재동기 flag).

## Phase Range

> Phase ID = `BP.<n>`. Step = 전체 단조 누적(BP-1~). 5-stage 루프(골격→초안→줄기검증→적대검증→수정·result).

| Phase | 이름 | Step | 산출물 |
|---|---|---|---|
| **BP.0** | 골격·게이트 동결 + 절 spine 확정 | 1–4 | 본 계획서(절 spine + clean-spine 게이트) |
| **BP.1** | 메인 Ch1 무대(서+기호+전하보존+ξ_eq) 초안 | 5–9 | `graphite_ica_ch1_clean.tex`(§서~§3) |
| **BP.2** | 메인 Ch1 주역(배리어낮춤+완화/L+spectrum+kernel/Θ) 초안 | 10–16 | 동 파일(§4~§7) |
| **BP.3** | 메인 Ch1 닫기(Volterra+closure+피팅식+반증) 초안 | 17–21 | 동 파일(§8~§11) |
| **BP.4** | reader test + 적대검증(줄기·차원·grounding) | 22–26 | 검증 보고 |
| **BP.5** | 수정 + 빌드 GREEN + result(11항목) + Decision Gate | 27–30 | 확정 `..._clean.tex` + `RB_LEDGER_CH1_CLEAN.md` |
| **BP.A** | (병행, 서브에이전트) 부록 B 보조 문서 재작성 | A1–A5 | `graphite_ica_ch1_appendixB_fitting.tex` + 보고 |

## Non-goals

- 신규 물리 *발명*(인과 사슬 보존; 단 과축조 물리의 *심플화*·무근거 가정 재작성은 In). 
- Ch2~5 손대기(사용자 "Ch2~ 잊고 Ch1 만"). 기존 `_rebuilt` 덮어쓰기/삭제. push·main 머지(별도 GO).
- solver 코드 구현. 부록 B 의 수치 DAE 상세를 메인 Ch1 에 재흡수(분리 유지).
- 측도론 형식(Radon–Nikodym 등)을 본문 줄기에 노출(→ rigor box).

## Implementation Changes

**생성**: `Claude/docs/graphite_ica_ch1_clean.tex`(메인 백지 재작성), `Claude/docs/graphite_ica_ch1_appendixB_fitting.tex`(보조, 서브에이전트), `Claude/results/RB_LEDGER_CH1_CLEAN.md`(result 11항목).
**수정**: 없음(`graphite_ica_ch1_rebuilt.tex` 등 기존 전부 보존).
**작업파일**: `Claude/work/`(빌드).

## Phase BP.0 — 골격·게이트 동결 (step 1–4)

- step1 새 절 spine 확정(아래). step2 clean-spine 게이트군 정의(아래 Test Plan). step3 부록 B 분리 경계 확정(Ch1 은 이론 줄기까지 = 피팅 닫힌식·반증; 수치 워크플로·식별성·DAE 는 보조 문서). step4 신규 파일명·preamble 매크로 출처(기존 head 의 매크로 self-contained 복사).
- gate: spine 11 절이 "질문→새양 동기→유도→의미·용도→다리" 5비트로 1행씩 기술. 다음: BP.1.

**★ 새 Ch1 절 spine (단일 인과 사슬, 부록 B 제외 · 최소 기준점)**

| § | 절 | 핵심 질문 | 도입 새 양(동기 먼저) |
|---|---|---|---|
| 서 | 단일 인과 사슬 | 저온 긴 꼬리를 무엇이 만드나 | (5단계 사슬 제시) |
| 1 | 기호와 단위 | (참조용 compact 표 + 본문 first-use 정의 병행) | — |
| 2 | 무대(I): 전하 보존 → V_n | 전류 흐를 때 내부 전위는 어디서 오나 | V_n(전하보존식의 해) |
| 3 | 무대(II): 평형 진행률 ξ_eq | 평형만으로 왜 설명이 안 되나 | ξ_eq(logistic), w=RT/F(저온 좁아짐=관찰 반대) |
| 4 | 주역(I): 극판 전위 → 배리어 낮춤 → k_j | 전위가 속도를 어떻게 바꾸나 | 𝒜_j(구동력), χ_j, k_j(Eyring) |
| 5 | 주역(II): lag → 꼬리, 완화 길이 L | "꼬리가 얼마나 긴가"를 무엇으로 재나 | **L=꼬리 감쇠 길이**(동기 먼저 → 정의 → 저온 L↑=꼬리↑) |
| 6 | 주역(III): 여러 mode → spectrum A_L | 전극은 mode 가 하나가 아니다 | A_L(완화 길이 분포; 단일→다수→평균 graded bridge, 측도 변환은 box) |
| 7 | 관측 꼬리 = kernel integral | 분포를 어떻게 관측 꼬리로 합치나 | **Θ(용량가중 진행, 여기서 정의)**, kernel |
| 8 | 자기참조 → Volterra | 왜 목표가 미지에 의존하나(되먹임) | Volterra 2종(single-mode 의 2-일반화로 유도) |
| 9 | 닫기: 피팅 가능한 닫힌식 | 그래서 피팅에 쓸 식은 무엇인가 | 닫힌 ICA/DVA 식 + 심플 근사식(무거운 수치는 보조 문서) |
| 10 | 온도 의존 꼬리 분해·반증 | 이 주장을 어떻게 검정하나 | tail Arrhenius(Eyring 보정, χ𝒜 빼기), falsifiable 예측 |

## Phase BP.1–BP.3 — 메인 Ch1 본문 (step 5–21)

각 절을 **5비트 양식**으로 작성: ① 질문+왜 → ② 새 양 물리 동기(말 먼저) → ③ 무비약 유도 → ④ 결과의 물리적 의미·용도 → ⑤ 다음 절 다리. 단서·예외·BOUNDED/FLAGGED 는 전부 box. forward ref 0. 매 식 차원·부호·극한 검산은 box 또는 각주.

## Phase BP.4–BP.5 — 검증·확정 (step 22–30)

reader test(아래) + 적대검증(차원·부호·극한·grounding·LaTeX) → 수정 → 빌드 GREEN → result 11항목 → 사용자 Decision Gate.

## Phase BP.A — 부록 B 보조 (서브에이전트, 병행)

서브에이전트가 현 부록 B(L893-1563) 를 같은 clean-spine 표준으로 **별도 standalone 보조 문서**로 재작성. Ch1 식 cross-ref 는 placeholder + 재동기 flag. 메인 Ch1 파일 미접촉(충돌 방지).

## Implementation Interfaces

- **신규 파일명**: 메인 `graphite_ica_ch1_clean.tex`, 보조 `graphite_ica_ch1_appendixB_fitting.tex`. preamble 매크로 = 기존 head self-contained 복사(\AL, \cell, \ext, \eq, \drive, \app, \OCV, \dd 등).
- **빌드**: xelatex 2-pass, `-output-directory=/d/Projects/Project_Anode_Fit/Claude/work/build`, `^!`=0·undefined ref/cite=0.
- **Result/ledger**: `feedback_phase_execution_loop` 11항목. 보존 규약: 기존 문건 덮어쓰기 0.

## Test Plan

**★ clean-spine 게이트군 (이전 attempt 의 빈틈 — 신규)**
- **G-spine**: 모든 box(BOUNDED/FLAGGED/rigor/주의)를 건너뛰고 본문만 읽어도 줄기가 안 끊긴다.
- **G-motive**: 모든 새 기호(L·A_L·Θ·𝒜·χ…)가 *공식 앞에서* 물리 말로 동기 부여된다.
- **G-interpret**: 모든 구한 양이 *공식 뒤에서* 물리적 의미·용도(무엇을 모사하나)로 마무리된다.
- **G-nofwd**: 본문 줄기 내 forward reference 0(모든 양은 first-use 에서 정의).
- **G-bridge**: 절→절 수학 기계 도약 시 graded bridge 필수(§5→§6 단일→다수→평균). 형식(측도/Radon–Nikodym)은 box.
- **G-reader**: 본문 줄기만 읽은 독립 reader(agent)가 절마다 (i)무슨 질문 (ii)새 양 물리 의미 (iii)왜 구했나 를 답한다. 못 하면 그 절 재작성.

**기존 유지 게이트**: G-noleap(자명/clearly 0) · G-dim(차원) · G-ground(가정=AL+cite) · G-noungrounded(무근거 0) · G-latex(빌드 무결).

**충돌 해소 규칙(핵심)**: G-spine 과 G-noleap/G-ground 가 충돌하면 → **엄밀 단서는 box 로 이동, 줄기는 깨끗 유지**. 둘 다 만족(깊이는 box 에, 흐름은 줄기에).

## Assumptions

- A1: 인과 사슬·식 흐름은 사용자 의도와 일치(서 확인) → 백지 재유도이되 물리 *발명* 아님. 과축조(§6 측도론) 심플화는 In.
- A2: 부록 B 분리는 사용자 D2 결정(서브에이전트 보조). 메인 Ch1 은 피팅 닫힌식·반증까지로 자기완결.
- A3: 빌드 환경 사용자 측, 정적 검수 + PDF 확인.

## Decisions Required (사용자 — 평문, 무응답 시 권고값)

- **D1 해소**: 완전 백지(사용자 확정). 
- **D2 해소**: 부록 B 분리 + 서브에이전트 보조(사용자 확정).
- **D3 (메인 파일명)**: `graphite_ica_ch1_clean.tex`. 권고: 그대로. 이의 시 변경.
- **D4 (Ch1 자기완결 경계)**: 피팅 닫힌식·심플 근사식·반증까지 Ch1, 수치 DAE/식별성/closure 상세는 보조 문서. 권고: 그대로.

## Correction History

| 일자 | 변경 |
|---|---|
| 2026-06-03 (v1) | 최초 작성. 사용자 GO(완전 백지 메인 + 부록 B 서브에이전트). clean-spine 게이트군 신설, 새 11 절 spine, 부록 B 분리. |
