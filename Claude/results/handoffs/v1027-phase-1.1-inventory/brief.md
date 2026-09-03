# brief — v1.0.27 작업 챕터 1 · Phase 1.1 · Step 1 「인벤토리 파일 생성(OUT-INV)」

> master(Fable 5.1) → 작업 sub(Fable 5.1). 2026-09-03. 통제 문서 = `Claude/plans/2026-09-02-v2-master-plan.md`(v5.2, 실행 기준 정본) Phase 1.1 절. 유닛 = master + 작업 sub + 검수 sub, **직렬**(동시 산 서브 ≤1). 본 brief 범위 = Step 1 만(Step 2 정독 배정표는 별도 지시).

## 0. 5항목 고지

1. **역할** — 너는 v1.0.27 arc · Phase 1.1 · Step 1 의 **작업 sub** 다. 3-세션 모델(master + 작업 + 검수) 안에서 본 sub 의 책임은 아래 §2 산출물 A·B·C 를 만드는 것뿐이다. 검수는 별도 검수 sub 가 뒤이어 하고, 통합·확정·commit 은 master 가 한다.
2. **분업 경계** — 담당 범위 = §2 의 신규 파일 3본 생성. **무변경 영역 = 그 밖의 모든 기존 파일**(특히 `Claude/docs/v1.0.24*/`·`v1.0.25/`·`v1.0.25.1/`·`v1.0.26A-regsol/`·`v1.0.26B-gallery/`·`Claude/plans/*`·기존 `Claude/results/*`). 기존 파일의 수정·삭제·이동·이름변경 금지. **commit 권한 없음 · git 명령 실행 금지(읽기 명령 포함 — untracked 목록은 §3.5 에 제공)**. **`Codex/` 무접근 — 읽기·디렉터리 목록 조회 포함 0회**(인벤토리 명령은 반드시 `D:\Projects\Project_Anode_Fit\Claude` 아래에서만 실행; 루트의 `CLAUDE.md` 1본만 별도 경로로 측정).
3. **범위 밖 자의 작업 금지** — 새 문건·새 표준·계획서 수정·memory 생성·brief 미명시 파일 생성을 하지 않는다. 필요하다고 판단되면 work_log 의 Decision Queue 에 목록만 적고 진행하지 않는다.
4. **허위 attribution 금지** — 보고·work_log 의 모든 판정은 4-tier(확정 / 근거 미발견 / 추정 / 미검증)로 표기하고, 확정에는 path+line 을 붙인다. 너의 판단은 "[sub 판단]" 으로 표시한다. 마스터 플랜·판독 산출(R1~R7)이 적어 둔 수치를 그대로 옮길 때는 출처를 병기하고, 실측과 다르면 실측을 정본으로 적고 차이를 기록한다.
5. **memory 맥락 주입**(서브는 native 메모리를 상속하지 않는다) — (a) 전문 정독: 정독 대상으로 지정된 파일은 head→tail 전 영역을 읽는다(부분 Read 는 합쳐서 전 영역 cover). 단 R1~R7 은 「Read Coverage」 절만 읽는 **토픽 한정 정독**이 허용된다(사용자 확정 DR-7). 읽은 파일·행 범위를 work_log 「Read Coverage」 표에 남긴다 — 표에 없으면 읽지 않은 것으로 간주된다. (b) 추정 금지: 측정하지 않은 값은 "미측정", 읽지 않은 것은 "미검독" 으로 적는다. (c) 흐름 보호: 사용자에게 질문하지 않는다(팝업·질문 도구 X). 결정이 필요하면 합리적 기본값으로 진행하고 DQ 에 기록한다. (d) 산출은 전부 파일로 남긴다 — 반환 메시지는 파일 경로 + 한 단락 요약이면 된다.

## 1. 입력(정독 대상 · 행 범위)

