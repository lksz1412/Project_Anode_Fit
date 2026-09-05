# V1027_HISTORY_INVENTORY — v1.0.27 작업 챕터 1 · Phase 1.1 · Step 1 인벤토리(OUT-INV)

> 작성 = 작업 sub(Fable 5.1), 2026-09-03. 통제 문서 = `Claude/plans/2026-09-02-v2-master-plan.md`(TSV 시점 v5.2 · 현재 v5.4) Phase 1.1 Step 1(L303–316) · 지시 = `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md`. 실측 원본 = `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/inventory_raw.tsv`(2,651행 · 절대경로·줄수·SHA256·바이트) · 작업 기록 = 같은 폴더 `work_log.md`. 검수·확정·commit 은 master 소관. **iter_2(2026-09-03, master 정정)**: 검수 sub 라운드 1(`iter_1/audit_log.md`, AUD-01~15) 삼각검증 후 master 가 직접 반영 — 반영 내역·DQ 처분 = §10. **iter_3(2026-09-03, master 정정)**: 검수 라운드 2(`iter_2/audit_log_r2.md`, AUD-R2-01~10) 반영 — 「추가 발견」 정책 단위 정의 확정 + 31본 등재 + 잔여 0 스크립트 증명(`iter_3/policy_check.txt`) = §10.4. **iter_4(2026-09-03, master 정정)**: 검수 라운드 3(`iter_3/audit_log_r3.md`, 확정결함 0 · AUD-R3-01~10) 반영 — 표기·문안·규칙 텍스트 정정 + `FITTING_GUIDE` 규약 기록 8본 등재 = §10.5. **iter_5(2026-09-05, master 정정)**: 검수 라운드 4(Workflow 3렌즈+반박 3인/건, `iter_4/audit_log_r4.md`, 확정결함 1 AUD-R4-01 = 정책 (b) 토크나이저 결함 · 경미 10 · 제안 4) 반영 — `CODE_w_check.md` 등재 · 토큰 정규화 규칙 명기·재실행 · 표기·규칙 텍스트 정정 = §10.6. iter_1 원문은 §10 에 적힌 변경 외 무수정.

## 0. 머리

- **목적**: 작업 챕터 1(이력 통합)의 정독 대상 전건을 실물(path·줄수·hash)로 고정한다 — Step 2 정독 배정표의 모집단. 마스터 플랜 Phase 1.1 Step 1 (i)~(xvi) + brief §4 (xvii)·(xviii) + 부속 (xix) 루트 `CLAUDE.md`(brief §3.4).
- **실측 일시**: 2026-09-03 09:34:39 +09:00 (PowerShell 7 · 작업 디렉터리 `D:\Projects\Project_Anode_Fit\Claude` · `Codex/` 0회 접근 · git 명령 0회).
- **실측 명령**(brief §3.1 그대로 · 재현 가능 · 읽기 전용):

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
(Get-Content $out).Count      # → 2651
```

- **모집단 정의**: 파일 단위 · 확장자 `.md .tex .txt .log .json .py` · `Claude/**` 재귀 + 루트 `CLAUDE.md` 1본 = 2,651행. 경로 표기는 `Claude/` 상대(루트 파일만 `CLAUDE.md`). png·pdf·html·npz·aux·csv 등 확장자 밖 파일은 모집단 밖(§5·§8 에 존재·바이트만). 본 Step 산출 3본(OUT-INV·TSV·work_log)은 TSV 생성 뒤 작성되어 TSV 에 없다.
- **줄수 정의**: `(Get-Content -Path).Count` = 개행 분리 행 수(마지막 개행 뒤 빈 문자열은 계수하지 않음). Read 도구 행 번호(R1~R7·brief·마스터 플랜이 적은 수치)는 파일이 개행으로 끝나면 마지막 빈 행을 1행 더 표시하므로 **TSV 값 = 그 표기 − 1** 인 경우가 대부분이다(확정 근거: `CLAUDE.md` 88 ↔ R3 89 · `docs/INDEX.md` 196 ↔ 197 · `INDEX_v25.md` 138 ↔ 139 — 세 파일 모두 trailing CRLF 개행 실측 True, work_log §2). 본 문건의 모든 줄수는 TSV 값이며 타 출처 수치는 §3 에서 병기·차이 기록.
- **4-tier 규약**: 확정(path:line 첨부) / 근거 미발견 / 추정 / 미검증. `[sub 판단]` = 본 작업 sub 의 판단(사용자·master 결정 아님).
- **열 어휘**: 문서 종류 ∈ {마스터플랜 / 세부 계획서 / 인계 / 감사 / 클로징 / INDEX / ledger / Result / 조사 / 서지 원장 / 원문 tex / 시드(판독) / 통제(본 arc) / 기타} — 어휘 밖 세부는 괄호. **매핑 규칙**(파일명 패턴 → 종류, `[sub 판단]`): `HANDOVER*`→인계 · `INDEX*`→INDEX · `*REFERENCE_LEDGER*`→서지 원장(`REFLEDGER_DRAFT`→서지 원장(초안)) · `*LEDGER*`/`STEP_LOG_*`/`*CHANGE_LOG*`→ledger · `*RESULT*`→Result · `MERGE_READINESS*`→감사(머지 판정) · `*AUDIT*`/`*REVIEW*`/`*TRIAGE*`/`*INSPECT*`→감사 · `CLOSING*`→클로징 · `plans/`·`PLAN_*`→마스터플랜(파일명에 `master`/`MASTER`)·세부 계획서 · `.tex`→원문 tex · `results/handoffs/`→시드(판독)·통제(본 arc) · `DATA_ADDENDUM`→기타(데이터 정정 addendum) · `DOC_EDIT_REPORT`/`T13_T14`→Result(집행 보고) · `CASCADE_TODO`→기타(지시서) · `ARCHIVE_NOTE`→기타(폴더 지위) · `TOUCHUP_NOTE`→기타(검증 기록) · `.py`/`.log`/`.json`→기타(코드/로그/데이터) · 그 밖의 `.md`→조사. **iter_4 추가**(AUD-R3-04): `COMPARISON*`/`*FIXLIST*`/`*SWEEP_LIST*`→감사 · `*CHARTER*`→기타(규약 charter) · `FITTING_GUIDE`→기타(가이드 — 규약 기록). **iter_5 추가**(AUD-R4-11·15): `AUD_*`→감사(선순위) · `V1010_*_REPORT`→Result(점검 보고) · `CHERRYPICK*`→Result(결정 기록) · `AUTHOR_BRIEF`→기타(경쟁 저작 brief) · `RB_AL_MASTER`→ledger(통합 Assumption Ledger — 본문 판단 · glob `*MASTER*` 오매치) · `.txt`→기타(텍스트)(단 `jcp_extract.txt`→조사(원문 추출)) · 루트 `CLAUDE.md`→통제(프로젝트 지침) · handoffs `.json`→시드(판독·json) · `CODE_w_check`→조사(코드 실행 검증 기록) · `*INSPECT*` 는 기본 규칙에 이미 있어 iter_4 구에서 제거 · 글로브 의미론 = `*x*` 부분 일치 / `x*` 접두(`policy_check` 정규식과 동일).
- **버전 귀속 규칙**(`[sub 판단]`): `docs/v1.0.NN(.M)/`→v1.0.NN(.M) · `docs/v1.0.26A/B`→v1.0.26 · `Claude/old/**`→구트랙 RB(단 `old/_archive/graphite_ica_ch1_{Fable,Opus}_vN.tex` 5본 = Fable v2~v10 세부 vN · `old/Ch1_v7~v10/`·`old/Ch2_v3~v4/` tex 6본 = Fable v2~v10 세부 v7~v10·Ch2 v3~v4 — iter_4 AUD-R3-04) · `results/comp_v24/`→v1.0.24 · `results/comp_v26_data/`→v1.0.26 · `V10NN_*`→v1.0.NN · `results/PHASE_FB*`·`results/V1024_FEEDBACK_*`→v1.0.24.1(`docs/INDEX.md`:21 v1.0.24.1 리비전 이력 — iter_2 AUD-10) · `results/PHASE_V0~V3*`→v1.0.24(추정) · `plans/` = 파일명 `v10NN` 우선, 없으면 날짜(2026-06-10~06-30 = Fable v2~v10 세부 vN/날짜, 06-09 이전 = "v2 이전 — 추정", **07-01 이후 무토큰 = `docs/INDEX.md` 계보 대응: `fable-reaudit*`→v1.0.12(:157 · 확정급) · `anodefit-*` 07-18→v1.0.23(추정) — iter_5 AUD-R4-10**) · `results/process/PHASE_*` 등 무버전 파일 = 계획서명·날짜 대응 추정(표에 "추정" 명기 — iter_5 AUD-R4-09 로 radius·rework·2track 9행 부기; 단 `docs/INDEX.md` 계보 절이 직접 귀속시키는 `FABLE_REAUDIT_*`→v1.0.12(:157)는 확정급) · `results/handoffs/`·본 arc 계획서→본 arc · INDEX 2본·`Fable_점검`·`CLAUDE.md`·`jcp_extract.txt`→횡단. "추정" 이 붙은 귀속은 실물 정독 없이 이름·날짜로 추론한 것이며 Step 2 정독에서 확정 대상이다.
- **판독 정독(R#) 열**: R1~R7 각 「Read Coverage」 절(work_log Read Coverage 표의 행 범위)에서만 채웠다. 표기 = `R#`(배정 전문) · `R#(추가)`/`R#(보조)`/`R#(보강)`(배정 밖 전문) · `R#(부분)`(행 범위 부분) · `R#(diff)`(diff 출력만) · `R#(grep)`/`R#(glob)`(매치 행·존재 확인만) · `—`(미정독). R3 의 `_sections/*.tex` 전건 grep 과 R7 의 `_sections` 53본 + 마스터 3본 기계 스캔은 파일별 태그로 붙이지 않고 §7 말미에 일괄 기록했다. 경계(iter_2 AUD-15): **행 범위가 특정된 grep 만 파일별 `R#(grep)` 태그**, 카운트·키워드 grep 은 §7 말미 일괄.
- **중복 처리 규칙**: 한 파일은 한 군에만 계수한다. 우선순위 = (vi) > (xv) > (i) > (ii) > (iii) > (iv) > (v) > (xii) > (x) > (xi) > (xvii) > (xvi) > (xviii) > (vii) > (viii) > (ix) > (xiii) > (xix). 다른 군 정의에도 걸리는 파일은 그 군 머리에 "→ (정본 군)" 으로 참조만 적는다. hash 가 같은 사본은 각각 별개 파일로 계수하되 비고에 고유본/사본을 표시한다(§4 규칙).

## 1. 군별 인벤토리 표

### (i) `Claude/plans/*.md` 전건

- 정의: `Claude/plans/` 직계 `.md` 전건(날짜 계획서 + `INDEX.md` + `MASTER_ROADMAP_*` + 본 arc 계획서). 하위 폴더 없음(실측). `INDEX.md` 는 (vi) 우선 규칙으로 (vi) 에 계수 — 본 표 = 92 행, (i) 정의상 전건 = 92 + INDEX 1 = 93
- 기대치(출처): 93 파일·10,383줄(1g 실측 I-6:15) · brief 90/9,567 · v1 sub 91/9,503 · master 92/9,567(§2.9 L195) — 차이 열거 = §3.1
- 실측: **92 파일 · 10315 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/plans/2026-05-29-consolidation-roadmap.md` | 109 | Fable v2~v10(세부: v2 이전 05-29, 추정) | 세부 계획서 | — | — |
| 2 | `Claude/plans/2026-05-29-intent-gap-diagnosis-consolidation-plan.md` | 450 | Fable v2~v10(세부: v2 이전 05-29, 추정) | 세부 계획서 | — | — |
| 3 | `Claude/plans/2026-05-30-undergrad-rederivation-rebuild-plan.md` | 213 | Fable v2~v10(세부: v2 이전 05-30, 추정) | 세부 계획서 | — | — |
| 4 | `Claude/plans/2026-06-01-ch1-self-contained-rework-plan.md` | 43 | Fable v2~v10(세부: v2 이전 06-01, 추정) | 세부 계획서 | — | — |
| 5 | `Claude/plans/2026-06-03-ch1-blank-page-clean-spine-rebuild-plan.md` | 125 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 6 | `Claude/plans/2026-06-03-ch1-FINAL-logical-chain-rebuild-plan.md` | 142 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 7 | `Claude/plans/2026-06-03-ch1-from-scratch-intersection-bridge-plan.md` | 123 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 8 | `Claude/plans/2026-06-03-ch1-peak-physics-derivation-plan.md` | 115 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 9 | `Claude/plans/2026-06-03-ch1-rerevision-plan.md` | 130 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 10 | `Claude/plans/2026-06-03-ch1-rerevision2-foundation-first-plan.md` | 218 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 11 | `Claude/plans/2026-06-03-ch1-rerevision2-signs-codex-plan.md` | 63 | Fable v2~v10(세부: v2 이전 06-03, 추정) | 세부 계획서 | — | — |
| 12 | `Claude/plans/2026-06-06-ch1-register-revision-plan.md` | 87 | Fable v2~v10(세부: v2 이전 06-06, 추정) | 세부 계획서 | — | — |
| 13 | `Claude/plans/2026-06-06-ch1-sec6-statmech-accessibility-plan.md` | 176 | Fable v2~v10(세부: v2 이전 06-06, 추정) | 세부 계획서 | — | — |
| 14 | `Claude/plans/2026-06-06-ch1-sec8-10-comprehension-bridge-plan.md` | 61 | Fable v2~v10(세부: v2 이전 06-06, 추정) | 세부 계획서 | — | — |
| 15 | `Claude/plans/2026-06-06-ch1-textbook-form-plan.md` | 89 | Fable v2~v10(세부: v2 이전 06-06, 추정) | 세부 계획서 | — | — |
| 16 | `Claude/plans/2026-06-07-ch2-5-rebuild-consistent-with-ch1-plan.md` | 69 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 17 | `Claude/plans/2026-06-07-ch2-deep-revision-plan.md` | 76 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 18 | `Claude/plans/2026-06-07-ch2-recheck-ch3-direction-plan.md` | 103 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 19 | `Claude/plans/2026-06-07-ch2-textbook-quality-overhaul-plan.md` | 78 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 20 | `Claude/plans/2026-06-07-ch3-5-textbook-quality-overhaul-plan.md` | 85 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 21 | `Claude/plans/2026-06-07-ch3-content-overhaul-plan.md` | 138 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 22 | `Claude/plans/2026-06-07-ch3-faithful-to-ver3-plan.md` | 113 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 23 | `Claude/plans/2026-06-07-ch3-rebuild-on-ch1-plan.md` | 102 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 24 | `Claude/plans/2026-06-07-NEW-ch2-kinetics-build-plan.md` | 95 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 세부 계획서 | — | — |
| 25 | `Claude/plans/2026-06-08-ch1-ch2-connective-masterequation-revision-plan.md` | 169 | Fable v2~v10(세부: v2 이전 06-08, 추정) | 세부 계획서 | — | 파일명 글로브 *master* 에는 걸리나(masterequation) 마스터플랜 아님 [sub 판단] |
| 26 | `Claude/plans/2026-06-08-ch2-content-deepening-plan.md` | 99 | Fable v2~v10(세부: v2 이전 06-08, 추정) | 세부 계획서 | — | — |
| 27 | `Claude/plans/2026-06-08-ch2-directive-registry-revision-plan.md` | 123 | Fable v2~v10(세부: v2 이전 06-08, 추정) | 세부 계획서 | — | — |
| 28 | `Claude/plans/2026-06-08-NEW-ch2-hysteresis-build-plan.md` | 89 | Fable v2~v10(세부: v2 이전 06-08, 추정) | 세부 계획서 | — | — |
| 29 | `Claude/plans/2026-06-09-ch1-ch2-integration-completeness-plan.md` | 96 | Fable v2~v10(세부: v2 이전 06-09, 추정) | 세부 계획서 | — | — |
| 30 | `Claude/plans/2026-06-09-ch3-heat-build-plan.md` | 121 | Fable v2~v10(세부: v2 이전 06-09, 추정) | 세부 계획서 | — | — |
| 31 | `Claude/plans/2026-06-09-ch3-volume-enhancement-plan.md` | 96 | Fable v2~v10(세부: v2 이전 06-09, 추정) | 세부 계획서 | — | — |
| 32 | `Claude/plans/2026-06-09-merge-ch1-ch2-single-chapter-plan.md` | 94 | Fable v2~v10(세부: v2 이전 06-09, 추정) | 세부 계획서 | — | — |
| 33 | `Claude/plans/2026-06-09-textbook-depth-expansion-plan.md` | 79 | Fable v2~v10(세부: v2 이전 06-09, 추정) | 세부 계획서 | — | — |
| 34 | `Claude/plans/2026-06-10-ch1-blank-rewrite-v2-plan.md` | 80 | Fable v2~v10(세부: v2) | 세부 계획서 | — | — |
| 35 | `Claude/plans/2026-06-10-ch1-textbook-rewrite-plan.md` | 97 | Fable v2~v10(세부: 날짜 06-10) | 세부 계획서 | — | — |
| 36 | `Claude/plans/2026-06-10-full-rereview-physics-pedagogy-plan.md` | 90 | Fable v2~v10(세부: 날짜 06-10) | 세부 계획서 | — | — |
| 37 | `Claude/plans/2026-06-11-ch1-v2-code-example-plan.md` | 49 | Fable v2~v10(세부: v2) | 세부 계획서 | — | — |
| 38 | `Claude/plans/2026-06-11-ch1-v2-proofread-pass-plan.md` | 65 | Fable v2~v10(세부: v2) | 세부 계획서 | — | — |
| 39 | `Claude/plans/2026-06-11-ch1-v2-tone-derivation-pass-plan.md` | 68 | Fable v2~v10(세부: v2) | 세부 계획서 | — | — |
| 40 | `Claude/plans/2026-06-12-ch1-v2-friendly-math-figures-pass-plan.md` | 52 | Fable v2~v10(세부: v2) | 세부 계획서 | — | — |
| 41 | `Claude/plans/2026-06-12-ch1-v3-equation-selfcontained-plan.md` | 41 | Fable v2~v10(세부: v3) | 세부 계획서 | — | — |
| 42 | `Claude/plans/2026-06-13-ch1-v3-w4-math-physics-figures-plan.md` | 66 | Fable v2~v10(세부: v3) | 세부 계획서 | — | — |
| 43 | `Claude/plans/2026-06-13-ch1-v3-x-pass-plan.md` | 43 | Fable v2~v10(세부: v3) | 세부 계획서 | — | — |
| 44 | `Claude/plans/2026-06-13-ch1-v4-stacking-section-redo-plan.md` | 64 | Fable v2~v10(세부: v4) | 세부 계획서 | — | — |
| 45 | `Claude/plans/2026-06-17-ch1-v5-equation-driven-plan.md` | 208 | Fable v2~v10(세부: v5) | 세부 계획서 | — | — |
| 46 | `Claude/plans/2026-06-22-ch1-v5-comprehensive-rereview-MASTER.md` | 111 | Fable v2~v10(세부: v5) | 마스터플랜 | — | — |
| 47 | `Claude/plans/2026-06-22-ch1-v5RR-phaseR0-plan.md` | 18 | Fable v2~v10(세부: v5RR) | 세부 계획서 | — | — |
| 48 | `Claude/plans/2026-06-22-ch1-v5RR-phaseR1-plan.md` | 24 | Fable v2~v10(세부: v5RR) | 세부 계획서 | — | — |
| 49 | `Claude/plans/2026-06-22-ch1-v5RR-phaseR2-plan.md` | 26 | Fable v2~v10(세부: v5RR) | 세부 계획서 | — | — |
| 50 | `Claude/plans/2026-06-22-ch1-v5RR-phaseR3-plan.md` | 21 | Fable v2~v10(세부: v5RR) | 세부 계획서 | — | — |
| 51 | `Claude/plans/2026-06-22-ch1-v6-flowchart-reassembly-MASTER.md` | 65 | Fable v2~v10(세부: v6) | 마스터플랜 | — | — |
| 52 | `Claude/plans/2026-06-29-ch1-v7-codeflow-equation-driven-9x9x1x1-plan.md` | 185 | Fable v2~v10(세부: v7) | 세부 계획서 | — | — |
| 53 | `Claude/plans/2026-06-29-ch1-v8-derivation-expanded-9x9x1x1-plan.md` | 161 | Fable v2~v10(세부: v8) | 세부 계획서 | — | — |
| 54 | `Claude/plans/2026-06-30-ch1v9-LCO-ch2v4-mixing-2track-9x9x1x1-plan.md` | 97 | Fable v2~v10(세부: v9 2track, 추정) | 세부 계획서 | — | — |
| 55 | `Claude/plans/2026-06-30-ch2-reversible-heat-entropy-survey-plan.md` | 98 | Fable v2~v10(세부: 날짜 06-30) | 세부 계획서 | — | — |
| 56 | `Claude/plans/2026-06-30-radius-distribution-from-dqdv-peak-shape-survey-plan.md` | 99 | Fable v2~v10(세부: 날짜 06-30) | 세부 계획서 | — | — |
| 57 | `Claude/plans/2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md` | 89 | Fable v2~v10(세부: v10 rework, 추정) | 세부 계획서 | — | — |
| 58 | `Claude/plans/2026-07-01-graph-verify-code-doc-unify-v1010-plan.md` | 61 | v1.0.10 | 세부 계획서 | — | — |
| 59 | `Claude/plans/2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md` | 90 | v1.0.10 | 세부 계획서 | — | plans/INDEX.md:51 ★MASTER 표기(파일명 규칙상 세부 계획서) |
| 60 | `Claude/plans/2026-07-02-fable-reaudit-P0-P1-history-audit-plan.md` | 24 | v1.0.12(fable reaudit) | 세부 계획서 | — | — |
| 61 | `Claude/plans/2026-07-02-fable-reaudit-P2-P3-content-code-audit-plan.md` | 29 | v1.0.12(fable reaudit) | 세부 계획서 | — | — |
| 62 | `Claude/plans/2026-07-02-fable-reaudit-P4-v12-authoring-plan.md` | 35 | v1.0.12(fable reaudit) | 세부 계획서 | — | — |
| 63 | `Claude/plans/2026-07-02-fable-reaudit-v12-master-plan.md` | 92 | v1.0.12(fable reaudit) | 마스터플랜 | — | — |
| 64 | `Claude/plans/2026-07-02-v1010-P1-code-audit-plan.md` | 20 | v1.0.10 | 세부 계획서 | — | — |
| 65 | `Claude/plans/2026-07-02-v1010-P2-ch1-textbook-plan.md` | 21 | v1.0.10 | 세부 계획서 | — | — |
| 66 | `Claude/plans/2026-07-02-v1010-P3-ch2-heat-plan.md` | 21 | v1.0.10 | 세부 계획서 | — | — |
| 67 | `Claude/plans/2026-07-02-v1013-P1-P2-design-part0-plan.md` | 49 | v1.0.13 | 세부 계획서 | — | — |
| 68 | `Claude/plans/2026-07-02-v1013-restructure-master-plan.md` | 159 | v1.0.13 | 마스터플랜 | — | — |
| 69 | `Claude/plans/2026-07-03-v1010-P4-code-revision-plan.md` | 33 | v1.0.10 | 세부 계획서 | — | — |
| 70 | `Claude/plans/2026-07-03-v1013-P3-P6-compress-terms-review-plan.md` | 37 | v1.0.13 | 세부 계획서 | — | — |
| 71 | `Claude/plans/2026-07-04-v1010-P5-final-check-plan.md` | 28 | v1.0.10 | 세부 계획서 | — | — |
| 72 | `Claude/plans/2026-07-04-v1014-tone-rigor-appendix-figures-plan.md` | 146 | v1.0.14 | 세부 계획서 | — | docs/INDEX.md:130 "마스터플랜 =" 표기(파일명 규칙상 세부 계획서) |
| 73 | `Claude/plans/2026-07-04-v1015-code-update-plan.md` | 97 | v1.0.15 | 세부 계획서 | — | — |
| 74 | `Claude/plans/2026-07-05-v1010-problem-inspection-plan.md` | 35 | v1.0.10 | 세부 계획서 | — | — |
| 75 | `Claude/plans/2026-07-05-v1015-code-doc-sync-master-plan.md` | 164 | v1.0.15 | 마스터플랜 | — | docs/INDEX.md:117 마스터플랜 |
| 76 | `Claude/plans/2026-07-06-v1010-handover-integrity-inspection-plan.md` | 34 | v1.0.10 | 세부 계획서 | — | — |
| 77 | `Claude/plans/2026-07-07-v1011-lco-equation-conversion-and-consistency-plan.md` | 91 | v1.0.11 | 세부 계획서 | — | — |
| 78 | `Claude/plans/2026-07-07-v1017-register-consistency-polish-plan.md` | 117 | v1.0.17 | 세부 계획서 | — | — |
| 79 | `Claude/plans/2026-07-08-v1018-physics-extension-master-plan.md` | 106 | v1.0.18.1·v1.0.18.2(공통 — 추정) | 마스터플랜 | — | — |
| 80 | `Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md` | 79 | v1.0.19 | 세부 계획서 | — | docs/INDEX.md:67 "계획 =" · plans/INDEX.md:40 직전 완결 |
| 81 | `Claude/plans/2026-07-16-v1021-master-plan.md` | 76 | v1.0.21 | 마스터플랜 | R2 | — |
| 82 | `Claude/plans/2026-07-17-v1022-master-plan.md` | 99 | v1.0.22 | 마스터플랜 | R2·R3(grep) | — |
| 83 | `Claude/plans/2026-07-18-anodefit-bdd-integration-plan.md` | 191 | v1.0.23(추정: 날짜 07-18) | 세부 계획서 | — | — |
| 84 | `Claude/plans/2026-07-18-anodefit-MASTER-plan.md` | 128 | v1.0.23(추정: 날짜 07-18) | 마스터플랜 | R2·R3 | B7 |
| 85 | `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | 225 | v1.0.23 | 세부 계획서 | R2·R3(grep) | B6 |
| 86 | `Claude/plans/2026-07-18-v1024-completeness-validation-plan.md` | 198 | v1.0.24 | 세부 계획서 | R2 | — |
| 87 | `Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md` | 215 | v1.0.24 | 세부 계획서 | — | (xiii) reflect 계획서 실물 = 이 파일(R2 DQ-3) |
| 88 | `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md` | 226 | v1.0.24 | 세부 계획서 | R2 | — |
| 89 | `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md` | 240 | v1.0.25 | 세부 계획서 | R2·R3 | plans/INDEX.md:18 ★MASTER 표기(파일명 규칙상 세부 계획서) · A8 |
| 90 | `Claude/plans/2026-09-02-v2-master-plan.md` | 812 | 본 arc | 마스터플랜 | — | 본 arc 통제 문서(TSV 시점 v5.2 812줄 — 현재 v5.4, §3.1 주석) · §2.9·brief 집계 시점엔 미존재(§2.8 L189 "신규 예정") |
| 91 | `Claude/plans/MASTER_ROADMAP_CH2_v1.md` | 131 | Fable v2~v10(세부: 미상 — 무날짜 파일명, 추정) | 마스터플랜 | — | plans/INDEX.md:57 "마스터/로드맵(역대)" |
| 92 | `Claude/plans/MASTER_ROADMAP_v3.md` | 320 | Fable v2~v10(세부: 미상 — 무날짜 파일명, 추정) | 마스터플랜 | — | plans/INDEX.md:57 "마스터/로드맵(역대)" |

### (i-b) 추가 발견 — 구트랙 계획서 `old/**`(iter_2 · AUD-02 · DQ-5 를 (i)·(ii) 로 확장)

- 정의: 마스터 플랜 L305 ①군 glob(`*master*`·`*MASTER*`·`MASTER_ROADMAP*`) 매치 중 (i) 폴더 밖 실물 + 같은 폴더의 형제 계획서. `old/v2/` 는 구트랙 "Chapter 1 Rebuild v2"(`old/v2/results/EXECUTION_LEDGER_v2.md`:1–7 — 검수 확정) 로 Fable v2 와 **동명이물**. glob 오매치 3본(`results/research/CH1v9_LCO/10_sources_master.md` 45 · `results/research/CH2_v3/10_sources_master.md` 60 · `results/builds/v9/v9-00_spine/review2/V2_citations_master.md` 267)은 마스터플랜이 아니므로 등재하지 않는다(§8.3 계수).
- 실측: **11 파일 · 2760 줄**(TSV) — iter_3: `RB_AL_MASTER.md`(139)는 실물 헤더 L1 이 "통합 Assumption Ledger + Notation Bible + 가독 Gate" 라 계획서가 아니므로 (vii-b) 로 이동(AUD-R2-03; glob `*MASTER*` 오매치 4본째)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan-SUPERSEDED.md` | 44 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) · 파일명 SUPERSEDED |
| 2 | `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan.md` | 436 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 3 | `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md` | 780 | 구트랙 RB | 마스터플랜 | — | 구트랙(old/) · glob `*master*` 매치(L305 ①군) |
| 4 | `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md` | 172 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 5 | `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e1-spine-plan.md` | 102 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 6 | `Claude/old/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e2-intro-notation-plan.md` | 117 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 7 | `Claude/old/plans/2026-05-27-anode-fit-situational-assessment-plan.md` | 293 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 8 | `Claude/old/plans/2026-05-28-anode-fit-chapter1-rebuild-phase-e3-effective-transition-plan.md` | 107 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 9 | `Claude/old/plans/2026-05-28-anode-fit-chapter1-rebuild-phase-e4-charge-balance-plan.md` | 161 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/) |
| 10 | `Claude/old/v2/plans/MASTER_ROADMAP_v2.md` | 447 | 구트랙 RB | 마스터플랜 | — | 구트랙(old/v2 = 구트랙 "Chapter 1 Rebuild v2" — Fable v2 와 동명이물, `old/v2/results/EXECUTION_LEDGER_v2.md`:1–7) · glob `MASTER_ROADMAP*` 매치 |
| 11 | `Claude/old/v2/plans/PHASE_0_v2_FOUNDATION_PLAN.md` | 101 | 구트랙 RB | 세부 계획서 | — | 구트랙(old/v2 — 동명이물 경고는 행 10 비고) |

### (ii) `Claude/docs/**/PLAN_*.md` + v1.0.20 마스터 플랜

- 정의: `docs/**/PLAN_*.md` 전건(v1.0.20 P0~P8 9본 · v1.0.22 R1/R2/R3/R5/RA/FR 6본) + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md`
- 기대치(출처): 15 + 1(brief §4 · §2.9 L196 · 1g I-6:15 "PLAN_* 15") — 일치
- 실측: **16 파일 · 852 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` | 207 | v1.0.20 | 마스터플랜 | — | v1.0.20 한정 위치 규약(docs/INDEX.md:53 · plans/INDEX.md:38) |
| 2 | `Claude/docs/v1.0.20/plans/PLAN_P0_setup.md` | 45 | v1.0.20 | 세부 계획서 | — | — |
| 3 | `Claude/docs/v1.0.20/plans/PLAN_P1_references.md` | 41 | v1.0.20 | 세부 계획서 | — | — |
| 4 | `Claude/docs/v1.0.20/plans/PLAN_P2_part0.md` | 50 | v1.0.20 | 세부 계획서 | — | — |
| 5 | `Claude/docs/v1.0.20/plans/PLAN_P3_graphite.md` | 44 | v1.0.20 | 세부 계획서 | — | — |
| 6 | `Claude/docs/v1.0.20/plans/PLAN_P4_lco.md` | 39 | v1.0.20 | 세부 계획서 | — | — |
| 7 | `Claude/docs/v1.0.20/plans/PLAN_P5_ch2.md` | 34 | v1.0.20 | 세부 계획서 | — | — |
| 8 | `Claude/docs/v1.0.20/plans/PLAN_P6_convention.md` | 34 | v1.0.20 | 세부 계획서 | — | — |
| 9 | `Claude/docs/v1.0.20/plans/PLAN_P7_review.md` | 37 | v1.0.20 | 세부 계획서 | — | — |
| 10 | `Claude/docs/v1.0.20/plans/PLAN_P8_closing.md` | 34 | v1.0.20 | 세부 계획서 | — | — |
| 11 | `Claude/docs/v1.0.22/plans/PLAN_FR_deep_review.md` | 26 | v1.0.22 | 세부 계획서 | — | — |
| 12 | `Claude/docs/v1.0.22/plans/PLAN_R1_reorg.md` | 98 | v1.0.22 | 세부 계획서 | — | — |
| 13 | `Claude/docs/v1.0.22/plans/PLAN_R2_ch1_completion.md` | 49 | v1.0.22 | 세부 계획서 | — | — |
| 14 | `Claude/docs/v1.0.22/plans/PLAN_R3_ch2_completion.md` | 30 | v1.0.22 | 세부 계획서 | — | — |
| 15 | `Claude/docs/v1.0.22/plans/PLAN_R5_ch3_authoring.md` | 45 | v1.0.22 | 세부 계획서 | — | — |
| 16 | `Claude/docs/v1.0.22/plans/PLAN_RA_lineage_audit.md` | 39 | v1.0.22 | 세부 계획서 | — | — |

### (iii) `HANDOVER*.md` 전건(old/ 제외 25 + old/ 3)

- 정의: 파일명 `HANDOVER*.md` 전건. old/ 3본 = 구트랙 별도 표시. hash 사본 판정 = §4(`HANDOVER_v24.md` ×4 · `HANDOVER_v25.md` ×2)
- 기대치(출처): 25/1,612(old 제외) + old 3 = 28(brief §4 · §2.9 L197 · 1g) — 차이 열거 = §3.2
- 실측: **28 파일 · 1915 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.10/HANDOVER_v1.0.11.md` | 78 | v1.0.10 | 인계 | R1 | v1.0.10 폴더에 v1.0.11 인계가 있음(파일명·폴더 불일치 — 관찰) |
| 2 | `Claude/docs/v1.0.13/HANDOVER_v1.0.13.md` | 24 | v1.0.13 | 인계 | R1 | — |
| 3 | `Claude/docs/v1.0.14/HANDOVER_v1.0.14.md` | 26 | v1.0.14 | 인계 | R1 | — |
| 4 | `Claude/docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md` | 29 | v1.0.14 | 인계 | R1 | — |
| 5 | `Claude/docs/v1.0.15/HANDOVER_v1.0.15.md` | 29 | v1.0.15 | 인계 | R1 | — |
| 6 | `Claude/docs/v1.0.16/HANDOVER_v1.0.16.md` | 28 | v1.0.16 | 인계 | R1 | — |
| 7 | `Claude/docs/v1.0.17/HANDOVER_v1.0.17.md` | 32 | v1.0.17 | 인계 | R1 | — |
| 8 | `Claude/docs/v1.0.18.1/HANDOVER_v1.0.18.1.md` | 23 | v1.0.18.1 | 인계 | R1 | — |
| 9 | `Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md` | 29 | v1.0.18.2 | 인계 | R1 | — |
| 10 | `Claude/docs/v1.0.19/HANDOVER_v1.0.19.md` | 38 | v1.0.19 | 인계 | R1 | — |
| 11 | `Claude/docs/v1.0.20/HANDOVER_v1.0.20.md` | 74 | v1.0.20 | 인계 | R2 | — |
| 12 | `Claude/docs/v1.0.21/HANDOVER_v1.0.21.md` | 24 | v1.0.21 | 인계 | R2·R3(grep) | — |
| 13 | `Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md` | 147 | v1.0.22 | 인계 | R2 | — |
| 14 | `Claude/docs/v1.0.23/results/HANDOVER_v23.md` | 43 | v1.0.23 | 인계 | R2 | — |
| 15 | `Claude/docs/v1.0.24.1/results/HANDOVER_v24.md` | 88 | v1.0.24.1 | 인계 | — | 사본(고유본 = Claude/docs/v1.0.24/results/HANDOVER_v24.md) |
| 16 | `Claude/docs/v1.0.24/results/HANDOVER_v24.md` | 88 | v1.0.24 | 인계 | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/HANDOVER_v24.md · Claude/docs/v1.0.25/results/HANDOVER_v24.md · Claude/docs/v1.0.25.1/results/HANDOVER_v24.md) |
| 17 | `Claude/docs/v1.0.25.1/results/HANDOVER_v24.md` | 88 | v1.0.25.1 | 인계 | R2 | A6(brief 는 v1.0.25.1 사본을 인용) ; 사본(고유본 = Claude/docs/v1.0.24/results/HANDOVER_v24.md) |
| 18 | `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` | 170 | v1.0.25.1 | 인계 | R2·R3 | A5 ; 사본(고유본 = Claude/docs/v1.0.25/results/HANDOVER_v25.md) |
| 19 | `Claude/docs/v1.0.25/results/HANDOVER_v24.md` | 88 | v1.0.25 | 인계 | — | 사본(고유본 = Claude/docs/v1.0.24/results/HANDOVER_v24.md) |
| 20 | `Claude/docs/v1.0.25/results/HANDOVER_v25.md` | 170 | v1.0.25 | 인계 | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/HANDOVER_v25.md) |
| 21 | `Claude/old/Archive_oldtrack/HANDOVER_RB_2026-05-31.md` | 90 | 구트랙 RB | 인계 | — | 구트랙(별도 표시) |
| 22 | `Claude/old/Archive_oldtrack/HANDOVER_RB_2026-06-02.md` | 129 | 구트랙 RB | 인계 | — | 구트랙(별도 표시) |
| 23 | `Claude/old/Archive_oldtrack/HANDOVER_RB_2026-06-02b.md` | 84 | 구트랙 RB | 인계 | — | 구트랙(별도 표시) |
| 24 | `Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md` | 55 | v1.0.26 | 인계 | R2·R5(보조) | A7 · `comp_v26_data/README.md:23` "착수 시점 인계(서비스 장애로 실행 차단됐던 기록)" = stale(R2) |
| 25 | `Claude/results/process/HANDOVER_2026-06-07_ch2-5-overnight.md` | 94 | Fable v2~v10(세부: v2 이전 06-07, 추정) | 인계 | R1 | — |
| 26 | `Claude/results/process/HANDOVER_2026-06-10_ch1-textbook-rewrite.md` | 29 | Fable v2~v10(세부: 날짜 06-10) | 인계 | R1 | — |
| 27 | `Claude/results/process/HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md` | 43 | Fable v2~v10(세부: v2) | 인계 | R1 | — |
| 28 | `Claude/results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md` | 75 | Fable v2~v10(세부: 날짜 06-30) | 인계 | R1 | — |

