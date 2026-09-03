# audit_log_r2 — Phase 1.1 Step 1 OUT-INV 검수 · 라운드 2 (iter_2 · 2026-09-03)

> 검수 sub(Fable 5.1, 라운드 1 과 동일 sub) → master. 지시 = `Claude/results/handoffs/v1027-phase-1.1-inventory/audit_checklist_r2.md`(전문 정독 L1–25). 대상 = iter_2 OUT-INV(`Claude/results/V1027_HISTORY_INVENTORY.md` — 실측 1,566행 · 209,806 B · SHA256 0E1E3C41E796E3F0… · mtime 10:46:06) + 마스터 플랜 v5.3(`Claude/plans/2026-09-02-v2-master-plan.md` — 813행 · SHA256 CF078C0D78937F05… · mtime 10:46:06). 불변 확인: TSV(E1A39374… · 09:34:39) · `iter_1/work_log.md`(E8428D27… · 131행) 무변경. 본 sub 의 파일 생성 = 본 audit_log_r2 1본(폴더 `iter_2/` 신설)뿐 · 기존 파일 무변경 · git 명령 0회 · `Codex/` 접근 0회. 라운드 1 문맥의 사본에 의존하지 않고 현재 파일을 다시 읽었다(§6).

## 0. 헤더 — 라운드·렌즈·청크 경계

| 항목 | 값 |
|---|---|
| 라운드 | 2 (통상 산출물 등급 — 연속 2R 확정결함 0 수렴 조건 중 2R 차) |
| 렌즈 | regression(master 변경 지점·계획서 정정 누락 grep) · 완결성(추가 26본 TSV 대조·§2·§8.3 산식·정책 (a)(b)(c) 잔여 전건 대조) · usable(파싱·귀속 이표기) · 구조(§10 처분표·라운드 1 반영 대조) — 라운드 1(구조·적대검산·완결성·usable)과 스킴 전환 |
| OUT-INV 절 경계 청크(라운드 1 의 250행 기계 분할과 다르게 헤더 실측 행으로 7분할) | ① §0~(i-b) = L1–155 ② (ii)~(iv-b) = L156–254 ③ (v)~(viii-b) = L255–559 ④ (ix)~(xix) = L560–871 ⑤ §2~§4 = L872–1216 ⑥ §5~§7 = L1217–1417 ⑦ §8~§10 = L1418–1566 (③·④·⑤ 는 305·312·345행으로 "≤~300" 을 조금 넘는다 — 절 경계를 깨지 않기 위해 그대로 둠) |
| 실제 Read 창(토큰 상한 25k 로 인해 ≤250행) | 1–250 · 251–500 · 501–750 · 751–1000 · 1001–1125 · 1126–1250 · 1251–1500 · 1501–1566 — 8창이 ①~⑦ 전 영역을 겹침·누락 없이 덮음(①=창1 · ②=창1–2 · ③=창2–3 · ④=창3–4 · ⑤=창4–6 · ⑥=창6–7 · ⑦=창7–8) |
| 계획서 | v5.3 정정 지점(§2.0 A1 L43 · §2.2 L90–91·L103 · §2.6 L153 · §2.9 L195·197·203 · Phase Range 2.1 L231 · 2.1 Step 14 L363 · 2.2 L372·L380 · 2.7 L424 · T-4 L572 · T-15 L583 · Assumptions 12 L608 · Correction History v5.3 L633) 전건 Read + 잔존 패턴 Grep 전문 · 그 밖은 라운드 1 지정 범위 밖 미검독 |

## 1. 발견 표

4-tier = 확정(재계산·재대조 실물) / 근거 미발견 / 추정 / 미검증. 약칭: INV = OUT-INV iter_2 · MP = 마스터 플랜 v5.3 · 줄수 = `(Get-Content).Count`(TSV 정의).

