# work_log — v1.0.27 작업 챕터 1 · Phase 1.1 · Step 1 「인벤토리 파일 생성(OUT-INV)」 · 작업 sub · iter_1

> 작성 = 작업 sub(Fable 5.1), 2026-09-03 09:24~10:10 +09:00. 지시 = `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md`(전문 정독). 통제 문서 = `Claude/plans/2026-09-02-v2-master-plan.md` Phase 1.1(L303–316). 본 sub 는 검수·확정·commit 을 하지 않는다(검수 sub·master 소관). git 명령 0회 · `Codex/` 0회 접근 · 기존 파일 수정·삭제·이동 0.

## 1. 수행(시간순)

| # | 시각 | 행위 | 결과 |
|---|---|---|---|
| 1 | 09:2x | brief 전문 정독(L1–133) | §0 5항목·§1 입력·§2 산출 3본·§3 명령·§4 양식·§5 게이트·§6 금지 확인 |
| 2 | 09:2x | I-1 마스터 플랜 지정 범위 5개 · I-2 `docs/INDEX.md` · I-3 `plans/INDEX.md` · I-4 `INDEX_v25.md` · I-6 1g txt · I-7 README L20–35 · I-8 마스터 tex 3본 정독 + R1~R7 「Read Coverage」 절 위치 Grep | Read Coverage 표(§6) 참조 |
| 3 | 09:34:39 | brief §3.1 명령 그대로 실행 → `iter_1/inventory_raw.tsv` 생성 | 2,651행(절대경로·줄수·SHA256·바이트) |
| 4 | 09:3x | R1~R7 Read Coverage 절 8개 정독(토픽 한정) · TSV 군별 분해(PowerShell 읽기 전용 집계) · hash 중복 그룹 · untracked 실물 확인(png 존재·바이트 · 폴더 3 내부 목록) · `\input` 중첩 검색 · png/C3 참조 검색 | 실측치 확보(§2) |
| 5 | 09:4x | `common_preamble_v1024.tex`·`ch1_preamble.tex`·`ch2_preamble.tex`·`V1010_INSPECT_draft_C3.md` 전문 정독(orphan·C3 지위 근거) · appendix `\documentclass` 실측 | brief §3.2 기대와 상이한 실측 확정(§2 항목 3) |
| 6 | 09:5x | OUT-INV 생성 스크립트 작성 → 인라인 실행이 명령 길이 제한(ENAMETOOLONG)으로 불가 → 세션 스크래치패드 `gen_outinv.ps1`(휘발·프로젝트 밖)로 실행 · 변수명 충돌 2건(PowerShell 대소문자 무구분: `$l`/`$L`, `$rc`/`$RC`) 수정 · process HANDOVER 4본 귀속 규칙 누락 수정 | `Claude/results/V1027_HISTORY_INVENTORY.md` 1차 생성(1,461행) |
| 7 | 10:0x | 생성 파일 전문 자체검수(L1–1461, 6 청크) → 결함 3 + 보강 2 발견·수정·재생성 | 1,463행(§2 항목 7) |
| 8 | 10:10 | 게이트 기계 대조(§4) · 본 work_log 작성 | 완료 |

## 2. 근거·판단(4-tier: 확정 / 근거 미발견 / 추정 / 미검증 · `[sub 판단]` = 본 sub 판단)