### (iv) `Claude/docs/Fable_점검/*.md`

- 정의: Fable 이력 전수감사 8본(01·02·03·note A1~A5)
- 기대치(출처): 8·885줄(brief §4 · 1g) — 일치(줄수 정의 무관하게 합계 일치)
- 실측: **8 파일 · 885 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | 72 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | R1·R3·R6 | A9 |
| 2 | `Claude/docs/Fable_점검/FABLE_AUDIT_02_ch1ch2_content.md` | 41 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | — | §2.9 L198 미검독(02) |
| 3 | `Claude/docs/Fable_점검/FABLE_AUDIT_03_code_fitness.md` | 24 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | — | §2.9 L198 미검독(03) |
| 4 | `Claude/docs/Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md` | 188 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | R1 | note_A1 |
| 5 | `Claude/docs/Fable_점검/FABLE_AUDIT_note_A2_v5-v7.md` | 142 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | R1 | note_A2 |
| 6 | `Claude/docs/Fable_점검/FABLE_AUDIT_note_A3_v7-v9.md` | 159 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | R1 | note_A3 |
| 7 | `Claude/docs/Fable_점검/FABLE_AUDIT_note_A4_v9-v1011.md` | 127 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | R1 | note_A4 |
| 8 | `Claude/docs/Fable_점검/FABLE_AUDIT_note_A5_ch2-code.md` | 132 | 횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점) | 감사 | R1 | note_A5 |

### (iv-b) 추가 발견 — 감사 성격 md(iter_2 · AUD-01·AUD-03 · 유사 파일 정책 일관화)

- 정의(master 확정 정책): 「추가 발견」 = (a) 등재 파일의 형제(같은 계열 파일명) (b) 통제 문서(프로젝트 `CLAUDE.md`·마스터 플랜·INDEX 3본 — 정본 = §10.4)가 인용하는 파일 (c) 동명 폴더·동명이물 충돌 파일. 아래 12본은 (a)~(c) 중 하나에 해당하며 iter_1 에서 §8.3 계수에만 있었다. 잔여 `results/process/` 비-ledger·비-Result md 는 (a)~(c) 밖이라 §8.3 계수 유지(1.2 Step 3 토픽 한정에서 필요 시 열람).
- 실측: **12 파일 · 1674 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/results/process/FABLE_REAUDIT_C1_note.md` | 63 | v1.0.12(fable reaudit) | 감사 | — | (a) 형제 = (viii) `FABLE_REAUDIT_P*_RESULT` |
| 2 | `Claude/results/process/FABLE_REAUDIT_C2_note.md` | 65 | v1.0.12(fable reaudit) | 감사 | — | (a) |
| 3 | `Claude/results/process/FABLE_REAUDIT_C3_note.md` | 68 | v1.0.12(fable reaudit) | 감사 | — | (a) |
| 4 | `Claude/results/process/FABLE_REAUDIT_C4_note.md` | 68 | v1.0.12(fable reaudit) | 감사 | — | (a) |
| 5 | `Claude/results/process/FABLE_REAUDIT_C5_note.md` | 95 | v1.0.12(fable reaudit) | 감사 | — | (a) |
| 6 | `Claude/results/process/FABLE_REAUDIT_C6_note.md` | 111 | v1.0.12(fable reaudit) | 감사 | — | (a) |
| 7 | `Claude/results/process/V1014_AUDIT_ADJUDICATION.md` | 27 | v1.0.14 | 감사 | — | (a) 형제 = (ix) `V1014_TONE_AUDIT` |
| 8 | `Claude/results/process/V1014_CODE_MENTION_AUDIT.md` | 254 | v1.0.14 | 감사 | — | (b) 프로젝트 `CLAUDE.md` P3 #8 "`CODE_MENTION_AUDIT` 승계" 인용 |
| 9 | `Claude/results/process/V3_W4_PHYSICS_AUDIT.md` | 34 | Fable v2~v10(세부: v3) | 감사 | — | (a) 형제 = (vii) `V7_9x9x1x1_LEDGER`·`V8_LEDGER` 계열 |
| 10 | `Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md` | 301 | v1.0.23 | 감사 | — | (c) **동명 폴더 경고**: `docs/v1.0.23/results/comp_v23/` ≠ (ix) 의 `docs/v1.0.22/results/comp_v23/`(AUD-03) |
| 11 | `Claude/old/results/PROJECT_AUDIT_REPORT.md` | 333 | 구트랙 RB | 감사 | — | (a) 구트랙(old/) — (vii)·(viii) old/ 등재 정책과 일관 |
| 12 | `Claude/old/results/PROJECT_AUDIT_REPORT_v0.2.md` | 255 | 구트랙 RB | 감사 | — | (a) 구트랙(old/) |

### (iv-c) 추가 발견 — 감사·점검 계열(iter_3 · AUD-R2-01·02 · 정책 (a)(b)(c) 기계 적용)

- 정의: master 확정 「추가 발견」 정책 (a)(b)(b′)(c) = **§10.4 문안(정본)과 동일** — 여기 재서술하지 않는다(문안 불일치 방지, AUD-R3-02). 적용 결과 = `iter_3/policy_check.txt`(잔여 0).
- 실측: **21 파일 · 2537 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/results/process/V1010_INSPECT_draft_C1.md` | 105 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` — (ix) 행 86 `V1010_INSPECT_draft_C3` 형제 |
| 2 | `Claude/results/process/V1010_INSPECT_draft_C2.md` | 89 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 3 | `Claude/results/process/V1010_INSPECT_draft_O1.md` | 96 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 4 | `Claude/results/process/V1010_INSPECT_draft_O2.md` | 98 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 5 | `Claude/results/process/V1010_INSPECT_draft_O3.md` | 113 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 6 | `Claude/results/process/V1010_INSPECT_draft_S1.md` | 209 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 7 | `Claude/results/process/V1010_INSPECT_draft_S2.md` | 265 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 8 | `Claude/results/process/V1010_INSPECT_draft_S3.md` | 320 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*` |
| 9 | `Claude/results/process/V1010_INSPECT_UNION.md` | 55 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*`(통합) |
| 10 | `Claude/results/process/V1010_INSPECT_verify10.md` | 31 | v1.0.10 | 감사 | — | (a) 계열 `V1010_INSPECT_*`(검증) |
| 11 | `Claude/docs/v1.0.23/results/comp_v23/AUD_REPORT_v23.md` | 65 | v1.0.23 | 감사 | — | (c) 동명 폴더 `docs/v1.0.23/results/comp_v23/` md 전건 — (iv-b) 행 10 과 같은 폴더 |
| 12 | `Claude/old/Archive_oldtrack/COMPARISON_CLAUDE_canonical_vs_CODEX_v2.md` | 93 | 구트랙 RB | 감사 | — | (b) 마스터 플랜 §2.8 L184 인용 `COMPARISON_*` · (a) (vii) `REVIEW_LEDGER_*` 형제 · 동명이물 경고(구트랙 v2~v5 ≠ Fable v2~v5) |
| 13 | `Claude/old/Archive_oldtrack/COMPARISON_CLAUDE_v4_vs_CODEX_REBUILT.md` | 123 | 구트랙 RB | 감사 | — | (b)(a) — 동명이물 경고 |
| 14 | `Claude/old/Archive_oldtrack/COMPARISON_CLAUDE_v5_1_vs_CODEX_v4.md` | 124 | 구트랙 RB | 감사 | — | (b)(a) — 동명이물 경고 |
| 15 | `Claude/old/Archive_oldtrack/COMPARISON_CLAUDE_v5_2_vs_CODEX_v5.md` | 74 | 구트랙 RB | 감사 | — | (b)(a) — 동명이물 경고 |
| 16 | `Claude/old/Archive_oldtrack/COMPARISON_CLAUDE_v5_vs_CODEX_v3.md` | 77 | 구트랙 RB | 감사 | — | (b)(a) — 동명이물 경고 |
| 17 | `Claude/old/Archive_oldtrack/COMPARISON_CLAUDE_vs_CODEX_CH1.md` | 149 | 구트랙 RB | 감사 | — | (b)(a) — 동명이물 경고 |
| 18 | `Claude/results/process/V1017_REVIEW_COMPLETE.md` | 60 | v1.0.17 | 감사 | — | (b) `docs/INDEX.md`:94·:103 인용(v1.0.17 절 — 라인별 검토 완전 복원 기록) |
| 19 | `Claude/results/process/V1017_FIXLIST_CONSOLIDATED.md` | 122 | v1.0.17 | 감사 | — | (b) `docs/INDEX.md`:94 인용(v1.0.17 절 fix-list) |
| 20 | `Claude/results/MISSING_CONTENT_REVIEW.md` | 93 | 횡단 | 감사 | — | (b) `docs/INDEX.md`:193 인용 |
| 21 | `Claude/docs/v1.0.22/results/R1B_SWEEP_LIST.md` | 176 | v1.0.22 | 감사 | — | (b) `docs/INDEX.md`:39 인용(v1.0.22 절 — 구획 전환 스윕 전수 분류표 118건 · S-008 정정 근거) |

### (v) `CLOSING_v1.0.15.md`

- 정의: v1.0.15 버전 클로징(헌법 3종)
- 기대치(출처): 106줄(brief §4 · A10) → 실측 105(줄수 정의 −1)
- 실측: **1 파일 · 105 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | 105 | v1.0.15 | 클로징 | R1·R3 | A10 · docs/INDEX.md:127 "다음 버전 착수 전 필독" |

### (vi) INDEX 전건

- 정의: `docs/INDEX.md` · `plans/INDEX.md` · `docs/v*/results/INDEX_v*.md` 전건
- 기대치(출처): 197·65·139(+기타) — 실측 196·69·138 + `INDEX_v1022`·`INDEX_v23`·`INDEX_v24`×4·`INDEX_v25`×2
- 실측: **10 파일 · 982 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/INDEX.md` | 196 | 횡단 | INDEX | R1·R3(grep) | A2 · brief 197 → 실측 196(정의 −1) |
| 2 | `Claude/docs/v1.0.22/results/INDEX_v1022.md` | 146 | v1.0.22 | INDEX | — | — |
| 3 | `Claude/docs/v1.0.23/results/INDEX_v23.md` | 43 | v1.0.23 | INDEX | — | — |
| 4 | `Claude/docs/v1.0.24.1/results/INDEX_v24.md` | 63 | v1.0.24.1 | INDEX | — | 사본(고유본 = Claude/docs/v1.0.24/results/INDEX_v24.md) |
| 5 | `Claude/docs/v1.0.24/results/INDEX_v24.md` | 63 | v1.0.24 | INDEX | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/INDEX_v24.md · Claude/docs/v1.0.25/results/INDEX_v24.md · Claude/docs/v1.0.25.1/results/INDEX_v24.md) |
| 6 | `Claude/docs/v1.0.25.1/results/INDEX_v24.md` | 63 | v1.0.25.1 | INDEX | — | 사본(고유본 = Claude/docs/v1.0.24/results/INDEX_v24.md) |
| 7 | `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | 138 | v1.0.25.1 | INDEX | R2·R4b(부분) | brief 139 → 실측 138(정의 −1) · I-4 전문 정독 ; 사본(고유본 = Claude/docs/v1.0.25/results/INDEX_v25.md) |
| 8 | `Claude/docs/v1.0.25/results/INDEX_v24.md` | 63 | v1.0.25 | INDEX | — | 사본(고유본 = Claude/docs/v1.0.24/results/INDEX_v24.md) |
| 9 | `Claude/docs/v1.0.25/results/INDEX_v25.md` | 138 | v1.0.25 | INDEX | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/INDEX_v25.md) |
| 10 | `Claude/plans/INDEX.md` | 69 | 횡단 | INDEX | R1 | A3 · brief 65 → 실측 69: 스테일 표기(자체 L5–8)이나 v1.0.27 행 L10–13 이 추가돼 있음(I-3 정독 확정) — +4 는 실제 갱신 |

### (vii) ledger 전건

- 정의: `Claude/results/**/*LEDGER*.md` + `docs/v*/results/*LEDGER*.md` + (추가 발견) `old/**/*LEDGER*.md` 구트랙 · `docs/v1.0.20/results/STEP_LOG_P*.md`. 서지 원장 4본은 (xii) 에 계수(→ (xii))
- 기대치(출처): 30(results 2·process 26·research 2) + docs 측 미실측(brief §4 · §2.9 L201) — 실측: results 30 ✓(2·26·2, 1,075줄) + docs 측 12(REFERENCE 4 제외) + STEP_LOG 8 + old/ 31
- 실측: **81 파일 · 3698 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.20/results/STEP_LOG_P0.md` | 40 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 2 | `Claude/docs/v1.0.20/results/STEP_LOG_P1.md` | 32 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 3 | `Claude/docs/v1.0.20/results/STEP_LOG_P2.md` | 34 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 4 | `Claude/docs/v1.0.20/results/STEP_LOG_P3.md` | 32 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 5 | `Claude/docs/v1.0.20/results/STEP_LOG_P4.md` | 33 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 6 | `Claude/docs/v1.0.20/results/STEP_LOG_P5.md` | 31 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 7 | `Claude/docs/v1.0.20/results/STEP_LOG_P6.md` | 41 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 8 | `Claude/docs/v1.0.20/results/STEP_LOG_P7.md` | 66 | v1.0.20 | ledger | — | 추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약) |
| 9 | `Claude/docs/v1.0.20/results/V1020_EXECUTION_LEDGER.md` | 16 | v1.0.20 | ledger | — | — |
| 10 | `Claude/docs/v1.0.20/results/V1020_REFLEDGER_DRAFT_candidates.md` | 47 | v1.0.20 | 서지 원장(초안) | — | 추가 발견(패턴 `*LEDGER*` 매치 · 서지 원장 초안) |
| 11 | `Claude/docs/v1.0.20/results/V1020_REFLEDGER_DRAFT_existing.md` | 77 | v1.0.20 | 서지 원장(초안) | — | 추가 발견(패턴 `*LEDGER*` 매치 · 서지 원장 초안) |
| 12 | `Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md` | 19 | v1.0.21 | ledger | R3(grep) | — |
| 13 | `Claude/docs/v1.0.22/results/V1022_EXECUTION_LEDGER.md` | 24 | v1.0.22 | ledger | — | — |
| 14 | `Claude/docs/v1.0.23/results/V1023_EXECUTION_LEDGER.md` | 12 | v1.0.23 | ledger | — | — |
| 15 | `Claude/docs/v1.0.24.1/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | v1.0.24.1 | ledger | — | (xiii) 대상 · 계수는 (vii) ; 사본(고유본 = Claude/docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md) |
| 16 | `Claude/docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | v1.0.24 | ledger | — | (xiii) 대상 · 계수는 (vii) ; 고유본(사본 3: Claude/docs/v1.0.24.1/results/V1024_REFLECT_EXECUTION_LEDGER.md · Claude/docs/v1.0.25/results/V1024_REFLECT_EXECUTION_LEDGER.md · Claude/docs/v1.0.25.1/results/V1024_REFLECT_EXECUTION_LEDGER.md) |
| 17 | `Claude/docs/v1.0.25.1/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | v1.0.25.1 | ledger | — | (xiii) 대상 · 계수는 (vii) ; 사본(고유본 = Claude/docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md) |
| 18 | `Claude/docs/v1.0.25.1/results/V1025_CHANGE_LEDGER.md` | 157 | v1.0.25.1 | ledger | — | (viii) 정의에도 해당 · 계수는 (vii) ; 사본(고유본 = Claude/docs/v1.0.25/results/V1025_CHANGE_LEDGER.md) |
| 19 | `Claude/docs/v1.0.25/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | v1.0.25 | ledger | — | (xiii) 대상 · 계수는 (vii) ; 사본(고유본 = Claude/docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md) |
| 20 | `Claude/docs/v1.0.25/results/V1025_CHANGE_LEDGER.md` | 157 | v1.0.25 | ledger | — | (viii) 정의에도 해당 · 계수는 (vii) ; 고유본(사본 1: Claude/docs/v1.0.25.1/results/V1025_CHANGE_LEDGER.md) |
| 21 | `Claude/old/Archive_oldtrack/ASSUMPTION_LEDGER_v3.md` | 61 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 22 | `Claude/old/Archive_oldtrack/PHASE_DIAG_EXECUTION_LEDGER.md` | 24 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 23 | `Claude/old/Archive_oldtrack/PHASE_DIAG_SALVAGE_LEDGER.md` | 84 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 24 | `Claude/old/Archive_oldtrack/RB_EXECUTION_LEDGER.md` | 68 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 25 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH1_REWORK.md` | 60 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 26 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH1.md` | 181 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 27 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH2_FINE_REVIEW.md` | 41 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 28 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH2.md` | 46 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 29 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH3_FINE_REVIEW.md` | 40 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 30 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH3.md` | 43 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 31 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH4_FINE_REVIEW.md` | 35 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 32 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH4.md` | 46 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 33 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH5_FINE_REVIEW.md` | 33 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 34 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH5.md` | 42 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 35 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH6_DISSOLUTION.md` | 30 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 36 | `Claude/old/Archive_oldtrack/RB_LEDGER_CH6.md` | 43 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 37 | `Claude/old/Archive_oldtrack/RB_LEDGER_CODEX_REVIEW_FIX_2026-06-02.md` | 44 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 38 | `Claude/old/Archive_oldtrack/RB_LEDGER_INTEGRATION.md` | 55 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 39 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND_CLAUDE_rerun_5-29.md` | 85 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) ; 사본(고유본 = Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND.md — iter_2 AUD-12) |
| 40 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND_priorpass_superseded.md` | 57 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 41 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND.md` | 85 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) ; 고유본(사본 1: Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND_CLAUDE_rerun_5-29.md — iter_2 AUD-12) |
| 42 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_CHAPTER_VS_INTEGRATED.md` | 45 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 43 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_DEEP_PHYSICS.md` | 54 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 44 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_G1_G2_10PASS.md` | 99 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 45 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_G3_10PASS.md` | 34 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 46 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_v3_CH1.md` | 57 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 47 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_v4_CANONICAL_CH1.md` | 62 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 48 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_v5_3_10ROUND.md` | 55 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 49 | `Claude/old/results/PHASE_A_D_EXECUTION_LEDGER.md` | 31 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 50 | `Claude/old/results/PHASE_E_F_EXECUTION_LEDGER.md` | 51 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 51 | `Claude/old/v2/results/EXECUTION_LEDGER_v2.md` | 58 | 구트랙 RB | ledger | — | 구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5) |
| 52 | `Claude/results/process/PHASE_A0-A5_EXECUTION_LEDGER.md` | 16 | Fable v2~v10(세부: v2 이전 06-06 sec6-statmech, 추정) | ledger | — | — |
| 53 | `Claude/results/process/PHASE_CH3_EXECUTION_LEDGER.md` | 64 | Fable v2~v10(세부: v2 이전 06-07 ch3~5 overhaul, 추정) | ledger | — | — |
| 54 | `Claude/results/process/PHASE_CM_EXECUTION_LEDGER.md` | 41 | Fable v2~v10(세부: v2 이전 06-08 connective-masterequation, 추정) | ledger | — | — |
| 55 | `Claude/results/process/PHASE_DEEP_REVIEW_LEDGER.md` | 70 | Fable v2~v10(세부: 미상, 추정) | ledger | — | — |
| 56 | `Claude/results/process/PHASE_F_EXECUTION_LEDGER.md` | 31 | Fable v2~v10(세부: 미상 F0~F9, 추정) | ledger | — | — |
| 57 | `Claude/results/process/PHASE_FRR_EXECUTION_LEDGER.md` | 32 | Fable v2~v10(세부: 06-10 full-rereview, 추정) | ledger | — | — |
| 58 | `Claude/results/process/PHASE_MERGE_LEDGER.md` | 35 | Fable v2~v10(세부: v2 이전 06-09 merge, 추정) | ledger | — | — |
| 59 | `Claude/results/process/PHASE_R0-R5_EXECUTION_LEDGER.md` | 19 | Fable v2~v10(세부: 미상 R0~R9, 추정) | ledger | — | — |
| 60 | `Claude/results/process/PHASE_TBR_EXECUTION_LEDGER.md` | 72 | Fable v2~v10(세부: 06-10 textbook-rewrite, 추정) | ledger | — | — |
| 61 | `Claude/results/process/PHASE_V2_EXECUTION_LEDGER.md` | 106 | Fable v2~v10(세부: v2) | ledger | — | — |
| 62 | `Claude/results/process/PHASE_V5_EXECUTION_LEDGER.md` | 79 | Fable v2~v10(세부: v5) | ledger | — | — |
| 63 | `Claude/results/process/PHASE_V5RR_EXECUTION_LEDGER.md` | 22 | Fable v2~v10(세부: v5RR) | ledger | — | — |
| 64 | `Claude/results/process/PHASE_V6_EXECUTION_LEDGER.md` | 13 | Fable v2~v10(세부: v6) | ledger | — | — |
| 65 | `Claude/results/process/PHASE_W_EXECUTION_LEDGER.md` | 16 | Fable v2~v10(세부: v2 이전 06-06 register-revision, 추정) | ledger | — | — |
| 66 | `Claude/results/process/V1010_EXECUTION_LEDGER.md` | 20 | v1.0.10 | ledger | — | — |
| 67 | `Claude/results/process/V1011_EXECUTION_LEDGER.md` | 17 | v1.0.11 | ledger | — | — |
| 68 | `Claude/results/process/V1012_EXECUTION_LEDGER.md` | 18 | v1.0.12 | ledger | — | — |
| 69 | `Claude/results/process/V1013_EXECUTION_LEDGER.md` | 32 | v1.0.13 | ledger | — | — |
| 70 | `Claude/results/process/V1014_EXECUTION_LEDGER.md` | 40 | v1.0.14 | ledger | — | — |
| 71 | `Claude/results/process/V1015_EXECUTION_LEDGER.md` | 20 | v1.0.15 | ledger | — | — |
| 72 | `Claude/results/process/V1016_EXECUTION_LEDGER.md` | 21 | v1.0.16 | ledger | — | — |
| 73 | `Claude/results/process/V1017_EXECUTION_LEDGER.md` | 26 | v1.0.17 | ledger | — | — |
| 74 | `Claude/results/process/V1018_EXECUTION_LEDGER.md` | 33 | v1.0.18.1·v1.0.18.2(공통 — 추정) | ledger | — | `:30–31` 두 개정(18.1 증판·18.2 코드) 한 원장 |
| 75 | `Claude/results/process/V1019_EXECUTION_LEDGER.md` | 56 | v1.0.19 | ledger | — | — |
| 76 | `Claude/results/process/V7_9x9x1x1_LEDGER.md` | 43 | Fable v2~v10(세부: v7) | ledger | — | — |
| 77 | `Claude/results/process/V8_LEDGER.md` | 35 | Fable v2~v10(세부: v8) | ledger | — | — |
| 78 | `Claude/results/research/CH2_v3/CH2_v3_LEDGER.md` | 21 | Fable v2~v10(세부: Ch2 v3 survey 06-30) | ledger | — | — |
| 79 | `Claude/results/research/radius/RADIUS_LEDGER.md` | 39 | Fable v2~v10(세부: radius survey 06-30, 추정) | ledger | — | — |
| 80 | `Claude/results/V1024_EXECUTION_LEDGER.md` | 14 | v1.0.24 | ledger | — | §2.8 L179 12-col 실례 |
| 81 | `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md` | 24 | v1.0.24.1 | ledger | — | §2.8 L179 12-col 실례 · 귀속 근거 `docs/INDEX.md`:21(v1.0.24.1 리비전 이력) |

### (vii-b) 추가 발견 — 구트랙 규약·통합 ledger(iter_3 · AUD-R2-03·AUD-R2-10)

- 정의: (b′) 등재 문서가 binding·입력으로 명시 인용하는 규약(charter) 문서 + (i-b) 에서 종류 정정으로 이동한 통합 ledger. 작업 챕터 1.3(유효 결정·제약 등록부)의 구트랙 원천.
- 실측: **4 파일 · 694 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/old/Archive_oldtrack/RB_AL_MASTER.md` | 139 | 구트랙 RB | ledger(통합 Assumption Ledger·Notation Bible) | — | (i-b) 에서 이동(AUD-R2-03) · 실물 헤더 L1 · glob `*MASTER*` 오매치 · 1.3 구트랙 원천 · `:3` 입력 = `RB_CHARTER.md` |
| 2 | `Claude/old/Archive_oldtrack/RB_CHARTER.md` | 105 | 구트랙 RB | 기타(규약 charter) | — | (b′) 등재 문서 `RB_AL_MASTER.md`:3 가 입력으로 명시 인용 — 1.3 원천 후보 |
| 3 | `Claude/old/Archive_oldtrack/CHARTER_v3.md` | 65 | 구트랙 RB | 기타(규약 charter) | — | (a) `CHARTER_*` 계열 — 1.3 원천 후보 |
| 4 | `Claude/old/v2/results/CHARTER_v2.md` | 385 | 구트랙 RB | 기타(규약 charter) | — | (b′) 등재 ledger `old/v2/results/EXECUTION_LEDGER_v2.md`:4 "Charter binding" 인용 — 1.3 원천 후보 · old/v2 동명이물 경고 |

### (vii-c) 추가 발견 — `FITTING_GUIDE` 규약 기록(hash 고유 내용 8본 · iter_4 · AUD-R3-06)

