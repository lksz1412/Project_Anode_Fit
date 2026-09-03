# Step 1 — 인벤토리 파일 생성(OUT-INV)

- **arc**: v1.0.27(마스터 플랜 `Claude/plans/2026-09-02-v2-master-plan.md` — 착수 시 v5.2, Step 중 사실 정정 v5.3·v5.4 · 실행 기준 정본)
- **작업 챕터 / Phase**: 1 이력 통합 / **1.1 인벤토리·정독 배정**
- **cumulative step**: 1(본 arc 첫 Step — 2.7 좌표대로 1 부터 단조 누적)
- **상태**: 진행 중(2026-09-03) — 작업 sub 산출(iter_1) → 검수 R1(확정결함 1) → master iter_2 → 검수 R2(확정결함 1) → master iter_3·3b → **검수 R3 대기**(연속 2R 확정결함 0 수렴 필요)
- **모델·유닛**: master Fable 5.1 · 작업 sub Fable 5.1 · 검수 sub Fable 5.1(R1·R2 동일 sub, 문맥 유지) · 직렬(동시 산 서브 ≤1)

## [Phase 1.1 착수 — 마스터 플랜 재독]

- 2026-09-03, master 가 `Claude/plans/2026-09-02-v2-master-plan.md` **본문 전문(1–813행, v5.2)** 을 Read 로 재독했다 — 8구간(1–108 · 109–216 · 217–324 · 325–432 · 433–540 · 541–648 · 649–756 · 757–813) 합쳐 전 영역 cover. 요약·기억으로 대체하지 않았다.
- 재독으로 고정한 Step 1 규칙(계획서 L303–316): 인벤토리 군 (i)~(xvi) 전건 = path + 줄수 + 버전 귀속 + 문서 종류 + 판독 정독 여부(R#) · 재현 가능 명령(`Get-ChildItem -Recurse` 줄수 · `Get-FileHash SHA256` 사본 판정 · 마스터 tex `\input` 차집합 orphan) · 증거 = 표 + 군별·전체 합계 + 명령 출력 첨부 + brief §3-C 건수·줄수 차이 파일 목록 + 판독 커버리지 대조(R# Read Coverage ⊆ OUT-INV) · untracked Claude 8 지위 / Codex 13 = 무접근 고정 기재(열람 0) · 유실 자산 원문 5본 등재(Assumptions 23).
- 게이트 1.1(L315): Test-Path True 100% · 줄수 빈 셀 0 · brief §3-C 차이 열거·정본 확정 · 배정표 차집합 0(Step 2) · 빌드 포함/미포함 60/60 · untracked Claude 8 지위 빈 셀 0 · Codex 13 무접근. 중단 조건 = 실물 부재는 "부재" 표기 후 진행(정지 아님).
- GO 직전 1g 실물 대조는 계획서 Correction History v5.2 행 + `handoffs/2026-09-02-v2-master-plan/wf/go_1g_check_2026-09-03.txt` 에 기록돼 있다(Assumptions 14 정정 1건 외 전건 참).

## 수행(시간순 · 2026-09-03)

| # | 시각 | 주체 | 행위 | 산출 |
|---|---|---|---|---|
| 1 | 09:2x | master | 마스터 플랜 전문 재독 · brief 저장(`handoffs/v1027-phase-1.1-inventory/brief.md`: 5항목 고지·입력 I-1~I-8·산출 A/B/C·실측 명령·양식 §1~§9·게이트 G1~G8) · 본 Step 파일 stub | brief · Step 1 stub |
| 2 | 09:24–10:10 | 작업 sub | brief 정독 → 실측 TSV(09:34:39 · 2,651행) → OUT-INV iter_1(1,463행 · 등재 665/93,005) → work_log · G1~G8 자체점검 전건 O · DQ 15 | `V1027_HISTORY_INVENTORY.md` · `iter_1/inventory_raw.tsv` · `iter_1/work_log.md` |
| 3 | 10:1x | master | DQ-9(plans +1)·DQ-14(tracked) 를 읽기 전용 git 으로 확인 · 생성 스크립트 보존 사본 복사(`iter_1/gen_outinv.ps1`, 10:16:52, 스크래치패드 원본과 SHA256 동일) | gen_outinv.ps1 |
| 4 | 10:14–10:3x | 검수 sub R1 | `audit_checklist.md` 4렌즈(구조·적대검산·완결성·usable) · 독립 재측정 R-a~R-i 전건 일치 · 발견 15(확정결함 1 AUD-01 등재 누락 11본 · 경미 8 · 제안 6) | `iter_1/audit_log.md` |
| 5 | 10:4x | master | 삼각검증 → 복원 지점 commit `72a0477`(iter_1) → iter_2 패치(AUD-01~15 전건 반영: (i-b)·(iv-b)·(viii-b) 26본 등재 · §10 처분표) + 계획서 v5.3(사실 정정 5건) | OUT-INV 1,566행 · 계획서 813행 |
| 6 | 10:5x–11:0x | 검수 sub R2 | `audit_checklist_r2.md` 4렌즈(regression·완결성·usable·구조) · iter_2 수치 전건 재현 · 발견 10(확정결함 1 AUD-R2-01 정책 미기계적용 잔여 19본+ · 경미 5 · 제안 4) | `iter_2/audit_log_r2.md` |
| 7 | 11:0x | master | 삼각검증 → 복원 지점 commit `cbc1d7c`(iter_2) → iter_3 패치: 「추가 발견」 정책 (a)(b)(b′)(c) 단위 정의 확정 + 31본 등재((iv-c) 21·(vii-b) 4(이동 1 포함)·(ix-b) 5·(xvii-b) 2) + `RB_AL_MASTER` 종류 정정 이동 + 이표기 2쌍 통일 + §8.3 표 스크립트 재생성 + 정책 잔여 스크립트 검사 → (a)(c) 0 · (b) 8 → iter_3b: (xvii-c) 계보 tex 6 · (viii-c) 결정 기록 2 등재 → **(a)(b)(c) 잔여 0**(`iter_3/policy_check.txt`) · 계획서 v5.4(§2.8 3곳·Assumptions 11·"지원 4본" 3곳·OUT-CLAUDEMD DR-13 후보) | OUT-INV 1,675행(등재 730/110,253) · 계획서 814행 |
| 8 | — | 검수 sub R3 | (대기) regression·완결성 — 연속 2R 확정결함 0 수렴 판정 | `iter_3/audit_log_r3.md` |

## 근거·판단(master · 4-tier)

1. **실측 정본(확정)** — plans 93 파일·10,384줄 · HANDOVER 25/1,612(old/ 제외)·28/1,915 · PLAN_* 15/645 + v1020 master 207 · `CLAUDE.md` 88 · 현행 tex 60/9,214(빌드 포함 = 마스터 3 + `\input` 53 = 56 · 미포함 4 = orphan `ch1_appD_si`·v1.0.21 잔재 `ch1_preamble`·`ch2_preamble` + 독립 부록 1) · v1.0.25 tex 60/9,207(v1.0.25.1 대비 hash 상이 tex 6) · 유실 원문 5본 존재 · untracked Claude 8 지위(png 5 유효·재생성 가능 / `C3_graph_check` 유효 / `C3_pdf_render` 유효·추정 상향 / `regsol_test` 폐기) · Codex 13 무접근 고정. 출처 = OUT-INV §3·§5·§6 · 검수 R1 독립 재측정 R-a~R-i 전건 일치(`iter_1/audit_log.md` §4).
2. **brief·계획서 기대와 다른 실측 3건(확정 → 계획서 정정 v5.3)** — ① 빌드 포함 58/미포함 2 → 56/4(preamble 2본은 어느 마스터에서도 `\input` 되지 않는 v1.0.21 잔재, `common_preamble_v1024.tex`:3 이 흡수 · 빌드 실사용 박스 정의 = `common_preamble_v1024.tex`:33–41) ② brief §3-C "HANDOVER 28(old/ 제외)" = old/ 포함 건수의 오기 ③ plans +1(1g 10,383 → 10,384) = 마스터 플랜 811→812(`git show 8d9362f` 811 · HEAD `f0c381b` 812 — v5.2 Correction History 행 추가, 검수 mtime 09:26:07 일치). 부수: `CLAUDE.md` 90 은 오기(mtime 2026-07-26 이후 무변경 · LF=CRLF=`wc -l`=88), `jcp_extract.txt` 725 = 끝 개행 없음, `HANDOVER_v1.0.10`·v1.0.12 인계 = 실물 부재.
3. **「추가 발견」 정책(master 확정 — OUT-INV §10.4)** — 검수 R1·R2 가 같은 뿌리(정책 비일관·미기계적용)를 두 번 지적했으므로 단위 정의를 문안으로 고정하고 스크립트로 증명했다: (a) 형제 = **파일명 계열**(같은 폴더 · 접두_핵심어 정규식; 접두만 같은 것은 계열 아님 → 접두 풀 ≈ 82본은 DQ-16 후보 풀·계수만) · (b) 통제 문서(프로젝트 `CLAUDE.md`·마스터 플랜·INDEX 3본)가 **이력·결정 근거로 인용**하는 md/tex 원문(가이드·코드·데이터·PDF·figs·`docs/` tex 본문 제외 — tex 본문은 2.1 자산 지도 소관; `old/` 소재 인용 tex(계보 원문)는 등재) · (b′) 등재 문서가 binding/입력으로 명시 인용하는 규약(charter) · (c) 동명 폴더 안 md 전건. 증거 = `iter_3/policy_check.txt`(정규식 28종 → 잔여 0 · 통제 문서 5본 인용 토큰 407건 → 잔여 0).
4. **hash 고유본 규칙(확정)** — 가장 이른 버전 폴더 · 버전 폴더 없는 구성원은 **ordinal** 경로 정렬 최상 · 같은 폴더 동명이물 2건(#179 `REVIEW_LEDGER_CH2_10ROUND`, #239 `graphite_ica_chapter2`)은 파일명 의미(base < rerun/fix)로 수동 지정 · 현행 tex 60 은 정독 경로 = `v1.0.25.1`.
5. **DQ 처분(master)** — OUT-INV §10.2·§10.4: 닫힘 = DQ-9·11·13·14·15 · 확정 = DQ-1·3·4·5·6·10 · 유지 = DQ-2(1.2 정독에서 확정) · 이관 = DQ-12(GAP 후보 → 2.1/2.5)·DQ-17(`CLAUDE.md` P1 인용 경로 스테일 → DR-13 OUT-CLAUDEMD) · **사용자 결정 대기(nonblocking, 기본값 현상 유지)** = DQ-7(untracked png 5 의 git 처리)·DQ-8(`C3_pdf_render/` 15.7 MiB 보존) → Phase 1.1 Result Decision Queue 로 이관 · 신규 DQ-16(접두 단위 후보 풀 = 1.2 Step 3 토픽 한정 열람 후보).
6. **검수 R1 AUD-09 관련 기록(확정)** — `out_versions/build.log` 36 은 R2 의 Read 표기 불일치(파일은 LF 36·끝 개행 True) — work_log 는 iter_1 기록으로 보존하고 OUT-INV (xi) 행 8 비고에 정정.
7. **계획서 정정(v5.3·v5.4 — 사실 정정만, 골격·Phase·Step·게이트 불변)** — §2.0 A1 · §2.2 orphan·자산 카운트 모집단·박스 환경 근거 · §2.6 구조 행 · §2.8 구조 맵 3곳 · §2.9 plans/HANDOVER/tex 행 · Phase Range 2.1 · 2.1 Step 14 · 2.2 청크·게이트 · 2.7 · T-4 · T-15 · Assumptions 11·12 · OUT-CLAUDEMD 행(DR-13 후보) · Correction History v5.3·v5.4 행. 2.1/2.2 줄수 좌표를 TSV 정의로 통일(361 / 8,853 = 9,214).
8. **추정·미검증 남김** — 버전 귀속 "추정" 행(2026-05-29~06-09 계획서·`results/process/PHASE_*` 계보·`anodefit-*`·`MASTER_ROADMAP_*`)은 1.2 Step 3·4 원천 정독에서 확정 · master 9,567 측정과 1g 총계의 차 1 은 측정 방식 차(추정)·미특정 · `C3_pdf_render` 지위는 폴더명 직접 참조 0 이라 추정 상향.

## 변경·생성 파일

- 생성: `Claude/results/V1027_HISTORY_INVENTORY.md`(OUT-INV · 작업 sub iter_1 → master iter_2/3/3b 정정) · `Claude/results/handoffs/v1027-phase-1.1-inventory/{brief.md, audit_checklist.md, audit_checklist_r2.md, iter_1/{inventory_raw.tsv, work_log.md, audit_log.md, gen_outinv.ps1}, iter_2/audit_log_r2.md, iter_3/policy_check.txt}` · 본 Step 파일.
- 갱신: `Claude/plans/2026-09-02-v2-master-plan.md` v5.2 → v5.3 → v5.4(Correction History 2행 — 사실 정정).
- 무변경: `Claude/docs/v1.0.24*`·`v1.0.25*`·`v1.0.26A/B` · `Codex/`(접근 0) · 판독 산출 R1~R7 · 작업 sub work_log(iter_1 기록 보존).
- commit: `72a0477`(iter_1 복원 지점) · `cbc1d7c`(iter_2+v5.3 복원 지점) · (Step 종료 시 검토·정정 commit 예정).

## 게이트

| 게이트 1.1(Step 1 몫) | 판정 | 근거 |
|---|---|---|
| Test-Path True 100% | O | OUT-INV §1 730 path 전건 TSV 존재(`policy_check` S=730 · 검수 R1 611/611·R2 637/637 재실행) |
| 줄수 열 빈 셀 0 | O | 730/730 숫자(TSV 값) |
| brief §3-C 차이 열거·정본 확정 | O | OUT-INV §3.1~3.5 |
| 빌드 포함/미포함 60/60 | O | OUT-INV §6(56/4 — 계획서 v5.3 정정) |
| untracked Claude 8 지위 · Codex 13 무접근 | O | OUT-INV §5 |
| 판독 커버리지 ⊆ | O | OUT-INV §7 131/131 |
| 정책 (a)(b)(b′)(c) 잔여 0 | O | `iter_3/policy_check.txt` |
| 검수 수렴(연속 2R 확정결함 0) | **대기** | R1 확정결함 1 → R2 확정결함 1 → R3·R4 필요 |
| 배정표 차집합 0 | N/A | Step 2 |

## 다음

- 검수 R3(regression·완결성) → 0 이면 R4(스킴 전환) → 수렴 시 검토·정정 commit → Step 2 정독 배정표(OUT-INV 730본 계보 순 정렬 · 청크 경계 · 정독 주체 열 · ①군 전문 / ②군 토픽 한정 · DQ-16 풀 부록) → 게이트 1.1 → `PHASE_1.1_V1027_INV_RESULT.md`+`.json` → Ledger 행 → push.
