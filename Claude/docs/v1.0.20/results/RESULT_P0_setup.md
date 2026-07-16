# Phase P0 — 준비 Result

## Summary
v1.0.20 작업 기반 완비: v1.0.19 문건 복제(내용 무변경 실증)·버전 태그, 빌드 환경 구축 성공(xelatex+kotex+D2Coding — 3본 GREEN, 페이지수 v1.0.19 일치), 코드 회귀 기준선(플랫폼 잡음 수준), 구조 검증·변경 통제 도구, 스타일 rubric, CHANGE_LOG/ERRATA 체계, ledger.

## Step Range
Steps 1–10 (계획 1–10, 전건 수행).

## Inputs
`docs/v1.0.19/` 전체(복제 원본), `docs/v1.0.15/CLOSING_v1.0.15.md`(헌법), 킥오프 조사 2본, rubric 원천 tex 7파일(아래 Read Coverage).

## Files Created
`docs/v1.0.20/`: graphite_ica_ch1/ch2_v1.0.20.tex·_sections/(41)·figs/(5)·appendix_phase_separation.tex(이상 복제+태그) / results/: tools_check_structure.py·snapshot_v1019_baseline.json·snapshot_v1020_p0.json·V1020_STYLE_RUBRIC.md·V1020_CHANGE_LOG.md·V1020_EXECUTION_LEDGER.md·STEP_LOG_P0.md·본 RESULT / plans/: PLAN_P0_setup.md.

## Files Updated
(v1.0.20 신설 폴더 밖 없음.)

## Read Coverage
- 전문: ch1_sec02b_part0(1–329)·ch2_sec00_intro(1–68)·ch2_sec01_partition(1–144)·ch2_sec03_vibel(1–95)·ch1_preamble(1–73). 기획 세션 계승: ch1_sec02a(1–268)·ch1_sec04(1–196)·ch1_sec11(1–172)·마스터 tex 2본 전문.
- 미정독(각 담당 phase 에서): 나머지 절 파일.

## Execution Evidence
- 빌드: "Output written on graphite_ica_ch1_v1.0.20.pdf (62 pages)." / ch2 "(25 pages)." / appendix "(8 pages)." — LaTeX Error·Undefined 카운트 0.
- 회귀: `test_regression_v1019.py` → 전 배열 max_abs_diff ≤ 4.33e-15(골든은 원 캡처 머신 bit-exact 기준).
- 구조: v1.0.19 Ch1 라벨 219·중복 0·cite/bib 정합·자산 336 유니크 / Ch2 라벨 69·정합·자산 앵커 21태그. 복제 스냅샷 4축 동일(True).

## Validation
- Gate "복제 diff = 태그만": PASS(스냅샷 labels/eqblocks/asset/bibitems 동일 + grep 잔존 검사).
- Gate "빌드 경로 판정": PASS — **빌드 게이트 이 환경에서 유효**(폴백 불요). D2Coding 은 npm 확보(GitHub 프록시 차단 우회).
- Gate "rubric·가드·ledger 존재": PASS(각 파일 생성, rubric 총 33항).

## Gate
**PASS** (PASS_P0_SETUP)

## Confirmed Non-Changes
본문 내용·수식·라벨 무변경(스냅샷 실증). 코드·FITTING_GUIDE·골든 미복제(P8 소관). Codex/ 미접촉.

## Open Issues / Decision Queue
- 회귀 bit-exact 은 이 환경에서 판정 불가(플랫폼 잡음) → 코드 검증 = 소스 diff + 허용오차(P8).
- P6 통일 후보 4건 rubric §G 에 기록(부록 번호 방식·bib 헤더 수·제목 "(재작성)" 꼬리·MSMR 키 명명).

## Next
P1(서지 원장) 착수 — Step 11 부터.