- 정의: 정책 (b) 의 "가이드" 제외를 정정 — `docs/INDEX.md` 가 `FITTING_GUIDE.md` 를 규약 기록(B-006 U_j 평가 규약 :62 · fit-n 4단 사다리 :113 · 방향규약·S0–S5 :164 등)으로 서술하므로 1.3 유효 결정·제약 등록부의 원천이다. 버전 폴더 19(폴더당 1본 · v1.0.10~v1.0.25.1) 19본 중 hash 고유 내용 = 4 그룹 고유본(§4 #1·#110·#132·#146) + 단독 4 = 8본. `CODE_GUIDE_v24.md` 는 스테일 코드 기록(7.x 소관)으로 계수만.
- 실측: **8 파일 · 854 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.10/FITTING_GUIDE.md` | 46 | v1.0.10 | 기타(가이드 — 규약 기록) | — | 고유본(사본 1: Claude/docs/v1.0.11/FITTING_GUIDE.md — §4 #146) · `docs/INDEX.md` 행 근거 미발견(v1.0.10 절 미기재) |
| 2 | `Claude/docs/v1.0.12/FITTING_GUIDE.md` | 98 | v1.0.12 | 기타(가이드 — 규약 기록) | — | hash 단독 · `docs/INDEX.md`:164 — tier 표·5-Phase round-trip·★방향규약 §0·S0–S5 식별 사슬·울타리 16(D3 선별 복원) — 1.4 S0–S5 유실 항목의 문서 실물 |
| 3 | `Claude/docs/v1.0.13/FITTING_GUIDE.md` | 99 | v1.0.13 | 기타(가이드 — 규약 기록) | — | hash 단독 · `docs/INDEX.md`:151 — §0 전극 인지 규약·ν≳10 정정·S0–S5 승계 |
| 4 | `Claude/docs/v1.0.14/FITTING_GUIDE.md` | 99 | v1.0.14 | 기타(가이드 — 규약 기록) | — | 고유본(사본 1: Claude/docs/v1.0.15/FITTING_GUIDE.md — §4 #132) · `docs/INDEX.md`:138 — Ω 하한 ≥0·χ tier·식별 트랩·문턱 |
| 5 | `Claude/docs/v1.0.16/FITTING_GUIDE.md` | 115 | v1.0.16 | 기타(가이드 — 규약 기록) | — | 고유본(사본 2: Claude/docs/v1.0.17/FITTING_GUIDE.md · Claude/docs/v1.0.18.1/FITTING_GUIDE.md — §4 #110) · `docs/INDEX.md`:113 — §1.5 fit-n·4단 사다리·n(T)→config(CLOSING Part 4 집행) |
| 6 | `Claude/docs/v1.0.18.2/FITTING_GUIDE.md` | 125 | v1.0.18.2 | 기타(가이드 — 규약 기록) | — | hash 단독 · `docs/INDEX.md`:89 — §1.6 vib θ_E 규약 |
| 7 | `Claude/docs/v1.0.19/FITTING_GUIDE.md` | 135 | v1.0.19 | 기타(가이드 — 규약 기록) | — | hash 단독 · `docs/INDEX.md`:75 — x̄ 진입점·return_terms·Phase D scope 정직·잔차 정규화 |
| 8 | `Claude/docs/v1.0.20/FITTING_GUIDE.md` | 137 | v1.0.20 | 기타(가이드 — 규약 기록) | — | 고유본(사본 7: Claude/docs/v1.0.21 · v1.0.22 · v1.0.23 · v1.0.24 · v1.0.24.1 · v1.0.25 · v1.0.25.1 의 FITTING_GUIDE.md — §4 #1) · `docs/INDEX.md`:62 — **B-006 U_j 평가 규약**((−ΔH+TΔS)/F 환산값 필수·표시 반올림 입력 금지) — 1.3 규약 원천 |

### (viii) 각 버전 MERGE_READINESS·CHANGE_LOG·PHASE_*_RESULT·AUDIT_LINEAGE·DATA_ADDENDUM·DOC_EDIT_REPORT·T13_T14·CASCADE_TODO·ARCHIVE_NOTE

- 정의: 파일명 패턴 매치 `.md` 전건(`docs/`·`results/`·`old/`). `*CHANGE_LEDGER*` 는 (vii) 에 계수(→ (vii)) · `INDEX_v*` → (vi) · `HANDOVER*` → (iii) · `handoffs/**/fix_change_log.md` → (xv). 추가 발견 = `RESULT_P*`·비-`PHASE_` `*_RESULT*`·`V1025_1_TOUCHUP_NOTE`
- 기대치(출처): 미실측(brief §4)
- 실측: **167 파일 · 14858 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.20/results/RESULT_P0_setup.md` | 43 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 2 | `Claude/docs/v1.0.20/results/RESULT_P1_references.md` | 41 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 3 | `Claude/docs/v1.0.20/results/RESULT_P2_part0.md` | 40 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 4 | `Claude/docs/v1.0.20/results/RESULT_P3_graphite.md` | 40 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 5 | `Claude/docs/v1.0.20/results/RESULT_P4_lco.md` | 42 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 6 | `Claude/docs/v1.0.20/results/RESULT_P5_ch2.md` | 44 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 7 | `Claude/docs/v1.0.20/results/RESULT_P6_convention.md` | 44 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 8 | `Claude/docs/v1.0.20/results/RESULT_P7_review.md` | 45 | v1.0.20 | Result | — | 추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약) |
| 9 | `Claude/docs/v1.0.20/results/V1020_CHANGE_LOG.md` | 43 | v1.0.20 | ledger | — | — |
| 10 | `Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md` | 37 | v1.0.21 | ledger | R3(grep) | — |
| 11 | `Claude/docs/v1.0.22/results/AUDIT_LINEAGE_v19_v22.md` | 59 | v1.0.22 | 감사 | — | — |
| 12 | `Claude/docs/v1.0.22/results/MERGE_READINESS.md` | 204 | v1.0.22 | 감사(머지 판정) | — | — |
| 13 | `Claude/docs/v1.0.22/results/V1022_CHANGE_LOG.md` | 49 | v1.0.22 | ledger | — | — |
| 14 | `Claude/docs/v1.0.23/results/MERGE_READINESS_v23.md` | 52 | v1.0.23 | 감사(머지 판정) | — | — |
| 15 | `Claude/docs/v1.0.23/results/PHASE_P1_RESULT.md` | 112 | v1.0.23 | Result | — | — |
| 16 | `Claude/docs/v1.0.23/results/PHASE_P2_RESULT.md` | 114 | v1.0.23 | Result | — | — |
| 17 | `Claude/docs/v1.0.23/results/PHASE_P3_RESULT.md` | 102 | v1.0.23 | Result | — | — |
| 18 | `Claude/docs/v1.0.23/results/PHASE_P5_RESULT.md` | 95 | v1.0.23 | Result | — | — |
| 19 | `Claude/docs/v1.0.23/results/V1023_CHANGE_LOG.md` | 17 | v1.0.23 | ledger | — | — |
| 20 | `Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md` | 40 | v1.0.24.1 | 기타(폴더 지위) | — | 동결 아카이브 권위 기록(docs/INDEX.md:25) |
| 21 | `Claude/docs/v1.0.24.1/results/MERGE_READINESS_v24.md` | 59 | v1.0.24.1 | 감사(머지 판정) | — | 사본(고유본 = Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md) |
| 22 | `Claude/docs/v1.0.24.1/results/PHASE_R0_RESULT.md` | 44 | v1.0.24.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R0_RESULT.md) |
| 23 | `Claude/docs/v1.0.24.1/results/PHASE_R1_RESULT.md` | 53 | v1.0.24.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md) |
| 24 | `Claude/docs/v1.0.24.1/results/PHASE_R2_RESULT.md` | 49 | v1.0.24.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md) |
| 25 | `Claude/docs/v1.0.24.1/results/PHASE_R3_RESULT.md` | 39 | v1.0.24.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md) |
| 26 | `Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md` | 59 | v1.0.24 | 감사(머지 판정) | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/MERGE_READINESS_v24.md · Claude/docs/v1.0.25/results/MERGE_READINESS_v24.md · Claude/docs/v1.0.25.1/results/MERGE_READINESS_v24.md) |
| 27 | `Claude/docs/v1.0.24/results/PHASE_R0_RESULT.md` | 44 | v1.0.24 | Result | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/PHASE_R0_RESULT.md · Claude/docs/v1.0.25/results/PHASE_R0_RESULT.md · Claude/docs/v1.0.25.1/results/PHASE_R0_RESULT.md) |
| 28 | `Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md` | 53 | v1.0.24 | Result | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/PHASE_R1_RESULT.md · Claude/docs/v1.0.25/results/PHASE_R1_RESULT.md · Claude/docs/v1.0.25.1/results/PHASE_R1_RESULT.md) |
| 29 | `Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md` | 49 | v1.0.24 | Result | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/PHASE_R2_RESULT.md · Claude/docs/v1.0.25/results/PHASE_R2_RESULT.md · Claude/docs/v1.0.25.1/results/PHASE_R2_RESULT.md) |
| 30 | `Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md` | 39 | v1.0.24 | Result | — | 고유본(사본 3: Claude/docs/v1.0.24.1/results/PHASE_R3_RESULT.md · Claude/docs/v1.0.25/results/PHASE_R3_RESULT.md · Claude/docs/v1.0.25.1/results/PHASE_R3_RESULT.md) |
| 31 | `Claude/docs/v1.0.25.1/ARCHIVE_NOTE.md` | 118 | v1.0.25.1 | 기타(폴더 지위) | R4b(부분) | v1.0.25 절 S1~S6 추기본(INDEX_v25.md:93) · v1.0.25 폴더본(109)과 hash 상이 |
| 32 | `Claude/docs/v1.0.25.1/results/MERGE_READINESS_v24.md` | 59 | v1.0.25.1 | 감사(머지 판정) | — | 사본(고유본 = Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md) |
| 33 | `Claude/docs/v1.0.25.1/results/MERGE_READINESS_v25.md` | 204 | v1.0.25.1 | 감사(머지 판정) | — | 사본(고유본 = Claude/docs/v1.0.25/results/MERGE_READINESS_v25.md) |
| 34 | `Claude/docs/v1.0.25.1/results/PHASE_R0_RESULT.md` | 44 | v1.0.25.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R0_RESULT.md) |
| 35 | `Claude/docs/v1.0.25.1/results/PHASE_R1_RESULT.md` | 53 | v1.0.25.1 | Result | R3(grep) | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md) |
| 36 | `Claude/docs/v1.0.25.1/results/PHASE_R2_RESULT.md` | 49 | v1.0.25.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md) |
| 37 | `Claude/docs/v1.0.25.1/results/PHASE_R3_RESULT.md` | 39 | v1.0.25.1 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md) |
| 38 | `Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md` | 61 | v1.0.25.1 | 기타(검증 기록) | R2 | 추가 발견 — A4 · docs/INDEX.md:12 "현행 권위 기록" |
| 39 | `Claude/docs/v1.0.25.1/results/V1025_DATA_ADDENDUM.md` | 291 | v1.0.25.1 | 기타(데이터 정정 addendum) | — | 사본(고유본 = Claude/docs/v1.0.25/results/V1025_DATA_ADDENDUM.md) |
| 40 | `Claude/docs/v1.0.25.1/results/V1025_DOC_CASCADE_TODO.md` | 182 | v1.0.25.1 | 기타(지시서) | — | 사본(고유본 = Claude/docs/v1.0.25/results/V1025_DOC_CASCADE_TODO.md) |
| 41 | `Claude/docs/v1.0.25.1/results/V1025_DOC_EDIT_REPORT.md` | 312 | v1.0.25.1 | Result(집행 보고) | R4b(부분) | 사본(고유본 = Claude/docs/v1.0.25/results/V1025_DOC_EDIT_REPORT.md) |
| 42 | `Claude/docs/v1.0.25.1/results/V1025_T13_T14_REPORT.md` | 487 | v1.0.25.1 | Result(집행 보고) | R4b(부분) | 사본(고유본 = Claude/docs/v1.0.25/results/V1025_T13_T14_REPORT.md) |
| 43 | `Claude/docs/v1.0.25/ARCHIVE_NOTE.md` | 109 | v1.0.25 | 기타(폴더 지위) | — | — |
| 44 | `Claude/docs/v1.0.25/results/MERGE_READINESS_v24.md` | 59 | v1.0.25 | 감사(머지 판정) | — | 사본(고유본 = Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md) |
| 45 | `Claude/docs/v1.0.25/results/MERGE_READINESS_v25.md` | 204 | v1.0.25 | 감사(머지 판정) | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/MERGE_READINESS_v25.md) |
| 46 | `Claude/docs/v1.0.25/results/PHASE_R0_RESULT.md` | 44 | v1.0.25 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R0_RESULT.md) |
| 47 | `Claude/docs/v1.0.25/results/PHASE_R1_RESULT.md` | 53 | v1.0.25 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md) |
| 48 | `Claude/docs/v1.0.25/results/PHASE_R2_RESULT.md` | 49 | v1.0.25 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md) |
| 49 | `Claude/docs/v1.0.25/results/PHASE_R3_RESULT.md` | 39 | v1.0.25 | Result | — | 사본(고유본 = Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md) |
| 50 | `Claude/docs/v1.0.25/results/V1025_DATA_ADDENDUM.md` | 291 | v1.0.25 | 기타(데이터 정정 addendum) | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/V1025_DATA_ADDENDUM.md) |
| 51 | `Claude/docs/v1.0.25/results/V1025_DOC_CASCADE_TODO.md` | 182 | v1.0.25 | 기타(지시서) | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/V1025_DOC_CASCADE_TODO.md) |
| 52 | `Claude/docs/v1.0.25/results/V1025_DOC_EDIT_REPORT.md` | 312 | v1.0.25 | Result(집행 보고) | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/V1025_DOC_EDIT_REPORT.md) |
| 53 | `Claude/docs/v1.0.25/results/V1025_T13_T14_REPORT.md` | 487 | v1.0.25 | Result(집행 보고) | — | 고유본(사본 1: Claude/docs/v1.0.25.1/results/V1025_T13_T14_REPORT.md) |
| 54 | `Claude/old/Archive_oldtrack/PHASE_0_foundation_RESULT.md` | 54 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 55 | `Claude/old/Archive_oldtrack/PHASE_1_2_ch1_grounding_RESULT.md` | 48 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 56 | `Claude/old/Archive_oldtrack/PHASE_1_ch1_RESULT.md` | 46 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 57 | `Claude/old/Archive_oldtrack/PHASE_1B_ch1_noskip_audit_RESULT.md` | 99 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 58 | `Claude/old/Archive_oldtrack/PHASE_A_consolidated_adversarial_review_RESULT.md` | 82 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 59 | `Claude/old/Archive_oldtrack/PHASE_B_crosschapter_build_review_RESULT.md` | 65 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 60 | `Claude/old/Archive_oldtrack/PHASE_DIAG_INTENT_GAP_RESULT.md` | 160 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 61 | `Claude/old/results/PHASE_A_ver5_master_structure_RESULT.md` | 319 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 62 | `Claude/old/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT_ADDENDUM_1.md` | 52 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 63 | `Claude/old/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` | 299 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 64 | `Claude/old/results/PHASE_C_chapter1_mapping_and_feedback_note_RESULT.md` | 213 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 65 | `Claude/old/results/PHASE_D_jcp_ref6_7_methodology_RESULT.md` | 296 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 66 | `Claude/old/results/PHASE_E0_foundation_reset_charter_RESULT_ADDENDUM_1.md` | 120 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 67 | `Claude/old/results/PHASE_E0_foundation_reset_charter_RESULT_ADDENDUM_2.md` | 104 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 68 | `Claude/old/results/PHASE_E0_foundation_reset_charter_RESULT.md` | 463 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 69 | `Claude/old/results/PHASE_E1_spine_redesign_RESULT.md` | 399 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 70 | `Claude/old/results/PHASE_E2_intro_notation_RESULT.md` | 250 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 71 | `Claude/old/results/PHASE_E3_effective_transition_potential_separation_RESULT.md` | 158 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 72 | `Claude/old/results/PHASE_E4_charge_balance_central_equation_RESULT.md` | 184 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 73 | `Claude/old/v2/results/PHASE_0_v2_FOUNDATION_RESULT.md` | 189 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 74 | `Claude/old/v2/results/PHASE_1_v2_BODY_INTRO_RESULT.md` | 59 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 75 | `Claude/old/v2/results/PHASE_10_v2_ICA_TAIL_RESULT.md` | 55 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 76 | `Claude/old/v2/results/PHASE_11_v2_FITTING_EXPRESSION_RESULT.md` | 69 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 77 | `Claude/old/v2/results/PHASE_12_v2_SUMMARY_RESULT.md` | 90 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 78 | `Claude/old/v2/results/PHASE_2_v2_NOTATION_RESULT.md` | 44 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 79 | `Claude/old/v2/results/PHASE_3_v2_STAGING_RESULT.md` | 38 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 80 | `Claude/old/v2/results/PHASE_4_v2_EFFECTIVE_BARRIER_RESULT.md` | 57 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 81 | `Claude/old/v2/results/PHASE_5_v2_EQUILIBRIUM_ERF_RESULT.md` | 50 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 82 | `Claude/old/v2/results/PHASE_6_v2_ARRHENIUS_RESULT.md` | 48 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 83 | `Claude/old/v2/results/PHASE_7_v2_KINETICS_RESULT.md` | 47 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 84 | `Claude/old/v2/results/PHASE_8_v2_VOLTERRA_RESULT.md` | 45 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 85 | `Claude/old/v2/results/PHASE_9_v2_RATIO_SUBSTITUTION_RESULT.md` | 62 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 86 | `Claude/old/v2/results/PHASE_AUDIT_RALPH_WIGGUM_v2_RESULT.md` | 190 | 구트랙 RB | Result | — | 구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5) |
| 87 | `Claude/results/builds/ch1v10/PHASE_CH1v10_RESULT.md` | 33 | Fable v2~v10(세부: v10) | Result | — | — |
| 88 | `Claude/results/PHASE_FB0_RESULT.md` | 67 | v1.0.24.1 | Result | — | — |
| 89 | `Claude/results/PHASE_FB1_RESULT.md` | 65 | v1.0.24.1 | Result | — | — |
| 90 | `Claude/results/PHASE_FB2_RESULT.md` | 49 | v1.0.24.1 | Result | — | — |
| 91 | `Claude/results/PHASE_FB3_RESULT.md` | 74 | v1.0.24.1 | Result | — | — |
| 92 | `Claude/results/PHASE_FB4_RESULT.md` | 53 | v1.0.24.1 | Result | — | — |
| 93 | `Claude/results/PHASE_FB5_RESULT.md` | 54 | v1.0.24.1 | Result | — | — |
| 94 | `Claude/results/PHASE_FB6_RESULT.md` | 52 | v1.0.24.1 | Result | — | — |
| 95 | `Claude/results/PHASE_FB7_RESULT.md` | 75 | v1.0.24.1 | Result | — | — |
| 96 | `Claude/results/PHASE_FB8_RESULT.md` | 81 | v1.0.24.1 | Result | — | — |
| 97 | `Claude/results/PHASE_FB9_RESULT.md` | 66 | v1.0.24.1 | Result | — | — |
| 98 | `Claude/results/PHASE_V0_RESULT.md` | 47 | v1.0.24(추정: completeness-validation V0~V3) | Result | — | — |
| 99 | `Claude/results/PHASE_V1_RESULT.md` | 45 | v1.0.24(추정: completeness-validation V0~V3) | Result | — | — |
| 100 | `Claude/results/PHASE_V2_RESULT.md` | 74 | v1.0.24(추정: completeness-validation V0~V3) | Result | — | — |
| 101 | `Claude/results/PHASE_V2B_RESULT.md` | 55 | v1.0.24(추정: completeness-validation V0~V3) | Result | — | — |
| 102 | `Claude/results/PHASE_V2C_RESULT.md` | 55 | v1.0.24(추정: completeness-validation V0~V3) | Result | — | — |
| 103 | `Claude/results/PHASE_V3_RESULT.md` | 49 | v1.0.24(추정: completeness-validation V0~V3) | Result | — | — |
| 104 | `Claude/results/process/CH3_D2B_OVERHAUL_RESULT.md` | 44 | Fable v2~v10(세부: v2 이전 06-07 ch3~5 overhaul, 추정) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 105 | `Claude/results/process/CH4_D2B_OVERHAUL_RESULT.md` | 41 | Fable v2~v10(세부: v2 이전 06-07 ch3~5 overhaul, 추정) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 106 | `Claude/results/process/CH5_D2B_OVERHAUL_RESULT.md` | 56 | Fable v2~v10(세부: v2 이전 06-07 ch3~5 overhaul, 추정) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 107 | `Claude/results/process/FABLE_REAUDIT_P0_P1_RESULT.md` | 74 | v1.0.12(fable reaudit) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 108 | `Claude/results/process/FABLE_REAUDIT_P2_P3_RESULT.md` | 23 | v1.0.12(fable reaudit) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 109 | `Claude/results/process/FABLE_REAUDIT_P4_RESULT.md` | 31 | v1.0.12(fable reaudit) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 110 | `Claude/results/process/GRAPH_VERIFY_RESULT.md` | 69 | v1.0.10 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 111 | `Claude/results/process/PHASE_2TRACK_RESULT.md` | 46 | Fable v2~v10(세부: v9 2track, 추정) | Result | — | — |
| 112 | `Claude/results/process/PHASE_A0_design_RESULT.md` | 40 | Fable v2~v10(세부: v2 이전 06-06 sec6-statmech, 추정) | Result | — | — |
| 113 | `Claude/results/process/PHASE_A1_eq-linebreak_RESULT.md` | 39 | Fable v2~v10(세부: v2 이전 06-06 sec6-statmech, 추정) | Result | — | — |
| 114 | `Claude/results/process/PHASE_A3-A5_statmech-section_RESULT.md` | 38 | Fable v2~v10(세부: v2 이전 06-06 sec6-statmech, 추정) | Result | — | — |
| 115 | `Claude/results/process/PHASE_CM_ch1_RESULT.md` | 51 | Fable v2~v10(세부: v2 이전 06-08 connective-masterequation, 추정) | Result | — | — |
| 116 | `Claude/results/process/PHASE_CM_ch2_RESULT.md` | 55 | Fable v2~v10(세부: v2 이전 06-08 connective-masterequation, 추정) | Result | — | — |
| 117 | `Claude/results/process/PHASE_CM2_ch2-deepening_RESULT.md` | 46 | Fable v2~v10(세부: v2 이전 06-08 connective-masterequation, 추정) | Result | — | — |
| 118 | `Claude/results/process/PHASE_F0_inventory-design_RESULT.md` | 57 | Fable v2~v10(세부: 미상 F0~F9, 추정) | Result | — | — |
| 119 | `Claude/results/process/PHASE_F1-F5_form-edits_RESULT.md` | 45 | Fable v2~v10(세부: 미상 F0~F9, 추정) | Result | — | — |
| 120 | `Claude/results/process/PHASE_F6_crossmodel_RESULT.md` | 45 | Fable v2~v10(세부: 미상 F0~F9, 추정) | Result | — | — |
| 121 | `Claude/results/process/PHASE_F7_change-history-audit_RESULT.md` | 66 | Fable v2~v10(세부: 미상 F0~F9, 추정) | Result | — | — |
| 122 | `Claude/results/process/PHASE_F8_textbook-register-polish_RESULT.md` | 35 | Fable v2~v10(세부: 미상 F0~F9, 추정) | Result | — | — |
| 123 | `Claude/results/process/PHASE_F9_content-preservation-audit_RESULT.md` | 60 | Fable v2~v10(세부: 미상 F0~F9, 추정) | Result | — | — |
| 124 | `Claude/results/process/PHASE_FRR_ch1_RESULT.md` | 40 | Fable v2~v10(세부: 06-10 full-rereview, 추정) | Result | — | — |
| 125 | `Claude/results/process/PHASE_FRR_ch3_RESULT.md` | 35 | Fable v2~v10(세부: 06-10 full-rereview, 추정) | Result | — | — |
| 126 | `Claude/results/process/PHASE_FRR_ch4_RESULT.md` | 31 | Fable v2~v10(세부: 06-10 full-rereview, 추정) | Result | — | — |
| 127 | `Claude/results/process/PHASE_FRR_ROUNDS_RESULT.md` | 106 | Fable v2~v10(세부: 06-10 full-rereview, 추정) | Result | — | — |
| 128 | `Claude/results/process/PHASE_G_sec8-10-comprehension_RESULT.md` | 29 | Fable v2~v10(세부: v2 이전 06-06 sec8-10, 추정) | Result | — | — |
| 129 | `Claude/results/process/PHASE_MERGE_RESULT.md` | 40 | Fable v2~v10(세부: v2 이전 06-09 merge, 추정) | Result | — | — |
| 130 | `Claude/results/process/PHASE_R0_convention-lock_RESULT.md` | 60 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 131 | `Claude/results/process/PHASE_R1_thermo_RESULT.md` | 51 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 132 | `Claude/results/process/PHASE_R2_kinetics_RESULT.md` | 46 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 133 | `Claude/results/process/PHASE_R3_synth_RESULT.md` | 39 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 134 | `Claude/results/process/PHASE_R4_refs_RESULT.md` | 42 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 135 | `Claude/results/process/PHASE_R5_verify_RESULT.md` | 52 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 136 | `Claude/results/process/PHASE_R6_section-convergence_RESULT.md` | 46 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 137 | `Claude/results/process/PHASE_R7_iterate-until-clean_RESULT.md` | 47 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 138 | `Claude/results/process/PHASE_R8_final-adversarial_RESULT.md` | 46 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 139 | `Claude/results/process/PHASE_R9_codex-crossmodel_RESULT.md` | 40 | Fable v2~v10(세부: 미상 R0~R9, 추정) | Result | — | — |
| 140 | `Claude/results/process/PHASE_REWORK_RESULT.md` | 38 | Fable v2~v10(세부: v10 rework, 추정) | Result | — | — |
| 141 | `Claude/results/process/PHASE_TBR_ch1_RESULT.md` | 13 | Fable v2~v10(세부: 06-10 textbook-rewrite, 추정) | Result | — | — |
| 142 | `Claude/results/process/PHASE_TBR_ROUNDS_RESULT.md` | 68 | Fable v2~v10(세부: 06-10 textbook-rewrite, 추정) | Result | — | — |
| 143 | `Claude/results/process/PHASE_TXB_ch1_RESULT.md` | 40 | Fable v2~v10(세부: v2 이전 06-06 textbook-form, 추정) | Result | — | — |
| 144 | `Claude/results/process/PHASE_TXB_ch2_RESULT.md` | 39 | Fable v2~v10(세부: v2 이전 06-06 textbook-form, 추정) | Result | — | — |
| 145 | `Claude/results/process/PHASE_V2_ch1_RESULT.md` | 51 | Fable v2~v10(세부: v2) | Result | — | — |
| 146 | `Claude/results/process/PHASE_V2_ROUNDS_RESULT.md` | 388 | Fable v2~v10(세부: v2) | Result | — | — |
| 147 | `Claude/results/process/PHASE_V5_RESULT.md` | 53 | Fable v2~v10(세부: v5) | Result | — | — |
| 148 | `Claude/results/process/PHASE_V5RR_ROUNDS_RESULT.md` | 175 | Fable v2~v10(세부: v5RR) | Result | — | — |
| 149 | `Claude/results/process/PHASE_V6_ROUNDS_RESULT.md` | 59 | Fable v2~v10(세부: v6) | Result | — | — |
| 150 | `Claude/results/process/PHASE_W_register-revision_RESULT.md` | 43 | Fable v2~v10(세부: v2 이전 06-06 register-revision, 추정) | Result | — | — |
| 151 | `Claude/results/process/PHASE8_v7_FINAL_RESULT.md` | 54 | Fable v2~v10(세부: v7) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 152 | `Claude/results/process/PHASE8_v8_FINAL_RESULT.md` | 51 | Fable v2~v10(세부: v8) | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 153 | `Claude/results/process/V1010_P1_code-audit_RESULT.md` | 445 | v1.0.10 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 154 | `Claude/results/process/V1010_P2_ch1_RESULT.md` | 83 | v1.0.10 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 155 | `Claude/results/process/V1010_P3_ch2_RESULT.md` | 54 | v1.0.10 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 156 | `Claude/results/process/V1010_P4_code-revision_RESULT.md` | 58 | v1.0.10 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 157 | `Claude/results/process/V1010_P5_final-check_RESULT.md` | 51 | v1.0.10 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 158 | `Claude/results/process/V1015_P1_anchor_RESULT.md` | 70 | v1.0.15 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 159 | `Claude/results/process/V1015_P3_RESULT.md` | 55 | v1.0.15 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 160 | `Claude/results/process/V1015_P4_RESULT.md` | 49 | v1.0.15 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 161 | `Claude/results/process/V1015_P5_RESULT.md` | 46 | v1.0.15 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 162 | `Claude/results/process/V1015_P6_RESULT.md` | 32 | v1.0.15 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 163 | `Claude/results/process/V1015_P7_RESULT.md` | 39 | v1.0.15 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 164 | `Claude/results/research/CH2_v3/PHASE_CH2v3_RESULT.md` | 46 | Fable v2~v10(세부: Ch2 v3 survey 06-30) | Result | — | — |
| 165 | `Claude/results/research/radius/PHASE_RADIUS_RESULT.md` | 18 | Fable v2~v10(세부: radius survey 06-30, 추정) | Result | — | — |
| 166 | `Claude/results/V1013_RESULT.md` | 50 | v1.0.13 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |
| 167 | `Claude/results/V1014_RESULT.md` | 52 | v1.0.14 | Result | — | 추가 발견(`PHASE_*_RESULT` 패턴 밖 Result) |

### (viii-b) 추가 발견 — Result 성격 md(iter_2 · AUD-01)

