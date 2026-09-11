# brief — v1.0.27 작업 챕터 1 · Phase 1.1 · Step 2 「정독 배정표」

> master(Fable 5.1) → 작업 sub(**Sonnet 4.6** — 기계 산출: 정렬·청크·집계 · 계획서 v5.6 모델 경계 · 자체검수 1회 + master 확인; 판정 열은 OUT-INV 값 전사만). 2026-09-11. 통제 문서 = `Claude/plans/2026-09-02-v2-master-plan.md`(v5.7) Phase 1.1 Step 2(v5.2 기준 L312–313 · 현행 +2) + 게이트 1.1 + DR-7. 입력 정본 = Step 1 산출 `Claude/results/V1027_HISTORY_INVENTORY.md`(OUT-INV iter_6 · 검수 R6 수렴본 · 등재 **740 파일·111,160줄**). 유닛 = master + 작업 sub(A3) · 검수 sub 없음(헌법 A3 규칙 — 자체검수 + master 기계 대조).

## 0. 5항목 고지

1. **역할** — 너는 Phase 1.1 Step 2 의 **작업 sub(Sonnet 4.6 · 기계 산출 등급)** 다. 책임 = §2 산출물 A·B·C 생성 + 자체검수 1회(§4 게이트 전항 스크립트 대조). 확정·commit 은 master(기계 대조 재실행).
2. **분업 경계** — 신규 파일 3본만 생성. **OUT-INV 를 포함한 모든 기존 파일 무변경**(OUT-INV 는 읽기 전용 입력 — 오류를 발견하면 work_log DQ 에 적고 표에는 "OUT-INV 표기 오류 후보" 비고). **commit 권한 없음 · git 명령 금지(읽기 포함)** · **`D:\Projects\Project_Anode_Fit\Codex\` 무접근(읽기·목록 0회)**.
3. **범위 밖 자의 금지** — 새 문건·계획서 수정·memory 생성 X. 결정 필요 항목은 DQ 목록만.
4. **허위 attribution 금지** — 4-tier(확정/근거 미발견/추정/미검증) + path:line. 너의 판단은 "[sub 판단]".
5. **memory 맥락** — 정독: OUT-INV 는 head→tail **전문 정독**(≤~250행 창으로 전 영역 cover · 창 경계를 work_log Read Coverage 에 기록) · 마스터 플랜은 지정 범위만 · 그 밖의 파일은 **열지 않는다**(배정표는 OUT-INV 메타데이터만으로 세운다 — 원천 본문 정독은 Step 3 이후의 일; 단 절 경계를 잡기 위한 Grep 은 §4.3 허용 범위에서만) · 질문 도구·팝업 X(기본값 + DQ) · 산출은 파일로.

## 1. 입력

| # | 파일 | 범위 |
|---|---|---|
| I-1 | `Claude/plans/2026-09-02-v2-master-plan.md` | L113–122(§2.3 계보 — 정렬 순서의 정본) · L191–207(§2.9) · L303–316(Phase 1.1 — Step 2 정의·게이트) · L317–357(Phase 1.2~1.5 — 배정 Step 의 정독 범위) · L359–380(2.1·2.2 — tex 정독 배정) · L706–710(DR-7) |
| I-2 | `Claude/results/V1027_HISTORY_INVENTORY.md` | 전문(1,757행 · iter_6) — §0 규칙·행 번호 기준 · §1 군별 표(각 행의 path·줄수·귀속·종류·R#·비고 = 배정표 원자료 — (i)~(xix) + (i-b)·(iv-b)·(iv-c)·(vii-b)·(vii-c)·(viii-b)·(viii-c)·(ix-b)·(xvii-b)·(xvii-c)) · §2 합계 · §4 hash 고유본/사본 · §6 tex · §8.3 미등재 · §10.1~10.7 처분(DQ-16 후보 풀 정의 · 정책 (b) 정본) |
| I-3 | `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/inventory_raw.tsv` | 스크립트 대조용(줄수·hash) — Read 불요, 파싱만 |

## 2. 산출물(신규 3본)

- **A. 정독 배정표** = `Claude/results/V1027_READING_ASSIGNMENT.md` — §4 양식.
- **B. 기계본** = `Claude/results/handoffs/v1027-phase-1.1-reading/iter_1/reading_assignment.tsv` — A 의 행 전건(열 = A 와 동일 · 탭 구분 · 헤더 1행). 검수 sub 가 차집합·합계를 기계 대조한다.
- **C. work_log** = `Claude/results/handoffs/v1027-phase-1.1-reading/iter_1/work_log.md` — 5항목 + Read Coverage 표 + DQ.

## 3. 배정 규칙(master 확정 — 그대로 적용)

### 3.1 정독 등급(5값 · 빈 셀 0 — 값은 OUT-INV 의 군·종류·비고에서 **기계 규칙으로만** 도출 · 판단 X · 규칙 밖 행은 DQ)

| 등급 | 정의 | 해당(OUT-INV 군·조건) |
|---|---|---|
| **①전문** | head→tail 전문 정독 + 검수 sub 근거 행 대조 | 마스터플랜급 계획서(문서 종류 = 마스터플랜 — (i)·(i-b)·(ii) 의 v1020 master; glob 오매치는 제외) · 인계 chain 전건 (iii) 고유본 · Fable 감사 8 (iv) · CLOSING (v) · INDEX 3본(`docs/INDEX.md`·`plans/INDEX.md`·`INDEX_v25.md`; 그 밖의 `INDEX_v*` 는 ②) · 서지 원장 4 (xii)(V1023 은 사본→"사본") · v1.0.26 실물 3본 + `build.log` (xi) · dossier (x) · `jcp_extract.txt`(①이되 배정 Step = 4.5/S-2 — 챕터 1 에서는 존재 확인만; 표기 "①(4.5 배정)") |
| **②토픽 한정** | 구조 추출(Phase 표·게이트·결정·Correction History·헤더) → 등록부 행의 근거 절만 원천에서 정독 → 검수 대조 · Read Coverage 에 행 범위 | 세부 계획서(plans 잔여·PLAN_*·old/plans·old/v2/plans) · ledger (vii)·(vii-b)·(vii-c 규약 기록) · Result (viii)·(viii-b)·(viii-c) · 조사 문서군 (ix)·(ix-b — `CODE_w_check` 포함) · 감사 성격 (iv-b)·(iv-c — `KNOWN_DEFECTS` 포함) · 구트랙 기준 원문·계보 원문 tex (xvii-b)·(xvii-c) · `INDEX_v*` 잔여 (vi) |
| **원문 tex(절 한정)** | 1.4 Step 11 (i) 의 해당 절만 head→tail(절 범위는 Step 11 착수 시 Grep 으로 확정 — 배정표엔 "절 범위 미정 · Step 11 확정" 과 목표 절 이름만) | (xvii) 유실 원문 5본: Fable v2 = Eyring 근본식 배열 · Opus v5/v6 = §1.15 S0~S5·16-울타리 · Fable v3/Opus v4/Opus v5 = §1.10 KWW/장벽분포 · Opus v4 = §1.18 적층 준안정·athermal |
| **현행 tex(2.x)** | 챕터 1 정독 대상 아님 — 2.1 Step 14(마스터 3 + 지원·orphan 4 = 361줄) · 2.2 Step 17~19(53본 8,853줄 — 청크 ≤~500) | (xvi) 60 · (xviii) v1.0.25 = hash 동일 54 "사본" + diff 6 "2.1 Step 15 diff hunk" |
| **정독 X** | 사본(고유본이 따로 등재) · 시드(판독 산출 (xv)) · 통제(본 arc 계획서) · 코드/데이터/로그(`.py`·`.json`·`.log` — (xi) 스크립트 등) | OUT-INV 비고의 "사본(고유본 = …)" 행 전건 · (xv) 24 · (i) 행 90 · (xi) `.py`/`.json`/`.log`/`skew_log.txt` |

- 사본 판정은 OUT-INV 비고의 `사본(고유본 = …)` 표기를 그대로 따른다(§4 규칙 · 현행 tex 60 은 예외적으로 정독 경로 = `v1.0.25.1` — OUT-INV §4 머리·DQ-4 처분). 사본 행도 배정표에 **행으로 존재**해야 한다(차집합 0 게이트) — 등급 "정독 X(사본 → 고유본 path)".

### 3.2 정렬(계보 순 — 마스터 플랜 §2.3 L115 순서를 좌표로)

좌표 열 값(고정 어휘 · 이 순서로 정렬): `00 구트랙 RB` → `01 6-07 Ch2~5 야간` → `02 6-10 TBR` → `03 Fable v2` → `04 v3` → `05 Opus v4` → `06 v5` → `07 v6` → `08 v7` → `09 v8` → `10 v9` → `11 v10` → `12 Ch2 v3~v5`(Ch2 트랙) → `13 v1.0.10` → `14 v1.0.11` → `15 v1.0.12` → `16 v1.0.13` → `17 v1.0.14` → `18 v1.0.15` → `19 v1.0.16` → `20 v1.0.17` → `21 v1.0.18.1/.2` → `22 v1.0.19` → `23 v1.0.20` → `24 v1.0.21` → `25 v1.0.22` → `26 v1.0.23` → `27 v1.0.24` → `28 v1.0.24.1` → `29 v1.0.25` → `30 v1.0.25.1` → `31 v1.0.26` → `90 횡단`(INDEX·Fable 감사·CLAUDE.md·jcp) → `95 시드(판독)` → `99 통제(본 arc)`. OUT-INV 버전 귀속 값을 이 좌표로 매핑한다(매핑표를 A §0 에 첨부 · "추정" 귀속은 좌표 뒤에 `(추정)` 유지 · 매핑 불능은 DQ). 같은 좌표 안에서는 문서 종류 순(마스터플랜 → 세부 계획서 → 인계 → 감사 → ledger → Result → 조사 → 원장 → 원문 tex → 기타) → path.

### 3.3 청크 경계

- 정독 등급 ①·②·현행 tex 행: 줄수 < 800 → 통째 1 청크 `1–N` · 줄수 ≥ 800 → ≤~500행 창(최대 ~700)으로 분할해 창 경계를 행 번호로 명시(예: `1–500 · 501–1000 · 1001–1352`). 절 경계에 맞추는 것은 Step 착수 시 담당이 조정 가능 — 배정표는 기계 분할 기준값.
- 원문 tex(절 한정)·정독 X 행: 청크 = `—` + 사유.
- 청크 수 합계·정독 대상 줄수 합계를 §5 요약에.

### 3.4 배정 Step(마스터 플랜 Phase 1.2~1.4 · 2.1·2.2 정의대로)

| 배정 Step | 대상 |
|---|---|
| 1.2 Step 3 | 좌표 00~12(구트랙~v10·Ch2 트랙)의 ①·② 전건 + 13~22(v1.0.10~v1.0.19) 중 인계·감사·계획서·ledger·Result · (xvii-b)·(xvii-c) 원문 tex · Fable 감사 02/03 · `research/broadening_w_design.md` |
| 1.2 Step 4 | 좌표 23~31(v1.0.20~v1.0.26) 전건 + 조사 문서군 (ix) 잔여 + `V1013_TERMS_POLICY`·`V1014_TONE_AUDIT`·`V1020_STYLE_RUBRIC`·comp_FR·comp_v23·comp_SM2 |
| 1.3 Step 8 | 규범군: CLOSING · `V1020_STYLE_RUBRIC` · `V1013_TERMS_POLICY` · `V1014_TONE_AUDIT` · `HANDOVER_v24/v25` · FITTING_GUIDE 8(vii-c 규약 기록) · `USER_FEEDBACK_v1024_READING` |
| 1.3 Step 9 | 결정군: v1021/v1022 master plan · `docs/v1.0.21/results/V1021_*`·`v1.0.22/results/*` · CHARTER 3 + `RB_AL_MASTER`(vii-b) · 서지 원장 4 · v1.0.26 실물 3 · `HANDOVER_regsol_investigation` |
| 1.4 Step 10~12 | R1 §5·R2 §4·R3 B 시드(xv) 참조 + 유실 원문 tex 5본(절 한정) + radius 판정문(ix-b) + `SM2_SURVEY`·`SURV_SYNTHESIS`·`IMPROVEMENT_DIRECTIONS`·`LIT_ADVANCE_SYNTHESIS`·`ROADMAP_future_physics` |
| 2.1 Step 14·15 | 현행 tex 마스터 3 + 지원·orphan 4 · v1.0.25 diff 6 · `INDEX_v25`·`MERGE_READINESS`·`V1025_*` 결과 문서 |
| 2.2 Step 17~19 | 현행 `_sections` 53본(청크 19 — 마스터 플랜 L372 기준 7/5/7) |
| 2.4~2.6 · 3.x · 4.5 | 서지 원장·comp_v24 데이터 문서·`jcp_extract`(4.5)·dossier(2.2/4.5) — 해당 Step 명 |
| (없음) | 정독 X 등급 |

한 파일이 둘 이상 Step 에 걸리면 첫 정독 Step 을 주 배정으로, 나머지를 "재참조" 열에.

### 3.5 정독 주체·검수 대조 방식(열 값 고정)

- 정독 주체 ∈ {작업 sub(직렬) / master(git 대조·통합 판단 항목 — 날짜 추정 행의 `git log --follow` 등) / (정독 X)}. 기본 = 작업 sub.
- 검수 대조 ∈ {①: 전문 정독 + 검수 sub 근거 행 전건 대조 / ②: 구조 추출 + 근거 절 정독 + 검수 sub 근거 행 대조 / 원문 tex: 절 범위 정독 + 검수 대조 / 2.x: 해당 Phase 규칙 / —}.
- 판독 참조 열 = OUT-INV `판독 정독(R#)` 열 **그대로 전사**(변경 금지 — 게이트 "판독 기정독 참조 열 = R# Read Coverage 와 일치").

### 3.6 정독 순서 규칙(A §0 에 명기)

- `results/comp_v24/` 원본 → `docs/v1.0.25.1/results/V1025_DATA_ADDENDUM.md`(충돌 시 addendum 우선 — `HANDOVER_v25.md`:150–152).
- 구트랙(좌표 00·old/) 파일은 **경로 병기 + 동명이물 경고**(구트랙 v2~v5 ≠ Fable v2~v5 · `old/v2/` = 구트랙 rebuild v2).
- hash 사본은 고유본 1본만 정독(사본 행에 고유본 path).

## 4. 양식(A `V1027_READING_ASSIGNMENT.md`)

- §0 머리: 목적 · 입력(OUT-INV 740/111,160 · iter_6 · 검수 R6 수렴본) · 등급 정의(§3.1 전사) · 좌표 매핑표(OUT-INV 귀속 값 → 좌표) · 정독 순서 규칙 · 청크 규칙.
- §1 배정표(740행 전건 · 계보 순): `#` · `좌표` · `path` · `줄수` · `군` · `문서 종류` · `정독 등급` · `정독 주체` · `청크 경계` · `배정 Step` · `재참조` · `판독 참조(R#)` · `검수 대조` · `비고`(사본→고유본 path · 추정 · 동명이물 · 절 이름 등).
- §2 Step 별 배정 집계: 각 배정 Step 의 파일 수·줄수·청크 수(①/② 분리).
- §3 등급별 집계: ①/②/원문 tex/현행 tex/정독 X 의 파일 수·줄수 · 정독 대상 합계(①+②+원문 tex 절 한정 미정 표시) — DR-7 비용 근거.
- §4 게이트 자체 점검: 배정표 집합 = OUT-INV 집합(차집합 0 — 스크립트로 양방향 대조 · 수치) · 청크 경계 명시율(정독 대상 행 100%) · 줄수 합계 = 111,160 · 판독 참조 열 = OUT-INV 전사 일치 740/740 · 정독 주체 빈 셀 0 · 등급 빈 셀 0 · **자체검수 1회**(A3): 위 대조 스크립트 출력을 work_log 에 첨부 — master 가 같은 스크립트로 재실행해 확정.
- §5 부록 — **DQ-16 후보 풀**(파일 단위 목록·줄수: OUT-INV §10.4 DQ-16 의 계열 패턴을 TSV 에 적용 — `results/process/V1014_REVIEW_R*`·`V1013_REVIEW_R*`·`V1013_CODE_MAP_ADDENDUM_R10`·`V1012_P43_review_*`·`V1012_P42b_fixer_note`·`V1010_P1~P5_review1`·`V1010_HANDOVER_INSPECT_*`·`V1010_LCO_STYLE_REPORT`·`V1015_P2_PHYSICS_REVIEW`·`V1019_FINAL_REVIEW_UNION` — 등재 X · "1.2 Step 3 토픽 한정 열람 후보") + **radius·CH2_v3 조사 카드**(계수) — 실측 건수·줄수 기재.
- §6 DQ.

## 5. 금지·주의

- OUT-INV 밖 파일 본문을 열지 않는다(원천 정독은 Step 3 이후). 예외 = 없음(절 경계 확정은 Step 11 몫).
- 기존 파일 수정 X · git X · Codex X · 추정 수치 X(줄수는 OUT-INV/TSV 값만).
- 반환 = 생성 3본 경로 + §4 게이트 O/X 요약 + DQ 건수.
- **흑연 우선 순서(계획서 v5.6)**: 배정 Step 열의 LCO·Si 몫(2.2 Step 19 · 2.3 Step 22 · 3.3 Step 43 · 4.6~4.8)은 "이연(Ch1 PDF 후)" 표지를 붙인다 — 배정은 그대로, 실행 시점만 뒤.
