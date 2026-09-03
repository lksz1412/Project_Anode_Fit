# audit_log — Phase 1.1 Step 1 OUT-INV 검수 · 라운드 1 (iter_1 · 2026-09-03)

> 검수 sub(Fable 5.1) → master. 지시 = `Claude/results/handoffs/v1027-phase-1.1-inventory/audit_checklist.md`(전문 정독 L1–66). 검수 대상 = 작업 sub 산출 3본(`Claude/results/V1027_HISTORY_INVENTORY.md` 1,463행 · `iter_1/inventory_raw.tsv` 2,651행 · `iter_1/work_log.md` 131행). 렌즈 4종 = 구조 · 적대검산 · 완결성 · usable. 본 sub 의 파일 생성 = 본 audit_log 1본뿐 · 기존 파일 무변경 · git 명령 0회 · `Codex/` 접근 0회(재측정 명령은 전부 `D:\Projects\Project_Anode_Fit\Claude` 아래 + 루트 `CLAUDE.md` 1본).

## 0. 헤더 — 라운드·렌즈·청크 경계

| 항목 | 값 |
|---|---|
| 라운드 | 1 (통상 산출물 등급 — 검수 sub ≥1R, 연속 2R 확정결함 0 수렴) |
| 렌즈 | 구조 · 적대검산(독립 재측정 R-a~R-i) · 완결성 · usable(Step 2 배정표 가능성) + §2.4 사양·의도 대조 |
| OUT-INV 청크 경계(6청크, 전 영역 cover) | ① L1–250 (§0 머리 · (i) 전건 · (ii) · (iii) · (iv) · (v) · (vi) · (vii) 헤더) ② L251–500 ((vii) 행 1–81 · (viii) 행 1–159) ③ L501–750 ((viii) 행 160–167 · (ix) · (x) · (xi) · (xii) · (xiii) · (xv) · (xvi) 행 1–31) ④ L751–1000 ((xvi) 행 32–60 · (xvii) · (xviii) · (xix) · §2 · §3 · §4 그룹 1–97) ⑤ L1001–1250 (§4 그룹 98–259 · §5 · §6 · §7 행 1–22) ⑥ L1251–1463 (§7 행 23–131 · §8 · §9) |
| 청크 크기 사유 | 500행 청크는 Read 도구 토큰 상한(25k)을 넘어 250행으로 축소 — 경계는 절 경계와 무관한 기계 분할이며 겹침·누락 0 |

## 1. 발견 표

4-tier = 확정(재계산·재대조 실물) / 근거 미발견 / 추정 / 미검증. 위치의 파일 약칭: INV = `Claude/results/V1027_HISTORY_INVENTORY.md` · WL = `iter_1/work_log.md` · MP = `Claude/plans/2026-09-02-v2-master-plan.md`.

