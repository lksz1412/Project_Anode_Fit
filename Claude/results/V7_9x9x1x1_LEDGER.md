# Ch1 v7 — 9+9+1+1 경쟁·체리픽 LEDGER

> plan = `Claude/plans/2026-06-29-ch1-v7-codeflow-equation-driven-9x9x1x1-plan.md`. spine = `Claude/results/v7-00_spine/`. 11 문건 + 검토 4 추적·복구지점. ★푸쉬 없음.

## Phase 진행 (12-col)

| Phase/Subphase | Planned Steps | Actual Steps | Block | Purpose | Status | Plan | Result | Machine Artifacts | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| Phase0.1 | 1-4 | 1-4 | setup | v11 정독·곡선식 인벤토리 | PASS | plan | v7-00_spine/v11_flowchart.md | Anode_Fit_v11_final.py | v11 1-706 정독·11노드 매핑 | PASS_SPINE_INVENTORY | 5 |
| Phase0.2 | 5-9 | 5-9 | setup | 플로우차트·AUTHOR_BRIEF | PASS | plan | v7-00_spine/AUTHOR_BRIEF.md | v11_flowchart.md | 노드↔메서드 1:1·brief 9항 | PASS_BRIEF | 10 |
| Phase1.1 | 10-14 | 10-14 | build | 9종 독립 작성(자체10회) | PASS | plan | v7-01..09/ | NOTE/PDF ×9 | 9/9 xelatex 0-err·ref undef 0·렌더 fig 영어전용(01/03 주석만 한글) | PASS_9_DRAFTS | 15 |
| Phase2.1 | 15-18 | 15-18 | review | 검토1 교차 | PASS | plan | PHASE2_v7_review9.md | REVIEW1×9 | 9종 6렌즈·系統 A-상수 결함 적발·v7-04/05 베이스 | PASS_REVIEW1 | 19 |
| Phase3.1 | 19-22 | 19-22 | build | 보완 9종(방향성만) | PASS | plan | v7-01..09/*b.tex | NOTEb/PDF×9 | 9/9 0-err·新부호회귀 0·flowchart 분극 정정(v7-05b 적발) | PASS_9_SUPPL | 23 |
| Phase4.1 | 23-25 | 23-25 | review | 검토2 | PASS | plan | PHASE4_v7_review9b.md | REVIEW2×9 | 보완 회귀 3건 적발(이식금지)·v7-06b 30/30 | PASS_REVIEW2 | 26 |
| Phase5.1 | 26-30 | 26-30 | build | 체리픽 v7-10(v6합류) | PASS | plan | v7-10/v7-10.tex | v7-10.pdf | 베이스 v7-06b+G-usable graft·v6 물리 교차검증·0-err 16p | PASS_CHERRYPICK | 31 |
| Phase6.1 | 31-33 | — | review | v7-10 재검수 | PENDING | plan | PHASE6_v7_review_v10.md | — | — | — | 34 |
| Phase7.1 | 34-39 | — | build | v7-11 최종+10회 | PENDING | plan | v7-11/ | — | — | — | 40 |
| Phase8.1 | 40-42 | — | wrap | 종합·메타평가 | PENDING | plan | PHASE8_v7_FINAL_RESULT.md | — | — | — | — |

## 11 문건 상태

| # | 버전 | 모델 | 단계 | 상태 | 산출 | 비고 |
|---|---|---|---|---|---|---|
| 1 | v7-01 | Sonnet | ① | ✅done | v7-01/v7-01.tex | 15p·28식·TikZ4·0-err / fig 주석 한글 24자(정리 대상) |
| 2 | v7-02 | Sonnet | ① | ✅done | v7-02/v7-02.tex | 14p·863줄·TikZ5·0-err·fig 영어전용 |
| 3 | v7-03 | Sonnet | ① | ✅done | v7-03/v7-03.tex | 15p·TikZ5·0-err / fig 주석 한글 8자(정리 대상) |
| 4 | v7-04 | Opus | ① | ✅done | v7-04/v7-04.tex | 16p·~30식·TikZ5·0-err·fig 영어전용·G-usable 6step |
| 5 | v7-05 | Opus | ① | ✅done | v7-05/v7-05.tex | 17p·65KB·39식·TikZ5·0-err·fig 영어전용·SymPy 재유도 |
| 6 | v7-06 | Opus | ① | ✅done | v7-06/v7-06.tex | 15p·55KB·TikZ5·0-err·fig 영어전용·부호검산 §10 |
| 7 | v7-07 | Codex | ① | ✅done | v7-07/v7-07.tex | 12p·32KB·TikZ4·0-err·fig 영어전용 |
| 8 | v7-08 | Codex | ① | ✅done | v7-08/v7-08.tex | 9p·24KB·TikZ4·0-err·fig 영어전용 |
| 9 | v7-09 | Codex | ① | ✅done | v7-09/v7-09.tex | 9p·28KB·TikZ6·0-err·fig 영어전용 |
| 10–18 | v7-01b…09b | 원모델 재지시 | ② | ✅done | v7-NN/v7-NNb.tex | 방향성만·9/9 0-err / 01b15p·02b14p·03b15p·04b16p·05b18p·06b16p·07b13p·08b10p·09b11p / 系統 A-상수 교정 반영 |
| 19 | v7-10 | Opus | ③ | ✅done | v7-10/v7-10.tex | 베이스 v7-06b + 전 인자표·6단계 재현 graft·v6 교차검증·16p 0-err |
| 20 | v7-11 | master→Opus | ④ | pending | v7-11/v7-11.tex | 최종·정식10회 |

## 커밋 로그
- 88b249e (시작): 계획서 + v11_final spine 도입.

## 진행 로그
- Phase 0: spine 3종(v11_final.py·v11_flowchart.md·AUTHOR_BRIEF.md) 생성. Phase 1 디스패치 준비.
