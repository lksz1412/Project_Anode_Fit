# Step 2 — 정독 배정표(OUT-INV 740본 → 계보 순 · 등급 · 청크 · 배정 Step)

- **arc**: v1.0.27(마스터 플랜 `Claude/plans/2026-09-02-v2-master-plan.md` v5.9)
- **작업 챕터 / Phase**: 1 이력 통합 / **1.1 인벤토리·정독 배정**(Step 1–2)
- **cumulative step**: 2
- **상태**: **완료(2026-09-11)** — 작업 sub(Sonnet 4.6 · A3) 산출 → 자체검수 O → master 독립 기계 대조 전건 O → 게이트 1.1 성립
- **모델·유닛**: master Fable 5.1 · 작업 sub **Sonnet 4.6**(계획서 v5.6 모델 경계 — 정렬·청크·집계 = 기계 산출) · 검수 sub 없음(헌법 A3 · master 가 같은 대조 스크립트로 확정)

## [Step 2 착수 — 세부 계획서 재독]

- 세부 계획서 = 마스터 플랜 Phase 1.1 절(v5.2 기준 L303–316 · 현행 +2). master 가 Step 2 정의(L312–313 · 게이트 = 배정표 집합 = OUT-INV 집합 차집합 0 · 청크 경계 명시 · 줄수 합계 = OUT-INV 합계 · 판독 참조 열 = R# 일치 · 정독 주체 빈 셀 0)와 DR-7(①군 전문 / ②군 토픽 한정)을 재독했다(2026-09-11 · 5-check 시 Read). 흑연 우선 재배열(v5.6)에 따라 LCO·Si 몫 Step 은 "이연" 표지.

## 수행

| # | 시각 | 주체 | 행위 | 산출 |
|---|---|---|---|---|
| 1 | 09-11 | master | Step 1 수렴(`100ffdb`) → brief `handoffs/v1027-phase-1.1-reading/brief.md`(Sonnet 기계 산출 · 740/111,160 · 이연 표지) 확정 → 본 Step 파일 stub → 작업 sub 디스패치 | brief · Step 2 stub |
| 2 | 09-11 | 작업 sub(Sonnet 4.6) | OUT-INV 전문 정독 → 배정표 A(879줄 · 740행) + 기계본 B(741줄) + work_log C · 자체검수 §4 전건 O · DQ 0 · (xviii) hash 동일 54본은 (xvi) 60 에서 역산 합성 · 비표준 귀속 61 패턴 좌표 매핑 | `V1027_READING_ASSIGNMENT.md` · `iter_1/reading_assignment.tsv` · `iter_1/work_log.md` |
| 3 | 09-11 | master | 독립 기계 대조(스크립트 재실행): 차집합 A−S 0 · S−A 0 · 중복 0 · 줄수 일치 740/740 · 합계 111,160 · R# 전사 불일치 0(OUT-INV 행 보유 686본) · 청크 규칙 위반 0 · 좌표 어휘 밖 0(25종) · 빈 셀 0 · 등급 분포 ① 58 / ② 482 / 원문 tex 5 / 현행 tex 66 / 정독 X 129 · 배정 Step 분포 1.2 Step 3 303 · Step 4 175 · 1.3 Step 8 15 · Step 9 22 · 1.4 18 · 2.1 25 · 2.2 52 · 4.5 1 · (없음) 129 → **게이트 1.1 성립** | 본 이력 · Result |

## 근거·판단(master · 4-tier)

1. **게이트 1.1 전건 확정** — 위 수행 행 3 의 독립 재대조(TSV·OUT-INV §1 정규식 추출 → 배정표 TSV 양방향 대조). 작업 sub 자체검수 수치와 전건 일치.
2. **모델 경계 첫 적용(확정)** — Sonnet 4.6 기계 산출 + 자체검수 1회 + master 대조(헌법 A3 · 계획서 v5.6). 판정 열(등급·좌표)은 brief §3 규칙으로만 도출됐고 규칙 밖 행 0(DQ 0).
3. **추정 유지** — 버전 귀속 "(추정)" 행의 좌표는 추정 표지 그대로 정렬(Step 3·4 원천 정독에서 확정 — DQ-2). (xviii) 사본 54본은 OUT-INV 에 행이 없어 배정표에서 합성(등급 "현행 tex(2.x) · 사본" · 정독 경로 = v1.0.25.1) — brief §3.1 규칙.
4. **흑연 우선(v5.6)** — 배정 Step 열의 2.2 Step 19(9본) 등 LCO·Si 몫은 "이연" 표지(실행 시점만 뒤).

## 변경·생성 파일

- 생성: 본 Step 파일 · `Claude/results/V1027_READING_ASSIGNMENT.md`(879줄) · `Claude/results/handoffs/v1027-phase-1.1-reading/iter_1/{reading_assignment.tsv, work_log.md}` · Phase 1.1 Result md+json · Ledger `PHASE_1-7_V1027_EXECUTION_LEDGER.md`(신설).
- 갱신: `Claude/docs/HANDOVER_v1.0.27.md`.

## 게이트

| 게이트(Step 2 · 마스터 플랜 게이트 1.1) | 판정 | 근거 |
|---|---|---|
| 배정표 집합 = OUT-INV 집합(차집합 0) | O | A−S 0 · S−A 0 · 740/740 |
| 각 파일 청크 경계(행) 명시 | O | 정독 대상 611행 전건 · 위반 0 |
| 총 줄수 = OUT-INV 합계 | O | 111,160 |
| 판독 참조 열 = R# 일치 | O | 불일치 0/686 |
| 정독 주체 빈 셀 0 | O | 740/740 |

## 다음

- (완료) Phase 1.1 Result md+json · Ledger 신설 · commit·push → **Phase 1.2 Step 3**(RB→v1.0.19 보강 정독 · 배정표 1.2 Step 3 303본 — 착수 시 마스터 플랜 재독 + 세부 계획서 = Phase 1.2 절).