| ID | 심각도 | 4-tier | 위치 | 내용 | 재현 근거(명령·수치) | 수정 제안(한 줄) |
|---|---|---|---|---|---|---|
| AUD-R2-01 | **확정결함** | 확정 | INV (iv-b) 정의 L237 · (ix) 행 86 L653 · (viii-b) 행 2 L558 · (iv-b) 행 10 L251 · MP §2.8 L184 · 프로젝트 `CLAUDE.md`:14–15 | **master 가 §10 에서 명문화한 「추가 발견」 정책 (a)(b)(c) 를 가장 좁게 읽어도 아직 빠진 파일이 19본·4,555줄이다.** (a) 형제(같은 계열 파일명): (ix) 행 86 `V1010_INSPECT_draft_C3.md` 가 등재됐으나 **같은 파일명 계열** `results/process/V1010_INSPECT_draft_{C1,C2,O1,O2,O3,S1,S2,S3}.md`(105·89·96·98·113·209·265·320) + `V1010_INSPECT_UNION.md`(55) + `V1010_INSPECT_verify10.md`(31) = **10본·1,381줄** 미등재. (c) 동명 폴더: (iv-b) 행 10 이 `docs/v1.0.23/results/comp_v23/COND_AUDIT.md` 를 동명 폴더 충돌로 등재했으나 같은 폴더의 `AUD_REPORT_v23.md`(65) 미등재(폴더 내 md 2본 중 1본만 적용). (b) 통제 문서 인용: MP §2.8 L184 가 `old\Archive_oldtrack\(… · COMPARISON_*/REVIEW_LEDGER_*[동명이물])` 로 명시 인용하는 `COMPARISON_CLAUDE_*.md` **6본·640줄**(93·123·124·74·77·149 — 등재된 `REVIEW_LEDGER_*` 와 같은 폴더의 형제이기도 함) 미등재; 프로젝트 `CLAUDE.md`:14–15 (P1) 가 프로젝트 목표의 기준 원문으로 인용하는 `graphite_ica_charge_balance_ver1_rechecked2.tex`(495)·`graphite_ica_dynamic_ver5.tex`(1,974) 는 실물이 `old/_archive/Archive_old/` 에 존재(CLAUDE.md 의 `Claude/docs/` 경로는 스테일)하는데 미등재 — (xvii) 유실 원문 5본과 같은 성격의 구트랙 원문 **2본·2,469줄**. 합 = 10 + 1 + 6 + 2 = 19본. 결과적으로 r2 지침 §1 완결성 게이트 "통제 문서가 인용하는 파일 중 OUT-INV 밖 = 0" 이 성립하지 않는다. | `Get-ChildItem results\process -Filter 'V1010_*INSPECT*'` → 22본 중 §1 등재 1(C3)·미등재 21(그중 `V1010_INSPECT_*` 계열 10, `V1010_HANDOVER_INSPECT_*` 11 — 후자는 AUD-R2-02 후보 풀) · `docs\v1.0.23\results\comp_v23\` = AUD_REPORT_v23.md[65]·COND_AUDIT.md[301]·p1_ratio_check.py[68] · `Get-ChildItem old\Archive_oldtrack -Filter 'COMPARISON*'` → 6본 · `Get-ChildItem Claude -Recurse \| ? Name -match 'dynamic_ver5\|charge_balance_ver1'` → `old\_archive\Archive_old\` 2본 · 전건 §1 행 집합(637) 미포함 확인(본 sub 스크립트) | (ix) 또는 (iv-b) 에 `V1010_INSPECT_*` 10본 "추가 발견(a)" · (iv-b) 에 `AUD_REPORT_v23` "(c)" · (iv-b)/(vii) 에 `COMPARISON_*` 6본 "(b) MP §2.8 인용 · (a) REVIEW_LEDGER 형제" · (xvii-b) 신설로 구트랙 원문 2본 "(b) CLAUDE.md P1 인용 · 경로 스테일 관찰" 등재 → §2 합계 710/102,233 · §8.3 갱신. master 직접 수정 가능(행 19 추가). |
| AUD-R2-02 | 경미 | 확정(후보 실물) · 정책 해석은 master 결정 | INV (iv-b) 정의 L237 · (iv-b) 행 7 L248 | **정책 (a) "형제(같은 계열 파일명)" 의 단위가 정의돼 있지 않아**(파일명 계열 단위 vs 버전 접두 단위) 적용 결과가 자기모순이다: master 는 `V1014_AUDIT_ADJUDICATION.md` 를 `V1014_TONE_AUDIT` 의 형제로 등재(접두 `V1014_` 단위)했으나, 같은 접두 단위로는 `V1014_REVIEW_R1_A~R7_B.md` 20본(2,071줄)·`V1013_REVIEW_R1~R10_{A,B,C}.md` 30본(4,095줄)+`V1013_CODE_MAP_ADDENDUM_R10.md`(176)·`V1012_P43_review_*` 11본+`V1012_P42b_fixer_note`(1,344)·`V1010_P1~P5_review1.md` 5본(210)·`V1010_HANDOVER_INSPECT_*` 11본(1,062)·`V1010_LCO_STYLE_REPORT`(29)·`V1015_P2_PHYSICS_REVIEW`(59)·`V1017_REVIEW_COMPLETE`(60)·`V1019_FINAL_REVIEW_UNION`(53) 이 전부 형제가 된다(합 ≈ 82본·9,159줄). 계열 단위로 읽으면 AUD-R2-01 의 10본만 남는다. 어느 쪽이든 현재 표는 두 해석을 섞어 쓰고 있다. 마찬가지로 (b) "통제 문서(… INDEX)가 인용하는 파일" 을 문면대로 적용하면 `docs/INDEX.md` 가 인용하는 실물 중 §1 밖이 **54본**(md 12 = `FITTING_GUIDE.md` ×8·`R1B_SWEEP_LIST`·`MISSING_CONTENT_REVIEW`·`V1017_FIXLIST_CONSOLIDATED`·`V1017_REVIEW_COMPLETE` · tex 27 · py 15), `INDEX_v25.md` 인용 중 12본(가이드 2·py 9·json 1), MP 인용 중 9본(`docs/v1.0.25.1/FITTING_GUIDE.md`·`results/research/broadening_w_design.md`·py 6·tex 1)이라 §8.3 계수 방침(가이드·코드·tex 본문 미등재)과 충돌한다 — (b) 에 "이력·결정 근거 md(가이드·코드·tex 본문·PDF 제외)" 류 한정어가 필요하다. | 통제 문서 5본(`CLAUDE.md`·MP·`docs/INDEX.md`·`plans/INDEX.md`·`INDEX_v25.md`)에서 확장자 토큰 정규식 추출 → TSV 실물 해소 → §1 집합 대조(본 sub 스크립트): CLAUDE.md 해소 1/미해소 7(스테일 경로 2·Codex 2·패턴 3) · MP 112 해소/9 밖 · docs/INDEX 97/54 · plans/INDEX 26/0 · INDEX_v25 57/12. `results/process` REVIEW·NOTE 계열 미등재 md 전건 목록·줄수 = 본 sub 스크립트 출력(§6 P3). | §10 정책 문안을 "(a) = **파일명 계열**(접두+계열어, 예 `V1010_INSPECT_draft_*`) · (b) = 통제 문서가 **이력·결정 근거로** 인용하는 md/tex 원문(가이드·코드·PDF·현행 tex 본문 제외) · (c) = 동명 폴더 안 md 전건" 으로 확정하고, 접두 단위 후보 풀(위 ≈82본)은 DQ 로 1.2 토픽 한정 열람 대상에 남길지 결정. |
| AUD-R2-03 | 경미(iter_2 회귀) | 확정 | INV (i-b) 행 12 L154 · (i-b) 정의 L138 | `Claude/old/Archive_oldtrack/RB_AL_MASTER.md`(139) 를 문서 종류 **마스터플랜**·군 (i-b) 계획서로 등재했으나 실물 헤더 L1 = "RB_AL_MASTER — **통합 Assumption Ledger + Notation Bible + 가독 Gate**(Phase 0.3, step 13–16)", L3 "입력: `RB_CHARTER.md`(규약)" — 계획서가 아니라 구트랙 ledger·규약 문서다. (i-b) 정의 L138 이 glob `*MASTER*` 오매치 3본(`10_sources_master`·`V2_citations_master`)은 "마스터플랜이 아니므로 등재하지 않는다" 고 했으면서 같은 오매치인 이 파일만 마스터플랜으로 올려 정의와 자기모순. 라운드 1 AUD-02 가 "구트랙 마스터 3" 으로 묶은 것을 master 가 실물 확인 없이 전사한 회귀. | `RB_AL_MASTER.md`:1–5 Read. | 행을 (vii) 로 이동(종류 ledger · 비고 "구트랙 통합 Assumption Ledger · glob `*MASTER*` 오매치") 또는 (i-b) 비고에 종류 정정; §2 (i-b) 12→11 · (vii) 81→82. |
| AUD-R2-04 | 경미(iter_2 회귀) | 확정 | INV (i) 행 79 L121 · (vii) 행 74 L365 · (i-b) 행 10–11 L152–153 · (vii) 행 51 L342 · (viii) 행 73–86 L454–467 | AUD-05·AUD-11 반영이 **새 이표기 2쌍**을 들였다: ① `v1.0.18.1·v1.0.18.2(공통 — 추정)`(행 79) vs `v1.0.18.1·v1.0.18.2(공통 — :30–31 두 개정 한 원장, 추정)`(행 74) — 같은 귀속을 두 문자열로 · ② `구트랙 RB(rebuild v2 — Fable v2 와 동명이물)`(old/v2/plans 2행) vs 같은 `old/v2/` 트리의 `old/v2/results/*` 15행은 `구트랙 RB`(무한정) — 동명이물 경고가 폴더의 일부 행에만 붙어 Step 2 계보 정렬 키가 갈린다. 버전 귀속 값 집합 71 → **66종**(AUD-11 통일 3쌍 성공: `v10 rework`·`v9 2track`·`v1.0.12(fable reaudit)` 각 1종) 이나 위 2쌍이 새로 생김. | §1 637행 버전 귀속 값 전수 집계(본 sub 스크립트) → 66종 · 위 값별 행 수 1/1 · 2/15. | ① 행 74 를 행 79 와 동일 문자열로 통일(근거 `:30–31` 은 비고로) ② `old/v2/**` 17행 전건에 같은 한정어 부여(또는 비고로 이동). |
| AUD-R2-05 | 경미 | 확정 | MP §2.8 L164 · L169 · L177 · Assumptions 11 L607 · L203 우측 열 · L231 · L366 | v5.3 정정이 **§2.8 구조 맵과 Assumptions 11 을 건너뛰어** 같은 사실의 구판 수치가 남았다: L164 "`CLAUDE.md` … (89행; brief 표기 90)" ← 정본 88(§2.0 A1 L43 은 정정됨) · L169 "`_sections\(56, ch1_appD_si.tex = orphan)`" ← orphan 3(L90 은 정정됨) · L177 "`plans\ INDEX.md(65, 스테일) + 91 계획서(9503줄)`" ← 69 · 93/10,384(L195·L608 은 정정됨) · L607 "plans 91(9503줄) … INDEX 401 … 9,567+1,612+885+106+401 = 12,571" ← 93/10,384 · INDEX 403(196+69+138) — 규모 근거식이 구판. 또 "지원 4본" 표현이 L203 우측 열("위 지원 4본 + 마스터 3본 전문")·L231("마스터 3본 + 지원 4본 전문 정독")·L366("마스터 3본·지원 4본 정독 행 범위")에 남아 L363·L372·L424 의 정정 표현 "지원·orphan 4본" 과 혼재(의미는 같으나 2본이 orphan 임을 잃음). | Grep(패턴별 히트 = §4 표) + L158–237·L598–613 Read. v5.3 행 L633 은 정정 대상으로 "§2.2·§2.6·§2.9·Phase Range 2.1·2.1 Step 14·2.2·2.7·T-4·T-15" 만 열거 — §2.8·Assumptions 11 미포함(누락의 원인). | v5.4(또는 v5.3 Correction History 추기)로 §2.8 3곳·Assumptions 11·"지원 4본" 3곳 정정. |
| AUD-R2-06 | 경미 | 확정(실물) · 기록 의도는 미검증 | INV §10.1 행 09 L1533 · 행 14 L1538 | §10.1 이 AUD-09 처리를 "정정은 본 문건·**Step 1 이력**" 로, AUD-14 를 "보존 사본 … — **Step 1 이력 기록**" 으로 적었으나 `Claude/results/Step 1 — 인벤토리 파일 생성(OUT-INV).md` 는 35행·mtime 09:33:28 로 TSV(09:34:39) 이전부터 무변경 — 두 기록이 아직 실물에 없다. Step 1 종료 시 쓸 예정이라면 §10.1 문구가 시제를 앞질렀다. | `Get-Item 'results\Step 1 — 인벤토리 파일 생성(OUT-INV).md'` → 35행 · 09-03 09:33:28 · `results/` 상위에서 10:00 이후 변경 파일 = OUT-INV 1본뿐. | Step 1 이력에 build.log R2 표기·gen_outinv.ps1 복사(10:16:52)·iter_2 반영을 기록하거나 §10.1 문구를 "기록 예정" 으로. |
| AUD-R2-07 | 제안 | 확정 | INV L3 · (i) 행 90 L132 · §3.1 L910–911 | ① L3 "통제 문서 = …(v5.2)" 와 (i) 행 90 비고 "본 arc 통제 문서(v5.2)" — 현재 v5.3(813행). TSV 시점(09:34) 값으로는 맞지만 통제 문서 참조 라벨로는 스테일. ② §3.1 정본 93/10,384 는 TSV 스냅샷 정의로 유지되는 것이 옳으나, v5.3 행 추가로 살아 있는 plans 합계는 10,385(813)임을 §3.1 에 한 줄 주석 권고. ③ §3.1 row 2 가 새로 적은 "9,567 + 811 + 4 = 10,382 vs 1g 10,383(차 1 … 파일 미특정)" 은 정직한 표기이나 master 9,567 의 측정 시각(`plans/INDEX.md` 69행 갱신 08:48:05 이전인지)이 기록되면 차 1 이 닫힌다(08:48 이전 측정이면 INDEX 65 포함 → +4 가산이 맞고 잔여 1 은 다른 파일; 이후면 +4 가산이 중복). | MP 813행·mtime 10:46:06 · INDEX.md mtime 08:48:05. | 라벨 v5.3 갱신 + 살아 있는 합계 주석 + 9,567 측정 시각 기록. |
| AUD-R2-08 | 제안 | 확정 | INV §8.3 L1434–1484 | §8.3 폴더별 표를 iter_1 값으로 두고 이동분 7행을 산문으로만 적었다(1,960·617,440 산식은 재현 ✓ = 2,651−691 · 715,118−97,678). 표 7행(`old/plans` 9→0 · `old/v2` 20→18 · `Archive_oldtrack` 14→13 · `old/results` 8→6 · `results/process` 424→415 · `docs/v1.0.10` 13→11 · `docs/v1.0.23` 68→67)을 갱신하면 표만으로 재현 가능. | 이동분 26본 = 9+2+1+2+9+2+1 · 줄수 2,212+548+139+588+785+100+301 = 4,673 ✓. | 표 7행 갱신. |
| AUD-R2-09 | 제안 | 확정 | 프로젝트 `CLAUDE.md`:14–15 · MP DR-13 | `CLAUDE.md` P1 이 인용하는 경로 `Claude/docs/graphite_ica_dynamic_ver5.tex`·`Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` 는 실물이 `Claude/old/_archive/Archive_old/` 로 이동돼 있다(존재 2/2, 인용 경로 0/2). DR-13(CLAUDE.md 스테일) 항목에 경로 정정 후보로 추가 권고. `Codex/AGENTS.md`·`Codex/plans/…guide.md` 인용은 무접근이라 미검증. | `Get-ChildItem Claude -Recurse \| ? Name -match 'dynamic_ver5\|charge_balance_ver1'` → `old\_archive\Archive_old\` 2본. | DR-13 후보 등재(OUT-CLAUDEMD). |
| AUD-R2-10 | 제안 | 확정(실물) · 편입 여부는 master | INV §8.3 · (vii) 행 51 L342 · (i-b) 행 12 | 등재된 구트랙 ledger 가 **binding 으로 인용**하는 문서가 미등재: `old/v2/results/EXECUTION_LEDGER_v2.md`:4 "Charter binding: `CHARTER_v2.md`"(385) · `RB_AL_MASTER.md`:3 "입력: `RB_CHARTER.md`"(105) · `CHARTER_v3.md`(65) — 1.3(유효 결정·제약 등록부)의 구트랙 원천. 또 `results/research/radius/{BAND,ORIGIN,RADIUS}_VERDICT.md`(69·79·83)·`50_report.md` ×2 는 등재 `RADIUS_LEDGER`·`PHASE_RADIUS_RESULT` 의 형제이며 `V1010_INSPECT_draft_C3.md`:16 이 인용. (a)(b) 문면 밖이라 결함으로 세지 않음. | `EXECUTION_LEDGER_v2.md`:1–7 · `RB_AL_MASTER.md`:1–5 · `V1010_INSPECT_draft_C3.md`:16 Read · 줄수 스크립트. | DQ 로 1.3·1.4 토픽 한정 원천 후보 등재. |

발견 합계: **확정결함 1(AUD-R2-01) · 경미 5(AUD-R2-02~06) · 제안 4(AUD-R2-07~10)**.

## 2. 라운드 1 발견 15건 반영 대조

| AUD | 라운드 1 심각도 | iter_2 반영 위치(실물 확인) | 반영 | 잔존 |
|---|---|---|---|---|
| 01 | 확정결함 | (iv-b) 12행 L235–253 · (viii-b) 2행 L550–558 · §2 L894–898 · §8.3 L1434 | O | 정책 (a)(b)(c) 잔여 → AUD-R2-01·02 |
| 02 | 경미 | (i-b) 12행 L136–154 · 오매치 3본 미등재 명기 L138 | O | 행 12 종류 오분류 → AUD-R2-03 |
| 03 | 경미 | (iv-b) 행 10 L251 동명 폴더 경고 | O | 같은 폴더 `AUD_REPORT_v23` 미등재 → AUD-R2-01 (c) |
| 04 | 경미 | §8.1 L1423 · MP L197 | O | 없음 |
| 05 | 경미 | (i) 행 79 L121 · (vii) 행 74 L365 | O | 두 표기 불일치 → AUD-R2-04 ① |
| 06 | 경미 | (x) 행 1 L665 · §3.5 L941 | O | 없음 |
| 07 | 경미 | §3.1 L910 (master git 811→812) · §10.2 DQ-9 닫힘 | O | §3.1 row 2 "차 1 미특정" 신규 → AUD-R2-07 ③(제안) |
| 08 | 제안 | §3.4 L931 · MP L43 | O | MP §2.8 L164 잔존 → AUD-R2-05 |
| 09 | 제안 | (xi) 행 8 L683 | O | Step 1 이력 미기록 → AUD-R2-06 |
| 10 | 경미 | §0 L29 · (vii) 행 81 L372 | O | 없음 |
| 11 | 경미 | 세부 표기 통일 3쌍(66종) · DQ-1 §10.1 L1535 | O | 신규 이표기 2쌍 → AUD-R2-04 |
| 12 | 제안 | §4 규칙 L951 · #179 L1135 · #239 L1195 · (vii) 행 39/41 L330·L332 | O | 없음(본 sub 재확인: 고유본 = `REVIEW_LEDGER_CH2_10ROUND.md`·`graphite_ica_chapter2.tex`) |
| 13 | 제안(계획서) | MP L43·90·91·103·153·195·197·203·231·363·372·380·424·572·583·608·633 | O | §2.8 3곳·Assumptions 11·"지원 4본" 3곳 → AUD-R2-05 |
| 14 | 제안 | §10.1 행 14 L1538 · §10.2 DQ-15 L1559 | O | Step 1 이력 미기록 → AUD-R2-06 |
| 15 | 제안 | §0 L30 태그 경계 1구 | O | 없음 |

반영 15/15 · 잔존 있는 항목 8(01·02·03·05·07·08·09·11·13·14 중 실질 잔존 = 01·02·03·05·08/13·09/14·11).

## 3. 계획서 잔존 grep(v5.3 · 813행)

| 패턴 | 히트 | 행 · 판정 |
|---|---|---|
| `빌드 58` · `58 \+` · `포함 58` · `58/2` | 0 | 잔존 없음 |
| `\b332\b` | 1 | L372 — 정정 문맥("R4a 표기 합 332 는 Read 도구 +1 표기") ✓ |
| `8,882` · `8882` | 1 | L380 — 정정 문맥("R4a/R4b 표기 합 8,882") ✓ |
| `orphan 1\b` · `미포함 2\b` | 0 | 문자열 잔존 없음 — 단 **L169** "`_sections\(56, ch1_appD_si.tex = orphan)`" 은 orphan 1 을 함의(AUD-R2-05) |
| `90\(R3` · `R3 실측 89` | 1 | L43 — 정정 문맥 ✓ · **L164** "(89행; brief 표기 90)" 은 별 패턴으로 잔존(AUD-R2-05) |
| `지원 4본` | 3 | L203(우측 열)·L231·L366 — 구 표현 잔존(L363·372·424 는 "지원·orphan 4본" 으로 정정됨) |
| `ch1_preamble\.tex`:31` | 1 | L103 — 정정 문맥("orphan 잔재") ✓ |
| `91 계획서\(9503줄\)` · `plans 91\(9503줄\)` | 2 | **L177 · L607** 잔존(AUD-R2-05) |
| `INDEX\.md\(65` | 1 | **L177** 잔존(실측 69) |
| `v5\.3` | 17 | L43·90·91·103·153·195·197·203·231·363·372·380·424·572·583·608·633 — 정정 표식(전건 Read 로 문면 확인: 실물과 일치 · 표 서식 열 수·구분선 깨짐 0) |

## 4. 완결성·usable 재측정(iter_2 추가분·합계)

| 항목 | iter_2 값 | 본 sub 재측정 | 판정 |
|---|---|---|---|
| §1 데이터 행 | 637 | 637 · 고유 637 · Test-Path 637/637 · 줄수 재계수 불일치 1 = `plans/2026-09-02-v2-master-plan.md` INV 812(TSV) vs 실물 813(v5.3 행 추가 — TSV 정의상 정상) · 빈 셀 0 | 일치 |
| 추가 26본 | (i-b) 12/2,899 · (iv-b) 12/1,674 · (viii-b) 2/100 | 전건 TSV 존재 · 줄수 TSV 값과 26/26 일치 · 군 합계 = 헤더 3/3 | 일치 |
| §2 합계 | 691 / 97,678 | 행 합 89,369 − (xviii) 행 898 + (xviii) 60본 9,207 = 97,678 · 665+26 = 691 · 93,005+4,673 = 97,678 | 일치 |
| §8.3 산식 | 1,960 · 617,440 | 2,651−691 = 1,960 · TSV 총합 715,118−97,678 = 617,440 | 일치 |
| 정책 (a)(b)(c) 잔여 | 0(암묵) | **≥19본(최협의) — AUD-R2-01** · 정의 확정 시 ≤ +82본(AUD-R2-02) | **불일치** |
| 통제 문서 인용 ⊆ | (미기재) | CLAUDE.md 인용 2 스테일 경로(실물 old/) · MP 9 밖(가이드 1·조사 1·py 6·구트랙 tex 1) · docs/INDEX 54 밖 · plans/INDEX 0 · INDEX_v25 12 밖 | (b) 정의 의존 — AUD-R2-02 |
| 버전 귀속 값 집합 | 71 → ? | **66종** · 신규 이표기 2쌍(AUD-R2-04) · 어휘 밖 값 0(`v1.0.18` 해소) | 부분 |
| 문서 종류 값 집합 | — | 28종(신규 `Result(점검 보고)` 1) · 전건 토큰+괄호 규칙 안 | 통과 |
| 고유본/사본 파싱 | — | §4 #179·#239 교체 ✓ · (vii) 행 39/41 표기 교체 ✓ · 정규식 `사본\(고유본 = ` / `고유본\(사본 n:` 파싱 가능 | 통과 |
| §10 처분표 | DQ 1~15 · AUD 01~15 | 15/15 · 15/15 존재 | 통과 |
| Codex 경로 | 무접근 | INV 17행 전부 전사·선언(측정치 0) · TSV `\Codex\` 0 | 통과 |

## 5. 최약점 1곳

**AUD-R2-01/02 — 「추가 발견」 정책이 문장으로만 명문화되고 기계 적용되지 않은 것.** 라운드 1 최약점(정책 비일관)을 master 가 (a)(b)(c) 로 답했으나, 그 정책을 파일 시스템에 한 번 돌려 보지 않아 정책이 등재한 바로 그 파일(`V1010_INSPECT_draft_C3`)의 형제 10본, 정책이 등재한 동명 폴더의 나머지 md, 통제 문서 §2.8 이 이름으로 부르는 `COMPARISON_*` 6본, 그리고 프로젝트 헌법 P1 이 "기준" 으로 지목한 구트랙 원문 2본이 다시 표 밖에 남았다. 정독 모집단의 새는 지점이 라운드 1 과 같은 종류이므로, 표 행 추가보다 **정책 문안의 단위 정의(계열/접두·인용 범위)를 확정하고 스크립트로 잔여 0 을 증명**하는 쪽이 수렴에 필요하다.

## 6. Read Coverage(본 sub 가 실제 읽은 파일 · 행 범위 · 방식 — 표에 없으면 읽지 않은 것)

| # | 파일(`D:\Projects\Project_Anode_Fit\` 기준) | 행 범위 | 방식 | 비고 |
|---|---|---|---|---|
| 1 | `Claude/results/handoffs/v1027-phase-1.1-inventory/audit_checklist_r2.md` | 1–25 전문 | Read | 지시 |
| 2 | `Claude/results/V1027_HISTORY_INVENTORY.md`(iter_2 · 1,566행) | 1–250 · 251–500 · 501–750 · 751–1000 · 1001–1125 · 1126–1250 · 1251–1500 · 1501–1566(8창 = 절 청크 ①~⑦ 전 영역) + PowerShell 전 행 파싱(헤더 행·§1 행·어휘·스테일 수치) | Read·PowerShell | 대상 |
| 3 | `Claude/plans/2026-09-02-v2-master-plan.md`(v5.3 · 813행) | 37–112 · 148–156 · 158–237 · 303–316 · 356–429 · 488–495 · 566–587 · 598–613 · 622–643 (Read) + Grep 잔존 패턴(§3 표 — 매치 행만) | Read(지정 범위)·Grep | 그 밖 미검독(라운드 1 지정 범위 밖) |
| 4 | `CLAUDE.md`(루트) | 1–88 전문(Read 표기 1–89) | Read | (b) 인용 대조 |
| 5 | `Claude/old/Archive_oldtrack/RB_AL_MASTER.md` | 1–8 | Read | AUD-R2-03 |
| 6 | `…/iter_1/inventory_raw.tsv` | 전 행(파싱·basename 맵·합계) | PowerShell | 불변 hash 확인 |
| P1 | 파일명 패턴 31종(`HANDOVER*`·`*LEDGER*`·`*RESULT*`·`*REPORT*`·`*AUDIT*`·`*MASTER*`·`*ROADMAP*`·`*INSPECT*`·`*REVIEW*`·`*NOTE*`·`*CHARTER*`·`*VERDICT*` 등) · `results/process`·`old/**` REVIEW/NOTE/CHARTER md · `docs/v1.0.23/results/comp_v23/` · `old/Archive_oldtrack/COMPARISON*` · `old/_archive/Archive_old/` 2 tex | 존재·§1 소속·줄수만 | PowerShell | 내용 미열람 |
| P2 | 통제 문서 5본(`CLAUDE.md`·MP·`docs/INDEX.md`·`plans/INDEX.md`·`INDEX_v25.md`) | 확장자 토큰 정규식 추출 → TSV 실물 해소 → §1 대조 | PowerShell | `docs/INDEX.md`·`plans/INDEX.md`·`INDEX_v25.md` 본문은 토큰 추출만(정독 아님) |
| P3 | `results/Step 1 — 인벤토리 파일 생성(OUT-INV).md` · `iter_1/work_log.md` · `iter_1/gen_outinv.ps1` · `iter_2/` 폴더 | 줄수·mtime·hash 만 | PowerShell | 내용 미열람 |

미검독(명시): 위 표 밖 전부 — 등재·후보 파일 본문(`V1010_INSPECT_*`·`COMPARISON_*`·구트랙 tex 2본·REVIEW 계열 등은 줄수만) · R1~R7 본문 · MP 지정 범위 밖 · png/pdf/html · `Codex/` 전체(0회).

## 7. 판정

**확정결함 1건(AUD-R2-01) → "master 수정 필요"** — 연속 2R 확정결함 0 조건 미충족(라운드 2 는 수렴 계수 0R). 수정 범위는 국소적이다: (a)(b)(c) 정의 문안 확정(AUD-R2-02) → 그 정의로 잔여 파일 스크립트 산출 → 최소 19행 추가(AUD-R2-01) + (i-b) 행 12 종류 정정(AUD-R2-03) + 귀속 이표기 2쌍 통일(AUD-R2-04) + MP §2.8·Assumptions 11·"지원 4본" 정정(AUD-R2-05) + Step 1 이력 기록(AUD-R2-06). 라운드 3 는 완결성(정의 적용 후 잔여 0 스크립트 재현)·regression 두 렌즈로 좁혀 돌리면 된다.

빈 통과 방지 정량: 본 라운드 재검증 범위 = §1 637행 전건(Test-Path·줄수·빈 셀·어휘 집합) · 추가 26본 TSV 대조 · §2·§8.3 산식 · §4 교체 2행 + (vii) 2행 · §10 표 30행 · v5.3 정정 지점 17곳 문면 Read · 계획서 잔존 패턴 11종 Grep · 파일명 패턴 31종 + 폴더 5개 실물 대조 · 통제 문서 5본 인용 토큰 407건 해소·대조 · 산출 4본 hash/mtime. 이 범위에서 master 의 iter_2 **수치 변경은 전건 재현**됐고, 결함은 정책 적용 범위·분류·문구 잔존에 관한 것이다.