| ID | 심각도 | 4-tier | 위치 | 내용 | 재현 근거(명령·수치) | 수정 제안(한 줄) |
|---|---|---|---|---|---|---|
| AUD-01 | **확정결함** | 확정 | INV §1 (iv)·(viii)·(ix) · §8.3 L1436 | **「추가 발견」 정책이 비일관 적용돼 정독 모집단에서 감사·Result 성격 md 11본·885줄이 빠졌다.** 같은 폴더 `results/process/` 의 `FABLE_REAUDIT_P0_P1/P2_P3/P4_RESULT.md` 3본은 (viii) 행 107–109 에 "추가 발견" 으로 등재했으나 형제 파일 `FABLE_REAUDIT_C1~C6_note.md` 6본(63·65·68·68·95·111줄 = 470, Fable 재감사 노트 = (iv) 유사 감사)은 미등재; `V1010_INSPECT_draft_C3.md` 는 (ix) 행 86 에 등재했으나 같은 v1.0.10 문제점검 산출 `docs/v1.0.10/V1010_PROBLEM_REPORT.md`(55)·`V1010_HANDOVER_INTEGRITY_REPORT.md`(45 — (i) 행 74·76 계획서의 Result 성격)은 미등재; `results/process/V1014_AUDIT_ADJUDICATION.md`(27)·`V1014_CODE_MENTION_AUDIT.md`(254 — 프로젝트 `CLAUDE.md` P3 #8 이 "CODE_MENTION_AUDIT 승계" 로 명시 인용하는 감사)·`V3_W4_PHYSICS_AUDIT.md`(34) 미등재. §8.3 은 이들을 "results/process 의 비-ledger·비-Result md(… 등)" 로 뭉뚱그려 계수만 했다(L1436). brief §4 말미 "패턴에 안 잡히는 유사 파일 발견 시 추가 발견으로 같은 군에 넣고 비고에 표시" 와 어긋나며, Step 2 배정표를 "이 표만으로" 세우면 위 11본은 정독 대상에서 조용히 탈락한다(usable 렌즈 실패). | `Get-ChildItem Claude -Recurse -Filter '*AUDIT*.md'` → 38 중 §1 미등재 12(위 9 + `docs/v1.0.23/results/comp_v23/COND_AUDIT.md` 301 + `old/results/PROJECT_AUDIT_REPORT*.md` 2); `docs/v1.0.10/*.md` = FITTING_GUIDE·HANDOVER_v1.0.11·V1010_HANDOVER_INTEGRITY_REPORT·V1010_PROBLEM_REPORT 중 뒤 2본 §1 부재; §1 행 집합 611 대조 스크립트(본 sub 실행 10:4x). 줄수는 `(Get-Content).Count`. | (iv) 또는 (ix) 에 "추가 발견(감사)" 로 9본, (viii) 에 "추가 발견(Result)" 로 2본 등재 + §8.3 문구 정정. master 직접 수정 가능(행 추가 11 · 합계 §2 갱신 665→676 · 93,005→93,890). |
| AUD-02 | 경미 | 확정 | INV (i) 정의 L37 · §8.3 L1414·L1417 · MP L305 | MP L305 의 DR-7 전문 정독 ① 은 파일명 glob(`*master*`·`*MASTER*`·`MASTER_ROADMAP*`)으로 정의돼 있는데 (i) 은 `Claude/plans/*.md` 폴더 한정이라 glob 매치 6본이 인벤토리 밖: 구트랙 마스터 3(`old/v2/plans/MASTER_ROADMAP_v2.md` 447 · `old/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md` 780 · `old/Archive_oldtrack/RB_AL_MASTER.md` 139) + 마스터플랜 아닌 동명 3(`results/research/CH1v9_LCO/10_sources_master.md` 45 · `results/research/CH2_v3/10_sources_master.md` 60 · `results/builds/v9/v9-00_spine/review2/V2_citations_master.md` 267). (vii)·(viii) 은 `old/**` 매치를 DQ-5 로 등재했으면서 (i)·(ii) 는 `old/plans`·`old/v2/plans` 를 §8.3 계수에만 두어 old/ 처리 기준이 군마다 다르다. 또 (i) 행 25 는 `connective-masterequation` 의 glob 오매치를 경고했으나 위 `*_master.md` 3본의 오매치 경고는 없다. | `Get-ChildItem Claude -Recurse -Filter '*MASTER*.md'` → 21 중 §1 미등재 6(위 목록). `old/v2/results/EXECUTION_LEDGER_v2.md`:1–7 "Chapter 1 Rebuild v2 · 2026-05-28 · Predecessor old/results PHASE_A_D(v1)" → old/v2 = 구트랙 계열 확정(Fable v2 와 동명이물). | DQ-5 범위를 (i)·(ii) 로 확장(구트랙 마스터 3 등재 + 비-마스터 3 은 "glob 오매치 · 등재 X" 명기) 또는 MP L305 glob 을 "(i) 군 안에서" 로 한정 — master 결정. |
| AUD-03 | 경미 | 확정 | INV (ix) 정의 L512 · MP L309 (ix) | (ix) 정의 `docs/v1.0.22/results/comp_v23/*.md` 와 **동명 폴더** `docs/v1.0.23/results/comp_v23/` 가 존재하고 그 안 `COND_AUDIT.md`(301줄)가 미등재·미언급이다. MP L312 "동명이물 경고" 취지상 폴더 동명 충돌은 표면화가 필요하다. | `Get-ChildItem Claude\docs -Recurse -Filter 'COND_AUDIT.md'` → `docs/v1.0.23/results/comp_v23/COND_AUDIT.md` 301 · `(Get-Content).Count`=301. | (ix) 에 "추가 발견(동명 폴더 v1.0.23/comp_v23)" 1행 + 비고에 폴더 동명 경고. |
| AUD-04 | 경미 | 확정 | INV §8.1 L1369 · MP L197 | §8.1 "기대 항목 중 실물 부재 = 0건" 은 brief §4 기대치 기준으로만 참이다. 통제 문서 MP §2.9 L197 은 HANDOVER 미검독 잔여를 "v1.0.10(HANDOVER_v1.0.10)·v1.0.12·구트랙 3" 으로 적어 `HANDOVER_v1.0.10`·v1.0.12 인계 실물을 전제하는데 둘 다 부재다(v1.0.10 폴더 인계 = `HANDOVER_v1.0.11.md` 1본 · v1.0.12 폴더 md = `FITTING_GUIDE.md` 1본). (iii) 행 1 비고가 폴더·파일명 불일치를 관찰했으나 §8.1 에 부재로 올리지 않았다. | `Get-ChildItem Claude -Recurse -Filter 'HANDOVER_v1.0.1*' \| ? Name -match '1\.0\.1[02]'` → 0건; `docs/v1.0.12/*.md` = FITTING_GUIDE.md 만. | §8.1 에 "MP L197 기대 `HANDOVER_v1.0.10`·v1.0.12 인계 = 실물 부재(v1.0.11 인계가 v1.0.10 폴더에 있음)" 1줄 추가 → MP §2.9 정정 후보로 이관. |
| AUD-05 | 경미 | 확정 | INV (i) 행 79 L121 · (vii) 행 74 L325 | 버전 귀속 "v1.0.18" 2행 = 어휘 밖 값. brief §4 어휘 `v1.0.10 … v1.0.26` 은 계보 버전 집합이고 MP L321 계보에 v1.0.18 은 없다(v1.0.18.1·v1.0.18.2 만). `V1018_EXECUTION_LEDGER.md`:30–31 은 18.1 증판과 18.2 코드를 한 원장에 담으므로 두 개정 공통 문서다. 611행×2열 중 어휘 밖 값은 이 2행뿐(확정 — 어휘 집계 스크립트). | §1 611행 버전 귀속·문서 종류 값 전수 집계(본 sub 스크립트) → "v1.0.18" = 2. | "v1.0.18.1·v1.0.18.2(공통 — 추정)" 로 표기 + DQ-2 편입. |
| AUD-06 | 경미 | 확정 | INV (x) 행 1 L615 · §3.5 L888 · WL §2-1 L30 | `jcp_extract.txt` "brief 724 → 실측 725(방향 반대 · 미검증)" 은 닫을 수 있는 항목이었다: 파일이 **개행으로 끝나지 않아**(LF 724 · endsWithNewline False · CR-only 0) `(Get-Content).Count` = 724 + 1(마지막 무개행 행) = 725 이고, brief 724 = LF 계수(`wc -l` 방식)다. 작업 sub 가 다른 5파일에 쓴 같은 `Get-Content -Raw` 끝문자 검사를 이 파일에만 생략했다. | `$r=Get-Content jcp_extract.txt -Raw; ([regex]::Matches($r,"`n")).Count` → 724 · `$r.EndsWith("`n")` → False · `(Get-Content).Count` → 725. | (x) 비고·§3.5 를 "확정: 끝 개행 없음 → Get-Content +1 · brief 는 LF 계수" 로 갱신. |
| AUD-07 | 경미 | 확정(mtime 근거) · 이전 줄수 811 은 미검증 | INV §3.1 L857–858 · §9 DQ-9 L1457 · WL §2-2 L31 | plans 10,384 vs 1g 10,383 의 +1 파일은 특정 가능하다: 1g(09:24)~TSV(09:34:39) 창에서 수정된 `Claude/plans/*.md` 는 `2026-09-02-v2-master-plan.md`(LastWriteTime **09:26:07**) 1본뿐이며 `INDEX.md` 는 08:48:05(1g 이전). 따라서 +1 = 마스터 플랜 811→812 (이전 값 811 은 git 없이 미검증). 작업 sub 는 mtime 조회(읽기 전용·허용 도구)로 스스로 닫을 수 있었다. | `Get-ChildItem Claude\plans\*.md \| sort LastWriteTime -Desc \| select -First 3` → v2-master-plan 09-03 09:26:07 · INDEX.md 09-03 08:48:05 · v1025-surgical 07-26. 1g 파일 헤더 "09:24". | DQ-9 를 "특정: 마스터 플랜(mtime 09:26:07) · 이전 줄수는 git 대조 시 확정" 으로 닫음. |
| AUD-08 | 제안 | 확정 | INV §3.4 L878 | `CLAUDE.md` brief 90 의 "작성 시점 실물이 다른 것인지 오기인지 미검증" 은 좁힐 수 있다: 파일 LastWriteTime = 2026-07-26 22:56:20 으로 brief·R3 작성(09-02~03) 훨씬 이전부터 무변경 → "실물이 달랐다" 가설 기각 → 오기(또는 다른 계수 방식) 확정. 또 `wc -l` 가설도 기각(LF 88 = CRLF 88 = Get-Content 88, 끝 개행 True) — R3 89 = Read 도구의 마지막 빈 행 표시(본 sub 도 `ch1_graphite_v1.0.24.tex` Read 에서 62행 파일이 63행으로 표시됨을 직접 확인). | `(Get-Content CLAUDE.md).Count`=88 · Raw LF=88 · CRLF=88 · endsNL=True · mtime 07-26. | §3.4 표 3행을 "근거 미발견(오기 확정 — 실물 07-26 이후 무변경)" 으로. |
| AUD-09 | 제안 | 확정 | WL §2-1 표 L28 · INV (xi) 행 8 L633 | `build.log` "36 = 36 일치 — 오프셋 규칙의 예외; 원인 미조사" 는 파일 구조가 아니라 **R2 의 표기 불일치**다: build.log 는 LF 36·끝 개행 True 라 Read 표시는 37행이어야 하는데 R2 는 "L1–L36" 으로 적었다(R2 는 같은 표에서 README 50/실측 49 · skew_log 12/11 · 26A README 199/198 처럼 +1 표기를 썼고, `summary_skew.json` 은 끝 개행 없음(LF 3)이라 4=4 가 맞다). | `build.log` Raw LF=36 endsNL=True · `summary_skew.json` count=4 LF=3 endsNL=False. | WL 표 비고를 "R2 표기 불일치(파일은 끝 개행 True)" 로 정정. |
| AUD-10 | 경미 | 확정 | INV §0 버전 귀속 규칙 L29 · (vii) 행 81 L332 · (viii) 행 88–97 | 규칙 텍스트에 없는 예외가 적용됐다: `V10NN_*`→v1.0.NN 규칙대로면 `results/V1024_FEEDBACK_EXECUTION_LEDGER.md` 는 v1.0.24 인데 표는 v1.0.24.1 이다(`results/PHASE_FB*`→24.1 규칙은 있으나 FEEDBACK ledger 규칙은 없음). 귀속 자체는 `docs/INDEX.md`:21 "리비전 이력 = ../results/V1024_FEEDBACK_EXECUTION_LEDGER.md·PHASE_FB0~9_RESULT.md"(v1.0.24.1 절) 로 정당하나 규칙·근거가 표에 없다. | `docs/INDEX.md` L21 Read. | §0 규칙에 `V1024_FEEDBACK_*`→v1.0.24.1(docs/INDEX.md:21) 1항 추가, 행 81 비고에 근거 병기. |
| AUD-11 | 경미 | 확정 | INV §9 DQ-1 L1449 · (xix) L820 · (x) L615 · (xv) L707 · (i)·(vii)·(viii) 세부 표기 | ① DQ-1 이 열거한 어휘 밖 세부(감사(머지 판정)·Result(집행 보고)·기타(…)·서지 원장(초안)) 외에 `통제(프로젝트 지침)`(어휘 토큰은 `통제(본 arc)`) · `조사(원문 추출)` · `시드(판독·json)` 3종이 더 있다. ② 같은 계보를 다른 문자열로 적은 세부 표기: "v10 rework 06-30"(1)/"v10 rework"(1) · "v9 2track 06-30"(1)/"v9 2track"(1) · "v1.0.12(fable reaudit → v12 저작)"(4)/"v1.0.12(fable reaudit)"(3) — Step 2 계보 순 기계 정렬 시 별개 키로 갈린다. | 문서 종류 27종·버전 귀속 71종 값 전수 집계(본 sub 스크립트). | DQ-1 목록 보강 + 세부 표기 6종 통일. |
| AUD-12 | 제안 | 확정 | INV §4 규칙 L898 · 그룹 #179 L1082 · #239 L1142 · DQ-4 L1452 | 고유본 규칙 검증 결과: 259 그룹 전건 TSV 구성원 수 일치 · 버전 폴더 있는 230 그룹 전건 "가장 이른 버전 폴더" 규칙 충족 · 버전 폴더 없는 29 그룹 중 27 은 ordinal 경로 정렬 최상과 일치, **2 그룹은 불일치**(#179 `REVIEW_LEDGER_CH2_10ROUND_CLAUDE_rerun_5-29.md` 선택 vs ordinal 최상 `REVIEW_LEDGER_CH2_10ROUND.md` · #239 `graphite_ica_chapter2_CLAUDE_criticalfix_5-29.tex` 선택 vs `graphite_ica_chapter2.tex`) — 원인은 PowerShell 기본 culture 정렬에서 `_` 가 `.` 보다 앞서기 때문(ordinal 은 반대). "경로 정렬 최상" 규칙이 정렬 의미론을 명시하지 않아 같은 폴더 동명이물에서 의미상 사본(rerun·criticalfix)이 고유본이 됐다. #179 는 DQ-4 에 있으나 #239 는 없다(다만 #239 는 어느 군에도 미등재라 정독 영향 0). §1 의 hash 중복 구성원 110행은 전건 §4 고유본과 일치하는 고유본/사본 표기를 갖고 단독 501행에 오표기 0. | 본 sub 스크립트: badGroups=0 · rule-consistent 257/259 · §1 dup rows ok=110 missing=0 wrong=0. | DQ-4 에 "정렬 의미론(ordinal vs culture) 명시 + 동명이물 2건은 파일명 의미(base < rerun/fix)로 수동 지정" 추가. |
| AUD-13 | 제안(계획서 정정 후보) | 확정 | MP L89 · L103 · L203 · L231 · L366 · L372 · L424 | OUT-INV §6 실측(마스터 3 + 포함 53 + 미포함 4)이 맞고 MP 가 틀리다 — 근거 행: ① `ch1_preamble.tex`:2–3 "graphite_ica_ch1_v1.0.21.tex 가 \input 한다" · `ch2_preamble.tex`:2–3 동형 · `common_preamble_v1024.tex`:3 "= 구 ch1_preamble ∪ ch2_preamble" · 마스터 3본 비주석 `\input` 55건(33/12/10) 전부 `\input{_sections/…}` 형태이며 `\include`·`\subfile`·`\import` 0 · `_sections` 안 중첩 `\input` 0(v1.0.25.1 tex 90본 Grep 매치 = 마스터 3본뿐). ② 따라서 MP L203 "지원 4본(divider·ch1_preamble·ch2_preamble·common_preamble)" 중 실제 빌드 포함 지원 파일은 divider(ch1 L39)·common_preamble(ch1 L10·ch2 L8·ch3 L8) 2본, preamble 2본은 orphan. ③ MP L231 "모집단 60 = 빌드 58 + 미포함 2" → "마스터 3 + 포함 53 + 미포함 4". ④ MP L372·L424 "마스터 3본 + 지원 4본 = 332줄 · 53본 8,882줄" 은 R4a 의 Read 표기(+1/파일, 29본) 합 5,558 을 그대로 써서 생긴 오차 — TSV 정의로 마스터 130 + 지원 4본 231 = **361**, 53본 = **8,853**(합 9,214). ⑤ MP L103 은 박스 환경 정의 근거를 orphan `ch1_preamble.tex`:31–36·`ch2_preamble.tex`:31–35 로 인용 — 빌드에 실제 쓰이는 정의는 `common_preamble_v1024.tex`:33–41(`\newtheorem*` keybox·codebox·signbox·verifybox·derivbox·bgbox·srcbox·warnbox·procedurebox 9종, 본 sub Grep). | 본 sub R-e 스크립트 출력(§5 표) · Grep `^[^%]*\\(input\|include\|subfile\|import)\{` v1.0.25.1/**/*.tex → 55/3파일 · 줄수 합 = OUT-INV (xvi) 값 재합산. | master 가 MP Correction History 로 정정(OUT-INV 무수정). DQ-3 은 "orphan 2본 = 계보 확인용 토픽 한정" 을 기본값으로 제안. |
| AUD-14 | 제안 | 확정(생성 주체는 mtime 추정) | `iter_1/gen_outinv.ps1` · WL §3 L48 · INV §0 L25 · DQ-15 | iter_1 폴더에 `gen_outinv.ps1`(70,288 B · 470행) 실물이 있다. CreationTime 10:16:52 = work_log(10:12:21)·audit_checklist(10:14:12) **이후**이고 세션 스크래치패드 `gen_outinv.ps1`(10:09:08)과 SHA256 동일 → master 가 사후 복사한 것으로 추정(작업 sub 의 "프로젝트 안 신규 3본" 진술과 모순 없음). 다만 현 폴더 상태와 WL·INV 의 "3본" 서술이 어긋나고, audit_checklist 입력 목록·Step 1 이력에 이 복사가 기록돼 있지 않다. `.ps1` 은 TSV 모집단 밖이라 인벤토리 수치 영향 0. | `Get-Item iter_1\gen_outinv.ps1` → Created 09-03 10:16:52 · 70288 B · hash = 스크래치패드 본과 동일(True). | Step 1 이력·DQ-15 결정에 "스크립트 보존 사본 = iter_1/gen_outinv.ps1(10:16 master 복사)" 기록. |
| AUD-15 | 제안 | 확정 | INV (xvi) 행 29 L748 · 행 5 L724 · §7 말미 L1363 | 태그 정책 비일관: `ch1_preamble`·`ch2_preamble` 는 R4a grep(31–36) 을 `R4a(grep)` 로 태그했으나 같은 R4a Read Coverage 의 "카운트 grep" 대상 `ch1v22_partT_divider` 는 `—` 로 두고 §7 말미 일괄 기록으로 돌렸다. 정의는 §0 L30 에 있으나 두 경우의 경계(행 범위 grep 은 태그 / 카운트 grep 은 미태그)가 적혀 있지 않다. | R4a L359–360 대조. | §0 L30 에 "행 범위가 특정된 grep 만 태그" 1구 추가. |

발견 합계: **확정결함 1 · 경미 8(AUD-02·03·04·05·06·07·10·11) · 제안 6(AUD-08·09·12·13·14·15)**.

## 2. 최약점 1곳

**AUD-01 — 「추가 발견」의 비일관 적용으로 정독 모집단이 조용히 새는 것.** 인벤토리의 존재 이유는 "정독 대상 전건을 실물로 고정" 하는 것인데, 같은 폴더의 형제 파일(`FABLE_REAUDIT_P*_RESULT` 는 등재 · `FABLE_REAUDIT_C1~C6_note` 는 미등재), 같은 점검의 산출(`V1010_INSPECT_draft_C3` 등재 · `V1010_PROBLEM_REPORT` 미등재), 헌법이 인용하는 감사(`V1014_CODE_MENTION_AUDIT` — 프로젝트 `CLAUDE.md` P3 #8)가 §8.3 의 "… 등" 안에 묻혀 있다. Step 2 가 "OUT-INV 파일 집합 = 배정표 파일 집합(차집합 0)" 게이트로 닫히면 이 누락은 이후 어느 게이트에서도 잡히지 않는다. AUD-02·03 도 같은 뿌리(폴더 한정 정의 vs 성격·glob 기준 정독 범위)다.

## 3. 렌즈별 통과·미통과 + §2.4 항목별 O/X

### 3.1 렌즈

| 렌즈 | 판정 | 근거 요지 |
|---|---|---|
| 구조 | 통과 | 군 (i)~(xix) 전건 표 존재 · 열 7개(xvi 8개) 고정 · 611행 빈 셀 0 · 문서 종류 값 27종 전부 어휘 토큰 + 괄호 세부(AUD-11) · 버전 귀속 어휘 밖 2행(AUD-05) · 한 파일 1군 계수 규칙 명시·중복 path 0 · 665 = Σ군 계수, 611 = 665 − 60 + 6 재현 · Codex 경로 등장 = §5.2 전사·무접근 선언 17행뿐(측정치 0) · TSV 2,651행 전부 4열·전건 `Claude\` 하위 또는 루트 `CLAUDE.md`(case-sensitive `\Codex\` 0) |
| 적대검산 | 통과(수치 오류 0) | R-a~R-i 전 항목 재현(§4 표) · path:line 근거 24건 실물 대조 전건 일치 · 작업 sub 값과 다른 수치 0 |
| 완결성 | **미통과(경미)** | AUD-01·02·03·04 — 유사 파일·동명 폴더·통제 문서 기대 부재가 §8 에 명시되지 않음. 등재된 것은 완결(§7 ⊆ 131/131 · §1↔§4 표기 110/110) |
| usable | 조건부 통과 | 버전 귀속·R#·고유본/사본 열은 기계 추출 가능(정규식 `사본\(고유본 = `·`고유본\(사본 n:` 로 110행 전건 파싱 성공). 단 AUD-01·02·03 의 14본이 표 밖이라 "이 표만으로" 세운 배정표는 그만큼 좁고, AUD-11 ② 의 세부 표기 불일치는 정렬 키를 갈라놓는다 |

### 3.2 마스터 플랜 Step 1 (i)~(xvi) 요구 대조

| 항목 | 요구 | O/X | 근거 |
|---|---|---|---|
| (i) | plans 91 + INDEX | O | 92 + (vi) INDEX 1 = 93 · 재측정 93/10,384 |
| (ii) | PLAN_* 15 + v1020 master | O | 16/852 · 재측정 15/645 + 207 |
| (iii) | HANDOVER 25 + old/ 3 별도 표시 · hash 사본 판정 | O | 28 행 · old 3 "구트랙(별도 표시)" · v24 ×4 · v25 ×2 사본 표기 |
| (iv) | Fable 8 | O | 8/885 |
| (v) | CLOSING | O | 105 |
| (vi) | INDEX 3 + 각 INDEX_v* | O | 10 (docs 전건 Glob 일치) |
| (vii) | results ledger 30 + docs vN/results ledger | O | 81 (results 30 = 2·26·2 재현 · docs 20 · old 31) |
| (viii) | MERGE_READINESS·CHANGE_LOG/LEDGER·PHASE_*_RESULT·AUDIT_LINEAGE·DATA_ADDENDUM·DOC_EDIT_REPORT·T13_T14·CASCADE_TODO·ARCHIVE_NOTE | O (패턴 전건) / △ (유사 파일) | 패턴 11종 Glob 미등재 0 · 유사 파일 AUD-01 |
| (ix) | comp_v24·comp_v26_data·comp_v23·comp_SM2·comp_FR·ROADMAP·v1.0.20 results 4종·TERMS_POLICY·TONE_AUDIT | O / △ | comp_v24 md 31/31 · comp_FR 31/31 · comp_SM2 5/5 · comp_v23(v1.0.22) 5/5 · v1.0.20 상위 md 31/31 · 동명 폴더 v1.0.23/comp_v23 미언급(AUD-03) |
| (x) | dossier · jcp_extract | O | 49 · 725(AUD-06) |
| (xi) | v1.0.26 실물 3 + build.log | O | 14 (추가 발견 2 = DQ-13) |
| (xii) | 서지 원장 4 (hash) | O | 4 · V1022=V1023 hash 동일 재현 |
| (xiii) | reflect 계획서 · REFLECT ledger 실물 경로 | O | 실물 경로 표 + hash ABE37E4B… 4본 동일 재현 |
| (xiv) | untracked Claude 8 지위 + Codex 13 무접근 | O | 8/8 근거 path:line 전건 실물 일치 · 13/13 고정 · 열람 0 |
| (xv) | R1~R7 + json + v1 초안·work_log | O | handoffs/2026-09-02 폴더 23/23 전건 |
| (xvi) | 60 tex 빌드 포함/미포함 열 | O | 60/60 · 마스터 3 + 포함 53 + 미포함 4 재현 |
| (xvii)·(xviii)·(xix) | brief 추가군 | O | 5/11,876 · 60/9,207(diff 6 재현) · 88 |

### 3.3 게이트 1.1(MP L315) 항목별

| 게이트 | O/X | 근거 |
|---|---|---|
| Test-Path True 100% | O | 611/611(본 sub 재실행) |
| 줄수 열 빈 셀 0 | O | 611/611 숫자 · 재계수 불일치 0 |
| brief §3-C 차이 파일명·줄수 열거 + 정본 확정 | O | plans 93/10,384 · HANDOVER 25/1,612 · PLAN_* 15/645 — 3건 정본 + 차이 파일 열거(AUD-07 로 +1 특정 가능) |
| 배정표 차집합 0 | N/A | Step 2 몫 |
| 빌드 포함/미포함 60/60 | O | 재현 |
| untracked Claude 8 지위 빈 셀 0 | O | 8/8 |
| Codex 13 무접근 표기(열람 0) | O | 13/13 · TSV·INV 측정치 0 |

### 3.4 DQ 15건 분류

| DQ | 정말 결정 필요? | 작업 sub 가 닫을 수 있었나 | 닫을 주체 |
|---|---|---|---|
| DQ-1 어휘 세부 | 예(어휘 정책) | 아니오 | master (AUD-11 보강 후) |
| DQ-2 추정 귀속 | 예 | 아니오(정독 필요) | Step 2 |
| DQ-3 orphan preamble 정독 | 예(계획서 정정 연동) | 아니오 | master (AUD-13) |
| DQ-4 고유본 표기 | 예 | 부분(정렬 의미론은 명시 가능했음) | master (AUD-12) |
| DQ-5 old/ 등재 범위 | 예 | 아니오 | master (AUD-02 로 (i)·(ii) 까지 확장 결정) |
| DQ-6 (ix) 하위군 | 예 | 아니오 | master |
| DQ-7 png git 처리 | 예(사용자) | 아니오 | 사용자 |
| DQ-8 C3_pdf_render 보존 | 예(사용자) | 아니오 | 사용자 (실측 16,490,986 B = 15.7 MiB) |
| DQ-9 +1 파일 | 아니오 | **예**(mtime) | 닫힘(AUD-07) |
| DQ-10 comp_v24 비-md | 예 | 아니오 | master |
| DQ-11 skills SKILL.md | 아니오(군 밖 자명) | 예 | 닫힘(미등재 유지) |
| DQ-12 preamble 헤더 파일명 | 아니오(관찰 기록) | 예 | 등록부/GAP 단계로 이관만 |
| DQ-13 R2 +2·+3 등재 | 아니오(기본값 타당) | 예 | 닫힘(등재 유지) |
| DQ-14 tracked 여부 | 예(git) | 아니오 | master |
| DQ-15 스크립트 보존 | 예 | 아니오 | master (AUD-14 — 이미 복사됨) |

## 4. 독립 재측정 수치 표(R-a ~ R-i)

| # | 항목 | 작업 sub 값 | 본 sub 재측정 | 판정·명령 |
|---|---|---|---|---|
| R-a | `Claude/plans/*.md` | 93 / 10,384 | **93 / 10,384** · 마스터 플랜 812 · INDEX 69 · ROADMAP 320+131 | 일치. +1 원인 = 마스터 플랜(mtime 09:26:07, 1g 09:24 이후 유일 수정) — AUD-07. 1g 파일은 파일별 줄수 미기록(총계만) |
| R-b | `HANDOVER*.md` | 25/1,612 · 28/1,915 | **25/1,612 · 28/1,915** | 일치(`Get-ChildItem -Recurse -Filter 'HANDOVER*.md'`, old\ 제외/포함) |
| R-c | `docs/**/PLAN_*.md` · v1020 master | 15/645 · 207 | **15/645 · 207** | 일치 |
| R-d | `CLAUDE.md` | 88 | **88** (Raw LF 88 · CRLF 88 · 끝 개행 True · mtime 2026-07-26) | 일치. R3 89 = Read 도구 +1 표시(`wc -l` 도 88 이라 wc 가설 기각) · brief 90 = 오기(AUD-08) |
| R-e | 마스터 3본 `\input` | 33/12/10 · 고유 53 · orphan 3 | **33/12/10 · 고유 53 · `_sections` 56 · 미포함 = ch1_appD_si·ch1_preamble·ch2_preamble · 대상 없는 input 0 · 형태 전건 `\input{_sections/…}` · `\include`/`\subfile`/`\import` 0 · 중첩 0(v1.0.25.1 tex 90본 Grep 매치 55건 = 마스터 3본뿐)** | 일치 → MP 정정 후보(AUD-13) |
| R-f | §1 path 전건 | 611 · Test-Path 611/611 | **611행 · 고유 611 · Test-Path 611/611 · 줄수 재계수 불일치 0 · 군별 합계 18/18 헤더 일치 · 빈 셀 0** | 일치 |
| R-g | hash 중복 | 259 그룹 / 769 파일 | **재계산(2,654본 SHA256 = TSV 2,651 + 산출 3) 259 / 769 · TSV 대비 hash 변경 0 · 그룹별 구성원 수 259/259 일치 · 고유본 규칙 257/259(불일치 2 = 동명이물 정렬 의미론, AUD-12) · §1 중복 구성원 110행 표기 전건 정확 · 대표 그룹 HANDOVER_v24 ×4(C9B02096…)·V1022=V1023(A20E9740…) 재확인** | 일치 |
| R-h | untracked Claude 8 근거 | 8/8 | **png 5 = 223,035/281,441/223,076/281,771/223,131 B · mtime 09-02 16:47–16:49 · 스크립트 OUT 경로 `graph_suite_v1017.py:37`·`sample_test_v1017.py:12,28`·`graph_suite_v1018_1.py:37`·`sample_test_v1018_1.py:12,28`·`graph_suite_v1018_2.py:37` 실물 일치 · `V1017_EXECUTION_LEDGER.md:19`·`V1018_EXECUTION_LEDGER.md:31` 복제 기록 일치 · C3_graph_check 1파일 157,313 B(`V1010_INSPECT_draft_C3.md`:14,23 경로 일치) · C3_pdf_render 50(ch1 35 · ch2 13 · contact 2 · 16,490,986 B · 07-02 01:38–01:39; `:15` 35/13쪽 pdftoppm 일치) · regsol_test 2(575,913 B; `comp_v26_data/README.md`:31 폐기 일치)** | 일치(24 근거 전건) |
| R-i | §7 ⊆ | 131 등재 · 부재 0 | **R1~R7 Read Coverage 절 독립 추출 = 명시 76 + `_sections` 55(divider 제외) = 131 · §7 131 과 양방향 차집합 0 · 전건 §1 행에 존재 · Test-Path 131/131** | 일치 |
| 부가 | TSV | 2,651 | **2,651행 · 4열 전건 · 빈 행 0 · 줄수 합 715,118 → 미등재 622,113(=715,118−93,005) 재현 · `\Codex\` 0** | 일치 |
| 부가 | v1.0.25 tex | 60/9,207 · diff 6 | **60/9,207 · hash 동일 54 · 상이 6(마스터 3 + width·eqpeak·sifr)** | 일치 |
| 부가 | 산출 3본 | INV 1,463행·197,079 B·77C2BF6A… / TSV 414,664 B·E1A39374… | **동일(hash·바이트·행 수)** · work_log 131행 | 일치 |

## 5. Read Coverage(본 sub 가 실제 읽은 파일 · 행 범위 · 방식 — 표에 없으면 읽지 않은 것)

| # | 파일(`D:\Projects\Project_Anode_Fit\` 기준) | 행 범위 | 방식 | 비고 |
|---|---|---|---|---|
| 1 | `Claude/results/handoffs/v1027-phase-1.1-inventory/audit_checklist.md` | 1–66 전문 | Read | 지시 |
| 2 | `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md` | 1–133 전문(Read 표기 1–134) | Read | A-1 |
| 3 | `Claude/plans/2026-09-02-v2-master-plan.md` | 185–214 · 298–322 · 590–624 (Read) + Grep 매치 행 89·103·129·203·231·363·366·372·424 | Read(지정 범위)·Grep | A-2 · 그 밖 미검독 |
| 4 | `Claude/results/V1027_HISTORY_INVENTORY.md` | 1–250 · 251–500 · 501–750 · 751–1000 · 1001–1250 · 1251–1463 (6청크 전문) + PowerShell 전 행 파싱 | Read·PowerShell | A-3 |
| 5 | `…/iter_1/work_log.md` | 1–131 전문(Read 표기 1–132) | Read | A-4 |
| 6 | `…/iter_1/inventory_raw.tsv` | 전 행(파싱·집계·hash 대조) | PowerShell | A-5 |
| 7 | `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` · `ch2_lco_v1.0.24.tex` · `ch3_si_v1.0.24.tex` | 1–62 · 1–34 · 1–34 전문 | Read + PowerShell `\input` 추출 | A-6 |
| 8 | `…/wf/R1_…md` 170–209 · `R2_…md` 260–304 · `R3_…md` 356–400 · `R4a_…md` 320–364 · `R4b_…md` 393–432 · `R5_…md` 385–429 · `R6_…md` 374–418 · `R7_…md` 509–538 | Read Coverage 절 전문(각 파일 끝까지) + 직전 DQ 수 행 | Read(토픽 한정) | A-7 |
| 9 | `…/wf/go_1g_check_2026-09-03.txt` | 1–15 전문 | Read | A-8 |
| 10 | `Claude/results/comp_v26_data/README.md` | 20–35 | Read | R-h |
| 11 | `Claude/results/process/V1010_INSPECT_draft_C3.md` | 1–30 | Read | R-h(:14·15·23) |
| 12 | `Claude/plans/INDEX.md` | 1–69 전문 | Read | path:line 대조(:10–13·18·38·40·51·57) |
| 13 | `Claude/docs/INDEX.md` | 10–27 · 52–67 · 116–130 · 190–196 | Read(부분) | path:line 대조(:12·21·25·53·67·117·127·130·193) |
| 14 | `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | 30–35 · 82–94 | Read(부분) | :32·83·93 |
| 15 | `Claude/docs/v1.0.25.1/_sections/ch1_preamble.tex` · `ch2_preamble.tex` · `common_preamble_v1024.tex` | 각 1–6 + common Grep 33–41 | Read(부분)·Grep | orphan·박스 정의 근거 |
| 16 | `Claude/docs/v1.0.17/graph_suite_v1017.py` 35–38 · `sample_test_v1017.py` 10–29 · `docs/v1.0.18.1/graph_suite_v1018_1.py` 36–38 · `sample_test_v1018_1.py` 11–29 · `docs/v1.0.18.2/graph_suite_v1018_2.py` 36–38 | 부분 | Read | R-h OUT 경로 |
| 17 | `Claude/results/process/V1017_EXECUTION_LEDGER.md` 18–20 · `V1018_EXECUTION_LEDGER.md` 30–32 | 부분 | Read | R-h 복제 기록 |
| 18 | `Claude/old/v2/results/EXECUTION_LEDGER_v2.md` | 1–8 | Read | old/v2 계보 확인(AUD-02) |
| G1 | `Claude/docs/v1.0.25.1/**/*.tex` | 패턴 `^[^%]*\\(input\|include\|subfile\|import)\{` 매치 카운트만 | Grep | 55/3파일 |
| P1 | `Claude/plans/*.md` · `Claude/**/HANDOVER*.md` · `Claude/docs/**/PLAN_*.md` · 루트 `CLAUDE.md` · `Claude/jcp_extract.txt` · `build.log` · `summary_skew.json` · `CLOSING_v1.0.15.md` | 줄수·Raw 끝문자·mtime 만 | PowerShell | 내용 미열람 |
| P2 | brief §3.1 모집단 2,654본 | SHA256 재계산·줄수 재계수 | PowerShell | 내용 미열람 |
| P3 | 27종 파일명 패턴 · 9개 폴더 전건 | 존재·§1 소속 대조·줄수 | PowerShell | 내용 미열람 |
| D1 | untracked 8 실물 · `iter_1/gen_outinv.ps1` · 스크래치패드 동명 파일 | 존재·바이트·mtime·CreationTime·hash 만 | PowerShell | png·html·ps1 내용 미열람 |

미검독(명시): 위 표 밖 전부 — 등재 파일 본문(계획서·인계·ledger·Result·조사·tex 본문) · R1~R7 의 Read Coverage 절 이외 영역 · 마스터 플랜 지정 범위 밖 · png/pdf/html · `Codex/` 전체(0회).

## 6. 판정

**확정결함 1건(AUD-01) → "master 직접 수정 가능"** (재작업 불요 — 행 11 추가 + §2·§8.3 갱신으로 닫힘). 경미 8건은 전부 국소 문구·1행 수정, 제안 6건 중 AUD-13 은 마스터 플랜 Correction History 소관.

빈 통과 방지 정량: 본 라운드가 재검증한 범위 = §1 611행 전건(Test-Path·줄수·빈 셀·어휘) · §4 259그룹 전건(구성원 수·고유본 규칙) + §1 중복 구성원 110행 표기 · §7 131건 양방향 · path:line 근거 24건 실물 · 파일명 패턴 27종 + 폴더 9개 소속 대조 · TSV 2,651행 형식·합계 · 모집단 2,654본 SHA256 재계산 · 마스터 tex 3본 `\input` 55건 · untracked 8 실물 · 산출 3본 hash. 이 범위에서 작업 sub 의 **수치 오류는 0** 이었고, 발견은 전부 등재 범위(정책 일관성)·명시(부재·어휘·닫을 수 있었던 미검증)에 관한 것이다. 2R 는 master 가 AUD-01~07·10·11 반영본에 대해 완결성·usable 렌즈로 재검수하면 수렴 판정이 가능하다.
