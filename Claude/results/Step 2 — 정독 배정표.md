# Step 2 — 정독 배정표(OUT-INV 740본 → 계보 순 · 등급 · 청크 · 배정 Step)

- **arc**: v1.0.27(마스터 플랜 `Claude/plans/2026-09-02-v2-master-plan.md` v5.9)
- **작업 챕터 / Phase**: 1 이력 통합 / **1.1 인벤토리·정독 배정**(Step 1–2)
- **cumulative step**: 2
- **상태**: 진행 중(2026-09-11) — 작업 sub(Sonnet 4.6 · A3 기계 산출 · 자체검수 1회) 디스패치 → master 기계 대조 → 게이트 1.1 → Phase 1.1 Result
- **모델·유닛**: master Fable 5.1 · 작업 sub **Sonnet 4.6**(계획서 v5.6 모델 경계 — 정렬·청크·집계 = 기계 산출) · 검수 sub 없음(헌법 A3 · master 가 같은 대조 스크립트로 확정)

## [Step 2 착수 — 세부 계획서 재독]

- 세부 계획서 = 마스터 플랜 Phase 1.1 절(v5.2 기준 L303–316 · 현행 +2). master 가 Step 2 정의(L312–313 · 게이트 = 배정표 집합 = OUT-INV 집합 차집합 0 · 청크 경계 명시 · 줄수 합계 = OUT-INV 합계 · 판독 참조 열 = R# 일치 · 정독 주체 빈 셀 0)와 DR-7(①군 전문 / ②군 토픽 한정)을 재독했다(2026-09-11 · 5-check 시 Read). 흑연 우선 재배열(v5.6)에 따라 LCO·Si 몫 Step 은 "이연" 표지.

## 수행

| # | 시각 | 주체 | 행위 | 산출 |
|---|---|---|---|---|
| 1 | 09-11 | master | Step 1 수렴(`100ffdb`) → brief `handoffs/v1027-phase-1.1-reading/brief.md`(Sonnet 기계 산출 · 740/111,160 · 이연 표지) 확정 → 본 Step 파일 stub → 작업 sub 디스패치 | brief · Step 2 stub |
| 2 | — | 작업 sub(Sonnet 4.6) | (진행 중) OUT-INV 전문 정독 → 배정표 A + 기계본 B + work_log C · 자체검수(§4 게이트 스크립트) | `V1027_READING_ASSIGNMENT.md` · `iter_1/reading_assignment.tsv` · `iter_1/work_log.md` |

## 근거·판단

- (완료 시 기재)

## 변경·생성 파일

- 생성: 본 Step 파일 · (완료 시) `Claude/results/V1027_READING_ASSIGNMENT.md` · `Claude/results/handoffs/v1027-phase-1.1-reading/iter_1/{reading_assignment.tsv, work_log.md}`.

## 게이트

- (완료 시 기재 — 차집합 0 · 청크 명시율 · 줄수 합계 111,160 · R# 전사 740/740 · 주체·등급 빈 셀 0)

## 다음

- 게이트 1.1 → `PHASE_1.1_V1027_INV_RESULT.md`+`.json` → `PHASE_1-7_V1027_EXECUTION_LEDGER.md` 생성 → commit·push → Phase 1.2 Step 3.
