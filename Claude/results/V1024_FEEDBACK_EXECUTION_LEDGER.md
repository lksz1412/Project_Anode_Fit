# v1.0.24 1차 피드백 리비전 — Execution Ledger (12-col, FB-계열)

> 캠페인 = 사용자 1차 정독 피드백(F-01~F-11) 문건 리비전. 계획서 = `plans/2026-07-22-v1024-feedback-revision-plan.md`.
> cumulative step FB-계열 1부터(반영 R-계열 1–27 종료 후 신규). 코드 `.py` 무변경(bit-exact sha256 f230f59b). commit=master.
> 지배 gate: CLOSING_v1.0.15(헌법3종+D1-6)·V1020_STYLE_RUBRIC(A~G)·V1013_TERMS_POLICY·V1014_TONE_AUDIT.

| Phase | Planned | Actual | Block | Purpose | Status | Plan | Result | Machine Artifacts | Validation | Gate | Next |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| FB0 | 1-5 | 1-5 | setup | 착수·이력정독·4 인벤토리·baseline·결정 D1-6 락 | PASS | `plans/2026-07-22-v1024-feedback-revision-plan.md` | `PHASE_FB0_RESULT.md` | `comp_v24/INV_code_in_body.md`·`INV_overflow.md`·`TERM_DECISION_TABLE.md`·`INV_register_titles_prose.md`·`HIST_*.md`·`FB0_code_baseline.sha256` | 빌드 91/28/20 0-err·0-undef · 게이트 3스위트 PASS(G1 max\|d\|=0) · 코드 sha256 고정 · 4 인벤토리 · Read Coverage(register/term honest-gap 명기) | PASS_FB0_BASELINE | 6 |
| FB1 | 6-11 | 6-11 | code | F-11 코드=부록 정리(전역·최우선)+재발 grep 게이트 | PASS | 〃 | `PHASE_FB1_RESULT.md` | 8 tex 편집(gr2L·lcoomega·sifr·cases·blend·notation·sec05_code·bib)+마스터 `\appendix` | 본문 코드토큰 grep=0 · 빌드 91/28/20 0-err·0-undef · §3.5 부록이전 참조무결 · Fig2 캡션 물리 · **F-09 식2.39 overflow 부수해소** · 코드 sha256 무변경 | PASS_FB1_CODE_TO_APPENDIX | 12 |
| FB2 | 12-14 | 12-14 | typeset | F-06 조판 전역(preamble) | PASS | 〃 | `PHASE_FB2_RESULT.md` | `common_preamble_v1024.tex`(여백25·줄간1.16·문단0.55·microtype)·`fb2_compare.png` | 빌드 98/30/21 0-err·0-undef · 전/후 렌더 밀도↓ · 단일 소스 정합 · 페이지수 91→98·28→30·20→21 | PASS_FB2_TYPESET | 15 |
| FB3 | 15-24 | 15-24 | authoring | F-04 register+F-05 제목+F-10 용어 전역(4서브 G1-G4+master 통합) | PASS | 〃 | `PHASE_FB3_RESULT.md` | 25 tex(제목31·G1흑연본문·G2 LCO·G3 PartT·G4 Ch3+부록)+master 용어통일(음함수 국문복원·요동/양성 영문·유일근 풀어쓰기·정직한한계→적용·sec04 self-diff 평서화) | 빌드 98/30/21 0-err·undefined ref/cite 0 · full-diff invariant 4종(eq/label키/주석/xref키 변경 0) · 용어 running-form grep 통일 · register offender(survival술어·판번호·정직형용사) 소거 · TOC 5쌍 정합 | PASS_FB3_REGISTER_TERM | 25 |
| FB4 | 25-30 | — | notation | F-02+F-03+F-05 노테이션 | 대기 | 〃 | — | — | — | — | — |
| FB5 | 31-35 | — | overflow | F-07+F-09+전역 overflow | 대기 | 〃 | — | — | — | — | — |
| FB6 | 36-39 | — | content | F-01+F-08 국소 | 대기 | 〃 | — | — | — | — | — |
| FB7 | 40-46 | — | closeout | 검증·N회 적대검수·마감 | 대기 | 〃 | — | — | — | — | — |

## 인벤토리 요약(FB0 산출 — 후속 phase 입력)
- **F-11(FB1)**: 본문 코드언급 17행(gr2L 6·lcoomega 3·blend 3·notation 1·cases 1·sifr 2·bib 1) + §3.5 절 전체(D5).
- **F-04(FB3)**: register offender ~94행(제목 11·본문 83). 집중처 = ch3v22_sec01_map·ch1_appD_si·ch1_sec16b_lcoomega. 최우선 = lcoomega 판번호 노출(D1 위반)·적대검토 수사문답 3파일.
- **F-10(FB3)**: 미결 6개어 = 요동·양성(최우선)·음함수·섭동·유일근·준위. 승계 = V1013 27+18 + 대정준/정준/분배함수.
- **F-06/07/09(FB2·FB5)**: F-07(E.3 좌측)·F-09(식2.39 cases) 렌더-only(경고無). 조판 레버 = 여백22→26·줄간1.12→1.18·문단0.45→0.6·microtype. FB2 후 재스캔.