1. **줄수 정의 오프셋(확정)** — brief §3.1 정의 `(Get-Content).Count` 는 마지막 개행 뒤 빈 문자열을 세지 않고, Read 도구 행 번호는 그것을 1행으로 표시한다. 실측(`Get-Content -Raw` 끝 문자 검사):

   | 파일 | (Get-Content).Count | 끝 개행 | CRLF | 타 출처 표기 |
   |---|---|---|---|---|
   | `CLAUDE.md` | 88 | True | True | R3 89 · brief 90 |
   | `Claude/docs/INDEX.md` | 196 | True | True | R1·brief 197 |
   | `Claude/plans/INDEX.md` | 69 | True | True | brief 65(실제 갱신 +4 — 항목 2) |
   | `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | 138 | True | True | R2·brief 139 |
   | `Claude/results/comp_v26_data/out_versions/build.log` | 36 | True | True | R2·brief 36(일치 — 오프셋 규칙의 예외; 원인 미조사·미검증) |

   → OUT-INV 의 줄수는 전부 TSV 값이며 타 출처 수치는 §3 에 병기했다. `jcp_extract.txt` 는 brief 724 → 실측 725 로 방향이 반대(미검증 · 개행 구조 미조사).
2. **`plans/INDEX.md` 65 → 69 는 실제 갱신(확정)** — I-3 전문 정독: L5–8 "본 INDEX 는 v1.0.22 이후 갱신이 밀려 있다" 스테일 경고가 남아 있으나 L10–13 에 "★ 현재 활성 — v1.0.27" 행이 추가돼 있다. 따라서 plans 합계 차이 = 본 arc 계획서 812 + INDEX +4 = 816 → 9,567 + 816 = 10,383 = 1g. 실측 10,384 의 잔여 +1 은 파일 미특정(추정: 1g 09:24 이후 마스터 플랜 v5.2 갱신 — DQ-9).
3. **빌드 포함/미포함 실측이 brief §3.2 기대와 다름(확정)** — 마스터 3본의 비주석 `\input{_sections/…}` = ch1 33 · ch2 12 · ch3 10(고유 53) · `docs/v1.0.25.1/**/*.tex` 전건 Grep 에서 마스터 외 `\input` 0(중첩 없음) → `_sections` 56 중 미포함 3 = `ch1_appD_si`(기대 일치) + `ch1_preamble` + `ch2_preamble`. 두 preamble 은 헤더 L2–3 이 "`graphite_ica_ch{1,2}_v1.0.21.tex` 가 `\input` 한다" 고 적힌 v1.0.21 잔재이고, `common_preamble_v1024.tex`:3 이 "= 구 ch1_preamble ∪ ch2_preamble" 로 흡수했음을 명시한다. 기대 58/2 → 실측 마스터 3 + 포함 53 + 미포함 4(독립 1 + orphan 3). 마스터 플랜 §2.9 L203 의 "지원 4본" 정독 배정은 재검토 대상(DQ-3). 부수 관찰: `common_preamble_v1024.tex`:2 헤더가 `common_preamble_v1022.tex` 로 표기(DQ-12) · `INDEX_v25.md`:32 의 "ch1 `\input` 34" vs 실측 33(근거 미발견).
4. **HANDOVER 수치(확정)** — old/ 제외 25/1,612(1g·master 일치) · old/ 포함 28/1,915. brief §3-C "28(old/ 제외)" 은 오기(28 = old/ 포함 건수).
5. **untracked Claude 8 지위(§5)** — png 5 = 같은 폴더 tracked 스크립트의 출력 경로와 정확히 일치(`graph_suite_v1017.py:37` 등, 확정) → "유효(재생성 가능 산출물)" `[sub 판단]`; `C3_graph_check/` = `V1010_INSPECT_draft_C3.md:14,23` 직접 참조(확정) → 유효; `C3_pdf_render/` = 폴더명 직접 참조 0(근거 미발견) 이나 `:15` "Ch1 35쪽·Ch2 13쪽 pdftoppm 렌더·contact sheet" 와 내용(ch1-01~35·ch2-01~13·contact sheet 2·동일 시각 2026-07-02 01:38–39) 대응(확정) → 유효(추정 상향); `regsol_test/` = `comp_v26_data/README.md:31` 폐기(확정). Codex 13 = 무접근 고정.
6. **군 우선순위·중복 규칙 `[sub 판단]`** — 한 파일 1군 계수. 우선순위 (vi)>(xv)>(i)>(ii)>(iii)>(iv)>(v)>(xii)>(x)>(xi)>(xvii)>(xvi)>(xviii)>(vii)>(viii)>(ix)>(xiii)>(xix). `old/**` 의 ledger 31·Result 33 은 패턴 매치로 등재하되 구트랙 RB 표시(DQ-5). brief 미정의 부속군 (xix) 루트 `CLAUDE.md` 를 §3.4 이행용으로 추가.
7. **자체검수에서 잡아 고친 것(확정)** — ① `2026-06-01-ch1-self-contained-rework-plan.md` 가 'rework' 규칙에 걸려 "v10 rework" 로 오귀속 → 규칙을 `rework-broadening` 한정 → "v2 이전 06-01, 추정"; ② `…connective-masterequation…` 이 `master` 문자열 매치로 마스터플랜 오분류 → 규칙을 `-master-plan`/`MASTER` 한정 + 비고; ③ §8.3 표에만 있던 `Claude/results/Step 1 — 인벤토리 파일 생성(OUT-INV).md`(35줄 · master 산출 · TSV 시점 존재)·`V1024_PROGRESS_SUMMARY.md`·`_FINAL_README.md`·`MISSING_CONTENT_REVIEW.md` 를 산문에 명시; ④ §6 에 `INDEX_v25.md`:32 34 vs 33 차이 기록; ⑤ process HANDOVER 4본 귀속 규칙 추가(1차 생성에서 "미측정" 으로 떨어졌던 것).
8. **버전 귀속 "추정" 행** — 날짜·이름으로만 추론한 행(2026-05-29~06-09 계획서 · `results/process/PHASE_*` 계보 · `anodefit-*` · `MASTER_ROADMAP_*`)은 표에 "추정" 을 명기했다(DQ-2). 실물 정독 없이 확정하지 않았다.
9. **스크래치패드 스크립트 사용 `[sub 판단]`** — 생성 명령 인라인 실행이 명령 길이 제한(ENAMETOOLONG)으로 불가. 지시의 "Out-File 은 brief 지정 신규 경로에만·Write 신규 3본" 을 프로젝트 파일에 대한 제약으로 읽고, 세션 스크래치패드(휘발·프로젝트 밖·시스템이 임시 스크립트 용도로 지정한 디렉터리)에 `gen_outinv.ps1` 을 두어 실행했다. 프로젝트 안 신규 파일은 3본뿐이다(DQ-15 로 표면화).

## 3. 생성 파일 3본(프로젝트 안 신규 파일 전건 · 기존 파일 무변경)

| 산출 | 절대 경로 | 실측 |
|---|---|---|
| A. OUT-INV | `D:\Projects\Project_Anode_Fit\Claude\results\V1027_HISTORY_INVENTORY.md` | 1,463행 · 197,079 B · SHA256 77C2BF6A5151B6D5… · 10:09:09 |
| B. 실측 원본 | `D:\Projects\Project_Anode_Fit\Claude\results\handoffs\v1027-phase-1.1-inventory\iter_1\inventory_raw.tsv` | 2,651행 · 414,664 B · SHA256 E1A393740350D22E… · 09:34:39(brief §3.1 명령 출력 그대로 · 가공 0) |
| C. work_log | `D:\Projects\Project_Anode_Fit\Claude\results\handoffs\v1027-phase-1.1-inventory\iter_1\work_log.md` | 본 파일 |

프로젝트 밖 휘발 파일(산출 아님): 세션 스크래치패드 `gen_outinv.ps1`(OUT-INV 생성 스크립트 — 재현 목적으로 master 가 원하면 결과 폴더로 옮길 수 있으나 본 sub 는 옮기지 않았다).

## 4. 게이트 자체점검(brief §5) — O/X + 근거

대조 코드(읽기 전용 · PowerShell): OUT-INV 를 읽어 §1 의 데이터 행 `| n | \`path\` | 줄수 | …` 을 정규식으로 추출 → 각 path 를 TSV 상대경로 집합과 `Test-Path`(루트 결합) 로 대조 · 줄수 셀 `^\d+$` 검사 · (xvi) 8열 표의 빌드 열 비어 있지 않음 검사 · §4 그룹 행 수 · §7 행 수/등재 수 · §5 행 수 계수. 실행 10:10:08.

| 게이트 | 판정 | 근거(수치) |
|---|---|---|
| G1 Test-Path 100% | **O** | §1 데이터 행 611 = 고유 path 611 · TSV 존재 611/611 · `Test-Path` True 611/611. (611 = 계수 665 − (xviii) 요약 처리 60 + (xviii) diff 행 6) |
| G2 줄수 빈 셀 0 | **O** | 611/611 숫자 · 부재 항목은 표에 넣지 않고 §8.1(부재 0건) |
| G3 빌드 포함/미포함 60/60 | **O** | (xvi) 빌드 열 60/60 채움 · 집계 마스터 3 + 포함 53 + 미포함 4(독립 1 + orphan 3) = 60 · §6 마스터별 순서 33/12/10 |
| G4 untracked | **O** | §5.1 Claude 8/8 지위+근거(path:line) · §5.2 Codex 13/13 "Codex 소관 · 무접근(판정 안 함)" 고정 · 열람 0 |
| G5 §3 차이 열거 | **O** | plans 93/10,384 · HANDOVER 25/1,612(old 제외)·28/1,915 · PLAN_* 15/645 + 1 — 3건 정본 확정 + 차이 파일명·줄수 열거(§3.1~3.5) + CLAUDE.md 88 |
| G6 §7 대조 | **O** | R1~R7 Read Coverage 열거 131 파일 → 등재 131 · 군 밖 0 · 부재 0 → ⊆ 성립(예외 0) |
| G7 hash 중복 | **O** | §4 그룹 259 전건(관련 파일 769) · 각 행 고유본 1 지정 · 규칙 명시(동명이물 1건은 DQ-4) |
| G8 Read Coverage | **O** | §6 표 = 본 sub 가 실제 읽은 파일·행 범위 전건(부분·grep·목록 조회 분리 표기) |

## 5. 다음(검수 sub · master 에게)

- 검수 sub: (a) §1 표의 `버전 귀속`·`문서 종류` 는 규칙 기반 자동 부여이므로 규칙(§0) 자체의 타당성과 "추정" 행을 우선 반박 대상으로 볼 것; (b) §3.2·§6·§8.1 의 "brief 기대와 다른 실측" 3건(HANDOVER 28 오기 · preamble orphan · plans +1) 이 실물과 맞는지 재대조; (c) §5 지위 판정의 근거 path:line 실물 대조.
- master: DQ-1~15(OUT-INV §9) 결정 · Step 2 정독 배정표 착수 시 (xviii) 60 은 행 미열거(diff 6 만) 임을 전제로 배정표 차집합 규칙 정의 · 스크래치패드 스크립트 보존 여부.
- 본 sub 미수행(범위 밖): 계획서 수정 · Result/Ledger 작성 · commit · Codex 접근 · png/pdf 열람 · 등재 파일 본문 정독.

## 6. Read Coverage(본 sub 가 실제 읽은 파일 · 행 범위 · 방식 — 표에 없으면 읽지 않은 것)

| # | 파일(`D:\Projects\Project_Anode_Fit\` 기준) | 행 범위 | 방식 | 비고 |
|---|---|---|---|---|
| 1 | `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md` | 1–133(전문; Read 표기 1–134) | Read | 지시 |
| 2 | `Claude/plans/2026-09-02-v2-master-plan.md` | 39–68 · 160–207 · 224–226 · 303–316 · 593–620 | Read(지정 범위) | I-1 · 그 밖의 영역 미검독 |
| 3 | `Claude/docs/INDEX.md` | 1–196(전문; Read 표기 1–197) | Read | I-2 |
| 4 | `Claude/plans/INDEX.md` | 1–69(전문; Read 표기 1–70) | Read | I-3 |
| 5 | `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | 1–138(전문; Read 표기 1–139) | Read | I-4 |
| 6 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R1_version_register_v3_to_v1019.md` | 174–205(§7 Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 7 | `…/wf/R2_version_register_v1020_to_v1026.md` | 265–299(§6 Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 8 | `…/wf/R3_binding_decisions_and_lost_directions.md` | 361–397(Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 9 | `…/wf/R4a_diagnosis_scope_ch1_partT.md` | 324–362(Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 10 | `…/wf/R4b_diagnosis_scope_ch2_ch3_appendix.md` | 397–430(§11 Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 11 | `…/wf/R5_theory_candidates_thermo_statmech.md` | 389–425(§8 Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 12 | `…/wf/R6_theory_candidates_kinetics_hys_heat.md` | 378–414(§9 Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 |
| 13 | `…/wf/R7_reference_master_map.md` | 513–533(Read Coverage 절 전문 = 파일 끝) | Read(토픽 한정) | I-5 · L5 는 Grep 매치 행으로만 열람 |
| 14 | `…/wf/go_1g_check_2026-09-03.txt` | 1–15(전문) | Read | I-6 |
| 15 | `Claude/results/comp_v26_data/README.md` | 20–35(토픽 한정) | Read | I-7 · 나머지 미검독 |
| 16 | `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` | 1–62(전문) | Read | I-8 |
| 17 | `Claude/docs/v1.0.25.1/ch2_lco_v1.0.24.tex` | 1–34(전문) | Read | I-8 |
| 18 | `Claude/docs/v1.0.25.1/ch3_si_v1.0.24.tex` | 1–34(전문) | Read | I-8 |
| 19 | `Claude/docs/v1.0.25.1/_sections/common_preamble_v1024.tex` | 1–84(전문) | Read | orphan 판정 근거(brief 밖 추가 정독) |
| 20 | `Claude/docs/v1.0.25.1/_sections/ch1_preamble.tex` | 1–77(전문) | Read | 동상 |
| 21 | `Claude/docs/v1.0.25.1/_sections/ch2_preamble.tex` | 1–56(전문) | Read | 동상 |
| 22 | `Claude/results/process/V1010_INSPECT_draft_C3.md` | 1–107(전문) | Read | untracked C3 폴더 지위 근거(brief 밖 추가 정독) |
| 23 | `Claude/results/V1027_HISTORY_INVENTORY.md`(본 sub 산출) | 1–1461(1차 생성본 전문 · 6 청크) + 재생성 후 변경 지점 Select-String 확인 | Read | 자체검수 |
| 24 | `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/inventory_raw.tsv`(본 sub 산출) | 전 행(PowerShell 파싱 · 집계) | PowerShell | 문서 정독 아님 |
| G1 | `Claude/docs/v1.0.25.1/**/*.tex` | 패턴 `^[^%]*\input\{` 매치 행만 | Grep | 마스터 3본 외 매치 0 |
| G2 | `Claude/**/*.md` | 패턴 `C3_graph_check\|C3_pdf_render\|sample_test_v1017\|sample_test_v1018\|graph_suite_v1017\|graph_suite_v1018\|regsol_test` 매치 행만 | Grep | untracked 참조 판정 |
| G3 | `Claude/results/**`(전 확장자) | 패턴 `C3_pdf_render\|pdf_render\|C3_graph_check` 매치 행만 | Grep | `C3_pdf_render` 0건 |
| G4 | `Claude/docs/v1.0.17` · `v1.0.18.1` · `v1.0.18.2` 의 md/py/tex/txt | 패턴 `sample_test\|graph_suite` 매치 행만 | Select-String | 스크립트 OUT 경로 확인 |
| G5 | `Claude/docs/INDEX.md` · `Claude/results/process/*.md` · `V1017_EXECUTION_LEDGER.md` · `V1018_EXECUTION_LEDGER.md` | 패턴 `sample_test\|graph_suite` / `png\|figs\|sample` 매치 행만 | Select-String | 간접 근거 |
| G6 | `Claude/docs/v1.0.25.1/appendix_phase_separation.tex` | 패턴 `\documentclass\|\begin{document}\|\input` 매치 행만(L13·L41) | Select-String | 독립 부록 확정 |
| G7 | `Claude/docs/v1.0.25.1/_sections/*.tex` | 패턴 `\input\|\include\|preamble`(비주석) 매치 행만 → 0건 | Select-String | 중첩 없음 재확인 |
| G8 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R*.md` | 패턴 `Read Coverage` 매치 행만 | Grep | 절 위치 확인 |
| D1 | `Claude/docs/v1.0.17` · `v1.0.18.1` · `v1.0.18.2` · `Claude/results/process/C3_graph_check` · `C3_pdf_render` · `Claude/results/regsol_test` · `Claude/skills` | 디렉터리 목록(이름·바이트·mtime)만 | Get-ChildItem | 내용 미열람(png·html 미개봉) |
| D2 | `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` | 존재·바이트만 | Get-Item | 미개봉 |
| M1 | `CLAUDE.md` · `docs/INDEX.md` · `plans/INDEX.md` · `INDEX_v25.md` · `out_versions/build.log` | `Get-Content -Raw` 끝 문자(개행·CRLF)만 | PowerShell | 오프셋 근거(§2 항목 1) · 내용 정독 아님 |

미검독(명시): 위 표 밖의 모든 파일 — OUT-INV 등재 665본의 본문(계획서·인계·ledger·Result·조사 문서·tex 본문·판독 산출 R1~R7 의 Read Coverage 절 이외 영역·마스터 플랜의 지정 범위 밖 영역) · png/pdf/html 전부 · `Codex/` 전체(0회 접근).

## 7. Decision Queue(본 sub 는 진행하지 않음 — OUT-INV §9 와 동일 15건 · 여기서는 요지만)

| # | 요지 | 기본값 |
|---|---|---|
| DQ-1 | 문서 종류 14종 어휘 밖 세부 매핑(감사(머지 판정)·Result(집행 보고)·기타(…)·서지 원장(초안)) 확정 | §0 규칙 |
| DQ-2 | 버전 귀속 "추정" 행(05-29~06-09 계획서 · process PHASE_* 계보 · anodefit 2본 · MASTER_ROADMAP 2본) 실물 정독 확정 | "추정" 명기 유지 |
| DQ-3 | orphan preamble 2본(`ch1_preamble`·`ch2_preamble`)의 정독 대상 유지 여부(§2.9 L203 "지원 4본" 재검토) | 등재 유지·orphan 표기 |
| DQ-4 | hash 고유본 표기(현행 tex 60 은 v1.0.24 사본이 고유본이 됨 · 동명이물 `REVIEW_LEDGER_CH2_10ROUND*`) | §4 규칙 그대로 |
| DQ-5 | `old/**` ledger 31·Result 33 등재 범위 | 등재(구트랙 RB) |
| DQ-6 | (ix) 미등재 하위군(v1.0.22 comp_AUD·R2~R8·RV 84 · v1.0.20 comp_* 97 · REVIEW 11) 편입 | 계수만 |
| DQ-7 | untracked png 5(재생성 가능 산출물) git 처리 | 지위 기재만 |
| DQ-8 | `C3_pdf_render/` 50장 보존 | 지위 기재만 |
| DQ-9 | plans 10,384 vs 1g 10,383 의 +1 파일 특정 | 실측 정본 |
| DQ-10 | `comp_v24` 비-md 52본 등재 | 계수만 |
| DQ-11 | `Claude/skills/…/SKILL.md` 등재 | 미등재 |
| DQ-12 | `common_preamble_v1024.tex`:2 헤더 파일명 불일치(문건 결함 후보) | 관찰만 |
| DQ-13 | (xi) 추가 발견 2본(R2 +2·+3 폐기분 산출) 등재 | 등재(폐기 표시) |
| DQ-14 | `sample_test_v1018_2.png`·`P4_lco_heat_validation.png` tracked 여부(git 필요) | 관찰만 |
| DQ-15 | OUT-INV 생성 스크립트를 세션 스크래치패드(휘발)에 두고 실행한 방식의 승인 · 보존 여부 | 스크래치패드 사용 |