- 정의: (i) 행 74·76 계획서(`v1010-problem-inspection`·`v1010-handover-integrity-inspection`)의 집행 보고 실물. (ix) 행 86 `V1010_INSPECT_draft_C3` 와 같은 점검 산출.
- 실측: **2 파일 · 100 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.10/V1010_PROBLEM_REPORT.md` | 55 | v1.0.10 | Result(점검 보고) | — | (i) 행 74 계획서의 Result |
| 2 | `Claude/docs/v1.0.10/V1010_HANDOVER_INTEGRITY_REPORT.md` | 45 | v1.0.10 | Result(점검 보고) | — | (i) 행 76 계획서의 Result |

### (viii-c) 추가 발견 — 경쟁 저작 결정 기록 2본(iter_3b · 정책 (b) 잔여 해소)

- 정의: `INDEX_v25.md` 가 v1.0.25 저작 이력으로 인용하는 `results/comp_R1/` 의 결정 기록(체리픽 결정·저자 brief). `iter_3/policy_check.txt` (b) 잔여 2 가 이 2본이었다. 경쟁 초안·검수 보고 본체는 DQ-6 대로 계수만.
- 실측: **2 파일 · 95 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.25.1/results/comp_R1/CHERRYPICK_R1.md` | 41 | v1.0.25.1 | Result(체리픽 결정 기록) | — | (b) `INDEX_v25.md`:87 인용 — v1.0.25 경쟁 저작 라운드 1 의 채택 결정 기록 ; 사본(고유본 = Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md — §4 #42 · 정독 경로 = 현행) |
| 2 | `Claude/docs/v1.0.25.1/results/comp_R1/AUTHOR_BRIEF.md` | 54 | v1.0.25.1 | 기타(경쟁 저작 brief) | — | (b) `INDEX_v25.md`:87 인용 — 경쟁 저자에게 준 brief(요구 사양 기록) · 같은 폴더의 경쟁 초안 tex·검수 md 는 DQ-6 계수만 ; 사본(고유본 = Claude/docs/v1.0.24/results/comp_R1/AUTHOR_BRIEF.md — §4 #68 · 정독 경로 = 현행) |

### (ix) 조사 문서군

- 정의: `results/comp_v24/*.md`(+lit_raw·sintef_data/SOURCES) · `results/comp_v26_data/*.md`(README → (xi) · HANDOVER → (iii)) · `docs/v1.0.22/results/comp_v23/*.md` · `comp_SM2/**` · `comp_FR/**` · `docs/v1.0.18.2/ROADMAP_future_physics.md` · `docs/v1.0.20/results/`(FIGS_PICK·DIRECTION_*·TRIAGE_P7·V1020_STYLE_RUBRIC + 추가 발견 상위 md) · `V1013_TERMS_POLICY` · `V1014_TONE_AUDIT` · (추가 발견) `V1010_INSPECT_draft_C3.md`
- 기대치(출처): 미실측(brief §4)
- 실측: **88 파일 · 15187 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` | 49 | v1.0.18.2 | 조사 | R3·R5·R6 | B1 |
| 2 | `Claude/docs/v1.0.20/results/CODE_IMPL_REPORT.md` | 148 | v1.0.20 | 조사 | — | 추가 발견(v1.0.20 results 상위 md — brief 명시 4종 밖) |
| 3 | `Claude/docs/v1.0.20/results/comp_P7_review/TRIAGE_P7.md` | 39 | v1.0.20 | 감사 | — | — |
| 4 | `Claude/docs/v1.0.20/results/DIRECTION_GENERAL_REPORT.md` | 264 | v1.0.20 | 조사 | — | — |
| 5 | `Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md` | 291 | v1.0.20 | 조사 | — | — |
| 6 | `Claude/docs/v1.0.20/results/DIRECTION_STATMECH_REPORT.md` | 359 | v1.0.20 | 조사 | — | — |
| 7 | `Claude/docs/v1.0.20/results/FIGS_PICK_JUDGMENT.md` | 131 | v1.0.20 | 조사 | — | — |
| 8 | `Claude/docs/v1.0.20/results/INTERCHAPTER_REPORT.md` | 174 | v1.0.20 | 조사 | — | 추가 발견(v1.0.20 results 상위 md — brief 명시 4종 밖) |
| 9 | `Claude/docs/v1.0.20/results/V1020_KICKOFF_SURVEY_history.md` | 29 | v1.0.20 | 조사 | — | 추가 발견(v1.0.20 results 상위 md — brief 명시 4종 밖) |
| 10 | `Claude/docs/v1.0.20/results/V1020_KICKOFF_SURVEY_structure_citation.md` | 97 | v1.0.20 | 조사 | — | 추가 발견(v1.0.20 results 상위 md — brief 명시 4종 밖) |
| 11 | `Claude/docs/v1.0.20/results/V1020_P1_CITATION_BASELINE.md` | 23 | v1.0.20 | 조사 | — | 추가 발견(v1.0.20 results 상위 md — brief 명시 4종 밖) |
| 12 | `Claude/docs/v1.0.20/results/V1020_STYLE_RUBRIC.md` | 50 | v1.0.20 | 조사 | — | — |
| 13 | `Claude/docs/v1.0.22/results/comp_FR/A01_REVIEW.md` | 479 | v1.0.22 | 감사 | — | — |
| 14 | `Claude/docs/v1.0.22/results/comp_FR/A02_REVIEW.md` | 460 | v1.0.22 | 감사 | — | — |
| 15 | `Claude/docs/v1.0.22/results/comp_FR/A03_REVIEW.md` | 346 | v1.0.22 | 감사 | — | — |
| 16 | `Claude/docs/v1.0.22/results/comp_FR/A04_REVIEW.md` | 353 | v1.0.22 | 감사 | — | — |
| 17 | `Claude/docs/v1.0.22/results/comp_FR/A05_REVIEW.md` | 323 | v1.0.22 | 감사 | — | — |
| 18 | `Claude/docs/v1.0.22/results/comp_FR/A06_REVIEW.md` | 398 | v1.0.22 | 감사 | — | — |
| 19 | `Claude/docs/v1.0.22/results/comp_FR/A07_REVIEW.md` | 311 | v1.0.22 | 감사 | — | — |
| 20 | `Claude/docs/v1.0.22/results/comp_FR/A08_REVIEW.md` | 383 | v1.0.22 | 감사 | — | — |
| 21 | `Claude/docs/v1.0.22/results/comp_FR/A09_REVIEW.md` | 531 | v1.0.22 | 감사 | — | — |
| 22 | `Claude/docs/v1.0.22/results/comp_FR/A10_REVIEW.md` | 150 | v1.0.22 | 감사 | — | — |
| 23 | `Claude/docs/v1.0.22/results/comp_FR/A11_REVIEW.md` | 412 | v1.0.22 | 감사 | — | — |
| 24 | `Claude/docs/v1.0.22/results/comp_FR/A12_REVIEW.md` | 404 | v1.0.22 | 감사 | — | — |
| 25 | `Claude/docs/v1.0.22/results/comp_FR/A13_REVIEW.md` | 480 | v1.0.22 | 감사 | — | — |
| 26 | `Claude/docs/v1.0.22/results/comp_FR/A14_REVIEW.md` | 201 | v1.0.22 | 감사 | — | — |
| 27 | `Claude/docs/v1.0.22/results/comp_FR/A15_REVIEW.md` | 330 | v1.0.22 | 감사 | — | — |
| 28 | `Claude/docs/v1.0.22/results/comp_FR/A16_REVIEW.md` | 136 | v1.0.22 | 감사 | — | — |
| 29 | `Claude/docs/v1.0.22/results/comp_FR/A17_REVIEW.md` | 191 | v1.0.22 | 감사 | — | — |
| 30 | `Claude/docs/v1.0.22/results/comp_FR/A18_REVIEW.md` | 456 | v1.0.22 | 감사 | — | — |
| 31 | `Claude/docs/v1.0.22/results/comp_FR/A19_REVIEW.md` | 613 | v1.0.22 | 감사 | — | — |
| 32 | `Claude/docs/v1.0.22/results/comp_FR/A20_REVIEW.md` | 506 | v1.0.22 | 감사 | — | — |
| 33 | `Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md` | 360 | v1.0.22 | 감사 | — | — |
| 34 | `Claude/docs/v1.0.22/results/comp_FR/A22_REVIEW.md` | 686 | v1.0.22 | 감사 | — | — |
| 35 | `Claude/docs/v1.0.22/results/comp_FR/A23_REVIEW.md` | 588 | v1.0.22 | 감사 | — | — |
| 36 | `Claude/docs/v1.0.22/results/comp_FR/BRIEF_FR_A.md` | 20 | v1.0.22 | 조사 | — | — |
| 37 | `Claude/docs/v1.0.22/results/comp_FR/EXEC_M1.md` | 35 | v1.0.22 | 조사 | — | — |
| 38 | `Claude/docs/v1.0.22/results/comp_FR/EXEC_M2.md` | 36 | v1.0.22 | 조사 | — | — |
| 39 | `Claude/docs/v1.0.22/results/comp_FR/EXEC_M3.md` | 32 | v1.0.22 | 조사 | — | — |
| 40 | `Claude/docs/v1.0.22/results/comp_FR/EXEC_M4.md` | 26 | v1.0.22 | 조사 | — | — |
| 41 | `Claude/docs/v1.0.22/results/comp_FR/FR_T_H_TRIAGE_PREP.md` | 38 | v1.0.22 | 감사 | — | — |
| 42 | `Claude/docs/v1.0.22/results/comp_FR/FR_T_ML_TRIAGE.md` | 37 | v1.0.22 | 감사 | — | — |
| 43 | `Claude/docs/v1.0.22/results/comp_FR/RESUME_FR.md` | 54 | v1.0.22 | 조사 | — | — |
| 44 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_DRAFTS/SM2A_susceptibility.tex` | 70 | v1.0.22 | 원문 tex | — | 추가 발견(`comp_SM2/*.md` 패턴 밖 tex 초안) |
| 45 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_DRAFTS/SM2B_ensemble_equiv.tex` | 51 | v1.0.22 | 원문 tex | — | 추가 발견(`comp_SM2/*.md` 패턴 밖 tex 초안) |
| 46 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_DRAFTS/SM2C_two_responses.tex` | 52 | v1.0.22 | 원문 tex | — | 추가 발견(`comp_SM2/*.md` 패턴 밖 tex 초안) |
| 47 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_REMOVAL.md` | 117 | v1.0.22 | 조사 | — | — |
| 48 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md` | 135 | v1.0.22 | 조사 | R3·R5·R7 | B5 |
| 49 | `Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | 44 | v1.0.22 | 조사 | R3·R5·R6·R7 | B4 |
| 50 | `Claude/docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md` | 178 | v1.0.22 | 조사 | R6 | — |
| 51 | `Claude/docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md` | 163 | v1.0.22 | 조사 | R6 | — |
| 52 | `Claude/docs/v1.0.22/results/comp_v23/SURV3_convex_inverse.md` | 124 | v1.0.22 | 조사 | R6 | — |
| 53 | `Claude/docs/v1.0.22/results/comp_v23/SURV4_bifurcation_stochastic.md` | 134 | v1.0.22 | 조사 | R6 | — |
| 54 | `Claude/results/comp_v24/ABLATION_ANODE.md` | 23 | v1.0.24 | 조사 | — | — |
| 55 | `Claude/results/comp_v24/AUDIT_v1024_DOC_CODE.md` | 43 | v1.0.24 | 감사 | — | — |
| 56 | `Claude/results/comp_v24/CODEX_REVIEW_VERIFICATION.md` | 35 | v1.0.24 | 감사 | — | — |
| 57 | `Claude/results/comp_v24/DATA_REGISTRY.md` | 70 | v1.0.24 | 조사 | — | — |
| 58 | `Claude/results/comp_v24/FIT_CHECK_v1024.md` | 87 | v1.0.24 | 조사 | — | — |
| 59 | `Claude/results/comp_v24/fit_registry.md` | 25 | v1.0.24 | 조사 | — | — |
| 60 | `Claude/results/comp_v24/GRAPHITE_STAGING_XRD.md` | 61 | v1.0.24 | 조사 | — | — |
| 61 | `Claude/results/comp_v24/HIST_layout_versionarc.md` | 151 | v1.0.24 | 조사 | — | — |
| 62 | `Claude/results/comp_v24/HIST_notation_code.md` | 106 | v1.0.24 | 조사 | — | — |
| 63 | `Claude/results/comp_v24/HIST_register.md` | 146 | v1.0.24 | 조사 | — | — |
| 64 | `Claude/results/comp_v24/HIST_terminology.md` | 143 | v1.0.24 | 조사 | — | — |
| 65 | `Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md` | 86 | v1.0.24 | 조사 | R3·R5 | B2 |
| 66 | `Claude/results/comp_v24/INV_code_in_body.md` | 39 | v1.0.24 | 조사 | — | — |
| 67 | `Claude/results/comp_v24/INV_overflow.md` | 51 | v1.0.24 | 조사 | — | — |
| 68 | `Claude/results/comp_v24/INV_register_titles_prose.md` | 142 | v1.0.24 | 조사 | — | — |
| 69 | `Claude/results/comp_v24/LCO_DIAGNOSIS.md` | 39 | v1.0.24 | 조사 | — | — |
| 70 | `Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | 129 | v1.0.24 | 조사 | R3·R5·R6·R7 | B3 |
| 71 | `Claude/results/comp_v24/lit_raw/01_graphite.md` | 141 | v1.0.24 | 조사 | — | 추가 발견(comp_v24 하위 폴더) |
| 72 | `Claude/results/comp_v24/lit_raw/02_methodology.md` | 119 | v1.0.24 | 조사 | — | 추가 발견(comp_v24 하위 폴더) |
| 73 | `Claude/results/comp_v24/lit_raw/03_graphite_si.md` | 82 | v1.0.24 | 조사 | — | 추가 발견(comp_v24 하위 폴더) |
| 74 | `Claude/results/comp_v24/lit_raw/04_lco.md` | 129 | v1.0.24 | 조사 | — | 추가 발견(comp_v24 하위 폴더) |
| 75 | `Claude/results/comp_v24/param_dist_stats.md` | 8 | v1.0.24 | 조사 | — | — |
| 76 | `Claude/results/comp_v24/PUBLIC_DATA_SURVEY.md` | 45 | v1.0.24 | 조사 | — | — |
| 77 | `Claude/results/comp_v24/SESSION_AUDIT_v1024.md` | 92 | v1.0.24 | 감사 | — | — |
| 78 | `Claude/results/comp_v24/sintef_data/SOURCES.md` | 25 | v1.0.24 | 조사 | — | 추가 발견(comp_v24 하위 폴더) |
| 79 | `Claude/results/comp_v24/T_SPLIT_FINDING.md` | 67 | v1.0.24 | 조사 | — | — |
| 80 | `Claude/results/comp_v24/TAKE_VS_DISCARD.md` | 85 | v1.0.24 | 조사 | — | — |
| 81 | `Claude/results/comp_v24/TERM_DECISION_TABLE.md` | 99 | v1.0.24 | 조사 | — | — |
| 82 | `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md` | 206 | v1.0.24 | 조사 | R2·R3 | A11 |
| 83 | `Claude/results/comp_v24/VALIDATION_SYNTHESIS.md` | 81 | v1.0.24 | 조사 | — | — |
| 84 | `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md` | 80 | v1.0.24 | 조사 | R2 | A12 · R2: L80 `</content>` 잔존 문자열 |
| 85 | `Claude/results/comp_v26_data/MULTI_DATASET_REVIEW.md` | 58 | v1.0.26 | 감사 | — | §2.9 L202 미검독 |
| 86 | `Claude/results/process/V1010_INSPECT_draft_C3.md` | 107 | v1.0.10 | 감사 | — | 추가 발견 — §5 `C3_graph_check/`·`C3_pdf_render/` 지위 근거(L14–15·23) |
| 87 | `Claude/results/process/V1013_TERMS_POLICY.md` | 90 | v1.0.13 | 조사 | — | brief 명시 |
| 88 | `Claude/results/process/V1014_TONE_AUDIT.md` | 200 | v1.0.14 | 감사 | — | 종류 = 감사(brief 는 조사 문서군에 배정 — 군은 (ix) 유지) |

### (ix-b) 추가 발견 — 조사 문서(iter_3 · AUD-R2-10 · 정책 (a)(b))

- 정의: 등재 ledger·Result 의 계열 형제(radius 조사 판정문 3 + 보고) + 마스터 플랜이 정독 대상으로 명시한 조사 md. radius 폴더의 미등재 md(iter_4 시점 16본)는 두 부류 — 조사 카드 14본(`00_`~`43_` · 1,455줄 · 계열 밖 → §8.3 계수 · 1.4 토픽 한정 열람 후보) + 보조 기록 2본: `CODE_w_check.md`(23 · `docs/INDEX.md`:181 인용 → **iter_5 에서 (b) 근거로 행 6 등재**, AUD-R4-01) · `DOCS_say_about_distribution.md`(28 · 통제 문서 5본 인용 0 → 계수 유지; 등재 문서 인용은 `HANDOVER_2026-06-30`:38,70·`note_A4`:25 — 1.4 토픽 한정 열람 후보).
- 실측: **6 파일 · 321 줄**(TSV) — iter_5 행 6 추가

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/results/research/radius/RADIUS_VERDICT.md` | 83 | Fable v2~v10(세부: radius survey 06-30, 추정) | 조사 | — | (a) (vii) `RADIUS_LEDGER`·(viii) `PHASE_RADIUS_RESULT` 형제 · 6-30 radius 조사 판정문 — [MODEL-1 선택] 원천은 **추정**(문서명·날짜 대응; R1 L-04 행은 `note_A3`·`HANDOVER_v1.0.11`·`HANDOVER_v1.0.19` 를 인용하고 이 파일은 미인용 — DR-15 연동, 1.3 Step 9 에서 확정) |
| 2 | `Claude/results/research/radius/ORIGIN_VERDICT.md` | 79 | Fable v2~v10(세부: radius survey 06-30, 추정) | 조사 | — | (a) 동상 |
| 3 | `Claude/results/research/radius/BAND_VERDICT.md` | 69 | Fable v2~v10(세부: radius survey 06-30, 추정) | 조사 | — | (a) 동상 |
| 4 | `Claude/results/research/radius/50_report.md` | 23 | Fable v2~v10(세부: radius survey 06-30, 추정) | 조사 | — | (a) 동상 · `V1010_INSPECT_draft_C3.md`:16 인용 |
| 5 | `Claude/results/research/broadening_w_design.md` | 44 | Fable v2~v10(세부: v10, 추정) | 조사 | — | (b) 마스터 플랜 1.2 Step 3 정독 대상 명시(L325 — L-21 ρ(U_j) 잔존 주의) |
| 6 | `Claude/results/research/radius/CODE_w_check.md` | 23 | Fable v2~v10(세부: radius survey 06-30, 추정) | 조사(코드 실행 검증 기록) | — | (b) `docs/INDEX.md`:181 인용 — Ch2 v4 w_eff narrowing 오류가 적대 2R 검수를 통과하고 코드 실행 검증에서 발각된 경위의 실물 근거(마스터 플랜 §2.3 Ch2 트랙·3.6 "설계 doc 순응 검수의 한계" 사건) · iter_5 AUD-R4-01(토크나이저가 여는 괄호 포함 토큰 `(CODE_w_check.md` 를 미해소로 오분류) |

### (x) dossier · jcp_extract(+ JCP PDF 존재)

- 정의: `old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` · `Claude/jcp_extract.txt` · JCP PDF 는 모집단 밖 — 존재·바이트만 비고에
- 기대치(출처): 50줄 · 724줄(brief §4)
- 실측: **2 파일 · 774 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/jcp_extract.txt` | 725 | 횡단 | 조사(원문 추출) | — | brief 724 → 실측 725(**확정** — 파일이 개행으로 끝나지 않아 `(Get-Content).Count` = LF 724 + 1 · brief 724 는 LF 계수, 검수 AUD-06) · JCP PDF 존재 = `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` 2,075,558 B(열지 않음) |
| 2 | `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` | 49 | 구트랙 RB | 조사 | R3(glob)·R6·R7 | brief 50 → 실측 49(정의 −1) · Assumptions 5·10 |

### (xi) v1.0.26 실물

- 정의: `docs/v1.0.26A-regsol/README.md` · `docs/v1.0.26B-gallery/README.md` · `results/comp_v26_data/README.md` · `out_versions/build.log` + 조사 스크립트 `.py` 목록 + (추가 발견) R2 가 읽은 `out_skew/summary_skew.json`·`skew_log.txt`
- 기대치(출처): 199·193·50·36(brief §4)
- 실측: **14 파일 · 2184 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.26A-regsol/README.md` | 198 | v1.0.26 | 조사 | R2(추가) | brief 199 → 198(정의 −1) |
| 2 | `Claude/docs/v1.0.26B-gallery/README.md` | 192 | v1.0.26 | 조사 | R2(추가) | brief 193 → 192(정의 −1) |
| 3 | `Claude/results/comp_v26_data/analyze_sintef.py` | 230 | v1.0.26 | 기타(코드) | — | README.md:24 미실행(잔여 과제) |
| 4 | `Claude/results/comp_v26_data/bdd_dqdv.py` | 177 | v1.0.26 | 기타(코드) | — | — |
| 5 | `Claude/results/comp_v26_data/build_two_versions.py` | 202 | v1.0.26 | 기타(코드) | — | README.md:20 |
| 6 | `Claude/results/comp_v26_data/make_version_docs.py` | 285 | v1.0.26 | 기타(코드) | — | README.md:21 |
| 7 | `Claude/results/comp_v26_data/out_skew/summary_skew.json` | 4 | v1.0.26 | 기타(데이터) | R2(추가) | 추가 발견(R2 Read Coverage +2 · README.md:30 폐기분 산출 "빈 JSON") |
| 8 | `Claude/results/comp_v26_data/out_versions/build.log` | 36 | v1.0.26 | 기타(로그) | R2(추가) | brief 36 = 36 — 파일은 LF 36·끝 개행 True 라 Read 표기는 37 이어야 하므로 R2 의 표기 불일치(AUD-09) · R2 DQ-2 A/B 수치 원천 |
| 9 | `Claude/results/comp_v26_data/README.md` | 49 | v1.0.26 | 조사 | R2(추가) | brief 50 → 49(정의 −1) · I-7 L20–35 토픽 정독 |
| 10 | `Claude/results/comp_v26_data/regsol_kernel.py` | 108 | v1.0.26 | 기타(코드) | — | §2.8 L181 |
| 11 | `Claude/results/comp_v26_data/skew_log.txt` | 11 | v1.0.26 | 기타(텍스트) | R2(추가) | 추가 발견(R2 Read Coverage +3) |
| 12 | `Claude/results/comp_v26_data/test_gallery_vs_regsol.py` | 242 | v1.0.26 | 기타(코드) | — | — |
| 13 | `Claude/results/comp_v26_data/test_skew_regsol_v2.py` | 297 | v1.0.26 | 기타(코드) | — | — |
| 14 | `Claude/results/comp_v26_data/test_skew_regsol.py` | 153 | v1.0.26 | 기타(코드) | — | README.md:30 폐기(실행 금지) |

### (xii) 서지 원장 4본

- 정의: `docs/v1.0.2N/results/V102N_REFERENCE_LEDGER.md` (N=0..3) · hash 사본 판정 §4
- 기대치(출처): 55·38·33·33(brief §4)
- 실측: **4 파일 · 155 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.20/results/V1020_REFERENCE_LEDGER.md` | 54 | v1.0.20 | 서지 원장 | R7 | brief 55 → 54(정의 −1) |
| 2 | `Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md` | 37 | v1.0.21 | 서지 원장 | R3(grep)·R7 | brief 38 → 37(정의 −1) |
| 3 | `Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md` | 32 | v1.0.22 | 서지 원장 | R7 | brief 33 → 32(정의 −1) ; 고유본(사본 1: Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md) |
| 4 | `Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md` | 32 | v1.0.23 | 서지 원장 | R7 | brief 33 → 32(정의 −1) · V1022 와 hash 동일(R7 md5 대조와 일치) ; 사본(고유본 = Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md) |

### (xiii) reflect 계획서 · V1024_REFLECT_EXECUTION_LEDGER(실물 경로 확인)

- 정의: 2026-07-19 reflect 계획서(→ (i) 계수) · `V1024_REFLECT_EXECUTION_LEDGER.md` ×4(→ (vii) 계수) · (추가 발견·본 군 계수) `REFLECT_SEED_TABLE.md` ×4
- 기대치(출처): 미실측(brief §4)
- 실측: **4 파일 · 236 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.24.1/results/REFLECT_SEED_TABLE.md` | 59 | v1.0.24.1 | 조사 | — | 추가 발견 ; 사본(고유본 = Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md) |
| 2 | `Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md` | 59 | v1.0.24 | 조사 | — | 추가 발견 · INDEX_v25.md:83 사양 원천(승계) — addendum A4·A7 이 supersede ; 고유본(사본 3: Claude/docs/v1.0.24.1/results/REFLECT_SEED_TABLE.md · Claude/docs/v1.0.25/results/REFLECT_SEED_TABLE.md · Claude/docs/v1.0.25.1/results/REFLECT_SEED_TABLE.md) |
| 3 | `Claude/docs/v1.0.25.1/results/REFLECT_SEED_TABLE.md` | 59 | v1.0.25.1 | 조사 | — | 추가 발견 ; 사본(고유본 = Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md) |
| 4 | `Claude/docs/v1.0.25/results/REFLECT_SEED_TABLE.md` | 59 | v1.0.25 | 조사 | — | 추가 발견 ; 사본(고유본 = Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md) |

실물 경로 확인(계수는 각 정본 군):

| 항목 | 실물 path | 줄수 | 계수 군 |
|---|---|---|---|
| reflect 계획서 | `Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md` | 215 | (i) |
| V1024_REFLECT_EXECUTION_LEDGER | `Claude/docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | (vii) — hash ABE37E4BE0B3 (4본 동일) |
| V1024_REFLECT_EXECUTION_LEDGER | `Claude/docs/v1.0.24.1/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | (vii) — hash ABE37E4BE0B3 (4본 동일) |
| V1024_REFLECT_EXECUTION_LEDGER | `Claude/docs/v1.0.25/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | (vii) — hash ABE37E4BE0B3 (4본 동일) |
| V1024_REFLECT_EXECUTION_LEDGER | `Claude/docs/v1.0.25.1/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 14 | (vii) — hash ABE37E4BE0B3 (4본 동일) |

### (xiv) git untracked 21건 — §5 참조(모집단 밖 png·html 포함이라 본 표에는 줄수 열 없음)

### (xv) 판독 산출(시드 등재 — 정독 대상 아님)

- 정의: `Claude/results/handoffs/2026-09-02-v2-master-plan/**` 전건(brief·audit_checklist·iter_1/*·wf/*) + (추가 발견) 본 Step brief
- 기대치(출처): 시드 등재(brief §4)
- 실측: **24 파일 · 10474 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/results/handoffs/2026-09-02-v2-master-plan/audit_checklist.md` | 47 | 본 arc | 시드(판독) | — | — |
| 2 | `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 218 | 본 arc | 시드(판독) | R1·R2·R3·R4a·R4b·R5·R6·R7 | — |
| 3 | `Claude/results/handoffs/2026-09-02-v2-master-plan/iter_1/plan_draft.md` | 575 | 본 arc | 시드(판독) | — | — |
| 4 | `Claude/results/handoffs/2026-09-02-v2-master-plan/iter_1/work_log.md` | 119 | 본 arc | 시드(판독) | — | — |
| 5 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/audit_format.md` | 83 | 본 arc | 시드(판독) | — | — |
| 6 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/audit_logic.md` | 89 | 본 arc | 시드(판독) | — | — |
| 7 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/audit_spec.md` | 161 | 본 arc | 시드(판독) | — | — |
| 8 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/critic.md` | 208 | 본 arc | 시드(판독) | — | — |
| 9 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/fix_change_log.md` | 132 | 본 arc | 시드(판독) | — | (viii) `CHANGE_LOG` 패턴에도 매치 — 계수는 (xv) |
| 10 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/go_1g_check_2026-09-03.txt` | 15 | 본 arc | 시드(판독) | — | I-6 전문 정독 · 1g 실측 대조 원본 |
| 11 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/plan_draft_v2.md` | 783 | 본 arc | 시드(판독) | — | — |
| 12 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/plan_draft_v3.md` | 859 | 본 arc | 시드(판독) | — | — |
| 13 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/plan_v3_appendix_ABC.md` | 103 | 본 arc | 시드(판독) | — | — |
| 14 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R1_version_register_v3_to_v1019.md` | 205 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 15 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R2_version_register_v1020_to_v1026.md` | 299 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 16 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R3_binding_decisions_and_lost_directions.md` | 397 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 17 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R4a_diagnosis_scope_ch1_partT.md` | 362 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 18 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R4b_diagnosis_scope_ch2_ch3_appendix.md` | 430 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 19 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R5_theory_candidates_thermo_statmech.md` | 425 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 20 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R6_theory_candidates_kinetics_hys_heat.md` | 414 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 21 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R7_reference_master_map.json` | 3833 | 본 arc | 시드(판독·json) | — | R7 json(3,833줄) |
| 22 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R7_reference_master_map.md` | 533 | 본 arc | 시드(판독) | — | 시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log) |
| 23 | `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/review_master.md` | 51 | 본 arc | 시드(판독) | — | — |
| 24 | `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md` | 133 | 본 arc | 통제(본 arc) | — | 추가 발견 — 본 Step 지시서(brief 정의 (xv) 밖 · 통제(본 arc)) |

### (xvi) 현행 tex 60(v1.0.25.1) — 빌드 포함/미포함 열

- 정의: `docs/v1.0.25.1/*.tex`(마스터 3 + 독립 부록 1) + `_sections/*.tex` 56. 빌드 열 = 마스터 3본의 비주석 `\input{_sections/…}` 실측(§6). `results/comp_R1/**/*.tex` 30본은 경쟁 초안이라 현행 tex 밖(§8)
- 기대치(출처): 60·9,214줄(brief §4 · 1g A2) — 일치. 빌드 기대 = 포함 58 / 미포함 2(orphan `ch1_appD_si` + 독립 부록) → **실측 = 마스터 3 + 포함 53 + 미포함 4(독립 1 + orphan 3)** — `ch1_preamble`·`ch2_preamble` 가 기대와 달리 \input 되지 않음(§6·§8.1)
- 실측: **60 파일 · 9214 줄**(TSV)

| # | path | 줄수 | 빌드 포함/미포함 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.25.1/_sections/ch1_appA_signcheck.tex` | 89 | 포함(ch1 L54) | v1.0.25.1 | 원문 tex | R4a | 사본(고유본 = Claude/docs/v1.0.22/_sections/ch1_appA_signcheck.tex) |
| 2 | `Claude/docs/v1.0.25.1/_sections/ch1_appB_codemap.tex` | 184 | 포함(ch1 L55) | v1.0.25.1 | 원문 tex | R4a | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_appB_codemap.tex) |
| 3 | `Claude/docs/v1.0.25.1/_sections/ch1_appD_si.tex` | 91 | 미포함·orphan | v1.0.25.1 | 원문 tex | R4b | orphan(기대와 일치 · R4b DQ-3) ; 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_appD_si.tex) |
| 4 | `Claude/docs/v1.0.25.1/_sections/ch1_appE_selfconsistent.tex` | 217 | 포함(ch1 L58) | v1.0.25.1 | 원문 tex | R3(grep)·R4a·R6 | A14 ; 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_appE_selfconsistent.tex) |
| 5 | `Claude/docs/v1.0.25.1/_sections/ch1_preamble.tex` | 77 | 미포함·orphan | v1.0.25.1 | 원문 tex | R4a(grep) | brief §3.2 기대 "지원 4본 = \input 되는 빌드 포함" 과 상이 — 헤더 L2–3 "graphite_ica_ch1_v1.0.21.tex 가 \input" (v1.0.21 잔재) · 현행 마스터 3본 어디에도 \input 0(Grep `\input{` v1.0.25.1 전 tex — 마스터 3본 외 0건) → orphan ; 사본(고유본 = Claude/docs/v1.0.21/_sections/ch1_preamble.tex) |
| 6 | `Claude/docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` | 94 | 포함(ch1 L25) | v1.0.25.1 | 원문 tex | R4a·R6(보강) | A13 ; 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec00_intro.tex) |
| 7 | `Claude/docs/v1.0.25.1/_sections/ch1_sec01_n0n1.tex` | 244 | 포함(ch1 L26) | v1.0.25.1 | 원문 tex | R4a·R6 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec01_n0n1.tex) |
| 8 | `Claude/docs/v1.0.25.1/_sections/ch1_sec02a_part0.tex` | 390 | 포함(ch1 L27) | v1.0.25.1 | 원문 tex | R3(grep)·R4a·R5 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec02a_part0.tex) |
| 9 | `Claude/docs/v1.0.25.1/_sections/ch1_sec02b_part0.tex` | 474 | 포함(ch1 L28) | v1.0.25.1 | 원문 tex | R4a·R5 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec02b_part0.tex) |
| 10 | `Claude/docs/v1.0.25.1/_sections/ch1_sec03_center.tex` | 121 | 포함(ch1 L29) | v1.0.25.1 | 원문 tex | R4a·R5 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec03_center.tex) |
| 11 | `Claude/docs/v1.0.25.1/_sections/ch1_sec04_hys.tex` | 336 | 포함(ch1 L30) | v1.0.25.1 | 원문 tex | R4a·R4b(부분)·R5·R6 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec04_hys.tex) |
| 12 | `Claude/docs/v1.0.25.1/_sections/ch1_sec05_width.tex` | 424 | 포함(ch1 L31) | v1.0.25.1 | 원문 tex | R4a·R5·R6 | — |
| 13 | `Claude/docs/v1.0.25.1/_sections/ch1_sec05b_gr2L.tex` | 238 | 포함(ch1 L32) | v1.0.25.1 | 원문 tex | R4a·R4b(부분)·R5 | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_sec05b_gr2L.tex) |
| 14 | `Claude/docs/v1.0.25.1/_sections/ch1_sec06_eqpeak.tex` | 131 | 포함(ch1 L33) | v1.0.25.1 | 원문 tex | R4a·R4b(부분)·R5 | — |
| 15 | `Claude/docs/v1.0.25.1/_sections/ch1_sec07_broadening.tex` | 375 | 포함(ch1 L34) | v1.0.25.1 | 원문 tex | R4a·R5 | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_sec07_broadening.tex) |
| 16 | `Claude/docs/v1.0.25.1/_sections/ch1_sec08_lag.tex` | 148 | 포함(ch1 L35) | v1.0.25.1 | 원문 tex | R4a·R6 | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_sec08_lag.tex) |
| 17 | `Claude/docs/v1.0.25.1/_sections/ch1_sec09_tail.tex` | 253 | 포함(ch1 L36) | v1.0.25.1 | 원문 tex | R4a·R6 | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_sec09_tail.tex) |
| 18 | `Claude/docs/v1.0.25.1/_sections/ch1_sec10_sum.tex` | 187 | 포함(ch1 L37) | v1.0.25.1 | 원문 tex | R4a·R5(grep) | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_sec10_sum.tex) |
| 19 | `Claude/docs/v1.0.25.1/_sections/ch1_sec11_lcointro.tex` | 175 | 포함(ch2 L24) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec11_lcointro.tex) |
| 20 | `Claude/docs/v1.0.25.1/_sections/ch1_sec12_lcocenter.tex` | 112 | 포함(ch2 L25) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec12_lcocenter.tex) |
| 21 | `Claude/docs/v1.0.25.1/_sections/ch1_sec13_lcohys.tex` | 223 | 포함(ch2 L26) | v1.0.25.1 | 원문 tex | R4b·R5(부분)·R6 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec13_lcohys.tex) |
| 22 | `Claude/docs/v1.0.25.1/_sections/ch1_sec14_lcodecomp.tex` | 143 | 포함(ch2 L27) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec14_lcodecomp.tex) |
| 23 | `Claude/docs/v1.0.25.1/_sections/ch1_sec15_lcoelec.tex` | 396 | 포함(ch2 L28) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex) |
| 24 | `Claude/docs/v1.0.25.1/_sections/ch1_sec16_lcopeak.tex` | 70 | 포함(ch2 L29) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.22/_sections/ch1_sec16_lcopeak.tex) |
| 25 | `Claude/docs/v1.0.25.1/_sections/ch1_sec16b_lcoomega.tex` | 160 | 포함(ch2 L30) | v1.0.25.1 | 원문 tex | R3(grep)·R4b·R5(보조) | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex) |
| 26 | `Claude/docs/v1.0.25.1/_sections/ch1_sec17_msmr.tex` | 176 | 포함(ch2 L31) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1_sec17_msmr.tex) |
| 27 | `Claude/docs/v1.0.25.1/_sections/ch1_sec18_inputs.tex` | 92 | 포함(ch1 L52) | v1.0.25.1 | 원문 tex | R4a | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch1_sec18_inputs.tex) |
| 28 | `Claude/docs/v1.0.25.1/_sections/ch1v22_bib.tex` | 56 | 포함(ch1 L60) | v1.0.25.1 | 원문 tex | R3(grep)·R4a·R5(보조)·R6(grep)·R7 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch1v22_bib.tex) |
| 29 | `Claude/docs/v1.0.25.1/_sections/ch1v22_partT_divider.tex` | 14 | 포함(ch1 L39) | v1.0.25.1 | 원문 tex | — | 지원(Part T 구획) · ch1 L39 \input ; 사본(고유본 = Claude/docs/v1.0.22/_sections/ch1v22_partT_divider.tex) |
| 30 | `Claude/docs/v1.0.25.1/_sections/ch2_appA_traps.tex` | 75 | 포함(ch1 L56) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.22/_sections/ch2_appA_traps.tex) |
| 31 | `Claude/docs/v1.0.25.1/_sections/ch2_appB_codemap.tex` | 77 | 포함(ch1 L57) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch2_appB_codemap.tex) |
| 32 | `Claude/docs/v1.0.25.1/_sections/ch2_preamble.tex` | 56 | 미포함·orphan | v1.0.25.1 | 원문 tex | R4a(grep) | 동상 — 헤더 L2–3 "graphite_ica_ch2_v1.0.21.tex 가 \input" · 현행 \input 0 → orphan ; 사본(고유본 = Claude/docs/v1.0.21/_sections/ch2_preamble.tex) |
| 33 | `Claude/docs/v1.0.25.1/_sections/ch2_sec00_intro.tex` | 71 | 포함(ch1 L40) | v1.0.25.1 | 원문 tex | R4a | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec00_intro.tex) |
| 34 | `Claude/docs/v1.0.25.1/_sections/ch2_sec01_partition.tex` | 149 | 포함(ch1 L41) | v1.0.25.1 | 원문 tex | R4a·R5 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec01_partition.tex) |
| 35 | `Claude/docs/v1.0.25.1/_sections/ch2_sec02_config.tex` | 190 | 포함(ch1 L42) | v1.0.25.1 | 원문 tex | R4a·R5 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec02_config.tex) |
| 36 | `Claude/docs/v1.0.25.1/_sections/ch2_sec03_vibel.tex` | 118 | 포함(ch1 L43) | v1.0.25.1 | 원문 tex | R4a·R4b(부분)·R5(보조) | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec03_vibel.tex) |
| 37 | `Claude/docs/v1.0.25.1/_sections/ch2_sec04_einstein.tex` | 207 | 포함(ch1 L44) | v1.0.25.1 | 원문 tex | R4a·R5(보조) | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec04_einstein.tex) |
| 38 | `Claude/docs/v1.0.25.1/_sections/ch2_sec05_mixing.tex` | 255 | 포함(ch1 L45) | v1.0.25.1 | 원문 tex | R4a·R5·R6(부분) | [C-92] warnbox L230–238(§2.0 L66) ; 사본(고유본 = Claude/docs/v1.0.25/_sections/ch2_sec05_mixing.tex) |
| 39 | `Claude/docs/v1.0.25.1/_sections/ch2_sec06_limits.tex` | 53 | 포함(ch1 L46) | v1.0.25.1 | 원문 tex | R4a·R5(보조) | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec06_limits.tex) |
| 40 | `Claude/docs/v1.0.25.1/_sections/ch2_sec07_revheat.tex` | 102 | 포함(ch1 L47) | v1.0.25.1 | 원문 tex | R4a·R5·R6(보강) | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec07_revheat.tex) |
| 41 | `Claude/docs/v1.0.25.1/_sections/ch2_sec08_synthesis.tex` | 238 | 포함(ch1 L48) | v1.0.25.1 | 원문 tex | R4a·R5(보조) | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch2_sec08_synthesis.tex) |
| 42 | `Claude/docs/v1.0.25.1/_sections/ch2_sec09_method.tex` | 64 | 포함(ch1 L49) | v1.0.25.1 | 원문 tex | R4a | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2_sec09_method.tex) |
| 43 | `Claude/docs/v1.0.25.1/_sections/ch2_sec10_closing.tex` | 29 | 포함(ch1 L50) | v1.0.25.1 | 원문 tex | R4a | 사본(고유본 = Claude/docs/v1.0.22/_sections/ch2_sec10_closing.tex) |
| 44 | `Claude/docs/v1.0.25.1/_sections/ch2v22_bib.tex` | 21 | 포함(ch2 L32) | v1.0.25.1 | 원문 tex | R4b·R5(보조)·R6(grep)·R7 | 사본(고유본 = Claude/docs/v1.0.22/_sections/ch2v22_bib.tex) |
| 45 | `Claude/docs/v1.0.25.1/_sections/ch2v22_notation.tex` | 14 | 포함(ch2 L23) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.22/_sections/ch2v22_notation.tex) |
| 46 | `Claude/docs/v1.0.25.1/_sections/ch2v22_sec00_intro.tex` | 12 | 포함(ch2 L22) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch2v22_sec00_intro.tex) |
| 47 | `Claude/docs/v1.0.25.1/_sections/ch3v22_bib.tex` | 44 | 포함(ch3 L32) | v1.0.25.1 | 원문 tex | R4b·R5(보조)·R6(grep)·R7 | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_bib.tex) |
| 48 | `Claude/docs/v1.0.25.1/_sections/ch3v22_notation.tex` | 46 | 포함(ch3 L24) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_notation.tex) |
| 49 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec00_intro.tex` | 12 | 포함(ch3 L23) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_sec00_intro.tex) |
| 50 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec01_map.tex` | 129 | 포함(ch3 L25) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_sec01_map.tex) |
| 51 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec02_cases.tex` | 173 | 포함(ch3 L26) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.25/_sections/ch3v22_sec02_cases.tex) |
| 52 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec02b_sifr.tex` | 220 | 포함(ch3 L27) | v1.0.25.1 | 원문 tex | R4b | — |
| 53 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec03_blend.tex` | 278 | 포함(ch3 L28) | v1.0.25.1 | 원문 tex | R4b | GS-2 L251–266(§2.0 L67) ; 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex) |
| 54 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec04_mech.tex` | 110 | 포함(ch3 L29) | v1.0.25.1 | 원문 tex | R4b·R6 | GS-1 L89–99(§2.0 L67) ; 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_sec04_mech.tex) |
| 55 | `Claude/docs/v1.0.25.1/_sections/ch3v22_sec05_code.tex` | 70 | 포함(ch3 L31) | v1.0.25.1 | 원문 tex | R4b | 사본(고유본 = Claude/docs/v1.0.24/_sections/ch3v22_sec05_code.tex) |
| 56 | `Claude/docs/v1.0.25.1/_sections/common_preamble_v1024.tex` | 84 | 포함(ch1 L10, ch2 L8, ch3 L8) | v1.0.25.1 | 원문 tex | R3(grep)·R4b(부분) | 마스터 3본이 \input(ch1 L10·ch2 L8·ch3 L8) · 헤더 L2 는 "common_preamble_v1022.tex" 로 표기(파일명 불일치 — 관찰, DQ-12) · L3 "= 구 ch1_preamble ∪ ch2_preamble" ; 사본(고유본 = Claude/docs/v1.0.24/_sections/common_preamble_v1024.tex) |
| 57 | `Claude/docs/v1.0.25.1/appendix_phase_separation.tex` | 497 | 미포함·독립(\documentclass L13) | v1.0.25.1 | 원문 tex | R4b·R5(보조)·R6·R7(부분) | 독립 부록 — 자체 `\documentclass` L13·`\begin{document}` L41 · `_sections` 밖 ; 사본(고유본 = Claude/docs/v1.0.21/appendix_phase_separation.tex) |
| 58 | `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` | 62 | 마스터 | v1.0.25.1 | 원문 tex | R3(grep)·R4b(부분) | — |
| 59 | `Claude/docs/v1.0.25.1/ch2_lco_v1.0.24.tex` | 34 | 마스터 | v1.0.25.1 | 원문 tex | R4b(부분) | — |
| 60 | `Claude/docs/v1.0.25.1/ch3_si_v1.0.24.tex` | 34 | 마스터 | v1.0.25.1 | 원문 tex | R3(grep)·R4b(부분) | — |

### (xvii) 유실 자산 원문 tex 5본