| # | 파일 | 범위 | 방식 |
|---|---|---|---|
| I-1 | `Claude/plans/2026-09-02-v2-master-plan.md` | L39–68(§2.0 원천 코드표) · L160–207(§2.8 구조 맵·§2.9 인벤토리 실측·판독 커버리지) · L224–226(Phase Range 1.1 행) · **L303–316(Phase 1.1 전문 — Step 1 (i)~(xvi) 정의·명령·증거·게이트)** · L593–620(Assumptions, 특히 12·14·22·23) | 지정 범위 전문 |
| I-2 | `Claude/docs/INDEX.md` | 전문(197줄) | 전문 |
| I-3 | `Claude/plans/INDEX.md` | 전문(스테일 — 인벤토리 대조용) | 전문 |
| I-4 | `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | 전문 | 전문 |
| I-5 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R1_version_register_v3_to_v1019.md` · `R2_version_register_v1020_to_v1026.md` · `R3_binding_decisions_and_lost_directions.md` · `R4a_diagnosis_scope_ch1_partT.md` · `R4b_diagnosis_scope_ch2_ch3_appendix.md` · `R5_theory_candidates_thermo_statmech.md` · `R6_theory_candidates_kinetics_hys_heat.md` · `R7_reference_master_map.md` | 각 파일의 「Read Coverage」 절(Grep 으로 위치 확인 → 그 절 전문) | 토픽 한정 |
| I-6 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/go_1g_check_2026-09-03.txt` | 전문 | 전문(GO 직전 1g 실측 — 네 실측과 대조) |
| I-7 | `Claude/results/comp_v26_data/README.md` | L20–35(untracked `regsol_test/` 폐기 판정 근거) | 토픽 한정 |
| I-8 | `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` · `ch2_lco_v1.0.24.tex` · `ch3_si_v1.0.24.tex` | 전문(마스터 tex 3본 — `\input` 목록 실측용; 짧다) | 전문 |

## 2. 산출물(전부 신규 파일)

- **A. OUT-INV** = `Claude/results/V1027_HISTORY_INVENTORY.md` — 양식은 §4.
- **B. 실측 원본** = `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/inventory_raw.tsv` — §3 명령의 출력 그대로(가공 X). 열 = 절대경로 · 줄수 · SHA256 · 바이트.
- **C. work_log** = `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/work_log.md` — 5항목(수행 / 근거·판단 / 생성 파일 / 게이트 자체점검 O·X / 다음) + **Read Coverage 표**(파일·행 범위·방식) + **Decision Queue**.

## 3. 실측 명령(재현 가능 · 읽기 전용)

### 3.1 전수 측정(줄수·hash·바이트)

PowerShell 7 에서, 작업 디렉터리를 `D:\Projects\Project_Anode_Fit\Claude` 로 두고 실행한다(Codex 폴더에 진입하지 않기 위해 루트가 아니라 `Claude` 에서 시작한다):

```powershell
$env:PYTHONIOENCODING='utf-8'
$root = 'D:\Projects\Project_Anode_Fit\Claude'
$out  = 'D:\Projects\Project_Anode_Fit\Claude\results\handoffs\v1027-phase-1.1-inventory\iter_1\inventory_raw.tsv'
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
$files = Get-ChildItem -Path $root -Recurse -File -Include *.md,*.tex,*.txt,*.log,*.json,*.py
$files += Get-Item 'D:\Projects\Project_Anode_Fit\CLAUDE.md'
$files | ForEach-Object {
  $h = (Get-FileHash -Algorithm SHA256 -Path $_.FullName).Hash
  "$($_.FullName)`t$((Get-Content -Path $_.FullName).Count)`t$h`t$($_.Length)"
} | Out-File -FilePath $out -Encoding utf8
(Get-Content $out).Count
```

이 TSV 가 OUT-INV 모든 행의 **유일한 줄수·hash 출처**다. 표의 줄수는 이 TSV 에서 옮기고, TSV 에 없는 경로를 표에 적지 않는다(= Test-Path 100% 게이트의 조작적 정의). 줄수 정의 = `(Get-Content).Count`(마지막 개행 유무 무관 행 수). 파일이 하나도 없는 군은 "부재" 로 적는다(정지 사유 아님).

### 3.2 빌드 포함/미포함(orphan) 검사 — (xvi)

마스터 tex 3본(I-8)에서 `\input{...}` 인자 집합을 뽑고(주석 `%` 줄 제외), `Claude/docs/v1.0.25.1/_sections/*.tex` 파일 집합과 차집합을 낸다. 기대 = orphan 1(`ch1_appD_si.tex`) · 독립 부록 1(`appendix_phase_separation.tex`, `_sections` 밖·자체 `\documentclass`) · 지원 4본(`ch1v22_partT_divider`·`ch1_preamble`·`ch2_preamble`·`common_preamble_v1024`)은 `\input` 되는 빌드 포함 파일이다. 실측이 기대와 다르면 실측을 적고 차이를 기록한다. 60 tex 전건에 빌드 포함/미포함 열을 채운다(마스터 3 = "마스터", 독립 부록 = "미포함·독립", orphan = "미포함·orphan").

### 3.3 hash 중복 판정

TSV 의 SHA256 이 같은 파일 그룹을 전건 열거한다(예상: `HANDOVER_v24.md` 4곳 사본, `V1023_REFERENCE_LEDGER.md` = `V1022_…` 사본). 각 그룹에 **고유본 1본**(정독 대상)을 지정하고 나머지는 "사본" 으로 표시한다. 고유본 선택 규칙 = 가장 이른 버전 폴더의 것(계보상 원본) — 근거를 적는다.

### 3.4 CLAUDE.md 실측

`D:\Projects\Project_Anode_Fit\CLAUDE.md` 줄수(brief 기재 90 vs R3 실측 89 — 정본 확정).

### 3.5 git untracked 21건(세션 시작 스냅샷 — master 제공 · git 실행 금지)

Claude 측 8 = `Claude/docs/v1.0.17/figs/graph_suite_v1017.png` · `Claude/docs/v1.0.17/sample_test_v1017.png` · `Claude/docs/v1.0.18.1/figs/graph_suite_v1018_1.png` · `Claude/docs/v1.0.18.1/sample_test_v1018_1.png` · `Claude/docs/v1.0.18.2/figs/graph_suite_v1018_2.png` · `Claude/results/process/C3_graph_check/` · `Claude/results/process/C3_pdf_render/` · `Claude/results/regsol_test/`.
Codex 측 13 = `Codex/work/agent_reports/` · `audit_runtime/` · `literature/` · `local_remote_pdf_compare_v10182/` · `phase004/` · `phase005/` · `phase006/` · `phase007/` · `phase010_sources/` · `scripts/` · `source_archives/` · `source_snapshots/` · `tools/`.
→ Claude 8 은 지위{유효 / 폐기 / 추정} + 근거(path:line — `regsol_test/` 는 I-7; `C3_*`·`sample_test_*`·`graph_suite_*` 는 `Claude/docs/INDEX.md`·해당 버전 HANDOVER·`results/process/` 안 ledger 에서 참조를 Grep 해 판정; 참조 0 이면 "근거 미발견·추정"). 폴더 2건은 내부 파일 목록(이름·개수)만 적는다. png 는 열지 않는다(존재·크기만).
→ Codex 13 은 표 13행 전부 지위 = "Codex 소관 · 무접근(판정 안 함)" 으로 **고정 기재**하고 열람 0 을 명시한다.

## 4. OUT-INV 양식(`V1027_HISTORY_INVENTORY.md`)

머리: 목적(Phase 1.1 Step 1 · OUT-INV) · 실측 일시 · 실측 명령(§3.1 그대로) · 모집단 정의(파일 단위 · 줄수 정의 · 경로는 `Claude/` 상대) · 4-tier 규약.

**§1 군별 인벤토리 표** — 군 (i)~(xvi) + (xvii)·(xviii)(아래). 열 고정: `#` · `path`(`Claude/` 상대) · `줄수` · `버전 귀속` · `문서 종류` · `판독 정독(R#)` · `비고`. 어휘 고정 — 문서 종류 ∈ {마스터플랜 / 세부 계획서 / 인계 / 감사 / 클로징 / INDEX / ledger / Result / 조사 / 서지 원장 / 원문 tex / 시드(판독) / 통제(본 arc) / 기타} · 버전 귀속 ∈ {구트랙 RB / Fable v2~v10(세부) / v1.0.10 … v1.0.26 / 본 arc / 횡단} · 판독 정독 ∈ {R1 / R2 / … / 복수 병기 / —}(I-5 Read Coverage 절에서만 채운다 — 추정 금지).

| 군 | 정의(마스터 플랜 Phase 1.1 Step 1) | 기대치(출처) |
|---|---|---|
| (i) | `Claude/plans/*.md` 전건(날짜 계획서 + `INDEX.md` + `MASTER_ROADMAP_*` + 본 arc 계획서) | 93 파일·10,383줄(1g 실측 I-6) · brief 90/9,567 · v1 sub 91/9,503 · master 92/9,567 |
| (ii) | `Claude/docs/**/PLAN_*.md` + `Claude/docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` | 15 + 1 |
| (iii) | `HANDOVER*.md` 전건 — `Claude/old/` 제외분과 `old/` 3본(구트랙, 별도 표시) 분리 · hash 사본 판정(§3.3) | 25/1,612(old 제외) + old 3 = 28 |
| (iv) | `Claude/docs/Fable_점검/*.md` | 8·885줄 |
| (v) | `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | 106줄 |
| (vi) | `Claude/docs/INDEX.md` · `Claude/plans/INDEX.md` · `Claude/docs/v*/results/INDEX_v*.md` 전건 | 197·65·139(+기타) |
| (vii) | ledger = `Claude/results/**/*LEDGER*.md` + `Claude/docs/v*/results/*LEDGER*.md` | 30(results 2·process 26·research 2) + docs 측 미실측 |
| (viii) | 각 버전 `MERGE_READINESS_*`·`*CHANGE_LOG*`/`*CHANGE_LEDGER*`·`PHASE_*_RESULT.md`·`AUDIT_LINEAGE*`·`V1025_DATA_ADDENDUM*`·`*DOC_EDIT_REPORT*`·`*T13_T14*`·`*CASCADE_TODO*`·`ARCHIVE_NOTE*` | 미실측 |
| (ix) | 조사 문서군 = `Claude/results/comp_v24/*.md` · `Claude/results/comp_v26_data/*.md` · `Claude/docs/v1.0.22/results/comp_v23/*.md` · `…/comp_SM2/*.md` · `…/comp_FR/**` · `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` · `Claude/docs/v1.0.20/results/*`(FIGS_PICK·DIRECTION_*·TRIAGE_P7·V1020_STYLE_RUBRIC) · `*V1013_TERMS_POLICY*` · `*V1014_TONE_AUDIT*` | 미실측 |
| (x) | `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` · `Claude/jcp_extract.txt`(+ `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` 존재·바이트만) | 50줄 · 724줄 |
| (xi) | v1.0.26 실물 = `Claude/docs/v1.0.26A-regsol/README.md` · `Claude/docs/v1.0.26B-gallery/README.md` · `Claude/results/comp_v26_data/README.md` · `Claude/results/comp_v26_data/out_versions/build.log` (+ 조사 스크립트 `.py` 목록·줄수) | 199·193·50·36 |
| (xii) | 서지 원장 = `Claude/docs/v1.0.20/results/V1020_REFERENCE_LEDGER.md` · V1021 · V1022 · V1023(사본 여부 hash) | 55·38·33·33 |
| (xiii) | `Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md`(또는 동일 취지 reflect 계획서 실물명) · `Claude/results/V1024_REFLECT_EXECUTION_LEDGER.md`(실물 경로 확인) | 미실측 |
| (xiv) | git untracked 21 = §3.5 | Claude 8 / Codex 13 |
| (xv) | 판독 산출 = `Claude/results/handoffs/2026-09-02-v2-master-plan/**` 전건(brief·audit_checklist·iter_1/*·wf/* — R1~R7·R7 json·audit 3본·plan_draft v2/v3·fix_change_log·critic·plan_v3_appendix_ABC·review_master·go_1g_check) | 시드 등재(정독 대상 아님 표시) |
| (xvi) | 현행 tex = `Claude/docs/v1.0.25.1/*.tex` + `_sections/*.tex` — 빌드 포함/미포함 열(§3.2) | 60·9,214줄 |
| (xvii) | 유실 자산 원문 = `Claude/old/_archive/graphite_ica_ch1_Fable_v2.tex` · `_Fable_v3.tex` · `_Opus_v4.tex` · `_Opus_v5.tex` · `_Opus_v6.tex`(Assumptions 23 — 1.4 Step 11 정독 대상) | 5본 존재 |
| (xviii) | v1.0.25 base tex = `Claude/docs/v1.0.25/*.tex` + `_sections/*.tex` — 파일 수·줄수 합계 + v1.0.25.1 대비 hash 상이 파일 목록(1g 기록 = 10 파일: sections 3 + masters 3 + ARCHIVE_NOTE + PDF 3 — tex 만 대조) | 60 |

(vii)~(ix)·(xiii) 처럼 "미실측" 인 군은 glob 패턴으로 실물을 찾아 전건 등재한다. 패턴에 안 잡히는 유사 파일(예: `*LEDGER*` 가 아닌 ledger 성격 파일)을 발견하면 "추가 발견" 으로 같은 군에 넣고 비고에 표시한다.

**§2 합계** — 군별 파일 수·줄수, 전체 합계, 중복(한 파일이 두 군에 걸침) 처리 규칙(한 번만 계수 · 어느 군을 정본으로 했는지).

**§3 brief §3-C·§2.9 수치와의 차이** — plans(90 / 91 / 92 / 93 · 9,567 / 9,503 / 10,383) · HANDOVER(28 / 25 · 1,612) · PLAN_*(15 / 16) 각각 **실측 정본**과 "차이를 만든 파일명·줄수" 열거(예: 본 arc 계획서 +1·+816, INDEX 포함 여부, MASTER_ROADMAP 2 포함 여부, old/ 3 포함 여부).

**§4 hash 중복 그룹** — §3.3 결과 전건 + 고유본 지정 + 근거.

**§5 untracked 21** — §3.5.

**§6 현행 tex 60** — §3.2 결과: `\input` 순서(마스터별) · 빌드 포함 58 / 미포함 2 · orphan · 독립 부록 · 지원 4본.

**§7 판독 커버리지 대조** — R1~R7 Read Coverage 절이 열거한 파일 집합이 OUT-INV 에 전부 있는지(⊆). 없는 경로가 있으면 열거하고 "R# 경로 오기 후보 / 실물 부재" 로 분류(수정하지 않는다 — 등록부 단계에서 다룬다).

**§8 부재·미검독 명시** — 실물이 없는 기대 항목(부재) · 이 Step 에서 열지 않은 파일군(미검독 — 예: 조사 문서군 본문은 존재·줄수만 측정, 내용 미검독).

**§9 Decision Queue** — 결정이 필요한 항목(예: 군 경계 모호 파일의 소속).

## 5. 게이트 자체 점검(work_log 에 O/X + 근거)

- G1 Test-Path 100%: OUT-INV 의 모든 path 가 TSV 에 존재(스크립트로 대조 — 대조 코드·결과 수치를 work_log 에).
- G2 줄수 열 빈 셀 0(부재 항목은 표에 넣지 않고 §8 에).
- G3 빌드 포함/미포함 60/60.
- G4 untracked Claude 8/8 지위 + 근거 · Codex 13/13 "무접근" 고정.
- G5 §3 차이 열거 완료(plans·HANDOVER·PLAN_* 3건 정본 확정).
- G6 §7 대조 완료(⊆ 판정 + 예외 열거).
- G7 hash 중복 그룹 전건 + 고유본 지정.
- G8 Read Coverage 표 = 실제 읽은 파일·행 범위 전건.

## 6. 금지·주의

- 기존 파일 수정·삭제·이동 X(신규 A·B·C 만) · git X · `Codex/` X · 계획서 수정 X · 추정 수치 X(실측 아니면 "미측정"/"미검독").
- `Get-Content` 로 png·pdf 를 읽지 않는다(존재·바이트만).
- 반환 메시지 = 생성 파일 3본 경로 + 게이트 O/X 요약 + DQ 건수. 본문 내용을 반환 메시지에 길게 옮기지 않는다(파일이 정본).
