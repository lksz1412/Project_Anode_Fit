# review_master — master 최종 통합 기록 (v3 → v4 · 2026-09-03)

> 작성 = master(Fable 5.1). 유닛 = master + 작업 sub(초안 v1) → ultracode 워크플로(판독 8 · 통합 1 · 감사 3 · 수정 1 · 비평 1, run `wf_d5f03d08-c26`, 세션 한도 1회 중단 후 저널 확인·무수정 재개) → master 삼각검증·최종 반영. 최종본 = `Claude/plans/2026-09-02-v2-master-plan.md`(v4).

## 1. master 정독(전문)

| 파일 | 행 | 방식 |
|---|---|---|
| `wf/plan_draft_v3.md` | 1–860(8 페이지 합쳐 전 영역) | Read |
| `wf/critic.md` | 1–208 | Read |
| `wf/fix_change_log.md` | 1–132 | Read |
| `wf/audit_spec.md` | 1–161 | Read |
| `wf/audit_format.md` | 1–83 | Read |
| `wf/audit_logic.md` | 1–89 | Read |
| 워크플로 결과 `tasks/w8xa5it6a.output` | 1–405(결과 JSON; 406~ 는 progress 메타) | Read |
| 저널 `journal.jsonl` | 26 entries(상태만) | 스크립트 |

안 읽은 것: 판독 R1~R7 본문(통합·감사·비평이 전문 정독한 것을 근거로 채택; master 는 R 파일의 요지·key_findings·coverage_note 와 v3 의 인용만 봤다 — 실물 대조는 Assumptions 19 의 GO 전 표본 대조 16건 + 1.1~2.5). `iter_1/plan_draft.md`(v1, 세션 중 sub 반환 요약만).

## 2. 실측(읽기 전용 · 2026-09-02~03)

| 항목 | 결과 | 비평·판독 주장과의 관계 |
|---|---|---|
| `Claude/old/_archive/graphite_ica_ch1_{Fable_v2,Fable_v3,Opus_v4,Opus_v5,Opus_v6}.tex` | 5본 존재(183,693 / 205,225 / 218,389 / 153,592 / 156,166 B) | critic #5 확정 |
| `Claude/docs/v1.0.26A-regsol/`·`v1.0.26B-gallery/` | 존재(README.md·figures/·params/) | R2 확정 · brief §4.3 "실행 차단 미완" = stale(master 오류) |
| plans | 92 파일 / 9,567줄(날짜 계획서 89 + INDEX + MASTER_ROADMAP 2) | brief 90 · v1 sub 91/9,503 — 집계 기준 차이 |
| HANDOVER | old/ 제외 25 / 1,612줄 · old/ 포함 28 | brief "28(old/ 제외)" = old/ 포함 수치 오기(SPEC-06 확정) |
| `docs/**/PLAN_*.md` | 15 | v1 sub 16 = v1020 master 포함 |
| SymPy / Python | 1.14.0 / 3.12.10, 패키지 import OK | critic #9 확정 · T-12 새 의존성 정지 조건 해소 |
| xelatex | 실행파일 존재 | Assumptions 1 |
| 신규 예정 파일·`Step *` | 전건 부재 / 0건 | Assumptions 22 |
| git 위상(2026-09-02) | origin/main = main = 4069cb3 · v1.0.25.1/v1.0.25-surgical/v1.0.24.1 는 main 조상 · PDF 102/30/22 | Assumptions 8·15 |

## 3. 삼각검증 판정

- 감사 55건(CRIT 0·HIGH 6) → fixer 전건 반영(rejected 0·부분 4). 부분 4 = SPEC-04(8·13 재계수 — 세션 git 스냅샷과 일치, 타당) · LOGIC-02(접두 규약 — **불충분**, 비평 #1 로 잔존) · LOGIC-10(v1 참조 헤더 정의 — 타당) · FORMAT-01(Result 편입 Step 불변 — 타당, DQ-I14 master 승인).
- 비평 14건 = HIGH 1·MED 4·LOW 9 **전건 확정·전건 반영**(v4 패치 — Correction History v4 행).
- DQ-I2(Step 40→50, 1h 확장 방향) 승인 · DQ-I14 승인 · DQ-I15(유실 원문 정독 범위 확장) 승인 · DQ-I16 승인 출처 = 사용자 "울트라 코드로 다시 시작해"(§1-병렬 ③) 기재 · DQ-I13(v1 참조 유지) 수용 · DQ-I3/I4/I5(원천 간 상충) = 2.1/2.5 실물 재계수로 이관 유지.
- 부록 A~C 는 `wf/plan_v3_appendix_ABC.md` 로 분리(FORMAT-12).

## 4. 최종본 v4 변경 요약(v3 대비)

헤더(최종본 표기·저장 위치) · Summary/3.1/3.2/4.1 의 R6 `T-1`/`T-2` 접두 · 이름공간 표 행 추가 · 4.x 회수 게이트 기준 좌표 · 4.6 게이트 문면 · 1.3 Step 8/게이트·2.5 Step 27(F-01·R1 L-14/L-15) · 1.4 Step 11 (i) 경로 · 2.1 Step 14(orphan 라벨) · 2.2 Step 19(산문 비율) · 4.0(동기 층) · 6.1(샘플 이미지 QA) · 1.5/3.7 중단 조건 · T-20 연습문제 · §2.1/§2.9 실측 갱신 · Assumptions 1/5/7/8/12/15/19/23 · DR-6 선택지·DR-16 부기 · Implementation Interfaces 병렬 승인 출처 · Correction History v4 · 말미 안내. 골격·Phase ID·Step 1–50·DR-1~23 번호·11-section 순서 불변.

## 5. 미해결(사용자)

DR-1~DR-23 결정 대기 · GO 범위(DR-9) · DG-A/B/C 는 3.7 정지에서.