- 정의: `old/_archive/graphite_ica_ch1_{Fable_v2,Fable_v3,Opus_v4,Opus_v5,Opus_v6}.tex`
- 기대치(출처): 5본 존재(Assumptions 23 · 1g A23 5/5)
- 실측: **5 파일 · 11876 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/old/_archive/graphite_ica_ch1_Fable_v2.tex` | 2420 | Fable v2~v10(세부: v2) | 원문 tex | — | Assumptions 23 바이트 일치(183693 B) · 1.4 Step 11 정독 대상 · 본 Step 내용 미검독 |
| 2 | `Claude/old/_archive/graphite_ica_ch1_Fable_v3.tex` | 2758 | Fable v2~v10(세부: v3) | 원문 tex | — | Assumptions 23 바이트 일치(205225 B) · 1.4 Step 11 정독 대상 · 본 Step 내용 미검독 |
| 3 | `Claude/old/_archive/graphite_ica_ch1_Opus_v4.tex` | 2912 | Fable v2~v10(세부: v4) | 원문 tex | — | Assumptions 23 바이트 일치(218389 B) · 1.4 Step 11 정독 대상 · 본 Step 내용 미검독 |
| 4 | `Claude/old/_archive/graphite_ica_ch1_Opus_v5.tex` | 1883 | Fable v2~v10(세부: v5) | 원문 tex | — | Assumptions 23 바이트 일치(153592 B) · 1.4 Step 11 정독 대상 · 본 Step 내용 미검독 |
| 5 | `Claude/old/_archive/graphite_ica_ch1_Opus_v6.tex` | 1903 | Fable v2~v10(세부: v6) | 원문 tex | — | Assumptions 23 바이트 일치(156166 B) · 1.4 Step 11 정독 대상 · 본 Step 내용 미검독 |

### (xvii-b) 추가 발견 — 구트랙 기준 원문 tex 2본(iter_3 · AUD-R2-01 (b)·AUD-R2-09)

- 정의: 프로젝트 `CLAUDE.md` P1 이 프로젝트 목표의 기준 원문으로 인용하는 구트랙 tex — (xvii) 유실 자산 원문과 같은 성격. `docs/` 하위 구버전 tex 본문은 DR-7 정독 범위 밖(§10.4 (b) 정본 참조 · §8.3 계수; 2.1 소관은 현행 두 버전만)이라 (b) 제외 대상이지만 이 2본은 `old/` 소재·헌법 인용이라 등재(비대칭 사유 = §10.4).
- 실측: **2 파일 · 2469 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/old/_archive/Archive_old/graphite_ica_charge_balance_ver1_rechecked2.tex` | 495 | 구트랙 RB | 원문 tex | — | (b) 프로젝트 `CLAUDE.md`:15 P1 "Chapter 1 = … 전하 보존식 기반 내부 전위 결정 흐름" 기준 원문 — 인용 경로 `Claude/docs/` 는 스테일(실물 = `old/_archive/Archive_old/`) → DR-13/OUT-CLAUDEMD 후보 |
| 2 | `Claude/old/_archive/Archive_old/graphite_ica_dynamic_ver5.tex` | 1974 | 구트랙 RB | 원문 tex | — | (b) 프로젝트 `CLAUDE.md`:14 P1 "`ver.1`~`ver.5` 적층 구조" 기준 원문 · Phase Range 이름공간 "역사적 ver." 행 — 인용 경로 스테일(동상) |

### (xvii-c) 추가 발견 — 계보 원문 tex 6본 `old/Ch1_v7~v10`·`Ch2_v3~v4`(iter_3b · 정책 (b) 잔여 해소)

