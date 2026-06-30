# Ch1 v8 — 유도 확장판 9+9+1+1 LEDGER

> plan = `Claude/plans/2026-06-29-ch1-v8-derivation-expanded-9x9x1x1-plan.md`. v8 = v7-11(배치 보존)+v5(유도 복원). spine = `v8-00_spine/AUTHOR_BRIEF_v8.md` + `v7-00_spine/{v11_flowchart.md, Anode_Fit_v11_final.py}`. ★푸쉬 없음. 그림 경쟁(v7-11 5개 후보 + 신규).

## Phase 진행 (12-col)
| Phase | Planned | Actual | Block | Purpose | Status | Plan | Result | Artifacts | Validation | Gate | Next |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| 0.1 | 1-4 | 1-4 | setup | v7-11·v5 정독·유도 인벤토리 | PASS | plan | (brief 내장) | AUTHOR_BRIEF_v8 | v7↔v5 매핑·11식 유도단계 | PASS_INV | 5 |
| 0.2 | 5-9 | 5-9 | setup | v8 brief·폴더 | PASS | plan | AUTHOR_BRIEF_v8.md | v8-01..11/ | 유도 의무·그림경쟁 명문 | PASS_BRIEF | 10 |
| 1.1 | 10-14 | 10-14 | build | 9종 독립(v7-11+v5·자체10회) | PASS | plan | v8-01..09/ | NOTE/PDF×9 | 9/9 xelatex 0-err·렌더 그림 한글 0·배치 보존·유도 복원·그림 6~9개(경쟁) | PASS_9_DRAFTS | 15 |
| 2.1 | 15-18 | 15-18 | review | 검토1(+G-derive) | PASS | plan | PHASE2_v8_review9.md | REVIEW1×9 | ★D-PEAK 상속 8/9 전파 적발·부호 9종 8/8·베이스 v8-06 | PASS_REVIEW1 | 19 |
| 3.1 | 19-22 | 19-22 | build | 보완 9(방향성만) | PASS | plan | v8-NNb×9 | NOTEb/PDF×9 | 9/9 0-err 19~22p·D-PEAK 8종 정정·v8-01b 표값/v8-04b fig 정정·Codex one-shot(절차 미준수 시인) | PASS_9_SUPPL | 23 |
| 4.1 | 23-25 | 23-25 | review | 검토2 | PASS | plan | PHASE4_v8_review9b.md | REVIEW2×9 | D-PEAK 정정 직접검산·보완회귀 3종 적발·베이스 v8-06b 34/35 | PASS_REVIEW2 | 26 |
| 5.1 | 26-30 | 26-30 | build | 체리픽 v8-10(v6·그림경쟁) | PASS | plan | v8-10/v8-10.tex | v8-10.pdf | 베이스 v8-06b+D-PEAK2 문턱불연속·그림 9(경쟁승자)·3-pass 0-err 21p | PASS_CHERRYPICK | 31 |
| 6.1 | 31-33 | 31-33 | review | v8-10 재검수 | PASS | plan | PHASE6_v8_review_v10.md | REVIEW_A/B | 빈통과거부·확정 CRIT/HIGH 0·LOW 폴리시 4·부호 8/8·11식 G-derive 통과 | PASS_REVIEW_V10 | 34 |
| 7.1 | 34-39 | 34-39 | build | v8-11 최종+10회 | PASS | plan | v8-11/v8-11.tex | v8-11.pdf·ROUND×3 | 폴리시 4·doublewell 메모 제거·최종 3갈래 CRIT/HIGH/MED 0·부호 8/8·G-usable 닫힘·3-pass 0-err 21p | PASS_V8_FINAL | 40 |
| 8.1 | 40-43 | — | wrap | 종합·메타·스킬화 | PENDING | plan | PHASE8_v8_FINAL_RESULT.md | Project_skills/ | — | — | — |

## 11 문건
| # | 버전 | 모델 | 단계 | 상태 | 비고 |
|---|---|---|---|---|---|
| 1-3 | v8-01/02/03 | Sonnet | ① | ✅done | 18/18/18p·그림 6/7/8·유도 11식 복원·부호 8/8·0-err |
| 4-6 | v8-04/05/06 | Opus | ① | ✅done | 22/21/21p·그림 8/8/9·유도 복원·자체 다중검수·부호 8/8·0-err (06=529 2회 후 재가동) |
| 7-9 | v8-07/08/09 | Codex | ① | ✅done | 20/21/20p·그림 5/6/6·유도 복원·부호 8/8·0-err |
| 10-18 | v8-01b…09b | 재지시 | ② | ✅done | 방향성만·9/9 0-err(01b19·02b19·03b19·04b22·05b21·06b21·07b20·08b21·09b21p)·D-PEAK 8종 정정(01은 무보유 유지)·새 회귀 self-test |
| 19 | v8-10 | Opus | ③ | ✅done | 베이스 v8-06b(34/35)+D-PEAK2 문턱 정직기술·그림 9(v7-11 5+신규 4)·3-pass 0-err 21p |
| 20 | v8-11 | master→Opus | ④ | ✅done | ★최종 권고본 — 유도 확장 교과서판·21p·그림 9·부호 8/8·11식 G-derive·3-pass 0-err |

> **★완료: 20/20 산출. 최종 권고본 = v8-11/v8-11.tex (21p, 유도 과정 포함 교과서 확장판).**

## 커밋 로그
- (시작 예정): v8 계획서 + AUTHOR_BRIEF_v8 + ledger.

## 진행 로그
- Phase 0: v8 brief(유도 깊이·그림 경쟁·11식 유도사슬) + 폴더. Phase 1 디스패치 준비.
