# audit_checklist — Phase 1.1 Step 1 OUT-INV 검수 sub 지침 (iter_1 · 2026-09-03)

> master(Fable 5.1) → 검수 sub(Fable 5.1). 검수 대상 = 작업 sub 가 만든 3본. 출력 = `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/audit_log.md`(신규 1본만). 등급 = 통상 산출물(등록부·인벤토리): 검수 sub ≥1R + 연속 2R 확정결함 0 수렴(마스터 플랜 Interfaces 검수 강도 · DR-23).

## 0. 5항목 고지

1. **역할** — 너는 v1.0.27 arc · Phase 1.1 · Step 1 의 **검수 sub** 다. 작업 sub 산출물의 품질·정합(수치 재계산·존재 대조·논리) + 사양·의도 대조(마스터 플랜 Phase 1.1 Step 1 · 게이트 1.1 · brief 요구)를 함께 검수한다. **refute mandate** — 산출물이 맞다고 전제하지 말고 틀린 곳을 찾는 것이 임무다. **최약점 1곳 필수 지목 · 빈 통과 금지**(발견 0 이면 "무엇을 어떻게 재검증했는데도 0 이었는지" 방법·범위를 정량으로 적는다).
2. **분업 경계** — 생성 파일 = `iter_1/audit_log.md` 1본만. **그 밖의 모든 파일 무변경**(OUT-INV·TSV·work_log 포함 — 결함은 지적만, 수정은 master). **commit 권한 없음 · git 명령 금지(읽기 포함)**. **`D:\Projects\Project_Anode_Fit\Codex\` 무접근(읽기·목록 0회)** — 재측정 명령은 `D:\Projects\Project_Anode_Fit\Claude` 아래에서만.
3. **범위 밖 자의 금지** — 검수 밖 작업(새 문건·수정·표준 제안 실행) X. 제안은 audit_log 의 「제안」 란에만.
4. **허위 attribution 금지** — 발견 건마다 4-tier(확정 / 근거 미발견 / 추정 / 미검증) + 근거 path:line + 재현 명령·수치. 확정은 네가 실제로 재계산·재대조한 것만. "그럴 것 같다" 는 추정으로 표기.
5. **memory 맥락** — 정독: 검수 대상 3본은 전문 정독(OUT-INV 1,463행은 ≤~500행 청크로 나눠 전 영역 cover — 청크 경계를 audit_log 에 기록) · 근거 원천(마스터 tex·INDEX 등)은 검수에 필요한 절만 · 읽은 파일·행 범위를 audit_log Read Coverage 표에 전건 기록 · 질문 도구·팝업 X(불명은 "미검증" 표기) · 산출은 파일로.

## 1. 입력

| # | 파일 | 범위 |
|---|---|---|
| A-1 | `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md` | 전문(사양 = §2·§3·§4·§5) |
| A-2 | `Claude/plans/2026-09-02-v2-master-plan.md` | L303–316(Phase 1.1 Step 1 사양·게이트 1.1) · L191–207(§2.9 실측 표) · L595–620(Assumptions 12·22·23) |
| A-3 | `Claude/results/V1027_HISTORY_INVENTORY.md` | 전문(청크 분할) |
| A-4 | `…/iter_1/work_log.md` | 전문 |
| A-5 | `…/iter_1/inventory_raw.tsv` | 스크립트 대조용(전문 Read 불요 — 파싱) |
| A-6 | `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` · `ch2_lco_v1.0.24.tex` · `ch3_si_v1.0.24.tex` | 전문(`\input` 집합 독립 재추출) |
| A-7 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R1_*.md … R7_*.md` | 「Read Coverage」 절만(G6 독립 재대조) |
| A-8 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/go_1g_check_2026-09-03.txt` | 전문 |

## 2. 검수 렌즈(이번 라운드 = 4종: 구조 · 적대검산 · 완결성 · usable)

### 2.1 적대검산 — 독립 재측정(작업 sub 의 TSV 를 믿지 말고 네가 다시 잰다)
- R-a `Claude/plans/*.md` 파일 수·줄수 합계 재측정 → OUT-INV §3 "93/10,384" 대조. +1(1g 10,383) 의 원인 파일을 특정할 수 있으면 특정(마스터 플랜 줄수 = ? · 1g 시점 줄수는 go_1g_check 에 기록돼 있는가).
- R-b `HANDOVER*.md` 재측정(old/ 제외·포함) → "25/1,612 · 28/1,915".
- R-c `docs/**/PLAN_*.md` 재측정 → "15/645" · v1020 master 207.
- R-d `CLAUDE.md` 줄수 → "88"(brief 90 · R3 89 와 다름 — `(Get-Content).Count` 와 `wc -l`·마지막 개행 차이인지 판정).
- R-e 마스터 tex 3본 `\input` 집합 독립 추출(주석 제외) → §6 "마스터 3 + 포함 53 + 미포함 4(독립 1 + orphan 3)" 검증. 특히 **`ch1_preamble.tex`·`ch2_preamble.tex` 가 정말 어느 마스터에서도 `\input` 되지 않는지**, 그리고 마스터 tex 가 `common_preamble_v1024`·`ch1v22_partT_divider` 를 어떤 형태(`\input`·`\include`·`\subfile`·상대경로)로 부르는지 실물로 확인. 마스터 플랜 §2.2 는 "지원 4본 = 빌드 포함" 으로 적었으므로 여기가 **계획서 정정 후보**다 — 어느 쪽이 맞는지 근거 행을 인용.
- R-f OUT-INV §1 표의 path 전건 → 실물 존재(Test-Path) + 줄수 = 네 재측정 값 — 스크립트로 전건 대조(불일치 건수·목록).
- R-g hash 중복 "259 그룹": 네가 SHA256 을 다시 계산해 그룹 수·대표 그룹(HANDOVER_v24 ×4 · V1023=V1022 원장) 을 재확인. 고유본 지정 규칙("가장 이른 버전 폴더")이 전 그룹에 일관 적용됐는지 표본 ≥10 그룹.
- R-h untracked Claude 8 의 지위 근거 path:line 이 실물에 있는지 전건 열어 확인(`regsol_test/` 폐기 = `comp_v26_data/README.md`:28–31 등).
- R-i G6: R1~R7 Read Coverage 파일 집합을 네가 독립 추출해 OUT-INV ⊆ 판정을 재현(131 파일이 맞는지 · 누락·오기 후보).

### 2.2 구조·완결성
- 군 (i)~(xviii) 전건 표 존재 · 열 7개 고정 어휘 준수(문서 종류·버전 귀속·판독 정독) · 빈 셀 0 · 어휘 밖 값 0.
- 한 파일이 두 군에 걸친 경우의 계수 규칙(§2)이 명시·일관 적용됐는가(합계 611 vs 665 산식 검증).
- (xiv) Codex 13 행 = "무접근" 고정 · Codex 경로가 TSV·OUT-INV 어디에도 실물 측정치로 등장하지 않는가(등장 = 접근 위반 신호).
- §8 부재·미검독 명시가 정직한가(예: 조사 문서군 본문 미검독 표시).
- work_log Read Coverage 표 ↔ 실제 필요 정독(brief §1 I-1~I-8)이 전건 있는가 · 행 범위가 파일 실제 길이 안인가.

### 2.3 usable(다음 Step 2 정독 배정표가 이 표만으로 세워지는가)
- 계보 순 정렬에 필요한 버전 귀속이 전건 채워졌는가 · 판독 정독 열이 R# 로 채워져 참조 열로 바로 쓰이는가 · 고유본/사본 표시가 있어 정독 대상 집합을 기계적으로 뽑을 수 있는가.

### 2.4 사양·의도 대조
- 마스터 플랜 Step 1 (i)~(xvi) 각 항목의 요구(예: (iii) old/ 3 별도 표시·hash 사본 판정 · (xiii) reflect 계획서·ledger 실물 경로 · (xvi) 빌드 포함/미포함 열)가 하나도 빠지지 않았는가 — 항목별 O/X.
- 게이트 1.1 문면(L315) 항목별 O/X(Step 2 몫 "배정표 차집합 0" 은 N/A 표기).
- DQ 15건 각각: 정말 결정이 필요한가 / 작업 sub 가 스스로 닫을 수 있었던 것인가 / master 가 닫을 것인가 분류.

## 3. 출력 양식(`iter_1/audit_log.md`)

1. 헤더(라운드 1 · 렌즈 4종 · 청크 경계 표).
2. **발견 표** — ID(AUD-01…) · 심각도{확정결함 / 경미 / 제안} · 4-tier · 위치(파일:행) · 내용 · 재현 근거(명령·수치) · 수정 제안(한 줄).
3. **최약점 1곳**(필수).
4. 렌즈별 통과·미통과 요약 + §2.4 항목별 O/X 표.
5. 독립 재측정 수치 표(R-a~R-i 결과 그대로 — 작업 sub 값과 나란히).
6. Read Coverage 표(파일·행 범위·방식).
7. 판정: 확정결함 n건 → "재작업 필요 / master 직접 수정 가능 / 통과".

## 4. 금지
- 파일 수정 X(audit_log 신규 1본만) · git X · Codex X · 질문 X · "적절해 보임" 류 정성 통과 X(항상 재현 수치·행 인용).
