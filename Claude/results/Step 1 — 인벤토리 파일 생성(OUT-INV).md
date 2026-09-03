# Step 1 — 인벤토리 파일 생성(OUT-INV)

- **arc**: v1.0.27(마스터 플랜 `Claude/plans/2026-09-02-v2-master-plan.md` v5.2 · 실행 기준 정본)
- **작업 챕터 / Phase**: 1 이력 통합 / **1.1 인벤토리·정독 배정**
- **cumulative step**: 1(본 arc 첫 Step — 2.7 좌표대로 1 부터 단조 누적)
- **상태**: 진행 중(2026-09-03) — 완료 시 아래 5항목을 채운다
- **모델·유닛**: master Fable 5.1 · 작업 sub Fable 5.1 · 검수 sub Fable 5.1 · 직렬(동시 산 서브 ≤1)

## [Phase 1.1 착수 — 마스터 플랜 재독]

- 2026-09-03, master 가 `Claude/plans/2026-09-02-v2-master-plan.md` **본문 전문(1–813행)** 을 Read 로 재독했다 — 8구간(1–108 · 109–216 · 217–324 · 325–432 · 433–540 · 541–648 · 649–756 · 757–813) 합쳐 전 영역 cover. 요약·기억으로 대체하지 않았다.
- 재독으로 고정한 Step 1 규칙(계획서 L303–316): 인벤토리 군 (i)~(xvi) 전건 = path + 줄수 + 버전 귀속 + 문서 종류 + 판독 정독 여부(R#) · 재현 가능 명령(`Get-ChildItem -Recurse` 줄수 · `Get-FileHash SHA256` 사본 판정 · 마스터 tex `\input` 차집합 orphan) · 증거 = 표 + 군별·전체 합계 + 명령 출력 첨부 + brief §3-C 건수·줄수 차이 파일 목록 + 판독 커버리지 대조(R# Read Coverage ⊆ OUT-INV) · untracked Claude 8 지위 / Codex 13 = 무접근 고정 기재(열람 0) · 유실 자산 원문 5본 등재(Assumptions 23).
- 게이트 1.1(L315): Test-Path True 100% · 줄수 빈 셀 0 · brief §3-C 차이 열거·정본 확정 · 배정표 차집합 0(Step 2) · 빌드 포함/미포함 60/60 · untracked Claude 8 지위 빈 셀 0 · Codex 13 무접근. 중단 조건 = 실물 부재는 "부재" 표기 후 진행(정지 아님).
- GO 직전 1g 실물 대조는 계획서 Correction History v5.2 행 + `handoffs/2026-09-02-v2-master-plan/wf/go_1g_check_2026-09-03.txt` 에 기록돼 있다(Assumptions 14 정정 1건 외 전건 참).

## 수행

- (진행 중) master: 핸드오프 brief `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md` 저장(5항목 고지 · 입력 I-1~I-8 · 산출물 A/B/C · 실측 명령 · OUT-INV 양식 §1~§9 · 게이트 자체점검 G1~G8 · 금지). 작업 sub 디스패치 예정 → 검수 sub cross-check → master 삼각검증·확정.

## 근거·판단

- (완료 시 기재)

## 변경·생성 파일

- 생성: `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md` · 본 Step 파일.
- (완료 시 추가: `Claude/results/V1027_HISTORY_INVENTORY.md` · `handoffs/v1027-phase-1.1-inventory/iter_1/{inventory_raw.tsv, work_log.md, audit_log.md}`)

## 게이트

- (완료 시 기재 — G1~G8 O/X + 검수 sub 발견 건·삼각검증 결과)

## 다음

- Step 2 — 정독 배정표(OUT-INV 전건 계보 순 정렬 · 청크 경계 · 정독 주체 열 · ①군 전문 / ②군 토픽 한정 · 판독 참조 열) → 게이트 1.1 → `PHASE_1.1_V1027_INV_RESULT.md`+`.json` → Ledger 행 → commit.