- 정의: `docs/INDEX.md` 가 각 버전 절에서 원문으로 인용하는 `old/` 소재 tex — (xvii) 유실 자산 원문 5본(v2~v6)에 이어지는 Fable v7~v10·Ch2 v3~v4 계보 원문. `iter_3/policy_check.txt` (b) 잔여 6 이 이 6본이었다. 1.2 Step 3(RB→v1.0.19 보강 정독)의 토픽 한정 원천이며 1.4 Step 11 (i) 전문 정독 대상은 아니다(계획서 Assumptions 23 = 5본 불변).
- 실측: **6 파일 · 6621 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/old/Ch1_v7/v7-11.tex` | 893 | Fable v2~v10(세부: v7) | 원문 tex | — | (b) `docs/INDEX.md`:178 인용 — 계보 §2.3 v7(코드 플로우차트 절삭판 894줄·17p) 원문 ; 고유본(사본 1: Claude/results/builds/v7/v7-11/v7-11.tex — §4 #224) |
| 2 | `Claude/old/Ch1_v8/v8-11.tex` | 1208 | Fable v2~v10(세부: v8) | 원문 tex | — | (b) `docs/INDEX.md`:177 인용 — 유도 4단 복원·G-derive 원문 ; 고유본(사본 2: Claude/results/builds/v8/v8-11/v8-11.tex · Claude/results/builds/v9/v9-00_spine/base_v8-11.tex — §4 #112) |
| 3 | `Claude/old/Ch1_v9/graphite_ica_ch1_v9.tex` | 1644 | Fable v2~v10(세부: v9) | 원문 tex | — | (b) `docs/INDEX.md`:175 인용 — LCO 전자 엔트로피·산문 회귀 기원 원문 ; 고유본(사본 2: Claude/results/builds/ch1v10/v10-00_spine/base_v9.tex · Claude/results/builds/v9/v9-11/v9-11.tex — §4 #107) |
| 4 | `Claude/old/Ch1_v10/graphite_ica_ch1_v10.tex` | 1852 | Fable v2~v10(세부: v10) | 원문 tex | — | (b) `docs/INDEX.md`:173 인용 — broadening 복원·w 이중지위·w_eff 제거 원문 ; 고유본(사본 1: Claude/results/builds/ch1v10/v10-11/v10-11.tex — §4 #232) |
| 5 | `Claude/old/Ch2_v3/graphite_ica_ch2_v3.tex` | 265 | Fable v2~v10(세부: Ch2 v3) | 원문 tex | — | (b) `docs/INDEX.md`:179 인용 — Ch2 트랙 v3(5p) 원문(R1 §3.1) ; 고유본(사본 1: Claude/results/builds/ch2_v4/v4-00_spine/base_ch2_v3.tex — §4 #243) |
| 6 | `Claude/old/Ch2_v4/graphite_ica_ch2_v4.tex` | 759 | Fable v2~v10(세부: Ch2 v4) | 원문 tex | — | (b) `docs/INDEX.md`:176 인용 — Ch2 트랙 v4(13p · w_eff narrowing 오류 적대 2R 통과 사례, R1 §3.1) 원문 ; 고유본(사본 1: Claude/results/builds/ch2_v4/v4-11/v4-11.tex — §4 #208) |

### (xviii) v1.0.25 base tex 60 — 합계 + v1.0.25.1 대비 hash 상이 파일만 행 등재

- 정의: `docs/v1.0.25/*.tex` + `_sections/*.tex`(60본 전건 계수 · 행은 hash 상이 파일만)
- 기대치(출처): 60(brief §4) · 1g A3 "diff 파일 10 = sections 3 + masters 3 + ARCHIVE_NOTE + PDF 3" → tex 만 대조 = 6(일치: sections 3 + masters 3) · 비-tex 대조(md/py/json): `ARCHIVE_NOTE.md` 109→118 상이 · `V1025_1_TOUCHUP_NOTE.md` 는 v1.0.25.1 에만 존재
- 실측: **60 파일 · 9207 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.25/_sections/ch1_sec05_width.tex` | 423 | v1.0.25 | 원문 tex | R4a(diff) | v1.0.25.1 대비 hash 상이 · 줄수 423 → 424 |
| 2 | `Claude/docs/v1.0.25/_sections/ch1_sec06_eqpeak.tex` | 130 | v1.0.25 | 원문 tex | R4a(diff) | v1.0.25.1 대비 hash 상이 · 줄수 130 → 131 |
| 3 | `Claude/docs/v1.0.25/_sections/ch3v22_sec02b_sifr.tex` | 215 | v1.0.25 | 원문 tex | R4b | v1.0.25.1 대비 hash 상이 · 줄수 215 → 220 |
| 4 | `Claude/docs/v1.0.25/ch1_graphite_v1.0.24.tex` | 62 | v1.0.25 | 원문 tex | — | v1.0.25.1 대비 hash 상이 · 줄수 62 → 62 |
| 5 | `Claude/docs/v1.0.25/ch2_lco_v1.0.24.tex` | 34 | v1.0.25 | 원문 tex | — | v1.0.25.1 대비 hash 상이 · 줄수 34 → 34 |
| 6 | `Claude/docs/v1.0.25/ch3_si_v1.0.24.tex` | 34 | v1.0.25 | 원문 tex | — | v1.0.25.1 대비 hash 상이 · 줄수 34 → 34 |

v1.0.25 tex 60 합계 = 9207 줄(v1.0.25.1 9,214 대비 −7) · 60본 중 hash 동일 54 · 상이 6.

### (xix) 루트 `CLAUDE.md`(brief §3.4 부속)

- 정의: `D:\Projects\Project_Anode_Fit\CLAUDE.md` 1본 — 별도 경로로 측정(Codex/ 무접근)
- 기대치(출처): brief·§2.0 A1 90 · R3 실측 89 → **정본 88**(TSV 정의; §3.4)
- 실측: **1 파일 · 88 줄**(TSV)

| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `CLAUDE.md` | 88 | 횡단 | 통제(프로젝트 지침) | R3 | A1 · 7,380 B · trailing CRLF 개행 True(R3 89 = Read 표기 +1) |

## 2. 합계

| 군 | 파일 수(계수) | 줄수 | 비고 |
|---|---|---|---|
| (i) | 92 | 10315 | INDEX.md 는 (vi) 계수 → (i) 정의상 93 |
| (ii) | 16 | 852 |  |
| (iii) | 28 | 1915 |  |
| (iv) | 8 | 885 |  |
| (v) | 1 | 105 |  |
| (vi) | 10 | 982 |  |
| (vii) | 81 | 3698 |  |
| (viii) | 167 | 14858 |  |
| (ix) | 88 | 15187 |  |
| (x) | 2 | 774 |  |
| (xi) | 14 | 2184 |  |
| (xii) | 4 | 155 |  |
| (xiii) | 4 | 236 | 계획서·ledger 는 (i)/(vii) 계수 |
| (xv) | 24 | 10474 |  |
| (xvi) | 60 | 9214 |  |
| (xvii) | 5 | 11876 |  |
| (xviii) | 60 | 9207 | 행은 hash 상이 6본만 |
| (xix) | 1 | 88 |  |
| (i-b) | 11 | 2760 | iter_2 추가(구트랙 계획서 · AUD-02) · iter_3 `RB_AL_MASTER` → (vii-b) 이동 |
| (iv-b) | 12 | 1674 | iter_2 추가(감사 성격 · AUD-01·03) |
| (viii-b) | 2 | 100 | iter_2 추가(Result 성격 · AUD-01) |
| (iv-c) | 21 | 2537 | iter_3 추가(감사·점검 계열 · AUD-R2-01·02) |
| (vii-b) | 4 | 694 | iter_3 추가(구트랙 규약·통합 ledger · AUD-R2-03·10 — 1본은 (i-b) 이동) |
| (ix-b) | 6 | 321 | iter_3 추가(조사 · AUD-R2-10) + iter_5 `CODE_w_check`(AUD-R4-01) |
| (xvii-b) | 2 | 2469 | iter_3 추가(구트랙 기준 원문 tex · AUD-R2-01·09) |
| (xvii-c) | 6 | 6621 | iter_3b 추가(계보 원문 tex v7~v10·Ch2 v3~v4 · 정책 (b) 잔여) |
| (viii-c) | 2 | 95 | iter_3b 추가(경쟁 저작 결정 기록 · 정책 (b) 잔여) |
| (vii-c) | 8 | 854 | iter_4 추가(FITTING_GUIDE 규약 기록 · AUD-R3-06) |
| (xiv) | 21(png 5 · 폴더 3 · Codex 13) | — | 모집단 밖(§5) |
| **합계(TSV 계수)** | **739** | **111130** | iter_1 665/93,005 + iter_2 26/4,673 + iter_3 31/5,859 + iter_3b 8/6,716 + iter_4 8/854 + iter_5 1/23 · TSV 2,651행 중 등재 739 · 미등재 1,912(§8.3) |

중복 처리 규칙 적용 결과: 한 파일이 두 군 정의에 걸린 경우 = `plans/INDEX.md`((i)∩(vi) → (vi)) · `HANDOVER_regsol_investigation.md`((iii)∩(ix) → (iii)) · `comp_v26_data/README.md`((ix)∩(xi) → (xi)) · `V102N_REFERENCE_LEDGER` 4본((vii)∩(xii) → (xii)) · `V1025_CHANGE_LEDGER` ×2((vii)∩(viii) → (vii)) · `V1024_REFLECT_EXECUTION_LEDGER` ×4((vii)∩(xiii) → (vii)) · reflect 계획서((i)∩(xiii) → (i)) · `INDEX_v*`((vi)∩(viii) → (vi)) · `fix_change_log.md`((viii)∩(xv) → (xv)) · `V1014_TONE_AUDIT`(종류 감사 · 군 (ix)).

## 3. brief §3-C · 마스터 플랜 §2.9 수치와의 차이(실측 정본 확정)

### 3.1 plans — 실측 정본 = **93 파일 · 10,384 줄**(TSV · `Claude/plans/*.md` 직계 전건 · 하위 폴더 없음)

정본 구성(실측): 날짜 계획서 90(2026-05-29 ~ 2026-09-02) + `INDEX.md` 1(69줄) + `MASTER_ROADMAP_*` 2(320·131줄) = 93.

(iter_3 주석) 정본 = TSV 스냅샷(09:34:39) 정의로 고정한다. 살아 있는 합계는 계획서 v5.3(813줄)·v5.4(814줄) 행 추가로 10,385→10,386(iter_3 시점; iter_4 추기 후 v5.4 = 816줄 → 10,388 — 살아 있는 값은 매 추기마다 변한다) 이 되지만 정본 수치는 바꾸지 않는다(Read Coverage·배정표는 스냅샷 값 기준, 계획서는 통제 문서라 정독 모집단 밖). master 9,567 의 측정 시각은 미기록(v4 작업 중 · `plans/INDEX.md` 갱신 08:48:05 이전으로 추정) → 아래 잔여 차 1 은 측정 방식 차(추정)·미특정.

| 출처 | 수치 | 실측과의 차이 | 차이를 만든 파일명·줄수 |
|---|---|---|---|
| 1g 실측(I-6 `go_1g_check_2026-09-03.txt`:15, 09:24) | 93 / 10,383 | 파일 0 · 줄 +1 | **[확정 — master git 대조]** `2026-09-02-v2-master-plan.md` 811(1g 시점 HEAD `8d9362f`, `git show`) → 812(v5.2 Correction History 행 추가, commit `f0c381b` 09:26:07) = +1 · 검수 AUD-07 의 mtime 09:26:07 과 일치 → DQ-9 닫힘 |
| master 재실측(§2.9 L195 · Assumptions 12 L608) | 92 / 9,567 | 파일 +1 · 줄 +817 | [확정] `2026-09-02-v2-master-plan.md` 812줄 — 집계 시점 미존재(§2.8 L189 "신규 예정 … master 최종 저장") · [확정] `plans/INDEX.md` 65 → 69 (+4: v1.0.27 행 L10–13 추가, I-3 정독) → 9,567 + 811(1g 시점) + 4 = 10,382 vs 1g 10,383(차 1 = master 9,567 집계와 1g 총계의 방식 차이 — 파일 미특정 · 정본은 본 실측 10,384 = 1g 10,383 + 계획서 +1) |
| brief §3-C(§2.9 L195 인용) | 90 / 9,567 | 파일 +3 · 줄 +817 | 줄수가 master 와 동일하므로 [추정] 건수만 `MASTER_ROADMAP_*` 2본(320·131) 또는 `INDEX.md` 계수 기준 차이 · 근거 미발견 |
| v1 sub(§2.9 L195) | 91 / 9,503 | 파일 +2 · 줄 +881 | [추정] 91 = 날짜 계획서 89 + `MASTER_ROADMAP_*` 2(`INDEX.md` 제외) · 9,503 ≈ 9,567 − 65(INDEX) + 1(정의 차) — 근거 미발견 |

### 3.2 HANDOVER — 실측 정본 = **old/ 제외 25 파일 · 1,612 줄** · old/ 포함 **28 · 1,915**

- 1g(I-6:15) 25/1,612 · master §2.9 L197 25/1,612 · Assumptions 12 L608 25/1,612 — **일치**(확정).
- brief §3-C "28본(old/ 제외)·1,612줄" → **오기 확정**: 28 은 old/ 3본 포함 건수이고 1,612 는 old/ 제외 줄수다(건수·줄수의 기준 불일치). old/ 3본 = `HANDOVER_RB_2026-05-31.md` 90 · `HANDOVER_RB_2026-06-02.md` 129 · `HANDOVER_RB_2026-06-02b.md` 84 = 303줄 → 1,612 + 303 = 1,915.
- 25 의 구성: `docs/` 20(v1.0.10~v1.0.25.1 — `HANDOVER_v24.md` ×4 · `HANDOVER_v25.md` ×2 포함) + `results/comp_v26_data/` 1 + `results/process/` 4. hash 고유본 = 25 − 3(v24 사본) − 1(v25 사본) = 21본(§4).

### 3.3 PLAN_* — 실측 정본 = **15 파일 · 645 줄** + `2026-07-16-v1020-master-plan.md` 207줄

- brief "15 + 1" · §2.9 L196 "15 + 1" · 1g A11/12 "PLAN_* 15" — **일치**(확정). 줄수는 brief 미실측 → 본 실측이 첫 정본.

### 3.4 `CLAUDE.md` — 실측 정본 = **88 줄**(7,380 B)

| 출처 | 수치 | 판정 |
|---|---|---|
| TSV(본 실측, `(Get-Content).Count`) | 88 | **정본**(brief §3.1 줄수 정의) |
| R3 Read Coverage(`R3_binding_decisions_and_lost_directions.md`:368 "1–89(전건) · brief 표기 90줄, 실측 89행") | 89 | 같은 파일의 Read 도구 표기(+1) — 파일 끝 CRLF 개행 실측 True(확정) |
| brief §3.4 · 마스터 플랜 §2.0 L43 "90(R3 실측 89)" | 90 | **오기 확정**(AUD-08: 파일 mtime 2026-07-26 22:56 이후 무변경 · LF = CRLF = `wc -l` = 88 — "실물이 달랐다" 가설 기각) → 마스터 플랜 §2.0 정정(v5.3) |

### 3.5 그 밖의 brief §4 기대치 대조(줄수 정의 −1 이 아닌 것만 굵게)

| 군 | 기대 | 실측 | 판정 |
|---|---|---|---|
| (iv) Fable | 8·885 | 8·885 | 일치(1g 도 885 — 1g 가 같은 정의로 측정했다는 증거) |
| (v) CLOSING | 106 | 105 | 정의 −1 |
| (vi) INDEX | 197·65·139 | 196·**69**·138 | docs·v25 는 정의 −1 · **plans/INDEX.md +4 = 실제 갱신**(v1.0.27 행) |
| (vii) results ledger | 30(2·26·2) | 30(2·26·2)·1,075 | 일치 |
| (x) dossier·jcp | 50·724 | 49·**725** | dossier 정의 −1 · **jcp_extract +1** = 끝 개행 없음(LF 724 + 마지막 무개행 행 1 — 확정, AUD-06) |
| (xi) v1.0.26 | 199·193·50·36 | 198·192·49·36 | 정의 −1(build.log 는 일치) |
| (xii) 서지 원장 | 55·38·33·33 | 54·37·32·32 | 정의 −1 |
| (xvi) 현행 tex | 60·9,214 | 60·9,214 | 일치(1g A2 동일) |
| (xviii) v1.0.25 tex | 60 · diff 10(1g A3, tex+md+pdf) | 60·9,207 · tex diff 6 | 일치(10 − ARCHIVE_NOTE 1 − PDF 3 = 6) |
| (xvii) 유실 원문 | 5본·바이트 5종 | 5본 · 183,693/205,225/218,389/153,592/156,166 B | 일치(Assumptions 23) |
| untracked | Claude 8 / Codex 13 | Claude 8 존재 확인 / Codex 13 무접근 | §5 |

## 4. hash 중복 그룹(TSV SHA256 동일 · 전건)

고유본 규칙(brief §3.3): 가장 이른 버전 폴더(`v1.0.NN(.M)` 최소)의 것 = 계보상 원본. 버전 폴더가 없는 구성원끼리는 경로 정렬 최상(예: `old/` < `results/`) — **정렬 의미론 = ordinal(문자 코드)** 로 명시(iter_2 AUD-12: PowerShell culture 정렬은 `_` < `.` 이라 2 그룹에서 결과가 달랐다). 같은 폴더 안 동명이물 2건은 파일명 의미(base < rerun/fix)로 master 가 수동 지정: #179 고유본 = `REVIEW_LEDGER_CH2_10ROUND.md`, #239 고유본 = `graphite_ica_chapter2.tex`. 이 규칙을 현행 tex 60 에 적용하면 v1.0.24 사본이 고유본이 되므로 **정독 경로는 현행 `v1.0.25.1` 을 쓰되 등록부 표기는 DQ-4** 에서 확정한다. 표기 = 동일 파일명이면 "동명 파일명 @ 폴더 목록", 아니면 전체 경로.

그룹 수 = 259 · 관련 파일 수 = 769

| # | hash(앞 16) | n | 줄수 | 고유본 | 사본 |
|---|---|---|---|---|---|
| 1 | A8EA55A67A4B703E | 8 | 137 | `Claude/docs/v1.0.20/FITTING_GUIDE.md` | 동명 `FITTING_GUIDE.md` @ Claude/docs/v1.0.21 · Claude/docs/v1.0.22 · Claude/docs/v1.0.23 · Claude/docs/v1.0.24 · Claude/docs/v1.0.24.1 · Claude/docs/v1.0.25 · Claude/docs/v1.0.25.1 |
| 2 | 33656A3279D2383C | 7 | 56 | `Claude/docs/v1.0.21/_sections/ch2_preamble.tex` | 동명 `ch2_preamble.tex` @ Claude/docs/v1.0.22/_sections · Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 3 | C34460DF5E6BE301 | 7 | 497 | `Claude/docs/v1.0.21/appendix_phase_separation.tex` | 동명 `appendix_phase_separation.tex` @ Claude/docs/v1.0.22 · Claude/docs/v1.0.23 · Claude/docs/v1.0.24 · Claude/docs/v1.0.24.1 · Claude/docs/v1.0.25 · Claude/docs/v1.0.25.1 |
| 4 | E4CB3D0013E60FC7 | 7 | 77 | `Claude/docs/v1.0.21/_sections/ch1_preamble.tex` | 동명 `ch1_preamble.tex` @ Claude/docs/v1.0.22/_sections · Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 5 | 7AA8430935DA39F2 | 6 | 29 | `Claude/docs/v1.0.22/_sections/ch2_sec10_closing.tex` | 동명 `ch2_sec10_closing.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 6 | 7E078F89EE44B233 | 6 | 89 | `Claude/docs/v1.0.22/_sections/ch1_appA_signcheck.tex` | 동명 `ch1_appA_signcheck.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 7 | 8E82733CC45642E2 | 6 | 75 | `Claude/docs/v1.0.22/_sections/ch2_appA_traps.tex` | 동명 `ch2_appA_traps.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 8 | B27483A2387B64CD | 6 | 14 | `Claude/docs/v1.0.22/_sections/ch1v22_partT_divider.tex` | 동명 `ch1v22_partT_divider.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 9 | BE34894A33A010CE | 6 | 14 | `Claude/docs/v1.0.22/_sections/ch2v22_notation.tex` | 동명 `ch2v22_notation.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 10 | DB67D86510E8D5D9 | 6 | 21 | `Claude/docs/v1.0.22/_sections/ch2v22_bib.tex` | 동명 `ch2v22_bib.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 11 | F83604C5DEFF8C9E | 6 | 170 | `Claude/docs/v1.0.22/results/tools_check_structure.py` | 동명 `tools_check_structure.py` @ Claude/docs/v1.0.23/results · Claude/docs/v1.0.24/results · Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 12 | FE0B1EA4611ECC57 | 6 | 70 | `Claude/docs/v1.0.22/_sections/ch1_sec16_lcopeak.tex` | 동명 `ch1_sec16_lcopeak.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 13 | B93CCC2A1205AF77 | 5 | 533 | `Claude/docs/v1.0.19/build_ch2_rp1_p2.log` | `Claude/docs/v1.0.19/build_ch2_rp1_p3.log` · `Claude/docs/v1.0.19/build_ch2_rp1b_p1.log` · `Claude/docs/v1.0.19/build_ch2_rp1b_p2.log` · `Claude/docs/v1.0.19/build_ch2_rp1b_p3.log` |
| 14 | 04F7ECDA8FA10363 | 4 | 141 | `Claude/docs/v1.0.24/results/comp_R1/W1/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W1 · Claude/docs/v1.0.25/results/comp_R1/W1 · Claude/docs/v1.0.25.1/results/comp_R1/W1 |
| 15 | 08E6CC4FBAB64F33 | 4 | 118 | `Claude/docs/v1.0.24/_sections/ch2_sec03_vibel.tex` | 동명 `ch2_sec03_vibel.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 16 | 0E2DD08FCA4F930D | 4 | 149 | `Claude/docs/v1.0.24/results/comp_R1/W9/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W9 · Claude/docs/v1.0.25/results/comp_R1/W9 · Claude/docs/v1.0.25.1/results/comp_R1/W9 |
| 17 | 109CBBFF5B9E20D0 | 4 | 67 | `Claude/docs/v1.0.24/results/comp_R1/W4/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W4 · Claude/docs/v1.0.25/results/comp_R1/W4 · Claude/docs/v1.0.25.1/results/comp_R1/W4 |
| 18 | 1B5B404FBBA779E3 | 4 | 632 | `Claude/docs/v1.0.24/test_gates_v1024.py` | 동명 `test_gates_v1024.py` @ Claude/docs/v1.0.24.1 · Claude/docs/v1.0.25 · Claude/docs/v1.0.25.1 |
| 19 | 1BB41B578C9CC601 | 4 | 59 | `Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md` | 동명 `REFLECT_SEED_TABLE.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 20 | 23029AD109950169 | 4 | 178 | `Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W1 · Claude/docs/v1.0.25/results/comp_R1/W1 · Claude/docs/v1.0.25.1/results/comp_R1/W1 |
| 21 | 255FF17F55EB5DCC | 4 | 110 | `Claude/docs/v1.0.24/_sections/ch3v22_sec04_mech.tex` | 동명 `ch3v22_sec04_mech.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 22 | 264E426D7E050ECE | 4 | 119 | `Claude/docs/v1.0.24/results/comp_R1/W2/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W2 · Claude/docs/v1.0.25/results/comp_R1/W2 · Claude/docs/v1.0.25.1/results/comp_R1/W2 |
| 23 | 272A30AAA54C060D | 4 | 120 | `Claude/docs/v1.0.24/results/comp_R1/W1/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W1 · Claude/docs/v1.0.25/results/comp_R1/W1 · Claude/docs/v1.0.25.1/results/comp_R1/W1 |
| 24 | 2748C6505B4B2A26 | 4 | 56 | `Claude/docs/v1.0.24/_sections/ch1v22_bib.tex` | 동명 `ch1v22_bib.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 25 | 27FD5A1D5BB99929 | 4 | 190 | `Claude/docs/v1.0.24/_sections/ch2_sec02_config.tex` | 동명 `ch2_sec02_config.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 26 | 2B031FF1AA17512C | 4 | 244 | `Claude/docs/v1.0.24/_sections/ch1_sec01_n0n1.tex` | 동명 `ch1_sec01_n0n1.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 27 | 2B75EAC952961C0E | 4 | 76 | `Claude/docs/v1.0.24/results/comp_R1/W3/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W3 · Claude/docs/v1.0.25/results/comp_R1/W3 · Claude/docs/v1.0.25.1/results/comp_R1/W3 |
| 28 | 2EDEB4D759BF69A1 | 4 | 89 | `Claude/docs/v1.0.24/results/comp_R1/refine_b/lco_omega_b_NOTE.md` | 동명 `lco_omega_b_NOTE.md` @ Claude/docs/v1.0.24.1/results/comp_R1/refine_b · Claude/docs/v1.0.25/results/comp_R1/refine_b · Claude/docs/v1.0.25.1/results/comp_R1/refine_b |
| 29 | 377AAB7CD71B2908 | 4 | 172 | `Claude/docs/v1.0.24/results/comp_R1/W6/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W6 · Claude/docs/v1.0.25/results/comp_R1/W6 · Claude/docs/v1.0.25.1/results/comp_R1/W6 |
| 30 | 37D14450C2ABEB4C | 4 | 176 | `Claude/docs/v1.0.24/_sections/ch1_sec17_msmr.tex` | 동명 `ch1_sec17_msmr.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 31 | 3C47F20AFF51C8C8 | 4 | 390 | `Claude/docs/v1.0.24/_sections/ch1_sec02a_part0.tex` | 동명 `ch1_sec02a_part0.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 32 | 404912C0CDED290E | 4 | 157 | `Claude/docs/v1.0.24/results/comp_R1/W5/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W5 · Claude/docs/v1.0.25/results/comp_R1/W5 · Claude/docs/v1.0.25.1/results/comp_R1/W5 |
| 33 | 457499EFFAB1A66F | 4 | 134 | `Claude/docs/v1.0.24/results/comp_R1/W1/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W1 · Claude/docs/v1.0.25/results/comp_R1/W1 · Claude/docs/v1.0.25.1/results/comp_R1/W1 |
| 34 | 48D4F24E7AA4FDEA | 4 | 160 | `Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex` | 동명 `ch1_sec16b_lcoomega.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 35 | 4A6B4A559E3D4927 | 4 | 53 | `Claude/docs/v1.0.24/_sections/ch2_sec06_limits.tex` | 동명 `ch2_sec06_limits.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 36 | 4D67057431500626 | 4 | 82 | `Claude/docs/v1.0.24/results/comp_R1/W4/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W4 · Claude/docs/v1.0.25/results/comp_R1/W4 · Claude/docs/v1.0.25.1/results/comp_R1/W4 |
| 37 | 4E022FC635DD7F20 | 4 | 170 | `Claude/docs/v1.0.24/results/comp_R1/refine_b/si_fr_b.tex` | 동명 `si_fr_b.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/refine_b · Claude/docs/v1.0.25/results/comp_R1/refine_b · Claude/docs/v1.0.25.1/results/comp_R1/refine_b |
| 38 | 562D21E405666DE7 | 4 | 103 | `Claude/docs/v1.0.24/results/comp_R1/W7/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W7 · Claude/docs/v1.0.25/results/comp_R1/W7 · Claude/docs/v1.0.25.1/results/comp_R1/W7 |
| 39 | 5A5FA421334B4938 | 4 | 95 | `Claude/docs/v1.0.24/results/comp_R1/W3/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W3 · Claude/docs/v1.0.25/results/comp_R1/W3 · Claude/docs/v1.0.25.1/results/comp_R1/W3 |
| 40 | 5B9BA7D25C1C04F4 | 4 | 94 | `Claude/docs/v1.0.24/results/comp_R1/W5/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W5 · Claude/docs/v1.0.25/results/comp_R1/W5 · Claude/docs/v1.0.25.1/results/comp_R1/W5 |
| 41 | 625F11B68AAA1CA8 | 4 | 121 | `Claude/docs/v1.0.24/_sections/ch1_sec03_center.tex` | 동명 `ch1_sec03_center.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 42 | 629BF3676E48D693 | 4 | 41 | `Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md` | 동명 `CHERRYPICK_R1.md` @ Claude/docs/v1.0.24.1/results/comp_R1 · Claude/docs/v1.0.25/results/comp_R1 · Claude/docs/v1.0.25.1/results/comp_R1 |
| 43 | 63B916E21B22AFD8 | 4 | 12 | `Claude/docs/v1.0.24/_sections/ch3v22_sec00_intro.tex` | 동명 `ch3v22_sec00_intro.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 44 | 63F4DF11CFBC508F | 4 | 64 | `Claude/docs/v1.0.24/_sections/ch2_sec09_method.tex` | 동명 `ch2_sec09_method.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 45 | 68E09C34AF57E4F1 | 4 | 97 | `Claude/docs/v1.0.24/results/comp_R1/W7/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W7 · Claude/docs/v1.0.25/results/comp_R1/W7 · Claude/docs/v1.0.25.1/results/comp_R1/W7 |
| 46 | 72EE563058016C5B | 4 | 278 | `Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex` | 동명 `ch3v22_sec03_blend.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 47 | 7317304A7CB77A81 | 4 | 62 | `Claude/docs/v1.0.24/results/comp_R1/W4/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W4 · Claude/docs/v1.0.25/results/comp_R1/W4 · Claude/docs/v1.0.25.1/results/comp_R1/W4 |
| 48 | 73387A1AA2073058 | 4 | 71 | `Claude/docs/v1.0.24/_sections/ch2_sec00_intro.tex` | 동명 `ch2_sec00_intro.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 49 | 75C87FD395C13BEA | 4 | 116 | `Claude/docs/v1.0.24/results/comp_R1/W6/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W6 · Claude/docs/v1.0.25/results/comp_R1/W6 · Claude/docs/v1.0.25.1/results/comp_R1/W6 |
| 50 | 80ADB34A566DB4C9 | 4 | 129 | `Claude/docs/v1.0.24/_sections/ch3v22_sec01_map.tex` | 동명 `ch3v22_sec01_map.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 51 | 869DD1A428729082 | 4 | 121 | `Claude/docs/v1.0.24/results/comp_R1/W2/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W2 · Claude/docs/v1.0.25/results/comp_R1/W2 · Claude/docs/v1.0.25.1/results/comp_R1/W2 |
| 52 | 86AC77F97D8D592C | 4 | 94 | `Claude/docs/v1.0.24/_sections/ch1_sec00_intro.tex` | 동명 `ch1_sec00_intro.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 53 | 899CED4586D8E90A | 4 | 98 | `Claude/docs/v1.0.24/results/comp_R1/W6/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W6 · Claude/docs/v1.0.25/results/comp_R1/W6 · Claude/docs/v1.0.25.1/results/comp_R1/W6 |
| 54 | 89C7243813D57F01 | 4 | 55 | `Claude/docs/v1.0.24/results/comp_R1/W4/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W4 · Claude/docs/v1.0.25/results/comp_R1/W4 · Claude/docs/v1.0.25.1/results/comp_R1/W4 |
| 55 | 8A69A273536AD87B | 4 | 104 | `Claude/docs/v1.0.24/results/comp_R1/W7/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W7 · Claude/docs/v1.0.25/results/comp_R1/W7 · Claude/docs/v1.0.25.1/results/comp_R1/W7 |
| 56 | 8AEE543B79FA2B70 | 4 | 39 | `Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md` | 동명 `PHASE_R3_RESULT.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 57 | 8CE0B2E64B193D59 | 4 | 149 | `Claude/docs/v1.0.24/_sections/ch2_sec01_partition.tex` | 동명 `ch2_sec01_partition.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 58 | 90494736352E6375 | 4 | 102 | `Claude/docs/v1.0.24/_sections/ch2_sec07_revheat.tex` | 동명 `ch2_sec07_revheat.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 59 | 90D06E9FD57A7FA4 | 4 | 137 | `Claude/docs/v1.0.24/results/comp_R1/W3/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W3 · Claude/docs/v1.0.25/results/comp_R1/W3 · Claude/docs/v1.0.25.1/results/comp_R1/W3 |
| 60 | 91F3835705E5BB7B | 4 | 112 | `Claude/docs/v1.0.24/_sections/ch1_sec12_lcocenter.tex` | 동명 `ch1_sec12_lcocenter.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 61 | 940463992CEEB2E9 | 4 | 1 | `Claude/docs/v1.0.24/results/snapshot_v1024_R0.json` | 동명 `snapshot_v1024_R0.json` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 62 | A032ADCDE3993C5F | 4 | 185 | `Claude/docs/v1.0.24/results/comp_R1/refine_b/gr_2L_b.tex` | 동명 `gr_2L_b.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/refine_b · Claude/docs/v1.0.25/results/comp_R1/refine_b · Claude/docs/v1.0.25.1/results/comp_R1/refine_b |
| 63 | A132E9918F003F2F | 4 | 175 | `Claude/docs/v1.0.24/_sections/ch1_sec11_lcointro.tex` | 동명 `ch1_sec11_lcointro.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 64 | A8DA93FFECC103FF | 4 | 121 | `Claude/docs/v1.0.24/results/comp_R1/W8/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W8 · Claude/docs/v1.0.25/results/comp_R1/W8 · Claude/docs/v1.0.25.1/results/comp_R1/W8 |
| 65 | AAB4407E8D28720D | 4 | 84 | `Claude/docs/v1.0.24/_sections/common_preamble_v1024.tex` | 동명 `common_preamble_v1024.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 66 | ABE37E4BE0B38D0A | 4 | 14 | `Claude/docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md` | 동명 `V1024_REFLECT_EXECUTION_LEDGER.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 67 | AC5C213A379B4F85 | 4 | 474 | `Claude/docs/v1.0.24/_sections/ch1_sec02b_part0.tex` | 동명 `ch1_sec02b_part0.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 68 | ACC2A414C2BA6466 | 4 | 54 | `Claude/docs/v1.0.24/results/comp_R1/AUTHOR_BRIEF.md` | 동명 `AUTHOR_BRIEF.md` @ Claude/docs/v1.0.24.1/results/comp_R1 · Claude/docs/v1.0.25/results/comp_R1 · Claude/docs/v1.0.25.1/results/comp_R1 |
| 69 | AE2173D8D9E9774E | 4 | 59 | `Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md` | 동명 `MERGE_READINESS_v24.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 70 | B11D6EC245A72D3E | 4 | 53 | `Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md` | 동명 `PHASE_R1_RESULT.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 71 | B1545353321335C5 | 4 | 374 | `Claude/docs/v1.0.24/CODE_GUIDE_v24.md` | 동명 `CODE_GUIDE_v24.md` @ Claude/docs/v1.0.24.1 · Claude/docs/v1.0.25 · Claude/docs/v1.0.25.1 |
| 72 | B1921E22F267F547 | 4 | 223 | `Claude/docs/v1.0.24/_sections/ch1_sec13_lcohys.tex` | 동명 `ch1_sec13_lcohys.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 73 | B3E9A81F7472AB63 | 4 | 49 | `Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md` | 동명 `PHASE_R2_RESULT.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 74 | B63E14147AADD3E1 | 4 | 125 | `Claude/docs/v1.0.24/results/comp_R1/W9/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W9 · Claude/docs/v1.0.25/results/comp_R1/W9 · Claude/docs/v1.0.25.1/results/comp_R1/W9 |
| 75 | B6E22FB9FE4C68A9 | 4 | 91 | `Claude/docs/v1.0.24/_sections/ch1_appD_si.tex` | 동명 `ch1_appD_si.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 76 | B7601F2E08C0972C | 4 | 44 | `Claude/docs/v1.0.24/results/PHASE_R0_RESULT.md` | 동명 `PHASE_R0_RESULT.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 77 | B7F2B9628AF05186 | 4 | 78 | `Claude/docs/v1.0.24/results/comp_R1/W9/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W9 · Claude/docs/v1.0.25/results/comp_R1/W9 · Claude/docs/v1.0.25.1/results/comp_R1/W9 |
| 78 | B828D368F458D2CD | 4 | 152 | `Claude/docs/v1.0.24/results/comp_R1/W8/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W8 · Claude/docs/v1.0.25/results/comp_R1/W8 · Claude/docs/v1.0.25.1/results/comp_R1/W8 |
| 79 | B958E914A2A8D4F9 | 4 | 87 | `Claude/docs/v1.0.24/results/comp_R1/refine_b/si_fr_b_NOTE.md` | 동명 `si_fr_b_NOTE.md` @ Claude/docs/v1.0.24.1/results/comp_R1/refine_b · Claude/docs/v1.0.25/results/comp_R1/refine_b · Claude/docs/v1.0.25.1/results/comp_R1/refine_b |
| 80 | B9F634DDF45F4864 | 4 | 97 | `Claude/docs/v1.0.24/results/comp_R1/W2/NOTES.md` | 동명 `NOTES.md` @ Claude/docs/v1.0.24.1/results/comp_R1/W2 · Claude/docs/v1.0.25/results/comp_R1/W2 · Claude/docs/v1.0.25.1/results/comp_R1/W2 |
| 81 | BE3125226CC89E4D | 4 | 100 | `Claude/docs/v1.0.24/results/comp_R1/W8/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W8 · Claude/docs/v1.0.25/results/comp_R1/W8 · Claude/docs/v1.0.25.1/results/comp_R1/W8 |
| 82 | BFD80F56C2A91409 | 4 | 103 | `Claude/docs/v1.0.24/results/comp_R1/W6/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W6 · Claude/docs/v1.0.25/results/comp_R1/W6 · Claude/docs/v1.0.25.1/results/comp_R1/W6 |
| 83 | C0A3C99D01F698F4 | 4 | 107 | `Claude/docs/v1.0.24/results/comp_R1/W5/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W5 · Claude/docs/v1.0.25/results/comp_R1/W5 · Claude/docs/v1.0.25.1/results/comp_R1/W5 |
| 84 | C5D6344F3AD1069F | 4 | 119 | `Claude/docs/v1.0.24/results/comp_R1/W3/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W3 · Claude/docs/v1.0.25/results/comp_R1/W3 · Claude/docs/v1.0.25.1/results/comp_R1/W3 |
| 85 | C6A87921CC0ACF67 | 4 | 144 | `Claude/docs/v1.0.24/results/comp_R1/W7/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W7 · Claude/docs/v1.0.25/results/comp_R1/W7 · Claude/docs/v1.0.25.1/results/comp_R1/W7 |
| 86 | C846A4926C0DBADB | 4 | 396 | `Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex` | 동명 `ch1_sec15_lcoelec.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 87 | C96A8260B2111F93 | 4 | 70 | `Claude/docs/v1.0.24/_sections/ch3v22_sec05_code.tex` | 동명 `ch3v22_sec05_code.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 88 | C9B0209620570511 | 4 | 88 | `Claude/docs/v1.0.24/results/HANDOVER_v24.md` | 동명 `HANDOVER_v24.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 89 | CD080E27CE41AA54 | 4 | 44 | `Claude/docs/v1.0.24/_sections/ch3v22_bib.tex` | 동명 `ch3v22_bib.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 90 | CD4A90E12DCCA1A8 | 4 | 143 | `Claude/docs/v1.0.24/_sections/ch1_sec14_lcodecomp.tex` | 동명 `ch1_sec14_lcodecomp.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 91 | D01D2CA7F8CE62E2 | 4 | 84 | `Claude/docs/v1.0.24/results/comp_R1/refine_b/gr_2L_b_NOTE.md` | 동명 `gr_2L_b_NOTE.md` @ Claude/docs/v1.0.24.1/results/comp_R1/refine_b · Claude/docs/v1.0.25/results/comp_R1/refine_b · Claude/docs/v1.0.25.1/results/comp_R1/refine_b |
| 92 | D2C80A7E8C32E1FC | 4 | 115 | `Claude/docs/v1.0.24/results/v1024_final_sample.py` | 동명 `v1024_final_sample.py` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 93 | D5FF02A5C3B2C11B | 4 | 336 | `Claude/docs/v1.0.24/_sections/ch1_sec04_hys.tex` | 동명 `ch1_sec04_hys.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 94 | D6F44BE298EC0C67 | 4 | 207 | `Claude/docs/v1.0.24/_sections/ch2_sec04_einstein.tex` | 동명 `ch2_sec04_einstein.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 95 | E28116093399A57B | 4 | 111 | `Claude/docs/v1.0.24/results/comp_R1/W5/lco_omega.tex` | 동명 `lco_omega.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W5 · Claude/docs/v1.0.25/results/comp_R1/W5 · Claude/docs/v1.0.25.1/results/comp_R1/W5 |
| 96 | E3590093DC2F8AA9 | 4 | 70 | `Claude/docs/v1.0.22/_sections/ch1_sec18_inputs.tex` | 동명 `ch1_sec18_inputs.tex` @ Claude/docs/v1.0.23/_sections · Claude/docs/v1.0.24/_sections · Claude/docs/v1.0.24.1/_sections |
| 97 | E35FE8FFD76BA51B | 4 | 40 | `Claude/docs/v1.0.24/results/v1024_reflect_curves.py` | 동명 `v1024_reflect_curves.py` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 98 | E69E16A39529CD37 | 4 | 142 | `Claude/docs/v1.0.24/results/comp_R1/W2/gr_2L.tex` | 동명 `gr_2L.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W2 · Claude/docs/v1.0.25/results/comp_R1/W2 · Claude/docs/v1.0.25.1/results/comp_R1/W2 |
| 99 | E82C90C581D316E0 | 4 | 97 | `Claude/docs/v1.0.24/results/comp_R1/W8/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W8 · Claude/docs/v1.0.25/results/comp_R1/W8 · Claude/docs/v1.0.25.1/results/comp_R1/W8 |
| 100 | EF231A4FA3BEA771 | 4 | 63 | `Claude/docs/v1.0.24/results/INDEX_v24.md` | 동명 `INDEX_v24.md` @ Claude/docs/v1.0.24.1/results · Claude/docs/v1.0.25/results · Claude/docs/v1.0.25.1/results |
| 101 | F08FD3DADDFA8942 | 4 | 164 | `Claude/docs/v1.0.24/results/comp_R1/refine_b/lco_omega_b.tex` | 동명 `lco_omega_b.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/refine_b · Claude/docs/v1.0.25/results/comp_R1/refine_b · Claude/docs/v1.0.25.1/results/comp_R1/refine_b |
| 102 | F0C73DB1CB3D81B9 | 4 | 119 | `Claude/docs/v1.0.24/results/comp_R1/W9/si_fr.tex` | 동명 `si_fr.tex` @ Claude/docs/v1.0.24.1/results/comp_R1/W9 · Claude/docs/v1.0.25/results/comp_R1/W9 · Claude/docs/v1.0.25.1/results/comp_R1/W9 |
| 103 | F8955ACD28B384C1 | 4 | 128 | `Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py` | 동명 `test_gates_v1024_selfconsistent.py` @ Claude/docs/v1.0.24.1 · Claude/docs/v1.0.25 · Claude/docs/v1.0.25.1 |
| 104 | F9266437EDC55AD7 | 4 | 46 | `Claude/docs/v1.0.24/_sections/ch3v22_notation.tex` | 동명 `ch3v22_notation.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 105 | FAD5BD692812F6C0 | 4 | 12 | `Claude/docs/v1.0.24/_sections/ch2v22_sec00_intro.tex` | 동명 `ch2v22_sec00_intro.tex` @ Claude/docs/v1.0.24.1/_sections · Claude/docs/v1.0.25/_sections · Claude/docs/v1.0.25.1/_sections |
| 106 | 53D297A738672516 | 3 | 628 | `Claude/results/builds/v9/v9-11/FINAL_p1.log` | `Claude/results/builds/v9/v9-11/FINAL_p2.log` · `Claude/results/builds/v9/v9-11/FINAL_p3.log` |
| 107 | 6262C5BD18FE5F68 | 3 | 1644 | `Claude/old/Ch1_v9/graphite_ica_ch1_v9.tex` | `Claude/results/builds/ch1v10/v10-00_spine/base_v9.tex` · `Claude/results/builds/v9/v9-11/v9-11.tex` |
| 108 | 72AF6EB9530475B7 | 3 | 628 | `Claude/results/builds/v9/v9-11/final_pass1.log` | `Claude/results/builds/v9/v9-11/final_pass2.log` · `Claude/results/builds/v9/v9-11/final_pass3.log` |
| 109 | 97ABAB86473F41BF | 3 | 135 | `Claude/docs/v1.0.10/plot_dqdv.py` | 동명 `plot_dqdv.py` @ Claude/docs/v1.0.11 · Claude/docs/v1.0.12 |
| 110 | A099B62C3F60C151 | 3 | 115 | `Claude/docs/v1.0.16/FITTING_GUIDE.md` | 동명 `FITTING_GUIDE.md` @ Claude/docs/v1.0.17 · Claude/docs/v1.0.18.1 |
| 111 | B12AF2BCE63016D4 | 3 | 80 | `Claude/docs/v1.0.10/test_regression_graphite.py` | 동명 `test_regression_graphite.py` @ Claude/docs/v1.0.11 · Claude/docs/v1.0.12 |
| 112 | B302CB72B9A9EF90 | 3 | 1208 | `Claude/old/Ch1_v8/v8-11.tex` | `Claude/results/builds/v8/v8-11/v8-11.tex` · `Claude/results/builds/v9/v9-00_spine/base_v8-11.tex` |
| 113 | CF7C571E77C2A6ED | 3 | 930 | `Claude/docs/v1.0.16/Anode_Fit_v1.0.16.py` | `Claude/docs/v1.0.17/Anode_Fit_v1.0.17.py` · `Claude/docs/v1.0.18.1/Anode_Fit_v1.0.18.1.py` |
| 114 | E09D1BB2528EEE4E | 3 | 955 | `Claude/docs/v1.0.19/build_ch1_rp1b_p1.log` | `Claude/docs/v1.0.19/build_ch1_rp1b_p2.log` · `Claude/docs/v1.0.19/build_ch1_rp1b_p3.log` |
| 115 | EB152719B58D83AB | 3 | 91 | `Claude/docs/v1.0.21/_sections/ch1_appD_si.tex` | 동명 `ch1_appD_si.tex` @ Claude/docs/v1.0.22/_sections · Claude/docs/v1.0.23/_sections |
| 116 | F8636A7FE73E8E69 | 3 | 72 | `Claude/docs/v1.0.10/demo_lco_heat.py` | 동명 `demo_lco_heat.py` @ Claude/docs/v1.0.11 · Claude/docs/v1.0.12 |
| 117 | 0A05BEDE39563FFF | 2 | 102 | `Claude/docs/v1.0.22/_sections/ch2_sec07_revheat.tex` | 동명 `ch2_sec07_revheat.tex` @ Claude/docs/v1.0.23/_sections |
| 118 | 0FD6E7B14F2871BB | 2 | 112 | `Claude/docs/v1.0.20/_sections/ch1_sec12_lcocenter.tex` | 동명 `ch1_sec12_lcocenter.tex` @ Claude/docs/v1.0.21/_sections |
| 119 | 10E336598EC8C8BF | 2 | 176 | `Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex` | 동명 `ch3v22_sec02b_sifr.tex` @ Claude/docs/v1.0.24.1/_sections |
| 120 | 11DEC25A12CD5DF7 | 2 | 60 | `Claude/docs/v1.0.24/ch1_graphite_v1.0.24.tex` | 동명 `ch1_graphite_v1.0.24.tex` @ Claude/docs/v1.0.24.1 |
| 121 | 12739D854B261959 | 2 | 238 | `Claude/docs/v1.0.25/_sections/ch1_sec05b_gr2L.tex` | 동명 `ch1_sec05b_gr2L.tex` @ Claude/docs/v1.0.25.1/_sections |
| 122 | 16E50EABBF654003 | 2 | 535 | `Claude/results/builds/v8/v8-04/final.log` | `Claude/results/builds/v8/v8-04/pass2.log` |
| 123 | 1A386DE5C357EE0E | 2 | 51 | `Claude/docs/v1.0.26B-gallery/params/params_silicon.json` | 동명 `params_silicon.json` @ Claude/results/comp_v26_data/out_versions/B_gallery |
| 124 | 1A665225CB4E0EE3 | 2 | 519 | `Claude/docs/v1.0.19/build_ch2_p2.log` | `Claude/docs/v1.0.19/build_ch2_p3.log` |
| 125 | 1B154D25B84CD27A | 2 | 165 | `Claude/docs/v1.0.20/results/tools_check_structure.py` | 동명 `tools_check_structure.py` @ Claude/docs/v1.0.21/results |
| 126 | 1BE0657EEFDC5971 | 2 | 947 | `Claude/old/_archive/Archive_rebuilt/graphite_ica_ch2_rebuilt.tex` | 동명 `graphite_ica_ch2_rebuilt.tex` @ Claude/old/work/oldtrack_src |
| 127 | 20992FC7154DFC53 | 2 | 94 | `Claude/docs/v1.0.10/sample_test_v1010.py` | `Claude/docs/v1.0.11/sample_test_v1011.py` |
| 128 | 20FAA61C725BBD5E | 2 | 15 | `Claude/old/work/roundtrip_log_2026-06-10.txt` | 동명 `roundtrip_log_2026-06-10.txt` @ Claude/results/process/TBR_R17_roundtrip |
| 129 | 211047BB32FDF9D7 | 2 | 307 | `Claude/docs/v1.0.20/_sections/ch1_sec07_broadening.tex` | 동명 `ch1_sec07_broadening.tex` @ Claude/docs/v1.0.21/_sections |
| 130 | 252BE1A6F4ADCD7E | 2 | 202 | `Claude/docs/v1.0.25/results/tools_tex_strict_check.py` | 동명 `tools_tex_strict_check.py` @ Claude/docs/v1.0.25.1/results |
| 131 | 259612430743E36B | 2 | 75 | `Claude/docs/v1.0.22/_sections/ch2_appB_codemap.tex` | 동명 `ch2_appB_codemap.tex` @ Claude/docs/v1.0.23/_sections |
| 132 | 2CED16E629AB578A | 2 | 99 | `Claude/docs/v1.0.14/FITTING_GUIDE.md` | 동명 `FITTING_GUIDE.md` @ Claude/docs/v1.0.15 |
| 133 | 32304CE517A467E1 | 2 | 118 | `Claude/docs/v1.0.22/_sections/ch2_sec03_vibel.tex` | 동명 `ch2_sec03_vibel.tex` @ Claude/docs/v1.0.23/_sections |
| 134 | 34088C6FA5260070 | 2 | 162 | `Claude/docs/v1.0.24/_sections/ch3v22_sec02_cases.tex` | 동명 `ch3v22_sec02_cases.tex` @ Claude/docs/v1.0.24.1/_sections |
| 135 | 3552631A1B676F53 | 2 | 207 | `Claude/docs/v1.0.22/_sections/ch2_sec04_einstein.tex` | 동명 `ch2_sec04_einstein.tex` @ Claude/docs/v1.0.23/_sections |
| 136 | 376A5E295AA187EF | 2 | 89 | `Claude/docs/v1.0.22/_sections/ch1_sec06_eqpeak.tex` | 동명 `ch1_sec06_eqpeak.tex` @ Claude/docs/v1.0.23/_sections |
| 137 | 39A5BCF2A000CBAC | 2 | 12 | `Claude/docs/v1.0.22/_sections/ch3v22_sec00_intro.tex` | 동명 `ch3v22_sec00_intro.tex` @ Claude/docs/v1.0.23/_sections |
| 138 | 40D174AD24ACC6FE | 2 | 74 | `Claude/docs/v1.0.20/_sections/ch2_appA_traps.tex` | 동명 `ch2_appA_traps.tex` @ Claude/docs/v1.0.21/_sections |
| 139 | 425347A1CFCEF987 | 2 | 231 | `Claude/docs/v1.0.22/_sections/ch2_sec08_synthesis.tex` | 동명 `ch2_sec08_synthesis.tex` @ Claude/docs/v1.0.23/_sections |
| 140 | 42A10DE9092A6FBB | 2 | 415 | `Claude/docs/v1.0.24/_sections/ch1_sec05_width.tex` | 동명 `ch1_sec05_width.tex` @ Claude/docs/v1.0.24.1/_sections |
| 141 | 44247D3564180E35 | 2 | 138 | `Claude/docs/v1.0.25/results/INDEX_v25.md` | 동명 `INDEX_v25.md` @ Claude/docs/v1.0.25.1/results |
| 142 | 44DE49AA0BE0FDE3 | 2 | 391 | `Claude/docs/v1.0.22/_sections/ch1_sec02a_part0.tex` | 동명 `ch1_sec02a_part0.tex` @ Claude/docs/v1.0.23/_sections |
| 143 | 47988F981D45D709 | 2 | 245 | `Claude/docs/v1.0.24/_sections/ch2_sec05_mixing.tex` | 동명 `ch2_sec05_mixing.tex` @ Claude/docs/v1.0.24.1/_sections |
| 144 | 47C9F0745A26C01D | 2 | 1004 | `Claude/old/_archive/Archive_rebuilt/graphite_ica_ch4_rebuilt.tex` | 동명 `graphite_ica_ch4_rebuilt.tex` @ Claude/old/work/oldtrack_src |
| 145 | 47D8BE1B768C073C | 2 | 357 | `Claude/docs/v1.0.22/_sections/ch1_sec07_broadening.tex` | 동명 `ch1_sec07_broadening.tex` @ Claude/docs/v1.0.23/_sections |
| 146 | 4B314F0B68C4FF1D | 2 | 46 | `Claude/docs/v1.0.10/FITTING_GUIDE.md` | 동명 `FITTING_GUIDE.md` @ Claude/docs/v1.0.11 |
| 147 | 4BAE320F18F7E340 | 2 | 176 | `Claude/docs/v1.0.22/_sections/ch1_sec17_msmr.tex` | 동명 `ch1_sec17_msmr.tex` @ Claude/docs/v1.0.23/_sections |
| 148 | 4D4B3AA96868BA15 | 2 | 89 | `Claude/docs/v1.0.20/_sections/ch1_appA_signcheck.tex` | 동명 `ch1_appA_signcheck.tex` @ Claude/docs/v1.0.21/_sections |
| 149 | 4E04600CB4431C16 | 2 | 190 | `Claude/docs/v1.0.20/_sections/ch2_sec02_config.tex` | 동명 `ch2_sec02_config.tex` @ Claude/docs/v1.0.21/_sections |
| 150 | 4F2296E54678F916 | 2 | 52 | `Claude/docs/v1.0.26A-regsol/params/params_silicon.json` | 동명 `params_silicon.json` @ Claude/results/comp_v26_data/out_versions/A_regsol |
| 151 | 50D97743074225FE | 2 | 70 | `Claude/docs/v1.0.22/_sections/ch3v22_sec05_code.tex` | 동명 `ch3v22_sec05_code.tex` @ Claude/docs/v1.0.23/_sections |
| 152 | 51DE93A5DAB19F73 | 2 | 345 | `Claude/results/builds/ch2_v4/v4-11/final.log` | `Claude/results/builds/ch2_v4/v4-11/pass2.log` |
| 153 | 527271C6658030F2 | 2 | 706 | `Claude/results/builds/v7/v7-00_spine/Anode_Fit_v11_final.py` | 동명 `Anode_Fit_v11_final.py` @ Claude/results/code |
| 154 | 545C1C2A56CD576D | 2 | 172 | `Claude/docs/v1.0.20/_sections/ch1_sec11_lcointro.tex` | 동명 `ch1_sec11_lcointro.tex` @ Claude/docs/v1.0.21/_sections |
| 155 | 583B8CD3DC82E66B | 2 | 1937 | `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` | `Claude/docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` |
| 156 | 59E685CE4BBFCB60 | 2 | 132 | `Claude/docs/v1.0.22/_sections/ch3v22_sec01_map.tex` | 동명 `ch3v22_sec01_map.tex` @ Claude/docs/v1.0.23/_sections |
| 157 | 5BA1A720EADCE912 | 2 | 916 | `Claude/old/_archive/Archive_rebuilt/graphite_ica_ch3_rebuilt.tex` | 동명 `graphite_ica_ch3_rebuilt.tex` @ Claude/old/work/oldtrack_src |
| 158 | 5EB9F89D3F279150 | 2 | 204 | `Claude/docs/v1.0.25/results/MERGE_READINESS_v25.md` | 동명 `MERGE_READINESS_v25.md` @ Claude/docs/v1.0.25.1/results |
| 159 | 60D02D81E1628BFE | 2 | 257 | `Claude/docs/v1.0.22/_sections/ch1_sec01_n0n1.tex` | 동명 `ch1_sec01_n0n1.tex` @ Claude/docs/v1.0.23/_sections |
| 160 | 65C9070AAF526190 | 2 | 245 | `Claude/docs/v1.0.22/_sections/ch1_sec09_tail.tex` | 동명 `ch1_sec09_tail.tex` @ Claude/docs/v1.0.23/_sections |
| 161 | 676473C5626A2318 | 2 | 182 | `Claude/docs/v1.0.25/results/V1025_DOC_CASCADE_TODO.md` | 동명 `V1025_DOC_CASCADE_TODO.md` @ Claude/docs/v1.0.25.1/results |
| 162 | 6AA941053D0EE7EA | 2 | 492 | `Claude/docs/v1.0.15/appendix_phase_separation.tex` | 동명 `appendix_phase_separation.tex` @ Claude/docs/v1.0.16 |
| 163 | 6AB271198A0220EB | 2 | 396 | `Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex` | 동명 `ch1_sec15_lcoelec.tex` @ Claude/docs/v1.0.23/_sections |
| 164 | 6DF00C51A8B7FCE5 | 2 | 245 | `Claude/docs/v1.0.24/_sections/ch1_sec09_tail.tex` | 동명 `ch1_sec09_tail.tex` @ Claude/docs/v1.0.24.1/_sections |
| 165 | 6FCF9F2AB6F2C8D8 | 2 | 365 | `Claude/docs/v1.0.20/_sections/ch1_sec02a_part0.tex` | 동명 `ch1_sec02a_part0.tex` @ Claude/docs/v1.0.21/_sections |
| 166 | 70E43A8BF6255451 | 2 | 244 | `Claude/docs/v1.0.20/_sections/ch1_sec09_tail.tex` | 동명 `ch1_sec09_tail.tex` @ Claude/docs/v1.0.21/_sections |
| 167 | 7167DE14A3152DF1 | 2 | 143 | `Claude/docs/v1.0.22/_sections/ch1_sec14_lcodecomp.tex` | 동명 `ch1_sec14_lcodecomp.tex` @ Claude/docs/v1.0.23/_sections |
| 168 | 71DA6A640B8DDCAC | 2 | 64 | `Claude/docs/v1.0.25/test_gates_v1024_reflect.py` | 동명 `test_gates_v1024_reflect.py` @ Claude/docs/v1.0.25.1 |
| 169 | 7938D8349D6866BA | 2 | 51 | `Claude/docs/v1.0.26B-gallery/params/params_graphite.json` | 동명 `params_graphite.json` @ Claude/results/comp_v26_data/out_versions/B_gallery |
| 170 | 7BF53D8FF151971F | 2 | 415 | `Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex` | 동명 `ch1_sec05_width.tex` @ Claude/docs/v1.0.23/_sections |
| 171 | 7C61768A9C1488F3 | 2 | 102 | `Claude/docs/v1.0.20/_sections/ch2_sec03_vibel.tex` | 동명 `ch2_sec03_vibel.tex` @ Claude/docs/v1.0.21/_sections |
| 172 | 7E78C10AD9E94C69 | 2 | 52 | `Claude/docs/v1.0.20/_sections/ch2_sec06_limits.tex` | 동명 `ch2_sec06_limits.tex` @ Claude/docs/v1.0.21/_sections |
| 173 | 7F9144FB8092ED3B | 2 | 155 | `Claude/docs/v1.0.24/_sections/ch1_appB_codemap.tex` | 동명 `ch1_appB_codemap.tex` @ Claude/docs/v1.0.24.1/_sections |
| 174 | 80A447E8852C7886 | 2 | 92 | `Claude/docs/v1.0.25/_sections/ch1_sec18_inputs.tex` | 동명 `ch1_sec18_inputs.tex` @ Claude/docs/v1.0.25.1/_sections |
| 175 | 812693BAE05A9651 | 2 | 68 | `Claude/docs/v1.0.20/_sections/ch1_sec18_inputs.tex` | 동명 `ch1_sec18_inputs.tex` @ Claude/docs/v1.0.21/_sections |
| 176 | 8648C3256DA46C54 | 2 | 68 | `Claude/docs/v1.0.20/_sections/ch1_sec16_lcopeak.tex` | 동명 `ch1_sec16_lcopeak.tex` @ Claude/docs/v1.0.21/_sections |
| 177 | 87651C084D035CC4 | 2 | 46 | `Claude/docs/v1.0.22/_sections/ch3v22_notation.tex` | 동명 `ch3v22_notation.tex` @ Claude/docs/v1.0.23/_sections |
| 178 | 8C5102A2461FE7B0 | 2 | 948 | `Claude/docs/v1.0.19/build_ch1_p2.log` | `Claude/docs/v1.0.19/build_ch1_p3.log` |
| 179 | 8D2507EFE83A2C0C | 2 | 85 | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND.md` | `Claude/old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND_CLAUDE_rerun_5-29.md` (iter_2 수동 지정 AUD-12) |
| 180 | 8D2631591E3E6268 | 2 | 398 | `Claude/docs/v1.0.25/test_gates_v1025.py` | 동명 `test_gates_v1025.py` @ Claude/docs/v1.0.25.1 |
| 181 | 8F2B9C2D272A5B79 | 2 | 145 | `Claude/docs/v1.0.24/_sections/ch1_sec08_lag.tex` | 동명 `ch1_sec08_lag.tex` @ Claude/docs/v1.0.24.1/_sections |
| 182 | 8FB6C76A9BE61CFA | 2 | 336 | `Claude/docs/v1.0.22/_sections/ch1_sec04_hys.tex` | 동명 `ch1_sec04_hys.tex` @ Claude/docs/v1.0.23/_sections |
| 183 | 960D1FA9379D046C | 2 | 220 | `Claude/old/work/ch1_fit_roundtrip.py` | 동명 `ch1_fit_roundtrip.py` @ Claude/results/process/TBR_R17_roundtrip |
| 184 | 96E2D329E455756D | 2 | 255 | `Claude/docs/v1.0.25/_sections/ch2_sec05_mixing.tex` | 동명 `ch2_sec05_mixing.tex` @ Claude/docs/v1.0.25.1/_sections |
| 185 | 97EA256B2990A568 | 2 | 53 | `Claude/docs/v1.0.22/_sections/ch2_sec06_limits.tex` | 동명 `ch2_sec06_limits.tex` @ Claude/docs/v1.0.23/_sections |
| 186 | 9A971FA36B6C7D5D | 2 | 170 | `Claude/docs/v1.0.22/_sections/ch1_sec10_sum.tex` | 동명 `ch1_sec10_sum.tex` @ Claude/docs/v1.0.23/_sections |
| 187 | 9B717A8216FF7811 | 2 | 375 | `Claude/docs/v1.0.25/_sections/ch1_sec07_broadening.tex` | 동명 `ch1_sec07_broadening.tex` @ Claude/docs/v1.0.25.1/_sections |
| 188 | 9E9CE209F6558E53 | 2 | 170 | `Claude/docs/v1.0.24/_sections/ch1_sec10_sum.tex` | 동명 `ch1_sec10_sum.tex` @ Claude/docs/v1.0.24.1/_sections |
| 189 | 9F50C35FF3D9A0B6 | 2 | 312 | `Claude/docs/v1.0.25/results/V1025_DOC_EDIT_REPORT.md` | 동명 `V1025_DOC_EDIT_REPORT.md` @ Claude/docs/v1.0.25.1/results |
| 190 | A037D1404E1005B8 | 2 | 43 | `Claude/docs/v1.0.20/_sections/ch2_sec09_method.tex` | 동명 `ch2_sec09_method.tex` @ Claude/docs/v1.0.21/_sections |
| 191 | A0617196797C312D | 2 | 291 | `Claude/docs/v1.0.25/results/V1025_DATA_ADDENDUM.md` | 동명 `V1025_DATA_ADDENDUM.md` @ Claude/docs/v1.0.25.1/results |
| 192 | A1AF50DB540D1485 | 2 | 231 | `Claude/docs/v1.0.24/_sections/ch2_sec08_synthesis.tex` | 동명 `ch2_sec08_synthesis.tex` @ Claude/docs/v1.0.24.1/_sections |
| 193 | A20E9740E1FC3099 | 2 | 32 | `Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md` | `Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md` |
| 194 | A3039AC47E2F5DE8 | 2 | 157 | `Claude/docs/v1.0.20/_sections/ch1_appB_codemap.tex` | 동명 `ch1_appB_codemap.tex` @ Claude/docs/v1.0.21/_sections |
| 195 | A4225F461F894109 | 2 | 157 | `Claude/docs/v1.0.25/results/V1025_CHANGE_LEDGER.md` | 동명 `V1025_CHANGE_LEDGER.md` @ Claude/docs/v1.0.25.1/results |
| 196 | A4BCD1C99CF254CF | 2 | 170 | `Claude/docs/v1.0.25/results/HANDOVER_v25.md` | 동명 `HANDOVER_v25.md` @ Claude/docs/v1.0.25.1/results |
| 197 | A5A4B91E23AC0AA8 | 2 | 474 | `Claude/docs/v1.0.22/_sections/ch1_sec02b_part0.tex` | 동명 `ch1_sec02b_part0.tex` @ Claude/docs/v1.0.23/_sections |
| 198 | A657CA63AC909244 | 2 | 59 | `Claude/docs/v1.0.25/results/tools_gate_forbidden_selftest.py` | 동명 `tools_gate_forbidden_selftest.py` @ Claude/docs/v1.0.25.1/results |
| 199 | A8BA6CB7D375EF35 | 2 | 1917 | `Claude/docs/v1.0.25/Anode_Fit_v1.0.24.py` | 동명 `Anode_Fit_v1.0.24.py` @ Claude/docs/v1.0.25.1 |
| 200 | AABA9664A6BB4C74 | 2 | 487 | `Claude/docs/v1.0.25/results/V1025_T13_T14_REPORT.md` | 동명 `V1025_T13_T14_REPORT.md` @ Claude/docs/v1.0.25.1/results |
| 201 | B14304815D4CA255 | 2 | 86 | `Claude/docs/v1.0.26B-gallery/params/params_blend.json` | 동명 `params_blend.json` @ Claude/results/comp_v26_data/out_versions/B_gallery |
| 202 | B3ECA6E3E3BC6B2F | 2 | 58 | `Claude/docs/v1.0.20/_sections/ch2_sec07_revheat.tex` | 동명 `ch2_sec07_revheat.tex` @ Claude/docs/v1.0.21/_sections |
| 203 | B641C1B19588FBDD | 2 | 128 | `Claude/old/work/v2_r13_tail_roundtrip.py` | 동명 `v2_r13_tail_roundtrip.py` @ Claude/results/process/V2_R13_roundtrip |
| 204 | B73AF55E122E88EF | 2 | 136 | `Claude/docs/v1.0.20/_sections/ch1_sec17_msmr.tex` | 동명 `ch1_sec17_msmr.tex` @ Claude/docs/v1.0.21/_sections |
| 205 | B87229619C7C0AE1 | 2 | 83 | `Claude/docs/v1.0.22/_sections/common_preamble_v1022.tex` | `Claude/docs/v1.0.23/_sections/common_preamble_v1023.tex` |
| 206 | B8AF5699C93C067E | 2 | 42 | `Claude/docs/v1.0.22/_sections/ch3v22_bib.tex` | 동명 `ch3v22_bib.tex` @ Claude/docs/v1.0.23/_sections |
| 207 | B8E5ECB6FE29633E | 2 | 11 | `Claude/docs/v1.0.22/_sections/ch2v22_sec00_intro.tex` | 동명 `ch2v22_sec00_intro.tex` @ Claude/docs/v1.0.23/_sections |
| 208 | BB73ED22E6469D25 | 2 | 759 | `Claude/old/Ch2_v4/graphite_ica_ch2_v4.tex` | `Claude/results/builds/ch2_v4/v4-11/v4-11.tex` |
| 209 | BD5E99902849A251 | 2 | 121 | `Claude/docs/v1.0.22/_sections/ch1_sec03_center.tex` | 동명 `ch1_sec03_center.tex` @ Claude/docs/v1.0.23/_sections |
| 210 | BDE0DB1635D70F48 | 2 | 162 | `Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex` | 동명 `ch3v22_sec02_cases.tex` @ Claude/docs/v1.0.23/_sections |
| 211 | BE0306B829DAE7C0 | 2 | 439 | `Claude/results/builds/ch2_v4/v4-04/b.log` | `Claude/results/builds/ch2_v4/v4-04/b2.log` |
| 212 | BEC003E638322C5D | 2 | 148 | `Claude/docs/v1.0.25/_sections/ch1_sec08_lag.tex` | 동명 `ch1_sec08_lag.tex` @ Claude/docs/v1.0.25.1/_sections |
| 213 | BF5A72188AAA163A | 2 | 253 | `Claude/docs/v1.0.19/build_app_rp1_p1.log` | `Claude/docs/v1.0.19/build_app_rp1_p2.log` |
| 214 | C09F4F6CA6C9D9A2 | 2 | 278 | `Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex` | 동명 `ch3v22_sec03_blend.tex` @ Claude/docs/v1.0.23/_sections |
| 215 | C3E1BDBE38F511F8 | 2 | 241 | `Claude/docs/v1.0.25/results/tools_doc_code_audit.py` | 동명 `tools_doc_code_audit.py` @ Claude/docs/v1.0.25.1/results |
| 216 | C46582420E0377BF | 2 | 238 | `Claude/docs/v1.0.25/_sections/ch2_sec08_synthesis.tex` | 동명 `ch2_sec08_synthesis.tex` @ Claude/docs/v1.0.25.1/_sections |
| 217 | C574A2008C40285C | 2 | 27 | `Claude/docs/v1.0.20/_sections/ch2_bib.tex` | 동명 `ch2_bib.tex` @ Claude/docs/v1.0.21/_sections |
| 218 | C692787DBE1726B5 | 2 | 173 | `Claude/docs/v1.0.25/_sections/ch3v22_sec02_cases.tex` | 동명 `ch3v22_sec02_cases.tex` @ Claude/docs/v1.0.25.1/_sections |
| 219 | CCCF949F10C925A2 | 2 | 253 | `Claude/docs/v1.0.25/_sections/ch1_sec09_tail.tex` | 동명 `ch1_sec09_tail.tex` @ Claude/docs/v1.0.25.1/_sections |
| 220 | CD7E82D0A49CEAE6 | 2 | 77 | `Claude/docs/v1.0.25/_sections/ch2_appB_codemap.tex` | 동명 `ch2_appB_codemap.tex` @ Claude/docs/v1.0.25.1/_sections |
| 221 | CE47F6D8AFD58BF9 | 2 | 75 | `Claude/docs/v1.0.24/_sections/ch2_appB_codemap.tex` | 동명 `ch2_appB_codemap.tex` @ Claude/docs/v1.0.24.1/_sections |
| 222 | CF6D2D8325B95209 | 2 | 52 | `Claude/docs/v1.0.26A-regsol/params/params_graphite.json` | 동명 `params_graphite.json` @ Claude/results/comp_v26_data/out_versions/A_regsol |
| 223 | D0D654623724A50E | 2 | 986 | `Claude/docs/v1.0.19/build_ch1_rp1_p2.log` | `Claude/docs/v1.0.19/build_ch1_rp1_p3.log` |
| 224 | D1D03BD57F903CF6 | 2 | 893 | `Claude/old/Ch1_v7/v7-11.tex` | 동명 `v7-11.tex` @ Claude/results/builds/v7/v7-11 |
| 225 | D37F8B6627411B6C | 2 | 223 | `Claude/docs/v1.0.22/_sections/ch1_sec13_lcohys.tex` | 동명 `ch1_sec13_lcohys.tex` @ Claude/docs/v1.0.23/_sections |
| 226 | D486986D519BDEC6 | 2 | 64 | `Claude/docs/v1.0.22/_sections/ch2_sec09_method.tex` | 동명 `ch2_sec09_method.tex` @ Claude/docs/v1.0.23/_sections |
| 227 | D5898DC15929D352 | 2 | 196 | `Claude/docs/v1.0.24/_sections/ch1_sec05b_gr2L.tex` | 동명 `ch1_sec05b_gr2L.tex` @ Claude/docs/v1.0.24.1/_sections |
| 228 | D8931ACBAB80CD4C | 2 | 112 | `Claude/docs/v1.0.22/_sections/ch1_sec12_lcocenter.tex` | 동명 `ch1_sec12_lcocenter.tex` @ Claude/docs/v1.0.23/_sections |
| 229 | DC57FB0422AD3A0C | 2 | 32 | `Claude/docs/v1.0.24/ch3_si_v1.0.24.tex` | 동명 `ch3_si_v1.0.24.tex` @ Claude/docs/v1.0.24.1 |
| 230 | DC7B84DB06DA3381 | 2 | 94 | `Claude/docs/v1.0.22/_sections/ch1_sec00_intro.tex` | 동명 `ch1_sec00_intro.tex` @ Claude/docs/v1.0.23/_sections |
| 231 | DD52E3BB276DA0D2 | 2 | 32 | `Claude/docs/v1.0.24/ch2_lco_v1.0.24.tex` | 동명 `ch2_lco_v1.0.24.tex` @ Claude/docs/v1.0.24.1 |
| 232 | DD5473B147E56E06 | 2 | 1852 | `Claude/old/Ch1_v10/graphite_ica_ch1_v10.tex` | `Claude/results/builds/ch1v10/v10-11/v10-11.tex` |
| 233 | DD5D328D33D7120E | 2 | 62 | `Claude/docs/v1.0.24/test_gates_v1024_reflect.py` | 동명 `test_gates_v1024_reflect.py` @ Claude/docs/v1.0.24.1 |
| 234 | DD9AE36E7A43BEC3 | 2 | 184 | `Claude/docs/v1.0.25/_sections/ch1_appB_codemap.tex` | 동명 `ch1_appB_codemap.tex` @ Claude/docs/v1.0.25.1/_sections |
| 235 | DE6C18827A5F7B9D | 2 | 750 | `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` | `Claude/docs/v1.0.11/graphite_ica_ch2_v1.0.11.tex` |
| 236 | E075FD66ADCE892F | 2 | 71 | `Claude/docs/v1.0.22/_sections/ch2_sec00_intro.tex` | 동명 `ch2_sec00_intro.tex` @ Claude/docs/v1.0.23/_sections |
| 237 | E3448370B3B6E3F1 | 2 | 43 | `Claude/docs/v1.0.20/_sections/ch1_sec06_eqpeak.tex` | 동명 `ch1_sec06_eqpeak.tex` @ Claude/docs/v1.0.21/_sections |
| 238 | E3B0C44298FC1C14 | 2 | 0 | `Claude/results/comp_v26_data/out_v2/run_v2.log` | `Claude/results/comp_v26_data/out_v3/run_v3.log` |
| 239 | E3D17283119ECC5B | 2 | 432 | `Claude/old/_archive/Archive_old/graphite_ica_chapter2.tex` | `Claude/old/_archive/Archive_old/graphite_ica_chapter2_CLAUDE_criticalfix_5-29.tex` (iter_2 수동 지정 AUD-12) |
| 240 | E586657F178CC0C1 | 2 | 175 | `Claude/docs/v1.0.22/_sections/ch1_sec11_lcointro.tex` | 동명 `ch1_sec11_lcointro.tex` @ Claude/docs/v1.0.23/_sections |
| 241 | E68671D07394F99B | 2 | 999 | `Claude/old/_archive/Archive_rebuilt/graphite_ica_ch5_rebuilt.tex` | 동명 `graphite_ica_ch5_rebuilt.tex` @ Claude/old/work/oldtrack_src |
| 242 | E885C9B121B97703 | 2 | 144 | `Claude/docs/v1.0.20/_sections/ch2_sec01_partition.tex` | 동명 `ch2_sec01_partition.tex` @ Claude/docs/v1.0.21/_sections |
| 243 | E8B408B2AAA7F8D9 | 2 | 265 | `Claude/old/Ch2_v3/graphite_ica_ch2_v3.tex` | `Claude/results/builds/ch2_v4/v4-00_spine/base_ch2_v3.tex` |
| 244 | EA38B57C7EFB6600 | 2 | 1734 | `Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py` | 동명 `Anode_Fit_v1.0.24.py` @ Claude/docs/v1.0.24.1 |
| 245 | EAC064794833C4E1 | 2 | 190 | `Claude/docs/v1.0.22/_sections/ch2_sec02_config.tex` | 동명 `ch2_sec02_config.tex` @ Claude/docs/v1.0.23/_sections |
| 246 | EBE88727171E0330 | 2 | 176 | `Claude/docs/v1.0.20/_sections/ch1_sec13_lcohys.tex` | 동명 `ch1_sec13_lcohys.tex` @ Claude/docs/v1.0.21/_sections |
| 247 | ECF16C279EF84253 | 2 | 25 | `Claude/docs/v1.0.20/_sections/ch2_sec10_closing.tex` | 동명 `ch2_sec10_closing.tex` @ Claude/docs/v1.0.21/_sections |
| 248 | ED86C91A6033760C | 2 | 111 | `Claude/docs/v1.0.22/_sections/ch3v22_sec04_mech.tex` | 동명 `ch3v22_sec04_mech.tex` @ Claude/docs/v1.0.23/_sections |
| 249 | F08FC1CDC1AEC140 | 2 | 212 | `Claude/docs/v1.0.24/_sections/ch1_appE_selfconsistent.tex` | 동명 `ch1_appE_selfconsistent.tex` @ Claude/docs/v1.0.24.1/_sections |
| 250 | F09E6E72AEE07093 | 2 | 851 | `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` | `Claude/docs/v1.0.11/Anode_Fit_v1.0.11.py` |
| 251 | F1333E22FAB858C4 | 2 | 357 | `Claude/docs/v1.0.24/_sections/ch1_sec07_broadening.tex` | 동명 `ch1_sec07_broadening.tex` @ Claude/docs/v1.0.24.1/_sections |
| 252 | F1B80B7C1BC8D003 | 2 | 217 | `Claude/docs/v1.0.25/_sections/ch1_appE_selfconsistent.tex` | 동명 `ch1_appE_selfconsistent.tex` @ Claude/docs/v1.0.25.1/_sections |
| 253 | F36DDF45E7916410 | 2 | 187 | `Claude/docs/v1.0.25/_sections/ch1_sec10_sum.tex` | 동명 `ch1_sec10_sum.tex` @ Claude/docs/v1.0.25.1/_sections |
| 254 | F3BD2B85D5EBFB7D | 2 | 89 | `Claude/docs/v1.0.24/_sections/ch1_sec06_eqpeak.tex` | 동명 `ch1_sec06_eqpeak.tex` @ Claude/docs/v1.0.24.1/_sections |
| 255 | F4F9D9B3A5C162D0 | 2 | 341 | `Claude/results/builds/ch2v5/pass1.log` | `Claude/results/builds/ch2v5/pass2.log` |
| 256 | F5384114EC5A2F7E | 2 | 1148 | `Claude/docs/v1.0.20/results/snapshot_v1020_p5.json` | `Claude/docs/v1.0.20/results/snapshot_v1020_p6.json` |
| 257 | F7A67E5F023AA2F4 | 2 | 245 | `Claude/docs/v1.0.22/_sections/ch2_sec05_mixing.tex` | 동명 `ch2_sec05_mixing.tex` @ Claude/docs/v1.0.23/_sections |
| 258 | FA6A731E9C9FADAB | 2 | 149 | `Claude/docs/v1.0.22/_sections/ch2_sec01_partition.tex` | 동명 `ch2_sec01_partition.tex` @ Claude/docs/v1.0.23/_sections |
| 259 | FE5C5EE6FE123D65 | 2 | 88 | `Claude/docs/v1.0.26A-regsol/params/params_blend.json` | 동명 `params_blend.json` @ Claude/results/comp_v26_data/out_versions/A_regsol |

## 5. git untracked 21건(세션 시작 스냅샷 · brief §3.5 · git 미실행 — 존재·크기·참조만 실측)

### 5.1 Claude 측 8건

| # | path | 실물(존재·바이트·mtime) | 지위 | 근거(4-tier) |
|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.17/figs/graph_suite_v1017.png` | 존재 · 223,035 B · 2026-09-02 16:49 | **유효(재생성 가능 산출물)** [sub 판단] | 확정: 같은 폴더 tracked 스크립트 `Claude/docs/v1.0.17/graph_suite_v1017.py:37` `OUT = r"…\v1.0.17\figs\graph_suite_v1017.png"` · `results/process/V1017_EXECUTION_LEDGER.md:19` "v1.0.16 → v1.0.17 복제(… figs)" (간접) · `docs/INDEX.md`·`HANDOVER_v1.0.17.md` 직접 언급 = 근거 미발견 |
| 2 | `Claude/docs/v1.0.17/sample_test_v1017.png` | 존재 · 281,441 B · 2026-09-02 16:48 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.17/sample_test_v1017.py:12` "Output: sample_test_v1017.png" · `:28` OUT 경로 |
| 3 | `Claude/docs/v1.0.18.1/figs/graph_suite_v1018_1.png` | 존재 · 223,076 B · 2026-09-02 16:47 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.18.1/graph_suite_v1018_1.py:37` · `V1018_EXECUTION_LEDGER.md:31` "v1.0.17 → v1.0.18.1 복제(… figs)" (간접) |
| 4 | `Claude/docs/v1.0.18.1/sample_test_v1018_1.png` | 존재 · 281,771 B · 2026-09-02 16:49 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.18.1/sample_test_v1018_1.py:12,28` |
| 5 | `Claude/docs/v1.0.18.2/figs/graph_suite_v1018_2.png` | 존재 · 223,131 B · 2026-09-02 16:47 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.18.2/graph_suite_v1018_2.py:37` |
| 6 | `Claude/results/process/C3_graph_check/` | 폴더 · 1 파일: `c3_graphite_lco_check.png`(157,313 B · 2026-07-02 01:38) | **유효(v1.0.10 문제점검 C3 실행 그래프 · 참조 문서 존재)** [sub 판단] | 확정: `Claude/results/process/V1010_INSPECT_draft_C3.md:14` "별도 임시 위치 `Claude/results/process/C3_graph_check/c3_graphite_lco_check.png`에 직접 실행 결과 생성 후 육안 판독" · `:23` 동일 경로 인용 |
| 7 | `Claude/results/process/C3_pdf_render/` | 폴더 · 50 파일: `ch1-01.png`~`ch1-35.png`(35) · `ch2-01.png`~`ch2-13.png`(13) · `ch1_contact_sheet.png`(1,832,571 B) · `ch2_contact_sheet.png`(706,435 B) · 전부 2026-07-02 01:38–01:39 | **유효(추정 상향)** — 폴더명 직접 참조 0 · 내용 대응 확정 [sub 판단] | 확정(내용 대응): `V1010_INSPECT_draft_C3.md:15` "Ch1 PDF 35쪽, Ch2 PDF 13쪽을 `pdftoppm`으로 렌더링해 contact sheet 및 핵심 페이지를 육안 판독" — 페이지 수 35/13 · contact sheet 2 · 시각(#6 과 동일 분) 일치 · 폴더명 문자열 검색(`C3_pdf_render`, `Claude/results/**` 전 파일) = 0건(근거 미발견) → 지위는 추정 |
| 8 | `Claude/results/regsol_test/` | 폴더 · 2 파일: `gr_regsol_vs_logistic.png`(244,903 B · 2026-07-27 01:07) · `regsol_view.html`(331,010 B · 2026-07-27 01:19) | **폐기** | 확정: `Claude/results/comp_v26_data/README.md:31` "`regsol_decision.html` · `../regsol_test/` — 위 폐기분 기반"(§ "⚠️ 폐기 (실행하지 말 것)" L26–31, I-7) |

관찰(판정 아님): #1~#5 의 mtime 은 전부 2026-09-02 16:47–16:49 로 같은 세션의 일괄 재생성으로 보인다(추정 · 실행 주체 미상). 같은 폴더의 `Claude/docs/v1.0.18.2/sample_test_v1018_2.png`(282,079 B · 2026-09-02 16:49)와 세 폴더의 `figs/P4_lco_heat_validation.png`(98,479 B · 2026-09-02 16:47–16:49)는 스냅샷의 untracked 목록에 없으므로 tracked 로 추정된다(git 미실행 — 미검증, DQ-14). png 는 열지 않았다.

### 5.2 Codex 측 13건 — 지위 고정 "Codex 소관 · 무접근(판정 안 함)" · 열람 0

| # | path | 지위 |
|---|---|---|
| 1 | `Codex/work/agent_reports/` | Codex 소관 · 무접근(판정 안 함) |
| 2 | `Codex/work/audit_runtime/` | Codex 소관 · 무접근(판정 안 함) |
| 3 | `Codex/work/literature/` | Codex 소관 · 무접근(판정 안 함) |
| 4 | `Codex/work/local_remote_pdf_compare_v10182/` | Codex 소관 · 무접근(판정 안 함) |
| 5 | `Codex/work/phase004/` | Codex 소관 · 무접근(판정 안 함) |
| 6 | `Codex/work/phase005/` | Codex 소관 · 무접근(판정 안 함) |
| 7 | `Codex/work/phase006/` | Codex 소관 · 무접근(판정 안 함) |
| 8 | `Codex/work/phase007/` | Codex 소관 · 무접근(판정 안 함) |
| 9 | `Codex/work/phase010_sources/` | Codex 소관 · 무접근(판정 안 함) |
| 10 | `Codex/work/scripts/` | Codex 소관 · 무접근(판정 안 함) |
| 11 | `Codex/work/source_archives/` | Codex 소관 · 무접근(판정 안 함) |
| 12 | `Codex/work/source_snapshots/` | Codex 소관 · 무접근(판정 안 함) |
| 13 | `Codex/work/tools/` | Codex 소관 · 무접근(판정 안 함) |

`Codex/` 는 읽기·디렉터리 목록 조회 포함 0회 접근(존재 여부조차 본 sub 는 확인하지 않았다 — 목록은 brief §3.5 전사).

## 6. 현행 tex 60 — 마스터별 `\input` 순서와 빌드 포함/미포함(§3.2)

마스터 tex 3본(I-8 전문 정독)의 비주석 행 `\input{_sections/…}` 실측(`Grep ^[^%]*\input\{` — `docs/v1.0.25.1/**/*.tex` 전건에서 마스터 3본 외 매치 0 → 중첩 `\input` 없음). 각 마스터는 먼저 `common_preamble_v1024`(L10/L8/L8)를 `\input` 하고 본문 절을 순서대로 `\input` 한다.

### ch1_graphite_v1.0.24.tex — `\input` 33건

`L10 common_preamble_v1024` → `L25 ch1_sec00_intro` → `L26 ch1_sec01_n0n1` → `L27 ch1_sec02a_part0` → `L28 ch1_sec02b_part0` → `L29 ch1_sec03_center` → `L30 ch1_sec04_hys` → `L31 ch1_sec05_width` → `L32 ch1_sec05b_gr2L` → `L33 ch1_sec06_eqpeak` → `L34 ch1_sec07_broadening` → `L35 ch1_sec08_lag` → `L36 ch1_sec09_tail` → `L37 ch1_sec10_sum` → `L39 ch1v22_partT_divider` → `L40 ch2_sec00_intro` → `L41 ch2_sec01_partition` → `L42 ch2_sec02_config` → `L43 ch2_sec03_vibel` → `L44 ch2_sec04_einstein` → `L45 ch2_sec05_mixing` → `L46 ch2_sec06_limits` → `L47 ch2_sec07_revheat` → `L48 ch2_sec08_synthesis` → `L49 ch2_sec09_method` → `L50 ch2_sec10_closing` → `L52 ch1_sec18_inputs` → `L54 ch1_appA_signcheck` → `L55 ch1_appB_codemap` → `L56 ch2_appA_traps` → `L57 ch2_appB_codemap` → `L58 ch1_appE_selfconsistent` → `L60 ch1v22_bib`

### ch2_lco_v1.0.24.tex — `\input` 12건

`L8 common_preamble_v1024` → `L22 ch2v22_sec00_intro` → `L23 ch2v22_notation` → `L24 ch1_sec11_lcointro` → `L25 ch1_sec12_lcocenter` → `L26 ch1_sec13_lcohys` → `L27 ch1_sec14_lcodecomp` → `L28 ch1_sec15_lcoelec` → `L29 ch1_sec16_lcopeak` → `L30 ch1_sec16b_lcoomega` → `L31 ch1_sec17_msmr` → `L32 ch2v22_bib`

### ch3_si_v1.0.24.tex — `\input` 10건

`L8 common_preamble_v1024` → `L23 ch3v22_sec00_intro` → `L24 ch3v22_notation` → `L25 ch3v22_sec01_map` → `L26 ch3v22_sec02_cases` → `L27 ch3v22_sec02b_sifr` → `L28 ch3v22_sec03_blend` → `L29 ch3v22_sec04_mech` → `L31 ch3v22_sec05_code` → `L32 ch3v22_bib`

### 집계 — 마스터 3 · 빌드 포함 53 · 미포함 4(독립 부록 1 + orphan 3) = 60/60

- `_sections` 56 중 `\input` 되는 고유 파일 = 53 (ch1 33 + ch2 12 + ch3 10 = 55 건, `common_preamble_v1024` 3회 중복 제거).
- orphan 3 = `ch1_appD_si.tex` · `ch1_preamble.tex` · `ch2_preamble.tex` — `ch1_appD_si` 는 기대(brief §3.2 · R4b DQ-3)와 일치; `ch1_preamble`·`ch2_preamble` 는 **기대(지원 4본 = 빌드 포함)와 상이**: 두 파일 헤더 L2–3 이 각각 `graphite_ica_ch1_v1.0.21.tex`·`graphite_ica_ch2_v1.0.21.tex` 가 `\input` 한다고 적은 v1.0.21 잔재이며, `common_preamble_v1024.tex`:3 이 "= 구 ch1_preamble ∪ ch2_preamble" 로 흡수했음을 명시한다(확정). 지원 파일로 실제 `\input` 되는 것은 `common_preamble_v1024`(마스터 3본)와 `ch1v22_partT_divider`(ch1 L39) 2본뿐.
- `INDEX_v25.md`:32 는 ch1 마스터의 `\input` 을 34 로 기재 — 본 실측(비주석 `\input{_sections/…}`)은 33. 차이 1 의 원인 = 근거 미발견(집계 기준 차이 추정 · 마스터 파일은 v1.0.25 → v1.0.25.1 에서 표시 버전만 변경).
- 독립 부록 `appendix_phase_separation.tex` = 자체 `\documentclass` L13 · `\begin{document}` L41 · `_sections` 밖 · `\input` 0(확정) → 미포함·독립.
- 마스터 플랜 §2.9 L203 "미정독 = ch1v22_partT_divider·ch1_preamble·ch2_preamble·common_preamble_v1024(grep 만) + 마스터 3본 → 배정 = 2.1 Step 14" 는 orphan 2본을 정독 대상으로 유지할지 재검토 대상(DQ-3).

## 7. 판독 커버리지 대조(R1~R7 Read Coverage 파일 집합 ⊆ OUT-INV)

| 파일 | R# 태그 | TSV 존재 | OUT-INV 군 | 판정 |
|---|---|---|---|---|
| `CLAUDE.md` | R3 | 있음 | (xix) | 등재 |
| `Claude/docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | R1·R3·R6 | 있음 | (iv) | 등재 |
| `Claude/docs/Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md` | R1 | 있음 | (iv) | 등재 |
| `Claude/docs/Fable_점검/FABLE_AUDIT_note_A2_v5-v7.md` | R1 | 있음 | (iv) | 등재 |
| `Claude/docs/Fable_점검/FABLE_AUDIT_note_A3_v7-v9.md` | R1 | 있음 | (iv) | 등재 |
| `Claude/docs/Fable_점검/FABLE_AUDIT_note_A4_v9-v1011.md` | R1 | 있음 | (iv) | 등재 |
| `Claude/docs/Fable_점검/FABLE_AUDIT_note_A5_ch2-code.md` | R1 | 있음 | (iv) | 등재 |
| `Claude/docs/INDEX.md` | R1·R3(grep) | 있음 | (vi) | 등재 |
| `Claude/docs/v1.0.10/HANDOVER_v1.0.11.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.13/HANDOVER_v1.0.13.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.14/HANDOVER_v1.0.14.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | R1·R3 | 있음 | (v) | 등재 |
| `Claude/docs/v1.0.15/HANDOVER_v1.0.15.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.16/HANDOVER_v1.0.16.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.17/HANDOVER_v1.0.17.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.18.1/HANDOVER_v1.0.18.1.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` | R3·R5·R6 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.19/HANDOVER_v1.0.19.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.20/HANDOVER_v1.0.20.md` | R2 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.20/results/V1020_REFERENCE_LEDGER.md` | R7 | 있음 | (xii) | 등재 |
| `Claude/docs/v1.0.21/HANDOVER_v1.0.21.md` | R2·R3(grep) | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md` | R3(grep) | 있음 | (viii) | 등재 |
| `Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md` | R3(grep) | 있음 | (vii) | 등재 |
| `Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md` | R3(grep)·R7 | 있음 | (xii) | 등재 |
| `Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md` | R3·R5·R7 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | R3·R5·R6·R7 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md` | R6 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md` | R6 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.22/results/comp_v23/SURV3_convex_inverse.md` | R6 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.22/results/comp_v23/SURV4_bifurcation_stochastic.md` | R6 | 있음 | (ix) | 등재 |
| `Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md` | R2 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md` | R7 | 있음 | (xii) | 등재 |
| `Claude/docs/v1.0.23/results/HANDOVER_v23.md` | R2 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md` | R7 | 있음 | (xii) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_appA_signcheck.tex` | R4a | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_appB_codemap.tex` | R4a | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_appD_si.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_appE_selfconsistent.tex` | R3(grep)·R4a·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_preamble.tex` | R4a(grep) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` | R4a·R6(보강) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec01_n0n1.tex` | R4a·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec02a_part0.tex` | R3(grep)·R4a·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec02b_part0.tex` | R4a·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec03_center.tex` | R4a·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec04_hys.tex` | R4a·R4b(부분)·R5·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec05_width.tex` | R4a·R5·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec05b_gr2L.tex` | R4a·R4b(부분)·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec06_eqpeak.tex` | R4a·R4b(부분)·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec07_broadening.tex` | R4a·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec08_lag.tex` | R4a·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec09_tail.tex` | R4a·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec10_sum.tex` | R4a·R5(grep) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec11_lcointro.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec12_lcocenter.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec13_lcohys.tex` | R4b·R5(부분)·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec14_lcodecomp.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec15_lcoelec.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec16_lcopeak.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec16b_lcoomega.tex` | R3(grep)·R4b·R5(보조) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec17_msmr.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec18_inputs.tex` | R4a | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch1v22_bib.tex` | R3(grep)·R4a·R5(보조)·R6(grep)·R7 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_appA_traps.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_appB_codemap.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_preamble.tex` | R4a(grep) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec00_intro.tex` | R4a | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec01_partition.tex` | R4a·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec02_config.tex` | R4a·R5 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec03_vibel.tex` | R4a·R4b(부분)·R5(보조) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec04_einstein.tex` | R4a·R5(보조) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec05_mixing.tex` | R4a·R5·R6(부분) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec06_limits.tex` | R4a·R5(보조) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec07_revheat.tex` | R4a·R5·R6(보강) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec08_synthesis.tex` | R4a·R5(보조) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec09_method.tex` | R4a | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2_sec10_closing.tex` | R4a | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2v22_bib.tex` | R4b·R5(보조)·R6(grep)·R7 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2v22_notation.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch2v22_sec00_intro.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_bib.tex` | R4b·R5(보조)·R6(grep)·R7 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_notation.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec00_intro.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec01_map.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec02_cases.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec02b_sifr.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec03_blend.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec04_mech.tex` | R4b·R6 | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_sec05_code.tex` | R4b | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/_sections/common_preamble_v1024.tex` | R3(grep)·R4b(부분) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/appendix_phase_separation.tex` | R4b·R5(보조)·R6·R7(부분) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/ARCHIVE_NOTE.md` | R4b(부분) | 있음 | (viii) | 등재 |
| `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` | R3(grep)·R4b(부분) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/ch2_lco_v1.0.24.tex` | R4b(부분) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/ch3_si_v1.0.24.tex` | R3(grep)·R4b(부분) | 있음 | (xvi) | 등재 |
| `Claude/docs/v1.0.25.1/results/HANDOVER_v24.md` | R2 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` | R2·R3 | 있음 | (iii) | 등재 |
| `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | R2·R4b(부분) | 있음 | (vi) | 등재 |
| `Claude/docs/v1.0.25.1/results/PHASE_R1_RESULT.md` | R3(grep) | 있음 | (viii) | 등재 |
| `Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md` | R2 | 있음 | (viii) | 등재 |
| `Claude/docs/v1.0.25.1/results/V1025_DOC_EDIT_REPORT.md` | R4b(부분) | 있음 | (viii) | 등재 |
| `Claude/docs/v1.0.25.1/results/V1025_T13_T14_REPORT.md` | R4b(부분) | 있음 | (viii) | 등재 |
| `Claude/docs/v1.0.25/_sections/ch1_sec05_width.tex` | R4a(diff) | 있음 | (xviii) | 등재 |
| `Claude/docs/v1.0.25/_sections/ch1_sec06_eqpeak.tex` | R4a(diff) | 있음 | (xviii) | 등재 |
| `Claude/docs/v1.0.25/_sections/ch3v22_sec02b_sifr.tex` | R4b | 있음 | (xviii) | 등재 |
| `Claude/docs/v1.0.26A-regsol/README.md` | R2(추가) | 있음 | (xi) | 등재 |
| `Claude/docs/v1.0.26B-gallery/README.md` | R2(추가) | 있음 | (xi) | 등재 |
| `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` | R3(glob)·R6·R7 | 있음 | (x) | 등재 |
| `Claude/plans/2026-07-16-v1021-master-plan.md` | R2 | 있음 | (i) | 등재 |
| `Claude/plans/2026-07-17-v1022-master-plan.md` | R2·R3(grep) | 있음 | (i) | 등재 |
| `Claude/plans/2026-07-18-anodefit-MASTER-plan.md` | R2·R3 | 있음 | (i) | 등재 |
| `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | R2·R3(grep) | 있음 | (i) | 등재 |
| `Claude/plans/2026-07-18-v1024-completeness-validation-plan.md` | R2 | 있음 | (i) | 등재 |
| `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md` | R2 | 있음 | (i) | 등재 |
| `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md` | R2·R3 | 있음 | (i) | 등재 |
| `Claude/plans/INDEX.md` | R1 | 있음 | (vi) | 등재 |
| `Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md` | R3·R5 | 있음 | (ix) | 등재 |
| `Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | R3·R5·R6·R7 | 있음 | (ix) | 등재 |
| `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md` | R2·R3 | 있음 | (ix) | 등재 |
| `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md` | R2 | 있음 | (ix) | 등재 |
| `Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md` | R2·R5(보조) | 있음 | (iii) | 등재 |
| `Claude/results/comp_v26_data/out_skew/summary_skew.json` | R2(추가) | 있음 | (xi) | 등재 |
| `Claude/results/comp_v26_data/out_versions/build.log` | R2(추가) | 있음 | (xi) | 등재 |
| `Claude/results/comp_v26_data/README.md` | R2(추가) | 있음 | (xi) | 등재 |
| `Claude/results/comp_v26_data/skew_log.txt` | R2(추가) | 있음 | (xi) | 등재 |
| `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | R1·R2·R3·R4a·R4b·R5·R6·R7 | 있음 | (xv) | 등재 |
| `Claude/results/process/HANDOVER_2026-06-07_ch2-5-overnight.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/results/process/HANDOVER_2026-06-10_ch1-textbook-rewrite.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/results/process/HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md` | R1 | 있음 | (iii) | 등재 |
| `Claude/results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md` | R1 | 있음 | (iii) | 등재 |

**판정**: R1~R7 Read Coverage 열거 파일 131 건 중 등재 131 · 군 밖 0 · 실물 부재 0 → ⊆ 성립.

일괄 기록(파일별 태그 미부여): R3 = `docs/v1.0.25.1/_sections/*.tex` 전건 키워드 grep + `Claude/**/*.md` `D21`·`D22` grep(매치 파일은 위 표에 `R3(grep)` 태그) · R4a = `_sections` LCO·Si·notation·divider·ch2 부록·`appendix_phase_separation.tex` 카운트 grep · R5·R6 = `_sections` 전건 키워드 grep · R7 = `_sections` 53본(bib 제외) + 마스터 3본 기계 스캔(`\cite`·절 제목·키워드 빈도, 전문 정독 아님). 이들은 (xvi) 60본 전건이 OUT-INV 에 있으므로 ⊆ 에 영향 없음. R# 가 적은 행 범위 상한(예: R1 `docs/INDEX.md` L1–197)은 TSV 줄수(196)와 +1 차이가 나며 이는 §0 줄수 정의 차이다(경로 오기 아님).

## 8. 부재·미검독 명시

### 8.1 부재(기대했으나 실물 없음)

- 기대 항목 중 실물 부재 = **0건**(brief §4 기대치 기준). 모든 군의 기대 파일이 존재한다(§7 실물 부재 0 포함).
- (iter_2 AUD-04) 통제 문서 기대 기준 부재 1건: 마스터 플랜 §2.9 L197 이 HANDOVER 미검독 잔여로 적은 `HANDOVER_v1.0.10`·v1.0.12 인계는 **실물 부재** — `docs/v1.0.10/` 의 인계 = `HANDOVER_v1.0.11.md` 1본, `docs/v1.0.12/*.md` = `FITTING_GUIDE.md` 1본(검수 재측정 확정) → 마스터 플랜 §2.9 정정(v5.3).
- (iter_5 AUD-R4-01 부수) 통제 문서 인용 기준 부재 1건 추가: `docs/INDEX.md`:174 가 "★★Ch2 v5 최신" 으로 인용하는 `graphite_ica_ch2_v5.tex` 는 TSV 0건(모집단 안 실물 부재 — `old/Ch2_v*` 에는 v3·v4 만) → 계보 §2.3 Ch2 트랙 v5(파생 C 제거) 원문 소재 = **근거 미발견** · 1.2 Step 3 Ch2 트랙 행에서 확인.
- 기대와 **다른** 실측(부재 아님): brief §3.2 "지원 4본은 `\input` 되는 빌드 포함 파일" → `ch1_preamble.tex`·`ch2_preamble.tex` 는 `\input` 0 = orphan(§6). 빌드 포함 58/미포함 2 기대 → 실측 56(마스터 3 + 포함 53)/4.

### 8.2 미검독(이 Step 에서 열지 않은 것 — 추정 금지)

- 본 sub 가 내용을 읽은 파일 = work_log 「Read Coverage」 표 전건뿐(brief · 마스터 플랜 지정 행 범위 · INDEX 3 · 1g txt · comp_v26 README L20–35 · 마스터 tex 3 · R1~R7 Read Coverage 절 · preamble 3본 · `V1010_INSPECT_draft_C3.md`). 그 밖의 OUT-INV 등재 파일 전부 = 존재·줄수·hash·바이트만 측정, **내용 미검독**(조사 문서군·ledger·Result·계획서 본문·tex 본문·판독 산출 본문 포함).
- png·pdf·html 은 열지 않았다(존재·바이트·mtime 만). `Codex/` 0회 접근.
- 버전 귀속에 "추정" 이 붙은 행(날짜·이름 추론)은 Step 2 정독에서 확정 대상.

### 8.3 모집단 안이지만 OUT-INV 군 밖(미등재 — 계수만)

TSV 2,651 − 등재 739 = 미등재 **1,912 파일 · 603,988 줄**(iter_5 — 표는 현재 §1 집합 기준으로 스크립트 재계산 `iter_3/policy_check.txt`; 이력: iter_1 1,986/622,113 → iter_2 1,960/617,440 → iter_3 1,929/611,581 → iter_3b 1,921/604,865 → iter_4 1,913/604,011 → iter_5 1,912/603,988). 폴더별(상위 3단계):

| 폴더 | 파일 | 줄수 | 내용(확장자 계수) |
|---|---|---|---|
| `Claude/docs/v1.0.10` | 10 | 6754 | .log 2 · .py 6 · .tex 2 |
| `Claude/docs/v1.0.11` | 10 | 6695 | .log 2 · .md 1 · .py 5 · .tex 2 |
| `Claude/docs/v1.0.12` | 9 | 7188 | .log 2 · .py 5 · .tex 2 |
| `Claude/docs/v1.0.13` | 10 | 8045 | .log 2 · .py 6 · .tex 2 |
| `Claude/docs/v1.0.14` | 12 | 10110 | .log 3 · .py 6 · .tex 3 |
| `Claude/docs/v1.0.15` | 13 | 10423 | .log 3 · .md 1 · .py 6 · .tex 3 |
| `Claude/docs/v1.0.16` | 12 | 10375 | .log 3 · .py 6 · .tex 3 |
| `Claude/docs/v1.0.17` | 13 | 10495 | .log 3 · .md 1 · .py 6 · .tex 3 |
| `Claude/docs/v1.0.18.1` | 13 | 10538 | .log 3 · .md 1 · .py 6 · .tex 3 |
| `Claude/docs/v1.0.18.2` | 12 | 10561 | .log 3 · .py 6 · .tex 3 |
| `Claude/docs/v1.0.19` | 72 | 27696 | .log 25 · .py 4 · .tex 42 · .txt 1 |
| `Claude/docs/v1.0.20` | 151 | 28287 | .json 11 · .md 25 · .py 8 · .tex 105 · .txt 2 |
| `Claude/docs/v1.0.21` | 59 | 20931 | .json 9 · .md 1 · .py 3 · .tex 46 |
| `Claude/docs/v1.0.22` | 145 | 18652 | .json 1 · .md 49 · .py 3 · .tex 92 |
| `Claude/docs/v1.0.23` | 66 | 11520 | .md 3 · .py 6 · .tex 57 |
| `Claude/docs/v1.0.24` | 114 | 17298 | .json 1 · .md 16 · .py 7 · .tex 90 |
| `Claude/docs/v1.0.24.1` | 114 | 17298 | .json 1 · .md 16 · .py 7 · .tex 90 |
| `Claude/docs/v1.0.25` | 58 | 9444 | .json 1 · .md 16 · .py 11 · .tex 30 |
| `Claude/docs/v1.0.25.1` | 56 | 9349 | .json 1 · .md 14 · .py 11 · .tex 30 |
| `Claude/docs/v1.0.26A-regsol` | 3 | 192 | .json 3 |
| `Claude/docs/v1.0.26B-gallery` | 3 | 188 | .json 3 |
| `Claude/old/_archive` | 49 | 41546 | .log 15 · .md 1 · .tex 33 |
| `Claude/old/Archive_oldtrack` | 5 | 691 | .md 5 |
| `Claude/old/docs` | 1 | 1203 | .tex 1 |
| `Claude/old/pre-restructure-2026-06-07-5ch` | 5 | 3935 | .tex 5 |
| `Claude/old/results` | 6 | 1364 | .json 5 · .md 1 |
| `Claude/old/v2` | 17 | 2478 | .json 15 · .md 1 · .tex 1 |
| `Claude/old/v3_single_length` | 1 | 810 | .tex 1 |
| `Claude/old/work` | 24 | 6555 | .log 1 · .md 1 · .py 13 · .tex 8 · .txt 1 |
| `Claude/results/_FINAL_README.md` | 1 | 25 | .md 1 |
| `Claude/results/builds` | 323 | 217663 | .log 103 · .md 135 · .py 1 · .tex 77 · .txt 7 |
| `Claude/results/code` | 3 | 1458 | .md 1 · .py 2 |
| `Claude/results/comp_v24` | 52 | 4753 | .json 16 · .py 29 · .txt 7 |
| `Claude/results/comp_v26_data` | 11 | 2261 | .json 9 · .log 2 |
| `Claude/results/process` | 403 | 64114 | .log 13 · .md 215 · .py 92 · .tex 76 · .txt 7 |
| `Claude/results/research` | 53 | 2909 | .md 53 |
| `Claude/results/Step 1 — 인벤토리 파일 생성(OUT-INV).md` | 1 | 35 | .md 1 |
| `Claude/results/V1024_PROGRESS_SUMMARY.md` | 1 | 51 | .md 1 |
| `Claude/skills/competition-cherrypick-authoring` | 1 | 98 | .md 1 |

주요 미등재 항목의 성격(전부 내용 미검독 · 등재 여부는 DQ-6·DQ-10·DQ-11):
- `results/comp_v24/` 비-md(`.py` 29 · `.json` 16 · `.txt` 7 — lco_data provenance 등) · `results/comp_v26_data/` 비-md(json 9 · log 2 ; `.py` 8 은 (xi) 등재).
- `docs/v1.0.22/results/` 의 `comp_AUD`(4)·`comp_R2`~`comp_R8`·`comp_RV`(3) = 경쟁 저작 초안·검수 보고 84본(md·tex) · `docs/v1.0.20/results/` 의 `comp_P2/P4/P7_figs/P7_review/Q2/Q3` 97본(md·tex·py·txt·json) 및 `snapshot_*.json`.
- `docs/v1.0.10 ~ v1.0.24.1` 구버전 폴더의 tex·py·log·md(CODE_GUIDE 등 — 현행 아님; FITTING_GUIDE 는 hash 사본 11본만 미등재 · 고유본 8 은 (vii-c) 등재) · `docs/v1.0.25*/results/comp_R1/**`(경쟁 초안 tex·md 각 30·13) · `docs/v1.0.25*/` 의 코드·게이트·가이드(`Anode_Fit_v1.0.24.py` 1,917 · `test_gates_*.py` 4 · `tools_*.py` 4 · `CODE_GUIDE_v24.md` · `FITTING_GUIDE.md`(hash 사본 — 고유본 v1.0.20 은 (vii-c))).
- `old/**` 잔여(구트랙 tex·md·py — ledger·Result·HANDOVER·dossier·유실 원문 5본은 등재) · `results/builds/**`·`results/research/**` 잔여(경쟁 빌드 로그·tex·조사 카드) · `results/code/Anode_Fit_v11_final.py` · `results/process/` 의 비-ledger·비-Result md(iter_3: `V1017_REVIEW_COMPLETE`·`V1017_FIXLIST_CONSOLIDATED`·`V1010_INSPECT_*` 는 (iv-c) 등재; 잔여 = 접두 단위 REVIEW/NOTE 계열 — `V1014_REVIEW_R*` 20 · `V1013_REVIEW_R*` 30 · `V1012_P43_review_*` 등 ≈ 82본·9,159줄 = **DQ-16 후보 풀**, 1.2 Step 3 토픽 한정 열람 대상).
- `Claude/skills/competition-cherrypick-authoring/SKILL.md`(98줄 · 스킬 사본 — 이력 문서 아님).
- `Claude/results/` 상위 md 4본(군 정의 밖): `Step 1 — 인벤토리 파일 생성(OUT-INV).md`(35줄 — 본 arc Step 1 이력 · master 산출 · TSV 시점 09:34 에 이미 존재; 1g A22 `Step*=0` 은 GO 직전 값) · `V1024_PROGRESS_SUMMARY.md`(51) · `_FINAL_README.md`(25) · `MISSING_CONTENT_REVIEW.md`(93 · `docs/INDEX.md`:193 참조 — iter_3 에서 (iv-c) 등재).

### 8.4 모집단 밖(확장자 밖)

- png·pdf·npz·aux·out·toc·html·csv·ps1·bat·pyc 는 계수하지 않았다(§5 의 untracked 실물·JCP PDF·v1.0.25.1 PDF 3종 포함 — PDF 페이지 102/30/22 는 1g A15 기록을 전사, 본 sub 미측정).
- 본 Step 산출 3본(`V1027_HISTORY_INVENTORY.md` · `iter_1/inventory_raw.tsv` · `iter_1/work_log.md`)은 TSV 생성 뒤 작성되어 TSV 에 없다.

## 9. Decision Queue(결정 필요 — 본 sub 는 진행하지 않음 · 기본값 명시 · **master 처분 = §10**)

| # | 항목 | 내용·근거 | 기본값(본 문건 적용) |
|---|---|---|---|
| DQ-1 | 문서 종류 매핑 확정 | 14종 어휘 밖 세부(감사(머지 판정)·Result(집행 보고)·기타(…)·서지 원장(초안))를 §0 매핑 규칙으로 부여 — master 확정 필요 | §0 규칙 그대로 |
| DQ-2 | 버전 귀속 "추정" 행 | `plans/` 2026-05-29~06-09 계획서(v2 이전) · `results/process/PHASE_*` 계보(F0~F9·R0~R9·DEEP_REVIEW 등 계획서 대응 미확정) · `anodefit-*` 2본(07-18 → v1.0.23 추정) · `MASTER_ROADMAP_*` 2본(무날짜) — Step 2 정독 배정 시 실물 정독으로 확정 | 표에 "추정" 명기·유지 |
| DQ-3 | orphan preamble 2본의 정독 대상 여부 | `ch1_preamble`·`ch2_preamble` 는 v1.0.21 잔재 orphan(§6) — §2.9 L203 은 "지원 4본" 을 2.1 Step 14 정독 배정. 정독 유지(계보 확인용) vs 제외 | 등재 유지 · 빌드 열 "미포함·orphan" |
| DQ-4 | hash 사본 고유본 표기 | 규칙(가장 이른 버전 폴더)을 현행 tex 60 에 적용하면 v1.0.24 사본이 고유본 — 정독은 현행 경로(v1.0.25.1) · 등록부 표기는? · 같은 폴더 동명이물(`old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND{,_CLAUDE_rerun_5-29}.md`) 고유본 | §4 규칙 그대로(경로 정렬 최상) · tex 는 비고에 "정독은 현행 경로" |
| DQ-5 | `old/**` ledger 31·Result 33 등재 범위 | (vii)·(viii) 패턴이 `old/` 에도 매치 — 마스터 플랜 정의는 "각 버전"·`results/**`·`docs/vN/results/` 라 `old/` 는 정의 밖. 구트랙 별도 표시로 등재 vs 제외 | 등재(구트랙 RB 표시) |
| DQ-6 | (ix) 미등재 하위군 | `docs/v1.0.22/results/comp_AUD·R2~R8·RV` 84 · `docs/v1.0.20/results/comp_*` 97 · `comp_P7_review/REVIEW_*` 11 — 조사 문서군 편입 여부 | §8.3 계수만 |
| DQ-7 | untracked png 5 처리 | 재생성 가능 산출물(§5.1 #1~#5) — git 추적/무시/삭제는 사용자 결정 | 지위 "유효" 기재만 |
| DQ-8 | `C3_pdf_render/` 50장 보존 | 참조 문서 있으나 폴더명 직접 참조 0 · 총 ~15 MB 추정(개별 바이트 합산 미실시) | 지위 "유효(추정)" 기재만 |
| DQ-9 | plans 10,384 vs 1g 10,383 | +1 파일 미특정 — master 가 1g 시점 파일별 수치를 보유하면 대조 | 실측 정본 10,384 |
| DQ-10 | `comp_v24` 비-md 52본 등재 | py 29·json 16·txt 7 — 2.6·3.1 데이터 판정에 재사용 가능(Assumptions 14) | §8.3 계수만 |
| DQ-11 | `Claude/skills/…/SKILL.md` | 군 밖 · 이력 문서 아님 | 미등재 |
| DQ-12 | `common_preamble_v1024.tex`:2 헤더 파일명 표기 `common_preamble_v1022.tex` | 문건 결함 후보(파일명 불일치) — 수정 X · 등록부/GAP 단계에서 다룸 | 관찰만 기재 |
| DQ-13 | (xi) 추가 발견 2본 | R2 Read Coverage +2·+3(`out_skew/summary_skew.json`·`skew_log.txt`, README.md:30 폐기분 산출) 을 ⊆ 유지 목적으로 (xi) 등재 | 등재(폐기분 표시) |
| DQ-14 | `sample_test_v1018_2.png`·`figs/P4_lco_heat_validation.png` tracked 여부 | mtime 2026-09-02 인데 untracked 목록에 없음 → tracked 추정 · git 필요(master) | 관찰만 기재 |
| DQ-15 | OUT-INV 생성 방식 | 본 문건의 §1·§2·§4·§6·§7·§8.3 표는 TSV 를 읽는 생성 스크립트(세션 스크래치패드 `gen_outinv.ps1` · 휘발 · 프로젝트 밖)로 산출 — 인라인 실행이 명령 길이 제한에 걸려 스크립트 파일 경유. 프로젝트 안 신규 파일은 3본뿐 | 스크래치패드 사용(work_log 기록) |

## 10. master 확정(iter_2 · 2026-09-03) — 검수 라운드 1 반영 + DQ 처분

### 10.1 검수 발견 AUD-01~15 반영(`iter_1/audit_log.md`)

| AUD | 심각도 | master 판정 | 반영 |
|---|---|---|---|
| 01 | 확정결함 | 인정 — 「추가 발견」 정책 (a)(b)(c) 명문화 | (iv-b) 12본 · (viii-b) 2본 등재 · §2·§8.3 갱신 |
| 02 | 경미 | 인정 — old/ 정책을 (i)·(ii) 로 확장 | (i-b) 12본 등재 · glob 오매치 3본 미등재 명기 |
| 03 | 경미 | 인정 | (iv-b) 행 10 `COND_AUDIT` + 동명 폴더 경고 |
| 04 | 경미 | 인정 | §8.1 추가 → 마스터 플랜 §2.9 L197 정정(v5.3) |
| 05 | 경미 | 인정 | (i) 행 79 · (vii) 행 74 귀속 표기 |
| 06 | 경미 | 인정 | (x) 행 1 · §3.5 확정 문구 |
| 07 | 경미 | 인정 + master git 확정(811→812) | §3.1 · DQ-9 닫힘 |
| 08 | 제안 | 채택 | §3.4 오기 확정 → 마스터 플랜 §2.0 정정(v5.3) |
| 09 | 제안 | 채택 | (xi) 행 8 비고(work_log 는 iter_1 기록 그대로 보존 — 정정은 본 문건 · Step 1 이력에 완료 시 기록) |
| 10 | 경미 | 인정 | §0 규칙 · (vii) 행 81 비고 |
| 11 | 경미 | 인정 | 세부 표기 6종 → 3종 통일 · DQ-1 어휘 세부 3종 추가 인지(`통제(프로젝트 지침)`·`조사(원문 추출)`·`시드(판독·json)` — 토큰 + 괄호 세부 규칙 안) |
| 12 | 제안 | 채택 | §4 규칙 ordinal 명시 · #179·#239 고유본 수동 지정 · (vii) 행 39·41 표기 교체 |
| 13 | 제안(계획서) | 채택 — OUT-INV 무수정 | 마스터 플랜 v5.3 사실 정정(§2.2·§2.6·§2.9·2.1·2.2·2.7·T-4·T-15·Assumptions 12) |
| 14 | 제안 | 채택 | 보존 사본 `iter_1/gen_outinv.ps1`(master 가 10:16:52 스크래치패드에서 복사 · SHA256 동일) — Step 1 이력에 완료 시 기록 |
| 15 | 제안 | 채택 | §0 태그 경계 1구 |

### 10.2 DQ-1~15 처분

| DQ | 처분 | 근거 |
|---|---|---|
| 1 | **확정** — 문서 종류 어휘 = 14종 토큰 + 괄호 세부 허용(§0 규칙 그대로, 세부 3종 추가 인지) | AUD-11 |
| 2 | **유지** — "추정" 귀속은 1.2 Step 3·4 원천 정독에서 확정(Step 2 배정표는 추정 귀속으로 정렬하고 표시 유지) | 계획서 1.2 |
| 3 | **확정** — orphan preamble 2본 등재 유지 · 2.1 Step 14 정독 대상 유지(9,214줄 전 영역 cover 게이트) · 성격 = v1.0.21 잔재 orphan(계보 확인용) · 마스터 플랜 정정 v5.3 | AUD-13 |
| 4 | **확정** — §4 규칙 + ordinal 정렬 + 동명이물 2건 수동 지정 · 현행 tex 60 은 정독 경로 = `v1.0.25.1`, 등록부 표기 = "고유본 = 최초 등장 버전 폴더" 병기 | AUD-12 |
| 5 | **확정** — `old/**` 매치는 구트랙 표시로 등재(ledger·Result·계획서·감사 전 군 일관) | AUD-02 |
| 6 | **확정** — 경쟁 저작 초안·검수 보고(`comp_AUD·R2~R8·RV` 84 · `comp_*` 97 · `comp_P7_review/REVIEW_*` 11)는 조사 문서군이 아니므로 §8.3 계수만 · 1.2 Step 4 토픽 한정에서 필요 시 열람 | 계획서 (ix) 정의 |
| 7 | **사용자 결정 대기(nonblocking)** — png 5 의 git 추적/무시/삭제 · 기본값 = 현상 유지(untracked) · Phase 1.1 Result Decision Queue 로 이관 | 사용자 소관 |
| 8 | **사용자 결정 대기(nonblocking)** — `C3_pdf_render/` 50장 15.7 MiB 보존/삭제 · 기본값 = 현상 유지 · Result DQ 이관 | 사용자 소관 |
| 9 | **닫힘** — +1 = 마스터 플랜 811→812(`git show 8d9362f` vs HEAD `f0c381b`) | master git 실측 |
| 10 | **확정** — `comp_v24` 비-md 52본은 데이터·코드 자산으로 §8.3 계수만 · 2.6·3.1 재사용(Assumptions 14) | 계획서 Non-goals |
| 11 | **닫힘** — 미등재 유지 | 군 밖 |
| 12 | **이관** — `common_preamble_v1024.tex`:2 헤더 파일명 불일치 = GAP 후보 → 2.1 Step 15 · 2.5 | 진단 소관 |
| 13 | **닫힘** — 등재 유지(폐기분 표시) | R2 ⊆ 유지 |
| 14 | **닫힘** — `sample_test_v1018_2.png`·`figs/P4_lco_heat_validation.png` ×3 = tracked(`git ls-files` 4/4, master) | master git 실측 |
| 15 | **닫힘** — 보존 사본 `iter_1/gen_outinv.ps1`(470행) | AUD-14 |

### 10.3 iter_2 후 게이트 재확인(master)

- G1: 추가 26본 전건 TSV 존재(경로·줄수는 TSV 행 전사) — 검수 라운드 2 에서 기계 재대조.
- G3 60/60 · G4 8/8·13/13 · G6 ⊆ 131/131 · G7 259 그룹(고유본 2건 수동 지정) — 불변.
- 합계 691 파일 · 97,678 줄.

### 10.4 iter_3(검수 라운드 2 반영 · 2026-09-03) — 정책 단위 정의 확정 + 잔여 0 증명

| AUD-R2 | 심각도 | master 판정 | 반영 |
|---|---|---|---|
| 01 | 확정결함 | 인정 | (iv-c) 21본 · (xvii-b) 2본 · (ix-b) 5본 · (vii-b) 3본(+이동 1) = 31본 신규 등재 · §2·§8.3 재생성 |
| 02 | 경미 | 인정 — 정책 문안 확정(아래) · 접두 단위 풀은 DQ-16 | `iter_3/policy_check.txt`(스크립트) 로 (a)(c) 정규식 28종 · (b) 통제 문서 5본 인용 토큰 잔여 = 0 |
| 03 | 경미(회귀) | 인정 | `RB_AL_MASTER` (i-b) → (vii-b) 이동 · 종류 = ledger(통합 Assumption Ledger) |
| 04 | 경미(회귀) | 인정 | (vii) 행 74 귀속 문자열 = (i) 행 79 와 동일 · old/v2 2행 귀속 = `구트랙 RB`(동명이물 경고는 비고) |
| 05 | 경미 | 인정 | 마스터 플랜 v5.4(§2.8 3곳 · Assumptions 11 · "지원 4본" 3곳) |
| 06 | 경미 | 인정 | §10.1 문구 시제 정정 · Step 1 이력은 Step 완료 시 기록 |
| 07 | 제안 | 채택 | 머리·(i) 행 90 라벨 · §3.1 주석(살아 있는 합계·9,567 측정 시각) |
| 08 | 제안 | 채택 | §8.3 표 스크립트 재생성(현재 §1 집합 기준) |
| 09 | 제안 | 채택 | (xvii-b) 비고 + 마스터 플랜 v5.4 OUT-CLAUDEMD 항목(DR-13 후보: P1 인용 경로 스테일) |
| 10 | 제안 | 채택 | (vii-b) CHARTER 3 · (ix-b) radius 판정문 4 + `broadening_w_design` |

**「추가 발견」 정책 문안(master 확정 · 정본 — (iv-b)·(iv-c) 정의·`policy_check.txt` 는 이 문안을 참조)** — (a) 형제 = **파일명 계열**(같은 폴더 · `접두_핵심어` 계열 정규식 일치; 접두만 같은 것은 계열이 아니다 → DQ-16 후보 풀) · (b) 통제 문서(프로젝트 `CLAUDE.md` · 마스터 플랜 · INDEX 3본 = `docs/INDEX.md`·`plans/INDEX.md`·`INDEX_v25.md` — 마스터 플랜 L307 DR-7 ①·L309 Phase 1.1 입력 지정; 그 밖의 `INDEX_v*` 는 (vi) 등재 대상이지 통제 문서가 아니며, 폴더 단위 인용(`docs/INDEX.md`:29·:32 `comp_*/`)은 basename 검사 밖 → DQ-6 처분으로 흡수 — AUD-R4-P1)가 **이력·결정 근거로 인용**하는 md/tex 원문 — 제외 = 코드 `.py` · 데이터 `.json/.txt` · PDF · figs · `CODE_GUIDE_v24`(`INDEX_v25.md`:94 "v1.0.25 미갱신" 스테일 코드 기록 — 7.x 소관) · **`docs/` 하위 구버전 tex 본문(v1.0.10~v1.0.24.1 장 본문·부록)은 DR-7 정독 범위 밖**(§8.3 계수 · 1.2 토픽 한정 시 원천 열람 가능; 현행 v1.0.25/v1.0.25.1 tex 는 (xvi)·(xviii)·2.1 자산 지도 소관) — 등재 = **`old/` 소재 인용 tex(계보 원문)**(xvii-b)·(xvii-c)(비대칭 사유: `docs/INDEX.md` 계보 절이 직접 인용 + 유실 원문 5본의 연속) · **`FITTING_GUIDE` hash 고유 내용 8본**(가이드가 아니라 규약 기록 — `docs/INDEX.md`:62 B-006 U_j 평가 규약)(vii-c) · **`CODE_w_check.md`**(`docs/INDEX.md`:181 인용 관찰 기록)(ix-b) · (b′) 등재 문서가 binding·입력으로 명시 인용하는 규약(charter) 문서 · (c) 동명 폴더 안 md 전건. 적용 = `iter_3/policy_check.txt`(정규식 28종 매치 → S 대조 · 통제 문서 5본 토큰 — **구두점 정규화: 토큰 문자 집합 `[A-Za-z0-9_.-]` 만, 괄호·꺾쇠·백틱은 토큰에 포함하지 않는다(iter_5 AUD-R4-01)** → TSV 해소(동명 basename 은 그중 하나라도 S 또는 제외 클래스면 통과) → S 대조) — **잔여 0**.

**DQ-16(신규)** — 접두 단위 후보 풀(`results/process/` REVIEW·NOTE 계열 ≈ 82본·9,159줄: `V1014_REVIEW_R1_A~R7_B` 20 · `V1013_REVIEW_R1~R10_{A,B,C}` 30 + `V1013_CODE_MAP_ADDENDUM_R10` · `V1012_P43_review_*` 11 + `V1012_P42b_fixer_note` · `V1010_P1~P5_review1` 5 · `V1010_HANDOVER_INSPECT_*` 11 · `V1010_LCO_STYLE_REPORT` · `V1015_P2_PHYSICS_REVIEW` · `V1017_REVIEW_COMPLETE`(등재) · `V1019_FINAL_REVIEW_UNION`)은 정독 모집단 밖·**1.2 Step 3 토픽 한정 열람 후보 풀**로 §8.3 계수 유지(master 처분: 등재 X · Step 2 배정표 부록에 풀 목록 첨부).
**DQ-17(신규)** — 프로젝트 `CLAUDE.md`:14–15 P1 인용 경로 `Claude/docs/graphite_ica_dynamic_ver5.tex`·`Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` = 스테일(실물 `Claude/old/_archive/Archive_old/`) → DR-13 OUT-CLAUDEMD 개정안 항목(사용자 결정 전 CLAUDE.md 무수정) · radius 조사 카드 14본·보조 기록 1본(`DOCS_say_about_distribution.md`)·CH2_v3 조사 카드 등은 1.4 토픽 한정 열람 후보(계수만).

**iter_3 후 합계** = 722 파일 · 103,537 줄 → 1차 스크립트 결과 (a)(c) 잔여 0 · (b) 잔여 8(`docs/INDEX.md` 인용 `old/` 계보 tex 6 · `INDEX_v25.md` 인용 경쟁 저작 결정 기록 2) → **iter_3b** 에서 (xvii-c)·(viii-c) 로 등재 → (b) 잔여 0. **iter_3b 합계 = 730 파일 · 110,253 줄** → iter_4(FITTING_GUIDE 8본) 후 **iter_4 합계 = 738 파일 · 111,107 줄 · 미등재 1,913/604,011** → iter_5(AUD-R4-01 `CODE_w_check` 등재) **최종 합계 = 739 파일 · 111,130 줄 · 미등재 1,912/603,988**(§8.3 재생성 · `iter_3/policy_check.txt` 최종판).

### 10.5 iter_4(검수 라운드 3 반영 · 2026-09-03) — 확정결함 0 · 경미·제안 반영

| AUD-R3 | 심각도 | master 판정 | 반영 |
|---|---|---|---|
| 01 | 경미(회귀) | 인정 | (xvii-c) 6행 고유본(사본 n: …) 표기 + "hash 미대조" 삭제(§4 #224 등 참조) · (viii-c) 2행 표준형 사본 표기 |
| 02 | 경미 | 인정 | 정책 문안 정본 = §10.4 한 곳 · (iv-c) 정의·`policy_check.txt` 는 참조/동일 문자열 · "27종" → 28종 |
| 03 | 경미 | 인정 | Step 1 이력 "407건" → PC 295(md/tex 정의) · 검수 R2 407(6 확장자 정의) 병기 |
| 04 | 경미 | 인정 | §0 매핑 규칙(COMPARISON/FIXLIST/SWEEP_LIST→감사 — iter_5: 중복 `*INSPECT*` 제거(AUD-R4-15) · CHARTER→기타(규약) · FITTING_GUIDE→기타(가이드—규약 기록)) · 귀속 예외에 `old/Ch[12]_v*/` 6본 추가 |
| 05 | 경미 | 인정 | (b) 제외 근거 문장 정정: `docs/` 구버전 tex 본문(v1.0.10~24.1) = DR-7 정독 범위 밖(§8.3 계수 · 1.2 토픽 한정 열람 가능) · 현행 두 버전만 2.1 소관 · (xvii-c) 비대칭 사유 명시 — §10.4·PC 반영, (xvii-b) 정의는 iter_5 에서 정정(AUD-R4-03) |
| 06 | 제안(최약점) | **채택** | `FITTING_GUIDE` = 규약 기록(`docs/INDEX.md`:62 B-006) → hash 고유 내용 8본 (vii-c) 등재 · `CODE_GUIDE_v24` 는 제외 유지(사유 명기) |
| 07 | 제안 | 채택 | PC 에 동명 basename 해소 규칙 + 미해소 목록 첨부 |
| 08 | 제안 | 채택 | 9행 비고에 `docs/INDEX.md` :line · (ix-b) 행 1 "원천" = 추정 표기 |
| 09 | 제안 | 채택 | 마스터 플랜 §2.8 각주(괄호 줄수 = Read 표기 · 정본 = OUT-INV §2) — v5.4 추기 |
| 10 | 제안 | 채택(Step 2) | DQ-16 파일 단위 목록(≈82본)은 Step 2 배정표 부록에 첨부 |

**iter_4 후 최종 합계** = 738 파일 · 111,107 줄 · 미등재 1,913/604,011 · 정책 잔여 (a)(c) 0 · (b) 0(`iter_3/policy_check.txt` iter_4 최종판).

### 10.6 iter_5(검수 라운드 4 반영 · 2026-09-05) — 확정결함 1(토크나이저) 정정 · 경미 10 · 제안 4 · 약생존 1

검수 라운드 4 = Workflow(렌즈 3 병렬 → 발견 28건 × 반박 3인 순차 → 통합 저작; 사용자 병렬 상한 지적 후 동시 ≤3 로 재실행) · `iter_4/audit_log_r4.md`.

| AUD-R4 | 심각도 | master 판정 | 반영 |
|---|---|---|---|
| 01 | **확정결함** | 인정 — iter_4 토크나이저 정규식 `[A-Za-z0-9_\-\.\(\)]+` 가 여는 괄호를 토큰에 포함해 `(CODE_w_check.md` 를 미해소로 오분류 | 토큰 문자 집합에서 `()` 제거 후 재실행 · `docs/INDEX.md`:181 인용 `CODE_w_check.md`(23줄) (ix-b) 행 6 등재 · §10.4 정책 문안에 토큰화 규칙 명기 · (b) 잔여 0 재성립(`policy_check.txt` iter_5 판) · 부수: `docs/INDEX.md`:174 인용 `graphite_ica_ch2_v5.tex` = 실물 부재 → §8.1 |
| 02 | 경미 | 인정 | §10.4 표 행 02 "27종" → 28종 |
| 03 | 경미 | 인정 | (xvii-b) 정의 구 근거 문장 정정 · §10.5 행 05 반영 열 명기 · Step 1 이력 근거 3 시점 표기 |
| 04 | 경미 | 인정 | (vii-c) 정의 "12 폴더" → 버전 폴더 19(폴더당 1본) |
| 05 | 경미 | 인정 | Step 1 이력 게이트 표 730 → 739(R4 재실행 738/738 + iter_5 +1) · L60·L65 시제·수치 |
| 06 | 경미 | 인정 | Step 1 이력 "계획서 815행" → 816 |
| 07 | 경미 | 인정 | 마스터 플랜 Correction History v5.4 행 라벨("— iter_3")을 시점별 이력 병기로 정정 · Assumptions 11 739/111,130 — v5.5 |
| 08 | 경미 | 인정 | (ix-b) 정의·DQ-17 "16본" → 조사 카드 14 + 보조 기록 2 분해 · `CODE_w_check` 등재 · `DOCS_say` 계수 유지 사유 |
| 09 | 경미 | 인정 | radius 6행·rework 2행·2track 1행 귀속에 ", 추정" 부기 · §0 L29 규칙 문구 |
| 10 | 경미 | 인정 | §0 L29 plans 절에 07-01 이후 무토큰 규칙(`fable-reaudit*`→v1.0.12 확정급 · `anodefit-*`→v1.0.23 추정) |
| 11 | 경미 | 인정 | §0 L28 매핑 규칙 8종 추가(AUD_·V1010_*_REPORT·CHERRYPICK·AUTHOR_BRIEF·RB_AL_MASTER·.txt·CLAUDE.md·json) · `CHARTER*` → `*CHARTER*` · 글로브 의미론 명기 |
| 12 | 제안 | 채택 | Step 1 이력 「변경·생성 파일」 목록·commit 갱신 |
| 13 | 제안 | 채택 | §8.3 서술 FITTING_GUIDE 한정(사본 11본만 미등재) |
| 14 | 제안 | 채택 | §3.1 주석에 iter_4 후 살아 있는 값(816줄 → 10,388) 시점 병기 |
| 15 | 제안 | 채택 | §0 L28 iter_4 구 중복 `*INSPECT*` 제거 · §10.5 행 04 문구 |
| P1 | 약생존(1/3) | 부분 채택 | §10.4 (b) 에 "INDEX 3본 = 마스터 플랜 L307/L309 지정" 근거 + 폴더 단위 인용의 DQ-6 흡수 명기 · (iv-b) 정의를 "INDEX 3본 — 정본 = §10.4" 로 정합 · `INDEX_v1022` 인용 21본은 DQ-6 처분(1.3 Step 9 `docs/v1.0.22/results/*` 토픽 한정 원천) 유지 |

**iter_5 후 최종 합계** = 739 파일 · 111,130 줄 · 미등재 1,912/603,988 · 정책 잔여 (a)(c) 0 · (b) 0(`iter_3/policy_check.txt` iter_5 최종판).

