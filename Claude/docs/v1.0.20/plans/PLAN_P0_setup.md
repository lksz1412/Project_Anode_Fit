# Phase P0 세부 계획서 — 준비: 골격 복제·환경 구축·rubric·변경 통제 가드 (Steps 1–10)

## Summary
v1.0.20 작업 기반 구축: v1.0.19 문건 복제(diff 기준선), 빌드/검증 경로 확정(TeX·pip 설치 시도 + 폴백), 구조 검증 스크립트, 스타일 rubric(통계역학 파트 기준), 변경 통제 가드(CHANGE_LOG/ERRATA), ledger 초기화. 마스터 = `2026-07-16-v1020-master-plan.md`(v2, GO 반영).

## Current Ground Truth
- v1.0.19 완결판 = `docs/v1.0.19/`(Ch1 24절 조립·Ch2 15절·appendix·figs 5). 킥오프 조사 ①② 디스크 보존 완료.
- 환경: xelatex·numpy 부재(실측), 웹 가동, 브랜치 `claude/anode-fit-v1-0-20-cxshf9`.
- 미정독(이번 phase 에서 rubric 원천으로 정독할 것): ch1_sec02b_part0.tex(329줄), ch2_sec00_intro(68), ch2_sec01_partition(144), ch2_sec03_vibel(95). (sec02a·sec04·sec11 은 기획 세션에서 전문 정독 완료.)

## Phase Range
본 문서 = P0 단독(Steps 1–10). 마스터 §4 참조.

## Non-goals
본문 내용 편집 X(복제·버전 태그만). 코드·가이드 복제 X(P8). Codex/ 접근 X.

## Implementation Changes
`docs/v1.0.20/`: 마스터 tex 2본(이름 v1.0.20)·`_sections/` 전체·`figs/` 전체·appendix 복제+버전 태그. 신규: `results/tools_check_structure.py`·`results/V1020_STYLE_RUBRIC.md`·`results/V1020_CHANGE_LOG.md`·`results/V1020_EXECUTION_LEDGER.md`·`results/STEP_LOG_P0.md`·`results/RESULT_P0_setup.md`·기준선 구조 리포트.

## Phase P0 Steps
| Step | 내용 | 산출/Gate |
|---|---|---|
| 1 | 본 세부 계획서 저장 | 본 파일 |
| 2 | v1.0.19→v1.0.20 복제 + 버전 문자열 갱신(마스터 tex date·헤더, preamble pdftitle 류, appendix 승계 각주) — 내용 무변경 | `git diff --stat` = 복제+태그만 |
| 3 | TeX Live(xelatex·kotex) 설치 시도 → 성공 시 3본 기준선 빌드(페이지수 v1.0.19 대조) / 실패 시 폴백 선언 | 빌드 로그 또는 폴백 기록 |
| 4 | pip numpy/scipy 설치 → `test_regression_v1019.py` 실행(골든 13/13) / 실패 시 코드 검증 = diff 대체 선언 | 실행 로그 |
| 5 | 구조 검증 스크립트 작성·기준선 실행(라벨 중복·미해소 ref/cite·환경 짝·boxed/라벨/수치 스냅샷·자산 앵커 수) | `tools_check_structure.py` + 기준선 리포트 |
| 6 | rubric 원천 4파일 전문 정독(Read Coverage 기록) | STEP_LOG 기재 |
| 7 | `V1020_STYLE_RUBRIC.md` 작성(어조·용어·기호·문단형식·박스 사용·D7/D8 양식 — 각 부문 ≥10항) | rubric 파일 |
| 8 | `V1020_CHANGE_LOG.md` 초기화(보강 등재부 + ERRATA 부 + 코드 영향 컬럼) | 파일 |
| 9 | `V1020_EXECUTION_LEDGER.md` 초기화(12컬럼·P0 행) + RESULT_P0 작성 | ledger·result |
| 10 | P0 커밋+푸시 | 커밋 해시 |

## Implementation Interfaces
- 구조 스크립트 출력 = `structure_report_<tag>.txt`(중복 라벨/미해소 참조/짝 오류/자산 앵커 수) + `snapshot_<tag>.json`(boxed 블록 해시·eq 라벨 집합·표 수치) — P2 이후 매 phase `--diff v1019_baseline` 로 변경 통제 gate.
- CHANGE_LOG 행: `| ID | 종류(보강/ERRATA) | 위치(파일:라벨) | 구판 요지 | 신판 요지 | 근거 | 코드 영향(무/유-내용) | phase |`

## Test Plan
Step 2 gate = git diff 검사(버전 문자열 외 변경 0). Step 3/4 = 실행 로그 원문. Step 5 = v1.0.20 사본에 대한 기준선 리포트가 v1.0.19 와 동일(복제 무결 교차 확인).

## Assumptions
TeX 설치 실패 시에도 P1~P7 진행 가능(구조 검증 대체) — 최종 PDF 는 P8/로컬 이월.

## Correction History
(없음 — 초판)
